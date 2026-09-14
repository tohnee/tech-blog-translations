---
title: "推理阶段的自回归文本生成是如何工作的？"
title_en: "How does autoregressive text generation work at inference time?"
source: https://sebastianraschka.com/faq/docs/autoregressive-text-generation.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 推理阶段的自回归文本生成是如何工作的？

> 原文：[How does autoregressive text generation work at inference time?](https://sebastianraschka.com/faq/docs/autoregressive-text-generation.html) · Sebastian Raschka's FAQ

自回归（autoregressive）文本生成是指 LLM 先生成一个 token，将其加入输入，然后重复这一过程。它在先前各轮中生成的 token 会成为下一次预测的上下文的一部分。*自回归*这个词正是由此而来。

我觉得通过跟踪单个生成步骤最容易看清其中的细节。假设我们从提示词 “Every effort moves you” 开始。分词器（tokenizer）首先把文本转换为 token ID，然后模型处理这个序列。其结果是每个输入位置各对应一组词表得分，也就是 logit。

![A GPT model produces vocabulary logits that are turned into a next-token choice](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/gpt-process.webp)

上图中有一个细节很容易被忽视。模型在每个位置都会返回 logit，但生成循环只需要最后一个位置的 logit。这些得分描述的是在完整提示词之后可能出现的内容。其他位置上的预测只涉及输入中更早的部分，在这里已经用不上了。

选择 token 发生在模型调用之后。我们先把最后的 logit 转换为概率，然后应用某种解码方法。

- **贪心解码（greedy decoding）** 选择概率最高的 token。
- **采样（sampling）** 从分布中抽取一个 token。我们可以通过温度等设置来修改这个分布，或者把抽取范围限制在前 *k* 个候选之内。

假设选中的 token 是一个逗号。我们把这个 token ID 追加到当前序列中，这样下一次模型调用接收到的就是 “Every effort moves you,”，而不是最初的提示词。随后模型会生成逗号之后那个 token 的得分。每一轮都恰好用一个被选中的 token 来扩展输入。

![The predicted token ID is chosen from the vocabulary scores and appended to the sequence](https://sebastianraschka.com/images/LLMs-from-scratch-images/ch05_compressed/proba-index.webp)

这也解释了为什么生成长回答需要许多连续的模型步骤。在 token `t` 存在之前，我们无法选择 token `t+1`。在训练期间，完整文本是现成的，模型可以一次性计算许多位置的损失。而在推理阶段，这种跨未来输出 token 的并行是不可用的。

**KV 缓存**通过存储已处理 token 的注意力键（key）和值（value），避免了一些重复计算。但即便有这个缓存，模型仍然必须等到当前 token 生成之后，才能生成下一个 token。

最后，这个循环还需要一个停止规则。生成通常会因为以下原因之一而结束：

- 模型输出了一个停止符或文本结束（end-of-text）token
- 达到了新生成 token 数的上限
- 触发了应用层面的停止规则
