---
title: "TurboQuant 首个全面研究：精度与性能"
title_en: "A First Comprehensive Study of TurboQuant: Accuracy and Performance"
source: https://vllm.ai/blog/2026-05-11-turboquant
crawled: 2026-09-12
translated: 2026-09-13
---

# TurboQuant 首个全面研究：精度与性能

> 原文：[A First Comprehensive Study of TurboQuant: Accuracy and Performance](https://vllm.ai/blog/2026-05-11-turboquant) · vLLM 博客

作者：Eldar Kurtić、Michael Goin、Alexandre Marques（Red Hat AI）

[#量化](https://vllm.ai/blog/tags/quantization)[#KV缓存](https://vllm.ai/blog/tags/kv_cache)[#turboquant](https://vllm.ai/blog/tags/turboquant)

## 引言

[TurboQuant](https://arxiv.org/pdf/2504.19874) 是一种 KV 缓存量化方法，最近因宣称可通过极低比特宽度的模型 KV 缓存量化大幅节省 GPU 显存而在社区获得显著关注。与 [FP8 KV 缓存量化](https://vllm.ai/blog/fp8-kvcache)不同——后者使用硬件原生的 FP8 Tensor Core 操作，同时对 KV 缓存存储和注意力计算本身进行量化——TurboQuant 只将 KV 缓存存储压缩到 3-4 比特，并在注意力计算时反量化回 BF16。这一架构差异对精度和性能都有重大影响。

然而，大多数已报告的结果都基于小模型和短上下文基准测试，并未对 KV 缓存量化形成真正的压力测试。为了给社区提供更具可操作性的数据，我们开展了一项全面研究，涵盖四个模型（既有纯稠密模型也有 MoE 模型），参数规模从 30B 到 200B+，以及五个基准测试，既包括预填充为主的长上下文检索，也包括解码为主的推理工作负载。

![Figure 1: Pareto frontier for Llama-3.3-70B-Instruct on 4xH100. FP8 dominates with 2.6x higher burst throughput than BF16 and 2x KV-cache capacity. All TurboQuant variants trade throughput for additional memory savings.](https://vllm.ai/blog-assets/figures/2026-05-11-turboquant/llama_70b_pareto.png)

图 1：Llama-3.3-70B-Instruct 在 4xH100 上的帕累托前沿。FP8 占据主导，突发吞吐量比 BF16 高 2.6 倍，KV 缓存容量为 2 倍。所有 TurboQuant 变体都以吞吐量换取更多显存节省。

![Figure 2: Pareto frontier for Qwen3-30B-A3B-Instruct-2507 on 2xH100. FP8 matches BF16 throughput at 2x capacity. TurboQuant variants extend capacity to 2.3-3.7x but at 40-52% throughput reduction.](https://vllm.ai/blog-assets/figures/2026-05-11-turboquant/qwen3_30b_a3b_pareto.png)

图 2：Qwen3-30B-A3B-Instruct-2507 在 2xH100 上的帕累托前沿。FP8 在 2 倍容量下匹配 BF16 吞吐量。TurboQuant 变体将容量扩展到 2.3-3.7 倍，但吞吐量下降 40-52%。

**TL;DR**

- 通过 `--kv-cache-dtype fp8` 使用 FP8 仍是 KV 缓存量化的最佳默认选择：它以可忽略的精度损失提供 2 倍 KV 缓存容量，在大多数性能指标上与 BF16 持平，并且在显存受限的服务场景下大幅改善这些指标。
- TurboQuant `k8v4` 相比 FP8 没有任何显著优势：它仅提供适度的 KV 缓存节省（2.4 倍对比 2 倍），却要对吞吐量和延迟指标造成持续的负面影响，得不偿失。
- TurboQuant `4bit-nc` 可能是最实用的 TurboQuant 变体：它在 KV 缓存显存压力下有帮助，但用额外的容量换来了中等程度的精度、延迟和吞吐量代价。对于显存是首要约束的边缘部署，它仍然可行。
- TurboQuant `k3v4-nc` 和 `3bit-nc` 出现明显的精度下降，尤其是在推理和超长上下文任务上，同时还会显著恶化延迟和吞吐量。这使它们不适合作为生产部署的选择。

**目录**

- [实验设置](#experimental-setup)
- [精度结果](#accuracy-results)
  - [长上下文检索](#long-context-retrieval)
  - [推理](#reasoning)
- [性能结果](#performance-results)
  - [延迟](#latency)
  - [吞吐量](#throughput)
  - [服务速度](#serving-speed)
- [关键发现与建议](#key-findings-and-recommendations)

**快速开始：**

```
# FP8 KV-cache for all layers
vllm serve MiniMaxAI/MiniMax-M2.7 --kv-cache-dtype fp8

# TurboQuant KV-cache, skipping the first and last two layers
vllm serve MiniMaxAI/MiniMax-M2.7 --kv-cache-dtype turboquant_4bit_nc
```

## 实验设置

**量化方案：** 我们将四种 TurboQuant 变体（`--kv-cache-dtype turboquant_{k8v4, 4bit_nc, k3v4_nc, 3bit_nc}`）与未量化的 BF16 和 FP8 KV 缓存基线进行对比测试。`turboquant_k8v4` 使用 8 比特键和 4 比特值；`turboquant_4bit_nc` 使用 4 比特键值并做范数校正（norm correction）；`turboquant_k3v4_nc` 使用 3 比特键和 4 比特值并做范数校正；`turboquant_3bit_nc` 使用 3 比特键值并做范数校正。FP8 基线（`--kv-cache-dtype fp8`）以 FP8 精度存储查询、键和值，并且对注意力计算本身也进行量化——这是它与只压缩存储的 TurboQuant 的关键区别。有关各 TurboQuant 变体的更多细节，请参阅[论文](https://arxiv.org/pdf/2504.19874)和 [vLLM 文档](https://docs.vllm.ai/en/latest/api/vllm/model_executor/layers/quantization/turboquant/)。有关 FP8 KV 缓存量化的更多细节，请参阅 [FP8 KV 缓存博客文章](https://vllm.ai/blog/fp8-kvcache)。

**基准测试：** 我们在五个基准上进行评估，这些基准旨在对预填充为主和解码为主两类工作负载下的 KV 缓存量化进行压力测试。长上下文检索（预填充为主）使用 `openai/mrcr`——一个具有挑战性的多轮上下文检索任务，测试序列长度直至每个模型支持的最大长度。推理（解码为主）使用 AIME25、GPQA:Diamond、MATH500 和 LiveCodeBench-v6。所有评估都采用模型创作者建议的默认非贪心采样参数，以模拟真实部署。

**模型：** 我们聚焦四个模型，覆盖小规模与大规模、纯稠密与 MoE 架构：`Llama-3.3-70B-Instruct`、`Qwen3-30B-A3B-Instruct-2507`、`Qwen3-30B-A3B-Thinking-2507` 和 `MiniMax-M2.7`。截至撰写时，TurboQuant 仅支持采用标准注意力机制（如 GQA）的模型——尚不支持滑动窗口注意力或混合注意力的模型。

## 精度结果

### 长上下文检索

长上下文评估使用 `openai/mrcr` 任务，测试序列长度直至每个模型支持的最大长度。我们报告每个序列长度桶在 5 次重复上的平均 pass@1 分数，并以曲线下面积（AUC）作为跨所有测试长度的聚合指标（[Context Arena](https://contextarena.ai/)）。

![Figure 3: Long-context retrieval results for Llama-3.3-70B-Instruct up to 64k context. At 128k, the model's maximum supported context length, the BF16 baseline collapses to <10%.](https://vllm.ai/blog-assets/figures/2026-05-11-turboquant/Llama-3.3-70B-Instruct_openai_mrcr_2_needles_plot.png)

图 3：Llama-3.3-70B-Instruct 在 64k 上下文以内的长上下文检索结果。在 128k（该模型支持的最大上下文长度）处，BF16 基线崩溃至 <10%。

在 Llama-3.3-70B-Instruct 上（图 3），较高比特的 TurboQuant 变体（k8v4 和 4bit-nc）很好地保留了长上下文检索能力，并保持了有竞争力的 AUC（约 52%）。然而，TQ k3v4-nc（48.6%）和 3bit-nc（50.3%）在所有序列长度上都表现出明显且持续的退化，且差距在 64k 上下文处进一步扩大，精度下降最多达 8 个百分点。

![Figure 4: Long-context retrieval results for Qwen3-30B-A3B-Instruct-2507 up to 256k context.](https://vllm.ai/blog-assets/figures/2026-05-11-turboquant/Qwen3-30B-A3B-Instruct-2507_openai_mrcr_2_needles_plot.png)

图 4：Qwen3-30B-A3B-Instruct-2507 在 256k 上下文以内的长上下文检索结果。

在支持最长 256k 上下文的 Qwen3-30B-A3B-Instruct-2507 上（图 4），差异更加明显。BF16（45.8%）、FP8（43.1%）和 TQ k8v4（43.0%）相互之间保持在彼此标准差范围内。TQ 4bit-nc（42.3%）同样具有竞争力。但激进的变体退化严重：TQ k3v4-nc 降至 33.5% AUC，TQ 3bit-nc 降至 31.2%——相对 BF16 约 30% 的相对退化。退化集中在最长的上下文长度（128k-256k），表明低比特 KV 缓存量化的误差会随序列长度累积。

**要点：** TQ k8v4 和 4bit-nc 在长上下文检索上是安全的。TQ k3v4-nc 和 3bit-nc 出现明显的精度退化，尤其是在超长上下文中。FP8 与较高比特的 TQ 变体相当，同时提供更好的推理性能（见后文）。

### 推理

解码为主的推理基准使用 AIME25、GPQA:Diamond、MATH500 和 LiveCodeBench-v6。我们报告平均 pass@1 分数：AIME25 和 LiveCodeBench-v6 为 10 次重复，GPQA:Diamond 和 MATH500 为 5 次重复。

![Figure 5: Reasoning results for Qwen3-30B-A3B-Thinking-2507. Aggressive TQ variants (k3v4-nc, 3bit-nc) show very large drops on AIME25 and LiveCodeBench-v6.](https://vllm.ai/blog-assets/figures/2026-05-11-turboquant/Qwen3-30B-A3B-Thinking-2507_reasoning_plot.png)

图 5：Qwen3-30B-A3B-Thinking-2507 的推理结果。激进的 TQ 变体（k3v4-nc、3bit-nc）在 AIME25 和 LiveCodeBench-v6 上出现非常大的降幅。

在 Qwen3-30B-A3B-Thinking-2507 上（图 5），我们可以看到清晰的精度层级。FP8 和 TQ k8v4 接近 BF16 基线，平均精度恢复率 >98%。TQ 4bit-nc 的降幅稍大，恢复率为 96%，而 TQ k3v4-nc 和 3bit-nc 出现约 20 个百分点的剧烈精度下降。即使在相对简单的 MATH500 基准上，精度下降也约为 4 个百分点，这表明激进的 TurboQuant 变体并不适合长生成推理任务。

![Figure 6: Reasoning results for MiniMax-M2.7. Despite the fact that larger models tend to be more robust to quantization, aggressive TurboQuant variants still show significant accuracy degradation, specifically on AIME25 and LiveCodeBench-v6.](https://vllm.ai/blog-assets/figures/2026-05-11-turboquant/MiniMax-M2.7_reasoning_plot.png)

图 6：MiniMax-M2.7 的推理结果。尽管更大的模型通常对量化更鲁棒，激进的 TurboQuant 变体仍表现出显著的精度退化，尤其是在 AIME25 和 LiveCodeBench-v6 上。

在参数规模大得多的 200B+ 模型 MiniMax-M2.7 上（图 6），我们观察到类似的模式。FP8 和 TQ k8v4 保持 >99% 的精度恢复率，而 TQ 4bit-nc 出现适度下降。与较小的 Qwen 模型一样，激进的 TQ 变体（k3v4-nc、3bit-nc）表现出显著的精度退化，尤其是在 AIME25 和 LiveCodeBench-v6 上，精度下降最多约 8 个百分点。

**要点：** 激进的 TurboQuant 变体（k3v4-nc、3bit-nc）表现出显著的精度退化，尤其是在 AIME25 和 LiveCodeBench-v6 这类困难的数学与编程任务上。TQ 4bit-nc 出现适度的精度下降，而 TQ k8v4 的表现与未量化的 BF16 基线相当。FP8 同样与未量化基线持平；但它提供的推理性能显著优于任何 TurboQuant 变体（见后文）。

## 性能结果

性能基准测试聚焦 `Qwen3-30B-A3B-Instruct-2507`（2xH100）和 `Llama-3.3-70B-Instruct`（4xH100）。我们在各种请求速率下测量延迟、离线吞吐量和在线服务指标（TPOT 与 TTFT）。模型使用 vLLM 版本 `0.20.2`（commit `6ec9bbec3`）部署。

### 延迟

我们使用 `vllm bench latency` 测量延迟，采用固定的合成请求（输入长度 1024、输出长度 256），扫过批大小 1、8、32 和 64。每个配置先进行 10 次预热迭代，再进行 30 次测量迭代。结果以相对 BF16 的减速比呈现（越低越好）。

![Figure 7: Latency overhead relative to BF16 for Qwen3-30B-A3B-Instruct-2507. FP8 has negligible overhead which disappears with batching; TurboQuant (TQ) adds up to 60% slowdown depending on the variant and batch size.](https://vllm.ai/blog-assets/figures/2026-05-11-turboquant/qwen3_30b_a3b_latency.png)

图 7：Qwen3-30B-A3B-Instruct-2507 相对 BF16 的延迟开销。FP8 的开销可忽略，且随批处理消失；TurboQuant（TQ）根据变体和批大小不同最多增加 60% 的减速。

![Figure 8: Latency overhead relative to BF16 for Llama-3.3-70B-Instruct. FP8 has negligible overhead, whereas TQ overhead ranges from 10% to 68%.](https://vllm.ai/blog-assets/figures/2026-05-11-turboquant/llama_70b_latency.png)

图 8：Llama-3.3-70B-Instruct 相对 BF16 的延迟开销。FP8 开销可忽略，而 TQ 的开销在 10% 到 68% 之间。

在两个模型和所有批大小上，FP8 始终保持可忽略或零延迟开销——这是符合预期的，因为 FP8 使用硬件原生的 FP8 Tensor Core 操作对注意力计算本身进行量化，避免了反量化开销。所有 TurboQuant 变体都会增加可测量的延迟：在 Qwen3-30B 上（图 7），开销范围约 10% 到 60%；在 Llama-3.3-70B 上（图 8），开销整体更高，约 10% 到 68%。值得注意的是，对于更大的 Llama-70B 模型，TQ 开销往往随批大小*增加*——这与该用例所期望的正好相反。这是因为 TurboQuant 必须在计算注意力之前将 KV 缓存从低比特存储反量化回 BF16，而这一反量化成本会随被访问的 KV 缓存量增长。

### 吞吐量

我们使用 `vllm bench throughput` 测量离线吞吐量，采用 200 个提示，覆盖三组输入/输出长度对：256/256、1024/512 和 4096/256。结果以 BF16 吞吐量的百分比呈现（越高越好）。

![Figure 9: Average throughput relative to BF16 for Qwen3-30B-A3B-Instruct-2507. FP8 preserves BF16 throughput, while all TurboQuant variants reduce throughput, indicating that lower KV-cache storage cost does not directly translate into faster serving.](https://vllm.ai/blog-assets/figures/2026-05-11-turboquant/qwen3_30b_a3b_throughput.png)

图 9：Qwen3-30B-A3B-Instruct-2507 相对 BF16 的平均吞吐量。FP8 保持了 BF16 吞吐量，而所有 TurboQuant 变体都降低了吞吐量，这表明更低的 KV 缓存存储成本并不能直接转化为更快的服务。

![Figure 10: Average throughput relative to BF16 for Llama-3.3-70B-Instruct. FP8 preserves BF16 throughput, while all TurboQuant variants reduce throughput, indicating that lower KV-cache storage cost does not directly translate into faster serving.](https://vllm.ai/blog-assets/figures/2026-05-11-turboquant/llama_70b_throughput.png)

图 10：Llama-3.3-70B-Instruct 相对 BF16 的平均吞吐量。FP8 保持了 BF16 吞吐量，而所有 TurboQuant 变体都降低了吞吐量，这表明更低的 KV 缓存存储成本并不能直接转化为更快的服务。

吞吐量结果印证了延迟方面的发现。FP8 在两个模型上都与 BF16 吞吐量持平。所有 TurboQuant 变体都严格低于 BF16：在 Qwen3-30B 上（图 9），范围从 80%（k8v4）到 73%（3bit-nc）；在 Llama-70B 上（图 10），从 75%（k8v4 和 4bit-nc）到 66%（3bit-nc）。更激进的量化始终带来更低的吞吐量——反量化开销随打包格式的复杂度增长。

### 服务速度

我们使用 `vllm bench serve` 测量服务性能，采用输入长度 1024、输出长度 512 的合成请求，300 个测量提示和 5 个预热请求。我们测试请求速率 2、8 和 `inf`（尽可能快地发送请求）。我们同时报告 TPOT（Time Per Output Token，每输出 token 时间——衡量解码速度）和 P99 TTFT（Time To First Token，首 token 时间——衡量请求开始生成的速度）。

![Figure 11: Serving time per output token (TPOT) for Qwen3-30B-A3B-Instruct-2507.](https://vllm.ai/blog-assets/figures/2026-05-11-turboquant/qwen3_30b_a3b_serve.png)

图 11：Qwen3-30B-A3B-Instruct-2507 的服务每输出 token 时间（TPOT）。

![Figure 12: Serving time per output token (TPOT) for Llama-3.3-70B-Instruct.](https://vllm.ai/blog-assets/figures/2026-05-11-turboquant/llama_70b_serve.png)

图 12：Llama-3.3-70B-Instruct 的服务每输出 token 时间（TPOT）。

TPOT 结果（图 11-12）与延迟和吞吐量的发现一致：FP8 在所有请求速率下要么与 BF16 持平，要么更优，而 TQ 变体增加了随负载增长的显著每 token 开销。在 Llama-70B 的突发负载下，FP8 比 BF16 快近 2 倍，而 TQ 变体慢 1.5 到 2.5 倍。

![Figure 13: P99 TTFT for Qwen3-30B-A3B-Instruct-2507.](https://vllm.ai/blog-assets/figures/2026-05-11-turboquant/qwen3_30b_a3b_ttft.png)

图 13：Qwen3-30B-A3B-Instruct-2507 的 P99 TTFT。

![Figure 14: P99 TTFT for Llama-3.3-70B-Instruct. Under burst load, BF16 TTFT explodes to ~17s due to memory saturation; TurboQuant variants stay under 3.5s and FP8 under 1.5s.](https://vllm.ai/blog-assets/figures/2026-05-11-turboquant/llama_70b_ttft.png)

图 14：Llama-3.3-70B-Instruct 的 P99 TTFT。在突发负载下，BF16 的 TTFT 因显存饱和而飙升至约 17 秒；TurboQuant 变体保持在 3.5 秒以内，FP8 则在 1.5 秒以内。

在 2xH100 上显存余量更多的 Qwen3-30B 上（图 13），FP8 在所有请求速率下的表现与 BF16 完全一致。TurboQuant 变体始终更慢，突发负载下减速最高达 2 倍。在 KV 缓存空间有限的 4xH100 上运行的 Llama-3.3-70B 上（图 14），突发负载下 BF16 的 TTFT 飙升至约 17 秒，因为系统耗尽 KV 缓存显存，必须将新到请求排队。所有 TurboQuant 变体都保持在 3.5 秒以内——5 倍的改善——因为其压缩的 KV 缓存允许更多并发请求无需排队即可处理。与此同时，FP8 以约 1.3 秒实现最低 TTFT，并始终优于所有 TurboQuant 变体。

**要点：** TurboQuant 通过降低吞吐量和增加每 token 延迟，始终逊于 BF16 和 FP8。然而，在显存受限的服务场景下，KV 缓存压缩可防止显存饱和，并在突发负载下相对 BF16 大幅降低 TTFT。这正是 TurboQuant 价值主张的核心：用每 token 速度换取服务那些原本会被排队请求的能力。而 FP8 则两全其美：它匹配甚至超越 BF16 吞吐量，同时提供可忽略的延迟开销和显著更好的突发负载 TTFT。

## 关键发现与建议

基于在精度与性能基准上的全面评估，我们给出以下实用建议：

**FP8（`--kv-cache-dtype fp8`）仍是 KV 缓存量化的最佳默认选择。** FP8 以零吞吐量代价、可忽略的精度损失提供 2 倍 KV 缓存容量，有时甚至通过量化注意力获得性能提升。对绝大多数工作负载而言，它是最安全、最可预测的选择，[FP8 KV 缓存博客文章](https://vllm.ai/blog/fp8-kvcache)中对此也有详细说明。

**TurboQuant k8v4 相比 FP8 没有任何显著优势。** 这一 TQ 变体仅提供适度的 KV 缓存节省（2.4 倍对比 2 倍），却要对吞吐量和延迟指标造成持续的负面影响，得不偿失。

**TurboQuant 4bit-nc 提供了诱人的以吞吐量换显存的折中。** 这一变体提供高达 3.4 倍的 KV 缓存容量，在大多数基准上精度仅下降 1-4 个百分点。对于显存受限的部署，突发负载下的 TTFT 改善超过其对其他所有指标的负面影响，因此它特别有价值。部署前请在目标工作负载上充分验证精度。

**未经充分验证，请避免使用 TurboQuant k3v4-nc 和 3bit-nc。** 这些激进变体会造成剧烈的精度下降，在具有挑战性的数学和编程基准上最多可达 20 个百分点。除精度外，它们因复杂的反量化步骤而持续的性能退化，也使其不适合生产部署。

**当 GPU 显存不是瓶颈时，请继续使用 BF16。** 如果你的工作负载使用短上下文、以低并发运行，或硬件显存充足，BF16 可提供最佳的精度-性能折中，且没有量化伪影的风险。
