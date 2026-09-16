---
title: "NVIDIA Blackwell 性能与 TCO 分析：B100 vs B200 vs GB200 NVL72"
title_en: "Nvidia Blackwell Perf TCO Analysis - B100 vs B200 vs GB200NVL72"
subtitle: "GPT-4 盈利能力、成本、推理模拟器、并行策略详解、大模型与小模型推理和训练的性能 TCO 建模"
date: 2024-04-10
source: https://newsletter.semianalysis.com/p/nvidia-blackwell-perf-tco-analysis
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# NVIDIA Blackwell 性能与 TCO 分析：B100 vs B200 vs GB200 NVL72

> 原文：[Nvidia Blackwell Perf TCO Analysis - B100 vs B200 vs GB200NVL72](https://newsletter.semianalysis.com/p/nvidia-blackwell-perf-tco-analysis) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**GPT-4 盈利能力、成本、推理模拟器、并行策略详解、大模型与小模型推理和训练的性能 TCO 建模**

NVIDIA 发布 B100、B200 和 GB200 所引发的关注甚至超过了 iPhone 发布会——至少在全世界的极客圈子里是如此。所有人真正想问的问题是：真实的性能提升到底是多少？NVIDIA 宣称 30 倍，但这是真的吗？更进一步说，真正的问题其实是：[性能/TCO](https://www.semianalysis.com/p/gpu-cloud-economics-explained-the) 究竟如何？

上一代的 H100 相对 A100 的性能/TCO 提升并不理想，原因在于价格大幅上涨——[在推理场景中 A100 的 TCO 实际上优于 H100](https://www.semianalysis.com/p/inference-race-to-the-bottom-make)，因为 H100 的内存带宽提升乏善可陈，而且价格较 A100 在 2022 年三季度的谷底价大幅上涨。不过这影响不大，因为 AI 行业对训练（而非推理）的庞大需求更能受益于 H100 更强的 FLOPS 性能，而且大部分涨价来自 NVIDIA [机会主义式的高利润率](https://www.semianalysis.com/p/nvidia-b100-b200-gb200-cogs-pricing)。

到了 Blackwell，这一切都变了，因为代际之间的价格涨幅远没有之前那么大。这要归因于市场上存量的庞大 H100 和 H200 所带来的竞争，以及新入场的挑战者——[超大规模云厂商的自研芯片](https://www.semianalysis.com/p/accelerator-model)、AMD 的 MI300X 和英特尔的 Gaudi 2/3 都在进入市场，并各自抛出性能/TCO 方面的论据。因此，NVIDIA 必须拿出有说服力的理由来推销其新一代产品。当然，[他们不会让竞争对手蚕食自己的地盘](https://www.semianalysis.com/p/nvidias-plans-to-crush-competition)，定价非常激进，[甚至可以说是厚道](https://www.semianalysis.com/p/nvidia-b100-b200-gb200-cogs-pricing)。

![](https://substack-post-media.s3.amazonaws.com/public/images/1cfad893-285e-4464-876a-c06e457c777a_3022x1964.png)
*来源：NVIDIA*

NVIDIA 宣称 Blackwell 相对 Hopper 的性能提升最高可达 30 倍。问题在于，这个 30 倍的数字基于一个非常特定的最佳场景。需要说明的是，这个场景当然是现实的、有可能实现的（撇开不公平的量化精度差异不谈），但它并不是一个能代表整个市场典型情况的场景。今天，让我们逐一拆解 NVIDIA 的性能宣称，并借助我们构建了一年半多的 LLM 模型性能模拟器，聚焦于各种应用场景下的实际性能提升，包括不同规模模型的推理与训练。我们还将剖析竞争对手在销售商用芯片（merchant silicon）时是否真有机会，以及尽管成本差距巨大，超大规模云厂商的自研硅芯片与 NVIDIA 新品相比究竟有没有竞争力。

有若干主要工作负载值得跟踪，它们各有不同的特性。推理与训练显然差异很大，因为训练存在反向传播（backward pass），batch size 也不同。使用大尺寸模型同样会带来截然不同的性能特征，因为需要突破 GPU 和节点的边界——例如把并行扩展到典型 HGX H100 服务器的 8 张 GPU 之外。

如今许多人在讨论性能时倾向于聚焦小模型推理（<1000 亿参数），但随着 Blackwell 大幅压低推理成本，加上小模型持续难以很好地满足工作负载需求，再结合 Databricks DBRX 132B、xAI Grok-1 314B、Cohere Command R+ 104B、Mistral 8x22B 等开放模型的发布，以及即将发布的 Meta LLAMA 3，重心显然将重新转回大模型的推理性能。

超过 1000 亿参数的模型将成为「小模型」微调与推理的新常态，而超过 1 万亿参数的稀疏模型将成为大模型的常态。需要说明的是，这些大模型今天已经占据了推理和训练算力的绝大部分。随着未来的模型发布，大模型的门槛只会越抬越高。请记住：硬件要在经济上划算，就必须能持续服役并保持有效 4-6 年，而不只是撑到下一次模型发布。

在深入我们的 LLM 性能模拟器及其对大模型与小模型、推理与训练的结论之前，先从规格说起。

## **规格——远不止表面所见**

主题演讲中展示的性能提升是通过多个维度的改进实现的——其中最基础、也最容易理解的因素，就是内存带宽与浮点运算（FLOPS）能力的提升。

风冷的 700W B100 将[率先出货](https://www.semianalysis.com/p/nvidia-b100-b200-gb200-cogs-pricing)，提供 1,750 TFLOPS 的 FP16/BF16 算力。B100 的基板被设计为直接插入当今 HGX H100 系统所用的同一套设计——这迫使 B100 以更低的功耗和时钟频率运行，以维持在现有系统的散热包络之内。B100 出货后不久，B200 将以更高功耗、更快时钟频率上市，提供 2,250 TFLOPS 的 FP16/BF16 算力。此外，GB200 NVL72 采用液冷，可以让 Blackwell GPU 在更高的功耗水平上运行，解锁更多性能上限——提供 2,500 TFLOPS 的 FP16/BF16 算力——相对 H100 和 H200 提升 153%。另外还有一款 1200W 的 B200，未包含在表中。

![](https://substack-post-media.s3.amazonaws.com/public/images/beb184fa-9881-4032-8bf4-c538550b96a1_1154x747.png)
*来源：NVIDIA、SemiAnalysis*

B100 的 FP16 和 TF32 FLOPS 仅提升 77%，但随着功耗提升，并叠加更进一步的量化，总 FLOPS 最多可扩展到 4 倍。内存带宽——可以说是最重要的一项规格升级——从 H100 的 3.4 TB/s 和 H200 的 4.8 TB/s 提升到 Blackwell 家族最高 8.0 TB/s——这最直接地改善推理吞吐量和交互性（每用户每秒 token 数），因为[推理常常受限于内存带宽](https://www.semianalysis.com/p/inference-race-to-the-bottom-make)。

我们要指出，即使在最差场景（FP16 对 FP16）下，FLOPS 也有 153% 的代际提升，但内存带宽的增幅更小。从 A100 到 H100 的带宽增幅大于这一代。[内存墙是 AI 行业未来扩展面临的最大挑战之一。](https://www.semianalysis.com/i/97006309/machine-learning-training-components)

![](https://substack-post-media.s3.amazonaws.com/public/images/dc7c8bd6-c489-49ba-a1fe-5dfbd874f847_1350x800.png)
*来源：NVIDIA、SemiAnalysis*

更重要的是看 FLOPS 乘以位数再除以带宽这个指标，它才揭示真实情况。在大多数数值格式下，这个比率大致不变，也就是说，要完全利用 FLOPS 所需的算术强度保持稳定。撇开新数值格式的出现不谈，大多数代码在给定算术强度下移植后应能达到相近的利用率。不过，一旦 Blackwell 张量核心的全部新特性被充分利用，Blackwell 的 MFU 总体上应当优于 Hopper。

然而——看待这些性能提升时必须放在这样一个背景下：Blackwell 的硅片面积（约 1600mm2、2080 亿晶体管）是 Hopper（约 800mm2、800 亿晶体管）的两倍。由于[摩尔定律放缓和 3nm 的种种问题](https://www.semianalysis.com/p/tsmcs-3nm-conundrum-does-it-even)，NVIDIA 在没有真正制程节点收缩的情况下必须交付代际性能提升。通过运用 DTCO 和[约 6% 的光学工艺微缩](https://www.semianalysis.com/i/92075531/nm-process-family-technology-detailed)，Blackwell 仍然实现了两倍于 Hopper 的性能。

看每平方毫米硅片的原始 TFLOPS，即以逻辑制造成本为基准来衡量，B100 交付的性能其实是缩水的：FLOPS 提升 77%，而硅片面积增长约 100%。这是为了快速上市而把频率压低、塞进现有 700W 平台的结果；只有到 B200 和 GB200 NVL72，我们才看到单位硅片面积的性能改进。

按硅片面积增益归一化后，风冷 B200 每单位硅片面积的 FP16 FLOPS 仅提升 14%——对一套全新架构来说实在说不上亮眼。因为大部分性能增益不过来自更多的硅片面积和量化。人们需要理解微缩（microscaling）的运作方式，并基于 Blackwell 架构解决 FP8、FP6 和 FP4 训练问题。

###### 另请注意：本文全文中，我们将 H100 和 H200 的 FP4 和 FP6 FLOPS 视为与 FP8 FLOPS 相同。虽然以 FP4 从内存加载后再向上转换为 FP8 存在轻微开销，但在算力受限场景下，内存带宽的节省足以降低功耗，并为达到峰值 FLOPS 留出更多余量，在真实使用场景中这实际上抵消了那部分开销。

基于硅片面积翻倍理应消耗翻倍功耗这一前提，分析等功耗（isopower）性能提升就很重要了——也就是每 GPU 每瓦特所能达到的 FLOPS。

![](https://substack-post-media.s3.amazonaws.com/public/images/a440249d-8c9d-44e7-9b10-0c4a908f5583_1123x994.png)
*来源：NVIDIA、SemiAnalysis*

B100 在同样 700W 功耗下确实多交付了 77% 的 FP16/BF16 FLOPS，但对 B200 和 GB200 而言，每向芯片追加一单位功耗所带来的 FLOPS 增益都在递减。GB200 相对 H100 每 GPU 瓦特 TFLOPS 提升 47%——这有帮助，但如果没有进一步的模型量化，依然谈不上惊艳，当然也远不足以支撑主题演讲中展示的 30 倍推理性能。

FLOPS 成本方面同样平淡无奇。GB200 NVL 和 B200 的每美元 TFLOPS 没有实质性的差别。

![](https://substack-post-media.s3.amazonaws.com/public/images/9321ee09-03cf-4b27-8da2-f040d3439ecf_1259x670.png)
*来源：NVIDIA、SemiAnalysis*

正如上述简单分析所表明的，规格本身只是故事的一小部分，宣称的 30 倍推理性能提升绝大部分来自量化，以及沿着其他改变格局的维度所做的架构改进。

## **模型性能探究**

NVIDIA 宣称 GB200 相对 H200 有 30 倍性能提升，但正如上述分析所示，任何单一规格都远达不到这个提升幅度。

这怎么可能？原因在于：系统的重要性超过了单颗芯片的规格。[FabricatedKnowledge](https://www.fabricatedknowledge.com/p/the-data-center-is-the-new-compute) 曾就黄仁勋念叨多年、如今终于在 GB200 NVL72 上兑现的那句「数据中心就是计算单元」写过一篇精彩的思考文章。我们要指出，就机器学习硬件而言，NVLink 背板和机柜级产品并不是什么新事物。

Google 自 2018 年起就在出货由无源铜互连起来的 64 TPU 子切片（subslice），超出这个范围的部分用光互连连接，而且机柜全部水冷。TPUv5p（Viperfish）与 TPUv5e（Viperlite）除了芯片级规格之外的主要区别在于：v5e（Viperlite）用铜互连连接 256 个 TPU 且不再向外扩展，而 v5p（Viperfish）用铜互连连接 64 个 TPU，再[通过光路交换机（OCS）](https://www.semianalysis.com/p/google-apollo-the-3-billion-game)连接到其余共 8960 个 TPU 的 pod。

下面这张图大概是我们见过的关于机器学习性能建模和最优总拥有成本（TCO）搜索空间最酷的一张图。它揭示了大量关于 LLM 性能建模与趋势的信息，还展示了多种不同的并行策略和 batch size。

![](https://substack-post-media.s3.amazonaws.com/public/images/4a9e89b3-7ab9-4f0e-b407-4b9f6d9d2b5a_3024x1964.png)
*来源：NVIDIA*

在单张 GPU 上运行较小模型的推理时，通常会得到类似下面这样的曲线：低 batch size 下交互性（每用户每秒 token 数）非常高，随着 batch size 增大，吞吐量上升，但交互性随之下降。面向所有用户的系统吞吐量（每 token 成本）与单用户交互性（用户体验）之间存在一条权衡曲线。

![](https://substack-post-media.s3.amazonaws.com/public/images/2acdcefd-586b-44e3-9a77-58652e23dcf1_1352x926.png)
*来源：SemiAnalysis*

不幸的是，对于 GPT-4 这样的巨型模型，单条权衡曲线的简洁性不复存在。巨型模型必须被切分到许多 GPU 上，这带来了大量复杂性。

例如，GPT-4 MoE 拥有 55B 注意力参数和 16 个各有 111B 参数的专家，分布在 120 层上，总计 1.831 万亿参数、每参数 8 比特，总共需要 1,831 GB 内存。

![](https://substack-post-media.s3.amazonaws.com/public/images/4eaceeb1-4ff6-423e-bb39-022a11578271_544x530.png)
*来源：SemiAnalysis*

这个模型不可能装进单张 GPU，甚至装不进一台 8 GPU 服务器。因此，它必须被切分到数十张 GPU 上。模型如何切分非常重要，因为每一种不同的切分配置都意味着截然不同的性能特征。

让我们从简单的开始，逐步深入。

## **推理并行技术——流水线并行、张量并行、专家并行与数据并行**

并行（parallelism），即把任务切分到多张 GPU 上，仅就「让模型装进系统」而言已是必需。但正如我们将看到的，并行的作用远不止缓解这一容量约束。让我们讲解最重要的几种并行形式，以及各种并行配置的组合为何是性能提升的核心。我们先给出一个忽略部分复杂性的简化讲解，使之更易理解，然后再进入考虑了 KV 缓存、预填充（prefill）以及各种内存、计算与通信开销的真实模型。

## **流水线并行**

流水线并行（pipeline parallelism）是最简单的并行形式：模型的各层被切分到多张 GPU 上——在下面这个使用 GPT-4 MoE 的例子中，120 层被切分到 16 张 GPU 上。

每个用户查询中的每个 token 在前向传播中依次穿过每张 GPU、经过所有层，直到跑完整个模型。由于每张 GPU 上的层数更少，模型现在可以装进这 16 张 GPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/eab501e6-cfde-455a-881f-a0e5f1bfd1ff_2539x806.png)
*来源：SemiAnalysis*

然而——由于查询中的 token 仍然必须按顺序通过流水线并行设置中的所有 GPU——交互性（每用户每秒 token 数）没有净提升。

把上面的 PP16 配置与假想的单 GPU 部署相比较，交互性是一样的（忽略了单 GPU 系统的 FLOPS 与内存容量约束——在 100 个用户对 GPT-4 MoE 做推理的情况下会触发该约束）。

流水线并行的主要好处是缓解内存容量压力——让模型装得下，而不是让它跑得快。流水线的每个 stage 会按顺序处理各自的一组用户。

## **张量并行**

流水线并行和张量并行（tensor parallelism）都有突破内存容量约束（即让模型装进系统）的好处，但在张量并行中，每一层的工作都被分布到多张 GPU 上，通常沿隐藏维度（hidden dimension）切分。中间结果通过跨设备的 all-reduce 多次交换——每一层的自注意力、前馈网络和层归一化中都有。这要求高带宽，尤其需要极低的延迟。

![](https://substack-post-media.s3.amazonaws.com/public/images/3e7a9974-01ee-4df6-8f5c-a56d2bbbff28_1772x1002.png)
*来源：Accelerating PyTorch Model Training*

实际上，扩展域内的每张 GPU 都与其他所有 GPU 一起协同处理每一层，就好像它们是一颗巨型 GPU。下图展示了 DGX H100 内部的两张网络——即 NVLink 纵向扩展（scale up）网络（连接到 NVSwitch 的多色通道）和通过橙色 ConnectX-7 网卡访问的 InfiniBand/以太网横向扩展（scale out）网络。

像 NVLink 和 Google 的 ICI 这样的纵向扩展网络，使张量并行比横向扩展网络快得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/13ac39d3-633c-4c45-ba6a-4fe500bd639b_1595x941.png)
*来源：NVIDIA*

张量并行允许内存带宽在所有 GPU 之间池化共享。这意味着前向传播中为每层加载模型参数时，可用的不再是 8,000 GB/s 的内存带宽，而是 128,000 GB/s。

在下面这个例子中，交互性（每用户每秒 token 数）是 PP16 例子的 16 倍——69.9 tokens/秒/用户，而 PP16 系统只有 4.4。在这个简化例子中，系统总吞吐量也相应是 16 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/74337f00-53fb-4374-9ec1-6766cff693ba_1506x549.png)
*来源：SemiAnalysis*

不过，上面展示的例子是完美场景，没有考虑导致实际观测到的内存带宽利用率（MBU）降低的各种因素。这里最值得注意的影响是 GPU 之间 all-reduce 和 all-to-all 操作的需求所带来的通信惩罚。张量并行中的 GPU 数量越多，这一效应对交互性和吞吐量的削弱就越明显。

现实中，流水线并行由于 GPU 间通信瓶颈更少，吞吐量高于张量并行。它通常也能达到更高的 batch size / MFU。

## **专家并行**

在张量并行中，所有 GPU 协同承载所有层；而在专家并行（expert parallelism）中，专家被切分到不同的 GPU 上，但注意力部分是复制的。

在下面这个 EP16 系统的例子中，每张 GPU 承载一个专家。这使得每个专家域加载的总参数降至仅 166B，即复制的注意力 55B 加上每个专家 111B。

![](https://substack-post-media.s3.amazonaws.com/public/images/06728865-70bd-47f5-a172-96d140d783a0_1505x617.png)
*来源：SemiAnalysis*

每个专家域还必须加载注意力权重，这一事实以每 token 内存带宽需求的形式带来了额外开销。因此，由于专家并行相对张量并行有更高的内存带宽需求，EP16 例子中可用内存带宽与加载模型所需带宽之比低于 TP16 例子，导致 EP16 的交互性为 48.2、低于 TP16 的 69.9，吞吐量也相应更低。

回想一下，使用张量并行会对内存带宽利用率施加重大的通信惩罚，拖慢吞吐量。这一效应与专家并行中注意力层的额外开销方向相反——而通信惩罚的程度决定了哪个效应占主导。

![](https://substack-post-media.s3.amazonaws.com/public/images/40993087-bf48-4246-bf0b-e29640cad46c_1683x1006.png)
*来源：A Hybrid Tensor-Expert-Data Parallelism Approach to Optimize Mixture-of-Experts Training. Singh et al.*

如上图所示，专家并行同样存在通信开销，但切分专家域并复制注意力意味着开销显著降低。基本上，图中右侧的 All Reduce 和 All to All 操作在专家并行中不需要执行。我们还要指出，并行 transformer（parallel transformers）在推理和训练成本上有巨大改进，尤其是随着模型规模扩大，正是因为每层内部所需的通信更少。不过，至少在开源模型的世界里，大规模实现它们仍有挑战。

## **数据并行**

数据并行（data parallelism）大概是所有并行形式里最简单的——本质上是复制系统的一切，不共享、也不整合任何系统资源。就像在美国和亚洲各部署一台 web 服务器：不同用户访问各自的服务器，跑的是同样的东西，但彼此完全独立。

在下面的例子中，交互性没有提升，因为每个 TP16 数据并行系统都已经撞上内存墙。保持总用户数 100 不变，总吞吐量也与 TP16 例子相同。数据并行扩大了在撞上 FLOPS 约束之前可以增加用户数的余量，因为总共有 32 张 GPU 的 FLOPS 可用（TP16 为 16 张），但如果我们不向系统引入更多用户、从而产生更多吞吐量，那么从 TP16 升级到 TP16 DP2 就是资源浪费。

![](https://substack-post-media.s3.amazonaws.com/public/images/044b8bea-9bad-4c36-a92d-d5e046d1ec3a_1290x1103.png)
*来源：SemiAnalysis*

如果我们在之前的 TP16 系统例子上保留那 100 个用户，但部署两套数据并行系统——即总共 200 个用户——那么吞吐量会翻倍。数据并行最重要的好处是没有开销，因为每个数据并行系统完全独立运行。我们要指出，对于其他系统，为了讲解简单我们随手略去了所有开销；而数据并行是真的没有任何开销！

## **并行的堆叠**

我们还可以把各种并行方案堆叠起来，以匹配给定的模型、用户数、交互性与吞吐量目标。

在下面这个 TP2 EP8 并行的例子中，我们实现了 8 个专家域，每个域内两张 GPU 以 TP2 张量并行方式运行。与 EP16 并行相比，每个专家域现在要加载两个专家的参数加注意力，而不是一个专家的参数加注意力——从而减少了总体所需的内存容量和带宽开销。因此，TP2 EP8 的系统总参数内存需求更低，为 2,216 GB，而 EP16 为 2,656 GB。

这带来了更高的交互性：TP2 EP8 为 57.8 tokens/秒/用户，EP16 为 48.2 tokens/秒/用户。不过，虽然内存容量/带宽开销更低，转向 TP2 EP8 会引入通信惩罚——本分析同样略去了这一点。

![](https://substack-post-media.s3.amazonaws.com/public/images/6587136e-afb4-47f1-87c1-2677f09b00ef_2562x992.png)
*来源：SemiAnalysis*

## **72 路并行堆叠**

[GB200 NVL72 的发布掀起波澜](https://www.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband)——[部分原因算是出于误会](https://www.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband)——并让人们对液冷含量增加、数据中心功率密度大幅提高浮想联翩。NVL72 在 72 张 GPU 之间实现了 900 GB/s 单向带宽的无阻塞 all-to-all 网络，远快于 InfiniBand/以太网横向扩展网络目前提供的 50 GB/s（400G）。比带宽提升更重要的是，NVL72 还实现了更低的延迟。

把这一切放在一起看——NVL72 的核心创新在于极大地扩展了 NVLink 网络所能支持的并行方式集合。H100 和 H200 的 8 GPU NVLink 网络只允许少量配置——例如，张量并行与专家并行的实用排列组合清单并不长：(TP1 EP8)、(TP2 EP4)、(TP4 EP2) 和 (TP8, EP1)。我们说「实用」，是因为你当然可以把张量并行扩展到单台服务器之外，但那样做会毁掉你的性能。

## **H200 的「最糟发型日」基准测试**

观察在 FP8 下运行 GPT-4 的 H200 时，随着张量并行所用 GPU 数量的增长，并行方案选择的帕累托最优前沿会出现相当严重的断崖式下跌。

在 TP8 时，GPU 之间全部通过 NVLink 通信，因此随着交互性（每用户每秒 token 数）的提升，惩罚还不算太糟；但紧接着，吞吐量突然一落千丈。这是因为张量并行被扩展到了 8 张 GPU 之外。把交互性从约 6.3 提高到约 6.5，会导致每 GPU 总吞吐量下降约 23%。这是非常剧烈的影响，原因就在于张量并行的通信此时必须跨出 NVLink 网络的边界、走上 InfiniBand/以太网。

![](https://substack-post-media.s3.amazonaws.com/public/images/b0785926-1950-4646-bb19-fea9b8da2bfa_1361x937.png)
*来源：NVIDIA、SemiAnalysis*

主要原因在于，经过 ConnectX-7 NIC 再加上一台网络交换机，从一张 GPU 到另一张 GPU 的延迟相对较高。此外，跨服务器传输通常还要穿过 DSP 和光模块，或者 AEC。相比之下，NVLink 网络只需经过 NVLink 交换机，其余全部是短距铜互连。

而且，当张量并行规模触及超过 16 张和 32 张 GPU 时，这种影响会再度出现。

有鉴于此——再回头看主题演讲的那张幻灯片——请注意 NVIDIA 所用的幻灯片选择以 TP64 作为基准，而那正是在 H200 上能跑的最糟糕的并行方案。

![](https://substack-post-media.s3.amazonaws.com/public/images/434d2373-17aa-4bba-9105-56ad0745bcfe_1584x992.png)
*来源：NVIDIA*

不仅如此，NVIDIA 还故意用 FP8 束缚了 H200 和 B200 系统的手脚，而 GB200 却用 FP4。所有这些系统从内存角度看都能受益于 FP4，那会把所有曲线在交互性指标上向右推。此外，B200 被限制在 FP8，尽管它的 FP4 FLOPS 是两倍。

解释 30 倍性能提升的最明显因素，是 GB200 NVL 的 FP4 性能与使用 FP8 量化的 H200 和 B200 之间的对比。在我们的模拟器中剥离这一层之后，**从 H200 到 GB200 我们只剩约 18 倍的性能增益**。远不如 NVIDIA 渲染的 30 倍那样惊悚，但仍然是一项极其了不起的成就。

下一个影响最大的因素则更微妙一些——基准测试场景对 GPT-4 施加了 32k 输入、1k 输出，并且所有基准都带有一个 5 秒首 token 时间（TTFT）生成约束。预填充（prefill）极度受 FLOPS 限制，因此任何这方面的约束对 H200 这样 FLOPS 较低的系统都非常严苛。此外，通过把每用户的预填充 token 拉满、把解码压到最少，这些约束变得更加苛刻。

这个场景通过有效地排除所有使用 H200 系统的大 batch size 配置来操纵基准测试，因为在 H200 系统上跑大 batch size 会因 FLOPS 较低而远超 5 秒首 token 时间约束。没有大 batch size，H200 系统就无法交付高的系统总吞吐量——这意味着 H200 曲线低于如果没有那 5 秒约束时本可达到的水平。

需要说明的是，更低的首 token 时间当然非常理想，但那是需要用户自己去权衡和做出的取舍。这个基准测试压缩了 H200 系统在吞吐量方面本可达到的性能包络，尽管代价是首 token 时间上的某些折中。

如果换成 512 输入、2k 输出的场景，同样施加 5 秒首 token 时间（TTFT）和 20 的交互性要求，**性能提升不到 8 倍。**我们并不确定实际大规模部署中输入与输出 token 的比例，也可能确实很多人需要极高的输入、极低的输出比例。智能体及其他新兴工作负载的预填充与解码比例，有可能比 NVIDIA 展示的 32:1 还要高。

即便剥去纯规格与营销花招的影响，在这个精心挑选的场景中，得益于架构和网络方面的增益，性能提升依然可观。

[分享](https://newsletter.semianalysis.com/p/nvidia-blackwell-perf-tco-analysis?utm_source=substack&utm_medium=email&utm_content=share&action=share)

接下来，让我们转而考察在我们认为更现实的场景下——各种模型规模、训练与推理——的真实性能与 TCO 提升。此外，还将深入探讨这些性能提升对推理系统盈利能力的驱动作用。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

## **真实性能与 TCO 提升**

当我们运行模型模拟器时，各 GPU SKU 得到的性能提升差异很大。接下来，让我们深入探讨从 H100/H200 到 B100、B200 和 GB200，大模型与小模型在训练和推理两方面的性能与 TCO 提升。此外，我们还将给出规模化 GPT-4 每套推理系统的营收、成本与盈利能力数字。
