---
title: "RoBERTa：一种优化的自监督 NLP 系统预训练方法"
title_en: "RoBERTa: An optimized method for pretraining self-supervised NLP systems"
date: 2019-03-15
source: http://ai.facebook.com/blog/roberta-an-optimized-method-for-pretraining-self-supervised-nlp-systems
crawled: 2026-09-22
translated: 2026-09-22
---

# RoBERTa：一种优化的自监督 NLP 系统预训练方法

> 原文：[RoBERTa: An optimized method for pretraining self-supervised NLP systems](http://ai.facebook.com/blog/roberta-an-optimized-method-for-pretraining-self-supervised-nlp-systems) · Meta AI（Wayback 存档）

**研究内容：** 一种经稳健优化的自然语言处理（NLP）系统预训练方法，改进自 Google 2018 年发布的自监督方法——来自 Transformer 的双向编码器表示（BERT）。BERT 是一项革命性技术，依靠从网络上获取的无标注文本（而非针对特定任务标注的语言语料库），在一系列 NLP 任务上取得了最先进的结果。此后，该技术既成为流行的 NLP 研究基线，也成为最终的任务架构。BERT 还彰显了 AI 研究的协作本质——得益于 Google 的开放发布，我们得以对 BERT 开展复现研究，揭示提升其性能的机会。我们优化后的方法 RoBERTa 在广泛使用的 NLP 基准「通用语言理解评估」（GLUE）上取得了最先进的结果。除了详述这些结果的论文外，我们还发布了用于展示该方法有效性的模型和代码。

**工作原理：** RoBERTa 建立在 BERT 的语言掩码策略之上——系统学习在无标注语言样本中预测被刻意隐藏的文本片段。RoBERTa 用 PyTorch 实现，修改了 BERT 的关键超参数，包括移除 BERT 的下一句预测预训练目标，并以更大的小批量（mini-batch）和学习率训练。这使 RoBERTa 在掩码语言建模目标上超越 BERT，并带来更好的下游任务表现。我们还探索用比 BERT 多一个数量级的数据、更长的时间训练 RoBERTa。我们既使用了现有的无标注 NLP 数据集，也使用了 CC-News——一个取自公开新闻文章的新数据集。实施这些设计变更后，我们的模型在 MNLI、QNLI、RTE、STS-B 和 RACE 任务上交付了最先进性能，并在 GLUE 基准上取得可观提升。RoBERTa 以 88.5 分登顶 GLUE 排行榜，追平了此前的领先者 XLNet-Large。这些结果凸显了 BERT 训练中此前未探索的设计选择的重要性，并有助于厘清数据规模、训练时长和预训练目标各自的相对贡献。

**为什么重要：** 我们的结果表明，调优 BERT 训练流程可以显著提升其在多种 NLP 任务上的性能，同时表明这一总体方法与替代方法相比依然具有竞争力。更广泛地说，这项研究进一步证明了自监督训练技术追平乃至超越更传统的监督方法性能的潜力。RoBERTa 是 Facebook 持续推进自监督系统技术前沿的承诺的一部分——这类系统的开发可以更少依赖耗时耗资源的数据标注。我们期待看到更广泛的共同体用 RoBERTa 的模型和代码做出什么。

阅读完整论文：RoBERTa: A robustly optimized BERT pretraining approach（RoBERTa：一种稳健优化的 BERT 预训练方法）
