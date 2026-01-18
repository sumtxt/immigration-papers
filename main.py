import argparse

from pipeline import (
    fetch_data,
    is_updated_today,
    crawl,
    rank,
    post_to_slack,
    save_output,
)


def main():
    parser = argparse.ArgumentParser(description="Run the immigration papers pipeline")
    parser.add_argument(
        "--slack",
        action="store_true",
        help="Post to Slack after ranking",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Run even if data was not updated today",
    )
    args = parser.parse_args()

    # Fetch data once
    print("Fetching data...")
    journals, publications, preprints = fetch_data()

    # Check update date
    if not args.force and not is_updated_today(publications):
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
    if args.slack:
        print("Posting to Slack...")
        post_to_slack(papers)

    print("Done.")


if __name__ == "__main__":
    main()
