---
title: "每个样本都算数：利用专家混合与高质量数据打造高效精准的代码大语言模型"
title_en: "Every Sample Matters: Leveraging Mixture-of-Experts and High-Quality Data for Efficient and Accurate Code LLM"
arxiv: 2503.17793
date: 2025-03-22
source: https://arxiv.org/abs/2503.17793
crawled: 2026-09-22
translated: 2026-09-22
---

# 每个样本都算数：利用专家混合与高质量数据打造高效精准的代码大语言模型

> 原文：[Every Sample Matters](https://arxiv.org/abs/2503.17793) · 蚂蚁集团 InclusionAI arXiv

CodeFuse 团队 & Ling 团队

蚂蚁集团

## 摘要

代码大语言模型（LLM）的最新进展已在代码生成与理解方面展现出卓越能力。
然而，要构建一个兼具全面性能与极致效率的代码 LLM 仍然充满挑战。开源社区已发布许多打破性能与效率之间权衡的尝试，例如 Qwen Coder 系列与 DeepSeek Coder 系列。
本文介绍了在该领域的又一次尝试，即 Ling-Coder-Lite。
我们利用高效的专家混合（Mixture-of-Experts，MoE）架构，配合一套高质量数据构建方法（尤其是基于程序分析的方法），构建了一个高效而强大的代码 LLM。
在 12 个代表性代码基准上，Ling-Coder-Lite 与同等规模的最先进模型（如 Qwen2.5-Coder-7B 和 DeepSeek-Coder-V2-Lite）表现相当，同时提供有竞争力的延迟与吞吐量。在实践中，相比同等规模的稠密模型，我们在不损失性能的前提下将部署资源降低了 50%。为促进该领域的进一步研究与发展，我们开源了模型以及退火与后训练阶段的大部分高质量数据。模型与数据可通过 <https://huggingface.co/inclusionAI/Ling-Coder-lite> 获取。

(a)

![Refer to caption](2503.17793v1/Ling-Coder-Evaluation_10.png)

(b)

(c)

图 1：Ling-Coder-Lite 通过利用高质量数据，在高性能与高效率之间实现了有效平衡。(a) Ling-Coder-Lite 训练过程中使用的高质量数据的大部分（约 3000 万样本）已作为开源数据发布；(b) 各同等参数规模代码 LLM 在 12 个代码基准上的平均表现；(c) 各模型在性能（以平均评测分数计）与理论计算量（以上下文长度 4096 的单次推理 TFLOPs 计）上的对比。

## 1 引言

代码 LLM，如 StarCoder 系列 [[25](#bib.bib25), [29](#bib.bib29)]、CodeLlama [[37](#bib.bib37)]、Qwen-Coder 系列 [[3](#bib.bib3), [16](#bib.bib16)]、DeepSeek-Coder 系列 [[10](#bib.bib10), [51](#bib.bib51)]、CodeStral [[31](#bib.bib31)] 与 OpenCoder [[13](#bib.bib13)]，得益于开源社区的努力已取得显著进展。最先进开源代码 LLM（如 DeepSeek-Coder-V2（236B）[[51](#bib.bib51)] 与 Qwen2.5-Coder-32B [[16](#bib.bib16)]）的代码能力已非常接近甚至超越其发布时可用的最佳专有模型。
然而，Qwen2.5-Coder-32B 等更大的模型虽然性能强劲，效率却相对较低。
构建一个同时实现强大性能与极致效率的代码 LLM 仍然相当具有挑战性。
鉴于推理效率在 AI-IDE 代码补全等实际场景中的重要性，
我们推出了 Ling-Coder-Lite，它采用 MoE 架构，总参数量为 16.8B，但激活参数仅 2.75B。与其他同等参数规模的高性能小模型（如 DeepSeek-Coder-V2-Lite（16B）[[51](#bib.bib51)]、Qwen2.5-Coder-7B [[16](#bib.bib16)] 与 OpenCoder-8B [[13](#bib.bib13)]）相比，Ling-Coder-Lite 在一系列代码评测基准上展现出相当的整体表现，同时具备有竞争力的延迟与吞吐量。

Ling-Coder-Lite 是在 Ling-Lite-Base 模型 [[43](#bib.bib43)] 的一个中间检查点之上持续训练开发的。
初始检查点在以自然语言为主的约 7T token 语料上训练，而 Ling-Coder-Lite-Base 进一步在以代码数据为主的额外 3.2T token 语料上训练，总训练量超过 10T token。指令模型 Ling-Coder-Lite 随后通过后训练对齐从 Ling-Coder-Lite-Base 获得。
持续训练分为若干阶段，每个阶段采用不同的代码数据、数学数据与自然语言数据比例。
性能提升不仅归功于精心设计的训练策略，也离不开一套高质量数据。
我们获取了约 1.4T 代码数据，包括约 836B 源代码数据、119B 代码相关文本数据、177B 合成代码数据，以及从原始代码语料衍生而来的 182B 高质量过滤代码数据与 132B 仓库级代码数据。注意，一部分高质量合成数据已在 HuggingFace 上开源（注 1：<https://huggingface.co/datasets/inclusionAI/Ling-Coder-SyntheticQA>）。
对于数学数据，我们采用与 DeepSeekMath [[40](#bib.bib40)] 类似的方法，从 Common Crawl 召回 200B 数学相关数据。
对于自然语言数据，我们直接从 Ling-Lite-Base 模型的训练语料中采样。
所有这些数据在被批准使用之前，都经过我们大数据平台上开发的严格数据构建流水线。

在后训练阶段，我们通过两阶段流程增强模型。首先，我们使用数百万条精心构建的代码样本，结合 Ling-Lite [[43](#bib.bib43)] 既有的数学与自然语言 SFT 数据，进行监督微调（SFT）[[33](#bib.bib33), [27](#bib.bib27), [7](#bib.bib7)]。其次，我们应用直接偏好优化（DPO）算法 [[35](#bib.bib35)] 使模型与人类偏好对齐。该对齐阶段纳入了数十万条代码专用偏好样本，以及 Ling-Lite [[43](#bib.bib43)] 的专业数学与自然语言偏好数据。这些步骤显著提升了 Ling-Coder-Lite 的编码能力，同时确保与人类偏好更好的对齐。值得注意的是，我们在 HuggingFace 上开源了大部分 SFT 与 DPO 代码数据（注 2：<https://huggingface.co/datasets/inclusionAI/Ling-Coder-SFT>；注 3：<https://huggingface.co/datasets/inclusionAI/Ling-Coder-DPO>）。最后，我们开发并开源了 Ling-Coder-Lite（注 4：<https://huggingface.co/inclusionAI/Ling-Coder-lite>），一个高效且高性能的代码 LLM。
我们在 12 个代表性代码基准上对模型与同等规模的最先进（SOTA）小型代码 LLM（如 Qwen2.5-Coder-7B、DeepSeek-Coder-V2-Lite 与 OpenCoder-8B）进行了广泛评测。
总体结果见图 1(b)，显示 Ling-Coder-Lite 与这些小型 SOTA 代码 LLM 的整体表现相当（12 项基准中 7 项获胜）。

主要贡献可总结如下：

- 我们推出并开源了基于 Ling-MoE 架构 [[43](#bib.bib43)] 的 Ling-Coder-Lite 与 Ling-Coder-Lite-Base 模型，总参数量 16.8B，推理时仅激活 2.75B。两个模型均以 MIT 许可证授权研究兼商用，尤其适用于要求低延迟响应的场景，如 AI-IDE 中的代码补全任务。
- 我们呈现了如何构建一个有竞争力的代码 LLM 的细节，包括高质量代码相关文本数据构建与问答（QA）数据合成技术，以及专用于数据混合与阶段调度的训练配方。
  我们公开发布了用于训练 Ling-Coder-Lite 模型的数据集的大部分，包括退火阶段合成 QA 数据的子集与一部分后训练数据，总计约 3000 万样本，如图 1(a) 所示。
- 我们在 12 个代表性代码基准上开展了广泛评测。结果表明，与同等参数规模的最先进开源代码模型（如 Qwen2.5-Coder-7B 与 DeepSeek-Coder-V2-Lite）相比，Ling-Coder-Lite 展现出相当的整体表现（12 项基准中 7 项获胜），同时提供有竞争力的效率，如图 1(c) 所示。在实践中，相比同等规模的稠密模型，我们在不损失性能的前提下实现了 50% 的部署资源降低。

## 2 数据收集与构建

Ling-Coder-Lite 从 Ling-Lite-Base [[43](#bib.bib43)] 获得的 7T 中间检查点开始，在 3.2T token 上持续训练。
在采用不同数据混合的若干持续训练阶段中，训练语料以代码数据为主，占比至少 60%。
由于自然语言与数学语料直接采样自 Ling-Lite 基座模型的训练数据，我们的重点放在代码数据上。

代码数据包括原始源代码（文件级与仓库级）、代码相关文本与合成 QA 数据。
为收集这些数据，我们主要利用来自 GitHub、Common Crawl（注 5：<https://commoncrawl.org>）与 GH Archive（注 6：<https://www.gharchive.org>）等来源的公开原始数据，并辅以开源数据集的代码数据，包括 The Stack [[20](#bib.bib20)]、the Stack v2 [[29](#bib.bib29)]、Dolma [[41](#bib.bib41)] 与 Matrix [[50](#bib.bib50)]。在以下章节中，我们将详细阐述数据预处理流水线以及构建每类数据所采用的具体方法。

### 2.1 数据构建流水线

图 2：Ling-Coder-Lite 所用代码数据的数据构建流水线。

我们利用大数据平台建立了标准化的数据构建流水线，如图 2 所示，涵盖数据收集、转换、清洗、质量检查与消融研究。Ling-Coder-Lite 预训练中使用的每个数据集都要经过该流水线，以确保其具备纳入资格。

在数据收集阶段，我们收集了截至 2024 年 6 月的 GitHub 公开仓库与截至 2024 年 8 月的 Common Crawl 数据。此外，我们还补充了 the Stack [[20](#bib.bib20), [29](#bib.bib29)] 与 Matrix [[50](#bib.bib50)] 等开源数据集语料。

在数据转换阶段，我们对原始数据进行过滤、组装并转换为适合 LLM 训练的格式。例如，我们将 Common Crawl 数据从 HTML 页面转换为纯文本，并有选择地检索代码相关内容。

随后，处理后的数据进入清洗阶段，包括基于规则的过滤、去重与安全净化。
我们开发了两套不同的过滤规则：一套用于源代码，另一套用于代码相关文本数据。
对于源代码，我们采用 StarCoder [[25](#bib.bib25), [29](#bib.bib29)] 的过滤标准（DeepSeek-Coder [[10](#bib.bib10), [51](#bib.bib51)] 亦采用），并基于质量评估反馈增加了额外规则。例如，我们排除 URL 或 IPv4/6 地址占内容超过 60% 的样本、电子邮箱地址/电话号码/日期时间字符串占比超过 50% 的样本、包含乱码字符的样本，以及行间重复率或词重复率超过 70% 的样本。
对于代码相关文本数据（如代码相关网页、Markdown 文件、notebook 数据、pull request、issue 与合成 QA 数据），我们开发了单独的一套过滤规则，因为源代码过滤规则无法直接复用，尤其是那些将最大行长限制为 1,000 字符或平均行长限制为 100 字符的规则。
代码相关文本数据还有其专属的新规则，例如移除包含图片引用、链接或占位符的样本。
应用过滤规则后，我们进一步使用近似去重方法 [[20](#bib.bib20)] 处理所得数据，并移除含有毒内容的样本。

在质量评估阶段，处理后的数据要经过完整的基于规则的校验、基于 LLM 的样本打分与人工样本打分。综合质量得分低于阈值（例如 100 分中的 85 分）的数据被判定为低质量并退回重新处理。达到质量阈值的数据进入下一阶段。

在消融研究阶段，我们使用 1B 小模型开展实验，比较对照组与实验组的表现。
对照组使用原数据集继续训练一定量 token（例如 50B）。实验组将所研究的代码数据与采样的原数据集以 1:1 比例混合，并从同一检查点开始训练相同数量的 token。只有当实验组在各类代码评测基准上的表现优于对照组时，新数据集才会被批准。

### 2.2 源代码

借助图 2 所示的构建流水线，我们获得了横跨 618 种编程语言、总计 1,100B token 的源代码数据，包括 836B token 的文件级数据、182B token 的高质量过滤数据与 132B token 的仓库级数据。
下文将介绍构建高质量源代码数据与仓库级数据的详细方法。

#### 2.2.1 高质量代码过滤

为进一步收集高质量源代码数据，我们设计了多个过滤算子来过滤低质量数据。这些过滤器主要利用代码度量、代码质量分数与仓库元数据。

代码度量过滤器评估若干关键方面，包括注释率、有效代码行数，以及通过抽象语法树分析判定的语法正确性。对于代码质量打分，我们实现了基于 FastText [[18](#bib.bib18)] 的分类模型，该模型在由教师 LLM 标注的高质量代码数据上训练。仓库元数据过滤器考虑星标数、fork 数与每个仓库内文件数量等因素。

通过应用这些全面的过滤器，我们成功识别出以较高注释率与更优质量分数为特征的高质量文件级代码数据。该过滤后数据集约 95B token，随后用于退火训练。这一严格的筛选过程确保我们的模型在典范性的编码实践与模式上训练。
作为一项独立步骤，我们利用 BERT 分类器、困惑度分布分析、askLLM [[38](#bib.bib38)] 等技术过滤出另一份高质量代码语料，总计约 87B。

#### 2.2.2 仓库级数据构建

传统代码 LLM 训练在文件级处理源代码，忽略了项目内文件间的依赖。先前研究 [[4](#bib.bib4), [25](#bib.bib25)] 强调，这种方式无法捕捉真实代码库中的结构关系，阻碍模型处理项目级代码。为此，我们实现了一种拓扑排序算法，通过识别 import 关系并对文件排序使依赖文件排在被依赖文件之前，来分析并利用仓库内的文件依赖。我们的方法超越了 DeepSeek-Coder [[10](#bib.bib10)] 基于正则的 import 识别方法，采用更精细的基于 AST（抽象语法树）的分析，分两阶段执行。

阶段 1：构建 import 依赖图。
该阶段包含四个关键步骤。首先，我们实现虚拟文件系统来处理仓库数据而无需恢复目录结构，显著减少磁盘 I/O 操作。其次，我们利用 Tree-sitter（注 7：<https://tree-sitter.github.io/tree-sitter>）为受支持的语言生成 AST，从而在 AST 层面而非使用正则模式精确识别 import 语句。第三，对每个 import 语句，我们通过基于路径的搜索与包命名约定分析确定仓库内对应的模块文件，并在复杂情况下结合两种方法。最后，我们构建有向图，其中节点表示文件、边表示 import 依赖。

阶段 2：字典序拓扑排序。
我们的排序算法扩展了字典序拓扑排序以同时适应 DAG（有向无环图）与含环图，确保得到唯一且稳定的排序。过程从输入校验开始，确认图是有向的。接着为每个节点分配唯一 ID 以保证一致处理，然后计算每个节点的入度即入边数量。在迭代处理中，找出入度最小的节点，并在并列时按字典序确定优先级。若最小入度大于零，则选择一个节点来「打破」环，并将其从图中移除。随后更新其后继节点的入度，重复这些步骤直至图为空。

该算法产生一个全序：对于原图中的每条边 $(u,v)$，$u$ 在结果中排在 $v$ 之前；当存在多个有效排序时，以字典序为准。

我们按仓库聚合经图 2 所示流水线构建的文件级代码数据。仓库内每个文件随后使用所提出的仓库拼接方法排序并拼接成完整样本。值得注意的是，我们的拼接算法支持 16 种编程语言，但无法分析隐式 import 依赖或来自动态代码调用的依赖。因此，部分仓库无法成功拼接。对于拼接成功的案例，我们基于若干仓库属性开展高质量过滤，包括每文件平均代码质量分数（使用 FastText 模型获得）、平均注释率与平均有效代码行数。最终，我们获得 132B 仓库级代码数据。

### 2.3 代码相关数据

我们还处理并获得了 119B 代码相关文本数据，包括代码相关网页、代码-注释对、notebook、Markdown 文件、GitHub Pull Request（PR）与 GitHub issue。

#### 2.3.1 代码相关网页

与 DeepSeek-Coder-V2 [[51](#bib.bib51)]、DeepSeekMath [[40](#bib.bib40)]、Qwen2.5-Coder [[16](#bib.bib16)] 与 OpenCoder [[13](#bib.bib13)] 类似，我们也开发了从 Common Crawl 超过 2,800 亿个网页中召回代码相关网页的流水线，得到 66B 数据集。

图 3：从 Common Crawl 召回代码相关数据的流水线。

我们的召回过程如图 3 所示，包含三个阶段。第一阶段，遵循 DeepSeek-Coder-V2 的方法论，我们以 50 万 StackOverflow 样本为正例、50 万随机采样的 Common Crawl 页面（从原始 HTML 解析为纯文本）为负例，训练 FastText [[19](#bib.bib19)] 分类器。值得注意的是，我们修改了 FastText 库（注 8：<https://github.com/facebookresearch/fastText>）源码以支持 BPE（Byte-Pair Encoding）分词，与 DeepSeek-Coder-V2 的实现对齐。随后将该分类器部署到我们的大数据平台，从 2,800 亿 Common Crawl 页面中召回代码相关网页。初步质量检查显示第一轮检索的数据质量欠佳。
第二阶段，我们与 DeepSeek-Coder-V2 分道扬镳，采用 askLLM [[38](#bib.bib38)] 策略提升训练数据质量。具体而言，我们利用开源 LLM 对随机采样的 Common Crawl 页面与初步召回结果按三个维度打分：代码相关性、教育价值与数据洁净度（1-5 分制）。得分 $\geq 3$ 的样本（结合精选 StackOverflow 样本）构成正例集（约 100 万），得分 <3 的样本构成负例集（约 100 万）。尽管用这批精炼数据重新训练了 FastText 模型，质量检查仍显示改进不足。
最后阶段，我们实现了基于 DistilRoberta [[39](#bib.bib39)] 的过滤系统。利用第二阶段 LLM 生成的分数，我们在 DistilRoberta-base（注 9：<https://huggingface.co/distilbert/distilroberta-base>）模型上微调了一个打分模型。该模型评估第二阶段的召回结果，最终仅选择得分为最高分（5/5）的页面进入最终数据集，产出 66B 数据。

值得注意的是，我们发现将 Common Crawl 原始页面解析为纯文本的质量对结果影响显著。为此，我们针对数学与代码内容实施了解析质量的定向改进。

#### 2.3.2 代码-注释对

我们从 the Stack v2 及其他拥有至少 10 个星标的热门 GitHub 仓库抓取了约 14.6 亿对代码-注释对（简称 COCO），获得了一组高质量数据。
为确保数据质量，我们沿用先前在代码变更理解上的尝试 [[23](#bib.bib23)]，开展两阶段净化流程：(1) 基于规则的净化；(2) 基于蒸馏的净化。
第一阶段移除语法上低质量的 COCO，第二阶段专注于确保其语义质量。

- 基于规则的净化。
  语法净化使用现有文献 [[34](#bib.bib34), [30](#bib.bib30), [6](#bib.bib6)] 中常见的七条启发式规则（i–vii）。
  第一步基于 MD5 值去除重复的 COCO（i）。
  随后，我们对每个 COCO 的代码与注释设置约束。
  对于代码，我们要求每个 COCO 由 30 至 100,000 个字符组成（ii），且行数为 1 至 100 行（iii）。
  对于注释，每个 COCO 应非空（iv），字符数在 30 至 100,000 之间（v），特殊字符占比低于 80%（vi），如 /、@、*、# 等。
  最后，带有特殊标注的注释（vii），如 TODO:、BUG: 与 FIXME:，被排除在外，因为开发者通常用它们传达与代码语义无关的信息。
- 基于蒸馏的净化。
  语义净化确保每个 COCO 的注释与其代码的语义（如行为、意图、功能等）一致。
  由于未找到合适的现有工具，我们通过使用教师 LLM 蒸馏的数据训练一个专门的小模型来完成该过程；这是一种流行且有效的技术 [[47](#bib.bib47), [36](#bib.bib36)]。
  最初，我们提示教师 LLM 逐步评估 25.6K 精选 COCO 的代码与注释之间的语义一致性。
  具体而言，对每个 COCO，我们指示它：
  (a) 逐行拆解所提供的代码，详述每一行完成的功能；
  (b) 将逐行的详细分析概括为一句捕捉代码精髓的简洁语句；
  (c) 审阅所提供的注释，指出其核心信息，分析其与步骤 a、b 概括的一致性，并给出清晰、逐步的评估理由；
  (d) 得出所提供代码与注释之间的总体一致性结论（真或假）以结束评估。
  随后，我们使用标注好的 25.6K COCO 微调小型语言模型 Qwen2-0.5B，其中 19.2K 用于训练，其余平均分为测试集与验证集（注 10）。
  微调后的模型在蒸馏数据上取得 0.9021 精确率、0.9198 召回率与 0.9109 F1。
  为增强 Qwen2-0.5B 的推理能力，我们的微调过程采用自回归方式，目标是让小模型学习逐步的思维链。
  最后，我们利用微调后的模型对剩余数据进行推理与标注；我们移除被标注为负面的样本。

最终，我们的净化流程产出约 17B token，横跨 18 种主流编程语言，包括 Java、JavaScript、Python、C++、Shell、Lua 等。

#### 2.3.3 其他代码相关数据

Pull Request。遵循 StarCoder2 [[29](#bib.bib29)]，我们采用类似方法构建 Pull Request（PR）数据。首先，从 GH Archive 下载 PR 的文本数据。随后，从这些文本数据中提取 commit 信息。接着，基于提取的 commit 信息从 GitHub 抓取关联的 commit diff 代码数据。然后，我们采用与 StarCoder2 相同的数据清洗策略净化这些代码数据。最后，按照 StarCoder2 详述的方法将属于单个 Pull Request 的文本与代码数据拼接。我们的 PR 过滤策略与 StarCoder2 的一个差异在于：排除了基础文件超过三个的 PR，同时确保所有相关文件都保留为相应 PR 的上下文。我们的处理涵盖了 2015 至 2018 年间 GitHub 上的全部 Pull Request，最终得到 110 万个 PR、总计 8B token 的语料。

Notebook。我们还参考 StarCoder2 的方法论，基于 notebook 数据构建脚本数据。我们从 GitHub 抓取全部 notebook 数据，经过构建与清洗后最终获得 14B 数据。我们的消融实验表明，该数据显著增强了模型能力。
我们还收集并处理了来自 The Stack [[20](#bib.bib20)] 的开源 notebook 数据，以及来自 Kaggle（注 11：<https://www.kaggle.com>）的 notebook 数据，额外获得 3B 数据。
我们推测这归因于 notebook 数据的固有特性。与典型代码数据相比，notebook 数据包含更丰富的文本信息，代码块通常承担独立功能，上下文一般局限于单个文件内。这些特性可能有助于模型学习文本与代码之间的紧密联系。

Markdown。
与 StarCoder 系列 [[25](#bib.bib25), [29](#bib.bib29)] 和 DeepSeek-Coder-V2 [[51](#bib.bib51)] 类似，我们也将从 GitHub 收集的 Markdown 文件视为一类代码相关数据。鉴于 GitHub 的原始 Markdown 文件常包含非代码相关内容甚至有毒内容，我们选择使用为从 Common Crawl 召回代码相关网页数据而训练的 DistilRoberta 打分模型，先评估其代码相关性与教育价值。只有具备高代码相关性与教育价值的样本才进入后续的清洗、质量检查与消融研究流程。最终，我们获得约 11B Markdown 数据。

### 2.4 合成数据

随着模型训练的快速进步与公开互联网数据的迅速消耗，合成数据变得日益重要且可行。
在 Ling-Coder-Lite 的训练中，我们使用两类合成数据。第一类使用 SOTA 开源 LLM 通过 Magpie [[48](#bib.bib48)] 方法生成，用于预训练阶段，总计约 163B token。
第二类为后训练合成数据，使用类似 OSS-Instruct [[45](#bib.bib45)] 与 Evol-Instruct [[46](#bib.bib46)] 的方法生成，包含超过 1,000 万样本。该数据的一部分与其他中等质量的 SFT 数据一起，作为退火阶段的预训练数据使用，总计约 14B。

#### 2.4.1 使用 Magpie 合成

Magpie [[48](#bib.bib48)] 是一条数据合成流水线，旨在不依赖提示工程或种子问题的情况下产出高质量对齐数据。它通过预查询模板提示已对齐 LLM 采样指令，直接构建指令数据。通常，这些已对齐 LLM 的输入由预查询模板、查询内容与后查询模板组成。
例如，Llama2-Chat 模型接受形如 "[INST] Hi! [/INST]" 的输入，其中 "[INST]" 充当预查询模板、"[/INST]" 充当后查询模板。
当仅提供预查询模板时，LLM 自回归地生成查询内容；一旦组装完整输入，即可获得 LLM 的回复。生成过程包含两个主要步骤：

- 指令生成。Magpie 基于 LLM 预定义的指令模板构建输入查询。该查询规定了指令提供者的角色（如用户），但不包含任何具体指令。自回归 LLM 已在按该模板格式化的指令数据上微调，因而能在输入 Magpie 构造的查询时自主生成指令。
- 回复生成。Magpie 将生成的指令传给 LLM，后者处理并产生相应回复。

对于特定的教师 LLM，我们采用 Magpie 技术合成覆盖多种编码场景的指令数据。这些场景包括多种编程语言的文本到代码、测试用例生成、代码解释、代码修复、代码重构与代码执行预测，
均旨在增强 Ling-Coder-Lite 的编码能力。
通过该过程，我们最终合成约 1.5 亿对经清洗与去毒的问答对，约 163B token，随后用于退火阶段。该合成数据集在提升模型跨多样编程语境理解与生成代码的能力方面发挥了关键作用。

实践考量。对于指令生成过程，建议将 TEMPERATURE 与 TOP-P 都设置为相对较高的值，以促进生成指令的多样性。相反，在回复生成期间，建议使用贪心解码或较低的 temperature，因为高概率 token 很可能源自 LLM 的训练数据。

#### 2.4.2 指令数据合成。

借鉴 OSS-Instruct [[45](#bib.bib45)] 与 Evol-Instruct [[46](#bib.bib46)] 的方法，我们稍作修改并将其结合用于合成指令数据。部分合成指令数据用作预训练数据，另一部分分配给微调。具体而言，我们提出两种合成方法：自下而上（Bottom-Up）合成与自上而下（Top-Down）合成。

图 4：自下而上指令数据合成流水线。

自下而上合成。
图 4 展示了自下而上方法的合成过程。我们首先收集一组种子（代码片段与代码相关文本），与文献 [[14](#bib.bib14)] 类似。
第一阶段，我们使用最先进的 LLM 从每个种子样本中提取层次化知识，涵盖高层主题及其对应的详细要点。
第二阶段，受 Evol-Instruct [[46](#bib.bib46)] 启发，我们通过提示 LLM 为每条知识生成五个演化变体来扩展知识集，确保这些变体与原知识相关但又有区别。
第三阶段，我们基于演化后的知识生成问题。应用来自 Arena [[26](#bib.bib26)] 的技术，我们将疑问句转换为陈述句，并为每条知识生成七个唯一问题。
如此一来，原始种子问题被扩展
$(K+1)\times N$ 倍。在实验中，我们设
$K=7$ 且 $N=5$，并认识到更大的值可能导致冗余。最终，该过程生成超过 1,000 万条指令样本。

所有合成指令数据，无论用于微调还是预训练，都首先经过标准的 SFT 数据清洗流水线，包括基于规则的异常检测、清洗、去毒、质量检查、消融研究等。

自上而下合成。
在自下而上的合成方法中，合成问题的知识受限于种子问题，即便经过知识演化也是如此。为增强合成数据的多样性，我们提出利用各类编程书籍知识的自上而下合成流水线。
我们利用 LLM 基于约 200 本与主流编程语言（如 Python）及其库（如 PyTorch）相关的书名生成内容。我们并非复现整本书，而是指示 LLM 创建层次化的知识结构。该过程分两步：

- LLM 为每个书名生成目录，按章、节、小节三级结构组织，形成一棵树。
- 接着，LLM 为每个叶节点（节或小节）提供细粒度知识，并指明其上层节点，以区分不同书籍中相似的小节（如 Python 与 C 书中都有「条件语句」）。

子主题表示知识点内更细的细节层级，由 LLM 决定是否有必要。为提升生成问题的区分度，我们以如下格式提供每个叶节点到根节点的路径："属于书籍 [BOOK] 中章节 [CHAPTER] 下小节 [SECTION] 的 [LEAF]"。

完成这些步骤后，我们获得每本书的完整知识树。我们提取从子主题到书名的所有知识路径，并提示 LLM 基于这些路径创建编程问题。LLM 还可以纳入其他相关主题以创建更具挑战性的问题。最终，我们合成约 120 万个问题，然后使用 LLM 为每个问题生成答案。

## 3 模型架构与训练细节

### 3.1 模型架构

Ling-Coder-Lite 在 Ling-Lite-Base [[43](#bib.bib43)] 之上持续训练，后者是总参数量 16.8B、激活参数量 2.75B 的专家混合（MoE）架构。Ling-Coder-Lite 配置了 28 层 transformer 与 2048 的隐藏维度。每个 MoE 层包含 2 个共享专家与 64 个路由专家，每个专家的中间隐藏维度为 1408。在路由过程中，每个 token 从 64 个路由专家中激活 6 个。为确保高效且稳定的训练，我们沿用了 Ling-Lite [[43](#bib.bib43)] 中引入的细粒度专家与 NormHead 策略。

### 3.2 训练细节

![Refer to caption](2503.17793v1/figures/training-pipeline.png)

图 5：Ling-Coder-Lite 的训练流水线。

图 5 展示了 Ling-Coder-Lite 的总体训练流水线。值得注意的是，我们从 Ling-Lite 的 7T token 中间检查点（记为 Ling-Lite-Base∗）开始持续预训练，而 Ling-Lite 最终以 9T token 结束初始预训练阶段 [[43](#bib.bib43)]。
我们从 Ling-Lite-Base∗ 开展持续预训练，目标包括下一 token 预测（Next-Token-Prediction）与中间填充（Fill-In-Middle，FIM）。在预训练的最后阶段，我们引入类似 [[44](#bib.bib44)] 的退火阶段，在该阶段我们提升训练数据质量并采用学习率退火策略以捕捉更精细的特征。随后，我们应用监督微调（SFT）与直接偏好优化（DPO），显著提升代码相关任务的实用性与可靠性。

表 1：各阶段预训练设置。

| 阶段 | 学习率 | 调度器 | 批量大小 | Tokens | 数据占比 (%)：Code/NLP/Math | 代码数据内占比 (%)：Raw Code/Code-Related/Synthetic |
| --- | --- | --- | --- | --- | --- | --- |
| 阶段 1 | 3e-4 ~ 1.5e-4 | multi-step | 16M | 870B | 70/20/10 | 94/5/1 |
| 阶段 2 | 1.4e-4 ~ 1.1e-4 | cosine | 16M | 1.7T | 65/20/15 | 75/20/5 |
| 退火 | 1.4e-4 ~ 1.4e-6 | inverse square root | 16M | 630B | 60/20/20 | 40/10/50 |

#### 3.2.1 持续预训练

由于计算资源与数据生产迭代速度的限制，我们在退火之前开展两阶段持续预训练。表 1 给出了预训练各阶段的训练参数与数据分布设置。总体上，我们逐步降低代码（尤其是原始代码）的比例，因为我们观察到该成分占比过高往往会损害自然语言理解能力。

阶段 1。该阶段在 870B token 上训练，批量大小为 16M token。最大与最小学习率分别设为 3e-4 与 1.5e-4。我们实施多步恒定学习率调度策略。具体而言，学习率在每一步内保持恒定、无衰减。当训练损失达到平台期或验证损失连续若干次迭代不再下降时，进一步降低学习率以促进持续收敛。

阶段 2。该阶段我们在 1.7T token 上训练模型，批量大小为 16M token。学习率配置为最大 1.4e-4、最小 1.1e-4，采用余弦衰减调度以促进训练损失的持续收敛。我们策略性地调整数据构成，降低 Raw Code 的比例，同时提高 Code-Related 与 Synthetic 数据的占比。这一策略性调整旨在增强模型对更复杂编码任务的理解，进一步提升其性能。

#### 3.2.2 退火

预训练的最后阶段涉及 630B token，保持 16M token 的一致批量大小。我们采用平方根倒数衰减调度器进行学习率退火，将学习率从 1.4e-4 快速降至 1.4e-6。与此同时，我们进一步调整数据构成：降低 Raw Code 的比例，同时大幅提高 Synthetic 数据（经过精心构建、质量最高）的占比。我们的策略利用退火阶段更精细、更稳定地吸收高质量知识，显著提升了性能。

#### 3.2.3 监督微调

数据准备。
在 SFT 阶段，我们收集了 1,880 万条指令数据，其中包括 1,170 万条代码相关指令。该数据集不仅包括代码与数学指令，还包含一部分来自 Ling-Lite [[43](#bib.bib43)] 的纯自然语言指令数据，代码、通用自然语言与数学指令的分布约为 3:1:1。这一纳入旨在保持模型在通用任务上的表现，同时增强其遵循指令解决复杂代码相关问题的能力。

此外，我们针对特定代码相关问题领域合成了大量指令数据。我们首先确定若干关键领域，如文本到代码、推理、SQL 与编程竞赛。然后，我们请最先进（SOTA）模型采用 2.4 节所述的自上而下与自下而上相结合的方法生成问题种子。借助 Evol-Instruct [[46](#bib.bib46)] 与 Oss-Instruct [[45](#bib.bib45)]，我们基于这些种子进一步扩展，创建更多问题。随后我们利用 SOTA 代码 LLM 为这些问题生成答案。最终，所得数据经过严格的去重、去污染与质量评估流程（如第 2 节所述）。

训练。Ling-Coder-Lite 在 1,880 万样本的数据集上微调 5 个 epoch。我们实施带 100 步预热的余弦调度。初始学习率设为 4e-5，总批量大小配置为 384。为优化训练效率，我们采用数据打包（data packing）技术 [[27](#bib.bib27)]。

#### 3.2.4 直接偏好优化

数据准备。我们首先汇集一套全面的开源 DPO 数据集。
为补充这些既有数据集，我们遵循 OSS-Instruct 方法论生成额外的 DPO 数据集。该过程分两步：首先，我们使用教师 LLM 基于从 the Stack [[20](#bib.bib20)] 随机采样的代码片段生成代码相关问题。然后，我们使用多种语言模型（包括 Ling-Coder-Lite-SFT 与其他 SOTA LLM）为每个问题生成多个答案。

为保障质量，我们使用 Llama-3.1-Nemotron-70B-Reward-HF [[8](#bib.bib8)] 奖励模型处理开源与合成数据集。该模型对每个问题的所有答案排序，我们过滤掉最高奖励分数低于预定阈值的数据点。通过消融研究，我们证明该过滤过程对提升 DPO 数据的整体质量至关重要。

训练。在完成 SFT 模型的开发后，我们实施离线直接偏好优化（DPO），使 Ling-Coder-Lite 进一步与人类偏好对齐。DPO 过程在 140 万条选定-拒绝配对样本上训练 2 个 epoch。我们将学习率设为 3e-7，总批量大小为 192 个样本，并使用带 150 步预热的余弦调度。我们的经验观察表明，DPO 显著增强了模型在开放式生成任务上的能力，且在标准基准上的性能没有实质性变化。

## 4 评测

为严格评估 Ling-Coder-Lite 模型的表现，我们在标准化的 CodeFuseEval 框架（注 12：<https://github.com/codefuse-ai/codefuse-evaluation>）内开展全面的多维度评测，确保结果的的可复现性与可比性（注 13：我们没有直接采用各对比模型论文中的结果数字，因为在部分基准上不同模型的基准配置略有差异，使得其结果数字无法直接比较。例如，对 MBPP 基准，一些模型报告 3-shot 结果，另一些报告 0-shot 结果；一些报告 500 个样本上的结果，另一些报告 1000 个样本上的结果。）。
评测分为基座模型与指令模型两部分。

### 4.1 评测配置

对于代码生成任务，我们采用 pass@k 指标；Text-to-SQL 任务采用执行准确率（EX）评估；所有任务统一采用贪心解码策略，并施加 4,096 token 的最大输出长度约束。提示词配置优先遵循被评测开源模型的原始设置，在无模型专属配置时默认采用各自的基准设置。该方式在确保技术精确性的同时，与既有的学术与操作惯例保持一致。

### 4.2 基准

为全面评估 Ling-Coder-Lite 与 Ling-Coder-Lite-Base 的能力，我们收集并在 12 个代表性代码相关基准上评测其表现，归为 6 类任务，详述如下：

- HumanEval [[4](#bib.bib4)] 是公认的 Python 代码补全评测数据集，由 OpenAI 研究者精心构建的 164 个问题组成。它强调 LLM 的基础 Python 编程能力，属于代码生成任务类别。
- MBPP [[2](#bib.bib2)] 包含 1,000 个 Python 编程问题，通过众包构建，主要考察模型的基础 Python 熟练度。在我们的评测中，我们从 MBPP 中选取 ID 为 11-510 的 500 个问题（即 MBPP-500）来评测文本到代码生成能力，具体为基于问题描述生成代码。它属于代码生成任务类别。
- EvalPlus [[28](#bib.bib28)] 是 HumanEval 与 MBPP 的增强版本，分别称为 HumanEval+ 与 MBPP+。
  HumanEval+ 将 HumanEval 基准的测试用例扩充 80 倍，而 MBPP+ 从 MBPP-500 中选取 378 个问题并将测试用例扩充 35 倍。
  EvalPlus 对模型编码能力提供更准确的评估，同样属于代码生成任务类别。
- LiveCodeBench（LCB）[[17](#bib.bib17)] 收集 LeetCode、AtCoder 与 Codeforces 平台定期竞赛的问题，用于构建一个随时间持续评测代码 LLM 在多样代码相关场景下表现的综合性基准。
  它包含四个子集：自我修复、代码执行、测试输出预测与代码生成。本研究仅关注其高级代码生成子集，使用 2024 年 8 月至 2024 年 11 月的评测数据，包含 22 道简单、34 道中等与 45 道困难问题。
  它属于高级代码生成任务类别。
- BigCodeBench（BCB）[[52](#bib.bib52)] 旨在在更真实的设置中评测 LLM 的真实编程能力。它面向 HumanEval 式的函数级代码生成任务，但指令更复杂、函数调用更多样。
  它包含 Complete 与 Instruct 两个拆分，各含 1,140 个问题。我们用 Complete 拆分测试基座模型，用 Instruct 拆分测试对话模型。
  它属于高级代码生成任务类别。
- MultiPL-E 将 HumanEval 与 MBPP 基准扩展到 18 种语言，以评测代码 LLM 的多语言表现。在我们的评测中，遵循 Qwen2.5-Coder 模型的语言选择，我们选取 10 种最广泛使用的编程语言：Python、Java、JavaScript、TypeScript、C++、C#、PHP、Rust、Go 与 Bash。为与 Qwen2.5-Coder 模型的评测对齐，我们将该数据集分为两个版本：MultiPL-E HumanEval（简称 MultiPLE-H）与 MultiPL-E MBPP（简称 MultiPLE-M）。它属于多语言代码生成任务类别。
- MBXP-PLUS 双语评测基准是开源 MBXP [[1](#bib.bib1)] 的优化版本，由两部分组成：MBXP-EN（英文版）与 MBXP-CN（中文版）。它聚焦自然语言到代码生成任务。该基准覆盖六种编程语言：Java、C++、JavaScript、TypeScript、Go 与 PHP，共提供 1,200 个任务实例，每种语言 100 个。每个任务实例都包含一个标准解答，确保 100% 的自验证通过率（pass@1）。此外，该数据集系统性地评估提示词与测试用例的有效性，以 pass@k 作为主要指标。
  它属于多语言代码生成任务类别。
- HumanEvalFix [[32](#bib.bib32)] 是基于 HumanEval 及其另外五种语言译本构建的基准套件，用于评估大模型的代码修复能力。它分为两部分：本文主要关注第一部分，其中仅提供测试用例而不提供 docstring；第二部分以 docstring 作为事实来源代替测试用例。它属于代码修复任务类别。
- CRUXEval [[9](#bib.bib9)]（Code Reasoning, Understanding, and eXecution Evaluation）是包含 800 个 Python 函数与输入输出对的基准。该基准包含两个任务：CRUXEval-I 涉及从输出预测输入，CRUXEval-O 涉及从输入预测输出。它属于代码理解与推理任务类别。
- DS-1000 [[22](#bib.bib22)] 聚焦评估模型使用 Python 代码执行数据科学分析的能力，覆盖 Numpy、Pandas、TensorFlow、Pytorch、Scipy、Sklearn 与 Matplotlib 等核心库。它属于数据分析应用任务类别。
- Spider 是一个大型人工标注数据集，面向复杂跨领域语义解析与 Text-to-SQL 基准，包含 2,147 个评测样本。它同样属于数据分析应用任务类别。

### 4.3 基座模型评测

表 2：各模型在 HumanEval、MBPP 与 BigCodeBench 上的表现（贪心模式，Pass@1）。

| 模型 | 总参数 | 激活参数 | HumanEval HE | HumanEval+ | MBPP 3-shot | MBPP+ | BigCodeBench Full | BigCodeBench Hard | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DS-Coder-V2-Lite-Base | 16B | 2.4B | 40.9 | 34.1 | 62.6 | 59.4 | 30.6 | 8.1 | 39.3 |
| Qwen2.5-Coder-7B-Base | 7B | – | 61.6 | 53.0 | 68.8 | 62.9 | 45.8 | 16.2 | 51.4 |
| OpenCoder-8B-Base | 8B | – | 66.5 | 63.4 | 60.6 | 70.4 | 40.5 | 9.5 | 51.8 |
| Ling-Coder-Lite-Base | 16.8B | 2.75B | 65.9 | 62.2 | 65.8 | 69.3 | 35.2 | 17.6 | 52.7 |

表 3：各模型在 CRUXEval 上的表现（贪心模式）。

| 模型 | 总参数 | 激活参数 | CruxEval-I-CoT | CruxEval-O-CoT | 平均 |
| --- | --- | --- | --- | --- | --- |
| DS-Coder-V2-Lite-Base | 16B | 2.4B | 53.4 | 46.1 | 49.6 |
| Qwen2.5-Coder-7B-Base | 7B | – | 56.5 | 56.0 | 56.3 |
| Ling-Coder-Lite-Base | 16.8B | 2.75B | 62.9 | 61.3 | 62.1 |

表 4：各模型在通用与数学基准上的表现（贪心模式）。我们对所有指标重新进行了对齐测试。

| 模型 | 总参数 | 激活参数 | C-Eval (5-shot) | CMMLU (5-shot) | MMLU (5-shot) | BBH (3-shot) | GSM8K (4-shot) | MATH (4-shot) | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ling-Lite-Base∗ (7T) | 16.8B | 2.75B | 62.2 | 62.5 | 60.0 | 51.5 | 49.1 | 18.1 | 50.6 |
| DS-Coder-V2-Lite-Base | 16B | 2.4B | 62.3 | 63.1 | 60.0 | 67.1 | 66.8 | 32.3 | 58.6 |
| Qwen2.5-Coder-7B-Base | 7B | – | 69.1 | 72.7 | 70.5 | 67.3 | 83.4 | 42.2 | 67.5 |
| Ling-Coder-Lite-Base | 16.8B | 2.75B | 74.8 | 75.5 | 67.6 | 69.3 | 78.8 | 40.5 | 67.7 |

对于基座模型，我们在三个关键方面开展全面比较：代码生成、代码理解与推理、通用与数学。我们的对比分析聚焦于最流行且最强大的开源代码模型，包括 DeepSeek-Coder-V2-Lite-Base、Qwen2.5-Coder-7B-Base 与 OpenCoder-8B-Base。这些模型的性能指标直接引自其各自的发表论文，我们计划在不久的将来补充我们自己对这些基座模型的测试结果。

#### 4.3.1 基础与高级代码生成

如表 2 所示，Ling-Coder-Lite-Base 在所有代码生成任务上取得最高平均分 52.7。该表现超过第二名 OpenCoder-8B-Base 0.9 分，领先 DeepSeek-Coder-V2-Lite-Base 13.4 分。这些结果表明 Ling-Coder-Lite-Base 在各项代码生成指标上展现出稳定实力，无明显短板。

HumanEval。为评估基座模型的基础代码片段补全能力，我们同时使用 HumanEval 及其扩展版 HumanEval-Plus。如表 2 所示，HumanEval 两项的平均分至少高于 DS-Coder-V2-Lite-Base 与 Qwen2.5-Coder-7B-Base 7 分，仅小幅落后 OpenCoder-8B-Base。该表现展示了 Ling-Coder-Lite-Base 在基础代码补全任务上的熟练度。

MBPP。为评估基础文本到代码生成能力，我们采用 MBPP 基准及其增强版 MBPP-Plus。注意，3-shot 版本使用 MBPP-500 作为测试集。Ling-Coder-Lite-Base 在两项 MBPP 指标上取得 67.6 的平均分，大幅领先第二名的 Qwen2.5-Coder-7B-Base（65.9）。这一同等规模开源代码模型中的 SOTA 表现证明了 Ling-Coder-Lite-Base 理解并解决基础编程问题的强大能力。

BigCodeBench。为进一步评估基座模型在实际编程场景中对复杂指令的理解与多样函数调用的熟练度，我们引入 BigCodeBench 指标。如表 2 所示，Ling-Coder-Lite-Base 的 BigCodeBench 总体平均分仅次于 Qwen2.5-Coder-7B-Base，同时在 Hard 子类上优于所有模型。

#### 4.3.2 代码理解与推理

为考察基座模型是否真正理解代码背后的逻辑推理与执行流程，我们引入 CRUXEval 指标。应当说明的是，OpenCoder-8B-Base 的论文未报告该指标，我们计划在本报告的后续版本中用自己的评测补充这些结果。

如表 3 所示，Ling-Coder-Lite-Base 在 CRUXEval-I 与 CRUXEval-O 上均展现出出色表现，分别取得 62.9 与 61.3 的分数。CRUXEval 平均分至少领先其他所有模型 6 分，在同等规模开源模型中创造了新的 SOTA。这一卓越表现可归功于我们在构建训练用合成数据时对代码执行预测场景的有意侧重。

#### 4.3.3 通用 NLP 与数学能力

我们在大幅提升 Ling-Coder-Lite-Base 编码性能的同时，仍保持了自然语言处理能力。为验证这一点，我们使用热门基准评估基座模型在通用自然语言处理与数学推理方面的能力，包括 C-Eval [[15](#bib.bib15)]、CMMLU [[24](#bib.bib24)]、MMLU [[11](#bib.bib11)]、BigBench Hard（BBH）[[42](#bib.bib42)]、GSM8K [[5](#bib.bib5)] 与 MATH [[12](#bib.bib12)]。如表 4 所示，我们对所有指标重新进行了对齐测试。
Ling-Coder-Lite-Base 在这六项指标上取得 67.7 的平均分，优于 DS-Coder-V2-Lite-Base，并与 Qwen2.5-Coder-7B-Base 表现相当。尽管在数学相关指标上略逊于 Qwen2.5-Coder-7B-Base，Ling-Coder-Lite-Base 在 C-Eval、CMMLU 与 BBH 等其他基准上表现出边际优势。值得注意的是，在经过大量代码数据的持续预训练后，Ling-Coder-Lite-Base 不仅保持而且提升了通用自然语言能力。与 Ling-Lite-Base∗ 相比，该模型在 C-Eval、CMMLU、MMLU 与 BBH 指标上平均提升 12 分。这一提升归功于预训练期间保持至少 20% 的自然语言文本数据。此外，通过纳入 10% 至 20% 的数学数据，Ling-Coder-Lite-Base 的整体数学推理能力相对 Ling-Lite-Base∗ 提升 25 分，进一步增强了模型的数学推理熟练度。

### 4.4 指令模型评测

对于指令模型，我们全面评测 Ling-Coder-Lite 在五类任务上的代码能力——代码生成、代码推理、代码修复、数据分析应用与 SQL 生成——共使用 12 项基准。
我们将其表现与先前同等参数规模的最先进代码 LLM 进行比较，包括 DeepSeek-Coder-V2-Lite-Instruct [[51](#bib.bib51)]、Qwen2.5-Coder-7B-Instruct [[16](#bib.bib16)] 与 OpenCoder-8B-Instruct [[13](#bib.bib13)]。
值得注意的是，为确保公平，我们使用完全相同的脚本与环境重新评测了所有这些模型。

#### 4.4.1 基础与高级代码生成

HumanEval 与 MBPP 基准。
我们按照大多数 LLM 的惯常做法，在 HumanEval [[4](#bib.bib4)]、MBPP [[2](#bib.bib2)] 及其增强版 EvalPlus [[28](#bib.bib28)] 上评估模型的基础 Python 编程技能。
对于 MBPP，我们评测其包含 500 个任务的原始版本，以及包含 378 个任务的增强版 MBPP+。两项评测均采用 zero-shot 方式。
如表 5 所示，Ling-Coder-Lite 在 HumanEval 与 HumanEval+ 上优于所有其他模型，分别领先第二名 Qwen2.5-Coder-7B-Instruct 1.21 与 3.22。
在 MBPP 与 MBPP+ 上，Ling-Coder-Lite 位列第二，落后表现最佳的 Qwen2.5-Coder-7B-Instruct 3.4 与 3.16。
此外，遵循 EvalPlus 官方排行榜的做法，我们计算 HumanEval+ 与 MBPP+ 的平均分。
从数值上看，Ling-Coder-Lite 成为表现最佳的模型，超过第二名 Qwen2.5-Coder-7B-Instruct 0.25。
鉴于 EvalPlus 中的评测样本具备更全面的测试用例、更能反映模型能力，有理由认为 Ling-Coder-Lite 的表现略优于先前同等参数规模的最先进代码 LLM。

表 5：Ling-Coder-Lite 与同等参数规模的热门开源代码 LLM 在 HumanEval 与 MBPP 基准上的表现（贪心模式，Pass@1）

| 模型 | 总参数 | 激活参数 | HumanEval | HumanEval+ | MBPP(500) | MBPP+ | EvalPlus 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CodeQwen1.5 | 7B | – | 82.93 | 69.60 | 75.00 | 67.19 | 71.10 |
| DeepSeek-Coder-V2 | 16B | 2.4B | 78.66 | 75.00 | 71.00 | 69.84 | 72.42 |
| Qwen2.5-Coder | 7B | – | 87.20 | 82.32 | 75.80 | 75.12 | 78.72 |
| OpenCoder | 8B | – | 82.32 | 77.44 | 64.80 | 69.84 | 73.64 |
| Ling-Coder-Lite | 16.8B | 2.75B | 88.41 | 85.98 | 72.40 | 71.96 | 78.97 |

高级编程。
除基础 Python 编程技能外，我们还使用复杂度更高的基准评估模型解决更具挑战性的竞赛级 Python 问题的能力，具体为 LiveCodeBench [[17](#bib.bib17)] 与 BigCodeBench [[52](#bib.bib52)]。
对于 LiveCodeBench，我们选取 2024 年 8 月至 2024 年 11 月期间的问题，共 101 道，包括 22 道简单、34 道中等与 45 道困难问题。
对于 BigCodeBench，我们使用适合 Instruct 模型的 Instruct 拆分，包含 1,140 个问题。
如表 6 所示，在完整 LiveCodeBench 集上，Ling-Coder-Lite 位列第二，落后 DeepSeek-Coder-V2-lite-Instruct 2.96；在中等与困难子集上情况相同，且均优于 Qwen2.5-Coder-7B-Instruct 与 Opencoder-8B-Instruct 模型。
在 BigCodeBench 上，Ling-Coder-Lite 在完整集与高难度子集上均取得最佳表现，分别超过第二名的 Qwen2.5-Coder-7B-Instruct 2.01 与 2.0。
总体而言，在应对更复杂的竞赛级高阶 Python 编程挑战时，Ling-Coder-Lite 与当前同等参数规模的最佳模型不相上下。

表 6：Ling-Coder-Lite 与同等参数规模的强大开源代码 LLM 在 LiveCodeBench 与 BigCodeBench 上的表现（贪心模式，Pass@1）

| 模型 | 总参数 | 激活参数 | LCB Easy(22) | LCB Medium(34) | LCB Hard(45) | LCB Full(101) | BCB-Instruct Hard | BCB-Instruct Full |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CodeQwen1.5 | 7B | – | 31.80 | 3.00 | 0.00 | 7.94 | 10.80 | 30.2 |
| DeepSeek-Coder-V2 | 16B | 2.4B | 59.09 | 29.41 | 13.33 | 28.70 | 12.16 | 37.11 |
| Qwen2.5-Coder | 7B | – | 63.60 | 14.71 | 8.89 | 22.77 | 20.30 | 40.80 |
| OpenCoder | 8B | – | 45.45 | 2.94 | 4.44 | 12.87 | 12.16 | 32.72 |
| Ling-Coder-Lite | 16.8B | 2.75B | 54.55 | 26.47 | 11.11 | 25.74 | 22.3 | 42.81 |

多语言编程。
除 Python 外，我们还在两个多语言基准上测试模型表现：用于代码补全的 MultiPL-E 与用于自然语言到代码的 MBXP_PLUS。对于 MultiPL-E，我们将其分为 HumanEval 与 MBPP 两个拆分，并选取 10 种主流编程语言：Python、C++、Java、PHP、TypeScript、C#、Bash、Go、Rust、JavaScript。对于 MBXP_PLUS，我们创建英文与中文两个拆分，每个拆分包含 6 种编程语言各 100 个问题：C++、Java、PHP、TypeScript、Go、Rust。

如表 7 所示，在 MultiPL-E 的 HumanEval 部分，Ling-Coder-Lite 总体落后表现最佳的 Qwen2.5-Coder-7B-Instruct 模型 0.58。
具体而言，Ling-Coder-Lite 在 Java 与 PHP 上优于其他模型，而在其他语言上与 Qwen2.5-Coder-7B-Instruct 持平或稍逊。
在 MultiPL-E 的 MBPP 部分，Ling-Coder-Lite 取得最佳总体表现，平均高于第二名的 Qwen2.5-Coder-7B-Instruct 模型 0.68。
就具体语言而言，Ling-Coder-Lite 在 C++、Java、PHP、C#、Rust 与 Bash 上表现出色，但在其余四种语言上不及 Qwen2.5-Coder-7B-Instruct。
在 MBXP_EN 拆分上，Ling-Coder-Lite 交出最佳总体表现，大幅领先第二名模型，仅在 PHP 上落后 Qwen2.5-Coder-7B-Instruct。
在对应的中文拆分 MBXP_CN 上，Ling-Coder-Lite 展现出同样的领先优势。
进一步观察发现，所有模型在中文上的表现都显著逊于对应英文版本，提示需要增强中文训练数据。
值得注意的是，在评测过程中我们发现 Ling-Coder-Lite 偶尔会错误地用 Python 回答一定比例的 TypeScript 问题。我们计划在未来的研究中更深入地调查并解决该问题。
总体而言，Ling-Coder-Lite 优于表 7 中的其他模型，展现了强大的多语言编程能力。

表 7：Ling-Coder-Lite 与同等参数规模代码 LLM 在多语言编程任务上的表现（贪心模式，Pass@1）。TS=TypeScript；JS=JavaScript。

| 模型 | 总参数 | 激活参数 | Python | C++ | Java | PHP | TS | C# | Bash | Go | Rust | JS | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **MultiPL-E HumanEval** | | | | | | | | | | | | | |
| CodeQwen1.5 | 7B | – | 83.54 | 70.19 | 74.68 | 75.15 | 76.10 | 57.59 | 44.94 | 49.35 | 72.43 | 77.02 | 66.28 |
| DeepSeek-Coder-V2 | 16B | 2.4B | 79.27 | 70.19 | 71.52 | 72.05 | 80.50 | 69.62 | 41.77 | 58.44 | 70.51 | 81.37 | 69.54 |
| Qwen2.5-Coder | 7B | – | 85.98 | 75.78 | 77.22 | 75.16 | 81.13 | 78.48 | 51.90 | 76.62 | 75.64 | 82.61 | 76.05 |
| OpenCoder | 8B | – | 82.32 | 67.70 | 70.89 | 63.98 | 65.41 | 70.89 | 44.30 | 68.18 | 63.46 | 52.17 | 64.93 |
| Ling-Coder-Lite | 16.8B | 2.75B | 85.98 | 75.78 | 82.28 | 78.88 | 80.50 | 77.22 | 49.37 | 72.08 | 73.72 | 78.88 | 75.47 |
| **MultiPL-E MBPP** | | | | | | | | | | | | | |
| CodeQwen1.5 | 7B | – | 74.25 | 61.71 | 58.28 | 61.46 | 72.31 | 51.81 | 41.36 | 54.01 | 63.28 | 67.51 | 60.6 |
| DeepSeek-Coder-V2 | 16B | 2.4B | 75.00 | 62.40 | 63.21 | 59.95 | 43.59 | 46.11 | 28.27 | 62.57 | 59.60 | 60.96 | 56.17 |
| Qwen2.5-Coder | 7B | – | 78.00 | 63.73 | 54.15 | 62.72 | 74.62 | 51.04 | 33.25 | 63.37 | 62.43 | 70.78 | 61.41 |
| OpenCoder | 8B | – | 70.25 | 58.69 | 62.44 | 60.96 | 47.95 | 46.89 | 40.05 | 57.49 | 49.15 | 58.19 | 55.21 |
| Ling-Coder-Lite | 16.8B | 2.75B | 76.25 | 68.26 | 67.88 | 65.99 | 56.15 | 53.37 | 39.79 | 66.31 | 57.63 | 69.27 | 62.09 |
| **MBXP EN** | | | | | | | | | | | | | |
| CodeQwen1.5 | 7B | – | – | 77.00 | 71.00 | 76.00 | 58.00 | – | – | 72.00 | – | 90.00 | 73.80 |
| DeepSeek-Coder-V2 | 16B | 2.4B | – | 69.00 | 56.00 | 91.00 | 83.00 | – | – | 73.00 | – | 91.00 | 77.20 |
| Qwen2.5-Coder | 7B | – | – | 87.00 | 90.00 | 95.00 | 78.00 | – | – | 85.00 | – | 91.00 | 87.67 |
| OpenCoder | 8B | – | – | 78.00 | 75.00 | 86.00 | 81.00 | – | – | 68.00 | – | 76.00 | 77.33 |
| Ling-Coder-Lite | 16.8B | 2.75B | – | 92.00 | 92.00 | 92.00 | 91.00 | – | – | 89.00 | – | 97.00 | 92.17 |
| **MBXP CN** | | | | | | | | | | | | | |
| CodeQwen1.5 | 7B | – | – | 60.00 | 67.00 | 70.00 | 80.00 | – | – | 66.00 | – | 81.00 | 70.70 |
| DeepSeek-Coder-V2 | 16B | 2.4B | – | 64.00 | 82.00 | 86.00 | 81.00 | – | – | 73.00 | – | 87.00 | 78.80 |
| Qwen2.5-Coder | 7B | – | – | 80.00 | 82.00 | 89.00 | 85.00 | – | – | 81.00 | – | 84.00 | 83.50 |
| OpenCoder | 8B | – | – | 71.00 | 73.00 | 78.00 | 79.00 | – | – | 74.00 | – | 73.00 | 74.67 |
| Ling-Coder-Lite | 16.8B | 2.75B | – | 86.00 | 90.00 | 88.00 | 87.00 | – | – | 82.00 | – | 93.00 | 87.67 |

#### 4.4.2 代码理解与推理

CRUXEval。
为评估模型的代码理解与推理能力，我们使用 CRUXEval [[9](#bib.bib9)] 基准，它分为 CRUXEval-I 与 CRUXEval-O 两个拆分，各包含 800 道 Python 题。在 CRUXEval-I 中，任务是给定一段 Python 代码及其某一执行输出结果，让模型推导并推断出能产生该输出的合适程序输入（即参数）。CRUXEval-O 则给出代码及其输入参数，要求模型推理并预测正确输出。这种评测方式可以更深入地检验模型对 Python 代码的理解，包括正向与反向执行逻辑。
评测期间，我们采用 CoT（思维链）提示方法，引导模型先给出逐步的思考过程再得出最终结果。

如表 8 所示，Ling-Coder-Lite 在输出预测任务 CRUXEval-O 上表现最佳，以 0.42 的微弱优势领先第二名的 Qwen2.5-Coder-7B-Instruct。在 CRUXEval-I 上排名反转，Ling-Coder-Lite 落后 2.1，但仍显著领先其他模型。总体上，Ling-Coder-Lite 落后 Qwen2.5-Coder-7B-Instruct 模型 0.84，却大幅领先 DeepSeek-Coder-V2-Instruct 与 OpenCoder-8B-Instruct，展现出强大的 Python 代码理解与推理能力。此外，我们发现该评测指标的改进也有助于提升模型的代码生成性能。

表 8：Ling-Coder-Lite 与同等参数规模代码 LLM 在 CRUXEval 上的表现

| 模型 | 总参数 | 激活参数 | Crux-I-CoT | Crux-O-CoT | Full |
| --- | --- | --- | --- | --- | --- |
| CodeQwen1.5 | 7B | – | 41.21 | 40.00 | 40.61 |
| DeepSeek-Coder-V2 | 16B | 2.4B | 51.71 | 52.72 | 52.22 |
| Qwen2.5-Coder | 7B | – | 68.22 | 70.38 | 69.30 |
| OpenCoder | 8B | – | 39.32 | 43.74 | 41.53 |
| Ling-Coder-Lite | 16.8B | 2.75B | 66.12 | 70.80 | 68.46 |

#### 4.4.3 代码修复

表 9：Ling-Coder-Lite 与同等参数规模代码 LLM 在 HumanEvalFix 上的表现。

| 模型 | 总参数 | 激活参数 | Python | Java | C++ | Go | Rust | JavaScript | 总体 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CodeQwen1.5 | 7B | – | 48.78 | 56.10 | 45.73 | 48.17 | 43.90 | 50.00 | 48.78 |
| DeepSeek-Coder-V2 | 16B | 2.4B | 71.95 | 60.37 | 63.41 | 71.95 | 67.07 | 76.83 | 68.60 |
| Qwen2.5-Coder | 7B | – | 78.65 | 79.26 | 49.39 | 76.22 | 54.87 | 77.44 | 69.31 |
| OpenCoder | 8B | – | 39.63 | 46.34 | 34.76 | 41.46 | 28.66 | 39.02 | 38.32 |
| Ling-Coder-Lite | 16.8B | 2.75B | 83.54 | 76.83 | 66.46 | 77.44 | 62.80 | 74.39 | 73.58 |

HumanEvalFix。我们进一步使用 HumanEvalFix [[32](#bib.bib32)] 基准评估模型的代码修复能力。HumanEvalFix 基于原始 HumanEval 及另外五种语言的翻译版本构建：Java、C++、JavaScript、Go 与 Rust。它由 test 与 docstring 两个拆分组成。在我们的评测中，我们选择 test 拆分，其中提供测试用例而不提供 docstring，要求模型基于测试用例描述的输入与期望输出，识别并纠正给定缺陷代码中的错误。该评测考察模型理解测试用例与代码内部逻辑的能力，部分反映其执行 TDD（测试驱动开发）任务的能力。
如表 9 所示，Ling-Coder-Lite 在 Python、C++ 与 Go 语言上表现最佳。在 Java 与 JavaScript 上，Qwen2.5-Coder-7B-Instruct 是最佳表现者，分别领先 Ling-Coder-Lite 2.43 与 3.05。在 Rust 上，最佳表现者是 DeepSeek-Coder-V2-Lite-Instruct 模型，Ling-Coder-Lite 次之。总体上，Ling-Coder-Lite 表现最佳，平均分高出第二名的 DeepSeek-Coder-V2-Lite-Instruct 模型 3.76。

#### 4.4.4 数据分析应用

我们进一步评估模型在数据分析应用上的表现，聚焦其使用主流 Python 数据科学分析库的能力，以及基于自然语言描述生成 SQL 语句的能力。

DS-1000。
我们使用 DS-1000 [[22](#bib.bib22)] 评估模型解决实际数据科学分析问题的能力。DS-1000 基准是为评估与检验模型在数据科学与分析任务上的能力而设计的综合数据集。它涵盖广泛的现实数据科学问题，聚焦使用 Python 进行数据分析、操作与解释的实际应用。
研究者从 StackOverflow 收集并整理了问题、参考答案与测试用例，涉及七个 Python 数据分析库的使用。这些原始问题构成基准的基础。为避免模型从训练数据中记忆这些问题与答案，研究者引入三类扰动——Surface（表层）、Semantic（语义）与 Difficult-Rewrite（困难改写）——对原始问题进行变换。该基准包含 1,000 个问题，分布如下：220 道 Numpy 题、291 道 Pandas 题、155 道 Matplotlib 题、68 道 Pytorch 题、106 道 Scipy 题、115 道 Sklearn 题、45 道 Tensorflow 题。值得一提的是，在两个候选系统提示词中我们选择了非默认版本："Only provide the code completion needed. Don't repeat the context code."。

表 10：Ling-Coder-Lite 与热门小型代码 LLM 在 DS-1000 基准上的表现。DR=Difficult-Rewrite，Mat=Matplotlib。

| 模型 | 总参数 | 激活参数 | Numpy | Pandas | Pytorch | Scipy | Sklearn | TF | Mat | 原始 | Surface | Semantic | DR | 总体 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Qwen2.5-Coder | 7B | – | 49.1 | 29.2 | 39.7 | 37.7 | 26.1 | 37.8 | 63.2 | 51.5 | 28.3 | 41.0 | 20.4 | 40.6 |
| OpenCoder | 8B | – | 51.8 | 33.3 | 35.3 | 36.8 | 41.7 | 35.6 | 51.6 | 50.9 | 29.6 | 41.5 | 28.4 | 41.8 |
| Ling-Coder-Lite | 16.8B | 2.75B | 56.4 | 36.1 | 44.1 | 36.8 | 47.8 | 40.0 | 58.1 | 55.3 | 40.8 | 43.6 | 29.0 | 46.1 |

如表 10 所示，总体上 Ling-Coder-Lite 展现出最佳表现，尤其在 Surface 扰动类型上表现卓越，显著优于其他模型。Surface 扰动涉及在保持参考答案不变的前提下变换原始问题描述，这凸显了 Ling-Coder-Lite 稳健的问题理解与泛化能力。Ling-Coder-Lite 在 Semantic 与 Difficult-Rewrite 扰动类型上也保持领先地位。

Spider。
数据库已深入日常生活的方方面面，使 SQL 成为一种不可或缺且广泛使用的工具。编写 SQL 查询颇具挑战性，这导致科技公司对从自然语言描述生成 SQL 语句（即 Text-to-SQL 任务）有强烈需求。
为测试模型的 Text-to-SQL 能力，我们选择 Spider [[49](#bib.bib49)] 基准。该数据集包含跨四个难度级别（简单、中等、困难、超难）的 2,147 个问题，可全面评估模型生成从简单到高度复杂 SQL 查询的能力。
如表 11 所示，Ling-Coder-Lite 位列第二，优于 DeepSeek-Coder-V2-Lite-Instruct 与 OpenCoder-8B-Instruct 模型，但仍落后于 Qwen2.5-Coder-7B-Instruct 模型。经过全面比较与分析，我们认为有必要在预训练阶段纳入 text-to-SQL 相关合成数据，并创建更高质量的 text-to-SQL 微调数据。这将是我们下一步工作之一。

表 11：Ling-Coder-Lite 与同等参数规模代码 LLM 在 Spider 上的 Text-to-SQL 表现

| 模型 | 总参数 | 激活参数 | Easy | Medium | Hard | Extra-Hard | Full |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CodeQwen1.5 | 7B | – | 88.5 | 76.3 | 68.6 | 55.90 | 72.9 |
| DeepSeek-Coder-V2 | 16B | 2.4B | 89.6 | 82.0 | 61.6 | 61.3 | 75.8 |
| Qwen2.5-Coder | 7B | – | 90.2 | 87.6 | 74.5 | 68.3 | 82.0 |
| OpenCoder | 8B | – | 83.4 | 78.9 | 51.8 | 46.2 | 68.1 |
| Ling-Coder-Lite | 16.8B | 2.75B | 87.7 | 81.2 | 67.6 | 68.1 | 77.5 |

## 5 效率分析

在本节中，我们分析 Ling-Coder-Lite 的效率，其中 5.1 节聚焦 FLOPs 与准确率的理论对比，5.2 节聚焦实际速度。

### 5.1 FLOPs 与准确率

我们首先研究若干对比模型在准确率与单次推理理论计算成本之间的权衡。具体而言，我们以 12 项基准上的平均分衡量各模型的表现（如图 1(b) 所示），并以上下文长度 4096 的单次推理的每秒万亿次浮点运算（TFLOPs）评估其理论计算需求（如图 1(c) 所示）。

结果表明，Ling-Coder-Lite 取得最佳平均分，优于 Qwen2.5-Coder-7B-Instruct 与 DeepSeek-Coder-V2-Lite-Instruct 两个模型。
此外，尽管 Ling-Coder-Lite 的单次推理理论计算成本略高于 DeepSeek-Coder-V2-Lite-Instruct，却远低于 Qwen2.5-Coder-7B-Instruct 与 OpenCoder-8B-Instruct。
这些发现表明，Ling-Coder-Lite 模型在性能与效率之间取得了更好的平衡。

### 5.2 实践中的效率

![Refer to caption](2503.17793v1/figures/inference_time.png)

图 6：Ling-Coder-Lite 与 Qwen2.5-Coder-7B-Instruct 的推理延迟对比。

我们进一步在各种输入输出长度下，对基于 MoE 的 Ling-Coder-Lite 与 SOTA 稠密模型 Qwen2.5-Coder-7B-Instruct 在实际设置中的推理效率进行对比分析。具体而言，我们使用 vLLM [[21](#bib.bib21)] 推理框架，模型在 L20 GPU 上以 FP16 精度运行。我们考察两种张量并行配置：tp=1（单张 L20 GPU）与 tp=2（两张 L20 GPU）。我们将批量大小设为 1，并系统性地从较短到较长序列改变输入-输出长度组合。推理延迟表现使用 vLLM 提供的 benchmark_latency（注 14：<https://github.com/vllm-project/vllm/blob/main/benchmarks/benchmark_latency.py>）脚本评估。

如图 6 所示，Ling-Coder-Lite 相比 Qwen2.5-Coder-7B-Instruct 展现出显著更优的推理效率。在 tp=1 配置下，Ling-Coder-Lite 比 Qwen2.5-Coder-7B-Instruct 快 1.5 至 2 倍，且随着长度增加优势更加明显。扩展到 tp=2 时，Ling-Coder-Lite 相对 tp=1 的对应情形取得约 1.2 倍加速，而 Qwen2.5-Coder-7B-Instruct 取得 1.6 倍的提升。我们推测 Ling-Coder-Lite 加速相对温和的原因，在于其 MoE 架构在张量并行下专家路由的跨机通信开销增加。尽管如此，在 tp=2 配置下，Ling-Coder-Lite 仍以 1.1 至 1.8 倍的优势胜过 Qwen2.5-Coder-7B-Instruct，且序列越长性能差距越大。

在实践中，我们内部有一款 AI-IDE 应用，
拥有超过 10,000 名用户，每天帮助用户生成数十万行代码。该服务此前由一个稠密 7B 代码 LLM 支撑。在为代码补全相关任务固定相同的延迟水平要求（≤500ms）后，
我们实现了 Ling-Coder-Lite 相比同等规模稠密模型（7B）约 50% 的部署资源降低，且在准确率与吞吐量上均无体验损失。

## 6 结论与未来工作

我们推出了 Ling-Coder-Lite，一个基于 MoE 的代码 LLM，在 12 项编码基准上媲美最先进表现，同时相比同等规模的代码 LLM 提供有竞争力的延迟与吞吐量。
我们呈现了构建此类编码 LLM 的细节，包括持续预训练与后训练的训练配方/策略，以及产出高质量代码数据、代码相关数据与合成指令数据的数据构建方法。
为支持该领域的进一步研究与发展，我们开源了模型以及退火与后训练阶段的大量高质量数据。

未来工作将进一步推动强大且高效的代码 LLM 的终极帕累托前沿。我们计划借助思维链改进推理表现，并在 RLHF 中为在线迭代训练加入执行反馈，从而能够处理软件工程中更复杂的编码任务。
与此同时，我们将进一步提升超越语法错误层面的数据质量，例如在函数方法、文件乃至仓库层面进行执行正确性检查。

## 作者列表

注：作者按姓氏的字母顺序排列。

Wenting Cai,
Yuchen Cao,
Chaoyu Chen,
Chen Chen,
Siba Chen,
Qing Cui,
Peng Di,
Junpeng Fang,
Zi Gong,
Ting Guo,
Zhengyu He,
Yang Huang,
Cong Li,
Jianguo Li,
Zheng Li,
Shijie Lian,
BingChang Liu,
Songshan Luo,
Shuo Mao,
Min Shen,
Jian Wu,
Jiaolong Yang,
Wenjie Yang,
Tong Ye,
Hang Yu,
Wei Zhang,
Zhenduo Zhang,
Hailin Zhao,
Xunjin Zheng,
Jun Zhou

## 参考文献

- [1]

  Ben Athiwaratkun, Sanjay Krishna Gouda, Xiaopeng Wang, Zijian an Li, Yuchen Tian, Ming Tan, Wasi Uddin Ahmad, Shiqi Wang, et al.
  Multi-lingual evaluation of code generation models.
  *arXiv preprint arXiv:2210.14868*, 2022.
- [2]

  Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le, et al.
  Program synthesis with large language models.
  *arXiv preprint arXiv:2108.07732*, 2021.
- [3]

  Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, et al.
  Qwen technical report.
  *arXiv preprint arXiv:2309.16609*, 2023.
- [4]

  Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, et al.
  Evaluating large language models trained on code.
  2021.
- [5]

  Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, et al.
  Training verifiers to solve math word problems.
  *arXiv preprint arXiv:2110.14168*, 2021.
- [6]

  Peng Di, Jianguo Li, Hang Yu, Wei Jiang, Wenting Cai, Yang Cao, Chaoyu Chen, Dajun Chen, et al.
  Codefuse-13b: A pretrained multi-lingual code large language model, 2023.
- [7]

  Zi Gong, Hang Yu, Cong Liao, Bingchang Liu, Chaoyu Chen, and Jianguo Li.
  Coba: Convergence balancer for multitask finetuning of large language models.
  *arXiv preprint arXiv:2410.06741*, 2024.
- [8]

  Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, et al.
  The llama 3 herd of models.
  *arXiv preprint arXiv:2407.21783*, 2024.
- [9]

  Alex Gu, Baptiste Rozière, Hugh Leather, Armando Solar-Lezama, Gabriel Synnaeve, and Sida I. Wang.
  Cruxeval: A benchmark for code reasoning, understanding and execution.
  *arXiv preprint arXiv:2401.03065*, 2024.
- [10]

  Daya Guo, Qihao Zhu, Dejian Yang, Zhenda Xie, Kai Dong, et al.
  Deepseek-coder: When the large language model meets programming – the rise of code intelligence, 2024.
  URL <https://arxiv.org/abs/2401.14196>.
- [11]

  Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt.
  Measuring massive multitask language understanding.
  *arXiv preprint arXiv:2009.03300*, 2020.
- [12]

  Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt.
  Measuring mathematical problem solving with the math dataset.
  *arXiv preprint arXiv:2103.03874*, 2021.
- [13]

  Siming Huang, Tianhao Cheng, Jason Klein Liu, Jiaran Hao, Liuyihan Song, et al.
  Opencoder: The open cookbook for top-tier code large language models.
  *arXiv preprint arXiv:2411.04905*, 2024a.
- [14]

  Yiming Huang, Xiao Liu, Yeyun Gong, Zhibin Gou, Yelong Shen, Nan Duan, and Weizhu Chen.
  Key-point-driven data synthesis with its enhancement on mathematical reasoning.
  *arXiv preprint arXiv:2403.02333*, 2024b.
- [15]

  Yuzhen Huang, Yuzhuo Bai, Zhihao Zhu, Junlei Zhang, Jinghan Zhang, Tangjun Su, et al.
  C-eval: A multi-level multi-discipline chinese evaluation suite for foundation models.
  *Advances in Neural Information Processing Systems*, 36:62991–63010, 2023.
- [16]

  Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang, Bowen Yu, Keming Lu, et al.
  Qwen2. 5-coder technical report.
  *arXiv preprint arXiv:2409.12186*, 2024.
- [17]

  Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, et al.
  Livecodebench: Holistic and contamination free evaluation of large language models for code.
  *arXiv preprint arXiv:2403.07974*, 2024.
- [18]

  Armand Joulin, Edouard Grave, Piotr Bojanowski, Matthijs Douze, Hérve Jégou, and Tomas Mikolov.
  Fasttext.zip: Compressing text classification models.
  *arXiv preprint arXiv:1612.03651*, 2016a.
- [19]

  Armand Joulin, Edouard Grave, Piotr Bojanowski, and Tomas Mikolov.
  Bag of tricks for efficient text classification.
  *arXiv preprint arXiv:1607.01759*, 2016b.
- [20]

  Denis Kocetkov, Raymond Li, Loubna Ben Allal, Jia Li, Chenghao Mou, Carlos Muñoz Ferrandis, et al.
  The stack: 3 tb of permissively licensed source code.
  *Preprint*, 2022.
- [21]

  Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, et al.
  Efficient memory management for large language model serving with pagedattention.
  In *Proceedings of the 29th Symposium on Operating Systems Principles*, pages 611–626, 2023.
- [22]

  Yuhang Lai, Chengxi Li, Yiming Wang, Tianyi Zhang, Ruiqi Zhong, Luke Zettlemoyer, Scott Wen tau Yih, Daniel Fried, Sida Wang, and Tao Yu.
  Ds-1000: A natural and reliable benchmark for data science code generation.
  *ArXiv*, abs/2211.11501, 2022.
- [23]

  Cong Li, Zhaogui Xu, Peng Di, et al.
  Understanding code changes practically with small-scale language models.
  In *Proceedings of the 39th IEEE/ACM International Conference on Automated Software Engineering*, ASE ’24, page 216–228, 2024a.
  ISBN 9798400712487.
  doi:[10.1145/3691620.3694999](https://doi.org/10.1145/3691620.3694999).
  URL <https://doi.org/10.1145/3691620.3694999>.
- [24]

  Haonan Li, Yixuan Zhang, Fajri Koto, Yifei Yang, Hai Zhao, Yeyun Gong, Nan Duan, and Timothy Baldwin.
  Cmmlu: Measuring massive multitask language understanding in chinese, 2024a.
  *URL https://arxiv. org/abs/2306.09212*.
- [25]

  Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas Muennighoff, Denis Kocetkov, et al.
  Starcoder: may the source be with you!
  *arXiv preprint arXiv:2305.06161*, 2023.
- [26]

  Tianle Li, Wei-Lin Chiang, Evan Frick, Lisa Dunlap, Tianhao Wu, et al.
  From crowdsourced data to high-quality benchmarks: Arena-hard and benchbuilder pipeline.
  *arXiv preprint arXiv:2406.11939*, 2024b.
- [27]

  Bingchang Liu, Chaoyu Chen, Zi Gong, Cong Liao, Huan Wang, Zhichao Lei, Ming Liang, Dajun Chen, et al.
  MFTCoder: Boosting code llms with multitask fine-tuning.
  In *Proceedings of the 30th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*, pages 5430–5441, 2024.
- [28]

  Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang.
  Is your code generated by chatGPT really correct? rigorous evaluation of large language models for code generation.
  In *NeuIPS*, 2023.
  URL <https://openreview.net/forum?id=1qvx610Cu7>.
- [29]

  Anton Lozhkov, Raymond Li, Loubna Ben Allal, Federico Cassano, Joel Lamy-Poirier, et al.
  Starcoder 2 and the stack v2: The next generation.
  *arXiv preprint arXiv:2402.19173*, 2024.
- [30]

  Shuai Lu, Daya Guo, Shuo Ren, Junjie Huang, Alexey Svyatkovskiy, et al.
  Codexglue: A machine learning benchmark dataset for code understanding and generation.
  *CoRR*, abs/2102.04664, 2021.
- [31]

  MistralAI.
  Codestral.
  <https://mistral.ai/news/codestral/>, 2024.
  Accessed: 2025-03-10.
- [32]

  Niklas Muennighoff, Qian Liu, Armel Zebaze, Qinkai Zheng, Binyuan Hui, Terry Yue Zhuo, Swayam Singh, Xiangru Tang, Leandro von Werra, and Shayne Longpre.
  Octopack: Instruction tuning code large language models, 2023.
- [33]

  Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, and d others.
  Training language models to follow instructions with human feedback.
  In *NeurIPS*, 2022.
- [34]

  Sheena Panthaplackel, Junyi Jessy Li, Milos Gligoric, and Raymond J. Mooney.
  Deep just-in-time inconsistency detection between comments and source code.
  In *AAAI*, pages 427–435, 2021.
- [35]

  Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, and Chelsea Finn.
  Direct preference optimization: Your language model is secretly a reward model, 2024.
  URL <https://arxiv.org/abs/2305.18290>.
- [36]

  Guoping Rong, Yongda Yu, Song Liu, Xin Tan, et al.
  Code Comment Inconsistency Detection and Rectification Using a Large Language Model .
  In *IEEE/ACM 47th International Conference on Software Engineering (ICSE)*, 2025.
- [37]

  Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi, Jingyu Liu, Tal Remez, Jérémy Rapin, et al.
  Code llama: Open foundation models for code.
  *arXiv preprint arXiv:2308.12950*, 2023.
- [38]

  Noveen Sachdeva, Benjamin Coleman, Wang-Cheng Kang, Jianmo Ni, Lichan Hong, Ed H. Chi, James Caverlee, Julian McAuley, and Derek Zhiyuan Cheng.
  How to train data-efficient llms, 2024.
  URL <https://arxiv.org/abs/2402.09668>.
- [39]

  Victor Sanh, Lysandre Debut, Julien Chaumond, and Thomas Wolf.
  Distilbert, a distilled version of bert: smaller, faster, cheaper and lighter.
  *ArXiv*, abs/1910.01108, 2019.
- [40]

  Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, et al.
  Deepseekmath: Pushing the limits of mathematical reasoning in open language models.
  *arXiv preprint arXiv:2402.03300*, 2024.
- [41]

  Luca Soldaini, Rodney Kinney, Akshita Bhagia, Dustin Schwenk, David Atkinson, et al.
  Dolma: an Open Corpus of Three Trillion Tokens for Language Model Pretraining Research.
  *arXiv preprint*, 2024.
- [42]

  Mirac Suzgun, Nathan Scales, Nathanael Schärli, Sebastian Gehrmann, et al.
  Challenging big-bench tasks and whether chain-of-thought can solve them.
  *arXiv preprint arXiv:2210.09261*, 2022.
- [43]

  Ling Team.
  Every FLOP counts: Scaling a 300B mixture-of-experts LING LLM without premium GPUs, 2025.
  URL <https://arxiv.org/abs/2503.05139>.
- [44]

  Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, et al.
  Llama 2: Open foundation and fine-tuned chat models.
  *arXiv preprint arXiv:2307.09288*, 2023.
- [45]

  Yuxiang Wei, Zhe Wang, Jiawei Liu, et al.
  Magicoder: Empowering code generation with oss-instruct.
  *arXiv preprint arXiv:2312.02120*, 2023.
- [46]

  Can Xu, Qingfeng Sun, Kai Zheng, Xiubo Geng, Pu Zhao, Jiazhan Feng, Chongyang Tao, and Daxin Jiang.
  Wizardlm: Empowering large language models to follow complex instructions.
  *arXiv preprint arXiv:2304.12244*, 2023.
- [47]

  Xiaohan Xu, Ming Li, Chongyang Tao, Tao Shen, Reynold Cheng, Jinyang Li, Can Xu, Dacheng Tao, and Tianyi Zhou.
  A survey on knowledge distillation of large language models, 2024a.
- [48]

  Zhangchen Xu, Fengqing Jiang, Luyao Niu, Yuntian Deng, Radha Poovendran, Yejin Choi, and Bill Yuchen Lin.
  Magpie: Alignment data synthesis from scratch by prompting aligned llms with nothing.
  *ArXiv*, abs/2406.08464, 2024b.
- [49]

  Tao Yu, Rui Zhang, Kai Yang, Michihiro Yasunaga, et al.
  Spider: A large-scale human-labeled dataset for complex and cross-domain semantic parsing and text-to-sql task, 2019.
- [50]

  Ge Zhang, Scott Qu, Jiaheng Liu, Chenchen Zhang, Chenghua Lin, Chou Leuang Yu, Danny Pan, and Esther Cheng others.
  Map-neo: Highly capable and transparent bilingual large language model series.
  *arXiv preprint arXiv: 2405.19327*, 2024.
- [51]

  Qihao Zhu, Daya Guo, Zhihong Shao, Dejian Yang, et al.
  Deepseek-coder-v2: Breaking the barrier of closed-source models in code intelligence.
  *arXiv preprint arXiv:2406.11931*.
- [52]

  Terry Yue Zhuo, Minh Chien Vu, Jenny Chim, Han Hu, Wenhao Yu, Ratnadira Widyasari, et al.
  Bigcodebench: Benchmarking code generation with diverse function calls and complex instructions.
  *arXiv preprint arXiv:2406.15877*, 2024.
