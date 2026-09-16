---
title: "Marvell 收购 Tanzanite Silicon：以基于 CXL 的内存扩展与池化实现可组合服务器架构"
title_en: "Marvell Acquires Tanzanite Silicon To Enable Composable Server Architectures Using CXL Based Memory Expansion And Pooling"
date: 2022-05-13
source: https://newsletter.semianalysis.com/p/marvell-acquires-tanzanite-silicon
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Marvell 收购 Tanzanite Silicon：以基于 CXL 的内存扩展与池化实现可组合服务器架构

> 原文：[Marvell Acquires Tanzanite Silicon To Enable Composable Server Architectures Using CXL Based Memory Expansion And Pooling](https://newsletter.semianalysis.com/p/marvell-acquires-tanzanite-silicon) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

Marvell 收下 Tanzanite 团队，延续了其精彩收购的火热势头。仅过去几年，Marvell 就收购了：Arm CPU 与 SOC 专家 Cavium、承袭 IBM 与 GlobalFoundries 衣钵的传奇定制 ASIC 团队 Avera Semi、SerDes、TIA 与 DSP 领域的领导者 Inphi，以及以太网交换机市场斗志昂扬的后起之秀 Innovium。Tanzanite Silicon Solutions 比这些收购标的都小得多，但它填补了 Marvell IP 阵容中一个非常重要的空缺。总之，这让 Marvell 在成为数据中心定制硅一站式商店的路上继续迈进——服务更广泛的服务器市场以及云/超大规模厂商的自研需求。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/aaa83c34-eac9-4b0d-930c-e16d8d8261eb_873x379.jpeg)

CXL 作为缓存一致性与内存池化的标准化协议实现，将成为一项变革性技术。Tanzanite 专注的正是内存池化。随着行业转向可组合服务器架构，内存池化是关键所在。我们在[关于 Ayar Labs 的文章](https://semianalysis.substack.com/p/ayar-labs-co-packaged-optics-revolution?s=w)中讨论过这一点，这里换成 Marvell 所着眼的角度来谈。

数据中心是极其烧钱的事业。所需资本开支巨大，而且你搭建所用的服务器并非同质的一整块。工作负载不是静态的，它们在不断增长和演变。计算资源、DRAM、NAND 与网络的配比随工作负载而变。一刀切的模式行不通，这正是云厂商动辄提供数十乃至数百种实例类型的原因：他们试图为不同的工作负载分别优化。即便如此，许多用户最终还是为自己根本不需要的东西买了单。

用一台只有 CPU 的简单服务器举例，先忽略加速器相关的复杂性。绝大多数已部署的服务器乍看都简单：挑一颗 CPU，英特尔（Intel）的或 AMD 的，配一块兼容的主板，插上内存、存储和网络。搞定。但事情没这么简单。你的工作负载对内存带宽或容量的需求千差万别：有的工作负载可能只要几个核，却要海量内存容量；有的可能要超大带宽和很多核，但对容量没有额外溢价。决策矩阵开始大规模堆叠。

这就是可组合服务器架构登场的时刻。核心思想是：云中面向每个工作负载的专属硬件都能按其确切需求精确定制。你只访问想要的资源，别无其他。你不再为多余的计算、存储付费，最重要的是不再为多余的 DRAM 付费。DRAM 是服务器中最昂贵的单一部件。尽管 Intel Ice Lake 和 AMD Milan 服务器 CPU 支持高达 4TB 内存，但出货量最大的配置是每路 256GB。为优化总拥有成本（TCO），DRAM 容量需要压到最低，同时仍能满足处理需求。

在任何资本高度密集的行业，稼动率都是成功最重要的因素。以半导体晶圆厂为例，除接近满载外的任何运行状态都不利于盈利与长期可持续。服务器世界的 DRAM 遵循同样的逻辑。尽管这是业务结构的基本事实，云服务商却没有多少杠杆能直接左右其数据中心内 DRAM 的利用率。每颗 CPU 的 DRAM 都通过传统内存通道直连。你可以在装机时多插或少插内存，甚至日后升级，但随着客户工作负载变化，这些都无法即时调整。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/fb22a13e-cda8-4d98-b524-1bdaaa32649d_1024x564.png)

美光（Micron）最近给出了这份预测，我们完全赞同。CPU、内存与存储部分解耦的可组合服务器架构这一未来图景终将实现。这需要 CXL 标准的多轮迭代，但标准组织全力投入，业界也一致认为这是改善成本结构的最佳路径。

这就是 Tanzanite 的用武之地。Tanzanite 有一颗「Smart Logic Interface Connector」（SLIC）SoC，可在服务器内部及跨服务器之间以低延迟实现内存与计算的独立扩展与共享。他们是最早公开展示跨 CXL 机柜级内存池化的公司之一。Astera Labs 也演示过类似技术，Rambus 也在做。我们将在仅限订阅者的章节讨论这些公司的进展，包括流片时间表。三星（Samsung）、SK 海力士（SK Hynix）和美光也很可能在开发类似的硅，但没有公开确认。短期内，DRAM 厂商可能只聚焦内存扩展，而非池化。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8ef40b73-9dea-4715-8a2f-3f79888de3cc_1024x576.png)

Tanzanite、Astera Labs 和 Rambus 当前的方案大体相似：卖一颗通过 CXL 连接其他芯片、再连接标准 DDR DIMM 的 ASIC。Tanzanite 具体瞄准 32 lane，即 2Tbps 双向带宽。他们的第一代 SLIC 芯片每颗将包含 4 通道 DDR 内存。我们与 Tanzanite 的交流以及框图显示，4 颗 CPU 连接一颗 SLIC ASIC。为免图片画质太差引起误解，这里说明一下：我获准用手机拍摄他们电脑屏幕的照片并公开展示，但拿不到直接的高质量图片。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/cec8e641-53ea-44ac-bf48-d3aa7f888cd6_1024x768.jpeg)

这是他们办公室里所跑演示的照片。向某颗 CPU 分配内存或移除内存都相当无缝、迅速。他们用 Intel Sapphire Rapids CPU 和英特尔 FPGA 跑演示，但 ASIC 还在开发中。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/37398c65-530f-438e-9e1e-8a752047aeb3_768x1024.jpeg)

内存池化的巨大好处在于，你可以只增减所需数量的 DRAM。代价是延迟惩罚，这是最大的顾虑。按 Tanzanite 的说法，相当于「CPU 到 CPU 的 NUMA 延迟」。可惜他们不肯给出确切数字，但我们估计往返延迟在 250ns 量级，而 Intel Ice Lake 和 AMD Milan 访问本地内存通常为 100ns 到 150ns。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7c7554d6-686b-4cc6-926e-06e7cd2cdbc9_1000x708.jpeg)

这些 CXL 内存加速器的不同之处在于，它们提供了面向单一 CPU 主机之外内存池的能力。三星已经做出了自己的 CXL 内存模组，但受限于只能连接单一节点，而且是低出货量的定制产品，并非大宗商品化的无缓冲或带寄存器 DIMM。

简而言之，Tanzanite 让 Marvell 得以抢先起跑，拥有最早一批 CXL 内存加速器之一。内存池与可组合服务器架构对突破带宽瓶颈和容量限制至关重要。它们应能提升内存利用率，同时提供远低于在每台服务器里塞大容量 LRDIMM 的总拥有成本。在付费章节中，我们将讨论 Tanzanite、Astera Labs 和 Rambus 的流片与量产时间表，也会谈 Tanzanite 的融资情况以及出售的动机。

[分享](https://newsletter.semianalysis.com/p/marvell-acquires-tanzanite-silicon?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)
