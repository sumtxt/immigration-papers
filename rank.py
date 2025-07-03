import json
from setfit import SetFitModel

# Load the pre-trained model
model = SetFitModel.from_pretrained("mmarbach/paraphrase-MiniLM-L3-v2_immig")

# Load the papers data
with open("./output/papers.json", "r") as f:
    papers = json.load(f)

# Add probabilities
for paper in papers:
    input_text = f"TITLE: {paper.get('title', '')} \nABSTRACT: {paper.get('abstract', '')}"
    paper['score'] = model.predict_proba([input_text])[0][0].item()

# Save the updated papers data
with open("./output/papers.json", "w") as f:
    json.dump(papers, f, indent=None)
