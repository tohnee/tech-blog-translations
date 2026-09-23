---
title: "Facebook 研究团队在 CVPR 2020"
title_en: "Facebook Research at CVPR 2020"
date: 2020-06-19
source: https://ai.facebook.com/blog/facebook-research-at-cvpr-2020
crawled: 2026-09-22
translated: 2026-09-22
---

# Facebook 研究团队在 CVPR 2020

> 原文：[Facebook Research at CVPR 2020](https://ai.facebook.com/blog/facebook-research-at-cvpr-2020) · Meta AI（Wayback 存档）

2020 年 6 月 12 日

来自世界各地的计算机视觉（CV）研究员与工程师将于 2020 年 6 月 14 日至 19 日线上齐聚 2020 年计算机视觉与模式识别会议（CVPR）。Facebook AI 的研究员以及 AR/VR 领域的研究者将通过报告展示研究、举办教程、在研讨会演讲，并参与在线互动问答。

在今年的 CVPR 上，Facebook AI 正在 CV 的许多重要领域推进技术水平，包括核心分割任务、架构搜索、迁移学习和多模态学习。我们还将分享几篇值得关注的论文的细节，它们提出了在常规 2D 图像中对 3D 物体进行推理的新方法。这项工作可以帮助我们解锁虚拟现实与增强现实创新等未来体验。我们也在下方分享完整的论文摘要清单以及 CVPR 参与细节。

## 仅凭单张图像生成复杂真实场景的新视角

我们构建了 SynSin——一个最先进的端到端模型，能接收单张 RGB 图像，然后从不同视角生成同一场景的新图像，无需任何 3D 监督。系统先预测一个 3D 点云，再通过我们基于 PyTorch3D 的新型可微渲染器把点云投影到新视角。渲染后的点云随后被送入生成对抗网络（GAN）合成输出图像。现有方法常使用稠密体素网格，在单个物体的合成场景上已有成效，但无法扩展到复杂的真实场景。凭借点云的灵活性，SynSin 不仅做到了这一点，还能泛化到不同分辨率，效率也高于体素网格等替代方案。SynSin 的高效性可以帮助我们探索广泛应用，例如生成更好的 3D 照片与 360 度视频。阅读完整研究论文。

## 从单张图像以前所未有的细节与质量重建 3D 人体

我们开发了一种从 2D 图像生成人体 3D 重建的新方法，具有最先进的质量与细节。它以高分辨率照片为输入，能捕捉手指、面部特征和衣物褶皱等极其复杂的细节——以往技术若不经过额外处理无法做到。为此，我们在内存效率极高的像素对齐隐式函数（PIFu）方法之上构建了一个层次化多级神经网络架构，同时处理全局上下文与局部细节，实现高分辨率 3D 重建。第一级网络利用较低分辨率的输入图像考虑人体的全局 3D 结构，与 PIFu 方法类似；第二级网络是一个轻量网络，可接收更高的 1K 分辨率输入图像来分析局部细节。借助对第一级全局 3D 信息的访问，我们的系统能够高效结合局部与全局信息，完成高分辨率 3D 人体重建。你可以在下方看到我们的方法与最先进技术的定性对比。如此高质量、细粒度的 3D 重建有助于增强创建更逼真虚拟现实体验等重要应用。阅读完整研究论文。

## 「真希望你也在这里」：上下文感知的人生成

我们构建了一个新系统，能把一张照片中的人物添加到另一张图像里，同时保持画面质量与场景交互的语义上下文。它可以在图像中其他人的上下文里生成某人的图像，调整源图像使其姿态与新上下文匹配。这是一个富有挑战的应用领域，因为生成图像中的新人物与原有人物之间的差异特别容易被察觉。与以往向现有图像添加人物的工作不同，我们的方法适用于多种姿态、视角、尺度和严重遮挡。我们的方法包含三个子网络：第一个生成新人物的结构，第二个根据生成的结构和输入目标渲染逼真的人物，第三个精化渲染出的面部。我们在多种实验中展示了高分辨率输出，并对每个网络单独评估，在姿态迁移基准以及其他可能应用（如画一个人、替换人的头发、上衣或裤子）上均取得最先进结果。随着人们对远程活动和跨地点交互的兴趣日增，我们的研究可以让人们在使用视频工具时更自然地协作，或启发新的 AR 体验。阅读完整论文。

## Facebook AI 在 CVPR 2020 的研讨会

**媒体取证研讨会，2020 年 6 月 15 日**
除上述新系统外，Facebook AI 还在研究面部与姿态生成的其他领域，以及被篡改媒体这一更大的开放挑战。我们将展示深度伪造检测方面的进展以及 GAN 等新合成方法。Facebook AI 的讲者包括 Cristian Canton Ferrer 和 Tal Hassner。

**低功耗计算机视觉挑战赛，2020 年 6 月 15 日**
我们与普渡大学、杜克大学和谷歌等社区成员共同举办低功耗计算机视觉挑战赛（LPCV）研讨会。研讨会聚焦把社区成员聚在一起，讨论低功耗计算机视觉的技术水平、创建高效视觉方案的挑战、有前景的技术、数据获取与标注方法，以及评估进展的基准与指标。参加使用 PyTorch-Mobile 的视频赛道竞赛的队伍也将齐聚本研讨会。Facebook AI 讲者包括 Vikas Chandra、Carole-Jean Wu、Joseph Spisak 和 Christian Keller。

**计算机视觉中的女性研讨会，2020 年 6 月 14 日**
Facebook AI 的 Georgia Gkioxari 将在为期半天的计算机视觉中的女性研讨会上演讲。研讨会的目标是为女性提供分享经历与工作、并与领域内榜样建立联系的机会。低年级女生也将通过海报环节分享工作。

**视觉问答与对话研讨会，2020 年 6 月 14 日**
Facebook AI 协助组织了视觉问答与视觉对话研讨会。Douwe Kiela 是讲者，联合组织者包括 Satwik Kottur、Dhruv Batra 和 Devi Parikh。本环节的重点是先通过视觉问答挑战赛对该领域的进展进行基准测试，再讨论最先进方法，包括 MMF：多模态 AI 模型框架。我们还将讨论多模态 AI 的最佳实践与未来方向。作为其中一部分，我们很高兴地宣布，Facebook AI 的研究员与工程师 Xinlei Chen、Duy Kien Nguyen、Vedanuj Goswami、Licheng Yu 以及我们前博士实习生 Huaizu Jiang（马萨诸塞大学阿默斯特分校）赢得了 VQA 挑战赛。在此了解他们使用卷积网格特征图的获胜技术。

**图像、视频与 3D 的视觉识别，2020 年 6 月 15 日**
我们举办一个教程，讨论面向不同输入模态的视觉识别任务家族的流行方法与最新进展。我们将涵盖目标识别与场景理解的最新工作，包括用 PyTorch3D 构建 3D 深度学习模型。教程负责人包括 Ross Girshick、Saining Xie、Alexander Kirillov、Yuxin Wu、Christoph Feichtenhofer、Haoqi Fan、Georgia Gkioxari、Justin Johnson、Nikhila Ravi、Piotr Dollár 和 Wan-Yen Lo。

**DeepVision，2020 年 6 月 19 日**
Facebook AI 领导者 Yann LeCun 与 Joaquin Quiñonero Candela 将在 6 月 19 日为期一天的第七届 DeepVision 研讨会上做主题演讲，Cristian Canton Ferrer 是活动联合组织者。议题将围绕多种前沿学习技术的理论与实践应用，包括有限数据学习、自监督学习、迁移学习等。

**面向 AR/VR 的计算机视觉，2020 年 6 月 15 日**
Facebook Reality Labs 的 Michael Abrash 将在第四届面向 AR/VR 的计算机视觉研讨会上演讲。研讨会旨在把 AR/VR 领域的工业界创新者与学术界领袖聚在一起，讨论 AR/VR 系统的问题、应用与现状。来自 Facebook 的联合组织者包括 Fernando De la Torre、Matt Uyttendaele、Alexandru Eugen Ichim 和 Weipeng Xu。

**具身 AI，2020 年 6 月 14 日**
Facebook AI 的 Franziska Meier 将在今年的具身 AI 研讨会上介绍我们在机器人方面的工作。研讨会旨在汇集计算机视觉、语言、图形学和机器人领域的研究者，分享并讨论能看、能说、能行动、能推理的智能体的现状。研讨会设三项挑战赛，聚焦点导航、物体导航以及模型从仿真环境向真实世界迁移的问题。多位 Facebook AI 研究员共同组织本活动：Julian Straub、Manolis Savva、Devi Parikh、Jitendra Malik、Oleksandr Maksymets、Abhishek Kadian、Aaron Gokaslan 和 Dhruv Batra。

**DynaVis：第二届动态场景重建国际研讨会，2020 年 6 月 14 日**
Facebook Reality Labs 的 Yaser Sheikh 是今年动态场景重建研讨会的特邀讲者，Michael Zollhoefer 是组织委员会成员。研讨会旨在汇集通用动态场景重建领域的顶尖专家。

**几何计算的深度学习，2020 年 6 月 14 日**
Facebook AI 研究总监 Jitendra Malik 将在今年关于用深度学习推进拓扑与几何形状分析技术水平的研讨会上做特邀讲者。Facebook AI 的 Daniel Huber 也在活动程序委员会中。

**计算机视觉中的对抗机器学习，2020 年 6 月 19 日**
Facebook AI 的 Laurens van der Maaten 是今年对抗机器学习研讨会的讲者。Facebook AI 的 Yuxin Wu 和 Kaiming He 在程序委员会中。讨论将围绕增强模型对对抗攻击的鲁棒性。在其他类似话题中，我们将聚焦改进当前计算机视觉模型的策略。

**面向时尚、艺术与设计的计算机视觉，2020 年 6 月 19 日**
Facebook AI 的 Kristen Grauman 与 Tamara Berg 是今年第三届面向时尚、艺术与设计的计算机视觉研讨会的联合组织者。Kristen 与 Devi Parikh 将在活动上演讲。我们正在帮助把艺术家、设计师与计算机视觉研究员和工程师聚在一起，在创意应用与计算机视觉的交叉点上交流思想。研讨会设两个数据集挑战赛和一个论文投稿环节。

## Facebook AI 在 CVPR 2020 的研究完整清单

**12-in-1：多任务视觉与语言表示学习（12-in-1: Multitask vision and language representation learning）**
Jiasen Lu、Vedanuj Goswami、Marcus Rohrbach、Devi Parikh、Stefan Lee
视觉与语言研究大多聚焦于一小批但多样的独立任务及配套数据集，且常被孤立研究；然而，在这些任务上取得成功所需的视觉落地语言理解技能高度重叠。在本工作中，我们通过建立大规模多任务训练机制研究视觉与语言任务间的这些关系。我们的方法最终形成单一模型，覆盖来自四大类任务的 12 个数据集，包括视觉问答、基于描述的图像检索、落地指称表达以及多模态验证。与独立训练的单任务模型相比，参数量从约 30 亿减少到 2.7 亿，同时各任务平均性能提升 2.05 个点。我们用多任务框架深入分析了联合训练多样任务的效果。此外，我们表明从单一多任务模型微调任务专用模型可以带来进一步提升，达到或超过最先进水平。

**高效训练视频模型的多重网格方法（A multigrid method for efficiently training video models）**
Chao-Yuan Wu、Ross Girshick、Kaiming He、Christoph Feichtenhofer、Philipp Krähenbühl
训练有竞争力的深度视频模型比训练对应的图像模型慢一个数量级。训练缓慢导致研究周期冗长，阻碍视频理解研究的进展。遵循训练图像模型的标准做法，视频模型训练一直使用固定的 mini-batch 形状：特定的片段数、帧数和空间尺寸。然而，最优形状是什么？高分辨率模型表现好但训练慢；低分辨率模型训练快但精度低。受数值优化中的多重网格方法启发，我们提出按调度使用不同时空分辨率的可变 mini-batch 形状。不同形状来自在多个采样网格上对训练数据重采样。当缩小其他维度时，通过放大 mini-batch 尺寸与学习率来加速训练。我们实证展示了一个通用而稳健的网格调度，为不同模型（I3D、nonlocal、SlowFast）、数据集（Kinetics、Something-Something、Charades）和训练设置（有无预训练、128 GPU 或 1 GPU）带来显著的开箱即用训练加速且无精度损失。举一个直观例子：与基线训练相比，所提多重网格方法训练 ResNet-50 SlowFast 网络快 4.5 倍（墙上时间、相同硬件），同时在 Kinetics-400 上精度还提升了 0.8 个百分点（绝对值）。代码已在线公开。

**ARCH：着装人体的可动画重建（ARCH: Animatable Reconstruction of Clothed Humans）**
Zeng Huang、Yuanlu Xu、Christoph Lassner、Hao Li、Tony Tung
在本文中，我们提出 ARCH（着装人体的可动画重建）——一个从单目图像精确重建可用于动画的 3D 着装人体的新颖端到端框架。现有的 3D 人体数字化方法难以处理姿态变化和恢复细节，也不能产出可直接用于动画的模型。相比之下，ARCH 是一个学习到的姿态感知模型，能从单张无约束 RGB 图像生成细节丰富的 3D 绑定全身人体化身。我们用参数化 3D 人体估计器构建语义空间与语义变形场，它们能把 2D/3D 着装人体变换到一个规范空间，减少训练数据中姿态变化与遮挡带来的几何歧义。细致的表面几何与外观用带空间局部特征的隐式函数表示学习。此外，我们提出用不透明度感知的可微渲染对 3D 重建施加逐像素监督。实验表明 ARCH 提升了人体重建的保真度。在公开数据集上，我们的标准指标重建误差比最先进方法低 50% 以上。我们还展示了大量文献中前所未见的高质量重建化身动画的定性示例。

**关节感知的规范表面映射（Articulation-aware Canonical Surface Mapping）**
Nilesh Kulkarni、Abhinav Gupta、David F. Fouhey、Shubham Tulsiani
我们处理两个任务：（1）预测规范表面映射（CSM），即从 2D 像素到规范模板形状上对应点的映射；（2）推断与输入图像对应的模板关节与姿态。以往方法依赖关键点监督来学习，我们提出一种无需此类标注的学习方法。我们的关键洞察是这些任务在几何上相关，可以通过在预测之间强制一致性来获得监督信号。我们在多样化的动物物体类别上给出结果，表明我们的方法可以仅用前景掩码标签训练，从图像集合中学习关节与 CSM 预测。我们实证表明允许关节建模有助于学习更准确的 CSM 预测，而与预测 CSM 的一致性约束对学习有意义的关节同样关键。

**用掩码传播在视频中分类、分割和跟踪物体实例（Classifying, segmenting, and tracking object instances in video with mask propagation）**
Gedas Bertasius、Lorenzo Torresani
我们引入一种在视频序列中同时分类、分割和跟踪物体实例的方法。该方法名为 MaskProp，通过增加一个掩码传播分支，把流行的 Mask R-CNN 适配到视频——该分支把每个视频帧的帧级物体实例掩码传播到视频片段中的所有其他帧。这使我们的系统能够相对于片段中间帧分割出的物体实例预测片段级实例轨迹。对序列中每一帧密集生成的片段级实例轨迹最终被聚合，产出视频级物体实例分割与分类。实验表明片段级实例分割使我们的方法对视频中的运动模糊和物体遮挡具有鲁棒性。MaskProp 在 YouTube-VIS 数据集上取得已报告的最佳精度，胜过 ICCV 2019 视频实例分割挑战赛冠军，同时结构更简单，使用的标注数据少几个数量级（130 万 vs 10 亿张图像，86 万 vs 1400 万个边界框）。项目页面：https://gberta.github.io/maskprop/。

**聚类再学习：改进视觉表示的泛化（Cluster and relearn: Improving generalization of visual representations）**
Xueting Yan、Ishan Misra、Abhinav Gupta、Deepti Ghadiyaram、Dhruv Mahajan
用弱监督与自监督策略预训练卷积神经网络，在多个计算机视觉任务中日益流行。然而，由于缺乏强判别信号，学到的表示可能过拟合预训练目标（如话题标签预测），对下游任务泛化不佳。在本工作中，我们提出一个简单策略——ClusterFit（CF）——来提升预训练期间学到的视觉表示的鲁棒性。给定一个数据集，我们（a）用 k-means 对预训练网络提取的特征聚类，（b）以聚类分配为伪标签，在该数据集上从头重训一个新网络。我们实证表明，聚类有助于从提取的特征中减少预训练任务专属信息，从而最小化对它的过拟合。我们的方法可扩展到不同的预训练框架——弱监督与自监督、模态——图像与视频，以及预训练任务——物体与动作分类。通过在 11 个不同词表与粒度的目标数据集上的大量迁移学习实验，我们表明 CF 显著提升了表示质量，胜过最先进的大规模（百万/十亿级）弱监督图像视频模型与自监督图像模型。

**设计网络设计空间（Designing network design spaces）**
Ilija Radosavovic、Raj Prateek Kosaraju、Ross Girshick、Kaiming He、Piotr Dollar
在本工作中，我们提出一种新的网络设计范式。我们的目标是帮助推进对网络设计的理解，并发现可跨设置泛化的设计原则。我们不聚焦于设计单个网络实例，而是设计对网络总体进行参数化的网络设计空间。整个过程类似于经典的手工网络设计，但提升到了设计空间层面。用我们的方法学探索网络设计的结构方面，得到了一个由简单、规则的网络组成的低维设计空间，我们称之为 RegNet。RegNet 参数化的核心洞察出奇简单：好网络的宽度与深度可以用一个量化线性函数解释。我们分析 RegNet 设计空间，得到了与当前网络设计实践不符的有趣发现。RegNet 设计空间提供了在广泛 FLOP 区间上都表现良好的简单快速网络。在可比的训练设置与 FLOPs 下，RegNet 模型胜过流行的 EfficientNet 模型，且在 GPU 上最快快 5 倍。

**不要以上下文论物体：学习克服上下文偏差（Don't judge an object by its context: Learning to overcome contextual bias）**
Krishna Kumar Singh、Dhruv Mahajan、Kristen Grauman、Yong Jae Lee、Matt Feiszli、Deepti Ghadiyaram
现有模型常利用物体与其上下文的共现来提升识别精度。然而，过度依赖上下文会危及模型的泛化能力，尤其是当典型共现模式缺失时。本工作聚焦解决此类上下文偏差，以提升所学特征表示的鲁棒性。我们的目标是在上下文缺失时准确识别一个类别，同时不牺牲它与上下文共现时的性能。我们的关键思想是把一个类别的特征表示与其共现上下文去相关。为此，我们学习一个显式表示无上下文出现的类别的特征子空间，以及一个同时表示类别与上下文的联合特征子空间。这个简单而有效的方法可扩展到两个多标签任务——物体分类与属性分类。在四个富有挑战的数据集上，我们展示了方法在降低上下文偏差上的有效性。

**EGO-TOPO：从自我中心视频获取环境可供性（EGO-TOPO: Environment affordances from egocentric video）**
Tushar Nagarajan、Yanghao Li、Christoph Feichtenhofer、Kristen Grauman
第一人称视频天然把物理环境的使用推到前台，因为它展现了佩戴者基于自身意图在空间中的流畅互动。然而，当前方法大多把观察到的动作与持久空间本身分离。我们引入一个直接从自我中心视频学习的环境可供性模型。主要思想是获得一个以人为中心的物理空间（如厨房）模型，捕捉（1）主要的交互空间区域和（2）这些区域可能支持的活动。我们的方法把空间分解为从第一人称活动导出的拓扑图，把自我视频组织为对不同区域的一系列访问。此外，我们展示如何跨多个相关环境（如多个厨房的视频）关联区域，获得环境功能的整合表示。在 EPIC-Kitchens 和 EGTEA+ 上，我们展示了该方法用于学习场景可供性以及在长视频中预测未来动作。项目页面：http://vision.cs.utexas.edu/projects/ego-topo/

**单张图像的端到端视图合成（End-to-end view synthesis from a single image）**
Olivia Wiles、Georgia Gkioxari、Richard Szeliski、Justin Johnson
视图合成允许从一张或多张图像生成场景的新视图。这很有挑战性，需要从图像全面理解 3D 场景。因此，现有方法通常使用多张图像、在真值深度上训练，或局限于合成数据。我们为该任务提出一个新颖的端到端模型，测试时只使用单张图像；它在真实图像上训练，无需任何真值 3D 信息。为此，我们引入一个新颖的可微点云渲染器，用于把特征的潜在 3D 点云变换到目标视图。投影后的特征由我们的精化网络解码，补绘缺失区域并生成逼真的输出图像。生成模型中的 3D 组件允许在测试时对潜在特征空间进行可解释的操控，例如我们可以从单张图像生成轨迹动画。此外，我们能生成高分辨率图像并泛化到其他输入分辨率。我们在 Matterport、Replica 和 RealEstate10K 数据集上胜过基线与先前工作。

**极线 transformer（Epipolar transformers）**
Yihui He、Rui Yan、Katerina Fragkiadaki、Shoou-I Yu
在同步且标定的多视角设置中定位 3D 人体关节的常见做法分两步：（1）在每个视角上分别应用 2D 检测器定位 2D 关节；（2）对各视角的 2D 检测做鲁棒三角化获得 3D 关节位置。然而在第 1 步中，2D 检测器只能在纯 2D 中解决那些本可在 3D 中更好解决的困难情形（如遮挡与斜视角），而未利用任何 3D 信息。因此，我们提出可微的「极线 transformer」，使 2D 检测器能利用 3D 感知特征改进 2D 姿态估计。直觉是：给定当前视角中的 2D 位置 p，我们先在相邻视角中找到其对应点 p0，然后把 p0 处的特征与 p 处的特征结合，从而在 p 处得到 3D 感知特征。受立体匹配启发，极线 transformer 利用极线约束与特征匹配来近似 p0 处的特征。在 InterHand 和 Human3.6M [13] 上的实验表明我们的方法相较基线持续改进。具体来说，在不使用外部数据的条件下，我们用 ResNet-50 主干、256×256 图像尺寸训练的 Human3.6M 模型超过最先进水平 4.23 毫米，达到 MPJPE 26.9 毫米。代码已公开。

**FBNetV2：面向空间与通道维度的可微神经架构搜索（FBNetV2: Differentiable neural architecture search for spatial and channel dimensions）**
Alvin Wan、Xiaoliang Dai、Peizhao Zhang、Zijian He、Yuandong Tian、Saining Xie、Bichen Wu、Matthew Yu、Tao Xu、Kan Chen、Peter Vajda、Joseph E. Gonzalez
可微神经架构搜索（DNAS）在设计最先进的高效神经网络方面已大获成功。然而，基于 DARTS 的 DNAS 搜索空间相比其他搜索方法较小，因为所有候选网络层都必须在内存中显式实例化。为突破这一瓶颈，我们提出内存与计算高效的 DNAS 变体：DMaskingNAS。该算法把搜索空间较传统 DNAS 最多扩展 10^14 倍，支持对原本代价高不可攀的空间与通道维度——输入分辨率与滤波器数量——的搜索。我们提出用于特征图复用的掩码机制，使搜索空间扩展时内存与计算成本几乎保持恒定。此外，我们采用有效的形状传播来最大化每 FLOP 或每参数的精度。搜索出的 FBNetV2 与此前所有架构相比取得最先进性能。以最多低 421 倍的搜索成本，DMaskingNAS 找到的模型比 MobileNetV3-Small 精度高 0.9%、FLOPs 少 15%；与 Efficient-B0 精度相当但 FLOPs 少 20%。此外，我们的 FBNetV2 在模型尺寸相当的情况下精度比 MobileNetV3 高 2.6%。FBNetV2 模型已开源：https://github.com/facebookresearch/mobile-vision。

**从巴黎到柏林：发现世界各地的风格影响（From Paris to Berlin: Discovering style influences around the world）**
Ziad Al-Halah、Kristen Grauman
服装风格的演化及其在世界各地的迁移引人入胜，却难以定量描述。我们提出从人们穿衣的日常图像中发现并量化时尚影响。我们引入一种检测哪些城市在传播风格方面影响其他哪些城市的方法，然后利用发现的影响模式指导一个预测模型，预测任意给定风格在任意给定城市未来的流行度。我们用 GeoStyle——一个覆盖全球 44 个主要城市、770 万张图像的大规模数据集——演示了这一想法，展示了发现的影响关系，揭示了城市如何对 50 种观察到的视觉风格施加和接受时尚影响。此外，所提预测模型在富有挑战的风格预测任务上取得最先进结果，显示了在空间与时间上同时锚定视觉风格演化的优势。

**从块到图（PaQ-2-PiQ）：映射图像质量的感知空间（From Patches to Pictures (PaQ-2-PiQ): Mapping the Perceptual Space of Picture Quality）**
Zhenqiang Ying、Haoran Niu、Praful Gupta、Dhruv Mahajan、Deepti Ghadiyaram、Alan Bovik
盲或无参考（NR）感知图像质量预测是一个困难且未解决的问题，对每天影响数十亿观众的社会与流媒体行业意义重大。遗憾的是，流行的 NR 预测模型在真实世界的失真图像上表现不佳。为推动该问题的进展，我们引入迄今最大的主观图像质量数据库，包含约 4 万张真实失真图像与 12 万个图像块，并收集了约 400 万条人类图像质量判断。利用这些图像与图像块质量标签，我们构建了基于区域的深度架构，学习产生最先进的全局图像质量预测以及有用的局部图像质量图。我们的创新包括既能做全局到局部推断、也能做局部到全局推断（通过反馈）的图像质量预测架构。数据集与源代码见 https://live.ece.utexas.edu/research.php。

**GrappaNet：结合并行成像与深度学习的多线圈 MRI 重建（GrappaNet: Combining Parallel Imaging With Deep Learning for Multi-Coil MRI Reconstruction）**
Anuroop Sriram、Jure Zbontar、Tullie Murrell、C. Lawrence Zitnick、Aaron Defazio、Daniel K. Sodickson
磁共振图像（MRI）采集本质上是一个缓慢的过程，这催生了两种加速方法：同时采集多个相关样本（并行成像），以及采集少于传统信号处理方法所需的样本数（压缩感知）。两种方法为加速 MRI 采集提供了互补途径。在本文中，我们提出一种把传统并行成像方法整合进深度神经网络的新方法，即便在高加速因子下也能生成高质量重建。所提方法称为 GrappaNet，执行渐进式重建：先用神经网络把重建问题映射到一个可用传统并行成像方法求解的更简单问题，接着应用并行成像方法，最后用另一个神经网络微调输出。整个网络可端到端训练。我们在新近发布的 fastMRI 数据集上给出实验结果，表明 GrappaNet 在 4 倍和 8 倍加速下都能生成比竞争方法质量更高的重建。

**用于视觉定位的层次化场景坐标分类与回归（Hierarchical scene coordinate classification and regression for visual localization）**
Xiaotian Li、Shuzhe Wang、Yi Zhao、Jakob Verbeek、Juho Kannala
视觉定位对计算机视觉与机器人的许多应用至关重要。针对单图像 RGB 定位，最先进的基于特征的方法在查询图像与预建 3D 模型之间匹配局部描述子。近来，深度神经网络被用来回归原始像素与场景 3D 坐标之间的映射，匹配由网络的前向传播隐式完成。然而，在大型且歧义多的环境中，单个网络直接学习这样的回归任务可能很困难。在本工作中，我们提出一个新的层次化场景坐标网络，从单张 RGB 图像以由粗到细的方式预测像素场景坐标。该网络由一系列输出层组成，每个层以前面的层为条件。最终输出层预测 3D 坐标，其余层产生逐渐更精细的离散位置标签。所提方法优于纯回归基线网络，使我们能训练可稳健扩展到大型环境的紧凑模型。它在 7-Scenes、12-Scenes、剑桥地标数据集及三个组合场景上刷新了单图像 RGB 定位性能的最先进水平。此外，针对 Aachen Day-Night 数据集上的大规模室外定位，我们提出一种混合方法，优于现有场景坐标回归方法，并显著缩小了与显式特征匹配方法的性能差距。

**用弱标注数据改进少样本目标检测（Improving lowshot object detection with weakly labeled Data）**
Vignesh Ramanathan、Rui Wang、Dhruv Mahajan
大型检测数据集存在边界框标注极少的少样本类长尾。我们希望仅用只有图像级标签的弱标注网络规模数据集来改进少样本类检测。这需要一个能与少量边界框标注图像和大量弱标注图像联合训练的检测框架。为此，我们对 FRCNN 模型提出修改，在训练期间自动为来自弱标注图像的物体候选推断标签分配。我们把这一标签分配表述为带约束的线性规划，约束图像中物体实例的数量与重叠。我们表明这可以在训练期间对弱标注图像高效求解。与只用少量标注样本训练相比，在我们的框架中加入弱标注样本带来显著增益。我们在 LVIS 数据集（AP 提升 3.5 个点）以及 COCO 数据集的不同少样本变体上进行了演示。我们详尽分析了训练检测模型所需的弱标注与全标注数据量的影响。我们的 DLWL 框架在少样本类上也能胜过 omni-supervision 等自监督基线。

**ImVoteNet：用图像投票增强点云 3D 目标检测（ImVoteNet: Boosting 3D object detection in point clouds with image votes）**
Charles R. Qi、Xinlei Chen、Or Litany、Leonidas J. Guibas
得益于点云深度学习的进展，3D 目标检测发展迅速。一些近期工作甚至仅凭点云输入就取得了最先进性能（如 VOTENET）。然而点云数据有固有局限：稀疏、缺乏颜色信息、且常有传感器噪声。图像则具有高分辨率与丰富纹理，可以补充点云提供的 3D 几何。但如何有效利用图像信息辅助基于点云的检测仍是开放问题。在本工作中，我们在 VOTENET 之上构建了专为 RGB-D 场景设计的 3D 检测架构 IMVOTENET。IMVOTENET 基于融合图像中的 2D 投票与点云中的 3D 投票。与以往多模态检测工作相比，我们从 2D 图像中显式提取几何与语义特征，并利用相机参数把这些特征提升到 3D。为改进 2D-3D 特征融合的协同，我们还提出多塔训练方案。我们在富有挑战的 SUN RGB-D 数据集上验证模型，把最先进结果提升 5.7 mAP。我们还提供丰富的消融研究，分析每个设计选择的贡献。

**为视觉问答中的网格特征辩护（In defense of grid features for visual question answering）**
Huaizu Jiang、Ishan Misra、Marcus Rohrbach、Erik Learned-Miller、Xinlei Chen
以「自下而上」注意力之名为人熟知的基于边界框（区域）的视觉特征，近来在视觉问答（VQA）等视觉与语言任务上超越了朴素的基于网格的卷积特征，成为事实标准。然而，区域的优势（如更好的定位）是否是自下而上注意力成功的关键原因尚不清楚。在本文中，我们重新审视 VQA 的网格特征，发现它们可以出人意料地好——在精度相同时（例如以类似方式预训练）运行快一个数量级以上。通过大量实验，我们验证这一观察在不同 VQA 模型与数据集上均成立，并很好泛化到图像描述等其他任务。由于网格特征使模型设计与训练过程简单得多，我们得以端到端训练它们并使用更灵活的网络设计。我们端到端学习 VQA 模型——从像素直接到答案——并表明不使用任何区域标注预训练也能取得强劲性能。我们希望这些发现有助于进一步改进 VQA 的科学理解与实际应用。代码与特征将公开。

**面向 TextVQA 的指针增强多模态 transformer 迭代答案预测（Iterative answer prediction with pointer-augmented multimodal transformers for TextVQA）**
Ronghang Hu、Amanpreet Singh、Trevor Darrell、Marcus Rohrbach
许多视觉场景中包含承载关键信息的文字，因此理解图像中的文字对下游推理任务至关重要。例如，警示牌上的深水标签提醒人们场景中的危险。近期工作探索了需要阅读和理解图像文字来回答问题的 TextVQA 任务。然而，现有的 TextVQA 方法大多基于两两模态之间的定制融合机制，并把 TextVQA 当作分类任务从而局限于单步预测。在本工作中，我们为 TextVQA 提出一个基于多模态 transformer 架构的新模型，并配有丰富的图像文字表示。我们的模型把不同模态嵌入公共语义空间从而自然地同质融合，并在该空间中应用自注意力建模模态间与模态内上下文。此外，它通过动态指针网络实现迭代答案解码，使模型能够通过多步预测而非一步分类形成答案。我们的模型在三个 TextVQA 基准数据集上大幅胜过现有方法。

**通过相机解耦表示的轻量多视角 3D 姿态估计（Lightweight multiview 3D pose estimation through camera-disentangled representation）**
Edoardo Remelli、Shangchen Han、Sina Honari、Pascal Fua、Robert Wang
我们提出一个轻量解决方案，从空间标定相机采集的多视角图像恢复 3D 姿态。基于可解释表示学习的最新进展，我们利用 3D 几何把输入图像融合成一个统一的姿态潜在表示，该表示与相机视角解耦。这使我们能够跨不同视角对 3D 姿态进行有效推理，而无需计算密集的体素网格。随后我们的架构以相机投影算子为条件处理学到的表示，产生精确的逐视角 2D 检测，并可通过可微直接线性变换（DLT）层简单提升到 3D。为高效完成这一点，我们提出一种新的 DLT 实现，在 GPU 架构上比标准的基于 SVD 的三角化方法快若干数量级。我们在两个大规模人体姿态数据集（H36M 和 Total Capture）上评估了方法：它优于或可比最先进的体素方法，而且与它们不同，能实现实时性能。

**先听后看：通过预览音频做动作识别（Listen to look: Action recognition by previewing audio）**
Ruohan Gao、Tae-Hyun Oh、Kristen Grauman、Lorenzo Torresani
面对视频数据的洪流，当今昂贵的片段级分类器越来越不切实际。我们提出一个面向未修剪视频高效动作识别的框架，用音频作为预览机制来消除短期与长期的视觉冗余。首先，我们设计 IMGAUD2VID 框架，通过从更轻的模态——单帧及其伴随音频——蒸馏来「幻觉」片段级特征，减少短期时间冗余，实现高效的片段级识别。其次，在 IMGAUD2VID 基础上，我们进一步提出 IMGAUD-SKIMMING——一个基于注意力的长短期记忆网络，迭代选择未修剪视频中的有用时刻，减少长期时间冗余，实现高效的视频级识别。在四个动作识别数据集上的大量实验表明，我们的方法在识别精度与速度两方面都达到最先进水平。

**用于无监督视觉表示学习的动量对比（Momentum contrast for unsupervised visual representation learning）**
Kaiming He、Haoqi Fan、Yuxin Wu、Saining Xie、Ross Girshick
我们提出用于无监督视觉表示学习的动量对比（MoCo）。从把对比学习 [27] 视为字典查找的视角出发，我们用队列和移动平均编码器构建了一个动态字典。这使我们能够即时构建一个大型且一致的字典，促进对比无监督学习。MoCo 在 ImageNet 分类的常见线性协议下提供了有竞争力的结果。更重要的是，MoCo 学到的表示能良好迁移到下游任务。在 PASCAL VOC、COCO 及其他数据集的 7 个检测/分割任务上，MoCo 可以胜过其有监督预训练对应版本，有时优势巨大。这表明在许多视觉任务中，无监督与有监督表示学习之间的差距已大幅缩小。代码见 https://github.com/facebookresearch/MoCo。

**物体融合（Object fusion）**
Martin Rünz、Kejie Li、Meng Tang、Lingni Ma、Chen Kong、Tanner Schmidt、Ian Reid、Lourdes Agapito、Julian Straub、Steven Lovegrove、Richard Newcombe
面向物体的地图对场景理解很重要，因为它们同时捕捉几何与语义，并允许单个实例化以及对物体的有意义推理。我们引入 FroDO——一种从 RGB 视频精确重建物体实例的方法，以由粗到细的方式推断物体位置、姿态与形状。FroDO 的关键在于把物体形状嵌入一个新颖的学习空间，允许在稀疏点云与稠密 DeepSDF 解码之间无缝切换。给定一串已定位的 RGB 帧序列，FroDO 先聚合 2D 检测，为每个物体实例化一个类别感知的 3D 边界框；然后用编码器网络回归一个形状码，再在学到的形状先验下用稀疏与稠密形状表示进一步优化形状与姿态。优化使用多视角几何、光度与轮廓损失。我们在 Pix3D、Redwood-OS 和 ScanNet 等真实数据集上评估单视角、多视角与多物体重建。

**面向人脸生成的单样本域适配（One-Shot Domain Adaptation For Face Generation）**
Chao Yang、Ser-Nam Lim
在本文中，我们提出一个框架，能够生成与给定单样本示例同分布的人脸图像。我们利用一个已学到通用人脸分布的预训练 StyleGAN 模型。给定单样本目标，我们开发了一种迭代优化方案，快速调整模型权重，把输出的高层分布转移到目标的分布。为生成同分布图像，我们引入一种风格混合技术，把目标的低层统计量迁移到用模型随机生成的人脸上。由此，我们能够生成数量不限的人脸，同时继承通用人脸与单样本示例的分布。新生成的人脸可作为其他下游任务的增广训练数据。这一设定颇具吸引力，因为目标域只需标注极少甚至一个样本——现实世界中的人脸篡改往往正是如此，其来源是各种未知且独特的分布，每种分布的出现率都极低。我们展示了单样本方法在检测人脸篡改上的有效性，并与其他少样本域适配方法做了定性与定量比较。

**PIFuHD：用于高分辨率 3D 人体数字化的多级像素对齐隐式函数（PIFuHD: Multilevel pixel-aligned implicit function for high-resolution 3D human digitization）**
Shunsuke Saito、Tomas Simon、Jason Saragih、Hanbyul Joo
基于图像的 3D 人体形状估计的最新进展，得益于深度神经网络表示能力的显著提升。尽管当前方法已在真实场景中展示了潜力，但仍无法产出输入图像中常见细节水平的重建。我们认为这一局限主要源于两个相互冲突的要求：准确的预测需要大上下文，而精确的预测需要高分辨率。受当前硬件内存限制，以往方法倾向于以低分辨率图像为输入以覆盖大空间上下文，结果只能产出较不精确（低分辨率）的 3D 估计。我们通过构建端到端可训练的多级架构来解决这一局限。粗层级以较低分辨率观察整幅图像并专注于整体推理，为细层级提供上下文；细层级通过观察更高分辨率图像估计高度细致的几何。我们证明，通过充分利用 1K 分辨率输入图像，我们的方法在单图像人体形状重建上显著优于现有最先进技术。

**PointRend：把图像分割当作渲染（PointRend: Image segmentation as rendering）**
Alexander Kirillov、Yuxin Wu、Kaiming He、Ross Girshick
我们提出一种高效高质量地分割物体与场景图像的新方法。通过把经典计算机图形学中的高效渲染方法类比为像素标注任务中的过采样与欠采样挑战，我们形成了把图像分割视为渲染问题的独特视角。从这一视角出发，我们提出 PointRend（基于点的渲染）神经网络模块：一个基于迭代细分算法在自适应选择的位置执行基于点的分割预测的模块。PointRend 可以在现有最先进模型之上灵活应用于实例分割与语义分割任务。尽管这一通用思想有许多可能的实现，我们表明一个简单设计已能取得出色结果。定性上，PointRend 在以往方法过度平滑的区域输出锐利的物体边界。定量上，PointRend 在 COCO 与 Cityscapes 上的实例与语义分割均带来显著增益。PointRend 的效率使输出分辨率达到现有方法在内存或计算上不切实际的水平。代码见 https://github.com/facebookresearch/detectron2/tree/master/projects/PointRend。

**前置任务不变的自监督表示学习（Pretext invariant self-supervised representation learning）**
Ishan Misra、Laurens van der Maaten
从图像进行自监督学习的目标，是通过不需要语义标注的前置任务构建语义上有意义的图像表示。许多前置任务得到的表示对图像变换是协变的。我们论证，语义表示恰恰应当在这样的变换下不变。具体而言，我们开发了前置任务不变表示学习（PIRL，读作「pearl」），基于前置任务学习不变表示。我们把 PIRL 与一个常用的涉及拼图求解的前置任务结合使用。我们发现 PIRL 大幅提升了所学图像表示的语义质量。我们的方法在多个流行的自监督学习基准上刷新了图像自监督学习的技术水平。尽管是无监督的，PIRL 在为物体检测学习图像表示上胜过有监督预训练。总而言之，我们的结果展示了具有良好不变性的自监督表示的潜力。

**把稠密姿态迁移到近缘动物类别（Transferring Dense Pose to Proximal Animal Classes）**
Artsiom Sanakoyeu、Vasil Khalidov、Maureen S. McCarthy、Andrea Vedaldi、Natalia Neverova
近期成果表明，给定一个详细标注姿态的大型数据集，可以稠密而准确地识别人类姿态。原则上，同样的方法可以扩展到任何动物类别，但为每种情况收集新标注所需的努力使这一策略不切实际——尽管它在自然保护、科学和商业上有重要应用。我们证明，至少对于黑猩猩等近缘动物类别，可以把人类稠密姿态识别以及更通用的物体检测器与分割器中已有的知识迁移到其他类别的稠密姿态识别问题。我们的做法是：（1）为新的动物建立一个在几何上也与人类对齐的 DensePose 模型；（2）引入便于在类别之间迁移多个识别任务的多头 R-CNN 架构；（3）找出哪些已知类别的组合能最有效地迁移到新动物；（4）用自校准不确定性头生成按质量分级的伪标签来训练该类别的模型。我们还引入两个以 DensePose 方式标注的黑猩猩类别基准数据集并用于评估方法，展示了出色的迁移学习性能。

**用原力吧，卢克！通过模拟效果学习预测物理力（Use the Force, Luke! Learning to predict physical forces by simulating effects）**
Kiana Ehsani、Shubham Tulsiani、Saurabh Gupta、Ali Farhadi、Abhinav Gupta
当我们人类观看人-物交互视频时，不仅能推断发生了什么，甚至能提取可操作的信息并模仿这些交互。另一方面，当前的识别或几何方法缺乏动作表示的物理性。在本文中，我们朝更物理的动作理解迈出一步。我们处理从人与物体交互视频中推断接触点与物理力的问题。解决该问题的主要挑战之一是获取力的真值标签。我们绕开这一问题，改用物理仿真器做监督。具体而言，我们用仿真器预测效果，并强制估计出的力必须产生与视频所示相同的效果。定量与定性结果表明：（a）我们可以从视频中预测有意义的力，其效果能准确模仿观察到的运动；（b）通过联合优化接触点与力预测，相比独立训练可以同时提升两个任务的性能；（c）我们可以从该模型学习一个能少样本泛化到新物体的表示。

**VPLNet：利用消失点与直线的深度单视图法线估计（VPLNet: Deep single view normal estimation with vanishing points and lines）**
Rui Wang、David Geraghty、Kevin Matzen、Jan-Michael Frahm、Richard Szeliski
我们提出一种新颖的单视图表面法线估计方法，把传统的直线与消失点分析和深度学习方法相结合。从彩色图像与曼哈顿线图出发，我们用深度神经网络回归稠密法线图，以及识别与曼哈顿方向对齐平面区域的稠密曼哈顿标签图。我们以完全可微的方式融合法线图与标签图，产出精化后的法线图作为最终输出。为此，我们把输出软分解为曼哈顿部分与非曼哈顿部分：曼哈顿部分由离散分类与消失点处理，非曼哈顿部分由直接监督学习。我们的方法在标准单视图法线估计基准上取得最先进结果。更重要的是，我们表明通过使用消失点与直线，我们的方法比现有工作具有更好的泛化能力。此外，我们展示了表面法线网络如何在定量与定性上改进深度估计网络的性能，尤其在墙壁与其他平坦表面的 3D 重建中。

**ViBE：为多样体型着装（ViBE: Dressing for diverse body shapes）**
Wei-Lin Hsiao、Kristen Grauman
体型在决定什么衣服最适合某个人方面扮演重要角色，但如今的服装推荐方法采用「一种版型适穿所有人」的思路。这些无视体型的视觉方法与数据集是包容性的障碍，难以对多样体型提供好建议。我们引入 ViBE——一种捕捉服装与不同体型亲和度的视觉体型感知嵌入（VIsual Body-aware Embedding）。给定一个人的图像，所提嵌入能识别会衬托其特定体型的服装。我们展示了如何从展示各种体形与尺寸的时装模特穿着产品的在线目录中学习该嵌入，并设计了一种解释算法对合身服装建议的方法。我们把该方法应用于一个多样化主体的数据集，无论按自动指标还是人类意见，都展示了它相对无视体型的现状推荐方法的强大优势。

**用相关网络做视频分类（Video classification with correlation networks）**
Heng Wang、Du Tran、Lorenzo Torresani、Matt Feiszli
运动是识别视频中动作的显著线索。现代动作识别模型要么显式地用光流作为输入、要么通过同时捕捉外观与运动信息的 3D 卷积滤波器隐式利用运动信息。本文提出一种基于可学习相关算子的替代方法，可在网络不同层的卷积特征图上建立帧到帧的匹配。所提架构使这种显式时间匹配信息能与 2D 卷积捕捉的传统外观线索融合。我们的相关网络与广泛使用的 3D CNN 视频建模相比表现更优，与著名的双流网络相比取得有竞争力的结果且训练快得多。我们实证表明相关网络在多种视频数据集上产生强劲结果，并在三个流行的动作识别基准——Kinetics、Something-Something 和 Diving48——上胜过最先进水平。

**基于神经拓扑映射的视觉导航（Visual navigation via neural topological mapping）**
Devendra Singh Chaplot、Ruslan Salakhutdinov、Abhinav Gupta、Saurabh Gupta
本文研究图像目标导航问题：在未见过的全新环境中导航到目标图像所示的位置。为解决该问题，我们设计了有效利用语义并支持近似几何推理的拓扑空间表示。表示的核心是带有关联语义特征、用粗略几何信息相互连接的节点。我们描述了能在带噪执行下构建、维护并使用此类表示的基于监督学习的算法。在视觉与物理逼真仿真中的实验研究表明，我们的方法构建了捕捉结构规律性的有效表示，并高效解决长时程导航问题。我们观察到相对现有研究该任务的方法有超过 50% 的相对提升。

**是什么让多模态网络训练变得困难？（What makes training multi-modal networks hard?）**
Weiyao Wang、Du Tran、Matt Feiszli
考虑在具有多种输入模态的任务上端到端训练多模态与单模态网络：多模态网络接收更多信息，因此应当不逊于甚至优于单模态对应版本。然而在我们的实验中观察到相反现象：最佳单模态网络常常优于多模态网络。这一观察在不同模态组合以及不同视频分类任务与基准上均一致。本文确定了性能下降的两个主因：第一，多模态网络因容量增加而容易过拟合；第二，不同模态以不同速率过拟合与泛化，用单一优化策略联合训练它们是次优的。我们用一种称为 Gradient-Blending 的技术解决这两个问题，它基于各模态的过拟合行为计算模态间的最优混合。我们证明 Gradient-Blending 胜过广泛使用的防过拟合基线，并在人体动作识别、自我中心动作识别与声学事件检测等多种任务上取得最先进精度。

**真希望你也在这里：上下文感知的人生成（Wish You Were Here: Context Aware Human Generation）**
Oran Gafni、Lior Wolf
我们提出一种把物体（特别是人）插入现有图像的新方法，使其以照片级逼真方式融入并尊重场景的语义上下文。我们的方法包含三个子网络：第一个根据场景中其他人的姿态与可选的边界框规范，生成新人物的语义图；第二个网络以多个外观组件形式的规范为基础，渲染新人物的像素及其混合掩码；第三个网络精化生成的面部，使其匹配目标人物。我们的实验在这一新颖而富有挑战的应用领域中展示了令人信服的高分辨率输出。此外，三个网络被单独评估，例如在姿态迁移基准上取得了最先进结果。

**X3D：扩展架构实现快速视频识别（X3D: Expanding Architectures for Fast Video Recognition）**
Christoph Feichtenhofer
本文提出 X3D——一族高效视频网络，通过沿多个网络轴（空间、时间、宽度与深度）渐进扩展一个微型 2D 图像分类架构得到。受机器学习中的特征选择方法启发，采用简单的逐步网络扩展方法，每步扩展单一轴，从而实现精度与复杂度的良好权衡。为把 X3D 扩展到特定目标复杂度，我们执行渐进式前向扩展和后向收缩。我们最惊人的发现是：一个具有高时空分辨率的快速网络可以表现很好，同时网络宽度与参数量极其轻量。我们在视频分类与检测基准上报告了前所未有的效率下的有竞争力精度。

**You2Me：通过第一与第二人称交互推断自我中心视频中的身体姿态（You2Me: Inferring body pose in egocentric video via first and second person interactions）**
Evonne Ng、Donglai Xiang、Hanbyul Joo、Kristen Grauman
佩戴相机者的身体姿态对增强现实、医疗健康和机器人等应用极具价值，但对典型的可穿戴相机而言，此人身体的大部分都在视野之外。我们提出一种基于学习的方法，从自我中心视频序列估计相机佩戴者的 3D 身体姿态。我们的关键洞察是利用与另一个人的交互——其身体姿态可以直接观察——作为与第一人称主体身体姿态内在关联的信号。我们表明，由于个体之间的交互常引发一串有序的往复反应，即使一方大部分时间不在视野内，也能学习相互关联姿态的时间模型。我们在多个双人交互领域演示了这一想法，并展示了对自我中心身体姿态估计的重大影响，改进了最先进水平。
