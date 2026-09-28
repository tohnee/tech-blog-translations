---
title: "ReAct：在语言模型中协同推理与行动"
title_en: "ReAct: Synergizing Reasoning and Acting in Language Models"
arxiv: 2210.03629
source: https://arxiv.org/abs/2210.03629
crawled: 2026-09-23
translated: 2026-09-23
---

# ReAct：在语言模型中协同推理与行动

> 原文：[ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) · Stanford CS329A 指定阅读

Shunyu Yao（普林斯顿大学计算机科学系，邮箱：{shunyuy,karthikn}@princeton.edu；注：本工作在 Google 实习期间完成，项目页面与代码：<https://react-lm.github.io/>）
Jeffrey Zhao、Dian Yu、Nan Du、Izhak Shafran、Yuan Cao（Google Research, Brain team，邮箱：{jeffreyzhao,dianyu,dunan,izhak,yuancao}@google.com）
Karthik Narasimhan（普林斯顿大学计算机科学系，邮箱：{shunyuy,karthikn}@princeton.edu）

###### 摘要

尽管大型语言模型（LLM）在语言理解与交互式决策任务上展现了令人瞩目的表现，但其推理能力（例如思维链提示）与行动能力（例如行动规划生成）此前主要被当作两个相互独立的课题来研究。本文探索用 LLM 以交错方式同时生成推理轨迹与任务特定行动，使二者之间产生更强的协同：推理轨迹帮助模型归纳、追踪并更新行动规划，以及处理异常情况；而行动则让模型能够与知识库或环境等外部信息源交互并获取额外信息。我们将这一名为 ReAct 的方法应用于一组多样的语言任务与决策任务，证明它优于最先进的基线方法，同时具有更好的人类可解释性与可信度。具体而言，在问答（HotpotQA）与事实验证（Fever）任务上，ReAct 通过与一个简单的 Wikipedia API 交互，克服了思维链推理中普遍存在的幻觉与错误传播问题，并生成类人的任务求解轨迹，比没有推理轨迹的基线更具可解释性。此外，在两个交互式决策基准（ALFWorld 与 WebShop）上，ReAct 仅凭一两个上下文示例提示，就以 34% 与 10% 的绝对成功率优势分别超越模仿学习与强化学习方法。

## 1 引言

人类智能的一个独特之处，是能够把面向任务的行动与言语推理（或内在言语，inner speech；Alderson-Day & Fernyhough, 2015）无缝结合；这种结合被认为在人类认知中扮演重要角色——支持自我调节或制定策略（Vygotsky, 1987；Luria, 1965；Fernyhough, 2010），并维持工作记忆（Baddeley, 1992）。以在厨房做一道菜为例：在任意两个具体动作之间，我们会用语言推理来追踪进度（「既然一切都切好了，我应该把那锅水烧开」）、处理异常或根据情况调整计划（「没有盐了，那就用酱油和胡椒代替吧」），以及意识到何时需要外部信息（「面团怎么和？让我上网搜一下」）。我们也会采取行动（翻开菜谱看书上的做法、打开冰箱、清点食材）来支持推理并回答问题（「我现在能做什么菜？」）。这种「行动」与「推理」之间的紧密协同，使人类能够快速学习新任务，即便在从未见过的情况下或面对不确定的信息时，也能进行稳健的决策或推理。

近期的结果暗示了在自主系统中把言语推理与交互式决策结合起来的可能性。一方面，经过恰当提示的大型语言模型（LLM）已展现出涌现能力：能在算术、常识与符号推理任务中执行多步推理轨迹，从问题推导出答案（Wei et al., 2022）。然而，这种「思维链」推理是一个静态的黑箱——模型使用自身内部表示来生成思考，并不与外部世界锚定，这限制了它进行反应式推理或更新知识的能力，并导致事实幻觉、以及错误在推理过程中传播等问题（图 1(1b)）。另一方面，近期工作探索了用预训练语言模型在交互式环境中进行规划与行动（Ahn et al., 2022；Nakano et al., 2021；Yao et al., 2020；Huang et al., 2022a），重点在于借助语言先验来预测行动。这类方法通常把多模态观察转换为文本，用语言模型生成领域特定的行动或规划，再由控制器选择或执行它们。但它们并没有让语言模型对高层目标进行抽象推理，也没有维护支持行动的工作记忆——唯一的例外是 Huang et al. (2022b)，他们执行了一种有限形式的言语推理来复述关于当前状态的空间事实。除了这类与几块积木互动的简单具身任务之外，尚无研究探讨推理与行动如何以协同的方式结合用于通用任务求解，也未探讨这种结合相较单独的推理或行动能否带来系统性收益。

在本工作中，我们提出 ReAct——一个用语言模型把推理与行动结合起来求解多样语言推理与决策任务的通用范式（图 1）。ReAct 提示 LLM 以交错方式生成与任务相关的言语推理轨迹和行动，使模型既能进行动态推理来创建、维护、调整高层的行动规划（以推理促行动），又能与外部环境（例如 Wikipedia）交互，把额外信息融入推理（以行动促推理）。

我们在四个多样的基准上对 ReAct 与最先进的基线进行实证评估：问答（HotPotQA，Yang et al., 2018）、事实验证（Fever，Thorne et al., 2018）、文字游戏（ALFWorld，Shridhar et al., 2020b）与网页导航（WebShop，Yao et al., 2022）。在 HotPotQA 与 Fever 上，借助一个模型可与之交互的 Wikipedia API，ReAct 优于朴素的行动生成模型，同时与思维链推理（CoT；Wei et al., 2022）表现相当。总体上最佳的方法是把 ReAct 与 CoT 结合，从而在推理时既可使用内部知识又可使用外部获取的信息。在 ALFWorld 与 WebShop 上，双样本甚至单样本的 ReAct 提示就能超越用 $10^3\sim 10^5$ 个任务实例训练的模仿学习或强化学习方法，成功率分别取得 34% 与 10% 的绝对提升。我们还通过对仅含行动的受控基线的一致优势，证明了稀疏而多用的推理在决策中的重要性。除通用性与性能提升之外，推理与行动的结合还在所有领域提升了模型的可解释性、可信度与可诊断性：人类可以清楚区分信息究竟来自模型内部知识还是外部环境，也可以检查推理轨迹来理解模型行动的决策依据。

总结而言，我们的主要贡献如下：（1）我们提出 ReAct，一个新颖的基于提示的范式，在语言模型中协同推理与行动以求解通用任务；（2）我们在多样基准上开展大量实验，展示 ReAct 在少样本学习设定下相较此前只做孤立推理或行动生成的方法的优势；（3）我们给出系统的消融与分析，理解行动在推理任务中的重要性以及推理在交互任务中的重要性；（4）我们分析 ReAct 在提示设定下的局限（即对推理与行动行为的支持有限），并开展初步微调实验，展示 ReAct 随训练数据增加而改进的潜力。将 ReAct 扩展到更多任务上训练与运行，并与强化学习等互补范式结合，有望进一步释放大型语言模型的潜力。

## 2 ReAct：协同推理 + 行动

考虑一个智能体与环境交互求解任务的一般设定。在时间步 $t$，智能体从环境接收观察 $o_t\in\mathcal{O}$，并依某种策略 $\pi(a_t|c_t)$ 采取行动 $a_t\in\mathcal{A}$，其中 $c_t=(o_1,a_1,\cdots,o_{t-1},a_{t-1},o_t)$ 是智能体的上下文。当映射 $c_t\mapsto a_t$ 高度隐含且需要大量计算时，学习这样的策略颇具挑战。例如，图 1(1c) 中的智能体无法生成完成问答任务所需的正确最终行动（Act 4），因为这需要对轨迹上下文（Question、Act 1-3、Obs 1-3）进行复杂推理。类似地，图 1(2a) 中的智能体无法从上下文中领会 sinkbasin 1 里并没有 peppershaker 1，于是不断产生幻觉行动。

ReAct 的想法很简单：把智能体的行动空间扩充为 $\hat{\mathcal{A}}=\mathcal{A}\cup\mathcal{L}$，其中 $\mathcal{L}$ 是语言空间。语言空间中的行动 $\hat{a}_t\in\mathcal{L}$——我们称之为思考（thought）或推理轨迹——不影响外部环境，因此不会带来观察反馈。相反，思考 $\hat{a}_t$ 旨在通过对当前上下文 $c_t$ 的推理来组织有用信息，并更新上下文 $c_{t+1}=(c_t,\hat{a}_t)$ 以支持后续的推理或行动。如图 1 所示，有用的思考可以有多种类型，例如：分解任务目标并创建行动规划（2b, Act 1；1d, Thought 1）、注入与任务求解相关的常识知识（2b, Act 1）、从观察中提取重要部分（1d, Thought 2、4）、追踪进度并切换行动规划（2b, Act 8）、处理异常并调整行动规划（1d, Thought 3），等等。

然而，由于语言空间 $\mathcal{L}$ 无限，在这个扩充后的行动空间中学习很困难，需要强大的语言先验。本文主要关注如下设定：用一个冻结的大型语言模型 PaLM-540B（Chowdhery et al., 2022）¹，以少样本上下文示例提示，使其同时生成领域特定的行动与自由形式的语言思考来求解任务（图 1(1d)、(2b)）。每个上下文示例都是一条人类编写的、由行动、思考与环境观察组成的任务求解轨迹（见附录 C）。对于推理居于首要地位的任务（图 1(1)），我们交替生成思考与行动，使任务求解轨迹由多个「思考-行动-观察」步骤组成。相反，对可能涉及大量行动的决策任务（图 1(2)），思考只需稀疏地出现在轨迹最相关的位置，因此我们让语言模型自行决定思考与行动的异步出现。

注 1：我们在附录 A.1 中给出部分 GPT-3（Brown et al., 2020）结果，其表现优于 PaLM-540B。

由于决策与推理能力被集成进同一个大型语言模型，ReAct 具备若干独特优点：

A) 直观且易于设计：设计 ReAct 提示非常直接——人类标注者只需在所采取的行动之上用语言写下自己的思考。本文没有使用任何专门的格式选择、思考设计或示例挑选。我们在第 3 节与第 4 节中详述各任务的提示设计。

B) 通用且灵活：得益于灵活的思考空间与思考-行动出现格式，ReAct 适用于行动空间与推理需求各异的多样任务，包括但不限于问答、事实验证、文字游戏与网页导航。

C) 高性能且稳健：ReAct 仅从一到六个上下文示例学习，就对新的任务实例表现出强大的泛化，在不同领域一致地超越只有推理或只有行动的基线。我们还在第 3 节展示启用微调后的额外收益，并在第 4 节展示 ReAct 的表现对提示选择具有稳健性。

D) 与人类对齐且可控：ReAct 提供可解释的序列决策与推理过程，人类可以轻松检查其推理与事实正确性。此外，如图 5（见第 4 节）所示，人类还可以通过编辑思考来即时控制或纠正智能体行为。

## 3 知识密集型推理任务

我们先从知识密集型推理任务入手，例如多跳问答与事实验证。如图 1(1d) 所示，通过与一个 Wikipedia API 交互，ReAct 能够检索信息来支撑推理，同时也用推理来确定下一步检索什么，展现了推理与行动的协同。

### 3.1 设定

##### 领域

我们考虑两个具有挑战性的知识检索与推理数据集：（1）HotPotQA（Yang et al., 2018），一个多跳问答基准，需要基于两篇或更多 Wikipedia 段落进行推理；（2）FEVER（Thorne et al., 2018），一个事实验证基准，每条断言依据是否存在可验证它的 Wikipedia 段落，被标注为 SUPPORTS、REFUTES 或 NOT ENOUGH INFO。本工作中，两个任务都采用仅有问题的设定：模型只接收问题/断言作为输入，无法访问支撑段落，必须依靠内部知识或通过与外部环境交互来检索知识以支撑推理。

##### 行动空间

我们设计了一个带三类行动的简单 Wikipedia web API 来支持交互式信息检索：（1）search[entity]，若对应实体 wiki 页面存在则返回该页面的前 5 个句子，否则从 Wikipedia 搜索引擎返回最相似的前 5 个实体；（2）lookup[string]，返回页面中包含 string 的下一个句子，模拟浏览器上的 Ctrl+F 功能；（3）finish[answer]，以 answer 结束当前任务。我们注意到，这一行动空间大多只能基于精确的页面名检索到段落的一小部分，明显弱于最先进的词法或神经检索器。其目的在于模拟人类使用 Wikipedia 的方式，并迫使模型通过显式的语言推理来进行检索。

### 3.2 方法

##### ReAct 提示

对 HotpotQA 与 Fever，我们分别从训练集随机选择 6 个与 3 个案例²，人工编写 ReAct 格式的轨迹，作为提示中的少样本示例。与图 1(d) 类似，每条轨迹由多个「思考-行动-观察」步骤组成（即密集思考），其中自由形式的思考服务于多种目的。具体而言，我们组合使用以下思考：分解问题（「I need to search x, find y, then find z」）、从 Wikipedia 观察中提取信息（「x was started in 1844」「The paragraph does not tell x」）、进行常识（「x is not y, so z must instead be…」）或算术推理（「1844 < 1989」）、引导搜索改写（「maybe I can search/look up x instead」），以及综合出最终答案（「…so the answer is x」）。详见附录 C。

注 2：我们发现更多示例并不能提升性能。

##### 基线

我们系统性地消融 ReAct 轨迹来构建多个基线的提示（格式见图 1(1a-1c)）：(a) 标准提示（Standard），移除 ReAct 轨迹中的全部思考、行动与观察；(b) 思维链提示（CoT；Wei et al., 2022），移除行动与观察，作为纯推理基线；我们还构建了自洽性基线（CoT-SC）（Wang et al., 2022a；Wang et al., 2022b）：推理时以解码温度 0.7 采样 21 条 CoT 轨迹并采纳多数答案，该方法被发现能稳定提升 CoT 的表现；(c) 仅行动提示（Act），移除 ReAct 轨迹中的思考，大体上近似 WebGPT（Nakano et al., 2021）与互联网交互回答问题的方式，不过它运行在不同的任务与行动空间上，且使用模仿与强化学习而非提示。

##### 结合内部知识与外部知识

正如第 3.3 节将详述的，我们观察到 ReAct 展示的问题求解过程更基于事实、更有依据，而 CoT 在组织推理结构上更准确，却容易受虚假事实或思考的影响。因此我们提出把 ReAct 与 CoT-SC 结合，让模型按以下启发式规则决定何时切换到另一种方法：

A) ReAct $\to$ CoT-SC：当 ReAct 在给定步数内未能返回答案时，回退到 CoT-SC。对 HotpotQA 与 FEVER 我们分别设 7 步与 5 步，因为更多步数不会提升 ReAct 的表现³。

B) CoT-SC $\to$ ReAct：当 $n$ 个 CoT-SC 样本中的多数答案出现次数少于 $n/2$（即内部知识可能不足以自信地支持该任务）时，回退到 ReAct。

注 3：在最终答案正确的所有轨迹中，HotpotQA 上 7 步与 FEVER 上 5 步的轨迹分别只占 0.84% 与 1.33%。

##### 微调

由于大规模人工标注推理轨迹与行动的困难，我们考虑一种与 Zelikman et al. (2022) 类似的自举（bootstrapping）方法：用 ReAct（以及其他基线）生成的 3,000 条答案正确的轨迹，微调较小的语言模型（PaLM-8/62B），使其在输入问题/断言条件下解码出完整轨迹（全部思考、行动、观察）。更多细节见附录 B.1。

### 3.3 结果与观察

##### ReAct 一致地优于 Act

表 1 给出以 PaLM-540B 为基础模型、不同提示方法在 HotpotQA 与 Fever 上的结果。我们注意到 ReAct 在两个任务上都优于 Act，证明了推理对引导行动的价值，尤其是在综合最终答案时，如图 1(1c-d) 所示。图 3 的微调结果也证实了推理轨迹有助于更有依据的行动。

| 提示方法 | HotpotQA | Fever |
| --- | --- | --- |
|  | (EM) | (Acc) |
| Standard | 28.7 | 57.1 |
| CoT（Wei et al., 2022） | 29.4 | 56.3 |
| CoT-SC（Wang et al., 2022a） | 33.4 | 60.4 |
| Act | 25.7 | 58.9 |
| ReAct | 27.4 | 60.9 |
| CoT-SC $\to$ ReAct | 34.2 | 64.6 |
| ReAct $\to$ CoT-SC | 35.1 | 62.0 |
| 有监督 SoTA（Zhu et al., 2021；Lewis et al., 2020） | 67.5 | 89.5 |

注 4：Wang et al. (2022b) 中 Standard、CoT、CoT-SC 的 HotpotQA EM 分别为 27.1、28.9、33.8。

表 1：PaLM-540B 在 HotpotQA 与 Fever 上的提示结果。

图 2：PaLM-540B 提示结果随所用 CoT-SC 样本数的变化。

|  | 类型 | 定义 | ReAct | CoT |
| --- | --- | --- | --- | --- |
| 成功 | 真阳性 | 推理轨迹与事实均正确 | 94% | 86% |
|  | 假阳性 | 推理轨迹或事实存在幻觉 | 6% | 14% |
| 失败 | 推理错误 | 推理轨迹错误（包括无法从重复步骤中恢复） | 47% | 16% |
|  | 检索结果错误 | 搜索返回为空或不包含有用信息 | 23% | - |
|  | 幻觉 | 推理轨迹或事实存在幻觉 | 0% | 56% |
|  | 标签歧义 | 预测正确但与标签不完全一致 | 29% | 28% |

表 2：ReAct 与 CoT 在 HotpotQA 上的成功与失败模式类型，以及人类研究的随机抽样示例中各类别的占比。

##### ReAct 对比 CoT

另一方面，ReAct 在 Fever 上优于 CoT（60.9 对 56.3），在 HotpotQA 上略逊于 CoT（27.4 对 29.4）。Fever 中 SUPPORTS/REFUTES 的断言可能只有细微差别（见附录 D.1），因此以行动检索准确且最新的知识至关重要。为更好理解 ReAct 与 CoT 在 HotpotQA 上的行为差异，我们从 ReAct 与 CoT 中各随机抽取 50 条答案正确与 50 条答案错误（以 EM 判断）的轨迹（共 200 个示例），人工标注其成功与失败模式（表 2）。若干关键观察如下：

A) 幻觉是 CoT 的严重问题：在成功模式中造成比 ReAct 高得多的假阳性率（14% 对 6%），并构成其主要失败模式（56%）。相比之下，得益于对外部知识库的访问，ReAct 的问题求解轨迹更基于事实、更可信。

B) 交错推理、行动与观察步骤提升了 ReAct 的事实性与可信度，但这种结构性约束也降低了其组织推理步骤的灵活性，导致比 CoT 更高的推理错误率。我们注意到 ReAct 存在一种特有的高频错误模式：模型反复生成先前的思考与行动；我们把它归入「推理错误」，因为模型未能推理出恰当的下一步行动、无法跳出循环⁶。

C) 对 ReAct 而言，通过搜索成功检索到有信息量的知识至关重要。无信息量的搜索占错误情形的 23%，会使模型推理脱轨，令其难以恢复并重新组织思考。这或许可以视为事实性与灵活性之间预期中的权衡，也促使我们提出结合两种方法的策略。

注 6：我们怀疑这可能源于次优的贪心解码过程，未来使用更好解码（例如束搜索）的工作或有助解决该问题。

我们在附录 E.1 中给出每种成功与失败模式的示例。我们还发现部分 HotpotQA 问题的答案标签可能已过时，示例见图 4。

##### ReAct + CoT-SC 是提示 LLM 的最佳组合

表 1 同样显示，HotpotQA 与 Fever 上最佳的提示方法分别是 ReAct → CoT-SC 与 CoT-SC → ReAct。此外，图 2 展示了不同方法的表现随 CoT-SC 样本数的变化。两种 ReAct + CoT-SC 方法虽然在各自任务上各占优势，但都在不同样本数下显著且一致地超越 CoT-SC，仅用 3-5 个样本就达到 CoT-SC 用 21 个样本的性能。这些结果说明，在推理任务中恰当结合模型内部知识与外部知识的价值。

图 3：ReAct（本文方法）与基线在 HotPotQA 上提示与微调的扩展结果。

##### ReAct 在微调设定下表现最佳

图 3 展示四种方法（Standard、CoT、Act、ReAct）在 HotpotQA 上提示/微调的扩展效应。对 PaLM-8/62B 而言，ReAct 提示在四种方法中表现最差，因为从上下文示例中同时学会推理与行动颇具难度。然而，仅用 3,000 个示例微调后，ReAct 就成为四者中的最佳方法：微调后的 PaLM-8B ReAct 超越所有 PaLM-62B 提示方法，微调后的 PaLM-62B ReAct 超越所有 540B 提示方法。相比之下，对 PaLM-8/62B 而言，微调 Standard 或 CoT 都显著差于微调 ReAct 或 Act，因为前者实质上是教模型记忆（可能虚构的）知识事实，而后者教模型如何（推理并）行动以从 Wikipedia 获取信息——这对知识推理是一项更可泛化的技能。由于所有提示方法仍与领域专用的最先进方法相去甚远（表 1），我们相信用更多人工编写数据做微调或许是释放 ReAct 潜力的更佳途径。

## 4 决策任务

我们还在两个基于语言的交互式决策任务 ALFWorld 与 WebShop 上测试 ReAct。两者都具有复杂的环境，要求智能体在稀疏奖励下长时程地行动，这正需要推理来有效地行动与探索。

##### ALFWorld

ALFWorld（Shridhar et al., 2020b）（图 1(2)）是一个合成的文字游戏，与具身基准 ALFRED（Shridhar et al., 2020a）对齐。它包含 6 类任务，智能体需要通过文本行动（例如 go to coffeetable 1、take paper 2、use desklamp 1）在模拟家庭中导航与交互，以达成高层目标（例如在台灯下查看纸张）。一个任务实例可包含 50 多个地点，专家策略求解需要 50 多步，因此考验智能体规划与追踪子目标以及系统性探索（例如逐一检查所有桌子寻找台灯）的能力。特别地，ALFWorld 内建的一个挑战是需要判断常见家居物品的可能位置（例如台灯 likely 出现在桌子、架子或衣柜上），这使该环境很适合 LLM 发挥其预训练常识知识。为提示 ReAct，我们从训练集为每类任务随机标注 3 条轨迹，每条轨迹包含稀疏的思考，用于：（1）分解目标，（2）追踪子目标完成情况，（3）确定下一个子目标，（4）借助常识推理某物体可能在哪里、对该物体做什么。ALFWorld 所用提示见附录 C.4。遵循 Shridhar et al. (2020b)，我们在 134 个未见过的评估游戏上按任务专用设定评测。为稳健起见，我们从标注的 3 条轨迹中取 2 条的每种排列，为每类任务构造 6 个提示。Act 提示用相同轨迹构造，但不含思考——由于任务实例从训练集随机选取，这对 ReAct 与 Act 都无偏向，从而为检验稀疏思考的重要性提供公平且受控的比较。基线方面，我们使用 BUTLER（Shridhar et al., 2020b）——一个在每类任务 $10^5$ 条专家轨迹上训练的模仿学习智能体⁷。

注 7：Micheli & Fleuret (2021) 在 3553 个任务实例上微调 GPT-2，取得了远优于 BUTLER 的表现，但它是在全部任务类型上训练的，因此未作为基线纳入。

##### WebShop

ReAct 能否与嘈杂的真实语言环境交互以支撑实际应用？我们研究 WebShop（Yao et al., 2022）——一个新近提出的在线购物网站环境，包含 118 万件真实商品与 1.2 万条人类指令。与 ALFWorld 不同，Webshop 含有大量结构化与非结构化文本（例如从 Amazon 抓取的商品标题、描述与选项），要求智能体根据用户指令（例如「I am looking for a nightstand with drawers. It should have a nickel finish, and priced lower than $140」）通过网页交互（例如搜索「nightstand drawers」、点击「color: modern-nickel-white」或「back to search」等按钮）购买一件商品。该任务在 500 条测试指令上以平均得分（所选商品覆盖期望属性的平均比例，按所有回合平均）与成功率（所选商品满足全部要求的回合比例）评估。我们构造 Act 提示，包含搜索、选择商品、选择选项与购买等行动；ReAct 提示额外加入推理，以确定探索什么、何时购买以及哪些商品选项与指令相关。示例提示见表 6，模型预测见附录中的表 10。我们对比的方法包括：用 1,012 条人类标注轨迹训练的模仿学习（IL）方法，以及额外用 10,587 条训练指令训练的模仿 + 强化学习（IL + RL）方法。

##### 结果

| 方法 | Pick | Clean | Heat | Cool | Look | Pick 2 | All |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Act（6 选最佳） | 88 | 42 | 74 | 67 | 72 | 41 | 45 |
| ReAct（平均） | 65 | 39 | 83 | 76 | 55 | 24 | 57 |
| ReAct（6 选最佳） | 92 | 58 | 96 | 86 | 78 | 41 | 71 |
| ReAct-IM（平均） | 55 | 59 | 60 | 55 | 23 | 24 | 48 |
| ReAct-IM（6 选最佳） | 62 | 68 | 87 | 57 | 39 | 33 | 53 |
| BUTLERg（8 选最佳） | 33 | 26 | 70 | 76 | 17 | 12 | 22 |
| BUTLER（8 选最佳） | 46 | 39 | 74 | 100 | 22 | 24 | 37 |

表 3：AlfWorld 任务专用成功率（%）。BUTLER 与 BUTLERg 结果取自 Shridhar et al. (2020b) 的表 4。除 BUTLER 使用束搜索外，所有方法均用贪心解码。

| 方法 | Score | SR |
| --- | --- | --- |
| Act | 62.3 | 30.1 |
| ReAct | 66.6 | 40.0 |
| IL | 59.9 | 29.1 |
| IL+RL | 62.4 | 28.7 |
| Human | 82.1 | 59.6 |
| Expert |  |  |

表 4：Webshop 上的得分与成功率（SR）。IL/IL+RL 取自 Yao et al. (2022)。

ReAct 在 ALFWorld（表 3）与 Webshop（表 4）上都优于 Act。在 ALFWorld 上，最佳的 ReAct 试验取得 71% 的平均成功率，显著超越最佳的 Act（45%）与 BUTLER（37%）试验。事实上，即便最差的 ReAct 试验（48%）也胜过这两种方法的最佳试验。此外，ReAct 相对 Act 的优势在六次受控试验中保持一致，相对性能增益从 33% 到 90% 不等，平均 62%。定性来看，我们观察到：完全没有思考时，Act 无法把目标正确分解为更小的子目标，或丢失对环境当前状态的追踪。比较 ReAct 与 Act 的示例轨迹见附录 D.2.1 与附录 D.2.2。

在 Webshop 上，单样本 Act 提示的表现已与 IL 及 IL+RL 方法相当。加入额外的稀疏推理后，ReAct 取得了显著更好的表现，相较此前最佳成功率有 10% 的绝对提升。通过检查示例，我们发现 ReAct 更容易通过推理来弥合嘈杂观察与行动之间的差距（例如「For ‘space-saving ottoman bench for living room’, the item has options ‘39x18x18inch’ and ‘blue’ and seems good to buy.」），从而识别与指令相关的商品和选项。然而，现有方法仍远逊于专家人类的表现（表 4）——人类会进行多得多的商品探索与查询改写，这对基于提示的方法仍具挑战性。

##### 论内部推理与外部反馈的价值

据我们所知，ReAct 是首个在闭环系统中把 LLM 的推理与行动结合起来应用于交互环境的演示。最接近的先前工作或许是 Inner Monologue（IM；Huang et al., 2022b），其中具身智能体的行动由同名的「内心独白」驱动。然而，IM 的「内心独白」仅限于对环境状态以及为满足目标智能体尚需完成之事的观察。相比之下，ReAct 中用于决策的推理轨迹灵活而稀疏，允许针对不同任务引入多样的推理类型（见第 2 节）。

为展示 ReAct 与 IM 的差异，并凸显内部推理相对简单响应外部反馈的重要性，我们用一个由 IM 式密集外部反馈组成的思考模式做了消融实验。如表 3 所示，ReAct 大幅超越 IM 式提示（ReAct-IM）（总体成功率 71 对 53），在六类任务中的五类上保持优势。定性来看，我们观察到 ReAct-IM 常因缺乏高层目标分解而在判断子目标何时完成或下一子目标是什么时出错。此外，许多 ReAct-IM 轨迹由于缺乏常识推理，难以判断物品在 ALFWorld 环境中可能位于何处。这两个不足都能在 ReAct 范式中得到解决。关于 ReAct-IM 的更多细节见附录 B.2。ReAct-IM 的示例提示见附录 C.4，示例轨迹见附录 D.2.3。

## 5 相关工作

##### 用于推理的语言模型

用 LLM 做推理的最著名工作或许当属思维链（CoT；Wei et al., 2022），它揭示了 LLM 为问题求解构建自身「思考过程」的能力。此后涌现了若干后续工作，包括求解复杂任务的最少到最多提示（least-to-most prompting；Zhou et al., 2022）、zero-shot-CoT（Kojima et al., 2022），以及基于自洽性的推理（Wang et al., 2022a）。近期，Madaan & Yazdanbakhsh (2022) 系统研究了 CoT 的表述与结构，观察到符号、模式与文本的存在对 CoT 的有效性至关重要。另一些工作则扩展到简单提示之外更复杂的推理架构。例如 Selection-Inference（Creswell et al., 2022）把推理过程分为「选择」与「推断」两步；STaR（Zelikman et al., 2022）通过在模型自身生成的正确理由上微调模型来自举推理过程；忠实推理（faithful reasoning；Creswell & Shanahan, 2022）把多步推理分解为三步，各由一个专用 LM 执行。类似的方法如 Scratchpad（Nye et al., 2021）——在中间计算步骤上微调 LM——同样在多步计算问题上展现出改进。与这些方法不同，ReAct 执行的并非孤立、固定的推理，而是把模型行动及其相应观察整合成连贯的输入流，使模型推理更准确，并能处理推理之外的任务（例如交互式决策）。

##### 用于决策的语言模型

LLM 的强大能力使其能够执行语言生成之外的任务，把 LLM 用作决策的策略模型（尤其是在交互环境中）正变得流行。WebGPT（Nakano et al., 2021）用 LM 与网页浏览器交互、浏览网页，并从 ELI5（Fan et al., 2019）的复杂问题中推导答案。与 ReAct 相比，WebGPT 并未显式建模思考与推理过程，而是依赖昂贵的人类反馈做强化学习。在对话建模中，BlenderBot（Shuster et al., 2022b）与 Sparrow（Glaese et al., 2022）等聊天机器人，以及 SimpleTOD（Hosseini-Asl et al., 2020）等面向任务的对话系统，同样训练 LM 做 API 调用决策。与 ReAct 不同，它们同样未显式考虑推理过程，且策略学习也依赖昂贵的数据集与人类反馈收集。相比之下，ReAct 以低廉得多的方式学习策略，因为其决策过程只需推理过程的语言描述⁸。

注 8：人类反馈也可以以互补方式引入，我们将其留作未来工作。

LLM 也越来越多地被用于交互与具身环境中的规划与决策。在这方面与 ReAct 最相关的或许是 SayCan（Ahn et al., 2022）与 Inner Monologue（Huang et al., 2022b），二者都用 LLM 做机器人行动规划与决策。在 SayCan 中，LLM 被提示直接预测机器人可采取的可能行动，再由一个锚定于视觉环境的可供性（affordance）模型重排序以作最终预测。Inner Monologue 通过加入同名的「内心独白」进一步改进，其实现方式为来自环境的注入反馈。据我们所知，Inner Monologue 是首个展示此类闭环系统的工作，ReAct 正是在此基础上构建。但我们认为 Inner Monologue 并不真正包含内在思考——第 4 节对此有详细阐述。我们还注意到，在交互式决策过程中利用语义丰富的语言输入已在其他设定下被证明成功（Abramson et al., 2020；Karamcheti et al., 2021；Huang et al., 2022a；Li et al., 2022）。越来越明显的是，在 LLM 的帮助下，语言作为一种基本认知机制将在交互与决策中扮演关键角色。此外，LLM 的进展也催生了 Reed et al. (2022) 等多功能、通用型智能体的发展。

## 6 结论

我们提出了 ReAct——一个在大型语言模型中协同推理与行动的简单而有效的方法。通过在多跳问答、事实核查与交互式决策任务上的大量实验，我们表明 ReAct 带来了更优的性能与可解释的决策轨迹。尽管方法简单，但具有庞大行动空间的复杂任务需要更多示范才能学好，遗憾的是这很容易超出上下文学习的输入长度限制。我们在 HotpotQA 上探索了微调方法并取得初步可喜的结果，但从更高质量的人工标注中学习将是进一步提升性能的期望路径。以多任务训练扩展 ReAct，并与强化学习等互补范式结合，有望造就更强的智能体，进一步释放 LLM 在更多应用中的潜力。

#### 致谢

我们感谢 Google Brain 团队与 Princeton NLP 组许多人的支持与反馈。本工作部分受美国国家科学基金会 Grant No. 2107048 资助。本材料中表达的观点、发现、结论或建议均属作者本人，不一定反映美国国家科学基金会的观点。

#### 可复现性声明

我们的主实验在 PaLM（Chowdhery et al., 2022）上完成，该模型目前尚未开放访问。为提高可复现性，我们在附录 C 中给出全部所用提示，在附录 A.1 中给出使用 GPT-3（Brown et al., 2020）的额外实验，并在 <https://anonymous.4open.science/r/ReAct-2268/> 提供相关 GPT-3 ReAct 提示代码。

#### 伦理声明

ReAct 提示大型语言模型生成比以往方法更具人类可解释性、可诊断性与可控性的任务求解轨迹。然而，把大型语言模型接入可与外部环境（例如网络、物理环境）交互的行动空间存在潜在风险，例如查询不当或私密信息，或在环境中采取有害行动。我们的实验通过把交互限制在不包含私密信息的特定网站（Wikipedia 或 WebShop）上来最小化此类风险，行动空间设计中也不含任何危险行动（即模型不能真的在研究基准 WebShop 上购买商品，也不能编辑 Wikipedia）。我们认为研究者在未来设计更大规模的实验之前应意识到这些风险。

## 参考文献
- Abramson et al. (2020)

  Josh Abramson, Arun Ahuja, Iain Barr, Arthur Brussee, Federico Carnevale, Mary
  Cassin, Rachita Chhaparia, Stephen Clark, Bogdan Damoc, Andrew Dudzik, Petko
  Georgiev, Aurelia Guy, Tim Harley, Felix Hill, Alden Hung, Zachary Kenton,
  Jessica Landon, Timothy Lillicrap, Kory Mathewson, Soňa Mokrá, Alistair
  Muldal, Adam Santoro, Nikolay Savinov, Vikrant Varma, Greg Wayne, Duncan
  Williams, Nathaniel Wong, Chen Yan, and Rui Zhu.
  Imitating interactive intelligence, 2020.
  URL <https://arxiv.org/abs/2012.05672>.
- Ahn et al. (2022)

  Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron
  David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman,
  Alex Herzog, Daniel Ho, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan,
  Eric Jang, Rosario Jauregui Ruano, Kyle Jeffrey, Sally Jesmonth, Nikhil J
  Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Kuang-Huei Lee, Sergey
  Levine, Yao Lu, Linda Luu, Carolina Parada, Peter Pastor, Jornell Quiambao,
  Kanishka Rao, Jarek Rettinghouse, Diego Reyes, Pierre Sermanet, Nicolas
  Sievers, Clayton Tan, Alexander Toshev, Vincent Vanhoucke, Fei Xia, Ted Xiao,
  Peng Xu, Sichun Xu, Mengyuan Yan, and Andy Zeng.
  Do as i can, not as i say: Grounding language in robotic affordances,
  2022.
  URL <https://arxiv.org/abs/2204.01691>.
- Alderson-Day & Fernyhough (2015)

  Ben Alderson-Day and Charles Fernyhough.
  Inner speech: development, cognitive functions, phenomenology, and
  neurobiology.
  *Psychological bulletin*, 141(5):931, 2015.
- Baddeley (1992)

  Alan Baddeley.
  Working memory.
  *Science*, 255(5044):556–559, 1992.
- Brown et al. (2020)

  Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla
  Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell,
  et al.
  Language models are few-shot learners.
  *Advances in neural information processing systems*,
  33:1877–1901, 2020.
- Chowdhery et al. (2022)

  Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra,
  Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian
  Gehrmann, et al.
  Palm: Scaling language modeling with pathways.
  *arXiv preprint arXiv:2204.02311*, 2022.
- Creswell & Shanahan (2022)

  Antonia Creswell and Murray Shanahan.
  Faithful reasoning using large language models, 2022.
  URL <https://arxiv.org/abs/2208.14271>.
- Creswell et al. (2022)

  Antonia Creswell, Murray Shanahan, and Irina Higgins.
  Selection-inference: Exploiting large language models for
  interpretable logical reasoning, 2022.
  URL <https://arxiv.org/abs/2205.09712>.
- Fan et al. (2019)

  Angela Fan, Yacine Jernite, Ethan Perez, David Grangier, Jason Weston, and
  Michael Auli.
  ELI5: Long form question answering.
  In *Proceedings of the 57th Annual Meeting of the Association
  for Computational Linguistics*, pp. 3558–3567, Florence, Italy, July 2019.
  Association for Computational Linguistics.
  doi: 10.18653/v1/P19-1346.
  URL <https://aclanthology.org/P19-1346>.
- Fernyhough (2010)

  Charles Fernyhough.
  Vygotsky, luria, and the social brain.
  *Self and social regulation: Social interaction and the
  development of social understanding and executive functions*, pp. 56–79,
  2010.
- Glaese et al. (2022)

  Amelia Glaese, Nat McAleese, Maja Trebacz, John Aslanides, Vlad Firoiu, Timo
  Ewalds, Maribeth Rauh, Laura Weidinger, Martin Chadwick, Phoebe Thacker, Lucy
  Campbell-Gillingham, Jonathan Uesato, Po-Sen Huang, Ramona Comanescu, Fan
  Yang, Abigail See, Sumanth Dathathri, Rory Greig, Charlie Chen, Doug Fritz,
  Jaume Sanchez Elias, Richard Green, Soňa Mokrá, Nicholas Fernando, Boxi Wu,
  Rachel Foley, Susannah Young, Iason Gabriel, William Isaac, John Mellor,
  Demis Hassabis, Koray Kavukcuoglu, Lisa Anne Hendricks, and Geoffrey Irving.
  Improving alignment of dialogue agents via targeted human judgements,
  2022.
  URL
  <https://storage.googleapis.com/deepmind-media/DeepMind.com/Authors-Notes/sparrow/sparrow-final.pdf>.
- Hosseini-Asl et al. (2020)

  Ehsan Hosseini-Asl, Bryan McCann, Chien-Sheng Wu, Semih Yavuz, and Richard
  Socher.
  A simple language model for task-oriented dialogue.
  *Advances in Neural Information Processing Systems*,
  33:20179–20191, 2020.
- Huang et al. (2022a)

  Wenlong Huang, Pieter Abbeel, Deepak Pathak, and Igor Mordatch.
  Language models as zero-shot planners: Extracting actionable
  knowledge for embodied agents.
  *arXiv preprint arXiv:2201.07207*, 2022a.
- Huang et al. (2022b)

  Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy
  Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, et al.
  Inner monologue: Embodied reasoning through planning with language
  models.
  *arXiv preprint arXiv:2207.05608*, 2022b.
- Karamcheti et al. (2021)

  Siddharth Karamcheti, Megha Srivastava, Percy Liang, and Dorsa Sadigh.
  Lila: Language-informed latent actions.
  In *CoRL*, pp. 1379–1390, 2021.
  URL <https://proceedings.mlr.press/v164/karamcheti22a.html>.
- Kojima et al. (2022)

  Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke
  Iwasawa.
  Large language models are zero-shot reasoners.
  *arXiv preprint arXiv:2205.11916*, 2022.
- Lazaridou et al. (2022)

  Angeliki Lazaridou, Elena Gribovskaya, Wojciech Stokowiec, and Nikolai
  Grigorev.
  Internet-augmented language models through few-shot prompting for
  open-domain question answering.
  *arXiv preprint arXiv:2203.05115*, 2022.
- Lewis et al. (2020)

  Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir
  Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim
  Rocktäschel, et al.
  Retrieval-augmented generation for knowledge-intensive nlp tasks.
  *Advances in Neural Information Processing Systems*,
  33:9459–9474, 2020.
- Li et al. (2022)

  Shuang Li, Xavier Puig, Chris Paxton, Yilun Du, Clinton Wang, Linxi Fan, Tao
  Chen, De-An Huang, Ekin Akyürek, Anima Anandkumar, Jacob Andreas, Igor
  Mordatch, Antonio Torralba, and Yuke Zhu.
  Pre-trained language models for interactive decision-making, 2022.
  URL <https://arxiv.org/abs/2202.01771>.
- Luria (1965)

  Aleksandr Romanovich Luria.
  Ls vygotsky and the problem of localization of functions.
  *Neuropsychologia*, 3(4):387–392, 1965.
- Madaan & Yazdanbakhsh (2022)

  Aman Madaan and Amir Yazdanbakhsh.
  Text and patterns: For effective chain of thought, it takes two to
  tango, 2022.
  URL <https://arxiv.org/abs/2209.07686>.
- Micheli & Fleuret (2021)

  Vincent Micheli and François Fleuret.
  Language models are few-shot butlers.
  *arXiv preprint arXiv:2104.07972*, 2021.
- Nakano et al. (2021)

  Reiichiro Nakano, Jacob Hilton, Suchir Balaji, Jeff Wu, Long Ouyang, Christina
  Kim, Christopher Hesse, Shantanu Jain, Vineet Kosaraju, William Saunders,
  Xu Jiang, Karl Cobbe, Tyna Eloundou, Gretchen Krueger, Kevin Button, Matthew
  Knight, Benjamin Chess, and John Schulman.
  Webgpt: Browser-assisted question-answering with human feedback,
  2021.
  URL <https://arxiv.org/abs/2112.09332>.
- Nye et al. (2021)

  Maxwell Nye, Anders Johan Andreassen, Guy Gur-Ari, Henryk Michalewski, Jacob
  Austin, David Bieber, David Dohan, Aitor Lewkowycz, Maarten Bosma, David
  Luan, Charles Sutton, and Augustus Odena.
  Show your work: Scratchpads for intermediate computation with
  language models, 2021.
  URL <https://arxiv.org/abs/2112.00114>.
- Reed et al. (2022)

  Scott Reed, Konrad Zolna, Emilio Parisotto, Sergio Gomez Colmenarejo, Alexander
  Novikov, Gabriel Barth-Maron, Mai Gimenez, Yury Sulsky, Jackie Kay,
  Jost Tobias Springenberg, Tom Eccles, Jake Bruce, Ali Razavi, Ashley Edwards,
  Nicolas Heess, Yutian Chen, Raia Hadsell, Oriol Vinyals, Mahyar Bordbar, and
  Nando de Freitas.
  A generalist agent, 2022.
  URL <https://arxiv.org/abs/2205.06175>.
- Shridhar et al. (2020a)

  Mohit Shridhar, Jesse Thomason, Daniel Gordon, Yonatan Bisk, Winson Han,
  Roozbeh Mottaghi, Luke Zettlemoyer, and Dieter Fox.
  Alfred: A benchmark for interpreting grounded instructions for
  everyday tasks.
  In *Proceedings of the IEEE/CVF conference on computer vision
  and pattern recognition*, pp. 10740–10749, 2020a.
- Shridhar et al. (2020b)

  Mohit Shridhar, Xingdi Yuan, Marc-Alexandre Côté, Yonatan Bisk, Adam
  Trischler, and Matthew Hausknecht.
  Alfworld: Aligning text and embodied environments for interactive
  learning.
  *arXiv preprint arXiv:2010.03768*, 2020b.
- Shuster et al. (2022a)

  Kurt Shuster, Mojtaba Komeili, Leonard Adolphs, Stephen Roller, Arthur Szlam,
  and Jason Weston.
  Language models that seek for knowledge: Modular search & generation
  for dialogue and prompt completion.
  *arXiv preprint arXiv:2203.13224*, 2022a.
- Shuster et al. (2022b)

  Kurt Shuster, Jing Xu, Mojtaba Komeili, Da Ju, Eric Michael Smith, Stephen
  Roller, Megan Ung, Moya Chen, Kushal Arora, Joshua Lane, Morteza Behrooz,
  William Ngan, Spencer Poff, Naman Goyal, Arthur Szlam, Y-Lan Boureau, Melanie
  Kambadur, and Jason Weston.
  Blenderbot 3: a deployed conversational agent that continually learns
  to responsibly engage, 2022b.
  URL <https://arxiv.org/abs/2208.03188>.
- Thorne et al. (2018)

  James Thorne, Andreas Vlachos, Christos Christodoulopoulos, and Arpit Mittal.
  Fever: a large-scale dataset for fact extraction and verification.
  *arXiv preprint arXiv:1803.05355*, 2018.
- Vygotsky (1987)

  Lev S Vygotsky.
  Thinking and speech.
  *The collected works of LS Vygotsky*, 1:39–285, 1987.
- Wang et al. (2022a)

  Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang,
  Aakanksha Chowdhery, and Denny Zhou.
  Self-consistency improves chain of thought reasoning in language
  models, 2022a.
  URL <https://arxiv.org/abs/2203.11171>.
- Wang et al. (2022b)

  Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, and Denny Zhou.
  Rationale-augmented ensembles in language models.
  *arXiv preprint arXiv:2207.00747*, 2022b.
- Wei et al. (2022)

  Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Ed Chi, Quoc Le, and
  Denny Zhou.
  Chain of thought prompting elicits reasoning in large language
  models.
  *arXiv preprint arXiv:2201.11903*, 2022.
- Yang et al. (2018)

  Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W Cohen, Ruslan
  Salakhutdinov, and Christopher D Manning.
  Hotpotqa: A dataset for diverse, explainable multi-hop question
  answering.
  *arXiv preprint arXiv:1809.09600*, 2018.
- Yao et al. (2020)

  Shunyu Yao, Rohan Rao, Matthew Hausknecht, and Karthik Narasimhan.
  Keep CALM and explore: Language models for action generation in
  text-based games.
  In *Proceedings of the 2020 Conference on Empirical Methods in
  Natural Language Processing (EMNLP)*, pp. 8736–8754, Online, November
  2020. Association for Computational Linguistics.
  doi: 10.18653/v1/2020.emnlp-main.704.
  URL <https://aclanthology.org/2020.emnlp-main.704>.
- Yao et al. (2022)

  Shunyu Yao, Howard Chen, John Yang, and Karthik Narasimhan.
  Webshop: Towards scalable real-world web interaction with grounded
  language agents.
  *arXiv preprint arXiv:2207.01206*, 2022.
- Zelikman et al. (2022)

  Eric Zelikman, Yuhuai Wu, Jesse Mu, and Noah D. Goodman.
  Star: Bootstrapping reasoning with reasoning, 2022.
  URL <https://arxiv.org/abs/2203.14465>.
- Zhou et al. (2022)

  Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang,
  Dale Schuurmans, Olivier Bousquet, Quoc Le, and Ed Chi.
  Least-to-most prompting enables complex reasoning in large language
  models, 2022.
  URL <https://arxiv.org/abs/2205.10625>.
- Zhu et al. (2021)

  Yunchang Zhu, Liang Pang, Yanyan Lan, Huawei Shen, and Xueqi Cheng.
  Adaptive information seeking for open-domain question answering.
  *arXiv preprint arXiv:2109.06747*, 2021.

## 附录 A 补充结果

### A.1 GPT-3 实验

|  | PaLM-540B | GPT-3 |
| --- | --- | --- |
| HotpotQA（精确匹配） | 29.4 | 30.8 |
| ALFWorld（成功率 %） | 70.9 | 78.4 |

表 5：使用 PaLM-540B 与 GPT-3（text-davinci-002，贪心解码）的 ReAct 提示结果。在 HotpotQA 上，我们随机抽取 500 个验证问题的子集。在 ALFWorld 上，我们使用全部 134 个未见过的验证任务实例，并采用按 PaLM-540B 选出的最佳提示集。

我们另行运行了 GPT-3（Brown et al., 2020）实验，以确认 ReAct 提示性能在不同大型语言模型间的普适性。如表 5 所示，GPT-3（text-davinci-002，贪心解码）在 HotpotQA 与 ALFWorld 上一致地优于 PaLM-540B，可能是因为它经过人类指令遵循的微调。这表明 ReAct 提示在不同任务、不同大型语言模型上均有效。这些实验的代码见 <https://react-lm.github.io/>。

### A.2 ReAct 在 HotpotQA 上获取最新知识

图 4：另一个 HotpotQA 问题示例，其原始标签已过时。只有 ReAct 得益于真实世界网页交互加推理，能够获取最新答案。

在检查轨迹时，我们还发现 ReAct 有时与数据集标签不一致，因为标签本身可能过时。例如图 4 所示，问题询问某酒店的大小，而该数值自 HotpotQA 构建之时起已增大。Standard 与 CoT 因幻觉给出错误答案；Act 尽管能与真实网络交互，却因缺乏引导如何与互联网交互以完成问答的推理而失败。只有 ReAct 能从互联网检索到最新信息并给出合理答案。因此，更好地融入推理能力，或将令近期互联网增强的语言模型（Nakano et al., 2021；Lazaridou et al., 2022；Shuster et al., 2022a）在最新任务求解中受益。

### A.3 AlfWorld 上的人在回路行为纠正

图 5：ReAct 在 AlfWorld 中的一个人在回路行为纠正示例。(a) ReAct 轨迹因一处幻觉思考（Act 17）而失败。(b) 人类仅编辑两处思考（Act 17、23）后，ReAct 轨迹即产生理想的推理轨迹与行动并取得成功。

我们还探索了与 ReAct 的人在回路交互，允许人类检查并编辑 ReAct 的推理轨迹。图 5 表明：只需删去 Act 17 中一句幻觉句子并在 Act 23 中加入一些提示，就能让 ReAct 大幅改变行为以契合这些人类思考编辑，并成功完成任务。从人类视角看，求解这样的任务变得显著更容易——从键入数十个行动变为只编辑两三处思考，这带来了新型的人机协作。我们注意到，这种即时的策略编辑对 Act 与以往的 RL 方法都很困难：人类无法更改模型参数，而改动少数几个行动未必能改变模型其余部分的行为。这一范式也超越了 Huang et al. (2022b) 中通过人类对话更新目标或子目标的设定——编辑 ReAct 思考固然可以做到这些，还能修改模型的内部信念、推理风格或灵活思考空间所支持的任何内容，以更好地求解任务。我们相信这是人类对齐的一个激动人心的方向，更系统的研究留作未来工作。

## 附录 B 实验细节

### B.1 HotpotQA 微调细节

所有微调均使用 batch size 64。在 PaLM-8B 上，ReAct 与 Act 方法微调 4,000 步，Standard 与 CoT 方法微调 2,000 步。在 PaLM-62B 上，ReAct 与 Act 方法微调 4,000 步，Standard 与 CoT 方法微调 1,000 步。我们发现 ReAct 与 Act 方法总体上受益于更多训练步数（及更多训练数据），而 Standard 与 CoT 方法在微调后很快退化。

### B.2 AlfWorld IM 式细节

对于 IM 式消融，ReAct 所用的同一些专家轨迹被重新标注为轨迹内的密集外部反馈思考，这些思考把 ReAct-IM 限制为只能思考：（1）分解当前目标，（2）当前需要完成的子目标。特别地，ReAct-IM 缺少以下思考：（1）判断子目标何时完成，（2）确定下一个子目标应是什么，（3）引导 LLM 调用其内部预训练知识来判断物品可能位于环境中的何处。

## 附录 C 提示词

### C.1 HotpotQA
Hotpot QA Prompts

Original

Question

What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?

Answer

1,800 to 7,000 ft

Question

Musician and satirist Allie Goertz wrote a song about the "The Simpsons" character Milhouse, who Matt Groening named after who?

Answer

Richard Nixon

Question

Which documentary is about Finnish rock groups, Adam Clayton Powell or The Saimaa Gesture?

Answer

The Saimaa Gesture

Question

What profession does Nicholas Ray and Elia Kazan have in common?

Answer

director, screenwriter, actor

Question

Which magazine was started first Arthur’s Magazine or First for Women?

Answer

Arthur’s Magazine

Question

Were Pavel Urysohn and Leonid Levin known for the same type of work?

Answer

Yes

Act

Question

What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?

Action 1

Search[Colorado orogeny]

Observation 1

The Colorado orogeny was an episode of mountain building (an orogeny) in Colorado and surrounding areas.

Action 2

Lookup[eastern sector]

Observation 2

(Result 1 / 1) The eastern sector extends into the High Plains and is called the Central Plains orogeny.

Action 3

Search[High Plains]

Observation 3

High Plains refers to one of two distinct land regions:

Action 4

Search[High Plains (United States)]

Observation 4

The High Plains are a subregion of the Great Plains. From east to west, the High Plains rise in elevation from around 1,800 to 7,000 ft (550 to 2,130 m).[3]

Action 5

Finish[1,800 to 7,000 ft]

Question

Musician and satirist Allie Goertz wrote a song about the "The Simpsons" character Milhouse, who Matt Groening named after who?

Action 1

Search[Milhouse]

Observation 1

Milhouse Mussolini Van Houten is a recurring character in the Fox animated television series The Simpsons voiced by Pamela Hayden and created by Matt Groening.

Action 2

Lookup[named after]

Observation 2

(Result 1 / 1) Milhouse was named after U.S. president Richard Nixon, whose middle name was Milhous.

Action 3

Finish[Richard Nixon]

Question

Which documentary is about Finnish rock groups, Adam Clayton Powell or The Saimaa Gesture?

Action 1

Search[Adam Clayton Powell]

Observation 1

Could not find [Adam Clayton Powell]. Similar: [’Adam Clayton Powell III’, ’Seventh Avenue (Manhattan)’, ’Adam Clayton Powell Jr. State Office Building’, ’Isabel Washington Powell’, ’Adam Powell’, ’Adam Clayton Powell (film)’, ’Giancarlo Esposito’].

Action 2

Search[Adam Clayton Powell (film)]

Observation 2

Adam Clayton Powell is a 1989 American documentary film directed by Richard Kilberg. The film is about the rise and fall of influential African-American politician Adam Clayton Powell Jr.[3][4] It was later aired as part of the PBS series The American Experience.

Action 3

Finish[The Saimaa Gesture]

Question

What profession does Nicholas Ray and Elia Kazan have in common?

Action 1

Search[Nicholas Ray]

Observation 1

Nicholas Ray (born Raymond Nicholas Kienzle Jr., August 7, 1911 – June 16, 1979) was an American film director, screenwriter, and actor best known for the 1955 film Rebel Without a Cause.

Action 2

Search[Elia Kazan]

Observation 2

Elia Kazan was an American film and theatre director, producer, screenwriter and actor.

Continued on next page

Hotpot QA Prompts – Continued from previous page

Action 3

Finish[director, screenwriter, actor]

Question

Which magazine was started first Arthur’s Magazine or First for Women?

Action 1

Search[Arthur’s Magazine]

Observation 1

Arthur’s Magazine (1844--1846) was an American literary periodical published in Philadelphia in the 19th century.

Action 2

Search[First for Women]

Observation 2

First for Women is a woman’s magazine published by Bauer Media Group in the USA.[1] The magazine was started in 1989.

Action 3

Finish[Arthur’s Magazine]

Question

Were Pavel Urysohn and Leonid Levin known for the same type of work?

Action 1

Search[Pavel Urysohn]

Observation 1

Pavel Samuilovich Urysohn (February 3, 1898 - August 17, 1924) was a Soviet mathematician who is best known for his contributions in dimension theory.

Action 2

Search[Leonid Levin]

Observation 2

Leonid Anatolievich Levin is a Soviet-American mathematician and computer scientist.

Action 3

Finish[yes]

CoT

Question

What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?

Thought

Let’s think step by step. The eastern sector of Colorado orogeny extends into the High Plains. High Plains rise in elevation from around 1,800 to 7,000 ft, so the answer is 1,800 to 7,000 ft.

Answer

1,800 to 7,000 ft

Question

Musician and satirist Allie Goertz wrote a song about the "The Simpsons" character Milhouse, who Matt Groening named after who?

Thought

Let’s think step by step. Milhouse was named after U.S. president Richard Nixon, so the answer is Richard Nixon.

Answer

Richard Nixon

Question

Which documentary is about Finnish rock groups, Adam Clayton Powell or The Saimaa Gesture?

Thought

Let’s think step by step. Adam Clayton Powell (film) is a documentary about an African-American politician, not Finnish rock groups. So the documentary about Finnish rock groups must instead be The Saimaa Gesture.

Answer

The Saimaa Gesture

Question

What profession does Nicholas Ray and Elia Kazan have in common?

Thought

Let’s think step by step. Professions of Nicholas Ray are director, screenwriter, and actor. Professions of Elia Kazan are director, producer, screenwriter, and actor. So profession Nicholas Ray and Elia Kazan have in common is director, screenwriter, and actor.

Answer

director, screenwriter, actor

Question

Which magazine was started first Arthur’s Magazine or First for Women?

Thought

Let’s think step by step. Arthur’s Magazine was started in 1844. First for Women was started in 1989. 1844 (Arthur’s Magazine) < 1989 (First for Women), so Arthur’s Magazine was started first.

Answer

Arthur’s Magazine

Question

Were Pavel Urysohn and Leonid Levin known for the same type of work?

Thought

Let’s think step by step. Pavel Urysohn is a mathematician. Leonid Levin is a mathematician and computer scientist. So Pavel Urysohn and Leonid Levin have the same type of work.

Answer

Yes

ReAct

Question

What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?

Thought 1

I need to search Colorado orogeny, find the area that the eastern sector of the Colorado orogeny extends into, then find the elevation range of the area.

Action 1

Search[Colorado orogeny]

Observation 1

The Colorado orogeny was an episode of mountain building (an orogeny) in Colorado and surrounding areas.

Thought 2

It does not mention the eastern sector. So I need to look up eastern sector.

Action 2

Lookup[eastern sector]

Observation 2

(Result 1 / 1) The eastern sector extends into the High Plains and is called the Central Plains orogeny.

Thought 3

The eastern sector of Colorado orogeny extends into the High Plains. So I need to search High Plains and find its elevation range.

Action 3

Search[High Plains]

Observation 3

High Plains refers to one of two distinct land regions

Thought 4

I need to instead search High Plains (United States).

Action 4

Search[High Plains (United States)]

Continued on next page

Hotpot QA Prompts – Continued from previous page

Observation 4

The High Plains are a subregion of the Great Plains. From east to west, the High Plains rise in elevation from around 1,800 to 7,000 ft (550 to 2,130 m).[3]

Thought 5

High Plains rise in elevation from around 1,800 to 7,000 ft, so the answer is 1,800 to 7,000 ft.

Action 5

Finish[1,800 to 7,000 ft]

Question

Musician and satirist Allie Goertz wrote a song about the "The Simpsons" character Milhouse, who Matt Groening named after who?

Thought 1

The question simplifies to "The Simpsons" character Milhouse is named after who. I only need to search Milhouse and find who it is named after.

Action 1

Search[Milhouse]

Observation 1

Milhouse Mussolini Van Houten is a recurring character in the Fox animated television series The Simpsons voiced by Pamela Hayden and created by Matt Groening.

Thought 2

The paragraph does not tell who Milhouse is named after, maybe I can look up "named after".

Action 2

Lookup[named after]

Observation 2

(Result 1 / 1) Milhouse was named after U.S. president Richard Nixon, whose middle name was Milhous.

Thought 3

Milhouse was named after U.S. president Richard Nixon, so the answer is Richard Nixon.

Action 3

Finish[Richard Nixon]

Question

Which documentary is about Finnish rock groups, Adam Clayton Powell or The Saimaa Gesture?

Thought 1

I need to search Adam Clayton Powell and The Saimaa Gesture, and find which documentary is about Finnish rock groups.

Action 1

Search[Adam Clayton Powell]

Observation 1

Could not find [Adam Clayton Powell]. Similar: [’Adam Clayton Powell III’, ’Seventh Avenue (Manhattan)’, ’Adam Clayton Powell Jr. State Office Building’, ’Isabel Washington Powell’, ’Adam Powell’, ’Adam Clayton Powell (film)’, ’Giancarlo Esposito’].

Thought 2

To find the documentary, I can search Adam Clayton Powell (film).

Action 2

Search[Adam Clayton Powell (film)]

Observation 2

Adam Clayton Powell is a 1989 American documentary film directed by Richard Kilberg.
The film is about the rise and fall of influential African-American politician Adam Clayton Powell Jr.[3][4] It was later aired as part of the PBS series The American Experience.

Thought 3

Adam Clayton Powell (film) is a documentary about an African-American politician, not Finnish rock groups. So the documentary about Finnish rock groups must instead be The Saimaa Gesture.

Action 3

Finish[The Saimaa Gesture]

Question

What profession does Nicholas Ray and Elia Kazan have in common?

Thought 1

I need to search Nicholas Ray and Elia Kazan, find their professions, then find the profession they have in common.

Action 1

Search[Nicholas Ray]

Observation 1

Nicholas Ray (born Raymond Nicholas Kienzle Jr., August 7, 1911 – June 16, 1979) was an American film director, screenwriter, and actor best known for the 1955 film Rebel Without a Cause.

Thought 2

Professions of Nicholas Ray are director, screenwriter, and actor. I need to search Elia Kazan next and find his professions.

Action 2

Search[Elia Kazan]

Observation 2

Elia Kazan was an American film and theatre director, producer, screenwriter and actor.

Thought 3

Professions of Elia Kazan are director, producer, screenwriter, and actor. So profession Nicholas Ray and Elia Kazan have in common is director, screenwriter, and actor.

Action 3

Finish[director, screenwriter, actor]

Question

Which magazine was started first Arthur’s Magazine or First for Women?

Thought 1

I need to search Arthur’s Magazine and First for Women, and find which was started first.

Action 1

Search[Arthur’s Magazine]

Observation 1

Arthur’s Magazine (1844-1846) was an American literary periodical published in Philadelphia in the 19th century.

Thought 2

Arthur’s Magazine was started in 1844. I need to search First for Women next.

Action 2

Search[First for Women]

Observation 2

First for Women is a woman’s magazine published by Bauer Media Group in the USA.[1] The magazine was started in 1989.

Thought 3

First for Women was started in 1989. 1844 (Arthur’s Magazine) < 1989 (First for Women), so Arthur’s Magazine was started first.

Action 3

Finish[Arthur’s Magazine]

Question

Were Pavel Urysohn and Leonid Levin known for the same type of work?

Thought 1

I need to search Pavel Urysohn and Leonid Levin, find their types of work, then find if they are the same.

Action 1

Search[Pavel Urysohn]

Continued on next page

Hotpot QA Prompts – Continued from previous page

Observation 1

Pavel Samuilovich Urysohn (February 3, 1898 - August 17, 1924) was a Soviet mathematician who is best known for his contributions in dimension theory.

Thought 2

Pavel Urysohn is a mathematician. I need to search Leonid Levin next and find its type of work.

Action 2

Search[Leonid Levin]

Observation 2

Leonid Anatolievich Levin is a Soviet-American mathematician and computer scientist.

Thought 3

Leonid Levin is a mathematician and computer scientist. So Pavel Urysohn and Leonid Levin have the same type of work.

Action 3

Finish[yes]

### C.2 Fever


FEVER Prompts

Original

Determine if there is Observation that SUPPORTS or REFUTES a Claim, or if there is NOT ENOUGH INFORMATION.

Claim

Nikolaj Coster-Waldau worked with the Fox Broadcasting Company.

Answer

SUPPORTS

Claim

Stranger Things is set in Bloomington, Indiana.

Answer

REFUTES

Claim

Beautiful reached number two on the Billboard Hot 100 in 2003.

Answer

NOT ENOUGH INFO

Act

Determine if there is Observation that SUPPORTS or REFUTES a Claim, or if there is NOT ENOUGH INFORMATION.

Claim

Nikolaj Coster-Waldau worked with the Fox Broadcasting Company.

Action2

Search[Nikolaj Coster-Waldau]

Observation 1

Nikolaj William Coster-Waldau (born 27 July 1970) is a Danish actor and producer. He graduated from the Danish National School of Performing Arts in Copenhagen in 1993,[1] and had his breakthrough role in Denmark with the film Nightwatch (1994). He played Jaime Lannister in the HBO fantasy drama series Game of Thrones, for which he received two Primetime Emmy Award nominations for Outstanding Supporting Actor in a Drama Series.. Coster-Waldau has appeared in numerous films in his native Denmark and Scandinavia, including Headhunters (2011) and A Thousand Times Good Night (2013). In the U.S, his debut film role was in the war film Black Hawk Down (2001), playing Medal of Honor recipient Gary Gordon.[2] He then played a detective in the short-lived Fox television series New Amsterdam (2008), and appeared in the 2009 Fox television film Virtuality, originally intended as a pilot.

Action 2

Finish[SUPPORTS]

Claim

Stranger Things is set in Bloomington, Indiana.

Action 1

Search[Stranger Things]

Observation 1

Stranger Things is an American science fiction horror drama television series created by the Duffer Brothers. Set in the 1980s, primarily in the fictional town of Hawkins, Indiana, the series centers on a number of mysteries and supernatural events occurring around the town and their impact on an ensemble of child and adult characters.

Action 2

Finish[REFUTES]

Claim

Beautiful reached number two on the Billboard Hot 100 in 2003.

Action 1

Search[Beautiful]

Observation 1

Could not find [Beautiful]. Similar: [’Beautiful’, ’Beautiful, Beautiful’, ’A Beautiful Mind (film)’, ’Beautiful (Christina Aguilera song)’, ’Life Is Beautiful’].

Action 2

Search[Beautiful (Christina Aguilera song)

Observation 2

"Beautiful" is a song recorded by American singer Christina Aguilera for her fourth studio album, Stripped (2002).

Action 3

Lookup[Billboard Hot 100]

Observation 3

(Result 1 / 3) The song peaked at number two on the Billboard Hot 100 in the United States, where it was certified Gold for 500,000 units shipped.

Action 4

Finish[NOT ENOUGH INFO]

CoT

Determine if there is Observation that SUPPORTS or REFUTES a Claim, or if there is NOT ENOUGH INFORMATION.

Claim

Nikolaj Coster-Waldau worked with the Fox Broadcasting Company.

Thought

Nikolaj William Coster-Waldau appeared in the 2009 Fox television film Virtuality, so he has worked with the Fox Broadcasting Company.

Answer

SUPPORTS

Claim

Stranger Things is set in Bloomington, Indiana.

Thought

Stranger Things is in the fictional town of Hawkins, Indiana, not in Bloomington, Indiana.

Answer

REFUTES

Continued on next page

Fever Prompts – Continued from previous page

Claim

Beautiful reached number two on the Billboard Hot 100 in 2003.

Thought

The song peaked at number two on the Billboard Hot 100 in the United States, but not sure if it was in 2003.

Answer

NOT ENOUGH INFO

ReAct

Determine if there is Observation that SUPPORTS or REFUTES a Claim, or if there is NOT ENOUGH INFORMATION.

Claim

Nikolaj Coster-Waldau worked with the Fox Broadcasting Company.

Thought 1

I need to search Nikolaj Coster-Waldau and find if he has worked with the Fox Broadcasting Company.

Action 1

Search[Nikolaj Coster-Waldau]

Observation 1

Nikolaj William Coster-Waldau (born 27 July 1970) is a Danish actor and producer. He graduated from the Danish National School of Performing Arts in Copenhagen in 1993,[1] and had his breakthrough role in Denmark with the film Nightwatch (1994). He played Jaime Lannister in the HBO fantasy drama series Game of Thrones, for which he received two Primetime Emmy Award nominations for Outstanding Supporting Actor in a Drama Series.. Coster-Waldau has appeared in numerous films in his native Denmark and Scandinavia, including Headhunters (2011) and A Thousand Times Good Night (2013). In the U.S, his debut film role was in the war film Black Hawk Down (2001), playing Medal of Honor recipient Gary Gordon.[2] He then played a detective in the short-lived Fox television series New Amsterdam (2008), and appeared in the 2009 Fox television film Virtuality, originally intended as a pilot.

Thought 2

Because he "appeared in the 2009 Fox television film Virtuality", he should have worked with the Fox Broadcasting Company.

Action 2

Finish[SUPPORTS]

Claim

Stranger Things is set in Bloomington, Indiana.

Thought 1

I should search for Stranger Things, and see if it is set in Bloomington, Indiana.

Action 1

Search[Stranger Things]

Observation 1

Stranger Things is an American science fiction horror drama television series created by the Duffer Brothers. Set in the 1980s, primarily in the fictional town of Hawkins, Indiana, the series centers on a number of mysteries and supernatural events occurring around the town and their impact on an ensemble of child and adult characters.

Thought 2

The observation says that it is set in a "fictional town of Hawkins, Indiana", so it is not set in Bloomington.

Action 2

Finish[REFUTES]

Claim

Beautiful reached number two on the Billboard Hot 100 in 2003.

Thought 1

I need to search the song Beautiful and find if it reached number two on the Billboard Hot 100 in 2003.

Action 1

Search[Beautiful]

Observation 1

Could not find [Beautiful]. Similar: [’Beautiful’, ’Beautiful, Beautiful’, ’A Beautiful Mind (film)’, ’Beautiful (Christina Aguilera song)’, ’Life Is Beautiful’].

Thought 2

From suggestions, I should search "Beautiful (Christina Aguilera song)" to find the song.

Action 2

Search[Beautiful (Christina Aguilera song)]

Observation 2

"Beautiful" is a song recorded by American singer Christina Aguilera for her fourth studio album, Stripped (2002).

Thought 3

It does not mention Billboard, so I need to look up "Billboard Hot 100" to find if it reached number two on it in 2003.

Action 3

Lookup[Billboard Hot 100]

Observation 3

(Result 1 / 3) The song peaked at number two on the Billboard Hot 100 in the United States, where it was certified Gold for 500,000 units shipped.

Thought 4

It only says the song peaked at number two on the Billboard Hot 100, but not if it was in 2003. I am not sure if this claim is true or not.

Action 4

Finish[NOT ENOUGH INFO]

### C.3 Webshop

表 6：第 4 节 Webshop 实验所用提示。左侧提示用于 Act，右侧提示（增加推理）用于 ReAct。

|  |  |
| --- | --- |
| Instruction: i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars | |
| Act | ReAct |
| Action: search[3 ounce bright citrus deodorant sensitive skin]  Observation:  [ Back to Search ]  Page 1 (Total results: 50)  [Next]  [B078GWRC1J]  Bright Citrus Deodorant by Earth Mama | Natural and Safe for  Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic  Calendula 3-Ounce  $10.99  [B078GTKVXY]  Ginger Fresh Deodorant by Earth Mama | Natural and Safe for  Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic  Calendula 3-Ounce  $10.99  [B08KBVJ4XN]  Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men  , Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar  & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage,  2.7 oz, 2-Pack)  $15.95  Action: click[B078GWRC1J]  Observation:  [Back to Search]  [Prev]  scent [assorted scents][bright citrus][calming lavender][ginger  [fresh] simply non-scents]  size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2  -pack)]  Bright Citrus Deodorant by Earth Mama | Natural and Safe for  Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic  Calendula 3-Ounce  Price: $10.99  Rating: N.A.  [Description]  [Features]  [Reviews]  [Buy Now]  Action: click[bright citrus]  Observation: You have clicked bright citrus.  Action: click[3 ounce (pack of 1)]  Observation: You have clicked 3 ounce (pack of 1).  Action: click[Buy Now] | Action: search[3 ounce bright citrus deodorant sensitive skin  Observation:  [ Back to Search ]  Page 1 (Total results: 50)  [Next]  [B078GWRC1J]  Bright Citrus Deodorant by Earth Mama | Natural and Safe for  Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic  Calendula 3-Ounce  $10.99  [B078GTKVXY]  Ginger Fresh Deodorant by Earth Mama | Natural and Safe for  Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic  Calendula 3-Ounce  $10.99  [B08KBVJ4XN]  Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men  , Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar  & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage,  2.7 oz, 2-Pack)  $15.95  Action: think[B078GWRC1J and B078GTKVXY are bright citrus  deodorant less then 50 dollars. I can check B078GWRC1J first.  Observation: OK.  Action: click[B078GWRC1J]  Observation:  [Back to Search]  [Prev]  scent [assorted scents][bright citrus][calming lavender][ginger  [fresh] simply non-scents]  size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2  -pack)]  Bright Citrus Deodorant by Earth Mama | Natural and Safe for  Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic  Calendula 3-Ounce  Price: $10.99  Rating: N.A.  [Description]  [Features]  [Reviews]  [Buy Now]  Action: think[For 3 ounce bottle of bright citrus deodorant  for sensitive skin, the item has options ’bright citrus’  and ’3 ounce (pack of 1)’ and seems good to buy.]  Observation: OK.  Action: click[bright citrus]  Observation: You have clicked bright citrus.  Action: click[3 ounce (pack of 1)]  Observation: You have clicked 3 ounce (pack of 1).  Action: click[Buy Now] |

### C.4 ALFWorld

表 7：ALFWorld clean 任务上的一个 Act 提示。不提供任何思考。

|  |
| --- |
| You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1. Your task is to: put a clean lettuce in diningtable. |
| >> go to fridge 1 |
| The fridge 1 is closed. |
| >> open fridge 1 |
| You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2. |
| >> go to diningtable 1 |
| On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1. |
| >> take lettuce 1 from diningtable 1 |
| You pick up the lettuce 1 from the diningtable 1. |
| >> go to sinkbasin 1 |
| On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3. |
| >> clean lettuce 1 with sinkbasin 1 |
| You clean the lettuce 1 using the sinkbasin 1. |
| >> think: Now I clean a lettuce (1). Next, I need to put it in/on diningtable 1. |
| OK. |
| >> go to diningtable 1 |
| On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1. |
| >> put lettuce 1 in/on diningtable 1 |
| You put the lettuce 1 in/on the diningtable 1. |
表 8：ALFWorld clean 任务上的一个 ReAct 提示。

|  |
| --- |
| You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1. Your task is to: put a clean lettuce in diningtable. |
| > think: To solve the task, I need to find and take a lettuce, then clean it with sinkbasin, then put it in diningtable. |
| OK. |
| > think: First I need to find a lettuce. A lettuce is more likely to appear in fridge (1), diningtable (1), sinkbasin (1), stoveburner (1-3), cabinet (1-13). I can check one by one, starting with fridge 1. |
| OK. |
| > go to fridge 1 |
| The fridge 1 is closed. |
| > open fridge 1 |
| You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2. |
| > go to diningtable 1 |
| On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1. |
| > think: Now I find a lettuce (1). Next, I need to take it. |
| OK. |
| > take lettuce 1 from diningtable 1 |
| You pick up the lettuce 1 from the diningtable 1. |
| > think: Now I take a lettuce (1). Next, I need to go to sinkbasin (1) and clean it. |
| OK. |
| > go to sinkbasin 1 |
| On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3. |
| > clean lettuce 1 with sinkbasin 1 |
| You clean the lettuce 1 using the sinkbasin 1. |
| > think: Now I clean a lettuce (1). Next, I need to put it in/on diningtable 1. |
| OK. |
| > go to diningtable 1 |
| On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1. |
| > put lettuce 1 in/on diningtable 1 |
| You put the lettuce 1 in/on the diningtable 1. |
|  |
表 9：ALFWorld clean 任务上的一个 ReAct-IM 提示。

|  |
| --- |
| You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1. Your task is to: put a clean lettuce in diningtable. |
| > think: To solve the task, I need to find and take a lettuce, then clean it with sinkbasin, then put it in diningtable. |
| OK. |
| > think: First I need to find a lettuce. |
| OK. |
| > go to fridge 1 |
| The fridge 1 is closed. |
| > think: First I need to find a lettuce. |
| OK. |
| > open fridge 1 |
| You open the fridge 1. The fridge 1 is open. In it, you see a cup 3, a egg 2, a potato 3, and a potato 2. |
| > think: First I need to find a lettuce. |
| OK. |
| > go to diningtable 1 |
| On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a lettuce 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1. |
| > think: First I need to find a lettuce. |
| OK. |
| > take lettuce 1 from diningtable 1 |
| You pick up the lettuce 1 from the diningtable 1. |
| > think: I need to clean this lettuce (1) using sinkbasin 1. |
| OK. |
| > go to sinkbasin 1 |
| On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3. |
| > think: I need to clean this lettuce (1) using sinkbasin 1. |
| OK. |
| > clean lettuce 1 with sinkbasin 1 |
| You clean the lettuce 1 using the sinkbasin 1. |
| > think: I need to put this cleaned lettuce (1) in/on diningtable 1. |
| OK. |
| > go to diningtable 1 |
| On the diningtable 1, you see a apple 1, a bread 1, a butterknife 2, a cup 2, a fork 2, a knife 2, a knife 1, a ladle 1, a mug 2, a mug 1, a pan 2, a peppershaker 1, a spatula 3, a tomato 2, and a tomato 1. |
| > think: I need to put this cleaned lettuce (1) in/on diningtable 1. |
| OK. |
| > put lettuce 1 in/on diningtable 1 |
| You put the lettuce 1 in/on the diningtable 1. |
## 附录 D 轨迹

### D.1 FEVER 轨迹

下面给出 ReAct、CoT 与 Act 在 FEVER 开发集若干随机抽取示例上产生的轨迹。为节省篇幅，搜索结果从略。

Example 2491 (gt: REFUTES)

ReAct

Claim:

Bermuda Triangle is a loosely-defined region in the Pacific Ocean.

Thought 1:

I need to search Bermuda Triangle and find if it is in the Pacific Ocean.

Action 1:

Search[Bermuda Triangle]

Observation 1:

Reportedly haunted locations...

Thought 2:

The observation says that it is in the western part of the North Atlantic Ocean, so it is not in the Pacific Ocean.

Action 2:

Finish[REFUTES]

Observation 2:

Episode finished

Act

Claim:

Bermuda Triangle is a loosely-defined region in the Pacific Ocean.

Action 1

: Search[Bermuda Triangle]

Observation 1

: Reportedly haunted locations:...

Action 2:

Finish[REFUTES]

Observation 2:

Episode finished

CoT

Claim:

Bermuda Triangle is a loosely-defined region in the Pacific Ocean.

Thought:

Let’s think step by step. The Bermuda Triangle is a loosely-defined region in the Atlantic Ocean. The Pacific Ocean is not the Atlantic Ocean.

Answer:

REFUTES

Example 5908 (gt: SUPPORTS)

ReAct

Claim:

Princess Mononoke is a film.

Thought 1:

I need to search Princess Mononoke and find if it is a film.

Action 1:

Search[Princess Mononoke]

Observation 1:

Princess Mononoke ...

Thought 2:

From the observation, it says that Princess Mononoke is a film.

Action 2:

Finish[SUPPORTS]

Observation 2:

Episode finished

Act

Claim:

Princess Mononoke is a film.

Action 1:

Search[Princess Mononoke]

Observation 1:

Princess Mononoke ...

Action 2:

Finish[SUPPORTS]

Observation 2:

Episode finished

CoT

Claim:

Princess Mononoke is a film.

Thought:

Let’s think step by step. Princess Mononoke is a movie, and movies are films.

Answer:

SUPPORTS

Example 1951 (gt: REFUTES)

ReAct

Claim:

Soyuz was part of the American space program.

Thought 1:

I need to search Soyuz and find if it was part of the American space program.

Action 1:

Search[Soyuz]

Observation 1:

Soyuz is a transliteration...

Thought 2:

It does not mention the American space program, so I need to search "American space program" to find if it was part of it.

Action 2:

Search[American space program]

Observation 2:

The space policy...

Thought 3:

It does not mention Soyuz, so I am not sure if this claim is true or not.

Action 3:

Finish[NOT ENOUGH INFO]

Observation 3:

Episode finished

Act

Claim:

Soyuz was part of the American space program.

Action 1:

Search[Soyuz]

Observation 1:

Soyuz is a transliteration...

Action 2:

Finish[NOT ENOUGH INFO]

Observation 2:

Episode finished

CoT

Claim:

Soyuz was part of the American space program.

Thought:

Let’s think step by step. Soyuz is a Russian spacecraft. The American space program is NASA. NASA and Russia have worked together on the International Space Station.

Answer:

SUPPORTS

Example 3208 (gt: REFUTES)

ReAct

Claim:

Reign Over Me is an American film made in 2010.

Thought 1:

I need to search for Reign Over Me and find if it is an American film made in 2010.

Action 1:

Search[Reign Over Me]

Observation 1:

Reign Over Me ...

Thought 2:

The observation says that it is an American film made in 2007, so it is not made in 2010.

Action 2:

Finish[REFUTES]

Observation 2:

Episode finished

Act

Claim:

Reign Over Me is an American film made in 2010.

Action 1:

Search[Reign Over Me]

Action 2:

Finish[SUPPORTS]

Observation 2:

Episode finished

CoT

Claim:

Reign Over Me is an American film made in 2010.

Thought:

Let’s think step by step. First, is Reign Over Me an American film? Yes, it is. Second, was it made in 2010? Yes, it was.

Answer:

SUPPORTS

### D.2 ALFWorld 轨迹

我们给出 ReAct、Act 与 ReAct-IM 在同一局 ALFWorld 游戏（pick_clean_then_place_in_recep-Knife-None-CounterTop-10/ 的 trial_T20190909_110445_675754）上的示例轨迹。

#### D.2.1 ReAct 轨迹

ReAct 能正确找到小刀、清洗它，然后把它放到台面上。


ReAct ALFWorld trajectory

You are in the middle of a room. Looking quickly around you, you see a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.

Your task is to: put a clean knife in countertop.

> think: To solve the task, I need to find and take a knife, then clean it with sinkbasin, then put it in countertop.

OK.

> think: First I need to find a knife. A knife is more likely to appear in cabinet (1-6), drawer (1-3), countertop (1-3), fridge (1), garbagecan (1), shelf (1-3), sinkbasin (1), stoveburner (1-4), toaster (1). I can check one by one, starting with cabinet 1.

OK.

> go to cabinet 1

On the cabinet 1, you see a bowl 1.

> go to cabinet 2

The cabinet 2 is closed.

> go to cabinet 3

On the cabinet 3, you see a glassbottle 1.

> go to cabinet 4

On the cabinet 4, you see a mug 1.

> go to cabinet 5

The cabinet 5 is closed.

> go to cabinet 6

The cabinet 6 is closed.

> go to drawer 1

The drawer 1 is closed.

> go to drawer 2

The drawer 2 is closed.

> go to drawer 3

The drawer 3 is closed.

> go to countertop 1

On the countertop 1, you see a lettuce 2, a mug 2, a peppershaker 1, and a spoon 2.

> go to countertop 2

On the countertop 2, you see a cup 1, a dishsponge 1, a glassbottle 3, a knife 1, a plate 2, a potato 3, and a statue 1.

> think: Now I find a knife (1). Next, I need to take it.

OK.

> take knife 1 from countertop 2

You pick up the knife 1 from the countertop 2.

> think: Now I take a knife (1). Next, I need to go to sinkbasin (1) and clean it.

OK.

> go to sinkbasin 1

On the sinkbasin 1, you see a fork 3, a lettuce 3, and a spatula 2.

> clean knife 1 with sinkbasin 1

You clean the knife 1 using the sinkbasin 1.

> think: Now I clean a knife (1). Next, I need to put it in/on countertop 1.

OK.

> go to countertop 1

On the countertop 1, you see a lettuce 2, a mug 2, a peppershaker 1, and a spoon 2.

> put knife 1 in/on countertop 1

You put the knife 1 in/on the countertop 1.

#### D.2.2 Act 轨迹

Act 能正确找到小刀，但尚未真正走到水池就试图用水池清洗它。此后模型无法恢复，卡在重复同一串命令上。若用 ReAct，既有的思考会明确指出小刀已被拿取、下一个子目标是走到水池清洗它。

Act ALFWorld trajectory

You are in the middle of a room. Looking quickly around you, you see a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.

Your task is to: put a clean knife in countertop.

> go to countertop 1

On the countertop 1, you see a lettuce 2, a mug 2, a peppershaker 1, and a spoon 2.

> go to countertop 2

On the countertop 2, you see a cup 1, a dishsponge 1, a glassbottle 3, a knife 1, a plate 2, a potato 3, and a statue 1.

> take knife 1 from countertop 2

You pick up the knife 1 from the countertop 2.

> go to countertop 1

On the countertop 1, you see a lettuce 2, a mug 2, a peppershaker 1, and a spoon 2.

> clean knife 1 with sinkbasin 1

Nothing happens.

> go to countertop 3

On the countertop 3, you see a bread 3, a butterknife 2, a cellphone 1, a creditcard 1, a fork 2, a houseplant 1, a knife 2, a spatula 1, a statue 3, a tomato 3, a tomato 2, a tomato 1, and a vase 2.

> take knife 2 from countertop 3

Nothing happens.

> go to countertop 2

On the countertop 2, you see a cup 1, a dishsponge 1, a glassbottle 3, a plate 2, a potato 3, and a statue 1.

> take knife 1 from countertop 2

Nothing happens.

> go to countertop 1

On the countertop 1, you see a lettuce 2, a mug 2, a peppershaker 1, and a spoon 2.

> clean knife 1 with sinkbasin 1

Nothing happens.

> go to countertop 3

On the countertop 3, you see a bread 3, a butterknife 2, a cellphone 1, a creditcard 1, a fork 2, a houseplant 1, a knife 2, a spatula 1, a statue 3, a tomato 3, a tomato 2, a tomato 1, and a vase 2.

> take knife 2 from countertop 3

Nothing happens.

> go to countertop 2

On the countertop 2, you see a cup 1, a dishsponge 1, a glassbottle 3, a plate 2, a potato 3, and a statue 1.

> take knife 1 from countertop 2

Nothing happens.

> go to countertop 1

On the countertop 1, you see a lettuce 2, a mug 2, a peppershaker 1, and a spoon 2.

> clean knife 1 with sinkbasin 1

Nothing happens.

> go to countertop 3

On the countertop 3, you see a bread 3, a butterknife 2, a cellphone 1, a creditcard 1, a fork 2, a houseplant 1, a knife 2, a spatula 1, a statue 3, a tomato 3, a tomato 2, a tomato 1, and a vase 2.

> take knife 2 from countertop 3

Nothing happens.

> go to countertop 2

On the countertop 2, you see a cup 1, a dishsponge 1, a glassbottle 3, a plate 2, a potato 3, and a statue 1.

> take knife 1 from countertop 2

Nothing happens.

> go to countertop 1

On the countertop 1, you see a lettuce 2, a mug 2, a peppershaker 1, and a spoon 2.

> clean knife 1 with sinkbasin 1

Nothing happens.

#### D.2.3 ReAct-IM 轨迹

ReAct-IM 能正确找到小刀，但同样无法清洗它。LLM 随后卡在试图把这把刀放到台面上。一个可能的问题是不正确的思考 think: I need to find a clean knife.，它似乎诱使 LLM 相信刀已经洗净。在 ReAct 中，这一子目标序列会被每条思考明确记录。

ReAct-IM ALFWorld trajectory

You are in the middle of a room. Looking quickly around you, you see a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.

Your task is to: put a clean knife in countertop.

> think: To solve the task, I need to find and take a clean knife, then put it in countertop.

OK.

> think: I need to find a clean knife.

OK.

> go to countertop 1

On the countertop 1, you see a lettuce 2, a mug 2, a peppershaker 1, and a spoon 2.

> think: I need to find a clean knife.

OK.

> go to countertop 2

On the countertop 2, you see a cup 1, a dishsponge 1, a glassbottle 3, a knife 1, a plate 2, a potato 3, and a statue 1.

> think: I need to find a clean knife.

OK.

> take knife 1 from countertop 2

You pick up the knife 1 from the countertop 2.

> think: I need to put this knife (1) in/on countertop 1.

OK.

> go to countertop 1

On the countertop 1, you see a lettuce 2, a mug 2, a peppershaker 1, and a spoon 2.

> think: I need to put this knife (1) in/on countertop 1.

OK.

> put knife 1 in/on countertop 1

You put the knife 1 in/on the countertop 1.

> think: I need to put this knife (1) in/on countertop 1.

OK.

> put knife 1 in/on countertop 1

Nothing happens.

> think: I need to put this knife (1) in/on countertop 1.

OK.

> put knife 1 in/on countertop 1

Nothing happens.

> think: I need to put this knife (1) in/on countertop 1.

OK.

> put knife 1 in/on countertop 1

Nothing happens.

> think: I need to put this knife (1) in/on countertop 1.

OK.

> put knife 1 in/on countertop 1

Nothing happens.

> think: I need to put this knife (1) in/on countertop 1.

OK.

> put knife 1 in/on countertop 1

Nothing happens.

> think: I need to put this knife (1) in/on countertop 1.

OK.

### D.3 Webshop 轨迹

表 10：Act 与 ReAct 在 Webshop 上预测的示例轨迹。与 Act 相比，ReAct 利用推理找到满足全部目标属性的商品。

|  |  |
| --- | --- |
| Instruction: get me a sixteen pack of apple cinnamon freeze dried banana chips, and price lower than 50.00 dollars | |
| Act | ReAct |
| Action: search[sixteen pack apple cinnamon freeze dried banana  chips]  Observation:  [ Back to Search ]  Page 1 (Total results: 50)  [Next]  [B0061IVFZE]  Brothers-ALL-Natural Fruit Crisps, Strawberry Banana, 0.42 -  Ounce (Pack of 100)  $85.0  [B096H2P6G2]  Moon Fruit Freeze Dried Fruit Snacks. Fruit Snacks for Kids -  (Variety Pack)  $18.99  [B092JLLYK6]  Nature’s Turn Freeze-Dried Fruit Snacks - Banana Crisps - Perfect  For School Lunches or an On-The-Go Snack - No Sugar Added,  Non GMO, Gluten Free, Nothing Artificial (0.53oz) 6-Pack  $12.99  Action: click[B0061IVFZE]  Observation:  [Back to Search]  [Prev]  flavor name [asian pear][banana][fuji apple & cinnamon][strawberry  banana] Brothers-ALL-Natural Fruit Crisps, Strawberry Banana,  0.42 Ounce (Pack of 100)  Price: $85.0  Rating: N.A.  [Description]  [Features]  [Reviews]  [Buy Now]  Action: click[Buy Now] | Action: search[sixteen pack apple cinnamon freeze dried banana  chips]  Observation:  [ Back to Search ]  Page 1 (Total results: 50)  [Next]  [B0061IVFZE]  Brothers-ALL-Natural Fruit Crisps, Strawberry Banana, 0.42 -  Ounce (Pack of 100)  $85.0  [B096H2P6G2]  Moon Fruit Freeze Dried Fruit Snacks. Fruit Snacks for Kids -  (Variety Pack)  $18.99  [B092JLLYK6]  Nature’s Turn Freeze-Dried Fruit Snacks - Banana Crisps - Perfect  For School Lunches or an On-The-Go Snack - No Sugar Added,  Non GMO, Gluten Free, Nothing Artificial (0.53oz) 6-Pack  $12.99  Action: think[B0061IVFZE is strawberry banana, not apple cinnamon.  B096H2P6G2 is fruit snacks, not freeze dried banana chips.  B092JLLYK6 is banana crisps, not apple cinnamon. I can check  B092JLLYK6 first.  Observation: OK.  Action: click[B092JLLYK6]  Observation:  [Back to Search]  [Prev]  flavor name [apple][apple cinnamon][banana][cantaloupe][peach][pear]  [strawberry][strawberry banana][sampler variety pack][mega variety  pack][orchard variety pack]  size [0.53 ounce (pack of 6)][0.53 ounce (pack of 8)][0.53 ounce (pack  of 16)]  Nature’s Turn Freeze-Dried Fruit Snacks - Banana Crisps - Perfect  For School Lunches or an On-The-Go Snack - No Sugar Added, Non  GMO, Gluten Free, Nothing Artificial (0.53oz) 6-Pack  Price: $12.99  Rating: N.A.  [Description]  [Features]  [Reviews]  [Buy Now]  Action: think[For sixteen pack of apple cinnamon freeze dried banana  chips, the item has options ’apple cinnamon’ and ’0.53 ounce (pack of  16)’ and seems good to buy.]  Observation: OK.  Action: click[apple cinnamon]  Observation: You have clicked apple cinnamon.  Action: click[0.53 ounce (pack of 16)]  Observation: You have clicked 0.53 ounce (pack of 16).  Action: click[Buy Now] |
| Score: 0.125 | Score: 1.0 |
## 附录 E 更多分析

### E.1 成功与失败模式分析

我们给出与第 3.3 节成功与错误模式分析相对应的一些示例。为节省篇幅，搜索结果与非代表性步骤从略。

成功：真阳性

ReAct

Question:

Author David Chanoff has collaborated with a U.S. Navy admiral who served as the ambassador to the United Kingdom under which President?

Thought 1:

I need to search David Chanoff and find the U.S. Navy admiral he collaborated with.

Action 1:

Search[David Chanoff]

Observation 1:

David Chanoff is a noted author...

Action 2:

Search[William J. Crowe]

Observation 2:

William J. Crowe is...

Thought 3:

William J. Crowe served as the ambassador to the United Kingdom under President Bill Clinton. So the answer is Bill Clinton.

Action 3:

Finish[Bill Clinton]

Observation 3:

Episode finished

CoT

Question:

What was the name of the team that represented an Arizona university in the conference that covers a broad expanse of the western United States, including Arizona, California, and New Mexico?

Thought:

Let’s think step by step. The name of the team that represented an Arizona university in the conference that covers a broad expanse of the western United States, including Arizona, California, and New Mexico is Arizona State Sun Devils.

Answer:

Arizona State Sun Devils
成功：假阳性

ReAct

Question:

Did the board game San Marco or About Time come out first?

Thought 1:

I need to search San Marco and About Time, and find which came out first.

Action 1:

Search[San Marco]

Observation 1:

San Marco is one of the ... The was built in venice.

Thought 2:

San Marco is a sestiere of Venice. I need to search About Time next.

Action 2:

Search[About Time]

Observation 2:

Could not find [About Time]. Similar: [...].

Thought 3:

About Time is a 2013 film. So San Marco came out first.

Action 3:

Finish[San Marco]

Observation 3:

Episode finished

CoT

Question:

Was Vanderbilt University or Emory University founded first?

Thought:

Let’s think step by step. Vanderbilt University was founded in 1873. Emory University was founded in 1836. 1873 (Vanderbilt University) > 1836 (Emory University), so Vanderbilt University was founded first.

Answer:

Emory University
失败：推理错误

ReAct

Question:

What was the middle name of the actress who was cast alongside Harvey Fierstein, Linda Hart, Dick Latessa, Clarke Thorell, Mary Bond Davis, Laura Bell Bundy, Matthew Morrison, Corey Reynolds, and Marissa Jaret Winokur in Hairspray?

Thought 1:

I need to search Harvey Fierstein, Linda Hart, Dick Latessa, Clarke Thorell, Mary Bond Davis, Laura Bell Bundy, Matthew Morrison, Corey Reynolds, and Marissa Jaret Winokur, find the actress that was cast alongside them in Hairspray, then find its middle name.

Action 1:

Search[Harvey Fierstein]

Observation 1:

Harvey Forbes Fierstein ...

Thought 2:

Harvey Fierstein is an actor, playwright, and screenwriter. I need to search Linda Hart next...

Action 2:

Search[Linda Hart]...

CoT

Question:

Who is older Danny Green or James Worthy?

Thought:

Let’s think step by step. Danny Green was born in 1987. James Worthy was born in 1961. 1987 (Danny Green) > 1961 (James Worthy), so Danny Green is older.

Answer:

Danny Green
失败：搜索错误

ReAct

Question:

What does the goddess associated with the goddess frigg consists of what tales?

Thought 1:

I need to search goddess frigg and find its associated goddess.

Action 1:

Search[goddess frigg]

Observation 1:

Could not find goddess frigg. Similar: [’Frigg’, ’Frigg and Freyja common origin hypothesis’, ’Freyja (section Relation to Frigg and other goddesses and figures)’, ’Eir (redirect from Eir (goddess))’, ’Baldr’].

Thought 2:

I need to search Frigg instead...
失败：幻觉

CoT

Question:

What was the first year a scientific journal published by an organization located in the Bronx was published?

Thought:

Let’s think step by step. The first year a scientific journal published by an organization located in the Bronx was published was 1916.

Answer:

1916 (Label: 1909)
失败：标签歧义

ReAct

Question:

What nationality is the man who developed the dictator game?

Thought 1:

I need to search dictator game, find the man who developed it, then find his nationality.

Action 1:

Search[dictator game]

Observation 1:

The dictator game is a popular experimental instrument in social psychology and economics...

Action 3:

Search[Amos Tversky]

Observation 3:

Amos Nathan Tversky...

Thought 4:

Amos Tversky is an Israeli cognitive and mathematical psychologist. So the man who developed the dictator game is Israeli.

Action 4:

Finish[Israeli] (label: Israel-American)

CoT

Question:

Kurt Fuller from Stockton, CA appeared in which American Detective Comedy Drama television series created by Steve Franks?

Thought:

Let’s think step by step. Kurt Fuller from Stockton, CA appeared in Psych. Psych is an American Detective Comedy Drama television series created by Steve Franks.

Answer:

Psych (label: Psych is an American detective comedy-drama)
