---
title: "Apple’s A14 Packs 134 Million Transistors/mm², but Falls Short of TSMC’s Density Claims"
date: 2020-10-27
source: https://newsletter.semianalysis.com/p/apples-a14-packs-134-million-transistorsmm
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
---

# Apple’s A14 Packs 134 Million Transistors/mm², but Falls Short of TSMC’s Density Claims

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/240314ac-6e90-4a24-b91b-05269761f1fb_1200x998.png)

Our friends over at ICmasters have delved into the package of the Apple A14 Bionic. The die size has been unmasked, and it stands in at 88mm2. Despite cramming in 11.8 billion transistors, the die size is incredibly small thanks to utilization of TSMC’s 5nm process node.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2ccc72fa-9235-4793-ba0e-0646ff2a60c5_1200x672.png)

The march of progress is not all rosy. Apple’s chips have historically achieved 90%+ of the process node’s theoretical density in their processors. This generation stands out by missing that mark by a large amount. A14 comes in at a cool 78% effective transistor density when compared to theoretical density. Despite TSMC claiming a 1.8x shrink for N5, Apple only achieves a 1.49x shrink.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2e092954-0ed8-45c1-8f2d-03aac767169c_2279x585.png)

This is not due to a failure of TSMC or Apple. These companies are clear leaders for the manufacturing and design of semiconductors respectively. Instead, this failure to convert theoretical to effective density stems from the slow death of SRAM scaling. SRAM is extensively used throughout a processor from registers to caches. Geoffrey Yeap of TSMC claims that the typical mobile SoC which consists of 60% logic, 30% SRAM, and 10% analog/IO.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a7d27d2b-cd9a-46cf-af8c-0d920f81b03c_1200x675.jpeg)

TSMC’s N5 node diverges from prior shrinks by showing signs of slowing SRAM scaling. Despite being a full shrink with logic, the SRAM is a 1.35x shrink. This figure is overstated as it will end up being even lower once other the other assist circuitry is accounted for. Hence TSMC’s guidance of chip area reduction at 35%-40% with N5. SemiAnalysis expects this to be a trend that will persist with new nodes. TSMC and Samsung are already demonstrating 3D stacked SRAM which will help alleviate the issue of density.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6b6947ca-bbbe-4dde-bb83-469e0942498d_1280x720.jpeg)

3D Stacking is not the silver bullet. Cost scaling has begun slowing dramatically. With TSMC N5 wafer pricing in the ~$17k range, it is clear cost per transistor has not fallen. Even if SRAM scaling kept up, the cost per transistor would still have remained flat from N7 to N5.

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/25e6115c-89e4-4224-ae97-35ca01034cd9_1147x663.jpeg)

*This article was originally published on [SemiAnalysis](https://semianalysis.com/apples-a14-packs-134-million-transistors-mm2-but-falls-far-short-of-tsmcs-density-claims/) on October 27nd 2020*.

*Clients and employees of SemiAnalysis may hold positions in companies referenced in this article*.
