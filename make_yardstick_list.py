import csv
import json

with open("./model_training/rawdata/yarstick_papers.csv", "r") as f:
    bib = list(csv.DictReader(f))

# Yardstick paper stack
cols = ["year", "author", "title", "journal", "doi"]
bib = [{k: row[k] for k in cols} for row in bib]
bib.sort(key=lambda x: x["year"], reverse=True)

with open("./output/yardstick_papers.json", "w") as f:
    json.dump(bib, f)
