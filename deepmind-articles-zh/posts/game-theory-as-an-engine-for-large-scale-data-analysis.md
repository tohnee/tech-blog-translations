---
title: "博弈论：大规模数据分析的引擎"
title_en: "Game theory as an engine for large-scale data analysis"
source: https://deepmind.google/blog/game-theory-as-an-engine-for-large-scale-data-analysis/
site: deepmind
date: 2021-05-06
crawled: 2026-09-13
translated: 2026-09-13
---

# 博弈论：大规模数据分析的引擎

> 原文：[Game theory as an engine for large-scale data analysis](https://deepmind.google/blog/game-theory-as-an-engine-for-large-scale-data-analysis/) · Google DeepMind

EigenGame 为解决基础机器学习问题开辟了一条新路径。

现代 AI 系统处理诸如[识别图像中的物体](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)和[预测蛋白质 3D 结构](https://deepmind.com/blog/article/alphafold-a-solution-to-a-50-year-old-grand-challenge-in-biology)这类任务的方式，就像一个勤奋的学生备考一样：通过在大量示例问题上训练，逐步减少错误，直到取得成功。但这是一种孤军奋战式的努力，也只是已知学习形式中的一种。学习同样可以通过与他人互动和博弈来进行。单个个体极少能独自解决极其复杂的问题。通过让问题求解带上这种博弈特质，DeepMind 先前的项目已经训练出能玩 [Capture the Flag](https://deepmind.com/blog/article/capture-the-flag-science) 的 AI 智能体，并在《星际争霸》中达到[宗师级别](https://deepmind.com/blog/article/alphastar-mastering-real-time-strategy-game-starcraft-ii)。这让我们思考：这种以博弈论为模型看待问题的视角，能否帮助解决其他基础机器学习问题。

在 [ICLR 2021](https://iclr.cc/)（国际学习表征会议）上，我们发表了《[EigenGame: PCA as a Nash Equilibrium](https://openreview.net/forum?id=NzTU59SYbNq)》（EigenGame：作为纳什均衡的 PCA），并获得了杰出论文奖。我们的研究为老问题探索了新解法：我们将主成分分析（PCA）——一种[特征值问题](https://en.wikipedia.org/wiki/Eigendecomposition_of_a_matrix)——重新表述为一个竞争性的多智能体博弈，我们称之为 EigenGame。PCA 通常被表述为一个优化问题（或单智能体问题）；然而我们发现，多智能体视角让我们得以发展出新的洞见与算法，并充分利用最新的计算资源。这使我们能够扩展到此前因计算需求过高而无法处理的海量数据集，并为未来的探索提供了另一种路径。

## 作为纳什均衡的 PCA

[PCA](https://en.wikipedia.org/wiki/Principal_component_analysis) 最早出现于 20 世纪初，是一种理解高维数据结构的经典技术。如今这一方法在数据处理流程中无处不在，作为第一步，它使数据的聚类与可视化变得容易。它也可以是学习低维表示以用于回归和分类的有用工具。一个多世纪过去了，研究 PCA 依然有着令人信服的理由。

首先，数据最初是人工记录在纸质笔记本上的，而现在它存储在仓库大小的数据中心里。结果是，这一熟悉的分析已成为计算瓶颈。研究者已经探索了[随机化算法](https://arxiv.org/abs/0909.4061)等方向来改进 PCA 的扩展性，但我们发现这些方法难以扩展到海量数据集，因为它们无法充分利用近期以深度学习为中心的计算进展——即对大量并行 GPU 或 TPU 的使用。

其次，PCA 与许多重要的机器学习和工程问题共享同一解，即[奇异值分解](https://en.wikipedia.org/wiki/Singular_value_decomposition)（SVD）。以正确的方式处理 PCA 问题，我们的洞见与算法就能更广泛地应用于机器学习之树的各个分支。

![机器学习之树的插图：树根标注为"SVD"，向上分叉成大脑形状的树冠，其中包含代表机器学习概念的圆圈：PCA、最小二乘、谱聚类、PVF、LSI 和排序。](https://lh3.googleusercontent.com/P5RV6oEE0BzEroaVUYlFOUSgOzr3QLwOdHa77-BlYwkSubeILRTjhkIg1pdb6eVNs6O8v16qYKCdnTcIuTjMKPo_l6H3vbdgzu5E0bzN83SgULF4=w1440)

图 1. 以 SVD 为根，这棵知识之树涵盖了机器学习中的许多基本思想，包括 PCA、最小二乘、谱聚类、原型价值函数（Proto Value Functions）、潜在语义索引和排序。

与任何棋盘游戏一样，要把 PCA 重新发明为一个博弈，我们需要一套供玩家遵循的规则与目标。设计这样一个博弈有很多可能的方式；不过，重要的思想来自 PCA 本身：最优解由特征向量构成，这些特征向量捕捉数据中重要的方差，并且彼此正交。

![将 PCA 表示为博弈的插图：数据点散点图上有两个正交的向量箭头，"玩家 1"（蓝色）与最大方差方向对齐，"玩家 2"（粉色）与其正交。](https://lh3.googleusercontent.com/nMwA723PiBoJDNTjJ4erYB-IJmm58-grtE47prwxe4B-9rQxPdP9XicouqsQfmmD28M7kVExqP1K5pP0ettVoVdvBn25ECqpQb-qfwzSN7h5XndoDA=w1440)

图 2. 每个玩家都想与最大方差方向（数据散布更大）对齐，同时保持与层级中位于其上方的玩家（所有编号更小的玩家）垂直。

在 EigenGame 中，每个玩家控制一个特征向量。玩家通过解释数据中的方差来增加得分，但如果与其他玩家过于接近（对齐）则会受到惩罚。我们还建立了一个层级：玩家 1 只关心最大化方差，而其他玩家还必须担心最小化自己与层级中位于其上方的玩家的对齐程度。这种奖励与惩罚的组合定义了每个玩家的效用。

![插图：展示 EigenGame 中效用函数的数学表达式，由方差项减去对齐项之和计算得出。方差项以散点图和对角向量示意，对齐项以正交的红蓝两个向量示意。](https://lh3.googleusercontent.com/8sy0BGzdnswoFSHFG9j1N9d9v5yIk5-D83zEXh5NcK7x4a5LgIEGYVRd-OuPrdbMyRJQB1-X5N7HLJaA4BGf7XZ-tJP-Ppfd4KmmBbvJZ0oIxaseTms=w1440)

图 3. 对上述每个玩家效用的总结。

通过恰当设计的 **Var** 和 **Align** 项，我们可以证明：

- 如果所有玩家都最优地行动，他们共同达成博弈的[纳什均衡](https://en.wikipedia.org/wiki/Nash_equilibrium)，即 PCA 的解。
- 这可以通过每个玩家独立且同时使用梯度上升来最大化自身效用而实现。

![3D 向量在球面上收敛的插图：左侧为互相正交的"真实特征向量"，标注为 V1（蓝色）、V2（粉色）和 V3（青色）；右侧为三条对应的彩色圆点路径，从空心圆（起点）出发，沿着线框球面轨迹，最终在箭头处（终点）与这些真实特征向量对齐。](https://lh3.googleusercontent.com/TetiQUjXs4WHCllUvxk898iSHEzofUiKPrgS6cBRlKGr16F9DFtSt2m95tf_wvO73_U-wUAn1LK4mLe0LAnL_kw_RwytRVP7papsWTOKiu0oqIrnBg=w1440)

图 4. EigenGame 引导每个玩家沿单位球面从空心圆并行移动到箭头处。蓝色是玩家 1，红色是玩家 2，绿色是玩家 3。

这种同时上升的独立性尤为重要，因为它允许计算分布在数十个 Google Cloud TPU 上，同时实现数据并行与模型并行。这使得我们的算法能够适应真正大规模的数据。对于包含数百万个特征或数十亿行数据的数百 TB 数据集，EigenGame 只需数小时即可找到主成分。

![比较模型并行数据分布的插图：左侧，一个 3x3 网格将不同玩家（V1、V2、V3、VK-2、VK-1、VK）分配到单个计算设备；右侧，玩家分布在更大的分组设备池中，以实现更大的规模。](https://lh3.googleusercontent.com/q-34Fz9ZOZ6stlScBEd1a12GLLv0MTBlNc8LwljNk7OMaZZKs6ZXlt7Jzt_c25aN5mauMH73dkle-uXyLKNpeEYTfaivJ_ai_bHkhlolQADkrzsTJw=w1440)

图 5. 每个彩色方块是一台独立的设备。(左) 每个玩家在一台设备上生存并计算更新。(右) 每个玩家被复制到多台设备上，并使用相互独立的数据批次计算更新；不同更新随后被平均，以形成更稳健的更新方向。

## 效用、更新以及介于其间的种种

通过从多智能体视角思考 PCA，我们得以提出可扩展的算法和新颖的分析。我们还发现了一个与[赫布学习](https://en.wikipedia.org/wiki/Hebbian_theory)（Hebbian Learning，即神经元如何在学习中适应）之间令人惊讶的联系。在 EigenGame 中，每个玩家最大化自身效用所产生的更新方程，与从大脑突触可塑性的赫布模型推导出的[更新规则](https://en.wikipedia.org/wiki/Generalized_Hebbian_algorithm)相似。赫布更新已知会收敛到 PCA 的解，但它们并不是作为任何效用函数的梯度推导出来的。博弈论为我们提供了一个看待赫布学习的新视角，也暗示了一条通往机器学习问题的连续谱系。

在机器学习连续谱的一端，是发展成熟的方法：提出一个可优化的目标函数。借助凸优化与非凸优化理论，研究者可以推理解的全局性质。在另一端，纯粹基于[连接主义](https://en.wikipedia.org/wiki/Connectionism)的方法和受神经科学启发的更新规则被直接指定，但对整个系统的分析可能更加困难，往往需要借助对复杂[动力系统](https://en.wikipedia.org/wiki/Dynamical_system)的研究。

EigenGame 这类博弈论方法则介于两者之间。玩家更新不局限于某个函数的梯度，只需是对其他玩家当前策略的最优反应。我们可以自由地设计具有理想性质的效用与更新——例如指定无偏的或加速的更新——同时确保纳什性质仍让我们能够把系统作为整体进行分析。

![梯度条形图：展示机器学习方法的连续谱，从左到右依次为"有效用（优化）"、居中的"多个效用（多智能体/博弈论）"，以及右侧的"无效用（赫布/动力系统）"。](https://lh3.googleusercontent.com/t5DveiWbra5YVGYTotrspJD8jsXc7VyJ244iO8mb19E6N3Feman7vWdOoMkJ5B8o871wKwQwRTMmXEa15TROdgxhQZC3GKkvhAhHj9Hj0dhLRdBb=w1440)

图 6：允许多个效用，架起了优化方法与动力系统之间的桥梁。

EigenGame 是一个具体的例子：把机器学习问题的解设计为大型多智能体系统的输出。更一般地说，把机器学习问题设计为多智能体博弈是一个富有挑战性的机制设计问题；不过，研究者已经使用双人[零和](https://en.wikipedia.org/wiki/Zero-sum_game)博弈这一类博弈来解决机器学习问题。最著名的是，[生成对抗网络](https://papers.nips.cc/paper/2014/file/5ca3e9b122f61f8f06494c97b1afccf3-Paper.pdf)（GAN）作为生成建模方法的成功，推动了人们对博弈论与机器学习之间关系的兴趣。

EigenGame 超越了这一点，进入更复杂的多玩家、一般和（general-sum）设定。这带来了更明显的并行性，从而获得更大的规模与更快的速度。它也为社区提供了一个定量基准，可以在更丰富的领域（例如 [Diplomacy](https://deepmind.com/research/publications/Learning-to-Play-No-Press-Diplomacy-with-Best-Response-Policy-Iteration) 和 [Soccer](https://deepmind.com/research/publications/emergent-coordination-through-competition)）中测试新颖的多智能体算法。

我们希望这套设计效用与更新的蓝图能鼓励其他人探索这一方向，以设计新的算法、智能体和系统。我们期待看到还有哪些问题可以被表述为博弈，以及我们获得的洞见能否进一步加深我们对智能之多智能体本质的理解。

更多细节请参阅我们的论文 [EigenGame: PCA as a Nash Equilibrium](https://openreview.net/forum?id=NzTU59SYbNq) 及后续工作 [EigenGame Unloaded: When playing games is better than optimising](https://arxiv.org/abs/2102.04152)。

**注释**

本博文基于与 Thore Graepel 的共同工作，他是 DeepMind 的研究组长，也是伦敦大学学院的机器学习讲席教授。

我们感谢 Rob Fergus 对本文的技术反馈，感谢 Sean Carlson、Jon Fildes、Dominic Barlow、Mario Pinto 和 Emma Yousif 协调完成了这一切。

定制插图由 Jim Kynvin 和 Adam Cain 绘制。
