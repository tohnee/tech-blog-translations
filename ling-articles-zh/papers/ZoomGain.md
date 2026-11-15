---
title: "ZoomGain：挖掘全局-拉近感知差以实现细粒度视觉监督"
title_en: "ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"
arxiv: 2611.14076
date: 2026-11-09
source: https://arxiv.org/abs/2611.14076
project: https://github.com/inclusionAI/ZoomGain
crawled: 2026-11-16
translated: 2026-11-16
---
# ZoomGain：挖掘全局-拉近感知差以实现细粒度视觉监督

> 原文：[ZoomGain](https://arxiv.org/abs/2611.14076) · InclusionAI · arXiv

## 摘要

细粒度视觉感知要求视觉语言模型（VLM）在复杂场景中定位并解读细微证据。为这一能力构建监督信号颇具挑战：问题必须具有正确、无歧义的答案，且答案应依赖真实的细粒度视觉细节，而非粗粒度线索或语言先验。验证这些性质使人工标注成为劳动密集型工作，也使自动生成对本身就在细粒度感知上吃力的模型而言困难重重。然而，一旦把区域拉近，这些模型往往又能识别出此类细节。我们利用这一全局-拉近感知差（global-to-zoom perception gap），提出 ZoomGain——一条数据构建流程：仅凭拉近后获得的视觉信息，构造关于整幅图像的问题。该流程用多个模型在拉近视图上验证每个答案，确保每个问题在整幅图像中仍然无歧义、且无法仅凭语言先验作答，并专门为多项选择题生成高质量干扰项。借助该流程与纯人工筛选（不做人工 QA 编辑），我们构建了 ZoomGainBench——一个包含 1,000 道题的双语基准；在该基准上，28 个 VLM 中的最佳者仅得 61.08 分。失败分析表明，模型在多项选择题答错时偏好某一类特定干扰项。除评测之外，仅用 9K 条 ZoomGain 样本训练，就显著提升了我们 4B/9B 模型的视觉感知能力，使其在多个感知基准上超越若干千亿参数级模型。训练后的 9B 模型在若干基准上取得 SoTA 性能，例如在 HR-Bench 4K 上达到 90.25。这些结果表明，全局-拉近感知差为在评测与训练中规模化构建细粒度视觉监督提供了实用基础。代码见[此处](https://github.com/inclusionAI/ZoomGain)。

†脚注：\*本文工作完成于在蚂蚁集团的实习期间。

†通讯作者：Jun Lan（[yelan.lj@antgroup.com](mailto:yelan.lj@antgroup.com)）与 Tiancheng Zhao（[tianchez@zju-bj.com](mailto:tianchez@zju-bj.com)）。

## 1 引言

![Refer to caption](2611.14076v1/zoomgain_overview_v8.png)

图 1：ZoomGain：把全局-拉近感知差转化为细粒度视觉监督。(a) 跑者的鞋子颜色在全局视图中不清晰，但在拉近视图中可辨；ZoomGain 在整幅图像中询问此类细节，并使用全局指代表达式来标识目标。成对视图 $V_{g}^{i}$ 与 $V_{z}^{i}$，以及指代表达式 $e_{i}$，定义于[第 3.2 节](#S3.SS2)。(b) ZoomGainBench 由人工筛选获得、未经 QA 编辑，令全部 28 个受评 VLM 都面临挑战。(c) 在 9K 训练 QA 对上做 RLVR，使 Qwen3.5-4B 与 Qwen3.5-9B 相对各自基座模型以及 ZwZ 训练的对应模型均有提升（ICML'26 [Wei et al. (2026)](#bib.bib1)）。

细粒度视觉感知在许多实际应用中至关重要：从在航拍图像中检测小型车辆（[Xia et al. (2018)](#bib.bib50)）、在工业质检中识别细微缺陷（[Bergmann et al. (2019)](#bib.bib51)），到为视障人士读取商品标签（[Gurari et al. (2018)](#bib.bib52)）。用视觉语言模型（VLM）（[Team (2026)](#bib.bib2)；[Bai et al. (2025)](#bib.bib5)；[Zhu et al. (2025)](#bib.bib53)；[Liu et al. (2023)](#bib.bib54)）处理这类任务，需要定位并解读整幅图像中容易被忽略的细小细节。要开发和基准评测这类细粒度能力，高质量监督必不可少：答案必须正确且无歧义，问题必须真正依赖细粒度视觉证据。

大规模构建此类监督颇具挑战。人工标注是劳动密集型工作，因为标注者必须逐一检查小区域并验证上述每项性质。自动生成（[Wang et al. (2025a)](#bib.bib24)；[Wei et al. (2026)](#bib.bib1)）面临相关困难：用于生成问题的模型本身可能就难以感知整幅图像中的相关细节。结果，它们可能产出错误答案、有歧义的指代，或实际上并不需要细粒度感知的问题。由此，关键挑战在于：对那些模型在完整场景中无法感知的视觉细节，获得可靠的监督。

拉近（zooming in）长期以来被用于恢复此类细节：或在推理阶段通过视觉搜索（[Wu and Xie (2023)](#bib.bib21)；[Lai et al. (2025)](#bib.bib23)；[Shen et al. (2025)](#bib.bib55)）与带裁剪工具的智能体 VLM（[Zheng et al. (2026)](#bib.bib26)；[Hong et al. (2026)](#bib.bib27)），或在训练阶段通过区域到图像的蒸馏（[Wei et al. (2026)](#bib.bib1)；[Yuan et al. (2026)](#bib.bib30)），因为模型在整幅图像中无法分辨的细节，一旦把区域拉近往往就变得可识别。我们则专门利用这一全局-拉近感知差来构造监督本身（[图 1](#S1.F1)(a)）：对比两种视图，可以定位在整幅图像中难以感知的细节。

基于这一思路，我们提出 ZoomGain——一条自动化数据构建流程，把*只有*通过拉近才能获得的视觉信息，转化为关于整幅图像的有挑战性问题（贡献 #1）。ZoomGain：(1) 仅从拉近视图中描述、但在整幅图像描述中不清晰或缺失的细节出发构建问题，使回答必须依赖该细节本身；(2) 只有当多个模型在拉近视图上对答案一致时才保留答案，并丢弃全局指代有歧义、或无需图像即可回答的问题；(3) 生成多种可能误导被查询 VLM 的多项选择干扰项。

借助 ZoomGain，我们整理了 ZoomGainBench——一个包含 1,000 道题的双语基准，覆盖属性识别、计数与 OCR，其问题与答案完全由模型撰写：两名人工审核者只负责接受/拒绝候选（贡献 #2）。在 28 个受评 VLM 中，最佳模型 GPT-5.6-Sol 仅得 61.08 分，只有五个模型超过 50 分（[图 1](#S1.F1)(b)）。错误分析进一步表明，错误选项集中在构建过程中从全局视图的错误预测中挖掘出的干扰项上（[第 3.3 节](#S3.SS3)）。这说明当细节无法分辨时，模型倾向于用场景上合理的相似猜测填补信息缺口，表明全局-拉近感知差是当前 VLM 的普遍弱点，而非特定模型的问题。

除评测之外，ZoomGain 数据还可作为有效的训练监督（贡献 #3）。在源图像与训练设置完全相同的情况下，我们用 9K 条 ZoomGain 与 ZwZ（ICML'26 [Wei et al. (2026)](#bib.bib1)）QA 对分别训练 Qwen3.5-4B 与 Qwen3.5-9B（[Team (2026)](#bib.bib2)）。ZoomGain 训练的模型在全部 14 个受评基准上一致优于 ZwZ（[图 1](#S1.F1)(c)）。增益不仅限于细粒度感知，还扩展到通用感知以及困难的感知-推理任务，例如 9B 模型在 O3-Bench（[Li et al. (2026a)](#bib.bib36)）上提升 11.01 分。值得注意的是，我们微调后的 9B 模型与 GLM-5.3-Flash（[GLM-5-Team et al. (2026)](#bib.bib3)）相当，4B 模型则超过 Qwen3.5-122B-A10B。消融表明，移除增量证据或多源干扰项中的任一项都会显著降低这些增益，证实这两个植根于全局-拉近感知差的设计都不可或缺。

## 2 相关工作

#### 细粒度感知基准。

已有多种基准专门评测高分辨率图像中的细粒度感知，包括 [Wu and Xie (2023)](#bib.bib21)；[Wang et al. (2025b)](#bib.bib22)；[Zhang et al. (2024)](#bib.bib38)；[Wang et al. (2025a)](#bib.bib24)；[Gavrikov et al. (2026)](#bib.bib56)；[Lai et al. (2025)](#bib.bib23)；[Zhang et al. (2026b)](#bib.bib25)；[Wei et al. (2026)](#bib.bib1)；O3-Bench（[Li et al. (2026a)](#bib.bib36)）进一步要求感知之外的多步推理。然而，这些基准中的问题通常由人工标注，或由模型生成后经大量人工编辑（[表 1](#S4.T1)），使规模化整理的成本高昂。此外，现有基准很少过滤语言先验捷径（[Cadene et al. (2019)](#bib.bib45)；[Chen et al. (2024)](#bib.bib32)；[Yue et al. (2025)](#bib.bib46)），也很少设计有针对性的干扰项。相比之下，ZoomGain 通过拉近视图验证、盲捷径过滤以及从模型错误中挖掘干扰项，完全自动化了 QA 撰写。

#### 提升细粒度感知。

拉近已被广泛用于增强细粒度感知：或在推理阶段通过视觉搜索（[Wu and Xie (2023)](#bib.bib21)；[Shen et al. (2025)](#bib.bib55)；[Lai et al. (2025)](#bib.bib23)；[Li et al. (2026a)](#bib.bib36)；[Wang et al. ()](#bib.bib57)）与智能体裁剪工具（[Zheng et al. (2026)](#bib.bib26)；[Hong et al. (2026)](#bib.bib27)；[Su et al. (2026)](#bib.bib28)；[Zhang et al. (2025)](#bib.bib29)），或在训练阶段通过拉近到全局的蒸馏（[Wei et al. (2026)](#bib.bib1)；[Yuan et al. (2026)](#bib.bib30)；[Li et al. (2026b)](#bib.bib58)；[Zhang et al. (2026a)](#bib.bib59)）。与关注推理流程或训练目标的先前工作不同，ZoomGain 直接面向数据构建本身：它利用全局-拉近感知差来确定问什么（严格基于拉近后才显现的细节），并可靠地验证真值，因此与现有方法互补。

## 3 ZoomGain 数据构建流程

ZoomGain 利用全局视图与拉近视图之间的感知差：在整幅图像中难以分辨的细粒度细节，一旦把目标区域拉近就可能变得清晰。如[图 2](#S3.F2)所示，ZoomGain 首先发现并定位目标锚点（[第 3.1 节](#S3.SS1)），然后基于拉近后新显现的细节构造问题与答案（[第 3.2 节](#S3.SS2)），最后验证答案可靠性与视觉依赖性，并构建能够捕捉模型合理错误的多源干扰项（[第 3.3 节](#S3.SS3)）。完整算法与更多实现细节见[附录 A](#A1)。

![Refer to caption](2611.14076v1/zoomgain_pipeline_v5.png)

图 2：ZoomGain 总览。(a) 通过独立定位发现锚点并获得一致区域。(b) 从成对视图中挖掘全局到拉近的增量证据，以构造问题与参考答案。(c) 验证答案与视觉依赖性，然后组装并复查带多源干扰项的多项选择题。

### 3.1 锚点发现与定位

给定输入图像（记为全局视图 $V_{g}$），我们首先用 VLM 生成全局场景描述 $C_{g}$。随后，一个纯文本 LLM 以 $C_{g}$ 作为唯一输入，提出一组候选锚点。每个锚点 $i$ 由一个指代表达式 $e_{i}$ 表示，用来描述目标的外观、空间位置或与其他物体的关系。为确保 $e_{i}$ 能在整幅图像中无歧义地标识一个可定位实例，三个 VLM 独立地在 $V_{g}$ 中定位 $e_{i}$。仅当每个模型都恰好返回一个有效边界框，且所有两两框的 IoU 都不低于 $0.5$ 时，我们才保留 $e_{i}$——缺失框或多个框意味着找不到指称对象或其指代可能有歧义；IoU 条件则提供跨模型证据，表明 $e_{i}$ 指向一致区域。对每个保留的锚点，我们取各预测框的逐坐标中位数，并扩展所得区域以纳入更多周边上下文，得到裁剪框 $b_{i}$；再用 $b_{i}$ 裁剪 $V_{g}$，得到拉近视图 $V_{z}^{i}$。四元组 $(V_{g}, V_{z}^{i}, b_{i}, e_{i})$ 作为后续问题构建阶段的输入。

### 3.2 全局到拉近的证据与 QA 构建

对每个保留的锚点 $i$，我们用一个强 VLM $M_{\mathrm{cap}}$ 从两种视图描述目标区域。具体而言，我们在 $V_{g}$ 中于 $b_{i}$ 处画一个红色边界框，得到带标注的全局视图 $V_{g}^{i}$。[图 1](#S1.F1)(a) 展示了成对视图 $(V_{g}^{i}, V_{z}^{i})$。我们把 $V_{g}^{i}$ 输入 $M_{\mathrm{cap}}$，提示它尽可能详细地*只*描述红框内的内容，得到全局视图描述 $C_{g}^{i}$。在另一次独立调用中，我们提供拉近视图 $V_{z}^{i}$，请求详细的描述 $C_{z}^{i}$。这样便得到同一区域 $b_{i}$ 在不同观察尺度下的两份描述。然后，我们用 LLM 比较 $C_{g}^{i}$ 与 $C_{z}^{i}$，抽取那些在 $C_{z}^{i}$ 中被明确描述、但在 $C_{g}^{i}$ 中仍不清晰或未提及的细节。这些细节构成候选事实集合 $\Delta_{i}$。例如，在[图 2](#S3.F2)(b) 中，跑者的鞋子颜色在全局视图描述中不清晰，而在拉近视图描述中被识别为红色，因此成为 $\Delta_{i}$ 中的一条候选事实。

我们生成三类问题：属性识别、文本识别（OCR）与计数。LLM 从 $\Delta_{i}$ 中选择一条能支持确定答案的事实，并据此生成局部问题 $q_{\mathrm{local}}^{i}$ 与参考答案 $a_{i}$。局部问题面向拉近视图措辞，使用诸如「这名跑者」的简单指代，而不指定目标在整幅图像中的位置。随后，LLM 把该指代替换为全局指代表达式 $e_{i}$，并调整措辞以生成全局视图问题 $q_{\mathrm{global}}^{i}$，同时保持所问细节与参考答案不变，使关于拉近后才显现的细节的问题能在整幅图像中清楚地标识目标。例如，「跑者的鞋面是什么颜色？」会变成「右侧黄线上穿深色上衣的跑者，其鞋面是什么颜色？」[附录 H](#A8)用属性、计数与 OCR 示例说明了这一构建过程。

### 3.3 质量验证与多源干扰项

我们以两种方式验证每个候选 QA 对。(1) *基于裁剪的验证*：向若干 VLM 提供 $q_{\mathrm{local}}^{i}$ 与拉近视图 $V_{z}^{i}$，并从每个模型采样多个答案。仅当所有模型在其采样答案上都达到预定义准确率阈值时，才保留该 QA 对。检查多个模型基于拉近视图作答的一致性，有助于确保答案正确，从而避免在答案标注上仅依赖单一模型的描述——后者可能包含幻觉（[Rohrbach et al. (2018)](#bib.bib47)；[Li et al. (2023)](#bib.bib48)；[Jing et al. (2024)](#bib.bib49)）。(2) *盲验证*：要求模型在无图像的情况下回答 $q_{\mathrm{global}}^{i}$。若所有盲答模型都超过规定的正确答案阈值，则丢弃该 QA。这一步有效滤除了可仅凭语言先验、而非真实图像内容回答的问题（[Cadene et al. (2019)](#bib.bib45)；[Chen et al. (2024)](#bib.bib32)；[Yue et al. (2025)](#bib.bib46)）。

对于适合多项选择评测的已验证 QA 对，我们从三个互补来源构建干扰项。(1) *视觉证据*从图像内容中提供貌似合理的替代项，例如[图 2](#S3.F2)(c) 中另一名跑者的荧光绿鞋子，可暴露目标选择或属性绑定上的错误。(2) *盲猜*提供无图像情况下产生的错误答案，捕捉语言先验。(3) *全局视图错误*提供从整幅图像产生的错误答案，捕捉局部细节难以分辨时的混淆。我们移除与参考答案等价、或对该问题同样有效的候选，合并语义冗余的候选，并规范其措辞，形成互不相同的选项。

我们把参考答案与选定的干扰项组合起来，并用拉近视图复查所得 MCQ。这一最终检查检验在引入竞争选项后，参考答案是否仍可被可靠区分。若未达到逐模型的一致性阈值，我们替换或移除有问题的干扰项。OCR 与计数问题保留开放式格式，跳过干扰项构建与 MCQ 复查。[附录 I](#A9)给出了被基于裁剪的验证与盲验证拒绝的候选 QA 对示例。

## 4 实现细节与数据准备

#### 模型角色与验证设置。

我们使用 Qwen3.5-397B-A17B（[Team (2026)](#bib.bib2)）作为 $M_{\mathrm{cap}}$ 及初始全局场景描述器。GLM-5.2（[GLM-5-Team et al. (2026)](#bib.bib3)）执行增量事实抽取与 QA 生成。全局视图错误干扰项从 Qwen3.5-397B-A17B、Qwen3-VL-235B-A22B-Instruct（[Bai et al. (2025)](#bib.bib5)）与 Kimi-K2.6（[Team et al. (2026b)](#bib.bib4)）对整幅图像上全局问题所产生的错误答案中挖掘，每个模型采样 10 个答案（共 30 个）。所有验证阶段同样对每个模型采样 10 个答案，并施加逐模型准确率阈值。完整的模型分工、验证阈值与干扰项修复设置见[附录 B](#A2)。

#### 数据生成与基准整理。

我们从 ZwZ（[Wei et al. (2026)](#bib.bib1)）中随机采样 12K 张图像——ZwZ 从多个来源收集高分辨率图像（[Kirillov et al. (2023)](#bib.bib39)；[Chuang et al. (2025)](#bib.bib41)；[Chen et al. (2022)](#bib.bib44)；[Changpinyo et al. (2021)](#bib.bib43)；[Krishna et al. (2017)](#bib.bib42)；[Schuhmann et al. (2022)](#bib.bib40)）——并用 ZoomGain 生成 23,610 个 QA 对的候选池。GLM-5.2 联合生成局部问题与全局问题的中英文版本，一道问题的两个语言版本计为一个 QA 对。两名人工审核者从该池中选出 1,000 道题用于基准，不撰写或编辑任何问题或答案。

#### 训练数据选择与匹配。

排除这 1,000 条基准条目后，其余 QA 构成训练池。为与 ZwZ 公平比较，对每张图像，我们取双方可用唯一问题数中的较小者，并从每一侧无放回地采样同样数量，得到 8,746 个图像匹配的 QA 对。随后在双方各复制 254 个随机选取的对，使每个数据集达到 9,000 个样本。因此两个训练集使用相同的源图像（ZwZ 保留其边界框叠加），仅在问题上不同。

表 1：与现有细粒度感知基准的比较。*QA 撰写*：谁撰写问题与答案；Model+Human 表示由模型生成、经人工标注者精修的问题，Model 表示完全由模型撰写、人工只决定纳入哪些候选的问题。*盲过滤*：构建期间移除无需图像即可回答的问题。*局部验证*：答案在拉近的证据区域上被自动验证。*双视图*：同时提供整幅图像与证据区域。*专用干扰项生成*：为构建干扰项选项设置的独立阶段（[第 3.3 节](#S3.SS3)）。该列中 ✗ 表示未报告专用阶段，N/A 表示开放式评测。「–」表示未提供或未说明。

| 基准 | 问题数 | QA 撰写 | 语言 | 证据 | 盲过滤 | 局部验证 | 双视图 | 专用干扰项生成 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ZoomBench [Wei et al. (2026)](#bib.bib1) | 845 | Model+Human | EN | 自动 | ✗ | ✗ | ✓ | ✗ |
| V\* Bench [Wu and Xie (2023)](#bib.bib21) | 191 | Human | EN | 人工 | ✗ | ✗ | ✗ | ✗ |
| HR-Bench [Wang et al. (2025b)](#bib.bib22) | 200 | Model+Human | EN | ✗ | ✗ | ✗ | ✗ | ✗ |
| VisualProbe [Lai et al. (2025)](#bib.bib23) | 500 | – | EN | ✗ | ✗ | ✗ | ✗ | N/A |
| TreeBench [Wang et al. (2025a)](#bib.bib24) | 405 | Model+Human | EN | 人工 | ✗ | ✗ | ✗ | ✗ |
| FINERS-4k [Zhang et al. (2026b)](#bib.bib25) | 2,427 | Human | EN | – | ✗ | ✗ | ✗ | ✗ |
| ZoomGainBench（本文） | 1,000 | Model | EN/ZH | 自动 | ✓ | ✓ | ✓ | ✓ |

## 5 在 ZoomGainBench 上的实验

为考察从全局-拉近感知差中挖掘的问题是否对当前 VLM 构成真实挑战，我们在 ZoomGainBench 上评测 28 个广泛使用的 VLM，涵盖闭源前沿、智能体、细粒度增强的单次前向，以及开源通用 VLM（[表 2](#S5.T2)）。

#### 统计。

ZoomGainBench 包含覆盖 941 张图像的 1,000 道题：472 道属性识别、94 道计数、434 道 OCR。属性题有 4 到 6 个选项；计数与 OCR 题为开放式。每道题都有英文与中文版本（共 2,000 个评测实例）以及由其裁剪框指定的自动获得证据区域。[附录 C](#A3)展示了三类问题的示例。[表 1](#S4.T1)将 ZoomGainBench 与现有基准比较：它是唯一同时具备完全由模型撰写的 QA、自动验证与专用干扰项构建的基准；[第 5.2 节](#S5.SS2)说明这些干扰项如何揭示跨模型共享的错误。

表 2：ZoomGainBench 上的评测结果。分数以百分比报告，分英文与中文问题。每种语言的「总体」按各类别问题数量加权。每列中加粗与带下划线的分数分别表示所有模型中的最佳与次佳结果。

| 模型 | 英文 属性 | 英文 计数 | 英文 OCR | 英文 总体 | 中文 属性 | 中文 计数 | 中文 OCR | 中文 总体 | 总体 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **闭源前沿 VLM** | | | | | | | | | |
| GPT-5.5 [OpenAI ()](#bib.bib15) | <u>52.75</u> | 57.45 | 60.40 | 56.51 | 52.12 | 63.83 | 60.96 | 57.06 | 56.79 |
| Gemini-3.6-Flash [Google DeepMind (2026)](#bib.bib20) | 51.27 | 42.55 | **74.71** | <u>60.62</u> | 48.52 | 45.74 | **71.42** | 58.20 | 59.41 |
| Claude-Opus-5 [Anthropic (2026)](#bib.bib18) | 48.09 | 63.83 | <u>71.86</u> | 59.89 | 48.73 | 62.77 | <u>71.29</u> | <u>59.84</u> | <u>59.86</u> |
| GPT-5.6-Sol [OpenAI ()](#bib.bib16) | **56.57** | 62.77 | 67.93 | **62.08** | **54.03** | 63.83 | 65.84 | **60.07** | **61.08** |
| **智能体 VLM** | | | | | | | | | |
| DeepEyes-7B [Zheng et al. (2026)](#bib.bib26) | 24.79 | 20.21 | 41.05 | 31.42 | 24.36 | 22.34 | 34.46 | 28.55 | 29.99 |
| Thyme-7B [Zhang et al. (2025)](#bib.bib29) | 26.69 | 34.04 | 43.88 | 34.85 | 22.88 | 31.91 | 40.31 | 31.30 | 33.07 |
| DeepEyesV2-7B [Hong et al. (2026)](#bib.bib27) | 22.25 | 41.49 | 43.70 | 33.37 | 22.67 | 34.04 | 43.62 | 32.83 | 33.10 |
| PixelReasoner-7B [Su et al. (2026)](#bib.bib28) | 27.12 | 45.74 | 44.83 | 36.56 | 25.42 | 23.40 | 40.13 | 31.62 | 34.09 |
| **细粒度增强的单次前向 VLM** | | | | | | | | | |
| ZwZ-4B [Wei et al. (2026)](#bib.bib1) | 30.08 | 39.36 | 29.68 | 30.78 | 33.47 | 50.00 | 34.45 | 35.45 | 33.12 |
| Vision-OPD-4B [Yuan et al. (2026)](#bib.bib30) | 35.59 | 59.57 | 45.69 | 42.23 | 39.62 | 59.57 | 43.80 | 43.31 | 42.77 |
| Vision-OPD-9B [Yuan et al. (2026)](#bib.bib30) | 46.40 | 55.32 | 47.18 | 47.58 | 47.67 | 60.64 | 37.97 | 44.68 | 46.13 |
| ZwZ-8B [Wei et al. (2026)](#bib.bib1) | 42.58 | 55.32 | 50.53 | 47.23 | 44.70 | 52.13 | 51.77 | 48.47 | 47.85 |
| **开源通用 VLM** | | | | | | | | | |
| MiMo-VL-7B-RL [Xiaomi (2025)](#bib.bib14) | 23.73 | 34.04 | 20.06 | 23.11 | 23.31 | 41.49 | 32.06 | 28.82 | 25.96 |
| GLM-4.6V (106B) [Team et al. (2025)](#bib.bib13) | 24.36 | 38.30 | 31.57 | 28.80 | 22.46 | 36.17 | 28.51 | 26.37 | 27.59 |
| Qwen3-VL-4B [Bai et al. (2025)](#bib.bib5) | 21.82 | 43.62 | 31.14 | 27.92 | 22.88 | 41.49 | 33.63 | 29.30 | 28.61 |
| Qwen3-VL-8B [Bai et al. (2025)](#bib.bib5) | 15.89 | 41.49 | 39.17 | 28.40 | 19.92 | 30.85 | 41.64 | 30.37 | 29.38 |
| Qwen3.5-4B [Team (2026)](#bib.bib2) | 21.40 | 51.06 | 34.40 | 29.83 | 22.67 | 46.81 | 34.87 | 30.23 | 30.03 |
| Qwen3.5-9B [Team (2026)](#bib.bib2) | 21.82 | 41.49 | 37.79 | 30.60 | 22.67 | 47.87 | 42.52 | 33.66 | 32.13 |
| Qwen3.5-35B-A3B [Team (2026)](#bib.bib2) | 28.18 | 44.68 | 46.10 | 37.51 | 27.33 | 51.06 | 47.95 | 38.51 | 38.01 |
| Qwen3.6-35B-A3B [Qwen Team (2026c)](#bib.bib7) | 26.91 | 54.26 | 50.21 | 39.59 | 26.69 | 52.13 | 46.17 | 37.54 | 38.57 |
| Qwen3-VL-235B-A22B [Bai et al. (2025)](#bib.bib5) | 29.45 | 52.13 | 48.01 | 39.64 | 30.93 | 50.00 | 50.90 | 41.39 | 40.51 |
| Qwen3.5-27B [Team (2026)](#bib.bib2) | 33.05 | 51.06 | 45.92 | 40.33 | 34.75 | 58.51 | 48.67 | 43.02 | 41.68 |
| Qwen3.6-27B [Qwen Team (2026b)](#bib.bib8) | 33.47 | 56.38 | 47.47 | 41.70 | 37.71 | **70.21** | 45.33 | 44.07 | 42.89 |
| Qwen3.8-27B [Qwen Team (2026e)](#bib.bib9) | 40.25 | 54.26 | 45.49 | 43.84 | 44.92 | 62.77 | 43.05 | 45.78 | 44.81 |
| Qwen3.5-397B-A17B [Team (2026)](#bib.bib2) | 33.47 | <u>65.96</u> | 51.95 | 44.55 | 38.14 | 62.77 | 50.41 | 45.78 | 45.16 |
| GLM-5.3-Flash (320B) [GLM-5-Team et al. (2026)](#bib.bib3) | 44.07 | 54.26 | 43.77 | 44.90 | 46.61 | 55.32 | 43.74 | 46.18 | 45.54 |
| Kimi-K3 (2.8T) [Team et al. (2026a)](#bib.bib12) | 49.15 | 64.89 | 45.48 | 49.04 | 46.82 | 64.89 | 46.22 | 48.26 | 48.65 |
| Qwen3.8-Flash-Next (125B) [Qwen Team (2026a)](#bib.bib10); [Qwen Team (2026d)](#bib.bib11) | 47.46 | **67.02** | 56.97 | 53.42 | <u>52.97</u> | <u>67.02</u> | 58.45 | 56.67 | 55.05 |

#### 评测协议。

多项选择题按所选选项的精确匹配计分，计数题按预测整数的精确匹配计分。OCR 题若 ANLS 分数不低于 $0.7$ 则取该分数，否则计 0。各模型的提示词、解码温度与思考模式设置见[附录 F](#A6)。

### 5.1 基准结果

ZoomGain 甚至令前沿 VLM 也感到棘手。最强模型 GPT-5.6-Sol 的总体得分仅为 61.08（[表 2](#S5.T2)），只有五个模型超过 50。四个闭源模型全部优于任何开源通用 VLM：即便是 GPT-5.5（56.79）也超过最佳开源通用模型 Qwen3.8-Flash-Next（55.05）。

细粒度增强 VLM 极具竞争力。ZwZ-8B 与 Vision-OPD-9B 分别比各自基座模型 Qwen3-VL-8B 与 Qwen3.5-9B 提升 18.47 与 14.00 分。尽管体积更小，ZwZ-8B（47.85）也超过 Qwen3.5-397B-A17B（45.16）。

属性识别是最困难的类别。在 28 个模型中有 23 个，属性识别在两种语言上的平均得分最低——尽管它是唯一的多项选择类别，而均匀猜测的准确率约为 21.5%。例如 Qwen3-VL-8B 在两种语言中都低于该水平（英文 15.89，中文 19.92），这促使我们分析究竟是哪些干扰项吸引了错误选择。

### 5.2 错误分析

图 3：模型在 ZoomGainBench 上失败在哪里。(a) 在只考虑错误答案时，各模型组选择每类干扰项的频率相对于随机基线的比值。大于 1 表示过度选择。*全局视图错误 + 盲猜* 表示同时作为模型查看整幅图像时的错误答案、以及在无图像时基于语言先验的猜测而产生的干扰项。(b) 未参与构建的 26 个模型（除 Qwen3.5-397B-A17B 与 Qwen3-VL-235B-A22B-Instruct 之外的全部受评模型）选择全局视图错误的频率，按每个错误在构建期间收集的 30 个整幅图像答案中出现的频率分组。(c) 按锚点在整幅图像中面积四分位分组的准确率。

#### 模型会被全局视图错误误导。

由于每个干扰项都保留了其在构建时的来源（[第 3.3 节](#S3.SS3)），我们可以追踪错误选择流向了哪里。在全部 28 个模型上，全局视图错误干扰项获得了 71.7% 的错误选择，超过 54.5% 的随机基线[^fn1]，而盲猜与视觉证据分别只获得其随机基线的 0.54 倍与 0.59 倍（[图 3](#S5.F3)(a)）。这种过度选择存在于每个模型上，包括未参与构建的模型。此外，在构建过程中出现得更频繁的错误答案，也更多被其他模型选择。在未参与构建的 26 个模型中，在 30 个整幅图像答案中出现 1–2 次的错误被选择的概率为 17.7%，而出现超过 10 次的错误为 46.0%（[图 3](#S5.F3)(b)）。也就是说，模型复现了构建期间观察到的全局视图混淆，猜测一个场景上合理的答案，而不是分辨所问细节，例如把冰球运动员裤子上的标志说成某个冰球装备品牌（见[附录 E](#A5)的[图 8](#A5.F8)(a)）。换言之，从全局视图错误中挖掘的干扰项捕捉的是跨模型共享的混淆，而非参与构建的模型的特有偏差。

[^fn1]: 该基线假设：每当模型答错时，它在该题的干扰项中均匀随机选择。

#### 目标越小越难。

对每个模型组，准确率都随锚点占图像面积比例的增大而上升（[图 3](#S5.F3)(c)）：在所有模型上平均，它从最小四分位的 28.9%（锚点占图像不到 0.4%）上升到最大四分位的 55.2%。

[附录 D](#A4)进一步报告开放式问题的错误分析，包括错误计数与真值的差异，以及常见的 OCR 错误模式。

## 6 ZoomGain 训练数据实验

### 6.1 主要结果

#### 设置。

我们在[第 4 节](#S4.SS0.SSS0.Px3)所述、按图像匹配的 ZoomGain 与 ZwZ 集合上进行实验，每个集合 9,000 个样本。我们选择 Qwen3.5-4B 与 Qwen3.5-9B（[Team (2026)](#bib.bib2)）作为基座模型，在相同设置下分别在每个集合上使用 GRPO（[Shao et al. (2024)](#bib.bib37)）进行强化学习（批大小 64，每题 8 次 rollout；其他细节见[附录 G](#A7)）。我们在四组基准上评测。*同源（held-in）*：ZoomGainBench。*留出细粒度感知（held-out）*：ZoomBench（[Wei et al. (2026)](#bib.bib1)）、V\* Bench（[Wu and Xie (2023)](#bib.bib21)）、HR-Bench 4K 与 8K（[Wang et al. (2025b)](#bib.bib22)）、MME-RealWorld-Lite（[Zhang et al. (2024)](#bib.bib38)）、TreeBench（[Wang et al. (2025a)](#bib.bib24)）与 VisualProbe（[Lai et al. (2025)](#bib.bib23)）。*通用感知*：CV-Bench（[Tong et al. (2024a)](#bib.bib31)）、MMStar（[Chen et al. (2024)](#bib.bib32)）与 MMVP（[Tong et al. (2024b)](#bib.bib33)）。*困难感知与推理*：BabyVision（[Chen et al. (2026)](#bib.bib34)）、PerceptionBench（[Lin et al. (2026)](#bib.bib35)）与 O3-Bench（[Li et al. (2026a)](#bib.bib36)）。我们还与若干大参数 VLM 比较，包括开源与闭源模型（[Google DeepMind (2025)](#bib.bib17)；[OpenAI ()](#bib.bib19)）。我们报告 13 个留出基准上的平均分，不含 ZoomGainBench。由于 ZoomGainBench 与 ZoomGain 训练数据由同一生成流程产生，纳入它可能对 ZoomGain 模型有利。

表 3：在 ZoomGain 与 ZwZ 数据上进行 RL 训练的结果。$\Delta_{\mathrm{ZoomGain-ZwZ}}$ 与 $\Delta_{\mathrm{ZoomGain-Base}}$ 分别表示相对 ZwZ 训练模型与基座模型的分数增益；Avg. 在 13 个留出基准上计算，不含 ZoomGainBench。

| 模型 | 同源 | 细粒度感知 | | | | | | | 通用感知 | | | 困难感知与推理 | | | 仅留出均值 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | ZoomGainBench | Zoom Bench | V\* Bench | HR 4K | HR 8K | MME-RW Lite | Tree Bench | Visual Probe | CV-Bench | MMStar | MMVP | Baby Vision | Perception Bench | O3-Bench |  |
| **若干大参数 VLM** | | | | | | | | | | | | | | | |
| GPT-5.1 | 23.22 | 47.22 | 70.16 | 67.00 | 65.25 | 45.86 | 47.65 | 29.90 | 84.22 | 71.60 | 32.67 | 13.92 | 28.97 | 31.01 | 48.88 |
| Qwen3-VL-235B-A22B | 40.51 | 49.11 | 87.96 | 84.50 | 81.62 | 58.16 | 53.58 | 46.41 | 86.72 | 76.33 | 64.00 | 18.30 | 35.50 | 60.58 | 61.75 |
| Qwen3.5-122B-A10B | 41.11 | 51.83 | 84.82 | 86.50 | 83.75 | 57.89 | 54.07 | 44.85 | 88.06 | 74.60 | 70.00 | 19.07 | 38.80 | 65.22 | 63.04 |
| Qwen3.5-397B-A17B | 45.16 | 54.91 | 87.43 | 86.50 | 85.12 | 57.06 | 53.33 | 49.51 | 89.57 | 76.00 | 72.67 | 20.36 | 47.50 | 72.17 | 65.55 |
| GLM-5.3-Flash (320B) | 45.54 | 56.80 | 89.01 | 87.00 | 84.75 | 62.12 | 60.25 | 48.35 | 88.94 | 79.47 | 74.67 | 20.10 | 41.90 | 65.51 | 66.07 |
| Gemini-3-Flash | 51.27 | 59.29 | 86.39 | 87.88 | 85.00 | 55.86 | 48.64 | 49.71 | 89.57 | 83.60 | 82.67 | 34.51 | 43.50 | 71.01 | 67.51 |
| **我们的实验模型** | | | | | | | | | | | | | | | |
| Qwen3.5-4B | 30.03 | 48.88 | 81.68 | 81.25 | 77.63 | 57.89 | 49.38 | 43.30 | 85.99 | 66.80 | 57.33 | 14.69 | 33.10 | 54.20 | 57.86 |
| w/ ZwZ 9K | 40.99 | 57.63 | 86.91 | 81.25 | 79.00 | 57.43 | 45.19 | 52.43 | 86.58 | 68.93 | 53.33 | 10.82 | 30.43 | 56.23 | 58.94 |
| w/ ZoomGain 9K | 55.81 | 59.88 | 90.05 | 87.25 | 83.88 | 61.59 | 49.14 | 57.28 | 88.02 | 72.53 | 61.33 | 21.13 | 36.23 | 63.19 | 63.96 |
| $\Delta_{\mathrm{ZoomGain-ZwZ}}$ | +14.83 | +2.25 | +3.14 | +6.00 | +4.88 | +4.17 | +3.95 | +4.85 | +1.44 | +3.60 | +8.00 | +10.31 | +5.80 | +6.96 | +5.03 |
| $\Delta_{\mathrm{ZoomGain-Base}}$ | +25.78 | +11.00 | +8.37 | +6.00 | +6.25 | +3.70 | -0.24 | +13.98 | +2.03 | +5.73 | +4.00 | +6.44 | +3.13 | +8.99 | +6.10 |
| Qwen3.5-9B | 32.13 | 50.30 | 86.91 | 82.13 | 79.63 | 58.52 | 49.88 | 44.66 | 86.27 | 71.73 | 60.00 | 15.98 | 34.20 | 56.52 | 59.75 |
| w/ ZwZ 9K | 44.07 | 58.93 | 90.58 | 85.50 | 82.38 | 61.70 | 47.90 | 52.62 | 88.16 | 73.27 | 63.33 | 17.27 | 34.13 | 57.10 | 62.53 |
| w/ ZoomGain 9K | 55.48 | 60.36 | 93.19 | 90.25 | 85.50 | 63.31 | 53.33 | 56.31 | 88.58 | 73.87 | 70.00 | 17.53 | 39.00 | 68.12 | 66.10 |
| $\Delta_{\mathrm{ZoomGain-ZwZ}}$ | +11.41 | +1.43 | +2.62 | +4.75 | +3.13 | +1.62 | +5.43 | +3.69 | +0.42 | +0.60 | +6.67 | +0.26 | +4.87 | +11.01 | +3.58 |
| $\Delta_{\mathrm{ZoomGain-Base}}$ | +23.35 | +10.06 | +6.28 | +8.12 | +5.87 | +4.79 | +3.45 | +11.65 | +2.31 | +2.14 | +10.00 | +1.55 | +4.80 | +11.60 | +6.35 |

#### 结果。

如[表 3](#S6.T3)所示，用 ZoomGain 数据训练的模型在全部 14 个基准上都一致优于其 ZwZ 训练的对应模型。由于两个训练集仅在问题上不同，这些增益可归因于 ZoomGain 构造的问题。此外，ZoomGain 带来的提升覆盖所有基准组。与基座模型相比，ZwZ 的增益主要集中在细粒度感知上。相比之下，ZoomGain 改善了全部三组。ZoomGain 相对 ZwZ 的优势在困难感知与推理上最明显：9B 模型在 O3-Bench 上增益 11.01 分，4B 模型在 BabyVision 上增益 10.31 分。这些结果表明，ZoomGain 数据使模型获得了可迁移的细粒度感知能力。

值得注意的是，仅用 9K 个训练样本，9B 模型就取得 66.10 的平均分，超过 Qwen3.5-397B-A17B（65.55），并与 GLM-5.3-Flash（66.07）相当；4B 模型（63.96）也超过 Qwen3.5-122B-A10B 与 ZwZ 训练的 9B 模型。此外，在所有对比模型中，ZoomGain 训练的模型在 7 个细粒度感知基准中的 6 个上取得最佳结果。不过我们也注意到，最强的大型模型在通用感知以及困难感知与推理上仍然领先，说明这些任务仍高度依赖模型规模与推理能力。

### 6.2 消融研究

#### 设置。

我们在 Qwen3.5-4B 上消融 ZoomGain 的两个核心设计。所有变体都使用 9K 训练样本，RL 设置与评测协议与[表 3](#S6.T3)相同。(1) 移除增量证据：不再要求问题基于只出现在拉近视图描述中的增量信息，而是直接从拉近视图描述生成问题。源图像、候选 QA 池大小与 9K 样本选择流程在其他方面与完整版本相同。(2) 移除专用干扰项：保持每道题、其答案、正确选项的位置与选项数量不变，仅把每道多项选择题的干扰项替换为同一答案类别（例如颜色或材质）中其他训练题的正确答案。OCR 与计数题为开放式，不受该消融影响。

表 4：增量证据与专用干扰项的消融。Avg. 在 10 个留出基准上计算。

| 模型 | 增量证据 | 专用干扰项 | 同源 | 细粒度感知 | | | | | | | 困难感知与推理 | | | 仅留出均值 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  | ZoomGainBench | Zoom Bench | V\* Bench | HR 4K | HR 8K | MME-RW Lite | Tree Bench | Visual Probe | Baby Vision | Perception Bench | O3-Bench |  |
| Qwen3.5-4B | – | – | 30.03 | 48.88 | 81.68 | 81.25 | 77.63 | 57.89 | 49.38 | 43.30 | 14.69 | 33.10 | 54.20 | 54.20 |
| +ZoomGain 9K | ✗ | ✓ | 49.71 | 56.45 | 88.48 | 85.50 | 81.75 | 60.24 | 48.40 | 52.82 | 18.56 | 34.70 | 58.84 | 58.57 |
| +ZoomGain 9K | ✓ | ✗ | 46.85 | 57.04 | 90.05 | 85.75 | 80.25 | 62.69 | 48.89 | 54.76 | 17.53 | 34.97 | 59.42 | 59.14 |
| +ZoomGain 9K | ✓ | ✓ | 55.81 | 59.88 | 90.05 | 87.25 | 83.88 | 61.59 | 49.14 | 57.28 | 21.13 | 36.23 | 63.19 | 60.96 |

#### 结果。

如[表 4](#S6.T4)所示，结果表明两个设计都对训练性能有贡献。完整 ZoomGain 流程在 10 个留出基准上取得最高平均分。移除任一组件都会在几乎所有基准上导致性能下降。两个消融在困难感知与推理组上的损失都最大。完整版本在这三个基准上平均比基座模型提升 6.19 分，而每个消融只保留了约一半的增益。这表明两个设计主要提升的是可迁移到训练分布之外的感知与推理能力。

增量证据的作用在细粒度基准上最明显：移除它使 ZoomBench 与 VisualProbe 的分数分别下降 3.43 与 4.46 分。这表明把问题限制在拉近后才显现的证据上，迫使模型学习定位并识别难以分辨的细节。同时，移除专用干扰项在同源 ZoomGainBench 上造成最大跌幅，达 8.96 分。这在意料之中，因为该基准的选项正是用同一流程构建的。使用专用干扰项引入了更难的混淆，迫使模型更仔细地关注视觉细节，从而在相同数据预算下增强其感知能力。

## 7 结论

为解决大规模构建可靠细粒度视觉监督的困难，我们提出 ZoomGain——一条利用全局视图与拉近视图之间感知差的数据构建流程。ZoomGain 把只有拉近后才显现的细节转化为关于整幅图像的问题，用多个模型在拉近视图上验证其答案，并挖掘可能误导 VLM 的多源干扰项。借助该流程，我们构建了 ZoomGainBench——一个具有挑战性的基准，其问题与答案完全由模型撰写。通过分析失败案例，我们发现不同 VLM 在整幅图像中细节无法分辨时存在相似的混淆。实验进一步表明，ZoomGain 数据作为训练监督是有效的，能够一致地提升 VLM 的细粒度感知、通用感知以及困难感知与推理能力。

## 参考文献

* Anthropic (2026)
  Anthropic
  Introducing Claude Opus 5.
  Note: <https://www.anthropic.com/news/claude-opus-5>
  Cited by: [Table 2](#S5.T2.8.6.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Bai et al. (2025)
  S. Bai, Y. Cai, R. Chen, K. Chen, X. Chen, Z. Cheng, L. Deng, W. Ding, C. Gao, C. Ge, W. Ge, Z. Guo, Q. Huang, J. Huang, F. Huang, B. Hui, S. Jiang, Z. Li, M. Li, M. Li, K. Li, Z. Lin, J. Lin, X. Liu, J. Liu, C. Liu, Y. Liu, D. Liu, S. Liu, D. Lu, R. Luo, C. Lv, R. Men, L. Meng, X. Ren, X. Ren, S. Song, Y. Sun, J. Tang, J. Tu, J. Wan, P. Wang, P. Wang, Q. Wang, Y. Wang, T. Xie, Y. Xu, H. Xu, J. Xu, Z. Yang, M. Yang, J. Yang, A. Yang, B. Yu, F. Zhang, H. Zhang, X. Zhang, B. Zheng, H. Zhong, J. Zhou, F. Zhou, J. Zhou, Y. Zhu, and K. Zhu
  Qwen3-vl technical report.
  arXiv preprint arXiv:2511.21631.
  Cited by: [Table 5](#A2.T5.4.4.1.1.1 "In Appendix B Construction Settings ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§1](#S1.p1.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§4](#S4.SS0.SSS0.Px1.p1.1 "Model Roles and Verification Settings. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.21.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.22.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.27.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Bergmann et al. (2019)
  P. Bergmann, M. Fauser, D. Sattlegger, and C. Steger
  MVTec ad – a comprehensive real-world dataset for unsupervised anomaly detection.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR),
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Cadene et al. (2019)
  R. Cadene, C. Dancette, M. Cord, D. Parikh, et al.
  RUBi: reducing unimodal biases for visual question answering.
  Advances in Neural Information Processing Systems 32, pp. 841–852.
  Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Fine-grained perception benchmarks. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§3.3](#S3.SS3.p1.1 "3.3 Quality Verification and Multi-Source Distractors ‣ 3 ZoomGain Data Construction Pipeline ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Changpinyo et al. (2021)
  S. Changpinyo, P. Sharma, N. Ding, and R. Soricut
  Conceptual 12m: pushing web-scale image-text pre-training to recognize long-tail visual concepts.
  In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition,
  pp. 3558–3568.
  Cited by: [§4](#S4.SS0.SSS0.Px2.p1.1 "Data Generation and Benchmark Curation. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Chen et al. (2026)
  L. Chen, W. Xie, Y. Liang, H. He, H. Zhao, Z. Yang, Z. Huang, H. Wu, H. Lu, Y. Bao, et al.
  Babyvision: visual reasoning beyond language.
  arXiv preprint arXiv:2601.06521.
  Cited by: [§6.1](#S6.SS1.SSS0.Px1.p1.1 "Setup. ‣ 6.1 Main Results ‣ 6 Experiments on ZoomGain Training Data ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Chen et al. (2024)
  L. Chen, J. Li, X. Dong, P. Zhang, Y. Zang, Z. Chen, H. Duan, J. Wang, Y. Qiao, D. Lin, and F. Zhao
  Are we on the right way for evaluating large vision-language models?.
  In Advances in Neural Information Processing Systems, A. Globerson, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. Tomczak, and C. Zhang (Eds.),
  Vol. 37, pp. 27056–27087.
  External Links: [Document](https://dx.doi.org/10.52202/079017-0850),
  [Link](https://proceedings.neurips.cc/paper_files/paper/2024/file/2f8ee6a3d766b426d2618e555b5aeb39-Paper-Conference.pdf)
  Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Fine-grained perception benchmarks. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§3.3](#S3.SS3.p1.1 "3.3 Quality Verification and Multi-Source Distractors ‣ 3 ZoomGain Data Construction Pipeline ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§6.1](#S6.SS1.SSS0.Px1.p1.1 "Setup. ‣ 6.1 Main Results ‣ 6 Experiments on ZoomGain Training Data ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Chen et al. (2022)
  M. Chen, Q. Hu, Z. Yu, H. Thomas, A. Feng, Y. Hou, K. McCullough, F. Ren, and L. Soibelman
  Stpls3d: a large-scale synthetic and real aerial photogrammetry 3d point cloud dataset.
  arXiv preprint arXiv:2203.09065.
  Cited by: [§4](#S4.SS0.SSS0.Px2.p1.1 "Data Generation and Benchmark Curation. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Chuang et al. (2025)
  Y. Chuang, Y. Li, D. Wang, C. Yeh, K. Lyu, R. Raghavendra, J. Glass, L. Huang, J. Weston, L. Zettlemoyer, et al.
  Meta clip 2: a worldwide scaling recipe.
  arXiv preprint arXiv:2507.22062.
  Cited by: [§4](#S4.SS0.SSS0.Px2.p1.1 "Data Generation and Benchmark Curation. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* DeepSeek-AI (2026)
  DeepSeek-AI
  DeepSeek-v4: towards highly efficient million-token context intelligence.
  Cited by: [Table 5](#A2.T5.4.7.1.1.1 "In Appendix B Construction Settings ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Gavrikov et al. (2026)
  P. Gavrikov, W. Lin, M. J. Mirza, S. Jahagirdar, M. Huzaifa, S. Doveh, S. Yeung-Levy, J. Glass, and H. Kuehne
  VisualOverload: probing visual understanding of vlms in really dense scenes.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR),
  Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Fine-grained perception benchmarks. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* GLM-5-Team et al. (2026)
  GLM-5-Team, :, A. Zeng, X. Lv, Z. Hou, Z. Du, Q. Zheng, B. Chen, D. Yin, C. Ge, C. Huang, C. Xie, C. Zhu, C. Yin, C. Wang, G. Pan, H. Zeng, H. Zhang, H. Wang, H. Chen, J. Zhang, J. Jiao, J. Guo, J. Wang, J. Du, J. Wu, K. Wang, L. Li, L. Fan, L. Zhong, M. Liu, M. Zhao, P. Du, Q. Dong, R. Lu, Shuang-Li, S. Cao, S. Liu, T. Jiang, X. Chen, X. Zhang, X. Huang, X. Dong, Y. Xu, Y. Wei, Y. An, Y. Niu, Y. Zhu, Y. Wen, Y. Cen, Y. Bai, Z. Qiao, Z. Wang, Z. Wang, Z. Zhu, Z. Liu, Z. Li, B. Wang, B. Wen, C. Huang, C. Cai, C. Yu, C. Li, C. Hu, C. Zhang, D. Zhang, D. Lin, D. Yang, D. Wang, D. Ai, E. Zhu, F. Yi, F. Chen, G. Wen, H. Sun, H. Zhao, H. Hu, H. Zhang, H. Liu, H. Zhang, H. Peng, H. Tai, H. Zhang, H. Liu, H. Wang, H. Yan, H. Ge, H. Liu, H. Chu, J. Zhao, J. Wang, J. Zhao, J. Ren, J. Wang, J. Zhang, J. Gui, J. Zhao, J. Li, J. An, J. Li, J. Yuan, J. Du, J. Liu, J. Zhi, J. Duan, K. Zhou, K. Wei, K. Wang, K. Luo, L. Zhang, L. Sha, L. Xu, L. Wu, L. Ding, L. Chen, M. Li, N. Lin, P. Ta, Q. Zou, R. Song, R. Yang, S. Tu, S. Yang, S. Wu, S. Zhang, S. Li, S. Li, S. Fan, W. Qin, W. Tian, W. Zhang, W. Yu, W. Liang, X. Kuang, X. Cheng, X. Li, X. Yan, X. Hu, X. Ling, X. Fan, X. Xia, X. Zhang, X. Zhang, X. Pan, X. Zou, X. Zhang, Y. Liu, Y. Wu, Y. Li, Y. Wang, Y. Zhu, Y. Tan, Y. Zhou, Y. Pan, Y. Zhang, Y. Su, Y. Geng, Y. Yan, Y. Tan, Y. Bi, Y. Shen, Y. Yang, Y. Li, Y. Liu, Y. Wang, Y. Li, Y. Wu, Y. Zhang, Y. Duan, Y. Zhang, Z. Liu, Z. Jiang, Z. Yan, Z. Zhang, Z. Wei, Z. Chen, Z. Feng, Z. Yao, Z. Chai, Z. Wang, Z. Zhang, B. Xu, M. Huang, H. Wang, J. Li, Y. Dong, and J. Tang
  GLM-5: from vibe coding to agentic engineering.
  External Links: 2602.15763,
  [Link](https://arxiv.org/abs/2602.15763)
  Cited by: [Table 5](#A2.T5.4.3.1.1.1 "In Appendix B Construction Settings ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§1](#S1.p6.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§4](#S4.SS0.SSS0.Px1.p1.1 "Model Roles and Verification Settings. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.32.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Google DeepMind (2025)
  Google DeepMind
  Gemini 3 Flash Model Card.
  Note: <https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-Flash-Model-Card.pdf>
  Cited by: [§6.1](#S6.SS1.SSS0.Px1.p1.1 "Setup. ‣ 6.1 Main Results ‣ 6 Experiments on ZoomGain Training Data ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Google DeepMind (2026)
  Google DeepMind
  Gemini 3.6 Flash Model Card.
  Note: <https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-3-6-Flash-Model-Card.pdf>
  Cited by: [Table 2](#S5.T2.8.5.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Gurari et al. (2018)
  D. Gurari, Q. Li, A. J. Stangl, A. Guo, C. Lin, K. Grauman, J. Luo, and J. P. Bigham
  VizWiz grand challenge: answering visual questions from blind people.
  In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR),
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Hong et al. (2026)
  J. Hong, C. Zhao, C. Zhu, W. Lu, and G. Xu
  Deepeyesv2: toward agentic multimodal model.
  In International Conference on Learning Representations,
  Vol. 2026, pp. 114851–114872.
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§2](#S2.SS0.SSS0.Px2.p1.1 "Improving fine-grained perception. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.11.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Jing et al. (2024)
  L. Jing, R. Li, Y. Chen, and X. Du
  FaithScore: fine-grained evaluations of hallucinations in large vision-language models.
  In Findings of the Association for Computational Linguistics: EMNLP 2024, Y. Al-Onaizan, M. Bansal, and Y. Chen (Eds.),
  Miami, Florida, USA, pp. 5042–5063.
  External Links: [Link](https://aclanthology.org/2024.findings-emnlp.290/),
  [Document](https://dx.doi.org/10.18653/v1/2024.findings-emnlp.290)
  Cited by: [§3.3](#S3.SS3.p1.1 "3.3 Quality Verification and Multi-Source Distractors ‣ 3 ZoomGain Data Construction Pipeline ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Kirillov et al. (2023)
  A. Kirillov, E. Mintun, N. Ravi, H. Mao, C. Rolland, L. Gustafson, T. Xiao, S. Whitehead, A. C. Berg, W. Lo, et al.
  Segment anything.
  In Proceedings of the IEEE/CVF International Conference on Computer Vision,
  pp. 4015–4026.
  Cited by: [§4](#S4.SS0.SSS0.Px2.p1.1 "Data Generation and Benchmark Curation. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Krishna et al. (2017)
  R. Krishna, Y. Zhu, O. Groth, J. Johnson, K. Hata, J. Kravitz, S. Chen, Y. Kalantidis, L. Li, D. A. Shamma, et al.
  Visual genome: connecting language and vision using crowdsourced dense image annotations.
  International journal of computer vision 123 (1), pp. 32–73.
  Cited by: [§4](#S4.SS0.SSS0.Px2.p1.1 "Data Generation and Benchmark Curation. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Lai et al. (2025)
  X. Lai, J. Li, W. Li, T. Liu, T. Li, and H. Zhao
  Mini-o3: scaling up reasoning patterns and interaction turns for visual search.
  arXiv:2509.07969.
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§2](#S2.SS0.SSS0.Px1.p1.1 "Fine-grained perception benchmarks. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§2](#S2.SS0.SSS0.Px2.p1.1 "Improving fine-grained perception. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 1](#S4.T1.16.1.5.1 "In Training Data Selection and Matching. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§6.1](#S6.SS1.SSS0.Px1.p1.1 "Setup. ‣ 6.1 Main Results ‣ 6 Experiments on ZoomGain Training Data ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Li et al. (2026a)
  K. Li, L. Yao, J. Wu, T. Yu, J. Chen, H. Bai, L. Hou, L. Hong, W. Zhang, and N. L. Zhang
  InSight-o3: empowering multimodal foundation models with generalized visual search.
  In The Fourteenth International Conference on Learning Representations,
  Cited by: [§1](#S1.p6.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§2](#S2.SS0.SSS0.Px1.p1.1 "Fine-grained perception benchmarks. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§2](#S2.SS0.SSS0.Px2.p1.1 "Improving fine-grained perception. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§6.1](#S6.SS1.SSS0.Px1.p1.1 "Setup. ‣ 6.1 Main Results ‣ 6 Experiments on ZoomGain Training Data ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Li et al. (2026b)
  P. Li, Z. Gao, L. Zhang, M. Huang, Y. Li, F. Xu, and J. Liu
  Visual-opsd: cross-modal on-policy self-distillation for efficient unified multimodal reasoning.
  arXiv preprint arXiv:2606.18974.
  Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Improving fine-grained perception. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Li et al. (2023)
  Y. Li, Y. Du, K. Zhou, J. Wang, X. Zhao, and J. Wen
  Evaluating object hallucination in large vision-language models.
  In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, H. Bouamor, J. Pino, and K. Bali (Eds.),
  Singapore, pp. 292–305.
  External Links: [Link](https://aclanthology.org/2023.emnlp-main.20/),
  [Document](https://dx.doi.org/10.18653/v1/2023.emnlp-main.20)
  Cited by: [§3.3](#S3.SS3.p1.1 "3.3 Quality Verification and Multi-Source Distractors ‣ 3 ZoomGain Data Construction Pipeline ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Lin et al. (2026)
  Z. Lin, Y. Xie, B. Qu, H. Wang, J. Li, H. Wu, Y. Dong, Z. Yang, J. Zhu, H. Lu, et al.
  PerceptionBench: evaluating atomic visual perception in multimodal large language models.
  arXiv preprint arXiv:2607.24957.
  Cited by: [§6.1](#S6.SS1.SSS0.Px1.p1.1 "Setup. ‣ 6.1 Main Results ‣ 6 Experiments on ZoomGain Training Data ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Liu et al. (2023)
  H. Liu, C. Li, Q. Wu, and Y. J. Lee
  Visual instruction tuning.
  Advances in neural information processing systems 36, pp. 34892–34916.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* [26]
  OpenAI
  GPT-5.1.
  Note: <https://developers.openai.com/api/docs/models/gpt-5.1>Accessed: 2026-09-26
  Cited by: [§6.1](#S6.SS1.SSS0.Px1.p1.1 "Setup. ‣ 6.1 Main Results ‣ 6 Experiments on ZoomGain Training Data ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* [27]
  OpenAI
  GPT-5.5.
  Note: <https://developers.openai.com/api/docs/models/gpt-5.5>
  Cited by: [Table 2](#S5.T2.8.4.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* [28]
  OpenAI
  GPT-5.6 Sol.
  Note: <https://developers.openai.com/api/docs/models/gpt-5.6-sol>
  Cited by: [Table 2](#S5.T2.8.7.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Qwen Team (2026a)
  Qwen Team
  On the design of Qwen3.8-Next architecture: evaluation, efficiency, and training stability.
  Technical report
   Alibaba Group.
  Cited by: [Table 2](#S5.T2.8.34.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Qwen Team (2026b)
  Qwen Team
  Qwen3.6-27B: flagship-level coding in a 27B dense model.
  External Links: [Link](https://qwen.ai/blog?id=qwen3.6-27b)
  Cited by: [Table 2](#S5.T2.8.29.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Qwen Team (2026c)
  Qwen Team
  Qwen3.6-35B-A3B: agentic coding power, now open to all.
  External Links: [Link](https://qwen.ai/blog?id=qwen3.6-35b-a3b)
  Cited by: [Table 2](#S5.T2.8.26.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Qwen Team (2026d)
  Qwen Team
  Qwen3.8-Flash-Next: a new architecture, towards ultimate cost-efficiency.
  External Links: [Link](https://qwen.ai/blog?id=qwen3.8-flash-next)
  Cited by: [Table 2](#S5.T2.8.34.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Qwen Team (2026e)
  Qwen Team
  Qwen3.8-Max: a new bar for coding and cowork.
  External Links: [Link](https://qwen.ai/blog?id=qwen3.8)
  Cited by: [Table 2](#S5.T2.8.30.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Rohrbach et al. (2018)
  A. Rohrbach, L. A. Hendricks, K. Burns, T. Darrell, and K. Saenko
  Object hallucination in image captioning.
  In Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing, E. Riloff, D. Chiang, J. Hockenmaier, and J. Tsujii (Eds.),
  Brussels, Belgium, pp. 4035–4045.
  External Links: [Link](https://aclanthology.org/D18-1437/),
  [Document](https://dx.doi.org/10.18653/v1/D18-1437)
  Cited by: [§3.3](#S3.SS3.p1.1 "3.3 Quality Verification and Multi-Source Distractors ‣ 3 ZoomGain Data Construction Pipeline ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Schuhmann et al. (2022)
  C. Schuhmann, R. Beaumont, R. Vencu, C. Gordon, R. Wightman, M. Cherti, T. Coombes, A. Katta, C. Mullis, M. Wortsman, et al.
  Laion-5b: an open large-scale dataset for training next generation image-text models.
  Advances in neural information processing systems 35, pp. 25278–25294.
  Cited by: [§4](#S4.SS0.SSS0.Px2.p1.1 "Data Generation and Benchmark Curation. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Shao et al. (2024)
  Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu, et al.
  Deepseekmath: pushing the limits of mathematical reasoning in open language models.
  arXiv preprint arXiv:2402.03300.
  Cited by: [§6.1](#S6.SS1.SSS0.Px1.p1.1 "Setup. ‣ 6.1 Main Results ‣ 6 Experiments on ZoomGain Training Data ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Shen et al. (2025)
  H. Shen, K. Zhao, T. Zhao, R. Xu, Z. Zhang, M. Zhu, and J. Yin
  Zoomeye: enhancing multimodal llms with human-like zooming capabilities through tree-based image exploration.
  In Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing,
  pp. 6613–6629.
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§2](#S2.SS0.SSS0.Px2.p1.1 "Improving fine-grained perception. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Su et al. (2026)
  A. Su, H. Wang, W. Ren, F. Lin, and W. Chen
  Pixel reasoner: incentivizing pixel space reasoning via curiosity-driven reinforcement learning.
  Advances in Neural Information Processing Systems 38, pp. 8222–8251.
  Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Improving fine-grained perception. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.12.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Team et al. (2026a)
  K. Team, T. Bai, Y. Bai, Y. Bao, M. C., J. Cai, X. Cai, P. Cao, Y. Cao, Z. Chai, Y. Charles, H. S. Che, G. Chen, G. Chen, G. Chen, H. Chen, J. Chen, J. Chen, J. Chen, K. Chen, P. Chen, R. Chen, W. Chen, X. Chen, Y. Chen, Y. Chen, Y. Chen, Y. Chen, Y. Chen, Y. Chen, Y. Chen, Z. Chen, D. Cheng, Y. Cheng, J. Cui, J. Cui, A. Dai, J. Deng, H. Ding, R. Ding, S. Ding, M. Dong, M. Dong, Y. Dong, Y. Dong, A. Du, C. Du, D. Du, J. Du, Y. Du, Y. Fan, J. Feng, Q. Feng, Y. Feng, K. Fu, Q. Fu, F. Gao, H. Gao, J. Gao, T. Gao, W. Gao, S. Geng, J. Gong, L. Gong, S. Gong, X. Gong, Q. Gu, Y. Gu, S. Guan, H. Guo, S. Guo, X. Guo, Z. Guo, B. Hao, W. Hao, X. Hao, D. He, H. He, L. He, Q. He, W. He, X. He, X. He, Y. He, Y. He, C. Hong, T. Hong, H. Hu, J. Hu, R. Hu, W. Hu, Y. Hu, Z. Hu, L. Hua, J. Huang, K. Huang, R. Huang, S. Huang, W. Huang, Y. Huang, Z. Huang, Z. Huang, Y. Hui, C. Jia, Y. Jiang, Z. Jiang, Z. Jiang, W. Jin, X. Jin, Y. Jing, H. Kong, G. Lai, A. Li, C. Li, C. Li, C. Li, F. Li, G. Li, H. Li, J. Li, J. Li, L. Li, L. Li, L. Li, W. Li, W. Li, X. Li, Y. Li, Y. Li, Y. Li, Y. Li, Z. Li, Z. Li, Z. Li, Z. Li, Z. Li, J. Lin, X. Lin, Y. Lin, Z. Lin, Z. Lin, B. Liu, B. Liu, C. Liu, L. Liu, S. Liu, S. Liu, S. Liu, T. Liu, W. Liu, Y. Liu, Y. Liu, Y. Liu, Y. Liu, Z. Liu, Z. Liu, E. Lu, H. Lu, L. Lu, T. Lu, Z. Lu, A. Luo, G. Luo, J. Luo, Y. Luo, B. Lyu, W. Lyu, S. Mao, Y. Mei, X. Men, M. Ni, Y. Niu, S. Pan, S. Peng, Z. Qi, R. Qin, Z. Qin, Z. Qin, H. Qiu, J. Qiu, J. Qiu, B. Qu, Y. Qu, Z. Shang, Y. Shao, H. Shen, J. Shi, J. Shi, L. Shi, S. Shi, W. Siu, P. Song, X. Song, J. Su, Y. Su, Z. Su, L. Sui, J. Sun, J. Sun, S. Sun, S. Sun, T. Sun, Y. Sun, Y. Tai, C. Tang, H. Tang, S. Tang, Z. Tang, C. Tian, R. Tian, Y. Tian, W. Tu, C. Wang, C. Wang, C. Wang, D. Wang, F. Wang, H. Wang, H. Wang, H. Wang, H. Wang, H. Wang, H. Wang, J. Wang, J. Wang, J. Wang, J. Wang, L. Wang, S. Wang, S. Wang, S. Wang, S. Wang, S. Wang, T. Wang, W. Wang, X. Wang, X. Wang, X. Wang, X. Wang, Y. Wang, Y. Wang, Y. Wang, Y. Wang, Y. Wang, Y. Wang, Y. Wang, Y. Wang, Z. Wang, Z. Wang, Z. Wang, Z. Wang, Z. Wang, Z. Wang, C. Wei, M. Wei, S. Wei, Z. Wen, F. Wu, H. Wu, R. Wu, W. Wu, X. Wu, Y. Wu, Y. Wu, Y. Wu, Z. Wu, X. Xian, C. Xiang, Y. Xiang, B. Xiao, C. Xiao, X. Xiao, J. Xie, X. Xie, Y. Xie, Z. Xie, B. Xing, Y. Xiong, B. Xu, B. Xu, J. Xu, J. Xu, J. Xu, J. Xu, L. H. Xu, Q. Xu, S. Xu, S. Xu, T. Xu, T. Xu, W. Xu, X. Xu, Y. Xu, Y. Xu, Y. Xu, Z. Xu, H. Xue, J. Yan, Y. Yan, F. Yang, G. Yang, H. Yang, J. Yang, R. Yang, W. Yang, X. Yang, X. Yang, Y. Yang, Y. Yang, Y. Yang, Y. Yang, Z. Yang, Z. Yang, Z. Yang, Z. Yang, H. Yao, D. Ye, H. Ye, W. Ye, Z. Ye, B. Yin, H. Yin, X. Yin, C. Yu, H. Yu, L. Yu, S. Yu, S. Yu, T. Yu, E. Yuan, M. Yuan, T. Yue, W. Yue, Y. Yue, D. Zha, H. Zhan, B. H. Zhang, D. Zhang, F. Zhang, H. Zhang, H. Zhang, H. Zhang, J. Zhang, J. Zhang, J. Zhang, K. Zhang, M. Zhang, P. Zhang, Q. Zhang, R. Zhang, R. Zhang, S. Zhang, S. Zhang, X. Zhang, X. Zhang, Y. Zhang, Y. Zhang, Y. Zhang, Y. Zhang, Y. Zhang, Y. Zhang, Y. Zhang, Y. Zhang, Y. Zhang, Y. Zhang, Z. Zhang, Z. Zhang, B. Zhao, C. Zhao, F. Zhao, J. Zhao, J. Zhao, S. Zhao, W. Zhao, X. Zhao, X. Zhao, Y. Zhao, Z. Zhao, H. Zheng, H. Zheng, R. Zheng, S. Zheng, T. Zheng, H. Zhong, L. Zhong, L. Zhong, M. Zhou, Q. Zhou, R. Zhou, R. Zhou, X. Zhou, Y. Zhou, Z. Zhou, J. Zhu, L. Zhu, X. Zhu, Y. Zhu, Y. Zhu, Z. Zhu, C. Zhuang, W. Zhuang, and X. Zu
  Kimi k3: open frontier intelligence.
  External Links: 2607.24653,
  [Link](https://arxiv.org/abs/2607.24653)
  Cited by: [Table 2](#S5.T2.8.33.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Team et al. (2026b)
  K. Team, T. Bai, Y. Bai, Y. Bao, S. H. Cai, Y. Cao, Y. Charles, H. S. Che, C. Chen, G. Chen, H. Chen, J. Chen, J. Chen, J. Chen, J. Chen, K. Chen, L. Chen, R. Chen, X. Chen, Y. Chen, Y. Chen, Y. Chen, Y. Chen, Y. Chen, Y. Chen, Y. Chen, Y. Chen, Z. Chen, Z. Chen, D. Cheng, M. Chu, J. Cui, J. Deng, M. Diao, H. Ding, M. Dong, M. Dong, Y. Dong, Y. Dong, A. Du, C. Du, D. Du, L. Du, Y. Du, Y. Fan, S. Fang, Q. Feng, Y. Feng, G. Fu, K. Fu, H. Gao, T. Gao, Y. Ge, S. Geng, C. Gong, X. Gong, Z. Gongque, Q. Gu, X. Gu, Y. Gu, L. Guan, Y. Guo, X. Hao, W. He, W. He, Y. He, C. Hong, H. Hu, J. Hu, Y. Hu, Z. Hu, K. Huang, R. Huang, W. Huang, Z. Huang, T. Jiang, Z. Jiang, X. Jin, Y. Jing, G. Lai, A. Li, C. Li, C. Li, F. Li, G. Li, G. Li, H. Li, H. Li, J. Li, J. Li, J. Li, L. Li, M. Li, W. Li, W. Li, X. Li, X. Li, Y. Li, Y. Li, Y. Li, Y. Li, Z. Li, Z. Li, W. Liao, J. Lin, X. Lin, Z. Lin, Z. Lin, C. Liu, C. Liu, H. Liu, L. Liu, S. Liu, S. Liu, S. Liu, T. Liu, T. Liu, W. Liu, X. Liu, Y. Liu, Y. Liu, Y. Liu, Y. Liu, Y. Liu, Z. Liu, Z. Liu, E. Lu, H. Lu, Z. Lu, J. Luo, T. Luo, Y. Luo, L. Ma, Y. Ma, S. Mao, Y. Mei, X. Men, F. Meng, Z. Meng, Y. Miao, M. Ni, K. Ouyang, S. Pan, B. Pang, Y. Qian, R. Qin, Z. Qin, J. Qiu, B. Qu, Z. Shang, Y. Shao, T. Shen, Z. Shen, J. Shi, L. Shi, S. Shi, F. Song, P. Song, T. Song, X. Song, H. Su, J. Su, Z. Su, L. Sui, J. Sun, J. Sun, T. Sun, F. Sung, Y. Tai, C. Tang, H. Tang, X. Tang, Z. Tang, J. Tao, S. Teng, C. Tian, P. Tian, A. Wang, B. Wang, C. Wang, C. Wang, C. Wang, D. Wang, D. Wang, D. Wang, F. Wang, H. Wang, H. Wang, H. Wang, H. Wang, H. Wang, J. Wang, J. Wang, J. Wang, K. Wang, L. Wang, Q. Wang, S. Wang, S. Wang, S. Wang, W. Wang, X. Wang, X. Wang, Y. Wang, Y. Wang, Y. Wang, Y. Wang, Y. Wang, Y. Wang, Z. Wang, Z. Wang, Z. Wang, Z. Wang, Z. Wang, Z. Wang, C. Wei, M. Wei, C. Wen, Z. Wen, C. Wu, H. Wu, J. Wu, R. Wu, W. Wu, Y. Wu, Y. Wu, Y. Wu, Z. Wu, C. Xiao, J. Xie, X. Xie, Y. Xie, Y. Xin, B. Xing, B. Xu, J. Xu, J. Xu, J. Xu, L. H. Xu, L. Xu, S. Xu, W. Xu, X. Xu, X. Xu, Y. Xu, Y. Xu, Y. Xu, Z. Xu, Z. Xu, J. Yan, Y. Yan, G. Yang, H. Yang, J. Yang, K. Yang, N. Yang, R. Yang, X. Yang, X. Yang, Y. Yang, Y. Yang, Y. Yang, Z. Yang, Z. Yang, Z. Yang, H. Yao, D. Ye, W. Ye, Z. Ye, B. Yin, C. Yu, L. Yu, T. Yu, T. Yu, E. Yuan, M. Yuan, X. Yuan, Y. Yue, W. Zeng, D. Zha, H. Zhan, D. Zhang, H. Zhang, J. Zhang, P. Zhang, Q. Zhang, R. Zhang, X. Zhang, Y. Zhang, Y. Zhang, Y. Zhang, Y. Zhang, Y. Zhang, Y. Zhang, Y. Zhang, Y. Zhang, Y. Zhang, Y. Zhang, Z. Zhang, C. Zhao, F. Zhao, J. Zhao, S. Zhao, X. Zhao, Y. Zhao, Z. Zhao, H. Zheng, R. Zheng, S. Zheng, T. Zheng, J. Zhong, L. Zhong, W. Zhong, M. Zhou, R. Zhou, X. Zhou, Z. Zhou, J. Zhu, L. Zhu, X. Zhu, Y. Zhu, Z. Zhu, J. Zhuang, W. Zhuang, Y. Zou, and X. Zu
  Kimi k2.5: visual agentic intelligence.
  External Links: 2602.02276,
  [Link](https://arxiv.org/abs/2602.02276)
  Cited by: [Table 5](#A2.T5.4.5.1.1.1 "In Appendix B Construction Settings ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§4](#S4.SS0.SSS0.Px1.p1.1 "Model Roles and Verification Settings. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Team (2026)
  Q. Team
  Qwen3.5: towards native multimodal agents.
  External Links: [Link](https://qwen.ai/blog?id=qwen3.5)
  Cited by: [Table 5](#A2.T5.4.2.1.1.1 "In Appendix B Construction Settings ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 5](#A2.T5.4.6.1.1.1 "In Appendix B Construction Settings ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§1](#S1.p1.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§1](#S1.p6.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§4](#S4.SS0.SSS0.Px1.p1.1 "Model Roles and Verification Settings. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.23.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.24.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.25.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.28.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.31.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§6.1](#S6.SS1.SSS0.Px1.p1.1 "Setup. ‣ 6.1 Main Results ‣ 6 Experiments on ZoomGain Training Data ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Team et al. (2025)
  V. Team, W. Hong, W. Yu, X. Gu, G. Wang, G. Gan, H. Tang, J. Cheng, J. Qi, J. Ji, L. Pan, S. Duan, W. Wang, Y. Wang, Y. Cheng, Z. He, Z. Su, Z. Yang, Z. Pan, A. Zeng, B. Wang, B. Chen, B. Shi, C. Pang, C. Zhang, D. Yin, F. Yang, G. Chen, J. Xu, J. Zhu, J. Chen, J. Chen, J. Chen, J. Lin, J. Wang, J. Chen, L. Lei, L. Gong, L. Pan, M. Liu, M. Xu, M. Zhang, Q. Zheng, S. Yang, S. Zhong, S. Huang, S. Zhao, S. Xue, S. Tu, S. Meng, T. Zhang, T. Luo, T. Hao, T. Tong, W. Li, W. Jia, X. Liu, X. Zhang, X. Lyu, X. Fan, X. Huang, Y. Wang, Y. Xue, Y. Wang, Y. Wang, Y. An, Y. Du, Y. Shi, Y. Huang, Y. Niu, Y. Wang, Y. Yue, Y. Li, Y. Zhang, Y. Wang, Y. Wang, Y. Zhang, Z. Xue, Z. Hou, Z. Du, Z. Wang, P. Zhang, D. Liu, B. Xu, J. Li, M. Huang, Y. Dong, and J. Tang
  GLM-4.5v and glm-4.1v-thinking: towards versatile multimodal reasoning with scalable reinforcement learning.
  External Links: 2507.01006,
  [Link](https://arxiv.org/abs/2507.01006)
  Cited by: [Table 2](#S5.T2.8.20.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Tong et al. (2024a)
  S. Tong, E. Brown, P. Wu, S. Woo, M. Middepogu, S. C. Akula, J. Yang, S. Yang, A. Iyer, X. Pan, A. Wang, R. Fergus, Y. LeCun, and S. Xie
  Cambrian-1: a fully open, vision-centric exploration of multimodal llms.
  External Links: 2406.16860
  Cited by: [§6.1](#S6.SS1.SSS0.Px1.p1.1 "Setup. ‣ 6.1 Main Results ‣ 6 Experiments on ZoomGain Training Data ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Tong et al. (2024b)
  S. Tong, Z. Liu, Y. Zhai, Y. Ma, Y. LeCun, and S. Xie
  Eyes wide shut? exploring the visual shortcomings of multimodal llms.
  External Links: 2401.06209
  Cited by: [§6.1](#S6.SS1.SSS0.Px1.p1.1 "Setup. ‣ 6.1 Main Results ‣ 6 Experiments on ZoomGain Training Data ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Wang et al. (2025a)
  H. Wang, X. Li, Z. Huang, A. Wang, J. Wang, T. Zhang, J. Zheng, S. Bai, Z. Kang, J. Feng, Z. Wang, and Z. Zhang
  Traceable evidence enhanced visual grounded reasoning: evaluation and methodology.
  arXiv preprint arXiv:2507.07999.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§2](#S2.SS0.SSS0.Px1.p1.1 "Fine-grained perception benchmarks. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 1](#S4.T1.16.1.6.1 "In Training Data Selection and Matching. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§6.1](#S6.SS1.SSS0.Px1.p1.1 "Setup. ‣ 6.1 Main Results ‣ 6 Experiments on ZoomGain Training Data ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Wang et al. (2025b)
  W. Wang, L. Ding, M. Zeng, X. Zhou, L. Shen, Y. Luo, W. Yu, and D. Tao
  Divide, conquer and combine: a training-free framework for high-resolution image perception in multimodal large language models.
  In Proceedings of the AAAI Conference on Artificial Intelligence,
  Vol. 39, pp. 7907–7915.
  Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Fine-grained perception benchmarks. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 1](#S4.T1.16.1.4.1 "In Training Data Selection and Matching. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§6.1](#S6.SS1.SSS0.Px1.p1.1 "Setup. ‣ 6.1 Main Results ‣ 6 Experiments on ZoomGain Training Data ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* [47]
  W. Wang, Y. Jing, L. Ding, Y. Wang, L. Shen, Y. Luo, B. Du, and D. Tao
  Retrieval-augmented perception: high-resolution image perception meets visual rag.
  In Forty-second International Conference on Machine Learning,
  External Links: [Link](https://arxiv.org/abs/2503.01222)
  Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Improving fine-grained perception. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Wei et al. (2026)
  L. Wei, L. He, J. Lan, L. Dong, Y. Cai, S. Li, H. Zhu, W. Wang, L. Kong, Y. Wang, et al.
  Zooming without zooming: region-to-image distillation for fine-grained multimodal perception.
  arXiv preprint arXiv:2602.11858.
  Cited by: [Appendix F](#A6.p1.1 "Appendix F ZoomGainBench Evaluation Settings ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Appendix G](#A7.SS0.SSS0.Px1.p1.1 "Training. ‣ Appendix G Training and Evaluation Settings ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Figure 1](#S1.F1 "In 1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§1](#S1.p2.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§1](#S1.p3.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§1](#S1.p6.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§2](#S2.SS0.SSS0.Px1.p1.1 "Fine-grained perception benchmarks. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§2](#S2.SS0.SSS0.Px2.p1.1 "Improving fine-grained perception. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§4](#S4.SS0.SSS0.Px2.p1.1 "Data Generation and Benchmark Curation. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 1](#S4.T1.16.1.2.1 "In Training Data Selection and Matching. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.14.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.17.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§6.1](#S6.SS1.SSS0.Px1.p1.1 "Setup. ‣ 6.1 Main Results ‣ 6 Experiments on ZoomGain Training Data ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Wu and Xie (2023)
  P. Wu and S. Xie
  V\*: guided visual search as a core mechanism in multimodal llms.
  arXiv preprint arXiv:2312.14135.
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§2](#S2.SS0.SSS0.Px1.p1.1 "Fine-grained perception benchmarks. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§2](#S2.SS0.SSS0.Px2.p1.1 "Improving fine-grained perception. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 1](#S4.T1.16.1.3.1 "In Training Data Selection and Matching. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§6.1](#S6.SS1.SSS0.Px1.p1.1 "Setup. ‣ 6.1 Main Results ‣ 6 Experiments on ZoomGain Training Data ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Xia et al. (2018)
  G. Xia, X. Bai, J. Ding, Z. Zhu, S. Belongie, J. Luo, M. Datcu, M. Pelillo, and L. Zhang
  DOTA: a large-scale dataset for object detection in aerial images.
  In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR),
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Xiaomi (2025)
  L. Xiaomi
  MiMo-vl technical report.
  External Links: 2506.03569,
  [Link](https://arxiv.org/abs/2506.03569)
  Cited by: [Table 2](#S5.T2.8.19.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Yuan et al. (2026)
  Q. Yuan, J. Lou, X. Yu, H. Lin, L. Sun, X. Han, and Y. Lu
  Vision-opd: learning to see fine details for multimodal llms via on-policy self-distillation.
  arXiv preprint arXiv:2605.18740.
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§2](#S2.SS0.SSS0.Px2.p1.1 "Improving fine-grained perception. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.15.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.16.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Yue et al. (2025)
  X. Yue, T. Zheng, Y. Ni, Y. Wang, K. Zhang, S. Tong, Y. Sun, B. Yu, G. Zhang, H. Sun, Y. Su, W. Chen, and G. Neubig
  MMMU-pro: a more robust multi-discipline multimodal understanding benchmark.
  In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), W. Che, J. Nabende, E. Shutova, and M. T. Pilehvar (Eds.),
  Vienna, Austria, pp. 15134–15186.
  External Links: [Link](https://aclanthology.org/2025.acl-long.736/),
  [Document](https://dx.doi.org/10.18653/v1/2025.acl-long.736),
  ISBN 979-8-89176-251-0
  Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Fine-grained perception benchmarks. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§3.3](#S3.SS3.p1.1 "3.3 Quality Verification and Multi-Source Distractors ‣ 3 ZoomGain Data Construction Pipeline ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Zhang et al. (2026a)
  K. Zhang, Y. Li, S. Shao, Q. Li, Z. Lu, Z. Yao, J. Lin, W. Jiao, Y. Lu, W. Liu, et al.
  VAD: attributing visual evidence for target reconstruction in multimodal on-policy distillation.
  arXiv preprint arXiv:2607.28590.
  Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Improving fine-grained perception. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Zhang et al. (2026b)
  L. Zhang, J. Yu, H. Xiong, P. Hu, Y. Zhuge, H. Lu, and Y. He
  Finers: fine-grained reasoning and segmentation of small objects with reinforcement learning.
  Advances in Neural Information Processing Systems 38, pp. 67403–67426.
  Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Fine-grained perception benchmarks. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 1](#S4.T1.16.1.7.1 "In Training Data Selection and Matching. ‣ 4 Implementation Details and Data Preparation ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Zhang et al. (2025)
  Y. Zhang, X. Lu, S. Yin, C. Fu, W. Chen, X. Hu, B. Wen, K. Jiang, C. Liu, T. Zhang, H. Fan, K. Chen, J. Chen, H. Ding, K. Tang, Z. Zhang, L. Wang, F. Yang, T. Gao, and G. Zhou
  Thyme: think beyond images.
  External Links: 2508.11630,
  [Link](https://arxiv.org/abs/2508.11630)
  Cited by: [§2](#S2.SS0.SSS0.Px2.p1.1 "Improving fine-grained perception. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.10.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Zhang et al. (2024)
  Y. Zhang, H. Zhang, H. Tian, C. Fu, S. Zhang, J. Wu, F. Li, K. Wang, Q. Wen, Z. Zhang, et al.
  MME-realworld: could your multimodal llm challenge high-resolution real-world scenarios that are difficult for humans?.
  arXiv preprint arXiv:2408.13257.
  Cited by: [§2](#S2.SS0.SSS0.Px1.p1.1 "Fine-grained perception benchmarks. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§6.1](#S6.SS1.SSS0.Px1.p1.1 "Setup. ‣ 6.1 Main Results ‣ 6 Experiments on ZoomGain Training Data ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Zheng et al. (2026)
  Z. Zheng, M. Yang, J. Hong, C. Zhao, G. Xu, L. Yang, and C. Shen
  Deepeyes: incentivizing" thinking with images" via reinforcement learning.
  In International Conference on Learning Representations,
  Vol. 2026, pp. 126775–126798.
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [§2](#S2.SS0.SSS0.Px2.p1.1 "Improving fine-grained perception. ‣ 2 Related Work ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision"),
  [Table 2](#S5.T2.8.9.1 "In Statistics. ‣ 5 Experiments on ZoomGain Bench ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").
* Zhu et al. (2025)
  J. Zhu, W. Wang, Z. Chen, Z. Liu, S. Ye, L. Gu, H. Tian, Y. Duan, W. Su, J. Shao, et al.
  Internvl3: exploring advanced training and test-time recipes for open-source multimodal models.
  arXiv preprint arXiv:2504.10479.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ ZoomGain: Mining Global-to-Zoom Perception Gaps for Fine-Grained Visual Supervision").

## 附录 A 完整算法与补充实现细节

[第 3 节](#S3)描述了核心流程。这里我们补充两项实现细节，二者已并入[算法 1](#alg1)。模型分工与阈值见[附录 B](#A2)；提示词汇总于[附录 J](#A10)。

#### 拉近视图中的锚点标记。

扩展后的裁剪图 $V_{z}^{i}$ 可能包含多个属于锚点类别的物体。一个 VLM 枚举这些实例（包括部分可见的实例），并把选定锚点与其定位框匹配。若存在多个实例，我们在锚点本身周围画一个红色矩形；若只有一个实例，裁剪图保持无标记。该矩形不同于 $b_{i}$——后者在全局视图中标记整个裁剪区域。带标记视图的描述提示词仅用它来识别锚点，其余方面遵循无标记视图的指令。不得把它描述为拍摄内容，也不得把它用作答案。局部问题可以引用该标记；全局问题使用自然的指代表达式。[图 4](#A1.F4)展示了这两种情况。

#### 裁剪图/整幅图像的联合审查与改写。

QA 生成之后，EDGE\_REWRITER 检查裁剪图与标有 $b_{i}$ 的整幅照片，以及两种问题形式与参考答案。它检查承载答案的文本或物体是否延伸出裁剪图、全局指称对象是否唯一、两种问题是否给出相同答案，并返回 *keep*、*rewrite* 或 *drop*。有界改写可以添加在两个视图中均有效、且不泄露答案的限定语，同时保留非 OCR 答案。对 OCR，它可以把问题与答案收窄到原始答案中包含的一个完整文本块或指定前缀/后缀，但不得添加从整幅图像读出的文本。所请求集合延伸到裁剪图之外的计数问题会被丢弃。修订会在局部/全局问题与中英文问题之间同步；在基于裁剪的验证（[第 3.3 节](#S3.SS3)）之前，会再次检查目标与答案约束。锚点枚举与这一审查都使用 Qwen3.5-397B-A17B。

![Refer to caption](2611.14076v1/anchor_marker_examples.png)

图 4：拉近视图中的条件式锚点标记。(a) 画面中有两个人，包括左侧部分可见的人；红色矩形选中披红黑格纹披肩的人。(b) 画面中只有一个人，因此不加标记。两种视图均由原始图像渲染，并使用流程的标记与缩放函数记录裁剪/锚点坐标。矩形标识的是锚点，而非承载答案的细节；它只用于拉近视图，不属于拍摄场景。

算法 1　ZoomGain 数据构建

```
 1: 输入：图像池 I；已配置模型；每个模型 N = 10 个采样；R = 3 轮 MCQ 验证
 2: 输出：经过验证的 QA 数据集 D，含证据区域与干扰项来源
 3: D ← ∅
 4: for 每张整幅图像 V_g ∈ I do
 5:   C_g ← SceneCaption(V_g); E ← ProposeAnchors(C_g)
 6:   for 每个指代表达式 e_i ∈ E do
 7:     // 锚点发现与定位
 8:     B_i ← GroundIndependently(V_g, e_i)
 9:     if ¬ValidGrounding(B_i, 0.5) then continue
10:     b_i ← Expand(median_coord(B_i)); V_z^i ← Crop(V_g, b_i)
11:     L_i ← EnumerateAnchorInstances(V_z^i, e_i)
12:     if 没有实例与已定位锚点匹配 then continue
13:     Ṽ_z^i ← MarkAnchorIfMultiple(V_z^i, L_i)
14:     // 全局到拉近的证据与 QA 构建
15:     V_g^i ← DrawBox(V_g, b_i)
16:     C_g^i ← M_cap(V_g^i, b_i); C_z^i ← M_cap(Ṽ_z^i)  // 独立调用
17:     Δ_i ← IncrementalFacts(C_g^i, C_z^i)
18:     (q_local^i, q_global^i, a_i, t_i) ← GenerateQA(Δ_i, e_i, L_i)
19:     if 未生成有支持且无歧义的 QA then continue
20:     (v, q_local^i, q_global^i, a_i) ← EdgeAuditAndRewrite(Ṽ_z^i, V_g^i, q_local^i, q_global^i, a_i)
21:     if v = drop 或改写后约束不满足 then continue
22:     // 质量验证与多源干扰项
23:     A_crop ← Sample(crop, Ṽ_z^i, q_local^i, N)
24:     if min_m Correct(A_crop^m, a_i) < 6 then continue
25:     A_blind ← Sample(blind, ∅, q_global^i, N)
26:     if min_m Correct(A_blind^m, a_i) ≥ 3 then continue
27:     O_i ← ∅; S_i ← ∅
28:     if t_i = attribute then
29:       A_global ← Sample(global, V_g, q_global^i, N)
30:       D_v ← VisualAlternatives(V_g, Ṽ_z^i, q_local^i, q_global^i, a_i)
31:       D_b ← Incorrect(A_blind, a_i); D_g ← Incorrect(A_global, a_i)
32:       (O_i, S_i) ← CurateOptions(a_i, D_v, D_b, D_g)
33:       verified ← false
34:       for r = 1, …, R do
35:         A_mcq ← Sample(mcq, Ṽ_z^i, (q_local^i, q_global^i, O_i), N)
36:         if min_m Correct(A_mcq^m, a_i) ≥ 6 then
37:           verified ← true; break
38:         end if
39:         if r < R then (O_i, S_i) ← RepairDistractors(O_i, S_i)
40:       end for
41:       if ¬verified then continue
42:     end if
43:     D ← D ∪ {(V_g, V_z^i, b_i, q_local^i, q_global^i, a_i, t_i, O_i, S_i)}
44:   end for
45: end for
46: return D
```

#### 记号与操作。

$L_{i}$ 记录锚点实例；$\widetilde{V}_{z}^{i}$ 是可选的带标记拉近视图。EdgeAuditAndRewrite 返回判定 $v$，以及在上述约束下保留或修订的 QA。两种问题形式都有英文与中文版本。其余操作遵循[第 3 节](#S3)，验证设置见[附录 B](#A2)；$S_{i}$ 在修复过程中保留干扰项来源。

## 附录 B 构建设置

[表 5](#A2.T5)给出了[第 4 节](#S4)所述 ZoomGain 流程的完整模型分工。

表 5：ZoomGain 构建流程中的模型分工。

| 模型 | 角色 |
| --- | --- |
| Qwen3.5-397B-A17B [Team (2026)](#bib.bib2) | 初始全局场景描述与成对视图描述（$M_{\mathrm{cap}}$）；定位；裁剪图锚点枚举；裁剪图/整幅图像联合审查与改写；盲答；全局视图错误收集；视觉干扰项生成；最终 MCQ 验证。 |
| GLM-5.2 [GLM-5-Team et al. (2026)](#bib.bib3) | 增量事实抽取与 QA 生成。 |
| Qwen3-VL-235B-A22B-Instruct [Bai et al. (2025)](#bib.bib5) | 定位；基于裁剪的验证；盲答；全局视图错误收集；最终 MCQ 验证。 |
| Kimi-K2.6 [Team et al. (2026b)](#bib.bib4) | 定位；基于裁剪的验证；盲答；全局视图错误收集；最终 MCQ 验证。 |
| Qwen3.5-122B-A10B [Team (2026)](#bib.bib2) | 答案等价判断。 |
| DeepSeek-V4-Pro [DeepSeek-AI (2026)](#bib.bib6) | 候选干扰项聚类与选项池整理。 |

#### 验证阈值。

所有验证阶段对每个模型采样 10 个答案。基于裁剪的验证要求其两个模型 Qwen3-VL-235B-A22B-Instruct 与 Kimi-K2.6 各自至少给出 6 个正确答案。盲验证仅当三个模型各自至少答对 3 次时才拒绝该问题。最终 MCQ 验证要求其三个模型各自至少 6 次正确选择。

#### 验证轮次与干扰项修复。

最终 MCQ 验证最多使用三轮：初始检查，随后在干扰项修复后最多再进行两次检查。每轮都施加上述逐模型阈值。最后一轮后仍失败的候选被丢弃。

## 附录 C 基准问题类别

ZoomGainBench 的三类问题覆盖以下细粒度细节。[图 5](#A3.F5)–[图 7](#A3.F7)每类展示三个示例，并附英文与中文对照问题。橙色框标出回答每道题所需的特定细节，虚线把它们与放大视图相连。这些框为示意而选取，不同于流程中的锚点框。

#### 属性识别。

问题涉及目标的颜色、材质、形状、物体身份、动作或关系。下面示例询问卡车的后视镜外壳、玻璃桌面，以及高尔夫球手遮阳帽上的一个小标志。

![Refer to caption](2611.14076v1/benchmark_cases_attribute.png)

图 5：属性识别示例。(a) 后视镜外壳颜色；(b) 桌面材质；(c) 标志形状。正确答案及其对应选项以绿色高亮。

#### 计数。

问题询问实体、物体部件或重复图案的数量。下面示例涵盖菜单上的重复图像、长椅上就座的人，以及衬衫上的口袋。

![Refer to caption](2611.14076v1/benchmark_cases_counting.png)

图 6：计数示例。(a) 菜单上的八张汉堡图片；(b) 候车亭内就座的三个人；(c) 衬衫上的两个胸袋。每道题都要求开放式的数值答案。

#### 文本识别（OCR）。

问题要求转写标牌、车辆、衣物、印刷材料和商品标签上的文字。下面示例包括一块道路标志、卡车上的日文字样，以及瓶子标签上的中文文字。无论问题语言如何，答案都保留图像中可见的原文。

![Refer to caption](2611.14076v1/benchmark_cases_ocr.png)

图 7：文本识别示例。(a) 一块辅助道路标志；(b) 卡车后门上的字样；(c) 瓶子标签上最大的中文文字。参考转写以绿色显示。

## 附录 D 补充错误分析

本节补充[第 5.2 节](#S5.SS2)。

#### 逐模型一致性。

每个受评模型都过度选择全局视图错误：它们获得各模型错误选择的 65.0–78.2%，而在每题干扰项中均匀选择时的期望值为 52.3–57.8%。对于未参与构建基准的四个闭源模型，这一比例为 75.7%，期望值为 57.4%。这些模型选择某个全局视图错误的比率也随其在构建期间出现的频繁程度上升：当它在 30 个整幅图像答案中被给出一两次时为 13.4%，被给出超过十次时为 35.2%。

#### 控制选项位置。

模型偏好某些选项位置。按各选项位置的平均选择率归一化后，全局视图错误仍被选择的频率是期望值的 1.34 倍；当它们同时与盲猜重合时为 1.46 倍；而盲猜与视觉证据分别为 0.52 倍与 0.55 倍。

#### Qwen3-VL-8B 的低于随机准确率。

Qwen3-VL-8B 对属性问题的答案中只有 1.5% 无法解析，因此其低于随机的准确率并非源于格式失败。相反，其错误选择中有 67.5% 落在全局视图错误上，期望值为 54.0%。它的回答通常声称仔细检查了目标，然后给出一个貌似合理但错误的属性，例如把深蓝色背包描述为黑色。

#### 开放式问题上的错误。

计数错误大多是「差一点」：71.6% 的错误数值答案恰好偏差 1，而 94 道计数题中有 67 道的真值不超过三，因此难点在于分辨少量小实例，而非枚举大量物体。对 OCR，在未获满分的转写中，29.1% 仍接近参考，字符级相似度至少为 0.5；10.1% 遗漏了目标文本的一部分或包含相邻文本；至少 13.4% 转写了场景中的其他文本而非目标文本——这是通过把预测与构建期间生成的场景描述匹配识别出来的。其余转写大多与参考几乎没有相似之处。

## 附录 E 代表性失败案例

[图 8](#A5.F8)展示了[第 5.2 节](#S5.SS2)讨论的代表性失败案例。

![Refer to caption](2611.14076v1/error_cases.png)

图 8：ZoomGainBench 上的代表性失败案例。每个案例展示整幅图像（所问细节以红框标出）、该区域的放大视图，以及 56 次评测（28 个模型 × 2 种语言）的响应。(a) 几乎所有评测都说出 Bauer——一个冰球装备品牌——而不是 NHL 标志，而盲猜（Reebok、Nike）从未被选中。(b) 白色托特包被当成塑料袋；从她肩上的黑包和另一名行人的钱包中提取的视觉证据干扰项从未被选中。(c) 多数评测（46/56）把卡车仪表盘上的白色物体说成橙色，这很可能是卡车前方工人所穿背心的颜色。(d) 醒目的反射剪影把选择从桅杆底部较小的起重机上引开。

## 附录 F ZoomGainBench 评测设置

所有非智能体模型都使用与 ZwZ（[Wei et al. (2026)](#bib.bib1)）相同的系统提示词：要求模型先推理，再把最终答案放入 `<answer>` 与 `</answer>` 标签之间。用户消息包含整幅图像以及问题（如适用，还包含选项）。计数题额外要求使用阿拉伯数字；OCR 题只要求在答案标签内给出转写，并保留大小写、空格、标点与符号。中文版本替换问题题干，但保留选项与格式指令。

Qwen 系列模型、ZwZ 与 Vision-OPD 使用温度 0、最大输出长度 2,048 token，并通过 `enable_thinking=false` 关闭原生思考。MiMo-VL-7B-RL 使用相同温度与输出上限，并在问题后追加 `/no_think`。GLM-4.6V 与 GLM-5.3-Flash 使用温度 0，输出上限分别为 4,096 与 8,192 token；其请求同样设置 `enable_thinking=false`。Kimi-K3 在开启思考、温度 0、输出上限 8,192 token 下评测。GPT-5.5、GPT-5.6-Sol、Gemini-3.6-Flash 与 Claude-Opus-5 使用 4,096 token 的输出上限，温度与思考模式保留服务商默认值。

四个智能体模型使用其原生推理与工具调用提示词，进行多轮图像交互，温度均为 0。每轮输出上限为：DeepEyes 与 PixelReasoner 10,240 token，DeepEyesV2 20,480 token，Thyme 2,048 token。每道题的总输出预算为 32,768 token。DeepEyes、DeepEyesV2 与 PixelReasoner 最多允许 11 轮，Thyme 允许 5 轮；除 PixelReasoner 允许 4 次外，其余工具调用上限均为 10 次。与原生智能体协议冲突的通用答案格式指令会被移除。

## 附录 G 训练与评测设置

#### 训练。

两个数据集都使用 GRPO 进行直接 RL 训练：批大小 64，每题 8 次 rollout，训练一个 epoch（140 步），并评测第 140 步的检查点。对 ZwZ 与 ZoomGain，我们都使用 $10^{-6}$ 的学习率、无 KL 正则化、最大响应长度 2,046 token。ZwZ 图像保留其原生边界框叠加，而 ZoomGain 使用原始图像。对 ZwZ，我们遵循官方奖励定义（[Wei et al. (2026)](#bib.bib1)）。对 ZoomGain，奖励遵循 ZoomGainBench 的计分规则：多项选择题与计数题分别在所选选项或预测整数精确匹配时给予奖励 1，否则为 0。OCR 题若 ANLS 分数不低于 $0.7$ 则以该分数为奖励，否则为 0。

#### 评测。

对训练实验，所有模型都在思维链提示与温度 0 下评测。在同一基准内，基座模型与训练模型共享相同的提示配置与输出上限：除 BabyVision、PerceptionBench 与 O3-Bench 使用 8,192 token 并由 GPT-5.5 作为答案评判模型计分外，其余基准均为 2,048 个新 token。MMVP 按成对准确率计分，CV-Bench 按其官方均衡得分计分，MME-RealWorld 在 1,919 道题上评测。VisualProbe 报告其简单（141）、中等（268）与困难（106）三个划分按问题数加权的平均值。

## 附录 H 全局到拉近的证据与 QA 构建示例

[图 9](#A8.F9)–[图 11](#A8.F11)展示了[第 3.2 节](#S3.SS2)中三类问题的构建过程。每个示例展示成对视图与描述摘录、原始增量事实列表中的部分条目，以及一条事实如何先形成局部 QA 对、再形成全局 QA 对。绿色文字标出拉近视图描述中新描述的细节；紫色文字高亮局部与全局目标指代。拉近视图使用流程的原始裁剪图。

![Refer to caption](2611.14076v1/dual_caption_attribute.png)

图 9：属性 QA 构建示例。全局视图描述提到遮阳帽上的标志，但没有说明其形状。拉近视图描述识别出一个小的星形标志。该事实支持一道形状问题；问题随后用全局指代表达式改写，同时保留答案。

![Refer to caption](2611.14076v1/dual_caption_counting.png)

图 10：计数 QA 构建示例。全局视图描述提到数字菜单板上的食物图片，但没有给出数量。拉近视图描述识别出八张排成两行、每行四张的汉堡图片。所选事实产生一道在两种视图中答案相同的计数问题。

![Refer to caption](2611.14076v1/dual_caption_ocr.png)

图 11：OCR QA 构建示例。全局视图描述提到一个带蓝色标签的瓶子，但没有转写其文字。拉近视图描述读出标签上的中文字符。所选文本事实支持一道局部 OCR 问题；问题随后被改写为在整幅图像中标识该瓶子，同时保留原始转写作为答案。

## 附录 I 质量验证示例

[图 12](#A9.F12)与[图 13](#A9.F13)展示了被[第 3.3 节](#S3.SS3)两个验证阶段拒绝的候选 QA 对。基于裁剪的验证检查图像是否支持生成的参考答案，盲验证则过滤掉答案无需图像即可预测的问题。所有问题、候选答案与投票计数均取自原始生成记录。

![Refer to caption](2611.14076v1/crop_verifier_rejections.png)

图 12：被基于裁剪的验证拒绝的示例。描述错误地把 (A) 赛车上的数字说成「3」而非「8」，把 (B) 门把手说成银色而非白色。两个验证模型在全部 10 次采样中都给出视觉上支持的答案，与生成的参考答案零匹配，未达到 6/10 阈值。原始裁剪输入没有红色锚点标记；橙色框与放大细节仅为展示而添加。

![Refer to caption](2611.14076v1/blind_verifier_rejections.png)

图 13：被盲验证拒绝的示例。参考答案 (A) 鸡腿与 (B) 蒸汽得到图像支持，但也能仅凭问题预测。在无图像情况下，三个模型分别总共获得 30/30 与 29/30 的参考匹配，每个模型都达到至少 3/10 匹配的拒绝阈值。图像与蓝色裁剪框仅为读者展示；盲答模型不接收任何图像。

## 附录 J 数据构建中使用的提示词

本节给出[第 3 节](#S3)所述角色所用的提示词，以及[附录 A](#A1)中的锚点枚举、带/不带标记的拉近视图描述与 EDGE\_REWRITER。模板取自 `zoom_inc_pipeline/prompts.py`；依赖视图的指令块取自 `pipeline.py` 中的调用方。`{anchor}`、`{question}`、`{reference}` 等样本相关占位符在运行时填充。JSON 花括号按字面花括号显示，而非 Python 字符串转义。形如 `<<<INSERT: NAME>>>` 的行表示在此处精确插入下方的同名块，使共享指令只打印一次而不省略其内容。插入记号仅用于展示，不会发送给模型。

【译者注：以下提示词原文为英文。为便于中文读者理解，正文按原意译出，但提示词标识符（如 SPATIAL\_FRAME\_RULES）、占位符、JSON 字段名以及作为指令示例的英文措辞保留原文；实际使用时请以论文原文的英文提示词为准。】

#### 视图相关输入。

CAPTION1 接收标出裁剪区域的整幅图像。CAPTION2 接收无标记的拉近视图，而 CAPTION2\_ANCHOR\_MARKED 在同一描述模板前添加标记专用指令。QA 生成中的局部锚点规则依据拉近视图是否有锚点标记来选择。EDGE\_REWRITER 接收裁剪图与标出其裁剪区域的整幅图像；裁剪图上的候选框还可以额外定位正在审查的指称对象。裁剪求解器回答局部问题；整幅图像求解器与盲求解器回答全局问题，盲答不提供图像。Kimi 格式指令追加到其开放答案请求中。视觉干扰项生成使用相应的裁剪图/整幅视图规则。MCQ 验证会看到裁剪图、局部问题、作为上下文的全局问题以及组装好的选项。

### J.1 共享指令

#### SPATIAL\_FRAME\_RULES。

空间坐标系契约——适用于你读到或写下的每一个方向词：

- 物体之间的 LEFT/RIGHT 使用图像的观察者坐标系：「the person to the left of the sign」指观察者看到的左侧。在定位一个物体相对于另一个物体的位置时，绝不要按参考物体自身的左右做镜像计算。当这类短语承担关键信息时，优先使用明确措辞，例如「on the left side of the image」。

- BODY PARTS 是解剖学意义，绝不相对观察者：「right hand」始终指该人自己的右手。侧面须由人物朝向推导，而不是由图像原始位置推导：面向镜头 → 右手出现在观察者的左侧；背对镜头 → 右手出现在观察者的右侧；面向图像左侧 → 身体左侧朝向镜头；面向图像右侧 → 身体右侧朝向镜头。若朝向不清晰可见，绝不要使用左右身体部位措辞；改用其他方式标识该部位（依据它拿着或接触的东西，或使用明确的观察者措辞，如「the hand on the left side of the image」）。

- FRONT/BEHIND 绝不是深度词。场景深度只能写作「closer to the camera (than X)」/「farther from the camera (than X)」/「beyond X from the camera's viewpoint」。front/behind 仅保留给已说明朝向的人、动物与车辆的内在正/背面：「in front of the seated man」是他面朝与胸口朝向的一侧，「behind him」是他的背面，与到镜头的距离无关。

- DEPTH-FLIP TRAP（最常见的错误——逐句检查）：当镜头看到一个人的背面时，此人背对镜头，因此场景中更深的物体位于此人前方，而镜头与此人之间的物体位于他身后。对一个从背后看到的人，把在其更远处的标志写成「behind the man」是错误的——应写「in front of the man (farther from the camera)」或「farther from the camera than the man」。同一翻转也适用于背对镜头观看某物的就座人群。

- 对没有内在正面的物体（杆、箱、树、蜡烛、标牌），绝不使用 front/behind；使用镜头距离或图像位置措辞。

- VEHICLE AND BUILDING PARTS 使用固定在物体本身的部件术语：「the cab end」「the rear of the trailer」「the side facing the camera」「the entrance side」。除非是车辆真正的前端/驾驶室端，绝不要把车辆某一端称为「front」。

- 朝向无法确定的 GROUPS 与实体：使用观察者坐标系并明确写出图像措辞（「in the upper-left part of the image」「farther from the camera」），绝不使用内在术语。

- 「THE IMAGE」指谁的坐标系。图像坐标系措辞——「in the upper-left part of the image」「near the left edge of the image」「图像左侧」——始终指整幅照片，且不指任何其他东西。

#### CROP\_FRAME\_CAVEAT。

裁剪图坐标系警示：

- 你的视图是从更大照片中部切出的窗口，因此它的边界不是照片的边界，它的左侧也不是照片的左侧。从此视图读出的位置只能表述为相对该视图的局部位置，绝不能写成图像坐标系措辞。

- 坐标系侧面只有在靠近边缘时才诚实。「on the left side of the image」对位于照片外侧三分之一的物体才值得说；对更靠近中心的任何东西，这种说法等于声称物体不在其实际位置，而按该侧扫描的求解器将找不到它。当目标靠近中心时，改为相对一个具名物体定位——「just right of the fire hydrant」「in front of the bus shelter and a little to its left」——这种说法无论画面边界如何画都成立。你无法看到此裁剪图在照片中的位置，因此有疑问时优先使用具名物体。

- 坐标系最高级需要整幅照片。leftmost、rightmost、topmost、bottommost、far left、far right、最左、最右、最上、最下、最顶、最底 都在断言同类中再没有更靠外的，而只有看到整幅照片才能确立这一点。看不到整幅照片时，两种语言都不要这样写。一个具名宿主内部的有限最高级（「the bottom word on the blue sign」）不受影响。

- 宿主的某个角需要该角在视野内。「the bottom right corner of the window」「the top of the sign」「货架最下层」命名的是另一物体内部的位置，只有当该物体在该侧的边缘在此可见时才成立。当宿主延伸出边界时，你看到的角是裁剪图的角，而不是宿主的角，该短语在整幅照片中指向的完全是别的东西：一个被裁到最上两层的书柜会使「the book at the bottom of the bookcase」指第二层的绿色书脊，而书柜真正的底层放的是一本红色的书。只有当你看到宿主在该侧的终点时才使用此类短语；否则通过它附着于什么、旁边是什么，或它自身可见的属性来标识。

#### KIMI\_FINAL\_ANSWER\_TAG。

以 `The answer is` 开头，然后只把最终答案放进 `<answer></answer>`。例如：`The answer is <answer>answer here</answer>`。

### J.2 场景描述与锚点定位

#### SCOUT\_CAPTION。

彻底描述这张图像。然后列出你能看到的每一个独立、可单独识别的物体或结构（建筑、船、车辆、人、标牌、雕像、门、桥等）。不要把天空、水、草地、植被或路面等背景材质列为物体。

方向措辞：给出图像坐标系中的每个位置（「on the left side of the image」「in the lower-right foreground」）。深度只用前景/背景/更靠近或更远离镜头表达。绝不要用人、动物或车辆的「in front of」或「behind」来表示更靠近或更远离镜头，也绝不要命名一个人自己的左右身体侧。

#### PHRASE\_REWRITE。

你正在为视觉定位模型准备指代表达式。

下面是一幅图像的描述。抽取至多 `{max_phrases}` 个候选地标物体，并把每个改写为自包含的英文指代短语，使看着图像的人能据此恰好挑出一个物体实例。

规则：

- 每个短语必须恰好指代一个物体实例。当裸名词可能匹配多个实例时，添加位置词（left / center / right、foreground / background）或颜色/尺寸属性。

- 短语中的位置词只能是图像坐标系词：left / center / right、upper / lower、foreground / background、closest to the camera。绝不要用「in front of」「behind」「ahead of」或「beyond」另一个物体或人来定位候选——深度意图有歧义，定位模型对此并不一致。绝不要使用一个人自己的左右身体侧，也绝不要通过描述将其置于明显不同深度的另一物体来定位一个物体。

- 只选具体的离散物体：建筑、船、车辆、标牌、塔、门、雕像、明确的人群。绝不选：天空、水、草、树、植被、路面、阴影、倒影、泛指人群。

- 短语只能依赖描述中可见的属性；不得杜撰。

- 绝不要把从图像中读到的文字、字母、标志或品牌名用作限定语（低分辨率下小字不可靠）。

- 只输出严格 JSON：

```
{"phrases": [{"phrase": "...", "head_noun": "...", "qualifier_type": "position|color|size|none"}]}
```

图像描述：

```
{caption}
```

#### GROUND\_NORM1000。

定位以下指称的对象：`"{phrase}"`

把短语中的 left/right/upper/lower/foreground/background 解释为观察者的图像坐标系，把 foreground/background 解释为到镜头的距离。

在相对于整幅图像宽高的 0 到 1000 整数坐标网格上测量 x 与 y。只返回一个紧致边界框，形式为：`[x1, y1, x2, y2]`

四个值都必须是 0 到 1000 之间的整数。包含被指对象的完整可见范围。若对象缺失或有歧义，返回 `[]`。不要输出任何其他文本。

#### GROUND\_NORM01。

定位以下指称的对象：`"{phrase}"`

把短语中的 left/right/upper/lower/foreground/background 解释为观察者的图像坐标系，把 foreground/background 解释为到镜头的距离。

在相对于整幅图像宽高的、0 到 1 的小数坐标上测量 x 与 y，其中 0 是左/上边缘，1 是右/下边缘。只返回一个用标签包裹的紧致边界框，形式为：

```
<bbox>[x1, y1, x2, y2]</bbox>
```

四个值都必须在 0 与 1 之间。包含被指对象的完整可见范围。若对象缺失或有歧义，返回 `<bbox>[]</bbox>`。不要输出任何其他文本。

### J.3 锚点枚举与成对视图描述

#### ANCHOR\_INSTANCE\_CHECK。

在这张图像裁剪图中，找出具体物体类别「{noun}」的每一个可见的独立实例。包括部分可见的实例。

对每个实例，只围绕其可见范围画一个紧致边界框。不要推断或包含被遮挡部分。使用从 0 到 1000 归一化的整数坐标，按 `[x1, y1, x2, y2]` 顺序。

只返回一个 JSON 对象，包含以下字段：

- `"count"`：一个非负整数，等于检测到的实例数。
- `"instances"`：一个 JSON 数组，恰好包含 `"count"` 个对象。

每个对象必须包含：

- `"bbox_2d"`：四个整数 `[x1, y1, x2, y2]`。
- `"description"`：简短、中性、不含答案的视觉描述。

以下一致性规则是强制的：

```
count == len(instances)
```

若没有可见实例，只返回：

```
{"count": 0, "instances": []}
```

仔细思考后再回答。只输出 JSON。不要使用 Markdown 代码围栏或添加解释。

#### CAPTION1。

你会看到一幅完整图像，其中一个矩形区域被红色高亮。

**只描述高亮区域内的视觉内容，绝不要提及图像其余部分。** 图像其余部分仅作为上下文使用。

流程已在该区域内预选了一个锚点物体（仅为定位元数据）：

`"{anchor}"`

以锚点为中心的组织方式（与拉近视图相同的约定）：把该锚点视为描述的主要参考点，而不是描述的排他范围。首先识别锚点并陈述在此尺度下可辨的它的每一项属性，然后覆盖其紧邻区域，再覆盖区域其余部分。只要视觉上支持，就相对该锚点表达其他物体的位置。锚点短语仅为定位元数据：除非你能在图像中独立看到，绝不要复制该短语中的属性、文字、计数或关系。若多个物体匹配该短语，逐一描述它们并说明指称有歧义；若无法确信定位指称对象，说明这一点并正常描述区域。锚点绝不缩小你的覆盖义务：区域内其他明显可见的东西仍必须描述。

你的描述定义了整幅图像视图能看到什么。后续阶段会把该描述与同一区域的拉近描述比较，并把任何你省略的属性视为「在整幅图像尺度下不可见」。拉近描述遵循与本描述相同的空间与纳入规则；两份描述之间唯一的预期差异是分辨率。因此，省略实际上明显可见的内容会污染比较。对此尺度下你能真正分辨的一切要详尽，对不能分辨的要明确说明。

详尽性契约（从大到小）：

- 对区域内每个大型或显著物体——尤其是人——陈述在此尺度下明显可辨的全部属性：衣物类型及其颜色（衬衫、裤子、连衣裙、帽子、鞋子）、物体颜色与材质、明显的姿态或动作、明显可识别的持有或附着物品，以及所描述物体之间的粗粒度空间关系。一个前景中的大人，如果衬衫颜色很明显，就必须说出该颜色。
- 然后以同样方式覆盖中等大小的物体。
- 对小物体与精细细节（小字、小物件、精确计数、细微图案、远处人脸），报告可辨内容，对其余部分明确说「unclear」或「not readable at this scale」。说「不清晰」是有价值的信号；默不作声地跳过则不是。
- 当多个不同物体各自的属性可见时，不要把它们压缩成一句含糊的总结。
- 当同一类别有多个实例（价签、标牌、窗户）时，把每个被描述的实例绑定到稳定的限定语——附着或最近物体关系、其在宿主上的部件位置，或明确的图像坐标系位置——而不是裸类别名词。

`<<<INSERT: SPATIAL_FRAME_RULES>>>`

人物朝向：在命名一个人自己的左右身体侧或某侧特定持有物之前，说明此人朝向，并按上述契约推导侧面。当此尺度下朝向不可辨时，使用观察者措辞（「the hand on the viewer's left」）或说明侧面不清晰；绝不猜测解剖学侧面。

矩形边缘策略（与拉近视图一致）：矩形边界是人为视口，不是拍摄场景内容。对跨越边界的离散物体，只应用以下一个分支：

- 若无法确信识别，或它没有任何完整部分位于区域内，则完全省略。
- 若它清晰可识别，且至少有一个部分在区域内完全可见，你可以只描述那些完全可见的部分及其可辨属性；对其小细节说「unclear」。绝不要对此类物体陈述整体属性、全身动作或总数，也绝不要描述区域外的部分，即使整幅图像显示了它——它不在本区域范围内。
- 绝不要在描述中任何地方提及裁切本身：不要用「partially visible」「cut off」或「at the edge」措辞。描述内部内容，对太小的事物说不清晰，对其余保持沉默。
- 当区域内包含相当大且有意义的场景表面或结构部分时，可以描述它们；不要描述其截断。

返回描述前，执行强制的删除检查：删除每一句提及矩形边界或物体被裁状态的句子。

若小细节在此尺度下无法辨认，明确说明不清晰。不要猜测不清晰的计数、文字、颜色或动作。

#### CAPTION2。

你会看到一张围绕某个选定锚点物体构建的图像裁剪图。

选定锚点物体（仅为定位元数据）：

`"{anchor}"`

写一段详细的自然语言描述，围绕该选定锚点及其可见邻域组织。把锚点视为主要参考点，而不是描述的排他范围。

覆盖范围与组织方式：

- 首先详细描述选定锚点本身，包括每一个清晰可见的部分、内容、标记、可读文字、颜色、属性、状态或属于它的动作。
- 然后描述图像中其他每一个清晰可见的物体与细节。不要仅仅因为某可靠视觉信息不属于锚点就省略它。
- 只要视觉上支持，就表达每个其他物体与锚点的关系，优先使用不依赖坐标系的表达：附着于它、包含于它、在其上、最靠近它，或在同一深度上位于其旁。需要方向词时，必须遵循下方的空间坐标系契约：物体之间的 left/right 是观察者的（写「to the viewer's left of the anchor」，绝不写锚点自身的 left/right）；above/below 是图像竖直方向；front/behind 只能用于命名已说明朝向的人、动物或车辆的内在侧面；任何深度差异都写作更靠近/更远离镜头。
- 若无法建立与锚点的可靠关系，仍可用该裁剪图内的中性位置描述可见物体。绝不要仅仅为了把它连到锚点而杜撰关系。
- DEPTH ZONES（强制）：该裁剪图是一个可能跨越非常不同场景深度的二维窗口。对你描述的每个非锚点物体，明确其与锚点的深度关系：处于锚点自身深度带、明显比锚点更靠近镜头，或明显更远离镜头。当一个物体在二维画面中看似靠近、但实际处于明显不同深度时，绝不要说它靠近、在旁或在锚点旁边（例如，围绕远处灯塔构建的裁剪图中的一个前景慢跑者，应写成「much closer to the camera than the lighthouse」，绝不是「near the lighthouse」）。
- 上面的锚点短语仅为定位元数据。除非在本图像中可独立看到，不要复制或假定该短语中的任何属性、文字、身份或全场景关系。

`<<<INSERT: SPATIAL_FRAME_RULES>>>` `<<<INSERT: CROP_FRAME_CAVEAT>>>`

人物朝向与手部（强制）：

- 在描述任何人的姿态、衣物侧面、持有物或身体部位侧面之前，说明此人朝向：面向镜头、背对镜头、面向图像左侧、面向图像右侧，或在无法确定时「facing unclear」。
- 姿态优先于侧面：当必须区分同一个人的两条肢体时，优先使用完全不需要侧向性的姿态或状态描述——抬起的手臂 vs. 垂在身侧的手臂、抓着带子的手、戴手套的手、搁在桌上的手臂。此类措辞对任何观察者都无歧义，且与朝向无关都成立。
- 只有当姿态描述无法区分肢体，且此分辨率下人物朝向明确无误（其脸或后背清楚可读——不是从几像素的头发或肩膀推断）时，才命名解剖学侧面。然后按坐标系契约从所述朝向推导侧面，并在括号中给出观察者侧的推导以便核查，例如：「He faces away from the camera; his right hand (on the viewer's right) holds a silver can.」
- 若朝向不明确无误，绝不写「left hand」或「right hand」：写姿态描述，或「one hand (laterality unclear)」加观察者坐标系位置。小或远的人正是自信断言侧面不安全的典型情形。
- 每当你描述一只手拿着什么时，同一次描述中也要交代另一只手：要么描述它明显拿着什么（或明显是空的），要么在 VISIBILITY AND REFERENCE NOTES 部分记录它不在视野内、内容未知。

重复物体的实例锁定：

- 当裁剪图显示、或可能延伸到同一类别的多个实例——价签、标签、标牌、屏幕、窗户、轮子、手、鞋、包及类似重复物品——绝不要把信息挂到裸类别名词上。把每个被描述的实例绑定到在整幅图像中仍然有效的稳定限定语：附着或最近物体关系（「the mug nearest the kettle」），或其在宿主上的部件位置（「on the tail of the aircraft」）。
- 此画面中的位置不是这样的限定语，也绝不算作限定语。该裁剪图是从更大照片中切出的窗口，其边界不是照片的边界：此处最左、最右或「on the left side」的任何东西，都可能位于整幅图像的正中或相反一侧。绝不要以任何措辞对任何事物写坐标系最高级——leftmost、rightmost、topmost、bottommost、far left、far right：你看不到裁剪图之外，因此无法知道其中任何东西是最靠外的。
- 当粗略位置确实有助于读者想象场景时，把它表述为相对本裁剪图的局部位置（「in the left part of this crop」），绝不要表述为关于图像的事实。没有附着或部件限定语的实例就不带限定语地描述，并记录在 VISIBILITY AND REFERENCE NOTES 部分，而不是用位置钉住。

包含有用的细节，例如物体、可读文字、颜色、属性、动作与空间关系。没有必需的 schema、项目符号格式或固定措辞；自然地组织描述。

让每一条陈述只基于本裁剪图中的视觉证据：

- HONEST EDGE REPORTING：裁剪图的四条外边缘是人为视口边界，不是拍摄场景内容。当物体被外边缘裁断（包括锚点）时，只说出你看到的：描述其清晰可见的部分及其属性，绝不要对此类物体陈述整体属性、全身动作、总数或整体形状/尺寸，也绝不猜测边缘之外继续的是什么。主体描述保持正面——写「确实可见」的内容——并把所有被裁/部分可见/不在视野内的说明放到末尾的 VISIBILITY AND REFERENCE NOTES 部分。连你都无法识别的截断物体只应放在该部分。
- 对文字，采用刻意保守的逐字符标准。一个字符只有在其完整字形与边界可见、且不存在合理解读替代时，才算清晰可辨；宁要较短但确定的转写，不要较长但貌似合理的转写，绝不要利用语言、品牌或场景上下文补全单词。若整段文字满足该标准，就精确转写。否则绝不要猜测不确定字符：当至少三个字符的连续子串清晰可辨时，只报告该子串，说明其余不清晰，并说明它所在位置（字符数，以及它是开头、结尾还是中段）。只有当该文本边界本身在裁剪图中可见时，才称其为开头或结尾，并说明与不确定侧相邻的字符是否有完整独立字形——在裁切、遮挡、模糊或小尺度下，此类边界字符不可靠。若承载文字的标牌、面板或表面本身在文字区域处或附近被裁剪图边缘裁断，即使每个可见字形都完整，也要把该文字视为部分可见，且被裁一侧不确定——裁剪图不是上帝视角，文字可能在隐藏部分继续。除非文字明显印在该物体上，绝不要把文字归到某个物体上。TEXT COLOR CAUTION：描边或双色字形在此尺度下容易被误读——深色字符配浅色描边常常看起来像深色面板上的白字。只有当笔画填充色明确无歧义时才陈述文字颜色；不确定时写「light-colored text on a dark panel」或「dark text on a light panel」，或干脆省略颜色。猜测的文字颜色绝不允许出现。
- FIGURE AND GROUND：面板的颜色绝不是字形的颜色。把笔画颜色与其所在表面的颜色作为两个独立事实命名（「red characters on a yellow panel」），绝不要让一个代替另一个。尤其注意多色标牌：一个左侧绿色、右侧白色的门头板有两种面板颜色，二者都不是文字颜色，因此把白面板上的黑字写成「white letters」与猜测是同一类错误。夜间发光标牌是最容易出错的地方。
- COUNTING-SCOPE POLICY：不要仅因为此裁剪图中恰好可见 N 个实例就陈述精确数量。只有以下两种情况之一允许精确计数：

  (A) ANCHOR-OWNED SET：被计数的物品是选定锚点的部件、附着于它、被它穿戴、被它持有或包含于它，且与该计数相关的锚点侧完整集合可见。

  (B) FULLY CLOSED ANCHOR-RELATIVE REGION：被计数物品位于由选定锚点与另一个具体可见物体界定的有限区间或区域内，且界定该区域所需的每条边界都完全可见于裁剪图。裁剪图边缘绝不能充当这些边界。

  near、around、behind、in front of、to the left/right of、in the background、in the water、on the beach、on the road 等短语只是定位可见实例；它们并不闭合计数集合。海、水、沙滩、道路、田野、天空、人群以及其他延伸出裁剪图的表面或场景区域都是开放集合，即使当前裁剪图中每个可见实例都清晰可分。对开放集合，在有用时使用非数值措辞，例如「several are visible」，并说明无法从裁剪图确定场景总数。绝不估计或给出范围。

- 不要推断隐藏部分，也不要用世界知识填补空白。把不确定细节描述为不清晰。

以标题恰好为 `VISIBILITY AND REFERENCE NOTES:` 的最后一节结束描述。它是一份简短的项目符号清单，唯一目的是警告后续阶段哪些指称会有歧义或开放；它不是描述，也绝不能被引用为视觉证据：

- 列出每个同类对应物，其内容因被裁剪图边缘裁断、不在视野内或被遮挡而未知：当你描述了一只手时，该人的另一只手；除你已完整描述的之外的其他价签/标签/标牌；当你描述了车辆或大型物体的某个部件时，其未见的其余部分。
- 每条记录只写：实体类别及其所有者或宿主（「the man's other hand」「additional price tags」「the rest of the blue trailer」）、其状态（在哪条边被裁断、不在视野内或被遮挡），以及在适用时写「content unknown」。
- 记录绝不能包含属性、颜色、计数、动作或转写文字，也绝不能猜测隐藏内容可能是什么。
- 若没有符合条件的内容，以恰好 `VISIBILITY AND REFERENCE NOTES: none.` 结束。

#### CAPTION2\_ANCHOR\_MARKED。

由于该裁剪图包含多个同类物体，我们在其中添加了一个细红色选择矩形。它标记下方指令中命名为选定锚点物体的那一个特定实例。静默地利用该矩形，把那个被拍摄物体及其部件、内容、标记和相关附近物体，与其他同类物体的对应内容区分开。然后，像该人为矩形不存在一样撰写描述。绝不要把矩形本身、其颜色、形状、位置、角或边界当作拍摄内容来提及、描述、计数、转写或处理。自然地指称选定的被拍摄物体，例如通过其物体类别与可见场景位置。

`<<<INSERT: CAPTION2>>>`

### J.4 增量证据与双语 QA 生成

#### INCREMENT。

这里给出同一图像区域的两份描述。caption1 是在看到整幅图像时写的（该区域用框高亮）。caption2 是在看到该区域的高分辨率裁剪图时写的。两份描述都被给予相同的选定锚点短语，并被要求围绕该锚点组织，因此任一描述中的「the anchor」都指同一个被拍摄物体；请用这一共享指代来对齐两份描述中的物体身份。

选定锚点物体：

`"{anchor}"`

caption2 中的「selected object」「selected anchor」「marked object」「outlined object」等短语指这个确切的拍摄锚点，而不是新出现的物体。仅用该元数据对齐两份描述之间的物体身份。不要把另一个同类物体与选定锚点合并。若某物体的身份无法可靠对齐，省略该候选事实。caption2 提到的任何选择矩形、轮廓、框、标记、标签或注释都是流程元数据，不是拍摄内容，绝不能成为增量事实。

抽取增量事实：caption2 提供、而 caption1 省略（absent）、标记为不清晰（unclear）或给出不同陈述（contradicted）的离散、可视觉验证的信息。矛盾也是增量：以 relation `"contradicted"` 报告，并记录 caption1 的主张。

强制的裁剪视口不变性检查（优先级高于把矛盾视为增量）：每条保留的事实都必须描述拍摄场景或物体的内在属性，并且在裁剪图扩展后仍语义为真。裁剪图不是场景的特权或上帝视角；它只是隐藏了四条人为边缘之外的内容。物体有多少部分落在裁剪图内，这一差异绝不是场景事实的 absent、unclear 或 contradicted。拒绝任何基于以下情况的候选：物体位于裁剪图边缘、被裁断、被裁剪、仅部分可见，或被裁剪图缩减为特定可见身体部位。例如，若 caption1 描述一个人在走路，而 caption2 说在底边只能看到此人的头和肩，这些主张并不矛盾：caption2 报告的是视口截断，因此完全省略该候选。即使 caption2 自信地陈述该边界观察，且可归入某类允许的事实类型，也应用该规则。把每条提议事实加入 JSON 前，静默审查其是否依赖裁剪边缘。

VISIBILITY AND REFERENCE NOTES 处理：caption2 可能以标题为 `VISIBILITY AND REFERENCE NOTES` 的节结束。该节仅是消歧上下文。绝不要从中抽取事实，绝不要整体或部分引用为 `source_from_caption2`，也绝不要让它添加、升级或反驳主描述内容。仅用它来意识到其他同类实例或隐藏部件存在且内容未知。

REFERENT QUALIFIER PRESERVATION：当 caption2 的证据句用限定语钉住某个实例——解剖学侧面（「in his right hand」）、已说明的朝向、附着或最近物体关系（「the mug nearest the kettle」）、宿主上的部件位置（「on the tail of the aircraft」）或深度带标签（「much closer to the camera than the anchor」）——该事实的陈述必须保留该限定语。禁止丢弃限定语并把信息归到裸类别（「the man holds a can」「the price tag reads 140」），因为裁剪图之外可能存在其他实例。复述证据时绝不要把解剖学侧面翻转成观察者侧面，或反之；caption2 中括号内的观察者侧推导可以在陈述中省略，但解剖学侧面本身必须精确保留。

SPATIAL-FRAME CONFLICTS ARE NOT INCREMENTS：两份描述遵循同一坐标系契约（解剖学身体侧由所述朝向推导；物体之间用观察者坐标系；不使用深度「behind」）。若两份描述仅在同一人的哪个身体侧携带某物品或姿态（左手/右手/手臂/腿/肩）上不一致，且 caption2 在陈述此人朝向时给出推导，而 caption1 没有，则把 caption2 的侧面视为对同一观察的修正重标：不要把侧面翻转本身作为 contradicted 事实输出，也绝不要创建以「某物在哪一侧身体」为主要内容的事实。在该物品的其他任何事实中，静默使用 caption2 的侧面。

CAPTION1 OMISSION GUARD（仅适用于 relation `"absent"`）：caption1 是在整幅图像尺度写的，但仍可能单纯忘记一个明显属性。当 caption1 清楚地把某物体描述为区域内的大或显著物体——例如占据其大部分的人——而候选事实陈述的是任何整幅图像观察者都会明显看到的粗粒度属性（主导衣物颜色或衣物类型、物体整体颜色、粗粒度姿态、明显的正在进行的动作）时，把缺失属性视为 caption1 的遗漏，而不是增量，并省略该事实。只对真正细粒度的信息保留 `"absent"` 事实：小字、小部件或配件、精确计数、细微图案、小持有物，或可见性合理需要拉近的细节。该守卫绝不适用于 relation 为 `"unclear"`（caption1 明确看不到）或 `"contradicted"`（caption1 做了不同陈述）的事实。

只保留以下类型的事实：`count`、`OCR text`、`color`、`action`、`local attribute`、`spatial relation`。丢弃：

- 主观措辞以及任何带「possibly/maybe」之类模糊限定的内容；
- 仅描述质地的内容（植被、草、天空、水、光照）；
- 关于区域边界本身的事实（框内/框外是什么、被裁剪边缘裁断的物体）；
- 范围计数（「15-20」）与估计；
- 色调级色差（红 vs 橙、青 vs 蓝）——只有两个主张显然属于不同颜色类别时才保留颜色矛盾。

COUNT FACT ELIGIBILITY（强制，优先级高于矛盾）：

- 只有当精确计数恰好属于两种范围类型之一时才保留：(A) `anchor_owned`——属于选定锚点的部件、附着于它、被它穿戴、被它持有或包含于它的物品；或 (B) `closed_anchor_relative_region`——位于由选定锚点与另一个具体物体明确界定的有限区域内、且所有边界都在 caption2 中完全可见的物品。
- 人为裁剪边界绝不闭合集合。near、around、behind、in front of、left/right of、in the background、in water、on a beach/road/field 等相对词是定位词，不是完整边界。海、沙滩、道路、田野、天空、人群或其他可能延伸出裁剪图的区域上可见的人或物子集，不是精确的场景计数。即使 caption2 给出自信数字，即使 caption1 给出不同数字，也拒绝它。
- 对每条保留的计数事实，添加 `count_scope_type`（`anchor_owned` 或 `closed_anchor_relative_region`）、`counted_entity`、`scope_boundary_description` 与 `scope_fully_visible=true`。若无法从 caption2 如实填写全部四个字段，省略该计数事实。对非计数事实，这些字段用 null。

OCR 证据规则：

- TYPE DISCIPLINE：任何陈述报告可读字符、字母、数字、单词、标志文字或铭文的 fact，都必须使用 type `"OCR text"` 并填写全部审计字段。绝不要把读文本的事实标为 attribute、local attribute 或 color——那会让它绕过所有 OCR 边界规则。
- 保留 caption2 的精确确定性边界。若 caption2 说只有某个子串可辨，把该事实标为部分 OCR 文本，并保留精确子串、其字符数及其所述位置。
- 部分 OCR 事实只有在包含至少三个连续清晰可辨字符、且 caption2 为该子串给出可用位置时才合格。
- 绝不要补全、修复、规范化或猜测不清晰字符。绝不把部分子串变成关于完整铭文、单词、品牌或名称的断言。
- 若 caption2 转写了一个序列，但也说铭文延伸到被裁剪或遮挡的一侧，即使可见序列本身被描述为清晰，也把它视为部分 OCR。保留哪一侧不确定，以及边界相邻字形是否完整孤立。
- 对每条 OCR 事实，添加以下审计字段：`ocr_scope`（full 或 partial）、`visible_sequence`（精确转写字符）、`uncertain_side`（left、right、top、bottom、both、internal、none 或 unknown）与 `boundary_character_isolated`（JSON 布尔值 true 或 false，绝不是带引号的字符串）。若同一铭文、标牌、标签或印刷文字的任何部分被描述为被裁剪、遮挡、不完整或不清晰，`ocr_scope` 必须为 partial。只有 caption2 明确确认接触不确定侧的字形完整且两侧明显分离时，才把 `boundary_character_isolated` 设为 true；否则用 false。
- 对每条 OCR 事实，还要相对于正常阅读顺序、而不仅相对于图像几何来表达证据。当完整铭文可见时把 `substring_position` 设为 full，当可见序列是更长铭文的开头时设为 prefix，是结尾时设为 suffix，caption2 不支持该判断时设为 unknown。当 `visible_sequence` 的相应边界字符接触不确定区域时，把 `unsafe_boundary` 设为 beginning 或 end；在适当时使用 both、internal、none 或 unknown。不要自行裁剪 `visible_sequence`。物理上的上/下/左/右与序列的开头/结尾是不同的概念。

只输出严格 JSON：

```
{"incremental_facts": [{"type": "...", "statement": "...", "source_from_caption2": "...", "ocr_scope": "full|partial|null", "visible_sequence": "...|null", "uncertain_side": "left|right|top|bottom|both|internal|none|unknown|null", "substring_position": "full|prefix|suffix|unknown|null", "unsafe_boundary": "beginning|end|both|internal|none|unknown|null", "boundary_character_isolated": false, "count_scope_type": "anchor_owned|closed_anchor_relative_region|null", "counted_entity": "...|null", "scope_boundary_description": "...|null", "scope_fully_visible": true, "relation_to_caption1": "absent|unclear|contradicted", "caption1_claim": null}], "skip_reason": null}
```

如果没有可靠增量——特别是每条候选事实都只涉及植被、天空、水、光照或一般质地——返回空列表并给出简短 `skip_reason`。

caption1:

```
{caption1}
```

caption2:

```
{caption2}
```

#### QA\_GENERATION。

你正在从增量事实生成细粒度视觉 QA。

锚点物体（在整幅图像中显著且可唯一定位）是：

`"{anchor}"`

裁剪图局部锚点规则：

```
{local_anchor_rule}
```

增量事实（只有拉近到锚点周围区域时才可见的信息；每条都有一个来自拉近描述的证据句）：

```
{facts}
```

该区域的完整拉近视图描述（用于检查同类重复物体——不作为新事实来源）：

```
{caption2}
```

当前生成目标以及针对同一锚点的先前 QA 候选反馈：

```
{retry_context}
```

生成至多 `{qa_per_anchor}` 个问题。

每条增量事实都有一个 `source_fact_index`。为每个 QA 所用事实返回该精确整数。可用时，直接从该事实的 `source_from_caption2` 复制 `evidence_sentence`；否则用其 `statement`。

问题规则：

- 每个答案必须来自恰好一条增量事实。
- 当同一响应中生成多个 QA 时，每个 QA 必须使用不同的 `source_fact_index` 与证据句；绝不要从同一事实造两道题，或换述同一道题。
- 任何要求求解器读取或转写文字、字母、字符、数字、单词、标志字样或指定字符跨度的问题，都必须使用 `question_type=ocr`。绝不要把此类问题标为 attribute、comparison 或其他类型。
- 优先级：若存在一条或多条合格 OCR 事实，先基于这些 OCR 事实生成 QA，再使用 count、attribute、action 或 spatial 事实。增量事实列表按 OCR 事实在前排序。
- 完整阅读 OCR 事实，尤其是 `statement` 与 `source_from_caption2`；不要把 `visible_sequence` 当作唯一有用信息。与文字明确关联的视觉细节——例如其背景颜色、文字颜色、位置、方向、所在面板，或与另一标签的关系——是有价值的指代线索。优先选择用这些线索标识某一文本区域的问题，而不是询问整块标牌或标志上所有文字的泛泛问题。把视觉属性用作定位器，而不是另一个被问的答案。
- 带模糊限定的身份不是指称。当 caption2 对某物是什么加模糊限定——「what looks like a bird」「possibly a helmet」「某种容器」——它是在告诉你它无法识别该物体，而基于该猜测构建的指代表达式在猜测错误时匹配不到任何东西：寻找鸟的求解器永远找不到它实际是塑料袋。去掉模糊名词，用确定的东西定位该物——它位于何处、它在什么里面或附着于什么、它的颜色与尺寸（「the small white object on the ledge above the second window」）。若没有确定信息能标识它，跳过该事实。也绝不要把模糊限定带进问题：「the shoe or boot」会告诉求解器你在猜。
- 定位属性可靠性：优先使用宿主级线索——面板/标牌颜色、位置、所在物体、最近地标——而不是文字自身的颜色。小字颜色经常被误感知（深色描边字被读成白色），错误的定位属性会误导求解器或匹配到另一文本区域。只有当事实无模糊限定地陈述文字颜色，且它提供了宿主线索未能提供的区分度时，才包含文字颜色；当仅靠面板已可唯一确定时，省略文字颜色。绝不要把多色标牌某一区域的颜色安到位于另一区域的文字上；若你无法无模糊地说出笔画填充色，只用宿主线索。
- 每个 OCR 答案只对应一个宿主。答案是由单一有界宿主承载的文字——一块标牌、标签、铭牌、面板或印刷行。绝不要用位于不同物体上的字符拼出答案，也绝不要用靠近某一组来界定 OCR 问题（「the digits printed near the green bottles」「the letters around the potted plants」）：与一个集合的邻近没有求解器可复现的边界，因此哪些字符属于答案就变得任意，第二位读者会纳入不同集合。若你想要的文字横跨多个独立宿主，改问其中一个。
- OCR 事实可能包含由代码计算的确定性字段：`safe_sequence`、`safe_character_count`、`required_span` 与 `qa_eligible`。绝不纠正、修复或杜撰 `safe_sequence` 之外的字符。答案必须是 `safe_sequence` 中一个明确有支持的连续片段。
- 对部分 OCR 事实（`required_span=first` 或 `last`），写一道关于该铭文的朴素读文本问题，用宿主级线索定位，答案等于 `safe_sequence` 原文。不要添加任何跨度措辞（不要「first/last k characters」），不要添加「entire」「complete」「all the text」等整体词，也绝不提及裁剪或隐藏字符。一个看到整幅照片的专用边缘改写阶段会把此类草稿改写为最终的安全跨度措辞；你的草稿只需选对铭文并复制 `safe_sequence`。
- 局部化的完整 OCR 片段：当 `required_span=full` 且事实本身明确把不同完整单词或连续词组与可独立识别的视觉区域关联时，你可以询问其中一个区域，并只用其完整文本作为答案。所选答案必须是 `safe_sequence` 中逐字出现的一个或多个完整连续单词；绝不从单词内部取字符。两道问题都必须包含该事实支持的、能隔离该片段的视觉定位器。不要杜撰颜色、位置、容器或关系。若事实不支持唯一的局部化片段，使用完整的 `safe_sequence`。
- 示例：若一条事实说 OPEN 以白色出现在上方绿色面板上，24 HOURS 出现在下方独立的黑色条带上，优先问上方绿色面板上是什么文字（答案：OPEN），而不是问标牌上所有文字是什么。该示例只说明策略；绝不要把它的物体、颜色、位置或文字复制到另一图像的 QA 中。
- 对 `required_span=full`，要么询问完整清晰可辨文字并逐字使用 `safe_sequence`，要么严格按上述定义应用局部化的完整 OCR 片段。
- 绝不写依赖视图的指令，例如「excluding the top character」「ignore the cropped character」「remove the first visible letter」，或任何提及图像/裁剪边界、裁剪、截断或隐藏字符的内容。固定的前/后 k 跨度在整幅图像与拉近图像中必须具有相同答案。
- 跳过所有 `qa_eligible=false` 或缺少全部必需确定性字段的 OCR 事实。
- 若上下文除 `generation_target_state` 外还包含先前候选条目，选择不同的增量事实与答案属性。不要重复或仅仅换述任何被拒绝或保留的全局/裁剪问题、证据句或源事实。
- 只用拒绝反馈来选择更有支持的候选。绝不要为模仿验证器输出而改动参考答案，也绝不要杜撰增量事实列表中不存在的事实。
- 若先前的候选未通过裁剪验证，优先选择另一条答案更大/更清晰、且在裁剪图中直接可见的事实。
- 上下文中的 `generation_target_state` 条目是权威的。若 `zoom_required_still_needed=true`，且先前被接受的候选可从整幅图像回答，优先选择明显更小或更精细、标记为 absent/unclear/contradicted 的细节。若为 false，则一条保留的、可从整幅图像回答的 QA 计入已接受问题下限；下一道不同的已接受 QA 可以是从整幅图像可回答的，也可以是必须拉近的。
- 若重试反馈说先前候选在专用的图像感知指称修复失败后仍存在歧义，使用另一个可唯一指称的目标。绝不要添加泄露答案的限定语。
- DISAMBIGUATION：写每道题之前，扫描上面的完整描述。若答案物体的类别可能匹配裁剪图中的多个物体（例如一个人戴的戒指 vs. 一件独立的戒指产品图），裁剪图局部指代短语必须包含能区分它们的限定语（位置、尺寸、展示中 vs. 佩戴中、颜色）。若没有裁剪图可见的限定语能使其唯一，跳过该事实。
- 为每道题写两个语义配对的版本：

  1. `question_zh` / `question_en` 是面向原始整幅图像的 GLOBAL 问题。它们必须让从未见过裁剪图的求解器能在整幅图像中定位答案物体。依据目标与锚点的真实关系选择定位方式（见下方 GLOBAL LOCATOR POLICY）。
  2. `crop_question_zh` / `crop_question_en` 是面向确切拉近裁剪图的 LOCAL 问题。移除裁剪图本身无法建立的上下文，例如「in the center of the plaza」「on the building in the background」「to the right of the white building」。只保留证据在裁剪图内可见、且在此处识别答案物体所需的限定语。

- 严格遵循裁剪图局部锚点规则。选择矩形只能用作拍摄锚点、其部件、内容、标记或相关附近物体的指代表达式定位器。绝不询问矩形本身、其颜色、形状、边界、角或任何人为标签。GLOBAL 问题绝不能提及选择矩形。
- GLOBAL 与 LOCAL 版本必须询问同一物体的同一属性，且答案必须相同。局部版本不是一道新问题。
- LOCAL 问题必须自包含，其答案物体必须能在裁剪图内唯一识别。若移除不可用的全局上下文会导致无法做到，跳过该事实。

GLOBAL LOCATOR POLICY（裁剪图是二维窗口；其中的物体可能处于完全不同的场景深度，因此裁剪图内的二维邻接不是场景邻近）：

(a) 若答案物体与锚点存在真实的、视觉支持场景关系——它是其部件、附着于它、在同一支撑面上、被它持有，或在同一深度上真正相邻——照常通过锚点短语定位。

(b) 若答案物体与锚点明显处于不同深度（拉近描述说它明显更近或更远，例如围绕背景灯塔构建的裁剪图中有一个前景慢跑者），绝不要用 near、beside、next to、附近、旁边等词声称邻近，也绝不要把 front/behind 当作伪装的深度词。那会杜撰不存在的关系，误导求解器在锚点周围搜索，读起来也不自然。优先通过诚实关系在问题中保留锚点——它是已验证、最容易找到的地标——从以下读起来自然的选项中择一：

- CAMERA-AXIS 关系（适用于任何锚点，包括无面结构；当目标位于或接近锚点视线时首选，裁剪图共属通常保证这一点）：用规范措辞陈述沿观察轴的深度顺序——目标更近：「the yellow taxi between the clock tower and the camera」/ 在钟楼与镜头之间的黄色出租车；目标更远：「the brick warehouse beyond the red barge, farther from the camera」/ 越过红色驳船更远处的砖砌仓库。当两者在图像中不重叠时，添加小的图像坐标系偏移词（「below the clock tower and between it and the camera」）。这种措辞是诚实的三维几何，绝不是邻近断言。
- INTRINSIC ANCHOR-FRAME 关系：当锚点是 caption2 已说明朝向的人、动物或车辆时，可在锚点自身坐标系中定位目标，每侧按契约机械推导。例如，一个朝观察者骑来的骑行者，其更深的场景在他身后，他的左手侧在观察者右侧，因此「the bright blue vertical sign behind the cyclist on his left-hand side」是诚实且自然的。SIDE-BLINDNESS GUARDRAIL：验证模型无法可靠分辨人的左右侧，因此任何锚点坐标系方向从句只是叙述脚手架——忽略该从句时，问题必须仍能通过至少一个与锚点无关的判别项（物体类型加颜色、最近固定地标或观察者坐标系位置）唯一标识目标。若唯一性依赖锚点坐标系从句本身，不要使用该选项。
- 与锚点的明确图像坐标系关系：诚实二维措辞，例如「in the image, above the cyclist in the background」或「below the lighthouse and much closer to the camera」，绝不使用暗示物理邻近的措辞。
- 自定位指称（当没有锚点链接措辞读起来自然时的兜底，例如跨越大而杂乱的深度差时链接会显得牵强）：放弃锚点，用整幅图像坐标系位置加目标自身可见属性来定位，例如「the jogger in the lower-center foreground of the image wearing a cap」。foreground/closer to the camera 等深度词跨视图仍为真；水平词必须从整幅图像重新推导，绝不从裁剪图问题复制。

(c) 若以上都无法产生你有信心在整幅图像中唯一的指称，跳过该事实。

优先选择关于锚点本身或其自身深度带内物体的事实：一个比锚点近得多的裁剪图前景物体在整幅图像中通常又大又清晰，因此其事实很少能通过整幅图像难度门；只有没有锚定事实可用时才用它们。

示例对：

GLOBAL: "What text is written on the sign in the center of the plaza?"
LOCAL: "What text is written on the sign?"

- 绝不要把答案属性本身放进任一指代表达式（若答案是颜色，指代短语不得提及该颜色）。
- 答案必须是单一确定值：精确计数、一个颜色词、短文本串或短动作。跳过带范围、模糊限定或主观措辞的事实。
- 答案本身绝不能是解剖学身体侧（「left hand」「right leg」），也绝不能是朝向物体的部件位置（「near the front left corner」「at the rear end」、车头/车尾）：所有视觉模型都有系统性的镜像与朝向混淆，因此此类答案无法可靠验证。侧面与部件位置只作为问题内的指代限定语。
- COUNTING SOURCE GATE：使用计数事实前，分类其真实场景范围。只有以下情况才合格：(A) `anchor_owned`：被计数物品是选定锚点的部件、附着于它、被它穿戴、被它持有或包含于它，且相关锚点侧完整集合可见；或 (B) `closed_anchor_relative_region`：物品占据由锚点与另一个具体可见物体明确界定的有限区间或区域，且所有边界完全可见。若两种分类都不成立，跳过该事实，即使它包含精确数字且被 caption1 反驳。
- 裁剪图边缘绝不闭合计数范围。near、around、behind、in front of、left/right of、in the background、in water、on a beach/road/field 等短语标识可见子集，但不定义完整集合。绝不要生成询问此类开放场景区域总数的问题。尤其禁止对海、沙滩、道路、人群、田野或天空的裁剪切片中当前可见实例计数。
- 对合格的 `anchor_owned` 计数，问题必须明确把被计数物品绑定到锚点。对合格的 `closed_anchor_relative_region` 计数，问题必须命名两个界定物体及其间的有限区间/区域。「behind the anchor」这样的泛泛短语不够。
- 优先选择携带 `count_scope_type` 与 `scope_fully_visible=true` 的计数事实。独立审查证据与完整裁剪图描述；元数据不能挽救实际开放的范围。
- 跳过关于区域边界与植被/天空质地的事实。
- 跳过仅在两个视图之间色调级不同的颜色事实。

`<<<INSERT: SPATIAL_FRAME_RULES>>>` `<<<INSERT: CROP_FRAME_CAVEAT>>>`

- 对问题与答案中的每个方向词应用上述坐标系契约。身体部位侧面保持事实所述的解剖学意义（「right hand」指他自己的右手）；绝不把解剖学侧面转成图像侧面，或反之。把括号内的朝向/观察者侧推导排除在问题文本之外——问题只携带自然的人类措辞。
- BILINGUAL FRAME PARITY：中文与英文版本必须以同样的纪律编码同一坐标系。中文里，场景深度必须写作 背景中 / 前景中 / 离镜头更远 / 更靠近镜头——绝不要在人/动物上使用 后方、身后、前方 或 前面（写 跑者背景中更远处的车辆，而不是 跑者后方的车辆）。只在人的内在侧面、且问题本身说明该人朝向时使用 身后/面前（例如 背对镜头的人身后）。左手/右手 只表示解剖学意义，与英文 left/right hand 完全一致。
- LIMB QUALIFIER PREFERENCE：为唯一指定一个人的成对肢体之一，优先使用事实记录的姿态或状态——抬起的手臂、垂在身侧的手臂、抓着带子的手——而不是解剖学侧面。姿态措辞自然、无需朝向推导，且是求解器唯一能核查的类型；验证模型无法可靠分辨人的左右手。只有当事实以明确的朝向推导陈述侧面、且没有姿态描述能区分肢体时，才使用「left/right hand」。
- REFERENT CLOSURE（强制）：若事实的答案物体属于多实例类别——手、脚、鞋、价签、标签、标牌、屏幕、轮子、窗户、包或类似重复部件与产品——且拉近描述或其 VISIBILITY AND REFERENCE NOTES 表明场景中任何地方存在其他实例、被裁断或不在视野内且内容未知，则全局问题与裁剪图问题都必须用事实及其证据携带的限定语钉住确切实例：解剖学侧面（「in his right hand」）、附着或最近关系（「on the price tag closest to the kettle」）或部件位置（「on the rear end of the large blue trailer」）。在这种情况下，裸的「in his hand」「on the price tag」「on the sign」或「on the vehicle」是被禁止的。若事实与证据没有此类限定语，而记录显示存在对应物，则跳过该事实。
- 绝不要在任何问题中提及裁剪视口、裁剪、截断、被裁或不在视野内状态、可见性限制，或 VISIBILITY AND REFERENCE NOTES 节；记录只告诉你何时需要额外的钉住限定语。「near the left edge of the image」等图像坐标系位置指称是定位词，不是视口话语，在坐标系契约下仍允许。
- FRAME CLAIMS COME FROM CAPTION1 ONLY。caption2 看到的是裁剪图，不是照片，因此其中任何左/右/侧面措辞描述的是裁剪图自身的坐标系，作为关于图像的陈述毫无价值——常常还是错的：从照片右侧取出的裁剪图有自己的左侧。绝不要把 caption2 中的水平位置复制或换述进问题。只有当看到整幅照片的 caption1 把目标放在那里，并像 caption1 那样措辞时才使用。
- NO FRAME SUPERLATIVES。两种语言都绝不要对图像写 leftmost、rightmost、topmost、bottommost、far left、far right、最左、最右、最上、最下、最顶、最底。成为某类别中最靠外者是对照片中一切事物的断言，两份描述都无法确立；改用附着、最近物体或部件限定语。一个具名宿主内部的最高级仍然可以（「the bottom word on the blue sign」），因为宿主为它定了界。
- 在合格 OCR 事实之后，优先选择计数/属性事实，并优先选择 `relation_to_caption1` 为 `"contradicted"` 或 `"unclear"` 的事实。

只输出严格 JSON：

```
{"qas": [{"question_zh": "...", "question_en": "...", "crop_question_zh": "...", "crop_question_en": "...", "answer": "...", "question_type": "counting|ocr|attribute|action|spatial|comparison", "evidence_sentence": "verbatim evidence", "source_fact_index": 0}]}
```

若没有事实合格，输出 `{"qas": []}`。

#### LOCAL\_ANCHOR\_RULE\_UNMARKED。

不存在人为选择矩形。两道 LOCAL 问题都不得提及框、轮廓、标记或注释。

#### LOCAL\_ANCHOR\_RULE\_MARKED。

裁剪图中有一个细红色选择矩形标识锚点。两道 LOCAL 问题都必须明确把矩形仅用作定位器，措辞如「the [object] inside the red selection rectangle」/「红框标出的[物体]」。若事实涉及部件、内容、标记或附近物体，要把它明确关联到该红框锚点。绝不要询问矩形本身。GLOBAL 问题必须自然描述拍摄锚点，且不得提及它。

### J.5 裁剪图/整幅图像的联合审查与改写

#### EDGE\_REWRITER。

你是视觉 QA 数据流程的裁剪边界审查器与问题改写器。

背景——为什么存在这一阶段：

流程围绕一个锚点物体撰写细粒度 QA。此前每个阶段都只看到围绕该锚点取出的裁剪图：描述器描述裁剪图，问题撰写者把描述事实转成裁剪图局部问题加整幅图像问题。二者都无法看到裁剪图四条边之外，因此两类反复出现的失败会逃过它们：

1. 答案主张不完整：承载答案的物体或文字延伸出裁剪边界，而记录的答案悄然声称自己是完整文本或整体属性，实际并非如此（一块标牌的顶行位于裁剪图之上；一个船体延伸出边缘且还有更多标记）。
2. 指称在整幅图像中有歧义：指代短语在裁剪图内恰好只匹配一个东西，但在整幅照片中匹配多个东西（同一面墙上有三块白标牌；同一船体上还有第二处红色文字）。

你是第一个同时看到两种视图的阶段，因此这些对你而言成为直接观察。下游的独立求解器模型将只看到裁剪图回答裁剪图局部问题，只看到整幅照片回答整幅图像问题。你的目标：任一视图中诚实、仔细的求解器都必须恰好得出记录的答案。拒绝一道问题会浪费已投入创建它的全部工作，因此优先用有界改写挽救问题，而不是丢弃——但绝不以真实性为代价挽救。

输入：

图像 1 是裁剪图。若存在标有 C1 的青色框，它标记的是裁剪图局部问题已认证的唯一指称对象；若存在细红色矩形，它标记锚点。二者都是注释，绝不是场景内容。

图像 2 是整幅照片，用红色矩形标出裁剪图的取景位置。用它查看裁剪图之外还延续着什么，以及场景中还有什么匹配问题措辞。图像 2 可能分辨率较低：用它检测延续与统计指称匹配数，不要用它读取新文字。

正在审查的 QA：

anchor: `"{anchor}"`

question\_type: `{question_type}`

global question（整幅图像求解器）EN：`{question_en}`

global question ZH：`{question_zh}`

crop-local question EN：`{crop_question_en}`

crop-local question ZH：`{crop_question_zh}`

recorded answer：`{answer}`

mechanical OCR contract（非 OCR 为 null）：`{ocr_constraint}`

caption evidence sentence：`{evidence}`

审查程序：

A. CONTINUATION：在图像 2 中，承载答案的物体或文字是否明显延伸出裁剪矩形，从而可能按问题措辞增加或改变答案？对 OCR 问题，还要检查裁剪图内该文字自身的宿主是否在文字附近被裁断或遮挡，以致文字可能在视野外继续。当问题只询问一个完全可见的有界部分时，宿主被裁断无害。

THE BURDEN IS ON 'false'。到达裁剪边界就是延续，除非你能指出它不是的理由。只有当你能在两个视图之一内部看到并命名该侧限制宿主的边界——其自身框架、边缘、角或末端——或图像 2 显示完整宿主之外别无他物时，才回答 false。若宿主延伸到边界且你看不到它在哪里结束，那就是 true，而不是 false，无论你能读到的部分多么清晰：一块左边缘就是裁剪图左边缘的街牌会被读成「STATION ROAD」，而实际是「OLD STATION ROAD」；一块底边就是裁剪图底边的菜单板只显示五行中的两行。两者看起来都完整。能读出可见内容并不证明没有其他内容。

回答 true 并不会判 QA 死刑——narrow_semantic 通过收窄到你能完整看到的子块（「the line nearest the arrow marker」「the bottom word」）来挽救它。优先选择这种挽救，而不是你无法证明的 confirm。

B. UNIQUENESS：读取 GLOBAL 问题的每个指代短语，统计其在图像 2 中的匹配数；读取 CROP 问题，统计其在图像 1 中的匹配数。仔细的求解器会视为决定性的定位差异（唯一附着、位置或尺寸措辞）算作消歧；裸类别加颜色通常不算。

对 OCR 问题，还要统计文本块：同一宿主上每一处独立文字，只要求解器可能认为它匹配问题对文本的描述（其颜色、大小写或样式），都是竞争候选。像严格求解器那样判断，而不是像品牌读者：较小的第二行算；同色系的更深色调算；数字与字母数字混合串算作大写字形文本；品牌名下方印的注册号或电话号码是典型的竞争块。若超过一个文本块可能匹配，诚实的求解器无法知道该读哪个：措辞必须按行、尺寸或位置唯一指定（改写），否则必须丢弃该 QA。绝不要假定最醒目的文字就是「那个」文字。

WEAK TEXT REFERENT RULE：仅用颜色和/或字母大小写描述（「the red capital letters」）、没有尺寸、行或位置限定语的文本指称是弱措辞。只要宿主带有任何其他标记——即使你判断它太小或太淡而无法阅读——也优先进行最小收紧改写（添加「the largest」、行或位置词），而不是 keep。收紧不付出代价，却能使问题对处于可读性边缘的标记保持稳健。

在输出字段 `other_inscriptions_on_host` 中列举该审查：同一宿主上每一处其他文字、印刷、编号或标记各一条（仅当宿主确实没有其他标记时为空列表）。`could_match_question_wording=true` 表示严格求解器可能认为该块匹配问题的文本描述。在任一 entries 为 true 时保留问题是矛盾的——那你就必须改写（按行、尺寸或位置唯一指定目标）或丢弃；代码会强制这一点。

C. COUNT SCOPE（计数问题）：被计数集合必须由可见边界闭合；若图像 2 显示该集合延伸出裁剪图，而问题暗示总数，则主张不成立。

VERDICTS：

- keep：两项审查都干净；记录的答案正是诚实的求解器在两种视图中都会给出的答案。
- rewrite：有界编辑修复问题——收紧指代短语使其在两种视图中唯一，或把 OCR 主张收窄到安全跨度（见 OCR SPAN DECISION）。一致地改写全部四个问题字段。
- drop：记录的答案在任一视图中事实上错误或无法验证，没有裁剪图可见的限定语能使指称唯一，或计数的范围被裁剪边缘打开。当挽救需要仅看裁剪图的求解器无法看到的信息时，也丢弃。
- COUNT RESCUE BAN：集合被裁剪图打开的计数问题绝不能通过措辞挽救。添加「visible」/「可见」或类似词会使裁剪图总数与整幅图像总数不同，于是两种视图会有不同正确答案。此类问题无法修复：丢弃。

REWRITE RULES：

- 记录的答案绝不能被你在图像 2 中读到的内容扩展、纠正或替换——你位于证据抽取的下游，只能收窄主张。对非 OCR 问题，答案必须完全不变；你只编辑措辞。对 OCR 问题，答案只能收缩为记录序列的一个连续部分。
- CROSS-VIEW LOCATOR ATTRIBUTES：对照两张图像检查问题用来寻找目标的每个属性——颜色、尺寸、材质、形状——包括草稿已包含的属性。裁剪图中的一小条常常会错误描述整幅照片中的整个物体：一块白标牌唯一可见的条带衬在橙色面板上，在裁剪图中会被读成「the orange sign」，而在整幅图像中匹配不到任何东西（或匹配到别的东西）。用两个视图中都为真的属性替换误导性属性，若不存在则丢弃。
- 你添加的每个限定语都必须能在裁剪图内验证（裁剪图求解器看不到外面），且在整幅图像中仍为真。优先使用附着、最近物体、部件位置、行/线位置或相对尺寸线索。绝不使用视口词（crop、edge、truncated、cut off、visible portion、画面边缘、被截断），也绝不把答案字符或答案词复制进任何问题字段。
- 保持两种语言同步，并保持全局/裁剪图配对：全局问题为整幅图像求解器定位目标（通常通过锚点）；裁剪图问题丢弃裁剪图无法建立的上下文。
- 改写中的空间措辞必须遵守该契约：

`<<<INSERT: SPATIAL_FRAME_RULES>>>` `<<<INSERT: CROP_FRAME_CAVEAT>>>`

OCR SPAN DECISION（每个 OCR 问题必填，放在 `ocr_span_decision`；非 OCR 为 null）：

你可以修改 OCR 问题的答案——这通常是最好的挽救，而不是最后手段——前提是新答案是记录答案的连续部分。上游草稿常常笨拙（一个 20 字符的位置跨度，或一个悄然跨越截断的序列）；你的工作是重新界定到一个易于指称、且在两种视图中都为真的片段：最下面的词、最大的一行、最上面一行，或开头几个字母。按以下顺序处理决策，并选择第一个能在两种视图中产生真实主张的选项：

- confirm：问题所问的文字完全可见，没有合理延续，且记录答案是它的完整文本（或问题已带有自洽的跨度措辞）。可与 verdict keep 或仅修正指代短语的 rewrite 一起使用。凡你观察到该文字的宿主在文字区域处或附近被裁断或延续——无论在裁剪图还是图像 2 中——都禁止 confirm。观察到延续却仍然 confirm 是矛盾；改选 narrow_semantic、demote 或 drop。
- narrow_semantic（首选挽救）：把问题重新界定到一个完全可见、视觉上可隔离的子块——最下面的词、最上面一行、最大的一行、某一面板上的组——其完整文本是记录序列中连续的完整单词部分；答案变成恰好该部分（「what is the bottom word on the sign」->「Bakery」，而记录答案是「Old Town Bakery」）。求解器会自然读取这样的单元，无需数字符。只用视觉属性（位置、尺寸、行、其面板的颜色）标识该子块，绝不引用其文本。
- 子块在被裁侧必须闭合。只有当一个子块自身的每条边界都在裁剪图内时，它才算「完全可见」，而重要的边界是面向裁断的那条。当宿主在其左侧或右侧被裁断时，一行或一条线会直接冲进该裁断而不闭合，因此「the lower line」「the word at the top of the sign」「the largest word on the second row」以及任何其他基于行或带的选法在那里都无效——改选一个远离裁断、四周有界的单元（一个远侧是空白区域的词、某个完整面板上的块）。当宿主在顶部或底部被裁断时，远离裁断的各行没问题，而列不行。对一个继续到视野外的单元使用尺寸最高级（「the largest word」）是在断言你看不到的文字。若不存在闭合子块，使用 demote_first / demote_last 或 drop；不要收窄到开放子块上。
- demote_first / demote_last：用于 narrow_semantic 无法表达的情况——没有完整单词是安全的，但一个干净的子词边界片段是（一个更长单词中只有「SUR」清晰可见）。询问记录序列恰好前/后 k 个字母数字字符，3 <= k <= 7——求解器必须数字符，因此更大的 k 会把阅读变成易错的计数并被机械拒绝。当文本开头边界明显真实、延续风险在结尾时用 demote_first；镜像情况用 demote_last。CROSS-VIEW SPAN AGREEMENT（强制）：选择 k 之前，在图像 2 中读取相同字符——你保留的 k 个字符中的每一个都必须在裁剪图与整幅照片中完全相同。跨越截断拼接起来的记录序列（两条被裁断的行被读成一个串）会在拼接处与真实文本分歧，任何到达拼接处的 k 都会使整幅图像求解器得到错误答案：选择严格位于分歧之前的最小稳定 k（>= 3）；若连 3 个一致的字符都不存在，则 demote 不可用。两个英文问题字段都必须在 first/last 旁明确写出 k（例如「the first 3 characters」），中文字段必须镜像（例如「前3个字母数字字符」）。答案是该精确跨度，保留其原始空格与标点。
- SHORT ANSWERS：少于 3 个字母数字字符的答案无法进一步收窄，因此只有当该文本任何地方都无延续时，它才能作为 confirm 存活。若文字继续到视野外（或其宿主在文字处被裁断），1–2 字符的记录答案就是更长内容的片段：丢弃它，而不是把问题重新界定到该片段——无论哪种方式，代码都会拒绝此类挽救。
- 只有在检查不存在任何收窄可能之后，才丢弃 OCR 问题：完整单词子块（narrow_semantic）与 3–7 字符边界跨度（demote）都无法产生两种视图中为真的主张。记录答案整体错误，并不足以在其收窄后的部分仍完全正确时成为丢弃理由。

除记录答案已包含的内容外，不要在理由中转写场景文字。只返回严格 JSON：

```
{"continuation_beyond_crop": true|false, "full_image_referent_matches": <integer count for the global question's referent in Image 2>, "crop_referent_matches": <integer count in Image 1>, "other_inscriptions_on_host": [{"description": "where/what kind of marking, WITHOUT transcribing it", "could_match_question_wording": true|false}] (for non-OCR questions use []), "verdict": "keep|rewrite|drop", "ocr_span_decision": "confirm|narrow_semantic|demote_first|demote_last"|null, "rewrite": null|{"question_zh": "...", "question_en": "...", "crop_question_zh": "...", "crop_question_en": "...", "answer": "..."}, "drop_reason": null|"concise reason", "reason": "concise image-specific audit reason"}
```

### J.6 裁剪图、整幅图像与盲答

#### CROP\_VQA。

看这张图像，用一个简短值回答问题（数字、颜色、文本串或几个词）。不要解释。

Question: `{question}`

#### CROP\_VQA\_ANCHOR\_MARKED。

细红色选择矩形是人为定位器，标识流程选定的拍摄锚点。裁剪图局部问题可以指红矩形内的物体、其部件、内容、标记或直接相关的附近物体。只用该矩形来解析该指称，而不是未标记的同类物体。绝不要把矩形本身当作拍摄内容或所请求的答案。

`<<<INSERT: CROP_VQA>>>`

#### CROP\_OCR\_VQA。

看这张图像，只转写所请求的文本或字符跨度来回答 OCR 问题。保持字符顺序，不要推断不清晰可见的字符。若所请求文本不清晰，恰好回答：`unknown`。若问题要求从指定位置起恰好 N 个字符或字母，按正常阅读顺序返回恰好 N 个字母数字字符：对 last/rightmost/ending-N 问题机械地取最后 N 个，对 first/leftmost/beginning-N 问题取前 N 个。空格与标点不计入 N。不要返回完整可见单词或任何多余字符。回答前检查响应恰好包含 N 个字符。只返回答案，不要解释。

Question: `{question}`

#### CROP\_OCR\_VQA\_ANCHOR\_MARKED。

细红色选择矩形是人为定位器，标识流程选定的拍摄锚点。裁剪图局部问题可以指红矩形内的物体、其部件、内容、标记或直接相关的附近物体。只用该矩形来解析该指称，而不是未标记的同类物体。绝不要把矩形本身转写或作为 OCR 内容返回。

`<<<INSERT: CROP_OCR_VQA>>>`

#### FULL\_IMAGE\_VQA。

看这张图像，用一个简短值回答问题（数字、颜色、文本串或几个词）。若你看不清答案，恰好回答：`unknown`。不要解释。

Question: `{question}`

#### FULL\_IMAGE\_OCR\_VQA。

看这张图像，只转写所请求的文本或字符跨度来回答 OCR 问题。保持字符顺序，即使有些字符难以辨认，也从可见图像中返回你唯一的、最佳的转写。若问题要求从指定位置起恰好 N 个字符或字母，按正常阅读顺序返回恰好 N 个字母数字字符：对 last/rightmost/ending-N 问题机械地取最后 N 个，对 first/leftmost/beginning-N 问题取前 N 个。空格与标点不计入 N。不要返回完整可见单词或任何多余字符。回答前检查响应恰好包含 N 个字符。只返回答案，不要解释。

Question: `{question}`

#### BLIND\_ANSWER。

你看不到照片。只根据问题措辞以及你学到的语言与世界知识回答。即使依赖图像的答案不确定，你也必须给出你唯一的、最可能的猜测。返回一个所请求类型的具体简短答案。绝不要回答 unknown、cannot determine、not enough information 或任何其他弃答。不要提供备选项或解释。

Question: `{question}`

#### ANSWER\_EQUIVALENCE。

你是短视觉问答答案的仔细、严格且确定性的评估者。

输入：

- Question: `{question}`
- Reference answer: `{reference}`
- Candidate answer: `{candidate}`

判断候选答案是否正确填充了问题所要求的精确答案槽。

内部按以下顺序执行：

1. 推断所请求的答案类型与问题中的每项显式约束。
2. 识别候选答案断言的唯一答案。若它给出互不相容的备选项，或添加了额外的错误答案，则拒绝。
3. 在语义上把该断言答案与参考比较。

接受无害的语法上下文、冠词、同义词、换述，以及在保留参考含义时更具体的描述。不要求相同措辞。拒绝仅相关的物体或属性、矛盾、错误答案类型、不完整答案，或额外的错误事实内容。

对普通 VQA，在问题语境中判断语义等价；当额外位置或物体上下文不改变所请求答案时，它是无害的。

内部完成比较。只输出一个标签，不要其他内容：

`<verdict>yes</verdict>`

或

`<verdict>no</verdict>`

#### OCR\_ANSWER\_EQUIVALENCE。

你在判断候选 OCR 响应是否正确回答该问题。判断视觉内容，而不是仅判断答案格式。

Question: `{question}`

Reference answer: `{reference}`

Candidate response: `{candidate}`

应用问题中的每项位置与长度约束。特别地，若问题要求前/最左/开头或后/最右/结尾 N 个字符，而候选给出了更长的转写，则在与参考比较前，机械地从该转写中取前 N 个或最后 N 个字母数字字符。当转写与其陈述答案彼此一致时，允许解释。不要仅因为参考文本出现在无关解释中就说 yes。若响应给出相互冲突的转写或答案，或推导出的所请求跨度有任何多余、缺失、重排、替换或带重音的字符差异，说 no。只忽略字母大小写与表面空格或标点。只回复一个词：yes 或 no。

### J.7 多源干扰项与 MCQ 验证

#### FULL\_DISTRACTOR\_CLUSTERING。

你是保守的语义审查器，正在从重复的整幅图像 VQA 响应中构建多项选择干扰项候选。你看不到图像，也绝不能决定哪个答案在视觉上为真。所有语义规范化与聚类都由你完成；调用方只机械地验证 ID 并统计支持数。

调用方已移除被判定与参考等价的响应，以及字面上只是「unknown」的响应。其余响应中仍可能有冗长的弃答、冲突答案或评判错误。要保守审查，而不是假定每个输入都是可用干扰项。

首先推断问题所请求的精确答案槽：例如计数、OCR 字符串、时间、颜色、材质、物体身份、动作或空间关系。然后独立审查每个响应。

响应规则：

1. committed 表示响应最终恰好选择一个具体答案。即使答案跟在推理或明确的自我纠正之后，也抽取最终选定的答案。
2. abstain 表示响应最终说 unknown、unclear、unreadable、cannot determine，或以其他方式拒绝回答。即使它提到推测性可能，也归类为 abstain。
3. conflicted 表示它留下多个互不相容的备选而未选择一个。不要任意保留其中一个备选。
4. 对 abstain 或 conflicted，`extracted_answer` 与 `cluster_id` 必须为 null。

聚类规则：

5. 只有当 committed 答案对该精确问题可互换时才聚类。在语义上规范化拼写、词形、数词、缩写与无害的周边措辞。
6. 不要合并仅相关的答案。不同计数、动作、时间、方向、材质、物体身份或 OCR 字符串都是不同答案。
7. 只有当该簇会以与参考相同的含义回答该问题时，`relation_to_reference` 才为 equivalent。由于先前的逐响应评判可能出错，此项检查仍然必需。
8. 只有当该簇提供所请求类型的答案时，`answer_slot_fit` 才为 valid。颜色对材质问题无效；只有能抽取一个干净最终答案时，解释才可接受。
9. `canonical_answer` 必须是该簇共享含义的简洁规范化形式。`representative_id` 必须命名一个实际成员，其答案支持该规范形式。

完整性契约：

- 每个提供的响应 ID 恰好处理一次。
- 每个 committed 响应恰好属于一个簇。
- 簇的 `member_ids` 必须恰好划分全部 committed 响应。
- 绝不杜撰、遗漏或重复 ID。
- 输出一个严格 JSON 对象，不要 Markdown。

Question type: `{question_type}`

Question: `{question}`

Reference answer: `{reference}`

Responses:

```
{responses}
```

输出 schema：

```
{"answer_slot": "short description of what kind of answer is requested", "responses": [{"id": "F001", "disposition": "committed|abstain|conflicted", "extracted_answer": "answer or null", "cluster_id": "C1 or null"}], "clusters": [{"cluster_id": "C1", "canonical_answer": "concise answer", "member_ids": ["F001"], "representative_id": "F001", "relation_to_reference": "equivalent|different", "answer_slot_fit": "valid|invalid", "reason": "short explanation"}]}
```

#### BLIND\_DISTRACTOR\_CLUSTERING。

你是保守的语义审查器，正在从盲答（纯文本）模型响应中构建多项选择干扰项候选。你看不到图像。所有语义规范化与聚类都由你完成；调用方只机械地验证 ID 并统计支持数。

首先推断问题所请求的精确答案槽：例如计数、OCR 字符串、时间、颜色、材质、物体身份、动作或空间关系。然后独立审查每个响应。

响应规则：

1. committed：响应最终恰好选择一个可识别答案。即使该最终答案被推理包围，也抽取它。
2. abstain：它说 unknown、cannot determine，或拒绝猜测。
3. conflicted：它留下多个互不相容的备选而未选择一个。当问题要求一种颜色时，「red or blue」这样的短语即为 conflicted。不要任意保留一个选项。
4. 对 abstain 或 conflicted，`extracted_answer` 与 `cluster_id` 必须为 null。

聚类规则：

5. 只有当 committed 答案对该精确问题可互换时才聚类。在语义上规范化拼写、词形、数词、缩写与无害的额外措辞。
6. 不要合并仅相关的答案。running、sitting、reading 与 waving 是不同动作，除非响应本身明确承诺同一个。ALPHA、BETA 与 GAMMA 是不同 OCR 字符串。这些只是抽象的边界示例；不要把它们复制到结果中。
7. 只有当该簇会以与参考相同的含义回答该问题时，`relation_to_reference` 才为 equivalent。
8. 只有当该簇提供所请求类型的答案时，`answer_slot_fit` 才为 valid。颜色对材质问题无效；只有能抽取一个干净最终答案时，解释才可接受。
9. `canonical_answer` 必须是该簇共享含义的简洁规范化形式。`representative_id` 必须命名一个实际成员，其答案支持该规范形式。

完整性契约：

- 每个响应 ID 恰好处理一次。
- 每个 committed 响应恰好属于一个簇。
- 簇的 `member_ids` 必须恰好划分全部 committed 响应。
- 绝不杜撰、遗漏或重复 ID。
- 输出一个严格 JSON 对象，不要 Markdown。

Question type: `{question_type}`

Question: `{question}`

Reference answer: `{reference}`

Responses:

```
{responses}
```

输出 schema：

```
{"answer_slot": "short description of what kind of answer is requested", "responses": [{"id": "B001", "disposition": "committed|abstain|conflicted", "extracted_answer": "answer or null", "cluster_id": "C1 or null"}], "clusters": [{"cluster_id": "C1", "canonical_answer": "concise answer", "member_ids": ["B001"], "representative_id": "B001", "relation_to_reference": "equivalent|different", "answer_slot_fit": "valid|invalid", "reason": "short explanation"}]}
```

#### VLM\_DISTRACTOR\_GENERATOR。

你是保守的视觉多项选择干扰项生成器。你恰好看到一张 `{view_name}` 图像。生成零到三个简短候选答案，它们有视觉依据，但对问题的预期目标肯定错误。参考答案不可变且正确。返回空候选胜过杜撰无支持内容。

先推断精确答案槽与参考的语义核心。每个候选都必须自然填充同一槽，且必须在该核心上不同；改动偶然形容词不构成不同答案。对物体身份，使用真正不同的核心名词，而不是参考物体的另一个有色实例。对动作，使用具体可见动作，而不是衣物、持有、外观或姿态。对计数，只使用可辩护的替代纳入边界或附近同类组。对空间/人物身份，保留所请求的关系或实体类型。

优先视觉策略，由强到弱：

1. same\_property\_other\_instance：另一相似可见物体上的所请求属性。
2. analogous\_relation\_other\_object：在类似关系或位置中可见的真正不同物体。
3. target\_other\_attribute：仅对颜色、材质或图案等标量属性，使用目标上另一个明显可见的值。
4. nearby\_same\_slot：附近物体或区域中明显可见、类型恰为所请求的值。
5. count\_near\_miss：另一个视觉上可辩护的计数，绝不是任意数字。

不同的可见来源是正面证据：对蓝色帽子的颜色问题，黄色衬衫或另一人的白帽可以提供黄色或白色。命名精确来源与关系。不要使用世界知识、通用替代、likely/perhaps/resembling 证据、unknown、参考或它的同义词。MUTUAL EXCLUSIVITY：当参考为真时，候选必须必然为假，且普通观察者必须能通过看图像反驳它。绝不提议参考的更宽或更窄改写（参考是 white stripes 时提 stripes；参考是不锈钢时提 metal）、逻辑嵌套类别（参考是正方形时提矩形——每个正方形都是矩形），或在感知上与参考过于接近、图像无法区分二者的值（正方形 vs 矩形、圆形 vs 近圆椭圆）。细红色矩形若存在，是人为定位器，绝不是图像内容。按强度排序，不要为凑三个而填充，且只输出严格 JSON。

视图纪律：

```
{view_rules}
```

Question type: `{question_type}`

Question: `{question}`

Immutable reference answer: `{reference}`

输出 schema：

```
{"candidates": [{"candidate_id": "V1", "answer": "short answer", "strategy": "strategy name", "evidence_description": "visible fact and location", "source_object": "source object or region", "relation_to_target": "why it belongs elsewhere", "quality": "high|medium|low"}], "no_candidate_reason": "reason or null"}
```

#### VISUAL\_DISTRACTOR\_CROP\_RULES。

只使用该扩展裁剪图中可见的信息。优先使用另一个局部实例的同属性值，其次是另一个同类型属性。不要假定未见整幅图像中的内容。

#### VISUAL\_DISTRACTOR\_FULL\_RULES。

只使用原生整幅图像中可见的信息。从不同物体或文本区域借用，并尽可能贴近所请求的答案槽。你无法访问拉近裁剪图。

#### VLM\_DISTRACTOR\_VALIDATOR。

你是提议的多项选择干扰项的独立保守视觉验证器。你看到生成器所用的同一张 `{view_name}` 图像。不可变参考是正确的。独立评估每个候选，不要生成替代项。候选应对预期目标为错，但可以有意从不同可见物体、属性、动作、计数边界、人或文本区域借用值。不要仅因来源在别处就拒绝。

推断精确答案槽与参考语义核心。对标量颜色、材质、图案或朝向，允许来自任何来源物体的直接可见值。对物体身份，拒绝任何共享参考核心名词/类别的候选，无论颜色、所有者或实例；只接受在类似关系中真正不同的物体。对动作，接受在别处明显执行的具体动作，但拒绝衣物、外观、穿戴、持有与静态属性。对计数，要求可辩护的可见组/边界。对空间/人物身份，保留所请求的关系/实体类型。

对 OCR，独立转写所声称的来源，而不是信任证据描述。候选必须是该转写中精确的完整 token，或问题许可的前/后 N 跨度；完整来源可能更长，因此 PORTUGAL 可以由 LICOR DE PORTUGAL 支持。单词问题要求一个单词，姓名问题拒绝裸路线/计数编号，但另一个可见单词不必与目标在现实世界中的含义相同。来源颜色与大小写影响质量，而不影响答案串本身是否契合。若文字太小而无法独立阅读，使用 reject 或 uncertain。

只有当候选具有相同答案类型/粒度、与参考核心不同、对目标并非同样正确、具有已核实视觉证据、使用有效策略且简洁/非 unknown 时才接受。MUTUAL EXCLUSIVITY IS MANDATORY：「不与参考等价」不够。拒绝任何可能与参考同时为真的候选——更宽/更窄改写（stripes vs white stripes）、逻辑嵌套类别（参考是正方形时的矩形）、或图像无法反驳的感知邻近值（正方形 vs 矩形、圆形 vs 近圆椭圆；经典颜色对：银色 vs 白色或灰色、金色 vs 黄色、米色或奶油色 vs 白色）。检验标准：仔细的观察者能否指着图像说「definitely not this」？若不能，拒绝。拒绝通用、推断、likely 或世界知识证据。decision=accept 要求 quality 为 high 或 medium。每个 ID 恰好处理一次，只输出严格 JSON。

View: `{view_name}`

Question type: `{question_type}`

Question: `{question}`

Immutable reference answer: `{reference}`

Candidates:

```
{candidates}
```

输出 schema：

```
{"answer_slot": "exact requested slot", "reference_semantic_core": "core meaning", "evaluations": [{"candidate_id": "V1", "decision": "accept|reject|uncertain", "slot_fit": true, "different_from_reference": true, "not_correct_for_target": "yes|no|unclear", "visual_source_verified": "yes|no|unclear|not_applicable", "strategy_valid": true, "ocr_length_constraint_satisfied": "yes|no|not_applicable", "independent_source_transcription": "exact text or null", "source_matches_candidate": "yes|no|unclear|not_applicable", "quality": "high|medium|low", "reason": "specific concise reason"}]}
```

#### DISTRACTOR\_ONLY\_REWRITE。

你在编辑多项选择干扰项选项。只改写列出的干扰项。参考答案是不可变上下文：绝不改写它、替换它、把它包含在输出列表中，或把任何干扰项变成参考答案。你看不到图像。

Question type: `{question_type}`

Question: `{question}`

Immutable reference answer: `{reference}`

Distractors to edit:

```
{distractors}
```

对每个干扰项：

1. 精确保留它承诺的答案。改写后必须与该干扰项对该问题语义可互换。
2. 使其成为简洁、自然、独立的答案。移除推理、模糊限定、冗余框架与句子级填充。
3. 在有用时匹配不可变参考的语法形式与表面风格，但不改动参考本身。例如，若参考把计数拼成数词，干扰项计数也拼成数词。
4. 绝不改变计数值、时间、OCR 字符序列、专名、方向、颜色、材质、否定、物体身份、动作或空间关系。含义不变时允许仅格式规范化。
5. 不要添加视觉细节、合并选项、解释选项为何错误，或提及图像或参考答案。
6. 若干扰项已经简洁、自然且风格兼容，原样复制。
7. 每个干扰项 ID 恰好处理一次。不要添加、丢弃、合并或重排 ID。只输出严格 JSON。

输出 schema：

```
{"distractors": [{"id": "D001", "rewritten_answer": "concise answer", "changed": true, "reason": "brief editing reason"}]}
```

#### MULTIPLE\_CHOICE\_POOL\_CURATOR。

你是视觉多项选择题的最终纯文本整理器。不可变参考答案正确。条目来自若干已经审查的来源：联合验证的裁剪图/整幅视图干扰项、真实的整幅图像模型错误答案、合格的盲先验答案，以及可能的 Qwen-only 视觉后备候选。你看不到图像。只做语义组织；不要杜撰、改写、改进、拆分或添加答案串。

把来源视为「该答案是一个严肃候选」的证据，绝不要把它当作保留两个语义相同选项的理由。当一个借用的标量值契合所请求槽时仍然允许：对帽子颜色问题，黄色可以来自一件可见的黄色衬衫。从问题与参考推断精确答案槽。每个条目 ID 恰好处理一次。只有当条目的答案串本身是该精确槽与语义粒度下简洁、已承诺的答案，与参考语义不同，且不是弃答、解释或畸形片段时，才标记为 eligible。拒绝相关但不同的组件、属性或类别：例如，黑色橡胶轮胎不契合参考为银色合金轮毂的轮毂样式槽，而有辐条的轮毂契合。图像正确性已在上游检查；这一步只判断答案槽契合、参考等价、与参考的互斥性以及跨条目等价。存活下来的干扰项在参考为真时必须必然为假：把任何可能与参考同时为真的更宽、更窄或逻辑嵌套描述归入 reference\_equivalent（参考是 white stripes 时的 stripes；参考是正方形时的矩形——每个正方形都是矩形；参考是不锈钢时的 metal），并把普通观察者无法因感知邻近而明确反驳的条目归入 invalid（正方形 vs 矩形、圆形 vs 近圆椭圆）。对换述、别名、仍会被接受为正确答案的更宽/更窄措辞、数值/数词等价，以及仅给同一所请求物体身份添加属性的答案，使用 reference\_equivalent。对错误答案类型、unknown/uncertain 文本，或无法独立作为选项的内容，使用 invalid。

按每个 eligible 条目对该精确问题承诺的答案聚类。跨所有来源合并语义等价项，即使措辞、冠词、大小写、词形变化、数字格式或具体程度不同。不要合并仅相关、会成为不同选项的备选。每个 eligible ID 必须恰好出现在一个簇中；被拒绝的 ID 不出现在任何簇中。从簇本身选择 `representative_id`，优先最简洁自然的现有答案。绝不输出新的规范答案。

Question type: `{question_type}`

Question: `{question}`

Immutable reference answer: `{reference}`

Pool entries:

```
{entries}
```

只输出严格 JSON：

```
{"answer_slot": "exact requested slot", "entries": [{"id": "P001", "disposition": "eligible|reference_equivalent|invalid", "cluster_id": "C1 or null", "reason": "concise semantic reason"}], "clusters": [{"cluster_id": "C1", "member_ids": ["P001"], "representative_id": "P001", "relation_to_reference": "different", "answer_slot_fit": "valid", "reason": "shared committed answer"}]}
```

#### MULTIPLE\_CHOICE\_SOLVER。

从提供的拉近裁剪图回答一道多项选择视觉问题。全局问题给出全场景身份上下文；裁剪图问题用适合该裁剪图的措辞询问同一目标。把裁剪图问题作为直接视觉任务。仔细检查图像，恰好选择一个显示的选项。不要解释、模糊限定、列出多个选项，或在裁剪图已提供答案时使用外部知识。

Question type: `{question_type}`

Global question: `{global_question}`

Crop question: `{crop_question}`

Options:

```
{options}
```

只返回严格 JSON，使用一个提供的选项标签：

```
{"choice": "A"}
```
