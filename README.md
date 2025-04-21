# Immigration Paper

Immigration Papers provides a weekly dashboard of newly published research on immigration in political science, sociology, and economics. The workflow is automated and timed using GitHub Actions. The data comes from [paper-picnic.com](https://paper-picnic.com/), which queries the Crossref API to identify new research articles published in the past week across more than 60 journals in political science and adjacent fields. 

To build your own dashboard, fork the repository, swap the yardstick data in `/parameters/rawdata/yardstick_papers.csv` and call `yardstick.R` locally. Then make changes to the Github repository settings for it to function properly.

1. Go to Settings > Actions > General. Scroll down to Workflow permissions and allow workflows to read and write in the repository.

2. Go to Security > Secrets and Variables > Actions. Set `OPENOPENAI_APIKEY` in as a repository secret. The latter is used to query the OpenAI API. 