---
title: "Google Gemini Eats The World – Gemini Smashes GPT-4 By 5X, The GPU-Poors"
subtitle: "Compute Resources That Make Everyone Look GPU-Poor"
date: 2023-08-28
source: https://newsletter.semianalysis.com/p/google-gemini-eats-the-world-gemini
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
---

# Google Gemini Eats The World – Gemini Smashes GPT-4 By 5X, The GPU-Poors

**Compute Resources That Make Everyone Look GPU-Poor**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Before Covid, Google released the MEENA model, which for a short period of time, was the best large language model in the world. The [blog](https://ai.googleblog.com/2020/01/towards-conversational-agent-that-can.html) and [paper](https://arxiv.org/abs/2001.09977) Google wrote were incredibly cute, because it specifically compared against to OpenAI.

> Compared to an existing state-of-the-art generative model, OpenAI GPT-2, Meena has 1.7x greater model capacity and was trained on 8.5x more data.

This model required more than 14x the FLOPS of GPT-2 to train, but this was largely irrelevant because only a few months later OpenAI dropped GPT-3, which was >65x more parameters and >60x the token count, >4,000x more FLOPS. The performance difference between these two models was massive.

The MEENA model sparked an internal memo written by Noam Shazeer titled "MEENA Eats The World.” In this memo, he predicted many of the things that the rest of the world woke up to after the release of ChatGPT. The key takeaways were that language models would get increasingly integrated into our lives in a variety of ways, and that they would dominate the globally deployed FLOPS. Noam was so far ahead of his time when he wrote this, but it was mostly ignored or even laughed at by key decision makers.

Let’s go on a tangent about how far ahead of his time, Noam really was. He was part of the team that did the original Transformer paper, “[Attention is All You Need](https://arxiv.org/abs/1706.03762).” He also was part of the [first modern Mixture of Experts paper](https://arxiv.org/abs/1701.06538), [Switch Transformer](https://arxiv.org/abs/2101.03961), [Image Transformer](https://arxiv.org/abs/1802.05751), and various elements of [LaMDA](https://blog.google/technology/ai/lamda/) and [PaLM](https://ai.googleblog.com/2022/04/pathways-language-model-palm-scaling-to.html). [One of the ideas from 2018 he hasn’t yet gotten credit](https://arxiv.org/abs/1811.03115) for more broadly is [speculative decoding which we detailed here in our exclusive tell-all about GPT-4](https://www.semianalysis.com/i/134355860/speculative-decoding). Speculative decoding reduces the cost of low batch inference by multiple-fold.

The point here is Google had all the keys to the kingdom, but they fumbled the bag. A statement that is obvious to everyone.

The statement that may not be obvious is that the sleeping giant, Google has woken up, and they are iterating on a pace that will smash GPT-4 total pre-training FLOPS by 5x before the end of the year. The path is clear to 20x by the end of next year given their current infrastructure buildout. Whether Google has the stomach to put these models out publicly without neutering their creativity or their existing business model is a different discussion.

Today we want to discuss Google’s training systems for Gemini, the iteration velocity for Gemini models, Google’s Viperfish (TPUv5) ramp, Google’s competitiveness going forward versus the other frontier labs, and a crowd we are dubbing the GPU-Poor.

## The GPU-Rich

Access to compute is a bimodal distribution. There are a handful of firms with 20k+ A/H100 GPUs, and individual researchers can access 100s or 1,000s of GPUs for pet projects. The chief among these are researchers at OpenAI, Google, Anthropic, Inflection, X, and Meta, who will have the highest ratios of compute resources to researchers. A few of the firms above as well as **multiple Chinese firms** will 100k+ by the end of next year, although we are unsure of the ratio of researchers in China, only the GPU volumes.

One of the funniest trends we see in the Bay area is with top ML researchers bragging about how many GPUs they have or will have access to soon. In fact, this has become so pervasive over the last ~4 months that it’s become a measuring contest that is directly influencing where top researchers decide to go. Meta, who will have the 2nd most number of H100 GPUs in the world, is actively using it as a recruiting tactic.

## The GPU-Poor

Then there are a whole host of startups and open-source researchers who are struggling with far fewer GPUs. They are spending significant time and effort attempting to do things that simply don’t help, or frankly, matter. For example, many researchers are spending countless hours agonizing on fine-tuning models with GPUs that don’t have enough VRAM. This is an extremely counter-productive use of their skills and time.

These startups and open-source researchers are using larger LLMs to fine-tune smaller models for leaderboard style benchmarks with broken evaluation methods that give more emphasis to style rather than accuracy or usefulness. They are generally ignorant that pretraining datasets and IFT data need to be significantly larger/higher quality for smaller open models to improve in real workloads.

Yes, being efficient with GPUs is very important, but in many ways, that’s being ignored by the GPU-poors. They aren’t concerned with efficiency at scale, and their time isn’t being spent productively. What can be done commercially in their GPU-poor environment is mostly irrelevant to a world that will be flooded by [more than 3.5 million H100s by the end of next year](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and). For learning, experimenting, smaller weaker gaming GPUs are just fine.

The GPU poor are still mostly using [dense models](https://www.semianalysis.com/p/gpt-4-architecture-infrastructure) because that’s what Meta graciously dropped on their lap with the LLAMA series of models. Without ~~God’s~~ Zuck’s good grace, most open source projects would be even worse off. If they were actually concerned with efficiency, especially on the client side, they’d be running sparse model architectures like MoE, training on these larger datasets, and [implementing speculative decoding](https://www.semianalysis.com/i/134355860/speculative-decoding) like the Frontier LLM Labs (OpenAI, Anthropic, Google Deepmind).

The underdogs should be focusing on tradeoffs that improve model performance or token to token latency by upping compute and memory capacity requirements in favor of reduced memory bandwidth because that’s what the edge needs. They should be focused on efficient serving of multiple finetuned models on shared infrastructure without paying the horrendous cost penalties of small batch sizes. Instead, they continually are focused on memory capacity constraints or quantizing too far while covering their eyes about real quality decreases.

To take the rant on a slight tangent, in general, model evaluation is broken. While there is a lot of effort in the closed world to improve this, the land of open benchmarks is pointless and measures almost nothing useful. For some reason there is an unhealthy obsession over the leaderboard-ification of LLMs, and meming with silly names for useless models (WizardVicunaUncensoredXPlusPlatypus). Hopefully the open efforts are redirected towards evaluations, speculative decoding, MoE, open IFT data, and clean pre-training datasets with over 10 trillion tokens, otherwise, there is no way [for the open source to compete with commercial giants](https://www.semianalysis.com/p/google-we-have-no-moat-and-neither).

While the US and China will be able to keep racing ahead, the European startups and government backed supercomputers such as Jules Verne are also completely uncompetitive. Europe will fall behind in this race due to the lack of ability to make big investments and choosing to stay GPU-poor. Even multiple Middle Eastern countries are investing more on enabling large scale infrastructure for AI.

Being GPU-poor isn’t limited to only scrappy startups though. Some of the most well recognized AI firms, HuggingFace, Databricks (MosaicML), and Together are also part of this GPU-poor group. In fact, they may be the most GPU-poor groups out there with regard to both the number of world class researchers per GPU and the number of GPUs versus the ambition/potential customer demand. They have world class researchers, but all of them are limited by working on systems with orders of magnitude less capabilities. These firms have tremendous inbound from enterprises on training real models, and on the order of thousands of H100s coming in, but that won’t be enough to grab much of the market.

Nvidia is eating their lunch with multiple times as many GPUs in their DGX Cloud service and various in-house supercomputers. Nvidia’s DGX Cloud offers pretrained models, frameworks for data processing, vector databases and personalization, optimized inference engines, APIs, and support from NVIDIA experts to help enterprises tune models for their custom use cases. That service has also already racked up multiple larger enterprises from verticals such as SaaS, insurance, manufacturing, pharmaceuticals, productivity software, and automotive. While not all customers are announced, even the public list of Amgen, Adobe, CCC, ServiceNow, Accenture, AstraZeneca, Getty Images, Shutterstock, Morningstar, Evozyne, Insilico Medicine, Quantiphi, InstaDeep, Oxford Nanopore, Peptone, Relation Therapeutics, ALCHEMAB Therapeutics, and Runway is quite impressive.

This is a far longer list than the other players have, and Nvidia has many other undisclosed partnerships too. To be clear, revenue from these announced customers of Nvidia’s DGX cloud service is unknown, but given the size of Nvidia’s cloud spending and in-house supercomputer construction, it seems that more services can/will be purchased from Nvidia’s Cloud than HuggingFace, Together, and Databricks can hope to offer, combined.

The few hundred million that HuggingFace and Together have raised collectively means they will remain GPU-poor, getting left in the dust as they will be unable to train N-1 LLMs that can serve as the base to fine tune for customers. This means they will ultimately be unable to capture high share at enterprises who can just access Nvidia’s service today anyways.

HuggingFace in particular has one the biggest names in the industry, and they need to leverage that to invest a huge amount and build a lot more model, customization, and inference capabilities. Their recent round was done at too high of a valuation to garner the investment they need to compete. HuggingFace’s leaderboards show how truly blind they are because they actively hurting the open source movement by tricking it into creating a bunch of models that are useless for real usage.

Databricks (MosaicML) could at least maybe catch up, due to their data and enterprise connections. The issue is they need to accelerate spend by multiple times if they want to have hopes of serving their over 7,000 customers. The $1.3B acquisition of MosaicML was a big bet on this vertical, but they also need to throw a similar amount of money at infrastructure. Unfortunately for Databricks, they can’t pay for GPUs in shares. They need to do a large offering via their upcoming private round/IPO, and use that cold hard cash to quadruple down on hardware.

The economic argument falls flat on its face because they must build before customers can come, because Nvidia is throwing money at their service. To be clear, many folks are buying loads of compute not making their money back, (Cohere, Saudi Arabia, UAE), but it is a pre-requisite to compete.

The picks and shovels training and inference ops firms (Databricks, HuggingFace, and Together) are behind their chief competition, who also happens to also be the source of almost all of their compute. The next largest operator of customized models is simply the fine tuning APIs from OpenAI.

The key here is everyone from Meta to Microsoft to startups are simply serving as a pipeline of capital to Nvidia’s bank account.

Can anyone save us from Nvidia slavery?

Yes, there is one potential savior.

## Google – The Most Compute Rich Firm In The World

While Google does use GPUs internally as well as a significant number sold via GCP, they a have a few Ace’s up their sleeve. These include Gemini and the next iteration which has already begun training. The most important advantage they have is their unbeatably efficient infrastructure.

Before getting into Gemini and their cloud business, we will share some datapoints on their insane buildout. The chart below shows the total advanced chips added by quarter. Here we give OpenAI every benefit of the doubt. That the number of total GPUs they have will 4x over 2 years. For Google, we ignore their entire existing fleet of TPUv4 (Pufferfish), TPUv4 lite, and internally used GPUs. Furthermore, we are also not including the TPUv5e (lite), despite that likely being the workhorse for inference of smaller language models. Google’s growth in this chart is only TPUv5 (Viperfish).

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
