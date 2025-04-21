library(jsonlite)
library(httr)

source("fun.R")
source("credentials.R")

# Compute yardstick 
bib <- read_csv("./parameters/rawdata/yarstick_articles_new.csv")
str <- with(bib, paste0("Title: ", title, "\n Abstract: ", ifelse(is.na(abstract), "", abstract)))
vec <- lapply(str, function(x) get_openai_embedding(x)) 
write(toJSON(vec), "./parameters/yardstick.json")

# Yardstick paper stack 
bib <- subset(bib, select=c("year", "author", "title", "journal", "doi"))
write(toJSON(bib), "./output/yardstick_papers.json")
