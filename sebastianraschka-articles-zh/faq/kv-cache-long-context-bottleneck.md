---
title: "为什么长上下文会让 KV 缓存成为内存瓶颈"
title_en: "Why Long Contexts Make the KV Cache a Memory Bottleneck"
source: https://sebastianraschka.com/faq/docs/kv-cache-long-context-bottleneck.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么长上下文会让 KV 缓存成为内存瓶颈

**KV 缓存**用内存换计算。在自回归生成期间，每个注意力层都会存储来自更早 token 的键向量和值向量。复用它们可以避免在每个解码步骤把完整前缀重新过一遍键和值投影。提示在预填充阶段填满缓存，之后每个生成的 token 再追加一条新条目。

![注意力在为当前 token 计算新查询的同时，复用来自更早 token 的缓存键和值](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/kv-cache/kv-cache-attn-1.png)

对于一个标准的注意力层，单个 token 新增的逻辑缓存为：

`2 x KV heads x head dimension x bytes per element`

因子 2 对应键张量和值张量。把这个量再乘上产生缓存的层数、保留的 token 数和活跃序列数。查询只为当前步骤计算，不会存入不断增长的缓存。

这一规模很快就会变得很大。Qwen3 8B 有 36 个 GQA 层，每层 8 个 KV 头，头维度为 128。在 bf16 数值下，它为每条序列的每个 token 增加 144 KiB 逻辑缓存。因此 32,768 个 token 的上下文要占用约 4.5 GiB。八条等长序列在计入分配器开销、临时缓冲区和其他服务状态之前，就需要约 36 GiB。

这与模型权重的内存不同。服务器可以在多个请求间共享同一份已加载的权重，而每条活跃序列都有自己独立的 KV 缓存。因此，更长的上下文和更大的连续批处理会减少同一加速器上能容纳的请求数。

缓存还会影响解码速度。在每一步，注意力都要读取保留的键和值，以便与新查询进行比较。更大的缓存增加了每个生成 token 的内存流量和注意力计算量。缓存避免了重算前缀，但长前缀并不是免费的。

![GQA 内存曲线展示了 KV 缓存随保留上下文长度的线性增长，以及减少 KV 头数量带来的降幅](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gqa-memory/3.webp)

若干优化方法分别削减计算式中的不同因子。[分组查询注意力](https://sebastianraschka.com/faq/docs/grouped-query-attention.html)和多查询注意力减少 KV 头的数量。低精度缓存降低每个元素的字节数。滑动窗口注意力或缓存淘汰限制保留的 token 数量。跨层 KV 共享减少产生独立缓存条目的层数，而多头潜在注意力（MLA）则存储压缩后的表示。

分页注意力（paged attention）等内存管理方法改善分配并减少碎片。它们帮助服务系统高效地打包请求，但对于给定序列，它们并不改变模型的逻辑缓存大小。

KV 缓存随保留的上下文长度线性增长。其他长上下文成本遵循不同的缩放规律。完整注意力的预填充阶段，其注意力计算量关于序列长度是二次的；而每生成一个新 token，解码注意力计算量随保留前缀线性增长。这些成本应当与缓存容量的计算分开度量。

[架构速览的计算页面](https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/)报告的是每个 token 的逻辑 bf16 缓存增长量，以便在同一口径下比较不同架构。实测的运行时内存可能有所不同，原因包括缓存量化、填充、分配器行为以及特定内核的内存布局。
