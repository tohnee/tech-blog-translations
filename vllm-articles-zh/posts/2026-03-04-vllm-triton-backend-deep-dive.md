---
title: "vLLM Triton 注意力后端深度剖析"
title_en: "vLLM Triton Attention Backend Deep Dive"
source: https://vllm.ai/blog/2026-03-04-vllm-triton-backend-deep-dive
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM Triton 注意力后端深度剖析

> 原文：[vLLM Triton Attention Backend Deep Dive](https://vllm.ai/blog/2026-03-04-vllm-triton-backend-deep-dive) · vLLM 博客

作者：IBM Research 的 vLLM 团队

[#性能](https://vllm.ai/blog/tags/performance)[#triton](https://vllm.ai/blog/tags/triton)[#注意力](https://vllm.ai/blog/tags/attention)

本文改编自 Red Hat 主办的 [vLLM Office Hours](https://www.youtube.com/watch?v=8QiM-i9ifFo&list=PLbMP1JcGBmSHxp4-lubU5WYmJ9YgAQcf3&index=1) 活动，主讲人为 IBM Research 的 Burkhard Ringlein，对 vLLM Triton 注意力后端进行了深入的技术讲解。[往期主题见这里](https://www.youtube.com/playlist?list=PLbMP1JcGBmSHxp4-lubU5WYmJ9YgAQcf3)，未来 office hours 的报名请点[这里](https://red.ht/office-hours)。

过去一年，IBM Research、Red Hat 与 AMD 的团队共同开发并向上游贡献了一个基于 Triton 的 vLLM 注意力后端，目标是实现最先进水平（SOTA）的性能，同时在各 GPU 厂商之间保持出色的可移植性。这项工作的动因是加速器硬件日益多样，而维护大量高度专业化内核的成本不断上升。

本文将对这项工作进行深入的技术讲解。我们先解释为什么 [Triton](https://github.com/triton-lang/triton) 适合 [vLLM](https://github.com/vllm-project/vllm)，介绍 Triton 注意力后端及其使用场景，然后深入剖析一个高性能分页注意力内核的实现。过程中我们会涉及内核级优化、并行化策略、CUDA Graph 交互以及基准测试结果，最后简要展望 Helion。

## **Triton 为何有助于 vLLM**

vLLM 的目标是在各种平台、模型与执行策略上提供尽可能好的推理性能。在实践中，这意味着要支持多种加速器及其多个世代、广泛的模型架构，以及多样的负载特征——例如不同的批大小、序列长度和注意力模式。

一种做法是编写大量高度专业化的内核，每个内核都针对特定模型与 GPU 架构调优。这种方法虽然有效，却无法规模化。要在 NVIDIA Hopper 与 Blackwell、AMD MI300、Intel 等众多 GPU 平台乃至未来平台上维护数百个内核，很快就会变得不切实际。

相反，我们更青睐能自动适配运行硬件的性能可移植内核。Triton 后端正是遵循这一思路。

Triton 是一种领域特定语言，让开发者能用 Python 编写 GPU 内核（例如矩阵乘法或注意力）。这些内核会被编译为面向多个平台的高效 GPU 代码。Triton 的分块（tiled）编程模型达成了平衡：它足够底层，能表达与硬件相关的优化；又足够高层，能在很大程度上保持与硬件无关。

如图 1 所示，开发者以逻辑分块（tile）为单位表达计算。Triton 编译器与自动调优器决定这些分块如何映射到底层硬件。分块形状与执行布局在不同 GPU 上可能差异巨大，但这些决策是自动完成的，通常由自动调优引导（更多细节见我们的论文 [GPU Performance Portability needs Autotuning (arxiv.org)](https://arxiv.org/abs/2505.03780)）。

![图 1](https://vllm.ai/blog-assets/figures/2026-03-04-vllm-triton-backend/image1.png)

图 1

图 1：Triton 的分块编程模型。逻辑分块由编译器与自动调优器映射为特定硬件的执行布局。

## **vLLM 中的 Triton 注意力后端**

注意力通常是大语言模型中对性能最敏感的操作。为了管理复杂度，vLLM 引入了名为注意力后端的抽象层，把各种注意力实现隔离在统一 API 之下，并将它们与线性层、层归一化等较简单的组件分开。

在这一抽象之下，vLLM 支持多种注意力后端，包括 CUDA 平台上的 FlashAttention 与 FlashInfer、基于 ROCm 的注意力后端，以及面向 MLA 类注意力的专用后端（完整列表见[这里](https://github.com/vllm-project/vllm/tree/main/vllm/v1/attention/backends)）。[Triton 注意力后端](https://github.com/vllm-project/vllm/blob/main/vllm/v1/attention/backends/triton_attn.py)完全用 Triton 实现，是 vLLM 的原生后端。

这个后端的引入是为了解决性能可移植性与依赖问题。它在 NVIDIA、AMD 与 Intel GPU 上运行同一份源代码，只依赖 PyTorch 与 Triton，并且作为 vLLM 的一部分始终可用。虽然它最初由 IBM Research 与 Red Hat AI 开发，如今已由更广泛的社区维护和扩展。

## **Triton 注意力后端的使用场景**

在运行 ROCm 的 AMD GPU 上，Triton 注意力后端是默认后端；在 Intel XPU 上也会使用它。当以 float32 运行时，vLLM 会回退到 Triton Attention，因为 Flash Attention 在该场景下不支持 fp32。它还支持需要特定特性的模型，例如 StepFun 音频模型使用的 ALiBi sqrt，以及 sink token 和 GPT-OSS 行为——尤其是在 A100 这类 Hopper 之前的 NVIDIA GPU 上。

此外，它还支持小 head 维度的模型、编码器与解码器注意力，以及多模态前缀注意力。由于 Triton 注意力后端始终存在，当 FlashAttention、FlashInfer 或其他依赖不可用或导入失败时，它也充当回退后端。批不变性（batch invariance）等特性同样受到支持。

## **用 Triton 编写高性能、可移植的分页注意力内核**

Triton 注意力后端开始开发时，内核先在 vLLM 之外实现，并通过大量微基准测试进行评估。内核 API 的设计匹配 vLLM 的需求，但性能调优是在端到端集成之前独立完成的。

[微基准测试](https://github.com/foundation-model-stack/vllm-triton-backend)对理解内核在预填充为主、解码为主与混合负载，以及不同批大小与上下文长度下的性能行为至关重要。

图 2 展示了有代表性的微基准测试结果。x 轴表示 token 总数，y 轴表示延迟。独立的子图区分了仅预填充、混合与仅解码负载。这些结果表明，不同的内核变体在不同的区间各有所长，没有任何单一配置能在所有场景中占优。

![图 2](https://vllm.ai/blog-assets/figures/2026-03-04-vllm-triton-backend/image2.png)

图 2

图 2：多个 Triton 分页注意力内核变体在预填充、解码与混合负载下的微基准测试对比。

微基准测试与端到端基准测试互为补充，它能暴露可能被系统级效应掩盖的内核级行为。

## **回顾：分页注意力内核做什么**

分页注意力通过分页管理 KV 缓存，以节省内存的方式实现注意力。对于批次中的每个查询，内核会处理每个查询 token；对每个 token，它遍历各查询头及其对应的 KV 头，然后遍历分页 KV 缓存，计算注意力得分并应用值向量。

这一结构如图 3 所示。查询 token 沿 x 轴排布，查询头沿 y 轴排布，分页 KV 缓存的遍历构成最内层循环。为清晰起见，因果掩码与滑动窗口等细节被省略。

![图 3](https://vllm.ai/blog-assets/figures/2026-03-04-vllm-triton-backend/image3.png)

图 3

图 3：分页注意力的概念视图，展示查询 token、查询头以及分页 KV 缓存的遍历。

关于内核底层优化的详细解释，我们推荐阅读内核作者撰写的 pytorch 博客：<https://pytorch.org/blog/enabling-vllm-v1-on-amd-gpus-with-triton/>

代码见这里：[https://github.com/vllm-project/vllm/blob/main/vllm/v1/attention/ops/triton\\_unified\\_attention.py](https://github.com/vllm-project/vllm/blob/main/vllm/v1/attention/ops/triton%5C_unified%5C_attention.py)

## **利用 Q Block 优化 tl.dot 的分块尺寸**

注意力中的核心计算是矩阵乘法，在 Triton 中用 tl.dot 实现。然而，要获得高性能需要足够大的分块来充分利用硬件，而只是简单加载分页 KV 缓存并不能带来好结果。

KV 一侧的分块尺寸受 KV 缓存页大小的约束，因此优化重点放在查询一侧。对于分组查询注意力（group query attention），把与单个 KV 头相关联的所有查询头一起处理可以提高缓存复用。为进一步提升并行度，多个查询 token 被归入同一个工作项，称为 Q block。

图 4 展示了这种方法。启动网格跨越批大小与 KV 头，而 Q block 决定每个内核实例处理多少查询 token 与查询头。自动调优为每个平台选择合适的块大小。

![图 4](https://vllm.ai/blog-assets/figures/2026-03-04-vllm-triton-backend/image4.png)

图 4

图 4：Q block 将多个查询头与查询 token 合并为单个工作项，以提高 tl.dot 的利用率和缓存复用。

## **用并行分块 softmax 增加并行化**

一次处理多个查询 token 对预填充负载很有效，但对只处理单个查询 token 的解码负载没有好处。为解决这一问题，我们通过并行分块 softmax——即所谓的"3D 内核"——引入了额外的并行化。

这种方法把 KV 缓存的遍历拆分到多个内核实例上。每个实例计算部分结果，之后再归约得到最终输出。由于 Triton 不提供全局屏障，这一归约需要启动第二个内核，从而在额外并行度与启动开销之间形成取舍。我们用启发式规则来判断这种做法何时有益。

## **CUDA Graph、启动网格与 GPU 执行波**

CUDA Graph 通过录制并重放固定的执行图来降低内核启动开销。然而，注意力内核带来了挑战，因为其启动网格往往取决于批大小与序列长度。

GPU 使用固定数量的流式多处理器（SM）执行内核。当启动的线程数超过 SM 数量时，执行会分波进行。图 5 展示了这种行为：第二波会导致利用率不足。

![图 5](https://vllm.ai/blog-assets/figures/2026-03-04-vllm-triton-backend/image5.png)

图 5

图 5：当启动的线程数超过可用的流式多处理器时的 GPU 执行波。本例中 GPU 有 8 个 SM，而我们要执行 12 个线程。

一旦被录入 CUDA Graph，即使实际负载规模下降，这种低效也会被原样重放。图 6 展示了固定启动网格如何导致额外的无效工作和延迟增加。

![图 6](https://vllm.ai/blog-assets/figures/2026-03-04-vllm-triton-backend/image6.png)

图 6

图 6：通过 CUDA Graph 重放固定启动网格时产生的额外无效工作。

## **从可变启动网格到持久化内核**

分页注意力内核的早期版本使用随负载规模伸缩的可变启动网格，如图 7 所示。这种方式虽然灵活，但与 CUDA Graph 的配合很差。

![图 7](https://vllm.ai/blog-assets/figures/2026-03-04-vllm-triton-backend/image7.png)

图 7

图 7：早期分页注意力内核使用的可变启动网格。

为解决这一问题，我们设计了持久化内核（指向 vLLM 的 PR 尚待合并）。启动固定数量的内核实例，数量等于可用的计算资源。每个实例通过从 GPU 内存读取元数据来动态决定要处理多少工作。这使启动网格保持恒定，让 CUDA Graph 能被高效复用。

![图 8](https://vllm.ai/blog-assets/figures/2026-03-04-vllm-triton-backend/image8.png)

图 8

图 8：采用固定启动网格与动态工作分配的持久化内核方案。

## **基准测试结果**

2025 年末的基准测试结果证明了这一方法的有效性。图 9 展示了在 NVIDIA H100 与 AMD MI300 上，Llama 3.1 8B 在批大小为 1、输入长度为 500 token 时的端到端延迟结果，输出长度标注在 x 轴上。

在 H100 上，对于较长的解码请求，Triton 注意力后端达到了 FlashAttention 3 性能的 100.7%。在 MI300 上，相比早期实现取得了约 5.8× 的加速。重要的是，两个平台使用的是同一份 Triton 内核源代码。请注意，Triton 中的分页注意力实现大约有 800 行代码，而 FlashAttention3 约有 70'000 行代码。

![图 9](https://vllm.ai/blog-assets/figures/2026-03-04-vllm-triton-backend/image9.png)

图 9

![图 9](https://vllm.ai/blog-assets/figures/2026-03-04-vllm-triton-backend/image10.png)

图 9

图 9：Triton 分页注意力与 FlashAttention 3 在 NVIDIA H100 与 AMD MI300 上的端到端延迟对比。结果以最左侧的基线归一化。

## **前瞻：Helion 中的分页注意力**

[Helion](https://github.com/pytorch/helion) 是 PyTorch 团队推出的新领域特定语言，可以视为更高层的 Triton，或"分块的 PyTorch"。作为实验，我们在 Helion 中实现了一个简化的分页注意力内核，早期结果令人鼓舞。这项工作已发表于 [PyTorch 博客](https://pytorch.org/blog/portable-paged-attention-in-helion/)，代码以[草稿 pull request](https://github.com/vllm-project/vllm/pull/27293) 的形式放在 vLLM 仓库中。

## **结论**

随着模型、推理优化与硬件平台的持续进步，性能可移植性变得日益重要。vLLM 的 Triton 注意力后端证明：仅凭一个可移植的内核实现，也能达到最先进水平的注意力性能。

通过精心的内核设计、大量的微基准测试，以及持久化内核与 CUDA Graph 等系统级优化，Triton 后端在保持跨 GPU 厂商可移植性的同时，达到甚至超越了高度专业化实现的性能。如今，它是 AMD 平台上的默认注意力后端，并以同一份源代码在 NVIDIA 与 Intel 平台上高效运行。

这篇博客概述了 Triton Attention 后端中最重要的优化，全部细节与更多基准测试结果请见我们的相关论文 [The Anatomy of a Triton Attention Kernel (arxiv.org)](https://arxiv.org/abs/2511.11581)。

## 致谢

这项工作由 IBM Research 的 AI 平台团队完成——感谢所有参与者：Burkhard Ringlein、Jan van Lunteren、Chih-Chieh Yang、Sara Kokkila Schumacher、Thomas Parnell、Mudhakar Srivatsa、Raghu Ganti。
