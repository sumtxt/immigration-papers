extract_doi_id <- function(url){
    return(gsub("http(|s)://(dx.|)doi.org/", "", url))
    }

############
############
# Crawlers #
############
############

add_col <- function(data, cname) {
    add <- cname[!cname %in% names(data)]
    if (length(add) != 0) data[add] <- NA
    return(data)
}

get_paper_picnic <- function(exclude = NULL, include = NULL, sample=NULL) {
    # Set parameters
    baseurl <- "https://paper-picnic.com/json/"

    files <- c(
        "politics.json",
        "communication.json",
        "economics.json",
        "migration.json",
        "multidisciplinary.json",
        "public_administration_and_policy.json",
        "sociology.json"
    )

    col_names <- c(
        "title", "authors",
        "abstract", "url",
        "doi", "filter"
    )

    # Prepare
    if (!is.null(exclude)) {
        files <- files[!files %in% exclude]
    }
    if (!is.null(include)) {
        files <- include
    }

    lst <- list()

    # Get each file and turn to data.frame
    for (file in files) {
        data <- fromJSON(paste0(baseurl, file))

        update <- data$update
        data <- data$content

        N_articles <- lapply(data$articles, nrow)

        articles <- data$articles[N_articles != 0]
        journal_full <- data$journal_full[N_articles != 0]
        K_journals <- length(articles)

        for (k in 1:K_journals) {
            tmp <- articles[[k]]
            tmp <- add_col(tmp, col_names)
            tmp$journal_full <- journal_full[k]
            tmp$file <- basename(file)
            articles[[k]] <- tmp
        }

        tmp <- do.call(rbind, articles)
        lst[[file]] <- tmp
    }

    data <- do.call(rbind, lst)
    rownames(data) <- NULL
    data$filter <- NULL

    if(!is.null(sample)){
        row <- sample(1:nrow(data), sample)
        data <- data[row, ]
    }

    data <- list(update = update, content = data)
    return(data)
}


get_preprint_picnic <- function(sample=NULL) {
    
    baseurl <- "https://preprint.paper-picnic.com/json/osf.json"

    data <- fromJSON(baseurl)
    update <- data$update
    data <- list(data$content$articles, data$content$articles_hidden)
    data <- do.call(rbind, data)

    if(!is.null(sample)){
        row <- sample(1:nrow(data), sample)
        data <- data[row, ]
    }

    data <- list(update = update, content = data)
    return(data)
}

get_paper_picnic_update_date <- function(){
 
    # Set parameters
    pubs <- paste0("https://paper-picnic.com/json/", c(
        "politics.json",
        "communication.json",
        "economics.json",
        "migration.json",
        "multidisciplinary.json",
        "public_administration_and_policy.json",
        "sociology.json"
    ))

    files <- c(pubs, "https://preprint.paper-picnic.com/json/osf.json" )
    lst <- list()

    # Get each file and turn to data.frame
    for (file in files) {
        lst[file] <- fromJSON(file)$update
    }
    update_date <- unique(unlist(lst))
    
    return(update_date)
    }


get_paper_picnic_journal_count <- function(){ 

    files <- paste0("https://paper-picnic.com/json/", c(
        "politics_journals.json",
        "communication_journals.json",
        "economics_journals.json",
        "migration_journals.json",
        "multidisciplinary_journals.json",
        "public_administration_and_policy_journals.json",
        "sociology_journals.json"
    ))

    count <- 0
    for (file in files) {
        count <- count + nrow(fromJSON(file))

    }
    return(count)
    }


check_update_date <- function(update_date){

    if(length(update_date) != 1){
        stop("Update date is not the same for all files")
    }
    if(update_date != Sys.Date()){
        stop("Update date is not today")
    }

}


#################
#################
# Post to Slack #
#################
#################

paper_to_slack <- function(paper) {
    response <- POST(
        url = .slack_workflow_trigger_url,
        body = toJSON(paper, auto_unbox = TRUE),
        add_headers(`Content-Type` = "application/json")
    )

    return(response)
}

all_papers_to_slack <- function(papers, wait_in_seconds = 2, rate_limit_per_minute = 10) {
    start_time <- Sys.time()

    N <- nrow(papers)
    if(N==0) return(NULL)
    
    papers <- subset(papers, select=c("title", "authors", "abstract", "url"))

    for (i in 1:N) {
        cat(".")
        paper <- as.vector(papers[i, ])
        response <- content(paper_to_slack(paper))

        if (response$ok != TRUE) stop("Error in posting to Slack: ", response)

        if (i %% rate_limit_per_minute == 0) {
            elapsed_time <- as.numeric(difftime(Sys.time(), start_time, units = "secs"))
            remaining_time <- max(0, 60 - elapsed_time)
            Sys.sleep(remaining_time)
            start_time <- Sys.time()
        } else {
            Sys.sleep(wait_in_seconds)
        }
    }
}