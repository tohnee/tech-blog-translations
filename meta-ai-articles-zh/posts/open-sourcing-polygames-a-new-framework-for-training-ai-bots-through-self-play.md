---
title: "开源 Polygames：通过自博弈训练 AI 机器人的新框架"
title_en: "Open-sourcing Polygames, a new framework for training AI bots through self-play"
date: 2019-03-15
source: https://ai.facebook.com/blog/open-sourcing-polygames-a-new-framework-for-training-ai-bots-through-self-play
crawled: 2026-09-22
translated: 2026-09-22
---

# 开源 Polygames：通过自博弈训练 AI 机器人的新框架

> 原文：[Open-sourcing Polygames, a new framework for training AI bots through self-play](https://ai.facebook.com/blog/open-sourcing-polygames-a-new-framework-for-training-ai-bots-through-self-play) · Meta AI（Wayback 存档）

**它是什么：**Polygames 是一个新的开源 AI 研究框架，用于训练智能体通过自博弈（self-play）掌握策略游戏，而不是通过研读大量成功对局的示例。由于比以往框架更灵活、特性更丰富，Polygames 可以帮助研究人员推进并基准测试广泛的零学习（zero learning，ZL）技术——这类技术不需要训练数据集。Polygames 的架构使其兼容比以往系统（如 AlphaZero 和 ELF OpenGo）更多种类的游戏，包括 Breakthrough、Hex、Havannah、Minishogi、Connect6、扫雷（Minesweeper）、Mastermind、EinStein würfelt nicht!、Nogo 和黑白棋（Othello）。除了在各种游戏中构建和评估 ZL 方法之外，Polygames 还允许研究人员研究迁移学习，即在一个游戏上训练的模型应用于其他游戏并取得成功的能力。Polygames 提供了一个内置游戏库，以及一个单文件 API 来实现你自己的游戏。我们在多项游戏竞赛中以强劲的模型表现证明了 Polygames 作为训练工具的有效性，其中包括训练出首个在 19x19 Hex 中击败顶级人类棋手的机器人。除了分享我们构建 Polygames 的方法，我们还开源了完整框架，可在 GitHub 上获取。

**它做了什么：**大多数 AI 系统通过在精心整理的历史成功示例数据集上训练来掌握任务——例如处理导致各种棋类获胜对局的着法——而 ZL 技术则迫使系统在没有大量任务特定示例的情况下学习。与自监督学习方法类似，ZL 在长期有望降低对资源密集型训练数据集的需求。Polygames 在几个重要方面超越了此前类似的框架：

- 模型能够考虑给定动作空间的空间结构，从而更快地学会相关任务，因为它们使用全卷积网络——所有层都是卷积层。这有别于大多数基于游戏的架构（后者还会使用全连接层）。这种结构还使模型可以在一种棋盘尺寸上训练，随后在更大和更小的棋盘上也有良好表现。
- 在我们的锦标赛模式中，我们保留一组此前表现良好的模型，以降低灾难性遗忘（也称红皇后效应）的概率——即系统忘记如何战胜自身的早期版本。
- 由于 Polygames 的模型是渐进式的（框架自带用于增加新层与新通道或加大核宽度的脚本），它们能够进行热启动训练，让神经网络在训练过程中生长。这种神经可塑性加快了整体训练过程。
- Polygames 支持比类似框架更广泛的游戏，包括单人游戏（如扫雷和 Mastermind）以及随机性游戏（如 EinStein würfelt nicht!）。

**为什么重要：**Polygames 灵活的架构提升了此前 ZL 技术的速度与通用性，包括模型泛化到更多任务和环境的能力。例如，一个在「使用骰子且能完整看到对方棋子」的游戏上训练的模型，可以在扫雷上表现出色——后者没有骰子、只有一名玩家，且依赖部分可观测的棋盘。我们用 Polygames 训练的模型还在多项游戏竞赛和单场对局中取得了获胜结果，包括在台湾 TAAI 2019 的 Breakthrough、Connect6 和 10x10 黑白棋项目中夺得金牌，以及在 Hex 中击败顶级人类棋手。那场 Hex 胜利是机器人的首次，展示了我们框架的通用性：该模型是在 13x13 棋盘版本的游戏上训练的，却能在更大的 19x19 棋盘上取胜。Polygames 的表现显示出 ZL 用于现实应用的长期潜力。例如，我们已用该框架攻克与哥隆尺（Golomb ruler）相关的数学问题——哥隆尺用于优化电力变压器和无线电天线的定位。凭借其开放的设计和对更多游戏的兼容性，我们期待看到其他研究人员如何用 Polygames 推进以游戏评估的 ZL 技术的最先进水平。

**GitHub 获取地址：**

- 论文：Polygames: Improved zero learning
- GitHub：https://github.com/facebookincubator/polygames

这项研究是大规模合作的成果，参与者包括 Facebook AI 的研究人员；巴黎多芬纳大学的 Tristan Cazenave；台湾师范大学的 Yen-Chi Chen；东华大学的 Chen-Ling Li、Guan-Wei Chen、Hsin-I Lin、Maria Elsa、Shi-Cheng Ye、Shi-Jim Yen、Shi-Yu Chen、Xian-Dong Chiu、Yi-Jun Ye 和 Yu-Jin Lin；以及滨海科塔尔大学（Université du Littoral Côte d'Opale）的 Julien Dehos 和 Fabien Teytaud。
