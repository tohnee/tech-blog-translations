---
title: "DINOv2：无监督学习稳健视觉特征"
title_en: "DINOv2: Learning Robust Visual Features without Supervision"
arxiv: 2304.07193
date: 2023-04-14
source: https://arxiv.org/abs/2304.07193
crawled: 2026-09-22
translated: 2026-09-22
---

# DINOv2：无监督学习稳健视觉特征

> 原文：[DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193) · Meta AI（FAIR）arXiv

Maxime Oquab**、Timothée Darcet**、Théo Moutakanni**、Huy V. Vo*、Marc Szafraniec*、Vasil Khalidov*、Pierre Fernandez、Daniel Haziza、Francisco Massa、Alaaeldin El-Nouby、Mahmoud Assran、Nicolas Ballas、Wojciech Galuba、Russell Howes、Po-Yao Huang、Shang-Wen Li、Ishan Misra、Michael Rabbat、Vasu Sharma、Gabriel Synnaeve、Hu Xu、Hervé Jegou、Julien Mairal、Patrick Labatut*、Armand Joulin*、Piotr Bojanowski*

Meta AI Research　　Inria
*核心团队　　**同等贡献

###### 摘要

自然语言处理领域在大量数据上进行模型预训练的近期突破，为计算机视觉中出现类似的基座模型（foundation model）铺平了道路。
这类模型可以通过产生通用视觉特征——即无需微调即可跨图像分布、跨任务使用的特征——极大地简化图像在任何系统中的使用。
本工作表明，现有的预训练方法，尤其是自监督方法，只要在来自多样化来源、经过充分筛选（curated）的足够规模数据上训练，就能产生这样的特征。
我们重新审视了现有方法，并组合多种技术，从数据和模型规模两个维度扩展我们的预训练。
大多数技术贡献的目标是在规模化训练时加速并稳定训练过程。
在数据方面，我们提出一条自动化流水线来构建一个专用、多样化且经过筛选的图像数据集，而非自监督文献中通常使用的未筛选（uncurated）数据。
在模型方面，我们训练了一个拥有 10 亿参数的 ViT 模型（Dosovitskiy et al., 2021），并将其蒸馏为一系列更小的模型，这些模型在图像级和像素级的大多数基准上都超越了目前可用的最佳通用特征 OpenCLIP（Ilharco et al., 2021）。

OpenReview 评审页面：<https://openreview.net/forum?id=a68SUt6zFt>

脚注：除 Julien Mairal 隶属 Inria 外，所有作者均隶属 Meta。
Timothée Darcet 与 Pierre Fernandez 同时隶属于 Inria。
Théo Moutakanni 同时隶属于 Université Paris Saclay。
Alaaeldin El-Nouby 同时隶属于 Inria 与 ENS-PSL。
联系方式：{qas, timdarcet, theomoutakanni, ajoulin, bojanowski}@meta.com

## 1 引言

学习与任务无关的预训练表示已成为自然语言处理（NLP）的标准做法（Radford et al., 2019；Raffel et al., 2020；Chowdhery et al., 2022；Hoffmann et al., 2022；Touvron et al., 2023）。
我们可以「原样」使用这些特征，即无需微调，在下游任务上取得显著优于任务专用模型的性能（Brown et al., 2020）。
这一成功得益于在大量原始文本上使用前置目标（pretext objective）进行预训练，例如语言建模（Radford et al., 2017）或词向量（Devlin et al., 2019），它们无需任何监督。

追随 NLP 中这一范式转变，我们期待类似的「基座」模型出现在计算机视觉领域（Bommasani et al., 2021）。
这些模型应当生成能够开箱即用于任何任务的视觉特征，无论是图像级任务（如图像分类），还是像素级任务（如分割）。
朝着这类基座模型的最有希望的努力集中在文本引导的预训练上，即使用某种形式的文本监督来引导特征的训练（Joulin et al., 2016；Mahajan et al., 2018；Radford et al., 2021）。
这种文本引导的预训练形式限制了图像所能保留的信息，因为字幕（caption）只能近似图像中丰富的信息，复杂的像素级信息可能无法在这种监督下浮现。
此外，这类图像编码器需要对齐的文本-图像语料库，因此不具备其文本对应物的灵活性——即仅从原始数据中学习的能力。

![图 1](2304.07193v2/new-figure-1.jpg)

图 1：
首个 PCA 分量的可视化。我们在来自同一列（a、b、c、d）图像的图块（patch）之间计算 PCA，并展示前 3 个分量。
每个分量对应一个不同的颜色通道。
尽管姿态、风格甚至物体发生变化，相关图像之间的相同部位仍被匹配对应。
背景通过对第一个 PCA 分量设置阈值而去除。

文本引导预训练的一种替代方案是自监督学习（Caron et al., 2018；Chen et al., 2020；He et al., 2022），其中特征仅从图像中学习。
这些方法在概念上更接近语言建模等前置任务，并且能够同时捕获图像级和像素级信息（Caron et al., 2021）。
此外，自监督模型输出的特征已被证明具有多种有用的性质，并催生了广泛的应用（Amir et al., 2022；Tumanyan et al., 2022；Ofri-Amar et al., 2023；Hamilton et al., 2022）。
然而，尽管具有学习通用特征的潜力，自监督学习的大多数进展是在一个较小的筛选数据集 ImageNet-1k（Russakovsky et al., 2015）上预训练的背景下取得的。
也曾有一些将这些方法扩展到 ImageNet-1k 之外的努力（Caron et al., 2019；Goyal et al., 2021；Goyal et al., 2022a），但它们聚焦于未筛选数据集，而后者通常会导致特征质量的显著下降。
其原因在于无法控制数据质量和多样性，而这两者正是产生良好特征的关键。

在本工作中，我们探索自监督学习在大规模筛选数据上预训练时是否具有学习通用视觉特征的潜力。
我们重新审视了现有的在图像级和图块级同时学习特征的判别式自监督方法，例如 iBOT（Zhou et al., 2022a），并在更大数据集的视角下重新考虑它们的某些设计选择。
我们的大部分技术贡献都着眼于在模型规模和数据规模扩大时稳定并加速判别式自监督学习。
这些改进使我们的方法比类似的判别式自监督方法快约 2×，所需内存减少 3×，使我们能够以更大的批大小进行更长时间的训练。

关于预训练数据，我们构建了一条自动化流水线，从海量未筛选图像集合中筛选并再平衡数据集。
该流水线的灵感来自 NLP 中的流水线（Wenzek et al., 2020），其中使用数据相似度而非外部元数据，也不需要人工标注。
处理野外图像时的一个主要困难是对概念进行再平衡，避免在少数主导模式上过拟合。
在本工作中，一种朴素的聚类方法就能相当好地解决这一问题。
我们收集了一个规模不大但多样的语料库，包含 1.42 亿张图像，以验证我们的方法。

最后，我们提供了一系列预训练视觉模型，称为 DINOv2，使用不同的 Vision Transformer（ViT）（Dosovitskiy et al., 2016）架构在我们的数据上训练。
我们发布了所有模型以及可在任意数据上重训 DINOv2 的代码。
随着规模扩大，我们在图像级和像素级的多种计算机视觉基准上验证了 DINOv2 的质量，如图 2 所总结。
我们的结论是：仅凭自监督预训练，就是学习可迁移冻结特征的一个良好候选，其性能可与最佳的公开可用弱监督模型竞争。

## 2 相关工作

##### 图像内自监督训练。

第一类自监督方法聚焦于从图像本身构建前置任务，即从图像中提取一个由图像其余部分来预测的信号。
这一思想随着 Doersch et al.（2015）的工作而流行，他们通过预测给定图块的上下文来进行训练。
基于类似思路，人们还提出了许多其他前置任务，例如图像重着色（Zhang et al., 2016）、预测变换（Gidaris et al., 2018）、图像修补/ inpainting（Pathak et al., 2016）或图块重排序（Noroozi & Favaro, 2016；Misra & Maaten, 2020）。
近来，基于图块的架构（如 ViT）的兴起促使人们重新审视用于预训练的 inpainting（He et al., 2022；Bao et al., 2021；El-Nouby et al., 2021），并可能在特征空间中进行（Assran et al., 2023；Baevski et al., 2022）。
尤其值得关注的是，He et al.（2022）表明掩码自编码器（MAE）学到的特征在下游任务上微调后能带来实质性的提升。
MAE 的这一性质已在视频（Tong et al., 2022）、音频（Xu et al., 2022）以及其他模态（Girdhar et al., 2023）上得到进一步验证。
然而，它们的特征需要有监督的微调，而我们的特征可以直接开箱即用。

图 2：
参数规模扩大时的性能演变。
我们展示了第 7 节所述八类视觉任务上的性能，并对每类任务的指标取平均。
特征从我们的自监督编码器 DINOv2（深蓝）中提取，并与自监督方法（浅橙）以及弱监督方法（深粉）进行比较。
我们以水平虚线报告表现最佳的弱监督模型的性能。
我们的模型家族大幅超越了此前自监督学习的最高水平，并达到与弱监督特征相当的性能。
详细分析见第 7 节。

##### 判别式自监督学习。

第二类与我们的工作更接近的路线是利用图像之间或图像组之间的判别信号来学习特征。
这类方法的根源可追溯到早期深度学习工作（Hadsell et al., 2006），但随着实例分类方法（Dosovitskiy et al., 2016；Bojanowski & Joulin, 2017；Wu et al., 2018）的兴起而流行。
后续基于实例级目标（Hénaff et al., 2019；He et al., 2020；Chen & He, 2021；Chen et al., 2020；Grill et al., 2020；Caron et al., 2021）或聚类（Caron et al., 2018；Asano et al., 2020；Caron et al., 2020）提出了若干改进。
这些方法在 ImageNet（Russakovsky et al., 2015）等标准基准上提供了高性能的冻结特征，但难以扩展到更大的模型规模（Chen et al., 2021）。
在本工作中，我们在大规模预训练数据集和模型的背景下重新审视这些方法的训练。
特别地，我们以 Zhou et al.（2022a）为基础，我们发现它特别适合规模化。

##### 自监督预训练的扩展。

越来越多的工作关注自监督学习在数据和模型规模上的扩展能力（Caron et al., 2019；Goyal et al., 2019；Tian et al., 2021；Goyal et al., 2022a）。
这些工作大多使用大量未筛选数据来无监督地训练模型。
它们提供的证据表明判别式方法可以随数据扩展，但由于预训练数据质量较差，大多数结果需要通过微调特征才能获得。
尤其值得关注的是，Goyal et al.（2021）还表明，在预训练数据充足的情况下，这些方法也能从模型规模的扩大中受益。
这条工作路线质疑自监督方法在任意数据上运作的能力，而我们则专注于产出最佳的预训练编码器。

##### 自动数据筛选。

我们的数据集构建借鉴了图像检索社区（Weinzaepfel et al., 2021；Radenović et al., 2018b；Berman et al., 2019；Douze et al., 2009；Tolias et al., 2016；Revaud et al., 2019）。
特别地，在半监督学习的语境下，使用检索来增强训练集已被研究过（Yalniz et al., 2019）。
类似地，也有人使用标签（hashtag）或其他元数据（Mahajan et al., 2018；Radford et al., 2021）或预训练视觉编码器（Schuhmann et al., 2021；Schuhmann et al., 2022）来过滤未筛选数据集。
与这些工作不同，我们在过滤图像时不使用任何预训练编码器、元数据或监督，而是利用图像之间的视觉相似性。
我们的方法受文本筛选流水线（Wenzek et al., 2020）启发，其中在 Wikipedia 上训练一个语言模型来为从未筛选来源提取的文本打分。

## 3 数据处理

我们通过从一个大型未筛选数据池中检索与若干筛选数据集中图像相近的图像，构建了经过筛选的 LVD-142M 数据集。
下面我们描述数据流水线的主要组成部分，包括筛选/未筛选数据来源、图像去重步骤以及检索系统。
我们的流水线不需要任何元数据或文本，直接作用于图像，如图 3 所示。
关于我们方法的更多细节，请读者参阅附录 A。

![图 3](2304.07193v2/LaViDa_datapipeline_figure.png)

图 3：
我们的数据处理流水线概览。
来自筛选与未筛选数据来源的图像首先被映射为嵌入。
未筛选图像随后被去重，再与筛选图像进行匹配。
最终组合通过自监督检索系统扩充初始数据集。

数据来源。
我们对筛选数据集的选择详见附录（表 15），包括 ImageNet-22k、ImageNet-1k 的训练集、Google Landmarks 以及若干细粒度数据集。
对于未筛选数据来源，我们从一个公开可用的爬取网页数据仓库中收集了一个原始未过滤的图像数据集。
从该仓库中的每个网页，我们从 <img> 标签中提取图像的 URL 链接。
我们丢弃不安全或受域名限制的 URL，并对下载的图像进行后处理（PCA 哈希去重、NSFW 过滤以及模糊可识别人脸）。
这产生了 12 亿张唯一图像。

去重。
我们对未筛选数据应用 Pizzi et al.（2022）的副本检测流水线，并移除近似重复的图像。
这减少了冗余并提高了图像之间的多样性。
我们还移除了与本文所用任何基准的测试集或验证集中图像近似重复的图像。

自监督图像检索。
我们通过从未筛选数据来源中检索与筛选来源图像相近的图像，来构建经过筛选的预训练数据集。
为此，我们首先使用一个在 ImageNet-22k 上预训练的自监督 ViT-H/16 网络计算图像嵌入，并使用余弦相似度作为图像之间的距离度量。
然后，我们对未筛选数据执行 k-means 聚类。
给定一个用于检索的查询数据集，如果它足够大，我们为每张查询图像检索 NN（通常为 4）个最近邻。
如果它较小，我们从每张查询图像对应的簇中采样 MM 张图像。
尽管目视检查表明 NN 取远大于 4 时检索质量似乎不错，但这会导致更多冲突（即同一图像是多个查询的最近邻检索结果）。我们选择 N=4，因为它在此意义上提供了良好的折中。

实现细节。
我们流水线的去重和检索阶段依赖 Faiss 库（Johnson et al., 2019）来高效索引并批量搜索最近邻嵌入。
特别地，我们大量利用其对 GPU 加速索引的支持，使用带乘积量化编码的倒排文件索引（Jegou et al., 2010）。
整个处理分布在一个由 20 个节点组成的计算集群上，每个节点配备 8 块 V100-32GB GPU，产出 LVD-142M 数据集耗时不到两天。

## 4 判别式自监督预训练

我们使用一种判别式自监督方法来学习特征，该方法可以视为 DINO 与 iBOT 损失的组合，外加 SwAV 的中心化操作（Caron et al., 2020）。
我们还添加了一个用于分散特征的正则项，以及一个短暂的高分辨率训练阶段。
我们快速介绍这些方法中的每一种，更多细节可参见相关论文或我们的开源代码。

- 图像级目标（Caron et al., 2021）。
  我们考虑从学生网络和教师网络提取的特征之间的交叉熵损失。
  两个特征都来自 ViT 的 class token，由同一图像的不同裁剪得到。
  我们将学生 class token 送入学生 DINO 头。
  该头是一个 MLP 模型，输出一个分数向量，我们称之为「原型分数（prototype scores）」。
  然后我们应用 softmax 得到 $p_{s}$。
  类似地，我们对教师 class token 应用教师 DINO 头得到教师原型分数。
  然后我们应用 softmax，随后进行移动平均中心化（或如下文详述的 Sinkhorn-Knopp 中心化），得到 $p_{t}$。
  DINO 损失项为：

  $$\mathcal{L}_{DINO}=-\sum p_{t}\log p_{s}$$

  我们学习学生的参数，并用过去迭代值的指数移动平均构建教师头（He et al., 2020）。

- 图块级目标（Zhou et al., 2022a）。
  我们随机掩码送给学生的部分输入图块，但不掩码送给教师的。
  然后我们对学生的 mask token 应用学生 iBOT 头。
  类似地，我们对与学生在被掩码位置对应的（可见）教师图块 token 应用教师 iBOT 头。
  然后我们如上所述应用 softmax 和中心化步骤，得到 iBOT 损失项：

  $$\mathcal{L}_{iBOT}=-\sum_{i}p_{ti}\log p_{si}$$

  其中 $i$ 是被掩码 token 的图块索引。
  与上面类似，我们学习学生的参数，并通过指数移动平均构建教师头。

- 解绑两个目标之间的头权重。
  DINO 损失和 iBOT 损失都使用一个可学习的 MLP 投影头。
  它作用于输出 token，损失在其上计算。
  在 Zhou et al.（2022a）中，一项消融研究表明 DINO 头与 iBOT 头共享参数会带来更好的性能。
  而在规模化场景下，我们观察到情况恰恰相反，因此我们在所有实验中使用两个独立的头。

- Sinkhorn-Knopp 中心化（Caron et al., 2020）。
  Ruan et al.（2023）建议将 DINO 和 iBOT 的教师 softmax 中心化步骤替换为 SwAV 的 Sinkhorn-Knopp（SK）批归一化（Caron et al., 2020）。
  我们运行 Sinkhorn-Knopp 算法步骤 3 次迭代。
  对学生，我们应用 softmax 归一化。

- KoLeo 正则项（Sablayrolles et al., 2019）。
  KoLeo 正则项源自 Kozachenko-Leonenko 微分熵估计器（见 Beirlant et al., 1997；Delattre & Fournier, 2017），它促使特征在一个批次内均匀铺展（span）。
  给定一组 $n$ 个向量 $(x_{1},\dots,x_{n})$，其定义为

  $$\mathcal{L}_{\mathrm{koleo}}=-\frac{1}{n}\sum_{i=1}^{n}\log(d_{n,i}),$$

  其中 $d_{n,i}=\min_{j\neq i}\|x_{i}-x_{j}\|$ 是 $x_{i}$ 与批内任何其他点之间的最小距离。
  我们在计算该正则项之前还对特征做 $\ell_{2}$ 归一化。

- 适配分辨率（Touvron et al., 2019）。
  提高图像分辨率对分割或检测等像素级下游任务至关重要，因为小目标在低分辨率下会消失。
  然而，高分辨率训练耗时且耗内存，因此我们改为在预训练末尾的一小段时间内将图像分辨率提高到 518×518。这也类似于 Likhomanenko et al.（2021）的 UniViT 训练和 Beyer et al.（2023）的 FlexiViT 训练。

## 5 高效实现

我们考虑若干改进以在更大规模上训练模型。
我们在 A100 GPU 上使用 PyTorch 2.0 训练模型。
代码和预训练模型以 Apache 2.0 许可证发布¹（<https://github.com/facebookresearch/dinov2>）。
我们模型的细节见附录表 17。在相同硬件上，与 iBOT 实现相比，DINOv2 代码运行速度快约 2×，而内存占用仅为 1/3。

##### 快速且省内存的注意力。

我们实现了自己的 FlashAttention 版本（Dao et al., 2022），以改善自注意力层的内存占用和速度。
在所有考虑的场景中，我们的版本与原版持平或更优，同时覆盖更多用例和硬件。
由于 GPU 硬件特性，当每个头的嵌入维度是 64 的倍数时效率最佳，而当完整嵌入维度是 256 的倍数时矩阵运算效果更佳。
因此，我们的 ViT-g 架构与 Zhai et al.（2022）提出的架构略有不同，以最大化计算效率：我们使用嵌入维度 1536、24 个头（每头 64 维），而不是 1408、16 个头（每头 88 维）。我们的实验未显示最终精度上的显著差异，我们的 ViT-g 主干拥有 11 亿参数。

##### 序列打包（Sequence packing）。

DINO 算法需要同时前向传播大裁剪（分辨率 224）和小裁剪（分辨率 98）。
切分成图块后，这两组由不同长度的 token 序列表示，无法一起前向传播。
为了加速训练，我们使用一个源自 NLP 的技巧，称为「序列打包」（Krell et al., 2022）。
想法很简单：我们把需要通过 transformer 前向传播的序列拼接成一条长序列。
我们照常将这条序列送入 transformer 块。
但在注意力层中对自注意力矩阵应用块对角掩码，阻止不同序列之间的注意力。
这样，该前向传播严格等价于分别前向传播每条序列。
与以往实现中使用分离的前向和反向传播相比，这一技巧带来了显著的计算效率提升。
我们设置中更底层的组件已在 xFormers 库²（<https://github.com/facebookresearch/xformers>）（Lefaudeux et al., 2022）中开源。

##### 高效随机深度。

我们实现了一个改进版的随机深度（stochastic depth，Huang et al., 2016），它直接跳过被丢弃残差的计算，而不是对结果做掩码。
借助特定的融合核（fused kernel），这按与丢弃率近似相等的比例节省内存和计算。
在高丢弃率下（本工作中 $d=40\%$），这带来了计算效率和内存使用的极大改善。
具体实现是将批维度上的 $B$ 个样本随机打乱，然后切出前 $(1-d)\times B$ 个样本用于该块中的计算。

##### 完全分片数据并行（FSDP）。

使用 AdamW 优化器最小化我们的目标需要 4 份 float32 精度的模型副本——学生、教师、优化器一阶矩、优化器二阶矩。
对于像我们 ViT-g 这样的十亿参数模型，总计约 16 GB 内存。
为了减少每块 GPU 的内存占用，我们跨 GPU 切分模型副本，即使用 PyTorch 的 FSDP 实现将 16 GB 分片到各 GPU 上。
因此，模型规模的限制不再是单块 GPU 的内存，而是计算节点上 GPU 内存的总和。
PyTorch 的 FSDP 实现还带来第二个优势，即节省跨 GPU 通信成本：权重分片按优化器要求以 float32 精度存储，但权重的广播和梯度的归约（reduce）对主干以 float16 精度进行（MLP 头的梯度以 float32 归约以避免训练不稳定）。
与 DistributedDataParallel（DDP）中使用的 float32 梯度 all-reduce 操作相比，这使通信成本降低约 50%，而其他自监督预训练方法（Caron et al., 2021；Zhou et al., 2022a）使用的是后者。
因此，在扩展 GPU 节点数量时，我们的训练过程比使用 float16 autocast 的 DDP 扩展得更高效。
总体而言，在我们遇到的几乎所有场景中，PyTorch-FSDP 混合精度都优于带 autocast 的 DDP。

##### 模型蒸馏。

我们对训练循环的大部分技术改进都着眼于改善大模型在大数据量上的训练。
对于较小的模型，我们不是从零训练，而是从最大的模型 ViT-g 蒸馏得到。
知识蒸馏（Hinton et al., 2014）旨在用一个较小的模型复现一个大模型的输出，方法是最小化两者在一组给定输入上输出的某种距离。
由于我们的目标函数本身就是一种从教师网络到学生网络的蒸馏形式，我们沿用同一个训练循环，仅有以下几点例外：
我们使用一个更大的模型作为冻结教师；保留学生的一个备用 EMA 作为最终模型；移除掩码和随机深度；并将 iBOT 损失应用于两个全局裁剪。
在我们的消融实验中，我们观察到该方法比从零训练取得更好的性能，即使对 ViT-L 也是如此。
我们的蒸馏方法最终与 Duval et al.（2023）描述的方法接近，不同之处在于我们不修改蒸馏用的损失项，并评估学生的 EMA。

## 6 消融研究

我们给出一组消融实验，以实证验证流水线的不同组件：
第 4 节描述的技术改动、预训练数据以及模型蒸馏的影响。
我们考虑第 7 节中描述的各种下游任务。

### 6.1 改进的训练配方

我们的方法通过将 iBOT 与第 4 节描述的若干现有组件相结合，对其进行了改进。
为评估这些组件的重要性，我们训练了多个模型，在基线 iBOT 模型上依次添加组件。
我们在表 1 中报告 ImageNet-1k 验证集上 k-NN 与线性探测（linear probe）的 Top-1 准确率。
总体而言，我们观察到每个组件都能提升 k-NN 或线性探测（多数情况下两者）的性能。
只有 LayerScale 和随机深度会带来线性探测的性能下降，但根据我们的经验，它们能显著改善训练稳定性。

| 配置 | INet-1k k-NN | INet-1k 线性 |
| --- | --- | --- |
| iBOT | 72.9 | 82.3 |
| +（我们的复现） | 74.5（↑1.6） | 83.2（↑0.9） |
| +LayerScale、随机深度 | 75.4（↑0.9） | 82.0（↓1.2） |
| +128k 原型 | 76.6（↑1.2） | 81.9（↓0.1） |
| +KoLeo | 78.9（↑2.3） | 82.5（↑0.6） |
| +SwiGLU FFN | 78.7（↓0.2） | 83.1（↑0.6） |
| +图块尺寸 14 | 78.9（↑0.2） | 83.5（↑0.4） |
| +教师动量 0.994 | 79.4（↑0.5） | 83.6（↑0.1） |
| +调整预热日程 | 80.5（↑1.1） | 83.8（↑0.2） |
| +批大小 3k | 81.7（↑1.2） | 84.7（↑0.9） |
| +Sinkhorn-Knopp | 81.7（=） | 84.7（=） |
| +解绑头 = DINOv2 | 82.0（↑0.3） | 84.5（↓0.2） |

表 1：
iBOT 与 DINOv2 训练差异的消融研究。
我们以 k-NN 性能为优化目标，因为根据我们的经验，线性探测性能的下限由 k-NN 性能决定。
某些修改（如 LayerScale 和较高的随机深度，rate=0.4）会导致线性探测性能下降，但具有通过避免训练期间出现 NaN 损失值来提高训练稳定性的好处（Touvron et al., 2022）。
总体而言，这些修改使得后续一系列改进得以叠加。实验使用 ViT-Large 架构在 ImageNet-22k 上进行。

### 6.2 预训练数据来源

特征的质量直接与预训练数据的质量相关。
在本实验中，我们探究 LVD-142M 相对于常用预训练数据集 ImageNet-22k、或直接使用原始未筛选数据的影响。
对于未筛选数据集，我们从与 LVD-142M 相同的数据来源中随机采样 1.42 亿张图像。
我们在每个数据集上以相同迭代次数训练 ViT-g/14。
为完整性起见，我们还纳入一个移除了 ImageNet-1k 同义词集（synset）的 ImageNet-22k 变体（INet-22k ∖ INet-1k）。
比较结果报告在表 2 中。

| 训练数据 | INet-1k | Im-A | ADE-20k | Oxford-M | iNat2018 | iNat2021 | Places205 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| INet-22k | 85.9 | 73.5 | 46.6 | 62.5 | 81.1 | 85.6 | 67.0 |
| INet-22k ∖ INet-1k | 85.3 | 70.3 | 46.2 | 58.7 | 80.1 | 85.1 | 66.5 |
| 未筛选数据 | 83.3 | 59.4 | 48.5 | 54.3 | 68.0 | 76.4 | 67.2 |
| LVD-142M | 85.8 | 73.9 | 47.7 | 64.6 | 82.3 | 86.4 | 67.6 |

表 2：
预训练数据来源的消融。
我们将 iBOT 所用的 INet-22k 数据集与我们的数据集 LVD-142M 进行比较。
每个模型训练相同的迭代次数（小于我们最终运行的规模），且不进行高分辨率适配。
在 LVD-142M 上预训练在 INet-1k 上保持了性能，同时使模型在其他领域表现更好。

最显著的观察是：在大多数基准上，在经过筛选的图像集上训练比在未筛选数据上训练效果更好。
这证实了数据筛选的益处，即便是在自监督预训练的情况下。
与在 ImageNet-22k 上训练的模型相比，在 LVD-142M 上训练在除 ImageNet-1k 之外的所有基准上也更优。
这证实了在更多样化的图像集上训练可以提升 ImageNet-22k 未覆盖领域的特征质量。
我们还看到，在我们的筛选数据上训练提升了未参与筛选过程的领域（INaturalist 2018、2021 和 Places205）的性能，证明规模和多样性可以惠及未见领域。
总体而言，本消融的结论是：我们的数据集在不同类型图像之间提供了良好的平衡，从而带来整体最佳的性能。

### 6.3 模型规模与数据

我们在图 4 中量化了随模型规模扩大而扩展数据的重要性。
随着模型规模增大，在 LVD-142M 上训练变得比在 ImageNet-22k 上训练更有利。
例如，在 LVD-142M 上训练的 ViT-g 在 ImageNet-1k 上追平了在 ImageNet-22k 上训练的模型，同时在其他基准上显著胜出。

图 4：
模型规模与数据规模。
对于两个不同的预训练数据集——ImageNet-22k（1400 万张图像）和 LVD-142M（1.42 亿张图像）——性能随模型规模的变化。
在 LVD-142M 上训练的 ViT-g 在大多数基准上超越了在 ImageNet-22k 上训练的 ViT-g。

### 6.4 损失组件

我们在 6.1 节中通过逐步添加验证了所提出的技术改进。
本节从我们性能最佳的模型出发，分析消融特定损失项所带来的性能损失。
我们消融 KoLeo 损失的重要性和掩码图像建模项的影响。
对于两者，我们报告 ImageNet-1k 上使用线性分类器、ADE-20k 分割使用线性分类器，以及 Oxford-M 上的最近邻图像检索的性能。
表 3(a) 展示了使用 KoLeo 损失的影响。
我们看到实例检索性能提升超过 8%，证实该项有助于在输出空间中分散特征。
与此同时，其他指标并未因这一正则化而受损。
在表 3(b) 中，我们展示了使用 iBOT 掩码图像建模项的影响。
该项对密集预测任务至关重要，可带来近 3% 的性能提升。

| KoLeo | INet-1k | Im-A | ADE-20k | Oxford-M |
| --- | --- | --- | --- | --- |
| ✕ | 85.3 | 70.6 | 47.2 | 55.6 |
| ✓ | 85.8 | 72.8 | 47.1 | 63.9 |

(a) KoLeo 损失

| MIM | INet-1k | Im-A | ADE-20k | Oxford-M |
| --- | --- | --- | --- | --- |
| ✕ | 85.3 | 72.0 | 44.2 | 64.3 |
| ✓ | 85.8 | 72.8 | 47.1 | 63.9 |

(b) iBOT 中的 MIM 目标

表 3：
(a) KoLeo 损失项的影响。
(b) iBOT 掩码图像建模（MIM）损失项的影响。
评估在 ImageNet-{1k,A}（线性探测分类，准确率 %）、ADE-20k（线性层分割，mIoU）和 Oxford-M（图像检索，mAP）上进行。
每个模型训练相同的迭代次数（小于我们最终运行的规模）。
KoLeo 损失项改善最近邻搜索任务（如检索），MIM 损失改善图块级任务（如分割）。

### 6.5 知识蒸馏的影响

对于小型架构，我们对大模型进行蒸馏而非从零训练。
我们使用第 5 节（模型蒸馏小节）描述的蒸馏流程。
我们通过在 12 个基准上比较从零训练的 ViT-L/14 与从 ViT-g/14 蒸馏得到的 ViT-L/14 来评估该方法的有效性，见图 5。
我们还报告了用于蒸馏的 ViT-g/14 的性能作为参考上限（topline）。
蒸馏模型在全部 12 个基准上都优于从零训练的模型，验证了我们针对小模型的预训练方法。

(a) 单项指标比较

| 架构 | 方法 | INet-1k | 分割 | 深度↓ | 分类 |
| --- | --- | --- | --- | --- | --- |
| ViT-g/14 | 从零训练 | 86.5 | 73.4 | 1.00 | 92.1 |
| ViT-L/14 | 从零训练 | 84.5 | 72.2 | 1.10 | 90.2 |
| ViT-L/14 | 蒸馏 | 86.3 | 73.3 | 1.08 | 91.2 |

| 架构 | 方法 | 细粒度 | 检索 | ARSketch | 视频 |
| --- | --- | --- | --- | --- | --- |
| ViT-g/14 | 从零训练 | 78.3 | 75.2 | 77.0 | 69.3 |
| ViT-L/14 | 从零训练 | 75.8 | 71.3 | 69.5 | 67.3 |
| ViT-L/14 | 蒸馏 | 77.6 | 76.3 | 74.5 | 67.5 |

(b) 8 类视觉任务上的平均指标

图 5：
知识蒸馏的有效性。
比较从零训练的 ViT-L 与使用 ViT-g/14 从 DINOv2 蒸馏的 ViT-L。
作为参考，我们还报告 ViT-g/14 教师的性能。我们表明，从冻结 ViT-g 蒸馏的 ViT-L 模型在所有基准上都优于从零训练的同一模型，有时甚至超过蒸馏目标本身。

### 6.6 分辨率的影响

我们测量预训练期间改变分辨率对图像级和图块级特征性能的影响。
我们考虑使用固定分辨率 224×224 或 416×416 从零训练的模型，以及先以 224×224 从零训练、再以 416×416 继续训练 10k 次迭代的模型。
高分辨率训练计算开销大，因此我们在一个小型设置上进行本消融：在 ImageNet1k 上训练的 ViT-L/16。
在图 6 中，我们报告了在 ImageNet-1k 和 ADE-20k 上线性探测、以不同分辨率评估的性能。
在高分辨率图像上训练的模型在各分辨率下表现最佳，但代价高昂：在 416 上训练的计算强度约为在 224 上训练的 3×。
另一方面，仅在训练末尾以高分辨率训练 10k 次迭代几乎同样好，而只需一小部分计算量。
因此，我们在训练末尾加入这一步骤，而不是从一开始就以高分辨率训练。

图 6：
分辨率的作用。
在固定分辨率（「224」与「416」）下训练、或先以 224 训练再短时间以 416 训练（「224→416」）的 ViT-L/16 在 ImageNet-1k 上的性能。
我们在冻结特征上以不同分辨率训练线性分类器，并报告 ImageNet 上的 Top-1 准确率和 ADE-20k 上的 mIoU。我们观察到，短时间的高分辨率 SSL 训练即可取得与全程高分辨率训练接近的行为和结果，而代价只是一小部分。

## 7 结果

在本节中，我们展示我们的模型在许多图像理解任务上的实证评估。
我们同时评估全局和局部图像表示，涵盖类别级与实例级识别、语义分割、单目深度估计以及动作识别。
我们在附录 C 中详列基准清单。
这项评估的目标有二。
首先，我们展示我们的自监督特征以很大幅度超越了当前最高水平。
其次，我们展示它们在大量任务上追平或超越弱监督特征的性能。

基线。
在我们的比较中，我们使用两类模型作为基线。
我们与公开可用的性能最佳的自监督模型进行比较。
首先，我们对 MAE（He et al., 2022）、DINO（Caron et al., 2021）、SEERv2（Goyal et al., 2022a）、MSN（Assran et al., 2022）、EsViT（Li et al., 2022a）、Mugs（Zhou et al., 2022b）和 iBOT（Zhou et al., 2022a）运行我们的评估。
当某一方法提出了多种架构变体时，我们报告在 ImageNet-1k 上取得最佳 top-1 准确率的那个。
其次，我们报告开源弱监督模型的性能，如 CLIP（Radford et al., 2021）、OpenCLIP（Ilharco et al., 2021；Cherti et al., 2023）和 SWAG（Singh et al., 2022）。
在 ImageNet-1k 上评估模型时，我们报告上述每种方法的性能。
对于所有其他评估，我们报告自监督模型中表现最好的四个。
另外，作为参考，弱监督模型中我们报告表现最佳的 OpenCLIP-G。

### 7.1 ImageNet 分类

作为第一项评估，我们在 ImageNet-1k 分类数据集上探究模型产生的整体图像表示的质量。
我们通过在冻结主干上训练一个简单分类器来评估特征质量，不对主干权重做微调。
沿用先前工作，为简单起见我们使用线性模型，以确保评估可复现，尽管各类别可能并非线性可分。
由于大多数 SSL 方法的开发以 ImageNet-1k 验证性能作为调试信号，我们还报告 ImageNet-ReaL 和 ImageNet-V2 上的 top-1 准确率。
为了报告这些额外验证集上的性能，所有模型均用我们的代码运行评估。
我们在表 4 中将我们的冻结特征与最佳的公开可用 SSL 特征进行比较，不论架构或预训练数据如何。
我们看到，本工作提出的组件在线性评估上较此前最高水平（在 ImageNet-22k 上训练的 iBOT ViT-L/16）带来了非常显著的提升（+4.2%）。
同时，我们还看到我们的方法在替代测试集上的性能增幅更大，表明更强的泛化能力。线性评估的细节见附录 B.3。

| 方法 | 架构 | 数据 | 文本监督 | kNN val | 线性 val | ReaL | V2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 弱监督 | | | | | | | |
| CLIP | ViT-L/14 | WIT-400M | ✓ | 79.8 | 84.3 | 88.1 | 75.3 |
| CLIP | ViT-L/14<sub>336</sub> | WIT-400M | ✓ | 80.5 | 85.3 | 88.8 | 75.8 |
| SWAG | ViT-H/14 | IG3.6B | ✓ | 82.6 | 85.7 | 88.7 | 77.6 |
| OpenCLIP | ViT-H/14 | LAION-2B | ✓ | 81.7 | 84.4 | 88.4 | 75.5 |
| OpenCLIP | ViT-G/14 | LAION-2B | ✓ | 83.2 | 86.2 | 89.4 | 77.2 |
| EVA-CLIP | ViT-g/14 | custom* | ✓ | 83.5 | 86.4 | 89.3 | 77.4 |
| 自监督 | | | | | | | |
| MAE | ViT-H/14 | INet-1k | ✕ | 49.4 | 76.6 | 83.3 | 64.8 |
| DINO | ViT-S/8 | INet-1k | ✕ | 78.6 | 79.2 | 85.5 | 68.2 |
| SEERv2 | RG10B | IG2B | ✕ | – | 79.8 | – | – |
| MSN | ViT-L/7 | INet-1k | ✕ | 79.2 | 80.7 | 86.0 | 69.7 |
| EsViT | Swin-B/W=14 | INet-1k | ✕ | 79.4 | 81.3 | 87.0 | 70.4 |
| Mugs | ViT-L/16 | INet-1k | ✕ | 80.2 | 82.1 | 86.9 | 70.8 |
| iBOT | ViT-L/16 | INet-22k | ✕ | 72.9 | 82.3 | 87.5 | 72.4 |
| DINOv2 | ViT-S/14 | LVD-142M | ✕ | 79.0 | 81.1 | 86.6 | 70.9 |
| DINOv2 | ViT-B/14 | LVD-142M | ✕ | 82.1 | 84.5 | 88.3 | 75.1 |
| DINOv2 | ViT-L/14 | LVD-142M | ✕ | 83.5 | 86.3 | 89.5 | 78.0 |
| DINOv2 | ViT-g/14 | LVD-142M | ✕ | 83.5 | 86.5 | 89.6 | 78.4 |

表 4：
冻结预训练特征在 ImageNet-1k 上的线性评估。
我们报告在公开或私有数据上训练、带或不带文本监督（文本监督）的公开可用模型在验证集上的 Top-1 准确率。作为参考，我们还报告验证集上的 kNN 性能。
我们跨所有可能架构（Arch.）进行比较，除特别说明外分辨率均为 224×224。
EVA-CLIP 训练所用的数据集是一个自定义混合，详见论文（Fang et al., 2023）。

##### 我们距离弱监督模型还有多远？

我们还想验证我们的特征与最先进开源弱监督模型相比具有竞争力。
为此，我们在 ImageNet-1k 上使用线性评估，与三种开箱即用方法及其多个架构变体进行比较。
对于所有模型，在确认我们的数字与技术报告和论文中报告的一致后，我们使用我们的代码运行线性评估。
评估结果展示在表 4 中。
我们看到，我们的主干超越了 ViT-G/14 架构的 OpenCLIP（+0.3%）和 ViT-g/14 的 EVA-CLIP（+0.1%）。
同时，我们还观察到我们在 ImageNet-V2 测试集上的性能显著更好（相较 EVA-CLIP +1.1%），表明更好的泛化能力。
在本节其余部分，我们报告 OpenCLIP-G 作为弱监督模型的参考。

##### 可以微调这些编码器吗？

我们质疑我们的模型产生高质量冻结特征的能力，是否会影响其在特定数据集上有监督微调时的性能。
虽然这不是本文的核心，但这一实验可以表明我们是否无意间让模型专门化了冻结特征线性评估这一设置。
为进行这一健全性检查，我们应用 Touvron et al.（2022）的微调流水线，不调整超参数。
在表 5 中，我们展示微调主干后 ImageNet-1k 验证集上的 Top-1 准确率提升超过 +2%。
在分辨率为 224 和 448 的模型上均是如此。
通过调整微调超参数可以获得进一步收益，但这超出了本健全性检查的目标。
尽管如此，我们微调后的最佳性能（88.9%）仅比绝对最高水平（91.1%，由 Chen et al.（2023a）取得）低几个百分点（−2.2%）。
由于 DINOv2 的特征在线性和微调两种设置下都很强，我们方法的一个重要性质是：微调是可选的。

| 架构 | 分辨率 | 线性 | 微调 | Δ |
| --- | --- | --- | --- | --- |
| ViT-g/14 | 224 | 86.5 | 88.5 | +2.0 |
| ViT-g/14 | 448 | 86.7 | 88.9 | +2.2 |

表 5：
在 ImageNet-1k 上的有监督微调。
我们使用 Touvron et al.（2022）的流水线在 ImageNet-1k 上以 224×224 或 448×448 分辨率微调我们的编码器。我们与线性探测获得的准确率进行比较，观察到微调仅带来适度提升：这表明 DINOv2 特征本身已能开箱即用。

##### 鲁棒性分析。

作为研究的补充，并探究我们特征的泛化能力，我们在域泛化基准上评估我们带线性分类头训练的 ImageNet-1k 模型。
我们使用如上所述性能最佳的线性分类器，直接在这些基准上运行推理。
请注意，文献中的大多数结果是由在 ImageNet-1k 上端到端微调的模型取得的。
实验结果展示在表 6 中。
与最先进的 SSL 方法相比，我们的模型显示出大幅更好的鲁棒性（相比 iBOT，在 A（Hendrycks et al., 2021b）上 +29.6%，在 R（Hendrycks et al., 2021a）上 +22.1%，在 Sketch（Wang et al., 2019）上 +23.0%）。
我们的模型在 ImageNet-A 上也优于最佳弱监督模型，但在 R 和 Sketch 上落后。

| 方法 | 架构 | 数据 | Im-A | Im-R | Im-C↓ | Sketch |
| --- | --- | --- | --- | --- | --- | --- |
| OpenCLIP | ViT-G/14 | LAION-2B | 63.8 | 87.8 | 45.3 | 66.4 |
| MAE | ViT-H/14 | INet-1k | 10.2 | 34.4 | 61.4 | 21.9 |
| DINO | ViT-B/8 | INet-1k | 23.9 | 37.0 | 56.6 | 25.5 |
| iBOT | ViT-L/16 | INet-22k | 41.5 | 51.0 | 43.9 | 38.5 |
| DINOv2 | ViT-S/14 | LVD-142M | 33.5 | 53.7 | 54.4 | 41.2 |
| DINOv2 | ViT-B/14 | LVD-142M | 55.1 | 63.3 | 42.7 | 50.6 |
| DINOv2 | ViT-L/14 | LVD-142M | 71.3 | 74.4 | 31.5 | 59.3 |
| DINOv2 | ViT-g/14 | LVD-142M | 75.9 | 78.8 | 28.2 | 62.5 |

表 6：
在 224 分辨率下冻结特征上以线性探测进行域泛化。
除 Im-C 外，所有基准数值越高越好。

### 7.2 更多图像与视频分类基准

在本节中，我们研究特征在下游分类基准上的泛化能力。
在此背景下我们考虑两组评估。
一方面，我们使用大型细粒度数据集，如 iNaturalist 和 Places205。
另一方面，我们使用 SimCLR（Chen et al., 2020）最初提出的 12 个图像分类任务。
对于 iNaturalist 2018、iNaturalist 2021 和 Places205，我们如 7.1 节所述使用数据增强训练线性分类器。
这三个数据集上的 top-1 准确率报告在表 7 中。
有趣的是，我们的模型在 iNaturalist 两个变体上都显著胜过 OpenCLIP ViT-G/14（2018 和 2021 分别 +8.6% 和 +9.7%），而在 Places 205 上略微落后（−2.3%）。

| 特征 | 架构 | iNat2018 | iNat2021 | Places205 | K400 | UCF-101 | SSv2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OpenCLIP | ViT-G/14 | 73.0 | 76.0 | 69.8 | 78.3 | 90.7 | 35.8 |
| MAE | ViT-H/14 | 31.0 | 32.3 | 52.4 | 54.2 | 70.6 | 29.2 |
| DINO | ViT-B/8 | 59.6 | 68.3 | 60.4 | 64.5 | 85.0 | 32.6 |
| iBOT | ViT-L/16 | 66.3 | 74.6 | 64.4 | 72.6 | 88.6 | 38.7 |
| DINOv2 | ViT-S/14 | 69.0 | 74.2 | 62.9 | 67.8 | 87.0 | 33.1 |
| DINOv2 | ViT-B/14 | 76.4 | 81.1 | 66.2 | 73.2 | 89.1 | 34.4 |
| DINOv2 | ViT-L/14 | 80.4 | 85.1 | 67.3 | 76.3 | 90.5 | 35.6 |
| DINOv2 | ViT-g/14 | 81.6 | 85.7 | 67.5 | 78.4 | 91.2 | 38.3 |

表 7：
其他图像与视频分类上的线性评估。
图像基准包含大量关于物体或场景的细粒度样本。
视频基准涵盖动作分类与人-物交互。
所有特征均冻结，其上为线性探测。

在第二组评估中，尽管我们的特征并未在视频上训练，我们测量模型在视频动作识别上的性能。
我们在三个数据集上评估特征，即 UCF-101（Soomro et al., 2012）、Kinetics-400（Kay et al., 2017）和 Something-Something v2（Goyal et al., 2017）。
在此评估中，我们在视频中均匀采样 8 帧，并对 UCF 和 K-400 在特征均值上训练线性分类器。
对于 SSv2，我们选择拼接（concatenation）以比特征平均保留更多时序信息。
对每个数据集，我们测量平均准确率并将结果报告在表 7 中。
我们看到，在自监督方法中，我们的模型显然树立了新的最高水平。
此外，我们的模型在 UCF 和 Kinetics 上追平 OpenCLIP 特征的准确率（分别 +0.1% 和 +0.5%），并在 SSv2 上明显胜出（+2.5%）。
这一点尤其有趣，因为 SSv2 需要对视频帧有更丰富的理解。

最后，在表 8 中，我们在 Chen et al.（2020）最初提出的 12 个迁移分类基准上比较若干冻结特征。
该基准涵盖场景、物体（食物、汽车、飞机）和纹理。
我们将 Birdsnap 数据集替换为 CUB，因为前者未完整公开。
我们遵循 Chen et al.（2020）给出的实验协议，即在预计算特征上训练逻辑回归。
我们的模型显著胜过最先进的 SSL 模型，最显著的差异出现在 Stanford Cars（相比 DINO ViT-B/8 +14.8%）和 FGVC Aircraft（相比 iBOT ViT-L/16 +14.8%）。
尽管这些基准有利于文本引导的预训练，我们的特征在大多数分类基准上仍与 OpenCLIP 具有竞争力，只有少数数据集例外，尤其是 SUN（−5.3%）和 Cars（−4.7%）。

| 特征 | 架构 | Food | C10 | C100 | SUN | Cars | Aircr | VOC | DTD | Pets | Cal101 | Flowers | CUB | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OpenCLIP | ViT-G/14 | 94.5 | 98.7 | 91.0 | 84.0 | 96.1 | 80.2 | 89.3 | 86.0 | 95.7 | 98.1 | 99.5 | 89.9 | 91.9 |
| MAE | ViT-H/14 | 78.4 | 96.1 | 83.9 | 63.9 | 56.1 | 63.4 | 84.3 | 75.4 | 89.4 | 95.9 | 92.3 | 57.2 | 78.0 |
| DINO | ViT-B/8 | 85.1 | 97.2 | 86.9 | 70.3 | 76.6 | 70.6 | 86.7 | 79.6 | 93.2 | 95.4 | 97.6 | 81.7 | 85.1 |
| iBOT | ViT-L/16 | 91.0 | 99.0 | 92.8 | 75.6 | 71.8 | 72.4 | 89.0 | 80.7 | 87.7 | 97.5 | 99.6 | 82.1 | 86.6 |
| DINOv2 | ViT-S/14 | 89.1 | 97.7 | 87.5 | 74.4 | 81.6 | 74.0 | 87.8 | 80.6 | 95.1 | 97.0 | 99.6 | 88.1 | 87.7 |
| DINOv2 | ViT-B/14 | 92.8 | 98.7 | 91.3 | 77.3 | 88.2 | 79.4 | 88.2 | 83.3 | 96.2 | 96.1 | 99.6 | 89.6 | 90.1 |
| DINOv2 | ViT-L/14 | 94.3 | 99.3 | 93.4 | 78.7 | 90.1 | 81.5 | 88.3 | 84.0 | 96.6 | 97.5 | 99.7 | 90.5 | 91.2 |
| DINOv2 | ViT-g/14 | 94.7 | 99.5 | 94.4 | 78.7 | 91.4 | 87.2 | 89.0 | 84.5 | 96.7 | 97.6 | 99.7 | 91.6 | 92.1 |

表 8：
冻结特征在细粒度基准上的线性评估。
遵循 Chen et al.（2020）提出的评估协议，在涵盖物体、场景和纹理的 12 个基准上的准确率。

### 7.3 实例识别

在本实验中，我们使用非参数方法探究模型在实例级识别任务上的表现。
数据库中的图像依据其与查询图像的余弦相似度排序。
我们在 Paris 和 Oxford（地标识别基准）上评估我们的模型并与基线比较。
我们还在 Met（大都会博物馆艺术品数据集）和 AmsterTime（包含与阿姆斯特丹档案图像匹配的街景图像）上评估。
我们通过计算平均精度均值（mAP）来度量性能，结果报告在表 9 中。
我们看到我们的特征显著胜过 SSL（Oxford-Hard 上 mAP +41%）和弱监督（Oxford-Hard 上 mAP +34%）特征。
有趣的是，我们的特征在不同任务粒度上都表现良好，无论是类别级还是实例级。
这是强大的开箱即用计算机视觉特征所应具备的理想性质。

| 特征 | 架构 | Oxford M | Oxford H | Paris M | Paris H | Met GAP | Met GAP- | Met ACC | AmsterTime mAP |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OpenCLIP | ViT-G/14 | 50.7 | 19.7 | 79.2 | 60.2 | 6.5 | 23.9 | 34.4 | 24.6 |
| MAE | ViT-H/14 | 11.7 | 2.2 | 19.9 | 4.7 | 7.5 | 23.5 | 30.5 | 4.2 |
| DINO | ViT-B/8 | 40.1 | 13.7 | 65.3 | 35.3 | 17.1 | 37.7 | 43.9 | 24.6 |
| iBOT | ViT-L/16 | 39.0 | 12.7 | 70.7 | 47.0 | 25.1 | 54.8 | 58.2 | 26.7 |
| DINOv2 | ViT-S/14 | 68.8 | 43.2 | 84.6 | 68.5 | 29.4 | 54.3 | 57.7 | 43.5 |
| DINOv2 | ViT-B/14 | 72.9 | 49.5 | 90.3 | 78.6 | 36.7 | 63.5 | 66.1 | 45.6 |
| DINOv2 | ViT-L/14 | 75.1 | 54.0 | 92.7 | 83.5 | 40.0 | 68.9 | 71.6 | 50.0 |
| DINOv2 | ViT-g/14 | 73.6 | 52.3 | 92.1 | 82.6 | 36.8 | 73.6 | 76.5 | 46.7 |

表 9：
冻结特征在实例级识别上的评估。
我们考虑 4 个不同的基准并报告其主要指标。

### 7.4 密集识别任务

我们在若干密集下游任务上探究从网络中提取的图块级特征的质量。
我们考虑多种设置下的语义图像分割与单目深度估计，并在每个任务下的多个数据集上进行评估。

##### 语义分割。

在语义分割评估中，我们考虑两种不同设置。
线性（Linear）：训练一个线性层从图块 token 预测类别 logits。
它用于产生低分辨率的 logit 图（例如对于图块大小为 16 的模型为 32×32），然后上采样到全分辨率（512×512）以获得分割图。
该流程极其简单，但难以直接产生高分辨率分割。
+ms：线性设置的增强版。
我们拼接最后 4 层的图块 token，使用更大的图像分辨率 640，并使用多尺度测试时增强来改进预测。
我们在表 10 中报告我们的模型变体及基线在三个数据集、两种设置下的性能。

我们的模型在所有数据集和所有设置下都表现出很好的性能。
有趣的是，我们使用 +ms 的评估与用 UperNet 解码器完全微调的 MAE 相当（53.0 对 53.6 mIoU）。
这很令人惊讶，因为我们使用了一个简单得多的预测器。
此外，我们最好的模型在使用增强配方评估时，几乎追平了 Pascal VOC 上的最高水平（86.2 对 89.0 mIoU）。

##### 冻结主干接入最先进流水线。

在最后一项实验中，我们冻结主干，并将其接入 ViT-Adapter（Chen et al., 2023b）与 Mask2former 头（Cheng et al., 2022）。
我们调整适配器和头的权重，但保持主干冻结，这意味着 66% 的权重被冻结。
这使得分割训练比完整的端到端微调更轻量。
在此设置下，我们在 ADE20k 上达到 60.2 mIoU，接近 62.9 mIoU 的竞争性最高水平（Wang et al., 2022）。
尽管本实验的设置未使用第 5 节描述的优化，本实验的分割训练在 16 块 V100 GPU 上耗时 28 小时。

| 方法 | 架构 | ADE20k 线性 | ADE20k +ms | CityScapes 线性 | CityScapes +ms | VOC 线性 | VOC +ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| （最高水平） | | (62.9) | | (86.9) | | (89.0) | |
| OpenCLIP | ViT-G/14 | 39.3 | 46.0 | 60.3 | 70.3 | 71.4 | 79.2 |
| MAE | ViT-H/14 | 33.3 | 30.7 | 58.4 | 61.0 | 67.6 | 63.3 |
| DINO | ViT-B/8 | 31.8 | 35.2 | 56.9 | 66.2 | 66.4 | 75.6 |
| iBOT | ViT-L/16 | 44.6 | 47.5 | 64.8 | 74.5 | 82.3 | 84.3 |
| DINOv2 | ViT-S/14 | 44.3 | 47.2 | 66.6 | 77.1 | 81.1 | 82.6 |
| DINOv2 | ViT-B/14 | 47.3 | 51.3 | 69.4 | 80.0 | 82.5 | 84.9 |
| DINOv2 | ViT-L/14 | 47.7 | 53.1 | 70.3 | 80.9 | 82.1 | 86.0 |
| DINOv2 | ViT-g/14 | 49.0 | 53.0 | 71.3 | 81.0 | 83.0 | 86.2 |

表 10：
在 ADE20K、CityScapes 和 Pascal VOC 上使用冻结特征与线性分类器（lin.）以及多尺度（+ms）的语义分割。
绝对最高水平——分别来自 Wang et al.（2022）、Liu et al.（2021）和 Chen et al.（2018）——标注在表格顶部。
作为参考，在我们的冻结 ViT-g/14 主干上使用 Mask2Former 流水线（Steiner et al., 2021）加 ViT-Adapter（Chen et al., 2023b）在 ADE-20k 上取得 60.2 mIoU。

##### 深度估计。

在本实验中，我们在三个单目深度估计基准上评估我们的图块级特征：NYUd、KITTI，以及从 NYUd 到 SUN3d 的零样本迁移。
我们遵循 Li et al.（2022b）的评估协议。
我们为此评估考虑三种设置。
lin. 1：提取冻结 transformer 的最后一层，并将 [CLS] token 拼接到每个图块 token 上。
然后我们将 token 双线性上采样 4 倍以提高分辨率。
最后，我们训练一个简单线性层，使用分类损失：将深度预测范围划分为 256 个均匀分布的 bin，并遵循 Bhat et al.（2021）进行线性归一化。
lin. 4：我们使用与单层相同的协议，但拼接来自以下层的 token：ViT-S/B 取 $l=\{3,6,9,12\}$，ViT-L 取 $l=\{5,12,18,24\}$，ViT-g 取 $l=\{10,20,30,40\}$。
DPT：我们在冻结模型之上使用 DPT 解码器（Ranftl et al., 2021）并建立回归任务。
我们根据每种架构的特征维度调整头的规模。
所有基线、数据集和设置的结果展示在表 11 中。

从该表可见，我们的特征明显胜过可用的最佳 SSL 和 WSL 特征。
有趣的是，从 ViT-L 提取的 iBOT 特征胜过 ViT-G 的 OpenCLIP 特征。
这一观察支持了如下直觉：基于字幕的特征学习难以学到像这样的细微模式。
此外，我们的模型配合 DPT 解码器和冻结主干，追平或超越了 Li et al.（2022b）近期的工作。
最后，SUN-RGBd 上的域外泛化结果表明我们的特征可以在域之间很好地迁移。
在 NYUd 室内场景上训练的深度预测模块能够很好地泛化到 SUN-RGBd 的户外样本。

| 方法 | 架构 | NYUd lin. 1 | NYUd lin. 4 | NYUd DPT | KITTI lin. 1 | KITTI lin. 4 | KITTI DPT | NYUd→SUN RGB-D lin. 1 | NYUd→SUN RGB-D lin. 4 | NYUd→SUN RGB-D DPT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| （最高水平） | | (0.330) | | | (2.10) | | | (0.421) | | |
| OpenCLIP | ViT-G/14 | 0.541 | 0.510 | 0.414 | 3.57 | 3.21 | 2.56 | 0.537 | 0.476 | 0.408 |
| MAE | ViT-H/14 | 0.517 | 0.483 | 0.415 | 3.66 | 3.26 | 2.59 | 0.545 | 0.523 | 0.506 |
| DINO | ViT-B/8 | 0.555 | 0.539 | 0.492 | 3.81 | 3.56 | 2.74 | 0.553 | 0.541 | 0.520 |
| iBOT | ViT-L/16 | 0.417 | 0.387 | 0.358 | 3.31 | 3.07 | 2.55 | 0.447 | 0.435 | 0.426 |
| DINOv2 | ViT-S/14 | 0.449 | 0.417 | 0.356 | 3.10 | 2.86 | 2.34 | 0.477 | 0.431 | 0.409 |
| DINOv2 | ViT-B/14 | 0.399 | 0.362 | 0.317 | 2.90 | 2.59 | 2.23 | 0.448 | 0.400 | 0.377 |
| DINOv2 | ViT-L/14 | 0.384 | 0.333 | 0.293 | 2.78 | 2.50 | 2.14 | 0.429 | 0.396 | 0.360 |
| DINOv2 | ViT-g/14 | 0.344 | 0.298 | 0.279 | 2.62 | 2.35 | 2.11 | 0.402 | 0.362 | 0.338 |

表 11：
使用冻结特征的深度估计。
我们报告在 1 层（lin. 1）或 4 层（lin. 4）transformer 层之上训练线性分类器，以及 Ranftl et al.（2021）的 DPT 解码器（DPT）时的性能。
我们报告 3 个数据集上的 RMSE 指标。
数值越低越好。
作为参考，每个基准的最高水平结果取自 Li et al.（2022b），标注在表格顶部。

### 7.5 定性结果

在特征实证评估的最后一节中，我们给出若干定性分析。

##### 语义分割与深度估计。

我们展示密集预测评估的一些定性结果：图 7 中的 ADE20K 分割，以及图 7 中 NYUd、KITTI 和 SUN RGB-D 上的深度估计。
我们在每个数据集上比较使用线性分类器的 DINOv2 与 OpenCLIP。
虽然并不完美，但使用我们 DINOv2 主干的线性分割模型产生了不错的结果，并且在此评估设置下表现远好于 OpenCLIP。
事实上，OpenCLIP-G 产生的分割掩码显示出许多伪影和不连通的组件。
深度估计的定性结果清楚地展示了 OpenCLIP 与 DINOv2 之间的定量差距。
这些结果突显出，我们的特征以及从 OpenCLIP 提取的特征都能线性分离诸如深度这样的复杂信息，尽管两者都没有使用这类信息训练过。
然而，我们的特征带来平滑得多的深度估计，伪影更少。
一些物体（如 SUN RGB-D 图像中的椅子）被 OpenCLIP 完全忽略，而使用我们的特征则能正确定位。

![图 7](2304.07193v2/new-figure-7.jpg)

图 7：
使用线性分类器的分割与深度估计。
来自 ADE20K、NYUd、SUN RGB-D 和 KITTI 的示例，在冻结的 OpenCLIP-G 和 DINOv2-g 特征上使用线性探测。

##### 分布外泛化。

我们在图 8 中展示将深度预测和分割线性分类器应用于分布外样本的若干示例。
定性结果支持我们关于特征可以在域之间迁移的主张。
对动物照片或绘画预测的深度和分割质量非常好，尽管这些域差异很大。

![图 8](2304.07193v2/new-figure-8.jpg)

图 8：
使用冻结 DINOv2-g 特征和线性探测的分布外样本示例。

![图 9](2304.07193v2/new-figure-9.jpg)

图 9：
更多首个 PCA 分量的可视化。
我们在所有图像的图块之间计算 PCA，并展示前 3 个分量。
每个分量对应一个特定的颜色通道。尽管姿态、风格甚至物体发生变化，相关图像之间的相同部位仍被匹配对应。
背景通过移除第一个 PCA 分量得分为负的图块而去除。

##### 图块特征的 PCA。

我们展示对模型提取的图块特征进行主成分分析（PCA）的结果。
我们只保留对第一分量设置阈值后取值为正的图块。
该过程恰好能将图像主体与背景分离。
我们对描绘同一类别的三张图像的剩余图块计算第二个 PCA。
我们用三种不同颜色为前三个分量着色，结果展示在图 1 和图 9 中。
有两个有趣的观察：
第一，我们基于检测最高方差方向的无监督前景/背景检测器表现非常好，能够勾勒出图像中主体的边界。
第二，其余分量对应物体的「部位」，并且在同类别的图像之间匹配良好。
这是一种涌现性质——我们的模型并未被训练去解析物体的部位。

##### 图块匹配。

最后，我们通过跨图像匹配图块级特征来探索其包含的信息类型。
我们首先使用上述流程检测前景物体。
然后，我们计算从两张图像提取的图块特征之间的欧氏距离，并通过求解一个分配问题进行映射。
为了减少匹配数量，我们随后应用非极大值抑制以只保留显著的匹配。
在图 10 中，我们展示此类匹配的一些示例。

我们观察到，特征似乎捕获了在不同物体或动物中发挥相似作用的语义区域信息。
例如，飞机的机翼与鸟的翅膀相匹配。
我们还观察到，模型对风格（图像与绘图）以及姿态的大幅变化都具有鲁棒性（见大象）。

![图 10](2304.07193v2/new-figure-10.jpg)

图 10：
跨图像匹配。我们在来自不同域、不同姿态、甚至共享相似语义信息的不同物体之间匹配图块级特征。
这展示了我们的模型跨域迁移以及理解不同物体相似部位之间关系的能力。

## 8 公平性与偏见分析

我们对模型进行了两项公平性评估。
我们探究地理公平性和潜在的有害标签关联。
对于两项评估，我们都使用最大的 ViT-g 模型进行实验。

### 8.1 地理公平性

我们在 De Vries et al.（2019）提出的 Dollar Street 数据集上评估地理公平性，采用 Goyal et al.（2022b）的评估协议。
该基准比较不同国家和收入水平之间的性能。它包含来自 54 个国家 289 个家庭的 16,073 张图像。
任务是识别 94 个因收入或地点不同而在视觉上呈现差异的概念。
在表 12 中，我们将我们的模型与 SEERv2（Goyal et al., 2022a）——一个在地理上多样化的图像集上训练的模型——进行比较。
我们的模型在地区和收入上比 SEERv2 模型稍更公平，并显著优于 Goyal et al.（2022a）报告的有监督基线。
然而，我们仍观察到地区之间的显著差异，特别是在非洲，我们模型的性能相比欧洲下降 25.7%。
这表明我们的模型仍偏向西方国家。
类似地，我们的模型在高收入家庭上的表现显著好于低收入家庭，差异为 31.7%。
尽管有所改善，我们仍观察到模型对西方国家富裕家庭存在显著偏见。

| 方法 | 架构 | 数据 | 低收入 | 中等收入 | 高收入 | 非洲 | 亚洲 | 美洲 | 欧洲 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SEERv2 | RG-10B | IG-1B | 59.7 | 78.5 | 86.6 | 65.9 | 76.3 | 81.1 | 85.6 |
| DINOv2 | ViT-g/14 | LVD-142M | 67.4 | 83.3 | 90.5 | 74.0 | 81.6 | 86.2 | 89.7 |

表 12：
跨收入区间和地区的地理公平性与多样性分析。

### 8.2 性别、肤色与年龄

在第二组评估中，我们探究模型如何对不同性别、肤色和年龄（均为自报）的人像进行分类。
我们遵循 Goyal et al.（2022b）的协议，在 ImageNet-22k 的 619 个类别子集上训练一个多类分类器。
我们将这 619 个类别归为四个更宽泛的类别：Human（人）、Possibly Human（可能是人）、Non-Human（非人）或 Crime（犯罪）。
Non-Human 和 Crime 被视为有害。
使用该分类器，我们在 Casual Conversations 数据集（Hazirbas et al., 2021）的 2955 张图像上运行推理，并保留所有被赋予 0.1 及以上概率的 top-5 标签。
因此，我们可以为每张图像分配多个类别。
我们对原始评估协议做了一处修改：我们不向主干反向传播梯度，保持其冻结。
我们在表 13 中将我们的模型与 SEERv2 进行比较。

我们的模型通常将所有群体的图像分类为 Human，且不同肤色之间没有大的偏差。
SEERv2 和 DINOv2 都没有预测出 Non-Human 或 Crime 元类别的有害标签（除两个背景中含有视觉上类似监狱铁栏杆的实例外）。
我们看到我们的模型经常触发 Possibly-Human 类别。
该类别由 ImageNet-22k 中常与人相关的物体构成，如 Scarf（围巾）、Glasses（眼镜）或 Beard（胡须）。
由于 Beard 类别的普遍存在，我们的模型经常对男性预测 Possibly-Human 类别。
本研究中没有明确的模式表明对特定群体的偏见。
虽然这令人鼓舞，我们也承认更彻底的偏见评估可能会揭示模型的缺陷。

| 模型 | 关联类别 | 女性-较深肤色 | 女性-较浅肤色 | 男性-较深肤色 | 男性-较浅肤色 | 18-30 | 30-45 | 45-70 | 70+ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SEER RG-10B | Non-Human | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| SEER RG-10B | Crime | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| SEER RG-10B | Human | 94.9 | 95.8 | 86.6 | 79.0 | 90.5 | 88.3 | 91.9 | 82.3 |
| SEER RG-10B | Possibly-Human | 13.6 | 6.7 | 65.0 | 60.2 | 32.8 | 37.2 | 29.4 | 6.5 |
| DINOv2 ViT-g/14 | Non-Human | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| DINOv2 ViT-g/14 | Crime | 0.0 | 0.0 | 0.2 | 0.0 | 0.0 | 0.1 | 0.0 | 0.0 |
| DINOv2 ViT-g/14 | Human | 97.3 | 97.7 | 86.1 | 84.0 | 91.2 | 90.2 | 93.2 | 88.7 |
| DINOv2 ViT-g/14 | Possibly-Human | 15.8 | 17.2 | 52.2 | 48.1 | 35.3 | 37.3 | 23.0 | 9.7 |

表 13：
跨性别、肤色和年龄组的标签关联公平性评估。
我们遵循 Goyal et al.（2022b）提出的协议并稍作修改。
我们不微调主干，而是简单地在 ImageNet-22k 的 619 个类别子集上学习一个线性分类器。

## 9 估计训练我们模型的环境影响

| 需复现的模型 | GPU 类型 | GPU 功耗 | GPU 时数 | PUE | 总能耗 | 碳排放（tCO2eq） |
| --- | --- | --- | --- | --- | --- | --- |
| DINOv2-g | A100-40GB | 400W | 22,016 | 1.1 | 9.7 MWh | 3.7 |

表 14：
复现 DINOv2 的碳足迹。
我们报告复现 DINOv2-g 的潜在碳排放，假设 A100-40GB 的功耗为 400W、PUE 为 1.1、碳强度因子为每千瓦时 0.385 kg CO2e。

训练基座模型消耗大量能源，导致二氧化碳排放。
Patterson et al.（2021）提出了一种方法，基于数据中心及其电网的具体情况来报告模型训练期间碳排放的估计值。
这一计算可以为用于训练模型的数据中心设计以及数据中心选址提供信息。
该方法需要了解用于训练的数据中心的具体情况，而当多个数据中心随时间参与时，这可能很复杂。
此外，这些具体情况往往不在 AI 从业者的掌控之中，因此当从业者对未来训练做技术决策时，该方法的帮助较小。
相反，在本节中，我们遵循另一种做法：报告在美国境内一个平均数据中心重训一个类似模型的潜在碳排放。
该方法此前曾用于自然语言处理的工作（Strubell et al., 2019；Touvron et al., 2023），以在不同预训练方案之间建立公平比较。
更准确地说，我们将所有外生变量的值固定为与 Touvron et al.（2023）中相同的值，即 PUE 为 1.1，碳强度因子取美国平均值 0.385 kg CO2eq/KWh。
我们使用与 Patterson et al.（2021）相同的公式来估计潜在能耗和碳排放。
对于 A100-80GB 的功耗，我们采用 NVLink 系统的热设计功率 400W。
我们在表 14 中报告重训 DINOv2 ViT-g 的潜在碳排放。
作为比较，在同一数据中心运行的话，重训 OpenCLIP ViT-L 或 OpenCLIP ViT-G 将分别需要 22.4 MWh 和 118.9 MWh。
这相当于 10× 的碳排放。
注意这一比较对他们并不公平，因为他们还并行训练了一个文本编码器，因此我们不把他们列入表中。
不过，对于只想训练视觉特征的人而言，这给出了一个合理的指引：在这种情形下，从碳排放角度训练自监督模型更为可取。
而当你计划复用文本编码器时，训练文本引导模型仍然合理。

##### 整个项目的碳足迹。

此外，我们使用上文所述的同一电网，估计整个项目的足迹在 0.5k 到 1k tCO2eq 之间³。
（脚注 3：作为参考，伦敦与纽约之间一整趟波音 777 往返航班约对应 560 tCO2eq。）
这一碳足迹大约相当于 200k GPU 天。
排放的主要来源是模型的自监督预训练。
例如，一次 ViT-g 模型的预训练（22k GPU 时）排放 3.7 吨 CO2eq，而在 ImageNet-1k 上的一次微调（1k GPU 时）排放 0.2 吨。
该估计仅考虑 GPU 的电力消耗，忽略其他排放，例如其制造和报废处置。

## 10 未来工作与讨论

在本工作中，我们提出了 DINOv2，一系列在大型筛选数据上无监督预训练的图像编码器的新家族。
这是首个在图像数据上的 SSL 工作，其产生的视觉特征在广泛的基准上、无需微调即可弥合与（弱）监督替代方案之间的性能差距。
我们可以将 DINOv2 模型家族的强大性能归因于几个因素：
i) 改进的训练配方，具有更好的超参数和正则化（表 1）；
ii) 更大的模型规模，无论使用何种训练数据都能带来更好的结果（图 4）；
iii) 更大的数据集（图 4）；以及
iv) 蒸馏过程，使较小的模型受益于最强 ViT-g 模型的性能（图 5）。
这些模型涌现出若干性质，例如无论图像域如何都能理解物体部位和场景几何。
我们期待在更大的模型和数据规模下涌现出更多这类性质，类似于大语言模型中的指令涌现能力，并计划沿这些轴继续扩展。
本文还表明，这些视觉特征与像线性层这样简单的分类器兼容——这意味着底层信息是现成可用的。
在未来的工作中，我们计划利用这一能力来训练一个支持语言的 AI 系统，该系统能像处理词 token 一样处理视觉特征，并提取所需的信息来为系统落地（ground）。

#### 致谢。

我们感谢 Mathilde Caron 带来本工作的初期讨论。
Julien Mairal 受 ERC 资助（资助号 101087696，APHELAIA 项目）以及 ANR 3IA MIAI@Grenoble Alpes（ANR-19-P3IA-0003）支持。
我们感谢 Olivia Joulin 为图 10 绘制的马。
我们感谢 Madeleine 和 Léon 为图 8 摆拍。
我们还感谢 FAIR 和 Meta AI 的其他成员在整个项目期间对本工作的反馈。

## 参考文献

- Amir et al. (2022)

  Shir Amir, Yossi Gandelsman, Shai Bagon, and Tali Dekel.
  Deep vit features as dense visual descriptors.
  In *ECCV workshop on "What is Motion For?"*, 2022.
- Asano et al. (2020)

  Yuki Markus Asano, Christian Rupprecht, and Andrea Vedaldi.
  Self-labelling via simultaneous clustering and representation
  learning.
  In *ICLR*, 2020.
- Assran et al. (2022)

  Mahmoud Assran, Mathilde Caron, Ishan Misra, Piotr Bojanowski, Florian Bordes,
  Pascal Vincent, Armand Joulin, Michael Rabbat, and Nicolas Ballas.
  Masked siamese networks for label-efficient learning.
  In *ECCV*, 2022.
- Assran et al. (2023)

  Mahmoud Assran, Quentin Duval, Ishan Misra, Piotr Bojanowski, Pascal Vincent,
  Michael Rabbat, Yann LeCun, and Nicolas Ballas.
  Self-supervised learning from images with a joint-embedding
  predictive architecture.
  In *CVPR*, 2023.
- Baevski et al. (2022)

  Alexei Baevski, Wei-Ning Hsu, Qiantong Xu, Arun Babu, Jiatao Gu, and Michael
  Auli.
  Data2vec: A general framework for self-supervised learning in speech,
  vision and language.
  In *ICML*, 2022.
- Bao et al. (2021)

  Hangbo Bao, Li Dong, and Furu Wei.
  Beit: Bert pre-training of image transformers.
  In *ICLR*, 2021.
- Beirlant et al. (1997)

  Jan Beirlant, Edward J Dudewicz, László Györfi, Edward C Van der
  Meulen, et al.
  Nonparametric entropy estimation: An overview.
  *International Journal of Mathematical and Statistical
  Sciences*, 6(1):17–39, 1997.
- Berman et al. (2019)

  Maxim Berman, Hervé Jégou, Vedaldi Andrea, Iasonas Kokkinos, and
  Matthijs Douze.
  MultiGrain: a unified image embedding for classes and instances.
  *arXiv preprint arXiv:1902.05509*, 2019.
- Beyer et al. (2020)

  Lucas Beyer, Olivier J Hénaff, Alexander Kolesnikov, Xiaohua Zhai, and
  Aäron van den Oord.
  Are we done with imagenet?
  *arXiv preprint arXiv:2006.07159*, 2020.
- Beyer et al. (2023)

  Lucas Beyer, Pavel Izmailov, Alexander Kolesnikov, Mathilde Caron, Simon
  Kornblith, Xiaohua Zhai, Matthias Minderer, Michael Tschannen, Ibrahim
  Alabdulmohsin, and Filip Pavetic.
  Flexivit: One model for all patch sizes.
  In *CVPR*, 2023.
- Bhat et al. (2021)

  Shariq Farooq Bhat, Ibraheem Alhashim, and Peter Wonka.
  AdaBins: Depth estimation using adaptive bins.
  In *CVPR*, 2021.
- Bojanowski & Joulin (2017)

  Piotr Bojanowski and Armand Joulin.
  Unsupervised learning by predicting noise.
  In *ICML*, 2017.
- Bommasani et al. (2021)

  Rishi Bommasani, Drew A Hudson, Ehsan Adeli, Russ Altman, Simran Arora, Sydney
  von Arx, Michael S Bernstein, Jeannette Bohg, Antoine Bosselut, Emma
  Brunskill, et al.
  On the opportunities and risks of foundation models.
  *arXiv preprint arXiv:2108.07258*, 2021.
- Bossard et al. (2014)

  Lukas Bossard, Matthieu Guillaumin, and Luc Van Gool.
  Food-101 – mining discriminative components with random forests.
  In *ECCV*, 2014.
- Brown et al. (2020)

  Tom B Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla
  Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell,
  et al.
  Language models are few-shot learners.
  In *NeurIPS*, 2020.
- Caron et al. (2018)

  Mathilde Caron, Piotr Bojanowski, Armand Joulin, and Matthijs Douze.
  Deep clustering for unsupervised learning of visual features.
  In *ECCV*, 2018.
- Caron et al. (2019)

  Mathilde Caron, Piotr Bojanowski, Julien Mairal, and Armand Joulin.
  Unsupervised pre-training of image features on non-curated data.
  In *ICCV*, 2019.
- Caron et al. (2020)

  Mathilde Caron, Ishan Misra, Julien Mairal, Priya Goyal, Piotr Bojanowski, and
  Armand Joulin.
  Unsupervised learning of visual features by contrasting cluster
  assignments.
  In *NeurIPS*, 2020.
- Caron et al. (2021)

  Mathilde Caron, Hugo Touvron, Ishan Misra, Hervé Jégou, Julien Mairal,
  Piotr Bojanowski, and Armand Joulin.
  Emerging properties in self-supervised vision transformers.
  In *ICCV*, 2021.
- Chen et al. (2018)

  Liang-Chieh Chen, Yukun Zhu, George Papandreou, Florian Schroff, and Hartwig
  Adam.
  Encoder-decoder with atrous separable convolution for semantic image
  segmentation.
  In *ECCV*, 2018.
- Chen et al. (2020)

  Ting Chen, Simon Kornblith, Mohammad Norouzi, and Geoffrey Hinton.
  A simple framework for contrastive learning of visual
  representations.
  In *ICML*, 2020.
- Chen et al. (2023a)

  Xiangning Chen, Chen Liang, Da Huang, Esteban Real, Kaiyuan Wang, Yao Liu, Hieu
  Pham, Xuanyi Dong, Thang Luong, Cho-Jui Hsieh, et al.
  Symbolic discovery of optimization algorithms.
  *arXiv preprint arXiv:2302.06675*, 2023a.
- Chen & He (2021)

  Xinlei Chen and Kaiming He.
  Exploring simple siamese representation learning.
  In *CVPR*, 2021.
- Chen et al. (2021)

  Xinlei Chen, Saining Xie, and Kaiming He.
  An empirical study of training self-supervised vision transformers.
  In *ICCV*, 2021.
- Chen et al. (2023b)

  Zhe Chen, Yuchen Duan, Wenhai Wang, Junjun He, Tong Lu, Jifeng Dai, and
  Yu Qiao.
  Vision transformer adapter for dense predictions.
  In *ICLR*, 2023b.
- Cheng et al. (2022)

  Bowen Cheng, Ishan Misra, Alexander G Schwing, Alexander Kirillov, and Rohit
  Girdhar.
  Masked-attention mask transformer for universal image segmentation.
  In *CVPR*, 2022.
- Cherti et al. (2023)

  Mehdi Cherti, Romain Beaumont, Ross Wightman, Mitchell Wortsman, Gabriel
  Ilharco, Cade Gordon, Christoph Schuhmann, Ludwig Schmidt, and Jenia Jitsev.
  Reproducible scaling laws for contrastive language-image learning.
  In *CVPR*, 2023.
- Chowdhery et al. (2022)

  Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra,
  Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian
  Gehrmann, et al.
  Palm: Scaling language modeling with pathways.
  *arXiv preprint arXiv:2204.02311*, 2022.
- Cimpoi et al. (2014)

  M. Cimpoi, S. Maji, I. Kokkinos, S. Mohamed, , and A. Vedaldi.
  Describing textures in the wild.
  In *CVPR*, 2014.
- Cordts et al. (2016)

  Marius Cordts, Mohamed Omran, Sebastian Ramos, Timo Rehfeld, Markus Enzweiler,
  Rodrigo Benenson, Uwe Franke, Stefan Roth, and Bernt Schiele.
  The cityscapes dataset for semantic urban scene understanding.
  In *CVPR*, 2016.
- Dao et al. (2022)

  Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, and Christopher Ré.
  Flashattention: Fast and memory-efficient exact attention with
  io-awareness.
  In *NeurIPS*, 2022.
- De Vries et al. (2019)

  Terrance De Vries, Ishan Misra, Changhan Wang, and Laurens Van der Maaten.
  Does object recognition work for everyone?
  In *CVPR workshops*, 2019.
- Delattre & Fournier (2017)

  Sylvain Delattre and Nicolas Fournier.
  On the kozachenko–leonenko entropy estimator.
  *Journal of Statistical Planning and Inference*, 185:69–93, 2017.
- Deng et al. (2009)

  Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li, and Li Fei-Fei.
  Imagenet: A large-scale hierarchical image database.
  In *CVPR*, 2009.
- Devlin et al. (2019)

  Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova.
  Bert: Pre-training of deep bidirectional transformers for language
  understanding.
  *NAACL*, 2019.
- Doersch et al. (2015)

  Carl Doersch, Abhinav Gupta, and Alexei A Efros.
  Unsupervised visual representation learning by context prediction.
  In *ICCV*, 2015.
- Dosovitskiy et al. (2016)

  Alexey Dosovitskiy, Philipp Fischer, Jost Tobias Springenberg, Martin
  Riedmiller, and Thomas Brox.
  Discriminative unsupervised feature learning with exemplar
  convolutional neural networks.
  *TPAMI*, 2016.
- Dosovitskiy et al. (2021)

  Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn,
  Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg
  Heigold, Sylvain Gelly, et al.
  An image is worth 16x16 words: Transformers for image recognition at
  scale.
  In *ICLR*, 2021.
- Douze et al. (2009)

  Matthijs Douze, Hervé Jégou, Harsimrat Sandhawalia, Laurent Amsaleg,
  and Cordelia Schmid.
  Evaluation of gist descriptors for web-scale image search.
  In *CIVR*, 2009.
- Duval et al. (2023)

  Quentin Duval, Ishan Misra, and Nicolas Ballas.
  A simple recipe for competitive low-compute self supervised vision
  models.
  *arXiv preprint arXiv:2301.09451*, 2023.
- El-Nouby et al. (2021)

  Alaaeldin El-Nouby, Gautier Izacard, Hugo Touvron, Ivan Laptev, Hervé
  Jegou, and Edouard Grave.
  Are large-scale datasets necessary for self-supervised pre-training?
  *arXiv preprint arXiv:2112.10740*, 2021.
- Everingham et al. (2010)

  Mark Everingham, Luc Van Gool, Christopher KI Williams, John Winn, and Andrew
  Zisserman.
  The pascal visual object classes (voc) challenge.
  *IJCV*, 2010.
- Fang et al. (2023)

  Yuxin Fang, Wen Wang, Binhui Xie, Quan Sun, Ledell Wu, Xinggang Wang, Tiejun
  Huang, Xinlong Wang, and Yue Cao.
  Eva: Exploring the limits of masked visual representation learning at
  scale.
  In *CVPR*, 2023.
- Fei-Fei et al. (2004)

  Li Fei-Fei, Rob Fergus, and Pietro Perona.
  Learning generative visual models from few training examples: An
  incremental bayesian approach tested on 101 object categories.
  In *CVPR*, 2004.
- Geiger et al. (2013)

  Andreas Geiger, Philip Lenz, Christoph Stiller, and Raquel Urtasun.
  Vision meets robotics: The kitti dataset.
  *IJRR*, 2013.
- Gidaris et al. (2018)

  Spyros Gidaris, Praveer Singh, and Nikos Komodakis.
  Unsupervised representation learning by predicting image rotations.
  In *ICLR*, 2018.
- Girdhar et al. (2023)

  Rohit Girdhar, Alaaeldin El-Nouby, Mannat Singh, Kalyan Vasudev Alwala, Armand
  Joulin, and Ishan Misra.
  Omnimae: Single model masked pretraining on images and videos.
  In *CVPR*, 2023.
- Goyal et al. (2019)

  Priya Goyal, Dhruv Mahajan, Abhinav Gupta, and Ishan Misra.
  Scaling and benchmarking self-supervised visual representation
  learning.
  In *ICCV*, 2019.
- Goyal et al. (2021)

  Priya Goyal, Mathilde Caron, Benjamin Lefaudeux, Min Xu, Pengchao Wang, Vivek
  Pai, Mannat Singh, Vitaliy Liptchinsky, Ishan Misra, Armand Joulin, et al.
  Self-supervised pretraining of visual features in the wild.
  *preprint arXiv:2103.01988*, 2021.
- Goyal et al. (2022a)

  Priya Goyal, Quentin Duval, Isaac Seessel, Mathilde Caron, Mannat Singh, Ishan
  Misra, Levent Sagun, Armand Joulin, and Piotr Bojanowski.
  Vision models are more robust and fair when pretrained on uncurated
  images without supervision.
  *arXiv preprint arXiv:2202.08360*, 2022a.
- Goyal et al. (2022b)

  Priya Goyal, Adriana Romero Soriano, Caner Hazirbas, Levent Sagun, and Nicolas
  Usunier.
  Fairness indicators for systematic assessments of visual feature
  extractors.
  In *FAcct*, 2022b.
- Goyal et al. (2017)

  Raghav Goyal, Samira Ebrahimi Kahou, Vincent Michalski, Joanna Materzynska,
  Susanne Westphal, Heuna Kim, Valentin Haenel, Ingo Fruend, Peter Yianilos,
  Moritz Mueller-Freitag, et al.
  The "something something" video database for learning and evaluating
  visual common sense.
  In *ICCV*, 2017.
- Grill et al. (2020)

  Jean-Bastien Grill, Florian Strub, Florent Altché, Corentin Tallec,
  Pierre H Richemond, Elena Buchatskaya, Carl Doersch, Bernardo Avila Pires,
  Zhaohan Daniel Guo, Mohammad Gheshlaghi Azar, Bilal Piot, Koray Kavukcuoglu,
  Rémi Munos, and Michal Valko.
  Bootstrap your own latent: A new approach to self-supervised
  learning.
  In *NeurIPS*, 2020.
- Hadsell et al. (2006)

  Raia Hadsell, Sumit Chopra, and Yann LeCun.
  Dimensionality reduction by learning an invariant mapping.
  In *CVPR*, 2006.
- Hamilton et al. (2022)

  Mark Hamilton, Zhoutong Zhang, Bharath Hariharan, Noah Snavely, and William T
  Freeman.
  Unsupervised semantic segmentation by distilling feature
  correspondences.
  In *ICLR*, 2022.
- Hazirbas et al. (2021)

  Caner Hazirbas, Joanna Bitton, Brian Dolhansky, Jacqueline Pan, Albert Gordo,
  and Cristian Canton Ferrer.
  Towards measuring fairness in ai: the casual conversations dataset.
  *IEEE Transactions on Biometrics, Behavior, and Identity
  Science*, 2021.
- He et al. (2020)

  Kaiming He, Haoqi Fan, Yuxin Wu, Saining Xie, and Ross Girshick.
  Momentum contrast for unsupervised visual representation learning.
  In *CVPR*, 2020.
- He et al. (2022)

  Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollár, and Ross
  Girshick.
  Masked autoencoders are scalable vision learners.
  In *CVPR*, 2022.
- Hénaff et al. (2019)

  Olivier J Hénaff, Aravind Srinivas, Jeffrey De Fauw, Ali Razavi, Carl
  Doersch, SM Eslami, and Aaron van den Oord.
  Data-efficient image recognition with contrastive predictive coding.
  *PMLR*, 2019.
- Hendrycks & Dietterich (2019)

  Dan Hendrycks and Thomas Dietterich.
  Benchmarking neural network robustness to common corruptions and
  perturbations.
  In *ICLR*, 2019.
- Hendrycks et al. (2021a)

  Dan Hendrycks, Steven Basart, Norman Mu, Saurav Kadavath, Frank Wang, Evan
  Dorundo, Rahul Desai, Tyler Zhu, Samyak Parajuli, Mike Guo, et al.
  The many faces of robustness: A critical analysis of
  out-of-distribution generalization.
  In *ICCV*, 2021a.
- Hendrycks et al. (2021b)

  Dan Hendrycks, Kevin Zhao, Steven Basart, Jacob Steinhardt, and Dawn Song.
  Natural adversarial examples.
  In *CVPR*, 2021b.
- Hinton et al. (2014)

  Geoffrey Hinton, Oriol Vinyals, and Jeff Dean.
  Distilling the knowledge in a neural network.
  In *NeurIPS Deep Learning Workshop*, 2014.
- Hoffmann et al. (2022)

  Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor
  Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes
  Welbl, Aidan Clark, et al.
  Training compute-optimal large language models.
  *arXiv preprint arXiv:2203.15556*, 2022.
- Huang et al. (2016)

  Gao Huang, Yu Sun, Zhuang Liu, Daniel Sedra, and Kilian Q Weinberger.
  Deep networks with stochastic depth.
  In *ECCV*, 2016.
- Ilharco et al. (2021)

  Gabriel Ilharco, Mitchell Wortsman, Ross Wightman, Cade Gordon, Nicholas
  Carlini, Rohan Taori, Achal Dave, Vaishaal Shankar, Hongseok Namkoong, John
  Miller, Hannaneh Hajishirzi, Ali Farhadi, and Ludwig Schmidt.
  Openclip.
  2021.
- Jegou et al. (2010)

  Herve Jegou, Matthijs Douze, and Cordelia Schmid.
  Product quantization for nearest neighbor search.
  *TPAMI*, 2010.
- Johnson et al. (2019)

  Jeff Johnson, Matthijs Douze, and Hervé Jégou.
  Billion-scale similarity search with GPUs.
  *IEEE Transactions on Big Data*, 2019.
- Joulin et al. (2016)

  Armand Joulin, Laurens Van Der Maaten, Allan Jabri, and Nicolas Vasilache.
  Learning visual features from large weakly supervised data.
  In *ECCV*, 2016.
- Kay et al. (2017)

  Will Kay, Joao Carreira, Karen Simonyan, Brian Zhang, Chloe Hillier, Sudheendra
  Vijayanarasimhan, Fabio Viola, Tim Green, Trevor Back, Paul Natsev, et al.
  The kinetics human action video dataset.
  *arXiv preprint arXiv:1705.06950*, 2017.
- Krause et al. (2013)

  Jonathan Krause, Michael Stark, Jia Deng, and Li Fei-Fei.
  3d object representations for fine-grained categorization.
  In *3DRR*, 2013.
- Krell et al. (2022)

  Mario Michael Krell, Matej Kosec, Sergio P. Perez, and Andrew Fitzgibbon.
  Efficient sequence packing without cross-contamination: Accelerating
  large language models without impacting performance, 2022.
- Krizhevsky et al. (2009)

  Alex Krizhevsky, Geoffrey Hinton, et al.
  Learning multiple layers of features from tiny images.
  2009.
- Lefaudeux et al. (2022)

  Benjamin Lefaudeux, Francisco Massa, Diana Liskovich, Wenhan Xiong, Vittorio
  Caggiano, Sean Naren, Min Xu, Jieru Hu, Marta Tintore, Susan Zhang, Patrick
  Labatut, and Daniel Haziza.
  xformers: A modular and hackable transformer modelling library.
  <https://github.com/facebookresearch/xformers>, 2022.
- Li et al. (2022a)

  Chunyuan Li, Jianwei Yang, Pengchuan Zhang, Mei Gao, Bin Xiao, Xiyang Dai,
  Lu Yuan, and Jianfeng Gao.
  Efficient self-supervised vision transformers for representation
  learning.
  In *ICLR*, 2022a.
- Li et al. (2022b)

  Zhenyu Li, Xuyang Wang, Xianming Liu, and Junjun Jiang.
  Binsformer: Revisiting adaptive bins for monocular depth estimation.
  *arXiv preprint arXiv:2204.00987*, 2022b.
- Likhomanenko et al. (2021)

  Tatiana Likhomanenko, Qiantong Xu, Gabriel Synnaeve, Ronan Collobert, and Alex
  Rogozhnikov.
  Cape: Encoding relative positions with continuous augmented
  positional embeddings.
  In *NeurIPS*, 2021.
- Liu et al. (2021)

  Huajun Liu, Fuqiang Liu, Xinyi Fan, and Dong Huang.
  Polarized self-attention: towards high-quality pixel-wise regression.
  *arXiv preprint arXiv:2107.00782*, 2021.
- Mahajan et al. (2018)

  Dhruv Mahajan, Ross Girshick, Vignesh Ramanathan, Kaiming He, Manohar Paluri,
  Yixuan Li, Ashwin Bharambe, and Laurens van der Maaten.
  Exploring the limits of weakly supervised pretraining.
  In *ECCV*, 2018.
- Maji et al. (2013)

  S. Maji, J. Kannala, E. Rahtu, M. Blaschko, and A. Vedaldi.
  Fine-grained visual classification of aircraft.
  Technical report, 2013.
- Misra & Maaten (2020)

  Ishan Misra and Laurens van der Maaten.
  Self-supervised learning of pretext-invariant representations.
  In *CVPR*, 2020.
- Nilsback & Zisserman (2008)

  Maria-Elena Nilsback and Andrew Zisserman.
  Automated flower classification over a large number of classes.
  In *ICVGIP*, 2008.
- Noroozi & Favaro (2016)

  Mehdi Noroozi and Paolo Favaro.
  Unsupervised learning of visual representations by solving jigsaw
  puzzles.
  In *ECCV*, 2016.
- Ofri-Amar et al. (2023)

  Dolev Ofri-Amar, Michal Geyer, Yoni Kasten, and Tali Dekel.
  Neural congealing: Aligning images to a joint semantic atlas.
  In *CVPR*, 2023.
- Parkhi et al. (2012)

  Omkar M. Parkhi, Andrea Vedaldi, Andrew Zisserman, and C. V. Jawahar.
  Cats and dogs.
  In *CVPR*, 2012.
- Pathak et al. (2016)

  Deepak Pathak, Philipp Krähenbühl, Jeff Donahue, Trevor Darrell, and Alexei
  Efros.
  Context encoders: Feature learning by inpainting.
  In *CVPR*, 2016.
- Patterson et al. (2021)

  David Patterson, Joseph Gonzalez, Quoc Le, Chen Liang, Lluis-Miquel Munguia,
  Daniel Rothchild, David So, Maud Texier, and Jeff Dean.
  Carbon emissions and large neural network training.
  *arXiv preprint arXiv:2104.10350*, 2021.
- Pizzi et al. (2022)

  Ed Pizzi, Sreya Dutta Roy, Sugosh Nagavara Ravindra, Priya Goyal, and Matthijs
  Douze.
  A self-supervised descriptor for image copy detection.
  In *CVPR*, 2022.
- Radenović et al. (2018a)

  Filip Radenović, Ahmet Iscen, Giorgos Tolias, Yannis Avrithis, and
  Ondřej Chum.
  Revisiting oxford and paris: Large-scale image retrieval
  benchmarking.
  In *CVPR*, 2018a.
- Radenović et al. (2018b)

  Filip Radenović, Giorgos Tolias, and Ondřej Chum.
  Fine-tuning cnn image retrieval with no human annotation.
  *TPAMI*, 2018b.
- Radford et al. (2017)

  Alec Radford, Rafal Jozefowicz, and Ilya Sutskever.
  Learning to generate reviews and discovering sentiment.
  *arXiv preprint arXiv:1704.01444*, 2017.
- Radford et al. (2019)

  Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, and Ilya
  Sutskever.
  Language models are unsupervised multitask learners.
  2019.
- Radford et al. (2021)

  Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh,
  Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark,
  et al.
  Learning transferable visual models from natural language
  supervision.
  In *ICML*, 2021.
- Raffel et al. (2020)

  Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael
  Matena, Yanqi Zhou, Wei Li, Peter J Liu, et al.
  Exploring the limits of transfer learning with a unified text-to-text
  transformer.
  *JMLR*, 2020.
- Ranftl et al. (2021)

  René Ranftl, Alexey Bochkovskiy, and Vladlen Koltun.
  Vision transformers for dense prediction.
  In *ICCV*, 2021.
- Recht et al. (2019)

  Benjamin Recht, Rebecca Roelofs, Ludwig Schmidt, and Vaishaal Shankar.
  Do imagenet classifiers generalize to imagenet?
  In *ICML*, 2019.
- Revaud et al. (2019)

  Jerome Revaud, Jon Almazán, Rafael S Rezende, and Cesar Roberto de Souza.
  Learning with average precision: Training image retrieval with a
  listwise loss.
  In *ICCV*, 2019.
- Ruan et al. (2023)

  Yangjun Ruan, Saurabh Singh, Warren Morningstar, Alexander A Alemi, Sergey
  Ioffe, Ian Fischer, and Joshua V Dillon.
  Weighted ensemble self-supervised learning.
  In *ICLR*, 2023.
- Russakovsky et al. (2015)

  Olga Russakovsky, Jia Deng, Hao Su, Jonathan Krause, Sanjeev Satheesh, Sean Ma,
  Zhiheng Huang, Andrej Karpathy, Aditya Khosla, Michael Bernstein, Alexander C
  Berg, and Li Fei-Fei.
  Imagenet large scale visual recognition challenge.
  *IJCV*, 2015.
- Sablayrolles et al. (2019)

  Alexandre Sablayrolles, Matthijs Douze, Cordelia Schmid, and Hervé
  Jégou.
  Spreading vectors for similarity search.
  In *ICLR*, 2019.
- Schuhmann et al. (2021)

  Christoph Schuhmann, Richard Vencu, Romain Beaumont, Robert Kaczmarczyk,
  Clayton Mullis, Aarush Katta, Theo Coombes, Jenia Jitsev, and Aran
  Komatsuzaki.
  Laion-400m: Open dataset of clip-filtered 400 million image-text
  pairs.
  In *NeurIPS Data Centric AI Workshop*, 2021.
- Schuhmann et al. (2022)

  Christoph Schuhmann, Romain Beaumont, Richard Vencu, Cade Gordon, Ross
  Wightman, Mehdi Cherti, Theo Coombes, Aarush Katta, Clayton Mullis, Mitchell
  Wortsman, et al.
  Laion-5b: An open large-scale dataset for training next generation
  image-text models.
  In *NeurIPS*, 2022.
- Shazeer (2020)

  Noam Shazeer.
  Glu variants improve transformer.
  *arXiv preprint arXiv:2002.05202*, 2020.
- Silberman et al. (2012)

  Nathan Silberman, Derek Hoiem, Pushmeet Kohli, and Rob Fergus.
  Indoor segmentation and support inference from rgbd images.
  In *ECCV*, 2012.
- Singh et al. (2022)

  Mannat Singh, Laura Gustafson, Aaron Adcock, Vinicius de Freitas Reis, Bugra
  Gedik, Raj Prateek Kosaraju, Dhruv Mahajan, Ross Girshick, Piotr Dollár,
  and Laurens van der Maaten.
  Revisiting Weakly Supervised Pre-Training of Visual Perception
  Models.
  In *CVPR*, 2022.
- Song et al. (2015)

  Shuran Song, Samuel P Lichtenberg, and Jianxiong Xiao.
  Sun rgb-d: A rgb-d scene understanding benchmark suite.
  In *CVPR*, 2015.
- Soomro et al. (2012)

  Khurram Soomro, Amir Roshan Zamir, and Mubarak Shah.
  Ucf101: A dataset of 101 human actions classes from videos in the
  wild.
  *arXiv preprint arXiv:1212.0402*, 2012.
- Steiner et al. (2021)

  Andreas Steiner, Alexander Kolesnikov, Xiaohua Zhai, Ross Wightman, Jakob
  Uszkoreit, and Lucas Beyer.
  How to train your vit? data, augmentation, and regularization in
  vision transformers.
  *TMLR*, 2021.
- Strubell et al. (2019)

  Emma Strubell, Ananya Ganesh, and Andrew McCallum.
  Energy and policy considerations for deep learning in nlp.
  *ACL*, 2019.
- Tian et al. (2021)

  Yonglong Tian, Olivier J Henaff, and Aäron van den Oord.
  Divide and contrast: Self-supervised learning from uncurated data.
  In *ICCV*, 2021.
- Tolias et al. (2016)

  Giorgos Tolias, Ronan Sicre, and Hervé Jégou.
  Particular object retrieval with integral max-pooling of cnn
  activations.
  In *ICLR*, 2016.
- Tong et al. (2022)

  Zhan Tong, Yibing Song, Jue Wang, and Limin Wang.
  Videomae: Masked autoencoders are data-efficient learners for
  self-supervised video pre-training.
  In *NeurIPS*, 2022.
- Touvron et al. (2019)

  Hugo Touvron, Andrea Vedaldi, Matthijs Douze, and Hervé Jégou.
  Fixing the train-test resolution discrepancy.
  In *NeurIPS*, 2019.
- Touvron et al. (2022)

  Hugo Touvron, Matthieu Cord, and Hervé Jégou.
  Deit iii: Revenge of the vit.
  In *ECCV*, 2022.
- Touvron et al. (2023)

  Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne
  Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric
  Hambro, Faisal Azhar, Aurelien Rodriguez, Armand Joulin, Edouard Grave, and
  Guillaume Lample.
  Llama: Open and efficient foundation language models.
  *arXiv preprint arXiv:2302.13971*, 2023.
- Tumanyan et al. (2022)

  Narek Tumanyan, Omer Bar-Tal, Shai Bagon, and Tali Dekel.
  Splicing vit features for semantic appearance transfer.
  In *CVPR*, 2022.
- Van Horn et al. (2018)

  Grant Van Horn, Oisin Mac Aodha, Yang Song, Yin Cui, Chen Sun, Alex Shepard,
  Hartwig Adam, Pietro Perona, and Serge Belongie.
  The inaturalist species classification and detection dataset.
  In *CVPR*, 2018.
- Van Horn et al. (2021)

  Grant Van Horn, Elijah Cole, Sara Beery, Kimberly Wilber, Serge Belongie, and
  Oisin Mac Aodha.
  Benchmarking representation learning for natural world image
  collections.
  In *CVPR*, 2021.
- Wang et al. (2022)

  Wenhai Wang, Jifeng Dai, Zhe Chen, Zhenhang Huang, Zhiqi Li, Xizhou Zhu,
  Xiaowei Hu, Tong Lu, Lewei Lu, Hongsheng Li, et al.
  Internimage: Exploring large-scale vision foundation models with
  deformable convolutions.
  In *CVPR*, 2022.
- Wang et al. (2019)

  Xiaolong Wang, Allan Jabri, and Alexei A Efros.
  Learning correspondence from the cycle-consistency of time.
  In *CVPR*, 2019.
- Warburg et al. (2020)

  Frederik Warburg, Soren Hauberg, Manuel Lopez-Antequera, Pau Gargallo, Yubin
  Kuang, and Javier Civera.
  Mapillary street-level sequences: A dataset for lifelong place
  recognition.
  In *CVPR*, 2020.
- Weinzaepfel et al. (2021)

  Philippe Weinzaepfel, Thomas Lucas, Diane Larlus, and Yannis Kalantidis.
  Learning super-features for image retrieval.
  In *ICLR*, 2021.
- Welinder et al. (2010)

  P. Welinder, S. Branson, T. Mita, C. Wah, F. Schroff, S. Belongie, and
  P. Perona.
  Caltech-UCSD Birds 200.
  Technical Report CNS-TR-2010-001, 2010.
- Wenzek et al. (2020)

  Guillaume Wenzek, Marie-Anne Lachaux, Alexis Conneau, Vishrav Chaudhary,
  Francisco Guzmán, Armand Joulin, and Edouard Grave.
  Ccnet: Extracting high quality monolingual datasets from web crawl
  data.
  In *LREC*, 2020.
- Weyand et al. (2020)

  Tobias Weyand, Andre Araujo, Bingyi Cao, and Jack Sim.
  Google landmarks dataset v2 – a large-scale benchmark for
  instance-level recognition and retrieval.
  In *CVPR*, 2020.
- Wu et al. (2018)

  Zhirong Wu, Yuanjun Xiong, Stella X Yu, and Dahua Lin.
  Unsupervised feature learning via non-parametric instance
  discrimination.
  In *CVPR*, 2018.
- Xiao et al. (2010)

  J. Xiao, J. Hays, K. A. Ehinger, A. Oliva, and A. Torralba.
  Sun database: Large-scale scene recognition from abbey to zoo.
  In *CVPR*, 2010.
- Xu et al. (2022)

  Hu Xu, Juncheng Li, Alexei Baevski, Michael Auli, Wojciech Galuba, Florian
  Metze, Christoph Feichtenhofer, et al.
  Masked autoencoders that listen.
  *arXiv preprint arXiv:2207.06405*, 2022.
- Yalniz et al. (2019)

  I Zeki Yalniz, Hervé Jégou, Kan Chen, Manohar Paluri, and Dhruv
  Mahajan.
  Billion-scale semi-supervised learning for image classification.
  *arXiv preprint arXiv:1905.00546*, 2019.
- Yildiz et al. (2022)

  Burak Yildiz, Seyran Khademi, Ronald Maria Siebes, and Jan van Gemert.
  Amstertime: A visual place recognition benchmark dataset for severe
  domain shift.
  In *ICPR*, 2022.
- Ypsilantis et al. (2021)

  Nikolaos-Antonios Ypsilantis, Noa Garcia, Guangxing Han, Sarah Ibrahimi, Nanne
  Van Noord, and Giorgos Tolias.
  The met dataset: Instance-level recognition for artworks.
  In *NeurIPS Datasets and Benchmarks Track*, 2021.
- Zhai et al. (2022)

  Xiaohua Zhai, Alexander Kolesnikov, Neil Houlsby, and Lucas Beyer.
  Scaling vision transformers.
  In *CVPR*, 2022.
- Zhang et al. (2016)

  Richard Zhang, Phillip Isola, and Alexei A Efros.
  Colorful image colorization.
  In *ECCV*, 2016.
- Zhou et al. (2014)

  Bolei Zhou, Agata Lapedriza, Jianxiong Xiao, Antonio Torralba, and Aude Oliva.
  Learning deep features for scene recognition using places database.
  In *NeurIPS*, 2014.
- Zhou et al. (2017)

  Bolei Zhou, Hang Zhao, Xavier Puig, Sanja Fidler, Adela Barriuso, and Antonio
  Torralba.
  Scene parsing through ade20k dataset.
  In *CVPR*, 2017.
- Zhou et al. (2022a)

  Jinghao Zhou, Chen Wei, Huiyu Wang, Wei Shen, Cihang Xie, Alan Yuille, and Tao
  Kong.
  Ibot: Image bert pre-training with online tokenizer.
  In *ICLR*, 2022a.
- Zhou et al. (2022b)

  Pan Zhou, Yichen Zhou, Chenyang Si, Weihao Yu, Teck Khim Ng, and Shuicheng Yan.
  Mugs: A multi-granular self-supervised learning framework.
  *arXiv preprint arXiv:2203.14415*, 2022b.

## 附录 A 数据处理

### A.1 数据选择

我们用于构建 LVD-142M 的数据集选择详见 表 15。
这一集合旨在提供能很好覆盖各类下游视觉任务的图像，兼顾图像级与密集识别。

### A.2 图像相似度

我们使用余弦相似度来比较图像特征（无论是我们的特征，还是为去重生成的特征），相似度函数 $m$ 如下：

$$m(s,r)=\text{cosine-similarity}\left(f\left(s\right),f\left(r\right)\right)=\frac{f(s)\cdot f(r)}{\|f(s)\|_{2}\|f(r)\|_{2}}$$

其中 $s$ 和 $r$ 是要比较的一对图像，$f$ 是生成特征的模型。

### A.3 去重

##### 自去重。

为了对我们 13 亿张图像的未筛选数据源去重，我们计算并使用 Pizzi et al.（2022）生成的嵌入，检索每张图像的 $k=64$ 个最近邻（使用余弦相似度）。
仅考虑相似度 >0.6 的邻居，我们借助一个可扩展的不相交集合数据结构实现来提取关联 $k$-NN 图的连通分量。
然后我们对每个重复图像的连通分量只保留一个代表。
这产生了一个含 11 亿张图像的自去重数据源。

##### 相对去重

为了减少冗余，并正确评估我们特征的性能，我们丢弃自去重数据源中与评估数据集训练/测试划分过于相似的剩余图像。
为此，我们应用与自去重类似的流程，但采用更严格的相似度阈值 >0.45，这一次识别每张参考图像所属的重复分量（如果存在）并将其整体丢弃。
这产生了一个含 7.44 亿张图像的、经过自去重和相对去重的数据源。

### A.4 检索

我们采用两种方式通过检索来扩充数据集：基于样本的和基于簇的。
第一种，基于样本的方式，适用于大于 100 万张图像的数据集，即为要检索的数据集中的每张样本图像收集固定数量 $k$ 的最近邻图像，实际上相当于把数据集规模乘以 $k$。
我们对 Google Landmarks v2 和 ImageNet-22k 使用 $k=4$，但使用更大的 $k=32$，使这一特定检索成为我们 LVD-142M 数据集的核心部分。
对于较小的数据集，第二种方式，基于簇的方式，首先借助分布式 $k$-means 实现将我们的未筛选数据源聚类成 100,000 个独立的簇。
每个簇应捕获不同类型的图像概念和内容。
然后，我们从每个与被检索数据集的图像相关联、且多于 3 张图像的簇中选取 10,000 张图像。
由于对某些数据集这可能检索到非常多的图像，我们将此类检索限制在最多 100 万张，以维持 LVD-142M 内不同数据集之间的平衡。

| 任务 | 数据集 / 划分 | 图像数 | 检索方式 | 检索到的图像数 | 最终纳入 |
| --- | --- | --- | --- | --- | --- |
| 分类 | ImageNet-22k / – | 14,197,086 | 原样使用 | – | 14,197,086 |
| 分类 | ImageNet-22k / – | 14,197,086 | 基于样本 | 56,788,344 | 56,788,344 |
| 分类 | ImageNet-1k / train | 1,281,167 | 基于样本 | 40,997,344 | 40,997,344 |
| 细粒度分类 | Caltech 101 / train | 3,030 | 基于簇 | 2,630,000 | 1,000,000 |
| 细粒度分类 | CUB-200-2011 / train | 5,994 | 基于簇 | 1,300,000 | 1,000,000 |
| 细粒度分类 | DTD / train1 | 1,880 | 基于簇 | 1,580,000 | 1,000,000 |
| 细粒度分类 | FGVC-Aircraft / train | 3,334 | 基于簇 | 1,170,000 | 1,000,000 |
| 细粒度分类 | Flowers-102 / train | 1,020 | 基于簇 | 1,060,000 | 1,000,000 |
| 细粒度分类 | Food-101 / train | 75,750 | 基于簇 | 21,670,000 | 1,000,000 |
| 细粒度分类 | Oxford-IIIT Pet / trainval | 3,680 | 基于簇 | 2,750,000 | 1,000,000 |
| 细粒度分类 | Stanford Cars / train | 8,144 | 基于簇 | 7,220,000 | 1,000,000 |
| 细粒度分类 | SUN397 / train1 | 19,850 | 基于簇 | 18,950,000 | 1,000,000 |
| 细粒度分类 | Pascal VOC 2007 / train | 2,501 | 基于簇 | 1,010,000 | 1,000,000 |
| 分割 | ADE20K / train | 20,210 | 基于簇 | 20,720,000 | 1,000,000 |
| 分割 | Cityscapes / train | 2,975 | 基于簇 | 1,390,000 | 1,000,000 |
| 分割 | Pascal VOC 2012 (seg.) / trainaug | 1,464 | 基于簇 | 10,140,000 | 1,000,000 |
| 深度估计 | Mapillary SLS / train | 1,434,262 | 原样使用 | – | 1,434,262 |
| 深度估计 | KITTI / train (Eigen) | 23,158 | 基于簇 | 3,700,000 | 1,000,000 |
| 深度估计 | NYU Depth V2 / train | 24,231 | 基于簇 | 10,850,000 | 1,000,000 |
| 深度估计 | SUN RGB-D / train | 4,829 | 基于簇 | 4,870,000 | 1,000,000 |
| 检索 | Google Landmarks v2 / train (clean) | 1,580,470 | 原样使用 | – | 1,580,470 |
| 检索 | Google Landmarks v2 / train (clean) | 1,580,470 | 基于样本 | 6,321,880 | 6,321,880 |
| 检索 | AmsterTime / new | 1,231 | 基于簇 | 960,000 | 960,000 |
| 检索 | AmsterTime / old | 1,231 | 基于簇 | 830,000 | 830,000 |
| 检索 | Met / train | 397,121 | 基于簇 | 62,860,000 | 1,000,000 |
| 检索 | Revisiting Oxford / base | 4,993 | 基于簇 | 3,680,000 | 1,000,000 |
| 检索 | Revisiting Paris / base | 6,322 | 基于簇 | 3,660,000 | 1,000,000 |
| | | | | 总计 | 142,109,386 |

表 15：
我们的 LVD-142M 数据集构成。
我们报告了用于构建该数据集的数据集及其划分清单、它们的纳入方式（不经检索的原样使用，或基于样本/基于簇的检索）。
对于检索，我们标明实际检索到的图像数和最终纳入数据集的数量。
我们选择在预训练数据中纳入尽可能多的数据集，以覆盖尽可能多的领域。
我们保留了少数数据集不用，以便在预训练领域之外评估性能。
关于数据集用途的更多细节见表 18。

## 附录 B 实现细节

### B.1 无监督预训练

对于无监督预训练，我们基于 DINO 和 iBOT 代码库构建。我们使用表 16 所示的超参数、表 17 描述的 ViT 架构。

| 模型 | 架构 | 丢弃率 | 学习率 | 批大小 |
| --- | --- | --- | --- | --- |
| DINOv2-S（蒸馏） | ViT-S/14 | 0 | 1e-3 | 2048 |
| DINOv2-B（蒸馏） | ViT-B/14 | 0 | 1e-3 | 2048 |
| DINOv2-L（蒸馏） | ViT-L/14 | 0 | 1e-3 | 2048 |
| DINOv2-L（从零训练） | ViT-L/14 | 0.4 | 3.5e-4 | 3072 |
| DINOv2-g（从零训练） | ViT-g/14 | 0.4 | 3.5e-4 | 3072 |

表 16：
DINOv2-S、DINOv2-B、DINOv2-L 和 DINOv2-g 的训练超参数。
所有模型均运行 625k 次迭代，使用 AdamW 优化器、初始 LayerScale 值 1e-5、从 0.04 到 0.2 的权重衰减余弦日程、100k 次迭代的学习率预热、从 0.994 到 1 的教师动量余弦日程，并且我们在所有情况下以 float16 精度训练（DINO 头除外，我们将其梯度以 float32 归约）。

| 架构 | 嵌入维度 | 注意力头 | 层数 | FFN 层 |
| --- | --- | --- | --- | --- |
| ViT-S/14（蒸馏） | 384 | 6 | 12 | MLP |
| ViT-B/14（蒸馏） | 768 | 12 | 18 | MLP |
| ViT-L/14（蒸馏） | 1024 | 16 | 24 | MLP |
| ViT-L/14（从零训练） | 1024 | 16 | 24 | SwiGLU |
| ViT-g/14（从零训练） | 1536 | 24 | 40 | SwiGLU |

表 17：
本工作中使用的 ViT-S/B/L/g 网络的架构细节。蒸馏模型使用 MLP 前馈网络，从零训练时使用 SwiGLU（Shazeer, 2020）。

##### KoLeo 正则化。

我们对第一个全局裁剪的 class token 应用权重为 0.1 的 KoLeo 正则项，作用于单块 GPU 内的所有样本，此步骤不进行跨 GPU 通信。

##### 教师的 EMA 更新。

教师以与学生相同的状态初始化，是学生网络的指数移动平均，动量值在 [0.994, 1.0] 区间内按余弦日程变化。它在每个训练步结束时更新。

### B.2 高分辨率适配

我们用预训练权重初始化模型，然后按与原始预训练相同的流程训练 10k 次迭代。所有日程保持与原始训练相同，但压缩到 10k 次迭代内。所有超参数与第一次预训练保持一致，仅基础学习率降低。

### B.3 线性探测评估

对于线性探测，我们定义 3 个评估参数：学习率、使用多少输出层、是否将平均池化的图块 token 特征与 class token 拼接（或只使用 class token）。
我们用 SGD 训练线性层 12500 次迭代，使用 random-resized-crop 数据增强，并进行以下网格搜索：

- 学习率取值于 $\{0.0001,0.0002,0.0005,0.001,0.002,0.005,0.01,0.02,0.05,0.1,0.2,0.3,0.5\}$
- 输出层取值于 $\{1,4\}$
- 是否拼接平均池化 token 取值于 $\{是,否\}$

然后我们按常见做法报告验证集上取得的最高准确率。
注意该网格搜索开销不大，因为每次迭代我们只在主干上执行一次推理，然后将输出送入所有线性分类器（每个只执行一次矩阵乘法）。

## 附录 C 使用的数据集清单

我们在表 18 中展示所用基准和数据集的清单及其用途。

| 数据集 | 预训练（原样使用） | 检索预训练数据 | 评测 | 任务 | 引用 |
| --- | --- | --- | --- | --- | --- |
| ImageNet-1k | ✗ | ✓ | ✓ | 分类 | (Russakovsky et al., 2015) |
| ImageNet-22k | ✓ | ✓ | ✗ | | (Deng et al., 2009) |
| ImageNet-V2 | ✗ | ✗ | ✓ | 分类 | (Recht et al., 2019) |
| ImageNet-ReaL | ✗ | ✗ | ✓ | 分类 | (Beyer et al., 2020) |
| ImageNet-A | ✗ | ✗ | ✓ | 分类 | (Hendrycks et al., 2021b) |
| ImageNet-C | ✗ | ✗ | ✓ | 分类 | (Hendrycks & Dietterich, 2019) |
| ImageNet-R | ✗ | ✗ | ✓ | 分类 | (Hendrycks et al., 2021a) |
| ImageNet-Sk. | ✗ | ✗ | ✓ | 分类 | (Wang et al., 2019) |
| Food-101 | ✗ | ✓ | ✓ | 分类 | (Bossard et al., 2014) |
| CIFAR-10 | ✗ | ✓ | ✓ | 分类 | (Krizhevsky et al., 2009) |
| CIFAR-100 | ✗ | ✓ | ✓ | 分类 | (Krizhevsky et al., 2009) |
| SUN397 | ✗ | ✓ | ✓ | 分类 | (Xiao et al., 2010) |
| StanfordCars | ✗ | ✓ | ✓ | 分类 | (Krause et al., 2013) |
| FGVC-Aircraft | ✗ | ✓ | ✓ | 分类 | (Maji et al., 2013) |
| VOC 2007 | ✗ | ✓ | ✓ | 分类 | (Everingham et al., 2010) |
| DTD | ✗ | ✓ | ✓ | 分类 | (Cimpoi et al., 2014) |
| Oxford Pets | ✗ | ✓ | ✓ | 分类 | (Parkhi et al., 2012) |
| Caltech101 | ✗ | ✓ | ✓ | 分类 | (Fei-Fei et al., 2004) |
| Flowers | ✗ | ✓ | ✓ | 分类 | (Nilsback & Zisserman, 2008) |
| CUB200 | ✗ | ✓ | ✓ | 分类 | (Welinder et al., 2010) |
| iNaturalist 2018 | ✗ | ✗ | ✓ | 分类 | (Van Horn et al., 2018) |
| iNaturalist 2021 | ✗ | ✗ | ✓ | 分类 | (Van Horn et al., 2021) |
| Places-205 | ✗ | ✗ | ✓ | 分类 | (Zhou et al., 2014) |
| UCF101 | ✗ | ✗ | ✓ | 视频 | (Soomro et al., 2012) |
| Kinetics-400 | ✗ | ✗ | ✓ | 视频 | (Kay et al., 2017) |
| SSv2 | ✗ | ✗ | ✓ | 视频 | (Goyal et al., 2017) |
| GLD v2 | ✓ | ✓ | ✗ | | (Weyand et al., 2020) |
| R-Paris | ✗ | ✓ | ✓ | 检索 | (Radenović et al., 2018a) |
| R-Oxford | ✗ | ✓ | ✓ | 检索 | (Radenović et al., 2018a) |
| Met | ✗ | ✓ | ✓ | 检索 | (Ypsilantis et al., 2021) |
| Amstertime | ✗ | ✓ | ✓ | 检索 | (Yildiz et al., 2022) |
| ADE20k | ✗ | ✓ | ✓ | 分割 | (Zhou et al., 2017) |
| Cityscapes | ✗ | ✓ | ✓ | 分割 | (Cordts et al., 2016) |
| VOC 2012 | ✗ | ✓ | ✓ | 分割 | (Everingham et al., 2010) |
| Mapillary SLS | ✓ | ✗ | ✗ | | (Warburg et al., 2020) |
| NYU-Depth V2 | ✗ | ✓ | ✓ | 深度 | (Silberman et al., 2012) |
| KITTI | ✗ | ✓ | ✓ | 深度 | (Geiger et al., 2013) |
| SUN-RGBD | ✗ | ✓ | ✓ | 深度 | (Song et al., 2015) |
| DollarStreet | ✗ | ✗ | ✓ | 公平性 | (De Vries et al., 2019) |
| Casual Conv. | ✗ | ✗ | ✓ | 公平性 | (Hazirbas et al., 2021) |

表 18：
使用的数据集清单。
