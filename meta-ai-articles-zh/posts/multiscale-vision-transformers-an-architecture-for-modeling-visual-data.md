---
title: "多尺度 Vision Transformer：表示图像与视频信息的层次化架构"
title_en: "Multiscale Vision Transformers: A hierarchical architecture for representing image and video information"
date: 2019-05-22
source: https://ai.facebook.com/blog/multiscale-vision-transformers-an-architecture-for-modeling-visual-data
crawled: 2026-09-22
translated: 2026-09-22
---

# 多尺度 Vision Transformer：表示图像与视频信息的层次化架构

> 原文：[Multiscale Vision Transformers: A hierarchical architecture for representing image and video information](https://ai.facebook.com/blog/multiscale-vision-transformers-an-architecture-for-modeling-visual-data) · Meta AI（Wayback 存档）

人脑中层次化视觉表示的理念已相当成熟。1960 年，D.H. Hubel 和 T.N. Wiesel 提出了视觉通路的层次化模型：大脑较低区域（如初级视觉皮层）的神经元对朝向边缘和条形等特征做出响应，而较高区域的神经元则对更特异的刺激做出响应。几十年后，Kunihiko Fukushima 提出了 Neocognitron——一种受 Hubel 与 Wiesel 层次结构直接启发的模式识别神经网络架构。这一核心主题至今仍清晰体现在卷积神经网络中——它们对输入构建多尺度的层次化表示。

**研究内容**：Facebook AI 构建了多尺度 Vision Transformer（Multiscale Vision Transformers，MViT），一种用于从图像和视频等视觉数据进行表示学习的 Transformer 架构。它是一个视觉识别模型家族，把层次化表示这一开创性概念融入强大的 Transformer 架构。MViT 是首个可以在视频识别数据集（如 Kinetics 400）上完全从零训练，并在多种迁移学习任务（如视频分类和人体动作定位）上达到最先进性能的此类系统。面对图像或视频时，MViT 模型能识别图像中出现的物体或视频中正在进行的动作。训练好的模型在 Kinetics 和 ImageNet 分类数据集上表现优异，并能很好地迁移到下游任务，如 Charades、Something-Something 和 Atomic Visual Actions（AVA）等数据集上的动作识别。未来，把 MViT 应用于自然场景中的视频和图像，可能有助于机器更好地分析真实世界未经整理的景象，而不只是那些小得多、人工整理的数据集中的元素。

（视频说明：本视频展示了多尺度注意力图的示例：最左列为原始输入视频；左起第二列以较低分辨率显示该视频；最后四列展示 MViT 架构不同注意力头的注意力图，越往下行对应越深的层。）

**工作原理**：MViT 的核心进展是在 Transformer 骨干内部构建时空特征层次。典型的 Vision Transformer 模型在所有层使用恒定的分辨率和特征维度，并依靠注意力机制决定应关注之前的哪些 token。在 MViT 中，我们以池化注意力机制取而代之，对投影后的查询（query）、键（key）和值（value）向量进行池化，从而降低视觉分辨率。我们将其与通道维度的增加相结合，构建出一个从高视觉分辨率的简单特征到低分辨率、高维复杂特征的层次结构。

（视频说明：多尺度 Vision Transformer 学习一个从视觉上致密、通道上简单，到粗糙、复杂的特征层次。若干「分辨率-通道」尺度阶段在逐步提升中间隐序列通道容量的同时，池化其长度并因此降低视觉分辨率。）

**为什么重要**：MViT 标志着对以往基于 Transformer 的视频理解尝试的重大改进——后者需要在海量数据集（如 ImageNet-21K）上进行计算昂贵的预训练，参数极为密集，且需要多步训练方案。相比之下，MViT 无需外部预训练，单步从零训练。它还在 ImageNet、Kinetics-400、Kinetics-600、AVA 等被充分研究的识别基准上显著提升了最先进性能。此外，MViT 模型展现出对时间线索的出色理解，而不会陷入虚假的空间偏差——这是以往方法的常见陷阱。虽然还有大量工作要做，但 MViT 带来的进展可以显著改进对人体动作的细致理解，而这对于机器人和自动驾驶车辆等真实世界 AI 应用是关键组件。此外，视频识别架构的创新是鲁棒、安全、以人为本 AI 的重要组成部分。

**在 GitHub 获取**：查看 PySlowFast 仓库获取代码，并到 Model Zoo 体验预训练模型！该模型很快将可通过 PyTorchVideo 供任何框架使用。

**致谢**：我们感谢与 Chao-Yuan Wu、Ross Girshick 和 Kaiming He 的讨论，以及 Chen Wei 在可视化方面的帮助。

阅读完整论文

作者：Karttikeya Mangalam，访问研究员；Haoqi Fan，研究工程师；Bo Xiong，研究工程师；Yanghao Li，研究工程师；Jitendra Malik，研究总监；Christoph Feichtenhofer，研究科学家
