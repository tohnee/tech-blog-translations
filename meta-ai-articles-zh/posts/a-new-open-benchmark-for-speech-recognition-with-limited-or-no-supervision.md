---
title: "面向有限或无监督语音识别的全新开放基准"
title_en: "A new open benchmark for speech recognition with limited or no supervision"
date: 2019-12-20
source: https://ai.meta.com/blog/a-new-open-benchmark-for-speech-recognition-with-limited-or-no-supervision/
crawled: 2026-09-22
translated: 2026-09-22
---

# 面向有限或无监督语音识别的全新开放基准

> 原文：[A new open benchmark for speech recognition with limited or no supervision](https://ai.meta.com/blog/a-new-open-benchmark-for-speech-recognition-with-limited-or-no-supervision/) · Meta AI（Wayback 存档）

**它是什么：**有史以来最大的开源语音技术数据集 Libri-light，完全由公有领域音频构建，并针对使用有限监督或无监督开发自动语音识别（ASR）系统进行了优化。以往语音数据集通常由人工标注的训练样本组成，以监督学习目标喂给 ASR 系统；我们则把 Libri-light 设计为支持三种对标签依赖更低的训练设定。这些方法包括：在原始未标注数据上预训练声学模型、混合使用标注与未标注数据训练，以及从不对齐的音频和文本训练。除训练集和测试集外，Libri-light 还包含指标和基线模型，帮助研究者比较不同的、所需监督更少乃至完全无需监督的 ASR 系统开发方法。

**工作原理：**我们使用来自 LibriVox（一个大型公有领域有声书仓库）的超过 60000 小时英语未标注语音构建 Libri-light。除了过滤损坏和重复的数据、添加语音活动、说话人和题材元数据以使其在 ASR 训练语境中更有用之外，我们还在流行的 LibriSpeech ASR 基准之上构建了基线系统和评估指标。具体来说，我们针对三种训练设定——自监督、半监督和远程监督（distant supervision）训练——构建了 ASR 系统，并在标准 LibriSpeech 开发集和测试集上评估。在原始音频上预训练我们的自监督模型，其准确率超过了最近一届 Zero Resource Speech Challenge 中的最先进系统；而我们的半监督系统（训练时使用了少量标注语音）的准确率随着预训练量的增加而提升，识别音素（与词相关的声音）时的错误更少。在远程监督设定（使用有限标签的不对齐文本与语音音频组合创建声学模型）中，我们使用了一个为未标注数据集自动生成标签的流程。所得系统的准确率低于全监督系统，但其表现表明：增加无监督预训练的程度可以改善词错误率，这说明在大量未标注数据上训练的价值——即便对同时使用标注的系统也是如此。

**为什么重要：**Libri-light 为训练面向那些缺乏传统全监督方法所需大规模训练数据集的语言的 ASR 系统树立了新标准。世界上 7000 种语言中的绝大多数都无法获得这些训练资源，因此 Libri-light 有望帮助全球数以百万计的人开发或改进 ASR。即使在英语、普通话、西班牙语和阿拉伯语等高资源语言中，对全监督的依赖也限制了 ASR 的效力，因为这些语言通常包含大量方言变体。我们的整体数据集比通常用于无监督语音学习的 Zero Resource Speech Challenge 数据集大三个数量级。而且由于 Libri-light 使用标准 LibriSpeech 作为测试集，它是首个让研究者能够直接比较使用不同程度监督的方法、并对照监督 ASR 最先进水平衡量其性能的基准。这将有助于提供共同的目标和里程碑，加速整个领域在减少监督、把 ASR 带给世界更多语言方面的集体进展。

**获取：**Libri-light 可在此获取，包括完整数据集以及我们用于评估的基线和指标。

阅读完整论文：Libri-light: A benchmark for ASR with limited or no supervision
