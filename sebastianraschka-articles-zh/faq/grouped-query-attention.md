---
title: "现代大语言模型中的分组查询注意力（GQA）"
title_en: "Grouped-Query Attention (GQA) in Modern LLMs"
source: https://sebastianraschka.com/faq/docs/grouped-query-attention.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 现代大语言模型中的分组查询注意力（GQA）

**分组查询注意力（GQA）**保留了常规数量的查询头，但使用更少的键头和值头。因此若干个查询头会读取同一组键值对。这减小了 KV 缓存的规模，也减少了自回归生成过程中必须读取的缓存数据量。

从头的数量上看，GQA 位于两个熟悉的端点之间。标准的多头注意力（MHA）使用相同数量的查询头和键值头。多查询注意力（MQA）使用大量查询头但只有单个键值头。GQA 则使用多于一个键值头，但键值头数量少于查询头数量。

例如，某一层可能有 32 个查询头和 8 个键值头。每个键值头由一组 4 个查询头共享。查询保持彼此独立，因此每个头仍能形成自己的注意力权重。

![分组查询注意力示意：四个查询头和两个键值头，每对键值服务于一组两个查询头](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gqa-memory/1.webp)

缓存节省量直接取决于键值头的数量。对于一层和被保留的一个 token，标准注意力缓存要为每个 KV 头存储一个键和一个值：

`cache bytes = 2 x KV heads x head dimension x bytes per element`

在 bf16 数值、8 个 KV 头、头维度为 128 的情况下，这是每层每 token 4,096 字节。Qwen3 8B 有 36 个这样的层，因此每保留一个 token，逻辑 bf16 KV 缓存增长 144 KiB。一个拥有 32 个 KV 头、维度相同的 MHA 版本则需要四倍的缓存。

这在解码阶段影响最大。每个生成的 token 都会向缓存追加键和值，后续解码步骤则要读取这些已存储的张量。内存需求随上下文长度和批大小增长，而读取更小的缓存还可以缓解内存带宽压力——在逐 token 生成中，这往往是一个实际瓶颈。

![KV 缓存对比图：减少键值头数量如何降低保留上下文变长时的内存增长](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/gqa-memory/3.webp)

GQA 对保留的序列仍然执行完整注意力。它不会缩短上下文，不会让注意力矩阵变稀疏，也不会消除完整注意力对序列长度的依赖。[滑动窗口注意力](https://sebastianraschka.com/faq/docs/when-gqa-and-swa.html)改变的是有多少更早的 token 仍然可用，因此它针对的是成本问题的另一部分。

为什么停在 MHA 和 MQA 之间？把同一个键值头共享给所有查询头能带来最大的缓存缩减，但也会损失更多各头专属的键值容量。2023 年的原始 [GQA 论文](https://arxiv.org/abs/2305.13245)发现，在其评估的设置中，中间程度的分组可以接近 MHA 的质量，同时保留 MQA 推理收益的大部分。具体的权衡取决于模型和训练方案。

Llama 3 8B、Qwen3 8B 和 Gemma 3 27B 都是使用 GQA 的模型示例。它们的查询头与 KV 头之比各不相同，但机制是一样的：多个查询头在共享一小组缓存键值的同时，保留各自独立的注意力模式。
