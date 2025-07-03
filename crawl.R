library(httr)
library(jsonlite)

source("fun.R")

s <- NULL

update_date <- get_paper_picnic_update_date()
# check_update_date(update_date)

journal_count <- get_paper_picnic_journal_count()

# Crawl Paper Picnic 
pubs <- get_paper_picnic(sample=s)$content 

pubs$specialized <- (pubs$file=="migration.json")
pubs$preprint <- FALSE
pubs$doi <- extract_doi_id(pubs$url)

pubs <- within(pubs, {
    file <- NULL
    vec <- NULL
})

# Crawl Preprint Picnic  
preprints <- get_preprint_picnic(sample=s)$content 

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

# Output to public dashboard
papers <- rbind(pubs[,colnames(pubs)], preprints[,colnames(pubs)])
write(toJSON(papers), file="./output/papers.json")

meta <- list(update_date=update_date, journal_count=journal_count)
write(toJSON(meta,auto_unbox=TRUE), file="./output/meta.json")