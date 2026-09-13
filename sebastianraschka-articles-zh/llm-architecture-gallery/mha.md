---
title: "多头注意力（MHA）"
title_en: "Multi-Head Attention (MHA)"
source: https://sebastianraschka.com/llm-architecture-gallery/mha/
crawled: 2026-09-06
translated: 2026-09-06
---

# 多头注意力（MHA）

> 原文：[Multi-Head Attention (MHA)](https://sebastianraschka.com/llm-architecture-gallery/mha/)

自注意力是大语言模型的"心脏"。它是一种让每个 token 评估自己与序列中其他每个 token（不包括未来 token）相关性的机制。多头注意力（MHA）则是在标准 transformer 架构中把多个注意力模块彼此并联堆叠起来的一种实现方式。也就是说，它以不同的可学习投影并行运行多个自注意力头，然后把它们的输出组合成一个更丰富的表示。

下面这一节是一场解释自注意力（进而解释 MHA）的速览。它更像是为分组查询注意力、滑动窗口注意力等相关注意力概念铺垫的快速概览。如果你想要更长、更细致的自注意力讲解，可以看看我那篇更长的《[Understanding and Coding Self-Attention, Multi-Head Attention, Causal-Attention, and Cross-Attention in LLMs](https://magazine.sebastianraschka.com/p/understanding-and-coding-self-attention)》。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[注意力文章](https://magazine.sebastianraschka.com/p/understanding-and-coding-self-attention)
[从零实现章节](https://sebastianraschka.com/llms-from-scratch/ch03/01_main-chapter-code/)

自注意力的动机

注意力最初是为了消除编码器-解码器 RNN 翻译模型中固定摘要的瓶颈而被引入的

从自注意力到 MHA

MHA 以不同的可学习投影并行运行多个自注意力头，并把它们的输出组合成一个表示

示例架构

[GPT-2 XL 1.5B](https://sebastianraschka.com/llm-architecture-gallery/#card-gpt-2-xl-1-5b)、
[OLMo 2 7B](https://sebastianraschka.com/llm-architecture-gallery/#card-olmo-2-7b) 和
[OLMo 3 7B](https://sebastianraschka.com/llm-architecture-gallery/#card-olmo-3-7b)

## 注意力为何被引入

注意力的出现早于 transformer 和 MHA。它的直接背景是用于翻译的编码器-解码器 RNN。

在那些较早的系统中，编码器 RNN 逐 token 读取源句子，把它压缩成一列隐藏状态；在最简单的版本里甚至压缩成单个最终状态。然后，解码器 RNN 必须从这个有限的摘要生成目标句子。这对简短、简单的情形是可行的，但一旦生成下一个输出词所需的信息位于输入句子的其他位置，就会形成一个明显的瓶颈。

简而言之，局限在于隐藏状态无法存储无限多的信息或上下文，而有时直接回看完整的输入序列会更有用。

下面的翻译示例展示了这种思路的一个局限。例如，一个译文可以在许多局部合理的选词上站得住脚，但只要模型把这个问题过分当作逐词映射来处理，它作为翻译仍然会失败。（上图展示了一个夸张的例子：我们逐词翻译这句话；显然，所得句子的语法是错误的。）
实际上，正确的下一个词取决于句子层面的结构，以及在这一步哪些较早的源词是重要的。当然，用 RNN 仍可能把它翻译好，但正如前面所说，由于隐藏状态只能存储有限的信息，它在更长序列或知识检索任务上会力不从心。

![激发注意力机制的句子翻译示例](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mha-motivation-translation.webp)

即使许多个别选词看起来合理，翻译仍可能失败，因为句子层面的结构
依然重要（原始出处：[*LLMs-from-scratch*](https://github.com/rasbt/LLMs-from-scratch)。）

因此，为了克服标准 RNN"一切都存进隐藏状态、模型无法在需要时访问原始输入"的局限，研究者们通过
《[*Neural Machine Translation by Jointly Learning to Align and Translate*](https://arxiv.org/abs/1409.0473)》引入了注意力机制。
要点是消除隐藏状态这一固定摘要的瓶颈：不再强迫解码器依赖对整个输入的单个压缩
摘要，注意力让它可以在每个输出步骤重新查看更相关的编码器状态，
构建一个针对该步骤的上下文向量。

在语言中，这一点很重要，因为我们想要的下一个词往往取决于源句中更早或更晚出现的内容，
而不仅仅是紧邻的前一个 token。

![展示旧式固定记忆瓶颈的编码器-解码器概览](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mha-motivation-encoder-decoder.webp)

旧式的编码器-解码器 RNN 设置必须把源句子挤过一条狭窄的隐藏状态通路，
解码器才能把它变成输出句子
（原始出处：[*LLMs-from-scratch*](https://github.com/rasbt/LLMs-from-scratch)。）

下一张图更直接地展示了这一变化。当解码器正在生成一个输出 token 时，它不应被限制在单条压缩记忆通路上，
而应能直接回溯到更相关的输入 token。

![允许输出 token 访问所有输入 token 的注意力机制](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mha-attention-revisits-input.webp)

注意力打破了 RNN 的瓶颈，让当前输出位置可以回看完整的输入序列，
而不必只依赖单个压缩状态（原始出处：
[*LLMs-from-scratch*](https://github.com/rasbt/LLMs-from-scratch)。）

transformer 保留了上述"加入注意力的 RNN"的核心思想，但去掉了循环。在这篇经典的
《[*Attention Is All You Need*](https://arxiv.org/abs/1706.03762)》论文中，
注意力本身成为主要的序列处理机制
（而不再只是 RNN 编码器-解码器的一部分）。

在 transformer 中，这种机制被称为自注意力：序列中的每个 token 对所有其他 token 计算一组权重，
并利用它们把这些 token 的信息混合进一个新的表示。多头注意力就是把同一个机制
并行运行多次。

## 带掩码的注意力矩阵

对于一个长度为
`T` 个 token 的序列，注意力需要为每个 token 提供一行权重，因此整体上我们得到一个 `T x T` 的矩阵。

每一行回答一个简单的问题：在更新这个 token 时，每个可见 token 应该占多大分量？在
仅解码器的 LLM 中，未来的位置会被掩码掉，这就是下图中矩阵右上部分呈灰色的原因。

自注意力从根本上说，就是在因果掩码约束下
学习这些 token 到 token 的权重模式，然后用它们构建具有上下文感知能力的 token
表示。

![带掩码的注意力矩阵：每个 token 只关注可见 token](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mha-masked-attention.webp)

一个具体的带掩码注意力矩阵：每一行属于一个 token，每个条目是一个注意力权重，
未来 token 的条目被因果掩码移除（原始出处：
[*Understanding and Coding Self-Attention*](https://magazine.sebastianraschka.com/p/understanding-and-coding-self-attention)。）

## 自注意力的内部机制

下一张图展示了 transformer 如何从输入嵌入 `X` 计算出注意力矩阵（`A`），
再用它生成变换后的输入（`Z`）。

这里的 `Q`、`K`、`V` 分别代表查询（queries）、键（keys）和值（values）。一个 token 的查询表示它在寻找什么，
键表示每个 token 为匹配提供什么，值则表示在注意力权重计算完成之后，
会被混合进输出的信息。

步骤如下：

- `Wq`、`Wk` 和 `Wv` 是把输入嵌入投影成 `Q`、`K` 和 `V` 的权重矩阵
- `QK^T` 生成原始的 token 到 token 相关性分数
- softmax 把这些分数转换成上一节讨论过的归一化注意力矩阵 `A`
- `A` 作用于 `V`，产生输出矩阵 `Z`

注意，注意力矩阵并不是一个单独手工构造的对象，它是从 `Q`、`K` 和 softmax 中自然产生的。

![X 被投影为 Q、K、V，再变换为注意力矩阵和输出的示意图](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/summary.webp)

完整的单头流程：从输入嵌入 X 到归一化注意力矩阵 A 再到输出
表示 Z（原始出处：
[*Understanding and Coding Self-Attention*](https://magazine.sebastianraschka.com/p/understanding-and-coding-self-attention)。）

下一张图展示的概念与上一张相同，只是注意力矩阵的计算被隐藏在"缩放点积注意力"（scaled-dot-product attention）方框内部，而且我们只对一个输入 token 而非所有输入 token 执行计算。这是为了在下一节扩展到多头注意力之前，先展示单头自注意力的一种紧凑形式。

![单头注意力概览](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/single-head.webp)

单个注意力头已经是一个完整的机制：一组可学习投影产出一个注意力矩阵
和一条具有上下文感知能力的输出流（原始出处：
[*Understanding and Coding Self-Attention*](https://magazine.sebastianraschka.com/p/understanding-and-coding-self-attention)。）

## 从单头到多头注意力

一组 `Wq/Wk/Wv` 矩阵给我们一个注意力头，也就是
一个注意力矩阵和一个输出矩阵 `Z`。（这个概念已在上一节中图示。）

多头注意力只是以不同的可学习投影矩阵，并行运行若干个这样的头。

这很有用，因为不同的头可以专注于不同的 token 关系：一个头可能聚焦于短程的
局部依赖，另一个聚焦于更宽泛的语义联系，再一个则聚焦于位置或句法结构。

![并行运行多个注意力头的多头注意力](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/multi-head.webp)

多头注意力保留了同样的基本注意力配方，只是在多个头上并行重复，
使模型可以同时学习多种 token 到 token 的模式（原始出处：
[*Understanding and Coding Self-Attention*](https://magazine.sebastianraschka.com/p/understanding-and-coding-self-attention)。）

参考资料

[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[Understanding and Coding Self-Attention](https://magazine.sebastianraschka.com/p/understanding-and-coding-self-attention)
[Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473)
[Attention Is All You Need](https://arxiv.org/abs/1706.03762)
[LLMs-from-scratch 第 3 章](https://sebastianraschka.com/llms-from-scratch/ch03/01_main-chapter-code/)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
