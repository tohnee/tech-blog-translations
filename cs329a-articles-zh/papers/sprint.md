---
title: "SPRINT：在推理模型中实现交错规划与并行执行"
title_en: "SPRINT: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models"
arxiv: 2506.05745
source: https://arxiv.org/abs/2506.05745
crawled: 2026-09-23
translated: 2026-09-23
---

# SPRINT：在推理模型中实现交错规划与并行执行

> 原文：[SPRINT: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models](https://arxiv.org/abs/2506.05745) · Stanford CS329A 指定阅读

Emil Biju（共同一作；斯坦福大学、微软）
Shayan Talaei¹（斯坦福大学）
Zhemin Huang¹（斯坦福大学）
Mohammadreza Pourreza（Google）
Azalia Mirhoseini（共同资深作者；斯坦福大学）
Amin Saberi²（斯坦福大学；邮箱：{emilbiju, stalaei, zheminh}@stanford.edu，pourreza@google.com，{azalia, saberi}@stanford.edu）

###### 摘要

大型推理模型（LRM）擅长复杂推理任务，但通常会生成冗长的串行思维链，导致在得出最终答案之前推理时间很长。为应对这一挑战，我们提出 Sprint——一个新颖的后训练与推理时框架，旨在让 LRM 在推理过程中动态识别并利用并行化机会。Sprint 引入了一条创新的数据构建管线，可将自然语言推理轨迹重组为「长时程规划 + 并行执行」的结构化轮次。只需在这类精心构建的少量数据上微调 LRM，模型便能*学会*在延伸的推理过程中动态识别独立子任务，并有效地并行执行它们。大量评估表明，用 Sprint 框架微调的模型在数学等复杂领域上可匹敌推理模型的性能，同时在需要超过 8,000 个输出 token 的问题上最多减少 39% 的串行 token。最后，我们观察到一致的结果可迁移到两个分布外任务——GPQA 与 Countdown——在更长的推理轨迹上平均串行 token 分别减少多达 45% 与 65%，同时保持与微调后推理模型相当的性能。

## 1 引言

在大型语言模型（LLM）中扩展推理时计算已被反复证明可以提升推理准确率。现有方法大致分为两类：串行（Wei et al., 2023）与并行（Brown et al., 2024）。串行方法，尤其是 Deepseek-R1（Guo et al., 2025）与 OpenAI o1（OpenAI, 2024）等大型推理模型（LRM），在数学与编程等复杂推理任务上取得了显著成功，但代价是生成非常长的 token 序列。另一方面，并行方法，如结合自洽性的重复采样（Wang et al., 2023）或 best-of-N（Cobbe et al., 2021；Lightman et al., 2023b），利用多次响应生成来提升准确率。然而，这些方法通常缺乏推理路径之间有效的协调与信息共享，导致冗余计算与有限的性能增益。此外，树搜索（Tree-of-Thoughts；Yao et al., 2023a）与图搜索（Graph-of-Thoughts；Besta et al., 2024）等结构化并行方法需要预定义的、启发式驱动的搜索结构，天然限制了其在多样任务上的灵活性与可扩展性。

我们提出 Sprint¹，一个面向推理模型的后训练与推理框架，它结合了串行推理与并行推理的优势，同时保持通用任务所需的灵活性。Sprint 不依赖人工结构，而是训练推理语言模型在推理时动态识别并利用并行化机会。这使 Sprint 能够达到推理模型的高准确率，同时显著减少求解数学等复杂推理任务所需的串行 token 数量。

注 1：Sprint 这一名称源自敏捷开发方法论——一个 sprint（冲刺）包含一个规划阶段，随后是并行的增量式执行。

在推理侧，Sprint 通过两种不同角色对 LRM 进行编排：一个规划器（planner）与一组执行器（executor）。在每一步，可访问推理轨迹累积上下文的规划器生成一组相互独立的计划，每个计划通过自然语言 *<prompt>* 来描述。随后，多个执行器并发地执行这些计划。这种规划与执行交错的策略通过让耗时任务同时执行来加速推理过程。

尽管许多现成的 LRM 通过串行推理轨迹取得了高性能，它们并未被训练来有效地提出可并行化的任务。考虑到 LRM 针对给定查询的推理轨迹包含对其先前步骤的反思、将任务分解为子任务、以及对备选策略的试错探索等步骤，我们质疑严格串行推理的必要性。实践中，许多推理步骤是相互独立的，因此可以并行执行；例如，同时探索多种策略，或独立计算一个复杂问题的不同组成部分。基于这些洞察，我们设计了一条数据构建管线，将自然语言推理轨迹谨慎地重组为结构化的计划与并行执行，同时密切保持原始数据分布。最终，仅用 1,700 个此类示范做监督微调，我们就解锁了模型动态识别并利用并行推理机会的能力。

为评估 Sprint 的准确性与有效性，我们在 MATH-500（Lightman et al., 2023b）上测试分布内表现，并在两个分布外基准上测试：GPQA-diamond（Rein et al., 2023）与 Countdown（24 点游戏；Yao et al., 2023a）。在 MATH-500 上，Sprint 将基座推理模型 Deepseek-R1-distill-7B（Guo et al., 2025）的准确率从 89.1% 提升至 92.5%，超过准确率为 91% 的推理微调模型（RFT），同时平均少生成 440 个串行 token。在需要更长推理轨迹的问题上（RFT 模型下超过 8,000 个 token），Sprint 取得更大的节省，串行 token 最多减少 39%。我们还表明 Sprint 能很好地泛化到分布外任务，在显著减少 token 使用的同时（Countdown 上减少 53%）匹敌推理微调模型的性能。

总而言之，我们的工作做出以下关键贡献²：

注 2：我们在[该仓库](https://github.com/ShayanTalaei/SPRINT/tree/main)开源了代码与数据集。

- 我们提出 Sprint——一个通过滚动视界（rolling horizon）并行规划与执行来加速大型推理模型推理过程的创新框架。
- 我们开发了一条新颖的数据构建管线，将复杂的自然语言推理轨迹谨慎地转换为用于微调 LRM 的结构化数据集，其多步流程包括步骤提取、有向无环图（DAG）构建、装箱（packing）、过滤与重格式化。
- 我们对比强推理基线分析了 Sprint 在复杂推理任务上的准确性与效率。结果表明，相比推理蒸馏模型，Sprint 可以取得更高的准确率，同时在长推理轨迹上最多减少 39% 的串行 token。
- 我们展示了 Sprint 在两个分布外基准上一致的泛化性能：GPQA 上节省约 45% 的串行 token，Countdown 上节省约 65%，同时匹敌推理微调模型的性能。这些结果凸显了 Sprint 在多样领域中有效并行化推理轨迹的能力。

## 2 相关工作

**用长思维链改进推理。** 近期进展表明，生成延伸的思维链（Wei et al., 2023）可显著增强大型语言模型的推理能力，尤其在数学问题求解与逻辑推断等任务上（Zhu et al., 2023；Zelikman et al., 2022；OpenAI, 2024；Guo et al., 2025）。尽管有效，这些方法天然产生很长的串行输出，增加延迟并拖慢推理速度。Sprint 通过让模型动态并行化相互独立的推理步骤来解决这一局限，显著减少串行生成并提升推理效率。

**结构化搜索与多智能体框架。** 树搜索（Tree-of-Thought；Yao et al., 2023a）、图搜索（Graph-of-Thought；Besta et al., 2024）、森林搜索（Forest-of-Thought；Bi et al., 2025）与原子搜索（Atom-of-Thought；Teng et al., 2025）等方法，以及多智能体交互方法（Du et al., 2023；Kim et al., 2024；Zhuge et al., 2024；Saad-Falcon et al., 2024），通过固定搜索模式或预定义交互协议（常作用于完整解层面）来结构化推理过程。Sprint 通过*训练*模型自主地在串行与并行任务之间分配推理时计算——以求解一条解轨迹的子部分或探索备选解——推广了这些框架。

**用语言模型进行规划与执行。** 将规划能力集成到语言模型中的研究已从多个方向展开：预先将任务分解为子任务（Zhou et al., 2022；Valmeekam et al., 2023；Juneja et al., 2024；Prasad et al., 2024），或基于中间反馈的迭代式精化（Yao et al., 2023b；Shinn et al., 2023）。这些方法主要依赖串行执行，未显式考虑动态并行规划。Sprint 通过让模型自主进行动态并行规划填补了这一空缺，借助并发执行提升推理效率。

表 1：推理时扩展方法的比较。方法依据是否支持推理时并行、自适应搜索、模型优化以及处理多步串行推理的能力来评估。Sprint 唯一地满足全部标准，在需要相互依赖串行步骤的通用推理任务中实现动态并行。

| 方法 | 推理时并行 | 自适应搜索 | 模型优化 | 多步推理 |
| --- | --- | --- | --- | --- |
| Tree-of-Thought (ToT)（Yao et al., 2023a） | ✓ | ✗ | ✗ | ✗ |
| Graph-of-Thought (GoT)（Besta et al., 2024） | ✓ | ✗ | ✗ | ✗ |
| Skeleton-of-Thought (SoT)（Ning et al., 2023） | ✓ | ✓ | ✗ | ✗ |
| 重复采样（Brown et al., 2024；Wang et al., 2023；Cobbe et al., 2021） | ✓ | ✗ | ✗ | ✗ |
| 推理模型（Guo et al., 2025；OpenAI, 2024） | ✗ | ✓ | ✓ | ✓ |
| PASTA（Jin et al., 2025） | ✓ | ✓ | ✓ | ✗ |
| Hogwild! Inference（Rodionov et al., 2025） | ✓ | ✓ | ✗ | ✗ |
| Sprint（本文） | ✓ | ✓ | ✓ | ✓ |

**语言模型推理中的并行化。** 利用并行推理路径的方法，如 best-of-N 采样（Cobbe et al., 2021；Lightman et al., 2023b）或自洽性（Wang et al., 2023），通过生成多条独立推理轨迹带来了性能提升。然而，这些技术通常缺乏并行线程之间的有效协调，导致冗余与低效计算。为缓解这一问题，Skeleton-of-Thought（SoT）（Ning et al., 2023）与 APAR（Liu et al., 2024）假设子任务之间语义独立来并行化解码，从而可分别处理响应的不同片段。尽管这些方法实现了更快的推理，它们在本质上需要串行推理的任务（如数学问题求解，后续步骤依赖先前计算）上表现欠佳。

近期有三项工作——PASTA（Jin et al., 2025）、Hogwild! Inference（Rodionov et al., 2025）与 APR（Pan et al., 2025）——研究了共享推理轨迹内部的并行化。PASTA 教模型把任务分解为并行子任务，随后将其完整上下文合并回单一主线程，但它并未针对需要多步规划的推理任务做优化。Hogwild! Inference 依赖并行提示让多个工作者协作推理，而没有对模型进行任务分发的调优。APR 训练模型把子任务委派给并行子线程以处理合成 Countdown 任务，但其训练数据构建依赖一个专用符号求解器，限制了其对通用推理任务的适用性。Sprint 通过引入一个可泛化的后训练框架来扩展这一研究方向，使推理模型能为通用推理任务动态地组织推理。

总体而言，一个有效的推理系统应支持逻辑上的多步相互依赖（多步推理），以准确处理后续步骤依赖先前结果的任务。它应能动态调整搜索策略（自适应搜索）以应对多样的问题结构。针对下游任务优化模型性能（模型优化）往往是取得高效结果的必要条件。最后，利用并行执行（推理时并行）对通过并发处理独立推理子任务来降低延迟至关重要。表 1 依据这些标准比较了我们的方法与现有的推理时扩展方法。

## 3 方法

本节概述 Sprint 的设计与组成。宏观上，Sprint 由一个面向推理模型的推理框架与一个训练协议组成，后者教会模型在推理过程中有效识别并利用可并行化的规划与执行。

### 3.1 推理时的交错规划与并行执行

图 1：Sprint 推理过程概览：1) 规划器接收累积上下文（包括先前的计划与执行结果），或提出一组新的独立任务，或产出最终答案以终止过程。2) 一组执行器根据各自提示并发执行每个任务。3) 执行结果附带对应标签追加回累积上下文，并回到步骤 1 进入下一次迭代。

Sprint 的推理包含两个主要模块：一个规划器与一组执行器，全部由微调后的推理模型驱动。推理始于规划器接收*输入查询*，随后是迭代式的规划与执行轮次（称为*阶段*，stage），直到规划器决定产出最终答案终止过程。如图 1 所示，每个推理阶段包含以下三个环节：

1. 规划。在第 $i$ 阶段，规划器接收推理轨迹的累积上下文，包括输入查询、先前的计划以及此前各阶段（第 1 到 $i-1$ 阶段）的执行输出。规划器随后为当前阶段生成计划，包裹在 *<Plan_i>* 标签内。在此阶段，规划器可以生成中间推理 token，受益于其推理能力。当规划器识别出适合委派给执行器的子任务时，它在 *<prompt_i.j>* 标签内指定该任务。每关闭一个 *</prompt_i.j>* 标签，一个执行器便基于当前累积上下文快照启动相应任务。

2. 并行执行。每个执行器独立且并发地执行其被分配的子任务，生成一条思维链推理轨迹来完成特定任务。与串行处理相比，并行执行这些子任务显著减少了串行生成的 token 总数，大幅提升推理效率。

3. 同步。一旦所有并行执行完成，各执行器的结果被 *<execution_i.j>* 标签包裹，清晰标示其对应任务。这些结果按其原始提示定义的顺序同步回累积上下文。更新后的上下文随后反馈给规划器，由其开启下一阶段或输出最终答案结束推理。

### 3.2 为 Sprint 框架训练推理模型

为有效训练推理模型在推理时识别并利用并行化机会，我们开发了一条数据构建管线，将完整的自然语言推理轨迹转换为「滚动视界规划 + 并行执行」的结构化轮次。该管线提取单个规划与执行步骤、按依赖关系组织成阶段，并生成同时涵盖串行规划与并行执行两方面的训练样本。管线概览见图 2。管线中每一步的详细提示见附录 A。

![Refer to caption](2506.05745v2/SPRINT_Training_overview.png)

图 2：Sprint 训练管线概览：(0) 从原始推理轨迹出发，(1) 首先提取单个推理步骤并识别其规划与执行阶段；接着 (2) 构建表示步骤间依赖关系的 DAG，然后 (3) 将步骤分组成可并行执行的紧凑阶段；最后 (4) 在过滤并将这些结构化阶段重格式化为训练样本后，我们对推理模型进行监督微调，使其能动态提出并执行可并行化的任务。

1. 步骤提取。给定由 DeepSeek-R1（Guo et al., 2025）针对查询 $Q$ 生成的推理轨迹 $\tau$，我们通过向一个 LLM（此处为 GPT-4o）提供特定指令，将其分解为不同的步骤 $S=\{S_{1},S_{2},\dots,S_{n}\}$；参见附录 A.2。每个步骤 $S_{i}$ 进一步分解为规划阶段（$P_{i}$，R1 在其中识别任务与策略）与执行阶段（$E_{i}$，其中执行规划好的任务）。注意，有些步骤可能只涉及规划而无显式执行；这类步骤称为*纯规划步骤*（plan-only step），不为它们生成执行器指令。

   为抑制琐碎的执行器调用，我们将非常短的执行合并回其规划阶段，使其成为纯规划步骤，鼓励规划器独立处理更简单的任务。

2. DAG 构建。接下来，我们通过提示一个较小的 LLM（GPT-4o-mini）判断哪些步骤依赖其他步骤来识别步骤间的依赖；指令见附录 A.2。这些依赖形式化表示为：

$$D=\{(S_{i},S_{j})\mid S_{j}\text{ 依赖于 }S_{i},\ i<j,\ S_{i},S_{j}\in S\}.$$

   这组依赖构成一个有向无环图（DAG），记为 $G=(S,D)$，其中节点表示单个步骤，边表示步骤间的依赖。

3. 装箱（packing）。我们将步骤分组为若干阶段，每个阶段包含可由规划器同时生成的计划以及可由执行器并发执行的执行。朴素做法会仅依据步骤在 DAG 中的深度来分组，而我们进一步优化阶段安排：观察到若节点 $S_{i}$ 的父节点 $S_{p}$ 是纯规划步骤，则 $S_{i}$ 可以安全地与 $S_{p}$ 放入同一阶段。这一优化既确保上下文可用性又提升并行化效率。有关此调整的更多细节见附录 A.2。

   形式化地，每个步骤 $S_{i}=(P_{i},E_{i})$ 的阶段编号 $\sigma(S_{i})$ 定义为：

$$\sigma(S_{i})=\begin{cases}1,&\text{若 }S_{i}\text{ 无父节点}\\ \max\limits_{S_{p}\in\text{Parents}(S_{i})}\left(\sigma(S_{p})+\mathbb{1}(E_{p}\neq\emptyset)\right),&\text{否则}\end{cases}$$

   给定阶段 $k$ 的步骤集合由所有阶段编号 $\sigma(S_{i})=k$ 的步骤组成，表示为：

$$\mathcal{L}^{(k)}=\{S_{i}\in S\mid\sigma(S_{i})=k\}.$$

   在每个阶段 $k$ 内，合并计划通过按原始顺序拼接 $\mathcal{L}^{(k)}$ 中所有步骤 $S_{i}$ 的计划构成。阶段 $k$ 的执行部分包括所有步骤的执行成分（纯规划步骤除外）：

$$\mathcal{P}^{(k)}=\text{concat}(P_{i}\mid S_{i}\in\mathcal{L}^{(k)}),\quad\mathcal{E}^{(k)}=\{E_{i}\mid S_{i}\in\mathcal{L}^{(k)},E_{i}\neq\emptyset\},$$

   其中 $E_{i}=\emptyset$ 表示 $S_{i}$ 是纯规划步骤。

4. 训练 LRM。为确保模型从具有显著并行化潜力的轨迹中学习，我们引入*并行化比率*，定义为 $(\#\text{steps})/(\#\text{stages})$，并丢弃比率低于 1.5 的轨迹。选出的轨迹被重格式化为逐阶段的计划与执行序列，按图 3 所示顺序以显式标签（*<Plan_i>* 与 *<execution_i.j>*）包裹。最后，我们在重格式化后的思考模式上微调 LRM。通过这一过程，模型学会基于先前的计划与执行序列动态提出独立、可并行化的任务，并按照对应提示有效执行每个任务。

图 3：推理期间解码的串行 token 比较。串行推理模型按顺序生成所有步骤，导致很长的 token 序列。Sprint 的微调数据将这些步骤重组为若干阶段，将可并行的计划与其相应执行分组。这种组织方式使 Sprint 的推理框架能够并行执行这些成组的步骤，显著减少串行 token 数量。

**方法概览。** 总体而言，如第 3.2 节所述，Sprint 训练推理模型提出可并行化的子任务，而非串行生成其完整推理轨迹。在推理时，如第 3.1 节所述，训练后的模型能有效管理长程相互依赖，同时显著减少生成的串行 token 数量。图 3 展示了这一工作流程，突出显示了 Sprint 如何在训练期间将串行推理轨迹重组为可并行的阶段，并随后在推理时利用这种学到的并行结构进行高效的并发执行。Sprint 推理与串行推理轨迹的对比示例见附录 B。

## 4 实验

### 4.1 实验设置

**数据集。** 为训练模型，我们从 DeepSeek-R1（Guo et al., 2025）在 MATH 数据集（Hendrycks et al., 2021）训练集上生成的 6,000 条推理轨迹开始，这些轨迹由 open-r1 (2025) 发布。在按最终答案的正确性过滤这些轨迹并经过我们的数据构建管线（第 3.2 节）处理后，我们得到约 1,700 个训练样本。

评估方面，我们主要使用 MATH-500 基准（Lightman et al., 2023a），这是一个由 500 道数学推理题组成、被广泛认可的测试集。为进一步检验 Sprint 在更具挑战性与分布外场景的泛化能力，我们在另外两个基准上对照强基线模型评估其表现。首先，我们在 GPQA-diamond（Rein et al., 2023）上评估——该数据集来自生物学、物理学与化学等完全不同的科学领域，从而考察跨领域推理的稳健性。此外，遵循 Pan et al. (2025) 与 Yao et al. (2023a) 的做法，我们在 Countdown（Yao et al., 2023a）的 1,000 个样本子集上测试 Sprint；这是一项合成数值推理任务，模型必须用算术运算（$+,-,\times,\div$）从四个给定数字推导出目标数字。

**基线。** 我们将 Sprint 与多个采用串行和并行采样策略的推理基线进行比较：

1. 基座推理模型（DeepSeek-R1-Distill-Qwen-7B）（Guo et al., 2025）：该模型是将主 R1 推理模型蒸馏到 Qwen-2.5-7B（Yang et al., 2024）的产物，由 DeepSeek 发布。我们既将该推理模型用作直接比较的基线，也将其作为微调实验的基座模型。

2. 推理微调模型（RFT）：为控制训练数据的影响并与常规蒸馏方法比较，我们用与训练 Sprint 相同的 1,700 条来自 MATH 的 R1 推理轨迹，对 DeepSeek-R1-Distill-Qwen-7B 进行监督微调。该模型代表 Qwen-2.5-7B 在 MATH 数据集 R1 轨迹上的标准持续蒸馏。

3. Skeleton-of-Thought（SoT）（Ning et al., 2023）：给定一个查询，SoT 将其分解为子任务，并在单个阶段内通过并行 LLM 调用执行。子任务生成与执行过程均依赖现成的 LLM，无需任何任务特定的微调。我们用 chat-instruct 版 Qwen-2.5-7B 模型（记为 SoT-chat）与面向推理的 DeepSeek-R1-Distill-Qwen-7B 模型（记为 SoT-reasoning）分别评估 SoT。

4. 重复采样 + 自洽性（Brown et al., 2024；Wang et al., 2023）：我们纳入结合自洽性聚合的重复采样作为基线，以评估纯并行采样方法能否达到与 Sprint 交错规划执行框架相当的准确率与效率。

**评估指标。** 我们考虑两个指标来评估各方法的性能与效率。第一，最终答案相对于下游任务的准确率，计算为每种方法正确回答查询的百分比（细节见附录 A.4）。第二，为评估延迟方面的效率改进，我们测量每种方法生成的串行 token 数量。特别地，对串行推理基线，串行 token 数恰为输出 token 数。对 Sprint，我们如下计算串行 token：

$$\text{number of sequential tokens}=\sum_{i=1}^{\text{\# stages}}\max_{k}^{\text{\# prompts at stage }i}(P_{i.k}+E_{i.k}),$$

其中 $P_{i.k}$ 与 $E_{i.k}$ 分别表示规划器在第 $i$ 步生成到第 $k$ 个提示结束时的串行 token 数，以及某个执行器在第 $i$ 步第 $k$ 次执行的串行 token 数。注意理想墙钟时间与每种方法生成的串行 token 数相关；但准确测量该指标需要更高的计算资源，我们在第 5 节进一步讨论。

### 4.2 结果

图 4：在 MATH-500 上各方法的准确率（%）与串行 token 数比较的帕累托图。Sprint 的准确率略高于 RFT 模型，同时平均少生成 440（约 15%）个 token。

图 5：MATH-500 中各难度级别的问题在到达最终答案前经历各交错规划阶段的比例。虚线表示各阶段中表现出并行性（多于一个计划）的问题数量。

|  | 分布内 |  |  | 分布外 |  |  |
| --- | --- | --- | --- | --- | --- | --- |
|  | MATH-500 |  |  | Countdown |  | GPQA-Diamond |
| 方法 | 准确率↑ | # 串行↓ | # 总数↓ | 准确率↑ | # 串行↓ | 准确率↑ | # 串行↓ |
| Self-consistency | 80.5 | 590 | 11645 | 78.5 | 2845 | 45.4 | 4735 |
| SoT-chat | 47.3 | 256 | 1290 | 80.0 | 2367 | 49.4 | 3526 |
| SoT-reasoning | 90.8 | 3836 | 11538 | 82.4 | 5823 | 48.0 | 7560 |
| RFT | 91.0 | 2880 | 2880 | 84.9 | 4917 | 50.5 | 7103 |
| Sprint | 92.5 | 2440 | 3622 | 85.9 | 2284 | 51.0 | 6336 |

表 2：MATH-500、GPQA-Diamond 与 Countdown 任务上 pass@1 准确率与串行 token 数的比较。Sprint 仅在数学推理上微调，但仍在 Countdown 与 GPQA-Diamond 这两个分布外任务上展现出强大的泛化能力。Sprint 还通过并行化执行减少了串行 token 数，而总 token 数没有大幅增加。

**与常规蒸馏的比较。** 图 4 展示了各方法在 MATH-500 基准上的准确率与平均串行 token 数。我们观察到，在 DeepSeek-R1 生成的轨迹上微调我们的基座模型（R1-Distill-7B）提升了 Sprint 与 RFT 的准确率，尽管其平均串行 token 数有所增加。准确率增益显著，使两个模型都接近大得多的 R1-Distill-32B 推理模型的性能。值得注意的是，Sprint 取得了 92.5% 的更高准确率，这可归因于每个阶段内的独立执行防止了一个结果影响另一个。尽管与 RFT 在相同的轨迹上微调（仅重组为规划-执行格式），Sprint 由于并行化执行少需要 440（约 15%）个串行 token。这些结果表明，Sprint 在实现与 RFT 所用常规蒸馏同等推理准确率的同时，大幅减少了串行 token 数。

**交错规划的有效性。** SoT-reasoning 基线在准确率与串行 token 数上均逊于 Sprint。由于 SoT 只允许单轮规划且使用未经任务特定微调的模型，它经常生成相互依赖的子任务。当模型独立并行执行它们时，无法用一个执行的结果指导另一个，导致子任务间的冗余计算，总 token 数几乎是 Sprint 的三倍（见表 2）。类似地，结合自洽性的重复采样对同一查询生成多个独立响应，导致很高的总 token 数。相比之下，Sprint 在多个阶段上使用交错规划与执行，每个阶段的计划基于先前执行的结果生成，实现了更好的协调。图 5 展示了 Sprint 交错规划的模式。正如预期，更难的问题在到达最终答案前需要更多阶段。此外，Sprint 在早期阶段生成更多计划——模型探索多种策略并识别相关子任务——而后期阶段更具确定性。

**串行 token 数的减少。** 我们在图 6 中进一步考察了 Sprint 相对 RFT 的串行 token 减少。对于推理轨迹较短的问题，额外的提示与计划/执行标签带来少量开销，导致串行 token 增加 5%。但随着问题难度增加、推理轨迹变长，由于并行执行，Sprint 相对 RFT 轨迹长度持续减少串行 token 数。特别地，在 RFT 平均需要超过 8,000 个 token 的问题上，Sprint 实现了 39% 的串行 token 减少。

**运行时间的降低。** 串行 token 的节省直接转化为更低的延迟。我们通过将每个计划/执行开始时的首 token 延迟（TTFT）开销加上随后的解码时间来估计每题运行时间。实践中解码占主导；预填充（TTFT）成本相对较小。在此估计下，Sprint 在 MATH-500 上比 RFT 快 9%（每题 36.92 秒 vs. 40.57 秒），在长推理链子集上快 38%（74.47 秒 vs. 120.54 秒）。由于运行时间主要随解码 token 数扩展，Sprint 的优势随轨迹长度增加而增大，在更难的样本上带来更大的绝对与相对延迟降低。

**泛化。** 为评估 Sprint 对分布外任务的泛化能力，我们在表 2 中报告 Countdown 与 GPQA-Diamond 上的表现。Sprint 利用 Countdown 任务高度可并行的特性，用少得多的串行 token 解决问题（2,284 个 token，相比之下 RFT 为 4,917 个），减少幅度达 53.5%。值得注意的是，这些并行化机会是在未接受该任务轨迹训练的情况下被识别出来的。得益于独立探索与交错规划，Sprint 还击败所有基线方法，达到 85.9% 的准确率。类似地，在 GPQA-Diamond 数据集上，Sprint 取得最高准确率（51.0%），同时相对 RFT 减少串行 token 数 10.8%。与 MATH-500 类似，我们从图 6 观察到，Sprint 在推理链较长的问题上提供更高的效率增益。

图 6：Sprint 实现的串行 token 减少。x 轴为 RFT 基线模型生成的串行 token 数，y 轴为 Sprint 实现的串行 token 平均减少量。随着基线的串行需求增加，Sprint 找到更大的并行化机会，带来更大的串行 token 减少。

## 5 局限与未来工作

**面向实际墙钟时间加速的硬件优化。** Sprint 带来了明确的效率增益——减少串行 token 并降低我们的端到端运行时估计——但要在墙钟时间上完全实现这些收益，需要硬件感知的优化。先前工作（Jin et al., 2025；Rodionov et al., 2025；Pan et al., 2025）表明串行 token 数与墙钟延迟密切相关。然而，要在实践中取得理想的延迟改进，需要优化的键值缓存机制与高带宽 GPU 互连，尤其是通用任务中遇到的长推理轨迹。此外，同时执行大量并行任务需要相应数量的 GPU。由于资源有限，我们无法为 Sprint 实现最优的硬件加速解码。未来工作可以探索在优化缓存框架与可扩展 GPU 架构中实现 Sprint，以充分实现并行解码策略带来的实际墙钟时间效率增益。

**推理模型中工具使用的并行化。** 在当前工作中，我们主要将执行视为模型为完成任务而解码的 token 序列。然而，从规划的角度看，这些执行也可以被看作接收特定任务并返回相应执行结果的黑盒模块。若干先前工作，如 ReAct（Yao et al., 2023b）、Self-Ask（Press et al., 2023）、Swirl（Goldie et al., 2025）等（Shi et al., 2025；Shen et al., 2023；Paranjape et al., 2023），引入了让语言模型把工具使用整合进推理循环的机制——迭代地规划、调用外部工具或 API，然后基于所得结果继续推理。这类推理-工具交互轨迹可以从并行化中显著受益，尤其是在工具调用主导解码延迟的场景。未来工作可以扩展 Sprint 的数据构建管线以容纳这类轨迹，训练模型在推理过程中有效并发地调用多个工具或 API。

**超越监督训练。** 通过在精选数据上的监督微调（SFT），我们的模型学会了如何定义可并行的计划，有效减少了串行 token 生成。然而，可实现的并行性天然受限于训练数据的质量。未来工作可以探索延迟感知的强化学习（RL），使用基于推理效率的奖励信号，让模型自主发现超越示范数据约束的、进一步增强并行推理的策略。

## 6 结论

在本工作中，我们提出了 Sprint——一个用于后训练推理语言模型的框架，它将推理轨迹重组为一系列计划与并行化执行。此外，Sprint 引入了一种推理机制，利用训练后的推理模型识别独立子任务并并行执行它们。该方法显著减少了串行 token 数量，同时取得与推理微调（RFT）模型相当的先进性能。值得注意的是，在需要大量推理轨迹的问题上，Sprint 揭示出更大的并行化潜力，实现 39% 的串行 token 减少。此外，我们在多个分布外任务上评估了模型的泛化能力，一致发现 Sprint 在保持与 RFT 相当性能的同时生成显著更少的串行 token。这些结果表明，Sprint 训练在具有更长推理轨迹的多样领域中解锁了模型的并行化推理能力。

## 7 致谢

本工作部分由美国空军科学研究办公室（AFOSR）资助（Grant FA9550-23-1-0251），部分由美国海军研究办公室资助（Grant N00014-24-1-2164）。我们还感谢伊利诺伊大学厄巴纳-香槟分校的 Yuhao Ge 在模型训练过程与计算需求方面提供的指导。

## 参考文献

- Besta et al. (2024)
  M. Besta, N. Blach, A. Kubicek, R. Gerstenberger, M. Podstawski, L. Gianinazzi, J. Gajda, T. Lehmann, H. Niewiadomski, P. Nyczyk, et al.
  Graph of thoughts: solving elaborate problems with large language models.
  In Proceedings of the AAAI Conference on Artificial Intelligence,
  Vol. 38, pp. 17682–17690.
- Bi et al. (2025)
  Z. Bi, K. Han, C. Liu, Y. Tang, and Y. Wang
  Forest-of-thought: scaling test-time compute for enhancing llm reasoning.
  External Links: 2412.09078,
  [Link](https://arxiv.org/abs/2412.09078)
- Brown et al. (2024)
  B. Brown, J. Juravsky, R. Ehrlich, R. Clark, Q. V. Le, C. Ré, and A. Mirhoseini
  Large language monkeys: scaling inference compute with repeated sampling.
  arXiv preprint arXiv:2407.21787.
- Cobbe et al. (2021)
  K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al.
  Training verifiers to solve math word problems.
  arXiv preprint arXiv:2110.14168.
- Dettmers et al. (2023)
  T. Dettmers, A. Pagnoni, A. Holtzman, and L. Zettlemoyer
  Qlora: efficient finetuning of quantized llms.
  Advances in neural information processing systems 36, pp. 10088–10115.
- Du et al. (2023)
  Y. Du, S. Li, A. Torralba, J. B. Tenenbaum, and I. Mordatch
  Improving factuality and reasoning in language models through multiagent debate.
  In Forty-first International Conference on Machine Learning,
- Goldie et al. (2025)
  A. Goldie, A. Mirhoseini, H. Zhou, I. Cai, and C. D. Manning
  Synthetic data generation & multi-step rl for reasoning & tool use.
  External Links: 2504.04736,
  [Link](https://arxiv.org/abs/2504.04736)
- Guo et al. (2025)
  D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, et al.
  Deepseek-r1: incentivizing reasoning capability in llms via reinforcement learning.
  arXiv preprint arXiv:2501.12948.
- Hendrycks et al. (2021)
  D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt
  Measuring mathematical problem solving with the math dataset.
  External Links: 2103.03874,
  [Link](https://arxiv.org/abs/2103.03874)
- Hu et al. (2022)
  E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen, et al.
  Lora: low-rank adaptation of large language models..
  ICLR 1 (2), pp. 3.
- Jin et al. (2025)
  T. Jin, E. Y. Cheng, Z. Ankner, N. Saunshi, B. M. Elias, A. Yazdanbakhsh, J. Ragan-Kelley, S. Subramanian, and M. Carbin
  Learning to keep a promise: scaling language model decoding parallelism with learned asynchronous decoding.
  External Links: 2502.11517,
  [Link](https://arxiv.org/abs/2502.11517)
- Juneja et al. (2024)
  G. Juneja, S. Dutta, S. Chakrabarti, S. Manchanda, and T. Chakraborty
  Small language models fine-tuned to coordinate larger language models improve complex reasoning.
  External Links: 2310.18338,
  [Link](https://arxiv.org/abs/2310.18338)
- Kim et al. (2024)
  S. Kim, S. Moon, R. Tabrizi, N. Lee, M. W. Mahoney, K. Keutzer, and A. Gholami
  An llm compiler for parallel function calling.
  In Forty-first International Conference on Machine Learning,
- Kwon et al. (2023)
  W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. Gonzalez, H. Zhang, and I. Stoica
  Efficient memory management for large language model serving with pagedattention.
  In Proceedings of the 29th Symposium on Operating Systems Principles,
  pp. 611–626.
- Lightman et al. (2023a)
  H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe
  Let’s verify step by step.
  arXiv preprint arXiv:2305.20050.
- Lightman et al. (2023b)
  H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe
  Let’s verify step by step.
  External Links: 2305.20050,
  [Link](https://arxiv.org/abs/2305.20050)
- Liu et al. (2024)
  M. Liu, A. Zeng, B. Wang, P. Zhang, J. Tang, and Y. Dong
  APAR: llms can do auto-parallel auto-regressive decoding.
  External Links: 2401.06761,
  [Link](https://arxiv.org/abs/2401.06761)
- Ning et al. (2023)
  X. Ning, Z. Lin, Z. Zhou, Z. Wang, H. Yang, and Y. Wang
  Skeleton-of-thought: prompting llms for efficient parallel generation.
  arXiv preprint arXiv:2307.15337.
- open-r1 (2025)
  open-r1
  OpenThoughts-114k-math.
  External Links: [Link](https://huggingface.co/datasets/open-r1/OpenThoughts-114k-math)
- OpenAI (2024)
  OpenAI
  Learning to reason with llms.
  External Links: [Link](https://openai.com/index/learning-to-reason-with-llms/)
- Pan et al. (2025)
  J. Pan, X. Li, L. Lian, C. Snell, Y. Zhou, A. Yala, T. Darrell, K. Keutzer, and A. Suhr
  Learning adaptive parallel reasoning with language models.
  External Links: 2504.15466,
  [Link](https://arxiv.org/abs/2504.15466)
- Paranjape et al. (2023)
  B. Paranjape, S. Lundberg, S. Singh, H. Hajishirzi, L. Zettlemoyer, and M. T. Ribeiro
  ART: automatic multi-step reasoning and tool-use for large language models.
  External Links: 2303.09014,
  [Link](https://arxiv.org/abs/2303.09014)
- Prasad et al. (2024)
  A. Prasad, A. Koller, M. Hartmann, P. Clark, A. Sabharwal, M. Bansal, and T. Khot
  ADaPT: as-needed decomposition and planning with language models.
  External Links: 2311.05772,
  [Link](https://arxiv.org/abs/2311.05772)
- Press et al. (2023)
  O. Press, M. Zhang, S. Min, L. Schmidt, N. A. Smith, and M. Lewis
  Measuring and narrowing the compositionality gap in language models.
  External Links: 2210.03350,
  [Link](https://arxiv.org/abs/2210.03350)
- Rajbhandari et al. (2020)
  S. Rajbhandari, J. Rasley, O. Ruwase, and Y. He
  Zero: memory optimizations toward training trillion parameter models.
  In SC20: International Conference for High Performance Computing, Networking, Storage and Analysis,
  pp. 1–16.
- Rasley et al. (2020)
  J. Rasley, S. Rajbhandari, O. Ruwase, and Y. He
  Deepspeed: system optimizations enable training deep learning models with over 100 billion parameters.
  In Proceedings of the 26th ACM SIGKDD international conference on knowledge discovery & data mining,
  pp. 3505–3506.
- Rein et al. (2023)
  D. Rein, B. L. Hou, A. C. Stickland, J. Petty, R. Y. Pang, J. Dirani, J. Michael, and S. R. Bowman
  GPQA: a graduate-level google-proof q&a benchmark.
  External Links: 2311.12022,
  [Link](https://arxiv.org/abs/2311.12022)
- Rodionov et al. (2025)
  G. Rodionov, R. Garipov, A. Shutova, G. Yakushev, V. Egiazarian, A. Sinitsin, D. Kuznedelev, and D. Alistarh
  Hogwild! inference: parallel llm generation via concurrent attention.
  External Links: 2504.06261,
  [Link](https://arxiv.org/abs/2504.06261)
- Saad-Falcon et al. (2024)
  J. Saad-Falcon, A. G. Lafuente, S. Natarajan, N. Maru, H. Todorov, E. Guha, E. K. Buchanan, M. Chen, N. Guha, C. Ré, and A. Mirhoseini
  Archon: an architecture search framework for inference-time techniques.
  External Links: 2409.15254,
  [Link](https://arxiv.org/abs/2409.15254)
- Shen et al. (2023)
  Y. Shen, K. Song, X. Tan, D. Li, W. Lu, and Y. Zhuang
  HuggingGPT: solving ai tasks with chatgpt and its friends in hugging face.
  External Links: 2303.17580,
  [Link](https://arxiv.org/abs/2303.17580)
- Shi et al. (2025)
  Z. Shi, S. Gao, L. Yan, Y. Feng, X. Chen, Z. Chen, D. Yin, S. Verberne, and Z. Ren
  Tool learning in the wild: empowering language models as automatic tool agents.
  External Links: 2405.16533,
  [Link](https://arxiv.org/abs/2405.16533)
- Shinn et al. (2023)
  N. Shinn, F. Cassano, E. Berman, A. Gopinath, K. Narasimhan, and S. Yao
  Reflexion: language agents with verbal reinforcement learning.
  External Links: 2303.11366,
  [Link](https://arxiv.org/abs/2303.11366)
- Teng et al. (2025)
  F. Teng, Z. Yu, Q. Shi, J. Zhang, C. Wu, and Y. Luo
  Atom of thoughts for markov llm test-time scaling.
  arXiv preprint arXiv:2502.12018.
- Valmeekam et al. (2023)
  K. Valmeekam, S. Sreedharan, M. Marquez, A. Olmo, and S. Kambhampati
  On the planning abilities of large language models (a critical investigation with a proposed benchmark).
  External Links: 2302.06706,
  [Link](https://arxiv.org/abs/2302.06706)
- [35]
  X. Wang, J. Wei, D. Schuurmans, Q. V. Le, E. H. Chi, S. Narang, A. Chowdhery, and D. Zhou
  Self-consistency improves chain of thought reasoning in language models.
  In The Eleventh International Conference on Learning Representations,
- Wei et al. (2023)
  J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. Chi, Q. Le, and D. Zhou
  Chain-of-thought prompting elicits reasoning in large language models.
  External Links: 2201.11903,
  [Link](https://arxiv.org/abs/2201.11903)
- Yang et al. (2024)
  A. Yang, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Li, D. Liu, F. Huang, H. Wei, et al.
  Qwen2. 5 technical report.
  arXiv preprint arXiv:2412.15115.
- Yao et al. (2023a)
  S. Yao, D. Yu, J. Zhao, I. Shafran, T. Griffiths, Y. Cao, and K. Narasimhan
  Tree of thoughts: deliberate problem solving with large language models.
  Advances in neural information processing systems 36, pp. 11809–11822.
- Yao et al. (2023b)
  S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao
  React: synergizing reasoning and acting in language models.
  In International Conference on Learning Representations (ICLR),
- Zelikman et al. (2022)
  E. Zelikman, Y. Wu, J. Mu, and N. Goodman
  Star: bootstrapping reasoning with reasoning.
  Advances in Neural Information Processing Systems 35, pp. 15476–15488.
- Zhao et al. (2024)
  Y. Zhao, J. Huang, J. Hu, X. Wang, Y. Mao, D. Zhang, Z. Jiang, Z. Wu, B. Ai, A. Wang, W. Zhou, and Y. Chen
  SWIFT:a scalable lightweight infrastructure for fine-tuning.
  External Links: 2408.05517,
  [Link](https://arxiv.org/abs/2408.05517)
- Zhou et al. (2022)
  D. Zhou, N. Schärli, L. Hou, J. Wei, N. Scales, X. Wang, D. Schuurmans, C. Cui, O. Bousquet, Q. Le, et al.
  Least-to-most prompting enables complex reasoning in large language models.
  arXiv preprint arXiv:2205.10625.
- Zhu et al. (2023)
  B. Zhu, H. Sharma, F. V. Frujeri, S. Dong, C. Zhu, M. I. Jordan, and J. Jiao
  Fine-tuning language models with advantage-induced policy alignment.
  arXiv preprint arXiv:2306.02231.
- Zhuge et al. (2024)
  M. Zhuge, W. Wang, L. Kirsch, F. Faccio, D. Khizbullin, and J. Schmidhuber
  GPTSwarm: language agents as optimizable graphs.
  In Proceedings of the 41st International Conference on Machine Learning,

## 附录 A 实现细节

### A.1 推理

#### 从串行推理模型推理。

为从 DeepSeek-R1-Distill-7B 与 RFT 模型等串行推理模型生成回复，我们使用下面提供的提示词。同一提示词也用于微调 DeepSeek-R1-Distill-7B 以得到 RFT 模型。推理时，问题被追加到提示词之后，模型以补全（completions）格式调用。遵循 DeepSeek 的建议，我们将生成温度设为 0.6 以缓解重复输出。此外，我们强制每个回复的 token 上限为 36,000，超出该阈值的输出会被截断。

Sequential Reasoning Prompt

Your role as an assistant involves thoroughly exploring questions through a systematic long thinking process before providing the final precise and accurate solutions. This requires engaging in a comprehensive cycle of analysis, summarizing, exploration, reassessment, reflection, backtracking, and iteration to develop well-considered thinking process.

Please structure your response into two main sections: Thought and Solution.

•

In the Thought section, detail your reasoning process using the specified format: <think> {thought with steps separated with "\n \n"} </think> Each step should include detailed considerations such as analyzing questions, summarizing relevant findings, brainstorming new ideas, verifying the accuracy of the current steps, refining any errors, and revisiting previous steps.
•

In the Solution section, based on various attempts, explorations, and reflections from the Thought section, systematically present the final solution that you deem correct. The solution should remain a logical, accurate, concise expression style and detail necessary step needed to reach the conclusion.
Now, try to solve the following question through the above guidelines. Return your final response within \boxed{}.

#### SPRINT 推理。

推理时，我们使用以下提示词引导 SPRINT 模型生成计划与执行。尽管模型经过微调可在单次生成中产出整条轨迹——包括所有计划与执行——我们通过管理模型调用与输出 token 处理，在规划器与执行器角色之间有效切换。

为把模型输出限制为每次调用仅一个计划或执行，我们使用特定的停止 token。一旦模型产生以下任一字符串（表示一个计划或执行片段完成），生成就终止：{</Execution_, </Plan_, </Final_answer>, </execution_}。

为第 $i$ 阶段生成计划时，我们把提示词连同输入查询与累积上下文（包括之前所有计划与执行）一起输入 Sprint 模型。相反，为生成对应某个 prompt_i.j 的执行，我们向模型提供提示词、输入查询、第 $i-1$ 阶段之前所有已生成的计划与执行，以及第 $i$ 阶段计划中到 prompt_i.j 结束为止的文本。这种结构化的上下文管理使我们能够在规划与执行任务之间无缝复用同一提示词。

模型最多被允许 12 个阶段来产出最终答案。为强制这一约束，我们在第 12 阶段调用模型时于提示词末尾追加 "<Final_answer>\n"。每个计划或执行的生成回复上限为 8,000 个 token，超出的 token 会被相应截断。该提示词与模型微调时使用的完全相同。

SPRINT Prompt

You are an AI system that follows a systematic long thinking process to arrive at the precise and accurate answer to the below math question specified within <Question> and </Question> tags. The solution is generated over multiple phases, where each phase consists of a plan and an execution.

#### Planning.

At phase p, you must first create a plan within <Plan_p> and </Plan_p> tags by thinking out loud and planning the tasks that need to be executed next.

•

Your plan may involve detailed considerations such as analyzing the question, summarizing relevant findings, brainstorming new/alternative approaches, verifying the accuracy of the current steps, refining any errors, or revisiting previous steps.
•

Since you may think about multiple aspects of the problem within the same plan, you must insert a line break using "- - - - -" before you transition from one train of thought to another.
•

While generating the plan, if you identify a task that needs to be executed, you must create a prompt that clearly specifies the task within <prompt_p.k> and </prompt_p.k> tags where k starts from 1.
•

When planning within each phase, you must create prompts that can be run independent of the results from the other prompts, to achieve speedup through parallelization. You must also try to minimize the number of phases required further to arrive at the accurate final answer.

#### Execution.

After creating the plan, you must carry out the tasks identified in the plan sequentially within <Execution_p> and </Execution_p> tags. For the prompt labeled as prompt_p.k, the corresponding execution must be generated within <execution_p.k> and </execution_p.k> tags.

If the plans and execution results you receive are sufficient to generate the accurate final answer, you must respond with the final answer within <Final_answer> and </Final_answer> tags. The numerical answer must be within \boxed{}.

### A.2 数据构建

#### 步骤提取。

步骤提取使用 GPT-4o 模型，温度设为 0。以下提示词用于从 DeepSeek R1 生成的推理轨迹中提取步骤。在提示词中，我们用「Component（组件）」一词指代提取的步骤，以防止模型将其与传统意义上数学解法中的「step（步骤）」混淆——后者可能是单次运算，而非解答的一个逻辑部分。这里定义的组件可以涉及如下任务：确定后续行动、验证先前结果、提出备选方法，或比较不同策略得出的解。对每个组件，模型先「边想边说」思考需要做什么，然后执行所识别的任务。我们把前一部分称为计划、后一部分称为执行，并使用此提示词分别提取它们。

传给模型作为输入的推理轨迹经过格式化，每行/句都被标注唯一的行号，模型为每个组件内的计划与执行提供行号范围。这最大限度地减少了模型必须生成的输出 token 数量，从而降低成本。行号随后从回复中解析，以推断与每个计划或执行相关的文本块。

Step Extraction Prompt

Given below is a math problem and a well-thought out solution to the problem generated by an AI model. The solution contains multiple components (progressing with next steps, verifying past steps, proposing alternative methods, comparing solutions across different methods, etc.). Within each component, there are three phases:

•

Planning: Here, the model first thinks out loud and plans what it needs to do.
•

Execution: Here,the model follows the plan and executes it.
•

Commenting: Here, the model comments on the execution results with phrases such as "Yes, that seems right", "Both methods lead to the same answer, etc.
Note that the verification of an execution should be considered as a separate component and not as the commenting phase of the same component.

I am building a new AI system to solve such math problems. This system will consist of two separate AI models – a planner and an executor.

•

Planner: The planner will receive all the components of the solution completed so far and will need to think aloud and generate a plan for the next component. Then, it needs to provide a prompt to the executor model to execute a specific task.
•

Executor: The executor will receive all the components of the solution completed so far, the plan for the next component generated by the planner, and the prompt generated by the planner. It will need to execute the specified task.
To train these two AI models, I must generate training data by breaking down the solution provided below into individual components. For each component, clearly provide the following details:

Required Response Format:
### Component X (Line Number Range)

•

Description: Brief explanation of what this component achieves.
•

Plan: Lines (minimal number of lines to describe the plan clearly).
•

Prompt: A precise, actionable instruction for the executor based explicitly on the above plan.
•

Execution: Lines (specific line numbers performing the planned task).
•

Comment: Lines (reflective comments or Lines not found if missing).

Important Notes:

•

The planning phase should only include a minimal number of lines required to specify what needs to be done. The remaining lines from the component where the model carries out the plan should be included in the execution phase.
•

There MUST be NO overlap between the line numbers of different components.
•

There MUST be NO overlap between the line numbers of the planning and execution phases of the same component.
•

All the lines in the solution should be covered by the components.
•

Use the line number mentioned at the start and end of each line to identify the line when specifying the line number range.
•

The prompt to the executor model must be a very specific instruction that the executor can follow to complete the required task. The executor must not perform more tasks than required. The prompt can refer to the plan for that component by saying "the above plan".
•

If the model does not comment on the execution results within a component, the corresponding bullet point can be written as Comment: Lines not found

#### DAG 构建。

DAG 构建使用 GPT-4o-mini 模型，温度设为 0。以下提示词用于以「父字典」的形式推断 DAG，其中每个键指代上面提取的一个步骤，对应的值指代该步骤所依赖的步骤。

DAG Creation Prompt

Given below is a well-thought out solution to a math problem generated by an AI system. The system consists of a planner and an executor. The planner model thinks out loud and plans the next component of the problem solution. Then, it provides a prompt along with the plan to an executor model. The executor then follows the instructions in the prompt and uses context from the plan to carry out the given task.
The solution consists of multiple components, each containing the following:

•

Description: A brief description of what the component does.
•

Plan: The plan generated by the planner.
•

Prompt: Instructions generated by the planner enclosed within <prompt> tags.
•

Execution: Output provided by the executor.
Though the executions are run sequentially in this solution, some of the executions may be parallelized to improve speed. Identify and explain which components can run in parallel and determine the best way to parallelize them to maximize speed. Note that parallel runs should not have co-dependency.

The parallelization schedule can be represented as a directed acyclic graph (DAG) where the nodes are the component numbers. You need to represent the DAG as a parent dictionary where each node is a key and its value is a list of nodes that point to it, i.e., the nodes that must be executed immediately before it. For a key node, do not include any nodes in its value that can be run in parallel with it.

Format of parent dictionary:

Let us consider a simple example. Suppose that the following constraints hold:

•

Component 1 needs to be run before any other component
•

Components 2, 3, 4 can be run in parallel after 1
•

Component 5 which depends on the results of 2 and 3 can be run after 2 and 3
•

Component 6 which depends on the results of 4 and 5 can be run after 4 and 5
The parent dictionary for this example *MUST* be represented as a python dictionary as follows:

```
parent_dictionary = {
    1: [],
    2: [1],
    3: [1],
    4: [1],
    5: [2, 3],
    6: [4, 5]
}
```

利用得到的 DAG，我们可以把组件重组成交错的计划与执行，得到可并行化的推理轨迹。一种简单策略是把处于同一 DAG 深度的组件分配到同一规划-执行阶段。不过，进一步的优化可以减少到达最终答案所需的阶段总数。

#### 装箱（packing）。

装箱的目标是为每个组件最优地分配阶段编号。为此，我们应用以下贪心启发式规则：

- 若某组件的执行少于三行，则直接与其对应计划合并。这一做法减少了额外提示编写与执行器调用的开销。通过在合并了短执行的轨迹上微调，规划器学会自己完成短小或琐碎的执行。
- 若组件 $C$ 依赖于纯规划组件 $P$，则 $C$ 的计划与 $P$ 所在阶段的执行结果无关。当 $C$ 的所有父组件都满足此条件时，通过合并各自的计划，把 $C$ 并入与 $P$ 相同的规划阶段。

由此我们得到每个组件的最优阶段编号，随后可用于生成微调轨迹。

### A.3 微调

我们通过在推理轨迹上训练进行模型的监督微调（SFT）。起初，我们尝试了 LoRA 与 qLoRA（Dettmers et al., 2023）等更高效的微调技术。但由于 LoRA 未能使模型充分遵循预期的响应格式，我们转而采用全量微调。

微调主要在单台配备八块 NVIDIA A100 GPU（每块 40 GB 显存）的机器上进行。我们使用 ms-swift 框架（Zhao et al., 2024）——Modelscope 社区提供的微调工具包。

每个模型微调 5 个 epoch。由于推理轨迹所需的长上下文与显存限制，训练期间 batch size 为 1。我们使用 bfloat16 精度、1×10⁻⁵ 的初始学习率以及 1×10⁻⁴ 的权重衰减因子。学习率调度包括前 5% 训练步数的线性预热，随后在其余训练迭代中线性衰减到零。模型评估每 100 步进行一次，并保留基于评估损失表现最佳的模型。

为优化训练期间的内存使用，我们集成了若干效率策略，尤其是 DeepSpeed ZeRO 冗余优化器（Rajbhandari et al., 2020；Rasley et al., 2020）与 4 比特量化。DeepSpeed 的 ZeRO 优化器提供一组内存分区策略，在内存节省与通信开销之间权衡。在许多工作负载中，ZeRO Stage 1 或 2 在内存效率与通信成本之间取得最佳平衡；但由于需要在长序列上训练，我们的单 GPU 内存需求超出了这些阶段所能支持的范围。因此，我们采用 ZeRO Stage 3 来以扩展上下文长度训练而不出现 OOM 错误。

### A.4 评估

模型评估方面，我们利用 vLLM（Kwon et al., 2023）来部署模型。具体而言，每个 7B 规模的模型（SPRINT、RFT 与 DeepSeek-R1-Distill-7B）部署在单块 40 GB 显存的 NVIDIA A100 GPU 上。

为提高评估准确性，我们指示模型把最终答案封装在 `\boxed{}` 中。在 MATH-500 与 Countdown 任务上，我们利用 Math-Verify 库与 SymPy 进行等价性检查，确保对数学上等价但表述不同的解具有稳健性。在 GPQA 任务中，准确率通过将显式生成的选项标签（如 A、B、C、D）与对应真值选项直接比较来确定。

尽管提供了显式的格式指令，我们偶尔观察到模型偏离指定的输出格式。例如，在 Countdown 任务评估中，模型偶尔产生意外格式的输出（如 `\times`、$\times$），使解析过程复杂化。为缓解这些问题，我们引入 GPT-4o-mini 模型作为辅助评估器，对照真值判定生成的答案。

### A.5 基线

下面给出我们研究中使用的基线的实现细节：

- SoT（Skeleton of Thought）：SoT-chat 使用 Qwen2.5-7B-Instruct 模型，温度设为 0.1。SoT-reasoning 使用 DeepSeek-R1-Distill-Qwen-7B 模型，温度设为 0.6。我们使用原论文报告的相同提示词（Ning et al., 2023）。完整解生成后，我们将其发送给 GPT-4o-mini 以提取用于评估的最终答案。
- RFT（推理微调模型）：该基线通过在串行 R1 轨迹上微调 DeepSeek 模型得到。推理时，我们设温度为 0.6，并采用附录 A.1 提供的串行推理提示词。
- 并行采样 + 自洽性：使用 Qwen2.5-7B-Instruct 模型，温度 0.3，每题生成 20 个独立样本。多数答案被视为该基线评估的预测答案。

## 附录 B 示例演示

### B.1 数据构建管线演示

为说明我们的数据构建管线，我们考察 MATH 训练集中的一个代表性例子。考虑以下问题：

问题：The vertex of the parabola described by the equation $y=-3x^{2}-30x-81$ is $(m,n)$. What is $n$?

接下来，我们给出 DeepSeek-R1 对该问题生成的回复，每个逻辑组件单独放在一个框中。注意，原始回复在其逻辑组件之间并无任何分隔，全文是作为一条长轨迹生成的。

Outline of DeepSeek-R1 response

Okay, so I need to find the vertex of the parabola given by the equation $y=-3x^{2}-30x-81$, and specifically determine the $n$-coordinate of the vertex, which is $(m,n)$. Hmm, let’s start by recalling how to find the vertex of a quadratic equation. I remember that quadratic equations are in the form $y=ax^{2}+bx+c$, and their graphs are parabolas. The vertex of a parabola can be found using the formula for the $x$-coordinate, which is $-b/(2a)$. Then once we have the $x$-coordinate, we can plug that back into the original equation to find the corresponding $y$-coordinate, which would be $n$ in this case.
So let’s identify $a$, $b$, and $c$ from the given equation. Comparing $y=-3x^{2}-30x-81$ with the standard form $y=ax^{2}+bx+c$, it looks like $a=-3$, $b=-30$, and $c=-81$.

Wait, is that right? Let me check again. The coefficient of $x^{2}$ is $-3$, so $a=-3$. The coefficient of $x$ is $-30$, so $b=-30$. The constant term is $-81$, so $c=-81$. Okay, that seems correct.

Now, using the formula for the $x$-coordinate of the vertex: $m=-b/(2a)$. Plugging in the values of $a$ and $b$, we get $m=-(-30)/(2*(-3))$. Let’s compute that step by step. The numerator is $-(-30)$, which is positive $30$. The denominator is $2$ times $a$, which is $2*(-3)=-6$. So $m=30/(-6)=-5$. Therefore, the $x$-coordinate of the vertex is $-5$. That seems straightforward.

Now, to find the $y$-coordinate $n$, I need to substitute $x=-5$ into the original equation. Let’s do that. The original equation is $y=-3x^{2}-30x-81$. Plugging in $x=-5$:
$y=-3*(-5)^{2}-30*(-5)-81$. Let’s compute each term step by step. First, $(-5)^{2}$ is $25$, so $-3*25$ is $-75$. Then, $-30*(-5)$ is positive $150$. And the last term is $-81$. So adding them up: $-75+150-81$. Let’s calculate this.
First, $-75+150=75$. Then, $75-81=-6$. So $n=-6$. Therefore, the vertex is at $(-5,-6)$, so $n$ is $-6$.

Wait, let me double-check my calculations to make sure I didn’t make any arithmetic errors. Let’s redo the substitution.
Calculating $y$ when $x=-5$:
First term: $-3*(-5)^{2}$. The exponent first: $(-5)^{2}=25$. Then multiply by $-3$: $-3*25=-75$. Second term: $-30*(-5)$. Multiply those: $-30$ times $-5$ is $150$. Third term is $-81$. So adding them: $-75+150=75$; $75-81=-6$. Yep, that’s correct.

Alternatively, maybe I can use another method to confirm. Sometimes, completing the square can be a good way to find the vertex. Let me try that. The given equation is $y=-3x^{2}-30x-81$. To complete the square, first factor out the coefficient of $x^{2}$ from the first two terms. So:
$y=-3(x^{2}+10x)-81$. Wait, let’s check: $-3x^{2}-30x$ becomes $-3(x^{2}+10x)$. Yes, that’s correct because $-3$ times $x^{2}$ is $-3x^{2}$ and $-3$ times $10x$ is $-30x$. Then, we have the remaining constant term as $-81$.
Now, to complete the square inside the parentheses, we need to take half of the coefficient of $x$, which is $10$, so half of $10$ is $5$, and then square it: $5^{2}=25$. So we add and subtract $25$ inside the parentheses to maintain equality. However, since we are adding $25$ inside the parentheses that’s multiplied by $-3$, we have to balance that by actually adding and subtracting $-3*25$ to the entire equation. Wait, maybe I need to write it out more carefully.
So:
$y=-3(x^{2}+10x+25-25)-81$
Wait, that is equivalent to:
$y=-3[(x^{2}+10x+25)-25]-81$
Which simplifies to:
$y=-3(x+5)^{2}+75-81$
Because $(x^{2}+10x+25)$ is $(x+5)^{2}$, and then we have $-3$ times $-25$ which is $+75$. Then, subtract $81$. So:
$y=-3(x+5)^{2}+75-81$
Then, combining the constants: $75-81=-6$. So the equation becomes:
$y=-3(x+5)^{2}-6$
Which is in vertex form: $y=a(x-h)^{2}+k$, where the vertex is $(h,k)$. Wait, in this case, it’s $(x+5)$ which is the same as $(x-(-5))$, so $h$ is $-5$ and $k$ is $-6$. Therefore, the vertex is at $(-5,-6)$, so $n$ is $-6$. That confirms the previous result.

Alternatively, maybe I can use calculus, taking the derivative and setting it to zero, but since this is a simple quadratic, that might be overkill. But for thoroughness, let’s try it. The derivative of $y$ with respect to $x$ is $dy/dx=2*(-3)x+(-30)=-6x-30$. Setting this equal to zero for critical points: $-6x-30=0$. Solving for $x$: $-6x=30\Rightarrow x=-5$. Then substitute $x=-5$ into original equation, as before, gives $y=-6$. So again, same result.

Therefore, all three methods (vertex formula, completing the square, calculus) lead to the same answer: $n=-6$.

Is there any chance I made a mistake in the signs? Let me check again. The original equation is $y=-3x^{2}-30x-81$. So $a=-3$, $b=-30$. Then the $x$-coordinate of vertex is $-b/(2a)=-(-30)/(2*(-3))=30/-6=-5$. That’s correct. Then substituting $x=-5$ into the equation: $y=-3*(-5)^{2}-30*(-5)-81$. Compute each term:
First term: $-3*(25)=-75$
Second term: $-30*(-5)=+150$
Third term: $-81$
Total: $-75+150=75$; $75-81=-6$. Correct.
Completing the square also confirmed the same. Calculus as well. So multiple methods confirm that $n=-6$.
Therefore, I’m confident that the answer is $n=-6$.

接下来，我们演示步骤提取的输出。如附录 A.2 所述，步骤提取的输出包含组件内每个计划与执行对应的行号。在下面的示例中，为便于理解，我们用推理轨迹中对应的文本块替换了行号。为简洁起见，我们只展示少数组件的完整细节。

Formatted output of Step Extraction

### Component 1

Description: Planning how to find the vertex of the parabola.

Plan: Okay, so I need to find the vertex … Then once we have the $x$-coordinate, we can plug that back into the original equation to find the corresponding $y$-coordinate, which would be $n$ in this case.

Prompt: Identify the values of $a$, $b$, and $c$ from the given quadratic equation.

Execution: So let’s identify $a$, $b$, and $c$ … it looks like $a=-3$, $b=-30$, and $c=-81$.
Comment: No lines found

### Component 2

Description: Verifying the identified values of $a$, $b$, and $c$.

…

### Component 3

Description: Calculating the $x$-coordinate of the vertex using the vertex formula.

…

### Component 4

Description: Calculating the $y$-coordinate of the vertex by substituting the $x$-coordinate.
…

### Component 5

Description: Verifying the calculation of the $y$-coordinate.
…

### Component 6

Description: Using the method of completing the square to find the vertex.

Plan: Alternatively, maybe I can use another method to confirm. Sometimes, completing the square can be a good way to find the vertex. Let me try that.

Prompt: Use the method of completing the square on the given equation to find the vertex.

Execution: The given equation is $y=-3x^{2}-30x-81$. To complete the square, first factor out the coefficient of $x^{2}$ … So the equation becomes: $y=-3(x+5)^{2}-6$ which is in vertex form: $y=a(x-h)^{2}+k$, where the vertex is $(h,k)$ … Therefore, the vertex is at $(-5,-6)$, so $n$ is $-6$.

Comment: That confirms the previous result.
…

### Component 7

Description: Using calculus to find the vertex by taking the derivative and setting it to zero.
…

### Component 8

Description: Comparing results from different methods.
…

### Component 9

Description: Final verification of the solution and confirming results.
…

在图 7 中，我们展示了在上述提取的步骤（即组件）上运行 DAG 构建所推断出的依赖关系。模型识别出组件 2、3、6、7 可以并行运行。这是因为一旦组件 1 识别出 $a$、$b$、$c$ 的值，对该计算的验证（组件 2）与 $x$ 坐标的计算（组件 3）相互独立。此外，配方法（组件 6）与微积分（组件 7）等备选方法不依赖组件 1 以外的组件。组件 4 依赖组件 3，因为 $y$ 坐标的计算依赖组件 3 中确定的 $x$ 坐标值。比较三种方法的结果（组件 8）依赖组件 4、6、7 的结果，而最终验证（组件 9）依赖组件 8。因此，DAG 有效建模了组件间的依赖并识别出并行化机会。

![Refer to caption](2506.05745v2/figures/dag_99.png)

图 7：对附录 B.1 示例推理轨迹中提取的步骤运行 DAG 构建所推断的依赖关系

如附录 A.2 所述，对执行较短的组件，我们把执行与其计划合并。因此对上述问题，组件 2、3、8 的执行与其计划合并。经过此修改后，为上述问题生成的包含计划与执行的轨迹如下所示。注意，计划依据 DAG 中建模的依赖排序。

R1 原始回复的串行 token 数以回复中的 token 总数计，为 1,645。下面的轨迹样本由于并行化执行，串行 token 数较少，为 1,445。

Trajectory sample for fine-tuning

<Plan_1>

Okay, so I need to find the vertex … it looks like $a=-3$, $b=-30$, and $c=-81$.
…
Wait, is that right? Let me check again … The constant term is $-81$, so $c=-81$.
…
Now, using the formula and plugging in the values of $a$ and $b$… Let’s compute that step by step.
…
<prompt_1.1> Calculate the x-coordinate of the vertex </prompt_1.1>
Alternatively, maybe I can use another method to confirm. Sometimes, completing the square can be a good way to find the vertex.
<prompt_1.2> Use the method of completing the square on the given equation to find the vertex. </prompt_1.2>

Alternatively, maybe I can use calculus, taking the derivative … let’s try it.
<prompt_1.3> Use calculus to find the $x$-coordinate </prompt_1.3>

</Plan_1>

<Execution_1>

<execution_1.1>

The numerator is $-(-30)$… So $m=30/(-6)=-5$. Therefore, the $x$-coordinate of the vertex is $-5$.
</execution_1.1>

<execution_1.2>

The given equation is $y=-3x^{2}-30x-81$. To complete the square, first factor out the coefficient of $x^{2}$ … So the equation becomes: $y=-3(x+5)^{2}-6$ which is in vertex form: $y=a(x-h)^{2}+k$, where the vertex is $(h,k)$ … Therefore, the vertex is at $(-5,-6)$, so $n$ is $-6$.
</execution_1.2>

<execution_1.3>

The derivative of $y$ with respect to $x$ is $dy/dx=2*(-3)x+(-30)=-6x-30$. Setting this equal to zero for critical points … as before, gives $y=-6$.
</execution_1.3>

</Execution_1>

<Plan_2>

Now, to find the y-coordinate $n$ … , I need to substitute $x=-5$…
<prompt_2.1> Substitute x = -5 to find the y-coordinate of the vertex. </prompt_2.1>

</Plan_2>

<Execution_2>

<execution_2.1>

Plugging in x = -5:
…
So $n=-6$.
</execution_2.1>

</Execution_2>

<Plan_3>

Based on execution_2.1:
Wait, let me double-check my calculations …
<prompt_3.1> Redo the substitution of $x=-5$ into the original equation to verify. </prompt_3.1>

Based on execution_2.1, execution_1.2, execution_1.3:
Therefore, all three methods (vertex formula, completing the square, calculus) lead to the same answer: $n=-6$.
Let me check again.
<prompt_3.2> Recheck the calculations and confirm the results </prompt_3.2>

</Plan_3>

<Execution_3>

<execution_3.1>

Calculating $y$ when $x=-5$: First term: $-3*(-5)^{2}$ … So adding them: $n=-75+150=75;75-81=-6$.
</execution_3.1>

<execution_3.2>

The original equation is … So multiple methods confirm that $n=-6$.
</execution_3.2>

</Execution_3>

<Final_answer>

Therefore, the value of $n$ is \boxed{-6}.
</Final_answer>

### B.2 Sprint 执行与 RFT 串行推理的对比演示

下面给出推理时 Sprint 应答 MATH-500 基准中一道问题的示例。并排展示的执行使用图 3 所示的推理策略并行完成。

问题：The binary number $10101001110_{2}$ is equal to what number in base eight?

Planning and parallel execution trajectory generated by Sprint

<Plan_1>

Okay, so I need to convert the binary number $10101001110_{2}$ to base eight. So, the plan is probably to group the binary digits into sets of three starting from the right and then convert each group to an octal digit.
Wait, but first, let me confirm: the binary number given is 10101001110. Let me count the digits.
Let’s see: 10101001110. That’s 11 binary digits. Since 8 is $2^{3}$, each octal digit is three bits, so 11 bits would need to be grouped into 4 octal digits (since 4*3=12, which is more than 11) but we need to add a leading zero to make it 12 bits? Wait, no, actually, when converting from binary to octal, you start from the right and split into groups of three.
Right, so even if the total number of bits isn’t a multiple of three, you can add leading zeros to make it a multiple of three. Let me check.
<prompt_1.1> Verify the method of converting binary to octal by considering the binary number 10101001110. </prompt_1.1>

But let me think again. Let me confirm with another approach.
Alternatively, I could convert the binary number to decimal first and then to octal. Maybe that’s a good way to cross-verify.
<prompt_1.2> Consider converting the binary number to decimal first and then to octal as an alternative method. </prompt_1.2>

</Plan_1>

<Execution_1>

<execution_1.1>

The original number is 10101001110. Let’s write them out: positions from right to left (since we start grouping from the right). Wait, actually, when grouping, we start from the right, so the leftmost digit might need to be padded with zeros to make the total number of digits a multiple of three.
So the binary number has 11 digits. 11 divided by 3 is 3 with a remainder of 2. So, we need to add one leading zero to make it 12 digits. Wait, 3*4=12, so yes, adding one zero on the left. So the original binary is 10101001110. Adding a leading zero gives 010101001110.
</execution_1.1>

<execution_1.2>

Let’s see. The binary number is 10101001110. Let me write down the positions from right to left, starting at 0. Wait, actually, in computers, the rightmost bit is the least significant bit, which is position 0. So let’s list the bits:
Position: 10 9 8 7 6 5 4 3 2 1 0
Bit: 1 0 1 0 1 0 0 1 1 1 0
…
So:
Bit 10: 1 ($2^{10}$)
Bit 9: 0 ($2^{9}$)
Bit 8: 1 ($2^{8}$)
…
So the binary number is:
$2^{10}+2^{8}+...2^{1}$
…
…
Adding them all up: 1024 + 256 = 1280; 1280 + 64 = 1344; 1344 + 8 = 1352; 1352 + 4 = 1356; 1356 + 2 = 1358.
So the decimal equivalent is 1358.
</execution_1.2>

</Execution_1>

<Plan_2>

Based on execution_1.1:
Now, splitting into groups of three starting from the right:
<prompt_2.1> Split the 12-digit binary number into groups of three starting from the right and convert each group to octal. </prompt_2.1>

Based on execution_1.2:
Now, converting 1358 to octal. Let’s divide by 8:
<prompt_2.2> Convert the decimal number 1358 to octal using division by 8. </prompt_2.2>

</Plan_2>

<Execution_2>

<execution_2.1>

0 1 0 1 0 0 0 1 1 1 0
Wait, no, wait. Wait, the binary number after adding a leading zero is 010101001110. Now, group into 4 sets of three:
Group 1 (leftmost): 010, Group 2: 101, Group 3: 001, Group 4: 110.
Then convert each of these to octal digits.
Wait, octal digits go from 0 to 7, so each group of three bits represents 0-7. Let me recall the binary to octal mapping:
000 = 0, 001 = 1, 010 = 2, … So:
Group 1: 010 $\rightarrow$ 2
Group 2: 101 $\rightarrow$ 5
Group 3: 001 $\rightarrow$ 1
Group 4: 110 $\rightarrow$ 6
So putting them together: 2 5 1 6 $\rightarrow$ $2516_{8}$.
</execution_2.1>

<execution_2.2>

1358 ÷ 8 = 169 with remainder 6 (since 169*8 = 1352, 1358 - 1352 = 6)
169 ÷ 8 = 21 with remainder 1 (21*8 = 168, 169 - 168 = 1)
21 ÷ 8 = 2 with remainder 5 (2*8 = 16, 21 - 16 = 5)
2 ÷ 8 = 0 with remainder 2
So the remainders, from last to first, are 2, 5, 1, 6. Therefore, 1358 in octal is $2516_{8}$.
</execution_2.2>

</Execution_2>

<Plan_3>

Based on execution_2.1:
Wait, but let me check again. Let’s verify the grouping.
<prompt_3.1> Verify the grouping of the binary digits and the conversion to octal. </prompt_3.1>

Based on execution_2.2:
Therefore, the binary number $10101001110_{2}$ is equal to $2516_{8}$.
So both methods give the same result, which is reassuring.
<prompt_3.2> Reflect on the solution and confirm its correctness by comparing both conversion methods. </prompt_3.2>

</Plan_3>

<Execution_3>

<execution_3.1>

Original binary with leading zero: 010 101 001 110.
Group 1: 010 → 2
Group 2: 101 → 5
Group 3: 001 → 1
Group 4: 110 → 6
So octal number is 2 5 1 6 → 2516.
</execution_3.1>

<execution_3.2>

I think this confirms that the answer is correct.
But let me just go through the steps once more to be thorough.
Original binary: 10101001110
Convert to groups of three starting from the right. Since it’s 11 digits, add a leading zero to make it 12 digits: 010101001110.
Group into four parts: 010 101 001 110. Convert each:
010 = 2, 101 = 5, 001 = 1, 110 = 6
Combine: 2516. Yep.
Alternatively, converting to decimal via binary to decimal conversion:
$10101001110_{2}=1*2^{1}0+0*2^{9}+1*2^{8}+0*2^{7}+...+0*2^{0}=1024+256+64+8+4+2=1358$. Then 1358 divided by 8 gives 169*8=1352, remainder 6; 169 divided by 8 is 21*8=168,
…
So 2 5 1 6. So 2516. All checks out.
Therefore, the final answer is 2516 in octal. I think that’s solid. No mistakes detected in the process.
</execution_3.2>

</Execution_3>

<Final_answer>

This step-by-step conversion shows that the binary number $10101001110_{2}$ is equal to \boxed{$2516_{8}$} in base eight.
</Final_answer>

上述 Sprint 回复的串行 token 数为 1,463。对同一问题，我们在下面给出 RFT 模型生成的串行轨迹。由于所有 token 都串行生成，该回复的串行 token 数为 1,989。这凸显了用 Sprint 并行化执行的收益。

Sequential reasoning trajectory generated by the RFT model

Okay, so I need to convert the binary number $10101001110_{2}$ to base eight. Hmm, I remember that converting between binary and octal is done by grouping the binary digits into sets of three, starting from the right. Each group of three bits corresponds to a single octal digit. Let me think through the steps carefully.

First, let me write down the binary number: $1\ 0\ 1\ 0\ 1\ 0\ 0\ 1\ 1\ 1\ 0$. Wait, let me count the digits. The original number is 10101001110, which has $11$ digits. Since octal groups are in threes, I need to split this into groups of three. But $11$ isn’t divisible by three. So, I should add leading zeros to make the total number of digits a multiple of three. Right, so $11$ divided by $3$ is $3$ with a remainder of $2$. That means I need to add one leading zero to make it $12$ digits. So the new number becomes $010101001110_{2}$.

Now, let me split this into groups of three starting from the right. Let me write it out:

Group $1$: $010$, Group $2$: $101$, Group $3$: $001$, Group $4$: $110$

Wait, no. Wait, the leading zeros are added at the beginning, so the original number was 10101001110. Adding a leading zero makes it 010101001110. Now, splitting into groups of three from the right:

Starting from the end, the last three digits are $110$, then moving left, the next three are $001$, then $101$, then $010$. So the groups are $010$, $101$, $001$, $110$. Now, each of these binary groups needs to be converted to their octal equivalents.

Let me convert each group:

$010_{2}$ is $2$ in octal because $0\times 4+1\times 2+0\times 1=2$.

$101_{2}$ is $5$ in octal because $1\times 4+0\times 2+1\times 1=5$.

…

So putting those together in order from left to right, the octal digits are $2$, $5$, $1$, $6$. Therefore, the octal number should be $2516_{8}$. Wait, but let me verify this again to make sure I didn’t make a mistake in grouping or conversion.

Wait, when grouping from the right, the first group (rightmost) is $110$, then moving left, the next is $001$, then $101$, then $010$. So the groups are $010$, $101$, $001$, $110$. Converting each to octal:

$010_{2}=2$, $101_{2}=5$, $001_{2}=1$, $110_{2}=6$. So the octal number is $2\ 5\ 1\ 6$, which is $2516_{8}$. Let me check if this is correct by converting the original binary number to decimal and then converting that decimal number to octal to see if it matches.

First, converting $10101001110_{2}$ to decimal. Let’s write out the binary number with each digit’s place value:

From right to left, the positions are $0$ to $10$. The digits are:

Position $10$: $1$, Position $9$: $0$, Position $8$: $1$, …, Position $0$: $0$

Calculating the decimal value:

$1\times(2^{10})+0\times(2^{9})+1\times(2^{8})+0\times(2^{7})+1\times(2^{6})+0\times(2^{5})+0\times(2^{4})+1\times(2^{3})+1\times(2^{2})+1\times(2^{1})+0\times(2^{0})$
Calculating each term:

$2^{10}=1024$, $2^{8}=256$, $2^{6}=64$, $2^{3}=8$, $2^{2}=4$, $2^{1}=2$

Adding them up: $1024+256=1280$; $1280+64=1344$; $1344+8=1352$; $1352+4=1356$; $1356+2=1358$.

So the decimal value is $1358$. Now, converting $1358$ to octal. Let’s divide $1358$ by $8$ repeatedly.

$1358\div 8=169$ with a remainder of $6$.

$169\div 8=21$ with a remainder of $1$.

$21\div 8=2$ with a remainder of $5$.

$2\div 8=0$ with a remainder of $2$.

Writing the remainders from last to first: $2\ 5\ 1\ 6$. So $2516_{8}$. Which matches the previous result. Therefore, the conversion is correct.

But wait, let me check the grouping again. The original binary number was 10101001110. When adding a leading zero, it becomes 010101001110. Splitting into groups of three from the right:

Starting from the right:

$111$ $001$ $101$ $010$. Wait, that’s different. Wait, perhaps I made a mistake in grouping.

Wait, the original binary number is 10101001110. Let me write it as $10\ 101\ 001\ 110$. Wait, that’s not correct. Wait, the original number is $11$ digits. So when adding a leading zero, it becomes $12$ digits: $0\ 1\ 0\ 1\ 0\ 1\ 0\ 0\ 1\ 1\ 1\ 0$. Then grouping from the right:

Group$1$: $0\ 1\ 0$ (positions $11,10,9$), Group$2$: $1\ 0\ 1$ (positions $8,7,6$), Group$3$: $0\ 0\ 1$ (positions $5,4,3$), Group$4$: $1\ 1\ 0$ (positions $2,1,0$)

Wait, but when grouping from the right, the rightmost group is the last three digits. So the original number is 010101001110. The rightmost three digits are $110$, then moving left, next three are $001$, then $101$, then $010$. So the groups are $010$, $101$, $001$, $110$. Which is the same as before. So converting each gives $2,5,1,6$. So $2516_{8}$. Which is correct. So the answer is $2516_{8}$.

But wait, when I grouped the original number as 10101001110, which is $11$ digits, adding a leading zero makes it 010101001110, which is $12$ digits. So grouping into three from the right: $010$, $101$, $001$, $110$. So that’s correct.

Alternatively, another way to check is by converting each group as I did before. So yes, the answer is 2516 in octal.

But let me just confirm once again by converting $2516_{8}$ back to binary to see if it’s $10101001110_{2}$.

2516 in octal:

Each digit corresponds to three binary digits:

$2\rightarrow 010$
$5\rightarrow 101$
$1\rightarrow 001$
$6\rightarrow 110$
So putting them together: $010\ 101\ 001\ 110\rightarrow 010101001110$, which is the original number. So that’s correct.

Therefore, the final answer is \boxed{2516} in base eight.

### B.3 单一解法内部并行性的 Sprint 演示

第 B.2 节的示例展示了 Sprint 在第 1、2 阶段并行化备选解法。在下面的示例中，我们展示 Sprint 也可以把单一解法拆分为子任务、并行执行它们、之后再汇总结果。这里，规划器把问题拆分为计算垂直渐近线与重新评估水平渐近线，即提示 1.1 与 1.2 并行。

问题：The graph of $\frac{2x}{x^{2}-5x-14}$ has vertical asymptotes $x=a$ and $x=b$, and horizontal asymptote $y=c$. Find $a+b+c$.

Trajectory sample for parallelism within a single solution method

<Plan_1>

Determine the vertical and horizontal asymptotes of f(x)=\frac{2x}{x^2-5x-14}, then compute a+b+c.
<prompt_1.1> Identify the vertical asymptotes by finding the roots of the denominator. </prompt_1.1>
<prompt_1.2> Re-evaluate the horizontal asymptote using the degrees of the numerator and denominator. </prompt_1.2>
</Plan_1>

<Execution_1>

<execution_1.1>

Vertical asymptotes occur where the denominator is zero (provided the numerator isn’t zero). Factoring x^2-5x-14 = (x-7)(x+2) gives roots at x=7 and x=-2. Thus, a=7 and b=-2.
</execution_1.1>

<execution_1.2>

Since the numerator’s degree (1) is less than the denominator’s (2), the horizontal asymptote is y=0. Hence, c=0.
</execution_1.2>

</Execution_1>

解答的其余部分继续……

### B.4 Sprint 在非 STEM 任务上的执行演示

我们用下面的示例展示 Sprint 尽管与用于微调的 MATH 数据集中的任务不同，仍能很好地泛化到创意写作等非 STEM 任务。当被要求生成一段简短的电影场景描述时，规划器成功地设计了三个独立子任务，每个由单独的执行器并发执行。经过三轮规划与执行后，这些独立产出的结果被整合成一段连贯统一的叙事。

Trajectory sample for creative writing task

<Plan_1>

The user wants a 250-word scene set shortly after the Battle of King’s Landing.
<prompt_1.1> Identify the key elements and emotions for each perspective: Bran Stark’s visions, the noble’s skepticism, and the urchin’s admiration. </prompt_1.1>
</Plan_1>

<Execution_1>

<execution_1.1>

- Bran: He’s the one who saw the vision of the White City…
- Noble from the Vale: He’s skeptical…
- Urchin: This adds an unexpected element…
</execution_1.1>

</Execution_1>

<Plan_2>

Based on Execution 1.1:
Bran: His lines should include visions…
<prompt_2.1> Develop Bran Stark’s lines to describe the vision of the White City and the Iron Throne. </prompt_2.1>

<prompt_2.2> Develop the noble’s lines to express skepticism about Bran’s leadership and his brother’s choice. </prompt_2.2>

<prompt_2.3> Develop the urchin’s lines to show admiration for Bran and the vision, and the impact on his journey. </prompt_2.3>

</Plan_2>

<Execution_2>

<execution_2.1>

The urchin’s lines should be simple but full of wonder…
</execution_2.1>

<execution_2.2>

The urchin in the Red Keep adds a layer of innocence, contrasting with…
</execution_2.2>

<execution_2.3>

The streets below are in ruins, but the urchin’s eyes…
</execution_2.3>

</Execution_2>

<Plan_3>

Based on Executions 2.1–2.3:
<prompt_3.1> Ensure each character’s perspective is distinct and contributes to the overall mood. The scene should capture the transition from battle chaos to the realm of possibility of a new order. </prompt_3.1>

</Plan_3>

<Execution_3>

<execution_3.1>

The urchin’s admiration is genuine…
</execution_3.1>

</Execution_3>

<Final_answer>

The air was thick with the scent of incense and the faint hum of machinery. The throne loomed before Bran…
The council chambers were quiet, save for the faint murmur of leather on wood…
The Red Keep was alive with the promise of change … The White City was his home, and the Iron Throne was his throne.
</Final_answer>
