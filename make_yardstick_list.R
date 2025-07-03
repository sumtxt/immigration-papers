library(readr)
library(jsonlite)

bib <- read_csv("./model_training/rawdata/yarstick_papers.csv")

# Yardstick paper stack 
bib <- subset(bib, select=c("year", "author", "title", "journal", "doi"))
bib <- bib[order(bib$year*(-1)),]
write(toJSON(bib), "./output/yardstick_papers.json")
