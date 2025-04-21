library(RefManageR)
library(bibtex)
library(jsonlite)
library(httr)

source("fun.R")
source("credentials.R")

bib <- ReadBib("./parameters/rawdata/yardstick_articles.bib")

bib <- as.data.frame(bib)
bib <- subset(bib, subset=bibtype!="Book", 
        select=c("title", "abstract"))

bib$title <- gsub("\\{|\\}", "", bib$title)
bib$abstract <- gsub("\\n|\\t}", " ", bib$abstract)
bib$abstract <- gsub("  *", " ", bib$abstract)
rownames(bib) <- NULL 

table(is.na(bib$title))
table(is.na(bib$abstract))

write(toJSON(bib), file="./parameters/rawdata/yarstick_articles.json")

str <- with(bib, paste0("Title: ", title, "\n Abstract: ", ifelse(is.na(abstract), "", abstract)))
vec <- lapply(str, function(x) get_openai_embedding(x)) 
write(toJSON(vec), "./parameters/yardstick.json")
