---
title: "通过全景分割改进场景理解"
title_en: "Improving scene understanding through panoptic segmentation"
date: 2019-04-18
source: https://ai.meta.com/blog/improving-scene-understanding-through-panoptic-segmentation
crawled: 2026-09-22
translated: 2026-09-22
---

# 通过全景分割改进场景理解

> 原文：[Improving scene understanding through panoptic segmentation](https://ai.meta.com/blog/improving-scene-understanding-through-panoptic-segmentation) · Meta AI（Wayback 存档）

2019 年 4 月 18 日

**研究内容：**一种新的目标识别方法，使用单一神经网络同时识别独立的前景物体（如动物或人，这一任务称为实例分割），并对图像背景的像素打上类别标签（如道路、天空或草地，这一任务称为语义分割）。以往研究大多使用不同类型的网络架构分别探索这两个分割任务，而我们的工作表明，两项任务可以在一个统一架构中完成。这一新方法内存和计算高效，并为最近提出的全景分割任务——把语义分割与实例分割合并为一个组合任务——确立了强有力的基线性能。

**工作原理：**新架构为 Mask R-CNN——Facebook 研究者 2017 年开发的广泛使用的实例分割系统——配备了一个语义分割分支，二者共享特征金字塔网络（FPN）骨干。这一称为 Panoptic FPN 的架构可以并行生成语义分割和实例分割，精度与训练两个独立的单任务模型相当，而总计算量大约减半。我们的测试还表明，当 Panoptic FPN 获得与两个独立网络相同的计算资源时，它在 COCO 和 Cityscapes 图像识别基准上显著优于各自的独立网络。

**为什么重要：**除了证明单网络全景分割方法既有效又易于实现之外，这项工作还为未来研究确立了基线。降低丰富而连贯的图像分割所需的内存和计算开销，对必须在物体移动、重叠的杂乱真实世界环境中理解图像的识别系统可能产生广泛影响。把前景物体与背景一起分割，对于理解完整场景以及执行相关行动（例如在场景中的动态要素之间导航）十分重要。

阅读完整论文：Panoptic feature pyramid networks
