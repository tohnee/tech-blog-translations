---
title: "How we’re using AI to help track and predict cyclones"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/weather-lab-ai-cyclone-prediction-tracking/
site: google-blog
date: 2025-08-04
authors: Joel Meares
crawled: 2026-09-13
---

In March, Google DeepMind’s Ferran Alet and Tom Andersson visited the fortress-like headquarters of the [National Hurricane Center](https://www.nhc.noaa.gov/) (NHC) in Miami. The pair recall being impressed by the operations room — where people gathered before a kaleidoscope of screens showing satellite imagery, radar and modeling — and the building’s 10-inch-thick concrete walls, designed to withstand winds up to 130 miles an hour.

Even during a [category 5 storm](https://www.nhc.noaa.gov/aboutsshws.php), the NHC must continue operating 24/7, issuing warnings and updates to help people prepare for and survive hurricanes — or cyclones and typhoons, as they’re known in other parts of the world. Ferran and Tom were there to share a first look at a new AI-powered experimental cyclone model to help them do just that.

Among the experts gathered in a boardroom to preview the model was a leading hurricane specialist who, some years before, had written a paper suggesting cyclone path prediction might have hit its limits. “After our presentation, he told us that our model’s performance was potentially revolutionary,” Tom says. “It was quite an honor.”

Now, Google DeepMind and Google Research are giving people outside that boardroom a first peek at the new model, which — unlike traditional forecasting models that simulate the complex physics of the atmosphere on supercomputers — makes predictions about cyclone path, size and intensity at unprecedented speeds. We’re sharing its forecasts with the NHC and launching [Weather Lab](https://deepmind.google.com/science/weatherlab), a new data and visualization platform hosting its real-time and historical predictions.

Our model (shown in blue) accurately predicted the paths of Cyclones Honde and Garance south of Madagascar, and captured the paths of Cyclones Jude and Ivone in the Indian Ocean almost seven days before they formed.

Timelier and more accurate forecasts of a storm’s movements and intensity are vital to giving forecasters the information they need to issue watches and warnings for hurricane hazards — and give people on the ground the time they need to evacuate or prepare their homes. But cyclones present a particular dilemma: They are one of the world’s most devastating weather events, and some of the hardest to predict.

“With weather generally, small differences and changes in data can result in widely different futures,” Ferran says. “But the extreme conditions of cyclones make them especially hard to simulate. They’re chaotic systems.”

Google DeepMind and Google Research had shown some promise in predicting cyclone tracks using historical data in weather models like [GenCast](https://blog.google/feed/gencast-weather-prediction/), [GraphCast](https://deepmind.google/discover/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/) and [NeuralGCM](https://research.google/blog/fast-accurate-climate-modeling-with-neuralgcm/). But these were designed for general weather, trained on low-resolution historical data and offered poor intensity predictions. Forecasters didn’t fully trust them. So the team began developing their experimental cyclone model to address the gap.

“Cyclones are so sparse and intense in terms of wind speed and vorticity that we had to change the way we actually trained our models,” Ferran says. “We now train on both general weather and sparse cyclone-specific data. To do that, rather than diffusion, which works iteratively in steps, we use a new probabilistic model that works in one step by introducing random perturbations during the prediction process, and ultimately produces a selection of 50 possible outcomes for the storm.”

According to preliminary internal evaluations, the new experimental cyclone model shows state-of-the-art accuracy for both cyclone track and intensity. It’s skillful at predicting a cyclone’s size as well.

The model’s ensemble mean prediction (bold blue line) correctly anticipated Cyclone Alfred’s rapid weakening to tropical storm status and eventual landfall near Brisbane, Australia, seven days later, with a high probability of landfall somewhere along the coast of the state of Queensland.

Trusted testers have had access to the model’s forecasts for about two months, providing the team with valuable feedback not just on accuracy, but how usefully they’re presenting the information and additional features that could help in their work.

On her own trip to the NHC — she remembers the formidable walls, too — Google Research product manager Olivia Graham sat side-by-side with a forecaster to walk her through [the interface](https://deepmind.google.com/science/weatherlab). It showed track and intensity predictions for current storms on a global map from the new model — and other Google weather models — along with official models the forecasters currently use for comparison.

“The forecaster told me that while this was helpful, a lot of their work involves looking at potential outcomes before a cyclone forms, or in the time of cyclogenesis,” Olivia says. “That actually led to the development of an ‘expert mode’ available to trusted testers where you can explore potential cyclones, grouping small circles on the map, each of which represents a ~2% chance of cyclone formation. This way you can see its potential track and strength should it form.”

That kind of close collaboration is key. “We’re really co-developing this technology with the people at the NHC who will be using it every day — asking what’s the most important data to them and how they want to use it,” Olivia says. “People in the path of danger depend on it, and we want to ensure we’re providing the best and most relevant information to help them save lives.”
