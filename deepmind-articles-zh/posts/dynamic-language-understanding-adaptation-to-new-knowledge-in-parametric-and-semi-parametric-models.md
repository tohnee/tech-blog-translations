---
title: "动态语言理解：参数化与半参数化模型对新知识的适应"
title_en: "Dynamic language understanding: adaptation to new knowledge in parametric and semi-parametric models"
source: https://deepmind.google/blog/dynamic-language-understanding-adaptation-to-new-knowledge-in-parametric-and-semi-parametric-models/
site: deepmind
date: 2022-05-26
crawled: 2026-09-13
translated: 2026-09-13
---

# 动态语言理解：参数化与半参数化模型对新知识的适应

> 原文：[Dynamic language understanding: adaptation to new knowledge in parametric and semi-parametric models](https://deepmind.google/blog/dynamic-language-understanding-adaptation-to-new-knowledge-in-parametric-and-semi-parametric-models/) · Google DeepMind

近年来语言模型（LM）的许多成功都是在一种"静态范式"下取得的：其关注点是在那些构建时并未考虑数据时间维度的基准测试上改进性能。例如，回答模型在训练期间可能学到过相关内容的事件的问题，或者在与训练数据同一时期抽取的文本上进行评估。然而，我们的语言和知识是动态且不断演化的。因此，要让问答模型实现下一次性能飞跃、并对其进行更贴近现实的评估，关键在于确保它们在遇到新的、未见过的数据时依然灵活而稳健。

![时间线图，展示 StreamingQA 评估设置：一个横跨 2007 年至 2020 年的"知识语料库"，随后是 2020 年和 2021 年间按季度划分的评估（"评估：未来文章与问题"），分为 Q1、Q2、Q3、Q4。](https://lh3.googleusercontent.com/voWKunmt0yVRAbZOSo9eS_gr4fnWeqQ5KHc6pO76mnUmzhQ2sil5xEbl5CsWOkraROILnVP8iGw6wadVkcKQPb_zKOUoVa-atppgNJ67pCBmbAWHvCc=w1440)

图 1. 我们在未见过的语言和知识上评估模型——图中展示的是关于 2020 年事件的问题，而模型仅使用截至 2019 年底的数据进行训练。

2021 年，我们发布了 [Mind the Gap: Assessing Temporal Generalization in Neural Language Models](https://arxiv.org/abs/2102.01951) 以及针对 WMT 和 arXiv 的[动态语言建模基准](https://github.com/deepmind/deepmind-research/tree/master/pitfalls_static_language_models)，以促进考虑时间动态的语言模型评估。在那篇论文中，我们强调了当前最先进的大型语言模型在时间泛化上面临的问题，并发现知识密集型 token 会遭受相当大的性能损失。

今天，我们发布两篇论文和一个新的基准，进一步推进这一主题的研究。在 [StreamingQA: A Benchmark for Adaptation to New Knowledge over Time in Question Answering Models](http://arxiv.org/abs/2205.11388) 中，我们在新提出的基准 [StreamingQA](https://github.com/deepmind/streamingqa) 上研究问答这一下游任务：我们想理解参数化模型与检索增强的半参数化问答模型如何适应新信息，从而回答关于新事件的问题。在 [Internet-augmented language models through few-shot prompting for open-domain question answering](https://arxiv.org/abs/2203.05115) 中，我们探索了将少样本提示（few-shot prompting）的大语言模型与 Google 搜索这一检索组件相结合的力量。这样做，我们旨在提升模型的事实准确性，同时确保它在回答各种问题时能够获取最新的信息。

## StreamingQA：问答模型随时间适应新知识的基准

通过问答（QA）评估的模型知识与语言理解能力，通常是在静态的知识快照（如 Wikipedia）上研究的。为了研究半参数化问答模型及其底层的参数化语言模型如何适应不断演化的知识，我们构建了新的大规模基准 StreamingQA，其中包含人工撰写和自动生成的问题，这些问题在给定日期提出，需要从 14 年带时间戳的新闻文章中寻找答案（见图 2）。我们证明，参数化模型可以在不完全重新训练的情况下得到更新，同时避免灾难性遗忘。对于半参数化模型，把新文章加入检索空间可以实现快速适应；不过，底层语言模型过时的模型，其表现不如使用重新训练后语言模型的模型。

![StreamingQA 基准数据集示例：显示一个来自 2020 年 2 月的"近期子集"问题，关于净零排放目标；以及一个在 2020 年 4 月提出的"过去子集"问题，关于 2016 年的一部 Netflix 剧集。](https://lh3.googleusercontent.com/fKIKWzhgXEhCZIsP83_g9YdPWo5-ctX-HKzQRoNbx1Lj4fYDo2Hi6ZO1eF30VLgbBzAxun18567rkbaVh7OzahWn3WPLCbRQWc8GT2mL6MKIUv7sjA=w1440)

图 2. StreamingQA 基准中的示例问题。

## 通过少样本提示实现互联网增强语言模型的开放域问答

我们的目标是利用大规模语言模型独有的少样本能力，来克服它们在锚定（grounding）事实性、最新信息方面的部分挑战。受半参数化语言模型的启发——这类模型把决策锚定在外部检索的证据上——我们使用少样本提示，让语言模型学会以 Google 搜索返回的信息为条件，Google 搜索是一个广泛且持续更新的知识来源。我们的方法不涉及微调或学习额外参数，因此几乎可以适用于任何语言模型。事实也确实如此：我们发现，以网络信息为条件的语言模型在开放域问答中的表现超越了规模相近甚至更大的闭卷（closed-book）模型。
