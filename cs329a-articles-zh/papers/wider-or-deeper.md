---
title: "更宽还是更深？用自适应分支树搜索扩展 LLM 推理时计算"
title_en: "Wider or Deeper? Scaling LLM Inference-Time Compute with Adaptive Branching Tree Search"
arxiv: 2503.04412
source: https://arxiv.org/abs/2503.04412
crawled: 2026-09-23
translated: 2026-09-23
---

# 更宽还是更深？用自适应分支树搜索扩展 LLM 推理时计算

> 原文：[Wider or Deeper? Scaling LLM Inference-Time Compute with Adaptive Branching Tree Search](https://arxiv.org/abs/2503.04412) · Stanford CS329A 指定阅读

Yuichi Inoue
††感谢：贡献相同，详见作者贡献。
  
Kou Misaki11footnotemark: 
1
  
Yuki Imajuku
  
So Kuroki
  
Taishi Nakamura
  
Takuya Akiba
所属机构：Sakana AI, Japan
所属机构：{y.inoue, takiba}@sakana.ai

###### 摘要

近期进展表明，增加推理时计算可以显著提升大型语言模型（LLM）的推理能力。尽管重复采样（即生成多个候选输出）是一种高度有效的策略，它并未利用外部反馈信号进行精炼，而这类信号在编程等真实任务中往往可得。在本工作中，我们提出*自适应分支蒙特卡洛树搜索（Adaptive Branching Monte Carlo Tree Search，AB-MCTS）*，一个新颖的推理时框架，以有原则的多轮探索与利用来推广重复采样。在搜索树的每个节点上，AB-MCTS 依据外部反馈信号，动态决定是通过扩展新的候选回答「变得更宽」，还是通过重访已有回答「变得更深」。我们在复杂编程与工程任务上用前沿模型评估了该方法。实验结果表明，AB-MCTS 胜过重复采样与标准 MCTS，凸显了把 LLM 的回答多样性与多轮解精炼相结合对于有效推理时扩展的重要性。代码见：<https://github.com/SakanaAI/treequest>。

## 1 引言

近期工作表明，*推理时扩展*（即在推理时分配更多计算）可以显著提升大型语言模型（LLM）在复杂任务上的表现。如第 2 节所述，现有的推理时扩展方法大致分为三类：(1) 后训练微调；(2) 奖励引导的思维链（CoT）生成；(3) 多答案生成。在本文中，我们聚焦第三类。多答案生成方法以非零温度反复查询 LLM 以产出一组候选输出，然后选出最有希望的一个。该方法即时地增强 LLM 的问题求解能力，无需进一步训练（Li et al., 2022；Wang et al., 2023；Brown et al., 2024；Madaan et al., 2024；Shinn et al., 2024；Li et al., 2025；Tang et al., 2024；Lee et al., 2025；Zhou et al., 2024；Antoniades et al., 2025；Ma et al., 2024）。因为它与前两族正交，所以可以与它们无缝结合。

该类别中最广泛成功的方法是*重复采样*，包括 best-of-$n$ 采样、多数投票与自洽性等技术（Wang et al., 2023；Brown et al., 2024；Liang et al., 2024）。在重复采样中，一个非零温度的 LLM 从相同初始提示独立生成多个候选输出，然后通常以简单启发式选出最终解。这一范式已在具有挑战性的基准上被证明有效，包括编程竞赛（Li et al., 2022；Brown et al., 2024）与 ARC-AGI（Greenblatt, 2024）。该策略利用了 LLM 生成所呈现的*多样而广阔的输出空间*，采样更多回答会提高其中出现高质量回答的概率。重复采样的实证成功凸显出：驾驭这种多样性是有效推理时扩展的核心。

然而，重复采样只关注*探索*，缺乏显式的*利用*机制。在某些真实场景中，可以获得对候选解的外部反馈。例如在编程任务中，可以运行测试来评估生成程序的正确性并收集改进反馈（Madaan et al., 2024；Shinn et al., 2024；Jain et al., 2025）。在这类场景中，自然的选择是挑选有希望的解并基于可用反馈进行精炼，而仅靠重复采样无法有效做到。

已有若干方法（Li et al., 2025；Tang et al., 2024；Zhou et al., 2024；Antoniades et al., 2025；Ma et al., 2024；Hao et al., 2023）被提出用于这类多轮设定中的探索与利用，但大多数设计于推理时扩展的力量被充分认识之前。因此，这些方法使用固定的「宽度」，即把单个提示生成的答案数量当作固定超参数。例如，基于标准蒙特卡洛树搜索（MCTS）的方法把固定分支因子（即每个状态的子节点数）作为超参数（Zhou et al., 2024；Antoniades et al., 2025；Ma et al., 2024；Hao et al., 2023）。正如重复采样的成功所表明的，有效的推理时扩展需要利用多样而广阔的输出空间，这为「固定宽度阻碍扩展」提供了充分的证据。

图 1：
AB-MCTS 与基线的直观比较。与纯宽（重复采样）、纯深（顺序精炼）或固定宽度（标准 MCTS）的基线不同，AB-MCTS 动态决定向外分支还是向下深挖，统一了两个搜索方向。

在本工作中，我们提出*自适应分支蒙特卡洛树搜索（AB-MCTS）*，一个新颖的推理时框架，以多轮探索与利用推广重复采样（图 1）。主要的技术挑战是把无界分支引入 MCTS。与传统 MCTS 不同，AB-MCTS 不把宽度固定为静态超参数。取而代之，在搜索树的每个节点上，AB-MCTS 利用外部反馈信号，自适应地决定是生成新的候选回答以探索（「变得更宽」），还是精炼已有回答以利用（「变得更深」）。在底层，我们通过贝叶斯后验更新形式化这一决策过程，确保每次扩展都以有原则的方式平衡探索与利用。这一设计自然地扩展了重复采样，让我们在必要时能够驾驭 LLM 多样而广阔的输出空间。因此，我们的框架在 LLM 推理时扩展的语境下提供了一个平衡探索与利用的强大机制。

我们在复杂编程与机器学习工程基准（Li et al., 2022；Chan et al., 2025）以及 ARC-AGI（Chollet, 2019）上评估了 AB-MCTS，使用 GPT-4o（OpenAI, 2024a）与 DeepSeek-V3（DeepSeek-AI, 2024）等前沿模型，场景是允许对每个任务实例进行多次生成调用来扩展推理时计算。在相同计算预算下，AB-MCTS 取得了优于重复采样与标准 MCTS 等先前方法的结果。

贡献。
① 我们强调了把无界分支有效纳入树搜索的挑战。这对于把 LLM 多样而广阔的输出空间（推理时扩展的基石）的力量与解精炼相结合至关重要。
② 为应对这一挑战，我们提出 AB-MCTS，系统地决定「变得更宽」还是「变得更深」。我们给出基于不同原理的两个变体 AB-MCTS-M 与 AB-MCTS-A，各有不同的取舍。
③ 在使用前沿模型与真实世界复杂任务的实际设定中，我们表明 AB-MCTS 胜过现有方法。

## 2 相关工作

通过后训练微调的推理时扩展。
近期的后训练工作，以 OpenAI o1/o3（OpenAI, 2024b；OpenAI, 2025a）为代表，使用强化学习或监督 CoT 微调来深化 LLM 推理并提升单答案质量（OpenAI, 2024b；OpenAI, 2025a；DeepSeek-AI, 2025；Ye et al., 2025；Muennighoff et al., 2025；Kimi Team, 2025）。我们的方法则生成大量候选并用外部反馈精炼，追求一个互补的目标。

通过奖励引导 CoT 的推理时扩展。
奖励引导 CoT 通过一次搜索一步（通常是一个句子）来扩展推理（Yao et al., 2024；Snell et al., 2025；Chen et al., 2024；Gao et al., 2025；Zhao et al., 2024；Qi et al., 2025；Guan et al., 2025；Wu et al., 2025；Zhang et al., 2024）。它主要用于数学任务，旨在提升单答案质量，因此与我们的多答案生成方法正交。

通过多答案生成的推理时扩展。
自社区认识到推理时扩展的力量以来，被广泛研究的策略是重复采样：模型生成大量候选答案并选出最佳（Li et al., 2022；Wang et al., 2023；Brown et al., 2024；Schaeffer et al., 2025）。尽管经验上强大且被广泛使用，重复采样并未利用外部反馈来精炼候选，仍有明显的改进空间（Madaan et al., 2024；Shinn et al., 2024）。在大规模推理时计算时代之前，曾提出多种面向较小规模的任务特定策略；例子包括由 LLM 引导的树扩展（Li et al., 2025）与贝叶斯方法（Tang et al., 2024）。LATS（Zhou et al., 2024）、RAP（Hao et al., 2023）、SWE-Search（Antoniades et al., 2025）与 RepoUnderstander（Ma et al., 2024）把 LLM 与 MCTS 结合，主要面向序列决策。在此语境下，节点表示状态、边表示动作，可能涉及与环境的交互。LATS 利用 API 调用与代码执行作为动作来求解任务。RAP 处理逐步求解方块移动谜题与数学应用题。SWE-Search 探索诸如搜索、编辑、运行测试的动作序列以解决软件仓库中的 issue。RepoUnderstander 用 MCTS 在仓库知识图谱上探索。LATS 在编程任务上的应用（Zhou et al., 2024, Section 5.2）与本文多答案生成的语境一致，对应我们实验中所称的「标准 MCTS」。

MCTS 中的渐进加宽。
渐进加宽（Progressive Widening，PW）（Coulom, 2007；Couëtoux et al., 2011）是一种经典技术，逐渐增加每个节点考虑的动作数。它为动作唯一且未尝试走法没有侧信息的博弈而设计，依赖访问计数启发式。作为 PW 的补充，Sokota et al. (2021) 提出「抽象精炼」，用递减的相似度阈值对相似后继分组，并在随机域的相同模拟预算下显示出对 PW 的优势。我们的方法不同之处在于：新分支是从同一个 LLM 采样的。这种生成的同质性允许用一条有原则的统计规则在加宽与加深之间选择。

## 3 方法

### 3.1 预备知识

首先，我们介绍设定与记号，更详细的阐述见附录 A.1。我们考虑这样的设定：一个 LLM，表示为函数 $f_{\rm LLM}$，接收一个文本提示 $t_{\rm in}$，其中包含 (1) 任务指令（可选地带少样本示例），和/或 (2) 先前生成的输出及外部反馈，并生成回答 $t_{\rm out}=f_{\rm LLM}(t_{\rm in})$。随后，打分函数 $R$ 评估回答 $t_{\rm out}$ 产生分数 $r=R(t_{\rm out})$，分数越高表现越好。我们通常假设分数 $r$ 归一化到 $[0,1]$ 区间，但我们的框架也允许任意范围。我们的目标是在推理时对 LLM 的有限调用次数下，找到取得高分 $r$ 的输出 $t_{\rm out}$。这类任务出现于例如代码生成，其输出的正确性或质量可以量化；例如 $R$ 可以执行生成的代码并返回通过的测试用例比例。在某些情况下，真实打分器可能不可访问（如隐藏测试用例），因此我们假设在搜索期间可以访问某个代理或部分评估器 $R$，例如公开测试评估器。我们旨在利用该评估器来引导对更优解的高效搜索。

图 2：混合模型版 AB-MCTS（AB-MCTS-M）的示例树结构与分数后验预测分布。此处 $a_{1}$ 引出了一组分数较高的子节点，使分布在较大的 $r$ 处出现峰值。随着收集的子样本增多，分布的方差减小。

### 3.2 自适应分支 MCTS

面向 LLM 答案生成的 MCTS。
我们通过构建搜索树 $T$ 来执行答案搜索，其中每个非根节点 $N$ 关联一个 LLM 对给定任务生成的答案。我们的目标是构建 $T$，使其包含分数尽可能高的答案。

为此，我们采用 MCTS，迭代式地表述如下。从单个根节点出发，我们执行 $n_{\text{nodes}}$ 次迭代，每次添加一个新节点，共得到 $1+n_{\text{nodes}}$ 个节点。每次迭代有三个步骤：
(1) 选择：选择一个待扩展的节点 $N$；
(2) 扩展：通过从节点 $N$ 生成一个新答案来扩展 $N$，创建新子节点 $N_{\text{new}}$ 并将其挂到 $N$ 上。具体而言，若 $N$ 是根节点，新答案直接从任务提示生成；若 $N$ 非根，新答案利用外部反馈精炼与 $N$ 关联的答案；以及
(3) 分数回传：把 $N_{\text{new}}$ 的分数向树 $T$ 的根方向传播。我们在所提方法中采用不同的回传规则（见第 3.3 与 3.4 节）。
在我们的设定中，不需要单独的 rollout，因为每个节点的分数 $r$ 一旦生成输出即可直接评估。经过 $n_{\text{nodes}}$ 次迭代后，我们依据选定准则选出最佳节点。

在标准 MCTS 中，只有叶节点会被选择和扩展（即每个节点至多被扩展一次），且扩展会加入固定数量的子节点。然而，由于对非零温度 LLM 的每次查询都可能从同一提示产生不同输出，分支因子理论上是无限的。为容纳这种无界分支，我们放宽标准 MCTS 的约束，允许选择与扩展非叶节点。此外，近期研究（Brown et al., 2024）表明，从同一提示以非零温度抽取大量输出可以提升性能。允许无界分支使我们能充分利用这些多样样本，而限制分支因子可能错过正确的答案生成、损害整体性能。

通过 GEN 节点实现自适应分支。
为充分发挥无界分支带来的潜在性能提升，与标准 MCTS 不同，我们允许已被扩展过一次的节点再次被扩展并进一步分支。为显式表示「生成新子节点」这一动作，我们引入 *GEN 节点*。每个节点 $N$（包括迭代期间新扩展的节点）都有一个 GEN 节点作为子节点。当父节点为 $N$ 的 GEN 节点在选择步骤中被选中时，我们通过添加一个新子节点来扩展 $N$。算法 1 概述了这一方法，称为*自适应分支蒙特卡洛树搜索*（*AB-MCTS*）。

算法 1　自适应分支 MCTS

1:

function AB-MCTS($n_{\rm nodes}$)

2:
　
$T\leftarrow$ InitializeTree( )

3:
　
for $n=1,\dots,n_{\rm nodes}$ do

4:
　　
$N\leftarrow$ SelectExpansionTarget($T$) $\triangleright$ 步骤 1. 选择扩展目标

5:
　　
$N_{\text{new}}\leftarrow$ Expand($N$, $T$) $\triangleright$ 步骤 2. 扩展所选节点以生成子节点

6:
　　
ScoreBackUp($N_{\text{new}}$, $T$) $\triangleright$ 步骤 3. 从生成节点回传分数

7:
　
return SelectBest($T$)

8:

function SelectExpansionTarget($T$)

9:
　
$N\leftarrow$ GetRoot($T$)

10:
　
while not IsLeaf($N$) do

11:
　　
$N_{\text{next}}\leftarrow$ SelectChild($N$, $T$) $\triangleright$ 详见第 3.3 与 3.4 节

12:
　　
if IsGenNode($N_{\text{next}}$) then $\triangleright$ 若选中 GEN 节点，则从该节点分支

13:
　　　
break

14:
　　
$N\leftarrow N_{\text{next}}$

15:
　
return $N$

我们剩下的唯一组件是选择策略，包括何时选择 GEN 节点。我们提出两个采用不同选择策略的算法：*AB-MCTS-M*（Mixed model，混合模型）与 *AB-MCTS-A*（node Aggregation，节点聚合）。二者都遵循算法 1 的整体流程，并使用 Thompson 采样来平衡探索与利用。

UCT 分数不适用于我们的 AB-MCTS，因为 GEN 节点使该问题与 UCT 所面向的标准多臂老虎机问题有本质区别。在标准 MCTS 中，摇臂（分支）是静态的。相比之下，AB-MCTS 中的 GEN 节点会动态生成新的摇臂。这种摇臂即时生成的问题设定阻碍了 UCT 的直接应用。因此我们采用贝叶斯概率模型。这使我们能基于后验分布进行 Thompson 采样，并免去复杂的 UCB 式置信界分析。

用于节点选择的 Thompson 采样。
在我们提出的方法中，我们采用带 Thompson 采样的贝叶斯方法进行节点选择。之所以采用 Thompson 采样，是因为 GEN 节点没有子节点，无法计算其 UCT 分数。此外，Thompson 采样具有允许并行节点扩展的优势。当评估节点分数耗时较长时（如 MLE-Bench 的情形，见附录 B.1 了解 MLE-Bench 细节），这尤其有益。

具体而言，在算法 1 第 11 行的 SelectChild 步骤中，我们用 Thompson 采样决定是扩展 GEN 节点，还是在节点 $N$ 的既有子节点中选择。设 $N$ 为一个具有候选动作的节点

$$
A_{N}=\{a_{0},a_{1},\dots,a_{n_{\rm child}}\},
$$

其中动作 $a_{0}$ 对应选择 GEN 节点，$a_{1},\dots,a_{n_{\rm child}}$ 对应选择已存在的子节点。设 $P_{N}(r\mid a_{i})$ 为：若我们在节点 $N$ 选择动作 $a_{i}$，最终扩展出的新节点（算法 1 第 5 行的 $N_{\text{new}}$）分数 $r$ 的后验预测分布。则 Thompson 采样按如下进行：

1. 为节点 $N$ 的每个动作 $a_{j}$ 计算 $P_{N}(r\mid a_{j})$。
2. 为每个动作 $a_{j}$ 从 $P_{N}(r\mid a_{j})$ 抽取分数 $r_{N_{\text{new}},a_{j}}$。
3. 选择 $\hat{a}=\arg\max_{a_{j}\in A_{N}}r_{N_{\text{new}},a_{j}}$。

这一三步流程对应一次 SelectChild 调用。

关键问题是如何执行步骤 1，即如何为所有 $a_{j}$（尤其 $j=0$，即 GEN 节点）建模并计算 $P_{N}(r\mid a_{j})$。我们用两种策略解决：混合贝叶斯模型（*AB-MCTS-M*）与节点聚合方法（*AB-MCTS-A*）。两种情况都用贝叶斯后验预测对分数概率分布建模，但采用不同的统计模型。

### 3.3 AB-MCTS-M：混合模型的自适应分支 MCTS

为建模 $P_{N}(r\mid a_{j})$，我们在每个节点 $N$ 上分别拟合一个节点特定的混合模型。也就是说，每当算法 1 中的 SelectChild 被调用时，我们为每个 $N$ 单独拟合一个模型。把 $r_{N_{\text{new}},a_{j}}\sim P_{N}(r\mid a_{j})$ 记为在 $N$ 选择动作 $a_{j}$ 时最终扩展节点 $N_{\text{new}}$ 的分数，我们的混合模型由下式给出：

$$
\begin{gathered}r_{N_{\text{new}},a_{j}}=\alpha_{j}+\sigma_{y}\epsilon_{N_{\text{new}}},\quad\alpha_{j}=\mu_{\alpha}+\sigma_{\alpha}\epsilon_{j},\\ \epsilon_{N_{\text{new}}}\sim\mathcal{N}(0,1),\quad\epsilon_{j}\sim\mathcal{N}(0,1),\end{gathered} \tag{1}
$$

这里，$\alpha_{j}$ 是刻画 $N_{j}$ 处基础解质量的「组级」截距，而 $\sigma_{y}\epsilon_{N_{\text{new}}}$ 表示逐实例噪声。为拟合该模型，我们对超参数（$\mu_{\alpha}$、$\sigma_{\alpha}$、$\sigma_{y}$）设置先验，并用马尔可夫链蒙特卡洛（MCMC）从其后验分布中采样。GEN 节点（动作 $a_{0}$）被视为一个新引入的组，自身没有直接观测。不过，其组级截距 $\alpha_{0}$ 不是仅从先验推断，而是从由其他观测数据告知的 $\mu_{\alpha}$ 与 $\sigma_{\alpha}$ 的后验分布推断。我们假设即使在多个精炼阶段之后，节点 $N_{j}$ 处答案的质量仍由该共享参数刻画（更多细节见附录 A.3.2）。

算法概要。
为建模 $P_{N}(r\mid a_{j})$，AB-MCTS-M 把 $N_{j}$ 之下的每棵子树（记作 $T_{\text{sub}}(N_{j})$）指派为一个独立的组 $j$（示例子树见图 2）。混合模型利用这些组的观测分数，计算从每组生成的新节点的期望分数的后验预测分布（示意见图 2）。我们用算得的后验预测从所有组（GEN 节点与各 $T_{\text{sub}}(N_{j})$）采样分数。若 GEN 节点的采样分数最高，我们调用 $f_{\text{LLM}}$ 生成一个新子节点。否则，我们选择分数最高的子节点 $N_{j}$ 并继续采样步骤。

分数回传机制。
当一个新节点 $N$ 被创建时，其观测分数被加入 $N$ 及其祖先的历史。这份累积记录用于更新混合模型中的后验分布。观测分数不回传到 GEN 节点，但会通过混合模型中的共享参数间接影响 GEN 节点的分数概率分布（详细演练见附录 A.5）。

### 3.4 AB-MCTS-A：节点聚合的自适应分支 MCTS

在 AB-MCTS-M 中，在 $N$ 的选择步骤中，我们使用通过共享模型参数在组间共享统计强度的混合模型。相比之下，AB-MCTS-A 本着与标准基于 UCT 的 MCTS 相同的精神设计，不同动作之间没有共享模型参数。这一设计简化了统计建模，并使计算相对 AB-MCTS-M 更轻量。

主要问题是如何把分数回传到 GEN 节点。由于生成的节点并不作为子节点挂在 GEN 节点之下，分数的回传难以定义。在此，我们在与所有 GEN 节点相同的树层级引入一个 *CONT 节点*（见图 3）。直观上，CONT 节点表示「从节点 $N$ 的当前答案继续精炼」这一动作，而非生成新节点。通过显式分离这两个动作——生成新答案（GEN）与精炼既有答案（CONT）——我们为分数传播创建了清晰的路径。具体而言，被扩展节点的分数先回传到 GEN 节点，而由于 GEN 节点的所有祖先要么是带 LLM 答案的节点、要么是 CONT 节点，分数随后不会穿过其他 GEN 节点传播（示例树见图 3）。

图 3：AB-MCTS-A 的示例树结构。所有子节点聚合在一个 CONT 节点之下，而 GEN 节点没有子节点。

算法概要。
AB-MCTS-A 把所有子节点聚合到单个 CONT 节点之下，该节点表示来自既有子节点的精炼（见图 3）。我们在贝叶斯框架下对每个节点的分数概率建模，并对后验预测执行 Thompson 采样，以决定生成新子节点（GEN）还是精炼既有子节点（CONT）。与 AB-MCTS-M 不同，我们在不同的节点概率分布之间不使用共享参数。

为建模 $P_{N}(r\mid a_{j})$，我们使用带共轭先验的指数族分布，从而可以进行解析且高效的后验更新。我们采用两种变体：

1. AB-MCTS-A（Gaussian），对无界分数使用 normal-inverse-$\chi^{2}$ 先验：$P_{N}(r\mid a_{j})=p(r\mid\{r_{k}\}_{k=1}^{K})=\mathcal{N}(r\mid\hat{m},\tfrac{\sigma^{2}}{\hat{\kappa}})\chi^{-2}(\sigma^{2}\mid\hat{\nu},\hat{\tau}^{2})$；以及
2. AB-MCTS-A（Beta），对 $[0,1]$ 内的分数使用 Beta 先验：$P_{N}(r\mid a_{j})=p(r\mid\{r_{k}\}_{k=1}^{K})=B(r\mid\hat{\alpha},\hat{\beta})$，

其中 $r_{k}$ 表示回传到节点 $N_{j}$（GEN 节点、CONT 节点或 LLM 生成的子节点；示例树见图 3）的分数，$\hat{m},\hat{\kappa},\hat{\nu},\hat{\tau},\hat{\alpha},\hat{\beta}$ 由观测分数 $r_{k}$ 确定，并随这些分数被回传而更新。详细的参数更新规则见附录 A.4。

分数回传机制。
在分数回传操作中，被扩展节点的分数回传到引发该扩展的 GEN 节点及该 GEN 节点的祖先（详细演练见附录 A.5）。从图 3 可以看到，GEN 节点的祖先只包括生成节点与 CONT 节点，因此分数只从通过选择该 GEN 节点而创建的节点回传到该 GEN 节点。回传的分数用于更新先验概率分布参数。

## 4 实验

### 4.1 实验设置

基准。
我们在四个需要复杂问题求解的多样基准上评估 AB-MCTS：LiveCodeBench（Jain et al., 2025）、CodeContest（Li et al., 2022）、ARC-AGI（Chollet, 2019）与 MLE-Bench（Chan et al., 2025）。LiveCodeBench 与 CodeContest 由竞赛编程题组成，要求数学与算法推理。ARC-AGI 涉及从视觉模式中抽象出共同变换规则并将其实现为代码。MLE-Bench 源自 Kaggle 竞赛，涉及构建并优化机器学习模型，以按各竞赛的评估指标取得高分。对所有这些基准，LLM 生成 Python 代码来求解每个任务，且外部反馈（如测试用例结果、验证分数）可用于引导搜索。基准的更多细节见附录 B.1。

模型。
我们使用 GPT-4o（gpt-4o-2024-08-06）（OpenAI, 2024a）与 DeepSeek-V3（deepseek-chat）（DeepSeek-AI, 2024）进行实验。每个 LLM 在单次 API 调用中生成完整解。我们把生成预算定义为最大 API 调用次数并设为 $2^{7}=128$。温度遵循 Brown et al. (2024) 对 GPT-4o 设为 0.6，对 DeepSeek-V3 遵循官方文档设为 1.0。

基线。
我们将 AB-MCTS 与三种代表性方法对比。(1) 重复采样（Best-of-$n$）（Li et al., 2022；Brown et al., 2024；Lightman et al., 2024）从单个 LLM 提示独立生成至多 $n$ 个候选解，是编程任务上简单而有竞争力的基线。(2) 顺序精炼（Madaan et al., 2024）通过用模型自身的输出与反馈重新提示 LLM，迭代地改进每个解。(3) 标准 MCTS 遵循 LATS（Zhou et al., 2024, Section 5.2）的配置（另见附录 C.8）。每次扩展加入五个子节点，搜索进行到达到 $2^{7}$ 个节点为止，最后一次扩展只创建三个节点以精确满足该上限。AB-MCTS 的超参数总结于附录 B.2。

表 1：
AB-MCTS 与基线在各基准与模型上的性能。
本表把 AB-MCTS 与基线方法进行比较。评估在 LiveCodeBench、CodeContest 与 ARC-AGI 上使用 GPT-4o 与 DeepSeek-V3、最大生成预算（$2^{7}$）进行。每项给出性能分数（越高越好）及对应排名（括号内，第 1 为最佳）。「Avg. Rank」列为所有设定下的平均排名。

|  | LiveCodeBench | | CodeContest | | ARC-AGI | |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 方法 | GPT-4o | DeepSeek-V3 | GPT-4o | DeepSeek-V3 | GPT-4o | DeepSeek-V3 | 平均排名 |
| 重复采样 | 37.8 $\pm$ 0.5 (4) | 40.7 $\pm$ 1.9 (6) | 37.9 $\pm$ 0.3 (4) | 43.2 $\pm$ 0.9 (5) | 15.0 $\pm$ 1.0 (1) | 18.6 $\pm$ 1.0 (1) | 3.5 |
| 顺序精炼 | 37.8 $\pm$ 2.4 (4) | 41.6 $\pm$ 0.6 (5) | 30.1 $\pm$ 0.3 (6) | 41.6 $\pm$ 0.9 (6) | 8.7 $\pm$ 0.9 (6) | 10.0 $\pm$ 0.6 (6) | 5.5 |
| 标准 MCTS | 36.7 $\pm$ 1.0 (6) | 43.2 $\pm$ 2.1 (1) | 37.5 $\pm$ 0.0 (5) | 43.8 $\pm$ 0.9 (3) | 9.0 $\pm$ 1.5 (5) | 14.0 $\pm$ 1.5 (5) | 4.2 |
| AB-MCTS-M | 38.9 $\pm$ 1.9 (2) | 43.0 $\pm$ 1.5 (2) | 40.6 $\pm$ 1.0 (1) | 44.6 $\pm$ 0.9 (2) | 12.3 $\pm$ 1.2 (4) | 16.0 $\pm$ 1.0 (3) | 2.3 |
| AB-MCTS-A (Gaussian) | 39.1 $\pm$ 1.9 (1) | 42.5 $\pm$ 1.5 (3) | 40.2 $\pm$ 1.7 (3) | 43.4 $\pm$ 0.9 (4) | 13.0 $\pm$ 3.6 (3) | 18.3 $\pm$ 0.6 (2) | 2.7 |
| AB-MCTS-A (Beta) | 38.7 $\pm$ 1.2 (3) | 42.3 $\pm$ 0.8 (4) | 40.4 $\pm$ 0.3 (2) | 44.8 $\pm$ 0.6 (1) | 14.0 $\pm$ 2.1 (2) | 16.6 $\pm$ 0.6 (4) | 2.7 |

表 2：
MLE-Bench 任务上的性能。
AB-MCTS-M 展现出稳健的性能，在多样的机器学习任务上取得最佳平均排名。

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| 方法 | Nomad2018 | Spooky. | Pizza. | Avg. |
| 重复采样 | 0.065 (3) | 0.47 (4) | 0.72 (2) | 3.0 |
| 顺序精炼 | 0.059 (1) | 0.46 (3) | 0.62 (3) | 2.3 |
| 标准 MCTS | 0.076 (4) | 0.45 (2) | 0.60 (4) | 3.3 |
| AB-MCTS-M | 0.060 (2) | 0.38 (1) | 0.72 (1) | 1.3 |

### 4.2 结果

如表 1 与表 2 所详述，我们的全面评估表明 AB-MCTS 是在各基准与各 LLM 上一致优越的方法，取得最高平均排名并胜过既有基线。这一持续的成功源于 AB-MCTS 的独特能力：通过针对每个问题的不同需求精确平衡探索与利用，动态调整其搜索策略——这种适应性在基线方法中基本缺失。下面按基准详述这些结果，随后分析 AB-MCTS 的搜索行为。

![Refer to caption](2503.04412v5/figure1_gpt4o.png)

图 4：
在 LiveCodeBench、CodeContest 与 ARC-AGI 上的性能比较。
我们使用 GPT-4o 比较六种方法，绘制成功率随生成预算的变化。插图给出最大生成预算（$2^{7}$）下性能的细致视图；展示了平均成功率、其 95% 置信区间以及各次独立运行的结果。生成预算为 $2^{0}$ 时的方差来自以非零温度独立进行每次实验。
更大预算的 ARC-AGI 实验见图 6。

![Refer to caption](2503.04412v5/figure2_gpt4o_3.png)

图 5：
按搜索树形状与性能比较算法。
每个点表示给定算法在特定生成预算下、相对平均树形状的性能。横轴为平均深度与平均宽度之比的对数。平均宽度是每个深度的平均节点数。横轴值越大表示搜索越深，越小表示搜索越宽。

LiveCodeBench 与 CodeContest。
图 5（左与中）报告了 GPT-4o 在 LiveCodeBench 与 CodeContest 上成功率（Pass@1）随生成预算的变化。正如预期，所有方法的表现都随计算预算增加而提升。在两个基准上，AB-MCTS 算法总体上胜过基线方法。值得注意的是，在 LiveCodeBench（图 5 左）上，AB-MCTS 在小到 $2^{3}$ 的预算下就开始领先基线。在 CodeContest（图 5 中）上，AB-MCTS 在 $2^{5}$ 及以上的更大预算下展现出优于基线的性能。附录图 10 表明，虽然标准 MCTS 在 DeepSeek-V3 上相对 GPT-4o 表现较好，但我们提出的方法在 LiveCodeBench 上取得相当的成功率，并在 CodeContest 上超越标准 MCTS。

ARC-AGI。
图 5（右）展示了在 ARC-AGI 这一特别具有挑战性的基准上的表现。遵循 ARC-AGI 的官方评估协议，我们报告 Pass@2（Pass@1 亦见附录 C.6）。与先前工作一致（Greenblatt, 2024），重复采样在我们的设定中是一个强基线，表明宽泛探索对该任务的重要性。虽然标准 MCTS 在更大预算下只有边际改进，我们的 AB-MCTS 框架取得了与重复采样相当的性能。这表明 AB-MCTS 有能力通过在有利时动态加宽搜索来进行有效探索。使用 DeepSeek-V3 也观察到类似结果，详见附录图 10。

MLE-Bench。
表 2 与附录图 10 展示了使用 GPT-4o 在 MLE-Bench 三个竞赛上的表现。由于 MLE-Bench 训练与评估机器学习模型需要大量 GPU 资源，我们只使用 GPT-4o，并聚焦于基线方法与 AB-MCTS-M（另见附录 B.1）。表现最好的基线方法因竞赛而异。这再次凸显了不同任务受益于不同的探索-利用取舍。相比之下，AB-MCTS-M 在这些任务上持续交出强劲表现。这种在多样竞赛上的一致成功，凸显了 AB-MCTS-M 有效适应不同问题结构的内在优势。

### 4.3 分析

图 6：增大预算下 ARC-AGI 的性能比较。通过把生成预算扩展至 512 来评估 AB-MCTS 的可扩展性。图中点为移动平均，以清晰呈现性能趋势。

搜索行为分析：宽度 vs. 深度。
为定量分析 AB-MCTS 如何平衡探索与利用，我们考察了所生成搜索树的平均深度与每个深度的平均宽度。图 5 表明，与标准 MCTS 相比，AB-MCTS 方法倾向于生成更宽的树。这是因为 AB-MCTS 可以从任意既有节点自适应地决定探索得更宽（选择 GEN 节点），而标准 MCTS 不能。该机制允许在各种树深度上更灵活地探索（另见附录 C.7）。除了这种加宽探索的灵活性，如 表 2 所示，AB-MCTS 在顺序精炼擅长的基准上也取得强劲表现，表明 AB-MCTS 能通过选择既有子节点进行精炼来有效识别并利用有希望的分支。这种自适应天性使它得以结合探索与利用的优势，在多样基准上取得稳健表现。

![Refer to caption](2503.04412v5/fig_3_graph_mlebench_gpt-4o-2024-08-06_Random_Acts_of_Pizza_AB-MCTS-M.png)

图 7：AB-MCTS-M 在 Random Acts of Pizza（MLE-Bench）上生成的示例搜索树。
该图展示了 AB-MCTS-M 如何动态平衡探索与利用。每个节点表示一个解。节点按其评估分数着色，该分数用作 AB-MCTS-M 的搜索信号。节点内的数字表示生成顺序。灰色节点标记代码执行失败、因此未获得分数的候选。

随预算增大的扩展。
高度复杂的问题往往需要大量生成预算才能找到正确解。ARC-AGI 是一个典型例子，如 Greenblatt (2024) 所报告，即便在很大预算下，通过重复采样进行广泛探索也已知能提升性能。为研究我们方法的扩展性质，我们在 ARC-AGI 上使用 DeepSeek-V3，把生成预算扩展到 $2^{9}=512$。如图 6 所示，当预算从 200 增加到 500 时，AB-MCTS 的性能持续显著提升，而重复采样的改进速率开始趋于平缓。标准 MCTS 在更大预算下也持续改进，但成功率显著低于 AB-MCTS 方法。这一性能差距凸显了在大计算规模下，AB-MCTS 更善于把搜索导向搜索树中有希望的分支。

搜索树的定性分析。
图 7 与附录图 11 展示了 AB-MCTS-M 与标准 MCTS 生成的示例搜索树。这些可视化说明了 AB-MCTS-M 相对标准 MCTS 更自适应的分支。这种自适应天性表明，AB-MCTS-M 在整个搜索过程中灵活平衡探索与利用，动态分配预算以探索多样的新候选（「变得更宽」）并精炼有希望的候选（「变得更深」）。进一步讨论见附录 C.3。

相对重复采样的效率与性能。
虽然重复采样受益于并行采样、无反馈计算开销等潜在效率优势，我们的结果展示了 AB-MCTS 的显著优势。在重复采样尤其强大的 ARC-AGI 上，AB-MCTS 不仅随预算增加持续改进，而且最终达到了重复采样无法企及的性能水平（图 6）。此外，在 LiveCodeBench 与 CodeContest 上，AB-MCTS 变体在许多情况下能显著更早达到重复采样的峰值性能（图 5、附录图 10）。这表明，即便把重复采样的固有优势考虑在内，AB-MCTS 仍是一种有前景的方法，能在多样场景中高效利用生成预算以取得更优结果。

## 5 结论

本文提出了自适应分支蒙特卡洛树搜索（AB-MCTS），一个通过有效整合多轮探索与利用来提升 LLM 在复杂任务上表现的推理时新框架。与先前方法不同，AB-MCTS 依据外部反馈动态决定「变得更宽」还是「变得更深」，利用贝叶斯决策。我们的实验结果表明 AB-MCTS 胜过重复采样与标准 MCTS，展示了自适应处理无界分支挑战对有效推理时扩展的价值。

局限。我们的方法假设存在可靠的分数评估器，但开发这样的评估器本身可能因任务而异、颇具挑战。未来工作还可以探索纳入超出 API 调用次数的更细粒度真实世界成本因素的搜索策略，从而可能提升 AB-MCTS 的实用性。我们相信，解决这些挑战将进一步增强 AB-MCTS 在更广泛问题上的适用性。

## 作者贡献

Kou Misaki 共同设计了 AB-MCTS 并实现了其算法与核心实验代码。
Yuichi Inoue 设计并领导了实验，提出并执行了实验分析，并共同领导了实验代码开发。
Yuki Imajuku 执行了 CodeContest 与 LiveCodeBench 实验并共同领导了实验代码开发。
So Kuroki 实现并执行了 MLE-Bench 实验。
Taishi Nakamura 执行了 ARC-AGI 实验。
Takuya Akiba 发起了该项目，共同设计了 AB-MCTS，对实验代码设计提供指导，并提供总体监督。
所有作者都参与了实验代码开发、结果解读与稿件打磨。

## 致谢

作者感谢 Edoardo Cetin、Luke Darlow、Taro Makino、Kosuke Nakago、Makoto Shing 与 Yutaro Yamada 对早期草稿的有益反馈。

## 参考文献

- [1]

  Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser,
  Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago,
  et al.
  Competition-level code generation with alphacode.
  *Science*, 378(6624):1092–1097, 2022.
- [2]

  Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V Le, Ed H. Chi, Sharan Narang,
  Aakanksha Chowdhery, and Denny Zhou.
  Self-consistency improves chain of thought reasoning in language
  models.
  In *International Conference on Learning Representations*, 2023.
- [3]

  Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V Le,
  Christopher Ré, and Azalia Mirhoseini.
  Large language monkeys: Scaling inference compute with repeated
  sampling.
  *arXiv preprint arXiv:2407.21787*, 2024.
- [4]

  Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah
  Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, et al.
  Self-refine: Iterative refinement with self-feedback.
  *Advances in Neural Information Processing Systems*, 36, 2024.
- [5]

  Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu
  Yao.
  Reflexion: Language agents with verbal reinforcement learning.
  *Advances in Neural Information Processing Systems*, 2024.
- [6]

  Jierui Li, Hung Le, Yingbo Zhou, Caiming Xiong, Silvio Savarese, and Doyen
  Sahoo.
  CodeTree: Agent-guided tree search for code generation with large
  language models.
  In *Proceedings of the 2025 Conference of the Nations of the
  Americas Chapter of the Association for Computational Linguistics: Human
  Language Technologies (Volume 1: Long Papers)*, pages 3711–3726, 2025.
- [7]

  Hao Tang, Keya Hu, Jin Peng Zhou, Si Cheng Zhong, Wei-Long Zheng, Xujie Si, and
  Kevin Ellis.
  Code repair with LLMs gives an exploration-exploitation tradeoff.
  In *Advances in Neural Information Processing Systems*, 2024.
- [8]

  Kuang-Huei Lee, Ian Fischer, Yueh-Hua Wu, Dave Marwood, Shumeet Baluja, Dale
  Schuurmans, and Xinyun Chen.
  Evolving deeper llm thinking.
  arXiv preprint arXiv:2501.09891, 2025.
- [9]

  Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman, Haohan Wang, and Yu-Xiong Wang.
  Language agent tree search unifies reasoning, acting, and planning in
  language models.
  In *International Conference on Machine Learning*, 2024.
- [10]

  Antonis Antoniades, Albert Örwall, Kexun Zhang, Yuxi Xie, Anirudh Goyal,
  and William Yang Wang.
  SWE-search: Enhancing software agents with monte carlo tree search
  and iterative refinement.
  In *International Conference on Learning Representations*, 2025.
- [11]

  Yingwei Ma, Qingping Yang, Rongyu Cao, Binhua Li, Fei Huang, and Yongbin Li.
  How to understand whole software repository?
  arXiv preprint arXiv:2406.01422, 2024.
- [12]

  Zhenwen Liang, Ye Liu, Tong Niu, Xiangliang Zhang, Yingbo Zhou, and Semih
  Yavuz.
  Improving llm reasoning through scaling inference computation with
  collaborative verification.
  arXiv preprint arXiv:2410.05318, 2024.
- [13]

  Ryan Greenblatt.
  Getting 50% (sota) on arc-agi with gpt-4o.
  <https://www.lesswrong.com/posts/Rdwui3wHxCeKb7feK/getting-50-sota-on-arc-agi-with-gpt-4o>,
  2024.
  Accessed: January 21, 2025.
- [14]

  Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida
  Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica.
  Livecodebench: Holistic and contamination free evaluation of large
  language models for code.
  In *International Conference on Learning Representations*, 2025.
- [15]

  Shibo Hao, Yi Gu, Haodi Ma, Joshua Hong, Zhen Wang, Daisy Wang, and Zhiting Hu.
  Reasoning with language model is planning with world model.
  In *Empirical Methods in Natural Language Processing*, pages
  8154–8173, 2023.
- [16]

  Jun Shern Chan, Neil Chowdhury, Oliver Jaffe, James Aung, Dane Sherburn, Evan
  Mays, Giulio Starace, Kevin Liu, Leon Maksin, Tejal Patwardhan, Aleksander
  Madry, and Lilian Weng.
  MLE-bench: Evaluating machine learning agents on machine learning
  engineering.
  In *International Conference on Learning Representations*, 2025.
- [17]

  François Chollet.
  On the measure of intelligence.
  arXiv preprint arXiv:1911.01547, 2019.
- [18]

  OpenAI.
  Gpt-4o system card.
  arXiv preprint arXiv:2410.21276, 2024a.
- [19]

  DeepSeek-AI.
  Deepseek-v3 technical report.
  arXiv preprint arXiv:2412.19437, 2024.
- [20]

  OpenAI.
  Openai o1 system card.
  *arXiv preprint arXiv:2412.16720*, 2024b.
- [21]

  OpenAI.
  Competitive programming with large reasoning models.
  arXiv preprint arXiv:2502.06807, 2025a.
- [22]

  DeepSeek-AI.
  Deepseek-r1: Incentivizing reasoning capability in llms via
  reinforcement learning.
  arXiv preprint arXiv:2501.12948, 2025.
- [23]

  Yixin Ye, Zhen Huang, Yang Xiao, Ethan Chern, Shijie Xia, and Pengfei Liu.
  Limo: Less is more for reasoning.
  arXiv preprint arXiv:2502.03387, 2025.
- [24]

  Niklas Muennighoff, Zitong Yang, Weijia Shi, Xiang Lisa Li, Li Fei-Fei,
  Hannaneh Hajishirzi, Luke Zettlemoyer, Percy Liang, Emmanuel Candès, and
  Tatsunori Hashimoto.
  s1: Simple test-time scaling.
  arXiv preprint arXiv:2501.19393, 2025.
- [25]

  Kimi Team.
  Kimi k1.5: Scaling reinforcement learning with llms.
  arXiv preprint arXiv:2501.12599, 2025.
- [26]

  Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Tom Griffiths, Yuan Cao, and
  Karthik Narasimhan.
  Tree of thoughts: Deliberate problem solving with large language
  models.
  *Advances in Neural Information Processing Systems*, 2024.
- [27]

  Charlie Victor Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar.
  Scaling test-time compute optimally can be more effective than
  scaling LLM parameters.
  In *International Conference on Learning Representations*, 2025.
- [28]

  Guoxin Chen, Minpeng Liao, Chengxi Li, and Kai Fan.
  Alphamath almost zero: Process supervision without process.
  In *Advances in Neural Information Processing Systems*, 2024.
- [29]

  Bofei Gao, Feifan Song, Zhe Yang, Zefan Cai, Yibo Miao, Qingxiu Dong, Lei Li,
  Chenghao Ma, Liang Chen, Runxin Xu, et al.
  Omni-MATH: A universal olympiad level mathematic benchmark for
  large language models.
  In *International Conference on Learning Representations*, 2025.
- [30]

  Yu Zhao, Huifeng Yin, Bo Zeng, Hao Wang, Tianqi Shi, Chenyang Lyu, Longyue
  Wang, Weihua Luo, and Kaifu Zhang.
  Marco-o1: Towards open reasoning models for open-ended solutions.
  arXiv preprint arXiv:2411.14405, 2024.
- [31]

  Zhenting Qi, Mingyuan MA, Jiahang Xu, Li Lyna Zhang, Fan Yang, and Mao Yang.
  Mutual reasoning makes smaller LLMs stronger problem-solver.
  In *International Conference on Learning Representations*, 2025.
- [32]

  Xinyu Guan, Li Lyna Zhang, Yifei Liu, Ning Shang, Youran Sun, Yi Zhu, Fan Yang,
  and Mao Yang.
  rstar-math: Small llms can master math reasoning with self-evolved
  deep thinking.
  arXiv preprint arXiv:2501.04519, 2025.
- [33]

  Yangzhen Wu, Zhiqing Sun, Shanda Li, Sean Welleck, and Yiming Yang.
  Inference scaling laws: An empirical analysis of compute-optimal
  inference for LLM problem-solving.
  In *International Conference on Learning Representations*, 2025.
- [34]

  Dan Zhang, Sining Zhoubian, Ziniu Hu, Yisong Yue, Yuxiao Dong, and Jie Tang.
  ReST-MCTS*: LLM self-training via process reward guided tree
  search.
  In *Advances in Neural Information Processing Systems*, 2024.
- [35]

  Rylan Schaeffer, Joshua Kazdan, John Hughes, Jordan Juravsky, Sara Price,
  Aengus Lynch, Erik Jones, Robert Kirk, Azalia Mirhoseini, and Sanmi Koyejo.
  How do large language monkeys get their power (laws)?, 2025.
- [36]

  Rémi Coulom.
  Computing “elo ratings” of move patterns in the game of go.
  *ICGA journal*, 30(4):198–208, 2007.
- [37]

  Adrien Couëtoux, Jean-Baptiste Hoock, Nataliya Sokolovska, Olivier Teytaud,
  and Nicolas Bonnard.
  Continuous upper confidence trees.
  In *Learning and Intelligent Optimization: 5th International
  Conference, LION 5, Rome, Italy, January 17-21, 2011. Selected Papers 5*,
  pages 433–445. Springer, 2011.
- [38]

  Samuel Sokota, Caleb Y Ho, Zaheen Ahmad, and J. Zico Kolter.
  Monte carlo tree search with iteratively refining state abstractions.
  In *Advances in Neural Information Processing Systems*,
  volume 34, pages 18698–18709, 2021.
- [39]

  Hunter Lightman, Vineet Kosaraju, Yuri Burda, Harrison Edwards, Bowen Baker,
  Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe.
  Let's verify step by step.
  In *International Conference on Learning Representations*, 2024.
- [40]

  An Yang, Beichen Zhang, Binyuan Hui, Bofei Gao, Bowen Yu, Chengpeng Li,
  Dayiheng Liu, Jianhong Tu, Jingren Zhou, Junyang Lin, et al.
  Qwen2.5-math technical report: Toward mathematical expert model via
  self-improvement.
  arXiv preprint arXiv:2409.12122, 2024.
- [41]

  Oriol Abril-Pla, Virgile Andreani, Colin Carroll, Larry Dong, Christopher J
  Fonnesbeck, Maxim Kochurov, Ravin Kumar, Junpeng Lao, Christian C Luhmann,
  Osvaldo A Martin, et al.
  PyMC: A modern, and comprehensive probabilistic programming
  framework in python.
  *PeerJ Computer Science*, 9:e1516, 2023.
- [42]

  Ruocheng Wang, Eric Zelikman, Gabriel Poesia, Yewen Pu, Nick Haber, and Noah
  Goodman.
  Hypothesis search: Inductive reasoning with language models.
  In *International Conference on Learning Representations*, 2024.
- [43]

  Jianhao Chen, Zishuo Xun, Bocheng Zhou, Han Qi, Hangfan Zhang, Qiaosheng Zhang,
  Yang Chen, Wei Hu, Yuzhong Qu, Wanli Ouyang, and Shuyue Hu.
  Do we truly need so many samples? multi-llm repeated sampling
  efficiently scales test-time compute.
  arXiv preprint arXiv:2501.12948, 2025.
- [44]

  Francois Chollet, Mike Knoop, Gregory Kamradt, Bryan Landers, and Henry
  Pinkard.
  Arc-agi-2: A new challenge for frontier ai reasoning systems.
  *arXiv preprint arXiv:2505.11831*, 2025.
- [45]

  Gemini Team.
  Gemini 2.5: Pushing the frontier with advanced reasoning,
  multimodality, long context, and next generation agentic capabilities.
  Technical report, Google DeepMind, jun 2025.
  URL
  <https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf>.
  Technical report, accessed 26 Jun 2025.
- [46]

  OpenAI.
  OpenAI o4-mini System Card.
  <https://openai.com/index/o3-o4-mini-system-card/>, apr
  2025b.
  Accessed 26 Jun 2025.

## 附录 A 方法细节

### A.1 扩展预备知识

#### A.1.1 问题设定

首先，我们定义问题设定并引入数学记号。

我们考虑输入为自然语言提示 $t_{\rm in}$（可包含少样本示例、任务指令等）的问题。给定 $t_{\rm in}$，LLM 产生自然语言输出 $t_{\rm out}$，随后由分数评估器打分得到最终分数 $r$。我们假设 $0\leq r\leq 1$，$r$ 越高对应答案越好。

这一两阶段流水线可以表示为：

$$
r=R(t_{\rm out})=R(f_{\rm LLM}(t_{\rm in})), \tag{2}
$$

其中函数 $f_{\rm LLM}$ 表示生成答案的 LLM，$R$ 是分数评估器。$f_{\rm LLM}$ 是随机的，对同一输入 $t_{\rm in}$ 可能产生不同输出 $t_{\rm out}$。这里我们允许 $t_{\rm out}$ 包含直接答案之外的信息（如推理步骤），并假设 $R$ 能正确解析该答案以执行分数评估。

我们的框架适用于任何最终答案可被定量打分的任务，例如编程任务（Li et al., 2022；Jain et al., 2025）、数学问题（Gao et al., 2025）与机器学习竞赛（Chan et al., 2025）。我们假设分数评估器 $R$ 已按任务特定方式定义，我们的目标是在推理时答案搜索期间找到取得尽可能高 $r$ 的 $t_{\rm out}$。

在有些模拟真实竞赛的任务中，真值分数评估器 $R_{\text{gt}}$（反映答案正确性）在答案搜索阶段不可访问。例如在 MLE-Bench（Chan et al., 2025）中，用于最终评估的测试数据集被保留；在编程竞赛任务（Li et al., 2022；Jain et al., 2025）中，参赛者通常只能有限次提交代码以获得隐藏测试用例上的分数。在这些情况下，为搜索最佳答案，可以求助于另一个分数评估器。例如在 MLE-Bench 中，这可以是公开数据集上的表现；在编程竞赛中，可以是解决的公开测试用例比例。对数学任务，可以使用单独训练的奖励模型（Yang et al., 2024）。在本工作中，我们假设答案搜索阶段存在某个可访问的分数评估器，能评估 $t_{\rm out}$ 的质量。

#### A.1.2 既有的推理时答案搜索方法

我们现在回顾两种只关注探索或只关注利用的标准方法。

只变得更宽：重复采样。
一种直接的推理时答案搜索方法是以非零温度从 LLM 反复采样答案。我们把每个采样步骤称为*直接答案生成过程*。执行 $n$ 次：

$$
t_{\rm out}^{m}=f_{\rm LLM}(t_{\rm in}),\quad m\in\{1,\dots,n\}, \tag{3}
$$

我们获得多个候选答案。然后可以按预定义准则选出最佳答案，例如最高分 $r$（best-of-$n$）、多数投票或自洽性。Brown et al. (2024) 最近表明，随着 $n$ 增大，生成答案的覆盖率会提升。AlphaCode（Li et al., 2022）采用类似方法在竞赛编程任务上达到了人类水平的表现。

只变得更深：顺序精炼。
或者，我们可以利用答案精炼过程并顺序地应用它来执行答案搜索。我们考虑这样的情形：已经让某个答案生成器求解当前问题 $k$ 次，并收集了这些答案生成的输入-输出对 $t_{\rm in}^{j}$ 与 $t_{\rm out}^{j}$，其中 $j\in\{1,\dots,k\}$。

我们把*答案精炼过程*定义为两步流程：(1) 从既有输入-输出对创建新的精炼输入；(2) 从 $t_{\rm in}^{k+1}$ 生成新答案 $t_{\rm out}^{k+1}$。符号化地，

$$
t^{k+1}_{\rm out}=f_{\rm LLM}(t^{k+1}_{\rm in})=f_{\rm LLM}\left(h_{\rm refine}\big(\{t_{\rm in}^{j},t_{\rm out}^{j}\}_{j\in\{1,\dots,k\}}\big)\right), \tag{4}
$$

其中 $h_{\rm refine}$ 是精炼输入生成器，提供精炼所需的全部信息，例如对每个答案的反馈（如编程任务的代码执行结果或错误）。

迭代地应用这一精炼步骤得到 $n$ 个答案：

$$
t_{\rm in}^{1}=t_{\rm in}, \tag{5}
$$

$$
t_{\rm out}^{1}=f_{\rm LLM}(t_{\rm in}^{1}), \tag{6}
$$

$$
t_{\rm in}^{m}=h_{\rm refine}\big(\{t_{\rm in}^{j},t_{\rm out}^{j}\}_{j\in\{1,\dots,m-1\}}\big) \tag{7}
$$

$$
t_{\rm out}^{m}=f_{\rm LLM}(t_{\rm in}^{m}) \tag{8}
$$

其中 $m\in\{2,\dots,n\}$。最后，与重复采样方法类似，依据选定准则从 $\{t_{\rm out}^{a}\}_{a\in\{1,\dots,n\}}$ 中选出最佳候选。

我们可以把上述两种方法（纯探索与纯利用）视为树搜索的特例：前者只从根节点扩展，而后者沿单条线性路径从最近到达的叶节点继续，向深处探索而不向外分支。标准 MCTS 自然地融合了两者，但它使用固定分支因子，从而在使用 LLM 时限制了来自重复采样的性能增益。我们的 AB-MCTS 采用更灵活的分支算法，有效利用重复采样带来的性能提升。

### A.2 AB-MCTS 与带渐进加宽的标准 MCTS 的比较

渐进加宽有参数 $(k,\alpha)$，用节点访问计数 $n$ 把分支数约束为 $kn^{\alpha}$。使用这些参数时，是否分支的规则作为节点访问计数的函数被预先确定。关键在于，这一决策并不使用搜索过程中收集的重要信息，即已扩展节点的观测奖励。UCT 分数只在决定不分支之后用于选择下潜到哪个子节点。此外，把分支规则定义为访问计数的函数意味着树的形状与节点度的扩展行为由超参数的选择预先决定。

相比之下，我们的方法不只基于访问计数与超参数来限制分支规则。相反，分支因子基于观测奖励动态适应。这对 LLM 测试时推理扩展是一个重要要求——在该领域，纯粹变宽的树搜索已知是强基线。为展示 AB-MCTS 的稳健性，我们在附录 C.4 中进行了比较 AB-MCTS 与渐进加宽的实验。

### A.3 AB-MCTS-M 细节

#### A.3.1 混合模型背景

混合线性模型是传统线性模型的扩展，通过同时纳入固定效应与随机效应来显式建模观测间的非独立性。固定效应对整个总体或数据集中一致、可预测的模式建模（如对所有组共同的处理效应）。相比之下，随机效应对特定嵌套或层级组内部或之间的变异建模（如参与者之间的个体差异，或学校之间的差异）。

#### A.3.2 详细的混合模型表述与示例代码

在 AB-MCTS-M 中，我们在 MCTS 树的每个节点 $N$（即 MCTS 选择步骤内的每个子步骤）分别拟合一个混合模型。具体而言，设 $N_{j}$（$j=1,\dots,n_{\text{child}}$）为 $N$ 的直接子节点，并定义 $T_{\text{sub}}(N_{j})$ 为 $N_{j}$ 之下的子树（包括 $N_{j}$ 自身）。对一个新生成的节点 $\tilde{N}$：(i) $j=0$（即 GEN 节点）且 $\tilde{N}$ 是 $N$ 的直接子节点，或 (ii) $j=1,\dots,n_{\text{child}}$ 且 $\tilde{N}$ 是在该迭代步从 $T_{\text{sub}}(N_{j})$ 中某节点扩展出的节点，我们假设：

$$
r_{\tilde{N}}=\alpha_{j}+\sigma_{y}\epsilon_{\tilde{N}},\quad\alpha_{j}=\mu_{\alpha}+\sigma_{\alpha}\epsilon_{j}, \tag{9}
$$

$$
\epsilon_{\tilde{N}}\sim\mathcal{N}(0,1),\quad\epsilon_{j}\sim\mathcal{N}(0,1), \tag{10}
$$

这里，$\alpha_{j}$ 是刻画 $N_{j}$ 处基础解质量的「组级」截距，而 $\sigma_{y}\epsilon_{\tilde{N}}$ 表示逐实例噪声。GEN 节点（动作 $a_{0}$）被视为一个新引入的组，自身没有直接观测。不过，其组级截距 $\alpha_{0}$ 不是仅从先验推断，而是从由其他观测数据告知的 $\mu_{\alpha}$ 与 $\sigma_{\alpha}$ 的后验分布推断。

我们对 $(\mu_{\alpha},\sigma_{\alpha},\sigma_{y})$ 设置先验并用 MCMC（马尔可夫链蒙特卡洛）估计它们，然后执行 Thompson 采样。因为 GEN 组（$j=0$）没有直接观测，其后验保持更高的不确定性，从而鼓励探索。为说明如何估计后验预测，代码清单 1 给出了与图 2 所示示例树对应的 PyMC（Abril-Pla et al., 2023）代码。

```python
import pymc as pm

# Child indices use 0-based indexing; note the difference from index j in Equations (9-10)

child_indices = [0, 0, 0, 1, 2, 2]

rewards = [0.8, 0.8, 1.0, 0, 0.2, 0.3]

coords = {"child_idx": [0, 1, 2]}

with pm.Model(coords=coords) as model:

## Priors

mu_alpha = pm.Normal("mu_alpha", mu=0.5, sigma=0.2)

sigma_alpha = pm.HalfNormal("sigma_alpha", sigma=0.2)

sigma_y = pm.HalfNormal("sigma_y", sigma=0.3)

## Priors END

eps_j = pm.Normal("eps_j", mu=0, sigma=1, dims="child_idx")

alpha = mu_alpha + eps_j * sigma_alpha

r = pm.Normal("r", mu=alpha[child_indices], sigma=sigma_y, observed=rewards)
```

代码清单 1：AB-MCTS-M 拟合模型示例代码

```python
eps_j_gen = pm.Normal("eps_j_gen", mu=0, sigma=1)

alpha_gen = mu_alpha + eps_j_gen * sigma_alpha

r_gen = pm.Normal("r_gen", mu=alpha_gen, sigma=sigma_y)
```

代码清单 2：AB-MCTS-M 的 GEN 节点奖励建模

这里，我们采用了与实验设定相同的先验，如附录 B.2 所述：

$$
\mu_{\alpha}\sim\mathcal{N}(0.5,0.2^{2}),\quad\sigma_{\alpha}\sim\mathcal{N}_{\text{half}}(0.2^{2}),\quad\sigma_{y}\sim\mathcal{N}_{\text{half}}(0.3^{2}), \tag{11}
$$

在该实现中，变量 alpha 是节点特定的（由 child_idx 索引），但共享参数 mu_alpha（表示由任务固有难度决定的总体平均答案质量）与 sigma_alpha（表示由 LLM 回答多样性引起的答案质量变异）。节点之间答案质量的差异由变量 eps_j 刻画。

为计算 GEN 节点的概率分布，我们通过添加一个表示 GEN 节点奖励的额外变量，引入一个略微修改的预测模型，如代码清单 2 所示。

由于 eps_j_gen 没有关联的观测数据，r_gen 通常比 r 呈现更高的方差。直观上，r_gen 同时纳入了源自精炼过程的方差与节点 $N$ 处答案生成的固有变异。这一增大的方差在 Thompson 采样中鼓励更多探索。

模型拟合后，r（既有子节点）与 r_gen（GEN 节点）的后验预测分布被用于 Thompson 采样。

### A.4 AB-MCTS-A 细节：参数更新规则

#### A.4.1 AB-MCTS-A（Gaussian）参数更新规则

至于参数更新规则，对高斯情形，我们使用 normal-inverse-$\chi^{2}$ 先验：

$$
p(r\mid\{r_{n}\}_{n=1}^{N})=\mathcal{N}(r\mid\invbreve{m},\tfrac{\sigma^{2}}{\invbreve{\kappa}})\chi^{-2}(\sigma^{2}\mid\invbreve{\nu},\invbreve{\tau}^{2}), \tag{12}
$$

$$
\invbreve{m}=\frac{\breve{\kappa}\breve{m}+N\bar{r}}{\invbreve{\kappa}}, \tag{13}
$$

$$
\invbreve{\kappa}=\breve{\kappa}+N, \tag{14}
$$

$$
\invbreve{\nu}=\breve{\nu}+N, \tag{15}
$$

$$
\invbreve{\nu}\,\invbreve{\tau}^{2}=\breve{\nu}\,\breve{\tau}^{2}+\sum_{n=1}^{N}(r_{n}-\bar{r})^{2}\;+\;\frac{N\,\breve{\kappa}}{\breve{\kappa}+N}\,(\invbreve{m}-\bar{r})^{2}, \tag{16}
$$

$$
\bar{r}=\frac{1}{N}\sum_{n=1}^{N}r_{n}, \tag{17}
$$

其中 $r_{n}$ 是观测分数。

#### A.4.2 AB-MCTS-A（Beta）参数更新规则

或者，若 $r\in[0,1]$，我们可以在观测 $\{r_{n}\}_{n=1}^{N}$ 后使用带以下参数更新规则的 Beta 分布：

$$
p(r\mid\{r_{n}\}_{n=1}^{N})=B(r\mid\invbreve{\alpha},\invbreve{\beta}), \tag{18}
$$

$$
\invbreve{\alpha}=\breve{\alpha}+\sum_{n=1}^{N}r_{n}, \tag{19}
$$

$$
\invbreve{\beta}=\breve{\beta}+\sum_{n=1}^{N}(1-r_{n}), \tag{20}
$$

其中 $B(\cdot\mid\alpha,\beta)$ 表示 Beta 分布。我们注意到，该更新规则通常与伯努利试验一同使用，但这里我们直接使用 Beta 分布对分数分布建模。实践中，根据我们的实验结果，这一参数更新规则表现良好。

### A.5 演练示例

我们在图 2 与图 3 的示例树上演练 AB-MCTS-M 与 AB-MCTS-A 的一次迭代。由于 Thompson 采样的存在，过程是随机的；为清晰起见，我们假设特定的采样结果。

#### A.5.1 AB-MCTS-M

AB-MCTS-M 通过每次添加一个节点来增量构建搜索树。在本节中，我们详述 AB-MCTS-M 算法的单次迭代，清楚说明选择待扩展节点、执行扩展、回传所得分数的顺序。为简单和具体起见，我们假设当前搜索树结构如图 2 所示，并描述一次包括选择、扩展与分数回传的完整迭代。

1. （$N\to N_{1}$）在 $N$ 处，我们在混合模型下为其四个子节点 GEN、$N_{1}$、$N_{2}$、$N_{3}$ 计算后验分布，并从每个分布抽取一个分数。若 GEN 取得最高采样，则扩展 GEN 并回传其分数（算法 1，第 11–13 行）。这里我们假设 $N_{1}$ 取得最高采样分数，反映了对后验峰值相对较大的子节点的利用。
2. （$N_{1}\to N_{1}^{\prime}$）$N_{1}$ 有两个直接子节点：$N_{1}^{\prime}\;(r=0.8)$ 与 $N_{2}^{\prime}\;(r=1.0)$。我们为 GEN、$N_{1}^{\prime}$、$N_{2}^{\prime}$ 计算后验并再次采样。尽管从图 2 可见子树 $T(N_{2}^{\prime})$ 当前包含分数更高的节点，但其后验的有限方差确保 $N_{2}^{\prime}$ 不会总被选中，并鼓励对欠探索树区域的更多探索。假设本次迭代选中 $N_{1}^{\prime}$。
3. （扩展 $N_{1}^{\prime}$）因为 $N_{1}^{\prime}$ 是叶节点，我们将其扩展（算法 1，第 10 行）。假设新生成的节点得到分数 $r=0.5$。由于所有叶节点都有 GEN 子节点，该扩展节点也会被挂上一个 GEN 节点。
4. （分数回传）分数从扩展节点向根方向传播，如标准 MCTS。在当前示例中，分数先回传到第 3 步生成的节点，再经过节点 $N_{1}^{\prime}$、$N_{1}$ 与 $N$。与标准 MCTS 不同，AB-MCTS-M 维护单独的分数而非平均值。具体而言，回传到节点 $N_{1},N_{2},N_{3}$ 的分数形成对应混合模型中各组的独立观测列表。虽然 GEN 节点因该分数回传规则而没有直接观测，其后验分布与这些组共享统计强度，允许间接的信息共享，并提高对节点扩展所得分数的估计精度。在下一次 SelectExpansionTarget 调用时，$N$ 处的四个后验形状不同；具体而言，$N_{1}$ 后验的峰值因期望值降低而左移。其他后验分布也受影响，例如 GEN 后验的右侧尾部收缩。请注意，在 AB-MCTS-M 中，后验分布形状的变化无法解析写出，而是由 MCMC 计算。因此，与标准 MCTS 不同，分数回传步骤只是把新分数追加到一个分数列表中。

#### A.5.2 AB-MCTS-A

AB-MCTS-A 的工作方式与 AB-MCTS-M 类似，区别在于 CONT 节点的引入以及分数回传的方式。为清楚说明算法并突出与 AB-MCTS-M 的差异，我们为 AB-MCTS-A 描述一次完整的选择、扩展与分数回传迭代。由于 Beta 与 Gaussian 变体的唯一区别是分数更新如何反映到后验分布中，这里我们聚焦后验更新的定性方面，并以示例树（图 3）为细节对象。

1. （$N\to\text{CONT}$）在根处，我们从 GEN 与 CONT 子节点的后验采样。如第 3.4 节所述，GEN 后验由 CONT 子节点 $N_{1}\;(0.8)$、$N_{2}\;(0.0)$、$N_{3}\;(0.2)$ 告知，而 CONT 后验使用 CONT 节点后代中除去 $N_{1}$、$N_{2}$、$N_{3}$ 之外的分数，即 0.8、1.0、0.3。这里我们假设选中 CONT。
2. （$\text{CONT}\to N_{1}$）接下来我们为 CONT 的子节点 $N_{1}$、$N_{2}$、$N_{3}$ 计算后验。由于分数回传规则，后验分布由先前扩展的节点计算；具体而言，以下分数用于后验分布计算：$N_{1}$：(0.8, 0.8, 1.0)，$N_{2}$：(0.0)，$N_{3}$：(0.2, 0.3)。这里我们假设 $N_{1}$ 通过 Thompson 采样取得最高采样。
3. （扩展 $N_{1}$）再次地，我们在 $N_{1}$ 的 GEN 与 CONT 子节点之间执行 Thompson 采样。GEN 后验使用 (0.8, 1.0)；CONT 后验因不存在已生成的后代而退回先验。这里我们假设选中 GEN，从而在 $N_{1}$ 的 CONT 子节点下扩展一个新节点。我们假设分数为 $r=0.5$。
4. （分数回传）我们按第 3.4 节的规定回传分数 $r=0.5$。首先，分数回传到生成该节点的 GEN 节点。其次，它传播到：(i) GEN 节点的祖先 $N_{1}$，以及 (ii) 作为 $N_{1}$ 父节点的 CONT 节点。因为 0.5 低于既有分数 0.8、1.0，$N_{1}$ 的后验峰值左移，降低了 $N_{1}$ 未来从 CONT 被再次选中的概率。类似地，把 0.5 加入既有分数 (0.8, 1.0, 0.3) 降低了 $N$ 处 CONT 后验的峰值，从而降低后续迭代中 CONT 在 $N$ 处被选中的概率。

### A.6 AB-MCTS 的超参数敏感性

本节给出 AB-MCTS 所用超参数的敏感性分析。如附录 B.2 所讨论，先验参数被设计为无信息以最小化偏差。由于随着搜索推进后验分布日益由数据驱动，我们假设初始先验的影响有限。这里我们通过广泛的分析实证检验这一假设。我们在 LiveCodeBench 上评估 AB-MCTS 各变体对其先验超参数的敏感性，使用 GPT-4o、生成预算 $2^{4}$。每个配置运行五次（$n=5$）以计算 Pass@1 的均值与标准差。表 3 总结了 AB-MCTS-M、AB-MCTS-A（Gaussian）与 AB-MCTS-A（Beta）在各种先验设定下的结果。在所有测试范围内，性能保持稳定，表明对初始超参数值的低敏感性。这证实 AB-MCTS 对先验超参数的初始化稳健，其性能主要由搜索期间数据驱动的后验更新主导。

表 3：
AB-MCTS 的超参数敏感性。
每种先验设定下的 Pass@1 结果。所有值为五次运行的平均。

AB-MCTS-M

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| $\breve{m}$ | 0.0 | 0.4 | 0.5 | 0.6 | 1.0 |
| Pass@1 | 38.4 ± 1.6 | 37.3 ± 0.4 | 36.8 ± 1.5 | 37.5 ± 1.5 | 37.7 ± 1.3 |

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| $\breve{\alpha}$ | 0.01 | 0.1 | 0.2 | 0.3 | 1.0 |
| Pass@1 | 38.4 ± 1.3 | 37.7 ± 0.9 | 36.8 ± 1.5 | 38.2 ± 2.3 | 38.6 ± 1.8 |

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| $\breve{\tau}$ | 0.01 | 0.1 | 0.2 | 0.3 | 1.0 |
| Pass@1 | 37.3 ± 2.0 | 38.2 ± 1.1 | 37.1 ± 1.2 | 36.8 ± 1.5 | 39.5 ± 1.3 |

AB-MCTS-A (Gaussian)

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| $\breve{m}$ | 0.0 | 0.1 | 0.5 | 1.0 |
| Pass@1 | 38.0 ± 1.6 | 37.0 ± 1.4 | 37.3 ± 1.5 | 37.7 ± 0.7 |

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| $\breve{\kappa}$ | 0.001 | 0.5 | 1.0 | 10.0 |
| Pass@1 | 38.4 ± 1.3 | 37.3 ± 1.5 | 38.0 ± 1.6 | 37.7 ± 0.7 |

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| $\breve{\nu}$ | 0.001 | 0.5 | 1.0 | 10.0 |
| Pass@1 | 38.2 ± 1.3 | 37.7 ± 1.3 | 38.0 ± 1.6 | 38.9 ± 1.0 |

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| $\breve{\tau}^{2}$ | 0.05 | 0.1 | 0.2 | 0.5 | 1.0 |
| Pass@1 | 37.5 ± 0.9 | 38.0 ± 1.6 | 37.7 ± 1.3 | 37.9 ± 0.8 | 37.7 ± 0.7 |

AB-MCTS-A (Beta)

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| $\breve{\alpha}$ | 0.1 | 0.4 | 0.5 | 0.6 | 1.0 |
| Pass@1 | 37.3 ± 1.5 | 37.0 ± 1.5 | 37.5 ± 1.3 | 37.5 ± 1.3 | 37.7 ± 1.2 |

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| $\breve{\beta}$ | 0.1 | 0.4 | 0.5 | 0.6 | 1.0 |
| Pass@1 | 38.4 ± 1.8 | 38.4 ± 1.1 | 37.5 ± 1.3 | 37.9 ± 0.5 | 37.9 ± 1.4 |

## 附录 B 补充实验细节

### B.1 任务与数据集

我们在四个基准上评估我们的方法：CodeContest（Li et al., 2022）、LiveCodeBench（Jain et al., 2025）、抽象与推理语料库（ARC）（Chollet, 2019）与 MLE-Bench（Chan et al., 2025）。所有这些基准的任务通常通过代码生成求解。每个实验以非零温度多次运行以计入随机性（LiveCodeBench $n=5$，CodeContest 与 ARC-AGI $n=3$）。对 MLE-Bench，由于计算成本巨大，实验以 $n=1$ 运行。

CodeContest 与 LiveCodeBench 是成熟的竞赛编程基准，均提供公开测试与隐藏测试。我们用公开测试计算每个节点的分数，用隐藏测试做最终评估。只有当解通过某道题的全部隐藏测试用例时才计为正确，成功率定义为所选解完全正确的题目比例。我们使用的提示模板基于先前工作（Jain et al., 2025）。在 LiveCodeBench 中，我们只使用 2024 年 8 月至 11 月发布的题目，与先前工作（DeepSeek-AI, 2024）保持一致以防止数据污染。

ARC-AGI 要求从多个输入-输出示例中发现共享的变换规则，然后用它预测测试输入的输出。从示例网格生成代码是 ARC 常用的方法（Tang et al., 2024；Greenblatt, 2024；Wang et al., 2024）。我们指示 LLM 从提供的输入/输出示例推断变换规则并生成相应的 Python 代码。每个节点的分数由其正确变换的示例比例决定。取得最高分的节点随后用于变换测试示例；若输出与真值完全匹配，该节点分数设为 1。我们在与先前工作（Greenblatt, 2024）相同的 100 道公开评估问题与提示上评估我们的方法。

MLE-Bench 包含源自 Kaggle 竞赛的实用机器学习任务。为支持公平比较（Chan et al., 2025），我们采用三个低复杂度挑战（Nomad2018 Predicting Transparent Conductors、Spooky Author Identification 与 Random Acts of Pizza）。每个竞赛的训练数据被随机拆分为 80% 训练与 20% 验证。验证集用于获得每个节点的分数。我们在给定推理预算下选择验证分数最高的节点，然后在隐藏测试集上评估以得到最终结果。遵循先前研究（Chan et al., 2025），我们使用 AIDE 脚手架进行实验。在这些竞赛中评估生成的机器学习模型资源消耗显著，即便处理单个候选解也需要大量 GPU 算力。在我们的实验中，每个候选解在单张 H100 GPU 上以一小时时限执行。这一计算需求仍远高于本工作讨论的其他基准。因此，由于这些可观的成本，在 MLE-Bench 上对所有方法与模型进行全面实验是不可行的。所以我们聚焦于用 GPT-4o 对这些任务评估 AB-MCTS-M。

### B.2 AB-MCTS 参数

由于其贝叶斯性质，AB-MCTS 的超参数只包含先验参数。我们对所有任务使用相同的先验参数，不使用任务特定的领域知识（仅假定分数范围约为 $[0,1]$），以最小化任何潜在偏差。因此，我们的先验具有以下共同性质：

- 绝大部分概率质量（对 AB-MCTS-A（Beta）而言是全部）位于 $[0,1]$ 之内。
- 分数的平均值为 0.5，反映对答案质量的中性初始假设（0 表示最差，1 表示最佳）。
- 概率质量不会过度集中在任何特定区域，反映我们的无偏先验。

我们对 AB-MCTS-M 在式 (9) 与 (10) 中设定以下先验：

$$
\mu_{\alpha}\sim\mathcal{N}(0.5,0.2^{2}),\quad\sigma_{\alpha}\sim\mathcal{N}_{\text{half}}(0.2^{2}),\quad\sigma_{y}\sim\mathcal{N}_{\text{half}}(0.3^{2}), \tag{21}
$$

其中 $\mathcal{N}_{\text{half}}$ 是半正态分布（请参阅第 3.3 节与附录 A.3）。对 AB-MCTS-A（Gaussian），我们在式 (12)–(17) 中设 $\breve{m}=0$、$\breve{\kappa}=1$、$\breve{\nu}=1$、$\breve{\tau}^{2}=0.1$；对 AB-MCTS-A（Beta），我们在式 (18)–(20) 中设 $\breve{\alpha}=0.5$、$\breve{\beta}=0.5$。如前所述，我们选择这些参数的方式尽可能少地施加假设以最小化偏差。

我们预计对特定初始先验参数值的依赖很小，主要因为我们评估中的计算预算可观，且随着搜索树因更多分数观测而扩展，后验分布日益由数据主导（多数实验中至多 $2^{7}$ 个节点，扩展 ARC-AGI 实验中为 $2^{9}$）。因为我们的节点选择方法（采用混合模型的 AB-MCTS-M 与使用共轭先验的 AB-MCTS-A）本质上是贝叶斯的，先验主要影响搜索的早期阶段。此外，混合模型固有的「借力（borrowing strength）」机制稳定了后验估计并促进收敛。随着搜索推进、分数观测累积，初始先验的影响自然消退。

![Refer to caption](2503.04412v5/figure1_deepseek.png)

图 8：
使用 DeepSeek-V3 在 LiveCodeBench、CodeContest 与 ARC-AGI 上的性能比较。
我们绘制成功率随生成预算的变化，比较 AB-MCTS 方法与基线。

![Refer to caption](2503.04412v5/figure2_deepseek_3.png)

图 9：
按搜索树形状与性能比较算法。
每个点表示给定算法在特定生成预算下、相对平均树形状的性能。横轴为平均树深度与平均树宽度之比的对数。平均宽度按每个深度的平均节点数计算。横轴值越大表示搜索越深，越小表示搜索越宽。

图 10：
使用 GPT-4o 在三个 MLE-Bench 任务上的性能比较。每幅图展示性能随总生成预算的变化。对 Nomad2018 Predicting Transparent Conductors 与 Spooky Author Identification，分数越低越好（分别为 RMSLE 与 Log Loss）；对 Random Acts of Pizza，分数越高越好（ROC AUC）。在每个预算下，我们基于验证集表现选出单一解并报告其测试集分数。

![Refer to caption](2503.04412v5/fig_3_graph_mlebench_gpt-4o-2024-08-06_Nomad2018_AB-MCTS-M.png)

![Refer to caption](2503.04412v5/fig_3_graph_mlebench_gpt-4o-2024-08-06_Nomad2018_Standard_MCTS.png)

![Refer to caption](2503.04412v5/fig_3_graph_mlebench_gpt-4o-2024-08-06_Spooky_Author_Identification_AB-MCTS-M.png)

![Refer to caption](2503.04412v5/fig_3_graph_mlebench_gpt-4o-2024-08-06_Spooky_Author_Identification_Standard_MCTS.png)

![Refer to caption](2503.04412v5/x1.png)

![Refer to caption](2503.04412v5/fig_3_graph_mlebench_gpt-4o-2024-08-06_Random_Acts_of_Pizza_Standard_MCTS.png)

图 11：MLE-Bench 上 AB-MCTS-M 与标准 MCTS 生成的示例搜索树。AB-MCTS-M 为 Random Acts of Pizza 生成的示例树与图 7 所示为同一棵树。

## 附录 C 补充实验与分析

### C.1 DeepSeek-V3 在竞赛编程与 ARC-AGI 上的结果

本附录提供使用 DeepSeek-V3 模型的补充结果，聚焦总体表现与搜索行为特征。

图 10 展示了 DeepSeek-V3 在竞赛编程（LiveCodeBench、CodeContest）与 ARC-AGI 基准上的性能（Pass@1）。虽然总体表现趋势与 GPT-4o（图 5）类似，但基线方法的相对强弱随 DeepSeek-V3 而变化。例如，标准 MCTS 在 LiveCodeBench 上取得最高成功率。在 CodeContest 上，AB-MCTS 与表现最好的基线之间的性能差异不如 GPT-4o 明显。尽管存在这些差异，AB-MCTS 变体在所有任务上都稳居领先方法之列。这表明即便底层模型的变化改变了不同基线策略的有效性，AB-MCTS 仍能可靠地交出强劲表现。

DeepSeek-V3 的搜索树形状与性能分析（图 10）与 GPT-4o 的发现（图 5）高度一致。正如预期，重复采样形成宽的搜索树，而顺序精炼形成深的树。与标准 MCTS 相比，AB-MCTS 方法一致地生成更宽的树。这种偏宽探索的倾向即使在 DeepSeek-V3 的 LiveCodeBench 等顺序精炼胜过重复采样的任务上也很显著。AB-MCTS 算法在此类场景中的强劲表现表明，它们不仅能广泛探索，还能通过自适应节点选择有效识别并加深有希望的分支。这凸显了 AB-MCTS 在不同模型间平衡这些竞争需求的稳健本质。

### C.2 GPT-4o 在 MLE-Bench 三个竞赛上的结果

图 10 在 MLE-Bench 三个竞赛上使用 GPT-4o 比较 AB-MCTS-M 与基线方法，绘制性能分数随生成预算的变化。值得注意的是，最有效的基线因竞赛而异。例如在 Nomad2018 上，顺序精炼最终取得最佳分数，而重复采样没有任何改进。在 Spooky Author Identification 上，标准 MCTS 在整个预算范围内持续改进。相反，在 Random Acts of Pizza 上，重复采样显著胜过其他基线。尽管基线有效性存在这种差异，AB-MCTS-M 在全部三个竞赛上都持续交出强劲表现。这凸显了 AB-MCTS-M 的稳健性与适应性，表明其有能力针对每个任务的不同特性有效调整搜索方式，尤其是在最佳策略事先不明朗时。

### C.3 各方法在 MLE-Bench 上生成的示例搜索树

图 11 展示了 AB-MCTS-M 与标准 MCTS 在三个 MLE-Bench 竞赛上生成的示例搜索树。在所有任务上，AB-MCTS-M 生成的树在视觉上显示出比标准 MCTS 更灵活的方式，有效地把更广的探索与对有希望节点的集中利用相结合。

表 4：
LiveCodeBench 上渐进加宽与 AB-MCTS 的比较。

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
|  | ($k$, $\alpha$) = (1, 0.45) | ($k$, $\alpha$) = (5, 0.5) | ($k$, $\alpha$) = (10, 0.55) | AB-MCTS-A (Gaussian) | AB-MCTS-A (Beta) | AB-MCTS-M |
| Pass@1 | 48.7 $\pm$0.8 | 50.7 $\pm$1.3 | 50.5 $\pm$3.1 | 48.9 $\pm$2.0 | 51.8 $\pm$1.4 | 49.6 $\pm$1.6 |

### C.4 在 LiveCodeBench 上与渐进加宽的比较

为把渐进加宽与 AB-MCTS 比较，我们在 LiveCodeBench 上以多种参数对渐进加宽进行了实验。我们使用 deepseek-v3-0324、生成预算 $2^{7}$（$n=5$）。结果示于表 4。虽然合适的渐进加宽参数能带来与 AB-MCTS 相当的强劲表现，但其有效性对超参数高度敏感。例如，$(k,\alpha)=(1,0.45)$ 产生了最差结果。此外，$(k,\alpha)=(10,0.55)$ 设定显示出搜索不稳定性，导致最高的方差。相比之下，AB-MCTS 无需此类调参即表现稳健，展示了其实用优势。

表 5：
ARC-AGI 上 GPT-4o 的 Pass@1 与 Pass@2 比较。

|  |  |  |
| --- | --- | --- |
| 方法 | Pass@1 | Pass@2 |
| 重复采样 | 14.0 ± 1.7 | 15.0 ± 1.0 |
| 顺序精炼 | 7.7 ± 0.6 | 8.7 ± 0.9 |
| 标准 MCTS | 8.0 ± 1.0 | 9.0 ± 1.5 |
| AB-MCTS-M | 11.0 ± 1.0 | 12.3 ± 1.2 |
| AB-MCTS-A (Gaussian) | 13.0 ± 3.6 | 13.0 ± 3.6 |
| AB-MCTS-A (Beta) | 12.7 ± 0.6 | 14.0 ± 2.1 |

### C.5 AB-MCTS-M vs. AB-MCTS-A：分析与选择

本文提出两种自适应分支算法：AB-MCTS-M 与 AB-MCTS-A。本节基于我们的实验发现与其不同的底层机制，给出二者之间的选择考量。

当以输出质量为首要考量时，AB-MCTS-M 常是首选，因为它表现持续强劲（表 1 与表 2）。在节点选择上，该算法使用 MCMC——一种提升有效性的迭代流程，但每次选择会带来一些计算开销。对时间约束严格的应用，AB-MCTS-A 提供更轻量的替代，其 Gaussian 与 Beta 变体采用解析可处理的后验更新。然而，当 LLM 推理时间或评估生成候选解所需的时间占主导时，MCMC 花费的额外时间对总运行时间影响甚微。

虽然两种算法都具备自适应搜索，图 5 与图 10 表明 AB-MCTS-A 倾向于构建更宽的搜索树。这一倾向源自其核心设计：在每个深度，AB-MCTS-A 在选择 GEN 节点与 CONT 节点之间二选一。到达深度 $d$ 需要 $d$ 次连续的 CONT 选择，因此更深的路径在概率上呈几何级数地低于更宽的扩展（另见第 A.4 节）。因此，对诸如 ARC-AGI 等更广探索被认为特别有益的任务，AB-MCTS-A 可能更可取。

归根结底，选择取决于应用的主要目标：当优先考虑输出质量时 AB-MCTS-M 往往表现良好，而 AB-MCTS-A 在计算效率与受益于更广探索的任务上具有优势。不过，二者都提供有能力的自适应搜索策略。

### C.6 ARC-AGI 上的 Pass@1 vs. Pass@2

在表 1 中，我们对 ARC-AGI 报告 Pass@2 分数，以遵循该基准定义的标准评估协议（Chollet, 2019）。为完整与透明起见，我们也在表 5 中报告对应的 Pass@1 结果。如表 5 所示，结果表明 Pass@1 与 Pass@2 之间的相对表现一致。特别是方法的排名保持不变，证实正文呈现的结论对评估指标稳健。

### C.7 通过节点度分布分析自适应搜索行为

为获得我们方法自适应特性的细致视角，我们分析在 LiveCodeBench 上用 DeepSeek-V3 生成的搜索树的节点度分布，见图 12。结果显示两种截然不同的行为。AB-MCTS-M 明显偏爱聚焦深度的搜索，约 90% 的非叶节点具有较小的度（1–3）。然而，其长尾分布（度数最高达 40）证实它会在需要时自适应地加宽搜索。相比之下，AB-MCTS-A 执行宽得多的搜索。低度节点（1–3）仅占其非叶节点的约 30%，且分布广泛铺开，度数超过 100。这种对搜索树的自适应塑形与基线更僵硬的模式形成鲜明对比，为我们框架的灵活性提供了有力证据。

图 12：
节点度分布揭示我们方法的自适应搜索本质。
该图展示搜索预算 $N=128$ 下每个度数（横轴）的节点频率（纵轴，对数尺度）。

### C.8 标准 MCTS 中固定分支因子 $w$ 的消融

表 6：
标准 MCTS 在 LiveCodeBench 上不同固定分支因子（$w$）的性能。
报告 Pass@1 分数。最佳结果以粗体显示。

|  |  |  |  |
| --- | --- | --- | --- |
| 指标 | $w=3$ | $w=5$ | $w=10$ |
| Pass@1 | 0.429 ± 0.018 | 0.432 ± 0.021 | 0.402 ± 0.015 |

我们在 LiveCodeBench 上使用 DeepSeek-V3 测试了固定分支因子（$w$）为 3、5、10 的标准 MCTS。结果总结于表 6。我们发现 $w=5$ 在测试值中取得最佳性能。关键的是，更小与更大的宽度都会导致性能下降，凸显了该基线对这一超参数的敏感性。这一发现凸显了我们自适应方法的关键优势：在搜索期间动态调整有效分支因子。

### C.9 AB-MCTS 性能的稳健性

在其他基线方法中，分支因子要么预先确定、要么由超参数决定。例如，我们需要在标准 MCTS 中预定义分支因子。然而，宽度 vs. 深度的效率强烈依赖于任务类型与 LLM。这反映在表 1 与表 2 中：AB-MCTS 在各种任务类型上表现稳健，而其他方法在某些任务上出色、在另一些任务上则不然。这归因于 AB-MCTS 的自适应分支本质：算法依据观测到的奖励适应变宽或变深的方向。这在 LLM 推理时扩展的语境下是有益的，因为近来 LLM 被用于求解各类任务（如数学任务、编程任务等），一个开箱即用、适用于各种任务类型的搜索算法有很高的需求。

### C.10 迈向推进 LLM 推理时扩展的帕累托前沿

在本节中，我们提出以下两个旨在推进 LLM 推理时扩展帕累托前沿的未来工作方向：

1. 通过难度估计增强自适应性：我们提议通过从收集的奖励中显式估计问题难度，来增强算法现有的深度-宽度平衡。对困难问题（以低奖励识别），策略将动态切换，例如从深搜索（AB-MCTS-M）切换到宽搜索（AB-MCTS-A）。这源于最优搜索策略依赖于难度的发现（Snell et al., 2025）。
2. 多 LLM 协同搜索：我们还提出一种在单次搜索中利用不同 LLM 多样优势的方法。其实现方式是把 AB-MCTS 扩展为多个 GEN 节点，每个 LLM 一个。

我们在第 D 节中详述第二个方向（协同搜索）的具体方法与初步实验结果。

## 附录 D 多 LLM AB-MCTS

视任务而定，使用多于一个 LLM 进行答案搜索（Chen et al., 2025）可能是有利的。例如，若 LLM A 能生成更多样的初始答案，而 LLM B 擅长精炼，那么用两个模型共同构建答案树有望提升性能。本节展示如何把 AB-MCTS 扩展到有多个 LLM 可用于答案生成的场景，并报告 ARC-AGI-2 上的实验结果，展示所提方法的有效性。

### D.1 方法

#### D.1.1 多个 LLM 作为答案生成器

设有 $L$ 个 LLM 可用于答案生成。沿用式 (2) 引入的记号，我们用 $f_{\text{LLM}}^{l}$ 表示由第 $l$ 个 LLM 实现的答案生成器，$l=1,\dots,L$。整体流程与单 LLM AB-MCTS（算法 1）相同，只是增加了为节点扩展选择 $L$ 个可用生成器之一的一步。该选择发生在每个扩展阶段，利用答案树 $T$ 的当前状态。然后使用所选生成器 $f_{\text{LLM}}^{l}$ 扩展所选节点。我们为这一生成器选择过程引入两种不同的算法。

#### D.1.2 生成器选择算法 I：单 GEN 节点

在该算法中，节点选择与 AB-MCTS 完全相同，随后是额外的生成器选择步骤。在此步骤中，整个答案树 $T$ 中的每个节点 $N$ 都标注了产生它的生成器的索引 $l$。对每个生成器，我们得到节点集

$$
\mathcal{N}_{l}\subseteq T,
$$

其中包含它已生成的全部节点；若该生成器尚未被选中过，则 $\mathcal{N}_{l}$ 为空。$\mathcal{N}_{l}$ 中节点的分数用于计算该生成器 $l$ 将生成的新节点期望分数的后验分布。在算得全部 $L$ 个后验后，应用 Thompson 采样：从每个分布抽取一个样本，采样最高的生成器被选中用于节点扩展。这些后验的建模方式与用于节点扩展目标选择的分布相同，详见下文。

带生成器选择算法 I 的多 LLM AB-MCTS-M。
在该算法中，多 LLM AB-MCTS-M 把各生成器当作混合效应模型中的组，定义为

$$
r_{\tilde{N}}=\alpha_{l}+\sigma_{y}\epsilon_{\tilde{N}},\quad\alpha_{l}=\mu_{\alpha}+\sigma_{\alpha}\epsilon_{l}, \tag{22}
$$

$$
\epsilon_{\tilde{N}}\sim\mathcal{N}(0,1),\quad\epsilon_{l}\sim\mathcal{N}(0,1), \tag{23}
$$

其中组索引 $j$ 已被替换为式 (9)–(10) 中的生成器索引 $l$。至于先验分布，我们可以使用式 (11) 中的先验。在用 $\mathcal{N}_{l}$ 为所有 $l$ 计算分数后验分布后，我们执行 Thompson 采样选择一个生成器。

带生成器选择算法 I 的多 LLM AB-MCTS-A。
在该算法中，多 LLM AB-MCTS-A 为每个第 $l$ 个生成器指派一个独立先验——Gaussian（式 (12)–(17)）或 Beta（式 (18)–(20)），取决于分数度量——并用 $\mathcal{N}_{l}$ 中节点的分数把这些先验更新为后验。在为所有 $l$ 算得后验后，我们执行 Thompson 采样选择一个生成器。

#### D.1.3 生成器选择算法 II：多个 GEN 节点

另一种方法是给树中的每个节点挂上多个 GEN 节点作为子节点——每个可用生成器（共 $L$ 个）一个。在扩展目标选择过程中的每个节点 $N$，进行如下流程：

1. AB-MCTS 选择逻辑在与每个生成器关联的子树内独立应用。也就是说，对每个生成器 $l$，我们运行一个考虑其关联 GEN 节点与它先前从节点 $N$ 生成的任何子节点的选择过程。
2. 用 Thompson 采样为每个生成器 $l$ 识别最佳节点（GEN 节点或既有子节点）。
3. 最后，比较上一步选出的 $L$ 个最佳节点的分数，选择总分最高的一个。

该算法旨在更好地捕捉搜索树的局部语境，允许在解题过程的每个具体阶段自适应地选择最合适的生成器。

### D.2 实验

在本节中，我们通过报告 ARC-AGI-2（Chollet et al., 2025）的结果与分析，评估多 LLM AB-MCTS 的有效性。ARC-AGI-2 是在原 ARC-AGI 基础上增强的基准，专为严格评估人工智能系统更高层认知能力而设计。它保持与 ARC-AGI 相同的基本原则，强调需要一般流体智力而非大量先验知识或记忆的任务。我们选择这一即便对前沿 LLM 也难以求解（成功率低于 5%（Chollet et al., 2025））的基准，来评估能否组合多个前沿推理 LLM 以在挑战性任务上获得更好性能。

#### D.2.1 实验设置

在本实验中，我们在构成 ARC-AGI-2 公开评估集的 120 道题上评估我们的方法。对每道题，生成预算设为 250。解生成与精炼流程与 ARC-AGI-1 实验相同：模型被指示以 Python 代码生成变换规则，搜索由与生成代码正确求解的演示样例数对应的奖励信号引导。在解生成上，我们使用三个前沿推理模型：Gemini-2.5 Pro（gemini-2.5-pro-preview-05-06）（Gemini Team, 2025）、o4-mini（o4-mini-2025-04-16）（OpenAI, 2025b）与 DeepSeek-R1-0528（deepseek-r1-0528）（DeepSeek-AI, 2025）。所有模型的温度均设为 0.6。

为初步评估多 LLM AB-MCTS 的潜力，我们使用 Pass@k 指标。该指标衡量在 $k$ 次尝试内是否至少找到一个正确解。这不同于官方 ARC-AGI-2 竞赛标准（通常采用 Pass@2 准则，即两个提交的最终答案之一必须正确）。评估 Pass@2 需要额外的选择机制从搜索历史中识别有希望的候选。因此，本实验通过 Pass@k 聚焦搜索能力本身。由于所用前沿推理模型的 API 成本可观，我们聚焦于单 LLM AB-MCTS-A 与多 LLM AB-MCTS-A（以及 o4-mini 的重复采样）的评估，因为它在我们 ARC-AGI-1 实验中运行效率最高。此外，我们的实验采用生成器选择算法 II（细节见第 D.1.3 节）。

#### D.2.2 结果

图 13：各生成预算下 ARC-AGI-2 的 Pass@k（覆盖率）。测试的方法为重复采样、AB-MCTS 与多 LLM AB-MCTS 方法。

我们把所提方法与重复采样（ARC-AGI-1 实验中效率最高的方法）进行比较，结果见图 13。如图所示，使用 o4-mini 模型的重复采样在公开评估集上取得 23% 的 Pass@k 成功率，而使用 o4-mini 的单模型 AB-MCTS 把成功率提升到 27.5%。随着生成预算增加（尤其在大约 50 预算之后），AB-MCTS 相对重复采样的性能优势变得更加明显。

通过采用整合 Gemini-2.5-Pro 与 DeepSeek-R1-0528 的多 LLM AB-MCTS，我们进一步提升了性能，最终为超过 30% 的问题找到了正确解。值得注意的是，尽管 DeepSeek-R1-0528 的单体表现较低，把它纳入多 LLM 框架带来了已解问题数量的增加。

#### D.2.3 分析

图 14：多 LLM AB-MCTS-A 在 120 道 ARC-AGI-2 问题上的 LLM 使用分布。试验按演示样例获得的最大奖励排序（奖励越高越靠左）。带星号的试验表示找到了正确的最终解。

多 LLM AB-MCTS 框架展示了依据问题特征把不同 LLM 有效分配给问题的能力。如图 14 所示，LLM 使用的分布因问题而异。对从演示样例快速获得高奖励的试验（图左侧），往往分配更强的模型。相反，对较难获得高奖励的试验（图右侧），模型的使用更为均衡。

图 15：在 ARC-AGI-2 上使用多 LLM AB-MCTS-A 的一次成功试验的示例搜索树。每个节点中的数字表示生成步骤，颜色表示所选 LLM。黄色节点生成了正确解决测试用例的代码。该问题未被任何单一模型独立解决。

![Refer to caption](2503.04412v5/solution_example_v5.png)

图 16：模型协作的示例。在此例中，DeepSeek-R1-0528 精炼了 o4-mini 生成的一个错误中间解（来自图 15 所示问题），产出了最终的正确解。

此外，我们观察到任何单一 LLM 都无法解决的问题通过多模型协作得到解决的实例。这表明存在超越简单地把最佳模型匹配到问题的协同交互。图 15 与图 16 描绘了一个搜索过程：o4-mini 生成的一个错误解成为 DeepSeek-R1-0528 与 Gemini-2.5-Pro 的有用提示，二者随后协作产出了正确解。这一结果表明，多 LLM AB-MCTS 能够促进异构前沿 LLM 之间灵活而有效的协作。

### D.3 挑战与未来工作

虽然我们的主要评估聚焦于使用 Pass@k 指标的搜索能力，我们还进行了一个基于 Pass@2 准则的初步评估供参考。使用一个简单的基于规则的方法选择两个最终答案（优先选择搜索后期生成的高奖励代码），多 LLM AB-MCTS 取得了 19.2% 的 Pass@2。虽然这是一个有希望的结果，但与 30% 的 Pass@250 相比仍有超过 10 个百分点的显著差距。未来工作应聚焦于通过开发更精巧的最终答案选择算法来缩小这一差距。潜在方向包括构建更准确的奖励模型，或集成 LLM-as-a-Judge 以对候选解进行更细致的评估。

