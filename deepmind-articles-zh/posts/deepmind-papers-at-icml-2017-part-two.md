---
title: "DeepMind 在 ICML 2017 的论文（第二部分）"
title_en: "DeepMind papers at ICML 2017 (part two)"
source: https://deepmind.google/blog/deepmind-papers-at-icml-2017-part-two/
site: deepmind
date: 2017-08-04
crawled: 2026-09-13
translated: 2026-09-13
---

# DeepMind 在 ICML 2017 的论文（第二部分）

> 原文：[DeepMind papers at ICML 2017 (part two)](https://deepmind.google/blog/deepmind-papers-at-icml-2017-part-two/) · Google DeepMind

本系列共三篇，这是第二篇，概述我们将在澳大利亚悉尼 ICML 2017 大会上展示的论文。

## Why is Posterior Sampling Better than Optimism for Reinforcement Learning?（在强化学习中后验采样为何优于乐观主义？）

**作者：** Ian Osband, Benjamin Van Roy

计算结果表明，用于强化学习的后验采样（PSRL）显著优于 UCRL2 等由乐观主义驱动的现有算法。我们深入揭示了这一性能提升的幅度及其背后的驱动现象。我们利用这一洞见，为 PSRL 在有限时域分段式马尔可夫决策过程中建立了 $\tilde{O}(H\sqrt{SAT})$ 的贝叶斯后悔界。这改进了此前任何强化学习算法的最佳贝叶斯后悔界 $\tilde{O}(H S \sqrt{AT})$。我们的理论结果得到了大量实证评估的支持。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1607.00215)。

**ICML 会场信息：**

Monday 07 August, 11:42-12:00 @ C4.5（口头报告）

Monday 07 August, 18:30-22:00 @ Gallery #36（海报）

## DARLA: Improving Zero-Shot Transfer in Reinforcement Learning（DARLA：改进强化学习中的零样本迁移）

**作者：** Irina Higgins\*, Arka Pal\*, Andrei Rusu, Loic Matthey, Chris Burgess, Alexander Pritzel, Matt Botvinick, Charles Blundell, Alexander Lerchner

现代深度强化学习智能体依赖大量数据来学习如何行动。在某些场景（例如机器人学）中，获取大量训练数据可能并不可行。因此，这类智能体通常先在与目标任务相关、但数据易于获取的任务（例如仿真）上训练，寄希望于学到的知识能泛化到目标任务（例如现实）。我们提出 DARLA——一个解耦表示学习智能体（DisentAngled Representation Learning Agent），它利用自身可解释、结构化的视觉，以对环境中各种新变化保持稳健的方式学习行动——其中包括机器人学中从仿真到现实的迁移场景。我们证明 DARLA 显著优于所有基线方法，而且其表现关键取决于视觉表示的质量。

更多细节与相关工作，请参阅[论文](http://arxiv.org/abs/1707.08475)。

**ICML 会场信息：**

Monday 07 August, 16:42-17:00 @ C4.5（口头报告）\

Monday 07 August, 18:30-22:00 @ Gallery #123（海报）

## Automated Curriculum Learning for Neural Networks（神经网络的自动化课程学习）

**作者：** Alex Graves, Marc G. Bellemare, Jacob Menick, Koray Kavukcuoglu, Remi Munos

随着神经网络被应用于越来越复杂的问题，对高效课程学习的需求也日益迫切。然而，设计有效的课程十分困难，通常需要大量手工调校。本文利用强化学习来自动化网络在课程中遵循的路径（即教学大纲），以最大化整体学习进展速率。我们考虑了九种不同的进展指标，其中包括一类新颖的复杂度增益信号。在三个问题上的实验结果表明，自动推导的教学大纲可以带来高效的课程学习，即使在并非为课程学习专门设计的数据（例如 bAbI 任务）上也是如此。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1704.03003)。

**ICML 会场信息：**

Monday 07 August, 16:42-17:00 @ C4.6 & C4.7（口头报告）

Monday 07 August, 18:30-20:00 @ Gallery #127（海报）

## Learning to learn without gradient descent by gradient descent（不用梯度下降、而用梯度下降来学习如何学习）

**作者：** Yutian Chen, Matthew Hoffman, Sergio Gomez, Misha Denil, Timothy Lillicrap, Matthew Botvinick , Nando de Freitas

我们通过梯度下降训练循环神经网络优化器，其训练对象是一些简单的合成函数。学到的优化器表现出显著程度的迁移能力：它们可以被用来高效优化一大类无导数黑盒问题，包括连续老虎机（bandit）问题、控制问题、全局优化基准以及超参数调优任务。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1611.03824)。

**ICML 会场信息：**

Monday 07 August, 17:15-17:33 @ Darling Harbour Theatre（口头报告）

Tuesday 08 August, 18:30-22:00 @ Gallery #6（海报）

## A Distributional Perspective on Reinforcement Learning（强化学习的分布视角）

**作者：** Marc G. Bellemare\*, Will Dabney\*, Remi Munos

我们论证了价值分布（value distribution）的根本重要性：它指的是强化学习智能体所获随机回报的分布。这与强化学习的常见做法形成对照——后者建模的是这一回报的期望，即价值。尽管已有相当篇幅的文献研究价值分布，但迄今为止它总是被用于特定目的，例如实现风险感知行为。我们从策略评估与控制两种设置下的理论结果出发，揭示了后者中存在的一种显著分布不稳定性。随后，我们利用分布视角设计了一种新算法，将贝尔曼方程应用于近似价值分布的学习。我们在街机学习环境（Arcade Learning Environment）的游戏套件上评估了该算法，既取得了当时最先进的结果，也获得了表明价值分布在近似强化学习中重要性的经验证据。最后，我们结合理论与实证证据，阐明了价值分布在近似设置下影响学习的种种方式。

更多细节与相关工作，请参阅[博客文章](https://deepmind.com/blog/article/going-beyond-average-reinforcement-learning)和[论文](https://arxiv.org/abs/1707.06887)。

**ICML 会场信息：**

Monday 07 August, 17:33-17:51 @ C4.5（口头报告）

Tuesday 08 August, 18:30-22:00 @ Gallery #13（海报）

## A Laplacian Framework for Option Discovery in Reinforcement Learning（强化学习中选项发现的拉普拉斯框架）

**作者：** Marlos Machado (Univ. Alberta), Marc G. Bellemare, Michael Bowling

表示学习与选项（option）发现是强化学习（RL）中最大的两个挑战。原型价值函数（PVFs）是马尔可夫决策过程（MDP）中一种著名的表示学习方法。本文通过展示 PVF 如何隐式地定义选项，来解决选项发现问题。具体做法是引入「本征目的」（eigenpurposes）——一种由学到的表示导出的内在奖励函数。由本征目的发现的选项沿着状态空间的主方向行进。它们对多个任务都有用，因为它们的发现过程完全不依赖环境的奖励。此外，不同选项在不同时间尺度上起作用，这使它们有助于探索。我们在传统的表格型领域以及 Atari 2600 游戏中展示了本征目的的特性。

更多细节与相关工作，请参阅[论文](http://proceedings.mlr.press/v70/machado17a/machado17a.pdf)。

**ICML 会场信息：**

Monday 07 August, 18:09-18:27 @ C4.5（口头报告）

Tuesday 08 August 18:30-20:00 @ Gallery #23（海报）

## Neural Audio Synthesis of Musical Notes with WaveNet Autoencoders（用 WaveNet 自编码器对乐音进行神经音频合成）

**作者：** Sander Dieleman, Karen Simonyan, Jesse Engel (Google Brain), Cinjon Resnick (Google Brain), Adam Roberts (Google Brain), Douglas Eck (Google Brain), Mohammad Norouzi (Google Brain)

在本文中，我们引入了一个强大的新型 WaveNet 风格自编码器模型，它用从原始音频波形中学到的时间编码来条件化一个自回归解码器。我们还发布了 NSynth——一个大规模、高质量的乐音数据集，其规模比同类公开数据集大一个数量级。借助 NSynth，我们展示了 WaveNet 自编码器相比经过精细调优的频谱自编码器基线在定性与定量性能上的提升。最后，我们证明该模型学到了一个嵌入流形，允许在不同乐器之间变形（morphing），在音色上有意义地插值，创造出真实而富有表现力的新型声音。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1704.01279)。

**ICML 会场信息：**

Tuesday 08 August, 14:42-15:00 @ Parkside 1（口头报告）

Tuesday 08 August, 18:30-22:00 @ Gallery #98（海报）
