---
title: "Nvidia's Optical Ascent: >$1B Revenue; The Missing 800G Ramp; AI Head-Fakes"
subtitle: "1 Supplier Is A Winner Take All, Revealing The AI Head-Fakes"
date: 2023-08-23
source: https://newsletter.semianalysis.com/p/nvidias-optical-ascent-1b-revenue
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
---

# Nvidia's Optical Ascent: >$1B Revenue; The Missing 800G Ramp; AI Head-Fakes

**1 Supplier Is A Winner Take All, Revealing The AI Head-Fakes**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

The performance of the network connecting your GPUs together is often the gating factor for performance and as such, it is the [highest cost](https://www.semianalysis.com/p/nvidias-infiniband-problem-qmx-ai) aspect of the AI buildout after the accelerators themselves. Nvidia is attempting to [wield the allocation of GPUs as a sword to push more networking content](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will). While Nvidia and Broadcom are fighting over the [high-margin socket of network switches](https://www.semianalysis.com/p/nvidias-infiniband-problem-qmx-ai), Nvidia is also pushing their own optical transceivers that connect to their InfiniBand, Ethernet, and NVLink networks. Due to their bundling, Nvidia will sell over $1B of optics over the next 12 months.

Today we want to walk through the ramp-up of the external NVLink network, 800G optical transceivers for switches, and the biggest beneficiary of Nvidia’s ramp. We will start with an overview of technological changes before covering the business.

![](https://substack-post-media.s3.amazonaws.com/public/images/20f40c6e-1a57-470b-9c6e-dba630d641ab_953x534.png)

There are huge bottlenecks in AI. Last year we covered Meta’s analysis of the coming problems to AI hardware and optics. We also noted that [Nvidia was playing a completely different game](https://www.semianalysis.com/p/meta-discusses-ai-hardware-and-co) versus everyone else.

This is because of their NVLink scale-up network. All other merchant silicon accelerators cannot scale up to bandwidth levels this high between accelerators. High bandwidth is incredibly important for training, but [potentially more important for inference, based on GPT-4’s architecture.](https://www.semianalysis.com/p/gpt-4-architecture-infrastructure)

While most 8x H100 deployments have a total of 400GB/s (3.2T) of network bandwidth, Nvidia has developed a special version with scale-up NVLink network. NVLink scale-up has 3.2TB/s of bandwidth by comparison. There is potential for as high as 1,152 800G optical transceivers per H100 Superpod, connecting the 32 GPU nodes and 18 switch nodes all to all. While this is important, 800G will be higher volume in Ethernet and InfiniBand, and Nvidia is bundling there too.

![](https://substack-post-media.s3.amazonaws.com/public/images/888a2891-039b-4cec-a975-5f6d0acbe3ef_866x307.png)

Across networking, there are multiple segments where people claim to be winners, because of 400G and 800G ramps, but [really many are AI head-fakes](https://www.semianalysis.com/p/nvidias-ramp-volume-asp-cloud-pricing). For example, there are [a few firms claiming victory in active electric and copper cables (AEC & ACC)](https://www.semianalysis.com/p/thick-cables-thin-margins-microsoft), but really by early next year, it is a 9-way knife fight where margins are collapsing. Nowhere have there been [more AI head-fakes](https://www.semianalysis.com/p/nvidias-ramp-volume-asp-cloud-pricing) than the optical transceiver market.

There are multiple components for this supply chain, from lasers, DSPs, TiAs, drivers, transmit/receive optics, to the general assembly of optical transceivers. Of these there are 3 primary highest cost elements are the DSPs, laser, and assembly/module manufacturing.

The [DSP is mainly dominated by Marvell](https://www.semianalysis.com/i/107160162/the-war-on-marvell), although [Broadcom is gaining a bit of share](https://www.semianalysis.com/i/107160162/the-war-on-marvell), and there are also [linear direct drive optics coming which remove the DSP](https://www.semianalysis.com/i/107160162/the-war-on-marvell), starting to bleed in next year. This segment is generally very strong, but tremendous weakness in Marvell’s other businesses such as storage and telecom carrier infrastructure could mask some of the positives over the near term.

*We will be hosting [AI and Semiconductor Symposium in Taiwan](https://www.eventbrite.com/e/ai-and-semiconductor-symposium-tickets-692838296997) with on September 3rd with many foundry, packaging, ODM suppliers, and buyside in attendance. Topics covered include the future of AI infrastructure, the next-generation model architectures employed by Google’s Gemini/Future OpenAI GPT, Chinese analog/power semi fab buildouts, and Nvidia’s current acquisition target. Speakers include multiple members of SemiAnalysis, [FabricatedKnowledge](https://www.fabricatedknowledge.com/), [Asianometry](https://www.asianometry.com/), [Alethia Capital](https://www.aletheia-capital.com/), and the CEO and Chairman of Andes, the highest volume RISC-V based firm in the world with over 1 billion cores shipped a year. [Register here](https://www.eventbrite.com/e/ai-and-semiconductor-symposium-tickets-692838296997) if you can come!*

The laser segment is one that has generally been highly profitable for the leaders, but has been weakening in recent years. While there are many different types of lasers, External Modulation Laser (EML) and Vertical-Cavity Surface-Emitting Laser (VCSEL) are the primary types. VCSELs are used in shorter range optics, with the main advantages being that they are lower power and cheaper. On the flipside, there are EML lasers which have much higher range, but higher power. 800G is primarily an EML market initially, but VCSELs should take over for the bulk of volume next year.

Lumentum, the largest laser manufacturer in the world was one such AI-headfake. Many were chasing optics module components, and Lumentem was near the top of the list. Though the company did well in the current quarter, guidance for the next quarter came in well below expectations at a $300M to $325M vs bank estimates of $366.8M. The company confirmed a sequential decline in Telecom and Datacom revenue into their next quarter, primarily due to telecom.

However, there is some silver lining. The company believes that:

> Telecom and Datacom revenue will be up in calendar ’24 compared to calendar ’23.
>
> We expect to start ramping shipments of 200-gig EML products in calendar ‘24, and customer qualifications of 800G and 1.6-terabit transceiver designs are well underway.

200G per lane is still a bit aways and isn’t expected to ship at any reasonable volume only starting at the tail end of 2024, probably alongside Nvidia’s next generation GPU and NVSwitch.

![](https://substack-post-media.s3.amazonaws.com/public/images/4b247aab-d7d2-4df6-8790-84b2cf07dbf6_1138x636.png)

While Lumentem is maintaining good share in optics modules from our checks, Lumentum’s datacom business is a chip business – which means much lower ASPs versus completed transceiver and thus less total revenue. Furthermore, 100G per lane EMLs are quite commoditized, currently with many firms making them. This makes it hard for the inflection to move the needle as meaningfully. Lastly, as 400G and 800G VCSEL based solutions ramp, laser content per optical transceiver will continue to fall.

The AI ramp is happening now in terms of GPUs and networking, but for Lumentum they don’t appear to have a major ramp in the 2023 calendar year, and as such, they are an AI head-fake.

The third high value segment is manufacturing the transceivers themselves. Coherent, is probably the biggest AI-head fake in this market. They are the largest player in the space and a vertically integrated debt-laden monster. They make both the laser and the module. They have been claiming AI is a huge driver of business, but when their results are inspected, the business isn’t there.

![](https://substack-post-media.s3.amazonaws.com/public/images/66ca7f35-7ca7-400f-9d9b-13d5fa334106_1267x701.png)

Guidance was well below expectations due to a soft telecom market and a lack of any meaningful datacom ramp. Furthermore, their competitive position isn’t as strong as it has been historically and will continue to weaken going forward to 800G. They even dropped this oddball statement recently.

> Not included in full year FY24 revenue guidance is several hundred million dollars of additional revenue related to the recent surge in demand for Datacom transceivers for AI driven data center buildouts as the supply chain ramps incremental capacity to address industry demand.

[Doug at Fabricated Knowledge](https://www.fabricatedknowledge.com/p/earnings-mchp-and-ifx-simo-rumors) had the [best question regarding this oddity](https://www.fabricatedknowledge.com/p/earnings-mchp-and-ifx-simo-rumors).

> If it’s real revenue, why not include it? Because they don’t think they can hit the ramp?

Check out [his full analysis on that and many other earnings here](https://www.fabricatedknowledge.com/p/earnings-mchp-and-ifx-simo-rumors).

Cisco is also the largest networking company on the planet and was surprisingly not an AI Head-fake. Mostly this is because no one thought they were a winner, but they seem to actually be getting a bit of share.

> To date, we have taken orders for over $0.5 billion for AI Ethernet fabrics. We are also piloting 800 gig capabilities for AI training fabrics. On the 800 gig, I think it's just a matter of we're engaged there. We're installed already. We've got trust with these customers.

While we won’t call them a winner, they seem to be indexing fairly, even winning a significant chunk of business that we assumed Broadcom and Nvidia would eat.

China’s Zhongji Innolight (Innolight) is another optical transceiver company that has been pitched as a major winner from the AI build out as it is believed to have strong market share in 800G transceivers. This is heavily embedded with the stock up 350% YTD – expectations are sky high. We will see how Innolight delivers on these expectations when it releases earnings on Aug 27th. Consensus estimates call for a 21% revenue growth in the fiscal year Ending December 2023, and a 54% growth in revenue in the fiscal year ending December 2024.

While our checks indicate that they are a winner at multiple hyperscalers, the volumes of >10 million that some in China are preaching are likely too high. We chalk it up to [supply chain intoxication.](https://www.semianalysis.com/i/136248981/nvidia-supply-chain-intoxication)

While they are a winner, their ramp of 800G isn’t as soon as the firm we discuss below. Next year as hyperscalers ramp their in-house purchases, Innolight’s business will ramp.

The 800G ramp in the latter part of this year is being driven by Nvidia. They chose a different supplier.

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
