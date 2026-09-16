---
title: "Huawei AI CloudMatrix 384 – China's Answer to Nvidia GB200 NVL72"
subtitle: "China Abundance of Power, 100% Optics, 0% Copper, Power Inefficiency, 2.6x lower FLOP per Watt, 14 Transceivers per Chip, Linear Pluggable Optics"
date: 2025-04-16
source: https://newsletter.semianalysis.com/p/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball", "Myron Xie", "Patrick Zhou", "Ivan Chiam", "AJ", "Christopher Seifel", "Doug"]
tags: ["Hardware Architecture", "Accelerators", "Export Controls"]
audience: only_paid
paywalled: true
---

# Huawei AI CloudMatrix 384 – China's Answer to Nvidia GB200 NVL72

**China Abundance of Power, 100% Optics, 0% Copper, Power Inefficiency, 2.6x lower FLOP per Watt, 14 Transceivers per Chip, Linear Pluggable Optics**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Huawei is making waves with its new AI accelerator and rack scale architecture. Meet China’s newest and most powerful Chinese domestic solution, the CloudMatrix 384 built using the Ascend 910C. This solution competes directly with the GB200 NVL72, and in some metrics is more advanced than Nvidia’s rack scale solution. The engineering advantage is at the system level, not just at the chip level, with innovation at the networking, optics, and software layers.

![](https://substack-post-media.s3.amazonaws.com/public/images/c395d1e6-7a89-4eb5-b54d-10a13df2347e_1080x524.png)
*Source: Huawei*

The Huawei Ascend chip is not new to SemiAnalysis, but in a [world where systems matter more than microarchitecture](https://semianalysis.com/2023/04/12/google-ai-infrastructure-supremacy/), Huawei is pushing the limits of AI system performance. There are trade-offs, but given export controls and lackluster domestic yields, it’s clear that there are further loopholes in the Chinese export controls.

While the Ascend chip *can be* fabricated at SMIC, we note that this is a global chip that has [HBM from Korea](https://www.semianalysis.com/p/accelerator-model), [primary wafer production from TSMC](https://semianalysis.com/accelerator-industry-model/), and is fabricated by [10s of billions of wafer fabrication equipment from the US, Netherlands, and Japan](https://semianalysis.com/wafer-fab-model/). We do a deep dive into what is possible for domestic Chinese production what is an aggressive skirting of the export controls, and why the US government needs to focus on these key new areas to limit China’s AI capabilities.

Huawei is a generation behind in chips, but its scale-up solution is arguably a generation ahead of Nvidia and AMD’s current products on the market. So what would be the specifications for Huawei’s CloudMatrix 384 (CM384)?

The CloudMatrix 384 consists of 384 Ascend 910C chips connected through an all-to-all topology. The tradeoff is simple: having five times as many Ascends more than offsets each GPU being only one-third the performance of an Nvidia Blackwell.

![](https://substack-post-media.s3.amazonaws.com/public/images/ec70db4a-8695-4864-a756-e740da2fece7_794x528.png)
*Source: SemiAnalysis, Nvidia, Huawei*

A full CloudMatrix system can now deliver **300 PFLOPs of dense BF16 compute, almost double that of the GB200 NVL72**. With more than **3.6x aggregate memory capacity** and **2.1x more memory bandwidth**, Huawei and China now have AI system capabilities that can beat Nvidia’s.

What’s more, is the CM384 is uniquely suited to China’s strengths, which is domestic networking production, infrastructure software to prevent network failures, and with further yield improvements, an ability to scale up to even larger domains.

The drawback here is that it takes **4.**1**x the power of a GB200 NVL72**, with **2.5x worse power per FLOP**, 1.9x worse power per TB/s memory bandwidth, and 1.2x worse power per TB HBM memory capacity.

**The deficiencies in power are relevant but not a limiting factor in China.**

## China has No Power Constraints, just Silicon Constraints

The common refrain in the West is that [AI is power-limited](https://www.semianalysis.com/p/datacenter-model), but in China, this is the opposite. The West has spent the last decade shifting a primarily coal-based power infrastructure to greener natural gas and renewable power generation paired with more efficient energy usage on a per capita basis. This is the opposite in China, where rising lifestyles and continued heavy investment mean massive power generation demand.

![](https://substack-post-media.s3.amazonaws.com/public/images/7b977aa8-9e8b-4996-ac88-6a67c69953c7_1855x598.png)
*Source: SemiAnalysis Datacenter Model*

Most of this has been powered by coal, but China also has the largest install bases of solar, hydro, wind, and now is the leader in deploying nuclear. The United States just maintains the nuclear power deployed in the 1970s. Put simply, upgrading and adding capacity to the US energy grid is a lost muscle, meanwhile in China they have added an entire US grid of capacity since 2011, or approximately the last 10 years.

If you do not have a power constraint because of your relative power abundance, it makes sense to forgo power density and increase scale-up, including optics in the design. The CM384 design considers system-level constraints even outside of the rack, and we believe that it’s not just the relative power availability that constrains China’s AI ambitions. We think that there are multiple ways for continued scaling for Huawei’s solution.

## How Many Ascend 910C and CloudMatrix 384 Can China Make?

One common misconception is that Huawei’s 910C is made in China. It is entirely designed there, but China still relies heavily on foreign production. Whether it be HBM from Samsung, wafers from TSMC, or equipment from America, Netherlands, and Japan, there is a big reliance on foreign industry.

While SMIC, the largest foundry in China, does have 7nm, the vast majority of Ascend 910B and 910C are made with TSMC’s 7nm. In fact, the US Government, TechInsights, and others have acquired Ascend 910B and 910C and every single one used TSMC dies. Huawei was able to circumvent the sanctions on them against TSMC by purchasing ~$500 million of 7nm wafers through another company, Sophgo.

![](https://substack-post-media.s3.amazonaws.com/public/images/a1896a04-96ed-4eaa-a0a2-d0a8d818d5c6_927x590.png)
*Source: SemiAnalysis Datacenter Model*

[TSMC is being fined $1 billion for this blatant sanctions violation](https://www.reuters.com/technology/tsmc-could-face-1-billion-or-more-fine-us-probe-sources-say-2025-04-08/), only 2x what they profited. It is rumored Huawei continues to receive wafers from TSMC via another 3rd party firm, but we cannot verify this rumor.

## Huawei’s HBM Access

Leading edge foreign reliance is part of the equation here, but China is even more reliant on HBM. China is not able to manufacture this reliably with CXMT still a year away from ramping any reasonable volume. Luckily Samsung has come to the rescue, having been the number one supplier of HBM to China through which Huawei has been able to stockpile a total of 13 million HBM stacks which can be used for 1.6 million Ascend 910C packages before any HBM bans.

Furthermore, this banned HBM is still being re-exported to China. The HBM export ban is specifically for raw HBM packages. Chips with HBM can still be shipped as long as they don’t exceed the FLOPS regulations. CoAsia Electronics is the sole distributor of HBM for Samsung in Greater China and they have been shipping HBM2E that is to ASIC design service company Faraday who gets SPIL to “package” it alongside of a cheap 16nm logic die.

Faraday then ships this system in package to China, which is technically allowed, but Chinese companies can then recover the HBM by desoldering. We think they employ techniques to make it very easy for the HBM to be extracted from the package, like using very weak low-temperature solder bumps, so when we say it is “packaged,” we mean this in the loosest way possible.

![](https://substack-post-media.s3.amazonaws.com/public/images/73215cc0-7d0f-4900-a0a8-69818f3b5a3e_1648x978.png)
*Source: CoAsia Electronics*

It is no coincidence that CoAsia’s revenue has exploded since 2025, right after these export controls came into force.

## Chinese Domestic Foundry Can Still Ramp

Foreign production is still required, but China’s domestic semiconductor supply chain capability has rapidly improved and is still underestimated. We’ve been consistently sounding the alarm on SMIC and CXMT’s fabrication abilities. Yield and throughput are still issues but the question is what happens longer term with China’s GPU production ramp.

Both SMIC and CXMT have received [tens of billions of dollars worth of tools](https://semianalysis.com/2024/10/28/fab-whack-a-mole-chinese-companies/), and they still receive [significant volumes of sole sourced chemicals and materials](https://semianalysis.com/2024/10/28/fab-whack-a-mole-chinese-companies/) from foreign countries despite sanctions.

![](https://substack-post-media.s3.amazonaws.com/public/images/d0abc690-f0d0-4459-8b4a-298f89941032_1294x433.png)
*Source: SemiAnalysis*

SMIC is adding capacity in Shanghai, Shenzhen, and Beijing for advanced node capacity. They will have nearly 50,000 wafers per month of capacity this year, and they continue to expand due to continued access to foreign tools and the lack of effective sanctions and enforcement. If they increase their yield, they can reach serious numbers on Huawei Ascend 910C packages.

While TSMC has provided 2.9 million dies which is enough for 800 thousand Ascend 910B’s and 1.05 million Ascend 910C’s across 2024 and 2025, the SMIC production has the potential to massively grow the capacity if HBM, wafer fabrication tools, tool servicing, and chemicals such as photoresist are not effectively controlled.

## CloudMatrix 384 System Architecture

Next let’s dive into the CloudMatrix 384 architecture, scale up networking, scale-out networking, power budget, and cost.

A full CloudMatrix system is spread across 16 racks, with each of the 12 compute rack containing 32 GPUs. In the middle of these 16 racks is 4 racks of scale up switches. To bring up world size, Huawei is scaling up across multiple racks and to do that Huawei has had to use optics. Getting to 100s of GPUs in an all-to-all scale up like Huawei is not an easy feat.

![](https://substack-post-media.s3.amazonaws.com/public/images/44796b8e-8a32-4b20-ae39-c4c0f50cefec_2560x884.png)
*Source: SemiAnalysis*

## Similarities to DGX H100 NVL256 “Ranger”

[Back in 2022, Nvidia had announced DGX H100 NVL256 “Ranger” Platform](https://pytorchtoatoms.substack.com/p/why-dgx-h100-nvl256-never-shipped), but decided to not bring it to production due to it being prohibitively expensive, power hungry, and unreliable due to all the optical transceivers required and the two tiers of network. The CloudMatrix Pod requires an incredible 6,912 400G LPO transceivers for networking, the vast majority of which are for the scaleup network.

![](https://substack-post-media.s3.amazonaws.com/public/images/803dd96a-d9ca-41d4-8de8-871ac8a3ab03_1430x804.png)
*Source: Nvidia HotChips*

## CloudMatrix384 Scale-Up Topology Estimates

The following section will explain in depth the rack architecture of their scale up NVLink competitor between 384 chips, their scale out networking, power budget break down for the entire system and implications on the massive number of optics and lack of copper cables.
