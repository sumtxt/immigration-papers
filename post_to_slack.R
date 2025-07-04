library(httr)
library(jsonlite)

source("fun.R")
source("credentials.R")

papers <- read_json("./output/papers.json", simplifyVector=TRUE)

# Post Top 10 to Slack 
papers <- papers[papers$score>=0.5,]
papers <- subset(papers, specialized==FALSE)

all_papers_to_slack(subset(papers, preprint==FALSE))
all_papers_to_slack(subset(papers, preprint==TRUE))
