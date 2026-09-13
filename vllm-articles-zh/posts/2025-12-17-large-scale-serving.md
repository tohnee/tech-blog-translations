---
title: "vLLM 大规模服务：借助 Wide-EP 在 H200 上实现 DeepSeek 2.2k tok/s"
title_en: "vLLM Large Scale Serving: DeepSeek @ 2.2k tok/s/H200 with Wide-EP"
source: https://vllm.ai/blog/2025-12-17-large-scale-serving
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM 大规模服务：借助 Wide-EP 在 H200 上实现 DeepSeek 2.2k tok/s

> 原文：[vLLM Large Scale Serving: DeepSeek @ 2.2k tok/s/H200 with Wide-EP](https://vllm.ai/blog/2025-12-17-large-scale-serving) · vLLM 博客

vLLM 团队

[#大规模服务](https://vllm.ai/blog/tags/large-scale-serving)[#性能](https://vllm.ai/blog/tags/performance)

# 引言

在 v0.11.0 中，vLLM V0 引擎的最后一段代码被移除，标志着向改进后的 [V1 引擎](https://blog.vllm.ai/2025/01/27/v1-alpha-release.html)架构的迁移彻底完成。如果没有 vLLM 社区的 1,969 位贡献者——他们在过去一个月（截至 2025 年 12 月 18 日）提交了超过 950 个 commit——这一成就不可能实现。

这些努力已经得到验证：vLLM 入选了 SemiAnalysis 开源 InferenceMax 性能[基准](https://inferencemax.semianalysis.com/)。此外，vLLM 深感自豪的是，Meta、LinkedIn、Red Hat、Mistral 和 HuggingFace 的团队都在生产环境中信任并使用 vLLM。

DeepSeek 风格的分离式服务与稀疏混合专家（MoE）模型部署，依然是高性能 LLM 推理的最先进方案。本文将概述 vLLM 团队为进一步提升吞吐量而构建的关键优化，包括：

- 异步调度
- 双批次重叠（Dual-batch overlap）
- 分离式服务
- CUDA Graph 模式 `FULL_AND_PIECEWISE`
- 默认启用 DeepGEMM
- DeepEP 内核集成
- 专家并行负载均衡
- DeepSeek-R1 的 SiLU 内核

如需更多参考，我们推荐 llm-d、PyTorch、Dynamo 和 Anyscale 团队围绕 vLLM 撰写的这些出色文章：[大规模服务](https://llm-d.ai/blog/llm-d-v0.3-expanded-hardware-faster-perf-and-igw-ga)、[分离式服务](https://pytorch.org/blog/disaggregated-inference-at-scale-with-pytorch-vllm/)、[分布式推理](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/#boosting_inference_performance_on_nvidia_gb200_nvl72_by_30x)与 [wide-EP](https://www.anyscale.com/blog/ray-serve-llm-anyscale-apis-wide-ep-disaggregated-serving-vllm)。

# 结果

最近在采用 Infiniband（配 ConnectX-7 网卡）互联的 Coreweave H200 集群上进行的[社区基准测试](https://llm-d.ai/blog/llm-d-v0.3-expanded-hardware-faster-perf-and-igw-ga#wide-ep-performance)显示，在类生产环境的多节点部署中，每块 H200 GPU 的持续吞吐量达到 2.2k tokens/s。

相比此前基准测试中每 GPU 约 1.5k tokens/s 的结果，这是一个显著提升。这一收益直接来自持续的优化工作，包括内核改进（silu-mul-quant 融合、Cutlass QKV 内核、TP 注意力 bug 修复）以及解码阶段双批次重叠（Dual Batch Overlap, DBO）的实现。

这一性能让运维者可以通过整合工作负载、减少达到目标 QPS 所需的副本数量而立即获益，最终降低每美元 token 成本。

![Prefill Results](https://vllm.ai/blog-assets/figures/2025-12-17-large-scale-serving/prefill_throughput.png)

预填充结果

![Decode Results](https://vllm.ai/blog-assets/figures/2025-12-17-large-scale-serving/decode_throughput.png)

解码结果

# 关键组件

## Wide-EP

部署 DeepSeek-V3 模型家族这类前沿模型进行大规模服务，需要考虑两个关键问题：

- 稀疏专家激活：在 DeepSeek-R1 中，模型 671B 总参数里每次前向传播只有 37B 处于激活状态
- KV 缓存管理：张量并行部署对 DeepSeek 的多头潜在注意力（MLA）注意力架构而言并非最优，因为潜在投影会在各个分片之间重复

专家并行（EP）是一种利用上述特性来最大化有效 KV 缓存的部署模式，vLLM 通过 `--enable-expert-parallel` 标志提供支持。在这种模式下，一组专家在部署的各 rank 之间共享。前向传播过程中，token 会在各 rank 之间路由，由合适的专家处理。

![Wide-EP token routing](https://vllm.ai/blog-assets/figures/2025-12-17-large-scale-serving/wide_ep.gif)

Wide-EP token 路由

Wide-EP 将 EP 与数据并行（DP）结合。数据并行部署可以使用 `mp` 或 `ray` 数据并行后端启动，后者在 Ray 集群内的配置更简单。相对张量并行的优势如下图所示，该图展示了 DeepSeek-V3 在张量并行与专家并行分片策略下每块 GPU 的内存占用。

TP 策略下每块 H200 有 34GB 空闲显存，但对 MLA 模型来说，每个 rank 都必须复制潜在注意力投影。而在 DP 部署中，注意力层被复制，使潜在投影在各 rank 之间相互独立，从而提高整个部署的有效批大小。

![](https://vllm.ai/blog-assets/figures/2025-12-17-large-scale-serving/kv_cache.png)

提高专家并行度会增加 rank 之间的同步开销。为解决这一问题，vLLM 集成了对 [DeepEP](https://github.com/deepseek-ai/DeepEP) 高吞吐与低延迟 all-to-all 内核的支持。此外，vLLM 还支持 Perplexity 的 [MoE 内核](https://github.com/perplexityai/pplx-kernels)以及基于 NCCL 的 AllGather-ReduceScatter all-to-all。关于 vLLM 中可用的 all-to-all 后端，请参阅 vLLM MoE [内核文档](https://docs.vllm.ai/en/latest/design/moe_kernel_features/)。

![vLLM all-to-all backends](https://vllm.ai/blog-assets/figures/2025-12-17-large-scale-serving/a2a_backends.png)

vLLM all-to-all 后端

## 双批次重叠（DBO）

vLLM 将 DeepSeek 的[微批处理策略](https://github.com/deepseek-ai/profile-data)集成为双批次重叠（dual batch overlap, DBO），可通过命令行的 `--enable-dbo` 标志启用。该策略让计算与集合通信重叠，以提高 GPU 利用率。具体而言，vLLM 的实现如下：

1. 先跨 rank 执行一次集合 `all_reduce`，确认微批处理会带来收益，最小阈值可通过 `--dbo-decode-token-threshold` 调节
2. 主线程创建微批次 worker 线程，完成 CUDA Graph 捕获
3. vLLM 模块化的 MoE all-to-all 内核基类协调微批次 worker 的启动，在等待 GPU 工作完成时让出控制权

下面是**未启用** DBO 时 DeepSeek 解码负载的分析轨迹。「MoE Dispatch/Combine」部分显示，尽管计算负载很小，集合通信却占用了超长的时长。

![Before DBO](https://vllm.ai/blog-assets/figures/2025-12-17-large-scale-serving/dbo_before.png)

DBO 之前

下面的轨迹展示了**启用** DBO 后的同一负载。第一个微批次 worker 线程发起并完成 MoE dispatch，然后立即让位给第二个微批次 worker 线程。接着，第二个线程完成自己的 dispatch，并在第一个线程完成时让位回它。最后，第一个 worker 完成自己的 combine，再让位回第二个微批次 worker。

这使得在通信开销较高的部署中 GPU 利用率更高——高专家并行度的部署正是如此。

![After DBO](https://vllm.ai/blog-assets/figures/2025-12-17-large-scale-serving/dbo_after.png)

DBO 之后

## 专家并行负载均衡（EPLB）

MoE 专家层在训练时针对专家间负载均衡进行了优化，但在推理时，真实负载可能导致 token 路由不均衡。关于不同负载间专家负载均衡差异的统计数据，可参见 NVIDIA 关于 MoE 专家路由的[实验结果](https://developer.nvidia.com/blog/applying-mixture-of-experts-in-llm-architectures/#experimental_results)。

在 wide-EP 部署中，这意味着一些 EP rank 可能处于闲置状态，而另一些 rank 则在处理大批量 token。为缓解这一问题，vLLM 实现了 DeepSeek 的[专家并行负载均衡器](https://github.com/deepseek-ai/EPLB)（EPLB）中的分层与全局负载均衡策略。EPLB 由 `--enable-eplb` 命令行标志控制，窗口大小、再均衡间隔、冗余专家和日志选项均可配置。

![EPLB in action](https://vllm.ai/blog-assets/figures/2025-12-17-large-scale-serving/eplb.gif)

EPLB 实际运行效果

实现上，每次 MoE 前向传播都会记录每 token 负载，一个滑动窗口会跨 EP rank 聚合这些统计信息。当达到再均衡间隔时，负载均衡器计算新的逻辑到物理专家映射，并编排一次权重重排（weight shuffle），使新放置无需重启模型即可生效。

## 分离式服务

由 Hao AI Lab 在 2024 年 DistServe [论文](https://hao-ai-lab.github.io/blogs/distserve-retro/)中描述的分离式预填充/解码服务模式，对专家并行部署尤其有用。

![P/D disaggregation in action](https://vllm.ai/blog-assets/figures/2025-12-17-large-scale-serving/disaggregated_serving.gif)

P/D 分离实际运行效果

由于专家分布在各 rank 上，一个请求的 token 起始于某个 rank，却可能需要由 EP 组中任何其他 rank 上的专家处理。这要求 MoE 层之间进行同步（以及在某 rank 未被使用时的空跑 pass），以便层的 combine 集合通信能够在恰当时机接收 token。

这意味着一个计算受限的预填充请求就可能拖延整个 EP 组的前向传播，进一步放大了分离式服务的收益。此外，DeepSeek 部署可以配置为专为其负载使用合适的 DeepEP 内核（高吞吐 vs. 低延迟）。

# 部署路径

## llm-d

llm-d 是一个 Kubernetes 原生的分布式推理服务栈，为任何人在大规模服务大型生成式 AI 模型提供清晰的路径。llm-d 帮助你在大多数硬件加速器与基础设施提供商上，为核心 OSS 模型实现最快的「达到最先进（SOTA）性能的时间」。欲了解更多细节，请查看 llm-d 的 Wide EP [最佳实践路径](https://github.com/llm-d/llm-d/tree/main/guides/wide-ep-lws)，以复现本文的结果。

![](https://vllm.ai/blog-assets/figures/2025-12-17-large-scale-serving/llm-d.png)

## Dynamo

Dynamo 面向 LLM 的高吞吐、低延迟生产部署。KV 感知路由、用于缓存卸载的 KV Block Manager，以及用于动态负载匹配的 Planner 等特性，帮助你在扩展到更多 GPU 的同时满足更严格的 SLA。Dynamo 原生支持 vLLM 与 wide-EP 服务，并包含上述全部特性。欲了解更多细节，请查看 [Dynamo](https://docs.nvidia.com/dynamo/latest/index.html) 以及用于复现本博客性能的[示例配方](https://github.com/ai-dynamo/dynamo/pull/4463/files#diff-363ddf6952864a610a1047f6b99c52461d6de9a4e198f89eb49d34f009a4d22b)。

![](https://vllm.ai/blog-assets/figures/2025-12-17-large-scale-serving/dynamo.png)

## Ray Serve LLM

Ray Serve LLM 构建在 Ray Serve 原语之上，为[预填充/解码分离](https://docs.ray.io/en/latest/serve/llm/architecture/serving-patterns/prefill-decode.html)、[数据并行注意力](https://docs.ray.io/en/latest/serve/llm/architecture/serving-patterns/data-parallel.html)和[前缀缓存亲和请求路由](https://docs.ray.io/en/latest/serve/llm/architecture/routing-policies.html)提供一等公民级的服务模式，注重模块化以及在 Ray 集群（包括 Kubernetes 上的 KubeRay）上部署的便利性。它的一大差异化优势是与更广泛的 Ray 生态无缝集成，包括数据处理和强化学习（RL）。

该框架集成了 NIXL 和 LMCache 连接器以实现高效的 KV 传输，并利用 Ray 的分布式计算原语，根据负载特征对各阶段进行独立的自动扩缩容。二者结合，为推理工作负载提供了一个灵活且可编程的层，可以轻松扩展和组合，实现多样化的服务模式。

![](https://vllm.ai/blog-assets/figures/2025-12-17-large-scale-serving/ray_serve_llm.png)

# 路线图

vLLM 在持续改进中，目前正在进行的工作包括：

- 弹性专家并行
- 长上下文服务
- 经由 CPU 的 KV 缓存传输
- 完全确定性与批次不变性
- 大型 MoE 优化，例如 DeepSeek-R1 与 gpt-oss 模型的算子融合
- 改进 FlashInfer 集成以纳入最新内核，例如 SwapAB
- 在分离式服务部署中支持独立的 TP 大小
- 面向大规模服务的 GB200 优化

如需最新参考，请访问 [roadmap.vllm.ai](http://roadmap.vllm.ai)。

# 总结

- vLLM 已完全迁移至 V1 引擎，在 DeepSeek 风格的 MoE 部署中展现出高吞吐，并通过 wide-EP 实现了 2.2k tok/s/H200。
- Wide-EP 为 MLA 架构最大化 KV 缓存效率，而双批次重叠与 EPLB 降低了通信瓶颈与负载不均衡。
- 分离式预填充/解码进一步优化了 MoE 负载的预填充与解码部署，可选 llm-d、Dynamo 与 Ray Serve LLM 等部署方案。
