---
title: "DeepMind 论文精选 @ NIPS（第一部分）"
title_en: "DeepMind Papers @ NIPS (Part 1)"
source: https://deepmind.google/blog/deepmind-papers-nips-part-1/
site: deepmind
date: 2016-12-02
crawled: 2026-09-13
translated: 2026-09-13
---

# DeepMind 论文精选 @ NIPS（第一部分）

> 原文：[DeepMind Papers @ NIPS (Part 1)](https://deepmind.google/blog/deepmind-papers-nips-part-1/) · Google DeepMind

## Interaction Networks for Learning about Objects, Relations and Physics

**作者：** Peter Battaglia, Razvan Pascanu, Matthew Lai, Danilo Rezende, Koray Kavukcuoglu

对物体、关系与物理的推理是人类智能的核心，也是人工智能的一个关键目标。然而，许多现代机器学习方法仍然面临表达能力强的结构与高效性能之间的权衡。

我们提出了「交互网络」（interaction networks），它能够推理复杂系统中各物体如何相互作用，既支持动力学预测，也支持对系统抽象属性的推断。交互网络兼具表达力与高效性，因为它结合了三种强大的方法：结构化模型、模拟与深度学习。它以图结构数据为输入，以类似于模拟的方式执行以物体和关系为中心的推理，并使用深度神经网络实现。它对实体与关系的排列置换保持不变，因此能够自动泛化到与训练时所经历的不同大小、不同结构的系统。

在实验中，我们用交互网络实现了第一个通用的可学习物理引擎。仅在单步预测上训练之后，我们的模型就能在数千个时间步内准确模拟 n 体系统、弹跳球和非刚性绳子系统的物理轨迹。同一架构还能推断潜在的物理属性，例如势能。

在物理推理之外，交互网络还可以为场景理解、社会感知、分层规划与类比推理等 AI 研究方向提供强大的框架。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1612.00222)。

关于交互网络在场景理解与基于想象的决策中的应用，请参阅我们投往 ICLR 2017 的两篇文章：[Discovering objects and their relations from entangled scene representations](https://openreview.net/forum?id=Bk2TqVcxe) 与 [Metacontrol for Adaptive Imagination-Based Optimization](https://openreview.net/forum?id=Bk8BvDqex)。

**NIPS 现场信息：** 12 月 5 日（周一）18:00 - 21:30 @ Area 5+6+7+8 #48
12 月 9 日（周五）08:00 - 18:30 @ Hilton Diag. Mar, Blrm. C

## Strategic Attentive Writer for Learning Macro-Actions

**作者：** Alexander (Sasha) Vezhnevets, Volodymyr Mnih, Simon Osindero, Alex Graves, Oriol Vinyals, John Agapiou, Koray Kavukcuoglu

学习时间上延展的动作，以及更一般的时间抽象，是强化学习中长期存在的问题。它们通过支持结构化探索和节省计算来促进学习。在本文中，我们提出一种新颖的深度循环神经网络架构，它在强化学习设定下纯粹通过与环境的交互、以端到端的方式学会构建隐式规划。该网络构建一个内部规划，并在观察到来自环境的下一个输入时持续更新。它还能通过学习「规划可以坚持多久」——即无需重新规划地持续执行多长时间——把这个内部表示切分为连续的子序列。结合这些特性，我们提出的模型——称为 STRategic Attentive Writer（STRAW）——能够学习不同长度的高层次、时间抽象化的宏动作（macro-action），而这些宏动作完全从数据中学得，不依赖任何先验信息。

请[在此](https://www.youtube.com/watch?v=niMOdSu3yio)观看视频。

更多细节与相关工作，请参阅[论文](https://arxiv.org/pdf/1606.04695.pdf)。

**NIPS 现场信息：** 12 月 5 日（周一）18:00 - 21:30 @ Area 5+6+7+8 #111

## Matching Networks for One Shot Learning

**作者：** Oriol Vinyals, Charles Blundell, Timothy Lillicrap, Koray Kavukcuoglu, Daan Wierstra

对于未见过的新类别，哪怕只给出寥寥几个、甚至仅一个样本，使用 Matching Networks 也能在 ImageNet 上取得很高的分类准确率。其核心架构简单直接、易于训练，并在一系列图像与文本分类任务上都有良好表现。

![用于单样本学习的 Matching Network 架构图，展示由狗图像组成的支持集经函数 g_theta 映射、目标图像经 f_theta 映射，以计算对各类别的注意力并输出预测。](https://lh3.googleusercontent.com/iwF_oAw70rcv-PZlHyr3rEL353s7WqNB3DghzHk90NyFwkKSb7zDrK-tW5B1BKdAdBZItjxy-R31R_7lvski2OvHT6aIXOtD8vCQiUeQYquyXoVlk3I=w1440)

Matching Networks 的训练方式与测试方式相同：呈现一系列即时的单样本学习训练任务，其中训练集的每个样本并行送入网络。然后，Matching Networks 被训练在许多不同的输入训练集上正确分类。其效果是训练出一个无需哪怕一步梯度下降就能在新数据集上进行分类的网络。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1606.04080)。

**NIPS 现场信息：** 12 月 5 日（周一）18:00 - 21:30 @ Area 5+6+7+8 #139

## Safe and efficient off-policy reinforcement learning

**作者：** Remi Munos, Tom Stepleton, Anna Harutyunyan, Marc G. Bellemare

我们的目标是设计一种具备两个理想性质的强化学习（RL）算法。其一，能够使用 off-policy 数据——这在我们使用经验回放或观察日志数据时对探索很重要。其二，能够使用多步回报，以便更快地传播奖励并避免近似/估计误差的累积。这两个性质对深度强化学习都至关重要。

我们提出「Retrace」算法，它使用多步回报，并且能够安全而高效地利用任何 off-policy 数据。我们证明了该算法在策略评估与最优控制两种设定下的收敛性。

作为推论，我们证明了 Watkin 的 Q(λ) 收敛到 Q\*（这是自 1989 年以来悬而未决的开放问题）。

最后，我们报告了在 Atari 领域上的数值结果，展示了 Retrace 相对于竞争算法的巨大优势。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1606.02647)。

**NIPS 现场信息：** 12 月 5 日（周一）18:00 - 21:30 @ Area 5+6+7+8 #151

## Blazing the trails before beating the path: Sample efficient Monte-Carlo planning

**作者：** Jean-Bastien Grill (INRIA), Michal Valko (INRIA), Remi Munos

你是一个机器人，你生活在一个马尔可夫决策过程（MDP）中，其中从状态-动作到下一状态有有限或无限多种转移。你有头脑，所以你行动之前先规划。幸运的是，你的机器人父母为你配备了一个生成模型，让你可以做蒙特卡洛规划。世界正在等你，你没有时间可以浪费。你希望你的规划是高效的。样本高效的。确切地说，你想通过只探索沿着近优策略可达的那部分状态，来利用 MDP 可能存在的结构。你想要依赖于「近优状态数量」这一度量的样本复杂度保证。你想要把蒙特卡洛采样（用于估计期望）扩展到交替进行最大化（对动作）与期望（对下一状态）的问题上。你想要实现起来简单、计算上高效的东西。你想要一切，而且现在就要。你想要 TrailBlazer。

更多细节与相关工作，请参阅[论文](https://papers.nips.cc/paper/6253-blazing-the-trails-before-beating-the-path-sample-efficient-monte-carlo-planning.pdf)。

**NIPS 现场信息：** 12 月 6 日（周二）17:00 - 17:20 @ Area 3（口头报告，Theory 分会场）
12 月 6 日（周二）@ Area 5+6+7+8 #193

## Deep Exploration via Bootstrapped DQN

**作者：** Ian Osband, Charles Blundell, Alex Pritzel and Benjamin Van Roy

复杂环境中的高效探索仍然是强化学习（RL）的一大挑战。近来强化学习领域出现了许多突破，但其中许多算法在学会做出好决策之前，需要海量数据（数百万局游戏）。在许多现实场景中，如此大量的数据并不可行。

这些算法学习如此缓慢的原因之一，是它们没有收集到用于了解问题的「正确」数据。这些算法使用抖动式探索（dithering，即随机采取动作）来探索环境——这比「深度」探索（deep exploration，在多个时间步上优先考虑可能富含信息的策略）的效率可能低指数倍。关于深度探索的算法，已有大量面向统计高效强化学习的文献。问题在于，这些算法没有一个能与深度学习在计算上兼容……直到现在。

本文的关键突破包括：

- 我们提出了第一个把深度学习与深度探索结合起来的实用强化学习算法：Bootstrapped DQN。
- 我们证明该算法可以带来指数级加快的学习。
- 我们在 Atari 2600 上取得了新的最先进结果。

更多细节与相关工作，请参阅[论文](https://papers.nips.cc/paper/6501-deep-exploration-via-bootstrapped-dqn)及我们的[视频播放列表](https://www.youtube.com/playlist?list=PLdy8eRAW78uLDPNo1jRv8jdTx7aup1ujM)。

**NIPS 现场信息：** 12 月 5 日（周一）18:00 - 21:30 @ Area 5+6+7+8 #79
