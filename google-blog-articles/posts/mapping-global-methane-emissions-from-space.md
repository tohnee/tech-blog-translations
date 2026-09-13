---
title: "A new deep learning model maps global methane emissions from space."
source: https://blog.google/innovation-and-ai/models-and-research/google-research/mapping-global-methane-emissions-from-space/
site: google-blog
date: 2026-09-09
authors: Vishal Batchu
crawled: 2026-09-13
---

In a new study published in [PNAS](https://www.pnas.org/doi/10.1073/pnas.2612145123), Google and NASA’s Jet Propulsion Laboratory (JPL) introduced MAPL-EMIT, an AI model that tracks methane emissions globally from space using NASA’s [EMIT](https://www.jpl.nasa.gov/missions/emit-earth-surface-mineral-dust-source-investigation/) instrument.

Methane is a potent greenhouse gas. Over a 100-year timeframe, its warming potential is 30 times greater than that of carbon dioxide. MAPL-EMIT tackles a critical bottleneck in methane detection. Trained on 3.6 million physics-simulated methane plumes (clouds of methane gas released into the atmosphere), it cuts through complex, noisy terrain to detect 50% more plumes than human experts and identifies more than 23,000 additional plumes globally, including 24 out of 25 of the world’s largest-emitting landfills. By making methane sources easier to find at scale, MAPL-EMIT enables faster, more targeted climate mitigation.

Google has released the global plume database on [Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/projects_nature-trace_assets_ghg_emit_mapl_emit_plumes_v1_0) alongside an [Earth Engine app](https://nature-trace.projects.earthengine.app/view/mapl-emit) to visualize the data. Open-source models are available on [Kaggle](https://www.kaggle.com/models/vishalbatchu/emit-methane-plume-detection-and-quantification/) and inference tools are on [GitHub](https://github.com/google-research/mapl) to support researchers, policymakers, and operators. Read more on the [Google Research blog](https://research.google/blog/mapping-global-methane-emissions-from-space-with-deep-learning/).

![A six-panel satellite graphic showing detected methane plumes and emission heatmaps in California (USA), Turkmenistan, Delhi (India), Sao Paulo (Brazil), Katowice (Poland) and Shanxi (China).](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Map_Global_Methane_social.width-1200.format-webp.webp)
