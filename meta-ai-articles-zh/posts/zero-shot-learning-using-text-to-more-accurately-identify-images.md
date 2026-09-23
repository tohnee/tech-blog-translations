---
title: "零样本学习：用文本更准确地识别图像"
title_en: "Zero-shot learning: Using text to more accurately identify images"
date: 2018-11-05
source: https://ai.facebook.com/blog/zero-shot-learning-using-text-to-more-accurately-identify-images
crawled: 2026-09-22
translated: 2026-09-22
---

# 零样本学习：用文本更准确地识别图像

> 原文：[Zero-shot learning: Using text to more accurately identify images](https://ai.facebook.com/blog/zero-shot-learning-using-text-to-more-accurately-identify-images) · Meta AI（Wayback 存档）

2018 年 11 月 5 日

**研究内容：** 零样本学习（zero-shot learning，ZSL）是机器学会识别其从未见过的物体的过程。Facebook 的研究人员开发了一个更准确的新 ZSL 模型，它使用称为生成对抗网络（GAN）的神经网络架构阅读并分析文本文章，然后视觉地识别文章所描述的物体。这种新颖的 ZSL 方法让机器能够基于类别对物体分类，再利用该信息识别其他相似物体，而不是像其他模型那样逐一学习每个物体。

**工作原理：** 研究人员训练了这个称为生成对抗零样本学习（generative adversarial zero-shot learning，GAZSL）的模型，在包含 6 万多张图像的两个数据库中识别 600 多个鸟类类别。随后给它网络文章，要求它利用其中的信息识别从未见过的鸟。模型从文本中提取了七个关键视觉特征，创建这些特征的合成可视化，并用这些特征识别正确的鸟类类别。研究人员随后将 GAZSL 模型与其他七种 ZSL 算法对比测试，发现它在四个不同基准上都始终更准确。总体上，GAZSL 模型比其他模型高出 4% 到 7%，某些情况下差距更大。

**为什么重要：** 要变得更有用，计算机视觉系统需要识别未专门训练过的物体。例如，据估计现存的鸟类超过 1 万种，而大多数鸟类计算机视觉数据集只有几百个类别。这个已开源的新 ZSL 模型已被证明能产生更好的结果，为未来的机器学习研究提供了一条有前景的道路。AI 研究的许多工作仍是基础性的，但改进系统理解文本并正确识别物体的能力的工作，将持续为更好、更可靠的 AI 系统奠定基础。

阅读完整论文：《A Generative Adversarial Approach for Zero-Shot Learning from Noisy Texts》
