---
title: "Astera Labs IPO - The Next Connectivity Superhero or Steamrolled By Competition?"
subtitle: "Bottoms Up Model, Units, ASP, Revenue, By Hyperscaler Analysis, EPS & Cashflow, Competitive Analysis"
date: 2024-03-17
source: https://newsletter.semianalysis.com/p/astera-labs-ipo-the-next-connectivity
crawled: 2026-09-15
authors: ["Dylan Patel", "Jeremie Eliahou Ontiveros"]
tags: []
audience: only_paid
paywalled: true
---

# Astera Labs IPO - The Next Connectivity Superhero or Steamrolled By Competition?

**Bottoms Up Model, Units, ASP, Revenue, By Hyperscaler Analysis, EPS & Cashflow, Competitive Analysis**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

The gold rush for AI infrastructure is creating huge opportunities for the companies supplying enabling technologies. Not everyone is an Nvidia in this infrastructure build out bonanza, there are many small key players too. Today we’ll dive into Astera Labs, whose chips have been silently shipped in more than 80% of AI servers.

Astera Labs is a datacenter connectivity pure-play and targets mainly 3 customer types: hyperscalers, AI accelerator vendors, and system OEMs. Astera Lab’s product portfolio is currently comprised of 3 families: Aries retimers, Taurus active electrical cable (AEC) paddle board modules, and Leo CXL Memory Controllers. We have previously covered some of markets in which it operates, most notably [CXL](https://www.semianalysis.com/p/cxl-is-dead-in-the-ai-era) and [AECs](https://www.semianalysis.com/p/thick-cables-thin-margins-microsoft).

![](https://substack-post-media.s3.amazonaws.com/public/images/138b1bdd-6d05-4187-bca4-e020bb10ba11_2384x1044.png)
*Astera Labs*

Connectivity is historically an extremely competitive, but sticky high margin portion of the datacenter market. Despite numerous attempts at competition in switching and DSPs, Broadcom and Marvell have been able to dominate with more than 80% revenue share at >65% gross margins.

The top question everyone has been asking is if Astera Labs caught lightning in a bottle by being early, or if the the first movers advantage doesn’t matter and competitors will come in and steamroll them. We will discuss the main competitors in all major markets they operate in, including Marvell Technologies, Broadcom, Montage Technology, Parade Technologies, Rambus, Microchip, XConn, and Credo. Astera Labs could fade away, or they could become the next connectivity Superhero if they maintain high retimer market share and expand into AEC and various CXL products.

In this report, we will share forecasts for revenue, EPS, market size, etc. Our approach is built from the bottoms up with ASP and volumes for these markets based on per firm/types of [AI accelerator](https://www.semianalysis.com/p/accelerator-model) and CPU shipments. We take into account per hyperscaler wins/share for the connectivity products long term.

Before getting to that, let’s first review Astera Lab’s history.

## **How Astera Labs Is Solving The Connectivity Bottleneck**

Astera Labs was established in 2017 in a garage, in typical Silicon Valley fashion. The co-founders, Jitendra Mohan, Sanjay Gajendra, and Casey Morrison, were at Texas Instrument’s High Speed Interface business. They saw the world with increasing connectivity bottlenecks, due to the exponential growth in compute and the need for heterogenous computing driven by AI workloads and Hyperscale Cloud Computing.

> Astera Labs is in the business of removing bottlenecks, wherever they appear in a system
>
> Jitendra Mohan

The below image shows 3 major bottlenecks that Astera Labs aims to solve.

![](https://substack-post-media.s3.amazonaws.com/public/images/fb4929d4-f743-4d80-88ef-0befc10979d0_1200x611.png)
*Astera Labs*

The main focus for the company was initially PCIe and related protocols, such as CXL. PCIe 4.0 specs was released in 2017, and for the first time defined formally the terms “redriver” and “retimer”. A redriver is essentially an analog signal amplifier device, to counteract the frequency-dependent attenuation caused by the PCB.

In simple terms it boosts the signal, think a “megaphone”. The major disadvantage of a redriver is that it also amplifies noise that is in the signal path. This worked well enough for PCIe Gen 1 to Gen 3 but started causing challenges at Gen 4, with Gen 5’s faster data rates exacerbating this further. The image below shows the loss per inch across various PCIe generations and PCB materials.

![](https://substack-post-media.s3.amazonaws.com/public/images/1e1a140c-e0d3-4705-a0d0-9098101084ff_1722x654.png)
*Planet Analog*

To compensate for signal losses, the preferred option was to use higher quality PCB Materials, but this comes at a high cost. For example, the PCB material “Megtron 6” is about seven times the cost of the PCB material “FR4”, the most popular and cost-effective material.

Keep in mind that PCIe specifications have a precise insertion loss budget; in the case of PCIe 5.0, this is 36 dB bump-to-bump for 32 GT/s with a bit error rate less than 10^-12.

![](https://substack-post-media.s3.amazonaws.com/public/images/f204e8d2-0f0b-4a0c-ae48-19beffe19f74_2059x1137.png)
*Astera Labs*

Astera Labs was based on solving the connectivity challenges of PCIe 4 and 5 (specs out in 2019). They built a company around solving these signal integrity challenges and designing a retimer based solution. A retimer is a mixed-signal digital/analog device that is protocol-aware and can fully recover the data, extract the embedded clock and retransmit a fresh copy of the data using a clean clock.

In simple terms, instead of a “megaphone” like the redriver, this is a high quality microphone + dedicated audio equipment feeding the corrected signal to speakers to speakers. The retimer is a small chip performing PCIe SerDes functions as well as monitoring and data collection about the singal integrity. The below diagram illustrates a typical architecture.

![](https://substack-post-media.s3.amazonaws.com/public/images/6379a3ea-55fa-431f-8d58-28b7b8533c6f_787x440.png)
*PCI-SIG*

A retimer enables the signal to be split into two channels, significantly reducing the channel loss. The below diagram shows how these chips are integrated to PCBs. This also illustrates how low-loss PCBs, and even ultra-low-loss PCBs, may not be sufficient to have the required channel loss.

![](https://substack-post-media.s3.amazonaws.com/public/images/c0c6ff9c-8b36-41be-a596-41241404ac28_2400x1134.png)
*PCI-SIG*

Astera Labs was first to market with their Aries Smart Retimer for PCIe 4.0 as well as PCIe 5.0 and securing their first design wins in 2019. Volume production started in 2020, using a TSMC process and in 2021, the company generated revenue of $34.8M. They have a good set of investors such as Fidelity, Atreides Management, Intel Capital, and Sutter Hill Ventures. Their last round before this public offering was following a rejected acquisition offer from Marvell.

Astera has unveiled a vision to offer a global connectivity platform and launched two more product lines: the CXL Memory Controller, and the Smart Cable Module. The below diagram gives an illustration of Astera Lab’s vision.

![](https://substack-post-media.s3.amazonaws.com/public/images/209beb23-35a4-4df3-a2d0-398e409444ca_2496x754.png)
*Astera Labs*

In 2023 started on the wrong path, with weak and declining Q1 and Q2 dragged down by an inventory correction affecting the general purpose datacenter & networking markets, driven by the [cloud crisis of their largest hyperscaler customer](https://www.semianalysis.com/p/amazons-cloud-crisis-how-aws-will). But this was not the end of the story, with Q3 2023 and Q4 2024 showing explosive growth. So, what happened there, and is this sustainable?

![](https://substack-post-media.s3.amazonaws.com/public/images/6cfec880-2d61-43a0-84d2-82a78aae3059_938x541.png)
*Astera Labs Form S-1*

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

To answer this, let’s dive more into the Aries product family, and their main applications.

## **Aries Retimers for AI and Cloud applications**

The short answer is yes: as AI accelerator demand continues to fire, the PCIe retimer market will grow too. Indeed, inside each accelerator card is included a retimer. Additional retimers can be found in the server head node, as shown in the image below. The main customers here are AI accelerator vendors and server ODMs.

![](https://substack-post-media.s3.amazonaws.com/public/images/136f3a6d-f265-44e6-951c-e9c40aebd240_1630x1240.png)
*Astera Labs*

The reason retimers are so popular in accelerated computing systems is [Signal Reflection](https://resources.pcb.cadence.com/blog/2022-signal-reflection-and-distortion-in-pcbs). Alongside distance, this is the second major cause of signal loss in PCB traces or cables. To put it simply, GPU systems are very dense: the above image shows how a baseboard (for example the Nvidia HGX) can include 8 GPUs. Such density induces signal challenges and requires PCIe re-timers. AI servers can include retimers both on the Accelerator baseboard and on the attached Server Head Node. The precise number of units per GPU varies depending on various factors, such as PCB and design layout, and we’ll share our estimates later in the report for subscribers. Different hyperscalers designs contain different numbers of retimers.

Astera Labs’s first major customer was actually Amazon for “typical” (non-AI) cloud workloads. In some instances, Aries retimers can help Cloud Service Providers achieve lower TCO than alternatives for high data rates. The below image shows where retimer can be found within IT equipment.

![](https://substack-post-media.s3.amazonaws.com/public/images/c2580389-7924-4cdb-9f91-f6c8021cc719_1006x763.jpeg)
*ServeTheHome*

Another upcoming driver for Aries is CXL, a protocol built on top of PCIe. As explained in our [deep dive](https://www.semianalysis.com/p/cxl-deep-dive-future-of-composable), CXL adoption for Memory Pooling will lead to an increasing need for CXL switches, which will require then retimers. Of course we are not that bullish on that topic.

Now that we’ve covered the basics, the majority of this report will explore the strength of Astera Labs’ moat and dive into the other major product lines. We will cover growth, ASP, competition, gross margin and more. We will also share forecasts through 2027 from revenue down to free cash flow. We take into account Astera’s differing levels of penetration by platform and hyperscaler to model units for each product line for each hyperscaler.

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
