---
title: "面向人脸图像的半对抗网络"
title_en: "Semi-Adversarial Nets for Face Images"
source: https://sebastianraschka.com/blog/2018/semi-adversarial-nets-1.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 面向人脸图像的半对抗网络

> 原文：[Semi-Adversarial Nets for Face Images](https://sebastianraschka.com/blog/2018/semi-adversarial-nets-1.html)

我觉得手头备有一些简明扼要的近期项目总结会很不错，可以分享给更广泛的受众，包括同事和学生。于是，我给自己定了个挑战：用不到 1000 字的篇幅写完，不被琐碎的细节和技术行话干扰。

在这篇文章中，我主要介绍我近期与 [iPRoBe 实验室](http://iprobe.cse.msu.edu)合作的一些研究，它们属于"在人脸图像中隐藏特定信息的方法"这一宽泛的研究方向。本文讨论的研究主题是"在保留实用性的同时最大化隐私"（这一目标与[差分隐私](https://en.wikipedia.org/wiki/Differential_Privacy)研究的目标有些相似）。

如果你对这里描述的研究感兴趣，可以在以下两篇论文中找到更详细的信息：

- "[Semi-Adversarial Networks: Convolutional Autoencoders for Imparting Privacy to Face Images](https://ieeexplore.ieee.org/document/8411207/)"（ICB 2018，预印本：<https://arxiv.org/abs/1712.00321>）
- "Gender Privacy: An Ensemble of Semi Adversarial Networks for Confounding Arbitrary Gender Classifiers"（BTAS 2018；预印本：<https://arxiv.org/abs/1807.11936>）

## 在保留实用性的同时提升隐私

我们可以把所研究的问题更一般地看作一个约束优化问题：我们想在人脸图像中隐藏特定信息，同时保留其生物特征识别方面的实用性。更具体地说，我们制定了以下三个目标：

1. 扰动性别信息
2. 确保人脸图像看起来真实
3. 保留生物特征人脸识别\*的实用性

*\*生物特征人脸识别*可分为两个相关的子任务：识别（A）与验证（B）：

![Semi adversarial nets 1 biometric id](https://sebastianraschka.com/images/blog/2018/semi-adversarial-nets-1/biometric-id.webp)

这里，对性别信息的"扰动"意味着给定的性别分类器不再能够对一个人的性别做出可靠预测。阻止自动提取个人属性可以有很多理由，以下是三个典型例子：

1. 基于性别的画像（profiling）
2. 身份盗用（通过组合多个公开来源的数据）
3. 未经用户同意提取数据，违反伦理

上述问题可能出现在人脸图像被采集、上传并存储到中央数据库的任何时候。作为一种对策，系统（例如超市或监控摄像头）可以在出售给第三方之前配备性别扰动技术，让终端用户更难侵犯用户隐私，并防止为未经批准的目的收集数据。例如，在人脸图像数据库中隐藏信息也有助于确保符合 [GDPR 准则](https://www.eugdpr.org)。

## 半对抗网络的普遍实用性

当然，只需在图像中加入噪声，或者把图像打乱到一定程度，就能轻松隐藏性别信息。但我们必须记住，对图像的大幅改动也很可能让图像的任何实用性（在这里指生物特征识别）失去意义。

上一段讲的是我们开发 SAN（半对抗网络）的主要动机，而 SAN 背后的一般思想可以看作一种在约束条件下优化任意损失函数的通用方法：那些我们希望**最大化一个分类器的性能、同时最小化另一个分类器性能**的问题。因此，即使你研究的问题不是人脸识别，SAN 仍可能对解决约束优化任务派上用场。

下一节介绍我们 ICB 2018 论文"[Semi-Adversarial Networks: Convolutional Autoencoders for Imparting Privacy to Face Images](https://ieeexplore.ieee.org/document/8411207/)"（预印本版本：<https://arxiv.org/abs/1712.00321>）中的整体 SAN 架构。

## 半对抗网络架构

虽然 SAN 架构在论文的插图中看起来有点绕，但如果把它拆成三个主要组成部分，其实相当直观：

1. 一个自编码器，用于扰动输入图像，同时确保扰动后的图像看起来接近原图
2. 一个人脸匹配器，它应当能够做出准确预测
3. 一个性别分类器，它应当*无法*做出准确预测

![Semi adversarial nets 1 san architecture](https://sebastianraschka.com/images/blog/2018/semi-adversarial-nets-1/san-architecture.webp)

SAN 的训练过程可以用下面的 PyTorch（伪）代码概括：

```python
ae = AutoEncoder()  
gc = GenderClassifier()  
fm = FaceMatcher()  

gc.load_state_dict(torch.load('saved_fm_model.pkl'))  
fm.load_state_dict(torch.load('saved_gc_model.pkl'))  

for fixed_model in (gc, fm):  
    for param in fixed_model.parameters():  
        param.requires_grad = False  

optimizer = torch.optim.Adam(ae.parameters(), lr=learning_rate)  

for epoch in range(num_total_epochs):  
    # ...  
    cost = loss_reconstruction + loss_gender_classification + loss_face_matching  
    cost.backward()  
    optimizer.step()
```

（完整源代码见 <https://github.com/iPRoBe-lab/semi-adversarial-networks>。）

请注意，除了使用一系列未见过的人脸图像数据集来评估 SAN 模型之外，我们还会丢弃训练时使用的性别分类器和人脸匹配器，改用一系列未见的人脸匹配器和性别分类器来评估我们的方法。

好奇的读者可以看看下面这张图，它解释了为什么我们把这种设置称为**半对抗**（semi-adversarial）：

![Semi adversarial nets 1 semi adversarial](https://sebastianraschka.com/images/blog/2018/semi-adversarial-nets-1/semi-adversarial.webp)

## 多样性与泛化

正如"Gender Privacy: An Ensemble of Semi Adversarial Networks for Confounding Arbitrary Gender Classifiers"一文所述，我们最近着重通过扩充数据集等手段来提升原始 SAN 模型的泛化性能。例如，为了避免 Buolamwini 等人在"[Gender shades: Intersectional accuracy disparities in commercial gender classification](http://proceedings.mlr.press/v81/buolamwini18a.html)"中讨论的常见偏差，我们对深肤色个体的随机样本做了过采样——这类样本在大多数人脸图像数据集中代表性不足——以缓解潜在偏差。此外，我们还将评估套件扩展到了更广泛的未见过的性别分类器和人脸匹配器。

## 接下来的计划

本文总结的两篇研究论文介绍了在约束条件下优化目标函数的底层架构和"半对抗"训练方案。当然，目前仍有许多方面在探索之中，比如论文中提到的不同集成方案，以及向更多属性扩展。

这篇文章大致概括了我们在 SAN 与差分隐私方面的一部分研究。后续还会有更多内容。我们也非常期待在 [BTAS 2018](https://www.isi.edu/events/btas2018/home) 会议上展示近期的成果，并于今秋晚些时候在 [ODSC West 2018](https://odsc.com/california) 上就此做报告。
