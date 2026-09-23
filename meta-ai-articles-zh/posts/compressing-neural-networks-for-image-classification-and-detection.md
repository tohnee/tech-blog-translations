---
title: "压缩用于图像分类与检测的神经网络"
title_en: "Compressing neural networks for image classification and detection"
date: 2019-07-25
source: https://ai.facebook.com/blog/compressing-neural-networks-for-image-classification-and-detection
crawled: 2026-09-22
translated: 2026-09-22
---

# 压缩用于图像分类与检测的神经网络

> 原文：[Compressing neural networks for image classification and detection](https://ai.facebook.com/blog/compressing-neural-networks-for-image-classification-and-detection) · Meta AI（Wayback 存档）

**这项研究是什么：**一种新方法，通过对神经网络的权重做量化（离散化）来缩减其内存占用，同时凭借字节对齐的方案保持较短的推理时间。这旨在帮助计算机视觉研究者——他们正不断用执行从图像分类到实例检测等任务的模型推进最先进水平。用传统方法，存储这些高性能神经网络并用其推理所需的内存通常超过 100 MB，使其无法用于嵌入式设备。我们正在开源压缩后的模型以及复现结果所需的代码。

**工作原理：**我们依赖一种流行的结构化量化方法——乘积量化（product quantization），并对其加以改造，专注于激活值的重建而非权重本身。换言之，此前的方法旨在让网络对任意输入都得到近似，而我们只关注对域内输入的重建质量。我们用未压缩的网络充当教师来指导学生网络的压缩，这利用了蒸馏技术。我们的方法是无监督的——不需要任何带标注的数据。

我们把该方法应用于由 Facebook AI 用半监督学习训练的高性能 ResNet-50。压缩后的模型只有 5 MB（20 倍压缩率），并在 ImageNet 上保持了原版 ResNet-50 的 top-1 准确率（76.1%）。我们还压缩了广泛使用的 Mask R-CNN（现已收录于 torchvision）用于实例检测，在模型体积约 6 MB（26 倍压缩率）的情况下达到了 33.9/30.8 的 Box AP/Mask AP。

**为什么重要：**对嵌入最优秀神经网络的需求日益增长，而每种应用都需要在体积与准确率之间做出特定权衡。例如，机器人和自动驾驶汽车需要可靠的技术，实时精确识别视频帧中出现的所有实例，这意味着相当大的模型亟需压缩。Oculus Quest 等虚拟现实与增强现实设备同样会从神经网络压缩的进展中受益。

阅读完整论文：And the bit goes down: Revisiting the quantization of neural networks

**作者**

- Pierre Stock，Facebook AI 研究助理
