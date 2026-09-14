---
title: "下一 token 预测（next-token prediction）是如何训练大语言模型的？"
title_en: "How does next-token prediction train a large language model?"
source: https://sebastianraschka.com/faq/docs/next-token-prediction.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 下一 token 预测（next-token prediction）是如何训练大语言模型的？

> 原文：[How does next-token prediction train a large language model?](https://sebastianraschka.com/faq/docs/next-token-prediction.html) · Sebastian Raschka's FAQ

下一 token 预测训练大语言模型的方式，是要求模型为文本序列中每个位置之后实际出现的那个 token 分配较高的概率。文本本身同时提供了输入和目标，因此这种训练设置被称为**自监督学习**（self-supervised learning）。无需人工标注员来标注下一个 token。

token 未必是一个完整的词。取决于分词器，它可以表示一个词、词的一部分、标点或空白。模型操作的是这些 token ID，而不是直接处理原始文本。

假设一个分好词的文本块包含 5 个 token。数据加载器会将该序列移动一位：

[
\begin{aligned}
\text{tokens} &= [t\_0, t\_1, t\_2, t\_3, t\_4]   
\text{input} &= [t\_0, t\_1, t\_2, t\_3]   
\text{target} &= [t\_1, t\_2, t\_3, t\_4].
\end{aligned}
]

这个文本块提供了 4 个训练目标。模型在第一个位置的输出与 (t\_1) 对比评估，第二个位置与 (t\_2) 对比，以此类推。因此，包含 (L+1) 个源 token 的序列可提供 (L) 个下一 token 预测。这些窗口的具体构造方式在[大语言模型预训练的输入-目标训练样本是如何构造的？](https://sebastianraschka.com/faq/docs/input-target-pretraining-examples.html)中有专门讨论。

![A tokenized sequence is shifted by one position to create aligned inputs and next-token targets.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch07_compressed/inputs-targets.webp)

目标序列由损失函数使用，它并不作为单独的答案提供给 transformer。transformer 接收输入序列，而[因果注意力掩码](https://sebastianraschka.com/faq/docs/causal-attention.html)（causal attention mask）会阻止每个位置读取更靠后的输入位置。当模型从包含 (t\_2) 的位置预测 (t\_3) 时，它的表示可以依赖于 (t\_0)、(t\_1) 和 (t\_2)，但不能使用 (t\_3)。

对于批量大小 (B)、序列长度 (L) 和词表大小 (V)，模型会返回一个形状为

[
B \times L \times V.
]

的 logits 张量。(L) 个位置中的每一个都对应词表中每个条目的一个得分。softmax 会把这些 logits 转换为概率分布，不过训练实现通常直接把原始 logits 传给一个在内部执行所需 log-softmax 的交叉熵函数。

![A GPT-style model maps each input position to a vector of vocabulary logits. Training uses all valid positions, while generation uses the final position.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-process.webp)

对于序列 (x\_0, x\_1, \ldots, x\_T)，平均下一 token 损失可以写成

[
\mathcal{L}
= -\frac{1}{N}
\sum\_{i \in \mathcal{I}}
\log p\_\theta(x\_i \mid x\_{<i}),
]

其中 (\mathcal{I}) 包含 (N) 个有效目标位置。如果模型给正确 token 分配 0.5 的概率，该位置对损失的贡献约为 0.693；概率为 0.01 时贡献约为 4.605。因此，给观测到的后续内容分配过小的概率会受到强烈惩罚。

填充 token 通常被排除在 (\mathcal{I}) 之外。在指令微调期间，训练方案还可能排除用户提示或模板位置，使损失聚焦于助手的回复。但同样的基本下一 token 目标仍然作用于每一个被纳入的位置。

![Cross-entropy measures how much probability the model assigns to the correct next token at each included position.](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/cross-entropy.webp)

反向传播会把这个平均损失经由输出层和整个 transformer 求导。随后，优化器更新 token 嵌入、注意力层、前馈层、归一化参数以及输出投影。在许多批次上重复这一过程，会让相似上下文中出现的后续内容变得更有可能。

训练时，完整的文本块是已知的。这使得模型可以在一次带掩码的前向传播中对全部 (L) 个位置打分，这种设置通常被称为**教师强制**（teacher forcing）。尽管各位置的矩阵运算是放在一起并行执行的，因果掩码仍能防止未来 token 的泄露。[为什么推理是串行的，而训练要并行得多？](https://sebastianraschka.com/faq/docs/inference-sequential-vs-training-parallel.html)更详细地讨论了这一区别。

生成阶段则以另一种循环使用同样的已学习条件概率。模型处理当前上下文，从最后的 logits 中选择一个 token，将其追加到序列中，然后运行下一个解码步。后续内容是未知的，因此未来的解码步无法提前计算。完整循环参见[自回归文本生成在推理时是如何工作的？](https://sebastianraschka.com/faq/docs/autoregressive-text-generation.html)。

下一 token 预测教会一个基座模型去近似其训练文本中的模式。它并不直接为事实正确性、有用性或指令遵循提供标签。这些属性取决于数据、模型容量以及后续的训练阶段。预训练目标本身仍然是一个具体的概率任务：在整个语料库上提高观测到的下一个 token 的似然。
