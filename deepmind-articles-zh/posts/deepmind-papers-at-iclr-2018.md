---
title: "DeepMind 在 ICLR 2018 发表的论文"
title_en: "DeepMind papers at ICLR 2018"
source: https://deepmind.google/blog/deepmind-papers-at-iclr-2018/
site: deepmind
date: 2018-04-26
crawled: 2026-09-13
translated: 2026-09-13
---

# DeepMind 在 ICLR 2018 发表的论文

> 原文：[DeepMind papers at ICLR 2018](https://deepmind.google/blog/deepmind-papers-at-iclr-2018/) · Google DeepMind

**4月30日至5月3日，数百名研究人员和工程师将齐聚加拿大温哥华，参加[第六届国际学习表征会议（ICLR）](https://iclr.cc/)。**

在这里，你可以了解 DeepMind 所有入选论文的详情，并找到相应海报展示和口头报告的场次信息。

### 最大后验策略优化（Maximum a posteriori policy optimisation）

**作者：** Abbas Abdolmaleki、Jost Tobias Springenberg、Nicolas Heess、Yuval Tassa、Remi Munos

我们提出了一种新的强化学习算法，称为最大后验策略优化（MPO），它建立在相对熵目标上的坐标上升之上。我们证明，若干现有方法可以直接与我们的推导联系起来。我们开发了两个离策略（off-policy）算法，并证明它们与深度强化学习领域最先进的方法相比具有竞争力。特别是在连续控制任务上，我们的方法在样本效率、过早收敛以及对超参数设置的鲁棒性方面均优于现有方法。

- 阅读[论文](https://openreview.net/forum?id=S1ANxQW0b)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 11:00–13:00

### 面向高效架构搜索的分层表征（Hierarchical representations for efficient architecture search）

**作者：** Hanxiao Liu（CMU）、Karen Simonyan、Oriol Vinyals、Chrisantha Fernando、Koray Kavukcuoglu

我们探索了高效的神经架构搜索方法，并证明一个简单而强大的进化算法可以发现性能优异的新架构。我们的方法将一种新颖的分层遗传表征方案——它模仿了人类专家通常采用的模块化设计模式——与支持复杂拓扑结构的、表达力丰富的搜索空间相结合。我们的算法高效地发现了一系列在图像分类任务上超越大量人工设计模型的架构，在 CIFAR-10 上取得 3.6% 的 top-1 错误率，迁移到 ImageNet 上为 20.3%，与现有最佳的神经架构搜索方法相比具有竞争力。我们还给出了使用随机搜索的结果：在 CIFAR-10 上 top-1 准确率仅低 0.3%、在 ImageNet 上仅低 0.1%，同时把搜索时间从 36 小时缩短到 1 小时。

- 阅读[论文](https://arxiv.org/abs/1711.00436)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 11:00–13:00

### 为可迁移的机器人技能学习嵌入空间（Learning an embedding space for transferable robot skills）

**作者：** Karol Hausman、Jost Tobias Springenberg、Ziyu Wang、Nicolas Heess、Martin Riedmiller

我们提出了一种方法，对经由技能嵌入空间参数化的紧密相关技能进行强化学习。我们利用隐变量，并借助强化学习与变分推断之间的联系来学习这类技能。

我们工作的主要贡献是面向分层策略的熵正则化策略梯度形式，以及与之配套的、基于随机价值梯度的高数据效率和鲁棒的离策略梯度算法。我们在多个模拟机器人操作任务上验证了该方法的有效性。

- 阅读[论文](https://openreview.net/forum?id=rk07ZXZRb)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 11:00–13:00

### 学习觉知模型（Learning awareness models）

**作者：** Brandon Amos、Laurent Dinh、Serkan Cabi、Thomas Rothörl、Sergio Gómez Colmenarejo、Alistair M Muldal、Tom Erez、Yuval Tassa、Nando de Freitas、Misha Denil

我们证明，被训练来预测智能体身体本体感觉信息的模型，会逐渐表征外部世界中的物体。这些模型能够成功预测未来 100 步以上的传感器读数，并且在失去接触之后仍能继续表征外部物体的形状。我们证明，通过最大化未来传感器读数的不确定性来进行主动数据收集，可以得到在用于控制时表现更优的模型。我们还从一只真实的机器人手上采集了数据，并证明同样的模型可用于回答有关现实世界中物体属性的问题。

- 阅读[论文](https://openreview.net/forum?id=r1HhRfWRZ)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 11:00–13:00

### 面向循环神经网络的 Kronecker 分解曲率近似（Kronecker-factored curvature approximations for recurrent neural networks）

**作者：** James Martens、Jimmy Ba（Vector Institute）、Matthew Johnson（Google）

Kronecker 因子近似曲率（K-FAC）（Martens & Grosse，2015）是一种二阶优化方法，已被证明能在大规模神经网络优化任务上取得最先进的性能（Ba 等，2017）。它建立在对费舍尔信息矩阵（FIM）的近似之上，并对网络的特定结构及其参数化方式做出了假设。原始的 K-FAC 方法只适用于全连接网络，不过 Grosse & Martens（2016）近来已将其扩展到卷积网络。在这项工作中，我们通过为 RNN 引入一种新颖的 FIM 近似，把该方法扩展到循环神经网络。这一近似的做法是：用链式结构的线性高斯图模型对不同时间步的梯度贡献之间的协方差结构建模，对各个互协方差求和，并以闭式解计算其逆。实验表明，在若干有挑战性的 RNN 训练任务上，我们的方法显著优于带动量 SGD 和 Adam 等通用最先进优化器。

- 阅读[论文](https://openreview.net/forum?id=HyMTkQZAb¬eId=HkIsQkpSG)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 11:00–13:00

### 分布式分布式确定性策略梯度（Distributed distributional deterministic policy gradients）

**作者：** Gabriel Barth-maron、Matthew Hoffman、David Budden、Will Dabney、Daniel Horgan、Dhruva Tirumala Bukkapatnam、Alistair M Muldal、Nicolas Heess、Timothy Lillicrap

本工作采纳了在强化学习中非常成功的分布式（distributional）视角，并将其适配到连续控制场景。我们将其整合进一个离策略学习的分布式框架中，提出了我们所说的分布式分布式深度确定性策略梯度算法（D4PG）。我们还将这一技术与若干额外的简单改进相结合，例如使用 N 步回报和优先经验回放。在实验中，我们逐一考察了每个组件的贡献，展示了它们之间如何相互作用，以及它们的综合贡献。我们的结果表明，在各种简单的控制任务、困难的操作任务以及一组困难的基于障碍物的移动任务上，D4PG 算法都达到了最先进的性能。

- 阅读[论文](https://openreview.net/forum?id=SyZipzbCb)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 16:30–18:30

### Kanerva 机器：生成式分布式记忆（The Kanerva Machine: A generative distributed memory）

**作者：** Yan Wu、Greg Wayne、Alex Graves、Timothy Lillicrap

我们提出了一种端到端训练的记忆系统，它能快速适应新数据并生成类似的新样本。该记忆具有解析可处理性，可通过贝叶斯更新规则实现最优的在线压缩。我们将其形式化为一个分层条件生成模型，其中记忆提供了一个丰富的、依赖数据的先验分布。由此，自上而下的记忆与自下而上的感知相结合，共同产生表示观测的编码。

- 阅读[论文](https://arxiv.org/abs/1804.01756)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 16:30–18:30

### 基于记忆的参数自适应（Memory-based parameter adaptation）

**作者：** Pablo Sprechmann、Siddhant Jayakumar、Jack Rae、Alexander Pritzel、Adria P Badia · Benigno Uria、Oriol Vinyals、Demis Hassabis、Razvan Pascanu、Charles Blundell

人类和动物能够从少量样例中快速吸收新知识，并在其一生中的大部分时间里不断这样做。相比之下，基于神经网络的模型依赖数据分布保持平稳，并通过渐进的训练过程来获得良好的泛化。我们从互补学习系统理论中获得启发，提出了基于记忆的参数自适应（MbPA）——一种用情景记忆增强神经网络的方法，使其能够快速获取新知识，同时保持标准深度模型的高性能和良好泛化。MbPA 把样例存储在记忆中，然后使用基于上下文的查找来直接修改神经网络的权重。它缓解了神经网络的若干缺陷，例如灾难性遗忘；同时支持新知识的快速、稳定习得，以及在评估阶段的快速学习。

- 阅读[论文](https://arxiv.org/abs/1802.10542)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 16:30–18:30


### SCAN：学习分层组合式的视觉概念（SCAN: Learning hierarchical compositional visual concepts）

**作者：** Irina Higgins、Nicolas Sonnerat、Loic Matthey、Arka Pal、Christopher P Burgess、Matko Bošnjak、Murray Shanahan、Matthew Botvinick、Alexander Lerchner

我们提出了一种新颖的理论方法，以解决抽象组合性问题——我们如何学习少量的、有锚定基础的构建模块，并用它们即时生成大量新的抽象概念？我们提出了一种名为符号-概念关联网络（Symbol-Concept Association Network，SCAN）的新神经网络架构，它能够学习有锚定基础的视觉概念层级，从而在语言指令的引导下想象新概念。

- [阅读完整博客](https://deepmind.com/blog/article/imagine-creating-new-visual-concepts-recombining-familiar-ones)。
- 阅读[论文](https://arxiv.org/abs/1707.03389)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 11:00–13:00

### 从符号与像素输入的指称博弈中涌现语言交流（Emergence of linguistic communication from referential games with symbolic and pixel input）

**作者：** Angeliki Lazaridou、Karl M Hermann、Karl Tuyls、Stephen Clark

算法演化或学习（组合式）交流协议的能力，传统上是在语言演化文献中通过涌现通信任务来研究的。在这里，我们使用当代深度学习方法，并在指称交流博弈上训练强化学习神经网络智能体，从而扩展了这一研究。此前的工作中智能体在符号环境中训练，我们则进一步开发出能够从原始像素数据中学习的智能体——这是一种更具挑战性也更贴近现实的输入表示。我们发现输入数据的结构化程度会影响涌现协议的性质，从而印证了如下假说：当智能体感知到世界具有结构时，结构化的组合式语言最有可能涌现。

- 阅读[论文](https://openreview.net/pdf?id=HJGv1Z-AW)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 11:00–13:00
- 参加 **5月2日（周三）** 在 Exhibition Hall A 举行的口头报告，时间 10:15–10:30

### 通往均衡的多条路径：GAN 无需在每一步都减小散度（Many paths to equilibrium: GANs do not need to decrease a divergence at every step）

**作者：** William Fedus（Université de Montréal）、Mihaela Rosca、Balaji Lakshminarayanan、Andrew Dai（Google）、Shakir Mohamed、Ian Goodfellow（Google Brain）

生成对抗网络（GAN）研究领域不断壮大，其背后是它们在计算机视觉中应用的成功。为了解决 GAN 的训练不稳定问题，已有多种关于训练动力学的理论解释被提出，新的训练方法也层出不穷。通过聚焦于 GAN 的散度最小化视角以及梯度惩罚等正则化手段，我们从经验上证明：其中一些方法的成功无法仅凭其配套的底层理论来解释。这促使我们需要一个新的理论框架，以涵盖并解释这些结果。

- 阅读[论文](https://arxiv.org/abs/1710.08446)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 16:30–18:30

### 神经网络能理解逻辑蕴涵吗？（Can neural networks understand logical entailment?）

**作者：** Richard Evans、David Saxton、David Amos、Pushmeet Kohli、Edward Grefenstette

我们引入了一个新的逻辑蕴涵数据集，用以在蕴涵预测任务上衡量模型捕捉并利用逻辑表达式结构的能力。我们利用这一任务比较了序列处理文献中一系列常见架构，以及一个新的模型类别——PossibleWorldNets——它把蕴涵计算为「在可能世界上的卷积」。结果表明：相对于 LSTM 循环神经网络，卷积网络对这类问题具有错误的归纳偏置；树结构神经网络因能更好地利用逻辑语法而优于 LSTM 循环神经网络；而 PossibleWorldNets 则超越了所有基准。

- 阅读[论文](https://openreview.net/forum?id=SkZxCk-0Z)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 16:30–18:30

### 分布式优先经验回放（Distributed prioritized experience replay）

**作者：** Daniel Horgan、John Quan、David Budden、Gabriel Barth-maron、Matteo Hessel、Hado van Hasselt、David Silver

我们提出了一种面向大规模深度强化学习的分布式架构，使智能体能够从比以往多出几个数量级的数据中有效学习。该算法将行动与学习解耦：行动者（actor）按照一个共享的神经网络选择动作，与各自的环境实例交互，并将产生的经验累积到共享的经验回放存储中；学习者（learner）对经验样本进行回放并更新神经网络。该架构依赖优先经验回放，只聚焦于行动者产生的最重要的数据。我们的架构显著提升了 Arcade Learning Environment 上的最先进水平，用一小部分实际训练时间取得了更好的最终性能。

- 阅读[论文](https://arxiv.org/abs/1803.00933)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 16:30–18:30

### The Reactor：一个快速且样本高效的强化学习 actor-critic 智能体（The Reactor: A fast and sample-efficient actor-critic agent for reinforcement learning）

**作者：** Audrunas Gruslys、Will Dabney、Mohammad Gheshlaghi Azar、Bilal Piot、Marc G Bellemare、Remi Munos

我们提出了多项算法和架构上的改进，所得到的智能体样本效率高于 Prioritized Dueling DQN 和 Categorical DQN，同时运行时性能优于 A3C。分布式 Retrace 策略评估算法把多步离策略更新带入了分布式强化学习场景。我们的方法可用于把多类多步策略评估算法转换为分布式版本。β-留一（β-leave-one-out）策略梯度算法使用动作价值作为基线。新的优先回放算法利用时间局部性实现更高效的回放优先级。Reactor 在不到一天的时间内经过 2 亿帧训练即达到最先进性能。

- 阅读[论文](https://arxiv.org/abs/1704.04651)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 16:30–18:30

### 最小冗余拉普拉斯特征映射（Minimally Redundant Laplacian Eigenmaps）

**作者：** David Pfau、Christopher P Burgess

用于学习低维数据流形的谱方法近年来已在很大程度上被深度学习方法取代。原因之一是经典的谱流形学习方法常常学到坍缩的嵌入，无法充满嵌入空间。我们证明，这是不同隐变量维度在观测空间中标度差异悬殊时数据的自然结果。我们提出了拉普拉斯特征映射的一个简单扩展来修复这一问题：选择既相互正交、又对嵌入的其他维度 \textit{minimally redundant}（最小冗余）的嵌入向量。在 NORB 和相似度变换人脸数据上的实验中，我们证明最小冗余拉普拉斯特征映射（MR-LEM）显著提升了嵌入向量的质量，准确恢复了数据的隐含拓扑，并发现了大量解耦的变化因子，其质量可与最先进的深度学习方法媲美。

- 阅读[论文](https://iclr.cc/Conferences/2018/Schedule?showEvent=475)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 16:30–18:30


### 论单个方向对泛化的重要性（On the importance of single directions for generalization）

**作者：** Ari Morcos、David GT Barrett、Neil C Rabinowitz、Matthew Botvinick

我们对单个方向对泛化重要性的研究……采用了一种受数十年实验神经科学启发的方法——考察损伤带来的影响——来回答：深度神经网络中的小群神经元有多重要？更易解释的神经元对网络的计算是否也更重要？我们通过删除单个神经元和成组神经元来测量损伤网络对性能的影响。实验带来了两个出人意料的发现：1. 尽管此前许多研究聚焦于理解易解释的单个神经元（例如「猫神经元」，即深度网络隐藏层中只对猫的图像才激活的神经元），我们发现这些可解释神经元并不比那些活动难以解读的「令人困惑的神经元」更重要。2. 能正确分类未见图像的网络比只能分类见过的图像的网络更能抵抗神经元删除。换言之，泛化良好的网络远没有死记硬背的网络那样依赖单个方向。

- [阅读完整博客](https://deepmind.com/blog/article/understanding-deep-learning-through-neuron-deletion)。
- 阅读[论文](https://openreview.net/forum?id=r1iuQjxCZ¬eId=r1On1W5xf)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 11:00–13:00

### 循环神经网络语言模型中的记忆架构（Memory architectures in recurrent neural network language models）

**作者：** Dani Yogatama、Yishu Miao、Gábor Melis、Wang Ling、Adhiguna Kuncoro、Chris Dyer、Phil Blunsom

生成流畅且合乎语法的语言，需要追踪过去已生成了哪些词。本文比较了三种记忆架构（顺序存取、随机存取和基于栈），发现栈结构记忆在留出困惑度（held-out perplexity）上表现最佳。为了让栈记忆更强大、更好地匹配语言中的现象，我们引入了对现有可微栈记忆的推广，使其能在每个时间步执行多次弹出（pop）操作，进一步提升了性能。最后，我们证明栈增强语言模型能够正确学会预测常规 LSTM 语言模型难以处理的长程一致性模式。

- 阅读[论文](https://openreview.net/forum?id=SkFqf0lAZ)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 11:00–13:00

### 少样本自回归密度估计：迈向学习如何学习分布（Few-shot autoregressive density estimation: Towards learning to learn distributions）

**作者：** Scott Reed、Yutian Chen、Thomas Paine、Aaron van den Oord、S. M. Ali Eslami、Danilo J Rezende、Oriol Vinyals、Nando de Freitas

当前的图像密度模型训练需要大量数据和计算时间。本文展示了如何将 1) 神经注意力与 2) 元学习技术同自回归模型相结合，实现有效的少样本密度估计。我们改进的 PixelCNN 在 Omniglot 上取得了最先进的少样本密度估计结果。我们对学到的注意力策略进行了可视化，发现它无需监督就为图像镜像和 Omniglot 数字绘制等简单任务学到了直观的算法。最后，我们在 Stanford Online Products 数据集上演示了少样本图像生成。

- 阅读[论文](https://arxiv.org/abs/1710.10304)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 11:00–13:00

### 论神经语言模型评测的现状（On the state of the art of evaluation in neural language models）

**作者：** Gábor Melis、Chris Dyer、Phil Blunsom

循环神经网络架构的不断推陈出新，为语言建模基准带来了一波又一波号称最先进的结果。然而，这些结果是在不同的代码库和有限的计算资源下评估的，构成了不受控制的实验变异来源。我们借助大规模自动化黑盒超参数调优重新评估了若干流行架构和正则化方法，得出了一个有些出人意料的结论：标准的 LSTM 架构在恰当正则化后优于更新的一些模型。我们在 Penn Treebank 和 Wikitext-2 语料上建立了新的最先进水平，并在 Hutter Prize 数据集上给出了强基线。

- 阅读[论文](https://arxiv.org/abs/1707.05589)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 11:00–13:00

### 通过谈判涌现交流（Emergent communication through negotiation）

**作者：** Kris Cao、Angeliki Lazaridou、Marc Lanctot、Joel Z Leibo、Karl Tuyls、Stephen Clark

多智能体强化学习为研究交流如何在需要解决特定问题的智能体社群中涌现提供了一条途径。本文研究谈判环境——一种半合作的智能体交互模型——中交流的涌现。我们引入了两种通信协议：一种锚定于博弈的语义，另一种先验地无锚定，属于「廉价磋商（cheap talk）」的一种形式。我们证明，自利的智能体可以利用预先锚定的通信信道进行公平谈判，却无法有效使用无锚定的信道；而亲社会智能体确实学会了利用廉价磋商找到最优谈判策略，这表明合作是语言涌现的必要条件。我们还研究了一个智能体与具有不同亲社会程度的社群中的智能体交互时的交流行为，并展示了智能体的可识别性如何有助于谈判。

- 阅读[论文](https://openreview.net/forum?id=Hk6WhagRW)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 16:30–18:30


### 从原始视觉输入中进行组合式 obverter 交流学习（Compositional obverter communication learning from raw visual input）

**作者：** Edward Choi、Angeliki Lazaridou、Nando de Freitas

人类语言的显著特征之一是其组合性，它让我们能够用有限的词汇描述复杂的环境。此前有研究表明，基于解耦的输入（例如人工设计的特征），神经网络智能体可以学会用一种高度结构化、可能是组合式的语言进行交流。然而，人类并不是基于被充分概括的特征来学习交流的。在这项工作中，我们训练神经智能体同时从原始图像像素发展视觉感知，并学习用一串离散符号进行交流。智能体玩一个图像描述博弈，图像中包含颜色、形状等因子。我们使用 obverter 技术训练智能体：智能体通过内省生成能使自身理解最大化的消息。通过定性分析、可视化以及零样本测试，我们证明在环境施加适当压力的条件下，智能体能够从原始图像像素发展出具有组合性特征的语言。

- 阅读[论文](https://arxiv.org/abs/1804.02341)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 11:00–13:00

### 用于探索的噪声网络（Noisy networks for exploration）

**作者：** Meire Fortunato、Mohammad Gheshlaghi Azar、Bilal Piot、Jacob Menick、Matteo Hessel、Ian Osband、Alex Graves、Volodymyr Mnih、Remi Munos、Demis Hassabis、Olivier Pietquin、Charles Blundell、Shane Legg

我们提出了 NoisyNet——一种在权重中加入参数化噪声的深度强化学习智能体——并证明由此带来的策略随机性可用于促进高效探索。噪声的参数与网络其余权重一起通过梯度下降学习。NoisyNet 实现简单，几乎不增加计算开销。我们发现，用 NoisyNet 替换 A3C、DQN 和 dueling 智能体的常规探索启发式（分别为熵奖励和 ε-greedy），可在大量 Atari 游戏上取得显著更高的分数，在某些情况下使智能体从低于人类的水平跃升至超越人类的水平。

- 阅读[论文](https://arxiv.org/abs/1706.10295)
- 海报展示位于 East Meeting 层 1、2、3 区域，时间 16:30–18:30
