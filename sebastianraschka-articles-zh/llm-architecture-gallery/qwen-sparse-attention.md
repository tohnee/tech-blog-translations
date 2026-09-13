---
title: "Qwen 稀疏注意力"
title_en: "Qwen Sparse Attention"
source: https://sebastianraschka.com/llm-architecture-gallery/qwen-sparse-attention/
crawled: 2026-09-06
translated: 2026-09-06
---

# Qwen 稀疏注意力

> 原文：[Qwen Sparse Attention](https://sebastianraschka.com/llm-architecture-gallery/qwen-sparse-attention/)

Qwen 稀疏注意力（Qwen Sparse Attention，QSA）是一种受 [DeepSeek 稀疏注意力](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/)（DSA）中稀疏选择思想启发的注意力机制。与 DSA 类似，QSA 也使用一个可学习的索引器。但它不选择（或不学习去选择）单个 token，而是从可见前缀中选择完整的四 token 微块（micro-block）。因此在这里，QSA 会读取被选块中的每个 token，外加当前不完整块中的可见 token。

再强调一次，与 [DeepSeek 稀疏注意力](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/)的主要区别就在于选择单元——后者对单个 token 位置进行排序。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[模型卡](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)
[技术报告](https://github.com/QwenLM/Qwen3.8-Flash-Next/blob/main/tech_report.pdf)

![展示 Qwen 稀疏注意力与 Gated DeltaNet 层的 Qwen3.8-Flash-Next 架构](https://sebastianraschka.com/llm-architecture-gallery/images/architectures/qwen3-8-flash-next.webp)

图 1. Qwen3.8-Flash-Next 以 3:1 的编排使用 12 层 QSA 和 36 层 Gated DeltaNet。架构细节来自
[模型卡](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)和
[公开配置](https://huggingface.co/Qwen/Qwen3.8-Flash-Next/blob/main/config.json)。

选择单元

完整的四 token 微块

选择预算

最多 512 个块，即 2,048 个被选 token，外加当前不完整的块尾

示例架构

[Qwen3.8-Flash-Next 125B-A6B](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-8-flash-next-125b-a6b)

## 块选择的工作方式

QSA 的索引器把查询之前的键（因为它仍是自回归的）按 4 个 token 一组划分，并对每个完整块内的键取平均。接着对这些池化后的键做归一化，再施加 RoPE（使用每个块中的第一个位置），然后让它们与当前查询计算分数。得分最高的块会在主注意力运算之前被重新展开为它们的四个 token 位置。

```python
complete_blocks = group(visible_prefix, block_size=4)
block_keys      = mean(keys in each complete block)
scores          = sum(relu(query_head @ block_key) for each indexer head)
selected_blocks = top_k(scores, k=512)
attention_input = flatten(selected_blocks) + current_incomplete_block
```

如果预算是 2,048 个 token、每块 4 个 token，那么 QSA 最多可以选择 512 个完整块，因为 2,048/4 = 512。

## QSA 与 DeepSeek 稀疏注意力的对比

|  | Qwen 稀疏注意力 | DeepSeek 稀疏注意力 |
| --- | --- | --- |
| 选择单元 | 完整的四 token 块 | 单个 token 位置 |
| 2,048 token 预算 | 最多选中 512 个块 | 最多选中 2,048 个 token |
| 当前不完整块 | 直接包含 | 没有对应的块尾规则 |
| 选择模式 | 由当前查询学习得到 | 由当前查询学习得到 |

QSA 使用的索引更粗：选中一个相关 token 的同时，也会把它所在四 token 块中的其他 token 一并带入。DSA 则可以独立地选择 token 位置。

## QSA 在模型中的位置

最后来看一下它首次出现的那个模型，也就是 [Qwen3.8-Flash-Next](https://sebastianraschka.com/llm-architecture-gallery/#card-qwen3-8-flash-next-125b-a6b)：该模型共有 48 个 transformer 块，每组包含三个 [Gated DeltaNet](https://sebastianraschka.com/llm-architecture-gallery/hybrid-attention/) 层加一个 QSA 层，共 36 个循环层和 12 个稀疏注意力层。

这里要注意的关键点是：只有 QSA 层会向不断增长的 KV 缓存写入内容。但由于是稀疏选择，这比标准注意力更高效。也就是说，在 1M token 的给定上下文中，每个查询只会选中 2,048 个 token（与 DeepSeek 稀疏注意力类似，但使用了更高效的按块选择机制）。

参考资料

[Qwen3.8-Flash-Next 模型卡](https://huggingface.co/Qwen/Qwen3.8-Flash-Next)
[Qwen3.8-Flash-Next 配置](https://huggingface.co/Qwen/Qwen3.8-Flash-Next/blob/main/config.json)
[Qwen3.8-Flash-Next 技术报告](https://github.com/QwenLM/Qwen3.8-Flash-Next/blob/main/tech_report.pdf)
[Transformers QSA 实现](https://github.com/huggingface/transformers/blob/main/src/transformers/models/qwen4_exp/modeling_qwen4_exp.py#L622-L718)
[DeepSeek 稀疏注意力解读](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
