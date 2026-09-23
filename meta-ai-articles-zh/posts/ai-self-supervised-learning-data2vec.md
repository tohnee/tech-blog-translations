---
title: "Data2vec 2.0：面向视觉、语音与文本的高效自监督学习"
title_en: "Data2vec 2.0: Highly efficient self-supervised learning for vision, speech and text"
date: 2022-12-13
source: https://ai.meta.com/blog/ai-self-supervised-learning-data2vec
crawled: 2026-09-22
translated: 2026-09-22
---

# Data2vec 2.0：面向视觉、语音与文本的高效自监督学习

> 原文：[Data2vec 2.0: Highly efficient self-supervised learning for vision, speech and text](https://ai.meta.com/blog/ai-self-supervised-learning-data2vec) · Meta AI（Wayback 存档）

2022 年 12 月 13 日

AI 领域近来的许多突破都由自监督学习（self-supervised learning）驱动，它让机器无需依赖标注数据即可学习。但现有算法存在若干重大局限，例如往往只针对单一模态（如图像或文本）专门设计，并且需要大量算力。这与人类学习形成鲜明对比：人类的学习效率似乎远高于当前的 AI，而且能以相似的方式从不同类型的信息中学习，而不需要为文本、语音及其他模态分别配备独立的学习机制。今年早些时候，Meta AI 发布了 data2vec，解决了其中一项局限——这是首个能以相同方式学习三种不同模态（语音、视觉、文本）的高性能自监督算法。data2vec 让把某个领域（比如文本理解）的研究进展迁移应用到图像分割或语音翻译任务变得容易得多。今天，我们分享 data2vec 2.0，一个效率大幅提升、性能超越前代的新算法。它在计算机视觉上达到与现有最流行自监督算法相同的精度，但速度快 16 倍。为了让其他研究者也能使用我们的研究，我们现在公开了代码和预训练模型。

## data2vec 2.0 的工作原理

自监督学习的总体思路是让机器仅通过观察世界来学习图像、语音和文本的结构。这一领域的进展带来了语音（如 wav2vec 2.0）、计算机视觉（如掩码自编码器）和自然语言处理（如 BERT）的诸多突破。但现代系统的计算开销可能非常大，因为训练超大模型需要大量 GPU。

data2vec 2.0 训练方式示意图。它可以分别在文本、语音或图像上训练。

与原始 data2vec 算法类似，data2vec 2.0 预测的是数据的上下文化表示（contextualized representation）——即神经网络的各层——而不是图像的像素、文本段落的词或语音的声音。与大多数其他算法不同，这些所谓的目标表示是上下文化的，也就是说它们会考虑整个训练样本。例如，单词 bank 的表示基于该词所处的整个句子，因此更容易表示出该词的正确含义（「金融机构」还是「河边的地面」）。我们相信，上下文化目标带来了更丰富的学习任务，使 data2vec 2.0 比其他算法学得更快。

我们通过几种方式提升了原始 data2vec 算法的效率：

第一，我们把为某个训练样本构建的目标表示复用于其多个掩码版本（即隐藏训练样本中不同的随机部分）。我们把每个版本都输入学生模型，让它对不同的掩码版本预测同一个上下文化目标表示。这有效地摊销了构建目标表示所需的计算量。

第二，与掩码自编码器类似，对于训练样本中被遮蔽掉的部分（在我们的场景中约占一张图像的 80%），我们不再运行学生编码器网络，从而节省了大量计算周期。

最后，我们使用了一个更高效的解码器模型，它不依赖 Transformer 网络，而是采用多层卷积网络。

在相同硬件上把 data2vec 2.0 训练到与流行现有算法相同精度时的相对训练时间改进。

## data2vec 2.0 带来的效率提升

为了更清楚地了解 data2vec 2.0 相比前代及其他算法高效多少，我们在广泛使用的基准上测试了它在计算机视觉、语音和文本任务上的表现。我们关注的是最终精度和预训练模型所需的时间，并在相同硬件（GPU 数量等）上测量各算法的速度。

在计算机视觉方面，我们在标准的 ImageNet-1K 图像分类基准上评测了 data2vec 2.0，它在那里学习图像表示。data2vec 2.0 可以达到掩码自编码器（MAE）相同的精度，但快 16 倍（在同等条件下按墙钟时间计）。如果给算法更多时间，它还能达到更高精度，同时仍比 MAE 快。

data2vec 2.0 计算机视觉结果：图中展示了各算法在流行的 ImageNet-1K 基准上速度与图像分类精度的关系。

在语音方面，我们在 LibriSpeech 语音识别基准上测试，其速度比 wav2vec 2.0 快 11 倍以上，精度相近。在自然语言处理（NLP）方面，我们在流行的通用语言理解评测（GLUE）基准上评测 data2vec 2.0，它以一半的训练时间达到了 RoBERTa（BERT 的一个重新实现）相同的精度。

data2vec 2.0 语音与 NLP 结果：上图展示在 LibriSpeech 上预训练、在 10 小时 Libri-light 数据上微调、并在 dev-other 上评测的模型的速度与语音识别词错误率的关系；下图展示采用原始 BERT 设置时在 GLUE 基准上的自然语言理解精度。

## 迈向高效学习的机器

我们正在努力构建更通用、更高效的自监督算法，使其能用单一学习目标从不同模态中学习。更高效的学习能力对视频这类处理起来计算量极大的模态尤为重要。我们希望 data2vec 2.0 这样更高效的自监督学习算法，最终能让机器深刻理解极其复杂的数据，比如一整部电影的内容。

开源代码与预训练模型可在此获取，论文请见此处（原文此处将 here 误写为 hear，照原文说明——译注）。

在 GitHub 上获取：https://github.com/facebookresearch/fairseq/tree/master/examples/data2vec

阅读论文：Efficient self-supervised learning with contextualized target representations for speech, vision, and language

本篇博客得益于 Alexei Baevski、Arun Babu、Wei-Ning Hsu 和 Michael Auli 的工作。本文第二张图已更新以更正一处笔误。
