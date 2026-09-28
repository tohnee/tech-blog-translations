---
title: "通过训练验证器求解数学应用题"
title_en: "Training Verifiers to Solve Math Word Problems"
arxiv: 2110.14168
source: https://arxiv.org/abs/2110.14168
crawled: 2026-09-23
translated: 2026-09-23
---

# 通过训练验证器求解数学应用题

> 原文：[Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168) · Stanford CS329A 指定阅读

Karl Cobbe、Vineet Kosaraju、Mohammad Bavarian、Mark Chen、Heewoo Jun、Łukasz Kaiser、Matthias Plappert、Jerry Tworek、Jacob Hilton、Reiichiro Nakano、Christopher Hesse、John Schulman

注：同等贡献。通讯作者：Karl Cobbe <karl@openai.com>、Vineet Kosaraju <vineet@openai.com>
所属机构：OpenAI

###### 摘要

最先进的语言模型在许多任务上已经可以匹敌人类表现，但它们在稳健地执行多步数学推理方面仍然举步维艰。为了诊断当前模型的失败模式并支持相关研究，我们提出了 GSM8K，一个包含 8.5K 道高质量、语言多样的小学数学应用题的数据集。我们发现，即便这一问题分布的概念非常简单，最大的 transformer 模型也无法取得很高的测试表现。为提升性能，我们提出训练验证器（verifier）来判定模型补全的正确性。在测试时，我们生成大量候选解答，并选择验证器打分最高的那一个。我们证明验证能显著提升 GSM8K 上的表现，并提供了强有力的实验证据，表明与微调基线相比，验证随数据增加的扩展效果要好得多。

## 1 引言

近年来，大型语言模型在众多不同任务上展现了令人印象深刻的能力（Wang et al., 2019；Brown et al., 2020）。Kaplan et al. (2020) 描述了增大模型规模带来的一致收益，并刻画了在多个数量级上都成立的缩放趋势。然而，即使是最大的模型，在需要执行多步数学推理时也会失灵（Hendrycks et al., 2021）。模型样本经常包含灾难性错误，即使模型已经过适当微调也是如此。数学推理由此揭示了现代语言模型的一个关键弱点。

数学推理中的一个重大挑战是对个别错误的高度敏感性（Shen et al., 2021a）。在生成解答时，自回归模型没有纠正自身错误的机制。一旦解答偏离正轨，很快就会变得无法挽回。如果我们纯粹依赖生成式方法并根据当前趋势外推，那么要在 MATH 数据集（Hendrycks et al., 2021）这样具有挑战性的分布上取得哪怕中等的表现，都需要极其庞大的参数量。这一证据有力地推动了寻找具有更优缩放定律的方法。

我们提出训练验证器来评估模型生成解答的正确性，这与 Shen et al. (2021a) 的同期工作类似。在测试时，我们采样固定数量的候选解答，并选择验证器打分最高的解答。验证器的优势既来自其固有的可选择权（optionality），也来自「验证」通常比「生成」更简单这一事实。

为便利研究，我们发布 GSM8K，一个包含 8.5K 道小学数学水平高质量题目的数据集。我们在设计该数据集时追求高语言多样性，同时只依赖相对简单的小学数学概念。最先进的语言模型难以在该数据集上取得高表现，主要原因在于题目之间的高度多样性。与此同时，GSM8K 的解答只依赖初等概念，因此取得高测试表现是一个可企及的目标。

![Refer to caption](2110.14168v2/figures/example_problems.png)

图 1：GSM8K 的三道示例题目。计算标注以红色高亮显示。

我们的主要贡献如下：

1. 我们提供了一个经过精心整理的数据集，包含 8.5K 道小学数学问题和自然语言解答，可用于探测大型语言模型的非形式化推理能力。
2. 我们证明，与微调基线相比，使用验证器带来的性能提升约等于将模型规模扩大 30 倍，并且验证器随数据增加的扩展效果显著更好。
3. 我们证明 dropout 是一种强正则化手段，能显著提升微调和验证两者的表现。

## 2 数据集

GSM8K 由人类出题者创作的 8.5K 道高质量小学数学问题构成。我们将其划分为 7.5K 道训练问题和 1K 道测试问题。这些问题需要 2 到 8 步才能求解，解答主要涉及使用基本算术运算（$+-\times\div$）执行一系列初等计算以得到最终答案。一名聪明的中学生应当能解出每一道题。

我们基于以下设计原则创建 GSM8K。

- **高质量** 我们避免容易出错的抓取流程，转而依赖人类工作者来创作题目。在基于工作者答案一致性进行大量质量控制之后，我们估计只有不到 2% 的题目包含破坏性错误。
- **高多样性** 我们力求题目之间的高度多样性。我们主动避免设计与来自同一语言模板或仅在表面细节上有差异的题目，而这正是许多其他数据集中普遍存在的问题。通过让每道题目都相对独特，留出测试集上的表现就成为了一个相关性高得多的指标。
- **中等难度** 我们选择了一个对最先进的大型语言模型具有挑战性、但并非完全无法处理的问题分布。GSM8K 将帮助我们更好地理解不同模型和方法在这一难度甜点上的数据缩放趋势。问题不涉及超越初等代数（early Algebra）水平的概念，且绝大多数问题无需显式定义变量即可求解。
- **自然语言解答** 我们以自然语言而非纯数学表达式的形式收集解答。我们相信这是最通用的数据格式，并期望它能帮助我们理解大型语言模型内心独白的性质。我们要求出题者尽可能详细地解释其推理过程，但允许他们以自己多样的语言风格撰写解答。

完整的 GSM8K 数据集可在 <https://github.com/openai/grade-school-math> 获取。示例题目见图 1，更多数据集细节在附录 A 中讨论。

## 3 相关工作

### 3.1 相关数据集

早期的数学应用题数据集（Kushman et al., 2014；Roy and Roth, 2015）规模相对较小，不适合用来测试现代语言模型的极限。Dolphin18K（Huang et al., 2016）是包含 18K 道题目的更大数据集，但解答仅以等式或最终答案的形式给出。AQuA-RAT（Ling et al., 2017）包含 100K 道题目，但遗憾的是该数据集既存在严重的题目模板化问题，自然语言解答的质量控制也很差。MathQA 是最近发布的 AQuA-RAT 子集，专注于纠正这些错误（Amini et al., 2019），但即使经过修正的数据集仍存在数据质量问题，约 30% 的数据存在不一致（Miao et al., 2021）。Ape210K（Zhao et al., 2020）是最大的公开数据集，由 210K 道中文小学数学题组成。然而，由于语言障碍和缺乏自然语言解答，我们无法在该数据集上评估我们的方法。

近期开发的 ASDiv 数据集（Miao et al., 2021）包含 2.3K 道数学应用题，通过确保题目兼具高多样性和高质量，解决了先前数据集的常见缺陷。我们在创建 GSM8K 时遵循相同的设计原则。不过，我们注意到 GSM8K 规模更大、提供自然语言解答，且题目平均需要更多步骤才能求解。MATH 数据集（Hendrycks et al., 2021）比 GSM8K 更大也更复杂，但以当前最先进语言模型的能力而言，其高难度使得准确衡量进展变得困难。

其他近期与推理相关的数据集聚焦于符号数学上的数学推理（Lample and Charton, 2019）、阅读理解（LogiQA）（Liu et al., 2020）以及常识问答（CommonsenseQA）（Talmor et al., 2018）。与 CommonsenseQA 类似，GSM8K 包含需要基本背景知识的问题，例如一周有多少天。与需要结合阅读理解与逻辑推理的 LogiQA 类似，GSM8K 的主要难点既在于正确解读题目，也在于推理解题的各个步骤。

### 3.2 相关方法

先前的工作曾尝试用循环 seq2seq 模型（Sutskever et al., 2014）及其密切相关的变体（Wang et al., 2017；Huang et al., 2018）求解经典的数学应用题基准。更近期的工作通过设计专门的编码器-解码器架构来提升表现（Amini et al., 2019；Chiang and Chen, 2018；Xie and Sun, 2019；Chen et al., 2020；Li et al., 2020），其中最强的结果往往依赖 BERT 家族的大型预训练编码器（Chen et al., 2019；Kim et al., 2020；Liang et al., 2021）。

另一些近期工作推荐使用额外的预训练任务来进一步提升大型 transformer 模型的数学推理能力。Hendrycks et al. (2021) 提出在新的 AMPS 语料库上预训练模型，该语料库源自可汗学院（Khan Academy）题目和 Mathematica 脚本。类似地，Shen et al. (2021b) 提出在从互联网上提取的学前后到大学水平的课程语料上预训练，Peng et al. (2021) 提出通过预测表达式树中被遮蔽的子表达式来进行预训练。

与验证类似，另一些方法微调语言模型以在多个模型补全中进行选择。Nichols et al. (2020) 提出了一种「采样-排序」（sample-and-rank）方法来提升大型语言模型的协作讲故事能力，其训练信号来自人类工作者的偏好。在与我们工作密切相关的同期研究中，Shen et al. (2021a) 将类似方法应用于求解数学应用题，联合训练一个既生成又排序解答的模型。我们的工作与他们的方法在许多基本方面相似，但在几个关键方面有所不同。首先，我们将注意力集中在自然语言解答这一空间上，因为这是比纯数学表达式更丰富、更通用的解答格式。此外，这一选择使我们的模型能够发展出语言化的分析技能，并产出更易于被人类解读的解答。其次，我们提供了证据表明验证器随额外数据的扩展远比基线方法有利。最后，我们使用独立的生成器和验证器网络，以防止生成器过拟合。

## 4 方法

图 2：在不同规模训练集上微调后，各尺寸 GPT-3 模型的最终测试表现。图中显示 3 次运行的均值和标准差。

我们研究两种求解 GSM8K 问题的方法：微调和验证。微调是我们的基线方法，使用与 GPT-3 生成式预训练相同的语言建模目标（Brown et al., 2020）。在测试时，我们通过自回归地采样单个低温度解答并检查最终答案是否正确来评估表现。相比之下，验证的做法是采样多个高温度解答，为每个解答打分，并输出排名最高的解答。验证器被训练来判定解答的正确性，其训练信号仅由解答是否得到正确的最终答案决定。

对于这两种方法，我们都使用 GPT-3 家族的模型作为初始化，主要关注 175B 和 6B 两种模型尺寸。175B 模型最大、结果最令人印象深刻，而 6B 模型对研究目的而言要方便得多。我们在附录 B 中讨论超参数选择。

我们的模型经常无法准确执行计算。尽管较大的模型比较小的模型犯的算术错误更少，这仍是一个常见的错误来源。为缓解这一问题，我们通过向训练集注入计算标注来训练所有模型使用计算器。在测试时，当模型选择使用这些标注时，计算器将覆盖采样过程。细节见附录 C。

图 3：在完整 GSM8K 训练集上微调 6B 模型后的测试求解率，分别对应允许模型猜测 1 次（左）和 100 次（右）的情况。

### 4.1 微调

我们通过更新模型参数以最小化所有训练 token 上的交叉熵损失来执行微调。图 2 展示了在不同规模训练集上微调 20 个 epoch 后的测试表现。我们将同一数据分别作为训练集规模和模型规模的函数进行可视化。测试表现由每道测试题的单次低温（$T=0$）采样决定。不出所料，175B 模型显著优于较小的模型。假设呈对数线性趋势，我们可以朴素地外推这些结果，估计在使用完整 GSM8K 训练集的情况下，需要一个具有 $10^{16}$ 个参数的模型才能达到 80% 的求解率。沿数据维度外推则更加困难，因为表现似乎并不遵循对数线性趋势。尽管如此，175B 模型似乎仍需要至少再多两个数量级的训练数据才能达到 80% 的求解率。

在图 3 中，我们展示了 6B 模型测试表现在 100 个训练 epoch 中的变化情况。我们用 test@N 表示允许模型对每道题独立猜测 N 次时，至少有一次解对的问题所占的百分比。我们使用低温（$T=0$）生成 test@1 样本，使用更高的温度（$T=0.7$）生成 test@100 样本。两个温度值均经经验性选择以获得最佳结果。test@1 表现近似单调提升，尽管我们在测试损失上很快开始过拟合。遗憾的是，随着 epoch 数量增加，test@100 表现的退化比 test@1 严重得多。这是意料之中的：随着模型反复遇到相同的数据，它对其预测变得越来越未经校准且过度自信。在测试时，这种过度自信导致对解答空间的覆盖不佳，而这一效应只有在我们在测试时考虑多个样本时才会显现。

选择一个覆盖良好的模型对于成功训练验证器至关重要。凭经验看，test@100 表现在前几个 epoch 内就达到峰值。因此，我们使用训练了 2 个 epoch 的模型来生成训练验证器所需的样本。我们在附录 D 中提供了 6B 和 175B 模型的若干示例解答。我们还注意到，让模型在输出最终答案之前生成完整的自然语言解答非常重要。如果我们转而微调 6B 模型直接输出最终答案而没有任何中间步骤，表现会从 20.6% 骤降至 5.2%。

图 4：验证训练流程示意图。

![Refer to caption](2110.14168v2/figures/verifier_diagram.png)

### 4.2 验证

为了在微调基线之上进一步提升，我们训练验证器来判定模型生成解答的正确性，并在测试时基于这些验证器进行搜索。以问题和候选解答为条件，验证器输出该解答正确的概率。训练解答仅依据其是否得到正确的最终答案被标记为正确或不正确。实践中，一些解答会通过有缺陷的推理得到正确的最终答案，从而导致假阳性。

如图 4 所示，我们按如下方式训练验证器：

1. 在训练集上微调一个模型（「生成器」）2 个 epoch。
2. 为每道训练题从生成器采样 100 个补全，并将每个解答标记为正确或不正确。
3. 在该数据集上训练验证器 1 个 epoch。

训练 2 个 epoch 足以让生成器学会该领域的基本技能。我们选择不训练更久，因为生成解答的多样性在此之后开始崩塌，如图 3 所示。我们训练独立的生成器和验证器模型，以限制生成器的训练并防止过拟合，但原则上应当可以合并这些模型。除非另有说明，我们对生成器和验证器使用相同的模型尺寸。除了预测解答正确性之外，我们还用与生成器相同的语言建模目标训练验证器。这对验证器而言是一个有价值的辅助目标。我们在附录 E 中讨论验证器训练的更多细节。

图 5：6B 和 175B 模型尺寸下微调与验证的对比。验证对每道题考虑 100 个解答。图中显示 3 次运行的均值和标准差，175B 验证除外，其仅显示单次运行。

在测试时，我们对每道测试题采样 100 个补全，用验证器对其排序，然后返回验证器得分最高的那一个。图 5 展示了 6B 和 175B 两种模型尺寸下验证与微调的对比。我们发现，在数据集规模较小时使用验证并无益处。我们认为这是由于过拟合正确答案的压力：在小数据集上，对正确答案的过拟合比学习正确推理的更泛化性质发生得更快。然而，一旦使用足够大的数据集，验证器就会带来强劲的提升。有趣的是，175B 验证器比 6B 验证器更早「起飞」，只需要更少的训练题就能超越微调基线。验证器找到的解答示例见附录 D，验证器置信度的可视化见附录 F。

(a) 比较在每个 token 后预测正确性（token 级）训练的验证器与仅在最后一个 token 后预测正确性（解答级）训练的验证器

(b) 比较联合训练以预测正确性和执行语言建模（联合）的验证器与仅训练预测正确性（仅验证）的验证器

(c) 单独改变生成器和验证器尺寸时的表现。增大生成器尺寸的影响大于增大验证器尺寸。

图 6：验证消融实验

### 4.3 验证消融实验

我们可以训练验证器在以整个生成的解答为条件下做出单个标量预测，或者在解答中的每个 token 之后做出标量预测。默认情况下，我们选择后者，训练验证器在每个 token 之后做出预测。这可以看作一种 token 级价值函数（value function）。我们在图 6(a) 中比较这两种方法，分别标记为「解答级」（solution-level）和「token 级」（token-level）。

在每个 token 处预测价值函数是比仅评判完整补全更困难、更嘈杂的任务。然而，尽管训练初期较慢，token 级验证器最终优于解答级验证器。此外，token 级验证器在训练后期仍在继续提升，而解答级验证器则很快显现过拟合迹象。我们假设完整的价值函数提供了一种有用的辅助信号，促使模型评判解答全程中的推理，而不是仅仅记住正确的最终答案。

在图 6(b) 中，我们消融训练验证器时使用的目标。如 4.2 节所述，我们可以在验证目标之外选择性地加入语言建模目标。我们比较同时使用两个目标与仅使用验证目标。尽管两者都是合理的选择，但加入语言建模目标是严格的改进。这符合直觉：更好地理解这一语言分布只应有助于验证器区分样本。

在图 6(c) 中，我们分别消融生成器和验证器的模型尺寸。我们发现，使用大生成器配小验证器的表现显著优于使用小生成器配大验证器。即使验证器远小于生成器，验证仍然非常有效。这表明验证器在区分来自某个生成器的解答时，可能往往依赖相对粗粒度的启发式，而非尝试更彻底的验证形式。

(a) 6B 验证在每道题给定不同数量的待排序补全时的测试表现。

(b) 6B 验证在允许不同数量的排名靠前样本对答案投票时的测试表现。

图 7：测试时计算量变化时的表现。

## 5 附加实验

### 5.1 测试时计算

在测试时，我们可以选择生成任意多的解答交由验证器评判，再选出排名最高的补全。图 7(a) 展示了 6B 验证器的表现如何随每道测试题的补全数量变化。在这一规模下，表现随着补全数量增加到 400 而提升。超过这一点后，表现开始下降。这表明搜索的收益最终会被找到能欺骗验证器的对抗性解答的风险所抵消。总体而言，我们使用 100 个补全来评估验证器的测试表现，因为这能以相对适中的计算成本捕获验证的大部分收益。

为进一步提升表现，我们可以在验证器排名最高的解答中取多数票，而不是只选择排名最高的单个解答。这一投票过程只考虑各解答所得到的最终答案：被选中的最终答案是得票最多的那个。图 7(b) 展示了当允许更多排名靠前的样本投票时表现如何变化。不出所料，当初始样本更多时，我们可以承受允许更多样本投票。当我们只有 100 个样本时，仅允许排名前 3-5 的样本投票是最优的。当我们有 3200 个样本时，允许排名前 30 的样本投票近似最优。

### 5.2 正则化

(a) 微调

(b) 解答级验证器

(c) token 级验证器

图 8：6B 微调与验证的 dropout 消融实验。

我们发现，微调和验证都强烈受益于将 dropout 用作正则化器。具体来说，我们在网络每一层的残差路径上应用残差 dropout（Vaswani et al., 2017）。所有 dropout 实验均使用 20% 的 dropout，该值基于一次超参数扫描的结果选出。我们注意到 GPT-3 模型在预训练时并未使用 dropout。因此，对于涉及 dropout 的实验，我们先带 dropout 进行额外的预训练，随后再微调模型。这缓解了模型在微调期间经历的分布偏移。

我们首先研究 dropout 在各种训练集规模下对微调的影响。图 8(a) 表明 dropout 相比基线带来了显著提升。接下来我们研究 dropout 对验证器的影响，同时考虑解答级和 token 级两种变体。在图 8(b) 中，我们看到 dropout 显著提升了解答级验证器的表现，缓解了无正则化基线中出现的过拟合。值得注意的是，在解答级验证器上使用 dropout 可以达到与 token 级验证器相近的表现水平。在图 8(c) 中，我们将 dropout 应用于 token 级验证器。由于 token 级验证器本身就不太容易过拟合，dropout 的影响不那么显著也就不足为奇了。不过，带 dropout 训练 token 级验证器仍然带来少许收益。注意，我们将 token 级验证器的批大小增大了 4 倍，以更好地应对更困难的目标和 dropout 带来的噪声。

## 6 结论

我们已经看到，相对于微调基线，验证带来了显著的性能提升。在完整数据集上，6B 验证略优于微调后的 175B 模型，从而提供了约等于模型规模扩大 30 倍的提升。我们还看到 token 级验证器比解答级验证器更不容易过拟合，并且所有方法都受益于残差 dropout 正则化。我们预期验证能很好地扩展到需要更复杂数学推理的问题分布，并希望 GSM8K 能支持发展出扩展性更好的新方法。

## 致谢

我们感谢 Dan Hendrycks、Leo Gao、Alec Radford 和 Giambattista Parascandolo 对本文的宝贵反馈；感谢 Harri Edwards、Yura Burda、Michael Wu 和 Nick Ryder 的许多富有洞见的讨论；感谢 Michael Petrov、Alethea Power 和 Jacob Jackson 的技术协助；感谢 OpenAI 超级计算团队提供了使这些实验成为可能的基础设施；并感谢 Surge AI 团队执行 GSM8K 的数据收集。

## 参考文献

- Amini et al. (2019)

  A. Amini, S. Gabriel, P. Lin, R. Koncel-Kedziorski, Y. Choi, and H. Hajishirzi.
  Mathqa: Towards interpretable math word problem solving with
  operation-based formalisms.
  *arXiv preprint arXiv:1905.13319*, 2019.
- Brown et al. (2020)

  T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal,
  A. Neelakantan, P. Shyam, G. Sastry, A. Askell, et al.
  Language models are few-shot learners.
  *arXiv preprint arXiv:2005.14165*, 2020.
- Chen et al. (2020)

  K. Chen, Q. Huang, H. Palangi, P. Smolensky, K. D. Forbus, and J. Gao.
  Mapping natural-language problems to formal-language solutions using
  structured neural representations.
  In *ICML*, 2020.
- Chen et al. (2019)

  X. Chen, C. Liang, A. W. Yu, D. Zhou, D. Song, and Q. V. Le.
  Neural symbolic reader: Scalable integration of distributed and
  symbolic representations for reading comprehension.
  In *International Conference on Learning Representations*, 2019.
- Chiang and Chen (2018)

  T.-R. Chiang and Y.-N. Chen.
  Semantically-aligned equation generation for solving and reasoning
  math word problems.
  *arXiv preprint arXiv:1811.00720*, 2018.
- Hendrycks et al. (2021)

  D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and
  J. Steinhardt.
  Measuring mathematical problem solving with the math dataset.
  *arXiv preprint arXiv:2103.03874*, 2021.
- Huang et al. (2016)

  D. Huang, S. Shi, C.-Y. Lin, J. Yin, and W.-Y. Ma.
  How well do computers solve math word problems? large-scale dataset
  construction and evaluation.
  In *Proceedings of the 54th Annual Meeting of the Association
  for Computational Linguistics (Volume 1: Long Papers)*, pages 887–896, 2016.
- Huang et al. (2018)

  D. Huang, J. Liu, C.-Y. Lin, and J. Yin.
  Neural math word problem solver with reinforcement learning.
  In *Proceedings of the 27th International Conference on
  Computational Linguistics*, pages 213–223, 2018.
- Kaplan et al. (2020)

  J. Kaplan, S. McCandlish, T. Henighan, T. B. Brown, B. Chess, R. Child,
  S. Gray, A. Radford, J. Wu, and D. Amodei.
  Scaling laws for neural language models.
  *arXiv preprint arXiv:2001.08361*, 2020.
- Kim et al. (2020)

  B. Kim, K. S. Ki, D. Lee, and G. Gweon.
  Point to the expression: Solving algebraic word problems using the
  expression-pointer transformer model.
  In *Proceedings of the 2020 Conference on Empirical Methods in
  Natural Language Processing (EMNLP)*, pages 3768–3779, 2020.
- Kushman et al. (2014)

  N. Kushman, Y. Artzi, L. Zettlemoyer, and R. Barzilay.
  Learning to automatically solve algebra word problems.
  In *Proceedings of the 52nd Annual Meeting of the Association
  for Computational Linguistics (Volume 1: Long Papers)*, pages 271–281, 2014.
- Lample and Charton (2019)

  G. Lample and F. Charton.
  Deep learning for symbolic mathematics.
  *arXiv preprint arXiv:1912.01412*, 2019.
- Li et al. (2020)

  S. Li, L. Wu, S. Feng, F. Xu, F. Xu, and S. Zhong.
  Graph-to-tree neural networks for learning structured input-output
  translation with applications to semantic parsing and math word problem.
  *EMNLP*, 2020.
- Liang et al. (2021)

  Z. Liang, J. Zhang, J. Shao, and X. Zhang.
  Mwp-bert: A strong baseline for math word problems, 07 2021.
- Ling et al. (2017)

  W. Ling, D. Yogatama, C. Dyer, and P. Blunsom.
  Program induction by rationale generation: Learning to solve and
  explain algebraic word problems.
  *arXiv preprint arXiv:1705.04146*, 2017.
- Liu et al. (2020)

  J. Liu, L. Cui, H. Liu, D. Huang, Y. Wang, and Y. Zhang.
  Logiqa: A challenge dataset for machine reading comprehension with
  logical reasoning.
  In *IJCAI*, 2020.
- Miao et al. (2021)

  S.-Y. Miao, C.-C. Liang, and K.-Y. Su.
  A diverse corpus for evaluating and developing english math word
  problem solvers.
  *arXiv preprint arXiv:2106.15772*, 2021.
- Nichols et al. (2020)

  E. Nichols, L. Gao, and R. Gomez.
  Collaborative storytelling with large-scale neural language models.
  *arXiv preprint arXiv:2011.10208*, 2020.
- Peng et al. (2021)

  S. Peng, K. Yuan, L. Gao, and Z. Tang.
  Mathbert: A pre-trained model for mathematical formula understanding.
  *ArXiv*, abs/2105.00377, 2021.
- Roy and Roth (2015)

  S. Roy and D. Roth.
  Solving general arithmetic word problems.
  In *Proceedings of the 2015 Conference on Empirical Methods in
  Natural Language Processing*, pages 1743–1752, Lisbon, Portugal, Sept. 2015.
  Association for Computational Linguistics.
  doi: 10.18653/v1/D15-1202.
  URL <https://aclanthology.org/D15-1202>.
- Shen et al. (2021a)

  J. Shen, Y. Yin, L. Li, L. Shang, X. Jiang, M. Zhang, and Q. Liu.
  Generate & rank: A multi-task framework for math word problems.
  *arXiv preprint arXiv:2109.03034*, 2021a.
- Shen et al. (2021b)

  J. T. Shen, M. Yamashita, E. Prihar, N. Heffernan, X. Wu, B. Graff, and D. Lee.
  Mathbert: A pre-trained language model for general nlp tasks in
  mathematics education, 08 2021b.
- Sutskever et al. (2014)

  I. Sutskever, O. Vinyals, and Q. V. Le.
  Sequence to sequence learning with neural networks.
  In *Advances in neural information processing systems*, pages
  3104–3112, 2014.
- Talmor et al. (2018)

  A. Talmor, J. Herzig, N. Lourie, and J. Berant.
  Commonsenseqa: A question answering challenge targeting commonsense
  knowledge.
  *arXiv preprint arXiv:1811.00937*, 2018.
- Vaswani et al. (2017)

  A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez,
  Ł. Kaiser, and I. Polosukhin.
  Attention is all you need.
  In *Advances in neural information processing systems*, pages
  5998–6008, 2017.
- Wang et al. (2019)

  A. Wang, Y. Pruksachatkun, N. Nangia, A. Singh, J. Michael, F. Hill, O. Levy,
  and S. R. Bowman.
  Superglue: A stickier benchmark for general-purpose language
  understanding systems.
  *arXiv preprint arXiv:1905.00537*, 2019.
- Wang et al. (2017)

  Y. Wang, X. Liu, and S. Shi.
  Deep neural solver for math word problems.
  In *Proceedings of the 2017 Conference on Empirical Methods in
  Natural Language Processing*, pages 845–854, Copenhagen, Denmark, Sept.
  2017. Association for Computational Linguistics.
  doi: 10.18653/v1/D17-1088.
  URL <https://aclanthology.org/D17-1088>.
- Xie and Sun (2019)

  Z. Xie and S. Sun.
  A goal-driven tree-structured neural model for math word problems.
  In *IJCAI*, 2019.
- Zhao et al. (2020)

  W. Zhao, M. Shang, Y. Liu, L. Wang, and J. Liu.
  Ape210k: A large-scale and template-rich dataset of math word
  problems.
  *arXiv preprint arXiv:2009.11506*, 2020.

## 附录 A 数据集细节

我们最初通过在 Upwork（[upwork.com](https://upwork.com)）雇佣自由职业承包者收集了一千道问题及自然语言解答的起始集合。随后我们与 Surge AI（[surgehq.ai](https://surgehq.ai)，一家 NLP 数据标注平台）合作，扩大了数据收集规模。收集完整数据集后，我们要求工作者重新求解所有问题，且没有工作者重复求解自己最初出过的题。我们检查他们的最终答案是否与原始解答一致，任何产生分歧的问题要么被修复，要么被丢弃。然后我们在一个较小的问题子集上进行了另一轮一致性检查，发现仍有 1.7% 的问题在承包者之间产生分歧。我们估计这就是包含破坏性错误或歧义的问题比例。包含细微错误的问题比例可能更高。

为协助承包者出题，我们提供了由少样本提示的 175B GPT-3 模型自动生成的种子问题。承包者可以直接使用这些种子问题，可以将其作为灵感并加以修改，也可以完全自行构思问题。我们指示承包者在解答中尽可能详尽地描述，并且不要在不同问题之间复用问题背景或模板。为确保承包者没有复用问题模板，我们计算了问题之间的两两相似度分数，并用它向承包者提供反馈。

## 附录 B 超参数

我们在下面给出重要超参数表。我们对学习率和批大小在表中数值的双向各一个数量级范围内进行了扫描，未能找到任何显著改进。对验证器温度（例如用 1.0 代替 0.7）和目标函数（用交叉熵代替均方误差）的其他合理选择在我们的消融实验中影响也可忽略不计。

|  |  |
| --- | --- |
| 通用超参数 | 取值 |
| 批大小 | $3.2\times 10^{4}$ tokens |
| 最大样本长度 | 400 tokens |
| 分词 | reversible_50000 |
| 优化器 | Adam，$\beta_{1}=0.9$，$\beta_{2}=0.95$ |
| Dropout | $0.0$ |
| 学习率调度 | 线性衰减至 0 |
| 微调超参数 | 取值 |
| Epoch 数 | 20 |
| 采样温度 | 0（argmax） |
| 基础学习率（$\alpha$） | $1.6\times 10^{-5}$（3B） |
|  | $1.2\times 10^{-5}$（6B） |
|  | $1.0\times 10^{-5}$（12B） |
|  | $6.0\times 10^{-6}$（175B） |
| 学习率 | $0.1\times\alpha$ |
| 验证超参数 | 取值 |
| Epoch 数 | 生成器 2，验证器 1 |
| 采样温度 | $0.7$ |
| 学习率 | $1.0\times 10^{-5}$ |
| 损失权重 | $1.0$ |
| 验证器损失 | MSE |
| 每道训练题的补全数 | 100 |
| 每道测试题的补全数 | 100 |

表 1：除非明确说明，所有实验使用的超参数。值得注意的例外包括图 8(c)，其每批使用多 4 倍的 token，并在训练和测试时均使用 300 个补全。图 8 中的所有 dropout 实验均使用 20% 的 dropout。图 7(a) 使用在 100 个补全上训练的验证器，但在测试时搜索更多补全。

## 附录 C 计算器标注

计算器标注并非由人类承包者提供：它们由硬编码逻辑和微调过的语言模型组合生成。自动生成计算器标注的逻辑并不完美。它极不可能生成错误的标注，但漏掉一些本可标注的行并不罕见。

在训练期间，被标注的 token 与解答的其余部分之间没有特殊区别：它们都只是 token。在测试期间，当存在格式正确的标注时，我们覆盖模型采样，具体而言是覆写紧跟在「=」之后以及位于 <<…>> 之内的 token。

为模拟计算器，我们直接使用 python 的 eval 函数来计算表达式中的 token（图 9）。超时或抛出错误的求值会导致跳过相应标注，并照常从模型采样。

我们注意到，本文所有结果所用的计算器原始版本存在一些小的实现 bug。因此我们报告的测试表现略有低估，不过在大多数实验中这一差异小于 1%。修复计算器后，在使用完整 GSM8K 训练集时，验证测试表现提升约 1%。

图 9：计算器采样流程示意图。

## 附录 D 模型解答示例

我们展示了少量对比 6B 和 175B 规模下微调与验证的样本。样本为多样性做了少许挑选。

![[Uncaptioned image]](2110.14168v2/figures/example_solutions_1.png)

![[Uncaptioned image]](2110.14168v2/figures/example_solutions_3.png)

![[Uncaptioned image]](2110.14168v2/figures/example_solutions_2.png)

![[Uncaptioned image]](2110.14168v2/figures/example_solutions_4.png)

![[Uncaptioned image]](2110.14168v2/figures/example_solutions_5.png)

![[Uncaptioned image]](2110.14168v2/figures/example_solutions_8.png)

![[Uncaptioned image]](2110.14168v2/figures/example_solutions_7.png)

![[Uncaptioned image]](2110.14168v2/figures/example_solutions_6.png)

## 附录 E 验证器细节

如 4.2 节所述，我们用联合目标训练验证器，模型在原有语言建模目标之外，还学习将模型补全标记为正确或不正确。在架构上，这意味着我们的验证器就是语言模型，外加一个在每个 token 上输出预测的小型标量头。

我们将该标量头实现为单个偏置参数和单个增益参数，作用于语言模型最后解嵌入层输出的 logits。具体而言，偏置和增益对词表中一个特殊 token 对应的 logit 进行平移和缩放。如此一来，其他 token 的 logits 可以继续表示语言建模目标，而这个特殊 token 则保留给验证器的预测。

我们可以选择从生成器微调所用的同一个预训练语言模型初始化验证器，或者从生成器本身初始化。在我们的消融实验中后者表现略好；我们怀疑这是因为更好地理解生成器学到的语言分布只应有助于验证器为来自该分布的样本打分。除非明确说明，我们在所有实验中都从对应的生成器初始化验证器。

用联合目标训练验证器时，我们使用语言数据与验证器数据的等量混合。由于我们为每个原始训练样本采样 100 个补全来生成验证器数据，使用等量混合意味着我们实际上将原始语言数据上采样了 100 倍。为构成联合目标，我们直接将验证器损失与语言建模损失无权重相加，并将该联合目标的一个 epoch 定义为每个验证器样本被看到一次。对于两个目标，我们都会遮蔽问题中的 token，只在解答中的 token 上训练，如图 12 所示。

图 12：联合训练目标的可视化。我们遮蔽问题中的 token，只考虑解答中 token 对应的损失。

## 附录 F 验证器可视化

![Refer to caption](2110.14168v2/vf_viz_cherrypicked.png)

图 13：由 175B 微调模型生成、并由 175B token 级验证器打分的五个精挑细选样本。绿色背景表示验证器得分高，红色背景表示验证器得分低。

token 级验证器的一个好处是这类模型即刻变得可解释：我们可以将每个 token 的预测值可视化，从而更好地理解验证器如何对样本做出评判。上面我们展示了五个精挑细选的问题和模型补全的预测值可视化，打分者是在完整训练集上训练的 175B token 级验证器。

在可视化中，文本的背景颜色对应该 token 的验证器得分，红色为低值（预测为不正确），绿色为高值（预测为正确）。表格第二列概述验证器的预测，第三列指示生成的模型补全实际上是正确还是不正确。第二列与第三列之间的任何分歧都表明验证器犯了错误。

第一行是一个真阳性示例，验证器正确地将补全判定为正确。注意，模型最初不确定解答是否正确，随着解答推进逐渐获得确定性：这很可能是验证器训练流程的一个性质，因为其训练数据中有很大比例是不正确的模型生成样本。

第二行包含一个解答正确、但验证器将其评为不正确的问题。这可能源于问题描述中「4 times」与「4 potatoes」之间的歧义。

第三行是另一个假阴性示例。然而，与上一个示例不同的是，这里的模型补全包含一些错误推理。因此，尽管模型补全中的最终答案是正确的，其自然语言解释是错误的，所以验证器正确地给出了低分。

在第四行中，我们看到验证器为一个开头正确、但随着解答推进验证器逐渐失去信心的模型补全打分。在解答犯下一个明显错误之后（说花了 $\$64$，而不是 $64+16+8=\$88$），验证器以很高的置信度判定该解答不正确。

最后一行包含一个假阳性，模型在第二步犯了错，从钻石首饰而非黄金首饰的价格中减去了 400。验证器偶尔会在将数量与其关系进行变量绑定时犯错。
