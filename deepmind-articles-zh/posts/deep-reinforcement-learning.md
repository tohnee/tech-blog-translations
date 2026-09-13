---
title: "深度强化学习"
title_en: "Deep Reinforcement Learning"
source: https://deepmind.google/blog/deep-reinforcement-learning/
site: deepmind
date: 2016-06-17
crawled: 2026-09-13
translated: 2026-09-13
---

# 深度强化学习

> 原文：[Deep Reinforcement Learning](https://deepmind.google/blog/deep-reinforcement-learning/) · Google DeepMind

人类擅长解决各种各样富有挑战性的问题，从低层次的运动控制一直到高层次的认知任务。我们在 DeepMind 的目标是创造出能够达到类似性能与通用性水平的人工智能体。像人类一样，我们的智能体自主学习那些能带来最大长期回报的成功策略。这种仅凭奖励或惩罚、通过试错来学习的范式，被称为[强化学习](https://en.wikipedia.org/wiki/Reinforcement_learning)（RL）。同样像人类一样，我们的智能体直接从视觉等原始输入中构建并学习自己的知识，不依赖任何人工设计的特征或领域启发式规则。这靠的是对神经网络的[深度学习](https://en.wikipedia.org/wiki/Deep_learning)。在 DeepMind，我们开创性地把这两种方法结合起来——即深度强化学习——创造出最早在许多富有挑战性的领域中达到人类水平性能的人工智能体。

我们的智能体必须不断做出价值判断，以便在好动作与坏动作之间选出前者。这些知识由一个 Q 网络来表示，它估计智能体在执行某个特定动作之后可以预期获得的总奖励。两年前，我们推出了第一个广泛成功的[深度强化学习算法](https://arxiv.org/pdf/1312.5602.pdf)。其核心思想是用深度神经网络来表示 Q 网络，并训练这个 Q 网络预测总奖励。以往把强化学习与神经网络结合的尝试大多因学习不稳定而失败。为了解决这些不稳定问题，我们的深度 Q 网络（DQN）算法会存储智能体的全部经验，然后随机采样并回放这些经验，以提供多样化、去相关的训练数据。我们把 DQN 用于学习在 Atari 2600 游戏机上玩游戏。在每个时间步，智能体观察屏幕上的原始像素、与游戏得分对应的奖励信号，并选择一个摇杆方向。在我们的[《自然》论文](https://storage.googleapis.com/deepmind-data/assets/papers/DeepMindNature14236Paper.pdf)中，我们为 50 个不同的 Atari 游戏分别训练了 DQN 智能体，全程不提供任何关于游戏规则的先验知识。

![横向条形图，比较 DQN（蓝色）与最佳线性学习器（灰色）在 50 个 Atari 2600 游戏上的表现（以人类表现为 100% 进行归一化）。游戏按 DQN 得分排序，从 2539% 的 Video Pinball 一路排到 0% 的 Montezuma's Revenge，图中有一条水平分隔线，区分 DQN 达到或超过人类水平的游戏与低于人类水平的游戏。](https://lh3.googleusercontent.com/ecmmIRmj9_Ippn9KP0Z-40ZbL0ll6RG1GRj_jFQHs6oX3uSTt9QDfIWTph_1ekCTi_9nw5Jd6dnPTZ4cHxLZi-CNu5x3UIbfuegrfSqdGJ8g9Gee=w1440)

令人惊叹的是，DQN 在它所应用的 50 个游戏中几乎有一半达到了人类水平；远远超过此前任何方法。[DQN 源代码](https://sites.google.com/a/deepmind.com/dqn/)和 [Atari 2600 模拟器](http://stella.sourceforge.net/)向所有想亲自实验的人免费开放。

此后，我们从许多方面改进了 DQN 算法：进一步稳定[学习](https://arxiv.org/pdf/1509.06461.pdf)[动力学](https://arxiv.org/pdf/1512.04860.pdf)；为[回放的经验](https://arxiv.org/pdf/1511.05952.pdf)设置优先级；对输出进行[归一化](https://arxiv.org/pdf/1511.06581.pdf)、[聚合](https://arxiv.org/pdf/1602.04621.pdf)与[重新缩放](https://arxiv.org/pdf/1602.07714.pdf)。把其中几项改进结合在一起，使 Atari 游戏的平均得分提升了 300%；如今几乎所有 Atari 游戏都达到了人类水平的表现。我们甚至能训练[单个神经网络](http://proceedings.mlr.press/v37/schaul15.pdf)来学习[多个 Atari 游戏](https://arxiv.org/pdf/1511.06295.pdf)。我们还构建了一个大规模分布式的深度强化学习系统，称为 [Gorila](https://8109f4a4-a-62cb3a1a-s-sites.googlegroups.com/site/deeplearning2015/1.pdf?amp%3Battredirects=2&attachauth=ANoY7crMVozLCUypNspkLHOoqcYslQMCOnrt0wRXpyXexWPae2CEpYUgmI19cOvTa7r41xbYwjSYL6EBpUKiUCHKpcf1fLwvjbI5a8GVyIYEEDtqv4tbctQTqnZzJ1BWvfAdFHS-0X1ACki0HYpfwgVhkLBrp0ELPt8ivrkBdd94YyaHF-kcDoY4NsYbO9ytKG6lkcxCUcgDRaFC-ZEasOoSAl1zxWnmxw%3D%3D&attredirects=0)，它利用 Google Cloud 平台把训练时间缩短了一个数量级；该系统已被应用于 Google 内部的推荐系统。

然而，深度 Q 网络只是解决深度强化学习问题的一种方式。我们最近推出了一种基于异步强化学习、更实用也更有效的方法。这一方法利用了标准 CPU 的多线程能力，其思想是并行执行智能体的许多实例，但使用一个共享的模型。这为经验回放提供了一个可行的替代方案，因为并行化同样能使数据多样化并去除相关性。我们的异步 actor-critic 算法 [A3C](https://arxiv.org/pdf/1602.01783.pdf) 把深度 Q 网络与用于选择动作的深度策略网络结合起来。它以 DQN 训练时间的一小部分、Gorila 资源消耗的一小部分，取得了最先进的结果。通过为[内在动机](https://arxiv.org/abs/1606.01868)与[时间抽象化规划](https://arxiv.org/pdf/1606.04695.pdf)构建新方法，我们还在最臭名昭著的困难 Atari 游戏（如 Montezuma's Revenge）上取得了突破性结果。

虽然 Atari 游戏展示了相当大的多样性，但它们仅限于基于 2D 精灵图的电子游戏。我们最近推出了 Labyrinth：一套富有挑战性的 3D 导航与解谜环境。同样，智能体只观察来自其直接视野的基于像素的输入，必须摸索出地图才能发现并获取奖励。

![DeepMind 的 Labyrinth 游戏的四幅第一人称视角截图，展示风格各异的彩色 3D 解谜房间：蜂窝纹理的地板、电路图案的墙壁、各种障碍物以及可拾取的奖励物品。](https://lh3.googleusercontent.com/EKaVYDjZM6dTjNKsi7ua5gYqyRQx54HN1vO6JkpyCsEMJo_Qf3Pz_CCLXv9fTYBKl2q6oQtxMIPVSbOBF-PQ_2S40SwG-ynhmkX5ipBPF4Ttd-micEs=w1440)

令人惊叹的是，A3C 算法开箱即用，就在许多 Labyrinth 任务上达到了人类水平。一种基于情节记忆（episodic memory）的[替代方法](https://arxiv.org/pdf/1606.04460.pdf)同样被证明是成功的。Labyrinth 也将在未来几个月内开源发布。

我们还为机器人操作与运动（locomotion）等连续控制问题开发了多种深度强化学习方法。我们的确定性策略梯度算法（[DPG](http://jmlr.org/proceedings/papers/v32/silver14.pdf)）提供了 DQN 在连续情形下的对应版本，利用 Q 网络的可微性来解决[种类繁多的](https://arxiv.org/pdf/1509.02971.pdf)[连续控制任务](http://arxiv.org/pdf/1510.09142)。[异步强化学习](http://arxiv.org/pdf/1602.01783)在这些领域同样表现出色，再配合层次化控制策略，就能在完全不了解动力学先验知识的情况下解决诸如蚂蚁足球、54 维人形绕桩等富有挑战性的问题。

围棋是经典游戏中最具挑战性的一个。尽管经过数十年的努力，此前的方法只达到业余水平。我们开发了一种深度强化学习算法，通过自我博弈的对局同时学习一个价值网络（预测胜者）和一个策略网络（选择动作）。我们的程序 AlphaGo 把这些深度神经网络与最先进的树搜索结合起来。2015 年 10 月，AlphaGo 成为[第一个击败职业人类棋手的程序](https://www.nature.com/articles/nature16961)。2016 年 3 月，AlphaGo 以 4 比 1 [击败了李世石](https://deepmind.com/research/case-studies/alphago-the-story-so-far)（Lee Sedol，过去十年最强的棋手，拥有惊人的 18 个世界冠军头衔），估计有 2 亿观众观看了这场对决。

![在 Google DeepMind 挑战赛上，李世石（右）在传统围棋盘上下出一手棋，对面由黄士杰（Aja Huang，左）操作 AlphaGo 的界面。](https://lh3.googleusercontent.com/HlvA_-wpA-MxDBy-swN0gmKwNWfvE1QqeCqy-jpJXHaO3Pq2v46kBCXndQdzvolgorvqjfGEIUaHoshcBuOAaHAaxdTLkgay6-ppIaTcV1LJpML0ffY=w1440)

另外，我们还为[深度强化学习](https://arxiv.org/pdf/1603.01121.pdf)开发了[博弈论](http://proceedings.mlr.press/v37/heinrich15.pdf)方法，最终打造出一个在单挑限注德州扑克上[超越人类](http://www.aaai.org/ocs/index.php/IJCAI/IJCAI15/paper/view/11230/10741)的扑克玩家。

从 Atari 到 Labyrinth，从运动控制到机械操作，再到扑克乃至围棋，我们的深度强化学习智能体已经在各种各样富有挑战性的任务上展现了卓越的进步。我们的目标是继续提升智能体的能力，并把它们用于[医疗保健](https://deepmind.com/about/health)等重要领域，为社会带来积极的影响。
