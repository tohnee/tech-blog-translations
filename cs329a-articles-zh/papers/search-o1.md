---
title: "Search-o1：智能体搜索增强的大型推理模型"
title_en: "Search-o1: Agentic Search-Enhanced Large Reasoning Models"
arxiv: 2501.05366
source: https://arxiv.org/abs/2501.05366
crawled: 2026-09-23
translated: 2026-09-23
---

# Search-o1：智能体搜索增强的大型推理模型

> 原文：[Search-o1: Agentic Search-Enhanced Large Reasoning Models](https://arxiv.org/abs/2501.05366) · Stanford CS329A 指定阅读

Xiaoxi Li（中国人民大学）
Guanting Dong（中国人民大学）
Jiajie Jin（中国人民大学）
Yuyao Zhang（中国人民大学）
Yujia Zhou（清华大学）
Yutao Zhu（中国人民大学）
Peitian Zhang（中国人民大学）
Zhicheng Dou（中国人民大学；通讯作者；邮箱：{xiaoxi_li, dou}@ruc.edu.cn；项目主页：<https://search-o1.github.io/>）

###### 摘要

以 OpenAI-o1 为代表的大型推理模型（LRM）通过大规模强化学习展现出令人印象深刻的长期逐步推理能力。然而，其延伸的推理过程常常受知识不足之苦，导致频繁的不确定性与潜在错误。为解决这一局限，我们提出 Search-o1——一个用智能体检索增强生成（RAG）机制与一个用于精炼检索文档的 Reason-in-Documents 模块来增强 LRM 的框架。Search-o1 把智能体搜索工作流整合进推理过程，使 LRM 在遇到不确定的知识点时能够动态检索外部知识。此外，由于检索文档往往冗长，我们设计了独立的 Reason-in-Documents 模块，在把检索信息注入推理链之前对其进行深入分析，最大限度降低噪声并保持连贯的推理流。在科学、数学与编程等复杂推理任务以及六个开放域问答基准上的大量实验证明了 Search-o1 的强劲表现。该方法提升了 LRM 在复杂推理任务上的可信度与适用性，为更可靠、更通用的智能系统铺平了道路。代码可在 <https://github.com/sunnynexus/Search-o1> 获取。

## 1 引言

近期出现的大型推理模型（LRM），以 OpenAI 的 o1（Jaech et al., 2024）、Qwen-QwQ（Qwen Team, 2024）与 DeepSeek-R1（DeepSeek-AI, 2024）为代表，借助大规模强化学习培养出令人印象深刻的长期逐步推理能力，为复杂推理问题提供了有前景的解决方案（OpenAI, 2024；Lewkowycz et al., 2022；Wei et al., 2022；Zhong et al., 2024；Yu et al., 2024；Yuan et al., 2023；Yang et al., 2024）。这一进展启发了一系列旨在探索与复现 o1 式推理模式的基础性工作，以将其应用拓宽到更广泛的基础模型（Qin et al., 2024；Huang et al., 2024；Zhang et al., 2024；Zhang et al., 2024；Ye et al., 2024；Jiang et al., 2024；Min et al., 2024）。

值得注意的是，o1 式推理模式引导 LRM 进入一个更慢的思考过程（Kahneman, 2017；Wu et al., 2024）：隐式地分解复杂问题，生成很长的内部推理链，然后逐步发现合适的解。虽然这一特性增强了推理的逻辑连贯性与可解释性，延伸的思维链可能导致过度思考（Chen et al., 2024）以及知识不足风险的上升（Raffel et al., 2020；Wong et al., 2021；Brown et al., 2020），任何知识缺口都可能传播错误并扰乱整条推理链（Zhang et al., 2023；Ling et al., 2023；Miao et al., 2024；Liu et al., 2024）。

为解决这一局限，我们开展初步实验来评估 LRM 因知识缺口而解码出的不确定词的频率。如图 1 所示，延伸的思考过程使 LRM 在有挑战性的推理问题中频繁解码出大量不确定表述，「perhaps」在每个推理过程中平均出现超过 30 次。值得注意的是，这些问题的高度专业化也使人工推理验证变得复杂，往往代价高昂（Xia et al., 2024）。因此，自动补充 o1 式推理过程所需的知识已成为一项重大挑战，限制着 LRM 在实现普遍可信推理方面的进展。

为阐明这一主题，我们的核心动机是通过自主检索增强具备 o1 式推理模式的 LRM。我们提出 Search-o1，它把 LRM 的推理过程与两个核心组件整合：一个智能体检索增强生成（RAG）机制与一个知识精炼模块。该设计旨在让 LRM 把智能体搜索工作流纳入推理过程，按需检索外部知识以支持逐步推理，同时全程保持连贯性。

具体而言，我们在图 1 中的结果揭示，与直接推理相比，传统的面向问题的 RAG 技术并未有效弥合知识缺口（Standard RAG vs. Direct Reasoning）。这一发现与人类直觉一致：标准 RAG 只以面向问题的方式检索一次相关知识，而复杂推理场景中每一步所需的知识往往是多样且各异的（Zheng et al., 2024；Liu et al., 2024；Dong et al., 2024）。与它们不同，Search-o1 采用智能体 RAG 技术，引导模型在面临知识短缺时主动解码搜索查询，从而触发检索机制获取相关外部知识。得益于这一设计，我们的检索机制可以在单次推理会话内被触发并迭代多次，满足各推理步骤的知识需求。

为把检索到的知识有效整合进 LRM 的推理过程，我们在实践中进一步识别出把检索文档直接纳入推理链时的两个关键挑战：
(1) **检索文档中的冗余信息。** 检索文档往往冗长且包含冗余信息，直接输入 LRM 可能破坏推理原有的连贯性，甚至引入噪声（Wu et al., 2024；Yoran et al., 2024；Jin et al., 2024）。
(2) **理解长文档的能力有限。** 大多数 LRM 在预训练与微调阶段专门针对复杂推理任务做了对齐。这种聚焦导致其通用能力出现一定程度的灾难性遗忘（Lin et al., 2024；Dong et al., 2024），最终限制了它们对检索文档的长上下文理解。

为应对这些挑战，我们引入独立于主推理链运行的 Reason-in-Documents 模块。该模块首先基于当前搜索查询与先前推理步骤对检索文档进行透彻分析，然后产出能无缝衔接先前推理链的精炼信息。

| 模型表达不确定性的案例 |
| --- |
| Wait, perhaps it's referring to dimethyl sulfone, but that doesn't seem right. |
| Alternatively, perhaps there's a mistake in my understanding of epistasis. Let me look up epistasis quickly. Epistasis is … |
| Alternatively, HBr could also abstract a hydrogen atom from the alkene, leading to a … |
| As I recall, Quinuclidine is a seven-membered ring with a nitrogen atom, likely not having the required symmetry. |

图 1：用 QwQ-32B-Preview 分析推理不确定性。左：推理过程中识别出的不确定词示例。右：GPQA diamond 集上每个输出的高频不确定词平均出现次数。

总而言之，我们的贡献如下：

- 我们提出 Search-o1——首个把智能体搜索工作流整合进 LRM 的 o1 式推理过程、实现自主知识补充的框架。

- 为在推理过程中有效整合外部知识，Search-o1 把推理过程与智能体 RAG 机制及知识精炼模块相结合。该设计使 LRM 能按需检索外部知识，在保持原有逻辑流的同时无缝纳入推理链。

- 凭借五个复杂推理领域与六个开放域问答基准，我们证明 Search-o1 在推理领域取得显著性能，同时在通用知识上保持大幅提升。进一步的定量分析确认了其效率与可扩展性，为 LRM 的可信推理提供实用指导。

## 2 相关工作

##### 大型推理模型。

大型推理模型聚焦于通过利用延伸的推理步骤提升测试时表现，与通过增大模型规模或扩展训练数据在训练期间实现可扩展性的传统大型预训练模型形成对照（Henighan et al., 2020；Yang et al., 2024；Qwen, 2024；Zhong et al., 2024；Zeng et al., 2024）。研究表明，测试时扩展可以提升较小模型在复杂任务上的推理能力（Feng et al., 2024；Zelikman et al., 2024）。近来，OpenAI-o1（Jaech et al., 2024）、Qwen-QwQ（Qwen Team, 2024）与 DeepSeek-R1（DeepSeek-AI, 2024）等模型显式展现思维链推理（Wei et al., 2022），在数学、编程等领域模仿人类的问题求解方式。

实现 o1 式推理能力的方法已被多方探索。一些方法把策略与奖励模型和蒙特卡洛树搜索（MCTS）结合（Jiang et al., 2024），但这并未把推理内化到模型中。其他研究在训练时在推理路径中纳入刻意错误，以部分内化这些能力（Qin et al., 2024；Ye et al., 2024）。此外，蒸馏训练数据已被证明可增强模型的 o1 式推理技能（Min et al., 2024）。o1 式推理范式在多个领域展现了强劲表现，包括视觉-语言推理（Xu et al., 2024；Dong et al., 2024；Qiao et al., 2024；Yao et al., 2024）、代码生成（Zhang et al., 2024；Li et al., 2024）、医疗（Chen et al., 2024）与机器翻译（Wang et al., 2024）。然而，这些方法受限于对静态参数化模型的依赖，在内部知识不足时无法利用外部世界知识。

##### 检索增强生成。

检索增强生成（RAG）引入检索机制来解决生成模型静态参数的局限，允许访问外部知识以求解更复杂的问题（Lewis et al., 2020；Zhao et al., 2024；Li et al., 2024；Zhou et al., 2024）。该领域的前沿研究从多个方面增强 RAG 系统，包括检索的必要性（Tan et al., 2024）、查询预处理（Ma et al., 2023；Wang et al., 2023）、检索文档压缩（Xu et al., 2023）、去噪（Liu et al., 2024；Liu et al., 2024）、精炼（Jiang et al., 2023；Jin et al., 2024；Zhou et al., 2024）、指令遵循（Dong et al., 2024；Dong et al., 2024；Zhou et al., 2024）等。此外，一些研究探索了实现 RAG 系统的端到端模型训练（Asai et al., 2023；Li et al., 2024；Li et al., 2024；Li et al., 2024）以及基于知识图谱的 RAG 系统（Edge et al., 2024；Liang et al., 2024）。

近来，智能体 RAG 系统使模型能按需自主决定何时检索以及检索什么知识，展现出更强的规划与问题求解能力（Chen et al., 2024；Verma et al., 2024；Yao et al., 2022）。也有研究把基于智能体的系统与 MCTS 结合来优化复杂工作流，利用检索器与其他工具完成任务（Zhang et al., 2024）。然而，现有 RAG 方法尚未与 o1 式模型的强推理能力结合，限制了在求解复杂任务上进一步提升系统性能的潜力。

图 2：推理方法比较：(a) 不带检索的直接推理常因知识缺失导致不准确。(b) 我们的智能体检索增强推理方法改善了知识获取，但通常返回冗长、冗余的文档，破坏连贯推理。(c) 我们的 Search-o1 把简洁准确的检索知识无缝整合进推理过程，实现精确而连贯的问题求解。

## 3 方法

### 3.1 问题形式化

我们考虑一个需要多步推理与外部知识检索才能导出解答的复杂推理任务。目标是为每个问题 $q$ 生成一个完整解答，由逻辑推理链 $\mathcal{R}$ 与最终答案 $a$ 组成。本工作中，我们使推理模型在推理过程中能利用外部知识源。具体而言，我们考虑问题求解过程的三个主要输入：任务指令 $I$、问题 $q$、以及外部检索文档 $\mathcal{D}$。这里 $I$ 提供对推理任务的总体描述，$q$ 是待回答的具体复杂问题，$\mathcal{D}$ 包含从相关知识库动态检索的背景知识。

目标是设计一个有效整合 $I$、$q$ 与 $\mathcal{D}$ 的推理机制，以产出连贯的推理链 $\mathcal{R}$ 与最终答案 $a$。这可形式化为映射 $(I,q,\mathcal{D})\rightarrow(\mathcal{R},a)$。推理序列与最终答案的生成可表示为：

$$P(\mathcal{R},a\mid I,q,\mathcal{D})=\underbrace{\prod_{t=1}^{T_{r}}P(\mathcal{R}_{t}\mid\mathcal{R}_{<t},I,q,\mathcal{D}_{<t})}_{\text{推理过程}}\cdot\underbrace{\prod_{t=1}^{T_{a}}P(a_{t}\mid a_{<t},\mathcal{R},I,q)}_{\text{答案生成}},\tag{1}$$

其中 $T_{r}$ 是推理序列 $\mathcal{R}$ 中的 token 数。位置 $t$ 的 token 为 $\mathcal{R}_{t}$，$\mathcal{R}_{<t}$ 表示位置 $t$ 之前生成的所有 token。$\mathcal{D}_{\leq t}$ 表示推理链中到 token $t$ 为止检索到的所有文档。类似地，$T_{a}$ 是答案序列 $a$ 的长度，$a_{t}$ 是位置 $t$ 的 token，$a_{<t}$ 表示位置 $t$ 之前生成的所有答案 token。

### 3.2 Search-o1 框架概览

Search-o1 框架通过把外部知识检索无缝整合进大型推理模型（LRM）的推理过程并保持思维链连贯性，来解决其知识不足问题。如图 2 所示，我们给出三种方法的比较分析：朴素推理、智能体检索增强生成（RAG）、以及我们提出的 Search-o1 框架。

- **朴素推理模式**：考虑图 2(a) 中的例子，任务是确定一个三步化学反应最终产物中的碳原子数。朴素推理方法在遇到知识缺口（例如「反式肉桂醛的结构」）时会失灵。由于无法获取准确信息，模型只能依赖假设，可能在后续推理步骤中导致级联错误。

- **智能体 RAG**：为在推理中弥合知识缺口，我们构建智能体 RAG 机制（图 2(b)），使模型能在需要时自主检索外部知识。当出现不确定性——例如关于化合物的结构——模型生成有针对性的搜索查询（如「structure of trans-Cinnamaldehyde」）。然而，直接插入往往包含冗长无关信息的检索文档，可能扰乱推理流并损害连贯性。

- **Search-o1**：我们的 Search-o1 框架（图 2(c)）通过纳入 Reason-in-Documents 模块扩展了智能体 RAG 机制。该模块把检索文档浓缩为聚焦的推理步骤，在整合外部知识的同时维持推理链的逻辑流。它考虑当前搜索查询、检索文档与既有推理链以生成连贯的步骤。这一迭代过程持续到得出最终答案。后续小节详细解释智能体 RAG、Reason-in-Documents 与 Search-o1 推理过程。

### 3.3 智能体检索增强生成机制

智能体 RAG 机制是 Search-o1 框架的关键组件，使推理模型能在推理过程中自主决定何时检索外部知识。该机制允许模型自身决定是继续生成推理步骤还是发起一次检索。详细的模型指令见附录 A.1。

在生成推理链 $\mathcal{R}$ 期间，模型可能间歇性地生成由特殊符号 <|begin_search_query|> 与 <|end_search_query|> 包裹的搜索查询 $q_{\text{search}}^{(i)}$，其中 $i$ 索引第 $i$ 次搜索步骤。每个搜索查询基于推理过程的当前状态与先前检索到的知识生成。每个搜索查询的生成表示为：

$$P(q_{\text{search}}^{(i)}\mid I,q,\mathcal{R}^{(i-1)})=\prod_{t=1}^{T_{q}^{(i)}}P\left(q_{\text{search},t}^{(i)}\mid q_{\text{search},<t}^{(i)},I,q,\mathcal{R}^{(i-1)}\right),\tag{2}$$

其中 $T_{q}^{(i)}$ 是第 $i$ 个搜索查询的长度，$q_{\text{search},t}^{(i)}$ 表示第 $i$ 个搜索查询第 $t$ 步生成的 token，$\mathcal{R}^{(i-1)}$ 表示第 $i$ 次搜索步骤之前的所有推理步骤（包括搜索查询与搜索结果）。

一旦在推理序列中检测到新的一对搜索查询特殊符号，我们就暂停推理过程，并提取搜索查询 $q_{\text{search}}^{(i)}$。调用检索函数 Search 获取相关文档：

$$\mathcal{D}^{(i)}=\texttt{Search}(q_{\text{search}}^{(i)}),\tag{3}$$

其中 $\mathcal{D}^{(i)}=\{d_{1}^{(i)},d_{2}^{(i)},\ldots,d_{k_{i}}^{(i)}\}$ 表示为第 $i$ 个搜索查询检索到的 top-$k_{i}$ 相关文档集合。检索到的文档 $\mathcal{D}^{(i)}$ 随后被注入推理链 $\mathcal{R}^{(i-1)}$ 中特殊符号 <|begin_search_result|> 与 <|end_search_result|> 之间，使推理模型能利用外部知识继续推理过程。

这一智能体机制使模型能动态、高效地纳入外部知识，保持推理过程的连贯性与相关性，同时避免来自过多或无关检索结果的信息过载。

### 3.4 通过 Reason-in-Documents 进行知识精炼

虽然智能体 RAG 机制解决了推理中的知识缺口，但由于长度与冗余，直接插入完整文档可能破坏连贯性。为克服这一点，Search-o1 框架包含知识精炼模块，通过使用原推理模型进行一个独立的生成过程，只选择性地把相关且简洁的信息整合进推理链。该模块处理检索文档以契合模型的具体推理需求，把原始信息转化为精炼且切题的知识，同时保持主推理链的连贯与逻辑一致。

Reason-in-Documents 的精炼指南详见附录 A.1。这些指南指示模型基于先前的推理步骤、当前搜索查询以及被搜索网页的内容来分析检索到的网页。目标是提取直接有助于推进原始问题推理过程的相关且准确的信息，确保与既有推理链的无缝整合。

对每次搜索步骤 $i$，令 $\mathcal{R}^{(<i)}$ 表示累积到第 $i$ 个搜索查询之前的推理链。给定 $\mathcal{R}^{(<i)}$、当前搜索查询 $q_{\text{search}}^{(i)}$ 与检索文档 $\mathcal{D}^{(i)}$，知识精炼过程分两阶段运作：先生成用于分析检索文档的中间推理序列 ${r}_{\text{docs}}^{(i)}$，然后基于该分析产出精炼知识 ${r}_{\text{final}}^{(i)}$。中间推理序列 ${r}_{\text{docs}}^{(i)}$ 的生成表示为：

$$P({r}_{\text{docs}}^{(i)}\mid\mathcal{R}^{(<i)},q_{\text{search}}^{(i)},\mathcal{D}^{(i)})=\prod_{t=1}^{T_{d}^{(i)}}P\left({r}_{\text{docs},t}^{(i)}\mid{r}_{\text{docs},<t}^{(i)},\mathcal{R}^{(<i)},q_{\text{search}}^{(i)},\mathcal{D}^{(i)}\right),\tag{4}$$

其中 $T_{d}^{(i)}$ 是中间推理序列的长度，${r}_{\text{docs},t}^{(i)}$ 表示第 $t$ 步的 token。精炼知识 ${r}_{\text{final}}^{(i)}$ 随后基于该分析生成：

$$P({r}_{\text{final}}^{(i)}\mid{r}_{\text{docs}}^{(i)},\mathcal{R}^{(<i)},q_{\text{search}}^{(i)})=\prod_{t=1}^{T_{r}^{(i)}}P\left({r}_{\text{final},t}^{(i)}\mid{r}_{\text{final},<t}^{(i)},{r}_{\text{docs}}^{(i)},\mathcal{R}^{(<i)},q_{\text{search}}^{(i)}\right),\tag{5}$$

其中 $T_{r}^{(i)}$ 是精炼知识序列的长度，${r}_{\text{final},t}^{(i)}$ 表示第 $t$ 步的 token。精炼知识 ${r}_{\text{final}}^{(i)}$ 随后被并入推理链 $\mathcal{R}^{(i)}$，使模型能在获取外部知识的情况下继续生成连贯的推理步骤。

$$P(\mathcal{R},a\mid I,q)=\prod_{t=1}^{T_{r}}P\left(\mathcal{R}_{t}\mid\mathcal{R}_{<t},I,q,\{r_{\text{final}}^{(j)}\}_{j\leq i(t)}\right)\cdot\prod_{t=1}^{T_{a}}P\left(a_{t}\mid a_{<t},\mathcal{R},I,q\right),\tag{6}$$

其中 $\{r_{\text{final}}^{(j)}\}_{j\leq i(t)}$ 表示到第 $i(t)$ 次搜索步骤为止的所有先前精炼知识。这里 $i(t)$ 表示与当前推理步骤 $t$ 对应的搜索步骤索引。这种精炼知识的整合确保每个推理步骤都能访问相关的外部信息，同时保持推理过程的简洁与聚焦。

**算法 1　Search-o1 推理**

```
1:  推理模型 M，搜索函数 Search
2:  输入：问题集 Q，任务指令 I，Reason-in-documents 指令 I_docs
3:  初始化未完成序列集合 S ← {I ⊕ q | q ∈ Q}
4:  初始化已完成序列集合 F ← {}
5:  while S ≠ ∅ do
6:      生成 S 中的所有序列直至 EOS 或 <|end_search_query|>：T ← M(S)      ▷ 批量生成
7:      初始化空集 S_r ← {}                                                 ▷ Reason-in-documents 输入
8:      for 每个序列 Seq ∈ T do
9:          if Seq 以 <|end_search_query|> 结尾 then
10:             提取搜索查询：q_search ← Extract(Seq, <|begin_search_query|>, <|end_search_query|>)
11:             检索文档：D ← Search(q_search)                               ▷ 检索
12:             构造 Reason-in-documents 输入：I_D ← I_docs ⊕ q_search ⊕ Seq
13:             把元组 (I_D, Seq) 追加到 S_r
14:         else if Seq 以 EOS 结尾 then
15:             把 Seq 从 S 移除，加入 F                                      ▷ 序列完成
16:     if S_r ≠ ∅ then
17:         准备批量输入：I_r ← {I_D | (I_D, Seq) ∈ S_r}
18:         Reason-in-documents：T_r ← M(I_r)                                ▷ 批量生成
19:         for i ← {1, …, |T_r|} do
20:             令 r ← T_r[i]，Seq ← S_r[i].Seq
21:             提取注入知识后的推理步骤：r_final ← Extract(r)
22:             更新 S 中的序列：Seq ← Insert(<|begin_search_result|>, r_final, <|end_search_result|>)
23: 输出：已完成序列 F
```

### 3.5 Search-o1 推理过程

##### 单个问题的推理逻辑。

对每个问题，Search-o1 推理首先用任务指令 $I$ 拼接具体问题 $q$ 来初始化推理序列。当推理模型 $\mathcal{M}$ 生成推理链 $\mathcal{R}$ 时，它可能产生由特殊符号 <|begin_search_query|> 与 <|end_search_query|> 包裹的搜索查询。检测到 <|end_search_query|> 符号后，提取相应搜索查询 $q_{\text{search}}$，触发检索函数 Search 获取相关外部文档 $\mathcal{D}$。这些检索文档连同 Reason-in-documents 指令 $I_{\text{docs}}$ 与当前推理序列 $\mathcal{R}$，随后由 Reason-in-Documents 模块处理。该模块把原始文档精炼为简洁、切题的信息 $r_{\text{final}}$，并无缝整合回符号 <|begin_search_result|> 与 <|end_search_result|> 之间的推理链 $\mathcal{R}$。这一迭代过程确保推理模型在纳入必要外部知识的同时保持连贯与逻辑一致，最终生成完整的推理链 $\mathcal{R}$ 与最终答案 $a$。

##### 批量推理机制。

为高效地同时处理多个问题，Search-o1 框架采用一种同时优化 token 生成与知识精炼的批量推理机制。初始时，通过把任务指令 $I$ 与批次 $\mathcal{Q}$ 中每个问题 $q$ 拼接，创建一组未完成推理序列 $\mathcal{S}$。推理模型 $\mathcal{M}$ 随后为 $\mathcal{S}$ 中的所有序列并行生成 token，推进每条推理链直至完成或需要外部知识检索。当在任何序列中识别出搜索查询时，提取相应查询并通过 Search 函数批量处理以检索相关文档 $\mathcal{D}$。这些文档随后由 Reason-in-Documents 模块统一精炼，为每个序列生成精炼知识 $r_{\text{final}}$。精炼知识随后插回各自的推理链。完成的序列移入已完成集合 $\mathcal{F}$，进行中的序列保留在 $\mathcal{S}$ 以待进一步处理。通过在生成与精炼两个步骤都利用并行处理，批量推理机制提升了并发处理多个输入的系统吞吐量。

## 4 实验

### 4.1 任务与数据集

本实验使用的评估包括以下两类：

**有挑战性的推理任务**：
(1) GPQA（Rein et al., 2023）是一个博士级科学多项选择问答数据集。问题由物理学、化学与生物学领域专家撰写。主实验中，我们使用包含 198 道题的最高质量 diamond 集；在表 2 中，我们使用包含 546 道题、更全面的扩展集来与人类专家的表现比较。
(2) 数学基准包括 MATH500（Lightman et al., 2024）、AMC2023¹ 与 AIME2024²。MATH500 由 MATH 测试集（Hendrycks et al., 2021）中的 500 道题组成。AMC2023 与 AIME2024 是涵盖算术、代数、几何等的中学生数学竞赛，分别包含 40 与 30 道题。在这三个数据集中，MATH500 与 AMC 相对简单，而 AIME 更难。
(3) LiveCodeBench（Jain et al., 2024）是评估 LLM 编程能力的基准，由简单、中等与困难难度的问题组成。它收集竞赛平台最近发布的编程问题以避免数据污染。我们使用 2024 年 8 月至 11 月的问题，共 112 道。

¹ <https://huggingface.co/datasets/AI-MO/aimo-validation-amc>
² <https://huggingface.co/datasets/AI-MO/aimo-validation-aime>

**开放域问答任务**：
(1) 单跳问答数据集：Natural Questions（NQ）（Kwiatkowski et al., 2019）包含来自真实 Google 搜索查询的问题，答案取自 Wikipedia 文章。TriviaQA（Joshi et al., 2017）是来自问答网站与竞赛的大规模数据集，具有复杂的实体关系。
(2) 多跳问答数据集：HotpotQA（Yang et al., 2018）是首个需要跨多个 Wikipedia 段落推理的大规模数据集。2WikiMultihopQA（2WIKI）（Ho et al., 2020）为多跳问题提供显式推理路径。MuSiQue（Trivedi et al., 2022）的特色是由五个既有单跳数据集构建的 2-4 跳问题。Bamboogle（Press et al., 2023）收集 Google 回答错误的复杂问题，用于评估模型在各领域的组合推理。

### 4.2 基线

我们将我们的方法与以下基线方法进行评估对比：

**直接推理**：这些方法利用模型内部知识而不检索。开源模型包括 Qwen2.5-32B-Instruct（Qwen, 2024）、Qwen2.5-Coder-32B-Instruct（Hui et al., 2024）、QwQ-32B-Preview（Qwen Team, 2024）、Qwen2.5-72B-Instruct（Qwen, 2024）与 Llama3.3-70B-Instruct（Dubey et al., 2024）。闭源非专有模型包括 DeepSeek-R1-Lite-Preview（DeepSeek-AI, 2024）、OpenAI GPT-4o（Hurst et al., 2024）与 o1-preview（Jaech et al., 2024）。开源模型的结果基于我们的实现，闭源模型结果取自其官方发布。

**检索增强推理**：这些方法检索外部信息来增强推理过程。我们考虑两种检索增强途径：
(1) 标准 RAG：为原始问题检索 top-10 文档，并与问题一同输入模型进行推理与答案生成。
(2) RAG 智能体（RAgent）：允许模型决定何时生成查询进行检索，详见第 3.3 节。为控制检索文档长度，受 ReAct（Yao et al., 2022）启发，我们在推理期间先检索 top-10 摘要片段，然后由模型在必要时决定获取哪些 URL 的完整文档。

### 4.3 实现细节

Search-o1 的主干大型推理模型，我们使用开源的 QwQ-32B-Preview（Qwen Team, 2024）。生成设置方面，所有模型均使用最多 32,768 个 token、温度 0.7、top_p 0.8、top_k 20、重复惩罚 1.05。检索方面，我们使用 Bing Web Search API，区域设为 US-EN，检索文档 top-$k$ 设为 10。我们使用 Jina Reader API 获取给定 URL 的网页内容。对所有基于检索的方法，遵循 Rein et al. (2023)，我们采用回退策略：当未给出最终答案时，使用直接推理的结果。对未针对 o1 式推理专门训练的基线模型，我们应用思维链（CoT；Wei et al., 2022）提示，使其在生成答案前先进行推理。所有模型的详细指令见附录 A。所有实验在八块 NVIDIA A800-80GB GPU 上进行。

表 1：有挑战性推理任务上的主要结果，包括博士级科学问答、数学与代码基准。所有任务报告 Pass@1 指标。对 32B 参数的模型，最佳结果加粗，次佳结果加下划线。更大或非专有模型的结果以灰色显示供参考。符号「†」表示来自其官方发布的结果。

| 方法 | GPQA（博士级科学问答） |  |  |  | 数学基准 |  |  | LiveCodeBench |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | 物理 | 化学 | 生物 | 总体 | MATH500 | AMC23 | AIME24 | 简单 | 中等 | 困难 | 总体 |
| 直接推理（无检索） |  |  |  |  |  |  |  |  |  |  |  |
| Qwen2.5-32B | 57.0 | 33.3 | 52.6 | 45.5 | 75.8 | 57.5 | 23.3 | 42.3 | 18.9 | 14.3 | 22.3 |
| Qwen2.5-Coder-32B | 37.2 | 25.8 | 57.9 | 33.8 | 71.2 | 67.5 | 20.0 | 61.5 | 16.2 | 12.2 | 25.0 |
| QwQ-32B | 75.6 | 39.8 | 68.4 | 58.1 | 83.2 | 82.5 | 53.3 | 61.5 | 29.7 | 20.4 | 33.0 |
| Qwen2.5-72B | 57.0 | 37.6 | 68.4 | 49.0 | 79.4 | 67.5 | 20.0 | 53.8 | 29.7 | 24.5 | 33.0 |
| Llama3.3-70B | 54.7 | 31.2 | 52.6 | 43.4 | 70.8 | 47.5 | 36.7 | 57.7 | 32.4 | 24.5 | 34.8 |
| DeepSeek-R1-Lite† | - | - | - | 58.5 | 91.6 | - | 52.5 | - | - | - | 51.6 |
| GPT-4o† | 59.5 | 40.2 | 61.6 | 50.6 | 60.3 | - | 9.3 | - | - | - | 33.4 |
| o1-preview† | 89.4 | 59.9 | 65.9 | 73.3 | 85.5 | - | 44.6 | - | - | - | 53.6 |
| 检索增强推理 |  |  |  |  |  |  |  |  |  |  |  |
| RAG-Qwen2.5-32B | 57.0 | 37.6 | 52.6 | 47.5 | 82.6 | 72.5 | 30.0 | 61.5 | 24.3 | 8.2 | 25.9 |
| RAG-QwQ-32B | 76.7 | 38.7 | 73.7 | 58.6 | 84.8 | 82.5 | 50.0 | 57.7 | 16.2 | 12.2 | 24.1 |
| RAgent-Qwen2.5-32B | 58.1 | 33.3 | 63.2 | 47.0 | 74.8 | 65.0 | 20.0 | 57.7 | 24.3 | 6.1 | 24.1 |
| RAgent-QwQ-32B | 76.7 | 46.2 | 68.4 | 61.6 | 85.0 | 85.0 | 56.7 | 65.4 | 18.9 | 12.2 | 26.8 |
| 带 Reason-in-Documents 的检索增强推理 |  |  |  |  |  |  |  |  |  |  |  |
| Search-o1（本文） | 77.9 | 47.3 | 78.9 | 63.6 | 86.4 | 85.0 | 56.7 | 57.7 | 32.4 | 20.4 | 33.0 |

### 4.4 有挑战性推理任务上的结果

##### 主要结果。

表 1 展示了 Search-o1 在复杂推理任务上的表现，主要结果概述如下：

1. 在无检索与检索增强两种设置下，大型推理模型 QwQ-32B-Preview 均持续优于传统指令微调 LLM。32B 参数的 QwQ 模型在直接推理设置下甚至超过 Qwen2.5-72B 与 Llama3.3-70B 等更大的 LLM，证明了 o1 式长 CoT 方法在复杂推理中的有效性。

2. RAgent-QwQ-32B 在大多数任务上超越标准 RAG 模型与直接推理的 QwQ-32B，这要归功于其自主检索信息以补充每步推理所需知识的智能体搜索机制。此外，我们发现使用智能体 RAG 的非推理模型 Qwen2.5-32B 在 GPQA 上与标准 RAG 表现相近，在数学与代码任务上甚至有所下降。这表明普通 LLM 无法有效利用搜索作为工具求解复杂推理任务。

3. 我们的 Search-o1 在大多数任务上进一步超过 RAgent-QwQ-32B，证明了 Reason-in-Documents 策略在整合外部知识同时确保不影响原有推理连贯性方面的有效性。具体而言，在全部五个数据集上平均，Search-o1 分别超出 RAgent-QwQ-32B 与 QwQ-32B 4.7% 与 3.1%，并显著超出非推理模型 Qwen2.5-32B 与 Llama3.3-70B 44.7% 与 39.3%。

##### 检索文档数量的扩展分析。

表 2：在 GPQA 扩展集（Rein et al., 2023）上与人类专家的表现比较。

| 方法 | GPQA 扩展集 |  |  |  |
| --- | --- | --- | --- | --- |
|  | 物理 | 化学 | 生物 | 总体 |
| 人类专家 |  |  |  |  |
| 物理学家 | 57.9 | 31.6 | 42.0 | 39.9 |
| 化学家 | 34.5 | 72.6 | 45.6 | 48.9 |
| 生物学家 | 30.4 | 28.8 | 68.9 | 37.2 |
| 推理模型 |  |  |  |  |
| QwQ-32B | 61.7 | 36.9 | 61.0 | 51.8 |
| RAG-QwQ-32B | 64.3 | 38.3 | 66.7 | 54.6 |
| Search-o1（本文） | 68.7 | 40.7 | 69.5 | 57.9 |

在该实验中，我们分析随检索文档数量变化的性能，如图 3 所示。我们的结果表明 Search-o1 能有效利用不断增多的检索文档，带来复杂推理任务处理的改进。我们还观察到，就总体性能而言，即使只检索一篇文档也能超过使用十篇检索文档的直接推理与标准 RAG 模型，展示了智能体搜索与 Reason-in-Documents 策略的有效性。

图 3：推理中使用的 top-k 检索文档的扩展分析。所有结果基于 QwQ-32B-Preview 模型。

##### 与人类专家的比较。

我们在 GPQA 扩展集上把 Search-o1 与各领域人类专家的表现进行比较。表 2 给出物理、化学与生物等学科人类专家的评估。我们的 Search-o1 模型在总体表现（57.9）以及物理（68.7）与生物（69.5）上都超过人类专家，展示了对复杂推理任务的出色处理。虽然 Search-o1 在化学子领域略逊于化学家（40.7 vs. 72.6），它总体上仍具竞争力，尤其在跨多领域的通用表现上。这凸显了 Search-o1 利用文档检索与推理取得媲美甚至超过专家水平的跨域表现的有效性。

### 4.5 开放域问答任务上的结果

除 LRM 擅长的推理任务外，我们还探索 Search-o1 在开放域问答任务上的表现。表 3 给出总体结果。关键观察如下：

1. 对不带检索的直接推理，LRM QwQ-32B 的表现与非推理 LLM Qwen2.5-32B 总体相近，在所有问答数据集上的平均 EM 略有下降（31.3 vs. 30.7）。这表明 LRM 在开放域问答任务上不如在推理任务上强势。

2. 采用检索增强推理时，检索显著提升了推理与非推理模型在所有任务上的表现，表明模型在这些任务上存在知识缺口。此外，对 QwQ-32B 模型，智能体 RAG 在多跳问答任务上相对标准 RAG 取得平均 23.2% 的 EM 提升，证明了我们的智能体 RAG 策略在知识型多跳问答上的有效性。然而，我们也观察到单跳任务上没有显著性能变化（平均 EM 47.8 vs. 47.6），因为这些问题只需单一知识点的信息，无需多次检索。这也验证了智能体搜索机制能在更复杂、更具挑战性的推理任务中更好地释放 LRM 的潜力。

3. 对我们的 Search-o1，我们发现它在多跳任务上总体优于所有基线。具体而言，就平均 EM 指标而言，Search-o1 分别超出 RAG-QwQ-32B 与 RAgent-QwQ-32B 29.6% 与 5.3%，证明了 Reason-in-Documents 策略在复杂问答任务中的有效性。这进一步强调了保持外部知识与推理逻辑链之间一致性的重要性。

表 3：开放域问答任务上的表现比较，包括单跳问答与多跳问答数据集。对 32B 参数的模型，最佳结果加粗，次佳结果加下划线。更大模型的结果以灰色显示供参考。

| 方法 | 单跳问答 |  |  |  | 多跳问答 |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | NQ |  | TriviaQA |  | HotpotQA |  | 2WIKI |  | MuSiQue |  | Bamboogle |  |
|  | EM | F1 | EM | F1 | EM | F1 | EM | F1 | EM | F1 | EM | F1 |
| 直接推理（无检索） |  |  |  |  |  |  |  |  |  |  |  |  |
| Qwen2.5-32B | 22.8 | 33.9 | 52.0 | 60.3 | 25.4 | 34.7 | 29.8 | 36.3 | 8.4 | 18.0 | 49.6 | 63.2 |
| QwQ-32B | 23.0 | 33.1 | 53.8 | 60.7 | 25.4 | 33.3 | 34.4 | 40.9 | 9.0 | 18.9 | 38.4 | 53.7 |
| Qwen2.5-72B | 27.6 | 41.2 | 56.8 | 65.8 | 29.2 | 38.8 | 34.4 | 42.7 | 11.4 | 20.4 | 47.2 | 61.7 |
| Llama3.3-70B | 36.0 | 48.7 | 68.8 | 76.8 | 37.8 | 49.1 | 46.0 | 54.2 | 14.8 | 23.6 | 54.4 | 67.8 |
| 检索增强推理 |  |  |  |  |  |  |  |  |  |  |  |  |
| RAG-Qwen2.5-32B | 33.4 | 49.3 | 65.8 | 79.2 | 38.6 | 50.4 | 31.6 | 40.6 | 10.4 | 19.8 | 52.0 | 66.0 |
| RAG-QwQ-32B | 29.6 | 44.4 | 65.6 | 77.6 | 34.2 | 46.4 | 35.6 | 46.2 | 10.6 | 20.2 | 55.2 | 67.4 |
| RAgent-Qwen2.5-32B | 32.4 | 47.8 | 63.0 | 72.6 | 44.6 | 56.8 | 55.4 | 69.7 | 13.0 | 25.4 | 54.4 | 66.4 |
| RAgent-QwQ-32B | 33.6 | 48.4 | 62.0 | 74.0 | 43.0 | 55.2 | 58.4 | 71.2 | 13.6 | 25.5 | 52.0 | 64.7 |
| 带 Reason-in-Documents 的检索增强推理 |  |  |  |  |  |  |  |  |  |  |  |  |
| Search-o1（本文） | 34.0 | 49.7 | 63.4 | 74.1 | 45.2 | 57.3 | 58.0 | 71.4 | 16.6 | 28.2 | 56.0 | 67.8 |

## 5 结论

本工作中，我们提出 Search-o1——一个通过整合智能体检索增强生成机制与 Reason-in-Documents 模块来解决大型推理模型（LRM）固有知识不足的框架。我们的方法使 LRM 能在推理过程中自主检索并无缝纳入外部知识，从而提升其长步骤推理能力的准确性与连贯性。在科学、数学与编程等多样复杂推理任务以及多个开放域问答基准上的全面实验表明，Search-o1 持续优于既有的检索增强与直接推理方法。值得注意的是，Search-o1 不仅在处理复杂推理挑战上超过基线模型，还在特定领域取得与人类专家相当或更高的表现水平。这些发现凸显了 Search-o1 显著提升 LRM 可靠性与通用性的潜力，为复杂问题求解场景中更可信、更有效的智能系统铺平道路。

## 参考文献

- [1]

  Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi.
  Self-rag: Learning to retrieve, generate, and critique through self-reflection.
  arXiv preprint arXiv:2310.11511, 2023.
- [2]

  Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei.
  Language models are few-shot learners.
  In Hugo Larochelle, Marc'Aurelio Ranzato, Raia Hadsell, Maria-Florina Balcan, and Hsuan-Tien Lin, editors, Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual, 2020.
- [3]

  Junying Chen, Zhenyang Cai, Ke Ji, Xidong Wang, Wanlong Liu, Rongsheng Wang, Jianye Hou, and Benyou Wang.
  Huatuogpt-o1, towards medical complex reasoning with llms.
  arXiv preprint arXiv:2412.18925, 2024.
- [4]

  Xingyu Chen, Jiahao Xu, Tian Liang, Zhiwei He, Jianhui Pang, Dian Yu, Linfeng Song, Qiuzhi Liu, Mengfei Zhou, Zhuosheng Zhang, Rui Wang, Zhaopeng Tu, Haitao Mi, and Dong Yu.
  Do not think that much for 2+3=? on the overthinking of o1-like llms, 2024.
- [5]

  Zehui Chen, Kuikun Liu, Qiuchen Wang, Jiangning Liu, Wenwei Zhang, Kai Chen, and Feng Zhao.
  Mindsearch: Mimicking human minds elicits deep ai searcher.
  arXiv preprint arXiv:2407.20183, 2024.
- [6]

  Kahneman Daniel.
  Thinking, fast and slow.
  2017.
- [7]

  DeepSeek-AI.
  Deepseek-r1-lite-preview is now live: unleashing supercharged reasoning power!, November 2024.
- [8]

  Guanting Dong, Keming Lu, Chengpeng Li, Tingyu Xia, Bowen Yu, Chang Zhou, and Jingren Zhou.
  Self-play with execution feedback: Improving instruction-following capabilities of large language models.
  CoRR, abs/2406.13542, 2024.
- [9]

  Guanting Dong, Xiaoshuai Song, Yutao Zhu, Runqi Qiao, Zhicheng Dou, and Ji-Rong Wen.
  Toward general instruction-following alignment for retrieval-augmented generation.
  CoRR, abs/2410.09584, 2024.
- [10]

  Guanting Dong, Hongyi Yuan, Keming Lu, Chengpeng Li, Mingfeng Xue, Dayiheng Liu, Wei Wang, Zheng Yuan, Chang Zhou, and Jingren Zhou.
  How abilities in large language models are affected by supervised fine-tuning data composition.
  In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors, Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2024, Bangkok, Thailand, August 11-16, 2024, pages 177–198. Association for Computational Linguistics, 2024.
- [11]

  Guanting Dong, Chenghao Zhang, Mengjie Deng, Yutao Zhu, Zhicheng Dou, and Ji-Rong Wen.
  Progressive multimodal reasoning via active retrieval.
  arXiv preprint arXiv:2412.14835, 2024.
- [12]

  Guanting Dong, Yutao Zhu, Chenghao Zhang, Zechen Wang, Zhicheng Dou, and Ji-Rong Wen.
  Understand what LLM needs: Dual preference alignment for retrieval-augmented generation.
  CoRR, abs/2406.18676, 2024.
- [13]

  Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al.
  The llama 3 herd of models.
  arXiv preprint arXiv:2407.21783, 2024.
- [14]

  Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, and Jonathan Larson.
  From local to global: A graph rag approach to query-focused summarization, 2024.
- [15]

  Guhao Feng, Bohang Zhang, Yuntian Gu, Haotian Ye, Di He, and Liwei Wang.
  Towards revealing the mystery behind chain of thought: a theoretical perspective.
  Advances in Neural Information Processing Systems, 36, 2024.
- [16]

  Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt.
  Measuring mathematical problem solving with the MATH dataset.
  In Joaquin Vanschoren and Sai-Kit Yeung, editors, Proceedings of the Neural Information Processing Systems Track on Datasets and Benchmarks 1, NeurIPS Datasets and Benchmarks 2021, December 2021, virtual, 2021.
- [17]

  Tom Henighan, Jared Kaplan, Mor Katz, Mark Chen, Christopher Hesse, Jacob Jackson, Heewoo Jun, Tom B Brown, Prafulla Dhariwal, Scott Gray, et al.
  Scaling laws for autoregressive generative modeling.
  arXiv preprint arXiv:2010.14701, 2020.
- [18]

  Xanh Ho, Anh-Khoa Duong Nguyen, Saku Sugawara, and Akiko Aizawa.
  Constructing A multi-hop QA dataset for comprehensive evaluation of reasoning steps.
  In Donia Scott, Núria Bel, and Chengqing Zong, editors, Proceedings of the 28th International Conference on Computational Linguistics, COLING 2020, Barcelona, Spain (Online), December 8-13, 2020, pages 6609–6625. International Committee on Computational Linguistics, 2020.
- [19]

  Zhen Huang, Haoyang Zou, Xuefeng Li, Yixiu Liu, Yuxiang Zheng, Ethan Chern, Shijie Xia, Yiwei Qin, Weizhe Yuan, and Pengfei Liu.
  O1 replication journey–part 2: Surpassing o1-preview through simple distillation, big progress or bitter lesson?
  arXiv preprint arXiv:2411.16489, 2024.
- [20]

  Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang, Bowen Yu, Kai Dang, An Yang, Rui Men, Fei Huang, Xingzhang Ren, Xuancheng Ren, Jingren Zhou, and Junyang Lin.
  Qwen2.5-coder technical report.
  CoRR, abs/2409.12186, 2024.
- [21]

  Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, et al.
  Gpt-4o system card.
  arXiv preprint arXiv:2410.21276, 2024.
- [22]

  Aaron Jaech, Adam Kalai, Adam Lerer, Adam Richardson, Ahmed El-Kishky, Aiden Low, Alec Helyar, Aleksander Madry, Alex Beutel, Alex Carney, et al.
  Openai o1 system card.
  arXiv preprint arXiv:2412.16720, 2024.
- [23]

  Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica.
  Livecodebench: Holistic and contamination free evaluation of large language models for code.
  CoRR, abs/2403.07974, 2024.
- [24]

  Huiqiang Jiang, Qianhui Wu, Xufang Luo, Dongsheng Li, Chin-Yew Lin, Yuqing Yang, and Lili Qiu.
  Longllmlingua: Accelerating and enhancing llms in long context scenarios via prompt compression.
  arXiv preprint arXiv:2310.06839, 2023.
- [25]

  Jinhao Jiang, Zhipeng Chen, Yingqian Min, Jie Chen, Xiaoxue Cheng, Jiapeng Wang, Yiru Tang, Haoxiang Sun, Jia Deng, Wayne Xin Zhao, et al.
  Technical report: Enhancing llm reasoning with reward-guided tree search.
  arXiv preprint arXiv:2411.11694, 2024.
- [26]

  Bowen Jin, Jinsung Yoon, Jiawei Han, and Sercan Ö. Arik.
  Long-context llms meet RAG: overcoming challenges for long inputs in RAG.
  CoRR, abs/2410.05983, 2024.
- [27]

  Jiajie Jin, Yutao Zhu, Yujia Zhou, and Zhicheng Dou.
  Bider: Bridging knowledge inconsistency for efficient retrieval-augmented llms via key supporting evidence.
  arXiv preprint arXiv:2402.12174, 2024.
- [28]

  Mandar Joshi, Eunsol Choi, Daniel Weld, and Luke Zettlemoyer.
  TriviaQA: A large scale distantly supervised challenge dataset for reading comprehension.
  In ACL, pages 1601–1611, Vancouver, Canada, July 2017. Association for Computational Linguistics.
- [29]

  Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, et al.
  Natural questions: a benchmark for question answering research.
  Transactions of the Association for Computational Linguistics, 7:453–466, 2019.
- [30]

  Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al.
  Retrieval-augmented generation for knowledge-intensive nlp tasks.
  Advances in Neural Information Processing Systems, 33:9459–9474, 2020.
- [31]

  Aitor Lewkowycz, Anders Andreassen, David Dohan, Ethan Dyer, Henryk Michalewski, Vinay V. Ramasesh, Ambrose Slone, Cem Anil, Imanol Schlag, Theo Gutman-Solo, Yuhuai Wu, Behnam Neyshabur, Guy Gur-Ari, and Vedant Misra.
  Solving quantitative reasoning problems with language models.
  In Sanmi Koyejo, S. Mohamed, A. Agarwal, Danielle Belgrave, K. Cho, and A. Oh, editors, Advances in Neural Information Processing Systems 35: Annual Conference on Neural Information Processing Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022, 2022.
- [32]

  Chengpeng Li, Guanting Dong, Mingfeng Xue, Ru Peng, Xiang Wang, and Dayiheng Liu.
  Dotamath: Decomposition of thought with code assistance and self-correction for mathematical reasoning.
  CoRR, abs/2407.04078, 2024.
- [33]

  Xiaoxi Li, Zhicheng Dou, Yujia Zhou, and Fangchao Liu.
  Corpuslm: Towards a unified language model on corpus for knowledge-intensive tasks.
  In Grace Hui Yang, Hongning Wang, Sam Han, Claudia Hauff, Guido Zuccon, and Yi Zhang, editors, Proceedings of the 47th International ACM SIGIR Conference on Research and Development in Information Retrieval, SIGIR 2024, Washington DC, USA, July 14-18, 2024, pages 26–37. ACM, 2024.
- [34]

  Xiaoxi Li, Jiajie Jin, Yujia Zhou, Yongkang Wu, Zhonghua Li, Qi Ye, and Zhicheng Dou.
  Retrollm: Empowering large language models to retrieve fine-grained evidence within generation.
  arXiv preprint arXiv:2412.11919, 2024.
- [35]

  Xiaoxi Li, Jiajie Jin, Yujia Zhou, Yuyao Zhang, Peitian Zhang, Yutao Zhu, and Zhicheng Dou.
  From matching to generation: A survey on generative information retrieval.
  CoRR, abs/2404.14851, 2024.
- [36]

  Xiaoxi Li, Yujia Zhou, and Zhicheng Dou.
  Unigen: A unified generative framework for retrieval and question answering with large language models.
  In Michael J. Wooldridge, Jennifer G. Dy, and Sriraam Natarajan, editors, Thirty-Eighth AAAI Conference on Artificial Intelligence, AAAI 2024, Thirty-Sixth Conference on Innovative Applications of Artificial Intelligence, IAAI 2024, Fourteenth Symposium on Educational Advances in Artificial Intelligence, EAAI 2014, February 20-27, 2024, Vancouver, Canada, pages 8688–8696. AAAI Press, 2024.
- [37]

  Lei Liang, Mengshu Sun, Zhengke Gui, Zhongshu Zhu, Zhouyu Jiang, Ling Zhong, Yuan Qu, Peilong Zhao, Zhongpu Bo, Jin Yang, Huaidong Xiong, Lin Yuan, Jun Xu, Zaoyang Wang, Zhiqiang Zhang, Wen Zhang, Huajun Chen, Wenguang Chen, and Jun Zhou.
  Kag: Boosting llms in professional domains via knowledge augmented generation, 2024.
- [38]

  Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe.
  Let's verify step by step.
  In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024.
- [39]

  Bill Yuchen Lin, Abhilasha Ravichander, Ximing Lu, Nouha Dziri, Melanie Sclar, Khyathi Raghavi Chandu, Chandra Bhagavatula, and Yejin Choi.
  The unlocking spell on base llms: Rethinking alignment via in-context learning.
  In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024.
- [40]

  Zhan Ling, Yunhao Fang, Xuanlin Li, Zhiao Huang, Mingu Lee, Roland Memisevic, and Hao Su.
  Deductive verification of chain-of-thought reasoning.
  In Alice Oh, Tristan Naumann, Amir Globerson, Kate Saenko, Moritz Hardt, and Sergey Levine, editors, Advances in Neural Information Processing Systems 36: Annual Conference on Neural Information Processing Systems 2023, NeurIPS 2023, New Orleans, LA, USA, December 10 - 16, 2023, 2023.
- [41]

  Jingyu Liu, Jiaen Lin, and Yong Liu.
  How much can RAG help the reasoning of llm?
  CoRR, abs/2410.02338, 2024.
- [42]

  Jingyu Liu, Jiaen Lin, and Yong Liu.
  How much can RAG help the reasoning of llm?
  CoRR, abs/2410.02338, 2024.
- [43]

  Xinbei Ma, Yeyun Gong, Pengcheng He, Hai Zhao, and Nan Duan.
  Query rewriting for retrieval-augmented large language models.
  arXiv preprint arXiv:2305.14283, 2023.
- [44]

  Ning Miao, Yee Whye Teh, and Tom Rainforth.
  Selfcheck: Using llms to zero-shot check their own step-by-step reasoning.
  In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024.
- [45]

  Yingqian Min, Zhipeng Chen, Jinhao Jiang, Jie Chen, Jia Deng, Yiwen Hu, Yiru Tang, Jiapeng Wang, Xiaoxue Cheng, Huatong Song, et al.
  Imitate, explore, and self-improve: A reproduction report on slow-thinking reasoning systems.
  arXiv preprint arXiv:2412.09413, 2024.
- [46]

  OpenAI.
  Learning to reason with llms, 2024.
- [47]

  Ofir Press, Muru Zhang, Sewon Min, Ludwig Schmidt, Noah A. Smith, and Mike Lewis.
  Measuring and narrowing the compositionality gap in language models.
  In Houda Bouamor, Juan Pino, and Kalika Bali, editors, Findings of the Association for Computational Linguistics: EMNLP 2023, Singapore, December 6-10, 2023, pages 5687–5711. Association for Computational Linguistics, 2023.
- [48]

  Runqi Qiao, Qiuna Tan, Guanting Dong, Minhui Wu, Chong Sun, Xiaoshuai Song, Zhuoma Gongque, Shanglin Lei, Zhe Wei, Miaoxuan Zhang, Runfeng Qiao, Yifan Zhang, Xiao Zong, Yida Xu, Muxi Diao, Zhimin Bao, Chen Li, and Honggang Zhang.
  We-math: Does your large multimodal model achieve human-like mathematical reasoning?
  CoRR, abs/2407.01284, 2024.
- [49]

  Yiwei Qin, Xuefeng Li, Haoyang Zou, Yixiu Liu, Shijie Xia, Zhen Huang, Yixin Ye, Weizhe Yuan, Hector Liu, Yuanzhi Li, et al.
  O1 replication journey: A strategic progress report–part 1.
  arXiv preprint arXiv:2410.18982, 2024.
- [50]

  Qwen, :, An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, Huan Lin, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Yang, Jiaxi Yang, Jingren Zhou, Junyang Lin, Kai Dang, Keming Lu, Keqin Bao, Kexin Yang, Le Yu, Mei Li, Mingfeng Xue, Pei Zhang, Qin Zhu, Rui Men, Runji Lin, Tianhao Li, Tingyu Xia, Xingzhang Ren, Xuancheng Ren, Yang Fan, Yang Su, Yichang Zhang, Yu Wan, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, and Zihan Qiu.
  Qwen2.5 technical report, 2024.
- [51]

  Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J. Liu.
  Exploring the limits of transfer learning with a unified text-to-text transformer.
  J. Mach. Learn. Res., 21:140:1–140:67, 2020.
- [52]

  David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian Michael, and Samuel R. Bowman.
  GPQA: A graduate-level google-proof q&a benchmark.
  CoRR, abs/2311.12022, 2023.
- [53]

  Jiejun Tan, Zhicheng Dou, Yutao Zhu, Peidong Guo, Kun Fang, and Ji-Rong Wen.
  Small models, big insights: Leveraging slim proxy models to decide when and what to retrieve for llms.
  arXiv preprint arXiv:2402.12052, 2024.
- [54]

  Qwen Team.
  Qwq: Reflect deeply on the boundaries of the unknown, November 2024.
- [55]

  Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal.
  ♫ musique: Multihop questions via single-hop question composition.
  Transactions of the Association for Computational Linguistics, 10:539–554, 2022.
- [56]

  Prakhar Verma, Sukruta Prakash Midigeshi, Gaurav Sinha, Arno Solin, Nagarajan Natarajan, and Amit Sharma.
  Planxrag: Planning-guided retrieval augmented generation.
  arXiv preprint arXiv:2410.20753, 2024.
- [57]

  Jiaan Wang, Fandong Meng, Yunlong Liang, and Jie Zhou.
  Drt-o1: Optimized deep reasoning translation via long chain-of-thought.
  arXiv preprint arXiv:2412.17498, 2024.
- [58]

  Liang Wang, Nan Yang, and Furu Wei.
  Query2doc: Query expansion with large language models.
  arXiv preprint arXiv:2303.07678, 2023.
- [59]

  Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al.
  Chain-of-thought prompting elicits reasoning in large language models.
  Advances in neural information processing systems, 35:24824–24837, 2022.
- [60]

  Ken C. L. Wong, Hongzhi Wang, Etienne E. Vos, Bianca Zadrozny, Campbell D. Watson, and Tanveer F. Syeda-Mahmood.
  Addressing deep learning model uncertainty in long-range climate forecasting with late fusion.
  CoRR, abs/2112.05254, 2021.
- [61]

  Siwei Wu, Zhongyuan Peng, Xinrun Du, Tuney Zheng, Minghao Liu, Jialong Wu, Jiachen Ma, Yizhi Li, Jian Yang, Wangchunshu Zhou, Qunshu Lin, Junbo Zhao, Zhaoxiang Zhang, Wenhao Huang, Ge Zhang, Chenghua Lin, and Jiaheng Liu.
  A comparative study on reasoning patterns of openai's o1 model.
  CoRR, abs/2410.13639, 2024.
- [62]

  Siye Wu, Jian Xie, Jiangjie Chen, Tinghui Zhu, Kai Zhang, and Yanghua Xiao.
  How easily do irrelevant inputs skew the responses of large language models?, 2024.
- [63]

  Shijie Xia, Xuefeng Li, Yixin Liu, Tongshuang Wu, and Pengfei Liu.
  Evaluating mathematical reasoning beyond accuracy.
  CoRR, abs/2404.05692, 2024.
- [64]

  Fangyuan Xu, Weijia Shi, and Eunsol Choi.
  Recomp: Improving retrieval-augmented lms with compression and selective augmentation.
  arXiv preprint arXiv:2310.04408, 2023.
- [65]

  Guowei Xu, Peng Jin, Li Hao, Yibing Song, Lichao Sun, and Li Yuan.
  Llava-o1: Let vision language models reason step-by-step.
  arXiv preprint arXiv:2411.10440, 2024.
- [66]

  An Yang, Baosong Yang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Zhou, Chengpeng Li, Chengyuan Li, Dayiheng Liu, Fei Huang, Guanting Dong, Haoran Wei, Huan Lin, Jialong Tang, Jialin Wang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Ma, Jianxin Yang, Jin Xu, Jingren Zhou, Jinze Bai, Jinzheng He, Junyang Lin, Kai Dang, Keming Lu, Keqin Chen, Kexin Yang, Mei Li, Mingfeng Xue, Na Ni, Pei Zhang, Peng Wang, Ru Peng, Rui Men, Ruize Gao, Runji Lin, Shijie Wang, Shuai Bai, Sinan Tan, Tianhang Zhu, Tianhao Li, Tianyu Liu, Wenbin Ge, Xiaodong Deng, Xiaohuan Zhou, Xingzhang Ren, Xinyu Zhang, Xipin Wei, Xuancheng Ren, Xuejing Liu, Yang Fan, Yang Yao, Yichang Zhang, Yu Wan, Yunfei Chu, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, Zhifang Guo, and Zhihao Fan.
  Qwen2 technical report.
  CoRR, abs/2407.10671, 2024.
- [67]

  An Yang, Beichen Zhang, Binyuan Hui, Bofei Gao, Bowen Yu, Chengpeng Li, Dayiheng Liu, Jianhong Tu, Jingren Zhou, Junyang Lin, Keming Lu, Mingfeng Xue, Runji Lin, Tianyu Liu, Xingzhang Ren, and Zhenru Zhang.
  Qwen2.5-math technical report: Toward mathematical expert model via self-improvement.
  CoRR, abs/2409.12122, 2024.
- [68]

  Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William Cohen, Ruslan Salakhutdinov, and Christopher D. Manning.
  HotpotQA: A dataset for diverse, explainable multi-hop question answering.
  In EMNLP, pages 2369–2380, Brussels, Belgium, October-November 2018. Association for Computational Linguistics.
- [69]

  Huanjin Yao, Jiaxing Huang, Wenhao Wu, Jingyi Zhang, Yibo Wang, Shunyu Liu, Yingjie Wang, Yuxin Song, Haocheng Feng, Li Shen, et al.
  Mulberry: Empowering mllm with o1-like reasoning and reflection via collective monte carlo tree search.
  arXiv preprint arXiv:2412.18319, 2024.
- [70]

  Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao.
  React: Synergizing reasoning and acting in language models.
  arXiv preprint arXiv:2210.03629, 2022.
- [71]

  Tian Ye, Zicheng Xu, Yuanzhi Li, and Zeyuan Allen-Zhu.
  Physics of language models: Part 2.2, how to learn from mistakes on grade-school math problems.
  arXiv preprint arXiv:2408.16293, 2024.
- [72]

  Ori Yoran, Tomer Wolfson, Ori Ram, and Jonathan Berant.
  Making retrieval-augmented language models robust to irrelevant context.
  In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024.
- [73]

  Longhui Yu, Weisen Jiang, Han Shi, Jincheng Yu, Zhengying Liu, Yu Zhang, James T. Kwok, Zhenguo Li, Adrian Weller, and Weiyang Liu.
  Metamath: Bootstrap your own mathematical questions for large language models.
  In The Twelfth International Conference on Learning Representations, ICLR 2024, Vienna, Austria, May 7-11, 2024. OpenReview.net, 2024.
- [74]

  Zheng Yuan, Hongyi Yuan, Chengpeng Li, Guanting Dong, Chuanqi Tan, and Chang Zhou.
  Scaling relationship on learning mathematical reasoning with large language models.
  CoRR, abs/2308.01825, 2023.
- [75]

  Eric Zelikman, Georges Harik, Yijia Shao, Varuna Jayasiri, Nick Haber, and Noah D Goodman.
  Quiet-star: Language models can teach themselves to think before speaking.
  arXiv preprint arXiv:2403.09629, 2024.
- [76]

  Zhiyuan Zeng, Qinyuan Cheng, Zhangyue Yin, Bo Wang, Shimin Li, Yunhua Zhou, Qipeng Guo, Xuanjing Huang, and Xipeng Qiu.
  Scaling of search and learning: A roadmap to reproduce o1 from reinforcement learning perspective.
  arXiv preprint arXiv:2412.14135, 2024.
- [77]

  Di Zhang, Jianbo Wu, Jingdi Lei, Tong Che, Jiatong Li, Tong Xie, Xiaoshui Huang, Shufei Zhang, Marco Pavone, Yuqiang Li, Wanli Ouyang, and Dongzhan Zhou.
  Llama-berry: Pairwise optimization for o1-like olympiad-level mathematical reasoning.
  CoRR, abs/2410.02884, 2024.
- [78]

  Jiayi Zhang, Jinyu Xiang, Zhaoyang Yu, Fengwei Teng, Xionghui Chen, Jiaqi Chen, Mingchen Zhuge, Xin Cheng, Sirui Hong, Jinlin Wang, et al.
  Aflow: Automating agentic workflow generation.
  arXiv preprint arXiv:2410.10762, 2024.
- [79]

  Yue Zhang, Yafu Li, Leyang Cui, Deng Cai, Lemao Liu, Tingchen Fu, Xinting Huang, Enbo Zhao, Yu Zhang, Yulong Chen, Longyue Wang, Anh Tuan Luu, Wei Bi, Freda Shi, and Shuming Shi.
  Siren's song in the AI ocean: A survey on hallucination in large language models.
  CoRR, abs/2309.01219, 2023.
- [80]

  Yuxiang Zhang, Shangxi Wu, Yuqi Yang, Jiangming Shu, Jinlin Xiao, Chao Kong, and Jitao Sang.
  o1-coder: an o1 replication for coding.
  CoRR, abs/2412.00154, 2024.
- [81]

  Yuxiang Zhang, Shangxi Wu, Yuqi Yang, Jiangming Shu, Jinlin Xiao, Chao Kong, and Jitao Sang.
  o1-coder: an o1 replication for coding.
  arXiv preprint arXiv:2412.00154, 2024.
- [82]

  Penghao Zhao, Hailin Zhang, Qinhan Yu, Zhengren Wang, Yunteng Geng, Fangcheng Fu, Ling Yang, Wentao Zhang, and Bin Cui.
  Retrieval-augmented generation for ai-generated content: A survey.
  arXiv preprint arXiv:2402.19473, 2024.
- [83]

  Chujie Zheng, Zhenru Zhang, Beichen Zhang, Runji Lin, Keming Lu, Bowen Yu, Dayiheng Liu, Jingren Zhou, and Junyang Lin.
  Processbench: Identifying process errors in mathematical reasoning.
  arXiv preprint arXiv:2412.06559, 2024.
- [84]

  Tianyang Zhong, Zhengliang Liu, Yi Pan, Yutong Zhang, Yifan Zhou, Shizhe Liang, Zihao Wu, Yanjun Lyu, Peng Shu, Xiaowei Yu, Chao Cao, Hanqi Jiang, Hanxu Chen, Yiwei Li, Junhao Chen, Huawen Hu, Yihen Liu, Huaqin Zhao, Shaochen Xu, Haixing Dai, Lin Zhao, Ruidong Zhang, Wei Zhao, Zhenyuan Yang, Jingyuan Chen, Peilong Wang, Wei Ruan, Hui Wang, Huan Zhao, Jing Zhang, Yiming Ren, Shihuan Qin, Tong Chen, Jiaxi Li, Arif Hassan Zidan, Afrar Jahin, Minheng Chen, Sichen Xia, Jason Holmes, Yan Zhuang, Jiaqi Wang, Bochen Xu, Weiran Xia, Jichao Yu, Kaibo Tang, Yaxuan Yang, Bolun Sun, Tao Yang, Guoyu Lu, Xianqiao Wang, Lilong Chai, He Li, Jin Lu, Lichao Sun, Xin Zhang, Bao Ge, Xintao Hu, Lian Zhang, Hua Zhou, Lu Zhang, Shu Zhang, Ninghao Liu, Bei Jiang, Linglong Kong, Zhen Xiang, Yudan Ren, Jun Liu, Xi Jiang, Yu Bao, Wei Zhang, Xiang Li, Gang Li, Wei Liu, Dinggang Shen, Andrea Sikora, Xiaoming Zhai, Dajiang Zhu, and Tianming Liu.
  Evaluation of openai o1: Opportunities and challenges of AGI.
  CoRR, abs/2409.18486, 2024.
- [85]

  Tianyang Zhong, Zhengliang Liu, Yi Pan, Yutong Zhang, Yifan Zhou, Shizhe Liang, Zihao Wu, Yanjun Lyu, Peng Shu, Xiaowei Yu, et al.
  Evaluation of openai o1: Opportunities and challenges of agi.
  arXiv preprint arXiv:2409.18486, 2024.
- [86]

  Yujia Zhou, Yan Liu, Xiaoxi Li, Jiajie Jin, Hongjin Qian, Zheng Liu, Chaozhuo Li, Zhicheng Dou, Tsung-Yi Ho, and Philip S. Yu.
  Trustworthiness in retrieval-augmented generation systems: A survey.
  CoRR, abs/2409.10102, 2024.
- [87]

  Yujia Zhou, Zheng Liu, and Zhicheng Dou.
  Assistrag: Boosting the potential of large language models with an intelligent information assistant.
  CoRR, abs/2411.06805, 2024.
- [88]

  Yujia Zhou, Zheng Liu, Jiajie Jin, Jian-Yun Nie, and Zhicheng Dou.
  Metacognitive retrieval-augmented large language models.
  In Tat-Seng Chua, Chong-Wah Ngo, Ravi Kumar, Hady W. Lauw, and Roy Ka-Wei Lee, editors, Proceedings of the ACM on Web Conference 2024, WWW 2024, Singapore, May 13-17, 2024, pages 1453–1463. ACM, 2024.

## 附录 A 指令模板

### A.1 Search-o1 的指令

Instruction for Search-o1

You are a reasoning assistant with the ability to perform web searches to help you answer the user's question accurately. You have special tools:

To perform a search: write <|begin_search_query|> your query here <|end_search_query|>.

Then, the system will search and analyze relevant web pages, then provide you with helpful information in the format <|begin_search_result|> …search results… <|end_search_result|>.

You can repeat the search process multiple times if necessary. The maximum number of search attempts is limited to {MAX_SEARCH_LIMIT}.

Once you have all the information you need, continue your reasoning.

Example:

Question: "…"

Assistant thinking steps:

- I might need to look up details about …

Assistant:

<|begin_search_query|>…<|end_search_query|>

(System returns processed information from relevant web pages)

Assistant continues reasoning with the new information…

Remember:

- Use <|begin_search_query|> to request a web search and end with <|end_search_query|>.

- When done searching, continue your reasoning.

Instruction for Reason-in-Documents

Task Instruction:

You are tasked with reading and analyzing web pages based on the following inputs: Previous Reasoning Steps, Current Search Query, and Searched Web Pages. Your objective is to extract relevant and helpful information for Current Search Query from the Searched Web Pages and seamlessly integrate this information into the Previous Reasoning Steps to continue reasoning for the original question.

Guidelines:

1. Analyze the Searched Web Pages:

- Carefully review the content of each searched web page.

- Identify factual information that is relevant to the Current Search Query and can aid in the reasoning process for the original question.

2. Extract Relevant Information:

- Select the information from the Searched Web Pages that directly contributes to advancing the Previous Reasoning Steps.

- Ensure that the extracted information is accurate and relevant.

3. Output Format:

- If the web pages provide helpful information for current search query: Present the information beginning with 'Final Information' as shown below.

Final Information

[Helpful information]

- If the web pages do not provide any helpful information for current search query: Output the following text.

Final Information

No helpful information found.

Inputs:

- Previous Reasoning Steps:

{prev_reasoning}

- Current Search Query:

{search_query}

- Searched Web Pages:

{document}

Now you should analyze each web page and find helpful information based on the current search query "{search_query}" and previous reasoning steps.

### A.2 标准 RAG 的指令

Instruction for Standard RAG

You are a knowledgeable assistant that utilizes the provided documents to answer the user's question accurately.
Question:
{question}
Documents:
{documents}
Guidelines:
- Analyze the provided documents to extract relevant information. Synthesize the information to formulate a coherent and accurate answer.
- Ensure that your response directly addresses the user's question using the information from the documents.

### A.3 RAG 智能体的指令

Instruction for RAG Agent

You are a reasoning assistant with the ability to perform web searches and retrieve webpage content to help you answer the user's question accurately. You have special tools:
- To perform a search: Write '<|begin_search_query|>' your query here '<|end_search_query|>'.
The system will call the web search API with your query and return the search results in the format '<|begin_search_result|> …search results… <|end_search_result|>'.
The search results will include a list of webpages with titles, URLs, and snippets (but not full content).
- To retrieve full page content: After receiving the search results, if you need more detailed information from specific URLs, write '<|begin_url|> url1, url2, … <|end_url|>'.
The system will fetch the full page content of those URLs and return it as '<|begin_full_page|> …full page content… <|end_full_page|>'.
You can repeat the search process multiple times if necessary. The maximum number of search attempts is limited to {MAX_SEARCH_LIMIT}.
You can fetch up to {MAX_URL_FETCH} URLs for detailed information.
Once you have all the information you need, continue your reasoning.
Example:
Question: "…"
Assistant thinking steps:
- I need to find out …
Assistant:
'<|begin_search_query|>…<|end_search_query|>'
(System returns search results)
Assistant:
'<|begin_search_result|> …search results without full page… <|end_search_result|>'
Assistant thinks: The search results mention several URLs. I want full details from one of them.
Assistant:
'<|begin_url|>http://…<|end_url|>'
(System returns full page content)
Assistant:
'<|begin_full_page|> …full page content… <|end_full_page|>'
Now the assistant has enough information and can continue reasoning.
Remember:
- Use '<|begin_search_query|>' to request a web search and end with '<|end_search_query|>'.
- Use '<|begin_url|>' to request full page content and end with '<|end_url|>'.
- When done retrieving information, continue your reasoning.

### A.4 任务专属指令

#### A.4.1 开放域问答任务指令

Instruction for Open-Domain QA Tasks

Please answer the following question.
You should provide your final answer in the format \boxed{YOUR_ANSWER}.
Question:
{question}

#### A.4.2 数学任务指令

Instruction for Math Tasks

Please answer the following math question.
You should provide your final answer in the format \boxed{YOUR_ANSWER}.
Question:
{question}

#### A.4.3 多项选择任务指令

Instruction for Multi-choice Tasks

You are to answer the following multiple-choice question by selecting the correct option.
Your final choice should be one of the letters A, B, C, or D. Do not include any answer content beyond the choice letter.
You should provide your final choice in the format \boxed{YOUR_CHOICE}.
Question:
{question}

#### A.4.4 代码任务指令

Instruction for Code Tasks

Generate a correct Python program that passes all tests for the given problem. You should provide your final code within a Python code block using triple backticks.

```
‘‘‘python
# YOUR CODE HERE
‘‘‘
```

Problem Title: {question_title}
Problem Statement:
{question}

### A.5 补充说明

对上述所有指令，我们以用户提示词而非系统提示词的形式输入。A.4 中的任务专属指令用于 QwQ-32B-Preview 模型。对 Qwen2.5-32B-Instruct、Qwen2.5-72B-Instruct 与 Llama3.3-70B-Instruct 等非推理模型，我们在问题前加入思维链提示「You should think step by step to solve it.」，显式地让这些模型在给出最终答案前进行推理。

## 附录 B 案例研究

表 4、表 5 与表 6 分别给出我们的 Search-o1 模型在 GPQA、AMC2023 与 HotpotQA 数据集上的输出示例。模型生成的搜索查询由 <|begin_search_query|> 与 <|end_search_query|> 包裹，精炼后的搜索结果由 <|begin_search_result|> 与 <|end_search_result|> 包裹。我们观察到，Reason-in-Documents 机制提供了连贯的信息，有效满足模型当前推理步骤的信息需求，并与先前的推理过程无缝衔接。

表 4：Search-o1 在 GPQA 数据集上的示例，搜索查询与搜索结果中使用的特殊符号分别以绿框和蓝框高亮显示。

| GPQA 数据集示例 #1 |
| --- |
| Question: |
| trans-cinnamaldehyde was treated with methylmagnesium bromide, forming product 1. |
| 1 was treated with pyridinium chlorochromate, forming product 2. |
| 3 was treated with (dimethyl(oxo)-l6-sulfaneylidene)methane in DMSO at elevated temperature, forming product 3. |
| how many carbon atoms are there in product 3? Choices: |
| (A) 10 |
| (B) 11 |
| (C) 14 |
| (D) 12 |
| Labeled Answer: |
| B |
| Model Output by Search-o1 |
| Alright, so I have this problem here about some chemical reactions, and I need to figure out how many carbon atoms are in the final product, which is product 3. Let's break this down step by step. |
| First, there's trans-cinnamaldehyde, and it's being treated with methylmagnesium bromide to form product 1. I know that methylmagnesium bromide is a Grignard reagent, which is nucleophilic and usually adds to carbonyl compounds. So, trans-cinnamaldehyde has a carbonyl group, right? It's an aldehyde, so it has a C=O bond. The Grignard reagent should attack the carbonyl carbon, adding the methyl group and turning the aldehyde into an alcohol, I think. But let me make sure. |
| Wait, maybe I should look up what exactly happens when a Grignard reagent reacts with an aldehyde. Let me try to search for that. |
| <|begin_search_query|> reaction of grignard reagent with aldehyde<|end_search_query|> |
| <|begin_search_result|> Reacting a Grignard reagent with an aldehyde results in the formation of a secondary alcohol, incorporating one additional carbon atom from the Grignard reagent. Therefore, if trans-cinnamaldehyde (9 carbon atoms) reacts with methylmagnesium bromide (1 carbon atom), the resulting product (product 1) will have 10 carbon atoms. Subsequent protonation to form product 2 and further reactions to form product 3 do not change the carbon atom count, assuming no carbon is added or removed in those steps. Hence, product 3 should have 10 carbon atoms.<|end_search_result|> |
| Hmm, according to this, product 1 should have 10 carbon atoms, starting from trans-cinnamaldehyde, which has 9 carbon atoms, plus the methyl group from the Grignard reagent, adding one more carbon atom. That makes sense. |
| Next, product 1 is treated with pyridinium chlorochromate to form product 2. Pyridinium chlorochromate (PCC) is used for oxidations, particularly for oxidizing primary alcohols to aldehydes or secondary alcohols to ketones. Since product 1 is a secondary alcohol (from the previous step), PCC should oxidize it to a ketone. Again, this shouldn't change the number of carbon atoms; it's just changing the functional group. |
| … |
| Alternatively, perhaps the initial trans-cinnamaldehyde has more or fewer carbon atoms than I thought. Let me confirm its structure. |
| <|begin_search_query|> structure of trans-cinnamaldehyde<|end_search_query|> |
| <|begin_search_result|> Trans-cinnamaldehyde, also known as (E)-cinnamaldehyde, has the molecular formula C9H8O. It consists of a phenyl ring connected to a propenal group via a double bond, forming a conjugated system that makes the molecule planar. The structure comprises 9 carbon atoms, 8 hydrogen atoms, and 1 oxygen atom, with the functional groups indicating its reactivity in chemical transformations.<|end_search_result|> |
| Yes, confirmed: trans-cinnamaldehyde has 9 carbon atoms. |
| Now, reacting with methylmagnesium bromide, which provides a methyl group (-CH3), adds one carbon atom, making product 1 have 10 carbon atoms. |
| Then, oxidation with PCC to convert the alcohol to a ketone doesn't change the carbon skeleton, so product 2 still has 10 carbon atoms. |
| … |
| Therefore, starting from 9 carbon atoms in trans-cinnamaldehyde, adding one carbon atom from the Grignard reagent to make 10, and then adding another carbon atom in the cyclopropanation to make 11. |
| So, the final answer is B |

表 5：Search-o1 在 AMC2023 数据集上的示例，搜索查询与搜索结果中使用的特殊符号分别以绿框和蓝框高亮显示。

| AMC2023 数据集示例 #2 |
| --- |
| Question: |
| There is a unique sequence of integers $a_{1},a_{2},\cdots a_{2023}$ such that $\tan 2023x=\frac{a_{1}\tan x+a_{3}\tan^{3}x+a_{5}\tan^{5}x+\cdots+a_{2023}\tan^{2023}x}{1+a_{2}\tan^{2}x+a_{4}\tan^{4}x\cdots+a_{2022}\tan^{2022}x}$ whenever $\tan 2023x$ is defined. What is $a_{2023}$? |
| Labeled Answer: |
| -1 |
| Model Output by Search-o1 |
| Alright, so I've got this problem here involving trigonometric identities, specifically with the tangent function. The equation given is: |
| … |
| And I need to find the value of $a_{2023}$. |
| First off, I know that there are multiple-angle identities for tangent, but I'm not sure if there's a direct formula for such a high multiple like 2023. Maybe there's a general formula for $\tan nx$ in terms of $\tan x$, and perhaps this problem is asking for the coefficients in that expansion. |
| … |
| Wait, I remember that tangent of multiple angles can be expressed using the Bernoulli polynomials or something similar, but I'm not sure. Maybe I need to search for a general formula for $\tan nx$. |
| Let me try to search for ẗangent multiple angle formulaẗo see if there's a general expression. |
| <|begin_search_query|> tangent multiple angle formula<|end_search_query|> |
| <|begin_search_result|> The recursive formula for tan(nθ) is given by:    $\tan(n\theta)=\frac{\tan[(n-1)\theta]+\tan\theta}{1-\tan[(n-1)\theta]\tan\theta}$ This formula can be used iteratively to compute tan(nθ) for any integer n, making it particularly useful for large values of n, such as n=2023, as encountered in the problem. This approach avoids the complexity of deriving high-degree polynomial expressions directly and leverages the tangent addition formula in a step-by-step manner.<|end_search_result|> |
| Okay, so there's a recursive formula for $\tan(n\theta)$:    $\tan(n\theta)=\frac{\tan[(n-1)\theta]+\tan\theta}{1-\tan[(n-1)\theta]\tan\theta}$ That seems useful, especially for large $n$, like 2023. But I'm not sure how to apply this recursively up to 2023 without going through each step, which isn't practical. |
| Maybe there's a general expression for $\tan(nx)$ in terms of $\tan(x)$ as a rational function. |
| … |
| Looking at $n=1$:    $\tan x=\frac{a_{1}\tan x}{1}\implies a_{1}=1$ For $n=3$, $a_{3}=-1$ |
| For $n=5$, $a_{5}=1$ |
| So it seems that $a_{n}=(-1)^{(n-1)/2}$ for odd $n$. |
| Wait, let's check: |
| For $n=1$, $(-1)^{(1-1)/2}=(-1)^{0}=1$, which matches $a_{1}=1$ |
| For $n=3$, $(-1)^{(3-1)/2}=(-1)^{1}=-1$, which matches $a_{3}=-1$ |
| For $n=5$, $(-1)^{(5-1)/2}=(-1)^{2}=1$, which matches $a_{5}=1$ |
| So, generalizing, for odd $n$, $a_{n}=(-1)^{(n-1)/2}$ |
| Now, 2023 is odd, so $a_{2023}=(-1)^{(2023-1)/2}=(-1)^{1011}=-1$ |
| Therefore, $a_{2023}=-1$ |
| I think that's the answer. |
| *Final Answer**    $\boxed{-1}$ |

表 6：Search-o1 在 HotpotQA 数据集上的示例，搜索查询与搜索结果中使用的特殊符号分别以绿框和蓝框高亮显示。

| HotpotQA 数据集示例 #3 |
| --- |
| Question: |
| Were Goo Goo Dolls and Echosmith formed in the same city? |
| Labeled Answer: |
| no |
| Model Output by Search-o1 |
| Alright, I've got this question: Ẅere Goo Goo Dolls and Echosmith formed in the same city?Ḧmm, I don't know much about these bands, so I'll need to look that up. |
| First, I should find out where each band was formed. Maybe start with Goo Goo Dolls. I think they're an older band, but I'm not sure. Let me search for their formation place. |
| <|begin_search_query|> where was Goo Goo Dolls formed?<|end_search_query|> |
| <|begin_search_result|> The Goo Goo Dolls were formed in Buffalo, New York, in 1986. They initially performed under the name Sex Maggots but changed to Goo Goo Dolls in 1986 for a gig, choosing the name from an ad in True Detective magazine. <|end_search_result|> |
| Okay, so Goo Goo Dolls were formed in Buffalo, New York. Now, I need to find out where Echosmith was formed. |
| <|begin_search_query|> where was Echosmith formed?<|end_search_query|> |
| <|begin_search_result|> Echosmith was formed in Chino, California, in February 2009.<|end_search_result|> |
| Chino, California, huh? That sounds different from Buffalo, New York. But maybe I should double-check to make sure I have the right information. |
| Let me look up Echosmith again to confirm their formation city. |
| <|begin_search_query|> Echosmith formation location<|end_search_query|> |
| <|begin_search_result|> Echosmith was formed in Toluca Lake, Los Angeles, California, in February 2009. The initial confusion about the formation location being Chino, California, or Buffalo, New York, is resolved by multiple recent sources confirming their formation in Los Angeles. Chino might be their hometown, but the band was established in Toluca Lake, Los Angeles.<|end_search_result|> |
| Wait, now it says Toluca Lake, Los Angeles, California. Earlier, I had Chino, California. Maybe there's some confusion here. |
| I should check more sources to make sure. |
| <|begin_search_query|> Echosmith origin city<|end_search_query|> |
| <|begin_search_result|> Echosmith was born in Chino, California, but formed the band in Toluca Lake, Los Angeles, California, in February 2009. Chino is their hometown, while Toluca Lake is where they officially formed as a band.<|end_search_result|> |
| So, it seems like Echosmith originates from Chino, California, but was formed in Toluca Lake, Los Angeles, California. |
| Now, comparing that to Goo Goo Dolls, who were formed in Buffalo, New York. |
| Clearly, Buffalo, New York, is different from Toluca Lake, Los Angeles, California. |
| But just to be thorough, maybe there's a connection I'm missing. |
| Let me see if Echosmith has any ties to Buffalo, New York. |
| <|begin_search_query|> Echosmith Buffalo, New York<|end_search_query|> |
| <|begin_search_result|> Echosmith has performed in Buffalo, New York, in the past, as evidenced by a setlist from a concert at Waiting Room on November 1, 2013. However, there are no current tour dates listed for Buffalo in the searched web pages.<|end_search_result|> |
| So, they've played in Buffalo, but that doesn't mean they were formed there. |
| Let me see if there's any other connection between the two bands. |
| <|begin_search_query|> Goo Goo Dolls and Echosmith connection<|end_search_query|><|begin_search_result|>The maximum search limit is exceeded. You are not allowed to search.<|end_search_result|> |
| Hmm, it seems I've reached my search limit. Based on the information I have so far, Goo Goo Dolls were formed in Buffalo, New York, and Echosmith was formed in Toluca Lake, Los Angeles, California. These are different cities, so the answer should be no, they were not formed in the same city. |
| Therefore, I can confidently say that Goo Goo Dolls and Echosmith were not formed in the same city. |
| *Final Answer**    $\boxed{\text{no}}$ |
