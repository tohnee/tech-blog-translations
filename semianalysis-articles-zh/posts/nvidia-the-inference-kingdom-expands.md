---
title: "NVIDIA——推理王国的扩张"
title_en: "Nvidia – The Inference Kingdom Expands"
subtitle: "Groq LP30、LPX 机柜、注意力 FFN 分离、Oberon 与 Kyber 更新、NVIDIA 的 CPO 路线图、Vera ETL256、CMX 与 STX"
date: 2026-03-24
source: https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie", "Daniel Nishball", "Gerald Wong", "Kimbo Chen", "Clara Ee", "Wega Chu", "Michael Chen", "Ivan Chiam", "Jordan Nanos"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# NVIDIA——推理王国的扩张

> 原文：[Nvidia – The Inference Kingdom Expands](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

![](https://substack-post-media.s3.amazonaws.com/public/images/f5522a45-77c1-40f8-94c0-395f272b8db1_2709x1815.png)
*来源：NVIDIA*

在 GTC 2026 上，NVIDIA 带来了一场充满突破性发布的活动。NVIDIA 的创新步伐没有显现出任何放缓迹象：今年他们推出了三个全新系统：Groq LPX、Vera ETL256 和 STX。同时发布的还有 NVIDIA Kyber 机柜架构系统的更新；随着 Rubin Ultra NVL576 和 Feynman NVL1152 多机柜系统的揭幕，CPO 首次亮相于纵向扩展（scale-up）网络。关于 Feynman 架构的早期暗示也是一个重要话题。Jensen 在主题演讲中[点名 InferenceX](https://newsletter.semianalysis.com/p/inferencex-v2-nvidia-blackwell-vs) 更是一大亮点。

这是我们的 GTC 2026 回顾，我们将解答 NVIDIA 留下的许多关键问题。具体来说，我们将剖析 LPX 机柜和 LP30 芯片，解释注意力与前馈网络分离（Attention FFN Disaggregation，AFD）如何工作；给出 NVL144、NVL576 和 NVL1152 背后各种机柜架构的更多细节，厘清其中会插入多少光学器件，以及高密度 Vera ETL256 背后的逻辑。下一代 Kyber 机柜有一些重大更新和一些隐藏细节。

## Groq

首先是 Groq LPU。近期 AI 基础设施领域最重大的事件之一，便是 NVIDIA 对 Groq 的「收购」。严格来说，NVIDIA 向 Groq 支付了 $20B，以获得其 IP 授权并雇佣其大部分团队。这在功能上几乎等同于一次收购，只是其交易结构在法律意义上并不构成收购，从而简化或免去了监管审批的需要。考虑到 NVIDIA 的市场份额，如果这笔交易按完整收购来构造并接受反垄断审查，很可能无法通过。另一个好处是避免了旷日持久的交易交割流程。NVIDIA 得以即时获得 Groq 的 IP 和人才。正因如此，交易宣布后不到四个月，NVIDIA 就已经拿出了正在集成进 Vera Rubin 推理栈的系统概念。

现在我们先复习一下 LPU 架构，看看 Groq 的 LPU 如何与 NVIDIA 的 GPU 形成互补。更多细节请[参阅我们最初的 Groq 文章](https://newsletter.semianalysis.com/p/groq-inference-tokenomics-speed-but)。那篇文章的前提判断至今未变：独立的 Groq LPU 系统在大规模提供 token 服务方面并不经济，但它能极快地输出 token，这可以带来很高的市场溢价。这正是 LPU 融入分离式解码系统的前提。

## LPU 芯片

Groq 第一个也是唯一公开发布的 LPU 架构在其 ISCA 2020 论文中有详细阐述。与连接大量通用核心的典型硬件架构不同，Groq 把架构重组为一组组单一用途的单元，再与其他不同用途的组相连，他们把这些组称为「切片（slice）」。功能单元之间是流式寄存器（streaming registers）和供功能单元彼此传递数据的便签式 SRAM（scratchpad SRAM）。Groq 选择单级便签 SRAM 而非多级存储层次，是为了让硬件执行具备确定性。

具体而言，LPU 架构包含用于向量运算的 VXM 切片、用于加载/存储数据的 MEM 切片、用于张量形状操控的 SXM 切片，以及用于执行矩阵乘法的 MXM 切片。在空间布局上，切片水平排布，让数据水平流动；在切片内部，指令纵向泵送穿越各个单元。从概念上讲，LPU 类似一个纵向泵送指令、水平流动数据的脉动阵列（systolic array）。

![](https://substack-post-media.s3.amazonaws.com/public/images/83c55dd8-42b5-4f62-9551-6668222d528b_1204x581.png)
*来源：Groq、SemiAnalysis*

这种数据流与指令流的设计需要细粒度流水线才能实现高性能。由于 LPU 架构让计算具备确定性，编译器可以激进地调度并重叠指令来隐藏延迟。LPU 对高带宽 SRAM 的使用和激进的流水线，是成就 LPU 低延迟的两大主因。

LPU 一代基于老一代的 Global Foundries 14nm 工艺设计，Marvell 负责该芯片的物理设计。2020 年流片时，与同行相比这是一个成熟得多的节点——当时 incumbent 的 AI 芯片平台大多在台积电（TSMC）的 N7 平台上。对于一个专注于验证 Groq 架构、并将其以推理为中心的设计推向市场的早期产品来说，这很合理。14nm 节点成熟、理解相对透彻，适合作为一颗以架构差异化（而非把硅片推进到先进制程）为重的首发芯片。

其卖点之一是，这颗芯片可以完全在美国本土制造和封装，而竞争对手则高度依赖亚洲半导体供应链：逻辑与封装在台湾，HBM 来自韩国。

此后，Groq 的路线图因执行问题而停滞，LPU 2 始终未能出货。这让 Groq LPU 在竞争对手的路线图面前显得愈发过时。相对 7nm 时代的同行，Groq 曾处于明显但尚可管理的制程劣势，如今这一差距已急剧拉大——2026 年，所有领先的加速器平台都在转向 3nm 级制程。

后续的 Groq LPU 2 是为三星（Samsung）Foundry 的 SF4X 节点设计的，具体在三星的奥斯汀（Austin）工厂生产，这让 Groq 得以延续其「美国本土制造」的卖点。三星还将提供后端设计支持。选择三星是受优惠条款/投资的驱动——三星 Foundry 当时正难以物色到先进制程客户，也错失了 AI 逻辑芯片客户。不出意料，三星是 Groq 随后 2024 年 8 月 D 轮融资的关键投资方，最近一次投资则在 2025 年 9 月、NVIDIA「收购」之前。

然而，Groq LPU 2 因设计问题始终未能产品化。芯片上的 C2C SerDes 无法达到宣传的 112G 速率，导致设计无法正常工作，我们很久以前就在[加速器模型](https://semianalysis.com/accelerator-hbm-model/)中详述过这一点。第三代 Groq LPU 才是 NVIDIA 将要产品化的那一颗。

## SRAM 与存储层次

我们曾撰文讨论 SRAM 在存储层次中的角色，这里快速复述：SRAM 非常快（低延迟、高带宽），但代价是密度低、因而成本高。

因此，Groq LPU 这类以 SRAM 为核心的机器能实现极快首 token 时间（time to first token）和单用户每秒 token 数，但牺牲了总吞吐量——其有限的 SRAM 容量很快就会被权重占满，留给 KV 缓存（KVcache）的空间所剩无几，而 KV 缓存会随着批处理用户数的增加而增长。正如我们已证明的，GPU 在吞吐量和成本上胜出。正因如此，NVIDIA 决定把这两种架构结合起来、取双方之长：在对延迟更敏感、内存占用没那么重的解码部分，放到 LPU 这种低延迟、SRAM 充裕的芯片上加速；而对内存渴求的注意力运算，则交给配备大量快速（但没有 SRAM 那么快）内存容量的 GPU 来执行。

![](https://substack-post-media.s3.amazonaws.com/public/images/a939a961-40da-4762-b7d2-1ebb2423e9a2_2188x350.png)
*来源：SemiAnalysis*

这就引出了 Groq 3 LPU，即 LP30——LPU 二代被直接跳过。这颗芯片没有 NVIDIA 的设计参与。影响二代的 SerDes 问题看起来已经修复。在付费墙后，我们将揭晓 SerDes IP 供应商，答案可能出人意料。NVIDIA 还发布了 LP35，这是 LP30 的小幅升级版，仍将采用 SF4 工艺，需要一次新的流片。它会加入 NVFP4 数值格式，但考虑到 NVIDIA 优先考虑上市时间，我们预计不会有其他激进的设计变更。

![](https://substack-post-media.s3.amazonaws.com/public/images/39025ad5-927c-4619-b929-88d5555be853_1590x860.jpeg)
*来源：NVIDIA*

LPU 3 接近光罩极限（reticle size）的裸片布局与 LPU 1 非常相似。500MB 的片上 SRAM 占掉了相当大的面积，而用于矩阵乘法核心的面积非常小——它提供 1.2 PFLOPS 的 FP8 算力，与 NVIDIA GPU 相比只是零头。相比之下，LPU 1 拥有 230MB SRAM 和 750 TFLOPS 的 INT8 算力，性能提升主要来自从 GF16 到 SF4 的制程迁移。由于是单颗单片（monolithic）裸片，不需要先进封装。

依赖 SF4 的好处之一是，它不像[台积电的 N3 那样受限——N3 正在给加速器生产封顶，也是整个行业算力持续受限的关键原因](https://newsletter.semianalysis.com/p/the-great-ai-silicon-shortage)。此外它也不用 [HBM——HBM 同样供应受限](https://newsletter.semianalysis.com/p/memory-mania-how-a-once-in-four-decades)。这让 NVIDIA 可以爬坡 LPU 的生产，而不必牺牲或挤占自己宝贵的台积电产能配给或 HBM 配给，代表着其他人无法企及的真正增量营收与产能。

自 NVIDIA 接管以来，下一代 LP40 将采用台积电 N3P 工艺制造并使用 CoWoS-R 封装，NVIDIA 将贡献更多自有 IP，例如支持 NVLink 协议而非 Groq 的 C2C。这将是第一颗与 Feynman 平台深度协同设计的 LPU。Groq 原本对 LPU 四代的规划同样是找台积电，后端设计合作伙伴为 Alchip。如今 NVIDIA 自己就能完成后端设计，Alchip 的参与已属多余。计划中的技术创新之一是混合键合（hybrid bonded）DRAM，用来扩展片上内存——相比 SRAM 只有轻微的延迟和带宽下降，但相比普通 DRAM 性能高得多。SK hynix 被选定为此 3D 堆叠所用 DRAM 的供应商。所有这些以及更多细节，我们很久以前就在[加速器模型](https://semianalysis.com/accelerator-hbm-model/)中详述过。

![](https://substack-post-media.s3.amazonaws.com/public/images/bf0a9df3-57f3-43b2-a090-67f9dbdee3d9_2218x1215.png)
*来源：NVIDIA、SemiAnalysis 加速器模型*

## GPU 与 LPU 的融合：注意力 FFN 分离（AFD）

![](https://substack-post-media.s3.amazonaws.com/public/images/05b555ed-9d4e-45db-ad03-cbc1cc261b17_3064x1497.jpeg)
*来源：NVIDIA*

了解了 LPU 擅长什么之后，我们就能理解它们如何融入推理部署。NVIDIA 引入 LPU 是为了提升高交互性场景的性能。在这些场景中，LPU 可以发挥其低延迟能力来改善解码阶段的延迟。LPU 改善解码延迟的一种方式，是应用注意力 FFN 分离（AFD）技术，该技术由 [MegaScale-Infer](https://arxiv.org/abs/2504.02263) 和 [Step-3](https://arxiv.org/abs/2507.19427) 提出。

正如我们在 [InferenceX 文章](https://newsletter.semianalysis.com/p/inferencex-v2-nvidia-blackwell-vs)中解释的，LLM 推理包含两个阶段：预填充（prefill）和解码（decode）。预填充处理完整的输入上下文：它是算力密集型的，适合 GPU。另一方面，解码预测新 token，受内存限制。解码对延迟敏感，因为模型要一个一个地预测新 token，而 LPU 的高 SRAM 带宽和低延迟能力可以帮助加速这一迭代过程。

![](https://substack-post-media.s3.amazonaws.com/public/images/97ce6be2-5ef7-4770-85b8-d65ebda7c049_1887x551.jpeg)
*来源：SemiAnalysis*

注意力和 FFN 是模型中运算的子集。在模型的一次前向传播中，注意力的输出馈入 token 路由器（token router），路由器将每个 token 分配给 k 个专家，每个专家就是一个 FFN。注意力和 FFN 的性能特性截然不同。在解码阶段，注意力对 GPU 的利用率几乎不随批大小（batch size）的扩大而改善，因为它受限于 KV 缓存的加载。相比之下，FFN 的 GPU 利用率随批大小扩展的效果要好得多。

过去 6 个多月里，我们一直在与某些硬件供应商和存储公司[通过我们的推理模拟器](https://semianalysis.com/institutional/inference-simulator/)就此展开合作。

![](https://substack-post-media.s3.amazonaws.com/public/images/c0bd1310-e0d9-4158-8959-b52bc3b65fab_577x409.jpeg)
*来源：MegaScale-Infer、SemiAnalysis*

随着最先进的混合专家（MoE）模型变得越来越稀疏，token 需要从更大的专家池中选择专家。结果是每个专家接收的 token 更少，导致利用率下降。这就催生了注意力与 FFN 的分离。如果一颗 GPU 只执行注意力运算，其 HBM 容量就可以全部分配给 KV 缓存，从而增加它能处理的 token 总量，进而提高每个专家平均处理的 token 数。

![](https://substack-post-media.s3.amazonaws.com/public/images/c51c24d7-d5a7-4c99-a243-0baa24afbf08_1474x783.jpeg)
*来源：SemiAnalysis*

对比这两种运算可以看到：注意力是有状态的（stateful），因为 KV 缓存的加载模式是动态的；而 FFN 是无状态的（stateless），其计算只取决于 token 输入。因此，我们将注意力与 FFN 的计算分离。我们把注意力计算映射到 GPU——它们擅长处理动态工作负载；把 FFN 映射到 LPU——因为 LPU 架构天然具备确定性，静态计算工作负载正合其意。

![](https://substack-post-media.s3.amazonaws.com/public/images/65ead35a-ac7d-4416-b5d8-b2484e3e5a45_1217x372.jpeg)
*来源：SemiAnalysis、MegaScale-Infer*

在 AFD 中，从 GPU 到 LPU 的 token 路由可能成为瓶颈，尤其是在严格的延迟约束下。token 路由流程包含两个操作：分发（dispatch）与合并（combine）。在分发步骤，我们用 All-to-All 集合通信将每个 token 路由到其 top-k 专家。专家完成计算后，我们执行合并步骤，用一次反向 All-to-All 集合通信把输出送回源位置，继续下一层的计算。

![](https://substack-post-media.s3.amazonaws.com/public/images/fd5a62c2-81f4-4f64-b101-6a7e9e611fe6_830x1054.jpeg)
*来源：SemiAnalysis*

为了隐藏分发与合并的通信延迟，我们采用乒乓（ping pong）流水线并行。除了像标准流水线并行那样把批次切成微批次并进行计算流水化之外，分发到 LPU 的 token 还会被合并回源 GPU，就这样在 GPU 与 LPU 之间来回打乒乓。

![](https://substack-post-media.s3.amazonaws.com/public/images/15b11e7c-2540-46c1-92a2-ad4fe5b4e561_1400x673.jpeg)
*来源：MegaScale-Infer*
![](https://substack-post-media.s3.amazonaws.com/public/images/efbdfe32-e16d-4a9b-bfd8-725d4b880569_1381x1082.jpeg)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/1204b3bb-7e16-4820-9a71-4171d79a719e_889x778.jpeg)
*来源：SemiAnalysis*

## 投机解码

LPU 改善解码阶段延迟的另一条路，是加速投机解码（speculative decoding）部署——把草稿模型（draft model）或多 token 预测（MTP）层部署到 LPU 上。

对于一个上下文为 N 个 token 的解码步骤，在前向传播中额外加入 k 个 token（对 k 个新 token 做一次热预填充（warm prefill）），当 k << N 时延迟增加微乎其微。利用这一特性，投机解码用一个小型草稿模型或 MTP 层预测 k 个新 token，从而节省时间——因为小模型每步解码的延迟更低。为验证这些草稿 token，主模型只需对 k 个新 token 做一次热预填充，延迟代价大约相当于单个解码步骤。投机解码通常能把每步解码的输出 token 数提升 1.5 到 2 个，具体取决于草稿模型/MTP 的准确率。凭借低延迟能力，LPU 可以进一步放大延迟节省并提升吞吐量。

![](https://substack-post-media.s3.amazonaws.com/public/images/4b9a77e7-dc29-4321-8f63-1c508cebc7e5_1335x671.jpeg)
*来源：SemiAnalysis*

对 LPU 而言，部署草稿模型或 MTP 层与应用 AFD 有很大不同。FFN 是无状态的，而草稿模型和 MTP 层需要动态 KV 缓存加载。每个 FFN 只有几百兆字节，而草稿模型和 MTP 层要占用几十 GB。为支撑这一内存用量，LPU 可以通过 LPX 计算托盘上的每个 Fabric Expansion Logic FPGA 访问最高 256 GB 的 DDR5。

## LPX 机柜系统

来看 LPX 机柜系统，其中有诸多有趣细节。NVIDIA 展示了一个 LPX 机柜，包含 32 个 1U LPU 计算托盘和 2 台 Spectrum-X 交换机。NVIDIA 在 GTC 上展示的这个 32 托盘 1U 版本，非常接近 Groq 被收购前的原始服务器设计。我们相信这一服务器配置并非将在三季度出货的版本，NVIDIA 会做出改动。这里我们将详述我们所知的实际量产版。这些内容此前已在[加速器模型](https://semianalysis.com/accelerator-hbm-model/)中详细披露。

![](https://substack-post-media.s3.amazonaws.com/public/images/105f4b85-95b2-49c0-ad0a-7afa73fddff1_434x860.png)
*来源：SemiAnalysis 加速器模型*

#### LPX 计算托盘

每个 LPX 计算托盘（节点）包含 16 颗 LPU、2 颗 Altera FPGA、1 颗英特尔（Intel）Granite Rapids 主机 CPU 和 1 个 BlueField-4 前端模块。与其他 NVIDIA 系统一样，超大规模云厂商客户可以、也将会使用自选的前端 NIC，而不是为 NVIDIA 的 BlueField 买单。

![](https://substack-post-media.s3.amazonaws.com/public/images/45fbdc52-ed59-45e7-b666-5315c454d94b_1354x1851.png)
*来源：SemiAnalysis 加速器模型*

LPU 模块在 PCB 上采用面对面（belly-to-belly）安装，即 8 个 LP30 模块在 PCB 顶面、另外 8 个 LP30 模块在底面。LPU 引出的所有连接都通过 PCB 走线，考虑到节点内连接采用密集的全互联（all-to-all）mesh，这需要规格极高的 PCB 来支撑布线。面对面安装正是为了缩短「X」和「Y」两个维度上的 PCB 走线长度。

![](https://substack-post-media.s3.amazonaws.com/public/images/57bb1916-27a0-42d5-85c7-0f81c305cb3c_1839x399.png)
*来源：SemiAnalysis 网络模型*

这个系统有个有趣之处：FPGA 扮演着重要角色。NVIDIA 把这些 FPGA 称为「Fabric Expansion Logic（架构扩展逻辑）」，用途多元。首先，它们充当 NIC，把 LPU 的 C2C 协议转换为以太网，接入基于 Spectrum-X 的以太网横向扩展（scale-out）网络。LPU 正是通过这个横向扩展网络连接到解码系统中的 GPU。

其次，LPU 也要经由 FPGA 才能抵达主机 CPU，由 FPGA 把 C2C 转换为 PCIe 连接到 CPU。

第三，FPGA 连接到背板（backplane）与节点内其他 FPGA 通信，我们认为这是为了帮助管理所有 LPU 的控制流与时序。这些 FPGA 还各自带来最高 256GB 的额外系统 DRAM。如果用户希望整个解码过程都由 LPX 承担，这池内存可用于 KV 缓存。

前面板上有 8 个 OSFP 笼座用于跨机柜 C2C，另有 2 个笼座（很可能是 QSFP-DD）连接到 Spectrum 交换机——后者用于在分离式解码系统中连接 LPU 与 GPU。我们会在描述网络时分享更多细节。

## LPU 网络

LPU 网络可分为纵向扩展的「C2C」网络和通过 Spectrum-X 与 NVIDIA GPU 交互的横向扩展网络。先讨论纵向扩展网络，它可分为三部分：节点内、节点间/机柜内、机柜间。对于机柜内的 C2C，NVIDIA 宣布每机柜纵向扩展总带宽为 640TB/s，其计算来源为 256 颗 LPU × 90 条 lane × 112Gbps/8 × 双向 = 645TB/s。注意，NVIDIA 用的是 112G 的线路总速率，而非 100G 的有效数据速率。

#### 托盘内拓扑

![](https://substack-post-media.s3.amazonaws.com/public/images/f5b18381-6c96-4d0f-912e-e7978cc30446_1414x1617.png)
*来源：SemiAnalysis 网络模型*

在每个托盘（节点）内，16 颗 LPU 以全互联 mesh 彼此相连。每个 LPU 模块以 4x100G 的 C2C 带宽连接到节点内其余 15 颗 LPU。注意这里的「C2C」与 NVLink 无关，而是 Groq 自有的纵向扩展网络。这些连接全部通过 PCB 走线，因而需要规格极高的 PCB 来支撑这种布线密度。这正是采用面对面布局的原因：它缩短了所有 LPU 之间「X」「Y」方向的距离，让布线改走「Z」维度。

每颗 LPU 另有 1x100G 连接到一颗 FPGA，每颗 FPGA 对接 8 颗 LPU。2 颗 FPGA 各有 8 条 PCIe Gen 5 连接到 CPU。LPU 必须经由 FPGA 才能与 CPU 对接，因为 LPU 没有可直接对接的 PCIe PHY。

#### 节点间/机柜内

![](https://substack-post-media.s3.amazonaws.com/public/images/25d7c5ea-dce9-4703-9d95-eda3887a2e72_1066x1155.png)
*来源：SemiAnalysis 网络模型*

每颗 LPU 与服务器内其余 15 个节点中的各一颗 LPU 相连。每条节点间链路为 2x100G，因此每颗 LPU 引出 15x2x100G 的节点间链路。这些节点间链路通过铜缆背板实现。此外，每颗 FPGA 还以每链路 25G 或 50G 的速率连接到其他每个节点的 FPGA，即 15x25G/50G，同样经由背板。这意味着每个节点有 16 × 15 × 2 条用于节点间 C2C 的 lane，加上 2 × 15 条用于节点间 FPGA 的 lane，共计 510 条 lane，或 1020 对差分线（Rx 与 Tx）。因此背板为 16 × 1020/2 = 8,160 对差分线——除以 2 是因为每个器件的 Tx 通道对应的是对端器件的 Rx 通道。

#### 机柜间

![](https://substack-post-media.s3.amazonaws.com/public/images/eaf1f2a7-972d-4d67-b1e8-aa596dcca070_3060x4100.png)
*来源：SemiAnalysis 网络模型*

最后是机柜间 C2C。每颗 LPU 有 4 条 100G lane 通向 OSFP 笼座，以连接跨 4 个机柜的 LPU。这种机柜间纵向扩展有多种可用配置。一种方案是每颗 LPU 的 4x100G 汇入一个 OSFP 笼座，每个 OSFP 引出来自 2 颗 LPU 的 800G C2C。不过，为了更大的扇出（fan out），首选配置似乎是 LPU 的每条 100G lane 分别通向 4 个独立笼座，每个笼座引出来自 8 颗 LPU 的 800G C2C。至于机柜之间如何组网，看起来是菊花链（daisy chain）配置，每个 Node0 连接到另外 2 个 Node0。这些都在 100G AEC 的可达距离之内，必要时也可使用光模块。

## NVIDIA 的 CPO 路线图

NVIDIA 在 GTC 2026 主题演讲上公布了其 CPO 路线图，Jensen 第二天在金融分析师问答会上又做了补充评论。尽管许多人对 CPO 用于 Rubin Ultra Kyber 的机柜内纵向扩展寄予厚望，NVIDIA 的重心却是用 CPO 来实现更大的 world-size 计算系统。

![](https://substack-post-media.s3.amazonaws.com/public/images/7d80c4f7-60e6-41ea-859b-f4ad8ddbf5ea_2064x397.png)
*来源：SemiAnalysis AI 网络模型、NVIDIA*

**在 Rubin 世代**，NVIDIA 将以 Oberon NVL72 形态提供 Rubin GPU，纵向扩展网络全铜。至于 Rubin Ultra，正如我们所预期的，Oberon 和 Kyber 机柜形态下的 Rubin Ultra 将只提供铜互联纵向扩展方案。Rubin Ultra 还将提供更大的 world-size 系统：连接 8 个各含 72 颗 Rubin Ultra GPU 的 Oberon 机柜，组成所谓的 NVL576。CPO 纵向扩展将用于构建这一更大的 world size，以两层全互联网络连接机柜之间，而机柜内部的纵向扩展仍将基于铜。

**到了 Feynman 世代**，CPO 的使用将通过另一个大 world-size 机柜进一步扩展，即由 8 个 Kyber 机柜组合而成的 NVL1152。勾勒机柜配置路线图的 [NVIDIA 技术博客](https://developer.nvidia.com/blog/nvidia-vera-rubin-pod-seven-chips-five-rack-scale-systems-one-ai-supercomputer/)写道「NVIDIA Kyber 将采用类似的直接光互连用于机柜间纵向扩展，扩展为一个庞大的全互联 NVL1152 超级计算机」，而黄仁勋在金融分析师问答会上确实说过 Feynman 的 NVL1152 将「全面采用 CPO」。至于机柜内的纵向扩展是否仍会使用铜、还是 CPO 将取代铜，目前尚存分歧。

NVIDIA 的一贯做法是：能用铜就用铜，必须用光才用光。Feynman 世代的 NVL1152 架构将遵循同一原则。NVL1152 机柜之间采用 CPO 已无悬念，但从 GPU 到 NVLink 交换机目前的生产默认方案（POR）仍是铜。NVIDIA 无法实现电气 lane 速率的再一次翻倍——从 224Gbit/s 双向（bi-di）到 448Gbit/s 单向（uni-di）——这意味着（铜方案下）带宽并没有那么可观。

虽然相比通过裸片到裸片连接光引擎，448G 高速 SerDes 在引出宽度（shoreline）、传输距离和功耗方面都面临巨大挑战，但 Feynman 的制造难度、成本和可靠性又决定了到交换机的连接必须用铜。

话虽如此，NVL1152 这个 SKU 距离问世还有数年——路线图极有可能变动。目前我们的基准假设是：机柜内用铜、机柜间用 CPO，但这随时可能改变。

眼下，我们对 NVIDIA CPO 路线图的最佳估计如下：

Rubin：

- NVL72——Oberon 全铜纵向扩展

Rubin Ultra：

- NVL72——Oberon 全铜纵向扩展
- NVL144——Kyber 机柜全铜纵向扩展
- NVL288——Kyber 机柜全铜纵向扩展，用铜把 2 个机柜连在一起
- NVL576——8 个 Oberon 机柜，机柜内铜互联纵向扩展，机柜间经交换机 CPO 互联，两层全互联拓扑。该版本将仅供测试、量很小

Feynman：

- NVL72——Oberon 机柜——全铜
- NVL144——Kyber 机柜——全铜
- NVL1152——8 个 Kyber 机柜——机柜内铜互联，机柜间经交换机 CPO

  ![](https://substack-post-media.s3.amazonaws.com/public/images/10cf337a-41ad-4a0e-b9a3-bd2f11c911f0_2389x905.png)
  *来源：SemiAnalysis、NVIDIA*

## Oberon 与 Kyber 更新、更大 World Size 登场、更多网络更新

NVIDIA 对其 Kyber 机柜形态给出了期待已久的更新——这是继 Oberon（于 GTC 2025 以原型首秀）之后产品阵容的最新成员。作为原型，机柜架构一直在演进，我们注意到一些变化。首先，每个计算刀片（compute blade）密度提升，各搭载 4 颗 Rubin Ultra GPU 和 2 颗 Vera。全机柜共 2 个 canister、每个 18 片计算刀片，合计 36 片计算刀片、144 颗 GPU。而最初的 Kyber 设计是每个计算刀片 2 颗 GPU 加 2 颗 Vera CPU，共 4 个 canister、每个 18 片计算刀片。

以下细节基于 Rubin Kyber 原型，但 Rubin Ultra 会重新设计。

![](https://substack-post-media.s3.amazonaws.com/public/images/6e91ff96-9d44-4d04-8a1f-eeb1575b235d_3000x4000.jpeg)
*来源：SemiAnalysis*

与 GTC 2025 原型相比，每个交换刀片（switch blade）高度也翻倍，每片交换刀片含 6 颗 NVLink 7 交换芯片，每机柜 12 片交换刀片，合计每个 Kyber 机柜 72 颗 NVLink 7 交换芯片。GPU 通过 2 块 PCB 中板（midplane）与交换刀片全互联，即每个 canister 1 块中板。

![](https://substack-post-media.s3.amazonaws.com/public/images/4c5a1ad2-cfca-47a0-be02-f39b150e8df4_3000x4000.jpeg)
*Kyber 中板 PCB（GPU 侧）。来源：NVIDIA、SemiAnalysis*

对 Rubin Ultra NVL144 Kyber 而言，[正如我们多次告知客户的，纵向扩展不会使用 CPO](https://semianalysis.com/institutional/multi-vertical-note-kyber-cpo-sku-will-be-a-low-volume-test-rack/)，尽管有其他分析师散布 Kyber 引入纵向扩展 CPO 的传言。不过，NVLink 的光学化正在到来，并将逐步导入。纵向扩展 CPO 将首先用于 Rubin Ultra NVL576 系统，连接 8 个 Oberon 形态的机柜，构成两层全互联网络。但机柜内部的纵向扩展网络仍将使用铜背板。这一系统仍属小批量/测试用途。

回到 Kyber 机柜：每颗 Rubin Ultra 逻辑 GPU 提供 14.4Tbit/s 单向纵向扩展带宽，每颗 GPU 通过一个 80DP 连接器（使用其中 72 个 DP × 200Gbit/s 双向通道 = 14.4Tbit/s）连接到中板。要把全部 144 颗 GPU 连成全互联网络，需要 72 颗 NVLink 7.0 交换芯片，每颗提供 28.8Tbit/s 单向聚合带宽。

![](https://substack-post-media.s3.amazonaws.com/public/images/a6507cbc-367c-4f8e-9f8a-6fcbccf61aa3_1513x655.png)
*来源：SemiAnalysis*

在下面的 Kyber 交换刀片照片中，可以看到有 2 块独立 PCB，各承载 3 颗交换芯片。交换刀片应配备 6 个 152DP 连接器，每块中板由 3 个连接器服务。照片是采用较低密度连接器的原型刀片，因此连接器有 12 个而非我们预期量产版的 6 个。

![](https://substack-post-media.s3.amazonaws.com/public/images/1bef24fc-b8ed-4652-a928-7abd4cf2d496_4000x3000.jpeg)
*来源：NVIDIA、SemiAnalysis*

每颗 28.8T NVLink 交换芯片拥有 144 条 200G lane（同时双向），这意味着每颗交换芯片向每个连接器引出 24 条 200G lane。各交换芯片通过铜质飞线（flyover）线缆连接到中板，因为涉及的距离对 PCB 走线而言太长。这也解释了为什么交换芯片离中板更远——为飞线的走线腾出空间。

![](https://substack-post-media.s3.amazonaws.com/public/images/376fc839-5860-4555-a18c-3b591ec13156_1582x1372.png)
*来源：SemiAnalysis 网络模型*

每颗 NVLink 交换芯片通过飞线连接到交换刀片边缘的连接器（使用 144 个 DP × 200Gbit/s 双向通道 = 28.8Tbit/s），这些连接器再插入中板。NVIDIA 正在研究使用共封装铜（co-packaged Copper）以进一步降低损耗，以防 NPC 不奏效。据我们所知，NVIDIA 正告知供应链全力转向全共封装铜方案。

#### **Rubin Ultra NVL288**

尽管 NVIDIA 在 GTC 2026 上并未官方讨论，但供应链内部已在探索 NVL288 概念。它将由两个相邻摆放的 NVL144 Kyber 机柜组成，用机柜间铜背板将两柜相连。一种可能是全部 288 颗 GPU 全互联，但这需要比现有 NVLink 7 交换芯片更高端口数（radix）的交换芯片——后者最多只有 144 个 200G 端口。

如果部署 Rubin Ultra NVL288，每颗 Rubin Ultra GPU 将拥有 14.4Tbit/s 单向纵向扩展带宽，需要 144 个 DP 的线缆连接 NVLink 7 交换芯片。每颗 GPU 72 个 DP 乘以 288 颗 GPU，意味着连接这一更大 world-size 域共需额外 20,736 个 DP。这涉及海量线缆，因此这是线缆用量的上限。

28.8T NVLink 交换芯片的端口数限制了每颗交换芯片在保证跨机柜连通性的前提下所能连接的 GPU 数量。要么改用更高端口数的交换芯片，要么该架构就得接受一定程度的收玫比（oversubscription），同时可能采用类 dragonfly 的网络拓扑。这也会减少所需的铜缆 DP 数量。

![](https://substack-post-media.s3.amazonaws.com/public/images/addf00bd-ed41-47b8-864e-35e96b6768c1_1613x1158.png)
*来源：SemiAnalysis*

供应链目前的全部证据都指向 NVSwitch 7 与 NVSwitch 6 带宽相同，但坦率说这有点不合逻辑。我们相信 NVSwitch 7 的带宽和端口数实际上是 NVSwitch 6 的 2 倍，这样才能实现全互联，而且从系统角度看，这在架构上也最合理。

#### **Rubin Ultra NVL576**

要把纵向扩展的 world size 推到 144 颗 GPU 以上、跨多个机柜，就需要光学互联——我们正在逼近铜互联可达范围内的最大计算密度。Rubin Ultra NVL576 如今已列入路线图，由 8 个较低密度的 Oberon 机柜组成。

![](https://substack-post-media.s3.amazonaws.com/public/images/ee215fef-65ff-41ce-be3d-1a54c3af2334_2449x1037.png)
*来源：SemiAnalysis*

机柜间连接将需要光学互联，不过严格来说尚未确认是采用可插拔光模块还是 CPO，尽管 CPO 的可能性要大得多。当前的 Blackwell NVL576 原型「Polyphe」使用的是可插拔光模块。

我们此前曾[展示过 GB200 的 NVL576 概念](https://newsletter.semianalysis.com/i/175661160/gb200-nvl576)，用可插拔光模块互联第二层 NVLink 交换机。可插拔光模块的使用导致物料清单（BOM）成本大幅攀升，使交换式全互联方案从 TCO 角度难以为继。不过，Rubin Ultra NVL576 很有可能在 Feynman NVL1152 之前以测试量投产——后者才是我们将看到纵向扩展 CPO 真正规模上量的地方。

这一切的下游影响在我们的机构研究中均有披露——该研究受到所有主要超大规模云厂商、半导体公司和 AI 实验室的信赖，请联系 sales@semianalysis.com。

#### **Feynman**

虽然关于 Feynman 的信息还不多，但主题演讲的惊鸿一瞥足以让我们确信 Feynman 将令人兴奋——三项重大技术创新全部押注于一个平台：[混合键合/SoIC](https://newsletter.semianalysis.com/p/hybrid-bonding-process-flow-advanced?utm_source=publication-search)、A16、[CPO](https://newsletter.semianalysis.com/p/co-packaged-optics-cpo-book-scaling?utm_source=publication-search) 和[定制 HBM](https://newsletter.semianalysis.com/i/174558655/custom-base-die)。

Feynman 采用 CPO 已在路线图上，问题是程度如何？机柜内互联会基于铜还是光？我们将在付费墙后展示可能的配置。**Vera ETL256**

随着 AI 工作负载在 GPU 算力之外还需要更多的数据处理、预处理和编排，CPU 需求正在上升。强化学习进一步推高了需求——CPU 需要并行运行仿真、执行代码并验证输出。由于 GPU 的扩展速度快于 CPU，就需要更大的 CPU 集群来让 GPU 保持满负荷，CPU 正日益成为瓶颈。

Vera 独立机柜直接回应了这一需求，以前所未有的密度将 256 颗 CPU 塞进单个机柜——这一壮举必须依赖液冷。其底层逻辑与 NVL 机柜的设计哲学一脉相承：把计算排布得足够紧凑，让铜互联就能触达机柜内的一切，从而免除 spine 层的光收发器。铜方案节省的成本远超额外增加的散热开销。

![](https://substack-post-media.s3.amazonaws.com/public/images/c9e8a2b9-8417-41bc-aa32-1072b2e68fc0_3000x4000.jpeg)
*来源：SemiAnalysis*

每个 Vera ETL 机柜由 32 个计算托盘组成，上 16 下 16，围绕居中的四个 1U MGX ETL 交换托盘（基于 Spectrum-6）对称排布。这种对称切分是有意为之：它将计算托盘到 spine 的线缆长度差异降到最小，使所有连接都处于铜互联可达范围内。每个交换托盘的后面板端口连接到铜质 spine 用于机柜内通信，而 32 个前面板 OSFP 笼座则提供通往 POD 其余部分的光连接。

机柜内组网采用 Spectrum-X 多平面（multiplane）拓扑，把 200 Gb/s lane 分摊到四台交换机上，在保持单层网络的同时实现完整全互联。每个计算托盘容纳 8 颗 Vera CPU，因此每机柜 256 颗 CPU，全部通过单一扁平的以太网络互联。

![](https://substack-post-media.s3.amazonaws.com/public/images/31febbf5-a0ec-4218-b2d0-e95e40704213_4000x3000.jpeg)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/91ab19c1-1ceb-4b0b-a13e-6de00121eebd_1427x199.webp)
*来源：NVIDIA*

## CMX 与 STX

我们在上一篇 Rubin 文章和存储模型中已详细写过 NVIDIA 的 CMX（即 ICMS）平台。NVIDIA 这次推出了 STX 参考存储机柜架构。

#### **CMX**

**CMX** 是 NVIDIA 的上下文存储（context memory storage）平台。CMX 针对的是现代推理基础设施中一个日益凸显的瓶颈：为支撑长上下文与智能体（agentic）工作负载而快速膨胀的 **KV 缓存**。

KV 缓存随输入序列长度和用户数线性增长，是预填充性能（首 token 时间）的主要权衡项。在大规模场景下，设备上的 HBM 容量不够。主机 DRAM 作为额外一层缓存在 HBM 容量之外延伸，但在单节点总量、内存带宽和网络带宽上也存在极限。于是 NVMe 存储登场，用于进一步卸载 KV 缓存。

NVIDIA 在 1 月的 CES 上为推理存储层次引入了一个「新」的中间存储层「G3.5」。G3.5 层 NVMe 位于 G3 层 DRAM 与 G4 层共享存储（同为 NVMe，或 SATA/SAS SSD，或 HDD）之间。它此前被称为 **ICMS（Inference Context Memory Storage）**，如今以 **CMX 平台**的品牌亮相——本质上只是通过 BlueField NIC 把存储服务器挂到计算服务器上的又一次品牌重塑。与普通 NVMe 架构唯一的区别是把 Connect-X NIC 换成了 BlueField NIC。

![](https://substack-post-media.s3.amazonaws.com/public/images/b3a0a186-dbca-4e82-b477-f41c8148e2f3_1336x1258.jpeg)
*来源：NVIDIA 2026 年 1 月的 ICMS 原始博客——2026 年 3 月 16 日更新重发 https://developer.nvidia.com/blog/introducing-nvidia-bluefield-4-powered-inference-context-memory-storage-platform-for-the-next-frontier-of-ai/*

#### **STX**

为扩展 CMX 的覆盖范围，NVIDIA 还发布了 STX。STX 是一个参考机柜架构，采用 NVIDIA 基于 BF-4 的存储方案，与 VR（Vera Rubin）计算机柜互补。该参考架构实际上明确规定了给定集群需要多少硬盘、Vera CPU、BF-4 DPU、CX-9 NIC 和 Spectrum-X 交换机。

![](https://substack-post-media.s3.amazonaws.com/public/images/ddb9b036-0027-4510-975b-9c707ca486c4_3000x4000.jpeg)
*STX 中的 BF-4。来源：NVIDIA、SemiAnalysis*

与 VR NVL72 中的 BF-4（由一颗 Grace CPU 和单个 CX-9 NIC 组成）不同，STX 参考设计中的 BF-4 包含一颗 Vera CPU、两个 CX-9 NIC 和两个 SOCAMM 模块。每个 STX 机箱包含两个 BF-4 单元，合计两颗 Vera CPU、四个 CX-9 NIC 和四个 SOCAMM 模块。整个 STX 机柜共 16 个机箱，即 32 颗 Vera CPU、64 个 CX-9 NIC 和 64 条 SOCAMM。

![](https://substack-post-media.s3.amazonaws.com/public/images/31ef2de0-8f01-45f0-bea0-0fca1c8744ee_878x1030.png)
*STX 机柜（左）。来源：NVIDIA、SemiAnalysis*

STX 发布还伴随着 NVIDIA 一贯的实力展示：他们把所有主要存储厂商都列为 STX 的支持者，包括 AIC、Cloudian、DDN、Dell Technologies、Everpure、Hitachi Vantara、HPE、IBM、MinIO、NetApp、Nutanix、Supermicro、Quanta Cloud Technology（QCT）、VAST Data 和 WEKA。

综合来看，BlueField-4、CMX 与 STX 代表着 NVIDIA 更宏大的布局：将集群在存储层的设计标准化。NVIDIA 已经拿下计算层和网络层，并正随着时间推移积极进军存储、软件和基础设施运维层。

接下来在付费墙后，我们将分享更多关于这一切如何影响供应链的细节，包括 LPX 系统的受益方以及更新后的 Kyber 机柜。我们还将揭晓一个 NVIDIA 尚未发布的机柜概念。
