Immigration Papers
===================

Immigration Papers offers a weekly dashboard showcasing newly published research on immigration in political science, sociology, and economics. The process is fully automated and scheduled using GitHub Actions. Data is sourced from [beta.paper-picnic.com](https://beta.paper-picnic.com), which queries the Crossref API to track recent publications across more than 60 journals in political science and related fields.

To create your own version of the dashboard, fork the repository, replace the yardstick data in `/parameters/rawdata/yardstick_papers.csv`, and run `yardstick.R` locally. You’ll also need to update the GitHub repository settings: Navigate to Settings > Actions > General. Scroll to Workflow permissions and enable workflows to read and write to the repository.