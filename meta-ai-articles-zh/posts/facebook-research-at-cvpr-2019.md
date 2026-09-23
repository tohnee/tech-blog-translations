---
title: "Facebook 研究团队在 CVPR 2019"
title_en: "Facebook Research at CVPR 2019"
date: 2019-03-15
source: https://ai.facebook.com/blog/facebook-research-at-cvpr-2019
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 研究团队在 CVPR 2019

> 原文：[Facebook Research at CVPR 2019](https://ai.facebook.com/blog/facebook-research-at-cvpr-2019) · Meta AI（Wayback 存档）

本周，来自世界各地的计算机视觉专家齐聚加利福尼亚州长滩，参加 2019 年计算机视觉与模式识别会议（CVPR）。Facebook AI 的研究将在口头 spotlight 和集体海报环节展示。我们的研究员和工程师还将在整个会议期间举办教程并参与研讨会，包括由研究科学家 Cristian Canton 与首席 AI 科学家 Yann LeCun 共同组织的 DeepVision 研讨会。我们还共同组织了首届「面向全球挑战的计算机视觉」（CV4GC）研讨会，探索计算机视觉用于解决疾病预防、基础设施测绘等全球问题的新途径。Facebook AI 以 Facebook AI 视频峰会拉开 CVPR 序幕，峰会由 Jitendra Malik、Matt Feizsli、Georgia Gkioxari、Manohar Paluri、Lorenzo Torresani 和 Christoph Feichtenhofer 组织，是为一批精选研究者举办的为期两天的场边活动，就视频理解前沿的新兴技术进行深入讨论，工业界与学术界的多位计算机视觉领军人物发表了演讲。对于参加 CVPR 的人，欢迎光临 Facebook Research 展位，了解我们在做的工作、聊聊职业机会或体验我们的演示。Facebook 在 CVPR 的论文、研讨会和教程完整日程请见此处。

## Facebook 在 CVPR 上展示的研究

**2.5D 视觉声音（2.5D Visual Sound）**
Ruohan Gao、Kristen Grauman
双耳音频为听众提供 3D 声音感受，带来丰富的场景感知体验。然而双耳录音十分稀少，获取它需要非同寻常的专长和设备。我们提出利用视频把普通的单声道音频转换为双耳音频。核心想法是：视觉帧揭示了显著的空间线索，这些线索在随附的单通道音频中明确缺失，却与之紧密关联。我们的多模态方法从无标注视频中恢复这一关联。我们设计了一个深度卷积神经网络，通过注入关于物体与场景配置的视觉信息，学习把单声道音轨解码为双声道对应物。我们把输出称为 2.5D 视觉声音——视觉流帮助把扁平的单通道音频「抬升」为空间化声音。除声音生成外，我们还表明网络学到的自监督表示有利于视听源分离。视频结果：http://vision.cs.utexas.edu/projects/2.5D_visual_sound/

**用时间卷积与半监督训练做视频 3D 人体姿态估计（3D Human Pose Estimation in Video with Temporal Convolutions and Semisupervised Training）**
Dario Pavllo、Christoph Feichtenhofer、David Grangier、Michael Auli
在本工作中，我们证明视频中的 3D 姿态可以用一个基于 2D 关键点上膨胀时间卷积的全卷积模型有效估计。我们还引入了反向投影（back-projection）——一种简单有效的半监督训练方法，可利用无标注视频数据。我们先为无标注视频预测 2D 关键点，然后估计 3D 姿态，最后反投影回输入的 2D 关键点。在有监督设置下，我们的全卷积模型在 Human3.6M 上以 6 毫米的平均每关节位置误差超越此前文献最佳结果（相当于误差降低 11%），在 HumanEva-I 上也有显著改进。此外，反向投影实验表明，在有标注数据稀缺的半监督设置中，它轻松超越了以往最先进结果。代码与模型见 https://github.com/facebookresearch/VideoPose3D。

**活动驱动的弱监督目标检测（Activity Driven Weakly Supervised Object Detection）**
Zhenheng Yang、Dhruv Mahajan、Deepti Ghadiyaram、Ram Nevatia、Vignesh Ramanathan
弱监督目标检测旨在减少训练检测模型所需的监督量。这类模型传统上从只标注了物体类别（而非物体边界框）的图像/视频中学习。在我们的工作中，我们试图不仅利用物体类别标签，还利用与数据相关的动作标签。我们表明，图像/视频所描绘的动作能为相关物体的位置提供强线索。我们学习依赖动作的物体空间先验（例如在「踢球」中，「球」更靠近「人的腿」），并把该先验纳入联合物体检测与动作分类模型的同步训练。我们在视频数据集和图像数据集上都做了实验来评估弱监督检测模型的性能。我们的方法在 Charades 视频数据集上以超过 6% 的 mAP 胜过当前最先进（SOTA）方法。

**多句视频描述的对抗推断（Adversarial Inference for Multi-Sentence Video Description）**
Jae Sung Park、Marcus Rohrbach、Trevor Darrell、Anna Rohrbach
尽管图像描述任务已取得显著进展，但由于视频数据的复杂性，视频描述仍处于起步阶段。为长视频生成多句描述更具挑战性。主要问题包括生成描述的流畅性与连贯性，及其与视频的相关性。近来，基于强化学习与对抗学习的方法被用于改进图像描述模型；但两类方法都存在若干问题，如 RL 方法的可读性差、冗余度高，GAN 的稳定性问题。在本工作中，我们转而提议在推断阶段应用对抗技术，设计一个鼓励更好多句视频描述的判别器。此外，我们发现多判别器「混合」设计——每个判别器针对描述的一个方面——效果最佳。具体而言，我们把判别器解耦为三个评估标准：（1）与视频的视觉相关性；（2）语言多样性与流畅度；（3）跨句子连贯性。如流行的 ActivityNet Captions 数据集上的自动与人工评估所示，我们的方法产出了更准确、多样且连贯的多句视频描述。

**多任务的专注单任务化（Attentive Single-Tasking of Multiple Tasks）**
Kevis-Kokitsi Maninis、Ilija Radosavovic、Iasonas Kokkinos
在本工作中，我们通过让网络在多个任务上训练、但一次只执行一个任务来解决通用网络中的任务干扰问题，我们称之为「多任务的单任务化」。网络通过任务依赖的特征自适应（即任务注意力）来修改自身行为。这使网络能够突出适配当前任务的特征，同时回避无关特征。我们进一步通过对抗训练迫使各任务梯度在统计上不可区分，确保服务所有任务的公共主干架构不被任何任务特定梯度主导，从而降低任务干扰。在三个多任务稠密标注问题上的结果一致表明：（1）参数量大幅减少的同时保持甚至提升性能；（2）计算与多任务精度之间的平滑权衡。系统代码与预训练模型见 https://github.com/facebookresearch/astmt。

**ChamNet：通过平台感知模型自适应实现高效网络设计（ChamNet: Towards Efficient Network Design Through Platform-Aware Model Adaptation）**
Xiaoliang Dai、Peizhao Zhang、Bichen Wu、Hongxu Yin、Fei Sun、Yanghan Wang、Marat Dukhan、Yunqing Hu、Yiming Wu、Yangqing Jia、Peter Vajda、Matt Uyttendaele、Niraj K. Jha
本文提出一种名为 Chameleon（ChamNet）的高效神经网络（NN）架构设计方法，它尊重给定的资源约束。我们不开发新构建块，也不使用计算密集的强化学习算法，而是利用现有高效网络构建块，专注于挖掘硬件特性并调整计算资源以适配目标时延和/或能耗约束。我们把平台感知的 NN 架构搜索表述为一个优化框架，并提出一种新算法，借助高效的精度与资源（时延和/或能耗）预测器搜索最优架构。算法的核心是建立在高斯过程之上、采用贝叶斯优化进行迭代采样的精度预测器。预测器只需一次性构建成本，我们的算法就能在几分钟内在不同平台上、给定约束下产出最先进的模型架构。结果表明，把计算资源适配到构建块对模型性能很重要。在未添加任何特殊功能的情况下，我们的模型相较最先进的手工设计与自动设计架构取得显著精度提升。在移动 CPU 和 DSP 上 20ms 时延下，我们在 ImageNet 上分别达到 73.8% 与 75.3% 的 top-1 精度。在更低时延下，我们的模型在移动 CPU（DSP）上相较 MobileNetV2 和 MnasNet 分别取得最高 8.2%（4.8%）和 6.7%（9.3%）的绝对 top-1 精度提升，并在 Nvidia GPU（Intel CPU）上分别比 ResNet-101 和 ResNet-152 高出 2.7%（4.6%）和 5.6%（2.6%）。

**面向鲁棒视觉问答的循环一致性（Cycle-Consistency for Robust Visual Question Answering）**
Meet Shah、Xinlei Chen、Marcus Rohrbach、Devi Parikh
尽管视觉问答（VQA）多年来进展显著，但当今 VQA 模型的鲁棒性仍大有可改进之处。我们引入新的评估协议与配套数据集（VQA-Rephrasings），并表明最先进的 VQA 模型对问题中的语言变化出了名地脆弱。VQA-Rephrasings 为 VQA v2.0 验证集中 4 万张图像的 4 万个问题提供了三个人工改写。作为提升 VQA 模型鲁棒性的一步，我们提出一个利用循环一致性的模型无关框架。具体而言，我们训练模型不仅回答问题，还基于答案生成一个问题，使得为生成问题预测的答案与原问题的真值答案相同。在不使用额外标注的情况下，我们表明在 VQA-Rephrasings 数据集上评估时，我们的方法比最先进的 VQA 模型对语言变化显著更鲁棒。此外，在富有挑战的 VQA v2.0 数据集上，我们的方法在标准 VQA 和视觉问题生成任务上都胜过最先进方法。

**DeepSDF：学习连续符号距离函数用于形状表示（DeepSDF: Learning Continuous Signed Distance Functions for Shape Representation）**
Jeong Joon Park、Peter Florence、Julian Straub、Richard Newcombe、Steven Lovegrove
计算机图形学、3D 计算机视觉和机器人社区已经产出了多种用于渲染与重建的 3D 几何表示方法，它们在保真度、效率和压缩能力上各有取舍。在本工作中，我们引入 DeepSDF——一类形状的学习型连续符号距离函数（SDF）表示，能够从部分且有噪声的 3D 输入数据实现高质量形状表示、插值和补全。与其经典对应物一样，DeepSDF 用连续的体积场表示形状表面：场中一点的幅值表示到表面边界的距离，符号表示该区域位于形状内部（-）还是外部（+）。因此我们的表示把形状边界隐式编码为所学函数的零水平集，同时显式表示空间是否属于形状内部的分类。经典 SDF 无论是解析形式还是离散体素形式通常表示单个形状的表面，而 DeepSDF 可以表示一整类形状。此外，我们在学习型 3D 形状表示与补全上展示了最先进的性能，同时模型尺寸比此前工作小一个数量级。

**用网络规模最近邻搜索防御对抗图像（Defense Against Adversarial Images Using Web-Scale Nearest-Neighbor Search）**
Abhimanyu Dubey、Laurens van der Maaten、Zeki Yalniz、Yixuan Li、Dhruv Mahajan
大量近期工作表明，卷积网络对对抗图像不鲁棒——这类图像通过扰动数据分布中的样本以最大化扰动样本上的损失来构造。在本工作中，我们假设对抗扰动使图像偏离了图像流形——即不存在能产生该对抗图像的物理过程。这一假设暗示，成功的对抗图像防御机制应致力于把图像投影回图像流形。我们研究了此类防御机制：用包含数百亿张图像的网络规模图像数据库的最近邻搜索来近似到未知图像流形的投影。该防御策略在 ImageNet 上的实证评估表明，在攻击者无法访问图像数据库的攻击设置中非常有效。我们还提出两种打破最近邻防御的新攻击方法，并展示了最近邻防御失效的条件。我们进行了一系列消融实验，结果表明：防御中的鲁棒性与准确性存在权衡；庞大的图像数据库（数亿张图像）对良好性能至关重要；精心构建图像数据库对抵御针对防御的定制攻击很重要。

**DMC-Net：为快速压缩视频动作识别生成有判别力的运动线索（DMC-Net: Generating Discriminative Motion Cues for Fast Compressed Video Action Recognition）**
Zheng Shou、Xudong Lin、Yannis Kalantidis、Laura Sevilla-Lara、Marcus Rohrbach、Shih-Fu Chang、Zhicheng Yan
运动对视频理解很有用，通常用光流表示。然而从视频帧计算光流非常耗时。近期工作直接利用压缩视频中现成的运动向量与残差来表示运动，几乎无性能开销。这虽然避免了光流计算，但也损害了精度，因为运动向量含噪且分辨率大幅降低，使其成为判别力较弱的运动表示。为弥补这些问题，我们提出一个轻量生成器网络，能降低运动向量噪声并捕捉细微运动细节，获得更有判别力的运动线索（DMC）表示。由于光流是更准确的运动表示，我们用重建损失和对抗损失训练 DMC 生成器逼近光流，并与下游动作分类任务联合训练。在三个动作识别基准（HMDB-51、UCF-101 和 Kinetics 子集）上的大量评估证实了方法的有效性。由生成器与分类器组成的完整系统称为 DMC-Net，精度接近使用光流的水平，而推断时比使用光流快两个数量级。

**基于点云感知的逼真环境具身问答（Embodied Question Answering in Photorealistic Environments with Point Cloud Perception）**
Erik Wijmans、Samyak Datta、Oleksandr Maksymets、Abhishek Das、Georgia Gkioxari、Stefan Lee、Irfan Essa、Devi Parikh、Dhruv Batra
为弥合互联网视觉式问题与具身感知视觉目标之间的鸿沟，我们实例化了一个大规模导航任务——逼真环境（Matterport3D）中的具身问答 [1]。我们深入研究了利用 3D 点云、RGB 图像或二者组合的导航策略。对这些模型的分析揭示了若干关键发现：我们发现两个看似朴素的导航基线——只前进与随机——是强有力的导航者，由于 [1] 给出的评估设置的特殊性而难以被超越；我们提出一种称为「拐点加权」（Inflection Weighting）的新损失加权方案，对用行为克隆训练循环导航模型很重要，并借此超越了基线；我们发现点云为学习避障提供了比 RGB 图像更丰富的信号，这促使我们在具身导航中使用（并继续研究）3D 深度学习模型。

**通过个性生成引人入胜的图像描述（Engaging Image Captioning via Personality）**
Kurt Shuster、Samuel Humeau、Hexiang Hu、Antoine Bordes、Jason Weston
COCO 和 Flickr30k 等标准图像描述任务是事实性的、语气中立，且（对人类而言）只陈述显而易见的内容（如「一个人在弹吉他」）。这类任务虽有助于验证机器是否理解图像内容，但作为描述对人类并无吸引力。有鉴于此，我们定义了一个新任务 PERSONALITY-CAPTIONS：通过融入可控的风格与个性特征，使描述对人尽可能有吸引力。我们收集并发布了 241858 条此类描述的大规模数据集，条件覆盖 215 种可能特质。我们构建的模型结合了（1）在 17 亿对话样本上训练的 Transformer 句子表示 [36]，与（2）在 35 亿社交媒体图像上训练 ResNet 的图像表示 [32]。我们在 Flickr30k 和 COCO 上取得最先进性能，并在新任务上表现强劲。最后，在线评估验证了我们的任务和模型对人具有吸引力，最佳模型接近人类水平。

**通过场景补全做 RGB-D 扫描的极端相对位姿估计（Extreme Relative Pose Estimation for RGB-D Scans via Scene Completion）**
Zhenpei Yang、Jeffrey Z. Pan、Linjie Luo、Xiaowei Zhou、Kristen Grauman、Qixing Huang
估计同一环境的两次 RGB-D 扫描之间的相对刚体位姿，是计算机视觉、机器人和计算机图形学的基础问题。现有大多数方法只允许有限的相对位姿变化，因为它们要求输入扫描之间有相当大的重叠。我们引入一种把适用范围扩展到极端相对位姿的新方法——输入扫描之间重叠很少甚至没有。关键思想是推断关于底层环境更完整的场景信息，并在补全后的扫描上进行匹配。特别地，我们的方法不是只从每个单独扫描做场景补全，而是在相对位姿估计与场景补全之间交替进行。这使我们能在后期迭代中利用两次输入扫描的信息进行场景补全，使场景补全与相对位姿估计都获得更好结果。基准数据集上的实验结果表明，我们的方法在相对位姿估计上比最先进方法有相当大的改进。特别是，即使对不重叠的扫描，我们的方法也能给出令人鼓舞的相对位姿估计。

**FBNet：通过可微神经架构搜索做硬件感知的高效卷积网络设计（FBNet: Hardware-Aware Efficient ConvNet Design via Differentiable Neural Architecture Search）**
Bichen Wu、Xiaoliang Dai、Peizhao Zhang、Yanghan Wang、Fei Sun、Yiming Wu、Yuandong Tian、Peter Vajda、Yangqing Jia、Kurt Keutzer
为移动设备设计精确高效的卷积网络颇具挑战，因为设计空间组合爆炸。因此，以往的神经架构搜索（NAS）方法计算开销高昂。卷积网络架构的最优性取决于输入分辨率、目标设备等因素，而现有方法对逐案重新设计而言资源消耗过大。此外，以往工作主要聚焦降低 FLOPs，但 FLOP 数并不总能反映实际时延。针对这些问题，我们提出可微神经架构搜索（DNAS）框架，用基于梯度的方法优化卷积网络架构，避免像以往方法那样分别枚举并训练各个架构。由 DNAS 发现的 FBNet（Facebook-Berkeley-Nets）模型家族胜过手工设计与自动生成的最先进模型。FBNet-B 在 ImageNet 上以 295M FLOPs、三星 S8 手机 23.1ms 时延达到 74.1% top-1 精度，比精度相近的 MobileNetV2-1.3 [17] 小 2.4 倍、快 1.5 倍。尽管精度更高、时延更低，我们估计 FBNet-B 的搜索成本比 MnasNet [20] 小 420 倍，仅 216 GPU 时。针对不同分辨率和通道尺寸搜索的 FBNet 比 MobileNetV2 精度高 1.5% 至 6.4%。最小的 FBNet 在三星 S8 上达到 50.2% 精度、2.9ms 时延（每秒 345 帧）。相较针对三星优化的 FBNet，针对 iPhone X 优化的模型在 iPhone X 上提速 1.4 倍。FBNet 模型已开源：https://github.com/facebookresearch/mobile-vision。

**改进对抗鲁棒性的特征去噪（Feature Denoising for Improving Adversarial Robustness）**
Cihang Xie、Yuxin Wu、Laurens van der Maaten、Alan Yuille、Kaiming He
针对图像分类系统的对抗攻击既给卷积网络带来挑战，也为理解它们提供了机会。本研究表明，图像上的对抗扰动会导致这些网络构建的特征中出现噪声。受此观察启发，我们开发了通过执行特征去噪来提升对抗鲁棒性的新网络架构。具体而言，我们的网络包含用非局部均值或其他滤波器为特征去噪的块；整个网络端到端训练。与对抗训练相结合时，我们的特征去噪网络在白盒和黑盒攻击设置下都大幅提升了对抗鲁棒性的最先进水平。在 ImageNet 上，在以往技术为 27.9% 精度的 10 次迭代 PGD 白盒攻击下，我们的方法达到 55.7%；即便在极端的 2000 次迭代 PGD 白盒攻击下，我们的方法仍保持 42.6% 的精度。我们的方法在 2018 年对抗攻击与防御竞赛（CAAD）中排名第一——在一个保密的、类 ImageNet 测试数据集上对抗 48 个未知攻击者取得 50.6% 的分类精度，超过第二名约 10%。代码见 https://github.com/facebookresearch/ImageNet-Adversarial-Training。

**基于图的全局推理网络（Graph-Based Global Reasoning Networks）**
Yunpeng Chen、Marcus Rohrbach、Zhicheng Yan、Shuicheng Yan、Jiashi Feng、Yannis Kalantidis
对区域间关系进行全局建模与推理，有利于图像和视频上的许多计算机视觉任务。卷积神经网络（CNN）擅长用卷积操作建模局部关系，但在捕捉远距离区域间的全局关系方面通常效率低下，且需要堆叠多个卷积层。在本工作中，我们提出一种全局推理的新方法：把一组特征在坐标空间上全局聚合，然后投影到一个可以高效计算关系推理的交互空间。推理完成后，关系感知特征被分发回原坐标空间用于下游任务。我们进一步给出该方法的一个高效实例化，引入全局推理单元（GloRe 单元）——用加权全局池化与加权广播实现坐标-交互空间映射，用交互空间中小图上的图卷积实现关系推理。所提出的 GloRe 单元轻量、可端到端训练，可轻松插入现有 CNN，适用于广泛任务。大量实验表明，GloRe 单元在图像分类、语义分割和视频动作识别任务上，对 2D 和 3D CNN 的最先进主干架构（包括 ResNet [15,16]、ResNeXt [34]、SE-Net [18]、DPN [9]）都能持续提升性能。

**落地视频描述（Grounded Video Description）**
Luowei Zhou、Yannis Kalantidis、Xinlei Chen、Jason J. Corso、Marcus Rohrbach
由于视频与语言两侧的巨大可变性，视频描述是视觉与语言理解中最具挑战性的问题之一。因此，模型通常会走识别的捷径，生成基于先验但未必落地于视频的貌似合理的句子。在本工作中，我们通过把句子中的每个名词短语标注到视频某一帧中对应的边界框，显式地把句子与视频中的证据关联起来。我们的数据集 ActivityNet-Entities 在富有挑战的 ActivityNet Captions 数据集上增加了 15.8 万个边界框标注，每个框落地一个名词短语。这使我们可以用这些数据训练视频描述模型，更重要的是，可以评估此类模型对其所描述视频的落地（「真实」）程度。为生成落地描述，我们提出一个能利用这些边界框标注的新颖视频描述模型。我们既在自有数据集上证明模型有效性，也展示它如何应用于 Flickr30k Entities 数据集的图像描述。我们在视频描述、视频段落描述和图像描述上取得最先进性能，并证明生成的句子更好地落地于视频。代码：https://github.com/facebookresearch/grounded-video-description；数据集：https://github.com/facebookresearch/activityNet-Entities。

**通过联合学习朝向与分割改进道路连通性（Improved Road Connectivity by Joint Learning of Orientation and Segmentation）**
Anil Batra、Suriya Singh、Guan Pang、Saikat Basu、C.V. Jawahar、Manohar Paluri
从卫星图像提取道路网络常产生破碎路段，导致道路地图无法用于实际应用。由于缺乏连通性监督以及施加拓扑约束的困难，逐像素分类无法预测拓扑正确且连通的道路掩码。在本文中，受人类以特定朝向描绘道路的标注行为启发，我们提出一个称为朝向学习（Orientation Learning）的连通性任务。我们还开发了一个堆叠多分支卷积模块，以有效利用朝向学习与分割任务之间的互信息。这些贡献确保模型预测拓扑正确且连通的道路掩码。我们还提出连通性精化方法进一步增强估计出的道路网络：精化模型先预训练以连接和修复被损坏的真值掩码，再微调以增强预测的道路掩码。我们在两个不同的道路提取数据集 SpaceNet [30] 与 DeepGlobe [11] 上展示方法优势。我们的方法在 SpaceNet 与 DeepGlobe 的道路拓扑指标上分别比最先进技术提升 9% 与 7.5%。

**反向烹饪：从食物图像生成菜谱（Inverse Cooking: Recipe Generation from Food Images）**
Amaia Salvador、Michal Drozdzal、Xavier Giro-i-Nieto、Adriana Romero
人们喜爱食物摄影，因为他们热爱美食。每餐背后都有一个以复杂菜谱讲述的故事，遗憾的是，仅凭一张食物图像，我们无法得知其制作过程。因此，本文引入一个反向烹饪系统，能根据食物图像重建烹饪菜谱。我们的系统用一种新颖架构把食材预测为集合，在不施加任何顺序的前提下建模其依赖关系，然后同时关注图像与推断出的食材来生成烹饪步骤。我们在大规模 Recipe1M 数据集上对整个系统做了详尽评估，结果表明：（1）我们在食材预测上优于以往基线；（2）我们能通过同时利用图像与食材获得高质量菜谱；（3）根据人类判断，我们的系统能产出比检索式方法更吸引人的菜谱。代码与模型公开于 https://github.com/facebookresearch/inversecooking。

**用于联合材质与光照估计的反向路径追踪（Inverse Path Tracing for Joint Material and Lighting Estimation）**
Dejan Azinovic、Tzu-Mao Li、Anton Kaplanyan、Matthias Niessner
现代计算机视觉算法为 3D 几何重建带来了显著进步。然而，光照与材质重建研究较少，现有方法对材质和光照采用非常简化的模型假设。我们引入反向路径追踪（Inverse Path Tracing）——一种通过可逆光传输仿真联合估计室内场景中物体材质属性与光源的新方法。我们假设有一个粗略的几何扫描及对应图像与相机位姿。本工作的关键贡献是同时准确检索光源与基于物理的材质属性（如漫反射率、镜面反射率、粗糙度等），以便在新条件下编辑和重渲染场景。为此，我们引入一种使用可微蒙特卡洛渲染器的新优化方法，计算关于未知光照与材质属性的导数。这使我们可以用定制的随机梯度下降对物理正确的光传输与材质模型进行联合优化。

**用于紧凑球面卷积的核变换网络（Kernel Transformer Networks for Compact Spherical Convolution）**
Yu-Chuan Su、Kristen Grauman
理想情况下，360° 图像应当能继承已在透视投影图像上成功训练的深度卷积神经网络（CNN）。然而，把 CNN 从透视图像迁移到球面图像的现有方法会带来显著计算开销和/或精度退化。我们提出核变换网络（KTN），高效地把卷积核从透视图像迁移到 360° 图像的等距柱状投影。给定一个面向透视图像的源 CNN 作为输入，KTN 输出一个以极角和核为参数的函数。给定一张新的 360° 图像，该函数可以为任意层和核计算卷积，效果如同源 CNN 在对应切平面投影上一样。与所有现有方法不同，KTN 支持模型迁移：同一模型可以应用于具有相同基础架构的不同源 CNN。这使其无需重训 KTN 即可应用于多个识别任务。我们用多个源 CNN 和数据集验证了方法，表明 KTN 改进了球面卷积的技术水平。KTN 成功保持了源 CNN 的精度，同时具备可迁移性、对典型图像分辨率的可扩展性，且在许多情况下内存占用大幅降低。

**面向视频动作识别的大规模弱监督预训练（Large-Scale Weakly Supervised Pretraining for Video Action Recognition）**
Deepti Ghadiyaram、Matt Feiszli、Du Tran、Xueting Yan、Heng Wang、Dhruv Mahajan
当前的全监督视频数据集只包含几十万条视频和不足一千个领域特定标签，这阻碍了先进视频架构的发展。本文深入研究了用海量网络视频为视频模型预训练以完成动作识别任务。我们的主要实证发现是：超大规模（超过 6500 万条视频）的预训练——即便基于带噪的社交媒体视频和话题标签——仍显著改进了三个富有挑战的公开动作识别数据集上的最先进水平。此外，我们考察了弱监督视频动作数据集构建中的三个问题：第一，鉴于动作涉及与物体的交互，应如何构建动宾结构预训练标签空间以最大程度利好迁移学习？第二，基于帧的模型在动作识别上表现相当好；那么预训练出好的图像特征是否就足够，还是预训练时空特征对最优迁移学习更有价值？最后，长视频中动作的定位通常不如短视频好；既然动作标签是在视频级给出的，在给定视频数量或分钟数预算下，应如何选择视频片段以获得最佳性能？

**LBS 自编码器：把关节网格自监督拟合到点云（LBS Autoencoder: Self-Supervised Fitting of Articulated Meshes to Point Clouds）**
Chun-Liang Li、Tomas Simon、Jason Saragih、Barnabás Póczos、Yaser Sheikh
我们提出 LBS-AE——一种把关节网格模型拟合到点云的自监督自编码算法。输入为待配准的点云序列以及一个美术师绑定的网格，即配备了由骨架层级参数化的线性混合蒙皮（LBS）变形空间的模板网格。输出是一个基于 LBS 的自编码器，能从输入点云生成配准网格。为弥合美术师定义几何与采集点云之间的鸿沟，我们的自编码器建模偏离模板几何的姿态相关偏差。训练期间，我们不使用关键点或姿态监督等显式对应关系，而是利用 LBS 变形自举学习过程。为避免因错误点对点对应陷入糟糕的局部极小，我们使用基于部件分割的结构化 Chamfer 距离——部件分割通过自监督同步学习。我们在真实采集的手部数据上展示定性结果，并在 FAUST 身体配准基准上报告定量评估。我们的方法优于其他无监督方法，与使用有监督样本的方法相当。

**少即是多：从视频时长学习高光检测（Less Is More: Learning Highlight Detection from Video Duration）**
Bo Xiong、Yannis Kalantidis、Deepti Ghadiyaram、Kristen Grauman
高光检测有望极大简化视频浏览，但现有方法常受制于昂贵的监督需求——需要人工观看者在训练视频中手动识别高光。我们提出一种可扩展的无监督解决方案，把视频时长用作隐式监督信号。我们的关键洞察是：较短的用户生成视频中的片段比较高视频中的更可能是高光，因为用户在拍摄较短视频时对内容更有选择性。利用这一洞察，我们引入一个新的排序框架，偏好较短视频的片段，同时妥善处理（无标签）训练数据中的固有噪声。我们用它训练了一个高光检测器，使用了 1000 万条带话题标签的 Instagram 视频。在两个富有挑战的公开视频高光检测基准上，我们的方法大幅提升了无监督高光检测的最先进水平。

**面向精细视频理解的长期特征库（Long-Term Feature Banks for Detailed Video Understanding）**
Chao-Yuan Wu、Christoph Feichtenhofer、Haoqi Fan、Kaiming He、Philipp Krähenbühl、Ross Girshick
要理解世界，我们人类需要不断把现在与过去关联起来，把事件放入上下文。在本文中，我们让现有视频模型也能这样做。我们提出长期特征库——从视频全片跨度提取的辅助信息——来增强原本只能观看 2-5 秒短片段的最先进视频模型。实验表明，用长期特征库增强 3D 卷积网络在三个富有挑战的视频数据集（AVA、EPIC-Kitchens、Charades）上取得最先进结果。代码已在线公开。

**LVIS：大词表实例分割数据集（LVIS: A Data Set for Large Vocabulary Instance Segmentation）**
Agrim Gupta、Piotr Dollár、Ross Girshick
目标检测的进步得益于那些把研究社区注意力聚焦到开放挑战上的数据集。这一进程把我们从简单图像带到复杂场景，从边界框带到分割掩码。在本工作中，我们引入 LVIS（读作「el-vis」）：一个面向大词表实例分割的新数据集。我们计划在 16.4 万张图像中，为超过 1000 个入门级物体类别收集 220 万个高质量实例分割掩码。由于自然图像中类别的齐夫分布，LVIS 天然存在只有少量训练样本的长尾类别。鉴于最先进的目标检测深度学习方法在少样本情形下表现不佳，我们相信该数据集提出了一个重要而激动人心的新科学挑战。LVIS 见 http://www.lvisdataset.org。

**多目标具身问答（Multi-Target Embodied Question Answering）**
Licheng Yu、Xinlei Chen、Georgia Gkioxari、Mohit Bansal、Tamara Berg、Dhruv Batra
具身问答（EQA）是一个相对较新的任务：智能体被要求从自我中心感知回答关于其环境的问题。[8] 中引入的 EQA 做了一个基本假设：每个问题（如「汽车是什么颜色？」）恰好询问一个目标（「汽车」）。这一假设直接限制了智能体的能力。我们提出 EQA 的泛化——多目标 EQA（MT-EQA）。具体而言，我们研究包含多个目标的问题，如「卧室里的梳妆台比厨房里的烤箱大吗？」——智能体必须导航到多个位置（「卧室的梳妆台」「厨房的烤箱」）并执行比较推理（「梳妆台」比「烤箱」大）才能回答。这类问题需要在智能体中开发全新的模块或组件。为此，我们提出一个由程序生成器、控制器、导航器和 VQA 模块组成的模块化架构：程序生成器把给定问题转换为顺序可执行的子程序；导航器引导智能体前往与导航相关子程序有关的多个位置；控制器学习沿路径选择相关观测。这些观测随后被送入 VQA 模块预测答案。我们对每个模型组件做了详细分析，并表明联合模型能以显著优势胜过以往方法与强基线。项目页面：https://embodiedqa.org。

**用生成式潜在最近邻做非对抗图像合成（Non-Adversarial Image Synthesis with Generative Latent Nearest Neighbors）**
Yedid Hoshen、Jitendra Malik
无条件图像生成近来由生成对抗网络（GAN）主导。GAN 方法训练一个从随机噪声向量回归图像的生成器，以及一个试图区分生成图像与真实图像训练集的判别器。GAN 在生成逼真图像方面展现了惊人的结果。尽管成功，GAN 存在关键缺陷，包括训练不稳定和模式丢失。GAN 的这些弱点推动了替代方法研究，包括变分自编码器（VAE）、潜在嵌入学习方法（如 GLO）以及基于最近邻的隐式最大似然估计（IMLE）。遗憾的是，目前 GAN 在图像生成上仍显著优于这些替代方法。在本工作中，我们提出一种新方法——生成式潜在最近邻（GLANN）——无需对抗训练即可训练生成模型。GLANN 以克服各自主要缺陷的方式结合了 IMLE 与 GLO 的优势。因此，GLANN 生成的图像远优于 GLO 与 IMLE。我们的方法不存在困扰 GAN 训练的模式崩溃，且稳定得多。定性结果表明 GLANN 在常用数据集上胜过由 800 个 GAN 与 VAE 组成的基线。我们的模型还被证明能有效训练真正非对抗的无监督图像翻译。

**全景特征金字塔网络（Panoptic Feature Pyramid Networks）**
Alexander Kirillov、Ross Girshick、Kaiming He、Piotr Dollár
新近提出的全景分割任务重新唤起了社区对统一实例分割（针对 thing 类）与语义分割（针对 stuff 类）的兴趣。然而，当前这一联合任务的最先进方法为实例分割与语义分割使用彼此分离且互不相似的网络，没有任何共享计算。在本工作中，我们致力于在架构层面统一这些方法，为两个任务设计单一网络。我们的做法是为流行的实例分割方法 Mask R-CNN 配备一个使用共享特征金字塔网络（FPN）主干的语义分割分支。令人惊讶的是，这个简单基线不仅对实例分割依然有效，还产出了一个轻量、顶尖的语义分割方法。在本工作中，我们对这个最小扩展的带 FPN 的 Mask R-CNN（称为 Panoptic FPN）进行了详细研究，表明它是两个任务稳健而准确的基线。鉴于其有效性与概念上的简洁性，我们希望该方法能成为强基线并助力未来的全景分割研究。

**全景分割（Panoptic Segmentation）**
Alexander Kirillov、Kaiming He、Ross Girshick、Carsten Rother、Piotr Dollár
我们提出并研究了一个名为全景分割（PS）的任务。全景分割统一了通常彼此独立的语义分割（为每个像素分配类别标签）与实例分割（检测并分割每个物体实例）任务。该任务要求生成既丰富又完整的连贯场景分割，这是迈向现实世界视觉系统的重要一步。虽然计算机视觉的早期工作处理过相关的图像/场景解析任务，但它们目前并不流行，可能由于缺乏合适的指标或配套的识别挑战赛。为此，我们提出一个新的全景质量（PQ）指标，以可解释且统一的方式涵盖所有类别（stuff 与 things）的性能。利用所提指标，我们在三个现有数据集上对人类与机器的 PS 表现进行了严格研究，揭示了关于该任务的有趣洞见。我们工作的目标是重新唤起社区对更统一的图像分割视角的兴趣。

**用主动采集降低欠采样 MRI 重建中的不确定性（Reducing Uncertainty in Undersampled MRI Reconstruction with Active Acquisition）**
Zizhao Zhang、Adriana Romero、Matthew J. Muckley、Pascal Vincent、Lin Yang、Michal Drozdzal
MRI 重建的目标是从部分观测中恢复高保真图像。这种部分视角天然引入重建不确定性，只能通过采集额外测量来降低。在本文中，我们提出一种新的 MRI 重建方法：在推断时动态选择要采集的测量并迭代精化预测，以最大程度降低重建误差及其不确定性。我们在大规模膝关节 MRI 数据集以及 ImageNet 上验证了方法。结果表明：（1）我们的系统成功胜过主动采集基线；（2）我们的不确定性估计与误差图相关；（3）我们基于 ResNet 的架构在 MRI 重建任务上超越标准像素到像素模型。所提方法不仅展示了高质量重建，也为加速 MRI 的更实用方案铺平了道路。

**用于单目性能追踪的高保真人脸模型自监督适配（Self-Supervised Adaptation of High-Fidelity Face Models for Monocular Performance Tracking）**
Jae Shin Yoon、Takaaki Shiratori、Shoou-I Yu、Hyun Soo Park
数据采集与人脸建模技术的进步使我们能够创建高保真的逼真人脸模型。然而，驱动这些逼真人脸模型需要特殊输入数据，如 3D 网格与展开纹理。而且这些模型期望在受控实验室环境下采集的干净输入，与野外收集的数据差别很大。这些约束使高保真模型难以用于普通摄像头的追踪。在本文中，我们提出一种自监督域适配方法，使高保真人脸模型能由普通摄像头驱动。我们的方法首先通过训练一个仅凭单张 2D 图像即可直接驱动人脸模型的新网络，绕开对特殊输入数据的需求；然后，基于「相邻帧纹理一致性」执行自监督域适配来克服实验室与不受控环境之间的域失配——其假设是人脸外观在相邻帧间保持一致，从而避免对照明或背景等新环境建模。实验表明，我们能够仅凭手机摄像头驱动高保真人脸模型完成复杂的面部运动，无需来自新域的任何标注数据。

**Slim DensePose：从稀疏标注与运动线索中节俭学习（Slim DensePose: Thrifty Learning from Sparse Annotations and Motion Cues）**
Natalia Neverova、James Thewlis、Riza Alp Güler、Iasonas Kokkinos、Andrea Vedaldi
DensePose 通过把图像像素密集映射到人体表面坐标，超越了传统关键点检测器。然而这种能力以大幅增加的标注成本为代价——监督模型需要为每个姿态实例手工标注数百个点。因此在本工作中，我们寻求大幅精简 DensePose 标注的方法，提出更高效的数据采集策略。特别地，我们证明如果标注在视频帧中采集，用运动线索可以让其效力免费倍增。为探索这一想法，我们引入 DensePose-Track——一个选定帧以传统 DensePose 方式标注的视频数据集。然后，依托 DensePose 映射的几何特性，我们利用视频动态在时间上传播真值标注，并从孪生等变性约束中学习。在对各种数据标注与学习策略做了详尽实证评估后，我们证明这样做能比强基线带来显著改进的姿态估计结果。然而，与一些近期工作暗示的相反，我们表明仅通过对孤立帧施加几何变换来合成运动模式的效果明显较差，运动线索从视频中提取时帮助要大得多。

**StereoDRNet：膨胀残差立体网络（StereoDRNet: Dilated Residual StereoNet）**
Rohan Chabra、Julian Straub、Chris Sweeney、Richard Newcombe、Henry Fuchs
我们提出一个用卷积神经网络（CNN）从立体图像对估计深度、随后对预测深度图做体素融合以生成场景 3D 重建的系统。我们提出的深度精化架构预测视角一致的视差与遮挡图，帮助融合系统产出几何一致的重建。我们在代价滤波网络中使用 3D 膨胀卷积，滤波效果更好且计算成本几乎减半（相较最先进的代价滤波架构）。特征提取采用 Vortex Pooling 架构。所提方法在 KITTI 2012、KITTI 2015 和 ETH 3D 立体基准上取得最先进结果。最后，我们证明该系统能产出高保真 3D 场景重建，胜过最先进的立体系统。

**发丝级多视角头发捕捉（Strand-Accurate Multi-View Hair Capture）**
Giljoo Nam、Chenglei Wu、Min H. Kim、Yaser Sheikh
头发是最难重建的物体之一，因为它具有微观结构、大量重复发丝且遮挡严重。在本文中，我们提出首个以发丝级精度捕捉高保真头发几何的方法。该方法分三个阶段：第一阶段提出一种带倾斜支撑线的新型多视角立体重建方法，求解不同视角间的头发对应关系。具体而言，我们贡献了一个由光度一致性项与几何项组成的新代价函数，把每个头发像素重建为一条 3D 直线。合并所有深度图后，得到点云及每个点的局部直线方向。于是第二阶段提出一种用均值漂移把含噪点数据转换为一组发丝的发丝重建方法。最后，我们用多视角几何约束生长发丝，延长短发丝并恢复缺失发丝，从而显著提升重建完整度。我们在合成数据与真实采集数据上评估了方法，表明该方法能以亚毫米精度重建发丝。

**跳出图像池：为相对属性主动创建训练图像（Thinking Outside the Pool: Active Training Image Creation for Relative Attributes）**
Aron Yu、Kristen Grauman
当前共识是标注图像数据越多越好，而获取标注是瓶颈。然而，策划一个足够多样且信息丰富的图像池本身就是挑战。对细粒度属性尤其如此——感兴趣的细微视觉差异在传统图像来源中可能很罕见。我们提出主动图像生成方法来解决这一问题。主要思想是联合学习属性排序任务，同时学习生成能让该任务受益的新颖逼真图像样本。我们引入一个端到端框架：动态「想象」会迷惑当前模型的图像对，呈现给人工标注者标注，再用新样本改进预测模型。在两个数据集上，我们表明通过跳出真实图像池思考，我们的方法在富有挑战的细粒度属性比较上获得泛化精度增益。

**迈向会阅读的 VQA 模型（Towards VQA Models That Can Read）**
Amanpreet Singh、Vivek Natarajan、Meet Shah、Yu Jiang、Xinlei Chen、Dhruv Batra、Devi Parikh、Marcus Rohrbach
研究表明，视障用户就周围环境图像提出的主要问题类别之一涉及读取图像中的文字。但如今的 VQA 模型不会阅读！我们的论文朝解决这一问题迈出第一步。首先，我们引入新的「TextVQA」数据集以推动这一重要问题的进展。现有数据集要么关于文字的问题占比很小（如 VQA 数据集），要么规模太小（如 VizWiz 数据集）。TextVQA 包含 28408 张图像上的 45336 个需要推理文字才能回答的问题。其次，我们引入一种新颖的模型架构：读取图像中的文字，在图像与问题上下文中对其进行推理，并预测答案——答案可能是基于文字与图像的推断，也可能由图像中发现的字符串组成。因此我们把方法称为「看、读、推理与回答」（Look, Read, Reason & Answer，LoRRA）。我们表明 LoRRA 在 TextVQA 数据集上胜过现有最先进 VQA 模型。我们发现 TextVQA 上人类与机器的性能差距显著大于 VQA 2.0，说明 TextVQA 非常适合作为 VQA 2.0 互补方向的基准。https://textvqa.org，代码库见 GitHub。

## CVPR 的其他活动

（完整组织者与讲者名单见 CVPR 网站。）

- 动作分类与视频建模（教程）——Christoph Feichtenhofer、Lorenzo Torresani，组织者
- 多目标跟踪基准（MOTChallenge）研讨会——Georgia Gkioxari，受邀讲者
- 把机器人带入计算机视觉社区（教程）——Abhinav Gupta，受邀讲者；Saurabh Gupta，组织者
- 五年后的计算机视觉研讨会——Saurabh Gupta，组织者
- 面向 AR/VR 的计算机视觉研讨会——Fernando De la Torre、Matt Uyttendaele，组织者；Richard Newcombe、Yaser Sheikh，讲者
- 实用 3D 摄影（演示）
- 面向全球挑战的计算机视觉（CV4GC）研讨会——Laura Sevilla-Lara、Yannis Kalantidis，主要组织者
- 面向语义视觉导航的深度学习研讨会——Georgia Gkioxari，受邀讲者
- DeepVision 研讨会——Cristian Canton、Yann LeCun，组织者；Laurens van der Maaten、Alex Berg，讲者
- 面向计算机视觉的高效深度学习——Peter Vajda，组织者；Yangqing Jia，讲者
- 自我中心感知、交互与计算（EPIC）研讨会——Kristen Grauman，组织者
- Habitat：具身智能体挑战赛与研讨会——Richard Newcombe、Jitendra Malik，讲者；Manolis Savva、Abhishek Kadian、Oleksandr Maksymets、Julian Straub、Bhavana Jain、Devi Parikh、Georgia Gkioxari、Marcus Rohrbach、Jitendra Malik、Erik Wijmans、Dhruv Batra，组织者
- 媒体取证研讨会——Cristian Canton，组织者
- 预认知：透过未来研讨会——论文《Leveraging the Present to Anticipate the Future in Videos》——Antoine Miech、Ivan Laptev、Josef Sivic、Heng Wang、Lorenzo Torresani、Du Tran
- 视觉与声音研讨会——Kristen Grauman，组织者
- 理解数据的主观属性：聚焦时尚与主观搜索——Kristen Grauman、Devi Parikh，组织者
- 视觉问答与对话——Amanpreet Singh、Meet Shah、Xinlei Chen、Marcus Rohrbach、Dhruv Batra、Devi Parikh，组织者
- 视觉识别及更多（教程）——Christoph Feichtenhofer、Kaiming He、Ross Girshick、Georgia Gkioxari、Alexander Kirillov、Piotr Dollár，组织者
- 计算机视觉中的女性（WiCV）研讨会——Devi Parikh、Judy Hoffman，讲者
