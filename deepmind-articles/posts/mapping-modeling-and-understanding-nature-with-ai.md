---
title: "Mapping, modeling, and understanding nature with AI"
source: https://deepmind.google/blog/mapping-modeling-and-understanding-nature-with-ai/
site: deepmind
date: 2025-11-05
authors: Ecosystem Modeling team
crawled: 2026-09-13
---

AI models can help map species, protect forests and listen to birds around the world

The planet’s biosphere is the sum of its plants, animals, fungi, and other organisms. Every day, we depend on it for our survival – the air we breathe, the water we drink, and the food we eat are all produced by Earth’s ecosystems.

As increasing demand for land and resources puts pressure on these ecosystems and their species, [artificial intelligence (AI) can be a transformative tool](https://blog.google/outreach-initiatives/sustainability/how-were-using-ai-to-help-nature-and-people-flourish-together/) to help protect them. It can make it easier for governments, companies and conservation groups to collect field data, integrate that data into new insights, and translate those insights into action. And it can inform better plans and monitor the success of those plans when put into practice.

Today we're announcing new biosphere research predicting the risk of deforestation, a new project to map the ranges of Earth’s species, and the latest updates on our bioacoustics model Perch.

## Predicting deforestation

Forests stand as one of the biosphere’s most critical pillars — storing carbon, regulating rainfall, mitigating floods, and harboring the majority of the planet’s terrestrial biodiversity. Unfortunately, despite their importance, forests continue to be lost at an alarming rate.

For more than 20 years it has been possible to track deforestation from space, using satellite-based remote sensing. Together with the [World Resources Institute](https://www.wri.org/), we recently went one level deeper, developing a model of the [drivers of forest loss](https://www.wri.org/insights/forest-loss-drivers-data-trends) — from agriculture and logging to mining and fire — at an unprecedented 1km2 resolution, for the years 2000-2024.

Today, we’re releasing a benchmark dataset for [predicting deforestation](https://research.google/blog/forecasting-the-future-of-forests-with-ai-from-counting-losses-to-predicting-risk/) risk. This model uses pure satellite inputs, avoiding the need for specific local input layers such as roads, and an efficient model architecture, built around vision transformers. This approach enables accurate, high-resolution predictions of deforestation risk, down to a scale of 30 meters, and over large regions.

![A map showing deforestation risk for a region in Southeast Asia in 2023, with green showing areas already deforested, and red indicating higher risk for deforestation.](https://lh3.googleusercontent.com/WAK2GGYAiNbQhdJ_HNmg4z9TNUhhbH-OL33rkDvgCr-TNwpTbqaHaYXVFrO4elmMvGD69EAQVOyOIT9FgngfA7MN6FWzQjuD_1vmNV5uW1UjO_qXJA=w1440-h810-n-nu)

A map showing deforestation risk for a region in Southeast Asia in 2023, with green showing areas already deforested, and red indicating higher risk for deforestation. Underlying map data ©2025 Imagery ©2025 Airbus, CNES / Airbus, Landsat / Copernicus, Maxar Technologies

## Modeling the distribution of Earth’s species

To conserve the planet’s threatened species, we have to know where they are. With more than 2 million known species, and millions more to be discovered and named, that’s a monumental task.

To help tackle this problem, Google researchers are developing a [new AI-powered approach](https://ar5iv.labs.arxiv.org/html/2503.11900) for producing species range maps at unprecedented scale – with more species, over more of the world, and at higher resolution than ever before. The Graph Neural Net (GNN) model combines open databases of field observations of species, with [satellite embeddings](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_SATELLITE_EMBEDDING_V1_ANNUAL) from [AlphaEarth Foundations](https://deepmind.google/discover/blog/alphaearth-foundations-helps-map-our-planet-in-unprecedented-detail/), and with species trait information (such as body mass). This approach allows us to infer a likely underlying geographical distribution for many species at once, and for scientists to refine those inferred distributions with additional local data and expertise.

As part of a pilot with researchers at [QCIF](https://www.qcif.edu.au/) and [EcoCommons](https://www.ecocommons.org.au/), we’ve used our model to map Australian mammals like the Greater Glider: a nocturnal, fluffy-tailed marsupial that lives in old-growth eucalyptus forests. We are also releasing 23 of these species maps via the [UN Biodiversity Lab](https://map.unbiodiversitylab.org/earth?basemap=grayscale&coordinates=-25.448847,132.236151,3&layers=UNBL.layer.australian-mammal-species-distributions_100) and [Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_species_distribution_models_australia_mammals_v0) today.

Using artificial intelligence, Google is shedding new light on where species live, helping scientists and decisionmakers better protect the Earth’s wildlife.

## Listening through bioacoustics

All efforts to understand and model ecosystems ultimately depend on monitoring in the field. AI can play a critical role here as well, augmenting traditional ecological field monitoring — which is notoriously difficult and costly — with automated identification of habitats and species from monitoring devices.

A compelling example is bioacoustics. Birds, amphibians, insects and other species use sound to communicate, making it an excellent modality for identifying resident species and understanding the health of an ecosystem. Reliable and affordable bioacoustic monitors are readily available. However, these devices produce vast audio datasets, full of unknown and overlapping sounds, which are too large to be reviewed manually, but also difficult to analyse automatically.

To help scientists and conservationists untangle this complexity, we recently released [Perch 2.0](https://www.kaggle.com/models/google/bird-vocalization-classifier/tensorFlow2/perch_v2) - an update to our animal vocalization classifier. This new model is not only state of the art for bird identification, but is also available as a foundational model, allowing for field ecologists to quickly adapt the model to identify new species and habitats, anywhere on Earth.

We are especially proud of our work with the University of Hawai`i, where Perch is guiding protective measures for endangered honeycreepers, and also being used to identify juvenile calls to understand population health.

Google's Perch model helps scientists leverage AI to identify sounds in nature - like endangered Hawaiian birds - enabling timely conservation action.

## The future of AI for Nature

The goal of this work is to make it easier for decisionmakers at all levels to take action to protect the planet. But better data only leads to better decisions if that data is thorough; if it really captures what’s happening in a given ecosystem at all levels.

That’s why we’re working to integrate these and other models together, combining data from more modalities like satellite data, images, bioacoustics, documents, and more. And, to join all this up alongside models of human activity like land-use changes and agricultural practices as well as models of agricultural yields, flood prevention, and other human-relevant consequences.

By giving policymakers a comprehensive understanding of threats to the biosphere, we can help them take action to protect future generations of plants, animals, and people. If we can model the environment, perhaps we can help it thrive.

Learn more about our AI and sustainability efforts by checking out

[Google Earth AI](https://blog.google/technology/research/new-updates-and-more-access-to-google-earth-ai/)[Google Earth Engine](https://cloud.google.com/blog/topics/sustainability/look-back-at-a-year-of-earth-engine-advancements)[AlphaEarth Foundations](https://deepmind.google/blog/alphaearth-foundations-helps-map-our-planet-in-unprecedented-detail/)

## Acknowledgements

This research was co-developed by Google DeepMind and Google Research.

Google DeepMind: Andrea Burns, Anton Raichuk, Arianna Manzini, Bart van Merrienboer, Burcu Karagol Ayan, Dominic Masters, Drew Purves, Jenny Hamer, Julia Haas, Keith Anderson, Matt Overlan, Maxim Neumann, Melanie Rey, Mustafa Chasmai, Petar Veličković, Ravi Rajakumar, Tom Denton, Vincent Dumoulin

Google Research and Google Partners: Ben Williams, Charlotte Stanton, Dan Morris, Elise Kleeman, Lauren Harrell, Michelangelo Conserva

We’d also like to thank our partners at UNEP-WCMC and QCIF, additional collaborators Aditee Kumthekar, Aparna Warrier, Artlind Kortoci, Burooj Ghani, Christine Kaeser-Chen, Grace Young, Kira Prabhu, Jamie McPike, Jane Labanowski, Jerome Massot, Kuan Lu, Mélisande Teng, Michal Kazmierski, Millie Chapman, Rishabh Baghel, Scott Riddle, Shelagh McLellan, Simon Guiroy, Stefan Kahl, Tim Coleman and Youngin Shin, as well as Peter Battaglia and Kat Chou for their support.
