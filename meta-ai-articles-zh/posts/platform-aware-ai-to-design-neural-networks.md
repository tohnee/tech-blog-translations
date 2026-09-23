---
title: "用平台感知 AI 设计紧凑高效的神经网络"
title_en: "Using platform-aware AI to design compact and efficient neural networks"
date: 2019-03-15
source: https://ai.facebook.com/blog/platform-aware-ai-to-design-neural-networks
crawled: 2026-09-22
translated: 2026-09-22
---

# 用平台感知 AI 设计紧凑高效的神经网络

> 原文：[Using platform-aware AI to design compact and efficient neural networks](https://ai.facebook.com/blog/platform-aware-ai-to-design-neural-networks) · Meta AI（Wayback 存档）

**研究内容：**一种自适应的神经网络设计方法，使用新颖的优化算法来提升网络架构的计算效率。此前构建紧凑到能在资源受限平台上运行的神经网络的努力，要么依赖计算量巨大的强化学习（RL）算法，要么依赖耗时的手工定制架构。这一由 Facebook、普林斯顿大学和加州大学伯克利分校的研究人员开发的方法提供了一种自动化替代：AI 模型基于搜索提出架构，搜索过程会把网络将要运行的平台的特定硬件、时延目标和能耗约束纳入考量。

**工作原理：**这一方法名为 Chameleon（变色龙），采用准确率、时延和能耗预测器来确定平台现有构件的最优使用方式。这些预测器比基于 RL 的算法更高效，其中结合了经贝叶斯优化增强的高斯过程回归器以及不平衡拟蒙特卡洛采样。在涉及多种硬件平台和资源约束的测试中，Chameleon 持续胜过最先进的手工设计和自动化模型。这些结果包括：在 Nvidia GTX 1060 GPU 上比 ResNet-152 准确率高出 5.8%，在移动 CPU 上比 MobileNetV2 高出 8.3%。与基于 RL 的架构搜索和手工定制架构改动相比，这些全方位的提升还伴随着计算开销和开发时间的大幅降低。

**为什么重要：**Chameleon 的结果表明，预测模型可以在不增加时延或能耗的情况下提升基于 AI 的神经网络设计效率。而且这一方法很快，每次自适应搜索只需几分钟，进一步降低了把神经网络优化到更精简平台上通常所需的成本和时间。由于 Chameleon 能适应呈现给它的约束和硬件，这一方法可以扩大神经网络的使用面，惠及目前没有资源利用这项技术的研究机构。

**阅读完整论文：**ChamNet: Towards efficient network design through platform-aware model adaptation

这项工作在 CVPR 2019 上做了展示。
