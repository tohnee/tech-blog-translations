---
title: "Facebook 与纽约大学扩展自然语言理解系统的可用语言"
title_en: "Facebook, NYU expand available languages for natural language understanding systems"
date: 2018-10-26
source: https://ai.meta.com/blog/facebook-nyu-expand-available-languages-for-natural-language-understanding-systems
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 与纽约大学扩展自然语言理解系统的可用语言

> 原文：[Facebook, NYU expand available languages for natural language understanding systems](https://ai.meta.com/blog/facebook-nyu-expand-available-languages-for-natural-language-understanding-systems) · Meta AI（Wayback 存档）

2018 年 10 月 26 日

**研究内容：**XLNI 数据集，为评估自然语言理解（NLU）的跨语言方法而创建。这是 Facebook 与纽约大学的合作成果，在常用的多体裁自然语言推理（MultiNLI）语料库基础上，为这个原本只有英语的数据集新增了 14 种语言，其中包括两种低资源语言：斯瓦希里语和乌尔都语。

**工作原理：**大多数现有 NLU 模型是在单一语言的有监督数据（为训练目的而人工标注的数据）上训练的。但当研究者希望增加系统能理解的语言数量时，为每种语言收集并标注数据的做法不可扩展。一种可能的解决方案是跨语言理解：先在一种语言的数据上训练模型，再在其他语言上测试该模型。跨语言自然语言推理（XNLI）数据集通过提供这样的测试数据推进了这一方法——它在 MultiNLI 数据集上新增了共 112500 对标注句对，覆盖另外 14 种语言。XNLI 还提供了多个基线，帮助其他人构建理解多种语言的系统。其中两个基线基于 AI 机器翻译系统；另外两个使用平行数据，供计算资源有限的研究者训练系统之用。

**为什么重要：**除了扩展一个被广泛使用的 NLU 研究数据集之外，XNLI 还服务于更宏大的研究目标——构建能理解更广泛语言的 AI 系统。通过纳入斯瓦希里语和乌尔都语的句对及结果，该数据集也支持了与低资源语言相关的研究，帮助该领域摆脱以英语为中心的 NLU 模型。该数据集可供下载。

**阅读完整论文：**《XNLI: Evaluating Cross-Lingual Sentence Representations》
