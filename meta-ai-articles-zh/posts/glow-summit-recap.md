---
title: "Glow 峰会回顾"
title_en: "Glow Summit recap"
date: 2019-04-04
source: https://ai.facebook.com/blog/glow-summit-recap
crawled: 2026-09-22
translated: 2026-09-22
---

# Glow 峰会回顾

> 原文：[Glow Summit recap](https://ai.facebook.com/blog/glow-summit-recap) · Meta AI（Wayback 存档）

2019 年 4 月 4 日

在首届 Glow 峰会上，我们汇聚了领先的硬件组织，共同探讨 Glow——一个面向神经网络硬件加速器的机器学习（ML）编译器——的未来。Glow 的开发旨在驱动不同硬件公司的各类硬件加速器。活动期间，Habana 和 Facebook 宣布了 Glow 编译器与运行时的首个实验性后端，面向 Habana 现有的 Goya 推理加速器。该后端代码现已作为 Glow 仓库的一部分提供，Habana 的客户可以使用 PyTorch 和 Glow 来驱动他们的硬件加速器。

（Facebook 软件工程师 Roman Levenstein 在 Glow 峰会上演讲。）

我们介绍了下一阶段开发迭代的路线图，包括 Glow 运行时——在服务器级机器上跨多块加速卡排队并执行推理请求的软件组件。我们还分享了当前的 Caffe2 集成情况，并介绍了支持 PyTorch 1.0 非 Caffe 接口的计划。机器学习专家介绍了他们在量化（quantization，即把神经网络从浮点运算转换为整数运算的过程）方面的工作，PyTorch 工程师则介绍了 PyText 和基于语言的模型。

## 关于 Glow

面向 ML 的硬件加速器为解决各种不同问题而设计：一些专注推理，另一些专注训练。Glow 专为面向广泛的硬件加速器而设计。编译器中与硬件无关的部分专注于与特定硬件型号无关的数学相关优化。除了与目标无关的优化之外，Glow 还包含一系列可配置以支持多种硬件目标的工具和构建模块。例如，编译器的内存分配器可为具有不同内存配置的多种硬件加速器生成高效代码。这些能力包括一个强大的线性代数优化器、一个覆盖广泛的测试套件、一个用于测试硬件加速器精度的基于 CPU 的参考实现，以及内存分配器、指令调度器等。使用 Glow 的硬件伙伴可以缩短产品上市时间。依赖既有的优化与能力可减少开发时间，而广泛的测试套件则增强了硬件提供商对编译器精度及其与 PyTorch 规范一致性的信心。

## 下一步

Glow 和 PyTorch 团队正在与业界伙伴一起启用第一代推理硬件加速器。这项工作包括为每个加速器目标构建新的硬件后端，并对生成的代码进行验证和优化。随着 PyTorch 的持续演进，我们还计划改进与 PyTorch 的互操作性。我们很高兴能在 GitHub 上以开放方式开发 Glow，期待借助社区反馈改进 Glow，并与硬件厂商合作支持新的硬件加速器。请从 Glow GitHub 项目开始。
