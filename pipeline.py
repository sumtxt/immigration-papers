import json
import os
import re
import time
from datetime import date

import pandas as pd
import requests
from setfit import SetFitModel

BASE_URL = "https://beta.paper-picnic.com/data/"


def extract_doi_id(url: str) -> str:
    return re.sub(r"https?://(dx\.)?doi\.org/", "", url)


def fetch_data() -> tuple[list, dict, dict]:
    """Fetch all data from the API. Returns (journals, publications, preprints)."""
    journals = requests.get(f"{BASE_URL}journals.json").json()
    publications = requests.get(f"{BASE_URL}publications.json").json()
    preprints = requests.get(f"{BASE_URL}preprints.json").json()
    return journals, publications, preprints


def get_update_date(publications: dict) -> str:
    """Extract update date from publications data."""
    return publications.get("update")


def is_updated_today(publications: dict) -> bool:
    """Check if the data was updated today."""
    update_date = get_update_date(publications)
    today = date.today().isoformat()
    return update_date == today


def crawl(journals: list, publications: dict, preprints_data: dict) -> tuple[pd.DataFrame, dict]:
    """Process raw data into papers DataFrame and metadata."""
    update_date = get_update_date(publications)
    journal_count = len(journals)

    # Build journal lookups
    journal_lookup = {j["id"]: j["name"] for j in journals}
    journal_category_lookup = {j["id"]: j.get("category", "") for j in journals}

    # Process publications
    pubs_list = []
    for journal in publications.get("content", []):
        journal_id = journal.get("journal_id")
        journal_name = journal.get("journal_name", journal_lookup.get(journal_id, ""))
        is_specialized = journal_category_lookup.get(journal_id, "") == "Migration Studies"

        for article_list in [journal.get("articles", []), journal.get("articles_hidden", [])]:
            for art in article_list:
                pubs_list.append({
                    "title": art.get("title"),
                    "authors": art.get("authors"),
                    "abstract": art.get("abstract"),
                    "url": art.get("doi"),
                    "journal_full": journal_name,
                    "specialized": is_specialized,
                })

    pubs = pd.DataFrame(pubs_list)
    pubs["preprint"] = False
    pubs["doi"] = pubs["url"].apply(extract_doi_id)

    # Process preprints
    preprints_list = []
    for prep in preprints_data.get("content", {}).get("articles", []):
        preprints_list.append({
            "title": prep.get("title"),
            "authors": prep.get("authors"),
            "abstract": prep.get("abstract"),
            "url": prep.get("doi"),
        })

    preprints = pd.DataFrame(preprints_list)
    preprints["specialized"] = False
    preprints["preprint"] = True
    preprints["journal_full"] = "(SocArXiv/OSF Preprints)"
    preprints["doi"] = preprints["url"].apply(extract_doi_id)

    # Combine
    common_cols = ["title", "authors", "abstract", "url", "doi", "journal_full", "specialized", "preprint"]
    papers = pd.concat([pubs[common_cols], preprints[common_cols]], ignore_index=True)

    meta = {"update_date": update_date, "journal_count": journal_count}

    return papers, meta


def rank(papers: list[dict]) -> list[dict]:
    """Add relevance scores to papers using the ML model."""
    model = SetFitModel.from_pretrained("sumtxt/paraphrase-MiniLM-L3-v2_immig")

    for paper in papers:
        input_text = f"TITLE: {paper.get('title', '')} \nABSTRACT: {paper.get('abstract', '')}"
        paper["score"] = model.predict_proba([input_text])[0][0].item()

    return papers


def post_to_slack(papers: list[dict]):
    """Post high-scoring papers to Slack."""
    df = pd.DataFrame(papers).fillna("")
    df = df[(df["score"] >= 0.5) & ~df["specialized"]]

    _all_papers_to_slack(df[~df["preprint"]])
    _all_papers_to_slack(df[df["preprint"]])


def _paper_to_slack(paper: dict) -> requests.Response:
    slack_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not slack_url:
        raise RuntimeError("SLACK_WEBHOOK_URL environment variable not set")
    response = requests.post(
        url=slack_url,
        json=paper,
        headers={"Content-Type": "application/json"},
    )
    return response


def _all_papers_to_slack(
    papers: pd.DataFrame, wait_in_seconds: int = 2, rate_limit_per_minute: int = 10
):
    if len(papers) == 0:
        return None

    start_time = time.time()
    papers = papers[["title", "authors", "abstract", "url"]]

    for i, (_, row) in enumerate(papers.iterrows(), start=1):
        print(".", end="", flush=True)
        paper = row.to_dict()
        response = _paper_to_slack(paper)
        result = response.json()

        if result.get("ok") is not True:
            raise RuntimeError(f"Error in posting to Slack: {result}")

        if i % rate_limit_per_minute == 0:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, 60 - elapsed_time)
            time.sleep(remaining_time)
            start_time = time.time()
        else:
            time.sleep(wait_in_seconds)

    print()


def save_output(papers: list[dict], meta: dict):
    """Save papers and metadata to JSON files."""
    with open("./output/papers.json", "w") as f:
        json.dump(papers, f, indent=None, ensure_ascii=False)

    with open("./output/meta.json", "w") as f:
        json.dump(meta, f)
