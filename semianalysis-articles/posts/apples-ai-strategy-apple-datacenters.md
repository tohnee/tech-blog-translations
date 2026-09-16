---
title: "Apple’s AI Strategy: Apple Datacenters, On-device, Cloud, And More"
subtitle: "When to run on-device, in Apple datacenters, or in the cloud with OpenAI, Deal economics"
date: 2024-05-27
source: https://newsletter.semianalysis.com/p/apples-ai-strategy-apple-datacenters
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie"]
tags: []
audience: only_paid
paywalled: true
---

# Apple’s AI Strategy: Apple Datacenters, On-device, Cloud, And More

**When to run on-device, in Apple datacenters, or in the cloud with OpenAI, Deal economics**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Nvidia continues to ramp their production to service the world’s insatiable demand for GPUs, and yet, our [Accelerator Model’s extensive checks](https://www.semianalysis.com/p/accelerator-model) show [Apple’s purchases of GPUs are quite miniscule](https://www.semianalysis.com/p/accelerator-model). In fact, they aren’t even a top 10 customer. Furthermore, while all eyes are on WWDC, Apple’s only announcing AI there, not shipping. The question on everyone’s mind is… what the heck is Apple doing inAI?

[Mark Gurman](https://www.bloomberg.com/news/newsletters/2024-05-26/apple-ios-18-macos-15-ai-features-project-greymatter-privacy-openai-deal-lwni63s3) laid out the features Apple is announcing at WWDC. Furthermore there’s a variety of rumors floating around from others, so let’s get to the bottom of what’s really happening, how, and what Apple can do.

The first thing is that multiple sources have reported that Apple is ramping up production of its M-series processors this year [to record volumes](https://www.semianalysis.com/p/accelerator-model). This is primarily Apple’s M2 Ultra SKUs which is 2 M2 Max SoCs stitched together with what Apple calls “UltraFusion.” Note that Apple’s M3 Ultra was cancelled.

![](https://substack-post-media.s3.amazonaws.com/public/images/16fc78ce-9823-4418-a73c-2096d0c1b5b3_1010x700.jpeg)
*Source: Apple*

Ultrafusion is Apple’s marketing name for using a local silicon interconnect (bridge die) to connect the two M2 Max chips in a package. The two chips are exposed as a single chip to many layers of software. M2 Ultra utilizes [TSMC’s InFO-LSI packaging technology](https://www.semianalysis.com/p/advanced-packaging-part-1-pad-limited). This is a similar concept as TSMC’s CoWoS-L that is being adopted by Nvidia’s Blackwell and future accelerators down the road to make large chips. The only major difference between Apple and Nvidia’s approaches are that InFO is chip-first vs CoWoS-L is chip-last process flow, and that they are using different types of memory.

![](https://substack-post-media.s3.amazonaws.com/public/images/1f352fc1-a4f7-49ab-bb63-5cc969897c61_1858x628.png)
*Source: Nvidia*

What’s curious about Apple’s production increases is that there is nothing on the demand front to support a sudden increase in M2 Ultra shipments. M2 Ultra is only used in high-end Mac Studio and Mac Pro products. There has been no meaningful refresh of these products in a year, and there are no plans for one any time soon. Furthermore, no new products are shipping with it either.

High end desktop PCs and Macs remains quite sluggish compared to the peak covid demand, yet 2024 production of the chips that would purportedly power these high end Macs is going to be significantly higher than the last few years even though there is nothing to suggest there will be consumer demand to soak up all these units.

How do we reconcile this?

## **Apple’s Own AI Servers**

This additional production of the M2 Ultras is consistent with recent reporting out from the [WSJ](https://www.wsj.com/tech/ai/apple-is-developing-ai-chips-for-data-centers-seeking-edge-in-arms-race-0bedd2b2) and [Bloomberg](https://www.bloomberg.com/news/articles/2024-05-09/apple-to-power-ios-18-ai-features-with-in-house-server-mac-chips-this-year) about Apple using their own silicon in their own Datacenters for serving AI to Apple users.

Furthermore, Apple has extensive expansion plans for their own datacenter infrastructure. We are tracking [7 different datacenter sites with over 30 buildings for Apple](https://www.semianalysis.com/p/datacenter-model) as well as their planned buildout. Their total capacity is doubling in a relatively short period of time.

![](https://substack-post-media.s3.amazonaws.com/public/images/1b0f1de1-a7a0-4001-a0c7-7bea0f45d829_2048x1487.jpeg)
*Source: SemiAnalysis Datacenter Model*

Above is Apple’s soon to be largest datacenter site. Currently they only have 1 datacenter there, but many will be coming up next year. Our [datacenter model](https://www.semianalysis.com/p/datacenter-model) has more details on the upcoming Apple datacenters.

## **Apple’s Infrastructure Team**

The other indication that Cupertino is serious about their AI hardware and infrastructure strategy is they made a number of major hires a few months ago. This includes Sumit Gupta who joined to lead cloud infrastructure at Apple in March. He’s an impressive hire. He was at Nvidia from 2007 to 2015, and involved in the beginning of Nvidia's foray into accelerated computing. After working on AI at IBM, he then joined Google’s AI infrastructure team in 2021 and eventually was the product manager for all Google infrastructure including the Google TPU and Arm based datacenter CPUs.

He’s been heavily involved in AI hardware at Nvidia and Google who are both the best in the business and are the only companies that are deploying AI infrastructure at scale today. This is the perfect hire.

Given this context, let’s look at what Apple is doing with their current and future in-house chips and external chips. We will look into Apple’s grudge with Nvidia. We will also discuss what Apple can run on-device, in cloud, and when they have to go to external service provider based AI. The economics around the deal differ from the $20B Google search deal, but not in the way you’d think. We will also discuss how Apple can offer this to customers and grow revenue.

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
