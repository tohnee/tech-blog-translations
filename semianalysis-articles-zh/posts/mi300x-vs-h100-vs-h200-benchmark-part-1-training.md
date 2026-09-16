---
title: "MI300X vs H100 vs H200 基准测试第一部分：训练——CUDA 护城河依然健在"
title_en: "MI300X vs H100 vs H200 Benchmark Part 1: Training - CUDA Moat Still Alive"
subtitle: "训练性能、用户体验、易用性、Nvidia、AMD、GEMM、Attention、网络、InfiniBand、Spectrum-X 以太网、RoCEv2 以太网、SHARP、总拥有成本"
date: 2024-12-22
source: https://newsletter.semianalysis.com/p/mi300x-vs-h100-vs-h200-benchmark-part-1-training
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball", "Reyk Knuhtsen"]
tags: ["Accelerators", "LLMs", "Benchmarks"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# MI300X vs H100 vs H200 基准测试第一部分：训练——CUDA 护城河依然健在

> 原文：[MI300X vs H100 vs H200 Benchmark Part 1: Training - CUDA Moat Still Alive](https://newsletter.semianalysis.com/p/mi300x-vs-h100-vs-h200-benchmark-part-1-training) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**训练性能、用户体验、易用性、Nvidia、AMD、GEMM、Attention、网络、InfiniBand、Spectrum-X 以太网、RoCEv2 以太网、SHARP、总拥有成本**

## 引言

为了弄清 MI300X 的真实情况，SemiAnalysis 走上了一段长达五个月的求证之旅。从理论上讲，无论规格还是总拥有成本（TCO），MI300X 相对英伟达（Nvidia）的 H100 和 H200 都应拥有巨大优势。然而现实是，下面列出的纸面规格并不能代表真实环境中可以期待的性能。如果 AMD 能够凭借这样的内存配置兑现下列宣传的性能，它将成为市场上一个非常强劲的竞争者。

![](https://substack-post-media.s3.amazonaws.com/public/images/76cfa222-48b8-4151-9fa9-254179b08aa6_2184x1088.jpeg)
*来源：SemiAnalysis、Nvidia、AMD*

今天我们将讲述这五个月来对 MI300X、H100 和 H200 进行独立分析与训练导向基准测试的历程，期间我们与英伟达和 AMD 双方都保持互动。我们将详细回顾所跑过的大量底层基准测试，摘要可参见目录。此外，我们还会比较英伟达与 AMD GPU 的总拥有成本，并把性能因素纳入考量。归根结底，我们所做的很多事情，就是在五个月的 bug 提交与修复之后，公开地向 AMD 提出一套全面的建议，告诉他们要做什么才能具备竞争力、解决软件问题。这不只是软件不成熟的问题——他们需要改变开发方式。

简而言之，在将英伟达 GPU 与 AMD MI300X 对比时，我们发现 MI300X 纸面上的潜在优势并未兑现，原因在于 AMD 公开发布的软件栈存在缺失，以及 AMD 缺乏测试。

AMD 的软件体验满是 bug，开箱即用（out of the box）的 AMD 训练根本无从谈起。我们曾期望 AMD 能在训练工作负载上成为英伟达的强劲对手，但遗憾的是，截至今天情况并非如此。由于 AMD 比预期更弱的软件质量保证（QA）文化以及极具挑战性的开箱体验，CUDA 护城河至今仍未被 AMD 跨越。**AMD 填平 CUDA 护城河的速度有多快，英伟达的工程师就在加班加点地用新特性、新库和性能更新把这条护城河挖得有多深。**

我们与英伟达和 AMD 双方共享了 GEMM 基准测试和单节点训练的基准测试源代码及中间测试结果，通过电话会议和讨论征集反馈、对基准测试实施改进，并与 AMD 合作对其软件栈实施 bug 修复。

我们这种高度迭代式互动的目标，是确保我们的测试能够无偏地评估真实世界用户将会获得的体验。

我们原本计划几个月前就发布这篇文章，但希望多花一些时间与 AMD 团队沟通，探索可能的修复或开发工作。我们花了相当多的时间识别并修复 AMD 软件 bug，以便给 AMD 充分的机会，让 MI300X 摆脱 AMD 软件栈 bug 的束缚展现实力，而不是只展示开箱即用时的问题表现。为了给出公允的印象，我们也详细说明了为达到这一步所做的大量调优和 bug 清剿工作。我们认为这种方式能为用户提供尽可能高的透明度。

**我们希望尽己所能，为改善 AMD 生态做出贡献。** **虽然** **经过我们的 bug 报告和反复敲打，AMD 软件如今已大有改善，但其公开软件栈仍不尽如人意**。我们已经将许多基准测试开源，并创建了简单的一行命令以便复现。

如果 Lisa Su 和 AMD 领导层加倍投入，聚焦其软件与测试栈，他们就有机会在训练上与英伟达一较高下。我们认为 AMD 的工程师极具能力，也在尽全力推进 AMD 生态——事实上，这些工程师以 bug 修复、配置帮助和定制镜像形式提供的支持，确实提升了我们能从 MI300X 上获得的结果。

为给我们的基准测试流程画上终止符，我们于 2024 年 11 月 15 日向英伟达和 AMD 发送了大部分主要 GEMM 和单节点基准测试代码及结果的草稿，供其评论、验证和微调。我们要求任何最终意见、修复、反馈和性能改进都须在 11 月 25 日前提交。我们设定这一时间框架是为了固化测试结果，留出时间撰写深度分析与评论，并进行多轮内外部评审——所有这些环节所需的时间都多变且往往不可预知，通常为 2-4 周。

几天前，在我们通知双方文章发布日期已确定为 12 月 20 日之后，AMD 请求我们推迟发布，以便纳入基于 AMD 某开发者分支上 beta WIP 开发构建的结果。我们对英伟达的全部基准测试都是在公开可用的稳定版构建上进行的。本着透明与公平的精神，我们既纳入了这些结果，也纳入了原始 11 月 25 日截止日镜像以及最新公开可用软件上更新后的测试套件结果。不过我们认为，解读这些结果的正确方式，是看 AMD/英伟达软件公开稳定版的性能。

**以下是我们用于基准测试的软件构建列表：**

- H100 公开稳定版（Public Stable Release）——英伟达 H100 的开箱体验。
- H200 公开稳定版——英伟达 H200 的开箱体验。
- MI300X 11 月 25 日定制构建（Nov 25th Custom Build）——这是一个手工打造的定制 VIP docker 镜像，由 AMD 首席工程师（principal engineer）编写，从源代码构建所有依赖。
- MI300X 公开稳定版 PyTorch 2.5.1——AMD MI300X 的开箱体验。
- MI300X 12 月 19 日公开 Nightly 版（Public Nightly Dec 19th）——这可以预示到 2025 年 1 月 PyTorch 2.6 发布时（即产品发布一年多之后）AMD 的性能水平。
- MI300X 12 月 21 日 WIP 开发构建（Dec 21st WIP dev build）——这是在我们同意推迟文章发布后 AMD 提交给我们的镜像。这是一个尚未合并进 AMD 内部主分支的实验性开发构建，且未使用 PyTorch 原生 flash attention API。该镜像的性能可以预示未来 1-2 个季度 AMD 公开稳定版的性能水平。

我们非常感谢 AMD 和英伟达在整个过程中提供的技术支持，但我们在发布的结果上保持独立性。我们要公开鸣谢并感谢我们在 AMD 的对接人：Anush Elangovan（AMD AI 副总裁）、Hui Liu，以及数十位出色的 AMD 首席/高级工程师、AMD 工程副总裁、AMD 工程院士（Engineering Fellow）、AMD 工程企业副总裁（CVP）和 AMD 工程总监，还有 AMD 软件库负责人，感谢他们对我们的各类 bug 报告进行分诊和修复。英伟达方面，我们感谢 Kedar Potdar、Ian Buck、Sylvain Jeaugey 以及英伟达 NCCL 团队的鼎力支持。

感谢 [Crusoe](https://crusoe.ai/cloud)、[TensorWave](https://tensorwave.com/)（*AMD Ventures 被投企业*）、[Nebius](https://nebius.com/)、[Lambda](https://lambdalabs.com/)、[Hot Aisle](https://hotaisle.xyz/) 以及 [Sustainable Metal Cloud (SMC)](https://smc.co/) / [Firmus](https://firmus.co/) 提供算力并支持开源基准测试。Crusoe、Nebius、SMC / Firmus 和 Lambda 开箱即支持托管 SLURM 和共享家目录。TensorWave 的托管 SLURM 目前处于 beta 阶段，该功能将于明年初正式商用（GA）。Sustainable Metal Cloud 是少数拥有[官方 MLPerf GPT-3 175B 训练成绩](https://mlcommons.org/benchmarks/training/)的新兴 GPU 云（neocloud）之一。

**我们将发布一篇关于 H100、H200 和 MI300X 推理的后续文章。几个月后我们可能还会再发一篇后续文章，跟踪 AMD 训练性能，看看开箱体验是否改善，并测试 LlaVa 和 Mamba 等其他模型。**

![](https://substack-post-media.s3.amazonaws.com/public/images/fd9ce744-8e42-4b9a-9120-22ff0192a3f9_2354x1244.png)
*来源：SemiAnalysis*

## 核心发现

1. 只比较纸面 FLOP/s 和 HBM 带宽/容量，就像只看像素数来比较相机。要判断实际性能，唯一的办法就是跑基准测试。
2. 英伟达的开箱性能和体验令人惊叹，我们在基准测试期间没有遇到任何英伟达特有的 bug。英伟达只指派了一名工程师为我们提供技术支持，但由于没碰到任何英伟达软件 bug，我们其实不太需要支持。
3. AMD 的开箱体验非常难用，需要极大的耐心和体力活才能推进到可用状态。**在我们的大多数基准测试中，AMD PyTorch 的公开稳定版仍然是坏的，我们需要各种绕行方案（workaround）**。
4. 如果没有多支 AMD 工程师团队为我们遇到的 AMD 软件 bug 进行分诊和修复，AMD 的成绩会比英伟达低得多。
5. 我们与 Sustainable Metal Cloud 合作，在 256 块 H100 上跑了非官方 MLPerf Training GPT-3 175B，以测试不同 VBoost 设置的影响
6. 对 AMD 而言，公开稳定版软件上的真实世界性能与其纸面宣传的 TFLOP/s 相去甚远。英伟达的真实性能也低于其宣传的 TFLOP/s，但差距远没有这么大。
7. 与 H100/H200 相比，MI300X 的总拥有成本（TCO）更低，但在 AMD 软件公开稳定版上，MI300X 的单位 TCO 训练性能更差。如果使用 AMD 软件的定制开发构建，情况会发生变化。
8. 训练性能更弱，MI300X 的矩阵乘法微基准测试就是明证；AMD 公开发布软件在单节点训练吞吐上仍落后于英伟达的 H100 和 H200。
9. **MI300X 的性能被 AMD 软件拖了后腿**。**BF16 开发分支上的 AMD MI300X 软件性能更好**，但尚未合并进 AMD 内部仓库的主分支。等到它合并进主分支并进入 PyTorch 稳定版时，英伟达 Blackwell 早已对所有人开放了。
10. AMD 的训练性能也受制于 MI300X 无法提供强大的横向扩展（scale out）性能。原因在于其较为薄弱的 ROCm Compute Communication Library（RCCL），以及与英伟达对其 Nvidia Collective Communications Library（NCCL）、InfiniBand/Spectrum-X 网络 fabric 与交换机的强整合相比，AMD 与网络和交换硬件的垂直整合程度更低。
11. AMD 的许多 AI 库是英伟达 AI 库的 fork，这导致了次优结果和兼容性问题。
12. AMD 客户往往只在推理中使用手工打造的内核，这意味着他们在非常狭窄的明确用例之外性能很差，而且完全不具备应对快速变化工作负载的灵活性。

## 给 AMD 的核心建议

**我们真诚地希望看到英伟达之外再有一个有力竞争者，也希望帮助 AMD 走到那个位置**，但遗憾的是，这方面还有大量工作要做。在文末我们列出了给 Lisa Su 和 AMD 领导团队的详细反馈清单，这里先给出摘要：

1. 给 AMD 工程师更多算力和工程资源来修复和改进 AMD 生态——相对英伟达提供给其工程师的资源，AMD 内部 GPU 机器少得可怜。TensorWave 这家最大的 AMD GPU 云，免费把 GPU 时长送给 AMD 的一个团队去修软件问题——考虑到这些 GPU 是他们真金白银买的，这实在离谱。
2. AMD 需要再接入数千块 MI300X、MI325X 用于 PyTorch CI/CD 自动化测试，以确保不出现 AMD 性能回退和功能性 AMD bug。目前 PyTorch/AWS 有数百块英伟达 GPU 用于 PyTorch CI/CD，以保障出色的开箱体验
3. AMD 高管团队应当亲自、高强度地内部试用（即 dogfood）那些即将公开发布的产品，而不是把重点放在测试内部构建上。最好在直播（twitch.tv）中 dogfood，展示真实的开箱体验。就像 geohotz 做直播那样
4. AMD 应与 Meta 合作，尽快让生产级 LLM 训练工作负载在 PyTorch ROCm（AMD 对 CUDA 的回应）上跑通，因为通常 Meta 没在用的 PyTorch 代码路径都有大量 bug。
5. 不要再过度依赖正确设置大量（多达几十个）环境标志才能让 AMD 部署可用，而应把这些设置固化进默认配置。让开箱体验真正可用！
6. 专注于做好开箱体验，而不是过度依赖那种从 main@specificcommit 源代码构建所有依赖、要花 5 个小时构建的定制 VIP 镜像。
7. 不要再指望终端用户去用 PYTORCH_TUNABLE_OPS——这是一个 bug 多多的原型特性，也不尊重终端用户的时间：用户每次想改自己的代码，都要再花约 1 个小时重新调优。
8. AMD 应提交 MLPerf Training GPT-3 175B 成绩。MLPerf 是一种对等可比的基准测试方法论，以收敛时间为北极星指标。
9. 我们希望 AMD 具备竞争力，也愿意当面沟通，就如何改善 AMD 数据中心 GPU 生态给出更详细的反馈。

## AMD 与英伟达之争的叙事概要

在深入探讨拖累 AMD 的软件栈的各个方面之前，我们先讨论 MI300X 的基本规格、相对总拥有成本，以及大多数分析师和投资者如何评价其竞争力。

MI300X 于 2023 年底发布，带来了一套令人兴奋的纸面规格——1,307 TFLOP/s 的 FP16 算力（高于 H100 的 989 TFLOP/s）、5.3 TB/s 内存带宽和 192GB HBM3；相比之下 H100 为 3.35 TB/s 内存带宽和 80GB HBM3。这些规格也超过了 H200——后者本质上是在内存规格上升级的 H100，提供 4.8TB/s 内存带宽和 141GB HBM3e。

![](https://substack-post-media.s3.amazonaws.com/public/images/c456bf40-8aa2-4d89-b666-8d062323d41e_2184x1088.jpeg)
*来源：SemiAnalysis、Nvidia、AMD*

纸面上，MI300X 部署的总拥有成本极具吸引力，不仅因为 MI300X 的平均售价（ASP）更低，还因为它通常采用更便宜的以太网组网。比较一个 16k H200 集群与一个 16k MI300X 以太网集群，仅网络一项就贡献了近 40% 的成本节约，其余节约来自更低的加速器成本。使用白盒以太网交换机相比使用英伟达 Quantum-2 交换机能节省可观成本，但真正的差距在更便宜的光收发器——英伟达品牌收发器的价格高达普通收发器 OEM 收费标准的 2-3 倍。

从表面看，MI300X 似乎两全其美：性能更高且总拥有成本更低。在它发布之时，从这一诱人组合出发，预期弱势一方 AMD 夺取市场份额是合乎逻辑的。下表展示了集群的前期总资本开支——集群资本开支组成部分的更详细拆解以及详细的网络物料清单（BoM）分析，见本文接近末尾的章节。

![](https://substack-post-media.s3.amazonaws.com/public/images/08a6d76b-c20b-4def-b349-448abaf02e2f_1819x619.jpeg)
*来源：SemiAnalysis AI TCO 模型*

随着订单落定，市场对 MI300X 潜力的热情不断高涨，AMD 的乐观评论和指引又推波助澜。凭借诱人的规格优势，很容易论证 AMD 指引还有上行空间——多数投资者都认定管理层在藏拙。理论上，AMD 手握一副好牌。毕竟其 2024 年在数据中心 GPU 的市场份额为个位数中段，按逻辑推演，到 2027 年迈向 10-12% 份额的路径甚至可能还偏保守，同时还能给 AMD 带来可观的盈利上行空间。

然而，从 2023 年末到 2024 年大部分时间，2024 全年数据中心 GPU 销售指引屡屡低于那些高企的预期。从 1Q24 财报到 3Q24 财报，AMD 只把指引从 40 亿美元上调到 50 亿美元，远低于基于 [CoWoS 与 HBM 供应协议](https://www.semianalysis.com/p/accelerator-model)得出的 60-80 亿美元投资者预期线。我们在 [Accelerator Model](https://semianalysis.com/accelerator-industry-model/) 中的需求观点，也跟踪到了[微软年初的失望情绪和后续订单的缺失](https://semianalysis.com/accelerator-industry-model/)。

前述看涨逻辑，就像只凭杂志宣传就买下某款车型，既不试驾、也不向车主打听反馈、更不看任何评测。不过不必担心——SemiAnalysis 已大规模实测了 MI300X、H100 和 H200，并能说明为什么 AMD 当前的软件栈问题决定性地推翻了这套逻辑。

## 通用矩阵乘法（GEMM）性能

在基于 transformer 的架构（即 ChatGPT、Llama 等）中，绝大多数 FLOPS 都用于矩阵乘法，也就是 GEMM。因此，**GEMM 性能是衡量 ChatGPT、Llama、Claude、Grok 等前沿 transformer 在硬件上训练表现的良好代理指标**。

GEMM 接收两个输入矩阵：矩阵 A 和矩阵 B。矩阵 A 的形状为 (M, K)，即 M 行 K 列；矩阵 B 的形状为 (K, N)；二者相乘得到形状为 (M, N) 的输出矩阵。

![](https://substack-post-media.s3.amazonaws.com/public/images/20b7820c-407a-4ce5-9311-33e1d9b41533_1499x1404.png)
*来源：Nvidia*

从概念上讲，结果矩阵的每个元素都是沿输入的「K」维度逐元素相乘后的求和。因此，K 维度也被称为归约（reduction）维度。

![](https://substack-post-media.s3.amazonaws.com/public/images/096e0e89-9404-49dd-88c2-18a86a0cf06b_1875x684.png)
*来源：SemiAnalysis*

下面我们测试了以下真实世界的矩阵形状，以 (M,N,K) 形式给出——它是「将维度为 (M,K) 与 (K,N) 的矩阵相乘」的简写。

以下矩阵形状实际用于 [Meta 的 Llama 70B](https://github.com/pytorch-labs/float8_experimental/blob/fe6e08c867abf56b1acd0f34473c69cde624f0a3/benchmarks/bench_matmul.py#L57) 生产训练：

- (16384, 8192, 1280) - 融合 QKV 投影 GEMM 形状
- (16384, 1024, 8192) - Attention 输出投影形状
- (16384, 8192, 7168) - FFN GEMM 形状
- (16384, 3584, 8192) - FFN GEMM 形状
- (8192, 8192, 8192) - 用于基准测试的标准 GEMM 形状

我们使用 OpenAI 的 do_bench 函数进行基准测试设置，这是 PyTorch 基准测试的行业标准方法。do_bench 函数默认在每轮运行之间清理缓存，并提供预热（warmup）和多次执行基准测试的方法，取中位数结果作为给定精度。这些测试中我们使用 warmup=30 和 rep=200。输入张量 A 和 B 均以均值为 0、方差为 1 的正态分布随机初始化。这是因为正态分布最接近现代神经网络中权重和激活值的真实分布。输入张量的分布会影响 TFLOP/s 性能基准测试的结果。我们将在后文讨论输入分布影响 TFLOP/s 性能的原因。

在 BF16 上，H100 和 H200 相对其标称的 989.5 TFLOP/s 实测约 720 TFLOP/s，而 MI300X 相对其标称的 1,307 TFLOP/s 仅达到约 620 TFLOP/s。

这意味着，尽管标称 BF16 TFLOP/s 高得多，MI300X 却比 H100 和 H200 慢 14%。这一 AMD 结果用的还是由 AMD 首席工程师手工打造的定制 docker 镜像，却依然慢于英伟达的 GPU。我们对 MI300X 的开箱测试中，TFLOP/s 吞吐甚至比这还要慢！除了定制镜像，AMD 还要求用户设置大量默认未设置的环境标志，才能达到这样的性能结果。

![](https://substack-post-media.s3.amazonaws.com/public/images/709f1dbd-d014-4737-b865-fdb53edf252d_1489x1084.png)
*来源：SemiAnalysis*

遗憾的是，FP8 的情况更糟。H100/H200 在标称 1979 TFLOP/s 中实测约 1,280 TFLOP/s，相比之下 MI300X 仅达到约 990 TFLOP/s。因此，在 FP8 上 MI300X 比 H100 慢 22%。这是在两个输入均为 e4m3 FP8（[即 4 位指数和 3 位尾数](https://semianalysis.com/2024/01/11/neural-network-quantization-and-number/)）数据类型下的结果。

![](https://substack-post-media.s3.amazonaws.com/public/images/fc5d7c11-6a1f-458d-9e3e-dd6e1624363e_1514x1152.png)
*来源：SemiAnalysis*

值得注意的是，调用 GEMM 是一项简单任务，我们本不应遇到 AMD 软件 bug。不幸的是，我们遇到的一个**重大 bug**是：整个夏季有几个月，torch.matmul 和 F.Linear 两个 API 在 AMD 上给出的性能一直不同。按理说 torch.matmul 和 F.Linear 应有相同性能，但令人意外的是，F.Linear 慢得多！

这是个奇怪的 bug，因为 torch.matmul 和 F.Linear 都是硬件厂商 GEMM 库的封装，本应达到相同的性能水平。F.Linear 尤其重要，因为这是 PyTorch 中大多数终端用户启动 GEMM 内核的方式。

五个月前我们刚开始测试 AMD 时，公开版 AMD PyTorch 仍有这个 bug。根因在于 AMD 实际上有两个不同的底层 GEMM 库：rocBLAS 和 hipBLASLt，其中 hipBLASLt 对 MI300X 的优化更好。bug 在于 torch.matmul 用的是优化过的 hipBLASLt，而 AMD 默认没有改 F.Linear，让它仍在使用未优化的 rocBLAS 库。

在我们的 bug 报告之后，AMD 几个月前最终修复了这个重大 bug，我们希望它不会因缺乏适当的回归测试而复发。如果 AMD 加强测试投入，而不是等着用户去发现这些关键问题，其可用性会大幅改善。

我们已将测试中使用的 GEMM 基准开源为一个简单的三行命令，任何人都能轻松运行：

![](https://substack-post-media.s3.amazonaws.com/public/images/cfc95cc8-cb39-4a7f-9717-ef5406c97b0b_821x571.png)
*来源：SemiAnalysis*

## 流行的 GEMM 基准测试并不准确

最近，互联网上流传着一个基准测试，声称在 GEMM 上 AMD MI300X 的性能接近 H100。

![](https://substack-post-media.s3.amazonaws.com/public/images/2a5ff26d-c895-43ee-b940-a7ef197c4ca7_1024x548.png)
*来源：Github*

这个基准测试有两大问题：它没有正确执行 L2 缓存清理，而且只是取最大性能值，而不是取特定形状多轮迭代的 TFLOP/s 中位数/均值。迭代之间不清理 L2 缓存，基准就无法准确反映真实世界的 GEMM 性能。此外，由于 TFLOP/s 会随迭代轮次变化，你需要以至少 100 轮迭代的均值/中位数为基准，才能得到准确的 GEMM 基准。OpenAI 的 do_bench 默认开箱即提供 L2 缓存清理和均值/中位数，因此我们建议工程师用它做微基准测试。下面我们把这个基准简化为伪代码，并对上述问题做了注释。

![](https://substack-post-media.s3.amazonaws.com/public/images/a9127f13-583a-4b0a-8037-a96876eeed4f_1470x880.png)
*来源：SemiAnalysis*

## HBM 内存带宽性能

众所周知，AMD MI300X 的内存带宽优于英伟达 H100 和 H200：MI300X 提供 5.3 TB/s 带宽，H200 为 4.8 TB/s，H100 为 3.35 TB/s。更好的 HBM 内存带宽对推理非常有用，对训练有时也有帮助。训练中，如果 HBM 内存容量和内存带宽更充裕，用户就可以设置更大的 batch size。不过一旦全局 batch size 超过某个规模，模型收敛所需时间会更长。用大全局 batch size 很容易跑出高吞吐，但总体上它会拖累收敛时间。

从我们的 HBM 内存带宽基准测试来看，MI300X 的内存带宽确实远好于 H200 和 H100。我们在 PyTorch 中用 Tensor.copy_ 测试内存带宽，并使用行业标准 OpenAI do_bench 确保准确性。

**正如我们即将发布的 H100 vs H200 vs MI300X 推理文章将展示的，内存带宽对推理极为重要。**

![](https://substack-post-media.s3.amazonaws.com/public/images/05fdf265-ecae-494e-bbd2-24b191d24768_1600x1114.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/8d1eef68-22bd-442f-810b-d039aee70a63_829x665.png)
*来源：SemiAnalysis*

## AMD 手工打造的 VIP 定制构建与 WIP 开发构建

我们能将 AMD 性能做到 H100/H200 的 75% 水平，唯一原因是得到了 AMD 多支团队的支持，修复了大量 AMD 软件 bug。为了让 AMD 达到性能尚可的可用状态，一位 AMD 首席工程师专门为我们手工打造了一个约 60 条命令的巨型 Dockerfile（从源码构建依赖）——因为 PyTorch Nightly 和公开 PyTorch AMD 镜像表现糟糕且版本各异。这个 docker 镜像从源码构建需要约 5 小时，还要安装依赖和子依赖（hipBLASLt、Triton、PyTorch、TransformerEngine），与英伟达形成巨大反差——英伟达提供预构建的开箱体验，只需一行代码。**大多数用户不会从源码构建 PyTorch、hipBLASLt，而是使用稳定版。**

使用公开 PyTorch 时，用户可以选择最新的稳定镜像或 nightly 版 PyTorch 上传。**因此，尽管 nightly 版 PyTorch 可能包含最新提交，有潜力带来更好性能或修复某些 bug，但用户必须接受它可能未经充分测试、可能包含新 bug**——这些 bug 来自 Meta/AMD/英伟达或其他 PyTorch 贡献者，尚未被发现。**请注意，大多数终端用户使用的是 PyTorch 稳定版。**

![](https://substack-post-media.s3.amazonaws.com/public/images/26876a7b-8446-4e9f-b543-510bdc8d1921_3680x7420.png)
*来源：SemiAnalysis、AMD*
![](https://substack-post-media.s3.amazonaws.com/public/images/6da81937-1fa0-40fa-854d-fb8c74e815c6_1024x453.png)
*来源：Nvidia*

令人愉快的是，英伟达的 Docker 镜像包含性能分析和调试所需的完整开发者工具，如 Nsight Compute 和 Nsight Systems。相比之下，AMD 开箱并不包含其 OmniTrace 开发者工具。

直到几周前，AMD docker 镜像还只支持 8 个月前发布的 PyTorch 2.3。此后 PyTorch 2.4 和 2.5 主线版本也已发布，PyTorch 2.6 将于 2025 年第一季度推出。我们向一位 AMD 首席工程师和 AMD 的 AI 副总裁建议，AMD 应当跟进最新的 AMD PyTorch 版本——此后 AMD 已开始为其中一些 AMD PyTorch 版本发布容器。AMD PyTorch 2.5 的 Docker 镜像仍然缺失。

![](https://substack-post-media.s3.amazonaws.com/public/images/09f56f85-cc14-47e0-9232-28e145214702_2057x1098.png)
*来源：Nvidia*

## 12 月 21 日 AMD 开发构建

下面是 AMD 12 月 21 日开发构建的 docker 镜像。可以看到，它为 hipBLASLt、AOTriton、ROCm Attention 等依赖使用多个非稳定开发分支，并从源代码安装包括 PyTorch 在内的一切，构建耗时超过 5 小时。这些版本的依赖甚至还没合并进 AMD 自己的主分支。**99.9% 的用户不会从源代码安装 PyTorch、也不会在开发分支上从源码安装其全部依赖，而是使用 PyPi 上公开稳定的 PyTorch。**

此外，这个 AMD 开发构建没有通过 PyTorch 原生、用户友好的 [torch. scaled_dot_product_attention](https://pytorch.org/docs/stable/generated/torch.nn.attention.sdpa_kernel.html) API 来使用 Flash Attention，而是引入了另一个库（同样是开发分支）的 attention 实现。我们看到越来越多用户通过 PyTorch 原生 [torch. scaled_dot_product_attention](https://pytorch.org/docs/stable/generated/torch.nn.attention.sdpa_kernel.html) API 使用 Flash Attention，因为它更友好且已内置于开箱版 PyTorch 中。[连 AMD 自己的公开文档也推荐通过 torch.scaled_dot_product_attention API 使用 Flash Attention](https://rocm.blogs.amd.com/artificial-intelligence/flash-attention/README.html#benchmarking-attention)。我们希望这些内核被合并进 PyTorch flash attention，而不是让终端用户另外安装一个要花数小时构建的独立库。这不是友好的用户体验。另外，AMD 必须支持 FlexAttention，它已迅速成为业界的首选。

AMD 12 月 21 日开发构建位于一个悬而未决的开发分支上。也就是说，这个分支尚未经过完整 QA，属于风险自担的使用分支。使用开发构建、开发分支并从源码构建，其结果的有效性存在诸多疑虑，因为大多数用户在现实中并不会这么做。大多数用户主要会从 PyPI 稳定版安装 AMD/英伟达 PyTorch，因此我们建议读者在分析这些结果时把这一点记在心上。

话虽如此，我们仍纳入这些开发构建结果，因为它能指示未来 1-2 个季度 AMD 公开稳定版软件的水平。但同时，到未来 1-2 个季度真正交锋时，英伟达 Blackwell 将已广泛部署，而 AMD MI355X 要到 2025 年下半年才会开始出货。

![](https://substack-post-media.s3.amazonaws.com/public/images/24add0ee-f573-47e2-b9b6-81fbc1ba812d_3680x5640.png)
*来源：SemiAnalysis、AMD*

## 训练测试方法论（GPT1.5B、Llama 8B、Llama 70B、Mistral）

测试训练性能的方法很多。最准确的方法是拿一家中等规模 AI 初创公司的模型内部代码库，在 512-1024 块 GPU 的集群上运行。这样，测试运行就具备典型用户会有的全部优化。其他一切方法都只是这些训练运行性能的代理。训练性能综合了 HBM 带宽、HBM 容量、TFLOP/s、网络和系统架构。**比较纸面 HBM 带宽/容量，就像比较纸面相机像素。**

MLPerf GPT3 175B 训练也是衡量训练到特定收敛所需时间的好代理。MLPerf 基准会考虑全局 batch size，以及混合精度实现是否会带来收敛惩罚。遗憾的是，MLPerf 相当难跑，因为缺少用户友好的文档和说明，而且其性能常常通过专门为 MLPerf 炮制的定制调优配置压榨到极致——普通用户不会采用这种配置。请注意，英伟达已提交超过 1.1 万块 H100 的 MLPerf Training 成绩，而 AMD 只在内部跑 MLPerf Training。AMD 的成绩很可能拿不出手，所以他们从未提交过任何 MLPerf Training，更不用说 MLPerf GPT3 175B 了。

在设计 SemiAnalysis 基准测试时，我们希望反映普通用户的模型实现方式，因此选择了 [torch. scaled_dot_product_attention](https://pytorch.org/docs/stable/generated/torch.nn.attention.sdpa_kernel.html) API（使用 flash attention 后端）、PyTorch Distributed Data Parallel（DDP）和/或 Fully Sharded Data Parallel（FSDP）加 [torch.compile](https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html)。[还要注意，AMD 在自己的文档中也建议用户使用 torch.scaled_dot_product_attention](https://rocm.blogs.amd.com/artificial-intelligence/flash-attention/README.html#benchmarking-attention)。我们认为这最能代表典型用户工作负载。此外，这些模型我们使用通用的 PyTorch 原生实现，以贴近典型的 ML 科学家用户，并保证一行代码即可运行。与 MLPerf 不同，我们基准的目标是尽可能简单易跑，同时仍是性能的良好代理。注意，由于我们没有考虑收敛时间，该基准对 AMD 略有偏向——我们在 AMD 上设置的 micro batch size 高于英伟达。若把收敛时间纳入考量，AMD 的结果会比文中所述更差。

顺带一提，许多 AI 从业者表示他们不使用 Megatron、NeMo 或 3D 并行，因为这些库复杂度高、灵活性差，其僵化与复杂使它们几乎无法用于 ML 研究。注意，就 3D 并行而言，英伟达和 AMD 都能获得更高性能——前提是软件栈能正常工作，而对 AMD 来说这是个很大的假设。AMD Megatron 是英伟达 Megatron 的 fork，star 数不到 10，这意味着它很可能没有被很好地 dogfood。要提交 bug 报告并等 AMD Megatron 能跑通简单模型，还需要**额外数月**。

在 SemiAnalysis 模型训练基准中，我们将测试四个模型：第一个是简单的 GPT 1.5B DDP，我们认为它能代表扩展到更大模型之前的小规模实验/消融研究的样子。DDP 是一种简单得多、网络开销低得多的并行形式。接下来，我们测试了标准的 Llama3 8B 和 Llama3 70B 4 层代理（4 Layer Proxy），作为流行模型性能的基线。第三，我们测试了 Mistral 7B v0.1，用于评估加入一点复杂度后硬件表现如何，因为 Mistral 使用滑动窗口注意力（sliding window attention）而非标准因果注意力（causal attention）。ChatGPT、Claude、Gemini、o1、o3 等现代模型并不使用标准因果注意力，而是使用复杂的注意力机制。

现代 GPT/Llama/Transformer 模型是由同一个 transformer 层反复堆叠而成的。因此，只测量 4 层的性能就是模型整体性能的极佳代理。

![](https://substack-post-media.s3.amazonaws.com/public/images/e6177898-4068-4f94-976e-fe116180e7de_502x1141.png)
*来源：Imgur*

此外，在所有前沿 LLM 模型的现代 LLM 训练中都会使用流水线并行（pipeline parallelism），这意味着每台 GPU 服务器只放置若干个 transformer 层。现代预训练中绝不会把整个模型放在单个节点上。

![](https://substack-post-media.s3.amazonaws.com/public/images/7481b615-82be-41dc-931b-47cc8e70428d_2150x735.png)
*来源：SemiAnalysis*

每训练一个 token 的模型 FLOP 由以下公式定义：

6 * non_input_embedding_params + 12 * num_layers * num_heads * head_dim * max_seq_len * density

其中 density 表示注意力相对于全掩码（full mask）的稀疏程度。例如，因果注意力的稀疏度为 50%，而滑动窗口注意力的稀疏度更低。

请注意，我们的测试套件最初用的是 6 * params 而非 6 * non_input_embedding_params，这是计算每 token 模型 FLOP 的错误方式。此外，我们使用 FSDP 的方式还存在另一个 bug。**此后我们更新了测试套件，回溯重测并更新了 H100、H200、MI300X 在所有软件版本（公开稳定版、公开 nightly、VIP 镜像和 AMD 开发构建）上的全部基准结果。下文列出的所有结果均来自更新后的测试套件。**

## 单节点训练性能

请注意，本报告中呈现的 H100/H200 性能反映的是开箱性能，未经英伟达工程师任何手工调优；而 MI300X 的结果则来自 AMD 工程师数月的调优和 bug 修复。与 bug 遍地的 AMD 训练相比，我们没有遇到任何英伟达特有的 bug。五个月前，由于 AMD 在 attention 反向传播和 torch compile 上的软件 bug，许多模型在 AMD MI300X 上跑不过 150 TFLOP/s，该 bug 迫使用户手动把模型某一区域标记为不可编译，而不是做全图编译。

可以看到，在所有模型上，H100/H200 都胜过 MI300X 公开发布版/公开 nightly 版/11 月 25 日源码构建 VIP 镜像。有意思的是，MI300X 在 GPT 1.5B 这类小模型上、以及在任何使用非因果注意力层的模型（如 Mistral 7B v0.1）上表现不佳。这是因为截至截止日期 FlexAttention 尚未完全可用，而在英伟达 GPU 上它自 2024 年 8 月起就能正常工作。因此，对 MI300X 公开发布版/公开 nightly 版/11 月 25 日 VIP 构建而言，H100/H200 的 TFLOP/s 领先超过 2.5 倍。

对 12 月 21 日 MI300X 内部 WIP 开发分支构建，我们看到它在 GPT 1.5B 上仍不如 H100/H200。此外，它在 Mistral 7B 上也略逊于 H100。在 Llama3 8B 和 Llama3 70B 代理上，12 月 21 日 MI300X WIP 开发构建表现优于 H100/H200，但请注意，这是因为该 WIP 开发使用的是某位 AMD 工程师的开发分支，甚至尚未合并进 AMD 主分支。

![](https://substack-post-media.s3.amazonaws.com/public/images/8c239ab5-1c2d-4303-8527-84498ef66c71_1491x1180.png)
*来源：SemiAnalysis*

三个月前，在 AMD 上尝试 FP8 训练会导致段错误（segfault）和硬错误。万一跑通了，实际上也比同样任务用 BF16 更慢。我们与 AMD 的 FP8 团队合作解决了这个问题，AMD hipBLASLt 团队也创建了[调优](https://github.com/ROCm/hipBLASLt/pull/1378)来修复 MI300X 的 FP8 性能。FP8 训练很重要，因为它比 BF16 训练更快，而且大多数前沿实验室都在用 FP8 训练。

经过大量修复后，可以看到 MI300X 11 月 25 日版在 Llama3 8B 和 GPT 1.5B 上的吞吐与 H100 大体有来有回。一如既往，H200 在这一档胜出。但在 Llama3 70B 4 层代理上，AMD 11 月 25 日的结果被狠狠击败。

对于带非因果注意力层的 Mistral 7B，AMD 11 月 25 日版的性能只有 H100 的一半左右。这说明，只要模型结构稍有改动，即使经过数月调优，AMD 在非简单模型上仍无竞争力。许多前沿模型和 AI 训练初创公司正在使用复杂注意力层来实现长上下文和高效注意力，而 AMD 在这些方面仍远远落后。

遗憾的是，AMD 上的 FP8 训练只能在定制镜像上工作，比如我们的 11 月 25 日 VIP 镜像和 12 月 21 日 WIP 开发分支镜像。我们刚开始尝试 AMD FP8 训练时，它比公开发布版上的 AMD BF16 训练还慢。

![](https://substack-post-media.s3.amazonaws.com/public/images/1ec9137f-add4-46d0-98b4-68050db8a439_1491x1181.png)
*来源：SemiAnalysis*

对 AMD 的 WIP 开发构建，我们看到在 Llama3 8B 上它赢了 H100，但仍慢于 H200 公开稳定版软件。H200 的性能完全击败 MI300X，即使后者用的是 12 月 21 日 WIP 开发分支。

有意思的是，MI300X 在非因果注意力层（如 Mistral 7B v0.1）上表现不佳，连其内部构建也不例外。Mistral 使用的滑动窗口注意力正是部分前沿模型在用的。看来，如果你想训练一个不用因果注意力的模型，AMD MI300X 天生就输定了。

虽然很多人发布硬件性能对比，但大多数人不开放测试源码，也不做易于复现。我们采用开源方式，已将单节点训练基准开源，只需几行命令即可运行：

![](https://substack-post-media.s3.amazonaws.com/public/images/2ec308cc-f094-4fdb-b165-16d1fa1b2da5_836x941.png)
*来源：SemiAnalysis*

## 多节点训练性能

多节点方面，我们对两节点 H100 和两节点 MI300X 进行了基准测试。遗憾的是，我们未能及时获得多节点 H200 部署的访问权限来完成本文。

在这项基准测试中，H100 再次以大优势战胜 MI300X，领先幅度为 10-25%。随着更多节点加入同一个训练工作负载，这一差距还会扩大。这是一个已知问题，AMD 试图在明年通过部署其新的自研 400G AI 专用 NIC 来解决。

## AMD 的 PYTORCH_TUNABLE_OPS 标志体验糟糕

要让 AMD 训练像样地跑起来，用户需要使用 PYTORCH_TUNABLE_OPS——这是 AMD 特有的原型标志，供终端用户调优 GEMM。由于这是原型特性（即不稳定），过去出现过许多相关 bug，包括但不限于[段错误](https://github.com/pytorch/pytorch/issues/139116)、HBM 内存泄漏，以及[一](https://github.com/pytorch/pytorch/pull/139137)[大](https://github.com/pytorch/pytorch/pull/143507)[堆](https://github.com/pytorch/pytorch/pull/140673)其他问题，比如许多[单元测试被禁用](https://www.torch-ci.com/failure?failureCaptures=%5B%22test_linalg.py%3A%3ATestLinalgCUDA%3A%3Atest_matmul_small_brute_force_tunableop_cuda_float16%22%5D)。这些已知的 tunable ops bug 如今已修复，但很可能还有更多未知的 AMD 软件 bug。

此外，即便用户没有遇到任何 bug、这个 AMD 原型标志得以一路畅通地工作，调优任何一个现代 LLM 模型仍需 1-2 小时。虽然这些 GEMM 可以被终端用户缓存，但用户代码稍有改动，就得再花 1-2 小时重新调优。可以想象，这会拖慢 ML 科学家在做模型研发和消融实验时的迭代周期速度。

在英伟达上不需要这个标志，因为其 GEMM 库（cuBLASLt）开箱即是调优好的，cuBLASLt 的启发式模型开箱就能为 H100/H200 上的大多数形状选出正确算法。相比之下，AMD hipBLASLt/rocBLAS 的启发式模型开箱即为大多数形状选错算法，这正是终端用户需要大量耗时调优的原因。

我们建议 AMD 修复其 GEMM 库的启发式模型，让它开箱就选出正确算法，而不是浪费终端用户的时间去自行调优。用户做研究时迭代往往很快，因此反复重跑 tunable ops 会显著拖慢研究速度。

## 纵向扩展 NVLink/xGMI 拓扑

纵向扩展（scale-up）fabric 对 GPU 集群极为重要，它为前沿模型训练中使用的张量并行和专家并行提供极速通道。为此，我们对 scale-up fabric 性能进行了基准测试。

H100 和 H200 的 scale-up fabric 叫做 NVLink，为每块 GPU 提供 450GByte/s 带宽，将 8 块 GPU 连接在一起。MI300X 的 scale-up fabric 叫做 xGMI，纸面上同样连接 8 块 GPU，为每块 GPU 提供 448GByte/s 带宽。表面上，MI300X 的 scale-up 网络与 H100/H200 极为相似、性能接近，纸面带宽只低 0.5%。遗憾的是，现实情况截然不同。

首先，MI300X 的 xGMI 是点对点 fabric，也就是说 GPU 两两之间*实际上*并没有 448GByte/s 的带宽，每两块 GPU 之间只能以 64GByte/s 通信。只有当一块 GPU 同时寻址其余全部 7 块 GPU 时，才能达到标称的 448GByte/s。这意味着，对于张量并行 TP=2，最大带宽为 64GByte/s；TP=4 时为 189GByte/s。

![](https://substack-post-media.s3.amazonaws.com/public/images/4ac85f6f-0fa0-4f51-be6b-88662b666680_1455x1147.png)
*来源：SemiAnalysis*

相比之下，英伟达 NVLink 采用交换式拓扑，一块 GPU 可以以完整的 450GByte/s 与另一块 GPU 通信。此外，H100/H200 中的四颗 NVSwitch 支持网内归约（称为 NVLink SHARP（NVLS），默认开启），这是一种通过在交换机内部执行集合通信/归约来减少数据搬运的技术。

![](https://substack-post-media.s3.amazonaws.com/public/images/77daa464-4fde-4e19-a96b-0b6195f59b82_2172x743.png)
*来源：SemiAnalysis*

## All Reduce/All to All/Reduce Scatter/All Gather 集合通信概览

我们将展示英伟达 H100/H200 和 AMD MI300 在纵向扩展和横向扩展网络上的基准测试。要测试的集合通信（collectives）是前沿 LLM 训练使用的主要集合通信操作：all_reduce、all_gather、reduce_scatter 和 all to all。all_reduce 用于数据并行和张量并行，all_gather 用于 ZeRO/FSDP 并行（也用于张量并行），reduce_scatter 用于 ZeRO/FSDP 并行。

由于计算与通信重叠（compute-communication overlapping）的工作方式，真实世界的消息大小从 16MiB 到 256MiB 不等，PyTorch DDP 默认大小为 25MiB（英伟达 MLPerf 11,000 块 H100 的 GPT-3 175B 训练使用的[消息大小最大为 200MiB](https://github.com/mlcommons/training_results_v4.1/blob/b87b9e396f771345d4ef122ba33456304f15228d/NVIDIA/benchmarks/gpt3/implementations/eos-dfw_n1452_ngc24.04_nemo/config_common.sh#L69)）。我们还测试了 8GiB 和 16GiB，只为看看峰值总线带宽，尽管这些消息大小在真实世界中并不使用。上述所有集合通信都用于 3D 并行和 FSDP/ZeRO 并行——这些都是训练前沿模型的常用技术。

![](https://substack-post-media.s3.amazonaws.com/public/images/f528ea53-0b8c-4dff-8a48-c89ba475be2b_2259x1357.png)
*来源：DeepSpeed*
![](https://substack-post-media.s3.amazonaws.com/public/images/515beda1-3436-4319-8759-e74590c3530a_2206x1165.png)
*来源：Meta*

## 单节点 NCCL 集合通信

我们看到，在所有真实世界消息大小上，英伟达在每一项集合通信上都大幅领先 AMD。这并不意外：H100/H200 拥有更优的 450GByte/s NVLink 交换式拓扑并支持网内归约（NVLS），而 MI300X 只有 7x64GByte/s 的 xGMI 点对点拓扑。

![](https://substack-post-media.s3.amazonaws.com/public/images/fe08fabf-8ed6-4405-ab0d-2b700f7ea5b7_1725x1216.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/af7610d4-3246-4dda-a955-81c0b48d5613_1592x1147.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/a06bb258-12dc-4f75-97ec-9d2a08347d0d_1593x1134.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/71df6db8-d62f-4f91-ae6c-78c1d08b6082_1594x1168.png)
*来源：SemiAnalysis*

要复现这项测试，可以使用我们开源的 ClusterMax-NCCL/RCCL 基准，我们把它开发成一行 Bash 即可轻松运行。ClusterMax 是我们即将推出的评估体系，从定量性能和定性用户体验两个维度对 H100/B200/GB200/MI300X 新兴 GPU 云集群进行排名。敬请期待我们即将发布的*《ClusterMax 新兴 GPU 云评估 | 如何租用 GPU》*一文。

![](https://substack-post-media.s3.amazonaws.com/public/images/009fda89-6efa-4a29-a2dc-c55c6d8de066_3496x1568.png)
*来源：SemiAnalysis*

## 多节点 RCCL/NCCL 集合通信与横向扩展网络基准测试

在英伟达 H100/H200 和 MI300X 上，每块 GPU 都通过 400G 网络接口卡（NIC）直接连接到横向扩展网络上的其他节点。H100/H200 参考设计通常在 InfiniBand NDR 上使用 ConnectX-7 NIC，或在 Spectrum-X 以太网上使用 BlueField-3。Spectrum-X 是英伟达为 AI 工作负载专门打造的定制以太网方案。MI300X 的参考设计则推荐搭配 Broadcom Thor-2 NIC 使用 RoCEv2 以太网。

![](https://substack-post-media.s3.amazonaws.com/public/images/003120b8-0c44-4463-b289-549993ea52cc_1100x624.png)
*来源：Nvidia*

典型的 GPU 集群几乎总是需要多于单层网络的层数，因为单层网络只能支持 128 块 GPU（Broadcom 以太网或英伟达 Spectrum-X 以太网的情形）和 64 块 GPU（H100/H200 InfiniBand）。在这种多层网络中，部署通常采用 8 轨（rail）优化的胖树结构，8 块 GPU 各自连接到不同的交换机（这种连接称为一条「轨」）。[我们在 AI 新兴 GPU 云手册与解剖一文中详细解释了轨优化网络的工作原理](https://semianalysis.com/2024/10/03/ai-neocloud-playbook-and-anatomy/#cluster-level-networking-bill-of-materials)。

![](https://substack-post-media.s3.amazonaws.com/public/images/1ba221b3-91a8-43ae-b321-d63d0d42bb5c_1614x781.png)
*来源：SemiAnalysis*

正如英伟达为其 scale-up 网络提供 NVLS 一样，英伟达 H100/H200 的 InfiniBand scale-out 网络也提供 InfiniBand SHARP 网内归约——这同样是英伟达独占的。AMD 没有面向 MI300X 的类似产品。InfiniBand SHARP 的工作方式与 NVLink SHARP 网内归约类似，二者都提供了一种减少网络流量的途径，InfiniBand SHARP 的归约在 Quantum-2 InfiniBand 交换机内部完成。

遗憾的是，与默认开启的 NVLink SHARP 不同，InfiniBand SHARP 在 UFM/IB 子网管理器中默认并不开启。我们与许多新兴 GPU 云、H100 集群运营方和 AI 前沿实验室交流过，大多数表示他们没有开启 SHARP，原因是 NCCL_TIMEOUT 比率上升以及网络安装配置困难。我们问过英伟达哪些 AI 客户在使用 InfiniBand SHARP，但他们拒绝具体回答。可以推测，如果 InfiniBand SHARP 在 AI 生产工作负载中真的有用，英伟达市场部门早就扯着嗓子宣传其成功部署了。鉴于目前 InfiniBand SHARP 的采用显然有限，我们在此同时展示英伟达开启和未开启 SHARP 两种情况下的集合通信性能。

在部分基准测试中，我们还采集了英伟达一个名为 Israel-1 的内部集群上的 Spectrum-X 以太网数据。英伟达 Spectrum-X 用于 xAI 的 200k H100/H200 集群，在 Spectrum-X 参考架构 1.2 版中可支持最多 100k GPU 的集群，而采用非参考的定制设计则有望支持多达 512k GPU。

我们还在测试 Google Cloud（GCP）H100 的自研以太网，以及部署在 AWS 自研以太网（称为 EFAv2/EFAv3）上的 AWS H100 和 H200。我们将在即将发布的《集合通信深度解析》一文中分享这些结果，该文将可视化展示不同类型的集合通信，解释不同的 NCCL 协议（SIMPLE、LL、LL128）、不同的 NCCL 算法（NVLS、NVLSTREE、RING、TREE、COLNETDIRECT、COLNETCHAIN、PAT），以及集合通信在 GCP H100 以太网、AWS H100/H200 EFA、InfiniBand H100、Spectrum-X 等平台上的运行方式。

下面我们展示 32 GPU 的 all reduce 集合通信测试。可以看到，与普通 InfiniBand H100 以及开启 SHARP 的 InfiniBand H100 相比，MI300X RoCEv2 垫底。简而言之，糟糕的 all reduce 性能导致糟糕的横向扩展训练。

![](https://substack-post-media.s3.amazonaws.com/public/images/09a00702-0524-4521-b8d5-50b6356cca42_1594x1203.png)
*来源：SemiAnalysis*

当增加参与集合通信的 GPU 数量（即横向扩展）时，MI300X 的性能会下降。可以想象，现代前沿训练是在至少 100,000 块 GPU 的集群上进行的。与 InfiniBand Non-SHARP 基线相比，MI300X RoCEv2 在 16MiB 到 256MiB 的所有真实世界消息大小上速度只有一半。如下面的图表所示，英伟达 Spectrum-X 以太网的性能与 InfiniBand Non-SHARP 相当接近，这得益于 Spectrum-X 与 NCCL 集合通信库的垂直整合，以及其良好的拥塞控制和自适应路由。AMD 正试图在明年通过其即将推出、支持 Ultra Ethernet 的 Pollara 400G NIC 实现垂直整合，有望使 AMD 与英伟达一较高下。而英伟达一如既往没有停下脚步：到明年晚些时候，其 800G ConnectX-8 NIC 将可投入生产，线速是 AMD Pollara NIC 的两倍。

AMD RCCL 是英伟达 NCCL 的 fork。AMD 的 RCCL 团队和许多其他 AMD 团队资源有限，无论是算力还是人手都不足以改进 AMD 生态。AMD RCCL 团队目前能稳定使用的*研发用 MI300X 不足 32 块*——这很讽刺，因为改进集合通信操作恰恰需要接触大量 GPU。坦率地说这很荒唐，AMD 应该加大投入，让软件团队用到更多 GPU。

这与英伟达 NCCL 团队形成鲜明对比——后者可以使用英伟达内部 11,000 块 H100 的 EOS 集群作为研发资源。此外，英伟达还有 Sylvain Jeaugey 这位集合通信领域的一流专家，以及许多其他世界级的集合通信专家。不幸的是，由于薪酬和资源吸引力不足，AMD 基本上没能吸引到集合通信库人才——而在英伟达，工程师因 RSU 升值年收入超过一百万美元的并不少见。

为帮助缓解这些问题，TensorWave 和 SemiAnalysis 目前正与 AMD RCCL 团队合作提升集合通信性能。TensorWave 慷慨地资助了 AMD 一个中等规模的集群，帮助 RCCL 团队获得更多资源开展工作。TensorWave 买了一大堆 GPU 之后，还得倒贴 GPU 给 AMD 让他们修自己的软件——这事实在离谱。

另一个值得注意的趋势是：对于非 SHARP 网络，GPU 数量每翻一倍，all reduce 集合通信的速度会按对数下降。相比之下，开启 SHARP 后，速度/完成时间保持不变。我们拥有最多 1,024 块 H100 的结果，表明 IB SHARP all reduce 在任何数量的 GPU 参与集合通信时都是常数时间。我们将在即将发布的*《集合通信深度解析》*一文中公布这些内容。

![](https://substack-post-media.s3.amazonaws.com/public/images/8577baae-b3f0-4fb9-b48d-84af6d4855bf_1473x1153.png)
*来源：SemiAnalysis*

在 all gather、all to all 和 reduce scatter 集合通信上，MI300X 比 InfiniBand 慢 2-4 倍。遗憾的是，我们没有 all gather 和 reduce scatter 的 Spectrum-X 或 InfiniBand SHARP 基准数据。

![](https://substack-post-media.s3.amazonaws.com/public/images/27e21f6c-7eac-418f-8c68-095a30b28f1d_1670x1250.jpeg)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/d2ce4511-0ba1-4935-99f1-027c1ac56ca1_1720x1221.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/8baeab3c-61d2-44ec-a466-96c7e5c8496d_1723x1219.png)
*来源：SemiAnalysis*

下面我们提供我们的 nccl/rccl 基准测试脚本。遗憾的是，由于集群环境各异，它没法一行搞定，需要你按照 nccl/rccl 和 nccl-tests/rccl-tests 的 README.md 操作才能正确运行。在 AWS 和 Google Cloud 上，可能还需要安装定制的 nccl 适配器。

![](https://substack-post-media.s3.amazonaws.com/public/images/bbec630b-1202-41aa-8b71-9795891e335b_814x747.png)
*来源：SemiAnalysis*

## AMD 用户体验欠佳，MI300X 开箱不可用

由于 AMD 内部测试（即 dogfood）不力和自动化测试缺失，MI300 开箱不可用，需要大量工作和调优。[2024 年 11 月，AMD 在其「Advancing AI」大会上，AMD 的 AI 高级副总裁](https://www.youtube.com/live/vJ8aEO6ggOs?si=ViPmlckQNmDYCayJ&t=3416)声称 AMD 内部每天晚上运行超过 200k 个测试。然而，这似乎对我们遇到的众多 AMD 软件 bug 没什么缓解作用，我们怀疑 AMD 是否在做规范的 CI/CD 测试，包括规范的性能回归测试、功能性以及收敛性/数值测试。我们在此列举几个例子，让读者理解我们遇到的 AMD 软件 bug 的性质，以及为什么我们认为它们严重妨碍了 AMD 上的良好用户体验。

[尽管 AMD 自己的文档推荐使用 PyTorch 原生 Flash Attention](https://rocm.blogs.amd.com/artificial-intelligence/flash-attention/README.html#benchmarking-attention)，今年夏天有好几个月，AMD 的 PyTorch 原生 Flash Attention 内核运行速度不足 20 TFLOP/s——这意味着一颗现代 CPU 计算 attention 反向层的速度*都比 MI300X GPU 快*。有一段时间，MI300X 上用 PyTorch 做的几乎所有 Transformer/GPT 模型训练都慢如龟爬。直到有人提交了 bug 报告——其背后是对 PyTorch/Perfetto 的深入性能分析，显示反向传播（紫色/棕色内核）占用的时间远多于前向传播（深绿色部分）——AMD 才有人注意到。通常，反向部分耗费的时间应只约为前向的 2 倍（若使用激活检查点则略多）。

![](https://substack-post-media.s3.amazonaws.com/public/images/358ec78a-dd8b-4604-a58c-d76c25837e2a_1481x209.png)
*来源：SemiAnalysis*

我们遇到的另一个问题是，AMD PyTorch 的 attention 层与 [torch.compile](https://pytorch.org/tutorials/intermediate/torch_compile_tutorial.html) 一起使用时会因 longsumexp 张量的秩（rank）不正确而硬报错。令人沮丧的是，这个问题早在 5 月 30 日就在 AMD PyTorch 内部构建中修复了，却直到 10 月份有人向他们指出存在 bug 之前，都没能进入任何 AMD PyTorch 发行版、甚至任何 PyTorch nightly 构建。这说明 AMD 对公开发布的软件包缺乏测试和 dogfood。这个问题的另一个核心原因是，PyTorch 的主要维护者 Meta 目前并未在内部用 MI300X 做生产级 LLM 训练，导致 Meta 内部不用的代码路径 bug 频出、也未被好好 dogfood。我们认为 AMD 应与 Meta 合作，让其内部 LLM 训练在 MI300X 上跑通。

![](https://substack-post-media.s3.amazonaws.com/public/images/39607c82-c678-4bae-8963-bcdfa8141049_890x453.png)
*来源：SemiAnalysis*

8 月 8 日，Horace He 和 Meta PyTorch 团队发布了 [FlexAttention](https://pytorch.org/blog/flexattention/)，这是一个关键 API，用于在不损失速度的前提下创建非因果注意力层。以前，要使用 document masking、滑动窗口注意力、softcap、Alibi 等注意力变体，用户需要花数周时间用 CUDA/HIP 语言手工打造自己的内核，再做 pybinding 接入 PyTorch。而有了 FlexAttention，用户用这个 API 就能快速生成所有注意力变体。FlexAttention 通过块稀疏（block sparsity）实现出色性能——只计算掩码中需要的块，忽略其余部分。

![](https://substack-post-media.s3.amazonaws.com/public/images/d9dbce6b-eefc-40ca-b6f2-753e47118714_437x357.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/59da3049-f7e0-419a-802f-4d2bbb774477_1600x1459.jpeg)
*来源：Meta*

配合滑动窗口注意力，FlexAttention 可以将性能提升 10-20 倍！这对终端用户是件大好事，但遗憾的是，直到几天前，MI300X 上的 FlexAttention 仍状态糟糕，存在大量 AMD 软件 bug（包括收敛问题）。虽然最新的 PyTorch nightly 已修复收敛问题，但这与英伟达上 8 月起就可用的 FlexAttention 形成鲜明反差。这意味着这些出色的 PyTorch 功能在英伟达与 AMD 平台上的可用性存在约 6 个月的差距。对前沿 AI 实验室来说，六个月就是一辈子——在此期间 OpenAI、Anthropic 和 Google 已发布了大量模型。

![](https://substack-post-media.s3.amazonaws.com/public/images/6388946a-2f1b-4006-b084-03b863949371_1475x1009.png)
*来源：SemiAnalysis*

## 探索在 AMD 上获得更好性能的思路

AMD 建议我们尝试 PYTORCH_TUNABLE_OPS，通过在运行时遍历 GEMM 算法来提升 GEMM 性能。然而，正如前文所述，这个 API 表现很差，因为 GEMM 应该在编译 hipBLASLt/rocBLAS/cuBLASLt 时调优，而不是在用户的运行时进行。英伟达 H100 用户在大多数形状上无需使用 PYTORCH_TUNABLE_OPS，因为 cuBLAS 启发式模型会选出正确算法。AMD 的启发式模型则相反，大多数形状下似乎永远选不对算法。我们建议 AMD 别再让用户尝试 tunable ops，而是专注于在内部把自己的 GEMM 库调好。

我们在 AMD 上尝试 PYTORCH_TUNABLE_OPS 时，出现了超过 25 GByte 的 HBM 内存泄漏——MI300X 总容量为 192GByte——这基本上抹掉了 MI300 相对 H100 的 HBM 容量优势。解决办法是为 hipBLASLt 和 rocBLAS 设置默认 workspace 以防内存泄漏。

![](https://substack-post-media.s3.amazonaws.com/public/images/a877f575-f237-4fde-8fa4-996f8180bf49_1024x540.png)
*来源：PyTorch/AMD*

正如本文前面提到的，我们遇到的另一个问题是，MI300X 需要设置一大堆环境标志才能真正可用。我们建议 AMD 不要再把用户推到必须自己设置这些环境标志的境地，而是设置好能带来可用环境的默认标志。问题不仅在于数量，还在于这些标志之间复杂的相互作用，使故障排查变得困难。想从 AMD MI300X 上获得合理的训练性能，是一个 NP-Hard 问题。

另一个问题是，由于 AMD 软件 CMake 的 bug 导致硬错误，某些 AMD ROCm 库无法安装进 Docker。此问题现已修复。在 AMD GPU 上，你需要传入一套繁琐的标志才能让 GPU 在容器里工作；而（对英伟达 GPU）用 docker 时，让 GPU 工作只需传入「--gpus=all」这么简单。我们建议 AMD 与 Docker 合作，确保 Docker 也能自动检测 AMD 的 GPU，让工作流像用英伟达 GPU 一样顺畅。

![](https://substack-post-media.s3.amazonaws.com/public/images/d46c3ac7-7cdd-4e97-ad4d-d7c7f1fd3d0a_3496x1300.png)
*来源：SemiAnalysis*

## AMD 的 fork 库

AMD 的许多库是从英伟达的开源库或生态库 fork 而来。AMD 使用一个叫 Hipify 的工具，把英伟达 CUDA 源到源翻译为 AMD HIP。动机可以理解，但**他们终究是在竞争对手的平台之上搞建设**，指望靠这种软件开发战略匹敌或超越英伟达的用户体验是不现实的。他们需要把自己的软件贡献到 AMD 生态中。例如，与其通过 fork 英伟达的 TransformerEngine 并做源到源翻译来支持 FP8 训练，不如努力让 PyTorch 原生 FP8 训练在自己的硬件上跑好。目前，AMD 的 PyTorch 原生 FP8 训练配方在 AMD 上根本跑不通，单元测试都还过不了，AMD PyTorch 原生 FP8 训练也没有 CI/CD。

![](https://substack-post-media.s3.amazonaws.com/public/images/25b16d02-fbc7-4a54-b31f-42573d8784e3_1024x330.png)
*来源：SemiAnalysis*

## 给 AMD 的详细建议：如何修复其软件

首先，AMD 需要着力吸引更多软件工程资源，并提高现有工程师的薪酬。目前 AMD 与英伟达的薪酬差距意味着顶尖人才被英伟达而非 AMD 吸引。顶尖人才也更青睐英伟达，因为它能为工程师提供多得多的算力/资源。AMD 应为其内部开发工作采购更多 GPU，并尽快提交一份 MLPerf GPT3 175B 成绩。即使这个成绩眼下无法与英伟达竞争，提交这一基准也将开启迭代改进的进程。

我们还注意到，AMD 经常给客户定制镜像，事实上 AMD 开发者自己也常在这些定制镜像之上工作。这不是最佳实践，因为这意味着 AMD 工程师的体验与公开可得的镜像不一致。AMD 应该反过来，在内部和面向客户时都使用公开镜像，以提升公开镜像的水准，而且 AMD 高管团队应当亲自在内部测试（即 dogfood）那些即将公开发布的东西。

我们建议 AMD 建一个每夜运行的公开仪表盘，展示其硬件在 MLPerf 或 TorchBench 等基准上的性能。该仪表盘还应包含 H100/H200 的性能作为基线。

最后，AMD 需要彻底改变其对环境标志的做法。不应让用户设置一堆标志才能开箱运行，而应把这些标志设为推荐的默认值，让用户快速上手。

AMD 应与 Meta 合作，让生产级训练工作负载在 ROCm 上跑通——PyTorch 用户圈子里众所周知，凡是 Meta 内部不用的 PyTorch 代码路径往往都 bug 成堆。Meta 目前为其生产级 MI300X 推理手写 HIP 内核，但并不用 MI300X 做真正的训练。如果下一版 Llama 的一个小尺寸版本在 AMD 上训练，对 AMD 生态将是极好的改善，也是一场营销胜利。更不用说这将为 AMD 与 Meta 逐步迈向更大模型/更大集群打开大门。Meta 用 AMD GPU 做真实模型训练对两家公司是双赢，因为 Meta 也在寻找英伟达之外的替代训练芯片。

目前，英伟达为 PyTorch 的持续改进和外部开发提供了远超 1,000 块 GPU，内部还有更多。AMD 没有。AMD 需要与专注于 AMD GPU 的新兴 GPU 云合作，让每一代 GPU 都有约 10,000 块用于内部开发和 PyTorch。相比英伟达即将到来的庞大 Blackwell 集群，这仍只有其 1/8，但至少是个开始。这些 GPU 可专用于内部开发和 PyTorch 的 CI/CD。

**Lisa，我们随时可以当面聊聊如何改善 AMD 数据中心 GPU 的用户体验！**

## H100/H200/MI300X 网络 BoM 分析与单位 TCO 性能

除了集合通信和 GEMM 吞吐的基准测试外，我们还做了若干实验，探索对后续基准测试和在集群上运行真实工作负载颇有启发的话题。这些实验涵盖：基准测试的预热（warmup）与重复（repeat）效应、VBoost 功耗切换（Power Shifting）、MLPerf Training GPT-3、BF16 与 FP16 吞吐对比、不同 GEMM 输入分布下的吞吐、每 FLOP 功耗，以及 PyTorch PyPi 发行版与英伟达 NGC 稳定版 PyTorch 镜像的吞吐对比。

我们还针对 1k GPU 以太网、1k GPU InfiniBand、16k GPU 以太网和 16k GPU InfiniBand 集群，给出详细的网络物料清单（BoM）分析，并讨论后端网络使用 51.2T radix 与 25.6T radix 交换机的影响。

最后——我们给出单位 TCO 性能分析，展示 H100/H200/MI300X 在每有效训练 petaflop 的 $/hr 上的高下。以下内容面向所有 SemiAnalysis 订阅者开放，对数据中心运营方、ML 科学家和投资者都将极具参考价值。
