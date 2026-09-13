---
title: "How AI is helping 38 million farmers with advance weather predictions"
source: https://blog.google/innovation-and-ai/technology/research/indian-farmers-monsoon-prediction/
site: google-blog
date: 2025-09-15
authors: Olivia Graham
crawled: 2026-09-13
---

This summer, 38 million farmers in India received AI-powered forecasts of the start of the monsoon season, helping them make more informed decisions about when to plant their crops for the season. These forecasts were powered in part by NeuralGCM, a Google Research model, which combines traditional physics-based modeling with machine learning for improved simulation accuracy and efficiency.

## An AI model to predict weather and climate

For years, weather and climate models have been costly and complex, often requiring a supercomputer to run. Our teams at Google Research wanted to see if we could build these models more efficiently and more accurately, leading to the creation of NeuralGCM. Unlike traditional models that rely purely on hard-coded physics, this AI-driven model is trained on decades of historical weather data to infer patterns and learn from past events, while also using physics. Crucially, it’s designed to be flexible and efficient — it can run on a single laptop, making high-quality forecasting more accessible to the scientific community.

## A collaboration with University of Chicago

When we open-sourced NeuralGCM, we hoped the community would use this new tool to power their own innovative applications. The University of Chicago's [Human-Centered Weather Forecasts Initiative](https://humancenteredforecasts.climate.uchicago.edu/) did just that. They recognized that one of the most impactful, yet increasingly challenging, decisions for Indian farmers is when to put seeds in the ground. Hundreds of millions of smallholder farmers across the tropics depend on information about when the rainy season, known as the monsoon, will come each year. However, accurate forecasting of when the monsoon will begin, especially at long lead times and at local scales, has remained a century-old challenge.

By rigorously testing several AI weather models, the University of Chicago team found that NeuralGCM, when blended with other advanced models like the European Centre for Medium-Range Weather Forecasts (ECMWF)’s Artificial Intelligence/Integrated Forecasting System (AIFS) and historical data, was the right tool for the job. It accurately predicted the onset of the Indian monsoon up to a month in advance, even capturing an unusual dry spell in the progression of the monsoon.

The image on the left shows the average of 120 years of historical data (e.g: what was expected). The image in the middle is what was observed by the India Meteorological Department. On the right is what the AI forecast predicted 15 days ahead of time.

Credit: The University of Chicago Institute for Climate and Growth’s Human-Centered Weather Forecasts Initiative.

![A three-panel map shows India's outline with color-coded rainfall data. The panels compare historical averages, a two-week dry spell in 2025, and a successful AI forecast of that dry spell.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/videoframe_4656.width-1200.format-webp.webp)

## Real-world impact — at scale

In partnership with the Indian Ministry of Agriculture and Farmers’ Welfare, this pioneering blend of AI models created by the University of Chicago successfully delivered tailored, advanced forecasts via SMS to 38 million farmers this summer. This initiative helped farmers proactively adjust their planting decisions — when to plant, whether to buy more seeds, switch to different crops or simply wait — allowing them to adapt to an unusually delayed monsoon season.

Existing [research](https://climate.uchicago.edu/impacts/providing-farmers-with-better-forecasts-helps-them-adapt-to-climate-change/) from the University of Chicago shows that by providing an accurate forecast around a month in advance, farmers can align their decisions with the coming weather and improve their outcomes. The study found that advance forecasts lead to an almost doubling of their annual income.

This project is a powerful example of how foundational AI technology, born from research, can serve real-world use cases, ultimately helping communities around the world build climate resilience.
