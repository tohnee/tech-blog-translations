---
title: "GenCast predicts weather and the risks of extreme conditions with state-of-the-art accuracy"
source: https://deepmind.google/blog/gencast-predicts-weather-and-the-risks-of-extreme-conditions-with-sota-accuracy/
site: deepmind
date: 2024-12-04
authors: Ilan Price, Matthew Willson
crawled: 2026-09-13
---

New AI model advances the prediction of weather uncertainties and risks, delivering faster, more accurate forecasts up to 15 days ahead

Weather impacts all of us — shaping our decisions, our safety, and our way of life. As climate change drives more extreme weather events, accurate and trustworthy forecasts are more essential than ever. Yet, weather cannot be predicted perfectly, and forecasts are especially uncertain beyond a few days.

Because a perfect weather forecast is not possible, scientists and weather agencies use probabilistic ensemble forecasts, where the model predicts a range of likely weather scenarios. Such ensemble forecasts are more useful than relying on a single forecast, as they provide decision makers with a fuller picture of possible weather conditions in the coming days and weeks and how likely each scenario is.

Today, in a paper [published in Nature](https://www.nature.com/articles/s41586-024-08252-9), we present GenCast, our new high resolution (0.25°) AI ensemble model. GenCast provides better forecasts of both day-to-day weather and extreme events than the top operational system, the European Centre for Medium-Range Weather Forecasts’ ([ECMWF](https://www.ecmwf.int/)) ENS, up to 15 days in advance. We’ll be releasing our model’s code, weights, and forecasts, to support the wider weather forecasting community.

## The evolution of AI weather models

GenCast marks a critical advance in AI-based weather prediction that builds on our previous [weather model](https://deepmind.google/discover/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/), which was deterministic, and provided a single, best estimate of future weather. By contrast, a GenCast forecast comprises an ensemble of 50 or more predictions, each representing a possible weather trajectory.

GenCast is a diffusion model, the type of generative AI model that underpins the recent, rapid advances in [image](https://deepmind.google/technologies/imagen-3/), [video](https://deepmind.google/technologies/veo/) and [music generation](https://deepmind.google/discover/blog/new-generative-ai-tools-open-the-doors-of-music-creation/). However, GenCast differs from these, in that it’s adapted to the spherical geometry of the Earth, and learns to accurately generate the complex probability distribution of future weather scenarios when given the most recent state of the weather as input.

To train GenCast, we provided it with four decades of historical weather data from ECMWF’s [ERA5 archive](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5). This data includes variables such as temperature, wind speed, and pressure at various altitudes. The model learned global weather patterns, at 0.25° resolution, directly from this processed weather data.

## Setting a new standard for weather forecasting

To rigorously evaluate GenCast's performance, we trained it on historical weather data up to 2018, and tested it on data from 2019. GenCast showed better forecasting skill than ECMWF’s ENS, the top operational ensemble forecasting system that many national and local decisions depend upon every day.

We comprehensively tested both systems, looking at forecasts of different variables at different lead times — 1320 combinations in total. GenCast was more accurate than ENS on 97.2% of these targets, and on 99.8% at lead times greater than 36 hours.

![Two graphs compare GenCast and ENS for extreme heat and winds, showing GenCast provides higher relative economic value at 1- and 5-day lead times.](https://lh3.googleusercontent.com/TaPUItEf5BIjjGyyiefLTOh_Imebp0qVuHwngs5K6CSJnBHlXzhj5O4dYB-cXlwZo-vS4-QBiAbftn_8S0P6d9zoUtqvCZZAw3LUQjpF9JgU5TcAeKM=w1440)

Better forecasts of extreme weather, such as heat waves or strong winds, enable timely and cost-effective preventative actions. GenCast offers greater value than ENS when making decisions about preparations for extreme weather, across a wide range of decision-making scenarios.

An ensemble forecast expresses uncertainty by making multiple predictions that represent different possible scenarios. If most predictions show a cyclone hitting the same area, uncertainty is low. But if they predict different locations, uncertainty is higher. GenCast strikes the right balance, avoiding both overstating or understating its confidence in its forecasts.

It takes a single Google Cloud TPU v5 just 8 minutes to produce one 15-day forecast in GenCast’s ensemble, and every forecast in the ensemble can be generated simultaneously, in parallel. Traditional physics-based ensemble forecasts such as those produced by ENS, at 0.2° or 0.1° resolution, take hours on a supercomputer with tens of thousands of processors.

## Advanced forecasts for extreme weather events

More accurate forecasts of risks of extreme weather can help officials safeguard more lives, avert damage, and save money. When we tested GenCast’s ability to predict extreme heat and cold, and high wind speeds, GenCast consistently outperformed ENS.

Now consider tropical cyclones, also known as hurricanes and typhoons. Getting better and more advanced warnings of where they’ll strike land is invaluable. GenCast delivers superior predictions of the tracks of these deadly storms.

![GenCast forecasts Typhoon Hagibis’s path at 7, 5, 3, and 1 days before landfall, showing predictions becoming more focused and accurate closer to landfall.](https://lh3.googleusercontent.com/XRybf2wdWzz9gjGDd7iEK65en5sl_PLkKBIZqCY-2jFzAOlmXQ5njnjLVgV74fGpFFII1OHWpObDFN5s9svoiYx5XSZaRBKIQd-Ow46uwQuNaZ2arA=w1440)

GenCast’s ensemble forecast shows a wide range of possible paths for Typhoon Hagibis seven days in advance, but the spread of predicted paths tightens over several days into a high-confidence, accurate cluster as the devastating cyclone approaches the coast of Japan.

Better forecasts could also play a key role in other aspects of society, such as renewable energy planning. For example, improvements in wind-power forecasting directly increase the reliability of wind-power as a source of sustainable energy, and will potentially accelerate its adoption. In a proof-of-principle experiment that analyzed predictions of the total wind power generated by groupings of wind farms all over the world, GenCast was more accurate than ENS.

## Next generation forecasting and climate understanding at Google

GenCast is part of Google’s growing suite of next-generation AI-based weather models, including Google DeepMind’s AI-based [deterministic medium-range forecasts](https://www.science.org/doi/10.1126/science.adi2336), and Google Research’s [NeuralGCM](https://research.google/blog/fast-accurate-climate-modeling-with-neuralgcm/), [SEEDS](https://research.google/blog/generative-ai-to-quantify-uncertainty-in-weather-forecasting/), and [floods models](https://www.nature.com/articles/s41586-024-07145-1). These models are starting to power user experiences on Google Search and Maps, and improving the forecasting of [precipitation](https://research.google/blog/metnet-3-a-state-of-the-art-neural-weather-model-available-in-google-products/), [wildfires](https://blog.google/outreach-initiatives/sustainability/google-ai-wildfire-detection/), [flooding](https://research.google/blog/a-flood-forecasting-ai-model-trained-and-evaluated-globally/) and [extreme heat](https://blog.google/outreach-initiatives/sustainability/google-ai-research-extreme-heat-resilience/).

We deeply value our partnerships with weather agencies, and will continue working with them to develop AI-based methods that enhance their forecasting. Meanwhile, traditional models remain essential for this work. For one thing, they supply the training data and initial weather conditions required by models such as GenCast. This cooperation between AI and traditional meteorology highlights the power of a combined approach to improve forecasts and better serve society.

To foster wider collaboration and help accelerate research and development in the weather and climate community, we’ve made GenCast an open model and released its [code](https://github.com/google-deepmind/graphcast) and [weights](https://console.cloud.google.com/storage/browser/dm_graphcast), as we did for our deterministic medium-range global weather forecasting model.

We'll soon be releasing real-time and historical forecasts from GenCast, and previous models, which will enable anyone to integrate these weather inputs into their own models and research workflows.

We are eager to engage with the wider weather community, including academic researchers, meteorologists, data scientists, renewable energy companies, and organizations focused on food security and disaster response. Such partnerships offer deep insights and constructive feedback, as well as invaluable opportunities for commercial and non-commercial impact, all of which are critical to our mission to apply our models to benefit humanity.

[Read our paper](https://www.nature.com/articles/s41586-024-08252-9)

**Acknowledgements**

We would like to recognize Raia Hadsell for supporting this work. We are grateful to Molly Beck for providing legal support; Ben Gaiarin, Roz Onions and Chris Apps for providing licensing support; Matthew Chantry, Peter Dueben and the dedicated team at the ECMWF for their help and feedback; and to our Nature reviewers for their careful and constructive feedback.

This work reflects the contributions of the paper’s co-authors: Ilan Price, Alvaro Sanchez-Gonzalez, Ferran Alet, Tom Andersson, Andrew El-Kadi, Dominic Masters, Timo Ewalds, Jacklynn Stott, Shakir Mohamed, Peter Battaglia, Remi Lam, and Matthew Willson.
