---
title: "SGLang 在 NVIDIA GB300 NVL72 上解锁 25 倍推理性能"
title_en: "Unlocking 25x Inference Performance with SGLang on NVIDIA GB300 NVL72"
author: "NVIDIA and Community SGLang Developers"
date: "February 20, 2026"
previewImg: /images/blog/gb300_inferencex/img-1.png
source: https://lmsys.org/blog/2026-02-20-gb300-inferencex/
translated: 2026-09-12
---

# SGLang 在 NVIDIA GB300 NVL72 上解锁 25 倍推理性能

> 原文：[Unlocking 25x Inference Performance with SGLang on NVIDIA GB300 NVL72](https://lmsys.org/blog/2026-02-20-gb300-inferencex/) · LMSYS Blog · NVIDIA and Community SGLang Developers

SGLang 团队已与 NVIDIA 在[多代 GPU](https://lmsys.org/blog/2025-05-05-large-scale-ep/) 上紧密合作，为专家混合（MoE）推理模型的大规模部署带来阶跃式的推理性能提升。在此前的[成果](https://lmsys.org/blog/2025-10-14-sa-inference-max/)中，SemiAnalysis InferenceMAXv1 基准显示 Blackwell B200 相比 Hopper H200 已取得 4 倍加速；如今，我们将这一势头延伸到了 Blackwell Ultra。在最新的 InferenceXv2 基准测试中，SGLang 在 GB300 NVL72 上相比 H200 实现了最高 25 倍的性能提升。此外，在不到 4 个月的时间里，我们将 SGLang 在 GB200 NVL72 上的 InferenceXv2 性能提升了最高 8 倍。这些性能提升源于 SGLang 开发者与 NVIDIA 工程团队的紧密协作，并直接转化为更低的延迟、更高的吞吐量，以及大规模专家混合（MoE）推理模型部署中显著降低的单 token 成本。

<img src="/images/blog/gb300_inferencex/img-1.png"
     style="display: block; margin: 20px auto 0; width: 75%; max-width: 100%; height: auto;">

## **搭载 Blackwell Ultra GPU 的 NVIDIA GB300 NVL72**

[NVIDIA GB200 NVL72](https://www.nvidia.com/en-us/data-center/gb300-nvl72/) 已被公认为最强大的纵向扩展（scale-up）数据中心 GPU 平台，它将 72 颗 Blackwell GPU 以 130 TB/s 的带宽连成单一高带宽域。这一架构特别适合 MoE 模型：MoE 模型依赖低延迟的 all-to-all 通信来执行大范围专家并行（Wide Expert Parallel），并在分离式推理服务中于预填充与解码 GPU 之间快速搬运 KV 缓存。

NVIDIA GB300 NVL72 在此基础上采用 Blackwell Ultra GPU，相对 GB200 NVL72 引入了多项关键增强：

**1.5 倍 NVFP4 峰值吞吐量。** 更新的 Tensor Core 使每时钟周期的 FP4 峰值吞吐量相比 Blackwell 提升 1.5 倍，从而加速受算力约束的 MoE 专家与稠密层 GEMM 运算。

**2 倍注意力 Softmax 吞吐量。** 升级后的特殊函数单元（SFU）将 softmax 运算的吞吐量提高 2 倍——softmax 是注意力层的关键组成部分。

**1.5 倍 HBM3e 容量。** Blackwell Ultra 集成了容量更高的 12-Hi HBM3e 堆栈（此前为 8-Hi），无需借助 CPU 卸载（offload）即可支持更大的模型与 batch size。

结合 72 GPU 的庞大 NVL72 域，这些能力提升了 MoE GEMM 的吞吐量，加快了注意力 softmax，并支持分离式推理配置下的超大解码 batch size。



## **GB300 NVL72 带来最高 25 倍的 SGLang 性能提升**

SemiAnalysis InferenceX（前身为 InferenceMAX）是一个持续运行的基准测试套件，在数百个加速器上评估主流开源框架和模型的真实世界推理性能，实时结果发布于 inferencemax.ai。[InferenceMAXv1 发布](https://lmsys.org/blog/2025-10-14-sa-inference-max/)时曾展示出 SGLang 在 Blackwell 上运行 DeepSeek R1 相比 Hopper 最高获取 4 倍性能提升的能力。

在最新的 InferenceXv2 中，NVIDIA 的 GB300 NVL72 机架级系统被纳入了基准测试矩阵。依托与 NVIDIA 的持续合作，SGLang 现已展现出在 GB300 NVL72 上运行 DeepSeek R1 时相比 H200 最高 25 倍的性能表现。这一提升结合了 Blackwell Ultra 的架构进步，以及 SGLang 在整条推理栈上的针对性软件与内核优化。

<img src="/images/blog/gb300_inferencex/img-2.png"
     style="display: block; margin: 20px auto 0; width: 75%; max-width: 100%; height: auto;">

需要说明的是，用于计算 25 倍提升的 H200 基线取自 50 TPS/user 的交互性（interactivity）档位，对应低延迟使用场景。在没有延迟约束的情况下，H200 也能达到相近的吞吐量，详见这篇[此前的博客](https://lmsys.org/blog/2025-05-05-large-scale-ep/)。本文选择 50 TPS/user 作为对比点，以呈现一个对延迟有合理要求的场景。

## **面向 Blackwell Ultra 的推理优化**

为充分释放 GB300 NVL72 上 Blackwell Ultra 的能力，SGLang 引入了覆盖低精度数据格式、内核设计与分离式推理服务的新优化：

**面向 MoE 与稠密层的 NVFP4 GEMM。** 对 MoE 专家及其他 GEMM 使用 [NVFP4 精度](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/)可以降低内存带宽压力，利用 Blackwell Ultra 上更高的 FP4 Tensor Core 吞吐量，并将 token 分发的通信量减半。这缩小了权重在内存中的占用，为更大的 KV 缓存腾出容量，从而支持更高的并发。

**计算-通信重叠。** 我们不再依赖传统的双批次重叠（Two-Batch Overlapping，TBO），而是采用了针对 NVL72 更高互联带宽调优的单批次重叠策略。在实践中，这使得 combine 通信能够以生产者-消费者模式与 down-GEMM 计算并发执行，同时在额外的 CUDA 流上重叠共享专家计算，以最大限度减少空闲时间。

**面向分离式推理的 NVIDIA Dynamo。** 在预填充-解码分离方面，我们集成了开源分布式推理服务引擎 [NVIDIA Dynamo](https://www.nvidia.com/en-us/ai/dynamo/)。Dynamo 的模块化设计使其 KV 感知路由器（KV-aware router）能够与 SGLang 的 HiCache 基数树深度耦合，同时提供 NIXL、Mooncake 等灵活的 KV 缓存传输后端，以适配不同的部署场景。

这些优化共同使推理软件栈与 Blackwell Ultra 的硬件特性相契合，推动更高的利用率，将原始硬件能力转化为实际交付的吞吐量。

## **GB200 NVL72 上的 8 倍性能提升**

尽管 GB300 NVL72 是我们新的性能旗舰，我们仍持续致力于改进 SGLang 在 GB200 NVL72 上的表现。与不到 4 个月前提交的 InferenceMAXv1 相比，采用低精度 NVFP4 的最新 v2 版本在高吞吐场景下单 GPU token 产出最高提升 8 倍，在高交互性场景下单用户 token 产出最高提升 4 倍，使现有 GB200 NVL72 部署获得更优的 token 经济性与终端用户体验。这些结果印证了 NVIDIA 与 SGLang 联合工程协作的力量。

<img src="/images/blog/gb300_inferencex/img-3.png"
     style="display: block; margin: 20px auto 0; width: 75%; max-width: 100%; height: auto;">

## **展望未来**

我们与 NVIDIA 的合作路线图不会止步于 InferenceXv2 上这一 25 倍的初步里程碑。下一阶段合作的重点包括：

在 GB300 NVL72 上启用多 token 预测（MTP），相对 Hopper 进一步释放性能提升

持续优化 GB300 NVL72，兼顾延迟敏感型与吞吐导向型部署

针对 Qwen 模型系列（包括最新的 Qwen 3.5）在 Blackwell 与 Blackwell Ultra 上调优 SGLang

将这些优化带到未来的 NVIDIA Vera Rubin NVL72 系统

通过与 NVIDIA 持续合作，SGLang 致力于不断推动推理性能向前发展，降低下一波前沿推理模型的部署成本。

## **致谢**

我们衷心感谢以下团队与合作者：

NVIDIA 团队：Amr Elmeleegy, Cyrus Chang, Elvis Chen, Grace Ho, Hao Lu, Ishan Dhanani, Jinyan Chen, Julien Lin, Kaixi Hou, Kedar Potar, Kyle Liang, Lee Nau, Mathew Wicks, Nicolas Castet, Pen Chung Li, Po-Han Huang, Qixiang Lin, Shu Wang, Shu-Hao Yeh, Trevor Morris, Weiliang Liu, Xuting Zhou, Yangmin Li 以及许多其他同事

SGLang 核心团队与社区贡献者：Baizhou Zhang, Jingyi Chen, Liangsheng Yin, Shangming Cai, Rain Jiang, Cheng Wan, Qiaolin Yu, Lianmin Zheng
