---
title: "Ask a Scientist: How do researchers use AI to predict a cyclone?"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/weathernext-extreme-weather-cyclone-predictions/
site: google-blog
date: 2026-09-01
authors: Hannah Hunt
crawled: 2026-09-13
---

As extreme weather events impact more communities around the world, the ability to accurately predict a storm's path is critical to keeping people safe. By combining decades of historical atmospheric data with advanced AI, Google researchers have achieved [a massive leap](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/weathernext-2-cyclones/) in cyclone forecasting accuracy — turning what once required building-sized supercomputers into life-saving models that can run on a single TPU. We sat down with Ferran Alet, a research scientist at Google DeepMind who helped develop our [WeatherNext](https://deepmind.google/science/weathernext/) models, to explore how this breakthrough technology is giving people and first responders the vital gift of time before a cyclone strikes.

**What do you do at Google?**

I came to Google DeepMind’s weather team after a background in academia exploring the intersection of AI and physics. Now, I’m using that background to apply AI to traditional physics-based models to better predict future weather. My team works on the WeatherNext forecasting models, which we've built to help meteorologists and scientists access AI-powered extreme weather predictions. These predictions help people get more accurate forecasts and warnings ahead of potentially devastating weather events, like cyclones.

**Before we go further: cyclones, hurricanes, typhoons — which is it?**

They all mean the same thing! Cyclones is the global scientific term for hurricanes and typhoons. In the Atlantic region, they’re called hurricanes, and in the North Pacific, they say typhoons. But all of the terms refer to a large-scale, rotating storm system that forms over a warm ocean. The warmth in the ocean causes warm, moist air to rise, which creates an area of low pressure beneath it and draws in cooler air. The Earth’s rotation causes that cycle of rising moist air and drawing in of cooling air to spin. Combine that with heavy rain and strong winds, and you have a cyclone…or hurricane or typhoon, depending on where you live.

**How have researchers predicted cyclones in the past?**

Historically, forecasting cyclones relied on physics-based models powered by supercomputers the size of shipping containers, or even as big as three-story buildings. Scientists used these machines to simulate the laws of fluid dynamics, predicting future weather based on *current* weather data from global sensors. But the data from those global sensors is often incomplete or noisy, and simulating exact physics requires immense computing power, which slows down the progress we can make in forecasting things like cyclones. The meteorological community historically gained about one day of forecast accuracy per decade, by building better models, launching more satellites and getting more computing power. By applying AI to the data from these physics-based models, we saw that same [decade of progress](https://deepmind.google/blog/weathernext-ai-model-achieves-breakthrough-in-forecasting-cyclones/) in a single generation leap of WeatherNext models.

**How are we using AI to change the way we predict cyclones?**

Physics models are really good at telling us about the past and the present. AI allows us to better predict the future, based on patterns from the past and data from the present. With WeatherNext, we trained AI on 50 years of historical weather data. Instead of having to rely on building-sized supercomputers, researchers can run these faster models on a single TPU. This gives the scientific community a massive leap in accuracy, improving predictions for both where a cyclone will hit and how intense it will be when it makes landfall. Weather agencies are looking to extend their public forecast horizons from five days to seven, giving communities vital extra time to prepare before a cyclone hits.

**What kind of difference can that extra time make for people who need it?**

We saw how crucial that time was last year with [Hurricane Melissa](https://deepmind.google/blog/how-weathernext-helped-the-national-hurricane-center-better-predict-hurricane-melissas-historic-landfall-in-jamaica). Ahead of hurricane season, we partnered with the National Hurricane Center to support their forecasts. What was notable about Melissa was that, while the hurricane initially appeared weak, the AI's high-confidence predictions helped the National Hurricane Center to issue a historic forecast, warning authorities of its rapid intensification from a Category 1 storm into a Category 5. It proved to be one of the most powerful hurricanes in history, which we could see from our models days in advance of it making landfall. The additional day of warning allowed authorities in Jamaica to make life-saving emergency preparations.

**What does technology like WeatherNext mean for the future of extreme weather forecasting?**

We’ve [open-sourced](https://github.com/google-deepmind/weathernext) our WeatherNext 2 and WeatherNext cyclones models, and developed an interactive [Weather Lab](https://deepmind.google.com/science/weatherlab) website to advance science for a global scientific community. This widespread access helps academics and scientists freely experiment with the models and hopefully make new discoveries that help people around the world.
