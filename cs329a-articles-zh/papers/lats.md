---
title: "LATS：语言智能体树搜索统一语言模型中的推理、行动与规划"
title_en: "Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models"
arxiv: 2310.04406
source: https://arxiv.org/abs/2310.04406
crawled: 2026-09-23
translated: 2026-09-23
---

# LATS：语言智能体树搜索统一语言模型中的推理、行动与规划


> 原文：[Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models](https://arxiv.org/abs/2310.04406) · Stanford CS329A 指定阅读

Andy Zhou（伊利诺伊大学厄巴纳-香槟分校；Lapis Labs；通讯作者：andyz3@illinois.edu）
Kai Yan、Michal Shlapentokh-Rothman、Haohan Wang、Yu-Xiong Wang（伊利诺伊大学厄巴纳-香槟分校）

###### 摘要

尽管语言模型（LM）已在一系列决策任务中展现出潜力，但它们对简单行动过程的依赖限制了其作为自主智能体的广泛部署。本文提出语言智能体树搜索（Language Agent Tree Search，LATS）——*首个*协同 LM 推理、行动与规划能力的*通用*框架。借助 LM 的上下文学习能力，我们把蒙特卡洛树搜索融入 LATS，使 LM 得以充当智能体，并配合 LM 驱动的价值函数与自我反思，实现娴熟的探索与更强的决策。我们方法的一个关键特点是引入外部反馈环境，提供一种比既有技术约束更审慎、更自适应的问题求解机制。我们在编程、交互式问答（QA）、网页导航与数学等多个领域的实验评估，验证了 LATS 在决策上的有效性与通用性，同时保持有竞争力或更优的推理表现。值得注意的是，LATS 在 HumanEval 上配合 GPT-4 取得 92.7% 的最先进 pass@1 编程准确率，并在 WebShop 上配合 GPT-3.5 取得 75.9 的平均分——一种与基于梯度的微调相当的无梯度表现。代码见 <https://github.com/lapisrocks/LanguageAgentTreeSearch>。

###### 关键词：

机器学习、大型语言模型、LM 智能体、LM 规划

## 1 引言

能够在多种环境中推理与决策的通用自主智能体（Wooldridge and Jennings, 1995）长期以来都是人工智能领域的兴趣所在。虽然这一课题传统上在强化学习中研究，但近期语言模型（LM）（Brown et al., 2020；Chowdhery et al., 2023；Touvron et al., 2023；OpenAI, 2023）的崛起——及其强大的推理与普适适应性——提供了另一种范式。LM 不仅在摘要（Nallapati et al., 2016）、语言推理（Bowman et al., 2015）等标准自然语言处理（NLP）任务上表现出色，还被适配到日益多样的任务上，这些任务往往需要高级常识推理或量化技能（Cobbe et al., 2021；Saparov and He, 2023）。此外，LM 能在涉及知识与推理的复杂环境中执行任务，例如网页导航（Yao et al., 2022；Deng et al., 2023）、工具使用（Schick et al., 2023）与开放式游戏（Fan et al., 2022）。

![Refer to caption](2310.04406v3/lats_teaser.png)

图 1：LATS 概览。作为一个统一框架，LATS 利用外部环境与基于 MCTS 的搜索算法来改进推理与决策。

通过用来自外部环境的反馈或观察增强 LM 的提示技术，推理与行动能力得到进一步提升，ReAct（Yao et al., 2023b）及其他工作（Gao et al., 2023；Shinn et al., 2023）即为代表。这免去了完全依赖 LM 基础能力的需要，借助外部工具或语义反馈予以增强。尽管有这些优势，这些方法是反射式的，达不到人类解决问题时审慎而深思的决策特性（Sloman, 1996；Evans, 2010）。特别地，它们没有考虑多条推理路径，也不会前瞻规划。近期以搜索引导 LM 的工作（Xie et al., 2023；Yao et al., 2023a；Hao et al., 2023）通过搜索多条推理链解决这一问题。这类方法虽然具备规划能力，却孤立运行，缺少能改进推理的外部反馈的融入。

为克服这些挑战，我们提出语言智能体树搜索（LATS）——一个用语言模型做决策与推理的*统一*框架。如图 1 所示，LATS 把 ReAct（Yao et al., 2023b）扩展为对「可能的推理与行动步骤组合空间」的搜索，从而*协同 LM 的推理、行动与规划*策略。这项工作并非易事——把搜索算法适配到语言智能体、从非交互任务转向交互任务，需要在节点、提示与搜索算法上做大量新颖设计。特别地，节点与提示必须有效存储并检索外部反馈，搜索算法要把这些信息纳入有用的价值赋值启发式。事实上，我们在第 5.1 节以 HotPotQA（Yang et al., 2018）展示的实证评估揭示：简单组合现有方法并不够用，即便能从环境获取真实答案，也未能超过内部推理的表现。

支撑 LATS 的*关键洞察*是改造蒙特卡洛树搜索（MCTS）——灵感来自其在基于模型的强化学习中的成功（Silver et al., 2017），以及「许多 LM 任务允许回退到较早步骤」这一观察——将其应用于语言智能体，把预训练 LM 重新用作智能体，配以 LM 驱动的价值函数与自我反思，实现更聪明的探索。借助现代 LM 的通用能力与上下文学习，我们用语言作为各组件之间的接口，使 LATS 能*无需额外训练*就把规划适配到环境状况。据我们所知，LATS 是*首个*融合推理、行动与规划以增强 LM 表现的框架。值得注意的是，LATS 在 HotPotQA（Yang et al., 2018）上把 ReAct（Yao et al., 2023b）的性能翻倍，并在 WebShop（Yao et al., 2022）上配合 GPT-3.5 把平均分提高 22.1。配合 GPT-4 使用时，LATS 在 HumanEval（Chen et al., 2021）上取得 92.7 的 pass@1，创当时最先进水平。

我们的贡献如下：1) 我们提出 LATS，一个基于蒙特卡洛树搜索的框架，从采样行动中构造最佳轨迹，相比反射式提示方法实现更灵活、更自适应的问题求解。2) 我们提出一个新颖的价值函数来引导搜索过程，并纳入自我优化（self-refinement）与自洽性等成功启发式。3) 通过整合外部反馈与自我反思，LATS 增强了模型的判断力，使智能体能从经验中学习，超越基于推理的搜索方法。通过在编程、交互式问答（QA）、网页导航与数学等多个领域的实验，我们展示了 LATS 在增强自主推理与决策上的通用性。

## 2 相关工作

| 方法 | 推理 | 行动 | 规划 | 自我反思 | 外部记忆 |
| --- | --- | --- | --- | --- | --- |
| CoT（Wei et al., 2022） | ✓ | × | × | × | × |
| ReAct（Yao et al., 2023b） | ✓ | ✓ | × | × | × |
| ToT（Yao et al., 2023a） | ✓ | × | ✓ | ✓ | ✓ |
| RAP（Hao et al., 2023） | ✓ | × | ✓ | × | ✓ |
| Self-Refine（Madaan et al., 2023） | ✓ | × | × | ✓ | × |
| Beam Search（Xie et al., 2023） | ✓ | × | × | ✓ | × |
| Reflexion（Shinn et al., 2023） | ✓ | ✓ | × | ✓ | ✓ |
| LATS（本文） | ✓ | ✓ | ✓ | ✓ | ✓ |

表 1：推理、行动与规划相关工作总结。LATS 是*首个*融合*全部三个*领域设计的工作，在所有相应任务中具有广泛适用性。我们把推理界定为 LM 内部推理，行动界定为外部决策，规划界定为使用搜索算法，自我反思界定为使用 LM 生成的反馈，外部记忆界定为存储过往文本上下文以供后续更新解。

面向推理的 LM。对 LM 而言，推理涉及把复杂输入分解为通向最终答案的序列化中间步骤（Cobbe et al., 2021），思维链（CoT）提示（Wei et al., 2022）及其变体（Wei et al., 2022；Kojima et al., 2022；Wang et al., 2022）即是示范。然而，这些在单步内自回归地构造链的方法，随着步数增加，常因复合误差而受错误传播之苦（Guo et al., 2018；Chen et al., 2023b）。各种进展试图缓解该问题：一些方法如自洽性（Wang et al., 2022）对采样的链做多数投票，另一些聚焦多步分解，如最少到最多提示（Zhou et al., 2022）。近期，CoT 又被搜索算法（Yao et al., 2023a；Hao et al., 2023；Besta et al., 2023）改进，后者能更有效地采样轨迹。思维树（ToT）提示（Yao et al., 2023a）用由 LM 生成启发式引导的 DFS 或 BFS（深/广度优先）搜索，而经由规划的推理（RAP）（Hao et al., 2023）用带 LM 模拟 rollout 的 MCTS。但它们只依赖 LM 内部知识，无法适配有用的外部反馈。

面向行动的 LM。LM 强大的推理与常识能力进一步被适配为交互环境中作为策略模型的决策或行动任务。在机器人学中，LM 被用作控制策略的高层控制器（Ahn et al., 2022；Huang et al., 2022；Driess et al., 2023）。类似工作（Baker et al., 2022；Wang et al., 2023）也把 LM 智能体适配到 Minecraft（Guss et al., 2019；Fan et al., 2022）等复杂多模态游戏。LM 在基于文本的环境中尤其有用（Liu et al., 2018；Shridhar et al., 2020；Liu et al., 2024），ReAct（Yao et al., 2023b）等基于行动的提示技术在此取得成功。与 CoT 类似，ReAct 受限于其简单性，无法有效适配环境状况。为解决该问题已有许多扩展，包括用自我改进增强推理与决策的 self-refine（Madaan et al., 2023）与 Reflexion（Shinn et al., 2023），以及同时纳入正负反馈的 AdaPlanner（Sun et al., 2023）。然而这些方法聚焦打磨单条轨迹，未考虑每步的备选选择。此外，近期工作（Huang et al., 2024）指出 LM 无法自我纠正其内部推理，这使得使用外部反馈至关重要。另外，除纯决策环境外，LM 的推理与实用能力也通过提供外部工具（如 API、搜索引擎、计算器与其他模型）得到增强（Schick et al., 2023；Shen et al., 2023；Surís et al., 2023）。我们在表 1 中总结先前工作。

基于树的搜索。基于树的搜索在搜索过程中探索多条结果分支，因其良好的探索-利用权衡而被广泛用于许多规划算法（Swiechowski et al., 2021；LaValle, 1998）与强化学习（RL）算法（Hafner et al., 2019；Du et al., 2023；Wu et al., 2023）。注意，虽然基于树的搜索需要一个能从任意状态展开的环境模型（Vodopivec et al., 2017），在 RL 中往往需要额外训练（Hafner et al., 2023），但对多数 LM 任务而言这一问题*并不*存在：对许多任务，我们只需把输入设为上下文与 LM 相应的历史输出，即可方便地回退到任意状态。因此，我们基于树的框架运作，并用 MCTS（Swiechowski et al., 2021）充分释放 LM 的潜力。此外，我们借助 LM 的上下文学习能力（Brown et al., 2020），避免了在语言描述上训练价值函数的开销。同期工作（Liu et al., 2023）也探索把搜索算法与 LM 智能体结合，但用的是现成搜索算法，未必对 LM 最优。最后，沿用 Yao et al. (2023a) 与 Hao et al. (2023) 的做法，我们在本文中交替使用「规划」与「搜索算法」。

## 3 预备知识

### 3.1 问题设定与提示

我们先定义问题，并概述几种利用语言模型做推理*或*决策的既有方法。在 LM 推理或决策中，给定自然语言输入 $x$ 与由 $\theta$ 参数化的预训练语言模型 $p_{\theta}(x)$；目标是生成对应答案（推理）或完成任务（决策）的最终输出 $y\sim p_{\theta}(x)$。$x$ 与 $y$ 都是语言序列，由一列 token（自然语言的基本元素，常为词）组成，记为 $x=(x[1],\dots,x[l_{x}])$ 与 $y=(y[1],\dots,y[l_{y}])$，其中 $l_x$、$l_y$ 为长度。LM 自回归地解码文本，即在没有其他输入时，LM 生成序列 $y$ 的概率为 $p_{\theta}(x)=\prod_{i=1}^{l_{x}}p_{\theta}(x[i]|x[1\dots i-1])$。通常，为改进推理，会随输入 $x$ 提供提示（prompt），即具体指令或少样本输入-输出示例。我们把输入提示 $\texttt{prompt}_{\mathrm{IO}}(x)$ 经 LM 变换为输出 $y$ 的通用过程记为 $y\sim p_{\theta}(\texttt{prompt}_{\mathrm{IO}}(x))$。

思维链（CoT）提示（Wei et al., 2022）面向 $x$ 到 $y$ 的直接映射错综复杂的场景，例如 $x$ 来自数学查询或困难问题。它依赖在 $x$ 与 $y$ 之间充当垫脚石的思考 $z_{1},\dots,z_{l}$；每个思考 $z_{i}$ 是一个语言序列。使用 CoT 提示时，思考按顺序抽取：$z_{i}\sim p_{\theta}^{\mathrm{CoT}}(x,z_{1\cdots i-1})$，最终输出为 $y\sim p_{\theta}^{\mathrm{CoT}}(x,z_{1\cdots l})$。

思维树（ToT）提示（Yao et al., 2023a）通过在思考上探索多条推理路径扩展 CoT。它把问题框定为树上的搜索，每个节点 $s=[x,z_{1\cdot i}]$ 表示由原始输入 $x$ 与思考序列 $z_{1\cdots i}$ 构成的部分解状态。思考 $z_{i}$ 通过 CoT 提议或采样生成：$z_{i}\sim p_{\theta}^{\mathrm{CoT}}(x,z_{1\cdots i-1})$。用深度优先（DFS）或广度优先（BFS）等搜索算法系统地探索这棵树，由基于 LM 对每个状态评估 $V(s)$ 的启发式引导。

ReAct（Yao et al., 2023b）把语言模型扩展到 $x$ 到 $y$ 的映射被与外部环境（如游戏或 API）的交互增强或必需的任务。该技术构造行动空间 $\hat{A}=A\cup Z$，在 CoT 的推理轨迹 $z\in Z$ 之上加入允许的行动 $a\in A$。来自环境的观察 $o$ 用于同时改进推理与行动。用 ReAct 解题时，每次观察后，行动由 $p_{\theta}$ 顺序生成：$a_{i}\sim p_{\theta}^{\mathrm{ReAct}}(x,o_{1\cdots i-1},a_{1\cdots i-1})$，最终输出为 $y\sim p_{\theta}^{\mathrm{ReAct}}(x,o_{1\cdots l},a_{1\cdots l})$。本文与 ReAct、Reflexion（Shinn et al., 2023）等其他 LM 智能体方法一致，聚焦*迭代间可回退*的决策任务。

上述提示技术虽然改进了 LM 在推理任务上的表现，但由于若干不足，在涉及多面决策的困难任务上折戟：1) 灵活性：基础提示设计（CoT 或 ReAct）自回归地从 LM 采样，忽略了特定状态下可能的替代延续。2) 判断力：基于推理的方法（CoT、RAP（Hao et al., 2023）或 ToT）只依赖 LM 的内部表示，无法考虑外部观察。这种依赖有事实幻觉与错误传播之虞，并设定了性能上限。3) 适应性：现行规划策略（RAP 或 ToT）使用 BFS 等简单搜索算法，或无法利用环境反馈改进规划。此外，智能体是静态的，不能复用先前经验或从试错中学习。RAP 虽也采用 MCTS，但受限于 LM 能充当世界模型并准确预测状态的任务。这些不足限制了 LM 作为通用问题求解智能体的部署，也构成了 LATS 的动机。

### 3.2 蒙特卡洛树搜索（MCTS）

蒙特卡洛树搜索（MCTS）是一种启发式搜索算法，已在许多决策环境中证明成功，如 Atari（Ye et al., 2021）与围棋（Silver et al., 2016）。MCTS 构建一棵决策树，树中每个节点是一个状态、每条边是一个行动。MCTS 运行 $k$ 个回合；每个回合从根（即初始状态）出发，迭代执行两步来扩展树：1) 展开（Expansion）：从当前父状态 $p$ 采样 $n$ 个行动，探索多个子状态 $s$；2) 选择（Selection）：选出 UCT（应用于树的上置信界）（Kocsis and Szepesvári, 2006）值最高的子状态供下一轮迭代展开。子状态 $s$ 的 UCT 计算如下：

$$UCT(s)=V(s)+w\sqrt{\frac{\ln N(p)}{N(s)}},\tag{1}$$

其中 $N(s)$ 是节点 $s$ 的访问次数，$V(s)$ 是从 $s$ 的子树出发的价值函数（期望回报），$w$ 是探索权重，$p$ 是 $s$ 的父节点。当回合结束时执行回传（backpropagation）：用回报 $r$ 按公式 $V(s)=\frac{V_{\text{old}}(s)(N(s)-1)+r}{N(s)}$ 更新路径上的每个 $V(s)$，其中 $V_{\text{old}}(s)$ 是旧价值函数。通常，MCTS 的主要缺点是需要一个能撤销先前步骤并构造搜索树的环境模型，这可能是很强的假设。但对许多 LM 任务来说这一限制*并不*存在，因为我们可以通过简单地复制粘贴历史文本输入来重置到任意步骤。这一特殊性质正是本工作的关键动机。

## 4 统一推理、行动与规划

### 4.1 LM 智能体

依据基础提示框架设计，LATS 支持序列化推理或决策任务。在时间步 $t$，智能体从环境接收观察 $o_{t}\in O$，并依某种策略 $\pi(a_{t}|x,o_{1\cdots t-1},a_{1\cdots t-1})$ 采取行动 $a_{t}\in A$。我们用 $p_{\theta}$ 初始化智能体，以利用 LM 的有用语言表示作为基础决策者。我们沿用 ReAct 的实例化：行动空间 $\hat{A}=A\cup Z$ 由允许行动的空间 $A$ 与推理轨迹的语言空间 $Z$ 共同组成。行动直接影响环境并产生观察，而思考用于通过组织信息、规划未来行动或注入内部知识来使决策形式化。行动空间的具体实例化取决于特定环境——对决策任务，行动可能由网站上的命令组成；对推理任务，行动空间可能限于少数外部工具或 API。在无反馈的环境（如推理任务）中，我们用 CoT 作为基础提示框架。

我们不是贪心解码一条轨迹或一个解，而是从 $p_{\theta}$ 用当前状态采样 $n$ 个行动。这基于如下直觉：对复杂决策任务，很可能存在一整族正确的潜在轨迹或推理路径（Evans, 2010）。每步采样多样的候选集，缓解了 LM 文本生成的随机性，并在决策与推理空间中获得更大的探索。我们把 $p_{\theta}$ 包装进我们提出的搜索算法，审慎地从采样行动中构造最佳轨迹。

### 4.2 LATS

图 2：LATS 六个操作概览。一个节点被选择、展开、评估，然后模拟直至到达终止节点，再把所得价值回传。若轨迹失败，则生成一次反思并作为后续尝试的额外上下文。这些操作依次进行，直到达到预算或任务成功。

LATS 的主组件是一个用规划控制问题求解过程的搜索算法。为找到最有希望的轨迹并系统地在探索与利用之间取得平衡，我们采用 MCTS 的一个变体，把决策框定为树搜索，其中每个节点 $s=[x,a_{1\cdots i},o_{1\cdots i}]$ 表示由原始输入 $x$、行动序列 $a_{1\cdot i}$ 与观察序列 $o_{1\cdot i}$ 组成的状态，其中 $i$ 是文本序列中的指示。

我们的主要技术贡献是把 MCTS 适配到语言智能体。LATS 把 $p_{\theta}$ 重新用作智能体、状态评估器与反馈生成器，利用现代 LM 的有用语言表示来促进规划。标准 MCTS 与 RAP（Hao et al., 2023）依赖内部动力学模型来辅助模拟，而 LATS 使用环境交互、不需要世界模型。如图 2 所示，LATS 由一系列操作组成——选择、展开、评估、模拟、回传与反思——依次执行，直到在采样 $k$ 条轨迹后任务成功完成或达到计算上限。LATS 的完整伪代码见附录 A 节。

选择（Selection）。第一个操作中，算法识别当前树中最适合后续展开的片段。从根节点（记为初始状态 $s_0$）出发，在树的每一层选出一个子节点，直到到达叶节点。为平衡探索与利用，我们用式 1 所示的 UCT 算法。

展开（Expansion）。选定节点后，第二个操作从 $p_{\theta}$ 采样 $n$ 个行动来扩展树，如前一节所述。环境接收每个行动并返回相应反馈作为观察。这会向树中添加 $n$ 个新子节点。这棵树存储在外部长期记忆结构中。

评估（Evaluation）。第三个操作为每个新子节点赋一个标量价值，用于选择与回传。该价值有效量化智能体的任务完成进度，作为引导搜索算法走向树中最有希望区域的启发式。由于 LATS 不涉及训练，我们为该设定提出一个由两部分组成的新颖价值函数：（1）*自生成*的 LM 打分；（2）*自洽性*分数。

受 ToT 启发，我们把 $p_{\theta}$ 改造为价值函数：提示其对给定状态进行推理。为得到标量值，我们指示 $p_{\theta}$ 在推理轨迹末尾给出一个表示轨迹正确性的分数。我们与 ToT 的关键区别是：我们在获得环境反馈之后再取该值，从而改进价值赋值。这也使其能扩展到更具挑战性的环境，因为 LM 在没有外部反馈时很难改进其回复（Huang et al., 2024）。此外，为进一步改进价值赋值，我们引入一个基于自洽性（Wang et al., 2022）的附加启发式：在同一状态被多次采样到的行动往往更准确。于是得到总价值函数：

$$V(s)=\lambda*\text{LM}(s)+(1-\lambda)*\text{SC}(s),\tag{2}$$

其中 $\lambda$ 是超参数。值得注意的是，我们的方法相对程序化启发式（Campbell et al., 2002）更灵活，相对学习得到的启发式（Silver et al., 2017）更高效。

模拟（Simulation）。第四个操作把当前选中的节点继续展开直至终止状态。在每个深度层，我们以相同操作采样并评估节点，但优先取价值最高者。到达终止状态可对轨迹正确性提供客观反馈。若任务成功完成，LATS 终止搜索。若解部分成功或失败，则执行下述两个附加操作。轨迹是否成功由具体环境的设计决定，例如网页导航环境中完成购买。

回传（Backpropagation）。该操作依据轨迹的结果更新树的取值。对搜索树中从根（初始状态 $s_0$）到叶（终止状态 $s_l$）的轨迹上的每个节点 $s_{0},s_{1},\dots,s_{l}$，其价值被更新以反映模拟结果：$N(s_{i})=N(s_{i-1})+1$ 且 $V(s_{i})=\frac{V(s_{i-1})N(s_{i-1})+r}{N(s_{i})}$，其中 $r$ 是奖励。更新后的值用于 UCT 公式（式 1）以指导下一个节点的选择。

反思（Reflection）。除环境反馈外，我们利用自我反思来进一步打磨决策过程（Shinn et al., 2023；Madaan et al., 2023）。遇到不成功的终止节点时，我们用轨迹与最终奖励提示 $p_{\theta}$ 给出言语自我反思，总结推理或行动过程中的错误并提出更优的替代方案。我们把失败轨迹与相应反思一并存入记忆。在后续迭代中，它们作为额外上下文整合进智能体与价值函数，通过上下文学习同时精化二者。这提供了一种比标量值更有用的语义梯度信号，使智能体无需强化学习等昂贵优化的成本即可从试错中学习。

讨论。概念上，作为 LM 智能体推理与决策的通用框架，LATS 有若干显著优点。（1）通用性：LATS 通过定义思考与行动的共享空间，同时支持推理与决策任务。（2）审慎性：LATS 中 MCTS 与 LM 价值函数的结合确保一种有原则的搜索——既选择高价值选项又探索有希望的替代。（3）适应性：LATS 通过观察与自我反思纳入外部反馈，在问题求解中实现更强的适应。（4）灵活性：LATS 可通过修改状态设计与树的维度适配不同场景、环境与资源约束。（5）模块化：基础 LM 智能体、反思生成器与价值函数可以独立更换并适配各自的 LM 特性。

| 提示方法 | HotpotQA (EM) ↑ |
| --- | --- |
| 基础 LM | 0.32 |
| CoT（Wei et al., 2022） | 0.34 |
| CoT-SC（Wang et al., 2022） | 0.38 |
| ToT（Yao et al., 2023a） | 0.55 |
| RAP（Hao et al., 2023） | 0.60 |
| RAP（n=10） | 0.60 |
| LATS（CoT） | 0.62 |

表 2：GPT-3.5 在 HotpotQA 上基于*推理*的提示结果。LATS 取得推理任务上最高的精确匹配（EM）。我们在展开时采样 $n=5$ 个节点、$k=50$ 条轨迹。

## 5 实验

为展示 LATS 的广泛适用性，我们在需要推理与行动的多个领域评估我们的方法：编程（Chen et al., 2021；Austin et al., 2022）、HotPotQA（Yang et al., 2018）、WebShop（Yao et al., 2022）与 24 点游戏（Yao et al., 2023a）。

### 5.1 HotPotQA

| 提示方法 | HotpotQA (EM) ↑ |
| --- | --- |
| ReAct（Yao et al., 2023b） | 0.32 |
| ReAct（k 中最佳） | 0.38 |
| Reflexion（Shinn et al., 2023） | 0.51 |
| ToT（ReAct） | 0.39 |
| RAP（ReAct） | 0.54 |
| LATS（ReAct） | 0.63 |
| LATS（n=3） | 0.58 |
| LATS（n=10） | 0.65 |
| LATS（CoT + ReAct） | 0.71 |

表 3：GPT-3.5 在 HotpotQA 上基于*行动*的提示结果。LATS 取得行动任务上最高的精确匹配（EM）。我们采样 $n=5$ 个节点、使用 $k=50$ 条轨迹。我们还评估了采样 ReAct $k$ 次、以及 LATS 同时使用 CoT 与 ReAct 基础提示设计（后者取得最佳表现）。注意 LATS 优于使用 ReAct 提示的 ToT 与 RAP——它们只是把搜索算法对决策任务的简单改编。

对一个既可用基于推理又可用基于行动策略求解的任务，我们考虑 HotPotQA（Yang et al., 2018）——一个需要检索两篇或更多 Wikipedia 段落的多跳问答基准。对行动空间，除 LM 思考外，我们沿用 Yao et al. (2023b) 的设定：为智能体提供搜索与检索信息的 API 调用。这些 API 调用的输出与自生成的反思构成观察空间。注意，与先前工作（Yao et al., 2023b；Shinn et al., 2023）一致，我们对 HotPotQA 使用 oracle 设定：环境在收到答案后就其正确性给出反馈。这使得我们的方法与基线在反馈质量高的场景下可以公平比较，让我们把评估聚焦在智能体吸收外部反馈的好坏上。我们使用 100 个问题的子集，每种方法用 3 个少样本示例。对 ToT，我们用 DFS 作为基础搜索算法。对所有涉及采样的方法（包括 LATS），我们采样 $k=50$ 条轨迹。更多细节见附录 D 节。

我们通过从上下文中移除行动与观察来评估内部推理策略，对应 CoT（Wei et al., 2022）及其变体 CoT-SC（Wang et al., 2022）、ToT（Yao et al., 2023a）与 RAP（Hao et al., 2023）。这些方法只依赖智能体的既有知识答题。我们进一步考虑基于行动的方法 ReAct、Reflexion 与 LATS——它们为智能体配备交互式 API 环境，主要评估其信息检索能力。我们还设计了搜索算法与 LM 智能体的简单整合：把 ToT 与 RAP 扩展为带 ReAct 提示以处理外部观察。此外，虽然 LATS 为「外部反馈可增强推理」的场景设计，我们也实现了一个以 CoT 为基础提示框架的纯推理版本。更进一步，我们在 LATS 中结合内部与外部推理：先用基于 CoT 的提示，失败后切换到基于 ReAct 的提示。这更接近人类处理该任务的方式——只在答案未知时才用工具检索额外信息。

结果。我们在表 2 与表 3 中观察到，内部推理与外部检索策略在 HotPotQA 上都表现良好。得益于大规模训练语料，现代 LM 已编码了事实知识，往往能直接答对问题。CoT 虽能小幅改进需要推理的问题，但更大的增益来自 ToT 与 RAP 等搜索方法（表 2 第 4、5 行）——它们能采样并探索更多输出。基于行动的方法结果类似。LATS 超越 ReAct，即便采样相同数量的轨迹，也凭借有原则的搜索展开更多节点。这在调整 $n$（每次迭代展开的节点数）时得到体现：增大 $n$ 能持续改进性能，尽管计算与推理成本更高。LATS 在内部推理上也优于 RAP，但其在 HotPotQA 决策设定上的表现高于推理设定。与 LATS 相反，ToT 与 RAP 的 ReAct 版本（表 3 第 4、5 行）甚至比 HotPotQA 的纯推理设定更差，说明基于行动的设定更困难，*把搜索算法适配到决策场景并非易事*。在 LATS 中结合内部与外部推理取得最高性能，说明即便在基座 LM 已能胜任的任务上，外部反馈对增强推理依然重要。

### 5.2 编程

| 提示方法 | 模型 | Pass@1 ↑ |
| --- | --- | --- |
| CoT（Wei et al., 2022） | GPT-3.5 | 46.9 |
| ReAct（Yao et al., 2023b） | GPT-3.5 | 56.9 |
| Reflexion（Shinn et al., 2023） | GPT-3.5 | 68.1 |
| ToT（Yao et al., 2023a） | GPT-3.5 | 54.4 |
| RAP（Hao et al., 2023） | GPT-3.5 | 63.1 |
| LATS（ReAct） | GPT-3.5 | 83.8 |
| 基础 LM | GPT-4 | 80.1 |
| Reflexion | GPT-4 | 91.0 |
| LATS（ReAct） | GPT-4 | 92.7 |

表 4：GPT-3.5 与 GPT-4 在 HumanEval 上的 pass@1 准确率。用 LATS 提示取得最佳表现。我们在展开时采样 5 个解，迭代 8 轮。

为展示外部观察对复杂推理任务的重要性，我们在编程任务上用 HumanEval（Chen et al., 2021）¹与 MBPP（Austin et al., 2022）评估基线与 LATS。两个数据集都衡量从自然语言 docstring 合成 Python 程序的正确性。我们把逐个的解作为行动空间，把测试套件与编译器反馈作为外部观察。我们沿用 Chen et al. (2023a)，用一个 LM 为每道题生成由语法合法的「assert」语句组成的合成测试套件。每一步，解在该测试套件上评估，结果（含通过/失败的测试与编译器输出）作为观察加入上下文。

注 1：部分基线使用 HumanEval 的 161 道题。我们对 LATS 使用全部 164 道题，发现性能差异极小，因此我们报告两种设定下的基线。

对该任务，推理与行动基线共享同一行动空间，但行动方法能把观察纳入额外上下文。对 LATS 而言，由于每个行动对应一个完整解，我们跳过 LATS 的模拟步骤，直接用通过测试的百分比作为回传奖励。我们用 $k=8$ 轮迭代，生成测试数设为 4，展开时采样 $n=5$ 个解。搜索完成后，我们选择价值最高的解，并在真实测试套件上评估以计算 pass@1 准确率。更多细节见附录 D 节。

结果。表 4 与表 5 表明，搜索与语义反馈对更优表现都至关重要。尽管不使用观察，ToT 与 RAP 与 Reflexion 相当。LATS 在两个数据集上均取得最高表现。RAP 使用与 LATS 相似的搜索算法，这揭示了外部反馈对编程等困难推理任务的重要性。配合 GPT-4，使用 LATS 在 HumanEval 上创造最先进水平，验证了 LATS 可以配合更先进的 LM 取得更高性能。

| 提示方法 | Pass@1 ↑ |
| --- | --- |
| CoT（Wei et al., 2022） | 54.9 |
| ReAct（Wei et al., 2022） | 67.0 |
| Reflexion（Shinn et al., 2023） | 70.0 |
| ToT（Yao et al., 2023a） | 65.8 |
| RAP（Hao et al., 2023） | 71.4 |
| LATS（ReAct） | 81.1 |

表 5：GPT-3.5 在 MBPP 上的 pass@1 准确率。用 LATS 提示取得最高表现。我们在展开时采样 5 个解，迭代 8 轮。

### 5.3 WebShop

对一个有实际应用的复杂决策环境，我们考虑 WebShop（Yao et al., 2022）——一个由含 118 万件真实商品与 1.2 万条人类指令的网站构成的在线购物环境。智能体必须通过多种命令浏览网站以购买符合用户规格的商品。我们使用预构建的搜索与点击命令行动空间，观察则由浏览器反馈与反思组成。性能用两个指标衡量：平均分（所选商品满足用户指定属性的百分比）与成功率（所选商品满足全部给定条件的频率）。我们与基于行动的提示方法及基于 RL 的方法比较。我们在 50 条指令上评估，LATS 展开 $n=5$ 个子节点，并对 LATS、ReAct（k 中最佳）与 Reflexion 设 $k=30$。更多细节与提示见附录 D 节与 G 节。

结果。我们在表 6 中发现，配 ReAct 的 GPT-3.5 与模仿学习（IL）相当，并能凭更强的提示策略超越强化学习技术。用 ReAct 与 Reflexion 采样 $k=30$ 条轨迹得到相近的表现，说明语义反馈在 WebShop 这样的复杂环境中没那么有用。与 Shinn et al. (2023) 类似，我们发现生成的反思往往泛泛而谈、不能提供有用反馈，导致智能体容易陷入局部极小。然而，使用 LATS 确实带来显著改进，表明在相同迭代次数下探索更有效。

| 方法 | 得分 ↑ | SR ↑ |
| --- | --- | --- |
| ReAct（Yao et al., 2023b） | 53.8 | 28.0 |
| ReAct（k 中最佳） | 59.1 | 32.0 |
| Reflexion（Shinn et al., 2023） | 64.2 | 35.0 |
| LATS（ReAct） | 75.9 | 38.0 |
| IL（Yao et al., 2022） | 59.9 | 29.1 |
| IL+RL（Yao et al., 2022） | 62.4 | 28.7 |
| 微调（Furuta et al., 2024） | 67.5 | 45.0 |
| 专家 | 82.1 | 59.6 |

表 6：WebShop 上的得分与成功率（SR）。结果按提示、基于 RL 的训练与人类表现分组。在相同迭代次数下，LATS 同时改进得分与 SR，并超越基于 RL 的训练。

| 提示方法 | 24 点游戏（成功率）↑ |
| --- | --- |
| CoT（Wei et al., 2022） | 0.08 |
| Reflexion（Shinn et al., 2023） | 0.12 |
| ToT（Yao et al., 2023a） | 0.20 |
| RAP（Hao et al., 2023） | 0.40 |
| LATS（CoT） | 0.44 |

表 7：GPT-3.5 在 24 点游戏上的结果。我们采样 $n=5$ 个节点、$k=30$ 条轨迹。

### 5.4 消融研究与补充分析

我们进一步在 24 点游戏上测试 LATS 的推理能力，并在 HotPotQA 上做额外实验以展示 LATS 各组件的作用（结果见表 8）。HotPotQA 上关于 token 消耗的更多消融见附录 C 节表 9。

24 点游戏上的推理。为展示 LATS 如何应用于纯内部推理任务，我们额外评估 24 点游戏（Yao et al., 2023a）——一个数学推理任务，智能体必须用一组数字与基本运算构造出 24。我们用 CoT 作为基础提示设计，并采用与其他设定相同的操作。我们在表 7 中发现，LATS 优于此前专为推理提出的方法。这归功于我们提出的价值函数，它把自洽性作为附加启发式纳入。

| 提示方法 | HotPotQA (EM) ↑ |
| --- | --- |
| ToT（ReAct） | 0.39 |
| RAP（ReAct） | 0.54 |
| LATS（无 LM 启发式） | 0.37 |
| LATS（DFS） | 0.42 |
| LATS（无反思） | 0.58 |
| LATS（ReAct） | 0.63 |

表 8：LATS 与基线变体在 HotPotQA 上的消融结果。我们用 ReAct 作为基础提示，采样 $n=5$ 个子节点、$k=50$ 条轨迹。LATS 需要每个组件与操作才能取得最佳表现。

自我反思。LATS 用自我反思为智能体提供额外语义信号。在表 8（第 5、6 行）中，我们观察到从 LATS 中移除自我反思会导致 0.05 的性能下降，验证了其用处。这比表 3 中 Reflexion 相对 ReAct 的 0.19 增益要小，说明「可通过自我反思改进的问题」与「可通过搜索改进的问题」存在重叠。该变体仍优于 RAP（ReAct），体现了我们对 MCTS 的改进。

| 方法 | 性能 ↑ | 样本复杂度 ↓ | token 消耗 ↓ |
| --- | --- | --- | --- |
| ReAct（最佳 k=250） | 0.42 | $O(k)$ | - |
| CoT-SC（n=1, k=250） | 0.40 | $O(k)$ | - |
| LATS（n=1, k=50） | 0.48 | $O(k)$ | - |
| ToT（ReAct, n=5, k=50） | 0.49 | $O(kn)$ | 210,215 |
| RAP（ReAct, n=5, k=50） | 0.54 | $O(kn)$ | 176,500 |
| LATS（n=5, k=50） | 0.63 | $O(kn)$ | 173,290 |

表 9：不同方法的性能、样本复杂度、平均展开节点数，以及带树搜索方法成功时的 token 消耗。$n$ 是每步展开的子节点数，$k$ 是轨迹数。LATS 与其他带树搜索的方法样本复杂度相同，且成功时展开节点更少，表明 token 成本更低。

| 方法 | k | HotPotQA ↑ | 节点数 ↓ |
| --- | --- | --- | --- |
| ToT | 10 | 0.34 | 33.97 |
| RAP | 10 | 0.44 | 31.53 |
| LATS | 10 | 0.44 | 28.42 |
| ToT | 30 | 0.39 | 47.54 |
| RAP | 30 | 0.50 | 37.71 |
| LATS | 30 | 0.52 | 34.12 |
| ToT | 50 | 0.49 | 84.05 |
| RAP | 50 | 0.54 | 70.60 |
| LATS | 50 | 0.61 | 66.65 |

表 10：不同方法在 HotPotQA 上的成本比较。在各 $k$ 轨迹采样量下，LATS 都取得最高准确率与最低的平均成功所需节点/状态数。

搜索算法。MCTS 是比 A*（Zhuang et al., 2023）或 DFS 等变体更有原则的搜索算法，是所观察到性能增益的基础。我们观察使用 DFS 的效果，并纳入 ToT 所用的基于 LM 的启发式（剪掉低价值分支）。这移除了选择与回传操作；在采样相同节点数时，我们观察到表 8（第 4 行）中 0.21 的性能下降，但仍优于 ToT（ReAct）。尽管同样受益于真实反馈，LATS 比 ToT 与 RAP 用得更好，能超越这些方法。我们还在表 8（第 3 行）发现，LM 打分（我们价值函数的主组件）对利用外部反馈与强性能至关重要。

样本复杂度与 token 消耗。LATS 的一个可能的顾虑是：树结构搜索可能比既有方法消耗多得多的 token。为进一步研究 LATS 相对先前方法的计算成本，我们考察本文所有方法的样本复杂度（即渐近 token 成本），并统计我们的方法与其他树结构方法（ToT 与 RAP）在 HotPotQA 上成功搜索时平均展开的节点数。结果见表 9 与表 10，表明我们的方法与其他基于树的搜索方法样本复杂度相同，且所需 token 与状态总体更少。若把失败轨迹计入，token 成本差距会更大，因为我们的方法成功率更高、更少触及计算预算上限。在采样较少轨迹时也是如此：平均而言，LATS 比 RAP 少用 3.55 个节点，比 ToT 少用 12.12 个节点。这些发现凸显了我们对 MCTS 的改进及对 LM 智能体的适配，造就了一种更有原则且高效的搜索机制。

## 6 结论

本工作提出语言智能体树搜索（LATS），首个统一推理、行动与规划以增强 LM 问题求解的框架。LATS 通过用搜索算法审慎构造轨迹、纳入外部反馈并使智能体从经验中学习，解决了先前提示技术的关键局限。我们的评估展示了 LATS 在*无需额外训练*的情况下为各类决策任务发挥 LM 能力、同时保持推理能力的表现。搜索、交互与反思之间的协同提供了一种 versatile 的自主决策方法，凸显了 LM 作为通用智能体的潜力。

局限与未来方向。LATS 有两个主要局限，应用前应予考虑。其一，相比 ReAct 或 Reflexion 等更简单的提示方法，它的计算成本更高，在某些情境下可能限制其实用性。其二，LATS 假设在决策环境中可以回退到较早状态，这未必在所有可能的环境中普遍适用。尽管有这些局限，值得注意的是 LATS 相比同类方法仍取得更好的性能与效率，且每步展开的节点数提供了性能与效率之间的权衡。此外，我们预期推理时计算成本会随时间下降，从而提升 LATS 及其他「System-2」LM 方法的用处。最后，回退性质在许多现实应用中可行，为 LM 决策社区带来新机会。未来方向包括把 LATS 扩展到更复杂的环境或多智能体框架，以及改进效率以降低成本。关于 LATS 局限的更详细讨论见附录 B 节。

## 影响声明

LATS 是通过与环境的交互增强 LM 表现的框架。这种自主决策能力的提升可能助长 LM 的有害用途。另一方面，LATS 增强了可解释性与更好对齐的潜力，因为它经由多轮决策与反思进行高层语言推理与行动，而非依赖自回归生成。最后，增强 LM 智能体的能力可能带来安全风险，例如执行恶意软件。我们鼓励进一步研究以充分理解并缓解 LM 的风险。

## 致谢

我们感谢 Daniel Campos 对本文早期版本的有益反馈。本工作部分受 NSF Grant 2106825、NIFA Award 2020-67021-32799、Jump ARCHES 通过伊利诺伊健康护理工程系统中心与 OSF 基金会提供的捐赠、以及 IBM-Illinois Discovery Accelerator Institute 资助。本工作通过 ACCESS 项目的分配 CIS220014、CIS230012 与 CIS230218 使用了 NCSA Delta 的 NVIDIA GPU。

## 参考文献
- Ahn et al. (2022)

  Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Daniel Ho, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Eric Jang, Rosario Jauregui Ruano, Kyle Jeffrey, Sally Jesmonth, Nikhil J Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Kuang-Huei Lee, Sergey Levine, Yao Lu, Linda Luu, Carolina Parada, Peter Pastor, Jornell Quiambao, Kanishka Rao, Jarek Rettinghouse, Diego Reyes, Pierre Sermanet, Nicolas Sievers, Clayton Tan, Alexander Toshev, Vincent Vanhoucke, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, Mengyuan Yan, and Andy Zeng.
  Do as I can, not as I say: Grounding language in robotic affordances.
  In *CoRL*, 2022.
- Austin et al. (2022)

  Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le, and Charles Sutton.
  Program synthesis with large language models.
  In *NeurIPS*, 2022.
- Baker et al. (2022)

  Bowen Baker, Ilge Akkaya, Peter Zhokhov, Joost Huizinga, Jie Tang, Adrien Ecoffet, Brandon Houghton, Raul Sampedro, and Jeff Clune.
  Video pretraining (VPT): Learning to act by watching unlabeled online videos.
  In *NeurIPS*, 2022.
- Besta et al. (2023)

  Maciej Besta, Nils Blach, Ales Kubicek, Robert Gerstenberger, Lukas Gianinazzi, Joanna Gajda, Tomasz Lehmann, Michal Podstawski, Hubert Niewiadomski, Piotr Nyczyk, and Torsten Hoefler.
  Graph of thoughts: Solving elaborate problems with large language models.
  *arXiv:2308.09687*, 2023.
- Bowman et al. (2015)

  Samuel R Bowman, Gabor Angeli, Christopher Potts, and Christopher D Manning.
  A large annotated corpus for learning natural language inference.
  In *EMNLP*, 2015.
- Brown et al. (2020)

  Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei.
  Language models are few-shot learners.
  In *NeurIPS*, 2020.
- Campbell et al. (2002)

  Murray Campbell, A Joseph Hoane Jr, and Feng-hsiung Hsu.
  Deep blue.
  *Artificial intelligence*, 2002.
- Chen et al. (2023a)

  Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan, Zeqi Lin, Jian-Guang Lou, and Weizhu Chen.
  CodeT: Code generation with generated tests.
  In *ICLR*, 2023a.
- Chen et al. (2021)

  Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde, Jared Kaplan, Harrison Edwards, Yura Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, David W. Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William H. Guss, Alex Nichol, Igor Babuschkin, Suchir Balaji, Shantanu Jain, Andrew Carr, Jan Leike, Joshua Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew M. Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba.
  Evaluating large language models trained on code.
  *arXiv:2107.03374*, 2021.
- Chen et al. (2023b)

  Wenhu Chen, Xueguang Ma, Xinyi Wang, and William W. Cohen.
  Program of thoughts prompting: disentangling computation from reasoning for numerical reasoning tasks.
  *TMLR*, 2023b.
  ISSN 2835-8856.
- Chowdhery et al. (2023)

  Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, Parker Schuh, Kensen Shi, Sasha Tsvyashchenko, Joshua Maynez, Abhishek Rao, Parker Barnes, Yi Tay, Noam Shazeer, Vinodkumar Prabhakaran, Emily Reif, Nan Du, Ben Hutchinson, Reiner Pope, James Bradbury, Jacob Austin, Michael Isard, Guy Gur-Ari, Pengcheng Yin, Toju Duke, Anselm Levskaya, Sanjay Ghemawat, Sunipa Dev, Henryk Michalewski, Xavier Garcia, Vedant Misra, Kevin Robinson, Liam Fedus, Denny Zhou, Daphne Ippolito, David Luan, Hyeontaek Lim, Barret Zoph, Alexander Spiridonov, Ryan Sepassi, David Dohan, Shivani Agrawal, Mark Omernick, Andrew M. Dai, Thanumalayan Sankaranarayana Pillai, Marie Pellat, Aitor Lewkowycz, Erica Moreira, Rewon Child, Oleksandr Polozov, Katherine Lee, Zongwei Zhou, Xuezhi Wang, Brennan Saeta, Mark Diaz, Orhan Firat, Michele Catasta, Jason Wei, Kathy Meier-Hellstern, Douglas Eck, Jeff Dean, Slav Petrov, and Noah Fiedel.
  PaLM: Scaling language modeling with pathways.
  *JMLR*, 24(240):1–113, 2023.
- Cobbe et al. (2021)

  Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman.
  Training verifiers to solve math word problems.
  *arXiv:2110.14168*, 2021.
- Deng et al. (2023)

  Xiang Deng, Yu Gu, Boyuan Zheng, Shijie Chen, Samuel Stevens, Boshi Wang, Huan Sun, and Yu Su.
  Mind2Web: Towards a generalist agent for the web.
  In *NeurIPS Datasets and Benchmarks Track*, 2023.
- Driess et al. (2023)

  Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, Yevgen Chebotar, Pierre Sermanet, Daniel Duckworth, Sergey Levine, Vincent Vanhoucke, Karol Hausman, Marc Toussaint, Klaus Greff, Andy Zeng, Igor Mordatch, and Pete Florence.
  PaLM-E: An embodied multimodal language model.
  In *ICML*, 2023.
- Du et al. (2023)

  Yilun Du, Mengjiao Yang, Bo Dai, Hanjun Dai, Ofir Nachum, Joshua B. Tenenbaum, Dale Schuurmans, and Pieter Abbeel.
  Learning universal policies via text-guided video generation.
  In *NeurIPS*, 2023.
- Evans (2010)

  Jonathan St BT Evans.
  Intuition and reasoning: A dual-process perspective.
  *Psychological Inquiry*, pages 313 – 326, 2010.
- Fan et al. (2022)

  Linxi Fan, Guanzhi Wang, Yunfan Jiang, Ajay Mandlekar, Yuncong Yang, Haoyi Zhu, Andrew Tang, De-An Huang, Yuke Zhu, and Anima Anandkumar.
  MineDojo: Building open-ended embodied agents with internet-scale knowledge.
  In *NeurIPS Datasets and Benchmarks Track*, 2022.
- Furuta et al. (2024)

  Hiroki Furuta, Ofir Nachum, Kuang-Huei Lee, Yutaka Matsuo, Shixiang Shane Gu, and Izzeddin Gur.
  Multimodal web navigation with instruction-finetuned foundation models.
  In *ICLR*, 2024.
- Gao et al. (2023)

  Luyu Gao, Aman Madaan, Shuyan Zhou, Uri Alon, Pengfei Liu, Yiming Yang, Jamie Callan, and Graham Neubig.
  PAL: Program-aided language models.
  In *ICML*, 2023.
- Guo et al. (2018)

  Jiaxian Guo, Sidi Lu, Han Cai, Weinan Zhang, Yong Yu, and Jun Wang.
  Long text generation via adversarial training with leaked information.
  In *AAAI*, 2018.
- Guss et al. (2019)

  William H. Guss, Brandon Houghton, Nicholay Topin, Phillip Wang, Cayden Codel, Manuela Veloso, and Ruslan Salakhutdinov.
  MineRL: A large-scale dataset of Minecraft demonstrations.
  In *IJCAI*, 2019.
- Hafner et al. (2019)

  Danijar Hafner, Timothy Lillicrap, Ian Fischer, Ruben Villegas, David Ha, Honglak Lee, and James Davidson.
  Learning latent dynamics for planning from pixels.
  In *ICML*, 2019.
- Hafner et al. (2023)

  Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap.
  Mastering diverse domains through world models.
  *arXiv:2301.04104*, 2023.
- Hao et al. (2023)

  Shibo Hao, Yi Gu, Haodi Ma, Joshua Jiahua Hong, Zhen Wang, Daisy Zhe Wang, and Zhiting Hu.
  Reasoning with language model is planning with world model.
  In *EMNLP*, 2023.
- Huang et al. (2024)

  Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny Zhou.
  Large language models cannot self-correct reasoning yet.
  In *ICLR*, 2024.
- Huang et al. (2022)

  Wenlong Huang, F. Xia, Ted Xiao, Harris Chan, Jacky Liang, Peter R. Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, Pierre Sermanet, Noah Brown, Tomas Jackson, Linda Luu, Sergey Levine, Karol Hausman, and Brian Ichter.
  Inner monologue: Embodied reasoning through planning with language models.
  In *CoRL*, 2022.
- Kocsis and Szepesvári (2006)

  Levente Kocsis and Csaba Szepesvári.
  Bandit based monte-carlo planning.
  In *ECML*, 2006.
- Kojima et al. (2022)

  Takeshi Kojima, Shixiang Shane Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa.
  Large language models are zero-shot reasoners.
  In *NeurIPS*, 2022.
- LaValle (1998)

  Steven M. LaValle.
  Rapidly-exploring random trees : A new tool for path planning.
  *The Annual Research Report*, 1998.
- Liu et al. (2018)

  Evan Zheran Liu, Kelvin Guu, Panupong Pasupat, Tianlin Shi, and Percy Liang.
  Reinforcement learning on web interfaces using workflow-guided exploration.
  In *ICLR*, 2018.
- Liu et al. (2024)

  Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Aohan Zeng, Zhengxiao Du, Chenhui Zhang, Sheng Shen, Tianjun Zhang, Yu Su, Huan Sun, Minlie Huang, Yuxiao Dong, and Jie Tang.
  AgentBench: Evaluating LLMs as agents.
  In *ICLR*, 2024.
- Liu et al. (2023)

  Zhihan Liu, Hao Hu, Shenao Zhang, Hongyi Guo, Shuqi Ke, Boyi Liu, and Zhaoran Wang.
  Reason for future, act for now: A principled framework for autonomous LLM agents with provable sample efficiency.
  *arXiv:2309.17382*, 2023.
- Madaan et al. (2023)

  Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, and Peter Clark.
  Self-refine: Iterative refinement with self-feedback.
  In *NeurIPS*, 2023.
- Nallapati et al. (2016)

  Ramesh Nallapati, Bowen Zhou, Cicero dos Santos, Caglar Gulcehre, and Bing Xiang.
  Abstractive text summarization using sequence-to-sequence RNNs and beyond.
  In *Special Interest Group on Natural Language Learning*, 2016.
- OpenAI (2023)

  OpenAI.
  GPT-4 technical report.
  *arXiv:2303.08774*, 2023.
- Qin et al. (2024)

  Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, Sihan Zhao, Runchu Tian, Ruobing Xie, Jie Zhou, Mark Gerstein, Dahai Li, Zhiyuan Liu, and Maosong Sun.
  ToolLLM: Facilitating large language models to master 16000+ real-world APIs.
  In *ICLR*, 2024.
- Saparov and He (2023)

  Abulhair Saparov and He He.
  Language models are greedy reasoners: A systematic formal analysis of chain-of-thought.
  In *ICLR*, 2023.
- Schick et al. (2023)

  Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom.
  Toolformer: Language models can teach themselves to use tools.
  In *NeurIPS*, 2023.
- Shen et al. (2023)

  Yongliang Shen, Kaitao Song, Xu Tan, Dongsheng Li, Weiming Lu, and Yueting Zhuang.
  HuggingGPT: Solving AI tasks with ChatGPT and its friends in Hugging Face.
  In *NeurIPS*, 2023.
- Shinn et al. (2023)

  Noah Shinn, Federico Cassano, Beck Labash, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao.
  Reflexion: Language agents with verbal reinforcement learning.
  In *NeurIPS*, 2023.
- Shridhar et al. (2020)

  Mohit Shridhar, Xingdi Yuan, Marc-Alexandre Côté, Yonatan Bisk, Adam Trischler, and Matthew Hausknecht.
  ALFWorld: Aligning text and embodied environments for interactive learning.
  In *ICLR*, 2020.
- Silver et al. (2016)

  David Silver, Aja Huang, Chris J. Maddison, Arthur Guez, L. Sifre, George van den Driessche, Julian Schrittwieser, Ioannis Antonoglou, Vedavyas Panneershelvam, Marc Lanctot, Sander Dieleman, Dominik Grewe, John Nham, Nal Kalchbrenner, Ilya Sutskever, Timothy P. Lillicrap, Madeleine Leach, Koray Kavukcuoglu, Thore Graepel, and Demis Hassabis.
  Mastering the game of Go with deep neural networks and tree search.
  *Nature*, 529:484–489, 2016.
- Silver et al. (2017)

  David Silver, Aja Huang, Chris J. Maddison, Arthur Guez, L. Sifre, George van den Driessche, Julian Schrittwieser, Ioannis Antonoglou, Vedavyas Panneershelvam, Marc Lanctot, Sander Dieleman, Dominik Grewe, John Nham, Nal Kalchbrenner, Ilya Sutskever, Timothy P. Lillicrap, Madeleine Leach, Koray Kavukcuoglu, Thore Graepel, and Demis Hassabis.
  Mastering chess and Shogi by self-play with a general reinforcement learning algorithm.
  *arXiv:1712.01815*, 2017.
- Sloman (1996)

  Steven A. Sloman.
  The empirical case for two systems of reasoning.
  *Psychological Bulletin*, 119:3–22, 1996.
- Sun et al. (2023)

  Haotian Sun, Yuchen Zhuang, Lingkai Kong, Bo Dai, and Chao Zhang.
  AdaPlanner: Adaptive planning from feedback with language models.
  In *NeurIPS*, 2023.
- Surís et al. (2023)

  Dídac Surís, Sachit Menon, and Carl Vondrick.
  ViperGPT: Visual inference via Python execution for reasoning.
  In *ICCV*, 2023.
- Swiechowski et al. (2021)

  Maciej Swiechowski, Konrad Godlewski, Bartosz Sawicki, and Jacek Ma’ndziuk.
  Monte Carlo tree search: A review of recent modifications and applications.
  *Artificial Intelligence Review*, 56:2497–2562, 2021.
- Touvron et al. (2023)

  Hugo Touvron, Louis Martin, Kevin R. Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Daniel M. Bikel, Lukas Blecher, Cristian Cantón Ferrer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony S. Hartshorn, Saghar Hosseini, Rui Hou, Hakan Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa, Isabel M. Kloumann, A. V. Korenev, Punit Singh Koura, Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich, Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov, Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi, Alan Schelten, Ruan Silva, Eric Michael Smith, R. Subramanian, Xia Tan, Binh Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu, Zhengxu Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan, Melanie Kambadur, Sharan Narang, Aurelien Rodriguez, Robert Stojnic, Sergey Edunov, and
  Thomas Scialom.
  Llama 2: Open foundation and fine-tuned chat models.
  *arXiv:2307.09288*, 2023.
- Vodopivec et al. (2017)

  Tom Vodopivec, Spyridon Samothrakis, and Branko Ster.
  On Monte Carlo tree search and reinforcement learning.
  *Journal of Artificial Intelligence Research*, 60:881–936, 2017.
- Wang et al. (2023)

  Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar.
  Voyager: An open-ended embodied agent with large language models.
  *arXiv:2305.16291*, 2023.
- Wang et al. (2022)

  Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, and Denny Zhou.
  Self-consistency improves chain of thought reasoning in language models.
  In *ICLR*, 2022.
- Wei et al. (2022)

  Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Ed Chi, Quoc Le, and Denny Zhou.
  Chain of thought prompting elicits reasoning in large language models.
  In *NeurIPS*, 2022.
- Wooldridge and Jennings (1995)

  Michael Wooldridge and Nicholas R Jennings.
  Intelligent agents: Theory and practice.
  *The Knowledge Engineering Review*, 10:115 – 152, 1995.
- Wu et al. (2023)

  Philipp Wu, Alejandro Escontrela, Danijar Hafner, Pieter Abbeel, and Ken Goldberg.
  Daydreamer: World models for physical robot learning.
  In *CoRL*, 2023.
- Xie et al. (2023)

  Yuxi Xie, Kenji Kawaguchi, Yiran Zhao, Xu Zhao, Min-Yen Kan, Junxian He, and Qizhe Xie.
  Decomposition enhances reasoning via self-evaluation guided decoding.
  *arXiv:2305.00633*, 2023.
- Yang et al. (2018)

  Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W Cohen, Ruslan Salakhutdinov, and Christopher D Manning.
  HotpotQA: A dataset for diverse, explainable multi-hop question answering.
  In *EMNLP*, 2018.
- Yao et al. (2022)

  Shunyu Yao, Howard Chen, John Yang, and Karthik R Narasimhan.
  WebShop: Towards scalable real-world web interaction with grounded language agents.
  In *NeurIPS*, 2022.
- Yao et al. (2023a)

  Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, and Karthik Narasimhan.
  Tree of thoughts: deliberate problem solving with large language models.
  In *NeurIPS*, 2023a.
- Yao et al. (2023b)

  Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao.
  ReAct: Synergizing reasoning and acting in language models.
  In *ICLR*, 2023b.
- Ye et al. (2021)

  Weirui Ye, Shaohuai Liu, Thanard Kurutach, Pieter Abbeel, and Yang Gao.
  Mastering Atari games with limited data.
  In *NeurIPS*, 2021.
- Zhou et al. (2022)

  Denny Zhou, Nathanael Schärli, Le Hou, Jason Wei, Nathan Scales, Xuezhi Wang, Dale Schuurmans, Olivier Bousquet, Quoc Le, and Ed Chi.
  Least-to-most prompting enables complex reasoning in large language models.
  In *ICLR*, 2022.
- Zhuang et al. (2023)

  Yuchen Zhuang, Xiang Chen, Tong Yu, Saayan Mitra, Victor Bursztyn, Ryan A. Rossi, Somdeb Sarkhel, and Chao Zhang.
  ToolChain*: Efficient action space navigation in large language models with A* search.
  In *ICLR*, 2023.

## LATS 附录

附录组织如下。首先在 A 节给出我们提出的算法 LATS 的伪代码。B 节进一步讨论我们方法的局限。C 节给出补充实验结果。D 节说明实验中的环境细节。最后，在 E 节（HotPotQA）、F 节（编程）与 G 节（WebShop）分别列出我们在三个环境中使用的提示词。

## 附录 A LATS 伪代码

算法 1 给出我们算法 LATS 的伪代码。节点显式存储在内存中。除非特别说明，所有实验中我们把采样节点数设为 $n=5$、探索权重 $w=1$。HotPotQA 与 24 点游戏的自洽性权重用 $\lambda=0.5$，编程与 WebShop 用 $\lambda=0.8$。

Algorithm 1  LATS⁡(s,pθ,pV,pref,d,k,n,w,a,b)\operatorname{LATS}(s,p_{\theta},{p_{V}},p_{\text{ref}},d,k,n,w,a,b)

Initial state ss, action generator pθp_{\theta}, value function pVp_{V}, reflection generator prefp_{\text{ref}}, number of generated actions nn, depth limit LL, number of roll-outs KK, context cc, exploration weight ww, and value function weight λ\lambda

Initialize action space AA, observation space OO

Initialize the state-action value function pV:S×A↦ℝ{p_{V}}:S\times A\mapsto\mathbb{R} and visit counter N:S↦ℕ{N}:S\mapsto\mathbb{N} to one

for k←0,…,K−1k\leftarrow 0,\dots,K-1 do

for t←0,…,L−1t\leftarrow 0,\dots,L-1 do

if sts_{t} not terminal then ⊳\triangleright Expansion & Simulation

for i←1,…,ni\leftarrow 1,\dots,n do

Sample at(i)∼pθ​(st)a_{t}^{(i)}\sim p_{\theta}(s_{t})

Get ot(i)o_{t}^{(i)} from environment, st+1(i)←(ct(i),ot(i),at(i))s_{t+1}^{(i)}\leftarrow(c_{t}^{(i)},o_{t}^{(i)},a_{t}^{(i)}), ct+1(i)←(ot(i),at(i))c_{t+1}^{(i)}\leftarrow(o_{t}^{(i)},a_{t}^{(i)})

Evaluate Vt(i)∼λ∗pV​(st(i))+(1−λ)∗SC​(st(i)){V}_{t}^{(i)}\sim\lambda*{p_{V}}(s_{t}^{(i)})+(1-\lambda)*\text{SC}(s_{t}^{(i)})
⊳\triangleright Evaluation

V⁡(st)←Vt(i){V}(s_{t})\leftarrow{V}_{t}^{(i)}

Add st(i)s_{t}^{(i)} to children

end for

end if

if sts_{t} is terminal then
⊳\triangleright Reflection

Get rr from environment

if rr not success then

reflection←pref​(ct)\text{reflection}\leftarrow p_{\text{ref}}(c_{t})

c←reflectionc\leftarrow\text{reflection}

end if

end if

at←arg⁡maxa∈e⁡(st)⁡[V⁡(st)+w​ln⁡N⁡(st)N⁡(st+1)]a_{t}\leftarrow\arg\max_{a\in e(s_{t})}\left[{V(s_{t})}+w\sqrt{\frac{\ln{N}(s_{t})}{{N}(s_{t+1})}}\right] ⊳\triangleright Selection

Get corresponding oto_{t} from memory, st+1←(ct,ot,at),ct+1←(ot,at)s_{t+1}\leftarrow(c_{t},o_{t},a_{t}),c_{t+1}\leftarrow(o_{t},a_{t})

N⁡(st+1)←N⁡(st+1)+1{N}(s_{t+1})\leftarrow{N}(s_{t+1})+1

if ata_{t} is an output action then break

end for

T←T\leftarrow the actual number of steps

for t←T−1,…,0t\leftarrow T-1,\dots,0 do ⊳\triangleright Backpropagation

V⁡(st)←V⁡(st)​(N⁡(st)−1)+rN⁡(st)V(s_{t})\leftarrow\frac{V(s_{t})(N(s_{t})-1)+r}{N(s_{t})}

end for

end for
## 附录 B 关于局限的更多讨论

如第 6 节所述，LATS 有两个主要局限：

计算成本。虽然 LATS 能改进推理与决策，但这是以相对 ReAct 或 Reflexion 等更简单提示方法更高的计算成本为代价的。不过，以下事实可缓解该问题：

- 渐近上，我们的方法与 ToT（Yao et al., 2023a）和 RAP（Hao et al., 2023）样本复杂度相同，但表现更好、成功时平均展开更少节点、使用更少 token。这表明我们的方法不仅解题能力更强，效率也更高。成本的完整分析见附录 C 的表 9。
- 每步展开的节点数 $n$ 提供了性能与效率之间的天然权衡。事实上，设 $n=1$ 可使该方法与多次尝试的 ReAct（Yao et al., 2023b）或 CoT-SC（Wang et al., 2022）一样高效。

总体而言，我们建议把 LATS 用于编程等困难任务，或实践中性能优先于效率的场景。我们希望 LM 的持续进步会降低成本并扩大 LATS 的适用性。

此外，查询环境也存在少量成本，我们发现这对我们研究的环境微不足道。大多数基于 LM 的环境涉及基于 API 的工具，使用起来便宜且快速。还值得注意的是，这比如先前搜索方法（Hao et al., 2023；Liu et al., 2023）中把 LM 用作世界模型带来的推理成本更便宜。

决策中环境回退的假设。由于我们的方法基于蒙特卡洛树搜索且是无模型的，LATS 在决策任务上的一个局限是要求智能体能回退到环境中的较早状态。然而，这一回退性质在许多现实环境与应用中可行（尽管并非在所有可能环境中普遍适用），包括编程（HumanEval（Chen et al., 2021））、网络搜索（WebShop（Yao et al., 2022））、基于文本的操作任务（Alfworld（Shridhar et al., 2020））以及带工具使用的 LM（ToolBench（Qin et al., 2024））。因此我们相信，利用回退性质并非缺点，而是尚未被 LM 决策社区明确关注的一项特性——它为新兴的 LM 智能体社区带来新机会。

此外，与现实交互环境的复杂性相比，我们本文使用的基准相对简单且聚焦决策。而且，某些环境可能不易支持回滚到先前状态。但 LATS 的设计是灵活的，可以针对各种资源约束调整。在 Minecraft（Fan et al., 2022）等环境及更多推理基准中使用基于规划的提示方法（如 LATS）是有趣的未来方向。

## 附录 C 补充消融

| 提示方法 | HotpotQA (EM) ↑ |
| --- | --- |
| LATS（w=0.5） | 0.55 |
| LATS（w=2.0） | 0.63 |
| LATS（d=4） | 0.58 |
| LATS（CoT） | 0.62 |
| LATS（无 LM 启发式） | 0.37 |
| LATS（w=1.0, d=7） | 0.63 |

表 11：LATS 与基线变体在 HotPotQA 上以精确匹配（EM）衡量的消融结果。我们测试不同深度 $d$、探索因子 $w$、以及使用 CoT 和无 LM 价值函数的 LATS 版本。我们采样 $n=5$、$k=50$ 条轨迹。

![Refer to caption](2310.04406v3/figures/k.png)

图 3：GPT-3.5 在 HumanEval 上随迭代推进的表现。

本节对 LATS 的各种设计做消融。实验在 HotPotQA（最多 $k=50$ 条轨迹、采样规模 $n=5$）与 HumanEval（最多 $k=8$ 条轨迹、采样规模 $n=5$）上进行。HotPotQA 的结果见表 8，HumanEval 的结果见图 3。

探索权重。我们发现，当选择公式中的探索权重 $w$ 降到 0.5 时，HotPotQA 上的表现下降，说明这削弱了搜索的有效性。把 $w$ 提高到 2.0 不会带来性能提升，但我们往往观察到更快的收敛。最优设定取决于具体环境与状态空间的复杂度。

深度。主实验中，遵循先前工作（Yao et al., 2023b），我们在 HotPotQA 上对所有方法使用最大深度 $d=7$。我们消融了把它降到 $d=4$ 对 LATS 的影响，性能仅轻微下降。我们发现大多数问题可在四步内回答，使用更多步数往往把智能体逼入局部极小，很少提升成功率。

LM 价值函数。LM 价值函数依据期望未来奖励为状态打分。没有这一启发式，引导搜索的信号就只剩完成轨迹的环境奖励——它们稀少且常为二元。移除评估操作后，我们观察到 0.26 的显著性能下降。

随时间的表现。为观察增加采样轨迹数的影响，我们把 $k$ 改为不同值。该实验在 HumanEval 上进行，因采样轨迹较少，差异更明显。结果见图 3：随着迭代增多，LATS 比 Reflexion 扩展得更好。

## 附录 D 环境细节

### D.1 HotPotQA

图 4：HotPotQA 上 ReAct（左）与 LATS（右）的示例轨迹。LATS 能采样更多行动，并通过用 LM 评估状态把搜索引向树中有希望的区域，从而避免重蹈先前错误的覆辙。

HotPotQA（Yang et al., 2018）是一个需要跨多份支撑文档推理作答的问答数据集。它包含 11.3 万对由众包工作者精心构造的基于 Wikipedia 的问答对，具有多样性、多跳性与可解释性。问题覆盖实体、地点、日期、以及两实体共有属性比较等多种类型。众包工作者还提供文档中支撑答案的事实。我们使用带全部 Wikipedia 段落的 HotPotQA 基准设定来测试检索。我们实验用随机选取的 100 个问题子集，最大深度限制为 6。图 4 展示了 ReAct 与 LATS 在 HotPotQA 示例任务上的运作方式，并给出 LATS 优于 ReAct 的定性示例。价值函数超参数方面，LM 打分与自洽性打分用 $\lambda=0.5$。

行动空间。我们采用 Yao et al. (2023b) 提出的 Wikipedia web API，含三类支持交互式信息检索的行动：

（1）search[entity]，若对应实体 wiki 页面存在则返回该页面的前 5 个句子，否则从 Wikipedia 搜索引擎返回最相似的前 5 个实体；

（2）lookup[string]，返回页面中包含 string 的下一个句子；

（3）finish[answer]，以 answer 结束当前任务。

这些 API 调用与自由形式的思考构成本环境的行动空间。

### D.2 编程

HumanEval 数据集（Chen et al., 2021）收录 164 道手写编程题，用于评估模型从自然语言描述合成程序的功能正确性。每题含函数签名、docstring 描述、参考实现与多个单元测试，平均每题 7.7 个测试。这些编程任务考察自然语言理解、推理、算法与基础数学，难度与简单软件面试题相当。通过率用 pass@k 指标评估：每题生成 k 个样本，任一样本通过全部测试即视为解决。我们实验使用全部 164 道题，最大深度限制为 8。对三道没有示例测试用例的题，我们自己编写。价值函数超参数方面，LM 打分与自洽性打分用 $\lambda=0.8$。GPT-3.5 用 6 个内部测试，GPT-4 用 4 个。

Mostly Basic Programming Problems（MBPP）（Austin et al., 2022）基准包含 974 个短 Python 函数，用于评估程序合成技术。该数据集由具备基础 Python 知识的工作者众包构造。每个数据点由编程任务的自然语言描述、参考解实现与三个功能正确性测试用例组成。自然语言提示通常是一句话的简短描述。解覆盖常见编程构造，包括数学运算、列表处理、字符串操作与 Python 标准库的使用。解平均 6.8 行代码。该数据集还补充了 426 道经人工核验规格无歧义、函数签名标准、测试用例准确的问题。我们实验用随机选取的 397 道题子集。价值函数超参数方面，LM 打分与自洽性打分用 $\lambda=0.8$。

### D.3 WebShop

WebShop（Yao et al., 2022）是一个交互式 web 环境，用于评估智能体的落地语言理解与决策能力。它通过向智能体提供从 Amazon 抓取的 100 多万件真实商品（跨 5 大类 113 个子类）来模拟电商购物任务。这些商品含丰富的语言信息，平均文本长度 262 词、词汇量 22.4 万。此外还有 80 多万个可供定制的唯一商品选项。环境以两种模式渲染网页：HTML 模式提供带交互元素的像素级观察；简单模式把原始 HTML 转换为更利于训练智能体的结构化文本观察。行动空间由查询搜索与按钮点击组成，在 4 种页面类型之间转移：搜索、结果、商品与商品详情。指令是众包的自然语言，指定商品属性与选项，共收集 1.2 万条。自动奖励通过把智能体购买的商品与指令中指定的属性和选项比对计算，同时使用词法匹配与语义相似度指标。

| 类型 | 参数 | 状态 → 下一状态 |
| --- | --- | --- |
| search | [Query] | Search → Results |
| choose | Back to search | ∗ → Search |
| choose | Prev/Next page | Results → Results |
| choose | [Product title] | Results → Item |
| choose | [Option] | Item → Item |
| choose | Desc/Overview | Item → Item-Detail |
| choose | Previous | Item-Detail → Item |
| choose | Buy | Item → Episode End |

表 12：WebShop 的行动空间。

WebShop 使用两个评估指标：（1）任务得分（Task Score），定义为 $(100\times\text{avg. reward})$，刻画各回合获得的平均奖励；（2）成功率（SR），定义为 $r=1$ 的指令占比。奖励依据所选商品满足的属性数计算。我们实验使用 50 个环境，最大深度限制为 15。价值函数超参数方面，LM 打分与自洽性打分用 $\lambda=0.8$。

### D.4 24 点游戏

24 点游戏是一个数学推理挑战，目标是用基本算术运算从 4 个数字构造出 24。我们沿用 Yao et al. (2023a) 的设定：若智能体给出一个等于 24 且每个输入数字只用一次的正确等式即记为成功。我们报告 50 局游戏上的成功率。我们用 $k=30$ 轮迭代，最大深度限制为 5。价值函数超参数方面，LM 打分与自洽性打分用 $\lambda=0.5$。表 13 给出 $\lambda=0.5$ 与 $\lambda=1$ 的性能比较，验证了我们自洽性项的设计。

| 提示方法 | 24 点游戏（成功率）↑ |
| --- | --- |
| LATS（CoT, λ=1） | 0.40 |
| LATS（CoT） | 0.44 |

表 13：GPT-3.5 在 24 点游戏上对 $\lambda$ 的消融。主文使用的 $\lambda=0.5$ 优于 $\lambda=1$（后者等价于移除自洽性），说明自洽性打分提升了 LATS 的性能。

## 附录 E HotPotQA 提示词

以下提示词展品保留英文原文。

### E.1 Base Acting Prompt

Solve a question answering task with interleaving Thought, Action, Observation steps. Thought can reason about the current situation, and Action can be three types:

(1) Search[entity], which searches the exact entity on Wikipedia and returns the first paragraph if it exists. If not, it will return some similar entities to search.

(2) Lookup[keyword], which returns the next sentence containing keyword in the current passage.

(3) Finish[answer], which returns the answer and finishes the task.

After each observation, provide the next Thought and next Action.

Here are some examples:

Question: Which magazine was started first Arthur’s Magazine or First for Women?

Thought 1: I need to search Arthur’s Magazine and First for Women, and find which was started first.

Action 1: Search[Arthur’s Magazine]

Observation 1: Arthur’s Magazine was an American literary periodical published in Philadelphia in the 19th century. Edited by Timothy Shay Arthur, it featured work by Edgar A. Poe, J.H. Ingraham, Sarah Josepha Hale, Thomas G. Spear, and others.[1][2] In May 1846 it was merged into Godey’s Lady’s Book.[3]

Thought 2: Arthur’s Magazine was started in 1844. I need to search First for Women next.

Action 2: Search[First for Women]

Observation 2: First for Women is a woman’s magazine published by Bauer Media Group in the USA.[1] The magazine was started in 1989. It is based in Englewood Cliffs, New Jersey.[2] In 2011 the circulation of the magazine was 1,310,696 copies.[3]

Thought 3: First for Women was started in 1989. 1844 (Arthur’s Magazine) << 1989 (First for Women), so Arthur’s Magazine was started first.

Action 3: Finish[Arthur’s Magazine]

(examples)

You have attempted to answer the following question before and failed. The following reflection(s) give a plan to avoid failing to answer the question in the same way you did previously. Use them to improve your strategy of correctly answering the given question.

(trajectories)

(input)

### E.2 Base Reasoning Prompt

Solve a question answering task by having a Thought, then Finish with your answer. Thought can reason about the current situation. Finish[answer] returns the answer and finishes the task. You will be given context that you should use to help you answer the question. Start your response with either Action or an indexed Thought

Here are some examples:

Question: What is the elevation range for the area that the eastern sector of the Colorado orogeny extends into?

Let’s think step by step.

Thought 1: The eastern sector of Colorado orogeny extends into the High Plains.

Thought 2: High Plains rise in elevation from around 1,800 to 7,000 ft

Thought 3: The answer is 1,800 to 7,000 ft.

Action: Finish[1,800 to 7,000 ft]

(examples)

Previous trial:
(trajectories)

(input)

### E.3 Value Function Prompt

Analyze the trajectories of a solution to a question answering task. The trajectories are labeled by environmental Observations about the situation, Thoughts that can reason about the current situation, and Actions that can be three types:

(1) Search[entity], which searches the exact entity on Wikipedia and returns the first paragraph if it exists. If not, it will return some similar entities to search.

(2) Lookup[keyword], which returns the next sentence containing keyword in the current passage.

(3) Finish[answer], which returns the answer and finishes the task.

Given a question and a trajectory, evaluate its correctness and provide your reasoning and analysis in detail. Focus on the latest thought, action, and observation. Incomplete trajectories can be correct if the thoughts and actions so far are correct, even if the answer is not found yet. Do not generate additional thoughts or actions. Then at the last line conclude “Thus the correctness score is s”, where s is an integer from 1 to 10.

Question: Which magazine was started first Arthur’s Magazine or First for Women?

Thought 1: I need to search Arthur’s Magazine and First for Women, and find which was started first.

Action 1: Search[Arthur’s Magazine]

Observation 1: Arthur’s Magazine was an American literary periodical published in Philadelphia in the 19th century. Edited by Timothy Shay Arthur, it featured work by Edgar A. Poe, J.H. Ingraham, Sarah Josepha Hale, Thomas G. Spear, and others.[1][2] In May 1846 it was merged into Godey’s Lady’s Book.[3]

This trajectory is correct as it is reasonable to search for the first magazine provided in the question. It is also better to have simple searches corresponding to a single entity, making this the best action.

Thus the correctness score is 10

(other examples)

(failed trajectories)

(context)

### E.4 Reflection Prompt

Analyze the trajectories of a solution to a question-answering task. The trajectories are labeled by environmental Observations about the situation, Thoughts that can reason about the current situation, and Actions that can be three types:

(1) Search[entity], which searches the exact entity on Wikipedia and returns the first paragraph if it exists. If not, it will return some similar entities to search.

(2) Lookup[keyword], which returns the next sentence containing keyword in the current passage.

(3) Finish[answer], which returns the answer and finishes the task.

Given a question and a trajectory, evaluate its correctness and provide your reasoning and analysis in detail. Focus on the latest thought, action, and observation. Incomplete trajectories can be correct if the thoughts and actions so far are correct, even if the answer is not found yet. Do not generate additional thoughts or actions. Then at the last line conclude “Thus the correctness score is s”, where s is an integer from 1 to 10.

Question: Which magazine was started first Arthur’s Magazine or First for Women?

Thought 1: I need to search Arthur’s Magazine and First for Women, and find which was started first.

Action 1: Search[Arthur’s Magazine]

Observation 1: Arthur’s Magazine was an American literary periodical published in Philadelphia in the 19th century. Edited by Timothy Shay Arthur, it featured work by Edgar A. Poe, J.H. Ingraham, Sarah Josepha Hale, Thomas G. Spear, and others.[1][2] In May 1846 it was merged into Godey’s Lady’s Book.[3]

This trajectory is correct as it is reasonable to search for the first magazine provided in the question. It is also better to have simple searches corresponding to a single entity, making this the best action.

Thus the correctness score is 10

(other examples)

(failed trajectories)

(context)
## 附录 F 编程提示词

以下提示词展品保留英文原文。

### F.1 HumanEval function implementation example

Sample function signature:

[⬇](data:text/plain;base64,ZGVmIG1pblN1YkFycmF5U3VtKG51bXMpOgogICAgR2l2ZW4gYW4gYXJyYXkgb2YgaW50ZWdlcnMgbnVtcywKICAgIGZpbmQgdGhlIG1pbmltdW0gc3VtIG9mIGFueQogICAgbm9uLWVtcHR5IHN1Yi1hcnJheSBvZiBudW1zLgogICAgRXhhbXBsZQogICAgbWluU3ViQXJyYXlTdW0oWy0xLCAtMiwgLTNdKSA9PSAtNg==)

def minSubArraySum(nums):

Given an array of integers nums,

find the minimum sum of any

non-empty sub-array of nums.

Example

minSubArraySum([-1, -2, -3]) == -6

Sample function body implementation:

[⬇](data:text/plain;base64,ICAgIG1pbl9zdW0gPSBmbG9hdCgnaW5mJykKICAgIGZvciBpIGluIHJhbmdlKGxlbihudW1zKSk6CiAgICAgICAgY3VycmVudF9zdW0gPSAwCiAgICAgICAgZm9yIGogaW4gcmFuZ2UoaSwgbGVuKG51bXMpKToKICAgICAgICAgICAgY3VycmVudF9zdW0gKz0gbnVtc1tqXQogICAgICAgICAgICBpZiBjdXJyZW50X3N1bSA8IG1pbl9zdW06CiAgICAgICAgICAgICAgICBtaW5fc3VtID0gY3VycmVudF9zdW0KICAgIHJldHVybiBtaW5fc3Vt)

min_sum = float(’inf’)

for i in range(len(nums)):

current_sum = 0

for j in range(i, len(nums)):

current_sum += nums[j]

if current_sum < min_sum:

min_sum = current_sum

return min_sum

### F.2 Base Acting/Reasoning Prompt

You are an AI Python assistant. You will be given your previous implementation of a function, a series of unit tests results, and your self-reflection on your previous implementation. Write your full implementation (restate the function signature).

Example 1:

[previous impl]:

[⬇](data:text/plain;base64,ZGVmIGFkZChhOiBpbnQsIGI6IGludCkgLT4gaW50OgogICAgYGBHaXZlbiBpbnRlZ2VycyBhIGFuZCBiLAogICAgcmV0dXJuIHRoZSB0b3RhbCB2YWx1ZSBvZiBhIGFuZCBiLicnCiAgICByZXR1cm4gYSAtIGI=)

def add(a: int, b: int) -> int:

“Given integers a and b,

return the total value of a and b.”

return a - b

[unit test results from previous impl]:

Tested passed:

Tests failed:

assert add(1, 2) == 3 # output: -1

assert add(1, 2) == 4 # output: -1

[reflection on previous impl]:

The implementation failed the test cases where the input integers are 1 and 2. The issue arises because the code does not add the two integers together, but instead subtracts the second integer from the first. To fix this issue, we should change the operator from ‘-’ to ‘+’ in the return statement. This will ensure that the function returns the correct output for the given input.

[improved impl]:

[⬇](data:text/plain;base64,ZGVmIGFkZChhOiBpbnQsIGI6IGludCkgLT4gaW50OgogICAgYGAKICAgIEdpdmVuIGludGVnZXJzIGEgYW5kIGIsCiAgICByZXR1cm4gdGhlIHRvdGFsIHZhbHVlIG9mIGEgYW5kIGIuCiAgICAnJwogICAgcmV0dXJuIGEgKyBi)

def add(a: int, b: int) -> int:

“

Given integers a and b,

return the total value of a and b.

”

return a + b

### F.3 Reflection Prompt

You are a Python programming assistant. You will be given a function implementation and a series of unit test results. Your goal is to write a few sentences to explain why your implementation is wrong, as indicated by the tests. You will need this as guidance when you try again later. Only provide the few sentence description in your answer, not the implementation. You will be given a few examples by the user.

Example 1:

[previous impl]:

[⬇](data:text/plain;base64,ICAgIGRlZiBhZGQoYTogaW50LCBiOiBpbnQpIC0+IGludDoKICAgICAgICBgYAogICAgICAgIEdpdmVuIGludGVnZXJzIGEgYW5kIGIsCiAgICAgICAgcmV0dXJuIHRoZSB0b3RhbCB2YWx1ZSBvZiBhIGFuZCBiLgogICAgICAgICcnCiAgICByZXR1cm4gYSAtIGI=)

def add(a: int, b: int) -> int:

“

Given integers a and b,

return the total value of a and b.

”

return a - b

[unit test results from previous impl]:

Tested passed:

Tests failed:

assert add(1, 2) == 3 # output: -1

assert add(1, 2) == 4 # output: -1

[reflection on previous impl]:

The implementation failed the test cases where the input integers are 1 and 2. The issue arises because the code does not add the two integers together, but instead subtracts the second integer from the first. To fix this issue, we should change the operator from ‘-’ to ‘+’ in the return statement. This will ensure that the function returns the correct output for the given input.

### F.4 Test Case Generation Prompt

You are an AI coding assistant that can write unique, diverse, and intuitive unit tests for functions given the signature and docstring.

(input)
## 附录 G WebShop 提示词

以下提示词展品保留英文原文。
### G.1 Acting Prompt

Webshop

Instruction:

i would like a 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars

[Search]

Action: search[3 ounce bright citrus deodorant sensitive skin]

Observation:

[Back to Search]

Page 1 (Total results: 50)

[Next
]
[B078GWRC1J]

Bright Citrus Deodorant by Earth Mama — Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce

$10.99

[B078GTKVXY]

Ginger Fresh Deodorant by Earth Mama — Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce

$10.99

[B08KBVJ4XN]

Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack)

$15.95

Action: think[B078GWRC1J and B078GTKVXY are bright citrus deodorant less then 50 dollars. I can check B078GWRC1J first.]

Observation: OK.

Action: click[B078GWRC1J]

Observation:

[Back to Search]

[Prev]

scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]
size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]
Bright Citrus Deodorant by Earth Mama — Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce

Price: $10.99

Rating: N.A.

[Description]

[Features]

[Reviews]

[Buy Now]

Action: think[For 3 ounce bottle of bright citrus deodorant for sensitive skin, the item has options ‘bright citrus’ and ‘3 ounce (pack of 1)’ and seems good to buy.]

Observation: OK.

Action: click[bright citrus]

Observation: You have clicked bright citrus.

Action: click[3 ounce (pack of 1)]

Observation: You have clicked 3 ounce (pack of 1).

Action: click[Buy Now]

### G.2 Value Function Prompt

Given an item to purchase and a trajectory that aims to buy an item that exactly matches the specification, which corresponds to the ideal score of 1.0, analyze the following trajectory, then at the last line conclude, “Thus the correctness score is s”, where s is an integer from 1 to 10.

Here are some examples

Webshop

Instruction:

i am looking for dairy free and apple variety pack of chips, and price lower than 30.00 dollars

[Search]

Action: search[dairy free and apple variety pack of chips]

Observation:

[Back to Search]

Page 1 (Total results: 50)

[Next]

[B07HRFJWP8]

Enjoy Life Foods Soft Baked Ovals, Breakfast Bars, Nut Free Bars, Soy Free, Dairy Free, Non GMO, Gluten Free, Vegan, Variety Pack, 4 Boxes (20 Bars Total)

$100.0

[B01KMHY5PG]

Enjoy Life Soft Baked Chewy Bars, Variety Pack, Nut Free Bars, Soy Free, Dairy Free, Gluten Free, 6 Boxes (30 Total Bars)

$21.49

[B008D2X8C4]

Enjoy Life Lentil Chips Variety Pack, Dairy Free Chips, Soy Free, Nut Free, Non GMO, Vegan, Gluten Free, 24 Bags (0.8 oz)

$100.0

Action: think[The first two items are not what I want. The third item is the dairy free and apple variety pack of chips I want.]

Observation: OK.

Action: click[B008D2X8C4]

Observation:

[Back to Search]

[Prev]

flavor name [dill and sour cream][garlic & parmesan][light sea salt][margherita pizza][thai chili lime][variety pack]
size [0.8 ounce (pack of 24)][4 ounce (pack of 12)]

Price: $100.0

Rating: N.A.

[Description]

[Features]

[Reviews]

[Buy Now]

Action: think[The item has options ‘variety pack’ and ‘0.8 ounce (pack of 24)’ and seems good to buy.]

Observation: OK.

Action: click[variety pack]

Observation: You have clicked variety pack.

Action: click[0.8 ounce (pack of 24)]

Observation: You have clicked 0.8 ounce (pack of 24).

Action: click[Buy Now]

Reflection: In this attempt, I was unsuccessful. I accidentally bought a product that was $100, which is more than my budget of $30. Either way, the initial search results were not good. Next time, I will do search[“variety pack of chip”;] and then check if the results meet the dairy free and the $30 budget constraints. I will continue to refine my searches so that I can find more products.

Thus the correctness score is 5

(input)

### G.3 Reflection Prompt

You are an advanced reasoning agent that can improve based on self-reflection. You will be given a previous reasoning trial in which you were given access to a shopping website and a specific type of item to buy. You were given access to relevant context and an item to purchase. You were unsuccessful in buying the correct item either because you did not find an item meeting all of the required specifications or because you did not select the correct item. The ideal score is 1.0, and anything less is incorrect. In a few sentences, Diagnose a possible reason for failure and devise a new, concise, high-level plan that aims to mitigate the same failure. Use complete sentences.
Here are some examples:

Previous Trial
Instruction:
i am looking for dairy free and apple variety pack of chips, and price lower than 30.00 dollars
[Search]

Action: search[dairy free and apple variety pack of chips]
Observation:
[Back to Search]
Page 1 (Total results: 50)
[Next >>]
[B07HRFJWP8]
Enjoy Life Foods Soft Baked Ovals, Breakfast Bars, Nut Free Bars, Soy Free, Dairy Free, Non GMO, Gluten Free, Vegan, Variety Pack, 4 Boxes (20 Bars Total)
$100.0
[B01KMHY5PG]
Enjoy Life Soft Baked Chewy Bars, Variety Pack, Nut Free Bars, Soy Free, Dairy Free, Gluten Free, 6 Boxes (30 Total Bars)
$21.49
[B008D2X8C4]
Enjoy Life Lentil Chips Variety Pack, Dairy Free Chips, Soy Free, Nut Free, Non GMO, Vegan, Gluten Free, 24 Bags (0.8 oz)
$100.0

Action: think[The first two items are not what I want. The third item is the dairy free and apple variety pack of chips I want.]
Observation: OK.

Action: click[B008D2X8C4]
Observation:
[Back to Search]
[<< Prev]
flavor name [dill and sour cream][garlic & parmesan][light sea salt][margherita pizza][thai chili lime][variety pack]
size [0.8 ounce (pack of 24)][4 ounce (pack of 12)]
Price: $100.0
Rating: N.A.
[Description]
[Features]
[Reviews]
[Buy Now]

Action: think[The item has options ‘variety pack’ and ‘0.8 ounce (pack of 24)’ and seems good to buy.]
Observation: OK.

Action: click[variety pack]
Observation: You have clicked variety pack.

Action: click[0.8 ounce (pack of 24)]
Observation: You have clicked 0.8 ounce (pack of 24).

Action: click[Buy Now]

STATUS: FAIL

Reflection: In this attempt, I was unsuccessful. I accidentally bought a product that was $100, which is more than my budget of $30. Either way, the initial search results were not good. Next time, I will do search[“variety pack of chips”] and then check if the results meet the dairy free and the $30 budget constraints. I will continue to refine my searches so that I can find more products.

Previous Trial
Instruction:
i need gluten free vegetarian smoked peppered bacon - 4 ounce (pack of 2), and price lower than 40.00 dollars
[Search]

Action: search[gluten free vegetarian smoked peppered bacon 4 ounce pack of 2]
Observation:
[Back to Search]
Page 1 (Total results: 50)
[Next >>]
[B06Y96MXJV]
Smoked Bacon Sea Salt 3-Pack: Smoked Bacon Chipotle, Smoked Bacon and Onion, Smoked Peppered Bacon - All-Natural Sea Salts Slowly Smoked Over Alderwood - No Gluten, No MSG, Non-GMO (12 total oz.)
$29.99
[B06Y96N1KG]
Spicy Hot Pepper Sea Salt 3-Pack: Ghost Pepper, Jalapeno, Habanero - All Natural, Delicious Blends of Peppers & Sea Salt - Gluten-Free, Kosher, No MSG, Non-GMO (12 total oz.)
$29.99
[B07GJTKYJQ]
Louisville Vegan Jerky - 5 Flavor Variety Pack, Non-GMO Soy Protein, Gluten-Free (Black Pepper, Buffalo Dill, Pepperoni, Maple Bacon, and Carolina BBQ, 3 Ounces)
$42.99

Action: think[The first two items are not what I want. The third item is not what I want, but it is the closest one.]
Observation: OK.

Action: click[B07GJTKYJQ]
Observation:
[Back to Search]
[<< Prev]
Louisville Vegan Jerky - 5 Flavor Variety Pack, Non-GMO Soy Protein, Gluten-Free (Black Pepper, Buffalo Dill, Pepperoni, Maple Bacon, and Carolina BBQ, 3 Ounces)
Price: $42.99
Rating: N.A.
[Description]
[Features]
[Reviews]
[Buy Now]

Action: think[The price is too high and it is not what I want.]
Observation: OK.

Action: click[<< Prev]
Observation:
[Back to Search]
Page 1 (Total results: 50)
[Next >>]
[B06Y96MXJV]
Smoked Bacon Sea Salt 3-Pack: Smoked Bacon Chipotle, Smoked Bacon and Onion, Smoked Peppered Bacon - All-Natural Sea Salts Slowly Smoked Over Alderwood - No Gluten, No MSG, Non-GMO (12 total oz.)
29.99
[B06Y96N1KG]
Spicy Hot Pepper Sea Salt 3-Pack: Ghost Pepper, Jalapeno, Habanero - All Natural, Delicious Blends of Peppers & Sea Salt - Gluten-Free, Kosher, No MSG, Non-GMO (12 total oz.)
29.99
[B07GJTKYJQ]
Louisville Vegan Jerky - 5 Flavor Variety Pack, Non-GMO Soy Protein, Gluten-Free (Black Pepper, Buffalo Dill, Pepperoni, Maple Bacon, and Carolina BBQ, 3 Ounces)
42.99

Action: think[The first two items are not what I want.]
Observation: OK.

Action: click[Next >>]
Observation: Invalid action!

Action: think[I need to refine my search.]
Observation: OK.

Action: click[<< Back to Search]
Observation: Invalid action!

Action: click[Back to Search]

STATUS: FAIL

Reflection: In this attempt, I was unsuccessful. The initial search results were not the products that I was looking for. Next time, I will do search[“vegetarian bacon”] for a broader search. I will check that the new results will fulfill the gluten free and 4 ounce pack of 2 constraints. I will continue to refine my searches so that I can find more products.

Previous trial:
trajectory
Reflection:”’
