---
title: "Archon：一个推理时技术的架构搜索框架"
title_en: "Archon: An Architecture Search Framework for Inference-Time Techniques"
arxiv: 2409.15254
source: https://arxiv.org/abs/2409.15254
crawled: 2026-09-23
translated: 2026-09-23
---

# Archon：一个推理时技术的架构搜索框架

> 原文：[Archon: An Architecture Search Framework for Inference-Time Techniques](https://arxiv.org/abs/2409.15254) · Stanford CS329A 指定阅读

Jon Saad-Falcon、Adrian Gamarra Lafuente、Shlok Natarajan、Nahum Maru、Hristo Todorov（斯坦福大学，斯坦福，加州，美国）；Etash Guha（华盛顿大学，西雅图，华盛顿州，美国）；E. Kelly Buchanan、Mayee Chen、Neel Guha、Christopher Ré、Azalia Mirhoseini（斯坦福大学，斯坦福，加州，美国）

通讯作者：Jon Saad-Falcon <jonsaadfalcon@stanford.edu>

###### 摘要

重复采样、迭代修订等推理时技术正在成为在测试阶段增强大语言模型（LLM）的强大手段。然而，由于我们对每项技术在不同模型与任务上的效用、它们之间的交互，以及组合它们的庞大搜索空间的理解仍然有限，构建组合这些技术的系统的最佳实践尚不成熟。为应对这些挑战，我们提出 Archon——一个模块化、自动化的框架，用于优化推理时技术与 LLM 的选择和组合过程。给定计算预算与一组可用 LLM，Archon 会探索一个庞大的设计空间，以发现针对目标基准量身定制的优化配置。它可以设计定制的或通用的架构，相对表现最佳的基线推进「准确率 vs. 最大 token 预算」的帕累托前沿。在指令遵循、推理与编程任务上，我们表明 Archon 能利用额外推理计算预算设计出平均超越 OpenAI 的 o1、GPT-4o 与 Claude 3.5 Sonnet 等前沿模型 15.1% 的系统。

## 1 引言

图 1：Archon 的性能随推理预算增加而有效扩展。各数据集的单独分析见图 8。

推理时技术——在模型推理期间使用额外计算的策略——正作为提升模型能力的有效方法获得关注。OpenAI 的 o1（OpenAI, 2024）、QwQ（Qwen Team, 2024）与 Sky-T1（NovaTeam, 2024）等 LLM 利用这类技术把额外推理计算转化为在广泛任务上更好的表现。示例技术包括生成集成、排序与融合：集成中的模型被并行查询，其回答被排序，其中最好的被融合成单个更高质量的输出（Jiang et al., 2023b；Wang et al., 2024a）。其他类型的推理时技术基于连续查询单个 LLM（通过重复采样），并使用投票策略或单元测试来选出最佳生成（Brown et al., 2024；Chen et al., 2024；Li et al., 2024a）。

近期工作在构建稳健的推理时架构——由一个或多个利用推理时技术的大语言模型（LLM）组成的系统——方面取得进展。例子包括 Mixture-of-Agents（MoA）（Wang et al., 2024a）与 LLM-Blender（Jiang et al., 2023b），以及 ADAS（Hu et al., 2024）与 AFlow（Zhang et al., 2024）等单模型系统。然而，我们的实验表明这些表现最好的基线在计算利用与任务泛化上存在局限（见第 4.2 节）。我们主张，设计有效且可泛化的推理时架构需要以下几点：

图 2：Archon 框架概览：Archon 的搜索算法需要以下输入：目标基准、推理调用预算、可用 LLM 与可用推理时技术（左）。搜索算法使用贝叶斯优化（Snoek et al., 2012）来构造并评估不同的 Archon 配置（中），然后为目标基准返回优化后的 Archon 架构（右）（第 3.3 节）。

- 理解推理时技术的效用：推理时架构通常把额外的推理预算分配给更多的模型采样调用（Chen et al., 2024；Brown et al., 2024），这对数学与编程任务可能有效。其他任务（如指令遵循与推理）已被证明可以从排序与融合等额外技术中受益（Wang et al., 2024a；Jiang et al., 2023b）。虽然所有这些方法都有价值，但识别哪些推理时技术对不同任务类别最有效至关重要。
- 理解推理时技术之间的交互：虽然先前研究（如 Chen et al. (2024) 对生成采样的分析）单独分析了这些技术，我们需要对不同任务上不同推理时技术之间关系更全面的理解（例如，使用更多模型还是每个模型生成更多样本更好？）。
- 高效且自动地搜索推理时架构的庞大设计空间：给定一组可用 LLM 与目标任务，目前不存在在所有任务上最大化下游准确率的单一主流推理时架构（表 1）。推理时架构的搜索空间广阔，要求从业者做出若干关键配置决策，例如使用哪些 LLM、采样多少次、如何组合与过滤候选生成。这些都需要自动化、自适应的架构搜索方法。

在我们的工作中，我们逐一应对这些挑战。首先，我们在指令遵循、推理与编程任务上评估一组全面的现有与新提出的推理时技术的效用。我们同时使用开源与闭源模型，考察集成、融合、排序、批评、验证以及基于模型的单元测试生成/评估等一系列技术（第 3.1 节与第 3.2 节）。我们发现没有单一技术在所有任务上完全占优，不同方法对不同任务更有效。

其次，我们分析推理时技术之间的交互，并探索单独添加新模型与新技术带来的收益。我们发现，生成集成结合批评、验证与融合，能把最终回答质量提升到超过来自单个（未融合）回答的 oracle 最佳候选的水平，尤其对指令遵循与推理任务（图 4；图 7；表 5）。我们还展示了随着扩展推理时技术的层数并组合多种方法，性能随之提升，使我们能发现推理时技术的有效新组合（第 3.2、4.2 节，附录 A.3）。组合多种策略显著改进任务表现，但确定具体组合仍然困难，这需要手动测试模型、推理时技术、架构设计、推理预算等等。

第三，基于我们对推理时技术的分析，我们提出 Archon——一个自动设计由现有推理时技术（或新技术）组成的 LLM 系统的开源模块化框架，使从业者能针对其期望的目标函数（准确率、延迟与成本）进行优化（第 3.1、3.3 节）。与在单个 LM 上做提示工程和工具使用的替代性 LM 系统（Khattab et al., 2023；Yuksekgonul et al., 2024；Hu et al., 2024；Zhang et al., 2024）不同，我们的方法在单一架构中集成多个 LM，并把提示选择简化为一组核心组件。Archon 框架利用自动架构搜索算法为给定任务最大化生成质量，借助受神经架构搜索（NAS）（Zoph & Le, 2017；Ren et al., 2021）启发的贝叶斯优化技术（Snoek et al., 2012；Nardi et al., 2019）快速遍历潜在推理架构的空间（第 3.3 节）。

我们在一组多样的指令遵循、推理与编程基准上评估 Archon 架构（表 1）：MT-Bench、Arena-Hard-Auto、AlpacaEval 2.0、MixEval、MATH 与 CodeContests（Zheng et al., 2023；Li et al., 2024b；Li et al., 2023；Ni et al., 2024；Hendrycks et al., 2021；Li et al., 2022）。我们最佳的 Archon 架构同时超越前沿模型（如 OpenAI 的 O1、GPT-4o 与 Claude-3.5 Sonnet）与先前表现最好的推理时架构（如 ADAS、AFlow 与 MoA），平均将最先进（SOTA）性能提升 15.1%。此外，Archon 在取得 SOTA 表现的同时，比替代推理时架构少用 20.0% 的推理调用、15.1% 的输入 token 与 13.5% 的输出 token（图 1；表 1；图 8）。即便只使用开源 LLM，Archon 架构平均也超过 SOTA LLM 11.2%。

总体而言，我们把 Archon 作为一个开源推理时框架呈现，可通过用户友好的接口轻松扩展到新的推理时技术、模型与任务。

## 2 相关工作

尽管推理时架构已有进展，许多架构聚焦于更多生成（Jiang et al., 2023b；Chen et al., 2024；Davis et al., 2024），这对推理任务有效（Brown et al., 2024）。然而，对指令遵循与推理等任务，融合与排序等技术能有效提升任务表现（Wang et al., 2024a；Jiang et al., 2023b）。先前研究探索了配置的有限方面，往往聚焦特定基准（Jiang et al., 2023b；Wang et al., 2024a；Chen et al., 2024；Li et al., 2024a）。高效地开发推理时架构至关重要，因为最优配置随基准、可用模型与推理计算限制而变（第 4.2 节）。此外，DSPy（Khattab et al., 2023）等 LM 编排框架只为单个 LM 优化单个提示，利用有监督数据使其更擅长工具使用，但仍无法并行或顺序地利用多个推理时技术。这些方法各自手动选择现有技术的一个子集，而 Archon 统一了可用的推理时技术并用搜索算法自动化架构构建，为每组任务简化了模型与组件的选择过程（第 3.1 节与第 3.3 节）。

## 3 Archon 的推理时技术

随着推理时技术的激增，Archon 引入了一个系统化框架来理解这些方法并将其统一到推理时架构中。下面我们详述每种推理时技术的结构、输入与输出（表 3）。然后我们讨论如何把不同技术组合成推理时架构（第 3.2 节），最后探索自动构建推理时架构的方法（第 3.3 节）。

### 3.1 Archon 的 LLM 组件

本节讨论 Archon 的 LLM 组件，即执行特定推理时技术的 LLM。我们测试了一系列受近期工作启发的不同组件，纳入了生成、排序与融合候选的方法（Wang et al., 2024a；Jiang et al., 2023b），以及通过批评、验证与单元测试改进候选回答质量的方法（Bai et al., 2022；Zheng et al., 2023）。组件及其提示总结在表 3 与附录 A.2 中。我们还对给定的 Archon 组件在指令遵循、推理与编程基准上做了广泛的消融研究，以更好理解它们各自的效用及其在不同任务上的最优组合（附录 A.3）。

生成器（Generator）是接受指令提示并输出候选回答的 LLM。生成器可以被并行调用以执行生成集成（即并行调用多个 LLM）（Wang et al., 2024a），或被多次采样（Brown et al., 2024）。模型数、采样数与生成温度均可调整。

我们发现额外的模型采样能显著提升表现（图 6），尤其对编程任务（表 1）。模型集成也有类似模式：从更多模型采样带来持续的性能增长（假设模型按给定任务从好到差排序）（图 7）。

融合器（Fuser）是一个 LLM，给定指令提示与一组提议回答作为输入，组合这些回答以生成一个或多个更高质量的融合回答。

在我们探索的每个基准上，Fuser 模块都大幅提升了表现（平均 8.9%）（图 6；图 7；图 4）。此外，我们在 Archon 框架中添加多层 Fuser 时观察到类似收益（图 4）。改进表现所需的 Fuser 层数因任务而异（图 12），一些任务从增加的层中收益有限（MixEval 准确率提高 1-2 个点），而另一些任务在 3-4 层及以上融合时收益显著（MT Bench 与 Alpaca Eval 2.0 的胜率提高 10 到 15 个点）。

排序器（Ranker）是一个 LLM，给定指令提示与一组提议回答作为输入，按质量对候选生成排序，输出排好序的回答列表。该排序随后用于把回答集合过滤到指定的 top-$K$。

从表 5、图 6 与图 7 的结果看，Ranker 对指令遵循与推理任务最有效，其使用的成对比较聚焦于风格与对提示的遵循。我们发现，在 MT Bench 与 Arena-Hard-Auto 基准上，Ranker 相对随机选择把输出质量提升 10.8%，同时与 oracle 选择相差不到 2.7%。

批评器（Critic）是一个 LLM，给定指令提示与一组提议回答作为输入，为每个回答生成一份优缺点列表，随后用于改进最终回答的质量（第 3.2 节；图 4）。

Critic 模块对我们在图 4 与表 5 中探索的每个任务都有效。在我们 10 模型 70B+ 生成器集成加 Fuser 的 Archon 配置上，添加 Critic 在所探索的基准上平均提升 11.5 个百分点。

验证器（Verifier）是一个 LLM，验证给定候选回答对给定指令提示是否具有恰当的推理。它分两个阶段进行：阶段 #1 接受指令提示与候选回答作为输入，输出该候选回答为何正确的推理；阶段 #2 接受指令提示、候选回答与产生的推理，然后输出推理以及一个裁决（即二元 [Correct] 或 [Incorrect]），判断按给定指令提示与推理，该候选回答是否正确。只有通过验证的回答才会传递到下一 Archon 层。

Verifier 对表 5 中探索的推理基准最有效，在 MixEval、MixEval Hard 与 MATH 上提升 8.4%。当只使用 70B+ 生成器集成并在生成后加 Verifier 模块时，该 Archon 配置在所有探索基准上平均落后于集成加融合器配置 1.5%，提示验证与其他推理时技术结合时最有效。

单元测试生成器（Unit Test Generator）与单元测试评估器（Unit Test Evaluator）是我们系统中互补的 LLM 组件：单元测试生成器接受指令提示并产出 5-10 条简洁的测试语句（第 4.2 节；示例见表 22）用于评估回答的准确性与相关性；评估器接受指令提示、候选回答与这些测试作为输入，按测试通过情况对回答排序。评估器为候选给出论证并聚合测试裁决，为推理与编程任务给每个回答打分，只有通过全部测试的回答才进入下一 Archon 层。该方法通过可配置的测试数量把评估从编程扩展到多种任务类型。

单元测试生成器与评估器对推理与编程任务最有效，在需要更多验证步骤的基准上提升表现（7.4% 的提升）（表 5）。当 70B+ 生成器集成只与单元测试组合时，它对 Arena-Hard-Auto 与 MixEval 等推理任务效果较差，落后集成加融合器配置 3.1%。然而，当我们增加生成采样并为 CodeContests 添加单元测试生成/评估时，我们观察到 Pass@1 性能提升 56%（表 1），从 17.9% 提升到 29.3%。

### 3.2 组合 LLM 组件

扩展推理时技术的性能增益：我们探索单个 Archon 组件的效用，并评估推理时技术的组合是否使我们能构建大于各部分之和的 LM 系统。在我们的分析中，我们考察跨越指令遵循、推理、数学与编程的七个数据集：MT-Bench（Zheng et al., 2023）、AlpacaEval 2.0（Li et al., 2023）、Arena Hard Auto（Li et al., 2024b）、MixEval（Ni et al., 2024）、MixEval-Hard、MATH（Hendrycks et al., 2021）与 CodeContests（Li et al., 2022）。我们还在当前 SOTA 的开源与闭源 LM 上测试（表 34；表 35）。对每项推理时技术的分析，我们聚焦于：1) 在不同基准上测试它；2) 单独扩展其使用；3) 在随机选择另一项技术并保持其固定的同时扩展它；4) 改变它在不同组件中的位置。我们把这些消融实验放在 A.3 节，其中 Archon 组件组合见表 5，组合中使用的模型类型见表 6 与表 9。

从我们的分析中，我们发现了推理时架构组合的若干趋势（以 T 标记）：

- T1：重复的模型采样与更多集成模型带来可观收益，分别带来 9.3% 与 18.5% 的增长（图 11；图 7）。
- T2：扩展推理时技术的层数显著改进指令遵循、推理与编程任务的表现，例如总是在最后一层加单个融合器（图 4）。
- T3：扩展纳入的推理时技术的多样性也能提升所探索任务的表现，其中融合器之前放置批评器与排序器尤其有效（图 4；图 11）。
- T4：在推理任务中，把 Verifier 与单元测试生成器/评估器模块和 Fuser 一同纳入，能通过过滤有缺陷的回答改进表现，为 MixEval 与 CodeContests 等任务贡献显著的性能增益（表 5；A.9 节）。

框架概览：基于我们对推理时组件的分析，我们提出 Archon——一个自动设计由现有推理时技术（或新技术）组成的 LLM 系统的框架。受神经网络结构启发（Hinton et al., 1992），Archon 由 LLM 组件的层构成（图 2；第 3.1 节）。每层由并行调用的 LLM 组件集合组成。这些组件对初始指令提示与来自上一层的候选回答执行文本到文本的操作。此外，与神经网络类似，一些层对给定字符串列表执行变换（如生成器与融合器），把字符串列表转换为不同的字符串列表（候选数量可以与原始候选数量不同）。其他组件为 Archon 结构引入非线性，执行字符串列表的过滤（如排序器与验证器）。最终，每层的输入与输出总是一个字符串列表——无论那是指令提示（即单个字符串）还是候选回答列表。若 Archon 结构的最后一层输出一个字符串列表，则返回列表中的第一个字符串。

与经典神经网络不同，LLM 组件与层之间不学习任何权重；相应地，Archon 架构可以不经任何调优直接部署。此外，单个状态从输入层到最终输出被顺序变换；这个单一状态就是初始指令提示与当前候选回答（示例架构见图 3）。

图 3：示例 Archon 架构：该架构从十个生成器模型（各采样一次）开始，随后是一个批评器模型、一个排序器模型、一层六个融合器模型、一个验证器模型，最后以一个融合器模型收尾。

构建规则：第 3.1 节中的 LLM 组件只能按特定顺序放置（表 4）。虽然 Archon 组件的替代组合与排序在技术上可行，但在七个基准与两类模型（开源与闭源）上对 Archon 组件进行消融研究后，我们发现这些排序是最优的（附录 A.3）。

1. 任一给定层只允许一种类型的组件。
2. 生成器组件只能放在 Archon 的第一层；可以放置一个或多个生成器。
3. Critic 必须在 Ranker 或 Fuser 之前。否则，生成的优缺点无法被纳入生成排序或融合。
4. Ranker、Critic、Verifier 与单元测试生成器/评估器层可以放在 Archon 中除第一层之外的任何位置。对这些组件中的每一个，它必须是该层中唯一的模块。
5. Fuser 组件可以放在 Archon 中除第一层之外的任何位置。一层可以使用多个 Fuser。
6. 单元测试生成器与评估器放在连续的层中，且单元测试生成器总在前。

图 4：通过扩展推理时技术的层数改进表现：在控制推理预算的情况下，跨 8 个不同 70B LLM 的生成集成与融合，通常比只用表现最佳模型做重复采样更有效。此外，添加批评与融合的层平均带来 18.8% 的任务性能提升。然而，最佳推理时架构因任务而异，如 MixEval 与 CodeContests（第 4.3 节），这促使我们为 Archon 开发架构搜索技术（第 3.3 节）。

### 3.3 架构搜索算法

搜索超参数：本节探索如何通过 Archon 的架构搜索算法自动为目标任务设计推理时架构。在第 3.2 节分析所发现趋势的指导下，我们为搜索空间确立六个超参数轴：

1. 集成的 Top-$K$ 生成器：初始生成器集成的 top-$K$ 模型，范围从 1 到 10（T1）。top-$K$ 模型按其在目标任务上的单独表现贪心选出（表 35）。
2. Top-$K$ 生成器采样：从每个集成生成器收集的样本数（对所有模型相同），范围从 1 到 5（T1）。对 CodeContests，我们探索高采样设置：[1, 10, 100, 500, 1000]。
3. 融合层数：范围从 1 到 4。最后一个融合层将始终只有一个 Fuser（T2）。
4. Top-$K$ 融合器：每个融合层使用的模型数，从 2 到 10、步长为 2（T2,3）。
5. Critic 与 Ranker 层：我们在每个融合器层之前添加批评与排序层，因为我们发现它们在所探索的基准上带来额外收益（T3）（第 3.2 节；图 4；图 7）。
6. 评估层：选择在最后一个 Fuser 层之前添加 Verifier、单元测试生成/评估，或都不加（T4）。

虽然进一步扩展潜在 Archon 架构的搜索空间是可能的（例如生成式 LLM 组件的不同温度、每个 LLM 组件的替代提示、Archon 的更多 LLM 组件等），但我们从第 3.2 节识别的趋势合理地把配置的搜索空间约束到最有影响力的超参数上。总计，我们的搜索空间包含 9,576 个配置，这是通过组合所有可能的超参数并移除无效配置得到的（例如，我们丢弃初始生成数超出融合器上下文窗口的配置）。

搜索方法：Archon 搜索方法接受四个输入：目标基准、推理调用预算、可用 LLM 集合与用于构建的推理时技术（图 2）。作为输出，搜索方法输出单个优化后的 Archon 架构。我们用每个目标数据集的 20% 作为指导架构搜索的开发集。我们探索三种 Archon 架构搜索方法：随机搜索（在搜索空间中随机测试潜在架构）、贪心搜索（从随机初始架构开始，一次一个地贪心优化各超参数）与贝叶斯优化（Snoek et al., 2012）（用高斯过程做全局超参数优化）。贝叶斯优化接受一个指定配置选择的向量作为输入：生成器（即模型数与样本数）、融合器层、每层融合器数，以及最终验证器/单元测试器（第 3.2 节）。贝叶斯优化先采样指定数量的随机 Archon 架构来校准其代理模型。这些采样架构的任务表现被用来在配置搜索期间指导更有依据的架构建议。算法重复以下循环——评估每个建议的架构并用其表现精炼后续建议——直到发现最优 Archon 配置，或推理调用预算耗尽。关于我们开源贝叶斯优化方法的更多细节请见附录 A.4，其中我们进一步讨论实现以及如何使用替代优化函数（如延迟）。

贝叶斯优化在 96.0% 的搜索中找到最佳架构，所需的架构评估比贪心搜索少 88.5%、比随机搜索少 90.4%（图 10）。贝叶斯优化的有效性随初始随机采样架构数量增加而上升，直到约 230-240 个样本，此后进一步测试最好聚焦于配置搜索（表 26）。对有限的推理调用预算（<20 次调用），贝叶斯优化效果较差，贪心搜索等传统方法可能表现相当（表 27）。

添加搜索限制：为在架构搜索期间施加计算约束，我们把任何会超出推理调用、输入 token 或输出 token 预算的 Archon 架构从搜索空间排除。可以添加多重限制。例如，你可以过滤掉超过 20 次推理调用或超过 20,000 输入 token 的架构。这使我们的贝叶斯优化算法在架构搜索中根本不会考虑这些无效架构，使我们能够与 ADAS、AFlow 等替代推理时框架做计算对齐的比较（图 8；图 5）。

## 4 实验

我们的实验聚焦于回答以下问题：(1) 在准确率与计算效率上，Archon 与现有 SOTA LLM 及推理时架构相比如何（第 4.2 节）？(2) Archon 的表现在所探索任务之间比较如何（第 4.3 节）？(3) 围绕 Archon 的模型规模、延迟与成本有哪些考量（第 4.4 节）？我们在第 4.1 节概述构建 Archon 架构的基准、模型与技术。

### 4.1 基准与模型

表 1：Archon 用开源、闭源与全源模型取得的强劲表现：在所探索的基准上持续超过 SOTA LLM 与 LM 系统。标准误由 10 次独立评估运行计算。∗MATH 与 CodeContests 使用其测试集的子集进行评估（第 4.1 节）。

| 类别 | 方法 | 平均推理调用 | 平均输入 token | 平均输出 token | 每查询平均 PFLOPs | 每查询美元 | MT Bench W.R. | AlpacaEval 2.0 L.C. W.R. | Arena-Hard-Auto W.R. | MixEval-Hard W.R. | MixEval Acc. | MATH Acc. | CodeContests Pass@1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 基线 LM | GPT-4o | 1 | 95 | 549 | 0.6 ± 0.1 | 0.01 ± 0.01 | 44.2% ±0.5 | 57.8% ±0.6 | 80.6% ±0.6 | 63.4% ±0.2 | 87.5% ±0.3 | 83.5% ±0.4 | 18.1% ±0.2 |
| | Claude 3.5 Sonnet | 1 | 105 | 602 | 1.4 ± 0.2 | 0.01 ± 0.01 | N/A | 52.7% ±0.4 | 81.4% ±0.4 | 68.7% ±0.2 | 89.1% ±0.2 | 82.5% ±0.7 | 12.3% ±0.4 |
| | Llama 3.1 405B | 1 | 118 | 631 | 1.5 ± 0.1 | 0.01 ± 0.01 | 44.1% ±0.3 | 40.7% ±0.5 | 64.5% ±0.7 | 66.0% ±0.3 | 88.2% ±0.2 | 85.0% ±0.5 | 20.4% ±0.5 |
| LM 系统 | MoA | 19 | 25,109 | 17,422 | 15.3 ± 0.3 | 0.06 ± 0.01 | 51.6% ±0.6 | 65.0% ±0.3 | 85.3% ±0.3 | 62.3% ±0.4 | 86.9% ±0.2 | 82.9% ±0.6 | 15.1% ±0.5 |
| | ADAS | 52 | 72,804 | 44,872 | 58.8 ± 0.3 | 0.63 ± 0.04 | 66.3% ±0.7 | 60.1% ±0.5 | 85.4% ±0.4 | 64.2% ±0.2 | 87.0% ±0.2 | 86.0% ±0.8 | 23.7% ±0.3 |
| | AFlow | 48 | 68,596 | 41,748 | 55.2 ± 0.4 | 0.59 ± 0.05 | 62.4% ±0.2 | 57.8% ±0.6 | 83.2% ±0.6 | 63.5% ±0.3 | 87.2% ±0.4 | 84.5% ±0.2 | 21.1% ±0.6 |
| | o1 | Unk. | 112 | Unk. | Unk. | 0.52 ±0.05 | 56.3% ±0.5 | 59.3% ±0.5 | 81.7% ±0.3 | 72.0% ±0.4 | 87.5% ±0.2 | 92.7% ±0.5 | 31.5% ±0.8 |
| Archon 开源 | 通用目的 | 35 | 51,113 | 31,508 | 3.1 ± 0.3 | 0.12 ± 0.02 | 67.2% ±0.4 | 63.3% ±0.6 | 85.6% ±0.5 | 65.3% ±0.3 | 86.2% ±0.2 | 87.5% ±0.6 | 18.2% ±0.4 |
| | 任务专属 | 44 | 63,157 | 39,949 | 3.7 ± 0.3 | 0.15 ± 0.02 | 71.1% ±0.6 | 68.1% ±0.4 | 89.6% ±0.4 | 67.5% ±0.2 | 88.8% ±0.3 | 89.5% ±0.3 | 28.9% ±0.9 |
| Archon 闭源 | 通用目的 | 32 | 52,747 | 27,894 | 40.3 ± 0.5 | 0.44 ± 0.04 | 72.7% ±0.3 | 63.9% ±0.7 | 86.2% ±0.7 | 67.5% ±0.4 | 87.2% ±0.2 | 87.9% ±0.7 | 20.2% ±0.6 |
| | 任务专属 | 40 | 59,085 | 37,271 | 48.2 ± 0.4 | 0.49 ± 0.05 | 77.0% ±0.5 | 68.9% ±0.5 | 90.5% ±0.3 | 72.3% ±0.3 | 89.5% ±0.3 | 92.1% ±0.4 | 25.1% ±0.6 |
| Archon 全源 | 通用目的 | 35 | 50,427 | 30,461 | 27.8 ± 0.4 | 0.32 ± 0.04 | 76.2% ±0.7 | 66.4% ±0.3 | 89.8% ±0.6 | 69.8% ±0.2 | 87.3% ±0.4 | 89.3% ±0.5 | 23.4% ±0.9 |
| | 任务专属 | 39 | 58,250 | 36,114 | 33.7 ± 0.6 | 0.37 ± 0.04 | 79.5% ±0.4 | 69.0% ±0.6 | 92.5% ±0.5 | 72.7% ±0.3 | 89.7% ±0.2 | 93.5% ±0.6 | 41.4% ±0.7 |

基准：我们用若干覆盖指令遵循、推理与编程的基准评估模型：MT-Bench（Zheng et al., 2023）、AlpacaEval 2.0（Li et al., 2023）、Arena Hard Auto（Li et al., 2024b）、MixEval（Ni et al., 2024）、MixEval-Hard、MATH（Hendrycks et al., 2021）与 CodeContests（Li et al., 2022）。表 28 给出各数据集概览。由于我们在每个基准随机抽样的 20% 子集上执行自动架构搜索，我们在基准其余留出的 80% 子集上评估（表 1）（Archon 在完整基准上的表现请见表 33）。Archon 在完整基准与 80% 留出子集上的表现差异较小：这些数据集上平均仅 0.44%，标准差 0.20%。对 MATH，我们从数据集测试集随机抽样 200 道题评估。对 CodeContests，我们在不含图片标签的 140 道测试集题目上评估。

模型：我们通过创建不同 Archon 架构来测试 Archon 框架的效力，涵盖三类模型：8B 及以下参数模型、70B 及以上参数模型，以及闭源模型 API。对 8B 与 70B+ 模型，我们选取 2024 年 7 月 Chatbot Arena 排行榜（Chiang et al., 2024）上各参数区间表现最好的前 10 个聊天模型。对 Archon 架构，我们探索多种模型类型：开源、闭源与全源（即可同时使用开源与闭源）。对闭源模型 API，我们纳入 GPT-4o、GPT-4-Turbo、Claude Opus 3.0、Claude Haiku 3.0 与 Claude Sonnet 3.5。我们在表 34 与表 35 中列出并比较 Archon 框架中测试的全部模型。对所用 LLM 与每个 Archon 组件，我们把生成温度设为 0.7。作为基线，我们让 Archon 同时与 SOTA 单调用 LLM（GPT-4o（OpenAI, 2024）、Claude 3.5 Sonnet（Anthropic, 2024）与 Llama 3.1 405B Instruct（Dubey et al., 2024））以及 SOTA 推理时方法（OpenAI 的 o1（OpenAI, 2024）、MoA（Wang et al., 2024a）、ADAS（Hu et al., 2024）与 AFlow（Zhang et al., 2024））比较。

任务专属与通用目的 Archon 架构：我们比较专门为单一评估数据集配置的定制 Archon 架构（「任务专属 Archon 架构」）与配置为处理所有评估数据集的泛化 Archon 架构（「通用目的 Archon 架构」）（表 1）。对 Archon 的三种模型选择设置（开源、闭源与全源），我们利用自动架构搜索为每个任务找到定向的 Archon 架构（共 7 个架构），并找到单一泛化 Archon 架构以最大化所有任务上的表现（表 1）。为泛化 Archon 架构搜索，各基准被拼接并打乱。重要的是，第 4 节中使用的所有 Archon 架构都由我们的贝叶斯架构搜索技术自动生成，该技术在第 3.3 节所述的 Archon 超参数搜索空间上搜索。定向与泛化 Archon 架构的例子见图 3 与附录 A.9。对我们的架构，我们在表 1 中按类别概述平均输入 token 数（即整个架构上输入 token 的合计总数）与输出 token 数（即整个架构上输出 token 的合计总数）。

### 4.2 Archon 对比闭源 LLM 与其他推理时架构

任务表现：我们首先在一组指令遵循、推理与编程任务上，把 Archon 架构与现有 SOTA 闭源 LLM 及推理时架构比较。基于表 1 的结果，我们发现 Archon 架构在所有探索的基准上持续匹敌或超越现有方法。开源模型的 Archon 架构相对 SOTA 开源方法平均改进 11.2%；即便在其最差表现上，我们的开源 Archon 架构在 AlpacaEval 2.0 上仍比 SOTA 开源方法高出 3.1%。闭源模型的 Archon 架构在 MT Bench、Arena-Hard-Auto、MixEval 与 MixEval-Hard 上取得 SOTA 表现，相对闭源 LM 平均改进 15.1%、相对开源推理时框架（即 MoA、ADAS 与 AFlow）平均改进 8.4%。与 o1 和 o1-mini 相比，Archon 的最佳定向架构在 MT Bench、AlpacaEval 2.0、Arena Hard Auto、MixEval、MixEval Hard、MATH 与 CodeContests 上平均分别超出 8.1% 与 9.7%。对使用全部可用模型（开源与闭源）的方法，Archon 相对现有 SOTA 单调用 LLM 平均改进 10.9%，相对现有推理时框架平均改进 8.6%。

计算效率：与开源推理时框架（即 AFlow、ADAS、MoA）相比，Archon 的推理调用效率高 20.0%，同时在所有测试基准上表现更高（表 1）。我们还发现，相比最佳的替代开源推理时框架，我们最佳的 Archon 架构少用 15.1% 的输入 token 与 13.5% 的输出 token。当我们以不同 token 预算使用 Archon 的架构搜索技术时（图 8），我们发现生成的 Archon 架构在相同预算下比替代基线高 12.4% 的表现。总体而言，泛化的全源 Archon 架构在所有任务上取得 6.4% 更好的表现，同时比最佳 LM 系统基线的 token 效率高 31%（表 1）。此外，与泛化的全源 Archon 架构相比，定向的全源 Archon 架构分别多使用 15.5% 与 18.6% 的输入与输出 token，但平均取得 8.4% 更高的准确率。定向架构计算更密集，因为它们可以进一步把额外 LM 操作用于单一组特定任务约束（附录 A.9）。

发现的架构：我们把定向与泛化 Archon 架构放在附录 A.9（图 13）。表现最好的全源通用目的 Archon 架构从我们 10 个最佳生成器的宽初始层开始，随后是分别用 Qwen2 72B 与 Claude 3.5 Sonnet 进行的连续四层批评与融合。后续每层的融合器模型更少（即 8、6、4），在最终输出前对生成产生「漏斗」效应。最佳定向架构因任务而异。对指令遵循与推理任务，定向架构倾向于用多样化 LM 混合做多层的批评与融合（图 14）。对数学任务，定向架构倾向于由初始的大量生成组成，然后快速缩减到选定的答案（图 15）。对编程任务，定向架构倾向于在输出答案前对单个回答做多轮生成、批评与融合（图 16）。除附录 A.9 收录的 Archon 架构外，我们在补充文件中提供全部泛化与定向 Archon 架构。

为探索我们通用目的 Archon 架构的效力，我们在三个此前未见过的任务上评估：GPQA（Rein et al., 2024）、MMLU（Hendrycks et al., 2021）与 MMLU Pro（Wang et al.）。我们发现我们的全源通用目的 Archon 架构在这些基准上捕获任务专属 Archon 架构表现的 91 到 94%，表明我们的架构更广泛地适用于域外任务（表 2）。泛化的 ADAS 与 AFlow 架构分别只达到其专门化架构表现的 66% 与 74%。

| | GPQA Diamond | MMLU∗ | MMLU Pro∗ |
| --- | --- | --- | --- |
| 全源泛化 AFlow | 37.1%±0.2 | 53.0%±0.4 | 43.4%±0.4 |
| 任务专属 AFlow | 52.4%±0.1 | 71.8%±0.5 | 62.9%±0.5 |
| AFlow 性能保留率 | 70.8% | 73.8% | 67.0% |
| 全源泛化 ADAS | 39.8%±0.3 | 53.5%±0.3 | 44.1%±0.7 |
| 任务专属 ADAS | 54.4%±0.5 | 73.0%±0.4 | 66.0%±0.4 |
| ADAS 性能保留率 | 73.2% | 73.3% | 66.8% |
| 全源泛化 Archon | 56.1%±0.4 | 76.5%±0.3 | 71.0%±0.1 |
| 任务专属 Archon | 61.2%±0.5 | 81.5%±0.3 | 75.4%±0.4 |
| Archon 性能保留率 | 91.7% | 93.9% | 94.2% |

表 2：泛化 Archon 架构在域外任务上的强劲表现：尽管未针对这些任务训练，泛化 Archon 架构在 GPQA、MMLU 与 MMLU Pro 上达到专门化 Archon 架构表现的 91 到 95%。标准误由 10 次独立评估运行计算。∗对 MMLU 与 MMLU Pro，我们使用测试集随机选取的 500 个查询样本进行评估。

图 5：Archon 的表现在各 FLOP 预算下超过基线：在不同 FLOP 预算下（第 3.3 节），我们把 Archon 架构与表现最好的推理时系统基线比较。MoA 架构与 OpenAI 的 o1 是静态的，因此它们在各预算下使用相同数量的 token。结果为 10 次独立评估运行的平均。∗MATH 与 CodeContests 使用其测试集的子集进行评估（第 4.1 节）。

### 4.3 按任务看 Archon

指令遵循与推理：在 MT Bench、AlpacaEval 2.0 与 Arena-Hard-Auto 上，开源 Archon 架构平均超过当前开源基线 10.5%，闭源 Archon 超过当前闭源基线 14.6%（表 1）。有了 Archon，用于生成器的多个模型与融合层的深度带来指令遵循任务上的性能提升，增加了回答的丰富度并允许对逐步的指令遵循做多轮迭代（表 36）。对推理任务，虽然当我们考虑 MixEval 与 MixEval-Hard 的总分时 Archon 的性能提升较小，但当我们为 MixEval 与 MixEval-Hard 下的每个单独任务创建推理时架构时，确实看到有意义的性能增长（表 30；表 31）。当我们为每个子任务创建单独的 Archon 架构时，MixEval 与 MixEval-Hard 的准确率分别平均提高 3.7 与 8.9 个百分点。这一发现表明，推理任务（如数学、科学、逻辑）需要更加个体化的推理时架构。

编程：我们观察到集成、融合与排序技术对 CodeContests 的影响有限（图 4）。例如，当我们把表 28 中的通用全源架构应用于 CodeContests 题目时，Archon 带来的增益很小（见表 1）。一个促成因素是：与指令遵循/推理任务的分布不同，编程任务往往有一两个 LLM 的表现显著优于其余模型（表 35）。然而，当我们添加单元测试生成/评估并扩大样本数量时，Archon 在 CodeContests 上的表现显著改进（表 1），使我们能把 GPT-4o 的 Pass@1 提升 44.3%（140 道题中从 40 提升到 58）。对基于模型的单元测试生成/评估，我们生成 5 个单元测试并用 LM 依据生成的单元测试评估每个候选回答，从而对不同的候选回答排序（细节见 A.2 节）。

### 4.4 讨论

模型规模的影响：Archon 框架在使用 70B+ 参数的 LLM 时最有效。当我们用 7B 开源模型构建 Archon 架构时，相对最佳的单独 7B LM，我们可以平均把任务表现提升 7.5%（表 38）。跨任务看，7B 模型适合做排序，但在批评与融合上效果较差。

延迟与成本：由于 Archon 架构为不同操作连续进行多次 LLM API 调用，其时间与花费可能是单次 LLM API 调用的 5 倍（表 39；表 40）。注意，这些计算成本与延迟的增加换来更高质量的回答，在许多应用领域（如科学、编程与复杂智能体任务）是合理的（Mialon et al., 2023；Rein et al., 2023）。此外，LLM 厂商正在快速降低推理成本（表 39）。对速度最重要的任务，未来工作应探索如何用蒸馏策略（Sreenivas et al., 2024；DeepSeek-AI et al., 2025）把 Archon 架构的聚合知识打包进更小的 LM。

## 致谢

我们感谢 Simran Arora、Daniel Biderman、Bradley Brown、Ryan Ehrlich、Sabri Eyuboglu、Jordan Juravsky、Jerry Liu、Avanika Narayan、Benjamin Spector、Alyssa Unell、Benjamin Viggiano 与 Michael Zhang 在论文撰写期间的建设性反馈。我们也感谢斯坦福人工智能实验室（SAIL）与 TogetherAI 的合作者。

我们衷心感谢以下支持：NIH（No. U54EB020405，Mobilize）；NSF（Nos. CCF2247015，Hardware-Aware；CCF1763315，Beyond Sparsity；CCF1563078，Volume to Velocity；1937301，RTML）；US DEVCOM ARL（Nos. W911NF-23-2-0184，Long-context；W911NF-21-2-0251，Interactive Human-AI Teaming）；ONR（No. N000142312633，Deep Signal Processing）；Stanford HAI（No. 247183）；Google DeepMind；Google Research；Google Cloud；NXP；Xilinx；LETI-CEA；Intel；IBM；Microsoft；NEC；Toshiba；TSMC；ARM；Hitachi；BASF；Accenture；Ericsson；Qualcomm；Analog Devices；Salesforce；Total；HAI-GCP Cloud Credits for Research 计划；斯坦福数据科学计划（SDSI）；斯坦福 DAWN 项目成员：Meta、Google 和 VMWare；以及斯坦福 SEAMS 项目成员：IBM 和 Felicis。美国政府被授权出于政府目的复制和分发重印本，尽管其上可能有任何版权标注。本材料中表达的观点、发现、结论或建议均为作者个人观点，不一定反映 NIH、ONR 或美国政府的观点、政策或背书，无论是明示还是暗示。

## 参考文献

- [1]

  Abdin, M., Jacobs, S. A., Awan, A. A., Aneja, J., Awadallah, A., Awadalla, H., Bach, N., Bahree, A., Bakhtiari, A., Behl, H., et al.
  Phi-3 technical report: A highly capable language model locally on your phone.
  *arXiv preprint arXiv:2404.14219*, 2024.
- [2]

  Anthropic.
  The claude 3 model family: Opus, sonnet, haiku.
  *ArXiv*, 2024.
- [3]

  at Meta, A.
  Llama 3 model card.
  *ArXiv*, 2024.
  URL <https://github.com/meta-llama/llama3/blob/main/MODEL_CARD.md>.
- [4]

  Bai, J., Bai, S., Chu, Y., Cui, Z., Dang, K., Deng, X., Fan, Y., Ge, W., Han, Y., Huang, F., Hui, B., Ji, L., Li, M., Lin, J., Lin, R., Liu, D., Liu, G., Lu, C., Lu, K., Ma, J., Men, R., Ren, X., Ren, X., Tan, C., Tan, S., Tu, J., Wang, P., Wang, S., Wang, W., Wu, S., Xu, B., Xu, J., Yang, A., Yang, H., Yang, J., Yang, S., Yao, Y., Yu, B., Yuan, H., Yuan, Z., Zhang, J., Zhang, X., Zhang, Y., Zhang, Z., Zhou, C., Zhou, J., Zhou, X., and Zhu, T.
  Qwen technical report.
  *arXiv preprint arXiv:2309.16609*, 2023.
- [5]

  Bai, Y., Kadavath, S., Kundu, S., Askell, A., Kernion, J., Jones, A., Chen, A., Goldie, A., Mirhoseini, A., McKinnon, C., Chen, C., Olsson, C., Olah, C., Hernandez, D., Drain, D., Ganguli, D., Li, D., Tran-Johnson, E., Perez, E., Kerr, J., Mueller, J., Ladish, J., Landau, J., Ndousse, K., Lukosuite, K., Lovitt, L., Sellitto, M., Elhage, N., Schiefer, N., Mercado, N., DasSarma, N., Lasenby, R., Larson, R., Ringer, S., Johnston, S., Kravec, S., Showk, S. E., Fort, S., Lanham, T., Telleen-Lawton, T., Conerly, T., Henighan, T., Hume, T., Bowman, S. R., Hatfield-Dodds, Z., Mann, B., Amodei, D., Joseph, N., McCandlish, S., Brown, T., and Kaplan, J.
  Constitutional ai: Harmlessness from ai feedback, 2022.
  URL <https://arxiv.org/abs/2212.08073>.
- [6]

  Brown, B., Juravsky, J., Ehrlich, R., Clark, R., Le, Q. V., Ré, C., and Mirhoseini, A.
  Large language monkeys: Scaling inference compute with repeated sampling, 2024.
  URL <https://arxiv.org/abs/2407.21787>.
- [7]

  Chen, L., Davis, J. Q., Hanin, B., Bailis, P., Stoica, I., Zaharia, M., and Zou, J.
  Are more llm calls all you need? towards scaling laws of compound inference systems, 2024.
  URL <https://arxiv.org/abs/2403.02419>.
- [8]

  Chiang, W.-L., Zheng, L., Sheng, Y., Angelopoulos, A. N., Li, T., Li, D., Zhang, H., Zhu, B., Jordan, M., Gonzalez, J. E., and Stoica, I.
  Chatbot arena: An open platform for evaluating llms by human preference, 2024.
- [9]

  Databricks.
  Dbrx technical report.
  2024.
- [10]

  Davis, J. Q., Hanin, B., Chen, L., Bailis, P., Stoica, I., and Zaharia, M.
  Networks of networks: Complexity class principles applied to compound ai systems design, 2024.
  URL <https://arxiv.org/abs/2407.16831>.
- [11]

  DeepSeek-AI, Guo, D., Yang, D., Zhang, H., Song, J., Zhang, R., Xu, R., Zhu, Q., Ma, S., Wang, P., Bi, X., Zhang, X., Yu, X., Wu, Y., Wu, Z. F., Gou, Z., Shao, Z., Li, Z., Gao, Z., Liu, A., Xue, B., Wang, B., Wu, B., Feng, B., Lu, C., Zhao, C., Deng, C., Zhang, C., Ruan, C., Dai, D., Chen, D., Ji, D., Li, E., Lin, F., Dai, F., Luo, F., Hao, G., Chen, G., Li, G., Zhang, H., Bao, H., Xu, H., Wang, H., Ding, H., Xin, H., Gao, H., Qu, H., Li, H., Guo, J., Li, J., Wang, J., Chen, J., Yuan, J., Qiu, J., Li, J., Cai, J. L., Ni, J., Liang, J., Chen, J., Dong, K., Hu, K., Gao, K., Guan, K., Huang, K., Yu, K., Wang, L., Zhang, L., Zhao, L., Wang, L., Zhang, L., Xu, L., Xia, L., Zhang, M., Zhang, M., Tang, M., Li, M., Wang, M., Li, M., Tian, N., Huang, P., Zhang, P., Wang, Q., Chen, Q., Du, Q., Ge, R., Zhang, R., Pan, R., Wang, R., Chen, R. J., Jin, R. L., Chen, R., Lu, S., Zhou, S., Chen, S., Ye, S., Wang, S., Yu, S., Zhou, S., Pan, S., Li, S. S., Zhou, S., Wu, S., Ye, S., Yun, T., Pei, T., Sun, T., Wang, T., Zeng, W.,
  Zhao, W., Liu, W., Liang, W., Gao, W., Yu, W., Zhang, W., Xiao, W. L., An, W., Liu, X., Wang, X., Chen, X., Nie, X., Cheng, X., Liu, X., Xie, X., Liu, X., Yang, X., Li, X., Su, X., Lin, X., Li, X. Q., Jin, X., Shen, X., Chen, X., Sun, X., Wang, X., Song, X., Zhou, X., Wang, X., Shan, X., Li, Y. K., Wang, Y. Q., Wei, Y. X., Zhang, Y., Xu, Y., Li, Y., Zhao, Y., Sun, Y., Wang, Y., Yu, Y., Zhang, Y., Shi, Y., Xiong, Y., He, Y., Piao, Y., Wang, Y., Tan, Y., Ma, Y., Liu, Y., Guo, Y., Ou, Y., Wang, Y., Gong, Y., Zou, Y., He, Y., Xiong, Y., Luo, Y., You, Y., Liu, Y., Zhou, Y., Zhu, Y. X., Xu, Y., Huang, Y., Li, Y., Zheng, Y., Zhu, Y., Ma, Y., Tang, Y., Zha, Y., Yan, Y., Ren, Z. Z., Ren, Z., Sha, Z., Fu, Z., Xu, Z., Xie, Z., Zhang, Z., Hao, Z., Ma, Z., Yan, Z., Wu, Z., Gu, Z., Zhu, Z., Liu, Z., Li, Z., Xie, Z., Song, Z., Pan, Z., Huang, Z., Xu, Z., Zhang, Z., and Zhang, Z.
  Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning, 2025.
  URL <https://arxiv.org/abs/2501.12948>.
- [12]

  Dubey, A., Jauhri, A., Pandey, A., Kadian, A., Al-Dahle, A., Letman, A., Mathur, A., Schelten, A., Yang, A., Fan, A., Goyal, A., Hartshorn, A., Yang, A., Mitra, A., Sravankumar, A., Korenev, A., Hinsvark, A., Rao, A., Zhang, A., Rodriguez, A., Gregerson, A., Spataru, A., Roziere, B., Biron, B., Tang, B., Chern, B., Caucheteux, C., Nayak, C., Bi, C., Marra, C., McConnell, C., Keller, C., Touret, C., Wu, C., Wong, C., Ferrer, C. C., Nikolaidis, C., Allonsius, D., Song, D., Pintz, D., Livshits, D., Esiobu, D., Choudhary, D., Mahajan, D., Garcia-Olano, D., Perino, D., Hupkes, D., Lakomkin, E., AlBadawy, E., Lobanova, E., Dinan, E., Smith, E. M., Radenovic, F., Zhang, F., Synnaeve, G., Lee, G., Anderson, G. L., Nail, G., Mialon, G., Pang, G., Cucurell, G., Nguyen, H., Korevaar, H., Xu, H., Touvron, H., Zarov, I., Ibarra, I. A., Kloumann, I., Misra, I., Evtimov, I., Copet, J., Lee, J., Geffert, J., Vranes, J., Park, J., Mahadeokar, J., Shah, J., van der Linde, J., Billock, J., Hong, J., Lee, J., Fu, J., Chi, J.,
  Huang, J., Liu, J., Wang, J., Yu, J., Bitton, J., Spisak, J., Park, J., Rocca, J., Johnstun, J., Saxe, J., Jia, J., Alwala, K. V., Upasani, K., Plawiak, K., Li, K., Heafield, K., Stone, K., El-Arini, K., Iyer, K., Malik, K., Chiu, K., Bhalla, K., Rantala-Yeary, L., van der Maaten, L., Chen, L., Tan, L., Jenkins, L., Martin, L., Madaan, L., Malo, L., Blecher, L., Landzaat, L., de Oliveira, L., Muzzi, M., Pasupuleti, M., Singh, M., Paluri, M., Kardas, M., Oldham, M., Rita, M., Pavlova, M., Kambadur, M., Lewis, M., Si, M., Singh, M. K., Hassan, M., Goyal, N., Torabi, N., Bashlykov, N., Bogoychev, N., Chatterji, N., Duchenne, O., Çelebi, O., Alrassy, P., Zhang, P., Li, P., Vasic, P., Weng, P., Bhargava, P., Dubal, P., Krishnan, P., Koura, P. S., Xu, P., He, Q., Dong, Q., Srinivasan, R., Ganapathy, R., Calderer, R., Cabral, R. S., Stojnic, R., Raileanu, R., Girdhar, R., Patel, R., Sauvestre, R., Polidoro, R., Sumbaly, R., Taylor, R., Silva, R., Hou, R., Wang, R., Hosseini, S., Chennabasappa, S., Singh, S.,
  Bell, S., Kim, S. S., Edunov, S., Nie, S., Narang, S., Raparthy, S., Shen, S., Wan, S., Bhosale, S., Zhang, S., Vandenhende, S., Batra, S., Whitman, S., Sootla, S., Collot, S., Gururangan, S., Borodinsky, S., Herman, T., Fowler, T., Sheasha, T., Georgiou, T., Scialom, T., Speckbacher, T., Mihaylov, T., Xiao, T., Karn, U., Goswami, V., Gupta, V., Ramanathan, V., Kerkez, V., Gonguet, V., Do, V., Vogeti, V., Petrovic, V., Chu, W., Xiong, W., Fu, W., Meers, W., Martinet, X., Wang, X., Tan, X. E., Xie, X., Jia, X., Wang, X., Goldschlag, Y., Gaur, Y., Babaei, Y., Wen, Y., Song, Y., Zhang, Y., Li, Y., Mao, Y., Coudert, Z. D., Yan, Z., Chen, Z., Papakipos, Z., Singh, A., Grattafiori, A., Jain, A., Kelsey, A., Shajnfeld, A., Gangidi, A., Victoria, A., Goldstand, A., Menon, A., Sharma, A., Boesenberg, A., Vaughan, A., Baevski, A., Feinstein, A., Kallet, A., Sangani, A., Yunus, A., Lupu, A., Alvarado, A., Caples, A., Gu, A., Ho, A., Poulton, A., Ryan, A., Ramchandani, A., Franco, A., Saraf, A., Chowdhury, A., Gabriel,
  A., Bharambe, A., Eisenman, A., Yazdan, A., James, B., Maurer, B., Leonhardi, B., Huang, B., Loyd, B., Paola, B. D., Paranjape, B., Liu, B., Wu, B., Ni, B., Hancock, B., Wasti, B., Spence, B., Stojkovic, B., Gamido, B., Montalvo, B., Parker, C., Burton, C., Mejia, C., Wang, C., Kim, C., Zhou, C., Hu, C., Chu, C.-H., Cai, C., Tindal, C., Feichtenhofer, C., Civin, D., Beaty, D., Kreymer, D., Li, D., Wyatt, D., Adkins, D., Xu, D., Testuggine, D., David, D., Parikh, D., Liskovich, D., Foss, D., Wang, D., Le, D., Holland, D., Dowling, E., Jamil, E., Montgomery, E., Presani, E., Hahn, E., Wood, E., Brinkman, E., Arcaute, E., Dunbar, E., Smothers, E., Sun, F., Kreuk, F., Tian, F., Ozgenel, F., Caggioni, F., Guzmán, F., Kanayet, F., Seide, F., Florez, G. M., Schwarz, G., Badeer, G., Swee, G., Halpern, G., Thattai, G., Herman, G., Sizov, G., Guangyi, Zhang, Lakshminarayanan, G., Shojanazeri, H., Zou, H., Wang, H., Zha, H., Habeeb, H., Rudolph, H., Suk, H., Aspegren, H., Goldman, H., Molybog, I., Tufanov, I.,
  Veliche, I.-E., Gat, I., Weissman, J., Geboski, J., Kohli, J., Asher, J., Gaya, J.-B., Marcus, J., Tang, J., Chan, J., Zhen, J., Reizenstein, J., Teboul, J., Zhong, J., Jin, J., Yang, J., Cummings, J., Carvill, J., Shepard, J., McPhie, J., Torres, J., Ginsburg, J., Wang, J., Wu, K., U, K. H., Saxena, K., Prasad, K., Khandelwal, K., Zand, K., Matosich, K., Veeraraghavan, K., Michelena, K., Li, K., Huang, K., Chawla, K., Lakhotia, K., Huang, K., Chen, L., Garg, L., A, L., Silva, L., Bell, L., Zhang, L., Guo, L., Yu, L., Moshkovich, L., Wehrstedt, L., Khabsa, M., Avalani, M., Bhatt, M., Tsimpoukelli, M., Mankus, M., Hasson, M., Lennie, M., Reso, M., Groshev, M., Naumov, M., Lathi, M., Keneally, M., Seltzer, M. L., Valko, M., Restrepo, M., Patel, M., Vyatskov, M., Samvelyan, M., Clark, M., Macey, M., Wang, M., Hermoso, M. J., Metanat, M., Rastegari, M., Bansal, M., Santhanam, N., Parks, N., White, N., Bawa, N., Singhal, N., Egebo, N., Usunier, N., Laptev, N. P., Dong, N., Zhang, N., Cheng, N., Chernoguz, O.,
  Hart, O., Salpekar, O., Kalinli, O., Kent, P., Parekh, P., Saab, P., Balaji, P., Rittner, P., Bontrager, P., Roux, P., Dollar, P., Zvyagina, P., Ratanchandani, P., Yuvraj, P., Liang, Q., Alao, R., Rodriguez, R., Ayub, R., Murthy, R., Nayani, R., Mitra, R., Li, R., Hogan, R., Battey, R., Wang, R., Maheswari, R., Howes, R., Rinott, R., Bondu, S. J., Datta, S., Chugh, S., Hunt, S., Dhillon, S., Sidorov, S., Pan, S., Verma, S., Yamamoto, S., Ramaswamy, S., Lindsay, S., Lindsay, S., Feng, S., Lin, S., Zha, S. C., Shankar, S., Zhang, S., Zhang, S., Wang, S., Agarwal, S., Sajuyigbe, S., Chintala, S., Max, S., Chen, S., Kehoe, S., Satterfield, S., Govindaprasad, S., Gupta, S., Cho, S., Virk, S., Subramanian, S., Choudhury, S., Goldman, S., Remez, T., Glaser, T., Best, T., Kohler, T., Robinson, T., Li, T., Zhang, T., Matthews, T., Chou, T., Shaked, T., Vontimitta, V., Ajayi, V., Montanez, V., Mohan, V., Kumar, V. S., Mangla, V., Ionescu, V., Poenaru, V., Mihailescu, V. T., Ivanov, V., Li, W., Wang, W., Jiang, W.,
  Bouaziz, W., Constable, W., Tang, X., Wang, X., Wu, X., Wang, X., Xia, X., Wu, X., Gao, X., Chen, Y., Hu, Y., Jia, Y., Qi, Y., Li, Y., Zhang, Y., Zhang, Y., Adi, Y., Nam, Y., Yu, Wang, Hao, Y., Qian, Y., He, Y., Rait, Z., DeVito, Z., Rosnbrick, Z., Wen, Z., Yang, Z., and Zhao, Z.
  The llama 3 herd of models, 2024.
  URL <https://arxiv.org/abs/2407.21783>.
- [13]

  Guo, D., Zhu, Q., Yang, D., Xie, Z., Dong, K., Zhang, W., Chen, G., Bi, X., Wu, Y., Li, Y. K., Luo, F., Xiong, Y., and Liang, W.
  Deepseek-coder: When the large language model meets programming – the rise of code intelligence, 2024.
  URL <https://arxiv.org/abs/2401.14196>.
- [14]

  Hartford, E.
  dolphin-2.2.1-mistral-7b.
  January 2024.
- [15]

  Hendrycks, D., Burns, C., Kadavath, S., Arora, A., Basart, S., Tang, E., Song, D., and Steinhardt, J.
  Measuring mathematical problem solving with the math dataset.
  *arXiv preprint arXiv:2103.03874*, 2021.
- [16]

  Hinton, G. E. et al.
  *How neural networks learn from experience*.
  na, 1992.
- [17]

  Hu, S., Lu, C., and Clune, J.
  Automated design of agentic systems.
  *arXiv preprint arXiv:2408.08435*, 2024.
- [18]

  Jiang, A. Q., Sablayrolles, A., Mensch, A., Bamford, C., Chaplot, D. S., de las Casas, D., Bressand, F., Lengyel, G., Lample, G., Saulnier, L., Lavaud, L. R., Lachaux, M.-A., Stock, P., Scao, T. L., Lavril, T., Wang, T., Lacroix, T., and Sayed, W. E.
  Mistral 7b, 2023a.
- [19]

  Jiang, A. Q., Sablayrolles, A., Roux, A., Mensch, A., Savary, B., Bamford, C., Chaplot, D. S., de las Casas, D., Hanna, E. B., Bressand, F., Lengyel, G., Bour, G., Lample, G., Lavaud, L. R., Saulnier, L., Lachaux, M.-A., Stock, P., Subramanian, S., Yang, S., Antoniak, S., Scao, T. L., Gervet, T., Lavril, T., Wang, T., Lacroix, T., and Sayed, W. E.
  Mixtral of experts, 2024.
- [20]

  Jiang, D., Ren, X., and Lin, B. Y.
  Llm-blender: Ensembling large language models with pairwise comparison and generative fusion.
  In *Proceedings of the 61th Annual Meeting of the Association for Computational Linguistics (ACL 2023)*, 2023b.
- [21]

  Khattab, O., Singhvi, A., Maheshwari, P., Zhang, Z., Santhanam, K., Vardhamanan, S., Haq, S., Sharma, A., Joshi, T. T., Moazam, H., Miller, H., Zaharia, M., and Potts, C.
  Dspy: Compiling declarative language model calls into self-improving pipelines.
  *arXiv preprint arXiv:2310.03714*, 2023.
- [22]

  Li, J., Zhang, Q., Yu, Y., Fu, Q., and Ye, D.
  More agents is all you need, 2024a.
  URL <https://arxiv.org/abs/2402.05120>.
- [23]

  Li, T., Chiang, W.-L., Frick, E., Dunlap, L., Banghua Zhu, J. E. G., and Stoica, I.
  From live data to high-quality benchmarks: The arena-hard pipeline, April 2024b.
  URL <https://lmsys.org/blog/2024-04-19-arena-hard/>.
- [24]

  Li, X., Zhang, T., Dubois, Y., Taori, R., Gulrajani, I., Guestrin, C., Liang, P., and Hashimoto, T. B.
  Alpacaeval: An automatic evaluator of instruction-following models.
  <https://github.com/tatsu-lab/alpaca_eval>, 2023.
- [25]

  Li, Y., Choi, D., Chung, J., Kushman, N., Schrittwieser, J., Leblond, R., Eccles, T., Keeling, J., Gimeno, F., Dal Lago, A., et al.
  Competition-level code generation with alphacode.
  *Science*, 378(6624):1092–1097, 2022.
- [26]

  Meng, Y., Xia, M., and Chen, D.
  SimPO: Simple preference optimization with a reference-free reward.
  *ArXiv*, 2024.
- [27]

  Mialon, G., Fourrier, C., Swift, C., Wolf, T., LeCun, Y., and Scialom, T.
  Gaia: a benchmark for general ai assistants, 2023.
  URL <https://arxiv.org/abs/2311.12983>.
- [28]

  Nardi, L., Souza, A., Koeplinger, D., and Olukotun, K.
  Hypermapper: a practical design space exploration framework.
  In *2019 IEEE 27th International Symposium on Modeling, Analysis, and Simulation of Computer and Telecommunication Systems (MASCOTS)*, pp. 425–426, 2019.
  doi: 10.1109/MASCOTS.2019.00053.
- [29]

  Ni, J., Xue, F., Yue, X., Deng, Y., Shah, M., Jain, K., Neubig, G., and You, Y.
  Mixeval: Deriving wisdom of the crowd from llm benchmark mixtures, 2024.
  URL <https://arxiv.org/abs/2406.06565>.
- [30]

  OpenAI.
  Learning to reason with LLMs.
  <https://openai.com/research/learning-to-reason-with-llms>, September 2024.
  Accessed November 13, 2024.
- [31]

  OpenAI, Achiam, J., Adler, S., Agarwal, S., Ahmad, L., Akkaya, I., Aleman, F. L., Almeida, D., Altenschmidt, J., Altman, S., Anadkat, S., Avila, R., Babuschkin, I., Balaji, S., Balcom, V., Baltescu, P., Bao, H., Bavarian, M., Belgum, J., Bello, I., Berdine, J., Bernadett-Shapiro, G., Berner, C., Bogdonoff, L., Boiko, O., Boyd, M., Brakman, A.-L., Brockman, G., Brooks, T., Brundage, M., Button, K., Cai, T., Campbell, R., Cann, A., Carey, B., Carlson, C., Carmichael, R., Chan, B., Chang, C., Chantzis, F., Chen, D., Chen, S., Chen, R., Chen, J., Chen, M., Chess, B., Cho, C., Chu, C., Chung, H. W., Cummings, D., Currier, J., Dai, Y., Decareaux, C., Degry, T., Deutsch, N., Deville, D., Dhar, A., Dohan, D., Dowling, S., Dunning, S., Ecoffet, A., Eleti, A., Eloundou, T., Farhi, D., Fedus, L., Felix, N., Fishman, S. P., Forte, J., Fulford, I., Gao, L., Georges, E., Gibson, C., Goel, V., Gogineni, T., Goh, G., Gontijo-Lopes, R., Gordon, J., Grafstein, M., Gray, S., Greene, R., Gross, J., Gu, S. S., Guo, Y., Hallacy,
  C., Han, J., Harris, J., He, Y., Heaton, M., Heidecke, J., Hesse, C., Hickey, A., Hickey, W., Hoeschele, P., Houghton, B., Hsu, K., Hu, S., Hu, X., Huizinga, J., Jain, S., Jain, S., Jang, J., Jiang, A., Jiang, R., Jin, H., Jin, D., Jomoto, S., Jonn, B., Jun, H., Kaftan, T., Łukasz Kaiser, Kamali, A., Kanitscheider, I., Keskar, N. S., Khan, T., Kilpatrick, L., Kim, J. W., Kim, C., Kim, Y., Kirchner, J. H., Kiros, J., Knight, M., Kokotajlo, D., Łukasz Kondraciuk, Kondrich, A., Konstantinidis, A., Kosic, K., Krueger, G., Kuo, V., Lampe, M., Lan, I., Lee, T., Leike, J., Leung, J., Levy, D., Li, C. M., Lim, R., Lin, M., Lin, S., Litwin, M., Lopez, T., Lowe, R., Lue, P., Makanju, A., Malfacini, K., Manning, S., Markov, T., Markovski, Y., Martin, B., Mayer, K., Mayne, A., McGrew, B., McKinney, S. M., McLeavey, C., McMillan, P., McNeil, J., Medina, D., Mehta, A., Menick, J., Metz, L., Mishchenko, A., Mishkin, P., Monaco, V., Morikawa, E., Mossing, D., Mu, T., Murati, M., Murk, O., Mély, D., Nair, A., Nakano, R.,
  Nayak, R., Neelakantan, A., Ngo, R., Noh, H., Ouyang, L., O’Keefe, C., Pachocki, J., Paino, A., Palermo, J., Pantuliano, A., Parascandolo, G., Parish, J., Parparita, E., Passos, A., Pavlov, M., Peng, A., Perelman, A., de Avila Belbute Peres, F., Petrov, M., de Oliveira Pinto, H. P., Michael, Pokorny, Pokrass, M., Pong, V. H., Powell, T., Power, A., Power, B., Proehl, E., Puri, R., Radford, A., Rae, J., Ramesh, A., Raymond, C., Real, F., Rimbach, K., Ross, C., Rotsted, B., Roussez, H., Ryder, N., Saltarelli, M., Sanders, T., Santurkar, S., Sastry, G., Schmidt, H., Schnurr, D., Schulman, J., Selsam, D., Sheppard, K., Sherbakov, T., Shieh, J., Shoker, S., Shyam, P., Sidor, S., Sigler, E., Simens, M., Sitkin, J., Slama, K., Sohl, I., Sokolowsky, B., Song, Y., Staudacher, N., Such, F. P., Summers, N., Sutskever, I., Tang, J., Tezak, N., Thompson, M. B., Tillet, P., Tootoonchian, A., Tseng, E., Tuggle, P., Turley, N., Tworek, J., Uribe, J. F. C., Vallone, A., Vijayvergiya, A., Voss, C., Wainwright, C., Wang,
  J. J., Wang, A., Wang, B., Ward, J., Wei, J., Weinmann, C., Welihinda, A., Welinder, P., Weng, J., Weng, L., Wiethoff, M., Willner, D., Winter, C., Wolrich, S., Wong, H., Workman, L., Wu, S., Wu, J., Wu, M., Xiao, K., Xu, T., Yoo, S., Yu, K., Yuan, Q., Zaremba, W., Zellers, R., Zhang, C., Zhang, M., Zhao, S., Zheng, T., Zhuang, J., Zhuk, W., and Zoph, B.
  Gpt-4 technical report, 2024.
  URL <https://arxiv.org/abs/2303.08774>.
- [32]

  Qwen.
  Qwen2 technical report.
  2024.
- [33]

  Rein, D., Hou, B. L., Stickland, A. C., Petty, J., Pang, R. Y., Dirani, J., Michael, J., and Bowman, S. R.
  Gpqa: A graduate-level google-proof qa benchmark, 2023.
  URL <https://arxiv.org/abs/2311.12022>.
- [34]

  Rein, D., Hou, B. L., Stickland, A. C., Petty, J., Pang, R. Y., Dirani, J., Michael, J., and Bowman, S. R.
  GPQA: A graduate-level google-proof qa benchmark.
  In *First Conference on Language Modeling*, 2024.
  URL <https://openreview.net/forum?id=Ti67584b98>.
- [35]

  Ren, P., Xiao, Y., Chang, X., Huang, P.-Y., Li, Z., Chen, X., and Wang, X.
  A comprehensive survey of neural architecture search: Challenges and solutions.
  *ACM Computing Surveys (CSUR)*, 54(4):1–34, 2021.
- [36]

  Snoek, J., Larochelle, H., and Adams, R. P.
  Practical bayesian optimization of machine learning algorithms, 2012.
  URL <https://arxiv.org/abs/1206.2944>.
- [37]

  Sreenivas, S. T., Muralidharan, S., Joshi, R., Chochowski, M., Patwary, M., Shoeybi, M., Catanzaro, B., Kautz, J., and Molchanov, P.
  Llm pruning and distillation in practice: The minitron approach, 2024.
  URL <https://arxiv.org/abs/2408.11796>.
- [38]

  Team, N.
  Sky-t1: Train your own o1 preview model within 450.
  https://novasky-ai.github.io/posts/sky-t1, 2025.
  Accessed: 2025-01-09.
- [39]

  Team, Q.
  Qwq: Reflect deeply on the boundaries of the unknown, November 2024.
  URL <https://qwenlm.github.io/blog/qwq-32b-preview/>.
- [40]

  Tran, H., Glaze, C., and Hancock, B.
  Iterative dpo alignment.
  Technical report, Snorkel AI, 2023.
- [41]

  Tunstall, L., Beeching, E., Lambert, N., Rajani, N., Rasul, K., Belkada, Y., Huang, S., von Werra, L., Fourrier, C., Habib, N., et al.
  Zephyr: Direct distillation of lm alignment.
  *arXiv preprint arXiv:2310.16944*, 2023.
- [42]

  Wang, J., Wang, J., Athiwaratkun, B., Zhang, C., and Zou, J.
  Mixture-of-agents enhances large language model capabilities, 2024a.
  URL <https://arxiv.org/abs/2406.04692>.
- [43]

  Wang, Y., Ma, X., Zhang, G., Ni, Y., Chandra, A., Guo, S., Ren, W., Arulraj, A., He, X., Jiang, Z., et al.
  Mmlu-pro: A more robust and challenging multi-task language understanding benchmark.
  *arXiv preprint arXiv:2406.01574*, 2024b.
- [44]

  Xu, C., Sun, Q., Zheng, K., Geng, X., Zhao, P., Feng, J., Tao, C., Lin, Q., and Jiang, D.
  WizardLM: Empowering large pre-trained language models to follow complex instructions.
  In *The Twelfth International Conference on Learning Representations*, 2024.
  URL <https://openreview.net/forum?id=CfXh93NDgH>.
- [45]

  Yuksekgonul, M., Bianchi, F., Boen, J., Liu, S., Huang, Z., Guestrin, C., and Zou, J.
  Textgrad: Automatic "differentiation" via text.
  2024.
- [46]

  Zhang, J., Xiang, J., Yu, Z., Teng, F., Chen, X., Chen, J., Zhuge, M., Cheng, X., Hong, S., Wang, J., Zheng, B., Liu, B., Luo, Y., and Wu, C.
  Aflow: Automating agentic workflow generation, 2024.
  URL <https://arxiv.org/abs/2410.10762>.
- [47]

  Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., and Stoica, I.
  Judging llm-as-a-judge with mt-bench and chatbot arena, 2023.
- [48]

  Zoph, B. and Le, Q. V.
  Neural architecture search with reinforcement learning, 2017.
  URL <https://arxiv.org/abs/1611.01578>.

## 附录 A

### A.1 目录

1. Archon LLM 组件：概述 Archon 使用的 LM 组件及组合它们的规则
2. LLM 组件的效用与交互：分析单个组件的有效性及其组合时的协同效应
3. Archon 的贝叶斯优化：描述用于架构发现的搜索空间与优化方法
4. 贝叶斯优化对比替代方法：对寻找最优配置的搜索技术做比较分析
5. Archon 架构算法比较：在不同推理预算下评估不同优化策略
6. Archon 基准与结果：覆盖指令遵循、推理与编程任务的全面评估结果
7. Archon LLM 分析：所测模型的参数量与序列长度等细节
8. Archon 架构：不同任务类别优化架构的图示与描述
9. 按推理计算预算、模型规模与成本看 Archon：分析不同计算约束与模型规模下的表现

### A.2 Archon LLM 组件

| 推理时技术 | 定义 | 输入 | 输出 | 推理成本 | 适用领域 |
| --- | --- | --- | --- | --- | --- |
| 生成器 | 从指令提示生成候选回答 | 指令提示 | 候选回答 | 每候选 1 次调用 | 所有领域 |
| 融合器 | 把多个候选回答合并为单个回答 | 指令提示 + 候选回答 | 融合后的候选回答 | 每候选 1 次调用 | 所有领域 |
| 批评器 | 为每个候选回答生成优缺点 | 指令提示 + 候选回答 | 候选回答 + 优缺点 | 每候选 1 次调用 | 所有领域 |
| 排序器 | 返回 top-K 候选回答 | 指令提示 + 候选回答 | 排序后的候选回答 | 每候选 1 次调用 | 所有领域 |
| 验证器 | 返回通过推理验证的候选回答 | 指令提示 + 候选回答 | 通过验证的候选回答 | 每候选 2 次调用 | 推理任务 |
| 单元测试生成器 | 生成用于评估候选回答的单元测试 | 指令提示 | 指令提示 + 单元测试 | 1 次调用 | 推理任务 |
| 单元测试评估器 | 用生成的单元测试评估候选回答 | 指令提示 + 单元测试 + 候选回答 | 打分后的候选回答 | 每候选 1 次调用 | 推理任务 |

表 3：Archon 推理时技术概览：定义、输入、输出、成本与应用领域。

| 模块 | 可作初始层 | 初始层之后的放置 | 层内可 >1 个模块 | 增加候选回答 | 减少候选回答 |
| --- | --- | --- | --- | --- | --- |
| 生成器 | 是 | 否 | 是 | 是 | 否 |
| 融合器 | 否 | 是 | 是 | 是 | 是 |
| 排序器 | 否 | 是 | 否 | 否 | 是 |
| 批评器 | 否 | 是 | 否 | 否 | 否 |
| 验证器 | 否 | 是 | 否 | 否 | 是 |
| 单元测试生成器 | 否 | 是 | 否 | 否 | 否 |
| 单元测试评估器 | 否 | 是 | 否 | 否 | 否 |

表 4：Archon 构建规则：第 3.1 节各 LLM 组件允许的组合。

### A.3 LLM 组件的效用与交互

![Refer to caption](2409.15254v6/figures/sampling_graph.png)

图 6：在单个模型上应用推理时技术带来的性能增益：我们对每个查询重复采样更多回答。对每个样本数，我们用 5 种方式选出最佳回答：(1) 使用 oracle（获得最佳样本表现的上界）；(2) 随机；(3) 使用排序器模型；(4) 融合——由一个模型基于全部样本合成一个回答；(5) 先把最佳的 top-5 回答排序再融合。对 MT Bench 与 Arena-Hard-Auto，我们发现融合是有效技术。特别地，先对候选排序、再选 top-5 并融合的得分最高。这些任务在全部 70B+ 模型中表现最好的开源模型是 WizardLM-2-8x22B（Xu et al.）（细节见表 35）。排序与融合均使用 Qwen2 72B Instruct（Qwen, 2024）。

在本小节中，我们通过在指令遵循任务（MT Bench、AlpacaEval 2.0、Arena-Hard-Auto）、推理任务（MixEval、MixEval-Hard、MATH）与编程任务（CodeContests）上的评估，呈现我们对每个 LLM 组件（即效用）与各组件之间关系（即组件交互）的分析（第 4.1 节）。对 Archon 模型，我们使用一批 70B+ 开源模型（第 4.1 节；表 34）。

#### A.3.1 生成器

效用：对我们的生成器模块，我们发现额外的模型采样显著提升表现（图 6），尤其对编程任务（表 1）。在推理调用预算有限的设置中，额外的模型样本带来最大的边际收益。模型集成也有类似模式：从更多模型采样带来持续的性能增长（假设模型按给定任务从好到差排序）（图 7）。

#### A.3.2 融合器

效用：在我们探索的每个基准上，Fuser 模块都大幅提升表现（图 6；图 7；图 4）。对 70B+ 模型的单次生成 10 模型集成，Fuser 模块相对单次生成的最佳模型平均把下游准确率提高 5.2 个点（图 7）。当与排序 top-5 候选回答的 Ranker 模块组合时，Fuser 相对单样本最佳模型与 oracle 最佳候选分别平均提高 7.3 与 3.6 个点（图 7）。总体而言，我们发现提供的候选回答越多，Fuser 的效力越强，这表明与 Fuser 结合时，额外的候选生成能持续增强推理时架构的表现。

在 MoA（Wang et al., 2024a）等先前工作中，多层 Fuser 被发现能提升某些指令遵循任务（即 MT Bench 与 Alpaca Eval 2.0）的表现。在我们探索的所有基准上，我们在 Archon 框架中添加多层 Fuser 时观察到类似收益（图 4）。然而，基于图 12 的结果，改进表现所需的 Fuser 层数因任务而异：一些任务从增加的层中收益有限（MixEval 准确率提高 1-2 个点），而另一些任务在 3-4 层及以上融合时收益显著（MT Bench 与 Alpaca Eval 2.0 的胜率提高 2 到 5 个点）。我们把这一差异归因于任务需求的不同：聊天与指令遵循任务更能从多个 Fuser 层的多次修订迭代中受益，从而使最终生成具有更大的多样性（表 36）。

![Refer to caption](2409.15254v6/figures/Ensembling_Graph.png)

图 7：在模型集成上应用推理时技术带来的性能增益：我们逐步向集成添加更多模型（由开源 70B+ 模型组成）。模型按其在每个任务上的表现从好到差加入池中（细节见表 35）。对每个集成规模，我们用 5 种模式选出最佳回答：(1) 使用 oracle（获得集成中最佳单回答表现的上界）；(2) 随机；(3) 使用排序器模型；(4) 融合——由一个模型基于集成模型的全部回答合成一个回答；(5) 先把最佳的 top-5 回答排序再融合。对 MT Bench 与 Arena-Hard-Auto，随着向集成添加更多模型，我们发现一致的性能改进。我们发现融合在各种集成规模下都有益，特别是基于 top-5 排序回答的融合候选得分最高。集成方法比在单个最佳表现模型上重复采样应用相同技术得分更高（见图 6）。排序与融合均使用 Qwen2 72B Instruct（Qwen, 2024）。

组件交互：为更好理解 Fuser 模块与其他 LLM 组件的协作，我们取「单样本 10 模型生成器集成 + 一个 Fuser」的配置，并尝试逐个添加以下组件：Critic、Ranker、Verifier 与单元测试生成器/评估器。在所有基准上，Critic 提供的额外候选回答分析改进了 Fuser 有效合并不同候选回答的能力，平均提升 3.1 个百分点（图 4）。加上 Ranker 后，Archon 架构在所有基准上把「集成 + Critic + Fuser」的表现平均再提高 4.8 个百分点（图 4）。Ranker 对风格导向的任务（如 MT Bench 与 AlpacaEval 2.0）最有效，因为这些例子主要聚焦于改进对所给提示的指令遵循。加上 Verifier 模块（图 4）后，「集成 + Critic + Fuser」配置在指令遵循任务上小幅改进（MT Bench、AlpacaEval 2.0 与 Arena-Hard-Auto 平均 1.2 个百分点）。但该配置在推理任务上改进更多（MixEval 与 MixEval-Hard 平均 3.2 个百分点），它通过在最终融合步骤前过滤无关或有缺陷的答案来辅助生成（图 4）。添加的单元测试生成器与评估器对指令遵循与推理任务效果较差，加入「集成 + Critic + Fuser」配置后平均只提高 1.5 个百分点（表 5）。然而，对编程任务，我们发现单元测试生成与评估显著改进表现：随着扩展模型采样，带来 10.7 个百分点的提升（相对提升 56%）（表 1）。

#### A.3.3 批评器

效用：Critic 模块对我们在图 4 与表 5 中探索的每个任务都有效。在我们 10 模型 70B+ 生成器集成加 Fuser 的 Archon 配置上，添加 Critic 在所探索基准上平均提升 3.1 个百分点。

组件交互：虽然对多数 Archon 架构都有用，但 Critic 模块提供的优缺点与 Fuser 模块组合时尤其有用，能引导单层的生成融合，甚至放在多个融合层之间也有用（图 4 的基准上平均提升 3.2 个百分点）。Critic 模块与 Ranker 模块组合也有效，为比较候选回答提供额外信息（图 6），平均带来 5.9 个百分点的提升（表 5）。

#### A.3.4 排序器

效用：从表 5、图 6 与图 7 的结果看，我们发现 Ranker 对指令遵循任务最有效，答案的成对比较聚焦于风格与对提示的遵循。为考察候选排序带来的候选选择改进，我们比较三种 Ranker 方法：(1) 随机选择候选生成，(2) oracle 选择候选生成，(3) 我们的 Ranker 选出的最高排名候选。对 MT Bench 与 Arena-Hard-Auto，我们发现排序器相对随机候选选择把生成输出质量提升 3.8%，且与 oracle 选择相差不到 2.7%（图 6）。

组件交互：基于表 5 的基准结果，Ranker 与 Critic 模块搭配良好；提供的优缺点帮助引导排序，尤其对指令遵循任务，平均提升 5.9 个百分点。此外，Ranker 与 Fuser 搭配也有效；过滤后的候选回答列表帮助改进 Fuser 产出的最终浓缩回答，平均提升 3.8 个百分点（图 7）。与 Verifier 和单元测试生成器搭配时，Ranker 的效果呈中性；表现变化在正负 1-2 个百分点之间（表 5）。

总体而言，我们的发现证明了为指令遵循与推理任务搭配 Fuser 时添加 Ranker 的价值。我们发现当 Ranker 单独与生成器集成一起使用时，其表现平均落后 10 样本最佳单模型配置 3.0 个百分点（表 5）。此外，我们的发现表明为数学与编程等更复杂的推理任务构建更好的排序器十分重要，这也是 Brown et al. (2024) 提出的挑战。

| 模型 / LLM 系统 | 推理调用数 | MT Bench W.R. | AlpacaEval 2.0 L.C. W.R. | Arena-Hard-Auto W.R. | MixEval-Hard W.R. | MixEval Acc. | MATH Acc. | CodeContests Acc. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 对照：最佳开源 70B+ 模型，采样一次 | 1 | 55.0% ±0.4 | 44.7% ±0.5 | 37.1% ±0.6 | 45.6% ±0.5 | 58.7% ±0.2 | 86.5% ±0.3 | 84.5% ±0.6 | 22.5% ±0.3 |
| 集成 + 融合器 | 9 | 58.4% ±0.6 | 57.5% ±0.4 | 51.3% ±0.5 | 54.3% ±0.7 | 60.1% ±0.5 | 87.3% ±0.2 | 85.5% ±0.3 | 23.1% ±0.7 |
| 集成 + 批评器 + 融合器 | 10 | 60.9% ±0.3 | 58.7% ±0.6 | 65.8% ±0.3 | 58.8% ±0.4 | 61.7% ±0.5 | 87.4% ±0.3 | 87.2% ±0.5 | 24.9% ±0.4 |
| 消融：集成 + 排序器 | 9 | 52.5% ±0.7 | 54.7% ±0.5 | 47.6% ±0.4 | 50.5% ±0.6 | 58.7% ±0.3 | 86.8% ±0.4 | 80.4% ±0.4 | 24.1% ±0.4 |
| 集成 + 验证器 | 24 | 53.2% ±0.5 | 56.2% ±0.3 | 50.2% ±0.7 | 52.4% ±0.3 | 55.9% ±0.5 | 85.6% ±0.2 | 85.2% ±0.7 | 25.3% ±0.5 |
| 集成 + 单元测试生成/评估 | 18 | 51.5% ±0.4 | 54.4% ±0.6 | 49.4% ±0.5 | 46.1% ±0.8 | 55.2% ±0.4 | 86.0% ±0.3 | 85.2% ±0.5 | 24.6% ±0.6 |
| 集成 + 排序器 + 融合器 | 10 | 62.5% ±0.8 | 60.3% ±0.4 | 63.6% ±0.6 | 57.2% ±0.5 | 59.7% ±0.2 | 87.6% ±0.3 | 85.3% ±0.6 | 24.0% ±0.2 |
| 集成 + 验证器 + 融合器 | 25 | 60.5% ±0.3 | 59.4% ±0.7 | 58.7% ±0.3 | 59.2% ±0.4 | 68.3% ±0.3 | 87.5% ±0.2 | 86.7% ±0.4 | 26.3% ±0.6 |
| 集成 + 单元测试生成/评估 + 融合器 | 17 | 61.4% ±0.6 | 58.5% ±0.5 | 55.1% ±0.4 | 56.4% ±0.7 | 63.9% ±0.3 | 86.9% ±0.3 | 86.4% ±0.8 | 28.0% ±0.6 |
| 集成 + 批评器 + 验证器 + 融合器 | 25 | 61.3% ±0.5 | 60.0% ±0.3 | 61.0% ±0.7 | 59.5% ±0.3 | 65.8% ±0.4 | 87.8% ±0.4 | 86.1% ±0.3 | 26.8% ±0.3 |
| 集成 + 批评器 + 排序器 + 融合器 | 11 | 64.7% ±0.4 | 62.6% ±0.6 | 72.4% ±0.5 | 60.9% ±0.6 | 66.8% ±0.4 | 88.3% ±0.2 | 87.3% ±0.5 | 25.5% ±0.3 |

表 5：不同 Archon 推理时技术组合的影响：我们看到向 Archon 添加新的 LLM 组件带来任务表现的提升。对 CodeContests，我们发现存在单个模型（Llama 3.1 405B Instruct）的表现显著优于其余 LLM，使额外的模型采样更有效（表 1）。对我们的集成，我们使用该任务最佳的开源 70B+ 模型中的前 8 个（表 35）。对我们的融合器、批评器、排序器与验证器组件，我们使用该任务找到的最佳融合模型（表 35）。对每个评估基准，我们在表 28 与第 4.1 节解释其配置。标准误由 10 次独立评估运行计算。

| 模型 / LLM 系统 | 推理调用数 | MT Bench W.R. | AlpacaEval 2.0 L.C. W.R. | Arena-Hard-Auto W.R. | MixEval-Hard W.R. | MixEval Acc. | MATH Acc. | CodeContests Acc. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 对照：单次生成 | 1 | 44.2% ±0.6 | 57.8% ±0.5 | 48.1% ±0.7 | 63.4% ±0.3 | 87.5% ±0.2 | 82.1% ±0.4 | 17.9% ±0.3 |
| 集成 + 融合器 | 11 | 53.7% ±0.3 | 59.5% ±0.6 | 49.7% ±0.5 | 65.5% ±0.2 | 82.0% ±0.3 | 81.0% ±0.6 | 16.0% ±0.4 |
| 集成 + 批评器 + 融合器 | 12 | 56.1% ±0.7 | 59.7% ±0.4 | 53.9% ±0.6 | 67.4% ±0.4 | 82.0% ±0.2 | 82.3% ±0.5 | 18.9% ±0.6 |
| 消融：集成 + 排序器 | 11 | 47.6% ±0.4 | 49.7% ±0.5 | 45.5% ±0.4 | 63.3% ±0.3 | 81.6% ±0.4 | 77.3% ±0.7 | 17.9% ±0.5 |
| 集成 + 验证器 | 11 | 48.4% ±0.5 | 51.2% ±0.7 | 47.7% ±0.8 | 61.4% ±0.2 | 80.5% ±0.3 | 75.5% ±0.3 | 23.0% ±0.4 |
| 集成 + 单元测试生成/评估 | 21 | 46.8% ±0.8 | 49.3% ±0.3 | 41.2% ±0.5 | 60.2% ±0.4 | 80.7% ±0.2 | 78.9% ±0.8 | 24.0% ±0.7 |
| 集成 + 排序器 + 融合器 | 12 | 58.0% ±0.2 | 60.1% ±0.6 | 52.2% ±0.3 | 65.0% ±0.3 | 82.0% ±0.4 | 82.1% ±0.4 | 18.0% ±0.3 |
| 集成 + 验证器 + 融合器 | 12 | 55.8% ±0.6 | 54.2% ±0.4 | 60.3% ±0.7 | 67.0% ±0.2 | 82.5% ±0.3 | 83.1% ±0.6 | 22.4% ±0.5 |
| 集成 + 单元测试生成/评估 + 融合器 | 22 | 56.5% ±0.3 | 61.4% ±0.5 | 51.6% ±0.4 | 67.7% ±0.4 | 81.7% ±0.2 | 84.3% ±0.5 | 25.4% ±0.6 |
| 集成 + 批评器 + 验证器 + 融合器 | 13 | 56.6% ±0.7 | 62.0% ±0.3 | 55.0% ±0.6 | 68.5% ±0.3 | 82.7% ±0.4 | 85.7% ±0.3 | 22.2% ±0.4 |
| 集成 + 批评器 + 排序器 + 融合器 | 13 | 60.0% ±0.4 | 62.8% ±0.6 | 56.2% ±0.5 | 69.4% ±0.2 | 88.5% ±0.3 | 87.0% ±0.7 | 18.5% ±0.5 |

表 6：用 GPT-4o 的 Archon 组件组合：该集成为给定查询生成 10 个样本。标准误由 10 次独立评估运行计算。

| 模型 / LLM 系统 | 推理调用数 | MT Bench W.R. | AlpacaEval 2.0 L.C. W.R. | Arena-Hard-Auto W.R. | MixEval-Hard W.R. | MixEval Acc. | MATH Acc. | CodeContests Acc. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 对照：单次生成 | 1 | 32.1% ±0.7 | 38.5% ±0.5 | 30.4% ±0.6 | 45.2% ±0.3 | 69.5% ±0.2 | 72.3% ±0.5 | 10.5% ±0.6 |
| 集成 + 融合器 | 11 | 44.2% ±0.3 | 43.0% ±0.6 | 40.2% ±0.4 | 46.0% ±0.4 | 73.0% ±0.3 | 70.5% ±0.7 | 6.0% ±0.4 |
| 集成 + 批评器 + 融合器 | 12 | 46.6% ±0.5 | 44.2% ±0.4 | 44.4% ±0.7 | 47.9% ±0.2 | 73.0% ±0.4 | 72.5% ±0.3 | 8.4% ±0.5 |
| 消融：集成 + 排序器 | 11 | 38.1% ±0.6 | 40.2% ±0.7 | 36.0% ±0.5 | 43.8% ±0.3 | 72.1% ±0.2 | 66.2% ±0.6 | 7.5% ±0.4 |
| 集成 + 验证器 | 11 | 38.9% ±0.4 | 41.7% ±0.3 | 38.2% ±0.8 | 41.9% ±0.4 | 71.0% ±0.3 | 68.5% ±0.4 | 19.0% ±0.7 |
| 集成 + 单元测试生成/评估 | 21 | 37.3% ±0.8 | 39.8% ±0.6 | 31.7% ±0.3 | 40.7% ±0.2 | 71.2% ±0.4 | 69.8% ±0.8 | 22.0% ±0.3 |
| 集成 + 排序器 + 融合器 | 12 | 48.0% ±0.2 | 45.6% ±0.5 | 42.7% ±0.6 | 45.0% ±0.3 | 73.0% ±0.2 | 70.1% ±0.5 | 8.0% ±0.6 |
| 集成 + 验证器 + 融合器 | 12 | 46.3% ±0.5 | 44.7% ±0.4 | 45.0% ±0.4 | 50.5% ±0.4 | 73.0% ±0.3 | 71.3% ±0.3 | 18.6% ±0.5 |
| 集成 + 单元测试生成/评估 + 融合器 | 22 | 47.0% ±0.3 | 43.9% ±0.7 | 42.1% ±0.7 | 48.2% ±0.2 | 72.2% ±0.4 | 73.1% ±0.6 | 23.5% ±0.4 |
| 集成 + 批评器 + 验证器 + 融合器 | 13 | 47.1% ±0.7 | 46.0% ±0.3 | 45.0% ±0.5 | 52.4% ±0.3 | 73.2% ±0.5 | 74.1% ±0.4 | 18.4% ±0.7 |
| 集成 + 批评器 + 排序器 + 融合器 | 13 | 50.5% ±0.4 | 48.3% ±0.6 | 46.7% ±0.3 | 55.1% ±0.4 | 73.7% ±0.3 | 76.4% ±0.5 | 8.1% ±0.5 |

表 7：用 GPT-4o-mini 的 Archon 组件组合：该集成为给定查询生成 10 个样本。标准误由 10 次独立评估运行计算。

| 模型 / LLM 系统 | 推理调用数 | MT Bench W.R. | AlpacaEval 2.0 L.C. W.R. | Arena-Hard-Auto W.R. | MixEval-Hard W.R. | MixEval Acc. | MATH Acc. | CodeContests Acc. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 对照：单次生成 | 1 | N/A | 52.7% ±0.4 | 81.4% ±0.6 | 68.7% ±0.3 | 89.1% ±0.2 | 83.5% ±0.5 | 12.5% ±0.3 |
| 集成 + 融合器 | 11 | N/A | 53.0% ±0.6 | 83.2% ±0.4 | 69.5% ±0.2 | 89.0% ±0.3 | 81.8% ±0.6 | 17.0% ±0.4 |
| 集成 + 批评器 + 融合器 | 12 | N/A | 54.2% ±0.3 | 85.4% ±0.7 | 70.9% ±0.4 | 89.5% ±0.2 | 82.6% ±0.4 | 19.4% ±0.6 |
| 消融：集成 + 排序器 | 11 | N/A | 50.2% ±0.5 | 85.7% ±0.5 | 63.8% ±0.3 | 82.1% ±0.4 | 80.2% ±0.7 | 18.5% ±0.5 |
| 集成 + 验证器 | 11 | N/A | 51.7% ±0.7 | 78.2% ±0.3 | 60.9% ±0.2 | 81.0% ±0.3 | 80.1% ±0.3 | 21.0% ±0.4 |
| 集成 + 单元测试生成/评估 | 21 | N/A | 49.8% ±0.4 | 71.7% ±0.8 | 59.0% ±0.2 | 81.2% ±0.2 | 80.9% ±0.8 | 22.0% ±0.7 |
| 集成 + 排序器 + 融合器 | 12 | N/A | 55.6% ±0.5 | 82.7% ±0.4 | 65.0% ±0.3 | 89.0% ±0.4 | 82.4% ±0.4 | 19.0% ±0.3 |
| 集成 + 验证器 + 融合器 | 12 | N/A | 54.7% ±0.3 | 85.0% ±0.6 | 70.5% ±0.2 | 89.3% ±0.3 | 84.1% ±0.6 | 21.6% ±0.5 |
| 集成 + 单元测试生成/评估 + 融合器 | 22 | N/A | 53.9% ±0.6 | 82.1% ±0.5 | 68.2% ±0.4 | 89.2% ±0.2 | 82.0% ±0.5 | 23.5% ±0.6 |
| 集成 + 批评器 + 验证器 + 融合器 | 13 | N/A | 56.0% ±0.4 | 85.0% ±0.3 | 71.0% ±0.3 | 89.4% ±0.4 | 83.1% ±0.3 | 21.4% ±0.4 |
| 集成 + 批评器 + 排序器 + 融合器 | 13 | N/A | 58.3% ±0.5 | 86.7% ±0.7 | 73.0% ±0.2 | 89.7% ±0.3 | 85.3% ±0.7 | 19.1% ±0.5 |

表 8：用 Claude 3.5 Sonnet 的 Archon 组件组合：该集成为给定查询生成 10 个样本。标准误由 10 次独立评估运行计算。

| 模型 / LLM 系统 | 推理调用数 | MT Bench W.R. | AlpacaEval 2.0 L.C. W.R. | Arena-Hard-Auto W.R. | MixEval-Hard W.R. | MixEval Acc. | MATH Acc. | CodeContests Acc. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 对照：单次生成 | 1 | 35.0% ±0.5 | 42.0% ±0.6 | 36.8% ±0.7 | 64.6% ±0.2 | 73.2% ±0.3 | 74.3% ±0.4 | 10.0% ±0.5 |
| 集成 + 融合器 | 11 | 48.2% ±0.3 | 47.0% ±0.4 | 44.2% ±0.5 | 66.5% ±0.3 | 77.0% ±0.2 | 75.1% ±0.7 | 10.8% ±0.3 |
| 集成 + 批评器 + 融合器 | 12 | 50.6% ±0.7 | 48.2% ±0.5 | 48.4% ±0.3 | 68.1% ±0.4 | 77.0% ±0.4 | 76.3% ±0.5 | 11.5% ±0.6 |
| 消融：集成 + 排序器 | 11 | 42.1% ±0.4 | 44.2% ±0.7 | 40.0% ±0.6 | 58.8% ±0.3 | 76.1% ±0.2 | 71.8% ±0.6 | 11.9% ±0.4 |
| 集成 + 验证器 | 11 | 42.9% ±0.6 | 45.7% ±0.3 | 42.2% ±0.8 | 57.9% ±0.2 | 75.0% ±0.3 | 70.5% ±0.4 | 12.0% ±0.7 |
| 集成 + 单元测试生成/评估 | 21 | 41.3% ±0.8 | 43.8% ±0.6 | 35.7% ±0.4 | 55.7% ±0.4 | 75.2% ±0.2 | 74.1% ±0.8 | 13.0% ±0.3 |
| 集成 + 排序器 + 融合器 | 12 | 52.0% ±0.2 | 49.6% ±0.5 | 46.7% ±0.7 | 60.0% ±0.3 | 77.0% ±0.4 | 75.0% ±0.5 | 12.0% ±0.6 |
| 集成 + 验证器 + 融合器 | 12 | 50.3% ±0.5 | 48.7% ±0.4 | 48.7% ±0.5 | 67.5% ±0.2 | 77.0% ±0.3 | 77.4% ±0.3 | 10.5% ±0.5 |
| 集成 + 单元测试生成/评估 + 融合器 | 22 | 51.0% ±0.3 | 47.9% ±0.7 | 46.1% ±0.6 | 64.2% ±0.4 | 76.2% ±0.2 | 78.3% ±0.6 | 14.3% ±0.4 |
| 集成 + 批评器 + 验证器 + 融合器 | 13 | 51.1% ±0.7 | 50.0% ±0.3 | 49.0% ±0.4 | 68.0% ±0.3 | 77.2% ±0.4 | 77.8% ±0.3 | 10.0% ±0.7 |
| 集成 + 批评器 + 排序器 + 融合器 | 13 | 54.5% ±0.4 | 52.3% ±0.6 | 50.7% ±0.3 | 70.4% ±0.2 | 77.7% ±0.3 | 80.5% ±0.5 | 11.5% ±0.5 |

表 9：用 Claude-3-Haiku 的 Archon 组件组合：该集成为给定查询生成 10 个样本。标准误由 10 次独立评估运行计算。

#### A.3.5 验证器

效用：Verifier 对表 5 中探索的推理基准最有效。当只使用 70B+ 生成器集成并在生成后加 Verifier 模块时，该 Archon 配置在所有探索基准上平均落后于 Archon 集成加融合器配置 1.5 个百分点。这提示 Verifier 与其他推理时技术结合时最有效。

组件交互：如 A.3.2 节所述，Verifier 在推理任务（如 Arena-Hard-Auto、MixEval、MixEval-Hard）上增强了 Critic 与 Fuser 的表现，与这些模块组合时平均提升 3.7 个百分点。总体而言，Verifier 在为需要验证中间步骤与最终回答的任务增强其他组件时最强大（表 5）。因此，Verifier 对指令遵循任务（如 MT Bench 与 AlpacaEval）帮助较小，但对推理任务（如 Arena-Hard-Auto 与 MixEval）更有效。

#### A.3.6 单元测试生成器与评估器

效用：单元测试生成器与评估器对推理与编程任务最有效，能改进需要更多验证步骤的基准上的表现，如 Arena-Hard-Auto、MixEval、MixEval-Hard、MATH 与 CodeContests（表 5）。对推理任务，我们发现单元测试生成器与评估器与其他组件组合时最有效。当 70B+ 生成器集成只与单元测试组合时，它对 Arena-Hard-Auto 与 MixEval 等推理任务效果较差，落后集成加融合器配置 3.1 个百分点。这促使我们研究单元测试生成的其他推理时技术组合，如增加采样与融合。当我们增加生成采样并为 CodeContests 添加单元测试生成/评估时，我们看到 Pass@1 性能提升 56%（表 1），从 17.9 提升到 29.3 Pass@1。

组件交互：与 Fuser 模块组合时，单元测试生成器与评估器在所探索基准上改进表现 2.1 个百分点（表 5）。「集成 + 单元测试生成器/评估器 + 融合器」的 Archon 组合配置对推理基准最有效，平均带来 2.5 个百分点的提升。对编程，单元测试生成器与评估器与（使用大样本数的）最佳表现生成器及最终融合器组合时最有效（第 4.2 节）。

图 8：Archon 的表现在各 token 预算下超过基线：在不同 token 预算下（第 3.3 节），我们把 Archon 架构与表现最好的推理时系统基线比较。MoA 架构与 OpenAI 的 o1 是静态的，因此它们在各预算下使用相同数量的 token。结果为 10 次独立评估运行的平均。∗MATH 与 CodeContests 使用其测试集的子集进行评估（第 4.1 节）。

![Refer to caption](2409.15254v6/figures/Dollars_per_Query_vs_Performance.png)

图 9：Archon 的表现在各每查询美元预算下超过基线：在不同每查询美元预算下（第 3.3 节），我们把 Archon 架构与表现最好的推理时系统基线比较。MoA 架构与 OpenAI 的 o1 是静态的，因此它们在各预算下使用相同数量的 token。结果为 10 次独立评估运行的平均。∗MATH 与 CodeContests 使用其测试集的子集进行评估（第 4.1 节）。

|  |
| --- |
| <instruction here>. |

表 10：生成器提示

|  |
| --- |
| You have been provided with a set of responses with their individual critiques of strengths/weaknesses from various open-source models to the latest user query. Your task is to synthesize these responses into a single, high-quality response. It is crucial to critically evaluate the information provided in these responses and their provided critiques of strengths/weaknesses, recognizing that some of it may be biased or incorrect. Your response should not simply replicate the given answers but should offer a refined, accurate, and comprehensive reply to the instruction. Ensure your response is well-structured, coherent, and adheres to the highest standards of accuracy and reliability.  Responses from models:  1. <response #1>   Critique: <critique #1>   2. <response #2>   Critique: <critique #2>   ...   N. <response #N>   Critique: <critique #N>   <instruction here> |

表 11：带批评

|  |
| --- |
| You have been provided with a set of responses from various open-source models to the latest user query. Your task is to synthesize these responses into a single, high-quality response. It is crucial to critically evaluate the information provided in these responses, recognizing that some of it may be biased or incorrect. Your response should not simply replicate the given answers but should offer a refined, accurate, and comprehensive reply to the instruction. Ensure your response is well-structured, coherent, and adheres to the highest standards of accuracy and reliability.  1. <response #1>   2. <response #2>   ...   N. <response #N>   <instruction here> |

表 12：不带批评

表 13：融合器提示：不带与带批评

|  |
| --- |
| I will provide you with N responses, each indicated by a numerical identifier []. Rank the responses based on their relevance to the instruction: <instruction here>.   [1] <response #1>   [2] <response #2>   ...   [N] <response #N>   Instruction: <instruction here>.   Rank the N responses above based on their relevance to the instruction. All the responses should be included and listed using identifiers, in descending order of relevance to the instruction. The output format should be [] > [], e.g., [4] > [2]. Only respond with the ranking results, do not say any word or explain. |

表 14：基于解码器的排序提示

|  |
| --- |
| You are a helpful assistant. I will provide you with N responses, each indicated by a numerical identifier (e.g., [1], [2], etc.). Rank the responses based on their relevance to the instruction: <instruction here>.   [1] <response #1>   [2] <response #2>   ...   [N] <response #N>   Instruction: <instruction here>.   Evaluate the N responses above based on their relevance to the instruction. All the responses should be included and listed using identifiers. For each response, start the critique with the numerical identifier (e.g., [1]) followed by the strengths and weaknesses. You must include both strengths and weaknesses, even if there are more of one than the other. At the end of each response’s analysis, include two new lines to separate the critiques. Do not include any preface or text after the critiques. Do not include any references to previous critiques within a critique. Start with the analysis for the first response and end with the analysis for the last response. All of the N responses should be included and evaluated using identifiers. Structure each response’s analysis as follows:  Strengths:   - <strength #1>   - <strength #2>   - <strength #n>   Weaknesses:   - <weakness #1>   - <weakness #2>   - <weakness #n> |

表 15：批评器提示

|  |
| --- |
| I will provide you with a response indicated by the identifier ’Response’. Provide reasoning for why the response accurately and completely addresses the instruction: <instruction here>.   Response: <response>   Instruction: <instruction here>.   Provide the reasoning for the response above based on its relevance, completeness, and accuracy when compared to the instruction. Do not include any preface or text after the reasoning. |

表 16：验证器提示

|  |
| --- |
| Instruction Prompt: Given the following query, generate a set of N unit tests that would evaluate the correctness of responses to this query.   - The unit tests should cover various aspects of the query and ensure comprehensive evaluation.   - Each unit test should be clearly stated and should include the expected outcome.   - The unit tests should be in the form of assertions that can be used to validate the correctness of responses to the query.   - The unit test should be formatted like ’The answer mentions…’, ’The answer states…’, ’The answer uses…’, etc. followed by the expected outcome.   - Solely provide the unit tests for the question below. Do not provide any text before or after the list. Only output the unit tests as a list of strings (e.g., [’unit test #1’, ’unit test #2’, ’unit test #3’]).   Query: <instruction here> |

表 17：带单元测试上限

|  |
| --- |
| Instruction Prompt: Given the following query, generate a set of unit tests that would evaluate the correctness of responses to this query.   - The unit tests should cover various aspects of the query and ensure comprehensive evaluation.   - Each unit test should be clearly stated and should include the expected outcome.   - The unit tests should be in the form of assertions that can be used to validate the correctness of responses to the query.   - The unit test should be formatted like ’The answer mentions…’, ’The answer states…’, ’The answer uses…’, etc. followed by the expected outcome.   - Solely provide the unit tests for the question below. Do not provide any text before or after the list. Only output the unit tests as a list of strings (e.g., [’unit test #1’, ’unit test #2’, ’unit test #3’]).   Query: <instruction here> |

表 18：不带单元测试上限

表 19：单元测试生成器提示：带与不带单元测试上限

|  |
| --- |
| Instruction Prompt: Compose an engaging travel blog post about a recent trip to Hawaii, highlighting cultural experiences and must-see attractions.  1.  Unit Test #1: The blog post mentions at least two cultural experiences specific to Hawaii. 2.  Unit Test #2: The blog post highlights at least three must-see attractions in Hawaii. 3.  Unit Test #3: The tone of the blog post is engaging and uses descriptive language that would appeal to readers interested in travel. 4.  Unit Test #4: The blog post includes factual information about Hawaii’s culture, such as local customs, festivals, or historical facts. 5.  Unit Test #5: The blog post contains a clear narrative structure, including an introduction, main body, and a conclusion. |

表 20：指令遵循查询

|  |
| --- |
| Instruction Prompt: Alice and Bob have two dice. They roll the dice together, note the sum of the two values shown, and repeat. For Alice to win, two consecutive turns (meaning, two consecutive sums) need to result in 7. For Bob to win, he needs to see an eight followed by a seven. Who do we expect to win this game?  1.  Unit Test #1: The response correctly identifies the winning condition for Alice (two consecutive sums of 7). 2.  Unit Test #2: The response correctly identifies the winning condition for Bob (a sum of 8 followed by a sum of 7). 3.  Unit Test #3: The response explains the probability of achieving two consecutive 7s when rolling two dice. 4.  Unit Test #4: The response explains the probability of achieving an 8 followed by a 7 when rolling two dice. 5.  Unit Test #5: The response provides a conclusion on who is more likely to win based on the probability analysis. |

表 21：推理查询

表 22：单元测试示例

|  |
| --- |
| Given the following query, candidate response, and unit tests, evaluate whether or not the response passes each unit test.   - In your evaluation, you should consider how the response aligns with the unit tests, retrieved documents, and query.   - Provide reasoning before you return your evaluation.   - At the end of your evaluation, you must finish with a list of verdicts corresponding to each unit test.  - You must include a verdict with one of these formatted options: ’[Passed]’ or ’[Failed]’.  - Here is an example of the output format:  Unit Test #1: [Passed]   Unit Test #2: [Failed]   Unit Test #3: [Passed]   - Each verdict should be on a new line and correspond to the unit test in the same position.  - Here is the query, response, and unit tests for your evaluation:    Query: <instruction here>.    Candidate Response: <response>    Unit Tests:   Unit Test #1: <Unit Test #1>   Unit Test #2: <Unit Test #2>   ...   Unit Test #N: <Unit Test #N> |

表 23：单元测试评估器提示

### A.4 Archon 的贝叶斯优化

#### A.4.1 Archon 搜索空间与目标

Archon 配置空间可定义为 $\mathcal{X}=\{x_{g},x_{s},x_{f},x_{r},x_{c},x_{v}\}$，其中：

- $x_{g}\in[1,10]$：生成器模型数量
- $x_{s}\in[1,5]$：每个生成器的采样数（对 CodeContests 扩展到 $[1,1000]$）
- $x_{f}\in[1,4]$：融合层数，包括末尾的最终融合层
- $x_{r}\in[2,10]$：每个融合层的模型数，从 2 到 10、步长为 2
- $x_{c}\in\{0,1\}$：是否在每个融合器之前使用批评与排序层
- $x_{v}\in\{0,1\}$：是否在最终融合之前使用验证层

总搜索空间最初包含 18,750 个配置（$10\cdot 5\cdot 5^{(4-1)}\cdot 3=18{,}750$），移除以下无效配置后减少到 9,576 个：1) 初始生成超出融合器上下文窗口（24 个候选）；2) 单融合层包含多个融合器（$x_{f}=1$ 而 $x_{r}\geq 2$）。

设 $f(x)$ 为评估 Archon 配置 $x\in\mathcal{X}$ 的目标函数，定义为：

$$
f(x)=\text{Performance}(x)-\lambda\cdot\text{Cost}(x) \tag{1}
$$

其中 Performance($x$) 是目标任务 20% 样本上的准确率，Cost($x$) 表示推理计算使用量。

#### A.4.2 优化过程

我们描述 Archon 贝叶斯优化搜索方法的各个组成部分。

首先，定义 $\mathcal{H}$ 为架构及其目标值的历史，我们在整个优化过程中累积它。我们使用期望改进（Expected Improvement，EI）作为采集函数来决定下一个要搜索的架构配置：

$$
\text{EI}(x;\mathcal{H})=\mathbb{E}[\max(0,f(x)-f(x^{+}))], \tag{2}
$$

其中 $f(x^{+})$ 是迄今观察到的最优目标值，对应 $(x^{+},f(x^{+}))\in\mathcal{H}$。我们用高斯过程模型作为近似 $f(x)$ 的代理模型。

现在描述贝叶斯优化过程。我们先初始化观测历史 $\mathcal{H}=\emptyset$。对时间步 $t=1,\dots,T$（$T$ 为最大迭代次数参数），我们执行以下操作：

1. 用采集函数选择架构 $x_{t}$：$x_{t}=\text{argmax}_{x\in\mathcal{X}}\text{EI}(x;\mathcal{H})$。
2. 评估架构 $x_{t}$，得到 $f(x_{t})$。
3. 用 $f(x_{t})$ 更新采集函数与代理模型：$H\leftarrow H\cup(x_{t},f(x_{t}))$。

过程持续直到以下任一情况：

- 达到最大迭代次数 $T$
- 性能收敛：$|f(x_{n+1})-f(x_{n})|<\epsilon$
- 预算耗尽：$\text{Cost}(x_{1},...,x_{n})>B$

对 Archon 的实现，我们以 230-240 个随机配置初始化，这是通过经验测试发现的最优值。超过这一点后的额外样本收益递减，更好地分配给配置搜索。在我们的实现中，我们使用[贝叶斯优化 Python 包](https://github.com/bayesian-optimization/BayesianOptimization)做基于高斯过程的全局优化。

这一表述使 Archon 能高效探索配置空间，所需评估比贪心搜索少 88.5%、比随机搜索少 90.4%，贝叶斯优化在 96.0% 的迭代中找到最佳架构。对有限的推理预算（<20 次调用），传统贪心搜索方法可能表现相当，但随着搜索空间与计算预算增大，贝叶斯优化变得越来越有效。

![Refer to caption](2409.15254v6/figures/Search_Algorithms.png)

图 10：不同优化算法对 Archon 架构搜索的影响：在 MT Bench 与 Arena-Hard-Auto 基准上，我们比较寻找最优推理时架构的多种方法：随机搜索、贪心搜索与贝叶斯优化。贝叶斯优化找到最优架构所需迭代比贪心搜索少 88.5%、比随机搜索少 90.4%。

### A.5 贝叶斯优化对比替代方法

搜索技术：在超参数空间内，我们探索了三种用来自动化开发推理时架构的搜索算法：

1. 随机搜索：为我们的 Archon 架构随机选择一组超参数组合。
2. 贪心搜索：从一个基础 Archon 配置开始，边际地改变每个超参数并测试是否改进表现。若改进则纳入该变化；否则移到下一个超参数。
3. 贝叶斯优化：通过构建概率代理模型并利用采集函数进行超参数选择，高效地为 Archon 选择最有前景的超参数配置（Snoek et al., 2012；Nardi et al., 2019）（A.4 节）。

为得到基准上的模型排名，我们在搜索的第一阶段通过在每份数据集基准的 20% 样本上单独测试每个模型来计算排名。为得到基准上的融合模型排名，我们用同样的方法，用一个由可用集合中随机选出的 10 个模型组成的集成测试每个模型的融合表现。从实验中我们发现，最佳生成器与融合模型因数据集而差异很大，因此为新数据集执行这些排名是有益的（表 35）。对搜索，我们使用与评估生成与融合相同的 20% 数据集样本，使我们能以更快的评估速度指导架构搜索，同时获得有意义的开发信号。

比较搜索算法：在图 10 中，我们比较每种搜索算法在我们探索的基准上的有效性。虽然随机搜索保证能找到最优 Archon 配置，我们发现贝叶斯优化在「找到最优配置」与「最小化测试配置数」的权衡上最有效。在图 10 测试的搜索迭代中，对 96.0% 的情况，我们发现贝叶斯优化在所探索的搜索算法中拥有最优配置。我们的贝叶斯优化架构搜索使用 230 个初始样本（A.4 节）。贝叶斯优化还以比贪心搜索少 88.5%、比随机搜索少 90.4% 的评估数找到最佳架构配置。

贝叶斯优化分析：在表 26 中，我们探索初始测试点数、探索迭代数与 Archon 推理调用预算如何影响贝叶斯优化的有效性。额外的初始测试点持续改进搜索效力，直到 230-240 个样本，超过后测试最好转投配置搜索。对较低的 Archon 推理调用预算（如 <20 次推理调用），贝叶斯优化效果较差，在有限的搜索空间下表现更接近贪心或随机搜索（表 27）。因此，贝叶斯优化对具有较大推理调用预算、更开放式的 Archon 架构搜索更有效；而对更有限的推理调用预算，传统组件工程可能更好。

### A.6 Archon 架构算法比较

| 初始点数 | 占总配置比例 | 达到最大配置的迭代数 | 合计迭代数 |
| --- | --- | --- | --- |
| 200 | 2.18% | 353 | 553 |
| 210 | 2.29% | 324 | 534 |
| 220 | 2.40% | 301 | 521 |
| 230 | 2.51% | 284 | 514 |
| 240 | 2.61% | 261 | 501 |
| 250 | 2.72% | 265 | 515 |
| 260 | 2.83% | 256 | 516 |
| 270 | 2.94% | 252 | 522 |

表 24：MT Bench

| 初始点数 | 占总配置比例 | 达到最大配置的迭代数 | 合计迭代数 |
| --- | --- | --- | --- |
| 200 | 2.18% | 478 | 678 |
| 210 | 2.29% | 431 | 641 |
| 220 | 2.40% | 415 | 635 |
| 230 | 2.51% | 382 | 612 |
| 240 | 2.61% | 389 | 629 |
| 250 | 2.72% | 385 | 635 |
| 260 | 2.83% | 372 | 632 |
| 270 | 2.94% | 368 | 638 |

表 25：Arena-Hard-Auto

表 26：贝叶斯优化超参数比较：在 MT Bench 与 Arena-Hard-Auto 上，我们比较不同初始样本点数的贝叶斯优化配置。我们发现 230 到 240 个初始样本点能最小化找到最优配置的（初始采样与探索）合计迭代数。对所探索的配置，超参数选择总数为 9,576。

| 推理预算 | 10 | 20 | 30 | 40 | 50 |
| --- | --- | --- | --- | --- | --- |
| 随机选择 | 387 | 1152 | 2731 | 4359 | 5843 |
| 贪心搜索 | 343 | 984 | 2153 | 3045 | 4895 |
| 贝叶斯优化 | 254 | 386 | 452 | 515 | 589 |

表 27：按推理调用预算比较 Archon 架构搜索算法（收敛所需迭代数）：我们的比较在 MT Bench 上评估。

### A.7 Archon 基准与结果

| 基准 | 示例数 | 参考模型 | 裁判模型 | 打分类型 | 指标 |
| --- | --- | --- | --- | --- | --- |
| AlpacaEval 2.0 | 805 | GPT-4-Turbo | GPT-4-Turbo | 成对比较 | L.C. 与原始胜率 |
| Arena-Hard-Auto | 500 | Claude-3.5-Sonnet | GPT-4-Turbo | 成对比较 | 胜率 |
| MT-Bench | 80 | Claude-3.5-Sonnet | GPT-4-0314 | 成对比较 | 调整后胜率 |
| MixEval | 2000 | N/A | N/A | 标准答案 | 准确率 |
| MixEval-Hard | 500 | N/A | N/A | 标准答案 | 准确率 |
| MATH | 200（从 5000 抽样） | N/A | N/A | 标准答案 | Pass@1 |
| CodeContests | 140（非视觉题目） | N/A | N/A | 标准答案 | Pass@1 |

表 28：基准概览：AlpacaEval 2.0（Li et al., 2023）、Arena-Hard-Auto（Li et al., 2024b）、MT-Bench（Zheng et al., 2023）、MixEval（Ni et al., 2024）、MixEval Hard、MATH（Hendrycks et al., 2021）与 CodeContests（Li et al., 2022）的评估配置。

（注：Arena-Hard-Auto 的参考模型按其官方流程默认使用 GPT-4-0314；此处列出按论文正文的设置说明。）

.

![Refer to caption](2409.15254v6/figures/Combined_Sampling_and_Ensembling.png)

图 11：在 Arena-Hard-Auto 上重复采样、集成、排序与融合带来的性能增益：随着我们扩展模型采样（左）或向生成器集成添加更多模型（右），Archon 的胜率持续显著增长，分别提升 9.3% 与 18.5%。这些最佳结果通过选出 top-5 回答并融合获得。集成模型按其在该任务上的单独表现从好到差加入（表 35）。oracle 选择是从集成生成的全部样本中选出最佳答案生成的表现。结果为 10 次独立评估运行的平均。

| 模型 / LLM 系统 | Arena-Hard-Auto 得分 | 置信区间（C.I.） |
| --- | --- | --- |
| Claude 3.5 Sonnet | N/A | N/A |
| GPT-4o | 48.1% | (-2.3, 1.8) |
| Llama 3.1 405B Instruct | 28.4% | (-2.7, 2.5) |
| 开源 通用目的 Archon 架构 | 66.2% | (-2.4, 2.2) |
| 开源 任务专属 Archon 架构 | 69.0% | (-2.8, 2.5) |
| 闭源 通用目的 Archon 架构 | 70.5% | (-2.5, 2.0) |
| 闭源 任务专属 Archon 架构 | 74.4% | (-2.3, 1.6) |
| 全源 通用目的 Archon 架构 | 72.5% | (-2.5, 1.8) |
| 全源 任务专属 Archon 架构 | 76.1% | (-1.8, 2.2) |

表 29：以 Claude-3.5-Sonnet 为基线模型的 Arena-Hard-Auto 上 Archon 结果：基线模型为 Claude-3.5-Sonnet（默认基线模型：GPT-4-0314），裁判模型为 GPT-4-Turbo。

| 模型 / LLM 系统 | 推理调用数 | GSM8K | TriviaQA | DROP | MATH | BBH | AGIEval | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-4o - 2024-05-13 | 1 | 94.9 | 89.1 | 88.2 | 98.5 | 98.3 | 71.5 | 90.3 |
| Claude 3.5 Sonnet | 1 | 98.0 | 92.0 | 92.6 | 96 | 95.6 | 78.0 | 92.0 |
| Llama 3.1 405B Instruct | 1 | 98.2 | 87.9 | 89.6 | 91.5 | 95.8 | 73.2 | 89.6 |
| 通用目的 Archon 架构 | 29 | 98.3 | 94.8 | 94.6 | 98.1 | 97.3 | 82.1 | 94.2 |
| 任务专属 Archon 架构 | 34 | 98.2 | 96.7 | 95.6 | 98.5 | 98.8 | 84.2 | 95.7 |

表 30：MixEval 按子数据集的结果：计算平均值时，我们不对每个数据集引入任何权重。

| 模型 / LLM 系统 | 推理调用数 | GSM8K | TriviaQA | DROP | MATH | BBH | AGIEval | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-4o - 2024-05-13 | 1 | 72.3 | 70.5 | 70.2 | 94.4 | 80.0 | 53.5 | 73.5 |
| Claude 3.5 Sonnet | 1 | 87.3 | 75.5 | 79.3 | 82.5 | 80.0 | 74.6 | 79.9 |
| Llama 3.1 405B Instruct | 1 | 98.7 | 71.2 | 70.7 | 86.9 | 78.8 | 62.0 | 78.1 |
| 通用目的 Archon 架构 | 33 | 96.7 | 82.7 | 83.2 | 93.4 | 82.0 | 76.7 | 85.8 |
| 任务专属 Archon 架构 | 37 | 98.9 | 86.2 | 85.2 | 96.2 | 86.0 | 80.1 | 88.8 |

表 31：MixEval-Hard 按子数据集的结果：计算平均值时，我们不对每个数据集引入任何权重。

| 模型 | GSM8K Pass@1 | MMLU Math Pass@1 | HumanEval Python Pass@1 | MBPP Pass@1 |
| --- | --- | --- | --- | --- |
| GPT-4o | 97.1% | 84.8% | 89.0% | 87.5% |
| Claude 3.5 Sonnet | 96.8% | 90.9% | 90.2% | 88.9% |
| Llama 3.1 405B Instruct | 95.9% | 85.4% | 90.2% | 88.6% |

表 32：探索的其他数学与编程基准

| 裁判模型 | MT Bench：GPT-4-0314 | AlpacaEval 2.0：GPT-4-Turbo | Arena-Hard-Auto：GPT-4-Turbo | Arena-Hard-Auto：GPT-4-Turbo | MixEval/MixEval-Hard/MATH：N/A |
| --- | --- | --- | --- | --- | --- |
| 参考模型 | Claude 3.5 Sonnet | GPT-4-Turbo | Claude 3.5 Sonnet | GPT-4-Turbo | N/A |
| 模型 / LLM 系统（推理调用数） | MT Bench W.R. | AlpacaEval 2.0 L.C. W.R. | Arena-Hard-Auto W.R. | Arena-Hard-Auto Raw W.R. | MixEval-Hard W.R. | MixEval Acc. | MATH Acc. | CodeContests Pass@1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-4o - 2024-05-13（1） | 44.7% | 57.5% | 51.3% | 48.1% | 80.3% | 63.6% | 88.0% | 84.5% |
| Claude 3.5 Sonnet（1） | N/A | 52.4% | 40.6% | N/A | 80.9% | 68.9% | 89.7% | 85.0% |
| Llama 3.1 405B Instruct（1） | 44.7% | 40.3% | 37.7% | 28.4% | 64.1% | 66.2% | 88.9% | 83.5% |
| MoA（19） | 51.6% | 65.1% | 59.8% | 52.2% | 84.2% | 62.5% | 87.3% | 82.0% |
| MoA Lite（7） | 45.6% | 59.3% | 57.0% | 40.6% | 87.8% | 61.1% | 87.1% | 83.0% |
| 开源 通用目的 Archon（35） | 67.5% | 63.0% | 68.3% | 66.2% | 85.1% | 65.5% | 86.9% | 86.5% |
| 开源 任务专属 Archon（44） | 71.6% | 66.7% | 70.7% | 69.0% | 89.5% | 67.5% | 89.6% | 90.5% |
| 闭源 通用目的 Archon（32） | 73.1% | 63.5% | 69.1% | 70.5% | 85.8% | 67.7% | 88.2% | 88.0% |
| 闭源 任务专属 Archon（40） | 77.5% | 68.4% | 72.1% | 74.4% | 90.2% | 72.9% | 90.4% | 89.5% |
| 全源 通用目的 Archon（35） | 76.8% | 65.8% | 70.2% | 72.5% | 89.3% | 70.1% | 88.1% | 90.0% |
| 全源 任务专属 Archon（39） | 80.4% | 67.6% | 73.3% | 76.1% | 92.1% | 72.9% | 90.6% | 93.5% |

表 33：Archon 架构优化后在完整评估数据集上的强劲表现：我们发现，在完整基准上评估时，Archon 的推理时架构持续超过单调用的 SOTA LLM（开源与闭源基线皆是）（表 28）。我们探索两种配置：为每个单独基准构建定制 Archon 配置的架构搜索，以及为所有基准构建单一通用目的 Archon 配置的架构搜索（第 4.1 节）。我们发现，在全源设置下，通用 Archon 配置平均只落后定制配置 3.2 个百分点，表明用我们的框架创建的通用目的推理时架构的效力。对 Arena-Hard-Auto，我们还给出以 Claude 3.5 Sonnet 为更强参考模型的配置，以便与 Archon 推理时架构比较并缓解 GPT 裁判对 GPT 生成的偏好偏差。对 MT Bench，我们使用 GPT-4-0314 裁判模型而非更新的 LLM 裁判，以与该基准的既有结果保持一致。对我们的任务专属 Archon 架构，我们还给出各基准上的平均推理调用数。探索模型的完整列表见表 34。对 MATH，我们使用随机抽样的大小为 200 的子集评估（第 4.1 节；表 28）。我们在表 1 中给出 Archon 架构在每个评估基准留出的 80% 子集上的结果。

### A.8 Archon LLM 分析

| 模型 | 源码 | 参数量 | 最大序列长度 |
| --- | --- | --- | --- |
| GPT-4o（OpenAI, 2024） | 闭源 | — | 128K |
| GPT-4-Turbo（OpenAI, 2024） | 闭源 | — | 128K |
| Claude-3-Opus（Anthropic, 2024） | 闭源 | — | 200K |
| Claude-3.5-Sonnet（Anthropic, 2024） | 闭源 | — | 200K |
| Claude-3-Haiku（Anthropic, 2024） | 闭源 | — | 200K |
| Llama-3.1-70B-Instruct（Dubey et al., 2024） | 开源 | 70B | 8k |
| Llama-3.1-405B-Instruct（Dubey et al., 2024） | 开源 | 70B | 8k |
| DeepSeek LLM 67B Chat（Guo et al., 2024） | 开源 | 67B | 32k |
| Qwen2 72B Instruct（Qwen, 2024） | 开源 | 72B | 32k |
| Qwen1.5 110B Chat（Bai et al., 2023） | 开源 | 110B | 32k |
| Qwen1.5 72B Chat（Bai et al., 2023） | 开源 | 72B | 32k |
| Mixtral 8x22B v0.1（Jiang et al., 2024） | 开源 | 176B | 32k |
| WizardLM 8x22B（Xu et al.） | 开源 | 176B | 32k |
| dbrx-instruct（Databricks, 2024） | 开源 | 132B | 32k |
| princeton-nlp/Llama-3-Instruct-8B-SimPO（Meng et al., 2024） | 开源 | 8B | 8k |
| princeton-nlp/Llama-3-Instruct-8B-DPO（Meng et al., 2024） | 开源 | 8B | 8k |
| princeton-nlp/Llama-3-Instruct-8B-RDPO（Meng et al., 2024） | 开源 | 8B | 8k |
| princeton-nlp/Llama-3-Instruct-8B-IPO（Meng et al., 2024） | 开源 | 8B | 8k |
| Llama-3.1-8B-Instruct（Dubey et al., 2024） | 开源 | 8B | 8k |
| Qwen2-7B-Instruct（Qwen, 2024） | 开源 | 7B | 32k |
| Qwen/Qwen1.5-7B-Chat（Bai et al., 2023） | 开源 | 7B | 32k |
| mistralai/Mistral-7B-Instruct-v0.2（Jiang et al., 2023a） | 开源 | 7B | 32k |
| cognitivecomputations/dolphin-2.2.1-mistral-7b（Hartford, 2024） | 开源 | 7B | 32k |
| microsoft/Phi-3-mini-4k-instruct（Abdin et al., 2024） | 开源 | 4B | 4k |
| HuggingFaceH4/zephyr-7b-beta（Tunstall et al.） | 开源 | 7B | 32k |
| microsoft/Phi-3-small-8k-instruct（Abdin et al., 2024） | 开源 | 7B | 8k |
| snorkelai/Snorkel-Mistral-PairRM-DPO（Tran et al., 2023） | 开源 | 7B | 32k |
| mistralai/Mistral-7B-Instruct-v0.3（Jiang et al., 2023a） | 开源 | 7B | 32k |

表 34：用 Archon 测试的模型。

| 模型 | MT Bench 生成 | MT Bench 融合 | Alpaca Eval 2.0 生成 | Alpaca Eval 2.0 融合 | Arena Hard Auto 生成 | Arena Hard Auto 融合 | MixEval 生成 | MixEval 融合 | MixEval Hard 生成 | MixEval Hard 融合 | MATH 生成 | MATH 融合 | CodeContests 生成 | CodeContests 融合 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-4o | 44.7% | 61.9% | 57.5% | 64.5% | 48.1% | 69.2% | 88.0% | 89.4% | 63.6% | 65.4% | 82.0% | 81.0% | 17.9% | 19.4% |
| GPT-4-Turbo | 42.2% | 63.1% | 55.0% | 65.8% | 48.1% | 61.9% | 88.9% | 89.0% | 64.1% | 64.4% | 79.5% | 73.5% | 9.3% | 14.2% |
| Claude 3 Opus | 30.9% | 57.2% | 40.5% | N/A | 27.0% | 47.9% | 88.3% | 88.2% | 63.6% | 64.0% | 74.5% | 74.0% | 10.0% | 12.5% |
| Claude 3.5 Sonnet | N/A | 71.9% | 52.37% | 63.6% | N/A | 73.2% | 89.7% | 89.3% | 68.9% | 69.5% | 83.5% | 86.5% | 12.1% | 15.5% |
| Qwen 2 72B Instruct | 35.0% | 59.7% | 37.48% | 56.0% | 14.5% | 49.5% | 86.5% | 87.5% | 58.7% | 61.1% | 81.0% | 78.5% | 3.6% | 5.2% |
| DeepSeek LLM 67B Instruct | 18.4% | 20.0% | 17.8% | 17.1% | N/A | N/A | 79.2% | N/A | 42.5% | N/A | 57.0% | N/A | 5.7% | N/A |
| Qwen 1.5 72B Chat | 24.7% | 46.3% | 36.6% | 55.7% | 14.4% | 36.4% | 84.5% | 82.5% | 50.3% | 52.2% | 71.5% | 67.5% | 15.0% | 13.9% |
| Qwen 1.5 110B Chat | 34.4% | 50.3% | 43.6% | 55.9% | 21.9% | 39.7% | 85.3% | 86.5% | 51.8% | 55.6% | 67.0% | 75.5% | 3.6% | 7.8% |
| Wizard 8x22B | 53.8% | 57.2% | 44.7% | 50.6% | 45.6% | 51.2% | 83% | 78.1% | 54.3% | 50.4% | 76.0% | 60.5% | 7.1% | 10.4% |
| Llama 3.1 8B Instruct | 33.1% | 45.9% | 25.6% | 34.9% | 11.9% | 28.6% | 75.0% | 57.5% | 41.3% | 46.5% | 65.5% | 60.5% | 8.6% | 7.8% |
| Llama 3.1 70B Instruct | 45.0% | 51.9% | 35.6% | 40.2% | 23.8% | 37.2% | 85.7% | 83.5% | 61.1% | 65.5% | 74.0% | 73.5% | 20.7% | 23.4% |
| Llama 3.1 405B Instruct | 44.7% | N/A | 40.3% | N/A | 28.4% | N/A | 88.9% | N/A | 66.2% | N/A | 78.0% | N/A | 27.1% | N/A |

表 35：Archon 单模型生成与融合表现：对 Alpaca Eval 2.0，我们使用长度控制胜率（LC WR）。对融合，我们从 top-10 生成器模型各收集一个候选。

| Jaccard 相似度（%） | MT Bench | AlpacaEval 2.0 | Arena-Hard-Auto | MixEval | MixEval-Hard | MATH | CodeContests |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 最佳开源 70B+ 模型，采样 8 次 + 融合器 | 45.3% | 52.1% | 48.4% | 55.2% | 58.9% | 65.2% | 63.7% |
| 集成（top-8 模型），各采样一次 + 融合器 | 31.6% | 34.1% | 28.9% | 38.6% | 40.9% | 57.1% | 53.4% |

表 36：按基准划分的候选回答与融合回答之间的 Jaccard 相似度：对融合器，我们使用每个基准表现最好的 70B+ 模型。

![Refer to caption](2409.15254v6/figures/Fusion_Layers_Analysis.png)

图 12：按基准划分的融合层效力：仅扩展融合层时，我们在所探索基准上看到有限收益，但当加入 Critic 与 Ranker 等其他推理时技术时，随着我们继续扩展推理时计算，下游表现随之提升（图 4）。我们对每个基准使用 top 生成器模型的 8 模型集成（表 35）。对我们的融合层，最终融合层使用最佳融合模型（表 35）。中间层使用每个基准的 top-8 融合模型。

### A.9 Archon 架构

图 13：全源可泛化 Archon 架构：使用 Archon 的架构搜索，我们发现该全源 Archon 配置在所探索的基准（CodeContests 除外）上有效。在上图中，我们用 10 个 SOTA 全源 LLM 创建连续多层的批评器、排序器与融合器，每个后续融合层的融合器更少，在处理候选生成时产生「漏斗」效应。批评器、排序器与融合器的层通过迭代批评与重写带来更好的候选生成。每个初始生成器模型都只采样一次。

图 14：用于指令遵循与推理的全源 Archon 架构：使用 Archon 的架构搜索，我们发现该全源 Archon 配置在所探索的指令遵循基准（MT Bench、AlpacaEval 2.0、ArenaHardAuto）上有效。

图 15：用于数学的全源 Archon 架构：使用 Archon 的架构搜索，我们发现该全源 Archon 配置在所探索的数学基准（MATH）上有效。

图 16：用于编程的全源 Archon 架构：使用 Archon 的架构搜索，我们发现该全源 Archon 配置在所探索的编程基准（CodeContests）上有效。

### A.10 按推理计算预算、模型规模与成本看 Archon

| 模型类别 | 推理调用数 | MT Bench | AlpacaEval 2.0 | Arena-Hard-Auto | MixEval | MixEval-Hard |
| --- | --- | --- | --- | --- | --- | --- |
| 70B+ 模型 | 1 | 55.0% | 44.7% | 45.6% | 86.5% | 61.1% |
| | 10 | 52.5% | 50.6% | 45.6% | 86.5% | 63.9% |
| | 20 | 65.3% | 60.4% | 59.4% | 89.0% | 65.0% |
| | 30 | 69.2% | 64.5% | 69.0% | 89.5% | 67.5% |
| | 40 | 69.5% | 66.7% | 69.0% | 89.5% | 67.5% |
| | 50 | 71.6% | 66.7% | 69.0% | 89.5% | 67.5% |
| 闭源模型 | 1 | 45.0% | 57.5% | 48.1% | 88.9% | 68.9% |
| | 10 | 57.1% | 63.2% | 68.4% | 90.0% | 70.1% |
| | 20 | 59.4% | 66.5% | 75.5% | 90.6% | 70.5% |
| | 30 | 70.2% | 68.8% | 77.4% | 90.6% | 72.9% |
| | 40 | 75.5% | 68.8% | 77.4% | 90.6% | 72.9% |
| | 50 | 80.4% | 68.8% | 77.4% | 90.6% | 72.9% |

表 37：不同推理预算下的 Archon：对 AlpacaEval 2.0，我们使用长度控制胜率（LC WR）。

| 模型 / LLM 系统 | MT Bench | AlpacaEval 2.0 | Arena-Hard-Auto | MixEval | MixEval-Hard |
| --- | --- | --- | --- | --- | --- |
| 最佳 7B 模型，1 样本 | 15.7% | 41.0% | 18.3% | 76.2% | 46.1% |
| 最佳 7B 模型，10 样本 + 排序 | 16.5% | 43.2% | 18.9% | 78.4% | 48.5% |
| 10 模型、1 样本集成 + 排序 | 22.4% | 48.2% | 25.6% | 81.5% | 52.9% |
| 10 模型、1 样本集成 + 融合 | 14.3% | 39.4% | 17.5% | 73.2% | 45.2% |
| 10 模型、1 样本集成 + top-5 排序 + 融合 | 15.9% | 41.2% | 18.0% | 75.1% | 46.9% |
| 10 模型、1 样本集成 + 批评器 + 融合 | 10.5% | 38.4% | 16.5% | 71.4% | 42.5% |

表 38：用 7B 开源模型的 Archon：对 AlpacaEval 2.0，我们使用长度控制胜率（LC WR）。我们使用表 34 中的开源 7B 模型进行测试。

| 模型 | 每百万输入 token 成本（$） | 每百万输出 token 成本（$） |
| --- | --- | --- |
| Claude 3.5 Sonnet | $3 | $15 |
| Claude 3.0 Opus | $15 | $75 |
| GPT-4o | $5 | $15 |
| GPT-4-Turbo | $10 | $30 |
| TogetherAI - Llama 3.1 405B Instruct | $5 | $5 |
| TogetherAI - Llama 3.1 70B Instruct | $0.88 | $0.88 |
| TogetherAI - 其他模型 | $0.90 | $0.90 |

表 39：截至 2024 年 11 月的模型 API 成本

| 模型 / LLM 系统 | MT Bench | AlpacaEval 2.0 | Arena-Hard-Auto | MixEval | MixEval-Hard | MATH | CodeContests |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Claude 3.5 Sonnet | 0.0305 | 0.0171 | 0.0212 | 0.0231 | 0.0226 | 0.0325 | 0.384 |
| GPT-4o | 0.0481 | 0.0236 | 0.0324 | 0.0357 | 0.0361 | 0.514 | 0.562 |
| Llama 3.1 405B Instruct | 0.0281 | 0.0174 | 0.0185 | 0.0212 | 0.0205 | 0.305 | 0.372 |
| 通用目的 Archon 架构 | 0.364 | 0.189 | 0.195 | 0.284 | 0.252 | 0.375 | 0.461 |
| 任务专属 Archon 架构 | 0.401 | 0.210 | 0.221 | 0.295 | 0.265 | 0.425 | 0.448 |

表 40：按基准划分的 Archon 每查询成本（$）
