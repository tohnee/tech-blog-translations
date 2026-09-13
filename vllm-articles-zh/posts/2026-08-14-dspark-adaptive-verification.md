---
title: "vLLM 中的自适应验证：DSpark 置信度调度的验证"
title_en: "Adaptive Verification in vLLM: DSpark confidence-scheduled verification"
source: https://vllm.ai/blog/2026-08-14-dspark-adaptive-verification
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM 中的自适应验证：DSpark 置信度调度的验证

> 原文：[Adaptive Verification in vLLM: DSpark confidence-scheduled verification](https://vllm.ai/blog/2026-08-14-dspark-adaptive-verification) · vLLM 博客

作者：vLLM 团队

[#性能](https://vllm.ai/blog/tags/performance)[#投机解码](https://vllm.ai/blog/tags/speculative-decoding)

投机解码用更多的计算换取更少的解码步数。在批大小为 1 时，这是一笔划算的交易：GPU 受内存带宽限制、算力有余，因此额外的工作（草稿 token）几乎是免费的。而在批大小为 256 时，这笔交易就微妙得多。草稿 token 要与真实 token 争夺同样的算力，每个被拒绝的 token 都会浪费有用的计算；当被拒绝的 token 足够多时，吞吐量会显著下降。

**TL;DR**：[DSpark](https://arxiv.org/abs/2607.05147) 的置信度头（confidence head）会为每个草稿 token 通过验证的可能性打分，因此 vLLM 不必为每次部署挑选一个固定的投机长度，而是可以在每一步决定验证草稿的多大部分。开启自适应验证（`num_speculative_tokens: 7`）后，投机解码在并发高达 256 时仍能带来收益，同时在较低并发下保持较长草稿长度的优势。这减少了用户为工作负载和部署调优 `num_speculative_tokens` 的需要，让 DSpark 更容易成为"默认开启"式的收益。该功能以 `enable_adaptive_verification` 的形式在 [PR #47808](https://github.com/vllm-project/vllm/pull/47808) 中落地。

## 问题所在

逐位置的接受率衰减很快：在 DeepSeek-V4-Pro-0813 上，7-token 块中最后一个草稿 token 的存活时间不足 10%，而第一个则超过 70%。这个低概率 token 会在每个验证批次中占用一个槽位。当 GPU 受内存限制时，该槽位实际上免费，值得赌一把；一旦 GPU 饱和，这种"赌博"就有了实际的吞吐量代价。挑战在于临界点会随负载以及依赖工作负载的接受率而移动，因此没有任何静态的 `num_speculative_tokens` 能在所有并发下都最优。DSpark 的应对方式是采用自适应草稿预算，它同时考虑系统负载以及 DSpark 头认为目标模型会接受每个草稿 token 的置信程度。

## 调度预算

DSpark 每次生成一个 *k* token 的草稿块（`num_speculative_tokens`），并用一个学习得到的置信度头为每个位置输出一个置信度。调度器把它们转换为存活概率，即沿每个请求的连乘：

$S(r,i)=\prod j\le iconfidence(r,j)$

存活概率只会随位置 *i* 递减，因此在草稿 token 预算为 *B* 时，把它分配给最可能的草稿序列就是在存活分数上做一个全局 top-*B*；这自然给出每个请求草稿的一个连续前缀，无需额外约束。槽位在请求之间竞争：一个高置信请求的第 5 个位置可以排在一个低置信请求的第 1 个位置之前。

![Fixed-length verification versus confidence-scheduled trimming](https://vllm.ai/blog-assets/figures/2026-08-14-dspark-adaptive-verification/fig1-policy.svg)

固定长度验证与置信度调度裁剪的对比

*图 1. 同一批次在两种策略下的表现。固定长度验证要为全部 21 个槽位付费，包括存活率接近零的那些；自适应验证则只验证最好的 B=11 个。*

*B* 来自对每单位步时间的期望 token 数做最大化：

$B^{\ast}=arg⁡maxB\frac{N_{sampling}+\sum j<BS_{sorted}[j]}{draft_cost[num_reqs]+verify_cost[T+B]}$

分子是每个采样请求一个的奖励 token，再加上 *B* 个最佳草稿槽位的存活概率；*N*sampling 统计本步会真正采样的请求数，因此仍在处理分块预填充的请求贡献为零。分母是一张经过剖析的成本表，以本步的 token 数为索引：*T* 是已调度但不是草稿的 token 数，因此 *T* + *B* 就是整个步。两者都是数组，所以这个选择就是对累计和做一次 `np.argmax`，成本以微秒计。

预算的规模估算在 CPU 上进行，此时 GPU 仍在处理上一步，输入是一个滞后一步的双缓冲置信度数组。把这 *B* 个槽位分配给各个请求则在 GPU 上针对当前值执行，因此每请求的分配使用的是当前置信度。该选择用 PyTorch 编写，由 `torch.compile` 降级为 Triton，并且从不回读到主机。

## 变长解码 CUDA Graph

要正确支持大小可变的验证，我们还需要变长（varlen）解码 CUDA Graph。这需要注意力内核的支持：稀疏 MLA 内核天然是变长的，因为每个 query token 都有独立的 top-k，而且 DeepSeek 在 [DeepGEMM](https://github.com/deepseek-ai/DeepGEMM) 中开源了一个 varlen indexer 内核，已作为 [PR #47808](https://github.com/vllm-project/vllm/pull/47808) 的一部分集成。解码图以 `num_reqs = min(num_tokens, max_num_seqs)` 捕获，并承诺 `max_query_len = num_speculative_tokens + 1`，因此一张图即可服务每请求 1 到 `num_speculative_tokens + 1` 个 token 的任意组合。

## 成本模型

预算规则要除以一个步成本，因此该成本必须查询起来足够便宜，并且能很好地近似真实成本。启动时，引擎对一组固定的形状（CUDA Graph 形状，再加上几个超过最大 cudagraph 尺寸的形状）计时运行虚拟步骤，每个形状取五次运行的中位数。这就得到两张扁平查找表：验证表以 token 数为索引，草稿表以请求数为索引，因为无论验证多少 token，草稿的成本都相同。两者相加。

![Measured verify and draft cost curves against the lookup tables](https://vllm.ai/blog-assets/figures/2026-08-14-dspark-adaptive-verification/fig2-costcurve.svg)

实测的验证与草稿成本曲线与查找表的对比

*图 2. 来自一次真实启动剖析的两张成本表，成本为 5 次采样的中位数。*

在捕获的 CUDA Graph 内部，成本是一段阶梯而非一条直线，这是 cudagraph 填充导致的：121 个 token 的批次会运行 128-token 的图，并（基本上）为全部 128 个 token 付费。超过捕获上限后，阶梯结束，成本才是真正连续的。在跌出 cudagraph 区域的地方有一个明显的跳变，这一转变在成本曲线中足够陡峭，会强烈地促使预算算法留在 cudagraph 区域之内。

剖析噪声通过强制曲线单调来处理。由于内核 tile 尺寸的原因，步成本确实可能随批次增大而下降，因此强制单调性有助于平滑成本曲线。步骤剖析基于一个合成的 KV 上下文，默认为 8192 个 token，可通过 `VLLM_ADAPTIVE_VERIFICATION_PROFILE_CONTEXT_LEN` 调节。

## 结果

DeepSeek-V4-Pro-0813，TP=8，运行在 8×B300（SM100）上，专家并行，FP8 KV 缓存，`max_model_len` 16384，`max_cudagraph_capture_size` 4096，vLLM `main` 分支 `73b8394`。基准测试为 880 条提示，temperature 1.0，输出最多 2048 个 token，并发从 1 到 256 扫描。

![Aggregate throughput against interactivity for adaptive and fixed speculation lengths](https://vllm.ai/blog-assets/figures/2026-08-14-dspark-adaptive-verification/fig3-pareto.svg)

自适应与固定投机长度下总吞吐量与交互性的关系

*图 3. 不同投机方案的吞吐量与交互性对比；自适应验证全程保持在帕累托前沿之上。*

在整个扫描范围内，自适应验证都处在帕累托曲线的边缘，且在两端都明显优于不投机。效果很容易从图上读出：它在低并发时表现得像一个长的固定块，在高并发时像一个短的固定块，无需事先了解工作负载的形态就能同时兼得两者。

## 局限性

- FULL 变长解码图要求 `AttentionCGSupport.ALWAYS`，DSV4 的 sparse-MLA、sparse-SWA 与 indexer 后端在 SM100 上均报告支持。在其他环境下，自适应验证会在启动时被拒绝，而不是回退到 PIECEWISE。
- `--enforce-eager`（步成本是从捕获的图中剖析出来的）、LoRA 和流水线并行目前均不支持。
- 自适应验证开启时会拒绝输出 logprobs，因为验证在前向传播之后会对 logits 进行压缩。

## 附录：复现

以下所有命令均使用 [PR #47808](https://github.com/vllm-project/vllm/pull/47808)，现已合并入 vLLM `main`；上面的数字是在 `73b8394` 上测得的。

**服务端**（所有测量；消融实验为 `--speculative-config` 的差异）：

```
vllm serve deepseek-ai/DeepSeek-V4-Pro-0813 \
  --tokenizer-mode deepseek_v4 --trust-remote-code \
  --tensor-parallel-size 8 --enable-expert-parallel \
  --kv-cache-dtype fp8 --max-model-len 16384 --max-num-seqs 256 \
  --max-num-batched-tokens 16384 --gpu-memory-utilization 0.8 \
  --compilation-config '{"max_cudagraph_capture_size":4096}' \
  --speculative-config '{"method":"dspark","attention_backend":"FLASH_ATTN","num_speculative_tokens":7,"draft_sample_method":"probabilistic","enable_adaptive_verification":true}'
```

草稿默认使用目标检查点，因此可以省略 `"model"`。`--kv-cache-dtype fp8` 是必需的：`fp8_ds_mla` 布局拒绝其他 KV dtype。`--max-num-seqs` 也很重要——默认值为 128，会把批次上限压到并发扫描的顶点之下。我们把 `max_cudagraph_capture_size` 提高到 `(num_speculative_tokens + 1) * max_num_seq`，以确保每个验证批次都落在 cudagraph 之内。更大的捕获尺寸需要更多 cudagraph 内存，因此使用 `--gpu-memory-utilization 0.8`；按默认值，捕获时会 OOM。

- 固定 k：`"enable_adaptive_verification": false`、`"num_speculative_tokens": k`，要求 k ≥ `dspark_block_size`（该检查点上为 5）
- 不投机：省略 `--speculative-config`

**吞吐量扫描**，并发 `c ∈ {1, 16, 32, 64, 128, 256}` 逐一进行，先跑一遍预热（`--speed-bench-output-len 256 --num-prompts 64 --max-concurrency 32`）：

```
MODEL=deepseek-ai/DeepSeek-V4-Pro-0813
for c in 256 128 64 32 16 1; do
  n=880; [ "$c" = 1 ] && n=240
  vllm bench serve \
    --backend openai-chat --base-url http://127.0.0.1:8000 \
    --endpoint /v1/chat/completions --model "$MODEL" \
    --tokenizer "$MODEL" --tokenizer-mode deepseek_v4 \
    --dataset-name speed_bench --dataset-path <speed-bench-dir> \
    --speed-bench-dataset-subset qualitative --speed-bench-output-len 2048 \
    --num-prompts $n --max-concurrency $c --request-rate inf \
    --skip-chat-template --disable-shuffle --temperature 1.0 --seed 0 \
    --save-result --result-filename adaptive_on_c${c}.json
done
```

`--disable-shuffle` 加上固定的提示集合，让每个实验组获得完全相同、顺序一致的提示；结果 JSON 中的 `output_throughput` 就是上面绘制的 tok/s。`--speed-bench-output-len` 是上限而非目标——请求会在 EOS 处停止，因此实际平均值远低于 2048。

## 致谢

这项工作由 Lucas Wilkinson（Red Hat）和 Benjamin Chislett（NVIDIA）完成。感谢 [DSpark](https://arxiv.org/abs/2607.05147) 的作者提供草稿算法与置信度头，感谢 DeepSeek 提供 DeepSeek-V4 检查点。
