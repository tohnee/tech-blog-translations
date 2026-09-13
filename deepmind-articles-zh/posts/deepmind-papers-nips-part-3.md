---
title: "DeepMind 论文精选 @ NIPS（第三部分）"
title_en: "DeepMind Papers @ NIPS (Part 3)"
source: https://deepmind.google/blog/deepmind-papers-nips-part-3/
site: deepmind
date: 2016-12-07
crawled: 2026-09-13
translated: 2026-09-13
---

# DeepMind 论文精选 @ NIPS（第三部分）

> 原文：[DeepMind Papers @ NIPS (Part 3)](https://deepmind.google/blog/deepmind-papers-nips-part-3/) · Google DeepMind

## Scaling Memory-Augmented Neural Networks with Sparse Reads and Writes

**作者：** J Rae, JJ Hunt, T Harley, I Danihelka, A Senior, G Wayne, A Graves, T Lillicrap

我们能够回忆起海量的记忆，并在表面上看毫不相关的事件之间建立联系。当你阅读一本小说时，你很可能不仅对刚读过的最后几段内容记得相当清楚，还能记得小说前文的情节梗概、人物之间的关联以及角色性格特征。

许多记忆类的机器学习模型，例如长短期记忆网络（Long Short Term Memory），在这类任务上表现吃力。这些模型的计算成本随其可存储记忆数量的增加呈二次增长，因此它们能容纳的记忆数量相当有限。近来，可微分神经计算机（Differentiable Neural Computer）或 Memory Networks 等记忆增强神经网络通过在计算之外添加独立的记忆模块，在阅读短篇故事并回答问题等任务上展现出可观的结果（如 Babi 等工作）。

然而，尽管这些新架构在小任务上表现可观，它们却使用「软注意力」（soft-attention）来访问记忆，这意味着在每个时间步都要触及记忆中的每一个词。因此，虽然它们可以扩展到短篇故事，但要阅读整本小说还相去甚远。

在这项工作中，我们开发了一套技术，利用此类模型的稀疏近似来大幅提升其可扩展性。在这些稀疏模型中，每个时间步只触及记忆中极小的一部分。重要的是，我们证明了这样做不会损害模型的学习能力。这意味着稀疏记忆增强神经网络能够解决同类任务，但所需的资源少了数千倍；在进一步改进之后，它有望成为阅读小说的一种有前景的技术。

更多细节与相关工作，请参阅论文：<https://arxiv.org/abs/1610.09027>

**NIPS 现场信息：** 12 月 7 日（周三）18:00 - 21:30 @ Area 5+6+7+8 #17

## Attend, Infer, Repeat- Fast Scene Understanding with Generative Models

**作者：** S. M. Ali Eslami, Nicolas Heess, Theophane Weber, Yuval Tassa, David Szepesvari, Koray Kavukcuoglu, Geoffrey Hinton

![示意图，展示 Attend, Infer, Repeat（AIR）架构：输入图像「x」依次经过循环隐状态处理，生成关于物体存在、类别与位置（z_pres、z_what、z_where）的潜变量。右侧为由解码器基于这些推断步骤重建的 3D 桌面场景，上面摆放着锅、杯子和盘子。](https://lh3.googleusercontent.com/Px1VyeY825a1HxUMkVyZlcXNi-vP6UO3X17up88phd2O4VDFf5G_KaLuc6pBllVXUcYjiy_9YmY5uFH6dxlSN9ouaL2-LP7VCkDn99VJOAf-U4nLzpA=w1440)

想象一下晚饭后收拾餐桌的任务。为了规划你的动作，你需要判断桌上有哪些物体、它们各属于什么类别，以及每个物体在桌上的位置。换句话说，对于许多与真实世界的交互来说，感知问题远远不止图像分类。我们希望构建这样的智能系统：它学会把场景图像解析为在空间中排布、具有视觉与物理属性、且彼此之间存在功能关系的物体；并且希望以尽可能少的监督来实现这一点。

基于这一思路，我们的论文提出了一个框架，用于在显式地对物体进行推理的结构化生成式图像模型中进行高效推断。我们通过一个循环神经网络执行概率推断来实现这一点：该网络关注场景中的各个元素，并逐个加以处理。关键在于，模型自身会学习选择合适数量的推断步骤。

我们利用这一方案学习在部分指定的 2D 模型（可变尺寸的变分自编码器）与完全指定的 3D 模型（概率渲染器）中执行推断。我们证明，这类模型无需任何监督即可学会识别多个物体——对场景元素进行计数、定位与分类——例如，在神经网络的单次前向传播中分解含有不同数量物体的 3D 图像。

更多细节与相关工作，请参阅论文：<https://arxiv.org/abs/1603.08575>

**NIPS 现场信息：** 12 月 7 日（周三）18:00 - 21:30 @ Area 5+6+7+8 #2

## Unifying Count-Based Exploration and Intrinsic Motivation

**作者：** Marc G. Bellemare, Sriram Srinivasan, Georg Ostrovski, Tom Schaul, David Saxton, Remi Munos

虽然我们已经成功地把智能体训练到在许多 Atari 2600 游戏上超越人类的水平，但有些游戏仍然难得出奇。我们最喜欢的「难」游戏之一是《Montezuma's Revenge》（蒙特祖玛的复仇）。它以充满敌意、毫不留情的环境著称：智能体必须在一个满是陷阱的房间迷宫中穿行。每一关有 24 个房间，呈金字塔形，如下图所示：

![Montezuma's Revenge 中 24 个房间的金字塔形地图，顶部（第 1 室）是游戏起始房间的截图，其余房间以带编号的白色方块表示。](https://lh3.googleusercontent.com/iwjydWMaeAxyPLGS51TShnk73MYx7_sNf_Z2oWyvuVQtu8HdGcr57q4EhE9T0JFI4-qm3UYCYzK4EyYYHYKFPmv9z_77l2VVopQ8ZVMtiw5h5alM=w1440)

迄今为止，大多数已发表的智能体甚至连第一个房间都走不出去。

这些困难的强化学习问题有一个共同点：奖励稀少且难得一见。在强化学习中，探索是指智能体逐步理解其环境并发现奖励所在的过程。大多数实际的强化学习应用仍然依赖粗糙的算法，例如 epsilon-greedy（偶尔随机选择一个动作），因为更有理论依据的方法无法扩展。但 epsilon-greedy 的数据效率相当低，常常连起步都做不到。

在本文中，我们展示了可以利用简单的密度模型（为状态赋予概率）来「统计」我们访问某个特定状态的次数。我们把算法的输出称为伪计数（pseudo-count）。伪计数让我们得以把握不确定性：我们对「已经探索过游戏的这一部分」有多大把握？得益于此，我们在 Montezuma's Revenge 中取得了大幅进展。标准 DQN 算法平均每局得分不到 100 分；相比之下，我们得到 3439 分。为了让你感受一下差距，请对比两种方法访问过的房间（白色 = 未探索）：

![Montezuma's Revenge 中探索情况的对比：「无奖励加成」（上）只探索了两个房间，其余是空白方块；而「有奖励加成」（下）成功探索了 15 个房间，方块中填满了游戏截图。](https://lh3.googleusercontent.com/5po5MrSHfpafMNQ28XzCWuo3hI--wD7_iLAJvjmsR4OZr62aNDIQVCv4PEb7tPDbwnjPRJAkBVjITLOvCt_nd-S-NikDOdfV5DVUP-ddQTexFuoWzQ=w1440)

总而言之，我们的智能体穿行了 15 个房间，而 DQN 只有 2 个。另请观看[我们的智能体玩 Montezuma's Revenge](https://youtu.be/0yI2wJ6F8r0) 的视频。

我们的方法受到 White 1959 年内在动机（intrinsic motivation）思想的启发：智能体行动首先是为了理解自己的环境（另见 Oudeyer、Barto 和 Schmidhuber 较新的工作）。令人兴奋的是，由于我们的智能体玩游戏是为了满足好奇心而不是立即取胜，它们最终反而超越了同类。

更多细节与相关工作，请参阅[论文](https://papers.nips.cc/paper/6383-unifying-count-based-exploration-and-intrinsic-motivation.pdf)。

**NIPS 现场信息：** 12 月 7 日（周三）18:00 — 21:30 @ Area 5+6+7+8 海报 #71

## Learning values across many orders of magnitude

**作者：** H van Hasselt, A Guez, M Hessel, V Mnih, D Silver

有时我们想学习一个事先不知道其量级、或量级会随时间变化的函数。例如，在基于价值的强化学习中，当我们的策略随时间改进时就会发生这种情况。起初，由于策略还不够好，价值可能很小；但之后它们会反复地、不可预测地增大。这对许多（深度）学习算法来说是个问题，因为它们在设计时往往没有考虑这类情形，于是会变得缓慢或不稳定。

一个具体的动机是：[DQN](https://deepmind.com/research/publications/human-level-control-through-deep-reinforcement-learning/) 算法成功学会玩许多 Atari 游戏，但它把所有非零奖励都截断到 -1 和 1。这让学习变得更容易，因为它改变了行为。例如，在《Ms. Pac-Man》里吃掉幽灵（实际奖励 100+）看上去就与吃掉豆子（实际奖励 10）得到的奖励一样了。

我们提出转而对呈现给深度神经网络的目标进行自适应归一化。为了直观感受这一方法的有效性，我们可以看看在 57 个不同的 Atari 游戏上学习过程中梯度（l2 范数）的量级：

![折线图，展示三种不同训练配置在 Atari 游戏上随帧数（百万）变化的梯度范数（对数刻度）：不截断（红）、截断（蓝）与 Pop-Art（绿）。不截断的梯度在六个数量级之间大幅波动，截断的梯度跨越约四个数量级，而 Pop-Art 的梯度最为稳定，仅在 1 到 100 之间的两个数量级内变化。](https://lh3.googleusercontent.com/wl5szX96XjEdaeDJedFAm2AvhaYI6bs30GfwaME3E1AaFB15y-salxTt_q8CSTbkA9zSWCDKIv99wwbbjy_0GxVUid1CH-p1ZvvGtyVukO-1os1C=w1440)

[Double DQN](https://hadovanhasselt.com/2015/12/10/deep-reinforcement-learning-with-double-q-learning-2/) 在左侧使用不截断的奖励，中间使用截断的奖励，右侧使用 Pop-Art。Pop-Art 带来的梯度一致性好得多，其量级落在窄得多的范围内，因而也更可预测。不截断的版本则反复无常得多——注意 y 轴是对数刻度。Pop-Art 的梯度归一化程度甚至优于截断变体，而且不像截断那样从性质上改变任务。在某些游戏上，所得性能远超此前最先进的水平。

Pop-Art 并不局限于 DQN、Atari 或强化学习。任何需要学习量级未知的函数、或量级随时间变化的场合，它都可能有用。此外，在同时学习多个信号时——例如这些信号具有不同的单位和/或模态——它也可能有用。按输出逐一归一化，有助于把信号的量级与其重要性解耦。

更多细节与相关工作，请参阅[论文](https://arxiv.org/abs/1602.07714)及配套[视频](https://youtu.be/68LfBLPLySg)。

**NIPS 现场信息：** 12 月 7 日（周三）18:00 — 21:30 @ Area 5+6+7+8 #81
