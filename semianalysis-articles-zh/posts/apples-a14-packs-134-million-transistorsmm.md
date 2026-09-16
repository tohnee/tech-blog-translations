---
title: "苹果 A14 每平方毫米集成 1.34 亿颗晶体管，但仍未达到台积电的密度宣称"
title_en: "Apple’s A14 Packs 134 Million Transistors/mm², but Falls Short of TSMC’s Density Claims"
date: 2020-10-27
source: https://newsletter.semianalysis.com/p/apples-a14-packs-134-million-transistorsmm
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 苹果 A14 每平方毫米集成 1.34 亿颗晶体管，但仍未达到台积电的密度宣称

> 原文：[Apple’s A14 Packs 134 Million Transistors/mm², but Falls Short of TSMC’s Density Claims](https://newsletter.semianalysis.com/p/apples-a14-packs-134-million-transistorsmm) · SemiAnalysis

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/240314ac-6e90-4a24-b91b-05269761f1fb_1200x998.png)

我们的朋友 ICmasters 深入分析了苹果 A14 Bionic 的封装。其裸片面积已经揭晓，为 88mm²。尽管塞入了 118 亿颗晶体管，得益于采用台积电（TSMC）的 5nm 制程节点，其裸片面积仍然非常小。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2ccc72fa-9235-4793-ba0e-0646ff2a60c5_1200x672.png)

进步的步伐并非一片美好。苹果的芯片历来能在其处理器中达到制程节点理论密度的 90% 以上。而这一代却大幅偏离了这个标准。与理论密度相比，A14 的有效晶体管密度只有区区 78%。尽管台积电宣称 N5 相比上代缩小 1.8 倍，苹果实际只实现了 1.49 倍的微缩。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2e092954-0ed8-45c1-8f2d-03aac767169c_2279x585.png)

这并不是台积电或苹果的失败。这两家公司分别是半导体制造与半导体设计领域毋庸置疑的领导者。理论密度无法转化为有效密度，其根源在于 SRAM 微缩正在缓慢走向消亡。SRAM 在处理器中被广泛使用，从寄存器到缓存都有它的身影。台积电的 Geoffrey Yeap 指出，典型的移动 SoC 由 60% 的逻辑、30% 的 SRAM 以及 10% 的模拟/IO 构成。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a7d27d2b-cd9a-46cf-af8c-0d920f81b03c_1200x675.jpeg)

台积电的 N5 节点不同于以往的微缩，显现出 SRAM 微缩放缓的迹象。尽管逻辑电路实现了完整的微缩，SRAM 却只有 1.35 倍的缩小。这一数字还被高估了——一旦把其他辅助电路计算在内，实际数值还会更低。这也解释了台积电为何指引 N5 的芯片面积缩减为 35%-40%。SemiAnalysis 预计这将成为未来新节点持续存在的趋势。台积电和三星（Samsung）已经在演示 3D 堆叠 SRAM，这将有助于缓解密度问题。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6b6947ca-bbbe-4dde-bb83-469e0942498d_1280x720.jpeg)

3D 堆叠并非银弹。成本微缩已开始急剧放缓。以台积电 N5 约 ~$17k 的晶圆定价来看，每颗晶体管的成本显然并没有下降。即使 SRAM 微缩能够跟上，从 N7 到 N5 每颗晶体管的成本也仍将持平。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/25e6115c-89e4-4224-ae97-35ca01034cd9_1147x663.jpeg)

*本文最初于 2020 年 10 月 27 日发布于 [SemiAnalysis](https://semianalysis.com/apples-a14-packs-134-million-transistors-mm2-but-falls-far-short-of-tsmcs-density-claims/)。*

*SemiAnalysis 的客户及员工可能持有本文所提及公司的头寸。*
