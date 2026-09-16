---
title: "100,000 H100 集群：供电、网络拓扑、以太网 vs InfiniBand、可靠性、故障与检查点"
title_en: "100,000 H100 Clusters: Power, Network Topology, Ethernet vs InfiniBand, Reliability, Failures, Checkpointing"
subtitle: "前沿模型扩展的挑战与要求、通过内存重构实现故障恢复、机柜布局"
date: 2024-06-17
source: https://newsletter.semianalysis.com/p/100000-h100-clusters-power-network
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 100,000 H100 集群：供电、网络拓扑、以太网 vs InfiniBand、可靠性、故障与检查点

> 原文：[100,000 H100 Clusters: Power, Network Topology, Ethernet vs InfiniBand, Reliability, Failures, Checkpointing](https://newsletter.semianalysis.com/p/100000-h100-clusters-power-network) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**前沿模型扩展的挑战与要求、通过内存重构实现故障恢复、机柜布局**

有一派观点认为，自 GPT-4 发布以来，AI 能力便陷入停滞。这大体属实，但原因只是没有人能够大规模增加投入给单个模型的算力。已发布的每一个模型大体都处于 GPT-4 的水平（训练算力约 2e25 FLOP）。这是因为投入给这些模型的训练算力也大致处于同一水平。以 Google 的 Gemini Ultra、Nvidia Nemotron 340B 和 Meta LLAMA 3 405B 为例，其投入的 FLOPS 与 GPT-4 相比处于相近量级甚至更高，但采用的架构更差，导致这些模型未能解锁新的能力。

![](https://substack-post-media.s3.amazonaws.com/public/images/ce07f3c8-eaf9-4152-9ca9-581eac73ba04_1252x741.png)
*来源：SemiAnalysis 估算*

虽然 OpenAI 拿到了更多算力，但他们主要把算力用于打造更小、过训练程度更高、推理成本更低的模型，例如 GPT-4 Turbo 和 GPT-4o。OpenAI 承认，[他们最近才开始训练下一档级别的模型](https://openai.com/index/openai-board-forms-safety-and-security-committee/)。

AI 显而易见的下一步，是用海量视频、图像、音频和文本来训练一个数万亿参数的多模态 transformer。[至今还没有人完成这项任务](https://openai.com/index/openai-board-forms-safety-and-security-committee/)，但争夺第一的竞赛已是一片热火朝天。

[包括但不限于 OpenAI/Microsoft、xAI 和 Meta 在内的多家大型 AI 实验室](https://www.semianalysis.com/p/accelerator-model)正在竞相构建拥有超过 100,000 个 GPU 的 GPU 集群。这些单体训练集群仅服务器资本开支就超过 40 亿美元，而且还[严重受制于数据中心容量和电力的短缺](https://www.semianalysis.com/p/ai-datacenter-energy-dilemma-race)，因为 GPU 通常需要部署在同一地点以实现高速芯片间网络互联。一个 100,000 GPU 的集群需要 >150MW 的数据中心容量，一年要吞掉 1.59 太瓦时（terawatt hour）电力，按 $0.078/kWh 的标准电价计算，电费高达 1.239 亿美元。

![](https://substack-post-media.s3.amazonaws.com/public/images/ed6477c4-c1ec-4d91-ac90-b23667b849fd_1032x455.png)
*来源：SemiAnalysis，美国能源信息署（US EIA）*

今天我们将深入探讨大型 AI 训练集群及其周边基础设施。构建这些集群远不是砸钱就能解决的问题。而要用它们实现高利用率则更加困难，因为各类组件（尤其是网络）的故障率很高。我们还将逐一讲解供电挑战、可靠性、检查点（checkpointing）、网络拓扑方案、并行策略、机柜布局，以及这些系统的完整物料清单（BOM）。一年多前，[我们曾报道过 Nvidia 的 InfiniBand 问题](https://www.semianalysis.com/p/nvidias-infiniband-problem-qmx-ai)，该问题导致一些公司选择 Spectrum-X 以太网而非 InfiniBand。我们还将讨论 Spectrum-X 的重大缺陷——正是它让超大规模云厂商转向了 Broadcom 的 Tomahawk 5。

为了直观感受一个 100,000 GPU 集群能提供多少算力：[OpenAI 训练 GPT-4 的 BF16 FLOPS 约为 ~2.15e25 FLOP（21.5 百万 ExaFLOP）](https://www.semianalysis.com/p/gpt-4-architecture-infrastructure)，使用约 20,000 张 A100，历时 90 到 100 天。那个集群的峰值吞吐量仅有 6.28 BF16 ExaFLOP/秒。而在 100k H100 集群上，这个数字将飙升至 198/99 FP8/FP16 ExaFLOP/秒。与 20k A100 集群相比，峰值理论 AI 训练 FLOPS 提升了 31.5 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/e7010330-0448-4c8f-8120-8ba71a0986b5_1065x325.png)
*来源：Nvidia，SemiAnalysis*

在 H100 上，AI 实验室在万亿参数训练任务中已实现高达 35% 的 FP8 模型 FLOPS 利用率（MFU）和 40% 的 FP16 MFU。回顾一下，MFU 是衡量在计入各种开销与瓶颈（[功率限制](https://www.thonking.ai/p/strangely-matrix-multiplications)、通信抖动、重计算、[掉队者（straggler）](https://pytorch.org/blog/straggler-mitigation/)以及低效 kernel）后，对峰值潜在 FLOPS 的有效吞吐量和利用率指标。一个 100,000 H100 集群用 FP8 训练 GPT-4 只需四天。在 100k H100 集群上跑一次 100 天的训练，可以实现约 ~6e26（600 百万 ExaFLOP）的有效 FP8 模型 FLOP。注意，硬件糟糕的可靠性会显著拉低 MFU。

## **供电挑战**

一个 100k H100 集群所需的关键 IT 电力约为 ~150MW。虽然 GPU 本身只有 700W，但在每台 H100 服务器内，CPU、网络接口卡（NIC）、电源单元（PSU）等每 GPU 还要再占约 ~575W。除 H100 服务器之外，一个 AI 集群还需要一批存储服务器、网络交换机、CPU 节点、光收发器以及其他许多设备，合计再占约 ~10% 的 IT 电力。直观感受一下 ~150MW 是什么概念：规模最大的国家实验室超算 El Capitan [也只需要 30MW 的关键 IT 电力](https://asc.llnl.gov/exascale/el-capitan)。政府超算在产业界面前相形见绌。

一个重大的供电挑战是：目前没有任何单一数据中心楼宇具备承接约 ~150MW 新部署的容量。当人们谈论 100k GPU 集群时，一般指的是同一园区（campus）而非同一栋楼。电力寻址已紧迫到什么程度？由于别无选择，X.AI 甚至[正在把田纳西州孟菲斯的一座老厂房改造成数据中心](https://www.semianalysis.com/p/datacenter-model)。

这些集群用光收发器互联，而光收发器的成本与传输距离呈阶梯关系。更长距离的「单模」DR 和 FR 收发器可以可靠地传输约 ~500 米到 ~2km 的信号，但价格可能是仅支持约 ~50 米距离的「多模」SR 和 AOC 收发器的 2.5 倍。此外，还存在传输距离超过 2km 的[园区级「相干」800G 收发器](https://www.marvell.com/products/optical-modules.html)，不过价格要高出 10 倍以上。

![](https://substack-post-media.s3.amazonaws.com/public/images/5f7943c7-7aab-4356-b7c9-f78c1ce9b4ff_1292x835.jpeg)

小规模的 H100 集群通常以 400G 把每个 GPU 通过仅一两层交换机、只用多模收发器连到其他所有 GPU。当集群规模变大，就必须增加更多交换层，光模块的开销也随之变得极为高昂。这类集群的网络拓扑会因首选供应商、当前与未来工作负载以及资本开支的不同而大相径庭。

每栋楼通常包含一个或多个 pod 的计算资源，pod 内部用更便宜的铜缆或多模收发器连接。然后再用更长距离的收发器在计算「岛（island）」之间互联。下图展示了 4 个计算岛：岛内带宽高，岛外带宽较低。155MW 在单一地点交付极具挑战，但我们[正在跟踪超过 15 个 Microsoft、Meta、Google、Amazon、Bytedance、X.AI、Oracle 等公司的数据中心建设项目](https://www.semianalysis.com/p/datacenter-model)，它们将拥有足以容纳这么多 AI 服务器和网络设备的空间。

![](https://substack-post-media.s3.amazonaws.com/public/images/a27fcbdb-9a97-4276-acf6-dc6e94f1f3cb_2908x1334.png)
*来源：SemiAnalysis*

不同客户基于多种因素选择不同的网络拓扑，例如数据搬运基础设施、成本、可维护性、电力、当前及未来工作负载等。因此，[有些客户选择基于 Broadcom Tomahawk 5 的交换机](https://www.semianalysis.com/p/nvidias-infiniband-problem-qmx-ai)，[另一些坚持用 InfiniBand](https://www.semianalysis.com/p/nvidias-infiniband-problem-qmx-ai)，还有一些[选择 NVIDIA Spectrum-X](https://www.semianalysis.com/p/nvidias-infiniband-problem-qmx-ai)。我们将在下文解释原因。

## **并行策略回顾**

要理解网络设计、拓扑、可靠性问题和检查点策略，我们先快速回顾万亿参数训练中使用的 3 种并行方式——数据并行（Data Parallelism）、张量并行（Tensor Parallelism）和流水线并行（Pipeline Parallelism）。[我们在此有一份关于并行策略的全面讲解，包含专家并行（Expert Parallelism）。](https://www.semianalysis.com/i/143439831/inference-parallelism-techniques-pipeline-parallelism-tensor-parallelism-expert-parallelism-and-data-parallelism)

数据并行是最简单的并行形式：每个 GPU 持有完整的模型权重副本，每个 GPU（rank）接收不同的数据子集。这种并行方式的通信量最低，因为只需在各个 GPU 之间做梯度求和（all reduce）。遗憾的是，数据并行只有在每个 GPU 都有足够内存存放完整模型权重、激活值和优化器状态时才可行。对于像 GPT-4 这样的 1.8 万亿参数模型，仅模型权重和优化器状态在训练时就可能占用多达 10.8 TB 的内存。

![](https://substack-post-media.s3.amazonaws.com/public/images/67e4e5ab-db0d-4899-9c15-b528082d721f_1776x1686.png)
*来源：ColossalAI*

为了克服这些内存限制，需要使用张量并行。在张量并行中，每一层的工作和模型权重被分布到多个 GPU 上，通常沿隐藏维度（hidden dimension）切分。中间结果通过跨设备的 all-reduction 交换，且在每一层的自注意力、前馈网络和层归一化中要多次进行。这要求极高带宽，尤其需要极低延迟。实际上，域内的每个 GPU 与其他所有 GPU 一起协同完成每一层的工作，就好似大家是一块巨型 GPU。张量并行将每个 GPU 的总内存占用降低为原来的 1/张量并行 rank 数。例如，如今通常通过 NVLink 使用 8 个张量并行 rank，这样每个 GPU 的内存占用就减少到 1/8。

![](https://substack-post-media.s3.amazonaws.com/public/images/9d3e375e-b61a-4e83-809b-da0a49154618_1456x823.webp)
*来源：Accelerating Pytorch Training*

另一种克服单个 GPU 内存不足以容纳模型权重和优化器状态这一挑战的技术是流水线并行。在流水线并行中，每个 GPU 只持有层数的一个子集，只做这些层的计算，并把输出传给下一个 GPU。该技术将所需内存降低为原来的 1/流水线并行 rank 数。流水线并行的通信量要求很高，但不如张量并行那么重。

![](https://substack-post-media.s3.amazonaws.com/public/images/ea55868d-fb43-4da0-bef3-691b03437d5d_1563x1053.png)
*来源：ColossalAI*

为了最大化模型 FLOPS 利用率（MFU），公司通常把三种并行方式组合成 3D 并行。然后在 H100 服务器内部的 GPU 之间用张量并行，在同一岛内的节点之间用流水线并行。由于数据并行的通信量最低，而岛间网络较慢，岛与岛之间使用数据并行。

![](https://substack-post-media.s3.amazonaws.com/public/images/3f4644a7-ec37-4f5a-bc9f-de64d0071a46_960x1050.png)
*来源：Optimus-CC*

虽然 FSDP 这类技术在 GPU world size 较小、模型非常大时很常见，但它在这里行不通。它实际上与流水线并行不兼容。

## **网络设计考量**

网络设计必须与并行策略相匹配。如果在一个胖树（fat tree）拓扑中让每个 GPU 都以最大带宽连接到其他所有 GPU，成本将高得离谱，因为需要 4 层交换。光模块的成本也会飙升，因为每多一层网络就需要在中间加光模块。

因此，没有人在大型 GPU 集群上部署完整的胖树架构。取而代之的做法是：构建内部为完整胖树架构的计算岛，岛与岛之间的带宽则较低。实现方式多种多样，但大多数公司选择对最顶层网络做「超订阅（oversubscribe）」。例如可参考 Meta 上一代面向最多 32,000 GPU 的集群架构：共有 8 个岛，岛内为完整胖带宽，最上面再加一层 7:1 超订阅的交换。岛间网络速度是岛内网络的 1/7。

![](https://substack-post-media.s3.amazonaws.com/public/images/82f1ba98-e3d3-4001-9a62-746c2fbe74f2_1920x1080.png)
*来源：Meta*

GPU 部署拥有[多张网络](https://www.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband)：前端网络、后端网络和纵向扩展网络（NVLink）。某些情况下，你会在每张网络上跑不同的并行策略。NVLink 网络可能是唯一能满足张量并行带宽需求的网络。后端网络一般可以轻松承载大多数其他类型的并行，但如果存在超订阅，往往就只能退化为仅跑数据并行。

此外，有些人甚至不在顶层做带宽超订阅的岛。他们干脆[从后端网络改走前端网络](https://www.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband)来做岛间通信。

## **InfiniBand 与前端以太网的混合组网**

有一家大厂在前端以太网上跨多个 InfiniBand 岛进行训练。原因是前端网络的成本低得多，而且可以利用楼宇之间现有的数据中心园区网络以及区域路由。

![](https://substack-post-media.s3.amazonaws.com/public/images/eca81978-a5e8-4871-8d77-2bbc2268292b_2272x960.png)
*来源：SemiAnalysis*

遗憾的是，随着 MoE 等稀疏化技术让模型规模增长快，前端网络需要承载的通信量也在增长。这一权衡必须仔细优化，否则你最终会得到两张成本相同的网络——因为前端网络带宽最终会膨胀到可能与后端网络带宽相当。

值得注意的是，Google 在多 TPU pod 的训练任务中完全只用前端网络。他们被称为 ICI 的「计算网络」最多只能扩展到 8960 颗芯片，需要用昂贵的 800G 光模块和光路交换机（optical circuit switch）连接每个 64 TPU 的水冷机柜。因此，Google 必须把 TPU 前端网络做得比大多数 GPU 前端网络更强大来弥补。

![](https://substack-post-media.s3.amazonaws.com/public/images/717a31e1-5d6b-4647-a16f-2d1fbf220ee2_1744x988.jpeg)
*来源：Google 在 MLSys24 上的报告*

在训练中使用前端网络时，必须执行网络拓扑感知的跨岛全局 all-reduce。首先，每个 pod 或岛会在 pod 内的 InfiniBand 或 ICI 网络中做本地 reduce-scatter，使得每个 GPU/TPU 拥有梯度某一小节的总和。接着，在前端以太网上对每个主机 rank 执行跨 pod all-reduce，最后每个 pod 再执行一次 pod 级别的 all-gather。

前端网络还负责数据加载。随着我们转向多模态图像和视频训练数据，前端网络的需求将呈指数级增长。在这种情况下，前端网络带宽将在加载大型视频文件和执行 all-reduce 之间互相争夺。此外，[掉队者](https://pytorch.org/blog/straggler-mitigation/)问题也会加剧：一旦存储网络流量不规律，就会拖慢你整个 all-reduce，而且无法对其建立可预测的模型。

另一种替代方案是 4 层 InfiniBand 网络、7:1 超订阅、共 4 个 pod，每个 pod 有 24,576 张 H100、pod 内为无阻塞 3 层系统。相比把前端网络当作跨岛通路，这种方案在未来带宽升级方面的灵活性要大得多——从 A 楼某台交换机到 B 楼另一台交换机之间加装光纤收发器，远比为了把集群从 100G 升级到 200G 而对每一个机箱做全套前端网络 NIC 升级容易得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/49f79933-ce8a-4884-805c-56abc9cbbafb_2445x790.png)
*来源：SemiAnalysis*

这样会形成更稳定的网络模式：前端网络可以专注于数据加载和检查点，后端网络可以专注于 GPU 到 GPU 的通信。这也有助于缓解掉队者问题。但遗憾的是，4 层 InfiniBand 网络极其昂贵，因为需要额外大量的交换机和收发器。

# 轨道优化 vs 机柜中置

为了提升可维护性，并增加铜网络（< 3 米）和多模网络（< 50 米）的使用比例，一些客户选择放弃 NVIDIA 推荐的轨道优化（rail optimized）设计，转而采用机柜中置（Middle of Rack）设计。

![](https://substack-post-media.s3.amazonaws.com/public/images/59f8507f-c26f-4567-9254-791aa1ff538a_1371x808.png)
*来源：Nvidia*

轨道优化是一种让每台 H100 服务器连接到 8 台不同的 leaf 交换机（而不是全部连到同一台机柜中置交换机）的技术，这样每个 GPU 与较远 GPU 通信时只需经过 1 跳交换机。这可以提升真实世界中的 all-to-all 集合通信性能。All-to-All 集合通信在混合专家（MoE）的专家并行中被大量使用。

![](https://substack-post-media.s3.amazonaws.com/public/images/d7de6797-6277-4fdc-8a94-19d14895f343_2222x1252.png)
*来源：Crusoe*

轨道优化设计的缺点是：你必须连接到距离各不相同的不同 leaf 交换机，而不是连接到一台紧邻服务器内全部 8 个 GPU 的机柜中置交换机。当交换机可以放在同一机柜时，可以使用无源直连铜缆（DAC）和有源电缆（AEC）；但在交换机不一定在同一机柜的轨道优化设计中，就必须使用光模块。此外，leaf 到 spine 的距离可能超过 50 米，从而被迫使用单模光收发器。

通过采用非轨道优化设计，你可以用廉价的直连铜缆替换连接 GPU 到 leaf 交换机的 98,304 个光收发器，使 GPU 网络中 25-33% 的部分变为铜连接。如下面的机柜图所示，不再需要每条 GPU 到 leaf 交换机的连接都向上走线缆桥架、再横向横跨 9 个机柜连到专门的轨道优化 leaf 交换机机柜，leaf 交换机现在位于机柜中部，使每个 GPU 都能用 DAC 铜缆。

![](https://substack-post-media.s3.amazonaws.com/public/images/343d24d1-f631-41f6-bac1-1e33c7e81b0a_1750x1302.png)
*非轨道优化的机柜中置设计，来源：SemiAnalysis*

DAC 铜缆比光模块更凉、更省电、也便宜得多。由于 DAC 电缆发热更少、功耗更低、可靠性更高，链路抖动（flapping，即网络链路间歇性断开）和故障也更少——而这是所有使用光模块的高速互联的一大顽疾。一台 Quantum-2 IB spine 交换机在使用 DAC 铜缆时功耗为 747 瓦；而使用多模光收发器时，功耗最高增至 1,500 瓦。

![](https://substack-post-media.s3.amazonaws.com/public/images/e9ece0f7-1490-4063-baaf-4d543e854a92_1932x1298.png)
*轨道优化的行尾设计，来源：SemiAnalysis*

此外，轨道优化设计的初次布线对数据中心技术人员来说极其耗时，因为每条链路的两端可能相距最远 50 米且不在同一机柜。相比之下，机柜中置设计中 leaf 交换机与所有连接它的 GPU 位于同一机柜。在机柜中置设计中，你甚至可以在集成工厂就完成计算节点到 leaf 交换机链路的测试，因为这一切都在同一机柜内。

![](https://substack-post-media.s3.amazonaws.com/public/images/4fe509fa-92e7-4d32-8489-6623ac2b939a_633x765.png)
*轨道优化的行尾水冷设计，来源：SemiAnalysis*

# 可靠性与恢复

可靠性是这些巨型集群最重要的运营难题之一，因为当前的前沿训练技术本质上是同步的。最常见的可靠性问题包括 GPU HBM ECC 错误、GPU 驱动卡死、光收发器故障、NIC 过热等。节点不断宕机或抛出错误。

为了让平均故障恢复时间保持在低位并让训练持续进行，数据中心必须在现场保留热备节点和冷备组件。发生故障时，最好的做法不是停下整个训练任务，而是换入一台已开机的热备节点，继续训练。这些服务器的停机时间很多仅仅是电源循环/重启节点，就能解决所出现的问题。

但简单重启并不能解决所有问题，很多情况下需要数据中心技术人员到场进行物理诊断和更换设备。最好的情况下，数据中心技术人员也要花数小时才能修好一台故障 GPU 服务器；而很多情况下，一个故障节点可能要过好几天才能重新加入训练。故障节点和热备节点都是理论上拥有 FLOPS、却没有实际为模型做出贡献的 GPU。

在模型训练过程中，需要频繁地把模型检查点（checkpoint）到 CPU 内存或 NAND SSD，以防 HBM ECC 之类的错误发生。一旦出错，必须从较慢的存储层重新加载模型权重和优化器并重启训练。可以使用[Oobleck](https://arxiv.org/abs/2309.08125) 等容错训练技术，提供用户级、应用驱动的手段来处理 GPU 和网络故障。

遗憾的是，频繁的检查点和容错训练技术会拖累系统整体的 MFU。集群需要不断暂停，把当前权重保存到持久存储或 CPU 内存。而且，从检查点重载时，通常每 100 次迭代才保存一次。这意味着最多会损失 99 步的有效工作量。在 100k 集群上，如果每次迭代耗时 2 秒，第 99 次迭代处的一次故障最多会损失 229 个 GPU 天的工作量。

另一种故障恢复方法是让备节点直接通过后端网络从其他 GPU 做 RDMA 拷贝。由于后端 GPU 网络约为 400Gbps，而每 GPU 有 80GB HBM 内存，拷贝权重大约只需 ~1.6 秒。用这种方法最多只损失 1 步（因为更多的 GPU HBM 中保有最新一份权重），也就是只损失 2.3 个 GPU 天的计算量 + 额外 1.85 个 GPU 天用于从其他 GPU 的 HBM 内存 RDMA 拷贝权重。

大多数领先的 AI 实验室已经实现了这一点，但许多较小的公司为了简单起见，仍然对所有故障都采用从检查点重启这种笨重、缓慢、低效的技术。实现基于内存重构的故障恢复，可以为一次大型训练增加数个百分点的 MFU。

![](https://substack-post-media.s3.amazonaws.com/public/images/0f64ae95-3b5f-4f25-887d-3b75019f6f4f_2048x1152.webp)
*来源：Meta*

最常遇到的问题之一是 InfiniBand/RoCE 链路故障。即使每条 NIC 到 leaf 交换机链路的平均无故障时间长达 5 年，由于收发器数量庞大，一个全新、正常运行的集群从上线到第一次任务故障只需 26.28 分钟。如果没有基于内存重构的故障恢复，在 100,000 GPU 集群上，因光模块故障而花在重启训练上的时间，将超过推进模型本身的时间。

![](https://substack-post-media.s3.amazonaws.com/public/images/85f790a8-0726-4871-b8c5-7d8a6a9052fa_1106x349.png)
*来源：SemiAnalysis*

由于每个 GPU 通过 PCIe 交换机直连一块 ConnectX-7 NIC，网络架构层面没有任何容错，因此故障必须在用户训练代码层面处理，直接增加了代码库的复杂度。这是当前 NVIDIA 和 AMD GPU 网络的一大难题：哪怕只坏一块 NIC，该 GPU 就没有其他路径与其他 GPU 通信。由于当前 LLM 在节点内使用张量并行，只要一块 NIC、一个收发器或一个 GPU 故障，整台服务器即视为宕机。

业界正在进行大量工作，让网络可重构、让节点不再如此脆弱。这项工作至关重要，因为现状意味着只要 1 个 GPU 故障或 1 个光模块故障，整台 GB200 NVL72 就会宕机。一台数百万美元的 72 GPU 机柜宕机，远比一台价值几十万美元的 8 GPU 服务器灾难性得多。

Nvidia 已经注意到这个重大问题，并加入了专用的可靠性、可用性与可维护性（RAS）引擎。我们认为 RAS 引擎会分析温度、ECC 重试恢复次数、时钟频率、电压等芯片级数据，预测芯片何时可能发生故障，并向数据中心技术人员告警。这样他们就可以做预防性维护，例如使用更高转速的风扇策略来维持可靠性，或把服务器下线，留待之后的维护窗口做进一步物理检查。此外，在启动训练任务之前，每颗芯片的 RAS 引擎都会做全面自检，例如用已知结果运行矩阵乘法，以检测静默数据损坏（SDC）。

# Cedar-7

另一项被 Microsoft/OpenAI 等客户采用的成本优化手段，是[每台服务器使用一个 Cedar Fever-7 网络模块，而不是使用 8 张 PCIe 形态的 ConnectX-7 网卡](https://pytorchtoatoms.substack.com/p/nvidia-connectx-7-16tbits-cedar-fever)。使用 Cedar Fever 模块的主要好处之一是只需要 4 个 OSFP 笼口而不是 8 个，这样在计算节点端也可以使用双端口 2x400G 收发器，而不再只是交换机端可用。这将连接 leaf 交换机的收发器数量从每 H100 节点 8 个减少到 4 个。连接 GPU 到 leaf 交换机的计算节点端收发器总量从 98,304 个减少到 49,152 个。

![](https://substack-post-media.s3.amazonaws.com/public/images/fd16dedc-78f0-4ddd-abce-e5f68c59f819_936x522.png)
*来源：Nvidia*

由于 GPU 到 leaf 交换机的链路数量减半，这也有助于改善预计的首次任务故障时间。我们估计每条双端口 2x400G 链路的平均无故障时间为 4 年（单端口 400G 链路为 5 年），这将把预计的首次任务故障时间拉长到 42.05 分钟，远好于不使用 Cedar-7 模块时的 26.28 分钟。

![](https://substack-post-media.s3.amazonaws.com/public/images/93f5d025-1487-4d6b-bc28-6c7751270b07_936x624.png)
*来源：ServeTheHome*

# NVIDIA Spectrum-X

目前有一个 [100k H100 集群正在部署中，将于年底前投入运营，采用的是 NVIDIA Spectrum-X 以太网](https://www.semianalysis.com/p/accelerator-model)。

去年我们介绍了 Spectrum-X 在大型网络中相对 InfiniBand 的诸多优势。即便抛开性能和可靠性优势不谈，Spectrum-X 也拥有巨大的成本优势。Spectrum-X 以太网的特点是：每台 SN5600 交换机有 128 个 400G 端口，而 InfiniBand NDR Quantum-2 交换机只有 64 个 400G 端口。注意，Broadcom 的 Tomahawk 5 交换机 ASIC 同样支持 128 个 400G 端口，这使得当前这一代 InfiniBand 处于很大劣势。

一个全互联的 100k 集群可以做成 3 层而不是 4 层。4 层相比 3 层意味着所需收发器多出 1.33 倍。由于 Quantum-2 交换机端口数（radix）较低，100k 集群上全互联 GPU 的最大数量被限制在 65,536 张 H100。[下一代名为 Quantum-X800 的 InfiniBand 交换机通过 144 个 800G 端口解决了这个问题——不过从「144」这个数字就能看出，它是为配合 NVL72 和 NVL36 系统设计的，预计不会在 B200 或 B100 集群中大量使用。](https://www.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband)尽管 Spectrum-X 无需 4 层组网带来了成本节约，但不幸的缺点是：你仍然需要从 Nvidia LinkX 产品线购买加价极高的收发器，因为其他厂商的收发器可能无法工作或未经 Nvidia 认证。

Spectrum-X 相对其他厂商的主要优势在于：Spectrum-X 获得 NVIDIA 库（如 NCCL）的一流支持，而且 Jensen 会把你往产能配给队列的前排推，让你成为其新产品线的首批客户；而用 Tomahawk 5 芯片，你需要投入大量自研工程力量，用 NCCL 优化你的网络才能达到最大吞吐量。

![](https://substack-post-media.s3.amazonaws.com/public/images/daf4f025-3f0e-4795-9771-e337c066c33d_2179x998.png)
*来源：SemiAnalysis*

用以太网而非 InfiniBand 做 GPU 网络的一个不幸缺点是：以太网目前不支持 SHARP 网内归约（in-network reduction）。网内归约的原理是让网络交换机来执行每个 GPU 求和的计算。SHARP 的理论网络带宽提升为 2 倍，因为它把每个 GPU 需要执行的发送和写入次数减少了 2 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/5dd30b88-0ba2-4b54-9f9a-8fad97f21195_1946x875.png)
*来源：Nvidia*

Spectrum-X 的另一个缺点是：对于第一代 400G Spectrum-X，Nvidia 用 Bluefield3 而不是 ConnectX-7 作为权宜之计。至于未来几代，我们预计 ConnectX-8 与 800G Spectrum-X 配合会完全没问题。在超大规模云厂商的采购量级下，Bluefield-3 与 ConnectX-7 卡之间的价差约为 $300 ASP，另一个缺点是 Bluefield-3 比 ConnectX-7 多耗电 50 瓦。因此每节点需要额外 400W 电力，拉低了整台训练服务器的「每皮焦耳智能」。与采用完全相同网络架构的 Broadcom Tomahawk 5 部署相比，部署 Spectrum-X 的数据中心在一个 100,000 GPU 的部署中现在需要额外 5MW 电力。

# Broadcom Tomahawk 5

为了避免缴纳高昂的「Nvidia 税」，很多客户正在部署基于 Broadcom Tomahawk 5 的交换机。每台基于 Tomahawk 5 的交换机与 Spectrum-X SN5600 交换机端口数相同，都是 128 个 400G 端口，而且如果你的公司拥有优秀的网络工程师，性能不相上下。此外，你可以从世界上任何供应商那里购买通用收发器和铜缆，随意混搭。

大多数客户直接与 Celestica 等 ODM 合作生产使用 Broadcom 交换机 ASIC 的交换机，并与 Innolight、Eoptolink 等公司合作采购收发器。基于交换机成本和通用收发器成本，Tomahawk 5 比 Nvidia InfiniBand 便宜得多，与 Nvidia Spectrum-X 相比也更便宜。

不幸的缺点是：你需要拥有足够的工程能力来为 Tomahawk 5 修补和优化 NCCL 通信集合操作。开箱即用的 NCCL 通信集合操作只对 Nvidia Spectrum-X 和 Nvidia InfiniBand 做过优化。好消息是：如果你有 40 亿美元建一个 100k 集群，你就有足够的工程能力去修补 NCCL 并编写优化。当然软件很难，而 Nvidia 永远站在最前沿，但我们总体上预计每一家超大规模厂商都会完成这些优化并从 InfiniBand 迁移走。

![](https://substack-post-media.s3.amazonaws.com/public/images/bc8e1b68-1b4f-489f-a55c-93f9f084133d_2179x998.png)
*来源：SemiAnalysis*

接下来我们将讲解 4 种不同 100k GPU 集群网络设计的物料清单、与之相关的交换机和收发器成本，展示不同网络设计的优势，并给出一个为减少光模块而优化的 GPU 集群物理平面布局。
