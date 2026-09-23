---
title: "一种对拼写错误具有鲁棒性的词嵌入新模型"
title_en: "A new model for word embeddings that are resilient to misspellings"
date: 2019-08-09
source: https://ai.meta.com/blog/-a-new-model-for-word-embeddings-that-are-resilient-to-misspellings-/
crawled: 2026-09-22
translated: 2026-09-22
---

# 一种对拼写错误具有鲁棒性的词嵌入新模型

> 原文：[A new model for word embeddings that are resilient to misspellings](https://ai.meta.com/blog/-a-new-model-for-word-embeddings-that-are-resilient-to-misspellings-/) · Meta AI（Wayback 存档）

**研究内容：**一种学习对拼写错误具有鲁棒性的词嵌入的新模型（词嵌入即把词或短语映射为以稠密数字向量表示其含义的方法）。尽管 word2vec 和 GloVe 等流行方法能为训练中见过的词提供可行的表示，但它们无法为词表外（OOV）词——即训练时未见过的词——生成嵌入。在处理包含缩写、俚语或拼写错误的文本时，这一问题尤为棘手。为弥补这一缺陷，我们提出了 Misspelling Oblivious Embeddings（MOE，拼写错误无关嵌入），这是一种将我们的开源库 fastText 与一个有监督任务相结合的新模型，该任务会将拼写错误的词嵌入到其正确变体的附近。我们通过多项内在与外在任务考察了这一方法的有效性，发现 MOE 在用户生成文本上优于 fastText。

**工作原理：**fastText 的损失函数旨在让出现在相同上下文中的词在嵌入空间中彼此靠近，我们称之为语义损失（semantic loss）。在语义损失之外，MOE 还考虑了一个额外的有监督损失，我们称之为拼写纠正损失（spell correction loss）。拼写纠正损失通过最小化语义损失与拼写纠正损失的加权和，把拼写错误的词嵌入到其正确版本的附近。最小化相应的损失函数分量（语义损失）等价于最大化在给定词的条件下预测其上下文的概率；类似地，拼写纠正损失旨在最大化在给定其拼写错误形式的情况下预测该词的概率。我们使用维基百科转储（Wikipedia Dump）来训练语义损失，并使用一个包含 2000 万条示例的拼写错误数据集。为便于后续研究，我们开放了这个拼写错误数据集。

为评估我们的方法，我们想验证是否确实把拼写错误的词映射到了正确变体的附近。下面以拼写错误「samallest」的结果为例：如果检索「samallest」的六个最近邻，fastText 返回的列表中并不会出现「smallest」。这说明对 fastText 而言，哪怕只改动一个字母，也可能显著改变生成的嵌入。而 MOE 能够把「smallest」检索进前三名结果之中。

**为什么重要：**现有词嵌入方法往往无法处理含有 OOV 词的不规范文本。在现实任务中，人们产生的输入文本常常包含拼写错误（OOV 词的常见来源），尤其是在网络搜索、聊天消息和社交媒体帖子等场景。多达 15% 的网络搜索查询中会出现拼写错误。我们的方法将提升词嵌入在现实场景中的可用性。未来的工作可以把这一方法应用于训练多语言嵌入和上下文嵌入。

阅读完整论文：Misspelling Oblivious Word Embeddings

GitHub：Misspellings Dataset
