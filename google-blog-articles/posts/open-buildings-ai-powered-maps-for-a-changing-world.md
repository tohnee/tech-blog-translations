---
title: "Open Buildings: AI-powered maps for a changing world"
source: https://blog.google/innovation-and-ai/technology/research/open-buildings-ai-powered-maps-for-a-changing-world/
site: google-blog
date: 2024-09-19
authors: Olivia Graham
crawled: 2026-09-13
---

According to the UN, around 2.5 billion more people will be living in cities by 2050, with most of this increase coming from population growth and population movements in the [Global South](https://en.wikipedia.org/wiki/Global_North_and_Global_South#:~:text=According%20to%20UN%20Trade%20and,excluding%20Australia%20and%20New%20Zealand).). We need new tools to understand how our cities are growing and changing over time, so we can ensure that all of their inhabitants are accounted for in decision-making and the planning of essential services like running water and electricity.

Today we’re expanding our [Open Buildings project](https://sites.research.google/open-buildings/), which aims to help various organizations understand and plan for our changing world, with a new dataset that includes information about how building presence changes over time. The [Open Buildings 2.5D Temporal Dataset](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings-temporal_v1) is now available for the years 2016-2023, and also includes information about building heights for the first time.

## Why mapping buildings matters

Maps are a lifeline to many things we need. For people to receive essential services, like electricity and running water, and to be accounted for in crisis response, decision-makers need to first know where they are. By creating maps, we can help decision-makers understand the current environment and ensure that everyone is reached. That’s why Google Research introduced the Open Buildings project in 2021. This project, which started in our AI Research Lab in Accra, Ghana, has mapped 1.8 billion buildings across Africa, Asia, Latin America and the Caribbean, covering about 40% of the globe and about 54% of the world’s population.

Over the past few years, governments, humanitarian organizations, researchers and companies have used the Open Buildings dataset for a variety of projects. For example, [Sunbird AI](https://sunbird.ai/), a Ugandan nonprofit, used the Open Buildings dataset to prioritize areas for rural electrification projects to deliver the greatest impact in places with the most need. This kind of data can be useful for a variety of purposes, and we’ve also used it to improve the accuracy of Google Maps, adding buildings across the world to the map.

Over time, as partners used the data for their projects, important questions began to emerge: When were these buildings constructed? How has this city or settlement changed over time? What did this place look like before a recent crisis event and what does it look like now?

Getting answers to these questions can be difficult or sometimes impossible, for a variety of reasons. For example, in low- and middle-income countries where resources are often scarce, this kind of data may not exist. Conflict may be prevalent, preventing data from being recorded. Or the terrain itself may pose obstacles. But with the world’s population growing by over 80 million annually, access to this information is more important than ever, especially for government agencies, humanitarian organizations and researchers studying development trends and urbanization.

## How we produced this new dataset

To produce this dataset, we used AI to super-resolve and extract building footprints and heights from publicly available, lower-resolution imagery from the Sentinel-2 collection. This is important because lower-resolution satellite imagery is more available for the Global South than high-resolution imagery, so we needed to create models that could accurately classify buildings with these lower fidelity images.

We’re sharing our [technical report](https://arxiv.org/abs/2310.11622) as well as an [interactive Earth Engine App](https://mmeka-ee.projects.earthengine.app/view/open-buildings-temporal-dataset) so anyone can explore our methods and results in greater detail.

We’re also making the Open Buildings 2.5D Temporal Dataset freely available to support the work of policymakers, humanitarian organizations and others working in the Global South. It's hosted as an ImageCollection in the Earth Engine Data Catalog ([link](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings-temporal_v1)), where it can be analyzed with Earth Engine’s planetary-scale computation capabilities and vast catalog of other environmental datasets.

Ghana’s urban population has more than tripled in the past three decades. Kumasi, Ghana’s second largest city, has seen lots of growth over the past few years. Here, we see rapid growth in Pramso, a village on the outskirts of Kumasi.

On September 28, 2018, a 7.4 magnitude earthquake off the coast of Indonesia triggered a tsunami, affecting around 1.5 million people on the island of Sulawesi. After this crisis the built area recedes from the coastline and the effects of the earthquake are visible in the data.

These are just a few examples. The entire dataset can be explored in our [fully interactive Earth Engine app.](https://mmeka-ee.projects.earthengine.app/view/open-buildings-temporal-dataset)

## How we’ve collaborated to scale impact

We’re collaborating with partners who are using the data for a variety of impactful projects. For example, [WorldPop](https://www.worldpop.org/) is using Open Buildings to produce fresh and accurate population estimates across the world. WorldPop estimates are used by governments and UN agencies. WorldPop is also working with partners in Nigeria who have used the data to identify and reach children that have not received routine immunization services. “Understanding where people live is vital for making sure that resources are distributed fairly and that no one is left behind in delivering services like healthcare,” explains Professor Andrew Tatem, director of the WorldPop team. “Google's Open Buildings dataset has been a fantastic addition to the open data in our field that has supported more accurate population mapping, and the new temporal dataset unlocks opportunities to better capture the rapid demographic changes we continue to see globally.”

Sunbird AI, is using our dataset in the [Data Cities](https://www.datacities.ug/) project, a collaboration with UN Global Pulse, to create comprehensive profiles of two emerging cities in Uganda: Fort Portal and Jinja. The goal is to use geospatial data to support city authorities with the tools they need to make informed decisions on urban planning and policy and understand broader trends they will need to address.

## Limitations and areas we are focused on improving

Our AI innovations like satellite image segmentation, super resolution and elevation estimates have created a dynamic, global dataset that puts the whole world on the map. Nonetheless, there are still some limitations which may affect the data and prevent us from accurately mapping some buildings.

- **Clear skies are key:** We need a series of cloud-free images to get the best results. In some very cloudy areas, this can be a problem, leading to less reliable data. You might notice that some years have lower confidence scores.
- **Tiny buildings can be missed:** We can find buildings smaller than a single image pixel, but there's a limit. Very small structures, like informal shelters, might not show up.
- **Pixels not polygons:** Whereas the previous dataset included the geometrical shape of the buildings, this is quite difficult to produce from Sentinel-2 given the lower resolution of the input data. Instead, our data about building presence is provided in raster format, with a confidence score for each pixel.
- **Other quirks:** There are a few other technical issues that can affect the data, like image stitching errors and some false positives (detecting something that isn't there). We explain these in more detail on our [website](https://sites.research.google/gr/open-buildings/temporal/).

Maps are dynamic — because the world is always changing. With the Open Buildings 2.5D Temporal Dataset, AI helps us understand this change. We look forward to providing this information to our partners who support sustainable and inclusive urban development, and to help put everyone on the map.

We invite researchers, policymakers, and development practitioners from around the world to explore the Open Buildings 2.5D Temporal Dataset and share your feedback with us.
