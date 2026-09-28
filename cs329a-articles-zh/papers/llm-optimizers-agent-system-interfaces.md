---
title: "通过智能体-系统接口用 LLM 优化器改进并行程序性能"
title_en: "Improving Parallel Program Performance with LLM Optimizers via Agent-System Interfaces"
arxiv: 2410.15625
source: https://arxiv.org/abs/2410.15625
crawled: 2026-09-23
translated: 2026-09-23
---

# 通过智能体-系统接口用 LLM 优化器改进并行程序性能

> 原文：[Improving Parallel Program Performance with LLM Optimizers via Agent-System Interfaces](https://arxiv.org/abs/2410.15625) · Stanford CS329A 指定阅读

Anjiang Wei（斯坦福大学，联系方式：anjiang@cs.stanford.edu）、Allen Nie（斯坦福大学）、Thiago S. F. X. Teixeira（Intel）、Rohan Yadav（斯坦福大学）、Wonchan Lee（NVIDIA）、Ke Wang（南京大学）、Alex Aiken（斯坦福大学）

###### 摘要

现代科学发现日益依赖高性能计算来完成复杂的建模与模拟。改进并行程序性能的一个关键挑战，是把任务高效地映射到处理器、把数据映射到内存，这一过程由被称为 *mapper*（映射器）的复杂低层系统代码决定。开发高性能 mapper 需要数天的人工调优，这对缺乏系统专业知识的领域科学家构成了重大障碍。我们提出一个用生成式优化（generative optimization）自动化 mapper 开发的框架，它利用标量性能指标之外的更丰富反馈。我们的方法以智能体-系统接口（Agent-System Interface）为核心，它包含一个领域特定语言（DSL）用于抽象掉系统代码的低层复杂性并定义结构化的搜索空间，以及 AutoGuide——一种把原始执行输出解读为可执行反馈的机制。与 OpenTuner 等仅依赖标量反馈的传统强化学习方法不同，我们的方法以远少得多的迭代次数找到更优的 mapper。仅用 10 次迭代，它就胜过运行 1000 次迭代后的 OpenTuner，取得 3.8 倍的性能优势。我们的方法找到的 mapper 在九个基准上最高以 1.34 倍加速超越专家手写的 mapper，同时把调优时间从数天缩短到几分钟。

###### 关键词：

机器学习，ICML

注：同等贡献。

## 1 引言

现代科学发现依赖于用于建模与模拟的先进软件工具（Stocks et al., 2024；Wang et al., 2024；Ltaief et al., 2024）。包括物理学家、化学家与生物学家在内的计算科学家依赖高性能计算来解决复杂问题。这些科学计算占据了世界上最强大超级计算机的主要工作负载（DOE, 2025）。然而，许多领域科学家缺乏计算机科学专业知识，因此由于底层机器的复杂性与规模而难以优化其程序。即便对专家而言，发现并修复因程序修改或移植到新机器而产生的性能问题也往往耗时费力。在自动化性能调优上的任何进展都对这一领域大有裨益。

基于任务的编程（task-based programming）（Slaughter et al., 2015；Bauer et al., 2012；Augonnet et al., 2009；Chamberlain et al., 2007；Moritz et al., 2018；Barham et al., 2022）已成为高性能计算的一条有前景的途径。该范式把计算分解为仅通过参数通信的独立任务。基于任务的系统的一个关键优势是，性能调优问题被分解为一个独立的映射（mapping）：把任务指派给处理器、把数据指派给特定内存。通过精心设计的 *mapper*（以代码实现）达成的高质量映射可以显著提升性能，往往可达一个数量级（Galvez et al., 2017）。

然而，目前编写 mapper 仍是一个劳动密集的过程，因为它需要对应用、硬件和低层系统 API 的深入知识。此外，这一过程高度依赖具体应用、具体输入与具体机器，专家往往需要数天的细致调优才能达到高性能。这一挑战对通常缺乏计算机系统与代码优化必要专业知识的领域科学家尤为突出。自动化 mapper 开发将使科学家能够专注于自己的领域专长，同时充分利用高性能计算系统的能力。

![Refer to caption](2410.15625v4/rl.png)

图 1：基于智能体的生成式优化的迭代 mapper 改进。该系统利用智能体-系统接口，由领域特定语言（DSL）与 AutoGuide 组成。DSL 抽象掉低层系统代码，为映射策略定义搜索空间，而 AutoGuide 把执行结果解读为可执行的指导。随着迭代推进，mapper 不断演化以提升性能。

本文提出一个由大语言模型（LLM）驱动的系统，自动化 mapper 代码的生成与优化。第一个挑战来自*生成 mapper 代码的复杂性*，源于原本的低层编程系统让智能体暴露于错综复杂的系统 API，同时来自系统的原始反馈信息对智能体往往缺乏信息量的问题。第二个挑战涉及*优化 mapper 性能*。具体而言，它包括 (1) 定义合适的搜索空间，以及 (2) 设计高效方法来寻找最优 mapper，从而最大化并行程序性能。

为应对第一个挑战，我们提出智能体-系统接口（Agent-System Interface，ASI），如图 1 所示，它是智能体与系统之间的抽象层，可简化代码生成并向智能体提供更有意义的反馈。ASI 的核心是一个*领域特定语言（DSL）*，一个封装了生成 mapper 所需全部性能关键决策的高级接口。DSL 用编译器抽象掉低层系统代码的复杂性。此外，DSL 定义了一个结构化的搜索空间，使映射策略得以被系统性地探索。我们还设计并实现了 *AutoGuide* 机制，把原始执行输出解读为信息丰富、可执行的指导。该机制使智能体能够利用增强的反馈更新其策略，迭代地优化 mapper。

对于第二个挑战，我们采用生成式优化（generative optimization）这一优化技术的最新进展。与仅依赖标量奖励的传统方法（如强化学习（Ansel et al., 2014））不同，生成式优化可以利用更丰富的反馈形式，例如以自然语言表达的错误解释与可执行建议。这种智能体式优化工作流此前已在多个领域被证明有效（Nie et al., 2024；Cheng et al., 2024；Yang et al., 2023；Khattab et al., 2023；Yuksekgonul et al., 2024）。我们的工作首次将该技术应用于系统优化领域。

我们的实验表明，由 LLM 驱动的智能体优化出的 mapper 不仅能匹敌、而且往往超越专家手写的 mapper，在九个基准上取得最高 1.34 倍的加速。由于专家手写的 mapper 代表了最高标准，超越它们是一项值得注意的成就。同时，我们的方法把 mapper 调优时间从数天显著缩短到几分钟，使领域科学家更容易获得高性能映射。为进一步凸显生成式优化的优势，我们将其与基于强化学习的自动调优框架 OpenTuner 比较。当两者都运行 10 次迭代时，我们的生成式优化器找到的 mapper 比 OpenTuner 快 11 倍；即便 OpenTuner 运行 1000 次迭代，我们仍保持 3.8 倍的优势。此外，消融研究强调了智能体-系统接口设计对取得这些性能提升的必要性。我们的贡献如下：

1. 智能体-系统接口的设计：
   我们引入一个简化 mapper 代码生成并向智能体提供指导的抽象层。领域特定语言（DSL）定义搜索空间，使智能体无需处理低层系统代码即可探索映射策略。AutoGuide 把原始执行输出解读为有针对性的反馈，使智能体能够更有效地改进 mapper 代码。

2. 面向系统的生成式优化：
   我们引入生成式优化以改进系统性能，利用更丰富的反馈，例如错误消息与自然语言表达的可行建议。与仅依赖标量反馈的 OpenTuner 等强化学习方法不同，我们的方法以少得多的迭代识别出更好的 mapper。仅 10 次迭代，它就在 OpenTuner 运行 1000 次迭代后仍胜出 3.8 倍。

3. 性能的实证评估：我们基于智能体的方案在九个基准上取得最高 1.34 倍的加速，超越专家手写的 mapper，同时把调优时间从数天缩短到几分钟。我们通过消融研究强调智能体-系统接口的关键作用，展示其对实现性能提升的影响。

## 2 相关工作

并行编程中的映射 许多并行编程系统允许用户自行做映射决策，例如 Legion（Bauer et al., 2012）、StarPU（Augonnet et al., 2009；Augonnet et al., 2010）、Chapel（Chamberlain et al., 2007）、HPX（Kaiser et al., 2014；Heller et al., 2017）、Sequoia（Fatahalian et al., 2006）、Ray（Moritz et al., 2018）、TaskFlow（Huang et al., 2021）与 Pathways（Barham et al., 2022）。已有多种自动化映射的技术被提出，包括机器学习模型（O'Boyle et al., 2013；Wang & O'Boyle, 2009）、静态分析（Poesia et al., 2017；Ren et al., 2008）、强化学习（Ansel et al., 2014；Mirhoseini et al., 2017）与自动调优（SFX Teixeira et al., 2023）。我们使用基于 LLM 的智能体方法，并探索比传统方法更大的 mapper 搜索空间。

智能体框架 由大语言模型（LLM）驱动的智能体在决策、规划、工具集成以及解决动态环境中的复杂问题方面发挥着关键作用（Guo et al., 2024）。已有许多智能体框架被开发（Yao et al., 2022；Wu et al., 2023；Li et al., 2023；Hong et al., 2023），用途遍及软件工程（Gur et al., 2023；Yang et al., 2024b；Jin et al., 2024）、机器人学（Kannan et al., 2024）、医疗健康（Li et al., 2024）、教育（Ramirez & Esparrell, 2024）与知识工程（Shao et al., 2024）等领域。我们的工作首次将智能体工作流应用于迭代优化 mapper 代码，提升并行程序的性能。

面向系统的 AI 用 AI 优化系统设计近年来获得显著关注。深度学习（Zheng et al., 2020a；Zheng et al., 2020b；Zheng et al., 2022b）与梯度提升树（Feng et al., 2023）等技术已被用于预测程序执行时间以优化性能。强化学习方法已应对芯片布局（Mirhoseini et al., 2021）、自动调优（Ansel et al., 2014）、自动向量化（Haj-Ali et al., 2020a）与编译器阶段排序（Haj-Ali et al., 2020b）等挑战。虽然以往工作主要依赖传统方法做代价预测与优化，我们的工作利用生成式优化的最新进展来应对复杂的系统挑战。

#### 生成式优化

近期工作探索用 LLM 解决传统上用数值方法处理的优化问题，包括混合整数规划（AhmadiTeshnizi et al., 2024a；AhmadiTeshnizi et al., 2024b）与数值优化（Nie et al., 2024）。生成式优化的一个关键优势是能够利用多样形式的反馈迭代改进解。例如，Cheng et al.（2024）把生成式优化应用于机器人操作与游戏，而 Yuksekgonul et al.（2024）优化提示与分子设计。虽然强化学习已被应用于系统优化，LLM 驱动优化在系统领域的潜力仍未被探索。我们的工作探索带有更丰富反馈的生成式优化是否优于系统优化中使用标量奖励的传统方法。

## 3 问题定义

```text
# Map task0 to GPU.
Task task0 GPU;

# Place certain data onto GPU ZeroCopy.
Region * ghost_region GPU ZCMEM

# Specify layout in memory
# (aligned to 64 bytes)
Layout * * * C_order SOA Align==64

# Define a cyclic mapping strategy
def cyclic(Task task):
    ip = task.ipoint;
    mgpu = Machine(GPU);
    node_idx = ip[0] % mgpu.size[0];
    gpu_idx = ip[0] % mgpu.size[1];
    return mgpu[node_idx, gpu_idx];

IndexTaskMap task4 cyclic
```

（a）领域特定语言（DSL）编写的一个 mapper 示例

```cpp
void slice_task(const Task& task,
                const SliceTaskInput &input,
                SliceTaskOutput &output) {
  vector<Processor> targets =
    this->select_targets_for_task(ctx, task);
  DomainT<2> space = input.domain;
  Point<2> num_points =
        space.bounds.hi - space.bounds.lo + ones;
  Rect<2> blocks(zeroes, num_blocks - ones);
  ... // 126 lines of C++ code omitted here
  for (PointInRectIterator<2> it(blocks); it() != NULL; it++)
  {
    DomainT<2,coord_t> slice_space;
    TaskSlice slice;
    slice.domain = {slice_lo, slice_hi};
    slice.proc = targets[index++ % targets.size()];
    output.slices.push_back(slice);
  }
}
```

（b）C++ mapper 的代码片段

图 2：DSL mapper 与 C++ mapper 的比较。DSL 的声明式高级设计抽象掉了低层 C++ 代码的复杂性，是智能体-系统接口的核心。高亮的方框展示了同样的功能——需要大量 C++ 系统代码——在 DSL 中只需几行即可简洁表达。

#### 动机与挑战

我们解决的具体问题是为 Legion 并行编程框架（Bauer et al., 2012）自动生成高性能 mapper。mapper 决定任务调度与数据放置。一个设计良好的 mapper 相对朴素策略可以取得数量级的加速。

然而，自动化 mapper 生成因两个关键因素而充满挑战。其一，低层系统代码的复杂性。实现一个 mapper 需要编写数百行错综复杂的 C++ 代码，需要对系统内部机制的专业知识。其二，映射策略的庞大搜索空间。搜索空间随任务数与参数数呈指数增长。

#### 搜索空间与性能影响

如图 A1 所示，mapper 的搜索空间涉及多个决策，每个决策都影响性能。第一个关键方面是处理器选择，它决定任务在 GPU、CPU 还是 OpenMP 运行时上运行。这一选择取决于任务大小、GPU 显存容量与内核启动开销等因素。例如，小任务可能因 GPU 内核启动开销而偏好 CPU，而显存占用大的任务在 GPU 显存不足时可能要在 CPU 上运行。

另一个关键维度是内存放置，它决定数据存放的位置。mapper 必须决定把数据放在 GPU 的 FrameBuffer 以获得快速访问、ZeroCopy 内存以实现 CPU-GPU 共享，还是 CPU 系统内存以获得更多可用存储。每个选项都在访问速度、内存用量与数据传输开销之间有权衡。

此外，内存布局进一步扩大了搜索空间，结构数组（SOA）与数组结构（AOS）的选择、数据排布（Fortran 序与 C 序）以及对齐约束（例如 128 字节对齐）等决策都会显著影响缓存效率与性能。

最后，高性能计算的一个重要惯用法是在分区数据上启动任务。索引映射（index mapping）决定数据分区与任务执行如何分布在多个处理器上。为便于统一表述，我们可以把数据分区表示为数据分区的张量、把机器表示为处理器的张量、把操作分区数据的任务表示为任务的张量。数据与任务索引映射到处理器索引的方式会影响处理器间通信，这是性能的关键因素（Unger et al., 2022；Zheng et al., 2022a）。

## 4 我们的方法：智能体-系统接口

### 4.1 领域特定语言设计

用编码智能体自动化 mapper 生成的一个关键挑战是低层系统代码的复杂性，它需要错综复杂的 C++ 实现。为此，我们设计了一种高级领域特定语言（DSL）作为智能体-系统接口（ASI）的核心。DSL 为映射策略提供*结构化的搜索空间*，同时*抽象掉低层实现细节*。与要求以命令式方式规约映射策略的 C++ 不同，我们的 DSL 采用声明式设计，允许用户指明要达成*什么*，而非*如何*实现它。最关键的是，DSL 分离了关注点，使映射决策的多个方面可以*彼此独立地表达，而不是纠缠*在低层系统 API 中。这一设计降低了代码复杂性，并自然地为智能体提供了可探索的搜索空间。为了实现它，我们开发了一个把 DSL 翻译为低层 C++ API 的*编译器*。

![Refer to caption](2410.15625v4/agent_workflow.png)

图 3：智能体优化过程。mapper 智能体以服务器规格与应用特定信息为输入，生成 mapper 代码，并与应用一起在服务器上执行。原始执行反馈用 AutoGuide 机制增强，并由 LLM 优化器迭代改进 mapper 以提升性能。

| 案例 | 原始执行输出 | AutoGuide |  |
| --- | --- | --- | --- |
|  |  | 解释 | 建议 |
| 案例 1 | 执行错误：Assertion failed: stride does not match expected value. | 内存布局不符合预期。 | 调整布局约束，或把任务移到其他处理器类型。 |
| 案例 2 | 性能指标：执行时间为 0.03s。 | N/A | 把更多任务移到 GPU 以缩短执行时间。 |

表 1：AutoGuide 反馈机制。AutoGuide 机制解读来自运行时系统的原始执行输出，提供信息更丰富的错误解释与 mapper 修改建议。它通过关键词匹配实现。更多示例见表 A3。

如图 2 所示，DSL 代码的复杂性显著低于 C++。图 2(a) 给出了一个 DSL mapper 示例，突出了我们 DSL 的关键特性。相比之下，图 2(b) 展示了 C++ mapper 的一个片段，强调低层实现细节的错综复杂。在各基准上，使用 DSL 平均减少 14 倍的代码行数。这一大幅缩减使 DSL 成为更适合 LLM 代码生成的目标，因为它抽象掉了低层系统固有的复杂性。正如我们将在第 5.2 节展示的，尽管 DSL 在 LLM 训练语料中没有示例，而 C++ 广泛存在，LLM 生成 DSL 代码的效果仍然更好。

接下来我们描述 DSL 的设计，强调其声明式本质与结构化搜索空间。第 3 节详述了每个决策的性能影响。

Task 语句（图 2(a) 第 2 行）定义每个任务的处理器选择，在 CPU、GPU 或 OpenMP 之间选择。第 2 行指定 task0 的实例应在 GPU 上运行。这一决策按任务做出；注意搜索空间随任务数量呈指数增长。

Region 语句（图 2(a) 第 5 行）控制数据参数的内存放置。第 5 行指定所有使用 ghost_region 的任务应把数据放在 GPU ZeroCopy 内存。其他选择包括 GPU FrameBuffer 内存与 CPU 系统内存。这一决策按任务、按参数做出，导致搜索空间指数增长。

Layout 语句（图 2(a) 第 9 行）定义内存布局。第 9 行为映射到所有处理器的所有任务所用的全部数据强制 C_order 轴序、SOA 布局与 64 字节内存对齐。备选包括 F_order、AOS 与多种对齐策略。这是按任务、按数据、按处理器的决策。

IndexTaskMap 语句（图 2(a) 第 19 行）用自定义函数控制索引映射。第 12 行定义了建立两个索引空间对应关系的映射函数：应用代码（例如 for 循环）中定义的任务索引空间（由 task.ipoint 表示）与分布式机器的处理器空间（由 Machine(GPU) 表示）。DSL 允许用户表达两个索引空间之间任意算术映射。这一决策适用于并行 for 循环启动的每个任务组。

我们的 DSL 旨在表达广泛的高性能映射策略，包括所有最重要的决策。虽然可能存在某些优化无法直接表达的情形，但我们尚未遇到。尽管比通用 C++ 更受限，DSL 已被证明有效：我们的智能体发现的、胜过专家手写 C++ 实现的所有 mapper 都可以在当前 DSL 内表达。

### 4.2 通过 AutoGuide 的生成式优化

我们把 mapper 生成形式化为一个在线优化问题。给定三元组 $(\Theta,\omega,\mathcal{T})$，其中 $\Theta$ 是可能的 mapper 集合，$\omega$ 是*优化目标*，$\mathcal{T}$ 是一个以 mapper $\theta\in\Theta$ 为输入的函数，$(f,g)=\mathcal{T}(\theta)$ 返回 $f$（执行该 mapper 的*反馈*，即用生成的 mapper 运行应用代码后测得的性能）与 $g$（追踪 mapper 如何生成的*过程图*）。在我们的设置中，mapper 性能是确定性的，因为我们仔细控制了环境中所有随机性来源。若参数空间是数值型的，这一在线优化问题可以用赌博机算法（Lattimore & Szepesvári, 2020）、强化学习（Sutton & Barto, 2018）或贝叶斯优化（Snoek et al., 2012）解决，但当参数搜索空间庞大且离散（即文本）时，这些方法效率较低。

在这个在线优化问题中，我们利用 DSL 构造参数空间以提升优化效率。这里 $\theta$ 表示程序代码，而 $\omega$ 与 $f$ 以文本表达。我们采用生成式优化，以 LLM 为优化器处理文本形式的目标。这种新兴的优化行为最近在多个领域被观察到并应用（Yang et al., 2024a；Cheng et al., 2024；Yuksekgonul et al., 2024；Patel et al., 2024）。

#### 优化过程

我们在图 3 中展示优化过程。智能体接收两个输入：服务器规格与应用元数据。服务器规格详述硬件配置，包括每节点的 CPU 与 GPU 数量以及总节点数。应用元数据提供任务名称及每个任务访问的相关数据参数信息。这些输入定义了智能体在优化期间探索的结构化搜索空间。智能体用给定输入生成 mapper 代码，并与应用代码一起在服务器上执行。来自运行时的原始执行反馈经 AutoGuide 机制增强后回喂给 LLM，迭代地改进智能体以生成更好的 mapper 代码。

图 4：性能比较。9 个基准的归一化吞吐量，比较专家 mapper、随机 mapper、Trace、OPRO 与 OpenTuner 在 5 次运行 10 次迭代内的平均优化轨迹，以及 Trace 找到的最佳 mapper。

图 5：Trace（生成式优化器）与 OpenTuner（传统强化学习）在 1K 次迭代内的比较（对全部 9 个基准取平均）。

#### 编码智能体

我们的 mapper 智能体通过迭代生成 DSL 代码来改进映射决策。mapper 智能体的高层模式如图 3 所示。mapper 智能体实现为 Trace（Cheng et al., 2024）框架中的一个 Python 程序，我们把生成单体 mapper 的任务分解为*独立的代码段*。这一分解使智能体可以分别决定每一段生成什么代码。这一做法之所以有效，是因为我们的 *DSL 设计消除了映射决策之间不必要的依赖*。我们的模块化策略与由少到多提示（least-to-most prompting）（Zhou et al., 2022）一致。

#### AutoGuide

AutoGuide 反馈机制基于三个关键动机设计：(1) 生成式优化受益于自然语言反馈，而非仅依赖标量值；(2) 来自运行时系统的原始执行输出往往信息量过低，无法有效引导智能体的决策；(3) 系统研究者已知的领域启发式可以自然地用语言表达（例如，多数任务在 GPU 上比 CPU 上更快）。为满足这些需求，AutoGuide 通过解释晦涩的错误消息与建议 mapper 修改来帮助智能体。如表 1 所示，它把信息量不足的执行输出解读为可执行的洞见，更多示例见第 A.5 节。其实现依赖对原始执行输出的关键词匹配。第 5.3 节的消融研究证明了它在实验中的有效性。

## 5 评估

实验在一个节点上进行，配备两颗 Intel 10 核 E5-2640 v4 CPU、256G 主存与四块 NVIDIA Tesla P100 GPU。我们使用 gpt-4o-2024-08-06。

### 5.1 应用性能的加速

#### 基准

我们的评估使用一套 9 个基准，包括 3 个科学计算工作负载与 6 个知名矩阵乘法算法。*Circuit* 是一个模拟基准，通过模拟互连节点与导线上的电流与电压来建模电路行为（Bauer et al., 2012）。*Stencil* 模拟一个 2D 网格，每个点的值依据其邻居决定的模板模式更新（Van der Wijngaart & Mattson, 2014）。*Pennant* 建模非结构网格拉格朗日交错网格流体动力学，常用于模拟可压缩流（Ferenbaugh, 2015）。其余六个基准——*Cannon's*、*SUMMA*、*PUMMA*、*Johnson's*、*Solomonik's* 与 *COSMA*——是知名的并行矩阵乘法算法（Cannon, 1969；Van De Geijn & Watts, 1997；Choi et al., 1994；Agarwal et al., 1995；Solomonik & Demmel, 2011；Kwasniewski et al., 2019）。由于并行矩阵乘法在高性能计算与科学模拟中的核心地位，它仍是一个活跃的研究课题（Yadav et al., 2022）。此外，改进矩阵乘法性能具有广泛影响，因为它能加速大量下游机器学习工作负载（Jangda et al., 2022；Zheng et al., 2025）。我们在第 A.3 节更详细地讨论这些矩阵乘法算法。这套基准兼具代表性矩阵乘法算法的深度与多种科学计算工作负载的多样性。

在本实验中，我们用以下基线评估 mapper 的性能。

专家手写的 mapper。这些 mapper 由花多年时间掌握计算科学的领域科学家手工开发。在并行编程框架中编写 mapper 本身就是一项挑战，针对特定应用调优可能需要数天。

随机生成的 mapper。这些 mapper 用 10 个不同的随机种子从每个应用的完整搜索空间中随机采样生成。我们报告平均性能。

智能体优化的 mapper。使用 Trace（Cheng et al., 2024），我们评估了 Trace 与 OPRO（Yang et al., 2023）两种搜索算法，每个应用运行 10 次迭代。为考虑随机输出，我们重复该过程 5 次并报告平均值。同时报告 Trace 多次运行中的最佳 mapper。

OpenTuner mapper。OpenTuner（Ansel et al., 2014）是一个程序自动调优框架，使用强化学习基于标量反馈优化性能。我们提供执行时间作为反馈，失败则施加高惩罚。

#### 结果

在图 4 中，我们使用归一化吞吐量作为性能指标，数值越高越好。吞吐量相对专家手写的 mapper 归一化，提供了清晰的比较基线。我们关注的是端到端性能的测量，它同时涵盖生成 mapper 的正确性与效率。若生成的代码有任何语法或运行时问题，其吞吐量记为 0。我们报告 Trace 找到的最佳 mapper，以及 Trace、OPRO 与 OpenTuner 在 5 次运行 10 次迭代内的平均优化轨迹。

Trace 找到的所有最佳 mapper 都能匹敌或超越专家手写的 mapper，凸显了基于智能体的生成式优化器的有效性。在我们的语境下，报告表现最好的 mapper 是恰当的。mapper 优化是一个离线过程，实践中多次运行优化器并部署最佳结果是标准做法。一经识别，mapper 就可以在相同应用、输入与硬件上跨重复执行复用，不产生进一步的搜索成本。

|  |  |  |  |  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 代码生成目标 | 映射策略 |  |  |  |  |  |  |  |  |  | 成功率 |
| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| C++（单次尝试） | ✗ | – | – | ✗ | – | – | ✗ | ✗ | – | – | 0% |
| DSL（单次尝试） | ✓ | ✓ | ✓ | ✓ | ✓ | – | ✓ | ✓ | ✓ | – | 80% |
| C++（迭代改进） | ✗ | – | – | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | 0% |
| DSL（迭代改进） | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | 100% |

表 2：代码生成成功率。用自然语言描述的 10 个映射策略的代码生成成功率。测试评估生成的代码能否通过编译并通过执行测试。两种设置下，生成 DSL 代码都显著优于生成 C++。符号含义：– 编译失败，✗ 编译通过但测试失败，✓ 通过测试。

随机 mapper 在所有应用上的表现持续低下，凸显了映射决策的关键作用。对每个应用，我们从 DSL 定义的完整搜索空间采样生成 10 个随机 mapper，9 个应用共 90 个。其中 74 个（82.2%）因无效映射决策引发运行时错误。运行时系统通过在执行期间拒绝此类 mapper 来保证正确性，其吞吐量为 0。

比较优化轨迹时，Trace 的表现与 OPRO 相近，并显著胜过 OpenTuner。为进一步比较基于智能体的优化器与传统强化学习，我们把 OpenTuner 的优化迭代从 10 次扩展到 1000 次，如图 5 所示，其中 x 轴为对数尺度的迭代次数，y 轴为相对吞吐量（对全部 9 个基准取平均）。值得注意的是，即便 OpenTuner 运行 1000 次迭代，Trace 仍取得 3.8 倍于它的加速。当两者都限于 10 次迭代时，Trace 胜过 OpenTuner 11 倍，展示了其快速识别高性能映射的能力。这凸显了 Trace（生成式优化器）相对 OpenTuner（传统强化学习）的优越性。此外，Trace 对每个应用仅需 10 分钟即可完成整个优化过程，把 mapper 开发时间从数天缩短到几分钟。

为更全面地呈现性能变化，我们提供更多统计量，包括我们方法与 OpenTuner 的均值、标准差、最差、中位数与最佳归一化吞吐量。这些统计量来自每个基准的 5 次运行，详见第 A.4 节。

#### 案例分析

Trace 相对专家 mapper 的最大性能增益出现在 Circuit 上，加速为 1.34 倍。这一改进主要源于*内存放置*：最佳 mapper 把两个数据集合分配到 GPU FrameBuffer 内存，而专家 mapper 把它们放在 GPU ZeroCopy 内存。尽管 GPU 间通信成本略有增加，Trace 因更快的内存访问而缩短了任务执行时间，带来更高的整体性能。对矩阵乘法算法，最大加速出现在 COSMA 上，Trace 相对专家 mapper 取得 1.31 倍加速。这归功于 Trace 更高效的索引映射函数，它通过在 GPU 间更好地分布分区子矩阵来*减少 GPU 间通信*。更多背景见第 A.8 节的 Trace mapper 示例。

### 5.2 DSL 用于代码生成的消融研究

在第 5.1 节中，我们展示了本方法的整体有效性。这里我们对 DSL——智能体-系统接口的核心——做消融研究。由于成功的生成是优化的基础，本小节聚焦 DSL 相比 C++ 能多好地帮助 LLM*生成*语法与语义正确的 mapper，而非直接*优化*性能。

图 6：不同反馈设计的比较。0-Shot 与 5-Shot 是基线。Execution 仅提供原始执行输出作为反馈。Explain 提供执行错误的额外解释。Suggest 提供 mapper 修改建议。所有反馈均为自动生成。

#### 实验设置

我们设计了 10 个用自然语言描述的映射策略，评估 LLM 能否用 DSL 与原始低层 C++ 生成正确代码。这些策略详见第 A.7 节。为确保公平比较，DSL 与 C++ 提供相同的提示材料（文档、示例与起始代码）。成功率依据生成的代码能否通过预定义测试用例衡量，并分别报告单次尝试与迭代改进（允许 LLM 最多 10 次迭代用编译器反馈改进代码）的结果。评估使用 DSPy（Khattab et al., 2023）框架进行。

#### 结果

表 2 显示，无论单次尝试还是迭代改进设置，DSL 的生成成功率都显著高于 C++。这证明了 DSL 设计在抽象系统复杂性、提供使 LLM 能够应对复杂系统代码生成挑战的高级接口方面的有效性。结合编译器反馈的迭代改进进一步提升了成功率，解决了 C++ 的四个编译错误与 DSL 的两个。不过，DSL mapper 与 C++ mapper 之间的差距依然巨大。值得注意的是，这些结果令人瞩目，因为 DSL 是一种没有预训练或微调数据的低资源语言，而 C++ 代码在 LLM 训练语料中广泛存在。

#### 分析

LLM 用 DSL 表现更好有两个原因。第一，自然语言与代码之间的语义差距在 DSL 下比 C++ 下更小。例如，编写一个「把所有数据在内存中对齐到 64 字节并使用 Fortran 序」的 mapper，在 DSL 中因*声明式设计*只需一行 `Layout * * * Align==64 F_order`。相比之下，C++ 映射 API 需要一系列操作来强制对齐与排序，这扩大了语义差距。第二，DSL 减少了代码量。如前所述，LLM 平均减少 14 倍的代码行数，简化了代码生成。这些结果凸显了高级智能体-系统接口的重要性。

### 5.3 AutoGuide 反馈的消融研究

AutoGuide 机制向智能体优化器提供增强的反馈。我们与替代反馈设计进行比较。

#### 实验设置

我们比较以下基线。0-shot 与 5-shot 无反馈，允许 LLM 在提供 0 个或 5 个示例的情况下一次性生成。Execution 仅提供原始执行反馈，Explain 提供执行错误的额外解释，Suggest 提供 mapper 修改建议。图 4 中展示的 Trace 轨迹使用完整的 AutoGuide 模式（Execution+Explain+Suggest 全开）。作为消融研究，我们评估 3 个基准。

#### 结果与分析

图 6 表明，完整反馈机制一致地胜过所有削减反馈的变体。0-shot 与 5-shot 的结果最差，凸显了基于反馈的迭代改进的重要性。这突出了智能体工作流的价值，表明性能提升并非仅由提示 LLM 驱动，而是工作流设计中迭代改进的直接结果。

## 6 结论

本文提出了一个利用 LLM 自动化 mapper 生成与优化的系统。智能体-系统接口（ASI）通过领域特定语言（DSL）简化代码生成——它抽象掉系统代码的低层复杂性——并通过 AutoGuide 丰富执行反馈——它把原始执行输出解读为可执行的指导。我们采用生成式优化，允许 LLM 利用标量指标之外的丰富文本反馈改进 mapper。与依赖数值奖励的 OpenTuner 等基于强化学习的方法不同，我们的方法纳入错误解释与针对性建议，加速了搜索效率。实验表明，智能体生成的 mapper 胜过专家手写的 mapper，在九个基准上取得最高 1.34 倍加速。我们的方法仅运行 10 次迭代，即便 OpenTuner 运行 1000 次迭代后仍保持 3.8 倍优势。通过把 mapper 开发时间从数天缩短到几分钟，我们的方法惠及计算科学家，并展示了生成式优化在系统设计中的有效性。

## 致谢

本工作部分由 Google Research Award 资助。我们感谢 Yuhui Zhang、Genghan Zhang、Qizheng Zhang、Mohammad R. Fadiheh、Ed Chen、Mert Yuksekgonul、Chenyang Yang、Jiaxin Ge、Simon Guo 与 Anne Ouyang 的反馈。我们感谢 Ching-An Cheng 与 Ken Liu 的讨论与反馈。

## 影响声明

本文提出的工作旨在推进机器学习领域。我们的工作有许多潜在的社会影响，但我们认为没有必要在此特别强调其中任何一项。

## 参考文献

- Agarwal et al. (1995)

  Agarwal, R. C., Balle, S. M., Gustavson, F. G., Joshi, M., and Palkar, P.
  A three-dimensional approach to parallel matrix multiplication.
  *IBM Journal of Research and Development*, 39(5):575–582, 1995.
- AhmadiTeshnizi et al. (2024a)

  AhmadiTeshnizi, A., Gao, W., Brunborg, H., Talaei, S., and Udell, M.
  OptiMUS-0.3: Using large language models to model and solve optimization problems at scale.
  *Submitted*, 2024a.
  URL <https://arxiv.org/abs/2407.19633>.
- AhmadiTeshnizi et al. (2024b)

  AhmadiTeshnizi, A., Gao, W., and Udell, M.
  OptiMUS: Scalable optimization modeling using MIP solvers and large language models.
  In *International Conference on Machine Learning (ICML)*, 2024b.
  URL <https://arxiv.org/abs/2402.10172>.
- Ansel et al. (2014)

  Ansel, J., Kamil, S., Veeramachaneni, K., Ragan-Kelley, J., Bosboom, J., O’Reilly, U.-M., and Amarasinghe, S.
  Opentuner: An extensible framework for program autotuning.
  In *Proceedings of the 23rd international conference on Parallel architectures and compilation*, pp. 303–316, 2014.
- Augonnet et al. (2009)

  Augonnet, C., Thibault, S., Namyst, R., and Wacrenier, P.-A.
  Starpu: a unified platform for task scheduling on heterogeneous multicore architectures.
  In *European Conference on Parallel Processing*, pp. 863–874. Springer, 2009.
- Augonnet et al. (2010)

  Augonnet, C., Clet-Ortega, J., Thibault, S., and Namyst, R.
  Data-Aware Task Scheduling on Multi-Accelerator based Platforms.
  In *16th International Conference on Parallel and Distributed Systems*, pp. 291–298, Shangai, China, December 2010. IEEE.
  URL <https://hal.inria.fr/inria-00523937>.
- Barham et al. (2022)

  Barham, P., Chowdhery, A., Dean, J., Ghemawat, S., Hand, S., Hurt, D., Isard, M., Lim, H., Pang, R., Roy, S., et al.
  Pathways: Asynchronous distributed dataflow for ml.
  *Proceedings of Machine Learning and Systems*, 4:430–449, 2022.
- Bauer et al. (2012)

  Bauer, M., Treichler, S., Slaughter, E., and Aiken, A.
  Legion: Expressing locality and independence with logical regions.
  In *SC’12: Proceedings of the International Conference on High Performance Computing, Networking, Storage and Analysis*, pp. 1–11. IEEE, 2012.
- Cannon (1969)

  Cannon, L. E.
  *A cellular computer to implement the Kalman filter algorithm*.
  Montana State University, 1969.
- Chamberlain et al. (2007)

  Chamberlain, B. L., Callahan, D., and Zima, H. P.
  Parallel programmability and the chapel language.
  *The International Journal of High Performance Computing Applications*, 21(3):291–312, 2007.
- Cheng et al. (2024)

  Cheng, C.-A., Nie, A., and Swaminathan, A.
  Trace is the next autodiff: Generative optimization with rich feedback, execution traces, and llms.
  *arXiv preprint arXiv:2406.16218*, 2024.
- Choi et al. (1994)

  Choi, J., Walker, D. W., and Dongarra, J. J.
  Pumma: Parallel universal matrix multiplication algorithms on distributed memory concurrent computers.
  *Concurrency: Practice and Experience*, 6(7):543–570, 1994.
- (13)

  Exascale Computing.
  DOE Explains Exascale Computing, 2025.
  <https://www.energy.gov/science/doe-explainsexascale-computing>.
- Fatahalian et al. (2006)

  Fatahalian, K., Horn, D. R., Knight, T. J., Leem, L., Houston, M., Park, J. Y., Erez, M., Ren, M., Aiken, A., Dally, W. J., and Hanrahan, P.
  Sequoia: Programming the memory hierarchy.
  In *SC ’06: Proceedings of the 2006 ACM/IEEE Conference on Supercomputing*, volume 0 of *SC ’06*, pp. 83–es, New York, NY, USA, 2006. Association for Computing Machinery.
  ISBN 0769527000.
- Feng et al. (2023)

  Feng, S., Hou, B., Jin, H., Lin, W., Shao, J., Lai, R., Ye, Z., Zheng, L., Yu, C. H., Yu, Y., et al.
  Tensorir: An abstraction for automatic tensorized program optimization.
  In *Proceedings of the 28th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 2*, pp. 804–817, 2023.
- Ferenbaugh (2015)

  Ferenbaugh, C. R.
  Pennant: an unstructured mesh mini-app for advanced architecture research.
  *Concurrency and Computation: Practice and Experience*, 27(17):4555–4572, 2015.
- Galvez et al. (2017)

  Galvez, J. J., Jain, N., and Kale, L. V.
  Automatic topology mapping of diverse large-scale parallel applications.
  In *Proceedings of the International Conference on Supercomputing*, pp. 1–10, 2017.
- Guo et al. (2024)

  Guo, T., Chen, X., Wang, Y., Chang, R., Pei, S., Chawla, N. V., Wiest, O., and Zhang, X.
  Large language model based multi-agents: A survey of progress and challenges.
  *arXiv preprint arXiv:2402.01680*, 2024.
- Gur et al. (2023)

  Gur, I., Furuta, H., Huang, A., Safdari, M., Matsuo, Y., Eck, D., and Faust, A.
  A real-world webagent with planning, long context understanding, and program synthesis.
  *arXiv preprint arXiv:2307.12856*, 2023.
- Haj-Ali et al. (2020a)

  Haj-Ali, A., Ahmed, N. K., Willke, T., Shao, Y. S., Asanovic, K., and Stoica, I.
  Neurovectorizer: End-to-end vectorization with deep reinforcement learning.
  In *Proceedings of the 18th ACM/IEEE International Symposium on Code Generation and Optimization*, pp. 242–255, 2020a.
- Haj-Ali et al. (2020b)

  Haj-Ali, A., Huang, Q. J., Xiang, J., Moses, W., Asanovic, K., Wawrzynek, J., and Stoica, I.
  Autophase: Juggling hls phase orderings in random forests with deep reinforcement learning.
  *Proceedings of Machine Learning and Systems*, 2:70–81, 2020b.
- Heller et al. (2017)

  Heller, T., Diehl, P., Byerly, Z., Biddiscombe, J., and Kaiser, H.
  Hpx–an open source c++ standard library for parallelism and concurrency.
  *Proceedings of OpenSuCo*, 5, 2017.
- Hong et al. (2023)

  Hong, S., Zheng, X., Chen, J., Cheng, Y., Wang, J., Zhang, C., Wang, Z., Yau, S. K. S., Lin, Z., Zhou, L., et al.
  Metagpt: Meta programming for multi-agent collaborative framework.
  *arXiv preprint arXiv:2308.00352*, 2023.
- Huang et al. (2021)

  Huang, T.-W., Lin, D.-L., Lin, C.-X., and Lin, Y.
  Taskflow: A lightweight parallel and heterogeneous task graph computing system.
  *IEEE Transactions on Parallel and Distributed Systems*, 33(6):1303–1320, 2021.
- Jangda et al. (2022)

  Jangda, A., Huang, J., Liu, G., Sabet, A. H. N., Maleki, S., Miao, Y., Musuvathi, M., Mytkowicz, T., and Saarikivi, O.
  Breaking the computation and communication abstraction barrier in distributed machine learning workloads.
  In *Proceedings of the 27th ACM International Conference on Architectural Support for Programming Languages and Operating Systems*, pp. 402–416, 2022.
- Jin et al. (2024)

  Jin, H., Huang, L., Cai, H., Yan, J., Li, B., and Chen, H.
  From llms to llm-based agents for software engineering: A survey of current, challenges and future.
  *arXiv preprint arXiv:2408.02479*, 2024.
- Kaiser et al. (2014)

  Kaiser, H., Heller, T., Adelstein-Lelbach, B., Serio, A., and Fey, D.
  Hpx: A task based programming model in a global address space.
  In *Proceedings of the 8th International Conference on Partitioned Global Address Space Programming Models*, pp. 1–11, 2014.
- Kannan et al. (2024)

  Kannan, S. S., Venkatesh, V. L., and Min, B.-C.
  Smart-llm: Smart multi-agent robot task planning using large language models.
  In *2024 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)*, pp. 12140–12147. IEEE, 2024.
- Khattab et al. (2023)

  Khattab, O., Singhvi, A., Maheshwari, P., Zhang, Z., Santhanam, K., Vardhamanan, S., Haq, S., Sharma, A., Joshi, T. T., Moazam, H., et al.
  Dspy: Compiling declarative language model calls into self-improving pipelines.
  *arXiv preprint arXiv:2310.03714*, 2023.
- Kwasniewski et al. (2019)

  Kwasniewski, G., Kabić, M., Besta, M., VandeVondele, J., Solcà, R., and Hoefler, T.
  Red-blue pebbling revisited: near optimal parallel matrix-matrix multiplication.
  In *Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis*, pp. 1–22, 2019.
- Lattimore & Szepesvári (2020)

  Lattimore, T. and Szepesvári, C.
  *Bandit algorithms*.
  Cambridge University Press, 2020.
- Li et al. (2023)

  Li, G., Hammoud, H., Itani, H., Khizbullin, D., and Ghanem, B.
  Camel: Communicative agents for" mind" exploration of large language model society.
  *Advances in Neural Information Processing Systems*, 36:51991–52008, 2023.
- Li et al. (2024)

  Li, J., Wang, S., Zhang, M., Li, W., Lai, Y., Kang, X., Ma, W., and Liu, Y.
  Agent hospital: A simulacrum of hospital with evolvable medical agents.
  *arXiv preprint arXiv:2405.02957*, 2024.
- Ltaief et al. (2024)

  Ltaief, H., Alomairy, R., Cao, Q., Ren, J., Slim, L., Kurth, T., Dorschner, B., Bougouffa, S., Abdelkhalak, R., and Keyes, D. E.
  Toward capturing genetic epistasis from multivariate genome-wide association studies using mixed-precision kernel ridge regression.
  In *SC24: International Conference for High Performance Computing, Networking, Storage and Analysis*, pp. 1–12. IEEE, 2024.
- Mirhoseini et al. (2017)

  Mirhoseini, A., Pham, H., Le, Q. V., Steiner, B., Larsen, R., Zhou, Y., Kumar, N., Norouzi, M., Bengio, S., and Dean, J.
  Device placement optimization with reinforcement learning.
  In *International conference on machine learning*, pp. 2430–2439. PMLR, 2017.
- Mirhoseini et al. (2021)

  Mirhoseini, A., Goldie, A., Yazgan, M., Jiang, J. W., Songhori, E., Wang, S., Lee, Y.-J., Johnson, E., Pathak, O., Nazi, A., et al.
  A graph placement methodology for fast chip design.
  *Nature*, 594(7862):207–212, 2021.
- Moritz et al. (2018)

  Moritz, P., Nishihara, R., Wang, S., Tumanov, A., Liaw, R., Liang, E., Elibol, M., Yang, Z., Paul, W., Jordan, M. I., et al.
  Ray: A distributed framework for emerging {\{AI}\} applications.
  In *13th USENIX Symposium on Operating Systems Design and Implementation (OSDI 18)*, pp. 561–577, 2018.
- Nie et al. (2024)

  Nie, A., Cheng, C.-A., Kolobov, A., and Swaminathan, A.
  The importance of directional feedback for llm-based optimizers.
  *arXiv preprint arXiv:2405.16434*, 2024.
- O’Boyle et al. (2013)

  O’Boyle, M. F. P., Wang, Z., and Grewe, D.
  Portable mapping of data parallel programs to opencl for heterogeneous systems.
  In *Proceedings of the 2013 IEEE/ACM International Symposium on Code Generation and Optimization (CGO)*, CGO ’13, pp. 1–10, USA, 2013. IEEE Computer Society.
  ISBN 9781467355247.
  doi: 10.1109/CGO.2013.6494993.
  URL <https://doi.org/10.1109/CGO.2013.6494993>.
- Patel et al. (2024)

  Patel, B., Chakraborty, S., Suttle, W. A., Wang, M., Bedi, A. S., and Manocha, D.
  Aime: Ai system optimization via multiple llm evaluators.
  *arXiv preprint arXiv:2410.03131*, 2024.
- Poesia et al. (2017)

  Poesia, G., Guimarães, B., Ferracioli, F., and Pereira, F. M. Q. a.
  Static placement of computation on heterogeneous devices.
  *Proceedings of the ACM on Programming Languages*, 1(OOPSLA), October 2017.
- Ramirez & Esparrell (2024)

  Ramirez, E. A. B. and Esparrell, J. A. F.
  Artificial intelligence (ai) in education: Unlocking the perfect synergy for learning.
  *Educational Process: International Journal*, 13(1):35–51, 2024.
- Ren et al. (2008)

  Ren, M., Park, J. Y., Houston, M., Aiken, A., and Dally, W. J.
  A tuning framework for software-managed memory hierarchies.
  In *Proceedings of the 17th International Conference on Parallel Architectures and Compilation Techniques*, PACT ’08, pp. 280–291, New York, NY, USA, 2008. Association for Computing Machinery.
  ISBN 9781605582825.
  doi: 10.1145/1454115.1454155.
  URL <https://doi.org/10.1145/1454115.1454155>.
- SFX Teixeira et al. (2023)

  SFX Teixeira, T., Henzinger, A., Yadav, R., and Aiken, A.
  Automated mapping of task-based programs onto distributed and heterogeneous machines.
  In *Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis*, pp. 1–13, 2023.
- Shao et al. (2024)

  Shao, Y., Jiang, Y., Kanell, T. A., Xu, P., Khattab, O., and Lam, M. S.
  Assisting in writing wikipedia-like articles from scratch with large language models.
  *arXiv preprint arXiv:2402.14207*, 2024.
- Slaughter et al. (2015)

  Slaughter, E., Lee, W., Treichler, S., Bauer, M., and Aiken, A.
  Regent: A high-productivity programming language for hpc with logical regions.
  In *Proceedings of the International Conference for High Performance Computing, Networking, Storage and Analysis*, pp. 1–12, 2015.
- Snoek et al. (2012)

  Snoek, J., Larochelle, H., and Adams, R. P.
  Practical bayesian optimization of machine learning algorithms.
  *Advances in neural information processing systems*, 25, 2012.
- Solomonik & Demmel (2011)

  Solomonik, E. and Demmel, J.
  Communication-optimal parallel 2.5 d matrix multiplication and lu factorization algorithms.
  In *Euro-Par 2011 Parallel Processing: 17th International Conference, Euro-Par 2011, Bordeaux, France, August 29-September 2, 2011, Proceedings, Part II 17*, pp. 90–109. Springer, 2011.
- Stocks et al. (2024)

  Stocks, R., Vallejo, J. L. G., Fiona, C., Snowdon, C., Palethorpe, E., Kurzak, J., Bykov, D., and Barca, G. M.
  Breaking the million-electron and 1 eflop/s barriers: Biomolecular-scale ab initio molecular dynamics using mp2 potentials.
  In *SC24: International Conference for High Performance Computing, Networking, Storage and Analysis*, pp. 1–12. IEEE, 2024.
- Sutton & Barto (2018)

  Sutton, R. S. and Barto, A. G.
  *Reinforcement learning: An introduction*.
  MIT press, 2018.
- Unger et al. (2022)

  Unger, C., Jia, Z., Wu, W., Lin, S., Baines, M., Narvaez, C. E. Q., Ramakrishnaiah, V., Prajapati, N., McCormick, P., Mohd-Yusof, J., et al.
  Unity: Accelerating {\{DNN}\} training through joint optimization of algebraic transformations and parallelization.
  In *16th USENIX Symposium on Operating Systems Design and Implementation (OSDI 22)*, pp. 267–284, 2022.
- Van De Geijn & Watts (1997)

  Van De Geijn, R. A. and Watts, J.
  Summa: Scalable universal matrix multiplication algorithm.
  *Concurrency: Practice and Experience*, 9(4):255–274, 1997.
- Van der Wijngaart & Mattson (2014)

  Van der Wijngaart, R. F. and Mattson, T. G.
  The parallel research kernels.
  In *2014 IEEE High Performance Extreme Computing Conference (HPEC)*, pp. 1–6. IEEE, 2014.
- Wang et al. (2024)

  Wang, X., Liu, S., Tsaris, A., Choi, J.-Y., Aji, A. M., Fan, M., Zhang, W., Yin, J., Ashfaq, M., Lu, D., et al.
  Orbit: Oak ridge base foundation model for earth system predictability.
  In *SC24: International Conference for High Performance Computing, Networking, Storage and Analysis*, pp. 1–11. IEEE, 2024.
- Wang & O’Boyle (2009)

  Wang, Z. and O’Boyle, M. F.
  Mapping parallelism to multi-cores: A machine learning based approach.
  In *Proceedings of the 14th ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming*, PPoPP ’09, pp. 75–84, New York, NY, USA, 2009. Association for Computing Machinery.
  ISBN 9781605583976.
  doi: 10.1145/1504176.1504189.
  URL <https://doi.org/10.1145/1504176.1504189>.
- Wu et al. (2023)

  Wu, Q., Bansal, G., Zhang, J., Wu, Y., Zhang, S., Zhu, E., Li, B., Jiang, L., Zhang, X., and Wang, C.
  Autogen: Enabling next-gen llm applications via multi-agent conversation framework.
  *arXiv preprint arXiv:2308.08155*, 2023.
- Yadav et al. (2022)

  Yadav, R., Aiken, A., and Kjolstad, F.
  Distal: the distributed tensor algebra compiler.
  In *Proceedings of the 43rd ACM SIGPLAN International Conference on Programming Language Design and Implementation*, pp. 286–300, 2022.
- Yang et al. (2023)

  Yang, C., Wang, X., Lu, Y., Liu, H., Le, Q. V., Zhou, D., and Chen, X.
  Large language models as optimizers.
  *arXiv preprint arXiv:2309.03409*, 2023.
- Yang et al. (2024a)

  Yang, C., Wang, X., Lu, Y., Liu, H., Le, Q. V., Zhou, D., and Chen, X.
  Large language models as optimizers.
  In *International Conference on Learning Representations*, 2024a.
- Yang et al. (2024b)

  Yang, J., Jimenez, C. E., Wettig, A., Lieret, K., Yao, S., Narasimhan, K., and Press, O.
  Swe-agent: Agent-computer interfaces enable automated software engineering.
  *arXiv preprint arXiv:2405.15793*, 2024b.
- Yao et al. (2022)

  Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., and Cao, Y.
  React: Synergizing reasoning and acting in language models.
  *arXiv preprint arXiv:2210.03629*, 2022.
- Yuksekgonul et al. (2024)

  Yuksekgonul, M., Bianchi, F., Boen, J., Liu, S., Huang, Z., Guestrin, C., and Zou, J.
  Textgrad: Automatic" differentiation" via text.
  *arXiv preprint arXiv:2406.07496*, 2024.
- Zheng et al. (2020a)

  Zheng, L., Jia, C., Sun, M., Wu, Z., Yu, C. H., Haj-Ali, A., Wang, Y., Yang, J., Zhuo, D., Sen, K., et al.
  Ansor: Generating {\{High-Performance}\} tensor programs for deep learning.
  In *14th USENIX symposium on operating systems design and implementation (OSDI 20)*, pp. 863–879, 2020a.
- Zheng et al. (2022a)

  Zheng, L., Li, Z., Zhang, H., Zhuang, Y., Chen, Z., Huang, Y., Wang, Y., Xu, Y., Zhuo, D., Xing, E. P., et al.
  Alpa: Automating inter-and {\{Intra-Operator}\} parallelism for distributed deep learning.
  In *16th USENIX Symposium on Operating Systems Design and Implementation (OSDI 22)*, pp. 559–578, 2022a.
- Zheng et al. (2020b)

  Zheng, S., Liang, Y., Wang, S., Chen, R., and Sheng, K.
  Flextensor: An automatic schedule exploration and optimization framework for tensor computation on heterogeneous system.
  In *Proceedings of the Twenty-Fifth International Conference on Architectural Support for Programming Languages and Operating Systems*, pp. 859–873, 2020b.
- Zheng et al. (2022b)

  Zheng, S., Chen, R., Wei, A., Jin, Y., Han, Q., Lu, L., Wu, B., Li, X., Yan, S., and Liang, Y.
  Amos: enabling automatic mapping for tensor computations on spatial accelerators with hardware abstraction.
  In *Proceedings of the 49th Annual International Symposium on Computer Architecture*, pp. 874–887, 2022b.
- Zheng et al. (2025)

  Zheng, S., Fang, J., Zheng, X., Hou, Q., Bao, W., Zheng, N., Jiang, Z., Wang, D., Ye, J., Lin, H., et al.
  Tilelink: Generating efficient compute-communication overlapping kernels using tile-centric primitives.
  *arXiv preprint arXiv:2503.20313*, 2025.
- Zhou et al. (2022)

  Zhou, D., Schärli, N., Hou, L., Wei, J., Scales, N., Wang, X., Schuurmans, D., Cui, C., Bousquet, O., Le, Q., et al.
  Least-to-most prompting enables complex reasoning in large language models.
  *arXiv preprint arXiv:2205.10625*, 2022.

## 附录 A 附录

### A.1 映射的图示

我们在图 A1 中展示映射的图示。

![Refer to caption](2410.15625v4/mapping.png)

图 A1：mapper 决定任务图中每个任务到处理器的放置、数据到内存的放置，以及数据的迭代空间如何被分区并映射到不同的处理器。

### A.2 DSL 语法

终结符：TaskName、RegionName、var、int

语法规则：

```text
Program        → Statement+
Statement      → TaskMap | DataMap | DataLayout | FuncDef | IndexTaskMap TaskName var
TaskMap        → Task TaskName Proc+
DataMap        → Region TaskName RegionName Proc Memory+
Proc           → CPU | GPU | OMP
Memory         → SYSMEM | FBMEM | ZCMEM
DataLayout     → Layout TaskName RegionName Proc Constraint+
Constraint     → SOA | AOS | C_order | F_order | Align == int
FuncDef        → def var(var+): FuncStmt+
FuncStmt       → var = Expr | return Expr
Expr           → var | var(Expr+) | Machine(Proc) | Expr.Expr | Expr Op Expr | (Expr)
               | Expr[Expr] | *Expr | Expr ? Expr : Expr
```

### A.3 并行矩阵乘法算法

#### 2D 算法

Cannon's（Cannon, 1969）为分布式矩阵乘法引入了带分块数据划分的脉动通信模式。PUMMA（Choi et al., 1994）与 SUMMA（Van De Geijn & Watts, 1997）扩展了该方法，支持非方阵并通过流水线提升通信效率。它们被称为 2D 算法，因为它们把矩阵划分为 2D 分块，然后映射到处理器空间。

#### 非 2D 算法

Johnson's（Agarwal et al., 1995）提出了一种 3D 算法，把输入矩阵划分为 3D 分块，并使用每处理器额外内存来减少相对 2D 算法的通信。Solomonik's（Solomonik & Demmel, 2011）通过使用额外内存进一步最小化通信，在 2D 与 3D 方法之间取得平衡。COSMA（Kwasniewski et al., 2019）则采用不同思路，依据输入规模与机器规模优化处理器网格与并行化策略。

### A.4 更多性能统计

在我们的设置中，报告多次运行的最佳结果是恰当的，因为最佳 mapper 正是用户想要的。mapper 搜索是一个离线优化过程，多次运行优化器以选出性能最高的 mapper 是可行的。一经识别，该 mapper 可以复用而不产生额外搜索成本，因为部署场景（应用、输入与硬件）保持固定。

话虽如此，关于性能变化的更多统计可以提供更完整的图景。这里我们给出我们的方法 Trace 与 OpenTuner 在每个基准 5 次运行中的均值、标准差、最差、中位数与最佳归一化吞吐量。

| 基准 | 均值 | 标准差 | 最差 | 中位数 | 最佳 |
| --- | --- | --- | --- | --- | --- |
| Circuit | 1.33× | 0.01 | 1.31× | 1.33× | 1.34× |
| Stencil | 1.01× | 0.01 | 1.00× | 1.01× | 1.02× |
| Pennant | 1.03× | 0.02 | 1.00× | 1.03× | 1.04× |
| Cannon | 1.09× | 0.00 | 1.08× | 1.09× | 1.09× |
| SUMMA | 0.86× | 0.48 | 0.00× | 1.07× | 1.09× |
| PUMMA | 0.57× | 0.55 | 0.00× | 0.66× | 1.09× |
| Johnson | 0.98× | 0.17 | 0.68× | 1.06× | 1.07× |
| Solomonik | 0.52× | 0.41 | 0.00× | 0.61× | 1.09× |
| COSMA | 1.25× | 0.03 | 1.23× | 1.23× | 1.31× |

表 A1：我们的框架 Trace 的归一化吞吐量。

| 基准 | 均值 | 标准差 | 最差 | 中位数 | 最佳 |
| --- | --- | --- | --- | --- | --- |
| Circuit | 0.97× | 0.16 | 0.81× | 0.99× | 1.20× |
| Stencil | 0.00× | 0.00 | 0.00× | 0.00× | 0.00× |
| Pennant | 0.00× | 0.00 | 0.00× | 0.00× | 0.00× |
| Cannon | 0.00× | 0.00 | 0.00× | 0.00× | 0.00× |
| SUMMA | 0.00× | 0.00 | 0.00× | 0.00× | 0.00× |
| PUMMA | 0.00× | 0.00 | 0.00× | 0.00× | 0.00× |
| Johnson | 0.00× | 0.00 | 0.00× | 0.00× | 0.00× |
| Solomonik | 0.00× | 0.00 | 0.00× | 0.00× | 0.00× |
| COSMA | 0.00× | 0.00 | 0.00× | 0.00× | 0.00× |

表 A2：OpenTuner 的归一化吞吐量。

我们的方法在大多数基准上取得相对稳定的性能。SUMMA、PUMMA 与 Solomonik 中较高的方差与偶尔出现的 0.00× 最差吞吐量，源于搜索空间中的无效 mapper 配置（例如违反 cuBLAS 布局约束）。运行时通过在执行期间拒绝此类配置来保证正确性。虽然生成式优化器通常能通过 AutoGuide 机制学会避免这些情形，但在 10 次迭代预算内偶尔的失败仍有可能。实践中，可以通过重复优化并选择表现最好的 mapper 来缓解此类失败。相比之下，OpenTuner 即便运行相同迭代次数，也在 9 个基准中的 8 个上无法生成有效 mapper。这凸显了用传统强化学习方法探索该搜索空间的困难。

### A.5 反馈配置示例

我们在表 A3 中给出原始执行输出与增强反馈的示例。增强反馈包括错误解释与 mapper 修改建议。

| 案例 | 原始执行输出 | AutoGuide |  |
| --- | --- | --- | --- |
|  |  | 解释 | 建议 |
| case1 | 编译错误：Syntax error, unexpected :, expecting { | N/A | 函数定义中不应有冒号 :。 |
| case2 | 编译错误：IndexTaskMap's function undefined | N/A | 在使用 IndexTaskMap 函数之前先定义它。 |
| case3 | 编译错误：mgpu not found | N/A | 在生成的代码中加入 mgpu = Machine(GPU);。 |
| case4 | 执行错误：Assertion failed: stride does not match expected value. | 内存布局不符合预期。 | 调整布局约束，或把任务移到其他处理器类型。 |
| case5 | 执行错误：DGEMM parameter number 8 had an illegal value | 内存布局不符合预期。 | 调整布局约束。 |
| case6 | 执行错误：Slice processor index out of bound | IndexTaskMap 语句引发错误。 | 确保 mgpu 的第一个索引以 % mgpu.size[0] 结尾，第二个元素以 % mgpu.size[1] 结尾。 |
| case7 | 执行错误：Assertion 'event.exists()' failed | InstanceLimit 语句引发错误。 | 避免生成 InstanceLimit 语句。 |
| case8 | 性能指标：执行时间为 0.03s。 | N/A | 把更多任务移到 GPU 以缩短执行时间。 |
| case9 | 性能指标：达到吞吐量 = 4877 GFLOPS | N/A | 尝试使用不同的 IndexTaskMap 或 SingleTaskMap 语句以最大化吞吐量。 |

表 A3：不同案例的原始执行输出与 AutoGuide（错误解释与调整建议）。

### A.6 Trace 智能体代码

Trace（Cheng et al., 2024）使用 @bundle 等 Python 装饰器来标注 Python 程序。它使我们能够像自己编写 Python 程序那样设计一个 LLM 代码生成智能体。我们首先搭建了一个端到端可运行的 Python 程序，它可以通过在搜索空间上随机决策生成一个有效 mapper 程序。我们在图 A3 中展示 Trace Mapper 的高层结构。图 A2 展示我们如何把来自执行的反馈纳入以更新智能体。在每个优化步，Trace 会执行 DSLMapperGenerator 并收集相应的执行流以构建图。然后它调用 LLM 对任何用 @bundle(trainable=True) 装饰的函数执行更新。DSLMapperGenerator 的结构与 DSL 规定的搜索空间一致，LLM 优化器可以沿预先设计的轴做决策。我们注意到，这类设计只有在 Trace 等近期进展下才成为可能，用更早的基于 LLM 的框架要难做得多。

```python
policy = MapperAgent()
params = policy.parameters()
optimizer = trace.Optimizer(params)

app = GetApplicationInfo()
test = GetMapperEvaluator(app)

for i in range(iterations):
    # Forward pass
    try:
        mapper = policy(app)
        # feedback (str) contains performance
        feedback = test(mapper)
    except TraceExecutionError as e:
        feedback = str(e)
        target = e.exception_node

    # Backward pass and update
    optimizer.zero_feedback()
    optimizer.backward(target, feedback)
    optimizer.step()
```

图 A2：我们展示如何用 Trace（以类 PyTorch 语法）把来自执行的反馈纳入以更新智能体。

```python
import opto.trace as trace

class MapperAgent(trace.Module):
    @trace.bundle(trainable=True)
    def task_decision(self, tasks):
        ...

    @trace.bundle(trainable=True)
    def region_decision(self, regions):
        ...

    @trace.bundle(trainable=True)
    def layout_decision(self):
        ...

    @trace.bundle(trainable=True)
    def instance_limit_decision(self, tasks):
        ...

    @trace.bundle(trainable=True)
    def index_task_map_decision(self, index_tasks):

    @trace.bundle(trainable=True)
    def single_task_map_decision(self, single_tasks):
        ...

    def generate_mapper(self):
        """
        Generate the final mapper code by combining all code statements.
        """
        task_statements = self.task_decision(self.tasks)
        region_statements = self.region_decision(self.regions)
        layout_statements = self.layout_decision()
        instance_limit_statements = self.instance_limit_decision(self.tasks)
        index_task_map_statements = self.index_task_map_decision(self.index_tasks, self.index_task_specification)
        single_task_statements = self.single_task_map_decision(self.single_tasks)

        code_statements = (
            task_statements +
            region_statements +
            layout_statements +
            instance_limit_statements +
            index_task_map_statements +
            single_task_statements
        )
        # Combine all code statements and function definitions into a single string
        code_list = code_statements
        mapper_code = str_join(node('\n'), *code_list)
        return mapper_code
```

图 A3：基于 Trace 的智能体模板的高层结构，其中用 @bundle(trainable=True) 标注的函数定义了 LLM 优化器在 mapper 生成期间更新的搜索空间。注：该智能体作为所有任务的共享起点。对每个任务，我们从这个起始智能体产出一个 mapper，然后让 LLM「优化」该智能体（通过修改可训练的函数）以产出对该特定任务最优的 mapper。

### A.7 映射策略

策略 1：把 calculate_new_currents、distribute_charge、update_voltages 的任务按如下方式映射到 GPU：把 2D GPU 处理器空间线性化为 1D，然后从启动域到线性化的 1D 处理器空间执行 1D 块映射。

```text
Task * GPU,CPU; # for any task, run on GPU if supported
Region * *GPU FBMEM; # for any task, any region, if mapped onto GPU, use FBMEM as default
Region * * CPU SYSMEM; # if mapped onto CPU, use SYSMEM as default

Layout * * * SOA C_order;

mcpu = Machine(CPU);
mgpu = Machine(GPU);

========== Above is fixed ==========
def linearblock(Task task) {
    return mgpu[task.ipoint[0] / mgpu.size[1], task.ipoint[0] % mgpu.size[1]];
}

IndexTaskMap calculate_new_currents,distribute_charge,update_voltages linearblock;
```

策略 2：把 ghost/shared 区域（rp_shared 与 rp_ghost）放到 GPU 零拷贝内存。

```text
Task * GPU,CPU; # for any task, run on GPU if supported

Region * * GPU FBMEM; # for any task, any region, if mapped onto GPU, use FBMEM as default
Region * * CPU SYSMEM; # if mapped onto CPU, use SYSMEM as default

Layout * * * SOA C_order;

mcpu = Machine(CPU);
mgpu = Machine(GPU);

========== Above is fixed ==========

Region * rp_shared GPU ZCMEM;
Region * rp_ghost GPU ZCMEM;
```

策略 3：对所有数据使用数组结构（AOS）数据布局，替代默认的 SOA。

```text
Task * GPU,CPU; # for any task, run on GPU if supported

Region * * GPU FBMEM; # for any task, any region, if mapped onto GPU, use FBMEM as default
Region * * CPU SYSMEM; # if mapped onto CPU, use SYSMEM as default

mcpu = Machine(CPU);
mgpu = Machine(GPU);

========== Above is fixed ==========

Layout * * * AOS;
```

策略 4：对所有数据使用 Fortran 序数据布局，替代默认的 C 序。

```text
Task * GPU,CPU; # for any task, run on GPU if supported

Region * * GPU FBMEM; # for any task, any region, if mapped onto GPU, use FBMEM as default
Region * * CPU SYSMEM; # if mapped onto CPU, use SYSMEM as default

mcpu = Machine(CPU);
mgpu = Machine(GPU);

========== Above is fixed ==========

Layout * * * F_order;
```

策略 5：把所有区域对齐到 64 字节，同时使用 Fortran 序数据布局。

```text
Task * GPU,CPU; # for any task, run on GPU if supported

Region * * GPU FBMEM; # for any task, any region, if mapped onto GPU, use FBMEM as default
Region * * CPU SYSMEM; # if mapped onto CPU, use SYSMEM as default

mcpu = Machine(CPU);
mgpu = Machine(GPU);

========== Above is fixed ==========

Layout * * * Align==64 F_order;
```

策略 6：把任务 calculate_new_currents 放到 CPU。

```text
Task * GPU,CPU; # for any task, run on GPU if supported

Region * * GPU FBMEM; # for any task, any region, if mapped onto GPU, use FBMEM as default
Region * * CPU SYSMEM; # if mapped onto CPU, use SYSMEM as default

mcpu = Machine(CPU);

mgpu = Machine(GPU);

Layout * * * SOA C_order;

========== Above is fixed ==========
Task calculate_new_currents CPU;
```

策略 7：收集任务 calculate_new_currents 使用的所有内存。

```text
Task * GPU,CPU; # for any task, run on GPU if supported

Region * * GPU FBMEM; # for any task, any region, if mapped onto GPU, use FBMEM as default
Region * * CPU SYSMEM; # if mapped onto CPU, use SYSMEM as default

mcpu = Machine(CPU);
mgpu = Machine(GPU);

Layout * * * SOA C_order;

========== Above is fixed ==========
CollectMemory calculate_new_currents *;
```

策略 8：确保任务 calculate_new_currents 最多同时运行 4 个实例。

```text
Task * GPU,CPU; # for any task, run on GPU if supported

Region * * GPU FBMEM; # for any task, any region, if mapped onto GPU, use FBMEM as default
Region * * CPU SYSMEM; # if mapped onto CPU, use SYSMEM as default

mcpu = Machine(CPU);
mgpu = Machine(GPU);

Layout * * * SOA C_order;

========== Above is fixed ==========
InstanceLimit calculate_new_currents 4;
```

策略 9：把任务 distribute_charge 的第二个区域参数映射到 GPU 的零拷贝内存。

```text
Task * GPU,CPU; # for any task, run on GPU if supported

Region * * GPU FBMEM; # for any task, any region, if mapped onto GPU, use FBMEM as default
Region * * CPU SYSMEM; # if mapped onto CPU, use SYSMEM as default

mcpu = Machine(CPU);
mgpu = Machine(GPU);

Layout * * * SOA C_order;

========== Above is fixed ==========
Region distribute_charge 1 GPU ZCMEM;
```

策略 10：把 calculate_new_currents、distribute_charge、update_voltages 的任务以 1D 循环方式映射到 GPU：在节点维与处理器维上都执行循环分布。

```text
Task * GPU,CPU; # for any task, run on GPU if supported

Region * * GPU FBMEM; # for any task, any region, if mapped onto GPU, use FBMEM as default
Region * * CPU SYSMEM; # if mapped onto CPU, use SYSMEM as default

mcpu = Machine(CPU);
mgpu = Machine(GPU);

Layout * * * SOA C_order;

========== Above is fixed ==========
def cyclic1d(Task task) {
    ip = task.ipoint;
    # cyclic over node, cyclic over gpu
    return mgpu[ip[0] % mgpu.size[0], ip[0] / mgpu.size[0] % mgpu.size[1]];
}

IndexTaskMap calculate_new_currents,distribute_charge,update_voltages cyclic1d;
```

### A.8 生成的 mapper 示例

这里我们给出一部分问题的生成 mapper 示例。这些用 DSL 编写的 mapper 由 mapper 智能体产出。虽然 LLM 负责创建与改进 mapper 智能体，但智能体本身用 Python 实现，并生成 DSL 程序形式的 mapper。
对电路模拟基准，优化后的 mapper（图 A5）比初始版本（图 A4）更简洁，并在数据布局中加入了字节对齐的额外约束。相比之下，对 Solomonik 算法，初始 mapper 相对简单（图 A6），而最终优化的 mapper 采用了更复杂、更细致的索引映射策略（图 A7）。

```text
Task * GPU,OMP,CPU;
Task calculate_new_currents GPU;
Task update_voltages GPU;
Region * * GPU FBMEM;
Region * * * SOCKMEM,SYSMEM;
Region * all_times GPU FBMEM;
Region * all_nodes GPU FBMEM;
Region * all_wires GPU FBMEM;
Region * ghost_ranges GPU FBMEM;
Region * rp_all_nodes GPU FBMEM;
Region * all_private GPU FBMEM;
Region * all_shared GPU FBMEM;
Region * rp_shared GPU FBMEM;
Region * rp_wires GPU FBMEM;
Region * rp_ghost_ranges GPU FBMEM;
Layout * * * C_order AOS;
mgpu = Machine(GPU);

m_2d = Machine(GPU);
def same_point(Task task) {
    return m_2d[*task.parent.processor(m_2d)];
}
```

图 A4：对 Circuit 任务，我们展示 mapper 智能体在第 2 次迭代产出的 mapper。

```text
Task * GPU,OMP,CPU;
Task calculate_new_currents GPU;
Task update_voltages GPU;
Region * * GPU FBMEM;
Layout * * * C_order AOS Align==128;
mgpu = Machine(GPU);

m_2d = Machine(GPU);
def same_point(Task task) {
    return m_2d[*task.parent.processor(m_2d)];
}
```

图 A5：对 Circuit 任务，我们展示 mapper 智能体在第 10 次迭代产出的 mapper。

```text
Task * GPU,OMP,CPU;
Region * * GPU FBMEM;
Region * * * SOCKMEM,SYSMEM;
Layout * * * F_order SOA;
mgpu = Machine(GPU);

def block1d(Task task) {
    ip = task.ipoint;
    return mgpu[ip[0] % mgpu.size[0], ip[0] % mgpu.size[1]];
}

IndexTaskMap task_2 block1d;

m_2d = Machine(GPU);
def same_point(Task task) {
    return m_2d[*task.parent.processor(m_2d)];
}
```

图 A6：对 Solomonik 算法，我们展示 mapper 智能体在第 2 次迭代产出的 mapper。

```text
Task * GPU,OMP,CPU;
Region * * GPU FBMEM;
Region * * * SOCKMEM,SYSMEM;
Layout * * * C_order SOA No_Align;
mgpu = Machine(GPU);

def linearize3D(Task task) {
    ip = task.ipoint;
    linearize = ip[0] + ip[1] + ip[2];
    return mgpu[linearize % mgpu.size[0], linearize % mgpu.size[1]];
}

IndexTaskMap task_1 linearize3D;

def linearize2D(Task task) {
    ip = task.ipoint;
    linearize = ip[0] * 2 + ip[2];
    return mgpu[linearize % mgpu.size[0], linearize % mgpu.size[1]];
}

IndexTaskMap task_1 linearize2D;
IndexTaskMap task_2 linearize2D;
IndexTaskMap task_3 linearize2D;
IndexTaskMap task_5 linearize2D;

m_2d = Machine(GPU);
def same_point(Task task) {
    return m_2d[*task.parent.processor(m_2d)];
}
```

图 A7：对 Solomonik 算法，我们展示 mapper 智能体在第 10 次迭代产出的 mapper。
