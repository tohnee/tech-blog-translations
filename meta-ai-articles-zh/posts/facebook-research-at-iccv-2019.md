---
title: "Facebook 研究团队在 ICCV 2019"
title_en: "Facebook Research at ICCV 2019"
date: 2019-03-15
source: https://ai.facebook.com/blog/facebook-research-at-iccv-2019
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 研究团队在 ICCV 2019

> 原文：[Facebook Research at ICCV 2019](https://ai.facebook.com/blog/facebook-research-at-iccv-2019) · Meta AI（Wayback 存档）

Facebook 的研究员将于 10 月 27 日至 11 月 2 日在韩国首尔参加国际计算机视觉会议（ICCV），与来自世界各地的计算机视觉专家讨论最新进展。这一研究会议是该领域领袖最负盛名的聚会之一，将有超过 5000 名学生、学者、业界专业人士和研究者出席。会议期间，Facebook 的研究者将通过口头报告、海报环节、研讨会和教程展示 40 多篇论文，主题包括：全新的具身 AI 研究平台；利用解释让视觉与语言模型更落地；大规模新物体描述；用新 3D-Craft 数据集做顺序感知生成建模；360 度感知与交互；以及面向时尚、艺术与设计的计算机视觉。参加会议的人请务必到 Facebook Research 的 C4 展位，与我们的计划经理、研究员和招聘人员交流。演示与展位活动安排如下：

- 演示：时尚分割（Fashion Segmentation）
- 演示：Habitat——人机对战（Beat the Bot）
- 演示：Quest 上的 Replica
- Detectron2 预览：10 月 29 日（周二）16:00-16:30
- 深度伪造检测挑战赛预览：10 月 30 日（周三）11:30-12:00

ICCV 研究展示的逐日日程见此处。

## Facebook 在 ICCV 上展示的研究

**Align2Ground：由图像-描述对齐引导的弱监督短语落地（Align2Ground: Weakly Supervised Phrase Grounding Guided by Image-Caption Alignment）**
Samyak Datta、Karan Sikka、Anirban Roy、Karuna Ahuja、Devi Parikh、Ajay Divakaran
我们利用图像-描述对的弱监督解决自由形式文本短语的落地问题。我们提出一个新颖的端到端模型，用描述到图像检索作为「下游」任务来引导短语定位过程。我们的方法第一步推断感兴趣区域（RoI）与描述中短语之间的潜在对应，并用这些匹配的 RoI 创建判别性图像表示；第二步把学到的表示与描述对齐。我们的关键贡献在于构建这种「描述条件化」的图像编码，它紧密耦合两个任务，使弱监督能有效引导视觉落地。我们提供了详尽的实证与定性分析，考察所提模型的不同组件，并与有竞争力的基线比较。在短语定位上，我们在 VisualGenome 与 Flickr30k Entities 数据集上分别比此前最先进水平提高 4.9% 与 1.3%（绝对值）。我们还在 COCO 与 Flickr30k 数据集的下游描述到图像检索任务上报告了与最先进水平相当的结果。

**C3DPO：面向非刚性运动恢复结构的规范 3D 姿态网络（C3DPO: Canonical 3D Pose Networks for Non-Rigid Structure from Motion）**
David Novotny、Nikhila Ravi、Benjamin Graham、Natalia Neverova、Andrea Vedaldi
我们提出 C3DPO——一种从无约束图像的 2D 关键点标注中提取可变形物体 3D 模型的方法。我们通过学习一个每次从单一视图重建 3D 物体的深度网络来实现，它能处理部分遮挡，并显式分解视角变化与物体变形的影响。为实现这一分解，我们引入一种新颖的正则化技术。我们首先证明：当且仅当重建形状存在某个规范化函数时，分解才会成功。然后我们把规范化函数与重建函数一起学习，约束结果保持一致。在包括 Up3D 与 PASCAL3D+ 在内的多个基准上，我们为不使用真值 3D 监督的方法展示了最先进的重建结果。

**通过几何循环一致性的规范表面映射（Canonical Surface Mapping via Geometric Cycle Consistency）**
Nilesh Kulkarni、Abhinav Gupta、Shubham Tulsiani
我们探索规范表面映射（CSM）任务。具体而言，给定一张图像，我们学习把物体上的像素映射到该类别抽象 3D 模型上的对应位置。但如何学习这样的映射？有监督方法需要大量手工标注，无法扩展到少数几个挑选类别之外。我们的关键洞察是：CSM 任务（像素到 3D）与 3D 投影（3D 到像素）结合可构成一个循环。因此，我们可以利用几何循环一致性损失，从而免去稠密的人工监督。我们的方法只需前景掩码标签即可训练，为多样化的类别集合训练 CSM 模型，无需稀疏或稠密关键点标注。我们表明，预测还允许推断两张图像之间的稠密对应，并把我们的方法与利用不同程度监督预测对应的多种方法进行了性能比较。

**Cap2Det：学习放大弱描述监督用于目标检测（Cap2Det: Learning to Amplify Weak Caption Supervision for Object Detection）**
Keren Ye、Mingda Zhang、Adriana Kovashka、Wei Li、Danfeng Qin、Jesse Berent
学习定位并命名物体实例是视觉的基础问题，但最先进的方法依赖昂贵的边界框监督。弱监督检测（WSOD）方法把对框的需求放宽到图像级标注，而更便宜的监督其实天然可得——用户上传图像内容时可自由提供的非结构化文本描述。然而，把这类数据用于 WSOD 的直接方法会浪费地丢弃与物体名称不完全匹配的描述。我们转而展示如何通过训练一个能泛化到数据集边界之外的纯文本分类器，从这些描述中榨取最多信息。这一发现为从带噪但更丰富、免费可得的描述数据中学习检测模型提供了机会。我们还在三个经典目标检测基准上验证模型，取得最先进的 WSOD 性能。代码在此公开。

**视觉物体的声音协同分离（Co-Separating Sounds of Visual Objects）**
Ruohan Gao、Kristen Grauman
从视频中学习物体的声音颇具挑战，因为它们常在单一音频通道中高度重叠。当前的视觉引导音频源分离方法通过人工混合视频片段训练来回避这一问题，但这给训练数据收集带来了笨重的限制，甚至可能阻碍学习「真正」混合声音的性质。我们引入协同分离（co-separation）训练范式，允许从无标注多源视频中学习物体级声音。我们新颖的训练目标要求深度神经网络为外观相似的物体分离出的音频保持一致可辨识，同时为每个源训练对重现准确的视频级音轨。我们的方法能在逼真测试视频中解耦声音，即使某物体在训练中从未被单独观察过。我们在 MUSIC、AudioSet 与 AV-Bench 数据集上的视觉引导音频源分离与音频去噪任务上取得最先进结果。

**组合式视频预测（Compositional Video Prediction）**
Yufei Ye、Maneesh Singh、Abhinav Gupta、Shubham Tulsiani
我们提出一种给定场景输入图像做像素级未来预测的方法。我们观察到场景由经历运动的不同实体组成，并提出把这一洞察具体化的方法。我们隐式预测独立实体的未来状态并推理其交互，再用这些预测状态合成未来视频帧。我们用全局轨迹级潜在随机变量克服任务固有的多模态性，并表明这使我们能采样多样且合理的未来。我们对照替代表示与多模态纳入方式实证验证了方法。我们考察了两个数据集——一个由可能倒塌的堆叠物体组成，另一个包含人在健身房活动的视频——并表明我们的方法在这些多样设置下都能进行逼真的随机视频预测。视频预测见项目网站。

**面向细粒度视觉分类的 Cross-X 学习（Cross-X Learning for Fine-Grained Visual Categorization）**
Wei Luo、Xitong Yang、Xianjie Mo、Yuheng Lu、Larry S. Davis、Jun Li、Jian Yang、Ser-Nam Lim
由于巨大的类内差异与微小的类间差异，识别差异细微的子类别物体仍是挑战。近期工作以弱监督方式处理这一问题：先检测物体部分，再提取相应的部分特定特征用于细粒度分类。然而这些方法通常孤立地对待每张图像的部分特定特征，忽略了不同图像之间的关系。在本文中，我们提出 Cross-X 学习——一种简单而有效的方法，利用不同图像之间与不同网络层之间的关系进行鲁棒的多尺度特征学习。我们的方法包含两个新颖组件：1）跨类别跨语义正则化器，引导提取的特征表示语义部分；2）跨层正则化器，通过匹配多层间的预测分布提升多尺度特征的鲁棒性。我们的方法可轻松端到端训练，并可扩展到 NABirds 等大型数据集。我们实证分析了方法各组件的贡献，并在五个基准数据集上展示了其鲁棒性、有效性与最先进性能。代码在此公开。

**DenseRaC：通过稠密渲染比较联合估计 3D 姿态与形状（DenseRaC: Joint 3D Pose and Shape Estimation by Dense Render-and-Compare）**
Yuanlu Xu、Song-Chun Zhu、Tony Tung
我们提出 DenseRaC——一个从单目 RGB 图像联合估计 3D 人体姿态与体型的全新端到端框架。我们的两步框架以身体像素到表面对应图（即 IUV 图）为代理表示，然后执行参数化人体姿态与形状估计。具体而言，给定估计的 IUV 图，我们开发了一个优化 3D 身体重建损失的深度神经网络，并进一步集成渲染比较方案，以最小化输入与渲染输出（即稠密身体关键点、身体部位掩码与对抗先验）之间的差异。为促进学习，我们进一步利用网络抓取的动作捕捉序列、3D 扫描与动画构建了大规模合成数据集（MOCA）。生成的数据覆盖多样的相机视角、人体动作与体型，并配有完整真值。我们的模型从混合数据集中联合学习表示 3D 人体，缓解了训练数据不成对的问题。实验表明，DenseRaC 在多个人体相关任务的公开基准上优于最先进水平。

**DistInit：无需任何标注视频学习视频表示（DistInit: Learning Video Representations Without a Single Labeled Video）**
Rohit Girdhar、Du Tran、Lorenzo Torresani、Deva Ramanan
过去几年，视频识别模型进展显著，从在手工特征上训练的浅层分类器演进到深度时空网络。然而，训练这类模型所需的标注视频数据，已跟不上网络深度与复杂度的持续增长。在本工作中，我们提出学习视频表示的替代方法：不需要任何语义标注视频，转而利用多年来在收集与标注大型干净静态图像数据集上的投入。我们用在图像数据集上预训练的最先进模型作为「教师」，在蒸馏框架中训练视频模型。我们证明，尽管只使用来自静态图像网络的监督，我们的方法学到的是真正的时空特征。此外，它用完全未筛选的原始视频数据源与不同 2D 教师模型，也能在不同输入模态上学到良好表示。我们的方法获得了强劲的迁移性能，相较用图像模型引导视频架构的标准技术高出 16%。我们相信该方法为从无标注视频数据学习时空表示开辟了新途径。

**降一个八度：用八度卷积减少卷积神经网络的空间冗余（Drop an Octave: Reducing Spatial Redundancy in Convolutional Neural Networks with the Octave Convolution）**
Yunpeng Chen、Haoqi Fan、Bing Xu、Zhicheng Yan、Yannis Kalantidis、Marcus Rohrbach、Shuicheng Yan、Jiashi Feng
在自然图像中，信息以不同频率传递：高频通常编码精细细节，低频通常编码全局结构。类似地，卷积层输出的特征图也可视为不同频率信息的混合。在本工作中，我们提议按频率分解混合特征图，并设计新颖的八度卷积（OctConv）操作，以更低的空间分辨率存储和处理空间上变化「较慢」的特征图，同时降低内存与计算成本。与现有多尺度方法不同，OctConv 被表述为单一、通用、即插即用的卷积单元，可直接替换（普通）卷积而无需对网络架构做任何调整。它也与建议更好拓扑或减少通道冗余（如分组或深度卷积）的方法正交互补。我们实验证明，只需把卷积替换为 OctConv，即可在图像与视频识别任务上一致提升精度，同时降低内存与计算成本。配备 OctConv 的 ResNet-152 在 ImageNet 上仅用 22.2 GFLOPs 即可达到 82.9% 的 top-1 分类精度。

**高效分割：学习在语义边界附近下采样（Efficient Segmentation: Learning Downsampling Near Semantic Boundaries）**
Dmitrii Marin、Zijian He、Peter Vajda、Priyam Chatterjee、Sam Tsai、Fei Yang、Yuri Boykov
自动驾驶等许多自动化流程依赖良好的语义分割作为关键组件。为加速性能，常见做法是对输入帧下采样。但这会以遗漏小物体与语义边界精度下降为代价。为解决该问题，我们提出一种新的内容自适应下采样技术，学习偏好目标类别语义边界附近的采样位置。成本-性能分析表明，我们的方法一致优于均匀采样，改进了精度与计算效率之间的平衡。我们的自适应采样带来边界质量更好、对小尺寸物体支持更可靠的分割。

**具身超越模态识别：学习移动以感知物体（Embodied Amodal Recognition: Learning to Move to Perceive Objects）**
Jianwei Yang、Zhile Ren、Mingze Xu、Xinlei Chen、David J. Crandall、Devi Parikh、Dhruv Batra
被动视觉系统通常无法在物体被严重遮挡的超越模态（amodal）设置下识别物体。相比之下，人类和其他具身智能体能够在环境中移动并主动控制视角，以更好地理解物体形状与语义。在本工作中，我们引入具身超越模态识别（EAR）任务：智能体被实例化在 3D 环境中靠近一个被遮挡的目标物体，可在环境中自由移动以执行物体分类、超越模态物体定位与超越模态物体分割。为解决该问题，我们开发了一个名为 Embodied Mask R-CNN 的新模型，让智能体学会策略性移动以提升视觉识别能力。我们使用室内环境仿真器进行实验。实验结果表明：1）具备具身性（移动）的智能体取得比被动智能体更好的视觉识别性能；2）为提升视觉识别能力，智能体可以学到与最短路径不同的策略性路径。

**用中间层攻击增强对抗样本可迁移性（Enhancing Adversarial Example Transferability with an Intermediate-Level Attack）**
Qian Huang、Isay Katsman、Horace He、Zeqi Gu、Serge Belongie、Ser-Nam Lim
神经网络容易受到对抗样本——为欺骗训练模型而精心构造的恶意输入——的攻击。对抗样本常表现出黑盒迁移性：为一个模型构造的对抗样本可以欺骗另一个模型。然而，对抗样本通常过拟合于利用源模型的特定架构与特征表示，导致对其他目标模型的黑盒迁移攻击次优。我们引入中间层攻击（ILA），试图通过增大对抗样本在源模型某个预设层上的扰动，来微调现有对抗样本以获得更强的黑盒可迁移性，改进了最先进方法。我们表明，可以在对目标模型一无所知的情况下选择源模型中要扰动的层，同时获得高可迁移性。此外，我们对方法以及在中间特征图上优化对抗样本的效果提供了一些解释性洞见。

**探索用于图像识别的随机连接神经网络（Exploring Randomly Wired Neural Networks for Image Recognition）**
Saining Xie、Alexander Kirillov、Ross Girshick、Kaiming He
图像识别的神经网络经过大量手工设计，从简单的链式模型演进到拥有多条连线路径的结构。ResNets [12] 与 DenseNets [17] 的成功很大程度上归功于其创新的连接方案。如今，神经架构搜索（NAS）研究正在探索连接与操作类型的联合优化，但可能连接的空间是受限的，且尽管经过搜索，仍由手工设计驱动。在本文中，我们通过随机连接神经网络的视角探索更多样的连接模式。为此，我们首先定义封装整个网络生成过程的随机网络生成器概念。封装为 NAS 与随机连接网络提供了统一视角。然后，我们用三种经典随机图模型为网络生成随机连接图。结果令人惊讶：这些随机生成器的若干变体产生的网络实例在 ImageNet 基准上具有有竞争力的精度。这些结果表明，专注于设计更好网络生成器的新努力，可能通过探索约束更少、新颖设计空间更大的搜索空间带来新突破。代码已公开。

**Fashion++：改进穿搭的极小编辑（Fashion++: Minimal Edits for Outfit Improvement）**
Wei-Lin Hsiao、Isay Katsman、Chao-Yuan Wu、Devi Parikh、Kristen Grauman
给定一套穿搭，哪些小改动最能提升其时尚度？这个问题提出了一个引人入胜的新视觉挑战。我们引入 Fashion++——一种对全身服装穿搭提出最小调整、却对时尚度产生最大影响的方法。我们的模型由一个深度图像生成神经网络组成，学习在逐件服装编码的条件下合成衣物。潜在编码按形状与纹理显式分解，从而分别允许对合身度/呈现方式与颜色/图案/材质的直接编辑。我们展示了如何借助网络照片自举训练一个时尚度模型，并开发了一种激活最大化式的方法，把输入图像变换为更时尚的版本。建议的编辑范围从换一件新衣物到调整其颜色、穿着方式（如卷起袖子）或合身度（如让裤子更宽松）。实验表明，无论按自动指标还是人类意见，Fashion++ 都能提供成功的编辑。

**从视频落地的人-物交互热点（Grounded Human-Object Interaction Hotspots from Video）**
Tushar Nagarajan、Christoph Feichtenhofer、Kristen Grauman
学习如何与物体交互是迈向具身视觉智能的重要一步，但现有技术受制于繁重的监督或传感要求。我们提出直接从视频学习人-物交互「热点」的方法。我们的方法不把可供性当作手工监督的语义分割任务，而是通过观看真实人类行为的视频并预测可实现的动作来学习交互。给定一张新图像或视频，我们的模型推断一个空间热点图，指示潜在交互中物体会被操作的位置——即使物体目前静止。通过第一人称与第三人称视频的结果，我们展示了把可供性落地到真实人-物交互中的价值。我们的弱监督热点不仅可与强监督的可供性方法竞争，还能预测新物体类别的物体交互。项目页面：http://vision.cs.utexas.edu/projects/interaction-hotspots/

**Habitat：具身 AI 研究平台（Habitat: A Platform for Embodied AI Research）**
Manolis Savva、Abhishek Kadian、Oleksandr Maksymets、Yili Zhao、Erik Wijmans、Bhavana Jain、Julian Straub、Jia Liu、Vladlen Koltun、Jitendra Malik、Devi Parikh、Dhruv Batra
我们提出 Habitat——一个具身人工智能（AI）研究平台。Habitat 支持在高效逼真的 3D 仿真中训练具身智能体（虚拟机器人）。具体而言，Habitat 由两部分组成：1）Habitat-Sim：一个灵活、高性能的 3D 仿真器，支持可配置的智能体、传感器与通用 3D 数据集处理。Habitat-Sim 很快——渲染 Matterport3D 场景时，单线程即可达到每秒数千帧（fps），单 GPU 多进程可超过 10000 fps。2）Habitat-API：一个模块化高层库，用于具身 AI 算法的端到端开发——定义任务（如导航、指令遵循、问答）、配置、训练与基准测试具身智能体。

**IMP：面向高精度 Thing 语义分割的实例掩码投影（IMP: Instance Mask Projection for High Accuracy Semantic Segmentation of Things）**
Cheng-Yang Fu、Tamara L. Berg、Alexander C. Berg
在本工作中，我们提出一个名为实例掩码投影（IMP）的新算子，把预测的实例分割投影为语义分割的新特征。它还支持反向传播，因此可端到端训练。通过添加该算子，我们引入了在语义分割中结合自上而下与自下而上信息的新范式。实验展示了 IMP 在服装解析（复杂层叠、大变形与非凸物体）与街景分割（大量重叠实例与小物体）上的有效性。在多样服装解析数据集（VCP）上，实例掩码投影在最先进 Panoptic FPN 分割方法之上把 mIoU 提升三个点。在 ModaNet 服装解析数据集上，相较现有基线语义分割结果绝对提升高达 20.4%。此外，实例掩码投影算子在其他（非服装）数据集上也表现良好，在最先进方法之上为 Cityscapes 与一个自动驾驶数据集的 Thing 类 mIoU 提升三个点。

**面向视频预测的改进条件 VRNN（Improved Conditional VRNNs for Video Prediction）**
Lluís Castrejon、Nicolas Ballas、Aaron Courville
为视频序列预测未来帧是一项富有挑战的生成建模任务。有前景的方法包括变分自编码器等概率隐变量模型。虽然 VAE 能处理不确定性并建模多种可能的未来结果，但它们往往产生模糊的预测。在本工作中，我们论证这是欠拟合的表现。为解决该问题，我们提议增加隐变量分布的表达能力并使用更高容量的似然模型。我们的方法依赖一个隐变量层级，定义了一族灵活的先验与后验分布，以更好地建模未来序列的概率。我们通过一系列消融实验验证了提议，并把方法与当前最先进的隐变量模型比较。我们的方法在三个不同数据集的多项指标下表现良好。

**视频中的人脸实时去标识（Live Face De-Identification in Video）**
Oran Gafni、Lior Wolf、Yaniv Taigman
我们提出一种人脸去标识方法，支持高帧率下的全自动视频修改。目标是在保持感知（姿态、光照与表情）不变的同时，最大程度地去关联身份。我们通过一个新颖的前馈编码器-解码器网络架构实现，它以人脸图像的高层表示为条件。该网络是全局的——不需要针对给定视频或给定身份重新训练——并生成随时间失真极小的自然图像序列。

**Mesh R-CNN**
Georgia Gkioxari、Jitendra Malik、Justin Johnson
2D 感知的快速进展带来了能精确检测真实世界图像中物体的系统。然而这些系统的预测是 2D 的，忽略了世界的 3D 结构。与此同时，3D 形状预测的进展大多聚焦于合成基准与孤立物体。我们统一了这两个领域的进展，提出一个在真实世界图像中检测物体并为每个检测到的物体输出给出完整 3D 形状的三角网格的系统。我们的系统称为 Mesh R-CNN，在 Mask R-CNN 上增加网格预测分支：先预测粗糙体素表示，转换为网格，再用作用于网格顶点与边的图卷积网络精化，从而输出拓扑结构各异的网格。我们在 ShapeNet 上验证网格预测分支，在单图像形状预测上超越以往工作。随后我们把完整的 Mesh R-CNN 系统部署到 Pix3D 上，联合检测物体并预测其 3D 形状。

**NoCaps：大规模新物体描述（NoCaps: Novel Object Captioning at Scale）**
Harsh Agrawal、Karan Desai、Yufei Wang、Xinlei Chen、Rishabh Jain、Mark Johnson、Dhruv Batra、Devi Parikh、Stefan Lee、Peter Anderson
图像描述模型在包含有限视觉概念与大量成对图像-描述训练数据的数据集上取得了亮眼成绩。然而，如果这些模型要在野外发挥作用，就必须学习更丰富的视觉概念，理想情况下从更少的监督中学习。为鼓励开发能从目标检测数据集等替代数据源学习视觉概念的图像描述模型，我们提出该任务的首个大规模基准。这个基准称为 nocaps（novel object captioning at scale，大规模新物体描述），由 166100 条人工生成的描述组成，描绘 Open Images 验证与测试集中的 15100 张图像。相关训练数据由 COCO 图像-描述对，加上 Open Images 的图像级标签与物体边界框组成。由于 Open Images 比 COCO 包含多得多的类别，测试图像中近 400 个物体类别没有或只有很少的相关训练描述（因此得名 nocaps）。我们扩展了现有的新物体描述模型，为该基准建立强基线，并提供分析以指导未来工作。

**论图像识别的网络设计空间（On Network Design Spaces for Image Recognition）**
Ilija Radosavovic、Justin Johnson、Saining Xie、Wan-Yen Lo、Piotr Dollár
过去几年，为视觉识别设计更好的神经网络架构的进展显著。为帮助保持这一进步速度，本工作提议重新审视比较网络架构的方法学。具体而言，我们引入分布估计这一新的比较范式：对采样模型总体应用统计技术来比较网络设计空间，同时控制网络复杂度等混淆因素。与当前比较模型族的点估计与曲线估计方法相比，分布估计更完整地呈现整个设计图景。作为案例研究，我们考察了神经架构搜索（NAS）中使用的设计空间，发现近期 NAS 设计空间变体之间存在在很大程度上被忽视的显著统计差异。此外，我们的分析揭示，ResNeXt 等标准模型族的设计空间可以与近期 NAS 工作使用的更复杂设计空间相当。我们希望这些分布分析的洞见能推动更稳健地发现更好的视觉识别网络。

**用 3D-Craft 数据集做顺序感知生成建模（Order-Aware Generative Modeling Using the 3D-Craft Dataset）**
Zhuoyuan Chen、Demi Guo、Tong Xiao、Saining Xie、Xinlei Chen、Haonan Yu、Jonathan Gray、Kavya Srinet、Haoqi Fan、Jerry Ma、Charles R. Qi、Shubham Tulsiani、Arthur Szlam、C. Lawrence Zitnick
2D 与 3D 生成模型的研究通常聚焦于最终产物，如图像或 3D 结构。与 2D 图像生成不同，现实世界中 3D 物体的生成通常受物体构建过程与顺序的约束。例如，搭建积木塔时需要考虑重力。在本文中，我们探索构造 3D 物体的有序动作预测。我们不基于物理约束预测动作，而是提议通过观察人类动作来学习。为支持大规模数据收集，我们使用 Minecraft 环境。我们引入 3D-Craft——一个新数据集，包含 2500 座由人类玩家从零开始按顺序搭建的 Minecraft 房屋。为从这些人类动作序列中学习，我们提出顺序感知的 3D 生成模型 VoxelCNN。与其他 3D 生成模型不同——它们要么没有显式顺序（如用 3DGAN [35] 的整体生成），要么遵循简单启发式顺序（如光栅扫描）——VoxelCNN 被训练为以空间感知模仿人类建造顺序。我们还将该顺序迁移到 ShapeNet [10] 等其他数据集。3D-Craft 数据集、模型与基准系统将公开，或可启发未来研究探索的新方向。

**面向部分监督多器官分割的先验感知神经网络（Prior-aware Neural Network for Partially Supervised Multi-Organ Segmentation）**
Yuyin Zhou、Zhe Li、Song Bai、Chong Wang、Xinlei Chen、Mei Han、Elliot Fishman、Alan L. Yuille
精确的多器官腹部 CT 分割对计算机辅助介入等许多临床应用至关重要。由于数据标注需要经验丰富的放射科医生投入大量人力，训练数据常常是部分标注的，例如胰腺数据集只标注了胰腺，其余都标记为背景。但在多器官分割中，这些背景标签可能有误导性，因为背景通常还包含其他感兴趣的器官。为解决这些部分标注数据集中的背景歧义，我们提出先验感知神经网络（PaNN），显式纳入腹部器官大小的解剖先验，用领域特定知识引导训练过程。更具体地说，PaNN 假设腹部平均器官大小分布应近似其经验分布——从完全标注数据集获得的先验统计。由于训练目标难以用随机梯度下降直接优化，我们提议将其重构为极小-极大形式，用随机原始-对偶梯度算法优化。PaNN 在 MICCAI2015 挑战赛「超越颅骨的多图集标注」（一项腹部器官分割竞赛）上取得最先进性能。我们报告了 84.97% 的平均 Dice 得分，大幅超越先前技术 3.27%。

**重新思考 ImageNet 预训练（Rethinking ImageNet Pre-training）**
Kaiming He、Ross Girshick、Piotr Dollár
我们报告了在 COCO 数据集上使用从随机初始化训练的标准模型得到的有竞争力的目标检测与实例分割结果。即便使用为微调预训练模型而优化的基线系统（Mask R-CNN）的超参数，结果也不逊于其 ImageNet 预训练对应版本——唯一例外是增加训练迭代次数，以便随机初始化的模型可以收敛。随机初始化训练出奇地鲁棒；即使 1）只使用 10% 的训练数据、2）用于更深更宽的模型、3）用于多个任务与指标，我们的结果依然成立。实验表明，ImageNet 预训练在训练早期加速收敛，但不一定提供正则化或提升最终目标任务精度。为突破极限，我们在不使用任何外部数据的情况下在 COCO 目标检测上达到 50.9 AP——与使用 ImageNet 预训练的 COCO 2017 竞赛顶尖结果相当。这些观察挑战了 ImageNet 预训练用于依赖任务的传统观念，我们期待这些发现将鼓励人们重新思考计算机视觉中预训练加微调的现行事实范式。

**自监督视觉表示学习的扩展与基准（Scaling and Benchmarking Self-Supervised Visual Representation Learning）**
Priya Goyal、Dhruv Mahajan、Abhinav Gupta、Ishan Misra
自监督学习旨在从数据本身学习表示，无需显式人工监督。现有努力忽略了自监督学习的一个关键方面——扩展到大量数据的能力，而自监督正是不需要人工标签。在本工作中，我们重访这一原则，把两种流行的自监督方法扩展到 1 亿张图像。我们表明，通过在多个轴上扩展（包括数据规模与问题「难度」），可以在目标检测、表面法线估计（3D）以及用强化学习的视觉导航等多种任务上，大幅匹配甚至超越有监督预训练的性能。扩展这些方法还为当前自监督技术与评估的局限提供了许多有趣洞见。我们的结论是：当前的自监督方法不够「难」，无法充分利用大规模数据，而且似乎学不到有效的高层语义表示。我们还引入了覆盖九个不同数据集与任务的广泛基准。我们相信，这样的基准与可比的评估设置对取得有意义的进展是必要的。代码见此处。

**SCSampler：从视频中采样显著片段以高效动作识别（SCSampler: Sampling Salient Clips from Video for Efficient Action Recognition）**
Bruno Korbar、Du Tran、Lorenzo Torresani
许多动作识别数据集由简短的修剪视频组成，每段包含一个相关动作，而真实世界的视频（如 YouTube 上的）性质很不同：它们往往长数分钟，简短的相关片段常与变化很少的长时段交错。对这类视频中的每个时间片段密集应用动作识别系统代价过高。而且，正如实验所示，这会导致识别精度次优——来自相关片段的信息性预测被视频中长而不具信息量片段上的无意义分类输出淹没。在本文中，我们引入一个轻量的「片段采样」模型，能高效识别长视频中最显著的时间片段。我们证明，只对这些最显著片段调用识别，可以大幅降低未修剪视频上动作识别的计算成本。此外，我们表明这相比分析所有片段或随机/均匀选择片段，带来显著的识别精度增益。在 Sports1M 上，我们的片段采样方案把已是最先进的动作分类器精度提高 7%，并把计算成本降低 15 倍以上。

**单网络全身姿态估计（Single-Network Whole-Body Pose Estimation）**
Gines Hidalgo、Yaadhav Raaj、Haroon Idrees、Donglai Xiang、Hanbyul Joo、Tomas Simon、Yaser Sheikh
我们提出首个用于 2D 全身姿态估计的单网络方法，即同时定位身体、面部、手与脚的关键点。得益于自下而上的表述，无论图像中有多少人，我们的方法都保持恒定的实时性能。网络通过多任务学习单阶段训练，采用能处理身体/脚与面部/手关键点之间尺度差异的改进架构。我们的方法在速度与整体精度上都大幅改进了 OpenPose [9]——此前唯一能做全身姿态估计的工作。与 [9] 不同，我们的方法不需要为每个手与脸候选运行额外网络，在多人场景下快得多。这项工作直接降低了需要 2D 全身信息的应用（如 VR/AR、重定向）的计算复杂度。此外，它还带来更高精度，尤其对被遮挡、模糊和低分辨率的面部与手。代码、训练模型与验证基准见我们的项目页面。

**面向视频识别的 SlowFast 网络（SlowFast Networks for Video Recognition）**
Christoph Feichtenhofer、Haoqi Fan、Jitendra Malik、Kaiming He
我们提出面向视频识别的 SlowFast 网络。我们的模型包括：1）以低帧率运行、捕捉空间语义的 Slow 通路；2）以高帧率运行、以精细时间分辨率捕捉运动的 Fast 通路。Fast 通路可通过减少通道容量做得非常轻量，却能学到对视频识别有用的时序信息。我们的模型在视频动作分类与检测上都取得强劲性能，SlowFast 概念带来的大幅提升被明确列为贡献。我们在 Kinetics、Charades 与 AVA 等主要视频识别基准上报告了最先进精度。代码已在此公开。

**SplitNet：面向具身视觉导航的 Sim2Sim 与任务到任务迁移（SplitNet: Sim2Sim and Task2Task Transfer for Embodied Visual Navigation）**
Daniel Gordon、Abhishek Kadian、Devi Parikh、Judy Hoffman、Dhruv Batra
我们提出 SplitNet——一种解耦视觉感知与策略学习的方法。通过纳入辅助任务与模型部分的选择性学习，我们把视觉导航的学习目标显式分解为感知世界与基于感知行动。我们在仿真器之间迁移上展示了相较基线模型的巨大改进，这是迈向 Sim2Real 的令人鼓舞的一步。此外，SplitNet 对来自同一仿真器的未见环境泛化更好，向新具身导航任务迁移更快更有效。进一步地，只给定目标域的小样本，SplitNet 即可匹配接收整个数据集的传统端到端流水线的性能。

**采纳提示（HINT）：利用解释让视觉与语言模型更落地（Taking a HINT: Leveraging Explanations to Make Vision and Language Models More Grounded）**
Devi Parikh、Dhruv Batra、Hongxia Jin、Larry Heck、Shalini Ghosh、Stefan Lee、Yilin Shen
许多视觉与语言模型存在视觉落地差的问题——往往退回到容易学习的语言先验，而非基于图像中的视觉概念做决策。在本工作中，我们提出一个名为人类重要性感知网络调优（HINT）的通用方法，有效利用人类演示改进视觉落地。HINT 鼓励深度网络对与人类相同的输入区域敏感。我们的方法优化人类注意力图与基于梯度的网络重要性之间的对齐——确保模型不仅学会「看」，而是学会依赖人类认为与任务相关的视觉概念来做预测。我们把 HINT 应用于视觉问答与图像描述任务，在惩罚过度依赖语言先验的划分（VQA-CP 与鲁棒描述）上胜过顶尖方法，而人类注意力演示仅用于 6% 的训练数据。

**Talking with Hands 16.2M：面向会话动作分析与合成的大规模身体-手指运动与音频同步数据集（Talking with Hands 16.2M: A Large-Scale Dataset of Synchronized Body-Finger Motion and Audio for Conversational Motion Analysis and Synthesis）**
Gilwoo Lee、Zhiwei Deng、Shugao Ma、Takaaki Shiratori、Siddhartha S. Srinivasa、Yaser Sheikh
我们提出一个 1620 万帧（50 小时）的多模态数据集，内容为两人面对面自发对话。数据集的特色是同步的身体与手指运动以及音频数据。据我们所知，它是迄今最大的自然对话动作捕捉与音频数据集。统计分析验证了手臂、手部与语音特征的强个体内与个体间协方差，有望为数据驱动的社交行为分析、预测与合成开辟新方向。作为示例，我们提出一种新颖的实时手指运动合成方法：一个创新性地用逆运动学（IK）损失训练的时间神经网络，为生成模型加入骨骼结构信息。定性用户研究表明，我们方法生成的手指运动被视为自然且增进对话，定量消融研究则证明了 IK 损失的有效性。

**面向零样本组合学习的任务驱动模块化网络（Task-Driven Modular Networks for Zero-Shot Compositional Learning）**
Senthil Purushwalkam、Maximilian Nickel、Abhinav Gupta、Marc'Aurelio Ranzato
人类智能的标志之一是能把学到的知识组合成新概念，并在没有一个训练样本的情况下识别它们。相比之下，当前最先进的方法需要为每个可能的类别提供数百个训练样本，才能构建可靠而精确的分类器。为缓解这种显著的效率差异，我们提出一个面向组合推理与样本高效学习的任务驱动模块化架构。我们的架构由一组神经网络模块组成，它们是在语义概念空间中运行的小型全连接层。这些模块通过以任务为条件的门控函数配置，产生表示输入图像与所考察概念之间兼容性的特征。这使我们能把任务表示为子任务的组合，并通过重新加权一组小模块泛化到未见类别。此外，该网络可以高效训练，因为它完全可微且模块在小子空间上运行。我们聚焦物体-属性类别的组合零样本分类问题。实验表明，当前的评估指标有缺陷，因为它们只考虑未见的物体-属性对。当把评估扩展到也考虑训练期间见过的对的广义设置时，我们发现朴素基线方法与当前方法表现相似甚至更好。而我们的模块化网络能够在两个广泛使用的基准数据集上胜过所有现有方法。

**TensorMask：稠密物体分割的基础（TensorMask: A Foundation for Dense Object Segmentation）**
Xinlei Chen、Kaiming He、Piotr Dollár、Ross Girshick
在稠密规则网格上生成边界框物体预测的滑动窗口检测器进展迅速且广受欢迎。相比之下，现代实例分割方法由先检测物体边界框、再裁剪并分割这些区域的方法主导（以 Mask R-CNN 为代表）。在本工作中，我们研究稠密滑动窗口实例分割范式——它出人意料地少有探索。我们的核心观察是：该任务与语义分割或边界框目标检测等其他稠密预测任务有根本不同，因为每个空间位置的输出本身就是具有自身空间维度的几何结构。为将其形式化，我们把稠密实例分割视为对 4D 张量的预测任务，并提出一个名为 TensorMask 的通用框架，显式捕捉这一几何结构并支持对 4D 张量的新算子。我们证明，张量视角相较忽略该结构的基线带来大幅提升，并取得与 Mask R-CNN 相当的结果。这些有前景的结果表明，TensorMask 可以作为稠密掩码预测新进展的基础，并帮助更完整地理解该任务。代码将公开。

**有监督分类任务的可迁移性与难度（Transferability and Hardness of Supervised Classification Tasks）**
Anh T. Tran、Cuong V. Nguyen、Tal Hassner
我们提出一种估计有监督分类任务难度与可迁移性的新方法。与以往工作不同，我们的方法与解决方案无关，不需要也不假设训练好的模型。我们用信息论方法估计这些值：把训练标签视为随机变量并探究其统计特性。在从源任务向目标任务迁移时，我们考虑两个此类变量（即两个任务的标签分配）之间的条件熵。我们解析与实证地表明该值与迁移模型的损失相关。我们进一步展示如何用该值估计任务难度。我们在三个大规模数据集——CelebA（40 个任务）、Animals with Attributes 2（85 个任务）与 Caltech-UCSD Birds 200（312 个任务）——上充分检验了我们的主张，共代表 437 个分类任务。我们提供的结果表明，难度与可迁移性估计与经验难度和可迁移性高度相关。作为案例研究，我们把学习到的人脸识别模型迁移到 CelebA 属性分类任务，对被估计为高可迁移性的任务展示了最先进精度。

**通过极端扰动与平滑掩码理解深度网络（Understanding Deep Networks via Extremal Perturbations and Smooth Masks）**
Ruth Fong、Mandela Patrick、Andrea Vedaldi
归因问题关注识别输入中对模型输出起作用的部分。一类重要的归因方法基于测量应用于输入的扰动效果。在本文中，我们讨论现有扰动分析方法的一些缺陷，并通过引入极端扰动（extremal perturbations）概念加以解决——它在理论上有根据且可解释。我们还引入若干计算极端扰动的技术创新，包括新的面积约束与平滑扰动的参数化族，使优化问题中的可调超参数全部消除。我们分析扰动面积与效果的关系，展示了对受激深度神经网络空间性质的出色敏感性。我们还将扰动分析扩展到网络的中间层，这一应用让我们能识别分类所需的显著通道，用特征反演可视化后可用于阐明模型行为。最后，我们介绍了基于 PyTorch 构建的可解释性库 TorchRay。

**在非筛选数据上无监督预训练图像特征（Unsupervised Pre-training of Image Features on Non-Curated Data）**
Mathilde Caron、Piotr Bojanowski、Julien Mairal、Armand Joulin
不依赖标注、用卷积神经网络预训练通用视觉特征，是一项富有挑战且重要的任务。近期无监督特征学习的工作大多聚焦于小型或高度筛选的数据集（如 ImageNet），而使用非筛选原始数据集被发现会在迁移任务评估时降低特征质量。我们的目标是弥合在筛选数据（获取成本高）上训练的无监督方法与轻易可得的海量原始数据集之间的性能差距。为此，我们提出一种新的无监督方法，结合自监督与聚类来捕捉大规模数据的互补统计信息。我们在 YFCC100M [44] 的 9600 万张图像上验证方法，在标准基准上取得无监督方法中的最先进结果，证实了只有非筛选原始数据可用时无监督学习的潜力。我们还表明，用我们的方法预训练有监督 VGG-16 可在 ImageNet 验证集上达到 74.9% 的 top-1 分类精度，比同一网络从头训练提高 0.8%。代码在此公开。

**用通道可分离卷积网络做视频分类（Video Classification with Channel Separable Convolutional Networks）**
Du Tran、Heng Wang、Lorenzo Torresani、Matt Feiszli
分组卷积已被证明在多种用于图像分类的 2D 卷积架构中节省大量计算。很自然的问题有：1）分组卷积能否缓解视频分类网络的高计算成本；2）3D 分组卷积网络中哪些因素最重要；3）3D 分组卷积网络有什么好的计算/精度权衡。本文研究了 3D 分组卷积网络在视频分类中不同设计选择的影响。我们实证表明，通道交互量对 3D 分组卷积网络的精度起重要作用。实验给出两个主要发现：第一，把 3D 卷积按分离通道交互与时空交互进行分解是好做法，能带来更高精度与更低计算成本；第二，3D 通道分离卷积提供了一种正则化，与 3D 卷积相比训练精度更低但测试精度更高。这两个实证发现引导我们设计了通道分离卷积网络（CSN）架构——简单高效而精确。在 Sports1M 与 Kinetics 上，我们的 CSN 与最先进水平相当或更优，同时效率高 2 到 3 倍。

**xR-EgoPose：从头显相机做自我中心 3D 人体姿态（xR-EgoPose: Egocentric 3D Human Pose from an HMD Camera）**
Denis Tome、Patrick Peluse、Lourdes Agapito、Hernan Badino
我们提出一个新的自我中心 3D 人体姿态估计方案，输入来自安装在头戴式虚拟现实设备边缘、朝下看的鱼眼相机的单目图像。这一不寻常的视角距用户面部仅 2 厘米，产生的图像具有独特的视觉外观：严重自遮挡与强透视畸变，导致下半身与上半身分辨率差异悬殊。我们的贡献有二。第一，我们提出一个新的编码器-解码器架构，带有专为应对 2D 关节位置不确定性的差异而设计的双分支解码器。我们在合成与真实数据集上的定量评估表明，该策略相较最先进的自我中心姿态估计方法带来大幅精度提升。第二个贡献是一个新的大规模逼真合成数据集 xR-EgoPose，提供 38.3 万帧高质量人物渲染，涵盖多样的肤色、体型与衣着，背景与光照条件多样，动作种类丰富。实验表明，新合成训练语料的高多样性带来对真实世界影像的良好泛化，并在带真值的真实数据集上取得最先进结果。此外，在 Human3.6M 基准上的评估表明，我们的方法在更经典的第三人称视角 3D 人体姿态问题上与表现顶尖的方法相当。

## ICCV 的其他活动

- 360° 感知与交互——Kristen Grauman（联合组织者）；Hanbyul Joo（讲者）
- 闭合视觉与语言之间的循环（CLVL）——Marcus Rohrbach（联合组织者）
- 面向时尚、艺术与设计的计算机视觉——Tamara Berg（讲者）；Kristen Grauman（指导委员会）
- CroMoL：真实世界中的跨模态学习——Lior Wolf（讲者）
- 野外伪装人脸（DFW）——Manohar Paluri（讲者）
- 自我中心感知、交互与计算（EPIC）——Kristen Grauman（联合组织者）
- 极端视觉建模——Vignesh Ramanathan、Dhruv Mahajan、Laurens van der Maaten、Alexander C. Berg、Ishan Misra（联合组织者）
- 面向 AR 与 VR 的眼动追踪——Sachin Talathi、Immo Schütz、Chen Jixu、Robert Cavin、Stephan Garbin（联合组织者）
- 几何遇上深度学习（GMDL）——Andrea Vedaldi（讲者）
- 解释与说明视觉人工智能模型——论文《Occlusions for Effective Data Augmentation in Image Classification》——Ruth Fong、Andrea Vedaldi
- COCO 与 Mapillary 联合识别研讨会：检测、关键点、全景与 DensePose 挑战赛——Larry Zitnick、Piotr Dollár、Ross Girshick（COCO 联盟）
- 大规模整体视频理解——Christoph Feichtenhofer（程序委员会）；Rohit Girdhar、Kristen Grauman、Manohar Paluri、Du Tran（讲者）
- 低功耗计算机视觉研讨会——Alexander C. Berg（联合组织者）
- 多模态视频分析与「时刻在时间」——Alexander C. Berg（联合组织者）
- Neural Architects——Ross Girshick（讲者）
- 场景图表示与学习——Devi Parikh、Laurens van der Maaten（讲者）
- 图像、视频与 3D 的视觉识别（教程）——Alexander Kirillov、Ross Girshick、Kaiming He、Georgia Gkioxari、Christoph Feichtenhofer、Saining Xie、Haoqi Fan、Yuxin Wu、Nikhila Ravi、Wan-Yen Lo、Piotr Dollár
- 医学图像的视觉识别——Kyunghyun Cho（联合组织者）；Adriana Romero（程序委员会）
- 预注册研讨会——Michela Paganini（讲者）
- YouTube-8M 大规模视频理解研讨会——Jitendra Malik（讲者）

## Everingham 奖

Facebook 人工智能研究院科学家 Tamara Berg 因自 2008 年创建以来生成并维护 Labeled Faces in the Wild（LFW）数据集与基准的工作，成为 2019 年度 PAMI Mark Everingham 奖得主。Everingham 奖授予为计算机视觉社区其他成员做出无私贡献、带来显著效益的研究者或研究团队。
