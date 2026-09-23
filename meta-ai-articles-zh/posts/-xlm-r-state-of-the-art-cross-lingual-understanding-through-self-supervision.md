---
title: "XLM-R：通过自监督实现最先进的跨语言理解"
title_en: "XLM-R: State-of-the-art cross-lingual understanding through self-supervision"
date: 2019-03-15
source: https://ai.meta.com/blog/-xlm-r-state-of-the-art-cross-lingual-understanding-through-self-supervision/
crawled: 2026-09-22
translated: 2026-09-22
---

# XLM-R：通过自监督实现最先进的跨语言理解

> 原文：[XLM-R: State-of-the-art cross-lingual understanding through self-supervision](https://ai.meta.com/blog/-xlm-r-state-of-the-art-cross-lingual-understanding-through-self-supervision/) · Meta AI（Wayback 存档）

**研究内容：**一个名为 XLM-R 的新模型，利用自监督训练技术在跨语言理解上达到最先进性能——这一任务要求模型以一种语言训练，然后无需额外训练数据即可用于其他语言。我们的模型通过纳入更多训练数据和更多语言（包括缺乏大量标注与未标注数据集的所谓低资源语言），改进了以往的多语言方法。XLM-R 在四个跨语言理解基准上取得了迄今最佳结果：在 XNLI 跨语言自然语言推断数据集上平均准确率提升 4.7%，在最新推出的 MLQA 问答数据集上平均 F1 分数提升 8.4%，在 NER 上 F1 分数提升 2.1%。经过大量实验和消融研究，我们证明 XLM-R 是首个优于依赖预训练模型的传统单语言基线的多语言模型。除了分享结果，我们还将此项研究使用的代码和模型开放，这些资源可在我们 GitHub 上的 fairseq、PyText 和 XLM 仓库中找到。

**工作原理：**虽然该领域早期工作已经证明了多语言掩码语言模型在跨语言理解上的有效性，但 XLM 和多语言 BERT 等模型在学习低资源语言的有用表示方面能力有限。XLM-R 在多个方面改进了以往方法：

- 在我们用于 XLM 和 RoBERTa 的跨语言方法基础上，我们为新模型增加了语言数量和训练样本，从超过 2 TB 经过清洗和过滤的公开 CommonCrawl 数据中训练自监督跨语言表示。其中包括为低资源语言生成新的未标注语料库，使这些语言可用的训练数据量提高了两个数量级。
- 在微调期间，我们利用多语言模型使用多语言标注数据的能力来提升下游任务性能。这使我们的模型在跨语言基准上取得最先进结果，同时超过单语言 BERT 模型的单语言性能。
- 我们调整了模型参数，以抵消「用跨语言迁移把模型扩展到更多语言也会限制模型理解每种语言的能力」这一事实。参数调整包括：在训练和词表构建期间对低资源语言上采样、生成更大的共享词表，并将整体模型容量提高到 5.5 亿参数。

我们发现 XLM-R 在低资源语言上表现尤为出色：与在最先进的、基于 15 种语言训练的先前模型相比，斯瓦希里语的 XNLI 性能提升 2.3%，乌尔都语提升 5%。

**为什么重要：**鉴于 Facebook 上的人们用超过 160 种语言发布内容，XLM-R 代表着朝我们的愿景迈出的重要一步：无论用户说什么语言，都为每个人在我们的平台上提供最佳体验。潜在应用包括为识别仇恨言论和其他违反政策内容提供覆盖广泛语言的高精度模型。随着这项工作帮助我们转向「一个模型服务多种语言」的方法（而非每种语言一个模型），它也将使我们更容易继续同时推出多种语言的高性能产品。通过开源模型和代码（可通过我们面向 fairseq、PyText 和 XLM 的 GitHub 仓库获取），我们希望提升研究社区构建的多语言模型的性能，尤其是那些使用自监督训练方法更好理解低资源语言的系统。

阅读完整论文：Unsupervised Cross-lingual Representation Learning at Scale
