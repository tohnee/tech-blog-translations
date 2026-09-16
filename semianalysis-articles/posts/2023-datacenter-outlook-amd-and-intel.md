---
title: "2023 Datacenter Outlook – AMD and Intel Revenue, ASP, and Units – Genoa Ramp Details"
subtitle: "AMD 35% revenue share?"
date: 2022-10-17
source: https://newsletter.semianalysis.com/p/2023-datacenter-outlook-amd-and-intel
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
---

# 2023 Datacenter Outlook – AMD and Intel Revenue, ASP, and Units – Genoa Ramp Details

**AMD 35% revenue share?**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Edit: conditions have weakened signficantly and it seems that units will be down signficantly in 2023. We believe AMD will still gain share, but the volumes are too high.

AMD has held pre-briefings for their next-generation 96-core Zen 4-based Genoa server platform. While we were unable to attend officially under NDA, the industry has been buzzing for months about the new product line. This includes this week at the OCP Summit which we are attending. Performance is absolutely incredible, with more than 2x the performance per socket in many general-purpose applications versus current platforms.

This report will quantify 2023 units, average selling price, and revenue for existing server CPU lines such as Rome/Milan and Ice Lake SP, as well as next-generation Genoa, Bergamo, Sienna, and Sapphire Rapids. We expect 2023 server units to be 5.4% lower than 2022 and 5.1% lower than 2021. Those detailed figures will be shown at a deeper level further below, but at a high level, DDR5 / PCIe 5.0 based x86 server platforms will only ramp to ~18.2% of total units shipped in Q4 2023. This is a slow ramp on volumes. Content is the more important metric, and we expect ~34% of bits shipped into datacenter CPUs to be DDR5 in Q4 2023.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d4eaaef7-0630-474f-a530-95185bdea130_1198x395.png)

Since the Rome CPU launch in late 2019, AMD’s market share in servers has increased rapidly. More importantly, their average sales price went from below Intel’s to well above it due to superior TCO. In 2 years, AMD more than doubled its market share. Going forward, we expect AMD’s share of x86 server units to increase from 13.9% in Q2 2022 to 21.2% in Q4 2023. AMD’s revenue share will balloon well beyond this figure due to high average sales prices (ASP). Quantifying AMD’s ASP increases going into the future will be more important than unit gains.

Thank you for reading SemiAnalysis, if you are enjoying it, share it!

[Share](https://newsletter.semianalysis.com/p/2023-datacenter-outlook-amd-and-intel?utm_source=substack&utm_medium=email&utm_content=share&action=share)

The sell-side and buy-side consensus seem to think that Genoa and Bergamo only increase ASPs by 20% to 30%, but clearly, they do not talk to any ODMs or hyperscalers. List prices significantly increased gen-on-gen for Genoa/Bergamo versus Milan/Rome (list prices are not representative of volume sales price). The argument against significant ASP increases has generally been that we are in a recession and that AMD would not have pricing power. The reality is that Genoa and Bergamo will drive the most extensive datacenter infrastructure replacement cycle since at least Broadwell and Skylake.

Generally, enterprises and even cloud providers have kept many of their Intel Skylake SP servers deployed in 2015 active to this day. This is due to the stagnation from Intel and the DRAM industry in improving the total cost of ownership (TCO) for a given performance level by a meaningful amount. Amazon, Microsoft, and most of the industry depreciated servers over 3 years. In 2019, Amazon began adjusting the useful life of cloud servers as Intel’s 2019 servers were basically a rewarmed version of Skylake SP. Fast forward to today, Amazon and Microsoft have adjusted the useful life of servers all the way up to 6 years!

Genoa marks a big shift in TCO that makes it sensible to replace aging servers. 2S (socket) Genoa offers 4x the general-purpose performance at significantly better TCO versus 2S Skylake/Cascade Lake SP server. Initial capital expenditures for Genoa-based servers are considerably higher due to the cost of higher costs of the CPU, DDR5, and PCIe 5.0. Despite this big cost jump, Genoa and Bergamo-based servers will pay for themselves many times over versus keeping already depreciated servers deployed.

These upfront capital costs are a minuscule portion of the actual cost of operating a datacenter. Infrastructure teams at hyperscalers have complex TCO models that account for non-CPU costs such as [DRAM, which makes up 50% of the Capex for a server](https://semianalysis.substack.com/p/cxl-enables-microsoft-azure-to-cut), utilization rates, power consumption, cooling costs, floor space in a datacenter, density of servers in a rack, networking, power delivery, duplication of resources, platform engineering costs, and licensed software.

These teams at hyperscalers sole jobs are maintaining this model and weighing different hardware options for various workloads. A gross oversimplification for TCO, an Amazon employee told us that he sometimes uses when on the go, is that a deployed server’s cost is 10x power cost.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/71c1ae94-0a33-404e-8e4a-a8aff426222f_1690x497.png)

Under this oversimplified model, upgrading to a 2-socket Genoa-based server from 4 existing 2-socket Skylake/Cascade Lake-based servers (2 CPUs vs 8 CPUs) is a net present value positive transaction. The payback period for Capex spent is roughly ~18 months. The payback period for a Rome/Milan server upgrade would still be ~4 years. The improvements are even more significant when you start considering new features related to security, CXL, and AVX512.

There are a thousand reasons why these TCO and payback numbers would vary from much more to much less depending on the use case, but this is just a demonstrative mental model for combatting the argument that the average sales price (ASP) for Genoa/Bergamo is only 20% to 30% higher. The other argument is that Genoa is nearly twice as much leading-edge silicon and a more complex package, so AMD must charge a higher price.

Moving on to our incremental quarterly ramp for Zen 4-based server platforms, followed by the Q4 2022 and 2023 quarterly units, ASP, and revenue for Intel and AMD. The ramp starts slow, but picks up in Q1 2023 to 100,000 incremental quarterly units. This accelerates into the latter half of 2023 as AMD ramps down existing platforms and allocates more backend substrate supply from Rome/Milan to Genoa/Bergamo/Siena.

[Get 20% off a group subscription](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
