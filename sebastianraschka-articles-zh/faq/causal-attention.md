---
title: "GPT 风格语言模型中的因果注意力"
title_en: "Causal Attention in GPT-Style Language Models"
source: https://sebastianraschka.com/faq/docs/causal-attention.html
crawled: 2026-09-06
translated: 2026-09-14
---

# GPT 风格语言模型中的因果注意力

> 原文：[Causal Attention in GPT-Style Language Models](https://sebastianraschka.com/faq/docs/causal-attention.html) · Sebastian Raschka's FAQ

**因果注意力（causal attention）**是带有一条阻断来自靠后 token 位置信息的规则的自注意力。在位置 `t` 处，模型只能关注（attend）到包括 `t` 在内及之前的位置。得到的表示随后被用来预测位置 `t+1` 处的 token。

举一个小例子，考虑 token 序列 “the cat sat”。当模型计算 “cat” 的表示时，它可以使用 “the” 和 “cat”。它不能使用 “sat”，因为 “sat” 正是此时下一 token 的预测目标。

![Causal attention masks future positions in the attention matrix](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch03_compressed/19.webp)

这一限制让 GPT 风格的模型能够在完整序列上训练，却看不到自身预测任务的答案。整条训练序列都在内存中可用，因此可以并行处理许多位置。注意力掩码仍然限制着每个位置能读取的内容。

如果没有掩码，“cat” 的表示就可能纳入来自 “sat” 的信息，进而利用这些信息去预测 “sat”。训练损失会因错误的理由而变得很低。而在生成阶段，未来的 token 并不存在，同样的捷径也就无从谈起。

具体实现是在注意力得分矩阵上使用三角掩码。指向靠后位置的条目在 softmax 之前会被赋予负无穷之类的值。它们的概率因此变为零，而对角线上以及对角线以下的条目仍然可用。

![The mask is applied before softmax so future-token weights become zero](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch03_compressed/21.webp)

一个有用的附带结果是：所有位置仍能在同一次前向传播中贡献训练信号。位置 5 可以学习预测位置 6，同时位置 20 学习预测位置 21。这些计算并行执行，而由于掩码的存在，每个位置观察到的是不同长度的前缀。

在推理阶段，生成过程使用同样的依赖模式。最后一个位置的表示可以使用提示词以及迄今为止生成的所有 token。它的 logit 选出下一个 token，该 token 被追加到序列中，然后模型再次运行。靠前的位置只能访问更短的前缀，因此它们不可能包含序列中较晚才引入的信息。

诸如 BERT 之类的 transformer 编码器使用双向注意力。BERT 接收完整的输入，允许一个 token 关注两侧的位置。这适合那些全文已知的任务，比如为分类构建表示。而 decoder-only 的 GPT 模型需要的则是文本生成所要求的从左到右的依赖关系。

「不能看到未来」这句话指的是当前序列内部的位置。它并不意味着注意力跨度很短。一个 token 仍然可以回溯到可用前缀中很远的地方，直至模型的上下文窗口上限。
