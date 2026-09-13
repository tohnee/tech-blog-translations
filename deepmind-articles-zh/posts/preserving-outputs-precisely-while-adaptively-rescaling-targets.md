---
title: "在自适应重缩放目标的同时精确保留输出"
title_en: "Preserving Outputs Precisely while Adaptively Rescaling Targets"
source: https://deepmind.google/blog/preserving-outputs-precisely-while-adaptively-rescaling-targets/
site: deepmind
date: 2018-09-13
crawled: 2026-09-13
translated: 2026-09-13
---

# 在自适应重缩放目标的同时精确保留输出

> 原文：[Preserving Outputs Precisely while Adaptively Rescaling Targets](https://deepmind.google/blog/preserving-outputs-precisely-while-adaptively-rescaling-targets/) · Google DeepMind

多任务学习——让单个智能体学会解决许多不同的任务——是人工智能研究的一个长期目标。最近，这一领域取得了许多出色的进展，例如 [DQN](https://deepmind.com/research/publications/human-level-control-through-deep-reinforcement-learning/) 这样的智能体能够用同一算法学会玩包括《打砖块》（Breakout）和《乒乓》（Pong）在内的多个游戏。但这些算法是被用来为每个任务训练单独的专家智能体。随着人工智能研究迈向更复杂的现实世界领域，构建一个单一的通用智能体——而非多个专家智能体——来学习执行多项任务将至关重要。然而，迄今为止，这已被证明是一项重大挑战。

原因之一是，我们的强化学习智能体用来判断成功的奖励尺度往往各不相同，导致它们把注意力集中在奖励任意偏高的任务上。例如，在 Atari 游戏《乒乓》中，智能体每步得到的奖励为 -1、0 或 +1。相比之下，玩《吃豆人小姐》（Ms. Pac-Man）的智能体可以在一步中获得数百分甚至上千分。即使单个奖励的大小具有可比性，随着智能体水平提升，奖励出现的频率也会随时间变化。这意味着智能体倾向于关注那些分数巨大的任务，导致在某些任务上表现更好，而在另一些任务上则差得多。

为了解决这类问题，我们开发了 [PopArt](https://arxiv.org/abs/1809.04474)，一种能够自适应调整每个游戏中分数尺度的技术，使智能体无论每个具体游戏中可用奖励的尺度如何，都判断这些游戏具有同等的学习价值。我们将 PopArt 归一化应用于一个最先进的强化学习智能体，得到了一个能够玩整套 57 个多样 Atari 视频游戏的单一智能体，且在整个集合上的中位数表现超过人类水平。

广义上讲，深度学习依赖于更新神经网络的权重，使其输出更接近期望的目标输出。当神经网络被用于深度强化学习时，情况也是如此。PopArt 的工作原理是估计这些目标（例如游戏中的分数）的均值和离散程度，然后在用它们更新网络权重之前，利用这些统计量对目标进行归一化。使用归一化后的目标能让学习更稳定，并对尺度和偏移的变化更加鲁棒。为了获得准确的估计值——例如对未来分数的期望——随后可以通过对归一化过程求逆，把网络的输出重新缩放回真实的目标范围。如果处理得简单粗暴，每次对统计量的更新都会改变所有未归一化的输出，包括那些已经非常出色的输出。我们通过在每次更新统计量时以相反方向更新网络来防止这种情况发生，并且这可以精确地做到。这意味着我们既获得了尺度良好的更新带来的好处，又保持了先前学到的输出不受影响。正是出于这些原因，我们把这种方法命名为 PopArt：它的全称即「在自适应重缩放目标的同时精确保留输出」（Preserving Outputs Precisely while Adaptively Rescaling Targets）。

## PopArt 作为奖励截断的替代方案

传统上，研究者通过在强化学习算法中使用奖励截断（reward clipping）来克服奖励尺度不一的问题。这种方法把或大或小的分数截断为 1 或 -1，从而大致对期望奖励进行归一化。虽然这让学习变得更容易，但它也改变了智能体的目标。例如，在《吃豆人小姐》中，目标是收集每颗价值 10 分的豆子，并吃掉价值 200 到 1600 分不等的幽灵。在奖励被截断的情况下，对智能体而言吃一颗豆子和吃一个幽灵没有明显区别，导致智能体只吃豆子、从不去追幽灵，正如[这段视频](https://videos.files.wordpress.com/1nYybrEH/clipped_pacman_dvd.mp4)所示。当我们移除奖励截断、改用 PopArt 的自适应归一化来稳定学习时，则会产生截然不同的行为：智能体会去追幽灵，并取得更高的分数，如[这段视频](https://videos.files.wordpress.com/0XtMJ12x/pacman_dvd.mp4)所示。

## 基于 PopArt 的多任务深度强化学习

我们将 PopArt 应用于重要性加权 Actor-Learner 架构（IMPALA）——DeepMind 最常用的深度强化学习智能体之一。在我们的实验中，与不带 PopArt 的基线智能体相比，PopArt 大幅提升了智能体的性能。无论奖励被截断还是未被截断，PopArt 智能体在各游戏上的中位数得分都高于人类中位数。这远高于带截断奖励的基线，而带未截断奖励的基线则完全无法达到有意义的性能，因为它无法有效应对各游戏之间奖励尺度的巨大差异。

![折线图，对比三个多任务强化学习智能体的性能。纵轴为中位数归一化得分（Median Normalised Score），横轴为环境帧数（至 1.2e10）。PopArt-IMPALA（未截断）智能体以绿色实线表示，取得最高分，在 100 附近趋于平稳。IMPALA（截断）智能体以蓝色虚线表示，得分约达 60。IMPALA（未截断）智能体以蓝色实线表示，未能取得进展，在零附近保持水平。](https://lh3.googleusercontent.com/lkgdCuq8hHfpmVZJUrd1cFjdkoFtA6XKXCl_yMa5akdDgD1tKMRiGQvNvgIISTUJRAgJF90zS2VWZnbs1-jyAQ3MlwNB0dWoVlKVN__7lO-B4Z3rSg=w1440)

57 个 Atari 游戏上的中位数标准化性能。每条线对应一个被训练用同一个神经网络玩所有这些游戏的智能体的中位数表现。实线表示使用了奖励截断，虚线表示使用了未截断的奖励。

这是我们首次看到单个智能体在这类多任务环境中取得超人类的表现，这表明 PopArt 可以为「如何在不手动截断或缩放的情况下平衡各种目标」这一开放研究问题提供一些答案。随着我们把 AI 应用于更复杂的多模态领域——智能体必须学会在众多不同奖励的目标之间进行权衡——它在学习过程中自动调整归一化的能力可能会变得非常重要。

**附注**

更多细节请参见我们最新的[论文](https://arxiv.org/abs/1809.04474)以及最初的[论文](https://arxiv.org/abs/1602.07714)。

这项工作由 Matteo Hessel、Hubert Soyer、Lasse Espeholt、Wojciech Czarnecki、Simon Schmitt 和 Hado van Hasselt 完成。
