---
title: "教 AI 系统从字母而非单词学习语言"
title_en: "Teaching AI systems to learn language from letters, not words"
date: 2019-03-15
source: https://ai.facebook.com/blog/teaching-ai-systems-to-learn-language-from-letters
crawled: 2026-09-22
translated: 2026-09-22
---

# 教 AI 系统从字母而非单词学习语言

> 原文：[Teaching AI systems to learn language from letters, not words](https://ai.facebook.com/blog/teaching-ai-systems-to-learn-language-from-letters) · Meta AI（Wayback 存档）

**研究内容：**一种新的自然语言处理（NLP）方法，通过使用未分词（unsegmented）的文本输入、让神经网络在单个字母之间的交互（而非整词）上进行训练，来教会神经网络语言学基础。

**工作原理：**构成 NLP 系统基础的大多数循环神经网络（RNN）都是在已知词表上训练的。为了让 RNN 的训练方式更接近人类学习语言基础的途径，我们从训练数据集中去掉了词边界，并在字符（而非词）级别训练这些网络。一项针对这一无监督字符级语言建模任务的多语言研究使用了英语、德语和意大利语各数百万词的数据集。结果表明，这些「近乎白板」（near tabula rasa）的 RNN 会发展出令人惊叹的语言学知识谱系，包括把字符组切分成词、区分名词与动词，甚至归纳出简单的词义形式。

**为什么重要：**这项工作是 Facebook AI 持续减少语言系统（包括机器翻译任务）对监督依赖的努力的一部分。这一方法的结果表明，只要有足够的输入，AI 系统可以有效地从零开始学习许多语言规则，为未来研究比当今 NLP 系统所需先验知识更少的无监督语言学习方法打开了大门。

**阅读完整论文：**Tabula nearly rasa: Probing the linguistic knowledge of character-level neural language models trained on unsegmented text
