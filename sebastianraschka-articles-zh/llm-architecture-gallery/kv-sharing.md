---
title: "跨层 KV 共享"
title_en: "Cross-Layer KV Sharing"
source: https://sebastianraschka.com/llm-architecture-gallery/kv-sharing/
crawled: 2026-09-06
translated: 2026-09-06
---

# 跨层 KV 共享

> 原文：[Cross-Layer KV Sharing](https://sebastianraschka.com/llm-architecture-gallery/kv-sharing/)

跨层 KV 共享是一种共享 KV 缓存的方案：较后的层复用较早层的键值状态。这可以降低长上下文下的内存和计算开销，因为向缓存写入自己键值的层数变少了。

这个 KV 共享的想法并非 Gemma 4 首创。例如，可参见 Brandon 等人的《[*Reducing Transformer Key-Value Cache Size with Cross-Layer Attention*](https://arxiv.org/abs/2405.12981)》（NeurIPS 2024）。但 Gemma 4 是我见到的第一个把这一概念付诸应用的主流架构。（跨层注意力不要与交叉注意力（cross-attention）混淆。）

[分组查询注意力（GQA）](https://sebastianraschka.com/llm-architecture-gallery/gqa/)已经在不同查询头之间共享键值头了，而跨层 KV 共享则是把这种共享应用到了 transformer 层之间。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[从零实现代码](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/10_kv-sharing)
[KV 缓存计算](https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/)

![Gemma 4 中的跨层 KV 共享](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gemma4-kv-sharing.webp)

跨层 KV 共享让查询投影保持在各层内部，同时复用由特定"生产者"层
输出的 K/V 张量。缓存只随生产者层的数量增长，从而降低长上下文的内存占用（原始出处：
[*LLMs-from-scratch* KV-sharing 材料](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/10_kv-sharing)。）

变化点

只有被选中的层才会为缓存生成新的键张量和值张量

实际收益

它能与 MQA 或 GQA 叠加使用，因为它减少了产生缓存的层数

示例架构

[Gemma 4 E2B](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-4-e2b) 和
[Gemma 4 E4B](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-4-e4b)

## 为什么要减小 KV 缓存？

在进一步解释 KV 共享之前，先简单谈谈动机。近段时间大语言模型架构设计的一个主要主题就是减小 KV 缓存大小。而减小 KV 缓存大小的动机，是降低所需内存，从而让我们能够处理更长的上下文。更多背景可参见我的《[Understanding and Coding the KV Cache in LLMs from Scratch](https://magazine.sebastianraschka.com/p/coding-the-kv-cache-in-llms)》一文。

举一个经典例子（Gemma 4 仍在使用）：GQA 已经通过在不同查询头之间共享键值头来减小 KV 缓存大小。多查询注意力（MQA）则是 GQA 只有一个 KV 头的特例。

在带 KV 缓存的常规注意力中，每个注意力层都会为每个生成的 token 存储一个键张量和一个值张量。跨层 KV 共享改变的是这个算式里的层数：不再为每一层缓存 K/V 张量，只有生产 K/V 的层才向缓存写入条目。

标准 KV 缓存：

```python
bytes = batch_size x seqlen x head_dim x n_kv_heads x n_layers x 2 x bytes_per_elem
```

采用跨层 KV 共享后：

```python
bytes = batch_size x seqlen x head_dim x n_kv_heads x n_kv_producing_layers x 2 x bytes_per_elem
```

transformer 层的其余部分依然存在，第二个算式只是把总层数替换成了产生新键值的层数。

## Gemma 4 如何应用 KV 共享

如前所述，Gemma 4 使用 GQA。不过，除了作为 GQA 一部分在查询之间共享 KV 之外，Gemma 4 还在不同层之间共享 KV 投影，而不是在每一层的注意力模块中都重新计算它们。这种 KV 共享方案也被称为跨层注意力（cross-layer attention）。

在 GQA（或 MQA）情形下，KV 共享是这样工作的：较后的层不再计算自己的键值投影，而是复用同一注意力类型中最近的较早非共享层的 KV 张量。换言之，滑动窗口层与之前的滑动窗口层共享 KV；全注意力层与之前的全注意力层共享 KV。这些层仍然计算自己的查询投影，因此每层都能形成自己的注意力模式，但昂贵且占内存的 KV 缓存却在多个层之间被复用了。

举例来说，Gemma 4 E2B 有 35 个 transformer 层，但只有前 15 层计算自己的 KV 投影；最后 20 层复用同一注意力类型中最近的较早非共享层的 KV 张量。类似地，Gemma 4 E4B 有 42 层，其中 24 层计算自己的 KV，最后 18 层共享它们。

这实际上能省多少？由于 Gemma 4 大约有一半的 KV 跨层共享，它能在应用 MQA 或 GQA 之后剩下的缓存中再省掉大约一半。对 E2B 来说，在 bfloat16 精度和 128k 上下文下约为 2.7 GB；对 E4B 约为 6 GB。

下面的图表展示了相对于 MHA 基线的合计节省。在 128k 上下文和批量大小为 1 时，类 E2B 配置从 MHA 的 37.58 GB 降到 MQA 加 KV 共享的 2.01 GB；类 E4B 配置从 MHA 的 56.37 GB 降到 GQA 加 KV 共享的 8.05 GB。这些图表尚未包含滑动窗口注意力保留策略带来的额外节省。

![类 Gemma 4 E2B 配置的 KV 缓存内存对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/kv-sharing-gemma4-e2b-memory.webp)

在类 E2B 配置中，1 个 KV 头和 15 个生产 K/V 的层把 128k token 下的全上下文缓存
从 37.58 GB 的 MHA 基线降到 2.01 GB，这还未计入滑动窗口保留策略的节省
（原始出处：[*LLMs-from-scratch* KV-sharing 材料](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/10_kv-sharing)。）

![类 Gemma 4 E4B 配置的 KV 缓存内存对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/kv-sharing-gemma4-e4b-memory.webp)

在类 E4B 配置中，2 个 KV 头和 24 个生产 K/V 的层把 128k token 下的全上下文缓存
从 56.37 GB 的 MHA 基线降到 8.05 GB，这还未计入滑动窗口保留策略的节省
（原始出处：[*LLMs-from-scratch* KV-sharing 材料](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/10_kv-sharing)。）

## 代价

KV 共享的缺点当然是：它是对"真东西"的一种近似，或者更准确地说，它降低了模型容量。现在有些层是通过复用的 K/V 张量来做注意力，而不是各层专属的 K/V 张量。

不过，[跨层注意力论文](https://arxiv.org/abs/2405.12981)报告称，对其测试的小型模型而言，这种影响可以非常小。Gemma 4 把这一想法与 MQA 或 GQA 以及滑动窗口注意力结合在一起，每种方法削减的是 KV 缓存成本的不同部分。

参考资料

[Brandon et al. (2024), *Reducing Transformer Key-Value Cache Size with Cross-Layer Attention*](https://arxiv.org/abs/2405.12981)
[LLMs-from-scratch KV-sharing 材料](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/10_kv-sharing)
[Gemma 4 模型卡](https://ai.google.dev/gemma/docs/core/model_card_4)
[KV 缓存 / token 画廊计算](https://sebastianraschka.com/llm-architecture-gallery/kv-cache-calculations/)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
