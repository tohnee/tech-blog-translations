---
title: "使用 vLLM 进行分布式推理"
title_en: "Distributed Inference with vLLM"
source: https://vllm.ai/blog/2025-02-17-distributed-inference
crawled: 2026-09-12
translated: 2026-09-13
---

# 使用 vLLM 进行分布式推理

> 原文：[Distributed Inference with vLLM](https://vllm.ai/blog/2025-02-17-distributed-inference) · vLLM 博客

作者：vLLM 团队

[#大规模服务](https://vllm.ai/blog/tags/large-scale-serving)

### 动机

服务大模型常常带来内存瓶颈，例如令人头疼的 **CUDA out of memory**（显存不足）错误。为解决这一问题，主要有两种方案：

1. **降低精度**——使用 FP8 及更低比特的量化方法可以减少内存使用。然而，这种方式可能影响精度和可扩展性，而且当模型规模超过数千亿参数时，仅靠它是不够的。
2. **分布式推理**——将模型计算分散到多个 GPU 或节点上，可实现可扩展性与效率。这正是张量并行和流水线并行等分布式架构发挥作用的地方。

### vLLM 架构与大语言模型推理的挑战

与训练相比，LLM 推理带来了独特的挑战：

- 训练专注于吞吐量且形状已知且静态，而推理不同，它要求低延迟并需要处理动态工作负载。
- 推理工作负载必须高效管理 KV 缓存、投机解码以及从预填充到解码的转换。
- 大模型常常**超出单张 GPU 的容量**，需要先进的**并行化策略**。

为解决这些问题，vLLM 提供了：

- **张量并行**：将模型的每一层切分到节点内的多个 GPU 上。
- **流水线并行**：将模型中连续的若干层分布到多个节点上。
- **优化的通信内核与控制面架构**，以最小化 CPU 开销并最大化 GPU 利用率。

## vLLM 中的 GPU 并行技术

### 张量并行

#### 问题：模型超出单张 GPU 的容量

随着模型不断变大，单张 GPU 无法容纳它们，因此需要多 GPU 策略。张量并行**将模型权重切分到多个 GPU 上**，实现并发计算，从而降低延迟并增强可扩展性。

这一方法最初为训练而开发（[Megatron-LM（Shoeybi et al., 2019）](https://arxiv.org/abs/1909.08053)），vLLM 对其进行了适配与优化，以用于推理工作负载。

![](https://vllm.ai/blog-assets/figures/distributed-inference/tp_strategies.png)

张量并行依赖两种主要技术：

1. 列并行：沿列切分权重矩阵，在计算完成后拼接结果。
2. 行并行：沿行切分矩阵，在计算完成后对各部分结果求和。

![](https://vllm.ai/blog-assets/figures/distributed-inference/column_row_parallel.png)

举一个具体例子，我们来看看这种并行方式如何作用于 Llama 模型中的 MLP（多层感知机）层：

- 列并行作用于上投影（up-projection）操作。
- 逐元素激活函数（如 SILU）在切分后的输出上运算。
- 行并行用于下投影（down-projection），并通过 **all-reduce** 操作聚合最终结果。

张量并行确保推理计算分布在多个 GPU 上，充分利用可用的内存带宽和算力。使用张量并行时，我们可以通过有效倍增内存带宽来改善延迟。这是因为切分模型权重使多个 GPU 能够并行访问内存，减少了单张 GPU 可能遇到的瓶颈。

![](https://vllm.ai/blog-assets/figures/distributed-inference/tensor_parallelism.png)

来源：[Sebastian Raschka, 2023](https://sebastianraschka.com/blog/2023/pytorch-memory-optimization.html)。

不过，张量并行要求每张 GPU 之间具备**高带宽互连**，如 NVLink 或 InfiniBand，以尽量降低通信开销增加带来的影响。

### 流水线并行

#### 问题：模型超出多 GPU 的容量

对于超大模型（如 DeepSeek R1、Llama 3.1 405B），单个节点可能不够用。流水线并行**将模型切分到多个节点上**，每个节点处理特定的连续模型层。

#### 工作原理

- 每张 GPU 加载并处理一组不同的层。
- **发送/接收操作：** 随着计算推进，中间激活值在 GPU 之间传输。

**与张量并行相比，这带来更低的通信开销**，因为数据传输在每个流水线阶段只发生一次。

流水线并行降低了各 GPU 的内存压力，但并不像张量并行那样天然缩短推理延迟。为缓解吞吐量上的低效，vLLM 引入了**先进的流水线调度**，通过优化微批次（micro-batch）执行来确保所有 GPU 保持活跃。

### 组合张量并行与流水线并行

一般而言，可以这样考虑并行的应用方式：

- 当互连较慢时，**节点间使用流水线并行，节点内使用张量并行**。
- 如果互连高效（如 NVLink、InfiniBand），**张量并行可以扩展到节点之间**。
- 明智地组合这两种技术可以**减少不必要的通信开销**并最大化 GPU 利用率。

#### 性能扩展与内存效应

虽然并行化的基本原理意味着线性扩展，但实际上，由于内存效应，**性能提升可能是超线性的**。无论使用张量并行还是流水线并行，由于可用于 KV 缓存的内存呈超线性增长，吞吐量的提升可能以不那么直观的方式出现。

![](https://vllm.ai/blog-assets/figures/distributed-inference/kv_cache_effects.png)

这种超线性扩展效应之所以发生，是因为更大的缓存允许更大的批大小，从而并行处理更多请求，并获得更好的内存局部性，使 GPU 利用率的提升超出单纯增加算力资源所能带来的预期。在上图中可以看到，从 TP=1 到 TP=2，KV 缓存块的数量增加了 13.9x，这使我们能够观察到 **3.9x 的 token 吞吐量提升**——远超我们用 2 张 GPU 替代 1 张 GPU 时预期的线性 2x。

### 延伸阅读

有兴趣深入了解影响 vLLM 设计的技术与系统的读者，可以参考：

- [Megatron-LM（Shoeybi et al., 2019）](https://arxiv.org/abs/1909.08053)介绍了大语言模型中模型并行的基础技术
- [Orca（Yu et al., 2022）](https://www.usenix.org/conference/osdi22/presentation/yu)提出了使用迭代级调度的另一种分布式服务方案
- [DeepSpeed](https://github.com/deepspeedai/DeepSpeed) 与 [FasterTransformer](https://github.com/NVIDIA/FasterTransformer) 为优化 Transformer 推理提供了互补的视角

### 结论

高效服务大模型需要**张量并行**、**流水线并行**以及**分块预填充（Chunked Prefill）**等性能优化的组合。vLLM 通过运用这些技术实现可扩展的推理，同时确保在不同硬件加速器上的适应性。在我们持续增强 vLLM 的过程中，关注**混合专家（MoE）的专家并行**和**更广泛的量化支持**等新进展，对于优化 AI 工作负载将至关重要。

##### 欢迎参加双周 Office Hours，进一步了解 LLM 推理优化与 vLLM！

### 致谢

感谢 Sangbin Cho（xAI）制作了部分图表。
