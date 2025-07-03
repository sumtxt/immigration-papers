library(tidyverse)
library(jsonlite)

yardstick <- read_csv("./rawdata/yarstick_papers.csv")
week27 <- read_json("./rawdata/papers_2025-06-27_exSpezialized_exPreprints_exNoAbstract_coded.json", simplifyVector=TRUE) 
week20 <- read_json("./rawdata/papers_2025-06-20_exSpezialized_exPreprints_exNoAbstract_coded.json", simplifyVector=TRUE) 

week <- bind_rows(week27, week20) %>% 
    select(title, abstract, decision) %>% 
    filter(decision!="exclude") %>% 
    mutate(decision=ifelse(decision=="yes", "immigration_topic", "other_topic")) %>% 
    rename(label=decision) 

set.seed(41)
week0 <- week %>% filter(label=="other_topic") %>% sample_n(40)

yardstick <- yardstick %>% 
    select(title, abstract) %>% 
    mutate(label="immigration_topic")

train <- bind_rows(yardstick, week0) %>% 
    group_by(label) %>% 
    slice_sample(prop = 1) %>% 
    mutate(batch=rep(1:5, 8)) 

test <- week %>% filter(!(title %in% week0$title))

train <- train %>% mutate(string = paste0("TITLE: ", title, "\nABSTRACT: ", abstract)) %>% 
    select(text=string, label, batch)

test <- test %>% mutate(string = paste0("TITLE: ", title, "\nABSTRACT: ", abstract)) %>% 
    select(text=string, label)

write_csv(train, "./usedata/train.csv")
write_csv(test, "./usedata/test.csv")