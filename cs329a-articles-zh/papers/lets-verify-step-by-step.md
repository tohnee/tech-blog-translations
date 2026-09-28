---
title: "让我们逐步验证"
title_en: "Let's Verify Step by Step"
arxiv: 2305.20050
source: https://arxiv.org/abs/2305.20050
crawled: 2026-09-23
translated: 2026-09-23
---

# 让我们逐步验证

> 原文：[Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) · Stanford CS329A 指定阅读

Hunter Lightman、Vineet Kosaraju、Yura Burda、Harri Edwards、Bowen Baker、Teddy Lee、Jan Leike、John Schulman、Ilya Sutskever、Karl Cobbe

注：前三位作者为主要作者（primary authors）。通讯作者：Karl Cobbe <karl@openai.com>
所属机构：OpenAI

###### 摘要

近年来，大型语言模型执行复杂多步推理的能力已大幅提升。然而，即使是最先进的模型也仍会经常性地犯逻辑错误。要训练更可靠的模型，我们可以求助于结果监督（outcome supervision，针对最终结果提供反馈）或过程监督（process supervision，针对每个中间推理步骤提供反馈）。鉴于训练可靠模型的重要性，以及人类反馈的高昂成本，仔细比较这两种方法十分重要。近期工作已经开始这种比较，但许多问题仍悬而未决。我们开展了自己的调查，发现对于训练模型求解具有挑战性的 MATH 数据集中的问题，过程监督显著优于结果监督。我们的过程监督模型求解了 MATH 测试集一个代表性子集中 78% 的问题。此外，我们证明主动学习能显著提升过程监督的效能。为支持相关研究，我们还发布了 PRM800K，这是用于训练我们最佳奖励模型的 80 万个步级人类反馈标签的完整数据集。

## 1 引言

大型语言模型能够以逐步的思维链（chain-of-thought）格式生成解答，从而求解需要复杂多步推理的任务（Nye et al., 2021；Wei et al., 2022；Kojima et al., 2022）。然而，即使是最先进的模型也容易产生虚假内容——它们在不确定的时刻表现出捏造事实的倾向（Bubeck et al., 2023）。这些幻觉（Maynez et al., 2020）在需要多步推理的领域中尤其成问题，因为单个逻辑错误就足以使一个更大的解答脱轨。检测并缓解幻觉对提升推理能力至关重要。

一种有效的方法是训练奖励模型来区分合意与不合意的输出。奖励模型随后可用于强化学习流水线（Ziegler et al., 2019；Stiennon et al., 2020；Nakano et al., 2021；Ouyang et al., 2022），或通过拒绝采样执行搜索（Nichols et al., 2020；Shen et al., 2021；Cobbe et al., 2021）。这些技术虽然有用，但所得系统的可靠性仅取决于奖励模型本身。因此，研究如何最有效地训练可靠的奖励模型十分重要。

在密切相关的工作中，Uesato et al. (2022) 描述了训练奖励模型的两种不同方法：结果监督与过程监督。结果监督奖励模型（ORM）仅使用模型思维链的最终结果进行训练，而过程监督奖励模型（PRM）则对思维链中的每一步获得反馈。有若干令人信服的理由倾向于过程监督。它提供更精确的反馈，因为它指明了所发生的任何错误的确切位置。它还有若干与 AI 对齐相关的优势：它更易于人类解读，并且它更直接地奖励模型遵循一条人类认可的思维链。在逻辑推理领域内，用结果监督训练的模型经常使用错误的推理来得到正确的最终答案（Zelikman et al., 2022；Creswell et al., 2022）。已有研究表明过程监督能缓解这种失配行为（Uesato et al., 2022）。

尽管有这些优势，Uesato et al. (2022) 发现在小学数学领域，结果监督与过程监督带来了相近的最终表现。我们对结果监督与过程监督进行了自己的细致比较，与他们的工作有三点主要不同：我们使用了能力更强的基础模型，我们使用了显著更多的人类反馈，并且我们在更具挑战性的 MATH 数据集（Hendrycks et al., 2021）上训练和测试。

我们的主要贡献如下：

1. 我们证明过程监督可以训练出比结果监督可靠得多的奖励模型。我们使用最先进的 PRM 求解了 MATH 测试集一个代表性子集中 78.2% 的问题。
2. 我们证明大型奖励模型可以为较小的奖励模型可靠地近似人类监督，并且它可以用于高效地开展大规模数据收集消融实验。
3. 我们证明主动学习使过程监督的数据效率提升了 $2.6\times$。
4. 我们发布了完整的过程监督数据集 PRM800K，以促进相关研究。

## 2 方法

我们比较结果监督与过程监督，方法论上与 Uesato et al. (2022) 类似。结果监督可以无需人类参与即可提供，因为 MATH 数据集中的所有问题都有可自动检查的答案。相比之下，没有简单的方法可以自动化过程监督。因此，我们依赖人类数据标注者提供过程监督，具体做法是为模型生成解答中的每一步标注正确性。

我们在两种不同设定下开展实验：大规模和小规模。两者各有优势，并提供互补的视角。在大规模设定下，我们从 GPT-4（OpenAI, 2023）微调所有模型。我们专注于通过尽可能训练最可靠的 ORM 和 PRM 来推进最先进水平。遗憾的是，这些奖励模型的训练集无法直接比较，原因将在第 3 节讨论。因此，这些模型并不适合对结果监督与过程监督进行 apples-to-apples 的直接比较。为弥补这一缺陷，我们还在小规模设定下训练模型，在那里可以进行更直接的比较。为了摆脱对昂贵人类反馈的依赖，我们使用大规模模型来监督小规模模型的训练。这一设置使我们能够开展若干否则不可行的重要消融实验。

### 2.1 范围

在每个模型规模上，我们都使用一个固定的模型来生成所有解答。我们称该模型为生成器（generator）。我们不尝试用强化学习（RL）改进生成器。当我们讨论结果监督与过程监督时，特指提供给奖励模型的监督。我们不讨论生成器若用 RL 训练将从奖励模型获得的任何监督。尽管用 RL 微调生成器是自然的下一步，但它有意地不是本工作的焦点。

我们转而专注于如何训练尽可能可靠的奖励模型。我们通过奖励模型对来自生成器的均匀采样解答执行 best-of-N 搜索的能力来评估它。对每道测试题，我们选出奖励模型排名最高的解答，根据其最终答案自动评分，并报告其中正确的比例。更可靠的奖励模型会更频繁地选出正确解答。

### 2.2 基础模型

所有大规模模型都从 GPT-4 基础模型（OpenAI, 2023）微调而来。该模型仅被预训练用于预测下一个 token；它没有经过任何基于人类反馈的强化学习（RLHF）预训练（Christiano et al., 2017）。小规模基础模型在设计上与 GPT-4 类似，但预训练所用的计算量大约少 200 倍。作为额外的预训练步骤，我们在一个约含 1.5B 个数学相关 token 的数据集上微调所有模型，我们称之为 MathMix。与 Lewkowycz et al. (2022) 类似，我们发现这提升了模型的数学推理能力。该数据集的构建细节见附录 A。

### 2.3 生成器

为使解析单个步骤更加容易，我们训练生成器以换行分隔的逐步格式生成解答。具体而言，我们少样本生成 MATH 训练题的解答，筛选出得到正确最终答案的那些，并在该数据集上微调基础模型 1 个 epoch。这一步并非要教给生成器新技能；它只是要教生成器以期望的格式生成解答。

图 1：用于为解答中每一步收集反馈的界面截图。

![Refer to caption](2305.20050v1/figures/data_interface_simple.png)

### 2.4 数据收集

为收集过程监督数据，我们向人类数据标注者展示由大规模生成器采样的 MATH 问题逐步解答。他们的任务是为解答中的每一步赋予正面、负面或中性标签，如图 1 所示。正面标签表示该步骤正确且合理。负面标签表示该步骤不正确或不合理。中性标签表示存在歧义。实践中，如果某一步带有微妙的误导性，或者它是一个技术上仍然有效的糟糕建议，则可能被标注为中性。我们允许中性标签，因为这使我们能推迟决定如何处理歧义：在测试时，我们可以将中性标签视为正面或负面。标注指南的更详细描述见附录 D。

我们仅从大规模生成器标注解答，以最大化有限人类数据资源的价值。我们将收集到的整个步级标签数据集称为 PRM800K。PRM800K 训练集包含跨 12K 道题目的 75K 个解答的 800K 个步级标签。为最小化过拟合，我们将 4.5K 道 MATH 测试题的数据纳入 PRM800K 训练集，因此我们只在其余 500 道 MATH 测试题上评估模型。关于该测试集的更多细节见附录 C。

在数据收集过程中，我们必须决定向数据标注者呈现哪些解答。最直接的策略是均匀呈现生成器产生的解答。然而，如果我们呈现的解答犯有显而易见的错误，我们获得的人类反馈价值就会降低。我们更愿意呈现更有可能欺骗我们最佳奖励模型的解答。为此，我们尝试策略性地选择向数据标注者展示哪些解答。具体而言，我们选择呈现「有说服力的错误答案」（convincing wrong-answer）解答。我们用「有说服力的」指被我们当前最佳 PRM 评为高分的解答，用「错误答案的」指得到错误最终答案的解答。我们使用这一略显冗长的措辞是为了强调：正确性仅通过检查最终答案来判定，而这一过程偶尔会导致解答被误判。我们预期从标注「有说服力的错误答案」解答中获得更多信息，因为我们知道 PRM 在每个此类解答中至少在某一步上出了错。

除了使用这一选择策略外，我们还在数据收集过程的多个时间点上用最新数据迭代重训我们的 PRM。每次迭代中，我们为每道题生成 N 个解答，并只向数据标注者呈现排名前 K 的最有说服力的错误答案解答。我们尝试了在问题级别施加这一 top-K 过滤（每道题 K 个解答），或在数据集全局施加（总共 K 个解答，在题目间不均匀分布）。由于数据收集过程昂贵，无法对这些决策开展规模化消融。不过，我们在第 4 节中使用我们最大的 PRM 作为较小 PRM 的标注 oracle，进行了若干替代性消融实验。数据收集的更多细节见附录 B。

![Refer to caption](2305.20050v1/figures/prm_true_positive.png)

![Refer to caption](2305.20050v1/figures/prm_true_negative.png)

图 2：同一问题的两个解答，由 PRM 打分。左侧解答正确，右侧解答不正确。绿色背景表示 PRM 得分高，红色背景表示得分低。PRM 正确识别出不正确解答中的错误。

### 2.5 结果监督奖励模型（ORM）

我们按照与 Cobbe et al. (2021) 类似的方法论训练 ORM。我们从生成器为每道题均匀采样固定数量的解答，并训练 ORM 预测每个解答正确与否。实践中，我们通常通过自动检查最终答案来确定正确性，但原则上这些标签也可以由人类提供。在测试时，我们使用 ORM 在最后一个 token 处的预测作为该解答的总分。我们注意到，用于确定 ORM 训练目标的自动评分并不完全可靠：用错误推理得到正确答案的假阳性解答会被误判。我们在附录 E 中讨论更多 ORM 训练细节。

### 2.6 过程监督奖励模型（PRM）

我们训练 PRM 在每一步的最后一个 token 之后预测该步的正确性。该预测以单个 token 的形式给出，我们在训练期间最大化这些目标 token 的对数似然。因此，PRM 可以在标准的语言模型流水线中训练，无需任何特殊适配。在测试时，只需对整个解答执行一次 PRM 前向传播即可得到步级预测。我们在图 2 中可视化了两个不同解答的大规模 PRM 得分。要比较多个解答，就需要为每个解答计算一个总分。这是一个重要但直接的细节：我们将一个解答的 PRM 得分定义为在该 PRM 下每一步都正确的概率。我们将其实现为每一步正确概率的乘积。其他可能的打分策略以及更多 PRM 训练细节在附录 F 中描述。

在提供过程监督时，我们刻意选择只监督到第一个不正确的步骤为止。这使得结果监督与过程监督的比较更加直接。对于正确解答，两种方法提供相同的信息，即每一步都正确。对于错误解答，两种方法都揭示至少存在一个错误，而过程监督还额外揭示该错误的确切位置。如果我们提供超出第一个错误之外的更多过程监督，那么过程监督的信息优势会更大。这一决定也使人类的标注成本大致持平：在不能依赖易于检查的最终答案的情况下，判定一个解答的正确性等价于找出它的第一个错误。虽然大多数 MATH 问题的最终答案易于检查，我们预期在更复杂的领域中这一点将不再成立。

## 3 大规模监督

我们使用 PRM800K 中的步级标签训练大规模 PRM。为确保大规模 ORM 基线尽可能强，我们在来自生成器的每道题 100 个均匀样本上训练。这意味着 ORM 训练集与 PRM800K 没有重叠，且大一个数量级。尽管这两个训练集无法直接比较，但每一个都代表了我们用相应监督形式推进最先进水平的最佳尝试。我们注意到，仅在 PRM800K 解答上训练 ORM 会有问题，因为我们的主动学习策略使该数据集严重偏向错误答案解答。我们确实探索过通过混入均匀采样的解答、在 PRM800K 解答的超集上训练 ORM，但发现这并未提升 ORM 表现。

|  | ORM | PRM | 多数投票 |
| --- | --- | --- | --- |
| 求解率（Best-of-1860） | 72.4 | $\mathbf{78.2}$ | 69.6 |

![Refer to caption](2305.20050v1/large_orm_prm.png)

图 3：结果监督与过程监督奖励模型的比较，以其在大量测试解答上进行搜索的能力评估。多数投票作为强基线展示。对于 $N\leq 1000$，我们可视化了我们总共为每道题生成的 1860 个解答的许多子样本之间的方差。

图 3 展示了各奖励模型的 best-of-N 表现如何随 N 变化。由于已知多数投票是一个强基线（Wang et al., 2022；Lewkowycz et al., 2022），我们也纳入该方法作为比较点。虽然 ORM 的表现略好于多数投票基线，但 PRM 显著优于两者。PRM 不仅在所有 N 值上都达到更高表现，而且随着 N 增大性能差距还在扩大。这表明 PRM 在大量模型生成解答中进行搜索方面比 ORM 和多数投票都更有效。我们尝试过使用 RM 加权投票（Li et al., 2022；Uesato et al., 2022）来结合 PRM 与多数投票的优点，但这并未明显提升表现。我们使用 MATH 测试集的一个特定子集进行评估，该子集在附录 C 中描述。我们在附录 G 中按问题难度进一步分解这些结果。

## 4 小规模合成监督

我们发现 PRM 在大规模下优于 ORM，但仅凭这一结果描绘的图景并不完整。为了更好地比较结果监督与过程监督，有两个混杂因素必须被隔离。首先，ORM 和 PRM 的训练集无法直接比较：PRM 训练集是用主动学习构建的，偏向答案错误的解答，且小一个数量级。其次，最终答案评分会给那些尽管推理错误却得到正确最终答案的伪解答提供正面标签。这可能损害 ORM 的表现，而这一效应我们未必想归咎于一般意义上的结果监督。

由于收集人类反馈的成本高昂，我们无法轻易用人类标注者消融这些因素。我们转而用大规模 PRM 监督较小的模型来执行相关消融。这一设置使我们能以适中的成本模拟大量数据收集。在本节余下部分，我们将第 3 节中的大规模 PRM 称为 $\text{PRM}_{\text{large}}$。

![Refer to caption](2305.20050v1/small_orm_prm_active.png)

(a) 使用不同数据收集策略训练的四组奖励模型，在不同规模训练集上的比较。

![Refer to caption](2305.20050v1/small_orm_prm_robustness.png)

(b) 使用不同监督形式在 200 个样本/题上训练的三个奖励模型，在许多测试时计算预算下的比较。

图 4：不同形式的结果监督与过程监督的比较。图中显示三个随机种子下的均值和标准差。

### 4.1 过程监督与结果监督对比

我们现在对结果监督与过程监督进行直接比较。我们首先从小规模生成器为每道题采样 1 到 200 个解答。对每个数据集，我们提供三种形式的监督：来自 $\text{PRM}_{\text{large}}$ 的过程监督、来自 $\text{PRM}_{\text{large}}$ 的结果监督、以及来自最终答案检查的结果监督。监督形式的选择是这三组奖励模型之间的唯一区别，它们在其他方面都在相同的数据集上训练。关于 $\text{PRM}_{\text{large}}$ 如何用于结果监督和过程监督的更多细节见附录 H。

在图 4(a) 中，我们以 best-of-500 选择评估各奖励模型。我们看到，在所有数据收集规模上，过程监督都显著优于两种形式的结果监督。在图 4(b) 中，我们以不同 N 值下的 best-of-N 表现评估每组中最佳的奖励模型。我们看到，用 $\text{PRM}_{\text{large}}$ 做结果监督明显比最终答案检查更有效。这可以用如下事实解释：$\text{PRM}_{\text{large}}$ 对那些用错误推理得到正确最终答案的解答提供了更好的监督。

由 $\text{PRM}_{\text{large}}$ 监督还是由最终答案检查监督，哪一个是更合适的结果监督基线，这一点并不明确。虽然最终答案监督更明确地基于结果，但其主要弱点——假阳性的存在——可以说在 MATH 数据集中被过度强调了。由 $\text{PRM}_{\text{large}}$ 做结果监督更好地代表了在较不容易出现假阳性的领域中的结果监督。我们认为由 $\text{PRM}_{\text{large}}$ 做结果监督是更相关的基线，但我们鼓励读者得出自己的结论。

### 4.2 主动学习

最后，我们研究主动学习的影响。我们在每道题的单个样本上训练一个小规模奖励模型 $\text{PRM}_{\text{selector}}$，并用该模型为每道题的 1000 个样本打分。为训练每个更大的奖励模型，我们为每道题选择 $N$ 个样本，其中 80% 是（根据 $\text{PRM}_{\text{selector}}$）最有说服力的错误答案样本，20% 是其余最有说服力的样本（无论答案对错）。我们用 $\text{PRM}_{\text{large}}$ 为选中的样本打分并在这些分数上训练。这一流程确保所有样本在 $\text{PRM}_{\text{selector}}$ 下都相对有说服力、其中很大比例已知至少包含一个错误，并且我们的整体数据集不会过度偏向错误答案解答。该数据标注方案的表现见图 4(a)。通过比较有主动学习与无主动学习时最佳拟合线的斜率，我们估计这种形式的主动学习的数据效率约为均匀数据标注的 2.6 倍。我们注意到，在最大主动学习数据集（每题 200 个样本）上训练的模型似乎略微落后于预期趋势线。我们对这一观察的最佳解释是：200 个样本占了整体选择池（1000 个样本）的相当大比例，而这种相对缺乏多样性限制了主动学习可能带来的上行空间。

我们还对在数据收集全程迭代重训 $\text{PRM}_{\text{selector}}$ 的影响进行了初步研究。在各次迭代之间，我们用当前所有已标注数据重训 $\text{PRM}_{\text{selector}}$。遗憾的是，我们观察到该过程存在无法诊断的不稳定性。所得奖励模型并不比上述模型更好。我们预期某种形式的迭代重训在主动学习中会有益处，但我们目前没有具体证据支持这一主张。我们认为这是未来研究中一个富有吸引力的方向。

## 5 分布外泛化

|  | ORM | PRM | 多数投票 | 题目数 |
| --- | --- | --- | --- | --- |
| AP 微积分 | $68.9\%$ | $\mathbf{86.7\%}$ | $80.0\%$ | 45 |
| AP 化学 | $68.9\%$ | $\mathbf{80.0\%}$ | $71.7\%$ | 60 |
| AP 物理 | $77.8\%$ | $\mathbf{86.7\%}$ | $82.2\%$ | 45 |
| AMC10/12 | $49.1\%$ | $\mathbf{53.2\%}$ | $32.8\%$ | 84 |
| 合计 | $63.8\%$ | $\mathbf{72.9\%}$ | $61.3\%$ | 234 |

表 1：我们用近期 STEM 考试衡量分布外泛化。我们使用每道题 100 个测试样本评估结果监督 RM、过程监督 RM 和多数投票。

为了对分布外泛化获得某种度量，我们在一个由 224 道 STEM 题目组成的留出集上评估我们的大规模 ORM 和 PRM，这些题目取自最近的 AP 物理、AP 微积分、AP 化学、AMC10 和 AMC12 考试。由于这些考试在预训练数据集汇编之后发布，我们可以高度确信模型没有见过这些题目。我们在表 1 中报告 ORM、PRM 和多数投票的 best-of-100 表现。我们观察到的结果与第 3 节类似：PRM 优于 ORM 和多数投票两者。这告诉我们 PRM 能容忍一定程度的分布偏移，其强劲表现在全新的测试题目上依然成立。

## 6 讨论

### 6.1 信用分配

过程监督的一个明显优势是它比结果监督提供更精确的反馈。用结果监督训练的奖励模型面临一个困难的信用分配（credit assignment）任务——要良好泛化，它必须确定一个错误解答究竟在哪里出了错。这对难题来说尤其困难：大多数模型生成的解答在某处都包含错误，因此来自结果监督的负面标签的边际价值很低。相比之下，过程监督提供了更丰富的信号：它既指明了前多少步实际上是正确的，也指明了错误步骤的精确位置。过程监督使信用分配更容易，我们相信这解释了它的强劲表现。

### 6.2 对对齐的影响

过程监督相对于结果监督有若干与 AI 对齐相关的优势。过程监督更有可能产生可解释的推理，因为它鼓励模型遵循一个由人类认可的过程。过程监督也内在地更安全：它直接奖励一条对齐的思维链，而不是依赖结果作为对齐行为的代理（Stuhlmüller and Byun, 2022）。相比之下，结果监督更难审查，其传达的偏好也更不精确。在最坏情况下，将结果用作不完美的代理可能导致模型在学会利用奖励信号之后变得失配（Uesato et al., 2022；Cotra, 2022；Everitt et al., 2017）。

在某些情况下，更安全的 AI 系统方法可能导致表现下降（Ouyang et al., 2022；Askell et al., 2021），这一代价被称为对齐税（alignment tax）。总体而言，任何对齐税都可能因为部署最强模型的压力而阻碍对齐方法的采用。我们的结果表明，过程监督实际上产生的是负的对齐税。这可能导致过程监督被更广泛地采用，而我们相信这会带来正面的对齐副作用。这些结果能在多大程度上推广到数学之外尚属未知，我们认为未来工作探索过程监督在其他领域中的影响十分重要。

### 6.3 测试集污染

MATH 数据集的测试集包含在多个在线场合被讨论过的问题，其中一些很可能出现在我们模型的预训练数据集中。我们尝试过使用字符串匹配启发式从 MathMix 数据集中移除所有 MATH 问题，但由于人们可以在网上发布难以检测的问题改写，很难对 MathMix 与 MATH 数据集之间的重叠给出任何强保证。

在我们检查模型生成解答的经验中，我们没有看到模型记忆 MATH 问题的明确迹象。然而，无法排除能躲过人工检查的微妙记忆形式，而且仍有可能某种程度的污染轻微夸大了我们在 MATH 测试集上的表现。即便如此，我们预期任何污染在所有方法中的表现是相似的，本工作中所做的相对比较大体上不会受影响。

我们还注意到，PRM 经常能从生成器下求解率仅为个位数百分比低的 MATH 问题中挑出正确解答，其中一些例子可以在附录 I 中看到。生成器的低求解率进一步表明它没有通过测试集污染遇到过这类问题。第 5 节的泛化结果进一步强化了测试集污染未显著影响本工作的主张，因为我们在保证未被污染的问题上观察到定性相似的结果。

## 7 相关工作

### 7.1 结果监督与过程监督

在与我们工作密切相关的文献中，Uesato et al. (2022) 比较了小学数学领域中结果监督与过程监督的影响。他们发现两种方法带来了相近的最终答案错误率，而过程监督用更少的数据达到了这些结果。虽然我们的核心方法论非常相似，但有三个主要细节不同。首先，我们使用能力更强的模型来收集 PRM800K 数据集并开展大规模实验。不过，我们在第 4 节的小规模结果表明，并不需要大规模模型就能观察到过程监督的好处。其次，我们在 MATH 数据集上评估，它比 GSM8K 显著更具挑战性。第三，我们收集了数量大得多的过程监督数据。

表面上看，Uesato et al. (2022) 的结果似乎与我们关于过程监督带来更好表现的主张相冲突。然而，我们相信这一表面的冲突可以用监督规模上的差异来解释。图 4(a) 中的数据缩放趋势表明，少量的过程监督与大量的结果监督确实会带来相近的表现，这与 Uesato et al. (2022) 的结果一致。该趋势还表明，当扩大规模时，即使仅以结果来评判，过程监督也胜过结果监督。这与我们在第 3 节中的结果一致。我们相信这些结果为使用过程监督提供了有力论据。

### 7.2 合成监督

与我们在第 4 节的工作类似，Gao et al. (2022) 使用大型奖励模型监督较小模型的训练。他们研究 RLHF 期间发生的过度优化，其实验需要大量人类偏好数据。为绕开这一挑战，他们用金标准（gold-standard）奖励模型替代人类反馈。我们用大规模奖励模型监督较小奖励模型的做法与他们的方法有相似之处。

### 7.3 自然语言推理

近期若干考察大型语言模型推理能力的研究与我们的工作有隐含的相关性。Lewkowycz et al. (2022) 表明，在大型技术内容语料库上微调模型能带来 MATH 上的显著提升。Wang et al. (2022) 表明，自洽性（self-consistency）在许多推理基准上带来格外强劲的表现，且显著地无需任何额外微调。Wei et al. (2022) 和 Nye et al. (2021) 展示了通过思维链或草稿板（scratchpad）显式执行中间推理步骤对于求解需要多步推理的任务的重要性。Kojima et al. (2022) 表明，仅以一个简单提示为条件，模型能够零样本地执行这一行为。

## 8 结论

我们已经证明，在数学推理领域，过程监督可以用来训练比结果监督可靠得多的奖励模型。我们还证明，主动学习可以用来降低人类数据收集的成本，方法是只把最有价值的模型补全呈现给人类获得反馈。我们发布了 PRM800K，即用于训练我们最先进奖励模型的完整人类反馈数据集，希望消除这一显著的准入门槛能够催化大型语言模型对齐的相关研究。我们相信过程监督目前仍探索不足，我们期待未来工作更深入地研究这些方法的泛化程度。

## 致谢

我们感谢 Joshua Achiam、Mark Chen、Jonathan Gordon、Dan Hendrycks、Lukasz Kaiser、Oleg Murk、Ben Sokolowsky、Francis Song 和 Jonathan Uesato 的宝贵反馈和深入讨论；感谢 Giambattista Parascandolo 和 Daniel Selsam 对 MathMix 数据集的贡献；感谢 Jonathan Ward 对数据收集界面的贡献；感谢 Wojciech Zaremba 鼓励我们扩大数据收集；感谢 Peter Hoeschele 和 Aris Kostantinidis 对数据收集的支持；感谢 OpenAI 的研究加速和超级计算团队提供基础设施支持；并感谢 Scale 团队以及创建 PRM800K 的众多数据标注者。

## 参考文献

- Askell et al. (2021)

  A. Askell, Y. Bai, A. Chen, D. Drain, D. Ganguli, T. Henighan, A. Jones,
  N. Joseph, B. Mann, N. DasSarma, et al.
  A general language assistant as a laboratory for alignment.
  *arXiv preprint arXiv:2112.00861*, 2021.
- Bubeck et al. (2023)

  S. Bubeck, V. Chandrasekaran, R. Eldan, J. Gehrke, E. Horvitz, E. Kamar,
  P. Lee, Y. T. Lee, Y. Li, S. Lundberg, et al.
  Sparks of artificial general intelligence: Early experiments with
  gpt-4.
  *arXiv preprint arXiv:2303.12712*, 2023.
- Christiano et al. (2017)

  P. F. Christiano, J. Leike, T. Brown, M. Martic, S. Legg, and D. Amodei.
  Deep reinforcement learning from human preferences.
  *Advances in neural information processing systems*, 30, 2017.
- Cobbe et al. (2021)

  K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert,
  J. Tworek, J. Hilton, R. Nakano, et al.
  Training verifiers to solve math word problems.
  *arXiv preprint arXiv:2110.14168*, 2021.
- Cotra (2022)

  A. Cotra.
  Without specific countermeasures, the easiest path to transformative
  AI likely leads to AI takeover.
  <https://www.alignmentforum.org/posts/pRkFkzwKZ2zfa3R6H/without-specific-countermeasures-the-easiest-path-to>,
  2022.
- Creswell et al. (2022)

  A. Creswell, M. Shanahan, and I. Higgins.
  Selection-inference: Exploiting large language models for
  interpretable logical reasoning.
  *arXiv preprint arXiv:2205.09712*, 2022.
- Everitt et al. (2017)

  T. Everitt, V. Krakovna, L. Orseau, M. Hutter, and S. Legg.
  Reinforcement learning with a corrupted reward channel.
  *arXiv preprint arXiv:1705.08417*, 2017.
- Gao et al. (2022)

  L. Gao, J. Schulman, and J. Hilton.
  Scaling laws for reward model overoptimization.
  *arXiv preprint arXiv:2210.10760*, 2022.
- Hendrycks et al. (2021)

  D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and
  J. Steinhardt.
  Measuring mathematical problem solving with the math dataset.
  *arXiv preprint arXiv:2103.03874*, 2021.
- Kojima et al. (2022)

  T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, and Y. Iwasawa.
  Large language models are zero-shot reasoners.
  *arXiv preprint arXiv:2205.11916*, 2022.
- Lewkowycz et al. (2022)

  A. Lewkowycz, A. Andreassen, D. Dohan, E. Dyer, H. Michalewski, V. Ramasesh,
  A. Slone, C. Anil, I. Schlag, T. Gutman-Solo, et al.
  Solving quantitative reasoning problems with language models.
  *arXiv preprint arXiv:2206.14858*, 2022.
- Li et al. (2022)

  Y. Li, Z. Lin, S. Zhang, Q. Fu, B. Chen, J.-G. Lou, and W. Chen.
  On the advance of making language models better reasoners.
  *arXiv preprint arXiv:2206.02336*, 2022.
- Maynez et al. (2020)

  J. Maynez, S. Narayan, B. Bohnet, and R. McDonald.
  On faithfulness and factuality in abstractive summarization.
  *arXiv preprint arXiv:2005.00661*, 2020.
- Nakano et al. (2021)

  R. Nakano, J. Hilton, S. Balaji, J. Wu, L. Ouyang, C. Kim, C. Hesse, S. Jain,
  V. Kosaraju, W. Saunders, et al.
  Webgpt: Browser-assisted question-answering with human feedback.
  *arXiv preprint arXiv:2112.09332*, 2021.
- Nichols et al. (2020)

  E. Nichols, L. Gao, and R. Gomez.
  Collaborative storytelling with large-scale neural language models.
  In *Proceedings of the 13th ACM SIGGRAPH Conference on Motion,
  Interaction and Games*, pages 1–10, 2020.
- Nye et al. (2021)

  M. Nye, A. J. Andreassen, G. Gur-Ari, H. Michalewski, J. Austin, D. Bieber,
  D. Dohan, A. Lewkowycz, M. Bosma, D. Luan, et al.
  Show your work: Scratchpads for intermediate computation with
  language models.
  *arXiv preprint arXiv:2112.00114*, 2021.
- OpenAI (2023)

  OpenAI.
  Gpt-4 technical report.
  *arXiv preprint arXiv:2303.08774*, 2023.
- Ouyang et al. (2022)

  L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. L. Wainwright, P. Mishkin, C. Zhang,
  S. Agarwal, K. Slama, A. Ray, et al.
  Training language models to follow instructions with human feedback.
  *arXiv preprint arXiv:2203.02155*, 2022.
- Shen et al. (2021)

  J. Shen, Y. Yin, L. Li, L. Shang, X. Jiang, M. Zhang, and Q. Liu.
  Generate & rank: A multi-task framework for math word problems.
  *arXiv preprint arXiv:2109.03034*, 2021.
- Stiennon et al. (2020)

  N. Stiennon, L. Ouyang, J. Wu, D. Ziegler, R. Lowe, C. Voss, A. Radford,
  D. Amodei, and P. F. Christiano.
  Learning to summarize with human feedback.
  *Advances in Neural Information Processing Systems*,
  33:3008–3021, 2020.
- Stuhlmüller and Byun (2022)

  A. Stuhlmüller and J. Byun.
  Supervise process, not outcomes.
  <https://ought.org/updates/2022-04-06-process>, 2022.
- Uesato et al. (2022)

  J. Uesato, N. Kushman, R. Kumar, F. Song, N. Siegel, L. Wang, A. Creswell,
  G. Irving, and I. Higgins.
  Solving math word problems with process-and outcome-based feedback.
  *arXiv preprint arXiv:2211.14275*, 2022.
- Wang et al. (2022)

  X. Wang, J. Wei, D. Schuurmans, Q. Le, E. Chi, and D. Zhou.
  Self-consistency improves chain of thought reasoning in language
  models.
  *arXiv preprint arXiv:2203.11171*, 2022.
- Wei et al. (2022)

  J. Wei, X. Wang, D. Schuurmans, M. Bosma, E. Chi, Q. Le, and D. Zhou.
  Chain of thought prompting elicits reasoning in large language
  models.
  *arXiv preprint arXiv:2201.11903*, 2022.
- Zelikman et al. (2022)

  E. Zelikman, Y. Wu, J. Mu, and N. Goodman.
  Star: Bootstrapping reasoning with reasoning.
  *Advances in Neural Information Processing Systems*,
  35:15476–15488, 2022.
- Ziegler et al. (2019)

  D. M. Ziegler, N. Stiennon, J. Wu, T. B. Brown, A. Radford, D. Amodei,
  P. Christiano, and G. Irving.
  Fine-tuning language models from human preferences.
  *arXiv preprint arXiv:1909.08593*, 2019.

## 附录 A MathMix

与 Lewkowycz et al. (2022) 类似，我们构建了一个高质量数学相关 token 的大规模数据集，用于一个轻量级预训练阶段，之后再在 MATH 和 PRM800K 等相对较小的数据集上微调。我们称之为 MathMix 的这一数据集与训练 Minerva 所用的数据集相比有两点主要差异。第一，它更小，并更激进地过滤为高质量数学解题内容；第二，它没有显式混入通用语言数据。

Minerva 在 38.5B 个 token 的 arXiv 文档和含 LaTeX 内容的网页抓取页面上训练，而 MathMix 由一个更小的 1.5B token 集合构成，包含单条数学问题及其解答、讨论数学问题与概念的自由文本，以及合成数据（表 2）。Minerva 预训练所用数据集含 5% 的通用自然语言数据，而我们选择不显式混入任何自然语言数据，主要因为 MathMix 已经包含大量自然语言数据。

| 数据类型 | token 数 | 是否存在于预训练中？ |
| --- | --- | --- |
| 数学问题与解答 | $\sim$ 275M | 否 |
| 自由数学讨论文本（1） | $\sim$ 430M | 否 |
| 自由数学讨论文本（2） | $\sim$ 450M | 是 |
| 合成数据（1） | $\sim$ 30M | 否 |
| 合成数据（2） | $\sim$ 100M | 是 |
| 评论评分数据（Critiques grading data） | $\sim$ 500M | 否 |

表 2：MathMix 数据集组成。

注意，在训练较小模型时（如第 4 节），我们使用一个略小的 MathMix 变体，它排除了评论数据，仅由 1B 个 token 构成。在大模型实验中，我们在 MathMix 上训练约 3B 个 token（2 个 epoch）。在小模型实验中，我们训练 6 个 epoch（约 6.6B 个 token）。

我们对 MathMix 针对 MATH 数据集测试划分应用了一组去污染检查，包括剥离 LaTeX 并搜索匹配的 n-gram，但我们无法对去污染的效果给出强保证。如 6.3 节所讨论的，我们预期本工作中的相对比较不会受到测试集污染的显著影响。

## 附录 B PRM800K

我们在 101,599 个解答样本上收集了 1,085,590 个步级标签。我们将整个未过滤数据集作为 PRM800K 发布。训练期间，我们丢弃用于质量控制的标签，以及标注者无法完成任务的任何步级标签。过滤后的数据集包含约 75,000 个解答上的约 800,000 个步级标签。完整的 PRM800K 数据集可在 <https://github.com/openai/prm800k> 获取。

数据收集分为两个独立阶段。在阶段 1，我们为解答每一步的多个备选补全收集标签。这为我们的数据集提供了种子，但过程繁琐——对许多步骤而言备选项是重复的，我们发现标注者花费大量时间监督冗长而乏味的解答。因此，我们在这一阶段收集的步级标签比后来收集的更具重复性。阶段 1 总计约占 PRM800K 的 5%，即约 40,000 个步级标签。

我们的大部分标签是作为阶段 2 的一部分收集的，在此期间我们扩大并精简了数据收集流程。阶段 2 的数据收集分为 10 个世代（generation）。对每个世代，我们从生成器为每道题采样 N 个解答。我们用当前最佳的 PRM 对这些解答排序，并将得分最高的错误答案解答呈现给标注者。我们在各世代之间用所有最新数据重训该 PRM。这一主动学习策略相当大地改变了数据的天平。虽然我们有时也呈现正确解答（或是手动注入正确解答，或因自动评分出错），我们在该阶段收集的标签绝大多数是关于错误解答的。表 3 分解了不同数据收集阶段之间正确/错误步骤与解答的平衡。尽管我们主要在错误解答上收集标签，我们仍然为正确的单个步骤收集了许多标签。事实上，我们在 4.2 节的小规模消融表明，这种偏好标注高分错误答案解答的主动学习策略，尽管造成数据集不平衡，仍能提升表现。

|  | 阶段 1 | 阶段 2 | 合并 |
| --- | --- | --- | --- |
| 以正确解答结束的比例 | 85.1 | 13.2 | 14.2 |
| 正确步骤比例 | 58.6 | 74.1 | 73.1 |

表 3：正面/负面步骤/解答的分布。

我们阶段 2 的一些问题用于质量控制。对于质量控制问题，研究者标出哪些步骤可以合理地标注为不正确。然后我们评估标注者能否一致地将这些步骤标为不正确。在开始阶段 2 之前，我们要求所有标注者标注 30 道质量控制问题。这作为筛选测试，我们只接纳与我们金标准标签至少 75% 一致的标注者。

随后我们在每个世代指定 10-20 道额外质量控制问题，并在标注者执行任务时随机呈现给他们。我们用这一持续质量控制的结果移除质量下滑过多的标注者，并用常见错误准备教学材料，以改进标注者与我们指南的一致性。

## 附录 C 评测

随着项目规模扩大，我们开始不得不为同一道训练题的多个解答收集标签。为避免在 7,500 道 MATH 训练题上过拟合的风险，我们将训练集扩充至包含 4,500 道 MATH 测试划分的题目。因此我们只在其余 500 道留出问题上评估模型。这 500 道测试问题是均匀随机抽取的。在图 5 中，我们展示了该子集中难度级别与科目分布对整个 MATH 测试集具有代表性。我们使用的具体测试集可在 <https://github.com/openai/prm800k> 获取。究竟需要多少不同的训练题、以及我们的方法多快会过拟合训练集，我们留给未来工作探索。

![Refer to caption](2305.20050v1/figures/math_difficulty.png)

![Refer to caption](2305.20050v1/figures/math_subject.png)

图 5：两幅直方图，比较原始 MATH 测试集与我们 500 题测试子集中问题难度级别和科目分布。

## 附录 D 标注指南

标注者的任务是查看解答中的步骤，并将每一步标注为正面、负面或中性。如果某一步在上下文中恰当、合理、正确，且只包含易于验证的计算，则该步被视为中性。如果某一步是中性的且同时向解答推进，则被视为正面。所有其他步骤被视为负面。标注者没有得到参考解答，但得到了基准真实（ground truth）最终答案。我们选择不提供参考解答，以避免使标注者偏向通往解答的某条特定路径。我们选择提供基准真实最终答案，因为这一信息有时能帮助标注者化解自己的误解。

在阶段 1，标注者被允许在所有候选步骤均为负面时输入自己的步骤。然后解答会从随机选择的一个正面步骤（若无正面步骤则选择中性步骤）继续推进。这经常导致轨迹陷入无尽的中性步骤序列——说着合理的话却以令人懊恼的缓慢速度向解答推进——或陷入需要持续人工监督的负面步骤。在阶段 2，我们预先生成完整解答，并在遇到第一个负面步骤时立即结束任务。给标注者的完整指南见 <https://github.com/openai/prm800k/tree/main/prm800k/instructions>。

## 附录 E ORM 训练细节

我们按照与 Cobbe et al. (2021) 中 token 级验证器相同的方式训练结果监督奖励模型，仅有少许超参数上的细微差异。具体而言，我们在每个「模型样本 + 奖励模型标签」数据集上只训练单个 epoch，不使用 dropout，也不联合学习语言建模目标。我们发现表现在合理范围内对大多数其他超参数不敏感。

为收集模型样本，我们直接从生成器在温度 1.0 下均匀采样，不对正负样本施加任何重新平衡。在训练时，奖励模型对上下文中的每个 token 做出预测。解答中每个 token 的目标相同，取决于该解答被标注为正确还是不正确。在测试时，我们直接使用补全中最后一个 token 的分数作为解答的总分。我们注意到，这一设置与 Cobbe et al. (2021) 中训练 token 级验证器的方式完全相同。

## 附录 F PRM 细节

### F.1 训练

我们通过微调 MathMix 模型来训练 PRM，使其在给定一个以某个被标注步骤结尾的解答前缀时，预测正面、负面和中性标签的概率。我们使用包含 PRM800K 前 $\sim10\%$ 的数据集扫描超参数。将 LLM 从其普通语言建模任务微调到这样的分类任务是一个很大的分布偏移，我们发现低学习率对稳定的 PRM 训练很重要。

我们所有的 PRM 都训练 2 个 epoch。在较小数据集上（如阶段 1 和阶段 2 的最初几个世代），这比只训练 1 个 epoch 提升了最终表现。在某个点之前的额外 epoch 不会明显帮助或损害表现。在较大数据集上，2 epoch 训练的好处减弱，但为了保持一致性我们继续这么做。

### F.2 打分

使用 PRM 为解答打分有多种方式。总体而言，我们通过对步级分数进行归约（reduction）产生单个解答级分数，其中步级分数是该步标签为正面的概率。这涉及两个具体的实现决策。第一，在确定步级分数时，我们将中性标签视为正面还是负面。第二，在确定解答级分数时，我们用步级分数的最小值还是乘积作为归约。

我们在表 4 中展示所有四种打分策略的结果。表现最佳的策略是取步级分数的乘积并将中性视为正面，但所有策略之间的表现差异很小。在本工作余下部分，我们将中性步骤视为正面，并将解答分数定义为步级分数的乘积。使用乘积而非最小值作为归约确实对步数较多的解答造成轻微偏置。

|  | 乘积 | 最小值 |
| --- | --- | --- |
| 中性 = 正面 | $78.2\%$ | $77.6\%$ |
| 中性 = 负面 | $77.4\%$ | $77.8\%$ |

表 4：使用 PRM 四种不同打分策略的 Best-of-1860 测试表现。

## 附录 G 难度分解

我们展示 ORM 和 PRM 在 MATH 数据集每个五分位（quintile）上的表现。我们根据生成器下的通过率确定五分位。有趣的是，表现差距不仅在高难度问题上明显：它在所有难度上实际上都明显。对最低难度的问题，我们看到有可能找到欺骗 ORM 的对抗样本，因为 ORM 的表现随样本数增加而略有下降。相比之下，PRM 在同一组样本上保持高度稳健。

我们还看到，增加样本数量对最高难度问题的正面影响最大。这是意料之中的，因为要找到难题的一个真实且有说服力的解答，可能需要大量生成器样本。

图 6：按问题难度分解的 ORM 与 PRM 表现。

![Refer to caption](2305.20050v1/difficulty_breakdown.png)

## 附录 H 合成监督细节

我们可以用 $\text{PRM}_{\text{large}}$ 为较小模型提供结果监督或过程监督。我们根据 $\text{PRM}_{\text{large}}$ 输出的步级概率确定单个步骤的标签。为此，我们设定一个任意阈值：$\text{PRM}_{\text{large}}$ 以大于 20% 的概率赋予负面标签的任何步骤被视为不正确。我们选择这一阈值是基于如下观察：$\text{PRM}_{\text{large}}$ 在偏向正面标签的方向上略有失准。

为给一个解答提供过程监督，我们直接返回 $\text{PRM}_{\text{large}}$ 提供的步级标签（正面或负面），直到第一个被标记为负面的步骤为止。这模仿了我们真实的人类数据收集过程。为提供结果监督，当且仅当 $\text{PRM}_{\text{large}}$ 认为每一步都正确（使用相同的阈值逻辑）时，我们将该解答标记为正确。

## 附录 I PRM 可视化

所示所有示例均来自大规模生成器（GPT-4）。我们注明生成器下的通过率，以给出这些问题难度的某种感觉。

### I.1 真阳性

这些精挑细选的示例展示了大规模 PRM 排名最高的、来自生成器的 best-of-1860 解答。

问题 1. 生成器通过率：0.1%。这道具有挑战性的三角学问题需要以一种完全不显眼的顺序应用多个恒等式。大多数解答尝试都失败，因为很难选择哪些恒等式真正有用。尽管此题的成功解答罕见，奖励模型正确地识别出何时找到了一条有效的思维链。

![[Uncaptioned image]](2305.20050v1/figures/true_positive_2.png)

问题 2. 生成器通过率：5.8%。在第 7、8 步，生成器开始执行试错猜测（guess-and-check）。这是模型可能产生幻觉的常见位置，即宣称某个猜测成功而实际并非如此。在本例中，奖励模型验证了每一步并判定该思维链正确。

![[Uncaptioned image]](2305.20050v1/figures/true_positive_1.png)

问题 3. 生成器通过率：1.7%。生成器成功应用多个三角恒等式化简该表达式。

![[Uncaptioned image]](2305.20050v1/figures/true_positive_3.png)

问题 4. 生成器通过率：4.5%。在这里，生成器成功执行了一连串复杂的多项式因式分解。第 5 步中 Sophie-Germain 恒等式的使用是一个可被视为富有洞察力的重要步骤。

![[Uncaptioned image]](2305.20050v1/figures/true_positive_4.png)

### I.2 真阴性

问题 5. 生成器通过率：4.5%。生成器在第 12 步尝试对一个实际上并非平方差的表达式使用平方差公式。奖励模型捕捉到了这一错误。

![[Uncaptioned image]](2305.20050v1/figures/true_negative_1.png)

问题 6. 生成器通过率：93.5%。在第 7 步，生成器做了一次错误的化简尝试。奖励模型捕捉到了这一错误。

![[Uncaptioned image]](2305.20050v1/figures/true_negative_2.png)

问题 7. 生成器通过率：48.0%。在第 11 步，生成器犯了一个简单的计算错误。奖励模型捕捉到了这一错误。

![[Uncaptioned image]](2305.20050v1/figures/true_negative_3.png)

问题 8. 生成器通过率：5.8%。第 8 步中的论证有些奇怪，但奖励模型放过了它。不过在第 9 步，模型对该表达式做了错误的因式分解。奖励模型捕捉到了这一错误。

![[Uncaptioned image]](2305.20050v1/figures/true_negative_4.png)

### I.3 假阳性

问题 9. 生成器通过率：18.5%。生成器在第 9 步犯了一个微妙的计数错误。表面上看，既然有 5 种颜色，声称交换同色球有 5 种方式似乎是合理的。然而这少算了一半，因为 Bob 有 2 种选择把哪个球还给 Alice。奖励模型被这一错误欺骗了。

![[Uncaptioned image]](2305.20050v1/figures/false_positive_1.png)

问题 10. 生成器通过率：17.6%。在第 13 步，生成器尝试通过合并同类项来化简方程。它正确地把线性项移到左侧并合并，但随后错误地未对右侧做任何处理。奖励模型被这一错误欺骗了。

![[Uncaptioned image]](2305.20050v1/figures/false_positive_2.png)

问题 11. 生成器通过率：13.4%。生成器尝试执行长除法，但在第 16 步，它忘记在十进制数的循环节中包含前导零。奖励模型被这一错误欺骗了。

![[Uncaptioned image]](2305.20050v1/figures/false_positive_3.png)

问题 12. 生成器通过率：9.1%。在第 4 步，生成器错误地声称该序列每 12 项循环一次，而实际上每 10 项循环一次。这类计数错误偶尔会欺骗奖励模型。

![[Uncaptioned image]](2305.20050v1/figures/false_positive_4.png)
