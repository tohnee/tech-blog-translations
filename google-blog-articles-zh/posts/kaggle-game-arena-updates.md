---
title: "用 Game Arena 推进 AI 基准测试"
title_en: "Advancing AI benchmarking with Game Arena"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/kaggle-game-arena-updates/
site: google-blog
date: 2026-02-02
crawled: 2026-09-13
translated: 2026-09-13
---

# 用 Game Arena 推进 AI 基准测试

> 原文：[Advancing AI benchmarking with Game Arena](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/kaggle-game-arena-updates/) · Google

国际象棋是完全信息博弈。真实世界不是。

去年，Google DeepMind 与 Kaggle 合作推出 [Game Arena](https://blog.google/innovation-and-ai/products/kaggle-game-arena/)，一个独立的公开基准测试平台，AI 模型在其中进行策略游戏对决。我们从国际象棋开始，以衡量推理和策略规划能力。但在真实世界中，决策很少基于完整的信息。正因如此，我们现在为 Kaggle Game Arena 扩展两个新的游戏基准，在社交推理（social deduction）和风险计算方面测试前沿模型。

游戏一直是 Google DeepMind 历史的核心部分，它提供了一个客观的试金石，难度随竞争水平而提升。随着 AI 系统变得更加通用，掌握多样化的游戏展示了它们在不同认知技能上的熟练程度。除了衡量表现之外，游戏还可以作为受控的沙盒环境来评估智能体安全（agentic safety），为了解模型在真实世界部署时将遇到的复杂环境中的行为提供洞见。

## 国际象棋：超越计算的推理

我们去年发布了国际象棋基准，通过让模型两两对决，评估它们的策略推理、动态适应和长期规划能力。为追踪这些模型能力的演进，我们更新了[排行榜](https://www.kaggle.com/benchmarks/kaggle/chess)，纳入了最新一代模型。

虽然 Stockfish 等传统国际象棋引擎扮演着专用超级计算器的角色，每秒评估数百万个局面以找到最优着法，但大语言模型并不是通过暴力计算来下棋的。相反，它们依靠模式识别和「直觉」来大幅缩小搜索空间——这种方式与人类棋手下棋的方式相似。

Gemini 3 Pro 和 Gemini 3 Flash 目前在排行榜上拥有最高的 Elo 等级分。模型的内部「思考」显示了基于熟悉的国际象棋概念（如棋子机动性、兵结构和王的安全）的策略推理。相比 Gemini 2.5 一代，这一显著的性能提升凸显了模型进步的快速节奏，也证明了 Game Arena 在长期追踪这些改进方面的价值。

![Kaggle Game Arena 国际象棋排行榜，评估不同的 AI 模型，「Gemini 3 Pro Preview」位列第一名](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Chess_Leaderboard.width-1200.format-webp.webp)

## Werewolf：社交推理的博弈

超越国际象棋的透明逻辑，我们正在用 [Werewolf](https://www.kaggle.com/benchmarks/kaggle/werewolf)（狼人杀）扩展 Kaggle Game Arena。这款社交推理游戏是我们的第一款完全通过自然语言进行的团队游戏，要求模型在对话中驾驭不完整的信息。在这场社交推理挑战中，「村民」团队必须协同区分真相与欺骗，找出隐藏的「狼人」才能获胜。

这一基准有助于评估下一代 AI 助手所需的「软技能」。游戏测试沟通、谈判以及在模糊性中导航的能力——这些正是智能体在企业环境中与人类及其他智能体有效协作所需的能力。

Werewolf 也是智能体安全研究的安全环境。要获胜需要扮演双方——寻求真相者（村民）和欺骗者（狼人）。这让我们能够测试模型识别他人操纵行为的能力，同时以红队测试（red teaming）的方式检验模型自身的欺骗能力，而无需承担真实世界部署的风险。这项研究对于构建能够充当对抗恶意行为者可靠防线的 AI 智能体而言至关重要。

Gemini 3 Pro 和 Gemini 3 Flash 目前占据[排行榜](https://www.kaggle.com/benchmarks/kaggle/werewolf)前两名。它们展示了跨多个游戏回合有效推理其他玩家言行的能力——例如，识别某位玩家的公开声明与其投票模式之间的不一致——并利用这些洞见与队友建立共识。

想深入了解我们如何衡量模型在 Werewolf 中的技能，请前往 [Kaggle 博客](https://www.kaggle.com/blog/game-arena-werewolf)。

![排行榜显示「Game Arena Werewolf Leaderboard」，包含排名、模型、均衡等级分（Equilibrium Rating）和每局平均推理成本等列，评估日期为 2026 年 1 月 22 日](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Werewolf_Leaderboard.width-1200.format-webp.webp)

## 扑克：计算风险的挑战

国际象棋依靠推理。Werewolf 依靠社交推理。扑克引入了新的维度：风险管理。与 Werewolf 一样，扑克是不完全信息博弈。但在这里，挑战不在于建立联盟——而在于量化不确定性。模型必须通过推断对手的手牌并适应他们的打法风格来克服发牌的运气，从而确定最佳行动。

为了测试这些技能，我们正在推出新的扑克基准，并举办一场 AI 扑克锦标赛，顶级模型将在单挑无限注德州扑克（Heads-Up No-Limit Texas Hold'em）中一决高下。最终扑克排行榜将于 2 月 4 日星期三在 [kaggle.com/game-arena](https://www.kaggle.com/game-arena) 揭晓，届时锦标赛决赛已落幕。

想了解我们如何评估模型在扑克中的能力，请查看 [Kaggle 博客](https://www.kaggle.com/blog/game-arena-poker)。

## 观看精彩对决

为纪念这些全新和更新基准的发布，我们与国际象棋特级大师 Hikaru Nakamura 以及扑克传奇人物 Nick Schulman、Doug Polk 和 Liv Boeree 合作，制作三场直播活动，为全部三个基准提供专家解说和分析。

请在太平洋时间每天上午 9:30 收看三场直播，网址为 [kaggle.com/game-arena](https://www.kaggle.com/game-arena)：

- **2 月 2 日星期一**：扑克排行榜前八的模型在 AI 扑克之战中正面交锋。
- **2 月 3 日星期二**：在扑克锦标赛半决赛进行的同时，我们还将呈现 Werewolf 和国际象棋排行榜的精彩对局。
- **2 月 4 日星期三**：最后两个模型争夺扑克桂冠，完整排行榜同步发布。我们以国际象棋排行榜前两名模型——Gemini 3 Pro 和 Gemini 3 Flash——之间的对局收官，并直播最佳 Werewolf 模型的游戏集锦。

## 探索竞技场

无论是寻找一步创造性的将杀、在 Werewolf 中谈判休战，还是在扑克桌上全押，Kaggle Game Arena 都是我们检验这些模型真正实力的地方。

前往 [kaggle.com/game-arena](http://kaggle.com/game-arena) 一探究竟。
