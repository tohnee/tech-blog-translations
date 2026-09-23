---
title: "用 PyTorch3D 构建 3D 深度学习模型"
title_en: "Building 3D deep learning models with PyTorch3D"
date: 2020-06-12
source: https://ai.facebook.com/blog/building-3d-deep-learning-models-with-pytorch3d
crawled: 2026-09-22
translated: 2026-09-22
---

# 用 PyTorch3D 构建 3D 深度学习模型

> 原文：[Building 3D deep learning models with PyTorch3D](https://ai.facebook.com/blog/building-3d-deep-learning-models-with-pytorch3d) · Meta AI（Wayback 存档）

正如 Torchvision 和 Detectron2 为 2D 计算机视觉提供了高度优化的库一样，PyTorch3D 提供了支持 3D 数据的各种能力。我们的这个 3D 深度学习开源库包括：对异构网格（mesh）和点云的便捷批处理支持、对常见 3D 算子（如 Chamfer Loss 和 Graph Conv）的优化实现，以及一个面向点云与网格的模块化可微分渲染器。我们已经在 Facebook 的 Mesh R-CNN 和 SynSin 等研究项目中使用 PyTorch3D。

自 2020 年 2 月首次发布以来，我们新增了多项功能，包括点云渲染、点到网格距离、快速 KNN、法向估计等。这些算子都支持批处理，经过优化且可微分，可以直接接入深度学习流水线。

你可以通过 PyTorch3D 联合创造者、软件工程师 Nikhila Ravi 的这段视频进一步了解它的工作原理。可以在这里试用代码和教程，也可以在这里阅读更多关于 PyTorch3D 的内容。欢迎参加我们在 CVPR 2020 上举办的「图像、视频与 3D 视觉识别」教程。
