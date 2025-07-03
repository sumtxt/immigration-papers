---
title: "Immigration Papers"
layout: home
image: "./assets/img/figure.png"
---

Immigration Papers provides a weekly dashboard of newly published research on immigration in political science, sociology, and economics. Each paper's relevance is determined by a text classification model, which computes a predicted probability that the study is related to immigration research. Given limited training data and a desire to minimize the computing footprint, we use SetFit to fine-tune a mini sentence transformer (paraphrase-MiniLM-L3-v2)[https://huggingface.co/sentence-transformers/paraphrase-MiniLM-L3-v2]. For details, see the original [paper](https://arxiv.org/abs/2209.11055) and [blog post](https://huggingface.co/blog/setfit) of the SetFit authors.

The source data comes from [paper-picnic.com](https://paper-picnic.com/), which queries the Crossref API to compile new research articles published in the past week across more than 60 journals in political science and adjacent fields. Crossref is the world’s largest registry of Digital Object Identifiers (DOIs) and metadata. Continuously updated by publishers, Crossref provides an easy way to obtain metadata for research articles.

The text classification model was trained on a random sample of 24 title-abstract pairs sourced from the syllabus [The Politics of Immigration](https://www.moritz-marbach.com/assets/download/Marbach_Bush689.pdf), along with an equally sized random sample of non-immigration-related title-abstract pairs from the Paper Picnic corpus in June 2025. Despite some longer title-abstracts being truncated due to the limited context window of the mini sentence transformer, a test-set evaluation shows a classification accuracy of 0.99 (F1: 0.99). The model is available on Hugging Face [here](https://huggingface.co/mmarbach/paraphrase-MiniLM-L3-v2_immig). All code, including the training data and training script, is available on [GitHub](https://github.com/sumtxt/immigration-papers).

The dashboard is fully automated via GitHub Actions, which retrieves the data, runs the classifier, and generates the dashboard on Fridays.