---
title: "Ventana RISC-V CPU 击败下一代 Intel Sapphire Rapids！——13 家 RISC-V 公司、CPU 与生态全景"
title_en: "Ventana RISC-V CPUs Beating Next Generation Intel Sapphire Rapids! – Overview of 13 RISC-V Companies, CPUs, and Ecosystem"
subtitle: "SiFive、Tenstorrent、Rivos、Codasip、Akeana、Alibaba、Imagination、Western Digital、Andes、Krakatoa、MIPS、XMOS 与 Ventana"
date: 2022-12-26
source: https://newsletter.semianalysis.com/p/ventana-risc-v-cpus-beating-next
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Ventana RISC-V CPU 击败下一代 Intel Sapphire Rapids！——13 家 RISC-V 公司、CPU 与生态全景

> 原文：[Ventana RISC-V CPUs Beating Next Generation Intel Sapphire Rapids! – Overview of 13 RISC-V Companies, CPUs, and Ecosystem](https://newsletter.semianalysis.com/p/ventana-risc-v-cpus-beating-next) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**SiFive、Tenstorrent、Rivos、Codasip、Akeana、Alibaba、Imagination、Western Digital、Andes、Krakatoa、MIPS、XMOS 与 Ventana**

上周我们参加了在圣何塞举办的 RISC-V 峰会。RISC-V 生态的发展动能正在越来越快地加速。过去几年里，嵌入式世界已累计出货数百亿颗 RISC-V 核心。高通（Qualcomm）自 2020 年的 S865 芯片起，已悄然将不对用户暴露的控制与安全核心切换为 RISC-V。这使他们累计出货了 6.5 亿颗 RISC-V 核心！Andes 和 Codasip 各自的 RISC-V 核心出货量都超过 20 亿颗，Western Digital 每年出货超过 10 亿颗 RISC-V 核心，甚至连 [Apple 也在把一些非面向用户的功能转向 RISC-V](https://www.semianalysis.com/p/sifive-powers-google-tpu-nasa-tenstorrent)！Google 还宣布 [Android 已可在 RISC-V 上运行](https://twitter.com/dylan522p/status/1603087270730502150?s=20&t=i-fe2L-bBvAPm0f-4RWfEA)，一线厂商推出基于 RISC-V 的手机将比大多数人预期的更早。

Arm 的软肋正遭到来自 SiFive、Codasip、Alibaba、Imagination、Western Digital、Andes、XMOS 和 MIPS 的 RISC-V 核心的极速攻击。到 2024 或 2025 年，RISC-V 将在嵌入式和微控制器领域超越 Arm。在本报告更后面的部分，我们还将分享一些关于 [Arm「核弹级选项」](https://www.semianalysis.com/p/arms-nuclear-option-qualcomm-must)——即对现有被授权方进行强制捆绑——的惊人细节。

所有人心中最大的问题是：RISC-V 何时进入面向用户的应用？答案是：这可能比人们预期的更近。目前有 4 家公司在研发大型 RISC-V 核心，与 Intel、AMD、Arm、Apple 等厂商最大最快的核心同场竞技。这 4 家公司是 Ventana Micro Systems、Tenstorrent、Rivos 和 Akeana。这几家公司的团队履历都令人印象深刻，但光有履历并不能保证成功。

本报告将涵盖上述 13 家公司的努力和/或核心概览。我们将聚焦上市策略（go-to-market）这类高层事项，以及与核心相关的底层细节。在能获取数据的情况下，核心概览将涵盖 ISA 等级、流水线级数、顺序执行 vs. 乱序执行、发射宽度（issue #）、特权模式、SMP/SMT 支持、TCM 指令/数据、TCM 大小、I$、D$、L2、L3 和 MMU。

## **Ventana Micro Systems**

Ventana 或许是最令人印象深刻的一家，无论是团队、上市策略还是性能。他们也是距离商业化产品最近的。Ventana 表示其核心瞄准从数据中心、汽车、5G 边缘、AI 乃至客户端的一切市场，但我们认为，至少对第一代而言，最具优势的价值主张将落在数据中心、网络和 5G DU/RU。

Ventana 的团队在业内拥有悠久而传奇的历史，包括打造了第一颗 64 位 Arm 核心。这支队伍的很大一部分经历了 Veloce、Applied Micro、Macom 再到 Ampere Computing 的传承。Ventana 累计融资 $108M，拥有足以支撑到第二代 CPU 的资金跑道。

开门见山地说：Ventana 的 Veyron VT1 单核性能与 Arm 的 Neoverse V 系列（[Amazon Graviton 3](https://www.semianalysis.com/p/amazon-graviton-3-uses-chiplets-and) 中的 V1 和 [Nvidia Grace](https://www.semianalysis.com/p/meta-discusses-ai-hardware-and-co) 中的 V2）相当，但频率更高。此外，它可在 300W 功耗包络内扩展到 128 核。这与 [AMD Genoa 所能达到的性能](https://www.semianalysis.com/p/amd-genoa-detailed-architecture-makes)相当。Ventana 还能实现 Amazon Graviton 3 两倍的核心数，尽管功耗更高。

另一个重要区别是：AMD Genoa 和 Graviton 3 都是硅片实测数据，且已可交付客户。Ventana 的性能数据是仿真结果，实际测试要等到第一季度流片之后。关于新产品发布，我们的一贯看法是：硅片进实验室之前一切都只是空谈。假设这些第一方数据哪怕有 20% 的偏差，Ventana 仍将碾压 Intel 当前一代的 Ice Lake，甚至击败 Intel 下一代的 Sapphire Rapids——后者要到 2023 年年中才能大批量出货。

在进入技术细节之前，我们想先强调其上市策略的强项。Ventana 并非只瞄准拥挤不堪、平淡无奇的通用 CPU 市场。Ventana 做的是 CPU 小芯片（chiplet），既可以集成进通用 CPU 市场，也可以用于各种异构计算场景。此外，Ventana 不亲自做 IO Die，而是与相关公司合作。这解锁了一种截然不同的集成与合伙策略。IO die 既可以从现有供应商那里直接采购现货，也可以用大部分为授权 IP 的 IO 和 NOC IP 低成本自研。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e306ed89-017f-423f-a28e-d471fbff1114_4000x2250.png)

客户可以专注于自己的用例和领域专用加速器。这些领域专用加速器可以直接集成在 IO die 上，也可以开发成独立的 chiplet。这一策略对超大规模云厂商市场可能非常有效，因为那正是他们想要的商业模式。

Amazon、Microsoft、Google、Meta、Alibaba、腾讯、百度这样的公司不喜欢被供应商的层层加价牵着鼻子走。他们想要掌控权，想在自己的产品中垂直整合更多环节。

并非每个超大规模云厂商和 ASIC 项目都需要重新发明轮子。他们可以以远低于完整封装 CPU 的成本购买并集成高性能 CPU chiplet。而且，在异构计算和定制设计方面，CPU chiplet 设计能让他们把加速器与 CPU 之间的功耗和延迟保持在最低。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ec6aacc3-dccd-4132-9442-fbe79189f38c_4147x2348.png)

一个 IO die 可以在台积电（TSMC）16nm 上开发并流片，成本约 $20M。一个台积电 7nm 的 IO Die 设计加流片约需 $30M。这个 IO die 可以从几个内存控制器和少量 PCIe 端口起步，一直扩展到海量的 IO 和网络。考虑到超大规模云厂商的用量，通过在 IO die 上集成或以 chiplet 形式挂接精确配比的高性能 CPU 与专用 ASIC 来打造一款新处理器，其增量成本相对很低。

这一商业模式可以延伸到 5G ORAN 的 DU 和 RU 处理器、边缘 AI、边缘网关、内存数据库、应用/Web 托管、存储服务器、负载均衡器、缓存设备、内容分发网络等领域。随着[摩尔定律步履蹒跚](https://www.semianalysis.com/p/tsmcs-3nm-conundrum-does-it-even)、工作负载越来越依赖处理器专门化，除非采取开放的 chiplet 路线，领域专用加速器的工程成本将一路飙升。

Ventana 采用开放计算项目（Open Compute Project）的 ODSA BOW 标准进行封装。我们知道在这一标准下，至少有 4 种不同的计算类 chiplet 和至少 3 种不同的 IO 相关 chiplet 正在开发之中。虽然长远来看 UCIe 会是赢家，但在 2023 和 2024 年，BOW 在短期内会更普及。Ventana 计划让未来版本同时支持 BOW 或 UCIe。这些 chiplet / IO Die 全部使用 AMBA CHI 协议，其延迟和功耗都远低于 [UCIe 之上的 CXL](https://www.semianalysis.com/p/cxl-deep-dive-future-of-composable)。

虽然 AMD 确实拥有 chiplet CPU 架构和定制芯片业务，但他们不使用开放协议。而且，AMD 不愿意只向超大规模云厂商出售 CPU chiplet。AMD 想在任何定制芯片交易中掌控从硅片设计到封装的整个垂直栈。这一策略带来更多的层层加价和更高的定价。AMD 的选择对其自身的商业模式而言说得通，但也给了超大规模云厂商将其解耦（disaggregate）的机会。Intel 的商业模式会走与 AMD 相同的路线，但其架构要到 2025 年才能支持这种程度的解耦。

归根结底，Ventana 最强的卖点是把定制硅片的增量成本从如今的数亿美元降至数千万美元。当超大规模云厂商只从无厂设计公司购买部分 chiplet、其余硅片直接向代工厂下单时，针对特定工作负载的每个已部署封装的增量成本将显著降低。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b6fcc8db-9f12-4d12-9346-739d8ba25bd8_4000x2250.png)

核心本身相当令人印象深刻。这是一个 8 宽度的乱序执行核心，带有高达 512KB 的指令缓存。每个核心配备 3MB 的 L3 缓存切片，不过在后续版本中这很容易重新配置。核心的设计目标相当简单却难以达成：最大化单线程性能、最大化核心密度、跨核高效扩展、跨核可预测的低延迟。值得注意的是，VT1 不含 RISC-V 向量扩展，因为向量扩展的批准时间太晚，赶不上设计周期。随后较快速跟进的 VT2 将包含 RISC-V 向量扩展。

Ventana 开发的 chiplet 最多可扩展到 16 核。人们大概会以为一个带有 16 个大高性能 CPU 核的 chiplet 裸片会很大，但这或许正是 Ventana 方案最惊艳之处：该 chiplet 在台积电 N5 工艺上仅 62mm^2。对比 [AMD 在 N5 上的 8 核 Zen 4 chiplet](https://www.semianalysis.com/p/amd-genoa-detailed-architecture-makes)——它比 Ventana 的 16 核 chiplet 还要大。

经济账令人印象深刻。Ventana 在设计 CPU 时还考虑了跨制程节点移植的便利性。例如，Ventana 与 Intel 的 IFS 加速器项目建立了合作，我们相信他们将在 Intel 的 3 或 18A 工艺上流片 VT2。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d5df7dd7-08c7-49a3-8f75-dffe8a4c9204_3954x2830.jpeg)

上图展示了为 Ventana VT1 设计的多种封装之一。这个特定的 IO Die 集成了大量网络能力，如以太网、包处理，以及面向 DPU 的 [CXL 2.0](https://www.semianalysis.com/p/cxl-deep-dive-future-of-composable)。Ventana 在这个 IO Die 与 CPU 的裸片间互连上使用 BoW，每个方向达 1Tbps。该链路从 PHY 到 PHY 连接的延迟低于 2ns，在 IO die 与 CPU 核心 chiplet 之间传输的能耗为 <0.5pj/bit。

与 Intel 的 Sapphire Rapids 相比，这是[更低的延迟（<2ns vs. 2.4ns）和更低的功耗（<0.5pj/bit vs. 0.5pj/bit）](https://twitter.com/dylan522p/status/1560861377589399554?s=20&t=ra8zXMl1TzusEnn366DYNw)；与 AMD 的 Zen 4 相比，这是更低的延迟和[低得多的功耗（<0.5pj/bit vs. <2pj/bit）](https://www.semianalysis.com/p/amd-genoa-detailed-architecture-makes)。Ventana 的 chiplet 封装采用[标准 8-2-8 有机基板](https://www.semianalysis.com/p/the-future-of-packaging-gets-blurry)和 [130um 微凸点](https://www.semianalysis.com/p/advanced-packaging-part-1-pad-limited)，而 Intel 为了达到同等效果，不得不使用[其更昂贵的 EMIB 先进封装](https://semianalysis.substack.com/p/advanced-packaging-part-2-review)和 [55um 微凸点](https://www.semianalysis.com/p/advanced-packaging-part-2-review)。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/89c81507-fd4a-4e98-a48d-fc6bb34894d8_4000x2250.png)

有了正确的上市策略和令人印象深刻的性能，Ventana 有望成功，但软件叙事也是这场讨论的重要组成部分。Arm 从宣布进军服务器到实现大规模部署用了十年。RISC-V 所需的时间会短得多，因为系统和软件对架构切换的准备度已大幅提高，但这仍是一大顾虑。Ventana 对此与其他任何人一样心知肚明——团队中的许多成员从第一颗 64 位 Arm 核心一路走来，并经由其后身 Ampere Computing 亲历过这些成长的阵痛。

Ventana 声称已为许多应用准备了大量现成软件，尤其是在底层、存储和网络应用方面。在没有自家硅片的情况下，Ventana 一直借助具有 ISA 兼容性的 SiFive 开发板来推进软件开发。从这个意义上说，将服务器软件生态带到 RISC-V 的挑战在 3 年前就已经开始。如果 Arm 花了 10 年，而 RISC-V 按加速时间表只需一半时间，那么可能我们距离 RISC-V 进入数据中心只有几年之遥。

当然，那是乐观的看法。我们预计 5G ORAN、网络和超大规模云厂商的内部工作负载可能会更早实现跳转，但通用多租户云实例则遥远得多。搭载 Ventana CPU chiplet 的开发套件将于明年年中上市，明年晚些时候批量出货。

接下来，我们将比较领先的 RISC-V 公司。这些公司是 Ventana、SiFive、Tenstorrent、Rivos、Codasip、Akeana、Alibaba、Imagination、Western Digital、Andes、MIPS、XMOS 和 Krakatoa。它们都在设计 RISC-V 核心。其中四家甚至瞄准了在单线程性能上与 AMD 和 Intel 服务器级核心正面竞争的超高性能核心。内容包括对各自战略与公司的概览。我们还将分享一些关于 [Arm 反竞争性捆绑](https://www.semianalysis.com/p/arms-nuclear-option-qualcomm-must)的惊人细节。

报告末尾还会附上一张技术规格表，包括 ISA 等级、流水线级数、顺序 vs. 乱序、发射宽度、特权模式、SMP/SMT 支持、TCM 指令/数据、TCM 大小、I$、D$、L2、L3 和 MMU。

[获取团体订阅 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

## **SiFive**

SiFive 是 RISC-V 领域最知名、最成功的公司。他们已经以 $175M 将一个业务部门出售给了 AlphaWave。SiFive 拥有令人印象深刻的估值和充足的资金跑道。他们的身影无处不在——[从下一代 TPU 到 NASA 的可扩展太空 chiplet](https://www.semianalysis.com/p/sifive-powers-google-tpu-nasa-tenstorrent)。可以说，SiFive 拥有海量核心，而[最令我们兴奋的是 X280](https://www.semianalysis.com/p/sifive-powers-google-tpu-nasa-tenstorrent)。我们*只*会把 X280、P470 和 P670 放入下文的核心对比表。尽管运营相当精简，SiFive 那一众不同的 CPU 核心仍在持续更新。这得益于他们对 Chisel 的使用。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d51edef2-f2f1-4fec-a322-d648e76c14f7_1762x716.png)

Chisel 是一种用于设计 CPU 的硬件设计语言。这是一门相对较新的语言，其全部目标就是让硬件工程师既能快速创建复杂设计，又仍能实现高性能。Chisel 用一种类 Scala 的中间语言编写，生成基于 Verilog 的数字电路寄存器传输级（RTL）描述。从这里开始，流程与其他任何芯片设计流程类似：Verilog 被综合为更低层的门级描述；门级描述随后用于创建电路的物理版图并制造实际芯片。

许多经典 CPU 架构师对 Chisel 有意见，抱怨其性能不足、时序收敛困难和调试困难。他们还表示，解决任何时序或调试问题都需要多轮综合，回到高级语言修改，然后循环往复。我们不够精通，无法评判其中的细微差别；从高层看，问题在于：人们是否还应像 20 年前那样设计硬件，还是应当做出某种重大变革。

高级语言与低级语言的利弊之争在软件世界早已上演多时。SiFive 正把这场争论推到硬件世界的聚光灯下。

[分享](https://newsletter.semianalysis.com/p/ventana-risc-v-cpus-beating-next?utm_source=substack&utm_medium=email&utm_content=share&action=share)
