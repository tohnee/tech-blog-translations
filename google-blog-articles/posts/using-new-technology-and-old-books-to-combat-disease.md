---
title: "Using new technology and old books to combat disease"
source: https://blog.google/innovation-and-ai/technology/research/using-new-technology-and-old-books-to-combat-disease/
site: google-blog
date: 2022-12-12
authors: Nikki Savickas
crawled: 2026-09-13
---

Hundreds of millions of people are affected by insect-borne diseases every year, and climate change is only making the problem worse. Increases in temperature and rainfall have expanded the range of insects, including ticks and mosquitos, contributing to outbreaks of diseases such as dengue fever, lyme disease and malaria.

Where can humanity find answers to the newest challenges? One idea: old books.

A team at Google Brain is using decades-old datasets mined by Google Books — along with a newly developed sensory map for odor — to combat this major global health issue. This is possible because the team recently discovered that a mosquito’s sense of smell is not so different from ours.

Former Google Brain researcher, and now Entrepreneur in Residence at Google Ventures, Alex Wiltschko, explains, “My team is focused on giving computers a sense of smell. As we reviewed predictions of the neural networks we trained to predict what molecules smell like to people, we found that they were also useful to predict how the 'smell parts' of the brains of insects respond to the same molecules.”

Insects like mosquitoes use smell to locate food — sugary nectar from plants, and in the case of egg-producing females of many species, a protein found in blood. Chemical repellents work to confuse the olfactory signals of these insects, distracting them from biting a possible victim and preventing the spread of disease-causing pathogens. The Google Brain team realized that if they could train computers to recognize the odors that repel mosquitoes, those computers could help predict safe, cheap and effective repellents to stop insect-borne disease in its tracks.

Of course, in order to train their models, they needed data.

The team identified relevant research completed by the United States Department of Agriculture during World War II. “We learned about a dataset where they tested thousands of repellents – much more than the 20 we had,” Alex says. But the USDA data was recorded in notebooks and file cabinets, some of it unindexed, and all of it too difficult to find and share with the Google Brain team. Fortunately, the USDA research had been scanned and indexed by another team at Google – Google Books. The USDA was able to provide search terms which helped the Google Brain team locate the missing dataset among the over 40 million volumes in the Google Books corpus.

A massive-but-forgotten insect repellent dataset discovered in Google Books that describes the first test of DEET in the late 1940s.

![A page from a study in the 1940s](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/oldbook.width-1200.format-webp.webp)

It was a good start. But when Google Books Technical Collections Specialist Kurt Groetsch heard about that first dataset, he knew he could find even more. A comprehensive search turned up over 100 datasets of varying sizes — datasets that had been long forgotten by the USDA, and everyone else. “Scientists did rigorous tests for these research projects. It’s really well-recorded scientific information, and it sits there in print for decades — its existence getting lost in time,” says Google Books Senior Library Partnerships Manager Ben Bunnell. “Now we can take tools that didn’t exist in the ‘40s and use their research to extrapolate information that can potentially save lives today.”

Exposing an arm treated with repellent in a cage of Aedes aegypti.

![A man with his arm in an enclosed box full of bugs.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/oldimage.width-1200.format-webp.webp)

With support from the Bill and Melinda Gates Foundation and armed with all of the data they could ask for, the Google Brain team tapped TropIQ, an organization that tests molecules to combat insect-borne infectious diseases, to find out if they could use it. “What we wanted to see was that good repellents in 1942 are still good repellents now — and that’s exactly what we found,” Alex says.

With confirmation of the quality of the USDA data, the [team was able to train a neural network](https://www.biorxiv.org/content/10.1101/2022.09.01.504601v2) to predict which molecules were effective as insect repellents. They crossed the molecules currently in use as chemical repellents off the list, then had TropIQ test the remainder: the molecules that had been identified as effective but were not currently in use. Of those, TropIQ’s test revealed 10 molecules that showed a higher level of repellency than DEET. The Google Brain team is currently investigating those molecules for cost, safety and availability, paving the way for a new batch of insect repellents to help combat diseases.

Additionally, the collaboration between Google Brain and Google Books has uncovered an enormous source of unexamined datasets for further study. “This project has opened up opportunities to extract more data of this nature for machine learning analysis — not just chemical, but environmental, astronomical, geological...the list goes on,” Ben says. “There’s so much information in Google Books just waiting to be found, and so many more books yet to be scanned – this project is just the first page of a very long story.” The team’s hope is that, by using Google Books to discover what lies beneath, we could unlock answers to some of the challenges facing people every day.
