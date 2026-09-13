---
title: "AlphaZero：为国际象棋、将棋和围棋带来新启示"
title_en: "AlphaZero: Shedding new light on chess, shogi, and Go"
source: https://deepmind.google/blog/alphazero-shedding-new-light-on-chess-shogi-and-go/
site: deepmind
date: 2018-12-06
crawled: 2026-09-13
translated: 2026-09-13
---

# AlphaZero：为国际象棋、将棋和围棋带来新启示

> 原文：[AlphaZero: Shedding new light on chess, shogi, and Go](https://deepmind.google/blog/alphazero-shedding-new-light-on-chess-shogi-and-go/) · Google DeepMind

2017 年底，我们[发布了 AlphaZero](https://arxiv.org/abs/1712.01815)——一个从零开始自学掌握国际象棋、[将棋](https://en.wikipedia.org/wiki/Shogi)（日本象棋）和[围棋](https://en.wikipedia.org/wiki/Go_(game))的单一系统，并在每一项上击败了世界冠军程序。我们对初步结果感到兴奋，也为国际象棋界的反响而欣喜：他们在 AlphaZero 的对局中看到了一种开创性的、极具动态性的、「[非传统](https://www.ft.com/content/ea707a24-f6b7-11e7-8715-e94187b3017e)」的棋风，与以往的任何国际象棋引擎都不相同。

今天，我们很高兴地介绍 AlphaZero 的完整评估，[已发表于《科学》（Science）期刊](https://www.science.org/doi/full/10.1126/science.aar6404)（[开放获取版本见此](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphazero-shedding-new-light-on-chess-shogi-and-go/alphazero_preprint.pdf)），它确认并更新了那些初步结果。评估描述了 AlphaZero 如何快速学会每一项游戏并成为各项历史上最强的棋手——尽管它的训练从随机走子开始，除了游戏的基本规则之外没有任何内置的领域知识。

> 我无法掩饰自己的满足感——它的棋风非常富有动态性，和我自己的风格很像！

加里·卡斯帕罗夫（Garry Kasparov）

前国际象棋世界冠军

这种不受人类棋风惯例约束、从零学习每一项游戏的能力，造就了一种独特的、非正统却富有创造性和动态性的棋风。国际象棋特级大师 Matthew Sadler 与女子国际大师 Natasha Regan 为[他们即将出版的著作《Game Changer》](https://www.newinchess.com/game-changer)（New in Chess，2019 年 1 月）分析了数千盘 AlphaZero 的国际象棋对局，他们表示它的棋风不同于任何传统国际象棋引擎。「这就像发现了过去某位伟大棋手的秘密笔记，」Matthew 说。

传统的国际象棋引擎——包括世界计算机国际象棋冠军 [Stockfish](https://en.wikipedia.org/wiki/Stockfish_(chess)) 和 [IBM 具有开创性的「深蓝」（Deep Blue）](https://www.ibm.com/ibm/history/ibm100/us/en/icons/deepblue/)——依赖由高水平人类棋手手工编写的数千条规则和启发式方法，试图涵盖对局中可能出现的每一种情况。将棋程序同样是针对特定游戏的，使用的搜索引擎和算法与国际象棋程序类似。

AlphaZero 采取了完全不同的方法，用深度[神经网络](https://en.wikipedia.org/wiki/Artificial_neural_network)和通用算法取代了这些手工编写的规则——除了基本规则之外，它们对游戏一无所知。

![动画折线图，展示 AlphaZero 的强化学习进展。在围棋棋盘插图旁，图中绘制了 Elo 等级分随训练步数（至 70 万步）的变化，展示 AlphaZero 如何在自我博弈中迅速提升棋力。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/622693c3f70ee14b39e7ee17_AlphaZero.gif)

在国际象棋中，AlphaZero 仅用了 4 个小时就首次超越 Stockfish；在将棋中，AlphaZero 用了 2 个小时首次超越 Elmo；在围棋中，AlphaZero 用了 30 个小时首次超越 2016 年击败传奇棋手李世石（Lee Sedol）的 AlphaGo 版本。注：每个训练步代表 4,096 个棋盘局面。

为了学习每一项游戏，一个未经训练的神经网络通过一种称为[强化学习](https://en.wikipedia.org/wiki/Reinforcement_learning)的试错过程与自己对弈数百万盘。起初，它完全随机地落子，但随着时间推移，系统从胜、负与和局中学习，调整神经网络的参数，使其更有可能在将来选择有利的着法。网络所需的训练量取决于游戏的风格和复杂度：国际象棋约需 9 小时，将棋约需 12 小时，围棋约需 13 天。

> 它的一些着法，比如把王走到棋盘中央，违背了将棋理论，而且从人类的角度看，似乎让 AlphaZero 陷入了危险的境地。但不可思议的是，它始终掌控着棋盘。它独特的棋风向我们展示了这项游戏的新可能。

羽生善治（Yoshiharu Habu）

九段职业棋手，历史上唯一同时持有将棋全部七大头衔的棋手

训练好的网络用于引导一种搜索算法——即蒙特卡洛树搜索（Monte-Carlo Tree Search，MCTS）——来在对局中选择最有希望的着法。对于每一步棋，AlphaZero 只搜索传统国际象棋引擎所考虑局面中的一小部分。以国际象棋为例，它每秒只搜索 6 万个局面，而 Stockfish 大约搜索 6,000 万个。

![信息图，对比每次决策的搜索量：人类特级大师搜索数百种走法，AlphaZero 搜索数万种走法，而最先进的国际象棋引擎搜索数千万种走法。](https://lh3.googleusercontent.com/e0wFggmSiOjbp5jtZ1xq8sNhAvOf7ids49D-qzO1wMl1w7cxVoZ8F5L02VzQ1SWvmHu3pqazmc2UY5N3cAU52A3dH_8XXkQYXn9HNkLgn1A0QVVUm60=w1440)

完整训练的系统接受了与最强手工编排引擎的测试：国际象棋的 [Stockfish](https://en.wikipedia.org/wiki/Stockfish_(chess)) 和将棋的 [Elmo](https://en.wikipedia.org/wiki/Elmo_(shogi_engine))，以及我们此前自学的系统 [AlphaGo Zero](https://deepmind.com/blog/article/alphago-zero-starting-scratch)——已知最强的围棋棋手。

- 每个程序都在为其设计的硬件上运行。Stockfish 和 Elmo 使用 44 个 CPU 核心（与 [TCEC 世界锦标赛](https://en.wikipedia.org/wiki/Top_Chess_Engine_Championship)中的配置相同），而 AlphaZero 和 AlphaGo Zero 使用一台配备 4 个第一代 [TPU](https://cloud.google.com/tpu/docs/tpus) 和 44 个 [CPU](https://en.wikipedia.org/wiki/Central_processing_unit) 核心的机器。第一代 TPU 的推理速度大致与 [NVIDIA Titan V GPU](https://www.nvidia.com/en-gb/titan/titan-v/) 等商用硬件相当，尽管两者架构无法直接比较。
- 所有比赛采用的时限为每局 3 小时，另加每步棋 15 秒。

在每项评估中，AlphaZero 都令人信服地击败了对手：

- 在国际象棋中，AlphaZero 击败了 [2016 年 TCEC（第 9 季）](https://www.chessbomb.com/arena/-/2016-tcec9)世界冠军 [Stockfish](https://stockfishchess.org/)，在 1,000 盘中赢下 155 盘，仅输 6 盘。为了验证 AlphaZero 的稳健性，我们还进行了从常见人类开局出发的一系列比赛。在每一种开局中，AlphaZero 都击败了 Stockfish。我们还进行了一场从 2016 年 TCEC 世界锦标赛所用开局局面集合出发的比赛，以及与最新开发版 Stockfish、以及使用强大开局库的 Stockfish 变体的一系列额外比赛。在所有比赛中，AlphaZero 均获胜。
- 在将棋中，AlphaZero 击败了 [2017 年 CSA 世界冠军版本的 Elmo](http://www2.computer-shogi.org/wcsc27/index_e.html)，胜率达 91.2%。
- 在围棋中，AlphaZero 击败了 [AlphaGo Zero](https://deepmind.com/blog/article/alphago-zero-learning-scratch)，胜率为 61%。

![信息图，对比 AlphaZero 在国际象棋、将棋和围棋中分别对阵 Stockfish、Elmo 和 AlphaGo Zero 的表现，显示按执白或执黑细分的胜/和/负比率。](https://lh3.googleusercontent.com/zyxpKGbbGJK-pId62KSa3pjYEYfdAHeOCCh6asmtiJD4jVdgxOZlNMWQ3HKKstdex7YVdAIgejUQlIB4VsbRJu2dU1hBiK77wcX9pSJMO3jDlJ6pGm4=w1440)

不过，玩家们最感兴趣的可能是 AlphaZero 下这些棋的方式。以国际象棋为例，AlphaZero 在自我博弈训练中独立发现并运用了常见的人类棋理，如开局、王的安全和兵形。但由于它是自学的，因此不受关于这项游戏的传统观念约束，它还发展出了自己的直觉和策略，增添了一套崭新的、开阔的、令人兴奋的新想法，为几个世纪以来关于国际象棋战略的思考锦上添花。

> 一个多世纪以来，国际象棋一直被用作人类认知与机器认知的「罗塞塔石碑」。AlphaZero 做了一件非同寻常的事，让一种古老棋盘游戏与尖端科学之间非凡的联系焕然一新。

加里·卡斯帕罗夫（Garry Kasparov）

前国际象棋世界冠军

Matthew Sadler 说，玩家首先注意到的就是 AlphaZero 的棋风——「它的棋子带着目的与力量包围对手的王的那个样子」。他说，支撑这一点的是 AlphaZero 高度动态的对弈方式：最大化己方棋子的活动性与机动性，同时最小化对手棋子的活动性与机动性。与直觉相反的是，AlphaZero 似乎对「子力」（material）的重视程度较低，而子力是现代棋艺的基石——每种棋子都有一个价值，如果一方在棋盘上棋子总价值高于另一方，那么它就拥有子力优势。相反，AlphaZero 愿意在棋局早期牺牲子力，以换取只有在长期才能收回的收益。

「令人印象深刻的是，它能在非常广泛的局面和开局中贯彻自己的棋风，」Matthew 说道。他还观察到，AlphaZero 从第一步棋起就以非常从容的风格行棋，带有「一种非常人性化的、目标始终如一的感觉」。

「传统引擎极其强大，很少犯明显的错误，但面对没有具体可计算解法的局面时可能会迷失方向，」他说。「恰恰是在需要『感觉』、『洞察』或『直觉』的局面中，AlphaZero 才大显身手。」

> 其影响远远超出了我所热爱的棋盘……这些自学成才的专家机器不仅表现得出色，我们还能真正从它们产生的新知识中学习。

加里·卡斯帕罗夫（Garry Kasparov）

前国际象棋世界冠军

这种在其他传统国际象棋引擎中未曾见过的独特能力，已被用来为棋迷提供对最近 [Magnus Carlsen](https://en.wikipedia.org/wiki/Magnus_Carlsen) 与 [Fabiano Caruana](https://en.wikipedia.org/wiki/Fabiano_Caruana) 之间[国际象棋世界冠军赛](https://worldchess.com/)的[全新洞见与解说](https://chess24.com/en/read/news/alphazero-on-carlsen-caruana-games-1-8)，并将在[《Game Changer》](https://www.newinchess.com/game-changer)中进一步探讨。「看到 AlphaZero 的分析与顶级国际象棋引擎乃至特级大师实战的差异，实在令人着迷，」Natasha Regan 说。「AlphaZero 可能会成为整个棋界的强大教学工具。」

AlphaZero 带来的启示与我们在 [AlphaGo](https://deepmind.com/research/case-studies/alphago-the-story-so-far) 于 2016 年对弈传奇冠军李世石（Lee Sedol）时所看到的遥相呼应。在那几局[比赛](https://deepmind.com/alphago-korea)中，AlphaGo 下出了许多[极具创造性的制胜着法](https://deepmind.com/blog/article/innovations-alphago)，包括第二局中的第 37 手，颠覆了数百年的思维定式。这些着法——以及许多其他着法——此后被各个水平的棋手研究，包括李世石本人，他在谈到第 37 手时说：「我曾以为 AlphaGo 是基于概率计算的，只不过是一台机器。但当我看到这一手时，我改变了想法。AlphaZero……AlphaGo 确实是有创造力的。」

正如围棋一样，我们对 AlphaZero 在国际象棋上展现的创造性回应感到兴奋。自计算时代黎明以来，国际象棋一直是人工智能的一项重大挑战，包括巴贝奇（Babbage）、图灵（Turing）、香农（Shannon）和冯·诺依曼（von Neumann）在内的早期先驱都曾尝试设计国际象棋程序。但 AlphaZero 的意义远不止于国际象棋、将棋或围棋。要创造能够解决广泛现实问题的智能系统，我们需要它们具备灵活性，并能泛化到新情境。虽然朝这一目标已取得一些进展，但它仍然是 AI 研究中的一项重大挑战——系统能够以极高的水准掌握特定技能，但在面对哪怕稍有变化的任务时却常常失败。

AlphaZero 掌握三种不同复杂游戏——并且潜在地可以掌握任何完全信息博弈——的能力，是克服这一问题的重要一步。它证明了单一算法可以学会在一系列情境中发现新知识。虽然现在还为时尚早，但 AlphaZero 的创造性洞见，加上我们在 [AlphaFold](https://deepmind.google/science/alphafold/) 等其他项目中看到的令人鼓舞的结果，让我们对[我们的使命](https://deepmind.com/about/)充满信心：创造通用的学习系统，有朝一日帮助我们为一些最重要、最复杂的科学问题找到全新的解决方案。

**附注**

1. 阅读[发表于《科学》的论文](http://science.sciencemag.org/cgi/content/full/362/6419/1140?ijkey=XGd77kI6W4rSc&keytype=ref&siteid=sci)
2. 下载[论文的开放获取版本](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphazero-shedding-new-light-on-chess-shogi-and-go/alphazero_preprint.pdf) [PDF]
3. 阅读加里·卡斯帕罗夫撰写的《科学》[配套社论](http://science.sciencemag.org/content/362/6419/1087)
4. 阅读「深蓝」共同创造者 Murray Campbell 在《科学》上发表的[配套 Perspective 文章](http://science.sciencemag.org/content/362/6419/1118)
5. 下载[由特级大师 Matthew Sadler 挑选的 AlphaZero 对 Stockfish 20 盘最佳对局](https://storage.googleapis.com/deepmind-media/DeepMind.com/Open-Source/alphazero-resources/alphazero_stockfish_top20.zip) [.zip]
6. 下载[由将棋名家羽生善治挑选的 AlphaZero 对 Elmo 10 盘最佳对局](https://storage.googleapis.com/deepmind-media/DeepMind.com/Open-Source/alphazero-resources/alphazero_elmo_top10%20(1).zip) [.zip]
7. 下载 [210 盘 AlphaZero 对 Stockfish 的国际象棋对局和 100 盘 AlphaZero 对 Elmo 的将棋对局](https://deepmind.com/research/open-source/alphazero-resources)
8. 下载[配套美术素材](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphazero-shedding-new-light-on-chess-shogi-and-go/alphazero_images.zip)
9. 进一步了解 AlphaZero 主题图书[《Game Changer》](https://www.newinchess.com/game-changer)（New in Chess，2019 年 1 月）

这项工作由 David Silver、Thomas Hubert、Julian Schrittwieser、Ioannis Antonoglou、Matthew Lai、Arthur Guez、Marc Lanctot、Laurent Sifre、Dharshan Kumaran、Thore Graepel、Timothy Lillicrap、Karen Simonyan 和 Demis Hassabis 完成。
