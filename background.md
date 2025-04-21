---
title: "Immigration Papers"
layout: home
image: "./assets/img/figure.png"
---

{% assign yardstick = site.data.yardstick_papers %}

Immigration Papers provides a weekly dashboard of newly published research on immigration in political science, sociology, and economics. Each paper is ranked based on its similarity to a set of benchmark (or "yardstick") papers, using a score derived from the highest cosine similarity between text embeddings of the paper’s title and abstract and those of the yardstick papers.

Our source data comes from [paper-picnic.com](https://paper-picnic.com/), which queries the Crossref API to identify new research articles published in the past week across more than 60 journals in political science and adjacent fields. Crossref is the world’s largest registry of Digital Object Identifiers (DOIs) and metadata. Continuously updated by publishers, Crossref provides an easy way to get metadata for research articles.

To assess similarity, we use OpenAI’s latest `text-embedding-3-large` model to convert the titles and abstracts of each paper into 3,072-dimensional vector representations. These text embeddings capture the semantic meaning and contextual relationships in the text. By comparing these vectors using cosine similarity, we identify papers that are most aligned—conceptually and contextually—with the yardstick set.

The yardstick paper stack is a collection of {{yardstick.size}} papers sourced from my syllabus [The Politics of Immigration](https://www.moritz-marbach.com/assets/download/Marbach_Bush689.pdf): 

{% for pub in yardstick %}
- {{ pub.author }}. {{ pub.year }}. 
[{{ pub.title }}]({{ pub.doi | prepend: "https://doi.org/" }}). _{{ pub.journal }}_
{% endfor %}


