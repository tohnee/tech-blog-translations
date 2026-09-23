---
title: "为数百种罕见物体类别实现高效精准的目标检测"
title_en: "Efficient, accurate object detection for hundreds of uncommon object classes"
date: 2022-08-01
source: https://ai.facebook.com/blog/efficient-accurate-object-detection-for-hundreds-of-uncommon-object-classes
crawled: 2026-09-22
translated: 2026-09-22
---

# 为数百种罕见物体类别实现高效精准的目标检测

> 原文：[Efficient, accurate object detection for hundreds of uncommon object classes](https://ai.facebook.com/blog/efficient-accurate-object-detection-for-hundreds-of-uncommon-object-classes) · Meta AI（Wayback 存档）

2022 年 8 月 1 日

## 这项研究是什么

Meta AI 正在分享关于用视觉 Transformer（ViT）做目标检测的新研究。我们的方法 ViTDet 在大词汇实例分割（LVIS）数据集的基准上超越了以往的替代方案——该数据集由 Meta AI 研究者于 2019 年发布，用于促进低样本目标检测研究。在这项任务中，模型必须学会识别比常规计算机视觉系统广泛得多的物体种类。ViTDet 在准确识别 LVIS 数据集中的物体方面超越了以往基于 ViT 的模型——该数据集不仅包含桌椅等标准物品，还有鸟食罐、花环、甜甜圈等等。为了让研究社区能够复现并在这些进展之上继续构建，我们现在将 ViTDet 代码和训练配方作为新的基线发布到我们的开源 Detectron2 目标检测库中。

## 它是如何工作的

过去一年，ViT 已被确立为视觉识别的强大主干。与典型的卷积神经网络不同，原始 ViT 是一个朴素、非分层的架构，在整个处理过程中保持单一尺度的特征图。然而，将 ViT 应用于目标检测时会遇到挑战。例如，如何用朴素主干有效检测多尺度物体？ViT 用于高分辨率图像的目标检测是否过于低效？与 Swin 和 MViTv2 等现有研究不同，ViTDet 只使用朴素的非分层 ViT 主干。它从 ViT 输出的单一尺度特征图构建一个简单特征金字塔，并主要使用简单的不重叠窗口注意力来高效提取高分辨率图像的特征。这一设计将 ViT 的预训练与检测的微调需求解耦，从而使目标检测器能够受益于现成可用的预训练掩码自编码器（MAE）模型。

（原文此处附图：ViTDet 从一个朴素、非分层视觉 Transformer 的输出构建简单特征金字塔。其检测器特定设计与 ViT 主干的解耦，使其能够受益于掩码自编码器（MAE）预训练。）

我们首先按照 Mask R-CNN 框架，用基础（B）、大型（L）和巨型（H）尺寸的 ViT 主干训练 ViTDet 检测器。我们评估两种预训练策略：监督预训练和自监督 MAE 预训练（监督预训练的 ViT-H 模型权重不可得）。我们用掩码平均精度（Mask AP）和稀有类别上的掩码平均精度（Mask AP-rare）衡量 LVIS 上的准确率。由于每个稀有类别只有 10 个或更少的训练样本，在稀有类别上取得良好性能颇具挑战。我们有两个主要观察：

- 与监督预训练相比，随着 ViTDet 的 ViT 主干规模扩大，MAE 预训练带来更好的 LVIS 结果。我们观察到稀有类别检测的 Mask AP 显著提升——这正是 LVIS 提出的低样本检测问题的核心。将 MAE 预训练的 ViT 主干从基础扩展到大型时，Mask AP 可以从 38.1 提升到 43.5（+5.4），而扩展监督预训练的 ViT 主干仅有 +1.1 的 Mask AP 提升。
- 采用 ViT-H 主干的 ViTDet 在 Mask R-CNN 中可以达到 45.9 的 Mask AP 和 37.9 的 Mask AP-rare，十分出色。

我们还用其他最近提出的分层 ViT 主干对 Mask R-CNN 做了基准测试，包括 Swin 和 MViTv2。Swin 和 MViTv2 在 ImageNet-1K 和 ImageNet-21K 上以监督方式预训练。只要可用，我们分别为基础（B）、大型（L）和巨型（H）尺寸的每种主干搜索最优配方。在所有被基准测试的主干中，MAE 预训练的 ViTDet 具有最佳的扩展行为，并在 LVIS 上交付最佳性能。

（原文此处附图：不同主干在 Mask R-CNN 中的目标检测器在 LVIS 上的基准结果。ViTDet-H 以 ImageNet-1K 自监督 MAE 预训练达到 45.9 Mask AP。）

## 为什么它重要

目标检测是一项重要的计算机视觉任务，应用范围涵盖自动驾驶、电子商务到增强现实。为了让目标检测更有用，CV 系统需要识别不常见物体以及训练数据中极少出现的物体。有了 ViTDet，我们现在看到了一个转折点：作为低样本目标检测挑战的基准数据集，LVIS 从更大的主干和更好的预训练中显著受益。我们希望通过开源我们用 ViTDet 建立的强劲新基线，帮助研究社区进一步推进最新水平，构建更有效的 CV 系统。

**阅读论文**　**基准结果**　**训练配方**

**作者**

- Hanzi Mao，研究科学家
- Yanghao Li，研究工程师
- Kaiming He，研究科学家
- Ross Girshick，研究科学家
