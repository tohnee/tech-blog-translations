---
title: "Cerebras 下一代 CS-4：快，变得更快"
title_en: "Cerebras's Next Generation CS-4: Fast Just Got Faster"
subtitle: "性能翻倍，功率翻倍，乐趣翻倍"
date: 2026-08-19
source: https://newsletter.semianalysis.com/p/cerebrass-next-generation-cs-4-fast
crawled: 2026-09-15
authors: ["Myron Xie", "Bryan Shan", "Wega Chu", "Jordan Nanos", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Cerebras 下一代 CS-4：快，变得更快

> 原文：[Cerebras's Next Generation CS-4: Fast Just Got Faster](https://newsletter.semianalysis.com/p/cerebrass-next-generation-cs-4-fast) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**性能翻倍，功率翻倍，乐趣翻倍**

Cerebras 本周发布了 CS-4，更多细节将在 Hot Chips 大会上公布。CS-4 是其第四代机柜，围绕同一颗第三代 5nm 晶圆级引擎（WSE-3）打造。CS-4 通过提高每片晶圆的功耗与时钟频率，以及更高的机柜级密度，实现了相对 CS-3 的性能翻倍。

这一切意味着，CS-4 能将每片晶圆的每秒每用户 token 数（tokens/s/user）相对 CS-3 翻倍，而成本与上一代大致相当。对客户来说这毫无悬念：同样的硬件开支即可享受翻倍的 token 收入。变快的不只是 token，产品上市时间也在变快：机柜架构本身经过重新设计、更加模块化，可制造性与部署时间都得到改善。最后同样重要的是，全新的 I/O 模块将为未来开放、异构、分离式的推理架构铺平道路。这类分离式推理（disaggregated inference）部署将通过与基于 HBM 的系统配对，大大帮助克服 CS-4 的内存容量限制。

![](https://substack-post-media.s3.amazonaws.com/public/images/c0e1a46c-39e0-40af-9892-cda940b120d9_2407x1339.png)
*来源：SemiAnalysis*

# 同一块晶圆，时钟翻倍

![](https://substack-post-media.s3.amazonaws.com/public/images/606cc687-c8a9-4507-8e56-fc3de6f682b6_1020x516.png)
*来源：SemiAnalysis*

CS-4 采用与 CS-3 相同的 5nm WSE-3，但 Cerebras 通过时钟频率翻倍榨取了两倍性能。这来源于向晶圆大幅增加供电，并得益于 CS-4 在供电与散热技术上的改进。虽然停留在同一代 5nm 硅片上听起来平淡无奇，但 Cerebras 仍然可以让最重要的指标翻倍：内存带宽。在其他条件不变的情况下，内存带宽翻倍应带来每秒每用户 token 数的近翻倍，而这正是客户想从 Cerebras 那里得到的。时钟频率翻倍也使峰值理论 FLOPs 和 WSE 的片外并行 I/O 翻倍，使 CS-4 的片外 I/O 从 CS-3 的 1.2Tb/s 升级到 2.4Tb/s。不过，每片晶圆 44GB 的 SRAM 容量保持不变，因为它由每片晶圆上可用的 SRAM 位单元数量决定，所以要等到下一代硅片才能在这方面看到提升。这是复用同一颗 WSE-3 的主要缺点：每片晶圆内存容量偏低，是 Cerebras 架构固有的关键取舍之一。

正如我们在[上一篇关于 Cerebras 的文章](https://newsletter.semianalysis.com/p/cerebras-faster-tokens-please)中所描述的，这颗晶圆因采用 SRAM 而拥有极为独特的架构，非常适合运行算术强度（Arithmetic Intensity）低的算子，例如小批量解码（decode）。

![](https://substack-post-media.s3.amazonaws.com/public/images/1fa5fbc1-16ad-49b8-ba4d-d61c0091004f_2800x1560.png)
*来源：SemiAnalysis*

# 网络改进

除了片外 I/O 带宽翻倍之外，片外通信还有更多改进，来自全新的晶圆 I/O 接口——这是一块升级版 FPGA 卡，用作 NIC，将 Cerebras 的专有 I/O 转换为标准以太网。从下图可以看到，晶圆南北两侧各引出一个 I/O 模块，共 2 个。

![](https://substack-post-media.s3.amazonaws.com/public/images/524dd8f8-64a7-4403-a290-2528afd9e9be_1819x1021.png)
*来源：Cerebras*

该 I/O 模块支持现场升级，因此 Cerebras 可以在不重新设计机箱的情况下迁移到新的网络标准。这看似小改动，影响却很大：它让 CS-4 更容易与其他系统对接，组建分离式推理部署。在分离式注意力-前馈网络（attention feed-forward network）配置中将 CS-4 与基于 HBM 的 XPU 配对，是克服 CS-4 低内存容量的一种方式，[与 NVIDIA 定位 Groq LPU 的方式如出一辙](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands?open=false#%C2%A7gpu-and-lpu-integration-attention-ffn-disaggregation-afd)。我们在下文会详细讨论。这一设计看起来尤其为 AWS 量身定做——后者希望在 CS-4 上配备自家的 EFA NIC，与 Trainium 服务器对接实现分离式推理。

此外，借助全新的低时延报文处理流水线，两层胖树网络（使用 Arista 以太网交换机）的时延从 CS-3 的 5 微秒降至 3 微秒。如今还支持晶圆直连链路，无需绕经交换网络，进一步把时延降到 2 微秒。晶圆直连路径还可配置，这意味着 FPGA 具备交换能力，可以让数据经由不同晶圆路由。

这是一项实打实的改进，但如今许多 Cerebras 竞争对手给出的交换总时延已以纳秒计，「超快」网络是相对的，我们认为这只是一次温和的改进。我们认为 3µs 的时延和带宽限制仍是一个瓶颈，阻碍了 EP（专家并行）、ETP 等专家层跨越多片晶圆的并行方案。从路由器到专家的 token 分发与合并对时延高度敏感，而专家负载不均问题再加上一跳额外网络，使流水线并行成为唯一可行的解法。

# 「背包」机柜

在系统层面，CS-4 最引人注目的变化是物理层面的。Cerebras 把机柜拆成专注供电的前半部分和专注计算的后半部分，并以模块化、可插拔的「背包」（backpack）形式封装。每个背包容纳一颗晶圆级引擎，一个 CS-4 机柜可容纳三个，而 CS-3 每机柜为两片晶圆。泵和热交换器等散热基础设施也被移出机柜，因为如今的数据中心本身就按支持全液冷机柜来建造。

![](https://substack-post-media.s3.amazonaws.com/public/images/c5821801-a81f-498c-a9d7-359074c95b22_2048x1198.png)
*来源：Cerebras*

背包是一个垂直封装体，独立划分为供电、散热、I/O 和 WSE-3 模块，这使整个系统的制造明显比 CS-3 更简单。WSE-3 晶圆垂直放置，供电面朝向机柜前部。供电模块经由晶圆正面供电，与 CS-3 相同。晶圆散热则从晶圆背面处理。I/O 模块附着在晶圆上下边缘，与晶圆共同构成一个矩形表面。

背包设计让部署流程更顺畅。客户可以先把带供电模块的机柜安装就绪，然后在现场把晶圆背包直接插接到机柜上。考虑到每机柜升级为三颗晶圆引擎、且以更高时钟频率运行，一个 CS-4 机柜的 TDP 落在 125-135kW，大约是单台 CS-3 23kW 功耗的两倍上下、或略低于两倍。总体来看，这意味着每瓦性能（performance/W）相比 CS-3 最多只有轻微提升。

![](https://substack-post-media.s3.amazonaws.com/public/images/c366bb11-0fbe-45a9-a3b2-c52c7cd7a659_1114x1442.png)
*来源：Cerebras*

代际之间的大改善应该在于成本。虽然散热和供电的增强本身会抬高物料清单（BOM）成本，但 CS-4 元器件数量的减少和更简单的组装应对这些成本项形成显著抵消，我们认为每片晶圆的有效 BOM 最终可能与 CS-3 相当。对客户而言，这意味着以相近的总拥有成本（TCO）获得近双倍的交互性与 token 收入，这是一个非常有吸引力的主张。

Cerebras 最钟爱的 CS-4 数字是 43 PB/s 的片上内存总带宽，公司将其宣传为约为 NVIDIA Rubin 内存带宽的 2,000 倍。这将是主导此次发布大部分报道的数字，因为片上 SRAM 带宽随功耗增加而水涨船高。

结果是，尽管内存带宽是 2,000 倍，Cerebras 宣称的交互性改善却是一个更合理的「相比 GPU 最多 30 倍」，并将其包装为新的「超快（ultrafast）」性能档位。我们预计 CS-4 在前沿模型上将达到接近 4,000 tok/sec/user，而 CS-3 为 2,000 tok/sec/user。同时我们预计 Blackwell GPU 的上限仍将是理论上的 200 tok/sec/user（没人真会跑在这个点上），在合理并发量下更现实的是 100 tok/sec/user。在我们看来这相当于 20-40 倍的交互性提升，那么为何不宣传「快达」40 倍呢？似乎也够公道了。

# 并行策略

由于单颗 WSE 的片上 SRAM 不足以容纳整个模型的权重，Cerebras 在这套系统上继续将重心放在流水线并行推理上。在 CS-4 上，给定模型的每个 MoE 专家都会交错放置在单一晶圆内。默认采用流水线并行与 GPU 不同——GPU 上最常见的是张量并行和专家并行，以便把大模型塞进可用的 HBM 中。Cerebras 一贯主张：用 GPU 的 HBM 存权重，比所有事情都在一片晶圆上完成更慢、更耗电、也更贵。

当然，在性能、功耗和成本上比较 WSE 集群与 GPU 集群时，结果很大程度上取决于你选择哪种并行策略。GPU 的配置选项区间非常宽（从高吞吐/低交互配置到高交互/低吞吐配置），而晶圆的区间则有限得多。本文只考虑高交互性/低吞吐的场景。

为了将 WSE 与 GPU 直接对比，我们对 NVIDIA 发布的 TileRT 特别感兴趣——它为 GPU 集群带来了高交互性/低吞吐配置。我们在上周的 TileRT 文章中讨论了部分内容

![](https://substack-post-media.s3.amazonaws.com/public/images/a005ae63-d068-4140-8461-25047b6a8a41_2048x1110.png)
*来源：InferenceX*

由于晶圆本身有 44GB，即便是当今运行的前沿模型（如 GPT 5.6 Sol），Cerebras 也尚未需要把 MoE 模型的单个专家切分到多片晶圆。不过，考虑到长上下文推理的需求，我们预计 OpenAI 等 Cerebras 客户会设法节省长上下文负载在晶圆上保存 KV 缓存的成本，以 256k 上下文窗口运行 5.6 Sol，而不是完整的 1M 上下文。

正如我们在 [Cerebras IPO 文章中所述](https://newsletter.semianalysis.com/p/cerebras-faster-tokens-please)，支撑长上下文推理的成本极其巨大。大多数人仍然明白，让模型完成一次前向传播所需的内存量与模型总参数量成正比。然而，保存 KV 缓存所需的内存会随并发用户数以及这些用户请求的平均/最大规模（由模型上下文窗口决定）成比例增长，这一点似乎仍是一个被严守的秘密。以大上下文窗口运行模型并支持大量并发用户，需要海量的内存容量。

当我们简单分析运行一个大模型（比如 1.6T 参数的 DeepSeek V4 Pro）需要什么时，我们发现：以 1M 上下文运行该模型所需的最少 Cerebras WSE 数量约为 20 套系统，而在 256 个请求的合理并发下约为 40 套系统。也就是说，在你能对一款前沿模型完成一次前向传播之前，就已经投入了超过 $20M 的资本开支（CAPEX）和 1MW 的功耗。

该分析可在我们公开的 [tokenomics 网站](https://tokenomics.info/cerebras)上查看：

![](https://substack-post-media.s3.amazonaws.com/public/images/0c4f13b1-6de1-457c-8026-9044658c339e_2048x1435.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/c9eee3e4-36ed-45c4-945c-1563289a5b66_2048x1426.png)
*来源：https://www.tokenomics.info/cerebras*

当然，在这笔前置投资之后，随之而来的是一些相当可观的聚合性能指标。让我们深入看看。

# 押注分离式架构

Cerebras 将 CS-4 定位为从零开始为开放、异构、分离式推理而打造。他们目前正与 AMD 和 AWS Trainium 合作，后续还有更多伙伴。在所有这些配置中，Cerebras 都将充当解码（decode）芯片，因为其 roofline 并不擅长计算受限的预填充（prefill）。公司全面看好各类分离式（disagg）部署，并宣称除了传统的预填充-解码分离（PDD）之外，还支持注意力-前馈分离（AFD）。

![](https://substack-post-media.s3.amazonaws.com/public/images/da0c70bb-afa9-457a-b9b7-8f2eae6d96d0_1456x865.png)
*来源：SemiAnalysis*

试图在 GPU 上复刻数据流执行的软件方案可以逼近 HBM roofline，但在带宽上无法与纯 SRAM 架构相比。然而，所有异构分离式部署都是双刃剑：集群中预填充与解码资源的配比，在硬件采购订单（PO）签署的那一天就被固定死了。而一整支 GPU 或 TPU 机队则可以随用户负载画像的变化动态调整为不同配比。现实世界里，负载确实会随时间变化。我们已经看到推理（reasoning）模型因为「思考」时间更长而推高解码成本，随后智能体缓存命中又拉低预填充成本，而解码成本保持不变。一个包打天下的 P:D 配比，不太可能在这些系统 5 年以上的生命周期里始终完美最优。

要更好地理解这些动态，以及基础设施团队在设计高性能推理集群时的思考过程，请阅读[我们的 TileRT 文章](https://newsletter.semianalysis.com/p/ultra-high-interactivity-on-nvidia)。

# 路线图：Nexus 与 CS-5

Cerebras 已经与全新的机柜级平台「Nexus」协同设计了下一代晶圆级引擎，这意味着 CS-4 机柜机箱很可能会延续到未来芯片世代，无需重大的机械重新设计。公司公开承诺的路线图是每年大约 2 倍的性能提升，具体目标是到 2027 年实现 20 倍的吞吐量改进。

在可靠性方面，Cerebras 正在解决现场更换晶圆托盘的操作难题，并持续投资于错误恢复、托盘级冗余，以及芯片本身跨核心与通道的良率收割。
