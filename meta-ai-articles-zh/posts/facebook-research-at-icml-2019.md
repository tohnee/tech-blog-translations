---
title: "Facebook 研究团队在 ICML 2019"
title_en: "Facebook Research at ICML 2019"
date: 2019-03-15
source: https://ai.facebook.com/blog/facebook-research-at-icml-2019
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 研究团队在 ICML 2019

> 原文：[Facebook Research at ICML 2019](https://ai.facebook.com/blog/facebook-research-at-icml-2019) · Meta AI（Wayback 存档）

本周，来自世界各地的机器学习专家齐聚长滩，参加 2019 年国际机器学习会议（ICML）。Facebook 的研究将在口头 spotlight 和集体海报环节展示。我们的研究员和工程师还将在本周参与其他活动，包括从「面向机器人与 AI 的生成建模与基于模型的推理」到「自监督学习」等多个研讨会。作为促进领域多元化承诺的一部分，Facebook AI 还联合赞助 ICML 的另外两项活动：女性机器学习工作者（WiML）晚宴与 Latinx in AI 研讨会。参加 ICML 的人请务必访问 Facebook Research 展位，进一步了解我们在做的工作。

## Facebook 在 ICML 上展示的研究

**完全可微的束搜索解码器（A Fully Differentiable Beam Search Decoder）**
Ronan Collobert、Awni Hannun、Gabriel Synnaeve
我们引入一个新的完全可微的束搜索解码器，使训练时通过推断过程进行优化成为可能。我们的解码器允许组合在不同粒度上运行的模型（如声学与语言模型）。它可以通过考虑目标序列与输入序列之间的所有可能对齐，用于二者不对齐的情形。我们通过把方法应用于语音识别、联合训练声学与词级语言模型，展示了其可扩展性。该系统是端到端的，梯度从词级转录贯穿整个架构流动。近期研究表明，带注意力机制的深度神经网络可以从最终转录成功训练声学模型，同时隐式学习语言模型。我们则表明，可以把声学模型与显式的、可能预训练过的语言模型联合判别训练。

**AdaGrad 步长：非凸地形上的尖锐收敛（AdaGrad Stepsizes: Sharp Convergence Over Non-convex Landscapes）**
Rachel Ward、XiaoXia Wu、Leon Bottou
AdaGrad 及其变体等自适应梯度方法，根据沿途收到的梯度即时更新随机梯度下降的步长；这类方法因收敛稳健、无需微调步长调度等参数，在大规模优化中得到广泛应用。然而，迄今为止 AdaGrad 的理论保证仅限于在线与凸优化。我们通过为 AdaGrad 在光滑非凸地形上的收敛提供强理论保证来弥合这一差距。我们证明，AdaGrad 的范数版本（AdaGrad-Norm）在随机设置下以 Õ(log(N)/√N) 的速率收敛到驻点，在批（非随机）设置下以最优的 Õ(1/N) 速率收敛——从这个意义上说，我们的收敛保证是「尖锐」的。特别是，我们的理论结果与大量数值实验都表明，AdaGrad-Norm 对未知的 Lipschitz 常数与梯度随机噪声水平具有鲁棒性。

**深度反事实遗憾最小化（Deep Counterfactual Regret Minimization）**
Noam Brown、Adam Lerer、Sam Gross、Tuomas Sandholm
反事实遗憾最小化（CFR）是求解大型不完美信息博弈的主导框架。它通过迭代遍历博弈树收敛到均衡。为处理极其庞大的博弈，通常在运行 CFR 之前先做抽象。抽象后的博弈用表格式 CFR 求解，其解再映射回完整博弈。这一过程可能有问题：抽象的诸多方面往往是手工且领域特定的，抽象算法可能遗漏博弈的重要策略细节，而且存在鸡生蛋蛋生鸡的问题——确定好的抽象需要知道博弈的均衡。本文引入深度反事实遗憾最小化——一种 CFR 形式，用深度神经网络近似 CFR 在完整博弈中的行为，从而免去抽象的需要。我们表明 Deep CFR 有原则依据，并在大型扑克博弈中取得强劲性能。这是首个在大型博弈中取得成功的非表格 CFR 变体。

**从原始选择数据中发现上下文效应（Discovering Context Effects from Raw Choice Data）**
Arjun Seshadri、Alex Peysakhovich、Johan Ugander
偏好学习中的许多应用假设决策来自稳定效用函数的最大化。然而大量实验文献表明，个体选择与判断会受到其所处上下文中「无关」方面的影响。这类上下文的重要一类是选择集的构成。在本工作中，我们的目标是从原始选择数据中发现这类选择集效应。我们引入多项 Logit（MNL）模型的一个扩展——上下文相关随机效用模型（CDM），它允许特定一类选择集效应。我们表明 CDM 可视为对一般选择系统的二阶近似，可用最大似然最优推断，且重要的是易于解释。我们把 CDM 应用于真实与模拟选择数据，对选择集效应的存在进行有原则的探索性分析。

**ELF OpenGo：AlphaZero 的分析与开源再实现（ELF OpenGo: An Analysis and Open Reimplementation of AlphaZero）**
Yuandong Tian、Jerry Ma、Qucheng Gong、Shubho Sengupta、Zhuoyuan Chen、James Pinkerton、Larry Zitnick
AlphaGo、AlphaGo Zero 与 AlphaZero 系列算法是深度强化学习能力的杰出示范，在复杂的围棋游戏中以逐步提高的自主性取得了超人类性能。然而，研究社区在理解和使用这些有前景的方法上仍存在许多障碍。为阐明未解之谜并促进未来研究，我们提出 ELF OpenGo——AlphaZero 算法的开源再实现。ELF OpenGo 是首个以对全球顶尖职业棋手完美（20:0）战绩令人信服地展示超人类性能的开源围棋 AI。我们用 ELF OpenGo 进行了大量消融研究，并识别与分析了模型训练与对弈推断过程中的许多有趣现象。我们的代码、模型、自我博弈数据集与辅助数据均已公开。

**神经网络的一阶对抗脆弱性与输入维度（First-Order Adversarial Vulnerability of Neural Networks and Input Dimension）**
Carl-Johann Simon-Gabriel、Yann Ollivier、Bernhard Scholkopf、Leon Bottou、David Lopez-Paz
过去几年，神经网络被证明容易受到对抗图像攻击：有针对性但不可察觉的图像扰动导致截然不同的预测。我们表明，对抗脆弱性随训练目标（视为输入的函数）的梯度增大而增大。令人惊讶的是，脆弱性并不依赖网络拓扑：对许多标准网络架构，我们证明在初始化时这些梯度的 l1 范数随输入维度的平方根增长，使网络随图像尺寸增大而愈发脆弱。我们实证表明，这种维度依赖在常规或鲁棒训练后仍然存在，但随更强正则化而减弱。

**垃圾进，奖励出：多臂老虎机中的自举探索（Garbage In, Reward Out: Bootstrapping Exploration in Multi-Armed Bandits）**
Branislav Kveton、Csaba Szepesvari、Sharan Vaswani、Zheng Wen、Mohammad Ghavamzadeh、Tor Lattimore
我们提出一种通过随机化奖励历史来进行探索的赌博机算法。具体而言，它拉动在「带伪奖励的历史」的非参数自举样本中平均奖励最高的臂。我们设计伪奖励，使自举均值以足够高的概率保持乐观。我们把算法称为 Giro，即「垃圾进，奖励出」。我们在伯努利赌博机中分析 Giro，推导出 n 轮遗憾的 O(K∆⁻¹ log n) 界，其中 ∆ 是最优臂与最佳次优臂期望奖励之差，K 是臂数。我们探索设计的主要优势是易于推广到结构化问题。为说明这一点，我们提出带任意奖励泛化模型的上下文 Giro。我们在多个合成与真实问题上评估 Giro 及其上下文变体，观察到其表现良好。

**GDPP：用行列式点过程学习多样生成（GDPP: Learning Diverse Generations Using Determinental Point Processes）**
Mohamed Elfeki、Camille Couprie、Morgane Rivière、Mohamed Elhoseiny
生成模型已被证明是表示高维概率分布与生成逼真图像的出色工具。生成模型的一个基本特征是产出多模态输出的能力。然而在训练时，它们常容易发生模式崩溃，即模型在把输入噪声映射到真实数据分布的少数几个模式上受限。在本文中，我们从行列式点过程（DPP）汲取灵感，实现一个缓解模式崩溃并产生更高质量样本的生成模型。DPP 是一种优雅的概率度量，用于建模子集内的负相关从而量化其多样性。我们用 DPP 核建模真实数据与合成数据中的多样性，然后设计一个生成惩罚项，鼓励合成器合成与真实数据相似多样性的数据。与往往使用额外可训练参数或复杂训练范式的此前最先进生成模型不同，我们的方法不改变原训练方案。嵌入对抗训练与变分自编码器后，我们的生成式 DPP 方法在多种合成数据与自然图像数据集上一致抵抗模式崩溃，同时在数据效率、收敛时间与生成质量上胜过最先进方法。代码将公开。

**GEOMetrics：为图编码物体利用几何结构（GEOMetrics: Exploiting Geometric Structure for Graph-Encoded Objects）**
Edward J. Smith、Scott Fujimoto、Adriana Romero、Dave Meger
网格模型是编码 3D 物体结构的有前景途径。当前的网格重建系统通过一系列图卷积预测预定义图上均匀分布的顶点位置，导致在性能或分辨率上做出妥协。在本文中，我们论证几何物体的图表示允许额外结构，应当加以利用以增强重建。因此，我们提出一个恰当受益于图编码物体几何结构优势的系统，引入：（1）保留顶点信息的图卷积更新；（2）允许细节涌现的自适应分裂启发式；（3）同时在顶点定义的局部表面与网格定义的全局结构上运行的训练目标。所提方法在 ShapeNet 数据集的图像 3D 物体重建任务上评估，无论视觉还是数值都展示了最先进性能，同时通过生成自适应网格使空间需求小得多。

**让深度 Q 学习方法对时间离散化鲁棒（Making Deep Q Learning Methods Robust to Time Discretization）**
Corentin Tallec、Léonard Blier、Yann Ollivier
尽管成果显著，深度强化学习（DRL）对超参数化、实现细节或环境微小变化并不鲁棒（Henderson 等 2017，Zhang 等 2018）。克服这种敏感性是让 DRL 适用于现实问题的关键。在本文中，我们把对近连续时间环境中时间离散化的敏感性识别为关键因素；这涵盖例如更改每秒帧数或控制器的动作频率。实证上，我们发现基于 Q 学习的方法（如深度 Q 学习（Mnih 等，2015）与深度确定性策略梯度（Lillicrap 等，2015））在小时间步下崩溃。形式上，我们证明 Q 学习在连续时间中不存在。我们详述了一种有原则的方法来构建在广泛时间离散化范围内产生相似性能的离策略 RL 算法，并实证确认了这种鲁棒性。

**流形 Mixup：通过插值隐藏状态学习更好表示（Manifold Mixup: Learning Better Representations by Interpolating Hidden States）**
Vikas Verma、Alex Lamb、Christopher Beckham、Amir Najafi Sharif、Ioannis Mitliagkas、David Lopez-Paz、Yoshua Bengio
深度神经网络擅长学习训练数据，但在稍有不同的测试样本上评估时，常给出错误且自信的预测，包括分布偏移、离群点与对抗样本。为解决这些问题，我们提出流形 Mixup——一个简单的正则化器，鼓励神经网络对隐藏表示的插值预测得更不自信。流形 Mixup 把语义插值作为额外训练信号，得到在多个表示层级上决策边界更平滑的神经网络。因此，用流形 Mixup 训练的神经网络学到更平坦的类表示，即方差方向更少。我们证明了在理想条件下这种平坦化为何发生的理论，在实际情况中实证验证，并将其与此前关于信息论与泛化的工作联系起来。尽管不产生显著计算开销、只用几行代码实现，流形 Mixup 在有监督学习、对单步对抗攻击的鲁棒性以及测试对数似然上改进了强基线。

**面向多样机器翻译的混合模型：实战技巧（Mixture Models for Diverse Machine Translation: Tricks of the Trade）**
Tianxiao Shen、Myle Ott、Michael Auli、Marc'Aurelio Ranzato
通过 EM 训练的混合模型是机器学习文献中最简单、使用最广、理解最深的隐变量模型之一。令人惊讶的是，这些模型在机器翻译等文本生成应用中几乎未被探索。原则上，它们提供了一个控制生成的隐变量，并能产生多样的假设集合。然而实践中，混合模型容易退化——常常只有一个组件得到训练，或隐变量被干脆忽略。我们发现，禁用责任计算中的 dropout 噪声对成功训练至关重要。此外，参数化、先验分布、硬 EM 对软 EM、在线对离线分配等设计选择会极大影响模型性能。我们开发了一个评估协议，对照多个参考评估生成的质量与多样性，并对多种混合模型变体进行了详尽的实证研究。我们的分析表明，某些类型的混合模型更鲁棒，相较变分模型与多样解码方法，在翻译质量与多样性之间提供最佳权衡。

**用弱监督做视频多模态内容定位（Multi-modal Content Localization in Videos Using Weak Supervision）**
Gourab Kundu、Prahal Arora、Ferdi Adeputra、Polina Kuznetsova、Daniel McKinnon、Michelle Cheung、Larry Anazia、Geoffrey Zweig
识别视频中包含与某类别或任务相关内容的时间片段，是一个困难而有趣的问题，在细粒度视频索引与检索中有应用。该问题的部分困难来自监督缺失，因为大规模标注包含感兴趣内容的定位片段非常昂贵。在本文中，我们提议用分配给整个视频的类别作为模型的弱监督。利用这种弱监督，我们的模型学习联合进行视频级分类与视频类别相关内容的定位。这可以看作既提供分类标签，又以视频相关区域的形式提供解释。在大规模数据集上的大量实验表明，我们的模型无需任何直接监督即可取得良好定位性能，并能组合语音与视觉等多种模态的信号。

**非单调顺序文本生成（Non-Monotonic Sequential Text Generation）**
Sean Welleck、Kianté Brantley、Hal Daumé III、Kyunghyun Cho
标准顺序生成方法假设预先指定生成顺序，如从左到右生成词的文本生成方法。在本工作中，我们提出一个训练以非单调顺序运行的文本生成模型的框架；模型直接学习好的顺序，无需任何额外标注。我们的框架通过在任意位置生成一个词，然后递归生成其左侧的词再生成右侧的词，产出一棵二叉树。学习被框定为模仿学习，包括一种从模仿 oracle 转向强化策略自身偏好的「指导」方法。实验结果表明，用所提方法可以学到无需预指定生成顺序的文本生成策略，同时取得与常规从左到右生成相当的性能。

**面向可解释视觉问答的概率神经-符号模型（Probabilistic Neural-Symbolic Models for Interpretable Visual Question Answering）**
Ramakrishna Vedantam、Karan Desai、Stefan Lee、Marcus Rohrbach、Dhruv Batra、Devi Parikh
我们提出一类新的概率神经-符号模型，把符号化函数程序作为潜在随机变量。在视觉问答的语境中实例化后，我们的概率表述相较以往的 VQA 神经-符号模型有两大概念优势。第一，我们模型生成的程序更易理解，同时需要的示教样本更少。第二，我们表明可以向模型提出反事实场景，以探查它对「给定图像与指定答案，哪些程序可能导致该答案」的信念。我们在 CLEVR 与 SHAPES 数据集上的结果验证了我们的假设，表明模型即使在低数据情形下也能取得更好的程序（与答案）预测精度，并允许探查推理的一致性与连贯性。

**通过分歧的自监督探索（Self-Supervised Exploration via Disagreement）**
Deepak Pathak、Dhiraj Gandhi、Abhinav Gupta
探索一直是感觉运动控制的基于模型与免模型学习方法中的长期问题。近年来在视频游戏与仿真等无噪声、非随机领域取得了重大进展。然而，当前大多数公式在存在随机动力学时会陷入困境。在本文中，我们受主动学习文献的工作启发，提出一种探索公式。具体而言，我们训练一个动力学模型集成，并激励智能体最大化这些集成的分歧或方差。我们表明该公式在非随机场景与其他公式表现相当，并在带随机动力学的场景中探索得更好。此外，我们表明该目标可用于执行可微策略优化，从而得到样本高效的探索策略。我们在大量标准环境上展示实验，证明该方法的效力。此外，我们在一个真实机器人上实现了我们的探索算法，它完全从零开始学会与物体交互。

**跨时间尺度分离价值函数（Separating Value Functions Across Time-Scales）**
Joshua Romoff、Peter Henderson、Ahmed Touati、Emma Brunskill、Joelle Pineau、Yann Ollivier
在许多有限视野回合式强化学习（RL）设置中，优化无折扣回报是可取的——例如在 Atari 等设置中，目标是长期存活的同时收集最多分数。然而，以该目标学习在数学上可能困难（甚至不可解）。因此，常应用时间折扣来在更短的有效规划视野上优化，代价是可能使优化目标偏离无折扣目标。在这种偏差不可接受的设置中——系统必须在更高折扣下为更长时间视野优化——价值函数逼近器的目标方差可能增大，导致学习困难。我们提出时间差分（TD）学习的一个扩展，称为 TD(∆)，把价值函数分解为一系列基于较小折扣因子价值函数之间差异的分量。把更长时间视野的价值函数分离为这些分量，在可扩展性与性能上具有有用性质。我们讨论这些性质，并在某些设置中展示相对标准 TD 学习的理论与实证改进。

**面向分布式深度学习的随机梯度推送（Stochastic Gradient Push for Distributed Deep Learning）**
Mahmoud Assran、Nicolas Loizou、Nicolas Ballas、Mike Rabbat
分布式数据并行算法旨在通过跨多个节点并行计算大 mini-batch 梯度更新，加速深度神经网络的训练。使用精确分布式平均（如通过 ALLREDUCE）同步节点的方法对落后者与通信延迟敏感。PUSHSUM 流言算法对这些问题鲁棒，但只执行近似分布式平均。本文研究随机梯度推送（SGP），把 PUSHSUM 与随机梯度更新相结合。我们证明 SGP 以与 SGD 相同的次线性速率收敛到光滑非凸目标的驻点，且所有节点达成共识。我们在图像分类（ResNet-50、ImageNet）与机器翻译（Transformer、WMT'16 英德）工作负载上实证验证了 SGP 的性能。代码将公开。

**TarMAC：有针对性的多智能体通信（TarMAC: Targeted Multi-Agent Communication）**
Abhishek Das、Théophile Gervet、Joshua Romoff、Dhruv Batra、Devi Parikh、Mike Rabbat、Joelle Pineau
我们提出一个面向多智能体强化学习的有针对性通信架构：智能体在部分可观测环境中执行合作任务时，既学习发送什么消息，也学习把消息发给谁。这种定向行为完全从下游任务特定奖励中学得，无需任何通信监督。我们还为其增加了多轮通信方法：智能体在环境中采取行动之前，通过多轮通信进行协调。我们在多种合作多智能体任务上评估方法——难度各异、智能体数量不同、环境从 2D 形状网格布局与模拟交通路口到 3D 室内环境——并展示了定向通信与多轮通信的益处。此外，我们表明智能体学到的定向通信策略可解释且直观。最后，我们表明该架构可以轻松扩展到混合与竞争环境，相较近期最先进方法带来性能与样本复杂度的改进。

**神经序列模型的序列集合可训练解码（Trainable Decoding of Sets of Sequences for Neural Sequence Models）**
Ashwin Vijayakumar、Peter Anderson、Stefan Lee、Dhruv Batra
许多序列预测任务允许有多个正确输出，因此解码出一个按某任务特定集合级指标最大化价值的输出集合往往很有用。然而，把为预测单一最佳输出定制的标准序列预测流程改用于此，往往产生包含非常相似序列的集合，无法捕捉输出空间中的变化。为解决这一问题，我们提出 ∇BS——一个可训练的解码流程，输出按指标评价高度有价值的序列集合。我们的方法紧密整合训练与解码阶段，并进一步允许优化任务特定指标，解决标准序列预测的不足。此外，我们讨论了常用集合级指标的权衡，并提出了一个能自然评估「捕捉输出空间变化」这一概念的新集合级指标。最后，我们在图像描述任务上给出结果，发现我们的模型胜过标准技术与自然消融。

**不可复现的研究是可复现的（Unreproducible Research Is Reproducible）**
Xavier Bouthillier、César Laurent、Pascal Vincent
标题中明显的矛盾是对「可复现」一词在不同科学领域被赋予不同含义的文字游戏。我们想表达的是：不可复现的发现可以建立在可复现的方法之上。在不否认促进方法复现的重要性的同时，我们认为有必要重申：发现的复现是科学探究的基本步骤。我们论证，追求方法与数值结果的轻松确定性复现这一值得称赞的目标，不应让我们忘记更重要的必要性——通过恰当考虑本质的变异来源，确保经验结论与发现的可复现性。我们提供实验来例证深度学习领域当前模型评估常见实践的脆弱性，表明即使结果可以复现，稍有不同的实验也不支持这些发现。我们希望帮助厘清深度学习领域探索性研究与经验研究的区别，并相信我们社区应投入更多精力于恰当的经验研究。这项工作是一次推广更严谨、更多样化方法学的尝试，不是要强加新方法学，也不是对探索性研究本质的批评。

**白盒对黑盒：成员推断的贝叶斯最优策略（White-box vs. Black-box: Bayes Optimal Strategies for Membership Inference）**
Alexandre Sablayrolles、Matthijs Douze、Yann Ollivier、Cordelia Schmid、Hervé Jegou
成员推断是指：给定一个样本与机器学习模型训练好的参数，判断该样本是否属于训练集。在本文中，我们在对参数分布做少量假设的情况下，推导出成员推断的最优策略。我们表明最优攻击只依赖损失函数，因此黑盒攻击与白盒攻击同样有效。由于最优策略不可计算，我们提供其近似，得到若干推断方法，并表明现有成员推断方法都是这一最优策略的更粗糙近似。我们的成员攻击在多种设置下胜过最先进水平，从简单的逻辑回归到更复杂的架构与数据集，如 ResNet-101 与 ImageNet。

## ICML 2019 的其他活动

**研讨会：面向机器人与 AI 的生成建模与基于模型的推理**
组织者：Aravind Rajeswaran、Emanuel Todorov、Igor Mordatch、William Agnew、Amy Zhang、Joelle Pineau、Michael Chang、Dumitru Erhan、Sergey Levine、Kimberly Stachenfeld、Marvin Zhang
讲者：David Silver、Chelsea Finn、Byron Boots、Jessica Hamrick、Rob Fergus、Abhinav Gupta、Yann LeCun

**研讨会：识别与理解深度学习现象**
组织者：Ari Morcos、Samy Bengio、Behnam Neyshabur、Ludwig Schmidt、Maithra Raghu、Hanie Sedghi、Kenji Hata、Ying Xiao、Ali Rahimi

**研讨会：多任务与终身强化学习**
组织者：Sarath Chandar、Chelsea Finn、Abhishek Gupta、Khimya Khetarpal、Andrei Rusu、Shagun Sodhani、Amy Zhang

**研讨会：面向现实生活的强化学习**
组织者：Alborz Geramifard、Lihong Li、Yuxi Li、Csaba Szepesvari、Tao Wang、Pieter Abbeel、Craig Boutilier、Emma Brunkskill、John Langford、David Silver、David Sontag
顾问：Kyunghyun Cho、Rob Fergus、Shie Mannor、Daniel J. Mankowitz、Doina Precup、Balaraman Ravindran、Tom Zahavy

**研讨会：自监督学习**
讲者：Yann LeCun、Chelsea Finn、Andrew Zisserman、Alexei Efros、Jacob Devlin、Abhinav Gupta
