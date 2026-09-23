---
title: "MLQA：评估跨语言抽取式问答"
title_en: "MLQA: Evaluating cross-lingual extractive question answering"
date: 2019-03-15
source: https://ai.facebook.com/blog/mlqa-evaluating-cross-lingual-extractive-question-answering
crawled: 2026-09-22
translated: 2026-09-22
---

# MLQA：评估跨语言抽取式问答

> 原文：[MLQA: Evaluating cross-lingual extractive question answering](https://ai.facebook.com/blog/mlqa-evaluating-cross-lingual-extractive-question-answering) · Meta AI（Wayback 存档）

**新内容**：MLQA 是一个多路对齐的抽取式问答（QA）评估基准。它旨在帮助 AI 社区在更多语言中改进和扩展问答，并促进零样本多语言 QA 方法的研究。MLQA 包含 12000 个英语 QA 实例，以及另外六种语言各超过 5000 个实例：阿拉伯语、德语、印地语、西班牙语、越南语和简体中文。Facebook AI 的 LASER 工具包被用来识别适合 MLQA 的文档。由于 MLQA 高度平行——数据集中的每个问题都以多种语言出现——研究者可以用它比较跨语言的迁移性能。它还便于进行跨语言评估，例如问题为越南语而答案为印地语的情形。我们在 MLQA 上评估了当前最先进的跨语言表示，发现训练语言与测试语言之间存在显著的性能差距。我们邀请问答与跨语言研究社区携手，在这一全新的跨语言理解任务上取得进展。为助力这一努力，我们提供了基于机器翻译的基线以及我们的评估结果。

（题图说明：该图示展示了 MLQA 标注流水线（简化为只展示一种目标语言）。如左图所示，我们首先在特定主题的维基百科文章中识别并抽取平行句子；然后由人类标注者构造相应的问题。最右侧的图展示了英语问题如何由专业译者转换为所有语言 qi，然后在目标语言中标注答案。）

**为什么重要**：近年来，抽取式问答系统（也称阅读理解模型）在准确率上取得显著改进，甚至已经超越人类。但这些模型的训练需要成千上万条干净数据点，而如此高质量的数据集只有少数几种语言才有。要构建在更多语言上都有良好表现的 QA 模型，研究社区需要高质量的评估数据来设定基准并度量进展。MLQA 数据集正是专为这一目的设计的，为跨语言研究提供了有价值的新工具。

**用途**：评估问答中的跨语言性能。

**获取地址**：https://github.com/facebookresearch/MLQA

作者：Patrick Lewis，博士生；Holger Schwenk，研究科学家
