---
title: "位置信息在基于 Transformer 的 LLM 中起什么作用？"
title_en: "What role does positional information play in a transformer-based LLM?"
source: https://sebastianraschka.com/faq/docs/positional-information-transformer.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 位置信息在基于 Transformer 的 LLM 中起什么作用？

位置信息让 transformer 能够区分不同序列位置上的相同 token 内容，并表达顺序、方向和距离。这些区分很重要，因为"dog bites man"（狗咬人）和"man bites dog"（人咬狗）包含同样的三个 token，却表达不同的事件。

问题的实质在于：不带任何位置相关输入的、普通的未掩码自注意力是**置换等变（permutation-equivariant）**的。如果输入 token 被重新排列，输出表示也会以同样的方式被重排。注意力可以比较 token 的内容，但它没有一个坐标能说明某个 token 出现在另一个之前，或两个 token 相距三个位置。

这有时被描述为置换不变性（permutation invariance），不过等变性才是更准确的说法。输入被重新排序时，序列输出依然会被重新排序，缺失的是对这种顺序含义的敏感性。

token 嵌入查表可以说明这个问题。"dog"的 token ID 无论出现在位置 1 还是位置 100，都映射到同一个向量。重复出现的 token 也都从同一个 token 向量出发。位置机制为网络提供了区分这些情形的额外信息。

![A token embedding identifies token content but does not, by itself, identify the token's sequence position.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch02_compressed/17.webp)

代码仓库中实现的小型 GPT 风格模型使用**可学习的绝对位置嵌入**。对于位置 (t) 上的 token (x\_t)，transformer 的输入为

[
z\_t = E\_{\text{token}}(x\_t) + E\_{\text{position}}(t).
]

token 表提供内容，位置表则为索引 (t) 提供一个学习到的向量。两个向量宽度相同，在进入第一个 transformer 块之前相加。

![The GPT-style input adds one learned position vector to each token embedding.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch02_compressed/18.webp)

绝对嵌入易于检查和实现。但可学习表也带来了硬性的架构限制，因为它只包含固定数量的位置行。扩展这张表会引入未经训练的位置。原始 Transformer 使用的固定正弦编码避免了可学习查表，但仍在输入端加上一个与绝对位置相关的向量。

现代 LLM 还使用其他几种方法：

- **旋转位置嵌入（RoPE）**按位置决定的角度旋转查询和键的通道对。由此得到的查询-键点积取决于 token 之间的相对偏移。
- **相对位置偏置**根据查询与键之间的距离和方向，向注意力得分添加一个可学习或固定的项。T5 风格的分桶偏置和 ALiBi 是两个例子。
- **部分或混合方案**只对部分通道或部分层应用某种位置方法。因此不同的注意力层可以使用不同的位置处理方式。
- **NoPE**在选定的注意力层中省略显式的位置嵌入、旋转或偏置。

RoPE 在结构上不同于 GPT 风格的做法，因为它并不在残差流输入上叠加位置向量，而是在注意力内部修改查询和键。这既让注意力直接获得相对偏移的表示，又在旋转后的向量中保留了绝对相位信息。[什么是 RoPE，为什么许多模型放弃了可学习的绝对位置嵌入？](https://sebastianraschka.com/faq/docs/rope-vs-absolute-positional-embeddings.html)更详细地介绍了这一机制。

这些方法在超出训练时见过的上下文长度之外的表现也不相同。从技术上讲，模型可以在更大的位置索引上求 RoPE 的值，但良好的长上下文行为并不会自动获得。RoPE 缩放、插值、额外训练以及频率配置都可能起作用。相对偏置有其自身的外推行为，而可学习的绝对位置表则必须被扩容或另行适配。

纯解码器 LLM 还有一个重要的细微之处。它们的[因果注意力掩码](https://sebastianraschka.com/faq/docs/causal-attention.html)本身已提供了一种有方向的结构信号。位置 (t) 只能看到不超过 (t) 的位置，因此不同位置拥有不同的可见前缀。这打破了未掩码注意力的完全置换对称性，也解释了因果模型为何能在没有显式位置嵌入的情况下学到一些顺序信息。

NoPE 正是利用了这一观察。NoPE 注意力层既不接收绝对嵌入，也不应用 RoPE 或显式相对偏置，而因果掩码依然保留。模型可以从这种嵌套的前缀结构中学习，尽管它没有用于精确位置或距离的直接坐标。一些新近的架构会混合使用 RoPE 层和 NoPE 层，而不是全程只用一种方案。[NoPE 图集讲解](https://sebastianraschka.com/llm-architecture-gallery/nope/)讨论了这种设置以及关于长度泛化的现有证据。

位置处理在生成的实现中同样重要。每个新解码的 token 都需要下一个位置索引，缓存中的键和值必须保留它们创建时所用的位置处理方式。具有不同填充或缓存长度的批量序列需要一致的位置 ID。一个索引错误可能产生看似合法的张量形状，却悄然改变注意力之间的关系。

因此，位置信息告诉 transformer token 之间的关系如何依赖于序列位置。具体架构可能添加向量、旋转注意力特征、给注意力得分加偏置，或部分依赖因果结构。正确的描述取决于具体模型，而不能只看模型家族的名称。
