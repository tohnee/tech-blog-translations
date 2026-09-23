---
title: "阅读以战怪兽：用强化学习教智能体泛化到新环境"
title_en: "Read to Fight Monsters: Using RL to teach agents to generalize to new settings"
date: 2019-03-15
source: https://ai.facebook.com/blog/read-to-fight-monsters-using-rl-to-teach-agents-to-generalize-to-new-settings
crawled: 2026-09-22
translated: 2026-09-22
---

# 阅读以战怪兽：用强化学习教智能体泛化到新环境

> 原文：[Read to Fight Monsters: Using RL to teach agents to generalize to new settings](https://ai.facebook.com/blog/read-to-fight-monsters-using-rl-to-teach-agents-to-generalize-to-new-settings) · Meta AI（Wayback 存档）

**研究内容：** 一个名为 Read to Fight Monsters（RTFM，「阅读以战怪兽」）的接地（grounded）强化学习问题：智能体必须对语言描述的目标、文档中描述的环境动态以及环境观测进行联合推理。此外，我们提出了一种名为 txt2π 的强化学习方法来建模这种三方交互。在用 txt2π 求解 RTFM 时，智能体学会了需要多个步骤、涉及推理与共指消解（coreference）的复杂任务——表现优于 FiLM 等最先进方法。而且，由于要求智能体阅读，txt2π 使其能够泛化到训练中未见过的动态环境中。

**工作原理：** 为了研究通过阅读实现泛化，我们把 RTFM 设置为一个游戏式场景：智能体必须利用一份解释环境动态的文本文档以及自身的环境观测来达成给定目标。我们以程序化方式生成大量独特的环境动态（包括物品列表，如有毒的怪物和受祝福的物品）、配套的文本描述（例如「受祝福的物品对有毒怪物有效」）以及目标（例如「击败森林教团」）。这些环境动态和相应的语言描述在每一回合（episode）都必须不同，这样智能体就无法记住有限的一组动态，而必须通过阅读进行系统化泛化。让智能体接触到组合爆炸级的大量动态，要求它交叉参照文档内和观测中的相关信息来塑造策略、达成目标。我们提出的 txt2π 方法由双向逐特征学习调制层组成，构建环境、目标和文本文档的相互依赖表示。与以往方法不同，txt2π 每一层中的注意力允许在推理过程的每个阶段选择性地阅读文档。在测试中，用这一方法训练的智能体展现出复杂行为，例如在获取正确物品后与正确的敌人交战，或避开不正确的敌人。

图中展示了一个训练好的策略在一个随机采样环境中的关键快照。第 1 帧是初始世界。第 4 帧中，智能体接近「狂热之剑」，它能击败目标「火焰哥布林」。第 5 帧中，智能体取得该剑。第 10 帧中，智能体在追逐目标的同时躲开干扰物「毒蝙蝠」。第 11 帧中，智能体与目标交战并将其击败，从而赢得该回合。精灵图（sprites）仅用于可视化——智能体观察到的单元内容是文本形式（以白色显示）。

**为什么重要：** 这项工作表明，通过阅读进行的语言理解是学习可泛化到新环境的策略的一条有希望的途径。尽管 txt2π 在 RTFM 上优于 FiLM 等最先进方法，我们最好的模型仍落后于人类玩家的表现。我们知道，在复杂的 RTFM 问题上，接地策略学习仍有很大改进空间。展望未来，我们有兴趣探索如何利用外部文档中的支持性证据来对计划进行推理并诱导分层策略。

阅读完整论文：RTFM: Generalising to Novel Environment Dynamics via Reading（RTFM：通过阅读泛化到新环境动态）
