---
title: "特斯拉 AI Day 超算芯片预告｜这是台积电 InFO_SoW 的首次部署吗？"
title_en: "Tesla AI Day Supercomputer Chip Teaser | Is This The First Deployment Of TSMC InFO_SoW?"
date: 2021-08-04
source: https://newsletter.semianalysis.com/p/tesla-ai-day-supercomputer-chip-teaser
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 特斯拉 AI Day 超算芯片预告｜这是台积电 InFO_SoW 的首次部署吗？

> 原文：[Tesla AI Day Supercomputer Chip Teaser | Is This The First Deployment Of TSMC InFO_SoW?](https://newsletter.semianalysis.com/p/tesla-ai-day-supercomputer-chip-teaser) · SemiAnalysis

我们做分析力求以事实为依据，但最近流出的一张特斯拉芯片照片引来了海量猜测，我们也想下水蹚一蹚。发帖人是 Dennis Hong，机器人与自动驾驶领域的世界知名研究者。他是加州大学洛杉矶分校（UCLA）的教授，执掌一个大型实验室。他的[推文](https://twitter.com/DennisHongRobot/status/1422435800755568644?s=19)只写了 Tesla AI Day 加上 8 月 19 日的日期、时间和活动地点。这个时间点相当耐人寻味——特斯拉刚刚建成了一台在某些人看来可算是全球第 3 大的超算。那台机器是[用超微（Super Micro）系统的英伟达 GPU 搭建的。](https://www.servethehome.com/tesla-supercomputer-with-nvidia-a100-80gb-and-perhaps-supermicro-shown/)

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/21a996eb-eab4-4c63-8585-c6ffda93f991_872x872.jpeg)

乍看之下，图中有载板、散热器和供电模块。当然，最有意思的部分是芯片。它有一大片 BGA 焊盘阵列和一个 5×5 的芯片阵列。这种封装看起来极其非主流，我们唯一能联想到的就是台积电的集成扇出晶圆级系统技术（InFO_SoW）。[这是 IEEE 上相关论文的链接。](https://ieeexplore.ieee.org/document/9159219)

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/72fd0d3a-a7a2-4304-afb0-0400085e0c36_762x433.png)

这张图与特斯拉芯片惊人地相似，并提供了些许线索。和特斯拉的图一样，图中有冷板，多颗芯片排成网格，一片 InFO 晶圆，还有连接器。结构与特斯拉那颗一一对应，但确切细节与台积电最初的论文似乎略有不同。

> InFO_SoW 自身充当载体，从而免去了基板和 PCB。紧凑系统内紧密排布的多芯片阵列，使该方案得以收获晶圆级的好处：低延迟芯片间通信、高带宽密度以及低 PDN 阻抗，从而带来更强的计算性能与能效。除异构芯片集成之外，其晶圆级工艺能力还支持基于小芯片（chiplet）的设计，带来更大的成本节约与设计灵活性。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/53870feb-3658-47a9-8746-7d2d4392291c_1024x246.jpeg)

这突破了当前多芯片模块（MCM）的瓶颈。采用中介层技术的方案（如英伟达数据中心 GPU）受限于中介层的制造极限。台积电第 5 代 CoWoS-S 近期[已量产 3 倍光罩极限的中介层](https://fuse.wikichip.org/news/6031/5th-gen-cowos-s-extends-3-reticle-size/)。光罩极限为 26mm × 33mm，对应光刻机一次曝光所能图案化的最大面积。由于中介层本身就是硅芯片，这种做法涉及光罩拼接（reticle stitching）等制造难题。这类封装在为巨型 AI 工作负载扩展芯片数量方面存在天花板。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/88be63c1-70c2-4d72-9048-7ac32f911a94_923x370.png)

另一种方法是倒装芯片（flip chip）封装。这种封装下最著名的 MCM 设计是 AMD 的 CPU。它们没有光罩极限的问题，但在功率和布线密度上有巨大的短板。芯片间数据传输的功耗显著更高，芯片间带宽受限。受这些限制，这类封装同样不适合巨型 AI 工作负载。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e0f98355-0698-4d58-9888-360ee781f279_788x408.png)

按特斯拉 Dojo 超算设计所期望的扩展规模，将产生惊人的热量。InFO_SoW 可支撑 7,000W 的功率。对比英伟达数据中心 A100 GPU，其最高配置也只有 500W。这就要求对散热做极度周密的考量，而台积电那篇 InFO_SoW 论文给出了一个方案。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d045fa92-66f1-4955-9c36-ec61b0b9adc8_655x364.png)

这张图相当简陋，但特斯拉图中的冷板与之类似，都有许多进水口和出水口。在这种功率和热密度下，水冷是刚需。

另一个显眼的细节是，图里似乎没有任何 HBM 或其他基于 DRAM 的技术。[与 Cerebras 如出一辙，他们很可能采用了完全依赖片上 SRAM 的设计。可参阅我们对 Cerebras 所用确切架构的深度解析。](https://semianalysis.substack.com/p/cerebras-wafer-scale-hardware-crushes)

虽然我们期待 8 月 19 日特斯拉 AI Day 的揭晓，但也不会在这颗芯片的确切细节上想得太远。InFO_SoW 目前只是推测，尽管此前有[传闻](https://www.chinatimes.com/newspapers/20200817000176-260202?chdtv)称特斯拉、博通、台积电三方将合作将其产品化。Google 与博通在 TPU 系列 AI 加速器上就有类似的合作安排。晶圆级系统技术与集成扇出的结合，可能让他们实现英伟达等现有 AI 加速器做梦都想不到的惊人纵向扩展 AI 性能。

三星（Samsung）[几乎可以肯定正在以其「5nm」制程生产下一代车载芯片](https://twitter.com/david_schor/status/1416918003913011200?s=20)。而这颗看起来可能是一颗完全不同的芯片：面积更大，封装方式也大不相同。上图那种封装不可能进到量产汽车里，而是部署在数据中心，用于训练随后部署到车上支撑自动驾驶的巨型 AI 网络。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

[分享](https://newsletter.semianalysis.com/p/tesla-ai-day-supercomputer-chip-teaser?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[发表评论](https://newsletter.semianalysis.com/p/tesla-ai-day-supercomputer-chip-teaser/comments)

*本文最初于 2021 年 8 月 4 日发布于 [SemiAnalysis](https://semianalysis.com/tesla-ai-day-supercomputer-chip-teaser-is-this-the-first-deployment-of-tsmc-info_sow/)。*

*SemiAnalysis 的客户及员工可能持有本文所提及公司的仓位。*
