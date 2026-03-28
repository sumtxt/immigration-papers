Immigration Papers
===================

Immigration Papers offers a weekly dashboard showcasing newly published research on immigration in political science, sociology, and economics. The process is fully automated and scheduled using GitHub Actions. Data is sourced from [paper-picnic.com](https://paper-picnic.com), which queries the Crossref API to track recent publications across more than 140 journals in political science and related fields.

## How It Works

The pipeline runs every Friday at 5 AM UTC and performs the following steps:

1. **Fetch Data** - Downloads the latest publications and preprints from paper-picnic.com
2. **Process Papers** - Extracts title, authors, abstract, DOI, and journal information
3. **Rank Papers** - Uses a fine-tuned [SetFit](https://huggingface.co/docs/setfit) model ([sumtxt/paraphrase-MiniLM-L3-v2_immig](https://huggingface.co/sumtxt/paraphrase-MiniLM-L3-v2_immig)) to score each paper's relevance to immigration research (0-1)
4. **Save Output** - Writes results to `output/papers.json` and `output/meta.json`
5. **Notify** - Posts high-scoring papers (score >= 0.5) to Slack (optional)

Papers from specialized migration journals are flagged separately and excluded from Slack notifications since they are all immigration-related by definition.

## Requirements

- Python 3.12
- Dependencies: `requests`, `pandas`, `setfit`, `transformers`

Install with:
```bash
pip install -r requirements.txt
```

## Usage

Run the pipeline locally:
```bash
python main.py
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `PIPELINE_SLACK` | Set to `true` to post results to Slack |
| `PIPELINE_FORCE` | Set to `true` to run even if data hasn't been updated today |
| `SLACK_WEBHOOK_URL` | Slack webhook URL for notifications |

## Project Structure

```
.
├── main.py                 # Entry point
├── pipeline.py             # Core pipeline functions
├── requirements.txt        # Python dependencies
├── output/
│   ├── papers.json         # Latest papers with relevance scores
│   └── meta.json           # Update date and journal count
├── model_training/         # ML model training scripts and data
│   ├── train_model.py      # SetFit model training
│   └── rawdata/            # Training data
└── .github/workflows/
    ├── crawl.yml           # Weekly data pipeline
    └── update.yml          # Syncs output to gh-pages
```

## Create Your Own Dashboard

1. Fork this repository
2. Replace the yardstick data in `model_training/rawdata/yardstick_papers.csv` with your own curated papers
3. Train a new model using `model_training/train_model.py`
4. Update repository settings: Navigate to **Settings > Actions > General**, scroll to **Workflow permissions**, and enable read/write access
5. (Optional) Add a `SLACK_WEBHOOK` secret for Slack notifications

# History

The first version of the dashboard went live in April 2025. The codebase was ported from R to Python in January 2026.