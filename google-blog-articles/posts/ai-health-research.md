---
title: "Applying technology to understand and treat disease"
source: https://blog.google/innovation-and-ai/technology/health/ai-health-research/
site: google-blog
date: 2026-10-12
authors: Yossi Matias
crawled: 2026-10-15
---

Google’s health research and tools span from fundamental cellular discovery to laboratory analysis and patient impact. Over the last five years, Google teams have published 90 peer-reviewed research papers about understanding and addressing diseases, accumulating more than 90,000 citations. And building on our vision for how [technology can accelerate science to improve lives](https://blog.google/innovation-and-ai/technology/ai/ai-applications-science-people/), we’re collaborating with clinicians, academic institutes, and researchers to ensure discoveries make it out of the lab to benefit patients. Here is how our efforts are helping to advance medical research and public health solutions.

## Decoding the mechanics of disease

AlphaGenome Atlas is the most comprehensive catalog of predictions for how single-letter variant changes in the human genome affect molecular biology.

![The photo shows a close-up of a petri dish.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Genetic_Variants.width-1200.format-webp_PDssfpH.webp)

To effectively treat an illness, it helps to understand how it operates at the molecular, genetic, and cellular levels. Our early-stage biology models act as collaborative research tools for scientists, revealing nature's hidden mechanics and advancing medical discoveries.

- **Accelerating drug discovery:** Researchers at the Institute for Global Health, Barcelona, used [AlphaFold](https://deepmind.google/science/alphafold/) to virtually screen 30,000 compounds for antiparasitic activity against Chagas disease, a neglected tropical illness that affects roughly 8 million people and can lead to life-threatening complications if left untreated. This research helped the Institute identify two FDA-approved drugs that could be repurposed for Chagas, expediting time-to-treatment.
- **Mapping genetic variants linked to aging:** Identifying which rare genetic changes are linked to specific diseases is challenging because the volume of non-impactful mutations creates "background noise." Researchers at the University of Exeter used [AlphaGenome Atlas](https://deepmind.google/blog/alphagenome-atlas-a-predictive-map-of-every-possible-dna-letter-change-in-the-human-genome/) to search through genomic data from over 54,000 individuals, pinpointing specific variants that drive the abundance of critical proteins circulating in the human body, including PLA2G7 (linked to aging) and EGLN1 (a vital cellular oxygen sensor).
- **Reconstructing the brain at nanoscale:** In partnership with Harvard’s Lichtman Lab, we [reconstructed a human brain fragment](https://research.google/blog/ten-years-of-neuroscience-at-google-yields-maps-of-human-brain/) at nanoscale resolution and made the data openly available via [Neuroglancer](https://h01-release.storage.googleapis.com/explore.html). We additionally mapped the brains of model organisms including the [fly](https://www.cell.com/cell/fulltext/S0092-8674%2826%2900942-6), [larval zebrafish](https://www.biorxiv.org/content/10.1101/2025.06.10.658982v1), and [songbird](https://www.biorxiv.org/content/10.1101/2025.10.25.684569v1). These neural mapping resources enable researchers to advance their study of brain function.

## Accelerating tools for medical solutions

Visual map of proteins developed with the support of AlphaFold.

![A man looking at a computer screen displaying a 3D molecular structure with red and green atoms and bonds against a dark background.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Understanding_Disease_inline_2.width-1200.format-webp.webp)

The lab is where biological discovery is validated, engineered, and turned into potential medical and public health solutions. Our models have replaced slow, iterative processes with systems that can process large amounts of data quickly and accurately.

- **Supporting genetic diagnoses with ultrarapid genome sequencing:** In collaboration with Stanford University School of Medicine, we used [DeepVariant](https://www.nature.com/articles/nbt.4235) and [DeepConsensus](https://blog.google/innovation-and-ai/products/a-new-genome-sequencing-tool-powered-with-our-technology/) in a clinical trial to help determine the cause of genetic disease in time-critical cases. The program assisted in [enabling life-saving interventions](https://www.nejm.org/doi/full/10.1056/NEJMc2112090) by achieving genetic diagnosis with whole genome sequencing in less than eight hours, an unprecedented achievement also recognized with a [Guinness World Record](https://stanmed.stanford.edu/genome-sequencing-breaks-speed-record/).
- **Designing custom enzymes from scratch:** We introduced [AlphaProtein Novo](https://www.biorxiv.org/content/10.64898/2026.10.01.756017v1.full.pdf), a machine learning pipeline for creating new-to-nature enzymes from first principles. In lab tests, it successfully designed custom enzymes to synthesize key drug motifs, and others to degrade toxic environmental plastics under extreme conditions — demonstrating the ability to design functional proteins that can go beyond what is currently known in nature.
- **Supporting proactive public health initiatives:** A community's health is [deeply connected](https://blog.google/innovation-and-ai/technology/health/google-earth-ai-global-public-health/) to its geography. We are using our [Google Earth AI](https://ai.google/earth-ai/) models in combination with environmental, weather, mobility, and other data to [help public health leaders](https://blog.google/innovation-and-ai/technology/health/google-earth-ai/) forecast disease outbreaks and deliver care to vulnerable communities. In new research from [WHO AFRO](https://afro.who.int/) and the DRC’s [INRB](https://www.inrb.net/), conversational geospatial models replaced weeks of manual coding to help identify Ebola exposure and transmission risks sooner — allowing local responders to proactively deploy mobile laboratories.

## Supporting medical providers with machine learning models

New mammography screening systems can help to catch historically missed interval cancers and reduce specialist reading workloads.

![A healthcare professional with short dark hair and a light jacket looking at a mammogram scan displayed on a computer screen.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Understanding_Disease_inline_3.width-1200.format-webp.webp)

A medical breakthrough only matters if it can help real people. Our research demonstrates that machine learning models can help support disease detection as well as alleviate the administrative workload so providers can focus on care.

- **Flagging historically missed cancer signatures:** In a [pair](https://www.nature.com/articles/s43018-026-01128-z) of [studies](https://www.nature.com/articles/s43018-026-01127-0) published in *Nature Cancer* in collaboration with Imperial College London and the UK’s National Health Service (NHS), we evaluated a mammography screening system across 125,000 women. The system [caught](https://blog.google/innovation-and-ai/technology/health/google-ai-breast-cancer-detection/) 25% of historically missed interval cancers while showing the possibility of reducing specialist reading workloads by up to 40% — which could help provide crucial relief to healthcare systems facing severe radiologist shortages.
- **Uncovering hidden pediatric leukemia mutations:** When applied by Children’s Mercy Hospital to previously sequenced real-world childhood leukemia cases, [DeepSomatic](https://blog.google/innovation-and-ai/technology/research/deepsomatic-an-open-source-ai-model-is-speeding-up-genetic-analysis-for-cancer-research/) confirmed all known variants while detecting 10 previously missed mutations — despite the challenge of working with a tumor-only sample. DeepSomatic is publicly available and has the potential to inform clinical judgments around patient risk and targeted treatments.
- **Predicting global flu surges:** A Google [flu forecasting model](https://blog.google/innovation-and-ai/models-and-research/google-research/google-science-ai-flu-forecasts/) was ranked #1 by the Centers for Disease Control (CDC) for predicting flu-related hospital admissions during the 2025–2026 season. Developed using our [Empirical Research Assistance](https://research.google/blog/four-ways-google-research-scientists-have-been-using-empirical-research-assistance/) tool, the model outperformed 38 other systems to accurately match observed hospitalizations, showing how the technology can help public health officials anticipate demand for medical services and better prepare for seasonal outbreaks.

## Better health within reach for everyone

Transforming health requires scientists, researchers, and institutions working hand-in-hand. That’s why we equip the science community with the advanced models and open-access platforms to fuel breakthrough research — along with the philanthropic funding and computing power they need to apply that research.

Through Google.org, we’re supporting organizations like the [Infectious Disease Institute at Makerere University](https://blog.google/company-news/outreach-and-initiatives/google-org/announcing-ai-for-science-awardees/) to forecast malaria drug resistance mutations with AlphaFold and AlphaMissense, and the University of Pennsylvania, using AlphaProteo and AlphaFold to help design novel cellular therapies that can augment the treatment of solid tumors and complex diseases. In 2026, Google.org has provided over $60 million to organizations around the world that are applying advanced models to transform how we understand and treat diseases.

By meeting disease at every stage, we can turn the most intractable human health challenges into actionable solutions, helping people everywhere live longer, healthier lives.
