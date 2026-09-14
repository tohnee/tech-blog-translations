---
title: "什么是 KV 缓存，它为什么能让 LLM 推理更快？"
title_en: "What is a KV cache, and why does it make LLM inference faster?"
source: https://sebastianraschka.com/faq/docs/kv-cache.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 什么是 KV 缓存，它为什么能让 LLM 推理更快？

**KV 缓存**保存每个注意力层为自回归序列中已有 token 生成的键张量和值张量。有了缓存，模型就可以复用这种逐层专属的状态，而不必在每个新 token 之后重算完整前缀。

考虑提示 `"Time flies"`。在**预填充**阶段，模型处理两个提示 token，并在每个产生缓存的层存储它们的键和值。最终的提示表示产生下一个 token 的 logits。

![预填充为提示 token 计算键向量和值向量，并在每个注意力层存储一对](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/kv-cache/kv-cache-attn-1.png)

假设解码规则选出了 `"fast"`。在下一次模型调用中，输入可以只有这个新 token，再加上 `"Time flies"` 的缓存。每层为 `"fast"` 计算查询、键和值。它的查询关注缓存的键值加上这一对新键值，而新的键和值被追加到缓存中。得到的 logits 预测 `"fast"` 之后的 token。

![追加新 token 时，更早的键值对保持不变，因此只需计算新的一对](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/kv-cache/kv-cache-attn-2.png)

如果没有缓存，第二次调用就得把 `"Time flies fast"` 整个重新送入模型。`"Time"` 和 `"flies"` 的隐藏状态和注意力投影会重复预填充阶段的工作。同样的冗余在之后的每一步都会累积。

![无缓存路径重算前缀，而缓存路径取出更早的键值，再用最新的 token 加以扩展](https://sebastianraschka.com/images/blog/2025/coding-the-kv-cache-in-llms/8.png)

不断增长的缓存中通常不包含查询。查询表示的是当前步骤正在计算其注意力输出的那个 token。未来的 token 需要更早的键和值作为可关注的内容，但它们不会复用更早的查询。

加速是有边界的。在完整注意力层中，新查询仍然要与所有保留的键和值交互。缓存消除的是重复的前缀投影和对更早 token 状态的重复处理。它并没有消除对保留前缀的注意力计算和内存流量。这部分剩余成本在长上下文下会变得很重要。

一个基础实现会在每个注意力块中保存 `cache_k` 和 `cache_v` 张量。这些张量带有一个随解码推进而增长的序列维度。实现还需要跟踪绝对缓存位置，以便因果掩码和位置编码（例如 RoPE）能与已存储的前缀对齐。

![从零实现加入了逐层缓存缓冲区，追加最新的键值，并跟踪当前缓存位置](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/kv-cache/new-sections.png)

相互独立的生成请求通常从空缓存开始，因为它们的前缀各不相同。服务系统可以复用完全相同共享提示的缓存状态，但前提是模型、分词、位置和前缀 token 全部匹配。

KV 缓存主要是一种推理优化。在因果语言模型训练期间，已知的序列各位置在一次带掩码的前向传播中一起处理，而且训练需要激活值来做反向传播。并不存在可供消除的逐 token 重复前缀求值。

代价则是内存。每个保留的 token 都会为每条活跃序列的相关层和 KV 头增加状态。[长上下文 KV 缓存 FAQ](https://sebastianraschka.com/faq/docs/kv-cache-long-context-bottleneck.html) 给出了内存公式和一份具体的 Qwen3 8B 计算。
