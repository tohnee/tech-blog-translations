---
title: "用视频中的视觉锚定实现无监督词语翻译"
title_en: "Visual Grounding in Video for Unsupervised Word Translation"
source: https://deepmind.google/blog/visual-grounding-in-video-for-unsupervised-word-translation/
site: deepmind
date: 2020-03-11
crawled: 2026-09-13
translated: 2026-09-13
---

# 用视频中的视觉锚定实现无监督词语翻译

> 原文：[Visual Grounding in Video for Unsupervised Word Translation](https://deepmind.google/blog/visual-grounding-in-video-for-unsupervised-word-translation/) · Google DeepMind

## 通过不配对的带解说视频翻译词语

机器翻译最常见的方法依赖于成对或平行的语料库的监督：源语言中的每个句子都与目标语言中的译文配对。这有局限性，因为对世界上大多数语言而言，我们无法获得这样的配对语料库。有趣的是，双语儿童可以在不同时接触两种语言的情况下学会这两种语言。他们可以利用情境之间的视觉相似性：周一听到「the dog is eating」时观察到的情境，与周五听到「le chien mange」时看到的情境是相似的。

在这项工作中，我们受双语儿童启发，开发了一个模型，它通过利用词语出现情境之间的视觉相似性，学会把词语从一种语言翻译成另一种语言。更具体地说，我们的训练数据集由用不同语言解说的、互不重叠的视频集合组成。这些视频共享相似的主题（例如煮意大利面或换轮胎）；例如，数据集中既有用韩语解说的关于如何煮意大利面的视频，也有一组主题相同但用英语解说的不同视频。请注意，不同语言的视频之间并不配对。

我们的模型通过把视频与其对应的解说关联到一个跨语言的共享嵌入空间中，来利用视频之间的视觉相似性。模型的训练在一种语言解说的视频与第二种语言解说的视频之间交替进行。得益于这样的训练流程，并且由于我们在两种语言之间共享视频表示，我们的模型学到了一个联合的双语-视觉空间，把两种不同语言中的词语对齐起来。

![一张示意图，展示 MUVE 模型架构：在共享的视觉-双语空间中，把英文文本嵌入与对应的视频嵌入对齐。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6228bf8f779b4968925406fe_Fig201.gif)

## MUVE：用视觉改进纯语言方法

我们证明了我们的方法 MUVE（Multilingual Unsupervised Visual Embeddings，多语言无监督视觉嵌入）可以补充现有的、在非配对语料上训练但不使用视觉的翻译技术。通过这样做，我们展示了无监督词语翻译质量的提升，最显著的是在纯语言方法最吃力的情形下，例如：（i）两种语言差异极大（如英语与韩语、英语与日语）；（ii）初始语料库在两种语言中具有不同的统计特性；或（iii）可用的训练数据有限。

我们的发现表明，在缺少配对数据时，利用视频等视觉数据是改进双语翻译模型的一个有前景的方向。
