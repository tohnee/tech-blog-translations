---
title: "As Moore’s Law Slows, Apple Is Forced To Use Cheaper Chipsets In Non-Pro iPhones"
subtitle: "Terrifying Implications For The Semiconductor Industry"
date: 2022-03-14
source: https://newsletter.semianalysis.com/p/as-moores-law-slows-apple-is-forced
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
---

# As Moore’s Law Slows, Apple Is Forced To Use Cheaper Chipsets In Non-Pro iPhones

**Terrifying Implications For The Semiconductor Industry**

> ⚠️ 付费订阅文章：以下正文为公开可见的预览部分，在付费墙处截断，并非全文。/ Paid post: only the publicly visible preview portion is archived; the body is truncated at the paywall.

Apple has consistently driven performance and smartphone capabilities in smartphone SOCs. The iPhone is one of the best phones and the incredible silicon teams at Apple are much of the reasons why. Apple has consistently had the best CPU, GPU, video recording, and efficiency with every release. Many buyers of the iPhone may even argue that the massive yearly gains in the chipset are irrelevant because the iPhone is already well past the point of diminishing returns.

Ming Chi Kuo, the legendary Apple supply chain analyst, has dropped some major news for fruit phone lovers. The not-so successful iPhone Mini is dead and Apple is instead replacing it with an [iPhone Max](https://twitter.com/mingchikuo/status/1503033674643939333?s=20&t=hS6vNUMnR_o3JEXEkeMdfA). This would be a larger iPhone with a similar screen size as the flagship iPhone Pro Max. In addition, Kuo commented that the iPhone 14 and iPhone 14 Max would not receive the new A16 chipset that launches this year, but instead [will receive the existing A15 chipset.](https://twitter.com/mingchikuo/status/1503033974473760768) In addition, he stated the Pro models would receive 6GB of LPDDR5 instead of 6GB of LPDDR4X like the non-pro iPhones.

Moore’s law has slowed, especially in the economic sense. 2018 was Apple’s last major step down in cost per transistor due to TSMC’s N10 to N7 process node shrink. With the transition from N7 to N5, the cost benefits were relatively small due to [SRAM scaling issues.](https://semianalysis.com/apples-a14-packs-134-million-transistors-mm2-but-falls-far-short-of-tsmcs-density-claims/) N7 is entering its 5th year of production, and N5 is now at its 3rd, yet the only hint of per wafer pricing changes have been in the wrong direction. Until now, Apple has already powered through [the existing cost scaling](https://semianalysis.com/apple-a14-die-annotation-and-analysis-terrifying-implications-for-the-industry/) issues and maintained a transistor count CAGR of 30% for the last 3 years.

This all changes in 2022.

[TSMC’s N3 has been delayed](https://semianalysis.substack.com/p/tsmc-3nm-wafer-shipments-pushed-into). For the first time ever, Apple will have 3 generations on the same generation of process density. Apple is using TSMC’s N4 process node, which is only a meager 5% increase in density for pure logic scaling. TSMC reports N4 process node revenue under their “N5” node on financial statements because they are the same node family and even share the same fabs.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f5b86cb9-de0e-44ad-833a-8a7dda2a3195_1023x467.png)

Apple using the same node is completely unprecedented and means they have to face tough decisions. [A15 was already a relatively chunky 107mm2.](https://semianalysis.substack.com/p/apple-a15-die-shot-and-annotation) Apple faced a tough choice of forcing their various IP teams under strict area budgets and influencing long term designs, or a large increase in cost of manufacturing. [While Apple’s CPU performance gains have slowed down](https://semianalysis.substack.com/p/apple-cpu-gains-grind-to-a-halt-and), they will be implementing a large core change this year. In addition, GPU, NPU, media blocks, and ISPs are also getting improved. To accommodate their new architecture, Apple is going to spend quite a few more transistors. This will likely bring transistor counts up to around ~19 billion, and die sizes to ~130mm2.

In addition, Apple will need to increase memory bandwidth for their SOC. They have been able to stay on LPDDR4x for 5 generations [by increasing on die cache sizes and improving utilization.](https://semianalysis.substack.com/p/apple-a15-die-shot-and-annotation) With the A16, the step up to LPDDR5 brings a large cost increase. Due to the way the 3 major DRAM companies have slowly increased output, cost per bit of DRAM has not really fallen. Memory prices are a major drag on computing.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6561c07f-c794-4f50-a31b-19c3adf20970_1096x696.png)

The iPhone 13 ships with 4GB of LPDDR4x, moving to 6GB of LPDDR5 and to the larger A16 chipset would be cost prohibitive. This would result in more than a $40 increase in bill of materials (BOM). With numerous supply chain disruptions and cost increases for energy and commodities, it would be a difficult pill for Apple to also swallow the ballooning silicon costs as well. Apple could also increase prices, but that likely would eat into sales volumes.

It seems Apple has chosen the middle ground of keeping the same A15 chipset in the iPhone 14 and iPhone 14 Max and moving memory up from 4GB to 6GB. This likely allows Apple to maintain the iPhone 13’s $799 price point for the iPhone 14. The 14 Max would then slot in at $899 and the same specs. The iPhone 14 Pro and Pro Max likely remain the same $999 and $1099 price points.

The bifurcation of iPhone SOCs is likely a trend that remains well into the future. Even when TSMC’s N3 is finally shipping [in early 2023](https://semianalysis.substack.com/p/tsmc-3nm-wafer-shipments-pushed-into), wafer cost will be well over $20k. Transistor cost scaling at N3 is non-existent and therefore this problem only continues. TSMC’s N5 yields are amazing, with D0 at around 0.07, so [chiplets with more advanced packaging](https://semianalysis.substack.com/p/advanced-packaging-part-1-pad-limited) isn’t a solution. The world will have to live with these cost scaling issues [by either eating the cost increases](https://www.fabricatedknowledge.com/p/the-rising-tide-of-semiconductor), or slowing the growth of transistor counts.

Behind the subscriber only wall, we will discuss the orders Apple has put into fabs and memory producers as well as our take on wafer fabrication equipment outlook. It has changed.

[Share](https://newsletter.semianalysis.com/p/as-moores-law-slows-apple-is-forced?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[Subscribe now](https://newsletter.semianalysis.com/subscribe?)
