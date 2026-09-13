---
title: "AlphaStar：运用多智能体强化学习在《星际争霸 II》达到宗师级水平"
title_en: "AlphaStar: Grandmaster level in StarCraft II using multi-agent reinforcement learning"
source: https://deepmind.google/blog/alphastar-grandmaster-level-in-starcraft-ii-using-multi-agent-reinforcement-learning/
site: deepmind
date: 2019-10-30
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaStar：运用多智能体强化学习在《星际争霸 II》达到宗师级水平

> 原文：[AlphaStar: Grandmaster level in StarCraft II using multi-agent reinforcement learning](https://deepmind.google/blog/alphastar-grandmaster-level-in-starcraft-ii-using-multi-agent-reinforcement-learning/) · Google DeepMind

**TL;DR：** AlphaStar 是首个在没有任何游戏限制的情况下，达到一款广受欢迎的电子竞技项目顶级联赛水平的 AI。[今年 1 月](https://deepmind.com/blog/article/alphastar-mastering-real-time-strategy-game-starcraft-ii)，AlphaStar 的一个早期版本向《星际争霸 II》（StarCraft II，有史以来最经久不衰、最受欢迎的即时战略游戏之一）的两位世界顶尖选手发起挑战。此后，我们接受了更大的挑战：在获得职业圈认可的条件之下，以宗师级（Grandmaster）水平完整地游玩这款游戏。

## 我们的新研究与以往工作相比有几个关键不同：

1. AlphaStar 现在拥有与人类玩家相同的约束条件——包括通过「摄像机视角」观察世界，以及对其操作频率施加更严格的限制\*（与《星际争霸》职业选手 [Dario "TLO" Wünsch](https://twitter.com/LiquidTLO?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor) 合作完成）。
2. AlphaStar 现在可以在一对一对战中作为或对抗 Protoss（星灵）、Terran（人族）和 Zerg（虫族）——《星际争霸 II》中的三个种族。星灵、人族和虫族的每个智能体都是一个单一神经网络。
3. 联赛（League）训练完全自动化，且仅从监督学习训练出的智能体起步，而不是复用以往实验中训练过的智能体。
4. [**AlphaStar 在官方游戏服务器**](https://news.blizzard.com/en-us/starcraft2/22933138/deepmind-research-on-ladder)[**Battle.net**](https://www.blizzard.com/en-gb/?ref=battle.net)**上进行了天梯对战，使用与人类玩家相同的地图和条件。所有游戏回放可在**[**这里**](https://deepmind.com/research/open-source/alphastar-resources)**查看。**

我们选择使用通用的机器学习技术——包括神经网络、通过强化学习进行的自我博弈、多智能体学习和模仿学习——以通用方法直接从游戏数据中学习。借助[《自然》论文](https://rdcu.be/bVI7G)中描述的进展，AlphaStar 在 Battle.net 上的排名超过了 99.8% 的活跃玩家，并在《星际争霸 II》全部三个种族——星灵、人族和虫族——上都达到了宗师级水平。我们预期这些方法可以应用于许多其他领域。

基于学习的系统与自我博弈是优雅的研究概念，它们推动了人工智能领域非凡的进步。1992 年，IBM 的研究人员开发了 TD-Gammon，将基于学习的系统与神经网络相结合来玩西洋双陆棋。TD-Gammon 并非按照硬编码的规则或启发式方法对弈，而是被设计为利用强化学习，通过反复试错，摸索出如何以最大化获胜概率的方式玩这款游戏。它的开发者运用了自我博弈的理念让系统更加稳健：通过与自身的各个版本对弈，系统的棋艺日益精进。两者相结合，基于学习的系统与自我博弈提供了一种强大的开放式学习范式。

此后的许多进展证明，这些方法可以扩展到难度递增的领域。例如，AlphaGo 和 AlphaZero 证明了一个系统可以学会在围棋、国际象棋和将棋上达到超越人类的水平；[OpenAI Five](https://openai.com/blog/openai-five/) 和 DeepMind 的 [FTW](https://deepmind.com/blog/article/capture-the-flag-science) 则展示了自我博弈在现代游戏 Dota 2 和雷神之锤 III（Quake III）中的威力。

在 DeepMind，我们感兴趣的是理解开放式学习的潜力——及其局限——它使我们能够开发出稳健而灵活的智能体，应对复杂的真实世界领域。像《星际争霸》这样的游戏是推进这些方法的绝佳训练场，因为玩家必须利用有限的信息做出动态而艰难的决策，而这些决策会在多个层面和多个时间尺度上产生影响。

> 我发现 AlphaStar 的对局表现令人赞叹——这个系统非常擅长评估自己的战略态势，并且清楚地知道何时与对手交战、何时脱离。虽然 AlphaStar 拥有出色而精准的操作，但它并不让人觉得「超人」——肯定没有超出人类理论上可达到的水平。总体而言，它感觉很公平——就像在下一盘「真正的」《星际争霸》。

Dario "TLO" Wünsch

《星际争霸 II》职业选手

尽管自我博弈屡获成功，它也有众所周知的缺陷。最显著的一个是遗忘：一个与自己对弈的智能体可能不断进步，但它也可能忘记如何战胜自己以前的版本。遗忘会造成智能体「追逐自己的尾巴」的循环，永远无法收敛，也无法取得真正的进步。例如，在石头剪刀布游戏中，智能体当前可能更倾向于出石头。随着自我博弈的进行，新的智能体会转而出布，因为布能赢石头。再往后，这个智能体会转而出剪刀，最终又回到石头，形成一个循环。虚拟自我博弈（fictitious self-play）——与以往所有策略的混合体对弈——是应对这一挑战的一种方案。

在首次将《星际争霸 II》[开源为研究环境](https://deepmind.com/blog/announcements/deepmind-and-blizzard-open-starcraft-ii-ai-research-environment)之后，我们发现即便是虚拟自我博弈技术也不足以产生强大的智能体，于是我们着手开发一种更好的通用解决方案。我们近期发表的《自然》论文的一个核心思想，是将虚拟自我博弈的概念扩展到一组智能体——即「联赛」。通常在自我博弈中，每个智能体都会最大化自己战胜对手的概率；然而这只是解决方案的一部分。在现实世界中，一个想提高《星际争霸》水平的玩家可能会选择与朋友结伴训练特定策略。如此一来，他们的训练搭档并不是为了战胜每一个可能的对手而打，而是为了暴露朋友的缺陷，帮助他们成为更出色、更稳健的选手。联赛的关键洞见在于：只求获胜是不够的——我们既需要目标是在对所有人时获胜的主力智能体（main agents），也需要专注于通过暴露主力智能体的缺陷来帮助其成长的利用者智能体（exploiter agents），而不是最大化自己对所有玩家的胜率。借助这种训练方法，联盟能以端到端、全自动的方式学会其全部复杂的《星际争霸 II》策略。

![示意图，展示利用利用者智能体进行训练如何打破自我博弈中的「遗忘」循环，以《星际争霸 II》单位（虚空辉光舰、追猎者和不朽者）作为石头剪刀布的类比。](https://lh3.googleusercontent.com/VzlaoRoPV8ehTc4CEW18Rg7QIOSAxnkDOGNgZEtMX6XW_gbQtosXNg0BSwjMtQDaC1Z7jcRlhRBHCyrGji4DnIrH5NYiPOPDEFTEdWYpu2uA-Er7fA=w1440)

图 1 描绘了《星际争霸》这类复杂领域中的一些挑战。（上排）玩家可以创造各种「单位」（例如工人、战斗单位或运输单位）来实施不同的战略部署。各单位的强项与弱点相互制衡，类似于石头剪刀布。得益于模仿学习，我们最初的智能体已经能够执行一套多样的策略，这里表现为游戏中创造的单位组合（在本例中：虚空辉光舰、追猎者和不朽者）。然而，由于某些策略更容易取得改进，朴素的强化学习会狭隘地聚焦于这些策略。其他策略可能需要更多学习，或者存在一些微妙的细节，使智能体更难将其完善。这就造成了一个恶性循环：某些有效的策略显得越来越低效，因为智能体为了主导策略而放弃了它们。（下排）我们在联赛中加入了一些智能体，其唯一目的就是暴露主力智能体的弱点。这意味着将有更多有效策略被发现和发展，使主力智能体面对对手时稳健得多。与此同时，我们采用了模仿学习技术（包括蒸馏）来防止 AlphaStar 在整个训练过程中遗忘，并使用隐变量来表示多样的开局策略。

探索是《星际争霸》这类复杂环境中的另一个关键挑战。我们的智能体在每个时间步最多有 1026 种可能的操作，而且它必须做出数千次操作之后才能知道自己这一局是胜是负。在如此庞大的解空间中寻找制胜策略极具挑战。即便拥有强大的自我博弈系统以及由主力智能体和利用者智能体组成的多元联赛，如果没有任何先验知识，一个系统几乎不可能在如此复杂的环境中发展出成功的策略。学习人类策略，并确保智能体在整个自我博弈过程中持续探索这些策略，是解锁 AlphaStar 性能的关键。为此，我们使用了模仿学习——结合先进的神经网络架构和用于语言建模的技术——创建了一个初始策略，其水平超过了 84% 的活跃玩家。我们还使用了一个隐变量来条件化策略，它编码了人类对局中开局走法的分布，这有助于保留高层策略。随后，AlphaStar 在整个自我博弈过程中使用了某种形式的蒸馏，将探索引导向人类策略。这一方法使 AlphaStar 能够在单个神经网络（每个种族一个）中容纳多种策略。在评估时，该神经网络不依赖于任何特定的开局走法。

> AlphaStar 是一位耐人寻味、不落窠臼的选手——拥有顶尖职业选手的反应和速度，但策略和风格却完全是它自己的。AlphaStar 通过智能体在联赛中相互竞争的方式训练而来，其打法之出人意料令人难以想象；它真的会让你反思：职业选手究竟探索了《星际争霸》多少样的可能性。

Diego "Kelazhur" Schwimer

《星际争霸 II》职业选手

此外，我们发现许多先前的强化学习方法在《星际争霸》中都难以奏效，原因在于其巨大的操作空间。具体来说，AlphaStar 使用了一种新的离策略强化学习算法，使它能够从旧策略对弈的游戏中高效地更新自己的策略。

利用基于学习的智能体和自我博弈的开放式学习系统，已在难度不断攀升的领域中取得了令人瞩目的成果。得益于模仿学习、强化学习和联赛的进展，我们得以训练出 AlphaStar Final——一个在未做任何修改的完整《星际争霸 II》游戏中达到宗师级水平的智能体，如上方视频所示。这个智能体通过游戏平台 Battle.net 匿名在线对战，并使用《星际争霸 II》全部三个种族达到了宗师级水平。AlphaStar 使用「摄像机视角」界面进行游戏，所获取的信息与人类玩家相仿，并且其操作频率受到限制，使其可与人类玩家相提并论。界面和限制方案获得了职业选手的认可。归根结底，这些结果有力地证明：通用学习技术可以让 AI 系统扩展到由多个参与者构成的复杂动态环境中工作。我们开发 AlphaStar 所用的技术，将有助于进一步全面提升 AI 系统的安全性与稳健性，并且我们希望，它们能推进我们在真实世界领域的研究。

> 看到这个智能体以不同于人类玩家的方式发展出自己的策略，令人兴奋……对它可执行操作的上限限制和摄像机视角限制，如今让对局变得很有看头——尽管作为职业选手，我仍能看出这个系统的一些弱点。

Grzegorz "MaNa" Komincz

在 [Nature](https://doi.org/10.1038/s41586-019-1724-z) 上阅读有关这项工作的更多内容

[这里](https://rdcu.be/bVI7G)可获取公开版论文

查看全部 [Battle.net 游戏回放](https://deepmind.com/research/open-source/alphastar-resources)

**AlphaStar 团队**

Oriol Vinyals、Igor Babuschkin、Wojciech M. Czarnecki、Michaël Mathieu、Andrew Dudzik、Junyoung Chung、David H. Choi、Richard Powell、Timo Ewalds、Petko Georgiev、Junhyuk Oh、Dan Horgan、Manuel Kroiss、Ivo Danihelka、Aja Huang、Laurent Sifre、Trevor Cai、John P. Agapiou、Max Jaderberg、Alexander S. Vezhnevets、Rémi Leblond、Tobias Pohlen、Valentin Dalibard、David Budden、Yury Sulsky、James Molloy、Tom L. Paine、Caglar Gulcerhe、Ziyu Wang、Tobias Pfaff、Yuhuai Wu、Roman Ring、Dani Yogatama、Dario Wünsch、Katrina McKinney、Oliver Smith、Tom Schaul、Timothy Lillicrap、Koray Kavukcuoglu、Demis Hassabis（德米斯·哈萨比斯）、Chris Apps、David Silver

**致谢**

我们感谢 [Dario Wünsch（TLO）](https://twitter.com/LiquidTLO)、[Grzegorz Komincz（MaNa）](https://twitter.com/Liquid_MaNa)和 [Diego Schwimer（Kelazhur）](https://twitter.com/kelazhur)提供的建议、指导和精湛技艺。我们也感谢 Blizzard 以及《星际争霸》游戏界和 AI 社区的持续支持，使这项工作成为可能——尤其是那些在 Battle.net 上与 AlphaStar 对战过的玩家。感谢 Ali Razavi、Daniel Toyama、David Balduzzi、Doug Fritz、Eser Aygün、Florian Strub、Guillaume Alain、Haoran Tang、Jaume Sanchez、Jonathan Fildes、Julian Schrittwieser、Justin Novosad、Karen Simonyan、Karol Kurach、Philippe Hamel、Ricardo Barreira、Scott Reed、Sergey Bartunov、Shibl Mourad、Steve Gaffney、Thomas Hubert、[创建 PySC2 的团队](https://deepmind.com/blog/announcements/deepmind-and-blizzard-open-starcraft-ii-ai-research-environment)以及整个 DeepMind 团队，特别感谢研究平台团队以及传播与活动团队。

\*智能体的操作被限制为每 5 秒最多 22 次智能体操作，其中一次智能体操作对应一次选择、一个技能和一个目标单位或目标点，在游戏内 APM 计数器中最多计为 3 次操作。移动摄像机同样算作一次智能体操作，尽管它不计入 APM。
