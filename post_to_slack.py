import json
import pandas as pd

from fun import all_papers_to_slack

with open("./output/papers.json", "r") as f:
    papers = pd.DataFrame(json.load(f))

# Post to Slack
papers = papers[(papers["score"] >= 0.5) & ~papers["specialized"]]

all_papers_to_slack(papers[~papers["preprint"]])
all_papers_to_slack(papers[papers["preprint"]])
