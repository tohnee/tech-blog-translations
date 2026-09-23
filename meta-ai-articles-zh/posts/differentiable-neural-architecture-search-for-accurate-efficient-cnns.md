---
title: "面向精准高效 CNN 的可微神经架构搜索"
title_en: "Differentiable neural architecture search for accurate, efficient CNNs"
date: 2019-03-15
source: https://ai.facebook.com/blog/differentiable-neural-architecture-search-for-accurate-efficient-cnns
crawled: 2026-09-22
translated: 2026-09-22
---

# 面向精准高效 CNN 的可微神经架构搜索

> 原文：[Differentiable neural architecture search for accurate, efficient CNNs](https://ai.facebook.com/blog/differentiable-neural-architecture-search-for-accurate-efficient-cnns) · Meta AI（Wayback 存档）

## 这项研究是什么

一个提出的可微神经架构搜索（DNAS）框架，使用基于梯度的方法优化卷积神经网络（CNN）架构。我们需要既精准（以支持更好的产品能力和用户体验）又高效（以让我们把服务交付给更多没有高端手机的人）的 CNN。但为移动设备设计精准高效的 CNN 颇具挑战，因为设计空间在组合意义上极其庞大。以往的神经架构搜索（NAS）方法计算开销很大。在 CNN 架构中，最优性取决于输入分辨率和目标设备等因素，这需要逐案重新设计。以往工作还主要聚焦于减少 FLOPs，但 FLOP 数量并不总能反映实际延迟。借助我们新提出的框架，不再需要分别枚举并训练单个架构，使流程更快、更针对真实设备的约束。我们介绍了 FBNet——一个由 DNAS 发现的优化 CNN 架构，超越了手工设计的和自动生成的最先进模型。

## 它是如何工作的

DNAS 允许我们探索逐层的搜索空间，使每一层可以从候选池中选择不同的算子。搜索空间由一个随机超网表示。超网的每一层包含若干并行的候选算子，按某种分布采样执行。为搜索最优架构，我们训练随机超网来优化架构分布——更频繁地采样那些有助于提升准确率的低成本算子。算子的计算负载可以用其 FLOP 数量、参数规模或其在目标设备上实测的延迟来度量。训练完成后，我们就可以从训练好的分布中采样最优架构。该过程如下图所示。

（原文此处附图：用于高效 CNN 设计的 DNAS 流程。）

## 为什么它重要

DNAS 提供了一个自动设计新 CNN 架构的快速强大工具。搜索空间可以包含任意算子，例如卷积、最大池化或量化卷积，这使我们可以将 DNAS 应用于不同问题，包括混合精度量化和高效 CNN 搜索。搜索过程极快，通常 8 块 GPU 24 小时即可完成，计算资源效率比其他方法高 420 倍。DNAS 支持直接针对目标设备的实际延迟进行优化，而我们的方法发现的 CNN 超越了此前最佳水平。

**阅读完整论文：** FBNet: Hardware-aware efficient ConvNet design via differentiable neural architecture search

参见这项工作在 CVPR 2019 上的展示。
