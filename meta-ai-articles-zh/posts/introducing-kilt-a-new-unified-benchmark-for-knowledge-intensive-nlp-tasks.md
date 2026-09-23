---
title: "推出 KILT：面向知识密集型 NLP 任务的新统一基准"
title_en: "Introducing KILT, a new unified benchmark for knowledge-intensive NLP tasks"
date: 2020-09-21
source: https://ai.facebook.com/blog/introducing-kilt-a-new-unified-benchmark-for-knowledge-intensive-nlp-tasks
crawled: 2026-09-22
translated: 2026-09-22
---

# 推出 KILT：面向知识密集型 NLP 任务的新统一基准

> 原文：[Introducing KILT, a new unified benchmark for knowledge-intensive NLP tasks](https://ai.facebook.com/blog/introducing-kilt-a-new-unified-benchmark-for-knowledge-intensive-nlp-tasks) · Meta AI（Wayback 存档）

**这项研究是什么：**KILT（Knowledge Intensive Language Tasks，知识密集型语言任务）是一个新的统一基准，旨在帮助 AI 研究者构建更能利用现实世界知识来完成广泛任务的模型。它统一了 11 个广泛使用的公开数据集，涵盖五种不同类型的任务：事实核查、开放域问答、槽位填充、实体链接和对话生成。KILT 是首个汇集如此多样知识密集型任务数据集的基准。KILT 中的所有数据集都对齐到同一个知识源：一份最新的维基百科快照。这有助于催化面向知识密集型任务的统一、任务无关架构研究，也让尝试不同的任务特定解决方案变得容易得多。在评估模型在知识型任务上的表现时，重要的不仅是最终输出，还包括产生该输出所使用的具体信息。KILT 基准包含出处（provenance）信息，即可解决任务的正确知识的映射。对若干任务，我们通过标注行动让出处标注更加全面。输出与出处相结合，使研究者既能评估模型的准确率，也能评估其为模型预测提供依据的能力。

**工作原理：**KILT 将其 11 个数据集统一为单一格式，并将它们落地（ground）到一份经过预处理的完整维基百科语料库集合中。预处理大型语料库是一个耗时的过程，且会对模型的下游表现产生很大影响。将所有数据集映射到同一语料库，不仅让这一领域的研究工作更加便利，还能在不同模型之间实现更准确、更均衡的评估。由于所有数据集都映射到同一语料库并采用统一格式，KILT 大大降低了探索多任务学习方法与迁移学习的门槛。我们希望由此推动开发出能在整套 KILT 任务上泛化的模型与表示。

（此图展示了 KILT 如何统一不同的知识密集型任务。）

**为什么重要：**AI 研究社区在构建能生成仿自然语言文本的模型方面已取得长足进步。如今最先进的系统表现如此之好，以致其输出很难与人写的文本区分开来。重要的下一步是让这些模型生成的文本不仅流畅，而且立足于现实世界知识。这类自然语言处理模型如今已应用于现实世界的 AI 产品中，从推荐系统到聊天机器人再到智能助手。KILT 为改进这些系统所需的研究提供了便利，并最终有助于构建对我们的世界拥有深入而广泛有用知识的机器。

阅读完整论文：https://arxiv.org/abs/2009.02252

https://github.com/facebookresearch/KILT

http://kiltbenchmark.org

**作者**

- Fabio Petroni，研究工程师
- Aleksandra Piktus，软件工程师
- Angela Fan，研究助理
