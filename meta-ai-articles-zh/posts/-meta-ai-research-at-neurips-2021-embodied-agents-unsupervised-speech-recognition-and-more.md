---
title: "Meta AI 在 NeurIPS 2021 上的研究：具身智能体、无监督语音识别等"
title_en: "Meta AI research at NeurIPS 2021: Embodied agents, unsupervised speech recognition, and more"
date: 2021-12-06
source: http://ai.facebook.com/blog/-meta-ai-research-at-neurips-2021-embodied-agents-unsupervised-speech-recognition-and-more
crawled: 2026-09-22
translated: 2026-09-22
---

# Meta AI 在 NeurIPS 2021 上的研究：具身智能体、无监督语音识别等

> 原文：[Meta AI research at NeurIPS 2021: Embodied agents, unsupervised speech recognition, and more](http://ai.facebook.com/blog/-meta-ai-research-at-neurips-2021-embodied-agents-unsupervised-speech-recognition-and-more) · Meta AI（Wayback 存档）

我们很高兴地宣布，Meta AI 研究者将在 NeurIPS 2021 上展示 83 篇论文，其中 8 篇为亮点报告（spotlight）、5 篇为口头报告（oral），还有一篇论文获得了杰出论文奖（Outstanding Paper Award）。我们的研究者还协助共同组织了六个 NeurIPS 研讨会和五项挑战赛，并将在研讨会上发表多场受邀和投稿演讲。

## 通过挑战赛和研讨会与 AI 社区协作

Meta AI 自豪地赞助了两个 NeurIPS 亲和团体研讨会（LatinX 与 WiML）以及 Black in AI 组织。今年我们还协助在 NeurIPS 组织了五项挑战赛：

- Billion-scale approximate nearest neighbor search challenge（十亿级近似最近邻搜索挑战赛）
- IGLU: Interactive grounded language understanding in a collaborative environment（协作环境中的交互式接地语言理解）
- The Image Similarity Challenge（图像相似性挑战赛）
- The NetHack Challenge（NetHack 挑战赛）
- Open Catalyst Challenge（开放催化剂挑战赛）

Meta AI 研究者还参与组织了六个研讨会：

- Cooperative AI workshop（合作 AI 研讨会）
- Data-centric AI workshop（以数据为中心的 AI 研讨会）
- Machine learning for creativity and design（面向创意与设计的机器学习）
- Privacy in machine learning（机器学习中的隐私）
- Self-supervised learning — theory and practice（自监督学习——理论与实践）
- Workshop on ML for systems（面向系统的机器学习研讨会）

## 以新研究推进最先进水平

下面我们按大致分为四个主题展示 Meta AI 在 NeurIPS 上的一些研究亮点：具身智能体与高效探索、语音与 NLP、从视觉数据理解世界，以及生成模型与表示学习基础。Meta AI 被接收论文的完整列表可在此处获取。

### 具身智能体与高效探索

（原文此处嵌入视频。）

强化学习（RL）智能体通过与环境交互来学习——环境通常是模拟的真实世界空间，以便更快速、安全、高效地进行试验。我们在这一主题下的贡献包括 Habitat 2.0——一个新的 3D 照片级仿真平台，智能体既可以在其中穿行环境，也可以与物体交互。我们的工作还涉及多种设定下高效探索的基本问题，例如在没有特定任务时使用新颖的内在奖励、目标是到达特定状态的设定，以及每步或每次仿真都可能昂贵的设定。

- Habitat 2.0（论文、博客文章）
- Interesting object, curious agent（口头报告，第 5 分会：RL 与规划，12 月 10 日周五）
- Stochastic shortest path: Minimax, parameter-free and towards horizon-free regret
- A provably efficient sample collection strategy for reinforcement learning

### 语音与 NLP

（原文此处嵌入视频。）

监督学习——从标注数据中学习——在 AI 的大多数领域提供了最先进的性能。然而人类在很大程度上是通过观察来学习关于世界的准确预测模型，无需标注样本。此外，获取人工数据标注耗时、易错且消耗资源。获取大量标注数据尤其成为在所谓低资源语言上训练语音识别模型的能力限制因素——这些语言没有充裕的、带有对应转写并已对齐文本的音频可用。我们在这一主题下的工作提出了无需转写数据训练语音识别模型的新方法、不区分语言地学习语音与文本的公共嵌入，以及扩展大型稀疏专家混合（MoE）模型的新方法——将输入自动路由到最合适的子系统。

其中包括一种无需转写数据即可训练语音识别模型的新方法，使得在当前没有或极少转写数据的许多语言上训练模型成为可能。我们还在先前 LASER 工作的基础上，提出一种将语音和文本嵌入到公共表示空间的新方法，使相关句子彼此接近，而无论输入是语音还是文本、来自哪种语言。新的嵌入开启了许多可能性，包括大规模语音到文本、甚至语音到语音挖掘，而无需先转写再翻译转写文本。

- Unsupervised speech recognition（无监督语音识别，口头报告，第 3 分会：深度学习，12 月 8 日周三）
- Multimodal and multilingual embeddings for large-scale speech mining（面向大规模语音挖掘的多模态多语言嵌入）

规模也一直是推动自然语言处理最先进水平的主要因素。我们在 Hash Layers 上的工作表明，通过对输入词元进行确定性哈希以将输入路由到专家，可以构建大规模、高性能的专家混合网络。与当前最先进的方法（使用学习将输入通过专家混合进行路由的模型）相比，我们的方法表现更佳。

- Hash layers for large sparse models（面向大型稀疏模型的哈希层）

### 从视觉数据理解世界

我们的 VolSDF 模型可以接收一组输入图像（左），学习由符号距离函数定义的体积密度（中左，切片图），并生成神经渲染（右）。这种密度定义有助于高质量的几何重建（中间灰色表面）。原始图像来自 BlendedMVS 数据集，采用知识共享署名 4.0 许可证。

从视觉数据（如图像或视频）理解世界仍是研究社区的一项关键挑战。视觉 Transformer 架构为涉及视觉数据的应用提供了一种强大的新归纳偏置，是卷积神经网络的泛化。我们提出了用于图像分割以及视频中跟踪与动作识别的新 transformer 模型。MaskFormer 模型在语义分割和全景分割上同时达到最先进的准确率。轨迹注意力（trajectory attention）在多个基准上的动作识别中达到最先进的准确率。虽然图像和视频等模态并不显式捕捉 3D 信息，但越来越多的视觉技术受益于利用世界的 3D 结构。例如，我们引入了一种名为 SEAL 的自监督新方法，通过在物理环境中移动来联合改进目标检测和实例分割模型。我们还引入了一种名为 VolSDF 的新技术，利用新颖的神经渲染技术从一组图像构建 3D 模型。

- Per-pixel classification is not all you need for semantic segmentation（语义分割并非只需逐像素分类）
- Keeping your eye on the ball（口头报告，第 3 分会：视觉应用，12 月 8 日周三）
- SEAL: Self-supervised embodied active learning（SEAL：自监督具身主动学习）
- Volume rendering of neural implicit surfaces（神经隐式曲面的体渲染，口头报告，第 3 分会：视觉应用，12 月 8 日周三）

### 生成模型与表示学习基础

以左图所示图像及类别标签为条件时，IC-GAN 生成了右侧的图像。

创造从未见过的新内容的能力，是通往人类水平智能道路上的重要一步。在实例条件 GAN（instance-conditioned GAN）的工作中，我们引入了一个新的可控生成模型家族，以另一幅图像的表示（可能还有类别标签）为条件生成新图像。这种额外的控制层次使我们能够生成远离模型训练图像分布的图像。我们还引入了一种新颖的计算高效的连续归一化流——Moser Flow，使得学习具有复杂几何结构的分布成为可能。

- IC-GAN（论文、博客文章）
- Moser Flow: Divergence-based generative modeling on manifolds（基于散度的流形生成建模，口头报告，第 5 分会：生成建模，12 月 10 日周五）。该工作获得了杰出论文奖。

大多数有损图像压缩方法（如 JPEG）旨在减少存储图像所需的比特数，同时不影响人类感知的视觉质量。我们引入了一种新的学习式压缩技术，可以显著减少存储图像所需的比特数（例如少用 1000 倍的比特），而不影响下游模型对图像内容进行分类的能力。

- Lossy compression for lossless prediction（面向无损预测的有损压缩）

我们的研究者将在相应的海报前分享更多工作并回答问题。我们也邀请你到 Gather.Town 上的 Meta AI 展区，与研究者和招聘人员交流。
