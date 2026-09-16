---
title: "Intel Emerald Rapids 在小芯片路线上回头——设计、性能与成本"
title_en: "Intel Emerald Rapids Backtracks on Chiplets – Design, Performance & Cost"
subtitle: "竞争格局分析考量，Sapphire Rapids 的悄然重新设计"
date: 2023-05-03
source: https://newsletter.semianalysis.com/p/intel-emerald-rapids-backtracks-on
crawled: 2026-09-15
authors: ["Dylan Patel", "Gerald Wong", "George Cozma", "Locuza", "Afzal Ahmad"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Intel Emerald Rapids 在小芯片路线上回头——设计、性能与成本

> 原文：[Intel Emerald Rapids Backtracks on Chiplets – Design, Performance & Cost](https://newsletter.semianalysis.com/p/intel-emerald-rapids-backtracks-on) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**竞争格局分析考量，Sapphire Rapids 的悄然重新设计**

在 Intel 最近的 DCAI 网络研讨会上，EVP Sandra Rivera 揭示了 Intel 第五代至强可扩展处理器 Emerald Rapids 在顶盖之下的模样。Intel 决定在小芯片（chiplet）路线上回退一代，只用 2 颗大裸片（die）来设计 Emerald Rapids（EMR）。它的前代 Sapphire Rapids（SPR）用的是 4 颗更小的裸片。反直觉的是，Intel 把最高核心数配置的芯片数量从 4 颗减到了 2 颗。这让大多数人摸不着头脑，因为包括 Intel 在内的所有人，此前都在鼓吹用更小的裸片做芯片解耦以改善良率并扩展性能。

今天，我们想更深入地探讨 Intel 在 Emerald Rapids（EMR）上相对于 Sapphire Rapids（SPR）所做的具体改动。我们将逐一讲解自制的版图（floor plan）示意图，按工作负载细谈性能、成本对比，以及与 AMD 相比的竞争环境。此外，我们还将详述发生在 Sapphire Rapids 身上、被大多数人忽视的一个重大变化。

## **Emerald Rapids 的变化**

最大的变体 EMR-XCC 将核心数从 SPR 的 60 核提升到 64 核。不过封装上总共有 66 个物理核心，通过降档屏蔽（binning）来辅助良率。Intel 不打算像 60 核 SPR 那样推出全量开启的 66 核 EMR SKU。EMR 由两颗 33 核裸片组成，而 SPR 用的是四颗 15 核裸片。

另一大变化是 Intel 大幅增加了共享 L3 缓存，从 SPR 的每核 1.875MB 提升到 EMR 高达每核 5MB！这意味着顶级 SKU 拥有全核共享的 320MB L3 缓存，是 SPR 所提供最大值的 2.84 倍。本地侦听过滤器（Local Snoop Filter）和远程侦听过滤器（Remote Snoop Filter）也相应增大，以配合 L3 缓存的大幅增加（LSF——3.75MB/核，RSF——1MB/核）。

![](https://substack-post-media.s3.amazonaws.com/public/images/7bcec9fe-311b-41a0-8635-5e9e58cf8ce0_1732x532.jpeg)

DDR5 内存支持从 4800 MT/s 提升到 5600 MT/s。用于跨插槽（socket）通信的 UPI 速率从 16 GT/s 升级到 20 GT/s。奇怪的是，尽管跨插槽速率更高，支持的总插槽数却从 8 路降到了 2 路。这很可能是为了加快上市时间，因为它只影响极小一部分市场，而且 AMD 本来也不在那个市场参与竞争。所有这些都可在现有的「Eagle Stream」平台上直接兼容，沿用同一 LGA 4677 Socket E1 插槽。PCIe 通道数保持不变，不过终于增加了 CXL 分叉（bifurcation）支持——这是 Sapphire Rapids 的一个痛点。

细看封装，我们注意到 Intel 在比 SPR 更小的面积里塞进了更多核心和多得多的缓存！含切割线（scribe lines）在内，两颗 763.03 mm² 的裸片合计 1,526.05 mm²，而 SPR 用四颗 393.88 mm² 的裸片，总计 1,575.52 mm²。EMR 面积小了 3.14%，但印刷核心数多 10%，L3 缓存是 2.84 倍。这一令人印象深刻的成绩，部分正是靠*减少*芯片数量实现的，我们稍后会解释。不过，还有其他因素在帮助 EMR 缩小面积。

在为 EMR 绘制版图草图时，我们发现无法把必要的模块压缩到与 Intel 公开信息相匹配的面积。我们以 SPR 的组件为参照，结果发现参照物太大了。这是因为 Intel 优化了物理设计，使一些模块更紧凑、面积效率更高，从而实现进一步的面积缩减。而且，这已经不是 Intel 第一次靠改物理设计来省面积了。

## **Sapphire Rapids 的裸片瘦身**

虽然公开场合很少谈及，但 Intel 在 Sapphire Rapids[通往量产 E5 步进的至暗时刻](https://www.semianalysis.com/p/the-dark-side-of-the-semiconductor)里，也曾对其进行过一次彻底的从头重新设计。信不信由你，Sapphire Rapids 芯片有*两套*不同的物理设计和裸片尺寸。

![](https://substack-post-media.s3.amazonaws.com/public/images/5a0cb739-65cf-46cb-931e-c8e09c247a72_1130x775.jpeg)

Raja Koduri 在 2021 年架构日上展示的是较大、较早版本的 SPR，早期工程样品的第三方拆解中出现的也是它。较小、较新的 SPR 变体在 Vision 2022 上亮相，最终量产 SKU 采用的正是它。

Intel 展示过两个版本 SPR 的晶圆。较早的版本每片晶圆有 137 颗毛裸片（gross die），而最终版本有 148 颗。这需要一路回退到芯片的版图规划和物理设计从头再做。一大好处是，每片晶圆多产 8% 的裸片，改善了 Sapphire Rapids 的成本结构。

![](https://substack-post-media.s3.amazonaws.com/public/images/072ab3c6-1a57-43b9-bee9-0bc42cf43582_6400x3500.jpeg)

在 [SPR 漫长 bring-up 过程中进行的多次流片修订](https://www.semianalysis.com/p/the-dark-side-of-the-semiconductor)中，我们发现 Intel 改动了核心及外围的物理设计与布局，实现了 5.7% 的面积缩减。I/O 区域（North Cap）经过重新实现，裸片高度节省了 0.46 mm。I/O 模块之间的水平间距也做了优化，裸片宽度节省 0.46 mm。容纳 CPU 核心、缓存和控制器的网格（mesh）瓦片（tile）面积也必须缩小 3.43% 才能塞进更紧凑的版图，同时微调了 CPU 核心宽度和瓦片间距。

![](https://substack-post-media.s3.amazonaws.com/public/images/437673a2-1959-4310-8b51-795641476edd_8000x4832.jpeg)

一般来说，设计团队极少会在产品发布前做两套不同布局和裸片尺寸，因为上市时间高于一切。也许是 Sapphire Rapids 的多次延期给了他们足够的时间去追求额外的面积节省。如果它按原定的 2021 年目标上市，我们大概率见不到这个更小的修订版，至少一开始见不到。

同理，Intel 把同样的布局优化原则应用到了 EMR 上，尤其是为容纳巨大的 L3 缓存。这里我们展示了核心和网格瓦片的改动示意，包括核心上方显著加高的 SRAM 区域，用来容纳增加的 L3 缓存和侦听过滤器。由此，每个核心瓦片的面积增加了 11.8%。得益于 SRAM 物理设计的优化，Intel 只增加了 1.41 mm²，就多塞进了 3200 KB 的 L3 缓存，还加大了 LSF 并把 RSF 翻倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/5caa2b52-6808-4607-a59c-c1f1eb6821ad_2696x1115.jpeg)

## **Emerald Rapids 版图**

下面是 EMR-XCC 的版图布局。两颗裸片上，66 个核心加上 I/O 区域通过一个 7x14 的网格互连网络连成一体。

![](https://substack-post-media.s3.amazonaws.com/public/images/f7ad95eb-e145-4418-b934-cac79f9607bc_7750x5650.jpeg)

在中部，网格网络通过 EMIB 跨越片外边界 7 次。相比之下，SPR 四颗裸片上是 8x12 的网格，有 20 处片外跨越。这一拓扑结构变化的影响将在下文性能部分展开。

从上面的布局可以看出，尽管两颗小芯片非常相似，它们实际上用的是不同的流片和光罩组，Intel 再次像 SPR 那样采用镜像裸片。若使用同一颗裸片旋转 180 度，可以把光罩组需求减半，但会使其跨越 EMIB 的多裸片 Fabric IO 复杂化。

![](https://substack-post-media.s3.amazonaws.com/public/images/fe95ad57-d43e-4890-9499-20e2b808e608_6096x4986.jpeg)

说到 EMIB，硅桥（silicon bridge）数量从 10 个大幅减少到仅 3 个，其中中间那根更宽以容纳 3 列网格。奇数列网格同样出现在[单片版 SPR](https://www.angstronomics.com/p/monolithic-sapphire-rapids) 上，这也可能是他们必须镜像裸片的原因之一，因为旋转会打乱对齐并使走线交叉复杂化。

![](https://substack-post-media.s3.amazonaws.com/public/images/f630e598-5a56-4d22-96df-f8bb70cec951_1681x544.jpeg)

透过这个新布局，我们可以看到小芯片「重新聚合」的真正好处。芯片接口占总面积的比例，从 SPR 的 16.2% 降到 EMR 的区区 5.8%。换个角度，可以看核心面积利用率，即总裸片面积中用于计算核心和缓存的比例。这一数字从 SPR 的低点 50.67% 提升到 EMR 好得多的 62.65%。这部分增益也来自 EMR 更少的物理 IO，因为 SPR 有更多只在单插槽工作站细分市场才开启的 PCIe 通道。

如果你的良率够好，既然可以用更少、更大的裸片，为什么还要把面积浪费在冗余 IO 和小芯片互连上？Intel 那部充满故事的 10nm 工艺，从 2017 年凄惨的开局一路走来，如今以改名后的 Intel 7 之身，良率已经相当不错。

## **成本——不是你想的那样**

以上这些关于布局优化、在更小总面积里塞进更多核心和缓存的讨论，会让你以为 EMR 比 SPR 更便宜。事实并非如此。

从根本上说，大矩形就是没法在圆形晶圆上摆得整齐。回到每片晶圆毛裸片数，我们估计 EMR-XCC 的晶圆布局与 SPR-MCC 相当，即每片晶圆 68 颗裸片。假设良率完美且裸片全部可用，EMR 每片晶圆只能出 34 颗 CPU，低于 SPR 每片晶圆的 37 颗。一旦良率偏离完美，EMR 的处境还会更糟，这显出了选用更大裸片的劣势。

尽管每颗 CPU 耗用的硅面积更少，EMR 的生产成本实际上高于 SPR。

平心而论，若要单独评估布局变化对成本的影响，应该把 EMR 与一个假想的每核 5MB L3 的 SPR 相比。对这颗更高的理论裸片做面积估算，结果是每片晶圆 136 颗毛裸片，即这个 4 芯片变体每片晶圆 34 颗 CPU——与实际的 2 芯片设计完全一样。此外，EMIB 数量从 10 个减到 3 个，也确实会改善 2 芯片方案的封装成本和良率。

![](https://substack-post-media.s3.amazonaws.com/public/images/f8a77b2c-0082-4a88-bfe7-3e200ca9c0aa_1575x948.jpeg)

[分享](https://newsletter.semianalysis.com/p/intel-emerald-rapids-backtracks-on?utm_source=substack&utm_medium=email&utm_content=share&action=share)

那么，如果布局变化和芯片数量缩减都无助于降低成本，EMR 的首要驱动因素到底是什么？

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
