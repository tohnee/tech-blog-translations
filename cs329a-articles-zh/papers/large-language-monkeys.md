---
title: "大语言模型猴子：用重复采样扩展推理计算"
title_en: "Large Language Monkeys: Scaling Inference Compute with Repeated Sampling"
arxiv: 2407.21787
source: https://arxiv.org/abs/2407.21787
crawled: 2026-09-23
translated: 2026-09-23
---

# 大语言模型猴子：用重复采样扩展推理计算

> 原文：[Large Language Monkeys: Scaling Inference Compute with Repeated Sampling](https://arxiv.org/abs/2407.21787) · Stanford CS329A 指定阅读

Bradley Brown∗、Jordan Juravsky∗、Ryan Ehrlich∗、Ronald Clark、Quoc V. Le、Christopher Ré、Azalia Mirhoseini

注：标题灵感来自「无限猴子定理」<https://en.m.wikipedia.org/wiki/Infinite_monkey_theorem>。∗ 表示同等贡献（Bradley Brown 的工作在其于斯坦福任访问研究员期间完成）。
所属机构：斯坦福大学计算机科学系；牛津大学；Google DeepMind
代码：<https://github.com/ScalingIntelligence/large_language_monkeys>；数据：<https://huggingface.co/datasets/ScalingIntelligence/monkey_business>。

###### 摘要

扩展用于训练语言模型的计算量已显著提升了它们的能力。然而在推理阶段，我们往往把模型限制为对每个问题只做一次尝试。在本工作中，我们将推理计算作为另一条扩展轴加以探索，所用的是从模型中重复采样候选解这一简单技术。在多个任务和多个模型上，我们观察到覆盖率（coverage，即任意一个生成样本所能求解的问题比例）随样本数量在四个数量级上同步扩展。有趣的是，覆盖率与样本数量之间的关系常常接近对数线性，并且可以用一个指数化幂律（exponentiated power law）来建模，这暗示了推理时缩放定律的存在。在代码与形式化证明这类答案可以被自动验证的领域，覆盖率的提升会直接转化为性能的改进。当我们把重复采样应用于 SWE-bench Lite 时，DeepSeek-Coder-V2-Instruct 解决 issue 的比例从单样本的 15.9% 提升到 250 个样本的 56%，超过了 43% 的单样本最优（SOTA）水平。在没有自动验证器的领域，我们发现从样本集合中挑选答案的常用方法（多数投票与奖励模型）在数百个样本之后便进入平台期，无法随样本预算充分扩展。

## 1 引言

大型语言模型（LLM）求解代码、数学及其他推理任务的能力在过去几年里显著提升（Radford et al., 2019；Brown et al., 2020b；OpenAI, 2024；Anthropic, 2024）。通过更大的模型、更长的预训练运行和更大的数据集来扩展训练计算量，是这些收益的一贯驱动力（Hestness et al., 2017；Kaplan et al., 2020b；Hoffmann et al., 2022）。

相比之下，对扩展推理期间所用计算量的投入则相对有限。更大的模型确实比小模型需要更多推理计算，而思维链（chain-of-thought）之类的提示技术（Wei et al., 2023）可以以更长（因而计算上也更昂贵）的输出为代价提升答案质量。然而，在与 LLM 交互时，用户和开发者往往把模型限制为求解问题时只做一次尝试。

在本工作中，我们探索重复采样（图 1）这一扩展推理计算的简单途径，以提升推理性能。已有工作提供了一些令人鼓舞的例子，表明重复采样在数学、代码和解谜场景中可以带来收益（Wang et al., 2023；Rozière et al., 2023；Greenblatt, 2024）。值得注意的是，竞赛编程领域最先进的系统 AlphaCode（Li et al., 2022）发现，每题采样一百万次时性能仍在持续提升。我们的目标是跨一系列任务、模型和样本预算，系统地刻画这些收益。

![Refer to caption](2407.21787v3/banner.png)

图 1：本文遵循的重复采样流程。1) 我们以正温度从 LLM 采样，为一个给定问题生成大量相互独立的候选解。2) 我们使用一个特定领域的验证器（例如代码的单元测试）从生成样本中选出最终答案。

重复采样的有效性由两个关键性质决定：

1. 覆盖率（coverage）：随着样本数量增加，我们能用已生成的任意样本求解多大比例的问题？
2. 精确率（precision）：我们能多经常地从生成集合中识别出正确的样本？

要在现实中取得强劲的表现，这两个性质缺一不可。在样本无限制时，任何对每个序列都赋予非零概率的模型都能达到完美覆盖率。然而，只有当我们能在可行的预算内提升覆盖率时，重复采样才具有实用性。类似地，生成大样本集合也只有在集合中的正确样本能被识别出来时才有用。精确率问题的难度因任务而异。在某些场景中，证明检查器与单元测试等现成工具可以自动验证每一个样本。而在求解文字题等其他情形下，则需要别的验证方法。

我们先探索覆盖率，发现每题最多采样 10,000 次可以显著提升数学与代码任务上的覆盖率（第 2 节）。用 Gemma-2B（Gemma Team et al., 2024）求解 CodeContests（Li et al., 2022）编程题时，我们把覆盖率提升了超过 300 倍：从单样本的 0.02% 到 10,000 个样本的 7.1%。有趣的是，$\log(\text{coverage})$ 与样本数量之间的关系常常近似服从幂律（第 3 节）。对 Llama-3（Meta, 2024）与 Gemma 模型而言，这使覆盖率在若干个数量级上随样本数量近似对数线性增长。

在拥有自动验证工具的场景中，覆盖率的提升会直接转化为任务性能的改进。将重复采样应用于竞赛编程和撰写 Lean 证明时，Llama-3-8B-Instruct 这类模型可以超过 GPT-4o（OpenAI, 2024）等强得多的模型在单样本下的表现。这种放大较弱模型的能力同样适用于由真实 GitHub issue 组成的、颇具挑战性的 SWE-bench Lite 数据集（Jimenez et al., 2024）——当前的单样本最优（SOTA）由 GPT-4o 与 Claude 3.5 Sonnet 的组合取得，为 43%（Aide.dev, 2024）。限制为单样本时，DeepSeek-Coder-V2-Instruct（DeepSeek-AI et al., 2024）只能解决 15.9% 的 issue。而只需把样本数量增加到 250，我们就把解决比例提升到 56%，比最优水平高出 13%。

除了改进模型质量之外，重复采样还提供了一种最小化 LLM 推理成本的新机制（第 2.3 节）。当推理总 FLOPs 保持不变时，我们发现：在某些数据集（如 MATH）上，用较小的模型配合更多样本能最大化覆盖率；而在另一些数据集（如 CodeContests）上，从较大的模型少采样几次更好。我们还在求解 SWE-bench Lite issue 的场景下比较了 DeepSeek-Coder-V2-Instruct、GPT-4o 和 Claude Sonnet 3.5 的 API 价格。在保持智能体框架（Moatless Tools，Örwall, 2024）不变的情况下，从更弱也更便宜的 DeepSeek 模型采样 5 次所解决的 issue 数多于 Claude 或 GPT 的单样本，同时价格便宜 3 倍以上。

最后，我们证明可扩展的验证是充分受益于重复采样的必要条件。随着样本数量增加，覆盖率通过模型对先前未能求解的问题生成出正确解而得到改善。然而，这些越来越稀有的正确生成只有在验证器能够「大海捞针」、从以错误为主的样本集合中把它们识别出来时才有价值。在数学文字题场景中，我们发现两种常见的验证方法（多数投票与奖励模型）并不具备这种能力。用 Llama-3-8B-Instruct 求解 MATH（Hendrycks et al., 2021b）问题时，覆盖率从 100 个样本的 82.9% 增长到 10,000 个样本的 98.44%；而用多数投票或奖励模型选择最终答案时，同一样本范围内性能的最大增幅仅从 40.50% 到 41.41%。随着样本数量增加，覆盖率（即完美验证器下的性能）与这些方法的性能之间的差距也在扩大（图 7）。

总而言之，我们的主要观察如下：

1. 我们证明，通过重复采样扩展推理计算可以在多种任务和模型上带来覆盖率的大幅提升。这使得用大量样本放大较弱模型、并超过更强模型的单样本表现成为可能，有时还更具成本效益。
2. 我们表明，覆盖率与样本数量之间的关系常常可以用一个指数化幂律建模，这提示了推理时计算的一种缩放定律形式。
3. 在没有自动验证器的领域，我们表明常见的验证方法在大约 100 个样本之后便进入平台期。这导致这些方法所能达到的性能与覆盖率上界之间的差距不断扩大。

## 2 扩展重复采样

我们聚焦于可通过/不通过评判的任务，即候选解可以被评分为对或错。此类任务的主要关注指标是成功率：我们所能求解的问题比例。在重复采样中，我们考虑模型在求解一个问题时可以生成许多候选解的设置。因此，成功率既受到为许多问题生成正确样本的能力（即覆盖率）影响，也受到识别这些正确样本的能力（即精确率）影响。

精确率问题的难度取决于样本验证工具的可用性。在 Lean 中证明形式化命题时，证明检查器可以迅速判断一个候选解是否正确。类似地，单元测试可用于验证代码任务的候选解。在这些情形下，精确率被自动处理，提升覆盖率直接转化为更高的成功率。相比之下，可用于验证 GSM8K 与 MATH 数学文字题解答的工具很有限，因此需要额外的验证方法来从许多（往往相互冲突的）样本中确定唯一的最终答案。

我们考虑以下五个任务：

1. GSM8K：一个小学水平数学文字题数据集（Cobbe et al., 2021）。我们在 GSM8K 测试集随机抽取的 128 道题的子集上评估。
2. MATH：另一个数学文字题数据集，总体上比 GSM8K 的题目更难（Chen et al., 2024a）。同样，我们在该数据集测试集随机抽取的 128 道题上评估。
3. MiniF2F-MATH：一个已被形式化为证明检查语言的数学题数据集（Zheng et al., 2021）。我们使用 Lean4 作为语言，并从形式化自 MATH 数据集的 130 道测试集题目上评估。
4. CodeContests：一个竞赛编程数据集（Li et al., 2022）。每道题有一段文字描述，以及一组可用于验证候选解正确性的输入-输出测试用例（对模型隐藏）。我们要求模型用 Python3 撰写解答。
5. SWE-bench Lite：一个真实世界 GitHub issue 数据集，每道题由一段描述和一个代码仓库快照组成（Jimenez et al., 2024）。要解决一道题，模型必须编辑代码库中的文件（在我们使用的 SWE-bench Lite 子集中，只需改动单个文件）。候选解可以用仓库的单元测试套件自动检查。

在这些任务中，MiniF2F-MATH、CodeContests 和 SWE-bench Lite 拥有自动验证器（分别以 Lean4 证明检查器、测试用例和单元测试套件的形式）。我们首先研究重复采样如何提升模型覆盖率。对于拥有自动验证器的任务，覆盖率的提升直接对应成功率的提高；而在一般情形下，覆盖率给出了成功率的上界。在代码场景中，我们对覆盖率的定义与常用的 pass@k 指标（Chen et al., 2021）等价，其中 $k$ 表示每题的样本数量。在 CodeContests 和 SWE-bench Lite 上评估时我们直接使用该指标。对 MiniF2F，指标类似，「通过」由 Lean4 证明检查器定义。对 GSM8K 与 MATH，覆盖率对应于使用一个 oracle 验证器，检查是否有样本通过输出正确的最终答案而「通过」。为降低计算覆盖率时的方差，我们采用 Chen et al. (2021) 的无偏估计公式。在每项实验中，我们先为每道问题索引 $i$ 生成 $N$ 个样本，并计算正确样本的数量 $C_i$。然后对每个感兴趣的 $k\leq N$，按以下公式计算 pass@k 分数：

$$
\text{pass@k}=\frac{1}{\text{\# of problems}}\sum_{i=1}^{\text{\# of problems}}\left(1-\frac{\binom{N-C_{i}}{k}}{\binom{N}{k}}\right) \tag{1}
$$

我们使用 Chen et al. (2021) 建议的上述公式的数值稳定实现。数据与代码见 <https://scalingintelligence.stanford.edu/pubs/large_language_monkeys/>。

### 2.1 重复采样在多种任务上都有效

图 2：在五个任务上，我们发现覆盖率（至少被一个生成样本求解的问题比例）随样本数量扩展而提升。值得注意的是，借助重复采样，我们把一个开源方法在 SWE-bench Lite 上的解决率从 15.9% 提升到 56%。

这里，我们确立重复采样在多个任务和一系列样本预算下都能提升覆盖率。我们在 CodeContests、MiniF2F、GSM8K 和 MATH 上评估 Llama-3-8B-Instruct 与 Llama-3-70B-Instruct，每题生成 10,000 个相互独立的样本。对 SWE-bench Lite，我们使用 DeepSeek-Coder-V2-Instruct（DeepSeek-AI et al., 2024），因为该任务所需的上下文长度超出了 Llama-3 模型的限制。按照求解 SWE-bench issue 的标准做法，我们为 LLM 配备一个软件框架，为模型提供浏览和编辑代码库的工具。本工作中我们使用开源的 Moatless Tools 库（Örwall, 2024）。注意，解决一个 SWE-bench issue 涉及 LLM 与 Moatless Tools 之间的多轮往返交互。该基准测试中的一个样本/尝试指一整条多轮轨迹。为控制成本，我们把每个 issue 的尝试次数限制为 250 次，所有尝试彼此独立。

我们在图 2 中报告结果。我们还纳入了 GPT-4o 在每个任务上的单次尝试表现，以及 SWE-bench Lite 的单次尝试最优水平（CodeStory Aide（Aide.dev, 2024），使用 GPT-4o 与 Claude 3.5 Sonnet 的组合）。在全部五个任务上，覆盖率都随样本预算增加而平滑提升。当所有 LLM 只有一次尝试时，GPT-4o 在每个任务上都优于 Llama 和 DeepSeek 模型。然而，随着样本数量增加，三个较弱的模型全部超过了 GPT-4o 的单次尝试表现。在 SWE-bench Lite 上，我们解决了 56% 的问题，超过了 43% 的单次尝试 SOTA。

### 2.2 重复采样在不同模型规模与家族上都有效

图 3：通过重复采样扩展推理时计算，可在多种模型规模（70M-70B）、多个家族（Llama、Gemma 和 Pythia）以及不同后训练水平（Base 与 Instruct 模型）上带来一致的覆盖率提升。

第 2.1 节的结果表明重复采样提升了覆盖率。然而，我们只在三个 8B 参数以上、较新的指令微调模型上展示了这一趋势。我们现在表明，这些趋势在其他模型规模、家族和后训练水平上同样成立。我们将评估扩展到更广的一组模型：

- Llama 3：Llama-3-8B、Llama-3-8B-Instruct、Llama-3-70B-Instruct。
- Gemma：Gemma-2B、Gemma-7B（Gemma Team et al., 2024）。
- Pythia：Pythia-70M 至 Pythia-12B（共八个模型）（Biderman et al., 2023）。

为最小化推理成本，我们把评估限制在 MATH 与 CodeContests 数据集，结果见图 3。在我们测试的几乎每个模型上，覆盖率都在提升；应用重复采样时，较小的模型展现出一些最陡峭的覆盖率增幅。在 CodeContests 上，Gemma-2B 的覆盖率提升了超过 300 倍：从 pass@1 的 0.02% 到 pass@10k 的 7.1%。类似地，用 Pythia-160M 求解 MATH 问题时，覆盖率从 pass@1 的 0.27% 提升到 pass@10k 的 57%。

各模型覆盖率普遍提升这一模式的例外是 Pythia 家族在 CodeContests 上的评估。所有 Pythia 模型在该数据集上的覆盖率都为零，即使有 10,000 个样本的预算也是如此。我们推测这是因为 Pythia 的训练数据中特定于编程的数据少于 Llama 和 Gemma。

### 2.3 重复采样有助于平衡性能与成本

第 2.1 节与第 2.2 节结果的一个启示是，重复采样使放大较弱模型的能力、并超过更强模型的单样本表现成为可能。这里我们证明，这种放大可以比使用更强、更昂贵的模型更具成本效益，为从业者在联合优化性能与成本时提供了一个新的自由度。

我们首先把 FLOPs 作为成本度量，考察第 2.1 节中的 Llama-3 结果。我们把图 2 的结果重新绘制，将覆盖率可视化为总推理 FLOPs（而非样本预算）的函数。由于 Llama-3 模型是大部分参数用于矩阵乘法的稠密 transformer，我们用以下公式近似推理 FLOPs：

$$
\text{FLOPsPerToken}(\text{ContextLen})\approx 2*\left(\text{NumParameters}+2*\text{NumLayers}*\text{TokenDim}*\text{ContextLen}\right)
$$

$$
\text{TotalInferenceFLOPs}\approx\left(\sum_{t=1}^{\text{NumPromptTokens}}\text{FLOPsPerToken}(t)\right)+\left(\sum_{t=1}^{\text{NumDecodeTokens}}\text{FLOPsPerToken}(t+\text{NumPromptTokens})*\text{NumCompletions}\right)
$$

我们在图 4 中给出 MiniF2F、CodeContests、MATH 和 GSM8K 的重新标度结果。有趣的是，最大化覆盖率的模型随计算预算与任务而异。在 MiniF2F、GSM8K 和 MATH 上，当 FLOP 预算固定时，Llama-3-8B-Instruct 总能获得比更大（也更昂贵）的 70B 模型更高的覆盖率。但对 CodeContests，70B 模型几乎总是更具成本效益。我们注意到，仅考察 FLOPs 是一种粗糙的成本度量，它忽略了系统效率的其他方面（Dehghani et al., 2022）。特别是，重复采样可以利用高批大小和专门的优化，相对于单次尝试的推理工作负载提升系统吞吐量（Juravsky et al., 2024；Athiwaratkun et al., 2024；Zheng et al., 2024）。我们在第 5 节更详细地讨论这一点。

图 4：Llama-3-8B-Instruct 与 Llama-3-70B-Instruct 的成本（以推理 FLOPs 数衡量）与覆盖率比较。可以看到，理想的模型规模取决于任务、计算预算和覆盖率要求。注意 Llama-3-70B-Instruct 在 GSM8K 上未能达到 100% 覆盖率，原因是一个标注错误的标准答案：见附录 E。

我们还用当前 API 定价考察了重复采样在求解 SWE-bench Lite issue 时的美元成本。保持智能体框架（Moatless Tools）不变，我们考虑用 Claude 3.5 Sonnet 和 GPT-4o 每 issue 做一次尝试，以及用 DeepSeek-Coder-V2-Instruct 做重复采样。我们在表 1 中报告每种方式的平均每 issue 成本与 issue 解决率。虽然 DeepSeek 模型弱于 GPT 和 Claude 模型，但它也便宜 10 倍以上。在本例中，重复采样提供了一种比付高价获取强模型更便宜的替代方案，同时取得了更高的 issue 解决率。

| 模型 | 每次尝试成本（美元） | 尝试次数 | 解决 issue 数（%） | 总成本（美元） | 相对总成本 |
| --- | --- | --- | --- | --- | --- |
| DeepSeek-Coder-V2-Instruct | 0.0072 | 5 | 29.62 | 10.8 | 1x |
| GPT-4o | 0.13 | 1 | 24.00 | 39 | 3.6x |
| Claude 3.5 Sonnet | 0.17 | 1 | 26.70 | 51 | 4.7x |

表 1：使用 Moatless Tools 智能体框架在 SWE-bench Lite 数据集上各模型的 API 成本（美元）与性能比较。加大采样数量后，开源的 DeepSeek-Coder-V2-Instruct 模型能以不到三分之一的价格取得与闭源前沿模型相同的 issue 解决率。

## 3 刻画重复采样的收益

LLM 损失与其训练计算量之间的关系已由训练缩放定律很好地刻画（Hestness et al., 2017；Kaplan et al., 2020a；Hoffmann et al., 2022）。这些定律在许多数量级上都经验性地成立，让模型开发者相信训练上的巨额投资终有回报。受训练缩放定律启发，我们在这里旨在更好地刻画覆盖率与样本预算（即推理计算量）之间的关系，并提出两个有趣的观察：

1. 覆盖率与样本数量之间的关系常常可以用一个指数化幂律建模。
2. 对给定任务，同一家族不同模型的覆盖率曲线形状类似于斜率相似但水平偏移不同的 S 形曲线。

### 3.1 重复采样的缩放定律

图 5：对多数任务与模型，覆盖率与样本数量之间的关系可以用指数化幂律建模。我们强调某些曲线（如 Llama-3-8B-Instruct 在 MiniF2F-MATH 上）并不紧密遵循这一趋势。我们展示覆盖率曲线与幂律拟合在对数尺度上均匀取样的 100 个点上的误差的均值与标准差。

这里，我们为覆盖率与样本数量之间的关系建立一个显式模型。GPT-4 技术报告（OpenAI et al., 2024）发现，模型在编程题上的平均对数通过率与其训练计算量之间的关系可以用幂律很好地建模。我们首先采用同一函数类，但现在把覆盖率 $c$ 的对数建模为样本数量 $k$ 的函数：

$$
\log(c)\approx ak^{b} \tag{2}
$$

其中 $a,b\in\mathbb{R}$ 是拟合得到的模型参数。为了直接预测覆盖率，我们对两边取指数，得到最终模型：

$$
c\approx\exp(ak^{b}) \tag{3}
$$

我们在图 5 中给出拟合覆盖率曲线的例子，更多曲线见附录 C.2。虽然这些定律不如训练缩放定律那样精确（在 MiniF2F-MATH 上最为明显），但它们提供了令人鼓舞的早期证据，表明推理扩展的收益是可以刻画的。

### 3.2 各模型覆盖率曲线的相似性

图 6：把同一家族中不同模型的覆盖率曲线叠加。我们通过水平平移每条曲线（x 轴为对数轴）使所有曲线都穿过点 $(1, c)$ 来实现叠加。我们把 $c$ 取为图中所有模型的最大 pass@1 分数。平移后曲线的相似性表明，在同一模型家族内部，采样缩放曲线遵循相似的形状。

有趣的是，比较同一家族中不同模型在同一任务上的覆盖率曲线（x 轴为对数轴，见图 3）时，描绘出的 S 形曲线斜率相同但水平偏移各异。为进一步研究这一点，我们在图 6 中叠加了同一家族中不同模型的覆盖率曲线。做法是选取一个锚点覆盖率值 $c$，将每条曲线（在对数空间中）向左平移，使其穿过点 $(1, c)$。这对应于向左平移 $\log(\text{pass@k}^{-1}(c))$，其中 $\text{pass@k}^{-1}(c)$ 表示使 $\text{pass@k}=c$ 成立的最近自然数 $k$。我们把 $c$ 取为同一家族所有模型的最大 pass@1 分数。这些相似性表明，对同一家族中的各模型而言，把覆盖率从 $c$ 提升到 $c'$ 所需的对数样本预算增量（等价地，样本预算的乘性增幅）近似为常数。

## 4 驾驭重复采样需要精确率

到目前为止，我们专注于度量模型覆盖率，刻画的是我们总能识别出正确模型样本这一情景下重复采样的收益。我们现在转向与之互补的精确率问题：给定一个模型样本集合，我们能多经常地识别出正确的样本？我们特别关心随着样本数量扩大，验证器的表现。对某些问题，正确解被模型以很低的概率采样到（例如 1% 或更低，见图 8）。随着样本数量增加，越来越多的问题得到了稀有正确解的生成，模型覆盖率随之改善。要把这些覆盖率提升转化为更高的成功率，验证器必须能够「大海捞针」，识别出低频出现的正确样本。

### 4.1 常见验证方法并不总能随样本预算扩展

图 7：随着样本数量增加，比较覆盖率（oracle 验证器下的性能）与挑选正确答案的现有主流方法（多数投票、奖励模型选择与奖励模型多数投票）。虽然达到了接近完美的覆盖率，但所有样本选择方法都未能达到覆盖率上界，并在 100 个样本之前就饱和。对每个 k 值，我们在 100 个大小为 k 的子集上计算指标，然后绘制子集间均值与一个标准差。

在我们评估的五个任务中，只有 GSM8K 与 MATH 缺少自动验证解答的工具。我们测试了三种简单且常用的验证方法，考察它们从这些数据集中识别正确解答的能力：

1. 多数投票（majority vote）：我们挑选最常见的最终答案（Wang et al., 2023）。
2. 奖励模型 + Best-of-N：我们用奖励模型（Christiano et al., 2017）为每个解答打分，并从得分最高的样本中选出答案。
3. 奖励模型 + 多数投票：我们计算多数投票，其中每个样本按其奖励模型得分加权。

我们复用第 2 节中用 Llama-3-8B-Instruct 与 Llama-3-70B-Instruct 生成的 10,000 个样本集合。我们使用 ArmoRM-Llama3-8B-v0.1（Wang et al., 2024a）作为奖励模型，它在 RewardBench 排行榜（Lambert et al., 2024）的推理部分得分很高。我们随样本数量增加在图 7 中报告结果。虽然三种方法的成功率最初都随样本数量增加而上升，但它们都在大约 100 个样本处进入平台期。与此同时，覆盖率持续随样本数量增长，最终超过 95%。就多数投票而言，这种成功率饱和是直观的：稀有正确解的出现不会影响多数投票所选出的最常见答案。

鉴于这些验证器（尤其是奖励模型）的糟糕表现，人们自然会问：验证一个候选解到底有多「难」？对 GSM8K 与 MATH，评估正确性时只使用样本的最终答案，中间的思维链被丢弃。如果模型只是在胡乱生成思维链之后猜中一个正确的最终答案，那么验证未必比直接解题更容易。我们通过人工评估 Llama-3-8B-Instruct 对 GSM8K 问题的 105 条正确样本思维链来研究这一问题，结果报告于表 2。

我们发现，超过 90% 被评级的思维链是忠实的，即便在正确答案出现频率很低的问题上也是如此。这些正确的推理步骤表明，存在可供验证器利用的信号来识别正确样本。有趣的是，在此过程中我们还发现了一道标准答案有误的 GSM8K 题目（见附录 E）。这道错误的 GSM8K 题目也是 Llama-3-70B-Instruct 在 10,000 次尝试中唯一没能生成「正确」样本的题目。

| pass@1 | 题目数 | 评级思维链条数 | 正确思维链 | 错误思维链 | 标准答案错误 |
| --- | --- | --- | --- | --- | --- |
| 0-10% | 5 | 15 | 11 | 1 | 1 道题，3 条思维链 |
| 10-25% | 10 | 30 | 27 | 3 | 0 道题 |
| 25-75% | 29 | 30 | 28 | 2 | 0 道题 |
| 75-100% | 84 | 30 | 30 | 0 | 0 道题 |

表 2：对 Llama-3-8B-Instruct 的 GSM8K 答案中思维链推理有效性的人工评估。每道题评级 3 条思维链。即使对于那些模型只有 ≤10% 样本正确的困难题目，思维链也几乎总是遵循有效的逻辑步骤。模型生成与人工标注见[此处](https://docs.google.com/spreadsheets/d/1D-suvkheNA4fjLsO2TuwHNqwx2TIECmp)。

### 4.2 验证器与软件任务：两个警世故事

软件开发任务在可用验证工具方面处于中间地带。一方面，执行和测试代码的能力使得自动验证程度高于非结构化语言任务所能达到的水平。然而，单元测试等工具以黑盒方式验证一段代码，不如证明检查器等方法全面。验证过程中的这些缺陷可能导致假阳性或假阴性，在应用重复采样时值得认真考虑。下面我们给出在生成第 2.1 节结果时遇到的两个软件验证器缺陷的例子。

#### 4.2.1 SWE-bench Lite 中的不稳定测试

在产出 SWE-bench Lite 结果时，我们发现 11.3% 的问题拥有不稳定（flaky）的测试套件——在同一候选解上反复运行时结果并不一致。这些不稳定测试偶尔甚至把数据集自带的标准 issue 解法也判定为错误。此外，某些 issue 的测试套件的行为会随候选解而非确定。例如，两个 SWE-bench Lite issue 涉及操纵天然无序的 Python 集合。这些 issue 的官方解法显式地对集合中的元素排序，因此能可靠地通过测试套件。然而，一些模型生成的候选解没有施加这种排序，于是在一些「走运」的运行中通过测试，在另一些运行中则失败。在附录 B 中，我们列出了识别出不稳定测试的全部问题 ID。我们还在剔除这些问题后重新报告了图 2 的 SWE-bench Lite 结果，发现与在整个数据集上的评估结果相近。

#### 4.2.2 CodeContests 中的假阴性

CodeContests 数据集的每道题都附带一组用于评估解答正确性的输入-输出测试用例。这些测试用例比 APPS（Hendrycks et al., 2021a）等早期编程基准更全面，降低了通过全部测试用例却并未真正解决所描述问题的假阳性解的出现频率。然而，CodeContests 测试套件的构造方式会引入虽正确却未通过测试的假阴性解。

对某些 CodeContests 题目，题目描述允许一个给定测试输入对应多个不同的正确输出。但相应的测试用例并不处理这些情形，而是要求输出某一个特定的正确答案。此外，许多 CodeContests 测试用例是通过变异题目的原始测试用例以程序化方式生成的。一些变异后的输入违反了题目的输入规范（例如题面承诺是正整数，变异输入却为零）。这些畸形的测试用例可能导致不同正确解之间行为不一致。

我们通过在 CodeContests 官方提供的正确解列表上运行每题的测试套件来评估这些问题的普遍程度。在测试集中有 Python3 解的 122 道题里，我们发现 35 道题存在未能通过相应测试的「正确」解。由于我们不允许模型查看题目的全部测试用例（及其特殊之处），对这些问题应用重复采样就带上了「掷骰子」的成分：生成的解不仅要正确，还要恰好输出能通过测试的那个特定输出。

![Refer to caption](2407.21787v3/figures/hist2.png)

图 8：柱状图，展示我们评估所用的 GSM8K 与 MATH 子集中每道题正确样本（10,000 个样本中）的比例。每道题对应一根柱子，柱高对应得到正确答案的样本比例。若自洽性选中了正确答案，柱子为绿色，否则为红色。我们强调，许多题存在正确解，但这些正确解被采样的频率很低。

## 5 讨论与局限

在本工作中，我们探索了重复采样这一在推理时扩展计算量的维度，以提升模型性能。在一系列模型与任务上，重复采样可以显著提升使用任意生成样本即可求解的问题比例（即覆盖率）。当正确解能被识别（无论借助自动验证工具还是其他验证算法）时，重复采样可以在推理阶段放大模型能力。这种放大可以让「较弱模型 + 大量样本」的组合比「较强但更贵模型的较少尝试」表现更好、也更省钱。

改进重复采样：在我们的实验中，我们只探索了重复采样的一个简单版本：对一道题的所有尝试都使用完全相同的提示和超参数、彼此独立地生成。我们相信这一设置还有改进空间，尤其是在以下方向上：

1. 解的多样性：我们目前仅依赖正的采样温度作为在样本间制造多样性的唯一机制。将这种 token 级采样与其他更高层次的方法结合，也许能进一步提升多样性。例如，AlphaCode 用不同的元数据标签为不同样本设置条件。
2. 多轮交互：尽管求解 CodeContests 与 MiniF2F 问题时可以使用自动验证工具，我们只使用了单轮设置：模型生成一个解，没有任何迭代改进的机会。向模型提供来自这些工具的执行反馈应当能提升解答质量。我们对多轮交互带来的权衡很感兴趣：每次尝试变得更昂贵，但也更可能成功。
3. 从先前尝试中学习：目前我们的实验把各次尝试完全相互隔离。获取已有样本（尤其是当验证工具能对它们给出反馈时）可能有助于生成后续尝试。

重复采样与推理系统：重复采样是一种与聊天机器人请求服务截然不同的 LLM 推理工作负载。生产级聊天机器人部署强调低响应延迟，而恪守延迟目标可能迫使较低的每设备批大小，降低硬件利用率。相反，在为单个提示采样大量补全时，可以把更多注意力放在整体吞吐与硬件利用率最大化上。此外，重复采样可以从利用跨序列提示重叠的专门注意力优化中受益（Juravsky et al., 2024；Athiwaratkun et al., 2024；Zheng et al., 2024）。因此，重复采样推理可以以低于向面向聊天机器人的 API 朴素地发起大量并行请求的成本完成。这些成本节约进一步支持了选择从更便宜的模型采样更多次、而非从更贵的模型采样更少次的做法。

验证器：我们第 4 节的结果凸显了在缺乏自动验证工具时改进样本验证方法的重要性。让模型具备评估自身输出的能力，将使重复采样得以扩展到远更多的任务。特别值得关注的是将重复采样应用于创意写作等非结构化任务——这类任务可能需要比我们考虑的通过/不通过任务更主观的样本间比较。发展基于模型的验证器之外的一个替代方向，是设计能把非结构化任务转化为可验证任务的转换器，例如把一个非形式化的数学命题形式化为 Lean 之类的语言，从而可以应用证明检查器。

## 6 相关工作

扩展推理计算：在推理期间执行额外计算的方法已在深度学习的许多领域取得成功。在各种游戏环境中，最先进的方法利用推理时搜索，在决定一步棋之前考察许多可能的未来游戏状态（Campbell et al., 2002；Silver et al., 2017；Brown et al., 2020a）。类似的基于树的方法与 LLM 结合也能奏效，使模型能更好地规划并探索不同的解题路径（Yao et al., 2023；Besta et al., 2024；Tian et al., 2024；Trinh et al., 2024）。增加 LLM 推理计算的另一条轴是允许模型在得出解之前花费 token 思考问题（Yao et al., 2022；Wei et al., 2023；Zelikman et al., 2024）。此外，多个模型可以在推理时被集成以结合各自优势（Wang et al., 2024b；Jiang et al., 2023；Ong et al., 2024；Wan et al., 2024；Chen et al., 2024b）。还有一类方法是让 LLM 批评并改进自身的回答（Madaan et al., 2023；Bai et al., 2022）。

重复采样：先前的工作已经证明重复采样可以在多个领域提升 LLM 能力。最有效的用例之一是编程（Rozière et al., 2023；Chen et al., 2021；Kulal et al., 2019），在该领域性能可持续扩展到一百万个样本，且验证工具（如单元测试）通常可用来自动为每个候选解打分。最近，Greenblatt (2024) 表明重复采样在求解 ARC 挑战（Chollet, 2019）的谜题时很有效，并观察到随样本数量增加呈对数线性扩展。在聊天应用中，重复采样配合奖励模型的 best-of-N 排序可以胜过贪心地采样单个回答（Irvine et al., 2023）。在没有自动验证工具的领域，已有工作表明，用多数投票（Wang et al., 2023）、提示一个 LLM（Davis et al., 2024）、或训练一个基于模型的验证器（Cobbe et al., 2021；Lightman et al., 2023；Wang et al., 2024c；Hosseini et al., 2024；Kang et al., 2024）来确定最终答案，可以比取单个样本提升推理任务上的表现。Nguyen et al. (2024) 发现对超过阈值长度的答案做多数投票，可以胜过对所有答案投票。与我们工作同期，Song et al. (2024) 发现使用可获得的最佳样本能提升 LLM 在聊天、数学和代码任务上的表现，扫描最多 128 个样本。此外，Hassid et al. (2024) 发现在求解编程任务时，从较小的模型多采样可能比从较大的模型少采样更有效。

缩放定律：刻画扩展如何影响模型性能，有助于在资源分配上做出更明智的决策。LLM 训练的缩放定律发现损失与训练计算量之间存在幂律关系，并在给定固定计算预算时给出最优模型与数据集规模的估计（Hestness et al., 2017；Kaplan et al., 2020a；Hoffmann et al., 2022）。Jones (2021) 在棋类游戏 Hex 的语境下发现了缩放定律，观察到性能随模型规模与题目难度可预测地扩展。有趣的是，他们还表明性能随执行树搜索所花费的测试时计算量而扩展。最近，Shao et al. (2024) 在用外部检索数据集增强 LLM 时观察到缩放定律，发现检索任务上的表现随检索语料库规模平滑扩展。

## 7 致谢

我们感谢 Together AI 为本项目部分赞助了计算资源，也感谢 Rahul Chalamala 与 Ben Athiwaratkun 在管理这些基础设施方面的帮助。我们感谢 John Yang 在运行 SWE-bench 实验时给出的建议与支持。最后，我们感谢 Mayee Chen、Neel Guha、Quinn McIntyre、Jon Saad-Falcon 和 Benjamin Spector 在整个项目中的有益讨论与反馈。

我们衷心感谢以下支持：NIH（No. U54EB020405，Mobilize）；NSF（Nos. CCF2247015，Hardware-Aware；CCF1763315，Beyond Sparsity；CCF1563078，Volume to Velocity；1937301，RTML）；US DEVCOM ARL（Nos. W911NF-23-2-0184，Long-context；W911NF-21-2-0251，Interactive Human-AI Teaming）；ONR（Nos. N000142312633，Deep Signal Processing）；Stanford HAI（No. 247183）；NXP、Xilinx、LETI-CEA、Intel、IBM、Microsoft、NEC、Toshiba、TSMC、ARM、Hitachi、BASF、Accenture、Ericsson、Qualcomm、Analog Devices、Google Cloud、Salesforce、Total、HAI-GCP Cloud Credits for Research 计划、斯坦福数据科学计划（SDSI），以及斯坦福 DAWN 项目的成员：Meta、Google 和 VMWare。美国政府被授权出于政府目的复制和分发重印本，尽管其上可能有任何版权标注。本材料中表达的观点、发现、结论或建议均为作者个人观点，不一定反映 NIH、ONR 或美国政府的观点、政策或背书，无论是明示还是暗示。

本工作在 Clarendon Fund 奖学金的资助下完成。

## 参考文献

- [1]

  Aide.dev, 2024.
  URL <https://aide.dev/>.
- [2]

  Hello gpt-4o, 2024.
  URL <https://openai.com/index/hello-gpt-4o/>.
- [3]

  Meta llama 3, 2024.
  URL <https://llama.meta.com/llama3/>.
- [4]

  Claude 3.5 sonnet, 2024.
  URL <https://www.anthropic.com/news/claude-3-5-sonnet>.
- [5]

  Voyage ai, 2024.
  URL <https://www.voyageai.com/>.
- [6]

  Ben Athiwaratkun, Sujan Kumar Gonugondla, Sanjay Krishna Gouda, Haifeng Qian, Hantian Ding, Qing Sun, Jun Wang, Jiacheng Guo, Liangfu Chen, Parminder Bhatia, Ramesh Nallapati, Sudipta Sengupta, and Bing Xiang.
  Bifurcated attention: Accelerating massively parallel decoding with shared prefixes in llms, 2024.
  URL <https://arxiv.org/abs/2403.08845>.
- [7]

  Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones, Anna Chen, Anna Goldie, Azalia Mirhoseini, Cameron McKinnon, Carol Chen, Catherine Olsson, Christopher Olah, Danny Hernandez, Dawn Drain, Deep Ganguli, Dustin Li, Eli Tran-Johnson, Ethan Perez, Jamie Kerr, Jared Mueller, Jeffrey Ladish, Joshua Landau, Kamal Ndousse, Kamile Lukosuite, Liane Lovitt, Michael Sellitto, Nelson Elhage, Nicholas Schiefer, Noemi Mercado, Nova DasSarma, Robert Lasenby, Robin Larson, Sam Ringer, Scott Johnston, Shauna Kravec, Sheer El Showk, Stanislav Fort, Tamera Lanham, Timothy Telleen-Lawton, Tom Conerly, Tom Henighan, Tristan Hume, Samuel R. Bowman, Zac Hatfield-Dodds, Ben Mann, Dario Amodei, Nicholas Joseph, Sam McCandlish, Tom Brown, and Jared Kaplan.
  Constitutional ai: Harmlessness from ai feedback, 2022.
- [8]

  Maciej Besta, Nils Blach, Ales Kubicek, Robert Gerstenberger, Michal Podstawski, Lukas Gianinazzi, Joanna Gajda, Tomasz Lehmann, Hubert Niewiadomski, Piotr Nyczyk, and Torsten Hoefler.
  Graph of thoughts: Solving elaborate problems with large language models.
  *Proceedings of the AAAI Conference on Artificial Intelligence*, 38(16):17682–17690, March 2024.
  ISSN 2159-5399.
  doi: 10.1609/aaai.v38i16.29720.
  URL <http://dx.doi.org/10.1609/aaai.v38i16.29720>.
- [9]

  Stella Biderman, Hailey Schoelkopf, Quentin Anthony, Herbie Bradley, Kyle O’Brien, Eric Hallahan, Mohammad Aflah Khan, Shivanshu Purohit, USVSN Sai Prashanth, Edward Raff, Aviya Skowron, Lintang Sutawika, and Oskar van der Wal.
  Pythia: A suite for analyzing large language models across training and scaling, 2023.
  URL <https://arxiv.org/abs/2304.01373>.
- [10]

  Noam Brown, Anton Bakhtin, Adam Lerer, and Qucheng Gong.
  Combining deep reinforcement learning and search for imperfect-information games.
  In *Proceedings of the 34th International Conference on Neural Information Processing Systems*, NIPS ’20, Red Hook, NY, USA, 2020a. Curran Associates Inc.
  ISBN 9781713829546.
- [11]

  Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei.
  Language models are few-shot learners, 2020b.
  URL <https://arxiv.org/abs/2005.14165>.
- [12]

  Murray Campbell, A. Joseph Hoane, and Feng-hsiung Hsu.
  Deep blue.
  *Artif. Intell.*, 134(1–2):57–83, jan 2002.
  ISSN 0004-3702.
  doi: 10.1016/S0004-3702(01)00129-1.
  URL <https://doi.org/10.1016/S0004-3702(01)00129-1>.
- [13]

  Guoxin Chen, Minpeng Liao, Chengxi Li, and Kai Fan.
  Alphamath almost zero: process supervision without process, 2024a.
- [14]

  Lingjiao Chen, Jared Quincy Davis, Boris Hanin, Peter Bailis, Ion Stoica, Matei Zaharia, and James Zou.
  Are more llm calls all you need? towards scaling laws of compound inference systems, 2024b.
  URL <https://arxiv.org/abs/2403.02419>.
- [15]

  Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba.
  Evaluating large language models trained on code, 2021.
  URL <https://arxiv.org/abs/2107.03374>.
- [16]

  François Chollet.
  On the measure of intelligence, 2019.
  URL <https://arxiv.org/abs/1911.01547>.
- [17]

  Paul Christiano, Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg, and Dario Amodei.
  Deep reinforcement learning from human preferences, 2017.
  URL <https://arxiv.org/abs/1706.03741>.
- [18]

  Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman.
  Training verifiers to solve math word problems, 2021.
- [19]

  Jared Quincy Davis, Boris Hanin, Lingjiao Chen, Peter Bailis, Ion Stoica, and Matei Zaharia.
  Networks of networks: Complexity class principles applied to compound ai systems design, 2024.
  URL <https://arxiv.org/abs/2407.16831>.
- [20]

  DeepSeek-AI et al.
  Deepseek-v2: A strong, economical, and efficient mixture-of-experts language model, 2024.
  URL <https://arxiv.org/abs/2405.04434>.
- [21]

  Mostafa Dehghani, Anurag Arnab, Lucas Beyer, Ashish Vaswani, and Yi Tay.
  The efficiency misnomer, 2022.
  URL <https://arxiv.org/abs/2110.12894>.
- [22]

  Leo Gao, Jonathan Tow, Baber Abbasi, Stella Biderman, Sid Black, Anthony DiPofi, Charles Foster, Laurence Golding, Jeffrey Hsu, Alain Le Noac’h, Haonan Li, Kyle McDonell, Niklas Muennighoff, Chris Ociepa, Jason Phang, Laria Reynolds, Hailey Schoelkopf, Aviya Skowron, Lintang Sutawika, Eric Tang, Anish Thite, Ben Wang, Kevin Wang, and Andy Zou.
  A framework for few-shot language model evaluation, 12 2023.
  URL <https://zenodo.org/records/10256836>.
- [23]

  Ryan Greenblatt.
  Geting 50
  <https://www.lesswrong.com/posts/Rdwui3wHxCeKb7feK/getting-50-sota-on-arc-agi-with-gpt-4o>, 2024.
- [24]

  Michael Hassid, Tal Remez, Jonas Gehring, Roy Schwartz, and Yossi Adi.
  The larger the better? improved llm code-generation via budget reallocation, 2024.
  URL <https://arxiv.org/abs/2404.00725>.
- [25]

  Dan Hendrycks, Steven Basart, Saurav Kadavath, Mantas Mazeika, Akul Arora, Ethan Guo, Collin Burns, Samir Puranik, Horace He, Dawn Song, and Jacob Steinhardt.
  Measuring coding challenge competence with apps, 2021a.
- [26]

  Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt.
  Measuring mathematical problem solving with the math dataset, 2021b.
- [27]

  Joel Hestness, Sharan Narang, Newsha Ardalani, Gregory Diamos, Heewoo Jun, Hassan Kianinejad, Md. Mostofa Ali Patwary, Yang Yang, and Yanqi Zhou.
  Deep learning scaling is predictable, empirically, 2017.
  URL <https://arxiv.org/abs/1712.00409>.
- [28]

  Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, Tom Hennigan, Eric Noland, Katie Millican, George van den Driessche, Bogdan Damoc, Aurelia Guy, Simon Osindero, Karen Simonyan, Erich Elsen, Jack W. Rae, Oriol Vinyals, and Laurent Sifre.
  Training compute-optimal large language models, 2022.
  URL <https://arxiv.org/abs/2203.15556>.
- [29]

  Arian Hosseini, Xingdi Yuan, Nikolay Malkin, Aaron Courville, Alessandro Sordoni, and Rishabh Agarwal.
  V-star: Training verifiers for self-taught reasoners, 2024.
- [30]

  Robert Irvine, Douglas Boubert, Vyas Raina, Adian Liusie, Ziyi Zhu, Vineet Mudupalli, Aliaksei Korshuk, Zongyi Liu, Fritz Cremer, Valentin Assassi, Christie-Carol Beauchamp, Xiaoding Lu, Thomas Rialan, and William Beauchamp.
  Rewarding chatbots for real-world engagement with millions of users, 2023.
  URL <https://arxiv.org/abs/2303.06135>.
- [31]

  Dongfu Jiang, Xiang Ren, and Bill Yuchen Lin.
  Llm-blender: Ensembling large language models with pairwise ranking and generative fusion, 2023.
  URL <https://arxiv.org/abs/2306.02561>.
- [32]

  Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan.
  Swe-bench: Can language models resolve real-world github issues?, 2024.
  URL <https://arxiv.org/abs/2310.06770>.
- [33]

  Andy L. Jones.
  Scaling scaling laws with board games, 2021.
  URL <https://arxiv.org/abs/2104.03113>.
- [34]

  Jordan Juravsky, Bradley Brown, Ryan Ehrlich, Daniel Y Fu, Christopher Ré, and Azalia Mirhoseini.
  Hydragen: High-throughput llm inference with shared prefixes.
  *arXiv preprint arXiv:2402.05099*, 2024.
- [35]

  Jikun Kang, Xin Zhe Li, Xi Chen, Amirreza Kazemi, Qianyi Sun, Boxing Chen, Dong Li, Xu He, Quan He, Feng Wen, Jianye Hao, and Jun Yao.
  Mindstar: Enhancing math reasoning in pre-trained llms at inference time, 2024.
  URL <https://arxiv.org/abs/2405.16265>.
- [36]

  Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei.
  Scaling laws for neural language models, 2020a.
- [37]

  Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei.
  Scaling laws for neural language models, 2020b.
  URL <https://arxiv.org/abs/2001.08361>.
- [38]

  Sumith Kulal, Panupong Pasupat, Kartik Chandra, Mina Lee, Oded Padon, Alex Aiken, and Percy Liang.
  Spoc: Search-based pseudocode to code, 2019.
  URL <https://arxiv.org/abs/1906.04908>.
- [39]

  Nathan Lambert, Valentina Pyatkin, Jacob Morrison, LJ Miranda, Bill Yuchen Lin, Khyathi Chandu, Nouha Dziri, Sachin Kumar, Tom Zick, Yejin Choi, Noah A. Smith, and Hannaneh Hajishirzi.
  Rewardbench: Evaluating reward models for language modeling, 2024.
  URL <https://arxiv.org/abs/2403.13787>.
- [40]

  Aitor Lewkowycz, Anders Andreassen, David Dohan, Ethan Dyer, Henryk Michalewski, Vinay Ramasesh, Ambrose Slone, Cem Anil, Imanol Schlag, Theo Gutman-Solo, Yuhuai Wu, Behnam Neyshabur, Guy Gur-Ari, and Vedant Misra.
  Solving quantitative reasoning problems with language models, 2022.
  URL <https://arxiv.org/abs/2206.14858>.
- [41]

  Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hubert, Peter Choy, Cyprien de Masson d’Autume, Igor Babuschkin, Xinyun Chen, Po-Sen Huang, Johannes Welbl, Sven Gowal, Alexey Cherepanov, James Molloy, Daniel J. Mankowitz, Esme Sutherland Robson, Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, and Oriol Vinyals.
  Competition-level code generation with alphacode.
  *Science*, 378(6624):1092–1097, December 2022.
  ISSN 1095-9203.
  doi: 10.1126/science.abq1158.
  URL <http://dx.doi.org/10.1126/science.abq1158>.
- [42]

  Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe.
  Let’s verify step by step, 2023.
- [43]

  Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, Shashank Gupta, Bodhisattwa Prasad Majumder, Katherine Hermann, Sean Welleck, Amir Yazdanbakhsh, and Peter Clark.
  Self-refine: Iterative refinement with self-feedback, 2023.
  URL <https://arxiv.org/abs/2303.17651>.
- [44]

  Alex Nguyen, Dheeraj Mekala, Chengyu Dong, and Jingbo Shang.
  When is the consistent prediction likely to be a correct prediction?, 2024.
  URL <https://arxiv.org/abs/2407.05778>.
- [45]

  Isaac Ong, Amjad Almahairi, Vincent Wu, Wei-Lin Chiang, Tianhao Wu, Joseph E. Gonzalez, M Waleed Kadous, and Ion Stoica.
  Routellm: Learning to route llms with preference data, 2024.
  URL <https://arxiv.org/abs/2406.18665>.
- [46]

  OpenAI et al.
  Gpt-4 technical report, 2024.
  URL <https://arxiv.org/abs/2303.08774>.
- [47]

  Alec Radford, Jeff Wu, Rewon Child, David Luan, Dario Amodei, and Ilya Sutskever.
  Language models are unsupervised multitask learners.
  2019.
- [48]

  Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi, Jingyu Liu, Romain Sauvestre, Tal Remez, Jérémy Rapin, Artyom Kozhevnikov, Ivan Evtimov, Joanna Bitton, Manish Bhatt, Cristian Canton Ferrer, Aaron Grattafiori, Wenhan Xiong, Alexandre Défossez, Jade Copet, Faisal Azhar, Hugo Touvron, Louis Martin, Nicolas Usunier, Thomas Scialom, and Gabriel Synnaeve.
  Code llama: Open foundation models for code, 2023.
  URL <https://arxiv.org/abs/2308.12950>.
- [49]

  Rulin Shao, Jacqueline He, Akari Asai, Weijia Shi, Tim Dettmers, Sewon Min, Luke Zettlemoyer, and Pang Wei Koh.
  Scaling retrieval-based language models with a trillion-token datastore, 2024.
  URL <https://arxiv.org/abs/2407.12854>.
- [50]

  David Silver, Thomas Hubert, Julian Schrittwieser, Ioannis Antonoglou, Matthew Lai, Arthur Guez, Marc Lanctot, Laurent Sifre, Dharshan Kumaran, Thore Graepel, Timothy Lillicrap, Karen Simonyan, and Demis Hassabis.
  Mastering chess and shogi by self-play with a general reinforcement learning algorithm, 2017.
- [51]

  Yifan Song, Guoyin Wang, Sujian Li, and Bill Yuchen Lin.
  The good, the bad, and the greedy: Evaluation of llms should not ignore non-determinism, 2024.
  URL <https://arxiv.org/abs/2407.10457>.
- [52]

  Gemma Team et al.
  Gemma: Open models based on gemini research and technology, 2024.
  URL <https://arxiv.org/abs/2403.08295>.
- [53]

  Ye Tian, Baolin Peng, Linfeng Song, Lifeng Jin, Dian Yu, Haitao Mi, and Dong Yu.
  Toward self-improvement of llms via imagination, searching, and criticizing, 2024.
  URL <https://arxiv.org/abs/2404.12253>.
- [54]

  Trieu H. Trinh, Yuhuai Wu, Quoc V. Le, He He, and Thang Luong.
  Solving olympiad geometry without human demonstrations.
  *Nature*, 625(7995):476–482, 2024.
  ISSN 1476-4687.
  doi: 10.1038/s41586-023-06747-5.
  URL <https://doi.org/10.1038/s41586-023-06747-5>.
- [55]

  Pauli Virtanen, Ralf Gommers, Travis E. Oliphant, Matt Haberland, Tyler Reddy, David Cournapeau, Evgeni Burovski, Pearu Peterson, Warren Weckesser, Jonathan Bright, Stéfan J. van der Walt, Matthew Brett, Joshua Wilson, K. Jarrod Millman, Nikolay Mayorov, Andrew R. J. Nelson, Eric Jones, Robert Kern, Eric Larson, C J Carey, İlhan Polat, Yu Feng, Eric W. Moore, Jake VanderPlas, Denis Laxalde, Josef Perktold, Robert Cimrman, Ian Henriksen, E. A. Quintero, Charles R. Harris, Anne M. Archibald, Antônio H. Ribeiro, Fabian Pedregosa, Paul van Mulbregt, and SciPy 1.0 Contributors.
  SciPy 1.0: Fundamental Algorithms for Scientific Computing in Python.
  *Nature Methods*, 17:261–272, 2020.
  doi: 10.1038/s41592-019-0686-2.
- [56]

  Fanqi Wan, Xinting Huang, Deng Cai, Xiaojun Quan, Wei Bi, and Shuming Shi.
  Knowledge fusion of large language models, 2024.
  URL <https://arxiv.org/abs/2401.10491>.
- [57]

  Haoxiang Wang, Wei Xiong, Tengyang Xie, Han Zhao, and Tong Zhang.
  Interpretable preferences via multi-objective reward modeling and mixture-of-experts, 2024a.
  URL <https://arxiv.org/abs/2406.12845>.
- [58]

  Junlin Wang, Jue Wang, Ben Athiwaratkun, Ce Zhang, and James Zou.
  Mixture-of-agents enhances large language model capabilities, 2024b.
  URL <https://arxiv.org/abs/2406.04692>.
- [59]

  Peiyi Wang, Lei Li, Zhihong Shao, R. X. Xu, Damai Dai, Yifei Li, Deli Chen, Y. Wu, and Zhifang Sui.
  Math-shepherd: Verify and reinforce llms step-by-step without human annotations, 2024c.
  URL <https://arxiv.org/abs/2312.08935>.
- [60]

  Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou.
  Self-consistency improves chain of thought reasoning in language models, 2023.
- [61]

  Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, and Denny Zhou.
  Chain-of-thought prompting elicits reasoning in large language models, 2023.
- [62]

  Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao.
  React: Synergizing reasoning and acting in language models, 2022.
  URL <https://arxiv.org/abs/2210.03629>.
- [63]

  Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, and Karthik Narasimhan.
  Tree of thoughts: Deliberate problem solving with large language models, 2023.
  URL <https://arxiv.org/abs/2305.10601>.
- [64]

  Eric Zelikman, Georges Harik, Yijia Shao, Varuna Jayasiri, Nick Haber, and Noah D. Goodman.
  Quiet-star: Language models can teach themselves to think before speaking, 2024.
  URL <https://arxiv.org/abs/2403.09629>.
- [65]

  Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
  Minif2f: a cross-system benchmark for formal olympiad-level mathematics.
  *arXiv preprint arXiv:2109.00110*, 2021.
- [66]

  Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Chuyue Sun, Jeff Huang, Cody Hao Yu, Shiyi Cao, Christos Kozyrakis, Ion Stoica, Joseph E. Gonzalez, Clark Barrett, and Ying Sheng.
  Sglang: Efficient execution of structured language model programs, 2024.
  URL <https://arxiv.org/abs/2312.07104>.
- [67]

  Albert Örwall.
  Moatless tools.
  <https://github.com/aorwall/moatless-tools/tree/a1017b78e3e69e7d205b1a3faa83a7d19fce3fa6>, 2024.

## 附录 A 采样实验设置

### A.1 Lean 形式化证明

我们在 [lean4 MiniF2F 数据集](https://github.com/rah4927/lean-dojo-mew/blob/main/MiniF2F/Test.lean)测试集中与形式化 MATH 题目对应的 130 道题上报告结果。该数据集派生自 Zheng et al. (2021) 创建的原始 MiniF2F 数据集的[修正版](https://github.com/facebookresearch/miniF2F)。我们以 0.5 的温度采样，不使用 nucleus 采样。每题生成 10,000 个样本。我们使用[验证集](https://github.com/rah4927/lean-dojo-mew/blob/main/MiniF2F/Validation.lean)中以下 5 条定理的证明作为少样本示例：

- `mathd_algebra_116`
- `amc12_2000_p5`
- `mathd_algebra_132`
- `mathd_algebra_11`
- `mathd_numbertheory_84`

我们的提示由以下部分组成：

1. 少样本示例。
2. HuggingFace 数据集 `cat-searcher/minif2f-lean4`（lean4 MiniF2F 数据集的一个上传版本）中每道题都出现的 header import。
3. 定理定义。为避免从定理名称泄露如何证明该定理的信息，我们把定理名替换为 `theorem_i`。少样本示例中 $i\in\{1,2,3,4,5\}$，当前题目 $i=6$。

我们把生成解答的最大 token 长度设为 200。为给解答评分，我们使用 `lean-dojo 1.1.2` 库与 lean 版本 `4.3.0-rc2`。每个 tactic 步骤的超时设为 10 秒。

少样本示例

Write a lean4 proof to the provided formal statement. You have access to the standard mathlib4 library.

```import Mathlib.Algebra.BigOperators.Basic

import Mathlib.Data.Real.Basic

import Mathlib.Data.Complex.Basic

import Mathlib.Data.Nat.Log

import Mathlib.Data.Complex.Exponential

import Mathlib.NumberTheory.Divisors

import Mathlib.Data.ZMod.Defs

import Mathlib.Data.ZMod.Basic

import Mathlib.Topology.Basic

import Mathlib.Data.Nat.Digits

open BigOperators

open Real

open Nat

open Topology

theorem theorem1

Int.floor ((9:ℝ) / 160 * 100) = 5 :=

by (

rw [Int.floor_eq_iff]

constructor

all_goals norm_num

)```

示例提示

Write a lean4 proof to the provided formal statement. You have access to the standard mathlib4 library.

```import Mathlib.Algebra.BigOperators.Basic

import Mathlib.Data.Real.Basic

import Mathlib.Data.Complex.Basic

import Mathlib.Data.Nat.Log

import Mathlib.Data.Complex.Exponential

import Mathlib.NumberTheory.Divisors

import Mathlib.Data.ZMod.Defs

import Mathlib.Data.ZMod.Basic

import Mathlib.Topology.Basic

import Mathlib.Data.Nat.Digits

open BigOperators

open Real

open Nat

open Topology

theorem theorem6

(b h v : ℝ)

(h_{0} : 0 << b ∧ 0 << h ∧ 0 << v)

(h_{1} : v = 1 / 3 * (b * h))

(h_{2} : b = 30)

(h_{3} : h = 13 / 2) :

v = 65 :=

by (

### A.2 CodeContests

我们在测试集中 140 道题干描述不含图片标签的题目上报告结果。遵循 CodeLlama（Rozière et al., 2023）的实验设置，我们以 0.6 的温度与 0.95 的 top-p 采样。每题生成 10,000 个样本。我们使用从训练集随机抽取的两个少样本示例（逐题随机）。生成解答的最大 token 长度设为 1024。我们使用与 Li et al. (2022) 相同的答案比较函数，并用公开、私有与生成测试的拼接来验证解答的正确性。

少样本示例

Q: Write python code to solve the following coding problem that obeys the constraints and passes the example test cases. The output code needs to read from and write to standard IO. Please wrap your code answer using ```:

Petya has equal…

…

(Rest of question and input/output examples)

…

A: ```

```
n = int(input())
a = int(input())
b = int(input())
ans = 6
cnt = 0
cur = 2
cnt += 2 * ((n - b) // a)
while cnt < 4:
    cur += 1
    cnt += (n // a)
ans = min(ans, cur)
if b * 2 <= n:
    cur, cnt = 0, 0
    cur = 1
    cnt += ((n - 2 * b) // a)
    while cnt < 4:
        cur += 1
        cnt += (n // a)
    ans = min(ans, cur)
print(ans)
```

```

示例提示

Q: Write python code to solve the following coding problem that obeys the constraints and passes the example test cases. The output code needs to read from and write to standard IO. Please wrap your code answer using ```:

This is the…

…

(Rest of question and input/output examples)

…

A:

### A.3 MATH

我们在随机选取的 128 道测试集题目上报告结果。我们以 0.6 的温度采样，不使用 nucleus 采样。每题使用 Lewkowycz et al. (2022) 的固定 5 个少样本示例。每题生成 10,000 个样本。生成解答的最大 token 长度设为 512。为给解答评分，我们使用 LMEval（Gao et al., 2023）的 `minerva_math` 函数提取模型的最终答案。然后，若提取的答案与标准答案精确字符串匹配，或 LMEval 中 `minerva_math` 的 `is_equiv` 函数求值为真，则判定为正确。

少样本示例

Problem:

If $\det\mathbf{A}=2$ and $\det\mathbf{B}=12$, then find $\det(\mathbf{A}\mathbf{B})$.
Solution:

We have that $\det(\mathbf{A}\mathbf{B})=(\det\mathbf{A})(\det\mathbf{B})=(2)(12)=\boxed{24}$.
Final Answer: The final answer is $24$. I hope it is correct.

示例提示

Problem:

What is the domain of the function

$f(x)=\frac{(2x-3)(2x+5)}{(3x-9)(3x+6)}~?$
Express your answer as an interval or as a union of intervals.
Solution:

### A.4 GSM8K

我们在随机抽样的 128 道测试集题目上报告结果。我们以 0.6 的温度采样，不使用 nucleus 采样。使用从训练集逐题随机抽取的 5 个少样本示例。每题生成 10,000 个样本。生成解答的最大 token 长度设为 512。为给解答评分，我们遵循 LMEval（Gao et al., 2023），用正则表达式提取四重井号之后的字符串。与 MATH 类似，随后通过检查提取的答案与标准答案是否精确字符串匹配、或 `is_equiv` 是否求值为真来评估正确性。

少样本示例

Question: James decides to replace his car. He sold his $20,000 car for 80% of its value and then was able to haggle to buy a $30,000 sticker price car for 90% of its value. How much was he out of pocket?

Answer: He sold his car for 20000*.8=$`<<`20000*.8=16000`>>`16,000
He bought the new car for 30,000*.9=$`<<`30000*.9=27000`>>`27,000
That means he was out of pocket 27,000-16,000=$`<<`27000-16000=11000`>>`11,000

#### 11000

示例提示

Question: Mary has 6 jars of sprinkles in her pantry. Each jar of sprinkles can decorate 8 cupcakes. Mary wants to bake enough cupcakes to use up all of her sprinkles. If each pan holds 12 cupcakes, how many pans worth of cupcakes should she bake?

Answer:

## 附录 B SWE-bench Lite

### B.1 实验设置

在我们的实验中，我们使用 DeepSeek-Coder-V2-Instruct 搭配 Moatless Tools 智能体框架（commit a1017b78e3e69e7d205b1a3faa83a7d19fce3fa6）。检索使用 Voyage AI（Voyage AI, 2024）嵌入，即 Moatless Tools 的默认设置。我们没有对模型或框架做任何修改，完全将它们作为现成组件使用。

在这一设置下，我们使用标准的基于温度的采样为每道题采样 250 个相互独立的补全。为确定最优采样温度，我们在测试集随机抽取的 50 道题上做了扫描，测试了 1.0、1.4、1.6 和 1.8 的温度。基于这些结果，我们在主实验中选择了 1.6 的温度。

### B.2 测试套件不稳定性

在分析过程中，我们在 SWE-bench Lite 中识别出 34 道题的测试套件含有不稳定测试。使用 SWE-bench 作者提供的测试执行框架，我们对每个解反复测试：对某些解，有时被标记为正确，另一些时候被标记为错误。在这 34 例中的 30 例，即便对数据集作者提供的正确解我们也观察到了不稳定性。表 3 列出了这 34 个含不稳定测试的实例 ID。

表 3：SWE-bench Lite 中含有不稳定测试的问题的实例 ID。

| 仓库 | 实例 ID |
| --- | --- |
| django | django__django-13315, django__django-13447, django__django-13590,  django__django-13710, django__django-13757, django__django-13933,  django__django-13964, django__django-14017, django__django-14238,  django__django-14382, django__django-14608, django__django-14672,  django__django-14752, django__django-14915, django__django-14997,  django__django-14999, django__django-15320, django__django-15738,  django__django-15790, django__django-15814, django__django-15819,  django__django-16229, django__django-16379, django__django-16400,  django__django-17051 |
| sympy | sympy__sympy-13146, sympy__sympy-13177, sympy__sympy-16988 |
| requests | psf__requests-863, psf__requests-2317,  psf__requests-2674, psf__requests-3362 |
| scikit-learn | scikit-learn__scikit-learn-13241 |
| matplotlib | matplotlib__matplotlib-23987 |

另一个实例 astropy__astropy-6938 在某些机器上不稳定，在另一些机器上则稳定。SWE-bench 的作者能够复现该不稳定性，但我们无法做到。我们的初步调查表明，这一具体问题源于运行单元测试的 docker 环境中依赖版本未固定。

这里我们给出剔除表 3 中问题后（266 道题）子集上的结果。对完整数据集评估，凡含有不稳定测试的题目，我们把测试套件运行 11 次，并用多数投票判定一个解是通过还是失败。对不含不稳定测试的子集评估时，我们比较的所有基线都公开了它们正确解决的问题，因此我们只需剔除含不稳定测试的问题并重新计算它们的分数。

图 9：SWE-bench Lite 结果，分别为剔除与保留含不稳定测试的问题。左图剔除了表 3 中的所有问题，右图包含所有问题。我们注意到，无论是否包含不稳定测试，趋势都相同。

## 附录 C 缩放定律细节

### C.1 实验细节

为把指数化幂律拟合到覆盖率曲线，我们首先在对数尺度上从 0 到 10,000 均匀抽取 40 个点并去重。然后使用 SciPy（Virtanen et al., 2020）的 `curve_fit` 函数，找出式 (3) 中最拟合这些点的 $a$ 与 $b$ 参数。

### C.2 附加结果

在图 10 中，我们展示了针对扩展的任务与模型集合、把幂律拟合到覆盖率曲线的附加结果。

图 10：对扩展的任务与模型集合，将指数化幂律拟合到覆盖率曲线。

## 附录 D 精确率细节

为计算多数投票、奖励模型 + Best-of-N 与奖励模型 + 多数投票指标，我们使用第 2 节引入的 MATH 与 GSM8K 数据集相同的 128 道题子集。每道题对应我们测试的每个模型的 10,000 个样本。对每种验证方法，我们抽取 100 个大小为 $k$ 的随机子集，并用每个子集计算成功率。我们在图 7 中报告子集间的均值与标准差。计算多数投票答案时，我们取每个子集中出现次数最多的答案（注意：两个答案若精确字符串匹配或 `is_equiv` 求值为真，即视为等价）。对奖励模型 + Best-of-N，我们取奖励模型打分最高的答案。对奖励模型 + 多数投票指标，我们把所有最终答案相同的样本的奖励模型得分求和，并取总和最高的最终答案。

## 附录 E GSM8K 错误答案

如第 4.1 节所述，我们发现 [GSM8K 测试集中的一道题（HuggingFace 上索引 1042）](https://huggingface.co/datasets/openai/gsm8k/viewer/main/test?row=1042)的标准解答有误。

Question

Johnny's dad brought him to watch some horse racing and his dad bet money. On the first race, he lost $5. On the second race, he won $11 more than twice the amount he previously lost. On the third race, he lost 1.5 times as much as he won in the second race. How much did he lose on average that day?

Answer

On the second race he won $11 because 1+5×2=<<1+5*2=11>>11

On the third race he lost $15 because 10×1.5=<<10*1.5=15>>15

He lost a total of $20 on the first and third races because 15+5=<<15+5=20>>20
He lost $9 that day because 11−20=<<11-20=-9>>-9

He lost an average of $3 per race because 9/3=<<9/3=3>>3

#### 3

错误出在解答的第二行：第三场比赛 Johnny 的爸爸输掉的是 $16.5 而不是 $15，也就是说他赢了 $11，却输掉了 $16.5+$5=$21.5。因此，正确答案是平均每场输 $3.5，而不是（数据集中的答案）每场输 $3。
