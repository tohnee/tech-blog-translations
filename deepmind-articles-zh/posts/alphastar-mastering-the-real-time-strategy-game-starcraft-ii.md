---
title: "AlphaStar：掌握即时战略游戏《星际争霸 II》"
title_en: "AlphaStar: Mastering the real-time strategy game StarCraft II"
source: https://deepmind.google/blog/alphastar-mastering-the-real-time-strategy-game-starcraft-ii/
site: deepmind
date: 2019-01-24
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaStar：掌握即时战略游戏《星际争霸 II》

> 原文：[AlphaStar: Mastering the real-time strategy game StarCraft II](https://deepmind.google/blog/alphastar-mastering-the-real-time-strategy-game-starcraft-ii/) · Google DeepMind

几十年来，游戏一直被用作测试和评估人工智能系统性能的重要方式。随着系统能力的提升，研究界不断寻求复杂度更高、能够涵盖解决科学问题和现实问题所需的各种智能要素的游戏。近年来，《星际争霸》（StarCraft）被公认为最具挑战性的即时战略游戏（RTS）之一，也是有史以来历史最悠久的电子竞技项目之一，它已成为业界公认的 AI 研究「重大挑战」。

现在，我们介绍我们的[《星际争霸 II》](https://starcraft2.com/en-us/)项目 AlphaStar——第一个击败顶级职业选手的人工智能。在 12 月 19 日举行的一系列测试赛中，AlphaStar 以 5:0 干净利落地击败了 [Team Liquid 战队](https://www.teamliquid.com/)的 Grzegorz "[MaNa](https://liquipedia.net/starcraft2/MaNa)" Komincz——[世界上最强的职业《星际争霸》选手之一](https://liquipedia.net/starcraft2/2018_StarCraft_II_World_Championship_Series_Circuit/Standings)；此前它还在一场基准测试赛中战胜了 MaNa 的队友 Dario "[TLO](https://liquipedia.net/starcraft2/TLO)" Wünsch。这些比赛在职业比赛条件下进行，使用竞技天梯[地图](https://liquipedia.net/starcraft2/Catalyst_LE)，且没有任何游戏规则限制。

尽管此前人工智能在 [Atari](https://deepmind.com/research/publications/playing-atari-deep-reinforcement-learning/)、[马里奥](https://www.youtube.com/watch?v=qv6UVOQ0F44&feature=youtu.be&a=)、[《雷神之锤 III 竞技场》夺旗模式](https://deepmind.com/blog/article/capture-the-flag-science)和 [Dota 2](https://openai.com/blog/openai-five/) 等电子游戏中取得了重大成功，但迄今为止，AI 技术一直难以应对《星际争霸》的复杂性。最好的[成绩](https://www.researchgate.net/publication/329202945_StarCraft_AI_Competitions_Bots_and_Tournament_Manager_Software)都是通过手工构建系统的主要组件、对游戏规则施加重大限制、赋予系统超人类能力，或在简化的地图上进行对局来实现的。即便做了这些修改，也没有任何系统能够接近职业选手的水平。相比之下，AlphaStar 玩的是完整的《星际争霸 II》游戏，它使用一个深度神经网络，通过[监督学习](https://en.wikipedia.org/wiki/Supervised_learning)和[强化学习](https://en.wikipedia.org/wiki/Reinforcement_learning)直接从原始游戏数据中训练而来。

## 《星际争霸》的挑战

《星际争霸 II》由 [Blizzard Entertainment](https://www.blizzard.com/en-gb/) 开发，背景设定在一个虚构的科幻宇宙中，具有丰富、多层次的游戏玩法，旨在挑战人类的智力。它与初代作品一起，跻身史上规模最大、最成功的游戏之列，玩家们在电子竞技锦标赛中角逐已超过 20 年。

![AlphaStar 与 LiquidTLO 对局的《星际争霸 II》游戏内截图，显示星灵（Protoss）的建筑与部队正在采集资源，状态面板显示 AlphaStar 在人口、矿物资源和兵力规模上领先。](https://lh3.googleusercontent.com/OhYgzlmP3mc64So5U6U-nJSSzCHEtKamnG_xOue4ASgsCODCmEgCxSeZaTpH98CoCOFWL1N5hJSti427v6O2mvprDoqydGMcxcqNbIQ9ImCcrlKvAqg=w1440)

游戏有多种不同的玩法，但在电子竞技中最常见的是五局分胜负的 1v1 锦标赛。开局时，玩家必须选择操控三种外星「种族」之一——虫族（Zerg）、星灵（Protoss）或人族（Terran），它们都拥有独特的特性和能力（尽管职业选手往往专精一个种族）。每名玩家开局都拥有若干工人单位，它们采集基础资源以建造更多单位和建筑、研发新技术。这些又让玩家能够采集其他资源、建造更复杂的基地和建筑，并发展可用于智取对手的新能力。要取得胜利，玩家必须精心平衡对经济的大局管理——即「宏观操作」（macro）——与对个体单位的微观控制——即「微观操作」（micro）。

平衡短期与长期目标并适应意外情况的需要，对那些往往脆弱而缺乏灵活性的系统构成了巨大挑战。掌握这一问题需要在多个 AI 研究挑战上取得突破，包括：

- **博弈论：**《星际争霸》像石头剪刀布一样，不存在单一的最优策略。因此，AI 训练过程需要不断探索并拓展战略知识的前沿。
- **不完全信息：**与国际象棋或围棋等玩家能看到全部信息的游戏不同，《星际争霸》玩家的关键信息是隐藏的，必须通过「侦察」主动获取。
- **长期规划：**与许多现实问题一样，因果并非即时显现。一局游戏可能长达一个小时之久，这意味着游戏早期采取的行动可能在很长时间内都不会有回报。
- **实时性：**与传统棋盘游戏中玩家轮流行动不同，《星际争霸》玩家必须随着游戏时钟的推进持续执行操作。
- **巨大的动作空间：**数百种不同的单位和建筑必须实时地同时控制，形成一个组合式的可能性空间。除此之外，动作是分层的，可以被修改和扩展。我们对游戏的参数化在每个时间步平均有约 10 的 26 次方个合法动作。

由于这些巨大的挑战，《星际争霸》已成为 AI 研究的一项「重大挑战」。自 2009 年 BroodWar API 发布以来，《星际争霸》和《星际争霸 II》的持续赛事一直在评估研究进展，包括 [AIIDE StarCraft AI 竞赛](http://www.cs.mun.ca/~dchurchill/starcraftaicomp/history.shtml)、CIG StarCraft 竞赛、[学生《星际争霸》AI 锦标赛](https://sscaitournament.com/)和[《星际争霸 II》AI 天梯](https://sc2ai.net/)。为了帮助研究界进一步探索这些问题，[我们曾在 2016 年和 2017 年与 Blizzard 合作，发布了一套名为 PySC2 的开源工具](https://deepmind.com/blog/announcements/deepmind-and-blizzard-open-starcraft-ii-ai-research-environment)，其中包括有史以来发布的规模最大的匿名游戏回放集。我们现在在这一工作基础上，结合工程与算法方面的突破，打造出了 AlphaStar。

![动画信息图，展示 AlphaStar 在与 MaNa 的实时对局中的决策过程，包括实时游戏画面、神经网络激活、地图分析、结果预测和计划中的建造动作。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62271e2f604e640534eeca99_AlphaStar2003.gif)

AlphaStar 智能体在与 MaNa 对局第二局期间的可视化。这展示了从智能体视角看到的游戏：输入神经网络的原始观测数据、神经网络的内部激活、智能体可以考虑的部分动作（例如点击位置和建造内容），以及预测的对局结果。同时也展示了 MaNa 的游戏视角，尽管智能体无法访问这一信息。

## AlphaStar 如何训练

AlphaStar 的行为由一个深度[神经网络](https://en.wikipedia.org/wiki/Artificial_neural_network)生成，该网络接收来自原始游戏接口（一个单位列表及其属性）的输入数据，并输出构成游戏内一个动作的指令序列。更具体地说，神经网络架构对单位应用了一个 [transformer](https://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf) 主干（类似于[关系型深度强化学习](https://openreview.net/forum?id=HkxaFoC9KQ)），结合了[深度 LSTM 核心](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.676.4320&rep=rep1&type=pdf)、带[指针网络](https://papers.nips.cc/paper/5866-pointer-networks.pdf)的[自回归策略头](https://arxiv.org/abs/1708.04782)，以及一个[集中式价值基线](https://www.cs.ox.ac.uk/people/shimon.whiteson/pubs/foersteraaai18.pdf)。我们相信，这一先进模型将有助于机器学习研究中许多其他涉及长期序列建模和巨大输出空间的挑战，例如翻译、语言建模和视觉表示。

AlphaStar 还使用了一种新颖的多智能体学习算法。神经网络最初通过从 Blizzard [发布的匿名人类对局](https://github.com/Blizzard/s2client-proto/tree/master/samples/replay-api)进行监督学习来训练。这使 AlphaStar 能够通过模仿，学习《星际争霸》天梯玩家使用的基本微观和宏观策略。这个初始智能体在 95% 的对局中击败了内置的「精英」（Elite）级 AI——大致相当于人类的黄金级别玩家。

![展示 AlphaStar 联赛训练过程的示意图：人类数据作为起点，经过数百次迭代生成一个分支化的多智能体强化学习结构，最终产出一个用于对抗职业《星际争霸 II》选手的智能体纳什分布。](https://lh3.googleusercontent.com/5D7zdXHxQEMu3FdiVcUxb9005LarwHcSyEWRkWAFMmPWybLu9xAWA0c4amAEmsGwdbh1iLG23qAE-KOCg5BcmlhDPdFZUHWFYLrrNkeYpgnqqbPUUQ=w1440)

AlphaStar 联赛。智能体最初从人类游戏回放中训练，然后与联赛中的其他对手进行对抗训练。在每次迭代中，会从现有对手分支出新的对手，原始对手被冻结，并且可以调整匹配概率和决定每个智能体学习目标的超参数，在保持多样性的同时提高难度。智能体的参数通过与对手对局结果的强化学习来更新。最终的智能体从联赛的纳什分布中（不放回地）采样得到。

这些初始智能体随后被用来启动一个多智能体强化学习过程。我们创建了一个持续进行的联赛，联赛中的智能体——即对手（competitors）——相互对局，就像人类通过在[《星际争霸》天梯](https://starcraft2.com/en-us/ladder/grandmaster/1)上对战来体验这款游戏一样。新的对手通过从现有对手分支的方式被动态地加入联赛；然后每个智能体从与其他对手的对局中学习。这种新的训练形式将[基于种群](https://deepmind.com/blog/article/capture-the-flag-science)和[多智能体](https://arxiv.org/pdf/1711.00832.pdf)强化学习的思想进一步推进，创建了一个持续探索《星际争霸》对局巨大战略空间的过程，同时确保每个对手在面对最强策略时表现出色，并且不会忘记如何击败较早的策略。

![散点图，显示 AlphaStar 在 14 天强化学习期间的预估 MMR 评分。初始监督学习智能体集中在 3000 MMR 左右，而 AlphaStar 训练联赛中的智能体呈稳步上升轨迹。值得注意的里程碑包括：AlphaStar 在第 9 天左右以约 5500 MMR 击败职业选手 TLO（星灵），在第 14 天前后以近 7000 MMR 击败 MaNa，使最终智能体远超宗师（Grandmaster）段位。](https://lh3.googleusercontent.com/iTlSuHDyrlAdlx-xcMkRlyNbj-VtOJPLxTFBT1oEalgoQ3jIkocB6DIA4J6fVDkLWuRVn1IqFPy7gnwuRba3AULKEyyj23bL0BdyxxzzADw07x72=w1440)

AlphaStar 联赛中各对手在整个训练期间的匹配评分（MMR）估计值——这是对玩家水平的近似衡量——与 Blizzard 在线天梯段位的对比。

随着联赛的推进和新对手的产生，能够击败早期策略的新反制策略不断涌现。一些新对手执行的策略只是对先前策略的改进，而另一些则发现了截然不同的全新策略，包括全新的建造顺序、单位组合和微观操作方案。例如，在 AlphaStar 联赛早期，诸如用[光子炮](https://liquipedia.net/starcraft2/Photon_Cannon_(Legacy_of_the_Void))或[黑暗圣堂武士](https://liquipedia.net/starcraft2/Dark_Templar_(Legacy_of_the_Void))进行极快突袭之类的「速攻流」（cheesy）策略曾受到青睐。随着训练的推进，这些冒险的策略被舍弃，转而出现其他策略：例如通过用更多工人过度扩张基地来积累经济优势，或者牺牲两个[先知](https://liquipedia.net/starcraft2/Oracle_(Legacy_of_the_Void))来扰乱对手的工人和经济。这一过程与《星际争霸》发布多年来玩家发现新策略、并能够击败以往主流打法的方式十分相似。

![彩色面积图，显示 AlphaStar 联赛中纳什分布在 14 个训练日内的单位数量，展示了所生产的不同星灵单位（如追猎者、使徒、干扰者）的演化。](https://lh3.googleusercontent.com/pT5uBqzo7ezV8UjMh8HAQrk7Mq9tj6Wwp4TKGlz4yIit84-C5ClPTrcC9ut4l5j7pT6Pn_oEkAhH1RrLlDcAwOHSnyxYuTledaCb66B8MsV8vLR-=w1440)

随着训练的推进，孕育出 AlphaStar 的联赛改变了它所建造单位的配比。

为了鼓励联赛中的多样性，每个智能体都有自己的学习目标：例如，该智能体应该以击败哪些对手为目标，以及任何额外的内部动机，这些动机会影响智能体的打法偏好。一个智能体的目标可能是击败某个特定的对手，而另一个智能体可能需要击败一整批对手，并且要通过建造更多某种特定的游戏单位来做到这一点。这些学习目标在训练期间会不断调整。

每个智能体的神经网络权重通过与对手对局的强化学习来更新，以优化其个人学习目标。权重更新规则是一种高效且新颖的[离策略 actor-critic](https://arxiv.org/pdf/1802.01561.pdf) 强化学习算法，结合了[经验回放](https://link.springer.com/content/pdf/10.1023%2FA%3A1022628806385.pdf)、[自我模仿学习](http://proceedings.mlr.press/v80/oh18b/oh18b.pdf)和[策略蒸馏](https://arxiv.org/pdf/1511.06295.pdf)。

![动画散点图，显示「MaNa Agent 4」在训练过程中的策略探索，以及其游戏单位构成不断变化的柱状图。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/62271f231cd532f91c5d4663_AlphaStar2007.gif)

图中展示了最终被选中与 MaNa 对战的一个智能体（黑点）在训练过程中如何演化其策略和对手（彩色点）。每个点代表 AlphaStar 联赛中的一个对手。点的位置代表其策略（见插图），点的大小代表它在训练期间被选为 MaNa 智能体对手的频率。

为了训练 AlphaStar，我们构建了一个高度可扩展的分布式训练系统，使用[谷歌的 v3 TPU](https://cloud.google.com/tpu/)，支持一个由众多智能体组成的种群从数千个并行运行的《星际争霸 II》实例中学习。AlphaStar 联赛运行了 14 天，每个智能体使用 16 个 TPU。在训练期间，每个智能体经历了相当于多达 200 年实时《星际争霸》对局的经验。最终的 AlphaStar 智能体由[联赛的纳什分布](https://papers.nips.cc/paper/7588-re-evaluating-evaluation.pdf)中的组件构成——换句话说，就是已发现策略中最有效的混合——可以在单块桌面 GPU 上运行。

这项工作的完整技术描述正在准备发表于一份同行评审期刊。

![三维 joyplot 图，显示 AlphaStar 联赛的纳什分布在 14 个训练日内的发展：随着训练时间推移，较新的智能体（智能体 ID 最高至 600）向右移动。](https://lh3.googleusercontent.com/a_Fnn_8quE6hLlSgAh-vLNTvx5PMypNLysLd3i4tPjL4eJVhqv6fhxADv2gG9NHQQUMdwD2gHufDPoeIJpQYl5DnfO_Wr5IyZSKtca-fyGb2C2t7WA=w1440)

随着 AlphaStar 联赛的推进和新对手的产生，各对手之上的纳什分布。纳什分布——即最不易被利用的一组互补对手——对最新的对手赋予最高权重，这表明相对于之前所有对手的持续进步。

## AlphaStar 如何游玩和观察游戏

像 TLO 和 MaNa 这样的职业《星际争霸》选手平均每分钟能够下达数百个[操作指令](https://github.com/Blizzard/s2client-proto/blob/master/docs/protocol.md#apm)（APM）。这远低于大多数[现有 AI 程序](http://www.cs.mun.ca/~dchurchill/starcraftaicomp/results.shtml)，后者独立控制每个单位，并持续保持数千甚至数万的 APM。

在与 TLO 和 MaNa 的比赛中，AlphaStar 的平均 APM 约为 280，显著低于职业选手，尽管它的操作可能更加精准。较低的 APM 部分是因为 AlphaStar 从回放数据开始训练，因此模仿了人类玩游戏的方式。此外，AlphaStar 从观测到行动之间存在平均 350 毫秒的延迟。

![折线图，对比 AlphaStar、TLO（星灵）和 MaNa 的每分钟操作数（APM）：AlphaStar 的平均 APM 为 277，MaNa 为 390，TLO 为 678；附图中的直方图显示了 AlphaStar 的操作延迟（毫秒）。](https://lh3.googleusercontent.com/5GBTec2tVDDe7dTMi1zKGJRdUQ630ZCVs-kErh_YQgcAgluYRha5Z69tl959lBWWQS0IVVa7bPLaaingb7-MX6Nymj16EsX-7bnuF9sMdMRp5jXv=w1440)

AlphaStar 在与 MaNa 和 TLO 比赛中的 APM 分布，以及观测与行动之间的总延迟。澄清说明（2019 年 1 月 29 日）：TLO 的 APM 看起来比 AlphaStar 和 MaNa 都高，这是因为他使用了快速施放快捷键以及「移出并加入编队」的按键绑定。另请注意，AlphaStar 的有效 APM 爆发有时高于两位选手。

在与 TLO 和 MaNa 的比赛中，AlphaStar 通过原始接口直接与《星际争霸》游戏引擎交互，这意味着它可以直接观察地图上己方和对手可见单位的属性，而无需移动镜头——相当于以一种拉远视角的方式进行游戏。相比之下，人类玩家必须显式地管理一种「注意力经济」，以决定将镜头聚焦于何处。然而，对 AlphaStar 对局的分析表明，它管理着一种隐式的注意力焦点。平均而言，智能体每分钟「切换上下文」约 30 次，与 MaNa 或 TLO 相当。

此外，在比赛之后，我们开发了 AlphaStar 的第二个版本。与人类玩家一样，这个版本的 AlphaStar 自行选择何时何地移动镜头，它的感知仅限于屏幕内的信息，其动作位置也仅限于其可视区域内。

![折线图，对比使用原始接口（红线）与镜头接口（蓝线）训练的 AlphaStar 智能体在 7 个训练日内的预估 MMR。两种接口都呈现超过 7000 MMR 的上升轨迹，远高于职业选手 TLO（星灵）和 MaNa 的水平。](https://lh3.googleusercontent.com/ch78YBvLciJ3G95rbWTD_KD1TBuYEbpk6Cf9VUDTj3SjKcGdCtvbYY2zK7KBkIpZa0tIR4lrQdIdGqkAS_1RcgAnSW85j0emcsrfnkUjYYOyeK7k=w1440)

使用原始接口和镜头接口的 AlphaStar 的表现，显示新训练的镜头接口智能体迅速赶上并几乎达到使用原始接口的智能体的水平。

我们训练了两个新智能体——一个使用原始接口，另一个必须学会控制镜头——与 AlphaStar 联赛对抗。每个智能体都首先通过人类数据进行监督学习训练，然后采用上述强化学习流程。使用镜头接口的 AlphaStar 版本几乎与原始接口一样强大，在我们的内部排行榜上超过了 7000 MMR。在一场表演赛中，MaNa 击败了一个仅训练了 7 天的使用镜头接口的 AlphaStar 原型版本。我们希望在不久的将来评估一个完整训练的镜头接口版本。

这些结果表明，AlphaStar 战胜 MaNa 和 TLO 实际上是由于更出色的宏观和微观战略决策，而不是更高的点击速率、更快的反应时间或原始接口。

## AlphaStar 与职业选手的对战评估

《星际争霸》允许玩家选择三种外星种族之一：人族、虫族或星灵。我们目前选择让 AlphaStar 专精单一种族——星灵——以减少训练时间以及报告内部联赛结果时的方差。请注意，同样的训练流程可以应用于任何种族。我们的智能体被训练用于在 CatalystLE 天梯地图上进行星灵对星灵的《星际争霸 II》（v4.6.2）对局。为了评估 AlphaStar 的表现，我们首先让智能体与 [TLO](https://liquipedia.net/starcraft2/TLO) 对战：他是一名[顶级职业虫族选手](https://liquipedia.net/starcraft2/2018_StarCraft_II_World_Championship_Series_Circuit/Standings)，同时也是宗师级别的星灵玩家。AlphaStar 以 5:0 赢得了这场比赛，使用了丰富多样的单位和建造顺序。「这个智能体的强大程度让我感到惊讶，」他说，「AlphaStar 把众所周知的策略玩出了新花样。它展示了些我以前从未想过的策略，这意味着可能还存在一些我们尚未充分探索的全新玩法。」

在额外训练智能体一周之后，我们与 MaNa 对战——[世界上最强的《星际争霸 II》选手之一](https://liquipedia.net/starcraft2/2018_StarCraft_II_World_Championship_Series_Circuit/Standings)，也是最强的星灵选手前十之一。AlphaStar 再次以 5:0 获胜，展现了强大的微观和宏观战略能力。「让我印象深刻的是，AlphaStar 在几乎每一局比赛中都能打出高阶操作和不同的策略，使用的是一种我完全没有预料到的、非常人性化的打法风格，」他说，「我意识到我的打法多么依赖迫使对手犯错并利用人类的反应，这让我对这款游戏有了全新的认识。我们都很期待接下来会发生什么。」

## AlphaStar 与其他复杂问题

虽然《星际争霸》只是一场游戏——尽管是一款复杂的游戏——但我们认为 AlphaStar 背后的技术可能有助于解决其他问题。例如，它的神经网络架构能够基于不完全信息对非常长的可能动作序列进行建模——游戏通常持续长达一小时、包含数以万计的操作。《星际争霸》的每一帧都被用作一步输入，神经网络在每一帧之后预测游戏剩余部分的预期动作序列。在非常长的数据序列上进行复杂预测这一根本性问题出现在许多现实世界的挑战中，例如天气预测、气候建模、语言理解等等。我们非常期待利用 AlphaStar 项目中的经验和发展，在这些领域取得重大进展。

我们还认为，我们的一些训练方法可能对安全且稳健的 AI 研究有所助益。AI 面临的重大挑战之一是系统出错的方式多种多样，《星际争霸》职业选手此前就很容易通过找到引发这些错误的巧妙方式来击败 AI 系统。AlphaStar 创新的基于联赛的训练过程能找出最可靠、最不容易出错的方法。我们对这种方法在总体上帮助提升 AI 系统安全性与稳健性的潜力感到兴奋，尤其是在能源等安全关键领域，在这些领域处理复杂的边缘情况至关重要。

达到《星际争霸》对局的最高水平，代表了这个有史以来最复杂的电子游戏之一中的重大突破。我们相信，这些进展，加上 [AlphaZero](https://deepmind.com/blog/article/alphazero-shedding-new-light-grand-games-chess-shogi-and-go) 和 [AlphaFold](https://deepmind.google/science/alphafold/) 等项目最近的其他进展，代表着我们在使命上向前迈进了一步：创造有朝一日能帮助我们为世界上一些最重要、最根本的科学问题找到全新解决方案的智能系统。

**我们感谢 Team Liquid 的 TLO 和 MaNa 的支持与卓越技艺。我们也感谢 Blizzard 和《星际争霸》社区的持续支持，使这项工作成为可能。**

**AlphaStar 团队**

Oriol Vinyals、Igor Babuschkin、Junyoung Chung、Michael Mathieu、Max Jaderberg、Wojtek Czarnecki、Andrew Dudzik、Aja Huang、Petko Georgiev、Richard Powell、Timo Ewalds、Dan Horgan、Manuel Kroiss、Ivo Danihelka、John Agapiou、Junhyuk Oh、Valentin Dalibard、David Choi、Laurent Sifre、Yury Sulsky、Sasha Vezhnevets、James Molloy、Trevor Cai、David Budden、Tom Paine、Caglar Gulcehre、Ziyu Wang、Tobias Pfaff、Toby Pohlen、Yuhuai Wu、Dani Yogatama、Julia Cohen、Katrina McKinney、Oliver Smith、Tom Schaul、Timothy Lillicrap、Chris Apps、Koray Kavukcuoglu、Demis Hassabis、David Silver

同时感谢

Ali Razavi、Daniel Toyama、David Balduzzi、Doug Fritz、Eser Aygün、Florian Strub、Guillaume Alain、Haoran Tang、Jaume Sanchez、Jonathan Fildes、Julian Schrittwieser、Justin Novosad、Karen Simonyan、Karol Kurach、Philippe Hamel、Remi Leblond、Ricardo Barreira、Scott Reed、Sergey Bartunov、Shibl Mourad、Steve Gaffney、Thomas Hubert、[创造 PySC2 的团队](https://deepmind.com/blog/announcements/deepmind-and-blizzard-open-starcraft-ii-ai-research-environment)以及整个 DeepMind 团队，特别感谢研究平台团队以及传播与活动团队。

1. [下载与 TLO 和 MaNa 对局的全部 11 场比赛回放](https://deepmind.com/research/open-source/alphastar-resources)
2. [观看与 MaNa 的表演赛](https://www.youtube.com/watch?v=cUTMhmVh1qs)
3. [观看 AlphaStar 与 MaNa 第二局全程的可视化](https://www.youtube.com/watch?v=HcZ48JDamyk)
4. [观看 AlphaStar 对阵 TLO 和 MaNa 的比赛集锦](https://youtu.be/6EQAsrfUIyo)
5. [观看 AlphaStar 对阵 TLO 和 MaNa 的比赛集锦](https://deepmind.com/documents/292/alphastar_reference_bibtex.txt)
6. [如需引用本博客，请使用此 Bibtex](https://storage.googleapis.com/deepmind-media/papers/alphastar_reference_bibtex.txt)
