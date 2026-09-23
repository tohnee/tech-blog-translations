---
title: "一个面向大规模训练最先进视觉分类模型的新框架"
title_en: "A new framework for large-scale training of state-of-the-art visual classification models"
date: 2019-12-06
source: https://ai.meta.com/blog/a-new-framework-for-large-scale-training-of-state-of-the-art-visual-classification-models/
crawled: 2026-09-22
translated: 2026-09-22
---

# 一个面向大规模训练最先进视觉分类模型的新框架

> 原文：[A new framework for large-scale training of state-of-the-art visual classification models](https://ai.meta.com/blog/a-new-framework-for-large-scale-training-of-state-of-the-art-visual-classification-models/) · Meta AI（Wayback 存档）

**它是什么：**一个全新的、基于 PyTorch 的端到端框架，用于大规模训练最先进的图像和视频分类模型。它有几项显著优势：

- **易用性。**该库采用模块化、灵活的设计，任何人都可以借助非常简单的抽象在 PyTorch 之上训练机器学习模型。该系统还与 Amazon Web Services（AWS）开箱即用地集成，便于大规模研究，并在研究与生产之间轻松切换。
- **高性能。**例如，研究者可以用该框架在短短 15 分钟内在 ImageNet 上训练 ResNet50。

该框架现已在 GitHub 上提供。我们还将于 12 月 8 日（周日）在温哥华举行的神经信息处理系统会议（NeurIPS）上主办「Multi-modal research to production」研讨会。

**它做什么：**以往的计算机视觉（CV）库专注于为用户提供组件，让他们为自己的研究构建自己的框架。这种方式给研究者带来了灵活性，但在生产环境中会导致重复劳动，而且要求用户在不同框架之间迁移研究，并重新学习高效分布式训练和数据加载的细节。我们基于 PyTorch 的 CV 框架提供了更好的解决方案。我们的抽象让一个项目可以轻松从小规模研究原型扩展到拥有数百块 GPU 和数十亿张图像的大规模一流生产任务。通过与 Torch.Hub 的易用集成，AI 研究者和工程师只需几行代码即可下载并微调公开可用的最佳 ImageNet 模型。我们还加入了对 PyTorch Elastic（实验版本）的集成，使分布式训练对任何瞬时故障都具有鲁棒性；它还可以（可选地）让分布式训练任务在运行时适应集群中的可用资源。在 Facebook，我们一直在研究中使用这一框架，以便用最先进的配方在最大的数据集上用最大的模型轻松训练。

**为什么重要：**在图像和视频分类任务上取得最先进的结果，越来越依赖大规模训练、大量 GPU 集群和不断增大的训练数据集。通过开源该框架并内置与 AWS 的开箱即用集成，我们希望让更广泛的社区更容易进行可扩展的研究，用于 AI 应用和生产系统。而且，由于用户可以整体或部分地使用这一框架，它能与 PyTorch 生态中丰富的工具和库良好互操作。我们目前正在探索添加特性并进一步扩大训练可用数据量的方法。该框架将有助于加快研究节奏：它让在大规模图像和视频分类中复现和迭代最先进工作变得容易，也让任何人都能使用 AWS 大规模开发自己的模型。它还支持可复现的研究，提供易用的配置文件和标准的项目结构等特性。

在 GitHub 上获取：https://github.com/facebookresearch/

**作者**

- Aaron Adcock，研究科学家
- Vinicius Reis，研究科学家
- Mannat Singh，软件工程师
- Zhicheng Yan，研究科学家
- Laurens van der Maaten，研究科学家
- Kai Zhang，软件工程师
- Simran Motwani，软件工程师
- Jon Guerin，软件工程师
- Naman Goyal，软件工程师
- Laura Gustafson，软件工程师
