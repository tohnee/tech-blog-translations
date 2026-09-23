---
title: "数据高效图像 Transformer：一种前景可观的新图像分类技术"
title_en: "Data-efficient image Transformers: A promising new technique for image classification"
date: 2020-12-23
source: https://ai.facebook.com/blog/data-efficient-image-transformers-a-promising-new-technique-for-image-classification
crawled: 2026-09-22
translated: 2026-09-22
---

# 数据高效图像 Transformer：一种前景可观的新图像分类技术

> 原文：[Data-efficient image Transformers: A promising new technique for image classification](https://ai.facebook.com/blog/data-efficient-image-transformers-a-promising-new-technique-for-image-classification) · Meta AI（Wayback 存档）

2020 年 12 月 23 日

## 这项研究是什么

我们开发了一种训练计算机视觉模型的新方法，利用 Transformer 这一突破性深度神经网络架构——它近来在 AI 的许多领域解锁了戏剧性的进展。Transformer 模型已在自然语言处理和机器翻译中产出了最先进的结果，Facebook AI 还用该架构在其他任务上取得突破，例如语音识别、符号数学以及编程语言之间的翻译。但 AI 研究社区才刚刚开始将 Transformer 引入计算机视觉领域，例如 Facebook AI 今年早些时候发布的 DETR 目标检测架构。

我们的新技术——数据高效图像 Transformer（DeiT）——只需少得多的数据和计算资源即可产出高性能图像分类模型。仅用一台 8-GPU 服务器训练 3 天，我们在广泛使用的 ImageNet 基准上取得了 84.2 的 top-1 准确率，且训练未使用任何外部数据。这一结果与前沿卷积神经网络（CNN）的性能相当，而后者多年来一直是图像分类的主导方法。通过展示 Transformer 可以仅用常规学术数据集就高效训练用于图像分类，我们希望推进计算机视觉领域，将 Transformer 扩展到新的用例，并让无法使用大规模系统训练巨型 AI 模型的研究者和工程师也能接触这项工作。

DeiT 是与索邦大学的 Matthieu Cord 教授合作开发的。我们现在开源代码并发表研究，以便他人复现我们的结果并在此基础上继续构建。

（原文此处附图：该图展示我们的方法（DeiT 以及带蒸馏的 DeiT）与此前视觉 Transformer 模型及现代最先进 CNN 的性能曲线对比。图中模型均在 ImageNet 上训练。）

## 它是如何工作的

图像分类——理解图像主要内容的任务——对人类容易，对机器却很难。尤其对于 DeiT 这类无卷积的 Transformer，这更具挑战性，因为这些系统没有多少关于图像的统计先验：它们通常需要「看」大量示例图像才能学会分类不同物体。而 DeiT 仅用 120 万张图像即可有效训练，而不需要数亿张。

DeiT 的第一个重要要素是它的训练策略。我们在最初为卷积神经网络开发的已有研究基础上进行了构建与改造。具体而言，我们使用了数据增强、优化和正则化来模拟在更大得多的数据集上训练。同样重要的是，我们修改了 Transformer 架构以支持原生蒸馏。蒸馏是一个神经网络（学生）从另一个网络（教师）的输出学习的过程。我们用 CNN 作为 Transformer 的教师模型。由于 CNN 架构具有更多关于图像的先验，它可以用相对较少的图像训练。使用蒸馏可能损害神经网络的性能。学生模型追求两个可能相互背离的目标：从标注数据集学习（强监督）和从教师学习。为缓解这一问题，我们引入了蒸馏 token——一个与变换后的图像数据一起在网络中流动的可学习向量。蒸馏 token 为模型的蒸馏输出提供提示，该输出可以与其类别输出不同。这种新的蒸馏方法为 Transformer 特有，进一步提升了图像分类性能。

（原文此处附图：我们在 Transformer 中加入一个蒸馏 token。它通过注意力层与分类向量和图像组件 token 交互。该蒸馏 token 的目标是从教师模型（一个 CNN）学习。）

## 为什么它重要

DeiT 是用 Transformer 推进计算机视觉的重要一步。它的性能已经与 CNN 相当，尽管后者在过去八年一直是计算机视觉任务的主导方法，并受益于大量改进与调整。我们希望这预示着进一步研究将带来显著的额外收益。

这项工作还将帮助 AI 研究平民化。DeiT 表明，数据与计算资源有限的开发者也能够训练或使用这些新模型。我们希望它能帮助更广大社区的研究者取得进展。

**阅读论文并获取代码：**

- 代码地址：https://github.com/facebookresearch/deit
- 论文地址：Training data-efficient image transformers and distillation through attention

**作者**

- Hugo Touvron，研究助理
- Matthijs Douze，研究科学家
- Francisco Massa，研究工程师
- Alex Sablayrolles，研究科学家
- Hervė Jegou，研究科学总监
