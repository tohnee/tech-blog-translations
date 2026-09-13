---
title: "GPT-OSS 在 NVIDIA Blackwell 上的性能优化：推进 Pareto 前沿"
title_en: "GPT-OSS Performance Optimizations on NVIDIA Blackwell: Pushing the Pareto Frontier"
source: https://vllm.ai/blog/2026-02-01-gpt-oss-optimizations
crawled: 2026-09-12
translated: 2026-09-13
---

# GPT-OSS 在 NVIDIA Blackwell 上的性能优化：推进 Pareto 前沿

> 原文：[GPT-OSS Performance Optimizations on NVIDIA Blackwell: Pushing the Pareto Frontier](https://vllm.ai/blog/2026-02-01-gpt-oss-optimizations) · vLLM 博客

作者：vLLM 与 NVIDIA 团队

[#性能](https://vllm.ai/blog/tags/performance)[#硬件](https://vllm.ai/blog/tags/hardware)

**TL;DR：** 在与开源社区的合作中，vLLM + NVIDIA 在运行于 NVIDIA Blackwell GPU 上的 `gpt-oss-120b` 模型上取得了显著的性能里程碑。通过与 FlashInfer 的深度集成、借助 `torch.compile` 实现的新型内核融合，以及多种推理运行时特性，我们刷新了该模型性能 Pareto 前沿的纪录——同时优化了最大吞吐量（+38%）与最佳交互性（+13%）。

本文详细介绍这一工程历程、技术突破以及复现结果的说明。持续基准测试数据也可在 **[SemiAnalysis Inference MAX](https://inferencemax.semianalysis.com/) 与 [vLLM Recipes](https://docs.vllm.ai/projects/recipes/en/latest/OpenAI/GPT-OSS.html)** 上查看。

## 目录

- [引言](#introduction)
- [FlashInfer + torch.compile](#fi-tc)
- [运行时改进](#runtime)
- [部署配置](#recipes)
- [结果](#results)
- [后续步骤](#next-steps)
- [致谢](#acknowledgements)

---

## 引言

只针对单一指标进行优化——比如最大吞吐量或单批延迟——往往不足以满足真实世界的部署需求。不同用例需要不同的延迟约束与请求并发度。因此，真正的挑战在于优化 **Pareto 前沿**：这条曲线代表了 **每 GPU 每秒 token 数（TPS）**（对应 TCO，总拥有成本）与 **每用户 TPS**（对应交互性）之间最优的权衡。把这条曲线向上、向右推进，意味着在为单个用户提供更快生成的同时，让更多用户共享硬件。[SemiAnalysis InferenceMAX](https://inferencemax.semianalysis.com/) 已经指明了这一关键需求：在现代 GPU 上测量、报告并改进此类 LLM 推理工作负载的性能数据。

关键用例之一是服务 OpenAI 的 `gpt-oss-120b` 模型——一个原生 4 比特量化（MXFP4）的混合专家（MoE）LLM。它在同规模模型中达到了 SOTA 精度，并具备强大的智能体能力。在最近的 SemiAnalysis InferenceMAX 展示中，vLLM 证明了其在 NVIDIA 最新的 Blackwell（B200/GB200）架构上高效处理这一工作负载的能力。

这些优化的核心是软硬件协同设计。NVIDIA B200/GB200 GPU 引入了诸如原生 FP4 Tensor Core 与每 GPU 192GB HBM 等强大特性，这对服务 `gpt-oss` 这样的大型 MoE 模型至关重要。为了充分发挥这一硬件的能力，vLLM 与 NVIDIA 团队与 **FlashInfer** 进行了集成，并采取了聚焦内核融合、降低通信开销和主机-设备重叠的严格优化策略。

## FlashInfer 集成与基于 torch.compile 的融合

为最大限度地利用 Blackwell 的 Tensor Core，vLLM 使用 **FlashInfer** 作为注意力、MoE 及其他计算密集型和融合操作的主要内核后端。

**1. 关键计算内核集成**：

- **MoE 后端：** 我们在 FlashInfer 中为 MoE 操作同时启用了 `trtllm-gen` [(PR23819)](https://github.com/vllm-project/vllm/pull/23819) 与 `cutlass` [(PR23696)](https://github.com/vllm-project/vllm/pull/23696) 两个后端。这使 vLLM 能够为专家路由与计算选择性能最佳的内核。除了为 LLM 提供性能最佳的内核外，FlashInfer 还包含即时编译（jit-in-time compilation）、自动调优与内核缓存，这极大改善了任何有高性能内核需求的开发者的使用体验。
- **FP8 KV 缓存：** 以 FP8 精度存储 KV 缓存，使引擎能够在相同的 KV 缓存预算下服务更多并发请求。此外，以 FP8 精度执行部分注意力操作还能降低注意力运算的计算/内存复杂度。为在这一用例中获得最佳性能，vLLM 集成了 [PR25674 中 FlashInfer 优化的注意力内核](https://github.com/vllm-project/vllm/pull/25674/)。

**2. 通过 torch.compile 实现图融合** 我们的优化工作有相当一部分聚焦于内核融合，以减少内存访问与内核启动开销。vLLM 没有采用硬编码的融合优化，而是基于 `torch.compile` 构建了一套[完善的基础设施](https://github.com/vllm-project/vllm/tree/main/vllm/compilation)来自动执行内核融合。这一做法不仅提升了性能，还显著降低了启用、泛化和维护此类改进的工作量。

- **AR + Norm 融合：** 我们实现了 AllReduce（AR）与 RMSNorm 操作的融合。这对张量并行（TP）部署尤为重要，因为在这类部署中通信开销可能成为瓶颈，详情请见 [PR20691](https://github.com/vllm-project/vllm/pull/20691)。
- **Pad + Quant 与 Finalize + Slice：** 我们正在积极推出针对填充/量化与 finalize/slice 操作的[融合 pass（PR30647）](https://github.com/vllm-project/vllm/pull/30647)，以进一步精简 MoE 执行路径，预期带来 6% 的性能提升。

随着我们识别并开发新的融合操作，团队将继续通过这一基础设施带来自动化的性能提升。

## 运行时改进

在 Blackwell 这样的新一代硬件上，GPU 速度极快，以至于 CPU（主机）常常成为瓶颈，难以足够快地派发内核以保持 GPU 忙碌。此外，`prepare\_batch`、请求调度与采样逻辑也需要大量的 CPU 侧处理。这种“主机开销”表现为内核执行之间的空隙，降低性能与整体 GPU 利用率。

为解决这一问题，我们在 vLLM 中实现了 **异步调度（Async Scheduling）** 与 **流间隔（Stream Interval）**，有效消除主机侧开销。

[异步调度（Async Scheduling）](https://github.com/vllm-project/vllm/pull/23569)：

- **机制：** 该调度器将 CPU 的请求调度与 GPU 的执行解耦。通过让 CPU 在 GPU 仍在处理当前批次时准备下一批请求，我们有效地隐藏了主机开销。
- **影响：** 这一优化对 `gpt-oss` 模型至关重要，在高吞吐与最低延迟两种场景中皆是如此。在性能更强的 GPU（H200、B200、GB200）上，可以获得约 10% 的性能提升。
- **配置：** 在近期的 vLLM 版本中已默认开启。

[流间隔（Stream Interval）](https://github.com/vllm-project/vllm/pull/27869)：

- **机制：** 该特性通过在将生成的 token 发送给客户端之前先进行缓冲，来降低网络响应的粒度。引擎不再为每一个 token 触发一次网络调用，而是等到达到指定的缓冲大小（即“间隔”）后再发送。关键在于，该实现通过确保**第一个 token 始终立即发送**（保持 TTFT 处于低位）来保持响应性，后续 token 则被批量发送。
- **影响：** 通过降低 HTTP/gRPC 响应派发的频率，这显著降低了与网络 I/O 和序列化相关的 CPU 开销。在高并发基准测试中（例如 `gpt-oss-20b` 配 1024 个并发请求），这一优化缓解了输出队列瓶颈，带来 **57% 的端到端性能提升**，并改善了每输出 token 时间（TPOT）。
- **配置：** 用户可以通过 `--stream-interval <num_tokens>` 参数配置这一行为。默认值为 `1`（标准流式），但增大该值（例如设为 `10`）对于降低高吞吐部署中的主机开销非常有效。

## 部署配置

大多数优化已在最新的 vLLM 版本中默认生效。此外，要在 Blackwell GPU（B200/GB200）上复现 `gpt-oss` 的优化性能，我们建议在你的 vLLM 部署配置中使用以下设置。这些内容也可以在 [vLLM Recipes 页面](https://docs.vllm.ai/projects/recipes/en/latest/OpenAI/GPT-OSS.html)找到。

**推荐的配置标志：**

- **图捕获（Graph Capture）：**
  - `--cuda-graph-capture-size 2048`
- **调度：**
  - `--api-server-count 20` 或 `--stream-interval 20`：这有助于将 HTTP API 服务器开销与推理引擎解耦，在高并发下稳定性能。
- **MoE 后端：**
  - 显式启用针对 FP8/FP4 MoE 优化的 Cutlass 后端以确保最大吞吐量：`VLLM_USE_FLASHINFER_MOE_MXFP4_MXFP8=1`。

## 结果

这些优化叠加的总体效果，使自 [InferenceMax](https://blog.vllm.ai/2025/10/09/blackwell-inferencemax.html) 发布以来性能显著上升。值得注意的是，最大吞吐量下性能提升 38%，最低延迟下性能提升 13%

![](https://vllm.ai/blog-assets/figures/blackwell-inferencemax/gpt-oss-120b-8k-1k-nov-jan.png)

这些改进不仅针对单一用例，而是**覆盖整条 Pareto 曲线，惠及整个 vLLM 社区**。

## 后续步骤

我们在 `gpt-oss` 上的工作仍在继续。以下是目前正在推进、以进一步拓展 Pareto 前沿的工程方向。该清单也可在 [Issue 30758](https://github.com/vllm-project/vllm/issues/30758) 中找到。

### 分离部署

通过把预填充阶段与解码阶段分离到不同 GPU 上，我们有望获得更高的单 GPU 吞吐量。我们目前正在试验这一部署方式，寻找能带来更优性能的正确配置。

### 数据+专家并行性能

我们的预测显示，在相同延迟（TPS/user）下，使用 DEP2（2 GPU 上的注意力 DP + MoE EP）有望比 TP1 和 TP2 实现更高的单 GPU 吞吐量。但目前 DEP2 的性能劣于 TP1/TP2，主要原因是 MoE 内核选择问题。我们正在积极解决这一问题。

### 最低延迟性能

我们已经确定了针对最低延迟场景的若干性能优化机会，更具体地说是 TP8 并发 8 的场景：

- RoPE+Q+Cache 融合：内核已在 FlashInfer 中可用，vLLM 中的集成正在进行。
- router GEMM 与 fc\_qkv/fc\_o\_proj GEMM：我们可以使用性能更好且支持 PDL 的专用小型 GEMM 内核。

## 致谢

我们要感谢 vLLM 社区中众多共同参与这项工作的优秀人才：

- Red Hat：Michael Goin, Alexander Matveev, Lucas Wilkinson, Luka Govedič, Wentao Ye, Ilia Markov, Matt Bonanni, Varun Sundar Rabindranath, Bill Nell, Tyler Michael Smith, Robert Shaw
- NVIDIA：Po-Han Huang, Pavani Majety, Shu Wang, Elvis Chen, Zihao Ye, Duncan Moss, Kaixi Hou, Siyuan Fu, Benjamin Chislett, Xin Li, Vadim Gimpelson, Minseok Lee, Amir Samani, Elfie Guo, Lee Nau, Kushan Ahmadian, Grace Ho, Pen Chun Li
- vLLM：Chen Zhang, Yongye Zhu, Bowen Wang, Kaichao You, Simon Mo, Woosuk Kwon, Zhuohan Li
- Meta：Yang Chen, Xiaozhu Meng, Boyuan Feng, Lu Fang
