---
title: "SWiRL：面向推理与工具使用的合成数据生成与多步 RL"
title_en: "Synthetic Data Generation & Multi-Step RL for Reasoning & Tool Use"
arxiv: 2504.04736
source: https://arxiv.org/abs/2504.04736
crawled: 2026-09-23
translated: 2026-09-23
---

# SWiRL：面向推理与工具使用的合成数据生成与多步 RL


> 原文：[Synthetic Data Generation & Multi-Step RL for Reasoning & Tool Use](https://arxiv.org/abs/2504.04736) · Stanford CS329A 指定阅读

Anna Goldie、Azalia Mirhoseini、Hao Zhou、Irene Cai、Christopher D. Manning（斯坦福大学计算机科学系；Google DeepMind；*同等贡献。邮箱：{agoldie,azalia}@cs.stanford.edu）

###### 摘要

强化学习已被证明能提升大型语言模型的表现。然而，RLHF、RLAIF 等传统方法把问题当作单步来处理。随着重心转向更复杂的推理与智能体任务，语言模型必须先经过多步的文本生成、推理与环境交互，才能给出解。我们提出一种面向多步优化场景的合成数据生成与 RL 方法论。这一称为逐步强化学习（Step-Wise Reinforcement Learning，SWiRL）的方法迭代地生成多步推理与工具使用数据，再从这些数据中学习。它采用一种简单的逐步分解：把每条多步轨迹拆成对应原模型每个行动的多条子轨迹，然后在这些子轨迹上施加合成数据过滤与 RL 优化。我们在多个多步工具使用、问答与数学推理任务上评估了 SWiRL。实验表明，SWiRL 在 GSM8K、HotPotQA、CofCA、MuSiQue 与 BeerQA 上的相对准确率分别比基线方法高出 21.5%、12.3%、14.8%、11.1% 与 15.3%。令人兴奋的是，该方法展现出跨任务的泛化：例如，只在 HotPotQA（文本问答）上训练，就能把 GSM8K（数学数据集）的零样本表现相对提升 16.9%。

## 1 引言

大型语言模型（LLM）已在自然语言处理中展现出卓越能力（Gemini Team et al., 2024；Anthropic, 2024；OpenAI et al., 2024）。然而，它们在回答需要跨多步推理与工具使用的复杂查询时常常力不从心（Wu et al., 2024），例如多跳问答、数学问题求解、编程及其他智能体任务（Yang et al., 2018；Trivedi et al., 2022；Wu et al., 2024；Cobbe et al., 2021；Jimenez et al., 2024；Ehrlich et al., 2025；Li et al., 2022）。

传统强化学习（RL）方法，如人类反馈强化学习（RLHF；Christiano et al., 2023）、AI 反馈强化学习（RLAIF；Bai et al., 2022）与执行反馈强化学习（RLEF；Gehring et al., 2025），都聚焦于单步优化，多步任务的挑战基本未被触及。许多现实问题需要一连串相互关联的行动；例如回答一道难题时，模型不仅要决定寻找什么信息，还要决定何时停止搜索并综合已有发现。多步推理带来复合性挑战：错误的中间步骤往往导致错误的最终结果，因此在整个行动链上保持准确，或学会从这类错误中有效恢复，至关重要。

为应对这一挑战，我们提出逐步强化学习（Step-Wise Reinforcement Learning，SWiRL）——一种离线多步优化技术。我们考虑这样的设定：模型可以访问一个工具（如搜索引擎或计算器），并按需执行一串工具调用来回答问题。我们的目标是教会模型：如何把复杂问题分解为一系列更可管理的子任务、何时调用工具、如何构造对工具的调用、何时利用这些查询的结果回答问题，以及如何有效地综合所得信息。具体而言，我们提出一种两阶段方法：先生成多步合成数据，再用逐步强化学习方法从这些数据中学习。这一方法有一个关键的实用优势：我们可以通过并行调用快速生成大量多步训练数据，避免缓慢的工具执行拖累训练过程。此外，这一离线过程因为有固定数据集而更具可复现性。

为生成多步合成训练数据，我们让一个开源 LLM（Gemma 2（Gemma Team et al., 2024b））访问相关工具（如搜索引擎或计算器）。我们迭代地提示模型生成多步轨迹；每一步，模型可自由生成思维链，并可以调用工具或给出最终答案——我们称之为模型的行动（action）。若模型生成工具调用，其查询会从整体回复中自动抽出并在环境中执行，结果在下一步呈现给模型。当模型生成对原始问题的答案（用特殊标记指示）时，轨迹结束。我们把每条含 $k$ 个行动的轨迹转换为 $k$ 条子轨迹，每条包含从轨迹开头到该行动为止的上下文。然后我们用逐步强化学习方法在该数据集上优化，采用一个在其子轨迹上下文中评估每个行动的生成式奖励模型。

这种细粒度方法使我们能在轨迹的每一步之后施加直接反馈，而且是以具备上下文感知的方式进行。与 DeepSeek-R1（DeepSeek-AI and others, 2025）、Llama-3（Grattafiori et al., 2024）等前沿开源模型所用的既有 RL 微调方法不同，我们不只针对最终表现优化，也不使用金标签（golden label）；但通过优化「给定先前步骤时每一步的合理性」，SWiRL 确实改进了最终表现。

除在具有挑战性的多跳问答与数学问题求解任务上评估 SWiRL 外，我们还研究该方法论的泛化性质。这一点至关重要，因为语言模型的智能体应用正爆发式增长，能在数据集与任务间泛化的方法将更容易、更便宜、更快速地适配新环境。我们还衡量不同合成数据过滤策略的有效性，研究 SWiRL 跨数据集与任务的泛化能力，测度模型规模与数据集规模的影响，并探索驱动这些性能提升的机制。

我们的贡献如下：

- 我们提出逐步强化学习（SWiRL），一种面向多步推理与工具使用的合成数据生成与离线 RL 方法。
- 我们展示了跨数据集的泛化。例如，在 HotPotQA 上训练 SWiRL 不仅改进该数据集本身的表现，也在其他多跳问答数据集上取得更优表现，例如 GSM8K（Cobbe et al., 2021）上 21.5%、BeerQA（Qi et al., 2021b）上 15.3%、MuSiQue（Trivedi et al., 2022）上 11.1%、CofCA（Wu et al., 2024）上 14.8%。
- 我们还展示了跨相异任务的迁移：数学推理到问答、以及反向。只在多跳 HotPotQA 问答上训练，就把 GSM8K（数学数据集）的表现提升 16.9%；而在 GSM8K 上训练，把 HotPotQA（多跳问答）的表现提升 9.2%。
- 我们在多步推理与工具使用设定下分析合成数据过滤策略的影响，并证明模型从「按步过滤以确保高质量推理轨迹、但不按结果（最终答案正确性）过滤」的数据集中学习效果最好。
- 我们探讨训练数据集规模与模型规模对 SWiRL 的影响，观察到仅用 1,000 条轨迹就能取得显著收益；较小模型（Gemma-2-2b 与 9b）能从域内 SWiRL 获益，但不像更大的 Gemma-2-27b 那样展现同样的泛化。
- 我们证明 SWiRL 有效提升平均过程奖励，即便在分布外任务上评估也是如此，说明下游性能收益来自多步推理的改进。

## 2 方法论

我们的方法论——逐步强化学习（SWiRL）——包含两个阶段。第一阶段生成并过滤合成数据。第二阶段用逐步强化学习方法在合成轨迹上优化一个生成式基座模型。SWiRL 不需要金标签或人工标注，而是完全依赖基于模型的判断来完成数据生成、过滤与 RL 优化。方法论的总体流程见图 1（阶段 1）与图 2（阶段 2）。

### 2.1 多步数据收集

![Refer to caption](2504.04736v2/syntheticdata.png)

图 1：在 SWiRL 阶段 1，我们生成并过滤多步合成轨迹。每一步，模型可自由生成思维链、调用搜索器或计算器等工具，并/或给出对原始问题的回答。过程过滤（process-filtered）数据对应每一步都被模型评审（Gemini 1.5 Pro Thinking）判定为合理的轨迹。结果过滤（outcome-filtered）数据对应最终答案与金标签一致的轨迹。

在阶段 1（见图 1），我们生成由多步推理与工具使用构成的合成轨迹，作为下一节所述逐步 RL 方法的训练数据。为汇编大规模合成轨迹集合，我们为语言模型增配一个工具（如搜索引擎或计算器），并迭代提示模型生成多步轨迹。每一步，模型被要求选择调用工具或给出最终答案，并且始终可以自由生成思维链（它通常也确实这么做）。若模型生成工具调用，该调用会从整体回复中解析出来、在环境中执行，其结果在下一步呈现给模型。提示见附录 E，其中包含问题、关于多步工具使用的明确指令，以及此前工具调用的结果。

对每条多步合成轨迹，我们定义如下记号。轨迹本身记为 $\tau=(s_{1},a_{1},\dots,s_{K},a_{K})$。第一个状态 $s_{1}$ 是原始提示。随后每个状态 $s_{i}$ 包含迄今的完整上下文：状态 $s_{i-1}$、行动 $a_{i-1}$，以及环境（工具调用）对 $a_{i-1}$ 的响应。每个行动 $a_{i}$ 是模型在状态 $s_{i}$ 下的回复。最后一个行动 $a_{K}$ 是模型对原始提示的回答。

本工作中，我们编制了一个由 HotPotQA 训练集（Yang et al., 2018）10,000 道多跳问题派生的 50,000 条合成轨迹数据集（即每题 5 条轨迹），以及一个由 GSM8K 训练集（Cobbe et al., 2021）7,500 道问题派生的 37,500 条数学推理合成轨迹数据集。注意，对 HotPotQA 我们剔除了「Easy」问题——它们通常一次搜索即可作答。为防止合成轨迹过长，我们对 HotPotQA 问题设最大步数为 5，对 GSM8K 问题（通常需 2-8 步求解）设为 10。

编制好这些数据集后，我们考虑四种过滤策略并衡量其对性能的影响（图 1）：（1）不过滤；（2）过程过滤：保留每一步在给定此前全部步骤时都被判定为合理的轨迹。具体而言，提示一个模型（我们的例子中是 Gemini 1.5 Pro Thinking）给出二元判断：给定上下文 $s_i$，行动 $a_i$ 是否合理。提示见附录 E。不使用金标签；（3）结果过滤：仅依据最终回复 $a_K$ 是否与金答案一致来选择轨迹；（4）过程加结果过滤：取两种过滤的交集，只保留既有逐步可靠性又有正确最终结果的轨迹。

DeepSeek-R1（DeepSeek-AI and others, 2025）等近期的合成数据蒸馏方法已经证明，按正确结果过滤的合成数据配合单步 RL 与有监督微调（SFT）可以带来良好性能。本工作中，我们试图探索这一模式在多步、工具使用设定下是否成立，并考察结果与过程两类过滤器的影响。与这些先前工作一样，我们观察到按正确性过滤多步轨迹对 SFT 有效，而且实际上是良好性能的关键。但我们发现，与 SFT 不同，SWiRL 甚至能从以错误最终答案收尾的轨迹中学习。事实上，纳入过程过滤数据（不论结果正确与否）带来了我们的最佳结果。

### 2.2 逐步强化学习方法

图 2：在 SWiRL 阶段 2，我们对阶段 1 得到的多步合成轨迹执行逐步 RL。每步包含一个行动，对应一次工具调用或最终回复。模型可在每步自由生成思维链。环境响应被记录在离线生成的合成轨迹的前序步骤中。细粒度反馈由一个生成式奖励模型提供，用于在给定先前上下文的情况下直接对每个行动做 RL 优化。

如图 2 所示，我们提出一种能有效从阶段 1 生成的多步合成轨迹中学习的 RL 方法。在每一步，优化一个基座模型以基于前文预测下一个中间步骤或最终回复。在第 $i$ 步，模型可以访问完整上下文历史，包括原始提示、此前所有模型生成的步骤以及相应的环境响应。

因此，我们的目标函数是逐步奖励的期望和：

$$J(\theta)=E_{s\sim\mathrm{T},~a\sim\pi_{\theta}(s)}\left[R(a|s)\right]$$

其中 $\pi_{\theta}$ 是由 $\theta$ 参数化、经 SWiRL 微调的基座模型（注意我们也用 $\pi_{\theta}$ 生成合成数据）。$\mathrm{T}$ 表示合成多步轨迹中全部状态的集合，即每条轨迹 $\tau$ 内的每个递增状态 $s$。奖励信号 $R(a|s)$ 来自一个生成式奖励模型——我们的实验中是 Gemini 1.5 Pro——它评估给定上下文 $s$ 时生成回复 $a$ 的质量。不使用金标签。

我们用与 Gemma 2 优化人类反馈奖励相同的策略梯度算法（Gemma Team et al., 2024a；Gemma Team et al., 2024b）来优化上述期望奖励。我们这种细粒度、逐步的微调范式，使模型在「每个预测合理性的即时反馈」引导下，同时学习局部决策（下一步预测）与全局轨迹优化（最终回复生成）。

### 2.3 逐步的推理时评估

如图 3 所示，在推理时我们迭代提示模型调用工具或给出最终答案。若模型生成搜索查询（以 <<search_query>> <</search_query>> 标记指示），我们解析出该查询，用 Gecko 模型嵌入，在相应向量数据库中做最近邻检索，并把检索到的文章注入模型的上下文窗口。若模型生成计算器调用（以 <<math_exp>> <</math_exp>> 标记指示），我们解析出数学表达式，用 SymPy 解释器执行，并把计算结果注入上下文窗口。当模型给出答案（以 <<answer>> <</answer>> 标记指示）或达到最大查询数（问答数据集 5 次、数学推理数据集 10 次）时，过程终止。示例轨迹见附录 F。

![Refer to caption](2504.04736v2/swirl-inference.png)

图 3：在推理时，我们迭代提示模型按需（至上限）多次调用工具，然后回答原始用户问题。

## 3 相关工作

面向 LLM 微调的强化学习。一种主流方法——人类反馈强化学习（RLHF；Ouyang et al., 2022；Christiano et al., 2023）——先在回复级的人类偏好标签上训练奖励模型，再用近端策略优化（PPO；Schulman et al., 2017）做 RL 优化。在该框架之上，AI 反馈强化学习（RLAIF；Bai et al., 2022）成为一种可扩展的替代：利用 AI 模型依据预定义原则或宪法生成反馈，减少对昂贵人工标注的依赖。执行反馈强化学习（RLEF；Gehring et al., 2025）用环境反馈（如编程测试用例的通过率）计算奖励，再经 PPO 优化。除 PPO 外，直接偏好优化（DPO；Rafailov et al., 2023）及其后继（如 Azar et al. (2023)、Ethayarajh et al. (2024)、Meng et al. (2024)、Lanchantin et al. (2025)）以及 GRPO（Shao et al., 2024）等其他 RL 优化，也被证明能有效微调 LLM 以最大化目标奖励。上述方法的一个局限在于它们聚焦单步优化、奖励只在回合末计算，导致多步优化下表现欠佳（Liu et al., 2024；Wang et al., 2024）。SWiRL 聚焦于「生成回复前需要多步推理与工具调用」的场景。与上述方法不同，SWiRL 使模型能就其细粒度的逐步行动获得反馈，从而在更长时程上实现更好的多步推理与工具使用。

用 RL 做多步优化。近期工作包括 DQO（Liu et al., 2024）与 OREO（Wang et al., 2024），提出离线强化学习以改进 LLM 的多步推理。但二者都未聚焦提升模型使用工具或与外部环境交互的能力。此外，与我们在（推理）步骤级优化的做法不同，DQO 依赖 token 级行动，而如 Wang et al. (2024) 所示，token 级行动通常不如步骤级行动有效。而且 OREO 需要训练单独的价值网络与策略，并依赖两模型的迭代协同优化；维护、训练并服务这两个模型的开销可能令人望而却步，对大模型尤甚。PRIME（Cui et al., 2025）提出改进多步推理的在线方法，但不支持工具使用或离线训练。Tulu-3（Lambert et al., 2025）用可验证奖励训练语言模型提升数学能力，但需要金标签。

用合成数据改进推理。已有多种生成合成推理数据的方法。这些方法要么依赖金标签过滤数据，要么组合金标签与过程或结果奖励模型（Zelikman et al., 2022；Singh et al., 2024）。例如 STaR（Zelikman et al., 2022）为推理问题生成思维链（CoT），筛出得到正确答案者，并对这些推理轨迹做有监督微调（SFT）。该文还提出一种名为「合理化（rationalization）」的增强技术：对模型答错的每道题，把正确答案提供给模型，提示其生成通向该答案的 CoT。拒绝采样微调（RFT；Yuan et al., 2023）是另一种方法：从模型收集推理轨迹，并只用结果正确者做 SFT。ReST（Gulcehre et al., 2023）通过迭代生成数据、再用有监督或强化学习目标在其上微调，在机器翻译上展现出强劲表现。$ReST^{EM}$（Singh et al., 2024）是 ReST 的扩展，在数学与编程评估上超越只用人类数据训练，但几轮迭代后就进入平台期，推测是过拟合所致。我们的方法同样使用基于模型的途径生成多步轨迹。但我们表明：用模型为每条推理轨迹中的步骤打标签，比只用含正确最终答案的轨迹带来更高的域外泛化，这意味着我们不需要金标签。此外，我们使模型能迭代使用工具来执行多跳问答与数学推理。

过程 vs. 结果导向的优化。在数学与推理领域，已有不少比较过程与结果导向方法有效性的尝试（Lightman et al., 2023；Uesato et al., 2022；Snell et al., 2024）。例如 Lightman et al. (2023) 表明，在为固定生成器模型的样本排序的任务上，结果奖励模型（ORM）比过程奖励模型（PRM）更有效；而 Uesato et al. (2022) 证明结果监督以更低成本取得与过程监督相当的准确率，但所得模型的推理轨迹保真度更低。两者都依赖昂贵的人工标注与金标签，且都未探讨 PRM 与 ORM 在强化学习优化中的影响，也未探讨数据过滤对有监督与 RL 优化目标的不同作用。

## 4 实验

| 数据集 | HotpotQA | CofCA（平均） | MuSiQue |
| --- | --- | --- | --- |
| 指标 | PM† | PM† | PM† |
| 专有 LLM |  |  |  |
| GPT-4 | 74.8 | 51.9 | 63.9 |
| GPT-3.5 | 62.8 | 40.7 | 53.1 |
| Gemini 1.0 Pro | 63.5 | 33.3 | 46.9 |
| Bing Chat | 72.1 | 41.6 | 52.3 |
| O1-preview | 76.9 | 58.5 | 67.9 |
| 开源 LLM |  |  |  |
| Llama 2-7b | 38.5 | 28.9 | 34.2 |
| Mistral-7b | 34.9 | 25.6 | 29.2 |
| Qwen 2-7b | 39.3 | 30.7 | 33.5 |
| Base Gemma 2-27b | 58.6 | 31.7 | 35.4 |
| SWiRL Gemma 2-27b（本文） | 67.8 | 39.3 | 43.6 |

表 1：多个数据集上的准确率对比（PM†：部分匹配）：HotpotQA、CofCA（2 跳、3 跳、4 跳的平均）与 MuSiQue。基线结果取自 Wu et al. (2024)。Gemma-2 模型（SWiRL 与基座模型）不提供上下文文档，但允许顺序查询向量数据库。SWiRL 模型用过程过滤数据在 HotPotQA 上训练；为与基线结果一致，在 300 道随机抽样的题目上用 GPT-4o 与 Wu et al. (2024) 相同的提示评估。示例 id 见附录 G。

### 4.1 评估数据集

为评估多步搜索工具使用的表现，我们选择了五个具有挑战性的多跳问答与数学推理数据集：

- HotPotQA（Yang et al., 2018）由来自多种领域的多跳问题组成。人类标注者构造的问题只有组合 Wikipedia 多个段落的信息才能回答。
- MuSiQue（Trivedi et al., 2022）是通过把多个单跳问题串接起来构造的多跳问答数据集。
- CofCA（Wu et al., 2024）是一个只有查询反事实版 Wikipedia 才能回答的多跳数据集，含 2 至 4 跳问题。
- BeerQA（Qi et al., 2021a）是 HotPotQA 的扩展，设计为比原数据集包含更多跳。
- GSM8K（Cobbe et al., 2021）由小学数学应用题组成，通常需 2-8 步求解。

对问答数据集，我们用 Gecko-1B 的 768 维（英文）嵌入（Lee et al., 2024）为每个数据划分的全部文章建立了向量数据库。

对表 1 的实验，我们沿用 Wu et al. (2024) 的流程：在目标数据集 300 个随机抽样的样本上评估，使用相同的评审语言模型（GPT4o）与相同提示。对本文其余实验，我们用 Gemma-2-27b 做评审，因为更省钱；例外是 GSM8K，我们用 Gemini 1.5 Pro，因为它的数值评估明显更好。基于模型的评估正成为精确匹配与 F1 指标的一种可扩展、更不易碎的替代（Zheng et al., 2023；Gu et al., 2025），但确实给评估引入了新的随机性来源。针对三种不同模型评审的人工检视与误差分析见附录 D。

如 2.3 节所述，对每道题，我们迭代提示模型调用工具或给出最终答案，并把最大查询数限制为：问答数据集 5 次、数学推理数据集 10 次。

### 4.2 结果与讨论

![Refer to caption](2504.04736v2/data_filtering.png)

图 4：数据过滤对 SWiRL 性能的影响。训练合成数据派生自 HotPotQA。即便在未过滤的合成数据上训练，SWiRL 也学会了多跳问答。SWiRL 的最佳表现来自只用过程过滤的数据训练——数据按推理轨迹中每一步的合理性挑选，但同时包含正确与错误的回复。注意，所有情形下模型都配备工具并允许多次调用。

数据过滤对模型性能的影响：我们评估了各种过滤机制对下游任务准确率的影响，如图 4 所示。具体考虑 4 种过滤：不过滤、确保最终答案正确的结果过滤、由模型判定每一步正确的过程过滤，以及过程加结果过滤。

所有实验中，我们固定用于微调的轨迹数量（研究数据集规模影响的消融除外），并为所有模型提供适当的工具。值得注意的是，只用过程过滤始终取得最高准确率，说明聚焦数据打磨的过程面比训练轨迹的正确性更重要。未过滤与过滤数据都相对基座模型有所改进，但按正确性过滤通常损害性能；除 MuSiQue 外，结果过滤或过程加结果过滤的数据不如未过滤数据有效。我们假设这是因为 SWiRL 实际上受益于同时拥有正例与负例。这些结果凸显了依赖金标签的结果过滤的相对不重要，也证明我们的过程 RL 方法甚至能从最终答案错误的轨迹中有效学习。

跨相异任务与工具的泛化：为衡量跨训练任务的泛化，我们评估了一个在带搜索工具的多跳问答（HotPotQA）上训练的模型的数学推理能力。具体地，我们在数学推理任务 GSM8K 上评估该模型，为其提供 SymPy 解释器作计算器。该实验在另一个 300 例的随机子样本上进行。如表 2 所示，把 SWiRL 应用于分布外数据与任务仍能改进性能。

|  | GSM8K | HotPotQA | CofCA | BeerQA | MuSiQue |
| --- | --- | --- | --- | --- | --- |
|  | (数学) | (问答) | (问答) | (问答) | (问答) |
| 基座模型 | 0.65 | 0.65 | 0.54 | 0.59 | 0.45 |
| 在 GSM8K 上 SWiRL（数学） | 0.79 | 0.71 | 0.56 | 0.68 | 0.49 |
| 在 HotPotQA 上 SWiRL（问答） | 0.76 | 0.73 | 0.62 | 0.68 | 0.50 |

表 2：SWiRL 泛化性能。在 HotPotQA 或 GSM8K 的合成轨迹上微调，同时改进分布内与分布外任务的表现。有趣的是，在不同领域与工具（如数学与计算器）上训练，能改进用搜索引擎的问答，反之亦然，说明 SWiRL 在提升通用多步推理与工具使用能力上的有效性。

![Refer to caption](2504.04736v2/sft_vs_rl.png)

图 5：SFT 与 SWiRL 的比较。SWiRL 大幅受益于只用过程过滤的轨迹，并且与 SFT 不同，它能从结果正确与错误的轨迹中学习。注意，所有情形下模型都配备相同工具（检索器或计算器）并允许多次调用。

有监督微调与 SWiRL 的比较：图 5 比较了有监督微调（SFT）与 SWiRL 在各种下游任务上的表现。结果表明 SFT 的总体表现不如 SWiRL。事实上，我们发现 SFT 相对基座模型甚至降低性能（见附录 B），这与先前表明 SFT 可能损害推理能力的工作一致（Chen et al., 2025）。有趣的是，我们观察到 SFT 在「过程加结果过滤」的数据上比只用过程过滤的数据表现更好，而 SWiRL 在只用过程过滤的数据上学习得最好。我们把这归因于 SFT 倾向记忆而非泛化（Chu et al., 2025；Setlur et al., 2024），这会妨碍模型在新颖、未见场景上的表现。相比之下，SWiRL 能通过针对每步奖励最大化来改进模型表现。SWiRL 使模型对必要步骤（如多步查询生成与检索）建立更深理解，从而增强规划与泛化。此外，附录 B 中我们在 Gemini 1.5 Pro（SWiRL 的奖励模型）生成的合成轨迹上做了 SFT，发现并未改进性能。

工具使用的影响：如 2.3 节所述，推理时我们使用图 3 所提出的多步评估，迭代提示模型按需调用工具回答问题。如图 9 所示，基座与 SWiRL 模型都从 SWiRL 的多步工具使用推理中获益，但 SWiRL 训练带来更大的进一步提升。值得注意的是，SWiRL 模型即便不访问工具也有显著改进，说明 SWiRL 训练提升了模型把复杂问题分解为多个可管理子任务的能力。

![Refer to caption](2504.04736v2/tooluse.png)

图 6：SWiRL 在有与无多步工具使用下的表现。SWiRL 的多步工具使用推理同时改进基座模型与 SWiRL 微调模型，但对后者助益显著更大。

微调数据集与模型规模扩展的影响：我们对微调数据集规模的扩展实验揭示了清晰趋势：如图 7 所示，SWiRL 有能力利用更大的数据集，即便只用过程过滤的数据。随着微调数据集规模增大，模型在目标多步推理任务上的表现持续增强。100 个数据点的小数据集不足以让模型有效泛化，而 1,000 个数据点就有显著改进，在所有数据集上都有扎实增益。进一步扩展到 10,000 个数据点继续带来性能提升，证实我们的方法能善用更大数据集改进推理能力。有趣的是，在 GSM8K 上我们还观察到，随着合成轨迹数量增加性能提升——即便这些轨迹来自不同领域（问答对数学推理）与不同工具（搜索对计算器）。

我们还改变了模型规模，观察到较小模型（2b 与 9b）可从域内 SWiRL 获益，但不像更大的 Gemma-2-27b 那样展现同样的泛化。结果见附录 C。

![Refer to caption](2504.04736v2/scaling_datasize.png)

图 7：性能随合成数据集规模的变化。合成训练数据派生自 HotPotQA，准确率由 Gemma-2-27b 评估。随着数据集规模扩大，模型表现持续改进。仅用 1000 个数据点，模型就在分布内与分布外数据集上都有稳健提升。所有情形下评估均使用多步 SWiRL 推理。

与奖励模型的比较：这里我们比较 Gemma-2-27b 经 SWiRL 微调前后的表现与 SWiRL 所用奖励模型 Gemini 1.5 Pro。与本文其他实验一样，Gemma-2-27b 用于合成数据生成，Gemini 1.5 Pro 用作奖励模型。结果见图 8。可以看到，SWiRL 在所有基准上都显著超过基座模型，甚至在部分分布外基准（包括 CofCA 与 BeerQA）上超过 Gemini 1.5 Pro。这些结果表明 SWiRL 并不只是在蒸馏更强的奖励模型（Gemini 1.5 Pro）。

![Refer to caption](2504.04736v2/swirlvsgemini.png)

图 8：SWiRL 与基座模型及 Gemini 1.5 Pro 的表现比较。SWiRL 微调改进所有基准上的表现，甚至使模型在部分分布外基准上超过 Gemini 1.5 Pro，说明 SWiRL 不只是蒸馏更大的奖励模型（Gemini 1.5 Pro）。注意，所有情形下每个模型都配备相同工具（检索器或计算器）并允许多次调用。

对平均过程标签准确率的影响：在前几小节中，我们评估了 SWiRL 对下游任务准确率的影响。这里我们考察 SWiRL 如何取得这些性能改进。表 3 展示了基座模型与 SWiRL 微调模型在 HotPotQA 与 GSM8K 各 500 条轨迹（由 100 道问题派生）上的平均过程标签准确率。为计算每步得分，我们使用与过程过滤相同的模型与提示（如第 4 节所述）。我们对轨迹内与跨轨迹的过程标签分数取宏平均。我们观察到，无论分布内还是分布外任务，SWiRL 模型生成的轨迹都有更高的平均过程标签，说明更高的最终准确率由更好的多步推理驱动。

|  | HotPotQA | GSM8K |
| --- | --- | --- |
|  | （分布内） | （分布外） |
| 基座（平均过程标签） | 82.5% | 87.5% |
| 在 HotPotQA 上 SWiRL（平均过程标签） | 91.0% | 91.6% |

表 3：SWiRL 对过程正确性的影响。多步 RL 优化后，我们观察到每步的平均正确性在分布内与分布外任务上都相对基座模型提升。

## 5 结论

本工作中，我们提出一种面向多步推理与工具使用的合成数据生成与离线强化学习方法。该方法在具有挑战性的多跳问答与数学推理任务上平均超越基线 15%。我们探讨了多步、工具使用设定下不同数据过滤策略的效果，发现我们的 RL 方法即便在未过滤数据上也有效，但在过程过滤数据上表现最佳。与有监督微调不同，我们的 RL 方法能从最终答案错误的轨迹中学习，并且实际上受益于正确与错误最终答案的混合。SWiRL 展现出强泛化性：在多跳问答（HotPotQA）上训练使数学推理（GSM8K）提升 16.9%，反向训练提升 9.2%。

## 参考文献
- Anthropic (2024)

  Anthropic.
  The Claude 3 Model Family: Opus, Sonnet, Haiku, 2024.
  URL <https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf>.
- Azar et al. (2023)

  Mohammad Gheshlaghi Azar, Mark Rowland, Bilal Piot, Daniel Guo, Daniele Calandriello, Michal Valko, and Rémi Munos.
  A General Theoretical Paradigm to Understand Learning from Human Preferences, 2023.
  URL <https://arxiv.org/abs/2310.12036>.
- Bai et al. (2022)

  Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones, Anna Chen, Anna Goldie, Azalia Mirhoseini, Cameron McKinnon, Carol Chen, Catherine Olsson, Christopher Olah, Danny Hernandez, Dawn Drain, Deep Ganguli, Dustin Li, Eli Tran-Johnson, Ethan Perez, Jamie Kerr, Jared Mueller, Jeffrey Ladish, Joshua Landau, Kamal Ndousse, Kamile Lukosuite, Liane Lovitt, Michael Sellitto, Nelson Elhage, Nicholas Schiefer, Noemi Mercado, Nova DasSarma, Robert Lasenby, Robin Larson, Sam Ringer, Scott Johnston, Shauna Kravec, Sheer El Showk, Stanislav Fort, Tamera Lanham, Timothy Telleen-Lawton, Tom Conerly, Tom Henighan, Tristan Hume, Samuel R. Bowman, Zac Hatfield-Dodds, Ben Mann, Dario Amodei, Nicholas Joseph, Sam McCandlish, Tom Brown, and Jared Kaplan.
  Constitutional AI: Harmlessness from AI Feedback, 2022.
  URL <https://arxiv.org/abs/2212.08073>.
- Chen et al. (2025)

  Hardy Chen, Haoqin Tu, Fali Wang, Hui Liu, Xianfeng Tang, Xinya Du, Yuyin Zhou, and Cihang Xie.
  SFT or RL? An Early Investigation into Training R1-Like Reasoning Large Vision-Language Models, 2025.
  URL <https://arxiv.org/abs/2504.11468>.
- Christiano et al. (2023)

  Paul Christiano, Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg, and Dario Amodei.
  Deep reinforcement learning from human preferences, 2023.
  URL <https://arxiv.org/abs/1706.03741>.
- Chu et al. (2025)

  Tianzhe Chu, Yuexiang Zhai, Jihan Yang, Shengbang Tong, Saining Xie, Dale Schuurmans, Quoc V. Le, Sergey Levine, and Yi Ma.
  SFT Memorizes, RL Generalizes: A Comparative Study of Foundation Model Post-training, 2025.
  URL <https://arxiv.org/abs/2501.17161>.
- Cobbe et al. (2021)

  Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman.
  Training Verifiers to Solve Math Word Problems, 2021.
  URL <https://arxiv.org/abs/2110.14168>.
- Cui et al. (2025)

  Ganqu Cui, Lifan Yuan, Zefan Wang, Hanbin Wang, Wendi Li, Bingxiang He, Yuchen Fan, Tianyu Yu, Qixin Xu, Weize Chen, Jiarui Yuan, Huayu Chen, Kaiyan Zhang, Xingtai Lv, Shuo Wang, Yuan Yao, Xu Han, Hao Peng, Yu Cheng, Zhiyuan Liu, Maosong Sun, Bowen Zhou, and Ning Ding.
  Process Reinforcement through Implicit Rewards, 2025.
  URL <https://arxiv.org/abs/2502.01456>.
- DeepSeek-AI and others (2025)

  DeepSeek-AI and others.
  Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning.
  *arXiv preprint arXiv:2501.12948*, 2025.
  doi: 10.48550/arXiv.2501.12948.
  URL <https://arxiv.org/abs/2501.12948>.
- Ehrlich et al. (2025)

  Ryan Ehrlich, Bradley Brown, Jordan Juravsky, Ronald Clark, Christopher Ré, and Azalia Mirhoseini.
  CodeMonkeys: Scaling Test-Time Compute for Software Engineering, 2025.
  URL <https://arxiv.org/abs/2501.14723>.
- Ethayarajh et al. (2024)

  Kawin Ethayarajh, Winnie Xu, Niklas Muennighoff, Dan Jurafsky, and Douwe Kiela.
  KTO: Model Alignment as Prospect Theoretic Optimization, 2024.
  URL <https://arxiv.org/abs/2402.01306>.
- Gehring et al. (2025)

  Jonas Gehring, Kunhao Zheng, Jade Copet, Vegard Mella, Quentin Carbonneaux, Taco Cohen, and Gabriel Synnaeve.
  RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning, 2025.
  URL <https://arxiv.org/abs/2410.02089>.
- Gemini Team et al. (2024)

  Gemini Team, Petko Georgiev, Ving Ian Lei, Ryan Burnell, Libin Bai, Anmol Gulati, Garrett Tanzer, Damien Vincent, Zhufeng Pan, Shibo Wang, Soroosh Mariooryad, Yifan Ding, Xinyang Geng, Fred Alcober, Roy Frostig, Mark Omernick, Lexi Walker, Cosmin Paduraru, Christina Sorokin, Andrea Tacchetti, Colin Gaffney, Samira Daruki, Olcan Sercinoglu, Zach Gleicher, Juliette Love, Paul Voigtlaender, Rohan Jain, Gabriela Surita, Kareem Mohamed, Rory Blevins, Junwhan Ahn, Tao Zhu, Kornraphop Kawintiranon, Orhan Firat, Yiming Gu, Yujing Zhang, Matthew Rahtz, Manaal Faruqui, Natalie Clay, Justin Gilmer, JD Co-Reyes, Ivo Penchev, Rui Zhu, Nobuyuki Morioka, Kevin Hui, Krishna Haridasan, Victor Campos, Mahdis Mahdieh, Mandy Guo, Samer Hassan, Kevin Kilgour, Arpi Vezer, Heng-Tze Cheng, Raoul de Liedekerke, Siddharth Goyal, Paul Barham, DJ Strouse, Seb Noury, Jonas Adler, Mukund Sundararajan, Sharad Vikram, Dmitry Lepikhin, Michela Paganini, Xavier Garcia, Fan Yang, Dasha Valter, Maja Trebacz, Kiran Vodrahalli, Chulayuth
  Asawaroengchai, Roman Ring, Norbert Kalb, Livio Baldini Soares, Siddhartha Brahma, David Steiner, Tianhe Yu, Fabian Mentzer, Antoine He, Lucas Gonzalez, Bibo Xu, Raphael Lopez Kaufman, Laurent El Shafey, Junhyuk Oh, Tom Hennigan, George van den Driessche, Seth Odoom, Mario Lucic, Becca Roelofs, Sid Lall, Amit Marathe, Betty Chan, Santiago Ontanon, Luheng He, Denis Teplyashin, Jonathan Lai, Phil Crone, Bogdan Damoc, Lewis Ho, Sebastian Riedel, Karel Lenc, Chih-Kuan Yeh, Aakanksha Chowdhery, Yang Xu, Mehran Kazemi, Ehsan Amid, Anastasia Petrushkina, Kevin Swersky, Ali Khodaei, Gowoon Chen, Chris Larkin, Mario Pinto, Geng Yan, Adria Puigdomenech Badia, Piyush Patil, Steven Hansen, Dave Orr, Sebastien M. R. Arnold, Jordan Grimstad, Andrew Dai, Sholto Douglas, Rishika Sinha, Vikas Yadav, Xi Chen, Elena Gribovskaya, Jacob Austin, Jeffrey Zhao, Kaushal Patel, Paul Komarek, Sophia Austin, Sebastian Borgeaud, Linda Friso, Abhimanyu Goyal, Ben Caine, Kris Cao, Da-Woon Chung, Matthew Lamm, Gabe Barth-Maron, Thais
  Kagohara, Kate Olszewska, Mia Chen, Kaushik Shivakumar, Rishabh Agarwal, Harshal Godhia, Ravi Rajwar, Javier Snaider, Xerxes Dotiwalla, Yuan Liu, Aditya Barua, Victor Ungureanu, Yuan Zhang, Bat-Orgil Batsaikhan, Mateo Wirth, James Qin, Ivo Danihelka, Tulsee Doshi, Martin Chadwick, Jilin Chen, Sanil Jain, Quoc Le, Arjun Kar, Madhu Gurumurthy, Cheng Li, Ruoxin Sang, Fangyu Liu, Lampros Lamprou, Rich Munoz, Nathan Lintz, Harsh Mehta, Heidi Howard, Malcolm Reynolds, Lora Aroyo, Quan Wang, Lorenzo Blanco, Albin Cassirer, Jordan Griffith, Dipanjan Das, Stephan Lee, Jakub Sygnowski, Zach Fisher, James Besley, Richard Powell, Zafarali Ahmed, Dominik Paulus, David Reitter, Zalan Borsos, Rishabh Joshi, Aedan Pope, Steven Hand, Vittorio Selo, Vihan Jain, Nikhil Sethi, Megha Goel, Takaki Makino, Rhys May, Zhen Yang, Johan Schalkwyk, Christina Butterfield, Anja Hauth, Alex Goldin, Will Hawkins, Evan Senter, Sergey Brin, Oliver Woodman, Marvin Ritter, Eric Noland, Minh Giang, Vijay Bolina, Lisa Lee, Tim Blyth, Ian
  Mackinnon, Machel Reid, Obaid Sarvana, David Silver, Alexander Chen, Lily Wang, Loren Maggiore, Oscar Chang, Nithya Attaluri, Gregory Thornton, Chung-Cheng Chiu, Oskar Bunyan, Nir Levine, Timothy Chung, Evgenii Eltyshev, Xiance Si, Timothy Lillicrap, Demetra Brady, Vaibhav Aggarwal, Boxi Wu, Yuanzhong Xu, Ross McIlroy, Kartikeya Badola, Paramjit Sandhu, Erica Moreira, Wojciech Stokowiec, Ross Hemsley, Dong Li, Alex Tudor, Pranav Shyam, Elahe Rahimtoroghi, Salem Haykal, Pablo Sprechmann, Xiang Zhou, Diana Mincu, Yujia Li, Ravi Addanki, Kalpesh Krishna, Xiao Wu, Alexandre Frechette, Matan Eyal, Allan Dafoe, Dave Lacey, Jay Whang, Thi Avrahami, Ye Zhang, Emanuel Taropa, Hanzhao Lin, Daniel Toyama, Eliza Rutherford, Motoki Sano, HyunJeong Choe, Alex Tomala, Chalence Safranek-Shrader, Nora Kassner, Mantas Pajarskas, Matt Harvey, Sean Sechrist, Meire Fortunato, Christina Lyu, Gamaleldin Elsayed, Chenkai Kuang, James Lottes, Eric Chu, Chao Jia, Chih-Wei Chen, Peter Humphreys, Kate Baumli, Connie Tao, Rajkumar
  Samuel, Cicero Nogueira dos Santos, Anders Andreassen, Nemanja Rakićević, Dominik Grewe, Aviral Kumar, Stephanie Winkler, Jonathan Caton, Andrew Brock, Sid Dalmia, Hannah Sheahan, Iain Barr, Yingjie Miao, Paul Natsev, Jacob Devlin, Feryal Behbahani, Flavien Prost, Yanhua Sun, Artiom Myaskovsky, Thanumalayan Sankaranarayana Pillai, Dan Hurt, Angeliki Lazaridou, Xi Xiong, Ce Zheng, Fabio Pardo, Xiaowei Li, Dan Horgan, Joe Stanton, Moran Ambar, Fei Xia, Alejandro Lince, Mingqiu Wang, Basil Mustafa, Albert Webson, Hyo Lee, Rohan Anil, Martin Wicke, Timothy Dozat, Abhishek Sinha, Enrique Piqueras, Elahe Dabir, Shyam Upadhyay, Anudhyan Boral, Lisa Anne Hendricks, Corey Fry, Josip Djolonga, Yi Su, Jake Walker, Jane Labanowski, Ronny Huang, Vedant Misra, Jeremy Chen, RJ Skerry-Ryan, Avi Singh, Shruti Rijhwani, Dian Yu, Alex Castro-Ros, Beer Changpinyo, Romina Datta, Sumit Bagri, Arnar Mar Hrafnkelsson, Marcello Maggioni, Daniel Zheng, Yury Sulsky, Shaobo Hou, Tom Le Paine, Antoine Yang, Jason Riesa, Dominika
  Rogozinska, Dror Marcus, Dalia El Badawy, Qiao Zhang, Luyu Wang, Helen Miller, Jeremy Greer, Lars Lowe Sjos, Azade Nova, Heiga Zen, Rahma Chaabouni, Mihaela Rosca, Jiepu Jiang, Charlie Chen, Ruibo Liu, Tara Sainath, Maxim Krikun, Alex Polozov, Jean-Baptiste Lespiau, Josh Newlan, Zeyncep Cankara, Soo Kwak, Yunhan Xu, Phil Chen, Andy Coenen, Clemens Meyer, Katerina Tsihlas, Ada Ma, Juraj Gottweis, Jinwei Xing, Chenjie Gu, Jin Miao, Christian Frank, Zeynep Cankara, Sanjay Ganapathy, Ishita Dasgupta, Steph Hughes-Fitt, Heng Chen, David Reid, Keran Rong, Hongmin Fan, Joost van Amersfoort, Vincent Zhuang, Aaron Cohen, Shixiang Shane Gu, Anhad Mohananey, Anastasija Ilic, Taylor Tobin, John Wieting, Anna Bortsova, Phoebe Thacker, Emma Wang, Emily Caveness, Justin Chiu, Eren Sezener, Alex Kaskasoli, Steven Baker, Katie Millican, Mohamed Elhawaty, Kostas Aisopos, Carl Lebsack, Nathan Byrd, Hanjun Dai, Wenhao Jia, Matthew Wiethoff, Elnaz Davoodi, Albert Weston, Lakshman Yagati, Arun Ahuja, Isabel Gao, Golan Pundak,
  Susan Zhang, Michael Azzam, Khe Chai Sim, Sergi Caelles, James Keeling, Abhanshu Sharma, Andy Swing, YaGuang Li, Chenxi Liu, Carrie Grimes Bostock, Yamini Bansal, Zachary Nado, Ankesh Anand, Josh Lipschultz, Abhijit Karmarkar, Lev Proleev, Abe Ittycheriah, Soheil Hassas Yeganeh, George Polovets, Aleksandra Faust, Jiao Sun, Alban Rrustemi, Pen Li, Rakesh Shivanna, Jeremiah Liu, Chris Welty, Federico Lebron, Anirudh Baddepudi, Sebastian Krause, Emilio Parisotto, Radu Soricut, Zheng Xu, Dawn Bloxwich, Melvin Johnson, Behnam Neyshabur, Justin Mao-Jones, Renshen Wang, Vinay Ramasesh, Zaheer Abbas, Arthur Guez, Constant Segal, Duc Dung Nguyen, James Svensson, Le Hou, Sarah York, Kieran Milan, Sophie Bridgers, Wiktor Gworek, Marco Tagliasacchi, James Lee-Thorp, Michael Chang, Alexey Guseynov, Ale Jakse Hartman, Michael Kwong, Ruizhe Zhao, Sheleem Kashem, Elizabeth Cole, Antoine Miech, Richard Tanburn, Mary Phuong, Filip Pavetic, Sebastien Cevey, Ramona Comanescu, Richard Ives, Sherry Yang, Cosmo Du, Bo Li, Zizhao
  Zhang, Mariko Iinuma, Clara Huiyi Hu, Aurko Roy, Shaan Bijwadia, Zhenkai Zhu, Danilo Martins, Rachel Saputro, Anita Gergely, Steven Zheng, Dawei Jia, Ioannis Antonoglou, Adam Sadovsky, Shane Gu, Yingying Bi, Alek Andreev, Sina Samangooei, Mina Khan, Tomas Kocisky, Angelos Filos, Chintu Kumar, Colton Bishop, Adams Yu, Sarah Hodkinson, Sid Mittal, Premal Shah, Alexandre Moufarek, Yong Cheng, Adam Bloniarz, Jaehoon Lee, Pedram Pejman, Paul Michel, Stephen Spencer, Vladimir Feinberg, Xuehan Xiong, Nikolay Savinov, Charlotte Smith, Siamak Shakeri, Dustin Tran, Mary Chesus, Bernd Bohnet, George Tucker, Tamara von Glehn, Carrie Muir, Yiran Mao, Hideto Kazawa, Ambrose Slone, Kedar Soparkar, Disha Shrivastava, James Cobon-Kerr, Michael Sharman, Jay Pavagadhi, Carlos Araya, Karolis Misiunas, Nimesh Ghelani, Michael Laskin, David Barker, Qiujia Li, Anton Briukhov, Neil Houlsby, Mia Glaese, Balaji Lakshminarayanan, Nathan Schucher, Yunhao Tang, Eli Collins, Hyeontaek Lim, Fangxiaoyu Feng, Adria Recasens, Guangda Lai,
  Alberto Magni, Nicola De Cao, Aditya Siddhant, Zoe Ashwood, Jordi Orbay, Mostafa Dehghani, Jenny Brennan, Yifan He, Kelvin Xu, Yang Gao, Carl Saroufim, James Molloy, Xinyi Wu, Seb Arnold, Solomon Chang, Julian Schrittwieser, Elena Buchatskaya, Soroush Radpour, Martin Polacek, Skye Giordano, Ankur Bapna, Simon Tokumine, Vincent Hellendoorn, Thibault Sottiaux, Sarah Cogan, Aliaksei Severyn, Mohammad Saleh, Shantanu Thakoor, Laurent Shefey, Siyuan Qiao, Meenu Gaba, Shuo yiin Chang, Craig Swanson, Biao Zhang, Benjamin Lee, Paul Kishan Rubenstein, Gan Song, Tom Kwiatkowski, Anna Koop, Ajay Kannan, David Kao, Parker Schuh, Axel Stjerngren, Golnaz Ghiasi, Gena Gibson, Luke Vilnis, Ye Yuan, Felipe Tiengo Ferreira, Aishwarya Kamath, Ted Klimenko, Ken Franko, Kefan Xiao, Indro Bhattacharya, Miteyan Patel, Rui Wang, Alex Morris, Robin Strudel, Vivek Sharma, Peter Choy, Sayed Hadi Hashemi, Jessica Landon, Mara Finkelstein, Priya Jhakra, Justin Frye, Megan Barnes, Matthew Mauger, Dennis Daun, Khuslen Baatarsukh, Matthew
  Tung, Wael Farhan, Henryk Michalewski, Fabio Viola, Felix de Chaumont Quitry, Charline Le Lan, Tom Hudson, Qingze Wang, Felix Fischer, Ivy Zheng, Elspeth White, Anca Dragan, Jean baptiste Alayrac, Eric Ni, Alexander Pritzel, Adam Iwanicki, Michael Isard, Anna Bulanova, Lukas Zilka, Ethan Dyer, Devendra Sachan, Srivatsan Srinivasan, Hannah Muckenhirn, Honglong Cai, Amol Mandhane, Mukarram Tariq, Jack W. Rae, Gary Wang, Kareem Ayoub, Nicholas FitzGerald, Yao Zhao, Woohyun Han, Chris Alberti, Dan Garrette, Kashyap Krishnakumar, Mai Gimenez, Anselm Levskaya, Daniel Sohn, Josip Matak, Inaki Iturrate, Michael B. Chang, Jackie Xiang, Yuan Cao, Nishant Ranka, Geoff Brown, Adrian Hutter, Vahab Mirrokni, Nanxin Chen, Kaisheng Yao, Zoltan Egyed, Francois Galilee, Tyler Liechty, Praveen Kallakuri, Evan Palmer, Sanjay Ghemawat, Jasmine Liu, David Tao, Chloe Thornton, Tim Green, Mimi Jasarevic, Sharon Lin, Victor Cotruta, Yi-Xuan Tan, Noah Fiedel, Hongkun Yu, Ed Chi, Alexander Neitz, Jens Heitkaemper, Anu Sinha, Denny
  Zhou, Yi Sun, Charbel Kaed, Brice Hulse, Swaroop Mishra, Maria Georgaki, Sneha Kudugunta, Clement Farabet, Izhak Shafran, Daniel Vlasic, Anton Tsitsulin, Rajagopal Ananthanarayanan, Alen Carin, Guolong Su, Pei Sun, Shashank V, Gabriel Carvajal, Josef Broder, Iulia Comsa, Alena Repina, William Wong, Warren Weilun Chen, Peter Hawkins, Egor Filonov, Lucia Loher, Christoph Hirnschall, Weiyi Wang, Jingchen Ye, Andrea Burns, Hardie Cate, Diana Gage Wright, Federico Piccinini, Lei Zhang, Chu-Cheng Lin, Ionel Gog, Yana Kulizhskaya, Ashwin Sreevatsa, Shuang Song, Luis C. Cobo, Anand Iyer, Chetan Tekur, Guillermo Garrido, Zhuyun Xiao, Rupert Kemp, Huaixiu Steven Zheng, Hui Li, Ananth Agarwal, Christel Ngani, Kati Goshvadi, Rebeca Santamaria-Fernandez, Wojciech Fica, Xinyun Chen, Chris Gorgolewski, Sean Sun, Roopal Garg, Xinyu Ye, S. M. Ali Eslami, Nan Hua, Jon Simon, Pratik Joshi, Yelin Kim, Ian Tenney, Sahitya Potluri, Lam Nguyen Thiet, Quan Yuan, Florian Luisier, Alexandra Chronopoulou, Salvatore Scellato, Praveen
  Srinivasan, Minmin Chen, Vinod Koverkathu, Valentin Dalibard, Yaming Xu, Brennan Saeta, Keith Anderson, Thibault Sellam, Nick Fernando, Fantine Huot, Junehyuk Jung, Mani Varadarajan, Michael Quinn, Amit Raul, Maigo Le, Ruslan Habalov, Jon Clark, Komal Jalan, Kalesha Bullard, Achintya Singhal, Thang Luong, Boyu Wang, Sujeevan Rajayogam, Julian Eisenschlos, Johnson Jia, Daniel Finchelstein, Alex Yakubovich, Daniel Balle, Michael Fink, Sameer Agarwal, Jing Li, Dj Dvijotham, Shalini Pal, Kai Kang, Jaclyn Konzelmann, Jennifer Beattie, Olivier Dousse, Diane Wu, Remi Crocker, Chen Elkind, Siddhartha Reddy Jonnalagadda, Jong Lee, Dan Holtmann-Rice, Krystal Kallarackal, Rosanne Liu, Denis Vnukov, Neera Vats, Luca Invernizzi, Mohsen Jafari, Huanjie Zhou, Lilly Taylor, Jennifer Prendki, Marcus Wu, Tom Eccles, Tianqi Liu, Kavya Kopparapu, Francoise Beaufays, Christof Angermueller, Andreea Marzoca, Shourya Sarcar, Hilal Dib, Jeff Stanway, Frank Perbet, Nejc Trdin, Rachel Sterneck, Andrey Khorlin, Dinghua Li, Xihui Wu,
  Sonam Goenka, David Madras, Sasha Goldshtein, Willi Gierke, Tong Zhou, Yaxin Liu, Yannie Liang, Anais White, Yunjie Li, Shreya Singh, Sanaz Bahargam, Mark Epstein, Sujoy Basu, Li Lao, Adnan Ozturel, Carl Crous, Alex Zhai, Han Lu, Zora Tung, Neeraj Gaur, Alanna Walton, Lucas Dixon, Ming Zhang, Amir Globerson, Grant Uy, Andrew Bolt, Olivia Wiles, Milad Nasr, Ilia Shumailov, Marco Selvi, Francesco Piccinno, Ricardo Aguilar, Sara McCarthy, Misha Khalman, Mrinal Shukla, Vlado Galic, John Carpenter, Kevin Villela, Haibin Zhang, Harry Richardson, James Martens, Matko Bosnjak, Shreyas Rammohan Belle, Jeff Seibert, Mahmoud Alnahlawi, Brian McWilliams, Sankalp Singh, Annie Louis, Wen Ding, Dan Popovici, Lenin Simicich, Laura Knight, Pulkit Mehta, Nishesh Gupta, Chongyang Shi, Saaber Fatehi, Jovana Mitrovic, Alex Grills, Joseph Pagadora, Tsendsuren Munkhdalai, Dessie Petrova, Danielle Eisenbud, Zhishuai Zhang, Damion Yates, Bhavishya Mittal, Nilesh Tripuraneni, Yannis Assael, Thomas Brovelli, Prateek Jain, Mihajlo
  Velimirovic, Canfer Akbulut, Jiaqi Mu, Wolfgang Macherey, Ravin Kumar, Jun Xu, Haroon Qureshi, Gheorghe Comanici, Jeremy Wiesner, Zhitao Gong, Anton Ruddock, Matthias Bauer, Nick Felt, Anirudh GP, Anurag Arnab, Dustin Zelle, Jonas Rothfuss, Bill Rosgen, Ashish Shenoy, Bryan Seybold, Xinjian Li, Jayaram Mudigonda, Goker Erdogan, Jiawei Xia, Jiri Simsa, Andrea Michi, Yi Yao, Christopher Yew, Steven Kan, Isaac Caswell, Carey Radebaugh, Andre Elisseeff, Pedro Valenzuela, Kay McKinney, Kim Paterson, Albert Cui, Eri Latorre-Chimoto, Solomon Kim, William Zeng, Ken Durden, Priya Ponnapalli, Tiberiu Sosea, Christopher A. Choquette-Choo, James Manyika, Brona Robenek, Harsha Vashisht, Sebastien Pereira, Hoi Lam, Marko Velic, Denese Owusu-Afriyie, Katherine Lee, Tolga Bolukbasi, Alicia Parrish, Shawn Lu, Jane Park, Balaji Venkatraman, Alice Talbert, Lambert Rosique, Yuchung Cheng, Andrei Sozanschi, Adam Paszke, Praveen Kumar, Jessica Austin, Lu Li, Khalid Salama, Bartek Perz, Wooyeol Kim, Nandita Dukkipati, Anthony
  Baryshnikov, Christos Kaplanis, XiangHai Sheng, Yuri Chervonyi, Caglar Unlu, Diego de Las Casas, Harry Askham, Kathryn Tunyasuvunakool, Felix Gimeno, Siim Poder, Chester Kwak, Matt Miecnikowski, Vahab Mirrokni, Alek Dimitriev, Aaron Parisi, Dangyi Liu, Tomy Tsai, Toby Shevlane, Christina Kouridi, Drew Garmon, Adrian Goedeckemeyer, Adam R. Brown, Anitha Vijayakumar, Ali Elqursh, Sadegh Jazayeri, Jin Huang, Sara Mc Carthy, Jay Hoover, Lucy Kim, Sandeep Kumar, Wei Chen, Courtney Biles, Garrett Bingham, Evan Rosen, Lisa Wang, Qijun Tan, David Engel, Francesco Pongetti, Dario de Cesare, Dongseong Hwang, Lily Yu, Jennifer Pullman, Srini Narayanan, Kyle Levin, Siddharth Gopal, Megan Li, Asaf Aharoni, Trieu Trinh, Jessica Lo, Norman Casagrande, Roopali Vij, Loic Matthey, Bramandia Ramadhana, Austin Matthews, CJ Carey, Matthew Johnson, Kremena Goranova, Rohin Shah, Shereen Ashraf, Kingshuk Dasgupta, Rasmus Larsen, Yicheng Wang, Manish Reddy Vuyyuru, Chong Jiang, Joana Ijazi, Kazuki Osawa, Celine Smith, Ramya Sree
  Boppana, Taylan Bilal, Yuma Koizumi, Ying Xu, Yasemin Altun, Nir Shabat, Ben Bariach, Alex Korchemniy, Kiam Choo, Olaf Ronneberger, Chimezie Iwuanyanwu, Shubin Zhao, David Soergel, Cho-Jui Hsieh, Irene Cai, Shariq Iqbal, Martin Sundermeyer, Zhe Chen, Elie Bursztein, Chaitanya Malaviya, Fadi Biadsy, Prakash Shroff, Inderjit Dhillon, Tejasi Latkar, Chris Dyer, Hannah Forbes, Massimo Nicosia, Vitaly Nikolaev, Somer Greene, Marin Georgiev, Pidong Wang, Nina Martin, Hanie Sedghi, John Zhang, Praseem Banzal, Doug Fritz, Vikram Rao, Xuezhi Wang, Jiageng Zhang, Viorica Patraucean, Dayou Du, Igor Mordatch, Ivan Jurin, Lewis Liu, Ayush Dubey, Abhi Mohan, Janek Nowakowski, Vlad-Doru Ion, Nan Wei, Reiko Tojo, Maria Abi Raad, Drew A. Hudson, Vaishakh Keshava, Shubham Agrawal, Kevin Ramirez, Zhichun Wu, Hoang Nguyen, Ji Liu, Madhavi Sewak, Bryce Petrini, DongHyun Choi, Ivan Philips, Ziyue Wang, Ioana Bica, Ankush Garg, Jarek Wilkiewicz, Priyanka Agrawal, Xiaowei Li, Danhao Guo, Emily Xue, Naseer Shaik, Andrew Leach,
  Sadh MNM Khan, Julia Wiesinger, Sammy Jerome, Abhishek Chakladar, Alek Wenjiao Wang, Tina Ornduff, Folake Abu, Alireza Ghaffarkhah, Marcus Wainwright, Mario Cortes, Frederick Liu, Joshua Maynez, Andreas Terzis, Pouya Samangouei, Riham Mansour, Tomasz Kępa, François-Xavier Aubet, Anton Algymr, Dan Banica, Agoston Weisz, Andras Orban, Alexandre Senges, Ewa Andrejczuk, Mark Geller, Niccolo Dal Santo, Valentin Anklin, Majd Al Merey, Martin Baeuml, Trevor Strohman, Junwen Bai, Slav Petrov, Yonghui Wu, Demis Hassabis, Koray Kavukcuoglu, Jeff Dean, and Oriol Vinyals.
  Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context, 2024.
  URL <https://arxiv.org/abs/2403.05530>.
- Gemma Team et al. (2024a)

  Gemma Team, Thomas Mesnard, Cassidy Hardin, Robert Dadashi, Surya Bhupatiraju, Shreya Pathak, Laurent Sifre, Morgane Rivière, Mihir Sanjay Kale, Juliette Love, Pouya Tafti, Léonard Hussenot, Pier Giuseppe Sessa, Aakanksha Chowdhery, Adam Roberts, Aditya Barua, Alex Botev, Alex Castro-Ros, Ambrose Slone, Amélie Héliou, Andrea Tacchetti, Anna Bulanova, Antonia Paterson, Beth Tsai, Bobak Shahriari, Charline Le Lan, Christopher A. Choquette-Choo, Clément Crepy, Daniel Cer, Daphne Ippolito, David Reid, Elena Buchatskaya, Eric Ni, Eric Noland, Geng Yan, George Tucker, George-Christian Muraru, Grigory Rozhdestvenskiy, Henryk Michalewski, Ian Tenney, Ivan Grishchenko, Jacob Austin, James Keeling, Jane Labanowski, Jean-Baptiste Lespiau, Jeff Stanway, Jenny Brennan, Jeremy Chen, Johan Ferret, Justin Chiu, Justin Mao-Jones, Katherine Lee, Kathy Yu, Katie Millican, Lars Lowe Sjoesund, Lisa Lee, Lucas Dixon, Machel Reid, Maciej Mikuła, Mateo Wirth, Michael Sharman, Nikolai Chinaev, Nithum Thain, Olivier Bachem,
  Oscar Chang, Oscar Wahltinez, Paige Bailey, Paul Michel, Petko Yotov, Rahma Chaabouni, Ramona Comanescu, Reena Jana, Rohan Anil, Ross McIlroy, Ruibo Liu, Ryan Mullins, Samuel L Smith, Sebastian Borgeaud, Sertan Girgin, Sholto Douglas, Shree Pandya, Siamak Shakeri, Soham De, Ted Klimenko, Tom Hennigan, Vlad Feinberg, Wojciech Stokowiec, Yu hui Chen, Zafarali Ahmed, Zhitao Gong, Tris Warkentin, Ludovic Peran, Minh Giang, Clément Farabet, Oriol Vinyals, Jeff Dean, Koray Kavukcuoglu, Demis Hassabis, Zoubin Ghahramani, Douglas Eck, Joelle Barral, Fernando Pereira, Eli Collins, Armand Joulin, Noah Fiedel, Evan Senter, Alek Andreev, and Kathleen Kenealy.
  Gemma: Open Models Based on Gemini Research and Technology, 2024a.
  URL <https://arxiv.org/abs/2403.08295>.
- Gemma Team et al. (2024b)

  Gemma Team, Morgane Riviere, Shreya Pathak, Pier Giuseppe Sessa, Cassidy Hardin, Surya Bhupatiraju, Léonard Hussenot, Thomas Mesnard, Bobak Shahriari, Alexandre Ramé, Johan Ferret, Peter Liu, Pouya Tafti, Abe Friesen, Michelle Casbon, Sabela Ramos, Ravin Kumar, Charline Le Lan, Sammy Jerome, Anton Tsitsulin, Nino Vieillard, Piotr Stanczyk, Sertan Girgin, Nikola Momchev, Matt Hoffman, Shantanu Thakoor, Jean-Bastien Grill, Behnam Neyshabur, Olivier Bachem, Alanna Walton, Aliaksei Severyn, Alicia Parrish, Aliya Ahmad, Allen Hutchison, Alvin Abdagic, Amanda Carl, Amy Shen, Andy Brock, Andy Coenen, Anthony Laforge, Antonia Paterson, Ben Bastian, Bilal Piot, Bo Wu, Brandon Royal, Charlie Chen, Chintu Kumar, Chris Perry, Chris Welty, Christopher A. Choquette-Choo, Danila Sinopalnikov, David Weinberger, Dimple Vijaykumar, Dominika Rogozińska, Dustin Herbison, Elisa Bandy, Emma Wang, Eric Noland, Erica Moreira, Evan Senter, Evgenii Eltyshev, Francesco Visin, Gabriel Rasskin, Gary Wei, Glenn Cameron, Gus Martins,
  Hadi Hashemi, Hanna Klimczak-Plucińska, Harleen Batra, Harsh Dhand, Ivan Nardini, Jacinda Mein, Jack Zhou, James Svensson, Jeff Stanway, Jetha Chan, Jin Peng Zhou, Joana Carrasqueira, Joana Iljazi, Jocelyn Becker, Joe Fernandez, Joost van Amersfoort, Josh Gordon, Josh Lipschultz, Josh Newlan, Ju yeong Ji, Kareem Mohamed, Kartikeya Badola, Kat Black, Katie Millican, Keelin McDonell, Kelvin Nguyen, Kiranbir Sodhia, Kish Greene, Lars Lowe Sjoesund, Lauren Usui, Laurent Sifre, Lena Heuermann, Leticia Lago, Lilly McNealus, Livio Baldini Soares, Logan Kilpatrick, Lucas Dixon, Luciano Martins, Machel Reid, Manvinder Singh, Mark Iverson, Martin Görner, Mat Velloso, Mateo Wirth, Matt Davidow, Matt Miller, Matthew Rahtz, Matthew Watson, Meg Risdal, Mehran Kazemi, Michael Moynihan, Ming Zhang, Minsuk Kahng, Minwoo Park, Mofi Rahman, Mohit Khatwani, Natalie Dao, Nenshad Bardoliwalla, Nesh Devanathan, Neta Dumai, Nilay Chauhan, Oscar Wahltinez, Pankil Botarda, Parker Barnes, Paul Barham, Paul Michel, Pengchong Jin,
  Petko Georgiev, Phil Culliton, Pradeep Kuppala, Ramona Comanescu, Ramona Merhej, Reena Jana, Reza Ardeshir Rokni, Rishabh Agarwal, Ryan Mullins, Samaneh Saadat, Sara Mc Carthy, Sarah Cogan, Sarah Perrin, Sébastien M. R. Arnold, Sebastian Krause, Shengyang Dai, Shruti Garg, Shruti Sheth, Sue Ronstrom, Susan Chan, Timothy Jordan, Ting Yu, Tom Eccles, Tom Hennigan, Tomas Kocisky, Tulsee Doshi, Vihan Jain, Vikas Yadav, Vilobh Meshram, Vishal Dharmadhikari, Warren Barkley, Wei Wei, Wenming Ye, Woohyun Han, Woosuk Kwon, Xiang Xu, Zhe Shen, Zhitao Gong, Zichuan Wei, Victor Cotruta, Phoebe Kirk, Anand Rao, Minh Giang, Ludovic Peran, Tris Warkentin, Eli Collins, Joelle Barral, Zoubin Ghahramani, Raia Hadsell, D. Sculley, Jeanine Banks, Anca Dragan, Slav Petrov, Oriol Vinyals, Jeff Dean, Demis Hassabis, Koray Kavukcuoglu, Clement Farabet, Elena Buchatskaya, Sebastian Borgeaud, Noah Fiedel, Armand Joulin, Kathleen Kenealy, Robert Dadashi, and Alek Andreev.
  Gemma 2: Improving Open Language Models at a Practical Size, 2024b.
  URL <https://arxiv.org/abs/2408.00118>.
- Grattafiori et al. (2024)

  Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, Amy Yang, Angela Fan, Anirudh Goyal, Anthony Hartshorn, Aobo Yang, Archi Mitra, Archie Sravankumar, Artem Korenev, Arthur Hinsvark, Arun Rao, Aston Zhang, Aurelien Rodriguez, Austen Gregerson, Ava Spataru, Baptiste Roziere, Bethany Biron, Binh Tang, Bobbie Chern, Charlotte Caucheteux, Chaya Nayak, Chloe Bi, Chris Marra, Chris McConnell, Christian Keller, Christophe Touret, Chunyang Wu, Corinne Wong, Cristian Canton Ferrer, Cyrus Nikolaidis, Damien Allonsius, Daniel Song, Danielle Pintz, Danny Livshits, Danny Wyatt, David Esiobu, Dhruv Choudhary, Dhruv Mahajan, Diego Garcia-Olano, Diego Perino, Dieuwke Hupkes, Egor Lakomkin, Ehab AlBadawy, Elina Lobanova, Emily Dinan, Eric Michael Smith, Filip Radenovic, Francisco Guzmán, Frank Zhang, Gabriel Synnaeve, Gabrielle Lee, Georgia Lewis Anderson, Govind Thattai, Graeme Nail, Gregoire Mialon, Guan Pang,
  Guillem Cucurell, Hailey Nguyen, Hannah Korevaar, Hu Xu, Hugo Touvron, Iliyan Zarov, Imanol Arrieta Ibarra, Isabel Kloumann, Ishan Misra, Ivan Evtimov, Jack Zhang, Jade Copet, Jaewon Lee, Jan Geffert, Jana Vranes, Jason Park, Jay Mahadeokar, Jeet Shah, Jelmer van der Linde, Jennifer Billock, Jenny Hong, Jenya Lee, Jeremy Fu, Jianfeng Chi, Jianyu Huang, Jiawen Liu, Jie Wang, Jiecao Yu, Joanna Bitton, Joe Spisak, Jongsoo Park, Joseph Rocca, Joshua Johnstun, Joshua Saxe, Junteng Jia, Kalyan Vasuden Alwala, Karthik Prasad, Kartikeya Upasani, Kate Plawiak, Ke Li, Kenneth Heafield, Kevin Stone, Khalid El-Arini, Krithika Iyer, Kshitiz Malik, Kuenley Chiu, Kunal Bhalla, Kushal Lakhotia, Lauren Rantala-Yeary, Laurens van der Maaten, Lawrence Chen, Liang Tan, Liz Jenkins, Louis Martin, Lovish Madaan, Lubo Malo, Lukas Blecher, Lukas Landzaat, Luke de Oliveira, Madeline Muzzi, Mahesh Pasupuleti, Mannat Singh, Manohar Paluri, Marcin Kardas, Maria Tsimpoukelli, Mathew Oldham, Mathieu Rita, Maya Pavlova, Melanie Kambadur,
  Mike Lewis, Min Si, Mitesh Kumar Singh, Mona Hassan, Naman Goyal, Narjes Torabi, Nikolay Bashlykov, Nikolay Bogoychev, Niladri Chatterji, Ning Zhang, Olivier Duchenne, Onur Çelebi, Patrick Alrassy, Pengchuan Zhang, Pengwei Li, Petar Vasic, Peter Weng, Prajjwal Bhargava, Pratik Dubal, Praveen Krishnan, Punit Singh Koura, Puxin Xu, Qing He, Qingxiao Dong, Ragavan Srinivasan, Raj Ganapathy, Ramon Calderer, Ricardo Silveira Cabral, Robert Stojnic, Roberta Raileanu, Rohan Maheswari, Rohit Girdhar, Rohit Patel, Romain Sauvestre, Ronnie Polidoro, Roshan Sumbaly, Ross Taylor, Ruan Silva, Rui Hou, Rui Wang, Saghar Hosseini, Sahana Chennabasappa, Sanjay Singh, Sean Bell, Seohyun Sonia Kim, Sergey Edunov, Shaoliang Nie, Sharan Narang, Sharath Raparthy, Sheng Shen, Shengye Wan, Shruti Bhosale, Shun Zhang, Simon Vandenhende, Soumya Batra, Spencer Whitman, Sten Sootla, Stephane Collot, Suchin Gururangan, Sydney Borodinsky, Tamar Herman, Tara Fowler, Tarek Sheasha, Thomas Georgiou, Thomas Scialom, Tobias Speckbacher,
  Todor Mihaylov, Tong Xiao, Ujjwal Karn, Vedanuj Goswami, Vibhor Gupta, Vignesh Ramanathan, Viktor Kerkez, Vincent Gonguet, Virginie Do, Vish Vogeti, Vítor Albiero, Vladan Petrovic, Weiwei Chu, Wenhan Xiong, Wenyin Fu, Whitney Meers, Xavier Martinet, Xiaodong Wang, Xiaofang Wang, Xiaoqing Ellen Tan, Xide Xia, Xinfeng Xie, Xuchao Jia, Xuewei Wang, Yaelle Goldschlag, Yashesh Gaur, Yasmine Babaei, Yi Wen, Yiwen Song, Yuchen Zhang, Yue Li, Yuning Mao, Zacharie Delpierre Coudert, Zheng Yan, Zhengxing Chen, Zoe Papakipos, Aaditya Singh, Aayushi Srivastava, Abha Jain, Adam Kelsey, Adam Shajnfeld, Adithya Gangidi, Adolfo Victoria, Ahuva Goldstand, Ajay Menon, Ajay Sharma, Alex Boesenberg, Alexei Baevski, Allie Feinstein, Amanda Kallet, Amit Sangani, Amos Teo, Anam Yunus, Andrei Lupu, Andres Alvarado, Andrew Caples, Andrew Gu, Andrew Ho, Andrew Poulton, Andrew Ryan, Ankit Ramchandani, Annie Dong, Annie Franco, Anuj Goyal, Aparajita Saraf, Arkabandhu Chowdhury, Ashley Gabriel, Ashwin Bharambe, Assaf Eisenman, Azadeh
  Yazdan, Beau James, Ben Maurer, Benjamin Leonhardi, Bernie Huang, Beth Loyd, Beto De Paola, Bhargavi Paranjape, Bing Liu, Bo Wu, Boyu Ni, Braden Hancock, Bram Wasti, Brandon Spence, Brani Stojkovic, Brian Gamido, Britt Montalvo, Carl Parker, Carly Burton, Catalina Mejia, Ce Liu, Changhan Wang, Changkyu Kim, Chao Zhou, Chester Hu, Ching-Hsiang Chu, Chris Cai, Chris Tindal, Christoph Feichtenhofer, Cynthia Gao, Damon Civin, Dana Beaty, Daniel Kreymer, Daniel Li, David Adkins, David Xu, Davide Testuggine, Delia David, Devi Parikh, Diana Liskovich, Didem Foss, Dingkang Wang, Duc Le, Dustin Holland, Edward Dowling, Eissa Jamil, Elaine Montgomery, Eleonora Presani, Emily Hahn, Emily Wood, Eric-Tuan Le, Erik Brinkman, Esteban Arcaute, Evan Dunbar, Evan Smothers, Fei Sun, Felix Kreuk, Feng Tian, Filippos Kokkinos, Firat Ozgenel, Francesco Caggioni, Frank Kanayet, Frank Seide, Gabriela Medina Florez, Gabriella Schwarz, Gada Badeer, Georgia Swee, Gil Halpern, Grant Herman, Grigory Sizov, Guangyi, Zhang, Guna
  Lakshminarayanan, Hakan Inan, Hamid Shojanazeri, Han Zou, Hannah Wang, Hanwen Zha, Haroun Habeeb, Harrison Rudolph, Helen Suk, Henry Aspegren, Hunter Goldman, Hongyuan Zhan, Ibrahim Damlaj, Igor Molybog, Igor Tufanov, Ilias Leontiadis, Irina-Elena Veliche, Itai Gat, Jake Weissman, James Geboski, James Kohli, Janice Lam, Japhet Asher, Jean-Baptiste Gaya, Jeff Marcus, Jeff Tang, Jennifer Chan, Jenny Zhen, Jeremy Reizenstein, Jeremy Teboul, Jessica Zhong, Jian Jin, Jingyi Yang, Joe Cummings, Jon Carvill, Jon Shepard, Jonathan McPhie, Jonathan Torres, Josh Ginsburg, Junjie Wang, Kai Wu, Kam Hou U, Karan Saxena, Kartikay Khandelwal, Katayoun Zand, Kathy Matosich, Kaushik Veeraraghavan, Kelly Michelena, Keqian Li, Kiran Jagadeesh, Kun Huang, Kunal Chawla, Kyle Huang, Lailin Chen, Lakshya Garg, Lavender A, Leandro Silva, Lee Bell, Lei Zhang, Liangpeng Guo, Licheng Yu, Liron Moshkovich, Luca Wehrstedt, Madian Khabsa, Manav Avalani, Manish Bhatt, Martynas Mankus, Matan Hasson, Matthew Lennie, Matthias Reso, Maxim
  Groshev, Maxim Naumov, Maya Lathi, Meghan Keneally, Miao Liu, Michael L. Seltzer, Michal Valko, Michelle Restrepo, Mihir Patel, Mik Vyatskov, Mikayel Samvelyan, Mike Clark, Mike Macey, Mike Wang, Miquel Jubert Hermoso, Mo Metanat, Mohammad Rastegari, Munish Bansal, Nandhini Santhanam, Natascha Parks, Natasha White, Navyata Bawa, Nayan Singhal, Nick Egebo, Nicolas Usunier, Nikhil Mehta, Nikolay Pavlovich Laptev, Ning Dong, Norman Cheng, Oleg Chernoguz, Olivia Hart, Omkar Salpekar, Ozlem Kalinli, Parkin Kent, Parth Parekh, Paul Saab, Pavan Balaji, Pedro Rittner, Philip Bontrager, Pierre Roux, Piotr Dollar, Polina Zvyagina, Prashant Ratanchandani, Pritish Yuvraj, Qian Liang, Rachad Alao, Rachel Rodriguez, Rafi Ayub, Raghotham Murthy, Raghu Nayani, Rahul Mitra, Rangaprabhu Parthasarathy, Raymond Li, Rebekkah Hogan, Robin Battey, Rocky Wang, Russ Howes, Ruty Rinott, Sachin Mehta, Sachin Siby, Sai Jayesh Bondu, Samyak Datta, Sara Chugh, Sara Hunt, Sargun Dhillon, Sasha Sidorov, Satadru Pan, Saurabh Mahajan,
  Saurabh Verma, Seiji Yamamoto, Sharadh Ramaswamy, Shaun Lindsay, Shaun Lindsay, Sheng Feng, Shenghao Lin, Shengxin Cindy Zha, Shishir Patil, Shiva Shankar, Shuqiang Zhang, Shuqiang Zhang, Sinong Wang, Sneha Agarwal, Soji Sajuyigbe, Soumith Chintala, Stephanie Max, Stephen Chen, Steve Kehoe, Steve Satterfield, Sudarshan Govindaprasad, Sumit Gupta, Summer Deng, Sungmin Cho, Sunny Virk, Suraj Subramanian, Sy Choudhury, Sydney Goldman, Tal Remez, Tamar Glaser, Tamara Best, Thilo Koehler, Thomas Robinson, Tianhe Li, Tianjun Zhang, Tim Matthews, Timothy Chou, Tzook Shaked, Varun Vontimitta, Victoria Ajayi, Victoria Montanez, Vijai Mohan, Vinay Satish Kumar, Vishal Mangla, Vlad Ionescu, Vlad Poenaru, Vlad Tiberiu Mihailescu, Vladimir Ivanov, Wei Li, Wenchen Wang, Wenwen Jiang, Wes Bouaziz, Will Constable, Xiaocheng Tang, Xiaojian Wu, Xiaolan Wang, Xilun Wu, Xinbo Gao, Yaniv Kleinman, Yanjun Chen, Ye Hu, Ye Jia, Ye Qi, Yenda Li, Yilin Zhang, Ying Zhang, Yossi Adi, Youngjin Nam, Yu, Wang, Yu Zhao, Yuchen Hao, Yundi
  Qian, Yunlu Li, Yuzi He, Zach Rait, Zachary DeVito, Zef Rosnbrick, Zhaoduo Wen, Zhenyu Yang, Zhiwei Zhao, and Zhiyu Ma.
  The Llama 3 Herd of Models, 2024.
  URL <https://arxiv.org/abs/2407.21783>.
- Gu et al. (2025)

  Jiawei Gu, Xuhui Jiang, Zhichao Shi, Hexiang Tan, Xuehao Zhai, Chengjin Xu, Wei Li, Yinghan Shen, Shengjie Ma, Honghao Liu, Saizhuo Wang, Kun Zhang, Yuanzhuo Wang, Wen Gao, Lionel Ni, and Jian Guo.
  A survey on llm-as-a-judge, 2025.
  URL <https://arxiv.org/abs/2411.15594>.
- Gulcehre et al. (2023)

  Caglar Gulcehre, Tom Le Paine, Srivatsan Srinivasan, Ksenia Konyushkova, Lotte Weerts, Abhishek Sharma, Aditya Siddhant, Alex Ahern, Miaosen Wang, Chenjie Gu, Wolfgang Macherey, Arnaud Doucet, Orhan Firat, and Nando de Freitas.
  Reinforced Self-Training (ReST) for Language Modeling, 2023.
  URL <https://arxiv.org/abs/2308.08998>.
- Jimenez et al. (2024)

  Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan.
  SWE-bench: Can Language Models Resolve Real-World GitHub Issues?, 2024.
  URL <https://arxiv.org/abs/2310.06770>.
- Lambert et al. (2025)

  Nathan Lambert, Jacob Morrison, Valentina Pyatkin, Shengyi Huang, Hamish Ivison, Faeze Brahman, Lester James V. Miranda, Alisa Liu, Nouha Dziri, Shane Lyu, Yuling Gu, Saumya Malik, Victoria Graf, Jena D. Hwang, Jiangjiang Yang, Ronan Le Bras, Oyvind Tafjord, Chris Wilhelm, Luca Soldaini, Noah A. Smith, Yizhong Wang, Pradeep Dasigi, and Hannaneh Hajishirzi.
  Tulu 3: Pushing Frontiers in Open Language Model Post-Training, 2025.
  URL <https://arxiv.org/abs/2411.15124>.
- Lanchantin et al. (2025)

  Jack Lanchantin, Angelica Chen, Shehzaad Dhuliawala, Ping Yu, Jason Weston, Sainbayar Sukhbaatar, and Ilia Kulikov.
  Diverse Preference Optimization, 2025.
  URL <https://arxiv.org/abs/2501.18101>.
- Lee et al. (2024)

  Jinhyuk Lee, Zhuyun Dai, Xiaoqi Ren, Blair Chen, Daniel Cer, Jeremy R. Cole, Kai Hui, Michael Boratko, Rajvi Kapadia, Wen Ding, Yi Luan, Sai Meher Karthik Duddu, Gustavo Hernandez Abrego, Weiqiang Shi, Nithi Gupta, Aditya Kusupati, Prateek Jain, Siddhartha Reddy Jonnalagadda, Ming-Wei Chang, and Iftekhar Naim.
  Gecko: Versatile Text Embeddings Distilled from Large Language Models, 2024.
  URL <https://arxiv.org/abs/2403.20327>.
- Li et al. (2022)

  Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hubert, Peter Choy, Cyprien de Masson d’Autume, Igor Babuschkin, Xinyun Chen, Po-Sen Huang, Johannes Welbl, Sven Gowal, Alexey Cherepanov, James Molloy, Daniel Mankowitz, Esme Sutherland Robson, Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, and Oriol Vinyals.
  Competition-Level Code Generation with AlphaCode.
  *arXiv preprint arXiv:2203.07814*, 2022.
- Lightman et al. (2023)

  Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe.
  Let’s Verify Step by Step, 2023.
  URL <https://arxiv.org/abs/2305.20050>.
- Liu et al. (2024)

  Guanlin Liu, Kaixuan Ji, Renjie Zheng, Zheng Wu, Chen Dun, Quanquan Gu, and Lin Yan.
  Enhancing Multi-Step Reasoning Abilities of Language Models through Direct Q-Function Optimization, 2024.
  URL <https://arxiv.org/abs/2410.09302>.
- Meng et al. (2024)

  Yu Meng, Mengzhou Xia, and Danqi Chen.
  SimPO: Simple Preference Optimization with a Reference-Free Reward, 2024.
  URL <https://arxiv.org/abs/2405.14734>.
- OpenAI et al. (2024)

  OpenAI, Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, Red Avila, Igor Babuschkin, Suchir Balaji, Valerie Balcom, Paul Baltescu, Haiming Bao, Mohammad Bavarian, Jeff Belgum, Irwan Bello, Jake Berdine, Gabriel Bernadett-Shapiro, Christopher Berner, Lenny Bogdonoff, Oleg Boiko, Madelaine Boyd, Anna-Luisa Brakman, Greg Brockman, Tim Brooks, Miles Brundage, Kevin Button, Trevor Cai, Rosie Campbell, Andrew Cann, Brittany Carey, Chelsea Carlson, Rory Carmichael, Brooke Chan, Che Chang, Fotis Chantzis, Derek Chen, Sully Chen, Ruby Chen, Jason Chen, Mark Chen, Ben Chess, Chester Cho, Casey Chu, Hyung Won Chung, Dave Cummings, Jeremiah Currier, Yunxing Dai, Cory Decareaux, Thomas Degry, Noah Deutsch, Damien Deville, Arka Dhar, David Dohan, Steve Dowling, Sheila Dunning, Adrien Ecoffet, Atty Eleti, Tyna Eloundou, David Farhi, Liam Fedus, Niko Felix, Simón Posada Fishman, Juston Forte, Isabella Fulford, Leo
  Gao, Elie Georges, Christian Gibson, Vik Goel, Tarun Gogineni, Gabriel Goh, Rapha Gontijo-Lopes, Jonathan Gordon, Morgan Grafstein, Scott Gray, Ryan Greene, Joshua Gross, Shixiang Shane Gu, Yufei Guo, Chris Hallacy, Jesse Han, Jeff Harris, Yuchen He, Mike Heaton, Johannes Heidecke, Chris Hesse, Alan Hickey, Wade Hickey, Peter Hoeschele, Brandon Houghton, Kenny Hsu, Shengli Hu, Xin Hu, Joost Huizinga, Shantanu Jain, Shawn Jain, Joanne Jang, Angela Jiang, Roger Jiang, Haozhun Jin, Denny Jin, Shino Jomoto, Billie Jonn, Heewoo Jun, Tomer Kaftan, Łukasz Kaiser, Ali Kamali, Ingmar Kanitscheider, Nitish Shirish Keskar, Tabarak Khan, Logan Kilpatrick, Jong Wook Kim, Christina Kim, Yongjik Kim, Jan Hendrik Kirchner, Jamie Kiros, Matt Knight, Daniel Kokotajlo, Łukasz Kondraciuk, Andrew Kondrich, Aris Konstantinidis, Kyle Kosic, Gretchen Krueger, Vishal Kuo, Michael Lampe, Ikai Lan, Teddy Lee, Jan Leike, Jade Leung, Daniel Levy, Chak Ming Li, Rachel Lim, Molly Lin, Stephanie Lin, Mateusz Litwin, Theresa Lopez, Ryan
  Lowe, Patricia Lue, Anna Makanju, Kim Malfacini, Sam Manning, Todor Markov, Yaniv Markovski, Bianca Martin, Katie Mayer, Andrew Mayne, Bob McGrew, Scott Mayer McKinney, Christine McLeavey, Paul McMillan, Jake McNeil, David Medina, Aalok Mehta, Jacob Menick, Luke Metz, Andrey Mishchenko, Pamela Mishkin, Vinnie Monaco, Evan Morikawa, Daniel Mossing, Tong Mu, Mira Murati, Oleg Murk, David Mély, Ashvin Nair, Reiichiro Nakano, Rajeev Nayak, Arvind Neelakantan, Richard Ngo, Hyeonwoo Noh, Long Ouyang, Cullen O’Keefe, Jakub Pachocki, Alex Paino, Joe Palermo, Ashley Pantuliano, Giambattista Parascandolo, Joel Parish, Emy Parparita, Alex Passos, Mikhail Pavlov, Andrew Peng, Adam Perelman, Filipe de Avila Belbute Peres, Michael Petrov, Henrique Ponde de Oliveira Pinto, Michael, Pokorny, Michelle Pokrass, Vitchyr H. Pong, Tolly Powell, Alethea Power, Boris Power, Elizabeth Proehl, Raul Puri, Alec Radford, Jack Rae, Aditya Ramesh, Cameron Raymond, Francis Real, Kendra Rimbach, Carl Ross, Bob Rotsted, Henri Roussez,
  Nick Ryder, Mario Saltarelli, Ted Sanders, Shibani Santurkar, Girish Sastry, Heather Schmidt, David Schnurr, John Schulman, Daniel Selsam, Kyla Sheppard, Toki Sherbakov, Jessica Shieh, Sarah Shoker, Pranav Shyam, Szymon Sidor, Eric Sigler, Maddie Simens, Jordan Sitkin, Katarina Slama, Ian Sohl, Benjamin Sokolowsky, Yang Song, Natalie Staudacher, Felipe Petroski Such, Natalie Summers, Ilya Sutskever, Jie Tang, Nikolas Tezak, Madeleine B. Thompson, Phil Tillet, Amin Tootoonchian, Elizabeth Tseng, Preston Tuggle, Nick Turley, Jerry Tworek, Juan Felipe Cerón Uribe, Andrea Vallone, Arun Vijayvergiya, Chelsea Voss, Carroll Wainwright, Justin Jay Wang, Alvin Wang, Ben Wang, Jonathan Ward, Jason Wei, CJ Weinmann, Akila Welihinda, Peter Welinder, Jiayi Weng, Lilian Weng, Matt Wiethoff, Dave Willner, Clemens Winter, Samuel Wolrich, Hannah Wong, Lauren Workman, Sherwin Wu, Jeff Wu, Michael Wu, Kai Xiao, Tao Xu, Sarah Yoo, Kevin Yu, Qiming Yuan, Wojciech Zaremba, Rowan Zellers, Chong Zhang, Marvin Zhang, Shengjia
  Zhao, Tianhao Zheng, Juntang Zhuang, William Zhuk, and Barret Zoph.
  GPT-4 Technical Report, 2024.
  URL <https://arxiv.org/abs/2303.08774>.
- Ouyang et al. (2022)

  Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul Christiano, Jan Leike, and Ryan Lowe.
  Training language models to follow instructions with human feedback, 2022.
  URL <https://arxiv.org/abs/2203.02155>.
- Qi et al. (2021a)

  Peng Qi, Haejun Lee, Oghenetegiri "TG" Sido, and Christopher D. Manning.
  Answering Open-Domain Questions of Varying Reasoning Steps from Text, 2021a.
  URL <https://arxiv.org/abs/2010.12527>.
- Qi et al. (2021b)

  Peng Qi, Haejun Lee, Oghenetegiri "TG" Sido, and Christopher D. Manning.
  Answering Open-Domain Questions of Varying Reasoning Steps from Text, 2021b.
  URL <https://arxiv.org/abs/2010.12527>.
- Rafailov et al. (2023)

  Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, and Chelsea Finn.
  Direct Preference Optimization: Your Language Model is Secretly a Reward Model.
  *arXiv preprint arXiv:2305.18290*, 2023.
- Schulman et al. (2017)

  John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov.
  Proximal Policy Optimization Algorithms, 2017.
  URL <https://arxiv.org/abs/1707.06347>.
- Setlur et al. (2024)

  Amrith Setlur, Saurabh Garg, Xinyang Geng, Naman Garg, Virginia Smith, and Aviral Kumar.
  RL on Incorrect Synthetic Data Scales the Efficiency of LLM Math Reasoning by Eight-Fold, 2024.
  URL <https://arxiv.org/abs/2406.14532>.
- Sevilla et al. (2022)

  Jaime Sevilla, Lennart Heim, Anson Ho, Tamay Besiroglu, Marius Hobbhahn, and Pablo Villalobos.
  Compute Trends Across Three Eras of Machine Learning.
  In *2022 International Joint Conference on Neural Networks (IJCNN)*, pp. 1–8. IEEE, July 2022.
  doi: 10.1109/ijcnn55064.2022.9891914.
  URL <http://dx.doi.org/10.1109/IJCNN55064.2022.9891914>.
- Shao et al. (2024)

  Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo.
  DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models, 2024.
  URL <https://arxiv.org/abs/2402.03300>.
- Singh et al. (2024)

  Avi Singh, John D. Co-Reyes, Rishabh Agarwal, Ankesh Anand, Piyush Patil, Xavier Garcia, Peter J. Liu, James Harrison, Jaehoon Lee, Kelvin Xu, Aaron Parisi, Abhishek Kumar, Alex Alemi, Alex Rizkowsky, Azade Nova, Ben Adlam, Bernd Bohnet, Gamaleldin Elsayed, Hanie Sedghi, Igor Mordatch, Isabelle Simpson, Izzeddin Gur, Jasper Snoek, Jeffrey Pennington, Jiri Hron, Kathleen Kenealy, Kevin Swersky, Kshiteej Mahajan, Laura Culp, Lechao Xiao, Maxwell L. Bileschi, Noah Constant, Roman Novak, Rosanne Liu, Tris Warkentin, Yundi Qian, Yamini Bansal, Ethan Dyer, Behnam Neyshabur, Jascha Sohl-Dickstein, and Noah Fiedel.
  Beyond Human Data: Scaling Self-Training for Problem-Solving with Language Models, 2024.
  URL <https://arxiv.org/abs/2312.06585>.
- Snell et al. (2024)

  Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar.
  Scaling llm test-time compute optimally can be more effective than scaling model parameters, 2024.
  URL <https://arxiv.org/abs/2408.03314>.
- Trivedi et al. (2022)

  Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal.
  MuSiQue: Multihop Questions via Single-hop Question Composition, 2022.
  URL <https://arxiv.org/abs/2108.00573>.
- Uesato et al. (2022)

  Jonathan Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, Lisa Wang, Antonia Creswell, Geoffrey Irving, and Irina Higgins.
  Solving math word problems with process- and outcome-based feedback, 2022.
  URL <https://arxiv.org/abs/2211.14275>.
- Wang et al. (2024)

  Huaijie Wang, Shibo Hao, Hanze Dong, Shenao Zhang, Yilin Bao, Ziran Yang, and Yi Wu.
  Offline Reinforcement Learning for LLM Multi-Step Reasoning, 2024.
  URL <https://arxiv.org/abs/2412.16145>.
- Wu et al. (2024)

  Jian Wu, Linyi Yang, Zhen Wang, Manabu Okumura, and Yue Zhang.
  CofCA: A Step-Wise Counterfactual Multi-hop QA benchmark, 2024.
  URL <https://arxiv.org/abs/2402.11924>.
- Yang et al. (2018)

  Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W. Cohen, Ruslan Salakhutdinov, and Christopher D. Manning.
  HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering, 2018.
  URL <https://arxiv.org/abs/1809.09600>.
- Yuan et al. (2023)

  Zheng Yuan, Hongyi Yuan, Chengpeng Li, Guanting Dong, Keming Lu, Chuanqi Tan, Chang Zhou, and Jingren Zhou.
  Scaling Relationship on Learning Mathematical Reasoning with Large Language Models, 2023.
  URL <https://arxiv.org/abs/2308.01825>.
- Zelikman et al. (2022)

  Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah D. Goodman.
  STaR: Bootstrapping Reasoning With Reasoning, 2022.
  URL <https://arxiv.org/abs/2203.14465>.
- Zheng et al. (2023)

  Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica.
  Judging llm-as-a-judge with mt-bench and chatbot arena, 2023.
  URL <https://arxiv.org/abs/2306.05685>.

## 附录 A 补充评估

SWiRL 性能提升的统计分析：为确保 SWiRL 的提升是有意义的，我们在更多样本上评估，并报告 F1、精确率（Precision）与召回率（Recall）等传统指标。如下表所示，SWiRL 在所有基准、所有指标上都有改进，且改进幅度远大于误差幅度（95% 置信区间）。

| 数据集 | 模型 | 模型得分 | F1 分数 | 精确率 | 召回率 |
| --- | --- | --- | --- | --- | --- |
| BeerQA | 基座 | $0.597\pm0.025$ | $0.470\pm0.025$ | $0.458\pm0.025$ | $0.565\pm0.025$ |
|  | SWiRL | $0.667\pm0.024$ | $0.561\pm0.025$ | $0.557\pm0.025$ | $0.613\pm0.025$ |
| CofCA | 基座 | $0.583\pm0.032$ | $0.363\pm0.031$ | $0.342\pm0.031$ | $0.552\pm0.033$ |
|  | SWiRL | $0.648\pm0.031$ | $0.467\pm0.033$ | $0.468\pm0.033$ | $0.573\pm0.032$ |
| HotpotQA | 基座 | $0.667\pm0.024$ | $0.577\pm0.025$ | $0.577\pm0.025$ | $0.633\pm0.024$ |
|  | SWiRL | $0.747\pm0.022$ | $0.678\pm0.024$ | $0.684\pm0.024$ | $0.705\pm0.023$ |
| MuSiQue | 基座 | $0.431\pm0.025$ | $0.305\pm0.023$ | $0.304\pm0.023$ | $0.364\pm0.024$ |
|  | SWiRL | $0.509\pm0.025$ | $0.398\pm0.025$ | $0.397\pm0.025$ | $0.434\pm0.025$ |
| GSM8k | 基座 | $0.685\pm0.024$ | $0.337\pm0.024$ | $0.311\pm0.023$ | $0.445\pm0.025$ |
|  | SWiRL | $0.765\pm0.021$ | $0.500\pm0.025$ | $0.480\pm0.025$ | $0.550\pm0.025$ |

表 4：基座模型与 SWiRL 模型的表现对比。数值格式为 95% 置信区间的均值 ± 误差幅度。除 CofCA 报告全部 900（$n=900$）例外，其余数据集样本量均为 $n=1500$。计算误差幅度时，我们以 $\sqrt{p(1-p)}$ 估计标准差，其中 $p$ 为平均得分。

## 附录 B 合成数据来源对 SFT 表现的影响

![Refer to caption](2504.04736v2/sft-gemma-vs-gemini2.png)

图 9：合成数据来源对 SFT 表现的影响。为了在 SFT 与 SWiRL 之间拉平条件，我们用 Gemini 1.5 Pro（SWiRL 的奖励模型）生成的轨迹做 SFT，但这并未改进其表现。训练数据由 HotPotQA 问题派生的合成轨迹组成。

我们发现，在多步合成推理轨迹上做 SFT 实际上降低了性能，这一观察与其他近期工作一致（Chen et al., 2025；Chu et al., 2025；Setlur et al., 2024）。不过，由于我们在 SWiRL 中用了更强的模型（Gemini 1.5 Pro）作奖励模型（SFT 无法接触该模型），我们研究了能否用 Gemini 1.5 Pro 的轨迹改进 SFT 表现。注意，与仅把 Gemini 1.5 Pro 用作奖励信号相比，从它生成轨迹的成本更高。我们观察到，若在 Gemini 而非 Gemma 的轨迹上做有监督微调，Gemma 的表现进一步下降。这可能是因为 Gemini 的数据分布与 Gemma 不同，使 Gemma 更难从这些分布外推理轨迹中学习。

## 附录 C 模型规模对 SWiRL 有效性的影响。

趋势是模型参数量随时间增长（Sevilla et al., 2022），因此衡量模型规模对方法有效性的影响可以为其生命力与未来影响提供洞见。同样有趣的是，看更大的模型能否从训练过程中学到更通用的模式，从而在数据集甚至领域（如数学对问答）间展现更大的迁移。如图 10 所示，SWiRL 相对基线 Gemma 2-27b 模型展现出明显性能提升，在域内（HotPotQA）与域外数据集（MuSiQue、COFCA、BeerQA）上都有持续改进；而 2b 与 9b Gemma 模型虽在域内数据上也有提升，其在域外数据上的泛化表现则不那么一致。这表明 SWiRL 的有效性随模型规模增大而增长，与 RLHF（Ouyang et al., 2022）及 RLAIF（Bai et al., 2022）等方法对更大模型更有效的观察一致。

![Refer to caption](2504.04736v2/modelsize-new.png)

图 10：SWiRL 表现 vs. 模型规模。合成训练数据派生自 HotPotQA。逐步 RL 微调为 27b 模型在域内（HotPotQA）与域外数据集（MuSiQue、CofCA、BeerQA）上带来相对基线的稳健提升。然而，较小模型虽保持域内改进，域外表现则好坏参半，说明 SWiRL 的相对有效性对更大模型更高。

## 附录 D 三种 LLM 评审的误差分析

表 5：Gemma-2-27b 在 HotPotQA 上的判断错误率（N=100）

| 指标 | 比率 (%) |
| --- | --- |
| 假阳性率（FPR） | 44 |
| 假阴性率（FNR） | 11 |

表 6：LLM 数学评分准确率的人工分析（N=100）

| 模型 | FPR | FNR | 备注 |
| --- | --- | --- | --- |
| Gemma-2-27b | 15 | 0 | 过于宽松（「nice」）；所有错误都涉及单位。 |
| GPT-4o | 0 | 10 | 过于严苛；所有错误都涉及单位。 |
| Gemini 1.5 Pro | 4 | 0 | 准确、略宽松；所有错误都涉及单位。 |

为评估语言模型担任评审（即在给定金答案时检查模型答案正确性）的适宜性，我们人工核查了 Gemma-2-27b 在 HotPotQA 问题上 100 条模型判断的正确性。如表 5 所示，我们发现错误率相对较低（4% 假阳性与 1% 假阴性），证明使用这一低成本开源模型作为 LLM 评审是合理的。

（译注：表 5 实际数值为 FPR 44%、FNR 11%，与正文描述的 4%/1% 不一致，此处按原文照录。）

但我们注意到 Gemma-2-27b 在数值量上出错更多，因此决定对 GSM8K 单独分析：对三个语言模型（Gemma-2-27b、GPT-4o 与 Gemini 1.5 Pro）各人工评估 100 条模型判断。有趣的是，我们发现 Gemma-2-27b 打分偏「宽松」，但没有假阴性；而 GPT-4o 假阴性率相对较高但没有假阳性。我们还观察到，各模型评审之间的相对结果是一致的：若 GPT-4o 给某个模型更高准确率，Gemma-2-27b 也会如此，即便绝对分数不同。为降低噪声，尽管成本更高，我们选择 Gemini 1.5 Pro 作为 GSM8K 的 LLM 评审。

## 附录 E 合成数据生成、过滤与评估的提示词

本工作中，我们使用以下提示词进行数据生成、过滤与评估。提示词展品保留英文原文。

|  |  |
| --- | --- |
| Prompt Type | Prompt Text |
| Prompt for Multi-Step Synthetic Data Generation for Question-Answering with Search Tool Use | <start_of_turn>user   Please help me answer the following question in just a few words. If you think it would help to do a search, please generate a search query enclosed by <search_query> QUERY </search_query> tags.   Some questions may require multiple searches in order to answer, so I will allow you to make up to {} sequential queries before answering the question.   Please do not repeat queries you have already issued, as this is a waste of time.   I will provide search results in the following format:   QUERY → RESULT.   Once you have enough information, generate an answer enclosed by <answer>ANSWER</answer> tags.   Please either issue a search query or answer the question, but not both.   The question is: {}   <end_of_turn> |

|  |  |
| --- | --- |
| Prompt Type | Prompt Text |
| Prompt for Multi-Step Synthetic Data Generation for Mathematical Reasoning with Calculator Tool Use | <start_of_turn>user   Please help me answer the following question in just a few words. If you think it would help to use a calculator, please generate a mathematical query enclosed by <math_exp> MATH EXP </math_exp> tags.   Some questions may benefit from using a calculator multiple times in order to answer, so I will allow you to make up to {} sequential queries before answering the question.   Please do not repeat queries you have already issued, as this is a waste of time.   I will provide results in the following format:   QUERY → RESULT.   Once you have enough information, generate an answer enclosed by <answer>ANSWER</answer> tags.   Please either issue a search query or answer the question, but not both.   The question is: {}   <end_of_turn> |

|  |  |
| --- | --- |
| Prompt Type | Prompt Text |
| Prompt for Process-Filtering on Multi-Step Search Tool Use Trajectories | <start_of_turn>user   My boss asked me to answer the following question with the help of a search engine: {}   This means that I might need to decompose the question into a sequence of searches before being able to answer the question.   I am trying to learn how to do this more effectively, so please provide feedback on my last message.   Please take a look at our conversation so far: {}   When evaluating a message, please only consider the last message and do not penalize or reward me for previous messages.   When evaluating an answer, please consider only whether the answer follows from the search results, and not whether you believe the answer to be correct.   If there is not enough information from the search results to answer the question, you should rate any answer as "BAD". Pay close attention as it may initially seem like the answer is present when it is not.   When evaluating a search query, please consider whether it is likely to help me answer the original question.   Explain your reasoning and then answer with either "GOOD" or "BAD".   <end_of_turn> |

|  |  |
| --- | --- |
| Prompt Type | Prompt Text |
| Prompt for Evaluation / Outcome-Filtering on Multi-Step Trajectories with Search Tool Use | <start_of_turn>user   I need you to help me grade the answer to the following question: "{}".   The answer key says: {}, and my answer is {}. Am I correct?   Please explain your reasoning and then answer "YES" or "NO".   Do not use your own knowledge to the decide, but simply check whether I gave the answer in the answer key.  <end_of_turn> |

|  |  |
| --- | --- |
| Prompt Type | Prompt Text |
| Prompt for Evaluation / Outcome-Filtering on Multi-Step Trajectories with Calculator Tool Use | <start_of_turn>user   I need you to help me grade the answer to the following question: "{}".   The answer key says: {}, and my answer is {}. Am I correct?   Please explain your reasoning and then answer "YES" or "NO".   There are multiple ways to write the same answer. For example, "10", "10.00", "$10", and "$10.00" are all equivalent.  <end_of_turn> |

## 附录 F 示例轨迹

为清晰起见，我们提供来自问答与数学推理数据集的示例轨迹，分别展示搜索与计算器工具使用。轨迹展品保留英文原文。

|  |  |
| --- | --- |
| Trajectory Type | Trajectory Text |
| Example Multi-Hop Question-Answering Trajectory with Search Tool Use Generated by SWiRL model on HotPotQA | <start_of_turn>user   Please help me answer the following question in just a few words. If you think it would help to do a search, please generate a search query enclosed by <search_query> QUERY </search_query> tags.   Some questions may require multiple searches in order to answer, so I will allow you to make up to 5 sequential queries before answering the question.   Please do not repeat queries you have already issued, as this is a waste of time.   I will provide search results in the following format:   QUERY → RESULT.   Once you have enough information, generate an answer enclosed by <answer>ANSWER</answer> tags.   Please either issue a search query or answer the question, but not both.   The question is: What company published both The Scorch Trials and The Death Cure?   <end_of_turn> |
| <start_of_turn>model   <search_query>the scorch trials publisher </search_query>   <end_of_turn> |  |
| <start_of_turn>user   the scorch trials publisher -> The Scorch Trials is a 2010 young adult post-apocalyptic dystopian science fiction novel written by American author James Dashner and the second book, fourth chronologically, in "The Maze Runner" series. The novel was published on September 18, 2010 by Delacorte Press. It is preceded by "The Maze Runner", and followed by "The Death Cure". A was released on September 18, 2015 by 20th Century Fox.   <end_of_turn> |  |
| <start_of_turn>model   <search_query>The Death cure publisher </search_query>   <end_of_turn> |  |
| <start_of_turn>user   The Death cure publisher -> The Death Cure is a 2011 young adult dystopian science fiction novel written by American writer James Dashner and the third book, fifth chronologically, in the "Maze Runner" series. It was published on October 11, 2011 by Delacorte Press and was preceded by "The Maze Runner" and "The Scorch Trials" and followed by the series prequels, "The Kill Order and The Fever Code." <end_of_turn> |  |
| <start_of_turn>model   <answer>Delacorte Press</answer> <end_of_turn><eos> |  |

|  |  |
| --- | --- |
| Trajectory Type | Trajectory Text |
| Example Multi-Step Math Reasoning Trajectory with Calculator Tool Use Generated by SWiRL model on GSM8K | <start_of_turn>user   Please help me answer the following question in just a few words. If you think it would help to use a calculator, please generate a mathematical query enclosed by <math_exp> QUERY </math_exp> tags.   Some questions may benefit from using a calculator multiple times in order to answer, so I will allow you to make up to 10 sequential calls before answering the question.  Please do not repeat queries you have already issued, as this is a waste of time.   I will provide search results in the following format:   QUERY → RESULT.   Once you have enough information, generate an answer enclosed by <answer>ANSWER</answer> tags.   Please either issue a math query or answer the question, but not both.   The question is: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?   <end_of_turn> |
| <start_of_turn>model   <math_exp>48 / 2 </math_exp>   <end_of_turn> |  |
| <start_of_turn>user   48 / 2 -> 24.0   <end_of_turn> |  |
| <start_of_turn>model   <math_exp>48 + 24</math_exp>   <end_of_turn> |  |
| <start_of_turn>user   48 + 24 -> 72.0 <end_of_turn> |  |
| <start_of_turn>model   <answer>72</answer> <end_of_turn><eos> |  |

## 附录 G 示例 Id

为便于复现，我们提供评估所用示例的 id。
|  |
| --- |
| HotPotQA Example Ids |
| 5ab46a295542990594ba9c1c, 5a85ad925542997b5ce40023, 5a8353285542996488c2e40d, 5a79be835542994bb9457052, 5a82a0fc55429954d2e2eb87, 5adc2c9355429947ff173904, 5ab1e71b554299340b525421, 5a7790ac5542992a6e59def9, 5a83e4195542990548d0b243, 5ab3239b554299194fa93574, 5ae1a460554299234fd042a8, 5a81e075554299676cceb128, 5a7f714c5542992097ad2f6e, 5ab639c055429953192ad2aa, 5a7c1fe4554299683c1c62cf, 5ab7cff355429928e1fe391e, 5aba5b2455429939ce03dc9c, 5a7173b45542994082a3e83c, 5a90049d55429933b8a20468, 5a8e0d7e5542995085b373b4, 5adfbf3155429906c02daa29, 5abf1fed5542990832d3a127, 5addf6415542990dbb2f7f25, 5a8138c155429938b6142300, 5a7ae77b554299042af8f6b0, 5ae293fb5542996483e649fe, 5ae40a8b55429970de88d8a9, 5ab457445542991751b4d748, 5a77d6025542995d83181301, 5a89c2715542993b751ca990, 5a7a4d845542990783324f04, 5ae0ef5e5542990adbacf6df, 5a72321f55429971e9dc934a, 5ac440355542995c82c4ad0d, 5a7dd8625542990b8f503ae8, 5ab48dd55542991779162cd9, 5abc3948554299700f9d782b, 5a8a7cb255429930ff3c0df8, 5ae1178e5542997b2ef7d0d6, 5abd08ae554299700f9d7980, 5ab1e5975542997061209590, 5a74dca85542996c70cfae1f, 5ab8348d55429934fafe6d13, 5a78f1ef55429974737f7919, 5ac16eb355429964131be1f5, 5ae5e12d55429929b08079e4, 5ade6bbf5542997c77adee24, 5adf573c5542995534e8c798, 5a8901d9554299515336125b, 5a89fd9e55429970aeb701e8, 5a7917d955429974737f7982, 5adc1017554299438c868d20, 5a8da5c355429941ae14dffe, 5a8cad265542996e8ac88b19, 5add4ae25542992200553a88, 5ae026eb55429924de1b703a, 5a74fcbe5542996c70cfae67, 5adfa8ac55429942ec259add, 5adbf4555542994650320c18, 5ac31609554299741d48a1c0, 5a7b65bf55429931da12ca86, 5a73870455429905862fe051, 5a8b009755429950cd6afc40, 5ae62b2d5542992ae0d1625b, 5a7b5d795542992d025e6825, 5ab3185755429976abd1bc5f, 5ac046475542996f0d89cb70, 5a89138255429951533612af, 5a85d69f5542997175ce2062, 5a82dfa455429940e5e1a938, 5a8730355542991e7718170f, 5a85b3455542994c784ddb4d, 5a8658c4554299211dda2b02, 5abd9fa55542996e802b4809, 5ab268aa5542993be8fa9908, 5ae5dcc755429929b08079d8, 5a727ef15542992359bc30c5, 5a8e2ba85542995a26add474, 5a84f9465542991dd0999e36, 5a87099455429960ec39b704, 5a864d835542994775f6073c, 5ab9bf3b554299743d22ebe6, 5a864dfc5542994775f6073f, 5a871ce055429960ec39b749, 5a8bd3375542997f31a41dd3, 5ab277965542993be8fa9919, 5abcea83554299114383a194, 5a897561554299515336130b, 5adfdf4a55429906c02daa7c, 5ae265bb5542992decbdccea, 5a84b3035542992a431d1a91, 5a77280b5542994aec3b71ff, 5ae4d41355429908b6326488, 5a76de035542994aec3b718d, 5a7d2045554299452d57bb09, 5abc7af15542993a06baf8ed, 5abddeb55542991f66106083, 5a8218855542990a1d231f4e, 5a732fbb5542992359bc3271, 5a8024ad5542992097ad2fde, 5ae142a4554299422ee9964a, 5a72d5155542991f9a20c5b4, 5a722a4b55429971e9dc931f, 5a7a9ca455429941d65f26f3, 5adfa5405542992d7e9f93ca, 5a7b8e3d55429927d897bfec, 5a7c6ac25542996dd594b925, 5abae9cd5542996cc5e49f04, 5ae18e37554299234fd0428f, 5a84d29d5542994c784dda60, 5ae44eeb5542995dadf2430f, 5adbe7b455429944faac23b0, 5abedd105542993fe9a41d63, 5a80a7df554299485f59867f, 5ab2f6b1554299545a2cfaea, 5ac29ddc554299657fa28fdc, 5a7222ce55429971e9dc92c7, 5ae221f15542994d89d5b366, 5a7f9cc25542995d8a8ddec2, 5abe42aa55429976d4830ac2, 5ae329e45542991a06ce993e, 5a882caa5542997e5c09a596, 5ac1a94455429964131be262, 5a762e0f5542992d0ec06052, 5a7918ec554299148911f9ef, 5a7e0bd25542997cc2c4750b, 5ab8af3c55429916710eb0ac, 5aba94465542994dbf019953, 5a82ef725542995ce29dcd0a, 5ab2a5fb554299545a2cf9ef, 5ab3d4ae5542992ade7c6ec5, 5ac25882554299636651998c, 5ae535f55542993aec5ec17c, 5ac55c915542993e66e8234f, 5adfcf7655429906c02daa49, 5a8a12555542992e4fca84f1, 5a8af82c55429950cd6afc31, 5a8c564b554299240d9c2128, 5a89efb25542992e4fca8497, 5ab58009554299637185c5b2, 5ae69a455542996d980e7c48, 5a8f8dfb5542997ba9cb32bb, 5a811e1955429903bc27b931, 5a81f2955542990a1d231eee, 5abc428955429959677d6a67, 5ac263a25542992f1f2b38a3, 5ac5190d5542996feb3fe9f8, 5a82fbfc55429954d2e2ebe5, 5abce73b5542993a06baf9a2, 5adbf672554299438c868cf0, 5a75dd02554299109176e5aa, 5a8200d055429926c1cdade2, 5a8090105542996402f6a55c, 5adfda36554299025d62a35e, 5a7f9e0155429969796c1aee, 5a7b5f64554299042af8f757, 5a8a7bfb5542996c9b8d5eff, 5ae73fae5542991bbc9761c9, 5a77b0795542992a6e59df89, 5ac178655542994ab5c67d5a, 5ab5eab35542992aa134a3dd, 5ab667be55429954757d328a, 5a7a333f5542996a35c17130, 5ac262a055429951e9e6859a, 5a87ae9d5542994846c1cdc6, 5ac1985e55429964131be248, 5a848c215542992a431d1a4f, 5a89a79c5542993b751ca970, 5a8e16d355429917b4a5bd18, 5a7289755542992359bc30d9, 5a7d1dd055429909bec76960, 5ac152e755429964131be1bb, 5ae7d4f4554299540e5a5659, 5ae21559554299492dc91bc2, 5a8935e6554299669944a506, 5a831cb955429966c78a6b3f, 5a77aa565542992a6e59df6a, 5abff5e95542997d6429596a, 5ae07634554299603e418412, 5ab4eb2b55429942dd415fa2, 5abd512655429924427fcfb4, 5a7ad0195542992d025e66fd, 5a7cf9b455429907fabef07c, 5ae0fa52554299422ee99594, 5ae24d1a5542992decbdcca6, 5a7144df5542994082a3e72f, 5ac0279c5542996f0d89cb3f, 5a88a93c5542994846c1cead, 5adec5955542992fa25da83f, 5abbfd00554299114383a0d4, 5a7b9cac554299042af8f78f, 5ab9020d5542991b5579f0ca, 5a7c1c595542990527d55456, 5a7c583e5542996dd594b910, 5a8e72f05542990e94052b13, 5a85a1015542991dd0999e6f, 5adcb8205542994ed6169bd2, 5a8cef7a554299441c6b9f8a, 5a7fee435542994857a7685b, 5a7b4f2c55429931da12ca66, 5abeaf8a5542997ec76fd346, 5abbe67e5542993f40c73c05, 5a8f4e8955429918e830d1f1, 5ac1a0e15542994ab5c67dab, 5a7a9b4755429941d65f26ef, 5a87c1ac5542997e5c09a565, 5ab962ff554299131ca4231f, 5a7b79c95542997c3ec971b0, 5abe3ac35542993f32c2a0ac, 5a7639d55542992db9473748, 5a7a2ec05542990198eaf0bc, 5ac3d31a5542995ef918c249, 5abae3eb5542996cc5e49ee2, 5adff38b55429925eb1afb7d, 5ab7530b55429928e1fe3849, 5a88dcef55429938390d3fe3, 5ae0027b55429942ec259bda, 5a85ec815542994775f606af, 5ac172a15542994d76dcce2e, 5ac073eb5542996f0d89cbd8, 5ac5262755429924173fb60f, 5a8e72fe5542990e94052b14, 5a76133755429976ec32bcff, 5ae6b38c5542992ae0d16392, 5ab98fee554299131ca4237c, 5ac0e564554299294b219045, 5a72edeb5542992359bc31da, 5a7b663355429931da12ca87, 5a7cbe0f55429909bec767ee, 5a845bdd5542996488c2e524, 5a8a28b55542996c9b8d5e23, 5ae5fb975542996de7b71aa8, 5aba9cff5542994dbf01997e, 5ae11f0b5542997b2ef7d0e0, 5abe16c655429976d4830a71, 5abbdd355542992ccd8e7fc6, 5abedbfa5542993fe9a41d5f, 5a792421554299148911fa09, 5a80c5f6554299260e20a151, 5ab4136b5542996a3a969f18, 5adc375055429944faac246c, 5ac14d9d55429964131be1ab, 5abf23a65542997ec76fd3d7, 5a7e1d4255429965cec5ea79, 5ae63c8f5542992663a4f27c, 5ae71816554299572ea546d1, 5ae4bdeb55429913cc2044ee, 5ae4a09e5542996836b02ced, 5ac2312755429964131be2c3, 5ae36d325542992e3233c3f8, 5a7d68045542995f4f40226d, 5aba88d555429901930fa811, 5a8e1e4b554299068b959e63, 5a7e6d325542991319bc94a7, 5ab96d865542996be20204df, 5ae4d2c255429960a22e01f6, 5a8053cf5542992097ad2fe0, 5a8db1b75542994ba4e3dd01, 5a8d40c95542994ba4e3dc3b, 5ae5af10554299546bf82f23, 5a8d48ff5542994ba4e3dc5a, 5ab5f694554299488d4d9a66, 5a8f99bc55429918e830d28d, 5add0ed35542990d50227dac, 5a8c38235542995e66a4755f, 5ab6ccf155429954757d3372, 5ae44fe75542995dadf24314, 5adcb67e5542994ed6169bca, 5abe833d5542993f32c2a140, 5a8b002155429950cd6afc3e, 5a76f3c65542994aec3b719a, 5ab5207c5542996a3a96a02b, 5a8a73dd5542996c9b8d5eee, 5a9063c955429933b8a2050f, 5a7b45c855429931da12ca4a, 5a8e8b6c5542990e94052b43, 5a7a57935542990783324f1d, 5abe225c5542991f661060ec, 5a72a6b65542994cef4bc3b7, 5ab7f3625542995dae37ea06, 5a7cfdda55429907fabef095, 5a8994505542993b751ca950, 5ae308775542992decbdcdcd, 5ab72f32554299110f219ac3, 5a7b93e05542995eb53be961, 5a88710b554299206df2b26b, 5ab6259855429953192ad272, 5ac29ca6554299218029dac0, 5ac0ab335542992a796ded5d, 5ade469c5542992fa25da722, 5ab318a0554299233954ff07, 5ab1f75d554299340b525443, 5ade5664554299728e26c6d5, 5ae4a3b65542995ad6573dee, 5ae40e3955429970de88d8c5, 5ab9025855429934fafe6e47, 5a82100955429926c1cdae1e, 5ac5138c5542994611c8b36a, 5ab2eb7755429929539468b9, 5ab738945542993667793f97 |

|  |
| --- |
| CofCA Example Ids |
| 5a866fee5542991e77181657, 5a7db2f75542990b8f503a34, 5a8ee0a35542990e94052ba0, 5ae525835542990ba0bbb1cd, 5ac4bfd05542997ea680caab, 5ac4c61a5542996feb3fe93c, 5abbbd0f55429931dba144d5, 5a89372855429951533612e6, 5ab381b155429969a97a816b, 5ac2a912554299218029dae8, 5ae3345f55429928c4239682, 5a7bb3d9554299294a54aaa0, 5abaa25155429901930fa868, 5ac39a1c554299657fa290f9, 5a73332b5542992359bc3287, 5ae655c855429908198fa599, 5add82fc5542997545bbbd57, 5add117e5542990d50227db2, 5ab93287554299753720f78f, 5ab979da554299131ca4233a, 5a79c7f95542994bb9457099, 5ab58ae15542992aa134a357, 5ae3bdfa5542990afbd1e1c0, 5add7d055542990dbb2f7e61, 5ae136f655429920d5234325, 5a80b4635542992bc0c4a7bd, 5ab93287554299753720f78f, 5ae3b4d05542992f92d82349, 5ae77a31554299540e5a55c7, 5ae0d91e55429924de1b7198, 5ae64cab5542991bbc9760be, 5ab865be5542990e739ec8e5, 5a804fc45542992bc0c4a6f0, 5ac2ffa9554299218029dbb2, 5ae7b03e5542993210983ef6, 5a77153355429937353601c8, 5ae61be055429929b0807ace, 5a8ae6c055429950cd6afbce, 5ae64cab5542991bbc9760be, 5a72a00d5542991f9a20c53c, 5ae7b03e5542993210983ef6, 5a8eacc75542995085b37473, 5ab9253c554299131ca4227f, 5a8ee0a35542990e94052ba0, 5a866fee5542991e77181657, 5a888a8a5542997e5c09a603, 5abeed7e5542993fe9a41da0, 5ae4b3da55429913cc2044d6, 5add28c85542992ae4cec4be, 5abffc58554299012d1db552, 5a8bab4e554299240d9c207c, 5abae52a5542996cc5e49eea, 5abba27f5542996606241708, 5ab6ad2855429953192ad35e, 5aba6b2d55429901930fa7a9, 5abc145b554299658360041f, 5a7336d05542991f9a20c68d, 5ac3b0f15542995ef918c1fc, 5ac3ad225542995ef918c1da, 5a7a06935542990198eaf050, 5ae6038155429929b0807a55, 5ab3dde2554299753aec59d6, 5ab381b155429969a97a816b, 5a77bd595542995d83181291, 5a76cb6e5542994aec3b717a, 5a7524ca55429929fddd850a, 5ade025e5542997dc790711e, 5ac17f4f5542994ab5c67d70, 5ae0fa8b5542997b2ef7d0c6, 5a7336d05542991f9a20c68d, 5a8b560855429950cd6afcba, 5adce28f5542990d50227d52, 5ac491eb5542996feb3fe8d2, 5a7fe9975542994857a76847, 5a72b2695542991f9a20c56f, 5a89372855429951533612e6, 5ac219df5542992f1f2b37fc, 5a8a84775542996c9b8d5f19, 5abd7ca05542993062266cab, 5ac07a585542996f0d89cbf0, 5a8e171b554299068b959e5a, 5a79e0445542994f819ef0e7, 5ae0d26455429945ae959473, 5a8f0e065542997ba9cb319c, 5adce28f5542990d50227d52, 5a8f7de3554299458435d657, 5adc1309554299438c868d3b, 5ac219df5542992f1f2b37fc, 5a80043055429969796c1ba0, 5ac39f2a554299391541382d, 5a72b1c25542992359bc3172, 5abe3f9455429976d4830aaa, 5a8f7de3554299458435d657, 5ab74412554299110f219ae8, 5a904e725542995651fb5118, 5a7a02235542996c55b2dcd3, 5adc318c5542996e685252d5, 5a78cdf7554299029c4b5e9f, 5ade8f5e55429975fa854f11, 5ab865be5542990e739ec8e5, 5abaf9df5542996cc5e49f45, 5adcf28c5542994ed6169c30, 5a7e7bf455429949594199d6, 5adbe1e755429947ff173853, 5a83168855429966c78a6b2e, 5adc134b5542994650320c5c, 5a90c58255429916514e756c, 5a8efd3c55429918e830d179, 5abbdc135542993f40c73bf6, 5add7d055542990dbb2f7e61, 5ab344af554299753aec5969, 5a8a35625542992d82986efd, 5ab3dad4554299753aec59cb, 5a8dcd8e55429941ae14e060, 5ae377155542991a06ce99c7, 5a7cb48a5542996dd594b9a1, 5ac143535542991316484aac, 5ac31c9d554299741d48a203, 5ae5569255429908b63265e4, 5ab93287554299753720f78f, 5abd04f15542996e802b467e, 5a72b2695542991f9a20c56f, 5ab59b045542997d4ad1f190, 5a7f3d325542992e7d278cb5, 5ae061d5554299603e41840e, 5ae56d31554299546bf82ed7, 5ae255db5542992decbdccc1, 5ab6e856554299710c8d1fac, 5a7a358f5542990783324ec1, 5a7f38ae5542992e7d278c99, 5ab5c9c5554299494045f065, 5ac061ab554299294b218fac, 5a8ee0a35542990e94052ba0, 5ae3bdfa5542990afbd1e1c0, 5ab561d85542992aa134a2fc, 5ae3d8dc5542992f92d8239c, 5a7bb3d9554299294a54aaa0, 5abb1f745542996cc5e49fb5, 5adce28f5542990d50227d52, 5a904e725542995651fb5118, 5add992c5542997545bbbd83, 5adc1309554299438c868d3b, 5adfd35b55429906c02daa54, 5ab39701554299233954ff5e, 5a8b58b955429950cd6afcc2, 5ae22d035542996483e64925, 5a7fa53c5542995d8a8ddedc, 5a84322b5542996488c2e50d, 5a8d0006554299441c6b9fa8, 5add82fc5542997545bbbd57, 5a80d30655429938b61421fe, 5a72b2695542991f9a20c56f, 5a81ff1d554299676cceb1c3, 5ae755665542997b22f6a6e9, 5a79e0445542994f819ef0e7, 5ae4c2145542995dadf243e7, 5abbbd0f55429931dba144d5, 5a7ccec9554299452d57ba72, 5a7bb3d9554299294a54aaa0, 5a8355f9554299123d8c20f3, 5ab5141a5542991779162d70, 5ae4c2145542995dadf243e7, 5ae2e27155429928c423952a, 5abee5e25542994516f45473, 5ab698885542995eadef002a, 5a7f98e655429969796c1ad8, 5a77bd595542995d83181291, 5a78ed46554299148911f9a6, 5ae377155542991a06ce99c7, 5ae614055542996de7b71b2a, 5a823ae45542990a1d231f6d, 5ab520565542996a3a96a02a, 5ac168865542994ab5c67d14, 5ac1944c5542996f0d89cc90, 5a7cedca55429909bec7689c, 5ab707c05542991d32223760, 5ae27edc5542992decbdcd2d, 5ab979da554299131ca4233a, 5ab345db55429969a97a8122, 5a88fea05542997e5c09a6e9, 5ae3b4d05542992f92d82349, 5ab39701554299233954ff5e, 5add992c5542997545bbbd83, 5ab5e6d65542997d4ad1f232, 5a88b7735542993e715ac079, 5adfd35b55429906c02daa54, 5a8514545542992a431d1ad2, 5adfd35b55429906c02daa54, 5ac538ef5542994611c8b437, 5ab520565542996a3a96a02a, 5a74fbe55542996c70cfae63, 5ab55435554299488d4d9939, 5ae31a9c55429928c42395ef, 5ab67b8f55429954757d32f0, 5ae13f525542997b2ef7d169, 5a7d1f605542995ed0d165fb, 5ade52e85542997c77adedfa, 5a7607d7554299109176e61a, 5a85603a5542997b5ce3fff1, 5ac17f4f5542994ab5c67d70, 5a7fa53c5542995d8a8ddedc, 5abaef34554299660624169c, 5ae3d8dc5542992f92d8239c, 5ae0fa8b5542997b2ef7d0c6, 5ab55435554299488d4d9939, 5a904e725542995651fb5118, 5a879c8e5542994846c1cdb3, 5a870d0255429960ec39b710, 5ab3dde2554299753aec59d6, 5ac3ad225542995ef918c1da, 5ae11a6755429901ffe4ad8d, 5ab9116f5542991b5579f0db, 5ae755665542997b22f6a6e9, 5ae316f355429928c42395e3, 5abfbb455542997ec76fd440, 5a88377c5542997e5c09a5a7, 5a8099025542996402f6a588, 5a74248855429929fddd83e5, 5ac39a1c554299657fa290f9, 5abbc70d5542992ccd8e7f9b, 5ae13f525542997b2ef7d169, 5ac1f7f355429964131be2ae, 5a84322b5542996488c2e50d, 5a7738dc554299373536021f, 5a760f6855429976ec32bcf9, 5a7f38ae5542992e7d278c99, 5ae655c855429908198fa599, 5a821ffa5542990a1d231f5c, 5a90c2b35542995651fb51df, 5a78ed46554299148911f9a6, 5a8454e85542992ef85e23be, 5a8514545542992a431d1ad2, 5ac168865542994ab5c67d14, 5a88b7735542993e715ac079, 5a77aff55542992a6e59df86, 5ab39701554299233954ff5e, 5ac219df5542992f1f2b37fc, 5ab67b8f55429954757d32f0, 5a7a0d455542990783324e13, 5a8461d55542990548d0b29b, 5a879ab05542996e4f30887e, 5ae5365d5542992663a4f16d, 5a7a0d455542990783324e13, 5a7f9ee855429969796c1af3, 5ae5365d5542992663a4f16d, 5a736bfa5542991f29ee2e03, 5abfbb455542997ec76fd440, 5a8f8f345542997ba9cb32c2, 5ab9121555429919ba4e238a, 5a8dfbeb5542995085b3736e, 5a8a35625542992d82986efd, 5ac31c9d554299741d48a203, 5ae5365d5542992663a4f16d, 5add28065542990d50227e08, 5ae64cbf5542992ae0d162c1, 5adc134b5542994650320c5c, 5ac31c9d554299741d48a203, 5adf2b325542993a75d2640b, 5ae755665542997b22f6a6e9, 5a8454e85542992ef85e23be, 5a7cc5ae55429909bec767fc, 5a8a84775542996c9b8d5f19, 5ae377a35542994393b9e6db, 5ac4fa8c55429924173fb536, 5a77aff55542992a6e59df86, 5ae31a9c55429928c42395ef, 5adf5ebd5542995ec70e8fd8, 5a8a4bdc55429930ff3c0d8c, 5ae77a31554299540e5a55c7, 5ac2adf3554299657fa2900f, 5ab5a2f85542997d4ad1f197, 5abd7cb855429924427fd00a, 5ae136f655429920d5234325, 5ae525835542990ba0bbb1cd, 5a7738dc554299373536021f, 5a7a52745542996c55b2dd4f, 5ae1f61a5542994d89d5b2e1, 5add28c85542992ae4cec4be, 5a8bdef85542997f31a41dea, 5ae614055542996de7b71b2a, 5a7336d05542991f9a20c68d, 5a8eacc75542995085b37473, 5a8cdc5255429941ae14df21, 5ae664955542992ae0d1631b, 5ae2aba15542996483e64a32, 5abba27f5542996606241708, 5abd7ca05542993062266cab, 5ac1a5cd5542994d76dcce94, 5a736bfa5542991f29ee2e03, 5a8f0e065542997ba9cb319c, 5a8a2d805542996c9b8d5e2e, 5ae546e85542992663a4f1b5, 5ab6e856554299710c8d1fac, 5aba0e675542994dbf0198a0, 5ae3345f55429928c4239682, 5a7a02235542996c55b2dcd3, 5ac4fa8c55429924173fb536, 5a8beddd5542995d1e6f1468, 5abd90545542996e802b47d7, 5a7e39515542995ed0d166da |

|  |
| --- |
| MuSiQue Example Ids |
| 2hop__376129_44537, 2hop__764465_126539, 3hop1__434518_136629_55288, 2hop__353084_36340, 2hop__344450_160798, 2hop__637856_351187, 2hop__760990_44191, 3hop1__162325_11248_3752, 2hop__326799_278127, 2hop__239927_62031, 2hop__153813_69936, 3hop1__213491_782843_75255, 2hop__2846_2741, 2hop__3880_909, 2hop__347735_36735, 2hop__144393_87372, 4hop1__709382_146811_31223_45305, 2hop__143434_20122, 2hop__21457_74218, 3hop1__129597_517267_451901, 2hop__469317_776926, 2hop__27032_5400, 3hop2__83954_32417_24628, 3hop2__14790_57411_86234, 2hop__78490_49700, 3hop1__228008_354329_5303, 2hop__631861_160851, 3hop1__662283_507729_351187, 2hop__482727_20661, 3hop1__858308_102146_84004, 2hop__565717_77346, 3hop1__470555_668347_492654, 2hop__25478_65517, 2hop__129389_31248, 2hop__527889_5365, 2hop__20857_20779, 2hop__770_919, 2hop__375649_80178, 3hop1__332614_131794_17114, 2hop__144295_211364, 2hop__108160_159045, 2hop__46545_88521, 2hop__518906_44191, 2hop__733628_131886, 4hop1__28235_74795_84660_15312, 2hop__104341_92821, 2hop__445544_127008, 2hop__46766_79233, 2hop__342213_185893, 2hop__528837_126102, 2hop__497897_541630, 3hop1__48619_26424_581618, 2hop__87287_83906, 4hop1__411538_805015_475503_32631, 2hop__658198_72962, 2hop__42307_120207, 2hop__30878_555599, 3hop1__8373_87072_45358, 3hop2__337255_48727_83343, 2hop__251450_8796, 3hop1__161080_639509_644660, 2hop__558231_52667, 2hop__424189_49441, 3hop1__821692_74047_756423, 2hop__531731_79705, 3hop1__257981_259472_611044, 2hop__370765_14904, 2hop__446352_14183, 2hop__81087_13292, 2hop__684971_333904, 2hop__234176_69926, 2hop__858097_121880, 4hop2__724536_444580_75897_631997, 2hop__492509_70585, 4hop1__405751_4520_65397_49736, 2hop__128610_126060, 3hop1__325154_786384_42990, 2hop__34130_56335, 2hop__145997_63766, 2hop__146446_690423, 2hop__225632_11125, 2hop__856457_495, 2hop__129234_330515, 2hop__15674_42467, 3hop1__161946_84298_53741, 2hop__48959_83539, 2hop__64650_20556, 3hop1__316518_395352_131877, 2hop__136618_92216, 2hop__199336_185893, 2hop__930_57555, 3hop1__31942_48661_15069, 2hop__35105_160978, 2hop__128804_351187, 2hop__153004_86587, 2hop__715365_565667, 2hop__401484_135138, 2hop__52622_67783, 2hop__713501_58946, 2hop__300786_39199, 2hop__5430_5348, 3hop2__29467_132027_73594, 3hop1__225298_755188_480696, 2hop__367037_80178, 2hop__343473_53204, 2hop__848923_66214, 3hop1__369072_287321_161879, 2hop__250315_64214, 3hop1__104311_833580_61459, 2hop__1835_322987, 3hop1__836616_291186_4303, 2hop__531924_1094, 2hop__131831_84128, 2hop__328708_90697, 2hop__704691_82816, 2hop__80353_3001, 2hop__196785_61424, 2hop__130964_47336, 3hop1__761109_548045_159613, 3hop1__4525_52205_55099, 3hop1__58522_787757_69397, 2hop__58284_37793, 2hop__487591_7672, 2hop__250913_58115, 2hop__131095_85298, 2hop__144937_8600, 3hop2__625639_25582_21116, 3hop2__30023_63595_53125, 2hop__584872_88978, 2hop__116643_351162, 2hop__826203_62031, 2hop__85036_909, 2hop__62996_299942, 2hop__236731_229413, 2hop__15169_87091, 2hop__143791_75878, 2hop__658198_90536, 2hop__70321_15755, 2hop__131105_68117, 2hop__143162_438686, 2hop__20771_65517, 2hop__65149_46180, 2hop__251426_88653, 3hop1__238983_403313_61770, 2hop__28291_709757, 2hop__391909_3430, 3hop1__266733_291186_50964, 2hop__205685_160137, 2hop__343141_702969, 3hop1__383692_434040_59381, 2hop__240975_736878, 2hop__507864_368521, 3hop1__723003_593059_76293, 2hop__109234_62766, 4hop1__16401_4520_65397_52251, 2hop__140591_256194, 2hop__104757_74309, 2hop__194976_55566, 2hop__361127_140822, 3hop1__108774_104782_14771, 4hop3__393686_620110_61746_261712, 2hop__324178_83854, 3hop1__849536_301867_127418, 2hop__24408_541630, 2hop__54755_729624, 2hop__693650_61232, 3hop1__89787_49283_632017, 4hop1__104663_221169_833580_61459, 2hop__664573_36741, 3hop1__702271_823374_26254, 2hop__129892_62851, 3hop1__659125_39490_23352, 2hop__222162_386543, 2hop__446009_412262, 2hop__781841_77980, 3hop1__706183_20196_10585, 2hop__809948_162428, 3hop1__458602_681261_369731, 2hop__529082_114112, 3hop1__388966_508834_145463, 2hop__582169_370960, 2hop__225632_52135, 2hop__302491_81463, 2hop__136889_52356, 2hop__81363_42667, 3hop1__599980_544161_92922, 2hop__504710_513189, 2hop__145939_11443, 2hop__320353_4018, 2hop__27033_85063, 2hop__145110_861627, 2hop__149891_44359, 2hop__376266_37939, 3hop2__10879_37094_161133, 3hop2__159915_8509_19700, 4hop1__15118_31258_43153_32993, 3hop1__522518_132413_16066, 2hop__129782_517267, 3hop1__252998_715836_26008, 4hop1__205937_144938_83779_44678, 2hop__131318_47465, 2hop__338405_68172, 4hop3__3153_3356_11988_24628, 2hop__106465_54210, 2hop__397761_404718, 4hop1__632232_164954_6975_6891, 2hop__121872_708662, 2hop__73501_31113, 2hop__378511_191233, 3hop1__85045_96305_25007, 3hop1__755950_592709_78102, 2hop__811421_377891, 3hop2__63595_391767_53125, 2hop__131380_84859, 3hop1__158678_48408_37793, 3hop1__7312_830682_68600, 2hop__207212_21032, 3hop1__10725_695397_74345, 2hop__445228_774871, 4hop1__603090_818753_783943_26110, 2hop__177131_646483, 3hop1__801682_192919_16121, 2hop__243908_500443, 3hop2__89818_157704_4107, 2hop__160546_26427, 2hop__128772_745471, 2hop__62588_20779, 2hop__661636_82027, 2hop__105388_89066, 2hop__368185_131944, 3hop1__153577_411195_8682, 2hop__327451_90697, 2hop__647590_134798, 3hop2__30796_804098_24137, 2hop__146227_42328, 2hop__152881_620955, 2hop__11693_42892, 2hop__753498_7606, 2hop__2795_2741, 3hop1__373317_533132_1660, 2hop__229374_333904, 3hop1__370820_301867_127418, 3hop1__713250_4016_83854, 2hop__130414_68117, 4hop1__7312_84360_334118_41330, 2hop__65149_68376, 2hop__182310_565529, 3hop1__136299_84467_89676, 2hop__454055_86874, 2hop__604878_40786, 2hop__307569_51671, 2hop__854082_159115, 2hop__198557_55566, 3hop1__352446_506157_44678, 2hop__468848_44537, 2hop__207571_126101, 4hop2__53235_18485_57802_311656, 2hop__451164_140822, 3hop1__37692_84298_53741, 3hop1__672119_196807_760519, 3hop2__131210_661360_54023, 2hop__8531_24846, 3hop2__77886_64137_69951, 2hop__730762_8600, 2hop__350323_45731, 2hop__131117_53519, 3hop1__157534_275705_81669, 2hop__185628_677577, 2hop__77119_20732, 2hop__67755_82010, 3hop1__790278_593059_76293, 3hop2__162189_611045_73761, 2hop__568848_50788, 2hop__45625_61952, 2hop__146207_30651, 2hop__57439_78714, 2hop__3756_52135, 3hop1__501828_348668_856982, 3hop1__106423_35178_686699, 2hop__103203_23140, 3hop1__77985_66386_16350, 2hop__664921_579740, 2hop__106125_20644, 2hop__400998_61424, 3hop1__35884_161545_16532, 2hop__584521_755188, 2hop__80508_400874, 2hop__664137_58115, 2hop__453207_80674, 3hop1__29335_30907_24600, 2hop__144364_68900, 2hop__226817_482901, 4hop3__39198_75897_8509_19700, 2hop__713863_64008, 2hop__71269_36735, 2hop__504228_64689, 2hop__604878_18657, 2hop__81372_303417, 3hop1__674688_707133_72062, 2hop__157766_18657 |
