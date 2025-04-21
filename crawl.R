library(httr)
library(jsonlite)
library(coop)

source("fun.R")
source("credentials.R")

s <- NULL 

update_date <- get_paper_picnic_update_date()
# check_update_date(update_date)

# Crawl Paper Picnic 
pubs <- get_paper_picnic(sample=s)$content |> 
    add_openai_embedding() |> 
    add_yardstick_distance()

pubs$specialized <- (pubs$file=="migration.json")
pubs$preprint <- FALSE
pubs$doi <- extract_doi_id(pubs$url)

pubs <- within(pubs, {
    file <- NULL
    vec <- NULL
})

# Crawl Preprint Picnic  
preprints <- get_preprint_picnic(sample=s)$content |> 
    add_openai_embedding() |> 
    add_yardstick_distance()

preprints$specialized <- FALSE
preprints$preprint <- TRUE
preprints$journal_full <- "(OSF Preprints)"

preprints <- within(preprints, {
    file <- NULL
    created <- NULL
    subjects <- NULL 
    subjects_osf <- NULL
    vec <- NULL
})

papers <- rbind(pubs[,colnames(pubs)], preprints[,colnames(pubs)])
write(toJSON(papers), file="./output/papers.json")

write(toJSON(update_date), file="./output/update_date.json")
