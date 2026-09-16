---
title: "H100 vs GB200 NVL72 训练基准测试——功耗、TCO 与可靠性分析，以及软件随时间的改进"
title_en: "H100 vs GB200 NVL72 Training Benchmarks - Power, TCO, and Reliability Analysis, Software Improvement Over Time"
subtitle: "每 token 焦耳、每百万 token 的 TCO、MFU、按美国家庭年耗电量折算的 token 数、DeepSeek 670B、GB200 可靠性问题、背板停机"
date: 2025-08-20
source: https://newsletter.semianalysis.com/p/h100-vs-gb200-nvl72-training-benchmarks
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball"]
tags: ["Hardware Architecture", "Accelerators", "LLMs", "Chip Design", "AI Infrastructure"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# H100 vs GB200 NVL72 训练基准测试——功耗、TCO 与可靠性分析，以及软件随时间的改进

> 原文：[H100 vs GB200 NVL72 Training Benchmarks - Power, TCO, and Reliability Analysis, Software Improvement Over Time](https://newsletter.semianalysis.com/p/h100-vs-gb200-nvl72-training-benchmarks) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**每 token 焦耳、每百万 token 的 TCO、MFU、按美国家庭年耗电量折算的 token 数、DeepSeek 670B、GB200 可靠性问题、背板停机**

前沿模型训练已把 GPU 和 AI 系统推向绝对极限，成本、效率、功耗、单位 TCO 性能与可靠性也因此成为有效训练讨论的核心。Hopper 与 Blackwell 的对比，并不像 NVIDIA 想让你相信的那么简单。

在本报告中，我们将首先呈现跨越 2,000 多颗 H100 GPU 的基准测试结果，分析模型算力利用率（MFU）、总拥有成本（TCO）以及训练 100 万 token 的成本数据。我们还将讨论能耗：考察每训练一个 token 所消耗的电力焦耳数，并将其与美国普通家庭的年度用电量对比，把能效问题放进社会语境中重新审视。我们还会展示把 GPU 集群从 128 颗 H100 扩展到 2,048 颗 H100、以及在不同版本 NVIDIA 软件下进行分析的结果。

在报告后半部分，我们还将分析 GB200 NVL72 在 Llama4 400B MoE 和 DeepSeek 670B MoE 上的基准测试结果，并将这些数据与前文 H100 的结果对比。我们会讨论：一旦把可靠性问题纳入考量，GB200 NVL72 的单位美元性能优势是否还能成立。

可靠性不佳导致的停机与工程时间损失，是我们在单位 TCO 性能计算中纳入的主要因素之一。目前尚无在 GB200 NVL72 上完成的大规模训练运行，因为软件仍在成熟过程中，可靠性难题也仍在攻克之中。这意味着 NVIDIA 的 H100 与 H200 以及 Google TPU，仍是当今唯一被成功用于完成前沿规模训练的 GPU。就现状而言，即便是前沿实验室和 CSP 中最先进的运营团队，也还无法在 GB200 NVL72 上执行超大规模训练。

话虽如此，每一代新架构都天然需要时间，让生态系统把软件爬坡到能有效利用该架构的程度。GB200 NVL72 的爬坡比前几代稍慢，但差距不大；我们有信心，到今年年底之前，GB200 NVL72 的软件将有显著改善。再加上前沿模型的架构本身就会针对更大的纵向扩展 world size 协同设计，我们预计到今年年底，使用 GB200 NVL72 将带来显著的效率收益。

在可靠性方面，仍将持续存在重大挑战，NVIDIA 必须与合作伙伴更紧密协作才能快速解决；但我们认为，整个生态系统会迅速调动资源，全力攻克这些可靠性难题。

## SemiAnalysis 正在招聘

我们正在寻找一名应届工程师加入我们的工程团队。这是一个独特的机会：在众多行业领袖与 CEO 的支持下，参与高关注度的特殊项目。如果你热爱性能工程与系统可靠性，希望在软硬件交界处施展拳脚，这是一个产生全行业影响的难得机会。

你将参与的工作：

- 构建并运行跨多家厂商（AMD、NVIDIA、TPU、Trainium 等）的大规模基准测试
- 设计可复现的 CI/CD 流水线，将基准测试工作流自动化
- 保障行业合作伙伴所用系统的可靠性与可扩展性

我们期望你具备：

- 扎实的 Python 功底
- 具备站点可靠性工程（SRE）背景或系统级问题解决能力
- 有 CI/CD 流水线与现代 DevOps 实践经验
- 对 GPU、TPU、Trainium、多云与性能基准测试抱有好奇心

申请链接：<https://app.dover.com/apply/SemiAnalysis/2a9c8da5-6d59-4ac8-8302-3877345dbce1>

## 基准测试与分析方法论

在基准测试与分析中，我们采用 NVIDIA DGXC 基准测试团队推出的全新 DGX Cloud Benchmarking Scripts，在 NVIDIA 内部的 H100 EOS 集群上执行，该集群配置了 8×400 Gbit/s InfiniBand 网络。这些结果可作为官方参考基准，供新兴 GPU 云（Neocloud）环境对照——在 Neocloud 与其客户签订服务级别协议（SLA）时即是如此。

各家云厂商也可以向 NVIDIA 提交基准测试结果，若能达到这些 EOS 参考数值，即可获得 NVIDIA Exemplar Cloud（典范云）认证。我们即将发布的 ClusterMAXv2 在评估服务质量时，将重点考量厂商的 Exemplar Cloud 状态——因为这一认证意味着该厂商在大规模 GPU 部署上，能够在多种工作负载中交付参考级性能表现。

上述基准测试基于 NeMo Megatron-LM 进行，但鉴于许多 GPU 最终用户并不只依赖 NeMo Megatron-LM，DGXC 基准测试团队计划将覆盖范围扩展到 TorchTitan 等原生 Torch DTensor 框架。

我们要感谢 NVIDIA DGXC 基准测试团队创建这套基准测试并提供参考数值，助力整个 GPU 云行业的水位提升！

## H100 与 GB200 NVL72 的资本开支、运营开支与总拥有成本分析

过去 18 个月，H100 服务器的价格有所回落，目前约为每台 $190k。对一家典型的超大规模云厂商而言，算上存储、网络及其他项目，每台服务器的前置资本开支总计约 $250k。

再看 GB200 NVL72：对典型超大规模云厂商，仅机柜级服务器本身就要 $3.1M。算上网络、存储及其他项目，每机柜的全套成本约为 $3.9M。

对比从超大规模云厂商、Neocloud 巨头到新兴 Neocloud 的全部三类买家，GB200 NVL72 的每 GPU 全套资本成本约为 H100 的 1.6 至 1.7 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/660ecea3-8430-4b34-908a-f5aa7b406d01_1024x446.png)
*来源：SemiAnalysis*

对比两套系统的运营成本，我们发现 GB200 NVL72 的每 GPU Opex 并不比 H100 高多少。成本差异来自 GB200 NVL72 每 GPU 的整体功耗高于 H100。其主要原因是 GB200 芯片每颗功耗为 1200W，而 H100 为 700W。

![](https://substack-post-media.s3.amazonaws.com/public/images/24d5c68d-8e3d-45a3-808d-0a73f79a87e4_1544x557.png)
*来源：SemiAnalysis*

把资本开支与运营开支都计入、得出总拥有成本（TCO）后，我们看到 GB200 NVL72 的 TCO 约比 H100 高 1.6 倍。这意味着 GB200 NVL72 至少要比 H100 快 1.6 倍，才能在单位 TCO 性能上取得相对 H100 的优势。

![](https://substack-post-media.s3.amazonaws.com/public/images/1b219c54-4bdf-4784-8887-8b00c086ce7d_2560x447.png)
*来源：SemiAnalysis*

## NVIDIA 可以为 ML 社区做得更好的三件事

在深入基准测试结果之前，我们先向 NVIDIA 提出三条关键建议。

第一，我们建议 NVIDIA 扩大基准测试的范围，并进一步提升透明度。要持续抬高整个 GPU 云行业的门槛，NVIDIA 需要同时对其超大规模云合作伙伴和 NVIDIA 云合作伙伴（NCP）进行基准测试，并公开这些数据。这样一来，ML 社区中的任何人在签署价值数千万乃至数亿美元的合同之前，都可以把基准测试数据纳入决策流程。

举个例子，[在 ClusterMAX 评级系统的首次发布中，我们指出 GCP 较老款的 a3-mega H100 在 O(Llama 70B) 量级训练上的 MFU 比平均水平差 10%，在 O(8x7B) 混合专家（MoE）稀疏模型上的 MFU 比平均水平差 15-20%](https://semianalysis.com/2025/03/26/the-gpu-cloud-clustermax-rating-system-how-to-rent-gpus/#google-cloud)。因此，最终用户租用 GCP 时应支付比市场平均低 10-20% 的租金，才能获得与市场平均相同的单位美元性能。如果有一套覆盖各家超大规模云与 NCP 厂商的公开基准测试结果，将极大地方便双方谈出公平的合同价格，并加快决策速度。这能免除旷日持久、成本高昂的概念验证（PoC）运行，为双方节省可观的时间与金钱。

我们的第二条建议是，NVIDIA 把基准测试的覆盖面扩展到 NeMo-MegatronLM 之外，因为许多用户更愿意使用带 FSDP2 与 DTensor 的原生 PyTorch，而非 NeMo-MegatronLM。使用 NeMo-MegatronLM 的一个优势在于：在任何时点，NeMo-MegatronLM 中都有许多尚未进入原生 PyTorch 的性能特性。最新特性先在 NeMo-Megatron 上推出是合理的，但所有这些特性最多应在一个月内上游（upstream）到原生 PyTorch。为此，NVIDIA 应把更多工程师投入到 PyTorch 核心开发，而不是继续给 NeMo 堆功能。NVIDIA 扩展基准测试范围、纳入采用 PyTorch 的运行，也将与这一举措完美衔接。

与其让工程师优化 NeMo，不如让他们去优化 TorchTitan。新的 [NeMo AutoModel](https://github.com/NVIDIA-NeMo/Automodel/) 库是朝正确方向迈出的一步：它在 Megatron-LM 之外还支持原生 PyTorch FSDP2 后端；但明显缺失的是基于 DTensor 的原生 PyTorch 3D+ 并行，许多预训练特性也付之阙如，现有特性大多面向微调。

我们的第三条建议是，NVIDIA 继续加快 GB200 NVL72 背板诊断与调试工具的开发。遗憾的是，即便经过大量的老化（burn-in）流程，NVLink 铜背板的可靠性依然不尽如人意。GB200 NVL72 的运营方还抱怨，用于诊断和调试背板相关错误的工具落后且不好用，使问题雪上加霜。NVIDIA 还可以坚持对 ODM/OEM 合作伙伴执行更严格的验收测试，再把 GB200 NVL72 机柜交付给客户，以改善这一局面。

## GPT-3 175B 的 Token/s/GPU、训练性能与功耗：2024 年 1 月至 2024 年 12 月的成本改进

下表展示了我们在不同时间点、于 128 颗 H100 集群上训练 GPT-3 175B 的基准测试结果。我们选取了从 2024 年 1 月到 2024 年 12 月不同版本的 NeMo-Megatron LM，分别对应 H100 大规模部署开始后一年与两年的时间点。

基准测试配置为 128 颗 H100、4 个数据副本。每个数据副本由 32 颗 GPU 组成，每层在 NVLink 域内跨 4 颗 GPU 做张量并行（即 TP=4），然后再做流水线并行。有人可能认为 TP=8 更好，以匹配 H100 整个 8 GPU 的 NVLink 域 world size；但对 GPT-3 175B 模型来说，TP=4 更优，因为这样算术强度更高。

具体来说，GPT-3 175B 的隐藏维度是 12,288，这意味着若使用 TP=8，K 的归约维度将小至 1,536；相比之下，使用 TP=4 时隐藏归约维度为 3,072。

基准测试的序列长度遵循[原始 GPT-3 论文的设置](https://arxiv.org/pdf/2005.14165)，采用 2,048 的序列长度和 256 个样本的全局批大小。这意味着模型在每次优化器步进之前会看到 500k（全局批大小 × 序列长度）个 token。

![](https://substack-post-media.s3.amazonaws.com/public/images/38b36a55-66ef-44bc-97ee-c65336dd1998_1475x679.png)

看 BF16 模型算力利用率（MFU），12 个月内从 34% 提升到 54%，相当于仅靠 CUDA 软件栈各层的改进，训练吞吐量就提升了 57%。这一改进来自 NVIDIA CuDNN/CuBLAS 工程师编写更优化的 fused wgmma 内核、NCCL 工程师编写占用更少 SM 做通信的更优集合通信原语，以及其他诸多优化。归根结底，起决定作用的是整个软件栈的优化。

FP8 MFU 呈现同样的趋势，同期从 29.5% 提升到 39.5%，仅软件层面就带来 34% 的吞吐量提升。

再看成本：假设 GPU 成本为 $1.42/小时（不含任何租赁毛利），GPT-3 175B 的 FP8 训练成本从 2024 年 1 月的每 100 万 token 72 美分，降到 2024 年 12 月的每 100 万 token 仅 54.2 美分。这意味着，按[原始论文 300B token 的训练量](https://arxiv.org/pdf/2005.14165)计算，GPT-3 175B 的训练成本从 2024 年 1 月的 $218k 降到 2024 年 12 月的仅 $162k。

最后，我们考察训练 GPT-3 的功耗。我们估算 128 颗 H100 集群的整体功率抽取，涵盖 GPU、CPU、网络、存储及其他组件；再按典型托管数据中心的电源使用效率（PUE）进行放大，得出每 token 的整体电力焦耳数。

不情愿地带大家重温一下高中物理：焦耳（Joule）是能量单位，等于 1 牛顿的力沿力的方向移动物体 1 米所做的功。一只 60W 白炽灯点亮一秒消耗 60 焦耳（瓦特（W）是每秒能量消耗的单位），一小时消耗 216kJ。能量的另一种表达方式是瓦时或千瓦时，即设备功率乘以使用小时数。2022 年美国普通家庭的年均能耗为 10,791kWh，约合 38,847,600,000 焦耳。把这 10,791kWh 除以一年的 8,760 小时，得到全年平均功率 1,232W——略高于单颗 GB200 GPU 的 1,200W！

使用 2024 年 12 月版 NVIDIA 软件时，每训练一个 token 消耗 2.46 焦耳（FP8）或 3.63 焦耳（BF16）。如果我们的能源预算相当于美国普通家庭的年度能耗，可以训练 15.8B 个 FP8 token。进一步推算，在 GPT-3 175B 上训练 300B token，FP8 需要相当于 19 个美国家庭年能耗的能源，BF16 则需要相当于 28 个家庭年能耗的能源。

GPT-3 总计 $162k 的训练成本和 19 个家庭的年能耗听起来不算夸张，但正是大量实验和大量失败的训练运行累加起来，构成了我们如今在美国看到的 AI 训练能耗的爆炸式增长。

## 弱扩展 vs 强扩展

强扩展（strong scaling）与弱扩展（weak scaling）描述的是在不同问题设定（例如不同批大小）下扩展算力资源所带来的性能提升。

强扩展指在保持模型规模和全局批大小不变的情况下扩展算力资源。此时可以用阿姆达尔定律（Amdahl's Law）——它描述了通过并行化计算步骤可获得的加速比——来量化强扩展的加速效果。

另一方面，弱扩展指扩展算力资源以在恒定时间内解决更大的问题。AI 训练本质上属于弱扩展：通过增加训练任务使用的 GPU 数量，就可以（视收敛情况）扩大模型规模和全局批大小。

![](https://substack-post-media.s3.amazonaws.com/public/images/e118b2e6-fbeb-4389-b52e-940e75fdea6a_1024x723.png)
*来源：SemiAnalysis、Performance and Scalability – SCENET Summer School*

## Llama3 405B 的 Token/s/GPU、每百万 token 成本、每 token 焦耳 vs GPU 数量（弱扩展）

在这项基准测试中，我们考察随着集群中 H100 GPU 数量增加，Llama3 405B 训练性能的变化——这是弱扩展的一个例子。

在下表中可以看到，当 GPU 集群规模从 576 颗 H100 增加到 2,304 颗 H100 时，FP8 MFU 与 BF16 MFU 在所有规模上分别稳定在约 43% 与 54%。在 [Llama 3 Herd of Models 论文](https://arxiv.org/pdf/2407.21783)公布的训练运行中，研究人员使用 16k 颗 H100 训练 Llama 3 405B，采用类似的并行策略，预训练[实现了 41% 的 BF16 MFU](https://arxiv.org/pdf/2407.21783)。注意上述预训练运行的序列长度为 8192；而在中期训练（mid-training）的上下文扩展阶段，每个样本的序列长度是 131,072 而非 8,192。更长的序列长度需要跨 16 个节点做上下文并行，由于 ring attention 带来的额外通信，MFU 降至 38%。

![](https://substack-post-media.s3.amazonaws.com/public/images/a3edeacd-176b-4c1e-b368-18473a2d70ad_1024x535.png)
*来源：SemiAnalysis*

再看总训练成本：仅执行预训练运行，用 2,304 颗 H100 集群以 BF16 训练 Llama 3 405B、跑完 15T token，成本为每 100 万 token $1.95。仅预训练阶段累计就达 $29.1M，远高于 DeepSeek 等混合专家模型——后者每次训练运行的成本只有 $5M。

当然，我们要再次强调：这一成本只反映单次最终成功的训练运行，而不包括为到达最终阶段所需的大量实验成本、研究人员的雇佣成本等其他开支。

由于 Llama3 405B 的总参数量约为 GPT-3 175B 的 2.3 倍，其每 token 整体电力焦耳数也约为后者的 2.3 倍：分别为每 token 8.8 焦耳与 3.6 焦耳。

这意味着，用美国普通家庭一年的耗电量，Meta 可以在 Llama3 405B 上以 BF16 训练 4.4B 个 token。而要以 15T token 训练至收敛，Meta 需要的能源相当于一个由 3,400 个美国家庭组成的整个社区的年度消耗量。

## Llama3 70B 训练性能：Token/s/GPU、每百万 token 成本、每 token 焦耳 vs GPU 数量（弱扩展）

接下来，我们考察 Llama3 70B 在不同集群规模下的训练性能。当集群规模从 64 颗 H100 增加到 2,048 颗 H100 时，FP8 的性能下降了 10%，从 64 颗 GPU 的 38.1% 降至 2,048 颗 GPU 的 35.5%。有趣的是，MFU 竟然下降了这么多（以百分比计——鉴于 MFU 基数本身不高，百分比降幅才是真正要紧的），因为随着规模扩大，每个数据副本的批大小并没有改变，并行策略也没有改变。所有运行仍然沿用 TP=4、PP=2、context parallel=2——唯一真正的变化是增加了更多数据副本。有意思的是，BF16 的 MFU 降幅要小得多，仅 1-2%，从 64 颗 H100 的 54.5% 降至 2,408 颗 GPU 的 53.7%。

![](https://substack-post-media.s3.amazonaws.com/public/images/5745ecee-4c3a-4d79-9128-c62e755aedf9_1767x925.png)

Llama3 405B 比 Llama3 70B 大 5.7 倍，而且与所有稠密模型一样，所需 FLOPs 与参数量成线性关系。因此，Llama 3 405B 的训练成本应当是 Llama 3 70B 的 5.7 倍。实际上，在约 2k 颗 H100 的规模下，以 BF16 的每百万 token 成本计，Llama3 405B 贵 5.4 倍。

在功耗方面，FP8 下用 2,408 颗 H100 训练时，每 token 能耗比用 64 颗 H100 训练高 10%。在 64 颗 H100 上以 FP8 训练 Llama 3 70B 至 15T token 收敛，仅需相当于 440 个美国家庭年能耗的能源；而在 2,048 颗 H100 规模上，则需要相当于 472 个美国家庭年能耗的能源。

## Llama3 8B 训练性能随时间的变化

Llama3 405B 和 Llama3 70B 等更大的模型同时使用张量并行、流水线并行和数据并行，而训练 Llama3 8B 只需要在 NVLink 域内每对 GPU 之间跨 8,192 序列长度做上下文并行，并用数据并行把工作分摊到其他 GPU 对上。在这项分析中，我们还考察了训练性能随时间的变化，以衡量整个软件栈的改进对训练性能的影响。我们看到，从 2024 年 11 月到 2025 年 4 月——后者距 Hopper 开始大规模部署已整整 23 个月——性能只有轻微提升。

![](https://substack-post-media.s3.amazonaws.com/public/images/7168e971-f701-4d8c-9739-0b0262435014_2260x1099.png)

在下一节中，我们将深入对比 GB200 NVL72 训练性能的现状与 H100 上的训练。我们将讨论训练 DeepSeek 670B MoE 和 Llama4 400B MoE 的基准测试，分析 GB200 相对 H100 的单位总拥有成本（TCO）性能。

我们还将聚焦前文提到的 GB200 NVL72 诊断与调试工具的缺失，讨论造成 GB200 NVL72 不可靠的诸多问题。这些正是 NVIDIA、CSP、Neocloud 以及前沿实验室的最终用户必须解决的挑战，只有这样，才能在今年年底之前在 GB200 NVL72 上成功且具成本效益地训练前沿模型。
