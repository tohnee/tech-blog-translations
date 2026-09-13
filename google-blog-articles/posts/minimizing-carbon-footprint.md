---
title: "How we’re minimizing AI’s carbon footprint"
source: https://blog.google/innovation-and-ai/technology/ai/minimizing-carbon-footprint/
site: google-blog
date: 2021-04-22
authors: David Patterson
crawled: 2026-09-13
---

The book that led to my visit to Google.

![A photograph of a textbook about computer architecture.](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/image4_PgpO6NB.width-100.format-webp.webp)

When I first visited Google back in 2002, I was a computer science professor at UC Berkeley. My colleague John Hennessey and I were updating our textbook on computer architecture, and Larry Page — who rode a hot-rodded electric scooter at the time — agreed to show me how his then three-year-old company designed its computing for Search. I remember the setup was lean yet powerful: just 6,000 low-cost PC servers and 12,000 PC disks answering 70 million queries around the world, every day. It was my first real look at how Google built its computer systems from the ground up, optimizing for efficiency at every level.

When I joined the company in 2016, it was with the goal of helping research how to maximize the efficiency of computer systems built specifically for artificial intelligence. Last year, Google set an ambitious goal of operating on 24/7 carbon-free energy, everywhere, by the end of the decade. But at the same time, machine learning systems are quickly becoming larger and more capable. What will be the environmental impact of those systems — and how can we neutralize that impact going forward? 

Today, we’re publishing a [detailed analysis](https://arxiv.org/abs/2104.10350) that addresses both of those questions. It’s an account of the energy- and carbon-costs of training six state-of-the art ML models, including five of our own. (Training a model is like building infrastructure: You spend the energy to train the model once, after which it’s used and reused many times, possibly by hundreds of millions of people.) To our knowledge, it’s the most thorough evaluation of its kind yet published. And while we had reason to believe our systems were efficient, we were encouraged by just how efficient they turned out to be.

For instance, we found that developing the Evolved Transformer model, a more efficient version of the popular Transformer architecture for ML, emitted nearly 100 times less [carbon dioxide equivalent](https://www3.epa.gov/carbon-footprint-calculator/tool/definitions/co2e.html) than a widely cited estimate. Of the roughly 12.7 terawatt-hours of electricity that [Google uses every year](https://sustainability.google/reports/), less than 1/200th of a percent of it was spent training our most computationally demanding models.

What’s more, our analysis found that there already exist many ways to develop and train ML systems even more efficiently: Specially designed models, processors and data centers can dramatically reduce energy requirements, while the right selection of energy sources can go a long way to reduce the carbon that’s emitted during training. In fact, the right combination of model, processor, data center and energy source can reduce the carbon footprint of training an ML system by 1000 times.

There’s no one easy trick for achieving a reduction that large, so let’s unpack that figure.  Minimizing a system’s carbon footprint is a two-part problem: First you want to minimize the energy the system consumes, then you have to supply that energy from the cleanest source possible.

Our analysis took a closer look at GShard and Switch Transformer, two models recently developed at Google Research. They’re the largest models we’ve ever created, but they both use a technique called sparse activation that enables them to only use a small fraction of their total architecture for a given task. It’s a bit like how your brain uses a small fraction of its 100 billion neurons to help you read this sentence. The result is that these sparse models consume less than one tenth the energy that you’d expect of similarly sized dense models — without sacrificing accuracy.

But to minimize ML’s energy use, you need more than just efficient models — you also need efficient processors and data centers to train and serve them. Google’s Tensor Processing Units (TPUs) are specifically designed for machine learning, which makes them up to five times more efficient than off-the-shelf processors. And the cloud computing data centers that house those TPUs are up to twice as efficient as typical enterprise data centers.

Once you’ve minimized your energy requirements, you have to think about where that energy originates. The electricity a data center consumes is determined by the grid where it’s located. And depending on what resources were used to generate the electricity on that grid, this may emit carbon.

The carbon intensity of grids varies greatly across regions, so it really matters where models are trained. For instance, the mix of energy supplying Google’s Iowa data center produces 0.080kg of CO2e per kilowatt hour of electricity, when combining the electricity supplied by the grid and produced by Google’s wind farms in Iowa. That’s 5.4 times less than the U.S. average. 

Any one of these four factors — models, chips, data centers and energy sources — can have a sizable effect on the costs associated with developing an ML system. But their cumulative impact can be enormous.

When John and I updated our textbook with what we’d learned on our visit to Google back in 2002, we wrote that “reducing the power per PC [server]” presented “a major opportunity for the future.” Nearly 20 years later, Google has found many opportunities to streamline its systems — but plenty remain to be seized. As a result of our analysis, we’ve already begun shifting where we train our computationally intensive ML models. We’re optimizing data center efficiency by [shifting compute tasks](https://blog.google/inside-google/infrastructure/data-centers-work-harder-sun-shines-wind-blows/) to times when low-carbon power sources are most plentiful. Our Oklahoma data center, in addition to receiving its energy from cleaner sources, will house many of our next generation of TPUs, which are even more efficient than their predecessors. And sparse activation is just one example of the algorithmic ingenuity Google is using to design ML models that work smarter, not harder.
