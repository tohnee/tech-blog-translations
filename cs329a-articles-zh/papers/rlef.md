---
title: "RLEF：用强化学习将代码 LLM 锚定在执行反馈上"
title_en: "RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning"
arxiv: 2410.02089
source: https://arxiv.org/abs/2410.02089
crawled: 2026-09-23
translated: 2026-09-23
---

# RLEF：用强化学习将代码 LLM 锚定在执行反馈上


> 原文：[RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning](https://arxiv.org/abs/2410.02089) · Stanford CS329A 指定阅读

Jonas Gehring、Kunhao Zheng、Jade Copet、Vegard Mella、Quentin Carbonneaux、Taco Cohen、Gabriel Synnaeve（Meta AI (FAIR)；邮箱：{jgehring,gab}@meta.com）

2026 年 8 月 24 日

###### 摘要

以智能体形式部署的大型语言模型（LLM）在多个步骤上求解用户指定的任务，同时把所需的人工介入降到最低。关键在于，这类 LLM 需要把自身的生成锚定在所获得的反馈上，才能可靠地达成期望的结果。我们提出一种端到端的强化学习方法，教模型在代码合成领域利用执行反馈——在该领域，最先进的 LLM 与独立采样相比一直难以迭代地改进代码。我们在竞赛编程任务上做基准测试，用小模型（8B 参数）与大模型（70B）都取得了新的最先进结果，同时把所需样本量降低了一个数量级。我们对推理时行为的分析表明，我们的方法得到的 LLM 能够在多个步骤上有效利用自动反馈。

## 1 引言

图 1：Llama 3.1 模型经 RLEF 训练后在 CodeContests 上的求解率，与此前报告的各采样预算下的结果对比（对数尺度）。

大型语言模型（LLM）能力的持续提升，促使研究者与开发者把它们基准化并部署到越来越复杂的环境中（Brown et al., 2020；OpenAI, 2023；AI @ Meta, 2024）。一个新兴的研究方向是把 LLM 用作智能体，在极少甚至没有人类监督的情况下多步求解任务，按需或按人工脚手架的指示查询外部计算或数据源（Schick et al., 2023；Kapoor et al., 2024）。例如，此类 LLM 的自主化应用有助于：以最新信息确保对用户查询的准确回答（Mialon et al., 2024）、与网站交互（Yao et al., 2022），或根据高层描述生成代码以实现软件功能（Yang et al., 2024）。

我们认为，任何提供自然语言接口的决策智能体都必须具备两项技能。其一，在收到提示时准确推断用户意图；对 LLM 而言，这通常通过按用户偏好微调以遵循指令来实现（Ouyang et al., 2022；Rafailov et al., 2023）。其二，必须把对智能体行动中间结果的反馈纳入考量，才能达成期望的结果。例如，包含必要信息的网页可能已下线，需要再发起一次搜索引擎查询。在代码生成的语境中，反馈可以提供实现缺陷的信息，以及那些完整、详尽地指定起来低效或繁琐的约束，例如软硬件平台细节或库依赖。因此，中间反馈对于把 LLM 的生成锚定在推理时遇到的具体情形上至关重要。

图 2：左：执行反馈强化学习（RLEF）概览。LLM 被反复提示根据问题描述实现代码。每次尝试在公共测试集上评估；失败时，反馈被插入对话。若公共测试通过、或达到指定的轮数上限，则在额外的私有测试上的执行结果决定奖励。随后用 PPO 更新模型。右：包含两个模型响应的示例对话。执行反馈提示首个解法效率低下，模型随之响应使用缓存。通过公共测试集的代码将在完整测试集上评估。

在本工作中，我们旨在让预训练 LLM 在「从自然语言描述合成代码」这一领域（Chen et al., 2021；Rozière et al., 2023）具备上述技能：任务对齐以及锚定于推理时反馈。在这里，反馈以生成代码的执行结果自然地给出，形式为错误信息与单元测试结果。然而迄今为止，把这类反馈用于 LLM 代码生成，在考虑计算开销时并未带来实质提升；事实上，在固定推理预算下，独立采样往往能取得更高的准确率（Kapoor et al., 2024；Xia et al., 2024）。作为研究并改进执行反馈锚定的试验平台，我们提出把代码生成框定为迭代任务：反复要求 LLM 依据所给自然语言描述生成代码（图 2）。每次生成后，代码在示例测试用例上评估，所得反馈作为额外上下文提供给后续尝试。由此我们得到一个交互式环境：行动对应代码，观察对应执行反馈。重要的是，这样的框定允许用强化学习（RL）算法做端到端优化，以最大化一个奖励信号——这里是一个二元奖励，取决于最终代码解是否通过一组留出测试用例。

我们在 CodeContests（Li et al., 2022）——一个有挑战性的竞赛编程基准——上对这一在强化学习语境中结合重复代码行动与执行反馈的训练方法（RLEF）进行基准测试。从 Llama 3.1 模型（AI @ Meta, 2024）出发，我们取得了显著的性能提升，超越了此前最先进的结果，同时把所需生成次数降低了一个数量级（图 1）。我们的分析表明，RLEF 训练解锁了利用推理时机器反馈的能力，使 LLM 在迭代式、多轮场景中行之有效。RLEF 在 CodeContests 上的改进还泛化到 HumanEval+ 与 MBPP+ 这两个流行的代码合成基准，并泛化到高于训练时的样本预算。

## 2 方法

### 2.1 迭代式代码合成

我们把代码合成任务组织为多轮对话：反复提示 LLM 为一道自然语言问题描述生成代码解。每个解之后，我们提供一条自动生成的响应，内容是在测试用例上执行该解代码所得的结果。这一设定适用于面向聊天场景与用户交互这一常见用途调优的语言模型，并沿用此前代码生成自我修复方面的工作（Shinn et al., 2023；Olausson et al., 2024）。

关键在于，我们使用两组不同的测试用例：*公共*（public）测试产生的执行反馈可在反复尝试中获取，并构成选择最终解的基础；而*私有*（private）测试集最终决定最终解的正确性。分离的测试集有两大好处。第一，若测试输入输出固定，留出测试可以防范优化过程中的捷径——LLM 依据执行反馈在后续回答中照抄期望的测试输出。第二，运行完整测试套件可能计算开销很大，而有限的公共测试集可以加速迭代式代码生成过程。不过，在推理时最大化执行反馈的测试覆盖或许更可取，我们验证了这确实能提升性能（附录 B.2 节）。

我们的代码生成对话流程如图 2 所示。具体而言，对话以问题描述开始，向 LLM 请求一个初始解。该解在公共测试集上验证，产生通过/未通过的测试用例结果，以及可能的语法或运行时错误。若有任何公共测试失败，这条执行反馈会被格式化并追加到对话中。随后向 LLM 请求更新后的代码解，提示中包含原始问题文本、先前的解及各自的反馈。若解通过全部公共测试，或达到指定轮数上限，则视为最终解并提交到私有测试集上评估。提示与执行反馈模板的清单请参见附录 C。

### 2.2 执行反馈强化学习

上一节描述的迭代式代码合成可理解为一个马尔可夫决策过程（MDP），语言模型则作为策略（Sutton & Barto, 2018）。为通用起见，我们假设部分可观测 MDP，因为我们的奖励函数使用一个策略无法访问的留出私有测试集（除非问题描述中恰好给出了期望程序行为的精确文本表示）。观察与行动以分词后的文本序列给出。具体地，初始观察 $o_0$ 是问题描述，每步 $t$ 的行动 $a_t$ 是文本回复。后续观察 $o_t$ 由过往观察与行动组成，包括在公共测试用例上评估前一个行动 $a_{t-1}$ 得到的执行反馈。当公共测试评估成功或达到指定步数上限时，回合终止。回合结束时，依据全部公共与私有测试是否通过给出一个标量奖励。我们不使用奖励折扣（即 $\gamma=1$）。

为在上述环境中优化策略，我们采用近端策略优化（PPO）——微调大型语言模型的常见选择（Schulman et al., 2017；Ziegler et al., 2020；Ouyang et al., 2022）。沿用先前工作，我们在奖励信号中加入 KL 惩罚，它既充当熵奖励，也起到向初始 LLM 分布正则化的作用。在初期实验中我们发现一种可能的失败模式是非最终回复中生成了无效代码，我们通过对无效回复施加小惩罚来解决。记待优化策略为 $\pi$、初始策略为 $\rho$，并缩写过往观察与行动为 $c_t=o_0,a_0,o_1,a_1,\dots,o_t$，则第 $t$ 步的奖励函数为

$$R(s_{t},a_{t})=r(s_{t},a_{t})-\beta\log\frac{\pi(a_{t}|c_{t})}{\rho(a_{t}|c_{t})},\quad r(s_{t},a_{t})=\begin{cases}1,&\text{若回合结束且全部测试通过}\\ -1,&\text{若回合结束且有任一测试失败}\\ -0.2,&\text{若 }a_{t}\text{ 不含有效代码}\\ \end{cases}$$

其中常数 $\beta$ 在任务奖励与 KL 最大化之间权衡。对 PPO，我们通过引入 concurrently 学习的价值函数作为基线来计算策略梯度，即训练策略以最大化优势 $A_t=-V(c_t)+\sum_{i=t}^{T}R(s_i,a_i)$；见附录 A.1 节。

我们注意到，尽管上述 MDP 把完整回复视为行动，底层的策略与价值函数是逐 token 输出的语言模型实现。因此，在我们的设定中选择合适的行动空间用于优化需要斟酌，合适的选择可能取决于手头的具体任务。我们提出在 token 层面建模策略、同时为整轮学习价值函数；与把两个模型都放在轮或 token 层面优化相比，这种混合做法在我们早期实验中效果最佳。因此，我们从每个回复 $a_t$ 对应提示的最后一个 token 预测该回复的价值，并对回复内的每个 token 行动使用同一优势值。我们基于回复的价值估计与 Zhou et al. (2024) 密切相关；但我们不训练额外的 Q 函数。对 KL 惩罚，我们发现把回复概率 $\pi(a_t|c_t)$ 计算为 token 概率的几何平均而非乘积是有益的。这抵消了一种可能有害的偏向较短生成的偏差，对非最终回复尤其如此。

## 3 实验结果

### 3.1 设定

我们在 Li et al. (2022) 提出的 CodeContests 基准上实验，该基准要求为自然语言描述的问题生成代码解，问题描述附带公共测试用例的文本描述。问题难度高，用于人类竞赛编程，聚焦算法、数据结构与运行效率。解的正确性用对参赛者隐藏的私有测试评估；在我们的设定中，这体现为只呈现来自公共测试的反馈。CodeContests 数据集由一个训练集和两个测试集（"valid" 与 "test"，分别含 117 和 165 道题）组成；我们用前者做模型与超参数选择。我们在训练集上优化模型，并因缺少公共或私有测试用例而从 13,328 道题中剔除 669 道。我们提示并训练所有模型输出 Python 3 代码。

Llama 3 系列模型（AI @ Meta, 2024）构成我们的初始策略，具体为 3.0 与 3.1 发布版中的 Instruct 8B 与 70B 参数模型。这些模型开箱即有很强的代码生成表现，并能遵循提示中的指令，省去了 RL 训练前的初始微调阶段。训练与评估期间，除非特别说明，轮数上限设为允许 LLM 对每道题尝试 3 次。我们分别对 8B 与 70B 模型进行 12,000 与 8,000 次更新，并依据验证集表现选择检查点。超参数与更多实验细节见附录 A。

我们沿用 Li et al. (2022) 以 $n@k$ 平均求解率报告结果。$n@k$ 指标表示从总共 $k$ 个样本中选出 $n$ 个解、其中任一解正确（即通过全部测试）的期望。在我们的多轮设定中，每一轮计为一个样本。这样可以在样本预算上做公平比较——在采用高推理成本大型 LLM 的智能体脚手架中这一点尤为重要（Kapoor et al., 2024）¹。

注 1：为简单起见，我们在评估中把一次完整的 LLM 回复计为单个样本。我们还注意到，对迭代式代码生成而言，分配的样本预算可能不会被完全用满，因为公共测试一旦成功运行将导致对话提前终止。

### 3.2 主要结果

| 模型 | 来源 | $n@k$ | 验证集 | 测试集 |
| --- | --- | --- | --- | --- |
| AlphaCode 9B | Li et al. (2022) | 10@1000 | 16.9 | 13.3 |
| AlphaCode 41B + 聚类 | Li et al. (2022) | 10@1000 | 21.0 | 16.4 |
| Code Llama 34B + PPO | Xu et al. (2024) | 10@1000 | 19.7 | 22.4 |
| AlphaCodium gpt-3.5-turbo-16k | Ridnik et al. (2024) | 5@100 | 25 | 17 |
| AlphaCodium gpt-4-0613 | Ridnik et al. (2024) | 5@100 | 44 | 29 |
| MapCoder gpt-3.5-turbo-1106 | Islam et al. (2024) | 1@23 | - | 12.7 |
| MapCoder gpt-4-1106-preview | Islam et al. (2024) | 1@19 | - | 28.5 |
| Llama 3.0 8B Instruct | 本文 | 1@3 | 4.1 | 3.2 |
| 1ex + RLEF | 本文 | 1@3 | 12.5 | 12.1 |
| Llama 3.1 8B Instruct | 本文 | 1@3 | 8.9 | 10.5 |
| 1ex + RLEF | 本文 | 1@3 | 17.2 | 16.0 |
| Llama 3.1 70B Instruct | 本文 | 1@3 | 25.9 | 27.5 |
| 1ex + RLEF | 本文 | 1@3 | $\bm{37.5}$ | $\bm{40.1}$ |
| Llama 3.1 8B Instruct | 本文 | 10@100 | 21.7 | 24.8 |
| 1ex + RLEF | 本文 | 10@100 | 29.8 | 28.7 |
| Llama 3.1 70B Instruct | 本文 | 10@100 | 50.2 | 50.3 |
| 1ex + RLEF | 本文 | 10@100 | $\bm{54.5}$ | $\bm{54.5}$ |

表 1：我们的初始模型与 RLEF 训练模型在 CodeContests 上与先前工作的结果对比。$n@k$ 中的样本预算 $k$ 指 LLM 回复数，例如我们的 1@3 对应单次 rollout 中最多三个模型回复。每个样本预算（至多 10、至多 100）下的最佳结果以粗体标出。70B 模型经 RLEF 后取得最先进结果，总体上显著优于 AlphaCodium 与 MapCoder，并在测试集上以少量样本取胜。RLEF 训练的 8B 模型以 100 个样本超过 AlphaCodium，以 3 个样本超过 MapCoder（gpt-3.5-turbo）。

表 1 列出我们最多三轮迭代式代码生成在 CodeContest 验证集与测试集上的求解率，以及此前报告的结果。从我们的模型采样时，1@3 用温度 0.2，10@100 用温度 1.0，所有情形都用 top-p 0.95 的核采样（Holtzman et al., 2020）。每个求解率在 200 次 rollout 上用 Li et al. (2022) 描述的估计量估计。我们对比 AlphaCode（Li et al., 2022）与 Xu et al. (2024) 在 Code Llama 34B 上以测试执行为奖励的 PPO，二者都以大量样本报告结果。AlphaCodium（Ridnik et al., 2024）与 MapCoder（Islam et al., 2024）是构建在专有 GPT 模型之上的高性能智能体框架，结合了思维链提示、代码执行、程序修复，以及（就 AlphaCodium 而言）自动测试生成。

经 RLEF 训练，我们较原始 Llama 3.1 模型显著改进，并以明显优势超越先前工作。值得注意的是，在测试集上 70B 模型以单次 rollout 击败此前最先进的 AlphaCodium（GPT-4 版）——后者为 100 个样本中取 5 个解（38.0 对 29）。同样，RLEF 的 8B 模型略胜规模相近的 AlphaCode 9B（16.0 对 13.3），但我们只用 3 个样本预算，AlphaCode 则用 1,000 个。虽然无法与更近的 AlphaCode 2（AlphaCode Team, 2023）直接比较，但其 10@100 在验证集上的性能估计为 34.2，而我们的 70B 模型仅用 3 个样本即领先（37.5）²。考虑 100 个样本的更大预算（相当于 33 次 rollout）时，原版 70B 模型即超过所有此前报告的结果，包括 AlphaCodium 在验证集上的表现。经 RLEF 训练后，我们进一步提升到验证集与测试集上的 54.5。相较 1@3 设定，10@100 设定下相对初始模型的改进虽然仍显著，但有所收窄。Kirk et al. (2024) 观察到 LLM 的 RL 训练会降低输出多样性，我们把我们的结果解读为对这一假说的进一步佐证。

注 2：AlphaCode Team (2023) 在未公开的竞赛题上训练与评估，但报告相对 AlphaCode 有 10,000 倍的样本效率提升；AlphaCode 在验证集上取得 10@1M 求解率 34.2。

表 1 还凸显：已发布的 Llama 3.1 模型在 CodeContests 上从起步就具备竞争力，我们把这归因于指令微调期间对编码能力的侧重（AI @ Meta, 2024）。不过，我们的 RLEF 方法对此前发布的 3.0 8B 模型同样高效，把 1@3 求解率在验证集与测试集上分别从 4.1 提升到 12.5、从 3.2 提升到 12.1。因此，对可以自动评估的任务，RLEF 或许可作为指令微调的部分替代。

### 3.3 推理时行为

| 模型 |  | CC. Test |  |  | HumanEval+ |  |  | MBPP+ | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  | ST | MT |  | ST | MT |  | ST | MT |
| Llama 3.1 8B Instruct |  | 11.8 | 10.5 |  | 65.3 | 63.9 |  | 58.3 | 60.5 |
| 1ex + RLEF |  | 9.7 | 16.0 |  | 67.5 | 69.5 |  | 57.0 | 63.1 |
| Llama 3.1 70B Instruct |  | 26.2 | 27.4 |  | 73.2 | 75.0 |  | 66.9 | 70.2 |
| 1ex + RLEF |  | 30.3 | 40.1 |  | 78.6 | 80.4 |  | 67.6 | 72.2 |
| gpt-4o-2024-05-13 |  | 25.3 | 24.3 |  | 82.8 | 80.7 |  | 68.8 | 71.7 |

表 2：基础模型与 RLEF 模型在单轮（ST）与多轮（MT）设定下的 1@3 求解率。在 CodeContests 上，除非采用 RLEF 训练，迭代式代码生成至多带来 modest 的收益，甚至造成性能下降。RLEF 在 CodeContests 多轮设定下的改进可迁移到 HumanEval+ 与 MBPP+，后者需要略作不同的执行反馈格式化。求解率在每题 20 次 rollout 上估计，温度 0.2。

表 2 中我们先细看固定 3 次 LLM 生成预算（1@3）下的单轮与多轮表现。这对应我们最多三个模型回复的迭代设定，或三个独立回复的单轮结果。我们还考虑向两个流行的代码生成基准 HumanEval+ 与 MBPP+（Liu et al., 2023b）的泛化：我们将其改造以匹配我们的迭代式代码生成设定——"base" 测试用于推理时执行反馈，"plus" 测试用于求解率估计（细节见 C.4 节）。结果表明，在固定样本预算下，基础模型在多轮代码生成设定中很少能从访问错误解与执行反馈中获益。这对 gpt-4o-2024-05-13 同样成立：它在 CodeContests 与 HumanEval+ 上独立采样解时表现更强。RLEF 训练后，8B 与 70B Llama 3.1 模型都能从执行反馈中获益，因而在改进的单轮分数之上取得更大收益——例外是 8B 模型在 CodeContests 与 MBPP+ 上单轮性能有所下降。尽管 RLEF 的多轮收益在 CodeContests（我们的模型训练领域）上最显著，我们在 HumanEval+ 与 MBPP+ 上也观察到可观改进。

图 3：初始模型与 RLEF 训练模型针对公共测试结果的行为分析，8B（上）与 70B（下）模型。在每题 20 次 rollout（共 5640 次）内，我们统计初始解（第 1 轮）中的错误；在第 2、3 轮被改为正确代码的错误数；以及依 chrF 指标衡量相邻解之间的代码改动量。RLEF 训练的模型初始犯错更少、更可靠地修复错误、并做更大的代码编辑；初始模型则频繁重复先前的解。使用随机执行反馈时，错误恢复严重受损。

接下来，我们试图确定 RLEF 训练的收益源自何处。基于表 2 中改进的单轮结果，我们假设对 70B 模型而言，部分收益来自在竞赛编程题这一特定领域上的训练。更重要的是，8B 与 70B 模型在迭代设定下的更高分数，既可能归因于在同一次 rollout 内采样的解更多样，也可能归因于基于执行反馈的更有针对性的自我修复。为探测模型对所见反馈的敏感性，我们用*随机*执行反馈做推理时消融。随机反馈的实现方式是：执行一道无关题目的错误解，但若当前解通过公共测试仍结束对话（细节见 C.2 节）。

图 3 中，我们考察（与执行反馈相关的）公共测试上的错误，覆盖验证集与测试集合计 20 次 rollout。我们观察到，RLEF 训练后，8B（上排）与 70B（下排）模型在首个回复中产生错误输出更少，但更容易超出时限。在后续回复中，从所有错误类别中恢复的能力显著改善。然而使用随机反馈时，自我修复明显受损，说明 RLEF 使 LLM 能有效利用所提供的反馈。我们还通过计算相邻代码间的字符 n-gram F 值（Popović, 2015，chrF）来衡量从一个回复到下一个回复的改动（图 3 右）。这凸显了未经 RLEF 的 Instruct 模型的一个缺点：它们只做极小的代码编辑；事实上我们观察到，即便内联反馈指出了错误，它们仍频繁输出同样的代码解。

上面对图 3 的分析提示：有了 RLEF，同一 rollout 内的样本更多样（代码相似度更低），但编辑也是有针对性的，因为随机执行反馈导致成功修复更少。这一发现与图 4(a) 相呼应，其中我们在不同轮数上限下比较真实反馈与随机反馈的模型。这里我们比较 pass@1 与 pass@10 指标，不考虑因轮数上限不同导致的样本预算差异（Chen et al., 2021）。pass@1 刻画得到正确最终解的精准度，pass@10 反映召回某个正确解的能力（即 10 个解中是否有任意一个通过私有测试）。在验证集与测试集上，随机反馈都导致 pass@1 下降，且随轮数上限增大而被放大。这为随机反馈下修复能力更缺乏针对性提供了进一步证据，因为程序无法被可靠地修复。值得注意的是，使用真实反馈时，产生正确解的概率随轮数上限提高而持续上升。对 pass@10，真实与随机执行反馈的差异不那么明显。由于该指标可以通过在对话内采样大量多样的候选解来优化，这些结果表明：面对随机反馈，我们的模型退而求其次，采样一系列多样的、可能正确的解。

最后，我们在给定样本预算下评估跨轮数上限的泛化。图 4(b) 中，我们以温度 1.0 做 rollout，通过提高生成多样性来突出更高样本预算下的表现。我们把 $k$ 个样本均匀分配到不同轮数上限的 rollout 上，计算 $10@k$ 求解率。对 8B 模型（上排），RLEF 训练前，除测试集上 30 个样本以上的情形外，独立采样（1 轮）可获得最佳表现。初始 70B 模型以 3 或 5 轮表现更好，尽管在小预算下单轮表现也有竞争力。RLEF 之后，我们观察到 3、5、10 轮相对独立采样带来一致改进，5 轮表现最佳。在所有情形下，固定样本预算时把轮数上限提高到 10 都没有收益。

(a)

(b)

图 4：(a) RLEF 训练模型在不同轮数上限下的 pass@1 与 pass@10，分别提供真实或随机执行反馈（温度 0.2）。随机反馈下 pass@1 降低而 pass@10 仅轻微受损，表明程序无法被一致地修复。(b) 各样本预算下轮数上限对 10@k 求解率的影响（上：8B 模型，下：70B 模型），温度 1.0。经 RLEF，迭代式代码生成可利用最多 5 轮达到计算最优性能。

### 3.4 消融研究

| 模型 | 方法 | 验证集 | 测试集 |
| --- | --- | --- | --- |
| 8B Instruct | – | 8.9 | 10.5 |
|  | Few-Shot | 8.5 | 8.5 |
|  | SFT | 10.3 | 10.0 |
|  | RLEF | 17.2 | 16.0 |
| 70B Instruct | – | 25.9 | 27.5 |
|  | Few-Shot | 22.5 | 20.3 |
|  | SFT | 27.7 | 27.2 |
|  | RLEF | 37.5 | 40.1 |

(a)

| 模型 | 训练 | 验证集 |  | 测试集 |  |
| --- | --- | --- | --- | --- | --- |
|  |  | ST | MT | ST | MT |
| 8B Instruct | – | 9.4 | 8.9 | 11.6 | 10.5 |
|  | ST | 10.3 | 10.2 | 9.9 | 10.9 |
|  | MT | 16.2 | 17.2 | 9.5 | 16.0 |
| 70B Instruct | – | 25.6 | 25.9 | 25.9 | 27.5 |
|  | ST | 28.3 | 31.1 | 27.3 | 32.9 |
|  | MT | 25.8 | 37.5 | 30.3 | 40.1 |

(b)

表 3：从 Llama 3.1 模型出发的 1@3 求解率，温度 0.2。(a) 获得迭代式代码合成能力的不同方法比较。RLEF 是最有效的训练方法，其次是有监督微调（SFT）。我们发现少样本提示对 Instruct 模型有害。(b) 用我们的 RL 循环比较常规单轮（ST）训练与我们的多轮（MT）训练。MT 训练比 ST 带来更大改进，而「单轮训练收益迁移到多轮推理」仅限于 70B 模型。

#### 3.4.1 学习迭代式代码合成

我们研究除 RL 训练外，LLM 能否借助少样本提示（Brown et al., 2020）与有监督微调（SFT）在多轮代码生成中奏效。由于缺少适合 SFT的真值训练样例，我们用 Llama 3.1 70B Instruct 在 CodeContests 训练集上挖掘 rollout，并按最终解的正确性过滤。然后我们在挖掘得到的语料上微调 Llama 3.1 8B 与 70B 参数模型的 Base 与 Instruct 版本，并把该语料用作少样本示例来源（A.3 节）。表 3(a) 的结果表明，少样本提示对指令微调模型有害。在 B.1 节中我们报告预训练模型的少样本 1@3 求解率，发现其表现低于指令模型的零样本提示（8B 在验证集与测试集上分别为 1.2 和 1.8，70B 分别为 4.6 和 5.8）。有监督微调仅在验证集上改进 Instruct 模型表现；测试集上未见改进。对预训练模型，SFT 有改进但分数低于指令微调模型（B.1 节）。RLEF 带来的求解率显著高于 SFT 模型，凸显了我们 RL 训练循环的效力。

#### 3.4.2 单轮训练

表 3(b) 中，我们把迭代式代码生成设定与传统的单轮生成相比较，后者不向模型呈现推理时反馈。我们对单次生成使用相同的训练循环，只是去掉对无效代码的惩罚（2.2 节），因为它已被错误解的奖励信号涵盖。对 Llama 3.1 Instruct 8B，单轮训练（ST）损害测试集表现。70B 模型受益于单轮训练，超过表 3(a) 中多轮 SFT 的结果。此外，我们观察到迁移效应：把单轮模型用于多轮设定能提高 1@3 求解率。我们把这归因于原版 70B Instruct 模型既有但相对较弱的多轮能力。总体而言，在训练与推理时都使用多轮的 RLEF 方法表现最强。

更多消融见附录。B.3 节中，我们评估在表 3(b) 单轮 8B 训练的输出上训练一个专用修复模型的效果，类似 Le et al. (2022)。单轮模型加修复模型在验证集与测试集上分别取得 1@3 求解率 14.8 与 12.6；优于单轮模型单独的表现（10.2 与 10.9），但显著低于对应的多轮模型（17.2 与 16.0）。B.4 节中我们表明，训练期间 withheld 公共测试执行反馈会导致显著更差的表现。最后，B.5 节用实验验证了轮级价值函数这一设计选择（2.2 节）。

## 4 相关工作

近年来，用 LLM 生成程序代码以自动化并辅助软件开发已被广泛研究，评估主要聚焦于从自然语言描述合成代码（Clement et al., 2020；Chen et al., 2021；Austin et al., 2021）。性能的一大跃升来自：在预训练中纳入大量源代码，并为后续面向指令遵循的微调选择或生成合适数据（Li et al., 2023；Gunasekar et al., 2023；Rozière et al., 2023；AI @ Meta, 2024）。

近期，若干工作研究了提升推理时表现的提示与流程工程技术，包括通过编译与执行验证生成的代码并再提示。Shinn et al. (2023) 与 Chen et al. (2024b) 用单元测试的反馈纠正先前的错误生成，并发现把模型生成的错误分析纳入后续生成的提示中至关重要。LDB（Zhong et al., 2024）、AlphaCodium（Ridnik et al., 2024）与 MapCoder（Islam et al., 2024）可视为智能体框架，因为它们为代码生成提供丰富的人工脚手架，串联多次 LLM 调用（例如用于思维链规划、测试生成与程序修复）并结合代码执行。这些方法在我们本文考虑的 CodeContests 等困难基准上有效，但每个解需要数十次 LLM 调用，显著推高了推理成本。

近期工作进一步指出 AlphaCodium、MapCoder 之类脚手架的问题。Olausson et al. (2024) 表明：独立采样代码解与修复错误代码相当有竞争力；提供有效的错误反馈需要大模型；多轮修复并不有效。Kapoor et al. (2024) 聚焦推理成本，证明在同等采样预算下，独立采样胜过 Shinn et al. (2023) 与 Zhong et al. (2024) 的方法。借助我们的方法，LLM 的自我修复能力可以被大幅增强，使迭代式代码生成在小与大样本预算下都有更优表现。与此同时，我们主张用领域专属的微调取代复杂、领域专属的提示工程与脚手架。

用强化学习微调大型语言模型是使其输出对齐用户偏好的流行方法（Ziegler et al., 2020；Touvron et al., 2023；OpenAI, 2023；DeepSeek-AI et al., 2024；AI @ Meta, 2024）。其中学习信号由专用奖励模型提供。但对代码合成而言，奖励可以通过在可用测试用例上执行 LLM 生成来确定（Le et al., 2022；Shojaee et al., 2023；Dou et al., 2024；Yu et al., 2024）。Le et al. (2022) 预训练一个代码生成 LLM，随后用策略梯度与下一 token 损失在执行奖励上微调。他们从微调期间得到的 rollout 中进一步训练了预测测试结果标签的模型与把错误解映射到真值解的模型，从而支持基于测试结果的推理时代码纠正（"critic sampling"），不过并未显式呈现执行输出。随后 Liu et al. (2023a) 以更细粒度的扩展奖励函数延伸了该工作。最后，Xu et al. (2024) 在更简单的设定中以单元测试二元奖励微调更强的代码专用 LLM，并在我们考虑的这个困难竞赛编程基准上观察到 RL 带来的实质改进。我们同样提出一个简单设定：无额外推理脚手架、不使用真值解。关键的是，我们把自然语言到代码的设定扩展为一个迭代环境，其中执行反馈不仅以标量奖励提供，也以文本形式提供。这使我们能用单一模型同时获得代码合成与代码修复能力，并把重心从大样本推理模式转向以低样本预算取得高准确率。

与我们的工作同期，Kumar et al. (2024) 提出两阶段 RL 方法（SCoRe）以改进 LLM 的自我纠正能力，训练其输出两个连续的解。与我们的方法不同，SCoRe 在推理时不利用执行反馈，而是要求模型重新审视其初始解。虽然这一思路有望应用于无自动反馈的领域，却无法受益于反馈消息中携带的信息。此外，推理时反馈可帮助模型在训练后泛化到新环境。最后，Chen et al. (2024a) 研究带人类反馈的代码生成，并基于训练单独的代码修复模型发展出相应的有监督微调策略。在我们的工作中，我们只用单一模型就有效利用了以自然语言格式化的自动生成反馈。

以往把强化学习应用于 LLM 更长时程决策任务的工作，强调获得在环境中锚定的必要能力。Carta et al. (2023) 报告，以任务成功完成衡量，用 PPO（Schulman et al., 2017）做 RL 调优优于有监督训练，可锚定于文字导航游戏。Zhou et al. (2024) 提出一族面向 LLM 的 RL 算法，在文字游戏（对抗 oracle LLM）与用简化网店 API 购物中测试；Zhai et al. (2024) 则处理视觉观察的环境，调整预训练视觉 LLM 的参数。尽管动机相似，我们处理的是一个本质上不同的领域——代码合成，其行动空间（合法 Python 程序的空间）远大于先前工作。

## 5 结论

在本工作中，我们提出了执行反馈强化学习（RLEF），一种 LLM 微调方法，赋予其自主运行的一项关键能力：把未来生成锚定于环境反馈。我们把 RLEF 应用于迭代式代码合成，在 CodeContests 竞赛编程基准上取得求解率的大幅提升，同时降低了推理所需的样本预算。RLEF 训练的模型还泛化到更高的轮数上限，以及 HumanEval+ 与 MBPP+ 这两个编程题更简单、执行反馈格式不同的流行代码生成基准。我们的深入分析揭示：虽然首轮正确生成的增加与后续生成多样性的提升构成了性能的主要来源，我们的模型也切实地把执行反馈纳入考量，并在多轮中解决错误。

##### 局限性。

尽管我们的结果展示了对推理时反馈的有效利用，我们考虑的代码合成任务局限于改进针对给定问题的单个解。把我们的方法泛化到包含需要分解的更大任务的环境——借助人工脚手架，或最终以自主引导的方式——仍是进一步研究的课题。基于单元测试执行结果迭代自然需要测试用例，而后者未必唾手可得。我们认为与自动单元测试生成（Watson et al., 2020；Jain et al., 2024）的结合是进一步实验的有吸引力的方向。

##### 更广泛的影响。

成功把 LLM 锚定于代码生成执行反馈，将放大其在辅助软件开发、执行质量控制等高影响力任务上的效用。但总体而言，提升如今已广泛部署于各类应用的 LLM 的能力，需要质量控制与护栏来促进安全并最小化潜在有害输出。我们把研究限于源代码生成，并把模型生成输出的执行限制在本地沙箱中。我们认为 Shavit et al. (2023) 关于 AI 智能体治理的框架对从业者是有用的资源。

##### 可复现性声明。

我们全部实验都使用公开可得的模型与数据集。3.1 节描述了数据集与预处理步骤、所用 Llama 模型的确切版本，并详述评估指标。训练的损失函数与超参数以及计算基础设施的描述见 A.1 节。A.3 节描述（较窄的）有监督微调超参数范围，A.2 节包含训练与评估期间代码执行的说明。全部提示列于附录 C。

##### 致谢。

我们感谢 Chris Cummins、Olivier Duchenne、Fabian Gloeckle、Baptiste Roziere、Sten Sootla、Nicolas Usunier 与 Sida Wang 的技术贡献、建议与富有洞见的讨论。

## 参考文献
- AI @ Meta (2024)

  Llama Team AI @ Meta.
  The Llama 3 Herd of Models.
  Technical report, 2024.
- AlphaCode Team (2023)

  Google DeepMind AlphaCode Team.
  AlphaCode 2 Technical Report.
  Technical report, 2023.
- Austin et al. (2021)

  Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le, and Charles Sutton.
  Program Synthesis with Large Language Models.
  *arXiv:2108.07732 [cs]*, Aug 2021.
- Brown et al. (2020)

  Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei.
  Language Models are Few-Shot Learners.
  In *NeurIPS*, 2020.
- Carta et al. (2023)

  Thomas Carta, Clément Romac, Thomas Wolf, Sylvain Lamprier, Olivier Sigaud, and Pierre-Yves Oudeyer.
  Grounding Large Language Models in Interactive Environments with Online Reinforcement Learning.
  *arXiv:2302.02662 [cs]*, Sep 2023.
- Chen et al. (2024a)

  Angelica Chen, Jérémy Scheurer, Tomasz Korbak, Jon Ander Campos, Jun Shern Chan, Samuel R. Bowman, Kyunghyun Cho, and Ethan Perez.
  Improving Code Generation by Training with Natural Language Feedback.
  *arXiv:2303.16749*, Feb 2024a.
- Chen et al. (2021)

  Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Pondé de Oliveira Pinto, Jared Kaplan, Harrison Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Joshua Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba.
  Evaluating Large Language Models Trained on Code.
  *arXiv:2107.03374 [cs]*, Jul 2021.
- Chen et al. (2024b)

  Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou.
  Teaching Large Language Models to Self-Debug.
  In *ICLR*, 2024b.
- Clement et al. (2020)

  Colin B. Clement, Dawn Drain, Jonathan Timcheck, Alexey Svyatkovskiy, and Neel Sundaresan.
  PyMT5: Multi-mode translation of natural language and Python code with transformers.
  In *EMNLP*, 2020.
- DeepSeek-AI et al. (2024)

  DeepSeek-AI, Qihao Zhu, Daya Guo, Zhihong Shao, Dejian Yang, Peiyi Wang, Runxin Xu, Y. Wu, Yukun Li, Huazuo Gao, Shirong Ma, Wangding Zeng, Xiao Bi, Zihui Gu, Hanwei Xu, Damai Dai, Kai Dong, Liyue Zhang, Yishi Piao, Zhibin Gou, Zhenda Xie, Zhewen Hao, Bingxuan Wang, Junxiao Song, Deli Chen, Xin Xie, Kang Guan, Yuxiang You, Aixin Liu, Qiushi Du, Wenjun Gao, Xuan Lu, Qinyu Chen, Yaohui Wang, Chengqi Deng, Jiashi Li, Chenggang Zhao, Chong Ruan, Fuli Luo, and Wenfeng Liang.
  DeepSeek-Coder-V2: Breaking the Barrier of Closed-Source Models in Code Intelligence.
  *arXiv:2406.11931 [cs]*, Jun 2024.
- Dou et al. (2024)

  Shihan Dou, Yan Liu, Haoxiang Jia, Limao Xiong, Enyu Zhou, Junjie Shan, Caishuang Huang, Wei Shen, Xiaoran Fan, Zhiheng Xi, Yuhao Zhou, Tao Ji, Rui Zheng, Qi Zhang, Xuanjing Huang, and Tao Gui.
  StepCoder: Improve Code Generation with Reinforcement Learning from Compiler Feedback.
  *arXiv:2402.01391 [cs]*, Feb 2024.
- Gunasekar et al. (2023)

  Suriya Gunasekar, Yi Zhang, Jyoti Aneja, Caio César Teodoro Mendes, Allie Del Giorno, Sivakanth Gopi, Mojan Javaheripi, Piero Kauffmann, Gustavo de Rosa, Olli Saarikivi, Adil Salim, Shital Shah, Harkirat Singh Behl, Xin Wang, Sébastien Bubeck, Ronen Eldan, Adam Tauman Kalai, Yin Tat Lee, and Yuanzhi Li.
  Textbooks Are All You Need.
  *arXiv:2306.11644 [cs]*, Jun 2023.
- Holtzman et al. (2020)

  Ari Holtzman, Jan Buys, Li Du, Maxwell Forbes, and Yejin Choi.
  The Curious Case of Neural Text Degeneration.
  In *ICLR*, 2020.
- Islam et al. (2024)

  Md Ashraful Islam, Mohammed Eunus Ali, and Md Rizwan Parvez.
  MapCoder: Multi-Agent Code Generation for Competitive Problem Solving.
  *arXiv:2405.11403 [cs]*, May 2024.
- Jain et al. (2024)

  Kush Jain, Gabriel Synnaeve, and Baptiste Rozière.
  TestGenEval: A Real World Unit Test Generation and Test Completion Benchmark.
  *arXiv:2410.00752 [cs]*, Oct 2024.
- Kapoor et al. (2024)

  Sayash Kapoor, Benedikt Stroebl, Zachary S. Siegel, Nitya Nadgir, and Arvind Narayanan.
  AI Agents That Matter.
  *arXiv:2407.01502 [cs]*, Jul 2024.
- Kirk et al. (2024)

  Robert Kirk, Ishita Mediratta, Christoforos Nalmpantis, Jelena Luketina, Eric Hambro, Edward Grefenstette, and Roberta Raileanu.
  Understanding the Effects of RLHF on LLM Generalisation and Diversity.
  In *ICLR*, 2024.
- Kumar et al. (2024)

  Aviral Kumar, Vincent Zhuang, Rishabh Agarwal, Yi Su, John D. Co-Reyes, Avi Singh, Kate Baumli, Shariq Iqbal, Colton Bishop, Rebecca Roelofs, Lei M. Zhang, Kay McKinney, Disha Shrivastava, Cosmin Paduraru, George Tucker, Doina Precup, Feryal Behbahani, and Aleksandra Faust.
  Training Language Models to Self-Correct via Reinforcement Learning.
  *arXiv:2409.12917 [cs]*, Sep 2024.
- Le et al. (2022)

  Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio Savarese, and Steven C. H. Hoi.
  CodeRL: Mastering Code Generation through Pretrained Models and Deep Reinforcement Learning.
  In *NeurIPS*, 2022.
- Li et al. (2023)

  Raymond Li, Loubna Ben Allal, Yangtian Zi, Niklas Muennighoff, Denis Kocetkov, Chenghao Mou, Marc Marone, Christopher Akiki, Jia Li, Jenny Chim, Qian Liu, Evgenii Zheltonozhskii, Terry Yue Zhuo, Thomas Wang, Olivier Dehaene, Joel Lamy-Poirier, Joao Monteiro, Nicolas Gontier, Ming-Ho Yee, Logesh Kumar Umapathi, Jian Zhu, Ben Lipkin, Muhtasham Oblokulov, Zhiruo Wang, Rudra Murthy, Jason T. Stillerman, Siva Sankalp Patel, Dmitry Abulkhanov, Marco Zocca, Manan Dey, Zhihan Zhang, Urvashi Bhattacharyya, Wenhao Yu, Sasha Luccioni, Paulo Villegas, Fedor Zhdanov, Tony Lee, Nadav Timor, Jennifer Ding, Claire S. Schlesinger, Hailey Schoelkopf, Jan Ebert, Tri Dao, Mayank Mishra, Alex Gu, Carolyn Jane Anderson, Brendan Dolan-Gavitt, Danish Contractor, Siva Reddy, Daniel Fried, Dzmitry Bahdanau, Yacine Jernite, Carlos Muñoz Ferrandis, Sean Hughes, Thomas Wolf, Arjun Guha, Leandro Von Werra, and Harm de Vries.
  StarCoder: May the source be with you!
  *Transactions on Machine Learning Research*, 2023.
- Li et al. (2022)

  Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hubert, Peter Choy, Cyprien de Masson d’Autume, Igor Babuschkin, Xinyun Chen, Po-Sen Huang, Johannes Welbl, Sven Gowal, Alexey Cherepanov, James Molloy, Daniel J. Mankowitz, Esme Sutherland Robson, Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, and Oriol Vinyals.
  Competition-Level Code Generation with AlphaCode.
  *arXiv:2203.07814 [cs]*, 378:1092–1097, Dec 2022.
- Liu et al. (2023a)

  Jiate Liu, Yiqin Zhu, Kaiwen Xiao, Qiang Fu, Xiao Han, Wei Yang, and Deheng Ye.
  RLTF: Reinforcement Learning from Unit Test Feedback.
  *TMLR*, 11/2023, 2023a.
- Liu et al. (2023b)

  Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang.
  Is Your Code Generated by ChatGPT Really Correct? Rigorous Evaluation of Large Language Models for Code Generation.
  In *NeurIPS*, 2023b.
- Loshchilov & Hutter (2019)

  Ilya Loshchilov and Frank Hutter.
  Decoupled Weight Decay Regularization.
  In *ICLR*, 2019.
- Mialon et al. (2024)

  Grégoire Mialon, Clémentine Fourrier, Craig Swift, Thomas Wolf, Yann LeCun, and Thomas Scialom.
  GAIA: A benchmark for General AI Assistants.
  In *ICLR*, 2024.
- Olausson et al. (2024)

  Theo X. Olausson, Jeevana Priya Inala, Chenglong Wang, Jianfeng Gao, and Armando Solar-Lezama.
  Is Self-Repair a Silver Bullet for Code Generation?
  In *ICLR*, 2024.
- OpenAI (2023)

  OpenAI.
  GPT-4 technical report.
  *arXiv:2303.08774*, 2023.
- Ouyang et al. (2022)

  Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul F. Christiano, Jan Leike, and Ryan Lowe.
  Training Language Models to Follow Instructions with Human Feedback.
  In *NeurIPS*, 2022.
- Popović (2015)

  Maja Popović.
  chrF: Character n-Gram F-score for automatic MT evaluation.
  In *WMT 2015*, pp. 392–395, Lisbon, Portugal, 2015. Association for Computational Linguistics.
- Rafailov et al. (2023)

  Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, and Chelsea Finn.
  Direct Preference Optimization: Your Language Model is Secretly a Reward Model.
  In *NeurIPS*, 2023.
- Ridnik et al. (2024)

  Tal Ridnik, Dedy Kredo, and Itamar Friedman.
  Code Generation with AlphaCodium: From Prompt Engineering to Flow Engineering.
  *arXiv:2401.08500 [cs]*, Jan 2024.
- Rozière et al. (2023)

  Baptiste Rozière, Jonas Gehring, Fabian Gloeckle, Sten Sootla, Itai Gat, Xiaoqing Ellen Tan, Yossi Adi, Jingyu Liu, Tal Remez, Jérémy Rapin, Artyom Kozhevnikov, Ivan Evtimov, Joanna Bitton, Manish Bhatt, Cristian Canton Ferrer, Aaron Grattafiori, Wenhan Xiong, Alexandre Défossez, Jade Copet, Faisal Azhar, Hugo Touvron, Louis Martin, Nicolas Usunier, Thomas Scialom, and Gabriel Synnaeve.
  Code Llama: Open Foundation Models for Code.
  *arXiv:2308.12950 [cs]*, Aug 2023.
- Schick et al. (2023)

  Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom.
  Toolformer: Language Models Can Teach Themselves to Use Tools.
  In *NeurIPS*, 2023.
- Schulman et al. (2017)

  John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov.
  Proximal Policy Optimization Algorithms.
  *arXiv:1707.06347 [cs]*, Aug 2017.
- Shavit et al. (2023)

  Yonadav Shavit, Cullen O’Keefe, Tyna Eloundou, Paul McMillan, Sandhini Agarwal, Miles Brundage, Steven Adler, Rosie Campbell, Teddy Lee, Pamela Mishkin, Alan Hickey, Katarina Slama, Lama Ahmad, Alex Beutel, Alexandre Passos, and David G Robinson.
  Practices for Governing Agentic AI Systems.
  2023.
- Shinn et al. (2023)

  Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao.
  Reflexion: Language Agents with Verbal Reinforcement Learning.
  In *NeurIPS*, 2023.
- Shojaee et al. (2023)

  Parshin Shojaee, Aneesh Jain, Sindhu Tipirneni, and Chandan K. Reddy.
  Execution-based Code Generation using Deep Reinforcement Learning.
  *TMLR*, 07/2023, 2023.
- Sutton & Barto (2018)

  Richard S. Sutton and Andrew G. Barto.
  *Reinforcement Learning: An Introduction*.
  Adaptive Computation and Machine Learning Series. The MIT Press, Cambridge, Massachusetts, second edition edition, 2018.
  ISBN 978-0-262-03924-6.
- Touvron et al. (2023)

  Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, Dan Bikel, Lukas Blecher, Cristian Canton-Ferrer, Moya Chen, Guillem Cucurull, David Esiobu, Jude Fernandes, Jeremy Fu, Wenyin Fu, Brian Fuller, Cynthia Gao, Vedanuj Goswami, Naman Goyal, Anthony Hartshorn, Saghar Hosseini, Rui Hou, Hakan Inan, Marcin Kardas, Viktor Kerkez, Madian Khabsa, Isabel Kloumann, Artem Korenev, Punit Singh Koura, Marie-Anne Lachaux, Thibaut Lavril, Jenya Lee, Diana Liskovich, Yinghai Lu, Yuning Mao, Xavier Martinet, Todor Mihaylov, Pushkar Mishra, Igor Molybog, Yixin Nie, Andrew Poulton, Jeremy Reizenstein, Rashi Rungta, Kalyan Saladi, Alan Schelten, Ruan Silva, Eric Michael Smith, Ranjan Subramanian, Xiaoqing Ellen Tan, Binh Tang, Ross Taylor, Adina Williams, Jian Xiang Kuan, Puxin Xu, Zheng Yan, Iliyan Zarov, Yuchen Zhang, Angela Fan, Melanie Kambadur, Sharan Narang, Aurélien Rodriguez, Robert Stojnic, Sergey Edunov, and Thomas Scialom.
  Llama 2: Open foundation and fine-tuned chat models.
  *arXiv:2307.09288*, 2023.
- Watson et al. (2020)

  Cody Watson, Michele Tufano, Kevin Moran, Gabriele Bavota, and Denys Poshyvanyk.
  On Learning Meaningful Assert Statements for Unit Test Cases.
  In *ICSE*, pp. 1398–1409, 2020.
- Xia et al. (2024)

  Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, and Lingming Zhang.
  Agentless: Demystifying LLM-based Software Engineering Agents.
  *arXiv:2407.01489 [cs]*, Jul 2024.
- Xu et al. (2024)

  Shusheng Xu, Wei Fu, Jiaxuan Gao, Wenjie Ye, Weilin Liu, Zhiyu Mei, Guangju Wang, Chao Yu, and Yi Wu.
  Is DPO Superior to PPO for LLM Alignment? A Comprehensive Study.
  In *ICML*, 2024.
- Yang et al. (2024)

  John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, and Ofir Press.
  SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering.
  *arXiv:2405.15793 [cs]*, May 2024.
- Yao et al. (2022)

  Shunyu Yao, Howard Chen, John Yang, and Karthik Narasimhan.
  WebShop: Towards Scalable Real-World Web Interaction with Grounded Language Agents.
  In *NeurIPS*, 2022.
- Yu et al. (2024)

  Zishun Yu, Yunzhe Tao, Liyu Chen, Tao Sun, and Hongxia Yang.
  ℬ\mathcal{B}-Coder: Value-Based Deep Reinforcement Learning for Program Synthesis.
  *arXiv:2310.03173*, Mar 2024.
- Zhai et al. (2024)

  Yuexiang Zhai, Hao Bai, Zipeng Lin, Jiayi Pan, Shengbang Tong, Yifei Zhou, Alane Suhr, Saining Xie, Yann LeCun, Yi Ma, and Sergey Levine.
  Fine-Tuning Large Vision-Language Models as Decision-Making Agents via Reinforcement Learning.
  *arXiv:2405.10292 [cs]*, May 2024.
- Zhong et al. (2024)

  Li Zhong, Zilong Wang, and Jingbo Shang.
  Debug like a Human: A Large Language Model Debugger via Verifying Runtime Execution Step-by-step.
  *arXiv:2402.16906 [cs]*, Jun 2024.
- Zhou et al. (2024)

  Yifei Zhou, Andrea Zanette, Jiayi Pan, Sergey Levine, and Aviral Kumar.
  ArCHer: Training Language Model Agents via Hierarchical Multi-Turn RL.
  In *ICLR 2024 Workshop on Large Language Model (LLM) Agents*, 2024.
- Ziegler et al. (2020)

  Daniel M. Ziegler, Nisan Stiennon, Jeffrey Wu, Tom B. Brown, Alec Radford, Dario Amodei, Paul Christiano, and Geoffrey Irving.
  Fine-Tuning Language Models from Human Preferences.
  *arXiv:1909.08593 [cs, stat]*, Jan 2020.

## 附录 A 实验细节

### A.1 RLEF

我们按各实验所述，从预训练与指令微调的 LLM 初始化相互独立的策略与价值函数网络；对价值函数，我们用一个随机初始化的线性投影替换输出层。对 PPO，我们使用 AdamW（Loshchilov & Hutter, 2019），学习率 $2\times 10^{-7}$，权重衰减 0.1，并在 50 步上做线性 warm-up。我们把奖励项的 KL 正则化因子 $\beta$ 设为 0.05（2.2 节）。所有模型用解耦推理与优化的在线异步训练基础设施训练。我们在 PPO 的裁剪替代目标（Schulman et al., 2017，式 7）中纳入重要性采样：

$$r_{t}(\theta)=\frac{\pi_{\theta}(a_{t}|c_{t})}{\pi_{\theta_{\text{old}}}(a_{t}|c_{t})}\operatorname{stop\_grad}\left(\min\left(\frac{\pi_{\theta}(a_{t}|c_{t})}{\pi_{\text{b}}(a_{t}|c_{t})},1\right)\right)$$

$$L^{\pi}(\theta)=\mathbb{\hat{E}}_{t}\left[\min\left(r_{t}(\theta)\hat{A}_{t},\operatorname{clip}\left(r_{t}(\theta),1-\epsilon,1+\epsilon\right)\hat{A}_{t}\right)\right]$$

其中 $\theta$ 为模型参数，$\hat{A}_{t}$ 为归一化优势，$\pi_{\text{b}}$ 为行为策略。我们设 $\epsilon=0.2$。

对价值函数的优化，我们使用裁剪价值损失。记价值模型参数为 $\psi$、奖励函数为 $R(s_t,a_t)$（见 2.2 节），有

$$R_{t}=\sum_{i=t}^{T}\gamma^{i-t}R(s_{i},a_{i})$$

$$L^{V}(\psi)=\mathbb{\hat{E}}_{t}\left[\frac{1}{2}\max\left(\left(V_{\psi}(c_{t})-R_{t}\right)^{2},\left(\operatorname{clip}\left(V_{\psi}(c_{t}),V_{\psi_{\text{old}}}(c_{t})}-\alpha,V_{\psi_{\text{old}}}(c_{t})+\alpha\right)-R_{t}\right)^{2}\right)\right]$$

其中折扣因子 $\gamma$ 设为 1，价值裁剪阈值 $\alpha$ 设为 0.2。

训练期间，我们以温度 1.0 推理；既不使用核采样（top-p）也不使用 top-k 采样。我们收集 1024 个 rollout，并对每批 256 个序列各做 4 次更新。每 800 次更新评估一次模型，并依据验证集表现选择最终模型。我们在 NVidia H100 GPU 上训练模型；一次训练约需 20 小时墙钟时间。采用上述参数，8B 与 70B 模型分别使用 288 块（128 块训练、160 块推理）与 2304 块（1024 块训练、1280 块推理）GPU。

### A.2 代码执行

我们用 Li et al. (2022) 的配套代码库³、以 Python 3.10 评估候选解。验证集与测试集中的所有题目都规定了内存限制，仅少数题目规定了时间限制。若已规定，我们在 RLEF 训练与评估中采用这些限制；否则我们对每个测试用例使用 1GB 内存限制与 10 秒最大墙钟时间。

注 3：<https://github.com/google-deepmind/code_contests>。

### A.3 有监督微调

我们为 3.4.1 节的消融执行有监督微调（SFT）。为组装训练数据集，我们在 CodeContests 训练集上用 Llama 3.1 70B Instruct 模型、按我们提出的设定做迭代式代码生成。我们把 top-p 设为 0.95，并为每个回复从 $\text{U}(0.1,1.0)$ 中采样温度。对训练集每道题收集 100 个多轮 rollout，得到 313,639 条成功轨迹。

我们对模型做下一 token 预测微调，只在最后一个回复（即同时通过公共与私有测试的回复）上计算损失；这比在全部回复上训练得到略好的模型。我们在学习率 $5\times 10^{-6}$ 与 $2\times 10^{-6}$、2 与 3 个 epoch 之间扫描，batch size 64、序列长度 8192。前 10 步做线性 warm-up，学习率按余弦日程退火。权重衰减设为 0.1。以 AdamW 每 200 个优化器步评估一次模型，并依据验证集表现选择最终参数。

## 附录 B 补充实验结果

### B.1 预训练模型

表 4(a) 列出从预训练 Llama 3.1 模型出发做少样本提示与有监督微调的求解率。我们观察到，在所有情形下其表现显著低于 Instruct 模型（表 3(a)）。

| 模型 | 方法 | 验证集 | 测试集 |
| --- | --- | --- | --- |
| 8B Base | Few-Shot | 1.2 | 1.8 |
|  | SFT | 6.9 | 3.5 |
| 70B Base | Few-Shot | 4.6 | 5.8 |
|  | SFT | 11.1 | 10.9 |

(a)

|  |  |  |
| --- | --- | --- |
| 方法（8B） | 验证集 | 测试集 |
| RLEF | 17.2 | 16.0 |
| 无执行反馈 | 12.2 | 10.9 |
| token 级价值函数 | 13.1 | 13.7 |
| 单轮 RL | 10.2 | 10.9 |
| 单轮 + 修复 | 14.8 | 12.6 |

(b)

表 4：(a) Llama 3.1 Base 模型在 CodeContests 上少样本提示与有监督微调（SFT）的 1@3 求解率。(b) Llama 3.1 Instruct 8B 的更多结果（1@3）：RL 期间不提供公共测试执行反馈；在 token 级学习价值函数；训练专用代码修复模型并应用于单轮 RL 模型的输出。

### B.2 来自私有测试的反馈

我们在 CodeContests 上的主评估与训练设定一致，即推理时提供公共测试用例的反馈，并在私有（及数据集生成的）测试上估计求解率。CodeContests 验证集与测试集的公共测试用例数在 1-7 之间，中位数为 1；通常每题有更多私有测试和大量生成测试。

我们验证 RLEF 训练的模型能否在推理时通过纳入私有与生成测试的反馈从更大测试集中获益。具体地，我们把每个模型回复对 20 个可用测试用例（含私有测试）测试，并就最多 8 个失败用例提供执行反馈。在轮数上限 3、温度 0.2 下比较 1@3 求解率：8B RLEF 模型在验证集上可从 17.2 提升到 18.1，测试集上则从 16.0 降到 14.4。70B RLEF 模型在验证集上从 37.5 提升到 40.4，测试集上相对仅公共测试反馈的 38.0 取得 41.2。

### B.3 额外修复模型

Le et al. (2022) 在 RL 训练的 LLM 之上用两个额外模型实现程序修复：一个「critic」预测全部单元测试的联合结果（如成功、失败、运行时错误），可用于排序与确定有希望的前缀；一个「repair」模型把错误解映射为真值解。本着这一精神，我们如下评估一个专用修复模型对 3.4.2 节单轮 8B 模型的改进效果。

在 RL 训练过程中，我们收集所有未通过公共单元测试的生成。在 12,000 个梯度步的训练时长内，这相当于 148 万个样本。接着我们构造训练对话：原始提示（如 C.1 节所述）、错误生成，以及 CodeContest 训练集中该题的一个随机正确生成。我们对 CodeContest 解做额外处理，确保它们确实通过所给单元测试并统一缩进。然后我们通过有监督微调 Llama 3.1 8B Instruct 训练修复模型，在学习率 $5\times 10^{-6}$、$2\times 10^{-6}$、$1\times 10^{-6}$ 与 1 或 2 个 epoch 之间扫描，batch size 64、序列长度 8192。

评估时，我们用 RL 训练的模型生成初始程序，再由修复模型给出最多两个独立样本，以此估计 1@3 求解率。与主 RLEF 设定类似，若最新解通过公共测试则（进一步）修复止步。我们每 400 个梯度步评估扫描中的全部模型，并依据验证集表现选择最佳检查点。该检查点与单轮 RL 模型组合，在验证集与测试集上分别取得 1@3 求解率 14.8 与 12.6，较单轮 RL 模型单独（分别为 10.2 与 10.9）有显著提升，但仍不及结合代码合成与代码修复的对应 RLEF 训练模型（分别为 17.2 与 16.0）。

### B.4 无公共测试执行反馈的 RL 训练

我们用一个不提供公共测试信息的消融，验证「内联执行反馈 + 基于公共测试的提前停止」这一设定（2.1 节）。具体地，我们从后续解的提示中移除执行反馈（C.1 节），直接以 "Give it another try" 开始。我们总是以这种方式向模型请求两个后续解（即总共三个解）。我们保留 2.2 节的奖励定义，但公共测试通过时不结束回合。

由此得到的模型（从 Llama 3.1 8B Instruct 出发）在验证集与测试集上分别取得 1@3 求解率 12.2 与 10.9（表 4(b)）。这优于初始 Instruct 模型（分别为 8.9 与 10.2），但显著低于对应的 RLEF 训练模型（分别为 17.2 与 16.0）。

### B.5 token 级价值函数

这里我们不按回复层级训练价值函数（2.2 节、A.1 节），而是为回复的每个 token 预测一个价值。我们的奖励形式不变；因而由于折扣因子设为 1，回复内每个 token 的价值函数目标（reward-to-go）相同。但我们现在为每个 token 分别计算优势。

采用这一方法且其余设定相同，从 Llama 3.1 8B Instruct 出发，我们在验证集与测试集上分别取得 1@3 求解率 13.1 与 13.7（表 4(b)）。这低于轮级价值函数的 17.2 与 16.0（表 1）。

## 附录 C 提示词

### C.1 CodeContests

在初始提示中，我们把 ${problem} 原样替换为原始问题描述。
[⬇](data:text/plain;base64,UHJvdmlkZSBhIFB5dGhvbiBzb2x1dGlvbiBmb3IgdGhlIGZvbGxvd2luZyBjb21wZXRpdGl2ZSBwcm9ncmFtbWluZyBxdWVzdGlvbjogXCR7cHJvYmxlbX0uCgpZb3VyIGNvZGUgc2hvdWxkIGJlIGVuY2xvc2VkIGluIHRyaXBsZSBiYWNrdGlja3MgbGlrZSBzbzogYGBgcHl0aG9uIFlPVVIgQ09ERSBIRVJFIGBgYC4gVXNlIHRoZSBiYWNrdGlja3MgZm9yIHlvdXIgY29kZSBvbmx5Lg==)

Provide a Python solution for the following competitive programming question: \${problem}.

Your code should be enclosed in triple backticks like so: “‘python YOUR CODE HERE “‘. Use the backticks for your code only.

在下面的执行反馈提示中，我们展示所考虑四种错误类型的模板：答案错误、异常、超时与内存不足。其后展示各失败测试的相应反馈。

[⬇](data:text/plain;base64,WW91ciBjb2RlIGZhaWxlZCB0aGUgZm9sbG93aW5nIHRlc3RzOgoKLSBpbnB1dCBgJHtpbnB1dH1gIGZhaWxlZDoKRXhwZWN0ZWQgb3V0cHV0IGAke2V4cGVjdGVkX291dHB1dH1gIGJ1dCBnb3QgYCR7b2JzZXJ2ZWRfb3V0cHV0fWAKLSBpbnB1dCBgJHtpbnB1dH1gIGZhaWxlZDoKJHtzdGFja3RyYWNlfQotIGlucHV0IGAke2lucHV0fWAgZmFpbGVkOiBFeGVjdXRpb24gdG9vayB0b28gbG9uZy4KLSBpbnB1dCBgJHtpbnB1dH1gIGZhaWxlZDogT3V0IG9mIG1lbW9yeS4KCkdpdmUgaXQgYW5vdGhlciB0cnkuCllvdXIgY29kZSBzaG91bGQgYmUgZW5jbG9zZWQgaW4gdHJpcGxlIGJhY2t0aWNrcyBsaWtlIHNvOiBgYGBweXRob24gWU9VUiBDT0RFIEhFUkUgYGBgLiBVc2UgdGhlIGJhY2t0aWNrcyBmb3IgeW91ciBjb2RlIG9ubHku)

Your code failed the following tests:

- input ‘${input}‘ failed:

Expected output ‘${expected_output}‘ but got ‘${observed_output}‘

- input ‘${input}‘ failed:

${stacktrace}

- input ‘${input}‘ failed: Execution took too long.

- input ‘${input}‘ failed: Out of memory.

Give it another try.

Your code should be enclosed in triple backticks like so: “‘python YOUR CODE HERE “‘. Use the backticks for your code only.

### C.2 随机反馈消融

3.3 节中我们用随机执行反馈测试 RLEF 训练的模型。对每道题，我们从相应测试集中采样一道含错误解的另一题目。我们随机选取其中一个错误解、对相应公共测试执行以获得无关反馈，并把所得反馈呈现给模型。若没有错误解在公共测试上失败，我们执行 raise NotImplementedError()。此时反馈将包含指向该错误回溯。其余对话照常进行：若 LLM 产生的代码解通过了该题的真实公共测试，我们即停止并在全部测试用例上评估该解。

### C.3 少样本提示

对 3.4 节的少样本消融，我们从 Llama 3.1 70B Instruct 模型在 CodeContests 训练集题目上的成功轨迹中选取。我们选取有 2 次与 3 次成功尝试的轨迹，作为成功多轮代码生成的示范。对指令模型，我们以少样本示例初始化对话，用空的 assistant 消息分隔。对预训练模型的少样本实验（B.1 节），我们使用每条消息以 [USER] 或 [ASSISTANT] 为前缀的对话格式。||（一个在 Python 中非法的符号）的 token 用作消息分隔符。

### C.4 HumanEval+

HumanEval 的题目提示由起始代码组成，函数声明后跟 docstring 与示例测试。

[⬇](data:text/plain;base64,V3JpdGUgYSBzb2x1dGlvbiB0byB0aGUgZm9sbG93aW5nIHByb2JsZW0gYW5kIG1ha2Ugc3VyZSB0aGF0IGl0IHBhc3NlcyB0aGUgdGVzdHM6CiR7cHJvYmxlbX0=)

Write a solution to the following problem and make sure that it passes the tests:

${problem}

随后我们在每个模型回复的开头再次提供题目提示以供补全。

HumanEval+ 中的测试由单个含若干 assert 语句的函数组成。为获得单个测试的执行反馈，我们从原始测试函数中抽取它们（计算通过率时使用原始测试代码）。我们进一步把 assert 语句转换为 Python 内建 unittest.TestCase 类的匹配函数调用。这样，测试失败会产生带运行时值的、信息更丰富的 AssertionError 异常；它们以 assertion_error 提供给模板。我们也展示成功的测试用例。

[⬇](data:text/plain;base64,WW91ciBjb2RlIGZhaWxlZCBzb21lIHRlc3QgY2FzZXM6CgotIEZhaWx1cmU6IGAke3Rlc3R9YDoKYCR7YXNzZXJ0aW9uX2Vycm9yfWAKLSBGYWlsdXJlOiBgJHt0ZXN0fWA6CiR7c3RhY2t0cmFjZX0KLSBGYWlsdXJlOiBgJHt0ZXN0fWA6CkV4ZWN1dGlvbiB0b29rIHRvbyBsb25nLgotIFN1Y2Nlc3M6IGAke3Rlc3R9YAoKR2l2ZSBpdCBhbm90aGVyIHRyeS4=)

Your code failed some test cases:

- Failure: ‘${test}‘:

‘${assertion_error}‘

- Failure: ‘${test}‘:

${stacktrace}

- Failure: ‘${test}‘:

Execution took too long.

- Success: ‘${test}‘

Give it another try.

### C.5 MBPP+

每个 MBPP 提示由问题描述与单个示例测试组成。

[⬇](data:text/plain;base64,UHJvdmlkZSBhIFB5dGhvbiBzb2x1dGlvbiBmb3IgdGhlIGZvbGxvd2luZyBwcm9ibGVtOiAke3Byb2JsZW19CllvdXIgY29kZSBzaG91bGQgcGFzcyB0aGVzZSB0ZXN0czoKCiR7dGVzdH0KCllvdXIgY29kZSBzaG91bGQgYmUgZW5jbG9zZWQgaW4gdHJpcGxlIGJhY2t0aWNrcyBsaWtlIHNvOiBgYGBweXRob24gWU9VUiBDT0RFIEhFUkUgYGBgLiBVc2UgdGhlIGJhY2t0aWNrcyBmb3IgeW91ciBjb2RlIG9ubHku)

Provide a Python solution for the following problem: ${problem}

Your code should pass these tests:

${test}

Your code should be enclosed in triple backticks like so: “‘python YOUR CODE HERE “‘. Use the backticks for your code only.

执行反馈沿用 C.4 节的 HumanEval+ 格式，并有额外的格式化准则。

[⬇](data:text/plain;base64,WW91ciBjb2RlIGZhaWxlZCBzb21lIHRlc3QgY2FzZXM6CgotIEZhaWx1cmU6IGAke3Rlc3R9YDoKYCR7ZXJyb3J9YAotIEZhaWx1cmU6IGAke3Rlc3R9YDoKJHtzdGFja3RyYWNlfQotIEZhaWx1cmU6IGAke3Rlc3R9YDoKRXhlY3V0aW9uIHRvb2sgdG9vIGxvbmcuCi0gU3VjY2VzczogYCR7dGVzdH1gCgpHaXZlIGl0IGFub3RoZXIgdHJ5LgpZb3VyIGNvZGUgc2hvdWxkIGJlIGVuY2xvc2VkIGluIHRyaXBsZSBiYWNrdGlja3MgbGlrZSBzbzogYGBgcHl0aG9uIFlPVVIgQ09ERSBIRVJFIGBgYC4gVXNlIHRoZSBiYWNrdGlja3MgZm9yIHlvdXIgY29kZSBvbmx5Lg==)

Your code failed some test cases:

- Failure: ‘${test}‘:

‘${error}‘

- Failure: ‘${test}‘:

${stacktrace}

- Failure: ‘${test}‘:

Execution took too long.

- Success: ‘${test}‘

Give it another try.

Your code should be enclosed in triple backticks like so: “‘python YOUR CODE HERE “‘. Use the backticks for your code only.

## 附录 D 示例

以下示例选自 CodeContests 验证集，由 RLEF 训练的 70B 模型生成，温度 0.2、top-p 0.95。为便于阅读，我们对初始提示做了轻度重排版。

在第一个示例中，第一个模型回复方向正确，但第一条 print() 语句输出了错误值。第二个回复朴素地实现了所要求的算法，但由于从 ll 到 rr 的循环而效率低下；对公共测试的最后一行约需两分钟。最终，第三个回复的代码既正确又快速。

[⬇](data:text/plain;base64,UHJvdmlkZSBhIFB5dGhvbiBzb2x1dGlvbiBmb3IgdGhlIGZvbGxvd2luZyBjb21wZXRpdGl2ZSBwcm9ncmFtbWluZyBxdWVzdGlvbjogWW91IGFyZSBnaXZlbiB0d28gaW50ZWdlcnMgbCBhbmQgciwgbCDiiaQgci4gRmluZCB0aGUgbGFyZ2VzdCBwb3NzaWJsZSB2YWx1ZSBvZiBhIG1vZCBiIG92ZXIgYWxsIHBhaXJzIChhLCBiKSBvZiBpbnRlZ2VycyBmb3Igd2hpY2ggciDiiaUgYSDiiaUgYiDiiaUgbC4KQXMgYSByZW1pbmRlciwgYSBtb2QgYiBpcyBhIHJlbWFpbmRlciB3ZSBnZXQgd2hlbiBkaXZpZGluZyBhIGJ5IGIuIEZvciBleGFtcGxlLCAyNiBtb2QgOCA9IDIuCgpJbnB1dAoKRWFjaCB0ZXN0IGNvbnRhaW5zIG11bHRpcGxlIHRlc3QgY2FzZXMuClRoZSBmaXJzdCBsaW5lIGNvbnRhaW5zIG9uZSBwb3NpdGl2ZSBpbnRlZ2VyIHQgKDEg4omkIHQg4omkIDEwXjQpLCBkZW5vdGluZyB0aGUgbnVtYmVyIG9mIHRlc3QgY2FzZXMuIERlc2NyaXB0aW9uIG9mIHRoZSB0ZXN0IGNhc2VzIGZvbGxvd3MuClRoZSBvbmx5IGxpbmUgb2YgZWFjaCB0ZXN0IGNhc2UgY29udGFpbnMgdHdvIGludGVnZXJzIGwsIHIgKDEg4omkIGwg4omkIHIg4omkIDEwXjkpLgoKT3V0cHV0CgpGb3IgZXZlcnkgdGVzdCBjYXNlLCBvdXRwdXQgdGhlIGxhcmdlc3QgcG9zc2libGUgdmFsdWUgb2YgYSBtb2QgYiBvdmVyIGFsbCBwYWlycyAoYSwgYikgb2YgaW50ZWdlcnMgZm9yIHdoaWNoIHIg4omlIGEg4omlIGIg4omlIGwuCgpFeGFtcGxlCgpJbnB1dAoKNAoxIDEKOTk5OTk5OTk5IDEwMDAwMDAwMDAKOCAyNgoxIDk5OTk5OTk5OQoKT3V0cHV0CgowCjEKMTIKNDk5OTk5OTk5CgpOb3RlCgpJbiB0aGUgZmlyc3QgdGVzdCBjYXNlLCB0aGUgb25seSBhbGxvd2VkIHBhaXIgaXMgKGEsIGIpID0gKDEsIDEpLCBmb3Igd2hpY2ggYSBtb2QgYiA9IDEgbW9kIDEgPSAwLgpJbiB0aGUgc2Vjb25kIHRlc3QgY2FzZSwgdGhlIG9wdGltYWwgY2hvaWNlIGlzIHBhaXIgKGEsIGIpID0gKDEwMDAwMDAwMDAsIDk5OTk5OTk5OSksIGZvciB3aGljaCBhIG1vZCBiID0gMS4uCllvdXIgY29kZSBzaG91bGQgYmUgZW5jbG9zZWQgaW4gdHJpcGxlIGJhY2t0aWNrcyBsaWtlIHNvOiBgYGBweXRob24gWU9VUiBDT0RFIEhFUkUgYGBgLiBVc2UgdGhlIGJhY2t0aWNrcyBmb3IgeW91ciBjb2RlIG9ubHku)

Provide a Python solution for the following competitive programming question: You are given two integers l and r, l ≤ r. Find the largest possible value of a mod b over all pairs (a, b) of integers for which r ≥ a ≥ b ≥ l.

As a reminder, a mod b is a remainder we get when dividing a by b. For example, 26 mod 8 = 2.

Input

Each test contains multiple test cases.

The first line contains one positive integer t (1 ≤ t ≤ 10^4), denoting the number of test cases. Description of the test cases follows.

The only line of each test case contains two integers l, r (1 ≤ l ≤ r ≤ 10^9).

Output

For every test case, output the largest possible value of a mod b over all pairs (a, b) of integers for which r ≥ a ≥ b ≥ l.

Example

Input

4

1 1

999999999 1000000000

8 26

1 999999999

Output

0

1

12

499999999

Note

In the first test case, the only allowed pair is (a, b) = (1, 1), for which a mod b = 1 mod 1 = 0.

In the second test case, the optimal choice is pair (a, b) = (1000000000, 999999999), for which a mod b = 1..

Your code should be enclosed in triple backticks like so: “‘python YOUR CODE HERE “‘. Use the backticks for your code only.

[⬇](data:text/plain;base64,YGBgcHl0aG9uCnQgPSBpbnQoaW5wdXQoKSkKCmZvciBfIGluIHJhbmdlKHQpOgogICAgbCwgciA9IG1hcChpbnQsIGlucHV0KCkuc3BsaXQoKSkKCiAgICBpZiByIC8vIDIgKyAxID49IGw6CiAgICAgICAgcHJpbnQoKHIgLy8gMikpCiAgICBlbHNlOgogICAgICAgIHByaW50KHIgJSBsKQpgYGA=)

“‘python

t = int(input())

for _ in range(t):

l, r = map(int, input().split())

if r // 2 + 1 >= l:

print((r // 2))

else:

print(r % l)

“‘

[⬇](data:text/plain;base64,WW91ciBjb2RlIGZhaWxlZCB0aGUgZm9sbG93aW5nIHRlc3RzOgoKLSBpbnB1dCBgNAoxIDEKOTk5OTk5OTk5IDEwMDAwMDAwMDAKOCAyNgoxIDk5OTk5OTk5OQpgIGZhaWxlZDoKRXhwZWN0ZWQgb3V0cHV0IGAwCjEKMTIKNDk5OTk5OTk5CmAgYnV0IGdvdCBgMAoxCjEzCjQ5OTk5OTk5OQpgCgpHaXZlIGl0IGFub3RoZXIgdHJ5LgpZb3VyIGNvZGUgc2hvdWxkIGJlIGVuY2xvc2VkIGluIHRyaXBsZSBiYWNrdGlja3MgbGlrZSBzbzogYGBgcHl0aG9uIFlPVVIgQ09ERSBIRVJFIGBgYC4gVXNlIHRoZSBiYWNrdGlja3MgZm9yIHlvdXIgY29kZSBvbmx5Lg==)

Your code failed the following tests:

- input ‘4

1 1

999999999 1000000000

8 26

1 999999999

‘ failed:

Expected output ‘0

1

12

499999999

‘ but got ‘0

1

13

499999999

‘

Give it another try.

Your code should be enclosed in triple backticks like so: “‘python YOUR CODE HERE “‘. Use the backticks for your code only.

[⬇](data:text/plain;base64,YGBgcHl0aG9uCnQgPSBpbnQoaW5wdXQoKSkKCmZvciBfIGluIHJhbmdlKHQpOgogICAgbCwgciA9IG1hcChpbnQsIGlucHV0KCkuc3BsaXQoKSkKCiAgICBtYXhfbW9kID0gMAogICAgZm9yIGIgaW4gcmFuZ2UobCwgciArIDEpOgogICAgICAgIGEgPSByCiAgICAgICAgbW9kID0gYSAlIGIKICAgICAgICBtYXhfbW9kID0gbWF4KG1heF9tb2QsIG1vZCkKCiAgICBwcmludChtYXhfbW9kKQpgYGA=)

“‘python

t = int(input())

for _ in range(t):

l, r = map(int, input().split())

max_mod = 0

for b in range(l, r + 1):

a = r

mod = a % b

max_mod = max(max_mod, mod)

print(max_mod)

“‘

[⬇](data:text/plain;base64,WW91ciBjb2RlIGZhaWxlZCB0aGUgZm9sbG93aW5nIHRlc3RzOgoKLSBpbnB1dCBgNAoxIDEKOTk5OTk5OTk5IDEwMDAwMDAwMDAKOCAyNgoxIDk5OTk5OTk5OQpgIGZhaWxlZDoKRXhlY3V0aW9uIHRvb2sgdG9vIGxvbmcKCkdpdmUgaXQgYW5vdGhlciB0cnkuCllvdXIgY29kZSBzaG91bGQgYmUgZW5jbG9zZWQgaW4gdHJpcGxlIGJhY2t0aWNrcyBsaWtlIHNvOiBgYGBweXRob24gWU9VUiBDT0RFIEhFUkUgYGBgLiBVc2UgdGhlIGJhY2t0aWNrcyBmb3IgeW91ciBjb2RlIG9ubHku)

Your code failed the following tests:

- input ‘4

1 1

999999999 1000000000

8 26

1 999999999

‘ failed:

Execution took too long

Give it another try.

Your code should be enclosed in triple backticks like so: “‘python YOUR CODE HERE “‘. Use the backticks for your code only.

[⬇](data:text/plain;base64,YGBgcHl0aG9uCnQgPSBpbnQoaW5wdXQoKSkKCmZvciBfIGluIHJhbmdlKHQpOgogICAgbCwgciA9IG1hcChpbnQsIGlucHV0KCkuc3BsaXQoKSkKCiAgICBpZiByID09IGw6CiAgICAgICAgcHJpbnQoMCkKICAgIGVsc2U6CiAgICAgICAgYiA9IChyIC8vIDIpICsgMQogICAgICAgIGlmIGIgPj0gbDoKICAgICAgICAgICAgcHJpbnQociAlIChiKSkKICAgICAgICBlbHNlOgogICAgICAgICAgICBwcmludChyICUgbCkKYGBg)

“‘python

t = int(input())

for _ in range(t):

l, r = map(int, input().split())

if r == l:

print(0)

else:

b = (r // 2) + 1

if b >= l:

print(r % (b))

else:

print(r % l)

“‘

[⬇](data:text/plain;base64,UGFzc2VzIHB1YmxpYyBhbmQgcHJpdmF0ZSB0ZXN0cy4=)

Passes public and private tests.

在第二个示例中，第一个代码解没有重置 pkp_{k} 的值。第二个正确的尝试修复了这一点。注意两个解都含未使用的变量：第一个回复中的 curr 与第二个回复中的 curr_a。对这道题，从 pk−1p_{k-1} 出发初始化 pkp_{k} 的动态规划做法更可取；不过第二个解也通过了全部测试用例。

[⬇](data:text/plain;base64,UHJvdmlkZSBhIFB5dGhvbiBzb2x1dGlvbiBmb3IgdGhlIGZvbGxvd2luZyBjb21wZXRpdGl2ZSBwcm9ncmFtbWluZyBxdWVzdGlvbjogWW91IGhhdmUgYW4gYXJyYXkgYSBjb25zaXN0aW5nIG9mIG4gZGlzdGluY3QgcG9zaXRpdmUgaW50ZWdlcnMsIG51bWJlcmVkIGZyb20gMSB0byBuLiBEZWZpbmUgcF9rIGFzICQkJHBfayA9IOKIkV97MSDiiaQgaSwgaiDiiaQga30gYV9pIG1vZCBhX2osIHdoZXJlIHggXGJtb2QgeSBkZW5vdGVzIHRoZSByZW1haW5kZXIgd2hlbiB4IGlzIGRpdmlkZWQgYnkgeS4gWW91IGhhdmUgdG8gZmluZCBhbmQgcHJpbnQgcF8xLCBwXzIsIFxsZG90cywgcF9uJCQkLgoKSW5wdXQKClRoZSBmaXJzdCBsaW5lIGNvbnRhaW5zIG4gLSB0aGUgbGVuZ3RoIG9mIHRoZSBhcnJheSAoMiDiiaQgbiDiiaQgMiDii4UgMTBeNSkuClRoZSBzZWNvbmQgbGluZSBjb250YWlucyBuIHNwYWNlLXNlcGFyYXRlZCBkaXN0aW5jdCBpbnRlZ2VycyBhXzEsIC4uLiwgYV9uICgxIOKJpCBhX2kg4omkIDMg4ouFIDEwXjUsIGFfaSDiiaAgYV9qIGlmIGkg4omgIGopLgoKT3V0cHV0CgpQcmludCBuIGludGVnZXJzIHBfMSwgcF8yLCAuLi4sIHBfbi4KCkV4YW1wbGVzCgpJbnB1dAoKNAo2IDIgNyAzCgpPdXRwdXQKCjAgMiAxMiAyMgoKSW5wdXQKCjMKMyAyIDEKCk91dHB1dAoKMCAzIDUuCllvdXIgY29kZSBzaG91bGQgYmUgZW5jbG9zZWQgaW4gdHJpcGxlIGJhY2t0aWNrcyBsaWtlIHNvOiBgYGBweXRob24gWU9VUiBDT0RFIEhFUkUgYGBgLiBVc2UgdGhlIGJhY2t0aWNrcyBmb3IgeW91ciBjb2RlIG9ubHku)

Provide a Python solution for the following competitive programming question: You have an array a consisting of n distinct positive integers, numbered from 1 to n. Define p_k as $$$p_k = ∑_{1 ≤ i, j ≤ k} a_i mod a_j, where x \bmod y denotes the remainder when x is divided by y. You have to find and print p_1, p_2, \ldots, p_n$$$.

Input

The first line contains n - the length of the array (2 ≤ n ≤ 2 ⋅ 10^5).

The second line contains n space-separated distinct integers a_1, …, a_n (1 ≤ a_i ≤ 3 ⋅ 10^5, a_i ≠ a_j if i ≠ j).

Output

Print n integers p_1, p_2, …, p_n.

Examples

Input

4

6 2 7 3

Output

0 2 12 22

Input

3

3 2 1

Output

0 3 5.

Your code should be enclosed in triple backticks like so: “‘python YOUR CODE HERE “‘. Use the backticks for your code only.

[⬇](data:text/plain;base64,YGBgcHl0aG9uCm4gPSBpbnQoaW5wdXQoKSkKYSA9IGxpc3QobWFwKGludCwgaW5wdXQoKS5zcGxpdCgpKSkKCnAgPSAwCnJlc3VsdCA9IFtdCmZvciBrIGluIHJhbmdlKG4pOgogICAgY3VyciA9IGFba10KICAgIGZvciBpIGluIHJhbmdlKGsgKyAxKToKICAgICAgICBmb3IgaiBpbiByYW5nZShrICsgMSk6CiAgICAgICAgICAgIHAgKz0gYVtpXSAlIGFbal0KICAgIHJlc3VsdC5hcHBlbmQocCkKCmZvciBudW0gaW4gcmVzdWx0OgogICAgcHJpbnQobnVtLCBlbmQ9IiAiKQpgYGA=)

“‘python

n = int(input())

a = list(map(int, input().split()))

p = 0

result = []

for k in range(n):

curr = a[k]

for i in range(k + 1):

for j in range(k + 1):

p += a[i] % a[j]

result.append(p)

for num in result:

print(num, end=” ”)

“‘

[⬇](data:text/plain;base64,WW91ciBjb2RlIGZhaWxlZCB0aGUgZm9sbG93aW5nIHRlc3RzOgoKLSBpbnB1dCBgNAo2IDIgNyAzCmAgZmFpbGVkOgpFeHBlY3RlZCBvdXRwdXQgYDAgMiAxMiAyMgpgIGJ1dCBnb3QgYDAgMiAxNCAzNiBgCi0gaW5wdXQgYDMKMyAyIDEKYCBmYWlsZWQ6CkV4cGVjdGVkIG91dHB1dCBgMCAzIDUKYCBidXQgZ290IGAwIDMgOCBgCgpHaXZlIGl0IGFub3RoZXIgdHJ5LgpZb3VyIGNvZGUgc2hvdWxkIGJlIGVuY2xvc2VkIGluIHRyaXBsZSBiYWNrdGlja3MgbGlrZSBzbzogYGBgcHl0aG9uIFlPVVIgQ09ERSBIRVJFIGBgYC4gVXNlIHRoZSBiYWNrdGlja3MgZm9yIHlvdXIgY29kZSBvbmx5Lg==)

Your code failed the following tests:

- input ‘4

6 2 7 3

‘ failed:

Expected output ‘0 2 12 22

‘ but got ‘0 2 14 36 ‘

- input ‘3

3 2 1

‘ failed:

Expected output ‘0 3 5

‘ but got ‘0 3 8 ‘

Give it another try.

Your code should be enclosed in triple backticks like so: “‘python YOUR CODE HERE “‘. Use the backticks for your code only.

[⬇](data:text/plain;base64,YGBgcHl0aG9uCm4gPSBpbnQoaW5wdXQoKSkKYSA9IGxpc3QobWFwKGludCwgaW5wdXQoKS5zcGxpdCgpKSkKCnJlc3VsdCA9IFtdCnRvdGFsID0gMApmb3IgayBpbiByYW5nZShuKToKICAgIGN1cnJfdG90YWwgPSAwCiAgICBjdXJyX2EgPSBhWzprKzFdCiAgICBmb3IgaSBpbiByYW5nZShrKzEpOgogICAgICAgIGZvciBqIGluIHJhbmdlKGsrMSk6CiAgICAgICAgICAgIGlmIGkgIT0gajoKICAgICAgICAgICAgICAgIGN1cnJfdG90YWwgKz0gYVtpXSAlIGFbal0KICAgIHJlc3VsdC5hcHBlbmQoY3Vycl90b3RhbCkKCmZvciBudW0gaW4gcmVzdWx0OgogICAgcHJpbnQobnVtLCBlbmQ9IiAiKQpgYGA=)

“‘python

n = int(input())

a = list(map(int, input().split()))

result = []

total = 0

for k in range(n):

curr_total = 0

curr_a = a[:k+1]

for i in range(k+1):

for j in range(k+1):

if i != j:

curr_total += a[i] % a[j]

result.append(curr_total)

for num in result:

print(num, end=” ”)

“‘

[⬇](data:text/plain;base64,UGFzc2VzIHB1YmxpYyBhbmQgcHJpdmF0ZSB0ZXN0cy4=)

Passes public and private tests.
