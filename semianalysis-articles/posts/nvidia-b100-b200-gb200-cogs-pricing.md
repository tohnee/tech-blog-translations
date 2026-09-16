---
title: "Nvidia B100, B200, GB200 - COGS, Pricing, Margins, Ramp - Oberon, Umbriel, Miranda"
subtitle: "The B Stands For Jensen's Benevolence"
date: 2024-03-18
source: https://newsletter.semianalysis.com/p/nvidia-b100-b200-gb200-cogs-pricing
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie", "Chaolien Tseng"]
tags: []
audience: only_paid
paywalled: true
---

# Nvidia B100, B200, GB200 - COGS, Pricing, Margins, Ramp - Oberon, Umbriel, Miranda

**The B Stands For Jensen's Benevolence**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Nvidia announced their new generation of Blackwell GPUs at GTC. We eagerly await the full architecture white paper to be released to detail the the much needed improvements to the tensor memory accelerator and exact [implementation of new MX number formats, discussed here.](https://www.semianalysis.com/p/neural-network-quantization-and-number)

We discussed many of the high level features of the architecture such as process node, package design, HBM capacity, SerDes speeds, [here](https://www.semianalysis.com/p/nvidias-plans-to-crush-competition), but let’s dive a bit deeper into the systems, ramp, pricing, margins, and Jensen’s Benevolence.

Nvidia is on top of the world. They have supreme pricing power right now, [despite hyperscaler silicon ramping](https://www.semianalysis.com/p/accelerator-model). Everyone simply has to take what Nvidia is feeding them with a silver spoon. The number one example of this is with the H100, which has a gross margin exceeding 85%. The advantage in performance and TCO continues to hold true because the B100 curb stomps the MI300X, Gaudi 3, and internal hyperscaler chips ([besides the Google TPU](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy)).

For subscribers will be the ramp, pricing, and the new B100, B200, and GB200. The pricing will come as a surprise to many, and as such we like to say the B stands for **Benevolence,** not Blackwell, because the graciousness of our lord and savior Jensen Huang is smiling upon the world, particularly the [GPU-poor](https://www.semianalysis.com/p/google-gemini-eats-the-world-gemini).

## **B100 / B200 Configuration**

[As previously discussed](https://www.semianalysis.com/p/nvidias-plans-to-crush-competition), Blackwell has 2 reticle-sized GPU dies. The GPU compute dies will remain on 4nm like Hopper, so the first time Nvidia is not opting for a node transition for their datacenter GPUs. This is quite noteworthy as Nvidia has shipped roughly ~800mm2+ for the V100, A100, and H100. Now instead of being able to shrink process nodes for a larger transistor budget, they have to double the amount of silicon. This is [due to issues with TSMC’s original 3nm, N3B](https://www.semianalysis.com/p/tsmcs-3nm-conundrum-does-it-even).

In addition, there is up to 8 stacks of 8-hi HBM3E with *up to* 192GB capacity. Both SK Hynix and Micron are suppliers with the vast majority being SK Hynix. This is a change from [SK Hynix being the sole supplier for the H100 ramp](https://www.semianalysis.com/p/ai-server-cost-analysis-memory-is). Samsung continues to be the laggard despite [their announcements](https://news.samsung.com/global/samsung-develops-industry-first-36gb-hbm3e-12h-dram) of developing “the world’s fastest” HBM3E. Samsung loves press releases, but they are currently facing major challenges in qualifications.

The trend in GPU roadmaps is more silicon (for both logic and memory) in a bigger package and silicon-based interposers are hitting their limit in terms of size. The increased size makes silicon much harder to handle which kills yields. The B100 package is much larger, and as such it will be the first major high volume product utilizing [CoWoS-L](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and). CoWoS-L is an organic RDL substrate with passive silicon bridges.

The first version of Blackwell, B100, codename Umbriel, is for time to market, it keeps PCIe Gen 5, 400G networking, etc. In fact, the B100 air-cooled 700W can even slide into existing servers that accept the H100 and H200 baseboards with nearly no modifications. Despite this NVLink speeds inside the box are doubled.

The B200 will follow shortly after, with a higher power limit of 1,000W. This version requires a redesign of servers. Based on checks from our newest analyst in Taiwan, Chaolien, the 1,000W version can still be air-cooled, which will come as a surprise to many. Both these keep PCIe Gen 5 and 3.2T networking per server

For the standard GPU only product, Miranda comes after Umbriel. Miranda has PCIe Gen 6 and up to 800G networking enabled, with 6.4T per server. It has up to 192GB on the roadmap. However, Nvidia has already bought up all the supply of 36GB HBM which SK Hynix and Micron are ramping early next year. This means that there can be a refresh that actually goes up to 288GB per GPU.

[Share](https://newsletter.semianalysis.com/p/nvidia-b100-b200-gb200-cogs-pricing?utm_source=substack&utm_medium=email&utm_content=share&action=share)

The product everyone in the supply chain is buzzing for is the Oberon GB200 platform. We will discuss that pricing, COGS, margins, ramp, and Jensen’s Benevolence for subscribers.

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
