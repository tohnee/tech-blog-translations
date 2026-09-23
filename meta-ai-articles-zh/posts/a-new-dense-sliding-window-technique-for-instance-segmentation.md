---
title: "一种用于实例分割的新型稠密滑动窗口技术"
title_en: "A new dense sliding-window technique for instance segmentation"
date: 2019-10-28
source: https://ai.meta.com/blog/a-new-dense-sliding-window-technique-for-instance-segmentation/
crawled: 2026-09-22
translated: 2026-09-22
---

# 一种用于实例分割的新型稠密滑动窗口技术

> 原文：[A new dense sliding-window technique for instance segmentation](https://ai.meta.com/blog/a-new-dense-sliding-window-technique-for-instance-segmentation/) · Meta AI（Wayback 存档）

**研究内容：**我们正在介绍一个名为 TensorMask 的新框架，它使用稠密滑动窗口技术实现非常锐利的实例分割。TensorMask 设计了新颖的架构和算子，用丰富、有效的表示来捕捉稠密图像的 4D 几何结构。这是该方法首次在定性和定量上都取得与 Facebook AI 开创性的边界框驱动框架 Mask R-CNN 相当的结果。

**工作原理：**直接的滑动窗口范式近来在边界框目标检测中复兴，使单阶段准确检测物体成为可能，而无需后续精修步骤。然而，这一方法在实例分割任务上一直不够有效，因为实例掩码是复杂的 2D 几何结构，而非简单的矩形。在 2D 规则网格上稠密滑窗时，实例掩码需要具有尺度自适应尺寸的高维 4D 张量才能有效表示。TensorMask 使用结构化的高维 4D 几何张量实现了这一点，这些张量由子张量组成，其坐标轴具有明确定义的像素单位。这些子张量支持几何上有意义的运算，如坐标变换、上下采样以及尺度金字塔的使用。相比之下，DeepMask 等以往尝试使用的是缺乏明确几何意义的非结构化 3D 张量，使其表示更难操作。

为了在滑动窗口中高效生成掩码，我们使用了多种张量表示，其中子张量表示掩码值。例如，对齐表示（aligned representation）的子张量会枚举与它重叠的所有窗口中的掩码值。正如下面的图像所示，对齐表示能够使用粗粒度子张量更好地预测更高分辨率的掩码。以往用于掩码表示的方法（自然表示与不对齐表示）要么效率较低，要么容易产生伪影。TensorMask 提出的对齐表示在稠密、重叠物体的情况下最为有效。我们用 TensorMask 框架开发了 Tensor Bipyramid（张量双金字塔）——一种自然捕捉任务几何结构的新金字塔结构：大物体在粗位置拥有高分辨率掩码，小物体在细位置拥有低分辨率掩码。最佳的 TensorMask 模型（利用 Tensor Bipyramid 结构）取得 37.1 AP（表示平均精度的标准指标），而对应的 Mask R-CNN 为 38.3 AP。

**为什么重要：**TensorMask 为探索与 Mask R-CNN 驱动的标准方法不同的实例分割研究新方向奠定了基础。有了 TensorMask，高性能实例分割不再需要边界框。这一新的互补方法有助于推动研究，把物体分割与背景分割自底向上地统一到单一模型中。这项研究将帮助我们更广泛地理解稠密掩码预测这一任务，它是我们持续创新并构建更强图像理解系统努力的重要组成部分。

阅读完整论文：TensorMask: A Foundation for Dense Object Segmentation
