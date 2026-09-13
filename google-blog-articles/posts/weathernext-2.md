---
title: "WeatherNext 2: Our most advanced weather forecasting model"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/weathernext-2/
site: google-blog
date: 2025-11-17
authors: The WeatherNext team
crawled: 2026-09-13
---

The weather affects important decisions we make everyday — from global supply chains and flight paths to your daily commute. In recent years, artificial intelligence (AI) has dramatically enhanced what’s possible in weather forecasting and the ways in which we can use it.

Today, Google DeepMind and Google Research are introducing [WeatherNext 2](https://deepmind.google/science/weathernext/), our most advanced and efficient forecasting model. WeatherNext 2 can generate forecasts 8x faster and with resolution up to 1-hour. This breakthrough is enabled by a new model that can provide hundreds of possible scenarios. Using this technology, we’ve supported weather agencies in making decisions based on a range of scenarios through our [experimental cyclone predictions](https://deepmind.google/blog/how-were-supporting-better-tropical-cyclone-prediction-with-ai/).

We're now taking our research out of the lab and putting it into the hands of users. WeatherNext 2's forecast data is now available in [Earth Engine](https://developers.google.com/earth-engine/datasets/catalog/projects_gcp-public-data-weathernext_assets_weathernext_2_0_0) and [BigQuery](https://console.cloud.google.com/bigquery/analytics-hub/exchanges/projects/871883017250/locations/us/dataExchanges/weathernext_19397e1bcb7/listings/weathernext_2_19a39fe59dd). We’re also launching an [early access program](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/weather-next-v2) on Google Cloud’s Vertex AI platform for custom model inference.

By incorporating WeatherNext technology, we’ve now upgraded weather forecasts in Search, Gemini, Pixel Weather and Google Maps Platform’s [Weather API](https://mapsplatform.google.com/maps-products/weather/). In the coming weeks, it will also help power weather information in Google Maps.

## Predicting more possible scenarios

From a single input, we use independently trained neural networks and inject noise in function space to create coherent variability in weather forecast predictions.

![Diagram showing the new algorithm used in WeatherNext 2.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/WeatherNext_2-blog-figure-03_lar.width-1200.format-webp.webp)

Weather predictions need to capture the full range of possibilities — including worst case scenarios, which are the most important to plan for.

WeatherNext 2 can predict hundreds of possible weather outcomes from a single starting point. Each prediction takes less than a minute on a single TPU; it would take hours on a supercomputer using physics-based models.

Our model is also highly skillful and capable of higher-resolution predictions, down to the hour. Overall, WeatherNext 2 surpasses our previous state-of-the-art WeatherNext model on 99.9% of variables (e.g. temperature, wind, humidity) and lead times (0-15 days), enabling more useful and accurate forecasts.

This improved performance is enabled by a new AI modelling approach called a [Functional Generative Network](https://arxiv.org/abs/2506.10772) (FGN), which injects ‘noise’ directly into the model architecture so the forecasts it generates remain physically realistic and interconnected.

This approach is particularly useful for predicting what meteorologists refer to as “marginals” and “joints.” Marginals are individual, standalone weather elements: the precise temperature at a specific location, the wind speed at a certain altitude or the humidity. What's novel about our approach is that the model is only trained on these marginals. Yet, from that training, it learns to skillfully forecast 'joints' — large, complex, interconnected systems that depend on how all those individual pieces fit together. This 'joint' forecasting is required for our most useful predictions, such as identifying entire regions affected by high heat, or expected power output across a wind farm.

Continuous Ranked Probability Score (CRPS) comparing WeatherNext 2 to WeatherNext Gen

![Heatmaps showing WeatherNext 2 consistently outperforms WeatherNext Gen across nearly all atmospheric variables, pressure levels, and lead times.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/WeatherNext2vs_graphic.width-1200.format-webp.webp)

## From research to reality

With WeatherNext 2, we're translating cutting edge research into high-impact applications. We’re committed to advancing the state of the art of this technology and making our latest tools available to the global community.

Looking ahead, we’re actively researching capabilities to improve our models, including integrating new data sources, and expanding access even further. By providing powerful tools and open data, we hope to accelerate scientific discovery and empower a global ecosystem of researchers, developers and businesses to make decisions on today’s most complex problems and build for the future.

To learn more about geospatial platforms and AI work at Google, check out [Google Earth](http://earth.google.com/), [Earth Engine](https://earthengine.google.com/), [AlphaEarth Foundations](https://deepmind.google/blog/alphaearth-foundations-helps-map-our-planet-in-unprecedented-detail/), and [Earth AI](https://ai.google/earth-ai/).

## Learn more about WeatherNext 2

- [Read our paper](https://arxiv.org/abs/2506.10772)
- [WeatherNext developer documentation](https://developers.google.com/weathernext)
- Explore the [Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets/catalog/projects_gcp-public-data-weathernext_assets_weathernext_2_0_0)
- Query forecast data in [BigQuery](https://console.cloud.google.com/bigquery/analytics-hub/exchanges/projects/871883017250/locations/us/dataExchanges/weathernext_19397e1bcb7/listings/weathernext_2_19a39fe59dd)
- Sign up to the [early access program](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/weather-next-v2) for Cloud Vertex AI
