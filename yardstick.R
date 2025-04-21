library(readr)
library(jsonlite)
library(httr)

source("fun.R")
source("credentials.R")

bib <- read_csv("./parameters/rawdata/yarstick_papers.csv")

# Compute yardstick 
str <- with(bib, paste0("Title: ", title, "\n Abstract: ", ifelse(is.na(abstract), "", abstract)))
vec <- lapply(str, function(x) get_openai_embedding(x)) 
write(toJSON(vec), "./parameters/yardstick.json")

# Yardstick paper stack 
bib <- subset(bib, select=c("year", "author", "title", "journal", "doi"))
bib <- bib[order(bib$year*(-1)),]
write(toJSON(bib), "./output/yardstick_papers.json")
