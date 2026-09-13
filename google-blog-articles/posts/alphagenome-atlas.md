---
title: "AlphaGenome Atlas: a high-resolution map of human DNA"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/alphagenome-atlas/
site: google-blog
date: 2026-09-08
authors: Pushmeet Kohli
crawled: 2026-09-13
---

The human genome is made of about 3 billion base pairs of DNA — but much of it remains a mystery. Scientists understand the 2% of the human genome that codes for proteins relatively well, but have only limited knowledge of the remaining 98%. Our AlphaGenome model has already shown how single changes in these non-coding DNA regions can disrupt molecular processes like protein production, but the bigger picture remained unclear.

Today, we're introducing [AlphaGenome Atlas](http://alphagenome.google/atlas), a database that predicts the effects of every possible single nucleotide variant in the human genome. We used the AlphaGenome AI model to pre-calculate the regulatory impact of all 9 billion single-letter genetic changes, resulting in a massive, 1-petabyte dataset. Our new Atlas helps scientists rapidly query this vast information.

To help researchers rapidly navigate this, the Atlas introduces the AlphaGenome Variant Impact (AVI) score. This single, easy-to-use score combines predictions for both coding and non-coding regions, allowing researchers to quickly prioritize the most promising avenues for research without sifting through thousands of data points.

## Empowering researchers to solve biological mysteries

AlphaGenome Atlas is already acting as a powerful augmentation partner for the scientific community, accelerating research in areas like:

- **Rare genomic variations:** At the Broad Institute, Laura Covill and her team used the AVI score to prioritize variants for unsolved rare disease research. The tool highlighted a critical variant in the DNM1 gene, predicting that it created an incorrect splice site. This provided crucial supporting evidence to successfully solve the case.
- **Complex traits:** Identifying rare, non-coding variants linked to complex traits is difficult due to statistical noise. Dr. Gareth Hawkes applied AlphaGenome Atlas to data from 54,000+ UK Biobank participants. By grouping variants based on predicted molecular effects, he uncovered 22% more non-coding genetic associations. Focusing on the top 1% of impactful variants, he identified 19 genetic regions linked to body mass index (BMI), directing the next stage of targeted research.

## Opening access to researchers and biologists worldwide

AlphaGenome Atlas is available today through an [intuitive website portal](http://alphagenome.google/atlas) that requires zero coding skills, democratizing access for clinical researchers and biologists worldwide. This is part of our ongoing commitment to accelerate genomic discovery and science, for everyone.

AlphaGenome Atlas provides grounded genomic insights that will accelerate the pace of biological discovery.

Read more on the [Google DeepMind blog](https://deepmind.google/blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/).
