---
title: "DeepScholar-Bench：生成式研究综合的实时基准与自动化评估"
title_en: "DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"
arxiv: 2508.20033
source: https://arxiv.org/abs/2508.20033
crawled: 2026-09-23
translated: 2026-09-23
---

# DeepScholar-Bench：生成式研究综合的实时基准与自动化评估

> 原文：[DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis](https://arxiv.org/abs/2508.20033) · Stanford CS329A 指定阅读

Liana Patel†（斯坦福大学，[lianapat@stanford.edu](mailto:lianapat@stanford.edu)）

Negar Arabzadeh‡（加州大学伯克利分校，[negara@berkeley.edu](mailto:negara@berkeley.edu)）

Harshit Gupta†（斯坦福大学，[gharshit@stanford.edu](mailto:gharshit@stanford.edu)）

Ankita Sundar‡（加州大学伯克利分校，[ankitasun@berkeley.edu](mailto:ankitasun@berkeley.edu)）

Ion Stoica‡（加州大学伯克利分校，[istoica@cs.berkeley.edu](mailto:istoica@cs.berkeley.edu)）

Matei Zaharia‡（加州大学伯克利分校，[matei@berkeley.edu](mailto:matei@berkeley.edu)）

Carlos Guestrin†（斯坦福大学，[guestrin@stanford.edu](mailto:guestrin@stanford.edu)）

† 斯坦福大学　‡ 加州大学伯克利分校。代码与数据：[DeepScholar-Bench Repository](https://github.com/guestrin-lab/deepscholar-bench)

###### 摘要

研究与综合知识的能力是人类专业素养与进步的核心。一类新的 AI 系统——为生成式研究综合（generative research synthesis）而生——旨在通过从实时网络检索信息并产出带引用的长篇报告来自动化这一过程。然而，评估此类系统仍是一个开放挑战：现有问答基准聚焦简短的事实性答案，而专家策划的数据集则面临过时与数据污染的风险，两者都无法刻画真实研究综合任务的复杂性与持续演化的本质。我们提出 DeepScholar-bench，一个面向生成式研究综合的实时（live）基准与自动化评估框架。DeepScholar-bench 从近期高质量的 ArXiv 论文中提取查询与人工撰写的范例，并评估一个真实综合任务：通过检索、综合并引用先前工作来生成相关工作（related work）章节。我们的自动化框架从三个关键维度整体度量性能——知识综合、检索质量与可验证性。为推动后续工作，我们还贡献了 DeepScholar-ref，一个简单、开源的参考流水线，它在 LOTUS 框架上实现并提供了强有力的基线。借助 DeepScholar-bench，我们系统评估了先前的开源系统、配备强大模型的搜索智能体、OpenAI 的 DeepResearch 以及 DeepScholar-ref。我们发现 DeepScholar-bench 远未饱和：没有任何系统在所有指标上的几何平均超过 31%。这些结果凸显了 DeepScholar-bench 的难度与重要性，它是推动具备生成式研究综合能力的 AI 系统进步的基础。我们的基准代码与数据开源于 <https://github.com/guestrin-lab/deepscholar-bench>。

## 1 引言

人类知识与创新的基石，是人类专家*研究并综合*已知事实与新发现的能力，它使其他人能够理解、验证并在先前工作之上继续构建。近来，面向*生成式研究综合*的系统开始涌现，有望自动化那些产出长篇成果（如多页报告）的任务——这类任务传统上需要人类专家数小时的文献检索、阅读与写作。这些产品既有商业化的——来自 OpenAI [33]、Gemini [13]、Anthropic [2]、Grok [59] 与 Perplexity [38]——也有开源方法，如 STORM [43]、DeepResearcher [65] 与 OpenScholar [6]。现有系统在事实性与问答基准上展现了可喜的性能 [55, 20, 31, 56]，不断推进 AI 能力的前沿。

![Refer to caption](2508.20033v2/figure1_whisker.png)

图 1：DeepScholarBench 概览。我们提出一个面向生成式研究综合的、持续更新的实时基准，并计划每月发布数据集与排行榜结果。我们用自动化数据管线（左上）从近期高质量的 ArXiv 论文中策划数据集。数据集任务是根据论文信息生成相关工作章节（上中）。DeepScholar-bench 评估框架（右上）用一整套自动化指标从三个关键维度评估系统报告的表现：知识综合、检索质量与可验证性。我们系统评估了 14 个现有基线（下），并展示它们在每个指标上的性能范围。粉色展示开源系统的性能范围，包括 DeepScholar、STORM、OpenScholar、搜索智能体（Search Agent）与我们的 DeepScholar-ref 流水线，均使用开源的 Llama-4-Scout-17B-16E-Instruct 模型。绿色展示专有系统以及使用闭源模型的开源系统的性能范围，包括 OpenAI 的 o3 DeepResearch，以及用 o3、Claude-opus-4、Gemini-2.5-pro 与 GPT4.1 运行的搜索智能体与 DeepScholar-ref。
总体而言，没有任何系统在所有指标上的几何平均超过 31%，反映了未来工作的巨大空间。完整评估结果见第 5 节。

然而，随着这一类新系统的出现，一个关键问题仍然悬而未决：*我们应当如何为生成式研究综合建立基准并加以评估？* 这些系统的进步需要基准细致地评估其关键能力——具体是三项核心功能：(1) *检索*，通常面向大型、复杂且持续演化的语料（如实时网络）以收集关键信息；(2) *知识综合*，生成连贯的长篇回答，把关键事实呈现出来，整合通用知识与来自众多检索来源的发现；(3) *可验证性*，提供引用，使读者能把综合回答中的每个论断追溯到检索集中某个可信来源。理想的基准必须整体覆盖这三个维度，同时提供真实且具挑战性的研究综合任务。

遗憾的是，现有基准无法满足这些目标。许多先前工作使用现有问答基准评估生成式研究综合系统，但这些基准不能反映真实的研究综合任务，而聚焦于有简短、易于验证答案的问题，在该场景下严重受限 [56, 55, 31, 20, 58, 53, 18, 61, 19, 21, 15, 49, 23]。这些问答基准无法刻画从多个来源综合而成的长篇回答的复杂性——后者是研究综合的关键组成部分。为弥补这一局限，近期一些工作转而利用带开放式研究问题与范例答案的专家策划数据集 [6, 66, 62, 60, 8, 45, 16]。不幸的是，随着新信息涌现，这些基准很快变得陈旧过时。此外，随着新模型在网络快照（包括公开数据集）上训练，这些数据集面临数据污染风险。策划、维护与更新专家策划基准的昂贵成本进一步限制了它们对真实、可扩展评估的效用。

在本工作中，我们提出 DeepScholar-bench——一个为评估生成式研究综合而设计的实时基准与整体性自动化评估框架。DeepScholar-bench 从近期高质量的 ArXiv 论文中提取查询，并聚焦一个真实研究综合任务：通过检索、综合并引用先前研究来生成论文的相关工作章节。我们计划提供*实时*基准——每月发布更新的研究查询，从业者也可以运行我们的自动化数据管线创建自己的数据集实例。此外，我们开发了一个自动化评估框架，利用从每篇 ArXiv 论文提取的人工撰写相关工作，从三个关键维度——知识综合、检索质量与可验证性——整体评估性能，所用指标与人类判断显示出高度一致。为推动未来工作，我们还开发了 DeepScholar-ref，一个在 LOTUS 框架 [28, 37] 上实现的、简单开源的生成式研究综合参考流水线。

借助 DeepScholar-bench 框架，我们系统评估了现有系统的性能，包括开源研究综合系统、配备强大专有模型的搜索智能体、OpenAI DeepResearch 以及 DeepScholar-ref。我们发现这些现有方法都有显著的改进空间，没有任何系统在所有指标上的几何平均超过 31%。此外，在若干关键指标上——包括信息点覆盖率（Nugget Coverage）、参考文献覆盖率（Reference Coverage）与文档重要性（Document Importance）——每个被评估方法的性能都远低于 40%，反映出 DeepScholar-bench 任务的内在难度：它要求系统在实时网络中导航，推理文档的相关性与重要性，并把关键事实呈现进一份连贯的最终回答。值得注意的是，OpenAI 的 DeepResearch 相对其他基线表现出色，在知识综合与检索质量上超越许多先前方法，信息点覆盖率得分为 39.2%、参考文献覆盖率 18.7%、文档重要性 12.4%；但相对许多其他方法，它在提供强可验证性方面仍然吃力。我们还发现 DeepScholar-ref 参考流水线是一个强劲的开源基线，在多数指标上提供有竞争力的性能，可验证性最高比 OpenAI 的 DeepResearch 高 6.3×。尽管如此，DeepScholar-bench 仍远未饱和，为进一步工作提供了令人兴奋的机会。我们希望我们的基准框架与参考流水线能支持新系统的进步，并相信攻克 DeepScholar-bench 是迈向更强 AI 系统的关键里程碑。

总体而言，我们的主要贡献如下：

- 我们提出 DeepScholar-bench，一个带真实研究综合任务的实时基准数据集与自动化整体评估。
- 我们开发 DeepScholar-ref，一个简单开源的生成式研究综合参考流水线，在使用相同模型时，在许多指标上与开源系统、搜索智能体及 OpenAI 的 DeepResearch 取得有竞争力的性能。
- 我们对现有基线在 DeepScholar-bench 上进行系统评估，发现显著的改进空间：没有任何系统在所有指标上的几何平均超过 31%。

表 1：评估指标汇总。

| 指标 | 描述 |
| --- | --- |
| *知识综合* | |
| 组织与连贯性（Organization & Coherency） | 评估系统回答的组织性与连贯性 |
| 信息点覆盖率（Nugget Coverage） | 评估回答对关键事实的覆盖程度 |
| *检索质量* | |
| 相关性比率（Relevance Rate） | 度量所有被引来源间的平均相关性 |
| 文档重要性（Document Importance） | 用被引次数度量被引来源的知名度 |
| 参考文献覆盖率（Reference Coverage） | 评估被引集合对关键、重要文献的覆盖程度 |
| *可验证性* | |
| 引用精确率（Citation Precision） | 度量被引来源中支持其附带论断的比例 |
| 论断覆盖率（Claim Coverage） | 度量完全被所引来源支持的论断比例 |

## 2 DeepScholar 数据集

我们研究生成学术论文相关工作章节的任务——一项基础的研究综合任务——并利用自动化数据管线提取的人工撰写范例为评估提供基准。我们从被学术会议录用的 ArXiv 论文 [5] 抓取数据集查询，并将数据集任务形式化如下：给定论文描述 $d$，目标是检索一组相关来源 $S$，并通过综合与引用检索到的文档生成相关工作章节 $W$。我们简要概述自动化数据收集框架（§2.1），并描述评估（§5）所用数据集实例（§2.2）。更多细节见附录 A.1。

### 2.1 自动化数据收集框架

我们的自动化数据收集框架旨在实现以下设计目标：

1. 纳入跨广泛研究领域*多样*的论文主题。
2. 聚焦*近期*研究论文——既为了提供真实、及时的基准查询，也为了在评估基于网络快照训练的模型时防止数据污染。
3. 控制*质量*——被抓取 ArXiv 论文与所提取数据的质量，聚焦被学术会议录用的同行评审稿件。

我们的数据管线抓取论文、过滤并提取内容以构建数据集，包括每篇 ArXiv 论文的元数据（如标题、摘要与链接）、论文的相关工作章节，以及相关工作章节中出现的参考文献引用列表。抓取器从一组配置的 ArXiv 领域（如 cs.ML）与配置的发表日期范围加载论文。为避免多 ArXiv 版本可能带来的数据污染，我们只保留 v1 版本的 ArXiv 论文。为控制论文质量，管线随后可选地依据 ArXiv 元数据，只保留在会议上标注为「accepted」或「published」的论文。我们还排除没有明确「Related Work」章节以及 .bib 文件（含格式规范的参考文献条目）的论文。然后管线处理每篇论文，从 LaTeX 文件与 PDF 文件（若可用）中提取 Related Works 章节。我们清洗提取的 LaTeX 章节以去除标签与注释。我们还提取相关工作章节中出现的所有引用，并使用 ArXiv 与 OpenAlex API [35] 恢复更详细的信息，如 ArXiv 与非 ArXiv 参考文献的摘要、作者与链接。

### 2.2 数据集描述与统计

评估（§5）所用的数据集实例 DeepScholar-June-2025 将发表日期范围配置为 2025 年 4 月至 6 月——紧随 2025 年 4 月 5 日 Llama-4 模型 [27]（我们评测的主要开源模型）的发布日期。该实例从 18 个不同的 ArXiv 领域——包括 cs.IR、cs.CV、cs.AI、cs.CL、cs.LG、cs.DC、cs.DB、cs.AR、cs.SD、cs.CR、cs.ET、cs.GR、cs.PL、cs.SY、cs.OS、cs.PF、cs.SE、cs.MM——抓取论文，并选择标注为会议录用的论文。我们还排除相关工作章节超过 1,000 词的论文以控制成本。最终数据集包含 63 篇 ArXiv 论文，每篇为我们的评估提供一条查询与一份提取的专家撰写范例。我们公开脚本以允许他人配置不同数据集，并计划每月发布近期查询的数据集。我们的实验以每篇论文的摘要作为论文描述 $d$，作为查询中的上下文提供给每个基线系统。我们分析数据集中人工撰写的范例，发现平均每个相关工作章节包含 23 条不重复的参考文献，且所有被引参考文献中超过 63% 在 ArXiv 上。
我们在附录 A.3.2 中在一个更近期、更扩展的数据集 DeepScholar-Nov-2025 上提供额外实验——该数据集包含来自超过 75 个不同 arXiv 学科的 200 条查询，横跨计算机科学、物理学、定量生物学、经济学与定量金融。我们在该数据集上的结果证实了基准与主要实验结论的泛化性。

## 3 DeepScholar 评估框架

评估研究综合本质上具有挑战性：任务复杂，且缺乏简单的「金标准」正确性概念，存在许多可行答案。为应对这些挑战，我们提出一个整体性自动化评估，从反映研究综合核心能力的三个关键维度评估 7 项细粒度指标：*知识综合*（§3.1）、*检索质量*（§3.2）与*可验证性*（§3.3）。本节概述评估框架，指标的更多细节与分析见附录 A.4，基于 LLM 指标的人工验证见附录 A.3。

### 3.1 知识综合

知识综合反映系统生成有效最终报告的能力——把关键事实与信息呈现进一份连贯的写作。我们既评估每份系统报告的整体*组织与连贯性*，也依据*信息点覆盖率*评估其事实内容。

*组织与连贯性。* 我们用 LLM 评审（LLM-as-a-judge）评估组织性与连贯性，在系统生成的报告与数据集中人工撰写的范例之间做两两比较。我们对每对被评报告做排列以避免位置偏差 [24]，并报告每个基线的胜率。这种基于模型的评估提供了可扩展性，同时是人类偏好的强替代 [42, 25, 24, 4]——我们在附录 A.3 的实验中对此进行了验证。

*信息点覆盖率。* 为评估生成报告的信息内容质量，我们使用基于信息点（nugget）的评估。一个*信息点*是与答案相关的一条关键事实或组件 [39, 51, 50, 9, 41]。对我们的任务，我们从每条查询的人工撰写范例相关工作章节生成信息点，并对每份生成的报告计算信息点覆盖率——即答案中出现的信息点比例——遵循 [39] 的自动化 LLM 方法论。

### 3.2 检索质量

生成式研究综合的关键组件是对实时网络的检索，这与传统信息检索评估差别很大 [47, 32]。这一场景缺乏带金标标签的封闭语料——专家撰写的范例只提供*一个*合理的参考集合，但可能存在许多同样高质量的可选集合。为应对这些挑战，我们评估每份生成报告检索所得参考文献集合的三项指标：相关性比率、关键来源的参考文献覆盖率，以及文档重要性。

*相关性比率。*
我们遵循 Cranfield 模型 [52]——IR 评估的标准做法，考虑在给定查询下单个文档（独立于其他文档）的相关性——评估每篇检索文档的相关性。我们用 LLM 评审方法为每个检索来源分配分级相关性分数，遵循近期工作 [51, 9, 42, 48, 6]。具体而言，LLM 评审为检索集合 $S$ 中的每个来源 $s$ 分配 0–2 的相关性分数 $Rel(s)$，我们计算 $S$ 的相关性比率为：

$$
RR(S)=\frac{1}{2|S|}\sum_{s\in S}Rel(s).
$$

*参考文献覆盖率。*
我们提出一个度量每份报告检索集合*参考文献覆盖率*的指标。度量该值的关键挑战在于定义「好报告应当引用」的核心重要来源集合。为构建该集合，我们取人工撰写范例中的全部参考文献，并将每条标注为「重要」或「不重要」——「不重要」指可以被省略或替换为其他来源的参考文献。对每份生成的报告，我们用检索到的重要参考文献数除以重要参考文献总数来报告其参考文献覆盖率。公式如下，其中 $E$ 是人工撰写范例中「重要」参考文献的集合：

$$
RC(S,E)=\frac{1}{|E|}\sum_{s\in S}I[s\in E].
$$

*文档重要性。*
上述检索指标评估了主题相关性与关键文献覆盖，而理想的研究综合系统还必须检索到许多*知名且重要*的来源。范例性人工撰写报告通常包含大量一手来源与高被引学术出版物。我们通过考虑检索集合中每个来源的被引次数来计算其*文档重要性*。具体而言，我们比较 $S$ 中来源被引次数的中位数与人工撰写范例参考集合 $S^{*}$ 中来源被引次数的中位数，并以 1 为上界：

$$
DI(S,S^{*})=min\Biggl(\;\frac{\operatorname{median}\bigl\{\operatorname{num-cites}(s)|s\in S\bigr\}}{\operatorname{median}\bigl\{\operatorname{num-cites}(s^{*})|s^{*}\in S^{*}\bigr\}},\;1\;\Biggr),
$$

其中 $\operatorname{num-cites}(s)$ 是来源 $s$ 的被引次数。

### 3.3 可验证性

为评估生成报告的可验证性，我们用基于 LLM 的蕴含评估计算引用精确率与论断覆盖率，遵循先前工作 [11, 26]。

*引用精确率。*
我们度量句子级精确率：若被引来源支持其所在句子中至少一条论断，则该引用被视为精确。对完整报告，我们通过对每条引用的精确率取平均来计算引用精确率。

*论断覆盖率。* 报告的论断覆盖率通过为每个句子打分——若该句所引来源支持句中全部论断则得 1 分——再对报告中所有句子得分取平均来计算。我们对先前工作的原始定义 [11, 57, 26] 做了两点调整以适配我们的长篇综合任务。第一，我们放宽原始论断覆盖率定义，考虑一个带支持引用的句子滑动窗口：具体而言，若某句子被该句内引用的来源或其前后 $w$ 句窗口内引用的来源完全支持，则该句得 1 分。此外，由于我们的任务查询提供了描述论文的上下文，我们把该上下文视为每个句子隐式引用的参考文献。

图 2：DeepScholar-ref 概览。系统迭代地编写查询并执行网络搜索，再把搜索结果送入一系列基于 LOTUS 系统的 LLM 数据处理语义算子——包括丢弃无关来源的过滤步骤、找出最相关来源的 top-k 排序步骤，以及从全部剩余来源生成最终报告的聚合步骤。

## 4 DeepScholar-ref

我们提出 DeepScholar-ref，一个为生成式研究综合设计的开源参考流水线。如图 2 所示，DeepScholar-ref 接收用户查询并迭代生成网络搜索查询，在每轮中总结搜索结果后再生成新查询。随后，系统利用在 LOTUS API [28] 上实现的一系列语义算子 [37] 对搜索结果做后处理。这包括一个语义过滤步骤——利用 LLM 滤除无关的来源文档——以及一个语义 top-k——基于文档与用户查询的相关性对文档做 LLM 排序。最后，我们对最终来源文档执行语义聚合以生成最终报告。参考流水线各步骤的更多细节见附录 A.6。

## 5 实验结果

在本节中，我们在 DeepScholar-bench 上评估近期最先进的生成式研究系统以及 DeepScholar-ref。总体而言，我们发现：

- 生成式研究综合的现有基线——包括强大的开源 LLM 系统、搜索智能体与商业系统——在知识综合、检索质量与可验证性三个关键维度上都显示出显著的改进空间。具体而言，没有任何系统在所有指标上的几何平均超过 31%。
- DeepScholar-ref 提供了一个强劲基线，持续优于先前开源系统与搜索智能体的性能，并取得有竞争力的表现，可验证性最高比 OpenAI 的 DeepResearch 高 6.3×。

*实验设置。*
我们评测的开源研究系统包括 DeepResearcher [65]、STORM [43] 与 OpenScholar [6]；搜索智能体分别使用 Llama-4-Scout-17B-16E-Instruct [30]、GPT-4.1-2025-04-14 [34]、o3-2025-04-16 [34]、Claude-opus-4-20250514 [3] 与 Gemini-2.5-pro [14] 模型；另有 OpenAI 的 o3-deep-research [34] 与 DeepScholar-ref。对每个被评测方法，我们控制检索语料：只允许每个系统通过 ArXiv API [5] 访问网络。我们还过滤掉任何在查询论文发表日期之后发布的搜索结果，以避免搜索期间可能的信息泄露。设置的更多细节见附录 A.2。

### 5.1 主要结果

表 2 给出各方法在 DeepScholar-June-2025 上的性能。对每个基线，我们报告在所有查询上取平均的各指标以及所有指标的几何平均。
附录 A.3 提供额外结果——包括生成报告的元数据统计（表 6）、与评估指标相关的统计（表 7）以及基于 LLM 指标的人工验证（表 10）——附录 A.7 给出报告示例。
下面详细讨论关键发现。

表 2：主要结果。最佳基线以粗体显示，次佳基线以下划线标出。∗ 表示在配对双尾 t 检验（$p<0.05$）下最佳基线显著优于次佳基线。

| | 知识综合 | | 检索质量 | | | 可验证性 | | 几何平均 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | 组织 | 信息点覆盖 | 相关率 | 文献覆盖 | 文档重要性 | 引用精确率 | 论断覆盖 ($w=1$) | |
| *人工撰写范例* | | | | | | | | |
| 人工撰写范例 | .500 | 1.000 | .585 | 1.000 | 1.000 | .900¹ | .850¹ | .782¹ |
| *开源研究系统* | | | | | | | | |
| DeepResearcher (Llama-4) | .206 | .230 | .385 | .047 | .008 | .312 | .396 | .137 |
| STORM (Llama-4) | .119 | .183 | .218 | .003 | .006 | .238 | .586 | .073 |
| OpenScholar (Llama-4) | .309 | .278 | .017 | .008 | .013 | .010 | .138 | .042 |
| *搜索智能体* | | | | | | | | |
| Search Agent (Llama-4) | .151 | .193 | .445 | .060 | .009 | .316 | .368 | .135 |
| Search Agent (GPT-4.1) | .556 | .265 | .490 | .050 | .009 | .498 | .470 | .186 |
| Search Agent (o3) | .849 | .348 | .610 | .165 | .026 | .425 | .495 | .287 |
| Search Agent (Claude) | .698 | .307 | .583 | .131 | .008 | .701 | .760 | .256 |
| Search Agent (Gemini) | .706 | .277 | .583 | .061 | .010 | .415 | .398 | .196 |
| *商业系统* | | | | | | | | |
| OpenAI DeepResearch | .857 | **.392**∗ | .629 | **.187**∗ | **.124**∗ | .399 | .138 | **.309**∗ |
| *DeepScholar 参考流水线* | | | | | | | | |
| DeepScholar-ref (Llama-4) | .206 | .241 | .436 | .103 | .008 | .674 | .851 | .195 |
| DeepScholar-ref (GPT-4.1) | .809 | .348 | .590 | .166 | .008 | .788 | .899 | .285 |
| DeepScholar-ref (GPT-4.1, o3) | .857 | .384 | .645 | .167 | .007 | .824 | .760 | .285 |
| DeepScholar-ref (GPT-4.1, Claude) | .698 | .307 | .610 | .152 | .009 | **.944**∗ | .895 | .286 |
| DeepScholar-ref (GPT-4.1, Gemini) | .770 | .331 | .590 | .181 | .006 | .904 | **.937**∗ | .282 |

**脚注 1：我们评估中的自动化可验证性指标低估了人类写作的真实可验证性，因此我们对小样本做人工验证给出估计，并在计算人工撰写范例的几何平均时排除这些指标。这是因为引用精确率与论断覆盖率要求我们评估论断与被引参考文献之间的蕴含关系。对每个基于 LLM 的系统，我们能够追踪被引来源中被直接作为上下文喂给 LLM 的精确片段与语境；而对人工撰写范例，我们缺乏指向每条参考文献所指精确文本片段的金标标签。我们对人工撰写范例的测量转而依赖每条被引来源的标题与摘要作为代理。**

#### 5.1.1 生成式研究综合系统仍有巨大改进空间

从表 2 可见，没有系统在所有指标上的几何平均超过 .31，其中 OpenAI DeepResearch 取得最高几何平均。此外，在若干关键指标上——包括信息点覆盖率、参考文献覆盖率与文档重要性——每个基线的性能都低于 .40。这反映出 DeepScholar-bench 所提供生成式研究任务的内在难度，尤其是系统需要在实时网络中导航、推理文档的覆盖与重要性，然后才在长篇报告中呈现关键信息。

我们现在逐维度分析，比较开源研究系统、搜索智能体与商业系统相对人工撰写范例的表现。在知识综合上，我们看到 OpenAI DeepResearch 在组织性（得分 .857）与信息点覆盖率（得分 .392）上都优于所有其他先前方法。OpenAI DeepResearch 以及 o3、Claude 与 Gemini 搜索智能体的组织性得分相对人工撰写范例都较高。然而在信息点覆盖率上，所有先前方法都低于 .40。这表明尽管现有系统（尤其那些使用最先进模型者）能生成组织良好、连贯的摘要，它们仍难以呈现回答研究查询所需的关键事实——这是研究综合任务的关键能力。

再看先前方法的检索质量表现，我们再次发现显著改进空间。OpenAI DeepResearch 在相关性比率、参考文献覆盖率与文档重要性上仍是先前方法中最强的，但仍远未饱和。尽管其相关性比率表现强劲（.629，超过人工范例），其参考文献覆盖率与文档重要性得分仍然极低：分别为 .187 与 .124。这表明尽管最先进的生成式研究综合系统擅长检索*相关*来源，它们仍难以找到*全面且知名的来源集合*，与人类专家的能力相比仍有差距。

最后，我们分析先前方法的可验证性表现。我们看到 OpenAI DeepResearch 在引用精确率与论断覆盖率上都被使用 GPT4.1、o3、Claude 与 Gemini 模型的搜索智能体超越。Claude 搜索智能体提供最高的引用精确率（.701）与论断覆盖率（.760）。与此同时，OpenAI 的 DeepResearch 以及所有其他先前方法的引用精确率都无法超过 .50、论断覆盖率无法超过 .60。我们还注意到人工撰写范例的引用精确率与论断覆盖率得分似乎相当低，但这些得分低估了人类写作的真实可验证性¹。总体而言，先前基于 LLM 的系统显示出显著的改进余量。

#### 5.1.2 DeepScholar-ref 为生成式研究综合提供强劲基线

我们将 DeepScholar-ref 的性能与 OpenAI DeepResearch、搜索智能体及开源系统比较，发现 DeepScholar-ref 在使用相同或更便宜模型时，在多数指标上提供了与其他基线有竞争力的强劲基线。与 OpenAI DeepResearch 相比，DeepScholar-ref (GPT-4.1, o3) 在组织性、信息点覆盖率、相关性比率、参考文献覆盖率、引用精确率与论断覆盖率上取得相同或更高的分数。值得注意的是，DeepScholar-ref 的可验证性得分最高高 6.3×，但其文档重要性相对 OpenAI 的 DeepResearch 仍较低。在附录表 6 中，我们提供额外成本分析，发现 DeepScholar-ref (GPT-4.1, o3) 是一条高效参考流水线，比 OpenAI DeepResearch 便宜 4.3×、快 2.28×。

接下来，我们比较 DeepScholar-ref 与搜索智能体的性能，发现 DeepScholar-ref 提供有竞争力且往往更强的表现——具体而言，在使用相同主模型的 5 个基线上平均，DeepScholar-ref 把组织性提升 1.18×、信息点覆盖率提升 1.17×、相关性比率提升 1.06×、参考文献覆盖率提升 2.03×、引用精确率提升 1.83×、论断覆盖率提升 1.86×。最后，我们把 DeepScholar-ref (Llama-4) 与都用 Llama-4 运行的开源研究系统比较。我们看到先前的开源研究系统在知识综合、检索质量与可验证性维度之间存在权衡。相对每项指标上表现最好的先前开源方法，DeepScholar-ref 提供有竞争力的知识综合性能，相关性比率高 1.09×、参考文献覆盖率高 2.18×、引用精确率高 2.08×、论断覆盖率高 1.41×。

总体而言，DeepScholar-ref 强劲的*相对*表现可能反映了其使用的语义数据处理算子 [37] 的效率——DeepScholar-ref 用它们对来源做基于 LLM 的过滤、排序与摘要以生成报告。值得注意的是，DeepScholar-ref 仍显示出显著改进空间，远未饱和 DeepScholar-Bench，尤其是在关键的知识综合与检索质量指标上。

表 3：比较不同检索 API 效果的消融研究。最佳基线以粗体显示，次佳基线以下划线标出。∗ 表示在配对双尾 t 检验（$p<0.05$）下最佳基线显著优于次佳基线。

| | 知识综合 | | 检索质量 | | | 可验证性 | | 几何平均 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| | 组织 | 信息点覆盖 | 相关率 | 文献覆盖 | 文档重要性 | 引用精确率 | 论断覆盖 ($w=1$) | |
| *DeepScholar-ref (GPT-4.1, Claude)* | | | | | | | | |
| arxiv.org 检索 | .698 | .307 | .610 | .152 | .009 | .944 | .895 | .286 |
| parallel.ai 检索 | .865 | .444 | .675 | .160 | .017 | .846 | .781 | .334 |
| taviliy.com 检索 | **.929**∗ | .327 | .550 | .070 | .015 | .711 | .578 | .258 |
| Oracle 检索 (arxiv.org) | .782 | .487 | .686 | **1.000**∗ | 1.000 | .955 | **.899**∗ | **.808** |
| Oracle 检索 (全部) | .778 | **.528**∗ | .680 | **1.000**∗ | .822 | .941 | .828 | .782 |
| *DeepScholar-ref (Llama-4)* | | | | | | | | |
| arxiv.org 检索 | .206 | .241 | .436 | .103 | .008 | .674 | .851 | .195 |
| parallel.ai 检索 | .246 | .265 | .559 | .114 | .015 | .223 | .543 | .186 |
| taviliy.com 检索 | .111 | .229 | .532 | .030 | .016 | .442 | .676 | .153 |
| Oracle 检索 (arxiv.org) | .202 | .316 | .681 | **1.000**∗ | 1.000 | .658 | .868 | .590 |
| Oracle 检索 (全部) | .198 | .350 | .693 | **1.000**∗ | .822 | **.796**∗ | .890 | .600 |

### 5.2 理解改进机会

为分析性能与改进机会，我们进行消融研究，测试不同检索器（包括两个 oracle 设定）。表 3 展示 DeepScholar-ref (GPT-4.1, Claude) 与 DeepScholar-ref (Llama-4) 各配 3 种检索 API 的性能：arxiv.org（主结果中的默认）、parallel.ai 与 tavily.com。此外，我们的两个 oracle 检索器包括 Oracle 检索 (arxiv.org) 设定与 Oracle 检索 (全部) 设定——分别向系统提供范例中所引重要参考文献集合中的 *ArXiv* 文献与*全部*文献，遵循我们评估参考文献覆盖率的方法论。

总体而言，结果表明关键改进机会在于检索与知识综合两方面能力。首先，我们看到 DeepScholar-ref (GPT-4.1, Claude) 配任一 oracle 检索器时在检索质量与可验证性指标上接近饱和，而同一方法使用 arxiv.org、parallel.ai 或 taviliy.com 检索器时得分低得多。具体而言，参考文献覆盖率与文档重要性存在显著性能差距，说明系统难以在实时网络中导航并找回多样的一组关键知名来源。此外，我们还看到 oracle 检索器把两个 DeepScholar-ref 方法的信息点覆盖率最高提升 1.62×（相对 arxiv.org、parallel.ai 或 tavily.ai 检索器）。然而 oracle 设定仍远未饱和信息点覆盖率，凸显出即便拥有高质量来源，AI 系统仍难以有效呈现重要事实与洞见。

### 5.3 人工评估

为评估基于 LLM 的指标是否反映人类专家判断，我们进行了 11 位标注者的人工评估——他们均为北美四所研究型大学的计算机科学博士生。总计收集超过 300 条人工标注，用于验证我们自动化评估中评估知识综合与检索质量所用的 LLM 评审。设置的更多细节见附录 A.3.4。

表 4：
比较人类与 LLM 在组织性、信息点重要性判断与参考文献重要性判断上的混淆矩阵，每张表中行与列分别代表人类与 LLM 的判断。

| 组织性 | | | |
| --- | --- | --- | --- |
| 人类 / LLM | 范例 | 生成 | 平局 |
| 范例 | 14.29% | 0% | 14.29% |
| 生成 | 0% | 57.14% | 14.29% |
| 平局 | 0% | 0% | 0% |

| 信息点重要性 | | |
| --- | --- | --- |
| 人类 / LLM | 关键（Vital） | 可有可无（Okay） |
| 关键 | 58.33% | 8.33% |
| 可有可无 | 8.33% | 25.00% |
| 无关 | 0% | 0% |

| 参考文献重要性 | | |
| --- | --- | --- |
| 人类 / LLM | 不重要 | 重要 |
| 不重要 | 40.2% | 9.8% |
| 重要 | 24.2% | 25.7% |

##### 一致性分析。

表 4 以混淆矩阵展示人工评估研究的结果——取人工标注者多数票与 LLM 评审的交叉。总体而言，结果基于 LLM 评审与专家标注者的高度一致展示了其稳健性。具体而言，我们观察到判断组织性的两两比较一致率为 71.43%，为计算信息点覆盖率而做信息点标注的一致率为 83.33%，为计算参考文献覆盖率而标注参考文献重要性的一致率为 65.9%。值得注意的是，这些任务都要求对复杂学术文献与冗长的候选相关工作章节进行推理。我们研究观察到的一致率为基于 LLM 的自动化评审与指标评估复杂生成式研究综合任务提供了可喜的验证。

对组织性，我们从混淆矩阵看到人类与 LLM 评审在两两比较上大多一致，强烈分歧（即人类偏好范例报告而 LLM 偏好生成报告，或反之）很少。而且，在人类与 LLM 评审之间出现的分歧中，LLM 误判在选择范例报告与生成报告之间相对均衡。

对信息点重要性，我们观察到除混淆矩阵显示的高一致率外，人类多数票认为所有 LLM 生成的信息点都相关，表明幻觉很少。我们还看到 LLM 评审的假阳性率与假阴性率相近且都相当小（低于 10%），再次表明严重的 LLM 误标注相当罕见。

最后，对参考文献重要性，我们观察到总体一致率为 65.9%，且重要的是假阴性率为 9.8%——即 LLM 错误地把某参考文献标注为不重要的情况。低假阴性率表明我们的参考文献覆盖率指标错误惩罚系统的可能性很低。较大的非对角质量（24.2%）反映 LLM 对关键参考文献标注不足，说明我们的参考文献覆盖率得分是一个相当保守的指标，只度量每个查询全部真正重要参考文献中一个子集的「召回」。

## 6 相关工作

*长篇综合基准。*
我们的工作用自动化数据管线提出持续更新的实时基准，而若干先前工作转而为长篇研究综合任务提供专家策划的数据集，包括 ScholarQABench [6]、OpenResearcher [66]、DeepConsult [62]、ResearcherBench [60]、DeepResearch Bench [8]、Deep Research Bench [10]、SurGE [45] 与 LiveDRBench [16]。遗憾的是，这些专家策划的基准构建与更新昂贵，会随着新信息出现而很快过时，并随着新模型在公开数据上训练而面临数据污染风险。

另外，若干近期基准——包括 AcademicEval [63]、LongBench-Cite [64] 与 SciIG [12]——评估的长篇生成任务*不需要在实时网络上搜索*，而那是生成式研究综合与我们基准的关键组件。其他基准聚焦其他长篇生成任务，如维基百科式文章生成 [43]，与我们对复杂研究综合任务的聚焦差别很大。关键的是，与这些先前工作都不同，我们的工作提出了一个评估生成式研究综合的实时、持续更新基准。

*事实性与问答基准。*
本工作为研究缺乏绝对正确性概念、允许多个合理答案的复杂长篇研究综合任务提出框架，而若干近期工作把评估聚焦在具有简短、易验证答案的问答（QA）与事实性基准上。这些先前基准包括 SimpleQA [55]、FRAMES [20]、GAIA [31]、BrowserComp [56]、BrowserComp-Plus [7]、WebWalkerQA [58]、DeepResearch Arena [54]，以及其他传统上用于评估检索增强生成（RAG）的基准 [53, 18, 61, 19, 21, 15, 49, 23]。此外，若干基准为实时基准开发了自动化数据集策划管线，但其任务聚焦简短问答而非长篇报告生成 [36, 29, 17]。

## 7 结论

在本工作中，我们提出了 DeepScholar-bench——一个实时数据集与整体性自动化评估框架，旨在严格基准测试新兴的生成式研究综合系统。通过自动从高质量、近期的 ArXiv 论文获取查询，我们的基准在提供真实研究综合任务的同时，缓解了数据陈旧与训练污染的风险。此外，DeepScholar-bench 提供自动化评估以整体度量三个关键维度：检索质量、知识综合与可验证性。我们还发布 DeepScholar-ref 参考流水线，并发现它为生成式研究综合提供了强劲基线。总体而言，我们对先前开源系统、搜索智能体、OpenAI 的 DeepResearch 与 DeepScholar-ref 的系统评估显示出未来工作的巨大机会——没有任何系统在所有指标上的几何平均超过 31%。这些结果既展示了 DeepScholar-bench 的难度，也展示了这一领域进一步发展的激动人心的机会。我们希望 DeepScholar-bench 与 DeepScholar-ref 能支持更强大的生成式研究综合 AI 系统的开发。

## 致谢

本研究部分由 Stanford DAWN 项目的附属成员与其他支持者资助，包括 Meta、Google 与 VMware，以及 Cisco、SAP 与斯隆研究奖。本材料中表达的观点、发现、结论或建议均为作者个人观点，不一定反映资助者的观点。

## 参考文献

- [1]
  S. Alzubi, C. Brooks, P. Chiniya, E. Contente, C. von Gerlach, L. Irwin, Y. Jiang, A. Kaz, W. Nguyen, S. Oh, H. Tyagi, and P. Viswanath (2025)
  Open Deep Search: Democratizing Search with Open-source Reasoning Agents.
  (en).
  External Links: [Link](https://arxiv.org/abs/2503.20201v1)
  Cited by: [§A.2.2](#A1.SS2.SSS2.p1.1 "A.2.2 Search Agents ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [2]
  Anthropic (2025)
  Claude takes research to new places.
  (en).
  External Links: [Link](https://www.anthropic.com/news/research)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [3]
  Anthropic (2025)
  Introducing Claude 4.
  (en).
  External Links: [Link](https://www.anthropic.com/news/claude-4)
  Cited by: [§A.2.2](#A1.SS2.SSS2.p1.1 "A.2.2 Search Agents ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2.4](#A1.SS2.SSS4.p1.1 "A.2.4 DeepScholar-ref ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2](#A1.SS2.p1.1 "A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§5](#S5.p2.1 "5 Experimental Results ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [4]
  N. Arabzadeh and C. L. A. Clarke (2025)
  Benchmarking llm-based relevance judgment methods.
  In Proceedings of the 48th International ACM SIGIR Conference on Research and Development in Information Retrieval,
  SIGIR ’25, New York, NY, USA.
  External Links: ISBN 9798400715921,
  [Link](https://doi.org/10.1145/3726302.3730305),
  [Document](https://dx.doi.org/10.1145/3726302.3730305)
  Cited by: [§3.1](#S3.SS1.p2.1 "3.1 Knowledge Synthesis ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [5]
  arxiv (2025)
  arXiv.org e-Print archive.
  External Links: [Link](https://arxiv.org/)
  Cited by: [§A.2.2](#A1.SS2.SSS2.p1.1 "A.2.2 Search Agents ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§2](#S2.p1.1.1 "2 The DeepScholar Dataset ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§5](#S5.p2.1 "5 Experimental Results ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [6]
  A. Asai, J. He, R. Shao, W. Shi, A. Singh, J. C. Chang, K. Lo, L. Soldaini, S. Feldman, M. D’arcy, D. Wadden, M. Latzke, M. Tian, P. Ji, S. Liu, H. Tong, B. Wu, Y. Xiong, L. Zettlemoyer, G. Neubig, D. Weld, D. Downey, W. Yih, P. W. Koh, and H. Hajishirzi (2024)
  OpenScholar: Synthesizing Scientific Literature with Retrieval-augmented LMs.
   arXiv.
  Note: arXiv:2411.14199 [cs]
  External Links: [Link](http://arxiv.org/abs/2411.14199),
  [Document](https://dx.doi.org/10.48550/arXiv.2411.14199)
  Cited by: [§A.2.1](#A1.SS2.SSS1.p1.1 "A.2.1 Open-source Research Systems ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2.1](#A1.SS2.SSS1.p4.1 "A.2.1 Open-source Research Systems ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2](#A1.SS2.p1.1 "A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§1](#S1.p1.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§3.2](#S3.SS2.p2.1 "3.2 Retrieval Quality ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§5](#S5.p2.1 "5 Experimental Results ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p1.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [7]
  Z. Chen, X. Ma, S. Zhuang, P. Nie, K. Zou, A. Liu, J. Green, K. Patel, R. Meng, M. Su, S. Sharifymoghaddam, Y. Li, H. Hong, X. Shi, X. Liu, N. Thakur, C. Zhang, L. Gao, W. Chen, and J. Lin (2025)
  BrowseComp-Plus: A More Fair and Transparent Evaluation Benchmark of Deep-Research Agent.
   arXiv.
  Note: arXiv:2508.06600 [cs]
  External Links: [Link](http://arxiv.org/abs/2508.06600),
  [Document](https://dx.doi.org/10.48550/arXiv.2508.06600)
  Cited by: [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [8]
  M. Du, B. Xu, C. Zhu, X. Wang, and Z. Mao (2025)
  DeepResearch Bench: A Comprehensive Benchmark for Deep Research Agents.
   arXiv.
  Note: arXiv:2506.11763 [cs]Comment: 31 pages, 5 figures
  External Links: [Link](http://arxiv.org/abs/2506.11763),
  [Document](https://dx.doi.org/10.48550/arXiv.2506.11763)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p1.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [9]
  G. Faggioli, L. Dietz, C. Clarke, G. Demartini, M. Hagen, C. Hauff, N. Kando, E. Kanoulas, M. Potthast, B. Stein, and H. Wachsmuth (2023)
  Perspectives on Large Language Models for Relevance Judgment.
  In Proceedings of the 2023 ACM SIGIR International Conference on Theory of Information Retrieval,
  pp. 39–50.
  Note: arXiv:2304.09161 [cs]
  External Links: [Link](http://arxiv.org/abs/2304.09161),
  [Document](https://dx.doi.org/10.1145/3578337.3605136)
  Cited by: [§3.1](#S3.SS1.p3.1 "3.1 Knowledge Synthesis ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§3.2](#S3.SS2.p2.1 "3.2 Retrieval Quality ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [10]
  FutureSearch, N. I. Bosse, J. Evans, R. G. Gambee, D. Hnyk, P. Mühlbacher, L. Phillips, D. Schwarz, and J. Wildman (2025)
  Deep Research Bench: Evaluating AI Web Research Agents.
   arXiv.
  Note: arXiv:2506.06287 [cs]
  External Links: [Link](http://arxiv.org/abs/2506.06287),
  [Document](https://dx.doi.org/10.48550/arXiv.2506.06287)
  Cited by: [§6](#S6.p1.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [11]
  T. Gao, H. Yen, J. Yu, and D. Chen (2023)
  Enabling Large Language Models to Generate Text with Citations.
  In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, H. Bouamor, J. Pino, and K. Bali (Eds.),
  Singapore, pp. 6465–6488.
  External Links: [Link](https://aclanthology.org/2023.emnlp-main.398/),
  [Document](https://dx.doi.org/10.18653/v1/2023.emnlp-main.398)
  Cited by: [5th item](#A1.I1.i5.p1.1 "In A.4 Evaluation Details ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§3.3](#S3.SS3.p1.1 "3.3 Verifiability ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§3.3](#S3.SS3.p3.1 "3.3 Verifiability ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [12]
  K. Garg, F. Shaik, S. Bandyopadhyay, and C. Caragea (2025)
  Let’s Use ChatGPT To Write Our Paper! Benchmarking LLMs To Write the Introduction of a Research Paper.
   arXiv.
  Note: arXiv:2508.14273 [cs]Comment: 20 pages, 15 figures
  External Links: [Link](http://arxiv.org/abs/2508.14273),
  [Document](https://dx.doi.org/10.48550/arXiv.2508.14273)
  Cited by: [§6](#S6.p2.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [13]
  Gemini (2025)
  Gemini Deep Research — your personal research assistant.
  External Links: [Link](https://gemini.google/overview/deep-research/)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [14]
  Gemini (2025)
  Gemini models | Gemini API.
  (en).
  External Links: [Link](https://ai.google.dev/gemini-api/docs/models)
  Cited by: [§A.2.2](#A1.SS2.SSS2.p1.1 "A.2.2 Search Agents ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2.4](#A1.SS2.SSS4.p1.1 "A.2.4 DeepScholar-ref ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2](#A1.SS2.p1.1 "A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§5](#S5.p2.1 "5 Experimental Results ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [15]
  X. Ho, A. Duong Nguyen, S. Sugawara, and A. Aizawa (2020)
  Constructing A Multi-hop QA Dataset for Comprehensive Evaluation of Reasoning Steps.
  In Proceedings of the 28th International Conference on Computational Linguistics, D. Scott, N. Bel, and C. Zong (Eds.),
  Barcelona, Spain (Online), pp. 6609–6625.
  External Links: [Link](https://aclanthology.org/2020.coling-main.580/),
  [Document](https://dx.doi.org/10.18653/v1/2020.coling-main.580)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [16]
  A. Java, A. Khandelwal, S. Midigeshi, A. Halfaker, A. Deshpande, N. Goyal, A. Gupta, N. Natarajan, and A. Sharma (2025)
  Characterizing Deep Research: A Benchmark and Formal Definition.
   arXiv.
  Note: arXiv:2508.04183 [cs]
  version: 1Comment: First three authors contributed equally (ordered alphabetically)
  External Links: [Link](http://arxiv.org/abs/2508.04183),
  [Document](https://dx.doi.org/10.48550/arXiv.2508.04183)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p1.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [17]
  M. Jiang, J. Gao, J. Zhan, and D. Wang (2025)
  MAC: A Live Benchmark for Multimodal Large Language Models in Scientific Understanding.
   arXiv.
  Note: arXiv:2508.15802 [cs]
  External Links: [Link](http://arxiv.org/abs/2508.15802),
  [Document](https://dx.doi.org/10.48550/arXiv.2508.15802)
  Cited by: [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [18]
  Q. Jin, B. Dhingra, Z. Liu, W. Cohen, and X. Lu (2019)
  PubMedQA: A Dataset for Biomedical Research Question Answering.
  In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), K. Inui, J. Jiang, V. Ng, and X. Wan (Eds.),
  Hong Kong, China, pp. 2567–2577.
  External Links: [Link](https://aclanthology.org/D19-1259/),
  [Document](https://dx.doi.org/10.18653/v1/D19-1259)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [19]
  M. Joshi, E. Choi, D. Weld, and L. Zettlemoyer (2017)
  TriviaQA: A Large Scale Distantly Supervised Challenge Dataset for Reading Comprehension.
  In Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), R. Barzilay and M. Kan (Eds.),
  Vancouver, Canada, pp. 1601–1611.
  External Links: [Link](https://aclanthology.org/P17-1147/),
  [Document](https://dx.doi.org/10.18653/v1/P17-1147)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [20]
  S. Krishna, K. Krishna, A. Mohananey, S. Schwarcz, A. Stambler, S. Upadhyay, and M. Faruqui (2025)
  Fact, Fetch, and Reason: A Unified Evaluation of Retrieval-Augmented Generation.
   arXiv.
  Note: arXiv:2409.12941 [cs]Comment: Annual Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics (NAACL), 2025
  External Links: [Link](http://arxiv.org/abs/2409.12941),
  [Document](https://dx.doi.org/10.48550/arXiv.2409.12941)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [21]
  T. Kwiatkowski, J. Palomaki, O. Redfield, M. Collins, A. Parikh, C. Alberti, D. Epstein, I. Polosukhin, J. Devlin, K. Lee, K. Toutanova, L. Jones, M. Kelcey, M. Chang, A. M. Dai, J. Uszkoreit, Q. Le, and S. Petrov (2019)
  Natural Questions: A Benchmark for Question Answering Research.
  Transactions of the Association for Computational Linguistics 7, pp. 452–466.
  Note: Place: Cambridge, MA
  Publisher: MIT Press
  External Links: [Link](https://aclanthology.org/Q19-1026/),
  [Document](https://dx.doi.org/10.1162/tacl%5Fa%5F00276)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [22]
  W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E. Gonzalez, H. Zhang, and I. Stoica (2023)
  Efficient Memory Management for Large Language Model Serving with PagedAttention.
   arXiv.
  Note: arXiv:2309.06180 [cs]Comment: SOSP 2023
  External Links: [Link](http://arxiv.org/abs/2309.06180),
  [Document](https://dx.doi.org/10.48550/arXiv.2309.06180)
  Cited by: [§A.2.1](#A1.SS2.SSS1.p1.1 "A.2.1 Open-source Research Systems ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [23]
  Y. Lee, K. Lee, S. Park, D. Hwang, J. Kim, H. Lee, and M. Lee (2023)
  QASA: Advanced Question Answering on Scientific Articles.
  In Proceedings of the 40th International Conference on Machine Learning,
  pp. 19036–19052 (en).
  External Links: [Link](https://proceedings.mlr.press/v202/lee23n.html)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [24]
  D. Li, B. Jiang, L. Huang, A. Beigi, C. Zhao, Z. Tan, A. Bhattacharjee, Y. Jiang, C. Chen, T. Wu, K. Shu, L. Cheng, and H. Liu (2025)
  From Generation to Judgment: Opportunities and Challenges of LLM-as-a-judge.
   arXiv.
  Note: arXiv:2411.16594 [cs]Comment: v6: add new citations; 36 pages, 5 figures
  External Links: [Link](http://arxiv.org/abs/2411.16594),
  [Document](https://dx.doi.org/10.48550/arXiv.2411.16594)
  Cited by: [§3.1](#S3.SS1.p2.1 "3.1 Knowledge Synthesis ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [25]
  R. Li, T. Patel, and X. Du (2024)
  PRD: Peer Rank and Discussion Improve Large Language Model based Evaluations.
   arXiv.
  Note: arXiv:2307.02762 [cs]Comment: Accepted by TMLR
  External Links: [Link](http://arxiv.org/abs/2307.02762),
  [Document](https://dx.doi.org/10.48550/arXiv.2307.02762)
  Cited by: [§3.1](#S3.SS1.p2.1 "3.1 Knowledge Synthesis ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [26]
  N. Liu, T. Zhang, and P. Liang (2023)
  Evaluating Verifiability in Generative Search Engines.
  In Findings of the Association for Computational Linguistics: EMNLP 2023, H. Bouamor, J. Pino, and K. Bali (Eds.),
  Singapore, pp. 7001–7025.
  External Links: [Link](https://aclanthology.org/2023.findings-emnlp.467/),
  [Document](https://dx.doi.org/10.18653/v1/2023.findings-emnlp.467)
  Cited by: [5th item](#A1.I1.i5.p1.1 "In A.4 Evaluation Details ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§3.3](#S3.SS3.p1.1 "3.3 Verifiability ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§3.3](#S3.SS3.p3.1 "3.3 Verifiability ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [27]
   (2025)
  Llama 4 - a meta-llama Collection.
  External Links: [Link](https://huggingface.co/collections/meta-llama/llama-4-67f0c30d9fe03840bc9d0164)
  Cited by: [§2.2](#S2.SS2.p1.1 "2.2 Dataset Description and Statistics ‣ 2 The DeepScholar Dataset ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [28]
  lotus (2025)
  Lotus-data/lotus.
   lotus-data.
  Note: original-date: 2024-07-16T16:39:06Z
  External Links: [Link](https://github.com/lotus-data/lotus)
  Cited by: [item Filtering](#A1.I2.ix2.p1.1 "In A.6 DeepScholar-ref Details and Configurations ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§1](#S1.p4.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§4](#S4.p1.1 "4 DeepScholar-ref ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [29]
  J. A. Meem, M. S. Rashid, Y. Dong, and V. Hristidis (2024)
  PAT-Questions: A Self-Updating Benchmark for Present-Anchored Temporal Question-Answering.
   arXiv.
  Note: arXiv:2402.11034 [cs]Comment: Accepted to Findings of ACL ’24
  External Links: [Link](http://arxiv.org/abs/2402.11034),
  [Document](https://dx.doi.org/10.48550/arXiv.2402.11034)
  Cited by: [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [30]
  Meta (2025)
  Meta-llama/Llama-4-Scout-17B-16E-Instruct · Hugging Face.
  External Links: [Link](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct)
  Cited by: [§A.2.1](#A1.SS2.SSS1.p1.1 "A.2.1 Open-source Research Systems ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2.1](#A1.SS2.SSS1.p2.1 "A.2.1 Open-source Research Systems ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2.2](#A1.SS2.SSS2.p1.1 "A.2.2 Search Agents ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2.4](#A1.SS2.SSS4.p1.1 "A.2.4 DeepScholar-ref ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2](#A1.SS2.p1.1 "A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§5](#S5.p2.1 "5 Experimental Results ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [31]
  G. Mialon, C. Fourrier, C. Swift, T. Wolf, Y. LeCun, and T. Scialom (2023)
  GAIA: a benchmark for General AI Assistants.
   arXiv.
  Note: arXiv:2311.12983 [cs]
  External Links: [Link](http://arxiv.org/abs/2311.12983),
  [Document](https://dx.doi.org/10.48550/arXiv.2311.12983)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [32]
  F. Nanni, B. Mitra, M. Magnusson, and L. Dietz (2017)
  Benchmark for Complex Answer Retrieval.
   arXiv.
  Note: arXiv:1705.04803 [cs]
  External Links: [Link](http://arxiv.org/abs/1705.04803),
  [Document](https://dx.doi.org/10.48550/arXiv.1705.04803)
  Cited by: [§3.2](#S3.SS2.p1.1 "3.2 Retrieval Quality ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [33]
  OpenAI (2025)
  Introducing deep research | OpenAI.
  External Links: [Link](https://openai.com/index/introducing-deep-research/)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [34]
  OpenAI (2025)
  Model - OpenAI API.
  (en-US).
  External Links: [Link](https://platform.openai.com)
  Cited by: [§A.2.2](#A1.SS2.SSS2.p1.1 "A.2.2 Search Agents ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2.3](#A1.SS2.SSS3.p1.1 "A.2.3 Commercial Systems. ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2.4](#A1.SS2.SSS4.p1.1 "A.2.4 DeepScholar-ref ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2](#A1.SS2.p1.1 "A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2](#A1.SS2.p2.1 "A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§5](#S5.p2.1 "5 Experimental Results ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [35]
  OpenAlex (2025)
  OpenAlex: The open catalog to the global research system | OpenAlex.
  External Links: [Link](https://openalex.org/)
  Cited by: [§A.2](#A1.SS2.p2.1 "A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.4.3](#A1.SS4.SSS3.p1.1 "A.4.3 Document Importance Across Human Exemplars ‣ A.4 Evaluation Details ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§2.1](#S2.SS1.p2.1 "2.1 Automated Data Collection Framework ‣ 2 The DeepScholar Dataset ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [36]
  J. Ouyang, T. Pan, M. Cheng, R. Yan, Y. Luo, J. Lin, and Q. Liu (2025)
  HoH: A Dynamic Benchmark for Evaluating the Impact of Outdated Information on Retrieval-Augmented Generation.
   arXiv.
  Note: arXiv:2503.04800 [cs]
  External Links: [Link](http://arxiv.org/abs/2503.04800),
  [Document](https://dx.doi.org/10.48550/arXiv.2503.04800)
  Cited by: [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [37]
  L. Patel, S. Jha, M. Pan, H. Gupta, P. Asawa, C. Guestrin, and M. Zaharia (2025)
  Semantic Operators: A Declarative Model for Rich, AI-based Data Processing.
   arXiv.
  Note: arXiv:2407.11418 [cs]
  External Links: [Link](http://arxiv.org/abs/2407.11418),
  [Document](https://dx.doi.org/10.48550/arXiv.2407.11418)
  Cited by: [item Filtering](#A1.I2.ix2.p1.1 "In A.6 DeepScholar-ref Details and Configurations ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§1](#S1.p4.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§4](#S4.p1.1 "4 DeepScholar-ref ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§5.1.2](#S5.SS1.SSS2.p3.1 "5.1.2 DeepScholar-ref Provides a Strong Baseline for Generative Research Synthesis. ‣ 5.1 Main Results ‣ 5 Experimental Results ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [38]
  Perplexity (2025)
  Introducing Perplexity Deep Research.
  External Links: [Link](https://www.perplexity.ai/hub/blog/introducing-perplexity-deep-research)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [39]
  R. Pradeep, N. Thakur, S. Upadhyay, D. Campos, N. Craswell, and J. Lin (2025)
  The Great Nugget Recall: Automating Fact Extraction and RAG Evaluation with Large Language Models.
   arXiv.
  Note: arXiv:2504.15068 [cs]Comment: To appear in SIGIR 2025. Significant updates and revisions to arXiv:2411.09607
  External Links: [Link](http://arxiv.org/abs/2504.15068),
  [Document](https://dx.doi.org/10.48550/arXiv.2504.15068)
  Cited by: [2nd item](#A1.I1.i2.p1.1 "In A.4 Evaluation Details ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§3.1](#S3.SS1.p3.1 "3.1 Knowledge Synthesis ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [40]
  Qwen, A. Yang, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Li, D. Liu, F. Huang, H. Wei, H. Lin, J. Yang, J. Tu, J. Zhang, J. Yang, J. Yang, J. Zhou, J. Lin, K. Dang, K. Lu, K. Bao, K. Yang, L. Yu, M. Li, M. Xue, P. Zhang, Q. Zhu, R. Men, R. Lin, T. Li, T. Tang, T. Xia, X. Ren, X. Ren, Y. Fan, Y. Su, Y. Zhang, Y. Wan, Y. Liu, Z. Cui, Z. Zhang, and Z. Qiu (2025)
  Qwen2.5 Technical Report.
   arXiv.
  Note: arXiv:2412.15115 [cs]
  External Links: [Link](http://arxiv.org/abs/2412.15115),
  [Document](https://dx.doi.org/10.48550/arXiv.2412.15115)
  Cited by: [§A.2.1](#A1.SS2.SSS1.p2.1 "A.2.1 Open-source Research Systems ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [41]
  H. A. Rahmani, C. Siro, M. Aliannejadi, N. Craswell, C. L. A. Clarke, G. Faggioli, B. Mitra, P. Thomas, and E. Yilmaz (2024)
  LLM4Eval: Large Language Model for Evaluation in IR.
  In Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval,
  Washington DC USA, pp. 3040–3043 (en).
  External Links: ISBN 9798400704314,
  [Link](https://dl.acm.org/doi/10.1145/3626772.3657992),
  [Document](https://dx.doi.org/10.1145/3626772.3657992)
  Cited by: [§3.1](#S3.SS1.p3.1 "3.1 Knowledge Synthesis ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [42]
  H. A. Rahmani, E. Yilmaz, N. Craswell, B. Mitra, P. Thomas, C. L. A. Clarke, M. Aliannejadi, C. Siro, and G. Faggioli (2024)
  LLMJudge: LLMs for Relevance Judgments.
   arXiv.
  Note: arXiv:2408.08896 [cs]Comment: LLMJudge Challenge Overview, 3 pages
  External Links: [Link](http://arxiv.org/abs/2408.08896),
  [Document](https://dx.doi.org/10.48550/arXiv.2408.08896)
  Cited by: [§3.1](#S3.SS1.p2.1 "3.1 Knowledge Synthesis ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§3.2](#S3.SS2.p2.1 "3.2 Retrieval Quality ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [43]
  Y. Shao, Y. Jiang, T. A. Kanell, P. Xu, O. Khattab, and M. S. Lam (2024)
  Assisting in Writing Wikipedia-like Articles From Scratch with Large Language Models.
   arXiv.
  Note: arXiv:2402.14207 [cs]Comment: 27 pages, NAACL 2024 Main Conference
  External Links: [Link](http://arxiv.org/abs/2402.14207),
  [Document](https://dx.doi.org/10.48550/arXiv.2402.14207)
  Cited by: [§A.2.1](#A1.SS2.SSS1.p1.1 "A.2.1 Open-source Research Systems ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2.1](#A1.SS2.SSS1.p3.1 "A.2.1 Open-source Research Systems ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2](#A1.SS2.p1.1 "A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§1](#S1.p1.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§5](#S5.p2.1 "5 Experimental Results ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p2.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [44]
  L. Soldaini, R. Kinney, A. Bhagia, D. Schwenk, D. Atkinson, R. Authur, B. Bogin, K. Chandu, J. Dumas, Y. Elazar, V. Hofmann, A. Jha, S. Kumar, L. Lucy, X. Lyu, N. Lambert, I. Magnusson, J. Morrison, N. Muennighoff, A. Naik, C. Nam, M. Peters, A. Ravichander, K. Richardson, Z. Shen, E. Strubell, N. Subramani, O. Tafjord, E. Walsh, L. Zettlemoyer, N. Smith, H. Hajishirzi, I. Beltagy, D. Groeneveld, J. Dodge, and K. Lo (2024)
  Dolma: an Open Corpus of Three Trillion Tokens for Language Model Pretraining Research.
  In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), L. Ku, A. Martins, and V. Srikumar (Eds.),
  Bangkok, Thailand, pp. 15725–15788.
  External Links: [Link](https://aclanthology.org/2024.acl-long.840/),
  [Document](https://dx.doi.org/10.18653/v1/2024.acl-long.840)
  Cited by: [§A.2.1](#A1.SS2.SSS1.p4.1 "A.2.1 Open-source Research Systems ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [45]
  W. Su, A. Xie, Q. Ai, J. Long, J. Mao, Z. Ye, and Y. Liu (2025)
  Benchmarking Computer Science Survey Generation.
   arXiv.
  Note: arXiv:2508.15658 [cs]
  External Links: [Link](http://arxiv.org/abs/2508.15658),
  [Document](https://dx.doi.org/10.48550/arXiv.2508.15658)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p1.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [46]
  N. Thakur, J. Lin, S. Havens, M. Carbin, O. Khattab, and A. Drozdov (2025)
  FreshStack: Building Realistic Benchmarks for Evaluating Retrieval on Technical Documents.
   arXiv.
  Note: arXiv:2504.13128 [cs]Comment: 21 pages, 4 figures, 8 tables
  External Links: [Link](http://arxiv.org/abs/2504.13128),
  [Document](https://dx.doi.org/10.48550/arXiv.2504.13128)
  Cited by: [§A.3.5](#A1.SS3.SSS5.p1.1 "A.3.5 Manual Validation of LLM-based Evaluation ‣ A.3 Additional Experimental Results ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [47]
  N. Thakur, N. Reimers, A. Rücklé, A. Srivastava, and I. Gurevych (2021)
  BEIR: A Heterogenous Benchmark for Zero-shot Evaluation of Information Retrieval Models.
   arXiv.
  Note: arXiv:2104.08663 [cs]Comment: Accepted at NeurIPS 2021 Dataset and Benchmark Track
  External Links: [Link](http://arxiv.org/abs/2104.08663),
  [Document](https://dx.doi.org/10.48550/arXiv.2104.08663)
  Cited by: [§3.2](#S3.SS2.p1.1 "3.2 Retrieval Quality ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [48]
  P. Thomas, S. Spielman, N. Craswell, and B. Mitra (2024)
  Large language models can accurately predict searcher preferences.
   arXiv.
  Note: arXiv:2309.10621 [cs]
  External Links: [Link](http://arxiv.org/abs/2309.10621),
  [Document](https://dx.doi.org/10.48550/arXiv.2309.10621)
  Cited by: [§3.2](#S3.SS2.p2.1 "3.2 Retrieval Quality ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [49]
  H. Trivedi, N. Balasubramanian, T. Khot, and A. Sabharwal (2022)
  MuSiQue: Multihop Questions via Single-hop Question Composition.
   arXiv.
  Note: arXiv:2108.00573 [cs]Comment: Accepted for publication in Transactions of the Association for Computational Linguistics (TACL), 2022
  External Links: [Link](http://arxiv.org/abs/2108.00573),
  [Document](https://dx.doi.org/10.48550/arXiv.2108.00573)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [50]
  S. Upadhyay, R. Pradeep, N. Thakur, D. Campos, N. Craswell, I. Soboroff, H. T. Dang, and J. Lin (2024)
  A Large-Scale Study of Relevance Assessments with Large Language Models: An Initial Look.
   arXiv.
  Note: arXiv:2411.08275 [cs]
  External Links: [Link](http://arxiv.org/abs/2411.08275),
  [Document](https://dx.doi.org/10.48550/arXiv.2411.08275)
  Cited by: [§3.1](#S3.SS1.p3.1 "3.1 Knowledge Synthesis ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [51]
  S. Upadhyay, R. Pradeep, N. Thakur, N. Craswell, and J. Lin (2024)
  UMBRELA: UMbrela is the (Open-Source Reproduction of the) Bing RELevance Assessor.
   arXiv.
  Note: arXiv:2406.06519 [cs]Comment: 5 pages, 3 figures
  External Links: [Link](http://arxiv.org/abs/2406.06519),
  [Document](https://dx.doi.org/10.48550/arXiv.2406.06519)
  Cited by: [§3.1](#S3.SS1.p3.1 "3.1 Knowledge Synthesis ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§3.2](#S3.SS2.p2.1 "3.2 Retrieval Quality ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [52]
  E. M. Voorhees (2009)
  I Come Not To Bury Cranfield, but to Praise It.
  NIST (en).
  Note: Last Modified: 2017-02-19T20:02-05:00
  Publisher: Ellen M. Voorhees
  External Links: [Link](https://www.nist.gov/publications/i-come-not-bury-cranfield-praise-it)
  Cited by: [§3.2](#S3.SS2.p2.1 "3.2 Retrieval Quality ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [53]
  D. Wadden, S. Lin, K. Lo, L. L. Wang, M. van Zuylen, A. Cohan, and H. Hajishirzi (2020)
  Fact or Fiction: Verifying Scientific Claims.
  In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP), B. Webber, T. Cohn, Y. He, and Y. Liu (Eds.),
  Online, pp. 7534–7550.
  External Links: [Link](https://aclanthology.org/2020.emnlp-main.609/),
  [Document](https://dx.doi.org/10.18653/v1/2020.emnlp-main.609)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [54]
  H. Wan, C. Yang, J. Yu, M. Tu, J. Lu, D. Yu, J. Cao, B. Gao, J. Xie, A. Wang, W. Zhang, P. Torr, and D. Zhou (2025)
  DeepResearch Arena: The First Exam of LLMs’ Research Abilities via Seminar-Grounded Tasks.
   arXiv.
  Note: arXiv:2509.01396 [cs]
  External Links: [Link](http://arxiv.org/abs/2509.01396),
  [Document](https://dx.doi.org/10.48550/arXiv.2509.01396)
  Cited by: [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [55]
  J. Wei, N. Karina, H. W. Chung, Y. J. Jiao, S. Papay, A. Glaese, J. Schulman, and W. Fedus (2024)
  Measuring short-form factuality in large language models.
   arXiv.
  Note: arXiv:2411.04368 [cs]Comment: Blog post: https://openai.com/index/introducing-simpleqa/
  External Links: [Link](http://arxiv.org/abs/2411.04368),
  [Document](https://dx.doi.org/10.48550/arXiv.2411.04368)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [56]
  J. Wei, Z. Sun, S. Papay, S. McKinney, J. Han, I. Fulford, H. W. Chung, A. T. Passos, W. Fedus, and A. Glaese (2025)
  BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents.
   arXiv.
  Note: arXiv:2504.12516 [cs]
  External Links: [Link](http://arxiv.org/abs/2504.12516),
  [Document](https://dx.doi.org/10.48550/arXiv.2504.12516)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [57]
  T. Worledge, T. Hashimoto, and C. Guestrin (2024)
  The Extractive-Abstractive Spectrum: Uncovering Verifiability Trade-offs in LLM Generations.
   arXiv.
  Note: arXiv:2411.17375 [cs]
  External Links: [Link](http://arxiv.org/abs/2411.17375),
  [Document](https://dx.doi.org/10.48550/arXiv.2411.17375)
  Cited by: [§3.3](#S3.SS3.p3.1 "3.3 Verifiability ‣ 3 The DeepScholar Evaluation Framework ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [58]
  J. Wu, W. Yin, Y. Jiang, Z. Wang, Z. Xi, R. Fang, L. Zhang, Y. He, D. Zhou, P. Xie, and F. Huang (2025)
  WebWalker: Benchmarking LLMs in Web Traversal.
   arXiv.
  Note: arXiv:2501.07572 [cs]
  External Links: [Link](http://arxiv.org/abs/2501.07572),
  [Document](https://dx.doi.org/10.48550/arXiv.2501.07572)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [59]
  xAI (2025)
  Grok 3 Beta — The Age of Reasoning Agents | xAI.
  (en).
  External Links: [Link](https://x.ai/news/grok-3)
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [60]
  T. Xu, P. Lu, L. Ye, X. Hu, and P. Liu (2025)
  ResearcherBench: Evaluating Deep AI Research Systems on the Frontiers of Scientific Inquiry.
   arXiv.
  Note: arXiv:2507.16280 [cs]Comment: 22 pages, 3 figures
  External Links: [Link](http://arxiv.org/abs/2507.16280),
  [Document](https://dx.doi.org/10.48550/arXiv.2507.16280)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p1.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [61]
  Z. Yang, P. Qi, S. Zhang, Y. Bengio, W. W. Cohen, R. Salakhutdinov, and C. D. Manning (2018)
  HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering.
   arXiv.
  Note: arXiv:1809.09600 [cs]Comment: EMNLP 2018 long paper. The first three authors contribute equally. Data, code, and blog posts available at https://hotpotqa.github.io/
  External Links: [Link](http://arxiv.org/abs/1809.09600),
  [Document](https://dx.doi.org/10.48550/arXiv.1809.09600)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p3.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [62]
  you.com (2025)
  Su-Sea/ydc-deep-research-evals: you.com’s framework for evaluating deep research systems..
  (en).
  External Links: [Link](https://github.com/Su-Sea/ydc-deep-research-evals)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§6](#S6.p1.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [63]
  H. Zhang, T. Feng, P. Han, and J. You (2024)
  AcademicEval: Live Long-Context LLM Benchmark.
  (en).
  External Links: [Link](https://openreview.net/forum?id=iRYExPKnxm)
  Cited by: [§6](#S6.p2.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [64]
  J. Zhang, Y. Bai, X. Lv, W. Gu, D. Liu, M. Zou, S. Cao, L. Hou, Y. Dong, L. Feng, and J. Li (2024)
  LongCite: Enabling LLMs to Generate Fine-grained Citations in Long-context QA.
   arXiv.
  Note: arXiv:2409.02897 [cs]
  External Links: [Link](http://arxiv.org/abs/2409.02897),
  [Document](https://dx.doi.org/10.48550/arXiv.2409.02897)
  Cited by: [§6](#S6.p2.1 "6 Related Work ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [65]
  Y. Zheng, D. Fu, X. Hu, X. Cai, L. Ye, P. Lu, and P. Liu (2025)
  DeepResearcher: Scaling Deep Research via Reinforcement Learning in Real-world Environments.
  (en).
  External Links: [Link](https://arxiv.org/abs/2504.03160v4)
  Cited by: [§A.2.1](#A1.SS2.SSS1.p1.1 "A.2.1 Open-source Research Systems ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2.1](#A1.SS2.SSS1.p2.1 "A.2.1 Open-source Research Systems ‣ A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§A.2](#A1.SS2.p1.1 "A.2 Overview of Baselines and Experimental Setup ‣ Appendix A Appendix ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§1](#S1.p1.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),
  [§5](#S5.p2.1 "5 Experimental Results ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis").
- [66]
  Y. Zheng, S. Sun, L. Qiu, D. Ru, C. Jiayang, X. Li, J. Lin, B. Wang, Y. Luo, R. Pan, Y. Xu, Q. Min, Z. Zhang, Y. Wang, W. Li, and P. Liu (2024)
  OpenResearcher: Unleashing AI for Accelerated Scientific Research.
  In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: System Demonstrations, D. I. Hernandez Farias, T. Hope, and M. Li (Eds.),
  Miami, Florida, USA, pp. 209–218.
  External Links: [Link](https://aclanthology.org/2024.emnlp-demo.22/),
  [Document](https://dx.doi.org/10.18653/v1/2024.emnlp-demo.22)
  Cited by: [§1](#S1.p3.1 "1 Introduction ‣ DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis"),

## 附录 A 附录

图 3：DeepScholar-bench 数据集模式（schema）。

### A.1 DeepScholar-bench 数据集

我们在图 3 中提供 DeepScholar-bench 数据集的详细概述与模式。此外，表 5 列出了 DeepScholar-June-2025 中收录的论文。

表 5：DeepScholar-June-2025 收录论文的标题与 ArXiv ID。

| # | ArXiv ID | 标题 |
| --- | --- | --- |
| 0 | 2506.02838v1 | TaxAgent: How Large Language Model Designs Fiscal Policy |
| 1 | 2506.02634v1 | KVCache Cache in the Wild: Characterizing and Optimizing KVCache Cache at a Large Cloud Provider |
| 2 | 2506.00958v1 | Speaking Beyond Language: A Large-Scale Multimodal Dataset for Learning Nonverbal Cues from Video-Grounded Dialogues |
| 3 | 2506.00832v1 | Counterfactual Activation Editing for Post-hoc Prosody and Mispronunciation Correction in TTS Models |
| 4 | 2506.00418v1 | Dual Debiasing for Noisy In-Context Learning for Text Generation |
| 5 | 2505.24754v1 | Don't Reinvent the Wheel: Efficient Instruction-Following Text Embedding based on Guided Space Transformation |
| 6 | 2505.24575v1 | NexusSum: Hierarchical LLM Agents for Long-Form Narrative Summarization |
| 7 | 2506.00085v1 | COSMIC: Generalized Refusal Direction Identification in LLM Activations |
| 8 | 2505.23996v1 | Is Your Model Fairly Certain? Uncertainty-Aware Fairness Evaluation for LLMs |
| 9 | 2505.23353v1 | Synthetic Generation and Latent Projection Denoising of Rim Lesions in Multiple Sclerosis |
| 10 | 2505.22757v1 | Pre-Training Curriculum for Multi-Token Prediction in Language Models |
| 11 | 2506.02853v1 | Learning Pyramid-structured Long-range Dependencies for 3D Human Pose Estimation |
| 12 | 2506.02547v1 | Probabilistic Online Event Downsampling |
| 13 | 2506.01071v1 | Aligned Contrastive Loss for Long-Tailed Recognition |
| 14 | 2506.01037v1 | Self-supervised ControlNet with Spatio-Temporal Mamba for Real-world Video Super-resolution |
| 15 | 2506.00434v1 | Efficient 3D Brain Tumor Segmentation with Axial-Coronal-Sagittal Embedding |
| 16 | 2506.00333v1 | Test-time Vocabulary Adaptation for Language-driven Object Detection |
| 17 | 2505.24443v1 | Diversify and Conquer: Open-set Disagreement for Robust Semi-supervised Learning with Outliers |
| 18 | 2505.24334v1 | KairosAD: A SAM-Based Model for Industrial Anomaly Detection on Embedded Devices |
| 19 | 2505.23290v1 | Wav2Sem: Plug-and-Play Audio Semantic Decoupling for 3D Speech-Driven Facial Animation |
| 20 | 2505.23180v1 | Proximal Algorithm Unrolling: Flexible and Efficient Reconstruction Networks for Single-Pixel Imaging |
| 21 | 2505.22616v1 | PS4PRO: Pixel-to-pixel Supervision for Photorealistic Rendering and Optimization |
| 22 | 2505.22458v1 | Universal Domain Adaptation for Semantic Segmentation |
| 23 | 2505.22427v1 | RC-AutoCalib: An End-to-End Radar-Camera Automatic Calibration Network |
| 24 | 2505.22167v1 | Q-VDiT: Towards Accurate Quantization and Distillation of Video-Generation Diffusion Transformers |
| 25 | 2505.22552v1 | ClaimPKG: Enhancing Claim Verification via Pseudo-Subgraph Generation with Lightweight Specialized LLM |
| 26 | 2504.21752v1 | VDDP: Verifiable Distributed Differential Privacy under the Client-Server-Verifier Setup |
| 27 | 2504.21282v1 | Birdie: Natural Language-Driven Table Discovery Using Differentiable Search Index |
| 28 | 2504.17448v1 | CHASe: Client Heterogeneity-Aware Data Selection for Effective Federated Active Learning |
| 29 | 2504.14861v1 | Stitching Inner Product and Euclidean Metrics for Topology-aware Maximum Inner Product Search |
| 30 | 2504.06975v1 | AWDIT: An Optimal Weak Database Isolation Tester |
| 31 | 2506.01833v1 | SPACE: Your Genomic Profile Predictor is a Powerful DNA Foundation Model |
| 32 | 2506.00382v1 | Spectral Insights into Data-Oblivious Critical Layers in Large Language Models |
| 33 | 2506.00205v1 | Unlocking the Power of Rehearsal in Continual Learning: A Theoretical Perspective |
| 34 | 2505.24835v1 | Timing is important: Risk-aware Fund Allocation based on Time-Series Forecasting |
| 35 | 2505.24203v1 | Aligning Protein Conformation Ensemble Generation with Physical Feedback |
| 36 | 2506.02847v1 | CLONE: Customizing LLMs for Efficient Latency-Aware Inference at the Edge |
| 37 | 2505.22194v1 | Refining Datapath for Microscaling ViTs |
| 38 | 2505.11554v1 | Multi-Objective Memory Bandwidth Regulation and Cache Partitioning for Multicore Real-Time Systems |
| 39 | 2505.08071v1 | NMP-PaK: Near-Memory Processing Acceleration of Scalable De Novo Genome Assembly |
| 40 | 2504.06211v1 | Need for zkSpeed: Accelerating HyperPlonk for Zero-Knowledge Proofs |
| 41 | 2504.19283v1 | Efficient Serverless Cold Start: Reducing Library Loading Overhead by Profile-guided Optimization |
| 42 | 2504.11007v1 | Kubernetes in the Cloud vs. Bare Metal: A Comparative Study of Network Costs |
| 43 | 2504.09307v1 | Lumos: Efficient Performance Modeling and Estimation for Large-scale LLM Training |
| 44 | 2506.02750v1 | Learning Binarized Representations with Pseudo-positive Sample Enhancement for Efficient Graph Collaborative Filtering |
| 45 | 2505.23452v1 | What About Emotions? Guiding Fine-Grained Emotion Extraction from Mobile App Reviews |
| 46 | 2505.21811v1 | Revisiting Self-attention for Cross-domain Sequential Recommendation |
| 47 | 2505.20227v1 | Measure Domain's Gap: A Similar Domain Selection Principle for Multi-Domain Recommendation |
| 48 | 2505.19356v1 | Optimized Text Embedding Models and Benchmarks for Amharic Passage Retrieval |
| 49 | 2505.19307v1 | Aligning Web Query Generation with Ranking Objectives via Direct Preference Optimization |
| 50 | 2505.17507v1 | Benchmarking Recommendation, Classification, and Tracing Based on Hugging Face Knowledge Graph |
| 51 | 2505.12791v1 | Unlearning for Federated Online Learning to Rank: A Reproducibility Study |
| 52 | 2505.07166v1 | Pre-training vs. Fine-tuning: A Reproducibility Study on Dense Retrieval Knowledge Acquisition |
| 53 | 2505.03484v1 | STAR-Rec: Making Peace with Length Variance and Pattern Diversity in Sequential Recommendation |
| 54 | 2505.00552v1 | Graph Spectral Filtering with Chebyshev Interpolation for Recommendation |
| 55 | 2504.20458v1 | Search-Based Interaction For Conversation Recommendation via Generative Reward Model Based Simulated User |
| 56 | 2504.18383v1 | Bridge the Domains: Large Language Models Enhanced Cross-domain Sequential Recommendation |
| 57 | 2504.17519v1 | Replication and Exploration of Generative Retrieval over Dynamic Corpora |
| 58 | 2504.15849v1 | NLCTables: A Dataset for Marrying Natural Language Conditions with Table Discovery |
| 59 | 2504.14991v1 | Understanding Accuracy-Fairness Trade-offs in Re-ranking through Elasticity in Economics |
| 60 | 2504.14243v1 | Unconstrained Monotonic Calibration of Predictions in Deep Ranking Systems |
| 61 | 2504.12900v1 | FashionDPO:Fine-tune Fashion Outfit Generation Model using Direct Preference Optimization |
| 62 | 2504.09935v1 | Constrained Auto-Regressive Decoding Constrains Generative Retrieval |

### A.2 基线与实验设置概述

我们简要概述在 DeepScholar-bench 上评测的所有基线系统，包括近期最先进的生成式研究系统以及 DeepScholar-ref。我们评测的开源研究系统包括 DeepResearcher [65]、STORM [43] 与 OpenScholar [6]；搜索智能体分别使用 Llama-4-Scout-17B-16E-Instruct [30]、GPT-4.1-2025-04-14 [34]、o3-2025-04-16 [34]、Claude-opus-4-20250514 [3] 与 Gemini-2.5-pro [14] 模型；另有 OpenAI 的 o3-deep-research [34] 与 DeepScholar-ref。

我们使用 GPT-4.1-2025-04-14 [34] 作为信息点覆盖率的评审，用 GPT-4o-2024-08-06 [34] 作为组织性、相关性比率、参考文献覆盖率、引用精确率与论断覆盖率的评审。组织性得分报告为含平局的胜率，信息点覆盖率报告 strict all 得分，论断覆盖率取窗口大小 $w=1$。对所有检索质量指标，我们把每份给定报告的检索集合视为报告中找到的全部有效 ArXiv 链接。为度量文档重要性，我们用 OpenAlex [35] API 恢复被引信息。每个指标我们报告所有报告上的平均值。

#### A.2.1 开源研究系统

我们评测三个最先进的开源系统：DeepResearcher [65]、STORM [43] 与 OpenScholar [6]。对每个系统，我们用 Llama-4-Scout-17B-16E-Instruct 模型 [30] 运行，并使用 vLLM [22] 以 4 块 A100 GPU 服务。

DeepResearcher [65] 利用训练过的智能体在网络上导航、浏览并综合信息。为训练智能体，该工作使用端到端强化学习训练 Qwen2.5-7B-Instruct [40]。在我们的基准中，我们既用作者发布的训练后模型评估 DeepResearcher，也用 Llama-4-Scout-17B-16E-Instruct 模型 [30] 作为核心 LLM 评估。我们报告两者中表现更好的基线——在我们的实验中是 Llama-4-Scout-17B-16E-Instruct 骨干。

STORM [43] 研究如何应用 LLM 从零开始撰写有依据、有组织的长篇文章（如维基百科文章）。该系统包含一个预写作阶段，通过激发多个智能体之间的对话并利用网络文档来发现关于某主题的多样研究视角。

OpenScholar [6] 构建了一个面向文献综合与科学查询的专用检索增强 LLM 系统。该方法包含一个在预索引 peS2o [44] 语料（截至 2024 年 10 月的 4,500 万篇开放获取学术论文）上训练的检索器，作为使用网络搜索前的初始检索来源。在我们的实验中，我们用该预索引语料评测该系统，并把网络搜索限制为 ArXiv API。

#### A.2.2 搜索智能体

我们评测以下模型：Llama-4-Scout-17B-16E-Instruct [30]、GPT-4.1-2025-04-14 [34]、o3-2025-04-16 [34]、Claude-opus-4-20250514 [3] 与 Gemini-2.5-pro [14]。我们为每个模型加上对 ArXiv [5] 的搜索能力，并使用流行的 ODS 框架 [1] 允许 LLM 对搜索 API 发起工具调用。

#### A.2.3 商业系统

我们对商业生成式研究综合系统的评测聚焦于 OpenAI 的 o3-deep-research [34]，它提供公开 API 以支持我们的评估。

#### A.2.4 DeepScholar-ref

与搜索智能体的评估类似，我们用以下模型评估 DeepScholar-ref：
Llama-4-Scout-17B-16E-Instruct [30]、GPT-4.1-2025-04-14 [34]、o3-2025-04-16 [34]、Claude-opus-4-20250514 [3] 与 Gemini-2.5-pro [14]。对这些基线，我们还使用相同或更弱的模型（Llama-4 或 GPT-4.1）执行语义过滤与 top-k 算子。我们把该方法限制为两轮搜索，每轮最多 2 条查询。

### A.3 额外实验结果

#### A.3.1 元数据统计

我们在表 6 中提供刻画每个被评测方法所生成报告的元数据统计，并在表 7 中提供与评估指标相关的统计。

表 6：报告统计。

| | 报告长度 | | | 引用 | | 成本 | |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | 字符 | 词 | 句 | 不重复文献数 | 行内引用数 | 延迟 (s) | 美元成本 (USD) |
| *人工撰写范例* | | | | | | | |
| 人工撰写范例 | 4381 | 497 | 28 | 23 | 27 | N/A | N/A |
| *开源研究系统* | | | | | | | |
| DeepResearcher (Llama-4) | 2573 | 319 | 35 | 8 | 7 | 31 | 0.00 |
| STORM (Llama-4) | 2766 | 381 | 31 | 18 | 21 | 162 | 0.00 |
| OpenScholar (Llama-4) | 3513 | 483 | 26 | 9 | 19 | 87 | 0.00 |
| *搜索智能体* | | | | | | | |
| Search Agent (Llama-4) | 1968 | 258 | 16 | 9 | 5 | 20 | 0.00 |
| Search Agent (GPT-4.1) | 3168 | 404 | 16 | 10 | 61 | 39 | 0.07 |
| Search Agent (o3) | 3844 | 501 | 24 | 11 | 16 | 263 | 0.15 |
| Search Agent (Claude) | 3977 | 499 | 27 | 13 | 8 | 147 | 1.36 |
| Search Agent (Gemini) | 2810 | 395 | 19 | 6 | 8 | 442 | 0.11 |
| *商业系统* | | | | | | | |
| OpenAI DeepResearch | 6577 | 864 | 74 | 17 | 6 | 630 | 5.02 |
| *DeepScholar 参考流水线* | | | | | | | |
| DeepScholar-ref (Llama-4) | 3499 | 360 | 53 | 19 | 35 | 313 | 0.00 |
| DeepScholar-ref (GPT-4.1) | 7863 | 735 | 115 | 20 | 89 | 234 | 1.66 |
| DeepScholar-ref (GPT-4.1, o3) | 5726 | 617 | 70 | 17 | 42 | 276 | 1.15 |
| DeepScholar-ref (GPT-4.1, Claude) | 5855 | 618 | 72 | 17 | 40 | 334 | 1.23 |
| DeepScholar-ref (GPT-4.1, Gemini) | 5623 | 570 | 86 | 24 | 63 | 349 | 1.29 |

表 7：与评估指标相关的统计。

| | 人工撰写范例上的平均值 | 相关指标 |
| --- | --- | --- |
| 来自 ArXiv.org 的重要参考文献数 | 11.47 | 文献覆盖率 |
| 来自 ArXiv.org 的每条参考文献被引次数中位数 | 647.5 | 文档重要性 |

#### A.3.2 DeepScholar-Nov-2025 上的结果

为研究我们的基准在实时 arXiv API 的领域与时间偏移下如何表现，除 DeepScholar-June-2025（§2，由 63 篇 arXiv 计算机科学论文构建，用于主结果中研究 DeepScholar-bench 的领域覆盖与稳健性）之外，我们实例化了第二个基准切片。

DeepScholar-Nov-2025 包含从超过 75 个不同 arXiv 学科采样的 200 条查询，横跨计算机科学、物理学、定量生物学、经济学与定量金融。我们评估一组高性能系统以检验结论是否稳定：分别以 Llama-4-Scout-17B-16E 与 GPT-4.1+o3 实例化的 DeepScholar-ref，以及以相同模型配置实例化的搜索智能体基线。

表 8 报告全部七项指标的得分。总体而言，我们观察到的模式与 DeepScholar-June-2025 的主结果（表 2）一致。对 DeepScholar-ref 与搜索智能体基线两者，基于 o3 的变体在组织性、信息点覆盖率、相关性比率、引用精确率与论断覆盖率上大幅优于其 Llama-4-Scout 对应版本，而参考文献覆盖率与文档重要性在各基线上仍普遍偏低。这些趋势与主基准切片中的相对排名与定性差距一致，说明我们从 DeepScholar-June-2025 得出的结论可推广到计算机科学以外的查询。

我们强调，DeepScholar-Bench 由自动化数据策划与评估管线定义，而非单一固定数据集。实例化新切片（如 DeepScholar-Nov-2025）只需指定一组查询论文与日期范围；管线随后自动构建相应基准并在同一评估协议下产出得分。这一设计让从业者能轻松创建额外的领域或时间特定评估，同时与我们的核心结果保持可比。

表 8：选定系统在 DeepScholar-Nov-2025（200 条查询、超过 75 个 arXiv 学科）上的性能。我们报告与表 2 相同的指标。

| 模型 | 组织 | 信息点覆盖 | 相关率 | 文献覆盖 | 文档重要性 | 引用精确率 | 论断覆盖 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DeepScholar-ref (Llama-4-Scout) | 0.120 | 0.358 | 0.395 | 0.072 | 0.061 | 0.178 | 0.581 |
| DeepScholar-ref (GPT-4.1 + o3) | 0.578 | 0.479 | 0.568 | 0.087 | 0.054 | 0.563 | 0.578 |
| Search Agent (Llama-4-Scout) | 0.108 | 0.252 | 0.179 | 0.034 | 0.124 | 0.189 | 0.314 |
| Search Agent (o3) | 0.608 | 0.480 | 0.623 | 0.078 | 0.763 | 0.475 | 0.452 |

#### A.3.3 消融研究：理解所选查询的性能影响

我们的主实验用论文摘要作为查询描述 $d$（§3.2）。一个自然的问题是：我们的结论是否依赖于这一特定的查询表述选择？为评估这一点，我们做了一个消融：把摘要替换为两种替代的、真实的用户查询：(i) 论文关键思想的两句话摘要（Key Idea）；(ii) 描述论文主要目标的单个研究问题（RQ）。对每篇论文，我们提示一个 LLM 把摘要转换为这两种替代查询表述。然后我们对每种查询版本重跑完整基准，并为所有主基线计算全部指标的系统级得分。

表 9 报告不同查询表述（行）下各指标（列）系统级得分之间的 Pearson 相关，并用基于置换的配对检验做显著性检验（$p<0.05$）。总体而言，我们观察到跨查询类型的很强一致性：组织性、信息点覆盖率、参考文献覆盖率、文档重要性与论断覆盖率的相关通常高于 0.95，而相关性比率在所有情况下都高于 0.77。Key Idea 与 RQ 之间的所有相关均统计显著，表明更自然、面向用户的查询表述产生高度一致的系统排名。

对查询表述的主要敏感性出现在文档重要性上，其次是引用精确率。文档重要性上的摘要 vs. Key Idea 与摘要 vs. RQ 相关，以及引用精确率上的摘要 vs. Key Idea 相关，虽数值很大（如文档重要性 $r=0.992$）却不统计显著。这提示这两项指标对查询措辞最敏感，可能因为查询的微小变化会改变哪些高被引论文被检索与引用。相比之下，其余指标在所有查询对上表现出高且统计显著的相关。综合来看，这些结果表明我们的基准结论对查询表述的合理变化总体稳健，只是不同查询类型下文档级重要性与引用精确率的表达存在适度敏感性。

表 9：
不同查询表述（摘要、Key Idea、RQ）下系统级得分之间的 Pearson 相关。每项在主基线的得分上计算。标 ∗ 的相关在基于置换的配对检验（阈值 $p<0.05$）下统计显著。

| 查询对 | 组织 | 信息点 | 相关率 | 文献覆盖 | 文档重要性 | 引用精确率 | 论断覆盖 ($w=1$) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 摘要 vs. Key Idea | 0.997∗ | 0.980∗ | 0.979∗ | 0.992∗ | 0.992 | 0.589 | 0.841∗ |
| 摘要 vs. RQ | 0.988∗ | 0.979∗ | 0.772∗ | 0.951∗ | 0.707 | 0.766∗ | 0.877∗ |
| Key Idea vs. RQ | 0.991∗ | 0.983∗ | 0.836∗ | 0.958∗ | 0.766∗ | 0.942∗ | 0.981∗ |

#### A.3.4 人工评估细节

为评估基于 LLM 的指标是否反映人类专家判断，我们进行了 11 位标注者的人工评估——他们均为北美四所研究型大学的计算机科学博士生。总计收集超过 300 条人工标注，旨在评估人类与 LLM 的一致性，以验证我们自动化评估中评估知识综合与检索质量所用的 LLM 评审。下面详述我们的设置。

##### 知识综合。

对组织与连贯性，我们抽样查询，并向标注者展示人工撰写的工作相关章节与一份系统生成的报告。对每一对，标注者指出他们更偏好系统报告、更偏好人工撰写范例，还是认为两者组织相当。这些标签用于评估我们组织性指标背后的两两比较结果。对信息点覆盖率，我们先从人工撰写的工作相关章节生成信息点，然后向标注者展示单个信息点，请其判断每个信息点对理解论文是*关键*（vital）、*可有可无*（okay）还是*无关*（irrelevant）。这些信息点重要性标签决定了计算信息点覆盖率得分时哪些信息点被视为关键。

##### 参考文献覆盖与关键引用。

为了让参考文献覆盖率指标立足于人类判断，我们请每位标注者选择一篇其认可相关工作章节质量的高质量论文。对这篇论文，标注者找出至少六条其认为*重要*的参考文献（即应出现在好的相关工作章节中的文献）与至少六条*不重要*的参考文献（即在不损害章节质量前提下可被省略或替换的文献）。这些标签构成重要与非重要参考文献的金标集合，我们既用它评估参考文献覆盖率，也用它验证我们基于 LLM 的重要性标签。然后，我们在超过 130 条盲评的文献级标注上比较人类多数票标签与 LLM 评审的预测。所得混淆矩阵（行 = 人类标签，列 = LLM 预测）见表 4。

#### A.3.5 基于 LLM 评估的人工验证

表 10：基于 LLM 评估的人工验证

| 评估指标 | LLM 分类标签 | 人类与 LLM 的一致率 |
| --- | --- | --- |
| 组织性 | 两两比较（负 / 平 / 胜） | 78% |
| 信息点覆盖率 | 信息点重要性（关键 / 非关键） | 72% |
| 信息点覆盖率 | 信息点覆盖（支持 / 部分支持 / 不支持） | 70% |
| 检索相关性比率 | 分级相关性（0/1/2） | 70% |
| 参考文献覆盖率 | 参考文献重要性（不重要 / 重要） | 82% |
| 文档重要性 | N/A | N/A |
| 引用精确率 | 蕴含（蕴含 / 不蕴含） | 80% |
| 论断覆盖率 | 蕴含（蕴含 / 不蕴含） | 80% |

我们研究基于 LLM 的评估与人类判断之间的对齐，以评估自动化指标的有效性。总体而言，我们发现我们为 DeepScholar-bench 任务引入的每个指标在基于 LLM 的判断与人类标注之间都表现出高一致。我们收集超过 400 条人工标注，表 10 展示每个自动化指标对应的 LLM 分类任务上人类与 LLM 的一致率。结果表明各项一致率均超过 70%。我们还遵循先前工作 [46] 计算了信息点精确率与 grounded-ness 得分，分别观察到 .83 与 1.0，表明生成的信息点准确且不含幻觉。

#### A.3.6 不同 LLM 评审之间的一致性

为检验评估对 LLM 评审选择的稳健性，我们用三个不同评审重复所有实验：GPT-4o、Llama-4-17b-16e-Instruct 与 DeepSeek-R1-Distill-Qwen-32B。对每一对评审，我们在五个基线（DeepScholar-ref (GPT-4.1, Claude)、DeepScholar-ref (Llama-4)、Search Agent (Claude)、Search Agent (Llama-4) 与 OpenAI DeepResearch）上计算除文档重要性（非基于 LLM）外所有指标的系统级得分之间的 Pearson 相关。然后我们运行基于扰动的置换检验来评估这些相关是否显著大于零。所得相关与显著性标记见表 11。

相关总体非常高（常高于 0.9）。值得注意的是，GPT-4o 与 DeepSeek 在全部指标上都表现出 $p<0.05$ 水平的统计显著相关，说明这两个评审高度一致。多数指标也保持显著相关，但我们观察到对评审选择的主要敏感性在信息点覆盖率上（GPT-4o vs. Llama-4-17b-16e-Instruct 与 DeepSeek-R1-Distill-Qwen-32B vs. Llama-4-17b-16e-Instruct 均不显著）。此外，相关性比率在 GPT-4o vs. Llama-4-17b-16e-Instruct 上、引用精确率在 DeepSeek-R1-Distill-Qwen-32B vs. Llama-4-17b-16e-Instruct 上相关不显著。值得一提的是，即便在这些情况下，相关仍很大（均高于 0.41），说明分歧并不严重。

表 11：
不同 LLM 评审在五个基线上对每个指标产生的系统级得分之间的 Pearson 相关。统计显著性用基于置换的配对 t 检验评估，阈值 $p<0.05$；$p<0.05$ 的相关标 ∗。

| 评审对 | 组织 | 信息点 | 相关率 | 文献覆盖 | 引用精确率 | 论断覆盖 ($w=1$) |
| --- | --- | --- | --- | --- | --- | --- |
| GPT-4o vs. Llama-4 | 0.985∗ | 0.413 | 0.941 | 0.975∗ | 0.817∗ | 0.958∗ |
| GPT-4o vs. DeepSeek | 0.966∗ | 0.920∗ | 0.980∗ | 0.990∗ | 0.843∗ | 0.996∗ |
| DeepSeek vs. Llama-4 | 0.991∗ | 0.668 | 0.942∗ | 0.994∗ | 0.986 | 0.963∗ |

### A.4 评估细节

这里我们提供 DeepScholar-Bench 所用评估指标的详细实现与提示词。此外我们还对不同的指标做一些消融研究。

- 知识综合——组织性：框 A.4.3 展示用于比较系统生成报告与人工撰写范例的提示词，得到每个系统基于组织与连贯性的胜率。
- 知识综合——信息点覆盖率：对该指标，我们遵循先前工作 [39] 的基于信息点的评估提示词——从范例中提取关键事实并检查其在生成报告中的存在性。
- 检索质量——文档重要性：我们用图 5 所示的 LOTUS 程序选择重要参考文献。
- 检索质量——相关性比率：遵循相关性的 Cranfield 模型，我们在框 A.4.3 中提示模型为每个检索来源分配分级相关性分数（0–2）。
- 可验证性——引用精确率与论断覆盖率：遵循先前工作 [11, 26]，我们用框 A.4.3 所示提示词检查论断相对被引来源的蕴含，如 §3.3 所述。

我们指出，参考文献覆盖率与文档重要性按 §3.2 所述以确定性方式计算：前者通过把检索集合与人工撰写范例中的重要参考文献比较，后者通过对参考文献的被引次数做归一化。

#### A.4.1 参考文献覆盖率

图 4：DeepScholar-Bench 中的引用重要性分解。每根柱对应一节人工范例相关工作章节，按总被引数排序。柱子的颜色编码表示*重要的 ArXiv 引用*（红色）、*重要的非 ArXiv 引用*（橙色）与*非关键引用*（蓝色）。

图 4 展示 DeepScholar-Bench 中人工范例报告间重要引用的分布。对每份范例，我们用图 5 所示的 LOTUS 程序识别哪些引用是*重要*的、因而是高质量相关工作章节必须包含的。然后我们把这些重要引用分为两组：出现在 ArXiv 上的（红色）与不在 ArXiv 上的（橙色）。每根柱的蓝色部分对应由同一基于 LOTUS 的流程判定的*非关键*引用。

该图突出两个一致趋势。第一，许多范例相关工作章节包含大量非关键引用。这类文献可能对叙事流畅性或更广的背景有用，但并非不可或缺。非关键引用带有一定主观性，取决于作者如何铺陈论文的故事。相比之下，重要引用代表「必备」文献，即定位该贡献所必需的领域基础性工作。第二，我们观察到红色部分（重要的 ArXiv 引用）在各范例间分布良好，说明 ArXiv 是找回许多关键文献的可靠且足够宽泛的来源。

```python
query_in = "Carefully read the {title}, {abstract} and {related_work_section} of an academic paper. \
 Then consider the cited paper in question, given the title {cited_paper_title}, the {cited_paper_authors} and a snippet of its content, {cited_paper_content}.\
 Is the cited paper in question an essential reference?\
 An essential reference reflects a key, notable prior work that provides key information, which a good related works section for this paper must include.\
 A non-essential reference is one that is not essential to the related work section of this paper and could be omitted or substituted with a different reference.\
 a non-essential reference may be a relevant reference that reflects an important topic area, but the particular reference could be omitted or substituted with a different related work.\
 Alternatively, a non-essential reference may be a tangential reference, an unimportant reference.\a non-essential reference may be a relevant reference that reflects an important topic area, but the particular reference could be omitted or substituted with a different related work."

res = citations_df.sem_filter(query_in, return_all=True, strategy=lotus.types.ReasoningStrategy.ZS_COT)
```

图 5：寻找重要参考文献的 LOTUS 程序

#### A.4.2 可验证性消融研究

在正文（§3.3）中，我们报告可验证性指标时使用大小 $w=1$ 的滑动窗口计算论断覆盖率。即对每个论断句，若同句或前后一句内的任一参考文献充分支持该论断，则视该引用有效。这里我们扩展分析，研究不同窗口大小的影响。具体而言，我们报告窗口大小从 $w=0$（仅同句）到 $w=5$（前后五句）时不同系统取得的引用覆盖率。

如图 6 所示，增大窗口大小在所有基线上一致地提升引用覆盖率。这是预期的：窗口越大，论断 $[-w,+w]$ 邻域内的被引文献之一提供充分支持的概率越高。不过我们也注意到，过大的窗口在实践中并不理想，因为那往往意味着文献离其要支持的论断很远，降低可读性，也使读者更难验证论断与引用之间的关联。此外，从表 6 可见，真实学术写作往往引用密集，人工范例中平均每句至少一条引用。总体而言，消融结果突出了更严格精确率（$w=0$）与更宽松的召回导向设定（$w\geq 1$）之间的权衡。

图 6：不同窗口大小下引用覆盖率的消融研究。
对每个论断，我们度量 $[-w,+w]$ 句滑动窗口内是否有任何引用支持它。

#### A.4.3 人工范例间的文档重要性

在本节中，我们以 DeepScholar-Bench 中人工撰写范例内参考文献的被引次数度量，展示文档重要性的分布。图 7 给出两幅直方图：(a) 全部参考文献的被引次数分布；(b) 限定为出现在 ArXiv 上的参考文献的分布。我们绘制被引次数的对数，数值来自 OpenAlex API [35]——一个开放且广泛使用的学术数据库，提供文献级元数据。虽然 OpenAlex 的被引数未必与 Google Scholar 等其他来源完全一致，但相对计数是一致的，使其成为可靠的开源替代。

如图 7 所示，分布因少数被引数极高的论文（如超过 1 万次被引）而高度偏斜。这些离群值抬高了均值，使平均值相对典型文献偏高（全部文献平均 478.3 次被引，仅 ArXiv 文献 647.6 次）。相比之下，中位数更低（全部文献 31，仅 ArXiv 文献 36）。这一偏斜凸显了用被引数作为重要性代理的挑战，因为不同人工撰写范例之间参考文献的被引次数中位数方差很大。

图 7：人工撰写范例中参考文献的被引次数（文档重要性）分布。
图 (a) 为全部文献，图 (b) 限定为 ArXiv 文献。
被引次数以对数尺度绘制。

**框 1：知识综合——组织性的提示词**

You are an intelligent, rigorous, and fair evaluator of scholarly writing quality and relevance.
You will receive the title and abstract of a research paper, together with two candidate related-work sections (A and B) written for that paper.
Do not consider the formatting of the text (e.g., LaTeX, markdown, etc.). Only consider the content.

Task: Decide which section—A or B—exhibits better organization and coherence.
How to judge (organization only)
Ignore breadth of coverage, citation accuracy, and analytic depth. Assess:
Logical structure – Clear introduction, grouping of related themes, and smooth progression of ideas.
Paragraph cohesion – Each paragraph develops a single topic and flows naturally to the next.
Clarity & readability – Minimal redundancy or contradictions; transitions guide the reader.
Signposting – Helpful headings, topic sentences, or discourse markers (if provided).

Pick the section that is easier to follow and better structured—no ties.

### Paper under assessment:
[TITLE + ABSTRACT GO HERE]
### Candidate related-work section A
[RELATED WORK A TEXT GOES HERE]
### Candidate related-work section B
[RELATED WORK B TEXT GOES HERE]

Output your answer as a JSON dictionary in the following format:
{"decision": "A" or "B", "explanation": "One sentence clearly explaining the key differences between the two options and why the selected one is preferred."}
Only output the dictionary, do not output any other text.

**框 2：参考文献相关性判断的提示词**

You are an intelligent, rigorous, and fair evaluator of scholarly writing quality and citation relevance.
You will receive the title and abstract of a research paper under assessment, the ground-truth related-work section written by human experts, and the title and abstract of a candidate reference paper.
Do not consider formatting (e.g., LaTeX, markdown, etc.). Only consider the content.

Task: Determine whether the candidate reference paper is relevant to the related-work section.
How to judge
• Consider the main research topic and themes described in the related-work section.

• If the reference discusses similar ideas, prior work, or background, mark it as relevant (1).

• If the reference is off-topic or unrelated in scope, mark it as not relevant (0).

• Remember: You are only seeing the title and abstract of the reference, so the full content might be more relevant than it appears.

### Paper under assessment:
[PAPER TITLE GOES HERE]
[PAPER ABSTRACT GOES HERE]
### Ground-truth related-work section:
[RELATED WORK TEXT GOES HERE]
### Candidate reference paper:
[REFERENCE TITLE GOES HERE]
[REFERENCE ABSTRACT GOES HERE]

Return only the score in this format:

### final score: <0 or 1>

**框 3：归因验证的提示词**

You are an intelligent and fair evaluator.
Your task is to verify whether a given reference can support the provided claim.

Task:
Given a claim and its associated set of references, determine whether the references sufficiently support all aspects of the claim.
### CLAIM:
[CLAIM TEXT GOES HERE]
### REFERENCES:
[REFERENCE TEXT GOES HERE]

Judgment Criteria:
• If the references support the claim, return 1.

• If the references do not support the claim, return 0.

• Do not explain your answer or include any additional commentary.

Output Format:

Answer: 1  or  Answer: 0

### A.5 基线的扩展描述

我们提供每个被评测方法的扩展描述，包括相关实现细节与评估所用参数。

#### A.5.1 DeepResearcher

DeepResearcher 流水线遵循一个为迭代式网络信息检索设计的结构化工具增强推理框架。该系统要求在任何工具调用之前进行显式推理，推理封装在 <think> 标签中以确保可解释性与可控性。推理之后，模型生成一个 JSON 格式的请求，指定「web search」工具及其查询。这些查询通过 Lotus Search API 执行——我们将其替换为 ArXiv 专用搜索接口，以为评估提供受控的检索 API。检索结果以包含标题、URL 与片段的结构化格式返回，并存储在内存中供后续推理步骤引用。这一迭代过程持续进行，直到模型判定已收集足够证据，随后产出综合的最终回答。

在我们的实验中，我们使用 Llama-4-Scout-17B-16E-Instruct 作为基座模型，替换最初提出的 DeepResearcher-7b，因为后者在我们的实验中检索增强推理表现始终更好（译注：原文如此）。我们对提示词略作修改以对齐 Llama-4 提示风格，详见框 A.5.1。检索深度设为每条查询 10 个来源——系统的默认值，在覆盖与效率之间提供平衡的折中。我们按照 DeepResearcher 默认将每条查询限制为单次 rollout、最多 10 步；这一上限很宽松，因为多数 rollout 在三步内收敛，但它确保系统对更复杂的查询有余量。默认网络搜索 API 被替换为 ArXiv 搜索以符合我们的基准设置。

**框 4：为配合 Llama-4-Scout-17B-16E-Instruct 优化修改后的 DeepResearcher 系统提示词**

## Background information
* Today is `{strftime("%Y-%m-%d", gmtime())}`
* You are Deep AI Research Assistant
The question I give you is a complex question that requires a *deep research* to answer.
I will provide you with two tools to help you answer the question:
* A web search tool to help you perform google search. Tool call format:

```
{{"name": "web_search",
"arguments": {{"query": ["<query1>","<query2>","<query3>"]}}}}
```

* A webpage browsing tool to help you get new page content. Tool call format:

```
{{"name": "browse_webpage",
"arguments": {{"url_list": ["<url1>","<url2>","<url3>"]}}}}
```

You don't have to answer the question now, but you should first think about the research plan or what to search next.
Your output format should be one of the following two formats:

```
<think>
YOUR THINKING PROCESS
</think>
<answer>
YOUR ANSWER AFTER GETTING ENOUGH INFORMATION
</answer>
```

or

```
<think>
YOUR THINKING PROCESS
</think>
<tool_call>
YOUR TOOL CALL WITH CORRECT FORMAT
</tool_call>
```

You should always follow the above two formats strictly. You will be heavily penalized if you do not follow the format strictly.
Only output the final answer (in words, numbers or phrase) inside the <answer></answer> tag, without any explanations or extra information. If this is a yes-or-no question, you should only answer yes or no.

#### A.5.2 OpenScholar

OpenScholar 流水线遵循四个阶段：初始检索、回复与反馈生成、迭代精炼，以及引用验证。第一阶段用 contriever 模型从固定索引检索文本段——该模型编码文本并基于语义相似性检索段落。这些段落被重排并用于生成初始草稿回复，引用与支持段落对齐。第二阶段引入反馈生成：模型产出最多三条反馈陈述，指出草稿的潜在改进点（如内容缺失或组织问题）；若需要更多证据则发出检索查询。第三阶段以先前的草稿、检索到的段落与新加入的证据为条件迭代精炼回复，每步产出更好的回复，直到反馈被完全吸收。最后，引用验证确保所有值得引用的陈述都被检索来源充分支撑，必要时插入额外引用而不删除内容。

为与其他基线一致，我们使用 Llama-4-Scout-17B-16E-Instruct 模型做生成。检索管线先用默认的 pes2o_contriever¹ 模型从 peS2o_v3 收集 100 个文本段。所用的重排器为 OpenScholar_Reranker²，同样保持默认设置。为在各基线间对齐参数化，我们把生成所用来源数（top_n）从 10 提高到 30。此外，默认搜索 API 被替换为 arXiv API，以为我们的实验提供受控的检索语料与 API。

**脚注 1：<https://huggingface.co/akariasai/pes2o_contriever>**

**脚注 2：<https://huggingface.co/OpenSciLM/OpenScholar_Reranker>**

#### A.5.3 搜索智能体

搜索智能体用各 LLM API 加搜索 API 访问实现。我们实现了一个 ReAct 智能体，从 smolagents.ToolCallingAgent 实例化，系统提示词基于为深度网络搜索与检索设计的开源 OpenDeepSearch（ODS）框架，并把搜索智能体作为外部工具。在每个推理步，ReAct 智能体既可以通过 web_search 动作调用搜索智能体，也可以决定产出 final_answer。搜索智能体与搜索 API 交互，针对查询取回相关学术文章，随后由一个 LLM 生成检索内容的简明摘要。为与基准设置保持一致，标准搜索 API 被替换为 arXiv API。常规搜索智能体在处理完整摘要查询时会失败，因此我们采用基于 ReAct 的智能体——它生成更短、更有效的可搜索查询。该智能体跨轮次跟踪检索结果，允许在推理过程中引用过去的证据。最多 5 次迭代后，智能体被迫给出最终回复，确保计算步骤有界。

对搜索智能体的参数化，我们把搜索智能体设为每条查询取回 30 个结果——比默认值更宽松，以与其他基线建立公平可比性。最大迭代上限固定为 5，与 ODS 框架的默认设置一致，在不至于过度搜索深度的前提下提供充分探索。ReAct 提示词被略作修改以适配 ArXiv 搜索 API 的具体使用，如框 A.5.3 所示。

**框 5：修改后的 ODS ReAct 智能体提示词（仅网络搜索工具调用）**

You are an expert assistant who can solve any task using tool calls. You will be given a task to solve as best you can.
To do so, you have been given access to some tools. Never use facts without verification and only cite the sources returned by the tool.
The tool call you write is an action: after the tool is executed, you will get the result of the tool call as an "observation".
This Action/Observation can repeat N times, you should take several steps when needed.
You can use the result of the previous action as input for the next action.
The observation will always be a string containing the search results.
To provide the final answer to the task, use an action blob with "name": "final_answer" tool. It is the only way to complete the task, else you will be stuck on a loop. So your final output should look like this:
Action:

```
{
  "name": "final_answer",
  "arguments": {"answer": "insert your final answer here"}
}
```

Here are a few examples using notional tools:

```
---
Task: "What historical event happened closest in time to the invention
of the telephone: the American Civil War or the establishment of the
Eiffel Tower?"
Action:
{
  "name": "web_search",
  "arguments": {"query": "year of telephone invention"}
}
Observation: "The telephone was invented in 1876."
Action:
{
  "name": "web_search",
  "arguments": {"query": "year American Civil War ended"}
}
Observation: "The American Civil War ended in 1865."
Action:
{
  "name": "web_search",
  "arguments": {"query": "year Eiffel Tower established"}
}
Observation: "The Eiffel Tower was completed in 1889."
Action:
{
  "name": "final_answer",
  "arguments": {"answer": "The historical event closest in time to the
  invention of the telephone is the end of the American
   Civil War (11 years apart)."}
}
---
Task: "Which country has a higher population density: Japan or India?"
Action:
{
  "name": "web_search",
  "arguments": {"query": "population and area of Japan"}
}
Observation: "Japan has a population of 125 million and an area of
377,975 square kilometers."
Action:
{
  "name": "web_search",
  "arguments": {"query": "population and area of India"}
}
```

**框 6：ODS 提示词（续）**

```
Observation: "India has a population of 1.38 billion and an area of
3,287,263 square kilometers."
Action:
{
  "name": "final_answer",
  "arguments": {"answer": "India has a higher population density
  (419.6 people/km2) than Japan (330.7 people/km2)."}
}
---
Task: "Which country hosted the first FIFA World Cup, and in what
year?"

Action:
{
  "name": "web_search",
  "arguments": {"query": "country hosted first FIFA World Cup"}
}
Observation: "Uruguay hosted the first FIFA World Cup."

Action:
{
  "name": "web_search",
  "arguments": {"query": "year of first FIFA World Cup"}
}
Observation: "The first FIFA World Cup was held in
1930."

Action:
{
  "name": "final_answer",
  "arguments": {"answer": "Uruguay hosted the first FIFA World Cup
  in 1930."}
}

---
Task: "Who invented the light bulb, and what company did he
later establish?"

Action:
{
  "name": "web_search",
  "arguments": {"query": "inventor of the light bulb"}
}
Observation: "Thomas Edison invented the light bulb."

Action:
{
  "name": "web_search",
  "arguments": {"query": "company founded by Thomas Edison"}
}
Observation: "Thomas Edison founded General Electric."

Action:
{
  "name": "final_answer",
  "arguments": {"answer": "Thomas Edison invented the light bulb and
  later established General Electric."}
}
---
```

**框 7：ODS 提示词（续）**

```
Task: "Which Shakespeare play contains the line \"All the world's
a stage,\" and how many years ago was it first performed if
today is 2024?"

Action:
{
  "name": "web_search",
  "arguments": {"query": "Shakespeare play All the world's a stage"}
}
Observation: "The line is from \"As You Like It.\""

Action:
{
  "name": "web_search",
  "arguments": {"query": "year As You Like It first performed"}
}
Observation: "\"As You Like It\" was first performed in 1603."
Action:
{
  "name": "calculate",
  "arguments": {"expression": "2024 - 1603"}
}
Observation: "421 years."

Action:
{
  "name": "final_answer",
  "arguments": {"answer": "\"As You Like It\" contains the line \"All
  the world's a stage\" and was first performed 421 years ago
  in 1603."}
}
```

Above examples were using notional tools that might not exist for you. You only have access to these tools:

```
{%- for tool in tools.values() %}
- {{ tool.name }}: {{ tool.description }}
    Takes inputs: {{tool.inputs}}
    Returns an output of type: {{tool.output_type}}
{%- endfor %}

{%- if managed_agents and managed_agents.values() | list %}
```

Here are the rules you should always follow to solve your task:
1. ALWAYS provide a tool call, else you will fail.
2. Always use the right arguments for the tools. Never use variable names as the action arguments, use the value instead.
3. Call a tool only when needed: do not call the search agent if you do not need information, try to solve the task yourself.
If no tool call is needed, use final_answer tool to return your answer.
4. Never re-do a tool call that you previously did with the exact same parameters.
5. Always cite sources using [X] format where X is the citation number.
6. Place citations immediately after the sentence or paragraph they are referencing.
7. Make sure to provide citations whenever using information from the source material.
8. Cite as many sources as possible.
9. Create a reference section at the end of your final answer.
Now Begin! If you solve the task correctly, you will receive a reward of $1,000,000.

#### A.5.4 STORM

STORM 流水线遵循结构化的多阶段过程，从给定主题生成全面的维基百科式文章。首先检索相关维基百科文章并聚类其目录以识别候选视角，作为探索的锚点。随后是模拟多轮对话：一个 LLM 同时扮演提问与回答角色，向检索模块查询并综合有依据的回答。与此并行，模型在草稿大纲生成阶段纯凭参数化知识生成初始大纲。然后通过用检索证据与对话输出来落地而精炼大纲。最后一步，每个章节都基于参数化知识与检索参考文献以显式行内引用起草。所有章节拼接形成最终结果。

参数设置方面，我们在尽可能之处使用 STORM 的默认配置以保真于其设计：每视角最多 3 轮、3 个视角、每轮最多 3 条搜索查询。搜索上，我们考虑每条查询的前 15 个结果，确保合理广度而不压垮管线。为使 STORM 与其他基线可比，我们把每个章节标题收集的参考文献数提高到 30（比默认更宽松），因为这允许起草时整合更丰富的证据。重要的是，我们把原始搜索 API 替换为 arXiv 搜索，以为基准设置控制检索 API。最后，我们使用 Llama-4-Scout-17B-16E-Instruct 作为基座模型。

#### A.5.5 OpenAI 的 DeepResearch

我们使用基于 o3-deep-research³ 模型的 OpenAI DeepResearch 系统，配一个自定义 MCP 以只搜索 ArXiv 且每条查询返回 $n=30$ 个结果。为防止模型取到给定论文上传之后的搜索结果，该 MCP 用一个自定义端点设置其应检索的最晚日期。其余设置均为默认值。

**脚注 3：<https://platform.openai.com/docs/models/o3-deep-research>**

### A.6 DeepScholar-ref 细节与配置

DeepScholar-base 通过三个主要阶段运作：检索、过滤与最终生成（图 2）。

**检索**
：   在这一阶段，一个 LLM 以输入摘要与先前检索的摘要为条件生成 $Q$ 条搜索查询。每条查询提交给配置的搜索 API（ArXiv、tavily 等），在指定日期范围内取回至多 $search\_K$ 篇相关论文。这一步所用代码与提示词分别见图 8 与框 A.7。该过程重复 $N$ 次。

```python
from lotus import web_search

class Query(BaseModel):
    queries: list[str]

# Generate the Queries
queries = get_completion(
    lm,
    query_generation_instruction.format(number_of_queries=num_queries),
    f"Topic: {topic}, Background: {background}",
    response_format=Query,
).queries

# Search. corpus = ArXiv/Tavily etc.
paper_dfs = []
for query in queries:
    paper_dfs.append(web_search(corpus, query, search_K))

papers = pd.concat(paper_dfs)
```

    图 8：检索阶段：查询生成与批量搜索。

**过滤**
：   检索结果用 LOTUS 的两个语义算子 [37, 28] 精炼：Sem-Filter 与 Sem-TopK，二者共同选出最相关的 top $K$ 篇论文。代码见图 9。

```python
instruction = (
    "given the article's abstract: {snippet}, "
    "is the article relevant to the specific interests in the user's query: {user_query}."
)

res_df = docs_df.sem_filter(
    instruction.format(user_query=topic, snippet="{snippet}"),
    strategy="cot"
)

res_df = res_df.sem_topk(
    instruction.format(user_query=topic, snippet="{snippet}"),
    strategy="cot", k=K,
)
```

    图 9：DeepScholar-ref 过滤步骤的 Sem-Filter 与 Sem-TopK 代码

**最终生成**
：   然后通过一个 Sem-Agg 查询聚合过滤后的论文集合以产生最终输出。这一步的相应代码见图 10，提示词见框 A.7。

```python
agg_instruction = section_writer_instructions.format(
    topic=topic,
    section_instructions=section_instructions,
    existing_content=existing_content,
    context="{context}",
)

res: pd.DataFrame = res_df.sem_agg(
    agg_instruction, suffix="summary", group_by=group_by
)
```

    图 10：DeepScholar-ref 最终生成中的 Sem-Agg

除非另有说明，流水线参数设为 $Q=2$、$search\_K=50$、$N=2$ 与 $K=30$。

### A.7 生成报告示例

我们提供各系统对数据集中论文 0（即表 5 中的『TaxAgent: How Large Language Model Designs Fiscal Policy』，ArXiv ID 2506.02838）生成的报告示例。图 11–15 分别展示 DeepScholar-ref、搜索智能体、DeepResearcher、OpenScholar 与 STORM 生成的报告，均使用 Llama-4。

## Related Works

Economic inequality is a pressing global issue, affecting education, healthcare, and social stability. Traditional taxation systems, such as the U.S. federal income tax, aim to reduce inequality but often lack adaptability [[Stephan Zheng' 2020-04-28](http://arxiv.org/abs/2004.13332v1)]. The Saez Optimal Taxation model is a notable attempt to create a dynamic system, but it does not account for taxpayer heterogeneity and irrational behavior [[Stephan Zheng' 2020-04-28](http://arxiv.org/abs/2004.13332v1)].

Recent studies have explored various approaches to optimize taxation and address economic inequality. For instance, the AI Economist framework uses two-level deep reinforcement learning to discover tax policies that balance economic equality and productivity [[Stephan Zheng' 2021-08-05](http://arxiv.org/abs/2108.02755v1)]. This approach has shown promising results in improving the trade-off between equality and productivity.

Agent-based modeling (ABM) has also been employed to study the effects of taxation on economic systems. For example, PolicySpace is a modeling platform that uses ABM to simulate public policies within an empirical, spatial environment [[Bernardo Alves Furtado' 2017-12-31](http://arxiv.org/abs/1801.00259v1)]. This platform has been applied to study the impact of tax transfer rules on cities' quality of life.

The use of machine learning and artificial intelligence in taxation is a growing area of research. TaxAI, a dynamic economic simulator, uses multi-agent reinforcement learning to benchmark tax policies [[Qirui Mi' 2023-09-28](http://arxiv.org/abs/2309.16307v2)]. This simulator has demonstrated the effectiveness of machine learning algorithms in optimizing tax policies.

Large language models (LLMs) have also been integrated with ABM to study complex economic systems. For instance, the TaxThemis system uses interactive visual analytics to help tax officers identify suspicious tax evasion groups [[Yating Lin' 2020-09-07](http://arxiv.org/abs/2009.03179v1)]. This system demonstrates the potential of LLMs in analyzing and detecting tax evasion behaviors.

Optimal taxation theory has also been explored in various studies. For example, the Domar-Musgrave effect explains cases where it is optimal to tax capital income [[Brendan K. Beare' 2023-11-10](http://arxiv.org/abs/2311.05822v2)]. Other studies have investigated the impact of tax evasion on economic systems [[M. L. Bertotti' 2016-02-18](http://arxiv.org/abs/1602.08467v1)][[Frank Westerhoff' 2008-05-07](http://arxiv.org/abs/0805.0998v1)].

Our work builds upon these studies by introducing TaxAgent, a novel integration of LLMs with ABM to design adaptive tax policies. TaxAgent simulates real-world taxpayer behaviors using heterogeneous H-Agents and optimizes tax rates using LLMs to balance equity and productivity [[Stephan Zheng' 2020-04-28](http://arxiv.org/abs/2004.13332v1)].

## References

1. [[Bernardo Alves Furtado' 2017-12-31](http://arxiv.org/abs/1801.00259v1)]

2. [[Emma Hubert' 2020-09-01](http://arxiv.org/abs/2009.00484v2)]

3. [[Stephan Zheng' 2020-04-28](http://arxiv.org/abs/2004.13332v1)]

4. [[Kelly Geyskens' 2018-10-16](http://arxiv.org/abs/1810.07243v1)]

5. [[M. L. Bertotti' 2016-12-19](http://arxiv.org/abs/1701.02662v1)]

6. [[Qirui Mi' 2023-09-28](http://arxiv.org/abs/2309.16307v2)]

7. [[Stephan Zheng' 2021-08-05](http://arxiv.org/abs/2108.02755v1)]

8. [[Xuyang Chen' 2024-09-09](http://arxiv.org/abs/2409.05397v1)]

9. [[Teddy Lazebnik' 2025-01-30](http://arxiv.org/abs/2501.18177v1)]

10. [[Stefan Steinerberger' 2019-04-30](http://arxiv.org/abs/1904.13276v1)]

11. [[Ozan Candogan' 2023-12-10](http://arxiv.org/abs/2312.05996v1)]

12. [[Nikolaos D. Goumagias' 2018-01-29](http://arxiv.org/abs/1801.09466v1)]

13. [[George Abuselidze' 2021-08-06](http://arxiv.org/abs/2108.03027v1)]

14. [[Padma Sharma' 2022-08-08](http://arxiv.org/abs/2208.03908v2)]

15. [[Alex A. T. Rathke' 2022-02-28](http://arxiv.org/abs/2202.13695v1)]

16. [[Felix Kuebler' 2022-10-17](http://arxiv.org/abs/2210.09066v1)]

17. [[Chen Xu' 2024-04-27](http://arxiv.org/abs/2404.17826v1)]

18. [[Maria Letizia Bertotti' 2012-07-05](http://arxiv.org/abs/1207.6081v2)]

19. [[Job Boerma' 2022-04-28](http://arxiv.org/abs/2204.13481v2)]

20. [[Xintong Wang' 2022-03-25](http://arxiv.org/abs/2203.13395v2)]

21. [[Jialin Dong' 2023-11-28](http://arxiv.org/abs/2311.17252v1)]

22. [[M. L. Bertotti' 2016-02-18](http://arxiv.org/abs/1602.08467v1)]

23. [[Yating Lin' 2020-09-07](http://arxiv.org/abs/2009.03179v1)]

24. [[Marinho Bertanha' 2021-01-04](http://arxiv.org/abs/2101.01170v3)]

25. [[Marco Alberto Javarone' 2016-05-27](http://arxiv.org/abs/1605.08690v1)]

26. [[Brendan K. Beare' 2023-11-10](http://arxiv.org/abs/2311.05822v2)]

27. [[Johannes Kasinger' 2024-09-02](http://arxiv.org/abs/2409.01493v1)]

28. [[Frank Westerhoff' 2008-05-07](http://arxiv.org/abs/0805.0998v1)]

29. [[Yuan Liang' 2022-07-05](http://arxiv.org/abs/2207.01793v3)]

30. [[Jose Ricardo Bezerra Nogueira' 2021-09-01](http://arxiv.org/abs/2109.00297v2)]

图 11：DeepScholar-ref 为论文『TaxAgent: How Large Language Model Designs Fiscal Policy』生成的报告示例。

## Related Works

Economic inequality and taxation are complex issues that have been explored using various models and simulations. Research has shown that large language models (LLMs) can be used to analyze the impact of taxation on inequality [1]. For instance, a study introduced a benchmark called PLAT to assess the ability of LLMs to predict the legitimacy of additional tax penalties [1].

Agent-based modeling has also been used to study the effects of taxation on wealth distribution. A model suggested that oligarchs will emerge when wealth taxation is below a certain threshold [2]. Another study found that taxation of income and capital gains alone cannot prevent the emergence of oligarchs [2].

The relationship between economic inequality and mobility has also been explored using kinetic models. Research found a negative correlation between economic inequality and mobility [3]. Furthermore, a study used a multi-LLM-agent-based framework to simulate policy impacts across heterogeneous agents, offering a new direction for economic and public policy analysis [4].

Optimal taxation models have also been developed, including the Saez Optimal Taxation model, which adjusts dynamically but fails to address taxpayer heterogeneity and irrational behavior [5]. In contrast, our study introduces TaxAgent, a novel integration of LLMs with agent-based modeling to design adaptive tax policies that balance equity and productivity.

Our approach builds upon existing research in taxation and inequality, leveraging the strengths of LLMs and agent-based modeling to simulate real-world taxpayer behaviors and optimize tax rates. Benchmarked against Saez Optimal Taxation, U.S. federal income taxes, and free markets, TaxAgent achieves superior equity-efficiency trade-offs.

## References

[1] [Taxation Perspectives from Large Language Models: A Case Study on Additional Tax Penalties](http://arxiv.org/abs/2503.03444v1)

[2] [ODE models of wealth concentration and taxation](http://arxiv.org/abs/2308.01500v1)

[3] [Economic inequality and mobility in kinetic models for social sciences](http://arxiv.org/abs/1504.03232v1)

[4] [A Multi-LLM-Agent-Based Framework for Economic and Public Policy Analysis](http://arxiv.org/abs/2502.16879v1)

[5] [Optimal taxation and the Domar-Musgrave effect](http://arxiv.org/abs/2311.05822v2)

图 12：搜索智能体为论文『TaxAgent: How Large Language Model Designs Fiscal Policy』生成的报告示例。

## Related Works

Economic inequality and taxation are critical issues in modern economies, with traditional systems like the U.S. federal income tax aiming to reduce inequality but often lacking adaptability [2311.05822v2]. The Saez Optimal Taxation model is a notable approach that adjusts dynamically but fails to account for taxpayer heterogeneity and irrational behavior [2312.05996v1].

Agent-based modeling (ABM) has been used to study economic systems and policy impacts, providing insights into the interactions between heterogeneous agents and their effects on macroeconomic variables [1702.02763v1][1701.06625v1]. For instance, ABM has been applied to model the impact of taxation on economic growth and inequality [1508.00275v2].

The integration of large language models (LLMs) with ABM is a nascent but promising area of research. LLMs have shown potential in economic policy analysis by simulating human-like reasoning and behavior [2502.16879v1]. They can be used to model subrational agent behaviors, such as myopic decision-making or risk aversion, which are characteristic of human economic agents [2402.08755v1].

Recent studies have explored the use of LLMs in market experiments, demonstrating their ability to simulate competitive market behavior but also highlighting their current limitations in replicating dynamic decision-making processes [2409.08357v2]. The application of LLMs in economic policy analysis offers a new direction for understanding policy impacts across heterogeneous agents [2505.21371v1].

Our work builds on these advances, introducing TaxAgent, a novel integration of LLMs with ABM to design adaptive tax policies that balance equity and productivity. By leveraging the strengths of both approaches, TaxAgent offers a scalable and data-driven framework for fiscal policy evaluation.

## References

1. [2311.05822v2] - Optimal taxation and the Domar-Musgrave effect

2. [2312.05996v1] - Achieving Fairness and Accuracy in Regressive Property Taxation

3. [2502.16879v1] - A Multi-LLM-Agent-Based Framework for Economic and Public Policy Analysis

4. [2409.08357v2] - An Experimental Study of Competitive Market Behavior Through LLMs

5. [2402.08755v1] - LLM-driven Imitation of Subrational Behavior : Illusion or Reality?

6. [2505.21371v1] - When Experimental Economics Meets Large Language Models: Tactics with Evidence

7. [1611.02547v2] - Optimal Extraction and Taxation of Strategic Natural Resources: A Differential Game Approach

8. [1508.00275v2] - On growth-optimal tax rates and the issue of wealth inequalities

9. [1803.02171v2] - Kinetic models for optimal control of wealth inequalities

图 13：DeepResearcher 为论文『TaxAgent: How Large Language Model Designs Fiscal Policy』生成的报告示例。

## Related Works

Economic inequality is a pressing global issue, affecting education, healthcare, and social stability [1]. Traditional taxation systems, such as the U.S. federal income tax, aim to reduce inequality but often lack adaptability to changing economic conditions [2]. In response, researchers have developed more dynamic models, including the Saez Optimal Taxation framework, which adjusts tax rates based on economic principles [3]. The Saez framework is built on the idea of optimizing tax rates to achieve a balance between equity and productivity, taking into account the elasticity of taxable income [3]. However, this framework has limitations, such as assuming a representative taxpayer and neglecting heterogeneity in taxpayer behavior [4]. Furthermore, it does not fully account for irrational behavior, such as taxpayer responses to tax rates that may not be solely driven by economic incentives [5].

Recent studies have explored the use of agent-based modeling (ABM) to simulate economic systems and design more effective tax policies [6]. ABM allows for the representation of heterogeneous agents, such as households, and their interactions within a macroeconomic environment [7]. For instance, [8] used ABM to examine the impact of tax policies on income inequality, finding that optimized tax schedules can lead to better equity-efficiency trade-offs. Specifically, [8] demonstrated that tax policies optimized for individual agent characteristics, such as income level and risk aversion, can lead to more effective reduction in income inequality.

The integration of large language models (LLMs) with ABM has shown promise in various applications, including economic policy design [9]. LLMs can process vast amounts of data and provide insights into complex systems, making them suitable for optimizing tax policies [10]. Researchers have also explored the use of reinforcement learning (RL) to optimize tax policies in dynamic economic environments [11]. Furthermore, the combination of LLMs and ABM has been applied to other domains, such as healthcare [12], financial markets [13], and transportation systems [14]. For example, [12] used LLMs to analyze patient data and predict disease outcomes while [13] applied LLMs to simulate stock market behavior and optimize investment strategies.

In the context of taxation, [15] demonstrated the potential of LLMs to improve tax policy design by analyzing taxpayer behavior and optimizing tax rates. Our work builds on these advancements, introducing TaxAgent, a novel integration of LLMs with ABM to design adaptive tax policies. TaxAgent utilizes LLMs to iteratively optimize tax rates, balancing equity and productivity in a macroeconomic simulation. The simulation features heterogeneous H-Agents (households) that simulate real-world taxpayer behaviors, providing a more realistic representation of economic systems.

Compared to existing models, such as the Saez Optimal Taxation framework, TaxAgent offers a more nuanced understanding of taxpayer behavior and its impact on tax policy effectiveness [3]. Additionally, TaxAgent's use of LLMs enables it to adapt to changing economic conditions, providing a more dynamic and responsive approach to tax policy design [9].

## References

[1] Piketty, T., & Saez, E. (2014). Inequality in the long run. Science, 344(6186), 838-843.

[2] Diamond, P., & Mirrlees, J. A. (1971). Optimal taxation and public production I: Production efficiency. Journal of Economic Theory, 3(4), 275-291.

[3] Saez, E. (2010). Do tax filers bunch around kink points? American Economic Journal: Economic Policy, 2(3), 180-212.

[4] Chetty, R. (2009). Is the taxable income elasticity sufficient to calculate deadweight loss? The effect of marginal tax rates on taxable income. Journal of Economic Perspectives, 23(4), 91-112.

[5] Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. Econometrica, 47(2), 263-292.

[6] Axtell, R. L. (2000). How agents interact matters for the macroeconomy. Journal of Economic Dynamics and Control, 24(5), 725-748.

[7] Epstein, J. M., & Axtell, R. L. (1996). Growing artificial societies: Social science from the bottom up. Brookings Institution Press.

[8] Zheng, X., et al. (2020). AI-driven economic simulations and two-level reinforcement learning. arXiv preprint arXiv:2006.04613.

[9] Narasimhan, K., et al. (2022). Language models for optimization: A study on large language models for economic policy design. arXiv preprint arXiv:2204.04644.

[10] Azizi, M., et al. (2022). Using large language models for economic policy analysis. arXiv preprint arXiv:2209.13443.

[11] Szpruch, L., et al. (2022). Reinforcement learning for optimal tax policy design. arXiv preprint arXiv:2206.03021.

[12] Li, M., et al. (2022). Large language models for healthcare: A study on disease diagnosis and patient outcome prediction. arXiv preprint arXiv:2207.08392.

[13] Wang, Y., et al. (2022). Simulating stock market behavior with large language models. arXiv preprint arXiv:2208.13415.

[14] Zhang, J., et al. (2022). Optimizing traffic flow with large language models. arXiv preprint arXiv:2209.15623.

[15] Chen, L., et al. (2022). Improving tax policy design with large language models. arXiv preprint arXiv:2210.01234.

图 14：OpenScholar 为论文『TaxAgent: How Large Language Model Designs Fiscal Policy』生成的报告示例。

# Related Works

Economic inequality is a pressing global issue, affecting education, healthcare, and social stability. To address this challenge, various studies have explored the impact of taxation on economic inequality. Traditional tax systems, such as the U.S. federal income tax, aim to reduce inequality but often lack adaptability [1]. In contrast, models like the Saez Optimal Taxation propose dynamic adjustments to tax policies, but they fail to account for taxpayer heterogeneity and irrational behavior [2].

Recent advances in artificial intelligence (AI) and agent-based modeling (ABM) have provided new avenues for studying economic systems and designing adaptive tax policies. For instance, agent-based models have been used to simulate economic systems, including the effects of tax evasion [1] and the impact of social cohesion on tax compliance [1]. These models have demonstrated the presence of threshold levels in the composition of society, which can explain the extent of damages deriving from tax evasion [1].

The use of large language models (LLMs) has also shown promise in understanding human behavior and decision-making. Research has demonstrated that LLMs can exhibit human-like reasoning, aligning with human behavior in economic experiments, surveys, and political discourse [3]. However, LLMs differ fundamentally from humans, relying on probabilistic patterns rather than embodied experiences or survival objectives [3]. Therefore, caution is advised when using LLMs to study human behavior or as surrogates or simulations [3].

In the context of tax policy design, several studies have explored the application of AI and ABM. For example, a case study on the role of Management Information System in time-saving during the payment of automobile tax in Sindh through e-filling methods highlights the importance of efficient tax collection systems [4]. Another study proposes a Web-Based Affectedness Indicator (WAI) for real-time monitoring of economic disruptions across diverse contexts, leveraging Large Language Model (LLM) assisted classification and information extraction [5].

The integration of LLMs with ABM has also been explored in other fields, such as multi-agent reinforcement learning [6]. The Learning Optimal Pigovian Tax method (LOPT) uses an additional agent to learn the tax/allowance allocation policy, internalizing externalities and alleviating social dilemmas [6]. Similarly, the use of information-theoretic approaches, such as the Information Bottleneck method, has been proposed for explainable AI (XAI) design [7].

This study builds upon these works, introducing TaxAgent, a novel integration of LLMs with ABM to design adaptive tax policies. By simulating real-world taxpayer behaviors and iteratively optimizing tax rates, TaxAgent achieves superior equity-efficiency trade-offs compared to traditional tax systems and models.

## References

[7] arXiv preprint: Recent advances in explainable AI (XAI) (2022)

[1] arXiv preprint: Agent-based model of an economic system (2022)

[4] arXiv preprint: Case Study on the role of Management Information System in time-saving during the payment of automobile tax in Sindh (2022)

[5] arXiv preprint: Web-Based Affectedness Indicator (WAI) for real-time monitoring of economic disruptions (2023)

[8] arXiv preprint: Agent-based approach for complex systems modelling (2023)

[9] arXiv preprint: Information Filter upon Diversity-Improved Decoding (IFDID) for Natural Language Generation (2023)

[6] arXiv preprint: Learning Optimal Pigovian Tax method (LOPT) for multi-agent reinforcement learning (2023)

[2] arXiv preprint: International Taxation and its impact on Georgian Business Subjects (2023)

[3] arXiv preprint: Assessing the reasoning depth of large language models (LLMs) (2024)

[10] arXiv preprint: (Not provided, as it was not mentioned in the context)

图 15：STORM 为论文『TaxAgent: How Large Language Model Designs Fiscal Policy』生成的报告示例。

**框 8：生成 ArXiv 搜索查询的提示词**

You are an expert technical writer generating targeted search queries to retrieve the most relevant arXiv papers for a technical report section.
<Report topic>
{{topic}}
</Report topic>
<Background>
{{background}}
</Background>
<Task>
Generate {number_of_queries} distinct arXiv search queries to comprehensively cover the section topic. Today's date is date.
Guidelines for queries:
1. Each query should use 1–10 keywords, focusing on a single, specific concept related to the topic.

2. Ensure queries explore different or complementary aspects of the topic to maximize coverage.

3. Use terminology and phrasing likely to match arXiv paper titles or abstracts.

4. Avoid overly broad or generic queries; be as precise as possible.

5. Queries should cover all the key aspects of the topic. Background information may be used to inform the queries.

6. DO NOT create a complex query using AND/OR etc. Keep it simple
The goal is to maximize the relevance and diversity of retrieved papers.
</Task>

**框 9：最终生成与摘要的 Sem-Agg 指令**

You are an expert technical writer crafting one section of a technical report.
<User Query>
{topic}
</User Query>
<Section instructions>
{section_instructions}
</Section instructions>
<Existing section content (if populated)>
{existing_content}
</Existing section content>
<Source material>
{context}
</Source material>
<Citation Guidelines>

- Use [X] format where X is the {citation_number}

- Place citations immediately after the sentence or paragraph they are referencing (e.g., information from context [3]. Further details discussed in contexts [2][7].).

- If urls are given in existing section content, rewrite them exactly if using information related to the url.

- Make sure to provide citations whenever you are using information from the source material. This is a MUST.

- Cite as many sources as possible.

- Make sure to retain the citation numbers from the input context.
- Provide in-line citations only. You do not need a reference section at the end.

<Citation Guidelines>
<Guidelines for writing>

1. If the existing section content is populated, write a new section that enhances the existing section content with the new information. If not, write a new section from scratch.

2. Provide groundings in the source material for all facts stated.

3. When using information from a given source, make sure to cite the source.

4. If a table or list would enhance understanding of a key point, and if so, include one.

5. Make sure to follow the user query strictly.

</Guidelines for writing>
<Writing style>

1. Content Requirements:

- Ground all facts in the source material and provide citations.

- Maintain an academic, technical focus throughout. No marketing language

- Address potential counter-arguments where relevant.

2. Structure and Formatting:

- Use Markdown formatting.

- Begin with ## for section title (Markdown format) and other headings as needed.

- Use simple, clear language appropriate for academic writing.

</Writing style>
<Quality checks>

- No preamble prior to creating the section content

- Cite as many sources as possible.

</Quality checks>
