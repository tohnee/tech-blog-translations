---
title: "为什么 Transformer LLM 使用多头注意力"
title_en: "Why Transformer LLMs Use Multi-Head Attention"
source: https://sebastianraschka.com/faq/docs/multi-head-attention.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么 Transformer LLM 使用多头注意力

基于 Transformer 的 LLM 使用**多头注意力（multi-head attention）**，让每个 token 能够同时形成多个相互独立的注意力分布。单个注意力头只产生一个关于其他 token 的分布。多个头让模型可以并行地比较和组合若干个这样的分布。

重要的是，这些头通常是对一个固定的投影宽度做切分。它们并不是整个注意力机制按完整宽度复制出的多份拷贝。

假设输入张量的形状为 (B \times T \times d\_{\text{model}})，其中 (B) 是批大小，(T) 是序列长度。在标准的多头注意力中，可学习的线性层把该输入投影为 query、key 和 value 张量。每个投影后的张量初始形状为

[
B \times T \times d\_{\text{model}}.
]

随后，实现会把每个张量重整（reshape）为

[
B \times H \times T \times d\_{\text{head}},
]

其中 (H) 是头的数量，且

[
d\_{\text{head}} = \frac{d\_{\text{model}}}{H}.
]

例如，一个 (d\_{\text{model}} = 4096)、有 32 个头的层会使用 (d\_{\text{head}} = 128)。query 投影仍然是 4,096 维宽，只是被重整为 32 个头，每个头 128 维。

![多头注意力对同一个输入序列应用多个注意力头。每个头使用各自独立的 query、key 和 value 投影。](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch03_compressed/24.webp)

在第 (h) 个头内部，缩放点积注意力为

[
\text{head}*h = \operatorname{softmax}\left(\frac{Q\_h K\_h^\top}{\sqrt{d*{\text{head}}}} + M\right)V\_h,
]

其中 (M) 是可选的掩码。GPT 风格的 LLM 使用因果掩码（causal mask），防止 token 关注未来的位置。关于这一掩码步骤，我在[什么是因果注意力，它是如何实现的？](https://sebastianraschka.com/faq/docs/causal-attention.html)中单独讨论。

每个头都有自己投影后的 query、key 和 value，因此它可以产生一个不同的 (T \times T) 注意力矩阵。这些头并不会被分配固定的职责，比如句法、格式化或长距离指代。这类模式可能在训练过程中涌现，但并无保证，而且有些头可能部分冗余。

注意力计算之后，每个头产生 (T \times d\_{\text{head}}) 的输出特征。实现会把各头的输出拼接（concatenate）起来，恢复出 (T \times d\_{\text{model}})，然后应用一个可学习的输出投影：

[
\operatorname{MultiHead}(X)
= \operatorname{Concat}(\text{head}\_1, \ldots, \text{head}\_H)W\_O.
]

这个输出投影很重要，因为它在结果进入残差连接和下一个 transformer 子层之前，混合了来自不同头的信息。

![一个高效的多头注意力实现会先计算较大的 query、key 和 value 投影，然后再把投影后的通道重整为各个独立的头。](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch03_compressed/26.webp)

在模型宽度固定的情况下，多头注意力并不会让 query、key 和 value 的参数量乘上头的数量。经典实现为 query、key、value 和输出投影各使用一个 (d\_{\text{model}} \times d\_{\text{model}}) 矩阵，与一个完整宽度的单头实现类似。各个头决定的是投影后的通道如何被划分以用于注意力计算。

主要的注意力计算量也仍然与 (T^2 d\_{\text{model}}) 成正比。注意力计算有 (H) 次，但每次只使用 (d\_{\text{head}} = d\_{\text{model}}/H) 个特征。基础实现确实会创建 (H) 个独立的 (T \times T) 注意力权重矩阵，这会带来额外的内存开销。优化过的内核可以减少必须存储的中间数据量。

头更多并不总是更好。增大 (H) 会让每个头更窄，而非常小的头维度会限制单个头所能表示的内容。额外的头也可能增加实现开销。因此，头的数量和头的维度是架构选择，必须与模型宽度相权衡。

标准的多头注意力通常缩写为 **MHA**，它使用相同数量的 query、key 和 value 头。较新的 LLM 有时会保留很多 query 头，同时共享更少的 key 和 value 头：

- MHA 使用 (H) 个 query 头和 (H) 个 key-value 头。
- 分组查询注意力（GQA）使用 (H) 个 query 头和更少的 key-value 头。
- 多查询注意力（MQA）使用 (H) 个 query 头和 1 个 key-value 头。

这些变体在减少自回归生成期间所使用的 key-value 缓存的同时，保留了多个依赖于 query 的注意力分布。相关差异在[什么是分组查询注意力，为什么 LLM 要使用它？](https://sebastianraschka.com/faq/docs/grouped-query-attention.html)中有详细解释。

简而言之，多头注意力让 transformer 拥有多种在 token 之间传递信息的独立途径，同时保持总投影宽度不变。随后的拼接和输出投影再把这些途径组合成一个表示，传递给 transformer 块的其余部分。
