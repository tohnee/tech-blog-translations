---
title: "MuZero：无需规则即可掌握围棋、国际象棋、将棋和 Atari"
title_en: "MuZero: Mastering Go, chess, shogi and Atari without rules"
source: https://deepmind.google/blog/muzero-mastering-go-chess-shogi-and-atari-without-rules/
site: deepmind
date: 2020-12-23
crawled: 2026-09-13
translated: 2026-09-13
---

# MuZero：无需规则即可掌握围棋、国际象棋、将棋和 Atari

> 原文：[MuZero: Mastering Go, chess, shogi and Atari without rules](https://deepmind.google/blog/muzero-mastering-go-chess-shogi-and-atari-without-rules/) · Google DeepMind

2016 年，我们推出了 [AlphaGo](https://deepmind.com/research/case-studies/alphago-the-story-so-far)，这是第一个在古老的围棋项目中击败人类的人工智能（AI）程序。两年后，它的继任者 [AlphaZero](https://deepmind.com/blog/article/alphazero-shedding-new-light-grand-games-chess-shogi-and-go) 从零开始学会了掌握围棋、国际象棋和将棋。如今，在[发表于《自然》（Nature）杂志的一篇论文](https://rdcu.be/ccErB)中，我们介绍了 MuZero——朝着通用算法目标迈出的重要一步。MuZero 无需被告知规则即可掌握围棋、国际象棋、将棋和 Atari，这得益于它在未知环境中规划制胜策略的能力。

多年来，研究者一直在寻找这样的方法：既能学习一个解释环境的模型，又能利用该模型规划最佳行动方案。迄今为止，大多数方法都难以在 Atari 这类规则或动力学通常未知且复杂的领域中有效规划。

MuZero 最初在[2019 年的一篇初步论文](https://deepmind.com/research/publications/Mastering-Atari-Go-Chess-and-Shogi-by-Planning-with-a-Learned-Model)中提出，它通过学习一个只关注环境中对规划最重要的方面的模型来解决这个问题。通过将这一模型与 AlphaZero 强大的前瞻树搜索相结合，MuZero 在 Atari 基准上创造了新的最先进结果，同时在围棋、国际象棋和将棋这些经典规划挑战中达到了与 AlphaZero 相当的性能。以此，MuZero 展示了强化学习算法能力的一次重大飞跃。

![对比图：展示 DeepMind 算法从 AlphaGo 到 MuZero 的演进。随着算法的推进，其掌握的领域数量从仅围棋增加到围棋、国际象棋、将棋和 Atari，而所需的先验知识则从人类数据、领域知识和已知规则逐渐减少，到 MuZero 时这些输入一概不再需要。](https://lh3.googleusercontent.com/Gy24iLqDpKl4TyH4BcMCFNOkiDlMRg6PbclXrOqhp6stgd8dQZHTabSqonlYa5UOZcv0EcGPhVS0DQK5ZEkFNHkJUom24m1__jIlRvXqkmaTCUOb=w1440)

## 泛化到未知模型

规划能力是人类智能的重要组成部分，它让我们能够解决问题并对未来做出决策。例如，如果看到乌云密布，我们可能会预测即将下雨，并在出门前决定带上雨伞。人类能快速学会这种能力，并将其泛化到新的情境中——这也是我们希望算法具备的特质。

研究者曾尝试用两种主要方法来攻克 AI 领域的这一重大挑战：前瞻搜索或基于模型的规划。

使用前瞻搜索的系统（例如 AlphaZero）已经在跳棋、国际象棋和扑克等经典博弈中取得了显著成功，但它们依赖于被告知环境动力学的知识，例如游戏规则或精确的模拟器。这使得它们难以应用于混乱的现实世界问题——这类问题通常复杂且难以提炼成简单规则。

基于模型的系统旨在解决这一问题：先学习一个环境动力学的精确模型，再用它进行规划。然而，对环境各个方面建模的复杂性意味着这些算法无法在 Atari 这类视觉丰富的领域中竞争。迄今为止，Atari 上的最好成绩来自无模型（model-free）系统，例如 [DQN](https://www.nature.com/articles/nature14236)、[R2D2](https://openreview.net/forum?id=r1lyTjAqYX) 和 [Agent57](https://arxiv.org/abs/2003.13350)。顾名思义，无模型算法不使用学习到的模型，而是直接估计下一步应采取的最佳动作。

MuZero 采用了一种不同的方法来克服以往方法的局限。它不去尝试对整个环境建模，而只对智能体决策过程重要的方面建模。毕竟，知道雨伞能让你保持干燥，比模拟空中雨滴的分布模式更有用。

具体而言，MuZero 对环境中对规划至关重要的三个要素进行建模：

- **价值（value）：** 当前局面有多好？
- **策略（policy）：** 采取哪个动作最好？
- **奖励（reward）：** 上一个动作效果如何？

这三者都通过深度神经网络学习得到，也正是 MuZero 理解采取某个动作后会发生什么并据此进行规划所需的全部信息。

![插图：展示如何利用蒙特卡洛树搜索配合 MuZero 神经网络进行规划。从游戏当前局面（动画顶部的围棋棋盘示意）出发，MuZero 使用表征函数（h）将观测映射为神经网络使用的嵌入（s0）。随后借助动力学函数（g）和预测函数（f），MuZero 可以考虑未来可能的动作序列（a），并选择最佳动作。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277f565ad61d23ae431c30_Fig202.gif)

插图：展示如何利用蒙特卡洛树搜索配合 MuZero 神经网络进行规划。从游戏当前局面（动画顶部的围棋棋盘示意）出发，MuZero 使用表征函数（h）将观测映射为神经网络使用的嵌入（s0）。随后借助动力学函数（g）和预测函数（f），MuZero 可以考虑未来可能的动作序列（a），并选择最佳动作。

![MuZero 使用它与环境交互时收集的经验来训练其神经网络。这些经验既包括来自环境的观测和奖励，也包括在决定最佳动作时所执行搜索的结果。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277f63a12b691d3d67ff4a_Fig203.gif)

MuZero 使用它与环境交互时收集的经验来训练其神经网络。这些经验既包括来自环境的观测和奖励，也包括在决定最佳动作时所执行搜索的结果。

![在训练过程中，模型沿着收集到的经验逐步展开，在每一步预测此前保存的信息：价值函数 v 预测观测奖励之和（u），策略估计（p）预测此前的搜索结果（π），奖励估计 r 预测最近一次观测到的奖励（u）。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62277f797f22435437106707_Fig204.gif)

在训练过程中，模型沿着收集到的经验逐步展开，在每一步预测此前保存的信息：价值函数 v 预测观测奖励之和（u），策略估计（p）预测此前的搜索结果（π），奖励估计 r 预测最近一次观测到的奖励（u）。

这一方法还带来另一个重要好处：MuZero 可以反复使用其学到的模型来改进规划，而不必从环境收集新数据。例如，在 Atari 套件的测试中，这一变体——被称为 MuZero Reanalyze——有 90% 的时间使用学到的模型来重新规划过往对局中本应采取的行动。

## MuZero 的表现

我们选择了四个不同的领域来测试 MuZero 的能力。围棋、国际象棋和将棋用于评估其在具有挑战性的规划问题上的表现，而 Atari 套件则作为视觉更复杂问题的基准。在所有情形下，MuZero 都为强化学习算法创造了新的最先进水平：在 Atari 套件上超越了所有先前算法，并在围棋、国际象棋和将棋上达到 AlphaZero 的超人表现。

![对比表：显示 MuZero 和 MuZero Reanalyse 在 Atari 游戏的中位数与平均分百分比上超越 Ape-X、R2D2、IMPALA、Rainbow、UNREAL 和 LASER 等先前强化学习算法，且使用的环境帧数更少。](https://lh3.googleusercontent.com/AswLdUjq0IW4v9UJBJePKFfLO92wZG9KAiZehkr6lSN620UKt-zDpdMpKRwOH2caQngbJiNyE3MPWvod32xxPByjYRrkQMOFZFwrCfPgDfi3DRWZoQ=w1440)

在每次训练使用 200M 或 20B 帧的情况下在 Atari 套件上的表现。MuZero 在两种设置下都创造了新的最先进水平。所有分数均以人类测试者的表现为基准（100%）进行归一化，每个设置中的最佳结果以粗体突出显示。

我们还更细致地测试了 MuZero 利用其学到的模型进行规划的能力。我们从围棋这一经典的精确规划挑战开始——在围棋中，一步之差可能就是胜负之分。为了验证「规划越多结果越好」这一直觉，我们测量了一个完全训练好的 MuZero 在每步获得更多规划时间时能变得多强（见下方左图）。结果表明，当每步规划时间从十分之一秒增加到 50 秒时，棋力提升了超过 1000 Elo（一种衡量棋手相对水平的指标）。这大致相当于一名强大的业余棋手与最强职业棋手之间的差距。

![两幅折线图：展示 MuZero 的表现。左图 (A) 显示随着每步搜索时间从 0.1 秒增加到 50 秒，棋力（Elo）提升超过 1000，学习模型与真实模拟器的曲线相似。右图 (D) 显示在 Ms. Pac-Man 上数百万训练步中的棋力变化，随着每步模拟次数从 5 增加到 50，性能提升更快、达到更高水平。](https://lh3.googleusercontent.com/BDp81lIpTe9oiPsPi3BGoP8fngCD7r8f8ETxB7vBm0BGGWg2F6D6v0et_t6STiVfXn5B8F8_sm2ic395zw8qrW1YwQlRpybkTZEnog4wRVZTJikjwo0=w1440)

左：随着每步可用规划时间的增加，围棋棋力显著提升。注意 MuZero 的扩展曲线与拥有完美模拟器的 AlphaZero 几乎完美吻合。右：Atari 游戏 Ms Pac-Man 中的得分在训练期间同样随每步规划量的增加而提升。每条曲线对应一次不同的训练运行，其中允许 MuZero 考虑的每步模拟次数各不相同。

为了检验规划是否也在整个训练过程中带来好处，我们在 Atari 游戏 Ms Pac-Man（见上方右图）上使用多个独立训练的 MuZero 实例进行了一组实验。每个实例被允许在每步考虑不同数量的规划模拟，从 5 到 50 不等。结果证实，增加每步的规划量能让 MuZero 学得更快，同时取得更好的最终性能。

有趣的是，当 MuZero 每步只被允许考虑六或七次模拟——这个数量不足以覆盖 Ms Pac-Man 中所有可用动作——它仍然取得了不错的表现。这表明 MuZero 能够在动作与情境之间进行泛化，并不需要穷尽搜索所有可能性就能有效学习。

## 新的视野

MuZero 既学习环境模型又成功利用该模型进行规划的能力，展示了强化学习以及通用算法追求上的一次重大进步。它的前身 AlphaZero 已经被应用于[化学](https://www.nature.com/articles/nature25978?proof=t)、[量子物理](https://www.nature.com/articles/s41534-019-0241-0)等领域的一系列复杂问题。MuZero 强大学习与规划算法背后的思想，或许能为应对机器人技术、工业系统以及其他「游戏规则」未知的混乱现实环境中的新挑战铺平道路。

**相关链接：**

- MuZero：[Nature 论文](https://rdcu.be/ccErB)
- MuZero 演讲：[NeurIPS](https://www.youtube.com/watch?v=vt5jOSy7cz8&t=2s)（9 分钟，2019 年 12 月）、[ICAPS](https://www.youtube.com/watch?v=L0A86LmH7Yw)（30 分钟，2020 年 10 月）
- MuZero：[预印本](https://arxiv.org/abs/1911.08265) | [NeurIPS 2019 海报](https://storage.googleapis.com/deepmind-media/research/muzero_poster_neurips_2019.pdf)
- AlphaGo：[博客](https://ai.googleblog.com/2016/01/alphago-mastering-ancient-game-of-go.html) | [论文](https://www.nature.com/articles/nature16961)

**注释**

设计：Adam Cain、Jim Kynvin 和 Aleksandrs Polozuns
