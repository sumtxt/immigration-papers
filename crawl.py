import json
import pandas as pd
import requests

from fun import extract_doi_id

BASE_URL = "https://beta.paper-picnic.com/data/"

# Fetch all data in 3 requests (instead of 7)
journals = requests.get(f"{BASE_URL}journals.json").json()
publications = requests.get(f"{BASE_URL}publications.json").json()
preprints_data = requests.get(f"{BASE_URL}preprints.json").json()

# Extract metadata
update_date = publications.get("update")
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
preprints["journal_full"] = "(OSF Preprints)"
preprints["doi"] = preprints["url"].apply(extract_doi_id)

# Output to public dashboard
common_cols = ["title", "authors", "abstract", "url", "doi", "journal_full", "specialized", "preprint"]
papers = pd.concat([pubs[common_cols], preprints[common_cols]], ignore_index=True)

with open("./output/papers.json", "w") as f:
    json.dump(papers.to_dict(orient="records"), f)

meta = {"update_date": update_date, "journal_count": journal_count}
with open("./output/meta.json", "w") as f:
    json.dump(meta, f)
