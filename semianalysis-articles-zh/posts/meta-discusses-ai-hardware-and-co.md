---
title: "Meta 谈 AI 硬件与共封装光学"
title_en: "Meta Discusses AI Hardware and Co-packaged Optics"
subtitle: "英伟达玩的是另一场游戏"
date: 2022-09-15
source: https://newsletter.semianalysis.com/p/meta-discusses-ai-hardware-and-co
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# Meta 谈 AI 硬件与共封装光学

> 原文：[Meta Discusses AI Hardware and Co-packaged Optics](https://newsletter.semianalysis.com/p/meta-discusses-ai-hardware-and-co) · SemiAnalysis

**英伟达玩的是另一场游戏**

今天在圣克拉拉的 AI Hardware Summit 上，Meta 的 Alexis Black Bjorlin（基础设施硬件副总裁）探讨了 AI 模型扩展、训练集群和共封装光学（CPO）。她这场演讲之所以有意思，不仅在于让人得以一窥 Meta 的基础设施，还在于对未来 AI 系统的评论。在我们看来，这场演讲还表明：英伟达（Nvidia）玩的是与大多数 AI 初创公司完全不同的游戏。

我们反复讨论过的一个共同趋势是 [DRAM 扩展](https://semianalysis.substack.com/p/cxl-deep-dive-future-of-composable)与[网络扩展](https://semianalysis.substack.com/p/ayar-labs-co-packaged-optics-revolution?s=w)问题。这两个趋势是一枚硬币的两面：每一代 FLOPS 的增长速度都超过了我们[把数据送进/送出芯片或封装](https://semianalysis.substack.com/p/advanced-packaging-part-1-pad-limited)的能力。这不是什么新现象，但对抗这种失配正变得越来越难。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ab7e3b85-482b-4807-8475-db0642aca2f5_3319x1852.jpeg)

Meta 谈到了未来模型扩展面临的这些挑战。他们提到，如今一个大型训练集群的功耗可能高达 6 兆瓦（MW），并表示未来这些训练集群将达到 64 MW。而目前全球最大的公开超算功耗为 20 MW 到 30 MW。训练 AI 模型将吞噬惊人的电力，这些模型的训练成本将持续飙升。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/edbbbe89-bfd2-44d7-8c93-7850a697fb9d_3449x2092.jpeg)

Meta 给出了一个训练集群的功耗拆解。在每节点 200GB/s 带宽的加速器世代，加速器服务器占掉了大部分功耗。而从每节点 200GB/s 向前推进几个世代到每节点 1200GB/s 后，网络的功耗急剧膨胀，将吃掉 70% 以上的电力。传统的光模块和基于以太网的 fabric 将难以为继，业界必须转向带共封装光学的、面向 HPC 优化的 fabric 交换机。这些问题在 Facebook 运行的 DLRM 模型上最为突出，因为其规模庞大的扩展表（extent table）。

英伟达玩的是另一场游戏，在这里体现得再明显不过。我们此前讨论过[英伟达的共封装光学研究](https://semianalysis.substack.com/p/globalfoundries-fotonix-the-leading)。凭借[对 Ayar Labs 的战略投资与共封装光学合作](https://semianalysis.substack.com/p/ayar-labs-co-packaged-optics-revolution?s=w)，英伟达已做好准备以大多数 AI 初创公司未曾考虑过的方式来攻克这一难题。他们还与格芯（GlobalFoundries）和台积电（TSMC）[建立了合作伙伴关系](https://semianalysis.substack.com/p/ayar-labs-co-packaged-optics-revolution?s=w)，进一步探索共封装光学。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/56596887-eba5-4e0d-ad08-93b04f5c3126_1501x802.png)

英伟达构建了自有的定制 fabric，用于连接众多节点。这张网络的首要目的是内存共享、把模型分片（sharding）到多个节点，以及对在途（in-flight）数据执行 all-reduce 操作。

我们相信，英伟达将在下一代 NVSwitch 上实现共封装光学，用于节点间通信。这些系统应能在一张 NVLink 网络中互联约 4,000 颗 GPU。Meta 表示，在 2025 年及以后的时间段，每颗加速器与网络其余部分的带宽应达到 1TB/s。随着 DLRS 和 MLP 的模型规模扩展到数千亿参数，一众竞争者将很难跟上。

虽然 Graphcore IPU 和 Habana Gaudi 等其他 AI 加速器提供芯片间直连用于节点间通信、可扩展到数百乃至数千颗加速器，但大多数竞品并不具备。此外，这些竞争者中的大多数似乎也没有共封装光学或具备在途计算能力的专用交换架构的近期规划。即便这些竞争者的计算架构在保持灵活性与可编程性的同时效率高出数倍，这些公司还需要自建网络专长。

一家新贵能在软件、计算硬件和网络三条战线上同时击败英伟达吗？

如果你喜欢我们的内容，请分享！帮忙传出去！

[分享](https://newsletter.semianalysis.com/p/meta-discusses-ai-hardware-and-co?utm_source=substack&utm_medium=email&utm_content=share&action=share)

SemiAnalysis 是一家精品半导体研究与咨询公司，专注于半导体供应链——从化学原料到晶圆厂，再到设计 IP 与战略。
