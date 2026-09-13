---
title: "DeepMind 与暴雪将把 StarCraft II 作为 AI 研究环境开放"
title_en: "DeepMind and Blizzard to release StarCraft II as an AI research environment"
source: https://deepmind.google/blog/deepmind-and-blizzard-to-release-starcraft-ii-as-an-ai-research-environment/
site: deepmind
date: 2016-11-04
crawled: 2026-09-13
translated: 2026-09-13
---

# DeepMind 与暴雪将把 StarCraft II 作为 AI 研究环境开放

> 原文：[DeepMind and Blizzard to release StarCraft II as an AI research environment](https://deepmind.google/blog/deepmind-and-blizzard-to-release-starcraft-ii-as-an-ai-research-environment/) · Google DeepMind

今天，在加利福尼亚州阿纳海姆举行的 BlizzCon 2016 上，我们宣布与[暴雪娱乐](https://www.blizzard.com/en-us/)（Blizzard Entertainment）合作，把 StarCraft II 开放给全世界的 AI 与机器学习研究者。

近 20 年来，StarCraft 游戏系列被广泛公认为 1v1 竞技电子游戏的巅峰，也是史上最优秀的 PC 游戏之一。初代 StarCraft 是电子竞技的早期先驱，自 90 年代末以来一直由顶尖职业选手在最高水准上竞技，至今仍竞争激烈。StarCraft 系列在竞技游戏中的长盛不衰，印证了暴雪的设计功力，以及他们多年来持续平衡与打磨游戏的努力。StarCraft II 延续了这一系列享誉盛名的电子竞技传统，也正是我们与暴雪合作的重点。

DeepMind 肩负着推动 AI 边界的科学使命，致力于开发无需被告知方法就能学会解决任何复杂问题的程序。游戏正是做这件事的完美环境：它让我们能够快速高效地开发并测试更聪明、更灵活的 AI 算法，还能通过分数即时反馈我们的进展。

过去五年里，我们帮助开创了把游戏用作 AI 研究环境、以推动机器学习与强化学习研究的做法：从 [Atari 上的 2D 游戏](https://www.youtube.com/watch?v=W2CAghUiofY)，到 [Torcs](http://torcs.sourceforge.net/) 等完整 3D 环境，再到[掌握围棋](https://deepmind.com/research/case-studies/alphago-the-story-so-far)，以及即将推出的 DeepMind Labyrinth。下面的图示从左到右展示了 Atari 与 Labyrinth 这两个研究环境的样子。

![截图对比 DeepMind 的 AI 研究环境：左侧是 Atari 上的《太空侵略者》，右侧是 DeepMind Labyrinth 的四幅 3D 透视图。](https://lh3.googleusercontent.com/Al7n8__CFRyEhI7QBkrrZlWPPkl736uKQpsT373ppyzZtp2EQjRUGmWGTfcCA75OukReNKYLNoyG4N3NSOjmDR-eueV69ASLWTKid8KaU_LnBLvl=w1440)

StarCraft 对当前的 AI 研究而言是一个有趣的测试环境，因为它为通向真实世界的杂乱性提供了一座有用的桥梁。智能体要在这个环境中不断推进、把 StarCraft 打好所需的技能，最终可能迁移到现实世界的任务上。

在一局 StarCraft 开始时，玩家从三个种族中选择一个，每个种族都有独特的单位能力和玩法路线。玩家的行动受游戏内经济的支配：必须采集矿物和瓦斯才能建造新建筑、生产新单位。对手同时也在建设自己的基地，但每位玩家只能看到自己单位视野范围内的部分地图。因此，玩家必须派出单位侦察未见的区域来获取对手的情报，并在很长时间内记住这些信息。这使得挑战更加复杂，因为环境变成了部分可观测的——与围棋或国际象棋这类完全信息游戏形成了有趣的对比。而且这是一款即时战略游戏——双方玩家同时行动，所以每个决策都必须快速高效地计算出来。

一个能玩 StarCraft 的智能体需要展现对记忆的有效运用、长时段规划的能力，以及根据新信息调整规划的应变能力。计算机的控制速度可以极快，但那并不必然体现智能，所以智能体必须在与游戏交互时遵守人类手速的「每分钟操作数」（APM）限制。StarCraft 的高维动作空间与此前强化学习研究中考察的大不相同：要执行「把基地扩张到某个位置」这样简单的目标，也必须协调鼠标点击、镜头与可用资源。这使得动作与规划具有层次性，而这正是[强化学习](https://deepmind.com/blog/article/deep-reinforcement-learning)中极具挑战性的一个方面。

让我们尤为欣慰的是，我们与暴雪共同构建的这个环境，明年就将向所有研究者开放。我们认可近年来 Brood War 社区的开发者与研究者所做的努力，并希望这个由暴雪团队直接支持、新颖、现代而灵活的环境能得到广泛使用，推动最先进水平不断向前。

我们与 StarCraft II 团队紧密合作，开发了一个 API，它支持的功能与以往用「脚本化」接口编写的机器人程序类似，允许对单个单位进行程序化控制、访问完整游戏状态（还有一些新选项）。最终，智能体将直接从像素开始游戏；为了走向那一天，我们开发了一种新的基于图像的接口，输出简化的低分辨率 RGB 图像数据（针对地图与小地图），并可选择把特征拆分为独立的「图层」，例如地形高度场、单位类型、单位生命值等。下面是特征图层 API 将呈现的样子示例。

我们还在与暴雪合作创建「课程」式场景，逐步呈现越来越复杂的任务，让任何水平的研究者都能把智能体跑起来，并对不同算法和进展进行基准比较。研究者也将拥有充分的灵活性与控制权，可以使用现有的 StarCraft II 编辑工具创建自己的任务。

我们非常期待看到与暴雪的合作会把我们带向何方。虽然距离能在 StarCraft II 上挑战职业人类玩家还很遥远，但我们希望与暴雪共同完成的这项工作，能成为更广泛的 AI 研究社区一个有用的测试平台。
