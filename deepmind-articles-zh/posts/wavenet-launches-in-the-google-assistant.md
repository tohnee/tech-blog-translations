---
title: "WaveNet 正式登陆 Google Assistant"
title_en: "WaveNet launches in the Google Assistant"
source: https://deepmind.google/blog/wavenet-launches-in-the-google-assistant/
site: deepmind
date: 2017-10-04
crawled: 2026-09-13
translated: 2026-09-13
---

# WaveNet 正式登陆 Google Assistant

> 原文：[WaveNet launches in the Google Assistant](https://deepmind.google/blog/wavenet-launches-in-the-google-assistant/) · Google DeepMind

**就在一年多以前，我们发布了** [WaveNet](https://deepmind.com/blog/article/wavenet-generative-model-raw-audio)——一种用于生成原始音频波形的新型深度神经网络，它能够生成比既有技术更好、听感更逼真的语音。当时，该模型还只是一个研究原型，计算量太大，无法在消费级产品中使用。

但在过去 12 个月里，我们努力显著提升了模型的速度和质量。今天，我们自豪地宣布：WaveNet 的更新版本已被用于在所有平台上生成 [Google Assistant](https://www.blog.google/products/assistant/google-assistant-powering-our-new-family-hardware/) 的美式英语和日语语音。

使用新的 WaveNet 模型，Assistant 将拥有一批听感更加自然的语音。

## 美式英语语音 I

您的浏览器不支持音频元素。您的浏览器不支持音频元素。

## 美式英语语音 II

您的浏览器不支持音频元素。您的浏览器不支持音频元素。

## 美式英语第三方语音

您的浏览器不支持音频元素。您的浏览器不支持音频元素。

## 日语语音

您的浏览器不支持音频元素。您的浏览器不支持音频元素。

要理解 WaveNet 为什么能超越当前最先进的技术，有必要先了解当今的文语转换（text-to-speech，TTS）——即[语音合成](https://en.wikipedia.org/wiki/Speech_synthesis)——系统是如何工作的。

其中大多数系统基于所谓的[拼接式 TTS（concatenative TTS）](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=Es-YRKMAAAAJ&citation_for_view=Es-YRKMAAAAJ:u5HHmVD_uO8C)，它使用一个由同一位配音演员在数小时内录制的高质量录音大数据库。这些录音被切分成微小的片段，然后可以根据需要把片段组合——即拼接——成完整的语句。然而，这类系统可能产生听感不自然的语音，而且难以修改：每次需要新增一组变化（例如新的情感或语调）时，都必须重新录制一整个数据库。

为了克服其中一些问题，人们有时会使用另一种被称为[参数式 TTS（parametric TTS）](https://scholar.google.com/citations?view_op=view_citation&hl=en&user=z3IRvDwAAAAJ&citation_for_view=z3IRvDwAAAAJ:d1gkVwhDpl0C)的模型。它通过一系列关于语法和口部动作的规则与参数来引导计算机生成的语音，从而免除了拼接声音的需要。虽然更便宜、更快速，但这种方法生成的语音听感较不自然。

WaveNet 采取了一种截然不同的思路。在[原始论文](https://arxiv.org/pdf/1609.03499.pdf)中，我们描述了一个深度生成模型，它能够从零开始逐个采样点地创建音频波形，每秒 16000 个采样点，且单个声音之间过渡平滑。

![示意图，展示 WaveNet 卷积神经网络的各层：底部的蓝色节点输入层、中间的三层灰色节点隐藏层，以及顶部的橙色节点输出层。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62227b1d1dd26da452c9e160_unnamed-2.gif)

支撑原始 WaveNet 模型的卷积神经网络结构

它使用[卷积神经网络](https://en.wikipedia.org/wiki/Convolutional_neural_network)构建，并在一个庞大的语音样本数据集上训练。在训练阶段，网络学习确定了语音的底层结构，例如哪些音调彼此相随、哪些波形是逼真的（哪些不是）。训练好的网络随后逐个采样点地合成语音，每个生成的采样点都会考虑上一个采样点的特性。由此产生的语音带有自然的语调，以及诸如咂嘴之类的其他特征。它的「口音」取决于训练所用的语音，这开启了从混合数据集中创造出任意数量独特语音的可能性。与所有文语转换系统一样，WaveNet 使用文本输入来告诉它应当针对查询生成哪些词。

用原始模型构建如此高保真的声波在计算上非常昂贵，这意味着 WaveNet 虽有前景，却无法部署到现实世界。但在过去 12 个月里，我们的团队努力开发了一个能够更快速生成波形的新模型。它现在还能大规模运行，并且是首个在[谷歌最新 TPU 云基础设施](https://www.blog.google/products/google-cloud/google-cloud-offer-tpus-machine-learning/)上发布的产品。

![](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62266baf02e48255b587a17f_WaveNet20generation.gif)

WaveNet 团队接下来将把重心转向准备一篇详细介绍新模型背后研究的论文，但结果本身已经说明一切。新的、改进后的 WaveNet 模型仍然生成原始波形，但速度比原始模型快 1000 倍——这意味着它只需 50 毫秒就能生成一秒的语音。事实上，该模型不仅更快，保真度也更高，能够生成每秒 24000 个采样点的波形。我们还将每个采样点的分辨率从 8 位提高到了 16 位——与激光唱片（CD）相同的分辨率。

根据人类听者的测试，这使新模型的听感更加自然。例如，新的美式英语语音 I 在 1 到 5 的量表上获得了 4.347 的平均意见得分（MOS），而即使是人类语音也只得到 4.667 分。

![标题为「平均意见得分」的柱状图，对比「当前最佳非 WaveNet」与「WaveNet」在四种语音上的表现：美式英语语音 I（4.186 对 4.347；训练数据 65 小时）、美式英语语音 II（4.089 对 4.314；训练数据 21 小时）、美式英语第三方语音（3.418 对 3.966；训练数据 9 小时）和日语语音（4.072 对 4.236；训练数据 28 小时）。四种情形下 WaveNet 均获得更高分数。](https://lh3.googleusercontent.com/oB2ZUCuvqvFUORBXOxhcMVE9AtTFmFBby2uQlvDb7sFhLjocuzKM3-KZe5USOyElZvnpLEyRxrTaYfAkqZekKs_8H8OtB-K8JXJLOmfNUzDF-sy-ow=w1440)

新模型还保留了原始 WaveNet 的灵活性，使我们能够在训练阶段更好地利用大量数据。具体来说，我们可以使用来自多个语音的数据来训练网络。这样，即便目标输出语音可用的训练数据很少，也能生成高质量、细腻入微的语音。

我们相信这只是 WaveNet 的起点，语音接口的力量如今能为世界上所有语言解锁的可能性令我们倍感兴奋。

**说明**

**这项工作由 DeepMind WaveNet 研究与工程团队以及谷歌文语转换团队完成。**

阅读[原始 WaveNet 博客文章](https://deepmind.com/blog/wavenet-generative-model-raw-audio/)。

阅读原始 [WaveNet 论文](https://arxiv.org/pdf/1609.03499.pdf)。

进一步了解[更新后的 Google Assistant](https://www.blog.google/products/assistant/google-assistant-powering-our-new-family-hardware/)。

**编者注：** 本文早期版本误将美式英语第三方语音的 MOS 得分写作 4.326。现已更正。
