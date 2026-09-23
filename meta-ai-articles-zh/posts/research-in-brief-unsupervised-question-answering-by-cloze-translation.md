---
title: "研究简报：通过完形填空翻译实现无监督问答"
title_en: "Research in Brief: Unsupervised Question Answering by Cloze Translation"
date: 2019-03-15
source: https://ai.facebook.com/blog/research-in-brief-unsupervised-question-answering-by-cloze-translation
crawled: 2026-09-22
translated: 2026-09-22
---

# 研究简报：通过完形填空翻译实现无监督问答

> 原文：[Research in Brief: Unsupervised Question Answering by Cloze Translation](https://ai.facebook.com/blog/research-in-brief-unsupervised-question-answering-by-cloze-translation) · Meta AI（Wayback 存档）

**研究内容：** 一种针对流行的抽取式问答（extractive QA）任务的新方法，它自行生成训练数据，而不需要现有的标注问答示例。抽取式问答是自然语言处理（NLP）研究的热门任务，模型必须从文档中抽取一个简短片段来回答自然语言问题。尽管监督模型在抽取式问答上表现出色，但它们需要数千乃至数十万个标注示例来训练，而且在训练所用的文本领域和语言之外测试时性能会下降。通过把抽取式问答当作自监督任务来处理，我们的技术在广泛使用的 SQuAD 数据集上超越了早期的监督模型，且无需任何标注问答训练数据。我们方法的代码现已可供下载。

**工作原理：** 我们的两步方法首先训练一个模型从样本文档中创建填空（也称完形填空，cloze）问题。这个生成管线首先从文本中识别潜在答案，然后构造一个完形填空问题，最后把该问题改写成自然语言形式。例如，模型可以面对这样的文本：

野马队在第五十届超级碗中早早取得领先，此后再未落后。[……] 丹佛野马队线卫 Von Miller 当选超级碗 MVP，贡献了 5 次单独擒抱、2.5 次擒杀和 2 次造成失球。

系统可能首先把「野马队」「丹佛」或各种数字（如「五」和「二」）识别为可能的答案。对于答案「野马队」，模型会创建完形填空问题「_____ 在第五十届超级碗中早早取得领先，此后再未落后」，随后给出最终的非完形填空版本：「哪支球队在第五十届超级碗中早早取得领先？」

在我们方法的第二步中，我们取一个标准的抽取式问答模型架构（通常需要人工标注的问答数据来训练），改用我们问题生成模型产出的数据来训练它。为评估我们的方法，我们在 SQuAD 基准的测试数据上衡量了所得模型的性能，发现其得分为 56.4 F1，击败了一个早期监督模型。

**为什么重要：** 我们的成果表明，自监督的抽取式问答不仅可行，而且已经能与一些监督系统一较高下。由于我们的两步方法无需特定领域或语言的现有标注训练数据就能自行生成训练样本，这项工作能让我们更接近创建可泛化到更多种类任务、支持更多语言的抽取式问答模型，从而有望提升虚拟助手系统的可及性。通过发布我们技术的代码，我们相信这项研究将助力 Facebook AI 推进自监督学习水平的更广泛努力，也帮助更广泛的 AI 共同体探索不那么依赖资源密集型标注数据集的方法。

阅读完整论文：Unsupervised question answering by cloze translation（通过完形填空翻译实现无监督问答）
