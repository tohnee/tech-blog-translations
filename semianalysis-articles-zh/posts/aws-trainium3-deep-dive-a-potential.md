---
title: "AWS Trainium3 深度解析 | 潜在挑战者正在逼近"
title_en: "AWS Trainium3 Deep Dive | A Potential Challenger Approaching"
subtitle: "软件与系统的阶跃式改进、“Amazon Basics”版 GB200 NVL36x2、NL72x2/NL32x2 纵向扩展机柜架构、单位 TCO 性能优化、Trainium4"
date: 2025-12-04
source: https://newsletter.semianalysis.com/p/aws-trainium3-deep-dive-a-potential
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball", "Wega Chu", "Myron Xie", "Ivan Chiam", "Clara Ee", "Cheang Kang Wen", "Wei Zhou", "Jeremie Eliahou Ontiveros", "Tanj Bennett"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AWS Trainium3 深度解析 | 潜在挑战者正在逼近

> 原文：[AWS Trainium3 Deep Dive | A Potential Challenger Approaching](https://newsletter.semianalysis.com/p/aws-trainium3-deep-dive-a-potential) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**软件与系统的阶跃式改进、“Amazon Basics”版 GB200 NVL36x2、NL72x2/NL32x2 纵向扩展机柜架构、单位 TCO 性能优化、Trainium4**

# Trainium3：新挑战者来袭！

在我们发布[万字 TPU 深度解析](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the)之后不久，Amazon 在年度 AWS re:Invent 大会上宣布 Trainium3（Trn3）正式全面上市，并发布了 Trainium4（Trn4）。在数据中心自定义芯片方面，Amazon 拥有历史最长、布局最广的积累。虽然他们[曾在 AI 领域落后了相当长一段时间](https://newsletter.semianalysis.com/p/amazons-cloud-crisis-how-aws-will)，但目前正在快速进步、走向具备竞争力。去年，我们[详细分析了 Amazon Trainium2（Trn2）加速器的爬坡](https://newsletter.semianalysis.com/p/amazons-ai-self-sufficiency-trainium2-architecture-networking)，其目标是内部 Bedrock 工作负载以及 Anthropic 的训练/推理需求。

自那以后，借助我们的[数据中心模型](https://semianalysis.com/datacenter-industry-model/)和[加速器模型](https://semianalysis.com/accelerator-model/)，我们详细拆解了那次大规模爬坡，并由此做出[那款爆款研判：AWS 营收将加速增长](https://newsletter.semianalysis.com/p/amazons-ai-resurgence-aws-anthropics-multi-gigawatt-trainium-expansion)。

今天，我们发布关于 Trainium3 这颗阶跃式改进芯片的下一部“技术圣经”，覆盖芯片、微架构、系统与机柜架构、纵向扩展、性能分析工具、软件平台以及数据中心爬坡。这是我们写过的关于一颗加速器及其软硬件最详尽的文章，桌面版带目录，便于读者分段查阅。

## “Amazon Basics”版 GB200，又称 GB200-at-Home

在 Trainium3 上，AWS 依然死死盯住单位总拥有成本性能（perf per TCO）的优化。其硬件北极星指标很简单：以最低 TCO 实现最快上市。AWS 不押注任何单一架构设计，而是最大化运营灵活性。这一点体现在从多方合作开展自定义芯片设计、管理自有供应链，到对多种组件供应商进行多源采购的方方面面。

在系统与网络层面，AWS 走的是一条围绕 perf per TCO 优化的“Amazon Basics”（亚马逊平价自营）路线。诸如选用 12.8T、25.6T 还是 51.2T 带宽的横向扩展交换机，或者选择液冷还是风冷，这类设计决策都只是手段，最终目的是为给定客户和给定数据中心提供最优 TCO。

在纵向扩展网络方面，Trn2 只支持 4x4x4 3D Torus（环面）网格纵向扩展拓扑，而 Trainium3 增加了一种独特的交换式 fabric，某种程度上类似 GB200 NVL36x2 拓扑，但有几个关键差异。之所以增加这种交换式 fabric，是因为对于前沿混合专家（MoE）模型架构而言，交换式纵向扩展拓扑在绝对性能和单位 TCO 性能上都更优。

即便是这种纵向扩展架构中使用的交换机，AWS 也决定**不做单一决定**：在 Trainium3 的生命周期内，他们将先后采用三种不同的纵向扩展交换机方案——先是用 160 通道、20 端口的 PCIe 交换机以最快上市（因为目前高通道数、高端口数的 PCIe 交换机供应有限），随后切换到 320 通道 PCIe 交换机，最终换用更大规模的 UALink，以转向最佳性能。

## **Amazon 的软件北极星**

在软件方面，AWS 的北极星指标是扩展并开放其软件栈、面向大众市场，而不再只是为内部 Bedrock 工作负载（即运行 vLLM v1 私有 fork 的 DeepSeek/Qwen 等）以及 Anthropic 的训练与推理工作负载（运行定制推理引擎和全套定制 NKI 内核）优化 perf per TCO。

事实上，他们正在软件战略上进行一场大规模、多阶段的转向。第一阶段是发布并开源一个新的 PyTorch 原生后端。他们还将开源其内核语言“NKI”（Neuron Kernal Interface）的编译器，以及其内核与通信库 matmul 和 ML ops（类似 NCCL、cuBLAS、cuDNN、Aten Ops）。第二阶段是开源其 XLA 图编译器和 JAX 软件栈。

通过开源大部分软件栈，AWS 将帮助扩大采用面、启动一个开放的开发者生态。我们认为，CUDA 护城河并不是由建造城堡的 Nvidia 工程师构筑的，而是由数百万外部开发者通过为 CUDA 生态做贡献、在城堡周围挖掘出来的。AWS 已经把这一点内化于心，并且正在践行完全相同的策略。

Trainium3 的 Day 0（首日）支持将仅限[逻辑 NeuronCore（LNC）](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-features/logical-neuroncore-config.html#logical-neuroncore-config)= 1 或 LNC = 2。LNC = 1 或 LNC = 2 是 Amazon/Anthropic 那批超高级、精英 L337 内核工程师想要的，但在广泛采用 Trainium 之前，更广大的 ML 研究科学家群体更偏好 LNC=8。遗憾的是，AWS 计划到 2026 年年中才会支持 LNC=8。关于 LNC 是什么、以及为什么不同模式对研究科学家的采用至关重要，我们将在后文详细展开。

Trainium3 的上市为 Jensen 又**开辟了一条战线**——此前他已要在两个战场应对[单位 TCO 性能极强的 Google TPUv7](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the)，以及复兴之中的[AMD MI450X UALoE72](https://newsletter.semianalysis.com/p/amd-2-0-new-sense-of-urgency-mi450x-chance-to-beat-nvidia-nvidias-new-moat)（其 perf per TCO 可能相当强，尤其是考虑到 OpenAI 拿到的“股权返利”——其有权最多持有 AMD 10% 的股份）。

我们仍然认为，只要 Nvidia 继续加快开发节奏、以光速前进，它就将保持[丛林之王](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the)的地位。Jensen 需要**加速（ACCELERATE）**，而且要比过去 4 个月还要快。正如 Intel 在 CPU 上固步自封、而 AMD 和 ARM 等迎头赶上一样，如果 Nvidia 沾沾自喜，其领跑位置会以更快的速度丢失。

今天，我们将讨论两款支持交换式纵向扩展机柜的 Trainium3 机柜 SKU：

> - 风冷 Trainium3 NL32x2 Switched（代号“Teton3 PDS”）
> - 液冷 Trainium3 NL72x2 Switched（代号“Teton3 MAX”）

我们将首先简要回顾 Trn2 架构并讲解 Trainium3 带来的变化。文章前半部分聚焦各 Trainium3 机柜 SKU 的规格、芯片设计、机柜架构、物料清单（BoM）与功耗预算，然后转向纵向扩展与横向扩展网络架构。文章后半部分将重点讨论 Trainium3 微架构，并进一步展开 Amazon 的软件战略。最后，我们将讨论 Amazon 与 Anthropic 的 AI 数据中心，并以总拥有成本（TCO）和单位 TCO 性能分析收束全文。

# Trainium3 服务器类型与规格总览

Trainium2 与 Trainium3 加起来共有四种服务器 SKU，供应链常以代号称呼它们，与 AWS 的官方品牌名并不一致。

读者在梳理各代际与机柜形态组合时，大概会在 AWS 品牌名与 ODM/供应链所用代号之间来回切换、一头雾水。**我们对 AWS 的恳求：负责产品营销与命名的人，快停下这些令人困惑的名字吧。**理想情况下，他们应效仿 Nvidia 和 AMD 的命名法，让产品名的后半部分标明纵向扩展技术和世界规模（world size），比如 GB200 NVL72 中的 NVL72 表示 NVLink、72 GPU 世界规模。

下表中，我们试图用一份不同群体所用命名法的“罗塞塔石碑”对照表，帮读者理清头绪：

![](https://substack-post-media.s3.amazonaws.com/public/images/9f8ed36b-3e66-49f8-92ca-cbc3ffb2a5b3_1265x303.png)
*来源：SemiAnalysis、AWS*

在规格方面，Trainium3 实现了多项显著的代际升级。

OCP MXFP8 吞吐量翻倍，并新增 OCP MXFP4 支持，但性能与 OCP MXFP8 相同。有趣的是，FP16 和 FP32 等更高精度数字格式的性能与 Trn2 持平。这些取舍的含义，我们将在微架构一节中阐述。

![](https://substack-post-media.s3.amazonaws.com/public/images/25d4e590-9255-4431-a235-7ffa428fe65f_1848x1230.png)
*来源：SemiAnalysis、AWS*

Trainium3 的 HBM3E 升级为 12 层堆叠，单片内存容量提升至 144GB。尽管仍保持 4 组 HBM3E 堆叠，AWS 却把内存带宽提升了 70%——引脚速率从 Trn2 低于平均水平的 5.7Gbps 提高到 Trn3 的 9.6Gbps，这是我们迄今见过的最高 HBM3E 引脚速率。事实上，Trn2 所用的 5.7Gbps 引脚速率更接近 HBM3 的水平，但它仍被归类为 HBM3E，因为它使用 24Gb 裸片，在 8 层堆叠中实现每堆叠 24GB。速度不足的原因在于所用内存来自三星（Samsung），其 HBM3E 与海力士（Hynix）或美光（Micron）相比明显逊色。在 Trainium3 所用的 HBM 上，AWS 正转向 Hynix 和美光以实现快得多的速率。[如需查看各加速器分厂商的 HBM 份额，请使用我们的加速器模型。](https://semianalysis.com/accelerator-model/)

Trainium3 每颗芯片的纵向扩展带宽相对 Trn2 翻倍，方法是转向 PCIe Gen 6——每通道（单向）64Gbps，而 PCIe Gen 5 为每通道 32Gbps。Trainium3 使用 144 条激活 PCIe 通道做纵向扩展，在 Gen6 下意味着每颗 Trainium3 支持每芯片 1.2 TB/s（单向）纵向扩展带宽。

横向扩展带宽支持翻倍至最高 400 Gb/s，但已投产的大多数 Trainium3 机柜仍将沿用 Trn2 时代的每 XPU 200Gb/s 横向扩展速率。

至于 Trainium4，Amazon 将使用 8 组 HBM4 堆叠，相比 Trainium3 实现 4 倍内存带宽和 2 倍容量。

# Trainium3 机柜架构

把视角拉回机柜方案层面，AWS 在 re:Invent 上发布了 Trainium3（Gen1）UltraServer 和 Trainium3（Gen2）UltraServer，分别对应 Trainium3 NL32x2 Switched 与 Trainium3 NL72x2 Switched 之名。两者的关键差异在于纵向扩展网络拓扑与机柜架构——本节将讲解两种 SKU 的拓扑与架构差异，并讨论每种架构最适合、最优化的 AI 工作负载。

先过一遍每种服务器类型的物理布局。下表列出了各机柜级 SKU 的关键规格：

![](https://substack-post-media.s3.amazonaws.com/public/images/1de9ca66-4cc6-4b4d-be44-4d1a5de1cf48_1867x1403.png)
*来源：SemiAnalysis、AWS*

Trainium2 只提供前两种机柜 SKU——即 Trn2 NL16 2D Torus 和 Trn2 NL32x2 2D Torus 服务器，而 Trainium3 将提供全部四种机柜 SKU，2026 年交付的 Trainium3 大部分为 Trainium3 NL32x2 Switched SKU。我们预计在其生命周期内，大部分 Trainium3 将以 Trainium3 NL32x2 Switched 和 Trainium3 NL72x2 Switched SKU 部署。

# Trainium3 芯片与封装

Trainium3 的计算从 Trn2 所用的 N5 节点迁移至 N3P 节点。Trainium3 将与 Vera Rubin 以及 MI450X 的有源中介层裸片（AID）一道，成为 N3P 的首批采用者之一。目前 N3P 存在一些漏电相关问题需要修复，可能使时间线推迟。我们[已在加速器模型中详细分析了这一点及其影响](https://semianalysis.com/institutional/amazon-tranium3-delayed-1-quarter-vera-rubin-changes-post-earnings-nvidia/)。

![](https://substack-post-media.s3.amazonaws.com/public/images/e8fd89b2-217a-46fe-ab66-4a099ba3a808_1942x1137.png)
*来源：AWS、SemiAnalysis*

我们将台积电（TSMC）的 N3P 视为 3nm 平台上的“HPC 旋钮”——在不引入新设计规则的前提下，比 N3E 再前进一小步但有意义的一步，以换取更高频率或更低功耗。公开数据显示，N3P 沿用 N3E 的规则与 IP，但在等漏电下速度提升约 5%，或在等频率下功耗降低 5-10%，另外在逻辑/SRAM/模拟混合设计上有效密度提升约 4%。这正是超大规模云厂商为巨型 AI ASIC 所想要的那种渐进式、低阻力收益。

Trainium3 正是适合建在该节点上的那种产品的典型例子。它也说明为什么自定义加速器会吸干 3nm HPC 产能：密集的矩阵引擎、肥厚的 SRAM 切片，以及非常长的片内互连——器件延迟和漏电的每一点微小降低都能让其受益。

在底层，N3P 与其说是单一突破，不如说是大量堆叠的设计-工艺协同优化（DTCO）微调。N3 世代的 FinFlex 库允许设计者在同一模块内混用更宽与更窄的鳍，在驱动强度、面积与漏电之间做细粒度折中。台积电还改进了 N3P 低层金属堆叠中的衬垫与阻挡层工艺，使互连线和过孔电阻相比早期 3nm 版本有所降低。这些变化合在一起，抠回了足够的裕量来支撑长全局路径上的更高时钟频率或更低 Vmin。

挑战在于，N3P 在做到这些的同时，把互连缩放和图形化推向了当前 EUV 设备几乎容许的极限。20 纳米出头的最小金属间距、高深宽比过孔、更紧的光学收缩，都会放大后道金属互连（BEOL）的波动性与 RC。过孔轮廓控制、刻蚀不足、介质损伤等问题会成为一阶时序问题。对台积电而言，这意味着更脆弱的工艺窗口、更复杂的在线监控，以及更重度地依赖 DTCO 反馈回路来让设计规则与产线在大规模下实际能印制的能力保持一致。我们目前观察到 N3P 缺陷密度的改善慢于预期，这迫使芯片设计者要么为良率重新流片，要么排队等待工艺改进。

能解读裸片标识的读者会注意到，上面的封装图其实是 Trn2——我们用的就是这张图，因为其封装布局与 Trainium3 完全一致。该封装由两个 CoWoS-R 组件构成，而不是一整块大中介层。两颗计算裸片通过封装基板彼此互连。

Trainium3 将继续采用台积电的 CoWoS-R——这一平台在保持成本竞争力的同时推进功率与延迟极限。与整块硅中介层不同，Trainium3 沿袭前代 Trainium2，使用带六层铜 RDL 的有机薄膜中介层（RDL 位于聚合物之上），以远低于硅中介层的成本和更好的机械顺应性覆盖光罩尺度的版图。它仍支持裸片与中介层之间几十微米级的精细布线与微凸点间距，这对密集的小芯片（chiplet）fabric 和 HBM 接口至关重要。其下方是一块 20 个增层的高层数 ABF 基板，将供电和 XSR 信号扇出到模块边界处 130 至 150 微米的 C4 凸点，MCM 在此与电路板连接。

CoWoS-R 上超过六层的多个 RDL 层是一种审慎折中，而非硬性上限。纯有机中介层便宜且顺应性好，但当我们要在 32Gbps 或更高速率上集成更多通道时，它们最终还是会被布线“黄金地皮”限制住。集成无源器件（IPD）通过仅在必要处向有机中介层版图中嵌入小型硅无源器件来弥补这一差距。每块 RDL 中介层中的数千个 IPD 实现了亚微米级布线密度、极精细的微凸点间距，并在芯片最嘈杂的部分（如 HBM PHY 环和核心 fabric）下方提供强力去耦。

芯片前端由 Annapurna 设计，PCIe SerDes 从 Synopsys 授权获得。Alchip 负责后端物理设计与封装设计。我们认为 Trainium3 中可能还有一些继承自 Marvell 所设计 Trainium2 的接口 IP，但从内容量上看无关紧要。Marvell 在其他第三方厂商那里也有封装设计业务。

有趣的是，该项目有两次流片：一套光罩由 Alchip 持有（代号“Anita”），另一套由 Annapurna 直接持有（“Mariana”）。Anita 版本中，Alchip 直接向台积电采购芯片组件；Mariana 则由 Annapurna 直接采购。主要出货量将来自 Mariana。虽然 Alchip 在 Mariana 上的设计参与度与 Anita 相当，但其从 Mariana 获得的营收应低于 Anita。Amazon 和 Annapurna 高度聚焦成本，对供应商压价凶狠。与 Broadcom 的 ASIC 生意相比，Trainium 项目留给芯片设计伙伴 Alchip 和 Marvell 的利润池要小得多。论单位 TCO 性能——Annapurna 更强调把 TCO 的分母压下去。

Marvell 成了这里的大输家。虽然 Trainium2 由他们设计，但这一代他们在与 Alchip 的设计竞标（bakeoff）中落败。Marvell 的 Trainium3 方案是基于小芯片的设计，把 I/O 放到了单独的小芯片上，而不是像 Trainium2 以及未来的 Trainium3 那样与计算同在单片裸片上。

Marvell 丢掉这一插槽的原因是 Trainium2 执行不力。开发周期拖得太久。Marvell 在为封装设计 RDL 中介层时也出了问题，最后是 Alchip 介入帮忙才交付了可用的方案。

![](https://substack-post-media.s3.amazonaws.com/public/images/957e9ff1-7521-47ee-ac0e-9e4bae0d7bbe_931x1009.png)
*来源：SemiAnalysis 加速器模型*

# Trainium4 路线图预估

对 Trainium4 而言，[多家设计公司](https://semianalysis.com/accelerator-hbm-model/)将沿着基于不同纵向扩展协议的两条轨道参与。我们最早在[7 个月前的 5 月于加速器模型中详细拆解了 Trainium4 的 UALink / NVLink 分裂路线](https://semianalysis.com/accelerator-hbm-model/)。与 Trainium3 一样，Alchip 领衔两条轨道的后端设计。

> - 第一条轨道将采用 UALink 224G
> - 第二条轨道将使用 Nvidia 的 NVLink 448G BiDi 协议

Nvidia 的 VR NVL144 与 NVLink Fusion 产品（如 Trainium4）之间可能存在显著的时间差。NVLink Fusion 轨道的时间表可能进一步推迟，因为 fusion 小芯片引入了额外的集成与验证要求，而且大部分 Nvidia 混合信号工程师的注意力将集中在 Nvidia VR NVL144 的新品导入上。

虽然搭载 NVLink Fusion 的 Trainium4 可能不会很快到来，但我们认为 AWS 拿到了优惠的商业条款，不太可能按 Nvidia 典型的约 75% 毛利率付费。Nvidia 有强烈的战略动机支持与 Trainium4 的互操作性，因为允许 AWS 使用 NVLink 有助于保住 Nvidia 在系统层面的锁定。因此，Nvidia 可能会给出比其标准毛利率结构下更优惠的定价。

与限定于固定 72 封装 NVLink 域的 VR NVL144 不同，Trainium4 可以通过跨机柜 AEC 扩展 NVLink 纵向扩展，构建大得多的 144+ 一致性域。NVLink 6 采用 400G 双向 SerDes，允许同一线路上同时进行 200G RX 和 200G TX。这种 400G BiDi 信号传输已经把铜推到了实际极限，尽管一些厂商可能会尝试迈出半代、升级到 600G BiDi。

![](https://substack-post-media.s3.amazonaws.com/public/images/b7e869e2-ba64-4c0c-b458-308d358c6daa_1164x934.png)
*来源：Nvidia*

# Trn2/3 NL16 2D Torus 与 NL64 3D Torus

Trainium2 NL16 2D Torus 与 Trainium2 NL64 3D Torus SKU 分别以 Trainium2 Server 和 Trainium2 UltraServer 之名于 2024 年 re:Invent 发布。我们在 Trainium2 深度解析中覆盖过这两种架构。

简要回顾 Trainium2 SKU——两者的关键差异是纵向扩展世界规模。Trainium2 NL16 2D Torus 以半个服务器机柜容纳整个纵向扩展世界规模，该世界规模包含 16 颗 Trainium2，组成 4x4 网格 2D Torus；而 Trainium2 NL32x2 3D Torus 把四个 Trainium2 NL16 2D Torus 半机柜连接在一起——总共占用两个机柜。这四个 Trainium2 NL16 2D Torus 半机柜服务器用 AEC 连接，构成 64 颗 Trainium2 的纵向扩展世界规模，即 4x4x4 3D Torus。

请注意，上图中 Trainium2 NL16 2D Torus 示意图代表一个完整机柜，但在所绘机柜内包含两个纵向扩展世界。

如前所述，Trainium2 仅提供 NL16 2D Torus 和 NL32x2 3D Torus 机柜 SKU，分别采用 2D 和 3D Torus 拓扑，没有交换式拓扑版本。大部分 Trainium2 部署将采用 Trainium2 NL64 3D Torus 形态，因为 Anthropic 的 Project Rainier 贡献了大部分需求，因此生产将跟随其对 NL64 3D Torus 的偏好。原因在于 Anthropic 的推理模型需要更大的纵向扩展拓扑。

# 交换式机柜级架构

当 Nvidia 推出 Oberon 架构（GB200 NVL72）——全互联纵向扩展拓扑、72 颗芯片的纵向扩展世界规模——时，许多 ASIC 和 GPU 厂商纷纷调整未来机柜设计路线图，效仿 Nvidia 的 Oberon 架构。虽然 AMD 是最先宣布类 Oberon 架构（MI400 Helios 机柜）的厂商，但 AWS 将成为 Nvidia 之外第一家真正出货并部署类似全互联交换式纵向扩展架构的公司，即 Trainium3 的 Trainium3 NL32x2 Switched 与 Trainium3 NL72x2 Switched 形态。AMD 的首个机柜级设计 MI450X UALoE72 将比 Trainium3 的机柜级设计晚一年到货，目标是年底。Meta 也会在 AMD 的 MI450X 之前出货其首个交换式架构。为什么交换式纵向扩展架构优于 Torus 架构，我们将在本文“3D Torus 与交换式对比”一节中解释。（译注：即上文“2D/3D Torus 与交换式纵向扩展网络”一节。）

re:Invent 上展示的 Trainium3 UltraServer 对应 Trainium3 NL72x2 Switched 机柜 SKU，但 Trainium3 NL72x2 Switched 只是 Trainium3 全互联交换式机柜的两种形态之一——另一种是 Trainium3 NL32x2 Switched。与 Trainium3 NL72x2 Switched 一样，Trainium3 NL32x2 Switched 也是全互联交换式，但区别在于 Trainium3 NL32x2 Switched 采用风冷，因此纵向扩展世界规模更小、功率密度更低。

## Trainium3 NL32x2 Switched（Teton3 PDS）

### 机柜架构

Trainium3 NL32x2 Switched 的机柜布局与 Trainium NL32x2 3D Torus 非常相似。两者每机柜都有 16 个 JBOG（Just a Bunch of GPUs）托盘和两个主机 CPU 托盘。每个 JBOG 托盘内有两颗 Trainium3 加速器，因此每机柜共 32 颗 Trainium3 芯片。一个完整的 Trainium3 NL32x2 Switched 纵向扩展世界由两台各 32 颗 Trainium3 的机柜组成，总计 64 颗 Trainium3 的世界规模。

Trainium NL32x2 3D Torus 与 Trainium NL32x2 Switched 的关键差异，是后者在机柜中部加入了纵向扩展 NeuronLink 交换机托盘，从而实现全互联交换网络。NeuronLink 交换机托盘放在机柜中部，与 Nvidia 把 NVLink 交换机托盘放在 Oberon 机柜中部的原因相同：最小化加速器与纵向扩展交换机之间最长的 SerDes 传输距离。对 Trainium NL32x2 Switched 而言，CPU 托盘、电源架、电池备份单元（BBU）托盘和机柜顶（ToR）交换机也从固定位于各自 8 个 JBOG 托盘组的顶部，改为位于机柜的顶部和底部，以缩短 16 个 JBOG 托盘与 4 个 NeuronLink 交换机托盘之间的距离。还会有采用 5 个 NeuronLink 交换机托盘的设计，以便不停机热插拔交换机托盘。这与 Nvidia 的 GB200/300 NVL72/VR NVL144 形成对比——后者在更换交换机托盘前，运维方必须先清空整柜负载。Amazon 的哲学始终围绕现场可维护性与可靠性，因为他们深度参与部署与运维。Nvidia 则以牺牲这些关切为代价追逐性能，因为性能才是他们卖的东西。

另一大差异在于 NeuronLink 拓扑及相关连接组件。Trainium NL32x2 Switched 将通过跨机柜 AEC 在两台机柜之间连接——从 A 机柜的某颗芯片直连 B 机柜的另一颗芯片。我们将在后文更详细地讨论纵向扩展网络。

### JBOG/计算托盘

Trainium3 NL32x2 Switched 的 JBOG 托盘将与 Trainium NL32x2 3D Torus 的非常相似。每个 JBOG 有两颗 Trainium3 芯片。Trainium3 NL32x2 Switched 采用基于 PCIe 6.0 的互连——相比使用基于 PCIe 5.0 互连的 Trainium2 NL16 2D Torus 和 Trainium2 NL32x2 3D Torus JBOG 是一次升级。因此，PCB 材料必须从 M8 级覆铜板（CCL）（具体为低 DK2 玻纤布 + HVLP2 铜箔）升级到 M8.5 级 CCL（低 DK2 玻纤布 + HVLP4 铜箔）。

迄今为止所有 Trainium 机柜都采用无线缆化设计理念以提高组装效率，所有信号都经 PCB 走线传输。信号在 PCB 上传输的损耗远高于飞越（flyover）线缆，因此必须在 JBOG 板中部放置 4 颗 PCIe 6.0 x16 重定时器（retimer），对从前部 I/O 端口到两颗 Trainium3 封装之间经 PCB 传输的信号进行再生。

Trainium3 的 NIC 也位于 JBOG 托盘内。对于 AWS 的后端网络 EFAv4，Trainium3 NL32x2 Switched 提供两种 NIC 配置：

> - 方案 1：每个含两颗 Trainium3 芯片的 JBOG 托盘配一个 Nitro-v6（2*200G）400Gbps NIC 模块：每颗 Trainium3 200Gbps EFA 带宽
> - 方案 2：每个含两颗 Trainium3 芯片的 JBOG 托盘配两个 Nitro-v6（2*200G）400Gbps Nitro NIC 模块：每颗 Trainium3 400Gbps EFA 带宽。

绝大多数 Trainium3 服务器将采用方案 1——每两颗 Trainium3 配一个 Nitro-v6 400G NIC，即每颗 Trainium3 芯片 200Gbps 横向扩展带宽。AWS 认为，即便对于当今最大的生产级推理模型，每 GPU 200Gbps 也足以让预填充实例与解码实例之间的 KV 缓存传输相互掩盖。对于训练，AWS 的哲学是：拥有精英程序员的小公司（比如 Anthropic 那样的人才会用流水线并行（PP）来减少网络流量，而不只依赖 FSDP/TP/上下文并行/DP。不过要记住，流水线并行对大规模训练绝对必要，但维护和调试带 PP 的代码库是个苦差事。

![](https://substack-post-media.s3.amazonaws.com/public/images/fb6b778f-929d-4af7-b166-450f2baf3851_1998x635.png)
*来源：Twitter*

对于 AWS 的前端网络 ENA，CPU 托盘内有一个专用 Nitro-v6（2*200）400Gbps NIC 模块。每个 JBOG 托盘与 CPU 托盘之间，通过一根沿服务器前部走线的专用 PCIe 6.0 x16 DAC 线缆（单向 128GByte/s）连接。Trainium2 NL16 2D Torus 以相同方式连接 CPU 托盘与 JBOG 托盘。

Trainium3 NL32x2 Switched 的 CPU 托盘布局将与 Trainium2 NL16 2D Torus 非常相似，具体见[Trainium2 一文](https://newsletter.semianalysis.com/p/amazons-ai-self-sufficiency-trainium2-architecture-networking)的讲解。

Trainium3 NL32x2 Switched 是 Trainium3 支持交换式纵向扩展架构的上市时间优先 SKU。由于是风冷机柜，机柜功率密度保持较低。可以把它理解为与 Trainium3 NL32x2 3D Torus 相同的功率密度画像，主要差别只是增加了纵向扩展交换机托盘。Trainium3 NL32x2 Switched 也是唯一一种可部署于非液冷就绪数据中心的交换式纵向扩展架构 SKU。

风冷的采用，使其相对其他竞争对手的液冷交换式纵向扩展加速器拥有上市时间优势，因为液冷数据中心的就绪度当前是部署的关键瓶颈。当运营者试图把液冷机柜硬塞进风冷数据中心时，必须使用低效的液-空侧挂换热器（Liquid to Air sidecar）。因此，我们预计 2026 年部署的 Trainium3 芯片大多数将采用 Trainium3 NL32x2 Switched SKU 形态。

## Trainium3 NL72x2 Switched（Teton3 Max）

Trainium3 NL32x2 Switched 与 Trainium3 NL72x2 Switched 都采用全互联交换式架构，但 Trainium3 NL72x2 Switched 是与 Nvidia GB200 NVL72 Oberon 架构可比性最高的机柜架构。除了 Oberon 与 Trainium3 NL72x2 Switched 都使用液冷之外，Trainium3 NL72x2 Switched 还像 Nvidia 那样把 CPU 集成进计算托盘——Grace 和 Vera 与 GPU 同在一块计算托盘上。相比之下，Trainium NL32x2 Switched 仍使用分离式 CPU 节点。与 Oberon 一样，Trainium NL72x2 Switched 使用冷板对 Trainium3 加速器和 Graviton 4 CPU 进行液冷。Trainium NL72x2 Switched 与 Oberon 架构的一大差异是使用跨机柜互连，把纵向扩展世界规模扩大到横跨两个机柜。

### 机柜架构

Trainium3 NL72x2 Switched 使用两台机柜实现 144 颗 XPU 的世界规模，每台机柜容纳 18 个计算托盘和 10 个位于中部的 NeuronLink 交换机托盘。每个计算托盘容纳 4 颗 Trainium3 和 1 颗 Graviton4 CPU，两台机柜合计 144 颗 Trainium3 和 36 颗 Graviton 4，构成 Trainium3 NL72x2 Switched 的世界规模。与 Trainium3 NL32x2 Switched 一样，Trainium3 NL72x2 Switched 使用母线排（busbar）供电。背板混合使用 TE 和 Amphenol 两家的连接器，具体拆分比例见我们的[网络模型](https://semianalysis.com/ai-networking-model/)。

### 计算托盘

Trainium3 NL72x2 Switched 更高的计算与功率密度从计算托盘开始——每个计算托盘包含 4 颗 Trainium3 芯片。Trainium3 NL72x2 Switched 的互连也主要基于 PCIe 6.0，因此 PCB 材料与上述 Trainium3 NL32x2 Switched 所用的相同。板上使用了 6 颗 PCIe 6.0 x16 重定时器来增加信号传输距离，连接各 Trainium3 芯片与前部 I/O 端口。请注意，由于其提升制造速度的无线缆设计，这套上市时间导向的设计中内置了几颗廉价重定时器，用于给设计去风险。在首批量产部署成功后，AWS 可以研究优化设计，有可能去掉部分重定时器。

如上所述，Trainium3 NL32x2 Switched 与 Trainium3 NL72x2 Switched 的主要差异在散热：Trainium3 NL72x2 Switched 采用液冷，而 Trainium3 NL32x2 Switched 为风冷。液冷用于给 Trainium3 模块、NeuronLinkv4 x32 通道 PCIe 6.0 交换机以及 Graviton4 CPU 散热。计算托盘中的其余部件——PCIe 6.0 x16 重定时器、Nitro-v6 NIC、PCIe 6.0 x16 AEC 线缆笼、DIMM 以及 2 块 8TB 本地 NVMe 盘——都由风扇风冷。

再看主机 CPU，Graviton4 将是 Trainium3 NL72x2 Switched 上市时唯一的 CPU 选项。在 Trainium3 生命周期内，CPU 之后可以升级到下一代 Graviton。理论上也支持 x86 CPU，因为它们同样可以通过 PCIe 与其他组件互连，但我们认为他们不打算推出 x86 版 Trainium3 NL72x2 Switched SKU，只会提供 x86 版 Trainium NL32x2 Switched SKU。由于 Trainium3 使用 PCIe 6.0 而 Graviton4 使用 PCIe 5.0，CPU 旁边必须放置两颗 PCIe gearbox（速率转换芯片），把 PCIe 6.0 转换为 PCIe 5.0 以实现 CPU 与 GPU 之间的通信。CPU 内存方面，CPU 旁布置了 12 个 DDR5 DIMM 插槽，主流 SKU 将使用 64GB 和 128GB 容量的 DDR5 DIMM 模组。每个计算托盘配备两块 8TB 本地 NVMe 盘用于本地存储。

## Trainium3 NL72x2 Switched 横向扩展网络

Trainium3 NL72x2 Switched 的横向扩展网络配置与 Trainium3 NL32x2 Switched 相同，即每颗 Trainium3 芯片可在 400G 或 200G 横向扩展带宽之间选择：

> - 方案 1：每个含 4 颗 Trainium3 芯片的 JBOG 托盘配两个 Nitro-V6（2*200G）400Gbps NIC 模块：每颗 Trainium3 200Gbps EFA 带宽
> - 方案 2：每个含 4 颗 Trainium3 芯片的 JBOG 托盘配四个 Nitro-V6（2*200G）400Gbps Nitro NIC 模块：每颗 Trainium3 400Gbps EFA 带宽。

与 Trainium3 NL32x2 Switched 一样，Trainium3 NL72x2 的大部分出货将是方案 1：每两颗 Trainium3 配一个 Nitro-v6 400G NIC，即每颗 Trainium3 芯片 200Gbps 横向扩展带宽。

不同之处在于，对 Trainium3 NL72x2 Switched 而言，主机 CPU 现在位于计算托盘上，CPU 专用的 Nitro-V6（2*200）400Gbps NIC 模块也位于该托盘中。而且借助 PCIe 交换机，CPU 也可以使用 Trainium3 专用 NIC 与外界通信。

Trainium3 NL72x2 Switched 是 AWS 对 Nvidia Oberon 机柜架构的回应。Trainium3 NL72x2 Switched 架构的功率密度比前代高得多。由于高功率密度和液冷就绪数据中心的要求，我们预计会有一部分 Trainium3 以 Trainium3 NL72x2 Switched SKU 部署，但大部分出货量仍将流向 Trainium3 NL32x2 Switched。了解了机柜布局和计算托盘布局/拓扑之后，是时候深入让 Trainium3 NL32x2 Switched 与 Trainium3 NL72x2 Switched 脱颖而出的真正秘方——交换式纵向扩展网络拓扑了。

# 纵向扩展网络架构

## 2D/3D Torus 与交换式纵向扩展网络

在描述新交换式纵向扩展网络的精确拓扑之前，先解释 AWS 为什么决定从 2D/3D Torus 转向交换式架构。Trainium2 NL26 2D Torus 与 Trainium2 NL32x2 3D Torus 服务器的 NeuronLinkv3 纵向扩展拓扑分别是 2D 网格 Torus 与 3D 网格 Torus（顾名思义！）。然而，Torus 拓扑对需要 all-to-all 集合通信的前沿混合专家（MoE）模型并不优化。相比之下，稠密模型并不大量使用 all-to-all 集合通信，这意味着交换式 fabric 用在稠密模型上并没有多少性能优势，TCO 却更高。

在 3D Torus 架构下，由于纵向扩展域内芯片间存在超额订阅（oversubscription），当消息尺寸从 16KB 增长到 1MB（即加大 batch size）时，纵向扩展网络会因超额订阅而突然变为带宽受限。相比之下，在 Trainium3 独特的交换式拓扑下，即便第一代 Trainium3 的交换网络不是扁平的单层交换拓扑，也不会发生超额订阅。

就预填充而言，更大规模的 Trainium3 NL72x2 Switched 纵向扩展拓扑带不来多少收益，因为预填充一般是计算受限的，更大的拓扑主要在解码阶段的宽专家并行中有用。对于总参数量 2-3 万亿的前沿 MoE 模型的解码阶段，Trainium3 NL32x2 Switched 的纵向扩展网络绰绰有余；但面对总参数量超过 4 万亿的前沿 MoE 模型时，把模型部署在更大的 Trainium3 NL72x2 Switched 之更大纵向扩展世界规模上会带来可观收益。

Trainium3 NL32x2 Switched 与 Trainium3 NL72x2 Switched 采取的是最终提供全互联纵向扩展交换方案的路线，但 AWS“以最低 TCO 快速上市”的信条使其决定构建一种能够兼容不同时期可用之各代纵向扩展交换机的网络架构。

在深入不同的机柜架构和交换机代际之前，我们先拆解 Trainium3 的 NeuronLinkv4/片间互连（ICI）带宽构成。

Trainium3 的 NeuronLinkv4 服务器内纵向扩展网络通过三种不同的连接介质互连 XPU：经 PCB、过背板、以及跨机柜互连。我们将逐一讲解纵向扩展网络连接，为便于查阅，在本节末尾附有简表。

每颗 Trainium3 在三种介质合计提供 160 条 PCIe 通道的 NeuronLinkv4 连接，其中 144 条激活通道和背板上 16 条冗余通道。对每颗 Trainium3，这 160 条通道的分布如下——

背板：共 80 条通道，其中 64 条激活、16 条冗余；通道经由一个 Strada Whisper 背板连接器接入背板，该连接器每颗 Trainium3 芯片支持 160 个差分对（DP——即 80 个 Tx 与 80 个 Rx DP）。AWS 利用冗余通道来容错背板线缆故障、交换机托盘级故障和端口托盘级故障。他们不把这 16 条额外通道用作额外带宽，有几个关键原因：

> - 对于解码这类时延受限的工作负载，用更多通道没有任何好处。这就好比用更粗的水管并不会影响一滴水从水管一端流到另一端的速度。
> - 训练这类通信密集型工作负载也不会因为启用全部 80 条通道就获得可观性能提升，因为存在掉队者效应（straggler effect）。在任何大型训练任务中，总会有至少几个机柜是在部分通道故障的状态下运行的。哪怕只有一个 Trainium3 机柜存在故障通道，整个训练任务实际上也只能按 80 条通道中的 64 条激活通道来运行，因为其他所有机柜都在等最慢的那个。

PCB：64 条通道经 NeuronLinkv4 PCB 走线连到相邻的 Trainium3 芯片。对 Trainium3 NL32x2 Switched，PCB 连接直连相邻 Trainium3；而对 Trainium3 NL72x2 Switched，PCB 连接经由 8 颗 PCIe 6.0 32 通道交换机（或 4 颗 64 通道交换机、或 2 颗 128 通道交换机）实现。这一设计的妙处在于 AWS 可以在制造时选择单位通道成本最低的方案。PCB 上不需要冗余通道，因为 PCB ICI 故障率远低于背板。

跨机柜：每颗 Trainium3 有 16 条通道经 PCB 走线到 OSFP-XD 线缆笼，再经 PCIe 有源电缆（AEC）通往相邻机柜。

![](https://substack-post-media.s3.amazonaws.com/public/images/e83297a0-fc31-4943-81b9-cb41ce1c1a20_2143x934.png)
*来源：SemiAnalysis*

# NeuronLink PCIe PHY 与 UALink 交换机

AWS 的北极星是以尽可能多元的供应链、以最低总拥有成本实现最快上市。其纵向扩展网络架构的设计方法也不例外。在 Trainium3 生命周期内将实施三代纵向扩展交换机：先是 160 通道 Scorpio X PCIe 6.0，接着是 320 通道 Scorpio-X PCIe 6.0，最终将有升级到更高端口数（radix）的 72+ 端口 UALink 交换机的选项。160 通道 Scorpio-X 交换机可以快速上市，但缺点是它强制采用了一种非理想、非全互联的纵向扩展网络拓扑，同一 Trainium3 NL72x2 Switched 机柜内的两颗 Trainium3 芯片之间最多需要 3 跳。不过换用 320 通道 Scorpio-X 或 UALink 交换机后，这一点会得到改善。

前两代交换机托盘采用多平面纵向扩展交换架构，从技术上讲无法在不多跳的情况下实现机柜内完全全互联通信。Gen1 交换机将相当快地被更高带宽、更高端口数的交换机取代。下表列出了两种机柜 SKU 与三代交换机托盘共六种组合的纵向扩展特性。

![](https://substack-post-media.s3.amazonaws.com/public/images/e5eaebaa-a560-4532-b85e-b9e1e678f3fa_1730x911.png)
*来源：SemiAnalysis*

# 上市时间优先的 Gen1 交换机托盘——Scorpio X PCIe 6.0，160 通道、20 端口

## 配 Gen1 交换机托盘的 Trainium3 NL32x2 Switched

Trainium3 NL32x2 Switched 的 Gen1 交换机托盘将先采用 160 通道 PCIe 交换机构建纵向扩展拓扑。每台机柜有两个交换平面，每个平面 8 颗交换机。由于每颗 PCIe 交换机端口数有限，每颗 Trainium3 只能连到同一平面上的 8 颗 PCIe 交换机，而不是每一颗 PCIe 交换机。结果就是，并非每颗 Trainium3 都能不多于一跳地与其他所有 Trainium3 直接通信。

例如，节点 1 的 Trainium3 A 只需一跳交换就能与其他每个节点的 Trainium3 A 通信。节点 1 的 Trainium3 B 同理，与其他每个节点的 Trainium3 B 也只相距一跳交换。

但请看三种不同交换平面或不同机柜的 Trainium 之间通信的情形。每种情形下，两颗 Trainium3 芯片之间都有多条数据可选路径，下面列出众多可能路径中的一部分：

- 路径 A：从 A 机柜节点 1 的 Trainium3 A 到 A 机柜节点 16 的 Trainium3 A，共 1 跳
- 路径 B：从 A 机柜节点 1 的 Trainium3 A 到 A 机柜节点 2 的 Trainium3 B，共 2 跳
- 路径 C：从 A 机柜节点 1 的 Trainium3 A 到 B 机柜节点 2 的 Trainium3 B，共 3 跳

由于 Trainium3 芯片具备自动转发（auto forwarding）能力，且集合通信的时延取决于 SBUF 到 SBUF 的数据传输，AWS 声称这种多跳旅程在时延上不成问题。我们认为，与 Nvidia GPU 相比这一时延可以忽略——在 GPU 上集合通信必须以 HBM 为起点或终点。但归根结底，还是要靠性能 ML 工程师将模型并行与纵向扩展拓扑协同优化，在考虑到跨机柜连接的带宽不到机柜内背板 10% 的前提下，让通信的跳数最小化。

最直观的做法是在机柜内部署专家并行（EP），然后在经 AEC“配对”起来的两机柜 Trainium3 之间使用张量并行（TP）。另一个直观的并行策略是机柜内用专家并行、机柜对之间用上下文并行。

还有一种可能的并行策略是在两个机柜上全量 EP，但围绕额外跳数做规划。这种策略对极稀疏模型可能效果很好——这类模型无法跨机柜实施 TP，因为 d_model 维度太小。所以——哪怕途经紧邻的 Trainium3 那额外一跳带来的时延，也是值得的。

# 配 Gen1 交换机托盘的 Trainium3 NL72x2 Switched

再看 Trainium3 NL72x2 Switched SKU，其纵向扩展拓扑更复杂一些。每台机柜有 4 个平面、每平面 10 颗 160 通道 PCIe 交换机，交换机托盘上共 40 颗交换机；另外 18 个计算托盘上各有 8 颗 32 通道 PCIe 交换机，即每机柜计算托盘上合计 144 颗较小的 PCIe 交换机。每台机柜共 184 颗纵向扩展交换机，整个 144 颗 Trainium3 的纵向扩展世界共 368 颗。我们把之前的汇总表复制在此，方便跟踪交换机用量：

![trn3 scale up switch roadmap](https://substack-post-media.s3.amazonaws.com/public/images/8d62d5fc-67c5-4a73-8a0b-7068b96f8f0a_2044x1084.png)
*来源：SemiAnalysis*

与交换机托盘上同样采用 160 通道 PCIe 交换机的 Trainium3 NL32x2 Switched 设计一样，这种纵向扩展设计受限于交换机托盘上每颗 PCIe 交换机只有 20 个端口，这意味着每颗交换机只能连到每节点 4 颗 Trainium3 芯片中的 1 颗（这 20 个端口中有 2 个留空或用于管理）。同一交换平面内，每颗 Trainium3 与其他 Trainium3 相距一跳交换。

与每个 JBOG 只有两颗 Trainium3 的 Trainium3 NL32x2 Switched 设计不同，Trainium3 NL72x2 Switched 的同一块计算托盘板上有 4 颗 Trainium3。同一块板上、处于不同交换平面的 Trainium3 芯片之间通过 8 颗 32 通道 Scorpio-P PCIe 交换机通信，这意味着不同交换平面的 Trainium3 芯片之间的芯片间通信需要额外的交换跳数。

当 Trainium3 不在同一交换平面时，交换跳数大于 1。看下面三种不同情形：

- 路径 A：从 A 机柜节点 1 的 Trainium3 A 到 A 机柜节点 2 的 Trainium3 A，共 1 跳
- 路径 B：从 A 机柜节点 1 的 Trainium3 A 到 A 机柜节点 2 的 Trainium3 C，共 3 跳
- 路径 C：从 A 机柜节点 1 的 Trainium3 A 到 B 机柜节点 2 的 Trainium3 C，共 4 跳

## 配 Gen1 备份交换机托盘的 Trainium3 NL72x2 Switched——Broadcom PEX90144

AWS 还为各种情形做了预案。如果 Scorpio X 160 通道 PCIe 交换机供应不上，可以用 144 通道、最多 72 个可用端口的 Broadcom PEX90144 交换机作为备份选项。不过，这个每端口 2 通道、最高 72 端口的更高端口数替代方案，并不意味着纵向扩展交换平面数量的减少。

![](https://substack-post-media.s3.amazonaws.com/public/images/600329ee-025f-4804-a0d7-8f2d8f650d7b_2058x1316.png)
*来源：SemiAnalysis AI 网络模型*

从 Trainium3 引出的 ICI 通道可能不希望被细分为每端口 2 通道，因为串行化时延可能偏高。这意味着对于 144 通道的 PEX90144 纵向扩展交换机备份方案，AWS 每颗交换机将使用 36 端口（每端口 x8 通道）或 18 端口（每端口 x4 通道）。下图展示了 PEX90144 的一种纵向扩展拓扑：每颗 PCIe 交换机 18 个端口、每端口 8 通道。

# Gen2 交换机托盘——Scorpio X PCIe 6.0 320 通道、40 端口

## 配 Gen2 交换机托盘的 Trainium3 NVL32x2 Switched

Trainium3 NL32x2 Switched SKU 同样兼容 320 通道 PCIe 纵向扩展交换机，待其上市后可替换 160 通道 PCIe 交换机。320 通道 PCIe 交换机端口数翻倍后，每台机柜的纵向扩展网络只需 8 颗交换机，于是机柜内每颗 Trainium3 芯片与其他芯片都只相距一跳交换。既然纵向扩展拓扑已经是全互联，PCB 上相邻 Trainium3 芯片之间的直连就成了锦上添花。

在这一设计中，机柜内任意两颗 Trainium3 芯片之间的最大跳距只有 1 跳——相比 Gen1 设计在 Trainium3 NL32x2 Switched SKU 上最坏 2 跳的距离是巨大改进，在 SKU 升级到 Gen2 交换机托盘后将带来时延优势。

## 配 Gen2 交换机托盘的 Trainium3 NL72x2 Switched

对 Trainium3 NL72x2 Switched 而言，从 160 通道 Scorpio X PCIe 交换机升级到 320 通道 Scorpio X PCIe 交换机意味着交换平面数从 4 个减少到 2 个。JBOG 托盘上相邻的 Trainium3 芯片仍需通过 Scorpio P 交换机通信。

# 终极目标——Gen3 交换机托盘——72+ 端口 UALink 交换机

当 UALink 就绪后，72+ 端口 Scorpio X UALink 交换机可以直接在数据中心内原位安装，替换掉每颗 40 端口的 320 通道 Scorpio X 交换机。UALink 交换机比基于 PCIe 的交换机方案时延更低，并将使用 UALink 协议。

## 配 Gen3 交换机托盘（72+ 端口 UALink 交换机）的 Trainium3 NVL32x2 Switched

下图展示了安装 Gen3 UALink 交换机托盘后 Trainium3 NL32x2 Switched SKU 的拓扑。采用 UALink 交换机后，Trainium3 NL32x2 Switched 将继续像 320 通道 Scorpio X PCIe 交换机那样支持全互联连接。具体端口数和每逻辑端口通道数尚未确定，但每机柜的纵向扩展总带宽将保持不变。

## 配 Gen3 交换机托盘（72+ 端口 UALink 交换机）的 Trainium3 NL72x2 Switched

对 Trainium3 NL72x2 Switched 而言，每台机柜的纵向扩展拓扑此时将变为全互联，因为每颗 UALink 交换机都能连到机柜内的每一颗 Trainium3 芯片。经 8 颗 32 通道 Scorpio P 交换机实现的本地计算托盘连接此时变成了富余带宽。

以上加起来就是一大堆 PCIe 交换机——哪怕只看一代！

好在 Amazon 与 Astera Labs 建立了战略合作伙伴关系。读者们无疑会联想到我们在[TPU 文章](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the?_gl=1*1ibvp2i*_ga*MTE0NTY1MDc4OC4xNzU0NjAxODE4*_ga_FKWNM9FBZ3*czE3NjQ2NTU5NTkkbzE4MyRnMCR0MTc2NDY1NTk1OSRqNjAkbDAkaDExMDkyOTg0ODY.)中强调过的 OpenAI/Anthropic/Nvidia 合作模式——而且多亏了那笔直接投资，Amazon 买得越多省得越多！

如果 AWS 达成对 ALAB PCIe 交换机和重定时器的采购量承诺，它将获得与产品采购挂钩的 ALAB 股票认股权证。这些认股权证随着 AWS 达成采购里程碑而归属，由于行权价只有 20.34 美元，任何高于该水平的市场价格都会给 AWS 带来即时价值。这一结构实际上给了 AWS 一种基于股权的采购“返利”。在下图情形中，截至 9 月 25 日已归属的股票认股权证折算成约 23% 的有效折扣。

![](https://substack-post-media.s3.amazonaws.com/public/images/e654daae-5e29-40a2-bc44-ec57444913d7_1768x516.png)
*来源：SemiAnalysis*

## 铜缆用量

各代 Trainium 的铜缆用量各不相同，因为纵向扩展拓扑（交换式 vs 网格）和 NeuronLink 通道数因 SKU 而异。Trainium2 NL16 2D Torus 依赖单一背板和数量相对较少的 AEC 链路，而 Trainium NL32x2 3D Torus 增加了通道数，需要 4 块 NeuronLink 背板和约 6,100 根铜缆来支撑更密集的 3D Torus 拓扑。Trainium3 NL32x2 Switched 保持了相近的背板数量，铜缆约 5,100 根；而 Trainium3 NL72x2 Switched 将纵向扩展域从 Trainium3 NL32x2 的 64 颗芯片进一步扩大到每个服务器组 144 颗，铜缆用量攀升至 11,520 根。

![](https://substack-post-media.s3.amazonaws.com/public/images/f0528af6-e632-46bf-8ca8-0b9c6c38cc91_2797x1140.png)
*来源：SemiAnalysis AI 网络模型、SemiAnalysis BoM 模型*

# Trainium3 机柜功耗预算与物料清单

我们为不同 Trainium 系统中各大类组件整理出了详尽的零部件清单和功耗预算概览。我们 [AI TCO 模型与 AI 硬件物料清单（BoM）模型](https://semianalysis.com/ai-cloud-tco-model/)的订阅用户可查看数量、ASP 和系统总成本等细节数据。

Trainium3 NL72x2 Switched 系统的总功耗自然更高，因为双机柜系统包含 144 颗芯片，而 Trainium3 NL32x2 Switched 系统的双机柜为 64 颗芯片。不过，一旦按每芯片功耗归一化，64 芯片的 Trainium3 NL32x2 Switched SKU 与 144 芯片的 Trainium3 NL72x2 Switched SKU 的每芯片功耗其实非常接近，因为 Trainium3 芯片 TDP 是整体功耗预算的最大决定因素。Trainium3 NL72x2 Switched 的每机柜功率密度自然更高，因为它每机柜装 64 颗芯片，而 Trainium3 NL32x2 Switched 为 32 颗。

# Trainium3 的变现时间战略

带着这套雄心勃勃的机柜架构，AWS 在机柜设计上做出了一系列战略决策，以优化 Trainium3 机柜的变现时间（time to monetization）。我们认为这是 Trainium3 的一大优势，部署 Trainium3 的客户将从中受益。变现时间的优化极大影响头部 AI 实验室的 [Tokenomics（token 经济学）](https://semianalysis.com/tokenomics-model/)ROIC。下面我们讨论 AWS 在 Trainium3 的设计与部署上为优化变现时间所做的创新和战略决策。

在供应链方面，自 2024 年底以来，AWS 借助 Trn2 已让供应链及其产能爬坡超过一年。虽然 2025 年上半年从晶圆出厂到机柜出货之间曾有很长延迟，但我们预计机柜 ODM 和数据中心供应链现在已经准备好承接 Trainium3 的爬坡，CoWoS 到机柜的时间线将大大缩短。我们观察到平均时间线已缩短至一个季度以内，并且还在继续缩短。

除了为爬坡备好供应链，AWS 还在 Trainium 机柜架构设计上做出了许多战略决策。正如我们在前文强调的，Trainium 服务器采用无线缆化理念设计，所有信号都在 JBOG 或节点内部的 PCB 上传输，以优化组装效率。尽管信号经飞越线缆传输的性能更好，但线缆是组装过程中的潜在故障点。GB200 组装的难点之一就是内部布线量太大，因此 Nvidia 实际上正在跟随 Trainium 的脚步，在 Vera Rubin 上采用无线缆计算托盘设计以提高制造效率。这样做的缺点是需要额外的 PCIe 重定时器，但考虑到 AWS 每次购买 PCIe 重定时器都能从 ALAB 拿到有效返利，这是个相对廉价的解决方案，对 AWS 尤其划算——因为变现时间被压缩了。

这种哲学的另一个例子是通往背板的纵向扩展链路的冗余考量。如上所述，每颗 Trainium3 有 80 条 NeuronLinkv4 通道专用于背板，其中 16 条用于冗余。采取这种做法是为了补偿背板的潜在不可靠性。鉴于 Nvidia GB200 的背板可靠性不佳、调试和更换费时，Trainium3 设计的冗余通道将有可能实现在不清空整柜负载的情况下热插拔纵向扩展交换机托盘。

最后，AWS 在硬件上灵活多路线的做法也使其能够在高密度机柜液冷数据中心未就绪、UALink 交换机缺位等约束下照样部署 Trainium3。同时拥有风冷（Trainium NL32x2 Switched）和液冷（Trainium NL72x2 Switched）全互联交换式纵向扩展机柜的妙处在于：即便液冷数据中心尚未就绪，AWS 也可以在其传统的低密度数据中心部署 Trainium NL32x2 Switched。这种灵活性可避免单一设施延误导致收入延误——正如我们最近在 CoreWeave 的 Denton 设施上所见。至于纵向扩展 NeuronSwitch，我们讨论过 AWS 打算如何先用低端口数交换机抢占上市时间。这再一次展现了他们的灵活性与优化变现时间的决心。

变现时间是 Nvidia 应当留意的事，因为其从芯片产出到客户产生收入的变现时间在 GB200 NVL72 上一直在拉长，而到了 Vera Rubin Kyber 机柜还会更长。这给 OEM/ODM 和终端云厂商带来巨大的营运资金压力，推高其 TCO、削弱盈利能力。

# 横向扩展与跨楼宇（Scale Across）网络

## **什么是 Amazon 的 Elastic Fabric Adaptor（EFA）？**

理解 EFA 要先理解 Elastic Network Attach（ENA）。在 AWS——当用户启动一台虚拟机时，也会通过 ENA 配置一定的网络容量。ENA 用于集群内实例之间的通信，也用于连接其他资源——如 S3、EFS 等存储服务，或负载均衡器等网络服务。ENA 还可以通过 Nitro 系统用于 EBS，并提供上行/WAN 连接和互联网连接。

ENA 为上述服务提供了足够容量，但正如我们所知，AI 服务器需要网络以无阻塞拓扑提供远超于此的容量。这正是 EFA 登场的地方。它是后端网络或“东西向”网络，而 ENA 是前端网络或“南北向”网络。

EFA 是一种网络接口，使用其自有的可扩展可靠数据报（SRD）自定义传输层来降低时延，同时提供拥塞控制和负载均衡。这些特性对 AI 至关重要，因为没有它们集合通信无法扩展。

EFA 并非以太网的直接替代品，因为它在第一层（物理层）和第二层（数据链路层）构建于以太网之上；它是以扩展以太网的 RoCEv2 的替代方案。AWS 声称 EFA 在许多方面超越了 RoCEv2 和 InfiniBand，因为它在更高层还包含许多特性。

AWS 声称 EFA 具有以下优势：

- **安全性**：在安全特性方面，EFA 构建在 Amazon 的 VPC 控制平面之上，这意味着它继承了其核心云安全属性。例如，Nitro 强制实施每实例隔离，用户空间不会让一个租户访问另一个租户的内存。EFA 还使用线速加密（AES-256）——即流量端到端全程加密。
- **可扩展性**：SRD 发送端具备多路径和拥塞感知能力，通过把内存报文喷洒到网络中的多条路径上、同时避开拥塞热点来实现。AWS 声称，处理拥塞并利用新路径而无瓶颈的能力，使 AWS 能够构建跨区域的大型网络 fabric，而无需大缓冲交换机。这与 Nvidia 的 Spectrum-XGS 及 OpenAI MRC 协议类似——后者同样声称跨区域不需要大缓冲交换机。
- **通用性**：Libfabric 应用编程接口（API）把 NIC 和 SRD 暴露给 MPI 实现层，例如 Nvidia 集合通信库（NCCL）。EFA 通过 Libfabric 变得更通用，因为多款 NIC 正在开发中以接入同一 API 接口，这意味着更多网络正通过 Libfabric 变得与 EFA 兼容。但实际上，由于 Nvidia 占有大量最常用的高层组件，通用性的说法在实践中并不成立。

在 AWS 的 Nvidia GPU 上，我们仍然不信服 EFA 相对 Spectrum-X、InfiniBand 或搭配 Connect-X 的 Arista 交换机能提供任何性能增益，因为用户体验持续糟糕。不过在 Trainium 上体验要好得多，这得益于 AWS 在 Trainium 上掌控整个软件栈的能力。

为支撑 EFA，AWS 自研网络接口卡（NIC）。下表展示了各代 EFA 与具体 EC2 服务器的对应关系：

![](https://substack-post-media.s3.amazonaws.com/public/images/40c76720-c96e-4d1c-b792-fbaf574e5084_1876x394.png)
*来源：AWS*

与我们此前在 Trainium2 文章中假设的前后端网络分离不同，AWS 和 Google 一样，把两类流量汇聚到一张网络上。其做法是把 Trainium 托盘和 CPU 托盘上的 Nitro-v6 NIC 都连到相同的机柜顶（ToR）交换机。

对 Trainium3 上的 EFAv4，有两种横向扩展网络速率可选：每颗 Trainium3 400G（每颗 Trainium3 配一个 400G Nitro-v6），或两颗 Trainium3 共享一个 400G Nitro-v6，即每颗 Trainium3 200G。已投产的大多数机柜将采用每 Trainium3 200G 的选项，这也是我们下文讨论并绘图的版本。无论哪种情形，Nitro-v6 NIC 都会连接到两个 200G OSFP 线缆笼。

在每 Trainium3 200G 的版本中，每个 400G Nitro-v6 NIC 将支持两颗 Trainium3 芯片。AWS 采用双 ToR 设计，一个 Nitro-v6 NIC 分别以两条 200G 链路各连到计算托盘上方两台 ToR 交换机中的一台。Trainium 托盘使用带 gearbox 的 400G Y 型有源铜缆（AEC），把 NIC 侧 56G SerDes 通道转换为 ToR 侧 112G SerDes 通道；而连接两个 CPU 托盘到同一对 ToR 交换机则使用直连 AEC 或 DAC（Direct Active Copper）铜缆。

对 Amazon 来说幸运的是，凭借拿到的 Credo 股票返利，他们在 AEC 上的交易比 PCIe 交换机和重定时器还要划算。Credo 的股票返利结构与 AWS 和 ALAB 的协议相同，但有效返利大得多——因为 AWS 在该协议中拿到的认股权证数量多得多，加之此后 Credo 股价大涨。这意味着 Amazon 拿到的 Credo 认股权证的价值超过了为使权证归属所需的采购支出。Credo 等于倒贴钱让 Amazon 拿走 AEC！

![](https://substack-post-media.s3.amazonaws.com/public/images/c5e5cb05-e5f7-409e-8bdb-699abb684211_2017x712.png)
*来源：SemiAnalysis*

尽管 Nvidia 的 InfiniBand 或 Spectrum 以太网参考网络架构采用轨道优化（rail-optimized）的 clos 拓扑来减少 GPU 之间的交换跳数，AWS 更愿意在可能的情况下用 ToR 交换机充当第一层交换。这通过在芯片与第一层交换之间用铜缆替代光链路，降低了整体网络成本。如果 ToR 的多余上行端口被用于对上层降额订阅（undersubscribe），以实现容错、虚拟轨道或连接其他服务，这还带来了可选择性。AWS 声称这种取舍是值得的。

![](https://substack-post-media.s3.amazonaws.com/public/images/2e62304b-df25-4740-bf10-956437403efe_2158x1381.png)
*来源：SemiAnalysis AI 网络模型*

## Amazon 直奔主题：默认高端口数

大多数新兴 GPU 云（neocloud）和超大规模云厂商的默认网络配置使用每逻辑端口 400G 或 800G，与 NIC 带宽对齐。例如，Nvidia 针对 2k GPU H100 集群的参考架构会使用 25.6T 的 QM9700 InfiniBand 交换机，每台 64 个 400G 逻辑端口，与 CX-7 NIC 提供的每 GPU 400G 带宽匹配。交换机数学告诉我们，用 64 端口交换机搭建的两层网络最多只能服务 2,048 块 GPU。

更高端口数（radix）网络——即把链路拆分成更多更小的逻辑端口——日益流行，以扩大网络上可承载的 GPU 数量上限。这表明固守大默认逻辑端口尺寸的做法，会让大量网络优化和成本节约机会白白流失。我们[关于 Microsoft 最大 AI 数据中心的近期文章详细推演了这背后的数学](https://newsletter.semianalysis.com/i/178649945/network)。

在 Microsoft 那篇文章中，我们还讨论了超大规模云厂商如何在最大几家 AI 实验室的要求下，开始部署高端口数网络。下图展示了这样一个例子——OpenAI 在 Oracle 的网络，使用 100G 逻辑端口即可在两层内连接 131,072 块 GPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/aaa68cc4-ecf2-4b89-b266-b29b7bf22384_2358x1257.png)
*来源：SemiAnalysis AI 网络模型*

AWS 的 AI 网络方案早已直奔主题，默认使用 100G 逻辑端口。这有两大好处：

1. AWS 只用 12.8T 交换机就能构建大型网络。

如果我们沿用传统方法、使用与 GPU NIC 对齐的逻辑端口尺寸（很多时候是 400G），就会发现只用 12.8T 交换机建出的网络小得没法用。全部用 12.8T 交换机搭建的两层网络最多只能连接 512 块 GPU。但如果改用 100G 逻辑端口，两层网络可达 8,192 块 GPU，三层网络可达 524,288 块 GPU——与当今最大的多栋建筑集群规模相当。

![](https://substack-post-media.s3.amazonaws.com/public/images/ac2f86d4-0ac7-43dd-9584-9a653e870b2a_2581x588.png)
*来源：SemiAnalysis AI 网络模型*

但为什么要用 12.8T 交换机建网？其实并没有这种执着。AWS 的信条是最小化总拥有成本，并围绕这一北极星灵活调整采购决策。打个比方——对 AWS 来说，猫是黑是白并不重要，[只要能抓到老鼠](https://en.wikipedia.org/wiki/Cat_theory_(Deng_Xiaoping))就是好猫。所以，12.8T、25.6T 还是 51.2T 的交换机，400G DR4、800G DR8 的光模块，AWS 什么都可以用——只要能交付最低的总拥有成本。

2. 如果引入 25.6T 和 51.2T 交换机，AWS 在两层内就能实现更大的规模。

按同样的数学，如果 AWS 引入 25.6T 和 51.2T 交换机，就能实现巨大的规模——如果我们简单假设默认 400G 或 800G 逻辑端口尺寸，这一规模会被大大低估。在下表中可以看到，对两层网络而言，51.2T 交换机上使用 100G 端口尺寸相比 400G 端口尺寸可连接 16 倍的 GPU 数量；对三层网络，这一倍数扩大到 64 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/970735d5-1c73-48a7-8c6d-84efe2872638_2440x1020.png)
*来源：SemiAnalysis AI 网络模型*

使用 100G 端口尺寸的缺点是连接极其复杂——运营者通常必须使用跳线板和配线架，或笨重的[章鱼线缆（octopus cables）](https://www.fs.com/sg/products/68054.html)把这些 100G 链路布到正确的目的地，而且对布线错误的容忍度很低。Amazon 则使用定制化的光配线厂 ViaPhoton 来支撑这种布线，把这一复杂性的影响降到最低。

## **Trainium3 横向扩展网络——高扩展、低阻力**

每个 Trainium pod 内的 ToR 交换机在 leaf 层和 spine 层被划分为多个平面并做轨道优化。所有 Trainium pod——它们是离散的可扩展单元——通过 spine 层互联。在下图中，我们假设了给定每平面 12.8T 带宽交换机、三层网络下的最大集群规模。

![](https://substack-post-media.s3.amazonaws.com/public/images/55ad95e4-4a6c-424d-a36d-d8c9a5c3eecc_2373x1299.png)
*来源：SemiAnalysis AI 网络模型*

把 leaf 和 spine 层的 12.8T 交换机换成 25.6T 交换机，意味着同一三层网络可支撑 4 倍的 Trainium3 芯片，pod 数量翻倍、每 pod 机柜数也翻倍。若 leaf 和 spine 换用 51.2T 交换机，该网络上的芯片数将再翻两番。

![](https://substack-post-media.s3.amazonaws.com/public/images/a6ff8009-6728-4da8-8060-f310ced7c5a1_2386x1330.png)
*来源：SemiAnalysis AI 网络模型*

横向扩展网络可以延伸跨越多栋建筑。FR 光模块可用于几公里距离，ZR 光模块可用于最远几百公里距离。秉承“让 NIC 和 fabric 自己管理更长距离带来的时延”的信条，AWS 将放弃使用深缓冲交换机，直接把不同建筑的 spine 层连接起来。

具体的跨楼宇拓扑尚不清楚——但下图展示了各超大规模云厂商用于跨楼宇扩展的一种拓扑。

![](https://substack-post-media.s3.amazonaws.com/public/images/894ef529-c3a9-46bc-94e7-d0fa427bdd17_1675x1348.png)
*来源：SemiAnalysis AI 网络模型*

最后——谈到横向扩展网络设备采购，很多人对 AWS 给 Trainium 用的是什么网络架构收到了相互矛盾的信号，因为 OpenAI 在 AWS 的集群根本不用 EFA。相反，该集群由 GB300 搭建，使用 CX-8，运行 OpenAI 自定义协议 MultiPath Reliable Connection（MRC）。OpenAI 甚至可能用 OCS（光电路交换机）连接不同集群。这大概在供应链中造成了一些混乱信号——AWS 到底怎么建网？我们希望本节已为想理解其中核心原理的读者澄清了疑惑。

# Trainium3 微架构

Trainium3 采取与 Trainium2 和 Google TPU 类似的路线，用少量大型 NeuronCore 搭建芯片。这与 Nvidia 和 AMD 的 GPU 架构形成对比——后者使用大量小型张量核心。大型核心对 GenAI 工作负载通常更好，因为控制开销更小。与 Trainium2 一样，Trainium3 每封装有 8 个 NeuronCore，每个 NeuronCore 包含以下四个引擎：

> - 张量引擎（Tensor Engine）
> - 向量引擎（Vector Engine）
> - 标量引擎（Scalar Engine）
> - GPSIMD

![](https://substack-post-media.s3.amazonaws.com/public/images/ce74fad9-01a5-40a9-bd6e-35ac3b07e7c3_1000x826.jpeg)
*来源：AWS*

## 张量引擎

**张量引擎**是一个 128x128 BF16 脉动阵列加一个 512x128 MXFP8/MXFP4 脉动阵列。Trainium3 的 BF16 脉动阵列尺寸与 Trn2 的 BF16 阵列相同，但 FP8 阵列尺寸翻倍。

脉动阵列从名为“SBUF”的 SRAM 缓冲区取输入，把结果输出到名为“PSUM”的部分和 SRAM 缓冲区。张量引擎可以在矩阵乘法（matmul）的 K 维度上循环，累加每次结果的部分和以得到完整结果。现代 LLM 工作负载超过 80% 的功耗和 FLOPS 都将投入张量引擎/脉动阵列。张量引擎还支持 MXFP8 4:8 和 4:16 结构化稀疏，可提供 4 倍于稠密计算的 FLOPS，但我们怀疑不会有客户用上。

MXFP4/MXFP8 的 512x128 脉动阵列还可以拆分为 4 个（128x128）脉动阵列，从而每周期向 PSUM 缓冲区压入 4 个结果。对某些 GEMM 形状，有一些优化能让 4x（128x128）脉动阵列比使用 512x128 阵列尺寸指令取得更高的 MFU。

通常，即便是 BF16/MXFP8，GEMM 也完全以 FP32 累加（Nvidia Hopper 上只有 FP22），但有些工作负载能容忍略低的累加精度。Trainium3 张量引擎提供了一个选项：以 FP32 累加 128 个元素，最后再降转为 BF16。

## 张量引擎支持的数字格式与单位功耗性能优化

Trainium3 团队之所以能在相同硅面积和功耗预算内把 MXFP8 性能翻倍，靠的是只聚焦 MXFP8 性能翻倍、保持 BF16 性能不变，辅以其他物理优化——如转向 3nm 工艺、专注高效布局规划、使用定制 cell 库。其他一些提升 MXFP8 单位功耗 FLOPS 的优化包括：采用了相比 Trn2 更新的垂直供电系统。许多关键物理设计工作都在内部完成，而不是把关键 PD 工作外包给供应商。为了把通常以较高精度存储的主权重转换为较低精度的计算权重，Trainium3 在硅片中内置了硬件加速单元，加速 MXFP8/MXFP4 的量化/反量化。

遗憾的是，只聚焦 MXFP8 的代价是 BF16 性能没有提升。像 Anthropic 这样的超高级 L337 用户训练时不需要 BF16，也有能力做 MXFP8 训练，但普通 ML 训练者只会用 BF16 做训练。

此外，Trainium3 的 MXFP4 性能与 MXFP8 相同，而与 AMD/Nvidia 的 GPU 相比，这对推理的优化程度不如后者——GPU 可以用略低的质量换取更快的推理。

不过，对解码这类内存受限的工作负载来说，这一点影响没那么大，因为 Amazon/Anthropic 可以把权重存成自定义块尺寸的 4 位存储格式，同时以 MXFP8 执行计算。这种技术通常称为 W4A8。对内存受限操作，使用 W4A8 可以视为让 HBM 的加载与存储速率翻倍——因为从 HBM 到芯片的传输将以 4 位而非 8 位进行，在送入张量引擎之前才在片上反量化。

另外，Trainium3 不支持 NVFP4（块尺寸 16，块缩放格式 E4M3），只有 OCP MXFP4（块尺寸 32，块缩放格式 E8M0）的硬件支持。这意味着与 Nvidia GPU 上所需的相比，Trainium3 [需要更先进的 QAT/PTQ 技术](https://dropbox.github.io/fp4_blogpost/)。E8M0 块缩放之所以比 E4M3 块缩放差，是因为 E8M0 会把缩放因子对齐到最近的 2^n，这会带来更严重的量化误差。尽管 Trainium3 在技术上确实支持 NVFP4 作为存储格式（或任何 4 位任意存储格式），也支持在线反量化到 OCP MXFP8，但它没有原生硬件加速的 NVFP4 到 OCP MXFP8 反量化支持，必须通过软件驱动的方式实现。

![](https://substack-post-media.s3.amazonaws.com/public/images/29447ee0-8203-4972-b67a-13dbb550844b_9364x4073.png)
*来源：Nvidia*

Trainium3 不支持 NVFP4 使 4 位训练难得多。Nvidia Research（以及 Nvidia 的市场部门）最近发表了他们关于 NVFP4 训练的研究论文，展示了一套在前向和反向传播中使用 4 位的实验性训练配方。我们认为西方前沿实验室在今后 12 个月内不会在前向和反向传播中都采用 4 位浮点训练，但我们确实认为，等配方成熟后他们最终可能转向 4 位。

尽管如此，一些西方前沿实验室已经在前向传播中采用了 NVFP4，但反向传播迄今仍停留在更高精度的数字格式上，而且看起来运行良好、质量损失并不明显。其中一些在前向传播中使用 4 位浮点训练的前沿实验室，已经把这些模型部署到了拥有数百万活跃用户的生产环境。

对 AWS Trainium3 的不利之处在于：如果 4 位前向传播训练在最先进用户中继续扩大采用，Trainium3 可能会因为不支持 NVFP4（块尺寸 16，块缩放格式 E8M0）、且 OCP MXFP4（块尺寸 32，块缩放格式 E4M3）算力只与 OCP MXFP8 持平而处于下风。

![](https://substack-post-media.s3.amazonaws.com/public/images/28e3897e-1965-4ca7-9336-8e225af74e39_11723x3534.png)
*来源：Nvidia Research*

## 向量引擎

向量引擎旨在加速向量运算——即每个输出元素依赖于多个输入元素的运算。这类运算的一个例子是注意力层中计算 softmax，或在层归一化/批归一化层中计算移动平均和方差。

![](https://substack-post-media.s3.amazonaws.com/public/images/6adbdda8-0e57-4544-a9f3-7c3bad2b0f1a_867x317.webp)
*来源：AWS*

## 标量引擎

第三个是标量引擎，负责执行 1:1 映射的运算，例如 SeLU、Ex 等逐元素操作。

## GPSIMD 引擎

最后，在 NeuronCore 内部有多个图灵完备的 GpSimd 引擎，可以运行任意 C++ 代码，方便任何 C++ 开发者快速运行自定义运算。

## 加速“注意力运算”：更快的指数函数硬件单元

NeuronCore 调度器可以并行化运算，让所有引擎同时工作。例如在注意力中，当脉动阵列被用来计算 QxK^T 矩阵乘或 AxV 矩阵乘时，向量/标量引擎可以同时计算当前分块的 softmax。除了每个 NeuronCore 中向量引擎 1.25 倍的时钟提速外，Trainium3 的指数函数每周期吞吐量也达到 Trn2 的 4 倍。这极其重要，因为如果指数函数（softmax 中使用）不够快，就会在整个注意力运算中拖累矩阵乘单元。Blackwell 也遇到过这个问题——指数单元运算不够快，促使 Nvidia 在 Blackwell Ultra 上把指数单元性能提升了 2 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/6c72c17b-558a-4874-88b9-39f75aed9558_937x481.png)
*来源：Tri Dao*

讲完 Trainium3 微架构的基本构件之后，来一轮闪电盘点，看看 AWS 架构师在 Trainium3 上实现的新增/改进特性：

## 集合通信专用核心

与 Trainium2 一样，Trainium3 有几十个专用集合通信核心，完全专职负责与其他芯片通信。这是一项出色的创新，因为它实现了计算与通信的重叠，且计算资源与通信资源之间毫无争用。

相比之下，在 Nvidia 和 AMD 的 GPU 上，通信运算与计算运算运行在相同的核心（SM）上。因此终端用户需要仔细平衡运行通信运算的 SM 与运行计算运算的 SM 的比例。在 GPU 上，这通过“NCCL_MIN_CTA”环境标志完成，实践中涉及相当复杂的调优。由于这种复杂性，只有最先进的用户才会去做通信/计算 SM 比例调优。

## 近存计算与自动转发

Trainium3 的集合通信核心可以用一条指令执行“近存计算”（读-加-写），以降低集合通信时延。Trainium3 降低集合通信时延的另一个特性是：与 GPU 不同，集合通信不必以 HBM 为起点或终点。为了进一步降低集合通信时延，Trainium3 可以把每个 NeuronCore 中的 SBUF（软件管理的 SRAM 暂存区）直接传输到同一封装上其他 NeuronCore 的 SRAM，也可以直接传输到纵向扩展域内其他 Trainium3 封装的 SRAM。这一特性对把 busBW 对消息尺寸的曲线向左移特别有用，可实现更高性能的中小消息尺寸。此外，集合通信核心在 SBUF 内部执行加-写操作的能力，对 Transformer 块内部的 residualAdd 也很有用。

Trainium3 集合通信核心的另一个实用特性是自动转发，这得益于整个 144 封装纵向扩展域共享同一 SBUF 内存映射。这意味着程序员无需在紧邻的 Trainium3 芯片上编程内核来手动把消息转发到最终的 Trainium3 目的芯片。由于上市时间导向的拓扑中一颗芯片到另一颗芯片存在多条路径，底层的 neuron 集合通信库必须针对负载均衡和拥塞控制做好优化，尤其是对无法在编译时预计算的动态在线 all-to-all MoE dispatch 与 MoE combine。

## “零成本”转置

转置在 LLM 训练工作负载中很常见。Trainium3 内置硬件加速指令，使转置可以做到近乎“零成本”，让这些运算在后台完成。

## 片上流量服务质量（QoS）

对某些 NoC/HBM/DMA 集合通信核心同时满负荷工作的工作负载，不同流量之间可能相互冲突。Trainium3 引入了一项名为“流量整形（traffic shaping）”的新硬件特性，为不同流量等级提供服务质量（QoS）。例如，编译器或终端用户可以优先处理张量并行和专家并行中使用的、有大量下游依赖的极度时间敏感流量，把它们排在较不紧急的流量（如从 CPU 后台预取数据，或为下一层后台预取权重/优化器状态（FSDP/ZeRO））之前。

该特性在 Day 0 尚不开放用户配置，但很快就会开放，允许内核程序员通过 NKI 提示来整形流量。在小 batch size（即高交互性、每用户每秒 token 数高）的工作负载中，用户看不到该特性的收益，因为 DMA/总线没有被吃满；但对使用中大 batch token 的查询，该特性可以通过消除流量等级间的争用来降低时延、提高吞吐。有意思的是，Graviton 过去几代也一直支持非常类似的“QoS”流量整形特性。

## 无需预重排的动态 MoE 分组 GEMM

对混合专家（MoE）模型，常见做法是对 token 做 permute/重排，使所有去往 0 号专家的 token 在内存中彼此“相邻”，所有去往 1 号专家的 token 也彼此“相邻”。Trainium3 引入了一项名为张量解引用（Tensor Dereferencing）的特性，用户可以动态索引激活矩阵，即便各专家的 token 并不严格彼此“相邻”。本质上，现有 VLIW AI 芯片架构的一个通病是不原生支持动态性，因此需要非常规的变通手段在运行时（而非编译时）确定每个专家 token 被送往何处——而这正是现代前沿 MoE 模型所要求的。

AWS 在 Trainium3 中新增的这一硬件张量解引用动态特性，意味着该架构本身可以原生支持动态 MoE token 路由。

# Trainium3 软件的大幅改进与战略路线修正

## PyTorch 原生后端支持

AWS 正在对软件战略进行一次大规模路线修正，我们相信这对扩大 Trainium3 的普及极其正面。该战略的第一阶段，是聚焦原生支持 PyTorch，而不是再用 PyTorch/XLA 项目把 Trainium“胶带缠绑”到 PyTorch 上。这个新的 PyTorch 后端是为世界上那些非 Anthropic 精英内核工程师的普通用户准备的。过去，用户只能依赖 PyTorch/XLA 的惰性张量图捕获，而没有一等公民的 eager 执行模式可用。此外，PyTorch/XLA 不支持 PyTorch 原生分布式 API（torch.distributed.*），也不支持 PyTorch 原生并行 API（DTensor、FSDP2、DDP 等），而是依赖奇怪的树外 XLA SPMD API（torch_xla.experimental.spmd_fsdp、torch_xla.distributed.spmd 等）。对于想转向 Trainium 的用户来说，这带来了非原生的二流体验——这些用户早已习惯了原生的 PyTorch CUDA。

![](https://substack-post-media.s3.amazonaws.com/public/images/14f1ba63-93bb-43fe-a39b-b84106093f93_1446x1012.png)
*来源：GitHub*

本周，AWS 宣布将发布并开源其原生 PyTorch 后端，通过“PrivateUse1”TorchDispatch 键支持原生 PyTorch Aten 算子 eager 模式。他们还将通过 [torch 编译器自定义后端函数](https://docs.pytorch.org/docs/stable/torch.compiler_custom_backends.html)接入其图编译器栈来支持 torch.compile API。AWS 还将支持全部原生 torch.distributed 与并行 API。eager 模式下还将支持 DTensor、FSDP1、FSDP2 和 SimpleFSDP。不过 Day 0 的 torch.compile 支持将仅限于 SimpleFSDP，因为它是编译器最友好的包。此外，Trainium 的 torch.compile 在 Day 0 不支持捕获数据依赖条件，也不支持 while 循环。这将触发图中断（graph breaks）。

AWS 还声称将在 Day 0 支持 torch 原生 aten 分组 gemm MoE 算子、MoE Dispatch 原生算子（torch.all_to_all_vdev_2d）和 MoE Combine 原生算子（torch.all_to_all_vdev_2d_offset）。连 AMD 都还没支持这些 MoE 通信算子！AWS 还将从 Day 0 起提供 Flex Attention 支持——任何不想只用朴素因果注意力训练模型的 ML 科学家都需要这一特性。

![](https://substack-post-media.s3.amazonaws.com/public/images/60dfe2f7-7d4e-49bd-826b-f4e531e585e3_1472x847.png)
*来源：AWS*

## PyTorch 原生后端的预期 MFU 与性能

在用 Trainium3 跑训练工作负载方面，AWS 声称 Day 0 时其 PyTorch 原生后端和 torch.compile 原生图编译器在 Qwen 稠密变体上已能达到 43% BF16 MFU，在 Qwen MoE 模型上已能达到 BF16 20-30% MFU。而 AWS 声称，采用手写 NKI（Neuron Kernal Interface，AWS 的内核编写语言）内核的训练代码库，Trainium3 在稠密文本模型上可维持约 60% BF16 MFU，在 DeepSeek 670B 这类稀疏 MoE 模型（每 token 仅激活 256 个专家中的 8 个）上可达 40% 以上 BF16 MFU。

请注意，上面宣传的 torch.compile MFU 只是 Day 0 的 MFU，随时间推移很可能继续改善。我们预计 torch.compile 的 MFU 性能将向手写 NKI 内核达到的性能收敛。话虽如此，NKI 内核性能本身也会继续提升，而且显然手写 NKI 内核永远都是性能前沿，尤其是对最新的模型架构。

## NKI 自定义内核与 Helion

想用 NKI 编写自定义内核的终端用户，可以通过 [torch custom ops API](https://docs.pytorch.org/tutorials/advanced/python_custom_ops.html#python-custom-ops-tutorial) 来实现。很高兴看到 AWS 从 Day 0 起支持整个原生 PyTorch API 面，同时还允许通过 custom ops“破窗”直改底层。

除了树内核心的原生 PyTorch API 之外，幕后还在推进把 NKI 内核语言集成为 Helion 的代码生成目标。可以把 Helion 想成一种更高层的语言，可以用高级语言写出性能相当不错的内核。由于其与原生 PyTorch Aten 算子的相似度更高，用户应把 Helion 看作低层 Aten 算子，而不是高层 Triton/NKI 算子。这将让那些不是硬核 1337 性能工程师的终端用户也能编写自定义内核。

![](https://substack-post-media.s3.amazonaws.com/public/images/073dd0c5-ea8a-4b31-870c-a3b98ce92c47_2546x1238.png)
*来源：PyTorch*
![](https://substack-post-media.s3.amazonaws.com/public/images/08c56eea-d1cd-467d-83f7-9e696953609c_1551x867.jpeg)
*来源：PyTorch*

## Trainium 原生 PyTorch 软件栈的推进

新的 Trainium 原生 PyTorch 栈将以树外（out-of-tree）、GitHub 优先的开源代码库起步（即不会放进“pytorch/pytorch”仓库），通过“PrivateUse1”TorchDispatch 键访问。不过 AWS 计划等软件栈成熟并获得 Meta 批准后将其移入树内。尽管纸面上 PyTorch 现由非营利组织 Linux 基金会掌控，但由于 PyTorch 的大多数维护者和贡献者仍在 Meta，哪些芯片能获批移入树内，还是 Meta 说了算。

对 Trainium 来说幸运的是，AWS 在 Meta 的 PyTorch 团队那里已经有很大话语权，因为现有的多数 CPU 和 Nvidia GPU 开源 PyTorch CI 都跑在 AWS 基础设施上。事实上，AWS 把这些云基础设施的大部分免费提供给 Meta PyTorch，积累了大量善意与关系。结果就是，一旦原生 Trainium PyTorch 栈成熟，AWS 说服 Meta 允许其入树（aten/src/Aten/native/neuron）应该毫无困难。

## PyTorch 基金会计算平台质量等级 RFC

我们列席旁听了 PyTorch 技术咨询委员会，最近有一份名为“PyTorch Compute Platform Quality Levels”的提案提交，定义了三个稳定度等级：

> - Stable（稳定）
> - Unstable（不稳定）
> - Engineering（工程级）

一个包要被上游合入 PyTorch 树内、加入 pytorch.org 文档、并在 pytorch.org 的入门页面设置下载链接，必须在这个质量等级记分卡上超过某个分数门槛。我们认为 Trainium 的 PyTorch 原生栈至少能在测试要求上于 2026 年 Q1 前后在树外仓库达到该门槛，但移入树内仓库仍需一些时间。我们估计大约要到 2026 年底才能入树，但目前尚无具体时间表。我们将在即将发布的 State of PyTorch 文章中，连同 PyTorch 生态的其他重大进展一起讨论这份“PyTorch Compute Platform Quality Levels”RFC。

## SemiAnalysis 甘当“CI Karen”

Trainium 的原生 PyTorch 最终将配备开源 CI，以支撑开源的 GitHub 优先路线。在督促 AMD ROCm 补齐[目前缺失的 600 多个单元测试/集成测试/模型精度测试](https://github.com/orgs/pytorch/projects/146/views/1?filterQuery=)这件事上，SemiAnalysis 一直扮演着 PyTorch“CI Karen”（较真监工）的角色。

![](https://substack-post-media.s3.amazonaws.com/public/images/7794bff5-9130-4500-84e6-97365d916319_1825x1098.png)
*来源：SemiAnalysis、PyTorch*

对 Nvidia，SemiAnalysis 也一直是 PyTorch 的“CI Karen”，确保他们为 PyTorch 基金会贡献应有份额的 CI 机器，而不是让 AWS/Meta 独自为 Nvidia GPU CI 买单。[2025 年 6 月，我们说服 Nvidia 向 PyTorch 基金会直接捐赠了 48 块 B200](https://newsletter.semianalysis.com/i/174558644/mix-pytorch-continuous-integration-ci-and-testing)，并说服 Nvidia 开始为 PyTorch 基金会 CI 提供资金支持。SemiAnalysis 很快还将成为 Intel GPGPU 的 PyTorch“CI Karen”，但不会对 Intel Gaudi 软件栈扮演这一角色，因为 Gaudi 已到生命周期尽头。一旦 Trainium PyTorch 原生栈开源，我们 110% 也会当 Trainium 的 PyTorch“CI Karen”。

![](https://substack-post-media.s3.amazonaws.com/public/images/f8efb3c6-1a7d-41b1-8bde-58de6e7207e5_1864x1098.png)
*来源：SemiAnalysis*

## Trainium 对 TorchTitan 与 PyTorch 生态的支持

Day 0 时，Trainium 的 PyTorch 原生栈将支持 TorchTitan。但对其他 PyTorch 生态库——如 Torchcomm、TorchMonarch、TorchForge 以及低精度训练用的 TorchAO——的支持，要等到 2026 年 Q2 前后。

在推理方面，Trainium 将在 Day 0 支持原生 vLLM v1 体验，而不是现在东拼西凑的 Trainium XLA vLLM 体验。我们认为 vLLM Trainium 有望在 2026 年年中实现上游合入，而且会是比 TPU 与 vLLM 的集成干净得多的集成——后者干脆是把 vLLM 的 PyTorch 代码翻译成 JAX。

## Trainium3 软件对 NIVIDA 的 NIXL KV 缓存传输库的支持

AWS 做了一个有趣的选择：标准化采用 Nvidia 的 NIXL KV 传输库，在预填充实例与解码实例之间传输 KV 缓存。他们做此决定，是为了可以在 Trn2/Trainium3/H100/H200/B300 等系统之间（只要在同一 fabric 上）搬运 KV 缓存。

这将允许用户跨不同推理系统混搭预填充实例与解码实例，目标是在满足端到端时延和交互性（每用户每秒 token 数）约束的前提下，优化可用区/数据中心的每秒吞吐（当然以 TCO 归一化）。

例如，可以用 B200 做预填充，再通过 NIXL（走 EFA）把 KV 缓存传给 Trainium3 NL72x2 Switched 做解码。有意思的是，Nvidia 已经[接受了 AWS 提交的、面向 Nvidia GPU EFA 的 PR 并合入上游 NIXL](https://github.com/ai-dynamo/nixl/pull/784)。但[把 Trainium 代码合入 Nvidia 上游 NIXL 仍在推进中——还等着 Nvidia 被说服接受，目前代码仍停在一位 AWS 工程师的 fork 里。](https://github.com/mcuiaws/nixl/commit/26f1ab1e381936091dcb419824890cdeeb3f73bc)

![](https://substack-post-media.s3.amazonaws.com/public/images/2c61af8a-adf7-432d-9118-e1dc3faab5d3_2246x931.png)
*来源：GitHub*

最后总结 Amazon 的开源路线图：在开源推进的第一阶段，AWS 将开源整个 PyTorch 栈以及 NKI 通信、GEMM、注意力和内核库（以及众多其他组件）。在开源推进的第二阶段，AWS 将开源其 XLA 图编译器和 JAX 软件栈。

# 逻辑 NeuronCore（LNC）与 Megacore

Day 0 时，Trn2/3 软件只支持每个逻辑设备映射到 1 或 2 个物理 neuron 核心，也就是说每个 Trainium 封装有 4 个逻辑设备。这意味着暴露给用户和 ML 应用的每个逻辑设备只能拿到 36GB HBM，而不是完整的 144GB。这里面有不少细节和重要的利弊需要拆解，遗憾的是 Day 0 没有让每个逻辑设备映射到整个封装（8 个 NeuronCore）的选项，用户得等到 2026 年年中。我们坚信，把整个封装（8 个 NeuronCore）映射为 1 个逻辑设备，是 Trainium 软件栈获得更广大 ML 研究界采用所必需的。

在 LNC=1 或 LNC=2 下，由于每个 NeuronCore 完全暴露给终端程序员，像 Anthropic 精英性能工程师这样的高级 L337 用户可以完全掌控 HBM 读取，可以直接管理芯片上 8 个 NeuronCore 之间的数据搬运，从而减少不必要的数据移动。精英内核程序员热爱这一特性，并将继续使用。LNC=1 或 LNC=2 的性能永远好于 LNC=8。

![](https://substack-post-media.s3.amazonaws.com/public/images/e59c4d66-8239-460d-8630-668abb1ed4c8_1075x931.png)
*来源：AWS*

另一方面，LNC=1 或 LNC=2 的缺点是：由于每个逻辑设备只能看到 36GB 内存，做小规模消融和实验的研究科学家和“普通”ML 研究者，需要在模型/batch size 小 4 倍的规模上就开始操心并行策略——而如果有 LNC=8 选项，把 1 个逻辑设备暴露为完整 8 个物理 neuron 核心及随之而来的 144GB 内存，就不必如此。

在其他商用芯片架构上，使用 H100 时 ML 研究科学家只需在规模超过 80GB 后才开始操心超出简单数据并行的模型并行策略（即比 Trainium3 Day 0 的 LHC=1 或 LHC=2 支持高 2.2 倍）。GB300 上 288GB 内存的余量更大——是 Trainium3 Day 0 逻辑设备映射的 8 倍。

有人可能会说，任何称职的研究者都能搞定 FSDP——这话不假——但同样属实的是，引入 FSDP 会增加一层间接性，而做小规模实验时，研究者通常希望把间接层的数量降到最少。

在完美的世界里，PyTorch FSDP API 完美无缺、零 bug，但众所周知这只存在于幻想世界，现实中使用 FSDP 通常会引入一些特定的错误。不然你以为为什么 FSDP API 有好几代？FSDP1/FSDP2/SimpleFSDP……

不管怎样，SimpleFSDP/DTensor 正朝着提供干净 FSDP API 的正确方向前进。

![](https://substack-post-media.s3.amazonaws.com/public/images/ebe6f0db-01b9-472d-a749-8eda9db46245_2067x970.png)
*来源：SemiAnalysis*

### **其他架构上的逻辑设备映射**

在 MI250X 上，把封装上的 2 个 chiplet 作为独立逻辑设备展示给 PyTorch 曾经是唯一选项。到了 MI300/MI325/MI355，AMD 意识到这导致糟糕的用户体验，于是改为默认 1 个完整封装映射 1 个逻辑设备，不过仍保留了[把每个 chiplet 暴露为独立逻辑设备的选项](https://rocm.blogs.amd.com/software-tools-optimization/compute-memory-modes/README.html)。与 Anthropic 所用 Trainium3 的 LNC=1 或 LNC=2 选项相比，值得注意的是：实践中，目前大批量使用 MI355X 的用户中没人真的会用 1 个逻辑设备映射 1 个 XCD 的选项。

### **Trainium 走向 LNC=8 的路径**

AWS 之所以尚未实现 LNC=8，是因为构建一个把 1 个逻辑设备映射到 8 个物理核心、同时最小化核心间不必要通信的编译器，是一件耗时的大工程，而且遗憾的是它不在 Anthropic/Bedrock 的优先级清单前列。所以最终结果是 Trainium3 将“先学爬再学走”，带着 LNC=1 或 LNC=2 上市——反正这正是其最大现有客户 Anthropic 在用的——然后再尝试实现 LNC=8。

在这方面 Trainium3 远非异类。事实上，Google TPU 从第 1 代到第 3 代只支持 LNC=1 选项。TPUv3 每封装有 2 个逻辑设备，直到 2022 年初 TPUv4 上市，才有了把每个逻辑设备映射到整个封装的支持。Google TPU 栈中负责这一映射的编译器叫做“MegaCore”。

Google 现已在 TPUv4/v5p/v6e 上支持 MegaCore，带来了更好的用户体验。而在 TPUv7e 上，Google 又回到了只提供“LNC=1”——即尽管每个封装有 2 个物理核心，每个逻辑设备只映射其中 1 个物理核心。虽然这对性能大有好处，我们仍建议 Google 在 TPUv7 上也支持“MegaCore”。

![](https://substack-post-media.s3.amazonaws.com/public/images/e77cb922-f4be-4f82-b7cf-e52b71e80850_1184x931.png)
*来源：First Principles Book*

# Neuron Explorer 性能分析工具

Trainium 软件已经胜过 Nvidia 的领域之一，是 Neuron Explorer 性能分析套件。该套件此前以 Web 应用形式提供（类似 Chrome Trace/Perfetto/Tensorboard），现在还提供了 VSCode 集成。

![](https://substack-post-media.s3.amazonaws.com/public/images/0000ba8a-5d8c-4dfb-a27f-8aefef32e9ee_1615x931.png)
*来源：AWS*

Trainium 的底层性能分析器深受 Anthropic 全体 1337 性能工程师喜爱，Anthropic 的性能负责人公开表示 Trainium 上的性能分析远好于 Nvidia GPU（显然也远好于 AMD GPU）。

![](https://substack-post-media.s3.amazonaws.com/public/images/de27206a-04ec-411a-9156-cecce845090a_2384x957.png)
*来源：X Tristan Hume*

Neuron Explorer 展示的正是性能工程师关心的指标。它有一个高层摘要页，报告平均算术强度和 MFU/HFU，并显示 DMA/HBM 指标。它还显示每个 NeuronCore 全部 4 个引擎的活动百分比。

![](https://substack-post-media.s3.amazonaws.com/public/images/45508dc9-ad67-43e6-a42b-6b74e6e288a0_1436x2098.png)
*来源：AWS*

与 Nsight Compute 一样，Neuron Explorer 可以为用户提供自动化建议——Anthropic/AWS 工程师声称这些建议甚至比 Nvidia 性能分析工具提供的更好。

![](https://substack-post-media.s3.amazonaws.com/public/images/c83786cd-40a1-41a5-b9f4-72bb35d4fd7e_1388x1825.png)
*来源：AWS*

在集合通信方面，Neuron Explorer 提供一个总览，按集合通信操作（即 allreduce、allgather 等）和按消息尺寸分组展示集合通信操作时长的分布。性能工程师可以分析这一分布图，通过优化流量模式、减少争用，来设法压缩时长分布的离散度。

![](https://substack-post-media.s3.amazonaws.com/public/images/fbafeba5-a26d-49f5-ac45-ad2e6415b97b_2177x1720.png)
*来源：AWS*

Neuron Explorer 还包含所有主要单元随时间变化的利用率时间线，工程师可以把性能优化变成[一局 Factorio 游戏](https://en.wikipedia.org/wiki/Factorio)。用户只需点进 NKI 内核源代码，看看如何消除瓶颈，就能定位瓶颈所在。

![](https://substack-post-media.s3.amazonaws.com/public/images/914f0015-580d-4da0-8431-62bb773b7c4b_3206x1720.png)
*来源：AWS*

# Amazon 与 Anthropic 的 AI 数据中心爬坡

几个月前，我们提出了[Amazon 的 AI 复兴](https://newsletter.semianalysis.com/p/amazons-ai-resurgence-aws-anthropics-multi-gigawatt-trainium-expansion)论——该论点在 Q3'25 财报后已被证明准确。通过估算 Project Rainier 每一栋楼的精确开工时间与最终满载容量，我们成功预测了 AWS 的增长加速。当许多同行还在与延期缠斗时，AWS 的执行力令人印象深刻。我们预计这轮建设将继续驱动增长加速。

![](https://substack-post-media.s3.amazonaws.com/public/images/6d9dde71-5446-4610-b960-9c7609763b4d_2534x1416.png)
*来源：SemiAnalysis AI 数据中心行业模型*

然而，这些数据中心甚至仅仅代表多吉瓦级 Project Rainier 建设的第一阶段。对 Trainium3，AWS 有多个同样令人印象深刻的大型园区正在建设中。下面我们展示一个专门用于 Project Rainier 的新大型 AWS 园区示例，它最终将扩展到 1GW。这个新园区位于某都会区附近，将与另一个同样已破土动工的相邻 1GW 场地相连。这些产能是在印第安纳等现有站点扩建之外的增量。我们的数据中心行业模型预测每栋楼精确的季度 MW 数和数据中心投运时间。

![](https://substack-post-media.s3.amazonaws.com/public/images/b6aa17a6-335c-43fc-906b-b9794f7e0e4d_1372x1302.png)
*来源：SemiAnalysis AI 数据中心行业模型*

## 为什么 Amazon 押注风冷正在获得回报

Amazon AI ASIC 路线图的另一个了不起之处，是从芯片到数据中心都相对缺席液冷。这与那些经历全面设计变更的同行形成反差——比如[我们去年报道过的 Meta 激进转向](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical)。

Amazon 的数据中心设计多年来几乎没有变化。我们在下面展示了 2021 年弗吉尼亚一个园区的设计，把该园区与位于印第安纳的旗舰 Project Rainier AI 集群相比，可以看到建筑设计几乎一模一样！

![](https://substack-post-media.s3.amazonaws.com/public/images/94ca572b-c32f-406b-8bf9-5c9ed469b909_2092x884.png)
*来源：SemiAnalysis AI 数据中心行业模型*

虽然有一些细微变化，但散热系统基本保持原样。一年前，我们的[数据中心散热系统](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-2-cooling-systems)深度解析讲解了 AWS 如何主要依赖外部空气为其数据中心散热。

![](https://substack-post-media.s3.amazonaws.com/public/images/2ce68c9e-8aa2-44bf-8526-b453ed86ae2d_2577x1326.png)
*来源：SemiAnalysis AI 数据中心行业模型*

只要简单看一眼 AWS 设施的卫星影像，就会发现既没有流体冷却回路也没有管道系统。换句话说——AWS 数据中心多年来一直为风冷做极致优化，这家云巨头在 GenAI 时代并未改弦更张，也没有偏离其“最低总拥有成本、最快上市”的信条。

![](https://substack-post-media.s3.amazonaws.com/public/images/2c9d7b7b-2fc1-45bf-b8f0-f1d842fb030b_1386x779.jpeg)
*来源：SemiAnalysis AI 数据中心行业模型*

许多人把这解读为 Amazon 落后了、误解了 AI，但我们认为这是一个自觉而明智的决策。

从上市时间的角度看，AWS 通过建造极其标准化且经过验证的设计获益巨大，从而避免了全面重新设计带来的任何延误。对 Project Rainier 的前几个阶段来说，这一切进展顺利，也让 Anthropic 受益。

## 数据中心直接液冷（DLC）与风冷的权衡

可替换性（fungibility）是另一大优势。AWS 可以保持中立，不被任何散热架构套牢，因为它可以把 CPU 和 Trainium3 轻松放进任何数据中心。像 GB200 这样的液冷芯片在采用液-液冷却时更难部署，但可以用侧挂换热器绕开这一难题。TCO 可能是个问题，但“负载可随处部署”的运营灵活性极其宝贵，不容低估。

总拥有成本与运营灵活性确实是个有争议的话题。在我们看来，业界许多玩家**并没有**在建“完全液冷优化”的数据中心。结果是，我们目睹 CapEx/MW 大幅上涨。反直觉的是，风冷优化设施的能效甚至可能更高。许多人认为直接液冷（DLC）会降低 PUE，但现实往往不同。许多设计为空气和液体回路采用同一根中央水管，而不是两条独立回路。中央管道通常在 25-30C 进水（甚至低于 25C）下运行，这意味着冷水系统在盛夏峰值日仍需要冷水机组。需要冷水机组意味着：(1) 相对采用蒸发进风的风冷优化设施（如 AWS 的典型数据中心），资本开支上升；(2) IT MW 下降，因为峰值 PUE 从约 1.2x 升到约 1.5x（按峰值场景日计算）；(3) 运营开支通常更高，因为高进风温度的风冷优化设施全年无冷水机组运行，省去了机械制冷和额外能耗。

我们去年在[散热系统深度解析](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-2-cooling-systems)中详细解释了所有这些概念。部署真正 DLC 优化的数据中心仍是巨大挑战。许多运营者害怕过度优化会失去“可替换性”，于是选择相对传统风冷优化设施推高 Capex 和 Opex 的设计。

# Trainium3 总拥有成本与单位 TCO 性能

接下来，我们将讨论总拥有成本，以及 Trainium3 的单位 TCO 性能与 Nvidia 和 Trn2 相比表现如何。我们 [AI TCO 模型与 AI 硬件物料清单（BoM）模型](https://semianalysis.com/ai-cloud-tco-model/)的订阅用户可查看数量、ASP 和系统总成本等细节数据。
