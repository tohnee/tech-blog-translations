---
title: "Nowcasting the next hour of rain"
source: https://deepmind.google/blog/nowcasting-the-next-hour-of-rain/
site: deepmind
date: 2021-09-29
authors: Nowcasting team
crawled: 2026-09-13
---

Our lives are dependent on the weather. At any moment in the UK, according to [one study](https://www.bbc.com/future/article/20151214-why-do-brits-talk-about-the-weather-so-much), one third of the country has talked about the weather in the past hour, reflecting the importance of weather in daily life. Amongst weather phenomena, rain is especially important because of its influence on our everyday decisions. Should I take an umbrella? How should we route vehicles experiencing heavy rain? What safety measures do we take for outdoor events? Will there be a flood?

[Our latest research](https://www.nature.com/articles/s41586-021-03854-z) and state-of-the-art model advances the science of [Precipitation Nowcasting](https://public.wmo.int/en/resources/bulletin/nowcasting-guidelines-%E2%80%93-summary), which is the prediction of rain (and other precipitation phenomena) within the next 1-2 hours. In a [paper](https://www.nature.com/articles/s41586-021-03854-z) written in collaboration with the Met Office and published in Nature, we directly tackle this important [grand challenge](https://www.nssl.noaa.gov/about/challenges/) in weather prediction. This collaboration between environmental science and AI focuses on value for decision-makers, opening up new avenues for the nowcasting of rain, and points to the opportunities for AI in supporting our response to the challenges of decision-making in an environment under constant change.

## Short-term weather predictions

Throughout history, the prediction of weather has held a place of importance for our communities and countries. [Medieval meteorologists](https://www.cambridge.org/core/books/medieval-meteorology/12DCC7DA683729A4E520C76ADCF6502D) began by using the stars to make predictions. Slowly, tables recording seasons and rain patterns started to be kept. Centuries later, Lewis Fry imagined a ‘[Forecast Factory](https://www.emetsoc.org/resources/rff/)’ that used computation and the physical equations of the atmosphere to predict global weather. In this evolving book of weather prediction, we now add a story on the role of machine learning for forecasting.

Today’s weather predictions are driven by powerful [numerical weather prediction](https://www.metoffice.gov.uk/weather/learn-about/how-forecasts-are-made/computer-models/history-of-numerical-weather-prediction) (NWP) systems. By solving physical equations, NWPs provide essential planet-scale predictions several days ahead. However, they struggle to generate high-resolution predictions for short lead times under two hours. Nowcasting fills the performance gap in this crucial time interval.

Nowcasting is essential for sectors like water management, agriculture, aviation, emergency planning, and [outdoor events](https://journals.ametsoc.org/view/journals/wefo/25/6/2010waf2222417_1.xml). Advances in weather sensing have made high-resolution radar data–which measures the amount of precipitation at ground level–available at high frequency (e.g., every 5 mins at 1 km resolution). This combination of a crucial area where existing methods struggle and the availability of high-quality data provides the opportunity for machine learning to make its contributions to nowcasting.

![Diagram showing how a deep generative model of rain processes context data from the past 20 minutes to generate a nowcast of precipitation for the next 90 minutes.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227e31239003803b4eb74db_Fig201.gif)

Past 20 mins of observed radar are used to provide probabilistic predictions for the next 90 mins using a Deep Generative Model of Rain (DGMR).

## Generative models for nowcasting

We focus on nowcasting rain: predictions up to 2 hours ahead that capture the amount, timing, and location of rainfall. We use an approach known as generative modelling to make detailed and plausible predictions of future radar based on past radar. Conceptually, this is a problem of generating radar movies. With such methods, we can both accurately capture large-scale events, while also generating many alternative rain scenarios (known as ensemble predictions), allowing rainfall uncertainty to be explored. We used radar data from both the UK and the US in our study results.

We were especially interested in the ability of these models to make predictions on medium to heavy-rain events, which are the events that most impact people and the economy, and we show statistically significant improvements in these regimes compared to competing methods. Importantly, we conducted a cognitive task assessment with more than 50 expert meteorologists at the Met Office, the UK’s national meteorological service, **who rated our new approach as their first choice in 89% of cases when compared to widely-used nowcasting methods**, demonstrating the ability of our approach to provide insight to real world decision-makers.

![Four radar maps of the UK showing rain patterns labeled Target, DGMR, PySTEPS, and UNet.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227e32e3d49b17ff5eba816_Fig202.gif)

A challenging event in April 2019 over the UK (Target is the observed radar). Our generative approach (DGMR) captures the circulation, intensity and structure better than an advection approach (PySTEPS), and more accurately predicts rainfall and motion in the northeast. DGMR also generates sharp predictions, unlike deterministic deep learning methods (UNet).

![Four radar maps of the UK showing rain patterns labeled Target, DGMR, PySTEPS, and UNet.](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227e35deb85793243440c30_Fig203.gif)

A heavy precipitation event in April 2019 over the eastern US (Target is the observed radar). The generative approach DGMR balances intensity and extent of precipitation compared to an advection approach (PySTEPS), the intensities of which are often too high, and does not blur like deterministic deep learning methods (UNet).

## What’s next

By using statistical, economic, and cognitive analyses we were able to demonstrate a new and competitive approach for precipitation nowcasting from radar. No method is without limitations, and more work is needed to improve the accuracy of long-term predictions and accuracy on rare and intense events. Future work will require us to develop additional ways of assessing performance, and further specialising these methods for specific real-world applications.

We think this is an exciting area of research and we hope our paper will serve as a foundation for new work by providing data and verification methods that make it possible to both provide competitive verification and operational utility. We also hope this collaboration with the Met Office will promote greater integration of machine learning and environmental science, and better support decision-making in our changing climate.

Read the paper [Skillful precipitation nowcasting using Deep Generative Models of Radar](https://www.nature.com/articles/s41586-021-03854-z) in the 30 September 2021 issue of Nature, which contains an extensive discussion of the model, data and verification approach. You can also explore the data we used for training and find a pre-trained model for the UK via [GitHub](https://dpmd.ai/github_nowcasting).

**Acknowledgements**

We are grateful to the Met Office and all our collaborators and advisors for their input to this work.
