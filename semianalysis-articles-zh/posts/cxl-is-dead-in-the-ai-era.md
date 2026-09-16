---
title: "CXL 在 AI 时代已死"
title_en: "CXL Is Dead In The AI Era"
subtitle: "AI 加速器的海滨面积考量、内存池化的负面因素、自研芯片的采用"
date: 2024-03-16
source: https://newsletter.semianalysis.com/p/cxl-is-dead-in-the-ai-era
crawled: 2026-09-15
authors: ["Dylan Patel", "Jeremie Eliahou Ontiveros"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# CXL 在 AI 时代已死

> 原文：[CXL Is Dead In The AI Era](https://newsletter.semianalysis.com/p/cxl-is-dead-in-the-ai-era) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**AI 加速器的海滨面积考量、内存池化的负面因素、自研芯片的采用**

如果把时间拨回两年前、AI 尚未迅速崛起之时，数据中心硬件圈的大半壁江山都在追逐 CXL。它被吹捧为带来异构计算、内存池化和可组合服务器架构的救世主。老牌厂商和一大批新创公司争相把 CXL 集成进自己的产品，或打造基于 CXL 的新产品，如内存扩展器（expander）、池化器（pooler）和交换机。快进到 2023 年和 2024 年初，许多项目已被悄悄搁置，许多超大规模云厂商和大型半导体公司几乎完全调转了方向。

随着 Astera Labs IPO 和产品发布临近，关于 CXL 的讨论至少在短期内重回前排。我们已[大量撰写过这门技术](https://www.semianalysis.com/p/cxl-deep-dive-future-of-composable)、它[为云服务商节约成本的潜力](https://www.semianalysis.com/p/cxl-enables-microsoft-azure-to-cut)，以及[生态系统与硬件栈](https://www.semianalysis.com/p/cxl-deep-dive-future-of-composable)。尽管纸面上前景光明，数据中心格局已发生巨变，但有一件事没变：控制器和交换机等 CXL 硬件仍然没有形成有意义的出货量。尽管如此，围绕 CXL 仍有许多噪音和研究，业内某些人士如今又在鼓吹 CXL 是 AI 的「使能者」这一叙事。

更广泛的 CXL 市场是否已准备好起飞并兑现承诺？CXL 能成为 AI 应用的互连吗？它在 CPU 外挂扩展与池化中的角色又是什么？我们将在本报告的订阅版部分回答这些问题。

简单的回答是：不能——那些鼓吹 CXL 用于 AI 的人大错特错。先快速回顾一下 CXL 的主要用例与承诺。

## CXL 快速回顾

CXL 是构建在 PCIe 物理层之上的协议，可实现跨设备的缓存与内存一致性。借助广泛普及的 PCIe 接口，CXL 允许内存在各种硬件之间共享：CPU、NIC 和 DPU、GPU 及其他加速器、SSD 和内存器件。

由此带来以下用例：

- 内存扩展：CXL 可以帮助提升服务器的内存带宽和容量。
- 内存池化：CXL 可以创建内存与 CPU 解耦的内存池，理论上可大幅提高 DRAM 利用率。纸面上，这能为每家云服务商节省数十亿美元。
- 异构计算：ASIC 的效率远高于通用 CPU。CXL 可以在 ASIC 与通用算力之间提供低时延的缓存一致性互连，帮助实现异构计算，让应用更容易把它们集成进现有代码库。
- 可组合服务器架构：服务器被拆解为各种组件并按组放置，这些资源可以动态、即时地分配给工作负载，减少资源搁浅、提高利用率，同时更好地匹配应用需求。

下图讲述了故事的一部分：CXL 可以填补主系统内存与存储之间的时延和带宽鸿沟，从而开启一个新的内存层级。

![](https://substack-post-media.s3.amazonaws.com/public/images/ccd5ab9c-add7-4a0c-bc41-1411531124b4_1281x737.png)
*SNIA*

现在有人[预测 CXL 销售额到 2028 年将达到 $15 billion](https://www.yolegroup.com/press-release/cxl-technology-unlocks-memory-performance/)，而今天只有几百万美元，所以我们觉得是时候对 CXL 市场做一次正经的更新了——因为那个预测彻头彻尾地荒谬。先从「CXL 用于人工智能」这个话题说起。

## **CXL 不会成为 AI 时代的互连**

当前，CXL 的可用性是主要问题：NVIDIA 的 GPU 不支持它，而在 AMD 那边，该技术仅限于 MI300A。MI300X 虽然在硬件上理论上可以支持 CXL，但并没有被正确暴露出来。CXL IP 的可用性未来会改善，但存在比可用性更深的问题，使 CXL 在加速计算时代无足轻重。

两个主要问题与 PCIe SerDes 以及海滨（beachfront/shoreline，即裸片边缘）面积有关。芯片的 IO 通常必须从裸片边缘引出。下面这张来自 NVIDIA 的图以卡通化的形式展示了 H100。中心是全部计算单元。上下两边 100% 留给了 HBM。从 H100 向前走到 B100，HBM 数量增至 8 颗，需要更多的海岸线面积。NVIDIA 继续用 HBM 占据其双裸片封装的两条完整边。

![](https://substack-post-media.s3.amazonaws.com/public/images/e170cc94-ccfa-4092-9855-6a5f24fcffdf_1874x1501.jpeg)
*Locuza*

剩下的两条边留给其他裸片间 IO，而这正是各标准与专有互连争夺裸片面积的地方。H100 GPU 有 3 种 IO 格式：PCIe、NVLink 和 C2C（用于连接 Grace）。NVIDIA 决定只保留最少的 16 条 PCIe 通道，因为它更偏爱后两者 NVLink 和 C2C。注意，服务器 CPU（如 AMD 的 Genoa）的 PCIe 通道多达 128 条。

这样选择的主要原因是带宽。16 通道 PCIe 接口每个方向的带宽为 64GB/s。NVIDIA 的 NVLink 到其他 GPU 每个方向带来 450 GB/s 带宽，大约高 7 倍。NVIDIA 的 C2C 与 Grace CPU 之间也是每个方向 450GB/s。说句公道话，NVIDIA 分配给 NVLink 的海滨面积要多得多，所以要把硅片面积算进等式；但即便如此，我们估计，就大量不同的 SOC 而言，NVIDIA NVLink、Google ICI 等以太网风格的 SerDes 按单位海岸线面积计算的带宽要高出 3 倍。

因此，如果你是身处带宽受限世界的芯片设计师，选择 PCIe 5.0 而不是 112G 以太网风格 SerDes，就等于把芯片做差了大约 3 倍。随着下一代 GPU 和 AI 加速器[采用 224G SerDes](https://www.semianalysis.com/p/nvidias-plans-to-crush-competition)，这一差距依然存在——与 PCIe 6.0 / CXL 3.0 相比仍保持 3 倍差距。我们身处一个焊盘受限（pad limited）的世界，把 IO 效率扔掉是疯狂的取舍。

AI 集群的主要纵向扩展与横向扩展互连将是 NVIDIA NVLink 和 Google ICI 这类专有协议，或者以太网与 InfiniBand。原因在于 [PCIe SerDes 的固有局限](https://www.semianalysis.com/i/137826061/roadmap-b-x-h-hbme-g-serdes-pcie-co-packaged-optics-optical-switch)——即便在纵向扩展形态下也是如此。由于时延目标不同，PCIe 与以太网 SerDes 对误码率（BER）的要求天差地别。

![](https://substack-post-media.s3.amazonaws.com/public/images/3796b781-3761-44dc-a77d-8bacb81b8a37_1913x800.png)
*Astera Labs*

PCIe 6 要求 BER < 1e-12，而以太网只要求 1e-4。这高达 8 个数量级的巨大差异源于 PCIe 严格的时延要求，迫使其采用极轻量的前向纠错（FEC）方案。FEC 在发送端以数字方式添加冗余的奇偶校验位/信息，接收端利用它们检测并纠正错误（比特翻转），类似内存系统中的 ECC。更重的 FEC 带来更多开销，占据了本可用于数据比特的空间。更重要的是，FEC 会给接收端增加大量时延。这就是为什么 PCIe 直到 Gen6 之前一直避免使用任何 FEC。

![](https://substack-post-media.s3.amazonaws.com/public/images/82f10c09-e16c-4951-8f86-e42363196829_2103x803.png)
*Wikipedia*

以太网风格的 SerDes 受 PCIe 严苛规范的约束要少得多，可以做到快得多、带宽高得多。因此，NVLink 的时延更高，但在大规模并行工作负载的 AI 世界里，这无伤大雅——~100ns 对 ~30ns 不值得纠结。

> 首先，MI300 AID 把大部分海滨面积给了 PCIe SerDes 而不是以太网风格 SerDes。虽然这让 AMD 在 IFIS、CXL 和 PCIe 连接方面拥有更多可配置性，但代价是总 IO 大约只有以太网风格 SerDes 的 1/3。如果 AMD 想与 NVIDIA 的 B100 有一丝竞争的希望，就必须立即在其 AI 加速器上弃用 PCIe 风格 SerDes。我们相信他们会在 MI400 上这么做。
>
> [NVIDIA 的竞争碾压计划——B100、「X100」、H200、224G SerDes、OCS、CPO、PCIe 7.0、HBM3E](https://www.semianalysis.com/p/nvidias-plans-to-crush-competition)

AMD 缺乏高质量 SerDes，这严重限制了其产品的长期竞争力。他们推出了 Open xGMI / Open Infinity Fabric / Accelerated Fabric Link，正是因为 CXL 不是适合 AI 的正确协议。它虽然主要基于 PCIe，但出于上市时间、性能、一致性和传输距离的考虑，摒弃了 PCIe 7.0 和 CXL 的一些标准特性。

![](https://substack-post-media.s3.amazonaws.com/public/images/b3db5561-633e-4f4e-ad99-9ed9e61c6d69_1200x675.jpeg)

那么，面向 AI 的 CXL 内存带宽扩展呢？超大规模云厂商自研 AI 芯片的采用情况呢？其他厂商的其他定制芯片，比如 Marvell 的 Google CXL 芯片呢？我们将回答这些问题，并审视更经典的内存池化与内存扩展用例。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
