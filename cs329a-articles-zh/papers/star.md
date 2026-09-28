---
title: "STaR：用推理自举推理"
title_en: "STaR: Bootstrapping Reasoning With Reasoning"
arxiv: 2203.14465
source: https://arxiv.org/abs/2203.14465
crawled: 2026-09-23
translated: 2026-09-23
---

# STaR：用推理自举推理

> 原文：[STaR: Bootstrapping Reasoning With Reasoning](https://arxiv.org/abs/2203.14465) · Stanford CS329A 指定阅读

**脚注：这些作者对本文贡献相同

Eric Zelikman
Email: [ezelikman@stanford.edu](mailto:)
  
Yuhuai Wu
Email: [yuhuai@stanford.edu](mailto:)
  
Jesse Mu
所属机构：斯坦福大学计算机科学系
Email: [muj@stanford.edu](mailto:)
  
Noah D. Goodman
所属机构：斯坦福大学计算机科学系
Email: [ngoodman@stanford.edu](mailto:)

所属机构：Google Research

###### 摘要

生成逐步的「思维链」（chain-of-thought）推理依据（rationale）可以提升语言模型在数学或常识问答等复杂推理任务上的表现。然而，要诱导语言模型生成推理依据，目前要么需要构建大规模的推理依据数据集，要么牺牲准确性而只使用少样本推理。我们提出一种技术，迭代地利用少量带推理依据的样本与一个不带推理依据的大数据集，自举出执行愈发复杂推理的能力。这一技术，即「自学习推理器」（Self-Taught Reasoner，STaR），依赖一个简单的循环：以少量带推理依据的样本为提示，为许多问题生成推理依据来作答；如果生成的答案是错的，就在给出正确答案的前提下再次尝试生成推理依据；在最终得到正确答案的所有推理依据上做微调；重复上述过程。我们表明，与微调后直接预测最终答案的模型相比，STaR 在多个数据集上显著提升性能，并在 CommonsenseQA 上与微调一个 30× 大的最先进语言模型的表现相当。因此，STaR 让模型能够通过学习自身生成的推理来改进自己。

## 1 引言

人类的决策往往是延伸思维链的结果（James, 1890；Ericsson & Simon, 1984）。近期工作表明，显式的中间推理（「推理依据」）同样能提升大型语言模型（LLM）的表现（Rajani et al., 2019；Shwartz et al., 2020；Nye et al., 2021；Wei et al., 2022；Marasović et al., 2021；Lampinen et al., 2022）。例如，Nye et al. (2021) 证明，被显式训练为使用「草稿纸」（scratchpad）记录中间步骤的 LLM，能在算术上取得完美的分布内性能与出色的分布外泛化，而被训练为直接预测答案的模型两者皆不可得。这些工作表明，在给出最终答案之前先生成显式推理依据（「推理依据生成」），对 LLM 在多样任务上的价值，包括数学推理、常识推理、代码评估、社会偏见推断与自然语言推断。然而，诱导推理依据生成的两种主要方法都有严重缺陷。

推理依据生成的一种做法是构建一个推理依据微调数据集，或由人工标注者手工完成，或用手工设计的模板自动完成（Rajani et al., 2019；Shwartz et al., 2020；Nye et al., 2021；Cobbe et al., 2021）。人工方法昂贵，且为每个有趣的问题构建这样的数据集并不可行（Rajani et al., 2019）。与此同时，基于模板的方法依赖自动生成的推理依据，但只有当通解已知（Nye et al., 2021）或可以设计合理的硬编码启发式时才奏效（Shwartz et al., 2020）。

另一种替代方案是利用上下文学习，只在语言模型提示中包含少量推理依据示例。这已被证明能在数学与符号推理任务上相对不带推理依据的提示（「直接」提示）提升准确率（Nye et al., 2021；Wei et al., 2022）。然而，尽管带推理依据的少样本技术往往胜过其非推理对应方法，它们通常显著逊于用更大数据集微调的直接预测答案模型（Nye et al., 2021；Wei et al., 2022）。

Q: What can be used to carry a small dog? Answer Choices: (a) swimming pool (b) basket (c) dog show (d) backyard (e) own home A:  The answer must be something that can be used to carry a small dog. Baskets are designed to hold things. Therefore, the answer is basket  (b).

图 1：STaR 概览以及在 CommonsenseQA 上一个 STaR 生成的推理依据。虚线表示微调外循环。问题与标准答案应存在于数据集中，而推理依据由 STaR 生成。

在本文中，我们采用一条不同的路径：通过利用 LLM 既有的推理能力，我们迭代地*自举*生成高质量推理依据的能力。具体而言，我们少样本提示一个大语言模型自生成推理依据，并通过在那些能导向正确答案的推理依据上微调来进一步精炼模型的能力。我们重复这一过程，每次都用改进后的模型生成下一个训练集。这是一个协同过程：推理依据生成的改进改善了训练数据，训练数据的改进又进一步改善推理依据生成。

然而，我们发现这一循环最终无法解出训练集中的新问题，因为它对未能解决的问题得不到直接的训练信号。为克服这一问题，我们提出合理化（rationalization）：对模型未能正确作答的每个问题，我们通过向模型提供正确答案来生成新的推理依据。这让模型能够反向推理——给定正确答案，模型能更容易地生成有用的推理依据。这些推理依据随后被收集为训练数据的一部分，往往能提升整体准确率。

由此我们提出自学习推理器（STaR，图 1）方法，一种可扩展的自举方法，让模型学会生成自己的推理依据，同时学会求解越来越难的问题。在我们的方法中，我们重复以下过程：在每次迭代中，首先用当前模型的推理依据生成能力尝试解题以构建微调数据集；然后用合理化增强该数据集，为模型未能解决的问题论证标准答案；最后在合并的数据集上微调大语言模型。

将 STaR 应用于算术、数学应用题与常识推理，我们观察到它能有效地将少量少样本提示转化为一个大规模推理依据数据集，带来显著的性能提升。在 CommonsenseQA（Talmor et al., 2019）上，我们发现 STaR 相对少样本基线（+35.9%）与微调后直接预测答案的基线（+12.5%）均有提升，并与一个大 30× 的微调模型表现相当（72.5% vs. 73.0%）。

因此，我们做出以下贡献：

1. 我们提出一种自举机制，从少量带推理依据的初始示例出发迭代生成推理依据数据集——无需检查新生成推理依据的正确性。
2. 我们用合理化补充推理依据生成：模型被要求论证一个答案，然后像它是在没有任何提示的情况下自己想出该推理依据一样被微调。我们表明合理化加速并改善了自举过程。
3. 我们在数学与常识推理两个领域用多种消融实验评估这些技术。
4. 我们提出据我们所知第一个让预训练大语言模型迭代地利用其语言建模能力进行自我改进的技术。

## 2 背景与相关工作

#### 上下文学习

近来涌现了一批探索大语言模型执行上下文学习能力的工作（Brown et al., 2020；Wei et al., 2022）。本质上，上下文学习把少样本学习当作一个语言建模问题：在上下文（即提示）中展示若干示例，让模型学习并识别可应用于新示例的模式。有人从贝叶斯推断的角度基于语言建模目标研究上下文学习（Xie et al., 2021），也有人尝试以「归纳头」（induction heads）更机制性地描述这一过程（Olsson et al., 2022）。此外，提示配置的差异已知会对少样本性能产生巨大影响。甚至有研究发现，把少样本提示替换为可在嵌入空间中优化的「软提示」能带来可观收益（Lester et al., 2021）。我们不强调问题的表示，而是聚焦模型输出；特别是，我们关注模型在得出结论之前推理问题的能力。

#### 推理依据

关于推理依据对语言模型性能影响的早期工作之一是 Rajani et al. (2019)，它表明在答案前带有显式推理依据的数据集上训练语言模型，可以提升模型生成最终答案的能力。然而，这需要人工标注者手动标注成千上万个训练示例的人类推理。近来，Nye et al. (2021) 证明逐步的「草稿纸」能提升微调后 LLM 在算术、多项式求值与程序评估等任务上的性能与泛化。类似地，Wei et al. (2022) 使用单个少样本「思维链」推理提示，在无需微调的情况下提升模型在一组任务上的表现。最后，Polu et al. (2022) 表明课程学习方法有助于求解形式数学问题，只要满足：1) 问题被翻译为 Lean（一种定理证明语言（de Moura et al., 2015））；2) 可以直接评估证明的有效性；3) 可以为每个问题采样大量候选解；4) 已训练一个单独的价值函数模型；5) 从 GPT-f（一个已在大规模数学数据集上微调的模型（Polu & Sutskever, 2020））出发。我们注意到，有许多领域并不全部满足这些条件。此外，也有工作试图解释推理依据为何有这种有益效果：有人从隐变量模型的视角分析其影响（Zhou et al., 2020），也有人为中间任务监督的益处提供了形式化证明（Wies et al., 2022）。

#### 迭代学习

已有多种迭代学习算法被提出，其中找到的解或成功方法又被反过来用于寻找更多解（Anthony et al., 2017；Vani et al., 2021；Polu et al., 2022）。Anthony et al. (2017) 提出专家迭代（Expert Iteration，ExIt），一种强化学习技术，是我们方法的重要灵感来源。本质上，它由「学徒」的自博弈循环组成，随后是来自较慢「专家」反馈的模仿学习，再用现已改进的学徒替换专家。Polu et al. (2022) 将 ExIt 应用于形式推理，而 Vani et al. (2021) 将迭代学习应用于视觉问答，使用可组合式的模块化网络。STaR 与专家迭代方法（Anthony et al., 2017）还有更多相似之处。例如，根据最终答案是否与目标匹配来过滤生成样本，可以看作专家反馈。不过，我们拥有一个固定的「专家」，且不训练单独的价值函数。

#### 自然语言解释

自然语言解释也从可解释机器学习的角度被讨论，侧重正当性论证而非推理（Camburu et al., 2018；Chen et al., 2021）。这条工作线的动机主要植根于可解释决策，与 Rajani et al. (2019) 类似，通常并未发现要求事后解释能提升模型性能。

## 3 方法

### 3.1 推理依据生成自举（不含合理化的 STaR）

给定一个预训练 LLM $M$ 与一个初始的问题 $x$ 及答案 $y$ 数据集：$\mathcal{D}=\{(x_{i},y_{i})\}_{i=1}^{D}$。我们的技术从一个小的*提示*集 $\mathcal{P}$ 出发，其中是带有中间*推理依据* $r$ 的示例：$\mathcal{P}=\{(x^{p}_{i},r^{p}_{i},y^{p}_{i})\}_{i=1}^{P}$，其中 $P\ll D$（例如 $P=10$）。与标准少样本提示一样，我们将该提示集拼接到 $\mathcal{D}$ 中每个示例之前，即 $x_{i}=(x^{p}_{1},r^{p}_{1},y^{p}_{1},\dots,x^{p}_{P},r^{p}_{P},y^{p}_{P},x_{i})$，这促使模型为 $x_{i}$ 生成一个推理依据 $\hat{r}_{i}$，随后给出答案 $\hat{y}_{i}$。我们假设导向正确答案的推理依据质量优于导向错误答案的推理依据。因此，我们过滤生成的推理依据，只保留那些得到正确答案的（$\hat{y}_{i}=y_{i}$）。我们在该过滤后的数据集上微调基础模型 $M$，然后用新微调的模型生成新的推理依据并重启该过程。我们不断重复，直到性能达到平台期。注意，在此过程中，一旦收集到新数据集，我们都从原始预训练模型 $M$ 开始训练，而非持续训练同一个模型，以避免过拟合。算法 1 给出了该算法的概要。

STaR 可以看作对一种 RL 风格策略梯度目标的近似。为看清这一点，注意 $M$ 可被视为一个离散隐变量模型 $p_{M}(y\mid x)=\sum_{r}p(r\mid x)p(y\mid x,r)$；换言之，$M$ 先采样一个隐推理依据 $r$ 再预测 $y$。现在，给定指示奖励函数 $\mathbbm{1}(\hat{y}=y)$，数据集上的总期望奖励为

$$
J(M,X,Y)=\sum_{i}\mathbb{E}_{\hat{r}_{i},\hat{y}_{i}\sim p_{M}(\cdot\mid x_{i})}\mathbbm{1}(\hat{y}_{i}=y_{i}), \tag{1}
$$

$$
\nabla J(M,X,Y)=\sum_{i}\mathbb{E}_{\hat{r}_{i},\hat{y}_{i}\sim p_{M}(\cdot\mid x_{i})}\left[\mathbbm{1}(\hat{y}_{i}=y_{i})\cdot\nabla\log p_{M}(\hat{y}_{i},\hat{r}_{i}\mid x_{i})\right], \tag{2}
$$

其中梯度通过策略梯度的标准 log-导数技巧得到。注意，指示函数丢弃了所有未导向正确答案 $y_{i}$ 的采样推理依据的梯度：这正是 STaR 中的过滤过程（第 5 行）。因此，STaR 通过以下方式近似 $J$：(1) 贪心解码 $(\hat{r}_{i},\hat{y}_{i})$ 的样本来降低该估计的方差（代价是推理依据的探索可能有偏），(2) 在同一批数据上走多个梯度步（类似某些策略梯度算法（Schulman et al., 2017））。这些近似使 STaR 成为一个简单且广泛适用的方法，可以用标准的 LLM 训练机制实现；未来工作应更深入地研究 STaR 与上述 RL 目标之间的联系。

### 3.2 合理化

Q: Where do you put your grapes just before checking out?

Answer Choices:

(a) mouth

(b) grocery cart (CORRECT)

(c) super market

(d) fruit basket

(e) fruit market

A: The answer should be the place where grocery items are placed before checking out. Of the above choices, grocery cart makes the most sense for holding grocery items. Therefore, the answer is grocery cart (b).

图 2：我们用于合理化（而非推理依据生成）的少样本提示提示示例，使用 Wei et al. (2022) 的推理依据，其中提示以绿色包含在内，其后是模型生成的推理依据与答案。

推理依据生成自举算法存在一个局限。由于模型只在它答对的示例上训练，当模型无法解出训练集中的新问题时，改进就会终止。这从根本上是因为算法无法从失败的示例中获得任何训练信号。受 Rajani et al. (2019) 启发，我们提出一种称为「合理化」（rationalization）的技术。具体而言，我们把答案作为提示提供给模型，要求它以与上一步推理依据生成相同的风格生成推理依据。给定答案后，模型能够反向推理，因而更容易生成导向正确答案的推理依据。例如，在图 2 中，我们在提示中提供「(b) grocery cart 是正确答案」这一提示来生成推理依据。我们对模型在推理依据生成中未能解决的问题应用合理化。当把合理化生成的推理依据加入数据集时，我们不在其对应提示中包含该提示，就好像模型是在没有提示的情况下自己想出了推理依据。过滤之后，我们在先前生成的数据集与合理化生成的数据集的合并集上微调。

算法 1　STaR

输入 $M$：一个预训练 LLM；数据集 $\mathcal{D}=\{(x_{i},y_{i})\}_{i=1}^{D}$（含少样本提示）

1: $M_{0}\leftarrow M$  # 复制原始模型
2: for $n$ in $1...N$ do  # 外循环
3: 　　$(\hat{r}_{i},\hat{y}_{i})\leftarrow M_{n-1}(x_{i})\quad\forall i\in[1,D]$  # 执行推理依据生成
4: 　　$(\hat{r}^{\text{rat}}_{i},\hat{y}^{\text{rat}}_{i})\leftarrow M_{n-1}(\text{add\_hint}(x_{i},y_{i}))\quad\forall i\in[1,D]$  # 执行合理化
5: 　　$\mathcal{D}_{n}\leftarrow\{(x_{i},\hat{r}_{i},y_{i})\mid i\in[1,D]\land\hat{y}_{i}=y_{i}\}$  # 用标准答案过滤推理依据
6: 　　$\mathcal{D}^{\text{rat}}_{n}\leftarrow\{(x_{i},\hat{r}^{\text{rat}}_{i},y_{i})\mid i\in[1,D]\land\hat{y}_{i}\neq y_{i}\land\hat{y}^{\text{rat}}_{i}=y_{i}\}$  # 过滤合理化后的推理依据
7: 　　$M_{n}\leftarrow\text{train}(M,\mathcal{D}_{n}\,{\color[rgb]{0,0,1}\cup\,\mathcal{D}^{\text{rat}}_{n}})$  # 在正确解上微调原始模型——内循环
8: end for

算法 1 描述了完整算法，蓝色部分对应合理化。去掉这些部分后，算法 1 即为不含合理化的 STaR。图 1 提供了概览示意图。在合理化生成的数据集上微调有一个关键好处：让模型接触到那些原本不会出现在其微调数据集中的困难问题。这可以理解为促使模型对其未能成功的问题「跳出框框思考」。合理化的一个次要好处是数据集规模的增加。

## 4 实验

在实验中，我们聚焦算术、常识推理与小学数学，以展示 STaR 的广度。特别是，对于算术，我们遵循受 Nye et al. (2021) 启发的设定。对于常识问答，我们遵循 Xie et al. (2021)、Wei et al. (2022) 的做法，使用该领域广泛使用的多选数据集 CommonsenseQA（CQA）（Talmor et al., 2019）。对于小学数学，我们使用 Cobbe et al. (2021) 的 GSM8K。

### 4.1 实验方案

我们使用 GPT-J 作为基础语言模型，并使用 GPT-J 仓库（Wang, 2021）提供的微调脚本。我们选择 GPT-J 这个 6B 参数模型，因为其检查点与微调代码公开可用（Wang, 2021），且模型足够大，能生成质量不俗、可供自举的推理依据。关于 GPT-J 与我们微调的更多超参数细节见附录 H。遵循 Wang (2021) 的默认设定，我们进行 100 步学习率预热，此后使用恒定学习率。除非另有说明，我们在第一个外循环从 40 个训练步开始，每个外循环将微调训练步数增加 20%。总体而言，我们发现开始时训练得更慢最终有利于模型性能。我们预计通过彻底的超参数搜索还能进一步改进——由于计算限制，我们将其留作未来工作。

对于算术问题，我们首先按 Nye et al. (2021) 引入的格式生成一个包含 50,000 道随机采样问题（数字位数上均匀分布）的数据集。对于算术的每个外循环迭代，我们从该数据集采样 10,000 道题。我们对每个数字位数使用 10 个随机少样本推理依据示例作为对应的少样本提示。对于 CommonsenseQA 训练集中全部 9,741 道题，我们把问题加入少样本推理依据提示，并提示模型为该问题生成推理依据与答案。对于 CQA 上的少样本提示，我们从 Wei et al. (2022) 所用的同样 10 个问题出发，略微修改推理依据以修正一个错误答案并更明确地引用相关知识。我们在附录 B 中给出这些修改后的提示。
注 1：基于 Min et al. (2022)，这不太可能显著影响 Wei et al. (2022) 的少样本性能。这些提示充当我们完整的解释集合。我们持续运行 STaR 直到性能饱和，并报告最佳结果。

在执行合理化时，我们发现第一次迭代之后的外循环迭代中包含或省略少样本提示，对该方法的最终性能没有实质影响。不过存在一些细微差别，我们在第 5 节进一步讨论，因此除非另有说明，我们使用少样本提示。

### 4.2 数据集

#### 算术

```
Input:
6 2 4 + 2 5 9
Target:
<scratch>
6 2 4 + 2 5 9 , C: 0
2 + 5 , 3  C: 1
6 + 2 , 8 3  C: 0
, 8 8 3  C: 0
0 8 8 3
</scratch>
8 8 3
```

图 3：一个带草稿纸的 3 位数算术问题示例的可视化。C 对应上一位数求和的进位。

算术任务是计算两个 $n$ 位数整数的和。我们基于 Nye et al. (2021) 的描述生成数据集，并在图 3 中可视化一个草稿纸示例。直到并包含「Target:」之前的所有内容都作为提示的一部分给出，模型被要求生成草稿纸（由「<scratch>」标记开始/结束）与最终答案，如 Nye et al. (2021) 所述。草稿纸的每一行对应从个位到最高位的每对数字的求和、逐步累积的答案数位，以及一个表示前一对数字之和是否至少为 10 的进位。我们为 1 到 5 位数提供少样本提示。执行合理化时，我们在「Target」之后包含正确答案，并要求模型生成草稿纸，然后在草稿纸之后重现正确答案。

#### CommonsenseQA

多选常识推理任务 CommonsenseQA（Talmor et al., 2019）（CQA）构建自 ConceptNet——一个拥有超过百万节点的概念及其关系语义图（Speer et al., 2016）。Talmor et al. (2019) 为每道题在 ConceptNet 中识别一组「目标」概念，这些目标概念与一个「源」概念共享语义关系。然后每道题经众包编写，使读者能识别一个目标概念，同时提及源概念。此外，加入两个干扰答案。该数据集有 12,247 道题，每题五个选项，其中 9,741 道在训练集，1,221 道在开发集，1,285 道在（保留的）测试集。

与 ConceptNet 的广泛多样性相对应，CQA 包含多样的题目，需要在标准世界知识之上进行常识推理，人类表现为 89%（Talmor et al., 2019）。许多人指出 CQA 在若干维度（包括性别）上存在偏差（Rajani et al., 2019）。我们在附录 G 中讨论这如何可能影响我们的方法。此外还有许多拼写错误与本质上歧义的问题。
注 2：例如，「Billy bought coffee and waited for his wife to arrive from France. Where might he have been?」的选项中同时包含 airport 与 train station。正确答案或许出人意料，是 train station。尽管存在这些问题我们仍使用它，因为它是一个同时依赖常识世界知识与简单推理的通用问答数据集，是我们方法的一个良好测试床。

#### 小学数学（GSM8K）

我们还在小学数学（GSM8K）数据集上评估，它包含 7,473 道训练题与 1,319 道测试题的小学程度应用题（Cobbe et al., 2021）。这些数学题以自然语言表述，需要两到八步计算才能得到最终答案。该数据集结合了算术与常识推理所需的技能。

### 4.3 符号推理：算术上的结果

外循环每次迭代中模型在 1-5 位数上的准确率绘制于图 4。运行 STaR 16 次迭代后，总体准确率为 89.5%。作为参考，在 10,000 个不带推理依据的示例上训练 5,000 步的基线达到 76.3% 的准确率。值得注意的是，算术问题上的少样本准确率非常低，即便带有推理依据：2 位数加法的准确率不足 1%，更多位数的准确率接近零。

（a）不含合理化

（b）含合理化

图 4：算术任务上含与不含合理化的 STaR 每次迭代 $n$ 位数求和准确率的可视化。每条曲线对应两个 $n$ 位数相加的准确率。

图 5：我们在第 20 次迭代时向含合理化的 STaR 引入更多位数。

借助合理化，准确率能够提升得尤其快。在模型生成的草稿纸上做一次微调迭代后，2 位数加法从不足 1% 提升到 32%。不含合理化时，性能提升是阶段式的：模型通常在 $n$ 位数求和上表现不佳，直到它在 $(n-1)$ 位数求和上有良好表现。有合理化时，模型可以一次学习多个位数，尽管准确率并不均等。合理化使许多问题可以被少样本解出，因此我们以 300 步开始 STaR 训练（注意，不含合理化时这样做会导致 11 位数加法上过拟合），并每迭代增加 20 步训练。

我们还做了一个实验：从第 20 次迭代之前开始，向含合理化的 STaR 继续预训练更多位数，同时保持每次迭代的训练样本总数不变。我们发现，这不仅似乎能快速提升初始位数集合上的性能，而且在训练中从未见过的 9 与 10 位数示例上评测时，模型成功解出了许多这类分布外问题。如图 5 所示，引入这些位数似乎使训练变得不太稳定，但确切原因尚不清楚。

### 4.4 自然语言推理：常识问答

CommonsenseQA（CQA）设定带来了若干新挑战。在算术任务中，推理步骤中一个错误的草稿纸（在合理化步骤中程度较轻）极可能导致错误答案。而 CQA 问题是五选一的多选题。因此，无论推理质量如何，随机也会有约 20% 的概率答对。此外，一些简单启发式（如语义相似度）可以在完全不做推理的情况下将其有意义地提升到约 30%，如 Talmor et al. (2019) 所示。

我们按照实验方案中所述评估该数据集，并与若干基线比较。第一个基线是微调 GPT-J 直接输出最终答案，我们称之为「GPT-J Finetuned」。我们还与 Xu et al. (2021) 中微调后直接预测最终答案的 GPT-3 比较，以及与 Wei et al. (2022) 中用思维链（CoT）推理依据做少样本提示的 137B 参数 LaMDA 模型比较。

我们发现，如表 1 所示，不含合理化的 STaR 在整个数据集上胜过直接在最终答案上微调的 GPT-J，尽管训练所用的数据更少。加入合理化将性能提升至 72.5%，远接近于大 30× 的 GPT-3 的 73%。正如预期，我们还看到 STaR 超越了少样本基线，包括大得多的 137B LaMDA 模型（Thoppilan et al., 2022；Wei et al., 2022）。我们预计，若将 STaR 应用于少样本性能更高的模型，准确率还会进一步提升。

#### 案例研究

注意，判断推理依据质量更难：对于算术，可以将它们与标准推理依据比较，但对于 CQA，评估必然是定性的。因此，我们在图 7 中给出一个案例研究。我们观察到所提供的推理依据总体上连贯，且结构与少样本推理依据相似。我们做出以下两点观察：

1. 用 STaR 训练后，我们看到模型能够生成合理的推理依据来求解新问题，这解释了所观察到的性能提升的一部分。
2. 我们还看到，在许多实例中，STaR 相对少样本方式生成的推理依据提升了质量。

表 1：我们评估若干基线，包括带与不带草稿纸的 GPT-J 少样本评估、微调后直接预测答案的 GPT-J 基线，以及应用于 GPT-J 的带与不带合理化的 STaR。我们用 CoT 表示输出推理依据的非 STaR 模型，用 Direct 表示直接预测最终答案的模型。注意，最终 STaR 模型的训练使用了 78.2% 的训练数据集做推理依据生成，另有 8.5% 来自合理化。

|  | CQA 开发集准确率 (%) | 使用的训练数据 (%) |
| --- | --- | --- |
| GPT-3 Direct Finetuned（Xu et al., 2021） | 73.0 | 100 |
| 少样本 Direct GPT-J | 20.9 | $\sim$0 |
| 少样本 CoT GPT-J 3 注 3：我们使用第 4.1 节所述的相同少样本推理依据——即修正拼写错误并提高清晰度。 | 36.6 | $\sim$0 |
| 少样本 CoT LaMDA 137B（Wei et al., 2022） | 55.6 | $\sim$0 |
| GPT-J Direct Finetuned | 60.0 | 100 |
| STaR（不含合理化） | 68.8 | 69.7 |
| STaR（含合理化） | 72.5 | 86.7 |

#### 人工评估

基于这样的观察——STaR 即使对少样本提示本来就能答对的问题也可能提升推理质量——我们进行了一项初步的定性分析。我们从少样本 CoT 与 STaR 生成的推理依据中，随机选取 50 道两者都答对的问题上的推理依据，以及 Rajani et al. (2019) 中这些问题的人工编写推理依据。然后，我们向 Prolific（Palan & Schitter, 2018）上的 20 名众包工人每人展示一个包含 10 道题及对应推理依据的随机子集，推理依据以随机顺序排列，请他们根据哪个最能论证答案来排序。参与者将 STaR 生成的推理依据排在少样本推理依据之上的概率高出 30%（$p=.039$）。这表明，正如案例研究中所提到的，STaR 能提升推理依据生成的质量。

我们还发现，参与者偏好 STaR 生成的推理依据而非人工编写推理依据的概率高出 74%（$p$ < .001）。需要说明的是，我们并不认为这表明达到了人类水平的推理依据生成性能。相反，我们认为它反映了引出高质量推理依据的困难。我们在附录 C 中重现测试提示，并详述众包解释数据集的局限。

#### 失败案例

最后，我们发现了多种有趣的失败案例，其中许多对应标准的逻辑谬误。例如，模型常做出与问题主题相关、但并非论证答案为何为真的陈述。有时，模型声称问题本身已蕴含答案作为论证，而不解释原因。另一些时候，尤其是在训练早期，模型回答得好像它了解某个具体个人，而不是做出一般性陈述——例如说「the king's castle is a place where he feels safe」而非「castles are places where kings feel safe」。我们在附录 A 中给出示例并分析错误。

#### 少样本提示训练

在微调期间包含少样本提示（Wei et al., 2022）似乎有显著的性能收益（不含合理化时从 60.9% 到 68.8%，含合理化时从 69.9% 到 72.5%）。因此，我们一般建议至少在训练的某一部分使用它，尽管我们在第 5 节讨论一些注意事项。

表 2：我们发现 STaR 在 GSM8K 上大幅超越基线，尽管不含合理化的模型仅在 25.0% 的数据上训练，含合理化的模型在 28.7% 的数据集（其中 0.5% 来自合理化）上训练。

|  | GSM8K 测试准确率 (%) | 使用的训练数据 (%) |
| --- | --- | --- |
| 少样本 Direct GPT-J | 3.0 | $\sim$0 |
| 少样本 CoT GPT-J | 3.1 | $\sim$0 |
| GPT-J Direct Finetuned | 5.8 | 100 |
| STaR（不含合理化） | 10.1 | 25.0 |
| STaR（含合理化） | 10.7 | 28.7 |

![Refer to caption](2203.14465v2/counts_heatmap.png)

图 6：模型为解出训练集示例所生成的计算步数与标准答案所用步数的比较。

### 4.5 语言中的数学推理：小学数学

我们再次在 GSM8K 上发现，STaR 大幅超越了带推理依据的少样本或直接预测答案（不带推理依据）的训练，见表 2，少样本提示见附录 I。我们观察到，在该任务上，合理化的使用并未显著提升性能。注意，在训练中，有必要在第 30 次迭代（7,912 步之后）限制训练步数上限，以防止训练过程过长。结果是在不含合理化的 STaR 运行 36 次迭代、再额外进行 10 次含合理化迭代后达到的。

大多数情况下，模型生成的计算步数与人类所走的步数一致（所有迭代中一致率一般在 53% 到 57% 之间）。我们在图 6 中明确可视化这一点。我们看到，当标准答案与模型在计算步数上不一致时，模型通常使用更少的步数。有时这是因为模型跳过了步骤，但偶尔它也找到不同的解法。我们在附录 J 中给出一个示例，模型忽略了冗余信息，用单步解出了一个 7 步的问题。

## 5 讨论与挑战

#### 合理化的影响

一个关键问题是合理化究竟扮演什么角色。直觉上，合理化允许模型逆向工程一个解，或为判断每一步是否让结论更可能提供了一个启发式。这类似于现实世界中已知最终结果、却难以推导出好论证的问题。从数学视角看，推理依据生成从模型 $M$ 提供的分布 $p(r\mid x)$ 中采样推理依据，而合理化以答案为条件，让我们能访问另一个分布 $p(r\mid x,y)$，它可能是更好的推理依据搜索空间。于是合理化可以被视为式 (1) 中目标的一个离策略（off-policy）估计，以带提示增强的模型作为提议分布采样。未来工作应建立合理化与这些 RL 目标之间的更多联系，并更一般地考察合理化何时以及为何能改进学习。

此外，由于采样温度低，不含合理化的输出对应模型对答案最有信心的那些示例。这导致这些示例提供的梯度信号弱于合理化示例，至少在第一次迭代中如此。由于我们每次运行微调迭代都从初始预训练模型重新训练，这一效应的程度也难以直接度量。最后，必须指出，加入「提示」的方法并非能从问题与答案直接推出，在某些情境下提供它可能并不简单。探索不同提示技术的各种影响及其通用性是未来工作的一个方向。

#### 温度

如果想要扩充训练数据集，合理化的一个直觉替代方案是更多、更高温的采样。然而在实践中，我们发现这适得其反。总体而言，它大幅增加了「尽管推理错误却得到正确答案」的可能性，而在糟糕或无关的推理上训练会妨碍泛化。这在算术等更结构化的任务中尤为明显：模型学会用更高温采样方式生成的草稿纸会退化成无意义内容，导致模型停滞不前。总体而言，我们发现以更高温度作为合理化的替代（例如 0.5 或 0.7）一致地得到比仅用推理更差的模型。此外，由于大语言模型的文本生成是顺序式的（即不生成前一个 token 就无法生成后一个 token），生成文本是瓶颈，这在计算上远不如合理化高效。例如，生成 10 个样本输出大约比生成 1 个样本输出慢 10 倍。不过，利用多个样本的一个潜在有价值的方式是使用 Wang et al. (2022) 提出的方法，把多个高温草稿纸的多数投票结果作为标准答案，用以比照低温草稿纸。这可能使 STaR 能应用于只有问题、没有答案的数据集。

#### 少样本提示

一个值得注意的现象是，在采样期间包含少样本提示似乎能显著减少「漂移」——即后续推理依据与初始少样本推理依据集越来越不相似的现象。一个好处是模型可能较少受初始推理依据的质量与难度的约束，理论上允许它更好地泛化。一个潜在的负面影响是推理依据的风格可能与原始提示风格匹配得不那么紧密。另一个好处在于计算资源——更短的提示长度允许采样时使用更短的序列长度。技术上，我们在训练中「关闭」少样本提示的时间点也是一个可调的超参数，但我们将其留作未来工作。此外，通过在初始外循环迭代之后去掉提示，模型在长时间训练后合理化的表现会逐渐变差。因此，用这种方法长时间训练时，可能有必要在训练中保留一些提示。

归根结底，是否在后续训练迭代中包含少样本提示似乎取决于使用场景：当目标是始终遵循特定提示风格（这可能有利于可解释性）时，在采样中包含少样本提示；当目标是更快的训练循环时，可以去掉它们。此外，使用其他数据集或更大模型时，这可能对性能有影响，因此我们建议一般将其视为一个超参数。

## 6 结论

我们提出自学习推理器（STaR），它迭代地改进模型生成推理依据以求解问题的能力。我们少样本提示模型以生成推理依据的方式逐步求解许多问题，然后提示它为做错的问题合理化正确答案。我们在初始即正确的解与合理化得到的正确解上都做微调，并重复该过程。我们发现该技术显著提升了模型在符号推理与自然语言推理上的泛化性能。

STaR 在此存在若干重要局限。为了 STaR 的第一次迭代能够成功，少样本性能必须高于随机，这暗示初始模型必须足够大、具备一定推理能力。例如，我们发现 GPT-2 甚至无法在算术领域从少样本推理自举。另一个局限是，随机性能水平较高的设定（如二元决策）会产生许多糟糕的推理依据，干扰 STaR 方法。在这些设定中如何过滤糟糕的推理是一个开放问题。

尽管如此，我们相信用不带推理的示例来自举推理是一种非常通用的方法，STaR 可以作为许多领域更复杂技术的基础。

## 致谢

我们感谢 Imano Schlag 对本工作的详细反馈，以及 Rose E Wang、Markus Rabe、Aitor Lewkowycz、Rishi Bommasani、Allen Nie、Alex Tamkin 和 Qian Huang。我们感谢 Cem Anil 提供的非常有帮助的洞见：若训练包含少样本推理依据，推理依据微调性能可以提升。我们还感谢 Ben Prystawski 对问卷设计的建议。我们感谢 Google TPU Research Cloud 提供 TPU 访问。

## 参考文献

- [1]

  William James, Frederick Burkhardt, Fredson Bowers, and Ignas K Skrupskelis.
  The principles of psychology, volume 1.
  Macmillan London, 1890.
- [2]

  K Anders Ericsson and Herbert A Simon.
  Protocol analysis: Verbal reports as data.
  the MIT Press, 1984.
- [3]

  Nazneen Fatema Rajani, Bryan McCann, Caiming Xiong, and Richard Socher.
  Explain yourself! leveraging language models for commonsense
  reasoning.
  ACL, 2019.
- [4]

  Vered Shwartz, Peter West, Ronan Le Bras, Chandra Bhagavatula, and Yejin Choi.
  Unsupervised commonsense question answering with self-talk.
  EMNLP 2020, 2020.
- [5]

  Maxwell Nye, Anders Johan Andreassen, Guy Gur-Ari, Henryk Michalewski, Jacob
  Austin, David Bieber, David Dohan, Aitor Lewkowycz, Maarten Bosma, David
  Luan, et al.
  Show your work: Scratchpads for intermediate computation with
  language models.
  arXiv preprint arXiv:2112.00114, 2021.
- [6]

  Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Ed Chi, Quoc Le, and
  Denny Zhou.
  Chain of thought prompting elicits reasoning in large language
  models.
  arXiv preprint arXiv:2201.11903, 2022.
- [7]

  Ana Marasović, Iz Beltagy, Doug Downey, and Matthew E Peters.
  Few-shot self-rationalization with natural language prompts.
  arXiv preprint arXiv:2111.08284, 2021.
- [8]

  Andrew K Lampinen, Ishita Dasgupta, Stephanie CY Chan, Kory Matthewson,
  Michael Henry Tessler, Antonia Creswell, James L McClelland, Jane X Wang, and
  Felix Hill.
  Can language models learn from explanations in context?
  arXiv preprint arXiv:2204.02329, 2022.
- [9]

  Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Jacob Hilton, Reiichiro Nakano,
  Christopher Hesse, and John Schulman.
  Training verifiers to solve math word problems.
  arXiv preprint arXiv:2110.14168, 2021.
- [10]

  Alon Talmor, Jonathan Herzig, Nicholas Lourie, and Jonathan Berant.
  Commonsenseqa: A question answering challenge targeting commonsense
  knowledge.
  In Proceedings of the 2019 Conference of the North American
  Chapter of the Association for Computational Linguistics: Human Language
  Technologies, Volume 1 (Long and Short Papers), pages 4149–4158, 2019.
- [11]

  Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla
  Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell,
  et al.
  Language models are few-shot learners.
  Advances in neural information processing systems,
  33:1877–1901, 2020.
- [12]

  Jason Wei, Maarten Bosma, Vincent Y Zhao, Kelvin Guu, Adams Wei Yu, Brian
  Lester, Nan Du, Andrew M Dai, and Quoc V Le.
  Finetuned language models are zero-shot learners.
  ICLR 2022, 2021.
- [13]

  Sang Michael Xie, Aditi Raghunathan, Percy Liang, and Tengyu Ma.
  An explanation of in-context learning as implicit bayesian inference.
  arXiv preprint arXiv:2111.02080, 2021.
- [14]

  Catherine Olsson, Nelson Elhage, Neel Nanda, Nicholas Joseph, Nova DasSarma,
  Tom Henighan, Ben Mann, Amanda Askell, Yuntao Bai, Anna Chen, and et al.
  In-context learning and induction heads.
  Transformer Circuits, Mar 2022.
- [15]

  Brian Lester, Rami Al-Rfou, and Noah Constant.
  The power of scale for parameter-efficient prompt tuning.
  EMNLP 2021, 2021.
- [16]

  Stanislas Polu, Jesse Michael Han, Kunhao Zheng, Mantas Baksys, Igor
  Babuschkin, and Ilya Sutskever.
  Formal mathematics statement curriculum learning.
  arXiv preprint arXiv:2202.01344, 2022.
- [17]

  Leonardo de Moura, Soonho Kong, Jeremy Avigad, Floris van Doorn, and Jakob von
  Raumer.
  The lean theorem prover (system description).
  In International Conference on Automated Deduction, pages
  378–388. Springer, 2015.
- [18]

  Stanislas Polu and Ilya Sutskever.
  Generative language modeling for automated theorem proving.
  arXiv preprint arXiv:2009.03393, 2020.
- [19]

  Wangchunshu Zhou, Jinyi Hu, Hanlin Zhang, Xiaodan Liang, Maosong Sun, Chenyan
  Xiong, and Jian Tang.
  Towards interpretable natural language understanding with
  explanations as latent variables.
  Advances in Neural Information Processing Systems,
  33:6803–6814, 2020.
- [20]

  Noam Wies, Yoav Levine, and Amnon Shashua.
  Sub-task decomposition enables learning in sequence to sequence
  tasks.
  arXiv preprint arXiv:2204.02892, 2022.
- [21]

  Thomas Anthony, Zheng Tian, and David Barber.
  Thinking fast and slow with deep learning and tree search.
  Advances in Neural Information Processing Systems, 30, 2017.
- [22]

  Ankit Vani, Max Schwarzer, Yuchen Lu, Eeshan Dhekane, and Aaron Courville.
  Iterated learning for emergent systematicity in vqa.
  ICLR 2021, 2021.
- [23]

  Oana-Maria Camburu, Tim Rocktäschel, Thomas Lukasiewicz, and Phil Blunsom.
  e-snli: Natural language inference with natural language
  explanations.
  Advances in Neural Information Processing Systems, 31, 2018.
- [24]

  Hanxiong Chen, Xu Chen, Shaoyun Shi, and Yongfeng Zhang.
  Generate natural language explanations for recommendation.
  arXiv preprint arXiv:2101.03392, 2021.
- [25]

  John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov.
  Proximal policy optimization algorithms.
  arXiv preprint arXiv:1707.06347, 2017.
- [26]

  Ben Wang.
  Mesh-Transformer-JAX: Model-Parallel Implementation of Transformer
  Language Model with JAX.
  <https://github.com/kingoflolz/mesh-transformer-jax>, May 2021.
- [27]

  Sewon Min, Xinxi Lyu, Ari Holtzman, Mikel Artetxe, Mike Lewis, Hannaneh
  Hajishirzi, and Luke Zettlemoyer.
  Rethinking the role of demonstrations: What makes in-context learning
  work?
  arXiv preprint arXiv:2202.12837, 2022.
- [28]

  Robyn Speer, Joshua Chin, and Catherine Havasi.
  Conceptnet 5.5: An open multilingual graph of general knowledge.
  singh 2002 (2016).
  arXiv preprint arxiv:1612.03975, 2016.
- [29]

  Yichong Xu, Chenguang Zhu, Shuohang Wang, Siqi Sun, Hao Cheng, Xiaodong Liu,
  Jianfeng Gao, Pengcheng He, Michael Zeng, and Xuedong Huang.
  Human parity on commonsenseqa: Augmenting self-attention with
  external attention.
  arXiv:2112.03254, December 2021.
  human parity result on CommonsenseQA.
- [30]

  Romal Thoppilan, Daniel De Freitas, Jamie Hall, Noam Shazeer, Apoorv
  Kulshreshtha, Heng-Tze Cheng, Alicia Jin, Taylor Bos, Leslie Baker, Yu Du,
  et al.
  Lamda: Language models for dialog applications.
  arXiv preprint arXiv:2201.08239, 2022.
- [31]

  Stefan Palan and Christian Schitter.
  Prolific. ac—a subject pool for online experiments.
  Journal of Behavioral and Experimental Finance, 17:22–27,
  2018.
- [32]

  Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, and Denny Zhou.
  Self-consistency improves chain of thought reasoning in language
  models, 2022.
- [33]

  Bernease Herman.
  The promise and peril of human evaluation for model interpretability.
  arXiv preprint arXiv:1711.07414, 2017.
- [34]

  Alon Jacovi and Yoav Goldberg.
  Towards faithfully interpretable nlp systems: How should we define
  and evaluate faithfulness?
  ACL 2020, 2020.
- [35]

  Leo Gao, Stella Biderman, Sid Black, Laurence Golding, Travis Hoppe, Charles
  Foster, Jason Phang, Horace He, Anish Thite, Noa Nabeshima, et al.
  The pile: An 800gb dataset of diverse text for language modeling.
  arXiv preprint arXiv:2101.00027, 2020.
- [36]

  Diederik P Kingma and Jimmy Ba.
  Adam: A method for stochastic optimization.
  arXiv preprint arXiv:1412.6980, 2014.

## 附录

## 附录 A CommonsenseQA 错误模式

在我们的实验中，我们遇到了多种有趣的常识推理失败案例。注意，所有最终答案都是正确的——但我们对其得出答案所用的推理存有异议。

### A.1 问题蕴含答案

一类关键的失败案例是形如「答案必须是某种具有<问题性质>的东西。<答案>具有<问题性质>。因此，正确答案是<答案>。」的回答。在这些案例中，模型未能解释它选择的答案为何满足问题性质。

```
Q: What might someone get from learning about science?
Answer Choices:
(a) headache
(b) see things differently
(c) increased knowledge
(d) accidents
(e) appreciation of nature
A: The answer must be something that someone would get from learning about
science. Learning about science would increase knowledge. Therefore, the
answer is increased knowledge (c).
```

这些推理依据虽然或许对模型有用，在我们读来却晦涩且缺乏解释力。

### A.2 循环论证（丐题）

一个相关但更强的前述失败案例版本虽不那么常见，却尤其缺乏洞见。有时模型会在其问题的表述中暗含它所选择的答案。

```
Q: The christian rock band was on a large stage, the singer's foot got caught
on a wire and he had a small what?
Answer Choices:
(a) commit sin
(b) fail
(c) disobey
(d) stumble
(e) boo boo
A: The answer must be something that would cause the singer to stumble. The
singer's foot got caught on a wire, so he would stumble. Therefore, the
answer is stumble (d).
```

### A.3 留给读者的练习

一种罕见的失败案例是模型认为没有必要论证其答案。例如：

```
Q: Other than school or from text where can one gain knowledge?
Answer Choices:
(a) book
(b) class
(c) thinking
(d) head
(e) meeting
A: The answer must be a place where someone can gain knowledge other than
school or from text. The answer is meeting (e).
```

### A.4 世界状态断言

有时，模型会假设它了解某个被用作变量的主体或人物。这引出有些滑稽的推理示例。部分原因在于，人们通常期望好的推理依据会利用对更一般对象类的理解，并诉诸这些一般类与特定实例之间的关系。例如，「人通常会因高处而感到兴奋」这一论证通常比「James 会因高处而感到兴奋」更有说服力。

```
Q: A person's hand hurts after hitting the bottle. What might happen to
the bottle?
Answer Choices:
(a) alcoholism
(b) breaking
(c) fly
(d) nausea
(e) ticket
A: The answer must be something that happens to the bottle. The bottle is
broken. Therefore, the answer is breaking (b).
```

```
Q: James loved climbing.  What emotion might he feel from heights?
Answer Choices:
(a) exhaustion
(b) exhilaration
(c) falling down
(d) nervousness
(e) vertigo
A: The answer must be a feeling that would cause someone to climb a mountain.
James would feel exhilaration from heights. Therefore, the answer is
exhilaration (b).
```

### A.5 烟雾弹（转移注意力）

一些推理错误对应模型做出了技术上正确、但无助于论证该主张的陈述。

```
Q: A squirrel ran up to it's home, where is the small dog likely to be
barking up?
Answer Choices:
(a) manhattan apartment
(b) wood
(c) neighbor's yard
(d) tree
(e) basket
A: The answer must be a place where a small dog would be likely to be
barking. Squirrels are not small dogs. Therefore, the answer is tree (d).
```

```
Q: John ran very fast, his feet touched the ground in what way?
Answer Choices:
(a) behind
(b) loose
(c) feverishly
(d) slowly
(e) lightly
A: The answer must be a way of running that is different from the way John
ran. Running is a fast, light-footed activity. Therefore, the answer is
lightly (e).
```

### A.6 提示捷径

在训练期间向模型展示一些「提示」示例以防止其随时间丧失合理化能力的实验中，模型似乎领会到最终答案总是对应被提示的答案。这导致了诸如此类的回答

```
Q: Billy bought coffee and waited for his wife to arrive from  France.
Where might he have been?
Answer Choices:
(a) airport
(b) grocery store
(c) internet cafe
(d) supermarket
(e) train station
A: The answer must be a place where Billy could have been waiting for his
wife to arrive from France. The airport is a place where people can wait
for flights. Therefore, the answer is train station (e).
```

## 附录 B 修改后的 CQA 提示

供参考，我们给出基于 Wei et al. (2022) 密切修改的提示。

Q: What do people use to absorb extra ink from a fountain pen?

Answer Choices:

(a) shirt pocket

(b) calligrapher's hand

(c) inkwell

(d) desk drawer

(e) blotter

A: The answer must be used to absorb extra ink. Blotters are designed to absorb liquids. Therefore, the answer is blotter (e).

Q: What home entertainment equipment requires cable?

Answer Choices:

(a) radio shack

(b) substation

(c) television

(d) cabinet

(e) desk

A: The answer must require cable. Cable is used to provide satellite channels to televisions. Therefore, the answer is television (c).

Q: The fox walked from the city into the forest, what was it looking for?

Answer Choices:

(a) pretty flowers

(b) hen house

(c) natural habitat

(d) storybook

(e) dense forest

A: The answer must be a reason for a fox to go into the forest. The forest is a fox's natural habitat. Therefore, the answer is natural habitat (c).

Q: Sammy wanted to go to where the people were. Where might he go?

Answer Choices:

(a) populated areas

(b) race track

(c) desert

(d) apartment

(e) roadblock

A: The answer must be a place with many people. Populated areas, by definition, have a lot of people. Therefore, the answer is populated areas (a).

Q: Where do you put your grapes just before checking out?

Answer Choices:

(a) mouth

(b) grocery cart

(c) super market

(d) fruit basket

(e) fruit market

A: The answer should be the place where grocery items are placed before checking out. Of the above choices, grocery cart makes the most sense for holding grocery items. Therefore, the answer is grocery cart (b).

Q: Google Maps and other highway and street GPS services have replaced what?

Answer Choices:

(a) united states

(b) mexico

(c) countryside

(d) atlas

(e) oceans

A: The answer must be something that used to do what Google Maps and GPS services do, which is give directions. Atlases were also used to give directions. Therefore, the answer is atlas (d).

Q: Before getting a divorce, what did the wife feel who was doing all the work?

Answer Choices:

(a) harder

(b) anguish

(c) bitterness

(d) tears

(e) sadness

A: The answer should be a feeling which would cause someone who was doing all the work to get divorced. If someone feels bitter towards their spouse, they are likely to want a divorce. Therefore, the answer is bitterness (c).

## 附录 C 人工评估的测试提示

我们还随机抽取了 50 道少样本与 STaR 训练模型（不含合理化）都答对的问题，如第 4.4 节所述。以随机顺序呈现时，二十名众包工人更偏好 STaR 生成的回答。我们在此重现这些示例，少样本推理依据在前、STaR 训练的推理依据居次、人工推理殿后，尽管呈现给参与者时这些是打乱顺序的。我们尽可能从 Rajani et al. (2019) 的原始划分推理依据中选取人工回答，发现新划分的推理依据中重复情况要常见得多。例如，解释「Rivers flow trough valleys,」在新划分数据集中逐字出现了 400 多次，「This word was most relevant」出现了 150 多次。Rajani et al. (2019) 的数据集还包含诸如「The only answer that makes sense」或「BOB WILL NOT POKEMON CARDS WERE COMMON AND WORTHLESS BUT WRONG ABOUT THEM SO FEEL REALLY RARE TO DELAY」或答案复述之类的解释。我们在解释末尾附加短语「Therefore, the answer is ANSWERTEXT (ANSWERLETTER)」，其中 ANSWERTEXT 替换为正确答案的文本、ANSWERLETTER 替换为正确答案字母。这样做是为了 1) 降低其中一个回答来自不同来源这一点的明显程度，2) 将差异聚焦于推理依据而非答案格式。

在问题之前、知情同意表之后，我们给出了如下指导语（原文为英文，保留不译）：

Each question will have three explanations for one answer, which is a pre-determined correct ("best") answer.

Please rank the explanations for each question from best to worst (with 1 as the best and 3 as the worst) based on how well they justify the correct answer.

Note there are some typos and grammatical errors in the examples, in the questions, answers, and the explanation. Please treat the answer letter (a / b / c / d / e) at the end of the explanations as the correct answer letter, even if another answer is valid (and perhaps more reasonable), and even if it does not match with the answer text preceding it.

示例经子采样后呈现给众包工人（每组三条例证依次为：少样本 CoT 生成、STaR 生成、人工编写）：

Q: Who is likely yo have a caring heart?

Answer Choices:

(a) person

(b) species

(c) artichoke

(d) all mammals

(e) live animal

A: The answer must be a person. All mammals have a caring heart. Therefore, the answer is person (a).

A: The answer must be someone who is likely to have a caring heart. Humans are the most likely to have a caring heart. Therefore, the answer is person (a).

A: A person is the only human being capable of having a caring heart. Therefore, the answer is person (a).

Q: If a person wanted to become a good writer what should they do in college?

Answer Choices:

(a) word sentence

(b) own animal

(c) read the newspaper

(d) catch cold

(e) study literature

A: The answer must be something that would help a person become a good writer. The answer is study literature (e).

A: The answer must be something that would help a person become a good writer. Literature is a form of study. Therefore, the answer is study literature (e).

A: studying literature will give one skills of writing. Therefore, the answer is study literature (e).

Q: The human always would have fun making up questions for the A.I. overlords, he found the task quite what?

Answer Choices:

(a) do enjoy

(b) eat cake

(c) enjoy living

(d) get laid

(e) enjoyable

A: The answer must be something that the human would enjoy doing. The human enjoys making up questions for the A.I. overlords. Therefore, the answer is enjoyable (e).

A: The answer must be something that the human found enjoyable. The human found the task of making up questions for the A.I. overlords enjoyable. Therefore, the answer is enjoyable (e).

A: Having fun is enjoyable. Therefore, the answer is enjoyable (e).

Q: What happens when I make a pig of myself eating breakfast?

Answer Choices:

(a) full stomach

(b) gain energy

(c) dieting

(d) have energy

(e) feeling satisfied

A: The answer must be a feeling which would cause someone to feel full after eating breakfast. The answer is full stomach (a).

A: The answer must be a feeling which would cause someone to make a pig of themselves eating breakfast. If someone feels full, they are likely to stop eating. Therefore, the answer is full stomach (a).

A: A colloquial phrase for over indulging in food. Therefore, the answer is full stomach (a).

Q: In order to see a story on the big screen what must you do?

Answer Choices:

(a) go to movies

(b) visualize

(c) reading

(d) open book

(e) sketching a picture

A: The answer must be something that you do to see a story on the big screen. Movies are a way to see a story on the big screen. Therefore, the answer is movies (a).

A: The answer must be something that is required to see a story on the big screen. Movies are a form of storytelling. Therefore, the answer is go to movies (a).

A: The big screen is a colloquial term meaning a movie theater. Therefore, the answer is go to movies (a).

Q: What is the opposite of remembering?

Answer Choices:

(a) answering question

(b) stopping to think

(c) knowing

(d) closing eyes

(e) forgetting

A: The answer must be something that is the opposite of remembering. The answer is forgetting (e).

A: The answer must be a feeling which would cause someone to not remember something. If someone forgets something, they are likely to not remember it. Therefore, the answer is forgetting (e).

A: Health complications. Therefore, the answer is forgetting (e).

Q: If you aren't experiencing curiosity and want to ensure viewing enjoyment, what may you watch?

Answer Choices:

(a) examine thing

(b) stare into a mirror

(c) go somewhere

(d) hear news

(e) see favorite show

A: The answer must be something that will make you want to watch. If you are not experiencing curiosity, you may want to watch something that will make you want to watch. Therefore, the answer is watch (e).

A: The answer must be something that will not cause you to want to watch. If you are not experiencing curiosity, you are likely to want to watch something that is entertaining. Therefore, the answer is favorite show (e).

A: see favorite show can you do in front of a tv if you have curiosity about what is being displayed on the tv. Therefore, the answer is favorite show (e).

Q: The carotid is a main artery susceptible to damage where?

Answer Choices:

(a) neck

(b) face

(c) busy city

(d) torso

(e) human body

A: The answer must be a place where the carotid artery is susceptible to damage. The carotid artery is located in the neck. Therefore, the answer is neck (a).

A: The answer must be a place where the carotid is susceptible to damage. The carotid is susceptible to damage in the neck. Therefore, the answer is neck (a).

A: The carotid artery is located in the neck. Therefore, the answer is neck (a).

Q: The king needed to feel safe, where did he go?

Answer Choices:

(a) castle

(b) throne room

(c) deck of cards

(d) fort

(e) court

A: The answer must be a place where the king feels safe. The king's castle is a place where he feels safe. Therefore, the answer is castle (a).

A: The answer must be a place where the king can feel safe. Castles are places where kings feel safe. Therefore, the answer is castle (a).

A: In general, King live in castle. Therefore, the answer is castle (a).

Q: What is the result of instituting civil action?

Answer Choices:

(a) bad feelings

(b) confusion

(c) going to court

(d) hurt feelings

(e) sandwiches

A: The answer must be a result of instituting civil action. The result of instituting civil action is a lawsuit. Therefore, the answer is going to court (c).

A: The answer must be a result of instituting civil action. If someone goes to court, they are likely to feel hurt feelings. Therefore, the answer is going to court (c).

A: Anger and Trial will not institute a court case. Therefore, the answer is going to court (c).Q: The person wanted to fix his car, what did he order?

Answer Choices:

(a) selling things

(b) gas

(c) feel resentful

(d) machine part

(e) cross street

A: The answer must be something that would help the person fix his car. The person would not want to sell things, because he would not want to give up his car. Therefore, the answer is machine part (d).

A: The answer must be something that would be used to fix a car. Machine parts are used to fix cars. Therefore, the answer is machine part (d).

A: A machine part is the only thing listed that would fix the car. Therefore, the answer is machine part (d).

Q: He always traveled up the mountain when winter arrived, he had a passion and desire to do what?

Answer Choices:

(a) play volleyball

(b) play hockey

(c) ski

(d) knit

(e) skate

A: The answer must be something that the person does when winter arrives. The answer is skiing (c).

A: The answer must be something that the person did when winter arrived. The answer is ski (c).

A: Skiing is the only option that is done on a mountain. Therefore, the answer is ski (c).

Q: Bob thought that his Pokemon cards were common and worthless, but he was wrong about them. They were really what?

Answer Choices:

(a) personal

(b) special

(c) shiny

(d) rare

(e) irregular

A: The answer must be something that is not common and worthless. Pokemon cards are not common and worthless. Therefore, the answer is rare (d).

A: The answer must be something that are rare. Pokemon cards are rare. Therefore, the answer is rare (d).

A: BOB WILL NOT POKEMON CARDS WERE COMMON AND WORTHLESS BUT WRONG ABOUT THEM SO FEEL REALLY RARE TO DELAY. Therefore, the answer is rare (d).

Q: If you're lighting a candle to see what are you in?

Answer Choices:

(a) dimly lit room

(b) synagogue

(c) sunlight

(d) birthday cake

(e) bedroom

A: The answer must be a place where you can see what you are in. The answer is a room with dim lighting. Therefore, the answer is dimly lit room (a).

A: The answer must be a place where you can see a candle. Candles are used to see things in the dark. Therefore, the answer is dimly lit room (a).

A: Lighting or illumination is the deliberate use of light to achieve a practical or aesthetic effect. Lighting includes the use of both artificial light sources like lamps ... Therefore, the answer is dimly lit room (a).

Q: The person was thirsty, what should he have done?

Answer Choices:

(a) eat

(b) sunny days

(c) compliments

(d) drink water

(e) all kinds of things

A: The answer must be something that would make the person feel better. If the person is thirsty, he should drink water. Therefore, the answer is drink water (d).

A: The answer must be something that would make someone feel better if they were thirsty. If someone is thirsty, they are likely to want to drink water. Therefore, the answer is drink water (d).

A: The person was thirsty, so drink water. Therefore, the answer is drink water (d).

Q: Where would you find many products for sale?

Answer Choices:

(a) market

(b) cost one dollar

(c) shelf

(d) salon

(e) demonstration

A: The answer must be a place where many products are sold. A market is a place where many products are sold. Therefore, the answer is market (a).

A: The answer must be a place with a lot of products for sale. Markets are the most common place to buy products. Therefore, the answer is market (a).

A: The only place products are for sale are in markets and stores. Therefore, the answer is market (a).

Q: If man and mammoth wanted to meet, they would probably have to do it during when?

Answer Choices:

(a) a baby shower

(b) ancient history

(c) storybook

(d) stone age

(e) forest

A: The answer must be a time when man and mammoth would meet. Stone age is the time when man and mammoth lived. Therefore, the answer is stone age (d).

A: The answer must be a time when man and mammoth would be able to meet. The stone age was a time when man and mammoth would be able to meet. Therefore, the answer is stone age (d).

A: During the stone age is the only time mammoths lived. Therefore, the answer is stone age (d).

Q: They prided themselves on being a wealth of knowledge, and that's why many chose to attend their what?

Answer Choices:

(a) book store

(b) university

(c) meeting

(d) class

(e) encyclopedia

A: The answer must be a place where people go to learn about things. The answer is university (b).

A: The answer must be a place where people go to learn about things. Universities are places where people go to learn about things. Therefore, the answer is university (b).

A: because in the university you get more knowledge. Therefore, the answer is university (b).

Q: what happens when visiting museum that have narrow halls?

Answer Choices:

(a) sore feet

(b) amazement

(c) retrospection

(d) boredom

(e) crowding

A: The answer must be something that happens when visiting a museum that has narrow halls. Crowding is a common problem in museums. Therefore, the answer is crowding (e).

A: The answer must be something that would cause someone to have sore feet if they are walking in narrow halls. If someone feels cramped, they are likely to want to go somewhere else. Therefore, the answer is crowding (e).

A: museum is one of the crowdest place. Therefore, the answer is crowding (e).

Q: On their hike they brought a filtering straw, they were worried about germs in the what?

Answer Choices:

(a) make sick

(b) doctor

(c) water

(d) stream

(e) mouth

A: The answer must be something that can filter out germs. Filtering straws are used to filter out germs. Therefore, the answer is filtering straw (c).

A: The answer must be something that would cause someone to bring a filtering straw on a hike. Filtering straws are used to filter water. Therefore, the answer is water (c).

A: straw it something used to drink water. Therefore, the answer is water (c).

Q: If I am not good at playing poker, I will begin what if I play?

Answer Choices:

(a) discord

(b) social event

(c) losing money

(d) competition

(e) heightened awareness

A: The answer must be something that will happen if you are not good at playing poker. If you are not good at playing poker, you will begin to lose money. Therefore, the answer is losing money (c).

A: The answer must be something that will help you if you are not good at playing poker. If you are losing money, you are likely to want to stop playing. Therefore, the answer is losing money (c).

A: Poker is a game in which people lose their money. Therefore, the answer is losing money (c).

Q: People are meeting people, what is the likely physical gesture?

Answer Choices:

(a) introducing yourself

(b) smiling

(c) shake hands

(d) share a hug

(e) talking

A: The answer must be a physical gesture that is used to greet someone. The answer is handshake (c).

A: The answer must be a gesture used to meet people. If someone wants to meet people, they are likely to want to shake hands. Therefore, the answer is shaking hands (c).

A: A handshake is a globally widespread. Therefore, the answer is shaking hands (c).

Q: What do dogs get that make them itch?

Answer Choices:

(a) bones

(b) fleas

(c) bad breath

(d) wagging tails

(e) four legs

A: The answer must be something that makes dogs itch. Dogs get fleas, which make them itch. Therefore, the answer is fleas (b).

A: The answer must be something that dogs get that make them itch. Fleas are a common cause of dog itch. Therefore, the answer is fleas (b).

A: fleas makes you itch. Therefore, the answer is fleas (b).

Q: What is ignorance often equated with?

Answer Choices:

(a) bliss

(b) hostility

(c) peace

(d) accidents

(e) find truth

A: The answer must be something that is often equated with ignorance. Bliss is often equated with ignorance. Therefore, the answer is bliss (a).

A: The answer must be a feeling which would cause someone to be ignorant. If someone feels bliss, they are likely to be ignorant. Therefore, the answer is bliss (a).

A: bliss comes from ignorance. Therefore, the answer is bliss (a).

Q: The two teams were competing all the time, what likely developed between them?

Answer Choices:

(a) accomplishment

(b) enemies

(c) rivalry

(d) friendship

(e) bad blood

A: The answer must be something that developed between the two teams. The teams were competing all the time. Therefore, the answer is rivalry (c).

A: The answer must be a feeling which would cause two teams to compete all the time. Rivalry is a common feeling which would cause two teams to compete all the time. Therefore, the answer is rivalry (c).

A: likely developed between them of rivalry. Therefore, the answer is rivalry (c).

Q: James doesn't want a relationship. He thinks that loving another will only create what?

Answer Choices:

(a) satisfaction

(b) jealousy

(c) happiness

(d) wonderful

(e) quiet

A: The answer must be something that would make James feel bad about not having a relationship. If someone feels jealous, they are likely to want a relationship. Therefore, the answer is jealousy (b).

A: The answer must be a feeling which would cause someone who doesn't want a relationship to not want one. If someone feels jealous of another, they are likely to not want a relationship. Therefore, the answer is jealousy (b).

A: Jealousy is a negative emotion. Therefore, the answer is jealousy (b).

Q: The had a reputation for celebrating in a debaucherous manner, what often happened as a result?

Answer Choices:

(a) drunkenness

(b) enjoyment

(c) have fun

(d) hang over

(e) fighting

A: The answer must be a result of a celebration. The answer is drunkenness (a).

A: The answer must be something that would cause someone to have a reputation for celebrating in a debaucherous manner. Alcohol is a depressant. Therefore, the answer is drunkenness (a).

A: it is normal not a good idea to get drunk. Therefore, the answer is drunkenness (a).

Q: The paper towels are usually in plain sight in the kitchen, where did the dad go next to find them?

Answer Choices:

(a) pantry

(b) cabinet

(c) grocery store

(d) waste bin

(e) market

A: The answer must be a place where the dad would go to find the paper towels. The pantry is a place where food is stored. Therefore, the answer is pantry (a).

A: The answer must be a place where paper towels are stored. Pantries are the most likely place to store paper towels. Therefore, the answer is pantry (a).

A: The pantry is in the kitchen and stores things. Therefore, the answer is pantry (a).

Q: My house is very dry, with little water in the air. What tool should I use to fix this?

Answer Choices:

(a) humidifier

(b) surface of earth

(c) skating rink

(d) ice cube

(e) burn it to the ground

A: The answer must be a tool that will make the air in your house moist. A humidifier is a tool that will make the air in your house moist. Therefore, the answer is humidifier (a).

A: The answer must be something that would make the air in my house more humid. A humidifier is used to make the air in a room more humid. Therefore, the answer is humidifier (a).

A: This word was most relevant. Therefore, the answer is humidifier (a).

Q: A motorcycle is quicker because it isn't as what as a car?

Answer Choices:

(a) heavy

(b) shiny

(c) red

(d) obesity

(e) expensive

A: The answer must be something that is not as heavy as a car. A motorcycle is lighter than a car. Therefore, the answer is not heavy (a).

A: The answer must be something that is not as quick as a motorcycle. Motorcycles are not as heavy as cars. Therefore, the answer is heavy (a).

A: Because it is much smaller. Therefore, the answer is heavy (a).

Q: The baseball team was playing ball. It was time for the pitcher to act. How did the pitcher get the ball to the batter?

Answer Choices:

(a) lose

(b) injury

(c) competition

(d) throwing

(e) rolled

A: The answer must be a way to get the ball to the batter. The pitcher is the one who throws the ball. Therefore, the answer is throwing (d).

A: The answer must be a way for the pitcher to get the ball to the batter. The pitcher is the person who is responsible for getting the ball to the batter. Therefore, the answer is throwing (d).

A: The pitcher threw the ball to the batter so that he could hit it. Therefore, the answer is throwing (d).

Q: In what sort of container should you keep your ficus?

Answer Choices:

(a) refigerator

(b) screened porch

(c) clay pot

(d) shady places

(e) arboretum

A: The answer must be a container that keeps the ficus in a shady place. Clay pots are used to keep plants in shady places. Therefore, the answer is clay pot (c).

A: The answer must be a container in which ficus can be kept. Ficus are tropical plants. Therefore, the answer is clay pot (c).

A: Clay pot is the only type of container listed. Therefore, the answer is clay pot (c).

Q: James was cooking s stew in his apartment kitchen. Where might he look for a potato.

Answer Choices:

(a) restaurants

(b) casserole

(c) root cellar

(d) pockets

(e) pantry

A: The answer must be a place where potatoes are stored. The answer is pantry (e).

A: The answer must be a place where potatoes are stored. Pantries are the most likely place to store potatoes. Therefore, the answer is pantry (e).

A: apartments do not often have root cellars, and are not restaurants. a pantry is closest to James inside his apartment. Therefore, the answer is pantry (e).

Q: If ships are in a storm and the sun comes out, what has happened?

Answer Choices:

(a) sinks

(b) cross river

(c) collide

(d) bottom out

(e) carry people

A: The answer must be a thing that happens when ships are in a storm and the sun comes out. Ships are in a storm when they are in the middle of the ocean. Therefore, the answer is bottom out (d).

A: The answer must be something that happens when the sun comes out. The sun is a source of energy. Therefore, the answer is bottom out (d).

A: the sun comes out so its not a storm any more. Therefore, the answer is bottom out (d).

Q: Where do all marmot live before they are captured?

Answer Choices:

(a) switzerland

(b) spain

(c) vancouver island

(d) wilderness

(e) australia

A: The answer must be a place where marmots live. Marmots live in the wilderness. Therefore, the answer is wilderness (d).

A: The answer must be a place where marmots are found. The wilderness is the most likely place to find marmots. Therefore, the answer is wilderness (d).

A: Marmots don't live in Australia or Switzerland. Therefore, the answer is wilderness (d).

Q: Where does one wait on a bench for something on tracks?

Answer Choices:

(a) train station

(b) state park

(c) crosswalk

(d) bus stop

(e) bus depot

A: The answer must be a place where one waits for a train, bus, or other vehicle. The answer is train station (a).

A: The answer must be a place where one can wait for a train. Train stations are places where trains stop. Therefore, the answer is train station (a).

A: Only trains are on tracks. Therefore, the answer is train station (a).

Q: What can planning vacation lead to between a couple when they disagree?

Answer Choices:

(a) relaxation

(b) enjoying

(c) arguments

(d) going abroad

(e) spending money

A: The answer must be something that can happen when a couple disagrees. Arguments are a common result of disagreements. Therefore, the answer is arguments (c).

A: The answer must be a result of planning vacation. Arguments are a common result of planning vacation. Therefore, the answer is arguments (c).

A: Arguments are the direct result of disagreements. Therefore, the answer is arguments (c).

Q: A sloth climbs slow, but it can eventually reach all the way up where?

Answer Choices:

(a) forest canopy

(b) universe

(c) tropical rainforest

(d) large trees

(e) nature preserve

A: The answer must be a place where a sloth can climb. The forest canopy is the highest point in the forest. Therefore, the answer is forest canopy (a).

A: The answer must be a place where a sloth can climb. The canopy of a forest is the highest point in a forest. Therefore, the answer is canopy of a forest (a).

A: The sloth is a mammal that lives in the trees of South America. They have a slow and peculiar way of moving about. In fact, they are the slowest land mammals and travel very sluggishly on the ground (0.025 m/s-0.050 m/s). Therefore, the answer is canopy of a forest (a).

Q: Where in America is known for theaters?

Answer Choices:

(a) new york city

(b) shopping mall

(c) downtown area

(d) skating rink

(e) military base

A: The answer must be a place where people go to see movies. Theaters are places where people go to see movies. Therefore, the answer is theater (a).

A: The answer must be a place with a lot of theaters. New York City is known for its many theaters. Therefore, the answer is New York City (a).

A: New York City is the main region in US known for theaters. Therefore, the answer is New York City (a).

Q: What does hearing someone play violin beautifully make you?

Answer Choices:

(a) buy earplugs

(b) inspiring

(c) guitar

(d) make music

(e) like music

A: The answer must be something that makes you feel inspired. Hearing someone play violin beautifully makes you feel inspired. Therefore, the answer is inspiring (b).

A: The answer must be a feeling which would cause someone to want to hear someone play violin beautifully. Music is a form of art. Therefore, the answer is inspiring (b).

A: Hearing someone play a violin beautifully makes me inspired. Therefore, the answer is inspiring (b).

Q: What emotion does committing murder induce?

Answer Choices:

(a) fear

(b) go to jail

(c) problems

(d) cruel

(e) dead

A: The answer must be a feeling that would cause someone to commit murder. Murder is a crime. Therefore, the answer is fear (a).

A: The answer must be a feeling which would cause someone to commit murder. If someone feels fear, they are likely to want to avoid committing murder. Therefore, the answer is fear (a).

A: The only feeling. Therefore, the answer is fear (a).

Q: Sitting to close while watching TV can cause what sort of pain?

Answer Choices:

(a) brain problems

(b) laziness

(c) get fat

(d) headache

(e) laughter

A: The answer must be a pain that comes from sitting too close to the TV. Sitting too close to the TV can cause headaches. Therefore, the answer is headache (d).

A: The answer must be a type of pain which can occur if you are sitting too close to the TV. Headaches are a common side effect of sitting too close to the TV. Therefore, the answer is headache (d).

A: the process of aging in humans. Therefore, the answer is headache (d).

Q: What might people do to protect their legs from getting dirty on the farm?

Answer Choices:

(a) wear jeans

(b) milk cow

(c) believe in god

(d) avoid mud

(e) plant flowers

A: The answer must be something that people do to protect their legs from getting dirty. Of the above choices, wearing jeans is the most logical. Therefore, the answer is jeans (a).

A: The answer must be something that would protect legs from getting dirty on the farm. Jeans are used to protect legs from getting dirty. Therefore, the answer is wear jeans (a).

A: Jeans cover over legs. Therefore, the answer is wear jeans (a).

Q: What types of stoves are there?

Answer Choices:

(a) these twos are irrelevent to the questions

(b) warm pot of beans

(c) brown meat

(d) warm room

(e) gas or electric

A: The answer must be a type of stove. The stove is used to heat food. Therefore, the answer is gas or electric (e).

A: The answer must be a type of stove. Stoves are used to warm rooms. Therefore, the answer is electric (e).

A: stoves are gas or electric. Therefore, the answer is gas or electric (e).

Q: In what geological feature will you find fungus growing?

Answer Choices:

(a) shower stall

(b) toenails

(c) basement

(d) forrest

(e) cave

A: The answer must be a place where fungus grows. The answer is cave (e).

A: The answer must be a place where fungus grows. Fungus grows in caves. Therefore, the answer is cave (e).

A: Rivers flow trough valleys. Therefore, the answer is cave (e).

Q: What is our sun considered to be the center of?

Answer Choices:

(a) universe

(b) solar system

(c) outer space

(d) star

(e) beans

A: The answer must be something that is considered to be the center of the universe. The sun is the center of the solar system. Therefore, the answer is solar system (b).

A: The answer must be a place where the sun is the center of. The sun is the center of the solar system. Therefore, the answer is solar system (b).

A: It is the best option because it is the closest. Therefore, the answer is solar system (b).

Q: What are people in a library likely doing?

Answer Choices:

(a) talk to each other

(b) board ships

(c) study books

(d) suffer hunger

(e) playing games

A: The answer must be something that people in a library are likely to be doing. People in a library are likely to be studying books. Therefore, the answer is study books (c).

A: The answer must be something that is likely to happen in a library. Libraries are places where people study books. Therefore, the answer is studying books (c).

A: Books shelved as study-skills: How to Become a Straight-A Student by Cal Newport, The Study Skills Handbook by Stella Cottrell, Make It Stick: The Scienc... Therefore, the answer is study books (c).

Q: A shark isn't something you have to worry about at the lake in the woods, but there are plenty of dangers in the what?

Answer Choices:

(a) great oceans

(b) great outdoors

(c) tropical waters

(d) pacific ocean

(e) gulf of mexico

A: The answer must be something that is dangerous in the great outdoors. The great outdoors is a place where there are many dangers. Therefore, the answer is great outdoors (b).

A: The answer must be a place where sharks are a danger. Lakes in the woods are not a place where sharks are a danger. Therefore, the answer is great outdoors (b).

A: The great outdoors is the only choice where you would find a lake in the woods. Therefore, the answer is great outdoors (b).

Q: You can share files with someone if you have a connection to a what?

Answer Choices:

(a) freeway

(b) radio

(c) wires

(d) computer network

(e) electrical circuit

A: The answer must be a way to share files. The answer is computer network (d).

A: The answer must be a connection which allows you to share files. A computer network is a collection of computers which are connected to each other. Therefore, the answer is computer network (d).

A: Files can be transmitted over a computer network, and not a freeway. "wires" doesnt make any sense. Therefore, the answer is computer network (d).

Q: What can an injury happen to?

Answer Choices:

(a) emergency room

(b) doctor's office

(c) living thing

(d) bones

(e) accident

A: The answer must be something that can happen to a living thing. The answer is living thing (c).

A: The answer must be something that can happen to a living thing. If someone is injured, they are likely to want to go to the emergency room. Therefore, the answer is living thing (c).

A: Living things feel pain, and therefore can be injured. Therefore, the answer is living thing (c).

## 附录 D CQA 上的合理化示例

我们给出一组随机采样的、模型在微调之前就能产生的合理化结果。我们观察到，有时模型会构造大致形如「答案必须具有一组性质。正确答案具有这些性质。因此，答案是正确答案。」的论证。这种论证结构相当标准，但鉴于模型原本答错了这些问题，它更像模板匹配而非推理。在直接作答之前先用更简单的方式改述问题的技巧也往往有效。总体而言，预训练模型合理化生成的推理依据与预训练模型推理依据生成的质量相近。我们在这里引用预训练模型而非 STaR 训练后的模型，因为最后一轮迭代的推理依据正是模型难以从中学习的那些——也就是说，如果那些推理依据足够好，我们本可预期模型已经把它们吸收进其推理依据生成中。

Q: Why do I eat just enough when eating breakfast?

Answer Choices:

(a) gas

(b) full stomach

(c) feeling satisfied (CORRECT)

(d) have energy

(e) bloated

A: The answer must be a reason for eating just enough when eating breakfast. Eating just enough is a way to feel satisfied. Therefore, the answer is feeling satisfied (c).

Q: How is a dog likely to communicate with another dog?

Answer Choices:

(a) reproduce

(b) bark (CORRECT)

(c) do many things

(d) clone

(e) jump up

A: The answer must be a way for a dog to communicate with another dog. Dogs bark to communicate with each other. Therefore, the answer is bark (b).

Q: If a person is trying to weasel out of punishment for a crime, where are they likely to be?

Answer Choices:

(a) court room (CORRECT)

(b) cherry tree

(c) chicken coop

(d) natural history museum

(e) jail

A: The answer must be a place where a person would be trying to get out of punishment for a crime. The answer is court room (a).

Q: What would easily hide a snake?

Answer Choices:

(a) living room of a house

(b) kew gardens

(c) terrarium

(d) thick forest (CORRECT)

(e) tropical forest

A: The answer must be something that would hide a snake. The answer is thick forest (d).

Q: The person didn't like the varying size of the cake slices handed out, she demand more what?

Answer Choices:

(a) fairness (CORRECT)

(b) candies

(c) compliments

(d) well fed

(e) arguements

A: The answer must be a reason for the person to demand more cake. The person is not happy with the size of the cake slices. Therefore, the answer is fairness (a).

Q: In America, the courthouse of any given town has a likely location, where is it?

Answer Choices:

(a) electrical circuit

(b) getting married

(c) capital city

(d) center of town (CORRECT)

(e) michigan

A: The answer must be a location where a courthouse is located. The capital city is the location of the capital of a state. Therefore, the answer is center of town (d).

Q: Where might I find a bowl nestled among other bowls in the kitchen?

Answer Choices:

(a) refrigerator

(b) kitchen top

(c) cupboard (CORRECT)

(d) dishwasher

(e) apartment

A: The answer must be a place where a bowl is found. The kitchen is a place where bowls are found. Therefore, the answer is cupboard (c).

Q: Which state has blue ridge mountains that are called Blue Mountain?

Answer Choices:

(a) appalachians

(b) virginia

(c) pennsylvania (CORRECT)

(d) north carolina

(e) montana

A: The answer must be a state with mountains. The answer is Pennsylvania (c).

Q: Where could you find many radio studio?

Answer Choices:

(a) radio station

(b) country

(c) clear area

(d) office building

(e) large city (CORRECT)

A: The answer must be a place where many radio studios are located. Radio studios are used to broadcast radio programs. Therefore, the answer is large city (e).

Q: Where would someone bring you a cup?

Answer Choices:

(a) apartment

(b) closet

(c) restaurant (CORRECT)

(d) table

(e) party

A: The answer must be a place where someone would bring you a cup. A restaurant is a place where people bring cups. Therefore, the answer is restaurant (c).

## 附录 E 不含合理化的 STaR（推理依据生成自举）

为方便起见，我们在此单独给出推理依据生成自举算法。不过它只是算法 1 去掉蓝色部分后的形式。

算法 2　推理依据生成自举（不含合理化的 STaR）

输入 $M$：一个预训练 LLM；数据集 $\mathcal{D}=\{(x_{i},y_{i})\}_{i=1}^{D}$（含少样本提示）

1: $M_{0}\leftarrow M$  # 复制原始模型
2: for $n$ in $1...N$ do  # 外循环
3: 　　$(\hat{r}_{i},\hat{y}_{i})\leftarrow M_{n-1}(x_{i})\quad\forall i\in[1,D]$  # 执行推理依据生成
4: 　　$\mathcal{D}_{n}\leftarrow\{(x_{i},\hat{r}_{i},y_{i})\mid i\in[1,D]\land\hat{y}_{i}=y_{i}\}$  # 用标准答案过滤推理依据
5: 　　$M_{n}\leftarrow\text{train}(M,\mathcal{D}_{n})$  # 在正确解上微调原始模型——内循环
6: end for

## 附录 F 案例研究

```
Q: John wants to eat at an Indian
restaurant in on top of the space
needle, where would he have to go?
Answer Choices:
(a) reservation (b) curry
(c) britsh town (d) seattle
(e) large city
A: The answer must be a place with
a space needle. The space needle is
a landmark in Seattle. Therefore,
the answer is Seattle (d).

Q: I put a towel in a cardboard box for
the kitten, I wanted it to have what?
Answer Choices:
(a) farmhouse (b) zoos (c) cold place
(d) floor (e) warm place
A: The answer must be a place where the
kitten would be comfortable. The kitten
would be comfortable in a warm place.
Therefore, the answer is warm place (e).

Q: Needlepoint requires many
accessories, what holds the work taut?
Answer Choices:
(a) sewing (b) collection of folk art
(c) livingroom (d) frame (e) bathroom
A: The answer must be something that
holds the work taut. The work is taut
because it is held in place. Therefore,
the answer is frame (d).
```

（a）模型能够解出其先前答错的问题的案例。

Q: They prided themselves on being awealth of knowledge, and that's why manychose to attend their what?Answer Choices:(a) book store (b) university (c) meeting(d) class (e) encyclopediaA: The answer must be a place where peoplego to learn about things. The answer isuniversity (b).A: The answer must be a place where peoplego to learn about things. Universities areplaces where people go to learn aboutthings. Therefore, the answer isuniversity (b).Q: You want a real estate agent that isstraight forward with you, the lastthing you want is for them to what ahouse's quality?Answer Choices:(a) cover up (b) offer price(c) misrepresent (d) lie (e) falsifyA: The answer must be a way to determinethe quality of a house. The answer ismisrepresent (c).A: The answer must be something thatwould be a bad thing for the real estateagent to do. The real estate agent wouldbe misrepresenting the house's qualityif they were to lie about it. Therefore,the answer is misrepresent (c).

（b）模型本来就能用少样本推理回答、但经过更多迭代后回答得更好的问题。

图 7：STaR 的案例研究。我们突出展示一些模型最初无法解出的问题，以及起初正确但随后改进的推理依据。我们注意到，对于 CQA，任务在于选出「最佳」答案，其中多个答案可能技术上均正确。

## 附录 G 偏差与忠实性

需要注意的是，STaR 的设计是为了放大在给定数据集上导向正确解的推理。这对于 CommonsenseQA 这样的数据集意味着：如果偏差对解该数据集是「有用的」，它们就会被放大。合理化使这一点更糟，因为模型原本可能不会自然得出的带偏回答，在某种意义上被从模型中拉了出来。数据集中的偏差与模型学到的既有偏差之间的确切相互作用尚不清楚，这是一般而言所有大语言模型（尤其是 STaR 训练模型）在真实世界部署前需要考虑的问题。

不过我们在这方面发现了一些令人鼓舞的初步结果：对于性别无关的问题，模型似乎会在解释中忽略性别。例如：「Q: Where is a good place for a woman to store her sunglasses? → A: The answer must be a place where sunglasses are stored. Sunglasses are stored in purses. Therefore, the answer is purse (e).」或「Q: The only baggage the woman checked was a drawstring bag, where was she heading with it? → A: The answer must be a place where a drawstring bag is checked. The answer is airport (e).」我们认为这个问题值得一项全面得多的研究。

追求可解释或为推理提供解释的模型面临的一个重要挑战是忠实性（faithfulness）。虽然我们的重点不在 STaR 可能带来的可解释性收益，但评估解释与推理依据存在一个根本挑战：即忠实性（Herman, 2017；Jacovi & Goldberg, 2020）。Jacovi & Goldberg (2020) 将忠实的解释描述为「准确[反映]模型预测背后的推理过程」的解释。虽然 STaR 鼓励在推理依据中使用能将模型导向正确答案的推理，但很难（如果不是不可能）确保推理依据反映了模型的内部处理。例如，很容易想象模型隐式地立即选定某个特定答案，然后生成一个论证该选定答案的推理依据。这将允许模型以有偏的方式选择答案，同时生成无偏的推理依据。

我们的模型胜过了微调后直接预测答案的模型，这一事实以及 Wei et al. (2022) 等论文的消融研究都清楚地表明，在给出答案之前生成推理依据，能非平凡地提升模型答案质量。然而，评估任何特定答案的推理依据的忠实程度是困难的。不过我们注意到，这些问题并非 STaR 独有，而是理解大语言模型（尤其是大语言模型生成的推理依据）之困难的通病。

## 附录 H 超参数

GPT-J 是一个 28 层的 decoder-only Transformer，嵌入大小为 1024，16 个维度为 256 的注意力头，FFN 隐藏层大小为 16384。它在 Pile（Gao et al., 2020）上预训练，词表大小为 50.4K。

一般而言，除非另有说明，我们使用 8 个序列的批次大小，每个序列长度 1024。我们还使用打包（packing），即把较短的示例打包成更长的序列（最长 1024）以提高 TPU 利用率。我们不使用权重衰减，并在单个 TPU-v3 节点上训练与采样。我们使用 Adam 优化器（Kingma & Ba, 2014）在 $10^{-7}$ 到 $10^{-4}$ 的学习率范围内进行了超参数搜索。我们发现 $10^{-6}$ 始终是表现最好的学习率。

## 附录 I GSM8K 少样本提示

我们给出以下 GSM8K 的少样本提示，基于 Cobbe et al. (2021) 中的示例（原文为英文，保留不译）。

Q: Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?

A: Natalia sold 48/2 = <<48/2=24>>24 clips in May.

Natalia sold 48+24 = <<48+24=72>>72 clips altogether in April and May.

#### 72

Q: Betty is saving money for a new wallet which costs $100. Betty has only half of the money she needs. Her parents decided to give her $15 for that purpose, and her grandparents twice as much as her parents. How much more money does Betty need to buy the wallet?

A: In the beginning, Betty has only 100 / 2 = $<<100/2=50>>50.

Betty's grandparents gave her 15 * 2 = $<<15*2=30>>30.

This means, Betty needs 100 - 50 - 30 - 15 = $<<100-50-30-15=5>>5 more.

#### 5

Q: Julie is reading a 120-page book. Yesterday, she was able to read 12 pages and today, she read twice as many pages as yesterday. If she wants to read half of the remaining pages tomorrow, how many pages should she read?

A: Maila read 12 x 2 = <<12*2=24>>24 pages today.

So she was able to read a total of 12 + 24 = <<12+24=36>>36 pages since yesterday.

There are 120 - 36 = <<120-36=84>>84 pages left to be read.

Since she wants to read half of the remaining pages tomorrow, then she should read 84/2 = <<84/2=42>>42 pages.

#### 42

Q: Mark has a garden with flowers. He planted plants of three different colors in it. Ten of them are yellow, and there are 80% more of those in purple. There are only 25% as many green flowers as there are yellow and purple flowers. How many flowers does Mark have in his garden?

A: There are 80/100 * 10 = <<80/100*10=8>>8 more purple flowers than yellow flowers.

So in Mark's garden, there are 10 + 8 = <<10+8=18>>18 purple flowers.

Purple and yellow flowers sum up to 10 + 18 = <<10+18=28>>28 flowers.

That means in Mark's garden there are 25/100 * 28 = <<25/100*28=7>>7 green flowers.

So in total Mark has 28 + 7 = <<28+7=35>>35 plants in his garden.

#### 35

Q: Alexis is applying for a new job and bought a new set of business clothes to wear to the interview. She went to a department store with a budget of $200 and spent $30 on a button-up shirt, $46 on suit pants, $38 on a suit coat, $11 on socks, and $18 on a belt. She also purchased a pair of shoes, but lost the receipt for them. She has $16 left from her budget. How much did Alexis pay for the shoes?

A: Let S be the amount Alexis paid for the shoes.

She spent S + 30 + 46 + 38 + 11 + 18 = S + <<+30+46+38+11+18=143>>143.

She used all but $16 of her budget, so S + 143 = 200 - 16 = 184.

Thus, Alexis paid S = 184 - 143 = $<<184-143=41>>41 for the shoes.

#### 41

Q: Tina makes $18.00 an hour.  If she works more than 8 hours per shift, she is eligible for overtime, which is paid by your hourly wage + 1/2 your hourly wage.  If she works 10 hours every day for 5 days, how much money does she make?

A: She works 8 hours a day for $18 per hour so she makes 8*18 = $<<8*18=144.00>>144.00 per 8-hour shift

She works 10 hours a day and anything over 8 hours is eligible for overtime, so she gets 10-8 = <<10-8=2>>2 hours of overtime

Overtime is calculated as time and a half so and she makes $18/hour so her overtime pay is 18*.5 = $<<18*.5=9.00>>9.00

Her overtime pay is 18+9 = $<<18+9=27.00>>27.00

Her base pay is $144.00 per 8-hour shift and she works 5 days and makes 5 * $144 = $<<144*5=720.00>>720.00

Her overtime pay is $27.00 per hour and she works 2 hours of overtime per day and makes 27*2 = $<<27*2=54.00>>54.00 in overtime pay

2 hours of overtime pay for 5 days means she makes 54*5 = $270.00

In 5 days her base pay is $720.00 and she makes $270.00 in overtime pay so she makes $720 + $270 = $<<720+270=990.00>>990.00

#### 990

## 附录 J STaR 的 GSM8K 解

我们观察到 STaR 训练模型给出的 GSM8K 解的一些有趣模式。通常，当解所用的计算步数远少于标准答案时，它对应于模型尽管推理有误却碰巧答对的情形。不过在有些情况下，模型会给出比标准答案更简单的解。图 8 给出了一个示例。

图 8：训练集中一个 STaR 推导出比标准答案显著更简单的解的示例问题。

