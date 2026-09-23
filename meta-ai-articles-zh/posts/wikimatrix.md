---
title: "WikiMatrix：从 1620 个语言对中抽取 1.35 亿条维基百科句子的双语文本"
title_en: "WikiMatrix: Bitext extraction of 135 million Wikipedia sentences in 1,620 language pairs"
date: 2019-03-15
source: http://ai.facebook.com/blog/wikimatrix
crawled: 2026-09-22
translated: 2026-09-22
---

# WikiMatrix：从 1620 个语言对中抽取 1.35 亿条维基百科句子的双语文本

> 原文：[WikiMatrix: Bitext extraction of 135 million Wikipedia sentences in 1,620 language pairs](http://ai.facebook.com/blog/wikimatrix) · Meta AI（Wayback 存档）

我们使用 Facebook AI 的 LASER 工具包和 Faiss 库创建了 WikiMatrix——迄今最大、最完整的多语言平行句抽取。利用公开可用的维基百科文章，我们为 85 种语言、1620 个不同语言对抽取了 1.35 亿条平行句子。这些配对系统性地覆盖所有可能的语言对，包括希伯来语-意大利语、阿拉伯语-越南语这类不常见的组合。我们现在正与 AI 研究社区分享 WikiMatrix。此外，我们通过训练超过 1800 个神经机器翻译系统并在 TED 语料库上评估，提供了详尽的质量评估。WikiMatrix 提供的平行数据可用于直接训练甚至远缘语言之间的神经机器翻译系统，无需先翻译成英语。

**为什么重要：** 大多数多语言模型（尤其是神经机器翻译系统）需要平行语料库来训练。大量平行文本只有部分主要语言才有，而且通常只与英语对齐。WikiMatrix 是首个系统处理维基百科上所有语言（包括低资源语言和方言）的数据集。此外，许多公开的平行语料库来自某一特定来源（如法律文本），而 WikiMatrix 语料库覆盖维基百科上的广泛主题。由于 WikiMatrix 包含大量不同语言的句子对，它可以更有效地为低资源语言训练和评估翻译系统。WikiMatrix 还展示了如何利用 LASER 的大规模多语言句子嵌入和 Faiss 库高效执行大规模基于距离的双语文本挖掘。相比之下，用暴力方法比较 1.34 亿条英语与 5100 万条德语维基百科条目，需要计算超过 6 千万亿（quadrillion）次距离。

**用途：** NLP 研究者可以使用 WikiMatrix 为 85 种不同的语言和方言训练、评估并比较新的翻译模型或其他多语言模型。

在 GitHub 上获取：
- 论文：https://arxiv.org/abs/1907.05791
- GitHub：https://github.com/facebookresearch/LASER/tree/master/tasks/WikiMatrix

**作者**
Holger Schwenk，研究科学家
