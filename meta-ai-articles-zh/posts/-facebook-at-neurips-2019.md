---
title: "Facebook 在 NeurIPS 2019 上的研究"
title_en: "Facebook at NeurIPS 2019"
date: 2019-03-15
source: https://ai.meta.com/blog/-facebook-at-neurips-2019/
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 在 NeurIPS 2019 上的研究

> 原文：[Facebook at NeurIPS 2019](https://ai.meta.com/blog/-facebook-at-neurips-2019/) · Meta AI（Wayback 存档）

2019 年神经信息处理系统大会（NeurIPS）将于 12 月 8 日（周日）至 12 月 14 日（周六）在加拿大不列颠哥伦比亚省温哥华举行。NeurIPS 拥有超过 15000 名参会者，是 AI 领域规模最大的会议，机器学习与神经科学专家将从世界各地赶来讨论该领域的最新进展。Facebook 在 AI、核心数据科学、网络与基础设施、增强与虚拟现实等领域的研究者和工程师将在会议的海报环节、亮点报告、研讨会（workshop）和教程中展示他们的研究。我们还将启动 Deepfake 检测挑战赛（Deepfake Detection Challenge）。从周日上午到周三晚上，参会者可以到 Facebook 展台与研究者见面、体验演示和教程，并与我们的招聘团队交流。周二下午，参会者可以参加 AI Residency 计划与应用流程的问答，与 AI Residency 计划的驻留者和导师面对面。今年，Facebook 对 NeurIPS Expo 的贡献是以 PyTorch 为主题的研讨会：Multi-modal Research to Production with PyTorch and Facebook 与 Responsible and Reproducible AI with PyTorch and Facebook。为持续支持 AI 领域的多样性，我们也在周日和周一支持 Women in AI、Black in AI 和 Latinx in AI 研讨会。请访问我们的 NeurIPS 2019 活动页面，了解演示和展台活动的更多细节，以及 Facebook 在 NeurIPS 2019 的更多信息。NeurIPS 上展示研究的完整逐日日程（含研讨会和教程等活动）可在此处查阅。

## Facebook 在 NeurIPS 上展示的研究

**A structured prediction approach for generalization in cooperative multi-agent reinforcement learning**
（合作多智能体强化学习中泛化的结构化预测方法）
Nicolas Carion、Nicolas Usunier、Gabriel Synnaeve、Alessandro Lazaric
有效的协调对解决多智能体协作（MAC）问题至关重要。虽然集中式强化学习方法可以最优地解决小规模 MAC 实例，但它们无法扩展到大型问题，也无法泛化到与训练时所见不同的场景。本文考虑具有某种内在局部性概念（如地理邻近性）的 MAC 问题，使得智能体与任务之间的交互在局部受限。利用这一性质，我们引入了一种新颖的结构化预测方法来把智能体分配给任务。在每一步，该分配都通过求解一个集中式优化问题（推断过程）得到，其目标函数由一个学习到的评分模型参数化。我们提出了推断过程与评分模型的多种组合，能够表示复杂度递增的协调模式。由此得到的分配策略可以在小规模问题实例上高效学习，并直接复用于智能体和任务更多的问题（即零样本泛化）。我们报告了在一个玩具级搜索救援问题以及《星际争霸：母巢之战》（StarCraft: Brood War）多个目标选择场景上的实验结果，在智能体和任务数量达到训练时五倍的实例上，我们的模型显著优于强大的基于规则的基线。

**Anti-efficient encoding in emergent communication**
（涌现通信中的反高效编码）
Rahma Chaabouni、Eugene Kharitonov、Emmanuel Dupoux、Marco Baroni
尽管基于神经网络的涌现语言模拟重新受到关注，人们对所诱导编码的基本性质及其与人类语言的比较仍知之甚少。人类语言的一个基本特征是齐夫缩略律（Zipf's Law of Abbreviation，ZLA）：更频繁的词高效地对应更短的字符串。我们研究了当两个神经网络——一个「说话者」和一个「听者」——被训练来玩传讯游戏时是否会涌现同样的模式。出人意料的是，我们发现网络发展出了一种反高效的编码方案：最频繁的输入对应最长的消息，而且消息整体偏向最大长度阈值。这种反高效编码似乎对听者来说更容易区分，而且与人类通信不同的是，说话者并没有施加与之相反的、指向简洁的最省力压力。事实上，当代价函数包含对较长消息的惩罚时，得到的消息分布便开始遵循 ZLA。我们的分析强调，在高度受控的设置中研究涌现通信的基本特征非常重要，以确保后者不会偏离人类语言太远。此外，我们还具体展示了不同的功能性压力如何催生缺乏人类语言基本性质的成功通信编码，从而凸显了这些压力在人类语言中所扮演的角色。

**Chasing ghosts: Instruction following as Bayesian state tracking**
（追逐幽灵：将指令跟随视为贝叶斯状态跟踪）
Peter Anderson、Ayush Shrivastava、Devi Parikh、Dhruv Batra、Stefan Lee
一条视觉接地的导航指令可以被解释为：沿正确轨迹行进的智能体将遇到的一系列预期观察与将执行的动作。基于这一直觉，我们把视觉-语言导航（VLN）[1] 中寻找目标位置的问题表述为贝叶斯状态跟踪框架——学习以这些可预期事件为条件的观察模型和运动模型。结合一个在导航过程中即时构建语义空间地图的映射器，我们构建了一个端到端可微分的贝叶斯滤波器，并通过依据指令预测穿过地图的最可能轨迹来训练它识别目标。由此得到的导航策略构成了一种新的指令跟随方法，显式地对状态上的概率分布建模，编码了强大的几何与算法先验，同时具备更好的可解释性。实验表明，在地图上预测目标位置时，我们的方法优于强大的 LingUNet [2] 基线。在完整 VLN 任务（即导航到目标位置）上，我们的方法在对导航约束依赖更少的情况下取得了有前景的结果。

**Cold case: The lost MNIST digits**
（悬案：丢失的 MNIST 数字）
Chhavi Yadav、Leon Bottou
尽管流行的 MNIST 数据集 [LeCun et al., 1994] 源自 NIST 数据库 [Grother and Hanaoka, 1995]，但这一派生的精确处理步骤已随时间遗失。我们提出了一种足够精确、可作为 MNIST 数据集替代品的重建方案，其准确率变化微不足道。我们将每个 MNIST 数字追溯至其 NIST 来源及其丰富的元数据（如书写者标识、分区标识等）。我们还重建了包含 60000 个样本的完整 MNIST 测试集，而非通常的 10000 个。由于其余 50000 个样本从未被分发，它们可以用来研究 25 年来 MNIST 实验对已报告测试性能的影响。我们有限的结果明确证实了 Recht 等人 [2018, 2019] 观察到的趋势：尽管误分类率略有偏差，分类器排序和模型选择在总体上仍然可靠。我们将这一现象归因于在同一批数字上比较分类器的配对优势。

**Compositional generalization through meta sequence-to-sequence learning**
（通过元序列到序列学习实现组合泛化）
Brenden Lake
人类可以学习一个新概念并组合地使用它——在学会如何「blicket」之后就能理解如何「blicket 两次」。相比之下，强大的序列到序列（seq2seq）神经网络无法通过这类组合性测试，尤其是在把新概念与已有概念组合时。本文展示了如何通过元 seq2seq 学习训练记忆增强神经网络来实现组合泛化。在这一方法中，模型在一系列 seq2seq 问题上训练，以获得解决新 seq2seq 问题所需的组合技能。元 seq2seq 学习解决了多个面向组合学习的 SCAN 测试，并能学会将隐式规则应用于变量。

**Correlated uncertainty for learning dense correspondences from noisy labels**
（从噪声标签学习稠密对应关系的相关性不确定性）
Natalia Neverova、David Novotny、Andrea Vedaldi
许多机器学习方法依赖人类监督以达到最优性能。然而，在 DensePose 这类以建立图像间稠密视觉对应为目标的任务中，人工标注的质量存在内在上限。我们通过让神经网络预测器具备输出标签分布的能力来解决这一问题，从而显式且内省地捕捉标注中的偶然不确定性。与以往工作相比，我们展示了相关误差场在 DensePose 等应用中会自然出现，并且这些场可以用深度网络建模，从而更好地理解标注误差。我们证明，这些模型凭借对不确定性更好的理解，可以更准确地解决原始 DensePose 任务，在该基准上刷新了最先进的准确率。最后，我们展示了不确定性估计在融合多个模型预测中的用途，得到一种更好、更有原则的模型集成方法，可进一步提升准确率。

**Cross-channel communication networks**
（跨通道通信网络）
Jianwei Yang、Zhile Ren、Chuang Gan、Hongyuan Zhu、Devi Parikh
卷积神经网络通过把逐通道的特征响应图送入后续层来处理输入数据。尽管加深网络带来了大量进展，但每个通道的信息只能以分层前馈的方式从低层传播到高层。如果把卷积层中的每个滤波器看作一个神经元，那么在 CNN 中这些神经元在每层内部并没有显式通信。我们引入了一种名为跨通道通信（C3）块的新型网络单元，这是一个简单而有效的模块，用于促进同一层内的神经元通信。C3 块使神经元能够通过一个微型神经网络交换信息，该网络由特征编码器、消息通信器和特征解码器组成，之后再把信息送入下一层。有了 C3 块，每个神经元都会考虑同层其他神经元的通道响应，从而学到更具判别性和互补性的表示。在多个计算机视觉任务上的大量实验表明，我们所提机制让更浅的网络也能在每层内聚合有用信息，性能超过基线深度网络和其他有竞争力的方法。

**Differentiable convex optimization layers**
（可微分凸优化层）
Akshay Agrawal、Brandon Amos、Shane Barratt、Stephen Boyd、Steven Diamond、J. Zico Kolter
最近的工作已经展示了如何将可微分优化问题（即其解可以被反向传播的问题）作为层嵌入深度学习架构。这一方法为某些问题提供了有用的归纳偏置，但现有的可微分优化层软件较为僵硬，难以应用于新场景。本文提出一种对规范化凸规划（disciplined convex programs，凸优化领域专用语言所使用的一类凸优化问题）进行微分的方法。我们引入了规范化参数化规划（disciplined parametrized programming）——规范凸规划的一个子集，并证明每个规范化参数化规划都可以表示为三者的复合：从参数到问题数据的仿射映射、求解器，以及从求解器解到原问题解的仿射映射（我们称之为仿射-求解器-仿射形式的新形式）。然后我们展示如何高效地对每个组成部分微分，从而实现对整个凸规划的端到端解析微分。我们在流行的 Python 嵌入式凸优化 DSL CVXPY 的 1.1 版本中实现了该方法，并在 PyTorch 和 TensorFlow 2.0 中额外实现了面向规范化凸规划的可微分层。我们的实现显著降低了在可微分程序中使用凸优化问题的门槛。我们展示了在线性机器学习模型和随机控制中的应用，并表明我们的层在执行时间上与以往工作的专用可微分求解器相比具有竞争力。

**Exploration bonus for regret minimization in discrete and continuous average reward MDPs**
（离散与连续平均奖励 MDP 中遗憾最小化的探索奖励）
Jian Qian、Ronan Fruit、Matteo Pirotta、Alessandro Lazaric
探索奖励是管理马尔可夫决策过程（MDP）中探索-利用权衡的有效方法。虽然它已在无限时域折扣问题和有限时程问题中得到分析，我们专注于更具挑战性的无限时程无折扣设定中探索奖励的设计与分析。我们首先引入 SCAL+——SCAL [1] 的一个变体——它使用合适的探索奖励来求解任意离散未知弱连通 MDP，只要已知最优偏置函数跨度（span）的上界 c。我们证明 SCAL+ 享有与 SCAL 相同的遗憾保证，而后者依赖效率较低的扩展值迭代方法。此外，我们利用探索奖励方案提供的灵活性，将 SCAL+ 推广到具有连续状态空间和离散动作的光滑 MDP。我们证明所得算法（SCCAL+）达到与 UCCRL [2] 相同的遗憾界，同时是该设定下首个可实现的算法。

**Finding the needle in the haystack with convolutions: On the benefits of architectural bias**
（用卷积在大海中捞针：论架构偏置的益处）
Stéphane d'Ascoli、Levent Sagun、Giulio Biroli、Joan Bruna
尽管深度神经网络在广泛的学习任务上取得了现象级的成功，但理解其工作方式的理论仍然缺乏。尤其是，众所周知卷积神经网络（CNN）在空间结构化数据上的表现远好于全连接网络（FCN）：CNN 的架构结构受益于数据特征的先验知识，例如平移不变性。这项工作的目的是通过损失景貌中的动力学这一视角来理解这一事实。我们引入了一种把 CNN 映射到其等价 FCN（记作 eFCN）的方法。这种嵌入使得可以直接在 FCN 空间中比较 CNN 与 FCN 的训练动力学。我们用这一方法测试了一种新的训练协议：先训练一个 CNN，在某个「松弛时刻」把它嵌入到 FCN 空间，然后在 FCN 空间中继续训练。我们观察到，对所有松弛时刻，偏离 CNN 子空间的程度都很小，而且 eFCN 达到的最终性能高于同架构的标准 FCN 所能达到的水平。更令人惊讶的是，对某些中间松弛时刻，eFCN 超过了它所源自的 CNN，以一种互补的方式结合了 CNN 的先验信息和 FCN 的表达能力。我们协议的实用价值受限于高度稀疏的 eFCN 的庞大尺寸，但它为架构偏置在随机梯度动力学下的持续性提供了有趣的洞见。它表明 FCN 损失景貌中存在一些与极好泛化相关联的罕见盆地，而只有借助 CNN 先验才能到达它们——这一先验有助于在优化早期引导景貌中的探索。

**Fixing the train-test resolution discrepancy**
（修正训练-测试分辨率差异）
Hugo Touvron、Andrea Vedaldi、Matthijs Douze、Hervé Jegou
数据增强是训练图像分类神经网络的关键。本文首先表明，现有的增强方法会在分类器于训练和测试时所见物体尺寸之间引入显著差异：事实上，更低的训练分辨率反而能改善测试时的分类效果！随后我们提出了一种简单的策略，采用不同的训练和测试分辨率来优化分类器性能。它依赖于在测试分辨率上对网络进行一次计算开销很低的微调。这使得可以用小尺寸训练图像训练出强大的分类器，从而显著缩短训练时间。例如，我们用 128×128 图像训练的 ResNet50 在 ImageNet 上获得 77.1% 的 top-1 准确率，用 224×224 训练的则达到 79.8%。一个在 9.4 亿张 224×224 图像上以弱监督预训练、再用我们的技术在 320×320 测试分辨率上进一步优化的 ResNeXt-101 32x48d 达到了 86.4% 的 top-1 准确率（top-5：98.0%）。据我们所知，这是迄今为止最高的 ImageNet 单裁剪准确率。

**Gossip-based actor-learner architectures for deep reinforcement learning**
（用于深度强化学习的基于流言传播的 actor-learner 架构）
Mahmoud Assran、Joshua Romoff、Nicolas Ballas、Joelle Pineau、Mike Rabbat
多模拟器训练通过稳定学习并允许更高训练吞吐量，为深度强化学习近来的成功做出了贡献。我们提出基于流言传播（gossip）的 actor-learner 架构（GALA）：若干 actor-learner（如 A2C 智能体）以对等通信拓扑组织，并通过异步流言交换信息，以利用大量分布式模拟器。我们证明，在使用松耦合异步通信时，GALA 智能体在训练期间始终彼此保持在某个 ε-球内。通过减少智能体之间的同步量，GALA 比其完全同步的对应者 A2C 更高效、更可扩展。GALA 也优于 A3C，更鲁棒且样本效率更高。我们展示了可以在单块 GPU 上并行运行多个松耦合的 GALA 智能体，在相近功耗下取得远高于原始 A2C 的硬件利用率和帧率。

**Hierarchical decision making by generating and following natural language instructions**
（通过生成和遵循自然语言指令进行分层决策）
Hengyuan Hu、Denis Yarats、Qucheng Gong、Yuandong Tian、Mike Lewis
我们探索将潜在自然语言指令作为复杂动作的表达性强、可组合的表示，用于分层决策。我们的智能体不是直接选择微观动作，而是先以自然语言生成一个潜在计划，再由另一个模型执行。我们引入了一个具有挑战性的即时战略游戏环境，需要在长时间尺度上协调大量单位的动作。我们从人类对局中收集了 76000 对「指令-执行」数据，并训练了指挥者模型和执行者模型。实验表明，以自然语言为潜在变量的模型显著优于直接模仿人类动作的模型。语言的组合结构对其作为动作表示的有效性至关重要。我们还发布了代码、模型和数据。

**Hyper-graph-network decoders for block codes**
（面向分组码的超图网络解码器）
Eliya Nachmani、Lior Wolf
神经解码器已被证明在短 BCH 码上优于经典的消息传递技术。在这项工作中，我们通过用图神经网络执行消息传递，把这些结果扩展到大得多的代数分组码家族。Tanner 图中每个变量节点处子网络的参数由一个超网络获得，该超网络以当前消息的绝对值为输入。为增加稳定性，我们采用了基于该激活函数高阶泰勒近似的简化版 arctanh 激活。结果表明，对于来自不同码族（BCH、LDPC、Polar）的大量代数分组码，我们方法得到的解码优于原始置信传播方法以及文献中的其他学习技术。

**Hyperbolic graph neural networks**
（双曲图神经网络）
Qi Liu、Maximilian Nickel、Douwe Kiela
从图结构数据中学习是机器学习和人工智能中的重要任务，图神经网络（GNN）在此已展现出巨大前景。受几何表示学习最新进展的启发，我们提出了一种新颖的 GNN 架构，用于在具有可微分指数映射和对数映射的黎曼流形上学习表示。我们开发了一种可扩展的算法来建模图的结构性质，并比较了欧氏几何与双曲几何。实验中，我们展示了双曲 GNN 可以在多个基准数据集上带来实质性提升。

**Learning temporal pose estimation from sparsely labeled videos**
（从稀疏标注视频中学习时序姿态估计）
Gedas Bertasius、Christoph Feichtenhofer、Du Tran、Jianbo Shi、Lorenzo Torresani
现代视频中多人姿态估计方法需要大量稠密标注。然而，标注视频中的每一帧既昂贵又费时。为减少对稠密标注的需求，我们提出了 PoseWarper 网络，利用稀疏标注（每 k 帧）的训练视频来学习执行稠密的时序姿态传播与估计。给定一对视频帧——已标注的帧 A 和未标注的帧 B——我们训练模型通过可变形卷积，利用帧 B 的特征预测帧 A 中的人体姿态，以隐式学习 A 与 B 之间的姿态变形（warping）。我们证明训练好的 PoseWarper 可用于多个应用。首先，在推理时可以反转网络的应用方向，把姿态信息从人工标注帧传播到未标注帧。这使得仅凭少量人工标注帧即可为整段视频生成姿态标注。与基于光流的现代标签传播方法相比，我们的变形机制紧凑得多（600 万对 3900 万参数），也更准确（88.7% mAP 对 83.8% mAP）。我们还展示，通过在把传播姿态加入原始人工标注所得到的增强数据集上训练，可以提升姿态估计器的准确率。最后，我们可以在推理时用 PoseWarper 聚合来自相邻帧的时序姿态信息。这使我们在 PoseTrack2017 和 PoseTrack2018 数据集上获得了最先进的姿态检测结果。

**Learning to perform local rewriting for combinatorial optimization**
（学习执行组合优化的局部重写）
Xinyun Chen、Yuandong Tian
针对困难组合优化的基于搜索的方法通常由启发式规则引导。在各种条件和情形下调节启发式规则往往非常耗时。本文提出 NeuRewriter，它学习一个策略来挑选启发式规则并重写当前解的局部组件，迭代改进直至收敛。该策略分解为区域选择和规则选择两个组件，各自由用强化学习 actor-critic 方法训练的神经网络参数化。NeuRewriter 捕捉组合问题的一般结构，在三项多样化任务中表现出色：表达式化简、在线作业调度和车辆路径问题。NeuRewriter 胜过 Z3 [15] 中的表达式化简组件；在在线作业调度中胜过 DeepRM [33] 和 Google OR-tools [19]；在车辆路径问题中胜过近期的神经基线 [35, 29] 和 Google OR-tools [19]。

**Levenshtein Transformer**
Jiatao Gu、Changhan Wang、Junbo Zhao
现代神经序列生成模型要么从零开始逐步生成词元，要么（迭代地）修改一个长度固定的词元序列。在这项工作中，我们开发了 Levenshtein Transformer，一个为更灵活、更易处理的序列生成而设计的新部分自回归模型。与以往方法不同，我们模型的基本运算是插入和删除。二者的结合不仅便于生成，也便于序列修正，允许长度动态变化。我们还为此提出了一套新的训练技术，利用其互补性质，有效地把一种运算作为另一种的学习信号。应用所提模型的实验表明，在生成（如机器翻译、文本摘要）和修正任务（如自动后编辑）上都以大幅提升的效率取得了相当甚至更好的性能。我们进一步确认了模型的灵活性：展示了一个用机器翻译训练的 Levenshtein Transformer 可以直接用于自动后编辑。

**Limiting extrapolation in linear approximate value iteration**
（限制线性近似值迭代中的外推）
Andrea Zanette、Alessandro Lazaric、Mykel J. Kochenderfer、Emma Brunskill
我们研究使用生成式模型的线性近似值迭代（LAVI）。虽然线性模型可以用少量参数精确表示最优值函数，但多项实证和理论研究显示，最小二乘投影与 Bellman 算子的组合可能是扩张的，导致 LAVI 在迭代中放大误差并最终发散。我们引入一种算法，通过组合在一组锚点状态上估计的 Q 值来近似值函数。我们的算法试图在线性方法的泛化性与紧凑性，和插值方法特有的小误差放大之间取得平衡。我们证明，如果任意状态的特征可以表示为锚点特征的凸组合，那么误差在迭代中以线性（而非指数）方式传播，且我们的方法在时程和锚点数量上达到多项式样本复杂度界。这些发现在一系列简单问题的初步仿真中得到了证实，而传统最小二乘 LAVI 方法在这些问题上是发散的。

**On the curved geometry of accelerated optimization**
（论加速优化的弯曲几何）
Aaron Defazio
在这项工作中，我们为强凸问题的 Nesterov 加速梯度法（AGM）提供了一个微分几何动机。通过把优化过程视为发生在一个具有自然结构的黎曼流形上，AGM 方法可以看作是在这一弯曲空间中应用的近似点方法（proximal point method）。这一视角也可以推广到连续时间情形，其中加速梯度法由流形上一个常微分方程（ODE）的自然分块隐式欧拉离散化产生。我们对二次目标下该 ODE 的收敛速率给出了分析。

**On the ineffectiveness of variance reduced optimization for deep learning**
（论方差缩减优化对深度学习的无效性）
Aaron Defazio、Leon Bottou
随机方差缩减在优化中的应用近来在理论和实践上都取得了显著成功。这些技术对现代深度神经网络训练中遇到的困难非凸优化问题的适用性仍是一个悬而未决的问题。我们展示了 SVRG 技术及相关方法的朴素应用会失败，并探究了其中的原因。

**One ticket to win them all: Generalizing lottery ticket initializations across datasets and optimizers**
（一张彩票通吃：彩票初始化在数据集和优化器间的泛化）
Ari Morcos、Haonan Yu、Michela Paganini、Yuandong Tian
彩票初始化 [7] 的成功表明，只要网络初始化得当，小型稀疏化网络也可以被训练。遗憾的是，寻找这些「中奖彩票」初始化在计算上非常昂贵。一种可能的解决方案是在多种数据集和优化器之间复用同样的中奖彩票。然而，中奖彩票初始化的普适性尚不清楚。在此，我们试图回答这一问题：为一个训练配置（优化器和数据集）生成中奖彩票，并在另一个配置上评估其性能。也许令人惊讶，我们发现，在自然图像领域内，中奖彩票初始化可以在多种数据集（包括 Fashion MNIST、SVHN、CIFAR-10/100、ImageNet 和 Places365）之间泛化，往往达到与在同一数据集上生成的中奖彩票接近的性能。此外，用更大数据集生成的中奖彩票始终比用小数据集生成的迁移效果更好。我们还发现中奖彩票初始化可以在优化器之间以高性能泛化。这些结果表明，由足够大的数据集生成的中奖彩票初始化包含对更广泛的神经网络通用的归纳偏置，能在多种设定下改进训练，并为开发更好的初始化方法带来希望。

**PerspectiveNet: A scene-consistent image generator for new view synthesis in real indoor environments**
（PerspectiveNet：面向真实室内环境新视图合成的场景一致图像生成器）
David Novotny、Benjamin Graham、Jeremy Reizenstein
给定一个室内环境的一组参考 RGBD 视图和一个新视点，我们的目标是预测从该位置看到的画面。以往的新视图生成工作主要聚焦于受限得多的场景，通常涉及孤立 CAD 模型的人工渲染视图。这里我们要处理的是该问题难得多的版本。我们设计了一种利用场景已知几何性质（逐帧相机外参和深度）把参考视图变形为新视图的方法。生成视图中的缺陷由一个新颖的 RGBD 图像修补网络 PerspectiveNet 处理，该网络针对给定场景微调，以获得与场景相机系统中所有视图几何一致的图像。在 ScanNet 和 SceneNet 数据集上的实验显示出优于强基线的性能。

**PHYRE: A new benchmark for physical reasoning**
（PHYRE：一个新的物理推理基准）
Anton Bakhtin、Laurens van der Maaten、Justin Johnson、Laura Gustafson、Ross Girshick
理解和推理物理是智能体的重要能力。我们开发了用于物理推理的 PHYRE 基准，它包含 2D 物理环境中一组简单的经典力学谜题。该基准旨在鼓励开发样本高效、跨谜题泛化良好的学习算法。我们在 PHYRE 上测试了多种现代学习算法，发现它们在高效求解这些谜题方面都有不足。我们期望 PHYRE 能鼓励开发新颖的、样本高效的智能体，学习有效而有用的物理模型。代码和亲自体验 PHYRE，请访问 https://player.phyre.ai/。

**PyTorch: An imperative style, high-performance deep learning library**
（PyTorch：命令式风格的高性能深度学习库）
Adam Paszke、Sam Gross、Francisco Massa、Adam Lerer、James Bradbury、Gregory Chanan、Trevor Killeen、Zeming Lin、Natalia Gimelshein、Luca Antiga、Alban Desmaison、Andreas Kopf、Edward Yang、Zachary DeVito、Martin Raison、Alykhan Tejani、Sasank Chilamkurthy、Benoit Steiner、Lu Fang、Junjie Bai、Soumith Chintala
深度学习框架往往只关注易用性或速度之一，而非两者兼得。PyTorch 是一个机器学习库，它表明这两个目标实际上是兼容的：它提供命令式、Pythonic 的编程风格，支持「代码即模型」、让调试变得容易、与其他流行的科学计算库一致，同时保持高效并支持 GPU 等硬件加速器。本文详述了驱动 PyTorch 实现的原则以及这些原则如何体现在其架构中。我们强调，PyTorch 的每个方面都是完全受用户控制的常规 Python 程序。我们还解释了其运行时关键组件的审慎而务实的实现如何使它们协同工作，实现出色的性能。我们展示了各个子系统的效率，以及 PyTorch 在多个常见基准上的整体速度。

**Robust multi-agent counterfactual prediction**
（鲁棒多智能体反事实预测）
Alexander Peysakhovich、Christian Kroer、Adam Lerer
我们考虑使用日志数据来预测「如果改变多智能体系统中的『游戏规则』会发生什么」的问题。这个任务很困难，因为在很多情况下我们观察到个体采取的行动，却看不到他们的私有信息或完整奖励函数。此外，智能体是策略性的，规则改变时他们的行动也会改变。现有方法（如结构估计、逆强化学习）假设智能体的行为来自某个效用函数的优化，或系统处于均衡。它们通过用观察到的行动学习潜在的效用函数（即类型），再求解反事实环境的均衡来做反事实预测。这一方法施加了沉重的假设，如被观察智能体的理性，以及对环境和智能体效用函数的正确建模。我们提出了一种分析反事实结论对这些假设被违反的敏感性的方法，称为鲁棒多智能体反事实预测（RMAC）。我们提供了计算 RMAC 界的一阶方法。我们把 RMAC 应用于市场设计中的经典环境：拍卖、学校选择和社会选择。

**Regret bounds for learning state representations in reinforcement learning**
（强化学习中学习状态表示的遗憾界）
Ronald Ortner、Matteo Pirotta、Alessandro Lazaric、Ronan Fruit、Odalric-Ambrym Maillard
我们考虑在线强化学习的问题，其中学习智能体可获得若干状态表示（把历史映射到离散状态空间）。假设其中至少有一个表示诱导出马尔可夫决策过程（MDP），智能体的性能以相对于该 MDP 表示中给出最高平均奖励的最优策略的累积遗憾来衡量。我们提出一个在任意连通 MDP 中遗憾为 Õ(√T) 的算法（UCB-MS）。该遗憾界表明 UCB-MS 自动适应马尔可夫模型，并改进了目前已知的最优 Õ(T2/3) 阶界。

**RUBi: Reducing unimodal biases in visual question answering**
（RUBi：减少视觉问答中的单模态偏置）
Remi Cadene、Corentin Dancette、Hedi Ben younes、Matthieu Cord、Devi Parikh
视觉问答（VQA）是回答关于图像的问题的任务。一些 VQA 模型常常利用单模态偏置来给出正确答案，而不使用图像信息。结果，在被评估于训练集分布之外的数据时，它们的性能大幅下降。这一关键问题使其不适合现实场景。我们提出 RUBi，一种减少任何 VQA 模型偏置的新学习策略。它降低最偏置样本（即不看图像也能正确分类的样本）的重要性，隐式地迫使 VQA 模型使用两种输入模态，而不是依赖问题与答案之间的统计规律。我们利用一个只看问题的模型来捕捉语言偏置，识别这些不受欢迎的规律何时被使用，并通过影响基础 VQA 模型的预测来阻止它学习这些规律，从而动态调整损失以补偿偏置。我们通过超越 VQA-CP v2 上的当前最优结果来验证我们的贡献。该数据集专门用于评估 VQA 模型在测试时暴露于与训练时不同问题偏置下的鲁棒性。代码可在此获取。

**SuperGLUE: A stickier benchmark for general-purpose language understanding Systems**
（SuperGLUE：一个更「黏」的通用语言理解系统基准）
Alex Wang、Yada Pruksachatkun、Nikita Nangia、Amanpreet Singh、Julian Michael、Felix Hill、Omer Levy、Samuel R. Bowman
过去一年中，新的预训练和迁移学习模型与方法在一系列语言理解任务上带来了显著的性能提升。一年多前引入的 GLUE 基准提供了一个汇总此类多样任务进展的单一数字指标，但该基准上的性能近来已超过非专家人类水平，表明进一步研究的提升空间有限。本文介绍 SuperGLUE——一个仿照 GLUE 的新基准，包含一组更困难的语言理解任务、一个软件工具包和一个公开排行榜。SuperGLUE 可在 super.gluebenchmark.com 获取。

**Third-person visual imitation learning via decoupled hierarchical controller**
（通过解耦分层控制器进行第三人称视觉模仿学习）
Pratyusha Sharma、Deepak Pathak、Abhinav Gupta
我们研究一个泛化的从示范中学习的设定：构建一个智能体，仅通过观看一段第三人称视角的人类示范视频，就能在未见过的场景中操纵新颖物体。为达成这一目标，我们的智能体不仅要学会在其语境中理解第三人称示范视频的意图，还要在其自身环境配置下执行预期任务。我们的核心洞见是在学习期间显式地施加这一结构，把「要达成什么」（预期任务）与「如何执行」（控制器）解耦。我们提出一个分层设定：高层模块学习以第三人称视频示范为条件生成一系列第一人称子目标，低层控制器预测达成这些子目标的动作。我们的智能体从原始图像观察出发行动，无法获取完整状态信息。我们在使用 Baxter 的真实机器人平台上展示了倒水和把物体放进箱子等操纵任务的结果。项目视频和代码见 https://pathak22.github.io/hierarchical-imitation/。

**Tight regret bounds for model-based reinforcement learning with greedy policies**
（基于模型的强化学习中贪心策略的紧遗憾界）
Yonathan Efroni、Nadav Merlis、Mohammad Ghavamzadeh、Shie Mannor
最先进的高效基于模型的强化学习（RL）算法通常通过迭代求解经验模型来行动，即对由收集到的经验构建的马尔可夫决策过程（MDP）执行完全规划。本文聚焦有限状态、有限时程、无折扣 MDP 设定下的基于模型的 RL，并确立了用贪心策略探索——即按一步规划行动——可以达到紧的极小化极大遗憾性能 Õ(√HSAT)。因此，基于模型的 RL 中的完全规划可以完全避免而不会有任何性能损失，且这样做可将计算复杂度降低 S 倍。这些结果基于对实时动态规划的新颖分析，随后被扩展到基于模型的 RL。具体而言，我们把执行完全规划的现有算法泛化为按一步规划行动，并为这些泛化证明了与其完全规划对应物具有相同速率的遗憾界。

**Unsupervised object segmentation by redrawing**
（通过重绘进行无监督物体分割）
Mickaël Chen、Thierry Artieres、Ludovic Denoyer
物体分割是一个关键问题，通常靠在由图像和对应物体掩码组成的大数据集上做监督学习来解决。由于掩码必须在像素级提供，为任何新领域构建这样的数据集可能非常昂贵。我们提出 ReDO，一个无需任何标注、以无监督方式从图像中提取物体的新模型。它依赖于这样的想法：改变物体的纹理或颜色应当可以做到不改变数据集的整体分布。基于这一假设，我们的方法基于对抗架构，其中生成器由输入样本引导：给定一张图像，它提取物体掩码，然后在同一位置重绘一个新物体。生成器由判别器控制，以确保生成图像的分布与原始分布对齐。我们在不同数据集上实验了该方法，证明了所提取掩码的良好质量。

**ViLBERT: Pretraining task-agnostic representations for vision and language**
（ViLBERT：预训练视觉与语言的任务无关表示）
Jiasen Lu、Dhruv Batra、Devi Parikh、Stefan Lee
我们提出 ViLBERT（Vision-and-Language BERT 的缩写），一个学习图像内容与自然语言的任务无关联合表示的模型。我们把流行的 BERT 架构扩展为多模态双流模型，在两条独立的流中分别处理视觉和文本输入，二者通过共同注意力的 transformer 层交互。我们通过两个代理任务在大型、自动收集的 Conceptual Captions 数据集上预训练模型，然后将其迁移到多个已有的视觉-语言任务——视觉问答、视觉常识推理、指代表达和基于描述的图像检索——只需对基础架构做少量添加。与现有的任务专用模型相比，我们观察到各任务上的显著提升——在全部四项任务上达到最先进水平。我们的工作代表着一种转变：从仅在任务训练中学习视觉与语言之间的接地，转向把视觉接地视为一种可预训练、可迁移的能力。

## NeurIPS 上的研讨会、教程及其他活动

**Bridging game theory and deep learning（博弈论与深度学习的桥接）**

- 论文：A closer look at the optimization landscape of GANs — Hugo Bérard、Gauthier Gidel、Amjad Almahairi、Pascal Vincent、Simon Lacoste-Julien

**Context and compositionality in biological and artificial neural systems（生物与人工神经系统中的语境与组合性）**

- 共同组织者：Kyunghyun Cho

**Conversational AI workshop（对话式 AI 研讨会）**

- 共同主席：Alborz Geramifard
- 受邀演讲者：Y-Lan Boureau
- 论文：Improving robustness of task-oriented dialog systems — Arash Einolghozati、Sonal Gupta、Mrinal Mohit、Rushin Shah

**Deep reinforcement learning（深度强化学习）**

- 共同组织者：Joelle Pineau
- 论文：Benchmarking batch deep reinforcement learning algorithms — Scott Fujimoto、Edoardo Conti、Mohammad Ghavamzadeh、Joelle Pineau
- 论文：Data-efficient co-adaptation of morphology and behaviour with deep reinforcement learning — Kevin Sebastian Luck、Heni Ben Amor、Roberto Calandra
- 论文：Modular visual navigation using active neural mapping — Devendra Singh Chaplot、Saurabh Gupta、Abhinav Gupta、Ruslan Salakhutdinov
- 论文：Objective mismatch in model-based reinforcement learning — Nathan Lambert、Brandon Amos、Omry Yadan、Roberto Calandra
- 论文：Plan2Vec: Unsupervised representation learning by latent plans — Ge Yang、Amy Zhang、Ari Morcos、Joelle Pineau、Pieter Abbeel、Roberto Calandra
- 论文：Search in cooperative partially observable games — Adam Lerer、Hengyuan Hu、Jakob Foerster、Noam Brown
- 论文：SEERL: Sample efficient ensemble reinforcement learning — Rohan Saphal、Balaraman Ravindran、Dheevatsa Mudigere、Sasikanth Avancha、Bharat Kaul

**EMC2: Energy-efficient machine learning and cognitive computing（能效机器学习与认知计算）**

- 大会主题演讲：Yann LeCun
- 论文：Energy-aware neural architecture optimization with splitting steepest descent — Dilin Wang、Lemeng Wu、Meng Li、Vikas Chandra、Qiang Liu
- 论文：Improving efficiency in neural network accelerator using operands hamming distance optimization — Meng Li、Yilei Li、Pierce Chuang、Liangzhen Lai、Vikas Chandra

**Emergent communication: Towards natural language（涌现通信：迈向自然语言）**

- 共同组织者：Kyunghyun Cho、Douwe Kiela、Cinjon Resnick

**Imitation learning and its application to natural language generation (tutorial)（模仿学习及其在自然语言生成中的应用，教程）**

- Kyunghyun Cho

**Machine learning and the physical sciences（机器学习与物理科学）**

- 共同组织者：Michela Paganini

**Machine learning for systems workshop（面向系统的机器学习研讨会）**

- 演讲者：Eytan Bakshy

**Machine learning and the physical sciences（机器学习与物理科学）**

- 共同组织者：Michela Paganini

**Meta-learning（元学习）**

- 共同组织者：Roberto Calandra
- 受邀演讲者：Brenden Lake

**MLSys: Workshop on systems for ML（ML 系统研讨会）**

- 共同组织者：Aparna Lakshmiratan
- 论文：Mvfst-rl: An asynchronous RL framework for congestion control with delayed actions — Viswanath Sivakumar、Tim Rocktäschel、Alexander H. Miller、Heinrich Küttler、Nantas Nardelli、Mike Rabbat、Joelle Pineau、Sebastian Riedel
- 论文：Post-training 4-bit quantization on embedding tables — Hui Guan、Andrey Malevich、Jiyan Yang、Jongsoo Park、Hector Yuen
- 论文：Predictive precompute with recurrent neural networks — Hanson Wang、Zehui Wang、Yuanyuan Ma

**Responsible and reproducible AI（负责任且可复现的 AI）**

- 演讲者：Narine Kokhlikyan、William Falcon、Shubho Sengupta、Joe Spisak、Ailing Zhang

**Multi-modal research to production（多模态研究到生产）**

- 演讲者：Raghuraman Krishnamoorthi、Xian Li、Dmytro Okhonko、Vinicius Reis、Michael Suo、Yongqiang Wang、Yuxin Wu

**Retrospectives: A venue for self-reflection in ML research（回顾：ML 研究自我反思的园地）**

- 共同组织者：Jessica Forde、Michela Paganini、Joelle Pineau、Koustuv Sinha、Shagun Sodhani

**Robot learning: Control and interaction in the real world（机器人学习：真实世界中的控制与交互）**

- 共同组织者：Roberto Calandra

**Safety and robustness in decision making（决策中的安全性与鲁棒性）**

- 共同组织者：Mohammad Ghavamzadeh
- 论文：Improved algorithms for conservative exploration in bandits — Evrard Garcelon、Mohammad Ghavamzadeh、Alessandro Lazaric、Matteo Pirotta
- 论文：Robust identifiability in linear structural equation models for causal inference — Karthik Abinav Sankararaman、Anand Louis、Navin Goyal
- 论文：Thompson sampling for contextual bandit problems with auxiliary safety constraints — Samuel Daulton、Shaun Singh、Vashist Avadhanula、Drew Dimmery、Eytan Bakshy

**Science meets engineering of deep learning（当深度学习的科学遇上工程）**

- 共同组织者：Adriana Romero、Levent Sagun
- 演讲者：Kyunghyun Cho、Natalia Neverova
- 小组成员：Nafissa Yakubova、Aparna Lakshmiratan
- 小组顾问：Michela Paganini
- 论文：Non-Gaussian processes and neural networks at finite widths — Sho Yaida
- 论文：The generalization-stability tradeoff in neural network pruning — Brian R. Bartoldson、Ari Morcos、Adrian Barbu、Gordon Erlebacher
- 论文：Training batchnorm and only batchnorm — Jonathan Frankle、David Schwab、Ari Morcos

**Women in machine learning workshop（女性机器学习研讨会）**

- 共同组织者：Michela Paganini
- 论文：CraftAssist: A framework for dialogue-enabled interactive agents — Kavya Srinet、Jonathan Gray、Yacine Jernite、Haonan Yu、Zhuoyuan Chen、Demi Guo、Siddharth Goyal、Larry Zitnick、Arthur Szlam
