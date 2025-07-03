library(httr)
library(jsonlite)

source("fun.R")
source("credentials.R")

papers <- read_json("./output/papers.json", simplifyVector=TRUE)

# Post Top 10 to Slack 
papers <- papers[papers$prob>=0.5,]
papers <- subset(papers, specialized==FALSE)

all_papers_to_slack(subset(papers, preprints=FALSE, select=c("title", "authors", "abstract", "url") ))
all_papers_to_slack(subset(papers, preprints=TRUE, select=c("title", "authors", "abstract", "url") ))
