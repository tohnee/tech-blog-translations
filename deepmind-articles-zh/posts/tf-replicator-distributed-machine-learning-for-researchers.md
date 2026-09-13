---
title: "TF-Replicator：面向研究者的分布式机器学习"
title_en: "TF-Replicator: Distributed Machine Learning for Researchers"
source: https://deepmind.google/blog/tf-replicator-distributed-machine-learning-for-researchers/
site: deepmind
date: 2019-03-07
crawled: 2026-09-13
translated: 2026-09-13
---

# TF-Replicator：面向研究者的分布式机器学习

> 原文：[TF-Replicator: Distributed Machine Learning for Researchers](https://deepmind.google/blog/tf-replicator-distributed-machine-learning-for-researchers/) · Google DeepMind

在 DeepMind，研究平台团队（Research Platform Team）负责构建基础设施，以赋能并加速我们的 AI 研究。今天，我们很高兴分享我们如何开发了 TF-Replicator——一个软件库，它帮助研究者以最小的代价、无需任何分布式系统经验，就能把他们的 TensorFlow 模型部署到 GPU 与 [Cloud TPU](https://cloud.google.com/tpu/) 上。TF-Replicator 的编程模型现已作为 TensorFlow 的 [tf.distribute.Strategy](https://www.tensorflow.org/beta/guide/distribute_strategy) 的一部分开源。这篇博客文章概述了 TF-Replicator 背后的理念与技术挑战。如需更全面的描述，请阅读我们的 [arXiv 论文](https://arxiv.org/abs/1902.00465)。

近年来 AI 突破的一个反复出现的主题——从 [AlphaFold](https://deepmind.google/science/alphafold/) 到 [BigGAN](https://arxiv.org/abs/1809.11096) 再到 [AlphaStar](https://deepmind.com/blog/article/alphastar-mastering-real-time-strategy-game-starcraft-ii)——是对轻松且可靠的可扩展性的需求。不断增长的计算能力让研究者能够训练越来越大的神经网络，获得新的能力。为此，研究平台团队开发了 TF-Replicator，它允许研究者面向不同的机器学习硬件加速器、把工作负载扩展到许多设备，并在不同类型的加速器之间无缝切换。虽然它最初是作为 TensorFlow 之上的一个库开发的，但 TF-Replicator 的 API 此后已被集成进 TensorFlow 2.0 全新的 [tf.distribute.Strategy](https://www.tensorflow.org/alpha/guide/distribute_strategy)。

虽然 TensorFlow 直接支持 CPU、GPU 和 TPU（[张量处理单元](https://cloud.google.com/tpu/)）设备，但在不同目标之间切换需要用户付出相当大的努力。这通常涉及针对特定硬件目标对代码进行专门化，从而把研究思路限制在那个平台的能力范围之内。一些构建在 TensorFlow 之上的现有框架，例如 [Estimators](https://www.tensorflow.org/guide/estimators)，试图解决这个问题。然而，它们通常面向生产用例，缺乏快速迭代研究思路所需的表达力与灵活性。

## 构建分布式机器学习库

我们开发 TF-Replicator 的最初动机，是为 DeepMind 研究者提供一个使用 [TPU](https://cloud.google.com/tpu/) 的简单 API。TPU 为机器学习工作负载提供了可扩展性，促成了诸如用我们的 [BigGAN](https://arxiv.org/abs/1809.11096) 模型实现最先进图像合成等研究突破。[TensorFlow 原生的 TPU API](https://www.tensorflow.org/api_docs/python/tf/contrib/tpu) 与 GPU 的目标定位方式不同，形成了 TPU 推广的障碍。TF-Replicator 提供了一个更简单、更友好的 API，隐藏了 TensorFlow TPU API 的复杂性。至关重要的是，研究平台团队与来自各个机器学习学科的研究者密切合作开发了 TF-Replicator API，以确保必要的灵活性与易用性。

## TF-Replicator API

用 TF-Replicator 编写的代码与为单个设备编写的 TensorFlow 代码很相似，允许用户自由定义自己的模型运行循环。用户只需定义：(1) 一个暴露 Dataset 的输入函数，以及 (2) 一个定义模型逻辑的步骤函数（例如单步梯度下降）：

把计算扩展到多个设备需要设备之间相互通信。在训练机器学习模型的语境下，最常见的通信形式是累积梯度，供 [随机梯度下降](https://en.wikipedia.org/wiki/Stochastic_gradient_descent)等优化算法使用。因此，我们提供了一个便捷的方法来包装 [TensorFlow 优化器](https://www.tensorflow.org/api_docs/python/tf/train/Optimizer)，使梯度在跨设备累积之后再更新模型参数。对于更一般的通信模式，我们提供类 [MPI](https://en.wikipedia.org/wiki/Message_Passing_Interface) 的原语，例如 `all\_reduce` 与 `broadcast`。这些原语让实现诸如全局批归一化（global batch normalisation）之类的操作变得轻而易举——这项技术对我们 [BigGAN](https://arxiv.org/abs/1809.11096) 模型的训练扩展至关重要（见论文第 3 节）。

![一幅示意图，展示运行时的复制式计算：单个输入流水线把数据分发到四个 GPU（标注为 GPU 0 至 GPU 3）。每个 GPU 执行一个相同的纵向结构计算图，横向的双向通信箭头把四个设备上计算图的第三阶段连接起来。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227216159c05b2d938808bd_TFR2002.gif)

输入数据从主机发送到每个 GPU，各 GPU 立即开始处理。当 GPU 之间需要交换信息时，它们会先同步再发送数据。

## 实现

对于多 GPU 计算，TF-Replicator 依赖一种「图内复制」（in-graph replication）模式：每个设备的计算在同一个 TensorFlow 计算图中被复制。设备之间的通信通过连接设备各自对应子图中的节点来实现。在 TF-Replicator 中实现这一点颇具挑战，因为通信可能发生在数据流图的任意位置。因此，计算被构建的顺序至关重要。

我们的第一个想法是在单独的 Python 线程中并发地构建每个设备的子图。当遇到通信原语时，各线程同步，主线程插入所需的跨设备计算；之后，每个线程继续构建自己设备的计算。然而，在我们考虑这一方案时，TensorFlow 的计算图构建 API 还不是线程安全的，这使得在不同线程中并发构建子图非常困难。于是，我们改用[计算图重写](https://www.tensorflow.org/api_docs/python/tf/contrib/graph_editor)，在所有设备的子图都构建完成之后再插入通信。构建子图时，在需要通信的位置插入占位符（placeholder）；随后我们收集跨设备的所有匹配占位符，并用相应的跨设备计算替换它们。

![](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6227217b7468185b29a75418_TFR2003.gif)

当 TF-Replicator 构建图内复制的计算时，它先独立地为每个设备构建计算，并在用户指定了跨设备计算的位置留出占位符。待所有设备的子图构建完毕后，TF-Replicator 用实际的跨设备计算替换占位符，从而把它们连接起来。

## 在 DeepMind 构建 AI 研究平台

通过在 TF-Replicator 的设计与实现全程与研究者密切合作，我们得以构建出一个库：它让用户能够轻松地把计算扩展到众多硬件加速器上，同时保留了进行前沿 AI 研究所需的掌控力与灵活性。例如，在与研究者讨论之后，我们添加了 all-reduce 等 MPI 风格的通信原语。TF-Replicator 与其他共享基础设施让我们得以在稳固的基础上构建日益复杂的实验，并快速在整个 DeepMind 推广最佳实践。

截至撰写本文时，TF-Replicator 是 DeepMind 内使用最广泛的 TPU 编程接口。虽然这个库本身并不局限于训练神经网络，但它最常被用于在大批量数据上进行训练。例如，[BigGAN](https://arxiv.org/abs/1809.11096) 模型是在 TPUv3 pod 上以 2048 的批次大小、跨最多 512 个核心训练的。在采用分布式 actor-learner 架构的强化学习智能体中，例如[我们的重要性加权 actor-learner 架构](https://deepmind.com/blog/article/impala-scalable-distributed-deeprl-dmlab-30)，可扩展性是靠大量 actor 与环境交互、生成新经验来实现的。这些数据随后由 learner 处理，以改进以神经网络表示的智能体策略。为应对越来越多的 actor，可以使用 TF-Replicator 轻松地把 learner 分布到许多硬件加速器上。这些及其他例子在[我们的 arXiv 论文](https://arxiv.org/abs/1902.00465)中有更详细的描述。

**注释**

TF-Replicator 只是 DeepMind 研究平台团队打造的众多有影响力的技术之一。DeepMind 在 AI 领域的许多突破，从 AlphaGo 到 AlphaStar，都有赖于这个团队。如果你认同我们的使命，并热衷于加速最前沿的 AI 研究，请留意 Research Platform 在 <https://deepmind.com/careers> 开放的软件工程师职位（这些职位不要求机器学习经验）。

这项工作由 DeepMind 研究平台团队完成。我们感谢 Frederic Besse、Fabio Viola、John Aslanides、Andy Brock、Aidan Clark、Sergio Gómez Colmenarejo、Karen Simonyan、Sander Dieleman、Lasse Espeholt、Akihiro Matsukawa、Tim Harley、Jean-Baptiste Lespiau、Koray Kavukcuoglu、Dan Belov 以及 DeepMind 的许多其他同事在 TF-Replicator 开发全程中提出的宝贵反馈。我们还要感谢 Google 的 Priya Gupta、Jonathan Hseu、Josh Levenberg、Martin Wicke 及其他同事，让这些理念作为 tf.distribute.Strategy 的一部分惠及所有 TensorFlow 用户。
