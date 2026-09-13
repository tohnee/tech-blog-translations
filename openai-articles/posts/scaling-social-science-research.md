---
title: "Scaling social science research"
date: 2026-02-13
source: https://openai.com/index/scaling-social-science-research/
crawled: 2026-09-13
category: research
---

A core part of our work at OpenAI is enabling scientists to move faster and solve harder problems. Today, our Economic Research Team is releasing GABRIEL: an open-source toolkit that uses GPT to turn unstructured text and images into quantitative measurements. It is designed for economists, social scientists, and data scientists to study qualitative data at scale.

Qualitative data tells the richest stories about the world—what people say, write, teach, argue, and experience. It spans everything from syllabi and interviews to social media and photographs. There is a tremendous amount of it. But transforming that type of data into rigorous evidence is incredibly time-consuming. Often it isn’t feasible at all. In too many cases, social scientists are forced to forego important avenues of research, not because the data doesn’t exist, but because it’s impossible to analyze.

GABRIEL is built to make qualitative data much more accessible. It allows researchers to describe what they want to measure in everyday words—like “how family-friendly is this job listing?”—and then applies that same question consistently across thousands (or millions) of documents, returning a score for each one. This lets researchers spend less time on repetitive data labeling and more time on the work that actually requires expertise: choosing what to measure, validating results, and drawing careful conclusions.

For example, GABRIEL can analyze a large collection of scientific papers to see what specific methods are used and how they evolve over time. It can look at course curricula to measure how much attention is given to different subjects or skills. It can extract structured historical details for every small town across Europe, or examine a trove of customer reviews and discover patterns in what people value most. In[our paper⁠(opens in a new window)](https://cdn.openai.com/pdf/7517a586-5bfa-4b87-bd3d-6ea0e9e844c7/GPT-as-a-measurement-tool.pdf), we benchmark GPT at labeling qualitative data across many use cases and find that it is highly accurate.

Beyond this type of measurement, GABRIEL also provides practical tools researchers often need. These include merging datasets even when the columns don’t match, smart deduplication, passage coding, ideating new scientific theories, and deidentifying personal information from text to preserve privacy.

GABRIEL is available now as an[open-source Python library⁠(opens in a new window)](https://github.com/openai/GABRIEL), with a[tutorial notebook⁠(opens in a new window)](https://colab.research.google.com/drive/1RMUeAWACpViqiUMlPMMwPTKyGU-OX756?usp=sharing)to get started. It is designed to require minimal technical background. We’ll keep improving GABRIEL over time based on feedback from the academic community. We hope this tool will help more researchers bring the richness of qualitative data and human stories into their work.
