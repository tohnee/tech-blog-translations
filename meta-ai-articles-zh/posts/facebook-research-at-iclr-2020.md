---
title: "Facebook 研究团队在 ICLR 2020"
title_en: "Facebook Research at ICLR 2020"
date: 2020-04-27
source: https://ai.facebook.com/blog/facebook-research-at-iclr-2020
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 研究团队在 ICLR 2020

> 原文：[Facebook Research at ICLR 2020](https://ai.facebook.com/blog/facebook-research-at-iclr-2020) · Meta AI（Wayback 存档）

2020 年 4 月 27 日

在即将于 4 月 26 日至 5 月 1 日举行的国际学习表征会议（ICLR）上，参会者将线上齐聚，探讨他们对推进深度学习的投入。与会者可以与主题讲者进行实时视频问答，讲者包括 Facebook AI 研究院（FAIR，Meta 基础人工智能研究院）成员 Devi Parikh（FAIR 与佐治亚理工学院）和 Yann LeCun（Facebook 首席 AI 科学家、纽约大学教授）。Parikh 将演讲「能看会说的 AI 系统」。LeCun 在去年的会议上获得图灵奖，他将与共同获奖者之一 Yoshua Bengio（蒙特利尔学习算法研究所）一起回顾这一荣誉。其他 Facebook 论文作者与讲者将提供预录视频与幻灯片，供参会者通过聊天流讨论。问题与评论也可以留在 OpenReview 上论文的公共论坛。会议还设虚拟展位，以两三人小组的形式与其他参会者交流、举办社交聚会、把研讨会讨论延续到会议周中，并与包括我们 Facebook 团队在内的会议赞助商交流。你可以线上会见我们的团队、讨论我们的最新进展，并预约与招聘人员或计划经理会面。

## Facebook 在 ICLR 2020 上展示的研究

**细看生成对抗网络的优化图景（A closer look at the optimization landscapes of generative adversarial networks）**
Hugo Berard、Gauthier Gidel、Amjad Almahairi、Pascal Vincent、Simon Lacoste-Julien
生成对抗网络在生成建模上非常成功，但与标准深度神经网络相比，训练仍相对困难。在本文中，我们为 GAN 的优化图景提出新的可视化技术，使我们能够研究由双方梯度拼接而成的博弈向量场。借助这些可视化技术，我们尝试弥合理论与实践之间的鸿沟，实证表明 GAN 的训练会在局部稳定驻点（LSSP）周围出现显著旋转，与理论在玩具样例上的预测相似。此外，我们提供经验证据：GAN 训练收敛到一个稳定的驻点——它是生成器损失的鞍点而非极小值——却仍能取得出色性能。

**比特落地：重新审视神经网络量化（And the bit goes down: Revisiting the quantization of neural networks）**
Pierre Stock、Armand Joulin、Rémi Gribonval、Benjamin Graham、Hervé Jégou
我们解决降低卷积网络架构内存占用的问题。我们引入一种向量量化方法，旨在保持网络输出（而非权重）的重建质量。我们方法的原则是最小化域内输入的损失重建误差。该方法在量化时只需要一组无标注数据，并使用字节对齐的码本存储压缩权重，从而支持 CPU 上的高效推断。我们通过把高性能 ResNet-50 模型量化到 5MB 内存（20 倍压缩比）且在 ImageNet 目标分类上保持 76.1% 的 top-1 精度，以及把 Mask R-CNN 压缩 26 倍，验证了方法。

**CoPhy：物理动力学的反事实学习（CoPhy: Counterfactual learning of physical dynamics）**
Fabien Baradel、Natalia Neverova、Julien Mille、Greg Mori、Christian Wolf
理解机械系统中的因果关系是物理世界推理的重要组成部分。本工作提出了一个新问题：从视觉输入对物体力学做反事实学习。我们开发 CoPhy 基准，评估最先进模型在合成 3D 环境中的因果物理推理能力，并提出一个在反事实设置下学习物理动力学的模型。在观察一个机械实验——例如倒塌中的积木塔、一组弹跳的球或碰撞的物体——之后，我们学习预测对初始条件施加任意干预（如移动场景中某个物体）会如何影响结果。替代未来是在改变后的过去以及模型以端到端方式学到的混淆因子潜在表示的基础上预测的，无需混淆因子监督。我们与前馈视频预测基线比较，并展示观察替代经验如何让网络捕捉环境的潜在物理性质，从而在超人类性能水平上做出显著更准确的预测。

**DD-PPO：从 25 亿帧学习近乎完美的点目标导航器（DD-PPO: Learning near-perfect pointgoal navigators from 2.5 billion frames）**
Erik Wijmans、Abhishek Kadian、Ari Morcos、Stefan Lee、Irfan Essa、Devi Parikh、Manolis Savva、Dhruv Batra
我们提出去中心化分布式近端策略优化（DD-PPO），一种在资源密集型仿真环境中进行分布式强化学习的方法。DD-PPO 是分布式的（使用多台机器）、去中心化的（没有中央服务器）且同步的（计算永不过时），概念简单且易于实现。在训练虚拟机器人于 Habitat-Sim（Savva 等，2019）中导航的实验中，DD-PPO 展现出近线性扩展——在 128 块 GPU 上相较串行实现提速 107 倍。我们利用这一扩展性训练智能体积累 25 亿步经验（相当于 80 年的人类经验）——超过 6 个月的 GPU 训练时间，用 64 块 GPU 在不到 3 天的墙钟时间内完成。这一大规模训练不仅刷新了 Habitat 自主导航挑战赛 2019 的最先进水平，而且基本上「解决」了该任务——在未见过的环境中，不依赖地图、仅凭 RGB-D 相机与 GPS+罗盘传感器实现近乎完美的自主导航。幸运的是，误差与计算呈现幂律式分布；因此，90% 的峰值性能相对较早（1 亿步时）且相对便宜（8 块 GPU 不到 1 天）即可获得。最后，我们表明学到的场景理解与导航策略可以迁移到其他导航任务——这是具身 AI 版的「ImageNet 预训练 + 任务专用微调」。我们的模型在这些迁移任务上胜过 ImageNet 预训练的 CNN，并可作为通用资源（所有模型与代码均已公开）。

**解耦表示与分类器以面向长尾识别（Decoupling representation and classifier for long-tailed recognition）**
Bingyi Kang、Saining Xie、Marcus Rohrbach、Zhicheng Yan、Albert Gordo、Jiashi Feng、Yannis Kalantidis
视觉世界的长尾分布给基于深度学习的分类模型处理类别不平衡问题带来巨大挑战。现有解决方案通常涉及类别平衡策略，如损失重加权、数据重采样或从头部向尾部类别迁移学习，但大多数仍坚持联合学习表示与分类器的方案。在本工作中，我们把学习过程解耦为表示学习与分类，并系统探索不同平衡策略对长尾识别的影响。发现令人惊讶：（1）数据不平衡在学习高质量表示时可能不是问题；（2）用最简单的实例平衡（自然）采样学到的表示，仅通过调整分类器也可能获得强大的长尾识别能力。我们进行了大量实验，在 ImageNet-LT、Places-LT 与 iNaturalist 等常用长尾基准上刷新了最先进性能，表明用解耦表示与分类的直接方法，可以胜过精心设计的损失、采样策略，甚至带记忆的复杂模块。代码见 https://github.com/facebookresearch/classifier-balancing。

**深度自适应 transformer（Depth-adaptive transformer）**
Maha Elbayad、Jiatao Gu、Edouard Grave、Michael Auli
面向大规模任务的最先进序列到序列模型对每个输入序列执行固定数量的计算，无论它易于还是难以处理。在本文中，我们训练可以在网络不同阶段做输出预测的 Transformer 模型，并研究预测特定序列需要多少计算的不同方式。与 Universal Transformer 中迭代应用同一组层的动态计算不同，我们在每一步应用不同的层，同时调整计算量与模型容量。在 IWSLT 德英翻译上，我们的方法在使用不到四分之一解码器层的情况下匹配了调优良好的基线 Transformer 的精度。

**通过重组演示发现运动程序（Discovering motor programs by recomposing demonstrations）**
Tanmay Shankar、Shubham Tulsiani、Lerrel Pinto、Abhinav Gupta
我们提出一种在大规模多样操作演示中学习可重组运动基元的方法。当前把演示分解为基元的方法通常假设手工定义的基元，回避了发现这些基元的困难。另一方面，基元发现的方法对基元复杂度施加了限制性假设，使其只能应用于狭窄任务。我们的方法试图通过联合学习底层运动基元与重组这些基元以还原原始演示来规避这些挑战。通过对基元分解的简约性与给定基元简单性的双重约束，我们得以学到多样的运动基元集合以及这些基元的连贯潜在表示。我们定性与定量地证明，学到的基元捕捉了演示中有语义意义的方面。这使我们能在分层强化学习设置中组合这些基元，高效解决够取与推动等机器人操作任务。

**动力学感知嵌入（Dynamics-aware embeddings）**
William F. Whitney、Rajat Agarwal、Kyunghyun Cho、Abhinav Gupta
在本文中，我们考虑用自监督表示学习提升强化学习（RL）的样本效率。我们提出一个同时学习状态嵌入与动作序列嵌入的前向预测目标。这些嵌入捕捉环境动力学的结构，实现高效的策略学习。我们证明，仅动作嵌入即可改进免模型 RL 在低维状态控制上的样本效率与峰值性能。通过结合状态与动作嵌入，我们在仅 100-200 万环境步内实现了从像素观测出发的目标条件连续控制的高质量策略的高效学习。

**面向原子分辨率蛋白质构象的基于能量的模型（Energy-based models for atomic-resolution protein conformations）**
Yilun Du、Joshua Meier、Jerry Ma、Rob Fergus、Alexander Rives
我们提出一个在原子尺度运行的蛋白质构象基于能量的模型（EBM）。该模型仅在结晶蛋白质数据上训练。相比之下，现有的构象评分方法使用的能量函数融合了物理原理知识以及数十年研究与调优的复杂产物特征。为评估模型，我们在旋转异构体恢复任务上做基准测试——从蛋白质结构中的上下文预测侧链构象的问题，该任务已被用于评估蛋白质设计的能量函数。模型取得了接近 Rosetta 能量函数的性能——后者是蛋白质结构预测与设计中广泛使用的最先进方法。对模型输出与隐藏表示的研究发现，它捕捉了与蛋白质能量相关的物理化学性质。

**提取并利用特征交互解释（Extracting and leveraging feature interaction interpretations）**
Michael Tsang、Dehua Cheng、Hanpeng Liu、Xue Feng、Eric Zhou、Yan Liu
推荐是影响众多用户的流行机器学习应用；因此，推荐模型既准确又可解释十分重要。在本工作中，我们提出一种既解释又增强黑盒推荐系统预测的方法。具体而言，我们提议从源推荐模型解释特征交互，并在目标推荐模型中显式编码这些交互——源模型与目标模型都是黑盒。由于不假设推荐系统的结构，我们的方法可用于一般设置。实验中，我们聚焦机器学习推荐的一个突出应用：广告点击预测。我们发现交互解释既有信息量又有预测力，即显著胜过现有推荐模型。此外，同一交互解释方法还能为推荐之外的领域（如文本与图像分类）提供新洞见。

**联邦学习中的公平资源分配（Fair resource allocation in federated learning）**
Tian Li、Maziar Sanjabi、Ahmad Beirami、Virginia Smith
联邦学习涉及在庞大而异构的网络中训练统计模型。在这样的网络中朴素地最小化聚合损失函数，可能会不成比例地优待或损害某些设备。在本工作中，我们受无线网络公平资源分配启发，提出 q-公平联邦学习（q-FFL）——一个新颖的优化目标，鼓励联邦网络中设备间更公平（具体而言更均匀）的精度分布。为求解 q-FFL，我们设计了适合联邦网络的通信高效方法 q-FedAvg。我们在一组含凸与非凸模型的联邦数据集上验证了 q-FFL 的有效性与 q-FedAvg 的高效性，并表明 q-FFL（连同 q-FedAvg）在最终公平性、灵活性与效率上胜过现有基线。

**通过记忆实现泛化：最近邻语言模型（Generalization through memorization: Nearest neighbor language models）**
Urvashi Khandelwal、Omer Levy、Dan Jurafsky、Luke Zettlemoyer、Michael Lewis
我们引入 kNN-LM，通过把预训练神经语言模型（LM）与 k 最近邻（kNN）模型线性插值来扩展它。最近邻按预训练 LM 嵌入空间中的距离计算，可来自任何文本集合，包括原始 LM 训练数据。把这一增强应用于一个强大的 WIKITEXT-103 LM（近邻取自原始训练集），我们的 kNN-LM 取得了 15.79 的新最先进困惑度——无需额外训练即改进 2.9 个点。我们还表明，该方法对高效扩展到更大训练集有启示，并允许仅通过更改最近邻数据存储实现有效的域适配，同样无需进一步训练。定性来看，该模型在预测罕见模式（如事实知识）时特别有帮助。总之，这些结果强烈表明：学习文本序列之间的相似性比预测下一个词更容易，而最近邻搜索是长尾语言建模的有效途径。

**鼓励协同行为的内在动机（Intrinsic motivation for encouraging synergistic behavior）**
Rohan Chitnis、Shubham Tulsiani、Saurabh Gupta、Abhinav Gupta
我们研究内在动机作为稀疏奖励协同任务中强化学习探索偏差的作用——这类任务需要多个智能体共同努力才能实现单个智能体无法实现的目标。我们的关键想法是：协同任务中内在动机的良好指导原则，是采取那些以智能体单独行动时无法实现的方式影响世界的行为。因此，我们提议激励智能体采取（联合）行动，其效果无法通过组合每个个体智能体的预测效果来预测。我们研究该思想的两个实例：一个基于实际遇到的状态，另一个基于与策略并发训练的动力学模型。前者更简单，后者的优势在于对所采取行动解析可微。我们在带稀疏奖励的机器人双手操作与多智能体运动任务上验证方法；我们发现该方法比 1）仅用稀疏奖励训练、2）使用典型的基于惊奇的内在动机表述（它不偏向协同行为）都更高效。视频见项目网页：https://sites.google.com/view/iclr2020-synergistic。

**学习用主动神经建图进行探索（Learning to explore using active neural mapping）**
Devendra Singh Chaplot、Saurabh Gupta、Dhiraj Gandhi、Abhinav Gupta、Ruslan Salakhutdinov
本工作提出了一种模块化、分层的方法来学习探索 3D 环境的策略。我们的方法结合经典方法与基于学习方法的优势：使用解析路径规划器与学习到的 SLAM 模块，以及全局与局部策略。学习的使用在输入模态上提供了灵活性（SLAM 模块）、利用了世界的结构规律（全局策略），并对状态估计误差提供了鲁棒性（局部策略）。在每个模块中使用学习保留了其益处；与此同时，分层分解与模块化训练使我们得以避开端到端策略训练的高样本复杂度。我们在视觉与物理逼真的仿真 3D 环境中的实验展示了该方法优于以往基于学习与几何的方法。

**论涌现交流中监督与自我博弈的交互（On the interaction between supervision and self-play in emergent communication）**
Ryan Lowe、Abhinav Gupta、Jakob Foerster、Douwe Kiela、Joelle Pineau
教会人工智能体使用自然语言的一个有前景的途径是人在回路的训练。然而，近期工作表明，当前机器学习方法的数据效率太低，无法以这种方式从头训练。在本文中，我们研究两类学习信号之间的关系，以期最终提升样本效率：通过监督学习模仿人类语言数据，以及通过自我博弈（如涌现交流中所做）最大化仿真多智能体环境中的奖励，并引入「监督自我博弈」（S2P）一词指代同时使用这两种信号的算法。我们发现，先用人类数据做监督学习再自我博弈优于相反顺序，表明从头涌现语言并无益处。然后，我们在两个环境中实证研究多种从监督学习开始的 S2P 调度：一个使用符号输入的 Lewis 信号博弈，和一个使用自然语言描述的基于图像的指称博弈。最后，我们引入基于种群的 S2P 方法，进一步提升了性能。

**面向语言组合泛化的置换等变模型（Permutation equivariant models for compositional generalization in language）**
Jonathan Gordon、David Lopez-Paz、Marco Baroni、Diane Bouchacourt
人类通过组合核心语言成分的含义与角色来理解新句子。相比之下，自然语言建模的神经网络在需要这种组合泛化时会失败。本文的主要贡献是提出假设：语言组合性是一种群等变性。基于这一假设，我们提出一组构建等变序列到序列模型的工具。通过在 SCAN 任务上的多种实验，我们在等变性视角下分析现有模型的行为，并证明我们的等变架构能够实现人类语言理解所需的组合泛化类型。

**Poly-encoder：面向快速准确多句打分的架构与预训练策略（Poly-encoders: Architectures and pre-training strategies for fast and accurate multi-sentence scoring）**
Samuel Humeau、Kurt Shuster、Marie-Anne Lachaux、Jason Weston
深度预训练 transformer 的使用在诸多应用中带来了显著进展（Devlin 等，2019）。对于在序列之间做两两比较、把给定输入与对应标签匹配的任务，常见两种方法：对序列对执行完整自注意力的 Cross-encoder，以及分别编码的 Bi-encoder。前者往往效果更好，但对实际使用而言太慢。在本工作中，我们开发了一种新的 transformer 架构——Poly-encoder，它学习全局而非 token 级的自注意力特征。我们对三种方法做了详细比较，包括哪种预训练与微调策略效果最佳。我们表明模型在四个任务上取得最先进结果，Poly-encoder 比 Cross-encoder 快、比 Bi-encoder 准确，且在与下游任务相似的大型数据集上预训练可获得最佳结果。

**用结构化 dropout 按需缩减 transformer 深度（Reducing transformer depth on demand with structured dropout）**
Angela Fan、Armand Joulin、Edouard Grave
过度参数化的 transformer 网络在机器翻译、语言建模与问答等诸多自然语言处理任务中取得了最先进结果。这些模型包含数亿参数，需要大量计算且容易过拟合。在本工作中，我们探索 LayerDrop——一种结构化 dropout，在训练期间具有正则化效果，并允许在推断时高效剪枝。特别地，我们表明可以从一个大网络中选择任意深度的子网络而无需微调，且对性能影响有限。我们通过改进机器翻译、语言建模、摘要、问答与语言理解基准上的最先进水平，展示了方法的有效性。此外，我们表明该方法相较从头训练或蒸馏能得到质量更高的小型 BERT 类模型。

**RIDE：在程序化生成环境中奖励影响驱动的探索（RIDE: Rewarding impact-driven exploration in procedurally-generated environments）**
Roberta Raileanu、Tim Rocktäschel
稀疏奖励环境中的探索仍是免模型强化学习的关键挑战之一。许多最先进方法不只依赖环境提供的外在奖励，还使用内在奖励鼓励探索。然而我们表明，在智能体不太可能再次访问同一状态的程序化生成环境中，现有方法有所不足。我们提出一种新颖的内在奖励，鼓励智能体采取能显著改变其学到的状态表示的行动。我们在 MiniGrid 的多个富有挑战的程序化生成任务以及以往工作所用的高维观测任务上评估方法。实验表明，该方法比现有探索方法样本效率更高，尤其对程序化生成的 MiniGrid 环境。此外，我们分析了智能体学到的行为及其收到的内在奖励。与以往方法不同，我们的内在奖励在训练过程中不会衰减，并且对与可控物体的交互给予明显更多奖励。

**RTFM：通过阅读泛化到新环境动力学（RTFM: Generalizing to novel environment dynamics via reading）**
Victor Yuan Zhong、Tim Rocktäschel、Edward Grefenstette
在强化学习中获得能泛化到新环境的策略颇具挑战。在本工作中，我们证明通过阅读策略学习器实现的语言理解是泛化到新环境的有前景载体。我们提出一个落地的策略学习问题「Read to Fight Monsters」（RTFM）：智能体必须联合推理语言目标、文档中描述的相关动力学以及环境观测。我们程序化生成环境动力学及相应的动力学语言描述，使智能体必须通过阅读来理解新的环境动力学，而非记忆任何特定信息。此外，我们提出 txt2π——一个捕捉目标、文档与观测之间三方交互的模型。在 RTFM 上，txt2π 通过阅读泛化到训练中未见动力学的新环境。此外，我们的模型在 RTFM 上胜过 FiLM 与语言条件 CNN 等基线。通过课程学习，txt2π 产生在需要多步推理与指代消解的复杂 RTFM 任务上表现卓越的策略。

**SlowMo：用慢动量改进通信高效的 SGD（SlowMo: Improving communication-efficient SGD with slow momentum）**
Jianyu Wang、Vinayak Tantia、Nicolas Ballas、Mike Rabbat
分布式优化对于在大型数据集上训练大模型至关重要。已有多种方法被提出以减少分布式训练中的通信开销，如只在执行多次本地 SGD 步后同步，以及用去中心化方法（如流言算法）解耦工作者之间的通信。尽管这些方法比每次更新前都阻塞通信的 ALLREDUCE 方法运行更快，但在相同更新次数后得到的模型可能精度较低。受 Chen 与 Huo（2016）的 BMUF 方法启发，我们提出慢动量（SLOWMO）框架：工作者在运行多轮基础优化算法后周期性同步并执行一次动量更新。图像分类与机器翻译任务的实验表明，即使把额外开销摊销到多次更新、使 SLOWMO 运行时间与基础优化器相当，SLOWMO 相对基础优化器仍在优化与泛化性能上持续带来改进。我们提供理论收敛保证，证明 SLOWMO 收敛到光滑非凸损失的驻点。由于 BMUF 可以通过 SLOWMO 框架表达，我们的结果也对应 BMUF 的首个理论收敛保证。

**面向时序知识库补全的张量分解（Tensor decompositions for temporal knowledge base completion）**
Timothee Lacroix、Guillaume Obozinski、Nicolas Usunier
大多数关系数据的表示学习与链接预测算法是为静态数据设计的。然而它们所应用的数据通常随时间演化，如社交网络中的好友图或推荐系统中用户与物品的交互。知识库也是如此，它包含只在特定时间点有效的事实，如（美国，总统是，贝拉克·奥巴马，[2009-2017]）。对于时间约束下的链接预测问题（如回答查询（美国，总统是，?，2012）），我们提出一个受四阶张量规范分解启发的解决方案。我们引入新的正则化方案，并提出 ComplEx（Trouillon 等，2016）的一个扩展，取得最先进性能。此外，我们提出一个从 Wikidata 构建的新知识库补全数据集，比以往基准大一个数量级，作为评估时序与非时序链接预测方法的新参照。

**神经网络训练的早期阶段（The early phase of neural network training）**
Jonathan Frankle、David J. Schwab、Ari Morcos
近期研究表明，神经网络学习的许多重要方面发生在训练的最初几次迭代或 epoch 内。例如，稀疏的可训练子网络会出现（Frankle 等，2019），梯度下降进入一个小子空间（Gur-Ari 等，2018），网络经历关键期（Achille 等，2019）。在这里，我们考察深度神经网络在训练早期阶段经历的变化。我们在这些早期迭代中对网络状态进行大量测量，并利用 Frankle 等（2019）的框架定量探查权重分布及其对数据集各层面的依赖。我们发现，在该框架内，深度网络在保持符号的情况下重新随机初始化权重后并不鲁棒，而且即使只有几百次迭代后权重分布也高度非独立。尽管有这些行为，用模糊输入或辅助自监督任务预训练可以近似有监督网络中的变化，表明这些变化并非本质上依赖标签，尽管标签显著加速了这一过程。总之，这些结果有助于阐明这一学习初始关键期间发生的网络变化。

**用贝叶斯神经网络做不确定性引导的持续学习（Uncertainty-guided continual learning with Bayesian neural networks）**
Sayna Ebrahimi、Mohamed Elhoseiny、Trevor Darrell、Marcus Rohrbach
持续学习旨在学习新任务而不遗忘已学任务。当无法访问先前任务的数据且模型容量固定时，这尤其困难。当前基于正则化的持续学习算法需要外部表示与额外计算来度量参数重要性。与之相反，我们提出不确定性引导的持续贝叶斯神经网络（UCB），其学习率根据网络权重概率分布中定义的不确定性自适应调整。不确定性是确定「记住什么、改变什么」的自然方式，从而缓解灾难性遗忘。我们还展示了模型的一个变体，它把不确定性用于权重剪枝，并通过按任务保存二值掩码在剪枝后保持任务性能。我们在具有长短任务序列的多样物体分类数据集上广泛评估 UCB 方法，报告相较现有方法更优或相当的性能。此外，我们表明模型在测试时不一定需要任务信息，即不假定样本属于哪个任务。

**Vid2game：从真实世界视频中提取可控角色（Vid2game: Controllable characters extracted from real-world videos）**
Oran Gafni、Lior Wolf、Yaniv Taigman
我们从一个人执行某活动的视频中提取可控模型。该模型根据任意用户定义的控制信号（通常标记运动身体的位移）生成该人的新图像序列。生成的视频可以有任意背景，并有效捕捉该人的动态与外观。该方法基于两个网络：第一个把当前姿态与单实例控制信号映射到下一姿态；第二个把当前姿态、新姿态与给定背景映射到输出帧。两个网络都包含多种支持高质量性能的创新。这在从舞者与运动员的多种视频中提取的多个角色上得到了展示。

**vq-wav2vec：离散语音表示的自监督学习（vq-wav2vec: Self-supervised learning of discrete speech representations）**
Alexei Baevski、Steffen Schneider、Michael Auli
我们提出 vq-wav2vec，通过 wav2vec 式的自监督上下文预测任务学习音频片段的离散表示。该算法使用 Gumbel-Softmax 或在线 k-means 聚类来量化稠密表示。离散化使 NLP 社区需要离散输入的算法可以直接应用。实验表明，BERT 预训练在 TIMIT 音素分类与 WSJ 语音识别上取得新的最先进水平。

你可以在 Facebook ICLR 页面访问完整论文列表。
