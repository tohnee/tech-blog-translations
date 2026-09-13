---
title: "vLLM V1：vLLM 核心架构的重大升级"
title_en: "vLLM V1: A Major Upgrade to vLLM's Core Architecture"
source: https://vllm.ai/blog/2025-01-27-v1-alpha-release
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM V1：vLLM 核心架构的重大升级

> 原文：[vLLM V1: A Major Upgrade to vLLM's Core Architecture](https://vllm.ai/blog/2025-01-27-v1-alpha-release) · vLLM 博客

作者：vLLM 团队

[#性能](https://vllm.ai/blog/tags/performance)

![](https://vllm.ai/blog-assets/figures/v1/vLLM_V1_Logo.png)

我们非常高兴地宣布 **vLLM V1 alpha 版正式发布**，这是对 vLLM 核心架构的一次重大升级。基于 vLLM 开发 1.5 年来积累的经验教训，我们重新审视了关键设计决策，整合了各类特性，并简化了代码库，以增强灵活性与可扩展性。V1 已经实现了**最先进水平（SOTA）的性能**，并且还将获得更多优化。最棒的是，用户可以无缝启用 V1——只需设置 `VLLM_USE_V1=1` 环境变量，**无需对现有 API 做任何改动**。在未来几周的测试与反馈收集之后，我们计划将 V1 过渡为默认引擎。

# 为什么需要 vLLM V1？

## 从 vLLM V0 中学习

在过去 1.5 年里，vLLM 在支持多样的模型、特性和硬件后端方面取得了显著成功。然而，在社区横向扩张的同时，我们在让系统保持简洁、以及在整个技术栈中纵向整合各类优化方面遇到了挑战。各项特性往往是独立开发的，导致难以干净利落地将它们有效组合。随着时间的推移，技术债不断累积，促使我们重新审视基础设计。

## V1 的目标

基于上述动机，vLLM V1 的设计目标是：

- 提供**简单、模块化、易于改造的代码库**。
- 以近乎为零的 CPU 开销确保**高性能**。
- 将**关键优化整合**到统一架构中。
- 通过默认启用特性/优化，实现**零配置**。

## V1 的范围

vLLM V1 对其核心组件进行了全面的重新架构，包括调度器、KV 缓存管理器、worker、采样器和 API 服务器。不过，它仍与 vLLM V0 共享大量代码，例如模型实现、GPU 内核、分布式控制面和各种工具函数。这种做法让 V1 既能复用 V0 建立的广泛覆盖面与稳定性，又能显著提升性能并降低代码复杂度。

# vLLM V1 有哪些新变化？

## 1. 优化的执行循环与 API 服务器

![](https://vllm.ai/blog-assets/figures/v1/v1_server_architecture.png)

作为一个功能完备的连续批处理引擎和 OpenAI 兼容 API 服务器，vLLM 的核心执行循环依赖 CPU 操作来管理模型前向传播之间的请求状态。随着 GPU 越来越快、模型执行时间大幅缩短，运行 API 服务器、调度任务、准备输入、反解析（de-tokenize）输出以及向用户流式返回响应等任务的 CPU 开销变得愈发明显。这个问题在 NVIDIA H100 GPU 上运行 Llama-8B 这类较小模型时尤其突出，因为此时 GPU 上的执行时间低至约 5ms。

在 [v0.6.0 版本](https://blog.vllm.ai/2024/09/05/perf-update.html)中，vLLM 引入了使用 ZeroMQ 作为 IPC 的多进程 API 服务器，实现了 API 服务器与 AsyncLLM 之间的重叠执行。vLLM V1 更进一步，将多进程架构更深入地整合到 AsyncLLM 的核心之中，创建了一个隔离的 `EngineCore` 执行循环，专注于调度器和模型执行器。这一设计使 CPU 密集型任务——例如分词、多模态输入处理、反解析和请求流式输出——能够与核心执行循环有更大程度的重叠，从而最大化模型吞吐量。

## 2. 简洁而灵活的调度器

![](https://vllm.ai/blog-assets/figures/v1/v1_scheduling.png)

vLLM V1 引入了一个简单而灵活的调度器。它取消了传统上"预填充"与"解码"阶段的区分，将用户给定的提示 token 和模型生成的输出 token 统一处理。调度决策被表示为一个简单的字典，例如 `{request_id: num_tokens}`，用于指定每一步中每个请求要处理的 token 数量。我们发现这种表示具有足够的通用性，可以支持分块预填充、前缀缓存和投机解码等特性。例如，分块预填充调度得以无缝实现：在固定的 token 预算内，调度器动态决定为每个请求分配多少 token（如上图所示）。

## 3. 零开销的前缀缓存

vLLM V1 与 V0 一样，使用基于哈希的前缀缓存和基于 LRU 的缓存淘汰。在 V0 中，启用前缀缓存有时会带来显著的 CPU 开销，当缓存命中率较低时甚至会导致性能明显下降，因此它默认是关闭的。在 V1 中，我们优化了数据结构以实现常数时间的缓存淘汰，并仔细地将 Python 对象创建的开销降到最低。这使得 V1 的前缀缓存即使缓存命中率为 0% 时也几乎不带来性能损失。

![](https://vllm.ai/blog-assets/figures/v1/v1_prefix_caching.png)

以下是一些基准测试结果。在我们的实验中，我们观察到即使缓存命中率为 0%，V1 的前缀缓存带来的吞吐量下降也不足 1%，而在缓存命中率较高时，它可以将性能提升数倍。**得益于近乎为零的开销，我们现在在 V1 中默认启用前缀缓存。**

## 4. 张量并行推理的整洁架构

![](https://vllm.ai/blog-assets/figures/v1/v1_tp_architecture.png)

vLLM V1 为张量并行推理引入了一个整洁而高效的架构，有效解决了 V0 的局限。在 V0 中，调度器和 Worker 0 被放置在同一个进程中，以减少向 worker 广播输入数据时的进程间通信开销。然而，这种设计引入了不对称的架构，增加了复杂度。V1 通过在 worker 侧缓存请求状态、每步只传输增量更新（diffs）来克服这一问题。这一优化将进程间通信降到最低，使调度器和 Worker 0 可以运行在各自的进程中，形成整洁、对称的架构。此外，V1 抽象掉了大部分分布式逻辑，使 worker 在单 GPU 和多 GPU 配置下都能以相同方式运行。

## 5. 高效的输入准备

![](https://vllm.ai/blog-assets/figures/v1/persistent_batch.png)

在 vLLM V0 中，模型的输入张量和元数据在每一步都会被重新创建，这通常带来可观的 CPU 开销。为优化这一点，V1 实现了[持久批处理（Persistent Batch）](https://github.com/InternLM/lmdeploy)技术，缓存输入张量并在每一步只对其应用增量更新。此外，V1 大量使用 Numpy 操作而非 Python 原生操作，将更新张量时的 CPU 开销降到最低。

## 6. torch.compile 与分段 CUDA Graph

![](https://vllm.ai/blog-assets/figures/v1/torch_compile_cuda_graph.png)

V1 利用 vLLM 的 `torch.compile` 集成来自动优化模型。这使 V1 能够高效支持各种模型，同时将编写自定义内核的需求降到最低。此外，V1 引入了*分段 CUDA Graph（piecewise CUDA graphs）*来缓解 CUDA Graph 的局限。我们正在准备关于 torch.compile 集成和分段 CUDA Graph 的专门博客文章，**敬请期待更多更新**！

## 7. 增强的多模态 LLM 支持

vLLM V1 将多模态大语言模型（MLLM）视为一等公民，并在其支持方面引入了几项关键改进。

首先，V1 将多模态输入预处理移入非阻塞进程，从而优化了多模态输入的预处理。例如，图像文件（如 JPG 或 PNG）在输入模型之前必须转换为像素值张量，并进行裁剪和变换。这种预处理可能消耗大量 CPU 周期，可能导致 GPU 闲置。为解决这一问题，V1 将预处理任务卸载到单独的进程中，避免其阻塞 GPU worker，并增加了预处理缓存，使处理后的输入可以在共享相同多模态输入的请求之间复用。

其次，V1 为多模态输入引入了前缀缓存。除了 token ID 的哈希之外，还使用图像哈希来识别图像输入对应的 KV 缓存。这一改进对包含图像输入的多轮对话尤其有益。

第三，V1 通过"编码器缓存"为 MLLM 启用了分块预填充调度。在 V0 中，图像输入和文本输入必须在同一步中处理，因为 LLM 解码器的 ![]() token 依赖视觉嵌入（vision embeddings），而后者在该步结束后即被丢弃。借助编码器缓存，V1 可以临时保存视觉嵌入，使调度器能够将文本输入拆分为多个块、跨多步处理，而无需每步重新生成视觉嵌入。

## 8. FlashAttention 3

vLLM V1 拼图的最后一块是集成 [FlashAttention 3](https://arxiv.org/abs/2407.08608)。鉴于 V1 的高度动态性——例如在同一批次中混合预填充与解码——一个灵活且高性能的注意力内核必不可少。FlashAttention 3 有效地满足了这一需求，在为广泛特性提供稳健支持的同时，在多种使用场景中保持了出色的性能。

# 性能

得益于大量的架构增强，vLLM V1 实现了最先进的吞吐量与延迟，相比 V0（*未启用多步调度*）吞吐量提升高达 **1.7x**。
这些显著的性能提升源于整个技术栈中全面的 CPU 开销削减。
对于 Qwen2-VL 这类视觉语言模型（VLM），得益于 V1 对 VLM 的增强支持，改进更加明显。

- **文本模型：Llama 3.1 8B 与 Llama 3.3 70B**

![](https://vllm.ai/blog-assets/figures/v1/v1_llama.png)

我们使用 ShareGPT 数据集测量了 vLLM V0 和 V1 在 Llama 3.1 8B 和 Llama 3.3 70B 模型上的性能。
得益于更高的吞吐量，V1 的延迟始终低于 V0，尤其在高 QPS 下表现明显。
鉴于 V0 与 V1 所使用的内核几乎相同，性能差异主要来自 V1 的架构改进（更少的 CPU 开销）。

- **视觉语言模型：Qwen2-VL**

![](https://vllm.ai/blog-assets/figures/v1/v1_qwen2vl.png)

我们使用 [VisionArena](https://arxiv.org/abs/2412.08687) 数据集测试 Qwen2-VL，评估了 VLM 上的性能。
得益于改进的 VLM 支持，V1 相比 V0 带来了更大的加速，这主要来自两项关键改进：将输入处理卸载到单独的进程，以及为多模态查询实现更灵活的调度。
我们还想指出，V1 现已原生支持多模态模型的前缀缓存，但在此略去相关基准测试结果。

- **展望未来**

虽然这些改进已经相当可观，但我们认为这只是开始。
重新设计的架构为快速开发新特性奠定了坚实基础。
我们期待在未来几周分享更多增强功能。
敬请期待更多更新！

# 局限性与后续工作

虽然 vLLM V1 的结果令人鼓舞，但它仍处于 alpha 阶段，缺少 V0 的一些特性。以下是一些说明：

**模型支持：**
V1 支持 Llama 等仅解码器（decoder-only）Transformer、Mixtral 等混合专家（MoE）模型，以及 Qwen2-VL 等若干 VLM。所有量化方法均已支持。不过，V1 目前不支持多模态 Llama 3.2 这类编码器-解码器架构、Jamba 这类基于 Mamba 的模型，以及嵌入模型。请查看[我们的文档](https://docs.vllm.ai/en/latest/models/supported_models.html)获取更详细的受支持模型列表。

**特性限制：**
V1 目前不支持 logprobs、prompt logprobs 采样参数、流水线并行、结构化解码、投机解码、Prometheus 指标和 LoRA。我们正在积极缩小这一特性差距，并为 V1 引擎添加全新优化。

**硬件支持：**
V1 目前仅支持 Ampere 及之后的 NVIDIA GPU。我们正在积极扩展对 TPU 等其他硬件后端的支持。

最后请注意，只要不设置 `VLLM_USE_V1=1`，你就可以继续使用 V0 并保持向后兼容。

# 如何开始使用

要使用 vLLM V1：

1. 使用 `pip install vllm --upgrade` 安装最新版本的 vLLM。
2. **设置环境变量 `export VLLM_USE_V1=1`。**
3. 使用 vLLM 的 [Python API](https://github.com/vllm-project/vllm/blob/main/examples/offline_inference/basic.py) 或 OpenAI 兼容服务器（`vllm serve <model-name>`）。你无需对现有 API 做任何改动。

请试用并分享你的反馈！

# 致谢

我们谨此致谢：vLLM V1 的设计借鉴并增强了多个开源 LLM 推理引擎，包括 [LightLLM](https://github.com/ModelTC/lightllm)、[LMDeploy](https://github.com/InternLM/lmdeploy)、[SGLang](https://github.com/sgl-project/sglang)、[TGI](https://github.com/huggingface/text-generation-inference) 和 [TRT-LLM](https://github.com/NVIDIA/TensorRT-LLM)。这些引擎对我们的工作产生了深远影响，我们从中学到了宝贵的经验。

V1 的重新架构是整个 vLLM 团队与社区持续共同努力的成果。以下是促成这一里程碑的贡献者（不完全）名单：

- UC Berkeley、Neural Magic（现为 Red Hat）、Anyscale 和 Roblox 共同主导了这项工作。
- [Woosuk Kwon](https://github.com/WoosukKwon) 发起了该项目，并实现了调度器和模型执行器（model runner）。
- [Robert Shaw](https://github.com/robertgshaw2-redhat) 实现了优化的执行循环与 API 服务器。
- [Cody Yu](https://github.com/comaniac) 为文本和图像输入实现了高效的前缀缓存。
- [Roger Wang](https://github.com/ywang96) 领导了 V1 中整体增强的 MLLM 支持。
- [Kaichao You](https://github.com/youkaichao) 领导了 torch.compile 集成，并实现了分段 CUDA Graph。
- [Tyler Michael Smith](https://github.com/tlrmchlsmth) 使用 Python 多进程实现了张量并行支持。
- [Rui Qiao](https://github.com/ruisearch42) 使用 Ray 实现了张量并行支持，目前正在进行流水线并行支持的实现。
- [Lucas Wilkinson](https://github.com/LucasWilkinson) 添加了对 FlashAttention 3 的支持。
- [Alexander Matveev](https://github.com/alexm-redhat) 实现了针对多模态输入的优化预处理器，目前正在进行 TPU 支持的实现。
- [Sourashis Roy](https://github.com/sroy745) 在采样器中实现了 logit 惩罚。
- [Cyrus Leung](https://github.com/DarkLight1337) 领导了 MLLM 输入处理的重构工作，并帮助将其集成到 V1。
- [Russell Bryant](https://github.com/russellb) 解决了多个与多进程相关的问题。
- [Nick Hill](https://github.com/njhill) 优化了引擎循环与 API 服务器。
- [Ricky Xu](https://github.com/rickyyx) 和 [Chen Zhang](https://github.com/heheda12345) 协助重构了 KV 缓存管理器。
- [Jie Li](https://github.com/jeejeelee) 和 [Michael Goin](https://github.com/mgoin) 协助了 MLLM 的支持与优化。
- [Aaron Pham](https://github.com/aarnphm) 正在实现结构化解码支持。
- [Varun Sundar Rabindranath](https://github.com/varun-sundar-rabindranath) 正在实现多 LoRA 支持。
- [Andrew Feldman](https://github.com/afeldman-nm) 正在实现 logprobs 与 prompt logprobs 支持。
- [Lily Liu](https://github.com/LiuXiaoxuanPKU) 正在实现投机解码支持。
- [Kuntai Du](https://github.com/KuntaiDu) 正在实现预填充分离与 KV 缓存传输支持。
- [Simon Mo](https://github.com/simon-mo) 和 [Zhuohan Li](https://github.com/zhuohan123) 为 V1 系统设计做出了贡献。
