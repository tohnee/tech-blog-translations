---
title: "每 token KV 缓存（bf16）"
title_en: "KV Cache / Token (bf16)"
source: https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/
crawled: 2026-09-06
translated: 2026-09-06
---

# 每 token KV 缓存（bf16）

> 原文：[KV Cache / Token (bf16)](https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/)

KV 缓存的数字很容易比错。例如，Qwen3 8B 标注的 `144 KiB` 指的是一个 token 在单条序列中新增的逻辑缓存。画廊使用 bf16（[16 位 bfloat](https://en.wikipedia.org/wiki/Bfloat16_floating-point_format)），因此每个缓存元素占 2 字节。

在自回归生成过程中，注意力层会复用较早 token 的 key 和 value。保留这些张量可以避免在每个解码步骤重新计算。prompt token 在 prefill 阶段填充缓存，每个解码出的 token 再追加一个条目。

我选择按 token 的数值，是因为它能让注意力堆栈差异很大的架构在一张卡片上具有可比性。由于分配器填充、服务缓冲区以及特定 kernel 的布局，实际运行时内存通常更高。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[内存计算器](https://sebastianraschka.com/llm-architecture-gallery/memory-calculator/)
[GQA](https://sebastianraschka.com/llm-architecture-gallery/gqa/)
[MLA](https://sebastianraschka.com/llm-architecture-gallery/mla/)
[混合注意力](https://sebastianraschka.com/llm-architecture-gallery/hybrid-attention/)

含义

一个被保留的 token 新增的逻辑缓存

固定假设

批次大小为 1，bf16，每个缓存元素 2 字节

重要注意事项

这是逻辑上的架构估算，与实测的服务内存是两回事

## 从单个注意力层开始

这个计算最一般的形式是：

```python
bytes_per_layer_per_token
= cached_tensors × num_kv_heads × head_dim × bytes_per_element
```

标准注意力存储一个 key 张量和一个 value 张量，因此 `cached_tensors = 2`。在 bf16 下，公式变为：

```python
bytes_per_layer_per_token
= 2 × num_kv_heads × head_dim × 2
= 4 × num_kv_heads × head_dim
```

query 头数量通过注意力类型间接进入计算。多头注意力（MHA）每个 query 头对应一个 KV 头；分组查询注意力（GQA）使用更少的 KV 头；多查询注意力（MQA）只用一个。这正是 GQA 和 MQA 能在不改变 query 头数量的情况下减小缓存的原因。

对于模型级别的数值，我把每个产生缓存张量的不同层的贡献加总起来：

```python
bytes_per_model_per_token
= sum(bytes_per_layer_per_token across cache-producing layers)
```

![float32、float16 与 bfloat16 位布局对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/kv-cache-precision.webp)

**图 1.** Bfloat16 每个元素使用 16 位，与 float16 存储大小相同。其指数占 8 位，尾数占 7 位。画廊对每个缓存的 bf16 值按 2 字节计。

## 保留策略与共享作用于不同因素

滑动窗口注意力对每个所存 token 的开销与其底层的 MHA、GQA 或 MQA 层相同；它改变的是一个 token 在缓存中停留多久。窗口填满后，新条目到来时即可移除旧条目。

跨层 KV 共享改变的是产生缓存的不同层的数量。复用较早层 key 和 value 的层不会再追加一对张量。[Gemma 4 E2B 与 E4B 模型](https://sebastianraschka.com/llm-architecture-gallery/kv-sharing/)采用了这种方式。

当每一轮循环都保留自己的缓存时，循环深度需要一个额外的循环次数因子。[Ouro-Thinking 2.6B](https://huggingface.co/ByteDance/Ouro-2.6B-Thinking/blob/main/modeling_ouro.py) 将其四次执行中的每一轮映射为共享的 48 层堆栈上各自独立的缓存条目：

```python
4 passes × 48 layers × 16 KV heads × 128 head_dim × 4
= 1,572,864 bytes
= 1.5 MiB per token
```

Ouro 论文还评估了解码时只保留一轮的缓存复用，这会把上述逻辑增长降到 `384 KiB/token`。公开发布的 Hugging Face 实现默认保留完整的四轮缓存。

统一的 key 和 value 会把张量数从 2 变成 1：

```python
bytes_per_layer_per_token
= num_kv_heads × head_dim × 2
= 2 × num_kv_heads × head_dim
```

Gemma 4 的全局全注意力层使用统一的 `K=V`。这些层还有自己的 `global_head_dim`，因此我把它们的贡献与滑动窗口层分开计算。GQA、保留窗口、跨层共享与统一 `K=V` 各自描述的是缓存计算的不同部分。

## MLA 存储压缩后的潜在表示

多头潜在注意力（MLA）保留一个压缩的 KV 潜在表示以及一个单独的旋转 key 分量。对于 DeepSeek 风格的 MLA，画廊使用该架构所描述的紧凑表示：

每个 MLA 层：

```python
bytes_per_layer_per_token
= (kv_lora_rank + qk_rope_head_dim) × 2
```

在整个模型上，即：

```python
bytes_per_model_per_token
= num_mla_layers × (kv_lora_rank + qk_rope_head_dim) × 2
```

此时缓存取决于潜在维度和 MLA 层数，query 头数量不再出现在这个紧凑公式中。如果服务端实现把潜在表示展开成完整的 key 和 value 张量，内存占用就会不一样。

## 混合架构需要逐层盘点

混合模型正是单一层数会误导人的地方。我只统计那些向不断增长的 KV 缓存追加条目的层。

- Qwen3-Next 与 Qwen3.5 通过其全注意力层贡献缓存。
- Kimi Linear 与 Ling 2.5/2.6 通过主解码器中的 MLA 层贡献缓存；Ling 2.6 的可选 MTP 路径在使用时会增加一小块 MLA 缓存。
- Nemotron 混合架构通过其显式 GQA 层贡献缓存。
- DeltaNet、Lightning Attention、Mamba-2 与 xLSTM 层对不断增长的 KV 缓存贡献 `0 B/token`。

最后一组仍然需要推理状态。其状态大小相对序列长度是固定的，因此我把它排除在衡量每 token 增长的指标之外。

```python
sum(per-layer cache growth over the cache-growing layers only)
```

## 与已发布配置的核对

我用对应的配置文件核对了画廊中的数值。下面的例子覆盖了上文的主要情形。

[Qwen3 8B](https://huggingface.co/Qwen/Qwen3-8B/blob/main/config.json) 有 36 个 GQA 层、8 个 KV 头，头维度为 128：

```python
36 layers × 8 KV heads × 128 head_dim × 4
= 147,456 bytes
= 144 KiB
```

[DeepSeek V3](https://huggingface.co/deepseek-ai/DeepSeek-V3/blob/main/config.json) 有 61 个 MLA 层，KV 潜在秩为 512，旋转 key 分量为 64 维：

```python
61 layers × (512 kv_lora_rank + 64 qk_rope_head_dim) × 2
= 70,272 bytes
= 68.6 KiB
```

[Qwen3-Next 80B-A3B](https://huggingface.co/Qwen/Qwen3-Next-80B-A3B-Instruct/blob/main/config.json) 有 48 个解码器层，每四层出现一次全注意力。进入不断增长的 KV 缓存计算的只有 12 层：

```python
12 full-attention layers × 2 KV heads × 256 head_dim × 4
= 24,576 bytes
= 24 KiB
```

[Gemma 4 31B](https://huggingface.co/google/gemma-4-31B-it/blob/main/config.json) 有 50 个滑动窗口层和 10 个全局层。全局层使用统一 `K=V` 和四个 512 维 KV 头：

```python
50 sliding-window layers × 16 KV heads × 256 head_dim × 4
+ 10 global layers × 4 KV heads × 512 global_head_dim × 2
= 819,200 + 40,960 bytes
= 860,160 bytes
= 840 KiB
```

同样的计算对 [Gemma 4 26B-A4B](https://huggingface.co/google/gemma-4-26B-A4B-it/blob/main/config.json) 得到 `210 KiB`，对 [Gemma 4 12B](https://huggingface.co/google/gemma-4-12B-it/blob/main/config.json) 得到 `328 KiB`。[xLSTM 7B](https://arxiv.org/abs/2503.13427) 没有注意力层，因此其不断增长的 KV 缓存值为 `0 B/token`；它的循环矩阵状态仍然存在。

## 从一个 token 到整个上下文

对全注意力模型，把画廊数值乘以保留的 token 数即可。在 32,768 个 token 时，Qwen3 8B 的 `144 KiB/token` 对应批次大小为 1 时的 `4.5 GiB` 逻辑 bf16 KV 缓存。

混合堆栈则需要逐层形式，因为不同层保留的 token 数可能不同：

```python
total_cache_bytes
= sum(bytes_per_layer_per_token × retained_tokens_for_that_layer)
```

更大的批次会为每个活跃序列追加一份缓存。分页服务、填充、缓存量化与临时缓冲区都可能使实测内存高于或低于简单的 bf16 估算。这就是为什么画廊字段最好被理解为架构对比数值。

## 画廊分档

画廊和模型对比工具给每个数值附上一个粗略标签：

- `0 B` -> `No cache`
- `> 0` 和 `<= 24 KiB` -> `Very low`
- `> 24 KiB` 和 `<= 72 KiB` -> `Low`
- `> 72 KiB` 和 `<= 160 KiB` -> `Moderate`
- `> 160 KiB` 和 `<= 300 KiB` -> `High`
- `> 300 KiB` -> `Very high`

这些标签只用于快速浏览，计算请使用数值本身。

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
