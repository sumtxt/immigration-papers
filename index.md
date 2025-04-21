---
title: "Immigration Papers"
layout: home
---

Immigration Papers displays a list of immigration-related papers in the fields of political science, sociology and economics weekly. The list ranking is determiend by a score that is a function of how similar a paper is to a set of yardstick papers. Technically, the score is a the maximum cosine similarity of the papers' text embedding with any of the text embedding for the yardstick papers. 

### Details 

The source data comes from [paper-picnic.com](https://paper-picnic.com/) which queries the Crossref API for new research articles that appeared in the previous 7 days across more than 60 journals in political science and adjacent fields. Crossref is the world’s largest registry of Digital Object Identifiers (DOIs) and metadata. Continuously updated by publishers, Crossref provides an easy way to get metadata for research articles.

To compute the similarity between the yardstick paper stack, the title and abstract are embedded using the OpenAI latest `text-embedding-3-large` embedding model (3072 dimensions). 

  


#### Yardstick papers 

The following papers are used as yardstick paper stack: 


