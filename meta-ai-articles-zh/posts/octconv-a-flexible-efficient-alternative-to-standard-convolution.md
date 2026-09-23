---
title: "OctConv：一种灵活高效的标准卷积替代方案"
title_en: "OctConv: A flexible, efficient alternative to standard convolution"
date: 2019-03-15
source: https://ai.facebook.com/blog/octconv-a-flexible-efficient-alternative-to-standard-convolution
crawled: 2026-09-22
translated: 2026-09-22
---

# OctConv：一种灵活高效的标准卷积替代方案

> 原文：[OctConv: A flexible, efficient alternative to standard convolution](https://ai.facebook.com/blog/octconv-a-flexible-efficient-alternative-to-standard-convolution) · Meta AI（Wayback 存档）

**它是什么：**八度卷积（Octave convolution，OctConv）是一种易于实现、高效的标准 2D 或 3D 卷积替代方案。OctConv 可以直接替换神经网络中的标准卷积，而无需对网络架构做任何其他调整。它能提升图像与视频识别任务的准确率，同时在训练和推理阶段都降低内存与计算开销。

**它做了什么：**利用低频信息所需内存与计算量更少这一事实，OctConv 以彼此相差一个八度的不同频率存储并处理特征图。尽管此前已有研究探索多频率卷积架构，但 OctConv 在不同频率之间的通信更加高效且不损失性能。具体而言，OctConv 使用一条单独的通路处理低频特征图，并以极简的操作与原有的高频通路交换信息。在我们的评测中，配备 OctConv 的 ResNet-50 将 GFLOPs 降低了 40%，实际运行速度提升 1.5 倍，同时保持同等准确率。配备 OctConv 的 ResNet-152 模型在 ImageNet 上可取得 82.9% 的 top-1 准确率，而仅消耗 22.2 GFLOPs。在视频分类方面，我们在 Kinetics-400/600 上进行基准测试时也得到了类似的准确率与效率结果。

**为什么重要：**OctConv 提供了一种简单而有效的方式来降低计算与内存开销，使在相同计算预算下使用更大、更强的模型成为可能。这不仅能提升这些系统的性能，也有望改善其他任务的表现，例如物体检测以及图像与视频分割。此外，更高效的图像与视频识别对于移动端及其他处理能力有限的芯片组上的设备端计算尤为重要。我们在 Facebook 内部对 OctConv 进行了图像与视频分类评测，在分类准确率与模型时延上取得的增益与公开基准测试的结果一致。针对 GPU 的硬件库优化可能进一步降低计算和有效内存消耗，并带来额外的性能提升。

**GitHub 获取地址：**https://github.com/facebookresearch/OctConv

关于 OctConv 的更多细节可参见论文。参加 ICCV 2019 的读者还可以在海报环节了解更多（海报 #52），时间为当地时间 10 月 30 日（周三）上午 10:30。

**作者**

- Marcus Rohrbach，研究科学家
- Zhicheng Yan，研究科学家
- Haoqi Fan，软件工程师
- Bing Xu，应用研究科学家
