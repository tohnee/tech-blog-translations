---
title: "CXL 助力 Microsoft Azure 削减数亿美元服务器资本开支"
title_en: "CXL Enables Microsoft Azure To Cut Server Capital Expenditures By Hundreds Of Millions Of Dollars"
date: 2022-07-07
source: https://newsletter.semianalysis.com/p/cxl-enables-microsoft-azure-to-cut
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# CXL 助力 Microsoft Azure 削减数亿美元服务器资本开支

> 原文：[CXL Enables Microsoft Azure To Cut Server Capital Expenditures By Hundreds Of Millions Of Dollars](https://newsletter.semianalysis.com/p/cxl-enables-microsoft-azure-to-cut) · SemiAnalysis

CXL（Compute Express Link）将是一项变革性技术，会重新定义数据中心的架构与建设方式。这是因为 CXL 为跨芯片缓存一致性、内存扩展和内存池化提供了标准化协议。本文将聚焦微软（Microsoft）披露的实践，但你可以在我们这篇关于 [Marvell 收购 Tanzanite Silicon 以及 Astera Labs 与 Rambus 在内存加速领域竞争](https://semianalysis.substack.com/p/marvell-acquires-tanzanite-silicon?s=w)的文章中了解更多细节。我们还与 [Fabricated Knowledge](https://www.fabricatedknowledge.com/p/cxl-protocol-for-heterogenous-datacenters) 合作录制了一期关于 CXL 与背面供电网络（BSPDN）的[播客](https://open.spotify.com/show/0HTOH7h5iw9ixmBxR6OQVD)，可在 [Spotify](https://open.spotify.com/show/0HTOH7h5iw9ixmBxR6OQVD)、[Apple](https://podcasts.apple.com/us/podcast/transistor-radio/id1607558815)、[Google](https://podcasts.google.com/feed/aHR0cHM6Ly9hbmNob3IuZm0vcy83Yjg2ZTU1NC9wb2RjYXN0L3Jzcw/episode/NDhmZmQxNmUtMzdjNC00ZmI4LWJkOTktMWE3ZWE4MDExZDA0?sa=X&ved=0CAUQkfYCahcKEwjIp-WLkuX4AhUAAAAAHQAAAAAQAQ) 和 [RSS](https://anchor.fm/s/7b86e554/podcast/rss) 收听。

🔗 [[嵌入内容]](https://open.spotify.com/embed/show/0HTOH7h5iw9ixmBxR6OQVD)

数据中心是一件极其烧钱的事。微软表示，其服务器成本中**高达 50% 仅来自 DRAM**。所需资本开支是巨量的，而且你用来扩容的服务器并不是一块同质化的整体。工作负载不是静态的，它们在持续增长和演进。计算资源、DRAM、NAND 和网络的比例组合会随工作负载而变化。

一刀切的模式行不通，这正是你会看到云服务商提供数十种乃至上百种不同实例类型的原因——它们试图针对不同工作负载优化硬件供给。即便如此，许多用户最终仍为他们其实并不需要的东西付费。

> 我们的结果显示，50% 的虚拟机（VM）从未触碰过其租用内存的一半。

实例的选择并不完美，实例与硬件的匹配同样如此。于是就有了平台级内存闲置（memory stranding）的问题。服务器是按悲观的实例类型场景来配置的。

> 在 Azure，我们发现 DRAM 低效的一个主要根源是平台级内存闲置（memory stranding）。当一台服务器的核心已全部租给虚拟机（VM）、但仍有内存未租出时，就发生了内存闲置。核心耗尽后，剩余的内存无法单独出租，因此被「闲置搁浅」。令人惊讶的是，我们发现**任意时刻最多可有 25% 的 DRAM 处于闲置状态**。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7329eae8-c315-421e-af1d-0f42bb6ad85c_1024x459.png)

这个问题的解决方案是内存池化（memory pooling）。多台服务器可以共享一部分内存，并动态地把它分配给不同服务器。服务器不必再按悲观方式配置，而是可以按接近平均水平的 DRAM 与核心比来供给，客户超出部分的 DRAM 需求由内存池来解决。这个内存池通过 CXL 协议通信。未来随着 CXL 协议的修订，各服务器甚至可以共享同一块内存来处理同一个工作负载，从而进一步降低 DRAM 需求。我们曾详细介绍 [Marvell、Astera Labs 和 Rambus](https://semianalysis.substack.com/p/marvell-acquires-tanzanite-silicon?s=w) 将于明年推出的、支持池化的硬件方案。

拥有大规模应用的成熟运营商，可以通过向开发者提供不同带宽和延迟的多个内存档位来解决这一问题。但对亚马逊、谷歌、微软等运营的公有云环境来说，这行不通。

> 为了实现最大的 DRAM 节约，公有云服务商更希望对以下两类对象隐藏额外延迟：(1) 绝大多数并非专家开发者的客户；(2) 不显式管理内存放置与性能的工作负载。

微软列出了公有云环境下内存池化面临的 3 大功能性挑战：客户工作负载（包括客户机操作系统 guest OS）不可修改；内存池化系统必须兼容直接 I/O 设备分配（device assignment）和 SR-IOV 等虚拟化加速技术；池化必须能在商用（commodity）硬件上实现。

过去也尝试过内存池化，但它需要定制硬件设计、修改 VM 客户机，并依赖缺页中断（page fault）。这些组合使它无法在云端部署。CXL 正是为此而来。英特尔、AMD 和多家 Arm 伙伴都已加入该标准。支持 CXL 的 CPU 将从今年晚些时候起陆续面世。此外，三星（Samsung）、美光（Micron）和 SK Hynix 三大 DRAM 厂商也都承诺支持该标准。

即便有硬件厂商的广泛支持，仍有大量问题待解。硬件层面：内存池应如何构建？如何在池规模增大带来的更高延迟与池大小之间取得平衡？软件层面：这些池如何管理并如何暴露给客户机操作系统？云上工作负载能容忍多大的额外内存延迟？调度层：服务商应如何在带 CXL 内存的机器上调度 VM？内存中哪些内容应存入池中、哪些放在直连内存？能否通过预测内存行为和延迟敏感性来获得更好性能？如果能，这些预测的准确度如何？

微软提出了这些问题，也尝试回答了它们。我们在此概述他们的发现。其第一代解决方案的架构取得了相当亮眼的结果。

> [第一代内存]解耦（disaggregation）可实现整体 DRAM 减少 9–10%，对一家大型云服务商而言相当于数亿美元的成本节约。

随着未来 CXL 版本推出、延迟进一步降低，这些收益还可以继续扩大。

首先是硬件层。微软用直接连接 8 到 32 个 CPU 插槽的多端口外部内存进行了测试。内存扩展通过 CXL 挂载的外部内存控制器（EMC）完成，EMC 拥有四个 80 位 ECC DDR5 通道的池化 DRAM，以及多条 CXL 链路以允许多个 CPU 插槽访问该内存。EMC 管理请求并跟踪分配给各主机的各内存区域的所有权。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f55a84f2-d852-46b1-8656-1fe3e0b584ab_1024x573.png)

x8 通道 CXL 的带宽大约相当于一个 DDR5 内存通道。每颗 CPU 都有自己的更快的本地内存，同时也能访问延迟更高的 CXL 池化内存，其延迟大致相当于一跳 NUMA。延迟的增加拆解开来为 67ns 到 87ns，涵盖 CXL 控制器与 PHY、可选的重定时器（retimer）、传播延迟以及外部内存控制器。

下图展示了将当前本地 DRAM 的固定比例（10%、30% 和 50%）切换为池化资源的效果。池化内存相对本地内存的占比越大，节约的 DRAM 越多。随着插槽数量增加，DRAM 节约幅度很快就趋于渐近线。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/35e9fe3e-6c62-458a-8a54-3d7ce69710bd_1024x480.png)

虽然更大的池规模和更多插槽看起来是最佳选项，但其中的性能与延迟影响也更多。如果池规模控制在 4 到 8 个 CPU 插槽，就不再需要重定时器。这能把延迟从 87ns 降到 67ns。此外，在插槽数较少的情况下，EMC 可以与所有 CPU 插槽直连。

32 插槽的大池则需要让各 EMC 连接到不同的 CPU 子集。这样可以在保持 EMC 设备到 CPU 端口数量固定的同时，实现跨更多 CPU 插槽的共享。这种场景需要重定时器，它在每个方向上贡献了 10ns 的延迟。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/fdf55f36-ad9d-4eda-94a7-d520bb445954_1024x627.png)

在软件侧，这套方案相当精巧。微软经常部署多路（multi-socket）系统。大多数情况下，VM 足够小，核心和内存可以完整地落在单个 NUMA 节点内。Azure 的 hypervisor 会尝试把所有核心和内存放在单个 NUMA 节点上，但在少数情况下（约 2% 的时间），一个 VM 会有一部分资源跨到另一个插槽。这一点不会暴露给用户。

内存池化在功能上以相同方式运作。内存设备会被呈现为一个零核心的虚拟 zNUMA 节点——没有核心，只有内存。内存分配会偏向避开这个 zNUMA 内存节点，但允许溢出（spillover）使用。粒度为每 1GB 的内存切片。

分布式系统软件层依赖对 VM 内存延迟敏感性的预测。从未被触碰的内存被称为「冷内存」（frigid memory）。Azure 估计，第 50 百分位的 VM 有 50% 的冷内存——这个数字听起来相当圆整。被预测为对内存延迟不敏感的 VM，会完全由池化 DRAM 承载。对内存敏感的 VM 则只为其冷内存配置一个 zNUMA 节点。这些预测在 VM 部署时完成，但管理是异步的，一旦检测到预测有误，就会改变 VM 的放置。

这些算法的准确性对基础设施成本节约至关重要。如果做错，性能影响可能巨大。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2b8446ac-c744-4fea-acd5-a71296431846_1024x678.png)

把云上租户的内存移到 67ns 到 87ns 之外的池里是相当危险的，因为潜在的性能影响可能巨大。

为此，微软在两种场景下对 158 个工作负载做了基准测试：一个是仅有本地 DRAM 的对照组；另一个使用模拟的 CXL 内存。需要强调的是，尽管英特尔此前声称其支持 CXL 的 Sapphire Rapids 平台将在 2021 年底发布，随后又声称 Sapphire Rapids 将在 2022 年初发布，但迄今为止并不存在任何 CXL 平台。因此微软只能模拟延迟影响。微软使用了一套 2 路 24 核 Skylake SP 系统。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/04b12e7f-a59f-4e9d-bc8d-1e72890ab42f_1024x367.png)

当带宽超过 80GB/s 时，测得内存访问延迟为 78ns。当一颗 CPU 跨 NUMA 边界访问另一颗 CPU 的内存时，会带来额外 64ns 的内存延迟。这与外部内存设备（EMC）在少插槽系统中将带来的 67ns 额外延迟非常接近。

20% 的工作负载没有受到影响。另有 23% 的工作负载性能下降不到 5%。25% 的工作负载遭遇严重减速，性能损失超过 20%，其中 12% 甚至出现超过 30% 的性能退化。这一比例会随工作负载的本地内存与池化内存配比不同而有很大变化。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/05f0a80f-cdd9-4d1b-8976-461880189b33_1024x668.png)

这进一步凸显了预测模型的重要性。微软基于随机森林机器学习的预测模型更准确，产生的假阳性减速更少。随着更多内存被池化，这个模型的重要性只增不减。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/0742fbf3-fafd-43b3-acb1-7148beaec12e_1024x363.png)
> 我们的结果显示，第一代内存解耦可将所需 DRAM 总量减少 9-10%。这相当于云服务器成本整体降低 4-5%。

随着 CXL 规范改进、延迟降低、预测模型完善，内存池化带来的节约有望增长到云服务器成本的两位数百分比。推荐阅读这篇[论文](https://arxiv.org/pdf/2203.00241.pdf)，其中包含比本文更多的细节。

[发表评论](https://newsletter.semianalysis.com/p/cxl-enables-microsoft-azure-to-cut/comments)

[分享](https://newsletter.semianalysis.com/p/cxl-enables-microsoft-azure-to-cut?utm_source=substack&utm_medium=email&utm_content=share&action=share)
