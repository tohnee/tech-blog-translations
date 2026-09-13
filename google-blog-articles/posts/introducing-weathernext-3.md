---
title: "Introducing WeatherNext 3, our most advanced and accurate global weather AI model"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/introducing-weathernext-3/
site: google-blog
date: 2026-09-03
authors: The WeatherNext team
crawled: 2026-09-13
---

Every day, the weather influences billions of decisions. Some are as simple as grabbing an umbrella before heading out the door, but others are far more consequential. Wind, rain, and extreme weather events, like heatwaves and droughts, have cascading impacts across agriculture, global supply chains, clean energy production, and national economies.

In recent years, AI has revolutionized weather forecasting, using historical records to make faster and more accurate predictions than traditional methods. Yet predicting highly local and rapidly changing weather has remained a challenge. Previous models often lacked sufficient spatial resolution, and struggled to incorporate real-time weather data from sources like satellites.

Today, Google DeepMind and Google Research are introducing [WeatherNext 3](https://arxiv.org/abs/2609.03582), the most advanced and accurate global weather model to date, according to independent [live evaluations](https://owb.brightband.com/) by Brightband. Our model learns directly from real-time observations, enabling it to provide timely and more localized predictions for the weather events that impact people the most. By using raw satellite data to produce a forecast every hour in high resolution, our model makes reliable forecasts accessible across Google products worldwide.

## Rapid weather prediction at unprecedented resolution

A forecast's utility often comes down to detail and how finely it resolves both time and space. WeatherNext 3 generates hourly forecasts at multiple spatial resolutions, maintaining physical consistency from broad global wind patterns all the way down to local topography.

With WeatherNext 3, we can visualize key surface variables — like temperature and moisture — at a 5-kilometer resolution, other surface variables at 10 kilometers, and atmospheric variables, like wind speed, at 25 kilometers. Overall, this provides a global weather picture roughly five times sharper than our previous model, WeatherNext 2, which produced forecasts on a 25-kilometer grid in 6-hour increments.

Figure 1: The end-to-end WeatherNext 3 system architecture. The model ingests live 1-hour geostationary satellite mosaics alongside traditional historical analysis to feed a single, flexible Functional Generative Network (FGN) mesh transformer. It outputs dense gridded fields, discrete cyclone tracks, and predicts station-level sparse coordinates natively.

![Diagram of the WeatherNext 3 System architecture](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/WeatherNext3_diagrams_fig-01.width-1200.format-webp.webp)

Figure 2: Comparison of 2-meter temperature forecasts over the UK. WeatherNext 2 (left) at 25-kilometer (0.25°) resolution vs. WeatherNext 3 (right) at a native 5-kilometer (0.05°) resolution. WeatherNext 3 resolves the intricate local topography, preventing the pixelated, over-smoothed thermal representations seen in older models.

## Real-world data at continuous global scale

WeatherNext 3's biggest leap forward is what it learns from. Most AI weather models, including WeatherNext 2, are trained on data from numerical weather prediction (NWP) models. Although useful, NWP models are complex, supercomputer-driven physics simulations that carry a six-hour data lag. This lag can lead to biases for fast-changing variables like rain or surface temperature.

By ingesting a mosaic of live, global geostationary satellite data, our new model gains a rich, continuously updating view of the atmosphere. This allows the model to generate a new forecast every hour, each one grounded in the most recent satellite observations available, at up to 5-kilometer resolution.

This is important because critical weather develops fast. When storms, fronts, or precipitation systems materialize suddenly, our rapid update cycle and higher resolution provides earlier, more detailed insights needed to help drive an effective response.

Some variables, like temperature and humidity, can fluctuate dramatically over just a few kilometers, which is particularly relevant for communities near coastlines, valleys, or mountain ranges. Traditional models struggle here because they train on representations of the atmosphere that lack detail and miss extreme local variations.

To address this, WeatherNext 3 instead trains directly on sparse weather station observation data. This allows us to make global forecasts on a 5-kilometer grid that account for regional details like topography.

This breakthrough is particularly vital for regions across Latin America, Africa, and Asia-Pacific that have historically been underserved by high-resolution forecasting due to the immense supercomputing costs of traditional regional models. It brings localized, high-fidelity forecasting to billions of people and local businesses in these areas.

Beyond improved resolution and forecast frequency, our model introduces predictions specifically engineered for renewable energy production. The model forecasts 100-meter wind speeds (roughly at turbine-height) for precise wind-energy output, alongside high-resolution cloud cover and sun radiation levels to help solar farms estimate how much light they will receive on the ground.

This data is crucial for global clean energy planning, allowing grid operators and renewables developers to accurately predict how much power their clean energy assets will generate and match it with consumer demand.

## Precipitation forecasting at breakthrough accuracy

Global weather models notoriously struggle to accurately predict precipitation. Rain and snow systems are driven by fast-moving cloud processes on tiny scales that are hard to model accurately using traditional physics-based simulations. Consequently, AI forecasts often produce blurry estimates or miss the boundaries of severe storms entirely.

To solve this, we train our model on two exceptionally high-quality sources of precipitation data: NASA’s satellite-based Integrated Multi-satellite Retrievals for GPM (IMERG) and our own global precipitation reanalysis based on satellite radar.

The result is a significant leap in precipitation forecasting accuracy. In medium-range global forecasts, evaluations against baselines show a Continuous Ranked Probability Score (CRPS) improvement of up to 60% against IMERG, 30% for MRMS, and 10% against rain gauge measurements for early lead times.

Figure 3: Medium-range probability of precipitation (PoP > 1mm) forecast comparison. WeatherNext 2 (left) at 25-kilometer resolution shows a highly diffused and pixelated precipitation footprint. WeatherNext 3 (middle) at 11-kilometer resolution closely mirrors the actual satellite ground truth (right), accurately capturing the sharp, convective bands of the weather systems.

![Comparison of prediction for WN2 and WN3](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/WeatherNext3_diagrams_fig-03.width-1200.format-webp.webp)

## Research applied across the ecosystem

Our primary goal is to advance weather intelligence to make it universally useful — whether for an emergency responder tracking sudden wind shifts, an air traffic controller planning flight paths, or a farmer managing crops.

To bring these breakthroughs out of the lab and into the real world, we’re integrating WeatherNext 3 across Google’s core ecosystem and beyond:

- **High-resolution forecast data:** We’re making global weather predictions, updated hourly and ready to integrate into your workflows with no model setup required. This enables researchers, developers and businesses to [query the data](https://developers.google.com/weathernext) in BigQuery and Earth Engine, or bulk-download from Google Cloud Storage.
- **Available globally**: WeatherNext 3 will begin powering weather experiences within Google Search, Gemini app, Google Maps, Google Maps Platform Weather API, and Google Earth Engine starting today. The update dramatically improves longer term forecasts. When planning a day or more ahead, people will see up to 50% more accurate precipitation forecasts — with the greatest improvements in regions where forecasts have historically been less reliable. So if you’re packing for a weekend trip or deciding the best day for an outdoor activity, you’ll now get more accurate predictions to help you plan.

The atmosphere will always retain a degree of unpredictability. However, by training on real-world observations and bypassing traditional modeling constraints, WeatherNext 3 brings us closer to a future where forecasts truly match what is happening on the ground.

To learn more about geospatial platforms and AI work at Google, check out [Google Earth Engine](https://earthengine.google.com/), [AlphaEarth Foundations](https://deepmind.google/blog/alphaearth-foundations-helps-map-our-planet-in-unprecedented-detail/), and [Earth AI](https://ai.google/earth-ai/).

**Disclaimer: For official weather forecasts, severe weather warnings, and public safety advisories, please refer to your local meteorological agency or national weather service.**

## Learn more about WeatherNext 3

- [Read our paper](https://arxiv.org/abs/2609.03582)
- [Build with WeatherNext 3](https://developers.google.com/weathernext)
- Explore [Weather Lab](https://deepmind.google.com/science/weatherlab) to see WeatherNext 3 visualized in real-time
- See where WeatherNext 3 ranks on independent [live leaderboards](http://owb.brightband.com/) from Brightband.
