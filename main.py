import os

from pipeline import (
    fetch_data,
    is_updated_today,
    crawl,
    rank,
    post_to_slack,
    save_output,
)


def env_bool(name: str, default: bool = False) -> bool:
    """Read a boolean from environment variable."""
    return os.environ.get(name, "").lower() in ("true", "1", "yes")


def main():
    slack = env_bool("PIPELINE_SLACK")
    force = env_bool("PIPELINE_FORCE")

    # Fetch data once
    print("Fetching data...")
    journals, publications, preprints = fetch_data()

    # Check update date
    if not force and not is_updated_today(publications):
        print("Data was not updated today. Skipping pipeline. Use --force to override.")
        return

    # Crawl
    print("Processing papers...")
    papers, meta = crawl(journals, publications, preprints)
    papers = papers.to_dict(orient="records")

    # Rank
    print("Ranking papers...")
    papers = rank(papers)

    # Save
    print("Saving output...")
    save_output(papers, meta)

    # Post to Slack
    if slack:
        print("Posting to Slack...")
        post_to_slack(papers)

    print("Done.")


if __name__ == "__main__":
    main()
