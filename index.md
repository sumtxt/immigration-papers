---
title: "Dashboard"
layout: main
---

{% assign data_crawl = site.data.papers | sort: 'score' | reverse %} 
{% include cards.html %}


