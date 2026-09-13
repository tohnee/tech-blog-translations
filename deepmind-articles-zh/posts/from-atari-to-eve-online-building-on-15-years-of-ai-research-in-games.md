---
title: "从 Atari 到 EVE Online：建立在 15 年游戏 AI 研究之上"
title_en: "From Atari to EVE Online: Building on 15 Years of AI Research in Games"
source: https://deepmind.google/blog/from-atari-to-eve-online-building-on-15-years-of-ai-research-in-games/
site: deepmind
date: 2026-08-21
crawled: 2026-09-13
translated: 2026-09-13
---

# 从 Atari 到 EVE Online：建立在 15 年游戏 AI 研究之上

> 原文：[From Atari to EVE Online: Building on 15 Years of AI Research in Games](https://deepmind.google/blog/from-atari-to-eve-online-building-on-15-years-of-ai-research-in-games/) · Google DeepMind

从 Atari 到围棋再到《星际争霸》，游戏推动了 AI 领域一些最重大的突破。现在，我们正与游戏开发者合作，打造全新的游戏体验原型，同时推动游戏与 AI 两个领域的边界。

自 2010 年 DeepMind 成立以来，游戏这种受限而又丰富的世界在理解智能方面发挥了关键作用。它们推动了我们一些最重大的 AI 突破，从掌握 Atari 游戏到帮助攻克蛋白质结构预测——并且仍然是我们工作的核心。

游戏深植于 GDM 的基因。Google DeepMind 的创始人之一 Demis Hassabis（德米斯·哈萨比斯）本人就曾是游戏开发者，GDM 团队中的许多人也是如此。我们加起来拥有数十年的游戏开发一手经验，并对制作游戏这门手艺怀有深深的敬意。

我们一直很清楚，利用游戏开展 AI 研究需要与游戏开发者深度合作——比如我们今年早些时候公布的与 Fenris Creations 及 EVE 宇宙的[重大新研究合作](https://fenris.com/news/2026/studio-behind-eve-online-goes-independent-rebrands-as-fenris-creations-enters-research-partnership-with-google-deepmind)，以及我们与 [Hello Games](https://hellogames.org/)、[Coffee Stain Studios](https://coffeestain.com/)、[Foulball Hangover](https://www.foulballhangover.com/) 等知名工作室共同完成的工作。

## 游戏作为 AI 研究的引擎

我们的旅程始于一个小团队训练深度神经网络直接从原始像素学习玩 Atari 2600 游戏。深度 Q 网络（Deep Q-Network, DQN）学会了玩 49 种不同的游戏——从《Pong》到《Breakout》再到《Space Invaders》——而不需要任何针对特定游戏的工程设计。关于 DQN 的[这篇 2015 年 Nature 论文](https://www.nature.com/articles/nature14236)帮助催生了深度强化学习的现代时代。

从那时起，我们尝试掌握更复杂的游戏，每一个里程碑都产出能力更强、更通用的系统。[AlphaGo](https://deepmind.google/research/breakthroughs/alphago/) 在 2016 年击败了围棋世界冠军李世石（Lee Sae Dol）——这是许多专家曾认为还要十年才能实现的壮举。[AlphaGo Zero](https://www.nature.com/articles/nature24270) 完全通过自我博弈（self-play）学习，不使用任何人类数据，超越了之前所有版本。[AlphaZero](https://www.science.org/doi/10.1126/science.aar6404) 将这一方法泛化，用同一个算法掌握了国际象棋、将棋和围棋，而 [MuZero](https://www.nature.com/articles/s41586-020-03051-4) 甚至在不知道规则的情况下学会了玩游戏。2019 年，[AlphaStar](https://www.nature.com/articles/s41586-019-1724-z) 在《星际争霸 II》（*StarCraft II*）中达到了宗师（Grandmaster）水平，应对了实时复杂性和不完全信息。

对于每一款游戏，AI 都丰富了游戏体验。AlphaGo 著名的[第 37 手](https://deepmind.google/research/breakthroughs/alphago/)（Move 37）是一步如此出人意料的落子，以至于职业解说最初以为是一步失误——它颠覆了围棋数百年的定论，并激励专家探索新的策略。AlphaZero 同样在国际象棋中启发了全新的下法。至关重要的是，这种在游戏中取得成功的探索精神对其他 AI 系统产生了深远影响：[AlphaFold](https://deepmind.google/science/alphafold/) 将这些基础应用于帮助攻克蛋白质结构预测这一延续 50 年的宏大挑战，这项突破获得了 2024 年诺贝尔化学奖。

## 从掌握游戏到理解游戏

我们早期的工作证明了，只要目标明确、训练充分，AI 就能掌握任何游戏。但现实世界并没有分数和规则手册——这促使我们提出一个根本不同的问题：AI 能否像人类一样理解并与任何游戏世界互动？

这就是 [SIMA](https://deepmind.google/blog/sima-generalist-ai-agent-for-3d-virtual-environments/)——我们的可扩展可指令多世界智能体（Scalable Instructable Multiworld Agent）——背后的挑战。SIMA 不是为高分而优化，而是一个通用智能体：它「看到」玩家在屏幕上看到的画面，理解自然语言指令，并通过普通的键盘和鼠标操作来行动——不需要任何 API 或源代码访问权限。

在 Gemini——我们的前沿 AI 模型——的加持下，[SIMA 2](https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/) 能够作为具备实时推理和对话能力的互动伙伴。它在复杂的 3D 研究环境和视频游戏（包括《无人深空》（*No Man's Sky*）、《Valheim》、《Hydroneer》等）中实现了类人类的游玩水平。

对游戏开发者而言，一个真正通用的游戏智能体将解锁无需修改游戏代码即可作用于现有游戏的 AI 能力。这可以驱动全新的游戏玩法，从真正理解游戏世界的 AI 伙伴，到能以脚本系统永远无法做到的方式适应和回应的非玩家角色（NPC）。

通用游戏智能体还可以变革游戏的制作方式。在开发过程中，游戏随每一次提交（commit）而变化，这类智能体可以实现真正稳健的 QA 测试。在上线后，当新内容引入或玩家行为不可预测时，它们可以实时适应——泛化到新情况而无需重新编写脚本。

为了安全、负责任地开发 SIMA 智能体，我们与知名游戏工作室合作，并正在建立一个不断增长的游戏研究组合。这使我们能够用越来越复杂的任务挑战我们的智能体，这些任务有朝一日或许能迁移到解决现实世界的问题上。

## 与游戏开发者携手，探索 AI 与游戏研究的新前沿

游戏工作室带来专业的技艺、非凡的游戏世界，以及对玩家的深刻理解。我们带来前沿 AI——从 Gemini 到生成式交互环境和具身智能体研究——研究专长，以及我们团队独特的游戏开发背景和在交互环境中构建 AI 的多年经验。我们共同专注于发现突破性体验——没有 AI 就不可能实现的、前所未有的游戏玩法。

重要的不是技术，而是有趣的体验。因此我们与合作伙伴采取「做出来看，而不是说出来」的方式。我们的团队与游戏开发者并肩工作，探索新想法、构建可玩的原型来寻找乐趣。

我们与 EVE 宇宙背后独立工作室 [Fenris Creations](https://www.fenris.com/) 的最新研究合作，代表了我们游戏 AI 研究历史的新篇章。

Fenris Creations 用二十多年时间打造了游戏界最非凡的持久世界之一。于 2003 年上线的《EVE Online》是一款大型多人太空模拟游戏，数千名玩家共享一个已连续演化超过 20 年的单一宇宙。其玩家驱动的经济体系具有真实的供需动态和横跨数千个星系的贸易网络。它的版图——由联盟、冲突和外交塑造——由人类互动驱动。

对 AI 研究而言，这是一个黄金机遇。这是一个活着的、不断演化的世界，它所要求的能力恰恰是我们认为对前沿 AI 至关重要的：

- **持续学习**：在一个不断变化的世界中，习得新技能而不遗忘已有知识。
- **记忆**：在远超当今模型上下文窗口的时间尺度上积累和检索知识。
- **长时程规划**：在数周、数月甚至数年的尺度上进行推理。
- **复杂的多智能体动态**：在大规模上应对合作、竞争、谈判、经济和涌现的社会行为。

这些挑战处于我们更广泛的研究计划的核心，即创建能够持续从经验中学习、且学习速度随时间加快的系统。我们相信这些前沿能力未来可以解锁新的游戏体验。

> 《EVE Online》从第一天起就被设想为一个由玩家塑造、具有持久后果的沙盒。数十年来，这为玩家和员工带来了无数关于人类成长的故事。与 Google DeepMind 一起，我们正迈向一片未知领域：AI 必须在没有任何其他游戏环境所要求的时间尺度上学习、适应和记忆，同时帮助我们理解人类与 AI 如何在虚拟环境中共存——在我们必须在现实生活中面对同样的问题之前。

Hilmar Pétursson

Fenris Creations 首席执行官

我们的研究合作横跨 Fenris Creations 不断扩展的宇宙，为 AI 开发提供各具特色的环境。《EVE Online》提供大规模单服持久宇宙，而《EVE Vanguard》则以第一人称视角游玩，为这个更广阔的持久世界带来贴近地面、快节奏的战术决策。这创造了研究智能体在多个抽象层级上运作的机会——从即时反应层面的战术到横跨星系的战略。

此外，《EVE Frontier》凭借其可编程的「Smart Assemblies」和开放、可扩展的架构，提供了一个开放式的环境——世界规则本身都可以改变——要求智能体适应全新的游戏机制。

![一群人围在一块显示游戏演示的大屏幕附近，一边交谈一边用笔记本电脑工作。](https://lh3.googleusercontent.com/acoFLxTvy-DIhcRG0Kedf8ZDpwBzIo5Hcxf_Pxj9PeWxaCMHUkiCPjKPcTDX4dgQavjV6o6x9kX79Jhor6CBX3XNY7S4xnzga4Ft73lLw0Zj0zwq0AY=w1440-h810-n-nu)

在 Google DeepMind 与 Fenris Creations 的一次工作坊中进行的「做出来看，而不是说出来」环节，我们的团队分享可玩原型与反馈，并讨论新游戏体验的想法

我们的合作已经带来了真实的玩家价值：[Aura Guidance](https://www.eveonline.com/news/view/eve-evolved-aura-guidance) 系统利用 Gemini 传递玩家生成的知识——基于真实的新手求助问答——来帮助新飞行员。

我们更长线的研究计划从《EVE Online》的离线实例开始，这是一个与在线玩家隔离的安全沙盒。随后推进到 EVE Frontier，将其作为研究人类与智能体如何在持久、开放的世界中共存的空间。只有在能力成熟之后，我们才会考虑将其引入《EVE Online》和《EVE Vanguard》，目标是丰富人类的游玩体验。

## 前方的路

游戏一直是智能的一面镜子。随着游戏变得更复杂、更持久、更开放，我们为驾驭它们而构建的 AI 系统也是如此。

我们追求的始终是同一个终极目标：AI 作为催化剂，而非替代品。我们的长期愿景是解锁突破性的游戏体验，让游戏更易上手、更个性化，并且——正如我们从 AlphaGo 到 AlphaFold 所看到的——把在游戏中学到的东西应用于现实世界的问题，推动科学发现。

我们感谢这段旅程中所有的游戏合作伙伴，也感谢 Fenris Creations 加入我们开启下一个篇章。我们迫不及待想分享我们的发现。

[了解更多关于 SIMA 2](https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/)[了解我们与 Fenris Creations 的合作](https://fenris.com/news/2026/studio-behind-eve-online-goes-independent-rebrands-as-fenris-creations-enters-research-partnership-with-google-deepmind)

## 致谢

我们要感谢 Google DeepMind 中多年来为在游戏中安全、负责任地推进 AI 研究做出贡献的众多团队。

特别感谢与我们合作的所有游戏开发者：Coffee Stain（*Valheim、Satisfactory、Goat Simulator 3*）、Fenris Creations（EVE Online、EVE Vanguard、EVE Frontier）、Foulball Hangover（*Hydroneer*）、Hello Games（*No Man's Sky*）、Keen Software House（*Space Engineers*）、RubberbandGames（*Wobbly Life*）、Strange Loop Games（*Eco*）、Thunderful Games（*ASKA、The Gunk、Steamworld Build*）、Digixart（*Road 96*），以及 Tuxedo Labs 与 Saber Interactive（*Teardown*）。
