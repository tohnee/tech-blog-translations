---
title: "一个学会回答完整问题的新生成式问答模型"
title_en: "A new generative QA model that learns to answer the whole question"
date: 2019-07-02
source: https://ai.meta.com/blog/a-new-generative-qa-model-that-learns-to-answer-the-whole-question/
crawled: 2026-09-22
translated: 2026-09-22
---

# 一个学会回答完整问题的新生成式问答模型

> 原文：[A new generative QA model that learns to answer the whole question](https://ai.meta.com/blog/a-new-generative-qa-model-that-learns-to-answer-the-whole-question/) · Meta AI（Wayback 存档）

**研究内容：**一个新的问答（QA）模型，通过逆向工程问题来确定正确回答。当前最先进的模型以判别方式训练，这意味着一旦任何线索能让它们预测出正确答案，它们就会停止学习。我们则训练模型从答案生成问题，这教会它解释所有线索。例如，如果给模型看一张图片并问草是什么颜色，目前大多数模型会不看图像直接记住「绿色」这个答案。而我们的模型必须预测问题，这要求它察看图像并学会识别草。如果给定颜色「绿色」，模型生成「草的颜色」这类问题的可能性，会比给定颜色「蓝色」时更高。

**工作原理：**我们的 QA 模型通过学习可能答案上的先验分布和一个生成问题的模型来实现。我们使用条件语言模型在给定答案的情况下生成问题——由于问题是逐词生成的，这带来了可扩展且可解释的多跳推理。上图展示了在验证问题上预测高亮词时，问题生成过程中的词概率映射。例如在上面的例子中，预测「object」这个词时，模型已经写下了「Is there a rubber」，因此知道下一个词必须是某种橡胶制品；于是模型只关注橡胶材质而非金属。

**为什么重要：**这是首个在聚焦困难推理的语言理解和问答两类任务上都表现良好的模型。它在对抗性问答上优于以往工作——在对抗性问答中，文档被故意加入了专门设计用于对抗的句子。更具体地说，我们的模型在关键基准上与专门的判别式模型取得了相当的竞争力，证明它是一种比以往工作更通用的语言理解与推理架构。这一行为对我们的研究很重要，不仅在自然语言处理方面，也在构建更直觉的 AI 系统方面。

阅读完整论文：Generative Question Answering: Learning to Answer the Whole Question
