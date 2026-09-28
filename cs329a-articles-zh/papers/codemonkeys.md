---
title: "CodeMonkeys：为软件工程扩展测试时计算"
title_en: "CodeMonkeys: Scaling Test-Time Compute for Software Engineering"
arxiv: 2501.14723
source: https://arxiv.org/abs/2501.14723
crawled: 2026-09-23
translated: 2026-09-23
---

# CodeMonkeys：为软件工程扩展测试时计算

> 原文：[CodeMonkeys: Scaling Test-Time Compute for Software Engineering](https://arxiv.org/abs/2501.14723) · Stanford CS329A 指定阅读

Ryan Ehrlich∗、Bradley Brown∗、Jordan Juravsky∗、Ronald Clark、Christopher Ré、Azalia Mirhoseini

联系方式：rehrlich@stanford.edu、bradley.brown@cs.ox.ac.uk、jbj@stanford.edu、ronald.clark@cs.ox.ac.uk、chrismre@stanford.edu、azalia@stanford.edu
所属机构：斯坦福大学计算机科学系；牛津大学

2025 年 1 月 24 日

注：∗ 表示同等贡献（BB 的工作在其于斯坦福任访问研究员期间完成）。

###### 摘要

扩展测试时计算（test-time compute）是提升 LLM 能力的一条前景广阔的轴线。然而，测试时计算可以有多种扩展方式，如何有效地组合不同方法仍是一个活跃的研究领域。本文在求解 SWE-bench 数据集中真实 GitHub issue 的场景下探索这一问题。我们名为 CodeMonkeys 的系统让模型在生成草稿编辑的同时联合生成并运行一个测试脚本，从而迭代地修改代码库。我们对每个 issue 采样大量此类多轮轨迹，以生成一组候选编辑。这一方法使我们既能通过增加每条轨迹的迭代次数来扩展「串行」测试时计算，也能通过增加每个问题的轨迹数量来扩展「并行」测试时计算。借助并行扩展，我们可以把前期成本摊销到多个下游样本上，从而使用「让 LLM 阅读每个文件」这一简单方法来识别相关的代码库上下文。为了在候选编辑之间做出选择，我们将基于模型生成测试的投票与一条专门用于选择的最终多轮轨迹相结合。总体而言，CodeMonkeys 以约 2300 美元的预算解决了 SWE-bench Verified 中 57.4% 的 issue。我们的选择方法还可以用于组合来自不同来源的候选：在由现有 SWE-bench Verified 顶级提交组成的编辑集成上进行选择，取得了 66.2% 的分数，优于该集成中最佳成员的单独表现。我们在 <https://scalingintelligence.stanford.edu/pubs/codemonkeys/> 完整发布了代码与数据。

## 1 引言

![Refer to caption](2501.14723v2/banner_final.png)

图 1：CodeMonkeys 系统总览。左：我们让模型先识别相关文件、再对它们做相对排序，以此检索代码库上下文。中：我们使用一对多轮状态机分别生成代码库编辑与测试脚本，并基于执行反馈进行迭代。我们并行运行这些状态机多次，为每个 issue 生成 10 个编辑与测试。右：我们通过找出通过最多生成测试的候选、再让模型在这些顶级候选之间做出决定，来在候选编辑之间进行选择。关于我们系统三个状态机的细节，见图 4。

|  | Claude Sonnet-3.5 API 成本 |  |  |  | 本地成本 | 总成本 |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 阶段 | 输入 | 输出 | 输入缓存 |  | Qwen-2.5 | USD（%） |  |
|  |  |  | 读 | 写 |  |  |  |
| 相关性 | 0.00 | 0.00 | 0.00 | 0.00 | 334.02 | 334.02 (14.6%) |  |
| 排序 | 0.00 | 11.92 | 1.10 | 6.90 | 0.00 | 19.92 (0.9%) |  |
| 生成测试 | 10.60 | 295.15 | 21.60 | 112.64 | 0.00 | 439.99 (19.2%) |  |
| 生成编辑 | 14.67 | 353.95 | 636.82 | 360.58 | 0.00 | 1366.02 (59.6%) |  |
| 选择 | 0.52 | 51.12 | 15.17 | 65.14 | 0.00 | 131.95 (5.8%) |  |
| 总计 | 25.79 | 712.14 | 674.69 | 545.26 | 334.02 | 2291.90 (100.0%) |  |

表 1：在 SWE-bench Verified 全部 GitHub issue 上运行 CodeMonkeys 的成本分解。所有成本以美元计。我们的系统使用两个 LLM：一个用于排序、生成与选择阶段的主模型（我们使用 Claude 3.5 Sonnet API（Anthropic, 2024）），以及一个用于扫描代码库以识别相关文件的更廉价模型（我们在本地运行 Qwen2.5-Coder-32B-Instruct（Hui et al., 2024））。在衡量 Claude API 的成本时，我们使用的价格为每百万输入 token 3 美元、每百万缓存读 token 0.3 美元、每百万缓存写 token 3.75 美元、每百万输出 token 15 美元。本地推理成本的估算细节见附录 C。

大型语言模型（LLM）求解日益复杂编码任务的能力已迅速提升（Chen et al., 2021；Li et al., 2023；Anthropic, 2024）。现代 LLM 在编程竞赛中已经能超越部分人类选手（Li et al., 2022；AlphaCode Team, 2024），并且已成为广受欢迎的编程助手（Ray, 2023；Anysphere Team, 2025）。以 SWE-bench 数据集（Jimenez et al., 2024）衡量，LLM 在求解真实 GitHub issue 这类软件工程任务上也在不断进步。进步的一个主要驱动力是增加模型训练所用的计算量与数据量，这已可靠地带来模型能力的提升（Hestness et al., 2017；Kaplan et al., 2020；Hoffmann et al., 2022）。然而，继续扩展模型训练的成本对大多数组织而言正变得难以承受（Grattafiori et al., 2024）。

进一步提升模型能力（包括 SWE-bench 这类编码任务）的另一条途径是扩展测试时计算（Li et al., 2022；Brown et al., 2024；Snell et al., 2024；Wu et al., 2024）。这类扩展通过增加推理期间消耗的计算量来产出更高质量的解。扩展测试时计算的一种做法是让模型在输出最终答案前进行更长时间的深思。这种「串行」扩展可以采取思维链的形式（Nye et al., 2021；Wei et al., 2023），即模型使用大量 token 的计算来推理一个问题；也可以通过多轮交互实现，即模型迭代地响应代码执行结果等外部反馈（Yao et al., 2023；Wang et al., 2024；Yang et al., 2024；Ruan et al., 2024）。或者，测试时计算也可以「并行」扩展，即为一个问题采样多个候选解（Wang et al., 2023；Li et al., 2022；Lightman et al., 2023；Snell et al., 2024）。在我们此前的工作 Large Language Monkeys（Brown et al., 2024）中，我们发现覆盖率——即用已生成的任意样本所能求解的数据集问题比例——常常随样本数量呈对数线性增长，在求解 SWE-bench issue 时也是如此。

虽然这些覆盖率结果为「并行扩展测试时计算可能有益于 SWE-bench」提供了令人鼓舞的证据，但它们并没有直接给出一套可操作的方案来利用它提升 issue 解决率。特别是，生成多个候选引入了一个问题：需要在其间选出最终答案。要从高覆盖率中受益，就需要一种能够区分正确与错误答案的选择方法。此外，在 Large Language Monkeys 中，我们使用了一个为生成单一解而设计的现成 SWE-bench 框架（Moatless Tools（Örwall, 2024）），我们只是以正温度对该框架重复采样来生成多个候选编辑。这就引出了一个问题：如果把从测试时计算扩展中受益作为首要考量，一个系统应当如何被不同地设计？

本工作的核心贡献就是探索这一想法，即提出一个专门围绕扩展测试时计算而设计的 SWE-bench 求解系统（图 1）。我们将一个 issue 的解决划分为三个主要步骤：1) 识别相关的代码库上下文，2) 生成用于解决该 issue 的候选代码库编辑，3) 在这些候选编辑之间进行选择（Xia et al., 2024）。在生成代码库编辑时，我们通过强制模型在编辑之外同时编写一个测试脚本来扩展串行计算，使模型能够根据执行反馈迭代修改其编辑与测试。我们通过为每个 SWE-bench issue 采样大量这种（编辑，测试）对来扩展并行测试时计算。这种组合式扩展在 SWE-bench Verified 上实现了 69.8% 的覆盖率。有趣的是，我们发现把推理预算在串行与并行扩展之间做不同分配，往往得到相近的覆盖率。此外，对并行扩展的运用让我们能把识别相关代码库上下文的成本摊销到多个下游样本上。我们采用「让 LLM 扫描每个文件」这一简单方法，在每个 issue 前期只运行一次时，其成本仅占总成本的 15%。

为了在候选代码库编辑之间进行选择，我们探索了基于模型生成测试进行投票（Ruan et al., 2024；Xia et al., 2024）以及直接用模型做选择（Ruan et al., 2024；Snell et al., 2024）的方法。我们发现这两种方法的组合效果最好：先用基于测试的投票对初始候选池进行筛选，再让模型在剩余编辑之间选择。此外，我们发现给模型更多串行计算可以进一步改进基于模型的选择，做法是让模型编写并运行测试来区分候选。使用这一选择方法，CodeMonkeys 在 SWE-bench Verified 上取得 57.4% 的总分（表 2），LLM 推理花费约 2300 美元（表 1）。

我们还表明，我们的选择方法可以有效地组合来自异构来源的生成结果。我们通过组装「Barrel of Monkeys」（猴子桶）来演示这一点：一个扩充后的候选编辑池，包含 SWE-bench Verified 排行榜前 4 名的提交。在这个覆盖率为 80.8% 的集成上进行选择得到 66.2% 的分数——高于集成中表现最好的提交的 62.8%，仅比 o3 报告的分数（71.7%）低 5.5%。我们在 <https://scalingintelligence.stanford.edu/pubs/codemonkeys/> 发布了我们的代码以及所有生成样本。

## 2 设计一个扩展测试时计算的 SWE-bench 求解器

![Refer to caption](2501.14723v2/figures/problem_resolution_flow.png)

图 2：在第 2 节我们所划分的三个子任务（上下文、生成与选择）上衡量 CodeMonkeys 的表现。注意，修改其中一个子任务的方法也可能影响其他子任务的表现。例如，生成更多候选编辑可能提高覆盖率，但也会让选择变得更难。

每个 SWE-bench 实例由一个 issue 描述和对应的代码仓库组成。目标是编辑代码库中的一个或多个文件来解决该 issue。编辑的正确性可以用仓库的测试套件自动评分。在本工作中，我们聚焦于 SWE-bench 的 Verified 划分（Chowdhury et al., 2024），其中包含经人类标注者判定为「可解」的实例（即 issue 描述明确无歧义、且测试套件不会滤除正确解）。我们把求解一个 SWE-bench Verified 实例分解为三个顺序子任务（图 1）：

1. 上下文（Context）：我们能否识别出需要编辑的代码库文件[注1](#fn1)并把它们放进上下文窗口？我们可以用召回率（recall）衡量这一子任务的结果：所有需要文件都已被识别出来的问题比例。

   注 1：在计算召回率时，我们通过检查 SWE-bench 数据集中提供的官方 issue 解法是否编辑了某文件来判断该文件是否需要编辑。这一计算没有考虑通过编辑另一组文件来解决 issue 的替代解法的存在。

2. 生成（Generation）：我们能否在采样的任意候选中产出一个正确的代码库编辑？我们可以用覆盖率（coverage）衡量这一子任务的结果：至少有一个生成编辑是正确的问题比例。

3. 选择（Selection）：我们能否从候选集合中选出一个正确的代码库编辑？完成这一子任务后，我们就可以衡量最终分数：我们系统提交的编辑所解决的数据集问题比例。

下面我们描述对每个子任务的处理方式，各子任务的指标见图 2，系统的成本分解见表 1。除非另有说明，系统的所有部分均使用 `claude-3-5-sonnet-20241022`（Anthropic, 2024）。我们在附录 A 中给出使用 DeepSeek-V3（DeepSeek-AI et al., 2024）的补充结果。

### 2.1 识别相关的代码库上下文

![Refer to caption](2501.14723v2/figures/context_recall.png)

图 3：左：随着上下文窗口大小上限的增加，测量召回率（即上下文窗口包含全部所需文件的 SWE-bench 问题比例）。在使用我们后续实验所用的 128k token 上限时，92.6% 的实例的上下文中包含正确文件。右：可视化 SWE-bench 问题上上下文压缩因子的分布，即相关性模型扫描的文件累计 token 数与经过相关性判断 + 排序后纳入的文件累计 token 数之比。

![Refer to caption](2501.14723v2/figures/state_machine_details.png)

图 4：CodeMonkeys 状态机的细节。测试状态机在尚未应用任何编辑的代码库上运行测试并根据执行反馈，迭代地生成测试脚本的初始草稿。编辑状态机首先以代码库上下文和测试状态机的输出测试为条件生成一个初始编辑，然后在应用编辑前后分别运行测试，基于执行反馈同时完善测试与编辑草稿。选择状态机首先生成一个测试来区分通过最多测试脚本的前 3 名候选编辑，然后基于在所有候选编辑以及未编辑代码库上运行该测试的执行反馈，决定是再创建一个新的测试脚本以进一步区分这些编辑，还是选出最终编辑。

求解 SWE-bench 实例的关键挑战之一是管理庞大的输入上下文。大多数 SWE-bench 代码库包含数百万 token 的上下文。这超出了大多数可用模型的上下文长度，而且用前沿模型处理这些上下文的成本也将高得离谱。管理 SWE-bench 上下文的现有方法包括使用嵌入模型（Örwall, 2024；Xia et al., 2024）、从文件树迭代扩展（Xia et al., 2024），以及给模型提供浏览文件的工具（Yang et al., 2024；Schluntz et al., 2024）。

在我们的系统中，我们知道会为每个实例生成一组候选编辑。因此，通过在所有下游编辑之间共享代码库上下文，我们可以摊销上下文生成的成本。这一观察使「让一个模型阅读代码库中的每个文件」（我们使用 Qwen2.5-Coder-32B-Instruct（Hui et al., 2024））、判断每个文件是否与目标 issue 相关、并只把相关文件纳入上下文窗口（Arora et al., 2023）这一简单方法成为可能[注2](#fn2)。每个实例执行一次这种全代码库扫描对系统总成本的贡献不足 15%（表 1），平均每个问题处理 294 万 token。如果我们不摊销这次扫描、而是为每个问题的 10 个编辑各自重跑一遍，它将成为最昂贵的步骤。在多个下游编辑之间共享上下文还能提高提示缓存（prompt caching）的命中率，从而进一步节省成本。

注 2：我们的扫描只纳入 Python 文件，并排除测试目录内的文件。

即便经过了相关性过滤，许多问题的上下文仍然过长。为了进一步压缩上下文，我们执行一个基于模型的排序过程，按重要性对文件排序。首先，作为初始代码库扫描的一部分，我们为每个被标记为相关的文件生成一段简短摘要，描述该文件与目标 issue 的关系。然后我们构造一个排序提示，其中包含每个相关文件的文件名、摘要和 token 数。我们要求排序模型在其排序中纳入约 60,000 token 的上下文。由于 Claude API 即便在温度 0 下也可能是非确定性的，我们从排序提示生成三次补全，并取每个文件在三次重复中的平均排名来构造最终排序。我们依据这个合并后的排序构造上下文窗口：纳入所有已排序文件的全部内容，上限为 128,000 token。平均而言，这带来 74,570 token 的代码库上下文，相比纳入所有被评估过相关性的文件，上下文大小平均缩减 50.5 倍。

### 2.2 生成带配套测试的候选代码库编辑

图 5：随着我们遍历每个编辑状态机的串行迭代次数与每个问题采样的并行状态机数量，测量覆盖率（左）与使用多数投票选择时的分数（右）。每条彩色曲线对应一个不同的并行状态机数量，曲线上的点对应状态机串行迭代次数的增加。最初几次串行迭代对性能提升影响巨大。但过了这一点之后，成本相近的不同配置带来相近的表现，对覆盖率而言尤其如此。

在识别出代码库的相关部分之后，我们就可以开始生成用于解决目标 issue 的候选代码库编辑。我们采用状态机抽象（Örwall, 2024）来建模一个多轮交互过程：模型根据执行反馈迭代地编辑目标代码库。此外，与 Large Language Monkeys（Brown et al., 2024）一样，我们为每个 SWE-bench 实例运行多个相互独立的状态机，使用正的采样温度在候选之间引入多样性。这一做法为我们提供了两种直接扩展测试时计算的途径：

1. 我们可以通过增加每个状态机执行的最大迭代次数来扩展串行计算[注3](#fn3)。

   注 3：确切地说，我们限制的是每个状态机的模型补全次数。模型的初始生成以及对先前格式错误响应的更正都计入该上限。

2. 我们可以通过增加每个实例运行的独立状态机数量来扩展并行计算。

重要的是，我们要求模型在生成每个编辑的同时联合生成并修改一个测试。这些测试被构造为独立的 Python 脚本，试图复现该 GitHub issue，并通过退出码传达结果。强制模型在编辑之外编写可执行脚本，为模型提供了更丰富的反馈来引导其迭代，从而更有效地扩展串行计算（Huang et al., 2024）。此外，测试还充当（不完美的）验证器，之后可以协助在候选编辑之间进行选择（见第 2.3 节）。

从经验上看，我们发现模型往往需要若干次迭代才能写出一个可运行的测试（例如由于配置错误、易于修复的崩溃等）。为了让模型可以先专注于这些步骤，我们把系统的这一阶段分解为两个前后衔接的状态机：

1. 一个初始的测试状态机，对测试脚本的初始草稿进行迭代。

2. 一个后续的编辑状态机，对一个代码库编辑（以 aider 风格的编辑 diff 形式（Gauthier, 2024））进行迭代。该状态机以一个测试状态机的输出作为种子，并可以在需要时修改测试脚本[注4](#fn4)。

   注 4：允许模型在编辑状态机期间继续修改测试很重要，这样它们才能进行「双向调试」。在测试状态机中，模型可以持续迭代，直到其脚本在未编辑的代码库上运行时能正确标记出 issue。然而，这可能导致测试总是报告错误，即便正确的代码库编辑已被应用。允许模型在编辑状态机期间继续修改测试，可以让它们验证测试在编辑前失败、编辑后通过。

这些状态机的结构如图 4 所示（左侧与中间面板），更多细节见附录 B.1。我们把测试与编辑拆分为独立状态机的做法也降低了系统成本。我们的成本表（表 1）显示，前缀缓存读取是编辑状态机最昂贵的组成部分，这在很大程度上是由于初始提示中包含的代码库文件。由于编写测试脚本通常不需要代码库上下文，我们可以在测试状态机中省略第 2.1 节识别出的文件，从而缩短提示长度（进而降低缓存读成本）。我们还通过在测试与编辑状态机之间清空聊天历史来缩短提示长度。

我们对 SWE-bench Verified 中的每个实例运行 10 对测试与编辑状态机，并将所有状态机的迭代次数限制为 8 次。在图 5 的左侧，我们在两个扩展参数上遍历并测量覆盖率。我们的最佳配置使用了每个实例全部 10 个状态机、每个状态机全部 8 次迭代，实现了 69.8% 的覆盖率。有趣的是，在最初几次迭代与状态机之后，出现了一条「边界线」：总推理成本相近的配置也具有相近的覆盖率，尽管这些成本在「更多状态机」与「更多迭代」之间的分布不同。然而，请注意这并不意味着串行与并行计算可以完全互换。特别地，两个覆盖率相同的配置在选择之后未必得到相同的最终分数。通过生成大量候选来扩展并行计算会让选择变得更难，而生成一条迭代次数很多的单一深度轨迹则完全消除了选择问题。两类扩展之间的另一个区别是，我们的设置只能间接地扩展串行计算：我们控制的是单个状态机内允许的最大迭代次数，但模型可以决定认可自己的测试和/或编辑，并在到达迭代上限之前终止状态机。进一步提高迭代上限对那些模型已经错误地认可了自己工作的「卡住」状态机并无帮助。相比之下，我们总是可以通过再运行一个状态机来进一步扩展并行计算，这保证了一次模型有机会生成正确代码库编辑的「全新开始」。

### 2.3 在候选编辑之间进行选择

图 6：比较应用于 CodeMonkeys 编辑状态机所生成候选编辑的各选择方法。我们表现最好的选择方法——先做 top-3 生成测试过滤再做选择状态机——恢复了随机选择下界与 oracle 选择上限（即覆盖率）之间差距的大约一半。

|  |  |
| --- | --- |
| 方法 | 分数 |
| Barrel of Monkeys（Oracle 选择） | 80.8 |
| o3 | 71.7 |
| CodeMonkeys（Oracle 选择） | 69.8 |
| Barrel of Monkeys | 66.2 |
| Blackbox AI Agent | 62.8 |
| CodeStory | 62.2 |
| Learn-by-interact | 60.2 |
| devlo | 58.2 |
| CodeMonkeys | 57.4 |
| Emergent E1 | 57.2 |
| Gru | 57.0 |

  

表 2：比较本文所探索的方法（加粗）与现有顶级方法在 SWE-bench Verified 上的最终分数。注意，Barrel of Monkeys 的结果依赖于 SWE-bench Verified 排行榜上现有提交的生成结果，而 oracle 选择方法的数值即覆盖率。

在 oracle 选择的最佳情形下（此时我们的最终分数等于 69.8% 的覆盖率），CodeMonkeys 将超越 SWE-bench Verified 排行榜上的所有提交，仅比 o3 报告的 71.7% 低 1.9%。然而，如果我们改为随机选择编辑，45.8% 的期望分数甚至进不了排行榜前 20 名。这一显著的性能差距凸显了准确选择的重要性。我们探索了四种在我们为每个实例生成的 10 个候选编辑之间进行选择的策略：

1. 基于测试的多数投票：我们在 10 个编辑上分别运行 10 个模型生成的测试，选出通过测试最多的编辑。若多个编辑的通过数并列最多，我们计算从中随机挑选时的期望分数。

2. 模型选择：我们在向模型提供 issue 描述、代码库上下文以及 git diff 形式的候选编辑后，让模型选择一个候选编辑。

3. 先做 top-3 过滤的模型选择：我们复用上面的模型选择提示，但只在通过最多生成测试的三个编辑之间选择。并列时偏向 git diff 更短的编辑。

4. 先做 top-3 过滤的选择状态机：我们把单轮的基于模型的选择升级为一个完整的状态机，允许模型编写新的测试脚本来区分候选编辑（图 4 右侧及附录 B.1）。该状态机的初始提示包含与基于模型的选择相同的信息，但还包括一个来自先前阶段的模型生成测试示例。在每次迭代中，模型可以选择一个最终编辑，或者生成一个新测试。每当写出新测试时，我们向模型展示该测试在每个候选编辑以及未编辑代码库上的运行输出。我们复用上述 top-3 过滤过程来缩小初始候选池。

我们在图 6 中比较这些选择方法的表现。四种方法都优于随机选择，其中选择状态机表现最佳。注意，选择状态机也是我们测试的四种方法中最昂贵的；不过它对系统总成本的贡献不足 10%。我们同样看到初始多数投票过滤的收益：不带 top-3 过滤的模型选择逊于纯多数投票，而带过滤的模型选择则胜过它。采用我们选定的「选择状态机 + top-3 过滤」方案，CodeMonkeys 在 SWE-bench Verified 上取得 57.4% 的最终分数（表 2），弥合了随机选择与 oracle 选择之间约一半的差距。

#### 2.3.1 Barrel of Monkeys：在现有 SWE-bench 提交的样本集成上进行选择

在 CodeMonkeys 中，我们在由本方法状态机生成的独立同分布（IID）候选编辑之间进行选择。这里我们证明，我们的选择状态机在组合来自异构来源的候选编辑时同样有用。我们通过将 CodeMonkeys 的最终（已经过选择的）编辑与 SWE-bench Verified 排行榜前四名[注5](#fn5)——Blackbox AI Agent（Blackbox AI, 2025）、CodeStory Midwit Agent + swe-search（Pani, 2024）、Learn-by-interact（Su et al., 2025）和 devlo（devlo, 2025）——的提交合并，构造了一个编辑集成，即「Barrel of Monkeys」。该集成每个问题有五个样本，合并覆盖率为 80.8%，显著高于 o3 报告的 71.7%。虽然这两个数字并不直接可比（o3 的分数对应 pass@1，而 Barrel of Monkeys 的覆盖率对应 pass@5），但我们认为有必要强调：现有方法（合起来）已经能解决 SWE-bench Verified 中相当大比例的实例。这进一步凸显了开发更强选择方法的潜在收益。

注 5：截至 2025 年 1 月 15 日。

由于 Barrel of Monkeys 的每个问题初始候选数比 CodeMonkeys 少，我们跳过初始的基于测试的过滤，直接把所有编辑传给选择状态机。状态机的示例测试取自作为集成一部分的 CodeMonkeys 候选编辑。在该集成上进行选择取得 66.2% 的分数，优于集成中表现最佳成员单独的分数（Blackbox AI Agent（Blackbox AI, 2025）为 62.8%）。不过，由于从该集成中随机选择可得 60.9% 的分数，这里我们的选择方法所恢复的「随机选择与覆盖率之间」差距的比例，相对于从编辑状态机中选择时要更小。

## 3 局限与未来工作

在本工作中，我们提出了一个成功扩展串行与并行测试时计算以提升 SWE-bench Verified 实例解决率的系统设计。然而，图 2 表明，我们系统的每个阶段都仍有改进空间：

- 上下文：我们的文件级「过滤 + 排序」流程在 7.4% 的 SWE-bench Verified 实例上仍会遗漏相关文件。随着模型可用上下文长度的增长和长上下文处理效率的提升，我们希望最终流水线的这一整个阶段可以替换为「直接把整个代码库连同所有相关文档作为上下文提供」（Magic Team, 2024）。另一个需要考虑的因素是，基础模型已经具备关于其正在编辑的仓库的背景知识。这一假设使我们无需向模型提供关于所编辑软件包的用途与用法的更基础解释（例如通过文档）。当求解训练数据中代表性不足的新仓库或私有仓库中的 issue 时，这一假设将不成立，届时可能需要修改我们的检索流水线以获得高召回率。

- 生成编辑与测试：我们也看到改进 CodeMonkeys 状态机、进一步提升覆盖率的空间。在我们的状态机中，我们只向模型提供来自其测试脚本的执行反馈，每个脚本都试图复现目标 issue。额外的执行反馈还可以来自模型编写的或已有的回归测试，以帮助防止引入新 bug。此外，与 Large Language Monkeys（Brown et al., 2024）一样，CodeMonkeys 仅通过正的 token 采样温度在生成中引入多样性。成对出现的测试/编辑状态机之间对为同一问题创建的其他状态机毫无感知，这可能导致冗余、缺乏多样性的生成。加入串行依赖、让模型知晓先前尝试的替代方法（Wang et al., 2024）可以鼓励生成期间更大的多样性。

- 选择：我们的选择方法应用于 CodeMonkeys 时恢复了随机与 oracle 选择之间分数差距的大约一半，而在 Barrel of Monkeys 上进行选择时恢复的比例更小。即使不对候选生成流程做任何改动，选择方法的改进也能显著提升 SWE-bench 总分。与生成环节列出的潜在改进类似，一个我们尚未利用的选择信号来源是每个仓库内部已有的测试套件。Agentless（Xia et al., 2024）与 Gemini 团队（Mallick & Korevec, 2024）都在其选择流程中纳入了这些测试。

此外，我们的工作没有涉及扩展测试时计算的其他途径，例如将不同模型集成在一起（Saad-Falcon et al., 2024；Wang et al., 2024），以及利用经过专门训练、在扩展思维链中探索候选解空间的专用推理模型（OpenAI, 2024；Qwen Team, 2024）。总的来说，我们对扩展测试时计算的方法以及利用这种扩展来解决真实任务系统的持续进展感到兴奋。

## 4 相关工作

面向软件工程的 AI：将 LLM 应用于编码任务已受到相当多的关注（Chen et al., 2021；Li et al., 2023；Liu et al., 2024）。这一领域的进展可以用一系列多样的基准来衡量，它们测试模型根据提示补全函数（Chen et al., 2021；Austin et al., 2021）、从规格说明构建完整的库（Zhao et al., 2024）以及执行领域特定编程任务（Ouyang et al., 2024；Tian et al., 2024）的能力。在本工作中，我们聚焦于 SWE-bench（Jimenez et al., 2024），一个由流行 Python 仓库的真实 GitHub issue 组成的数据集。自发布以来，该基准上的最先进水平迅速提升：早期方法在 SWE-bench Verified 上解决的实例不足 5%（Chowdhury et al., 2024），而当前方法已能解决超过 60%（Blackbox AI, 2025；Pani, 2024；Su et al., 2025）。这一提升既归功于更强的基础模型（Anthropic, 2024；OpenAI, 2024；Mallick & Korevec, 2024），也归功于为模型装备工具、引导 issue 解决流程的更好框架。

这些框架占据了一个广阔的设计空间。一些方法采用相对放手的思路，为模型提供一套可以按任意顺序使用的工具，直到问题解决（Yang et al., 2024；Schluntz et al., 2024）。另一些方法（包括 CodeMonkeys）对 issue 解决流程施加更严格的结构，例如引入状态机（Örwall, 2024）或一个专门的步骤序列（Xia et al., 2024）。与 CodeMonkeys 类似，Agentless（Xia et al., 2024）也把 issue 解决划分为识别相关上下文、生成候选编辑、在编辑之间选择等步骤。但我们对这些步骤的实现（例如用 LLM 驱动的扫描识别上下文、用多轮反馈循环生成编辑并在其间选择）与 Agentless 不同。

各框架向模型提供的工具类型也不同。有些工具是通用的，例如运行 shell 命令或搜索网络的能力（Yang et al., 2024；Schluntz et al., 2024；Wang et al., 2024）。另一些工具更狭窄，例如用 Aider 引入的搜索-替换格式编辑文件（Gauthier, 2024；Örwall, 2024；Xia et al., 2024）。一些框架还向模型提供识别相关代码库上下文的工具，例如打开文件或运行语义搜索（Örwall, 2024；Yang et al., 2024；Schluntz et al., 2024）。求解 SWE-bench issue 的现有框架也已探索扩展测试时计算。串行计算通常通过让模型反思/修改其工作（Örwall, 2024）或向其提供执行或工具调用反馈（Wang et al., 2024；Huang et al., 2024；Ruan et al., 2024）来扩展。值得注意的是，在 Anthropic 展示升级版 Claude 3.5 Sonnet 的框架（Schluntz et al., 2024）中，Claude 有时在提交正确解之前使用了数百轮反馈。Agentless（Xia et al., 2024）与 Gemini 团队（Mallick & Korevec, 2024）通过生成多个候选编辑并利用仓库已有的单元测试协助选择来扩展并行计算。Agentless 还在选择期间使用模型编写的复现测试来检查候选编辑是否真正解决了 issue，而 Gemini 团队与 SpecRover（Ruan et al., 2024）则纳入了基于模型的选择。SWE-search（Antoniades et al., 2024）与 CodeStory（Pani, 2024）等方法通过在中间状态上进行树搜索并结合基于模型的价值估计，将串行与并行扩展结合起来。

扩展测试时计算：通过树搜索消耗测试时计算长期以来是设计下棋 AI 系统的成功策略（Campbell et al., 2002；Silver et al., 2017；Brown et al., 2020）。近来，类似的搜索技术也已与 LLM 结合，成功证明了形式化数学命题（Trinh et al., 2024）。在更广泛的各种场景中，允许 LLM 在输出最终答案前使用更多 token 思考问题，已带来模型推理能力的大幅提升（Wei et al., 2023；Nye et al., 2021）。显式地优化模型执行这种深思过程（例如用强化学习）则进一步提升了能力（OpenAI, 2024；Qwen Team, 2024；DeepSeek-AI, 2025）。

现有工作也探索了通过每个问题采样多个补全来扩展并行测试时计算（Brown et al., 2024；Wu et al., 2024；Snell et al., 2024）。在数学与编码任务上，用小模型重复采样可以获得比大模型单样本更高的覆盖率（Hassid et al., 2024）。重复采样对编码任务尤其有效，因为运行并测试模型输出的能力可以协助选择（Li et al., 2022；Greenblatt, 2024；Li et al., 2024）。更一般的选择方法包括使用结果奖励模型（Christiano et al., 2017）、过程奖励模型（Lightman et al., 2023；Wang et al., 2024），或基于提示的验证器设置（Snell et al., 2024）。PlanSearch（Wang et al., 2024）表明，把一部分并行样本转换为顺序尝试可以提升多样性，降低达到给定覆盖率所需的计算量。Archon（Saad-Falcon et al., 2024）、Mixture-of-Agents（Wang et al., 2024）与 MALT（Motwani et al., 2024）考虑了许多不同模型可以生成样本、或充当样本验证器与聚合器的设定，探索如何自动发现这些 LLM 组件的高性能组合。

## 5 致谢

我们感谢 Benjamin Spector、Chris Fifty、Jerry Liu、Jon Saad-Falcon、Owen Dugan、Quinn McIntyre、Simon Guo 和 Will Tennien 在整个项目中的有益讨论与反馈。

我们衷心感谢以下支持：NIH No. U54EB020405（Mobilize）；NSF Nos. CCF2247015（Hardware-Aware）、CCF1763315（Beyond Sparsity）、CCF1563078（Volume to Velocity）与 1937301（RTML）；US DEVCOM ARL Nos. W911NF-23-2-0184（Long-context）与 W911NF-21-2-0251（Interactive Human-AI Teaming）；ONR No. N000142312633（Deep Signal Processing）；Stanford HAI No. 247183；NXP、Xilinx、LETI-CEA、Intel、IBM、Microsoft、NEC、Toshiba、TSMC、ARM、Hitachi、BASF、Accenture、Ericsson、Qualcomm、Analog Devices、Google Cloud、Salesforce、Total、HAI-GCP Cloud Credits for Research 计划、Stanford Data Science Initiative（SDSI），以及 Stanford DAWN 项目的成员：Meta、Google 和 VMWare。美国政府被授权出于政府目的复制和分发重印本，而不受其上任何版权标注的限制。本材料中表达的任何意见、发现、结论或建议均属作者本人，不一定反映 NIH、ONR 或美国政府的观点、政策或背书，无论是明示还是暗示。

本工作在 Clarendon Fund 奖学金的资助下完成。

## 参考文献

- [1]

  Elevating swe-bench verified with blackbox agent.
  <https://blog.blackbox.ai/posts/swe-bench>, 2025.
- [2]

  Your ai-developer teammate.
  <https://devlo.ai/>, 2025.
- [3]

  Anthropic.
  Introducing computer use, a new claude 3.5 sonnet, and claude 3.5 haiku, 2024.
- [4]

  Antonis Antoniades, Albert Örwall, Kexun Zhang, Yuxi Xie, Anirudh Goyal, and William Wang.
  Swe-search: Enhancing software agents with monte carlo tree search and iterative refinement, 2024.
- [5]

  Anysphere Team.
  Series B and Automating Code, January 2025.
  Blog post announcing $105M Series B funding and company milestones.
- [6]

  Simran Arora, Brandon Yang, Sabri Eyuboglu, Avanika Narayan, Andrew Hojel, Immanuel Trummer, and Christopher Ré.
  Language models enable simple systems for generating structured views of heterogeneous data lakes, 2023.
- [7]

  Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le, and Charles Sutton.
  Program synthesis with large language models, 2021.
- [8]

  Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V. Le, Christopher Ré, and Azalia Mirhoseini.
  Large language monkeys: Scaling inference compute with repeated sampling, 2024.
- [9]

  Noam Brown, Anton Bakhtin, Adam Lerer, and Qucheng Gong.
  Combining deep reinforcement learning and search for imperfect-information games.
  In Proceedings of the 34th International Conference on Neural Information Processing Systems, NIPS ’20, Red Hook, NY, USA, 2020. Curran Associates Inc.
- [10]

  Murray Campbell, A. Joseph Hoane, and Feng-hsiung Hsu.
  Deep blue.
  Artif. Intell., 134(1–2):57–83, jan 2002.
- [11]

  Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al.
  Evaluating large language models trained on code, 2021.
- [12]

  Neil Chowdhury, James Aung, Chan Jun Shern, Oliver Jaffe, Dane Sherburn, Giulio Starace, Evan Mays, Rachel Dias, Marwan Aljubeh, Mia Glaese, Carlos E. Jimenez, John Yang, Kevin Liu, and Aleksander Madry.
  Introducing SWE-bench Verified, August 2024.
  Blog post announcing a human-validated subset of SWE-bench for evaluating AI models’ software engineering capabilities.
- [13]

  Paul Christiano, Jan Leike, Tom B. Brown, Miljan Martic, Shane Legg, and Dario Amodei.
  Deep reinforcement learning from human preferences, 2017.
- [14]

  DeepSeek-AI.
  Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning, 2025.
- [15]

  DeepSeek-AI, Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, et al.
  Deepseek-v3 technical report, 2024.
- [16]

  Paul Gauthier.
  Aider is ai pair programming in your terminal.
  <https://aider.chat/>, 2024.
- [17]

  Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, et al.
  The llama 3 herd of models, 2024.
- [18]

  Ryan Greenblatt.
  Geting 50
  <https://www.lesswrong.com/posts/Rdwui3wHxCeKb7feK/getting-50-sota-on-arc-agi-with-gpt-4o>, 2024.
- [19]

  Michael Hassid, Tal Remez, Jonas Gehring, Roy Schwartz, and Yossi Adi.
  The larger the better? improved llm code-generation via budget reallocation, 2024.
- [20]

  Joel Hestness, Sharan Narang, Newsha Ardalani, Gregory Diamos, Heewoo Jun, Hassan Kianinejad, Md. Mostofa Ali Patwary, Yang Yang, and Yanqi Zhou.
  Deep learning scaling is predictable, empirically, 2017.
- [21]

  Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, Tom Hennigan, Eric Noland, Katie Millican, George van den Driessche, Bogdan Damoc, Aurelia Guy, Simon Osindero, Karen Simonyan, Erich Elsen, Jack W. Rae, Oriol Vinyals, and Laurent Sifre.
  Training compute-optimal large language models, 2022.
- [22]

  Dong Huang, Jie M. Zhang, Michael Luck, Qingwen Bu, Yuhao Qing, and Heming Cui.
  Agentcoder: Multi-agent-based code generation with iterative testing and optimisation, 2024.
- [23]

  Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny Zhou.
  Large language models cannot self-correct reasoning yet, 2024.
- [24]

  Binyuan Hui, Jian Yang, Zeyu Cui, Jiaxi Yang, Dayiheng Liu, Lei Zhang, Tianyu Liu, Jiajun Zhang, Bowen Yu, Kai Dang, et al.
  Qwen2. 5-coder technical report.
  arXiv preprint arXiv:2409.12186, 2024.
- [25]

  Carlos E. Jimenez, John Yang, Alexander Wettig, Shunyu Yao, Kexin Pei, Ofir Press, and Karthik Narasimhan.
  Swe-bench: Can language models resolve real-world github issues?, 2024.
- [26]

  Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei.
  Scaling laws for neural language models, 2020.
- [27]

  Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas Muennikoff, Denis Kocetkov, Chenghao Mou, Marc Marone, Christopher Akiki, Jia Li, Jenny Chim, et al.
  Starcoder: may the source be with you!, 2023.
- [28]

  Wen-Ding Li, Keya Hu, Carter Larsen, Yuqing Wu, Simon Alford, Caleb Woo, Spencer M. Dunn, Hao Tang, Michelangelo Naim, Dat Nguyen, Wei-Long Zheng, Zenna Tavares, Yewen Pu, and Kevin Ellis.
  Combining induction and transduction for abstract reasoning, 2024.
- [29]

  Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittweser, Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hubert, Peter Choy, Cyprien de Masson d’Autume, Igor Babuschkin, Xinyun Chen, Po-Sen Huang, Johannes Welbl, Sven Gowal, Alexey Cherepanov, James Molloy, Daniel J. Mankowitz, Esme Sutherland Robson, Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, and Oriol Vinyals.
  Competition-level code generation with alphacode.
  Science, 378(6624):1092–1097, December 2022.
- [30]

  Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe.
  Let’s verify step by step, 2023.
- [31]

  Junwei Liu, Kaixin Wang, Yixuan Chen, Xin Peng, Zhenpeng Chen, Lingming Zhang, and Yiling Lou.
  Large language model-based agents for software engineering: A survey, 2024.
- [32]

  Magic Team.
  100M token context windows, aug 2024.
  Blog post.
- [33]

  Shrestha Basu Mallick and Kathy Korevec.
  The next chapter of the gemini era for developers, 2024.
- [34]

  Sumeet Ramesh Motwani, Chandler Smith, Rocktim Jyoti Das, Markian Rybchuk, Philip H. S. Torr, Ivan Laptev, Fabio Pizzati, Ronald Clark, and Christian Schroeder de Witt.
  Malt: Improving reasoning with multi-agent llm training, 2024.
- [35]

  NVIDIA.
  Nvidia l40s data sheet.
  <https://resources.nvidia.com/en-us-l40s/l40s-datasheet-28413>, 2024.
  Accessed: 2024-01-14.
- [36]

  Maxwell Nye, Anders Johan Andreassen, Guy Gur-Ari, Henryk Michalewski, Jacob Austin, David Bieber, David Dohan, Aitor Lewkowycz, Maarten Bosma, David Luan, Charles Sutton, and Augustus Odena.
  Show your work: Scratchpads for intermediate computation with language models, 2021.
- [37]

  OpenAI.
  Introducing openai o1, 2024.
- [38]

  Anne Ouyang, Simon Guo, and Azalia Mirhoseini.
  Kernelbench: Can llms write gpu kernels?, 2024.
- [39]

  Sandeep Kumar Pani.
  Sota on swebench-verified: (re)learning the bitter lesson, 2024.
- [40]

  Tiernan Ray.
  Microsoft has over a million paying Github Copilot users: CEO Nadella.
  ZDNET, October 2023.
  Reports Microsoft’s GitHub Copilot reaching 1 million paid users across 37,000 organizations.
- [41]

  Haifeng Ruan, Yuntong Zhang, and Abhik Roychoudhury.
  Specrover: Code intent extraction via llms, 2024.
- [42]

  RunPod.
  Runpod cloud gpu pricing.
  <https://www.runpod.io/console/deploy>, 2024.
  Accessed: 2024-01-14.
- [43]

  Jon Saad-Falcon, Adrian Gamarra Lafuente, Shlok Natarajan, Nahum Maru, Hristo Todorov, Etash Guha, E. Kelly Buchanan, Mayee Chen, Neel Guha, Christopher Ré, and Azalia Mirhoseini.
  Archon: An architecture search framework for inference-time techniques, 2024.
- [44]

  Nikhil Sardana, Jacob Portes, Sasha Doubov, and Jonathan Frankle.
  Beyond chinchilla-optimal: Accounting for inference in language model scaling laws, 2024.
- [45]

  Erik Schluntz, Simon Biggs, Dawn Drain, Eric Christiansen, Shauna Kravec, Felipe Rosso, Nova DasSarma, and Ven Chandrasekaran.
  Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet.
  Blog post, Anthropic, oct 2024.
- [46]

  David Silver, Thomas Hubert, Julian Schrittweser, Ioannis Antonoglou, Matthew Lai, Arthur Guez, Marc Lanctot, Laurent Sifre, Dharshan Kumaran, Thore Graepel, Timothy Lillicrap, Karen Simonyan, and Demis Hassabis.
  Mastering chess and shogi by self-play with a general reinforcement learning algorithm, 2017.
- [47]

  Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar.
  Scaling llm test-time compute optimally can be more effective than scaling model parameters, 2024.
- [48]

  Hongjin Su, Ruoxi Sun, Jinsung Yoon, Pengcheng Yin, Tao Yu, and Sercan Ö. Arık.
  Learn-by-interact: A data-centric framework for self-adaptive agents in realistic environments, 2025.
- [49]

  AlphaCode Team.
  Alphacode 2 technical report, 2024.
- [50]

  Qwen Team.
  Qwq: Reflect deeply on the boundaries of the unknown, 2024.
- [51]

  Minyang Tian, Luyu Gao, Shizhuo Dylan Zhang, Xinan Chen, Cunwei Fan, Xuefei Guo, Roland Haas, Pan Ji, Kittithat Krongchon, Yao Li, Shengyan Liu, Di Luo, Yutao Ma, Hao Tong, Kha Trinh, Chenyu Tian, Zihan Wang, Bohao Wu, Yanyu Xiong, Shengzhu Yin, Minhui Zhu, Kilian Lieret, Yanxin Lu, Genglin Liu, Yufeng Du, Tianhua Tao, Ofir Press, Jamie Callan, Eliu Huerta, and Hao Peng.
  Scicode: A research coding benchmark curated by scientists, 2024.
- [52]

  Trieu H. Trinh, Yuhuai Wu, Quoc V. Le, He He, and Thang Luong.
  Solving olympiad geometry without human demonstrations.
  Nature, 625(7995):476–482, 2024.
- [53]

  Evan Wang, Federico Cassano, Catherine Wu, Yunfeng Bai, Will Song, Vaskar Nath, Ziwen Han, Sean Hendryx, Summer Yue, and Hugh Zhang.
  Planning in natural language improves llm search for code generation, 2024.
- [54]

  Junlin Wang, Jue Wang, Ben Athiwaratkun, Ce Zhang, and James Zou.
  Mixture-of-agents enhances large language model capabilities, 2024.
- [55]

  Peiyi Wang, Lei Li, Zhihong Shao, R. X. Xu, Damai Dai, Yifei Li, Deli Chen, Y. Wu, and Zhifang Sui.
  Math-shepherd: Verify and reinforce llms step-by-step without human annotations, 2024.
- [56]

  Xingyao Wang, Boxuan Li, Yufan Song, Frank F. Xu, Xiangru Tang, Mingchen Zhuge, Jiayi Pan, Yueqi Song, Bowen Li, Jaskirat Singh, Hoang H. Tran, Fuqiang Li, Ren Ma, Mingzhang Zheng, Bill Qian, Yanjun Shao, Niklas Muennikoff, Yizhe Zhang, Binyuan Hui, Junyang Lin, Robert Brennan, Hao Peng, Heng Ji, and Graham Neubig.
  Openhands: An open platform for ai software developers as generalist agents, 2024.
- [57]

  Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou.
  Self-consistency improves chain of thought reasoning in language models, 2023.
- [58]

  Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, and Denny Zhou.
  Chain-of-thought prompting elicits reasoning in large language models, 2023.
- [59]

  Yangzhen Wu, Zhiqing Sun, Shanda Li, Sean Welleck, and Yiming Yang.
  Inference scaling laws: An empirical analysis of compute-optimal inference for problem-solving with language models, 2024.
- [60]

  Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, and Lingming Zhang.
  Agentless: Demystifying llm-based software engineering agents, 2024.
- [61]

  John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, and Ofir Press.
  Swe-agent: Agent-computer interfaces enable automated software engineering, 2024.
- [62]

  Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao.
  React: Synergizing reasoning and acting in language models, 2023.
- [63]

  Wenting Zhao, Nan Jiang, Celine Lee, Justin T Chiu, Claire Cardie, Matthias Gallé, and Alexander M Rush.
  Commit0: Library generation from scratch, 2024.
- [64]

  Albert Örwall.
  Moatless tools.
  <https://github.com/aorwall/moatless-tools/tree/a1017b78e3e69e7d205b1a3faa83a7d19fce3fa6>, 2024.

## 附录 A DeepSeek-V3 结果

图 7：左：比较扩展并行样本数与串行迭代次数对 Claude 与 DeepSeek-V3 多数投票分数的影响。每条线对应固定的样本数，线上的每个点是不同的串行迭代次数上限。我们看到，虽然 Claude 能取得更高的总分，但 DeepSeek-V3 能以几分之一的成本取得该分数的 86.8%。中：DeepSeek-V3 多数投票扩展的更细致视图。右：DeepSeek-V3 的覆盖率随并行样本数与串行迭代次数的变化。我们强调，覆盖率随推理计算的增加仍在持续扩展。

在此，我们对 DeepSeek-V3（DeepSeek-AI et al., 2024）作为系统中 Claude 3.5 Sonnet 的潜在替代者进行了初步评估。我们复用了 CodeMonkeys 主实验相同的代码库上下文文件，并在 SWE-bench Verified 的一个 100 实例随机子集上用 DeepSeek-V3 重跑了我们的测试与编辑状态机。在图 7 中，我们比较了与 Claude Sonnet 3.5 相比，覆盖率与多数投票分数随样本数和迭代次数的扩展情况。我们注意到，Claude Sonnet 3.5 在这一子集上能取得 45.74% 的分数，比 DeepSeek-V3 的最佳分数高 6.02%。然而，DeepSeek API 比 Claude 便宜一个数量级以上。这些结果凸显了从 DeepSeek-V3 这类更廉价的模型生成大量候选解的潜在收益——只要选择方法能从大集合中识别出正确的样本。

## 附录 B 实验细节

我们在 <https://scalingintelligence.stanford.edu/pubs/codemonkeys/> 发布了代码与轨迹。发布内容包括：

- 运行 CodeMonkeys 求解 SWE-bench Verified 所需的全部代码。

- 生成本文图表所需的全部命令。

- CodeMonkeys 求解每个问题时走过的完整轨迹。

### B.1 状态机细节

CodeMonkeys 的三个状态机（测试、编辑与选择状态机）遵循相同的结构。每个状态机一开始向模型给出一个初始提示和一个初始任务。模型完成初始任务后，进入反馈循环。在每次迭代中，向模型提供上一次迭代的某些执行反馈。然后，模型可以修改其工作（触发循环的新一次迭代），或认可其工作（终止状态机）。在表 3 中，我们给出了三个状态机各自的输入、初始任务、每次迭代提供的信息以及每次迭代的任务。完整提示请参见我们代码库中的 codemonkeys/prompts 文件夹。

|  |  |  |  |
| --- | --- | --- | --- |
|  | 测试状态机 | 编辑状态机 | 选择状态机 |
| 初始提示中的信息 | GitHub issue 描述。 | GitHub issue 描述、代码库上下文、来自某个测试状态机的最终测试脚本、在未编辑代码库上运行所提供测试的执行输出。 | GitHub issue 描述、git diff 形式的候选编辑、所有已被编辑的代码库文件的完整内容、来自通过最多生成测试的那个编辑的测试脚本（并列时取最短编辑）。 |
| 初始任务 | 编写一个复现该 issue 的测试脚本。脚本应在 issue 已修复时以退出码 0 退出，在 issue 未修复时以退出码 2 退出。 | 编写一个解决该 issue 的代码库编辑。 | 编写一个用于区分候选并评估其正确性的测试脚本。 |
| 迭代提示中的信息 | 在（尚未编辑的）代码库上运行测试的执行输出。 | 在未编辑代码库与已编辑代码库上运行测试脚本的执行输出。 | 在应用每个编辑后的代码库以及未编辑代码库上运行测试脚本的执行输出。 |
| 迭代任务 | 重写测试脚本或认可它（终止状态机）。 | 重写编辑、重写测试脚本，或认可（编辑，测试）对（终止状态机）。 | 编写新的测试脚本，或在候选编辑之间做出选择（终止状态机）。 |

表 3：测试、编辑与选择状态机的细节。

### B.2 超参数

我们在表 4 中详述各部分的其他实验细节。

|  |  |  |  |
| --- | --- | --- | --- |
| 子任务 | 阶段 | 参数 | 取值 |
| 上下文 | 相关性 | 模型 | Qwen-2.5-Coder-32B-Instruct |
|  |  | 硬件 | 8xL40S |
|  |  | 温度 | 0.0 |
|  | 排序 | 模型 | Claude Sonnet 3.5 |
|  |  | 温度 | 0.0 |
|  |  | 重复次数 | 3 |
| 生成 | 测试与编辑 | 温度（Sonnet 3.5） | 0.5 |
|  |  | 温度（DeepSeek-V3） | 0.6 |
|  |  | 每实例状态机数量 | 10 |
|  |  | 最大迭代次数 | 8 |
|  |  | 生成测试超时（秒） | 100 |
| 选择 | — | 温度 | 0.0 |
|  |  | 最大迭代次数 | 10 |
|  |  | 生成测试超时（秒） | 100 |

表 4：CodeMonkeys 超参数汇总。

## 附录 C 相关性阶段的本地计算

在相关性阶段，我们在 8xL40S GPU 上以 bf16 本地运行 Qwen-2.5-Coder-32B-Instruct（Hui et al., 2024）。每块 L40S 的 bf16 计算吞吐为 362.05 TFLOPS（NVIDIA, 2024），因此我们节点的理论吞吐量为：

$$8\text{ devices}\cdot 362.05\text{ TFLOPS/device}=2{,}896.4\text{ TFLOPS}$$

由于我们运行的模型是一个无参数共享的稠密 Transformer，我们可以把每 token 的 FLOPs 估计为 2 × 参数量（Sardana et al., 2024）。假设推理期间的硬件利用率为 20%，我们得到每节点的吞吐量为：

$$\text{Throughput}\approx\frac{0.2\cdot 2{,}896.4\cdot 10^{12}\text{ FLOPs/second}}{2\cdot 32\cdot 10^{9}\text{ FLOPs/token}}=9{,}051\text{ tokens/second}$$

在 SWE-bench Verified 的 500 个实例上，相关性阶段需要处理总计 $1.32084\cdot 10^{9}$ 个 token。为估算计算成本，我们使用 RunPod 的定价：一个 8xL40S 节点每小时 8.24 美元（RunPod, 2024），由此得到总成本：

$$\text{Relevance cost}\approx\frac{1.32083\cdot 10^{9}\text{ tokens}}{9{,}051\text{ tokens/second}\cdot 3{,}600\text{ seconds/hour}}\cdot \$8.24/\text{hour}$$

$$=40.5\text{ hours}\cdot \$8.24/\text{hour}=\$334.02$$
