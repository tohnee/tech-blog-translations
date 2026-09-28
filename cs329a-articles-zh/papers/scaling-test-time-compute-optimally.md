---
title: "优化扩展 LLM 测试时计算可比扩展模型参数更有效"
title_en: "Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters"
arxiv: 2408.03314
source: https://arxiv.org/abs/2408.03314
crawled: 2026-09-23
translated: 2026-09-23
---

# 优化扩展 LLM 测试时计算可比扩展模型参数更有效

> 原文：[Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters](https://arxiv.org/abs/2408.03314) · Stanford CS329A 指定阅读

Charlie Snell（UC Berkeley）、Jaehoon Lee（Google DeepMind）、Kelvin Xu（Google DeepMind）、Aviral Kumar（Google DeepMind）

注：同等指导（equal advising）。本工作在 Charlie Snell 于 Google DeepMind 实习期间完成。

###### 摘要

让 LLM 通过使用更多测试时计算来改进自身输出，是构建能够在开放式自然语言上运行的通用自我改进智能体的关键一步。在本文中，我们研究 LLM 推理时计算的扩展，重点回答这样一个问题：*如果允许 LLM 使用固定但不可忽略的推理时计算量，它在一个有挑战性的提示上能将性能提升多少？*回答这一问题不仅关系到 LLM 可达到的性能，也关系到 LLM 预训练的未来，以及应当如何在推理时计算与预训练计算之间做权衡。尽管这个问题很重要，却鲜有研究尝试理解各种测试时推理方法的缩放行为。此外，当前的工作对其中不少策略给出的主要是负面结果。在本工作中，我们分析扩展测试时计算的两种主要机制：(1) 针对稠密的、基于过程的验证器奖励模型进行搜索；(2) 在测试时根据提示自适应地更新模型对回答的分布。我们发现，在这两种情形下，不同测试时计算扩展方法的有效性都关键性地取决于提示的难度。这一观察促使我们应用一种「计算最优」（compute-optimal）缩放策略，其作用是逐提示地自适应分配测试时计算，以实现最高效的利用。使用这一计算最优策略，我们可以把测试时计算扩展的效率相对 best-of-N 基线提升 4 倍以上。此外，在一项 FLOPs 对齐的评估中，我们发现：在较小基座模型已能取得一定非平凡成功率的问题上，测试时计算可以用来超过一个比它大 14 倍的模型。

## 1 引言

人类面对困难问题时往往会思考更久，以可靠地改进自己的决策（Kahneman, 2013；Evans, 1984；Kahneman, 2003）。我们能否把类似的能力灌输给当今的大型语言模型（LLM）？更具体地说，给定一个有挑战性的输入查询，*我们能否让语言模型最有效地利用测试时的额外计算来提高回答的准确性？*理论上，通过在测试时施加额外计算，LLM 应当能做得比它被训练的目标更好。此外，这种测试时的能力也有潜力在智能体与推理任务中开辟新的方向（Shinn et al., 2023；Wei et al., 2023；Qu et al., 2024b）。例如，如果可以用推理期间的额外计算来换取预训练模型规模，就能让 LLM 部署到可以用较小的端侧模型替代数据中心级 LLM 的用例中。通过额外推理时计算自动生成改进的模型输出，也为一条可在减少人类监督下运行的通用自我改进算法提供了路径。

图 1：*主要结果总结。*左：迭代自我精炼（即修订）与搜索的计算最优缩放。左侧上方在修订设置中比较我们 PaLM 2-S* 修订模型的计算最优缩放策略与各基线，下方在 PRM 搜索设置中做同样比较。可以看到，在修订情形下，标准 best-of-N（如「并行」）与计算最优缩放之间的差距逐渐拉大，使计算最优缩放能以少 4 倍的测试时计算胜过 best-of-N。类似地，在 PRM 搜索设置中，我们观察到计算最优缩放相对 best-of-N 在早期即有显著改进，在若干点上几乎以少 4 倍的计算追平 best-of-N。细节见第 5 节与第 6 节。右：比较测试时计算与模型参数扩展。我们比较 PaLM 2-S* 的计算最优测试时扩展与一个约大 14 倍的预训练模型在不加额外测试时计算（如贪心采样）时的表现。我们考虑两个模型都预期有 $X$ 个预训练 token、$Y$ 个推理 token 的设置。训练更大的模型等于把这两项的 FLOPs 需求都乘上倍数。如果我们对较小的模型施加额外测试时计算以匹配该更大模型的 FLOPs 需求，它在准确性上比较如何？可以看到，对于修订（上方），当 $Y\ll X$ 时，测试时计算往往优于额外预训练。然而，随着推理与预训练 token 之比增大，测试时计算在简单问题上仍然更优，而在较难的问题上，预训练在这些设置中更可取。PRM 搜索（下方）也呈现类似趋势。更多细节见第 7 节。

先前研究推理时计算的工作给出了好坏参半的结果。一方面，一些工作表明当前 LLM 可以利用测试时计算改进输出（Bai et al., 2022；Madaan et al., 2023；Du et al., 2023；Saunders et al., 2022；Yao et al., 2023）；另一方面，另一些工作表明这些方法在数学推理等更复杂任务上的有效性仍然相当有限（Huang et al., 2023；Stechly et al., 2023；Valmeekam et al., 2023），尽管推理问题往往需要对已有知识做推断，而不是需要新知识。这类相互矛盾的发现，正需要我们对不同的测试时计算扩展方法做系统分析。

我们希望理解扩大测试时计算的收益。可以说最简单也研究得最充分的测试时计算扩展方法是 *best-of-N* 采样：从基座 LLM「并行」采样 N 个输出，并依据一个学习到的验证器或奖励模型选出得分最高的那个（Cobbe et al., 2021；Lightman et al., 2023）。但这并非利用测试时计算改进 LLM 的唯一途径。通过修改获取回答的*提议分布*（例如让基座模型「顺序」修订其初始回答（Qu et al., 2024b）），或改变*验证器*的使用方式（例如训练一个基于过程的稠密验证器（Lightman et al., 2023；Wang et al., 2023）并针对它进行搜索），扩展测试时计算的能力可以大幅提升，本文将对此加以展示。

为了理解扩大测试时计算的收益，我们在具有挑战性的 MATH 基准（Hendrycks et al., 2021）上，使用经专门微调的 PaLM-2（Anil et al., 2023）模型开展实验，这些模型被微调为或者修订错误答案（Qu et al., 2024b）（即改进提议分布；第 6 节），或者用过程奖励模型（PRM）（Lightman et al., 2023；Wang et al., 2023）验证答案中各步骤的正确性（第 5 节）。

注（脚注 1）：在 MATH 上让基座模型具备修订与验证能力，必须做针对特定能力的微调，因为即使是最强的商用 LLM 也缺乏这些能力（Huang et al., 2023；Sharma et al., 2024）。不过我们预期未来的 LLM 会因规模增大以及纳入专门针对这些能力的额外数据，而在验证与修订上更有效（Snell et al., 2024；Blakeney et al., 2024；McAleese et al., 2024）。因此，为了推进对测试时计算扩展的理解，我们必须使用针对这些能力微调的模型。话虽如此，我们预计未来模型会直接在预训练中具备此类能力，从而免去针对特定能力的微调。

在这两种方法下，我们都发现某一测试时计算策略的有效性关键取决于手头具体问题的性质和所用的基座 LLM。例如，在较容易的问题上（基座 LLM 已经能轻松给出合理回答），允许模型通过预测一串 N 次修订来迭代精炼初始答案（即修改提议分布）可能是比并行采样 N 个独立回答更有效的测试时计算用法。另一方面，对可能需要在许多不同高层解题路径之间搜索的更难问题，并行独立地重采样新回答、或针对过程奖励模型部署树搜索，很可能是更有效的测试时计算用法。这一发现说明需要部署一种自适应的「计算最优」策略来扩展测试时计算，其中根据提示选择利用测试时计算的具体方式，以最好地利用额外计算。我们还表明，从基座 LLM 视角出发的*问题难度*概念（第 4 节）可以用来预测测试时计算的效能，使我们能够在给定提示时实际实例化这一「计算最优」策略。通过以这种方式恰当地分配测试时计算，我们能够大幅改进测试时计算的扩展，在修订与搜索两种方式下都只使用约少 4 倍的计算即可超过 best-of-N 基线（第 5 节与第 6 节）。

随后，利用我们改进的测试时计算扩展策略，我们着手理解测试时计算能在多大程度上有效替代额外预训练。我们对「使用额外测试时计算的较小模型」与「预训练一个 14 倍大的模型」进行了 FLOPs 对齐的比较。我们发现在简单和中等难度问题上，甚至在困难问题上（取决于预训练与推理工作负载的具体条件），额外的测试时计算往往优于扩展预训练。这一发现表明，与其单纯聚焦于扩展预训练，在某些设置下更有效的做法是用更少计算预训练较小的模型，然后应用测试时计算来改进模型输出。话虽如此，对最具挑战性的问题，我们观察到扩大测试时计算的收益甚微。相反，我们发现在这些问题上，施加额外的预训练计算更能带来进展，这表明当前扩展测试时计算的方法与扩展预训练并非一对一可互换。总体而言，这暗示即便采用相当朴素的方法，扩大测试时计算已经可以比扩大预训练更可取，而随着测试时策略成熟还会有更多改进。从长远看，这预示着一个预训练期间花费更少 FLOPs、推理期间花费更多 FLOPs 的未来。

## 2 测试时计算的统一视角：提议器与验证器

我们首先统一各种使用测试时计算的方法，然后分析若干代表性方法。首先，我们透过「在测试时根据给定提示自适应修改模型预测分布」的视角来看待额外测试时计算的使用。理想情况下，测试时计算应当修改分布，使其生成比从 LLM 自身朴素采样更好的输出。一般而言，有两组旋钮可用来诱导 LLM 分布的修改：(1) 输入层面：通过为给定提示增补一组额外 token、让 LLM 以之为条件来获得修改后的分布；(2) 输出层面：从标准 LM 采样多个候选并对这些候选做手术。换言之，我们可以直接修改 LLM 自身诱导的提议分布，使其优于朴素地以提示为条件；也可以使用某种事后验证器或打分器来执行输出修改。这一过程令人联想到马尔可夫链蒙特卡洛（MCMC）（Andrieu et al., 2003）从复杂目标分布采样的做法——通过组合一个简单提议分布与一个得分函数。

通过改变输入 token 直接修改提议分布与使用验证器，构成了我们研究的两条独立轴线。

修改提议分布。改进提议分布的一种方式是通过 STaR 或 ReST$^{\text{EM}}$ 等受强化学习启发的微调方法，让模型直接为给定推理任务做优化（Zelikman et al., 2022；Singh et al., 2024）。注意这些技术不使用任何额外输入 token，而是专门微调模型以诱导改进的提议分布。另一类做法是自批评（self-critique）（Bai et al., 2022；Madaan et al., 2023；Du et al., 2023；Saunders et al., 2022），它让模型在测试时通过迭代地批评并修订自身输出来改进自己的提议分布。由于对现成模型做提示并不能有效地在测试时实现有效修订，我们专门微调模型，使其在复杂推理场景中迭代修订自己的答案。为此，我们采用在策略（on-policy）数据上微调、并以 Best-of-N 引导模型回答改进的做法（Qu et al., 2024b）。

优化验证器。在我们对提议分布与验证器的抽象中，验证器用于从提议分布中聚合或选出最佳答案。使用此类验证器最经典的方式是 best-of-N 采样：采样 N 个完整解答，然后按验证器选出最佳的一个（Cobbe et al., 2021）。不过这一方式还可以进一步改进：训练一个基于过程的验证器（Lightman et al., 2023）即过程奖励模型（PRM），它对解答中每个中间步骤（而不仅是最终答案）的正确性给出预测。随后我们可以利用这些逐步预测在解答空间上执行树搜索，相比朴素的 best-of-N，这提供了一种潜在更高效、也更有效的针对验证器的搜索方式（Yao et al., 2023；Feng et al., 2024；Chen et al., 2024）。

## 3 如何最优地扩展测试时计算

在统一了各种方法之后，我们现在想理解如何*最有效地*利用测试时计算来提升 LM 在给定提示上的表现。具体而言，我们希望回答：

问题设置

给定一个提示和用于求解该问题的测试时计算预算。在上述抽象下，存在多种利用测试时计算的方式。这些方法各自的有效性可能因给定具体问题而异。我们如何为给定提示确定利用测试时计算的*最有效*方式？这种方式与直接使用一个大得多的预训练模型相比又如何？

无论是精炼提议分布还是针对验证器搜索，都有若干不同的超参数可以调整，以决定测试时计算预算应当如何分配。例如，当使用为修订微调的模型作为提议分布、以 ORM 作为验证器时，我们既可以把全部测试时计算预算用于从模型并行生成 N 个独立样本然后应用 best-of-N；也可以用修订模型顺序采样 N 次修订，然后用 ORM 从序列中选出最佳答案；或在这两个极端之间取得平衡。直觉上，我们可能预期「较容易」的问题从修订中获益更多，因为模型的初始样本更可能已在大致正确的轨道上，只是需要进一步精炼。另一方面，有挑战性的问题可能需要更多地探索不同的高层解题策略，因此并行独立采样多次在此设置下可能更优。

在验证器方面，我们还可以在不同的搜索算法之间选择（例如束搜索、前瞻搜索、best-of-N），各自的特性取决于手头验证器与提议分布的质量。相比简单得多的 best-of-N 或多数投票基线，更复杂的搜索程序在更难的问题上可能更有用。

### 3.1 测试时计算最优缩放策略

因此，总体而言，我们希望为给定问题选择测试时计算预算的*最优*分配。为此，对任何一种利用测试时计算的方式（本文中例如修订与针对验证器搜索，其他场合为各种其他方法），我们把「测试时计算最优缩放策略」定义为：在测试时为给定提示选择对应超参数、以获取最大性能收益的策略。形式上，定义 $\operatorname{Target}(\theta,N,q)$ 为模型对给定提示 $q$、使用测试时计算超参数 $\theta$ 与计算预算 $N$ 所诱导的自然语言输出 token 上的分布。我们希望选择使目标分布在该问题上准确率最大的超参数 $\theta$。形式化表达为：

$$
\theta^{*}_{q,a^{*}(q)}(N)=\operatorname{argmax}_{\theta}\left(\mathbb{E}_{y\sim\operatorname{Target}(\theta,N,q)}\left[\mathbbm{1}_{y=y^{*}(q)}\right]\right), \tag{1}
$$

其中 $y^{*}(q)$ 表示问题 $q$ 的标准正确回答，$\theta^{*}_{q,y^{*}(q)}(N)$ 表示问题 $q$ 在计算预算 $N$ 下的测试时计算最优缩放策略。

### 3.2 为计算最优缩放估计题目难度

为了有效分析第 2 节讨论的不同机制（例如提议分布与验证器）的测试时缩放性质，我们将给出该最优策略 $\theta^{*}_{q,y^{*}(q)}(N)$ 的一个近似，它是给定提示的某个统计量的函数。该统计量估计给定提示的*难度*。计算最优策略被定义为该提示难度的函数。尽管它只是式 (1) 所示问题的一个近似解，我们发现相对「以临时（ad-hoc）或均匀随机方式分配推理时计算」的基线策略，它仍能带来可观的性能提升。

我们对题目难度的估计把给定题目归入五个难度级别之一。随后可以利用这一离散难度分类，在给定测试时计算预算下于验证集上估计 $\theta^{*}_{q,y^{*}(q)}(N)$，再把这些计算最优策略应用于测试集。具体地，我们为每个难度桶独立选择表现最好的测试时计算策略。这样，题目难度就在设计计算最优策略时充当了题目的充分统计量。

定义题目难度。按照 Lightman et al. (2023) 的做法，我们把题目难度定义为给定基座 LLM 的函数。具体而言，我们把模型在测试集每道题上的 pass@1 率（由 2048 个样本估计）分成五个分位数桶，各对应递增的难度级别。我们发现，这种模型特定的难度桶比 MATH 数据集中人工标注的难度桶更能预测使用测试时计算的效能。

话虽如此，我们注意到，如上评估一道题的难度假定可以 oracle 式访问标准正确性检查函数，而这在部署时当然不可用——那时我们只能拿到不知道答案的测试提示。要在实践中可行，以难度为条件的计算最优缩放策略需要先评估难度，再用正确的缩放策略来求解该问题。因此，我们通过「模型预测难度」的概念来近似问题难度：对同样的每题 2048 个样本，改用学习到的验证器（而非标准答案正确性检查）的平均最终答案得分执行相同的分桶过程。我们把这一设置称为模型预测难度（model-predicted difficulty），把依赖标准正确性的设置称为 oracle 难度（oracle difficulty）。

虽然模型预测难度免去了知道标准答案标签的需要，但以这种方式估计难度仍会在推理期间产生额外计算成本。不过，这一一次性推理成本可以并入实际运行推理时策略的成本中（例如使用验证器时，可以用同样的推理计算同时运行搜索）。更一般地说，这类似强化学习中的探索-利用权衡：在真实部署条件下，我们必须在评估难度所花计算与采用最计算最优方法之间取得平衡。这是未来工作的一条重要途径（见第 8 节）；我们的实验大半出于简便而未计入这一成本，因为我们的目标是给出关于「有效分配测试时计算究竟可能做到什么」的首批结果。

为避免用同一测试集既计算难度桶又选择计算最优策略带来的混杂，我们在测试集的每个难度桶上使用二折交叉验证。按其中一折上的表现选出最佳策略，然后用该策略在另一折上度量表现，反之亦然，最后对两折测试结果取平均。

## 4 实验设置

我们首先概述在多种验证器设计选择与提议分布下开展这一分析的实验设置，随后各节给出分析结果。

数据集。我们预期测试时计算在模型已具备回答问题所需的全部基础「知识」、而主要挑战在于从这些知识中做出（复杂）推断时最有帮助。为此，我们聚焦 MATH 基准（Hendrycks et al., 2021），它由难度各异的高中竞赛级数学题组成。所有实验均使用 Lightman et al. (2023) 所用的数据集划分：12k 道训练题与 500 道测试题。

模型。我们使用 PaLM 2-S*（Anil et al., 2023）（Codey）基座模型开展分析。我们相信该模型能代表许多当代 LLM 的能力，因此认为我们的发现很可能迁移到类似模型。最重要的是，该模型在 MATH 上已取得非平凡的表现且尚未饱和，所以我们预期它是我们一个良好的试验平台。

## 5 通过验证器扩展测试时计算

本节分析如何通过尽可能优化验证器来扩展测试时计算。为此，我们研究用过程验证器（PRM）执行测试时搜索的不同方法，并分析这些不同方法的测试时计算缩放性质。

### 5.1 训练适合搜索的验证器

PRM 训练。最初的 PRM 训练（Uesato et al., 2022；Lightman et al., 2023）使用众包工人标注。虽然 Lightman et al. (2023) 公开了他们的 PRM 训练数据（即 PRM800k 数据集），我们发现这份数据对我们而言基本无效：我们发现，即便是 best-of-N 采样这样朴素的策略也很容易利用（exploit）在该数据集上训练的 PRM。我们推测这很可能源于其数据集中 GPT-4 生成样本与我们的 PaLM 2 模型之间的分布差异。我们没有走为 PaLM 2 模型收集众包 PRM 标签这一昂贵流程，而是采用 Wang et al. (2023) 的方法在无人类标签下监督 PRM：从解答的每一步出发运行蒙特卡洛展开（rollout），用得到的逐步正确性估计作为监督。因此，我们 PRM 的逐步预测对应于基座模型采样策略的「未来回报」（reward-to-go）价值估计，与近期工作类似（Wang et al., 2023；Setlur et al., 2024）。我们还与 ORM 基线做了比较（附录 F），发现我们的 PRM 始终优于 ORM。因此，本节所有搜索实验都使用 PRM 模型。PRM 训练的更多细节见附录 D。

答案聚合。在测试时，基于过程的验证器可用于为从基座模型采样的一组解答中的每一步打分。为了用 PRM 选出 best-of-N 答案，我们需要一个函数来聚合每个答案的全部逐步得分，以确定正确答案的最佳候选。为此，我们先聚合单个答案各自的逐步得分，得到整个答案的最终得分（步内聚合）；再跨答案聚合以确定最佳答案（答案间聚合）。具体地，我们对步内与答案间聚合的处理如下：

- 步内聚合。我们不用乘积或最小值来聚合逐步得分（Wang et al., 2023；Lightman et al., 2023），而是用 PRM 在最后一步的预测作为整个答案的得分。在我们研究的所有聚合方法中，这一做法表现最好（见附录 E）。
- 答案间聚合。我们遵循 Li et al. (2023)，采用「best-of-N 加权」（best-of-N weighted）选择而非标准 best-of-N。best-of-N 加权选择把验证器对最终答案相同的所有解答的正确性得分做边缘化求和，选出总和最大的最终答案。

### 5.2 针对 PRM 的搜索方法

图 2：*比较不同的 PRM 搜索方法。*左：best-of-N 采样 N 个完整答案，然后按 PRM 最终得分选出最佳答案。中：束搜索在每一步采样 N 个候选，并按 PRM 选出前 M 个继续搜索。右：前瞻搜索把束搜索的每一步扩展为使用 k 步前瞻来评估保留哪些步骤并继续搜索，因此前瞻搜索需要更多计算。

我们在测试时通过搜索方法来优化 PRM。我们研究三种从少样本提示的基座 LLM 采样输出的搜索方法（见附录 G）。图 2 给出了示意。

Best-of-N 加权。我们从基座 LLM 独立采样 N 个答案，然后按 PRM 的最终答案判断选出最佳答案。

束搜索。束搜索通过在 PRM 的逐步预测上搜索来优化 PRM。我们的实现类似于 BFS-V（Yao et al., 2023；Feng et al., 2024）。具体地，我们考虑固定数量的束 $N$ 与束宽 $M$，然后执行以下步骤：

1. 为解答的第一步采样 $N$ 个初始预测
2. 按 PRM 预测的逐步「未来回报」估计为生成的步骤打分（由于此设置中奖励是稀疏的，它也对应前缀的总奖励）
3. 只保留得分最高的前 $N/M$ 个步骤
4. 现在从每个候选出发，为下一步采样 $M$ 个提案，再次得到共 $N/M\times M$ 个候选前缀。然后重复步骤 2-4。

我们运行该算法直到解答结束或达到最大束扩展轮数（我们的设置是 40）。搜索以 N 个最终答案候选收尾，再对其应用上述 best-of-N 加权选择得到最终答案预测。

前瞻搜索。前瞻搜索修改束搜索评估单个步骤的方式。它利用前瞻展开（rollout）来提升搜索过程中每一步 PRM 价值估计的准确性。具体而言，在束搜索的每一步，不再用当前步骤的 PRM 得分来选择头部候选，前瞻搜索执行一次模拟：继续向前展开至多 $k$ 步，若到达解答末尾则提前停止。为降低模拟展开的方差，我们以温度 0 执行展开。展开结束时 PRM 的预测被用来为束搜索中的当前步骤打分。换言之，可以把束搜索视为 $k=0$ 的前瞻搜索特例。给定一个准确的 PRM，增大 $k$ 应当能提升逐步价值估计的准确性，代价是额外计算。还应注意，这一版本的前瞻搜索是 MCTS（Sutton & Barto, 2018）的特例：MCTS 中为促进探索而设计的随机元素被移除了，因为 PRM 已经训练完成并被冻结。这些随机元素对学习价值函数（我们的 PRM 已经学到）大有用处，但在测试时我们想利用而非探索时用处不大。因此，前瞻搜索在很大程度上代表了 MCTS 式方法在测试时的实际使用方式。

图 3：左：*比较针对 PRM 验证器执行搜索的不同方法。*可以看到，在低生成预算下束搜索表现最好，但随着预算进一步扩大，改进逐渐减小，最终落到 best-of-N 基线之下。前瞻搜索在相同生成预算下总体不如其他方法。右：*按难度级别分桶比较束搜索与 best-of-N。*每个难度桶中的四根柱子对应递增的测试时计算预算（4、16、64、256 次生成）。在较容易的问题（桶 1 与 2）上，束搜索在更高预算下出现过优化的迹象，而 best-of-N 没有。在中等难度问题（桶 3 与 4）上，我们看到束搜索相对 best-of-N 有持续改进。

### 5.3 分析结果：验证器搜索的测试时缩放

我们现在给出比较各种搜索算法的结果，并为搜索方法识别一个依赖于提示难度的计算最优缩放策略。

比较搜索算法。我们首先对各种搜索设置做扫描。除标准 best-of-N 方法外，我们扫描了区分不同树搜索方法的两个主要参数：束宽 $M$ 与前瞻步数 $k$。虽然无法穷尽扫描每一个配置，我们在最大预算 256 下扫描了以下设置：

1. 束宽设为 $\sqrt{N}$ 的束搜索，其中 $N$ 为生成预算。
2. 固定束宽为 4 的束搜索。
3. 在束搜索设置 1) 与 2) 上应用 $k=3$ 的前瞻搜索。
4. 在束搜索设置 1) 上应用 $k=1$ 的前瞻搜索。

为了公平地以生成预算为函数比较各搜索方法，我们建立了一套估计每种方法成本的协议。我们把一次生成视为从基座 LLM 采样的一个答案。对束搜索与 best-of-N，生成预算分别对应束数与 $N$。而前瞻搜索使用了额外计算：在搜索的每一步，我们额外向前采样 $k$ 步。因此，我们定义前瞻搜索的成本为 $N\times(k+1)$ 个样本。

结果。如图 3（左）所示，在较小的生成预算下，束搜索显著优于 best-of-N。然而随着预算扩大，这些改进大幅缩水，束搜索常常落到 best-of-N 基线之下。我们还看到，前瞻搜索在相同生成预算下总体不如其他方法，原因很可能是模拟前瞻展开引入的额外计算。搜索收益递减很可能源于对 PRM 预测的过度利用（exploit）。例如，我们看到一些实例（如图 29），搜索导致模型在解答末尾生成低信息量的重复步骤。在另一些情形中，我们发现过度优化搜索会产生只有 1-2 步的过短解答。这解释了为什么最强大的搜索方法（即前瞻搜索）表现最差。我们在附录 M 中收录了若干由搜索发现的此类例子。

搜索改进了哪些问题？为理解如何计算最优地扩展搜索方法，我们现在做难度分桶分析。具体而言，我们比较束搜索（$M=4$）与 best-of-N。在图 3（右）中我们看到，虽然在总体上束搜索与 best-of-N 在高生成预算下表现相近，但按难度桶评估其效能揭示了截然不同的趋势。在简单问题（级别 1 与 2）上，两者中更强的优化器——束搜索——的性能随生成预算增加而退化，显示出利用 PRM 信号的迹象。相比之下，在较难的问题（级别 3 与 4）上，束搜索持续优于 best-of-N。在最困难的问题（级别 5）上，任何方法都没有多大实质性进展。

这些发现与直觉相符：我们可以预期，在简单问题上验证器对正确性的判断大体正确。因此，通过束搜索进一步优化，只会进一步放大验证器学到的任何虚假特征，导致性能退化。而在更困难的问题上，基座模型本来就不太可能一次性采样到正确答案，因此搜索可以帮助引导模型更频繁地给出正确答案。

图 4：*在 PRM 搜索中比较计算最优测试时计算分配与各基线。*通过按题目难度的概念扩展测试时计算，我们发现最多可以用少 4 倍的测试时计算（例如 16 对 64 次生成）几乎胜过 PRM best-of-N。「Compute-optimal oracle」指使用由标准正确性信息导出的 oracle 难度桶，「compute-optimal predicted」指使用 PRM 的预测生成难度桶。可以看到，两类难度桶的曲线基本重合。

计算最优搜索。基于上述结果，题目难度显然可以成为预测给定计算预算下最优搜索策略的有用统计量。此外，最优搜索策略的选择会随该难度统计量剧烈变化。因此我们在图 4 中可视化「计算最优」缩放趋势，即每个难度级别上表现最好的搜索策略。可以看到，在低生成预算区间，无论使用 oracle 还是预测难度，计算最优缩放都最多可以用少 *4 倍*的测试时计算几乎胜过 best-of-N（例如 16 对 64 次生成）。而在较高预算区间，使用预测难度时部分收益缩水；但使用 oracle 桶时，我们仍能看到最优扩展测试时计算带来的持续改进。这一结果展示了在搜索期间自适应分配测试时计算所能获得的性能增益。

验证器计算最优扩展的要点

我们发现任何给定验证器搜索方法的效能都关键取决于计算预算与手头问题。具体而言，束搜索在较难问题与较低计算预算下更有效，而 best-of-N 在较容易问题与更高预算下更有效。此外，通过为给定题目难度与测试时计算预算选择最佳搜索设置，我们最多可以用少 *4 倍*的测试时计算几乎胜过 best-of-N。

## 6 精炼提议分布

到目前为止，我们研究了针对验证器搜索的测试时计算缩放性质。现在转向研究修改提议分布（第 2 节）的缩放性质。具体而言，我们让模型迭代地修订自己的答案，使模型得以在测试时动态改进自身的分布。单纯提示现有 LLM 纠正自己的错误，在推理问题上基本无法带来性能提升（Huang et al., 2023）。因此，我们在 Qu et al. (2024b) 给出的配方基础上，针对我们的设置做了一些修改，微调语言模型使其迭代地修订自己的答案。我们先描述如何训练与使用「通过顺序地以自己先前对该题的尝试为条件来精炼自身提议分布」的模型，然后分析修订模型的推理时缩放性质。

图 5：*并行采样（如 best-of-N）与顺序修订对比。*左：并行采样相互独立地并行生成 N 个答案，而顺序修订在前次尝试的条件下逐个生成。右：在顺序与并行两种情形中，我们都可以用验证器确定 best-of-N 答案（例如通过应用 best-of-N 加权）。我们也可以把一部分预算分配给并行、一部分给顺序，从而有效地组合这两种采样策略。在这种情形下，我们先用验证器在每条顺序链内选出最佳答案，再跨链选出最佳答案。

### 6.1 设置：训练与使用修订模型

我们微调修订模型的过程与 Qu et al. (2024b) 类似，但引入了一些关键差异。微调时，我们需要由「一串错误答案后跟一个正确答案」组成的轨迹，然后对其执行 SFT。理想情况下，我们希望正确答案与上下文中提供的错误答案*相关*，以便有效教会模型*隐式*识别上下文示例中的错误，随后通过做编辑来纠正这些错误，而不是完全无视上下文示例、从头再试。

生成修订数据。Qu et al. (2024b) 获取多轮展开的按策略（on-policy）方法已被证明有效，但由于运行多轮展开的计算成本，在我们的基础设施中并不完全可行。因此，我们以更高温度*并行*采样 64 个回答，并事后从这些独立样本构造多轮展开。具体而言，按照文献 [1]（Training revision models with synthetic data, 2024，即将发布）的配方，我们把每个正确答案与来自该集合的一串错误答案配对作为上下文，构造多轮微调数据。上下文中最多包含四个错误答案，上下文中解答的具体数量从 0 到 4 的均匀分布中随机抽取。我们使用字符编辑距离度量来优先选择与最终正确答案相关的错误答案（见附录 H）。注意，token 编辑距离并非完美相关性度量，但我们发现这一启发式足以让上下文中的错误答案与正确的目标答案相关联，从而训练出有意义的修订模型，而不是把不相关联的错误与正确回答随机配对。

在推理时使用修订。给定微调好的修订模型，我们在测试时可以从模型采样一串修订。虽然我们的修订模型只用最多四个先前答案的上下文训练，但可以通过把上下文截断到最近的四个修订回答来采样更长的链。在图 6（左）中，我们看到随着从修订模型采样更长的链，模型每一步的 pass@1 逐渐改善，表明我们能够有效地教会模型从上下文中先前答案所犯的错误中学习。

图 6：左：*我们的修订模型在每个修订步的 pass@1。*每经过一次修订 pass@1 逐步改善，甚至在其训练所用 4 个修订步之外仍在改善。我们通过对测试集每道题的 4 条长度为 64 的修订轨迹的表现取平均来估计每步的 pass@1。右：*从修订模型顺序采样与并行采样对比。*比较并行生成 N 个初始回答与用该模型顺序生成 N 次修订的表现。当同时使用验证器与多数投票来选择答案时，用修订模型顺序生成回答略优于并行生成。

话虽如此，推理时存在分布偏移：模型只在上下文含错误答案的序列上训练，但测试时模型可能采样到正确答案并进入上下文。此时，它可能在下一个修订步中偶然把正确答案改成错误答案。我们发现，确实与 Qu et al. (2024b) 类似，使用朴素方法时约 38% 的正确答案会被我们的修订模型改回错误答案。因此，我们采用基于顺序多数投票或基于验证器选择的机制，从模型做出的修订序列中选出最正确的答案（见图 5）以产出最佳答案。

比较。为测试通过修订修改提议分布的效能，我们对「顺序采样 N 次修订」与「并行采样 N 次尝试」的表现设置了公平比较。我们在图 6（右）看到，无论使用基于验证器还是基于多数的选择机制，顺序采样解答都优于并行采样。

![Refer to caption](2408.03314v1/revisions_varing_ratio_and_with_difficulty.png)

图 7：左：*改变分配给顺序修订与并行样本的生成预算比例。*每条线表示一个固定生成预算下随比例变化的结果。我们用验证器选择答案。可以看到，虽然增加顺序修订往往优于更多并行计算，但在较高生成预算下存在一个在两个极端之间取得平衡的理想比例。右：*生成预算为 128 时按难度桶改变顺序与并行比例。*使用基于验证器的选择，我们看到较容易的问题以全部顺序计算取得最佳表现；而在较难的问题上，存在一个理想的顺序与并行测试时计算之比。

### 6.2 分析结果：修订的测试时缩放

我们此前看到顺序提出答案优于并行提出。然而，顺序与并行采样可能具有不同性质。并行采样答案更像一种全局搜索过程，原则上可以覆盖许多完全不同的解题路径——例如不同候选可能采用完全不同的高层方法。顺序采样则更像一种局部精炼过程，修订已经多少在正确轨道上的回答。由于这些互补的收益，我们应当在这两个极端之间取得平衡：把推理时预算的一部分分配给并行采样（例如 $\sqrt{N}$），其余分配给顺序修订（例如 $\sqrt{N}$）。我们现在将证明顺序与并行采样之间存在一个计算最优比例，并基于给定提示的难度理解它们各自的优劣。

权衡顺序与并行测试时计算。为理解如何最优分配顺序与并行计算，我们对多个不同比例做了扫描。我们在图 7（左）中看到，在给定生成预算下确实存在一个能达到最大准确率的理想顺序与并行比例。我们在图 7（右）中还看到，理想的顺序与并行比例随给定题目难度而变化。特别地，简单问题从顺序修订中获益更多，而在困难问题上，在顺序与并行计算之间取得平衡才是最优。这一发现支持了如下假设：顺序修订（即改变提议分布）与并行采样（即用验证器搜索）是扩展测试时计算的两条互补轴线，逐提示地组合使用可能更有效。我们在附录 L 中收录了我们模型生成的一些例子。附加结果见附录 B。

图 8：*用我们的修订模型比较计算最优测试时计算分配与并行计算基线。*通过按题目难度最优地扩展测试时计算，我们发现最多可以用少 *4 倍*的测试时计算（例如 64 对 256 个样本）胜过 best-of-N。「Compute-optimal oracle」指使用由标准正确性信息导出的 oracle 难度桶，「compute-optimal predicted」指用 PRM 的预测生成模型预测难度桶。

计算最优修订。鉴于顺序与并行采样的效能取决于题目难度，我们可以为每个难度桶选择理想的顺序与并行计算比例。在图 8 中，我们绘制了同时使用 oracle 与预测两种难度概念时这一计算最优缩放策略的结果。两种情形下，我们都通过修订改进提议分布，大幅改善了测试时计算的扩展。特别地，我们看到在较高生成预算下并行采样似乎进入平台期，而计算最优缩放展现了持续改进。无论 oracle 还是预测难度桶，计算最优缩放都最多可以用少 *4 倍*的测试时计算（例如 64 对 256 个样本）胜过 best-of-N。总体而言，这些结果展示了逐提示地调整提议分布以改进测试时计算扩展的潜力。

通过修订精炼提议分布实现计算最优扩展的要点

我们发现顺序（如修订）与并行（如标准 best-of-N）测试时计算之间存在权衡，理想的顺序与并行测试时计算比例关键取决于计算预算与手头具体问题。具体而言，较容易的问题受益于纯顺序的测试时计算，而较难的问题往往在某个理想的顺序与并行之比下表现最佳。此外，通过为给定题目难度与测试时计算预算选择最佳设置，我们最多可以用少 *4 倍*的测试时计算胜过并行 best-of-N 基线。

## 7 综合起来：交换预训练与测试时计算

到目前为止，我们看到利用额外的测试时计算可以使我们表示出比基座 LLM 自身预测的分布更复杂的分布，从而提升性能。我们现在提出假设：这种表示分布的更大灵活性意味着，额外的测试时计算可以弥补更高容量模型或预训练更多 FLOPs 的缺失。本节*研究这在多大程度上可行*。我们提出以下问题：

问题：交换预训练与测试时计算

假设一个模型用 $X$ FLOPs 完成预训练，且我们计划用该模型运行 $Y$ FLOPs 的推理。如果想把总 FLOPs 预算扩大 $M$ 倍以提升性能（即预训练与推理合计 $M(X+Y)$ FLOPs），我们应当把 FLOPs 花在增加预训练计算上，还是花在额外测试时计算上？

增加预训练 FLOPs 引入了额外的设计决策：把计算分配给更多数据还是更多参数（Hoffmann et al., 2022）。我们聚焦于放大模型参数、固定训练数据量的设置，这与开源 LLaMA 系列模型的做法一致（Touvron et al., 2023）。我们选择这一设置，是因为它代表了扩展预训练计算的一种典型做法，而把数据与参数同等缩放的计算最优预训练计算扩展分析（Sardana & Frankle, 2023）留作未来工作。

定义 FLOPs 之间的兑换率。我们现在描述如何定义预训练与推理 FLOPs 之间的兑换率。为确定预训练 FLOPs，我们使用常见近似 $X=6ND_{\text{pretrain}}$（Hoffmann et al., 2022）；为确定推理 FLOPs，我们使用 $Y=2ND_{\text{inference}}$（Sardana & Frankle, 2023）。这里 $N$ 表示模型参数，$D_{\text{pretrain}}$ 是预训练使用的 token 数，$D_{\text{inference}}$ 是推理时生成的总 token 数。借助这些近似可以看出，若把模型参数乘以 $M$，则预训练与推理 FLOPs（后者因更大模型贪心解码的成本）都增长 $M$ 倍（合计 $M(X+Y)$ FLOPs）。

![Refer to caption](2408.03314v1/comparing_test_pretrain_v8.png)

图 9：*FLOPs 对齐评估中预训练与测试时计算的权衡。*每条线表示在各个 oracle 难度桶中用我们的计算最优策略扩展测试时计算的表现。左为修订结果，右为搜索结果。星号表示一个参数量约多 14 倍的基座模型贪心 pass@1 的表现。x 轴为测试时计算预算，星号被放在 x 轴上三个不同位置，分别对应三种不同推理计算负载下（例如 $R=\frac{D_{\text{inference}}}{D_{\text{pretrain}}}$）扩展参数与扩展测试时计算的 FLOPs 等价比较点。若星号位于线下方，意味着用测试时计算比扩展模型参数更有效；若星号位于线上方，则意味着扩展参数更有效。可以看到，在简单问题上或在推理负载较低的设置中（如 $R\ll 1$），测试时计算通常能胜过扩展模型参数。然而在较难问题上或推理负载较高的设置中（如 $R\gg 1$），预训练是提升性能更有效的途径。

为用较小模型的测试时计算匹配放大模型参数的 FLOPs，我们可以把较小模型的推理计算乘以因子 $M+3\left(\frac{D_{\text{pretrain}}}{D_{\text{inference}}}\right)(M-1)$。值得注意的是，可用于匹配较大模型 FLOPs 的推理计算量取决于比值 $\frac{D_{\text{pretrain}}}{D_{\text{inference}}}$。我们把该比值的倒数记为 $R$（即 $\frac{D_{\text{inference}}}{D_{\text{pretrain}}}$）。取决于具体的生产设置或用例，$R$ 的取值可能大不相同。特别地，在许多大规模生产设置中，推理 token 可能显著多于预训练 token，此时 $R\gg 1$。另一方面，在许多当代用测试时计算改进模型的自我改进设置中，生成的推理 token 很可能显著少于预训练 token，即 $R\ll 1$。因此，由于我们能施加的测试时计算规模依赖这一比值，我们预期结论会因具体设置而异。

在图 9 中，我们用这种交换测试时与预训练计算的方法，把我们的计算最优扩展与参数量放大约 14 倍的模型做比较。我们对 3 个不同的 $R$ 值做比较：0.16（$R\ll 1$）、0.79（$R\sim 1$）与 22（$R\gg 1$），每个比值对应一个推理预算。可以看到，如果我们只预期遇到非常困难的问题（如难度桶 4/5）或 $D_{\text{inference}}$ 较大（对应更大的 $R$ 值），那么把预算分配给预训练往往更有效（如星号位于线上方）。反之，如果我们预期大多是简单或中等难度问题（如桶 1/2/3，有时是 4）或推理需求较低（如自我改进流水线的情形），那么利用测试时计算更好。

交换预训练与测试时计算的要点

测试时计算与预训练计算并非一对一「可互换」。在模型能力范围内的简单与中等问题上，或在推理需求小的设置中，测试时计算可以轻松弥补额外预训练。然而，在超出给定基座模型能力的挑战性问题上，或在更高推理需求下，预训练很可能更有利于提升性能。

## 8 讨论与未来工作

在本工作中，我们深入分析了「针对验证器搜索」与「精炼 LLM 提议分布」这两类旨在扩展数学推理测试时计算的技术各自的效能。总体而言，我们发现给定方法的效能与问题难度（从基座 LLM 能力的视角看）高度相关。这促使我们提出测试时计算的「计算最优」扩展概念，它给出一种自适应、依赖提示的策略，以在给定测试时计算预算下提升性能。通过应用这样的计算最优缩放策略，我们发现可以把测试时计算扩展的效率提升 2-4 倍。在 FLOPs 对齐的设置中，把额外测试时计算的收益与额外预训练计算的收益相比较，我们首次表明：用看似简单的方法（即修订与搜索）使用测试时计算，已经可以在某些类型的提示上良好扩展，相对把这些 FLOPs 花在预训练上更有收益。话虽如此，我们的研究也存在一些局限，未来工作可以着手解决。

进一步改进测试时计算扩展。本工作中我们聚焦于改进两种主要机制的测试时计算扩展：验证器与（通过修订实现的）提议分布。虽然我们在第 6 节把验证器与修订结合了起来，但没有实验把 PRM 树搜索技术与修订结合，也没有研究批评并修订（Madaan et al., 2023）等其他技术。未来工作应当研究如何组合这些多种方法以进一步改进测试时计算扩展。此外，我们发现这些方案在困难问题上普遍收益甚微；未来工作应致力于开发能绕过这一限制的、使用测试时计算的新方式。

快速评估题目难度。我们用题目难度这一简单的充分统计量来近似计算最优测试时缩放策略。虽然这一方案有效，但估计我们的难度概念本身就需要施加不可忽略的测试时计算。未来工作应考虑更高效估计题目难度的替代方式（例如通过预训练或微调模型直接预测一道题的难度），或在评估难度与尝试解题之间动态切换。

交错测试时与训练时计算。本工作纯粹聚焦测试时计算的扩展以及测试时计算可换取额外预训练的程度。然而我们设想，未来施加额外测试时计算的输出可以被蒸馏回基座 LLM，从而形成一个在开放式自然语言上运行的迭代自我改进循环。为此，未来工作应扩展我们的发现，研究如何利用应用测试时计算的输出改进基座 LLM 本身。

## 致谢

我们感谢 Yi Su、Rishabh Agarwal、Yinlam Chow、Aleksandra Faust、Vincent Zhuang、George Tucker、Hao Liu、Jiayi Pan、Ethan Dyer、Behnam Neyshabur、Xavier Garcia、Yamini Bansal、Lampros Lamprou、Yuxiao Qu 和 Amrith Setlur 对本文早期版本的反馈与讨论。我们将文献 [1] 中关于「成对样本生成训练修订模型」与「基于编辑距离的采样」的想法与实验归功并感谢 Rishabh Agarwal、Vincent Zhuang、Yi Su 和 Avi Singh，以及与其的讨论。我们感谢 Slav Petrov 的领导支持。

## 参考文献

- [1]

  Training revision models with synthetic data.
  Coming soon, 2024.
- [2]

  C. Andrieu, N. De Freitas, A. Doucet, and M. I. Jordan.
  An introduction to mcmc for machine learning.
  2003.
- [3]

  R. Anil, A. M. Dai, O. Firat, M. Johnson, D. Lepikhin, A. Passos, S. Shakeri, E. Taropa, P. Bailey, Z. Chen, E. Chu, J. H. Clark, L. E. Shafey, Y. Huang, K. Meier-Hellstern, G. Mishra, E. Moreira, M. Omernick, K. Robinson, S. Ruder, Y. Tay, K. Xiao, Y. Xu, Y. Zhang, G. H. Abrego, J. Ahn, J. Austin, P. Barham, J. Botha, J. Bradbury, S. Brahma, K. Brooks, M. Catasta, Y. Cheng, C. Cherry, C. A. Choquette-Choo, A. Chowdhery, C. Crepy, S. Dave, M. Dehghani, S. Dev, J. Devlin, M. Díaz, N. Du, E. Dyer, V. Feinberg, F. Feng, V. Fienber, M. Freitag, X. Garcia, S. Gehrmann, L. Gonzalez, G. Gur-Ari, S. Hand, H. Hashemi, L. Hou, J. Howland, A. Hu, J. Hui, J. Hurwitz, M. Isard, A. Ittycheriah, M. Jagielski, W. Jia, K. Kenealy, M. Krikun, S. Kudugunta, C. Lan, K. Lee, B. Lee, E. Li, M. Li, W. Li, Y. Li, J. Li, H. Lim, H. Lin, Z. Liu, F. Liu, M. Maggioni, A. Mahendru, J. Maynez, V. Misra, M. Moussalem, Z. Nado, J. Nham, E. Ni, A. Nystrom, A. Parrish, M. Pellat, M. Polacek, A. Polozov, R. Pope, S. Qiao, E. Reif, B. Richter,
  P. Riley, A. C. Ros, A. Roy, B. Saeta, R. Samuel, R. Shelby, A. Slone, D. Smilkov, D. R. So, D. Sohn, S. Tokumine, D. Valter, V. Vasudevan, K. Vodrahalli, X. Wang, P. Wang, Z. Wang, T. Wang, J. Wieting, Y. Wu, K. Xu, Y. Xu, L. Xue, P. Yin, J. Yu, Q. Zhang, S. Zheng, C. Zheng, W. Zhou, D. Zhou, S. Petrov, and Y. Wu.
  Palm 2 technical report, 2023.
- [4]

  Y. Bai, S. Kadavath, S. Kundu, A. Askell, J. Kernion, A. Jones, A. Chen, A. Goldie, A. Mirhoseini, C. McKinnon, C. Chen, C. Olsson, C. Olah, D. Hernandez, D. Drain, D. Ganguli, D. Li, E. Tran-Johnson, E. Perez, J. Kerr, J. Mueller, J. Ladish, J. Landau, K. Ndousse, K. Lukosuite, L. Lovitt, M. Sellitto, N. Elhage, N. Schiefer, N. Mercado, N. DasSarma, R. Lasenby, R. Larson, S. Ringer, S. Johnston, S. Kravec, S. E. Showk, S. Fort, T. Lanham, T. Telleen-Lawton, T. Conerly, T. Henighan, T. Hume, S. R. Bowman, Z. Hatfield-Dodds, B. Mann, D. Amodei, N. Joseph, S. McCandlish, T. Brown, and J. Kaplan.
  Constitutional ai: Harmlessness from ai feedback, 2022.
- [5]

  C. Blakeney, M. Paul, B. W. Larsen, S. Owen, and J. Frankle.
  Does your data spark joy? performance gains from domain upsampling at the end of training, 2024.
  URL <https://arxiv.org/abs/2406.03476>.
- [6]

  G. Chen, M. Liao, C. Li, and K. Fan.
  Alphamath almost zero: process supervision without process, 2024.
- [7]

  K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, C. Hesse, and J. Schulman.
  Training verifiers to solve math word problems, 2021.
- [8]

  Y. Du, S. Li, A. Torralba, J. B. Tenenbaum, and I. Mordatch.
  Improving factuality and reasoning in language models through multiagent debate, 2023.
- [9]

  J. S. B. T. Evans.
  Heuristic and analytic processes in reasoning.
  *British Journal of Psychology*, 75(4):451–468, 1984.
- [10]

  X. Feng, Z. Wan, M. Wen, S. M. McAleer, Y. Wen, W. Zhang, and J. Wang.
  Alphazero-like tree-search can guide large language model decoding and training, 2024.
- [11]

  L. Gao, A. Madaan, S. Zhou, U. Alon, P. Liu, Y. Yang, J. Callan, and G. Neubig.
  Pal: Program-aided language models, 2023.
  URL <https://arxiv.org/abs/2211.10435>.
- [12]

  S. Goyal, Z. Ji, A. S. Rawat, A. K. Menon, S. Kumar, and V. Nagarajan.
  Think before you speak: Training language models with pause tokens, 2024.
  URL <https://arxiv.org/abs/2310.02226>.
- [13]

  D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt.
  Measuring mathematical problem solving with the math dataset, 2021.
- [14]

  J. Hoffmann, S. Borgeaud, A. Mensch, E. Buchatskaya, T. Cai, E. Rutherford, D. de Las Casas, L. A. Hendricks, J. Welbl, A. Clark, T. Hennigan, E. Noland, K. Millican, G. van den Driessche, B. Damoc, A. Guy, S. Osindero, K. Simonyan, E. Elsen, J. W. Rae, O. Vinyals, and L. Sifre.
  Training compute-optimal large language models, 2022.
- [15]

  J. Huang, X. Chen, S. Mishra, H. S. Zheng, A. W. Yu, X. Song, and D. Zhou.
  Large language models cannot self-correct reasoning yet, 2023.
- [16]

  A. L. Jones.
  Scaling scaling laws with board games, 2021.
  URL <https://arxiv.org/abs/2104.03113>.
- [17]

  D. Kahneman.
  Maps of bounded rationality: Psychology for behavioral economics.
  *The American Economic Review*, 93(5):1449–1475, 2003.
- [18]

  D. Kahneman.
  *Thinking, fast and slow*.
  Farrar, Straus and Giroux, New York, first paperback edition edition, 2013.
- [19]

  L. Kocsis and C. Szepesv’ari.
  Bandit based monte-carlo planning.
  In *European conference on machine learning*, pages 282–293. Springer, 2006.
- [20]

  A. Lewkowycz, A. Andreassen, D. Dohan, E. Dyer, H. Michalewski, V. Ramasesh, A. Slone, C. Anil, I. Schlag, T. Gutman-Solo, Y. Wu, B. Neyshabur, G. Gur-Ari, and V. Misra.
  Solving quantitative reasoning problems with language models, 2022.
- [21]

  Y. Li, Z. Lin, S. Zhang, Q. Fu, B. Chen, J.-G. Lou, and W. Chen.
  Making large language models better reasoners with step-aware verifier, 2023.
- [22]

  H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe.
  Let’s verify step by step, 2023.
- [23]

  A. Madaan, N. Tandon, P. Gupta, S. Hallinan, L. Gao, S. Wiegreffe, U. Alon, N. Dziri, S. Prabhumoye, Y. Yang, S. Gupta, B. P. Majumder, K. Hermann, S. Welleck, A. Yazdanbakhsh, and P. Clark.
  Self-refine: Iterative refinement with self-feedback, 2023.
- [24]

  N. McAleese, R. Pokorny, J. F. Cerón Uribe, E. Nitishinskaya, M. Trębacz, and J. Leike.
  Llm critics help catch llm bugs.
  *OpenAI*, 2024.
- [25]

  OpenAI.
  Gpt-4 technical report, 2024.
- [26]

  Y. Qin, S. Liang, Y. Ye, K. Zhu, L. Yan, Y. Lu, Y. Lin, X. Cong, X. Tang, B. Qian, S. Zhao, L. Hong, R. Tian, R. Xie, J. Zhou, M. Gerstein, D. Li, Z. Liu, and M. Sun.
  Toolllm: Facilitating large language models to master 16000+ real-world apis, 2023.
  URL <https://arxiv.org/abs/2307.16789>.
- [27]

  C. Qu, S. Dai, X. Wei, H. Cai, S. Wang, D. Yin, J. Xu, and J.-R. Wen.
  Tool learning with large language models: A survey, 2024a.
  URL <https://arxiv.org/abs/2405.17935>.
- [28]

  Y. Qu, T. Zhang, N. Garg, and A. Kumar.
  Recursive introspection: Teaching foundation models how to self-improve.
  2024b.
- [29]

  N. Sardana and J. Frankle.
  Beyond chinchilla-optimal: Accounting for inference in language model scaling laws, 2023.
- [30]

  W. Saunders, C. Yeh, J. Wu, S. Bills, L. Ouyang, J. Ward, and J. Leike.
  Self-critiquing models for assisting human evaluators, 2022.
- [31]

  A. Setlur, S. Garg, X. Geng, N. Garg, V. Smith, and A. Kumar.
  Rl on incorrect synthetic data scales the efficiency of llm math reasoning by eight-fold.
  *arXiv preprint arXiv:2406.14532*, 2024.
- [32]

  Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, X. Bi, H. Zhang, M. Zhang, Y. K. Li, Y. Wu, and D. Guo.
  Deepseekmath: Pushing the limits of mathematical reasoning in open language models, 2024.
- [33]

  A. Sharma, S. Keh, E. Mitchell, C. Finn, K. Arora, and T. Kollar.
  A critical evaluation of ai feedback for aligning large language models, 2024.
  URL <https://arxiv.org/abs/2402.12366>.
- [34]

  N. Shinn, F. Cassano, E. Berman, A. Gopinath, K. Narasimhan, and S. Yao.
  Reflexion: Language agents with verbal reinforcement learning, 2023.
- [35]

  A. Singh, J. D. Co-Reyes, R. Agarwal, A. Anand, P. Patil, X. Garcia, P. J. Liu, J. Harrison, J. Lee, K. Xu, A. Parisi, A. Kumar, A. Alemi, A. Rizkowsky, A. Nova, B. Adlam, B. Bohnet, G. Elsayed, H. Sedghi, I. Mordatch, I. Simpson, I. Gur, J. Snoek, J. Pennington, J. Hron, K. Kenealy, K. Swersky, K. Mahajan, L. Culp, L. Xiao, M. L. Bileschi, N. Constant, R. Novak, R. Liu, T. Warkentin, Y. Qian, Y. Bansal, E. Dyer, B. Neyshabur, J. Sohl-Dickstein, and N. Fiedel.
  Beyond human data: Scaling self-training for problem-solving with language models, 2024.
- [36]

  C. Snell, E. Wallace, D. Klein, and S. Levine.
  Predicting emergent capabilities by finetuning.
  *Conference on Language Modeling 2024*, 2024.
- [37]

  K. Stechly, M. Marquez, and S. Kambhampati.
  Gpt-4 doesn’t know it’s wrong: An analysis of iterative prompting for reasoning problems, 2023.
- [38]

  R. S. Sutton and A. G. Barto.
  *Reinforcement learning: An introduction*.
  Second edition, 2018.
- [39]

  G. Team.
  Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context, 2024.
- [40]

  Y. Tian, B. Peng, L. Song, L. Jin, D. Yu, H. Mi, and D. Yu.
  Toward self-improvement of llms via imagination, searching, and criticizing, 2024.
- [41]

  H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei, N. Bashlykov, S. Batra, P. Bhargava, S. Bhosale, D. Bikel, L. Blecher, C. C. Ferrer, M. Chen, G. Cucurull, D. Esiobu, J. Fernandes, J. Fu, W. Fu, B. Fuller, C. Gao, V. Goswami, N. Goyal, A. Hartshorn, S. Hosseini, R. Hou, H. Inan, M. Kardas, V. Kerkez, M. Khabsa, I. Kloumann, A. Korenev, P. S. Koura, M.-A. Lachaux, T. Lavril, J. Lee, D. Liskovich, Y. Lu, Y. Mao, X. Martinet, T. Mihaylov, P. Mishra, I. Molybog, Y. Nie, A. Poulton, J. Reizenstein, R. Rungta, K. Saladi, A. Schelten, R. Silva, E. M. Smith, R. Subramanian, X. E. Tan, B. Tang, R. Taylor, A. Williams, J. X. Kuan, P. Xu, Z. Yan, I. Zarov, Y. Zhang, A. Fan, M. Kambadur, S. Narang, A. Rodriguez, R. Stojnic, S. Edunov, and T. Scialom.
  Llama 2: Open foundation and fine-tuned chat models, 2023.
  URL <https://arxiv.org/abs/2307.09288>.
- [42]

  J. Uesato, N. Kushman, R. Kumar, F. Song, N. Siegel, L. Wang, A. Creswell, G. Irving, and I. Higgins.
  Solving math word problems with process- and outcome-based feedback, 2022.
- [43]

  K. Valmeekam, M. Marquez, and S. Kambhampati.
  Can large language models really improve by self-critiquing their own plans?, 2023.
- [44]

  P. Villalobos and D. Atkinson.
  Trading off compute in training and inference, 2023.
  URL <https://epochai.org/blog/trading-off-compute-in-training-and-inference>.
  Accessed: 2024-07-03.
- [45]

  P. Wang, L. Li, Z. Shao, R. X. Xu, D. Dai, Y. Li, D. Chen, Y. Wu, and Z. Sui.
  Math-shepherd: Verify and reinforce llms step-by-step without human annotations, 2023.
- [46]

  R. Wang, E. Zelikman, G. Poesia, Y. Pu, N. Haber, and N. D. Goodman.
  Hypothesis search: Inductive reasoning with language models, 2024.
  URL <https://arxiv.org/abs/2309.05660>.
- [47]

  J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. Chi, Q. Le, and D. Zhou.
  Chain-of-thought prompting elicits reasoning in large language models, 2023.
- [48]

  S. Yao, D. Yu, J. Zhao, I. Shafran, T. L. Griffiths, Y. Cao, and K. Narasimhan.
  Tree of thoughts: Deliberate problem solving with large language models, 2023.
- [49]

  Z. Yuan, H. Yuan, C. Li, G. Dong, K. Lu, C. Tan, C. Zhou, and J. Zhou.
  Scaling relationship on learning mathematical reasoning with large language models, 2023.
- [50]

  E. Zelikman, Y. Wu, J. Mu, and N. D. Goodman.
  Star: Bootstrapping reasoning with reasoning, 2022.
- [51]

  E. Zelikman, G. Harik, Y. Shao, V. Jayasiri, N. Haber, and N. D. Goodman.
  Quiet-star: Language models can teach themselves to think before speaking, 2024.
  URL <https://arxiv.org/abs/2403.09629>.

## 附录

### 附录 A 相关工作

语言模型推理。近年来，语言模型在具有挑战性的数学推理任务上的表现迅速提升（Lewkowycz et al., 2022；Team, 2024；OpenAI, 2024；Shao et al., 2024；Lightman et al., 2023）。这些改进可归因于四个主要因素：1) 在以数学为主的大型语料上做持续预训练（Lewkowycz et al., 2022；Team, 2024；Shao et al., 2024；Lightman et al., 2023）；2) 改进 LLM 提议分布，要么通过用 RL 微调对特定推理任务施加针对性优化（Singh et al., 2024；Zelikman et al., 2022；Shao et al., 2024；Yuan et al., 2023），要么让模型迭代地批评并修订自己的答案（Bai et al., 2022；Madaan et al., 2023；Du et al., 2023；Saunders et al., 2022）；3) 通过微调验证器使 LLM 受益于额外测试时计算（Lightman et al., 2023；Cobbe et al., 2021；Uesato et al., 2022；Wang et al., 2023；Yao et al., 2023；Feng et al., 2024；Chen et al., 2024；Tian et al., 2024）。我们的工作建立在第二与第三条研究线之上，分析测试时计算扩展可通过 1) 精炼 LLM 提议分布与 2) 针对验证器搜索 得到多大改进。

分析测试时计算扩展。Jones (2021) 曾用应用于棋类游戏 Hex 的蒙特卡洛树搜索研究训练时与测试时计算的权衡。我们则把分析聚焦在全规模语言模型数学推理问题上。Villalobos & Atkinson (2023) 的调研工作分析了多个领域中训练与推理之间的权衡，但其语言模型分析大多聚焦于标准答案已知设置下的测试时计算扩展。相比之下，我们的分析聚焦标准答案未知的设置。此外，强化学习文献中已有不少方法（如 MCTS（Kocsis & Szepesvári, 2006））旨在驾驭测试时与训练时计算之间的权衡，以实现某种迭代自博弈。我们工作中的发现可用来帮助开发能在开放式自然语言上运行的类似算法。

用测试时计算增强 LLM。除验证器与修订外，还有若干工作提出了让 LM 利用测试时计算进行推理的其他方法。例如，Wang et al. (2024) 执行分层假设搜索以实现归纳推理能力。许多相关工作提出在测试时为语言模型配备工具，这可以大幅提升其在下游任务上的表现（Gao et al., 2023；Qin et al., 2023；Qu et al., 2024a）。最后，若干工作提出了以无监督方式学习思考 token 的方法（Zelikman et al., 2024；Goyal et al., 2024），使模型能更有效地利用采样更长序列带来的额外测试时计算。虽然本工作聚焦于扩展测试时计算的两条主要机制（如验证器与修订），但我们开展分析的许多方法（例如按题目难度做计算最优扩展）原则上也可应用于任何其他扩展测试时计算的方法，我们相信这是未来研究一个有趣的方向。

### 附录 B 附加修订结果

我们在图 10 中绘制了用我们的 PaLM 2-S* 修订模型做多数选择的附加结果。采用多数选择时，我们看到与验证器选择的图 7 基本相似的趋势。

![Refer to caption](2408.03314v1/iso_gens_majority_difficulty.png)

图 10：改变分配给顺序与并行样本的生成预算比例，用多数投票（而非验证器）选择答案。左：每条线表示一个固定生成预算下随比例变化的结果。可以看到与验证器情形类似，多数投票情形下在给定预算也存在一个理想的顺序与并行测试时计算比例。右：按难度桶分析表现，可以看到较容易的问题对顺序与并行之比基本不敏感，而在较难的问题上存在一个理想的顺序与并行测试时计算比例。

### 附录 C 无监督难度桶

我们在不使用 oracle 标准正确性信息的情况下计算难度桶：对每道题在 2048 个样本上取 PRM 最终答案得分的平均，得到对应于该题的价值估计。然后我们把测试集中每道题的该值分成五个五分位桶（与 oracle 难度桶使用相同流程）。我们称之为「预测难度」而非「oracle 难度」。从技术上讲，这一流程代价极高，因为它需要生成大量样本。虽然我们的分析未计入这一成本，但在实际生产环境中，这一成本会是个问题。一种更高效的做法是微调一个模型，直接根据题目预测正确性。我们没有在本工作中探索这一点，把这种更廉价的难度估计方法的探索留作未来工作。

在图 12 中，我们绘制了使用我们的难度桶的 PRM 搜索结果；在图 11 中，我们绘制了相应的修订结果。可以看到，在这两种设置下，这些预测桶都展现出与 oracle 桶相似的趋势。

![Refer to caption](2408.03314v1/bon_unsupervised_difficulty_output.png)

![Refer to caption](2408.03314v1/maj_unsupervised_difficulty_output.png)

图 11：用我们的 PaLM 2-S* PRM 在不使用标准正确性信息的情况下为修订计算难度桶。左为验证器选择，右为多数选择。可以看到，这些桶的表现趋势与图 7 和图 10 中使用标准答案的桶基本相似。

图 12：用我们的 PaLM 2-S* PRM 在不使用标准正确性信息的情况下为 PRM 搜索计算难度桶。可以看到，这些桶的表现趋势与图 3 中使用标准答案的桶基本相似。

### 附录 D PRM 训练细节

我们把 PRM 微调为一个二分类器，模型在解答的每一步预测一个 0 到 1 之间的值。我们用蒙特卡洛展开得到的软值训练模型，使用二元交叉熵损失函数（即 $-(y\log(\hat{y})+(1-y)\log(1-\hat{y}))$，其中 $y$ 对应软性标准值，$\hat{y}$ 为模型的预测值）。我们使用 AdamW 优化器微调基座模型：学习率 3e-5，批大小 128，dropout 0.05，Adam betas $(0.9,0.95)$。我们做早停，在一个随机留出的验证集（由原始 PRM800k 训练划分中 10% 的题目组成）上选择验证损失最低的检查点。

我们在来自对应少样本提示基座模型的每题 16 个样本上微调 PRM。在每一步，我们用同一个基座模型与提示做 16 次蒙特卡洛展开来估计步级价值。我们剔除了训练数据中所有未能输出有效、可解析最终答案的样本，因为在初期实验中发现它们会损害 PRM 表现。

生成样本时，基座模型被提示以换行分隔的逐步格式输出答案，做法与 Lightman et al. (2023) 相同。然后我们用简单的换行切分流程把每个答案切分成步骤。我们提示的细节见附录 G。

### 附录 E 比较 PRM 聚合策略

我们比较了聚合逐步 PRM 得分以产生整个解答最终得分的不同方法。具体比较：1) 取所有步骤中的最小得分，即 Lightman et al. (2023) 的做法（「min」）；2) 取所有步骤正确性概率的乘积（「prod」）；3) 只取最后一步的预测（「last」）。我们在图 13 中看到，取最后一步优于另外两种做法。先前工作（Lightman et al., 2023；Wang et al., 2023）发现 min 是最佳聚合器。我们认为这一差异源于我们的验证器是用软性 MC 回报标签训练的，其表现与二元正确性标签很不一样，因此其他聚合策略可能不产生同样效果。

有趣的是，使用最后一步聚合时，我们实际上是在把 PRM 当作 ORM 用。然而我们看到 PRM 仍胜过 ORM，这提示在我们的情形中，逐步 PRM 训练可能在很大程度上作为一种表示学习发挥作用，而不仅是推理时的工具。未来工作应进一步探索这一思路。

图 13：我们比较聚合逐步 PRM 得分以产生整个解答最终得分的不同方法：「min」指取所有步骤得分的乘积最小值，「prod」取所有步骤正确性概率的乘积，「last」只用最后一步得分。可以看到，last 在所有聚合策略中表现最好。

### 附录 F 比较 PRM 与 ORM

我们用 PaLM 2-S* 基座 LM 训练了一个 PRM 与一个 ORM 模型。我们在图 14 中看到，PRM 胜过 ORM，且 PRM 与 ORM 之间的差距随使用样本数增多而扩大。我们按附录 E 的描述用 PRM 的最后一步预测为答案打分。

图 14：我们在 best-of-N 评估中比较从 PaLM 2-S* 微调的 PRM 与 ORM 模型。我们用 PaLM 2-S* 基座 LM 以少样本提示采样输出。可以看到，在大样本数下 PRM 大幅胜过 ORM。

### 附录 G 提示细节

为了让基座模型以可应用 PRM 的逐步格式输出答案，我们使用一个 4 样本提示，由 Lightman et al. (2023) 发布的 PRM800k 数据中随机选取的正确答案示例组成。具体而言，我们使用第 1 阶段训练划分中的答案。这些答案是 GPT-4 生成的正确答案示例，包含正确的逐步格式。在初期实验中，我们发现这一提示流程产生的结果与 Lewkowycz et al. (2022) 所用的提示相近。我们用这一提示为 PRM 与修订模型生成训练数据，也在测试集上针对 PRM 进行搜索时使用该提示。为给该提示预测的最终答案评分，我们使用 Lightman et al. (2023) 发布的评分函数。

### 附录 H 修订模型微调细节

微调修订模型时，我们遵循第 6.1 节所述流程。我们先为每题采样 64 个输出，然后剔除所有以无效解答结尾的答案。对每个正确答案，我们从 0 到 4 之间均匀采样一个数，表示训练时上下文中包含多少个错误答案。正确答案作为轨迹中的最后一个答案（我们训练模型去生成它），错误答案放入上下文。若采样到的数大于 0，我们再按字符级编辑距离度量找出最接近的错误答案，作为轨迹中最后一个错误答案。这样做的目的是选出一个与正确答案有某种相关的错误答案，以促进学习。其余错误答案从可用答案集合中随机抽取。若错误答案少于 4 个，我们把均匀分布的上限截断到错误样本数。我们用这一流程为训练数据中的所有题目生成轨迹。

然后我们在这些生成轨迹中的正确答案解答上微调基座语言模型。我们使用 AdamW 优化器：学习率 1e-5，批大小 128，dropout 0.0，Adam betas $(0.9,0.95)$。

我们发现，总体而言，在按上述方式生成的轨迹组成的评估集上评估损失并不能为早停提供好信号。相反，我们发现验证损失开始上升之后很久的检查点反而更擅长修订。这可能是因为微调修订模型之后，评估集代表的是离策略（off-policy）数据，相对模型自身按策略会生成的轨迹天然是分布外的。因此，我们把修订模型检查点选在观察到验证集过拟合之后不远处。

### 附录 I 修订模型选择准则

如第 6.1 节所述，为有效使用我们的修订模型，我们需要部署一个准则，在修订轨迹内与多条并行轨迹间都选出最佳答案。我们用两种方法：1) ORM 验证器；2) 多数投票。

对 ORM 验证器，我们按附录 J 的流程在修订模型的输出上训练一个 ORM。推理时我们用这个验证器选择最佳答案。由于我们要在两个轴上做聚合（每条修订轨迹内与多条轨迹之间），我们部署分层策略：先在每条修订轨迹内选出最佳答案，再跨轨迹聚合这些被选出的答案。为在每条轨迹内选出最佳答案，我们执行 best-of-N 加权聚合，然后选出具有最大 best-of-N 加权答案的最高得分解答。随后，为在所有修订链中选出最终答案，我们对每条修订链的最佳答案再做一轮 best-of-N 加权选择。这第二轮 best-of-N 加权之后的答案即我们的最终答案预测。

对多数投票，我们发现当轨迹长度或轨迹条数太小时，分层聚合会出问题：样本不足时多数投票无法有效选出最佳选项。因此对多数投票，我们直接一次性取所有轨迹的全部答案，取其多数作为最终答案。我们发现这比分层方法产生平滑得多的缩放行为。

### 附录 J 修订模型验证器训练

我们发现，在 PaLM 2-S* 基座模型输出上微调的 PRM 应用于 PaLM 2-S* 修订模型的输出时效果不佳（见图 15），原因很可能是与修订模型的分布偏移。因此，我们单独训练了一个 ORM 验证器供 PaLM 2-S* 修订模型使用。我们本可以也训练一个 PRM，但生成逐步 PRM 标签成本高昂，故选择了 ORM。

我们针对修订设置对标准 ORM 略作修改：微调 ORM 时把先前的修订放入上下文，使验证器能访问与修订模型相同的上下文，从而在给当前答案打分时看到修订模型先前的答题尝试。其余实验细节与训练 PRM 时相同。

经验上，我们发现把修订历史纳入上下文能略微提升表现（见图 15）。此外，即使上下文中没有修订，顺序修订仍略优于并行，说明顺序采样带来的改进并非仅仅来自验证器的上下文。

图 15：左：我们比较在修订模型输出上训练的 ORM 与在 PaLM 2-S* 基座模型输出上训练的 PRM。可以看到，应用于修订模型的输出时，适配修订模型的 ORM 胜过 PRM，原因很可能是与修订模型的分布偏移。右：我们消融了在修订模型验证器上下文中包含先前修订的效果。可以看到，把修订纳入上下文对验证器略有帮助，但两种设置都仍胜过并行基线。

### 附录 K ReST$^{\text{EM}}$ 修订模型实验

我们尝试用一个简化 RL 算法 ReST$^{\text{EM}}$（Singh et al., 2024）进一步优化我们的 PaLM 2-S* 修订模型。具体而言，我们在 MATH 训练集上为每题生成了最多长度为 5 的 64 条修订轨迹。我们在每条轨迹的第一个正确答案处停止修订模型。利用这些生成的数据，我们再在正确答案数据上微调基座 LM。为帮助模型学习任务，我们显式地均衡了轨迹长度的分布。

在图 16 中，我们绘制了这一新修订模型随顺序与并行比例变化的性能。可以看到，对这个新模型，增加顺序修订显著损害性能。我们推测这一退化源于运行 ReST$^{\text{EM}}$ 得到的在线数据加剧了修订数据中的虚假相关，导致被优化的模型未能学会修订任务。我们相信，采用 Qu et al. (2024b) 那样更偏离线的数据收集策略可能更有效，进一步的探索留作未来工作。

![Refer to caption](2408.03314v1/rest_em_revision_model_iso_gens_output.png)

图 16：我们的 ReST$^{\text{EM}}$ 优化修订模型随顺序与并行比例变化的性能。我们用多数投票选择答案。可以看到，这一优化后的修订模型在增加顺序修订时表现出显著的性能退化。

### 附录 L 修订模型示例输出

在图 17、18、19、20、21、22 与 23 中，我们收录了我们修订模型输出的精选示例。

![Refer to caption](2408.03314v1/figures/revisions_ex1.png)

图 17：修订模型示例 1。模型在前两次尝试中最后求和出错，但在第三次尝试中成功并得到正确答案。

![Refer to caption](2408.03314v1/figures/revisions_ex2.png)

图 18：修订模型示例 2。第一次尝试中模型采取了错误方法，第二次尝试更接近但在结尾出错。最后一次尝试得到正确答案。

![Refer to caption](2408.03314v1/figures/revisions_ex3.png)

图 19：修订模型示例 3。第一次尝试中模型在最终答案的格式上出错；第二次尝试予以纠正。

![Refer to caption](2408.03314v1/figures/revisions_ex4.png)

图 20：修订模型示例 4。前几次尝试中模型未能完成 10 进制到 8 进制的转换。最后一次尝试做出了正确计算。

![Refer to caption](2408.03314v1/figures/revisions_ex5.png)

图 21：修订模型示例 5。前两次尝试中模型在把欧几里得坐标转换为极坐标时出错。最后一次尝试没有犯这些错误。

![Refer to caption](2408.03314v1/figures/revisions_ex6.png)

图 22：修订模型示例 6。前两次尝试中模型在对 284 的真因数求和时出错。第三次尝试正确求出了这个和。

![Refer to caption](2408.03314v1/figures/revisions_ex7.png)

图 23：修订模型示例 7。第一次尝试中模型错误地计算了 $\frac{1}{3}+2$。第二次尝试纠正了这一错误。

### 附录 M PRM 束搜索示例输出

在图 24、25、26、27、28 与 29 中，我们收录了 PRM 束搜索的精选示例。我们在示例中给出了每一步介于 0 与 1 之间的 PRM 得分。

![Refer to caption](2408.03314v1/figures/PRM_ex1.png)

图 24：PRM 束搜索示例 1。

![Refer to caption](2408.03314v1/figures/PRM_ex2.png)

图 25：PRM 束搜索示例 2。

![Refer to caption](2408.03314v1/figures/PRM_ex3.png)

图 26：PRM 束搜索示例 3。

![Refer to caption](2408.03314v1/figures/PRM_ex4.png)

图 27：PRM 束搜索示例 4。

![Refer to caption](2408.03314v1/figures/PRM_ex5.png)

图 28：PRM 束搜索示例 5。

![Refer to caption](2408.03314v1/figures/PRM_ex6.png)

图 29：PRM 束搜索示例 6。
