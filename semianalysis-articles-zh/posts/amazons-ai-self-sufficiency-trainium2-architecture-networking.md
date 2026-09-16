---
title: "亚马逊的 AI 自给自足 | Trainium2 架构与网络"
title_en: "Amazon’s AI Self Sufficiency | Trainium2 Architecture & Networking"
subtitle: "Trn2、Trn2-Ultra、性能、软件、NeuronLinkv3、EFAv3、TCO、3D 环面、网络成本、供应链"
date: 2024-12-03
source: https://newsletter.semianalysis.com/p/amazons-ai-self-sufficiency-trainium2-architecture-networking
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball", "Reyk Knuhtsen"]
tags: ["Hardware Architecture", "Hyperscaler", "Accelerators"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 亚马逊的 AI 自给自足 | Trainium2 架构与网络

> 原文：[Amazon’s AI Self Sufficiency | Trainium2 Architecture & Networking](https://newsletter.semianalysis.com/p/amazons-ai-self-sufficiency-trainium2-architecture-networking) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Trn2、Trn2-Ultra、性能、软件、NeuronLinkv3、EFAv3、TCO、3D 环面、网络成本、供应链**

亚马逊目前正在进行全球规模最大的 AI 集群建设之一，部署数量可观的 Hopper 和 Blackwell GPU。除了向基于 Nvidia 的集群投入巨额资本开支（capex）之外，AWS 还在向 Trainium2 AI 集群[投入数十亿美元量级的资本开支](https://semianalysis.com/accelerator-industry-model/)。AWS 目前正在为 Anthropic 部署一个包含 400k 颗 Trainium2 芯片的集群，名为「Project Rainier」。我们的[业界领先的加速器模型](https://semianalysis.com/accelerator-industry-model/)近一年来一直掌握着与亚马逊这场庞大产能爬坡相关的单位出货量、成本、规格以及许多其他细节（涉及 Marvell 等多家供应商）。

迄今为止，亚马逊基于 Trainium1 和 Inferentia2 的实例由于硬件规格偏弱、软件整合不佳，在 GenAI 前沿模型的训练或推理上一直缺乏竞争力。随着 Trainium2 的发布，亚马逊完成了一次重大的路线修正，正走在一条最终能够在芯片、系统以及软件编译器/框架层面提供有竞争力的定制芯片（custom silicon）训练与推理能力的道路上。

需要说明的是，由于 Titan 和 Olympus 等内部模型均告失败，亚马逊目前仍处于危机模式。此外，尽管继 Google 之后，亚马逊已牢牢确立了自己在定制 AI 芯片竞赛中**远远落后的**第二名地位，但它仍然严重依赖 Nvidia 的产能。亚马逊的 Trainium2 并非一颗经过验证的「训练」芯片，其大部分出货量将集中在 LLM 推理上。亚马逊对 Anthropic 新增的 40 亿美元投资，实际上会回流到 Project Rainier 这个 400k Trainium2 集群中，而且目前还没有其他大客户。

## **AWS Trainium1 / Inferentia2 在 GenAI 上的弱点**

2022 年，AWS 发布了 Trainium1 和 Inferentia2 芯片。Trainium1 芯片和 Inferentia2 芯片几乎完全相同，区别仅在于 Inferentia2 芯片只有两个 Neuronlink-v2 互连端口，而 Trainium1 有四个端口。

![](https://substack-post-media.s3.amazonaws.com/public/images/48bd5ace-2700-4917-a40b-4e7a4c84ce79_1200x533.png)
*来源：AWS*

由于纵向扩展（scale-up）和横向扩展（scale-out）网络缺乏竞争力，加上大量软件缺陷也拖累了客户的工作负载，Trainium1/Inferentia2 在 GenAI 训练上的表现一直不尽如人意。因此，Trainium1/Inferentia2 反而被用于训练亚马逊内部非复杂的非 GenAI 工作负载（例如信用卡欺诈检测 AI 模型），以及为 Anthropic 和亚马逊内部工作负载做推理。

颇具讽刺意味的是，Trainium1 用于 GenAI 推理的表现反而好于训练。在内部，亚马逊也一直在使用 Inferentia2 进行推理，例如在 2024 年 Prime Day 期间，超过 80k 颗 Inferentia2/Trainium1 芯片被用于驱动亚马逊的一个机器学习助手，为 Amazon.com 的 [Prime 会员](https://www.youtube.com/watch?v=UTlghIzmLDI)提供服务。

## **AWS Trainium2 规格总览**

随着 Trainium2 的推出，这一切都有望改变：AWS 如今明确瞄准复杂的 GenAI LLM 推理和训练工作负载。这是一颗约 500W 的芯片，每颗芯片具备 667 TFLOP/s 的稠密 BF16 算力和 96GByte 的 HBM3e 内存容量。

Trn2 将同时使用 HBM3 和 HBM3e，但当前所有 SKU 都已通过固件将速率统一设置为 HBM3 的 2.9TByte/s。未来，AWS 可能会推出一个定制 SKU，配备 HBM3e 的芯片将达到 3.2TByte/s。

![](https://substack-post-media.s3.amazonaws.com/public/images/82b0978a-65eb-48f6-b6d9-9e5eeb6e8a35_1494x1210.png)
*来源：SemiAnalysis*

另一项关键进步在于 Trainium2 的纵向扩展网络。Nvidia 的纵向扩展网络名为 NVLink，在 H100 上每颗 GPU 的带宽为 450GByte/s，而 InfiniBand 横向扩展网络为 50GByte/s；Google TPU 的纵向扩展网络名为 ICI，AWS 的纵向扩展网络则名为 NeuronLink。所有配备纵向扩展网络的 AI 集群部署仍然会使用一个后端横向扩展网络。纵向扩展网络提供的高带宽域用于实现那些要求高带宽、低延迟的并行方案，例如张量并行（Tensor Parallelism）；而横向扩展网络的低带宽域则用于其他相对不那么延迟敏感的并行形式，例如数据并行。Nvidia 借助 GB200 NVL72 从 8-GPU NVLink 域转向 72-GPU NVLink 域，是[将大模型推理成本降低约 14 倍的最重要驱动因素之一](https://semianalysis.com/2024/04/10/nvidia-blackwell-perf-tco-analysis/)，因为它使得在较小的纵向扩展域中无法实现的种类繁多的并行方案成为可能。

**Trainium2 有两种 SKU**：第一种将每台服务器单元中的 16 颗 Trainium2 芯片以 4x4 2D 环面（torus）拓扑连成一个单一的纵向扩展 world size；第二种则将每台服务器单元（跨越两个机柜）中的 64 颗 Trainium2 芯片以 4x4x4 3D 环面拓扑连成一个单一的纵向扩展 world size，即 Trainium2-ultra。相比仅采用 4x4 2D 环面的 Trainium1，Trainium2-ultra 现在提供了一个额外的连接维度。这一额外维度使得张量并行和激活分片（activation sharding）可以跨越整个纵向扩展域进行。

**Trainium2-ultra 将成为亚马逊内部工作负载以及 Anthropic 工作负载进行 GenAI 前沿模型训练与推理的主力 SKU**。我们将在本文后面深入解析 NeuronLink 纵向扩展网络。

## **Trainium2 与 TPUv6e/GB200/H100 的对比**

Trainium2 的纵向扩展拓扑对于 16 芯片 SKU / 64 芯片 SKU 分别是 2D / 3D 环面，这意味着 Trainium2 的纵向扩展网络更接近 TPU 式的拓扑（只是 Trainium2 的 world size 要小得多），而不是 Nvidia NVLink 式的拓扑。关键区别在于：Trainium 和 TPU 采用点对点连接，而 NVLink 采用交换机（Switch）并实现全互联（all to all）连通。

Trainium2 与其他加速器的主要差异在于其算术强度（Arithmetic Intensity）低得多，为每字节 225.9 BF16 FLOP，而 TPUv6e/GB200/H100 的目标为每字节 300 至 560 BF16 FLOP。算术强度的计算方法是用 FLOP/s 除以以 Byte/s 为单位的 HBM 带宽，它表示计算吞吐与内存带宽之比。对这一指标进行分析很重要，因为许多应用（例如推理）经常受内存带宽瓶颈限制，导致计算 FLOPS 利用不足，因此不同的算术强度可能意味着某款加速器更适合特定的任务或技术——后文会详细讨论。

![](https://substack-post-media.s3.amazonaws.com/public/images/099005a0-c5f9-438b-b8f8-e75fb6a865bd_2256x1218.png)
*来源：SemiAnalysis*

将 Trainium2 设计成较低的算术强度，可能是一个正确的选择，因为得益于机器学习研究的进步，模型的算术强度增长已经放缓。突出的例子包括非常流行的混合专家（Mixture of Experts，MoE），它使用分组 GEMM（Grouped GEMMs）。在分组 GEMM 中，每个 token 最多只会被路由到少数几个专家，因此，与稠密前馈网络（FFN，其中每个被「看到」的 token 都要与每份权重进行计算）相比，需要加载的权重所对应的内存量要大得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/ce9a3c48-901c-4588-99dd-44bc027696db_858x635.png)
*来源：SemiAnalysis*

按纵向扩展域中的芯片数量归一化后，我们可以看到 Trainium2 的算术强度仍然更低，而且由于 Trainium2 的 world size 较小——Trainium2-Ultra 为 64 颗芯片，而 TPUv6e 的 world size 为 256 颗芯片——每个纵向扩展 world size 的聚合峰值 FLOP/s 也低得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/02f1ef2d-254a-4d11-be4e-3246d8d20e14_1015x713.png)
*来源：SemiAnalysis*

## **AWS Trainium2 封装**

每颗 Trainium2 芯片由两个计算小芯片（chiplet）和四堆 HBM3e 内存组成。每个计算小芯片通过 CoWoS-S / R 封装与其紧邻的两个 HBM3e 堆栈通信，芯片的两半之间则通过 ABF 基板互连。当一个计算小芯片试图访问非紧邻 HBM 堆栈的内存时会有轻微的性能损失，因此可能需要进行 NUMA 感知的编程才能达到峰值性能，这一点与 MI300X 的小芯片类似。芯片中还有两颗无源结构性硅裸片（structural silicon die）。

![](https://substack-post-media.s3.amazonaws.com/public/images/dc24a6eb-7135-4b33-8b99-bb49badc5e9c_2178x1272.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/2e7a1fc8-2f84-412f-9707-78bcdfaf0f37_824x667.png)
*来源：SemiAnalysis、AWS*

[SemiAnalysis 加速器模型](https://semianalysis.com/accelerator-industry-model/)对每颗 Trainium2 ASIC 的所有相关成本进行了估算，涵盖计算小芯片、HBM 堆栈成本、CoWoS 封装成本等。

## **AWS Trainium2 微架构**

与 Trainium1 和 Google TPU 一样，Trainium2 由少量大型 NeuronCore 核心组成。这与 GPU 形成鲜明对比，后者使用大量更小的张量核心（tensor core）。大型核心通常更适合 GenAI 工作负载，因为它们的控制开销更小。H100 SXM 上有 528 个张量核心，GB200 上大约有 640 个张量核心。每个 NeuronCore 中有四个引擎：

- 张量引擎（Tensor Engine）
- 向量引擎（Vector Engine）
- 标量引擎（Scalar Engine）
- GPSIMD

![](https://substack-post-media.s3.amazonaws.com/public/images/32b5fca8-eae8-4da6-b4bb-e337c3273987_1000x826.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/2eb4e4d9-5bf5-4150-ada3-160222e54664_673x407.png)
*来源：AWS*

第一个是**张量引擎（Tensor Engine）**，它是一个 128x128 的脉动阵列（Systolic Array），从一个名为「SBUF」的 SRAM 缓冲区获取输入，并将结果输出到一个名为「PSUM」的部分和（partial sum）SRAM 缓冲区。张量引擎可以在矩阵乘法（matmul）的 K 维度上循环，并将每个结果的部分和累加起来得到完整结果。在现代 LLM 工作负载中，超过 80% 的功耗和 FLOPS 都将消耗在张量引擎 / 脉动阵列上。

接下来是**向量引擎（Vector Engine）**，它专为加速向量运算而设计——即每个输出元素依赖于多个输入元素的运算，例如在注意力层计算 softmax，或在层归一化/批归一化层中计算滑动平均值和方差。NeuronCore 调度器可以进行并行化调度，使所有引擎同时工作。例如在注意力计算中，向量引擎可以在脉动阵列计算 QxK^T 矩阵乘法或 AxV 矩阵乘法的同时，计算当前 tile 的 softmax。

![](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/general/nki/trainium_inferentia2_arch.html#vector-engine)
*来源：AWS*

第三个是**标量引擎（Scalar Engine）**，它专为执行 1:1 映射的运算而设计，例如逐元素（element wise）运算，如 SeLU、Exp，或在 Linear 层末尾加上偏置（bias）。

最后，在 NeuronCore 内部还有多个图灵完备的 **GpSimd 引擎**，它们可以运行任意 C++ 代码，使任何 C++ 开发者都能快速运行自定义算子（custom ops）。例如，GpSimd 引擎可用于自注意力层中，此时需要应用三角掩码（triangular mask），使当前 token 无法看到任何未来 token，只能看到当前和过去的 token。不过，随着由 [Tri Dao 的 Flash-Attention](https://arxiv.org/abs/2205.14135) 和 [Horace He 的 FlexAttention](https://pytorch.org/blog/flexattention/) 推广开的块稀疏注意力（Block Sparse Attention）的发展，应用三角掩码的重要性未来可能会逐渐下降。

此外，与 Trainium1 一样，Trainium2 拥有专用的集合通信（collective communication）核心，专门负责与其他芯片通信。这是一项出色的创新，因为它可以实现计算与通信的重叠（overlapping），且计算资源与通信资源之间**不存在**任何争用。

相比之下，在 Nvidia 和 AMD 的 GPU 上，通信运算与计算运算运行在相同的核心（SM）上。因此，终端用户需要仔细平衡运行通信算子的 SM 与运行计算算子的 SM 之间的比例。在 GPU 上，这是通过「[NCCL_MIN_NCHANNELS](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html#nccl-min-nchannels)」环境变量标志来实现的，在实践中是一项相当复杂的调优工作。

由于这种复杂性，只有最资深的用户才会去做通信/计算 SM 比例的调优。此外，执行通信运算往往会降低运行计算运算的 SM 的 L2 缓存命中率（cache hint rate）。因此，[Nvidia PTX 提供了缓存提示（cache hints）](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html#cache-operators)，让集合通信内核工程师可以告诉 GPU 跳过将其元素存入 L2 缓存。

总体而言，我们认为拥有专用的集合通信核心是一种更简洁的设计，更有利于优化通信与计算的重叠。

![](https://substack-post-media.s3.amazonaws.com/public/images/10b484c6-6565-44a3-b3ed-f3c625799ed6_450x449.png)
*来源：AWS*

拥有这么多专用引擎看似是个绝妙的主意，因为与通用化资源相比，专用资源消耗的功耗和面积更少，但它也可能带来瓶颈。各种专用资源的配比必须提前很久确定下来，这就带来了该配比对于各种不同工作负载而言可能失衡的风险。某些资源会一直利用不足，而另一些资源则始终在限制性能。从某种意义上说，在工作负载仍在演进之时过早地将架构专用化，可能是一个有风险的决定。

## **服务器架构**

Trainium2 和 Trainium2-Ultra 服务器的基本构建模块，是我们所称的 Trainium2「物理服务器」（Physical Server）。每台 Trainium2 物理服务器采用独特的架构，占用 18 个机柜单元（RU），由一个 2 机柜单元（2U）的 CPU 主托盘（head tray）连接八个 2U 计算托盘（compute tray）组成。在服务器的背面，所有计算托盘通过一个无源铜背板（passive copper backplane）连成 4x4 2D 环面，这与 GB200 NVL36 类似；不同之处在于，GB200 NVL36 的背板将每颗 GPU 连接到若干 NVSwitch，而 Trainium2 不使用任何交换机，所有连接都只是两颗加速器之间的点对点连接。

![](https://substack-post-media.s3.amazonaws.com/public/images/377b7613-f4e4-4cc6-8f53-3f60cef0e395_693x565.png)
*来源：SemiAnalysis*

每个 2U 计算托盘包含两颗 Trainium 芯片，没有 CPU。这与 GB200 NVL72 架构不同，后者的每个计算托盘中同时包含 CPU 和 GPU。每个 Trainium2 计算托盘通常也被称作 JBOG（"just a bunch of GPUs"，「只是一堆 GPU」），因为每个计算托盘没有任何 CPU，无法独立运行。

因此，每台 Trainium2 服务器容纳 16 颗 Trainium2 芯片。两台 16 芯片 Trainium2 服务器可装入一个机柜。对于 Trainium2-Ultra SKU，每台服务器由四台各含 16 颗芯片的物理服务器组成，因此总共容纳 64 颗芯片，占用整整两个机柜。我们将在下文更详细地描述机柜布局并提供立面图（elevation diagram）。

![](https://substack-post-media.s3.amazonaws.com/public/images/e37d2ebf-5bbc-4976-acee-e47070406a77_1387x770.png)
*来源：SemiAnalysis*

每个计算托盘通过服务器正面的一根外置 PCIe 5.0 x16 DAC 无源铜缆连接到 CPU 托盘。

![](https://substack-post-media.s3.amazonaws.com/public/images/fa14c96d-8453-4768-b1d1-c8f2dafa2045_612x753.png)
*来源：SemiAnalysis*

## **CPU 托盘**

CPU 托盘内部有 PCIe 交换机，将计算托盘与本地 NVMe 磁盘连接起来，使 Trainium2 能够使用 GPUDirect-Storage 访问存储，而无需经过 CPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/71fc7e1b-f969-4d0e-9ac9-178332749dbe_1556x678.png)
*来源：SemiAnalysis*

每台服务器总共有 16 块本地 NVMe 磁盘，Trainium2 芯片都可以直接访问它们。此外，还有连接到主 CPU0 的标准 80Gbit/s Elastic Block Storage 链路，以及一张用于 AWS 前端网络的主用 100Gbit/s Nitro 卡，该网络称为 Elastic Network Adapter（ENA）。

![](https://substack-post-media.s3.amazonaws.com/public/images/05c2d8ec-52c7-4e4a-9ab5-a8a926ca1719_1524x677.png)
*来源：SemiAnalysis*

每个 CPU 托盘由两颗 Intel Xeon Sapphire Rapids CPU 和 32 个 DDR5 内存 DIMM 插槽组成，最多可支持 2 TB 的 CPU 内存，并采用类似的机柜级 48V 直流母线（bus bar）配电系统。

![](https://substack-post-media.s3.amazonaws.com/public/images/d4096453-722e-4337-934d-c4920540dda5_1114x822.png)
*来源：SemiAnalysis*

## **计算托盘**

如文章开头所述，共有两种 SKU：

- Trainium2（Trn2）
- Trainium2-Ultra（Trn2-Ultra）

我们先讨论普通 Trn2 Trainium2 实例的计算托盘。每个 Trn2 计算托盘在一块 PCB 上有两颗 Trainium2 芯片，并有 6 个服务器内纵向扩展铜背板连接器，用于连接同一台服务器中的其他计算托盘。

![](https://substack-post-media.s3.amazonaws.com/public/images/c8ada0e6-0b6a-4985-af08-06eecd5f703a_871x829.png)
*来源：SemiAnalysis*

此外，对于 Trn2，每个计算托盘最多有八张 200G EFAv3 NIC，可为每颗芯片提供高达 800Gbit/s 的横向扩展以太网带宽。从计算托盘连接到 CPU 托盘的笼形连接器（cage）还需要一个重定时器（retimer）。计算托盘左侧的 Trainium2 芯片将使用通往 CPU 托盘连接的前 8 个通道，而右侧的 Trainium2 芯片将使用该连接的后 8 个通道。

![](https://substack-post-media.s3.amazonaws.com/public/images/97189e05-e528-4395-8d66-51e78dff33ad_1180x642.png)
*来源：SemiAnalysis*

Trn2-Ultra SKU 与普通 Trn2 SKU 非常相似，但 Trainium2 芯片上用于横向扩展网络的 PCIe SerDes 通道更少：Trn2-Ultra 芯片只有 200Gbit/s 的横向扩展带宽，而 Trn2 为 800Gbit/s。这些通道转而被用于将 4 台物理服务器（各 16 颗芯片）互连为一个纵向扩展 world size 为 64 的整体。该纵向扩展网络的实现方式是：每颗芯片拥有两个 16 通道的 OSFP-XD 笼形连接器，插入有源电气铜缆（active electrical copper cable），将四台各含 16 颗芯片的物理服务器连接在一起，构成 world size 为 64 颗芯片的 Trn2-Ultra 服务器。

![](https://substack-post-media.s3.amazonaws.com/public/images/f16fa914-07ed-46ce-b82b-c64bd92b271e_933x826.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/2693ee7d-bd39-46f2-ae9d-8479bde1bfd9_1340x632.png)
*来源：SemiAnalysis*

## **系统/机柜架构**

接下来讨论系统/机柜架构，我们先从普通的 Trn2 SKU 讲起。每个机柜将包含两台 Trn2 服务器和四台 12.8T ToR EFAv3 以太网交换机，为每颗芯片提供高达 800Gbit/s 的横向扩展带宽。这种机柜采用类似的 48V 直流母线架构，交流到直流的转换在机柜级完成，而不是由每个机箱单独进行转换。

![](https://substack-post-media.s3.amazonaws.com/public/images/d03c5dc3-da8d-4be9-97de-2b978b10ec70_652x1177.png)
*来源：SemiAnalysis*

Trn2-Ultra SKU 的每个纵向扩展域由四台 16 芯片物理服务器组成，因此每个纵向扩展域有 64 颗芯片；它由两个机柜构成，配置与 GB200 NVL36x2 类似。为了沿 z 轴形成环面，每台物理服务器使用一组有源电气铜缆连接到另外两台物理服务器。

![](https://substack-post-media.s3.amazonaws.com/public/images/793df66c-3ee4-4264-a0ca-e87cbbe66e5a_1758x1132.png)
*来源：SemiAnalysis*

## **功耗预算**

我们对每种 SKU 的机柜功耗进行了估算：Trn2-Ultra 64 芯片服务器的两个机柜各需要 24kW 功耗（每台 Trn2-Ultra 64 芯片服务器合计 48kW）。

![](https://substack-post-media.s3.amazonaws.com/public/images/2fb4a101-ac79-4e6c-85b9-08e434e48518_1103x1140.png)
*来源：SemiAnalysis*

用于容纳普通 Trn2 服务器的机柜功率密度为 27kW，但请记住，一个机柜中会容纳两台 16 芯片 Trn2 服务器。容纳 Trn2 服务器的机柜功率密度更高，是因为需要额外的 NIC 以及更多、更高端口数（radix）的 ToR 交换机，以支持每颗 Trainium2 芯片高达 800Gbit/s 的横向扩展网络；与 Trn2-Ultra 服务器额外的服务器间 AEC NeuronLinkv3 线缆相比，这些部件消耗的功耗更多。

![](https://substack-post-media.s3.amazonaws.com/public/images/095cc0ef-6f5d-46c9-8531-a1034d26f70f_1062x1138.png)
*来源：SemiAnalysis*

## **Project Rainier——400k Trainium2 集群**

我们认为最大的 Trainium2 集群部署之一将位于印第安纳州。AWS 目前正在这里为 Anthropic 部署一个包含 400k 颗 Trainium2 芯片的集群，名为「Project Rainier」。

该园区[已完成第一期的建设，目前有七栋建筑，每栋拥有 65MW 的 IT 功率，总计 455MW](https://semianalysis.com/datacenter-industry-model/)。这个印第安纳州 AWS 园区的第二期将再增加九栋 65MW 的建筑，总功率达到 1,040MW。我们认为该园区的 PUE 约为 1.10-1.15，因为园区位于印第安纳州北部。除了 Trainium2 部署之外，该数据中心园区还将与 AWS 传统的面向 CPU 的服务器以及 AWS 的 Blackwell 集群部署共用。

![](https://substack-post-media.s3.amazonaws.com/public/images/94ed0075-6b19-4bd2-bff5-911b087e87a4_1359x847.png)
*来源：SemiAnalysis 数据中心模型*

我们认为，AWS 将以 16 个机柜为一个封闭通道单元（containment pod）来部署 Trainium2 机柜，并在末端额外放置 4 个机柜，用于网络交换机、管理交换机以及共同放置在封闭通道内的其他服务器。冷空气将从服务器前面进入，而服务器背面则将热空气强力排入烟囱（chimney）。

![](https://substack-post-media.s3.amazonaws.com/public/images/223f5283-1d20-4085-a0d1-aa8d373f2bce_1280x506.png)
*来源：SemiAnalysis*

请注意，400k 颗 Trainium2 的原始算力（raw flops）低于一个 100k GB200 集群。这意味着，鉴于阿姆达尔定律（Amdahl's law）可能让它们吃尽苦头，Anthropic 将很难与竞争对手的 100k GB200 集群抗衡。在 400k 颗 Trainium2 和 EFA 之间做 all reduce 将非常困难，因此 Anthropic 需要在异步训练方面做出相当大的创新突破。

## **网络总览**

上文我们已经提及并讨论了网络拼图中的各个部分，而本节将全面解释 Trainium2 架构所使用的所有网络。

基于 Trainium2 的实例上有四种不同类型的网络：

- 纵向扩展（Scale-up）：NeuronLinkv3

  - 服务器内（Intra-Server）NeuronLinkv3
  - 服务器间（Inter-Server）NeuronLinkv3
- 横向扩展（Scale-out）：Elastic Fabric Adaptor EFAv3
- 前端与存储：Elastic Network Adaptor（ENA）、Elastic Block Store（EBS）
- 带外管理网络（Out of Band Management Networking）

NeuronLinkv3 是一种纵向扩展网络，是 AWS 版的 Nvidia NVLink 互连。与 Nvidia 的 NVLink 互连不同，NeuronLinkv3 分为两种类型：服务器内和服务器间。服务器内 NeuronLink 将每台物理服务器内的 16 颗芯片连接在一起，而服务器间 NeuronLink 则将来自不同物理服务器的芯片连接起来，形成总计 64 颗芯片的 world size。每颗芯片拥有 640GByte/s 的单向带宽，最多与 6 个直接邻居相连。

与 NeuronLinkv3 有限的 64 芯片 world size 相比，EFAv3 后端/计算网络（fabric）用于将通信从数十个机柜扩展到数千个机柜。尽管 EFAv3 可以连接多得多的芯片，但缺点是它比 NeuronLink 网络慢得多。在 Trn2 SKU 上，EFAv3 网络慢 6.4 倍；在 Trn2-Ultra SKU 上，EFAv3 网络慢 25.6 倍。

简单回顾一下：前端网络只是一个普通的以太网，用于连接互联网、SLURM/Kubernetes，以及用于加载训练数据和模型检查点（checkpoint）的网络存储。对于每台包含一个 CPU 托盘的 16 芯片物理服务器，有 100Gbit/s 的 ENA 前端网络和 80Gbit/s 的专用 EBS 块存储网络。

最后是带外管理网络。它用于重装操作系统镜像，以及监控节点健康状况，如风扇转速、温度、功耗等。服务器、PDU、交换机、CDU 上的基板管理控制器（BMC）通常都连接到这个网络，以监控和控制服务器及其他各种 IT 设备。

在接下来的几节中，我们将更深入地探讨并详细解释上述部分网络主题与网络架构。

## **NeuronLinkv3 纵向扩展网络**

每台 Trainium2 物理服务器都有一个铜背板：每颗芯片通过 JBOG PCB 板上的一条 PCB 走线连接到另一颗芯片（即同一 JBOG 上的左侧 Trainium2 芯片连接右侧 Trainium2 芯片），每颗芯片还通过铜背板连接到三颗其他服务器内芯片。NeuronLinkv3 基于 PCIe Gen 5.0，即每通道 32Gbit/s（单向）。

![](https://substack-post-media.s3.amazonaws.com/public/images/69928680-eb55-4392-b07c-cf63c568861b_1173x938.png)
*来源：SemiAnalysis*

每颗芯片使用 32 条 PCIe 通道连接其他服务器内芯片，这意味着每颗芯片与其每个服务器内邻居的通信速率为 128GByte/s（单向）。服务器内 NeuronLinkv3 是一个 2x2x2x2 超立方体（hypercube）网格。

![](https://substack-post-media.s3.amazonaws.com/public/images/5bd4ef15-6144-4fa7-a522-5bc5b8ea06d1_925x1024.png)
*来源：SemiAnalysis*

## **2x2x2x2 超立方体 == 4x4 环面的同构证明**

有趣的是，2x2x2x2 的 4D 超立方体与 4x4 2D 环面是同构的（isomorphic），这意味着每台 Trainium2 物理服务器实际上就是一个 4x4 2D 环面。

同构的数学证明非常简单。我们只需检查两个图的顶点总数和边总数是否相同，以及每个顶点在每个图中是否拥有相同数量的橙色、蓝色和绿色邻居。从下面的可视化图中可以清楚地看到，两个图都有 16 个顶点、32 条边，且两个图中的每个顶点都有 1 条橙色边、1 条绿色边和 2 条蓝色边。由于满足所有这些条件，它们确实是同构的。

![](https://substack-post-media.s3.amazonaws.com/public/images/428b253d-649d-466b-b302-b1074d9d04e4_1920x624.png)
*来源：SemiAnalysis*

## **服务器间 NeuronLinkv3 纵向扩展**

在 Trainium2 Trn2-Ultra SKU 中，四台物理服务器连接在一起，构成一台纵向扩展域内拥有 64 颗芯片的「Ultra 服务器」。这 64 颗芯片以 4x4x4 3D 环面的方式连接在一起，其中 z 轴的点对点带宽只有 64GByte/s，而 x 轴和 y 轴为 128GByte/s，是 z 轴的两倍。每颗芯片通过每个连接一条 OSFP-XD 有源电气铜缆，连接到其他物理服务器中的两颗芯片。这样，芯片就能够在 z 轴上形成带有回绕（wrap-around）连接的链（物理服务器 A -> 物理服务器 B -> 物理服务器 C -> 物理服务器 D -> 物理服务器 A）。

![](https://substack-post-media.s3.amazonaws.com/public/images/d2b87fa0-d225-4560-b415-24920bc375b9_2074x916.png)
*来源：SemiAnalysis*

这种 4x4x4 3D 环面与 TPU 的立方体（cube）机柜设计非常相似，后者同样是 4x4x4 3D 环面，并且三个轴上的点对点带宽都是对称的。Trainium2 拓扑与 TPU 拓扑的另一个区别在于：TPU 立方体可以通过光模块和 OCS 在全部六个面上连接到其他 TPU 立方体，而 Trainium2 不支持这一点。

![](https://substack-post-media.s3.amazonaws.com/public/images/ef4d812c-1693-4576-a123-a22127170a65_397x403.png)
*来源：Google*

关于纵向扩展与横向扩展带宽的取舍，亚马逊和 Anthropic 很可能达成了妥协，因为得益于 PCIe 物理层允许在 NIC 与 NeuronLinkv3 之间重新分配通道，两者是可以互相转化的。Trainium2 的 NeuronLinkv3 通道数量只够构建一个 world size 为 32、三个轴上点对点带宽对称的 4x4x2 3D 环面，但对于前沿 LLM 的训练和推理而言，world size 为 64 但带宽不对称的方案，很可能比 world size 只有 32 的更小方案好得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/fb5b3624-1afd-4318-861b-2418b6205e8c_636x1101.png)
*来源：SemiAnalysis*

## **NeuronLinkv3 不使用 PCIe 光模块**

由于每个机柜有两台物理服务器，这些物理服务器能够在不到 2 米的距离内形成一个环，从而可以保持在 PCIe AEC 的传输范围之内。

![](https://substack-post-media.s3.amazonaws.com/public/images/129f67a1-a09d-4bd4-9724-51fc4a6c519d_1288x838.png)
*来源：SemiAnalysis*

如果 AWS 当初把 Trainium2 架构设计成更低的机柜功率密度，从而每个机柜只能容纳一台服务器，那么它们就必须构建一个由四台物理服务器组成的环来形成 64 芯片的 Ultra 服务器，此时 AWS 就需要使用 PCIe 光模块了，因为最长的连接将横跨四个机柜，超出了 PCIe AEC 的范围。

![](https://substack-post-media.s3.amazonaws.com/public/images/df9be3b4-d315-4ff9-b03d-76bc5064bca4_2098x1063.png)
*来源：SemiAnalysis*

与实际选定的设计（使用便宜得多、可靠得多的 AEC）相比，引入 PCIe 光模块会使 NeuronLinkv3 服务器间网络的可靠性下降多个数量级、成本上升多个数量级。

## **Trn2-Ultra-Max-Plus 4x4x16 概念 SKU**

由于 NeuronLink 服务器间架构是一个 3D 环面，且沿 z 轴的第 5、第 6 个邻居通过 AEC 连接，我们认为有可能将 z 轴从仅 4 台服务器扩展到 16 台服务器，沿着热通道封闭（hot aisle containment）一侧的服务器物理排列方向延伸。

我们提出一个名为「trn-2-ultra-max-plus」的概念 SKU，它将 256 颗芯片以 4x4x16 3D 环面连接在一起，而不是正式发布（General Availability）的 Trn2-Ultra SKU 中的 64 颗芯片。这个概念 SKU 的点对点带宽在 x 轴和 y 轴上仍为 128GByte/s，在 z 轴上仍为 64GByte/s。

我们认为，256 颗芯片将是 AEC 和无源铜缆所能达到的上限，超过这个范围就需要使用 PCIe 光模块来连接单个热通道封闭区之外的各排机柜。

更大的纵向扩展 world size 将使那些无法装进单台 Trn2-Ultra 64 芯片服务器的相对较大的模型得以更高效地训练。这个概念的一个缺点是，它意味着许多芯片将在环面这样的点对点拓扑中被永久地绑定在一起。

![](https://substack-post-media.s3.amazonaws.com/public/images/7519fe44-683b-4605-9fd2-510f272474c2_2362x853.png)
*来源：SemiAnalysis*

## **作业爆炸半径（Job Blast Radius）**

当许多芯片以点对点环面拓扑连接在一起时，只要环面中有任意一颗芯片发生故障，整个环面纵向扩展域就会失效。这会导致有效吞吐（goodput）低下，TPUv2 pod 和 TPUv3 pod 就曾出现过这种情况。对于 Trn2-Ultra，如果 Trn2-Ultra 服务器内的 64 颗芯片中只要有一颗发生故障，全部 64 颗芯片都将无法贡献任何有效工作。在我们的概念 SKU trn2-ultra-max-plus 中，鉴于有 256 颗芯片串连在一起，只要 256 颗芯片中有 1 颗发生故障，**全部** 256 颗芯片都会被视为宕机。

对于 TPUv4，Google 针对这个巨大的作业爆炸半径问题提出了解决方案。该方案是在一个个 4x4x4 环面立方体之间使用可重构光交换机（OCS），从而在纵向扩展 pod 规模高达 4k 颗芯片的情况下，将每次芯片故障的爆炸半径限制在仅 64 颗芯片。

![](https://substack-post-media.s3.amazonaws.com/public/images/00e80351-fb1c-4699-b305-e74ff0f8722f_1024x759.png)
*来源：Google*

正如下方 TPU pod 立方体地图所示，不同用户可以构建一个绕开故障立方体（红色立方体）的 3D 环面。尽管这是一个巧妙的解决方案，但我们认为 AWS 并没有走这条在每个 4x4x4 立方体之间放置 OCS、拥有巨型 world size 的路线，因为 OCS 无论从软件还是硬件角度部署都非常复杂，而且需要使用昂贵的光模块。光链路需要收发器，而收发器由于需求旺盛仍然供应短缺，且[单位带宽的价格往往比无源 DAC 铜缆贵 10 倍](https://arxiv.org/pdf/2304.01433)。正是因为光模块成本极其高昂，你会看到 TPU 立方体内部大多使用 DAC 铜缆，这也是 Nvidia GB200 NVL72 的纵向扩展网络采用铜缆的一个关键原因。

![](https://substack-post-media.s3.amazonaws.com/public/images/d073084a-0b8a-4119-bab7-6b331201e4b4_1024x568.png)
*来源：Google*

尽管在一个立方体内部，单颗芯片故障意味着整个立方体停止服务，但芯片之间网络链路的故障通常可以被绕开。话虽如此，我们预计网络链路可靠性会很高，因此我们并不认为 Trainium2 NeuronLinkv3 网络链路会频繁故障或震荡（flap），因为所有链路都使用无源铜缆和有源铜缆。

通过光收发器实现的网络链路与无源/有源电气铜缆链路相比，平均故障时间（MTTF）差异巨大。由于收发器激光器故障，光链路的 MTTF 可能为 100 万到 1,000 万小时，而铜缆的典型 MTTF 约为 1 亿小时，可靠性要好 10 到 100 倍。

可能比更长的 MTBF 更重要的是，与光模块相比，无源/有源电气铜缆发生震荡（flapping）的概率要低几个数量级。震荡是光系统中的常见问题：由于激光器问题和/或模块过热，链路会断开一段时间，短则几微秒，长则数秒。对于依赖稳定网络在芯片之间进行通信的训练作业而言，震荡会造成巨大问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/9079684a-0643-4a2a-9cd3-292efd16d275_1979x958.png)
*来源：OCP 2024*

由于 TPU 在立方体之间使用光链路，Google 不得不创建容错路由（fault tolerant routing），以应对收发器和/或 OCS 发生故障的情况。有了容错路由，当光链路断裂时，整个 pod 不会完全停止服务，而是在 LLM 训练工作负载上仅出现轻微减速即可继续运行。与让一个立方体做零有效工作相比，这种轻微的减速对整个物理 TPU 系统的有效吞吐大有裨益。

然而，需要注意的是，TPU 的容错路由只能帮助应对链路断开的问题；当发生芯片级故障时，仍然会形成 64 颗芯片的爆炸半径，因为 JAX/PyTorch 要求长方体形状且无空洞的拓扑。

我们认为，在实践中 Trainium2 将不需要实现容错路由，因为其链路采用无源和有源铜缆，NeuronLink 故障实际上将为零，链路可靠性将比 TPU 跨立方体光系统好 100 倍。如果出于某种原因，这些无源和有源铜缆链路开始成为重要的错误来源，那么 Trainium2 的 Neuronx 集合通信团队就需要着手实现容错路由了。

## **EFAv3 横向扩展以太网**

对于 Trainium2，为了在单个互连集群中扩展到数万颗芯片，AWS 将使用其自研的以太网方案，称为 Elastic Fabric Adapter Version（EFAv3）。对于普通 Trn2（16 芯片）实例，它将支持每颗芯片高达 800Gbit/s 的 EFAv3 带宽；对于 Trn2-Ultra（64 芯片），则为每颗芯片 200Gbit/s 的 EFAv3 带宽。如上所述，Trn2-Ultra SKU 将是最大的前沿训练和推理工作负载中最常用的实例。与 EFAv2 NIC 高达 9 微秒的包延迟相比，EFAv3 NIC 的包延迟更低，为 6.5 微秒。包延迟是决定集合通信算法带宽（algorithmic bandwidth）能跑多快的主要因素之一。我们将在即将发布的 NCCL 集合通信深度解析文章中更详细地解释这些概念。

与 Nvidia 的参考网络设计不同，亚马逊目前不会使用轨道优化（rail optimized）网络。也就是说，一台服务器内的所有芯片都将连接到同一机柜内的同一台直接交换机，这被称为「机柜顶部」（Top of Rack，ToR）网络设计。

![](https://substack-post-media.s3.amazonaws.com/public/images/276454c7-4409-40c1-92a7-061bc1556b22_1024x947.png)
*来源：NVIDIA*

这意味着平均而言，与轨道优化拓扑（大多数流只需一跳）相比，每个流在网络中需要经过更多跳数。在 ToR 设计中，**必须**有极其出色的自适应路由（adaptive routing）来避免不同并发流之间的路径冲突。诸如用队列对 ID（queue pair ID）代替标准五元组进行哈希等技术，可以提高网络的信息熵，从而限制流冲突的数量。

下图展示了我们对这种无阻塞（non-blocking）ToR 网络的仿真热力图，其中浅蓝色表示因拥塞导致的带宽下降，深蓝色表示接近满线速。正如你所见，使用 ToR 拓扑可以达到线速，但由于全部 8 条流进入同一台交换机，仍然存在相当程度的拥塞，吞吐量变得更加不稳定，高拥塞导致这些流的可用带宽下降。

![](https://semianalysis.com/2024/10/03/ai-neocloud-playbook-and-anatomy/)
*来源：SemiAnalysis 新兴 GPU 云（Neocloud）文章*

尽管 ToR 网络性能较差，但我们认为 AWS 选择基于 ToR 的网络而非轨道优化设计的原因在于：ToR 更便宜，且可靠性更高，因为 ToR 架构从 AI 芯片到第一级直接交换机之间可以使用铜缆。相比之下，在轨道优化设计中，每颗 AI 芯片可能要连接到远处的机柜，许多链路就不得不使用光模块。AWS 曾在内部试验过轨道优化，但由于上文讨论的可靠性影响以及快速部署的诉求，他们选择坚持 ToR 架构。减少光模块的使用，也降低了因 AI 热潮带来的空前需求增长而导致的全球光收发器持续短缺所引发问题的风险敞口。

ToR 的另一个好处是：通常在 AI 集群中，横向扩展 NIC 到其第一级直接交换机之间存在单点故障。而在 ToR 架构中，连接横向扩展 NIC 与 ToR 交换机的无源 DAC 铜缆的 MTTF 好 100 倍，震荡少 100 倍。AWS 将在 NIC 与 ToR 交换机之间使用 400G QSFP-DD 转两个 200G QSFP56 的无源铜缆。

![](https://substack-post-media.s3.amazonaws.com/public/images/5104524d-04b1-475a-9a06-b30b1896e493_1993x1290.png)
*来源：Molex*

对于机柜内的 ToR 交换机，我们认为大多数将是基于 Marvell Teralynx 6.4T 和 12.8T 交换芯片的白盒交换机。在 ToR 交换机上，AWS 会在 Broadcom 与 Marvell 的商用交换 ASIC 之间进行多供应商采购。

![](https://substack-post-media.s3.amazonaws.com/public/images/b784f048-05b4-4526-a7f7-76260356278e_2560x1440.jpeg)
*来源：Marvell*

对于 Leaf 和 Spine 交换机，AWS 将使用基于 Broadcom Tomahawk4 芯片的 1U 25.6T 白盒交换机。

AWS 不会用多台交换机组建成机箱式模块化交换机（chassis based modular switch），因为这种配置的爆炸半径太大。如果机箱发生故障，那么该机箱连接的所有线卡和链路都会失效，受影响的 Trainium2 芯片可能达到数百颗。大多数超大规模云厂商通常对这类物理机箱式模块化交换机避之不及，因为其潜在爆炸半径太大。

![](https://substack-post-media.s3.amazonaws.com/public/images/2fd0b4b5-0d04-4856-a803-fa41a4fc65dc_590x1024.png)
*来源：Arista*

取而代之的是，AWS 更愿意使用虚拟模块化交换机（virtual modular switch）：用无源和有源电气铜缆将单个机柜内的多台 1U「披萨盒」（pizza box）交换机连接起来，构成一台本质上的模块化交换机。这样就不会有单一故障会影响到很大的爆炸半径。[我们在我们的新兴 GPU 云（Neocloud）剖析文章中解释了更多关于虚拟模块化交换机的内容，并讨论了它们的优缺点。](https://semianalysis.com/2024/10/03/ai-neocloud-playbook-and-anatomy/#virtual-modular-switch)

## **EBS+ENA+OOB**

每台 Trainium2 物理服务器都将有一条连接到 AWS 托管块存储（称为「Elastic Block Storage」，EBS）的专用 80Gbit/s 链路，以及一条称为「Elastic Network Adapter」（ENA）的 100Gbit/s 前端链路。它们将为常规网络流量（例如容器拉取、SLURM/Kubernetes 管理流量）提供快速访问。这两个网络都使用 AWS 自研的 Nitro DPU 卡，将 VPC 和安全功能卸载到硬件上，从而释放 CPU 资源。最重要的是，这些 Nitro 卡能够精确测量通过 NIC 的流量，从而对这些流量精确计费！请注意，物理张量和 AI 流量不会在这些网络上运行，而只会在我们之前讨论过的 EFAv3 横向扩展网络和 NeuronLinkv3 纵向扩展网络上运行。

## **网络连接器与线缆成本**

对于 Trainium2 的两种 SKU，TE 都将是背板的独家供应商，每台服务器将包含 48 个连接器和 1,536 根铜缆。与 GB200 NVL72 的 NVLink 线缆从 GPU 连接到 NVLink 交换机不同，Trainium2 的线缆是每颗芯片之间的点对点连接。Trn2-Ultra SKU 还将使用 AEC 线缆，由 Astera Labs 供应。我们认为，网络连接器和线缆的总成本合计将达到每颗芯片近 $1,000。

![](https://substack-post-media.s3.amazonaws.com/public/images/60ce96ab-8d8e-4dd2-8912-d0fff90ba24c_723x1031.png)
*来源：SemiAnalysis*

对于 Trn2 SKU，虽然没有服务器间 NeuronLinkv3 AEC 线缆，但每颗芯片 EFAv3 带宽提升至高达 800Gbit/s 所增加的成本，远远抵消了这部分节省，使网络连接器与线缆的总成本升至每颗芯片约 $1.2k。

![](https://substack-post-media.s3.amazonaws.com/public/images/144cbd0d-4e05-41ae-aba5-34e0ca7442d3_723x852.png)
*来源：SemiAnalysis*

## **软件**

设计定制 AI 芯片最具挑战性的方面之一是软件，其中 ML 编译器以及融入现有 ML 科学家工作流程时的出色用户体验都至关重要。

此前，在 Trainium 上使用这颗 AI 芯片的唯一途径是通过 PyTorch XLA Lazy Tensor ML 编译器，这是一个非常糟糕的 API，会产生大量缺陷，而且缺乏可移植性。我们认为 AWS Trainium 团队此后已经完成了路线修正，提供了一种类似 Triton 的 tile 编程语言来直接编写内核（Kernel）。此外，Trainium 软件团队现在已对 JAX 提供了 beta 支持——JAX 是一个更偏向 XLA ML 编译器和环面拓扑静态编译 AI 芯片的 ML 框架。Trainium 和 Trainium2 与 TPU 非常相似，它们都是采用环面拓扑的巨型脉动阵列芯片，因此 Trainium 软件如今通过 XLA 支持 JAX，将是一个更合适的软件栈。

总体而言，由于 Trainium2 将完整的 ISA 汇编暴露给终端用户，糟糕的软件可以被 Anthropic 等高级用户绕过。在 Anthropic，他们拥有极其聪明的程序员，即使当前软件仍有不足，也会为了充分发挥 Trainium2 的全部能力而直接编写汇编。

## **XLA**

PyTorch XLA 的梦想是使用惰性张量（lazy tensor）来跟踪并编译计算图和所有 PyTorch 算子，只在遇到图中需要物化（materialization）的部分时才在 Trainium 设备上运行该图。这对简单模型很有效，但惰性张量的问题在于，只要给 ML 模型架构增加任何一点复杂性，就会出现大量缺陷。使用大量控制流语句会破坏惰性张量，尤其是在大量使用依赖数据的控制流语句时。此外，对于包含数十万个计算算子的巨型计算图（例如大型 LLM 模型），由于 Python 本身速度较慢，惰性地跟踪图也会带来很高的开销。

![](https://substack-post-media.s3.amazonaws.com/public/images/aa9904b2-8f73-404c-a3f8-6e1f2b6f4cbb_865x436.png)
*来源：SemiAnalysis*

PyTorch XLA 的目标是：一旦 PyTorch<>XLA 将计算图跟踪并转换为 StableHLO，XLA 就能执行图优化，例如删除构成恒等式（identity）的子图，以及进行纵向 + 横向融合（vertical + horizon fusion）。然后 XLA 会将其下层（lower）为依赖硬件的图，进行向量化（vectorization）和流水线（pipelining）优化，生成高性能的内核。

![](https://substack-post-media.s3.amazonaws.com/public/images/5f3e3903-6090-4fae-a7a2-0b746593c177_1271x712.png)
*来源：AWS*

PyTorch 2.0 引入了一种利用 Python 字节码解释来捕获计算图的新方法，称为「TorchDynamo」。

TorchDynamo 能够将计算图捕获到一个名为「Aten IR」的 IR 中，其中计算 IR 的每个节点都是一个 Aten 算子。然后，编译器后端可以将这个 Aten IR 图作为输入，将其下层为某个领域特定的内部 IR，例如 XLA 的 StableHLO 或 Inductor IR。我们认为这个 API 更适合 Trainium XLA，通过 Dynamo API 对 PyTorch 的支持也会好得多。

关于 TorchDynamo XLA 的坏消息是，目前 TorchDynamo 会将训练图拆分为三个图（前向、反向、优化器步进），而不是一个完整图，导致性能不如 LazyTensor XLA。好消息是 Meta 团队正在致力于在 TorchDynamo 中捕获完整图，而这项工作可以扩展到 TorchDynamo XLA。

对 Trainium 而言的坏消息是，PyTorch<>XLA 代码路径通常没有在 Meta 内部被广泛使用，因此主要由 AWS 和 Google 的 PyTorch 团队维护，这也是 PyTorch<>XLA 代码路径存在大量缺陷的主要原因。此外，Google 和 AWS 的 PyTorch 团队相比各自的 JAX 团队都属于二等公民，因为 DeepMind 和 Anthropic 等实验室的工作负载都通过 JAX 技术栈运行。

同样，Meta 也没有在内部对 PyTorch AMD 代码路径进行广泛的实战测试。我们将在即将发布的文章《Training of MI300X vs H100 vs H200 Comparsion》中进一步讨论 AMD 的性能。AWS 团队应该与 Meta 合作，针对 Meta 的内部生产训练工作负载对 Trainium2 进行内部实战测试，让 PyTorch Trainium2 的软件体验变得出色！

传统上，JAX 在使用 Google 内部 XLA ML 编译器时只支持 Google 的 TPU 芯片，但我们认为 JAX 的编程模型同样非常适合 Trainium2，因为 TPU 和 Trainium2 都是拥有巨型脉动阵列、使用 3D 环面静态编译图的 AI 芯片。这意味着 Trainium 接入 XLA 编译器插件和 PRJT 运行时是顺理成章的。JAX 的逻辑长方体网格（logical cuboid mesh）和轴（axis）与 Trainium 拓扑非常契合。AWS 最近宣布其 JAX <> Trainium 集成开启公开 beta，这是一个非常令人兴奋的方向。

## **NKI 内核语言**

Neuron Kernel Language（NKI）——读作「Nicky」——是 Trainium 用于编写内核的领域特定语言，类似于 NVIDIA 的 CUDA 和 OpenAI 的 Triton 语言。与 Nvidia 的 CUDA 语言不同，NKI 像 OpenAI 的 Triton 编程语言一样基于 tile 编程。NKI 将让专家级程序员能够在 Trainium2 芯片上达到接近极限速度（speed of light，SOL）的性能。

除了 AWS 自己的公开文档和内核示例之外，为了普及 NKI 内核语言的知识与教育，亚马逊还与[斯坦福合作给学生布置作业](https://github.com/stanford-cs149/asst4-trainium)，专注于编写真实世界的内核，例如融合卷积 + max_pool。我们欣赏他们前进的方向，因为要想与 CUDA 生态系统竞争，AWS 必须以生态和开源的方式来推进 NKI 内核语言的教育。

![](https://substack-post-media.s3.amazonaws.com/public/images/861cd465-267d-4a6a-8152-43582905c0e8_1270x703.png)
*来源：AWS*

## **分布式调试与性能分析工具**

亚马逊还提供了极其细粒度的内核级和分布式系统级调试与性能分析（profiling）工具，类似于 Nvidia 在其 GPU 生态系统中提供的工具。我们认为这是正确的方向，因为它能让专家级终端用户发现其训练和推理工作负载的瓶颈并加以修复。

与 Nvidia Nsight Compute 类似，你可以查看内核级别的性能分析，查看张量引擎（Tensor Engine）的活动情况以及 SRAM 寄存器压力等指标。

![](https://substack-post-media.s3.amazonaws.com/public/images/ec77510d-0cad-461e-a420-de8440fbf996_1531x1086.png)
*来源：AWS*

在 Nvidia 生态系统中拥有 Nvidia Nsight Systems 和 PyTorch Perfetto 性能分析器等价工具的地方，Trainium2 生态系统则有 Neuron Distributed Event Tracing。它使 ML 工程师能够调试分布式性能问题，并查看通信与计算的重叠程度。在某些方面，它比开箱即用的 PyTorch profiler 更好，因为它会自动合并来自所有 rank 的所有 trace，而不是让[终端用户手动编写脚本合并各个 rank 的 trace，而这些脚本本身可能包含缺陷](https://github.com/mosaicml/composer/blob/main/composer/profiler/json_trace_merger.py)。

![](https://substack-post-media.s3.amazonaws.com/public/images/df5a95ae-ad01-4af4-8fa9-31844a1fc8b5_3678x2212.png)
*来源：AWS*

此外，亚马逊公开了大部分 ISA 和精确的周期时间（cycle time），这使得开发者在调试和性能分析时能获得比在基于 Nvidia 的 GPU 上开发好得多的体验。这意味着，与故意对用户隐瞒细节的 Nvidia GPU 相比，从硬件中榨取真正的极限性能要容易得多。

## **集合通信库**

在集合通信方面，AWS 创建了一个 Trainium 专用的库，称为 [NeuronX Collective Communication Library](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/general/arch/neuron-features/collective-communication.html)。这个库类似于 Nvidia 的 NCCL，提供了一整套集合通信算法和集合通信原语（collectives），如 All Reduce、All Gather、Reduce Scatter 等，专为 Trainium2 的 2D/3D 环面拓扑而构建。终端用户可以通过 C++ 接口（或通过 Python 绑定）直接访问该库，XLA ML 编译器也可以在编译阶段自动插入集合通信调用。Trainium2 还能够使用一种名为「GPUDirect RDMA」的技术直接与它的 EFAv3 NIC 通信，而无需经过 CPU。此外，借助 AWS 自研的 libfabric，它们可以实现内核 OS 旁路（kernel OS bypass），进一步降低包延迟。

Trainium 的 NeuronX 集合通信库[目前不支持 All to All 集合通信](https://github.com/aws-neuron/aws-neuron-sdk/issues/572)。All to All 集合通信对于混合专家（MoE）模型中使用的专家并行（expert parallelism）极其重要。该 issue 于 2022 年 10 月创建，大约三周前以来一直处于不活跃状态，原因是 AWS 想要支持 [DataBricks 的 DBRX MoE 模型](https://github.com/aws-neuron/aws-neuron-sdk/issues/956)以及其他即将推出的模型。Databricks 最近宣布与 AWS 建立「合作伙伴关系」，使用 Trainium2 芯片进行训练和推理。我们认为，Databricks 将成为 GenAI 推理领域第二大 Trainium2 外部客户。

自本文发布以来，AWS 团队已经关闭了该 issue，理由是 all to all 一年前就已经得到支持，只是该 issue 并未反映真实情况。

![](https://substack-post-media.s3.amazonaws.com/public/images/4de76ebb-cd5a-437d-98d8-1d78302d9feb_948x382.png)
*来源：AWS*

## **Ultra 服务器对之间的异步检查点**

为了加快检查点（checkpoint）的保存速度，Trainium NeuronX 软件包提供了跨主机检查点冗余支持。Trainium2 芯片无需在向相对较慢的 S3 或 AWS 托管 Lustre 存储写检查点时空闲等待，而是快速将检查点写入自己服务器的 CPU 内存和/或本地 NVMe 存储，随后 Trainium2 芯片就继续运行其工作负载。

这种方法的问题在于，如果服务器发生严重崩溃（hard crash），检查点将没有任何冗余或其他备份，从而导致大量 Trainium 时（Trainium-hours）的计算时间损失。

![](https://substack-post-media.s3.amazonaws.com/public/images/4f06a2dd-d0ac-483d-bdef-3c252a6df724_1024x563.png)
*来源：AWS*

为了解决这个问题，Trainium2 服务器能够以成对的方式将检查点缓慢复制到其他服务器。此外，为了避免 Trainium2 服务器将检查点复制到相邻服务器时造成训练减速，AWS 声称能够将检查点复制流量调度到训练工作负载没有通信的时间段进行。

![](https://substack-post-media.s3.amazonaws.com/public/images/93344c9f-7cab-49d6-978e-4db2ef5aabdc_1024x569.png)
*来源：AWS*

高级用户可能已经在自己的训练任务中通过其他异步检查点策略实现了类似功能，但这极大地降低了普通用户的使用门槛。

## **工作负载编排**

Trainium2 的终端用户将通过类 SLURM 方式或类 Kubernetes 方式来编排其工作负载。

在类 SLURM 方面，AWS 提供两种托管服务：AWS ParallelCluster 和 AWS Batch。AWS ParallelCluster 基本上就是托管的 SLURM。SLURM 只是一个近乎 Linux/bash 原语的编排器。许多出身学术实验室环境的 ML 工程师/科学家对 SLURM 有强烈偏好，因为它使用 bash 和 Linux 原语。在运行交互式作业和进行代码开发时，它的体验非常出色。这与 Kubernetes 容器方案形成对比，后者开箱即用并不真正支持交互式作业。

在类托管 Kubernetes 的工作负载编排方面，AWS 提供 Elastic Kubernetes Service（EKS）和 Elastic Container Service（ECS）。Kubernetes 开箱即用**并非**为训练工作负载这类需要成组调度（gang scheduling）的批处理作业而构建。Kubernetes 非常适合推理这类面向服务的工作负载，其中每个副本大多数时候就是一台服务器，因此可以只是一个 Kubernetes pod。

要让 Kubernetes 支持训练的批处理/成组调度需要大量工作，要让 Kubernetes 支持交互式工作负载同样需要大量工作。因此，我们确实只看到 OpenAI 和字节跳动（ByteDance）等最大的 AI 实验室采用这种方式，因为它们有能力配备内部集群工程师来构建工具，使 Kubernetes 能够支持成组训练和交互式工作负载。

最后，Kubernetes 通常更适合智能体（agent）训练/推理，以及为 AI 智能体拉起和销毁容器。我们希望这些容器最好经过了安全加固，以防止 AGI 泄漏出去。

## **自动化的被动与主动健康检查**

当单个工作负载扩展到数万颗 AI 芯片时，可靠性是确保训练工作负载成功完成的重要方面。这正是 Nvidia 发布 DCGM 工具的原因。借助 DCGM 诊断，终端用户可以通过数值和全芯片自检测出集群中发生的 80% 的静默数据损坏（silent data corruption，SDC）。我们见过的另一个有趣的相关功能来自 [新兴 GPU 云巨头](https://www.semianalysis.com/p/ai-neocloud-playbook-and-anatomy) Nebius，他们在其 operator 工作负载调度器中实现了一项功能，可以通过 CRON 作业来调度主动健康检查。

![](https://substack-post-media.s3.amazonaws.com/public/images/df9330e3-1ba5-428c-92ea-99fc44af1530_1232x986.jpeg)
*来源：Nebius*

这些主动健康检查可以检查 Nvidia GPU 的 NVLink 网络并运行大量其他检查。此外，它们只需单个节点即可自测其 InfiniBand 网络（做法是禁用 NVLink），而其他用户在测试 IB 时通常需要使用多个节点。

![](https://substack-post-media.s3.amazonaws.com/public/images/e2bbd5df-6e11-4511-bf47-8001c61c7129_865x462.png)
*来源：SemiAnalysis*

在 Trainium2 软件栈方面，也有类似的工具。可以使用 NCCOM 本地测试来自测 NeuronLink 和/或横向扩展 EFAv3 链路。此外，AWS 还提供了一项测试，它会运行一个小型训练工作负载，并确保该工作负载的实际输出与基准（golden）工作负载的输出一致。

接下来，我们将详细讨论 Trainium2 在各种不同服务器配置下的物料清单（BOM）、网络成本、存储成本、电力成本等更多内容。我们还将比较 Nvidia 与亚马逊两种方案在 4k 颗芯片规模下的总集群成本。我们会考察总拥有成本（TCO），并最终与我们的性能估算进行对比。理解这里的性能与 TCO 权衡，对亚马逊定制芯片事业的未来可行性至关重要。
