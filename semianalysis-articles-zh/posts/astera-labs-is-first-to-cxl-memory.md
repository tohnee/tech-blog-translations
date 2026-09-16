---
title: "Astera Labs 率先推出 CXL 内存池化芯片——击败 Marvell、Rambus、Microchip 与澜起科技"
title_en: "Astera Labs Is First To CXL Memory Pooling Silicon – Beating Marvell, Rambus, Microchip, and Montage Technologies"
subtitle: "Astera Labs Leo 拥有功能与上市时间双重优势"
date: 2022-08-30
source: https://newsletter.semianalysis.com/p/astera-labs-is-first-to-cxl-memory
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# Astera Labs 率先推出 CXL 内存池化芯片——击败 Marvell、Rambus、Microchip 与澜起科技

> 原文：[Astera Labs Is First To CXL Memory Pooling Silicon – Beating Marvell, Rambus, Microchip, and Montage Technologies](https://newsletter.semianalysis.com/p/astera-labs-is-first-to-cxl-memory) · SemiAnalysis

**Astera Labs Leo 拥有功能与上市时间双重优势。**

CXL 将通过[可组合服务器架构](https://semianalysis.substack.com/p/cxl-deep-dive-future-of-composable)和[异构计算](https://semianalysis.substack.com/p/cxl-deep-dive-future-of-composable)变革数据中心。我们最近做了一次[对 CXL 标准的深度解析，梳理了 20 家公司在 CXL 上的产品、时间表与战略](https://semianalysis.substack.com/p/cxl-deep-dive-future-of-composable)，涵盖交换机、NIC、DPU、IPU、共封装光学、内存扩展器、内存池化器、内存共享器、CPU、GPU 和加速器。未来几年，这些产品中最重要的品类将与内存相关，因为[服务器成本的 50% 仅来自 DRAM](https://semianalysis.substack.com/p/cxl-enables-microsoft-azure-to-cut)。

> [第一代内存]解耦（disaggregation）可实现整体 DRAM 用量降低 9 – 10%，对一家大型云厂商而言这意味着数亿美元的成本节约。
>
> > —— [微软](https://semianalysis.substack.com/p/cxl-enables-microsoft-azure-to-cut)

随着各大云厂商争相在数据中心内部署内存池化以提高内存利用率、降低成本，内存解耦硬件的主要供应商将获益巨大。SemiAnalysis 认为，基于 CXL 的内存扩展与内存池化硬件市场在 2025 年将超过 10 亿美元。业界对此心知肚明，因此这是一个异常拥挤的赛道。三星（Samsung）、美光（Micron）和 SK 海力士（SK Hynix）都在开发内存扩展硬件。此外，Rambus、Microchip、澜起科技（Montage Technologies）、Marvell 和 Astera Labs 也都在开发内存扩展与池化 ASIC。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8ffdd69e-7873-410c-9775-fc1c0eb65ae0_1501x852.png)

玩家这么多，最终只会诞生少数赢家和大量输家。[在我们此前解释 Marvell 为何收购 Tanzanite Silicon 的报告中](https://semianalysis.substack.com/p/marvell-acquires-tanzanite-silicon?s=w)，我们也评估了 Astera Labs 的硬件进展。

> Astera Labs（的 CXL 内存池化产品）会更早上市。他们迄今的成功，是作为 PCIe 5.0/CXL 唯一大量出货的智能重定时器（retimer）。我们相信他们的 CXL 内存加速器已流片，代号 Leo。Astera Labs 应能在明年年初出货。我们认为它将成为 2023 年出货量最大的 CXL 内存加速器。
>
> > —— [《Marvell 收购 Tanzanite Silicon，以基于 CXL 的内存扩展与池化实现可组合服务器架构》](https://semianalysis.substack.com/p/marvell-acquires-tanzanite-silicon?s=w)

我们坚持此前报告的判断，并希望结合今天 Leo 内存连接平台的官方发布做进一步展开。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/832a922f-782f-4817-a39e-e69b8efa39b3_1521x852.png)

Astera Labs 宣布已向多家客户送样 Leo 扩展与池化芯片。相比之下，其他公司才刚开始点亮其内存池化器件，或仍在基于 FPGA 的实现上打转。Astera Labs 表示其 CXL 控制器已进入第三代，而别人还在第一代上努力。

Astera Labs 在 2019 年就有了一颗测试用 CXL 芯片。去年他们批量出货了智能重定时器。内存扩展与池化器件 Leo 是第三代。Astera Labs 2021 年营收约 ~$35M，2022 年预计超过 $100M。Leo 很可能为 Astera Labs 攻下多个设计导入（design win），使其得以延续这一惊人的增长步伐。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/58cea2b4-193f-4f04-b4a5-c12203548c7c_1518x847.png)

Astera Labs 表示，他们已用 Leo 搭载业界领先的 CPU/GPU 平台和 DRAM 内存模组，在各类真实工作负载下完成了端到端互操作性测试。我们相信这些平台是 AMD 的 Genoa/Bergamo 和英特尔的 Sapphire Rapids。Leo 芯片支持 ECC 以及服务器级、可定制的可靠性、可用性与可服务性（RAS）能力。[额外延迟对性能的影响可能非常大](https://semianalysis.substack.com/p/cxl-enables-microsoft-azure-to-cut)，因此 Astera Labs 把 Leo 智能内存控制器的重心放在延迟上是对的。

Leo 最关键的功能，是可以在 CXL 1.1 平台上实现内存池化。Marvell 的 Tanzanite Silicon 方案同样支持在 CXL 1.1 上做内存池化。

> （Marvell 方案）有一些缺陷。每当内存池容量发生变化时，主机都需要重启，这在云 VM 环境下不可接受，但在高性能计算环境中没有问题。
>
> > —— [《CXL 深度解析——可组合服务器架构与异构计算的未来、20 家公司的产品、3.0 标准概览》](https://semianalysis.substack.com/p/cxl-deep-dive-future-of-composable)

Astera Labs Leo 无需重启主机 CPU 即可动态调整池容量。这使得内存池化在最重要的市场——多租户云——成为可能。在这一支持层级上，Astera Labs 的方案定位独特、优势明显。

软件同样重要，Astera Labs 在这方面投入很大。他们开发了丰富的遥测功能与面向集群管理的软件 API，便于在云平台上大规模管理、调试和部署。这些用原生 Linux 驱动即可完成。

Leo 支持 2TB 内存。它可以使用 DDR4，或每内存通道最高 DDR5 5600MT/s——这是喂满 CXL 1.1 和 CXL 2.0 带宽所必需的。除支持 JEDEC 标准 DDR 接口外，Leo 还支持「其他内存厂商专用接口」。我们不确定这些厂商专用接口会是什么，但[DRAM 封装很可能正在开发一种新的外形规格。](https://www.businesswire.com/news/home/20220824005210/en/CXL%E2%84%A2-Consortium-and-JEDEC%C2%AE-Sign-MOU-Agreement-to-Advance-DRAM-and-Persistent-Memory-Technology)

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/97a28e1a-1bf7-406b-a57b-722bc63e67f6_1512x848.png)

Astera Leo 分为 E 和 P 两条产品线。E 仅用于扩展，P 用于池化与共享。从 SKU 看，E 系列的 CM5082E 配备 x8 PCIe 通道，而 CM5162P 和 CM5162E 配备 x16 PCIe 通道。我们判断背后是两颗不同的芯片：一颗 8 通道内存扩展器，以及一颗 16 通道内存扩展/池化器。

16 通道平台看起来更具吸引力，因为可以连接多颗 CPU 来实现内存池化。在搭配英特尔 Sapphire Rapids 做内存扩展时它也占优势。原因在于英特尔在 Sapphire Rapids 上存在 CXL 通道 bifurcation（通道拆分）问题，意味着一个 8 通道 CXL 器件仍会占掉整个 16 通道 CXL 端口。这个问题将在 Emerald Rapids 上解决。

总体而言，AMD 的 Genoa 和 Bergamo 将是内存池化的首选系统。因为它们支持 CXL 通道拆分，而且尽管官方支持等级是 CXL 1.1，却具备 CXL 2.0 的部分内存池化特性。在内存扩展模式下，8 通道芯片反而占优，因为纯扩展器的数据通路更简化，延迟略低。

> CXL 被设计为一个开放标准接口，支持可扩展与共享内存资源的可组合内存基础设施，为现代数据中心带来更高效率。我们很高兴与 Astera Labs 紧密合作开发其 Leo 内存连接平台，实现与 AMD 处理器及**加速器**的互操作性和稳健验证。
>
> > —— Raghu Nambiar，AMD 公司副总裁，数据中心生态系统与解决方案

发布内容中包含 AMD 的这段话。其中「加速器」一词的登场耐人寻味，因为它暗示 FPGA 或 [MI300](https://semianalysis.substack.com/p/amd-to-infinity-and-beyond) 也可能支持 Leo 的内存池化。

相对 Rambus、Microchip、澜起科技和 Marvell 的竞品内存扩展与池化 ASIC，Astera Labs Leo 拥有功能与上市时间的双重优势。在内存扩展器市场，凭借公开市场芯片（merchant silicon）的商业模式，Astera Labs 对阵 SK 海力士、美光和三星同样占优。超大规模云厂商更愿意购买商用 ASIC 再搭配大宗 DRAM，而不是采购内存厂商直供的更昂贵扩展器。我们估算 DRAM 扩展与池化市场 2025 年将超过 10 亿美元，而 Astera Labs 有望成为商用 ASIC 细分市场的领导者。

如果你喜欢我们的内容，请分享！帮忙传出去！

[分享](https://newsletter.semianalysis.com/p/astera-labs-is-first-to-cxl-memory?utm_source=substack&utm_medium=email&utm_content=share&action=share)

SemiAnalysis 是一家精品半导体研究与咨询公司，专注于半导体供应链——从化学原料到晶圆厂，再到设计 IP 与战略。
