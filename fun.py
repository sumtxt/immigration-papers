import re
import time
import requests
import pandas as pd

from credentials import SLACK_WORKFLOW_TRIGGER_URL


def extract_doi_id(url: str) -> str:
    return re.sub(r"https?://(dx\.)?doi\.org/", "", url)


#################
#################
# Post to Slack #
#################
#################

def paper_to_slack(paper: dict) -> requests.Response:
    response = requests.post(
        url=SLACK_WORKFLOW_TRIGGER_URL,
        json=paper,
        headers={"Content-Type": "application/json"},
    )
    return response


def all_papers_to_slack(
    papers: pd.DataFrame, wait_in_seconds: int = 2, rate_limit_per_minute: int = 10
):
    if len(papers) == 0:
        return None

    start_time = time.time()

    papers = papers[["title", "authors", "abstract", "url"]]

    for i, (_, row) in enumerate(papers.iterrows(), start=1):
        print(".", end="", flush=True)
        paper = row.to_dict()
        response = paper_to_slack(paper)
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
