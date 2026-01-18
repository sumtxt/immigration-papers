import argparse
import subprocess
import sys


def run_script(script: str):
    print(f"Running {script}...")
    result = subprocess.run([sys.executable, script], check=True)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run the immigration papers pipeline")
    parser.add_argument(
        "--no-slack",
        action="store_true",
        help="Skip posting to Slack",
    )
    args = parser.parse_args()

    run_script("crawl.py")
    run_script("rank.py")

    if not args.no_slack:
        run_script("post_to_slack.py")
    else:
        print("Skipping post_to_slack.py")

    print("Done.")


if __name__ == "__main__":
    main()
