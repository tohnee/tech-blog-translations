---
title: "Ampere Computing 的「云原生」是营销噱头吗？——Siryn、Ampere One 5nm 架构、成本分析与 IPO 分析"
title_en: "Is Ampere Computing's Cloud Native Marketing Fluff? – Siryn Ampere One 5nm Architecture, Cost Analysis, and IPO Analysis"
date: 2022-06-01
source: https://newsletter.semianalysis.com/p/is-ampere-computings-cloud-native
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Ampere Computing 的「云原生」是营销噱头吗？——Siryn、Ampere One 5nm 架构、成本分析与 IPO 分析

> 原文：[Is Ampere Computing's Cloud Native Marketing Fluff? – Siryn Ampere One 5nm Architecture, Cost Analysis, and IPO Analysis](https://newsletter.semianalysis.com/p/is-ampere-computings-cloud-native) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

本文将讨论 Ampere Computing 及其「云原生（Cloud Native）」CPU。SemiAnalysis 经常被问到：这到底只是营销话术，还是这几个字背后确有实质内容？因此本文可以视为对其优点与不足的一次解释。我们将把当代 Ampere Altra 和 Altra Max 与英特尔（Intel）的 Ice Lake、AMD 的 Milan 服务器平台做成本对比，还会推测下一代 Ampere One、Intel Sapphire Rapids 与 AMD Genoa 在成本层面可能呈现的格局。我们也会谈谈对即将到来的 IPO 的看法。

最后，我们还会讨论他们基于 5nm 的自研 Ampere One 架构，它将用于代号「Siryn」的服务器芯片。虽然我们不知道这些下一代 CPU 的性能，但通过 [GitHub 上的 LLVM 代码](https://github.com/llvm/llvm-project/blob/64816e68f4419a9e14c23be8aa96fa412bed7e12/llvm/lib/Target/AArch64/AArch64SchedAmpere1.td)可以获取相当多的数据。在 [Cardyak](https://twitter.com/Cardyak) 的帮助下，我们得以深挖并确定其中一些架构细节，甚至绘制了可与其他 Arm 核心对照的架构图。如果你更喜欢看视频听讲解，这里还有一个 [YouTube 视频](https://youtu.be/qyt92qmrYV8)。

# **云原生——是营销噱头吗？**

Ampere Computing 在年度路线图与战略更新中对细节相当吝啬，所以我们想解释一下其产品背后的基本趋势。Ampere 把自己的总体战略浓缩成两个词：「云原生（Cloud Native）」。AMD 和英特尔必须让他们的 CPU 面向从企业到云计算的各种工作负载，从存储服务器、Web 服务器到搭载加速器的 AI 系统无所不包。这些 AMD 和英特尔的 CPU 核心只需少量修改也能用于客户端计算。Ampere 声称，他们可以聚焦数据中心中增长最快的部分——云——并为其专门优化产品。他们相信，计算的未来将高度依赖微服务、容器化和[无服务器（serverless）执行](https://en.wikipedia.org/wiki/Serverless_computing)模式。这些概念大体上是指通过大量小任务和小进程横向扩展性能，突破单线程 CPU 性能的边界。Ampere 给出了其 CPU「云原生」的 3 个主要体现：

1. 单颗 CPU 更高的性能
2. 可预测的性能
3. 可扩展性

下面拆解他们的架构是如何实现这些的。Ampere Computing 依靠更高的核心数来实现更高的性能，而更高的核心数靠的是采用比英特尔和 AMD 更小的核心。在单线程性能尤其是浮点性能方面，Ampere 的核心落后于 AMD 和英特尔。这些核心绝不算弱，但许多工作负载确实高度依赖单线程性能，而英特尔和 AMD 以更高的晶体管数量和每核心硅面积为代价提供了这种性能。

Ampere Computing 还通过每核只跑 1 个线程来提供更可预测的性能。英特尔和 AMD 每核提供 2 个线程，即同步多线程（[SMT](https://en.wikipedia.org/wiki/Simultaneous_multithreading)），这可能导致性能不可预测。Ampere Computing 还认为，摒弃 SMT 能让他们的 CPU 更可扩展、更安全。利用 SMT 漏洞是[侧信道攻击](https://en.wikipedia.org/wiki/Side-channel_attack)的常见手段，而自 [Spectre](https://en.wikipedia.org/wiki/Spectre_(security_vulnerability)) 和 [Meltdown](https://en.wikipedia.org/wiki/Meltdown_(security_vulnerability)) 问世以来，这类攻击大爆发。当然 SMT 并非纯粹的负面。它利用工作负载中的空隙（主要来自等待内存），让硬件执行资源的利用率更高。SMT 在几乎不增加每核硅面积和晶体管数的情况下提升性能。这种性能可预测性也延伸到 Ampere 的缓存架构：每个核心有更大的私有 L2 缓存，而共享 L3 缓存相对很小。AMD 和英特尔依赖更大的共享 L3 缓存，这在许多工作负载中有帮助，但也会损害性能的可预测性。

Ampere Computing 还非常强调把频率维持在固定水平，而不是伺机加速。英特尔和 AMD 的 CPU 会根据正在使用的核心/线程数以及正在执行的代码类型大幅调整核心频率，这有助于其 CPU 在给定的功耗与散热预算内最大化性能，在许多工作负载中是巨大优势。Ampere Computing 无视这一点、坚守固定频率，以此提升性能的可预测性——他们认为这才是「云原生」CPU 最合理的选择。

云原生 CPU 的策略正在被英特尔和 AMD 效仿，对应其即将推出的 Sierra Forest 和 Bergamo 产品架构。两者都被描述为面向云工作负载，但这些平台问世的时间不会像 Ampere 下一代那样快。

# **成本对比**

总体而言，更小、更简单的核心以及缺少 SMT 和加速频率等技术，缩短了设计与验证周期，从而降低 Ampere Computing 的设计成本。对 SemiAnalysis 而言，核心尺寸的论据最为重要。80 核 Ampere Altra 裸片估计约 ~574mm²，128 核 Altra Max 估计约 ~650mm²。这比 AMD 的 64 核 Milan 或英特尔的 40 核 Ice Lake 用的硅少得多。

下面用制造成本对比来演示。下表包含大量假设，包括晶圆成本、良率，而且完全没有考虑裸片收割（die harvesting）。所谓裸片收割，是指有缺陷的裸片仍可通过削减核心数或其他能力来出售。参数良率（parametric yield）也未计入。这对英特尔尤其重要，因为他们卖的裸片最大，而且相对 AMD 和 Ampere 所依赖的台积电制程节点良率更低。英特尔还生产图中未展示的更小的 28 核 HCC 裸片。与小芯片（chiplet）方案相关的分级（binning）优势、以及各 SKU 更宽松的频率目标也未计入。尽管与 AMD 使用同一制程节点，考虑到出货量差异，假设 Ampere 的晶圆成本比 AMD 高 10%。向 IP 供应商支付的授权费也未计入。还有许多固定的设计与流片成本（例如光罩）没有考虑。请把这当作演示性示例，而非事实。我们用更精确的数字做过更高级的成本分析，其中计入了上述部分项目，但那种模型的解释成本远超本文这种体裁所能容纳。最后，服务器 TCO 还受纯 CPU 成本之外许多其他因素的影响，所以这只是拼图的一角。

编者按：Ampere Altra 的实际裸片面积后来公布。我们最初的估算有误，下表已用正确数字更新。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/eec820b5-a18e-4fe3-a008-5cf96a074d8f_1445x610.png)

Ampere 的每核心成本更低。对比 AMD 接近每核心成本的一半，对比英特尔的差距更大。这是 Ampere 所选核心架构的天然优势。Ampere 靠的是小核心、小 L3 缓存的组合，并通过在每个 mesh 停靠点放 2 个 DSU、每个 DSU 放 2 个核心来缩减互连（fabric）面积。当代产品使用 Arm 的 N1 核心。性能不能忽视，Ampere 芯片在许多基准测试中的表现明显逊色。话虽如此，当工作负载由大量互不相关的独立任务构成时，Ampere 往往性能高得多，甚至击败 AMD 的 Milan。推荐阅读我们的朋友 [ServeTheHome 的评测](https://www.servethehome.com/ampere-altra-wiwynn-mt-jade-server-review-the-most-significant-arm-server/)。

# **路线图与现有战果**

Ampere Computing 的 Siryn 芯片将基于自研的 Ampere One 核心架构，还将采用 DDR5 和 PCIe5。架构仍是单片式，不使用小芯片。

在下一代产品发布会上，Renee James 有一句很有意思的话：

> 我们会有两个产品家族。它们并存共生，各自面向不同的工作负载、市场细分和应用场景，拥有不同的特性与性能。比如我们面向边缘场景的 32 核 40 瓦产品。
>
> Renee James，Ampere Computing 联合创始人兼 CEO ——[引言来源](https://www.youtube.com/watch?v=rxPt7bpXGSk)

尽管云原生造势不断，Ampere 却在意想不到的地方收获了另一个设计导入。通用汽车（GM）旗下的 Cruise 自动驾驶部门实际使用的是一款 32 核、40W 功耗包络的 Ampere Altra 变体。这相当奇怪，但用例说得通。Cruise 硬件工程副总裁 Carl Jenkins 表示，这是因为他们需要处理各种不同来源的传感器数据。Ampere 的 Altra 是唯一能在低功耗下提供所需 CPU 吞吐量的 CPU。

> 客户可以在我们所有 Ampere 处理器之间无缝迁移工作负载。而且我们推出新品时，不会让既定路线图过时。在消费电子行业，新品会让上一代过时。Ampere 的云原生路线图不是这样。Ampere Altra 80 核和 Altra Max 128 核是客户设计的主力。与此同时，同样的客户还在增加新的 Ampere One 5nm 产品，以获得进一步的性能与特性演进。
>
> Renee James，Ampere Computing 联合创始人兼 CEO ——[引言来源](https://www.youtube.com/watch?v=rxPt7bpXGSk)

在我们听来这段话很奇怪。虽然服务器 CPU 的生命周期更长，但随着 Ice Lake 爬坡，英特尔正在快速缩减上一代 Cascade Lake 服务器 CPU 的产量；随着 Milan 爬坡，AMD 也在快速缩减 Rome 的产量。到 2023 和 2024 年，随着 Sapphire Rapids、Emerald Rapids 以及 AMD Zen 4 架构的各种变体（如 Genoa 和 Bergamo）爬坡，同样的命运也会降临到当代平台上。

她到底想表达什么，我们只能猜测——我们联系 Ampere 询问，未获回复。可能是指他们的下一代产品将迈向更高的成本与功耗包络，也可能只是围绕服务器 CPU 生命周期的漂亮话，承诺把当代产品再卖几年，好继续攒下订单。

顺便说一句，这些订单相当可观。Ampere 几乎进入了所有主要公有云：Microsoft Azure、腾讯云、阿里云、Oracle Cloud 和 Equinix Metal。唯一缺席的大云当然是亚马逊。排除 Ampere 说得通：从架构角度看，Graviton 2 与 Ampere Altra 相当接近，两者都基于同一款 Arm N1 核心。虽然存在差异，但向自家客户提供那套硬件并不合理。随着 Ampere 的架构与亚马逊自研方向分道扬镳，我们预计亚马逊会开始提供基于 Ampere 的实例。Ampere 在服务器制造商方面也有斩获，如技嘉（Gigabyte）、浪潮（Inspur）和超微（SuperMicro）。销量均未披露，但我们听说 Ampere 的绝大部分销售都流向了上述公有云厂商。

Ampere 的路线图是年度发布节奏，与 AMD 和英特尔一致。与 AMD 和英特尔不一致的是他们的设计方法论——至少是他们对设计方法论的说法。

> 我们做架构和设计的一个核心准则——是采用了更接近敏捷软件的做法。路线图的关键在于保持稳定的发布节奏；我们储备一批特性，然后为它们找到合适的切入时点，所以发布节奏不会变，但随着时间推移，我们可以基于客户反馈增删特性。找我们的话，你想加一个特性，18 个月后它就真的落地了，不用等上三年、四年或五年。
>
> Jeff Wittich，Ampere Computing 首席产品官 ——[引言来源](https://www.nextplatform.com/2022/05/27/ampere-roadmap-has-four-future-arm-server-chips/)

这个说法相当惊人。我们只能认为这与核心架构没有直接关系，因为以 CPU 核心及产品化的周期来看，那实在太快了。举例来说，我们知道谷歌 6 年前向英特尔提出过一个底层核心架构特性，要到 2023 年才会上市。这个例子固然与英特尔当时正在追赶路线图、推行新设计方法论有关，但即便是 AMD，做这种级别的改动也需要大约 3 到 4 年。当然还有许多其他特性，尤其是 IO 相关的，这个说法可能是成立的。AMD 凭借现行的小芯片架构、英特尔凭借未来的 tile 架构，确实可以相当快地实现这类改动。

# **架构**

如果你喜欢看架构，这一节是为你准备的。不喜欢的话，直接跳到细节对比表格之后。我们指出该架构的细节可以在 [GitHub 的 LLVM 代码](https://github.com/llvm/llvm-project/blob/64816e68f4419a9e14c23be8aa96fa412bed7e12/llvm/lib/Target/AArch64/AArch64SchedAmpere1.td)中找到之后，[Cardyak](https://twitter.com/Cardyak) 应我们的请求绘制了这些图。

注：原版 Arm 核心的 L2 缓存是动态可变的，但为简单起见，下图只显示 1 个数字。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/17e10128-bd0d-41ca-bba4-7d8c7c0ca170_657x1024.jpeg)

相对 x86 竞争对手所用的核心，这是一个非常小的核。亚马逊 Graviton 2、Ampere Altra、Ampere Altra Max 和英特尔 Mount Evans 都在用这颗核。它源自 Cortex A76，实现 Armv8.2-A 指令集。Arm 的路线图在下一代核心上出现了一些分岔：N 系列延续，同时他们还提供了大得多、每核性能显著更高的 V1 核心。峰值浮点性能翻倍，并实现了 SVE。这些变化让单线程性能追平英特尔和 AMD 的当代产品，但核心尺寸也随之看齐。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b3fe230b-eb83-427f-9add-ad403be28330_1023x841.jpeg)

这个 V1 架构目前用于亚马逊的 Graviton 3 芯片，还将被欧洲、韩国和印度的国产 HPC 项目采用。它与 Cortex-X1 最为接近，但实现的是 Armv8.4-A 指令集。

与 Cortex-X1 相比，它配备更深的重排序缓冲区（ROB）以挖掘更多指令级并行（ILP），并且每周期可执行 3 读 2 写，而 Cortex-X1 为每周期 2 读 1 写。它的 L1 TLB 也略大。它有 3K 表项的微操作（micro-op）缓存，非常大，甚至超过英特尔的 Sunny Cove 和 AMD 的 Zen 3。V1 还新增了对 bFloat16 和 Int8 数据格式的支持，主要用于处理 AI 与机器学习工作负载。这些变化意味着 V1 的 IPC 相比 N1 高出近 50%。

Arm 的另一颗下一代核心 N2 也即将上市。其性能仅比 V1 低 10%，但面积和晶体管数显著更少。峰值浮点性能相对 V1 减半，但 SVE2 得以落地，将对浮点工作负载大有帮助。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/83347cce-db86-42f2-bfff-e4817eabd064_1024x966.jpeg)

N2 架构将会普遍得多。Marvell 已宣布多款采用该架构的芯片。此外，多家超大规模云厂商也可能采用该架构。我们已知至少有 2 家美国超大规模云厂商有采用该架构的芯片在设计。最后，还有 3 家中国公司声称将把基于 N2 的服务器芯片推向市场：两家是中国超大规模云厂商，一家是独立商用硅公司。

这颗核与 Cortex-A710 最为接近，实现 Armv9.0-A 指令集，带来[一大堆广为宣传的改进](https://fuse.wikichip.org/news/4646/arm-launches-armv9/)。它的 IPC 相比 N1 高达 40%。不过这大约需要多 40% 的晶体管。该核心在 5nm 上的尺寸与前任 N1 在 7nm 上的尺寸大致相当。分支预测器每周期可预测 2 条发生跳转的分支，是每周期只能预测 1 条的 N1 的两倍。N2 拥有 1.5K 表项的微操作缓存，应能降低功耗，并凭借更快的误预测恢复提升 IPC（代价是面积）。重命名宽度从 4 提升到 5，后端 ALU 从 N1 的 3 个增加到 4 个。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a0dd2c1e-123c-4e6f-b13c-a2e05060610c_657x1024.jpeg)

虽然与 Ampere One 相关的许多架构细节仍缺失，但已知不少。Ampere One 实现 Armv8.6，也包含部分 Armv9.1 的特性。核心宽度看来与 N1 非常接近，但核心显然更大、性能更高。Ampere 把 L2 缓存翻倍，并且看起来有 2 个分支单元，而 Arm Neoverse N1 只有 1 个。该核心没有实现任何形式的 SVE。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/0c36ae6f-f630-43df-8f6c-0abb5f366e16_1023x444.png)

关于 Ampere One 最重要的细节是：它延续了现行「云原生」战略的路线。它应该会比 Arm 伙伴们基于 Neoverse V1 和 Neoverse N2 做出的东西小得多。Ampere One 与 AMD Genoa、Intel Sapphire Rapids 等下一代平台之间的核心尺寸差距将显著拉大。我们会在仅限订阅者的章节用一次专项成本对比讨论与这些平台的比较，并谈谈我们对 IPO 与商用硅未来的看法。

注意，Sapphire Rapids 和 Genoa 的成本会远比估算的 Ampere One 准确，因为后者除了制程节点和扒出来的架构细节之外，完全没有第一方信息。

[分享](https://newsletter.semianalysis.com/p/is-ampere-computings-cloud-native?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)
