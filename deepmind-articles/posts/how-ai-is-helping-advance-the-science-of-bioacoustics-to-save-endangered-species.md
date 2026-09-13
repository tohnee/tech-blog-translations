---
title: "How AI is helping advance the science of bioacoustics to save endangered species"
source: https://deepmind.google/blog/how-ai-is-helping-advance-the-science-of-bioacoustics-to-save-endangered-species/
site: deepmind
date: 2025-08-07
authors: Perch team
crawled: 2026-09-13
---

Our new Perch model helps conservationists analyze audio faster to protect endangered species, from Hawaiian honeycreepers to coral reefs.

One of the ways scientists protect the health of our planet’s wild ecosystems is by using microphones (or underwater hydrophones) to collect vast amounts of audio dense with vocalizations from birds, frogs, insects, whales, fish and more. These recordings can tell us a lot about the animals present in a given area, along with other clues about the health of that ecosystem. Making sense of so much data, however, remains a massive undertaking.

Today, we are releasing an update to [Perch](http://arxiv.org/abs/2508.04665), our AI model designed to help conservationists analyze bioacoustic data. This new model has better state-of-the-art off-the-shelf bird species predictions than the previous model. It can better adapt to new environments, particularly underwater ones like coral reefs. It’s trained on a wider range of animals, including mammals, amphibians and anthropogenic noise — nearly twice as much data in all, from public sources like [Xeno-Canto](https://xeno-canto.org/) and [iNaturalist](https://neurips.cc/virtual/2024/poster/97701). It can disentangle complex acoustic scenes over thousands or even millions of hours of audio data. And it’s versatile, able to help answer many different kinds of questions, from “how many babies are being born” to “how many individual animals are present in a given area.”

In order to help scientists protect our planet’s ecosystems, we’re releasing this new version of Perch as an open model and making it available on [Kaggle](https://www.kaggle.com/models/google/bird-vocalization-classifier/tensorFlow2/perch_v2).

![A 10-panel photo collage featuring diverse ecosystems and species monitored by bioacoustics, including a red-eyed tree frog, a humpback whale, a gibbon, a colorful coral reef, a group of meerkats, a spotted seal, a hanging bat, a mosquito, a walrus, and an aerial view of a coral reef.](https://lh3.googleusercontent.com/kJ2OlrhiAEdXxydXx9yt4fNNCDp1jsPTaUv321UUB0D-tqcAjZabF_Zxkki1faXfUD1tRKS5fkEVgfWIITLPk7qX-T8AJoew7A9WHsqpL7y_Y83kQA=w1440)

Perch not only recognizes the sound of bird species. Our new model was trained on a wider range of animals including mammals, amphibians and anthropogenic noise.

## Success Stories: Perch in the Field

Since it was first launched in 2023, the initial version of Perch has already been [downloaded over 250,000 times](https://www.kaggle.com/models/google/bird-vocalization-classifier) and its openly available solutions are now well-integrated into tools for working biologists. For example, Perch’s vector search library is now part of Cornell's widely-used [BirdNet Analyzer](https://github.com/birdnet-team/BirdNET-Analyzer).

In addition, Perch is helping BirdLife Australia and the Australian Acoustic Observatory build classifiers for a number of unique Australian species. For example, our tools enabled the [discovery](https://www.theguardian.com/environment/2025/feb/12/plains-wanderers-spotted-in-melbournes-west-for-first-time-in-30-years-with-help-of-ai) of a new population of the elusive Plains Wanderer.

> This is an incredible discovery – acoustic monitoring like this will help shape the future of many endangered bird species.

Paul Roe

Dean Research, James Cook University, Australia

Recent work has also found that the earlier version of Perch can be used to [identify individual birds](https://www.sciencedirect.com/science/article/pii/S1574954125003395) and [track bird abundance](https://www.sciencedirect.com/science/article/pii/S1470160X24013876), potentially reducing the need for catch-and-release studies to monitor populations.

Finally, biologists from the [LOHE Bioacoustics Lab](https://lohelab.org/) at the University of Hawaiʻi have used it to monitor and protect populations of honeycreepers, which are important to [Hawaiian mythology](https://www.mauiforestbirds.org/cultural-significance) and face extinction from the threat of avian malaria spread by non-native mosquitoes. Perch helped the LOHE Lab find honeycreeper sounds nearly 50x faster than their usual methods, enabling them to monitor more species of honeycreeper over greater areas. We expect the new model will further accelerate these efforts.

![](https://lh3.googleusercontent.com/ItTZW3LgJsjeCWxuC3GSzzAfqs0jXrDkaeEWrgQt7efPUBlVRd495QZmHHOW_1zhDqzkT6O0hnE7aDt9nvOT18_zWCy2lHym6w84PlLv_WWK3bYZLLA=w1440-h810-n-nu)

## Untangling the Planet's Playlist

The Perch model can predict which species are present in a recording, but that's only part of the story: We also provide [tools](https://github.com/google-research/perch-hoplite) that allow scientists to quickly build new classifiers starting from a single example and monitor species for which there is scarce training data or for very specific sounds like juvenile calls. Given one example of a sound, vector search with Perch surfaces the most similar sounds in a dataset. A local expert can then mark the search results as relevant or irrelevant to train a classifier.

Together, this combination of vector search and active learning with a strong embedding model is called [agile modeling](https://openaccess.thecvf.com/content/ICCV2023/papers/Stretcu_Agile_Modeling_From_Concept_to_Classifier_in_Minutes_ICCV_2023_paper.pdf)***.*** Our recent paper–["The Search for Squawk: Agile Modeling in Bioacoustics"](https://arxiv.org/abs/2505.03071)–shows that this method works across birds and coral reefs, allowing the creation of high quality classifiers in under an hour.

## Looking ahead: the future of bioacoustics

Together, our models and methods are helping maximize the impact of conservation efforts, leaving more time and resources for meaningful, on-the-ground work. From the forests of Hawaiʻi to the reefs of the ocean, the Perch project showcases the profound impact we can have when we apply our technical expertise to the world's most pressing challenges. Every classifier built and every hour of data analyzed brings us closer to a world where the soundtrack of our planet is one of rich, thriving biodiversity.

**Learn more**

[Download the new Perch model from Kaggle Models](https://www.kaggle.com/models/google/bird-vocalization-classifier/tensorFlow2/perch_v2)[Read our paper on arxiv](http://arxiv.org/abs/2508.04665)[Read our paper on agile modeling for bioacoustics](https://arxiv.org/abs/2505.03071)[Explore our GitHub repository](https://github.com/google-research/perch-hoplite)

**Acknowledgements**

This research was developed by the Perch team: Bart van Merriënboer, Jenny Hamer, Vincent Dumoulin, Lauren Harrell, and Tom Denton, and Otilia Stretcu from Google Research. We also thank our collaborators Amanda Navine and Pat Hart at the University of Hawaiʻi, and Holger Klinck, Stefan Kahl and the BirdNet team at the Cornell Lab of Ornithology. And all our friends and collaborators whom we would have written about in this blog post if only we had another thousand words.
