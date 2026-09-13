---
title: "GraphCast: AI model for faster and more accurate global weather forecasting"
source: https://deepmind.google/blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/
site: deepmind
date: 2023-11-14
authors: Remi Lam, GraphCast team
crawled: 2026-09-13
---

Our state-of-the-art model delivers 10-day weather predictions at unprecedented accuracy in under one minute

The weather affects us all, in ways big and small. It can dictate how we dress in the morning, provide us with green energy and, in the worst cases, create storms that can devastate communities. In a world of increasingly extreme weather, fast and accurate forecasts have never been more important.

In a paper [published in Science](https://www.science.org/stoken/author-tokens/ST-1550/full), we introduce GraphCast, a state-of-the-art AI model able to make medium-range weather forecasts with unprecedented accuracy. GraphCast predicts weather conditions up to 10 days in advance more accurately and much faster than the industry gold-standard weather simulation system – the High Resolution Forecast (HRES), produced by the European Centre for Medium-Range Weather Forecasts (ECMWF).

GraphCast can also offer earlier warnings of extreme weather events. It can predict the tracks of cyclones with great accuracy further into the future, identifies atmospheric rivers associated with flood risk, and predicts the onset of extreme temperatures. This ability has the potential to save lives through greater preparedness.

GraphCast takes a significant step forward in AI for weather prediction, offering more accurate and efficient forecasts, and opening paths to support decision-making critical to the needs of our industries and societies. And, by [open sourcing the model code for GraphCast,](https://github.com/google-deepmind/graphcast) we are enabling scientists and forecasters around the world to benefit billions of people in their everyday lives. GraphCast is already being used by weather agencies, including ECMWF, which is running a live experiment of [our model’s forecasts on its website](https://charts.ecmwf.int/products/graphcast_medium-mslp-wind850).

![](https://lh3.googleusercontent.com/OWZ3ECzygWSBeHJhs_DT9Lkb2Sr7bQX21ImJimz3DFV172vj73m9j54swniHpHn3aK0QTKhhA19QkIH-7EuABWF3_mroVtOjWPnzebaLWlokJzZNxr8=w1440-h810-n-nu)

A selection of GraphCast’s predictions rolling across 10 days showing specific humidity at 700 hectopascals (about 3 km above surface), surface temperature, and surface wind speed.

## The challenge of global weather forecasting

Weather prediction is one of the oldest and most challenging–scientific endeavours. Medium range predictions are important to support key decision-making across sectors, from renewable energy to event logistics, but are difficult to do accurately and efficiently.

Forecasts typically rely on Numerical Weather Prediction (NWP), which begins with carefully defined physics equations, which are then translated into computer algorithms run on supercomputers. While this traditional approach has been a triumph of science and engineering, designing the equations and algorithms is time-consuming and requires deep expertise, as well as costly compute resources to make accurate predictions.

Deep learning offers a different approach: using data instead of physical equations to create a weather forecast system. GraphCast is trained on decades of historical weather data to learn a model of the cause and effect relationships that govern how Earth’s weather evolves, from the present into the future.

Crucially, GraphCast and traditional approaches go hand-in-hand: we trained GraphCast on four decades of weather reanalysis data, from the ECMWF’s ERA5 dataset. This trove is based on historical weather observations such as satellite images, radar, and weather stations using a traditional NWP to ‘fill in the blanks’ where the observations are incomplete, to reconstruct a rich record of global historical weather.

## GraphCast: An AI model for weather prediction

GraphCast is a weather forecasting system based on machine learning and Graph Neural Networks (GNNs), which are a particularly useful architecture for processing spatially structured data.

GraphCast makes forecasts at the high resolution of 0.25 degrees longitude/latitude (28km x 28km at the equator). That’s more than a million grid points covering the entire Earth’s surface. At each grid point the model predicts five Earth-surface variables – including temperature, wind speed and direction, and mean sea-level pressure – and six atmospheric variables at each of 37 levels of altitude, including specific humidity, wind speed and direction, and temperature.

While GraphCast’s training was computationally intensive, the resulting forecasting model is highly efficient. Making 10-day forecasts with GraphCast takes less than a minute on a single Google TPU v4 machine. For comparison, a 10-day forecast using a conventional approach, such as HRES, can take hours of computation in a supercomputer with hundreds of machines.

In a comprehensive performance evaluation against the gold-standard deterministic system, HRES, GraphCast provided more accurate predictions on more than 90% of 1380 test variables and forecast lead times (see our [Science paper](https://www.science.org/stoken/author-tokens/ST-1550/full) for details). When we limited the evaluation to the troposphere, the 6-20 kilometer high region of the atmosphere nearest to Earth’s surface where accurate forecasting is most important, our model outperformed HRES on 99.7% of the test variables for future weather.

![A three-step diagram showing how GraphCast works: a) taking stacked global weather maps as input, b) predicting the next weather state, and c) rolling out a series of future forecasts.](https://lh3.googleusercontent.com/Ujm4BZdWGHc7JaTDZntbC4qzyawCJUseZdJHMgmFJRnO3Eu6wj3xd25n0ZiCpJhluo7J1Rm7to3ZVvLTkneLVELXj9q7kuMzPHtFcqOPEeLW-VeY=w1440)

For inputs, GraphCast requires just two sets of data: the state of the weather 6 hours ago, and the current state of the weather. The model then predicts the weather 6 hours in the future. This process can then be rolled forward in 6-hour increments to provide state-of-the-art forecasts up to 10 days in advance.

## Better warnings for extreme weather events

Our analyses revealed that GraphCast can also identify severe weather events earlier than traditional forecasting models, despite not having been trained to look for them. This is a prime example of how GraphCast could help with preparedness to save lives and reduce the impact of storms and extreme weather on communities.

By applying a simple cyclone tracker directly onto GraphCast forecasts, we could predict cyclone movement more accurately than the HRES model. In September, a live version of our publicly available GraphCast model, deployed on the ECMWF website, accurately predicted about nine days in advance that Hurricane Lee would make landfall in Nova Scotia. By contrast, traditional forecasts had greater variability in where and when landfall would occur, and only locked in on Nova Scotia about six days in advance.

GraphCast can also characterize atmospheric rivers – narrow regions of the atmosphere that transfer most of the water vapour outside of the tropics. The intensity of an atmospheric river can indicate whether it will bring beneficial rain or a flood-inducing deluge. GraphCast forecasts can help characterize atmospheric rivers, which could help planning emergency responses together with [AI models to forecast floods.](https://sites.research.google/floodforecasting/?utm_source=&utm_medium=&utm_campaign=&utm_content=)

Finally, predicting extreme temperatures is of growing importance in our warming world. GraphCast can characterize when the heat is set to rise above the historical top temperatures for any given location on Earth. This is particularly useful in anticipating heat waves, disruptive and dangerous events that are becoming increasingly common.

![Two line graphs comparing the forecast error of GraphCast (blue line) and the HRES model (black line) over lead time in days. The left graph, titled "Cyclone tracking," shows GraphCast has a lower median track error (km) over a 5-day lead time. The right graph, titled "Atmospheric rivers," shows GraphCast has a lower root-mean-square error (kg/m/s) over a 10-day lead time.](https://lh3.googleusercontent.com/cIsyDic31c-LYmEWuhfK0UQGYqC63trY-UccLJphHv9sEzxyboyGRNP6HRj7hSUw2Ky97Mf_Gc6PCeJf1M9DpwFaKyEXrzD2xBUEsg_gyVheNI2LLLQ=w1440)

Severe-event prediction - how GraphCast and HRES compare.

Left: Cyclone tracking performances. As the lead time for predicting cyclone movements grows, GraphCast maintains greater accuracy than HRES.

Right: Atmospheric river prediction. GraphCast’s prediction errors are markedly lower than HRES’s for the entirety of their 10-day predictions

## The future of AI for weather

GraphCast is now the most accurate 10-day global weather forecasting system in the world, and can predict extreme weather events further into the future than was previously possible. As the weather patterns evolve in a changing climate, GraphCast will evolve and improve as higher quality data becomes available.

To make AI-powered weather forecasting more accessible, we’ve [open sourced our model’s code](https://github.com/google-deepmind/graphcast). ECMWF is already [experimenting with GraphCast’s 10-day forecasts](https://charts.ecmwf.int/products/graphcast_medium-mslp-wind850) and we’re excited to see the possibilities it unlocks for researchers – from tailoring the model for particular weather phenomena to optimizing it for different parts of the world.

GraphCast joins other state-of-the-art weather prediction systems from Google DeepMind and Google Research, including a regional [Nowcasting model](https://deepmind.google/discover/blog/nowcasting-the-next-hour-of-rain/) that produces forecasts up to 90 minutes ahead, and [MetNet-3](https://blog.research.google/2023/11/metnet-3-state-of-art-neural-weather.html?utm_source=&utm_medium=&utm_campaign=&utm_content=), a regional weather forecasting model already in operation across the US and Europe that produces more accurate 24-hour forecasts than any other system.

Pioneering the use of AI in weather forecasting will benefit billions of people in their everyday lives. But our wider research is not just about anticipating weather – it’s about understanding the broader patterns of our climate. By developing new tools and accelerating research, we hope AI can empower the global community to tackle our greatest environmental challenges.

![](https://lh3.googleusercontent.com/a3uPjh6ngpq8MS7AWnKkn-Kh6BbXrXwrNqUiY6FZDgFR2ODBMr1zvMztdb-3GTnE28sYbyDTVYUeKfrJDlvbjP3taDAHMIG6cAtWgPPR8CenowjfLA=w1440-h810-n-nu)

**Learn more about GraphCast**

[Read our paper in Science](https://www.science.org/stoken/author-tokens/ST-1550/full)[Read an open access copy of our paper\*](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/graphcast-ai-model-for-faster-and-more-accurate-global-weather-forecasting/Learning_skillful_medium-range_global_weather_forecasting.pdf?utm_source=&utm_medium=&utm_campaign=&utm_content=/)[Access GraphCast on Github](https://github.com/google-deepmind/graphcast)[View GraphCast live on ECMWF](https://charts.ecmwf.int/products/graphcast_medium-mslp-wind850)

We are grateful to Matthew Chantry, Peter Dueben and Linus Magnusson from ECMWF, for their help and feedback. We also want to thank Svetlana Grant, Jon Small for providing legal support. This work was done thanks to the contributions of the co-authors: Remi Lam, Alvaro Sanchez-Gonzalez, Matthew Willson, Peter Wirnsberger, Meire Fortunato, Ferran Alet, Suman Ravuri, Timo Ewalds, Zach Eaton-Rosen, Weihua Hu, Alexander Merose, Stephan Hoyer, George Holland, Oriol Vinyals, Jacklynn Stott, Alexander Pritzel, Shakir Mohamed and Peter Battaglia.

\*This is the author's version of the work. It is posted here by permission of the AAAS for personal use, not for redistribution. The definitive version was published in Science doi: 10.1126/science.adi2336.
