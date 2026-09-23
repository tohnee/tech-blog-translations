---
title: "DeepFovea：在 AR/VR 中用深度学习实现注视点重建"
title_en: "DeepFovea: Using deep learning for foveated reconstruction in AR-VR"
date: 2019-11-18
source: http://ai.facebook.com/blog/deepfovea-using-deep-learning-for-foveated-reconstruction-in-ar-vr
crawled: 2026-09-22
translated: 2026-09-22
---

# DeepFovea：在 AR/VR 中用深度学习实现注视点重建

> 原文：[DeepFovea: Using deep learning for foveated reconstruction in AR-VR](http://ai.facebook.com/blog/deepfovea-using-deep-learning-for-foveated-reconstruction-in-ar-vr) · Meta AI（Wayback 存档）

2019 年 11 月 18 日

## 这项研究是什么

DeepFovea 是一个新的 AI 驱动的注视点渲染（foveated rendering）系统，面向增强现实和虚拟现实显示器。它用比以往系统少一个数量级的像素渲染图像，产出现实逼真、随视线变化的完整质量体验。这是第一个能够以极稀疏输入为条件生成自然外观视频序列的实用生成对抗网络（GAN）。在我们的测试中，DeepFovea 可将渲染所需的计算资源减少多达 10-14 倍，同时任何图像差异对人眼仍不可察觉。我们在此分享完整的图结构和材料。

## 它是如何工作的

当人眼直视一个物体时，能看清极多细节。而周边视觉的质量要低得多，但由于大脑会推断缺失的信息，人类并不会察觉。DeepFovea 利用生成对抗网络（GAN）的最新进展，通过生成感知上一致的内容，同样地「脑补」缺失的周边细节。该系统通过输入大量降低像素密度的视频序列进行训练。输入模拟周边图像的退化，而目标帮助网络学习如何根据它见过的所有视频的统计规律填补缺失细节。其结果是从一串稀疏像素流中生成出自然外观的视频——在 60x40 度视场的周边区域，像素密度最多降低了 99%。该系统还将周边区域的闪烁、混叠及其他视频伪影控制在人眼可检测的阈值之下。（示例视频可在此查看。）

## 为什么它重要

高质量的 AR 和 VR 体验需要高图像分辨率、高帧率和多视图，这会极其耗费资源。为了推进这些系统并将其带到更广泛的设备上——例如使用移动芯片组和小型便携电池的设备——我们需要大幅提升渲染效率。DeepFovea 展示了深度学习如何通过注视点重建帮助完成这一任务。这种方法与硬件无关，使其成为有望用于下一代头戴式显示技术的工具。随着社区探索在 AR 和 VR 中使用眼动追踪，构建 DeepFovea 这类随视线变化的技术将特别有用。该系统是我们为改进 AR/VR 图形而推出的若干研究项目之一。它延续了我们此前发布的 DeepFocus——后者用 AI 解决另一个挑战：对焦调节（accommodation）。

**阅读完整论文**

DeepFovea: Neural Reconstruction for Foveated Rendering and Video Compression using Learned Statistics of Natural Videos

**作者**

- Anton Kaplanyan，研究科学家
