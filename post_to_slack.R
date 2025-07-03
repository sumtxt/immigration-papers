library(httr)
library(jsonlite)

source("fun.R")
source("credentials.R")

# Post Top 10 to Slack 
papers <- papers[order(-1*papers$dist),]
papers <- subset(papers, specialized==FALSE & preprint==FALSE, select=c("title", "authors", "abstract", "url"))
papers <- papers[1:10,]
all_papers_to_slack(papers)
