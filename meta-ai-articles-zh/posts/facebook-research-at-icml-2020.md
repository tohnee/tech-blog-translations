---
title: "Facebook 研究团队在 ICML 2020"
title_en: "Facebook research at ICML 2020"
date: 2020-07-10
source: https://ai.facebook.com/blog/facebook-research-at-icml-2020
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 研究团队在 ICML 2020

> 原文：[Facebook research at ICML 2020](https://ai.facebook.com/blog/facebook-research-at-icml-2020) · Meta AI（Wayback 存档）

2020 年 7 月 10 日

来自世界各地的机器学习专家将线上齐聚 2020 年国际机器学习会议（ICML），展示机器学习理解的最新进展。Facebook 的研究将以预录视频加现场问答的形式展示。Facebook 的研究员还将在多个线上研讨会演讲。例如，Arthur Szlam 将在首届强化学习研讨会上演讲；Tim Rocktäschel 将在「人工开放世界中的学习」研讨会——一个聚焦现实场景机器学习的研讨会——上演讲。作为促进领域多元化承诺的一部分，Facebook AI 还联合赞助女性机器学习「反研讨会」（Un-Workshop，讨论主要由参与者驱动），Francisco Guzman 将在 Latinx in AI 研讨会上演讲。参加 ICML 的人请关注我们的 Twitter 频道以获取最新消息。关于 Facebook AI 在 ICML 的更多信息，请查看我们的网站。

## Facebook 在 ICML 上展示的研究

**面向非自回归机器翻译的对齐交叉熵（Aligned cross entropy for non-autoregressive machine translation）**
Marjan Ghazvininejad、Vladimir Karpukhin、Luke Zettlemoyer、Omer Levy
非自回归机器翻译模型通过允许并行预测整个目标序列显著加速解码。然而，由于模型中缺乏自回归因子，建模词序更具挑战性。使用交叉熵损失的训练加剧了这一困难——它会对词序的轻微偏移施加严重惩罚。在本文中，我们提出对齐交叉熵（AXE）作为训练非自回归模型的替代损失函数。AXE 使用可微动态规划，基于目标 token 与模型预测之间最佳的可能单调对齐来分配损失。基于 AXE 的条件掩码语言模型（CMLM）非单调训练在 WMT 16 英罗和 WMT 14 英德上分别提升 3 和 5 个 BLEU 点，并在一系列翻译基准上显著胜过最先进的非自回归模型。

**改进声音事件识别泛化能力的顺序自教学方法（A sequential self teaching approach for improving generalization in sound event recognition）**
Anurag Kumar、Vamsi Krishna Ithapu
机器听觉感知的一个重要问题是识别与检测声音事件。在本文中，我们提出一种顺序自教学的语音学习方法。我们的主要命题是：在弱标注和/或噪声标注数据等不利情形下学习声音更难，这些情形下单阶段学习是不够的。我们的方案是一个顺序的分阶段学习过程，能改进给定建模系统的泛化能力。我们用技术结果论证该方法，在最大的声音事件数据集 Audioset 上，我们的顺序学习方法可带来最高 9% 的性能提升。综合评估还表明，该方法提升了从已训练模型迁移知识的能力，从而在迁移学习任务上获得更好的泛化能力。

**从机器学习模型中认证移除数据（Certified data removal from machine learning models）**
Chuan Guo、Thomas Goldstein、Awni Hannun、Laurens van der Maaten
良好的数据管理要求应数据所有者请求移除数据。这就带来一个问题：一个隐式存储了训练数据信息的已训练机器学习模型，是否以及如何应受这种移除请求的影响？能否从机器学习模型中「移除」数据？我们通过定义「认证移除」来研究该问题：一个非常强的理论保证——移除数据后的模型与从未见过该数据的模型无法区分。我们为线性分类器开发了认证移除机制，并实证研究了该机制切实可行的学习设置。

**通过反向价值函数求解约束马尔可夫决策过程（Constrained Markov decision processes via reverse value functions）**
Harsh Satija、Philip Amortila、Joelle Pineau
尽管强化学习（RL）算法在仿真领域取得了巨大成功，但它们往往不能直接应用于物理系统，尤其是存在必须满足的硬约束（如安全或资源）时。在标准 RL 中，只要能最大化奖励，智能体就被激励去探索任何行为；但在现实世界中，不良行为可能以破坏学习过程本身的方式损害系统或智能体。在本工作中，我们把带约束的学习问题建模为约束马尔可夫决策过程，并给出一个新的在策略求解表述。我们方法的一个关键贡献是把累积成本约束转换为基于状态的约束。由此我们定义了一个安全策略改进算法，在确保每一步都满足约束的同时最大化回报。我们提供了智能体在保证训练全程安全的前提下收敛的理论保证，并强调了该方法的计算优势。该方法的有效性在安全导航任务与 MuJoCo 环境的安全约束版本中用深度神经网络得到了展示。

**对 Fréchet 均值求导（Differentiating through the Fréchet mean）**
Aaron Lou、Isay Katsman、Qingxuan Jiang、Serge Belongie、Ser Nam Lim、Christopher De Sa
黎曼流形上深度表示学习的最新进展，把经典深度学习操作扩展到更好地捕捉流形几何。一个可能的扩展是 Fréchet 均值——欧氏均值的推广；但由于它缺乏闭式解与易计算的导数，一直难以应用。在本文中，我们展示如何对任意黎曼流形上的 Fréchet 均值求导。然后聚焦双曲空间，我们推导出显式梯度表达式以及一个快速、准确、免超参数的 Fréchet 均值求解器。这把 Fréchet 均值完全整合进双曲神经网络流水线。为展示这一整合，我们给出两个案例研究。第一，我们把 Fréchet 均值应用于现有的双曲图卷积网络，替换其投影聚合，在高双曲性数据集上取得最先进结果。第二，为展示 Fréchet 均值泛化欧氏神经网络操作的能力，我们开发了双曲批归一化方法，带来与欧氏设置中观察到的类似的改进。

**通过拉格朗日松弛在线性二次调节器中高效乐观探索（Efficient optimistic exploration in linear-quadratic regulators via Lagrangian relaxation）**
Marc Abeille、Alessandro Lazaric
我们研究线性二次调节器（LQR）设置中的探索-利用困境。受有限 MDP 乐观算法中使用的扩展值迭代算法启发，我们提议松弛 OFU-LQ 的乐观优化，把它转化为一个约束型「扩展」LQR 问题，其中一个额外控制变量隐式地在置信区间内选择系统动力学。然后我们转到对应的拉格朗日表述并证明强对偶性。结果表明，通过求解至多 O(log(1/ε)) 个 Riccati 方程即可高效计算 ε 乐观控制器。最后，我们证明松弛原 OFU 问题不影响学习性能，从而恢复 OFU-LQ 的 Õ(√T) 遗憾。据我们所知，这是首个具有最坏情况最优遗憾保证的计算高效的基于置信度的 LQR 算法。

**涌现语言中的熵最小化（Entropy minimization in emergent languages）**
Evgeny Rahma（原文如此）、Diane Marco
研究神经智能体被联合训练以解决需要通过离散信道通信的任务时涌现的语言，正受到越来越多的关注。我们在此研究这类语言的信息论复杂度，聚焦基本的双智能体单交换设置。我们发现，在常见训练流程下，涌现语言受到一种在人类语言中也检测到的熵最小化压力：在成功通信所需范围内，通信智能体输入与消息之间的互信息被最小化。随着我们增大通信信道的离散性，这种压力被放大。此外，我们观察到更强的离散信道驱动的熵最小化带来对过拟合与对抗攻击更鲁棒的表示。最后，我们讨论这些发现对自然与人工通信系统研究的启示。

**完全并行超参数搜索：重塑空间填充（Fully parallel hyperparameter search: Reshaped space-filling）**
Camille Couprie、Olivier Teytaud、Jérémy Rapin、Morgane Rivière、Nicolas Usunie
随机搜索是最经典的完全并行超参数搜索方法，胜过网格搜索，且与空间填充设计等复杂方法几乎等价。我们证明许多方法实际上至多相差一个常数就等价。基于这些结果，考虑到保持相同搜索分布、仅放宽独立性的空间填充设计带来一致但温和的改进，我们提议重塑搜索分布。当最优值服从正态分布时，我们表明在高维中，限制为 0 处狄拉克峰的搜索分布（所有样本相等，基数为 1）实际上优于从同一正态分布中抽取的基数随维度指数增长的样本。我们由此推导出采样器的简单修改，其中一个重塑方案赢得了 Facebook 一次性优化 CEC 竞赛，并在最优值先验概率分布已知时反复胜过其他方法。在最优值先验概率分布未知的情形下，柯西对应方案表现最佳。

**神经网络的图结构（Graph structure of neural networks）**
Jiaxuan You、Jure Leskovec、Kaiming He、Saining Xie
神经网络常被表示为神经元之间的连接图。然而尽管其应用广泛，目前对神经网络图结构与预测性能之间关系的理解甚少。在这里，我们系统研究神经网络的图结构如何影响其预测性能。为此，我们开发了一种新颖的基于图的神经网络表示——关系图，其中神经网络计算的层对应沿图结构的消息交换轮次。利用这一表示，我们表明：（1）神经网络的图结构很重要；（2）关系图存在一个「最佳点」，使神经网络的预测性能显著提升；（3）神经网络的性能近似是其关系图的聚类系数与平均路径长度的平滑函数；（4）我们的发现在许多不同任务与数据集上一致；（5）可以高效识别顶尖架构；（6）表现良好的神经网络的图结构与真实生物神经网络的图结构惊人相似。我们的工作为神经架构设计与对神经网络的总体理解开辟了新方向。

**增长的动作空间（Growing action spaces）**
Gregory Farquhar、Laura Gustafson、Zeming Lin、Shimon Whiteson、Nicolas Usunier、Gabriel Synnaeve
在具有大组合动作空间等复杂任务中，随机探索可能过于低效，无法取得有意义的学习进展。在本工作中，我们使用渐进增长的动作空间课程来加速学习。我们假设环境不受我们控制，但智能体可以通过最初限制其动作空间来设定内部课程。我们的方法使用离策略强化学习同时估计多个动作空间的最优价值函数，并把数据、价值估计与状态表示从受限动作空间高效迁移到完整任务。我们在概念验证控制任务与具有大型多智能体动作空间的富有挑战的大规模《星际争霸》微管理任务上展示了方法的效力。

**时间差分学习中的干扰与泛化（Interference and generalization in temporal difference learning）**
Emmanuel Bengio、Joelle Pineau、Doina Precup
我们研究时间差分（TD）学习中泛化与干扰之间的联系。干扰被定义为两个不同梯度的内积，表示它们的对齐程度；这一量从关于神经网络、参数共享与学习动力学的多种观察中浮现为值得关注的对象。我们发现 TD 容易导向低干扰、欠泛化的参数，而在监督学习中效果似乎相反。我们假设原因可追溯到干扰与自举的动力学之间的相互作用。这得到若干实证观察支持：TD 中泛化差距与干扰的负相关、自举对干扰与目标局部连贯性的负面影响，以及 TD(0) 与 TD(λ) 与蒙特卡洛策略评估等回归任务之间信息传播速率的对比。我们希望这些新发现能指导未来发现更好的自举方法。

**面向块 MDP 的不变因果预测（Invariant causal prediction for block MDPs）**
Amy Zhang、Clare Lyle、Shagun Sodhani、Angelos Filos、Marta Kwiatkowska、Joelle Pineau、Yarin Gal、Doina Precup
跨环境泛化是强化学习算法成功应用于现实挑战的关键。在本文中，我们考虑在块 MDP（共享潜在状态空间与该空间上的动力学结构、但观测不同的环境族）中学习可泛化抽象的问题。我们借助因果推断工具，提出一种不变预测方法，学习能泛化到多环境设置中新观测的状态抽象。我们证明，对某些类别的环境，该方法以高概率输出对应于关于回报的因果特征集的状态抽象。我们进一步给出多环境设置中模型误差与泛化误差的更一般界，并在此过程中展示因果变量选择与 MDP 状态抽象框架之间的联系。我们给出实证证据，表明我们的方法在线性与非线性设置下均有效，相较单任务与多任务基线获得更好的泛化。

**以低固有贝尔曼误差学习近优策略（Learning near optimal policies with low inherent Bellman error）**
Andrea Zanette、Alessandro Lazaric、Mykel Kochenderfer、Emma Brunskill
我们在回合式强化学习中研究带近似线性动作价值函数的探索问题，采用低固有贝尔曼误差的概念——这一条件通常用于证明近似值迭代的收敛。首先，我们把该条件与其他常见框架关联，表明它比先前工作的低秩（线性）MDP 假设严格更一般。其次，我们给出一个具有高概率遗憾界 Õ(Σ_{t=1}^H d_t√K + Σ_{t=1}^H √(d_t)·IBE·√K) 的算法，其中 H 是视野，K 是回合数，IBE 是固有贝尔曼误差的值，d_t 是时间步 t 的特征维度。此外，我们通过匹配的下界表明该结果在常数与对数因子之外不可改进。这有两点重要推论：1）该算法在该设置下具有最优统计速率，而该设置比先前关于低秩 MDP 的工作更一般；2）尽管在在线设置下工作，非封闭性（以固有贝尔曼误差度量）只被 √d_t 放大。最后，该算法在 H=1 时退化为著名的 LINUCB，但探索参数的不同选择使其能处理错设的上下文线性赌博机。虽然 MDP 设置的计算可解性问题仍开放，这丰富了具有动作价值函数线性表示、且统计高效强化学习可行的 MDP 类别。

**用时间变分推断学习机器人技能（Learning robot skills with temporal variational inference）**
Tanmay Shankar、Abhinav Gupta
在本文中，我们解决从演示中无监督地发现机器人选项的问题。具体而言，我们提出一个框架，从机器人执行各种任务的演示中，联合学习低层控制策略与如何使用它们的更高层策略。通过把选项表示为连续潜在变量，我们把学习这些选项的问题框定为隐变量推断。然后我们提出基于轨迹似然时间因子分解的时间变分推断表述，使我们可以无监督地推断选项。我们在三个机器人演示数据集上展示了框架学习此类选项的能力。

**用共享摊销变分推断做元学习（Meta-learning with shared amortized variational inference）**
Ekaterina Iakovleva、Jakob Verbeek、Karteek Alahari
我们为经验贝叶斯元学习模型提出一种新颖的摊销变分推断方案，其中模型参数被视为隐变量。我们用变分自编码器方法学习以有限训练数据为条件的模型参数先验分布，并在模型参数的条件先验与变分后验分布之间共享同一摊销推断网络。后验同时利用带标注的支持集与查询数据，而条件先验仅基于带标注的支持集。我们表明，在先前基于蒙特卡洛近似的方法中，条件先验会塌缩为狄拉克德尔塔函数；相比之下，我们的变分方法防止了这种塌缩，保留了模型参数的不确定性。我们在 miniImageNet 与 FC100 数据集上评估方法，并给出展示其相对先前工作优势的结果。

**随机线性赌博机中的元学习（Meta-learning in stochastic linear bandits）**
Leonardo Cella、Alessandro Lazaric、Massimiliano Pontil
我们在随机线性赌博机任务设置中研究元学习流程。目标是在从任务分布采样的赌博机任务类上，选择平均表现良好的学习算法。受近期「学习如何学习线性回归」工作的启发，我们考虑一类实现正则化版著名 OFUL 算法的赌博机算法，其中正则化是与某个偏置向量的欧氏距离平方。我们首先研究带偏置 OFUL 算法在遗憾最小化上的收益。然后我们提出两种在「学习如何学习」设置中估计偏置的策略。我们在理论与实验上均表明，当任务数增长且任务分布方差小时，我们的策略相对孤立地学习各任务有显著优势。

**用自适应批处理与再稀疏化的近线性时间高斯过程优化（Near-linear time Gaussian process optimization with adaptive batching and resparsification）**
Alessandro Lazaric、Daniele Calandriello、Luigi Carratino、Alessandro Lazaric、Michal Valko、Lorenzo Rosasco
高斯过程（GP）是建模不确定性最成功的框架之一。然而，GP 优化（如 GP-UCB）存在严重的可扩展性问题。除非成批选择候选（如用 GP-BUCB）并并行评估，否则实验时间随评估次数线性增长。此外，计算成本往往过高，因为 GP-BUCB 等算法选择每批需要至少与维度和迭代数呈二次方的时间。在本文中，我们引入 BBKB（Batch Budgeted Kernel Bandits）——首个可证明以近线性时间运行并成批选择候选的无遗憾 GP 优化算法。这通过一个新的后验方差追踪保证实现，使 BBKB 能选择越来越大的批次，改进 GP-BUCB。此外，我们表明同一界可用于自适应地推迟 BBKB 所用稀疏 GP 近似的昂贵更新，实现近常数的每步摊销成本。这些发现在多个实验中得到确认，BBKB 比最先进方法快得多。

**目标导向强化学习中的无遗憾探索（No-regret exploration in goal-oriented reinforcement learning）**
Jean Tarbouriech、Evrard Garcelon、Michal Valko、Matteo Pirotta、Alessandro Lazaric
许多流行的强化学习问题（如迷宫导航、部分 Atari 游戏、山车）是其随机最短路径（SSP）表述下的回合式设置的实例：智能体须在最小化累积成本的同时到达目标状态。尽管该设置很流行，但在一般 SSP 问题中，探索-利用困境鲜有研究，理论文献大多聚焦不同问题（如固定视野与无限视野）或做出限制性的无环 SSP 假设（即一个回合中任何状态不能被访问两次）。在本文中，我们研究不对动力学做任何假设的一般 SSP 问题（某些策略可能永远无法到达目标）。我们引入 UC-SSP——该设置下的首个无遗憾算法，并对任意具有 S 个状态、A 个动作、正成本与 SSP 直径 D（定义为从任意起始状态到目标的最小期望命中时间）的未知 SSP，证明 K 个回合后的遗憾界为 Õ(DS√(ADK))。我们通过精心设计的新颖停止规则实现这一结果：如果当前策略耗时过长，UC-SSP 可以中断它并切换到为快速结束回合而设计的替代策略。

**用自适应量化模块的在线学习持续压缩（Online learned continual compression with adaptive quantization modules）**
Lucas Caccia、Eugene Belilovsky、Massimo Caccia、Joelle Pineau
我们引入并研究「在线持续压缩」问题：尝试同时学习压缩与存储来自非独立同分布数据流的代表性数据集，且每个样本只观察一次。在该设置中朴素应用自编码器会遇到重大挑战：从较早编码器状态导出的表示必须能被较晚的解码器状态使用。我们展示如何用离散自编码器有效应对这一挑战，并引入自适应量化模块（AQM）来控制学习任一阶段模块压缩能力的变化。这使我们能在考虑总体内存约束与已学压缩的当前进展的情况下，为传入样本选择合适的压缩率。与以往方法不同，我们的方法不需要任何预训练，即便在富有挑战的数据集上也是如此。我们表明，在持续学习设置中用 AQM 替换标准情节记忆，在图像、LiDAR 与强化学习智能体的持续学习基准上带来显著增益。

**论随机设置下 Nesterov 加速梯度法的收敛（On the Convergence of Nesterov's Accelerated Gradient Method in Stochastic Settings）**
Mido Assran、Michael Rabbat
我们在随机近似设置（无偏梯度且方差有界）与有限和设置（随机性来自 mini-batch 采样）中，研究带常数步长与动量参数的 Nesterov 加速梯度法。为更好地理解 Nesterov 方法在随机设置中的行为，我们始终聚焦光滑、强凸且二阶连续可微的目标。在随机近似设置中，Nesterov 方法以与确定性设置相同的加速速率收敛到最优点的一个邻域。也许令人惊讶的是，在有限和设置中，我们证明 Nesterov 方法在常规步长与动量选择下可能发散，除非满足与条件数和数据一致性相关的额外问题条件。我们的结果阐明了 Nesterov 方法在有限和设置中可能无法收敛或无法加速的原因。

**面向零样本协调的「他者博弈」（"Other-play" for zero-shot coordination）**
Hengyuan Hu、Adam Lerer、Alex Peysakhovich、Jakob Foerster
我们考虑零样本协调问题——构建能与未曾见过的新伙伴（如人类）协调的 AI 智能体。标准多智能体强化学习（MARL）方法通常聚焦自我博弈（SP）设置：智能体通过与自己反复对局来构建策略。遗憾的是，把 SP 朴素地应用于零样本协调问题，可能产生建立了高度特化惯例的智能体，这些惯例无法迁移到未与之训练过的新伙伴。我们引入一个名为「他者博弈」（other-play，OP）的新学习算法，通过寻找更鲁棒的策略来增强自我博弈。我们从理论与实验两方面刻画 OP。我们研究合作牌类游戏 Hanabi，表明 OP 智能体与独立训练的智能体以及人类玩家配对时，得分都高于 SP 智能体。

**面向光滑博弈的随机哈密顿梯度方法（Stochastic Hamiltonian gradient methods for smooth games）**
Nicolas Loizou、Hugo Berard、Alexia Jolicoeur-Martineau、Pascal Vincent、Simon Lacoste-Julien、Ioannis Mitliagkas
光滑博弈的分析受到对抗式表述成功的推动而备受关注。哈密顿方法是一种轻量级的二阶途径，把问题重新表述为最小化目标。共识优化可视为其推广：它把哈密顿项与原博弈动力学混合。这一族哈密顿方法在文献中显示出前景，但对随机博弈没有保证。经典的随机额外梯度与 mirror-prox 方法需要在紧域上平均才能收敛。近期的方差缩减一阶方案聚焦无界域，但止步于证明双线性矩阵博弈的最后迭代收敛。我们分析随机哈密顿方法及其新颖的方差缩减变体，为随机无界双线性博弈提供首组最后迭代收敛保证。更一般地，我们为一族随机博弈（特别包括某些非凸博弈）提供收敛保证。我们用随机双线性博弈实验（其中我们的理论被证明是紧的）与简单的对抗机器学习表述来补充分析。

**有限宽度与输入维度下深度整流网络中的学生特化（Student Specialization in Deep Rectified Networks With Finite Width and Input Dimension）**
Yuandong Tian
我们考虑一个深度 ReLU/Leaky ReLU 学生网络，用随机梯度下降（SGD）从固定同深度教师网络的输出训练。学生网络是「过实现」的：在每一层 l，学生节点数 n_l 多于教师的 m_l。在关于数据集与教师网络的温和条件下，我们证明当每个数据样本上的梯度都很小时，每个教师节点在「最低层」被至少一个学生节点「特化」。对两层网络，这种特化可以通过在任意「多项式」规模（K^{5/2}d^3ε^{-1}）的数据集上训练、直到梯度幅值降到 ε/(K^{3/2}√d) 来实现。这里 d 是输入维度，K=m_1+n_1 是教师与学生最低层的总神经元数。注意，我们需要特定形式的数据增强，样本复杂度包含增强产生的额外数据。据我们所知，我们是首个在教师-学生设置中给出有限深度与宽度的两层（Leaky）ReLU 网络学生特化的多项式样本复杂度、以及多层情形最低层特化有限复杂度的工作，且不需要对输入的参数化假设（如高斯）。我们的理论表明，具有大扇出权重的教师节点会在梯度仍大时先被特化，其他节点则在梯度小时被特化，这暗示了训练中的归纳偏置。这塑造了此前多项工作经验观察到的训练阶段。合成数据与 CIFAR10 上的实验验证了我们的发现。代码已在 GitHub 发布：https://github.com/facebookresearch/luckmatters。

**可微交叉熵方法（The differentiable cross-entropy method）**
Brandon Amos、Denis Yarats
我们研究用于连续参数化目标函数非凸优化的交叉熵方法（CEM），并引入一个可微变体，使我们能对 CEM 的输出关于目标函数参数求导。在机器学习设置中，这把 CEM 带入了此前不可能的端到端学习流水线。我们展示在合成基于能量的结构预测任务与非凸连续控制中的应用。在控制设置中，我们展示如何把最优动作序列嵌入低维空间。这使我们能通过对基于 CEM 的控制器求导、用策略优化微调建模组件。

**用解耦上下文 transformer 做并行机器翻译（Parallel machine translation with disentangled context transformer）**
Jungo Kasai、James Cross、Marjan Ghazvininejad、Jiatao Gu
最先进的神经机器翻译模型从左到右生成翻译，每一步都以先前生成的 token 为条件。这种生成过程的序列性带来推断中的根本延迟，因为我们无法并行生成句子中的多个 token。我们提出一个基于注意力掩码的模型——解耦上下文（DisCo）transformer，能在给定不同上下文时同时生成所有 token。DisCo transformer 被训练为在给定其余参考 token 的任意子集时预测每个输出 token。我们还开发了并行「先易后难」推断算法，迭代地并行精化每个 token 并减少所需迭代次数。我们在七个不同数据规模方向上的大量实验表明，我们的模型与非自回归机器翻译的最先进水平相比取得有竞争力甚至更好的性能，同时平均显著减少解码时间。

**未知数量多说话人的语音分离（Voice separation with an unknown number of multiple speakers）**
Eliya Nachmani、Yossef Mordechay Adi、Lior Wolf
我们提出一种分离混合音频序列的新方法，其中多个声音同时说话。新方法采用门控神经网络，经训练在多个处理步骤中分离声音，同时保持每个输出通道中的说话人固定。为每个可能的说话人数训练一个不同的模型，并用说话人数最多的模型来选择给定样本中的实际说话人数。我们的方法大幅胜过当前最先进水平——正如我们所示，后者在超过两个说话人时已无竞争力。

**用字母到词编码器的词级语音识别（Word-level speech recognition with a letter to word encoder）**
Ronan Collobert、Awni Hannun、Gabriel Synnaeve
我们提出一个直接到词的序列模型，用一个词网络从字母学习词嵌入。词网络可与任意序列模型无缝集成，包括连接时序分类与带注意力的编码器-解码器模型。我们表明，直接到词模型在语音识别上相对子词级模型能取得词错误率增益。我们还表明，直接到词方法保留了预测训练时未见词的能力而无需任何重训。最后，我们证明词级模型可以在保持精度的同时使用比子词级模型更大的步长，这使模型在训练与推断上都更高效。

## Facebook 在 ICML 的研讨会与问答

- **Latinx in AI 研讨会**，7 月 13 日，美国东部时间 7:30——Francisco Guzman 为讲者
- **女性机器学习反研讨会（Un-Workshop）**，7 月 13 日，GMT 6:00——Facebook AI 赞助该研讨会，Kalesha Bullard 演讲
- **PyTorch 实时问答**，7 月 15 日——全天 PyTorch 实时问答，日程可通过 Facebook AI 虚拟展位查看
- **持续学习研讨会**，7 月 17 日——David Lopez-Paz 为组织委员会成员
- **音频与语音中的自监督**，7 月 17 日，GMT 7:05——Lorenzo Torresani 为讲者
- **极限分类研讨会：理论与应用**，7 月 17 日，美国东部时间 9:00——Tomas Mikolov 为讲者
- **第 1 届强化学习中的语言研讨会（LaReL）**，7 月 18 日，美国东部时间 10:00——Jakob Foerster、Edward Grefenstette、Tim Rocktäschel 为组织委员会成员，Arthur Szlam 为讲者
- **终身学习研讨会**，7 月 18 日，美国东部时间 5:00——Shagun Sodhani 与 Koustuv Sinha 为组织委员会成员
- **人工开放世界中的学习研讨会**，7 月 18 日，美国东部时间 10:00——Kavya Srinet 与 Arthur Szlam 为组织委员会成员，Tim Rocktäschel 为讲者
- **MLRetrospectives：机器学习研究的自我反思场所**，2020 年 7 月 18 日，美国东部时间 9:00——Joelle Pineau 为组织者
