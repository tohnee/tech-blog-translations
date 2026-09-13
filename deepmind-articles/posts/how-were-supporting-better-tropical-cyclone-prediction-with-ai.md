---
title: "How we're supporting better tropical cyclone prediction with AI"
source: https://deepmind.google/blog/how-were-supporting-better-tropical-cyclone-prediction-with-ai/
site: deepmind
date: 2025-06-12
authors: Weather Lab team
crawled: 2026-09-13
---

We’re launching Weather Lab, featuring our experimental cyclone predictions, and we’re partnering with the U.S. National Hurricane Center to support their forecasts and warnings this cyclone season.

Tropical cyclones are extremely dangerous, endangering lives and devastating communities in their wake. And in the past 50 years, they’ve caused [$1.4 trillion in economic losses](https://wmo.int/topics/tropical-cyclone).

These vast, rotating storms, also known as hurricanes or typhoons, form over warm ocean waters — fueled by heat, moisture and convection. They are very sensitive to even small differences in atmospheric conditions, making them notoriously difficult to forecast accurately. Yet, improving the accuracy of cyclone predictions can help protect communities through [more effective disaster preparedness](https://www.nber.org/digest/202409/value-improving-hurricane-forecasts) and earlier evacuations.

Today, Google DeepMind and Google Research are launching [Weather Lab](https://deepmind.google.com/science/weatherlab?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=), an interactive website for sharing our artificial intelligence (AI) weather models. Weather Lab features our latest experimental AI-based tropical cyclone model, based on stochastic neural networks. This model can predict a cyclone’s formation, track, intensity, size and shape — generating 50 possible scenarios, up to 15 days ahead.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Animation showing a prediction from our experimental cyclone model. Our model (in blue) accurately predicted the paths of Cyclones Honde and Garance, south of Madagascar, at the time they were active. Our model also captured the paths of Cyclones Jude and Ivone in the Indian Ocean, almost seven days in the future, robustly predicting areas of stormy weather that would eventually intensify into tropical cyclones.

We’ve released a [new paper](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/how-we-re-supporting-better-tropical-cyclone-prediction-with-ai/skillful-joint-probabilistic-weather-forecasting-from-marginals.pdf?utm_source=&utm_medium=&utm_campaign=&utm_content=) describing our core weather model, and are providing an archive on Weather Lab of historical cyclone track data, for evaluation and backtesting.

Internal testing shows that our model's predictions for cyclone track and intensity are as accurate as, and often more accurate than**,** current physics-based methods. We’ve been partnering with the U.S. National Hurricane Center ([NHC](https://www.nhc.noaa.gov/)), who assess cyclone risks in the Atlantic and East Pacific basins, to scientifically validate our approach and outputs.

NHC expert forecasters are now seeing live predictions from our experimental AI models, alongside other physics-based models and observations. We hope this data can help improve NHC forecasts and provide earlier and more accurate warnings for hazards linked to tropical cyclones.

## Weather Lab’s live and historical cyclone predictions

[Weather Lab](https://deepmind.google.com/science/weatherlab?utm_source=&utm_medium=&utm_campaign=&utm_content=) shows live and historical cyclone predictions for different AI weather models, alongside physics-based models from the European Centre for Medium-Range Weather Forecasts ([ECMWF](https://www.ecmwf.int/)). Several of our AI weather models are running in real time: WeatherNext Graph, WeatherNext Gen and our latest experimental cyclone model. We’re also launching Weather Lab with over two years of historical predictions for experts and researchers to download and analyze, enabling external evaluations of our models across all ocean basins.

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

Animation showing our model’s prediction for Cyclone Alfred when it was a Category 3 cyclone in the Coral Sea. The model’s ensemble mean prediction (bold blue line) correctly anticipated Cyclone Alfred’s rapid weakening to tropical storm status and eventual landfall near Brisbane, Australia, seven days later, with a high probability of landfall somewhere along the Queensland coast.

Weather Lab users can explore and compare the predictions from various AI and physics-based models. When read together, these predictions can help weather agencies and emergency service experts better anticipate a cyclone’s path and intensity. This could help experts and decision-makers better prepare for different scenarios, share news of risks involved and support decisions to manage a cyclone’s impact.

It's important to emphasise that Weather Lab is a research tool. Live predictions shown are generated by models still under development and are not official warnings. Please keep this in mind when using the tool, including to support decisions based on predictions generated by Weather Lab. For official weather forecasts and warnings, refer to your local meteorological agency or national weather service.

## AI-powered cyclone predictions

In physics-based cyclone prediction, the approximations required to meet operational demands mean it’s difficult for a single model to excel at predicting both a cyclone’s track and its intensity. This is because a cyclone's track is governed by vast atmospheric steering currents, whereas a cyclone’s intensity depends on complex turbulent processes within and around its compact core. Global, low-resolution models perform best at predicting cyclone tracks, but don’t capture the fine-scale processes dictating cyclone intensity, which is why regional, high-resolution models are needed.

Our experimental cyclone model is a single system that overcomes this trade-off, with our internal evaluations showing state-of-the-art accuracy for both cyclone track and intensity. It’s trained to model two distinct types of data: a vast reanalysis dataset that reconstructs past weather over the entire Earth from millions of observations, and a specialized database containing key information about the track, intensity, size and wind radii of nearly 5,000 observed cyclones from the past 45 years.

Modeling the analysis data and cyclone data together greatly improves cyclone prediction capabilities. For example, our initial evaluations of NHC’s observed hurricane data, on test years 2023 and 2024, in the North Atlantic and East Pacific basins, showed that our model’s 5-day cyclone track prediction is, on average, 140 km closer to the true cyclone location than ENS — the leading global physics-based ensemble model from ECMWF. This is comparable to the accuracy of ENS’s 3.5-day predictions — a 1.5-day improvement that has typically taken [over a decade to achieve](https://ourworldindata.org/grapher/hurricane-track-error).

While previous AI weather models have struggled to calculate cyclone intensity, our experimental cyclone model outperformed the average intensity error of the National Oceanic and Atmospheric Administration ([NOAA](https://www.noaa.gov/))’s Hurricane Analysis and Forecast System ([HAFS](https://www.aoml.noaa.gov/hurricane-modeling-prediction/#hafs)), a leading regional, high-resolution physics-based model. Preliminary tests also show our model’s predictions of size and wind radii are comparable with physics-based baselines.

Here we visualize track and intensity prediction errors, and show evaluation results of our experimental cyclone model’s average performance up to five days in advance, compared to ENS and HAFS.

![Four-panel chart comparing cyclone track and intensity prediction errors, demonstrating the accuracy of the experimental AI model over established models](https://lh3.googleusercontent.com/z3RtVV-EUuIRNZQkKDSkjxk6bAOTiAwC4tFvriyZ5GvA3MTNekYtkio2MwujmjF_A-w6EjKncdPN7yoUFCbWLww7lVvu4guQV9A6-4IXXESwW5selLg=w1440)

Evaluations of our experimental cyclone model’s track and intensity predictions compared to leading physics-based models ENS and HAFS-A. Our evaluations use NHC best-tracks as ground truth and follow their homogenous verification protocol.

## More useful data for decision makers

In addition to the NHC, we’ve been working closely with the Cooperative Institute for Research in the Atmosphere ([CIRA](https://www.cira.colostate.edu/)) at Colorado State University. Dr. Kate Musgrave, a CIRA Research Scientist, and her team evaluated our model and found it to have “comparable or greater skill than the best operational models for track and intensity.” Musgrave stated, “We’re looking forward to confirming those results from real-time forecasts during the 2025 hurricane season”. We’ve also been working with the [UK Met Office](https://www.metoffice.gov.uk/), [University of Tokyo](https://www.u-tokyo.ac.jp/en/), Japan’s [Weathernews Inc.](https://global.weathernews.com/) and other experts to improve our models.

Our new experimental tropical cyclone model is the latest milestone in our series of pioneering [WeatherNext research](https://deepmind.google/science/weathernext/?utm_source=&utm_medium=&utm_campaign=&utm_content=). By sharing our AI weather models responsibly through Weather Lab, we’ll continue to gather important feedback from weather agency and emergency service experts about how our technology can improve official forecasts and inform life-saving decisions.

[Visit Weather Lab](https://deepmind.google.com/science/weatherlab?utm_source=&utm_medium=&utm_campaign=&utm_content=)[Read our paper](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/how-we-re-supporting-better-tropical-cyclone-prediction-with-ai/skillful-joint-probabilistic-weather-forecasting-from-marginals.pdf?utm_source=&utm_medium=&utm_campaign=&utm_content=)

**Acknowledgements**
This research was co-developed by Google DeepMind and Google Research.

We’d like to thank our collaborators NOAA’s NHC, CIRA, the UK Met Office, University of Tokyo, Japan’s Weathernews Inc., Bryan Norcross at FOX Weather and our other trusted tester partners that have shared invaluable feedback throughout the development of Weather Lab.
