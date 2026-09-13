---
title: "迈向 SGLang 确定性推理与可复现 RL 训练"
title_en: "Towards Deterministic Inference in SGLang and Reproducible RL Training"
author: "The SGLang Team"
date: "September 22, 2025 (Updated on September 24)"
previewImg: /images/blog/deterministic/logo.png
source: https://lmsys.org/blog/2025-09-22-sglang-deterministic/
translated: 2026-09-12
---

# 迈向 SGLang 确定性推理与可复现 RL 训练

> 原文：[Towards Deterministic Inference in SGLang and Reproducible RL Training](https://lmsys.org/blog/2025-09-22-sglang-deterministic/) · LMSYS Blog · The SGLang Team


**TL;DR**：本文分享了我们在 SGLang 中实现确定性推理的工作，以及与 [slime](https://github.com/THUDM/slime) 合作推进可复现 RL 训练的进展。

<br />


近期，Thinking Machines Lab 发布了一篇[博客](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)，详细介绍了他们的研究发现。该博客发布后，业界反响热烈，热切期待开源推理引擎能够实现稳定可用的确定性推理，乃至更进一步，实现完全可复现的 RL 训练。现在，SGLang 与 slime 共同给出了答案。

基于 Thinking Machines Lab 的批不变（batch-invariant）算子，SGLang 实现了完全确定性推理，同时保持与**分块预填充（chunked prefill）**、**CUDA 图（CUDA Graph）**、**基数树缓存（radix cache）**以及**非贪心采样**的兼容。借助 CUDA 图，SGLang 实现了 **2.8 倍加速**，并将性能开销降至仅 **34.35%**（TML 为 **61.5%**）。
 
在此基础上更进一步，SGLang 与 slime 团队合作，以极小的代码改动解锁了 **100% 可复现的 RL 训练**——这是一项重要突破。我们在 Qwen3-8B 上的验证实验展示了完美的可复现性：**两次独立的训练运行产生了完全一致的曲线**，为严谨的科学实验提供了所需的可靠性。

![slime](/images/blog/deterministic/slime.png)<small><center>[*可复现指南*](https://thudm.github.io/slime/_examples_synced/reproducibility/README.html#reproducibility)</center></small>


<br />

下面让我们深入了解一些技术细节。

## 为什么确定性推理很重要

从大语言模型（LLM）推理中获得一致输出的能力正变得越来越重要。例如，正如[研究人员指出的](https://fengyao.notion.site/off-policy-rl)，推理结果的非确定性会将同策略强化学习（on-policy RL）隐式地变为异策略强化学习（off-policy RL）。然而，即使我们将 SGLang 中的温度调到 0，由于动态批处理和基数树缓存的使用，采样仍然不是确定性的（过往讨论见[这里](https://docs.sglang.io/references/faq.html#the-results-are-not-deterministic-even-with-a-temperature-of-0)）。

正如该[博客](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)所述，非确定性的最大来源是批大小的变化：即使用户反复提交相同的 prompt，输出也可能因运行而异，因为该请求可能与其他用户的请求被合入同一批，而批大小的差异会导致推理结果不确定。

进一步解释：不同的批大小会影响 kernel 的归约（reduction）切分过程，导致每个归约块的顺序和大小各不相同，而浮点运算不满足结合律，因此会产生不确定的输出。为解决这一问题，他们用批不变的实现替换了归约类 kernel（RMSNorm、矩阵乘法、注意力等）。这些 kernel 也作为[配套库](https://github.com/thinking-machines-lab/batch_invariant_ops)发布，供外部集成使用。 

![figure1](/images/blog/deterministic/deterministic_intro.png)<small><center>*He, Horace and Thinking Machines Lab, "Defeating Nondeterminism in LLM Inference", 
Thinking Machines Lab: Connectionism, Sep 2025.*</center></small>


基于 Thinking Machines Lab 的工作，SGLang 交付了一套稳健、高吞吐的确定性 LLM 推理方案，将批不变 kernel、CUDA 图、基数树缓存与分块预填充以高效性能结合在一起。确定性已通过全面测试和 RL 训练实验得到充分验证。

主要增强包括：
- **集成 Thinking Machines Lab 的批不变 kernel**，包括 mean、log-softmax 和矩阵乘法 kernel。
- **实现固定 split-KV 大小的批不变注意力 kernel**。支持多种后端，包括 FlashInfer、FlashAttention 3 和 Triton。
- **完全兼容常见推理特性**：分块预填充、CUDA 图、基数树缓存等在启用确定性推理后均继续可用。
- **在采样参数中暴露每请求种子（per-request seed）**，使用户即使 temperature > 0 也能启用确定性推理。
- **更好的性能**：相比 TML 博客中报告的 **61.5%** 降速，SGLang 在 FlashInfer 和 FlashAttention 3 后端下平均降速仅 **34.35%**，改进显著。配合 CUDA 图，相比最小集成方案可实现 2.8 倍加速。


## 结果


### 验证确定性

我们引入了[一套确定性测试套件](https://github.com/sgl-project/sglang/blob/f1d789231896da438749b395f7bf007a5b0819c0/python/sglang/test/test_deterministic.py)，用于验证推理结果在不同批处理条件下是否保持一致。该测试包含三个子测试，难度由浅入深：

- Single：在不同批大小下运行相同的 prompt，检查输出是否保持一致。
- Mixed：在同一批内混合不同类型的 prompt（短 prompt 和长 prompt），验证一致性。
- Prefix：使用由同一长文本派生、前缀长度不同的 prompt，随机组批，测试多次试验的结果是否可复现。

以下是 50 次采样试验的结果。数字表示每个子测试观察到的不同输出数量（数值越低，确定性越强）。

| 注意力后端 | 模式 | Single 测试 | Mixed 测试 (P1/P2/Long) | Prefix 测试 (prefix_len=1/511/2048/4097) | 
| --- | --- | --- | --- | --- |
| FlashInfer | 正常 | 4| 3 / 3 / 2 | 5 / 8 / 18 / 2 |
| FlashInfer | 确定性 | 1 | 1 / 1 / 1 | 1 / 1 / 1 / 1 |
| FA3 | 正常 | 3 | 3 / 2 / 2 | 4 / 4 / 10 / 1 |
| FA3 | 确定性 | 1 | 1 / 1 / 1 | 1 / 1 / 1 / 1 |
| Triton | 正常 | 3 | 2 / 3 / 1 | 5 / 4 / 13 / 2 |
| Triton | 确定性 | 1 | 1 / 1 / 1 | 1 / 1 / 1 / 1 |
---
<small>*测试模型：QWen3-8B</small>

<small>* 已启用 CUDA graph 和分块预填充。FlashInfer 与 Triton 的基数树缓存支持仍在开发中，故对其禁用。 </small>


### CUDA 图加速 

CUDA 图可以通过将多次 kernel 启动合并为一次启动来加速推理过程。我们的评测比较了启用与禁用 CUDA 图时确定性推理的总吞吐量。测试负载为 16 个请求，每个请求输入长度 1024、输出长度 1024。结果显示，启用 CUDA 图后，所有注意力 kernel 至少获得 2.79 倍加速。

| 注意力后端 | CUDA 图 | 吞吐量 |
| --- | --- | --- |
| FlashInfer | 禁用 | 441.73 |
| FlashInfer | 启用 | 1245.51 (2.82x) |
| FA3 | 禁用 | 447.64 |
| FA3 | 启用 | 1247.64 (2.79x) |
| Triton | 禁用 | 419.64 |
| Triton | 启用 | 1228.36 (2.93x) |
---
<small>*环境：QWen3-8B、TP1、H100 80GB  </small>

<small>*由于 FlashInfer 与 Triton 的基数树缓存支持仍在开发中，所有性能基准测试均禁用了基数树缓存。 </small>

### 离线推理性能测量

我们使用三种常见 RL rollout 负载（256 个请求，输入/输出长度各不相同），测量了非确定性与确定性两种模式下的端到端延迟。

确定性推理总体可用，大多数场景的降速在 25% 至 45% 之间，FlashInfer 和 FlashAttention 3 后端的平均降速为 34.35%。这些开销大部分来自尚未优化的批不变 kernel（矩阵乘法和注意力），表明性能仍有很大的提升空间。

| 注意力后端 | 模式 | Input 1024 Output 1024| Input 4096 Output 4096 | Input 8192 Output 8192 | 
| --- | --- | --- | --- | --- |
| FlashInfer | 正常 | 30.85 | 332.32 | 1623.87 |
| FlashInfer | 确定性 | 43.99 (+42.6%) | 485.16 (+46.0%) | 2020.13 (+24.4%) |
| FA3 | 正常 | 34.70 | 379.85 | 1438.41 |
| FA3 | 确定性 | 44.14 (+27.2%) | 494.56 (+30.2%) | 1952.92 (+35.7%) |
| Triton | 正常 | 36.91 | 400.59 | 1586.05  |
| Triton | 确定性 | 57.25 (+55.1%) | 579.43 (+44.64%) | 2296.60 (+44.80%) |
---
<small>*环境：QWen3-8B、TP1、H200 140GB。 </small>

<small>*由于 FlashInfer 与 Triton 的基数树缓存支持仍在开发中，所有性能基准测试均禁用了基数树缓存。 </small>

我们承认确定性推理目前明显慢于正常模式。我们建议将其主要用于调试与可复现性场景。未来的工作将聚焦于加速确定性推理，目标是将性能差距缩小到 20% 以内，理想情况下与正常模式持平。

## 使用方法

### 环境搭建

要搭建环境，请安装版本 >=0.5.3 的 SGLang
```bash
pip install "sglang[all]>=0.5.3"
```
### 启动服务器

SGLang 支持跨多个模型的确定性推理。例如，对于 Qwen3-8B，只需在启动服务器时添加 `--enable-deterministic-inference` flag 即可：

```bash
python3 -m sglang.launch_server \
    --model-path Qwen/Qwen3-8B \
    --attention-backend <flashinfer|fa3|triton> \
    --enable-deterministic-inference
```

## 技术细节


### 分块预填充

SGLang 的分块预填充技术旨在管理长上下文请求。但其默认分块策略违反了注意力 kernel 的确定性要求。  

如下图所示，考虑两条输入序列 `seq_a` 和 `seq_b`，上下文长度均为 6,000。分块预填充的最大块大小为 8192，而确定性注意力所需的 split-KV 大小为 2,048。每条序列可以被切分为三个更小的单元（`a1` 到 `a3` 以及 `b1` 到 `b3`），长度分别为 2,048、2,048 和 1,904。如果这些较小单元在分块预填充过程中保持完整，它们就能由同一个注意力 kernel 处理，从而产生确定性的归约行为。


<img src="/images/blog/deterministic/chunked_prefill.png" style="width: 30vw; min-width: 200px;" />


标准分块策略遵循"尽力而为"（best-effort）原则。在本例中，该策略试图通过将 `seq_b` 的 `b2` 单元拆分为两个更小的部分来生成 8,192 个 token 的 `chunk_1`。这会导致截断点不一致，因为 `b2` 拆分后的长度取决于 `seq_a` 的长度。为解决这一问题，我们调整了分块逻辑，**将截断点对齐到 split_kv_size 的整数倍**。这一调整确保 `b2` 的处理被推迟到后续块中，使其能够作为一个完整单元由注意力 kernel 计算。 

### 注意力后端

注意力 kernel 是确定性的重要组成部分。针对不同的注意力后端，我们以不同方式进行了修改，以满足各自的使用要求。
- 对于 FlashInfer 后端，我们利用[批不变 FA2 kernel](https://github.com/flashinfer-ai/flashinfer/pull/1675) 中的 `fixed_split_size` 和 `disable_kv_split` 参数，在 kernel 规划（planning）阶段固定 split 大小。分块预填充的截断点与预填充 split 大小对齐。（[PR 链接](https://github.com/sgl-project/sglang/pull/10645)）
- 对于 FlashAttention-3 后端，将 flash attention kernel 的 num-splits 固定为 1 以确保确定性。（[PR 链接](https://github.com/sgl-project/sglang/pull/10651)）
- 对于 Triton 后端，我们固定了解码的 split 大小，并手动设置了分块预填充的对齐大小。借助 Triton 后端的可扩展性，确定性推理也可以在 **AMD** 硬件上运行。（[PR 链接](https://github.com/sgl-project/sglang/pull/10694)）。 


### 可复现的非贪心采样
为了将确定性扩展到贪心解码之外，我们引入了一个新的采样函数：[multinomial_with_seed](https://github.com/sgl-project/sglang/blob/e2ac7888b8cb1fd6c33a7ec58d27a5f5b5b24e0c/python/sglang/srt/layers/sampler.py#L268-L299)。

我们不再依赖 `torch.multinomial`——它在批处理下本质上是不确定的——而是让该算子使用由**带种子的哈希函数**生成的 Gumbel 噪声对 logits 进行扰动。这样，相同的 `(inputs, seed)` 组合总是产生相同的采样结果，即使 temperature > 0。


这一修改在保留强化学习 rollout 所需随机性的同时，实现了**确定性的多项分布采样**。


### RL 框架集成（slime）

我们[将](https://github.com/THUDM/slime/pull/361) temperature > 0 的确定性推理集成到了 slime 的 GRPO 训练流程中。在初步实验中，重复的 RL 训练运行在最初的若干次迭代中产生了**完全一致的 rollout 响应与损失值**，证实了 rollout 过程本身是确定性的。 

在后续的 [PR](https://github.com/THUDM/slime/pull/370) 中，我们通过实现以下关键配置，进一步实现了完整的训练可复现性：

- **Flash Attention**：使用 Flash Attention v2 替代 v3，以实现确定性的反向传播
- **Megatron**：设置 `--deterministic-mode` flag 以实现确定性训练
- **环境变量**：配置关键设置：
  - `NCCL_ALGO=Ring`
  - `NVTE_ALLOW_NONDETERMINISTIC_ALGO=0`
  - `CUBLAS_WORKSPACE_CONFIG=:4096:8`
- **PyTorch**：启用 `torch.use_deterministic_algorithms(True, warn_only=False)`

通过这些全面改动，我们成功实现了 slime 中 GRPO 的完整训练可复现性，达成了真正确定性的端到端 RL 训练流水线。


## 未来工作
我们未来的工作将聚焦于通过解决以下关键方向来增强确定性推理：
- **更快的批不变 kernel**：批不变 kernel 是性能瓶颈，因此我们将致力于优化其配置，并可能对其进行重写以提升性能。这对提高 RL rollout 的速度也至关重要。
- **支持 MoE 模型**：目前我们仅支持 QWen3-8B 或 LLaMa-3.1-8B 等稠密模型的确定性推理。未来我们计划将支持扩展到 Qwen3-30B-A3B 或 DeepSeek-V3 等 MoE 模型。
- **真正的同策略（on-policy）RL**：我们计划进一步将确定性推理集成到强化学习框架（如 [slime](https://github.com/THUDM/slime)）中，实现可复现采样，最终目标是实现真正的同策略训练。
- **增强基数树缓存功能**：我们将改进基数树，使其兼容更多种类的注意力 kernel，突破当前仅限 FlashAttention 3 后端的限制。
- **张量并行**：由于浮点加法顺序一致，TP1 和 TP2 是确定性的；更大的 TP 配置需要修改归约 kernel 才能实现确定性。
- **FlexAttention 集成**：除目前支持的注意力后端外，我们计划未来将确定性推理的支持扩展到 FlexAttention。
- 确定性推理功能的**路线图**见[该 issue](https://github.com/sgl-project/sglang/issues/10278)。

SGLang 的确定性推理与 slime 的可复现训练能力目前仍在积极开发和改进中。我们诚挚欢迎用户和开发者积极试用这些功能，并向我们提供宝贵反馈。你们的经验与建议将帮助我们进一步优化这些重要能力，推动确定性推理技术的发展。 

## 致谢
我们谨向以下团队与合作者致以衷心的感谢：
- **SGLang 团队与社区**：Baizhou Zhang、Biao He、Qiaolin Yu、Xinyuan Tong、Ke Bao、Yineng Zhang、Chi Zhang、Ying Sheng、Lianmin Zheng 以及许多其他贡献者
- **FlashInfer 团队与社区**：Wenxuan Tan、Yilong Zhao、Zihao Ye
- **slime 团队与社区**：Zilin Zhu
- **AMD**：Yusheng Su
- **Thinking Machines Lab**：感谢他们出色的[博客](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)与 [batch_invariant_ops 库](https://github.com/thinking-machines-lab/batch_invariant_ops)
