---
title: "Facebook 在 NeurIPS 2018"
title_en: "Facebook at NeurIPS 2018"
date: 2018-12-01
source: https://ai.meta.com/blog/facebook-at-neurips-2018
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 在 NeurIPS 2018

> 原文：[Facebook at NeurIPS 2018](https://ai.meta.com/blog/facebook-at-neurips-2018) · Meta AI（Wayback 存档）

2018 年 12 月 1 日

机器学习与计算神经科学领域的专家将于 12 月 2 日（周日）至 12 月 8 日（周六）齐聚蒙特利尔，参加第三十二届神经信息处理系统年会（NeurIPS）。Facebook 的研究将在口头报告和海报环节中展示。Facebook 的研究员和工程师还将在整个会议期间组织和参与多个研讨会。对于无法到场的人，会议将于 12 月 3 日至 6 日在 NeurIPS 的 Facebook 页面上直播。

## Facebook 在 NeurIPS 2018 上展示的研究

**A²-Nets：双重注意力网络（Double Attention Networks）**
Yunpeng Chen、Yannis Kalantidis、Jianshu Li、Shuicheng Yan、Jiashi Feng
学习捕捉长程依赖关系对图像/视频识别至关重要。现有 CNN 模型通常依赖增加深度来建模此类关系，效率非常低下。在本工作中，我们提出「双重注意力块」（double attention block）这一新颖组件，它从输入图像/视频的整个时空空间中聚合并传播有信息量的全局特征，使后续卷积层能够高效地访问整个空间中的特征。该组件通过两步的双重注意力机制设计：第一步通过二阶注意力池化把整个空间的特征汇聚成一个紧凑集合，第二步通过另一个注意力自适应地选择特征并将其分配到每个位置。所提出的双重注意力块易于采用，可以方便地插入现有的深度神经网络。我们在图像和视频识别任务上进行了大量消融研究和实验以评估其性能。在图像识别任务上，配备双重注意力块的 ResNet-50 在 ImageNet-1k 数据集上以少 40% 以上的参数量和更少的 FLOPs 胜过了大得多的 ResNet-152 架构。在动作识别任务上，我们提出的模型在 Kinetics 和 UCF-101 数据集上取得了最先进的结果，效率显著高于近期工作。

**均值-方差优化的块坐标上升算法（A Block Coordinate Ascent Algorithm for Mean-Variance Optimization）**
Tengyang Xie、Bo Liu、Yangyang Xu、Mohammad Ghavamzadeh、Yinlam Chow、Daoming Lyu、Daesub Yoon
动态决策问题中的风险管理是金融投资、自动驾驶和医疗健康等许多领域的核心关切。均值-方差函数因其简单性和可解释性，是风险管理中使用最广泛的目标函数之一。现有的均值-方差优化算法基于多时间尺度随机近似，其学习率调度往往难以调参，且只有渐近收敛证明。在本文中，我们为均值-方差优化开发了一个免模型的策略搜索框架，并给出有限样本误差界分析（针对局部最优）。我们的出发点是用 Legendre-Fenchel 对偶对原均值-方差函数进行重构，据此提出一种随机块坐标上升策略搜索算法。我们既给出了最后一次迭代解的渐近收敛保证，也给出了随机抽取解的收敛速率，并在多个基准域上验证了其适用性。

**一种基于 Lyapunov 的安全强化学习方法（A Lyapunov-based Approach to Safe Reinforcement Learning）**
Yinlam Chow、Ofir Nachum、Edgar Duenez-Guzman、Mohammad Ghavamzadeh
在许多现实世界的强化学习（RL）问题中，除了优化主目标函数之外，智能体还必须同时避免违反若干约束。尤其是，除了优化性能之外，在训练和部署期间保证智能体的安全至关重要（例如，机器人应避免采取会对其硬件造成不可逆损害的动作——无论是探索性的还是别的）。为了在 RL 中纳入安全性，我们在约束马尔可夫决策过程（CMDP）框架下推导算法——CMDP 是标准马尔可夫决策过程（MDP）的扩展，增加了对期望累积成本的约束。我们的方法基于一种新颖的 Lyapunov 方法。我们定义并给出了一种构造 Lyapunov 函数的方法，它通过一组局部线性约束，为训练期间行为策略的全局安全提供了有效保障。依托这些理论基础，我们展示了如何用 Lyapunov 方法系统地 把动态规划（DP）和 RL 算法转化为其安全版本。为说明其有效性，我们在一个安全基准域的多个 CMDP 规划与决策任务上评估了这些算法。结果表明，我们提出的方法在平衡约束满足与性能方面显著优于现有基线。

**深度学习模型的描述长度（The Description Length of Deep Learning Models）**
Léonard Blier、Yann Ollivier
Solomonoff 的一般推断理论（Solomonoff，1964）与最小描述长度原则（Grünwald，2007；Rissanen，2007）将奥卡姆剃刀形式化，认为数据的好模型是一个擅长无损压缩数据的模型——包括描述模型本身的代价。考虑到需要编码的参数数量庞大，深度神经网络似乎与这一原则相悖。我们通过实验证明，即使把参数编码计算在内，深度神经网络仍然具备压缩训练数据的能力。压缩视角最初推动了变分方法在神经网络中的应用（Hinton 与 Van Camp，1993；Schmidhuber，1997）。出乎意料的是，我们发现这些变分方法尽管是专为最小化此类界而构建的，提供的压缩界却出奇地差。这或许可以解释变分方法在深度学习中相对欠佳的实际表现。另一方面，简单的增量编码方法在深度网络上产生了极佳的压缩值，印证了 Solomonoff 的思路。

**Kronecker 分解特征基中的快速近似自然梯度下降（Fast Approximate Natural Gradient Descent in a Kronecker Factored Eigenbasis）**
Thomas George、César Laurent、Xavier Bouthillier、Nicolas Ballas、Pascal Vincent
利用梯度协方差信息的优化算法（如自然梯度下降的变体，Amari，1998）有望产生更有效的下降方向。对于参数量庞大的模型，它们所依赖的协方差矩阵会变得极其巨大，使其无法以原始形式应用。这推动了对简单的对角近似和更精细的分解近似（如 KFAC，Heskes，2000；Martens 与 Grosse，2015；Grosse 与 Martens，2016）的研究。在本工作中，我们从两者中汲取灵感，提出一种可证明优于 KFAC、且支持廉价部分更新的新颖近似。它的做法是追踪一个对角方差——但不是在参数坐标系中，而是在一个 Kronecker 分解的特征基中，在该基下对角近似可能更为有效。实验表明，在多种深度网络架构上，优化速度相比 KFAC 有所提升。

**用线性强化学习对抗推荐系统中的厌倦感（Fighting Boredom in Recommender Systems with Linear Reinforcement Learning）**
Romain Warlop、Alessandro Lazaric、Jérémie Mary
推荐系统（RS）中一个常见的假设是存在一个最优的固定推荐策略。这种策略可以很简单、工作在物品层面（例如，多臂老虎机假设存在一个最优的固定臂/物品），也可以实现更复杂的推荐系统（例如，A/B 测试的目标是找到最优的固定推荐系统并在此后一直执行它）。我们论证这一假设在实践中很少成立，因为推荐过程本身会影响用户的偏好。例如，用户可能对某个策略感到厌倦，而如果距上次使用该策略已过足够长的时间，其兴趣可能恢复。在这种情况下，更好的做法是以合适的频率交替使用不同方案，以充分挖掘其潜力。在本文中，我们首先把问题表述为一个马尔可夫决策过程，其中奖励是近期动作历史的线性函数，并证明考虑推荐长期影响的策略可以同时优于固定动作策略和上下文贪心策略。接着，我们引入 UCRL 算法的扩展（LINUCRL），在未知环境中有效平衡探索与利用，并推导出一个与状态数无关的遗憾界。最后，我们在多个现实场景中实证验证了模型假设与算法。

**部分可观测策略游戏的前向建模——《星际争霸》去战争迷雾器（Forward Modeling for Partial Observation Strategy Games – A StarCraft Defogger）**
Gabriel Synnaeve、Zeming Lin、Jonas Gehring、Dan Gant、Vegard Mella、Vasil Khalidov、Nicolas Carion、Nicolas Usunier
我们把「去迷雾」（defogging）问题表述为：在即时战略游戏场景下，基于既往的部分观测进行状态估计与未来状态预测。我们提议为此采用编码器-解码器神经网络，并引入代理任务与评估基线，以评估其捕捉基本游戏规则和高层动态的能力。通过结合卷积神经网络与循环网络，我们利用空间与序列相关性，在一个大型《星际争霸®：母巢之战®》人类对战数据集上训练出了性能良好的模型。最后，我们把模型应用于一个最先进的基于规则的《星际争霸》机器人中的敌方单位预测，证明了它与下游任务的相关性。我们观察到其对多个强劲社区机器人的胜率有所提升。

**GLoMo：以无监督学习的关系图作为可迁移表示（GLoMo: Unsupervisedly Learned Relational Graphs as Transferable Representations）**
Zhilin Yang、Jake Zhao、Bhuwan Dhingra、Kaiming He、William Cohen、Ruslan Salakhutdinov、Yann LeCun
现代深度迁移学习方法主要聚焦于从一个任务中学习可迁移到其他任务的通用特征向量，如语言中的词嵌入和视觉中的预训练卷积特征。然而，这些方法通常迁移的是一元特征，很大程度上忽略了更结构化的图表示。这项工作探索了从大规模无标注数据中学习捕捉成对数据单元（如词或像素）之间依赖关系的通用潜在关系图，并将这些图迁移到下游任务的可能性。我们提出的迁移学习框架在问答、自然语言推理、情感分析和图像分类等多种任务上提升了性能。我们还表明，学到的图足够通用，可以迁移到训练时未使用过的不同嵌入上（包括 GloVe 嵌入、ELMo 嵌入以及任务专用 RNN 隐藏单元），或无嵌入的单元（如图像像素）。

**非连通马尔可夫决策过程中接近最优的探索-利用（Near Optimal Exploration-Exploitation in Non-Communicating Markov Decision Processes）**
Ronan Fruit、Matteo Pirotta、Alessandro Lazaric
在设计 MDP 的状态空间时，通常会把瞬态状态或任何策略都不可达的状态包含进来（例如，在山车问题中，速度与位置的乘积空间包含物理上不可达的构型）。这会导致弱连通或多链 MDP。在本文中，我们提出 TUCRL——首个能够在任意有限马尔可夫决策过程（MDP）中进行高效探索-利用而无需任何形式先验知识的算法。具体而言，对于具有 SC 个连通状态、A 个动作和最多 ΓC 个可达连通后继状态的 MDP，我们推导出 Õ(D_C √(Γ_C S C A T)) 的遗憾界，其中 D_C 是 MDP 连通部分的直径（即任意两状态之间最长最短路径的长度）。与之形成对比的是：现有的乐观算法（如 UCRL、Optimistic PSRL）在弱连通 MDP 中会遭受线性遗憾；而后验采样或正则化算法（如 REGAL）则需要关于最优策略偏差跨度的先验知识才能达到次线性遗憾。我们还证明，在弱连通 MDP 中，任何算法若不先在随 MDP 参数呈指数级增长的步数上遭受线性遗憾，就不可能实现遗憾的对数增长。最后，我们报告了支持理论发现的数值模拟，并展示了 TUCRL 如何克服现有技术的局限。

**用 VAE 做非对抗映射（Non-Adversarial Mapping with VAEs）**
Yedid Hoshen
无监督跨域映射的研究近来备受关注。近期进展很大程度上得益于对抗训练与循环约束的使用。对抗训练在实践中的困难促使人们研究非对抗方法。在近期的一篇论文中，有人证明不使用循环或 GAN 也可以进行跨域映射。该方法虽有前景，但存在若干缺点，包括推断成本高昂，以及每个训练样本都对应一个优化变量，导致方法无法使用大型训练集。我们提出一种替代方法，能够用一种新颖形式的变分自编码器实现非对抗映射。我们的方法在推断时快得多，能够利用大型数据集，且解释简单。

**单样本无监督跨域翻译（One-Shot Unsupervised Cross Domain Translation）**
Sagie Benaim、Lior Wolf
给定来自域 A 的单张图像 x 以及来自域 B 的一组图像，我们的任务是生成 x 在 B 中的对应物。我们论证，这一任务可能是一项关键的 AI 能力，是认知智能体在世界中行动能力的基础，并给出经验证据表明现有的无监督域翻译方法无法胜任该任务。我们的方法分两步：首先，训练一个针对域 B 的变分自编码器；然后，给定新样本 x，通过调整靠近图像的层来直接拟合 x，从而创建一个针对域 A 的变分自编码器，而其他层只被间接调整。实验表明，新方法在仅用单个样本 x 训练时，效果与享有域 A 大量训练样本的现有域迁移方法相当。我们的代码已在 https://github.com/sagiebenaim/OneShotTranslation 公开。

**SING：符号到乐器的神经生成器（SING: Symbol-to-Instrument Neural Generator）**
Alexandre Defossez、Neil Zeghidour、Nicolas Usunier、Leon Bottou、Francis Bach
深度学习在音频合成方面的最新进展，为直接生成波形的模型铺平了道路，使其从依赖声码器或 MIDI 合成器进行语音或音乐生成的传统范式转向。尽管取得了成功，但 WaveNet 和 SampleRNN [24, 17] 等当前最先进的神经音频合成器训练与推断时间高得惊人，因为它们基于自回归模型，以 16kHz 的速率逐个生成音频样本。在本工作中，我们研究一种计算效率更高的替代方案：以大步长逐帧生成波形。我们提出 SING，一个轻量级神经音频合成器，面向一项新任务：在给定乐器、音高和力度的情况下生成音符。借助一种新的损失函数——最小化生成波形与目标波形对数频谱图之间的距离，我们的模型可以用单一解码器端到端地训练，生成近 1000 种乐器的音符。在为训练中未见过的音高-乐器组合合成音符的泛化任务上，以平均意见得分（MOS）衡量，SING 生成的音频相较基于 WaveNet 的最先进自编码器 [4] 在感知质量上有显著提升，且训练约快 32 倍、推断约快 2500 倍。SING 音频样本（见原文页面）。

**马尔可夫决策过程的时间正则化（Temporal Regularization for Markov Decision Process）**
Pierre Thodoroff、Audrey Durand、Joelle Pineau、Doina Precup
强化学习的若干应用会因高方差而出现不稳定，这在高维领域尤为普遍。正则化是机器学习中常用的降低方差的技术，代价是引入一些偏差。现有正则化技术大多关注空间（感知）正则化。然而在强化学习中，由于贝尔曼方程的性质，还有机会利用基于轨迹上价值估计平滑性的时间正则化。本文探讨了一类时间正则化方法。我们用马尔可夫链概念正式刻画了这一技术引入的偏差，并通过一系列简单的离散与连续 MDP 展示时间正则化的各种特性，同时表明该技术即便在高维 Atari 游戏中也能带来改进。

## NeurIPS 2018 的其他活动

**AI for Social Good 研讨会**
论文：《From Satellite Imagery to Disaster Insights》——Jigar Doshi、Saikat Basu、Guan Pang

**宣布第二届对话智能挑战赛（ConvAI2）获胜者**
团队：Mikhail Burtsev、Varvara Logacheva、Valentin Malykh、Ryan Lowe、Iulian Serban、Shrimai Prabhumoye、Emily Dinan、Douwe Kiela、Alexander Miller、Kurt Shuster、Arthur Szlam、Jack Urbanek、Jason Weston
顾问委员会：Yoshua Bengio、Alan W. Black、Joelle Pineau、Alexander Rudnicky、Jason Williams

**贝叶斯深度学习研讨会**
论文：《Bayesian Neural Networks using HackPPL with Application to User Location State Prediction》——Beliz Gokkaya、Jessica Ai、Michael Tingley、Yonglong Zhang、Ning Dong、Thomas Jiang、Anitha Kubendran、Arun Kumar

**贝叶斯非参数研讨会**
Ben Letham，受邀讲者

**Black in AI 研讨会**
Yann Dauphin，讲者

**因果学习研讨会**
论文：《Causality in Physics and Effective Theories of Agency》——Dan Roberts、Max Kleiman-Weiner

**持续学习研讨会**
Marc'Aurelio Ranzato，讲者

**对话式 AI 研讨会**
论文：《Cross-lingual contextual word representations for multilingual slot filling》——Sonal Gupta、Rushin Shah、Sebastian Shuster
论文：《Improving Semantic Parsing for Task Oriented Dialog》——Arash Einolghozati

**机器学习趋势的批评与修正研讨会**
Kim Hazelwood，受邀讲者

**深度强化学习研讨会**
Joelle Pineau，组织者；Yann LeCun，讲者
论文：《Deep Counterfactual Regret Minimization》——Noam Brown、Adam Lerer、Sam Gross、Tuomas Sandholm

**AI 的伦理、社会与治理问题研讨会**
Sarah Bird、Isabel Kloumann、Dario Garcia，组织者

**涌现通信研讨会**
Douwe Kiela、Kyunghyun Cho，组织者
论文：《Learning to communicate at scale in multiagent cooperative and competitive tasks》——Amanpreet Singh、Tushar Jain、Sainbayar Sukhbaatar

**深度学习理论整合研讨会**
论文：《SGD Implicitly Regularizes Generalization Error》——Dan Roberts

**依令学习研讨会**
Jason Weston，讲者

**面向创意与设计的机器学习研讨会**
Yaniv Taigman，讲者

**面向分子与材料的机器学习研讨会**
Kyunghyun Cho，讲者

**部分可观测下的强化学习研讨会**
Joelle Pineau，讲者
论文：《High-Level Strategy Selection under Partial Observability in StarCraft: Brood War》——Jonas Gehring、Da Ju、Vegard Mella、Daniel Gant、Nicolas Usunier、Gabriel Synnaeve
论文：《Learning Minimal Sufficient Representations of Partially Observable Decision Processes》——Tommaso Furlanello、Amy Zhang、Kamyar Azizzadenesheli、Anima Anandkumar、Zachary C. Lipton、Laurent Itti、Joelle Pineau

**关系表示学习研讨会**
Maximilian Nickel，讲者
论文：《Compositional Language Understanding with Text-based Relational Reasoning》——Koustuv Sinha、Shagun Sodhani、William L. Hamilton、Joelle Pineau

**可复现、可重用、鲁棒的强化学习（受邀报告）**
Joelle Pineau
摘要：近年来，深度强化学习取得了显著成就。然而，复现最先进深度强化学习方法的结果绝非易事。某些方法的高方差会让学习在环境或奖励高度随机时格外困难。此外，结果可能对领域或实验流程中的轻微扰动十分脆弱。在本报告中，我将回顾深度强化学习实验技术与报告流程中出现的挑战，并介绍若干旨在让未来结果更可复现、可重用且鲁棒的最新成果与指导原则。

**Facebook NLP 应用的研究到生产（Expo 研讨会）**
教程：《Using PyTorch 1.0 Hybrid Frontend to Train and Export a seq2seq model》——James Cross、Xian Li、Myle Ott、Juan Miguel Pino

**第二届对话式 AI 研讨会**
Alborz Geramifard，主席

**平滑博弈优化与机器学习研讨会**
论文：《A Variational Inequality Perspective on GANs》——Gauthier Gidel、Hugo Berard、Gaëtan Vignoud、Pascal Vincent、Simon Lacoste-Julien

**机器学习系统研讨会**
Kim Hazelwood，受邀讲者；Aparna Lakshmiratan、Sarah Bird，组织委员会
论文：《AE: A domain-agnostic platform for adaptive experimentation》——Eytan Bakshy、Lili Dworkin、Brian Karrer、Kostya Kashin、Ben Letham、Ashwin Murthy、Shaun Singh
论文：《Explore-Exploit: A Framework for Interactive and Online Learning》——Honglei Liu、Anuj Kumar、Wenhai Yang、Benoit Dumoulin
论文：《Pythia – A platform for vision and language research》——Amanpreet Singh、Vivek Natarajan、Yu Jiang、Meet Shah、Xinlei Chen、Marcus Rohrbach、Dhruv Batra、Devi Parikh
论文：《Rethinking floating point for deep learning》——Jeff Johnson
论文：《Stochastic Gradient Push for Distributed Deep Learning》——Mido Assran、Nicolas Loizou、Nicolas Ballas、Mike Rabbat
论文：《Training with Low-precision Embedding Tables》——Jian Zhang、Jiyan Yang、Hector Yuen

**无监督深度学习研讨会**
Marc'Aurelio Ranzato，联合讲者

**视觉落地交互与语言（ViGIL）研讨会**
Dhruv Batra、Devi Parikh，组织者；Douwe Kiela，讲者
论文：《Embodied Question Answering in Photorealistic Environments with Point Cloud Perception》——Erik Wijmans、Samyak Datta、Oleksandr Maksymets、Abhishek Das、Georgia Gkioxari、Stefan Lee、Irfan Essa、Dhruv Batra、Devi Parikh

**Wordplay：基于文本游戏的强化与语言学习研讨会**
Jason Weston，讲者

**女性机器学习工作者研讨会**
Amy Zhang、Aude Hofleitner，组织者
