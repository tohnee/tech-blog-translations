---
title: "Segment Anything（分割一切）"
title_en: "Segment Anything"
arxiv: 2304.02643
date: 2023-04-05
source: https://arxiv.org/abs/2304.02643
crawled: 2026-09-22
translated: 2026-09-22
---

# Segment Anything（分割一切）

> 原文：[Segment Anything](https://arxiv.org/abs/2304.02643) · Meta AI（FAIR）arXiv

Alexander Kirillov　Eric Mintun　Nikhila Ravi　Hanzi Mao　Chloe Rolland　Laura Gustafson

Tete Xiao　Spencer Whitehead　Alexander C. Berg　Wan-Yen Lo　Piotr Dollár　Ross Girshick

Meta AI Research, FAIR（项目负责人　共同第一作者　同等贡献　方向负责人）

###### 摘要

我们提出「Segment Anything（分割一切，SA）」项目：面向图像分割的一项新任务、一个新模型和一个新数据集。利用我们的高效模型构建数据收集闭环，我们构建了迄今（远远）最大的分割数据集——在 1100 万张（11M）已授权且尊重隐私的图像上标注了超过 10 亿（1B）个掩码。该模型在设计与训练上支持可提示（promptable）使用，因此能够零样本迁移到新的图像分布与任务。我们在众多任务上评估其能力，发现其零样本性能令人印象深刻——往往能与以往全监督结果竞争，甚至更优。我们在 <https://segment-anything.com> 发布分割一切模型（Segment Anything Model，SAM）及对应的数据集（SA-1B，包含 10 亿掩码与 1100 万张图像），以推动计算机视觉基座模型（foundation model）的研究。

![图 1](2304.02643v1/teaser.png)

图 1：我们旨在通过引入三个相互关联的组件来构建分割领域的基座模型：一个可提示的分割*任务*、一个为数据标注提供支撑并可通过提示工程零样本迁移到一系列任务的分割*模型*（SAM），以及一个用于收集 SA-1B（我们超过 10 亿掩码的数据集）的*数据*引擎。

## 1 引言

在网页级数据集上预训练的大型语言模型正凭借强大的零样本与少样本泛化能力变革自然语言处理（NLP）[[10](#bib.bib10)]。这类「基座模型」[[8](#bib.bib8)]能够泛化到训练之外的任务和数据分布。这种能力通常通过*提示工程*（prompt engineering）实现：用手工构造的文本来提示语言模型，使其针对当前任务生成有效的文本回应。当以海量网页文本语料进行规模化训练后，这些模型的零样本与少样本性能可与微调模型出人意料地接近（在某些情况下甚至相当）[[10](#bib.bib10), [21](#bib.bib21)]。经验趋势表明，这一表现会随模型规模、数据集规模和总训练算力的增长而提升 [[56](#bib.bib56), [10](#bib.bib10), [21](#bib.bib21), [51](#bib.bib51)]。

基座模型在计算机视觉领域也已得到探索，只是程度较轻。或许最突出的例子是对来自网页的成对文本与图像进行对齐。例如，CLIP [[82](#bib.bib82)] 与 ALIGN [[55](#bib.bib55)] 使用对比学习训练文本编码器与图像编码器以对齐这两种模态。训练完成后，经过设计的文本提示即可实现对新颖视觉概念与数据分布的零样本泛化。这类编码器还能与其他模块有效组合以支撑下游任务，例如图像生成（如 DALL·E [[83](#bib.bib83)]）。尽管视觉-语言编码器已取得长足进展，计算机视觉仍包含大量超出该范畴的问题，而对其中许多问题而言，并不存在充足的训练数据。

在本工作中，我们的目标是构建*图像分割的基座模型*。也就是说，我们希望开发一个可提示的模型，并用一个能带来强大泛化能力的任务在广泛的数据集上对其进行预训练。借助该模型，我们旨在通过提示工程在新的数据分布上解决一系列下游分割问题。

这一计划的成败取决于三个要素：任务、模型和数据。为了开发它们，我们围绕图像分割回答以下问题：

1. 什么任务能够实现零样本泛化？
2. 对应的模型架构是什么？
3. 什么数据能够驱动这一任务与模型？

这些问题相互交织，需要一套综合方案。我们首先定义一个*可提示分割*任务，它足够通用，既能提供强大的预训练目标，又能支撑广泛的下游应用。该任务要求模型支持灵活的提示，并能在收到提示后实时输出分割掩码，以便交互式使用。为训练模型，我们需要多样化、大规模的数据来源。遗憾的是，分割领域并不存在网页级的数据源；为此，我们构建了一个「数据引擎」，即在「用高效模型辅助数据收集」与「用新收集的数据改进模型」之间反复迭代。下面我们依次介绍这些相互关联的组件，随后介绍我们创建的数据集以及验证我们方法有效性的实验。

#### 任务（§2）。

在 NLP 以及近来的计算机视觉中，基座模型是一项令人期待的发展，它们通常借助「提示」技术对新数据集和新任务进行零样本与少样本学习。受这一方向启发，我们提出*可提示分割任务*：给定任意分割*提示*，返回一个*有效*的分割掩码（见图 1(a)）。提示只是指定在图像中分割什么，例如，提示可以包含指明某个物体的空间信息或文本信息。要求输出掩码有效意味着：即使提示有歧义、可能指向多个物体（例如，落在衬衫上的一个点既可能指衬衫，也可能指穿着衬衫的人），输出也应是其中至少一个物体的合理掩码。我们将可提示分割任务同时用作预训练目标，并通过提示工程来解决一般的下游分割任务。

#### 模型（§3）。

可提示分割任务与实际应用目标对模型架构提出了约束。具体而言，模型必须支持*灵活的提示*，需要以摊销*实时*的速度计算掩码以支持交互式使用，还必须*具备歧义感知能力*。令人惊讶的是，我们发现一个简单的设计即可同时满足这三项约束：一个强大的图像编码器计算图像嵌入，一个提示编码器嵌入提示，随后这两路信息在一个轻量级掩码解码器中融合并预测分割掩码。我们将该模型称为分割一切模型（Segment Anything Model，SAM）（见图 1(b)）。通过将 SAM 拆分为图像编码器与快速的提示编码器/掩码解码器，同一图像嵌入可以被不同的提示复用（其成本也被摊销）。给定图像嵌入后，提示编码器与掩码解码器在网页浏览器中约 50ms 即可从提示预测出掩码。我们聚焦于点、框和掩码提示，并给出自由格式文本提示的初步结果。为使 SAM 具备歧义感知能力，我们将其设计为对单个提示预测多个掩码，使 SAM 能自然地处理歧义，例如前述衬衫*对*人的例子。

#### 数据引擎（§4）。

为了实现对新数据分布的强泛化，我们发现有必要在远超任何现有分割数据集的大规模、多样化掩码集合上训练 SAM。基座模型的典型做法是从网络上获取数据 [[82](#bib.bib82)]，但掩码在网络上并不天然丰富，因此我们需要另一种策略。我们的解决方案是构建一个「数据引擎」，即让模型与「模型在环」的数据集标注协同演进（见图 1(c)）。我们的数据引擎分为三个阶段：*辅助人工*、*半自动*和*全自动*。第一阶段，SAM 辅助标注者标注掩码，类似于经典的交互式分割设置。第二阶段，通过用可能的目标位置提示 SAM，使其自动为一部分物体生成掩码，标注者专注于标注其余物体，这有助于提升掩码多样性。最后阶段，我们用规则的前景点网格提示 SAM，平均每张图像得到约 100 个高质量掩码。

#### 数据集（§5）。

我们的最终数据集 SA-1B 包含来自 1100 万张（11M）已授权且保护隐私图像的超过 *10 亿（1B）*个掩码（见图 2）。SA-1B 完全使用数据引擎最后阶段全自动收集，其掩码数量是任何现有分割数据集的 400 倍 [[66](#bib.bib66), [44](#bib.bib44), [117](#bib.bib117), [60](#bib.bib60)]，而且如我们广泛验证的那样，这些掩码具有高质量与高多样性。除了用于训练出稳健且泛化的 SAM 之外，我们希望 SA-1B 能成为旨在构建新基座模型的研究的宝贵资源。

#### 负责任 AI（§6）。

我们研究并报告了使用 SA-1B 与 SAM 时潜在的公平性顾虑与偏见。SA-1B 的图像覆盖了地理与经济上多样化的国家，我们发现 SAM 在不同人群上的表现相近。我们希望这些努力能让本工作在实际应用场景中更加公平。附录中提供了模型卡与数据集卡。

#### 实验（§7）。

我们对 SAM 进行了广泛评估。首先，使用一个由 23 个分割数据集组成的多样化新套件，我们发现 SAM 仅凭单个前景点就能生成高质量掩码，往往只是略低于人工标注的真值。其次，在零样本迁移协议下，通过提示工程，我们在多种下游任务上取得了持续强劲的定量与定性结果，包括边缘检测、物体候选框生成、实例分割，以及文本到掩码预测的初步探索。这些结果表明，SAM 可以通过提示工程开箱即用地解决涉及 SAM 训练数据之外的物体与图像分布的多种任务。当然，改进空间依然存在，我们在 §8 中讨论。

#### 发布。

我们以研究目的发布 SA-1B 数据集，并以宽松的开源许可证（Apache 2.0）在 <https://segment-anything.com> 开放 SAM。我们还通过[在线演示](https://segment-anything.com/demo)展示 SAM 的能力。

<50 个掩码
![](2304.02643v1/figs/sa1b_examples/9_sa_1192782.jpg)
![](2304.02643v1/figs/sa1b_examples/25_sa_864082.jpg)
![](2304.02643v1/figs/sa1b_examples/32_sa_8234897.jpg)
![](2304.02643v1/figs/sa1b_examples/45_sa_4298678.jpg)

50-100 个掩码
![](2304.02643v1/figs/sa1b_examples/67_sa_1468983.jpg)
![](2304.02643v1/figs/sa1b_examples/61_sa_2146330.jpg)
![](2304.02643v1/figs/sa1b_examples/66_sa_9307564.jpg)
![](2304.02643v1/figs/sa1b_examples/65_sa_2889438.jpg)

100-200 个掩码
![](2304.02643v1/figs/sa1b_examples/187_sa_7694512.jpg)
![](2304.02643v1/figs/sa1b_examples/145_sa_3647402.jpg)
![](2304.02643v1/figs/sa1b_examples/116_sa_6137832.jpg)
![](2304.02643v1/figs/sa1b_examples/154_sa_2945741.jpg)

200-300 个掩码
![](2304.02643v1/figs/sa1b_examples/208_sa_6808005.jpg)
![](2304.02643v1/figs/sa1b_examples/230_sa_6506882.jpg)
![](2304.02643v1/figs/sa1b_examples/250_sa_9338205.jpg)
![](2304.02643v1/figs/sa1b_examples/221_sa_9820072.jpg)

300-400 个掩码
![](2304.02643v1/figs/sa1b_examples/360_sa_5537747.jpg)
![](2304.02643v1/figs/sa1b_examples/318_sa_7769360.jpg)
![](2304.02643v1/figs/sa1b_examples/304_sa_1437195.jpg)
![](2304.02643v1/figs/sa1b_examples/317_sa_7651290.jpg)

400-500 个掩码
![](2304.02643v1/figs/sa1b_examples/456_sa_11107398.jpg)
![](2304.02643v1/figs/sa1b_examples/452_sa_10129735.jpg)
![](2304.02643v1/figs/sa1b_examples/438_sa_1596486.jpg)
![](2304.02643v1/figs/sa1b_examples/401_sa_10771020.jpg)

>500 个掩码
![](2304.02643v1/figs/sa1b_examples/783_sa_3805502.jpg)
![](2304.02643v1/figs/sa1b_examples/823_sa_11048476.jpg)
![](2304.02643v1/figs/sa1b_examples/576_sa_10463977.jpg)
![](2304.02643v1/figs/sa1b_examples/579_sa_1232910.jpg)

图 2：我们新引入的数据集 SA-1B 中叠加了掩码的示例图像。SA-1B 包含 1100 万张多样化、高分辨率、已授权且保护隐私的图像，以及 11 亿个高质量分割掩码。这些掩码完全由 SAM *全自动*标注，并且正如我们通过人工评分与大量实验所验证的，它们具有高质量与高多样性。为便于可视化，我们按每张图像的掩码数量对图像分组（平均每张图像约 100 个掩码）。

## 2 分割一切任务

我们从 NLP 中汲取灵感：下一词元预测任务既被用于基座模型预训练，*也*通过提示工程被用来解决多样的下游任务 [[10](#bib.bib10)]。为构建分割的基座模型，我们旨在定义一个具有类似能力的任务。

#### 任务。

我们首先把 NLP 中「提示」的概念迁移到分割领域：提示可以是一组前景/背景点、一个粗略的框或掩码、自由格式的文本，或者泛而言之，任何指明在图像中分割什么的信息。于是，*可提示分割任务*就是给定任意*提示*时返回一个*有效*的分割掩码。对「有效」掩码的要求只是意味着：即使某个提示是*歧义*的、可能指向多个物体（例如回顾衬衫*对*人的例子，见图 3），输出也应是其中至少*一个*物体的合理掩码。这一要求类似于期望语言模型对歧义提示输出连贯回应。我们选择这一任务，是因为它自然地导出一种预训练算法，*并且*给出一种通过提示零样本迁移到下游分割任务的通用方法。

#### 预训练。

可提示分割任务提示了一种自然的预训练算法：为每个训练样本模拟一系列提示（如点、框、掩码），并将模型的掩码预测与真值进行比较。这一方法改编自交互式分割 [[109](#bib.bib109), [70](#bib.bib70)]，但与交互式分割——其目标是在足够的用户输入后最终预测出有效掩码——不同，我们的目标是即使提示*有歧义*，也始终为*任意提示*预测出*有效掩码*。这确保了预训练模型在涉及歧义的使用场景（包括我们数据引擎 §4 所需的自动标注）中依然有效。我们注意到，在该任务上表现出色颇具挑战性，需要专门的建模与训练损失选择，我们将在 §3 中讨论。

#### 零样本迁移。

直观地说，我们的预训练任务赋予模型在推理时对任意提示做出恰当回应的能力，因此可以通过设计合适的提示来解决下游任务。例如，如果已有一个猫的边界框检测器，就可以把该检测器的框输出作为提示提供给我们模型，从而解决猫的实例分割。一般而言，大量实际的分割任务都可以转化为提示。除了自动数据集标注之外，我们还在 §7 的实验中探索了五个多样化的示例任务。

![](2304.02643v1/ambiguity_examples.png)

图 3：每列展示 SAM 从单个歧义点提示（绿色圆圈）生成的 3 个有效掩码。

#### 相关任务。

分割是一个宽泛的领域：包括交互式分割 [[57](#bib.bib57), [109](#bib.bib109)]、边缘检测 [[3](#bib.bib3)]、超像素化 [[85](#bib.bib85)]、物体候选框生成 [[2](#bib.bib2)]、前景分割 [[94](#bib.bib94)]、语义分割 [[90](#bib.bib90)]、实例分割 [[66](#bib.bib66)]、全景分割 [[59](#bib.bib59)] 等。我们的可提示分割任务的目标是产出一个能力广泛的模型，可通过提示工程适应*许多*（尽管不是全部）现有及*新*的分割任务。这种能力是任务泛化的一种形式 [[26](#bib.bib26)]。注意，这与以往的多任务分割系统不同。在多任务系统中，单个模型执行*固定*的一组任务，例如联合语义、实例与全景分割 [[114](#bib.bib114), [19](#bib.bib19), [54](#bib.bib54)]，但其训练任务与测试任务相同。我们工作中一个重要区别是：为可提示分割训练的模型可以在推理时作为一个更大系统中的*组件*去执行一个新的、不同的任务，例如要做实例分割时，可提示分割模型需与现有物体检测器*组合*使用。

#### 讨论。

提示与组合是让单个模型以可扩展方式使用的强大工具，甚至有望完成模型设计时未知的应用任务。这种方式与其他基座模型的用法类似，例如 CLIP [[82](#bib.bib82)] 是 DALL·E [[83](#bib.bib83)] 图像生成系统中的文本-图像对齐组件。我们预期，由提示工程等技术驱动的可组合系统设计，将比专门针对固定任务集合训练的系统支撑更丰富多样的应用。通过组合的视角比较可提示分割与交互式分割也颇有意味：交互式分割模型以人类用户为设计对象，而正如我们将要演示的，为可提示分割训练的模型同样可以组合进更大的算法系统。

![](2304.02643v1/model_diagram.png)

图 4：分割一切模型（SAM）概览。一个重量级图像编码器输出图像嵌入，随后可被多种输入提示高效查询，以摊销实时的速度产生物体掩码。对于对应多个物体的歧义提示，SAM 可以输出多个有效掩码及相应的置信度分数。

## 3 分割一切模型

接下来我们描述用于可提示分割的分割一切模型（SAM）。SAM 有三个组件，如图 4 所示：图像编码器、灵活的提示编码器和快速的掩码解码器。我们基于 Transformer 视觉模型 [[14](#bib.bib14), [33](#bib.bib33), [20](#bib.bib20), [62](#bib.bib62)] 构建，并针对（摊销）实时性能做了特定权衡。我们在此从高层描述这些组件，细节见附录 A。

#### 图像编码器。

出于可扩展性与强大预训练方法的考虑，我们使用经 MAE [[47](#bib.bib47)] 预训练、并做了最小改动以处理高分辨率输入 [[62](#bib.bib62)] 的 Vision Transformer（ViT）[[33](#bib.bib33)]。图像编码器每张图像只运行一次，可以在提示模型之前预先完成。

#### 提示编码器。

我们考虑两组提示：*稀疏*（点、框、文本）与*稠密*（掩码）。点和框用位置编码 [[95](#bib.bib95)] 与每种提示类型的学习嵌入相加来表示，自由格式文本则使用 CLIP [[82](#bib.bib82)] 的现成文本编码器嵌入。稠密提示（即掩码）通过卷积嵌入，并与图像嵌入逐元素相加。

#### 掩码解码器。

掩码解码器高效地将图像嵌入、提示嵌入与一个输出词元映射为掩码。这一设计受 [[14](#bib.bib14), [20](#bib.bib20)] 启发，采用改进的 Transformer 解码器块 [[103](#bib.bib103)] 后接动态掩码预测头。我们改进的解码器块使用提示自注意力与双向（提示到图像嵌入以及反向）交叉注意力来更新*所有*嵌入。运行两个块之后，我们对图像嵌入上采样，并由一个 MLP 将输出词元映射为动态线性分类器，进而在每个图像位置计算掩码前景概率。

#### 消解歧义。

若只有一个输出，模型在给定歧义提示时会把多个有效掩码取平均。为解决这一问题，我们修改模型使其对单个提示预测多个输出掩码（见图 3）。我们发现 3 个掩码输出足以应对最常见的情况（嵌套掩码通常最多三层：整体、部分、子部分）。训练时，我们只对掩码中*最小*的损失进行反向传播 [[15](#bib.bib15), [45](#bib.bib45), [64](#bib.bib64)]。为对掩码排序，模型为每个掩码预测一个置信度分数（即估计的 IoU）。

#### 效率。

整体模型设计在很大程度上出于效率考虑。给定预计算的图像嵌入，提示编码器与掩码解码器可在网页浏览器中、CPU 上约 50ms 内运行。这一运行性能使我们模型的无缝实时交互提示成为可能。

#### 损失与训练。

我们使用 [[14](#bib.bib14)] 中采用的 focal loss [[65](#bib.bib65)] 与 dice loss [[73](#bib.bib73)] 的线性组合来监督掩码预测。我们使用几何提示的混合来训练可提示分割任务（文本提示见 §7.5）。参照 [[92](#bib.bib92), [37](#bib.bib37)]，我们通过每个掩码随机采样提示、模拟 11 轮交互设置，使 SAM 能够无缝融入我们的数据引擎。

## 4 分割一切数据引擎

由于分割掩码在互联网上并不丰富，我们构建了一个数据引擎来支撑 11 亿掩码数据集 SA-1B 的收集。数据引擎分为三个阶段：(1) 模型辅助的人工标注阶段，(2) 自动预测掩码与模型辅助标注混合的半自动阶段，(3) 模型在无标注者输入情况下生成掩码的全自动阶段。下面逐一详述。

#### 辅助人工阶段。

第一阶段类似经典交互式分割：一支专业标注团队使用由 SAM 驱动的浏览器交互式分割工具，通过点击前景/背景物体点来标注掩码。掩码可用像素级精确的「画笔」与「橡皮擦」工具细化。我们的模型辅助标注直接在浏览器中实时运行（使用预计算的图像嵌入），带来真正的交互式体验。我们没有对标注物体施加语义约束，标注者自由标注「stuff（材料类）」与「things（物体类）」[[1](#bib.bib1)]。我们建议标注者标注他们能命名或描述的物体，但没有收集这些名称或描述。标注者被要求按显著程度依次标注物体，并且一旦某个掩码的标注时间超过 30 秒，就被鼓励进入下一张图像。

在该阶段开始时，SAM 使用常见的公开分割数据集训练。在积累了足够的数据标注后，SAM 仅用新标注的掩码重新训练。随着收集到更多掩码，图像编码器从 ViT-B 扩展到 ViT-H，其他架构细节也在演进；我们总共重新训练模型 6 次。随着模型改进，每个掩码的平均标注时间从 34 秒降至 14 秒。我们注意到，14 秒比 COCO [[66](#bib.bib66)] 的掩码标注快 6.5 倍，仅比使用极值点的边界框标注慢 2 倍 [[76](#bib.bib76), [71](#bib.bib71)]。随着 SAM 改进，每张图像的平均掩码数从 20 增加到 44。总体而言，我们在该阶段从 12 万张图像中收集了 430 万个掩码。

#### 半自动阶段。

在此阶段，我们的目标是提升掩码的*多样性*，以改进模型分割一切的能力。为了让标注者聚焦于不那么显著的物体，我们首先自动检测高置信度的掩码。然后，我们向标注者展示预填充了这些掩码的图像，请他们标注任何额外的未标注物体。为了检测高置信度掩码，我们在第一阶段全部掩码上以通用的「物体」类别训练了一个边界框检测器 [[84](#bib.bib84)]。在此阶段，我们在 18 万张图像中额外收集了 590 万个掩码（总计 1020 万个）。与第一阶段一样，我们定期用新收集的数据重新训练模型（5 次）。由于这些物体更难标注，每个掩码的平均标注时间回升至 34 秒（不含自动生成的掩码）。每张图像的平均掩码数从 44 增至 72（含自动掩码）。

#### 全自动阶段。

在最后阶段，标注*完全自动化*。这得益于我们模型的两项重大改进。其一，在该阶段开始时，我们已收集到足以大幅改进模型的掩码，其中包括上一阶段的多样化掩码。其二，到该阶段我们已开发出歧义感知模型，即使在歧义情形下也能预测有效掩码。具体而言，我们用 32×32 的规则点网格提示模型，并为每个点预测一组可能对应有效物体的掩码。借助歧义感知模型，如果一个点落在某个部分或子部分上，我们的模型会返回子部分、部分与整体物体。我们使用模型的 IoU 预测模块来选择*高置信度*掩码；此外，我们还识别并仅选择*稳定*的掩码（若将概率图分别在 0.5−δ 与 0.5+δ 处阈值化得到相似掩码，则认为该掩码稳定）。最后，在选出高置信度且稳定的掩码后，我们应用非极大值抑制（NMS）过滤重复。为进一步提升较小掩码的质量，我们还处理了多个重叠的放大图像裁剪。该阶段的更多细节见附录 B。我们对数据集中的全部 1100 万张图像应用全自动掩码生成，共产生 11 亿个高质量掩码。下面对由此得到的数据集 SA-1B 进行描述与分析。

![](2304.02643v1/figs/center_distribution.png)

图 5：按图像尺寸归一化的掩码中心分布。

图 6：数据集掩码属性。图例注明了每个数据集的图像数与掩码数。注意，SA-1B 的图像数是现有最大分割数据集 Open Images [[60](#bib.bib60)] 的 11 倍，掩码数是其 400 倍。

## 5 分割一切数据集

我们的数据集 SA-1B 由 1100 万张多样化、高分辨率、已授权且保护隐私的图像，以及用数据引擎收集的 11 亿个高质量分割掩码组成。我们将 SA-1B 与现有数据集比较，并分析掩码质量与属性。我们发布 SA-1B 以助力计算机视觉基座模型的未来发展。我们注意到，SA-1B 将以对特定研究用途友好的许可协议发布，并为研究人员提供保护。

#### 图像。

我们从一家与摄影师直接合作的提供商授权了 1100 万张新图像。这些图像分辨率很高（平均 3300×4950 像素），由此产生的数据规模可能带来访问与存储挑战。因此，我们发布的是短边缩放到 1500 像素的下采样图像。即便经过下采样，我们的图像分辨率仍显著高于许多现有视觉数据集（例如 COCO [[66](#bib.bib66)] 图像约为 480×640 像素）。注意，今天的大多数模型在低得多的输入分辨率上运行。发布图像中的人脸与车辆牌照已做模糊处理。

#### 掩码。

我们的数据引擎产生了 11 亿个掩码，其中 99.1% 完全自动生成。因此，自动掩码的质量至关重要。我们将其与专业标注直接比较，并考察各种掩码属性与知名分割数据集的对比。我们的主要结论（由下述分析及 §7 实验支持）是：自动掩码质量高，且用于训练模型行之有效。基于这些发现，SA-1B *仅包含自动生成的掩码。*

#### 掩码质量。

为估计掩码质量，我们随机抽取了 500 张图像（约 5 万个掩码），请专业标注者提升这些图像中所有掩码的质量。标注者使用我们的模型和像素级精确的「画笔」「橡皮擦」编辑工具完成此项工作。这一流程产生了成对的自动预测掩码与专业修正掩码。我们计算每对掩码的 IoU，发现 94% 的掩码对 IoU 大于 90%（97% 的掩码对 IoU 大于 75%）。作为比较，以往工作估计标注者间一致性为 85-91% IoU [[44](#bib.bib44), [60](#bib.bib60)]。§7 中的实验通过人工评分证实，相对多种数据集其掩码质量都很高，且在自动掩码上训练模型的效果几乎与使用数据引擎产出的全部掩码一样好。

![](2304.02643v1/ablation_sa1b_geography.png)

图 7：SA-1B 图像的估计地理分布。世界上大多数国家在 SA-1B 中拥有超过 1000 张图像，且图像数量最多的三个国家来自世界不同地区。

#### 掩码属性。

在图 5 中，我们绘制了 SA-1B 与现有最大分割数据集的物体中心空间分布对比。所有数据集都存在常见的摄影师偏差。我们观察到，与分布最相近的两个数据集 LVIS v1 [[44](#bib.bib44)] 和 ADE20K [[117](#bib.bib117)] 相比，SA-1B 对图像四角的覆盖更广，而 COCO [[66](#bib.bib66)] 与 Open Images V5 [[60](#bib.bib60)] 的中心偏差更明显。在图 6（图例）中，我们按规模比较这些数据集。SA-1B 的图像数是第二大者 Open Images 的 11 倍，掩码数是其 400 倍。平均而言，其每张图像的掩码数是 Open Images 的 36 倍。这方面最接近的数据集 ADE20K，其每张图像的掩码数仍少 3.5 倍。图 6（左）绘制了每张图像掩码数的分布。接着，我们在图 6（中）中考察相对图像的掩码尺寸（掩码面积的平方根除以图像面积）。不出所料，由于我们的数据集每张图像掩码更多，中小相对尺寸掩码的占比也趋于更高。最后，为分析形状复杂度，我们在图 6（右）中考察掩码凹度（1 减去掩码面积除以掩码凸包面积）。由于形状复杂度与掩码尺寸相关，我们先对掩码尺寸分箱做分层抽样，以控制各数据集的掩码尺寸分布。我们观察到，我们掩码的凹度分布与其他数据集大体相似。

## 6 分割一切 RAI 分析

接下来，我们通过考察使用 SA-1B 与 SAM 时潜在的公平性顾虑与偏见，对本工作进行负责任 AI（RAI）分析。我们聚焦 SA-1B 的地理与收入分布，以及 SAM 在人物受保护属性上的公平性。我们还在附录 F 中提供数据集卡、数据标注卡与模型卡。

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
|  |  | SA-1B | | 图像占比 | | |
|  | 国家数 | 图像数 | 掩码数 | SA-1B | COCO | O.I. |
| 非洲 | 54 | 300k | 28M | 2.8% | 3.0% | 1.7% |
| 亚洲与大洋洲 | 70 | 3.9M | 423M | 36.2% | 11.4% | 14.3% |
| 欧洲 | 47 | 5.4M | 540M | 49.8% | 34.2% | 36.2% |
| 拉丁美洲与加勒比 | 42 | 380k | 36M | 3.5% | 3.1% | 5.0% |
| 北美洲 | 4 | 830k | 80M | 7.7% | 48.3% | 42.8% |
| 高收入国家 | 81 | 5.8M | 598M | 54.0% | 89.1% | 87.5% |
| 中等收入国家 | 108 | 4.9M | 499M | 45.0% | 10.5% | 12.0% |
| 低收入国家 | 28 | 100k | 9.4M | 0.9% | 0.4% | 0.5% |

表 1：地理与收入代表性比较。SA-1B 在欧洲、亚洲与大洋洲以及中等收入国家中的代表性更高。来自非洲、拉丁美洲与加勒比以及低收入国家的图像在所有数据集中均代表性不足。

#### 地理与收入代表性。

我们用标准方法推断图像拍摄所在国家（见附录 C）。在图 7 中，我们可视化了 SA-1B 中各国图像数量（左）以及图像数最多的 50 个国家（右）。我们注意到图像数前三的国家来自世界不同地区。接着在表 1 中，我们比较了 SA-1B、COCO [[66](#bib.bib66)] 与 Open Images [[60](#bib.bib60)] 的地理与收入代表性。SA-1B 在欧洲与亚洲大洋洲以及中等收入国家的图像占比显著更高。所有数据集对非洲及低收入国家的代表性都不足。我们注意到，在 SA-1B 中，包括非洲在内的所有区域都至少有 2800 万个掩码，是任何以往数据集掩码*总*数的 10 倍以上。最后，我们观察到每张图像的平均掩码数（未展示）在各区域与收入组之间相当一致（每张 94-108 个）。

#### 人物分割的公平性。

我们通过测量 SAM 在不同群体间的性能差异，考察感知性别表现、感知年龄段与感知肤色方面潜在的公平性问题。性别表现与年龄使用 More Inclusive Annotations for People（MIAP）数据集 [[87](#bib.bib87)]，肤色使用一个专有数据集（见附录 C）。我们的评估采用随机采样 1 点与 3 点的模拟交互式分割（见附录 D）。表 2（左上）展示感知性别表现的结果。我们注意到，女性已被证明在检测与分割数据集中代表性不足 [[115](#bib.bib115)]，但观察到 SAM 在各群体间表现相近。我们在表 2（左下）对感知年龄重复该分析，注意到被感知为更年轻与更年长者在大型数据集中已被证明代表性不足 [[110](#bib.bib110)]。SAM 在被感知为年长者上表现最好（尽管置信区间较大）。最后，我们在表 2（右）对感知肤色重复该分析，注意到肤色较浅者在大型数据集中被证明代表性过高，而肤色较深者代表性不足 [[110](#bib.bib110)]。由于 MIAP 不包含感知肤色标注，我们使用一个包含感知 Fitzpatrick 皮肤类型标注 [[36](#bib.bib36)] 的专有数据集，其取值范围从 1（最浅肤色）到 6（最深肤色）。虽然各组均值略有差异，但我们未发现显著差异。我们认为这些发现源于任务本身性质，同时承认当 SAM 作为更大系统的组件使用时可能出现偏见。最后，在附录 C 中我们将分析扩展到服装分割，发现了感知性别表现方面存在偏见迹象。

|  |  |  |
| --- | --- | --- |
|  | mIoU | |
|  | 1 点 | 3 点 |
| *感知性别表现* | | |
| 女性化 | 54.4±1.7 | 90.4±0.6 |
| 男性化 | 55.7±1.7 | 90.1±0.6 |
| *感知年龄段* | | |
| 年长 | 62.9±6.7 | 92.6±1.3 |
| 中年 | 54.5±1.3 | 90.2±0.5 |
| 年轻 | 54.2±2.2 | 91.2±0.7 |

|  |  |  |
| --- | --- | --- |
|  | mIoU | |
|  | 1 点 | 3 点 |
| *感知肤色* | | |
| 1 | 52.9±2.2 | 91.0±0.9 |
| 2 | 51.5±1.4 | 91.1±0.5 |
| 3 | 52.2±1.9 | 91.4±0.7 |
| 4 | 51.5±2.7 | 91.7±1.0 |
| 5 | 52.4±4.2 | 92.5±1.4 |
| 6 | 56.7±6.3 | 91.2±2.4 |

表 2：SAM 在感知性别表现、年龄段与肤色上的人物分割性能。展示 95% 置信区间。在每个分组内，除「年长*对*中年」外，所有置信区间均重叠。

## 7 零样本迁移实验

本节展示分割一切模型 SAM 的*零样本迁移*实验。我们考虑五项任务，其中四项与训练 SAM 所用的可提示分割任务差异显著。这些实验在与训练时未见的数据集和任务上评估 SAM（我们对「零样本迁移」的用法沿用 CLIP [[82](#bib.bib82)] 中的用法）。这些数据集可能包含新颖的图像分布，例如水下或自我中心（ego-centric）图像（如图 8），据我们所知，它们未出现在 SA-1B 中。

我们的实验从检验可提示分割的核心目标开始：从任意提示产生有效掩码。我们强调*单个*前景点提示这一挑战性场景，因为它比其他更具体的提示更可能出现歧义。接下来是一系列贯穿低层、中层与高层图像理解、且大致对应该领域历史发展脉络的实验。具体而言，我们提示 SAM (1) 执行边缘检测，(2) 分割一切，即物体候选框生成，(3) 分割检测到的物体，即实例分割，以及 (4) 作为概念验证，从自由格式文本分割物体。这四项任务与训练 SAM 的可提示分割任务差异显著，均通过提示工程实现。实验最后以消融研究收尾。

#### 实现。

除非另有说明：(1) SAM 使用 MAE [[47](#bib.bib47)] 预训练的 ViT-H [[33](#bib.bib33)] 图像编码器；(2) SAM 在 SA-1B 上训练，注意该数据集仅包含数据引擎最后阶段自动生成的掩码。其余模型与训练细节（如超参数）见附录 A。

### 7.1 零样本单点有效掩码评估

#### 任务。

我们评估从*单个*前景点分割物体。该任务是病态的，因为一个点可能指向多个物体。大多数数据集的真值掩码并未枚举*所有*可能的掩码，这会使自动指标不可靠。因此，我们在标准 mIoU 指标（即预测掩码与真值掩码之间所有 IoU 的均值）之外，补充一项人工研究：标注者按 1（无意义）到 10（像素级完美）为掩码质量评分。更多细节见附录 D.1、附录 E 与附录 G。

默认情况下，我们遵循交互式分割的标准评估协议 [[92](#bib.bib92)]，从真值掩码的「中心」（掩码内部距离变换的最大值处）采样点。由于 SAM 能预测多个掩码，默认情况下我们只评估模型置信度最高的掩码。基线均为单掩码方法。我们主要与 RITM [[92](#bib.bib92)] 比较——在我们基准上，它相较于其他强基线 [[67](#bib.bib67), [18](#bib.bib18)] 表现最佳。

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ADE20K [[117](#bib.bib117)] | BBBC038v1 [[12](#bib.bib12)] | Cityscapes [[25](#bib.bib25)] | DOORS [[80](#bib.bib80)] | DRAM [[24](#bib.bib24)] | EgoHOS [[113](#bib.bib113)] | GTEA [[34](#bib.bib34), [63](#bib.bib63)] | Hypersim [[86](#bib.bib86)] |
| 示例 | 示例 | 示例 | 示例 | 示例 | 示例 | 示例 | 示例 |

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| IBD [[17](#bib.bib17)] | iShape [[111](#bib.bib111)] | LVIS [[44](#bib.bib44)] | NDD20 [[100](#bib.bib100)] | NDISPark [[22](#bib.bib22), [23](#bib.bib23)] | OVIS [[81](#bib.bib81)] | PPDLS [[74](#bib.bib74)] | Plittersdorf [[46](#bib.bib46)] |
| 示例 | 示例 | 示例 | 示例 | 示例 | 示例 | 示例 | 示例 |

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| STREETS [[91](#bib.bib91)] | TimberSeg [[38](#bib.bib38)] | TrashCan [[52](#bib.bib52)] | VISOR [[28](#bib.bib28), [27](#bib.bib27)] | WoodScape [[112](#bib.bib112)] | PIDRay [[104](#bib.bib104)] | ZeroWaste-f [[6](#bib.bib6)] |
| 示例 | 示例 | 示例 | 示例 | 示例 | 示例 | 示例 |

图 8：用于评估 SAM 零样本迁移能力的 23 个多样化分割数据集的样本。

#### 数据集。

我们使用新编译的 23 个数据集套件，涵盖多样化的图像分布。图 8 列出了这些数据集并展示各自样本（更多细节见附录表 7）。我们将全部 23 个数据集用于 mIoU 评估。对于人工研究，我们使用图 9(b) 列出的子集（受此类研究的资源限制所限）。该子集同时包含按自动指标衡量 SAM 优于和逊于 RITM 的数据集。

|  |
| --- |
| -200+20+40IoU delta at 1 center pointGTEA [[34](#bib.bib34), [63](#bib.bib63)]TrashCan [[52](#bib.bib52)]DRAM [[24](#bib.bib24)]PIDRay [[104](#bib.bib104)]Cityscapes [[25](#bib.bib25)]WoodScape [[112](#bib.bib112)]IBD [[17](#bib.bib17)]EgoHOS [[113](#bib.bib113)]Plittersdorf [[46](#bib.bib46)]VISOR [[28](#bib.bib28), [27](#bib.bib27)]NDISPark [[22](#bib.bib22), [23](#bib.bib23)]Hypersim [[86](#bib.bib86)]OVIS [[81](#bib.bib81)]ADE20K [[117](#bib.bib117)]iShape [[111](#bib.bib111)]ZeroWaste-f [[6](#bib.bib6)]STREETS [[91](#bib.bib91)]LVIS [[44](#bib.bib44)]NDD20 [[100](#bib.bib100)]TimberSeg [[38](#bib.bib38)]DOORS [[80](#bib.bib80)]BBBC038v1 [[12](#bib.bib12)]PPDLS [[74](#bib.bib74)]-21.4-15.0-6.5-5.8-2.0-0.6-0.3+0.8+1.5+1.8+2.7+6.1+7.0+7.8+8.8+9.1+17.3+18.5+21.1+28.9+41.1+44.7+46.9 |
| （a）SAM 与 RITM [[92](#bib.bib92)] 在 23 个数据集上的对比 |

|  |
| --- |
|  |
| （b）人工标注者的掩码质量评分 |
| |  |  | | --- | --- | |  |  | | （c）中心点（默认） | （d）随机点 | |

图 9：23 个数据集上的点到掩码评估。（a）SAM 与最强单点分割器 RITM [[92](#bib.bib92)] 的平均 IoU。由于歧义，单个掩码可能无法匹配真值；圆圈展示从 SAM 的 3 个预测中选取最相关者的「oracle」结果。（b）标注者对掩码质量的逐数据集评分对比，从 1（最差）到 10（最佳）。所有方法均使用真值掩码中心作为提示。（c、d）不同点数下的 mIoU。SAM 在 1 点时显著超越以往交互式分割器，点数更多时则与之持平。1 点时绝对 mIoU 偏低是歧义所致。

#### 结果。

首先看 23 个数据集全套上的 mIoU 自动评估。我们在图 9(a) 中与 RITM 逐数据集比较。SAM 在 23 个数据集中的 16 个上取得更高结果，最高领先约 47 IoU。我们还给出「oracle」结果：不再选择置信度最高的掩码，而是将 SAM 的 3 个掩码与真值比较后选择最相关者。这揭示了歧义对自动评估的影响。特别地，在 oracle 完成歧义消解后，SAM 在*所有*数据集上都优于 RITM。

人工研究的结果见图 9(b)。误差条为平均掩码评分的 95% 置信区间（所有差异均显著；细节见附录 E）。我们观察到，标注者对 SAM 掩码质量的评分持续显著高于最强基线 RITM。一个消融的、无歧义感知的单输出掩码 SAM 版本评分持续偏低，但仍高于 RITM。SAM 的平均评分介于 7 到 9 之间，对应于定性评分准则：「*高分（7-9）：物体可辨识，误差小且罕见（例如，漏掉一个小的、被严重遮挡的不连通部分……）。*」这些结果表明，SAM 已学会从单个点分割出有效掩码。注意，对于 DRAM 和 IBD 这类 SAM 在自动指标上较差的数据集，*它在人工研究中获得的评分持续更高*。

图 9(c) 展示了更多基线：SimpleClick [[67](#bib.bib67)] 与 FocalClick [[18](#bib.bib18)]，它们的单点性能低于 RITM 与 SAM。随着点数从 1 增加到 9，我们观察到方法间差距缩小。这在预期之内，因为任务变得更简单；同时 SAM 也未针对超高 IoU 区间优化。最后，在图 9(d) 中，我们把默认的中心点采样替换为随机点采样。我们观察到 SAM 与基线的差距拉大，且 SAM 在两种采样方式下都能取得相当的结果。

### 7.2 零样本边缘检测

#### 方法。

我们在 BSDS500 [[72](#bib.bib72), [3](#bib.bib3)] 上评估 SAM 执行边缘检测这一经典低层任务。我们使用自动掩码生成流水线的简化版本。具体而言，我们用 16×16 的规则前景点网格提示 SAM，得到 768 个预测掩码（每个点 3 个）。冗余掩码由 NMS 去除。然后，对未阈值化的掩码概率图做 Sobel 滤波，并辅以标准轻量后处理（包括边缘 NMS）计算边缘图（细节见附录 D.2）。

|  |  |  |
| --- | --- | --- |
| 图像 | 真值 | SAM |
| 示例 | 示例 | 示例 |
| 示例 | 示例 | 示例 |

图 10：BSDS500 上的零样本边缘预测。SAM 未被训练去预测边缘图，训练期间也未接触 BSDS 图像或标注。

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| 方法 | 年份 | ODS | OIS | AP | R50 |
| HED [[108](#bib.bib108)] | 2015 | .788 | .808 | .840 | .923 |
| EDETR [[79](#bib.bib79)] | 2022 | .840 | .858 | .896 | .930 |
| *零样本迁移方法：* | | | | | |
| Sobel 滤波 | 1968 | .539 | - | - | - |
| Canny [[13](#bib.bib13)] | 1986 | .600 | .640 | .580 | - |
| Felz-Hutt [[35](#bib.bib35)] | 2004 | .610 | .640 | .560 | - |
| SAM | 2023 | .768 | .786 | .794 | .928 |

表 3：BSDS500 上向边缘检测的零样本迁移。

#### 结果。

我们在图 10 中可视化代表性边缘图（更多见图 15）。定性来看，尽管 SAM 未针对边缘检测训练，它仍产生了合理的边缘图。与真值相比，SAM 预测出更多边缘，包括 BSDS500 中未标注的合理边缘。这一偏差在表 3 中得到定量体现：50% 精度下的召回率（R50）很高，但以精度为代价。SAM 自然落后于学习到 BSDS500 偏差（即应抑制哪些边缘）的最先进方法。尽管如此，与 HED [[108](#bib.bib108)] 等开创性深度学习方法（同样在 BSDS500 上训练）相比，SAM 表现良好，并显著优于以往（诚然已过时的）零样本迁移方法。

### 7.3 零样本物体候选框

#### 方法。

接下来，我们在物体候选框生成 [[2](#bib.bib2), [102](#bib.bib102)] 这一中层任务上评估 SAM。该任务在物体检测研究中曾扮演重要角色，是开创性系统（如 [[102](#bib.bib102), [41](#bib.bib41), [84](#bib.bib84)]）的中间步骤。为生成物体候选框，我们运行略作修改的自动掩码生成流水线，并将掩码作为候选输出（细节见附录 D.3）。

我们在 LVIS v1 [[44](#bib.bib44)] 上计算标准的平均召回率（AR）指标。我们聚焦 LVIS 是因为其类别数量庞大，构成挑战性测试。我们比较的*强*基线实现为 ViTDet [[62](#bib.bib62)] 检测器（cascade Mask R-CNN [[48](#bib.bib48), [11](#bib.bib11)] ViT-H）。注意，该「基线」对应「Detector Masquerading as Proposal generator」（DMP）方法 [[16](#bib.bib16)]，后者已被证明会钻 AR 的空子，因此这是一次真正严苛的比较。

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  | 掩码 AR@1000 | | | | | | |
| 方法 | 全部 | 小 | 中 | 大 | 频繁 | 常见 | 稀有 |
| ViTDet-H [[62](#bib.bib62)] | 63.0 | 51.7 | 80.8 | 87.0 | 63.1 | 63.3 | 58.3 |
| *零样本迁移方法：* | | | | | | | |
| SAM – 单输出 | 54.9 | 42.8 | 76.7 | 74.4 | 54.7 | 59.8 | 62.0 |
| SAM | 59.3 | 45.5 | 81.6 | 86.9 | 59.1 | 63.9 | 65.8 |

表 4：LVIS v1 上的物体候选框生成。SAM 以零样本方式应用，即它未针对物体候选框生成训练，也未接触 LVIS 图像或标注。

#### 结果。

在表 4 中，不出所料，使用 ViTDet-H 的检测结果作为物体候选（即钻 AR 空子的 DMP 方法 [[16](#bib.bib16)]）总体表现最佳。然而，SAM 在多项指标上表现出色。值得注意的是，它在中型与大型物体以及稀有与常见物体上优于 ViTDet-H。事实上，SAM 仅在小型物体与频繁物体上逊于 ViTDet-H——ViTDet-H 在 LVIS 上训练，因而能轻易学到 LVIS 特有的标注偏差，而 SAM 不能。我们还与消融的无歧义感知版本 SAM（「单输出」）比较，后者在所有 AR 指标上都显著逊于 SAM。

### 7.4 零样本实例分割

#### 方法。

进入更高层的视觉任务，我们将 SAM 用作实例分割器的分割模块。实现很简单：运行一个物体检测器（即前述 ViTDet），并用其输出的框提示 SAM。这展示了将 SAM *组合*进更大系统的方式。

#### 结果。

我们在表 5 中比较 SAM 与 ViTDet 在 COCO 与 LVIS 上预测的掩码。观察掩码 AP 指标，两个数据集上都存在差距，SAM 相当接近，但确实落后于 ViTDet。通过可视化输出，我们观察到 SAM 的掩码在质量上往往优于 ViTDet，边界更清晰（见附录 D.4 与图 16）。为深入研究这一观察，我们进行了额外的人工研究，请标注者用之前的 1 到 10 质量量表为 ViTDet 掩码与 SAM 掩码评分。在图 11 中，我们观察到在人工研究中 SAM 持续胜过 ViTDet。

|  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | COCO [[66](#bib.bib66)] | | | | LVIS v1 [[44](#bib.bib44)] | | | |
| 方法 | AP | AP_S | AP_M | AP_L | AP | AP_S | AP_M | AP_L |
| ViTDet-H [[62](#bib.bib62)] | 51.0 | 32.0 | 54.3 | 68.9 | 46.6 | 35.0 | 58.0 | 66.3 |
| *零样本迁移方法（仅分割模块）：* | | | | | | | | |
| SAM | 46.5 | 30.8 | 51.0 | 61.7 | 44.7 | 32.5 | 57.6 | 65.5 |

表 5：实例分割结果。SAM 以 ViTDet 框为提示进行零样本分割。全监督的 ViTDet 优于 SAM，但在质量更高的 LVIS 掩码上差距缩小。有趣的是，按人工评分 SAM 胜过 ViTDet（见图 11）。

图 11：人工研究中 ViTDet 与 SAM（均应用于 LVIS 真值框）的掩码质量评分分布。我们还报告 LVIS 与 COCO 真值的质量。图例展示评分均值与 95% 置信区间。尽管 AP 较低（表 5），SAM 的评分高于 ViTDet，这表明 ViTDet 利用了 COCO 与 LVIS 训练数据中的偏差。

我们推测，在掩码 AP 差距更大且真值质量相对较低的 COCO 上（人工研究证实了这一点），ViTDet 学到了 COCO 掩码的特定偏差。SAM 作为零样本方法，无法利用这些（通常不可取的）偏差。LVIS 数据集真值质量更高，但仍有其特殊之处（例如，掩码不含孔洞，构造上就是简单多边形），以及模态（modal）*对*非模态（amodal）掩码的偏差。同样，SAM 未被训练去学习这些偏差，而 ViTDet 可以利用它们。

### 7.5 零样本文本到掩码

#### 方法。

最后，我们考虑一个更高层的任务：从自由格式文本分割物体。本实验是 SAM 处理文本提示能力的概念验证。在之前所有实验中我们使用完全相同的 SAM，而本实验对 SAM 的训练流程做了修改以使其具备文本感知能力，但不需要新的文本标注。具体而言，对每个面积大于 100² 的人工收集掩码，我们提取 CLIP 的*图像*嵌入。然后在训练时，我们以提取的 CLIP 图像嵌入作为第一次交互来提示 SAM。这里的关键观察是：由于 CLIP 的*图像*嵌入经过与*文本*嵌入对齐的训练，我们可以在训练时用图像嵌入，而在推理时用文本嵌入。也就是说，推理时我们让文本通过 CLIP 的文本编码器，再将得到的文本嵌入作为提示提供给 SAM（细节见附录 D.5）。

|  |  |
| --- | --- |
| ✓示例 | ✓示例 |
| ✗示例 | ✓示例 |
| ✗示例 | ✓示例 |

图 12：零样本文本到掩码。SAM 可以处理简单和细微的文本提示。当 SAM 无法做出正确预测时，一个额外的点提示可以提供帮助。

#### 结果。

我们在图 12 中展示定性结果。SAM 能基于「a wheel（车轮）」这样的简单文本提示以及「beaver tooth grille（海狸牙格栅）」这样的短语分割物体。当 SAM 仅凭文本提示无法选对物体时，一个额外的点通常能修正预测，这与 [[31](#bib.bib31)] 类似。

图 13：数据引擎阶段、图像编码器规模与训练数据规模的消融研究。（左）数据引擎的每个阶段都带来 23 个数据集套件上的提升，且仅用自动数据（我们的默认设置）训练与使用全部三个阶段的数据训练结果相近。（中）用约 10% 的 SA-1B 与完整 SA-1B 训练的 SAM 表现相当。我们默认使用全部 1100 万张图像训练，但使用 100 万张图像也是合理的实际设置。（右）扩展 SAM 的图像编码器带来有意义的但趋于饱和的收益。尽管如此，在特定场景下较小的图像编码器可能更受青睐。

### 7.6 消融实验

我们在 23 个数据集套件上、以单中心点提示协议进行多项消融。回顾一下，单个点可能有歧义，而歧义可能未在真值中体现——真值每点只含一个掩码。由于 SAM 处于零样本迁移设置，其排名第一的掩码与数据标注指南所产生的掩码之间可能存在系统性偏差。因此，我们还报告相对于真值的最佳掩码（「oracle」）。

图 13（左）绘制了在数据引擎各阶段累积数据上训练时 SAM 的性能。我们观察到每个阶段都提升了 mIoU。当使用全部三个阶段的数据训练时，自动掩码在数量上远超人工与半自动掩码。为此，我们发现训练时对人工与半自动掩码做 10 倍过采样效果最佳。这一设置使训练复杂化。因此我们测试了第四种设置：仅使用自动生成的掩码。用这些数据训练时，SAM 的表现仅略低于使用全部数据（约 0.5 mIoU）。因此，默认情况下我们仅使用自动生成的掩码，以简化训练设置。

在图 13（中）中，我们考察数据量的影响。完整 SA-1B 包含 1100 万张图像，我们在本消融中将其均匀子采样为 100 万与 10 万张。在 10 万张图像时，我们观察到所有设置下 mIoU 大幅下降。然而，在 100 万张图像（约为完整数据集的 10%）时，结果与使用完整数据集相当。这一数据规模仍包含约 1 亿个掩码，对许多用例而言可能是切实可行的设置。

最后，图 13（右）展示使用 ViT-B、ViT-L 与 ViT-H 图像编码器的结果。ViT-H 相比 ViT-B 有大幅提升，但相比 ViT-L 仅略有收益。目前看来，进一步扩大图像编码器并无益处。

## 8 讨论

#### 基座模型。

自机器学习早期以来，预训练模型就被适配到下游任务 [[99](#bib.bib99)]。近年来，随着对规模的日益强调，这一范式愈发重要，此类模型最近被（重新）冠以「基座模型」之名：即「在大规模广泛数据上训练、可适配到广泛下游任务」的模型 [[8](#bib.bib8)]。我们的工作与该定义契合，不过我们注意到，图像分割的基座模型本质上范围有限，因为它只代表计算机视觉中一个重要但局部的子集。我们还把本工作的一点与 [[8](#bib.bib8)] 对比，后者强调*自监督*学习在基座模型中的作用。虽然我们的模型用自监督技术（MAE [[47](#bib.bib47)]）初始化，其能力的绝大部分来自大规模*监督*训练。在数据引擎能够扩展可用标注（如我们的引擎）的场景下，监督训练是一种有效的解决方案。

#### 可组合性。

预训练模型能够支撑甚至超出训练之时想象的新能力。一个突出例子是 CLIP [[82](#bib.bib82)] 作为更大系统（如 DALL·E [[83](#bib.bib83)]）中的*组件*使用。我们的目标是让这类组合在 SAM 上变得简单。我们通过要求 SAM 对广泛的分割提示预测有效掩码来实现这一点，其效果是在 SAM 与其他组件之间建立可靠的接口。例如，MCC [[106](#bib.bib106)] 可以轻松用 SAM 分割感兴趣的物体，在从单张 RGB-D 图像做 3D 重建时实现对未见物体的强泛化。再如，可以用可穿戴设备检测到的注视点提示 SAM，开启新的应用。得益于 SAM 向自我中心图像等新领域泛化的能力，此类系统无需额外训练即可工作。

#### 局限性。

尽管 SAM 总体表现良好，它并不完美。它可能遗漏精细结构，有时会幻觉出细小的连通成分，边界也不如那些计算量更大的「放大」（zoom-in）方法（如 [[18](#bib.bib18)]）清晰。总体而言，我们预期当提供很多点时，专用的交互式分割方法（如 [[67](#bib.bib67)]）会胜过 SAM。与这些方法不同，SAM 的设计目标是通用性与使用广度，而非高 IoU 的交互式分割。此外，虽然 SAM 可以实时处理提示，但使用重量级图像编码器时其整体性能并非实时。我们对文本到掩码任务的尝试是探索性的，尚不完全稳健，尽管我们相信通过更多努力可以改进。虽然 SAM 能执行许多任务，但如何设计简单提示来实现语义分割与全景分割尚不清楚。最后，还有一些领域专用工具（如 [[7](#bib.bib7)]），我们预期它们在各自领域会胜过 SAM。

#### 结论。

Segment Anything 项目是一次将图像分割带入基座模型时代的尝试。我们的主要贡献是使这一跨越成为可能的新任务（可提示分割）、新模型（SAM）与新数据集（SA-1B）。SAM 能否取得基座模型的地位，将由社区如何使用它来检验，但无论如何，我们期待本工作的视角、超过 10 亿掩码的发布以及我们的可提示分割模型能助力铺就前路。

#### 致谢。

感谢 Aaron Adcock 与 Jitendra Malik 的有益讨论。感谢 Vaibhav Aggarwal 与 Yanghao Li 在模型扩展上的帮助。感谢 Cheng-Yang Fu、Jiabo Hu 与 Robert Kuo 在数据标注平台上的帮助。感谢 Allen Goodman 与 Bram Wasti 在优化模型网页版上的帮助。最后，感谢 Morteza Behrooz、Ashley Gabriel、Ahuva Goldstand、Sumanth Gurram、Somya Jain、Devansh Kukreja、Joshua Lane、Lilian Luong、Mallika Malhotra、William Ngan、Omkar Parkhi、Nikhil Raina、Dirk Rowe、Neil Sejoor、Vanessa Stark、Bala Varadarajan 与 Zachary Winstrom 在演示、数据集查看器及其他资产与工具上的帮助。

## 参考文献

- [1]

  Edward H Adelson.
  On seeing stuff: the perception of materials by humans and machines.
  Human vision and electronic imaging VI, 2001.
- [2]

  Bogdan Alexe, Thomas Deselaers, and Vittorio Ferrari.
  What is an object?
  CVPR, 2010.
- [3]

  Pablo Arbeláez, Michael Maire, Charless Fowlkes, and Jitendra Malik.
  Contour detection and hierarchical image segmentation.
  TPAMI, 2010.
- [4]

  Jimmy Lei Ba, Jamie Ryan Kiros, and Geoffrey E Hinton.
  Layer normalization.
  arXiv:1607.06450, 2016.
- [5]

  Hangbo Bao, Li Dong, and Furu Wei.
  BEiT: BERT pre-training of image transformers.
  arXiv:2106.08254, 2021.
- [6]

  Dina Bashkirova, Mohamed Abdelfattah, Ziliang Zhu, James Akl, Fadi Alladkani,
  Ping Hu, Vitaly Ablavsky, Berk Calli, Sarah Adel Bargal, and Kate Saenko.
  ZeroWaste dataset: Towards deformable object segmentation in
  cluttered scenes.
  CVPR, 2022.
- [7]

  Stuart Berg, Dominik Kutra, Thorben Kroeger, Christoph N. Straehle, Bernhard X.
  Kausler, Carsten Haubold, Martin Schiegg, Janez Ales, Thorsten Beier, Markus
  Rudy, Kemal Eren, Jaime I. Cervantes, Buote Xu, Fynn Beuttenmueller, Adrian
  Wolny, Chong Zhang, Ullrich Koethe, Fred A. Hamprecht, and Anna Kreshuk.
  ilastik: interactive machine learning for (bio)image analysis.
  Nature Methods, 2019.
- [8]

  Rishi Bommasani, Drew A Hudson, Ehsan Adeli, Russ Altman, Simran Arora, Sydney
  von Arx, Michael S Bernstein, Jeannette Bohg, Antoine Bosselut, Emma
  Brunskill, et al.
  On the opportunities and risks of foundation models.
  arXiv:2108.07258, 2021.
- [9]

  Gustav Bredell, Christine Tanner, and Ender Konukoglu.
  Iterative interaction training for segmentation editing networks.
  MICCAI, 2018.
- [10]

  Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla
  Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell,
  Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon
  Child, Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens Winter, Chris
  Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess,
  Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever,
  and Dario Amodei.
  Language models are few-shot learners.
  NeurIPS, 2020.
- [11]

  Zhaowei Cai and Nuno Vasconcelos.
  Cascade R-CNN: Delving into high quality object detection.
  CVPR, 2018.
- [12]

  Juan C. Caicedo, Allen Goodman, Kyle W. Karhohs, Beth A. Cimini, Jeanelle
  Ackerman, Marzieh Haghighi, CherKeng Heng, Tim Becker, Minh Doan, Claire
  McQuin, Mohammad Rohban, Shantanu Singh, and Anne E. Carpenter.
  Nucleus segmentation across imaging experiments: the 2018 data
  science bowl.
  Nature Methods, 2019.
- [13]

  John Canny.
  A computational approach to edge detection.
  TPAMI, 1986.
- [14]

  Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander
  Kirillov, and Sergey Zagoruyko.
  End-to-end object detection with Transformers.
  ECCV, 2020.
- [15]

  Guillaume Charpiat, Matthias Hofmann, and Bernhard Schölkopf.
  Automatic image colorization via multimodal predictions.
  ECCV, 2008.
- [16]

  Neelima Chavali, Harsh Agrawal, Aroma Mahendru, and Dhruv Batra.
  Object-proposal evaluation protocol is’ gameable’.
  CVPR, 2016.
- [17]

  Jiazhou Chen, Yanghui Xu, Shufang Lu, Ronghua Liang, and Liangliang Nan.
  3D instance segmentation of MVS buildings.
  IEEE Transactions on Geoscience and Remote Sensing, 2022.
- [18]

  Xi Chen, Zhiyan Zhao, Yilei Zhang, Manni Duan, Donglian Qi, and Hengshuang
  Zhao.
  FocalClick: towards practical interactive image segmentation.
  CVPR, 2022.
- [19]

  Bowen Cheng, Ishan Misra, Alexander G Schwing, Alexander Kirillov, and Rohit
  Girdhar.
  Masked-attention mask transformer for universal image segmentation.
  CVPR, 2022.
- [20]

  Bowen Cheng, Alex Schwing, and Alexander Kirillov.
  Per-pixel classification is not all you need for semantic
  segmentation.
  NeurIPS, 2021.
- [21]

  Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra,
  Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian
  Gehrmann, et al.
  PaLM: Scaling language modeling with pathways.
  arXiv:2204.02311, 2022.
- [22]

  Luca Ciampi, Carlos Santiago, Joao Costeira, Claudio Gennaro, and Giuseppe
  Amato.
  Domain adaptation for traffic density estimation.
  International Joint Conference on Computer Vision, Imaging and
  Computer Graphics Theory and Applications, 2021.
- [23]

  Luca Ciampi, Carlos Santiago, Joao Costeira, Claudio Gennaro, and Giuseppe
  Amato.
  Night and day instance segmented park (NDISPark) dataset: a
  collection of images taken by day and by night for vehicle detection,
  segmentation and counting in parking areas.
  Zenodo, 2022.
- [24]

  Nadav Cohen, Yael Newman, and Ariel Shamir.
  Semantic segmentation in art paintings.
  Computer Graphics Forum, 2022.
- [25]

  Marius Cordts, Mohamed Omran, Sebastian Ramos, Timo Rehfeld, Markus Enzweiler,
  Rodrigo Benenson, Uwe Franke, Stefan Roth, and Bernt Schiele.
  The Cityscapes dataset for semantic urban scene understanding.
  CVPR, 2016.
- [26]

  Bruno da Silva, George Konidaris, and Andrew Barto.
  Learning parameterized skills.
  ICML, 2012.
- [27]

  Dima Damen, Hazel Doughty, Giovanni Maria Farinella, Antonino Furnari, Jian Ma,
  Evangelos Kazakos, Davide Moltisanti, Jonathan Munro, Toby Perrett, Will
  Price, and Michael Wray.
  Rescaling egocentric vision: Collection, pipeline and challenges for
  EPIC-KITCHENS-100.
  IJCV, 2022.
- [28]

  Ahmad Darkhalil, Dandan Shan, Bin Zhu, Jian Ma, Amlan Kar, Richard Higgins,
  Sanja Fidler, David Fouhey, and Dima Damen.
  EPIC-KITCHENS VISOR benchmark: Video segmentations and object
  relations.
  NeurIPS, 2022.
- [29]

  Terrance De Vries, Ishan Misra, Changhan Wang, and Laurens Van der Maaten.
  Does object recognition work for everyone?
  CVPR workshops, 2019.
- [30]

  Mark Díaz, Ian Kivlichan, Rachel Rosen, Dylan Baker, Razvan Amironesei,
  Vinodkumar Prabhakaran, and Emily Denton.
  CrowdWorkSheets: Accounting for individual and collective
  identities underlying crowdsourced dataset annotation.
  ACM Conference on Fairness, Accountability, and Transparency,
  2022.
- [31]

  Henghui Ding, Scott Cohen, Brian Price, and Xudong Jiang.
  PhraseClick: toward achieving flexible interactive segmentation by
  phrase and click.
  ECCV, 2020.
- [32]

  Piotr Dollár and C Lawrence Zitnick.
  Fast edge detection using structured forests.
  TPAMI, 2014.
- [33]

  Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn,
  Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg
  Heigold, Sylvain Gelly, Jakob Uszkoreit, and Neil Houlsby.
  An image is worth 16x16 words: Transformers for image recognition at
  scale.
  ICLR, 2021.
- [34]

  Alireza Fathi, Xiaofeng Ren, and James M. Rehg.
  Learning to recognize objects in egocentric activities.
  CVPR, 2011.
- [35]

  Pedro F Felzenszwalb and Daniel P Huttenlocher.
  Efficient graph-based image segmentation.
  IJCV, 2004.
- [36]

  Thomas B. Fitzpatrick.
  The validity and practicality of sun-reactive skin types i through
  vi.
  Archives of Dermatology, 1988.
- [37]

  Marco Forte, Brian Price, Scott Cohen, Ning Xu, and François Pitié.
  Getting to 99% accuracy in interactive segmentation.
  arXiv:2003.07932, 2020.
- [38]

  Jean-Michel Fortin, Olivier Gamache, Vincent Grondin, François Pomerleau, and
  Philippe Giguère.
  Instance segmentation for autonomous log grasping in forestry
  operations.
  IROS, 2022.
- [39]

  Timnit Gebru, Jamie Morgenstern, Briana Vecchione, Jennifer Wortman Vaughan,
  Hanna Wallach, Hal Daumé Iii, and Kate Crawford.
  Datasheets for datasets.
  Communications of the ACM, 2021.
- [40]

  Golnaz Ghiasi, Yin Cui, Aravind Srinivas, Rui Qian, Tsung-Yi Lin, Ekin D Cubuk,
  Quoc V Le, and Barret Zoph.
  Simple copy-paste is a strong data augmentation method for instance
  segmentation.
  CVPR, 2021.
- [41]

  Ross Girshick, Jeff Donahue, Trevor Darrell, and Jitendra Malik.
  Rich feature hierarchies for accurate object detection and semantic
  segmentation.
  CVPR, 2014.
- [42]

  Priya Goyal, Piotr Dollár, Ross Girshick, Pieter Noordhuis, Lukasz Wesolowski,
  Aapo Kyrola, Andrew Tulloch, Yangqing Jia, and Kaiming He.
  Accurate, large minibatch SGD: Training ImageNet in 1 hour.
  arXiv:1706.02677, 2017.
- [43]

  Kristen Grauman, Andrew Westbury, Eugene Byrne, Zachary Chavis, Antonino
  Furnari, Rohit Girdhar, Jackson Hamburger, Hao Jiang, Miao Liu, Xingyu Liu,
  Miguel Martin, Tushar Nagarajan, Ilija Radosavovic, Santhosh Kumar
  Ramakrishnan, Fiona Ryan, Jayant Sharma, Michael Wray, Mengmeng Xu,
  Eric Zhongcong Xu, Chen Zhao, Siddhant Bansal, Dhruv Batra, Vincent
  Cartillier, Sean Crane, Tien Do, Morrie Doulaty, Akshay Erapalli, Christoph
  Feichtenhofer, Adriano Fragomeni, Qichen Fu, Christian Fuegen, Abrham
  Gebreselasie, Cristina Gonzalez, James Hillis, Xuhua Huang, Yifei Huang,
  Wenqi Jia, Weslie Khoo, Jachym Kolar, Satwik Kottur, Anurag Kumar, Federico
  Landini, Chao Li, Yanghao Li, Zhenqiang Li, Karttikeya Mangalam, Raghava
  Modhugu, Jonathan Munro, Tullie Murrell, Takumi Nishiyasu, Will Price,
  Paola Ruiz Puentes, Merey Ramazanova, Leda Sari, Kiran Somasundaram, Audrey
  Southerland, Yusuke Sugano, Ruijie Tao, Minh Vo, Yuchen Wang, Xindi Wu,
  Takuma Yagi, Yunyi Zhu, Pablo Arbelaez, David Crandall, Dima Damen,
  Giovanni Maria Farinella, Bernard Ghanem, Vamsi Krishna Ithapu, C. V.
  Jawahar, Hanbyul Joo, Kris Kitani, Haizhou Li, Richard Newcombe, Aude Oliva,
  Hyun Soo Park, James M. Rehg, Yoichi Sato, Jianbo Shi, Mike Zheng Shou,
  Antonio Torralba, Lorenzo Torresani, Mingfei Yan, and Jitendra Malik.
  Ego4D: Around the World in 3,000 Hours of Egocentric Video.
  CVPR, 2022.
- [44]

  Agrim Gupta, Piotr Dollar, and Ross Girshick.
  LVIS: A dataset for large vocabulary instance segmentation.
  CVPR, 2019.
- [45]

  Abner Guzman-Rivera, Dhruv Batra, and Pushmeet Kohli.
  Multiple choice learning: Learning to produce multiple structured
  outputs.
  NeurIPS, 2012.
- [46]

  Timm Haucke, Hjalmar S. Kühl, and Volker Steinhage.
  SOCRATES: Introducing depth in visual wildlife monitoring using
  stereo vision.
  Sensors, 2022.
- [47]

  Kaiming He, Xinlei Chen, Saining Xie, Yanghao Li, Piotr Dollár, and Ross
  Girshick.
  Masked autoencoders are scalable vision learners.
  CVPR, 2022.
- [48]

  Kaiming He, Georgia Gkioxari, Piotr Dollár, and Ross Girshick.
  Mask R-CNN.
  ICCV, 2017.
- [49]

  Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun.
  Deep residual learning for image recognition.
  CVPR, 2016.
- [50]

  Dan Hendrycks and Kevin Gimpel.
  Gaussian error linear units (gelus).
  arXiv:1606.08415, 2016.
- [51]

  Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor
  Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes
  Welbl, Aidan Clark, et al.
  Training compute-optimal large language models.
  arXiv:2203.15556, 2022.
- [52]

  Jungseok Hong, Michael Fulton, and Junaed Sattar.
  TrashCan: A semantically-segmented dataset towards visual detection
  of marine debris.
  arXiv:2007.08097, 2020.
- [53]

  Gao Huang, Yu Sun, Zhuang Liu, Daniel Sedra, and Kilian Q Weinberger.
  Deep networks with stochastic depth.
  ECCV, 2016.
- [54]

  Jitesh Jain, Jiachen Li, MangTik Chiu, Ali Hassani, Nikita Orlov, and Humphrey
  Shi.
  Oneformer: One transformer to rule universal image segmentation.
  arXiv:2211.06220, 2022.
- [55]

  Chao Jia, Yinfei Yang, Ye Xia, Yi-Ting Chen, Zarana Parekh, Hieu Pham, Quoc Le,
  Yun-Hsuan Sung, Zhen Li, and Tom Duerig.
  Scaling up visual and vision-language representation learning with
  noisy text supervision.
  ICML, 2021.
- [56]

  Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon
  Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei.
  Scaling laws for neural language models.
  arXiv:2001.08361, 2020.
- [57]

  Michael Kass, Andrew Witkin, and Demetri Terzopoulos.
  Snakes: Active contour models.
  IJCV, 1988.
- [58]

  Dahun Kim, Tsung-Yi Lin, Anelia Angelova, In So Kweon, and Weicheng Kuo.
  Learning open-world object proposals without learning to classify.
  IEEE Robotics and Automation Letters, 2022.
- [59]

  Alexander Kirillov, Kaiming He, Ross Girshick, Carsten Rother, and Piotr
  Dollár.
  Panoptic segmentation.
  CVPR, 2019.
- [60]

  Alina Kuznetsova, Hassan Rom, Neil Alldrin, Jasper Uijlings, Ivan Krasin, Jordi
  Pont-Tuset, Shahab Kamali, Stefan Popov, Matteo Malloci, Alexander
  Kolesnikov, Tom Duerig, and Vittorio Ferrari.
  The open images dataset v4: Unified image classification, object
  detection, and visual relationship detection at scale.
  IJCV, 2020.
- [61]

  Alexandre Lacoste, Alexandra Luccioni, Victor Schmidt, and Thomas Dandres.
  Quantifying the carbon emissions of machine learning.
  arXiv:1910.09700, 2019.
- [62]

  Yanghao Li, Hanzi Mao, Ross Girshick, and Kaiming He.
  Exploring plain vision transformer backbones for object detection.
  ECCV, 2022.
- [63]

  Yin Li, Zhefan Ye, and James M. Rehg.
  Delving into egocentric actions.
  CVPR, 2015.
- [64]

  Zhuwen Li, Qifeng Chen, and Vladlen Koltun.
  Interactive image segmentation with latent diversity.
  CVPR, 2018.
- [65]

  Tsung-Yi Lin, Priya Goyal, Ross Girshick, Kaiming He, and Piotr Dollár.
  Focal loss for dense object detection.
  ICCV, 2017.
- [66]

  Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva
  Ramanan, Piotr Dollár, and C Lawrence Zitnick.
  Microsoft COCO: Common objects in context.
  ECCV, 2014.
- [67]

  Qin Liu, Zhenlin Xu, Gedas Bertasius, and Marc Niethammer.
  SimpleClick: Interactive image segmentation with simple vision
  transformers.
  arXiv:2210.11006, 2022.
- [68]

  Ilya Loshchilov and Frank Hutter.
  Decoupled weight decay regularization.
  ICLR, 2019.
- [69]

  Cathy H Lucas, Daniel OB Jones, Catherine J Hollyhead, Robert H Condon,
  Carlos M Duarte, William M Graham, Kelly L Robinson, Kylie A Pitt, Mark
  Schildhauer, and Jim Regetz.
  Gelatinous zooplankton biomass in the global oceans: geographic
  variation and environmental drivers.
  Global Ecology and Biogeography, 2014.
- [70]

  Sabarinath Mahadevan, Paul Voigtlaender, and Bastian Leibe.
  Iteratively trained interactive segmentation.
  BMVC, 2018.
- [71]

  Kevis-Kokitsi Maninis, Sergi Caelles, Jordi Pont-Tuset, and Luc Van Gool.
  Deep extreme cut: From extreme points to object segmentation.
  CVPR, 2018.
- [72]

  David Martin, Charless Fowlkes, Doron Tal, and Jitendra Malik.
  A database of human segmented natural images and its application to
  evaluating segmentation algorithms and measuring ecological statistics.
  ICCV, 2001.
- [73]

  Fausto Milletari, Nassir Navab, and Seyed-Ahmad Ahmadi.
  V-Net: Fully convolutional neural networks for volumetric medical
  image segmentation.
  3DV, 2016.
- [74]

  Massimo Minervini, Andreas Fischbach, Hanno Scharr, and Sotirios A. Tsaftaris.
  Finely-grained annotated datasets for image-based plant phenotyping.
  Pattern Recognition Letters, 2016.
- [75]

  Margaret Mitchell, Simone Wu, Andrew Zaldivar, Parker Barnes, Lucy Vasserman,
  Ben Hutchinson, Elena Spitzer, Inioluwa Deborah Raji, and Timnit Gebru.
  Model cards for model reporting.
  Proceedings of the conference on fairness, accountability, and
  transparency, 2019.
- [76]

  Dim P Papadopoulos, Jasper RR Uijlings, Frank Keller, and Vittorio Ferrari.
  Extreme clicking for efficient object annotation.
  ICCV, 2017.
- [77]

  David Patterson, Joseph Gonzalez, Quoc Le, Chen Liang, Lluis-Miquel Munguia,
  Daniel Rothchild, David So, Maud Texier, and Jeff Dean.
  Carbon emissions and large neural network training.
  arXiv:2104.10350, 2021.
- [78]

  Matthew E Peters, Waleed Ammar, Chandra Bhagavatula, and Russell Power.
  Semi-supervised sequence tagging with bidirectional language models.
  Proceedings of the 55th Annual Meeting of the Association for
  Computational Linguistics, 2017.
- [79]

  Mengyang Pu, Yaping Huang, Yuming Liu, Qingji Guan, and Haibin Ling.
  EDTER: Edge detection with transformer.
  CVPR, 2022.
- [80]

  Mattia Pugliatti and Francesco Topputo.
  DOORS: Dataset fOr bOuldeRs Segmentation.
  Zenodo, 2022.
- [81]

  Jiyang Qi, Yan Gao, Yao Hu, Xinggang Wang, Xiaoyu Liu, Xiang Bai, Serge
  Belongie, Alan Yuille, Philip Torr, and Song Bai.
  Occluded video instance segmentation: A benchmark.
  ICCV, 2022.
- [82]

  Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh,
  Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark,
  et al.
  Learning transferable visual models from natural language
  supervision.
  ICML, 2021.
- [83]

  Aditya Ramesh, Mikhail Pavlov, Gabriel Goh, Scott Gray, Chelsea Voss, Alec
  Radford, Mark Chen, and Ilya Sutskever.
  Zero-shot text-to-image generation.
  ICML, 2021.
- [84]

  Shaoqing Ren, Kaiming He, Ross Girshick, and Jian Sun.
  Faster R-CNN: Towards real-time object detection with region
  proposal networks.
  NeurIPS, 2015.
- [85]

  Xiaofeng Ren and Jitendra Malik.
  Learning a classification model for segmentation.
  ICCV, 2003.
- [86]

  Mike Roberts, Jason Ramapuram, Anurag Ranjan, Atulit Kumar, Miguel Angel
  Bautista, Nathan Paczan, Russ Webb, and Joshua M. Susskind.
  Hypersim: A photorealistic synthetic dataset for holistic indoor
  scene understanding.
  ICCV, 2021.
- [87]

  Candice Schumann, Susanna Ricco, Utsav Prabhu, Vittorio Ferrari, and Caroline
  Pantofaru.
  A step toward more inclusive people annotations for fairness.
  Proceedings of the 2021 AAAI/ACM Conference on AI, Ethics, and
  Society, 2021.
- [88]

  Sefik Ilkin Serengil and Alper Ozpinar.
  LightFace: A hybrid deep face recognition framework.
  ASYU, 2020.
- [89]

  Sefik Ilkin Serengil and Alper Ozpinar.
  HyperExtended LightFace: A facial attribute analysis framework.
  ICEET, 2021.
- [90]

  Jamie Shotton, John Winn, Carsten Rother, and Antonio Criminisi.
  TextonBoost: Joint appearance, shape and context modeling for
  mulit-class object recognition and segmentation.
  ECCV, 2006.
- [91]

  Corey Snyder and Minh Do.
  STREETS: A novel camera network dataset for traffic flow.
  NeurIPS, 2019.
- [92]

  Konstantin Sofiiuk, Ilya A Petrov, and Anton Konushin.
  Reviving iterative training with mask guidance for interactive
  segmentation.
  ICIP, 2022.
- [93]

  Nitish Srivastava, Geoffrey Hinton, Alex Krizhevsky, Ilya Sutskever, and Ruslan
  Salakhutdinov.
  Dropout: A simple way to prevent neural networks from overfitting.
  The Journal of Machine Learning Research, 2014.
- [94]

  Chris Stauffer and W Eric L Grimson.
  Adaptive background mixture models for real-time tracking.
  CVPR, 1999.
- [95]

  Matthew Tancik, Pratul Srinivasan, Ben Mildenhall, Sara Fridovich-Keil, Nithin
  Raghavan, Utkarsh Singhal, Ravi Ramamoorthi, Jonathan Barron, and Ren Ng.
  Fourier features let networks learn high frequency functions in low
  dimensional domains.
  NeurIPS, 2020.
- [96]

  Yansong Tang, Yi Tian, Jiwen Lu, Jianjiang Feng, and Jie Zhou.
  Action recognition in RGB-D egocentric videos.
  ICIP, 2017.
- [97]

  Yansong Tang, Zian Wang, Jiwen Lu, Jianjiang Feng, and Jie Zhou.
  Multi-stream deep neural networks for RGB-D egocentric action
  recognition.
  IEEE Transactions on Circuits and Systems for Video Technology,
  2019.
- [98]

  The World Bank.
  The world by income and regions, 2022.
  <https://datatopics.worldbank.org/world-development-indicators/the-world-by-income-and-region.html>.
- [99]

  Sebastian Thrun.
  Is learning the n-th thing any easier than learning the first?
  NeurIPS, 1995.
- [100]

  Cameron Trotter, Georgia Atkinson, Matt Sharpe, Kirsten Richardson, A. Stephen
  McGough, Nick Wright, Ben Burville, and Per Berggren.
  NDD20: A large-scale few-shot dolphin dataset for coarse and
  fine-grained categorisation.
  arXiv:2005.13359, 2020.
- [101]

  United States Environmental Protection Agency.
  Greenhouse Gas Equivalencies Calculator.
  <https://www.epa.gov/energy/greenhouse-gas-equivalencies-calculator>,
  2022.
- [102]

  Koen EA van de Sande, Jasper RR Uijlings, Theo Gevers, and Arnold WM Smeulders.
  Segmentation as selective search for object recognition.
  ICCV, 2011.
- [103]

  Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones,
  Aidan N Gomez, Lukasz Kaiser, and Illia Polosukhin.
  Attention is all you need.
  NeurIPS, 2017.
- [104]

  Boying Wang, Libo Zhang, Longyin Wen, Xianglong Liu, and Yanjun Wu.
  Towards real-world prohibited item detection: A large-scale x-ray
  benchmark.
  CVPR, 2021.
- [105]

  Weiyao Wang, Matt Feiszli, Heng Wang, Jitendra Malik, and Du Tran.
  Open-world instance segmentation: Exploiting pseudo ground truth from
  learned pairwise affinity.
  CVPR, 2022.
- [106]

  Chao-Yuan Wu, Justin Johnson, Jitendra Malik, Christoph Feichtenhofer, and
  Georgia Gkioxari.
  Multiview compressive coding for 3D reconstruction.
  CVPR, 2023.
- [107]

  Jianxiong Xiao, James Hays, Krista Ehinger, Aude Oliva, and Antonio Torralba.
  SUN database: Large-scale scene recognition from abbey to zoo.
  CVPR, 2010.
- [108]

  Saining Xie and Zhuowen Tu.
  Holistically-nested edge detection.
  ICCV, 2015.
- [109]

  Ning Xu, Brian Price, Scott Cohen, Jimei Yang, and Thomas S Huang.
  Deep interactive object selection.
  CVPR, 2016.
- [110]

  Kaiyu Yang, Klint Qinami, Li Fei-Fei, Jia Deng, and Olga Russakovsky.
  Towards fairer datasets: Filtering and balancing the distribution of
  the people subtree in the imagenet hierarchy.
  Proceedings of the 2020 conference on fairness, accountability,
  and transparency, 2020.
- [111]

  Lei Yang, Yan Zi Wei, Yisheng HE, Wei Sun, Zhenhang Huang, Haibin Huang, and
  Haoqiang Fan.
  iShape: A first step towards irregular shape instance segmentation.
  arXiv:2109.15068, 2021.
- [112]

  Senthil Yogamani, Ciarán Hughes, Jonathan Horgan, Ganesh Sistu, Padraig
  Varley, Derek O’Dea, Michal Uricár, Stefan Milz, Martin Simon, Karl
  Amende, et al.
  WoodScape: A multi-task, multi-camera fisheye dataset for
  autonomous driving.
  ICCV, 2019.
- [113]

  Lingzhi Zhang, Shenghao Zhou, Simon Stent, and Jianbo Shi.
  Fine-grained egocentric hand-object segmentation: Dataset, model, and
  applications.
  ECCV, 2022.
- [114]

  Wenwei Zhang, Jiangmiao Pang, Kai Chen, and Chen Change Loy.
  K-Net: Towards unified image segmentation.
  NeurIPS, 2021.
- [115]

  Jieyu Zhao, Tianlu Wang, Mark Yatskar, Vicente Ordonez, and Kai-Wei Chang.
  Men also like shopping: Reducing gender bias amplification using
  corpus-level constraints.
  arXiv:1707.09457, 2017.
- [116]

  Bolei Zhou, Agata Lapedriza, Aditya Khosla, Aude Oliva, and Antonio Torralba.
  Places: A 10 million image database for scene recognition.
  TPAMI, 2017.
- [117]

  Bolei Zhou, Hang Zhao, Xavier Puig, Tete Xiao, Sanja Fidler, Adela Barriuso,
  and Antonio Torralba.
  Semantic understanding of scenes through the ADE20K dataset.
  IJCV, 2019.

## 附录

#### 目录：

- §A：分割一切模型与任务细节
- §B：自动掩码生成细节
- §C：RAI 补充细节
- §D：实验实现细节
- §E：人工研究实验设计
- §F：数据集卡、标注卡与模型卡
- §G：标注指南

## 附录 A 分割一切模型与任务细节

#### 图像编码器。

总体而言，图像编码器可以是任何输出 C×H×W 图像嵌入的网络。出于可扩展性及可获得强大预训练的考虑，我们使用经 MAE [[47](#bib.bib47)] 预训练、并做了最小改动以处理高分辨率输入的 Vision Transformer（ViT）[[33](#bib.bib33)]，具体为 ViT-H/16，采用 14×14 窗口注意力与四个等距全局注意力块，遵循 [[62](#bib.bib62)]。图像编码器的输出是输入图像 16× 下采样的嵌入。由于我们的运行时目标是实时处理每个提示，图像编码器可以有很高的 FLOPs，因为它每张图像只计算一次，而*不是*每个提示计算一次。

遵循标准做法（如 [[40](#bib.bib40)]），我们使用 1024×1024 的输入分辨率，通过对图像重新缩放并对短边填充得到。因此图像嵌入为 64×64。为缩减通道维度，遵循 [[62](#bib.bib62)]，我们先使用 1×1 卷积得到 256 通道，再使用一个同样输出 256 通道的 3×3 卷积。每个卷积后接层归一化 [[4](#bib.bib4)]。

#### 提示编码器。

稀疏提示按如下方式映射为 256 维向量嵌入。一个点表示为该点位置的位置编码 [[95](#bib.bib95)] 与两个学习嵌入之一（指明该点属于前景还是背景）之和。一个框用一对嵌入表示：(1) 其左上角的位置编码加上表示「左上角」的学习嵌入，(2) 同样结构但使用表示「右下角」的学习嵌入。最后，为表示自由格式文本，我们使用 CLIP [[82](#bib.bib82)] 的文本编码器（一般而言任何文本编码器皆可）。本节余下部分我们聚焦几何提示，文本提示在 §D.5 中深入讨论。

稠密提示（即掩码）与图像有空间对应关系。我们以比输入图像低 4× 的分辨率输入掩码，再用两个 2×2、步长为 2、输出通道分别为 4 和 16 的卷积额外下采样 4×。最后一个 1×1 卷积将通道维度映射为 256。各层之间以 GELU 激活 [[50](#bib.bib50)] 与层归一化分隔。随后掩码嵌入与图像嵌入逐元素相加。如果没有掩码提示，则向每个图像嵌入位置加入一个表示「无掩码」的学习嵌入。

图 14：轻量级掩码解码器细节。一个两层解码器通过交叉注意力同时更新图像嵌入与提示词元。然后对图像嵌入上采样，并用更新后的输出词元动态预测掩码。（为清晰起见未在图中展示：在每个注意力层，位置编码会被加到图像嵌入上；完整的原始提示词元（含位置编码）会被重新加到词元的查询与键上。）

#### 轻量级掩码解码器。

该模块将图像嵌入与一组提示嵌入高效映射为输出掩码。为融合这些输入，我们从 Transformer 分割模型 [[14](#bib.bib14), [20](#bib.bib20)] 汲取灵感并修改标准 Transformer 解码器 [[103](#bib.bib103)]。在应用解码器之前，我们先向提示嵌入集合中插入一个学习的输出词元嵌入，它将用于解码器的输出，类似于 [[33](#bib.bib33)] 中的 [class] 词元。为简单起见，我们将这些嵌入（*不含*图像嵌入）统称为「词元」（tokens）。

我们的解码器设计见图 14。每个解码器层执行 4 步：(1) 词元自注意力，(2) 从词元（作为查询）到图像嵌入的交叉注意力，(3) 逐点 MLP 更新每个词元，(4) 从图像嵌入（作为查询）到词元的交叉注意力。最后一步用提示信息更新图像嵌入。在交叉注意力中，图像嵌入被视为 64² 个 256 维向量的集合。每个自/交叉注意力与 MLP 都带有残差连接 [[49](#bib.bib49)]、层归一化，训练时使用 0.1 的 dropout [[93](#bib.bib93)]。下一个解码器层接收上一层更新后的词元与图像嵌入。我们使用两层解码器。

为确保解码器能获取关键几何信息，只要图像嵌入参与注意力层，位置编码就会被加到其上。此外，只要提示词元参与注意力层，*完整的*原始提示词元（含其位置编码）会被重新加到更新后的词元上。这使其能够强烈依赖于提示词元的几何位置与类型。

运行解码器后，我们用两个转置卷积层将更新后的图像嵌入上采样 4×（此时相对输入图像下采样 4×）。然后，词元再一次对图像嵌入做注意力，我们把更新后的输出词元嵌入送入一个输出向量与上采样图像嵌入通道维度匹配的小型 3 层 MLP。最后，我们用上采样图像嵌入与 MLP 输出之间的空间逐点乘积预测掩码。

Transformer 的嵌入维度为 256。Transformer MLP 块的内部维度较大，为 2048，但该 MLP 仅应用于数量相对较少的提示词元（很少超过 20 个）。然而，在图像嵌入为 64×64 的交叉注意力层中，为提高计算效率，我们将查询、键、值的通道维度缩减 2× 至 128。所有注意力层使用 8 个头。

用于上采样输出图像嵌入的转置卷积为 2×2、步长 2，输出通道维度分别为 64 和 32，并带有 GELU 激活。它们之间以层归一化分隔。

#### 使模型具备歧义感知能力。

如前所述，单个输入提示可能有歧义，即对应多个有效掩码，而模型会学会在这些掩码上取平均。我们用简单的修改消除这一问题：不预测单个掩码，而是使用少量输出词元并同时预测多个掩码。默认情况下我们预测三个掩码，因为我们观察到三层（整体、部分、子部分）通常足以描述嵌套掩码。训练时，我们计算真值与每个预测掩码之间的损失（稍后描述），但只从最低损失反向传播。这是多输出模型常用的一项技术 [[15](#bib.bib15), [45](#bib.bib45), [64](#bib.bib64)]。为便于应用，我们希望对预测掩码排序，因此添加了一个小头（在一个额外的输出词元上运行）来估计每个预测掩码与其覆盖物体的 IoU。

在多提示情况下歧义要少见得多，三个输出掩码通常会变得相似。为了尽量减少训练时退化损失的计算，并确保单一无歧义掩码获得正常的梯度信号，当给定多个提示时我们只预测单个掩码。这通过为额外的掩码预测添加第四个输出词元实现。这个第四掩码在单提示时从不返回，而在多提示时是唯一返回的掩码。

#### 损失。

我们用 focal loss [[65](#bib.bib65)] 与 dice loss [[73](#bib.bib73)] 以 20:1 的线性组合监督掩码预测，遵循 [[20](#bib.bib20), [14](#bib.bib14)]。与 [[20](#bib.bib20), [14](#bib.bib14)] 不同，我们观察到在每个解码器层之后的辅助深度监督并无帮助。IoU 预测头用 IoU 预测值与预测掩码对真值掩码的 IoU 之间的均方误差损失训练，并以 1.0 的常数缩放因子加到掩码损失上。

#### 训练算法。

遵循近期方法 [[92](#bib.bib92), [37](#bib.bib37)]，我们在训练时模拟交互式分割设置。首先，以相同概率为目标掩码随机选择一个前景点或边界框。点从真值掩码中均匀采样。框取为真值掩码的边界框，并对每个坐标添加标准差等于框边长 10%、最大 20 像素的随机噪声。这一噪声特性在两类应用之间是合理折中：实例分割会围绕目标物体产生紧凑的框，而交互式分割中用户可能画出宽松的框。

从第一个提示做出预测后，后续点从上一次掩码预测与真值掩码之间的错误区域中均匀选取。若错误区域为假阴性或假阳性，则每个新点分别取为前景或背景。我们还将上一轮迭代的掩码预测作为额外提示提供给模型。为给下一轮迭代提供最大信息，我们提供未阈值化的掩码 logits 而非二值化掩码。当返回多个掩码时，传递给下一轮迭代并用于采样下一个点的是预测 IoU 最高的那个掩码。

我们发现 8 个迭代采样点之后收益递减（我们最多测试过 16 个）。此外，为鼓励模型从提供的掩码中获益，我们还使用两轮不采样额外点的迭代。其中一轮随机插入在 8 个迭代采样点之间，另一轮始终在最后。这样共 11 轮迭代：一个采样的初始输入提示、8 个迭代采样的点，以及两轮不向模型提供新外部信息的迭代，使其学会细化自身的掩码预测。我们注意到，之所以能使用相对较多的迭代次数，是因为我们的轻量级掩码解码器所需算力不到图像编码器的 1%，因此每轮迭代只增加很小的开销。这与以往的交互式方法不同，后者每次优化器更新只执行一次或少数几步交互 [[70](#bib.bib70), [9](#bib.bib9), [37](#bib.bib37), [92](#bib.bib92)]。

#### 训练配方。

我们使用 AdamW [[68](#bib.bib68)] 优化器（β₁=0.9，β₂=0.999），250 轮迭代的线性学习率 warmup [[42](#bib.bib42)] 以及阶梯式学习率衰减。warmup 之后的初始学习率（*lr*）为 8e-4。我们训练 90k 轮迭代（约 2 个 SA-1B epoch），并在 60k 轮迭代时将 *lr* 降低 10 倍，在 86666 轮时再降低 10 倍。批大小为 256 张图像。为对 SAM 进行正则化，我们设置权重衰减（*wd*）为 0.1，并以 0.4 的比率应用 drop path [[53](#bib.bib53)]（*dp*）。我们使用 0.8 的逐层学习率衰减 [[5](#bib.bib5)]（*ld*）。未使用数据增强。我们从 MAE [[47](#bib.bib47)] 预训练的 ViT-H 初始化 SAM。由于图像编码器庞大且输入为 1024×1024，我们将训练分布在 256 块 GPU 上。为限制 GPU 显存占用，每块 GPU 最多训练 64 个随机采样的掩码。此外，我们发现对 SA-1B 掩码做轻度过滤、丢弃覆盖超过图像 90% 的掩码，可在定性上改进结果。

对于消融及其他训练变体（如文本到掩码 §D.5），我们对上述默认配方做如下调整。当仅用数据引擎第一、二阶段的数据训练时，我们对输入做尺度范围为 [0.1, 2.0] 的大尺度抖动（large-scale jitter）[[40](#bib.bib40)] 增强。直观上，训练数据较有限时数据增强可能有帮助。训练 ViT-B 与 ViT-L 时，我们使用 180k 轮迭代，批大小 128，分布在 128 块 GPU 上。对 ViT-B/L 分别设置 *lr* = 8e-4/4e-4、*ld* = 0.6/0.8、*wd* = 0.1、*dp* = 0.6/0.4。

## 附录 B 自动掩码生成细节

这里讨论用于生成所发布 SA-1B 的数据引擎全自动阶段细节。

#### 裁剪。

掩码在全图上由 32×32 的规则点网格生成，另有 20 个来自 2×2 与 4×4 部分重叠窗口的放大裁剪，分别使用 16×16 与 8×8 的规则点网格。裁剪使用原始高分辨率图像（这是唯一一次使用它们）。我们移除了接触裁剪内边界的掩码。我们分两阶段应用标准的基于框的贪心 NMS（出于效率使用框）：先在每个裁剪内，再跨裁剪。在裁剪内应用 NMS 时，我们用模型预测的 IoU 对掩码排序。跨裁剪应用 NMS 时，我们依据来源裁剪，把掩码从放大最多（即来自 4×4 裁剪）到放大最少（即原图）排序。两种情况下，NMS 阈值均取 0.7。

#### 过滤。

我们使用三个过滤器提升掩码质量。第一，为只保留*高置信度*掩码，我们按模型预测的 IoU 分数以 88.0 的阈值过滤。第二，为只保留*稳定*掩码，我们对同一底层软掩码在不同值处阈值化得到两个二值掩码并比较。只有当 -1 与 +1 阈值化掩码对的 IoU 大于等于 95.0 时，才保留该预测（即在 0 处对 logits 阈值化得到的二值掩码）。第三，我们注意到偶尔会有自动掩码覆盖整张图像。这类掩码通常无意义，我们通过移除覆盖图像 95% 及以上的掩码来过滤。所有过滤阈值的选择，都是为了按 §5 中描述的方法、由专业标注者评判，同时获得大量掩码与高质量掩码。

#### 后处理。

我们观察到两类易于通过后处理缓解的错误。第一，估计约 4% 的掩码包含细小的虚假成分。为此，我们移除面积小于 100 像素的连通成分（若最大成分低于该阈值，则移除整个掩码）。第二，另有估计约 4% 的掩码包含细小的虚假孔洞。为此，我们填充面积小于 100 像素的孔洞。孔洞被识别为反转掩码的成分。

#### 自动掩码生成模型。

我们训练了一个用于全自动掩码生成的特殊版本 SAM，它以牺牲部分推理速度换取更好的掩码生成特性。我们在此说明默认 SAM 与用于数据生成的 SAM 之间的差异：后者仅在人工与半自动数据上训练；训练时间更长（177656 轮迭代而非 90k），并使用大尺度抖动数据增强 [[40](#bib.bib40)]；模拟交互训练只使用点与掩码提示（不含框），且训练时每个掩码只采样 4 个点（从默认的 9 减到 4 加快了训练迭代，对 1 点性能无影响，但若以更多点评估会损害 mIoU）；最后，掩码解码器使用 3 层而非 2 层。

#### SA-1B 示例。

我们在图 2 中展示 SA-1B 样本。更多示例请见我们的[数据集浏览器](https://www.segment-anything.com/dataset/index.html)。

## 附录 C RAI 补充细节

#### 推断 SA-1B 的地理信息。

虽然 SA-1B 中的图像没有地理标记，但每张图像都有描述其内容及拍摄地点的说明文字。我们使用基于 Elmo 的命名实体识别模型 [[78](#bib.bib78)] 从这些说明中推断近似地理位置。每个提取出的地点实体被映射到所有匹配的国家、省份与城市。说明文字通过先考虑匹配的国家、再省份、最后城市，映射到单一国家。我们注意到该方法存在歧义与潜在偏见（例如「Georgia」可能指国家格鲁吉亚，也可能指美国佐治亚州）。因此，我们用提取的地点分析数据集整体，但不发布推断的地点。按照图像提供商的要求，说明文字不会公开发布。

#### 推断 COCO 与 Open Images 的地理信息。

COCO [[66](#bib.bib66)] 与 Open Images [[60](#bib.bib60)] 数据集不提供地理位置。遵循 [[29](#bib.bib29)]，我们通过 Flickr API 检索地理元数据。我们检索到 COCO 训练集 24%（19,562 张图像）的位置；对 Open Images，我们检索到训练集 18%（493,517 张图像，仅考虑含掩码的图像）。我们注意到地理信息是近似的，拥有该信息的图像样本可能不完全匹配完整数据集分布。

#### 推断收入信息。

我们用每张图像推断出的国家，按世界银行定义的收入水平 [[98](#bib.bib98)] 查询其收入等级。我们将中高收入与中低收入合并为单一的中等收入等级。

#### 人物分割的公平性。

为考察 SAM 分割人物的公平性，我们使用 Open Images [[60](#bib.bib60)] 的 More Inclusive Annotations for People（MIAP）[[87](#bib.bib87)] 测试集标注，以便跨感知性别表现与感知年龄段比较 SAM 的表现。MIAP 提供框标注，而本分析需要真值掩码。为获得真值掩码，我们从 Open Images 中选取每个人物类别掩码，条件是其对应边界框（基于相对框边长）与 MIAP 中标注的边界框误差在 1% 以内，共得到 3.9k 个掩码。

|  |  |  |
| --- | --- | --- |
|  | mIoU | |
|  | 1 点 | 3 点 |
| *感知性别表现* | | |
| 女性化 | 76.3±1.1 | 90.7±0.5 |
| 男性化 | 81.0±1.2 | 92.3±0.4 |

|  |  |  |
| --- | --- | --- |
|  | mIoU | |
|  | 1 点 | 3 点 |
| *感知年龄段* | | |
| 年长 | 81.9±3.8 | 92.8±1.6 |
| 中年 | 78.2±0.8 | 91.3±0.3 |
| 年轻 | 77.3±2.7 | 91.5±0.9 |

表 6：SAM 在感知性别表现与年龄段上的服装分割性能。感知性别的置信区间不相交，男性化的 mIoU 更高。年龄段的置信区间重叠。

#### 服装分割的公平性。

我们将 §6 的分析扩展到服装分割。我们考察 SAM 在服装上的表现与穿着者属性的关系。我们使用 Open Images 中属于服装超类别且位于 MIAP 人物框内的全部 6.5k 个真值掩码。在表 6 中，我们跨感知性别表现与年龄段比较性能。我们发现 SAM 在分割以男性化表现为主的人的服装时更好，95% 置信区间不相交。从 1 点评估转为 3 点评估时差距缩小。感知年龄段的差异不显著。我们的结果表明，以单点提示分割服装时，跨感知性别表现存在偏见，我们提醒 SAM 的用户注意这一局限。

## 附录 D 实验实现细节

### D.1 零样本单点有效掩码评估

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 数据集 | 缩写与链接 | 图像类型 | 描述 | 掩码类型 | 来源划分 | 采样图像数 | 采样掩码数 |
| Plant Phenotyping Datasets Leaf Segmentation [[74](#bib.bib74)] | [PPDLS](https://www.plant-phenotyping.org/datasets-home) | 植物 | 烟草与拟南芥图像的叶片分割。 | 实例 | N/A | 182 | 2347 |
| Broad Bioimage Benchmark Collection 中的 BBBC038v1 [[12](#bib.bib12)] | [BBBC038v1](https://bbbc.broadinstitute.org/BBBC038) | 显微镜 | 多种环境下细胞生物图像，检验细胞核分割的稳健性。 | 实例 | Train | 227 | 10506 |
| Dataset fOr bOuldeRs Segmentation [[80](#bib.bib80)] | [DOORS](https://zenodo.org/record/7107409#.ZAzNnOzMJ47) | 巨石 | 位于球面网格表面的单个巨石的分割掩码。 | 实例 | DS1 | 10000 | 10000 |
| TimberSeg 1.0 [[38](#bib.bib38)] | [TimberSeg](https://data.mendeley.com/datasets/y5npsm3gkj) | 原木 | 各种环境与条件下木材堆中单根原木的分割掩码。图像取自操作员视角。 | 实例 | N/A | 220 | 2487 |
| Northumberland Dolphin Dataset 2020 [[100](#bib.bib100)] | [NDD20](https://doi.org/10.25405/data.ncl.c.4982342) | 水下 | 水上与水下拍摄图像中两种不同海豚的分割掩码。 | 实例 | N/A | 4402 | 6100 |
| Large Vocabulary Instance Segmentation [[44](#bib.bib44)] | [LVIS](https://www.lvisdataset.org/) | 场景 | 对 COCO [[66](#bib.bib66)] 数据集的补充标注，用于研究长尾物体检测与分割。 | 实例 | Validation (v0.5) | 945 | 9642 |
| STREETS [[91](#bib.bib91)] | [STREETS](https://databank.illinois.edu/datasets/IDB-3671567) | 交通摄像头 | 交通摄像头画面中汽车的分割掩码。 | 实例 | N/A | 819 | 9854 |
| ZeroWaste-f [[6](#bib.bib6)] | [ZeroWaste-f](http://ai.bu.edu/zerowaste/) | 回收 | 杂乱场景中变形回收垃圾的分割掩码。 | 实例 | Train | 2947 | 6155 |
| iShape [[111](#bib.bib111)] | [iShape](https://ishape.github.io/) | 不规则形状 | 天线、原木、栅栏、衣架等不规则形状的分割掩码。 | 实例 | Validation | 754 | 9742 |
| ADE20K [[117](#bib.bib117)] | [ADE20K](https://groups.csail.mit.edu/vision/datasets/ADE20K/) | 场景 | 来自 SUN [[107](#bib.bib107)] 与 Places [[116](#bib.bib116)] 数据集图像的物体及部件分割掩码。 | 实例 | Validation | 302 | 10128 |
| Occluded Video Instance Segmentation [[81](#bib.bib81)] | [OVIS](http://songbai.site/ovis/) | 遮挡 | 视频中的实例分割掩码，聚焦被遮挡物体。 | 实例 | Train | 2044 | 10011 |
| Hypersim [[86](#bib.bib86)] | [Hypersim](https://github.com/apple/ml-hypersim) | 仿真 | 带实例掩码的逼真合成室内场景数据集。 | 实例 | Evermotion archinteriors volumes 1-55 excluding 20,25,40,49 | 338 | 9445 |
| Night and Day Instance Segmented Park [[22](#bib.bib22), [23](#bib.bib23)] | [NDISPark](https://zenodo.org/record/6560823#.ZAzLlezMJ46) | 停车场 | 白天与夜晚、不同天气与摄像头角度下视频画面的停车场图像，用于车辆分割。 | 实例 | Train | 111 | 2577 |
| EPIC-KITCHENS VISOR [[28](#bib.bib28), [27](#bib.bib27)] | [VISOR](https://epic-kitchens.github.io/VISOR/) | 自我中心 | 烹饪数据集 EPIC-KITCHENS [[27](#bib.bib27)] 自我中心视频中手与活动物体的分割掩码。 | 实例 | Validation | 1864 | 10141 |
| Plittersdorf dataset [[46](#bib.bib46)] | [Plittersdorf](https://timm.haucke.xyz/datasets/plittersdorf) | 立体图像 | 用 SOCRATES 立体相机陷阱拍摄的图像中野生动物的分割掩码。 | 实例 | Train, validation, test | 187 | 546 |
| Egocentric Hand-Object Segmentation [[113](#bib.bib113)] | [EgoHOS](https://github.com/owenzlz/EgoHOS) | 自我中心 | 细粒度自我中心手-物体分割数据集。该数据集为现有数据集提供掩码标注。 | 实例 | Train（仅含 Ego4D [[43](#bib.bib43)] 与 THU-READ [[97](#bib.bib97), [96](#bib.bib96)]） | 2940 | 9961 |
| InstanceBuilding 2D [[17](#bib.bib17)] | [IBD](https://californiachen.github.io/datasets/InstanceBuilding) | 无人机 | 标注了屋顶实例分割掩码的高分辨率无人机图像。 | 实例 | Train（2D 标注） | 467 | 11953 |
| WoodScape [[112](#bib.bib112)] | [WoodScape](https://woodscape.valeo.com/home) | 鱼眼驾驶 | 带分割掩码的鱼眼驾驶数据集。图像来自四个环视摄像头。 | 实例 | Set 1 | 107 | 10266 |
| Cityscapes [[25](#bib.bib25)] | [Cityscapes](https://www.cityscapes-dataset.com/) | 驾驶 | 带分割掩码的街景立体视频。 | 全景 | Validation | 293 | 9973 |
| PIDray [[104](#bib.bib104)] | [PIDRay](https://github.com/bywang2018/security-dataset) | X 射线 | 行李 X 射线图像中违禁品的分割掩码。 | 实例 | Test（hard） | 3733 | 8892 |
| Diverse Realism in Art Movements [[24](#bib.bib24)] | [DRAM](https://faculty.runi.ac.il/arik/site/artseg/Dram-Dataset.html) | 绘画 | 用于艺术绘画语义分割的领域自适应数据集。 | 语义 | Test | 718 | 1179 |
| TrashCan [[52](#bib.bib52)] | [TrashCan](https://conservancy.umn.edu/handle/11299/214865) | 水下 | 水下遥控载具（ROV）拍摄图像中垃圾的分割掩码。图像来自 J-EDI [[69](#bib.bib69)] 数据集。 | 实例 | Train（实例任务） | 5936 | 9540 |
| Georgia Tech Egocentric Activity Datasets [[34](#bib.bib34), [63](#bib.bib63)] | [GTEA](https://cbs.ic.gatech.edu/fpv/) | 自我中心 | 视频由四个不同受试者执行七类日常活动构成，带手的分割掩码。 | 实例 | Train（分割手任务） | 652 | 1208 |

表 7：用于以点提示评估零样本分割的分割数据集。23 个数据集覆盖广泛领域；见「图像类型」列。为提高评估效率，我们对掩码数超过 15k 的数据集做了子采样。具体而言，我们随机抽取图像，使图像中的掩码总数约为 10k。

#### 数据集。

我们用来自以往工作的 23 个多样化分割数据集构建了一个新的分割基准，以评估模型的零样本迁移能力。各数据集的描述见表 7。示例见正文图 8。该套件覆盖的领域包括自我中心 [[34](#bib.bib34), [28](#bib.bib28), [113](#bib.bib113)]、显微镜 [[12](#bib.bib12)]、X 射线 [[104](#bib.bib104)]、水下 [[52](#bib.bib52), [100](#bib.bib100)]、航拍 [[17](#bib.bib17)]、仿真 [[86](#bib.bib86)]、驾驶 [[25](#bib.bib25)] 与绘画 [[24](#bib.bib24)] 图像。为高效评估，我们对掩码超过 15k 的数据集做了子采样。具体而言，我们随机挑选图像，使采样图像中的掩码总数约为 10k。我们对所有数据集中的人脸做了模糊处理。

#### 点采样。

我们的默认点采样遵循交互式分割的标准做法 [[109](#bib.bib109), [64](#bib.bib64), [92](#bib.bib92)]。第一个点被确定性地选为距物体边界最远的点。后续每个点都取真值与上一次预测之间错误区域中距边界最远的点。一些实验（在文中注明）使用更具挑战性的采样策略：第一个点是*随机*点，而非确定性选择的「中心」点。后续点的选取方式同上。该设置更好地反映了第一个点并不可靠地位于掩码中心的使用场景，例如基于眼动注视的提示。

#### 评估。

我们测量 N 个点提示后的预测与真值掩码之间的 IoU，其中 N={1,2,3,5,9}，点按上述任一策略迭代采样。每个数据集的 mIoU 是该数据集所有物体的逐掩码 IoU 平均值。最后，我们对 23 个数据集的 mIoU 取平均作为首要指标。我们的评估不同于标准交互式分割评估协议（该协议测量达到 X% IoU 所需的平均点数，最多 20 个点）。我们聚焦仅一个或少数几个点之后的预测，因为我们的许多用例只涉及单个或极少的提示。鉴于我们的应用方向需要实时提示处理，我们预期在使用大量点时，最佳交互式分割模型会胜过 SAM。

#### 基线。

我们使用三个近期强交互式基线：RITM [[92](#bib.bib92)]、FocalClick [[18](#bib.bib18)] 与 SimpleClick [[67](#bib.bib67)]。对每个基线，我们使用作者公开发布的在最广泛数据集上训练的最大模型。对 RITM，我们使用作者提出的、在 COCO [[66](#bib.bib66)] 与 LVIS [[44](#bib.bib44)] 组合上训练的 HRNet32 IT-M。对 FocalClick，我们使用在包含 8 个不同分割数据集的「组合数据集」[[18](#bib.bib18)] 上训练的 SegFormerB3-S2。对 SimpleClick，我们使用在 COCO 与 LVIS 组合上训练的 ViT-H448。我们遵循建议的默认数据预处理策略（即数据增强或图像缩放），不为我们的评估更改或适配任何参数。在实验中，我们观察到 RITM 在我们的 23 个数据集套件上的 1 点评估中优于其他基线。因此，我们默认与 RITM 比较。以更多点评估时，我们报告所有基线的结果。

#### 单点歧义与 oracle 评估。

除 N 点提示后的 IoU 之外，我们还报告 SAM 在 1 点时的「oracle」性能：在 SAM 的三个预测中评估与真值最匹配的预测掩码（而非像默认那样使用 SAM 自己排名第一的掩码）。该协议通过放宽「必须在多个有效物体中猜出唯一正确掩码」的要求，来解决单点提示可能的歧义。

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| 图像 | 真值 | SAM | 图像 | 真值 | SAM |
| 示例 | 示例 | 示例 | 示例 | 示例 | 示例 |
| 示例 | 示例 | 示例 | 示例 | 示例 | 示例 |

图 15：BSDS500 上零样本边缘预测的更多可视化。回顾一下，SAM 未被训练去预测边缘图，训练期间也未接触 BSDS 图像与标注。

### D.2 零样本边缘检测

#### 数据集与指标。

我们在 BSDS500 [[72](#bib.bib72), [3](#bib.bib3)] 上进行零样本边缘检测实验。每张图像的真值来自五个不同受试者的人工标注。我们在 200 张图像的测试子集上报告结果，使用边缘检测的四项标准指标 [[3](#bib.bib3), [32](#bib.bib32)]：最优数据集尺度（ODS）、最优图像尺度（OIS）、平均精度（AP）与 50% 精度下的召回率（R50）。

#### 方法。

为零样本迁移，我们使用自动掩码生成流水线的简化版本。我们用 16×16 的规则前景点网格提示 SAM，得到 768 个预测掩码（每个点三个）。我们不按预测 IoU 或稳定性过滤。冗余掩码由 NMS 去除。然后我们对剩余掩码的未阈值化概率图应用 Sobel 滤波，并将不与掩码外边界像素相交的值置零。最后，我们对所有预测取逐像素最大值，将结果线性归一化到 [0,1]，并应用边缘 NMS [[13](#bib.bib13)] 细化边缘。

#### 可视化。

在图 15 中，我们展示了 SAM 零样本边缘预测的更多示例。这些定性示例进一步说明，尽管 SAM 未针对边缘检测训练，它仍倾向于输出合理的边缘图。我们看到边缘能与人工标注良好对齐。不过，如前所述，由于 SAM 未针对边缘检测训练，它没有学到 BSDS500 数据集的偏差，常常输出比真值标注更多的边缘。

### D.3 零样本物体候选框

#### 数据集与指标。

我们在 LVIS v1 验证集 [[44](#bib.bib44)] 上报告 1000 个候选下掩码的标准平均召回率（AR）指标。由于 LVIS 为 1203 个物体类别提供高质量掩码，它为物体候选框生成提供了挑战性测试。鉴于模型的开放世界性质——即使在 LVIS 的 1203 类之外也可能产生许多有效掩码——我们聚焦 AR@1000。为测量频繁、常见与稀有类别上的表现，我们使用 AR@1000，但真值集仅包含相应的 LVIS 类别。

#### 基线。

我们使用 cascade ViTDet-H 作为基线，即 [[62](#bib.bib62)] 中按 LVIS 上 AP 衡量的最强模型。如正文所述，域内训练的物体检测器可以「钻」AR 的空子 [[16](#bib.bib16)]，预期是比其他聚焦开放世界候选或分割的模型 [[58](#bib.bib58), [105](#bib.bib105)] 更强的基线。为产生 1000 个候选，我们在三个 cascade 阶段禁用分数阈值，并将每阶段的最大预测数提高到 1000。

#### 方法。

我们使用修改版的 SAM 自动掩码生成流水线进行零样本迁移。第一，为使推理时间与 ViTDet 相当，我们不处理图像裁剪。第二，我们移除了按预测 IoU 与稳定性的过滤。这样剩下两个可调参数来获得每图约 1000 个掩码：输入点网格与重复掩码抑制的 NMS 阈值。我们选择 64×64 点网格与 0.9 的 NMS 阈值，平均每张图像产生约 900 个掩码。评估时，若某张图像提出的掩码超过 1000 个，则按置信度与稳定性分数的均值排序，截取前 1000 个候选。

我们推测，SAM 输出多个掩码的能力对该任务尤其有价值，因为召回率应受益于从单个输入点在多个尺度上生成的候选。为检验这一点，我们与一个只输出单个掩码（而非三个）的消融版 SAM（SAM - 单输出）比较。由于该模型产生的掩码更少，我们进一步把采样点数与 NMS 阈值分别提高到 128×128 与 0.95，平均每张图像获得约 950 个掩码。此外，单输出 SAM 不产生自动掩码生成流水线中用于 NMS 排序的 IoU 分数，因此掩码被随机排序。测试表明，这与更精细的掩码排序方法（如用掩码的最大 logit 值作为模型置信度的代理）性能相近。

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| 真值 | ViTDet | SAM | 真值 | ViTDet | SAM |
| 示例 | 示例 | 示例 | 示例 | 示例 | 示例 |
| 示例 | 示例 | 示例 | 示例 | 示例 | 示例 |

图 16：LVIS v1 上的零样本实例分割。SAM 产生比 ViTDet 质量更高的掩码。作为零样本模型，SAM 没有机会学到特定的训练数据偏差；见右上角示例，SAM 做出了模态（modal）预测，而 LVIS 真值是非模态（amodal）的，因为 LVIS 的掩码标注没有孔洞。

### D.4 零样本实例分割

#### 方法。

对于零样本实例分割，我们用全监督 ViTDet-H 在 COCO 与 LVIS v1 验证集上输出的框提示 SAM。我们额外进行一轮掩码细化迭代：将置信度最高的预测掩码连同框提示一起送回掩码解码器以产生最终预测。我们在图 16 中展示 LVIS 上的零样本实例分割预测。与 ViTDet 相比，SAM 倾向于产生边界更干净的高质量掩码。我们通过 §7.4 的人工研究证实了这一观察。注意，作为零样本模型，SAM 无法学到数据集的标注偏差。例如，我们看到 SAM 对盘子做出了有效的模态预测，而 LVIS 掩码在设计上不能包含孔洞，因此盘子被标注为非模态。

### D.5 零样本文本到掩码

#### 模型与训练。

我们使用最大的公开 CLIP 模型 [[82](#bib.bib82)]（ViT-L/14@336px）计算文本与图像嵌入，并在使用前做 ℓ2 归一化。为训练 SAM，我们使用数据引擎前两个阶段的掩码。此外，我们丢弃所有面积小于 100² 像素的掩码。我们用大尺度抖动 [[40](#bib.bib40)] 训练该模型 120k 轮迭代，批大小 128。其余训练参数遵循默认设置。

#### 生成训练提示。

为提取输入提示，我们首先将每个掩码周围的边界框按 1× 到 2× 的随机因子扩展，对扩展后的框做方形裁剪以保持纵横比，并调整到 336×336 像素。在把裁剪送入 CLIP 图像编码器之前，我们以 50% 的概率将掩码外的像素置零。为确保嵌入聚焦于物体，我们在最后一层使用掩码注意力，把输出词元的注意力限制在掩码内的图像位置上。最后，我们的提示即该输出词元嵌入。训练时我们先提供基于 CLIP 的提示，再以额外的迭代点提示细化预测。

#### 推理。

推理时，我们不做任何修改地使用 CLIP 文本编码器为 SAM 创建提示。我们依赖于 CLIP 已将文本与图像嵌入对齐这一事实，这使我们无需任何显式文本监督即可训练，同时推理时使用基于文本的提示。

![](2304.02643v1/latent_visualization.png)

图 17：对 SAM 潜在空间中掩码嵌入相似度做阈值化的可视化。查询由品红色框指示；上行为低阈值下的匹配，下行为高阈值下的匹配。同一图像中最相似的掩码嵌入往往在语义上与查询掩码嵌入相似，尽管 SAM 未用显式语义监督训练。

### D.6 探索 SAM 的潜在空间

最后，我们做一项初步研究，定性探查 SAM 学到的潜在空间。具体而言，我们感兴趣的是：即使未用显式语义监督训练，SAM 的表示是否仍能捕获某些语义。为此，我们计算*掩码嵌入*：从掩码周围的图像裁剪及其水平翻转版本中提取 SAM 图像嵌入，将图像嵌入乘以二值掩码，并在空间位置上取平均。在图 17 中，我们展示了查询掩码与同一图像中（潜在空间内）相似掩码的 3 个示例。我们观察到，每个查询的最近邻显示出一定（尽管不完美）的形状与语义相似性。虽然这些结果是初步的，但它们表明 SAM 的表示可能对多种用途有价值，例如进一步的数据标注、理解数据集内容，或作为下游任务的特征。

## 附录 E 人工研究实验设计

这里描述用于评估 §7.1 与 §7.4 中掩码质量的人工研究细节。人工研究的目的在于解决用「与真值的 IoU」衡量预测掩码质量的两个局限。第一个局限是，对于单点这类歧义输入，模型可能因返回了不同于真值的另一个物体的有效掩码而受到严重惩罚。第二个局限是，真值掩码可能包含各种偏差，例如边缘质量的系统性错误，或对遮挡物体采用模态/非模态分割的取舍。域内训练的模型能学到这些偏差，在不一定产生更好掩码的情况下获得更高 IoU。人工评审可以获得独立于底层真值掩码的掩码质量度量，从而缓解这些问题。

#### 模型。

对于单点评估，我们使用 RITM [[92](#bib.bib92)]、单输出 SAM 与 SAM 检验两个假设。第一，我们假设在给定单点时，SAM 产生视觉质量高于基线交互式分割模型的掩码，即使与真值的 IoU 等指标无法揭示这一点。第二，我们假设 SAM 消解掩码歧义的能力提升了单点输入的掩码质量，因为单输出 SAM 可能返回在歧义掩码上取平均的掩码。

对于实例分割实验，我们评估 cascade ViTDet-H [[62](#bib.bib62)] 与 SAM，以检验「即使因无法学到验证集特定标注偏差而获得较低 AP，SAM 仍产生视觉质量更高的掩码」这一假设。

#### 数据集。

对于单点实验，我们从 23 个数据集中选取 7 个，因为完整套件对人工评审而言过大。我们选择 LVIS v0.5 [[17](#bib.bib17)]、VISOR [[28](#bib.bib28), [27](#bib.bib27)]、DRAM [[24](#bib.bib24)]、IBD [[17](#bib.bib17)]、NDD20 [[100](#bib.bib100)]、OVIS [[81](#bib.bib81)] 与 iShape [[111](#bib.bib111)]，它们提供了多样化的图像，包括场景级、自我中心、绘制、俯拍、水下与合成图像。此外，该集合既包含按 IoU 指标 SAM 优于 RITM 的数据集，也包含反之的数据集。对于实例分割实验，我们使用 LVIS v1 验证集，可与在 LVIS 上训练的 ViTDet 直接比较。

#### 方法论。

我们将模型生成的掩码展示给专业标注者，请他们按提供的准则（完整准则见附录 G）为每个掩码评分。标注者来自为数据引擎收集人工标注掩码的同一家公司。标注者可以查看图像、单个模型的预测掩码以及模型输入（单点或单框），并被要求按三条标准评判掩码：掩码是否对应有效物体？掩码边界是否干净？掩码是否与输入对应？然后提交 1-10 的评分表示掩码的总体质量。

1 分表示掩码完全不对应任何物体；低分（2-4）表示掩码有巨大错误，例如包含其他物体的大块区域或大面积无意义的边界；中等分数（5-6）表示掩码大体合理但仍有显著的语义或边界错误；高分（7-9）表示掩码只有轻微的边界错误；10 分表示掩码无可视错误。标注者可使用五种不同视图，每种用于帮助识别不同类型的错误。

对于单点实验，每个数据集从用于零样本交互式分割基准的相同子集中随机选取 1000 个掩码（子集细节见附录 D.1）。模型输入是最中心的点，计算为距掩码边缘的距离变换的最大值。对于实例分割实验，从 LVIS v1 验证集选取 1000 个掩码，模型输入为 LVIS 真值框。在所有实验中，尺寸小于 24² 像素的掩码被排除在采样之外，以避免向评分者展示过小而难以准确评判的掩码。出于内存与显示原因，大图像在预测掩码前被缩放到最大边长 2000。在所有实验中，相同输入被送入每个模型以产生预测掩码。

作为比较，各数据集的真值掩码也提交评分。对于单点实验，每个数据集共 4000 个评分任务（RITM、单输出 SAM、SAM 与真值各 1000 个掩码）；对于实例分割实验，共 3000 个任务（ViTDet、SAM 与真值）。

（a）LVIS v0.5 [[17](#bib.bib17)]

（b）VISOR [[28](#bib.bib28), [27](#bib.bib27)]

（c）DRAM [[24](#bib.bib24)]

（d）IBD [[17](#bib.bib17)]

（e）NDD20 [[100](#bib.bib100)]

（f）OVIS [[81](#bib.bib81)]

（g）iShape [[111](#bib.bib111)]

图 18：人工评估研究中各数据集的掩码质量评分分布。

对每个数据集，这些任务以随机顺序插入队列，由 30 名标注者从中领取。在评审研究的初期测试中，我们把每个任务交给五名不同标注者，发现评分具有合理的一致性：五名标注者评分的平均标准差为 0.83。此外，标注公司部署了质量保障测试人员，对一部分结果进行抽查，以发现严重偏离准则的情况。因此在正式实验中，每个任务（即对一张图像中的一个掩码评分）只由一名标注者完成。每名标注者每个任务的平均耗时为 90 秒，长于我们最初 30 秒的目标，但仍足够快，可以在选定的 7 个数据集上收集大量评分。

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
|  | SAM >> 基线 | | SAM >> 单输出 SAM | |
| 数据集 | p 值 | CI99(Δμ) | p 值 | CI99(Δμ) |
| *点输入（基线为 RITM [[92](#bib.bib92)]）：* | | | | |
| LVIS v0.5 [[44](#bib.bib44)] | 4e-69 | (1.40, 1.84) | 2e-11 | (0.29, 0.64) |
| VISOR [[28](#bib.bib28), [27](#bib.bib27)] | 7e-98 | (1.81, 2.24) | 7e-26 | (0.58, 0.94) |
| DRAM [[24](#bib.bib24)] | 1e-76 | (1.54, 2.00) | 2e-24 | (0.62, 1.03) |
| IBD [[17](#bib.bib17)] | 2e-57 | (1.03, 1.39) | 1e-15 | (0.32, 0.62) |
| NDD20 [[100](#bib.bib100)] | 2e-86 | (1.88, 2.37) | 5e-08 | (0.19, 0.55) |
| OVIS [[81](#bib.bib81)] | 2e-64 | (1.38, 1.84) | 3e-10 | (0.27, 0.63) |
| iShape [[111](#bib.bib111)] | 2e-88 | (1.97, 2.47) | 7e-23 | (0.65, 1.10) |
| *框输入（基线为 ViTDet-H [[62](#bib.bib62)]）：* | | | | |
| LVIS v1 [[44](#bib.bib44)] | 2e-05 | (0.11, 0.42) | N/A | N/A |

表 8：表明 SAM 的掩码质量评分显著高于基线及单输出 SAM 的统计检验。p 值由配对 t 检验计算，均值差置信区间由 1 万次配对自助法（bootstrap）计算。所有 p 值均显著，所有置信区间均不含零。

#### 结果。

图 18 展示单点实验中各数据集评分的直方图。我们对两个假设进行统计检验：(1) SAM 得分高于基线模型（RITM 或 ViTDet）；(2) SAM 得分高于单输出 SAM。p 值通过对模型得分均值的配对 t 检验计算，并辅以 1 万次样本的配对自助检验求均值差的 99% 置信区间。表 8 展示这些检验的 p 值与置信区间。所有统计检验均高度显著，所有置信区间均不含零。

对于实例分割，正文图 11 展示评分直方图。为了与 COCO 真值比较，我们额外纳入 794 条在测试人工评审流程期间收集的 COCO 真值掩码评分。这些掩码以与 LVIS 结果完全相同的设置展示给评分者。为公平比较，图 11 中 LVIS 的结果被子采样为每个模型与真值相同的 794 个输入。表 8 使用完整的 1000 条评分进行统计检验，表明 SAM 相对 ViTDet 的掩码质量提升具有统计显著性。

## 附录 F 数据集卡、标注卡与模型卡

在 §F.1 中，我们遵循 [[39](#bib.bib39)]，以问答列表形式提供 SA-1B 的数据集卡。接下来，我们遵循 CrowdWorkSheets [[30](#bib.bib30)]，在 §F.2 中为 §4 描述的数据引擎前两个阶段提供数据标注卡，同样以问答列表形式。我们在表 9 中提供遵循 [[75](#bib.bib75)] 的模型卡。

### F.1 SA-1B 数据集卡

#### 动机

1. 数据集为何而创建？是否有特定任务考量？是否有需要填补的特定空白？请提供描述。我们的数据集对视觉社区的贡献有四：(1) 我们发布包含 1100 万张图像与 11 亿个掩码的数据集，是迄今最大的分割数据集。(2) 我们发布的数据集保护隐私：我们已对所有图像中的人脸与牌照做模糊处理。(3) 数据集在宽泛的使用条款下授权，条款见 <https://ai.facebook.com/datasets/segment-anything>。(4) 数据在地理上比以往数据集更加多样，我们希望它能让社区向构建更公平、更公正的模型再进一步。
2. 数据集由谁创建（如哪个团队、研究组），代表哪个实体（如公司、机构、组织）？数据集由 Meta AI 的 FAIR 团队创建。底层图像从第三方摄影公司收集并授权。
3. 谁资助了数据集的创建？若有相关资助，请提供资助方名称及资助名称与编号。数据集的创建由 Meta AI 资助。
4. 还有其他说明吗？无。

#### 构成

1. 组成数据集的实例代表什么（如文档、照片、人物、国家）？是否存在多种类型的实例（如电影、用户与评分；人物及其交互；节点与边）？请提供描述。数据集中的所有实例均为照片。照片主题各异；常见主题包括：地点、物体、场景。所有照片互不相同，但有一些照片拍摄的是同一主题。
2. 总共有多少实例（如适用，按类型分）？共有 1100 万张图像。
3. 数据集包含所有可能的实例，还是来自更大集合的（未必随机的）样本？若是样本，更大的集合是什么？该样本能否代表更大集合（如地理覆盖）？若能，请描述如何验证/核实了这种代表性；若不能，请描述原因（如为覆盖更多样的实例范围，或因实例被保留或不可得）。数据集由从图片提供商处授权的图像组成，包含全部已授权实例。图像是照片而非艺术品，尽管有少数例外。数据集包含其中每张图像的所有生成掩码。我们保留了约 2k 张随机选取的图像用于测试。
4. 每个实例由什么数据构成？是「原始」数据（如未处理的文本或图像）还是特征？请提供描述。数据集中的每个实例是一张图像。图像经过处理以模糊人脸与牌照，保护图中人物的身份。
5. 每个实例是否有关联的标签或目标？请提供描述。每张图像标注了掩码。掩码没有关联的类别或文本。平均每张图像约 100 个掩码，总计约 11 亿个掩码。
6. 各实例是否缺失某些信息？请描述并解释缺失原因（如因不可得）。这不包括有意移除的信息，但可能包括如被遮盖的文本。是的。每张图像附带一段以自由格式文本描述照片内容与拍摄地点的简短说明。根据与图片提供商的协议，我们不能发布这些说明。但我们用它们在论文中分析了数据集的地理分布。
7. 各实例之间的关系是否显式给出（如用户的电影评分、社交网络链接）？请描述这些关系如何显式给出。否，数据集中实例间没有已知关系。
8. 数据集中是否存在错误、噪声来源或冗余？请提供描述。错误：掩码由分割模型生成，因此掩码中可能存在错误或不一致。冗余：虽然没有两张图像完全相同，但存在对同一主题在时间上相近拍摄的图像。
9. 数据集是自包含的，还是链接或依赖外部资源（如网站、推文、其他数据集）？若链接或依赖外部资源：a) 是否有保证它们随时间存在且保持不变；b) 是否有完整数据集的官方存档版本（即包含数据集创建时存在的外部资源）；c) 与任何外部资源相关的限制（如许可、费用）是否可能适用于数据集使用者？请酌情描述所有外部资源及相关限制，以及链接或其他访问入口。数据集是自包含的。
10. 数据集是否包含可能被视为机密的数据（如受法律特权或医患保密保护的数据，包含个人非公开通信内容的数据）？请提供描述。否。
11. 数据集是否包含直接查看时可能具有冒犯性、侮辱性、威胁性或可能引发焦虑的数据？请描述原因。我们有两项安全措施防止不良内容：(1) 照片从图片提供商处授权，且必须满足其服务条款。我们要求从授权图像中过滤所有不良内容。(2) 若用户在数据集中发现不良图像，我们邀请其向 [segment-anything@meta.com](mailto:segment-anything@meta.com) 报告以移除。尽管采取了这些措施，我们观察到少部分图像包含聚焦于多样宗教信仰或政治观点的抗议或其他集会场景，可能具有冒犯性。我们无法产出去除所有此类图像的过滤策略，依赖用户报告此类内容。
12. 数据集是否识别任何子群体（如按年龄、性别）？请描述如何识别这些子群体，并描述它们在数据集中的分布。数据集不识别照片中人物的任何子群体。
13. 是否可能直接或间接（即结合其他数据）从数据集中识别出个人（即一名或多名自然人）？请描述如何识别。否。图像经过人脸模糊模型处理以移除任何个人可识别信息。若用户发现任何匿名化问题，我们邀请其向 [segment-anything@meta.com](mailto:segment-anything@meta.com) 报告该问题及图像编号。
14. 数据集是否包含任何可能被视为敏感的数据（如揭示种族或族裔出身、性取向、宗教信仰、政治观点或工会成员身份、位置的数据；财务或健康数据；生物特征或基因数据；政府身份证件形式如社会安全号码；犯罪记录）？请提供描述。数据集包含抗议或可能暗示宗教信仰、政治观点或工会成员身份的其他集会场景。但数据集中所有人物的面部均已通过模糊匿名化，因此无法识别数据集中的任何个人。
15. 还有其他说明吗？无。

#### 收集过程

1. 与每个实例关联的数据如何获得？数据是直接可观察的（如原始文本、电影评分）、由受试者报告的（如调查回答），还是从其他数据间接推断/衍生（如词性标注、基于模型的年龄或语言猜测）？若由受试者报告或间接推断/衍生，数据是否经过验证/核实？请描述。与每张图像关联的已发布掩码由我们的分割模型 SAM 自动推断。通过模型辅助人工标注收集的掩码不会发布。质量验证方式如 §5 所述。
2. 使用了什么机制或流程收集数据（如硬件设备或传感器、人工筛选、软件程序、软件 API）？这些机制或流程如何验证？数据集中的图像从图像提供商授权。它们都是摄影师用不同相机拍摄的照片。
3. 若数据集是更大集合的样本，采样策略是什么（如确定性、以特定采样概率的概率采样）？我们保留了约 2k 张随机选取的图像用于测试。其余已授权图像均包含在数据集中。
4. 谁参与了数据收集过程（如学生、众包工作者、承包商），报酬如何（如众包工作者获得多少报酬）？已发布的掩码由 SAM 自动推断。模型辅助人工标注流程的细节见 §F.2 的数据标注卡。注意这些掩码不会发布。
5. 数据在什么时间段内收集？该时间段是否与实例关联数据的创建时间段一致（如近期抓取的旧新闻文章）？若不一致，请描述实例关联数据的创建时间段。已授权照片的拍摄日期跨越多年，直至 2022 年。
6. 是否进行了伦理审查（如机构审查委员会）？请描述审查流程及结果，并提供支持文档的链接或其他访问入口。若数据集不涉及人员，可跳过本节其余问题。我们进行了内部隐私审查，以评估并确定如何缓解照片中人物隐私方面的潜在风险。模糊人脸与牌照保护了照片中人物的隐私。
7. 您是直接从相关个人处收集数据，还是通过第三方或其他来源（如网站）获得？我们从第三方图片提供商处授权获得数据。
8. 相关个人是否被告知数据收集？若是，请描述（或以截图等方式展示）告知方式，并提供通知原文的链接或其他访问入口。图像从第三方授权，该方就向个人收集任何必要通知与同意提供了适当声明。此外，所有可识别信息（如人脸、牌照）均已模糊。数据集许可条款禁止尝试识别图像中的特定个人或将图像与特定个人关联。
9. 相关个人是否同意收集和使用其数据？若是，请描述（或以截图等方式展示）同意的请求与授予方式，并提供个人所同意内容的原文的链接或其他访问入口。图像从第三方授权，该方就向个人收集任何必要通知与同意提供了适当声明。此外，所有图像中的可识别信息（如人脸、牌照）均已模糊。为免生疑，数据集许可条款禁止尝试识别特定个人或将图像与特定个人关联。
10. 若已获得同意，是否为同意者提供了未来或针对特定用途撤销同意的机制？请提供描述及该机制的链接或其他访问入口（如适用）。我们邀请用户向 [segment-anything@meta.com](mailto:segment-anything@meta.com) 报告以移除图像。
11. 是否对数据集及其使用对数据主体的潜在影响做过分析（如数据保护影响分析）？请提供分析描述（包括结果）及支持文档的链接或其他访问入口。为消除照片被纳入数据集的人群受到的任何潜在影响，可识别信息（人脸、牌照）已被模糊。
12. 还有其他说明吗？无。

#### 预处理 / 清洗 / 标注

1. 是否对数据做过预处理/清洗/标注（如离散化或分桶、分词、词性标注、SIFT 特征提取、移除实例、缺失值处理）？请提供描述；若否，可跳过本节其余问题。我们将高分辨率授权图像调整为短边 1500 像素，且仅对图像做去除任何可识别与个人信息（人脸、牌照）的处理。
2. 除预处理/清洗/标注后的数据外，是否保存了「原始」数据（如为支持未来未预见的用途）？若是，请提供原始数据的链接或其他访问入口。否。出于安全与尊重隐私的原因我们移除了数据，不发布未修改的照片。
3. 用于预处理/清洗/标注的软件是否可用？若是，请提供链接或其他访问入口。我们使用 RetinaFace [[88](#bib.bib88), [89](#bib.bib89)] 模型（<https://github.com/serengil/retinaface>）检测人脸。用于模糊牌照的模型未公开。

#### 用途

1. 数据集是否已被用于任何任务？请提供描述。数据集被用于训练我们的分割模型 SAM。
2. 是否有链接到使用该数据集的论文或系统的仓库？若是，请提供链接或其他访问入口。否。但所有数据集使用者必须引用它，因此其使用情况可通过引用检索工具追踪。
3. 数据集还可以用于哪些（其他）任务？我们希望该数据集成为大规模分割数据集。同时，我们邀请研究社区为该数据集收集更多标注。
4. 数据集的构成或其收集与预处理/清洗/标注方式中，是否有会影响未来用途的因素？例如，数据集使用者是否需要了解某些情况，以避免可能导致对个人或群体不公平对待（如刻板印象、服务质量问题）或其他风险或危害（如法律风险、经济损失）的用途？请提供描述。数据集使用者能做些什么来缓解这些风险或危害？我们在 §6 中对数据集的近似地理与收入水平覆盖做了分析。虽然我们相信本数据集比目前大多数公开数据集更具代表性，但我们承认并未在所有群体间达到均等，我们鼓励使用者留意其模型用该数据集学到的潜在偏见。
5. 是否存在不应使用该数据集的任务？请提供描述。数据集的完整使用条款（含禁用场景）见 <https://ai.facebook.com/datasets/segment-anything>。
6. 还有其他说明吗？无。

#### 分发

1. 数据集是否会分发给创建它的实体（如公司、机构、组织）之外的第三方？请提供描述。数据集将向研究社区开放。
2. 数据集将如何分发（如网站上的压缩包、API、GitHub）？数据集是否有数字对象标识符（DOI）？数据集可在 <https://ai.facebook.com/datasets/segment-anything> 获取。
3. 数据集将于何时分发？数据集将于 2023 年发布。
4. 数据集是否在版权或其他知识产权（IP）许可和/或适用使用条款（ToU）下分发？请描述该许可和/或 ToU，并提供相关许可条款或 ToU 的链接或其他访问入口或原文，以及相关费用。是。数据集的许可协议与使用条款见 <https://ai.facebook.com/datasets/segment-anything>。用户在下载或使用数据集前必须同意使用条款。
5. 是否有第三方对与实例关联的数据施加了基于 IP 或其他限制？请描述这些限制，并提供相关许可条款的链接或其他访问入口或原文，以及相关费用。SA-1B 数据集的完整使用条款与使用限制见 <https://ai.facebook.com/datasets/segment-anything>。
6. 是否有出口管制或其他监管限制适用于数据集或单个实例？请描述这些限制，并提供支持文档的链接或其他访问入口。SA-1B 数据集的许可与使用限制见 <https://ai.facebook.com/datasets/segment-anything>。
7. 还有其他说明吗？无。

#### 维护

1. 谁将支持/托管/维护数据集？数据集将托管于 <https://ai.facebook.com/datasets/segment-anything>，由 Meta AI 维护。
2. 如何联系数据集的所有者/管理者（如电子邮件地址）？请发送邮件至 [segment-anything@meta.com](mailto:segment-anything@meta.com)。
3. 是否有勘误表？若有，请提供链接或其他访问入口。无。
4. 数据集是否会更新（如更正标注错误、添加新实例、删除实例）？请描述更新频率、执行者，以及如何通知数据集使用者（如邮件列表、GitHub）。为支持基于 SA-1B 的研究可复现性，唯一的更新是移除被报告的图像。
5. 若数据集涉及人员，对与实例关联的数据保留是否有适用限制（如是否告知相关个人其数据将保留固定时间后删除）？请描述这些限制及其执行方式。数据保留没有限制。我们已采取措施从任何人物图像中移除个人可识别信息。用户可向 [segment-anything@meta.com](mailto:segment-anything@meta.com) 报告内容以申请移除。
6. 数据集的旧版本是否会继续支持/托管/维护？若是，请描述方式；若否，请描述如何将其废弃告知数据集使用者。不会。由于唯一的更新是移除潜在有害内容，我们不会保留含这些内容的旧版本。
7. 若他人想扩展/增强/基于该数据集构建或为其做贡献，是否有相应机制？请提供描述。这些贡献是否会被验证/核实？如何验证？是否有向数据集使用者沟通/分发这些贡献的流程？我们鼓励用户为 SA-1B 收集更多标注。任何生成标注的用户需自行负责其标注的托管与分发。
8. 还有其他说明吗？无。

### F.2 数据标注卡

#### 任务表述

1. 从高层看，任务的主观性体现在哪里？分割图像中出现的物体本质上是一项主观任务。例如，一名标注者可能把两只靴子分割为一个掩码，而另一名可能把每只靴子分开分割。取决于标注者的技能，掩码质量与每张图像的掩码数量因人而异。尽管任务存在这些主观性，我们相信高效标注是可行的，因为数据以逐掩码方式标注，重点在于数据的多样性而非完备性。
2. 您对标注者做了哪些假设？我们的标注者全职从事我们的标注任务，流失率极低。这使我们能够通过定期反馈与答疑来培训标注者。具体而言：(1) 通过清晰传达本工作的目标并提供包括任务截图与录屏在内的明确指南，标注者有足够上下文来理解并合理执行任务。(2) 与标注者共享目标与关键结果并每周会面，提高了标注者随时间改进标注质量与数量的可能性。
3. 您如何选择任务指令的具体措辞？采取了哪些步骤来验证指令与措辞对标注者的清晰度？由于任务是图像标注，标注指南包含视觉示例。我们的研究团队完成了 30 个标注任务，以发现标注工具的明显难点，共同决定复杂案例的处理方式，并完善指南。研究团队每周与标注者举行反馈会。研究团队执行任务的录像与标注者实时共享，随后进行问答。标注者可以在反馈会上及异步地对不明确之处提出反馈。
4. 任务对标注者构成哪些风险（若有）？他们在参与任务前是否被告知风险？无已识别风险。图像在标注阶段之前已过滤不良内容。
5. 向标注者提供的精确指令是什么？我们仅提供高层指令：给定一张图像，我们目标是分割所有可能的物体。标注者为他们能识别的每个潜在物体生成掩码。可以用我们的交互式分割工具分割物体：通过校正性的前景/背景点击添加/移除掩码部分，或围绕物体绘制边界框。掩码可用像素级精确的工具细化。

#### 标注者选择

1. 是否有应当优先考虑的视角？若有，您如何寻求这些视角？我们选择与此前做过其他视觉标注任务的标注者合作。
2. 是否有纳入后可能有害的视角？若有，您如何筛除？无。
3. 是否使用了社会人口特征来为任务挑选标注者？请详述过程。否。
4. 若有关于标注者队伍的汇总社会人口统计信息，请描述。您是否有理由认为标注者的社会人口特征可能影响其数据标注方式？原因是什么？我们与 130 名标注者合作。标注者均位于肯尼亚。我们不认为标注者的社会人口特征对标注数据有实质性影响。
5. 请考虑数据集的预期使用场景，以及受在该数据集上训练的模型影响的个人与社区。这些社区是否在您的标注者队伍中有代表？Segment Anything 1B（SA-1B）数据集仅用于研究目的。如 §6 所讨论，SA-1B 是地理最多样化的分割数据集之一。此外，我们在 §6 中分析了在该数据集上训练的模型的负责任 AI 维度。

#### 平台与基础设施选择

1. 您使用了什么标注平台？高层来看，哪些考虑促成了您对该平台的选择？所选平台是否充分满足您对标注者队伍的要求？是否有未覆盖的方面？我们使用专有标注平台。
2. 您选择的平台提供了哪些（若有）与标注者沟通的渠道？该沟通渠道如何影响标注过程和/或最终标注？我们人工审查标注，并每周与标注者分享反馈。我们沟通常见错误或不一致及相应更正。此外，标注 QA 团队每天向标注者提供改进反馈。每周反馈会之外，标注者可通过电子表格与聊天群与研究团队沟通。这一流程极大提升了标注的平均速度与质量。
3. 标注者获得多少报酬？在确定报酬时是否考虑了特定薪酬标准？请描述。标注者按供应商设定的时薪获得报酬。该供应商是一家认证的 B 型企业（Certified B Corporation）。

#### 数据集分析与评估

1. 您在您的场景中如何定义标注质量，如何评估所构建数据集的质量？标注者先进入培训。他们参加供应商主导的 1 天培训，然后被要求标注训练队列中的大量示例。当供应商 QA 团队与研究团队协作人工抽检标注者的掩码确保质量后，标注者从培训转入生产。平均而言，标注者在毕业前接受一周培训。生产质量评估遵循类似流程：供应商 QA 团队与研究团队每周人工审查标注，并每周分享反馈。
2. 您是否对分歧模式做过分析？使用了什么分析，主要发现是什么？是否分析了分歧的潜在来源？我们在与标注者的每周会议上指出常见错误。
3. 单个标注者的回应与数据集最终发布的标签有何关系？这些标注仅用于训练早期版本的 SAM 模型，我们目前不计划发布它们。

#### 数据集发布与维护

1. 您是否有理由认为该数据集中的标注可能随时间变化？是否计划更新数据集？没有，除非移除不良图像。
2. 是否有若发生变化会影响数据集效用的条件或定义？我们认为没有。
3. 您是否会尝试跟踪、限制或以其他方式影响数据集的使用方式？如何实施？SA-1B 数据集将在许可协议下发布，允许特定研究用途并为研究人员提供保护。研究人员必须同意许可协议条款才能访问数据集。
4. 标注者是否被告知数据如何对外发布？若数据集发生变化，是否会通知他们？否，我们目前不计划发布人工标注。
5. 是否存在标注者日后选择撤回其在数据集中数据的流程？请详述。无。

|  |  |
| --- | --- |
| 模型概览 | |
| 名称 | SAM 或 Segment Anything Model |
| 版本 | 1.0 |
| 日期 | 2023 |
| 组织 | Meta AI 的 FAIR 团队 |
| 模型类型 | 可提示分割模型 |
| 架构 | 见 §3 |
| 代码仓库 | <https://github.com/facebookresearch/segment-anything> |
| 引用 | <https://research.facebook.com/publications/segment-anything> |
| 许可证 | Apache 2.0 |
| 预期用途 | |
| 主要预期用途 | SAM 可用于任何基于提示的分割任务。我们探索了其在以下任务中的使用：从单点分割物体（§7.1）、边缘检测（§7.2）、分割所有物体（§7.3）与分割检测到的物体（§7.4）。我们还探索了 SAM 如何与其他视觉模型集成以从文本分割物体（§7.5）。 |
| 主要预期用户 | SAM 主要为研究而开发。SAM 的许可证见 <https://github.com/facebookresearch/segment-anything>。 |
| 超出范围的使用场景 | 见 <https://github.com/facebookresearch/segment-anything> 上 SAM 的使用条款。另见「伦理考量」下的用例部分。 |
| 注意事项与建议 | SAM 在广泛任务上具有令人印象深刻的零样本性能。但我们注意到，在零样本设置下，给定输入可能有多个有效的真值掩码。我们建议用户在将 SAM 用于零样本分割时考虑这一点。SAM 可能遗漏精细结构，也可能幻觉出细小的不连通成分。局限性讨论见 §8。 |
| 相关因素 | |
| 群体 | SAM 被设计为可分割任何物体，包括 stuff（材料类）与 things（物体类）。 |
| 工具与环境 | 我们在多样化数据集上对 SAM 做了基准测试，发现 SAM 能处理多种视觉数据，包括仿真、绘画、水下图像、显微镜图像、驾驶数据、立体图像、鱼眼图像。所用基准信息见附录 D.1 与表 7。 |
| 指标 | |
| 模型性能度量 | 我们在实验中按下游任务用多种指标评估 SAM。• mIoU：我们用给定提示数量后的平均交并比评估以点提示时掩码的分割质量。• 人工评估：我们进行了人工研究（详见附录 E）以评估 SAM 的真实世界表现。我们用 1 到 10 的感知质量量表，将 SAM 生成的掩码与基线最先进交互式分割模型 RITM [[92](#bib.bib92)] 比较。• AP：我们用平均精度评估给定框的实例分割与边缘检测。• AR@1000：我们用平均召回率评估物体候选框生成。• ODS、OIS、AP、R50：我们使用 BSDS500 [[72](#bib.bib72), [3](#bib.bib3)] 的标准边缘检测评估指标。 |
| 评估数据 | |
| 数据来源 | 见附录 D.1。 |
| 训练数据 | |
| 数据来源 | 见 §F.1 的数据集卡。 |
| 伦理考量 | |
| 数据 | 我们在授权图像上训练 SAM。图像已经提供商过滤不良内容，但我们承认可能存在漏网之鱼。我们在 §6 中对 SA-1B 数据集做了地理分析。虽然 SA-1B 在地理上比许多以往数据集更多样，我们承认某些地理区域与经济群体代表性不足。 |
| 算力成本与影响 | SAM 在 256 块 A100 GPU 上训练 68 小时。我们承认训练大规模模型的环境影响与成本。使用 [[77](#bib.bib77)] 描述的计算方法与 ML CO2 Impact 计算器 [[61](#bib.bib61)]，针对所用的特定数据中心，已发布 SAM 模型训练的环境影响约为 6963 kWh，估计产生 2.8 公吨二氧化碳。这大致相当于美国普通燃油乘用车行驶约 7000 英里 [[101](#bib.bib101)]。我们发布 SAM 模型，以减少重训需求并降低大规模视觉研究的门槛。 |
| 风险与危害 | 我们在 §6 中评估了 SAM 的公平性。SAM 的下游用例将产生各自的偏见与公平性隐患。因此我们建议用户在其具体用例中使用 SAM 时自行开展公平性评估。 |
| 用例 | 我们恳请用户对模型的下游使用做出最佳判断。 |

表 9：SAM 的模型卡，遵循 [[75](#bib.bib75)] 详述的流程。

我们有多个模型，当输入一次点击或一个框时输出一个掩码。我们希望通过在大量示例上为这些模型的掩码质量评分来比较它们的质量。界面与常规掩码标注不同。

- 每个任务评审一张图像中的一个掩码。
- 右侧将有两行共五张图像缩略图。鼠标悬停可在每张缩略图上以更大尺寸显示图像。点击缩略图可全屏显示，再次点击返回原画面。

  - 图像以五种不同视图展示同一掩码。上排：（左）不带掩码的图像、（中）掩码叠加在图像上、（右）仅掩码。下排：（左）物体的放大视图（不带掩码）、（右）掩码叠加在图像上的放大视图。提供这些视图是为了便于看到不同类型的掩码错误。
  - 掩码叠加在图像上时为红色。
  - 单独显示时，掩码为黄色，背景为紫色。
  - 每张图像上会有一个蓝点或一个蓝白框。这是模型的输入，如同你在此位置点击过或画过这个框。
- 左侧有标有 1-10 的按钮，用于为所示掩码的质量评分。

目标与设置

![](2304.02643v1/figs/annotator_guidelines/im1.jpg)

界面示例页。右侧有五张图像，左侧有一个问题框。

![](2304.02643v1/figs/annotator_guidelines/im2.jpg)

鼠标悬停在图像上可显示完整图像。

![](2304.02643v1/figs/annotator_guidelines/im3.jpg)

点击图像可全屏显示。箭头可在图像间切换。再次点击返回先前视图。

![](2304.02643v1/figs/annotator_guidelines/im4.jpg)

上排第一张图显示不带掩码的图像。感兴趣的物体上会有一个蓝点，或周围有一个蓝白框。

![](2304.02643v1/figs/annotator_guidelines/im5.jpg)

上排第二张图以红色显示物体的掩码。

![](2304.02643v1/figs/annotator_guidelines/im6.jpg)

上排第三张图仅显示掩码。掩码为黄色，背景为紫色。

![](2304.02643v1/figs/annotator_guidelines/im7.jpg)

下排第一张图显示不带掩码的物体放大视图。

![](2304.02643v1/figs/annotator_guidelines/im8.jpg)

下排第二张图显示带掩码的物体放大视图。掩码为红色。

![](2304.02643v1/figs/annotator_guidelines/im9.jpg)

左侧是掩码质量评分按钮，可选 1-10。

我们希望你对每个任务做的事情：

- 请力争每个任务花费不超过 30 秒。
- 鼠标悬停或点击右侧三张掩码图像，以了解掩码质量。缩略图太小，不足以评判掩码，不要仅凭缩略图评判。每张图像可提供关于潜在掩码错误的不同信号：

  - 未放大的图像可给出掩码的上下文：该掩码是否对应真实物体？
  - 仅掩码的图像可显示掩码是否有小孔或分离的错误像素。
  - 放大的图像可显示掩码边界是否合理。
- 按三条标准评判掩码质量。示例随后。

  - 掩码是否对应真实物体？
  - 掩码是否有良好边界？
  - 掩码是否与给定的点或框对应？
- 用左侧的下拉框按 1-10 为掩码质量评分。
- 接下来是按三条标准评判掩码质量的细节与示例。这些只是示例，可能出现其他情况，判断某个掩码是否良好时请运用你的最佳判断。

任务

掩码是否对应真实物体？

- 有效物体可包括：

  - 完整的单个物体（如一个人、一件衬衫或一棵树）
  - 物体的合理部分（椅子腿、车门、桌面）
  - 物体的集合（一摞书、一群人）
  - 「stuff」（地面、天空）。
- 掩码可能存在的错误示例。这些错误的严重程度可轻可重：

  - 包含另一物体的一部分（一个人的掩码包含了旁边人的手臂）
  - 遗漏物体的一部分（掩码只覆盖被前景树木遮挡的建筑的一部分）
  - 合并两个不相关的事物（一个掩码同时覆盖桌上的马克杯和笔）
  - 对点输入包含集合的任意一部分（点在某一个苹果上，但掩码覆盖了一大堆苹果中的三个）。若框围住的是一个任意集合，为这些物体给出掩码不算错误。
- 若你不确定，一个好的经验法则是：你能说出所涉物体的名字吗？不过，一些难以命名的事物仍可能是好物体（机器上的一个不常见部件、图像边缘难以判断为何物的东西）。

评判掩码质量（1/3）

掩码是否有良好边界？

- 边界错误可包括：

  - 掩码中不正确的孔洞
  - 与掩码主体分离的错误像素
  - 边缘质量差，即掩码与物体边缘不完全吻合。
  - 未能一致地处理遮挡的前景物体（覆盖遮挡物的掩码可以，不覆盖遮挡物的掩码也可以，但一部分覆盖一部分不覆盖就有错误）
  - 小掩码的像素化不算错误，只要掩码仍与物体边缘吻合。

评判掩码质量（2/3）

掩码是否与给定的点或框对应？

- 对于点：

  - 点必须在掩码上。
  - 物体相对于点的大小或位置无关紧要（某人戴手套的手上的点可以对应手套，也可以对应整个人，两者都是有效掩码）。
- 对于框：

  - 物体必须是尺寸与框相当的最佳物体（若框围住某人的整个头部，而掩码是其头发，这是错误：头发在框内但不是正确物体）。
  - 若框明显对应某个物体但略小于它，掩码略微超出框是可以的（若围住一个人的框漏掉了其伸出的手，掩码仍可包含手，即使掩码超出框）。

评判掩码质量（3/3）

![](2304.02643v1/figs/annotator_guidelines/im10.jpg)

「包含另一物体的一部分」的错误示例：大象掩码包含了附近另一头大象的一部分。

![](2304.02643v1/figs/annotator_guidelines/im11.jpg)![](2304.02643v1/figs/annotator_guidelines/im12.jpg)

「遗漏物体一部分」的错误示例：掩码遗漏了物体不连通的一部分：斑马的后半部分，以及盘子的右部。

![](2304.02643v1/figs/annotator_guidelines/im13.jpg)![](2304.02643v1/figs/annotator_guidelines/im14.jpg)

「包含集合的任意一部分」的错误示例：在上图中，点在一个橘子上，但掩码覆盖了两个橘子。这是掩码错误：掩码覆盖了集合中任意数量的物体，应当要么覆盖一个橘子，要么全部覆盖。在下图中，框围住了两个蔬菜。由于这是与框的最佳匹配，这不算掩码错误。

![](2304.02643v1/figs/annotator_guidelines/im15.jpg)

「掩码中不正确的孔洞」错误示例：该掩码在左上及左侧有孔洞（黑色箭头）。这些孔洞在「仅掩码」图像上更容易看到。

![](2304.02643v1/figs/annotator_guidelines/im16.jpg)

「包含与掩码主体分离的错误像素」错误示例：「仅掩码」视图揭示了钟面上几个零散的错误像素。

![](2304.02643v1/figs/annotator_guidelines/im17.jpg)

「边缘质量差」错误示例：该掩码边缘质量差，沿伞的边缘及细伞杆处均是。

图 19：这里我们提供为掩码质量人工评审给标注者的完整指南。部分图像略有编辑且人脸已模糊以便发布。建议放大查看（第 1 部分，共 2 部分）。

## 附录 G 标注指南

我们在图 19 与图 20 中提供为掩码质量人工评审给标注者的完整指南。

![](2304.02643v1/figs/annotator_guidelines/im18.jpg)

「合并两个不相关事物」示例：点指示的是蜥蜴，但掩码同时覆盖了蜥蜴和一只鸟。这是掩码错误。

![](2304.02643v1/figs/annotator_guidelines/im19.jpg)

「未能一致地处理遮挡的前景物体」错误示例：右侧的杆（蓝色箭头）被排除在掩码外，而左侧的杆被包含在物体中（黑色箭头）。掩码应当同时包含或同时排除这两者。

![](2304.02643v1/figs/annotator_guidelines/im20.jpg)

「小掩码像素化」示例：该掩码边界不完美，因为在黑色箭头处超出了物体。但掩码的「块状」图案不是错误，因为放大到这种程度时，图像同样呈块状。

![](2304.02643v1/figs/annotator_guidelines/im21.jpg)

与给定点不一致的错误示例：掩码与蓝点不一致，因此这是掩码错误。

![](2304.02643v1/figs/annotator_guidelines/im22.jpg)

与给定点一致的示例：对该输入点，标志（左）与容器（右）都是有效物体，因为蓝点同时位于两者之上。两个掩码都没有错误。

![](2304.02643v1/figs/annotator_guidelines/im23.jpg)

与框一致的示例：框围住的是一碗橘子，但掩码只是单个橘子。这是掩码错误。

![](2304.02643v1/figs/annotator_guidelines/im24.jpg)

与框一致的示例：框的形状贴合斑马。即使掩码略微超出框以包含斑马的左腿，这也不是错误。

总体掩码质量是主观的，上述每种错误对掩码质量的损害可大可小，取决于错误大小。选择掩码分数时请运用最佳判断，并尽量在掩码之间保持一致。以下是不同分数应对应的一般指南：

- 1 分：无法判断该掩码对应什么物体。包括完全看不到掩码的情况。
- 低分（2-4）：物体大体可辨认，但掩码质量极差（如掩码大块区域覆盖其他物体；物体大块区域缺失；斑驳不堪的掩码边界切穿物体中部）。
- 中等分数（5-6）：物体可辨认且边界大体正确，但存在重大错误（遗漏物体显著的不连通部分；包含另一物体的显著部分；物体某一区域边界质量很差但并非整个物体）。
- 高分（7-9）：物体可辨认，错误小且罕见（遗漏一个小的、被严重遮挡的不连通成分；掩码边界与物体边界不完全吻合的小块区域）。
- 10 分：掩码像素级完美；完全无可辨认错误。

掩码评分

![](2304.02643v1/figs/annotator_guidelines/im25.jpg)

1 分掩码示例：不清楚该掩码对应什么物体。

![](2304.02643v1/figs/annotator_guidelines/im26.jpg)

低分（2-4）掩码示例：主要物体可辨认，但掩码包含了另一物体的大块错误部分。

![](2304.02643v1/figs/annotator_guidelines/im27.jpg)

低分（2-4）掩码示例：主要物体可辨认，但物体的一大块随机部分缺失。

![](2304.02643v1/figs/annotator_guidelines/im28.jpg)

中低分（4-5）掩码示例：物体可辨认且边缘全部正确，但掩码错误地包含了左侧人物的手。

![](2304.02643v1/figs/annotator_guidelines/im29.jpg)

中等分数（5-6）掩码示例：掩码明显对应盘子，但与华夫饼的边界相当差。

![](2304.02643v1/figs/annotator_guidelines/im30.jpg)

中等分数（5-6）掩码示例：物体易于辨认，大多数边缘合理。但存在显著的不连通部分（画框内的手臂）大部分缺失，且该区域有斑驳像素。

![](2304.02643v1/figs/annotator_guidelines/im31.jpg)

中高分（6-8）掩码示例：掩码有两小块边界较差的区域，位于掩码顶部与右下。

![](2304.02643v1/figs/annotator_guidelines/im16.jpg)

中高分（6-8）掩码示例：花环是与框尺寸相当的有效物体（整个花环 + 时钟也是有效物体）。但钟面上有不正确的零散掩码像素。

![](2304.02643v1/figs/annotator_guidelines/im32.jpg)

高分（7-9）掩码示例：马的边界几乎完全正确，仅其后腿右侧除外。掩码一致地包含了马佩戴的全部马具，边界合理。

![](2304.02643v1/figs/annotator_guidelines/im33.jpg)

极高分（约 9）掩码示例：仅在掩码边缘附近有轻微错误。块状「像素化」不是错误，因为图像在该尺度下同样是块状的。

![](2304.02643v1/figs/annotator_guidelines/im34.jpg)

极高分（9-10）掩码示例：掩码仅在右下边缘有极轻微错误。

![](2304.02643v1/figs/annotator_guidelines/im35.jpg)

极高分（9-10）掩码示例：仅在掩码边缘附近有轻微错误。

图 20：这里我们提供为掩码质量人工评审给标注者的完整指南。部分图像略有编辑且人脸已模糊以便发布。建议放大查看（第 2 部分，共 2 部分）。
