---
title: "推出 Temporal 数据集：识别视频中动作的基准"
title_en: "Introducing the Temporal dataset, a benchmark for recognizing actions in videos"
date: 2019-03-15
source: https://ai.facebook.com/blog/introducing-the-temporal-data-set-a-benchmark-for-recognizing-actions-in-videos
crawled: 2026-09-22
translated: 2026-09-22
---

# 推出 Temporal 数据集：识别视频中动作的基准

> 原文：[Introducing the Temporal dataset, a benchmark for recognizing actions in videos](https://ai.facebook.com/blog/introducing-the-temporal-data-set-a-benchmark-for-recognizing-actions-in-videos) · Meta AI（Wayback 存档）

**这项研究是什么：**一个用于训练 AI 系统并为其建立基准的新数据集，帮助其更好地理解视频中的动作——尤其是那些仅凭单帧画面无法判定的动作。目前的视频数据集往往聚焦于单张图像就足以识别的动作，比如洗碗、吃披萨或弹吉他。为了改进计算机视觉系统对那些只有在视频序列中才能识别的元素的理解——比如某人是在打喷嚏还是在开门——我们发现了一组动作，对它们的识别而言时序信息必不可少。我们现在分享这项工作，包括确定这些类别的方法论以及在其上训练网络的结果，以帮助研究者为其系统识别时序动作的能力建立基准。

**工作原理：**为发现视频中的哪些动作应被划为「时序类别」，我们向标注者展示来自现有视频识别数据集的视频片段，但帧序被打乱。如果标注者无法识别某个动作，我们就认定时序信息对其识别至关重要，并将该类别加入数据集。我们总共发现了 50 个这样的时序动作类别，关联到来自 Kinetics 与 Something-Something 基准的 35,504 个公开视频。我们最终得到的类别列表称为 Temporal 数据集，它并不包含视频内容本身，而是由与这些基准中特定片段相关联的类别组成。为评估数据集的效用，我们用它为当前的视频识别方法建立基准，发现一些最先进的网络捕捉到的图像信息多于时序信息。我们还用这个新的 Temporal 数据集训练现有的视频识别网络，发现它们对时序变化更敏感、对图像信息的依赖更低，从而提升了泛化到未见过的动作类别的能力。

**为什么重要：**我们的训练结果表明，纳入时序数据可以提升视频理解系统的整体表现。但我们的工作也提示，当前的视频数据集低估了那些时序信息对理解至关重要的类别，这可能使进展偏向图像理解，而非那些只有视频中才能识别的动作的理解。我们的数据集并非单独的可下载资源，可在下面论文的附录中找到。它将帮助研究者评估并改进系统利用时序信息的能力，同时推动该领域把时序信息纳入未来的视频数据集。

阅读完整论文：Only time can tell: Discovering temporal data for temporal modeling
