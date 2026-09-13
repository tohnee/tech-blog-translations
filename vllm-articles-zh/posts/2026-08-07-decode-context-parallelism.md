---
title: "面向长上下文工作负载的 vLLM 高效解码上下文并行"
title_en: "Efficient Decode Context Parallelism with vLLM for Long Context Workloads"
source: https://vllm.ai/blog/2026-08-07-decode-context-parallelism
crawled: 2026-09-12
translated: 2026-09-13
---

# 面向长上下文工作负载的 vLLM 高效解码上下文并行

> 原文：[Efficient Decode Context Parallelism with vLLM for Long Context Workloads](https://vllm.ai/blog/2026-08-07-decode-context-parallelism) · vLLM 博客

作者：Seonghee Lee、Sungsoo Ha、Omri Almog（NVIDIA）、Lucas Wilkinson（Red Hat AI）

[#性能](https://vllm.ai/blog/tags/performance)[#注意力](https://vllm.ai/blog/tags/attention)[#并行](https://vllm.ai/blog/tags/parallelism)

## 1. 引言

长上下文推理对智能体 AI 正变得不可或缺：助手可能需要对大型代码仓库和冗长的聊天历史进行推理。智能体轨迹基准测试如今从 64K 一直延伸到 1M token，其 KV 缓存也相应巨大。在基线张量并行（TP）配置下，KV 缓存按注意力头划分，这为其能缩小到什么程度设下了硬性下限。

现代模型使用两种注意力方案之一，而两者都会撞上这个下限。分组查询注意力（GQA）模型存储少量 KV 头，TP 只能把 KV 缓存切分到每 GPU 一个头；一旦 TP 超过 KV 头的数量，缓存就开始在 GPU 间复制。多头潜在注意力（MLA）模型让情况更糟：MLA 把 Key/Value 压缩成单个低秩 *潜在*向量，由所有查询头共享，因此它实际上只有一个 KV 头。在常规 TP 下没有头可切，意味着潜在 KV 缓存会在 *每个* TP rank 上完整复制一份。在这两种情况下，被复制的 KV 缓存都会侵占 GPU 内存，几乎没有余量去服务更多请求。这限制了系统可处理的并发请求数，拉低吞吐并推高每 token 成本。

解码上下文并行（Decode Context Parallelism，DCP）通过把 KV 缓存切分到多块 GPU 上来解决这一问题，使每块 GPU 只存储和读取 KV 缓存的一部分。这释放了 GPU 内存，让每块 GPU 能承接更多请求，从而以更大的批大小运行。在具有高带宽 GPU 间互连的系统上，这有助于在同时服务大量长上下文智能体时保持交互响应能力。

vLLM 支持 DCP 已近一年，但我们现在写这篇博客来突出该特性以及我们近期对它的改进与进展，因为长上下文智能体用例的兴起使其收益比以往任何时候都更加相关。

![](https://vllm.ai/blog-assets/figures/2026-07-27-decode-context-parallelism/kv-parallelism-overview.svg)

## 2. 性能结果

为了量化解码上下文并行的收益，我们在完全相同的一组 GPU 上比较基线张量并行部署与 DCP，保持模型、硬件与工作负载不变，只改变解码期间 KV 缓存的分片方式。

![](https://vllm.ai/blog-assets/figures/2026-07-27-decode-context-parallelism/figure-1.png)
![](https://vllm.ai/blog-assets/figures/2026-07-27-decode-context-parallelism/figure-2.png)

### 2.1 数据集

数据集是一个公开的智能体长上下文轨迹，采用 Mooncake trace 格式，[发布于此](https://github.com/ai-dynamo/dynamo/blob/main/recipes/kimi-k2.6/perf/traces/64k_400_90kv_agent_new_noschedule_short_15perc.jsonl)。数据集的更多细节见[这一节](https://github.com/ai-dynamo/dynamo/blob/main/recipes/kimi-k2.6/perf/README.md#dataset)。它以 JSONL 提供，每行是一个包含 `input_length`、`output_length` 和 `hash_ids` 字段的请求，因此可以直接用任何兼容 Mooncake 的工具重放（例如 `aiperf --custom-dataset-type mooncake_trace`）。`hash_ids` 字段编码了共享前缀块，非常适合对 KV 缓存复用与前缀缓存行为做基准测试。

这是一个智能体多轮工作负载：长输入配短生成，用以反映真实的长程智能体行为。输入以约 67k token 的中位数为中心，配以约 400 token 的短输出，但输入分布是双峰的而非一律巨大：约一半请求在 64k 以上（≈53%，重尾延伸到约 1M token），另一半为中短输入（≈47% 低于 64k，约 18% 低于 8k）。约 8% 的请求超过 128k，约 3–4% 超过 256k。

### 2.2 解码上下文并行的收益

我们在一台 8×B200 节点上用 vLLM 以 NVFP4 服务 Kimi K2.6 做了实验，请求并发从 16 扫到 512（见下表）。DCP 支持远更高的并发，并在整个吞吐–交互性 Pareto 前沿上提供明显更高的每 GPU 吞吐。

![](https://vllm.ai/blog-assets/figures/2026-07-27-decode-context-parallelism/figure-3.png)

差异归结为 KV 缓存放在哪里。基线 TP 在每块 GPU 上复制 KV 缓存，峰值内存很快填满：并发 64 时达到 100% 并撞墙，吞吐在约 1,863 tok/s/GPU 附近走平，因为再也塞不下额外请求。而 DCP 沿序列维度分片 KV 缓存，每块 GPU 只存储每个请求 KV 的 1/N，使 GPU 上的空间能够支撑更多进入的请求。因此，即使在 TP 撞墙的高并发下，DCP 仍能继续扩展。DCP 在 c512 时达到 6,091 tok/s/GPU，同时 KV 使用率仅为 82%。**DCP 的核心价值在于它能支撑远更高的并发，即便在长上下文运行中也是如此——而这正是复制 KV 的 TP 最先耗尽内存的区间。**

### 2.3 按序列长度比较

![](https://vllm.ai/blog-assets/figures/2026-07-27-decode-context-parallelism/figure-4.png)

我们还把性能对完整序列长度（输入 + 输出）作图。图中显示一条贯穿的吞吐–交互性 Pareto 前沿，请求被分为五个长度区间（<32k、32–64k、64–128k、128–200k 和 200k+），以便观察性能如何随上下文长度变化。**即使在 200k+ 区间，DCP 仍保持高且稳定的前沿**，短与长区间的曲线几乎重叠：吞吐随并发扩展，而单用户速度在长上下文长度下依然可用——正是在这些长度上，复制 KV 的基线因内存耗尽而无法扩展。

## 3. 服务长上下文的挑战

在张量并行下，KV 缓存**按注意力头**划分。每个 KV 头拥有自己独立的 K 和 V 张量，头是你能交给一块 GPU 的最小单元。标准 TP 没有机制去切分单个头的 KV 缓存。因此如果你有 K 个 KV 头，你可以给每块 GPU 分配这些头的一个互不相同的子集，但只能分到每块 GPU 持有一个头为止。一旦 TP 超过 K，就没有足够多的不同头可分，两块或更多 GPU 最终只能持有同一个头的 KV 缓存副本，而不是独有的分片。

## 4. 什么是 DCP？

与纯 TP 方法不同，DCP 能够沿序列（上下文）维度把 KV 缓存切分到多块 GPU 上。每块 GPU 负责同一序列中一段 *token 位置*的 KV 缓存。对于一个 200K token 的请求，GPU 0 可能持有 token 0–50K 的缓存，GPU 1 持有 50K–100K，GPU 2 持有 100K–150K，GPU 3 持有 150K–200K。通过分片 KV 缓存，每 GPU 的 KV 缓存占用随 GPU 增加不断缩小，释放出可用于提高批大小、服务更高并发的内存。

![](https://vllm.ai/blog-assets/figures/2026-07-27-decode-context-parallelism/figure-5.png)

### 4.1 解码上下文并行的流程

标准的解码上下文并行保持通信模式简单，遵循 **AllGather Q → 计算 → AllGather + ReduceScatter** 的节奏。

- **AllGather Q：** 每块 GPU 只计算了查询的一个片段，但注意力需要完整的查询向量才能对任意键打分。在 DCP 组内做一次 all-gather，会在每块 GPU 上组装出一份完整的查询副本。解码期间这一步很便宜，因为查询只是单个 token。作为 MLA 的可选替代方案，[vLLM #45964](https://github.com/vllm-project/vllm/pull/45964) 可以在加载时于每个 DCP 组内复制（很小的）查询投影，使解码完全跳过这次查询 all-gather（`VLLM_DCP_Q_REPLICATE=1`）。
- **计算：** 每块 GPU 在收集到的查询与其 *本地* KV 缓存切片之间执行注意力。在 vLLM 中，MLA 对应 `k_up`，GQA 对应 `tensor_broadcast`。
- **AllGather + ReduceScatter（`cp_lse_ag_out_rs`）：** 把部分结果合并成真正的输出。AllGather 共享每块 GPU 的部分输出与 LSE；LSE 值对部分结果重新加权并合并（即 online-softmax 技巧），ReduceScatter 对其求和，同时只把各自头部对应的切片交还给每块 GPU。

## 5. vLLM 用法

启用 DCP 只需在现有张量并行设置之外增加一个参数：`decode_context_parallel_size`。

### 5.1 离线

```
from vllm import LLM, SamplingParams

prompts = [
    "The future of AI is",
]
sampling_params = SamplingParams(temperature=0.8, top_p=0.95)

llm = LLM(
    model="deepseek-ai/DeepSeek-V2-Lite",
    tensor_parallel_size=2,
    decode_context_parallel_size=2,
)
outputs = llm.generate(prompts, sampling_params)
```

### 5.2 在线

```
vllm serve deepseek-ai/DeepSeek-V2-Lite \
    --tensor-parallel-size 2 \
    --decode-context-parallel-size 2
```

### 5.3 MLA 后端

**模型：** 使用多头潜在注意力的 DeepSeek-V2 / V3 / R1、Kimi K2.6 等模型。

**为何不同。** MLA 把 Key/Value 压缩成单个低秩 *潜在*向量，由所有查询头共享——实际上只有一个 KV “头”。在纯张量并行下没有头可切，这个潜在 KV 缓存会在 *每个* TP rank 上完整复制。TP 无法缩小它，这让 MLA 成为 DCP 的理想候选：整个缓存都是冗余的，因此整个缓存都可以按序列切分。

**它们如何工作。** DCP 沿序列维度切分潜在 KV 缓存，每个 rank 只存储自己那份潜在切片；在注意力时，每个 rank 对自己的潜在切片做上投影（即 `k_up` 步骤），重建所需的 Key/Value。由于有效 KV 头数为 1，序列可以一直切分到整个 TP 度——因此有如下约束：

- `tensor_parallel_size >= decode_context_parallel_size`
- `tensor_parallel_size % decode_context_parallel_size == 0`

```
vllm serve deepseek-ai/DeepSeek-R1 \
    --tensor-parallel-size 8 \
    --decode-context-parallel-size 8
```

### 5.4 GQA 后端

**示例模型：** Qwen3-235B 以及其他分组查询注意力模型（Llama 系列等）。

**为何不同。** GQA 存储 `num_key_value_heads` 个 KV 头，TP 首先按这些头切分 KV 缓存。这只在不超过 `num_key_value_heads` 时才能干净地进行；一旦 `tensor_parallel_size` 超过它，KV 缓存就开始复制，各 rank 间出现 `tp // num_key_value_heads` 份完全相同的副本。

**它们如何工作。** DCP 把那些本将成为副本的空间拿来放 *不同* 的序列块，同时共享的 KV 头在其查询头之间广播（即 “GQA 的张量广播” 步骤）。因此序列切分度受复制因子 `tp // num_key_value_heads` 上限约束：

- `(tensor_parallel_size // num_key_value_heads) >= decode_context_parallel_size`
- `(tensor_parallel_size // num_key_value_heads) % decode_context_parallel_size == 0`

```
# Qwen3-235B has num_key_value_heads = 4; tp=8 gives 8//4 = 2 redundant copies,
# so dcp can be up to 2.
vllm serve Qwen/Qwen3-235B-A22B \
    --tensor-parallel-size 8 \
    --decode-context-parallel-size 2
```

## 6. 未来工作

展望未来，我们计划沿几个主要方向扩展 DCP。我们将为 TP 和 DCP 增加更细粒度的并行规模支持，让用户对并行布局有更精细的控制，并收回因过度分片而损失的效率。我们还在为多节点与单节点场景开发更好的 DCP all-to-all（A2A）通信内核，在上下文长度与设备数量增长时减少暴露的通信并改善与计算的重叠。我们正在改进对 MTP 和投机解码的支持，使 DCP 能在不牺牲投机方法延迟收益的情况下发挥其效率优势；同时加固预填充/解码（P/D）分离支持，使 DCP 在分离服务部署中保持稳健。最后，我们希望扩大 DCP 的适用范围：支持更多种类的后端，并将其与混合模型及动态分块流水线并行（Dynamic Chunked Pipeline Parallelism）集成，让更广泛的工作负载受益于上下文并行带来的效率提升。

社区也在把 DCP 扩展到 GLM-5.2 和 Kimi K3 等更多模型，预填充上下文并行（PCP）也有更长期的路线图。我们正在为 Kimi K3 模型做 DCP 性能基准测试，并计划在该工作成熟后分享结果。DCP 的部署指南与历史沿革参见 [vLLM 解码上下文并行文档](https://docs.vllm.ai/en/latest/serving/context_parallel_deployment/#decode-context-parallel)。

## 7. 结论

解码上下文并行代表着对长上下文推理中 GPU 组织方式的一次根本性反思。DCP 不再迫使 GPU 复制 KV 缓存或闲置低载，而是让每块 GPU 都干活：在注意力期间分片序列，随后立即把同一批 GPU 重新组织起来，把 FFN 权重加载摊销到整个资源池上。其结果是系统能随上下文长度优雅扩展，而不是在长上下文下性能退化。

随着 vLLM 中的原生支持，解码上下文并行已准备好支撑下一代长上下文智能体应用——从文档推理到多会话智能体流水线——并达到生产所要求的吞吐与延迟。它也汇入了业界走向解码上下文并行的更大趋势，NVIDIA 在 TensorRT-LLM 中也以 [Helix Parallelism](https://github.com/NVIDIA/TensorRT-LLM/blob/main/docs/source/blogs/tech_blog/blog22_Helix_Parallelism_Scaling_Multi_Million_Token_Decoding_with_KV_Cache_Sharding.md) 探索了同一方向。我们还在为 Kimi K3 模型做 DCP 性能基准测试，并计划在该工作成熟后分享结果。

## 关于我们

特别感谢 NVIDIA 团队的 Anahita Bhiwandiwalla、Xin Li、Pavani Majety、Nidhi Bhatia、Roman Ageev、Pen Chung Li 和 Chris Hoge 在整个研究过程中提供的评审、基准测试支持与工程意见。我们还要感谢 [Moonshot AI](https://www.moonshot.cn/) 完成最初的解码上下文并行工作并通过 [vLLM #23734](https://github.com/vllm-project/vllm/pull/23734) 上游化，感谢 [Lucas Wilkinson](https://github.com/LucasWilkinson) 做出的大量后续贡献，帮助加固并扩展了 DCP。我们也感谢更广泛的 vLLM 社区——其开源引擎与持续协作使这项基准测试工作得以完成。关于 DCP 部署及相关历史的更多信息，请参见 [vLLM 解码上下文并行文档](https://docs.vllm.ai/en/latest/serving/context_parallel_deployment/#decode-context-parallel)。

本文中的 DCP 结果在 NVIDIA B200 GPU 上以 NVFP4 服务 Kimi K2.6 测得，配方可在当前支持 `--decode-context-parallel-size` 的 vLLM 版本上复现。我们也在为 Kimi K3 模型做 DCP 性能基准测试，并计划在该工作成熟后分享结果。
