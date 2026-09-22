---
title: "MiMo-VL 技术报告"
title_en: "MiMo-VL Technical Report"
arxiv: 2506.03569
date: 2025-06-04
source: https://arxiv.org/abs/2506.03569
crawled: 2026-09-22
translated: 2026-09-22
---

# MiMo-VL 技术报告

> 原文：[MiMo-VL Technical Report](https://arxiv.org/abs/2506.03569) · 小米 MiMo arXiv

小米 LLM-Core

###### 摘要

我们开源 MiMo-VL-7B-SFT 与 MiMo-VL-7B-RL 两款强大的视觉语言模型，在通用视觉理解与多模态推理两方面均交付最先进性能。
MiMo-VL-7B-RL 在 40 项评测任务中的 35 项上超越 Qwen2.5-VL-7B，并在 OlympiadBench 上取得 59.4 分，超越最高 78B 参数的模型。
在 GUI 定位应用上，它以 OSWorld-G 上 56.1 分的成绩树立新标准，甚至超越 UI-TARS 等专用模型。
我们的训练将四阶段预训练（2.4 万亿 token）与整合多种奖励信号的混合在策略强化学习（Mixed On-policy Reinforcement Learning，MORL）相结合。
我们识别出在预训练阶段纳入带长思维链（Chain-of-Thought）的高质量推理数据的重要性，也识别出混合 RL 的收益——尽管多域同时优化仍面临挑战。
我们还贡献了一套覆盖 50 余项任务的综合评测套件，以促进可复现性并推动该领域发展。
模型检查点与完整评测套件可在 <https://github.com/XiaomiMiMo/MiMo-VL> 获取。

图 1：
MiMo-VL-7B 在各基准测试上的性能。

## 1 引言

视觉语言模型（VLM）已成为多模态 AI 系统的基础骨干，使自主智能体（agentic）能够感知视觉世界、对多模态内容进行推理（[Yue et al., 2024b](#bib.bib69)），并与数字环境（[Xie et al., 2024](#bib.bib62)；[OpenAI, 2025](#bib.bib40)）和物理环境（[Zitkovich et al., 2023](#bib.bib76)；[Black et al., 2024](#bib.bib4)）交互。
这些能力的重要性推动了多个维度的广泛探索，包括新颖的架构设计（[Alayrac et al., 2022](#bib.bib1)；[Team, 2024](#bib.bib52)；[Ye et al., 2025](#bib.bib66)）以及配合优化数据配方的创新训练方法（[Karamcheti et al., 2024](#bib.bib21)；[Dai et al., 2024](#bib.bib10)），带来了该领域的快速进展（[Liu et al., 2023](#bib.bib28)；[Tong et al., 2024](#bib.bib53)；[Bai et al., 2025a](#bib.bib2)）。

在本报告中，我们分享构建紧凑而强大的 VLM——MiMo-VL-7B 的努力。
MiMo-VL-7B 由三个组件构成：(1) 保留细粒度视觉细节的原生分辨率 Vision Transformer（ViT）编码器；(2) 用于高效跨模态对齐的多层感知机（MLP）投影器；(3) 专为复杂推理任务优化的 MiMo-7B（[Xiaomi, 2025](#bib.bib61)）语言模型。

MiMo-VL-7B 的研发包含两个先后衔接的训练过程：
(1) *四阶段预训练阶段*，包括投影器预热、视觉-语言对齐、通用多模态预训练与长上下文监督微调（SFT）。
在这些阶段中，我们通过策略性地整合开源数据集合成数据生成技术来策展高质量数据集，共消耗 2.4 万亿 token，并在不同阶段调整数据集分布以促进训练。该阶段产出 MiMo-VL-7B-SFT 模型。
(2) 随后的*后训练阶段*，我们引入混合在策略强化学习（MORL）——一个无缝整合多种奖励信号的新框架，覆盖感知准确性、视觉定位精度、逻辑推理能力与人类偏好。
我们采纳 GRPO（[Shao et al., 2024](#bib.bib50)）的思想，并在此阶段仅执行在策略（on-policy）梯度更新以增强训练稳定性。该阶段产出 MiMo-VL-7B-RL 模型。

在这一历程中，我们发现：

(1) 从预训练阶段起就纳入高质量、覆盖面广的推理数据，对提升模型性能至关重要。
在当前这个「思考」模型的时代，海量多模态预训练数据正在经历一场重大重估。
传统问答（QA）数据答案直接、篇幅短小，往往把模型限制在表层模式匹配并导致过拟合。
与之相反，带长思维链（CoT）的合成推理数据能够学习复杂的逻辑关系与可泛化的推理模式，提供更丰富的监督信号，显著改善性能与训练效率。
为利用这一优势，我们通过识别多样查询、用大型推理模型重新生成长 CoT 回复、并应用拒绝采样确保质量，来策展高质量推理数据。
此外，我们并非将其仅作为补充性微调数据，而是把相当数量的此类合成推理数据直接纳入后期预训练阶段——在那里延长训练可带来持续的性能提升而无饱和迹象。

(2) 混合在策略强化学习进一步提升模型性能，但要实现稳定的同步提升仍具挑战。
我们将 RL 应用于多种能力，包括推理、感知、定位与人类偏好对齐，覆盖文本、图像与视频等模态。
虽然这种混合训练方式进一步释放了模型潜力，数据域之间的干扰依然棘手。
回复长度与任务难度水平的增长趋势差异，阻碍了各项能力稳定、同步的提升。

MiMo-VL-7B-RL 在多模态能力的全谱系上交付了卓越结果。
(1) 在基础视觉感知任务上，它在同等规模的开源 VLM 中取得最先进性能，在 MMMU（[Yue et al., 2024b](#bib.bib69)）上得分 66.7，并在 40 项评测任务中的 35 项上超越 Qwen2.5-VL-7B（[Bai et al., 2025a](#bib.bib2)）。
(2) 在复杂多模态推理上，MiMo-VL-7B-RL 表现出色，在 OlympiadBench（[He et al., 2024](#bib.bib17)）上得分 59.4，超越最高 72B 参数的模型。
(3) 在面向智能体应用的 GUI 定位上，我们的模型在 OSWorld-G（[Xie et al., 2025](#bib.bib63)）上取得 54.7 分，树立了新标准，甚至超过 UI-TARS（[Qin et al., 2025b](#bib.bib46)）等专用模型。
(4) 在用户体验与偏好方面，MiMo-VL-7B-RL 在我们内部的用户偏好评测中取得所有开源 VLM 中最高的 Elo 评分，与 Claude 3.7 Sonnet 等闭源模型表现相当。

这些结果验证了我们的方法：通过 MORL 框架将强感知、复杂推理与精准定位能力相结合，MiMo-VL-7B-SFT 与 MiMo-VL-7B-RL 为开源视觉语言模型确立了新标准。
为促进透明与可复现，我们还贡献了一套覆盖 50 余项任务、附带完整提示词与协议的综合评测套件，使社区能够在本工作之上继续构建。

## 2 预训练

在本节中，我们首先介绍 MiMo-VL-7B 的架构设计，随后介绍预训练各阶段的数据策展过程与训练配方。

### 2.1 架构

MiMo-VL-7B 由三个组件组成：(1) 用于编码图像与视频等视觉输入的 Vision Transformer（ViT）；(2) 将视觉编码映射到与大语言模型（LLM）对齐的潜在空间的投影器；(3) 执行文本理解与推理的 LLM 本体。
为支持原生分辨率输入，我们采用 Qwen2.5-ViT（[Bai et al., 2025a](#bib.bib2)）作为视觉编码器。
我们用 MiMo-7B-Base（[Xiaomi, 2025](#bib.bib61)）初始化 LLM 骨干以利用其强大的推理能力，并使用随机初始化的多层感知机（MLP）作为投影器。
整体架构如图 [2](#S2.F2) 所示，模型配置详见附录 [B](#A2)。

![Refer to caption](2506.03569v1/mimo_vl_arch.png)

图 2：MiMo-VL-7B 模型架构。

| 阶段 | 阶段 1 | 阶段 2 | 阶段 3 | 阶段 4 |
| --- | --- | --- | --- | --- |
| 目的 | 投影器预热 | 视觉-语言对齐 | 多模态预训练 | 长上下文 SFT |
| 数据集 | 图文对 | 图文对 + 交错数据 | 交错数据、纯文本、OCR、定位（Grounding）、QA、视频、GUI、指令数据、推理数据 | 以上 + 长纯文本、长文档、高分辨率图像、扩展视频、长推理数据 |
| 学习率 | 1e-3 | 1e-4, 1e-5 | 1e-5 | 2.5e-5 |
| 训练 token | 300B | 167B | 1.4T | 550B |
| 序列长度 | 8K | 8K | 8K | 32K |
| 可训练组件 | 投影器 | ViT、投影器 | 全部 | 全部 |

表 1：MiMo-VL-7B 训练阶段概览。

### 2.2 预训练数据

MiMo-VL-7B 预训练数据集包含 2.4 万亿 token 的高质量、多样化多模态数据，涵盖图像、视频与文本。
这一综合数据集包括通用图像描述（caption）、交错数据、光学字符识别（OCR）数据、定位（grounding）数据、视频内容、GUI 交互、推理示例与纯文本序列。

为确保每种数据模态的质量，我们实施了针对各数据类型特点定制的专属数据策展管线。
在整个训练过程中，我们系统性地调整不同训练阶段各数据模态的比例，以同时优化训练效率与模型稳定性。
此外，我们采用基于 phash 的图像去重来消除训练数据集与评测基准之间的潜在重叠，从而将数据污染降到最低。

以下小节详述各类数据的具体处理流程。

#### 2.2.1 图像描述数据

我们的图像描述数据集构建涉及一个多阶段流程，旨在确保高质量与分布均衡。
我们首先从网络来源聚合大量公开可用的描述数据。
这一初始语料随后经历严格的去重阶段，采用图像感知哈希（phash）并结合文本过滤，得到一组精炼的唯一原始描述。

随后，以图像及其原始文本描述作为先验，我们利用一个专用描述模型对整个原始描述数据集重新生成描述。
重描述之后，我们基于语言一致性与重复模式对生成的描述施加过滤机制，以确保重描述文本的质量。
为解决固有的数据不均衡，我们采用 MetaCLIP（[Xu et al., 2023](#bib.bib64)）的方法论，构建全新的中英双语元数据。
这一关键步骤用于精炼描述分布，从而缓解高频条目的过度呈现并降低数据集噪声。

这一丝不苟流程的结晶是一个均衡、高质量且多样化的描述数据集。
至关重要的是，我们观察到这一丰富数据集显著增强了模型的泛化能力与定性性能，其优势未必能在现有专用基准的评测中完全体现。

#### 2.2.2 交错数据

我们从网页、书籍与学术论文等多种来源编纂了广泛的图文交错数据语料。
对于来自书籍与论文的内容，我们采用先进的 PDF 解析工具包进行内容抽取与清洗。
过滤流程优先保留富含世界知识的数据类型，如教科书、百科全书、手册、指南、专利与传记。
在这一交错数据集内，文本片段基于知识密度与可读性等指标进行评估。
对于视觉部分，我们实施过滤器以排除尺寸过小、宽高比异常、不安全以及视觉信息量极低的图像（例如装饰性章节标题与插图）。
最后，图文对按相关性、互补性与信息密度平衡度打分，确保保留高质量数据。
这一策展数据集显著扩充了模型的知识库，从而为其后续推理能力奠定了坚实基础。

#### 2.2.3 OCR 与定位数据

为增强模型在 OCR 与物体定位方面的能力，我们从开源数据集编纂了广泛的 OCR 与定位数据用于预训练。

对于 OCR 数据，图像涵盖来自文档、表格、通用场景、产品包装与数学公式的多样文本内容。
为提高学习难度，除标准印刷文本外，我们还特意纳入包含手写体、排版变形文本与模糊/遮挡文本的图像，从而提升模型的识别性能与鲁棒性。
对其中一部分数据，文本区域标注了边界框，使模型能够同时预测这些位置。

对于定位数据，我们的图像涵盖单物体与多物体场景。
我们进一步通过在定位提示中使用复杂的物体表述，提升模型理解复杂指代表图的能力。
在所有涉及定位的场景中，我们都使用绝对坐标进行表示。

#### 2.2.4 视频数据

我们的视频数据集主要取自公开可用的在线视频，覆盖广泛的领域、体裁与时长。
基于这些视频，我们设计了视频重描述管线，生成稠密、细粒度的事件级描述。
每条描述都以精确的起止时间戳进行时序定位，使模型发展出具备时间意识的通用视频感知能力。
从该描述数据集中，我们进一步收集一个事件时长分布均衡的子集，用于时序定位预训练。
我们还策展了总结视频全局语义的视频分析数据，例如叙事结构、风格元素与隐含意图。
这些分析段落使模型能够深入理解视频并获得扩展的世界知识。
为增强模型的对话连贯性，我们收集了关于视频的多样且有挑战性的问题，并合成相应回复。
我们还纳入开源视频描述与对话数据集，以进一步丰富视频预训练数据。

#### 2.2.5 图形用户界面数据

为增强模型在图形用户界面（GUI）中的导航能力，我们收集了覆盖移动端、网页端与桌面端等各类平台的开源预训练数据。
我们还设计了合成数据引擎，以弥补开源数据的局限并强化模型能力的特定方面。
例如，我们构建了大量中文 GUI 数据，使模型能够更好地应对中文 GUI 场景。

对于 GUI 定位（Grounding），我们同时收集元素定位与指令定位数据。
元素定位训练模型根据文本描述精确定位界面元素，建立对静态用户界面的稳健感知。
指令定位要求模型根据用户指令在截图上识别目标物体，增强对 GUI 交互逻辑的理解。
在这一部分，我们额外引入一个基于前后截图预测中间动作的预训练任务。
经验证据表明，这一方法显著改善了模型对 GUI 界面的动态感知。

对于 GUI 动作（Action），我们收集了大规模的长 GUI 动作轨迹。
为确保跨平台一致性，我们将移动端、网页端与桌面端环境的动作统一到一个标准化动作空间中。
该动作空间的详细规范见附录 [D](#A4)。
这种统一在保持平台特定功能的同时避免了动作冲突。

#### 2.2.6 合成推理数据

我们生成合成推理数据的方法始于对开源问题的全面策展。
这一多样化集合涵盖感知问答、文档问答、视频问答与视觉推理任务，并辅以从网页内容与文学作品中衍生的问题-答案对。

在对这些源问题进行初步过滤后，我们利用大型推理模型生成整合了显式推理的答案。
我们方法论的基石是严格的多阶段质量控制。
除验证答案的事实正确性外，我们还对推理过程本身施加严格过滤标准，评估思路清晰度、消除冗余并确保格式一致。

所得的高保真数据集在赋能模型方面发挥了关键作用。
它促进了 MiMo-7B-Base（[Xiaomi, 2025](#bib.bib61)）固有的强推理能力的有效继承，使其无缝迁移并适应多模态场景。
因此，我们的模型得以在广泛领域展现出强大而多样的多模态推理能力。

### 2.3 预训练阶段

我们的模型经历四个预训练阶段，如表 [1](#S2.T1) 所示：

阶段 1：我们冻结 ViT 与 LLM 组件，用图文对预热随机初始化的投影器。
这确保投影器学会将视觉概念有效映射到语言模型的表示空间，为后续训练阶段提供有信息量的梯度信号，而非来自未对齐投影器的噪声更新。

阶段 2：随后解冻 ViT，并引入交错数据以进一步加强视觉-语言对齐。
交错数据中复杂多样的图像提升了 ViT 的性能与鲁棒性。

阶段 3：在这一阶段，所有参数均可训练。
我们引入更多样的数据与任务，包括 OCR、定位、视频与 GUI 数据——累计 1.4 万亿 token——以增强模型的通用多模态能力。
为确保中期评测监控的稳定，还纳入少量 QA、指令遵循与推理数据。
此外，使用有限数量的纯文本数据以保持 MiMo-7B-Base 的文本能力。

阶段 4：这一阶段专注于增强模型对长上下文输入的适应性。
训练序列长度从 8K 扩展到 32K token。
我们引入额外数据类型，如长纯文本、高分辨率图像、长文档、扩展视频与长推理数据，以增强其长上下文处理能力。
由于长上下文打包（packing）显著增大了有效 batch size，学习率从 1e-5 调整为 2.5e-5。
相对于阶段 3，这一阶段的推理数据占比显著提高，并引入了长篇推理模式。

这四个阶段造就了强大的模型 MiMo-VL-7B-SFT。
尤其是阶段 4，模型的推理能力得到充分实现，使其能够解决高度复杂的 STEM 问题。
这种高级推理资质还能有效泛化到常见感知任务。
因此，我们的模型在各类下游基准上表现出极高性能。

## 3 后训练

在预训练建立的视觉感知能力与多模态推理之上，我们进行后训练以进一步增强 MiMo-VL-7B。
我们的方法采用新颖的混合在策略强化学习（MORL）框架，将可验证奖励强化学习（RLVR）（[Shao et al., 2024](#bib.bib50)；[Lambert et al., 2025](#bib.bib24)）与人类反馈强化学习（RLHF）（[Ouyang et al., 2022](#bib.bib41)）无缝整合，以在有挑战的推理任务与人类偏好对齐两方面改进 MiMo-VL-7B。

### 3.1 可验证奖励强化学习

RLVR 仅依赖基于规则的奖励函数，使模型能够持续自我改进。
在 MiMo-VL-7B 的后训练中，我们设计了多个可验证的推理与感知任务，其最终解可由预定义规则精确验证。

##### 视觉推理

视觉推理能力是多模态模型理解并解决同时需要视觉感知与逻辑思维的复杂问题的基础。
为促成这一能力，我们从开源社区与自有 K-12 题库编纂了多样的可验证 STEM 问题。
我们用一个 LLM 过滤证明类问题，并将带数值或符号答案的选择题改写为自由作答格式，以缓解潜在的奖励黑客（reward hacking）。
我们进一步通过全面的基于模型的难度评估来精炼题目质量，排除先进 VLM 也无法解决的题目以及过于容易的题目——以 MiMo-VL-7B rollout 通过率超过 90% 为界。
此外，我们移除了即便没有图像输入也能解答的问题。
经过数据清洗与类别均衡后，我们策展出包含 8 万道题的视觉推理数据集。
评测时，我们使用基于规则的 Math-Verify 库（https://github.com/huggingface/Math-Verify）判定回复正确性。

##### 文本推理

由于大多数视觉推理数据局限于 K-12 水平的题目，RL 训练模型的推理表现可能受限。
相比之下，纯文本推理数据集包含更多需要大学或竞赛级智力的挑战性查询。
为释放模型的全部推理潜力，我们纳入了来自 Xiaomi (2025) 的数学推理数据。
奖励使用同一个基于规则的 Math-Verify 库计算，以确保视觉与文本推理任务评测的一致性。

##### 图像定位

精准的空间定位对于模型理解图像中物体关系与空间推理至关重要。
我们在 RLVR 框架中同时纳入通用与 GUI 定位任务，以增强 MiMo-VL-7B 的定位能力。
对于边界框预测，奖励以预测框与真值框之间的广义交并比（GIoU）（[Rezatofighi et al., 2019](#bib.bib49)）计算。
对于点式输出，奖励取决于预测点是否落在真值边界框内。

##### 视觉计数

精准的计数能力对于定量视觉理解与视觉情境中的数学推理至关重要（[Chen et al., 2025a](#bib.bib5)）。
我们通过 RL 训练增强视觉计数能力，其中奖励由模型计数预测相对真值计数的准确性定义。

##### 时序视频定位

除静态图像理解与推理外，我们将 RLVR 框架扩展到动态视频内容以捕捉时序依赖。
我们纳入时序视频定位任务，要求模型定位与自然语言查询对应的视频片段（[Wang et al., 2025](#bib.bib56)）。
模型以 [mm:ss,mm:ss] 格式输出时间戳，指示目标视频片段的起止时间。
奖励以预测与真值时间片段之间的交并比（IoU）计算。

### 3.2 人类反馈强化学习

为使模型输出与人类偏好对齐并减少不良行为，我们采用人类反馈强化学习（RLHF），作为可验证奖励框架的互补方法。

##### 查询收集

查询多样性对 RLHF 的成功至关重要。
我们的方法首先从开源指令微调数据集与内部人工撰写的来源收集多模态与纯文本查询。
所有收集到的查询（无论文本或多模态）随后经历专门的筛选流程。
为进一步增强多样性，我们采用诸如基于嵌入的查询聚类并分析所得模式等技术。
至关重要的是，在策展最终查询集之前，我们平衡了中英文查询的比例，以及面向有用性与无害性的查询比例。
对每个选定的查询，我们让 MiMo-VL-7B 与其他多个顶级 VLM 生成回复。
这些回复随后由一个先进 VLM 进行成对排序，构建用于奖励模型训练的最终数据集。
值得注意的是，为缓解潜在的奖励黑客，奖励模型训练与 RLHF 过程使用同一查询集。

##### 奖励模型

我们开发了两个针对不同输入模态定制的专用奖励模型，使用 Bradley-Terry 奖励建模目标（[Ouyang et al., 2022](#bib.bib41)）训练。
纯文本奖励模型从 MiMo-7B（[Xiaomi, 2025](#bib.bib61)）初始化，以利用其强大的语言理解能力；多模态奖励模型则基于 MiMo-VL-7B 构建，以有效处理包含视觉输入的查询。
这种双模型方法确保在文本与多模态评测场景下均有最优表现。

### 3.3 混合在策略强化学习

在 MiMo-VL-7B 的后训练阶段，我们实施混合在策略强化学习（MORL），同时优化 RLVR 与 RLHF 目标。
如图 [3](#S3.F3) 所示，我们在 verl 框架（[Sheng et al., 2024](#bib.bib51)）中将基于规则与基于模型的奖励整合为统一服务，并由无缝 Rollout 引擎（[Xiaomi, 2025](#bib.bib61)）加持。

![Refer to caption](2506.03569v1/morl_pipeline.png)

图 3：后训练阶段的混合在策略强化学习。

##### 在策略 RL 配方

我们采用 GRPO（[Shao et al., 2024](#bib.bib50)）的完全在策略变体作为 RL 算法，它展现出稳健的训练稳定性与有效的探索能力（[Chen et al., 2025b](#bib.bib7)）。
对每个问题 $q$，算法从策略 $\pi_{\theta}$ 采样一组回复 $\left\{o_{1},o_{2},...,o_{G}\right\}$，并通过最大化以下目标更新策略：

$$
\mathcal{J}_{\mathrm{GRPO}}\left(\theta\right)=\mathbb{E}_{q\sim D,\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta}(\cdot|q)}\left[\frac{1}{\sum_{i=1}^{G}\left|o_{i}\right|}\sum_{i=1}^{G}\sum_{j=1}^{\left|o_{i}\right|}A_{i,j}\right] \tag{1}
$$

其中 $A_{i,j}$ 是优势，由同组回复的奖励 $\left\{r_{1},r_{2},...,r_{G}\right\}$ 计算得出：

$$
A_{i,j}=\frac{r_{i}-\mathrm{mean}(\{r_{i}\}_{i=1}^{G})}{\mathrm{std}(\{r_{i}\}_{i=1}^{G})} \tag{2}
$$

与朴素 GRPO 相比，这一在策略变体在回复 rollout 后执行单步策略更新，无需裁剪代理训练目标。
沿用 Xiaomi (2025) 的做法，我们将多项改进整合进 RL 训练配方，包括移除 KL 损失、动态采样、简单数据过滤与重采样策略。

##### 奖励即服务

MORL 过程整合了推理、感知、定位、多模态 RLHF 与纯文本 RLHF 等任务，各自需要不同的奖励函数或专用奖励模型。
为提供统一接口与近零延迟的奖励计算，我们引入奖励即服务（Reward-as-a-Service，RaaS）。
一个奖励路由器根据查询的任务类型动态选择合适的奖励函数。
为最小化延迟，奖励模型作为独立服务部署，确保可通过 HTTP 访问的可扩展奖励计算。
所有奖励都归一化到 $[0,1]$ 区间。
训练过程中不引入额外奖励，例如格式奖励。

## 4 评测

我们在 50 项任务上评测 MiMo-VL-7B，以全面评估其能力。附录 [C](#A3) 列出了评测中采用的所有基准。
我们还使用一套内部评测集评估模型性能。

| 基准 | 指标 | MiMo-VL 7B-SFT | MiMo-VL 7B-RL | Qwen2.5-VL 7B | InternVL3 8B | Gemma-3 27B-IT | GPT-4o | Claude 3.7 Sonnet |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **通用** | | | | | | | | |
| MMMU$_{val}$† | Acc. | 64.6 | **66.7** | 58.6 | 62.7 | 64.9 | 70.7 | 69.8* |
| MMMU-Pro$_{standard}$ | Acc. | 45.2 | **46.2** | 34.7* | 45.6* | 37.8* | 42.5* | 56.5* |
| MMMU-Pro$_{vision}$ | Acc. | 39.4 | **40.3** | 29.4* | 37.8* | 24.9* | 36.1* | 45.8* |
| MMBench-en$_{test}$ | Acc. | **84.5** | 84.4 | 83.5 | 83.4 | 81.6* | 84.6* | 84.8* |
| MMBench-cn$_{test}$ | Acc. | 81.9 | 82.0 | **83.4** | 82.2 | 82.4* | 84.5* | 83.7* |
| Mantis | Acc. | **78.8** | 78.3 | 74.7* | 72.8* | 70.0* | 75.6* | 75.1* |
| MME-RealWorld$_{en}$ | Acc. | 57.4 | **59.1** | 57.4 | 56.1* | 51.9* | 57.5* | 50.8* |
| MME-RealWorld$_{cn}$ | Acc. | 55.0 | 55.5 | 51.2* | **58.5*** | 47.9* | 58.5* | 40.6* |
| AI2D | Acc. | 83.2 | 83.5 | 83.9 | **85.2** | 84.5 | 82.6* | 81.4* |
| BLINK$_{val}$ | Acc. | **62.5** | 62.4 | 56.4 | 55.5 | 53.3* | 60.0 | 62.3* |
| CV-Bench | Acc. | 81.8 | **82.3** | 75.4* | 81.0* | 70.4* | 76.0* | 75.4* |
| VibeEval† | GPT-Score | 47.2 | **54.7** | 47.7* | 43.6* | 44.0* | 64.7 | 39.0* |
| VL-RewardBench† | Macro Acc. | 61.9 | **62.7** | 47.3* | 49.7* | 51.9* | 62.4 | 67.4* |
| V* | Acc. | 80.6 | **81.7** | 73.8* | 72.8* | 50.8* | 73.9 | - |
| VLMs are Blind | Acc. | 78.0 | **79.4** | 37.4* | 36.8* | 18.6* | 49.8* | 72.1* |
| PixmoCount | Acc. | **79.4** | **79.4** | 60.7* | 62.0 | 48.6* | 54.4* | 53.5* |
| CountBench | Acc. | 87.0 | **90.4** | 74.1* | 80.0* | 77.2* | 85.7* | 90.2* |
| RefCOCO$_{val}^{avg}$ | Acc.@0.5 | 85.7 | 89.6 | 87.1 | **90.1** | - | - | - |
| **文档与 OCR** | | | | | | | | |
| ChartQA† | Acc. | **92.9** | 91.7 | 90.2* | 89.6* | 78.0 | 86.7 | 92.2* |
| CharXiv$_{RQ}$† | Acc. | 54.4 | **56.5** | 42.5 | 37.6 | 29.2* | 52.0 | 63.0* |
| CharXiv$_{DQ}$† | Acc. | **87.0** | 86.8 | 73.9 | 73.6 | 63.8* | 86.5 | 89.5* |
| DocVQA$_{val}$† | Acc. | 95.2 | **95.7** | 95.5* | 89.4* | 86.6 | 93.0* | 94.1* |
| InfoVQA$_{val}$† | Acc. | 87.2 | **88.0** | 81.4* | 70.7* | 70.6 | 82.1* | 65.5* |
| SEED-Bench-2-Plus | Acc. | 71.9 | **72.4** | 70.7 | 69.7 | 66.3* | 71.1* | 72.9* |
| OCRBench† | Acc. | 87.6 | 86.6 | **89.7*** | 88.0 | 77.6* | 84.3* | 80.6* |
| **GUI** | | | | | | | | |
| VisualWebBench$_{avg}$ | Acc. | **80.2** | **80.2** | 72.9* | 62.7 | 49.7* | 80.2 | 79.3* |
| WebSrc$_{val}$ | SQuAD F1 | **96.5** | 95.3 | 94.6* | 91.1 | 89.0* | 89.1* | 91.1* |
| ScreenSpot | Center Acc. | **87.3** | 87.2 | 84.7 | 79.5 | - | 18.3 | - |
| ScreenSpot-v2 | Center Acc. | 89.5 | **90.5** | 88.0 | 81.4 | - | 18.5 | - |
| ScreenSpot-Pro$_{avg}$ | Center Acc. | 39.9 | **41.9** | 29.0 | - | - | - | - |
| OSWorld-G$_{no\_refusal}$ | Center Acc. | 54.7 | **56.1** | 37.5* | - | - | - | - |
| **视频** | | | | | | | | |
| Video-MME$_{w/o\;sub.}$ | Acc. | 66.9 | **67.4** | 65.1 | 66.3 | - | - | - |
| Video-MMMU | Acc. | **53.1** | 43.3 | 47.4 | 48.9* | - | - | - |
| EgoSchema$_{val}$ | Acc. | 60.4 | 59.6 | 62.4* | **68.2*** | - | - | - |
| Charades-STA | mIoU | 38.5 | **50.0** | 43.6 | 25.4 | - | - | - |
| **文本** | | | | | | | | |
| GPQA Diamond | Pass@1 | 56.3 | **58.3** | 30.3* | 33.5* | 40.9 | 50.6* | 66.0* |
| SuperGPQA | Pass@1 | 42.6 | **44.3** | 25.4* | 29.4* | 29.3* | 31.6* | 54.4* |
| DROP | 3-shot F1 | 82.7 | **85.1** | 67.6* | 77.5* | 72.2 | 81.5 | 87.2* |
| MMLU-Pro | EM | 59.8 | **64.8** | 48.7* | 58.3* | 45.3 | 69.1 | 81.0 |
| IF-Eval | Prompt Strict | 75.3 | 75.9 | 75.1* | 87.2* | **88.9** | 82.5 | 88.7* |

表 2：
MiMo-VL-7B 系列模型与其他模型在多样视觉-语言与文本基准上的对比。
标 * 的结果由我们的评测框架获得；† 表示使用 GPT-4o 进行评测；开源模型中的最佳结果以粗体标出。

### 4.1 评测设置

对于图像理解基准，我们将输入图像的最大像素数设为 4096 × 28 × 28，最大生成 token 数设为 32,768，解码采用贪心搜索。
对于视频基准，视频以 2 FPS 采样，最多 256 帧，总 token 上限 16,384。
对于文本评测基准，我们将最大新生成 token 数设为 32,768，temperature 为 0.6，top-p 为 0.95。
我们基于 LMMs-Eval（[Zhang et al., 2024a](#bib.bib71)）改造现有框架，以更好地适配长 CoT 推理模型。
我们进一步针对特定任务优化评测逻辑，以确保更好的评测一致性。
为促进开放研究，我们开源了我们的评测框架及所用全部提示词（https://github.com/XiaomiMiMo/lmms-eval）。

### 4.2 通用能力

表 [2](#S4.T2) 给出了评估 VLM 通用能力的基准结果。
我们的 MiMo-VL-7B 系列模型在多样的视觉-语言与文本基准上始终保持领先表现，在开源模型中创立新的最先进结果，甚至超越闭源对手。

(i) 在通用视觉-语言任务上，我们的模型取得引领开源界的卓越性能。
MiMo-VL-7B-SFT 与 MiMo-VL-7B-RL 在 MMMU$_{val}$ 上分别取得 64.6% 与 66.7%，超越 Gemma 3 27B 等规模大得多的模型。
在文档与图表理解上，MiMo-VL-7B-RL 表现出众，在 CharXiv$_{RQ}$ 上以 56.5% 取得开源最高分，显著超出 Qwen2.5-VL（42.5%）14.0 分、超出 InternVL3（37.6%）18.9 分。
(ii) 我们的模型展现出卓越的视频理解能力，同时保持强劲的文本性能。
MiMo-VL-SFT 在 Video-MMMU 上取得领先的 53.1%，MiMo-VL-RL 在 Charades-STA 上取得令人瞩目的 50.0% mIoU。
(iii) 与 MiMo-7B 相比，我们的模型在纯文本基准上保持了不错的表现。
(iv) 值得注意的是，我们的 MORL 带来了全面提升，其中最亮眼的提升出现在 VibeEval 与 CountBench 等有挑战性的基准上。

| 推理基准 | 指标 | MiMo-VL 7B-SFT | MiMo-VL 7B-RL | QVQ-72B Preview | Qwen2.5-VL 72B | Intern-VL3 78B | Qwen2.5 72B | GPT-4o | Gemini-2.5 Pro |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **多模态** | | | | | | | | | |
| OlympiadBench | Acc. | **59.4** | **59.4** | 20.4 | 37.2* | 12.3 | - | 25.9 | 69.8 |
| MathVision | Acc. | 57.9 | **60.4** | 35.9 | 38.1 | 43.2 | - | 31.2 | 69.1 |
| MathVerse†$_{vision\_only}$ | Acc. | 67.1 | **71.5** | 45.1* | 57.6 | 51.0 | - | 49.9 | 76.7 |
| DynaMath | Worst-case Acc. | **46.9** | 45.9 | 30.7 | 38.1* | 35.1 | - | 48.5 | 56.3 |
| WeMath | Strict Score | 65.1 | **66.3** | 37.7* | 50.6* | 46.1 | - | 50.6 | 78.0 |
| LogicVista | Acc. | 61.2 | **61.4** | 53.8* | 57.1* | 55.9 | - | 64.4 | 73.8 |
| MathVista†$_{mini}$ | Acc. | **81.8** | 81.5 | 71.4 | 74.8 | 72.2 | - | 63.8 | 80.9 |
| **文本** | | | | | | | | | |
| MATH500 | Pass@1 | 95.0 | **95.4** | 83.8* | 83.0 | 68.8* | 82.8* | 78.2* | 95.2 |
| AIME24 | Pass@1 | 66.4 | **67.5** | 25.2* | 16.7* | 12.2* | 19.4* | 10.9* | 92.0 |
| AIME25 | Pass@1 | 50.9 | **52.5** | 18.1* | 10.8* | 11.7* | 13.3* | 8.7* | 86.7 |

表 3：
MiMo-VL-7B 与其他模型在推理基准上的对比。
标 * 的结果由我们的评测框架获得；† 表示使用 GPT-4o 进行评测；开源模型中的最佳结果以粗体标出。

### 4.3 推理任务

表 [3](#S4.T3) 给出了多模态与文本推理基准的评测结果。
在多模态推理上，SFT 与 RL 模型在这些基准上均显著超越所有对比的开源基线。
值得注意的是，MiMo-VL-7B-SFT 超越了 Qwen2.5-VL-72B 与 QVQ-72B-Preview 等规模大得多的模型。
RL 模型在大多数推理基准上进一步提升性能。
例如，MiMo-VL-7B-RL 将 MathVision 上的准确率从 57.9% 提升到 60.4%。
MiMo-VL-7B 系列模型在纯文本基准上也展现出令人瞩目的推理能力，甚至超越 Qwen2.5-72B。
这些结果表明，我们的多模态预训练与后训练配方有效赋予了模型卓越的视觉能力与强大的文本智能。

### 4.4 GUI 任务

图 4：GUI 理解与定位结果。MiMo-VL-7B-RL 取得与 GUI 专用模型相当的结果。

此外，我们证明 MiMo-VL-7B 系列模型具备卓越的 GUI 理解与定位能力。
在表 [2](#S4.T2) 中，MiMo-VL-7B-RL 优于所有其他参与对比的通用 VLM。
在图 [4](#S4.F4) 中，我们进一步将 MiMo-VL-7B-RL 与规模相近的 GUI 专用模型（UI-TARS-1.0（[Qin et al., 2025a](#bib.bib45)）、Aguvis（[Xu et al., 2024](#bib.bib65)）、OS-Atlas（[Wu et al., 2024](#bib.bib59)））在 GUI 理解（WebSrc、VisualWebBench）与定位（Screenspot、Screenspot-v2、Screenspot-Pro、OSWorld-G）基准上进行比较。
作为通用 VLM，MiMo-VL 取得与 GUI 专用模型相当甚至更优的性能，在更具挑战性的 Screenspot-Pro 与 OSWorld-G 基准上尤为突出。

图 5：各 VLM 的 Elo 评分对比。MiMo-VL-7B-RL 在开源模型中取得最高评分，接近 Claude 3.7 Sonnet 等闭源模型的水平。

图 6：MiMo-VL-7B-SFT 在阶段 4 的训练曲线。

图 7：在策略 RL 与原始 GRPO 呈现截然不同的扩展行为：在策略 RL 的性能随数据量增加持续提升，而原始 GRPO 在约 20,000 个样本后进入平台期。

### 4.5 Elo 评分

受 ChatbotArena（[Zheng et al., 2023](#bib.bib74)）启发，我们构建了一个均衡的中英双语内部评测数据集，包含真实用户提示。
这一方法在传统基准分数之外评估用户偏好，为真实场景下的模型性能提供洞见。

沿用 Chou et al. (2024) 的方法论，我们在 MiMo-VL-7B 与竞品模型（包括领先的闭源模型以及 7B 到 72B 参数的开源 VLM）之间进行成对比较。
我们基于 GPT-4o 的评判、采用风格受控的评测协议计算 Elo 评分。
我们的评测覆盖多样的视觉-语言任务，包括多模态推理、图像理解与 GUI 交互场景，因而是用户偏好的良好代理。

如图 [5](#S4.F5) 所示，MiMo-VL-7B-RL 在所有受评开源 VLM 中取得最高 Elo 评分，在 7B 到 72B 参数的模型中排名第一。
这展示了其在评测集上的卓越用户体验，模型性能紧逼 Claude 3.7 Sonnet 等闭源模型。
此外，MORL 为 MiMo-VL-7B-SFT 带来了 22 分以上的提升。
这些结果凸显了我们模型的竞争力，并验证了训练方法的有效性。

## 5 讨论

### 5.1 在预训练中增强推理能力

图 [6](#S4.F6) 展示了 MiMo-VL-7B-SFT 在阶段 4（其最终预训练阶段）期间的表现。
在这一阶段，大量合成长篇推理数据被纳入，模型性能急剧上升，例如 MMMU 上 +9、OSWorld-G 上 +14、OlympiadBench 上 +16。
值得注意的是，模型性能持续提升而无饱和。
这些提升归因于模型推理深度的增加。
例如在 MMMU 上，经过阶段 4 后，模型每题的平均回复 token 数从 680 增长到 2.5K，表明其在解决问题时进行更细致、更深入的推理。

### 5.2 在策略 RL 对比原始 GRPO

我们用纯文本推理任务探索在策略 RL 相对原始 GRPO 的收益。
如图 [7](#S4.F7) 所示，在策略算法展现出训练数据量与性能得分之间持续的正相关。
其学习曲线在观测的训练窗口内没有饱和迹象，表明随着更多计算资源与数据还有进一步提升的潜力。
相反，原始 GRPO 算法最初表现出更高的样本效率，在训练早期即取得稳健性能。
然而这一优势是短暂的。
该算法的性能通常在约 20,000 个训练样本处饱和，此后继续训练带来的提升微乎其微。

|  |
| --- |
| Refer to caption |
| Instruction: Convert it to a table. |
| MiMo-VL-7B-RL: |
| Refer to caption |
| Refer to caption |
| Instruction: Answer the question in image. |
| MiMo-VL-7B-RL: <think>...</think> To solve for the tension in the wire, we use the equilibrium of torques about the hinge point PP. For a beam in equilibrium, the sum of clockwise torques equals the sum of counterclockwise torques. Step 1: Identify Forces and Torques - Beam’s weight (425​N425\,\text{N}): Acts downward at the beam’s midpoint (since it is uniform). The beam’s length is 8.4​m8.4\,\text{m}, so the midpoint is 8.42=4.2​m\frac{8.4}{2}=4.2\,\text{m} from PP. - Block’s weight (720​N720\,\text{N}): Acts downward at 8.4​m8.4\,\text{m} from PP. - Tension in the wire (TT): Acts at 3.4​m3.4\,\text{m} from PP at an angle of 23∘23^{\circ} above the horizontal. Only the vertical component of tension (Tsin23∘T\sin 23^{\circ}) contributes to torque (the horizontal component acts along the beam, so its torque about PP is zero). Step 2: Calculate Torques Torque is defined as force×perpendicular distance from pivot\text{force}\times\text{perpendicular distance from pivot}. - Clockwise torques (from the beam and block weights): - Beam’s weight: 425​N×4.2​m=1785​N·m425\,\text{N}\times 4.2\,\text{m}=1785\,\text{N·m} - Block’s weight: 720​N×8.4​m=6048​N·m720\,\text{N}\times 8.4\,\text{m}=6048\,\text{N·m} - Total clockwise torque: 1785+6048=7833​N·m1785+6048=7833\,\text{N·m} - Counterclockwise torque (from tension’s vertical component): - Tension’s vertical component: Tsin23∘T\sin 23^{\circ} - Perpendicular distance from PP to the wire: 3.4​m3.4\,\text{m} - Torque from tension: Tsin23∘×3.4mT\sin 23^{\circ}\times 3.4\,\text{m} Step 3: Solve for Tension In equilibrium, clockwise torque = counterclockwise torque: Tsin23∘×3.4=7833T\sin 23^{\circ}\times 3.4=7833 Solve for TT: T=78333.4×sin⁡23∘T=\frac{7833}{3.4\times\sin 23^{\circ}} Using sin⁡23∘≈0.3907\sin 23^{\circ}\approx 0.3907: T=78333.4×0.3907≈78331.328≈5900​NT=\frac{7833}{3.4\times 0.3907}\approx\frac{7833}{1.328}\approx 5900\,\text{N} Final Answer The tension in the wire is approximately 𝟓𝟗𝟎𝟎​N\boldsymbol{5900\,\text{N}}. |

  

图 8：MiMo-VL-7B 解决复杂问题的示例。

### 5.3 RL 任务间的干扰

尽管 MORL 训练增强了几乎所有受评任务上的性能，要在多样任务域上实现稳定的同步提升仍是一个重大挑战。
在训练期间，我们观察到推理任务与视觉感知及定位任务（如视觉定位与计数）之间存在差异，使得难以匹敌在单项任务上单独 RL 的性能。

潜在原因在于回复长度相反的增长趋势：推理任务在 RL 过程中鼓励更长的 CoT，而定位与计数任务则导致 CoT 缩短。
任务难度差异与奖励黑客风险也可能助长这种干扰。
我们正在积极研究这一现象的根本原因，并寻求在所有任务上实现一致且持续增长的解决方案。

## 6 案例研究

![Refer to caption](2506.03569v1/gui_case.png)

图 9：展示模型智能体能力的案例。MiMo-VL-7B 成功浏览网站，将小米 SU7 加入心愿单，并自定义车漆与内饰选项。所有截图尺寸均为 1886*1544（宽*高）。

我们在图 [8](#S5.F8) 与附录 [E](#A5) 中展示定性结果。
如 图 [8](#S5.F8) 顶部示例所示，我们的模型展现出强大的图表理解能力，成功将一张复杂的图表转换为结构良好的 markdown 表格。
此外，我们突出模型在 STEM 任务中的卓越推理能力。
在图 [10](#A5.F10) 与图 [13](#A5.F13) 所示的示例中，模型在单次回复中有效解答了多道 STEM 题目。
此外，我们的模型展现出强大的智能体能力。
如图 [9](#S6.F9) 所示，MiMo-VL-7B 成功浏览网站，将小米 SU7 加入心愿单，并自定义车漆与内饰选项。

## 7 结论

在本报告中，我们呈现了构建 MiMo-VL-7B 系列模型的努力。
依托精心策展的高质量预训练数据集与我们的 MORL 框架，MiMo-VL-7B-SFT 与 MiMo-VL-7B-RL 在受评基准上展现了最先进的性能。
我们分享开发过程中的关键观察：在后期预训练阶段纳入推理数据带来一致的性能增益、在策略 RL 相对原始 GRPO 的优势，以及在多样能力上应用 MORL 时任务干扰的挑战。
伴随发布的模型检查点，我们还开源了综合评测套件，以促进多模态研究的透明与可复现。
我们希望本工作推动强大开源视觉语言模型的发展，并为社区提供宝贵洞见。

## 参考文献

- Alayrac et al. (2022)

  J. Alayrac, J. Donahue, P. Luc, A. Miech, I. Barr, Y. Hasson, K. Lenc, A. Mensch, K. Millican, M. Reynolds, R. Ring, E. Rutherford, S. Cabi, T. Han, Z. Gong, S. Samangooei, M. Monteiro, J. L. Menick, S. Borgeaud, A. Brock, A. Nematzadeh, S. Sharifzadeh, M. Binkowski, R. Barreira, O. Vinyals, A. Zisserman, and K. Simonyan.
  Flamingo: a visual language model for few-shot learning.
  In *NeurIPS*, 2022.
- Bai et al. (2025a)

  S. Bai, K. Chen, X. Liu, J. Wang, W. Ge, S. Song, K. Dang, P. Wang, S. Wang, J. Tang, H. Zhong, Y. Zhu, M. Yang, Z. Li, J. Wan, P. Wang, W. Ding, Z. Fu, Y. Xu, J. Ye, X. Zhang, T. Xie, Z. Cheng, H. Zhang, Z. Yang, H. Xu, and J. Lin.
  Qwen2.5-vl technical report.
  *arXiv preprint arXiv:2502.13923*, 2025a.
- Bai et al. (2025b)

  S. Bai, K. Chen, X. Liu, J. Wang, W. Ge, S. Song, K. Dang, P. Wang, S. Wang, J. Tang, et al.
  Qwen2. 5-vl technical report.
  *arXiv preprint arXiv:2502.13923*, 2025b.
- Black et al. (2024)

  K. Black, N. Brown, D. Driess, A. Esmail, M. Equi, C. Finn, N. Fusai, L. Groom, K. Hausman, B. Ichter, S. Jakubczak, T. Jones, L. Ke, S. Levine, A. Li-Bell, M. Mothukuri, S. Nair, K. Pertsch, L. X. Shi, J. Tanner, Q. Vuong, A. Walling, H. Wang, and U. Zhilinsky.
  π\pi0: A vision-language-action flow model for general robot control.
  *ArXiv*, abs/2410.24164, 2024.
  URL <https://api.semanticscholar.org/CorpusID:273811174>.
- Chen et al. (2025a)

  L. Chen, L. Li, H. Zhao, Y. Song, and Vinci.
  R1-v: Reinforcing super generalization ability in vision-language models with less than $3.
  <https://github.com/Deep-Agent/R1-V>, 2025a.
  Accessed: 2025-02-02.
- Chen et al. (2021)

  X. Chen, Z. Zhao, L. Chen, D. Zhang, J. Ji, A. Luo, Y. Xiong, and K. Yu.
  Websrc: a dataset for web-based structural reading comprehension.
  *arXiv preprint arXiv:2101.09465*, 2021.
- Chen et al. (2025b)

  Y. Chen, Z. Yang, Z. Liu, C. Lee, P. Xu, M. Shoeybi, B. Catanzaro, and W. Ping.
  Acereason-nemotron: Advancing math and code reasoning through reinforcement learning.
  *arXiv preprint arXiv:2505.16400*, 2025b.
- Cheng et al. (2024)

  K. Cheng, Q. Sun, Y. Chu, F. Xu, Y. Li, J. Zhang, and Z. Wu.
  Seeclick: Harnessing gui grounding for advanced visual gui agents.
  *arXiv preprint arXiv:2401.10935*, 2024.
- Chou et al. (2024)

  C. Chou, L. Dunlap, K. Mashita, K. Mandal, T. Darrell, I. Stoica, J. Gonzalez, and W.-L. Chiang.
  Visionarena: 230k real world user-vlm conversations with preference labels.
  *ArXiv*, abs/2412.08687, 2024.
  URL <https://api.semanticscholar.org/CorpusID:274655992>.
- Dai et al. (2024)

  W. Dai, N. Lee, B. Wang, Z. Yang, Z. Liu, J. Barker, T. Rintamaki, M. Shoeybi, B. Catanzaro, and W. Ping.
  Nvlm: Open frontier-class multimodal llms.
  *arXiv preprint*, 2024.
- Deitke et al. (2024)

  M. Deitke, C. Clark, S. Lee, R. Tripathi, Y. Yang, J. S. Park, M. Salehi, N. Muennighoff, K. Lo, L. Soldaini, et al.
  Molmo and pixmo: Open weights and open data for state-of-the-art multimodal models.
  *ArXiv preprint*, abs/2409.17146, 2024.
- Du et al. (2025)

  X. Du, Y. Yao, K. Ma, B. Wang, T. Zheng, K. Zhu, M. Liu, Y. Liang, X. Jin, Z. Wei, et al.
  Supergpqa: Scaling llm evaluation across 285 graduate disciplines.
  *ArXiv preprint*, abs/2502.14739, 2025.
  URL <https://arxiv.org/abs/2502.14739>.
- Dua et al. (2019)

  D. Dua, Y. Wang, P. Dasigi, G. Stanovsky, S. Singh, and M. Gardner.
  DROP: A reading comprehension benchmark requiring discrete reasoning over paragraphs.
  In J. Burstein, C. Doran, and T. Solorio, editors, *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers)*, pages 2368–2378, Minneapolis, Minnesota, 2019. Association for Computational Linguistics.
  [10.18653/v1/N19-1246](https://doi.org/10.18653/v1/N19-1246).
  URL <https://aclanthology.org/N19-1246>.
- Fu et al. (2024a)

  C. Fu, Y. Dai, Y. Luo, L. Li, S. Ren, R. Zhang, Z. Wang, C. Zhou, Y. Shen, M. Zhang, et al.
  Video-mme: The first-ever comprehensive evaluation benchmark of multi-modal llms in video analysis.
  *arXiv preprint arXiv:2405.21075*, 2024a.
- Fu et al. (2024b)

  X. Fu, Y. Hu, B. Li, Y. Feng, H. Wang, X. Lin, D. Roth, N. A. Smith, W.-C. Ma, and R. Krishna.
  Blink: Multimodal large language models can see but not perceive.
  In *European Conference on Computer Vision*, pages 148–166. Springer, 2024b.
- Gao et al. (2017)

  J. Gao, C. Sun, Z. Yang, and R. Nevatia.
  Tall: Temporal activity localization via language query.
  In *Proceedings of the IEEE international conference on computer vision*, pages 5267–5275, 2017.
- He et al. (2024)

  C. He, R. Luo, Y. Bai, S. Hu, Z. L. Thai, J. Shen, J. Hu, X. Han, Y. Huang, Y. Zhang, et al.
  Olympiadbench: A challenging benchmark for promoting agi with olympiad-level bilingual multimodal scientific problems.
  *arXiv preprint arXiv:2402.14008*, 2024.
- Hendrycks et al. (2021)

  D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt.
  Measuring mathematical problem solving with the math dataset.
  *ArXiv preprint*, abs/2103.03874, 2021.
  URL <https://arxiv.org/abs/2103.03874>.
- Hu et al. (2025)

  K. Hu, P. Wu, F. Pu, W. Xiao, Y. Zhang, X. Yue, B. Li, and Z. Liu.
  Video-mmmu: Evaluating knowledge acquisition from multi-discipline professional videos.
  *arXiv preprint arXiv:2501.13826*, 2025.
- Jiang et al. (2024)

  D. Jiang, X. He, H. Zeng, C. Wei, M. Ku, Q. Liu, and W. Chen.
  Mantis: Interleaved multi-image instruction tuning.
  *arXiv preprint arXiv:2405.01483*, 2024.
- Karamcheti et al. (2024)

  S. Karamcheti, S. Nair, A. Balakrishna, P. Liang, T. Kollar, and D. Sadigh.
  Prismatic vlms: Investigating the design space of visually-conditioned language models.
  In *ICML*, 2024.
- Kazemzadeh et al. (2014)

  S. Kazemzadeh, V. Ordonez, M. Matten, and T. Berg.
  Referitgame: Referring to objects in photographs of natural scenes.
  In *Proceedings of the 2014 conference on empirical methods in natural language processing (EMNLP)*, pages 787–798, 2014.
- Kembhavi et al. (2016)

  A. Kembhavi, M. Salvato, E. Kolve, M. Seo, H. Hajishirzi, and A. Farhadi.
  A diagram is worth a dozen images.
  In *Computer Vision–ECCV 2016: 14th European Conference, Amsterdam, The Netherlands, October 11–14, 2016, Proceedings, Part IV 14*, pages 235–251. Springer, 2016.
- Lambert et al. (2025)

  N. Lambert, J. Morrison, V. Pyatkin, S. Huang, H. Ivison, F. Brahman, L. J. V. Miranda, A. Liu, N. Dziri, S. Lyu, Y. Gu, S. Malik, V. Graf, J. D. Hwang, J. Yang, R. L. Bras, O. Tafjord, C. Wilhelm, L. Soldaini, N. A. Smith, Y. Wang, P. Dasigi, and H. Hajishirzi.
  Tulu 3: Pushing frontiers in open language model post-training, 2025.
  URL <https://arxiv.org/abs/2411.15124>.
- Li et al. (2024a)

  B. Li, Y. Ge, Y. Chen, Y. Ge, R. Zhang, and Y. Shan.
  Seed-bench-2-plus: Benchmarking multimodal large language models with text-rich visual comprehension.
  *arXiv preprint arXiv:2404.16790*, 2024a.
- Li et al. (2025)

  K. Li, Z. Meng, H. Lin, Z. Luo, Y. Tian, J. Ma, Z. Huang, and T.-S. Chua.
  Screenspot-pro: Gui grounding for professional high-resolution computer use.
  *arXiv preprint arXiv:2504.07981*, 2025.
- Li et al. (2024b)

  L. Li, Y. Wei, Z. Xie, X. Yang, Y. Song, P. Wang, C. An, T. Liu, S. Li, B. Y. Lin, L. Kong, and Q. Liu.
  Vlrewardbench: A challenging benchmark for vision-language generative reward models.
  *ArXiv*, abs/2411.17451, 2024b.
  URL <https://api.semanticscholar.org/CorpusID:274281459>.
- Liu et al. (2023)

  H. Liu, C. Li, Q. Wu, and Y. J. Lee.
  Visual instruction tuning.
  In *NeurIPS*, 2023.
- Liu et al. (2024a)

  J. Liu, Y. Song, B. Y. Lin, W. Lam, G. Neubig, Y. Li, and X. Yue.
  Visualwebbench: How far have multimodal llms evolved in web page understanding and grounding?
  *arXiv preprint arXiv:2404.05955*, 2024a.
- Liu et al. (2024b)

  Y. Liu, H. Duan, Y. Zhang, B. Li, S. Zhang, W. Zhao, Y. Yuan, J. Wang, C. He, Z. Liu, et al.
  Mmbench: Is your multi-modal model an all-around player?
  In *European conference on computer vision*, pages 216–233. Springer, 2024b.
- Liu et al. (2024c)

  Y. Liu, Z. Li, M. Huang, B. Yang, W. Yu, C. Li, X.-C. Yin, C.-L. Liu, L. Jin, and X. Bai.
  Ocrbench: on the hidden mystery of ocr in large multimodal models.
  *Science China Information Sciences*, 67(12):220102, 2024c.
- Lu et al. (2023)

  P. Lu, H. Bansal, T. Xia, J. Liu, C. Li, H. Hajishirzi, H. Cheng, K.-W. Chang, M. Galley, and J. Gao.
  Mathvista: Evaluating mathematical reasoning of foundation models in visual contexts.
  *arXiv preprint arXiv:2310.02255*, 2023.
- MAA (2024)

  MAA.
  American invitational mathematics examination - aime.
  In *American Invitational Mathematics Examination - AIME*, 2024.
  URL <https://maa.org/math-competitions/american-invitational-mathematics-examination-aime>.
- MAA (2025)

  MAA.
  American invitational mathematics examination - aime.
  In *American Invitational Mathematics Examination - AIME*, 2025.
  URL <https://maa.org/math-competitions/american-invitational-mathematics-examination-aime>.
- Mangalam et al. (2023)

  K. Mangalam, R. Akshulakov, and J. Malik.
  Egoschema: A diagnostic benchmark for very long-form video language understanding.
  *Advances in Neural Information Processing Systems*, 36:46212–46244, 2023.
- Masry et al. (2022)

  A. Masry, D. X. Long, J. Q. Tan, S. Joty, and E. Hoque.
  Chartqa: A benchmark for question answering about charts with visual and logical reasoning.
  *arXiv preprint arXiv:2203.10244*, 2022.
- Mathew et al. (2021)

  M. Mathew, D. Karatzas, and C. Jawahar.
  Docvqa: A dataset for vqa on document images.
  In *Proceedings of the IEEE/CVF winter conference on applications of computer vision*, pages 2200–2209, 2021.
- Mathew et al. (2022)

  M. Mathew, V. Bagal, R. Tito, D. Karatzas, E. Valveny, and C. Jawahar.
  Infographicvqa.
  In *Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision*, pages 1697–1706, 2022.
- Nagaraja et al. (2016)

  V. K. Nagaraja, V. I. Morariu, and L. S. Davis.
  Modeling context between objects for referring expression understanding.
  In *Computer Vision–ECCV 2016: 14th European Conference, Amsterdam, The Netherlands, October 11–14, 2016, Proceedings, Part IV 14*, pages 792–807. Springer, 2016.
- OpenAI (2025)

  OpenAI.
  Computer-using agent: Introducing a universal interface for ai to interact with the digital world.
  2025.
  URL <https://openai.com/index/computer-using-agent>.
- Ouyang et al. (2022)

  L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. L. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, J. Schulman, J. Hilton, F. Kelton, L. Miller, M. Simens, A. Askell, P. Welinder, P. F. Christiano, J. Leike, and R. Lowe.
  Training language models to follow instructions with human feedback.
  In *NeurIPS*, 2022.
- Padlewski et al. (2024)

  P. Padlewski, M. Bain, M. Henderson, Z. Zhu, N. Relan, H. Pham, D. Ong, K. Aleksiev, A. Ormazabal, S. Phua, et al.
  Vibe-eval: A hard evaluation suite for measuring progress of multimodal language models.
  *ArXiv preprint*, abs/2405.02287, 2024.
- Paiss et al. (2023)

  R. Paiss, A. Ephrat, O. Tov, S. Zada, I. Mosseri, M. Irani, and T. Dekel.
  Teaching clip to count to ten.
  In *Proceedings of the IEEE/CVF International Conference on Computer Vision*, pages 3170–3180, 2023.
- Qiao et al. (2024)

  R. Qiao, Q. Tan, G. Dong, M. Wu, C. Sun, X. Song, Z. GongQue, S. Lei, Z. Wei, M. Zhang, et al.
  We-math: Does your large multimodal model achieve human-like mathematical reasoning?
  *arXiv preprint arXiv:2407.01284*, 2024.
- Qin et al. (2025a)

  Y. Qin, Y. Ye, J. Fang, H. Wang, S. Liang, S. Tian, J. Zhang, J. Li, Y. Li, S. Huang, et al.
  Ui-tars: Pioneering automated gui interaction with native agents.
  *arXiv preprint arXiv:2501.12326*, 2025a.
- Qin et al. (2025b)

  Y. Qin, Y. Ye, J. Fang, H. Wang, S. Liang, S. Tian, J. Zhang, J. Li, Y. Li, S. Huang, et al.
  Ui-tars: Pioneering automated gui interaction with native agents.
  *arXiv preprint arXiv:2501.12326*, 2025b.
- Rahmanzadehgervi et al. (2025)

  P. Rahmanzadehgervi, L. Bolton, M. R. Taesiri, and A. T. Nguyen.
  Vision language models are blind: Failing to translate detailed visual features into words, 2025.
  URL <https://arxiv.org/abs/2407.06581>.
- Rein et al. (2024)

  D. Rein, B. L. Hou, A. C. Stickland, J. Petty, R. Y. Pang, J. Dirani, J. Michael, and S. R. Bowman.
  Gpqa: A graduate-level google-proof q&a benchmark.
  In *First Conference on Language Modeling*, 2024.
- Rezatofighi et al. (2019)

  H. Rezatofighi, N. Tsoi, J. Gwak, A. Sadeghian, I. Reid, and S. Savarese.
  Generalized intersection over union: A metric and a loss for bounding box regression.
  In *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition*, pages 658–666, 2019.
- Shao et al. (2024)

  Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. Li, Y. Wu, et al.
  Deepseekmath: Pushing the limits of mathematical reasoning in open language models.
  *arXiv preprint arXiv:2402.03300*, 2024.
- Sheng et al. (2024)

  G. Sheng, C. Zhang, Z. Ye, X. Wu, W. Zhang, R. Zhang, Y. Peng, H. Lin, and C. Wu.
  Hybridflow: A flexible and efficient rlhf framework.
  *ArXiv preprint*, abs/2409.19256, 2024.
  URL <https://arxiv.org/abs/2409.19256>.
- Team (2024)

  C. Team.
  Chameleon: Mixed-modal early-fusion foundation models.
  *arXiv preprint arXiv:2405.09818*, 2024.
- Tong et al. (2024)

  P. Tong, E. Brown, P. Wu, S. Woo, A. J. V. IYER, S. C. Akula, S. Yang, J. Yang, M. Middepogu, Z. Wang, et al.
  Cambrian-1: A fully open, vision-centric exploration of multimodal llms.
  *Advances in Neural Information Processing Systems*, 37:87310–87356, 2024.
- Wang et al. (2024a)

  K. Wang, J. Pan, W. Shi, Z. Lu, H. Ren, A. Zhou, M. Zhan, and H. Li.
  Measuring multimodal mathematical reasoning with math-vision dataset.
  *Advances in Neural Information Processing Systems*, 37:95095–95169, 2024a.
- Wang et al. (2024b)

  Y. Wang, X. Ma, G. Zhang, Y. Ni, A. Chandra, S. Guo, W. Ren, A. Arulraj, X. He, Z. Jiang, T. Li, M. Ku, K. Wang, A. Zhuang, R. Fan, X. Yue, and W. Chen.
  Mmlu-pro: A more robust and challenging multi-task language understanding benchmark.
  In A. Globersons, L. Mackey, D. Belgrave, A. Fan, U. Paquet, J. M. Tomczak, and C. Zhang, editors, *Advances in Neural Information Processing Systems 38: Annual Conference on Neural Information Processing Systems 2024, NeurIPS 2024, Vancouver, BC, Canada, December 10 - 15, 2024*, 2024b.
  URL <http://papers.nips.cc/paper_files/paper/2024/hash/ad236edc564f3e3156e1b2feafb99a24-Abstract-Datasets_and_Benchmarks_Track.html>.
- Wang et al. (2025)

  Y. Wang, B. Xu, Z. Yue, Z. Xiao, Z. Wang, L. Zhang, D. Yang, W. Wang, and Q. Jin.
  Timezero: Temporal video grounding with reasoning-guided lvlm.
  *arXiv preprint arXiv:2503.13377*, 2025.
- Wang et al. (2024c)

  Z. Wang, M. Xia, L. He, H. Chen, Y. Liu, R. Zhu, K. Liang, X. Wu, H. Liu, S. Malladi, et al.
  Charxiv: Charting gaps in realistic chart understanding in multimodal llms.
  *Advances in Neural Information Processing Systems*, 37:113569–113697, 2024c.
- Wu and Xie (2023)

  P. Wu and S. Xie.
  V*: Guided visual search as a core mechanism in multimodal llms, 2023.
  URL <https://arxiv.org/abs/2312.14135>.
- Wu et al. (2024)

  Z. Wu, Z. Wu, F. Xu, Y. Wang, Q. Sun, C. Jia, K. Cheng, Z. Ding, L. Chen, P. P. Liang, et al.
  Os-atlas: A foundation action model for generalist gui agents.
  *arXiv preprint arXiv:2410.23218*, 2024.
- Xiao et al. (2024)

  Y. Xiao, E. Sun, T. Liu, and W. Wang.
  Logicvista: Multimodal llm logical reasoning benchmark in visual contexts.
  *arXiv preprint arXiv:2407.04973*, 2024.
- Xiaomi (2025)

  L.-C.-T. Xiaomi.
  Mimo: Unlocking the reasoning potential of language model–from pretraining to posttraining.
  *arXiv preprint arXiv:2505.07608*, 2025.
- Xie et al. (2024)

  T. Xie, D. Zhang, J. Chen, X. Li, S. Zhao, R. Cao, T. J. Hua, Z. Cheng, D. Shin, F. Lei, et al.
  Osworld: Benchmarking multimodal agents for open-ended tasks in real computer environments.
  *Advances in Neural Information Processing Systems*, 37:52040–52094, 2024.
- Xie et al. (2025)

  T. Xie, J. Deng, X. Li, J. Yang, H. Wu, J. Chen, W. Hu, X. Wang, Y. Xu, Z. Wang, Y. Xu, J. Wang, D. Sahoo, T. Yu, and C. Xiong.
  Scaling computer-use grounding via user interface decomposition and synthesis, 2025.
  URL <https://arxiv.org/abs/2505.13227>.
- Xu et al. (2023)

  H. Xu, S. Xie, X. E. Tan, P.-Y. Huang, R. Howes, V. Sharma, S.-W. Li, G. Ghosh, L. Zettlemoyer, and C. Feichtenhofer.
  Demystifying clip data.
  *arXiv preprint arXiv:2309.16671*, 2023.
- Xu et al. (2024)

  Y. Xu, Z. Wang, J. Wang, D. Lu, T. Xie, A. Saha, D. Sahoo, T. Yu, and C. Xiong.
  Aguvis: Unified pure vision agents for autonomous gui interaction.
  *arXiv preprint arXiv:2412.04454*, 2024.
- Ye et al. (2025)

  J. Ye, Z. Xie, L. Zheng, J. Gao, Z. Wu, X. Jiang, Z. Li, and L. Kong.
  Dream 7b, 2025.
  URL <https://hkunlp.github.io/blog/2025/dream>.
- Yu et al. (2016)

  L. Yu, P. Poirson, S. Yang, A. C. Berg, and T. L. Berg.
  Modeling context in referring expressions.
  In *Computer Vision–ECCV 2016: 14th European Conference, Amsterdam, The Netherlands, October 11-14, 2016, Proceedings, Part II 14*, pages 69–85. Springer, 2016.
- Yue et al. (2024a)

  X. Yue, Y. Ni, K. Zhang, T. Zheng, R. Liu, G. Zhang, S. Stevens, D. Jiang, W. Ren, Y. Sun, et al.
  Mmmu: A massive multi-discipline multimodal understanding and reasoning benchmark for expert agi.
  In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition*, pages 9556–9567, 2024a.
- Yue et al. (2024b)

  X. Yue, Y. Ni, T. Zheng, K. Zhang, R. Liu, G. Zhang, S. Stevens, D. Jiang, W. Ren, Y. Sun, C. Wei, B. Yu, R. Yuan, R. Sun, M. Yin, B. Zheng, Z. Yang, Y. Liu, W. Huang, H. Sun, Y. Su, and W. Chen.
  MMMU: A massive multi-discipline multimodal understanding and reasoning benchmark for expert AGI.
  In *CVPR*, pages 9556–9567, 2024b.
- Yue et al. (2024c)

  X. Yue, T. Zheng, Y. Ni, Y. Wang, K. Zhang, S. Tong, Y. Sun, B. Yu, G. Zhang, H. Sun, et al.
  Mmmu-pro: A more robust multi-discipline multimodal understanding benchmark.
  *arXiv preprint arXiv:2409.02813*, 2024c.
- Zhang et al. (2024a)

  K. Zhang, B. Li, P. Zhang, F. Pu, J. A. Cahyono, K. Hu, S. Liu, Y. Zhang, J. Yang, C. Li, and Z. Liu.
  Lmms-eval: Reality check on the evaluation of large multimodal models, 2024a.
  URL <https://arxiv.org/abs/2407.12772>.
- Zhang et al. (2024b)

  R. Zhang, D. Jiang, Y. Zhang, H. Lin, Z. Guo, P. Qiu, A. Zhou, P. Lu, K.-W. Chang, P. Gao, et al.
  Mathverse: Does your multi-modal llm truly see the diagrams in visual math problems?
  *ArXiv preprint*, abs/2403.14624, 2024b.
- Zhang et al. (2024c)

  Y.-F. Zhang, H. Zhang, H. Tian, C. Fu, S. Zhang, J. Wu, F. Li, K. Wang, Q. Wen, Z. Zhang, et al.
  Mme-realworld: Could your multimodal llm challenge high-resolution real-world scenarios that are difficult for humans?
  *arXiv preprint arXiv:2408.13257*, 2024c.
- Zheng et al. (2023)

  L. Zheng, W. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. P. Xing, H. Zhang, J. E. Gonzalez, and I. Stoica.
  Judging llm-as-a-judge with mt-bench and chatbot arena.
  In *NeurIPS*, 2023.
- Zhou et al. (2023)

  J. Zhou, T. Lu, S. Mishra, S. Brahma, S. Basu, Y. Luan, D. Zhou, and L. Hou.
  Instruction-following evaluation for large language models, 2023.
  URL <https://arxiv.org/abs/2311.07911>.
- Zitkovich et al. (2023)

  B. Zitkovich, T. Yu, S. Xu, P. Xu, T. Xiao, F. Xia, J. Wu, P. Wohlhart, S. Welker, A. Wahid, et al.
  Rt-2: Vision-language-action models transfer web knowledge to robotic control.
  In *Conference on Robot Learning*, pages 2165–2183. PMLR, 2023.
- Zou et al. (2024)

  C. Zou, X. Guo, R. Yang, J. Zhang, B. Hu, and H. Zhang.
  Dynamath: A dynamic visual benchmark for evaluating mathematical reasoning robustness of vision language models.
  *arXiv preprint arXiv:2411.00836*, 2024.

## 附录 A 贡献与致谢

我们谨向所有贡献者表达诚挚谢意，感谢他们宝贵的支持与付出，包括小米 LLM-Plus、Mify、MiChat 与 CloudML 团队，以及未在本文中明确列出的贡献者。
各角色内的作者按名字倒序排列。

**核心贡献者**
Zihao Yue、Zhenru Lin、Yifan Song、Weikun Wang、Shuhuai Ren、Shuhao Gu、Shicheng Li、Peidian Li、Liang Zhao、Lei Li、Kainan Bao、Hao Tian、Hailin Zhang、Gang Wang、Dawei Zhu、Cici、Chenhong He、Bowen Ye、Bowen Shen

**贡献者**
Zihan Zhang、Zihan Jiang、Zhixian Zheng、Zhichao Song、Zhenbo Luo、Yue Yu、Yudong Wang、Yuanyuan Tian、Yu Tu、Yihan Yan、Yi Huang、Xu Wang、Xinzhe Xu、Xingchen Song、Xing Zhang、Xing Yong、Xin Zhang、Xiangwei Deng、Wenyu Yang、Wenhan Ma、Weiwei Lv、Weiji Zhuang、Wei Liu、Sirui Deng、Shuo Liu、Shimao Chen、Shihua Yu、Shaohui Liu、Shande Wang、Rui Ma、Qiantong Wang、Peng Wang、Nuo Chen、Menghang Zhu、Kangyang Zhou、Kang Zhou、Kai Fang、Jun Shi、Jinhao Dong、Jiebao Xiao、Jiaming Xu、Huaqiu Liu、Hongshen Xu、Heng Qu、Haochen Zhao、Hanglong Lv、Guoan Wang、Duo Zhang、Dong Zhang、Di Zhang、Chong Ma、Chang Liu、Can Cai、Bingquan Xia

## 附录 B MiMo-VL-7B 模型配置

表 [4](#A2.T4) 详细列出了 MiMo-VL-7B 的架构与配置。

|  | 视觉编码器 | 语言模型 |
| --- | --- | --- |
| 层数（# Layers） | 32 | 36 |
| 注意力头数（# Heads） | 16 | 32 |
| 隐藏层大小 | 1280 | 4096 |
| 中间层大小 | 3456 | 11008 |
| 位置编码 | 2D RoPE | MRoPE ([Bai et al., 2025b](#bib.bib3)) |
| Patch 大小 | 14 | - |

表 4：MiMo-VL-7B 配置。我们采用 Qwen2.5-ViT（[Bai et al., 2025a](#bib.bib2)）作为视觉编码器以支持原生分辨率输入，采用 MiMo-7B-Base（[Xiaomi, 2025](#bib.bib61)）作为 LLM 骨干以利用其强大的推理能力。与 Qwen2.5-VL-7B（[Bai et al., 2025a](#bib.bib2)）的 LLM 骨干相比，我们的 LLM 在层数（36 对 28）、隐藏层大小（4096 对 3584）与中间层大小（11008 对 18944）上有所不同。

## 附录 C 评测基准

我们在 50 项多样任务上评测模型，包括：

##### 通用视觉理解

AI2D ([Kembhavi et al., 2016](#bib.bib23))、
BLINK ([Fu et al., 2024b](#bib.bib15))、
CV-Bench ([Tong et al., 2024](#bib.bib53))、
MMMU ([Yue et al., 2024a](#bib.bib68))、
MMMU-Pro（Standard 与 Vision）([Yue et al., 2024c](#bib.bib70))、
Mantis ([Jiang et al., 2024](#bib.bib20))、
MME-RealWorld（英文与中文）([Zhang et al., 2024c](#bib.bib73))、
MMBench（英文与中文）([Liu et al., 2024b](#bib.bib30))、
VibeEval ([Padlewski et al., 2024](#bib.bib42))、
VL-RewardBench ([Li et al., 2024b](#bib.bib27))、
V* ([Wu and Xie, 2023](#bib.bib58))
与 VLMs are Blind ([Rahmanzadehgervi et al., 2025](#bib.bib47))。

##### 通用定位与计数

RefCOCO ([Yu et al., 2016](#bib.bib67); [Nagaraja et al., 2016](#bib.bib39); [Kazemzadeh et al., 2014](#bib.bib22))、
CountBench ([Paiss et al., 2023](#bib.bib43))
与 PixmoCount ([Deitke et al., 2024](#bib.bib11))。

##### 文档与图表理解

ChartQA ([Masry et al., 2022](#bib.bib36))、InfographicVQA ([Mathew et al., 2022](#bib.bib38))、DocVQA ([Mathew et al., 2021](#bib.bib37))、
OCRBench ([Liu et al., 2024c](#bib.bib31))、
SEED-Bench-2-Plus ([Li et al., 2024a](#bib.bib25))
与 CharXiv（RQ/DQ）([Wang et al., 2024c](#bib.bib57))。

##### 视频理解与定位

Video-MME ([Fu et al., 2024a](#bib.bib14))、
Video-MMMU ([Hu et al., 2025](#bib.bib19))、
EgoSchema ([Mangalam et al., 2023](#bib.bib35))
与 Charades-STA [Gao et al. (2017)](#bib.bib16)。

##### GUI 理解与定位

WebSrc ([Chen et al., 2021](#bib.bib6))、VisualWebBench ([Liu et al., 2024a](#bib.bib29))、ScreenSpot ([Cheng et al., 2024](#bib.bib8))、
ScreenSpot-V2 ([Wu et al., 2024](#bib.bib59))、
ScreenSpot-Pro ([Li et al., 2025](#bib.bib26))
与 OSWorld-G ([Xie et al., 2025](#bib.bib63))。

##### 纯文本基准

GPQA ([Rein et al., 2024](#bib.bib48))、SuperGPQA ([Du et al., 2025](#bib.bib12))、DROP ([Dua et al., 2019](#bib.bib13))、MMLU-Pro ([Wang et al., 2024b](#bib.bib55))
与 IFEval ([Zhou et al., 2023](#bib.bib75))。

##### 多模态推理

OlympiadBench ([He et al., 2024](#bib.bib17))、MathVision ([Wang et al., 2024a](#bib.bib54))、MathVerse（Vision Only）([Zhang et al., 2024b](#bib.bib72))、DynaMath ([Zou et al., 2024](#bib.bib77))、WeMath ([Qiao et al., 2024](#bib.bib44))、LogicVista ([Xiao et al., 2024](#bib.bib60))
与 MathVista ([Lu et al., 2023](#bib.bib32))。

##### 文本推理

MATH500 ([Hendrycks et al., 2021](#bib.bib18))、AIME 2024 ([MAA, 2024](#bib.bib33)) 与 AIME 2025 ([MAA, 2025](#bib.bib34))。

## 附录 D GUI 动作空间

GUI 动作空间中各动作的语法与定义总结于表 [5](#A4.T5)。

| 动作 | 语法 | 定义 |
| --- | --- | --- |
| click | {"action":"click","start_point":[x,y],"text"(opt.):text} | 在给定文本的元素上点击 (x, y) 处。 |
| scroll | {"action":"scroll","direction":dir,"scroll_distance"(opt.):dist} | 沿给定方向滚动指定距离。注：向上/向下滚动 → 查看更多下方/上方内容；水平方向同理。 |
| input | {"action":"input","text":text,"start_point"(opt.):[x,y]} | 在坐标 (x, y) 处输入指定文本。 |
| drag | {"action":"drag","start_point":[x1,y1],"end_point":[x2,y2]} | 从 start_point 拖拽至 end_point。 |
| open | {"action":"open","app":app_name} | 打开指定应用 app_name。 |
| press | {"action":"press","keys":[key1,key2,...]} | 按下指定的组合键（[key1, key2,...]）。 |
| finished | {"action":"finished","status":status} | 以给定状态标记任务完成。 |
| longpress | {"action":"longpress","start_point":[x,y]} | 在坐标 (x, y) 处长按。 |
| hover | {"action":"hover"} | 将鼠标悬停于某一位置。 |
| select | {"action":"select","text":text} | 选中指定文本。 |
| wait | {"action":"wait"} | 暂停片刻。 |
| appswitch | {"action":"appswitch","app":app_name} | 切换到指定应用 app_name。 |

表 5：动作空间细节。opt. 表示可选。

## 附录 E 更多定性示例

|  |
| --- |
| Input image:Refer to caption |
| Instruction: 完成该试卷    MiMo-VL-7B: <think>...</think> 第1题：集合的交集 集合 A={0,1,2,8}A=\{0,1,2,8\}，B={−1,1,6,8}B=\{-1,1,6,8\}，交集为同时属于两个集合的元素，即 A∩B={1,8}A\cap B=\{1,8\}。 第2题：复数的实部 设 z=x+y​iz=x+yi（x,yx,y 为实数），由 i⋅z=1+2​ii\cdot z=1+2i，即 i⁡(x+y​i)=−y+x​i=1+2​ii(x+yi)=-y+xi=1+2i。 分离实部和虚部：−y=1-y=1（实部），x=2x=2（虚部）。故 zz 的实部为 22。 第3题：茎叶图的平均数 茎叶图中，茎为十位，叶为个位。分数为 89,89,90,91,9189,89,90,91,91（共5个）。 平均数为 89+89+90+91+915=4505=90\frac{89+89+90+91+91}{5}=\frac{450}{5}=90。 第4题：伪代码的循环结果 初始化 I=1I=1，S=1S=1。循环条件 I<6I<6： - 第1次循环：I=1+2=3I=1+2=3，S=2×1=2S=2\times 1=2； - 第2次循环：I=3+2=5I=3+2=5，S=2×2=4S=2\times 2=4； - 第3次循环：I=5+2=7I=5+2=7（不满足 I<6I<6，退出循环）。 最终 S=8S=8。 第5题：函数的定义域 函数 f⁡(x)=log2⁡x−1f(x)=\sqrt{\log_{2}x-1} 需满足： 1. 二次根式内非负：log2⁡x−1≥0\log_{2}x-1\geq 0； 2. 对数有定义：x>0x>0。 由 log2⁡x≥1\log_{2}x\geq 1 得 x≥21=2x\geq 2^{1}=2，故定义域为 [2,+∞)[2,+\infty)。 第6题：组合的概率 2男3女中选2人，总选法 C52=10C_{5}^{2}=10；选中2女生的选法 C32=3C_{3}^{2}=3。 概率为 310\frac{3}{10}。 第7题：正弦函数的对称轴 函数 y=sin⁡(2​x+φ)y=\sin(2x+\varphi) 关于 x=π3x=\frac{\pi}{3} 对称，即 2⋅π3+φ=k​π+π22\cdot\frac{\pi}{3}+\varphi=k\pi+\frac{\pi}{2}（k∈ℤk\in\mathbb{Z}）。 取 k=0k=0，得 φ=−π6\varphi=-\frac{\pi}{6}（满足 −π2<φ<π2-\frac{\pi}{2}<\varphi<\frac{\pi}{2}）。 第8题：双曲线的离心率 双曲线 x2a2−y2b2=1\frac{x^{2}}{a^{2}}-\frac{y^{2}}{b^{2}}=1，右焦点 F⁡(c,0)F(c,0)（c=a2+b2c=\sqrt{a^{2}+b^{2}}），渐近线 b​x−a​y=0bx-ay=0。 焦点到渐近线的距离为 |b​c|a2+b2=b\frac{|bc|}{\sqrt{a^{2}+b^{2}}}=b，由题设 b=32​cb=\frac{\sqrt{3}}{2}c。 结合 c2=a2+b2c^{2}=a^{2}+b^{2}，得 a=c2a=\frac{c}{2}，离心率 e=ca=2e=\frac{c}{a}=2。 第9题：周期函数与复合函数 f⁡(x+4)=f⁡(x)f(x+4)=f(x) 说明周期为4。 - f⁡(15)=f⁡(15−4×3)=f⁡(3)=f⁡(−1)f(15)=f(15-4\times 3)=f(3)=f(-1)（3=−1+43=-1+4）； - x∈(−2,0]x\in(-2,0] 时，f⁡(−1)=|−1+12|=12f(-1)=|-1+\frac{1}{2}|=\frac{1}{2}； - f⁡(12)=cos⁡(π2⋅12)=cos⁡π4=22f(\frac{1}{2})=\cos\left(\frac{\pi}{2}\cdot\frac{1}{2}\right)=\cos\frac{\pi}{4}=\frac{\sqrt{2}}{2}（12∈(0,2]\frac{1}{2}\in(0,2]）。 第10题：多面体的体积 正方体棱长2，面中心坐标为 (±1,0,0),(0,±1,0),(0,0,±1)(\pm 1,0,0),(0,\pm 1,0),(0,0,\pm 1)，构成正八面体。 正八面体体积为两个四棱锥之和，底面正方形边长 2\sqrt{2}，高1，体积为 2×13×2×1=432\times\frac{1}{3}\times 2\times 1=\frac{4}{3}。 第11题：函数的极值与零点 函数 f⁡(x)=2​x3−a​x2+1f(x)=2x^{3}-ax^{2}+1 在 (0,+∞)(0,+\infty) 内有且只有一个零点，导数 f′​(x)=6​x2−2​a​xf^{\prime}(x)=6x^{2}-2ax，临界点 x=0x=0 和 x=a3x=\frac{a}{3}。 当 f⁡(a3)=0f(\frac{a}{3})=0 时（极小值为0，仅1个零点），解得 a=3a=3。 f⁡(x)f(x) 在 [−1,1][-1,1] 上，f⁡(0)=1f(0)=1（最大值），f⁡(−1)=−4f(-1)=-4（最小值），和为 1+(−4)=−31+(-4)=-3。 第12题：向量垂直的条件 设 A⁡(x,2​x)A(x,2x)，A​B=(5−x,−2​x)AB=(5-x,-2x)，圆心 C⁡(x+52,x)C\left(\frac{x+5}{2},x\right)，另一交点 D⁡(1,2)D(1,2)（由圆与直线交点唯一性得）。 向量 C​D→=(−x−32,2−x)\overrightarrow{CD}=\left(\frac{-x-3}{2},2-x\right)，由 A​B→⋅C​D→=0\overrightarrow{AB}\cdot\overrightarrow{CD}=0，解得 x=3x=3。 答案 1. {𝟏,𝟖}\boldsymbol{\{1,8\}} 2. 𝟐\boldsymbol{2} 3. 𝟗𝟎\boldsymbol{90} 4. 𝟖\boldsymbol{8} 5. [𝟐,+∞)\boldsymbol{[2,+\infty)} 6. 𝟑𝟏𝟎\boldsymbol{\frac{3}{10}} 7. −𝝅𝟔\boldsymbol{-\frac{\pi}{6}} 8. 𝟐\boldsymbol{2} 9. 𝟐𝟐\boldsymbol{\frac{\sqrt{2}}{2}} 10. 𝟒𝟑\boldsymbol{\frac{4}{3}} 11. −𝟑\boldsymbol{-3} 12. 𝟑\boldsymbol{3} |

图 10：MiMo-VL-7B-RL 在一整份试卷中回答全部题目的示例。

|  |  |
| --- | --- |
| Refer to caption | Instruction: 这瓶可乐喝10罐会摄入多少克钠？ MiMo-VL-7B-RL: <think>...</think>要计算喝10罐可口可乐零度时摄入的钠量，需按以下步骤分析：  1.  步骤1：明确营养成分表信息 从图片中“营养成分表”可知：每100毫升该饮料中，钠的含量为 18毫克。 2.  步骤2：确定单罐饮料容量（行业常见规格） 可口可乐零度的罐装规格通常为 330毫升/罐（这是饮料行业的常见罐装容量，若实际容量不同需以产品标注为准，此处默认330ml）。 3.  步骤3：计算单罐钠含量 单罐（330ml）中钠的含量 = 每100ml钠含量 × 单罐容量 ÷ 100 即：18​毫克/100ml​×​330​ml​÷​100=59.4​毫克18\ \text{毫克/100ml}×330\ \text{ml}÷100=59.4\ \text{毫克} 4.  步骤4：计算10罐钠总量 10罐钠总量 = 单罐钠含量 × 10 即：59.4​毫克​×​10=594​毫克59.4\ \text{毫克}×10=594\ \text{毫克} 因此，喝10罐该款可口可乐零度，约摄入 594毫克 钠。 |
| Refer to caption | Instruction: 该发票缺失的税额应该是多少？ MiMo-VL-7B-RL: <think>...</think>要计算该发票的税额，需结合税率和价税合计金额来推导：  1.  步骤1：明确关键信息 - 发票税率：13%13\%（发票中“税率”栏显示） - 价税合计金额（大写）：壹拾壹万贰仟伍佰捌拾玖圆伍角贰分，对应小写为 112589.52元 2.  步骤2：税额的计算逻辑 发票税额 = 价税合计金额 × （1 - 税率）× 税率 （即：总价价税合计 = 不含税金额 + 税额 → 税额 = 价税合计 × 税率 ÷ (1 + 税率) ） 设不含税金额为 X\ X ，则： X+X​×​13%=112589.52X+X×13\%=112589.52 X​×​1.13=112589.52X×1.13=112589.52 X=112589.52​÷​1.13=99636.74X=112589.52÷1.13=99636.74 元【不含税金额】 税额 = 不含税金额 × 税率 = 99636.74 × 13% = 12952.78 元 |

图 11：MiMo-VL-7B-RL 借助推理解决复杂 OCR 问题的示例。

|  |  |
| --- | --- |
| Refer to caption | Instruction: How many muffin in the image? MiMo-VL-7B-RL: <think>...</think> To determine the number of muffins in the image, we analyze the 3×4 grid (12 cells total) and count muffins row by row: - Top row (row 1): Columns 1 and 3 are muffins → 2 muffins. - Middle row (row 2): Columns 2 and 4 are muffins → 2 muffins. - Bottom row (row 3): Columns 1 and 3 are muffins → 2 muffins. Adding these, 2+2+2=62+2+2=6. There are 6 muffins in the image. |
| Refer to caption | Instruction: How many cats in the image? MiMo-VL-7B-RL: <think>...</think> To determine the number of cats in the image, we can observe and count: - There is a black cat lying on the floor. - There is a white and brown cat sitting behind the black cat. Thus, the number of cats in the image is 2. |
| Refer to caption | Instruction: How many dogs in the image? MiMo-VL-7B-RL: <think>...</think> To determine the number of dogs in the image, we analyze both the printed dogs on the blanket and the real dog in the foreground:  1.  Printed dogs on the blanket: The blanket features a grid of dog faces. Counting these, we see 3 rows with 4 dogs each, so 3×4=123\times 4=12 printed dogs. 2.  Real dog in the foreground: There is 1 real dog standing in front of the blanket. Adding these together, 12+1=1312+1=13. Thus, the total number of dogs in the image is 13. |

图 12：MiMo-VL-7B-RL 解决细节感知问题的示例。

|  |  |
| --- | --- |
| Refer to caption | Instruction: answer all the questions. MiMo-VL-7B-RL: <think>...</think>  1.  Problem 7 To find xx and yy, we analyze the two right triangles formed by the height:  - **Right triangle (30° angle)**: Hypotenuse = 44. The height hh (opposite 30°) is 44⋅sin⁡(30∘)=44⋅0.5=2244\cdot\sin(30^{\circ})=44\cdot 0.5=22. The base segment yy (adjacent to 30°) is 44⋅cos⁡(30∘)=44⋅32=22​344\cdot\cos(30^{\circ})=44\cdot\frac{\sqrt{3}}{2}=22\sqrt{3}.  - **Right triangle (45° angle)**: This is a 45-45-90 triangle, so legs are equal. The height h=22h=22, so the other leg (left base segment) is also 22. Hypotenuse xx (45-45-90 ratio: leg ⋅2\cdot\sqrt{2}) is 22​222\sqrt{2}. 2.  Problem 8 For a square with diagonal d=22d=22, the side length ss relates to the diagonal by d=s​2d=s\sqrt{2}. Solving for ss: s=d2=222=11​2s=\frac{d}{\sqrt{2}}=\frac{22}{\sqrt{2}}=11\sqrt{2} (rationalizing the denominator). 3.  Problem 9 A pentagon circumscribed about a circle (tangential pentagon) has the property that the sum of the lengths of all sides equals 2×2\times the sum of the tangent segments from each vertex. However, since the problem provides the side lengths Q​Z=10QZ=10, Y​X=9YX=9, X​W=13XW=13, U​W=16UW=16, S​U=17SU=17, and the pentagon is tangential, the perimeter is the sum of these sides (as they represent the sides of the pentagon).  Perimeter =10+9+13+16+17=65=10+9+13+16+17=65. 4.  Problem 10 S​R¯\overline{SR} is tangent to ⊙Q\odot Q at RR, so Q​R⟂S​RQR\perp SR (tangent is perpendicular to radius). Thus, △​Q​R​S\triangle QRS is a right triangle with Q​R=7QR=7 (radius) and Q​S=25QS=25 (hypotenuse). By the Pythagorean theorem: S​R=Q​S2−Q​R2=252−72=625−49=576=24SR=\sqrt{QS^{2}-QR^{2}}=\sqrt{25^{2}-7^{2}}=\sqrt{625-49}=\sqrt{576}=24 5.  Problem 11 A perpendicular from the circle’s center to a chord bisects the chord. The chord length is 16, so half the chord is 162=8\frac{16}{2}=8. The distance from the center to the chord is 6, forming a right triangle with legs 6 and 8, and hypotenuse xx (radius). By the Pythagorean theorem: x=62+82=36+64=100=10x=\sqrt{6^{2}+8^{2}}=\sqrt{36+64}=\sqrt{100}=10 6.  Problem 12 Since R,S,TR,S,T are collinear and SS is between RR and TT, R​S+S​T=R​TRS+ST=RT. Substitute R​S=2​w+1RS=2w+1, S​T=w−1ST=w-1, and R​T=18RT=18:    (2​w+1)+(w−1)=18(2w+1)+(w-1)=18 Simplify: 3​w=18⟹w=63w=18\implies w=6. Substitute w=6w=6 into R​SRS: R​S=2​(6)+1=13RS=2(6)+1=13 Final Answers 7. x=22​2x=22\sqrt{2}, y=22​3y=22\sqrt{3} 8. 11​211\sqrt{2} 9. 6565 10. 2424 11. 1010 12. w=6w=6, R​S¯=13\overline{RS}=13 |

图 13：MiMo-VL-7B-RL 解决多道几何题的示例。
