---
title: "AI 加持：用卷积神经网络把任意 2D 照片变成 3D"
title_en: "Powered by AI: Turning any 2D photo into 3D using convolutional neural nets"
date: 2020-02-28
source: https://ai.facebook.com/blog/-powered-by-ai-turning-any-2d-photo-into-3d-using-convolutional-neural-nets
crawled: 2026-09-22
translated: 2026-09-22
---

# AI 加持：用卷积神经网络把任意 2D 照片变成 3D

> 原文：[Powered by AI: Turning any 2D photo into 3D using convolutional neural nets](https://ai.facebook.com/blog/-powered-by-ai-turning-any-2d-photo-into-3d-using-convolutional-neural-nets) · Meta AI（Wayback 存档）

我们的 [3D 照片功能](https://www.facebook.com/help/414295416095269)于 2018 年在 Facebook 上线，是一种与亲朋好友分享图片的全新沉浸式格式。然而该功能一直依赖仅在新款高端智能手机上才有的双镜头「人像模式」能力，因此在只有单个后置摄像头的普通移动设备上无法使用。为了让这一新的视觉格式惠及更多人，我们利用最先进的机器学习技术，从几乎任意标准 2D 图片生成 3D 照片。该系统能推断任意图像的 3D 结构——无论是刚用标准单摄像头的 Android 或 iOS 设备拍摄的新照片，还是最近上传到手机或笔记本电脑上的几十年前的老照片。

这一进展首次让数千万使用单镜头手机或平板的人群能够轻松用上 3D 照片技术。它还让每个人都能以全新的方式体验几十年前的家庭老照片和其他珍贵影像——只需把它们转换成 3D。拥有最先进双摄像头设备的用户同样可以受益：现在可以用单个前置摄像头拍摄 3D 自拍。任何 iPhone 7 或更高机型、或近年中端及以上 Android 设备的用户，现在都可以在 Facebook 应用中试用这些选项。

![](https://static.xx.fbcdn.net/rsrc.php/v3/y4/r/-PAXP-deijE.gif)

（原文此处嵌入视频，展示如何估计 2D 图片中不同区域的深度以创建 3D 图像。）

构建这一增强版 3D 照片技术需要克服各种技术挑战，例如训练一个能正确推断极广泛题材 3D 位置的模型，以及优化系统使其能在典型移动处理器上以几分之一秒的时间在设备端运行。为克服这些挑战，我们在数百万对公开 3D 图像及其配套深度图上训练了一个卷积神经网络（CNN），并利用了 Facebook AI 此前研发的多种移动优化技术，例如 [FBNet](https://ai.facebook.com/blog/differentiable-neural-architecture-search-for-accurate-efficient-cnns/) 和 [ChamNet](https://ai.facebook.com/blog/platform-aware-ai-to-design-neural-networks/)。（我们还曾在此处讨论近期[相关的 3D 理解研究](https://ai.facebook.com/blog/pushing-state-of-the-art-in-3d-content-understanding/)。）

如今这一功能已面向所有 Facebook 用户开放，我们在此分享它的构建细节。

![](https://static.xx.fbcdn.net/rsrc.php/v3/y4/r/-PAXP-deijE.gif)

（原文此处嵌入视频。小狗的原始照片由单镜头相机拍摄，不含任何深度图数据；我们的系统把它转换成了此处展示的 3D 图像。）

## 在移动设备上实现高效性能

给定一张标准 RGB 图像，3D 照片 CNN 可以估计每个像素到相机的距离。我们通过四种手段实现这一点：

- 采用一组可参数化、面向移动端优化的神经构件搭建的网络架构。
- 自动化架构搜索以找到这些构件的有效配置，使系统能在广泛多样的设备上不到一秒内完成任务。
- 量化感知训练，以便在移动端利用高性能 INT8 量化的同时，尽量减少量化过程带来的潜在质量损失。
- 来自公开 3D 照片的海量训练数据。

## 神经构件

我们的架构使用了受 [FBNet](https://l.facebook.com/l.php?u=https%3A%2F%2Fresearch.fb.com%2Fpublications%2Ffbnet-hardware-aware-efficient-convnet-design-via-differentiable-neural-architecture-search%2F&h=AT0xnZEZj9joq4tfeR9LAa3iMXM2IEI6mabKtHioDh8yGhXlmvGpAgxkLM_pt1-AE9TYJ0dN6f_gMyqt4yUy7UzPzQe6OUV5yRW0n3wK9yhR-bZ9_Sj-2nxYeaN7umiix83AUHEs-sb5pQhj) 启发的构件——FBNet 是一个为移动端及其他资源受限设备优化 ConvNet 架构的框架。一个构件由逐点卷积、可选的上采样、K x K 深度卷积和一个额外的逐点卷积组成。我们实现了一个经过修改的 U-net 风格架构，把 FBNet 构件放置在跳跃连接上。U-net 的编码器和解码器各包含五个阶段，每个阶段对应一种不同的空间分辨率。

![](https://static.xx.fbcdn.net/rsrc.php/v3/y4/r/-PAXP-deijE.gif)

（原文此处嵌入视频。）我们的网络架构概览。它是一个在跳跃连接上额外放置了宏级构件的 U-net。

## 自动化架构搜索

为了找到有效的架构配置，我们使用 Facebook AI 开发的 [ChamNet](https://l.facebook.com/l.php?u=https%3A%2F%2Fresearch.fb.com%2Fpublications%2Fchamnet-towards-efficient-network-design-through-platform-aware-model-adaptation%2F&h=AT2oa7UsOPhibXtzPW6sjjdTS1Jz8ciG0bbHIKxGT1QyolF0L8C4w9fjbOOiZ1AhMtF7HZuQFdipRGeRhVcNIU6LW8qUK7qdiADFgQ_rB6mzeQKDzSvO7RHUEyL77XZQZ80IYhTdPVeBE0UT) 算法将搜索过程自动化。ChamNet 算法迭代地从搜索空间中采样点来训练一个准确率预测器。该准确率预测器用于加速遗传搜索，以在满足指定资源约束的前提下找到预测准确率最大化的模型。在这一场景中，我们使用的搜索空间会改变每个块的通道扩张因子和输出通道数，产生约 3.4x10^22 种可能的架构。随后我们用 800 块 Tesla V100 GPU 在大约三天内完成了搜索，通过设定并调整模型架构上的 FLOP 约束来达到不同的工作点。

## 量化感知训练

默认情况下，我们的模型使用单精度浮点权重和激活进行训练，但我们发现把权重和激活都量化为仅 8 位有显著优势。具体而言，int8 权重只需 float32 权重四分之一的存储空间，从而减少首次使用时必须传输到设备的字节数。

![](https://static.xx.fbcdn.net/rsrc.php/v3/y4/r/-PAXP-deijE.gif)

（原文此处嵌入视频。这些图像原本都是普通 2D 图像，经我们的深度估计神经网络转换为 3D。）

得益于调优良好的库（如已集成到 PyTorch 中的 Facebook AI [QNNPACK](https://ai.facebook.com/blog/qnnpack-open-source-library-for-optimized-mobile-deep-learning/)），基于 int8 的算子相较 float32 对应算子的吞吐量也高得多。我们使用量化感知训练（QAT）来避免量化导致不可接受的质量下降。[QAT 现已成为 PyTorch 的一部分](https://l.facebook.com/l.php?u=https%3A%2F%2Fpytorch.org%2Fdocs%2Fstable%2Fquantization.html&h=AT0m-NwEMaaNkzGG80kOXnL9RrSdeIKxN9gdMKg1MdZ1O0WBHUGgu6L15M9py904MGaZCJkVV-FDH87KxYzoeXVDnwghb4eJjUiA--No_NnrhfLGPDLN06WNUugZudHh6quluLPUCav7atea)，它在训练期间模拟量化并支持反向传播，从而消除训练与生产性能之间的差距。

![](https://static.xx.fbcdn.net/rsrc.php/v3/y4/r/-PAXP-deijE.gif)

（原文此处嵌入视频。我们的神经网络适用于多种内容，包括绘画和复杂场景图像。特雷维喷泉照片由 Livioandronic2013 拍摄，以 https://creativecommons.org/licenses/by-sa/4.0/ 许可证共享。）

## 探索创造 3D 体验的新方式

除了继续打磨和改进我们的深度估计算法，我们还在努力为移动设备拍摄的视频实现高质量深度估计。视频带来了值得注意的挑战，因为每一帧的深度都必须与下一帧保持一致。但这同时也是提升性能的机会，因为同一物体的多次观察可以为高精度深度估计提供额外信号。视频长度的深度估计将为我们的用户开启各种创新的内容创作工具。随着我们持续改进神经网络的性能，我们还将探索在增强现实等实时应用中利用深度估计、表面法线估计和空间推理。

除了这些潜在的新体验之外，这项工作还将帮助我们更普遍地理解 2D 图像的内容。对 3D 场景更好的理解也可以帮助机器人在物理世界中导航和交互。我们希望通过分享 3D 照片系统的细节，帮助 AI 社区在这些领域取得进展，并利用先进的 3D 理解创造新体验。

## 作者

- Kevin Matzen，研究科学家
- Matthew Yu，软件工程师
- Jonathan Lehman，软件工程师
- Peizhao Zhang，研究科学家
- Jan-Michael Frahm，研究科学家经理
- Peter Vajda，研究科学家经理
- Johannes Kopf，研究科学家经理
- Matt Uyttendaele，工程总监

## 相关文章

- [Introducing PyTorch3D: An open-source library for 3D deep learning](https://ai.facebook.com/blog/-introducing-pytorch3d-an-open-source-library-for-3d-deep-learning/)（2020 年 2 月 6 日）
- [Pushing the state of the art in 3D content understanding](https://ai.facebook.com/blog/pushing-state-of-the-art-in-3d-content-understanding/)（2019 年 10 月 29 日）
- [A new dense, sliding-window technique for instance segmentation](https://ai.facebook.com/blog/a-new-dense-sliding-window-technique-for-instance-segmentation/)（2019 年 10 月 28 日）

## 相关标签

- [ML Applications](https://ai.facebook.com/blog/results/ml-applications/)（机器学习应用）
- [Computer Vision](https://ai.facebook.com/blog/results/computer-vision/)（计算机视觉）
- [Research](https://ai.facebook.com/blog/results/research/)（研究）
