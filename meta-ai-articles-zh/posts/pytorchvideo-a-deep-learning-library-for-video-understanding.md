---
title: "PyTorchVideo：一个面向视频理解的深度学习库"
title_en: "PyTorchVideo: A deep learning library for video understanding"
date: 2021-05-18
source: https://ai.facebook.com/blog/pytorchvideo-a-deep-learning-library-for-video-understanding
crawled: 2026-09-22
translated: 2026-09-22
---

# PyTorchVideo：一个面向视频理解的深度学习库

> 原文：[PyTorchVideo: A deep learning library for video understanding](https://ai.facebook.com/blog/pytorchvideo-a-deep-learning-library-for-video-understanding) · Meta AI（Wayback 存档）

2021 年 5 月 18 日

**它是什么：** PyTorchVideo 是一个面向视频理解研究与应用的深度学习库。它以 PyTorch 为基础，提供易用、高效且可复现的最先进视频模型、数据集、变换和工具的实现。

**它能做什么：** PyTorchVideo 库支持的组件可用于多种视频理解任务，例如视频分类、检测、自监督学习和光流。更重要的是，它不局限于视觉信号：PyTorchVideo 还支持其他模态，包括音频和文本。此外，PyTorchVideo 也不局限于桌面设备：Accelerator 软件包提供针对移动硬件的专项优化和模型部署流程，不断突破设备端性能的边界。

（原文此处嵌入视频：Something Went Wrong We're having trouble playing this video. Learn more）

在三星 Galaxy S10 手机上运行的 PyTorchVideo 加速版 X3D 模型。该模型运行速度约为实时的 8 倍，处理一秒视频仅需约 130 毫秒。

（原文此处嵌入视频：Something Went Wrong We're having trouble playing this video. Learn more）

执行视频动作检测的、基于 PyTorchVideo 的 SlowFast 模型。

让 PyTorchVideo 得以加速项目的特性包括：

- 一整套最先进的视频模型及其预训练权重，组件可定制，让研究员能够构建新的视频架构。
- 一组下游任务，包括动作分类、声学事件检测、动作检测和自监督学习（SSL）。
- 支持种类繁多的数据集和任务，可在不同评测协议下对各种视频模型进行基准测试。
- 针对硬件推理（移动设备、Intel NNPI 等）优化的高效构建模块和部署流程，支持硬件感知的模型设计和全速的设备端模型执行。
- 不断增长的视频处理常用脚本工具集，包括解码、追踪和光流提取。

展望未来，我们承诺持续增强 PyTorchVideo 库，以支持视频理解领域更多突破性研究。我们欢迎整个共同体的贡献。我们的一切努力都将指向支持那个致力于推动视频研究前沿的丰富开源共同体。

**为什么重要：** 理解视频是计算机视觉的重大挑战之一。计算资源的增长和网络上的视频数据量正在推动该领域取得更多进展。然而，视频数据分析的规模、丰富性和难度意味着业界对有效且高效的前沿模型、基础设施和工具有着强烈需求。PyTorchVideo 旨在满足这一需求，提供可复现、高效的视频理解组件的统一仓库，可直接集中用于研究和生产应用。

另一个重大挑战是缺乏一个标准化的、以视频为中心、一站式服务多种视频用例的库。这为初次接触视频的开发者设置了入门门槛。缺乏标准化也让协作和在他人的工作之上构建变得困难。在这方面，PyTorchVideo 是我们解决其中一些瓶颈的真诚努力。

在 Facebook，PyTorchVideo 支撑着来自 FAIR（Meta 基础人工智能研究院）的最先进研究工作，例如：

- SlowFast networks for video recognition（用于视频识别的 SlowFast 网络）
- Audiovisual SlowFast networks for video recognition（用于视频识别的视听 SlowFast 网络）
- X3D: Expanding architectures for efficient video recognition（X3D：扩展高效视频识别架构）
- Non-local neural networks（非局部神经网络）
- A closer look at spatiotemporal convolutions for action recognition（细看动作识别中的时空卷积）
- Video classification with channel-separated convolutional networks（用通道分离卷积网络做视频分类）

它也被用于推动视频 Transformer 和自监督学习的最新进展，例如：

- Multiscale vision transformers（多尺度视觉 Transformer）
- A large-scale study on unsupervised spatiotemporal representation learning（无监督时空表示学习的大规模研究）
- Multiview pseudo-labeling for semi-supervised learning from video（用于视频半监督学习的多视角伪标注）
- Unidentified video objects: A benchmark for dense, open-world segmentation（未识别视频对象：稠密开放世界分割基准）
- Is space-time attention all you need for video understanding?（时空注意力是视频理解所需的一切吗？）

访问 PyTorchVideo 网站

在 GitHub 上获取代码

**致谢：** PyTorchVideo 由以下贡献者支持和开发：Tullie Murrell、Haoqi Fan、Kalyan Vasudev Alwala、Yilei Li、Yanghao Li、Heng Wang、Bo Xiong、Nikhila Ravi、Matt Feiszli、Aaron Adcock、Wan-Yen Lo、Jitendra Malik、Ross Girshick 和 Christoph Feichtenhofer。

## 作者

PyTorchVideo 团队
