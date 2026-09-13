---
title: "Ask a Scientist: How can researchers use AI to predict a flood?"
source: https://blog.google/innovation-and-ai/technology/research/flood-prediction-ai/
site: google-blog
date: 2026-08-18
authors: Hannah Hunt
crawled: 2026-09-13
---

In 2018, we [piloted](https://blog.google/products-and-platforms/products/search/helping-keep-people-safe-ai-enabled-flood-forecasting/) a flood forecasting model in India that relied on real-time river data to predict a flood. Since then, our [advancements](https://research.google/blog/a-flood-forecasting-ai-model-trained-and-evaluated-globally/) in AI have made it possible for us to make predictions in 150 countries around the world where more than 2 billion people live. And in March 2026, [we announced Groundsource](https://blog.google/innovation-and-ai/technology/research/gemini-help-communities-predict-crisis/), a new AI-powered methodology that transforms public disaster data into a high-quality data archive — starting with flash floods in urban areas. We sat down with Deborah Cohen, a senior staff research scientist from Google Research, to understand how AI has made flood forecasting possible and what potential the research holds for predicting other natural disasters.

**What do you do at Google?**

I lead the Flood Forecasting work on the Climate Crisis Resilience team. Our goal is to keep people safe from natural disasters using AI, starting with floods, one of the most common — and deadliest — natural disasters. Early warnings can prevent much of the harm floods cause. This is why we started the Google Flood Forecasting Initiative: We want everyone to have access to forecasts and warnings so they can be safe and informed.

**How does Google use AI to predict a flood?**

That’s changed a few times since we first started this research nearly a decade ago! But at a very basic level, we use a collection of models to crunch massive amounts of global data on things like rainfall, river levels, and ground surface conditions to predict riverine floods up to seven days before they strike and urban flash floods up to 24 hours before they hit. These predictions live in our [Flood Hub](https://sites.research.google/floods/) tool and also show up in Search when people are looking for more information on a flood in their area. We also provide a Floods API that gives organizations access to flood predictions, helping them warn and support people before the most severe floods hit.

Flood Hub in action

![Screenshot of the Flood Hub tool showing a map of the world with different shadings to indicate flood risks.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Flood_Hub.width-1200.format-webp.webp)

**What does Flood Hub do?**

Flood Hub takes leading weather data from around the world and uses AI to create prediction alerts on a map. This is a major leap from traditional flood models, which typically require local historical data like water levels for calibration. Our AI allows us to pull from information across the world to provide predictions in locations even without historical data — which is critical since people who need warnings the most usually live in data-scarce regions.

When we first built the Flood Hub tool, it was limited to predicting when a river would flood. Over the last few years, we’ve built a new AI methodology called Groundsource, which expanded our coverage to include urban flash flooding.

**Why did it take us longer to integrate urban flash flooding into Flood Hub?**

We had a huge amount of global data on river floods and almost none on urban flash floods. Flood Hub predicts river floods with two AI models that process a range of publicly available data sources. The Hydrologic Model uses weather and land conditions to forecast the amount of water that will flow through a river, and the Inundation Model uses streamflow data to predict what areas will be affected. There are a lot of physical gauges — or rulers — in rivers around the world to measure water levels over time, which helps with those predictions. It’s really unusual to find sensors monitoring flash flooding in urban areas, so we don’t have that kind of historical data for urban flash floods.

**Where did you go to find data on urban flooding?**

Without an authoritative global data set on urban flooding, we knew we’d need to build it ourselves. That’s when we came up with the idea for Groundsource. First, it used Gemini to read over 5 million news reports about flooding spanning a 20-year period, creating a massive, unique dataset of 2.6 million historical flood events in more than 150 countries. We then integrated that data into a new urban flash flood model that’s live in Flood Hub.

**How is Flood Hub helping communities impacted by floods?**

Researchers and aid organizations, like [Give Directly](https://www.givedirectly.org/flood-forecast-ai), are using Flood Hub to help understand where floods will occur and who’s at risk. Last year, by using our [Flood Forecasting API](https://developers.google.com/flood-forecasting), Give Directly was able to deliver cash to people in Kogi, Nigeria — one of the most flood-affected regions in West Africa — before water actually rose. They found that this early cash helped families evacuate, protect assets, and rebuild. Incomes more than doubled, food insecurity dropped by 90%, and 93% of recipients felt better prepared for future floods.

**What’s next for Flood Hub and Groundsource?**

The models that power Flood Hub are currently limited to predicting flash floods in urban areas because that’s where we have the best data. We’re researching ways to increase the quality of our models and to include predictions for flash flooding in rural areas, as well as coastal flooding. This is pretty difficult to do with the data sets we currently have, but we haven’t let that stop us before — that’s why we created Groundsource, to fill a data gap. We’re also doing more research there to see how the Groundsource methodology could be useful for other disasters like heat waves or mudslides.

**Where can researchers find this data?**

To help further protect the communities that most need this information, we [open sourced](https://research.google/blog/the-next-chapter-in-flood-resilience-open-sourcing-googles-hydrology-framework/) our hydrology framework. This enables National Meteorological and Hydrological Services (NMHSs) and other meteorological agencies to integrate their own data with the model, generate tailored forecasts, and use those forecasts for their specific needs. We’ve also made the [Groundsource dataset](https://zenodo.org/records/18647054) and the [Flood Forecasting API](https://developers.google.com/flood-forecasting) publicly available to help improve future research on floods. Ultimately, this is all part of our goal to use AI to help accurately predict natural disasters and keep as many people safe as possible.
