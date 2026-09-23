---
title: "Facebook 研究团队在 ECCV 2020"
title_en: "Facebook research at ECCV 2020"
date: 2020-08-21
source: https://ai.facebook.com/blog/facebook-research-at-eccv-2020
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 研究团队在 ECCV 2020

> 原文：[Facebook research at ECCV 2020](https://ai.facebook.com/blog/facebook-research-at-eccv-2020) · Meta AI（Wayback 存档）

2020 年 8 月 21 日

Facebook 的研究员还将在整个会议期间组织和参与线上教程与研讨会。「OpenEyes：AR、VR 与野外中的眼动注视」研讨会由 Facebook Reality Labs 研究员与该领域其他学者合作组织。Facebook AI 研究院还组织了「图像、视频与 3D 的视觉识别」教程，讨论不同输入模态视觉识别任务的进展与方法。在与 ECCV 联合举办的手语识别、翻译与生成研讨会上，我们还将展示 How2Sign——一个包含 80 小时美国手语打签视频并附带标注的多模态数据集。自动手语识别、生成与翻译领域的进展一直受制于缺乏大型标注数据集，尤其是按句子或话语级标注和切分的连续手语数据集。我们希望 How2Sign 能加速该领域的研究。关于 Facebook 今年 8 月 23 日至 28 日在 ECCV 的更多活动信息，请查看 Facebook at ECCV 页面。

## Facebook 在 ECCV 2020 上展示的研究

**度量学习现实检验（A Metric Learning Reality Check）**
Kevin Musgrave、Serge Belongie、Ser-Nam Lim
过去四年的深度度量学习论文不断声称精度大幅提升，往往比十年前的方法性能翻倍以上。在本文中，我们更仔细地审视该领域，看这是否属实。我们发现了这些论文实验设置中的缺陷，并提出评估度量学习算法的新方法。最后，我们给出的实验结果表明，随时间的改进充其量只是边缘性的。

**对抗持续学习（Adversarial continual learning）**
Sayna Ebrahimi、Franziska Meier、Roberto Calandra、Trevor Darrell、Marcus Rohrbach
持续学习旨在学习新任务而不遗忘已学任务。我们假设为解决序列中每个任务而学到的表示既有共享结构，又包含一些任务特有属性。我们表明共享特征显著更不易遗忘，并提出一个新颖的混合持续学习框架，为解决一系列任务所需的任务不变特征与任务特定特征学习互不相交的表示。我们的模型结合架构增长（防止任务特定技能遗忘）与经验回放（保留共享技能）。我们证明该混合方法能有效避免遗忘，并在单数据集类别增量学习以及图像分类的多个数据集序列上优于基于架构与基于记忆的方法。代码在此公开。

**在空间与时间上对齐视频（Aligning videos in space and time）**
Senthil Purushwalkam、Tian Ye、Saurabh Gupta、Abhinav Gupta
在本文中，我们聚焦跨视频提取视觉对应的任务。给定来自某个动作类别的查询视频片段，我们的目标是在空间与时间上将其与训练视频对齐。为这种细粒度对齐任务获取训练数据既困难又常有歧义。因此，我们提出一种新颖的对齐流程，通过跨视频循环一致性学习空间与时间上的对应。训练时，给定一对视频，我们计算这样的循环：把第一个视频中某帧的图像块通过在第二个视频各帧中的匹配连接起来。连接重叠图像块的循环被鼓励获得比连接非重叠图像块的循环更高的分数。我们在 Penn Action 与 Pouring 数据集上的实验表明，所提方法能成功学习跨视频对应语义相似的图像块，并学到对物体与动作状态敏感的表示。

**神经架构搜索中标签是否必要？（Are labels necessary in neural architecture search?）**
Chenxi Liu、Piotr Dollar、Kaiming He、Ross Girshick、Alan Yuille、Saining Xie
计算机视觉中现有的神经网络架构——无论由人还是由机器设计——通常都是同时使用图像及其关联标签找到的。在本文中，我们提出一个问题：能否只使用图像而不用人工标注标签，找到高质量的神经架构？为回答这个问题，我们首先定义了一个名为无监督神经架构搜索（UnNAS）的新设置，然后进行两组实验。在基于采样的实验中，我们用有监督或无监督目标训练大量（500 个）多样架构，发现有标签与无标签产生的架构排名高度相关。在基于搜索的实验中，我们用多种无监督目标运行成熟的 NAS 算法（DARTS），报告无标签搜索出的架构可以与有标签搜索的对应架构竞争。综合来看，这些结果揭示了一个可能令人惊讶的发现：标签并非必要，仅图像统计量就可能足以识别好的神经架构。

**基于注意力的查询扩展学习（Attention-based query expansion learning）**
Albert Gordo、Filip Radenovic、Tamara Berg
查询扩展是图像搜索中广泛使用的技术，把原始查询中排名靠前的图像组合成扩展查询再重新发出，通常能提升召回率与精度。查询扩展的一个重要方面是选择合适的方式把图像组合成新查询。有趣的是，尽管查询扩展的实证成功毋庸置疑，占据主导地位的仍是带有各种缺陷的临时方法，关于如何「学习」查询扩展的研究并不多。在本文中，我们为查询扩展提出一个更有原则的框架：以判别方式训练一个模型，学习图像应如何聚合以形成扩展查询。在该框架内，我们提出一个利用自注意力机制的模型，在聚合之前有效学习在不同图像之间传递信息。我们的方法在标准基准上获得比现有方法更高的精度。更重要的是，我们的方法是唯一在不同情形下都持续保持高精度的方法，克服了现有方法的缺陷。

**超越导航图：连续环境中的视觉与语言导航（Beyond the nav-graph: Vision-and-language navigation in continuous environments）**
Jacob Krantz、Erik Wijmans、Arjun Majumdar、Dhruv Batra、Stefan Lee
我们开发了一个设定在连续 3D 环境中的语言引导导航任务，智能体必须执行低层动作来遵循自然语言导航指令。通过置身连续环境，这一设定消除了先前工作中把环境表示为稀疏全景图（边对应可通行性）所隐含的若干假设。具体而言，我们的设定去除了已知环境拓扑、短程 oracle 导航以及完美智能体定位这三个前提。为给这一新任务定位，我们开发了反映此前设定中许多进展的模型以及单模态基线。虽然有些迁移有效，我们发现在连续设定下的绝对性能显著更低——这表明此前「导航图」设定中的性能可能被强隐含假设抬高了。代码见 jacobkrantz.github.io/vlnce。

**通过时间偏移小波变换做连拍去噪（Burst denoising via temporally shifted wavelet transforms）**
Denis Demandoix、Kevin Matzen、Priyam Chatterjee、Xuejian Rong、Yingli Tian
移动摄影近年来进步巨大，但低光成像仍是挑战。长曝光可以改善信噪比（SNR），但拍摄动态场景时会产生不希望的运动模糊。因此，成像流水线常依赖计算摄影，通过融合多次短曝光提升 SNR。近来基于深度神经网络的方法已能通过精细融合这些曝光生成视觉上赏心悦目的结果，但计算成本往往更高。我们提出一个端到端可训练的连拍去噪流水线，联合捕捉源自小波变换的高分辨率与高频深度特征。在我们的模型中，宝贵的高频子带特征保留了局部细节以增强最终感知质量，低频子带特征承载结构信息以忠实重建并保证最终客观质量。该模型通过时间特征偏移支持可变长度连拍捕捉，计算开销仅略有增加。最后，我们用真实噪声模型训练模型以泛化到真实环境。凭借这些技术，我们的方法在感知质量上达到最先进水平，同时快一个数量级。

**ContactPose：带物体接触与手部姿态的抓握数据集（ContactPose: A dataset of grasps with object contact and hand pose）**
Samarth Brahmbhatt、Chengcheng Tang、Christopher D. Twigg、Charles C. Kemp、James Hays
抓握对人类而言很自然。然而它涉及复杂的手部构型与软组织变形，可能在手与物体之间产生复杂的接触区域。理解并建模这种接触有望改进手部模型、AR/VR 体验和机器人抓取。但我们目前缺乏手-物接触与其他数据模态配对的数据集，而这对于开发和评估接触建模技术至关重要。我们引入 ContactPose——首个把手-物接触与手部姿态、物体姿态及 RGB-D 图像配对的数据集。ContactPose 包含 50 名参与者以 2 种功能意图抓握 25 种家居物体的 2306 个独特抓握，以及超过 290 万张 RGB-D 抓握图像。对 ContactPose 数据的分析揭示了手部姿态与接触之间的有趣关系。我们用这些数据严格评估了各种数据表示、文献中的启发式方法以及接触建模的学习方法。数据、代码与训练模型见 https://contactpose.cc.gatech.edu。

**多源域适配中源选择的课程管理器（Curriculum Manager for Source Selection in Multi-Source Domain Adaptation）**
Luyu Yang、Yogesh Balaji、Ser-Nam Lim、Abhinav Shrivastava
多源无监督域适配的性能在很大程度上取决于从有标注源域样本迁移的有效性。在本文中，我们提出一个为源样本学习动态课程的对抗智能体，称为源选择课程管理器（CMSS）。课程管理器是一个独立网络模块，在训练期间不断更新课程，迭代学习哪些域或样本最适合与目标域对齐。其背后的直觉是迫使课程管理器不断重新度量潜在域随时间变化的可迁移性，以对抗性地提高域判别器的错误率。CMSS 不需要任何域标签知识，却在四个知名基准上大幅胜过其他方法。我们还提供了可解释的结果，阐明所提方法的原理。

**深度局部形状：为精细 3D 重建学习局部 SDF 先验（Deep Local Shapes: Learning local SDF priors for detailed 3D reconstruction）**
Roham Chabra、Jan E. Lenssen、Eddy Ilg、Tanner Schmidt、Julian Straub、Steven Lovegrove、Richard Newcombe
高效地大规模重建复杂精细的表面，是机器感知的长期目标。为解决这一问题，我们引入深度局部形状（DeepLS）——一种深度形状表示，能够在没有过高内存需求的情况下编码和重建高质量 3D 形状。DeepLS 用一组由神经网络定义的局部学习的连续 SDF，取代传统表面重建系统中使用的稠密体积符号距离函数（SDF）表示，灵感来自 DeepSDF 等近期工作。与用神经网络加单一潜在码表示物体级 SDF 的 DeepSDF 不同，我们存储一个独立潜在码网格，每个码负责存储小局部邻域中表面的信息。把场景分解为局部形状简化了网络必须学习的先验分布，也使推断高效。我们通过物体形状编码与完整场景重建展示了 DeepLS 的有效性与泛化能力，它带来了高压缩率、高精度与局部形状补全。

**DeepHandMesh：用于高保真手部网格建模的弱监督深度编解码框架（DeepHandMesh: Weakly supervised deep encoder and decoder framework for high-fidelity hand mesh modeling）**
Gyeongsik Moon、Takaaki Shiratori、Kyoung Mu Lee
人手在与他人和物体交互中扮演核心角色。要逼真地复现这类手部动作，必须重建高保真的手部网格。在本研究中，我们首次提出 DeepHandMesh——一个用于高保真手部网格建模的弱监督深度编解码框架。我们的系统设计为端到端弱监督训练，因此不需要真值网格。它依赖较弱的监督，如 3D 关节坐标与多视角深度图——它们比真值网格更易获取且不依赖网格拓扑。尽管 DeepHandMesh 以弱监督方式训练，它比以往全监督手部模型提供了逼真得多的手部网格。我们新引入的穿透避免损失通过复现手部部件间的物理交互进一步改进结果。最后，我们证明该系统也能成功应用于从一般图像做 3D 手部网格估计。我们的手部模型、数据集与代码已公开。

**用于高效点云生成的离散点流网络（Discrete point flow networks for efficient point cloud generation）**
Roman Klokov、Edmond Boyer、Jakob Verbeek
生成模型已被证明能有效建模 3D 形状及其统计变化。在本文中，我们研究其在点云上的应用——点云是计算机视觉中广泛使用的 3D 形状表示，但迄今提出的生成模型很少。我们引入一个基于带仿射耦合层的归一化流的隐变量模型，在给定潜在形状表示的情况下生成任意规模的 3D 点云。为评估其对形状建模的益处，我们把该模型应用于生成、自编码与单视图形状重建任务。在评估生成与自编码的大多数指标上，我们改进了近期基于 GAN 的模型。与近期基于连续流的工作相比，我们的模型在性能相似或更好的情况下，训练与推断时间都显著加速。在单视图形状重建上，我们也取得了与最先进的体素、点云与网格方法相当的结果。

**用 transformer 做端到端目标检测（End-to-end object detection with transformers）**
Nicolas Carion、Francisco Massa、Gabriel Synnaeve、Nicolas Usunier、Alexander Kirillov、Sergey Zagoruyko
我们提出一种把目标检测视为直接集合预测问题的新方法。我们的方法简化了检测流水线，有效去除了许多手工设计组件的需求，如非极大值抑制流程或显式编码任务先验知识的锚框生成。这个名为 DEtection TRansformer（DETR）的新框架的主要成分是：一个通过二部匹配强制唯一预测的基于集合的全局损失，以及一个 transformer 编码器-解码器架构。给定一小组固定的已学习目标查询，DETR 推理目标之间的关系与全局图像上下文，并行直接输出最终预测集合。新模型在概念上很简单，与许多其他现代检测器不同，不需要专用库。在富有挑战的 COCO 目标检测数据集上，DETR 展示了与成熟且高度优化的 Faster RCNN 基线相当的精度与运行时间。此外，DETR 可以轻松泛化，以统一方式产生全景分割。我们表明它显著胜过有竞争力的基线。训练代码与预训练模型在此公开。

**用模块化编解码化身实现富有表现力的远程呈现（Expressive telepresence via Modular Codec Avatars）**
Hang Chu、Shugao Ma、Fernando De la Torre、Sanja Fidler、Yaser Sheikh
VR 远程呈现指在以化身表示的虚拟空间中与另一个人交互。如今大多数化身是卡通式的，但很快技术将允许视频级逼真的化身。本文正是朝这一方向努力，提出模块化编解码化身（MCA）——一种由 VR 头显中的相机驱动的超逼真人脸生成方法。MCA 用学习到的模块化表示取代整体模型，扩展了传统的编解码化身（CA）。值得注意的是，传统面向特定人的 CA 从少量训练样本学习，通常缺乏鲁棒性，迁移面部表情的表现力也有限。MCA 通过学习面部不同组件的调制自适应混合以及基于样例的潜在对齐解决了这些问题。我们证明 MCA 在多种真实数据集与实际场景中相较 CA 取得了更好的表现力与鲁棒性。最后，我们展示了所提模型支持的 VR 远程呈现新应用。

**SF-Net：用于时序动作定位的单帧监督（SF-Net: Single-frame supervision for temporal action localization）**
Fan Ma、Linchao Zhu、Yi Yang、Shengxin Zha、Gourab Kundu、Matt Feiszli、Zheng Shou
在本文中，我们研究时序动作定位（TAL）的一种中间监督形式——单帧监督。为获得单帧监督，标注者只需在动作的时间窗口内识别一帧。这可以显著降低获取全监督（需标注动作边界）的人力成本。与只标注视频级标签的弱监督相比，单帧监督在保持低标注开销的同时引入了额外的时间动作信号。为充分利用这种单帧监督，我们提出统一系统 SF-Net。首先，我们提议为每个视频帧预测一个动作性（actionness）分数。与典型的类别分数一起，动作性分数可以提供关于潜在动作发生的全面信息，并在推断时辅助时间边界精化。其次，我们基于单帧标注挖掘伪动作帧与背景帧：通过自适应地把每个标注单帧扩展到其邻近的上下文帧来识别伪动作帧，并从多个视频的所有未标注帧中挖掘伪背景帧。这些伪标注帧与真值标注帧一起进一步用于训练分类器。在 THUMOS14、GTEA 和 BEOID 上的大量实验中，SF-Net 在片段定位与单帧定位两方面都显著超越了最先进的弱监督方法。值得注意的是，SF-Net 取得了与需要更耗资源标注的全监督对应方法相当的结果。代码见 https://github.com/Flowerfan/SF-Net。

**几何对应场：野外 3D 姿态精化的学习型可微渲染（Geometric correspondence fields: Learned differentiable rendering for 3D pose refinement in the wild）**
Alexander Grabner、Yaming Wang、Peizhao Zhang、Peihong Guo、Tong Xiao、Peter Vajda、Peter M. Roth、Vincent Lepetit
我们提出一种基于可微渲染的野外任意类别物体 3D 姿态精化新方法。与以往方法相比，我们有两项主要贡献：第一，我们不在 RGB 或掩码空间比较真实图像与合成渲染，而是在为 3D 姿态精化优化的特征空间中比较；第二，我们引入一个新的可微渲染器，它从数据中学习近似光栅化的反向传播，而非依赖手工设计的算法。为此，我们以所谓几何对应场的形式预测 RGB 图像与 3D 模型渲染之间的深度跨域对应。这些对应场作为像素级梯度，经解析地沿渲染流水线反向传播，直接对 3D 姿态执行基于梯度的优化。这样，我们把 3D 模型精确对齐到 RGB 图像中的物体，带来显著改进的 3D 姿态估计。我们在富有挑战的 Pix3D 数据集上评估方法，在多项指标上比最先进精化方法最高提升 55%。

**基础数据集设计对少样本图像分类的影响（Impact of base dataset design on few-shot image classification）**
Markus Hofinger、Samuel Rota Bulò、Lorenzo Porzi、Arno Knapitsch、Thomas Pock、Peter Kontschieder
深度图像特征的质量与通用性关键取决于其训练数据，但这一常被忽视的影响鲜有研究。在本文中，我们通过在少样本分类设置中评估在不同图像集上训练的深度特征，系统研究训练数据变化的影响。我们定义的实验协议可以探索关键的实际问题：基础类与测试类的相似性有何影响？在固定标注预算下，每类图像数与类别数之间的最优权衡是什么？给定固定数据集，拆分或合并不同类别能否改进特征？应标注简单的还是多样的类别？在大量实验中，我们在 miniImageNet、ImageNet 和 CUB-200 基准上给出了这些问题的明确答案。我们还表明，基础数据集设计对少样本分类性能的提升，可以比用先进的最先进算法替换简单基线更显著。

**在金字塔层级上改进光流（Improving optical flow on a pyramid level）**
Markus Hofinger、Samuel Rota Bulò、Lorenzo Porzi、Arno Knapitsch、Thomas Pock、Peter Kontschieder
在本工作中，我们审视由粗到细的空间特征金字塔概念——它被最先进的光流估计网络用来使像素流搜索空间的探索在计算上可行且高效。在单个金字塔层级内，我们通过从基于变形的策略转向基于采样的策略改进代价体构建过程，避免重影，从而更好地保留细微流细节。我们进一步通过层级特定的损失最大化池化策略放大这些正面效果，自适应地把学习过程的焦点转移到表现不佳的预测上。我们的第二项贡献修正了跨金字塔层级的梯度流。每个金字塔层级执行的典型操作可能产生跨层级的噪声甚至相互矛盾的梯度。我们展示并讨论了如何适当阻断其中一些梯度分量以改进收敛并最终提升性能。最后，我们引入蒸馏概念来对抗微调期间的灾难性遗忘，从而在按序训练于多个数据集的模型间保留知识。我们的发现概念简单且易于实现，却在相关误差指标上带来可观改进，并通过 Flying Chairs2、Flying Things、Sintel 和 KITTI 等数据集的详尽消融加以证明。我们在富有挑战的 Sintel 与 KITTI 2012 测试集上刷新了最先进结果，还展示了这些发现可移植到不同的光流与双目深度方法。

**用网络图文对改进视觉与语言导航（Improving Vision-and-Language Navigation with web image-text pairs）**
Arjun Majumbar、Ayush Shrivastava、Stefan Lee、Peter Anderson、Devi Parikh、Dhruv Batra
遵循「走下楼梯并在棕色沙发处停下」这样的导航指令，要求具身 AI 智能体把被指称的场景元素（如「楼梯」）落地到环境中的视觉内容（对应「楼梯」的像素）。我们提出如下问题：能否利用丰富的「非具身」网络抓取视觉与语言语料（如 Conceptual Captions）来学习视觉落地，以改进相对缺乏数据的具身感知任务（视觉与语言导航）？具体而言，我们开发了 VLN-BERT——一个视觉语言 transformer 模型，用于给指令（「……在棕色沙发处停下」）与智能体捕捉的全景 RGB 图像轨迹之间的兼容性打分。我们证明，先在网络图文对上预训练 VLN-BERT，再在具身路径-指令数据上微调，能显著提升 VLN 性能——在完全可观测设置下成功率比先前最先进水平高出 4 个绝对百分点。对预训练课程的消融显示每个阶段都有效——组合后增益更大。

**InterHand2.6M：面向单张 RGB 图像 3D 单手与交互手姿态估计的新大规模数据集与基线（InterHand2.6M: A new large-scale dataset and baseline for 3D single and interacting hand pose estimation from a single RGB image）**
Gyeongsik Moon、Shoou-I Yu、He Wen、Takaaki Shiratori、Kyoung Mu Lee
手-手交互分析是更好理解人类行为的关键一步。但 3D 手部姿态估计的大多数研究聚焦于孤立单手情形。因此，我们首先提出（1）大规模数据集 InterHand2.6M，以及（2）用于从单张 RGB 图像做 3D 交互手姿态估计的基线网络 InterNet。所提 InterHand2.6M 包含多名受试者各种姿态下的 260 万帧标注的单手与交互手图像。我们的 InterNet 同时执行 3D 单手与交互手姿态估计。实验中，我们展示了利用 InterHand2.6M 中的交互手数据后，3D 交互手姿态估计精度大幅提升。我们还报告了 InterNet 在 InterHand2.6M 上的精度，作为该新数据集的强基线。最后，我们展示了从一般图像做 3D 交互手姿态估计的结果。代码与数据集已公开。

**面向视觉对话的大规模预训练：一个简单的最先进基线（Large-scale pretraining for visual dialog: A simple state-of-the-art baseline）**
Vishvak Murahari、Dhruv Batra、Devi Parikh、Abhishek Das
以往的视觉对话工作聚焦于孤立地在 VisDial 上训练深度神经模型。与此不同，我们提出一种先在相关视觉-语言数据集上预训练、再迁移到视觉对话的方法。我们改造近期提出的 ViLBERT 模型以适应多轮视觉落地对话。我们的模型在 Conceptual Captions 与视觉问答数据集上预训练，并在 VisDial 上微调。我们的最佳单模型在 NDCG 与 MRR 上比此前发表工作高出 1 个百分点以上（绝对值）。接着，我们发现用 VisDial 的「稠密」标注做额外微调会带来更高的 NDCG——比基础模型高 10 个百分点以上——但损害 MRR——比基础模型低 17 个百分点以上！这凸显了两大主要指标 NDCG 与 MRR 之间的权衡，我们发现原因在于稠密标注与问题的原始真值答案相关性不佳。

**学习生成落地的视觉描述而无需定位监督（Learning to generate grounded visual captions without localization supervision）**
Chih-Yao Ma、Yannis Kalantidis、Ghassan AlRegib、Peter Vajda、Marcus Rohrbach、Zsolt Kira
在为图像或视频自动生成句描述时，生成的描述落地程度如何往往不清楚：模型是使用了正确的图像区域来输出特定词语，还是基于数据集和/或语言模型中的先验「产生幻觉」？描述模型中把图像区域与词语关联的最常见方式是对作为预测下一词输入的区域施加注意力机制。因此，模型必须在不知道应定位哪个词的情况下学会预测注意力权重。在没有落地监督的情况下这很难训练，因为循环模型会传播过去的信息，且没有显式信号强制描述模型恰当地落地每个解码的词。在本工作中，我们通过新颖的循环训练方案帮助模型实现这一点：在句子解码器生成每个词后，强制模型在图像中定位该词，然后从定位到的图像区域重建句子以匹配真值。我们提出的框架只需学习一个额外的全连接层（定位器），该层在测试时可移除。我们表明，无论图像还是视频描述任务，我们的模型都在不依赖落地监督、不增加推断期计算的情况下显著提升了落地精度。代码在此公开。

**制作隐身斗篷：针对目标检测器的现实世界对抗攻击（Making an invisibility cloak: Real world adversarial attacks on object detectors）**
Zuxuan Wu、Ser-Nam Lim、Larry S. Davis、Tom Goldstein
我们对最先进目标检测框架上对抗攻击的可迁移性进行了系统研究。使用标准检测数据集，我们训练出能抑制一系列常用检测器及检测器集成所产生的物体性（objectness）分数的图案。通过大量实验，我们在白盒与黑盒设置下对对抗训练的补丁效果进行基准测试，并量化攻击在数据集、物体类别与检测器模型之间的可迁移性。最后，我们对使用印刷海报与可穿戴衣物的物理世界攻击进行了详细研究，并用不同指标严格量化此类攻击的性能。

**Mapillary 行星级深度数据集（Mapillary planet-scale depth dataset）**
Manuel Lopez-Antequera、Pau Gargallo、Markus Hofinger、Samuel Rota Bulò、Yubin Kuang、Peter Kontschieder
基于学习的方法在成熟基准上训练时，在单图像深度任务上产生了出色的结果，但从这些基准到真实世界性能之间有很大差距，且这一差距常被在目标数据集上微调的常见做法掩盖。我们引入一个新的深度数据集，规模比以往数据集大一个数量级，更重要的是涵盖了前所未有的地点、相机型号与场景类型，并提供度量深度（而非仅相对尺度）。此外，我们研究了用许多不同相机拍摄的图像训练单图像深度网络的问题，验证了一种现有方法并提出了一个更简单的替代方案。凭借我们的贡献，我们在微调前就在富有挑战的基准上取得了出色结果，并在微调后刷新了流行的 KITTI 数据集的最先进水平。数据集见 mapillary.com/dataset/depth。

**Mask TextSpotter v3：面向鲁棒场景文本识别的分割建议网络（Mask TextSpotter v3: Segmentation proposal network for robust scene text spotting）**
Minghui Liao、Guan Pang、Jing Huang、Tal Hassner、Xiang Bai
近来集成检测与识别的端到端可训练场景文本识别方法进展颇多。但当前大多数任意形状场景文本识别器使用区域建议网络（RPN）产生建议。RPN 严重依赖手工设计的锚框，其建议用轴对齐矩形表示。前者在处理极端长宽比或不规则形状的文本实例时存在困难，后者在密集排布文本情形下常把多个相邻实例包含进单个建议。为解决这些问题，我们提出 Mask TextSpotter v3——一个采用分割建议网络（SPN）替代 RPN 的端到端可训练场景文本识别器。我们的 SPN 免锚框且能给出任意形状建议的精确表示，因此在检测极端长宽比或不规则形状文本实例时优于 RPN。此外，SPN 产生的精确建议允许使用掩码 RoI 特征解耦相邻文本实例。因此，Mask TextSpotter v3 能处理极端长宽比或不规则形状的文本实例，其识别精度不受邻近文本或背景噪声影响。具体而言，我们在 Rotated ICDAR 2013 数据集（旋转鲁棒性）上超过最先进方法 21.9%，在 Total-Text 数据集（形状鲁棒性）上超过 5.9%，并在 MSRA-TD500 数据集（长宽比鲁棒性）上取得最先进性能。

**面向高效导航的占用预测（Occupancy anticipation for efficient navigation）**
Santhosh K. Ramakrishnan、Ziad Al-Halah、Kristen Grauman
最先进的导航方法利用空间记忆来泛化到新环境，但其占用图仅限于捕捉智能体直接观察到的几何结构。我们提出占用预测：智能体利用其自我中心 RGB-D 观测推断可见区域之外的占用状态。这样，智能体能更快建立空间感知，从而在 3D 环境中高效探索与导航。通过利用自我中心视图与俯视图中的上下文，我们的模型成功预测出更宽的环境地图，性能显著优于强基线。此外，在部署到探索与导航这类序列决策任务时，我们的模型在 Gibson 与 Matterport3D 数据集上胜过最先进方法。我们的方法是 2020 年 Habitat PointNav 挑战赛的获胜方案。项目页面：http://vision.cs.utexas.edu/projects/occupancy_anticipation/。

**PatchNets：基于块的通用深度隐式 3D 形状表示（PatchNets: Patch-based generalizable DeepImplicit 3D shape representations）**
Edgar Tretschk、Ayush Tewari、Vladislav Golyanik、Michal Zollhoffer、Carsten Stoll、Christian Theobalt
符号距离函数等隐式表面表示与深度学习相结合，产生了能表示任意拓扑物体精细形状的出色模型。由于学习的是连续函数，重建可以以任意分辨率提取。但训练这类模型需要 ShapeNet 等大型数据集。在本文中，我们提出一种新的中层基于块的表面表示。在块的层面，不同类别的物体具有相似性，这带来更通用的模型。接着我们引入一种新颖方法，在规范空间中学习这种基于块的表示，使其尽可能与物体无关。我们表明，在 ShapeNet 一个类别上训练的表示也能很好地表示任何其他类别的精细形状。此外，与现有方法相比，它可以用少得多的形状训练。我们展示了新表示的多种应用，包括形状插值与部分点云补全。由于对块的位置、朝向与尺度有显式控制，我们的表示也比物体级表示更可控，使我们能对编码的形状做非刚性变形。见补充材料。

**从野外单张图像感知 3D 人-物空间布局（Perceiving 3D human-object spatial arrangements from a single image in the wild）**
Jason Y. Zhang、Sam Pepose、Hanbyul Joo、Deva Ramanan、Jitendra Malik、Angjoo Kanazawa
我们提出一种方法，从在不受控环境中拍摄的野外单张图像，推断全局一致的 3D 场景中人与物体的空间布局与形状。值得注意的是，我们的方法无需任何场景或物体级 3D 监督即可在数据集上运行。我们的关键洞察是：把人与物体联合考虑会产生可用于消解歧义的「3D 常识」约束。具体而言，我们引入了从数据学习物体尺寸分布的尺度损失、优化物体姿态的遮挡感知轮廓重投影损失，以及捕捉与人交互物体空间布局的人-物交互损失。我们实证验证了这些约束大幅缩小了可能的 3D 空间构型空间。我们在人与大物体（如自行车、摩托车、冲浪板）及手持物体（如笔记本电脑、网球拍、滑板）交互的富有挑战野外图像上展示了方法。我们量化了方法恢复人-物布局的能力，并概述了这一相对未探索领域的剩余挑战。项目网页见 https://jasonyzhang.com/phosa。

**PointContrast：面向 3D 点云理解的无监督预训练（PointContrast: Unsupervised pre-training for 3D point cloud understanding）**
Saining Xie、Jiatao Gu、Demi Guo、Or Litany、Charles R. Qi、Leonidas Guibas
可以说，深度学习最成功的案例之一是迁移学习。在富集源集（如 ImageNet）上预训练网络、再在通常小得多的目标集上微调可以提升性能——这一发现对语言与视觉的许多应用至关重要。但其在 3D 点云理解中的效用鲜有研究。考虑到 3D 数据标注所需的工作量，我们认为这是一个机会。在本工作中，我们旨在促进 3D 表示学习研究。与以往工作不同，我们聚焦高层场景理解任务。为此，我们选择一组多样的数据集与任务，衡量无监督预训练在大型 3D 场景源集上的效果。我们的发现极为鼓舞人心：使用统一的架构、源数据集与对比损失三元组进行预训练，我们在室内室外、真实合成数据集的六个不同基准上的分割与检测都取得了超越近期最佳结果的改进——表明学到的表示能跨域泛化。此外，改进幅度与有监督预训练相当，这提示未来工作应更倾向于扩大数据收集而非更精细的标注。我们希望这些发现能鼓励更多面向 3D 深度学习的无监督前置任务设计研究。

**基于建议的视频补全（Proposal-based video completion）**
Yuan-Ting Hu、Heng Wang、Nicolas Ballas、Kristen Grauman、Alexander Schwing
视频补绘是从视频内容编辑到视频修复等各种应用的重要技术。早期方法遵循图像补绘范式，但受复杂相机运动与非刚性变形的挑战。为应对这些挑战，人们提出了流引导传播技术。然而，对未观测区域计算光流并非易事，且跨整个视频序列传播的计算需求很高。与之相反，本文提出基于建议的视频补绘算法：我们用 3D 卷积获得初始补绘估计，随后通过融合一组生成的建议加以精化。与现有的视频补绘方法不同，并受目标检测中已被充分探索的机制启发，我们论证建议提供了丰富的信息源，允许组合在空间与时间上可能远离待补绘区域但外观相似的图像块。我们在富有挑战的 YouTube VOS 与 DAVIS 数据集上用不同设置验证了方法的有效性，并展示在标准指标上超越最先进水平的结果。

**量化引导的 JPEG 伪影校正（Quantization guided JPEG artifact correction）**
Max Ehrlich、Larry Davis、Ser-Nam Lim、Abhinav Shrivastava
JPEG 图像压缩算法因其高压缩比能力成为最流行的图像压缩方法。但为实现高压缩，信息会丢失。在激进量化设置下，这导致图像质量明显下降。伪影校正在深度神经网络语境下已被研究一段时间，但当前提供最先进结果的方法需要为每种质量设置训练不同模型，极大限制了其实际应用。我们通过创建以 JPEG 文件量化矩阵为参数的新颖架构解决了这一问题。这使我们的单一模型能达到专为特定质量设置训练的模型的最先进性能。

**看见未见之景：为房间导航学习超越模态的语义地图（Seeing the un-Scene: Learning amodal semantic maps for room navigation）**
Medhini Narasimhan、Erik Wijmans、Xinlei Chen、Trevor Darrell、Dhruv Batra、Devi Parikh、Amanpreet Singh
我们引入一种使用语义地图的基于学习的房间导航方法。我们提出的架构学会预测智能体视野之外区域的自上而下信念图，同时建模房屋的建筑与风格规律。首先，我们训练一个模型生成超越模态的语义自上而下地图，通过学习房屋的底层建筑模式指示房间的位置、大小与形状信念。接着，我们用这些地图预测目标房间内的一个点，并训练一个策略导航到该点。我们实证表明，通过预测语义地图，模型学到了房屋中的常见相关性并泛化到新环境。我们还表明，把房间导航简化为点导航可进一步提升性能。我们将公开代码，希望这项工作为该领域的进一步研究铺路。

**SOLAR：面向图像检索的二阶损失与注意力（SOLAR: Second-order loss and attention for image retrieval）**
Tony Ng、Vassileios Balntas、Yurun Tian、Krystian Mikolajczyk
深度学习的近期工作表明，二阶信息在许多计算机视觉相关任务中是有益的。二阶信息可以在空间上下文与抽象特征维度上同时施加。在本工作中，我们探索两个二阶组件。一个聚焦二阶空间信息以提升图像描述子（局部与全局）的性能。更具体地说，它用于重新加权特征图，从而突出显著的图像位置，随后用于描述。第二个组件关注二阶相似度（SOS）损失，我们将其扩展到图像检索的全局描述子，用于结合难负例挖掘增强三元组损失。我们在图像检索与图像匹配的两个不同任务与数据集上验证了方法。结果表明两个二阶组件相辅相成，为两个任务带来显著性能提升，并在基准上取得最先进结果。代码见 http://github.com/tonyngjichun/SOLAR。

**SoundSpaces：视听具身导航（SoundSpaces: Audio-visual embodied navigation）**
Changan Chen、Unnat Jain、Carl Schissler、Sebastia Vicenc Amengual Gari、Ziad Al-Halah、Vamsi Krishna Ithapu、Philip Robinson、Kristen Grauman
在世界中移动天然是多感官体验，但如今的具身智能体却是「聋的」——仅限于对环境的视觉感知。我们为声学与视觉都逼真的复杂 3D 环境引入视听导航。通过同时看与听，智能体必须学会导航到发声物体。我们提出多模态深度强化学习方法，从自我中心视听观测流端到端训练导航策略，使智能体能够（1）发现混响音频所指示的物理空间几何要素，（2）检测并跟随发声目标。我们进一步引入 SoundSpaces——首个基于几何声学仿真的音频渲染数据集，覆盖两组公开 3D 环境（Matterport3D 与 Replica），并为 Habitat 提供新传感器支持，使在一批真实扫描环境中插入任意声源成为可能。结果表明音频极大地有益于 3D 空间中的具身视觉导航，我们的工作为带视听感知的具身 AI 新研究奠定了基础。项目：http://vision.cs.utexas.edu/projects/audio_visual_navigation。

**面向 TextVQA 的空间感知多模态 transformer（Spatially aware multimodal transformers for TextVQA）**
Yash Kant、Dhruv Batra、Peter Anderson、Alexander Schwing、Devi Parikh、Jiasen Lu、Harsh Agrawal
文字线索对日常任务（如买杂货、乘坐公共交通）至关重要。为开发这类辅助技术，我们研究 TextVQA 任务：推理图像中的文字来回答问题。现有方法在使用空间关系上受限，依赖全连接的 transformer 架构隐式学习场景的空间结构。与之相反，我们提出新颖的空间感知自注意力层，使每个视觉实体只关注由空间图定义的相邻实体。此外，多头自注意力层的每个头聚焦不同的关系子集。我们的方法有两个优势：（1）每个头考虑局部上下文，而非把注意力分散到所有视觉实体；（2）我们避免学习冗余特征。我们表明，模型在改进基线之上把当前最先进方法在 TextVQA 上的绝对精度总体提升 2.2%，在涉及空间推理且可用 OCR token 正确回答的问题上提升 4.62%。类似地，在 ST-VQA 上我们把绝对精度提升 4.2%。我们进一步表明空间感知自注意力改进了视觉落地。

**SqueezeSegV3：面向高效点云分割的空间自适应卷积（SqueezeSegV3: Spatially adaptive convolution for efficient point-cloud segmentation）**
Chenfeng Xu、Bichen Wu、Zining Wang、Wei Zhan、Peter Vajda、Kurt Keutzer、Masayoshi Tomizuka
LiDAR 点云分割是许多应用的重要问题。对大规模点云分割，事实方法是把 3D 点云投影得到 2D LiDAR 图像再用卷积处理。尽管常规 RGB 图像与 LiDAR 图像相似，我们首次发现 LiDAR 图像的特征分布在不同图像位置剧变。用标准卷积处理这类 LiDAR 图像是有问题的，因为卷积滤波器提取的局部特征只在图像特定区域活跃。结果是网络容量利用不足、分割性能下降。为解决这一问题，我们提出空间自适应卷积（SAC），根据输入图像对不同位置采用不同滤波器。SAC 可以高效计算，因为它可以实现为一系列逐元素乘法、im2col 与标准卷积。它是一个通用框架，若干以往方法可视为 SAC 的特例。使用 SAC，我们构建了用于 LiDAR 点云分割的 SqueezeSegV3，在 SemanticKITTI 基准上以至少 2.0 个 mIoU 胜过所有此前发表的方法。代码与预训练模型见 https://github.com/chenfengxu714/SqueezeSegV3。

**TexMesh：从 RGB-D 视频重建精细人体纹理与几何（TexMesh: Reconstructing detailed human texture and geometry from RGB-D video）**
Tiancheng Zhi、Christoph Lassner、Tony Tung、Carsten Stoll、Srinivasa G. Narasimhan、Minh Vo
我们提出 TexMesh——一种从 RGB-D 视频重建带高分辨率全身纹理的精细人体网格的新方法。TexMesh 支持人体的高质量自由视点渲染。给定 RGB 帧、采集的环境图以及来自 RGB-D 跟踪的逐帧粗人体网格，我们的方法重建时空一致且精细的逐帧网格以及高分辨率反照率纹理。利用入射光照，我们能准确估计局部表面几何与反照率，进而利用光度约束以自监督方式把合成训练的模型适配到真实序列，用于精细表面几何与高分辨率纹理估计。实践中，我们在一段短样例序列上训练模型进行自适应，之后模型以交互帧率运行。我们在合成与真实数据上验证 TexMesh，定量与定性均优于现有技术水平。

**TextCaps：带阅读理解的图像描述数据集（TextCaps: a dataset for Image Captioning with Reading Comprehension）**
Oleksii Sidorov、Ronghang Hu、Marcus Rohrbach、Amanpreet Singh
图像描述可以帮助视障人士快速理解图像内容。尽管我们在自动图像描述与光学字符识别方面取得了显著进展，但现有方法无法把书写的文字纳入描述，尽管文字在人类环境中无处不在，且对理解周围环境往往至关重要。为研究如何在图像语境下理解文字，我们收集了一个新数据集 TextCaps，包含 28K 张图像的 145K 条描述。该数据集挑战模型识别文字、将其与视觉语境关联、并决定复制或改写哪部分文字，需要多个文字 token 与视觉实体（如物体）之间的空间、语义与视觉推理。我们研究了基线并改造现有方法以适应这一新任务，我们称之为「带阅读理解的图像描述」。自动与人工分析表明，新的 TextCaps 数据集相比以往数据集提出了许多新的技术挑战。

**面向全球尺度检测与分类的 Mapillary 交通标志数据集（The mapillary traffic sign dataset for detection and classification on a global scale）**
Christian Ertler、Jerneja Mislej、Tobias Ollmann、Lorenzo Porzi、Gerhard Neuhold、Yubin Kuang
交通标志是智慧城市与导航的重要地图要素。为开发精确鲁棒的交通标志检测与分类算法，需要大规模且多样的基准数据集。在本文中，我们引入一个新的交通标志数据集，包含世界各地 10.5 万张街景图像，覆盖 400 个手工标注的交通标志类别，场景多样、地理位置广泛、天气与光照条件多变。数据集包含 5.2 万张完整标注图像。此外，我们展示了如何用 5.3 万张半监督、部分标注的图像扩充数据集。这是最大、最多样的交通标志数据集，由来自世界各地的图像组成，并带有交通标志类别的细粒度标注。我们进行了大量实验，为检测与分类任务建立强基线。此外，我们验证了该数据集的多样性能为现有的交通标志检测与分类大规模基准数据集带来有效迁移学习。该数据集可免费用于学术研究。

**迈向跨深度泛化的单目 3D 目标检测（Towards generalization across depth for monocular 3D object detection）**
Andrea Simonelli、Samuel Rota Bulò、Lorenzo Porzi、Elisa Ricci、Peter Kontschieder
虽然昂贵的 LiDAR 与双目相机设备推动了成功的 3D 目标检测方法的发展，但纯单目 RGB 方法远远落后。本工作通过引入 MoVi-3D——一个新颖的单阶段单目 3D 目标检测深度架构——推进了技术水平。MoVi-3D 建立在新方法之上：利用几何信息在训练与测试时生成虚拟视图，其中物体外观相对于距离被归一化。这些虚拟生成的视图便利了检测任务，因为它们显著降低了放置在距相机不同距离处物体的视觉外观可变性。因此，深度模型无需学习特定深度表示，其复杂性可以显著降低。特别是，在本工作中我们表明，得益于我们的虚拟视图生成过程，一个轻量的单阶段架构就足以在流行的 KITTI3D 基准上刷新最先进结果。

**VisualEchoes：通过回声定位学习空间图像表示（VisualEchoes: Spatial image representation learning through echolocation）**
Ruohan Gao、Changan Chen、Ziad Al-Halah、Carl Schissler、Kristen Grauman
若干动物物种（如蝙蝠、海豚与鲸）甚至视障人类都拥有回声定位的非凡能力：一种用于感知空间布局与定位世界中物体的生物声呐。我们探索回声中所含的空间线索及其如何有益于需要空间推理的视觉任务。我们首先在逼真 3D 室内场景环境中采集回声响应。然后我们提出一个新颖的基于交互的表示学习框架，通过回声定位学习有用的视觉特征。我们表明，学到的图像特征对多个需要空间推理的下游视觉任务——单目深度估计、表面法线估计与视觉导航——都有用，结果可与重监督预训练相当甚至更好。我们的工作为具身智能体的表示学习开辟了新路径：监督来自与物理世界的交互。

## ECCV 2020 的其他活动

**教程**

- 图像、视频与 3D 的视觉识别——Alexander Kirillov、Christoph Feichtenhofer、Georgia Gkioxari、Haoqi Fan、Nikhila Ravi、Piotr Dollár、Ross Girshick、Saining Xie、Wan-Yen Lo、Yuxin Wu，组织者

**研讨会**

8 月 23 日（周日）：

- OpenEyes：VR、AR 与野外中的眼动注视——Sachin S. Talathi、Abhishek Sharma、Yiru Shen、Elias Guerstein、Alexander Fix、Tarek Hefny、Robert Cavin、Kapil Krishnakumar、Jixu Chen，组织者
- 面向 3D 视觉的整体场景结构——Chen Liu，组织者
- 多模态视频分析研讨会与「时刻在时间」挑战赛——Zhicheng Yan，组织者

8 月 28 日（周五）：

- 学习形状与外观的 3D 表示——Tanner Schmidt、Shubham Tulsiani，组织者
- 变化条件下的长期视觉定位——Vassileios Balnatas、Huub Heijnen，组织者
- 通过结构化生成模型的感知——Shubham Tulsiani，组织者
- 自监督学习——下一步是什么？——Armand Joulin，组织者
