---
title: "DeepMind 在 ICML 2017 的论文（第三部分）"
title_en: "DeepMind papers at ICML 2017 (part three)"
source: https://deepmind.google/blog/deepmind-papers-at-icml-2017-part-three/
site: deepmind
date: 2017-08-04
crawled: 2026-09-13
translated: 2026-09-13
---

# DeepMind 在 ICML 2017 的论文（第三部分）

> 原文：[DeepMind papers at ICML 2017 (part three)](https://deepmind.google/blog/deepmind-papers-at-icml-2017-part-three/) · Google DeepMind

本系列共三篇，这是最后一篇，概述我们将在澳大利亚悉尼 ICML 2017 大会上展示的论文。

## Cognitive Psychology for Deep Neural Networks: A Shape Bias Case Study（面向深度神经网络的认知心理学：一个形状偏置案例研究）

**作者：** Samuel Ritter\*, David Barrett\*, Adam Santoro, Matt Botvinick

深度神经网络（DNN）在广泛的任务上取得了前所未有的性能，其速度之快，已远远超出了我们对这些解的本质的理解。在这项工作中，我们提议借助认知心理学所发展出的问题描述、理论与实验方法，来解决现代 DNN 的这一可解释性问题。在一个案例研究中，我们应用人类词语学习心理学中的一种理论和方法，以更好地理解现代单样本（one-shot）学习系统是如何工作的。结果不仅揭示出我们的 DNN 展现出与人类相同的归纳偏置，还揭示了 DNN 的若干出人意料的特性。

更多细节与相关工作，请参阅[论文](https://arxiv.org/pdf/1706.08606.pdf)。

**ICML 会场信息：**

Tuesday 08 August, 15:48-16:06 @ Darling Harbour Theatre（口头报告）

Tuesday 08 August, 18:30-20:00 @ Gallery #113（海报）

## Count-Based Exploration with Neural Density Models（基于神经密度模型的计数式探索）

**作者：** Georg Ostrovski, Marc Bellemare, Aaron van den Oord, Remi Munos

此前，基于简单图形密度模型预测增益的计数式探索，已经在一些最难的 Atari 探索类游戏中取得了最先进的结果。我们研究了两个悬而未决的问题：1）更好的密度模型是否带来更好的探索；2）本工作中使用的混合蒙特卡洛更新规则在探索中扮演何种角色。我们证明，神经密度模型 PixelCNN 可以在强化学习智能体的经验流上在线训练，并用于计数式探索，从而在更大范围的困难探索类游戏中取得更好的结果，同时在容易探索的游戏上保持更高的性能。我们还证明，在最稀疏的奖励设置下，蒙特卡洛回报对于利用内在奖励信号至关重要，且无法轻易被更平滑的 lambda 回报更新规则取代。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1703.01310)。

**ICML 会场信息：**

Wednesday 09 August, 13:30-13:48 @ C4.5（口头报告）

Wednesday 09 August, 18:30-22:00 @ Gallery #64（海报）

## The Predictron: End-to-End Learning and Planning（The Predictron：端到端学习与规划）

**作者：** David Silver, Hado van Hasselt, Matteo Hessel, Tom Schaul, Arthur Guez, Tim Harley, Gabriel Dulac-Arnold, David Reichert, Neil Rabinowitz, Andre Barreto, Thomas Degris

人工智能的关键挑战之一，是学习在规划情境中有效的模型。在本文中，我们介绍 predictron 架构。predictron 由一个完全抽象的模型构成，该模型以马尔可夫奖励过程表示，可以向前展开多个「想象出来的」规划步骤。predictron 的每次前向传播都会在多个规划深度上累积内部奖励与价值。predictron 以端到端方式训练，使这些累积的价值能够准确逼近真实的价值函数。我们将 predictron 应用于程序化生成的随机迷宫和一个台球游戏模拟器。predictron 给出的预测显著比传统深度神经网络架构更准确。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1612.08810)。

**ICML 会场信息：**

Wednesday 09 August, 14:24-14:42 @ C4.5（口头报告）

Wednesday 09 August 18:30-20:00 @ Gallery #91（海报）

## FeUdal Networks for Hierarchical Reinforcement Learning（用于分层强化学习的 FeUdal Networks）

**作者：** Sasha Vezhnevets, Simon Osindero, Tom Schaul, Nicolas Hees, Max Jaderberg, David Silver, Koray Kavukcuoglu

如何创建能够学会把自身行为分解为有意义的基本单元（primitives）、然后复用它们以更高效地获取新行为的智能体，是一个由来已久的研究问题。这一问题的答案，可能是通往具备通用智能与胜任力的智能体的一块重要垫脚石。本文提出了 FeUdal Networks（FuN）——一种新颖的架构，它将子目标表述为潜在状态空间中的方向；一旦沿着这些方向前进，就会转化为有意义的行为基本单元。FuN 清晰地把发现并设定子目标的模块与通过基本动作生成行为的模块分离开来。这创造出一个稳定、自然的层级结构，并允许两个模块以互补的方式学习。我们的实验清楚地表明，这使得长期信用分配和记忆变得更加可控。这也为后续研究开辟了许多途径，例如：可以通过在多个时间尺度上设定目标来构建更深的层级结构，也可以把智能体扩展到具有稀疏奖励和部分可观测性的真正大型环境中。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1703.01161)。

**ICML 会场信息：**

Wednesday 09 August, 15:30-15:48 @ C4.5（口头报告）

Wednesday 09 August, 18:30-20:00 @ Gallery #107（海报）

## Neural Episodic Control（神经情景控制）

**作者：** Alex Pritzel, Benigno Uria, Sriram Srinivasan, Adria Puigdomenech, Oriol Vinyals, Demis Hassabis, Daan Wierstra, Charles Blundell

深度强化学习算法已在多种任务上取得最先进的性能，但它们的数据利用效率往往非常低下。在这项工作中，我们提出一种新算法，能够快速吸纳智能体收集到的新信息。为此，我们引入一种新的可微数据结构——可微神经字典（differentiable neural dictionary），它可以立即纳入新信息，同时能够根据算法所要解决的任务更新其内部表示。我们的智能体 Neural Episodic Control 建立在这一可微数据结构之上，能够在广泛的环境中显著更快地学习。

更多细节与相关工作，请参阅[论文](https://arxiv.org/pdf/1703.01988.pdf)。

**ICML 会场信息：**

Wednesday 09 August, 16:06-16:24 @ C4.5

Wednesday 09 August, 18:30-22:00 @ Gallery #125

## Neural Message Passing Learns Quantum Chemistry（神经消息传递学习量子化学）

**作者：** Justin Gilmer (Google Brain), Sam Schoenholz (Google Brain), Patrick Riley (Google Google), Oriol Vinyals, George Dahl (Google Brain)

在这项工作中，我们展示了如何通过扩展神经网络使其能在图上运行，把昂贵的量子化学性质模拟当作一个可供学习的监督数据集来处理，从而将运行时性能提升数个数量级。我们的模型极为精确且速度极快。在论文中，我们还提供了一个统一框架，总结了此前关于图形状输入与神经网络的工作。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1704.01212)。

**ICML 会场信息：**

Wednesday 09 August, 16:24-16:42 @ Darling Harbour Theatre（口头报告）

Wednesday 09 August, 18:30-22:00 @ Gallery #131（海报）
