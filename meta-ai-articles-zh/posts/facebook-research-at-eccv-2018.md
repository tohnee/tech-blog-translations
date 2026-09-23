---
title: "Facebook 研究团队在 ECCV 2018"
title_en: "Facebook Research at ECCV 2018"
date: 2018-09-08
source: https://ai.facebook.com/blog/facebook-research-at-eccv-2018
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 研究团队在 ECCV 2018

> 原文：[Facebook Research at ECCV 2018](https://ai.facebook.com/blog/facebook-research-at-eccv-2018) · Meta AI（Wayback 存档）

2018 年 9 月 8 日

本周末，计算机视觉专家齐聚德国慕尼黑参加欧洲计算机视觉会议（ECCV），展示该领域的最新进展。Facebook 的研究将在口头报告和海报环节展示。Facebook 的研究员和工程师还将在整个会议期间组织和参与多个研讨会。

## Facebook 在 ECCV 2018 上展示的研究

**选择你的神经元：通过神经元重要性融入领域知识（Choose Your Neuron: Incorporating Domain Knowledge through Neuron Importance）**
Ramprasaath R. Selvaraju、Prithvijit Chattopadhyay、Mohamed Elhoseiny、Tilak Sharma、Dhruv Batra、Devi Parikh、Stefan Lee
已有研究表明，为图像级分类任务监督训练的卷积神经网络中的单个神经元会隐式学习语义上有意义的概念——从简单纹理与形状到完整或部分物体——形成学习过程中习得的概念「词典」。在本工作中，我们基于这一观察引入一种简单高效的零样本学习方法。该方法称为神经元重要性感知权重迁移（NIWT），学习把关于新「未见」类别的领域知识映射到这个已学概念词典上，然后优化能有效组合这些概念的网络参数——本质上是通过发现并组合深度网络中已学的语义概念来学习分类器。我们的方法在 CUBirds 和 AWA2 广义零样本学习基准上优于以往方法。我们在多种语义输入（包括属性与自然语言描述）作为外部领域知识上演示了方法。此外，通过学习逆映射，NIWT 可以为新学分类器的预测提供视觉与文本解释，并给出神经元命名。代码见 https://github.com/ramprs/neuron-importance-zsl。

**超越精度的 ConvNets 与 ImageNet：理解错误并揭示偏差（ConvNets and ImageNet Beyond Accuracy: Understanding Mistakes and Uncovering Biases）**
Pierre Stock、Moustapha Cisse
ConvNets 与 ImageNet 推动了深度学习在图像分类上的近期成功。然而，性能提升明显放缓、神经网络对对抗样本缺乏鲁棒性以及表现出不良偏差的倾向，都让人质疑这些方法的可靠性。本工作从终端用户视角出发，利用人类被试研究与解释来考察这些问题。本研究的贡献有三：首先，我们实验证明在 ImageNet 上测得的 ConvNets 精度与鲁棒性被大大低估；其次，我们表明解释可以从终端用户视角减轻被误分类对抗样本的影响；最后，我们引入一个揭示模型所学不良偏差的新工具。这些贡献还表明，解释既是改进我们理解 ConvNets 预测的宝贵工具，也有助于设计更可靠的模型。

**DDRNet：用级联 CNN 为消费级深度相机做深度图去噪与精化（DDRNet: Depth Map Denoising and Refinement for Consumer Depth Cameras Using Cascaded CNNs）**
Shi Yan、Chenglei Wu、Lizhen Wang、Feng Xu、Liang An、Kaiwen Guo、Yebin Liu
消费级深度传感器越来越普及，随着近期集成到最新的 iPhone X 而进入日常生活。然而它们仍受严重噪声困扰，极大限制了应用。尽管在降噪与增强几何细节方面已有大量进展，但由于问题固有的病态性与实时性要求，它仍远未解决。我们提出级联的深度去噪与精化网络（DDRNet），通过联合训练策略利用多帧融合几何与随附的高质量彩色图像来解决这一问题。经典渲染方程在我们的网络中以无监督方式被精妙利用。实验结果表明，我们的网络在多种静态与动态场景类别上实现了实时去噪与精化。得益于级联网络中低频与高频信息的良好解耦，我们的性能优于最先进技术。

**深度聚类：视觉特征的无监督学习（Deep Clustering for Unsupervised Learning of Visual Features）**
Mathilde Caron、Piotr Bojanowski、Armand Joulin、Matthijs Douze
聚类是一类在计算机视觉中被广泛应用与研究的无监督学习方法。但把它适配到大规模数据集上视觉特征的端到端训练的工作很少。在本工作中，我们提出 DeepCluster——一种联合学习神经网络参数与所得特征聚类分配的聚类方法。DeepCluster 迭代地用标准聚类算法 k-means 对特征分组，并把后续分配作为监督来更新网络权重。我们把 DeepCluster 应用于 ImageNet 与 YFCC100M 等大型数据集上卷积神经网络的无监督训练。所得模型在所有标准基准上大幅超越当前最先进水平。

**DeepWrinkles：精确逼真的衣物建模（DeepWrinkles: Accurate and Realistic Clothing Modeling）**
Zorah Lahner、Daniel Cremers、Tony Tung
我们提出一种从真实数据采集生成精确逼真衣物变形的新方法。以往逼真布料建模方法主要依赖基于物理的仿真密集计算（含大量启发式参数），而从视觉观测重建的模型通常缺乏几何细节。在此，我们提出一个由两个模块组成的原创框架，协同工作以高保真表示全局形状变形与表面细节。全局形状变形从身着衣物运动人群的 3D 数据学到的子空间模型恢复，高频细节则添加到用条件生成对抗网络创建的法线图上，其架构设计强调真实感与时间一致性。这带来了空前的衣物变形序列高质量渲染，可以恢复（真实）高分辨率观测中的细微褶皱。此外，由于模型独立于体型与姿态学习，该框架适合需要重定向的应用（如身体动画）。我们的实验以灵活的模型展示了原创的高质量结果。我们主张完全数据驱动的逼真布料褶皱生成是可行的。

**探索监督预训练的极限（Exploring the Limits of Supervised Pretraining）**
Dhruv Mahajan、Ross Girshick、Vignesh Ramanathan、Kaiming He、Manohar Paluri、Yixuan Li、Ashwin Bharambe、Laurens van der Maaten
各类任务的最先进视觉感知模型都依赖监督预训练。ImageNet 分类是这些模型事实上的预训练任务。然而 ImageNet 已近十年之龄，按现代标准算是「小」的。即便如此，对大若干数量级的数据集上的预训练行为，人们所知相对有限。原因很明显：这类数据集难以收集与标注。在本文中，我们提出一项独特研究：用训练于数十亿社交媒体图像上的大型卷积网络预测话题标签的迁移学习。我们的实验表明，大规模话题标签预测训练带来了出色的结果。我们在多个图像分类与目标检测任务上展示了改进，并报告了迄今最高的 ImageNet-1k 单裁剪 top-1 精度：85.4%（top-5 为 97.6%）。我们还进行了大量实验，为大规模预训练与迁移学习性能之间的关系提供了新颖的实证数据。

**面向视频识别的多纤维网络（Multi-fiber Networks for Video Recognition）**
Yunpeng Chen、Yannis Kalantidis、Jianshu Li、Shuicheng Yan、Jiashi Feng
在本文中，我们旨在降低时空深度神经网络的计算成本，使其运行得像 2D 对应网络一样快，同时保持在视频识别基准上的最先进精度。为此，我们提出新颖的多纤维（Multi-Fiber）架构，把复杂神经网络切分为贯穿网络的一组轻量网络或「纤维」。为促进纤维间的信息流动，我们进一步引入多路复用器模块，最终使 3D 网络的计算成本降低一个数量级，同时提升识别性能。大量实验结果表明，我们的多纤维架构显著提升了现有卷积网络在图像与视频识别任务上的效率，在 UCF-101、HMDB-51 和 Kinetics 数据集上取得最先进性能。我们提出的模型所需计算量分别比 I3D [1] 与 R(2+1)D [2] 少 9 倍以上和 13 倍以上，精度反而更高。

**用于场景图生成的 Graph R-CNN（Graph RCNN for Scene Graph Generation）**
Jianwei Yang、Jiasen Lu、Stefan Lee、Dhruv Batra、Devi Parikh
我们提出一个名为 Graph R-CNN 的新颖场景图生成模型，能高效且有效地检测图像中的物体及其关系。我们的模型包含一个关系建议网络（RePN），能高效处理图像中物体间潜在关系的二次方量级问题。我们还提出注意力图卷积网络（aGCN），有效捕捉物体与关系之间的上下文信息。最后，我们引入一个比现有指标更整体、更真实的新评估指标。我们报告了使用现有指标与我们所提指标评估的场景图生成最先进性能。

**组归一化（Group Normalization）**
Yuxin Wu、Kaiming He
批归一化（BN）是深度学习发展中的里程碑技术，使各种网络得以训练。然而，沿批次维度归一化带来了问题——当批次尺寸变小时，BN 的误差迅速增大，原因在于批次统计量估计不准确。这限制了 BN 在训练更大模型以及把特征迁移到检测、分割和视频等计算机视觉任务上的使用——这些任务受内存消耗限制需要小批次。在本文中，我们提出组归一化（GN）作为 BN 的简单替代。GN 把通道分组，并在每组内计算用于归一化的均值与方差。GN 的计算与批次尺寸无关，其精度在很宽的批次尺寸范围内保持稳定。在 ImageNet 训练的 ResNet-50 上，批次尺寸为 2 时 GN 的误差比 BN 低 10.6%；在典型批次尺寸下，GN 与 BN 相当且优于其他归一化变体。此外，GN 可以自然地从预训练迁移到微调。在 COCO 的目标检测与分割以及 Kinetics 的视频分类上，GN 可以胜过基于 BN 的对应版本，表明 GN 能在多种任务中有效替代强大的 BN。GN 用几行代码即可轻松实现。

**NAM：非对抗无监督域映射（NAM: Non-Adversarial Unsupervised Domain Mapping）**
Yedid Hoshen、Lior Wolf
近来有若干方法被提出用于在没有任何对应关系先验的情况下在域之间翻译图像。现有方法应用对抗学习以确保映射后的源域分布与目标域不可区分，但这存在已知的稳定性问题。此外，大多数方法严重依赖域之间的「循环」关系，强制一一映射。在本工作中，我们引入替代方法：非对抗映射（NAM），把目标域生成建模任务与跨域映射任务分离。NAM 依赖预训练的目标域生成模型，把每张源图像与一张从目标域合成的图像对齐，同时联合优化域映射函数。它有几个关键优势：更高质量与分辨率的图像翻译、更简单稳定的训练、可复用的目标模型。大量实验验证了我们方法的优势。

**记忆感知突触：学习什么（不）该遗忘（Memory Aware Synapses: Learning what (not) to forget）**
Rahaf Aljundi、Francesca Babiloni、Mohamed Elhoseiny、Marcus Rohrbach、Tinne Tuytelaars
人类可以持续学习。旧的、很少使用的知识可以被新来的信息覆盖，而重要的、经常使用的知识则免于被抹除。在人工学习系统中，终身学习迄今主要聚焦于跨任务积累知识并克服灾难性遗忘。在本文中，我们论证：鉴于模型容量有限而要学习的新信息无限，知识必须被有选择地保留或抹除。受神经可塑性启发，我们提出一种终身学习的新方法，称为记忆感知突触（MAS）。它以无监督、在线的方式计算神经网络参数的重要性。给定一个输入网络的新样本，MAS 基于预测输出函数对该参数变化的敏感程度，为网络的每个参数累积重要性度量。学习新任务时，对重要参数的改变可以被惩罚，从而有效防止与之前任务相关的重要知识被覆盖。此外，我们展示了方法的局部版本与赫布规则（Hebb's rule，大脑学习过程的一种模型）之间的有趣联系。我们在一系列物体识别任务以及学习预测<主语，谓语，宾语>三元组嵌入这一富有挑战的问题上测试了方法。我们展示了最先进的性能，并首次展示了基于无标签数据调整参数重要性、使网络忘记（或记住）它所需内容的能力——这会随测试条件而变化。

**视频中的物体级视觉推理（Object Level Visual Reasoning in Videos）**
Fabien Baradel、Natalia Neverova、Christian Wolf、Julien Mille、Greg Mori
人类活动识别通常通过训练模型检测关键概念来解决，如全局与局部运动、场景中物体类别相关的特征，以及全局上下文相关的特征。活动识别的下一个开放挑战需要的理解水平要超越这些——需要对场景中演员与物体之间交互的精细区分和详细理解。我们提出一个能够学习推理视频中有语义意义时空交互的模型。方法的关键在于选择在物体层面执行这一推理，通过集成最先进的物体实例分割网络。这使模型能学习语义上与物体交互相关的详细空间交互。我们在三个标准数据集上评估了方法：TwentyBN Something-Something、VLOG 和 EPIC Kitchens，并在其上取得最先进结果。最后，我们还展示了模型学到的交互可视化，呈现了物体类别及对应不同活动类别的交互。

**通过预测卷积特征来预测未来实例分割（Predicting Future Instance Segmentation by Forecasting Convolutional Features）**
Pauline Luc、Camille Couprie、Yann LeCun、Jakob Verbeek
预判未来事件是智能行为的重要前提。视频预测已被作为通向这一目标的代理任务来研究。近期工作表明，要预测未来帧的语义分割，在语义层预测比先预测 RGB 帧再分割更有效。在本文中，我们考虑更困难的未来实例分割问题——它还要把单个物体分割出来。为处理每张图像输出标签数量不定的问题，我们在 Mask R-CNN 实例分割模型的定长卷积特征空间中开发了一个预测模型。我们把 Mask R-CNN 的「检测头」应用于预测特征，产生未来帧的实例分割。实验表明，该方法显著优于基于光流与改造的实例分割架构的强基线。

**Recycle-GAN：无监督视频重定向（Recycle-GAN: Unsupervised Video Retargeting）**
Aayush Bansal、Shugao Ma、Deva Ramanan、Yaser Sheikh
我们引入一种数据驱动的无监督视频重定向方法，把内容从一个域翻译到另一个域，同时保留该域原生的风格。也就是说，如果把约翰·奥利弗演讲的内容转移给斯蒂芬·科尔伯特，生成的内容/演讲应当是科尔伯特的风格。我们的方法结合空间与时间信息以及用于内容翻译与风格保持的对抗损失。在本工作中，我们首先研究使用时空约束相对纯空间约束对有效重定向的优势；然后针对空间与时间信息均重要的问题演示所提方法，如人脸到人脸翻译、花到花、风与云合成、日出与日落。

**稠密姿态迁移（Dense Pose Transfer）**
Natalia Neverova、Rıza Alp Guler、Iasonas Kokkinos
在本工作中，我们把基于表面的建模思想与神经合成相结合：提出基于表面的姿态估计与深度生成模型的组合，使我们能执行精确的姿态迁移——即基于某人的单张图像与一位姿态供体的图像，合成该人的新图像。我们使用稠密姿态估计系统把两张图像的像素映射到共同的基于表面的坐标系，使两图相互对应。我们在表面坐标系中对源图像强度做补绘与精化，再把它变形到目标姿态。这些预测与一个卷积预测模块的输出通过神经合成模块融合，使整条流水线可以联合端到端训练，优化对抗损失与感知损失的组合。我们表明稠密姿态估计是比关键点或掩码替代方案强大得多的条件输入，并在 DeepFashion 与 MVC 数据集上报告了对最先进生成器的系统性改进。

**面向神经网络训练与推断的数值感知量化（Value-aware Quantization for Training and Inference of Neural Networks）**
Eunhyeok Park、Sungjoo Yoo、Peter Vajda
我们提出一种新颖的数值感知量化：对大多数数据施加激进降低的精度，同时以高精度单独处理少量大数值，从而在极低精度下降低总量化误差。我们给出了把所提量化应用于训练与推断的新技术。实验表明，使用 3 比特激活（其中 2% 为大数值）的方法可达到与全精度相同的训练精度，同时相较最先进方法，在 ResNet-152 和 Inception-v3 上分别显著减少激活内存成本 41.6% 与 53.7%。实验还表明，Inception-v3、ResNet-101 和 DenseNet-121 等深度网络可以用 4 比特权重与激活（含 1% 的 16 比特数据）量化推理，top-1 精度损失在 1% 以内。

**用神经模块网络做视觉对话中的视觉指代消解（Visual Coreference Resolution in Visual Dialog using Neural Module Networks）**
Satwik Kottur、Jose M. F. Moura、Devi Parikh、Dhruv Batra、Marcus Rohrbach
视觉对话 [11, 41] 需要以对话历史为上下文，回答一系列基于某图像的问题。除了视觉问答（VQA）[6]（可视为单轮对话）中的挑战外，视觉对话还包含更多难题。我们聚焦其中一个称为视觉指代消解的问题：确定哪些词（通常是名词短语与代词）共指图像中的同一实体/物体实例。这一点至关重要，尤其对代词（「它」）而言：对话智能体必须先把「它」链接到先前的指称（「船」），然后才能依赖指称「船」的视觉落地来推理代词「它」。以往工作对视觉指代消解的建模要么（a）通过对历史记录的记忆网络隐式进行，要么（b）对整个问题在粗粒度进行，而非显式地在短语级粒度进行。在本工作中，我们为视觉对话提出神经模块网络架构，引入两个新颖模块——Refer 与 Exclude——在更细的词级别执行显式的、落地的指代消解。我们在 MNIST Dialog [38]（视觉简单但指代复杂的数据集）上以接近完美的精度、在 VisDial [11]（大型真实图像的富有挑战视觉对话数据集）上以有竞争力的表现证明了模型的有效性，且模型在定性上更可解释、更落地、更一致。代码已公开。

## ECCV 2018 的其他活动

- 第二届 YouTube-8M 大规模视频理解研讨会——Manohar Paluri，讲者
- 第 11 届计算机视觉感知组织（POCV）研讨会：动作、感知与组织——Jitendra Malik、Abhinav Gupta、Iasonas Kokkinos，讲者
- 360° 感知与交互研讨会——Shannon Chen，讲者
- 预判人类行为研讨会——Abhinav Gupta，讲者；论文《Joint Future Semantic and Instance Segmentation Prediction》——Camille Couprie、Pauline Luc、Jakob Verbeek；论文《Predicting Future Instance Segmentation by Forecasting Convolutional Features》——Pauline Luc、Camille Couprie、Yann LeCun、Jakob Verbeek
- 首届无约束环境自主导航国际研讨会——Jitendra Malik，讲者
- 首届面向时尚、艺术与设计的计算机视觉研讨会——论文《DesIGN: Design Inspiration from Generative Networks》——Othman Sbai、Mohamed Elhoseiny、Antoine Bordes、Yann LeCun、Camille Couprie
- 几何遇上深度学习研讨会——Iasonas Kokkinos，讲者
- PoseTrack 挑战赛：野外铰接人体跟踪（研讨会）——Iasonas Kokkinos，讲者
- 第三届自我中心感知、交互与计算国际研讨会——Abhinav Gupta，讲者
- 第三届视频分割国际研讨会——Iasonas Kokkinos，组织者
- 视觉识别及更多（教程）——Georgia Gkioxari、Ross Girshick、Kaiming He、Piotr Dollar、Christoph Feichtenhofer、Natalia Neverova，讲者
- 仿真环境中的视觉学习与具身智能体研讨会——Jitendra Malik、Dhruv Batra、Abhinav Gupta，讲者；Manolis Savva，组织者
- VizWiz 大挑战：回答盲人的视觉问题——Devi Parikh，讲者
- 光流有什么用？研讨会——Jitendra Malik、Richard Szeliski，讲者；Laura Sevilla-Lara，组织者
- 计算机视觉中的女性（WiCV）研讨会——Ilke Demir，委员会；Camille Couprie，导师
- 视觉与语言的短板研讨会——Dhruv Batra，组织者
