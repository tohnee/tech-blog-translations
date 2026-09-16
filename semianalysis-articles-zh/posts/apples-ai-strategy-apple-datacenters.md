---
title: "Apple 的 AI 战略：Apple 数据中心、端侧、云端及其他"
title_en: "Apple’s AI Strategy: Apple Datacenters, On-device, Cloud, And More"
subtitle: "何时在端侧运行、何时用 Apple 数据中心、何时用 OpenAI 的云，以及交易经济学"
date: 2024-05-27
source: https://newsletter.semianalysis.com/p/apples-ai-strategy-apple-datacenters
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Apple 的 AI 战略：Apple 数据中心、端侧、云端及其他

> 原文：[Apple’s AI Strategy: Apple Datacenters, On-device, Cloud, And More](https://newsletter.semianalysis.com/p/apples-ai-strategy-apple-datacenters) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**何时在端侧运行、何时用 Apple 数据中心、何时用 OpenAI 的云，以及交易经济学**

Nvidia 持续爬坡产能，以满足全世界对 GPU 的无限渴求，然而我们 [Accelerator 模型的广泛核查](https://www.semianalysis.com/p/accelerator-model)显示，[Apple 采购的 GPU 数量微不足道](https://www.semianalysis.com/p/accelerator-model)。事实上，他们甚至排不进前十客户。此外，虽然所有目光都聚焦在 WWDC 上，但 Apple 只是在那里「发布」AI，而不是「出货」。所有人心中悬而未决的问题是……Apple 在 AI 上到底在干什么？

[Mark Gurman](https://www.bloomberg.com/news/newsletters/2024-05-26/apple-ios-18-macos-15-ai-features-project-greymatter-privacy-openai-deal-lwni63s3) 列出了 Apple 将在 WWDC 上宣布的功能。此外各路消息满天飞，那么让我们搞清楚到底发生了什么、怎么做、以及 Apple 能做什么。

第一件事是：多个信源报道称，Apple 今年正把 M 系列处理器的产量提升至[创纪录的规模](https://www.semianalysis.com/p/accelerator-model)。这主要是 Apple 的 M2 Ultra SKU——两颗 M2 Max SoC 通过 Apple 称之为「UltraFusion」的方式拼接而成。注意，Apple 的 M3 Ultra 已被取消。

![](https://substack-post-media.s3.amazonaws.com/public/images/16fc78ce-9823-4418-a73c-2096d0c1b5b3_1010x700.jpeg)
*来源：Apple*

UltraFusion 是 Apple 的营销名称，指的是用局部硅互连（桥接裸片，bridge die）把封装内的两颗 M2 Max 芯片连接起来。在软件的许多层看来，这两颗芯片暴露为单一芯片。M2 Ultra 采用[台积电（TSMC）的 InFO-LSI 封装技术](https://www.semianalysis.com/p/advanced-packaging-part-1-pad-limited)。这与 TSMC 的 CoWoS-L 概念类似——Nvidia 的 Blackwell 以及未来的加速器都正在采用 CoWoS-L 来制造大芯片。Apple 与 Nvidia 做法的唯一主要区别是：InFO 是芯片先行（chip-first）工艺流程，而 CoWoS-L 是芯片后行（chip-last）工艺流程，而且两者使用的内存类型不同。

![](https://substack-post-media.s3.amazonaws.com/public/images/1f352fc1-a4f7-49ab-bb63-5cc969897c61_1858x628.png)
*来源：Nvidia*

Apple 此番增产令人费解之处在于：需求端没有任何迹象能够支撑 M2 Ultra 出货量的突然暴增。M2 Ultra 只用于高端 Mac Studio 和 Mac Pro 产品。这些产品已经一年没有实质性更新，短期内也没有更新计划。此外，也没有搭载它的新产品出货。

与疫情峰值需求相比，高端台式 PC 和 Mac 市场依旧相当疲软，然而 2024 年这些据称将驱动高端 Mac 的芯片产量却将显著高于过去几年，尽管没有任何迹象表明会有足够的消费需求消化掉所有这些芯片。

我们该如何解释这件事？

## **Apple 自有的 AI 服务器**

M2 Ultra 的额外产量，与近期《华尔街日报》（[WSJ](https://www.wsj.com/tech/ai/apple-is-developing-ai-chips-for-data-centers-seeking-edge-in-arms-race-0bedd2b2)）和 [Bloomberg](https://www.bloomberg.com/news/articles/2024-05-09/apple-to-power-ios-18-ai-features-with-in-house-server-mac-chips-this-year) 关于 Apple 在自建数据中心中用自研芯片向 Apple 用户供 AI 服务的报道相吻合。

此外，Apple 对自有数据中心基础设施有着庞大的扩张计划。我们正在[为 Apple 跟踪 7 个不同的数据中心站点、超过 30 栋楼宇](https://www.semianalysis.com/p/datacenter-model)以及它们的规划建设进度。其总容量将在相对较短的时间内翻倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/1b0f1de1-a7a0-4001-a0c7-7bea0f45d829_2048x1487.jpeg)
*来源：SemiAnalysis 数据中心模型*

上图是 Apple 即将建成的最大数据中心站点。目前那里只有 1 座数据中心，但明年将有多座陆续建成。我们的[数据中心模型](https://www.semianalysis.com/p/datacenter-model)有关于 Apple 未来数据中心的更多细节。

## **Apple 的基础设施团队**

表明库比蒂诺对 AI 硬件与基础设施战略动真格的另一个迹象是：几个月前他们进行了一系列重要招聘。其中包括 Sumit Gupta，他于 3 月加入 Apple 领导云基础设施。这是一次令人印象深刻的招聘。他 2007 至 2015 年在 Nvidia，参与过 Nvidia 进军加速计算的起点阶段。在 IBM 从事 AI 工作之后，他于 2021 年加入 Google 的 AI 基础设施团队，最终成为 Google 全部基础设施的产品负责人，涵盖 Google TPU 和基于 Arm 的数据中心 CPU。

他在 AI 硬件领域的深厚历练来自 Nvidia 和 Google——这两家是该领域最顶尖的公司，也是当今唯二大规模部署 AI 基础设施的公司。这是一个完美的招聘。

基于这一背景，让我们看看 Apple 正在用他们当前和未来的自研芯片以及外部芯片做什么。我们将研究 Apple 与 Nvidia 的积怨。我们还将讨论 Apple 什么可以在端侧运行、什么可以放在云端、什么必须借助外部服务商的 AI。围绕这笔交易的经济学与 Google 搜索那笔 200 亿美元的交易不同，但差异的方式和你想的不一样。我们还将讨论 Apple 如何把这些能力提供给客户并实现收入增长。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
