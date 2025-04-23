---
title: "Immigration Papers"
layout: home
image: "./assets/img/figure.png"
---

{% assign yardstick = site.data.yardstick_papers %}

Immigration Papers provides a weekly dashboard of newly published research on immigration in political science, sociology, and economics. Each paper is ranked based on its similarity to a set of benchmark (or "yardstick") papers, using a score derived from the highest cosine similarity between text embeddings of the paper’s title and abstract and those of the yardstick papers.

The source data comes from [paper-picnic.com](https://paper-picnic.com/), which queries the Crossref API to identify new research articles published in the past week across more than 60 journals in political science and adjacent fields. Crossref is the world’s largest registry of Digital Object Identifiers (DOIs) and metadata. Continuously updated by publishers, Crossref provides an easy way to get metadata for research articles.

To assess similarity, OpenAI’s latest `text-embedding-3-large` model converts the titles and abstracts of each paper into 3,072-dimensional vector representations. These text embeddings capture the semantic meaning and contextual relationships in the text. Comparing these vectors using cosine similarity identifies papers most aligned—conceptually and contextually—with the yardstick set. 

The process is fully automated via Github Actions which retrieves the data, computes the similarity scores, and generates the dashboard on Fridays. All code is available on [GitHub](https://github.com/sumtxt/immigration-papers). 

The yardstick paper stack consists of {{yardstick.size}} papers sourced from the syllabus [The Politics of Immigration](https://www.moritz-marbach.com/assets/download/Marbach_Bush689.pdf): 

{% for pub in yardstick %}
- {{ pub.author }}. {{ pub.year }}. 
[{{ pub.title }}]({{ pub.doi | prepend: "https://doi.org/" }}). _{{ pub.journal }}_
{% endfor %}


