---
title: "AMD MI300 Ramp, GPT-4 Performance, ASP & Volumes"
subtitle: "Order Volumes From Microsoft, Meta, Oracle, Google, Supermicro/Quanta direct, Amazon"
date: 2023-11-01
source: https://newsletter.semianalysis.com/p/amd-mi300-ramp-gpt-4-performance
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie"]
tags: []
audience: only_paid
paywalled: true
---

# AMD MI300 Ramp, GPT-4 Performance, ASP & Volumes

**Order Volumes From Microsoft, Meta, Oracle, Google, Supermicro/Quanta direct, Amazon**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

AMD’s upcoming MI300 is poised as the only legitimate competitor to Nvidia and Google hardware in LLM inference. Groq, SambaNova, Intel, Amazon, Microsoft Athena, etc still do not compete. To enable this AMD has been investing heavily into their own RoCM software, the PyTorch ecosystem, and OpenAI’s Triton.

In the above we wrote about the software issues and how they were being solved as well as MI300’s primary customers, advantages, and use cases (LLM Inference) in January. This has started to come to true with firms like [Databricks](https://www.databricks.com/blog/training-llms-scale-amd-mi250-gpus), [AI21](https://blog.allenai.org/announcing-ai2-olmo-an-open-language-model-made-by-scientists-for-scientists-ab761e4e9b76), [Lamini](https://www.lamini.ai/blog/lamini-amd-paving-the-road-to-gpu-rich-enterprise-llms), [Moreph, and Korea Telecom (KT)](https://moreh.io/blog/training-221b-parameter-korean-llm-on-1200-amd-mi250-gpu-cluster-230814) using AMD GPUs for inference/training.

We detailed the MI300 architecture in June, where we reiterated those above points and dove much deeper into cost, networking, and the various configurations. Today we also want to note GPT-4 performance for MI300.

Companies such as Microsoft, Meta, Oracle, Google, Supermicro/Quanta direct, Amazon and more have already placed varying amounts of orders for MI300. We will detail the volumes, gross margins, and average price for these below, but first let’s talk about what AMD officially says.

> Based on the rapid progress we are making with our AI road map execution and purchase commitments from cloud customers, we now expect Datacenter GPU revenue to be approximately $400 million in the fourth quarter and exceed $2 billion in 2024 as revenue ramps throughout the year. This growth would make MI300 the fastest product to ramp to $1 billion in sales in AMD history. I look forward to sharing more details on our progress at our December AI event.
>
> Lisa Su, AMD CEO

Note she is actually sandbagging MI300 here by only saying >$2 billion. We will share our numbers below, but note there is supreme visibility due to AMD MI300’s complicated supply chain, it takes ~7 months for AMD to actually have a MI300X 8 GPU Baseboard to ship from the moment TSMC starts working on the wafers.

Positing away from AMD’s current <0.1% market share in LLM training and inference, AMD continues to gain market share steadily in datacenter. That will continue through next year with Turin and Turin-Dense launching in the middle of next year.

There are two angles to go at to arrive at AMD’s revenue from MI300 next year. These are how much supply AMD can secure, and how much major customers will order.

On the supply side, our AI Accelerator model accounts for HBM volumes by memory manufacturer, CoWoS volumes, packaging yields, and more for every accelerator that is produced using CoWoS including those for Nvidia, AMD, Google/Broadcom, Meta/Broadcom, Intel/AlChip, Amazon/AlChip, Amazon/Marvell, Microsoft/GUC, and more.

We have updated this regularly for client, but this gives us a total units that AMD can ship by quarter. Note there is a lag on TSMC N5/N6 wafer production, SoIC reconstituted wafer production, CoWoS wafer production, GPU package shipment, testing, and 8-GPU baseboard production. The orders were placed quite some time ago in order to achieve the volumes we will discuss below, especially due to supply constraints on HBM and CoWoS.

The other side is that of customers. Microsoft, Meta, Oracle, Google, Supermicro/Quanta direct, and Amazon are the primary vectors of orders, but there are also some orders from other parts of the supply chain as well including some for the MI300A in HPC style applications. Meshing these together, we get to the picture of AMD being supply constrained until Q3, then being oversupplied in Q4. Our demand side modelling accounts for the Nvidia B100 accelerated timing.

Now onto the numbers including volumes, gross margins, and ASPs. We will also discuss MI350X and MI400 briefly.

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
