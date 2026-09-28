---
title: "衡量 AI 完成长任务的能力"
title_en: "Measuring AI Ability to Complete Long Software Tasks"
arxiv: 2503.14499
source: https://arxiv.org/abs/2503.14499
crawled: 2026-09-23
translated: 2026-09-23
---

# 衡量 AI 完成长任务的能力

> 原文：[Measuring AI Ability to Complete Long Software Tasks](https://arxiv.org/abs/2503.14499) · Stanford CS329A 指定阅读

Thomas Kwa†、Ben West†、Joel Becker、Amy Deng、Katharyn Garcia、Max Hasin、Sami Jawhar、Megan Kinniment、Nate Rush、Sydney Von Arx、Ryan Bloom、Thomas Broadley、Haoxing Du、Brian Goodrich、Nikola Jurkovic、Luke Harold Miles、Seraphina Nix、Tao Lin、Chris Painter、Neev Parikh、David Rein、Lucas Jun Koba Sato、Hjalmar Wijk、Daniel M. Ziegler、Elizabeth Barnes、Lawrence Chan

（Model Evaluation & Threat Research（METR））

注：† 表示同等贡献。通讯作者：thomas.kwa@metr.org。Ohm Chip（工作完成于 METR）；Anthropic（工作完成于 METR）。

###### 摘要

尽管 AI 基准测试进展迅速，基准表现在现实世界中的含义仍不清楚。为了用人类能力来量化 AI 系统的能力，我们提出一个新指标：*50% 任务完成时间视界*（50%-task-completion time horizon），即 AI 模型能以 50% 成功率完成的任务，人类通常需要花费的时间。我们首先让具有相关领域专业知识的人类在 RE-Bench、HCAST 与 66 个新的较短任务的组合上计时。在这些任务上，当前的前沿 AI 模型（如 o3）的 50% 时间视界约为 110 分钟。此外，自 2019 年以来，前沿 AI 的时间视界大约每七个月翻一番，不过该趋势自 2024 年以来可能有所加速。AI 模型时间视界的增长似乎主要由更高的可靠性、适应错误的能力、逻辑推理与工具使用能力所驱动。我们讨论了结果的局限——包括其外部效度程度——以及自主性增强对危险能力的影响。如果这些结果能推广到真实世界软件任务，对该趋势的外推预测：在 5 年内，AI 系统将能够自动化许多目前人类需要一个月才能完成的软件任务。

## 1 引言

![Refer to caption](2503.14499v4/plots/bootstrap/headline-log.png)

图 1：通用自主前沿模型智能体能够以 50% 可靠性完成的任务长度（以人类专业人士完成所需时长衡量），在过去 6 年里大约每 7 个月翻一番（第 3 节）。阴影区域表示对任务族、任务与任务尝试做分层自助抽样得到的 95% 置信区间。即便绝对测量偏差 10 倍，该趋势也预测：不出十年，我们将看到能够独立完成很大一部分目前人类需要数天或数周才能完成的软件任务的 AI 智能体（第 5 节）。

在过去五年里，前沿 AI 系统的能力发生了戏剧性的转变，从基础的文本生成（Radford et al., 2019）演进到自主执行复杂的多小时机器学习研究项目（Wijk et al., 2024）。足够强大的 AI 可能执行危险且高度复杂的行动，例如自主开发生化放核武器（CBRN）以及在人类控制之外自我复制与适应（Phuong et al., 2024）。理解 AI 能力有助于在系统日益强大时为安全护栏的开发提供信息。特别是，许多前沿 AI 开发者已承诺使用特定 AI 能力的度量来确定其前沿 AI 系统所需的风险缓解措施。能够准确追踪与预测 AI 能力的稳健基准，因此构成负责任 AI 治理与风险缓解的基础。

然而，现有基准面临若干关键局限。第一，它们通常由人工构造的而非有经济价值的任务组成。第二，基准往往被对抗性地选择为当前模型相对人类表现吃力的任务[注1](#fn1)，使与人类表现的比较有偏。最关键的是，单个基准饱和得越来越快（Maslej et al., 2024），而我们缺乏一种更通用、直观且量化的方式在不同基准之间比较[注2](#fn2)，这阻碍了对能力差异巨大的模型（例如 GPT-2 与 Claude 3.7）之间做有意义的比较。因此，尽管过去几年 AI 在许多单个基准上的表现大幅提升，理解 AI 能力的总体进展一直需要估算 AI 系统所能通过的最新基准的*定性难度*。

注 1：例如 HellaSwag（Zellers et al., 2019）与 Humanity's Last Exam（Phan et al., 2025）都是通过用当时最强的语言模型做对抗性过滤来生成问题的。

注 2：SWE-bench Verified（Chowdhury et al., 2024）确实附带人工估计的任务完成时间。我们在第 4.1 节使用 SWE-bench Verified 任务及其时间估计来验证主要结果。

我们提议用任务完成时间视界（task completion time horizon）来追踪 AI 随时间的进展：模型能以某一成功概率完成的任务时长，相比人类提供了一种直观的真实世界能力度量。由于模型可能无法可靠地完成给定长度的*所有*任务，我们将其操作化为测量 X%（任务完成）时间视界——模型大约有 X% 的时间能完成的任务长度。

我们用三个旨在捕捉研究或软件工程所需技能的数据集来原型化这一方法（第 2.1 节），共 170 个任务、难度跨度极大：HCAST（Rein et al., 2025）、RE-Bench（Wijk et al., 2024），以及软件原子动作（Software Atomic Actions，SWAA）——一套可以衡量 2023 年之前模型的较短软件任务（附录 B.1.3）。借助熟练的人类基线者（baseliner），我们估计具备领域知识（但无任务特定上下文）的人类完成这些任务所需的时长（第 2.2 节）。我们评估 2019 至 2025 年间 12 个前沿模型在这些任务上的表现（第 2.3 节）。随后，借鉴人类心理测量学的方法，我们估计模型能以 50% 成功率完成的任务时长——即 50% 时间视界（第 3.1 节）。

我们发现，2019-2025 年间这些任务的 50% 时间视界呈指数增长，倍增时间约为七个月（图 1）。我们把主要结果与非 SWAA 任务上的探索性结果比较，发现 2023-2025 年的视界增长率约比 2019-2025 年快 20%（附录 F.1）。我们还测量了模型的 80% 时间视界（图 17），发现趋势相似，但视界大约短 5 倍。这一进展似乎由几个关键因素驱动：逻辑推理的改进、更好的工具使用，以及任务执行中更高的可靠性与自我觉察（第 3.3 节）。我们还指出当前系统的若干局限—— notably，在结构化程度更低、「更杂乱」的任务上表现差得多（附录 F.2）。

由于我们的任务并不能完美代表研究者与软件工程师智力劳动的平均片段，这引出了外部效度问题（第 4 节）：指数趋势是否在真实世界任务上成立。我们纳入三个补充性的外部效度实验，它们没有发现证据表明在我们测试的较为真实的任务上性能趋势更慢，但不能排除在自动化软件工程师岗位所需的任务分布上趋势显著更慢的可能性。我们还发现证据表明，AI 智能体的时间视界会因任务领域与参考人类群体的不同而相差很大。

最后讨论对 AI 能力预测的意义（第 5 节）。朴素地外推视界长度趋势意味着，AI 将在 2028 年中到 2031 年中之间达到 >1 个月（167 个工作小时）的时间视界（图 6）。不过，外推受外部效度疑虑与趋势未来变化两方面影响。

![Refer to caption](2503.14499v4/images/methodology_new.png)

图 2：我们测量 AI 智能体时间视界的方法。第一，我们创建一个含 170 个任务的多样任务套件。第二，我们让人类与 AI 智能体（由 AI 模型加脚手架组成）都尝试这些任务，记录成功人类所花时间与 AI 智能体的成功率。第三，我们拟合逻辑斯蒂模型，找出每个 AI 智能体有 50% 成功概率的时间视界，并对照模型发布日期绘图。

### 1.1 相关工作

这里我们简要讨论相关工作。扩展讨论见附录 A。

##### 智能体式 AI 能力基准

许多近期基准旨在衡量 AI 系统作为通用智能体的能力，包括 AgentBench（Liu et al., 2023）、ToolBench（Guo et al., 2024）、GAIA（Mialon et al., 2024）、TheAgentCompany（Xu et al., 2024）与 Berkeley Function Calling Leaderboard（Yan et al., 2024）。在本工作中，我们研究 AI 智能体在 RE-Bench（Wijk et al., 2024）、HCAST（Rein et al., 2025）与 SWE-Bench Verified（Chowdhury et al., 2024）上的表现，它们聚焦机器学习与软件工程任务。其他类似基准包括 MLAgentBench（Huang et al., 2024）、MLEBench（Chan et al., 2024）与 DSBench（Jing et al., 2024）。在同期工作中，Miserendino et al.（2025）创建了 SWE-Lancer 基准，由从 Upwork 收集的 1,400 个自由职业软件工程任务组成，真实报酬总额超过 100 万美元。

##### AI 能力预测

本工作建立在以往预测 AI 系统能力随时间变化的工作之上，包括用人类专家来语境化基准表现的努力（Phuong et al., 2024；Murray et al., 2025），以及预测特定基准表现的努力（Owen, 2024；Pimpale et al., 2025）。用人类时间视界来语境化 AI 能力由 Ngo（2023）提出，类似概念在 Carlsmith（2020）与 Cotra（2020）中亦有讨论。

##### 人类心理测量方法

我们的方法借鉴了人类心理测量测试，尤其是项目反应理论（Item Response Theory）（Baker, 2001；de Ayala, 2017；Martínez-Plumed et al., 2019）。

## 2 测量 AI 智能体在真实任务上的表现

### 2.1 任务套件 / 数据集

我们的任务由三个不同的任务套件组成：

1. HCAST（Rein et al., 2025）的一个子集：97 个多样的软件任务，时长从 1 分钟到 30 小时[注3](#fn3)。

   注 3：我们的结果还包括来自 GAIA（Mialon et al., 2024）的一个任务，以及五个涉及编写能抵御对手的代码的任务。

2. RE-Bench（Wijk et al., 2024）：7 个困难的机器学习研究工程任务，全部为八小时长。

3. 软件原子动作（SWAA）：66 个单步任务，代表软件开发者工作中较短的片段，时长从 1 秒到 30 秒。

所有任务都以连续分数或二元阈值自动评分；我们如何归一化与处理分数的细节见第 3.1 节，任务套件的其他细节见附录 B。

##### 示例任务

表 1 给出五个示例任务。1 分钟以下的任务衡量与专业软件工程相关的知识。在 10 分钟处，任务可以包括真实软件项目中最简单而有意义的一步（例如配置一个常见的开源软件包）。可以作为独立的有经济价值项目的最短任务约需一小时；到八小时，任务代表有价值的软件项目。更多任务示例见 Wijk et al.（2024）与 Rein et al.（2025）。

| 任务族 | 时长 | 描述 |
| --- | --- | --- |
| find_shell_script | 3 秒 | 多选题：「哪个文件是 shell 脚本？」选项：“run.sh”、“run.txt”、“run.py”、“run.md” |
| wikipedia_research | 1 分钟 | 从维基百科研究简单的事实信息，并就直白的问题给出准确回答。 |
| oxdna_simple | 9 分钟 | 使用 oxDNA 软件包检测并修复分子动力学模拟输入文件中的一个 bug。 |
| munge_data | 56 分钟 | 编写一个 Python 脚本，通过从提供的示例文件推断转换规则，把 JSON 数据从一种格式转换为另一种。 |
| cuda_backtesting | 8 小时 | 通过实现自定义 CUDA 内核加速一个交易执行的 Python 回测工具，同时保留所有功能，目标是 30 倍性能提升。 |

表 1：不同时长的示例任务；更多示例见 Rein et al.（2025）与 Wijk et al.（2024）。

### 2.2 基线测量

为了给 AI 智能体的表现提供参照，我们还测量多名人类「基线者」在大多数任务上的表现，并记录其尝试的时长。总共，我们使用了超过 800 次基线、共计 2,529 小时，其中 558 次（286 次成功）来自 HCAST 与 RE-Bench，249 次（236 次成功）来自较短的 SWAA 任务。169 个任务中有 148 个有人类基线，但对 HCAST 中的 21 个任务我们依赖研究者的估计。

我们的基线者是软件工程、机器学习与网络安全领域的熟练专业人士，大多就读过世界前 100 的大学。他们平均有约 5 年相关经验，其中软件工程基线者的经验多于机器学习或网络安全基线者。基线的更多细节见附录 C.1。

### 2.3 结果

我们测量 2019 至 2025 年间发布的 12 个前沿（及 4 个近前沿）模型；模型与所用脚手架的完整信息见附录 C.3。我们对每个智能体/任务对执行 8 次运行[注4](#fn4)，并在图 3 中报告平均结果。随时间有强劲的上升趋势，近期模型完成约 50% 的全部任务，而早期模型的表现差得多。我们发现各模型能完成的任务之间有显著相关（图 22），平均相关约 0.73。

注 4：该数字是近似的，因为有少量运行因内部基础设施问题而失败。

![Refer to caption](2503.14499v4/plots/bar_chart_weighted_scores/headline.png)

![Refer to caption](2503.14499v4/plots/success_rates/model_success_rate_vs_human_completion_time.png)

图 3：左：每个模型在整个合并套件上的平均任务成功率。与本文正文报告的所有结果一样，为降低大任务族的影响，我们对每个任务按其所属族中任务数的平方根倒数加权。右：模型成功率与人类完成任务所需时间呈负相关。（$y=-0.07x+0.66$，$R^{2}$：0.83）

人类基线者完成一个任务所需时间与该任务上的平均成功率（跨所有模型）之间存在负相关。成功率随长度的这种下降（图 3）用指数模型拟合得很好（把模型成功率对人类完成时间的对数做回归，$R^{2}\approx 0.80$）。正如预期，更新的模型能完成更长的任务，Claude 3.7 Sonnet 与 o3 能完成一些人类基线者需 >4 小时的任务（图 4）。

## 3 时间视界

### 3.1 计算时间视界

为把智能体运行数据转换为任务完成时间视界，我们首先把智能体在每个任务上的表现转换为二元值（成功或失败）。许多任务天然是二元的，包括全部 SWAA 任务。连续计分的任务通过一个任务特定的阈值二值化，该阈值选取为代表人类表现。对 HCAST，任务特定阈值与人类基线者试图达到的「目标分数」相同，我们也用它筛选成功的运行。RE-Bench 任务有固定的 8 小时时长评级，因此任务特定阈值是 7-9 小时人类运行的平均分。

![Refer to caption](2503.14499v4/plots/individual_histograms/default/histograms.png)

图 4：所有模型在测试套件上的成功率，展示时间视界作为预测 50% 成功率时间的计算方式。逻辑斯蒂拟合相当好，不过在 <1 分钟的 SWAA 任务与 >1 分钟的 HCAST 任务之间成功率有一个跳变。

一旦获得每个任务的智能体成功率与时长评级，我们通过以下逻辑斯蒂回归拟合时间视界[注5](#fn5)：

注 5：与项目反应理论（IRT）（Baker, 2001）相比：与 IRT 一样，我们用逻辑斯蒂回归找出智能体有 50% 成功概率的任务难度，但与 IRT 不同，我们直接使用基于人类基线时间的难度评级，而非从智能体表现中学习的评级。更多细节及与标准 IRT 方法的比较见附录 C.4。

$$p_{\mathrm{success}}(\mathrm{agent},\mathrm{task})=\sigma((\log h_{\mathrm{agent}}-\log t_{\mathrm{task}})\cdot\beta_{\mathrm{agent}})$$

其中 $t_{\mathrm{task}}$ 是成功人类基线的几何平均时间，$h_{\mathrm{agent}}$ 与 $\beta_{\mathrm{agent}}$ 是学习到的参数，$h_{\mathrm{agent}}$ 表示 50% 时间视界。

### 3.2 时间视界与发布日期

在图 1 中，我们把每个模型的时间视界对其发布日期作图——即实验室首次公开发布该前沿模型的日期[注6](#fn6)。此外，我们把 $\log(\text{时间视界})$ 对发布日期做线性回归[注7](#fn7)，发现时间视界每 207 天翻一番，95% 自助置信区间为 166-240 天（约 $\pm 19\%$）。误差棒由对任务族、再到任务、再到运行的三层分层自助抽样取 10,000 个样本计算。

注 6：在多数情况下，发布日期对应的前沿 AI 模型与我们评估的是同一模型。但 GPT-3（davinci）与 GPT-3.5（code-davinci-002 与 text-davinci-002）已闭源且无法再通过 API 访问，我们使用最接近的可用模型（OpenAI 宣称其性能相当）的发布日期：davinci-002 用 GPT-3 的发布日期，gpt3.5-turbo-instruct 用 GPT-3.5 的日期。

注 7：具体而言，我们对 $\log(\text{model\_horizon})=\alpha+\beta\cdot\text{release\_date}$ 做普通最小二乘回归。附录 H 讨论了其他曲线拟合方法，并结论是拟合对正则化、任务加权、WLS 与 OLS 等各种超参数不敏感。

虽然每个模型各自的视界长度误差棒很宽，但这些误差在模型之间高度相关。这是因为相同人类时长评级的任务对模型的难度差异很大，采样到简单（或困难）的任务会导致所有模型的视界估计偏高（或偏低）。因此，我们对时间视界趋势的斜率比对任何特定模型的时间视界更有信心。该拟合对正则化、任务加权、WLS 与 OLS 等各种超参数不敏感（见图 6）。

从 2019 到 2025 年初的整段时间内，视界长度显著增长。GPT-2 的 50% 时间视界只有 2 秒，而 o3 的时间视界为 110 分钟，并成功完成若干超过 4 小时的任务。此外，o3 位于长期趋势之上（p = 0.006）；这对使用连续计分等方法学消融稳健（附录 H），这可能意味着 2024 年与 2025 年初的趋势更快。

#### 3.2.1 50% 成功率与 80% 成功率的时间视界

为检查我们选择 50% 成功率是否影响长期趋势，我们还计算了 AI 智能体以 80% 成功率成功完成任务的时间视界，见图 17。80% 时间视界的倍增时间（204 天）与 50% 时间视界的倍增时间（207 天）在误差范围内相似。但模型的 80% 时间视界短 4-6 倍，表明即使有时能在困难且多样的任务上成功的模型，也无法可靠地执行中等长度的任务。由于数据集有限，我们无法可信地测量非常高成功率（如 95%）下的时间视界——见第 E.3 节。

### 3.3 定性分析

通过检视 31 次随机抽样 的 GPT-4 1106 智能体失败运行与 32 次 o1 失败运行的轨迹，我们观察到模型在工具使用能力上似乎大幅提升，展现出明显更强的适应错误的能力（而非重复不成功的行动），并在需要逻辑推理或代码生成的任务部分表现好得多。然而，我们注意到 AI 智能体在直觉上「更杂乱」的环境中似乎仍然吃力——具体而言，是没有清晰反馈回路的环境，或智能体需要主动搜寻相关信息的场合。

表 2 展示按模型分类的失败。我们在附录 D 中提供这些类别的定义，以及定性改进与持续局限的示例。

  

| 失败类型 | GPT-4 1106 | o1 |
| --- | --- | --- |
| 规划/工具选择不佳 | 4 | 6 |
| 心算/推理错误 | 6 | 7 |
| 过早放弃任务 | 8 | 16 |
| 重复失败的操作 | 12 | 2 |
| 其他 | 1 | 1 |
| 总计 | 31 | 32 |

表 2：对 GPT-4 1106 的 31 次失败运行与 o1 的 32 次失败运行的分类（第 3.3 节）。注意，由于 o1 成功的任务更多，其失败对应于比 GPT-4 的失败更具挑战性的任务。

## 4 外部效度与稳健性

我们检验了不含 SWAA 数据集的 2023-2025 趋势能否回测自 2019 年以来的趋势，发现两者一致。我们还做了三个实验来检验外部效度。

第一，我们在 SWE-bench Verified 上复现我们的方法。我们发现指数趋势仍然成立（图 5）， albeit 倍增时间更短，可能因为 SWE-bench Verified 的难度标注本意是代表高上下文维护者时间，可能不成比例地低估人类承包商完成较简单 SWE-bench 任务所花的时间。

第二，我们用一个包含 16 项「杂乱度」（messiness）因子的清单对 HCAST 与 RE-Bench 任务评分，这些因子旨在捕捉此处研究的任务与困难「真实世界」任务之间的某些系统性差异。一些例子包括任务是否受资源限制、是否新颖、或是否涉及动态环境（第 H.6 节）。在控制任务长度后，我们发现模型在杂乱度得分较高的任务上表现更差。值得注意的是，这些任务中较低与较高杂乱度子集的 AI 智能体表现随时间的趋势相似（见图 12）。特别是，我们没有发现较高杂乱度子集特有的表现趋势平台期。

第三，我们测量 AI 智能体在我们内部拉取请求（PR）的一个小的、未受污染的集合上的表现（第 C.2 节）。我们发现不同人类群体完成内部 PR 任务的速度差异巨大，承包商修复 issue 的时间是仓库维护者的 5-18 倍。我们还发现，若以维护者完成时间作为任务长度的度量，AI 智能体表现比预测更差；但与承包商完成时间一致。

SWE-bench Verified 的信息如下。回测与杂乱度分析的细节见附录 F，内部 PR 实验的细节见第 C.2 节。

### 4.1 SWE-bench Verified

为检查我们是否在其他基准上观察到类似的性能趋势，我们把方法应用于 SWE-bench Verified——一个评估语言模型在软件工程任务上表现的行业标准基准（OpenAI, 2025）。SWE-bench Verified 数据集中的全部任务收集自大型开源仓库（如 matplotlib 或 django），并经过筛选以确保可自动检查、规约明确（Jimenez et al., 2024）。

![Refer to caption](2503.14499v4/plots/logistic/swe_bench.png)

图 5：
  
基于公开报告的 SWE-bench Verified 结果的前沿 AI 模型表现（第 4.1 节）。我们观察到与图 1 类似的指数趋势， albeit 斜率更陡。

从 SWE-bench Verified 任务计算出的模型时间视界似乎遵循从 2023 年末到 2024 年的指数趋势。然而，用 2024 年模型在 HCAST + SWAA + RE-bench 上预测的倍增时间为 143 天，而 SWE-bench Verified 结果上的倍增时间更短——约 70 天。

SWE-bench Verified 的时间标注基于「一位花了几小时熟悉代码库的工程师」解决该 issue 预计所需的时间（Jimenez et al., 2024）。我们发现标注者的时间估计不成比例地低估了我们的承包基线者完成最容易的 SWE-bench Verified 任务所花的时间。因此，我们（使用标注时间的）SWE-bench Verified 时间视界估计可能相对承包商时间低估了能力较弱模型的时间视界，进而缩短倍增时间。更多细节见附录 H.5。

## 5 外推

##### 向一个月视界 AI 外推

为预测 AI 系统何时可能有能力自主创造巨大经济价值并采取潜在灾难性行动，我们选择一个月（为与人类公平比较约 167 个工作小时，因为人类不能 7×24 小时工作），理由有二。第一，Ngo（2023）写道，1 个月 AGI（定义为在给定 1 个月工作时长即 167 小时的任务上超越大多数知识渊博人类的 AI）必然在编写大型软件应用、创办初创公司、做出新颖科学发现等有经济价值的事业上超越人类表现[注8](#fn8)。第二，一个月大约是公司新员工开始完成入职并产生经济价值的时期[注9](#fn9)，因此视界为 1 个月的 AI 可能有能力像人类员工那样获取上下文，从而既能完成高上下文也能完成低上下文任务。我们不能排除一个能完成 1 个月任务的系统——即便只有 50% 的可靠性——会对我们的社会产生变革性影响，包括造成灾难性伤害的能力。

注 8：注意我们的预测针对在软件任务上有 1 个月视界的 AI，而非 1 个月 AGI，因为我们只在软件与研究任务上评估模型。不过，鉴于过去 AI 各领域表现之间的相关性，具有 1 个月（167 小时）时间视界的 AI 可能具有显著的通用能力。

注 9：入职「可能持续几周到一年多」（Zielinski, 2019），员工往往在入职过程中途就开始产生经济价值。

![Refer to caption](2503.14499v4/plots/multiverse/boxplot.png)

图 6：对前沿 AI 系统达到 1 个月视界日期的外推敏感性分析。每一行，我们对数据施加 10,000 次随机扰动，并求扰动数据所蕴含的 1 个月 AI 日期分布。箱体端点表示第 25 与 75 百分位，须线表示第 10 与 90 百分位，离群值未显示。注意此图未考虑趋势的未来变化或外部效度疑虑，而这些是我们不确定性的主要来源。

##### 敏感性分析

图 6 展示了结果对各种噪声来源的敏感性分析。「Bootstrap（任务）」「Bootstrap（运行）」与「Bootstrap（模型）」分别代表任务数量有限、运行间方差与模型数量有限。「加权/正则化」代表方法学选择；该扰动包括 10 种超参数组合（有/无任务多样性加权，逻辑斯蒂回归正则化参数在 0.01 到 0.2 之间）。「IID 基线噪声」依据基线时间的经验分布给每个任务时长乘一个随机因子。注意我们对仅 2024-2025 趋势的信心较低，因为该时间段只有七个前沿模型。

由于我们的分析认为我们任务上时间视界增长率比每 8 个月翻一番慢得多的概率很低，1 个月 AI 外推日期的不确定性相当小（80% 置信区间宽度约 2 年，中心估计 2029 年中）。如果未来进展转而遵循 2024-2025 趋势，1 个月 AI 会更早到来，一半概率在 2027 年、甚至 2026 年末。

系统性偏置与替代方法学可能对预测有更大影响，我们在附录 H 中讨论。此外，由于预测未来固有的困难，真实预测的误差会大于这一朴素外推，我们在下面讨论。

##### 任务分布局限

我们在附录 B.2 中指出此任务套件与真实任务的若干差异：简言之，真实任务很少有自动评分，且往往需要应对其他智能体、资源约束、动态环境与高可靠性要求。这些差异使人怀疑在此任务套件（及其他基准）上看到的快速性能改进能否推广。可能 HCAST 与 SWE-Bench Verified 这类基准不足以预测真实世界的 AI 能力，准确的预测将需要有意识地构建没有这些局限的更真实基准。

##### 时间视界趋势的未来变化

时间视界趋势未来可能因智能体式训练（agency training）、算力扩展与 AI 研发自动化等因素而显著改变。智能体式训练与最终的 AI 研发自动化更可能加速趋势，而算力扩展可能使其放缓（但被算法进步部分抵消）；未来的通用人工智能（AGI）严格来说可以拥有无限的时间视界。细节见附录 E。

## 6 讨论

##### 总结

本文提出了一个直观、量化的 AI 能力度量：任务完成时间视界，它把 AI 在任务上的表现与人类专家完成这些任务通常所需的时长联系起来。我们构建了 66 个较短 SWAA 任务的数据集，把它们与现有基准结合，并进行基线测量以估计难度。为测量时间视界的趋势，我们在此数据集上对 2019 至 2025 年间发布的 11 个前沿 AI 模型做基准测试，并发现（第 3 节）这些任务上的 50% 任务完成时间视界在 2019-2025 年间呈指数增长，倍增时间约七个月（图 1）。我们还指出当前系统的重要局限，尤其它们在结构化程度更低、「更杂乱」任务上的较低表现（附录 F.2）。

最后，我们尝试把这些任务上的趋势外推到一个月（167 小时）AI（第 5 节），发现如果趋势持续且观察到的性能趋势能推广到真实世界任务，能完成 1 个月长软件任务的 AI 的发布日期的 80% 置信区间为 2028 年中到 2030 年中——如果 2024-2025 趋势持续，甚至可能早至 2027 年初。

##### 局限与未来工作

尽管我们相信指数趋势是稳健的，我们提醒：时间视界总是相对某个领域、任务分布以及人类基线者的技能与上下文水平测量的，实践中可能难以测量，尤其是对更长的视界或接近 100% 的成功率。我们在附录 E.3 中讨论解读时间视界的细微之处。最后，我们在附录 E.4 中讨论扩展或改进我们结果的方式，例如研究多个领域、更多模型、更好的性能引出（elicitation）、推理扩展或其他统计方法。

## 致谢与资金披露

作者感谢以下评审者对本文草稿版本的反馈：Ryan Greenblatt、Aaron Scher、Romeo Dean、Mike Knoop、Jeff Wu、Steve Newman、Rohit Krishnan、Taren Stinebrickner-Kauffman、JS Denain、Jacob Pfau、Seb Krier、Anton Troynikov、Max Henderson、Ajeya Cotra、Max Nadeau、Tamay Besiroglu、Nate Thomas。作者感谢 Charles Foster 与 Michael Chen 对发表的支持。

我们特别感谢以下评审者的实质性反馈：Sara Fish、David Duvenaud、Eli Lifland、Holden Karnofsky 与 Rif A. Saurous。我们也感谢 Stephanie He 为图 2 做的平面设计工作，以及 Ryan Greenblatt 对评分方法的意见。

## 参考文献


- Amodei and Hernandez (2018)
  D. Amodei and D. Hernandez
  AI and compute.
  Note: OpenAI blog post, May 16, 2018
  External Links: [Link](https://openai.com/blog/ai-and-compute/)
- Austin et al. (2021)
  J. Austin A. Odena et al.
  Program synthesis with large language models.
  Note: arXiv preprint, arXiv:2108.07732
  External Links: [Link](https://arxiv.org/abs/2108.07732)
- Baker (2001)
  F. B. Baker
  The basics of item response theory.
   ERIC.
- Carlsmith (2020)
  J. Carlsmith
  How much computational power does it take to match the human brain?.
  Note: Open Philanthropy report, August 14, 2020
  External Links: [Link](https://www.openphilanthropy.org/research/how-much-computational-power-does-it-take-to-match-the-human-brain/)
- Chan et al. (2024)
  J. S. Chan, N. Chowdhury, O. Jaffe, J. Aung, D. Sherburn, E. Mays, G. Starace, K. Liu, L. Maksin, T. Patwardhan, L. Weng, and A. Madry
  MLE-bench: evaluating machine learning agents on machine learning engineering.
  External Links: 2410.07095,
  [Link](https://arxiv.org/abs/2410.07095)
- Chen et al. (2021)
  M. Chen, J. Tworek, H. Jun, Q. Yuan, H. Ponde de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, et al.
  Evaluating large language models trained on code.
  Note: arXiv preprint, arXiv:2107.03374
  External Links: [Link](https://arxiv.org/abs/2107.03374)
- Chowdhury et al. (2024)
  N. Chowdhury, J. Aung, C. J. Shern, O. Jaffe, D. Sherburn, G. Starace, E. Mays, R. Dias, M. Aljubeh, M. Glaese, C. E. Jimenez, J. Yang, L. Ho, T. Patwardhan, K. Liu, and A. Madry
  Introducing SWE-bench verified.
  Note: <https://openai.com/index/introducing-swe-bench-verified/>Accessed: 2025-02-26
- Cobbe et al. (2021)
  K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al.
  Training verifiers to solve math word problems.
  arXiv preprint arXiv:2110.14168.
- Cotra (2020)
  A. Cotra
  Draft report on ai timelines.
  Note: Draft report on AI timelines; technical report
  External Links: [Link](https://www.alignmentforum.org/posts/KrJfoZzpSDpnrv9va/draft-report-on-ai-timelines)
- de Ayala (2017)
  R. J. de Ayala
  Handbook of item response theory: models, applications, and issues.
   Guilford Press.
- Epoch AI (2024)
  Epoch AI
  Data on notable AI models.
  Note: Accessed: 2025-03-04
  External Links: [Link](https://epoch.ai/data/notable-ai-models)
- Erdil and Besiroglu (2023)
  E. Erdil and T. Besiroglu
  Algorithmic progress in computer vision.
  External Links: 2212.05153,
  [Link](https://arxiv.org/abs/2212.05153)
- Guo et al. (2024)
  Z. Guo, S. Cheng, H. Wang, S. Liang, Y. Qin, P. Li, Z. Liu, M. Sun, and Y. Liu
  StableToolBench: towards stable large-scale benchmarking on tool learning of large language models.
  External Links: 2403.07714
- Hendrycks et al. (2021)
  D. Hendrycks, S. Basart, S. Kadavath, M. Mazeika, A. Arora, E. Guo, C. Burns, S. Puranik, H. He, D. Song, et al.
  Measuring coding challenge competence with apps.
  In Advances in Neural Information Processing Systems (NeurIPS) Datasets and Benchmarks Track,
  External Links: [Link](https://arxiv.org/abs/2105.09938)
- Hendrycks et al. (2020)
  D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt
  Measuring massive multitask language understanding.
  CoRR abs/2009.03300.
  External Links: [Link](https://arxiv.org/abs/2009.03300),
  2009.03300
- Ho et al. (2024)
  A. Ho, T. Besiroglu, E. Erdil, D. Owen, R. Rahman, Z. C. Guo, D. Atkinson, N. Thompson, and J. Sevilla
  Algorithmic progress in language models.
  External Links: 2403.05812,
  [Link](https://arxiv.org/abs/2403.05812)
- Huang et al. (2024)
  Q. Huang, J. Vora, P. Liang, and J. Leskovec
  MLAgentBench: evaluating language agents on machine learning experimentation.
  In Proceedings of the 41st International Conference on Machine Learning,
  ICML’24.
- Jiang et al. (2025)
  Z. Jiang, D. Schmidt, D. Srikanth, D. Xu, I. Kaplan, D. Jacenko, and Y. Wu
  AIDE: ai-driven exploration in the space of code.
  arXiv preprint arXiv:2502.13138.
- Jimenez et al. (2024)
  C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. R. Narasimhan
  SWE-bench: can language models resolve real-world github issues?.
  In The Twelfth International Conference on Learning Representations,
  External Links: [Link](https://openreview.net/forum?id=VTF8yNQM66)
- Jing et al. (2024)
  L. Jing, Z. Huang, X. Wang, W. Yao, W. Yu, K. Ma, H. Zhang, X. Du, and D. Yu
  DSBench: how far are data science agents to becoming data science experts?.
  arXiv preprint arXiv:2409.07703.
- Kipnis et al. (2025)
  A. Kipnis, K. Voudouris, L. M. S. Buschoff, and E. Schulz
  Metabench – a sparse benchmark of reasoning and knowledge in large language models.
  External Links: 2407.12844,
  [Link](https://arxiv.org/abs/2407.12844)
- Liu et al. (2023)
  X. Liu, H. Yu, H. Zhang, Y. Xu, X. Lei, H. Lai, Y. Gu, H. Ding, K. Men, K. Yang, S. Zhang, X. Deng, A. Zeng, Z. Du, C. Zhang, S. Shen, T. Zhang, Y. Su, H. Sun, M. Huang, Y. Dong, and J. Tang
  AgentBench: evaluating llms as agents.
  arXiv preprint arXiv:2308.03688.
  External Links: [Link](https://arxiv.org/abs/2308.03688)
- Martínez-Plumed et al. (2019)
  F. Martínez-Plumed, R. B.C. Prudêncio, A. Martínez-Usó, and J. Hernández-Orallo
  Item response theory in ai: analysing machine learning classifiers at the instance level.
  Artificial Intelligence 271, pp. 18–42.
  External Links: ISSN 0004-3702,
  [Document](https://dx.doi.org/https%3A//doi.org/10.1016/j.artint.2018.09.004),
  [Link](https://www.sciencedirect.com/science/article/pii/S0004370219300220)
- Maslej et al. (2024)
  N. Maslej, L. Fattorini, R. Perrault, V. Parli, A. Reuel, E. Brynjolfsson, J. Etchemendy, K. Ligett, T. Lyons, J. Manyika, J. C. Niebles, Y. Shoham, R. Wald, and J. Clark
  Artificial intelligence index report 2024.
  External Links: 2405.19522,
  [Link](https://arxiv.org/abs/2405.19522)
- METR (2025)
  METR
  Measuring automated kernel engineering.
  Note: <https://metr.org/blog/2025-02-14-measuring-automated-kernel-engineering/>
- Mialon et al. (2024)
  G. Mialon, C. Fourrier, T. Wolf, Y. LeCun, and T. Scialom
  GAIA: a benchmark for general AI assistants.
  In The Twelfth International Conference on Learning Representations,
  External Links: [Link](https://openreview.net/forum?id=fibxvahvs3)
- Miserendino et al. (2025)
  S. Miserendino, M. Wang, T. Patwardhan, and J. Heidecke
  SWE-lancer: can frontier llms earn $1 million from real-world freelance software engineering?.
  External Links: 2502.12115,
  [Link](https://arxiv.org/abs/2502.12115)
- Murray et al. (2025)
  M. Murray, H. Papadatos, O. Quarks, P. Gimenez, and S. Campos
  Mapping ai benchmark data to quantitative risk estimates through expert elicitation.
  arXiv preprint arXiv:2503.04299.
- Ngo (2023)
  R. Ngo
  Clarifying and predicting AGI.
   LessWrong.
  Note: <https://www.lesswrong.com/posts/BoA3agdkAzL6HQtQP/clarifying-and-predicting-agi>Accessed: 2024-03-21
- OpenAI (2025)
  OpenAI
  OpenAI o3-mini.
  Note: <https://openai.com/index/openai-o3-mini>[Accessed 18-03-2025]
- Owen (2024)
  D. Owen
  How predictable is language model benchmark performance?.
  External Links: 2401.04757
- Paperno et al. (2016)
  D. Paperno, G. Kruszewski, A. Lazaridou, N. Pham, R. Bernardi, S. Pezzelle, M. Baroni, G. Boleda, and R. Fernández
  The LAMBADA dataset: word prediction requiring a broad discourse context.
  In Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),
  pp. 1525–1534.
- Phan et al. (2025)
  L. Phan, A. Gatti, Z. Han, N. Li, J. Hu, H. Zhang, S. Shi, M. Choi, A. Agrawal, A. Chopra, et al.
  Humanity’s last exam.
  arXiv preprint arXiv:2501.14249.
- Phuong et al. (2024)
  M. Phuong, M. Aitchison, E. Catt, S. Cogan, A. Kaskasoli, V. Krakovna, D. Lindner, M. Rahtz, Y. Assael, S. Hodkinson, et al.
  Evaluating frontier models for dangerous capabilities.
  arXiv preprint arXiv:2403.13793.
- Pimpale et al. (2025)
  G. Pimpale, A. Højmark, J. Scheurer, and M. Hobbhahn
  Forecasting frontier language model agent capabilities.
  External Links: 2502.15850,
  [Link](https://arxiv.org/abs/2502.15850)
- Qin et al. (2023)
  Y. Qin, S. Liang, Y. Ye, K. Zhu, L. Yan, Y. Lu, Y. Lin, X. Cong, X. Tang, B. Qian, S. Zhao, L. Hong, R. Tian, R. Xie, J. Zhou, M. Gerstein, D. Li, Z. Liu, and M. Sun
  ToolLLM: facilitating large language models to master 16000+ real-world apis.
  External Links: 2307.16789,
  [Link](https://arxiv.org/abs/2307.16789)
- Radford et al. (2019)
  A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, I. Sutskever, et al.
  Language models are unsupervised multitask learners.
  OpenAI blog 1 (8), pp. 9.
- Rein et al. (2025)
  D. Rein, J. Becker, A. Deng, S. Nix, C. Canal, D. O’Connell, P. Arnott, R. Bloom, T. Broadley, K. Garcia, B. Goodrich, M. Hasin, S. Jawhar, M. Kinniment, T. Kwa, A. Lajko, N. Rush, L. J. K. Sato, S. Von Arx, B. West, L. Chan, and E. Barnes
  HCAST: Human-Calibrated Autonomy Software Tasks.
  Note: Forthcoming
- Roberts et al. (2025)
  J. Roberts, M. R. Taesiri, A. Sharma, A. Gupta, S. Roberts, I. Croitoru, S. Bogolin, J. Tang, F. Langer, V. Raina, V. Raina, H. Xiong, V. Udandarao, J. Lu, S. Chen, S. Purkis, T. Yan, W. Lin, G. Shin, Q. Yang, A. T. Nguyen, D. I. Atkinson, A. Baranwal, A. Coca, M. Dang, S. Dziadzio, J. D. Kunz, K. Liang, A. Lo, B. Pulfer, S. Walton, C. Yang, K. Han, and S. Albanie
  ZeroBench: an impossible visual benchmark for contemporary large multimodal models.
  External Links: 2502.09696,
  [Link](https://arxiv.org/abs/2502.09696)
- Roodman (2020)
  D. M. Roodman
  On the probability distribution of long-term changes in the growth rate of the global economy: an outside view.
  External Links: [Link](https://api.semanticscholar.org/CorpusID:221641799)
- Sevilla et al. (2022)
  J. Sevilla, L. Heim, A. Ho, T. Besiroglu, M. Hobbhahn, and P. Villalobos
  Compute trends across three eras of machine learning.
  In 2022 International Joint Conference on Neural Networks (IJCNN),
  pp. 1–8.
- Song and Flach (2021)
  H. Song and P. Flach
  Efficient and robust model benchmarks with item response theory and adaptive testing.
  International Journal of Interactive Multimedia and Artificial Intelligence.
- Srivastava et al. (2022)
  [. Srivastava et al.
  Beyond the imitation game: quantifying and extrapolating the capabilities of language models.
  arXiv preprint arXiv:2206.04615.
- Wang et al. (2019)
  A. Wang, Y. Pruksachatkun, N. Nangia, A. Singh, J. Michael, and S. R. Bowman
  SuperGLUE: a stickier benchmark for general-purpose language understanding systems.
  In Advances in Neural Information Processing Systems (NeurIPS) Workshop,
  External Links: [Link](https://super.gluebenchmark.com/)
- Wang et al. (2018)
  A. Wang, A. Singh, J. Michael, F. Hill, O. Levy, and S. R. Bowman
  GLUE: a multi-task benchmark and analysis platform for natural language understanding.
  In International Conference on Learning Representations (ICLR),
  External Links: [Link](https://gluebenchmark.com/)
- Wijk et al. (2024)
  H. Wijk, T. Lin, J. Becker, S. Jawhar, N. Parikh, T. Broadley, L. Chan, M. Chen, J. Clymer, J. Dhyani, et al.
  RE-Bench: evaluating frontier AI R&D capabilities of language model agents against human experts.
  arXiv preprint arXiv:2411.15114.
- Xu et al. (2024)
  F. F. Xu, Y. Song, B. Li, Y. Tang, K. Jain, M. Bao, Z. Z. Wang, X. Zhou, Z. Guo, M. Cao, et al.
  TheAgentCompany: benchmarking llm agents on consequential real world tasks.
  arXiv preprint arXiv:2412.14161.
- Yan et al. (2024)
  F. Yan, H. Mao, C. C. Ji, T. Zhang, S. G. Patil, I. Stoica, and J. E. Gonzalez
  Berkeley function calling leaderboard.
  Note: <https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html>
- Yao et al. (2023)
  S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao
  ReAct: synergizing reasoning and acting in language models.
  External Links: 2210.03629,
  [Link](https://arxiv.org/abs/2210.03629)
- Zellers et al. (2019)
  R. Zellers, A. Holtzman, Y. Bisk, A. Farhadi, and Y. Choi
  HellaSwag: can a machine really finish your sentence?.
  In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics,
  pp. 4791–4800.
- Zhang et al. (2024)
  A. K. Zhang, N. Perry, R. Dulepet, J. Ji, C. Menders, J. W. Lin, E. Jones, G. Hussein, S. Liu, D. Jasper, et al.
  Cybench: a framework for evaluating cybersecurity capabilities and risks of language models.
  arXiv preprint arXiv:2408.08926.
- Zielinski (2019)
  D. Zielinski
  How to optimize onboarding.
   Society for Human Resource Management.
  Note: Accessed on March 17, 2025
  External Links: [Link](https://www.shrm.org/topics-tools/news/hr-magazine/how-to-optimize-onboarding)


## 附录 A 扩展的相关工作

下面，我们扩展第 1.1 节中相关工作的讨论。

### A.1 智能体与能力基准

AI 能力的评估已从单任务基准显著演进为旨在评估类智能体行为的复杂多步评估。虽然 GLUE（Wang et al., 2018）、SuperGLUE（Wang et al., 2019）与 MMLU（Hendrycks et al., 2020）等传统基准为语言模型表现提供了宝贵洞见，它们主要测量静态知识，而非真实世界应用所必需的动态问题求解能力。

近期工作开发了更复杂的智能体基准。AgentBench（Liu et al., 2023）在网页浏览、编码与游戏等多种环境中评估智能体。MLAgentBench（Huang et al., 2024）与 MLEBench（Chan et al., 2024）专门聚焦机器学习研究任务，而 ToolBench（Qin et al., 2023；Guo et al., 2024）评估工具使用能力。近期的 ZeroBench（Roberts et al., 2025）涉及困难推理，但在视觉谜题而非有经济价值任务的语境下。其他值得注意的基准包括 GAIA（Mialon et al., 2024），评估跨多种模态的推理，以及 BIG-bench（Srivastava and others, 2022），包含数百个多样任务，其中许多需要多步推理。

软件工程已成为评估 AI 能力特别有信息量的领域。HumanEval（Chen et al., 2021）与 MBPP（Austin et al., 2021）提供复杂度各异的编程挑战，而 SWE-bench（Jimenez et al., 2024）与 APPS（Hendrycks et al., 2021）等更复杂的基准测试更精深的编程能力。我们在本工作中使用 SWE-bench Verified（Chowdhury et al., 2024）的人工任务完成时间估计。RE-Bench（Wijk et al., 2024）——我们本工作所使用——在可能需要数小时人类努力的复杂研究工程任务上评估模型，并把 AI 表现与人类机器学习工程师比较。SWE-Lancer（Miserendino et al., 2025）生成任务

虽然这些基准对特定能力提供了宝贵洞见，它们往往缺少一个能随时间追踪进展并比较能力差异巨大的模型的统一指标。我们的时间视界方法旨在弥补这一空缺，提供一个可用于跨不同能力水平测量进展的连续指标。

### A.2 预测 AI 进展

AI 进展的定量预测采用了多种方法，往往始于对 AI 训练所用算力随时间大幅增加的观察。Amodei and Hernandez（2018）观察到 AI 训练算力用量呈指数增长，2012 到 2018 年间大约每 3.4 个月翻一番；Epoch AI（2024）纳入了更近的数据以及训练数据集规模与能耗的趋势。

其他工作研究了 AI 表现如何随时间提升，把基准表现与发布日期、算力用量及其他投入联系起来。Sevilla et al.（2022）发现算力用量增长率在 2010 年「深度学习时代」开始时上升，与表现的提升相吻合。更近期，Owen（2024）与 Pimpale et al.（2025）用算力等指标预测未来的基准表现。

近来有若干努力为 AI 基准表现提供语境。其中之一是年度 AI Index Report（Maslej et al., 2024），它追踪各种基准上的表现，包括模型达到人类水平表现的日期。Murray et al.（2025）让网络安全专家把 AI 在 Cybench（Zhang et al., 2024）上的表现与自主开发恶意软件的能力联系起来。Phuong et al.（2024）委托专业预测者以基准表现为条件，预测到 2030 年 AI 是否跻身最受关注的公共议题。这些努力通常缺少一个跨基准比较的统一量化指标。

Carlsmith（2020）与 Cotra（2020）发展了「生物锚点」框架，把训练 AI 模型涉及的算力与 AI 产生变革性影响所需任务的「有效视界长度」联系起来。Ngo（2023）提议用 AI 系统在多数任务上超越多数人类专家的时间视界来度量通用 AI 能力。在本工作中，我们实证评估任务时长与 AI 智能体成功率之间的关系，并将其转换为 AI 智能体表现的量化指标。

### A.3 心理测量方法与项目反应理论

我们的方法学路径借鉴心理测量测试，尤其是项目反应理论（IRT）（Baker, 2001），它建模潜在特质（如能力）与测试题目观察响应之间的关系。在传统 IRT 中，题目难度是逻辑斯蒂模型中基于被试能力预测回答正确性的参数。我们的做法与此相反，用任务完成时间（难度的代理）预测 AI 表现。我们的方法学也与教育测试中的难度估计技术相关（de Ayala, 2017），那里用包括完成时间在内的多种指标估计任务难度。IRT 已被 Martínez-Plumed et al.（2019）应用于机器学习分类器，并被 Song and Flach（2021）用于设计高效基准。

## 附录 B 任务套件细节

与大多数基准一样，我们研究的三个任务套件旨在隔离一个可以在时限内可靠完成的具体工作单元。这通常意味着任务所需的上下文远少于较大项目中途的平均任务[注10](#fn10)。我们确认所有任务在所提供的说明下都是可行的——人类至少成功完成过每个任务一次[注11](#fn11)。

注 10：我们把上下文定义为有经验的员工用来完成任务、但不在任务描述中明确给出、也不为多数外部专家所拥有的信息。例如，修复软件包的 bug 时，包的维护者可能利用对同包过往 bug 的经验来猜测成因、凭借对代码库的熟练来定位 bug、并依据对其组织优先级的了解决定打补丁还是彻底修复。我们在第 4 节讨论上下文的可能影响。

注 11：由于这些尝试多由内部员工完成或使用了不同方法，我们把它们排除在人类基线数字之外。

### B.1 任务子套件

HCAST 与 SWAA 套件被划分为任务族，即彼此相似的任务组。例如「crossword」任务族包含创建 3x3 填字游戏、5x5 填字游戏等任务。我们把任务划分成族，因为族内表现相关，且我们对任务多的族降权以保持多样性。

#### B.1.1 HCAST 套件

我们使用 HCAST 中来自 46 个任务族的 97 个任务，这是一组覆盖网络安全、机器学习、软件工程与一般推理的多样挑战。

该套件的任务从人类只需几分钟的简单任务（例如在维基百科上查找一个基础事实问题）到专家人类需数小时的任务（例如编写 CUDA 内核、或修复 PyTorch 中的微妙 bug）。由于现代前沿 AI 系统相对更擅长基于文本的任务，这些任务多数不需要视觉/多模态能力，且所有任务都可通过 bash shell 的文本编辑解决。

与许多近期基准相比，HCAST 中的任务并非为让人类领域专业人士或当前 AI 系统尽可能难以完成而设计。相反，多数任务以真实为目标，使在任务上表现出色需要我们预期有经济价值的技能。因此，我们预期这些任务大多可由在相关领域有几年专业经验的人类解决。

任务由其说明、初始资源与一个算法评分函数定义。任务说明是字符串，通常在 1-2 句到几段之间，不过它们可以引用作为初始资源包含的其他信息来源，或通过互联网外部获得。初始资源通常由代码、数据与文档组成。

每个任务自动在 0 到 1 之间评分，分数越高表现越好。许多任务只返回 0 或 1 分，但对连续计分的任务，我们手工定义一个成功阈值分数，用于部分分析中将智能体分数二值化[注12](#fn12)。（我们不公开多数任务的内容，以降低 AI 系统意外或故意在其上训练的可能性。）

注 12：这些任务的一小部分可按需提供。

HCAST 任务的更多细节见 Rein et al.（2025）。

#### B.1.2 RE-Bench 套件

RE-Bench 由 7 个具有挑战性的开放式机器学习研究工程环境组成，每个环境预期人类专家约需 8 小时完成。详见 Wijk et al.（2024）。

#### B.1.3 软件原子动作（SWAA）套件

HCAST 设计为一组多样的任务，但最短的任务约 1 分钟长，这限制了在更短任务上测量 AI 智能体表现的代表性与可达到的分辨率。为填补这一空缺，我们观察到现实世界的智力劳动部分由短于 1 分钟的可测量单步动作组成。我们创建了 SWAA 任务套件，包含 66 个小任务，对应软件工程工作中常见的 <1 分钟原子动作。SWAA 子集包括选择题与填空题。

```text
Which file is most likely to have a password in it?

1. credentials.txt

2. installation_notes.txt

3. main.py

4. launcher_win.exe
```

与 LAMBADA（Paperno et al., 2016）或 GSM8K（Cobbe et al., 2021）等测试与软件工程无直接适用技能的简单基准不同，SWAA 集代表软件工程工作与我们研究的较长任务中都需要的动作。SWAA 由 5 个任务族组成：三个代表常见决策，一个用于代码补全，一个用于数学；详见附录 B.1.3。

SWAA 任务的开发对 AI 智能体表现盲视；即所有任务在看到 AI 尝试之前写就，性能引出（开发用于评估的少样本提示）在一个单独的开发任务套件上进行。

![Refer to caption](2503.14499v4/plots/task_distribution.png)

图 7：按难度评级堆叠的任务直方图。HCAST 主要包括长于 4 分钟的任务，而我们用 SWAA 聚焦 2 秒到 15 秒范围的任务以测量 GPT-2 与 GPT-3。两者之间存在空档，限制了我们测量该范围时间视界的能力。

SWAA 由五个任务族组成：三个代表常见决策，一个用于代码补全，一个用于数学。

##### 决策（选择题）

- 文件选择：哪个文件具有某属性，或在某情境下适合读取？

- 告警分诊：公司里哪个团队应该调查一个告警？

- 请求路由：针对某个请求需要采取什么行动？

##### 填空

- 代码补全：补全代码中的单个词。

- 数学：求解简单算术题，独立题或软件工程主题的应用题。

开发 SWAA 任务时，我们试图通过让任务作者对模型表现盲视来避免结果偏置，因此初步的 71 个任务在开发期间未运行任何模型。之后排除多于一名基线者失败的任务，筛减为最终的 66 个。

##### RE-Bench

![Refer to caption](2503.14499v4/images/rebench.png)

图 8：最初的 7 个 RE-Bench 任务。

RE-Bench 任务的描述见图 8[注13](#fn13)。

注 13：Restricted MLM 任务在禁止某些 PyTorch 方法的同时涉及机器学习工程；当前模型有时以间接方式使用这些被禁方法，使作弊无法被自动检测，但模型作弊不会显著影响我们的结果。

### B.2 任务套件的局限

我们用来衡量 AI 能力的任务与真实任务有系统性差异。这些差异可能导致我们在这些任务上观察到的趋势无法推广到真实世界任务。例如，全部 SWAA、HCAST 与 RE-Bench 在以下方面都不同于真实世界任务：

- 自动评分 我们使用的所有任务都可自动评分，意味着任务环境中运行的一段代码决定最终分数。这对解决方案的格式等施加了约束，往往降低任务的开放性，也降低了对合理价值判断的需要。

- 不与其他智能体交互 没有任务涉及与其他自主智能体交互。与其他智能体协调或竞争似乎很可能增加任务难度，例如通过提高战略决策、实时协调与预测其他复杂智能体行动的重要性。

- 宽松的资源约束 没有 SWAA 任务、也很少有 HCAST 任务显著涉及高效利用有限资源——这是真实世界任务的常见约束。

- 无惩罚性 类似地，很少有任务对单次失误施以惩罚[注14](#fn14)。这部分是为了降低收集人类基线的预期成本。真实世界任务往往更具惩罚性，例如当它们涉及与其他智能体竞争时。例如，国际象棋中一次失误可能大幅降低赢棋概率。

注 14：HCAST 任务中过早提交答案是例外。

- 静态环境 此套件中的任务通常使用除非被智能体直接作用否则不会显著变化的环境。相比之下，真实任务往往发生在变化的环境中。

我们在第 F.2 节中试图通过把上述性质作为「杂乱度」因子来测量这些系统性差异可能对 AI 智能体表现的影响。我们发现，虽然「更杂乱」任务上的绝对表现更低，表现趋势与不那么杂乱的任务相似。

## 附录 C 方法学细节

### C.1 人类基线

#### C.1.1 HCAST 任务

我们使用作为 HCAST 一部分收集的现有基线。这些基线收集自具有软件工程、机器学习与网络安全相关经验的领域专业人士。基线者在与智能体相同的环境中工作，使用 Vivaria（一个开源的语言模型智能体评估平台），其屏幕与音频被录制以供人工审查防止作弊。他们因成功完成以及比其他基线者更快完成任务而获得奖金激励。在筛除我们 HCAST 子集之外任务的尝试、失败尝试以及有问题的尝试（如使用被禁止的 AI 工具）后，我们从约 460 次总尝试中纳入 286 次成功基线。任务时长用成功基线的几何平均计算，缺少成功基线的任务用人工估计[注15](#fn15)。

注 15：非基线估计基于的信息包括未遵循严格基线条件的 QA 运行时长，以及有成功基线的类似任务时长。

关于 HCAST 基线的更多信息见 Rein et al.（2025）。

#### C.1.2 RE-Bench 基线

对 RE-Bench，我们使用了 Wijk et al.（2024）的基线。由于基线者被指示在每个任务上取得最佳表现，我们把这 6 个任务的任务时长视为 8 小时，并改用花费 7 到 9 小时的基线者的平均分把原始分转换为成功阈值。

RE-Bench 基线与 HCAST 使用相同的基线者池与激励，但有一些差异。基线者没有被要求达到阈值分数，而是给定 8 小时的固定时限并被指示最大化分数；阈值依据基线者平均表现设定。RE-Bench 基线者可以使用 AI 工具，因此这些任务上的人类分数可能偏高。

#### C.1.3 SWAA 基线

与由外部承包商做基线的 HCAST 与 RE-Bench 不同，SWAA 由具备相关专长的内部员工用一个能更精确计时的定制 web 应用做基线。因为这些任务意在为单步并排除上下文获取，SWAA 任务的计时器在用户选择回答后立即结束。决策类任务只允许一次选择以避免随机猜测；填空任务中，基线者可以多次尝试直到答对或选择跳过。我们对每个决策类任务做 4 次基线，每个填空类任务 3 次。

与 HCAST 和 RE-Bench 集不同，SWAA 由具备相关专长的内部员工用一个能更精确计时的定制 web 应用做基线。因为这些任务意在为单步并排除上下文获取，SWAA 任务的计时器在阅读一般说明后启动、在用户选择回答后立即结束，因此基线时间只包括阅读问题本身与选择答案。我们常规设置下的基线有数秒到数十秒的计时开销，对时长短于 2 秒的单步任务而言高得不可接受。

#### C.1.4 基线成功率

我们把人类基线时间聚合为任务时长评级，方法是取成功基线运行的几何平均时间，它比平均时间更能预测模型表现，因为基线时间大致呈对数正态分布。

我们选择只筛选成功的运行，有两个主要原因——一个实际、一个原则性的。首先，为每个任务收集足够多的基线以估计时间-成功率曲线在实践中很困难。其次，我们想排除基线因不适用于模型的原因而失败的情形。相当一部分人类失败似乎属于此类——包括人类对任务专业知识不足，或因不明原因放弃任务（可能被打断或感到无聊）。特别是，由于我们以获得成功基线为目标，我们的报酬方案激励承包商快速猜一个答案或尽早放弃，以便转到预期收益更高的其他任务。

然而，以成功为条件会使任务时长评级偏短，从而低估模型表现。如果许多人类失败源于对模型也相关的问题——例如部分任务需要猜测——这一偏置尤其显著。该偏置在较长任务上最明显，其基线者成功率往往低于 50%；因此我们对这些较长任务的难度评级信心较低，并预期它们可能被低估。若真如此，我们可能低估了模型改进的速度。

##### 人类时间视界

另一种做法是用与模型相同的方法学计算人类的时间视界。对时间视界的一种自然解读意味着「给定 x 小时的人类」的时间视界是 x 小时。由于我们的基线者按每任务最多 8 小时计酬，我们预期其时间视界约为 8 小时。然而实践中它低得多，约 1.5 小时（这将意味着最好的模型在不到 7 个月内超越人类）。如上所述，我们认为这一数字被人为压低，因为许多人类失败似乎是我们激励方案的产物。

图 9 展示按任务长度划分的基线者成功率。

![Refer to caption](2503.14499v4/plots/individual_histograms/human_baselines/histograms.png)

图 9：人类基线者的成功率与时间视界。注意该时间视界与机器学习模型的时间视界不可直接比较（见第 C.1.4 节）。

#### C.1.5 基线时间分析

我们人工观看并标注了 50 次基线的录像，以了解基线者如何分配时间。基于这一小样本调查：

1. 在短（5-15 分钟）任务上，相当一部分时间（25-75%）花在阅读说明或理解如何正确提交上。尤其对短任务，我们的时间估计可能难以解读，因为阅读说明存在一些固定开销，与任务本身难度无关。

2. 我们的任务设计为需要相对少的上下文，但基线者仍花超过 25% 的时间回忆相关信息（例如如何做端口转发）。

### C.2 内部 PR 任务

##### 摘要

我们在一个内部仓库的五个未受污染 issue 上运行了 GPT-4o、Claude 3.5 Sonnet（New）与 o1。解决这些 issue 是内部员工执行的真实工作，因此我们预期这些任务上的结果比典型基准任务更能代表在有经济价值的真实任务上的表现。

我们发现，承包基线者解决 issue 的时间是仓库维护者的 5-18 倍。此外，若用承包商完成时间度量任务长度，AI 智能体在这些 issue 上的表现与从 HCAST、SWAA 与 RE-Bench 表现导出的 AI 智能体成功率曲线不矛盾。不过，我们的承包基线者完成这些任务的时间比仓库维护者长得多。这表明时间视界可能与低上下文人类的劳动对应得更好，而非高上下文人类。

##### 方法

我们从内部仓库收集了五个真实的、近期的、未受污染的 issue。然后我们在这些 issue 上运行 GPT-4o、Claude 3.5 Sonnet（New）与 o1。我们记录了仓库维护者解决这些 issue 的时间，并让外部基线者尝试修复。与 SWE-bench Verified 不同，我们没有做要求这些 issue 可自动验证的筛选。相关仓库的维护者像审查 PR 那样人工给模型与基线者的方案打分：

1. 0 分：PR 不正确，需要根本性重做。

2. 0.25 分：合并前必须做少量修改。

3. 0.75 分：有小问题但 PR 仍可合并。

4. 1.0 分：PR 可以直接合并。

##### 示例 issue

我们给出两个示例 issue——一个简单（Issue 1），另一个（Issue 8）更具挑战性。Issue 8 展示了代码库上下文如何在基线者与仓库维护者之间带来人类完成时间的巨大加速。这些基线的结果见表 3。

```text
The stage plot_logistic_individual with the error message:

“‘
FileNotFoundError: [Errno 2] No such file or directory:
’plots/logistic_individual/invsqrt_task_weight-0.01.png’
ERROR: failed to reproduce ’plot_logistic_individual@invsqrt_task_weight-0.01’:
failed to run: python -m src.plot.logistic_individual –input-file data/wrangled/logistic_regression_invsqrt_task_weight_0.01_ftr.csv
–output-file plots/logistic_individual/invsqrt_task_weight-0.01.png
–plot-format png –log-level INFO, exited with 1
“‘
```

```text
Reweighting in bootstrapping
Currently the hierarchical bootstrapping does not reweight runs.
```

| Issue | 执行者 | 所花时间 | 分数 |
| --- | --- | --- | --- |
| 1 | 仓库维护者 | 5 分钟 | 1.0 |
|  | 基线者 | 81 分钟 | 1.0 |
| 8 | 仓库维护者 | 20 分钟 | 1.0 |
|  | 基线者 | 113 分钟 | 0.25 |

表 3：所选内部 PR 上基线的结果

##### 

| 任务 ID | GPT-4o | Claude 3.5 Sonnet | o1 |
| --- | --- | --- | --- |
| Issue 1 | 0.35 (5) | 0.45 (5) | 0.875 (6) |
| Issue 8 | 0.0 (5) | 0.0 (5) | 0.0 (5) |
| Issue 9-1 | 0.0 (5) | 0.0 (5) | 0.0 (5) |
| Issue 9-2 | 0.0 (5) | 1.0 (5) | 0.85 (5) |
| Issue 10 | 0.0 (5) | 0.0 (5) | 0.0 (5) |
| Issue 11 | 0.02 (12) | 0.0 (11) | 0.0 (8) |

表 4：内部 PR 每任务平均分（括号内为试验次数）。注意我们对 Issue 9 做了最少的处理把它拆成两个 issue，因为实际上该 issue 描述包含两件完全独立的工作。

##### 仓库维护者时间 vs. 基线者时间

基线者完成 issue 所需时间与仓库维护者所需时间差异巨大（表 5）。实践中，仓库维护者完成给定 issue 快 5-18 倍。

|  |  |  |  |
| --- | --- | --- | --- |
| 任务 ID | 维护者时间（分钟） | 基线者时间（分钟） | 减速 |
| eval-analysis-public-1 | 5 | 81（分数 1） | 16x |
| eval-analysis-public-8 | 20 | 113（分数 .25） | ~5.5x |
| eval-analysis-public-9-1 | 235 | - | - |
| eval-analysis-public-9-2 | 5 | 69（分数 1）* | 14x |
| eval-analysis-public-10 | 20 | - | - |
| eval-analysis-public-11 | 5 | 93（分数 .75） | 18.6x |
| *注：这是在一个轻微变体上运行的 | | | |
| --- | --- | --- | --- |

表 5：仓库维护者与基线者修复 issue 时间的比较

##### 人工评分方法与结果

维护者、基线者与模型的方案像拉取请求一样被人工评分。我们试验了承包商给 PR 评分，以及不同仓库的维护者给 PR 评分。实践中，仓库维护者的评分比承包商一致得多。承包商之间的相关在 50-60%。仓库维护者之间的相关在 88-91%。

##### 评分时间

若要在真实工作上有成本竞争力，模型完成一个 PR 的总成本必须低于仓库维护者自己实现该 PR 的成本（加上辅助成本，例如代码评审者的时间）。因此我们记录了给模型方案评分所花的时间，以更好理解用模型修复真实 issue 的净成本。仓库维护者评分比承包商快得多，但比值不如完成时间那么悬殊——承包商平均每次运行 8 分钟，仓库维护者平均每次 3.5 分钟。不同 issue 的平均评分时间不同，较容易的 issue 通常评分更快，所有 issue 的评分都快于完成。未来我们计划创建一个考虑评分工作量、模型成本与模型成功率的近似成本指标。我们预期这将是理解模型/维护者工作之比未来如何随智能体使用成本持续下降而转移的有用框架。

##### 承包基线者 vs 仓库维护者

模型成功率与承包基线者时间预测的相当一致。实践中，基线者在简单任务上也比有经验的维护者差得多。例如 Issue 11，基线者花了一个半小时以上完成，因此我们不会预期模型能稳定完成该任务。

##### 定性印象

与 HCAST + SWAA + RE-bench 任务的每时间桶成功率朴素比较，仓库维护者完成时间并不能很好预测模型在这些任务上的表现。例如，Issue 11 对维护者是最简单的任务。它需要在 10 个 Python 文件中写简单注释，维护者不到五分钟即完成。但模型在 30 次运行中一次也未成功完成。也有模型确实成功的任务，正如我们从其他任务的每时间桶成功率所预期。例如，模型能稳定地为数据管道的单一阶段补上缺失的建目录步骤。虽然基线者与模型相较仓库维护者都吃力，但吃力的方式不同。基线者往往缺乏对代码库所用工具与技术的了解：例如「DVC 是什么？」「自助法是什么来着？」。而当前 AI 模型对工具与技术展现出稳定的知识，但在真实代码库工作所需的更大上下文上似乎吃力。

### C.3 模型如何运行

| 模型 | 智能体 |
| --- | --- |
| Claude 3.5 Sonnet (Old) | modular-public |
| Claude 3.5 Sonnet (New) | modular-public |
| Claude 3 Opus | modular-public |
| davinci-002 | modular-public |
| gpt-3.5-turbo-instruct | modular-public |
| GPT-4 0314 | modular-public |
| GPT-4 0125 | modular-public |
| GPT-4 1106 | modular-public |
| GPT-4 Turbo | modular-public |
| GPT-4o | modular-public |
| o1 | triframe |
| o1-preview | duet |

表 6：本报告中每个模型所用的脚手架

所有模型都通过使用 Anthropic 或 OpenAI API 的智能体脚手架运行。

我们在整个评估套件上使用相同的智能体脚手架，没有任务特定的提示或脚手架，SWAA 任务除外——它使用简单的提示脚手架。所有智能体都被提供与人类基线者相同的条件。

GPT-2 因上下文长度太低而与我们的脚手架不兼容，因此我们把 GPT-2 在 RE-Bench 与 HCAST 的所有任务上的分数插补为零。我们认为这合理，因为强得多的 davinci-002（GPT-3）在该集合上得零分。去掉这些插补的 GPT-2 零分对本文后续所有结果的影响可忽略。

#### C.3.1 脚手架与平台细节

大多数 AI 模型用 modular-public——一个基础智能体脚手架——评估。该脚手架为模型提供 Python 与 Bash 命令以及一些非常简单的上下文管理，以使输入保持在 LM 的上下文窗口长度内。我们对 o1-preview 与 o1 使用了略有不同的脚手架，因为它们似乎在工具使用、响应环境反馈以及总体上作为智能体行动方面吃力。

对人类基线与 AI 智能体运行，我们的实验都使用开源平台 Vivaria。CPU 与 GPU 资源依据任务的资源规格在安全 VM 内提供。表 6 展示每个模型使用的脚手架。modular-public 与 triframe/duet 都融入了 ReAct 框架（Yao et al., 2023）的原则，该框架把推理轨迹与行动交织。这些智能体在一个不包含在 HCAST 中的留存开发集上开发，以降低对这些任务过拟合的可能性。这些脚手架的实现细节见各自的代码库。

两种脚手架都允许智能体在调用一组工具之前通过思维链推理进行规划。智能体主要通过运行 Python 代码与 Bash 命令与其任务环境交互。

在 Modular 中，模型生成单条待执行命令，然后脚手架执行该函数调用，返回来自环境的相关信息（例如 STDOUT/STDERR）。该过程重复，直到模型判定答案可以提交，或系统达到预定义的使用上限。

在 Triframe 中，为决定执行哪条命令，模型先生成一个建议计划，然后基于该计划生成三条可能执行的命令，以及三条忽略计划的建议命令（以多样化其生成的想法）。然后，模型为六个提议行动各生成两个 -2 到 2 之间的分数，脚手架执行按两个分数平均得分最高的函数调用。

#### C.3.2 算力使用

使用的总算力包括 RE-Bench 环境约 2,000 H100 小时、其他环境 50,000 CPU 小时（云与内部机器的组合），加上内部或 API 供应商提供的约 50,000 H100 小时等价推理算力。这包括初步实验所用的算力。数据分析所用算力极少。

### C.4 与项目反应理论的比较

项目反应理论（IRT）是一组统计技术，用于基于能力水平预测一个人正确回答问题的概率。标准 IRT 双参数逻辑斯蒂（2PL）模型为（简化自 Cai et al.）：

$$T_{i}(1|\eta_{agent})=\sigma((\eta_{agent}-\alpha_{task})\cdot\beta_{task})$$

其中 $T_{i}(1|\eta_{agent})$ 表示能力水平为 $\eta_{agent}$ 的人正确完成任务的概率[注16](#fn16)。IRT 通常同时回归题目难度与能力水平；相比之下，我们把题目难度定义为人类基线时间的对数，因此只回归能力水平。具体而言，我们的模型如下。

$$T_{i}(1|h_{agent})=\sigma((\log h_{agent}-\log t_{task})\cdot\beta_{agent}) \tag{1}$$

注 16：在三参数逻辑斯蒂模型中，加入一个表示正确猜中任务概率的参数 $\gamma_{task}$。在 2PL 模型与我们的方法中，$\gamma_{task}=0$。这对多数任务事实上成立，但一些 SWAA 任务是选择题，猜对概率为 25%。这一选择只影响 GPT-2 与 GPT-3 的时间视界，不会显著影响我们的结果。

注意相对 2PL 模型的以下变化：

1. $\alpha_{task}=\log t_{task}$，其中 $t_{task}$ 是成功人类基线时间的几何平均。

2. $\eta_{agent}$ 现在可解读为 $\log h_{agent}$，其中 $h_{agent}$ 是智能体的 50% 时间视界而非抽象能力参数。这是因为当 $h_{agent}=t_{task}$ 时，我们的模型预测成功概率为 $\sigma(0\cdot\beta_{agent})=\sigma(0)=0.5$。

3. $\beta_{agent}$ 是依赖智能体的学习参数，而非依赖任务。

为拟合公式 (1)，我们按多样性给任务加权，使来自大小为 $n$ 的族的任务权重为 $1/\sqrt{n}$。然后我们用逻辑斯蒂回归为每个模型拟合时间视界 $h_{agent}$ 与斜率 $\beta_{agent}$。例如，按此方法学 o1 的时间视界约为 39 分钟（见图 4）。

这些改动使我们能计算一个可解读的时间视界，而避开 IRT 的若干复杂性。第一，IRT 有一个从所有智能体分数估计任务难度的初始校准/联合优化阶段，因此一个智能体的能力分数可能依赖于其他智能体的表现；在我们的方法中每个智能体的时间视界单独计算。第二，IRT 输出「能力分数」，随后需要转换为时间视界估计；我们的方法通过直接估计视界消除了这一步。第三，2PL 模型对每个任务使用一个斜率参数，而我们每个智能体使用一个斜率参数。在我们这种智能体远少于任务的设置下，这减少了总参数量。

作为交换，我们放弃了使用为测试设计而设的 IRT 指标的能力，例如单个任务的 Fisher 信息函数（Kipnis et al., 2025 等所用）。未来改进的方法学可以纳入这些指标，以设计植根于人类数据的样本高效基准与评估。

## 附录 D 定性分析

### D.1 失败类别

为更好理解当前与较早 AI 智能体失败的差异，我们从 GPT-4 1106 智能体分别抽取 31 次失败运行，从 o1 智能体抽取 32 次失败运行，并人工按以下互斥的失败类别标注：

- 规划与工具选择不佳：智能体生成本身就不可行的高层计划，或为计划选择的工具无法达成预期目的。

- 心算或推理错误：智能体在关键步骤执行了错误的心算或逻辑推理，导致运行失败。

- 过早放弃任务：智能体在尝试中途放弃任务，提交无意义的答案，或未经正确性检查就提交方案。这些失败常源于智能体在查看得出正确解所需的全部代码或信息之前就提交答案。

- 重复失败的操作：智能体重复不推进问题的同一行为，例如一遍遍运行导致错误的命令，而不尝试其他方法。

我们在表 2 中报告结果。我们发现超过三分之一的 GPT-4 失败源于重复失败的操作，而 o1 的 32 次中只有 2 次——我们把这视为模型适应错误能力提升的定量证据。一半的 o1 失败源于过早放弃任务，而 GPT-4 的失败只有四分之一源于此——这可能因为 o1 的失败发生在定性更难的任务上，也可能反映 o1 的特性。

### D.2 较新模型的具体技能

为更好语境化观察到的模型表现改进趋势，我们检视了较早模型（例如 GPT-4）显著差于当前模型的任务轨迹。具体而言，我们按所需专长类型对所有任务族分类，注意到当前模型在涉及机器学习训练、逆向工程编译后软件二进制与网络安全 CTF 的任务上往往胜过较早模型。此外，我们注意到智能体在需要对其自身局限的情境觉察或击败对抗策略的任务上大幅提升。这给了我们五组任务族来检视。

对每一组任务族，我们让承包商人工通读所有模型在所有任务上的全部运行，找出 AI 智能体在这些任务上改进的可能解释以及潜在局限。

如第 3.3 节所述，我们给出模型改进方式及其主要局限的示例。

#### D.2.1 较新模型做得更好的是什么？

我们先讨论当前模型相较 2023 年前模型改进的一些方式。对部分公开任务，我们还提供完整运行轨迹的链接。

##### 对错误更强的稳健性

模型随时间日益稳健，尤其似乎能避免重复失败的操作。早期模型通常连琐碎的错误也无法纠正，而是陷入循环行为或引入新错误。但从 GPT-4o 开始，模型展现出从错误中恢复与纠正方向的改进能力，这一能力在 pico_ctf 任务的较难变体或其他需要迭代的编码相关任务中尤其有价值。考虑一个需要调试少量 Python 代码的任务中的例子：

1. 在一次运行中，gpt-4-turbo-2024-04-09 因 Python 文件中一个错位的反斜杠字符引入语法错误，尽管尝试繁多，直到放弃也无法理解或修复该问题。

2. Claude 3.5 Sonnet（New）先把代码加错了位置，然后多次尝试用 CLI 工具 sed 把代码加到正确文件。但这样做时遇到 IndentationError 与重复的方法。最后它成功转向从头重写整个文件。

   ```text
   I apologize for the confusion. It seems that our previous attempt didn’t fully remove the old ‘save‘ method. Let’s try one more time to fix the ‘base_model.py‘ file. We’ll remove both ‘save‘ methods and add the correct one
   ...
   ```

   ```text
   I apologize for the persistent issue. It seems that our previous attempts didn’t fully resolve the problem. Let’s try one more time to fix the ‘base_model.py‘ file by completely rewriting the content of the file:
   ...
   ```

##### 工具使用

davinci-002（GPT-3）等早期模型在语法正确的工具使用上吃力，而后续模型随提示中的清晰解释与示例而改进。当前前沿模型一般能无碍地使用我们脚手架提供的工具。例如，我们注意到当任务需要编辑 Python 脚本时，GPT-3 即使有明确指示也在格式上挣扎，GPT-4o 有时用 bash 的 echo 命令逐行写脚本，而 o1-preview 能稳定高效地编辑文件。

1. 尽管用户消息中有关于预期格式的提醒，davinci-002 仍未能用带尖括号的正确语法。

   ```text
   No function call was included in the last message. Please include a function call in the next message using the <[tool_name]> [args] </[tool_name]> syntax.

   bash> touch test.txt
   python> import time
   python> time.sleep(10)
   python> exit()
   submit> python main.py
   ```

2. GPT-4o 有时难以有效编写 Python 脚本。在同一任务的一次运行中，它用单独的命令低效地逐行写脚本。

   ```text
   I will write the script content directly into the script file using echo commands, one line at a time.
   bash: {”command”:
     ”echo ‘def read_nth_line(file_path, n):’ >> update_test_txt.py”}
   bash: {”command”:
     ”echo ‘    with open(file_path, ”r”) as file:’ >> update_test_txt.py”}
   ```

3. o1-preview 在该任务上毫无问题地稳定编辑文件。

##### 改进的逻辑与程序化问题求解

与编码与推理基准上表现提升一致，我们看到模型编写语法与语义正确代码的能力逐渐增强。这使模型能更可靠地正确解读任务说明并用代码找到正确答案。

1. 例如，在 interpret_data 任务上，GPT-4o 在一次运行中因把「找出 1972 年世界第一高楼」的请求错误解读为「找出 1972 年建成的世界第一高楼」而失败——而不是常识解读即找出 1972 年当时的世界最高楼。例如它写了这样的代码：

   ```python
   tallest_building_1972 = data[data[’completion_year’] == 1972][’height_m’].max()
   tallest_building_1972
   ```

2. 相比之下，o1-preview 正确地把请求解读为找出 1972 年或之前建成的世界第一高楼。

#### D.2.2 它们仍然做不好的是什么？

尽管有改进，即便是当前前沿模型仍有显著的吃力之处。总体上，我们的观察表明智能体在定性上「更杂乱」的任务上表现更差。我们在第 F.2 节进一步考察这一主张。

##### AI 智能体在没有清晰反馈时吃力

没有清晰的反馈或低成本的验证方式（例如单元测试或答案检查脚本），我们测试的所有模型常常难以判断其解是否正确。例如，各时间桶中对模型最困难的两个任务是 'blackbox' 与 'symbolic regression'。这两个任务都涉及在探查信息有代价的约束下猜测一个隐藏函数。

##### AI 智能体常常不主动搜寻相关信息

我们还观察到所有模型在理解自身局限或主动搜寻有用信息上仍有欠缺；相反，模型倾向于假设自己已经知道如何完成任务，只在失败后才重新评估。

例如，在一个关于试验 API 接口的任务中，智能体被告知可以在本地的一份 markdown 文档中阅读该 API 的更多信息。即便最终成功，智能体通常一开始就 hallucinate 或猜测 API 端点，只有当从任务环境遇到错误后才去读 API 文档。

在一个夺旗任务中，智能体要用 python 打开一个未知编码的文件，常因指定错误编码而第一次失败。连最好的模型也只是在 python 脚本里换着编码尝试，低效且浪费 token。我们从未见过智能体运行能直接识别所需编码的 bash file 命令。

## 附录 E 进一步讨论

### E.1 常数因子与斜率变化

尽管外推总是不完美的，把 AI 时间视界预测到遥远的未来，对倍增速率的变化远比对时间视界的常数因子敏感。例如，基于 o1 的 39 分钟时间视界与 218 天（每年 3.2 倍）的历史倍增时间的朴素外推预测，AI 将在 o1 发布后约 4.8 年达到 1 个月 50% 时间视界（相对 o1 约需 8 次翻倍）。倍增时间增加 2 倍会把 1 个月节点再推迟 4.8 年，但时间视界的常数因子缩短 2 倍只会推迟 0.6 年。

### E.2 可能改变时间视界斜率的重要因素

##### 智能体式训练

自 2024 年以来的视界增长（可能快于长期趋势）可以这样解释：研究者用基于结果的强化学习对模型做后训练使其更具智能体性（即能执行通向任务完成的许多顺序行动）。让模型有能力且具智能体性的研究很可能继续。未来的智能体式训练可能快于长期趋势（因为后训练在提升视界长度上可能比预训练更省算力）。但 2024-2025 的智能体式训练也可能是摘低垂果实带来的一次性提升，这种情况下视界增长会在这些收益耗尽后放缓。总体而言，我们认为智能体式训练相比 2019-2024 趋势更可能提高时间视界增长率。

##### 算力扩展

从 GPT-2 发布至今，训练最令人印象深刻的前沿语言模型所用算力至少增长了 10,000 倍（Epoch AI, 2024），训练算力用量每 6-10 个月翻一番（Sevilla et al., 2022）。更近期，o1 与 o3 等模型开始在推理时使用更多算力。未来 5 年是否有足够产能把训练或推理算力再扩展多个数量级尚不清楚。但历史上降低了固定表现水平算力需求的算法进步（Erdil and Besiroglu, 2023；Ho et al., 2024）可以替代算力限制。我们认为算力扩展的极限会使 AI 智能体时间视界的增长有所放缓，但会被对算法改进的更多投入部分补偿。

##### AI 研发的自动化

AI 研发的主要投入是算力与研究者时间。如果未来 AI 系统能替代人类研究工程师和/或提升训练的算力效率，AI 进步的速率将提高。我们认为，一旦前沿 AI 时间视界达到数十小时，很可能出现实质性的 AI 研发自动化，缩短从那时到一个月视界 AI 的时间。

##### AGI 将拥有「无限」时间视界

无限时间视界并不意味着任意强大的 AI，而只是能完成人类需要任意长时间完成的任务。如果一个通用人工智能（AGI）能以至少 X% 的成功率完成专家人类能完成的所有任务，其 X% 时间视界必然是无限的。因此，如果此类系统终被开发，时间视界的长期趋势将快于指数，渐近线位于 AGI 部署之日。

### E.3 解读时间视界

尽管时间视界是 AI 智能体能力的直观度量，测量它需要标注有人类时间的大型数据集，且时间视界总是相对一个任务分布以及基线者的上下文与技能水平测量的。

##### 上下文与技能效应

在真实公司，初级软件工程师往往需要数周入职才能开始贡献经济价值。决定多数任务时长的人类基线者的上下文远少于普通员工，可能使测得的任务时长偏长。我们的任务设计为只需最少上下文，一定程度上缓解了该问题；我们的内部 PR（第 C.2 节）没有这样设计，因此基线者花的时间是员工的许多倍。但高技能基线者也能比普通员工快得多地完成任务。我们的专家基线者可能比平均软件工程师熟练得多，可能使我们测得的任务时长偏短。

##### 任务分布效应

图 3 表明 AI 智能体成功率并不能被人类完成时间完美预测，意味着其他因素也显著影响任务难度。当模型在研究数学、计算生物学或法律等其他智力劳动领域被测量时，我们预期其时间视界会有所不同。

##### 测量极端时间视界

准确测量一个 AI 智能体的 X% 时间视界约为 $t$ 分钟，需要许多人类时长为 $t$ 分钟、且 AI 智能体以约 X% 成功率完成的任务。这有两层含义。第一，准确测量很长的时间视界需要一个带长人类基线运行的困难任务数据集，构建起来可能不切实际，尤其因为真实困难任务的成功标准往往复杂到需要人工评分。第二，测量极高成功率水平（95%、98% 或更高）的时间视界，需要噪声接近零、覆盖其意在代表任务总体的极大数据集。

##### 人类时间视界测量

理论上，也可以测量一个人或一群人的时间视界。但这既有理论困难也有实践困难。我们在附录 C.1.4 中进一步讨论。

### E.4 局限与未来工作

我们相信本工作有若干可以改进之处。

##### 更多模型与更好的性能引出

总体上，我们发现恰当地引出（elicit）模型能使其表现产生很大差异[注17](#fn17)。我们在引出模型使其在任务上有良好表现上投入的努力有限，因此虽然我们的结果是合理的下界，一些模型的能力可能比我们展示的更强。引出上投入最多的是 o1 与最初的 Claude 3.5 Sonnet，各自投入了约 2-3 个工程师周的迭代开发。所有其他模型使用相同脚手架，至多做轻微改动。未来工作可以在引出前沿模型的全部能力上投入更多努力来复现我们的结果。

注 17：这是常见观察；例如 AIDE 带来的软件开发能力提升（Jiang et al., 2025），或近期关于 KernelBench 的工作（METR, 2025）。

##### 更严格的人类基线

我们每任务的人类时间估计可能因样本量相对较小而有噪声，且可能以各种方式系统性偏斜。最值得注意的是，我们只筛选任务的成功完成，并鼓励基线放弃他们可能无法在合理时间内完成的任务。我们基线者的技能也差异很大，而这些任务相关的技能五花八门。虽然我们试图给基线者匹配适当任务，该过程不可能完美。从对基线尝试的人工审查中，我们还观察到人类有时在任务看似在其能力之内时也会放弃，不清楚这对成功时间分布产生了什么选择效应。人类基线时间中的偏置可能如何影响结果的进一步讨论见附录 C.1.4。未来工作可以用更严格的人类基线者选择复现结果，或探索结果对基线方法学选择的敏感性。

##### 更自然、更多样的任务

有理由相信我们的任务分布与有经济价值工作的分布系统性不同（也可能与风险模型相关任务的分布系统性不同）。我们在第 4 节探索了其中一些原因，但还有许多差异未探索。例如，这些任务的交互模态也相对窄——例如没有任务需要使用鼠标。没有任务需要与人类或其他智能体合作或竞争[注18](#fn18)，而真实软件工程或机器学习研究涉及与经理及其他工程师或研究者沟通协调。许多真实世界任务要求极高可靠性，而由于在这些任务上测量模型的困难，这些在我们的数据集中代表性不足。最重要的是，我们研究的任务严重偏向软件工程与机器学习研究。未来工作可以探索 AI 智能体能力在其他领域的进展。

注 18：Xu et al.（2024）是一个需要相对真实场景下多智能体交互的近期基准示例。

##### 更多地使用推理算力

我们的脚手架对推理时算力的使用相对有限。假设人类专家报酬为每小时 143.61 美元（Google L4 工程师平均年薪除以 2,000 小时），超过 80% 的成功运行成本低于人类执行同一任务成本的 10%（图 14）。这意味着如果推理时计算可以用来提升表现，仍有大量空间可以在保持与人类专家成本竞争力的同时这么做。此前研究发现 best-of-k 等技术可以显著提升在这些任务一个子集上的表现（Wijk et al., 2024），更好地使用推理时算力可能带来显著不同的分数。

##### 数据分析

2024-2025 趋势似乎快于 2019-2025 趋势，但由于模型数量少，不清楚这是否为噪声。未来工作应包括检测可能的 2024 年斜率变化的假设检验，以及用更精细的统计方法为总体预测建立可信区间。我们还在多阶段估计——把基线数据转换为任务难度评级、时间视界计算、以及寻找趋势的线性回归——中损失了一些信息，端到端方法可能更省数据。

## 附录 F 外部效度细节

### F.1 从 2023-2025 数据回测

作为本文探索性工作的一部分，我们只用 HCAST 与 RE-Bench 套件测量了 2023 与 2024 年发布的 9 个前沿与近前沿模型的时间视界。该趋势（加入 Claude 3.7 Sonnet 与 o3 后）见图 10：时间视界大约每六个月翻一番。由于我们只有两个 2023 年模型（GPT-4 0314 与 GPT-4 1106）且数据范围小（发布日期跨 2 年、时间视界跨 5 次翻倍），误差棒非常宽。此外，把数据进一步限制为仅 2024 年模型产生了时间视界约每三个月翻一番的不同趋势，因此任何对未来的外推都不稳健。

为解决这些问题，我们收集了更多数据把趋势线延伸到过去，开发了软件原子动作（SWAA）套件，把任务套件的最短人类时间从 1 分钟降到 2 秒以下，使我们能在合并套件上测量 GPT-2、davinci-002（GPT-3）与 GPT-3.5-turbo-instruct。

2023-2025 趋势可能快于更长期趋势（图 11）。2019-2025 全部六年的实测倍增时间为 207 天，不如基于非 SWAA 任务与 2023-2025 模型的 172 天趋势陡峭。但这一差异仍在误差范围内。

### F.2 杂乱度因子

现实世界的智力劳动常涉及基准通常不包含的杂乱细节，例如规约不足或范围不清、反馈回路或成功标准模糊、或需要多线工作之间的实时协调。我们总体观察到智能体在有这些「杂乱」细节的任务上更吃力（第 3.3 节）。因此一个自然的问题是：智能体在「不那么杂乱」与「更杂乱」的任务上是否表现出相似的改进速率。

我们按预期 1) 能代表真实世界任务可能比我们研究的任务系统性更难、且 2) 与 AI 智能体表现相关的 16 项性质给 HCAST 与 RE-Bench 任务评级。一些示例因子包括任务是否涉及新颖情境、是否受有限资源约束、是否涉及实时协调、或是否源自真实世界场景。我们给 RE-bench 与 HCAST 任务标注这 16 项杂乱因子的有无，然后求和得到 0 到 16 的「杂乱度得分」。因子定义见附录 H.6。

HCAST 与 RE-Bench 任务的平均杂乱度得分为 3.2/16。没有任务的杂乱度得分高于 8/16。作为对比，「写一篇好研究论文」这类任务依具体情形会得 9/16 到 15/16。

在 HCAST 任务上，AI 智能体在更杂乱任务上的表现确实差于仅按任务长度的预测（b=-0.081，$R^{2}$ = 0.251），见图 13。任务杂乱度每增加 1 分，平均成功率约降低 8.1%[注19](#fn19)。

注 19：这里用线性近似来直观地粗略量化该效应的大小。

不过，任务套件中较低与较高杂乱度子集的 AI 智能体表现随时间的趋势相似。例如，在小于一小时的任务上，2023 年 1 月到 2025 年 5 月间高低杂乱度两组的成功率都提高了 40 个百分点（图 12）。特别是，我们没有发现较高杂乱度子集特有的明显更慢的表现趋势或平台期。

## 附录 G 其他表格与图

以下是不在正文中的若干图，来自外部效度等章节。

表 7：按模型与任务来源的平均成功率

| 任务来源 | HCAST | RE-Bench | SWAA |
| --- | --- | --- | --- |
| Claude 3 Opus | 0.25 | 0.00 | 0.98 |
| Claude 3.5 Sonnet (New) | 0.46 | 0.11 | 0.99 |
| Claude 3.5 Sonnet (Old) | 0.38 | 0.05 | 1.00 |
| Claude 3.7 Sonnet | 0.58 | 0.04 | 1.00 |
| GPT-2 | - | - | 0.40 |
| GPT-4 0314 | 0.23 | 0.00 | 0.98 |
| GPT-4 1106 | 0.30 | 0.02 | 0.97 |
| GPT-4 Turbo | 0.23 | 0.00 | 1.00 |
| GPT-4o | 0.30 | 0.00 | 0.98 |
| davinci-002 (GPT-3) | 0.00 | 0.00 | 0.65 |
| gpt-3.5-turbo-instruct | 0.01 | 0.00 | 0.95 |
| o1 | 0.54 | 0.07 | 1.00 |
| o1-preview | 0.44 | 0.02 | 1.00 |
| o3 | 0.65 | 0.40 | - |
| o4-mini | 0.61 | 0.27 | - |

![Refer to caption](2503.14499v4/plots/logistic/single_line_2023_ga_rebench.png)

图 10：HCAST + RE-bench 上自 GPT-4 0314 起的模型的时间视界。

![Refer to caption](2503.14499v4/plots/logistic/double_line_all_data_retrodict_excluding_swaa.png)

图 11：按发布日期排列的模型时间视界完整时间序列。我们用蓝色绘出仅基于 2023+ 数据在 HCAST + RE-Bench 任务上的回归并延伸到过去，用灰色绘出全部任务（含 SWAA）在整个六年期间的回归。图中的点是模型在包括 SWAA 的全部数据上的时间视界。

![Refer to caption](2503.14499v4/plots/messiness/success_trend_by_messiness_and_length_with_boundary_0.5.png)

图 12：HCAST 与 RE-Bench 任务按长度与杂乱度划分的表现随时间的趋势（第 F.2 节）。数据只跨 2023-2025，因为 2023 年前的模型在非 SWAA 任务上得 0 分。虽然更杂乱的任务平均成功率更低，但模型表现改进的趋势在高杂乱度分组上并没有明显更慢。

![Refer to caption](2503.14499v4/plots/messiness/messiness_effect_expanded_combined_alpha_0.010.png)

图 13：我们把超额成功率（观察到的经验任务成功率减去用任务长度预测的成功率，见第 3.1 节）对每个任务的杂乱度得分作图。如第 F.2 节所述，超额成功率与杂乱度之间存在负相关。

![Refer to caption](2503.14499v4/plots/cost/ratio_vs_length.png)

图 14：用 LLM 智能体成功运行一次的成本，作为人类专家执行同一任务薪水成本的比率。

## 附录 H 更多消融与稳健性检查

衡量「完成一个『定义明确的任务』所需时间」有很多方式，因此我们的分析涉及许多略有任意的选择。为确保结果稳健，我们用方法学的改动复现了结果，发现结果对这些改动大体稳健。

由于我们用这些分析来指导方法学选择，这些消融是相对于一个与最终报告略有不同的流水线版本执行的。特别是，它们包含略不同的基线集合与不同的任务成功筛选。

1. 替代曲线拟合（第 H.1 节）

2. 把任务套件重新归一化为对数均匀以外的分布

3. 替代的任务难度估计方式

4. 对基线者能力的敏感性：

   - 我们主观上非常有信心的基线者

   - 把任务套件限制为至少有 2 次基线的任务，用每任务的最佳基线时间作为难度估计

   - 把任务套件限制为至少有 2 次基线的任务，用每任务的最差基线时间作为难度估计

   - 给基线时间加噪声（见图 6）

5. 任务选择：去掉 RE-Bench 任务

6. 任务族的不同加权：$\frac{1}{\sqrt{\text{family size}}}$ vs 均匀（见图 6）；还有 $\frac{1}{\text{family size}}$

7. 估计的训练日期 vs 发布日期估计

8. 连续计分：图 16

### H.1 替代曲线拟合

![Refer to caption](2503.14499v4/plots/horizon_alternative_fits.png)

图 15：2019 年以来模型时间视界的线性、双曲与指数拟合。

在我们的主要结果中，我们拟合指数曲线（对数 y 轴下为线性），因为拟合非常好（$R^{2}\geq 0.96$，取决于具体数据与方法）。线性与双曲曲线拟合不佳（图 15）。由于我们研究的时间跨度内只有 12 个前沿模型，而指数拟合只用两个参数就有如此高的 $R^{2}$，我们认为应用参数更多的拟合更可能过拟合而非给出准确预测。特别地，我们考虑过：

- 双指数函数 $\log(\mathrm{horizon})\sim a+b\exp(c\cdot(\mathrm{release\_date}+d))$ 严格比指数更具表达力（因为当 $c$ 小时 $\exp(x)\approx x$，两者等价）

- 同样，任何饱和逻辑斯蒂函数 $\mathrm{horizon}\sim a\cdot\sigma(\mathrm{release\_date}+d)$ 的初始部分看起来非常像指数，而且在没有任何证据表明 AI 视界（用我们的指标）正在趋平的情况下，基本上不可能预测它何时、是否、以及会平台化多久。

- 渐近到无穷的复杂随机模型往往有很大不确定性；见 Roodman（2020），它把一个超指数扩散模型应用于经济数据。如我们在第 5 节讨论的，为长期预测构造预测区间时大不确定性可能是恰当的，但对我们提到的这些因素的潜在影响做定量建模超出了本文范围，因此我们更愿意定性讨论。

![Refer to caption](2503.14499v4/plots/logistic/partial_scoring.png)

图 16：连续（非二值化）计分下的时间视界。Claude 3.7 Sonnet 的 50% 时间视界接近 2 小时。我们认为该方法学从 8 小时的 RE-Bench 任务中捕捉到更多信号，但高估了近期模型的时间视界，因为在多数任务上达到平均 0.5 分比 50% 的时间追平人类表现更容易。斜率也很可能被高估，因为更长的任务往往采用连续计分。

### H.2 80% 成功率下的视界

在图 17 中，我们展示模型 80% 时间视界随时间的趋势。倍增时间与 50% 图相似，但视界显著更低。

![Refer to caption](2503.14499v4/plots/logistic/p80.png)

图 17：80% 成功率时间视界的趋势。倍增时间与 50% 图相似，但视界显著更低。50% 视界趋势以灰色显示。

### H.3 成功率与推理成本

在图 18 中，我们把模型在我们任务上的成功率作为 token 成本的函数作图。所研究的所有模型在更大 token 预算下表现更好，但多数模型显示在远低于各自分配的最大 token 数之前就出现明显的平台期。

![Refer to caption](2503.14499v4/plots/success_over_resource/line_generation_cost_with_humaninvsqrt_task_weightscore_binarized.png)

图 18：按成本的成功率。模型被给予足够高的 token 上限以达到成功率的平台期。o3 与 o4-mini 的成本信息未包含。

### H.4 2024-2025 视界增长趋势

![Refer to caption](2503.14499v4/plots/logistic/double_line_2024_trendline.png)

图 19：50% 时间视界的 2024-2025 与 2019-2025 指数拟合。

如果 2024-2025 视界增长趋势持续超过 2019-2023 斜率，未来工作应做变点分析以确定斜率差异是否统计显著。

### H.5 SWE-bench Verified

##### 数据收集

我们从官方 SWE-bench 评估结果仓库收集了前沿模型的每模型、每任务结果：Claude 3 Opus、Claude 3.5 Sonnet（Old）、Claude 3.5 Sonnet（New）、GPT-4 1106、GPT-4o 与 o1。注意这只是我们主要结果所含 11 个模型中的 6 个。

##### 时间估计

SWE-bench Verified 包含承包商创建的时间估计，把任务分为四桶：<15 分钟修复、15 分钟-1 小时、1-4 小时、或 >4 小时。这些估计基于「一位花了几小时熟悉代码库的工程师」解决该 issue 预计所需的时间。

我们通过在 6 个 SWE-bench Verified 任务上运行 7 次基线来验证标注者的时间桶。我们在「<15 分钟修复」桶做了四个任务的基线，发现我们的基线者分别花了 8、26、67 与 84 分钟。我们在「1-4 小时」桶做了两个任务的基线，两名基线者都花了 2-3 小时。

##### 分析方法

我们把标注者的时间范围估计转换为每任务的时间估计，做法是取时间桶起止时间的几何平均。我们选择 16 小时作为 SWE-bench Verified 任务的上限，但该时间桶只有 3 个任务，不会显著影响结果。然后我们用与第 3 节相同的方法，把每模型、每任务的结果与任务时间估计转换为模型时间视界。为降低相似任务的影响，我们把涉及同一仓库 issue 的任务视为同一任务族，并按同族任务数的平方根降权任务的贡献。

| 任务时间桶 | 任务时间估计 | 平均基线时间 |
| --- | --- | --- |
| <15 分钟修复 | 3.9 min | 32.9 min |
| 15 分钟-1 小时 | 30.0 min | – |
| 1-4 小时 | 120.0 min | 131.6 min |
| >4 小时 | 480.0 min | – |

表 8：我们取时间标注的几何平均，把 SWE-bench Verified 的时间标注转换为任务估计。我们提醒，这很可能低估了无上下文的人类基线者解决每个 issue 所需的时间——值得注意的是，我们观察到「<15 分钟修复」桶中随机抽取的四个任务的基线者时间几何平均为 32.9 分钟。

##### 标注者 vs 承包基线者时间

如表 8 所示，我们发现标注者的时间估计在「<15 分钟修复」时间桶上可能更不准确，因为实践中基线者完成任务往往远超这个时间。这导致较容易任务的难度被低估，意味着 SWE-bench Verified 的时间视界估计很可能低估能力较弱模型的真实表现，进而导致更陡的指数趋势。

|  |  |  |  |
| --- | --- | --- | --- |
| 模型 | （我们的任务）模型时间视界 | （SWE-bench Verified）模型时间视界 | 时间视界比 |
| Claude 3 Opus | 6.42 min | 0.83 min | 7.8x |
| GPT-4 1106 | 8.56 min | 1.18 min | 7.2x |
| GPT-4o | 9.17 min | 5.96 min | 1.5x |
| Claude 3.5 Sonnet (Old) | 18.22 min | 5.91 min | 3.1x |
| Claude 3.5 Sonnet (New) | 28.98 min | 16.88 min | 1.7x |
| o1 | 39.21 min | 51.21 min | 0.8x |

表 9：能力较弱模型的时间视界在我们的任务上显著长于 SWE-bench Verified。

### H.6 杂乱度因子

杂乱度因子标签由 2 名内部承包商与 1 名研究者收集。

所用杂乱度因子与定义的完整清单见表 10 与表 11。

表 10：杂乱度因子定义 1-8

| 因子 | 定义 |
| --- | --- |
| 真实来源 | 该任务是否：要么 1. 意在代表某个真实世界的端到端任务（若不确定，则多半如此），要么 2. 源自一个真实问题，且 3. 未被有意简化为更容易更小的子任务。 |
| 资源受限 | 该任务是否：需要使用有限且一次性消耗的资源，且两者兼备：1. 明智地使用该资源比明智地使用默认资源限制（时间、token、成本）更关乎任务成败 2. 该资源在任务内不易补充（例如对验证器的有限查询次数，或对智能体得分扣减的永久猜测计数器） |
| 不易重置 | 在没有采取非常明显糟糕的行动的前提下，智能体若愿意是否难以把（与任务成功相关的）状态重置回初始状态？（例如 rm -rf 掉环境过于明显糟糕）要易于重置，应无需事先规划即可做到，但可以基于到目前为止的行动历史回溯。 |
| 存在不可逆失误的可能 | 你是否认为有相当可能（>20%）第 20 百分位的人类（来自具备任务领域背景但对该具体任务无先验上下文的人群）会在其前 50% 的任务时间里犯一个会永久且不可逆地降低其可得分数的错误？ |
| 动态环境 | 任务是否涉及与一个变化环境的交互且该交互对任务成功显著，即便智能体不采取任何行动？若任务的显著部分如此即为真，即便并非整个任务期间都如此。 |
| 困难的反事实 | 任务是否有显著关乎成功的部分，其中智能体难以判断某个效应应归因于它自己的行动（或不行动），还是归因于其他因素？一个例子是智能体优化一个分布式计算系统性能的任务。在该任务中系统偶尔出现级联变慢与故障，但任务提示中未提及。如果智能体在做某个看似无关的优化，可能难以判断这些故障的起因是智能体直接改动的下游影响、随时间变化的负载差异、还是随机波动等等。另一个例子是加入日志等调试行为会改变被记录系统的行为，从而使观察系统并分离不同干预的因果效应更难。 |
| 非纯自动评分 | 该任务是否没有完全自动的评分函数？具体而言，对按任务标准实现的任务：1. 评分函数没有返回 None 的分支，且 2. 任务在这些情形下提供了人工评分说明，且 3. 没有关于遵守实际上未在自动评分中检查的规则的条款。（例如某个任务族有「不得尝试逆向工程 X」的指示，但自动评分函数不检查这一点） |
| 需要隐式泛化 | 是否显著可能以某种方式满足提示中陈述的成功条件，但任务的精神实际上未被履行、或产品对隐含目的无用？例如，一个要求智能体训练好的小模型的任务可能有若干明确陈述的得分条件，如达到的损失或准确率。但满足这些要求的字面可能并不足以让方案对隐含目的（此例中即「做出一个好模型」）有用。例如，每生成一个 token 要花一分钟 的模型似乎没什么用。这可以看作解决方案要泛化到隐含用例的隐式要求。这一列的精神基本上是「智能体是否必须对任务提示未必明确陈述的软约束做出合理判断，才能产出对任务隐含有用的输出」？对没有强理由认为存在隐含目的的玩具任务，此项为假。并且 这些隐式泛化要求在评分中是否被检查（由评分函数或人工判断/审查）？（例如，有些任务有额外的人工审查阶段检查钻空子方案，这算数。其他任务用人工评分者的判断检查输出是否有用。） |

表 11：杂乱度因子定义 9-16

| 因子 | 定义 |
| --- | --- |
| 评分描述不明确 | 两者都须为真：其一：a. 对智能体评分所依据的约束并非全部明确陈述，或 b. 评分的描述方式使评分中仍有显著的隐藏信息；且其二：这种评分信息的缺乏在任务内产生关于最佳行动路线的任务相关不确定性。（例如在两个被优化的因素之间权衡，但其在评分中的确切权重不确定）例如，一个只要求返回 2022 年 3 月有多少天的任务不算评分描述不明确，因为这种信息缺失没有引入任务相关的不确定性。 |
| 次优行为被利用 | 该任务是否涉及与其他智能体或程序竞争，而后者会主动利用智能体（或其输出）的弱点或次优行为？有某种对抗性程序或行为的任务是典型例子。 |
| 无提供的验证机制 | 任务没有提供让智能体在运行中检查其答案或分数的方式。需要智能体做相当一部分工作才能检查答案。 |
| 实时协调 | 该任务是否需要与其他智能体或服务实时协调，或需要胜任地并行编排多个实时过程？对此，监视一个进行中的训练运行不算，除非任务预期/要求智能体并行执行多次训练运行（或类似活动）。 |
| 需要自我修改 | 该任务是否要求智能体修改自身的一部分、或用于与环境交互的代码、或为自己创建新工具、或创建可用于此目的的数据？ |
| 需要自我改进 | 该任务是否要求智能体以某种永久提升其在广泛任务分布上表现的方式改进自身？例如，对 AI 智能体，创建能提升智能体自身通用智能体表现的微调数据即满足此项。但创建提升某个狭窄任务表现的微调数据不满足（而满足自我修改）。 |
| 需要信息搜寻 | 任务需要收集智能体不太可能预先知道的信息。例如探查一个新颖系统的行为。 |
| 新颖情境 | 任务有某种不寻常的约束或性质，没有它任务会显著更容易或更机械，且它是任务困难性的重要来源。 |

在图 20 中，我们把 HCAST 任务的杂乱度得分对对数人类完成时间作图。我们发现杂乱度与任务长度相关，且高杂乱度得分的短任务很少。我们还按模型表现给每个点上色。杂乱度高且人类耗时长的任务往往成功率低，较短、杂乱度低的任务则相反。

![Refer to caption](2503.14499v4/images/length_vs_messiness.png)

图 20：更杂乱的任务往往更长。

我们的杂乱度因子的一个局限是，它们至少在某种程度上是针对当前模型对抗性选择的。这是因为一方面选择了被认为与模型表现相关的因子，另一方面所有这些因子都被预期使任务更难。因此，我们可能预期模型表现与我们的任务杂乱度度量的负相关比应有的更强——且基于杂乱度的预测性调整对远在本分析之前或之后发布的模型效果更差。

![Refer to caption](2503.14499v4/plots/messiness/success_trend_by_messiness_with_boundary_0.5.png)

图 21：模型在 HCAST + RE-Bench 任务上的成功率，按任务杂乱度评级划分。模型在较不杂乱的任务上成功率更高，但随时间的改进速率在两个子集上相似。davinci-002 与 gpt-3.5-turbo instruct 在杂乱度较高的 HCAST + RE-Bench 子集上均得 0 分。

### H.7 随机化文件名

为更好理解杂乱度对智能体与人类表现的影响，我们修改了一个现有的 HCAST 任务——该任务涉及翻查本地 LaTeX 与 PDF 文件以找到特定信息——做法是随机化文件名、文件夹名，并减少关于搜索内容的信息。

#### H.7.1 方法

被修改的 HCAST 任务名为 Local Research TeX。未修改版本把智能体环境初始化为一组嵌套的文件夹与内容，然后提示用户找到某个具体信息，例如提示「根据 AR 报告，表现最好的智能体完成了多少任务？」。智能体（或人类）随后必须搜索本地文件夹与内容以找到该问题的具体答案（此例中为「四」）。我们以多种方式修改了该任务，最值得注意的变体包括：

1. 把提示从「根据 AR 报告」改为「在 /home/agent/resources/ 中的某个资源里找到以下问题的答案」：

2. 把所有文件夹名改为随机整数，所有文件名改为「final」或「my_file」等无意义名称。

然后我们在该任务的原始变体与修改版本上各运行了约一百次智能体，并比较各自的成功率。我们还用标准基线方法计算了人类完成时间。

#### H.7.2 结果

出乎意料的是，o1 在更杂乱的报告变体上平均表现更好，而人类基线者表现差得多。

| 任务变体 | 成功率 | 基线者时间 |
| --- | --- | --- |
| local_research_tex/ar_report | 34% | 24 分钟 |
| local_research_tex/ar_report_scrambled_files | 50% | 53 分钟 |

定性上，o1 在打乱文件名变体上似乎表现好得多，因为其提示中没有「AR 报告」一词。实践中，o1 常决定 grep「AR 报告」一词却找不到（因为实际报告名为「ARA 报告」），然后猜一个答案。另一方面，当被告知在某个资源中查找时，o1 执行更通用的搜索，并（更经常地）找到它要找的报告。虽然这只是一个有限的例子，我们相信它进一步说明了量化与预测任务各面如何影响智能体表现的挑战——事实上，让人类在某些任务上更差的因素确实可能提升智能体表现。

### H.8 智能体间的表现相关

在图 22 中，我们报告每对模型之间每任务成功率的相关矩阵。

##### 超额成功率

超额成功率（$\frac{S_{observed}-S_{predicted}}{S_{predicted}}$）是一个度量，衡量 AI 智能体相对我们在给定任务长度与该模型能力下的预期的表现好（或差）多少（预期成功率见图 4）。

在图 23 中，我们报告超额成功率 $({S_{observed}-S_{predicted}})/{S_{predicted}}$（其中 $S_{predicted}$ 是从模型时间视界预测的成功率）的相关矩阵。虽然超额成功率的相关低于原始任务成功率的相关（0.38 对 0.71），但它为正这一事实表明，存在跨模型共同、能解释各模型在任务间成功率的额外因素。

![Refer to caption](2503.14499v4/plots/success_correlations/observed_success_rates_correlations.png)

图 22：所有模型与任务上观察成功率的的相关矩阵。

![Refer to caption](2503.14499v4/plots/success_correlations/fractional_excess_success_rates_correlations.png)

图 23：所有模型与任务上超额成功率（定义为 $\frac{S_{observed}-S_{predicted}}{S_{predicted}}$）的相关矩阵。

![Refer to caption](2503.14499v4/plots/bootstrap/headline-linear.png)

图 24：前沿模型时间视界随时间的变化。注：显示的数据与图 1 相同，但采用线性轴。

![Refer to caption](2503.14499v4/plots/logistic/all_models.png)

图 25：我们测量的所有模型（含非前沿模型）的时间视界。

![Refer to caption](2503.14499v4/plots/bootstrap/headline-log.png)

图 26：前沿模型随时间能胜任的任务的人类专家钟表时间长度。
时间视界长度的计算细节见第 3 节。
直线代表线性回归拟合，置信区域由分层自助法计算。
在此图中，davinci-002 与 gpt-3.5-turbo-instruct 分别放在 GPT-3 与 GPT-3.5 的发布日期，GPT-2 在我们的脚手架不兼容的较长任务上的分数插补为零。注：这与图 1 相同，只是呈现方式不同。

## 附录 I 代码

复现本文部分核心图表的代码与数据将在补充材料中提供；完整代码库无法公开与匿名化，但作者可应评审者要求提供单个额外图表的代码。

## 附录 J 作者贡献

Thomas Kwa 领导了 SWAA 任务的开发，编写了大部分数据分析代码，并撰写了终稿的最大份额，包括生成约一半的图表。Ben West 执行了初始分析，并共同领导本项目。Joel Becker 领导了 RE-Bench 与 HCAST 任务的人类基线流程与数据收集，并贡献了早期数据分析代码。Amy Deng 创建了大部分 SWAA 任务，收集了 SWAA 任务上的人类基线与 AI 智能体结果。她还调查了智能体与任务失败，并协助获取 HCAST 任务上的智能体结果。Katharyn Garcia 编写了评估与数据分析代码。Max Hasin 领导定性印象工作并撰写了关键章节，收集了内部 PR，并贡献了数据分析代码与基线收集。Sami Jawhar 贡献了任务运行与数据分析基础设施。Megan Kinniment 执行了杂乱度实验、超额成功率与初始可靠性分析，监督了许多 HCAST 任务的创建，并贡献了图表与写作。Nate Rush 领导了 SWE-Bench 与内部 PR 实验并起草了论文的相应章节。Sydney Von Arx 监督了内部效度分析。

Brian Goodrich 贡献了 modular-public 智能体的开发，并创建了 flock 与 duet 智能体。Nikola Jurkovic 为 SWAA 与 RE-Bench 任务做了基线并测试了 RE-Bench 任务。Seraphina Nix 贡献了论文与图表的写作与修订。David Rein 管理了 HCAST 任务的开发与收集，并监督了这些任务的人类基线流程。Lucas Jun Koba Sato 领导了 AI 智能体的开发与 HCAST 任务上智能体结果的收集。Chris Painter 提出了重大的框架与呈现修改建议。Neev Parikh 贡献了外部效度实验的运行。

Elizabeth Barnes 帮助发展了基本概念，建议了实验/分析，提供反馈，并协助写作/早期任务开发/分析代码。Lawrence Chan 共同领导了本项目，包括设定总体方向、帮助决定运行哪些实验，并贡献了论文的大部分写作。
