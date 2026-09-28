---
title: "Darwin Gödel Machine：自我改进智能体的开放式进化"
title_en: "Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents"
arxiv: 2505.22954
source: https://arxiv.org/abs/2505.22954
crawled: 2026-09-23
translated: 2026-09-23
---

# Darwin Gödel Machine：自我改进智能体的开放式进化

> 原文：[Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents](https://arxiv.org/abs/2505.22954) · Stanford CS329A 指定阅读

注：¹ 共同第一作者；† 共同资深作者。

Jenny Zhang（University of British Columbia；Vector Institute）

Shengran Hu（University of British Columbia；Vector Institute；Sakana AI）

Cong Lu（University of British Columbia；Vector Institute；Sakana AI）

Robert Lange（Sakana AI）

Jeff Clune（University of British Columbia；Vector Institute；Canada CIFAR AI Chair）

邮箱：{jennyzzt,srhu,conglu}@cs.ubc.ca，robert@sakana.ai，jeff.clune@ubc.ca

###### 摘要

如今的大多数 AI 系统都受限于人类设计的固定架构，无法自主且持续地自我改进。与此相对，科学方法是一种累积性的开放式系统：每一项创新都建立在既有成果之上，从而催生未来的发现。人们愈发期待，当前推进 AI 的人工流程本身也能被自动化。若能安全地做到这一点，这样的自动化将加速 AI 的发展，让我们更早收获其红利。这一前景引出了一个问题：AI 系统如何在不断提升解决相关问题的能力的同时，无尽地自我改进？元学习可以自动发现新算法，但受限于一阶改进，也受限于对合适搜索空间的人工设计。哥德尔机（Gödel machine）（Schmidhuber, 2007）提出了一种理论上的替代方案：一种以可证明有益的方式反复修改自身的自我改进 AI。遗憾的是，在实践中证明大多数改动是净有益的并不可能。我们提出 Darwin Gödel Machine（DGM），一种新颖的自我改进系统：它迭代地修改自己的代码（从而也提升其修改自身代码库的能力），并利用编码基准测试对每次改动进行实证验证。受达尔文进化与开放式进化（open-endedness）研究的启发，DGM 会不断扩充一个由生成的编码智能体组成的档案库。它从该档案库中采样智能体，让这些智能体自我修改，创造出新的、有趣的自身版本。这种开放式探索形成一棵不断生长的、由多样且高质量的智能体构成的树，并支持对搜索空间中许多不同路径的并行探索。在实验中，DGM 自动改进了自身的编码能力（例如更好的代码编辑工具、长上下文窗口管理、同行评审机制），在 SWE-bench 上的性能从 20.0% 提升到 50.0%，在 Polyglot 上从 14.2% 提升到 30.7%。此外，DGM 显著优于没有自我改进或没有开放式探索的基线。所有实验均在安全防护措施（如沙箱隔离、人类监督）下进行。总体而言，DGM 代表了向自我改进 AI 迈出的重要一步：这样的 AI 能够在一条不断展开、通向无尽创新的道路上，自行收集自己的垫脚石。

全部代码已在 <https://github.com/jennyzzt/dgm> 开源。

## 1 引言

科学进步是累积且开放式的，每一项突破都站在无数先前洞察的肩膀上。同样，我们最先进的 AI 系统也建立在一长串创新谱系之上。例如，Transformer（Vaswani et al., 2017）——当前大语言模型（LLM）（Brown et al., 2020）的骨干——并非孤立出现，而是建立在多年过往创新之上，例如循环神经网络（Linnainmaa, 1970；Amari, 1972；Hopfield, 1982；Rumelhart et al., 1985）与注意力机制（Schmidhuber and Huber, 1990；Bahdanau et al., 2015；Kim et al., 2017；Parikh et al., 2016）。然而，如今的大多数 AI 系统仍受限于固定的、人类设计的架构，只能在预定义的边界内学习，不具备自主重写自身源代码以自我改进的能力。因此，AI 发展的每一步进展仍在很大程度上依赖人类干预，束缚了进步的步伐。本文研究一个引人入胜的可能性：安全地自动化对越来越好的 AI 的搜索。可以想象这样一个 AI 系统，它像科学发现本身一样，成为自身进步的引擎——立足于自己的过去、递归地改进、并推动自身迈向更高级的能力。

![Refer to caption](2505.22954v3/conceptual.png)

图 1：Darwin Gödel Machine。DGM 通过将自我修改与下游任务评估交替进行，迭代地构建一个不断增长的智能体档案库。档案库中的智能体通过开放式探索被选出进行自我修改。

Schmidhuber（2007）提出了一类数学上严谨的、自指的、自我改进的问题求解器。它依赖形式化证明来论证代码重写，确保任何自我修改都是可证明有益的。然而在实践中，若不对系统施加限制性假设，就无法形式化地证明对 AI 系统的某项修改是否有益。例如，虽然一个基于 LLM 的编码智能体似乎会从更多工具（如代码搜索、测试运行器）中受益，但实际影响在很大程度上取决于模型的训练与任务情境（例如，为某一环境优化的测试工具在其他环境下可能会让智能体陷入困惑）。我们不要求形式化证明，而是针对基准测试对自我修改进行实证验证，让系统基于观测到的结果来改进和探索。这一做法与生物进化类似：突变与适应不会被预先验证，而是先产生、再试验，然后经由自然选择被筛选。我们还从达尔文进化（Darwin, 2023）中汲取灵感，研究维护一个由已发现智能体构成的库、将其作为后续世代垫脚石的有效性。

我们提出 Darwin Gödel Machine（DGM），一个自指的自我改进系统，它编写并修改自己的代码，从而成为更好的编码智能体。每次自我修改都要求 DGM 编辑自己的代码库。我们使用 Python——它是图灵完备的——使 DGM 有潜力构建任何可计算的机器。我们的框架设想智能体能够重写自己的训练脚本（包括训练一个新的基础模型（FM））。但本文不展示这一点，因为训练 FM 计算开销巨大，且会引入大量额外复杂性，我们将其留作未来工作。相反，本文聚焦于在冻结的预训练 FM 之上改进编码智能体的设计（例如工具使用、工作流）。DGM 在自我修改阶段与评估阶段之间交替。在自我修改阶段，从档案库中选出的编码智能体生成修改后的自身版本。在评估阶段，每个修改后的智能体在一个编码基准测试上接受检验，以估计其编码能力，然后被加入档案库。通过这一循环改进自身能力，DGM 在解决编码任务与进行未来的自我改进两方面都变得更好。一个关键假设是：编码基准测试性能的提升表明更强的编码能力，因而也表明更强的自我修改与自我改进能力。此外，DGM 维护一个由生成的编码智能体构成的档案库，初始化时只有一个智能体，并随时间不断累积所有生成的变体。为支持持续的自我改进，DGM 借鉴开放式进化研究（Wang et al., 2019；Fernando et al., 2024；Faldor et al., 2025），累积多样的垫脚石（即有趣但次优、却可能催生未来突破的解或特征）。这种开放式探索鼓励发现即时性能收益之外的新颖且潜在有用的自我修改。

我们在两个编码基准测试上给出结果：SWE-bench（Jimenez et al., 2024）与 Polyglot（Paul Gauthier, 2024）。DGM 在 SWE-bench 上自动将自己从 20.0% 改进到 50.0%，在 Polyglot 上从 14.2% 改进到 30.7%。我们表明，自我改进能带来持续进步：DGM 优于反复使用同一基础智能体来修改并生成新智能体（即没有自我改进）的基线。我们还表明，开放式探索与保留所有已生成智能体的档案库，能带来对更好的编码智能体的发现。DGM 优于没有开放式探索的基线（即不累积一个由「有趣地不同」的垫脚石构成的档案库的基线，其中编码智能体总是基于自己的最新版本进行构建）。总体而言，DGM 代表了迈向能够立足于自身先前创新并递归改进的 AI 系统的一步。我们深入考虑并讨论了安全性问题，包括沙箱隔离与自我修改的可追溯性，以确保负责任的实验（第 5 节）。通过推进安全、自指、自我改进模型的可能性，DGM 让我们更接近这样一种 AI：它不仅学习，而且像科学本身一样，沿着开放式、自我加速的轨迹进化。

## 2 相关工作

开放式进化（Open-Endedness）。驱动无界创新的一大挑战，是设计能够持续产生新颖且可学习产物的开放式 AI 系统（Stanley et al., 2017）。Hughes et al.（2024）将开放式进化刻画为一个系统从观察者视角产生既新颖又可学习的产物序列的能力。核心难点在于如何组织并探索庞大的搜索空间，以持续产出令人类感兴趣的产物（Clune, 2019；Jiang et al., 2023）。早期进展借助质量-多样性算法、目标导向探索、内在动机与学习进展框架（Pugh et al., 2016；Ecoffet et al., 2019；Lehman and Stanley, 2011；Oudeyer et al., 2007），而近期进展则利用大规模基础模型（FM）作为人类「有趣性」的代理，以及跨多样领域生成与评估新颖行为的通用引擎（Brown et al., 2020；Hu et al., 2025；Zhang et al., 2024b）。然而，这些方法尚未闭合自指自我改进的回路，也就是说，下游任务上的改进并不能转化为更强的自我修改能力，也无法加速进一步的创新。我们希望模拟科学与技术的加速过程：新工具与新发现催化更多发现的产生。我们如何效仿自然的进化轨迹——它不仅趋向复杂性，还趋向越来越强的进化能力（Dawkins, 2019；Gerhart and Kirschner, 2007；Hendrikse et al., 2007）？

元学习 FM 智能体。许多基于 FM 的智能体是手工打造的。其中一些建模要素包括提示工程（Chen et al., 2023；Schulhoff et al., 2024）、思维链（Wei et al., 2022；Yao et al., 2023；Hu and Clune, 2024；Guo et al., 2025；Lightman et al., 2023；Muennighoff et al., 2025；Zelikman et al., 2024a）、自我反思（Shinn et al., 2023；Yao et al., 2023；Madaan et al., 2023）、多智能体辩论（Zhuge et al., 2023；Liang et al., 2023；Khan et al., 2024）、记忆（Liu et al., 2023；Zhong et al., 2024；Modarressi et al., 2023）、温度采样（Zhu et al., 2024）与检索增强生成（Lewis et al., 2020）。这些组件的人工组合使系统的能力受限于其人类设计者的巧思。近来涌现了多种利用 FM 的元学习方法，可自动优化提示（Fernando et al., 2024；(FAIR)† et al., 2022；Khattab et al., 2023；Cheng et al., 2024；Yuksekgonul et al., 2024；Yuan et al., 2024）并设计智能体模块（Zhang et al., 2024c；Zhou et al., 2024；Yin et al., 2024；Zhuge et al., 2024；Rosser and Foerster, 2025；Zhang et al., 2025a；Ye et al., 2025；Gao et al., 2025；Nie et al., 2025；Su et al., 2025；Zhang et al., 2025b；Niu et al., 2025）。智能体系统的自动化设计（Automated Design of Agentic Systems，ADAS）（Hu et al., 2025）用一个固定的元智能体迭代生成下游智能体，在目标基准测试上评估它们，并结合反馈改进后续世代。与之相反，DGM 是一个单一系统，既求解下游任务（即编码问题），又改进自身的实现（即其代码库），从而无需固定的人工设计元智能体，并实现自指的改进。

自我改进 AI。早期，多位研究者概述了自我改进的理论与概念路径（Good, 1966；Schmidhuber, 1987；Schmidhuber, 2007）。自动化自我改进的一些实践方法包括由神经网络权重参数化定义的系统（Schmidhuber, 1993；Hall, 2007；Hobbhahn, 2025；Kirsch and Schmidhuber, 2022；Irie et al., 2022；Irie et al., 2025；Lu et al., 2023；Havrilla et al., 2024b）。Metz et al.（2021）开发了一个基于梯度的优化器，使用种群训练的一个变体（Jaderberg et al., 2017）进行自指的元训练。Lange et al.（2023）将该方法扩展到无梯度学习。Silver et al.（2017）利用自我博弈持续进化智能体，在国际象棋与围棋等挑战性领域取得了超人类表现。与 DGM 更接近的是近期利用基于 FM 的智能体进行自我改进的方法（Yin et al., 2024；Robeyns et al., 2025；Hu et al., 2024；Zelikman et al., 2024b；Huang et al., 2022；Singh et al., 2023）。Zelikman et al.（2024b）使用元智能体生成下游智能体，并依据从生成解中导出的元效用更新元智能体。Yin et al.（2024）使用单一系统既求解下游任务又递归修改自身。然而，下游任务或元效用并不总是与自我改进所需的能力对齐。在 DGM 中，下游任务的改进直接反映自我改进能力的提升，从而使自我加速的进步成为可能。最相似的是 Robeyns et al.（2025）的同期工作，它同样由单一智能体递归地解决编码问题并修改自己的代码库。与 Robeyns et al.（2025）（以及 Zelikman et al., 2024b；Yin et al., 2024）的主要区别在于：DGM 具有一个开放式探索回路，鼓励即时性能收益之外的自我修改，从而避免停滞在次优状态。附录 B 还讨论了关于程序合成与达尔文进化的其他相关工作。

## 3 Darwin Gödel Machine

哥德尔机是一种理论上的 AI 构想：它搜索可证明能够改进自身的方式（Schmidhuber, 2007）。本文提出 Darwin Gödel Machine（DGM），一次实现创造哥德尔机这一长期梦想的尝试。DGM 放宽了哥德尔机「在理论上证明某项改动会改进系统」这一不切实际的要求，转而要求来自实验的实证证据来表明所提出的新版本能提升性能。此外，由于 DGM 依赖改进的实证证据，它可能陷入可能系统（即所有可计算算法）构成的庞大搜索空间中的局部最优。为解决这一问题，DGM 在搜索过程中维护一个由已发现解构成的档案库，促成开放式探索，而不是只演化单一解。由于其原理与达尔文进化（Darwin, 2023）相呼应（附录 B）——从先前发现的解的档案库中选择一个实体、修改它，若它有趣地新颖则保留（Zhang et al., 2024b；Faldor et al., 2025；Stanley and Lehman, 2015）——我们将我们的算法称为 Darwin Gödel Machine（图 1）。

编码智能体的自指自我改进。DGM 初始化时只有一个编码智能体，其进展在编码基准测试上评估。编码智能体被定义为一个单一系统，由一个代码仓库实现、由冻结的预训练基础模型（FM）驱动，能够读取、编写与执行代码。用通用图灵完备语言（如 Python）表达的代码，是构建与改进智能系统的强大媒介，因为它能表示任何可计算过程。近期工作（Hu et al., 2025；Zhang et al., 2024c）表明，这类智能体可以通过对它们的设计（如提示、工作流与工具，实现在其代码仓库中）做元学习来改进。因此，我们将自我改进定义为这样一项编码任务：修改智能体自身组件的设计（即它自己的代码，不含下一段所述的开放式探索过程）。关键动机在于：实证证据必须同时反映系统自我改进与求解下游任务的能力。通过将 DGM 配置为一个编码智能体并检验其编码能力，观测到的改进不仅表明下游任务性能的增强，也表明进一步自我改进的能力，因为自我改进本质上就是修改该编码智能体自身代码仓库的一项编码任务。

基于种群的开放式探索。从单一初始编码智能体出发，DGM 构建一个包含所有已发现智能体的档案库。每次迭代中，DGM 选择父代智能体进行自我修改并分叉产生新智能体。父代选择的概率大致正比于各智能体的性能分数、反比于其具有代码库编辑功能的后代数量（附录 C.2 节）。这有利于那些表现强劲却探索不足（即现有后代较少）的智能体，从而既强化对优秀者的利用，又鼓励对有潜力但较少被采样谱系的探索。所有智能体都保有非零的选择概率，确保在足够算力下任何改进路径都依然可行。每个被选中的父代分析自己的基准评估日志，提出下一个要实现的功能，并把该提议作为待执行的问题陈述接收（附录 C.3 节）。随后父代把建议的功能实现进自己的代码库，生成一个新的编码智能体。每个新生成的智能体都在选定的编码基准测试上做定量评估，以估计其编码能力。只有能成功编译且保留编辑给定代码库能力的智能体才会被加入 DGM 档案库，因为只有它们能继续自我修改；其余一律丢弃。父代选择、自我修改与评估的循环持续进行，逐步扩充解的档案库。值得注意的是，档案库中的解可以作为垫脚石，在其被发现很久之后才带来改进，这使我们的方法与爬山式的智能体设计方法（Robeyns et al., 2025）有本质不同。目前，开放式探索过程（即档案库维护、父代选择）是固定的，不可被 DGM 修改，我们将其留作未来工作。附录 C.4 节给出 DGM 算法的伪代码。

## 4 实验

第 4.1 节描述实验设置，包括初始化 DGM 的初始编码智能体。我们在两个编码基准测试上开展实验：SWE-bench（Jimenez et al., 2024）与 Polyglot（Paul Gauthier, 2024）（第 4.2 节）。对每个基准测试，我们将 DGM 与两个基线比较：不含自我改进智能体的 DGM 与不含开放式探索的 DGM（第 4.3 节）。在全部实验中，我们都发现 DGM 优于这两个基线，说明自我改进机制与开放式探索对持续的性能提升必不可少（第 4.4 节）。此外，我们表明 DGM 发现的功能可以跨模型、跨基准测试与跨任务迁移（第 4.4 节）。

### 4.1 实验设置

DGM 由单一编码智能体初始化。该基础智能体围绕一个冻结的 FM 构建，并被赋予工具使用能力（Schick et al., 2023；Anthropic, 2024b）。FM 在每一步自主决定其行动，使用它认为合适的任何工具。基础智能体可使用两个工具：一个用于执行 bash 命令的 Bash 工具，以及一个用于查看与编辑目录和整个文件的编辑工具（附录 C.1 节）。智能体接收单一输入提示，其中指定目标仓库的位置、问题陈述与仓库的测试框架（附录 C.1 节）。基础智能体被有意保持轻量，以提供一个简单的起点，使自我改进能够被清晰展示。我们将 DGM 运行 80 次迭代（每次迭代生成一个新智能体），SWE-bench 上两个迭代并行运行，Polyglot 上四个迭代并行运行（附录 C.2 节）。自我修改期间，SWE-bench 与 Polyglot 实验中的编码智能体均由 Claude 3.5 Sonnet (New)（Anthropic, 2024a）驱动。基准评估期间，编码智能体在 SWE-bench 上由 Claude 3.5 Sonnet (New) 驱动，在 Polyglot 上由 o3-mini（OpenAI, 2025）驱动（附录 D.1 节）。

### 4.2 基准测试

我们在两个评估编码任务不同方面的流行基准测试上评估 DGM，以验证算法在多种用例下的有效性。SWE-bench 与 Polyglot 都是评估 AI 智能体自动求解编码任务好坏的基准测试。给定一个代码仓库与一条任务指令，智能体需要对仓库做出修改以完成该任务。两者都是被广泛使用的基准测试（Zhang et al., 2024d；Zhang et al., 2024a；Xia et al., 2024；Cao et al., 2024；Google DeepMind, 2025；Gauthier, 2024），要求 AI 智能体在代码仓库中导航、理解不同文件中函数之间的相互作用，并在盘根错节的代码中发现细微错误。SWE-bench 只含 Python 任务，而 Polyglot 的任务覆盖多种编程语言。另一个区别是：每个 SWE-bench 任务可能需要编辑多个文件，而每个 Polyglot 任务主要是从头在单个文件中实现一个解（尽管智能体仍需查看其他文件以理解需要哪些改动），因此总体文件编辑次数更少。

SWE-bench。为避免把算力浪费在无解任务上，我们使用 SWE-bench Verified（OpenAI, 2024）——SWE-bench（Jimenez et al., 2024）经人工筛选、全部任务均可解的子集。在本文中，「SWE-bench」一词默认指 SWE-bench Verified 子集。

Polyglot。Polyglot 包含多种编程语言（C++、Rust、Python 等）的任务（Paul Gauthier, 2024）。与 SWE-bench——最广泛使用的编码基准测试之一、很可能已包含在 FM 训练集中——相比，Polyglot 更小众，更不可能出现在 FM 的后训练数据中。此外，Polyglot 主要被其开发者用于评估 Aider（Gauthier, 2024）。这提供了一个机会，把自动设计的智能体与社区中一个有代表性的编码智能体进行比较——后者由人类开发者针对 Polyglot 基准持续开发与测试超过一年。最后，Polyglot 能够检验 DGM 在 Python 之外多种编程语言上的泛化能力。我们遵循 Polyglot 排行榜的设置（Paul Gauthier, 2024），但有一个关键区别：排行榜报告 pass@2，其中智能体可以查看一次来自真值测试的反馈；而我们报告 pass@1，智能体从不看到真值测试结果。

由于在全量基准测试上评估成本高昂（附录 E.1 节），我们采用分阶段评估策略来估计编码智能体的性能。总体而言，当我们越有信心某个智能体相对较强时，就在越多任务上评估它。我们首先在一个 10 任务的集合上评估每个编码智能体，以验证基本的代码库编辑功能。只有保留代码编辑能力的智能体才能求解下游编码任务或进行进一步的自我修改。通过这一初始阶段的智能体随后在一个扩展的 50 任务集合上接受评估。对 SWE-bench，任务基于 SWE-bench-verified-mini（Hobbhahn, 2025）选取，后者被设计为全量基准测试的代表性样本（附录 E.2 节）。对 Polyglot，任务取自全量基准测试的随机子集（附录 E.3 节）。由于我们使用的 LLM 天然具有随机性，性能可能带有噪声。我们用较小的子集评估来估计总体有效性并识别顶尖候选者。对 SWE-bench，若一个编码智能体在 60 任务子集上成功率超过 40%（该阈值是根据初步运行中观察到的噪声选取的启发式值）且位列档案库中表现最佳的前两名，则会在 200 个任务（140 个加上先前的 60 个）上评估，以更准确地衡量其真实编码能力（附录 E.2 节）。对 Polyglot，若一个编码智能体在 10 任务子集上成功率超过 40%，则在扩展的 50 任务子集上评估（附录 E.3 节）。

### 4.3 基线

为分离并评估 DGM 核心组件的贡献，我们将 DGM 与两个基线比较：不含自我改进智能体的 DGM（DGM w/o self-improve）与不含开放式探索的 DGM（DGM w/o open-ended exploration）。DGM w/o self-improve 在此设置下复刻 ADAS（Hu et al., 2025）的方法：负责修改编码智能体的元智能体在整个实验中保持为初始基础智能体（算法 2）。该基线使我们能够评估迭代式自我改进在加速更优编码智能体演化中的作用。DGM w/o open-ended exploration 取消档案库的使用，总是自我修改其存储的最新版本（算法 3）。若一个编码智能体自我修改到失去编辑代码库所需的基本功能，它就无法再修改自己或求解任何编码任务。因此，DGM w/o open-ended exploration 会保留仍维持代码库编辑基本功能的最新自身版本。该基线使我们能够评估拥有档案库、以及有充分文献记载的开放式探索有益原则（Clune, 2019；Stanley and Lehman, 2015；Zhang et al., 2024b；Fernando et al., 2024；Lee et al., 2020；Samvelyan et al., 2024；Colas et al., 2022b）在引导智能体演化上的影响。

除学习型基线外，我们还将 DGM 与手工设计的开源方案进行比较。对 SWE-bench，我们取经过核验（即 SWE-bench 团队能够复现其结果）的最先进（SoTA）开源方案（附录 E.4 节）。对 Polyglot，我们取有代表性的智能体 Aider（Gauthier, 2024），它已开源，被设计为支持多种编程语言与大型代码库编辑（附录 E.5 节）。为公平比较，我们在与评估 DGM 相同的基准子集上测量求解任务的百分比（附录 E.2 节、附录 E.3 节）。这些数值在图 2 中以水平虚线表示。

### 4.4 结果

图 2：自我改进与开放式探索使 DGM 能够持续取得进展并提升性能。DGM 自动发现越来越好的编码智能体，在（左）SWE-bench 与（右）Polyglot 上都表现更佳。它优于缺少自我改进或开放式探索的基线，表明这两个组件对持续自我改进都必不可少。这些分数来自在第 4.2 节详述的基准子集上的评估。

![Refer to caption](2505.22954v3/dgm_archive.png)

![Refer to caption](2505.22954v3/dgm_progress.png)

图 3：DGM 自动自我改进，成为更好的编码智能体。（左）DGM 在 SWE-bench 上运行期间生成的编码智能体档案库。每个节点代表一个编码智能体，节点 0 对应基础智能体。节点颜色表示在 SWE-bench 上的性能（求解任务的百分比），边框颜色反映该智能体被评估的任务数。边表示哪些智能体自我修改产生了后代。许多创新路径穿过性能较低的节点，而关键创新（如节点 24）会引发建立在其上的创新爆发。这两个性质都凸显了开放式搜索的好处。（右）DGM 在 SWE-bench 上的进展图。浅蓝线表示所有具备基本代码库编辑功能的智能体的平均分。蓝线追踪每次迭代时档案库中任意智能体取得的最佳分数。深色线显示最终最佳发现智能体及其前驱节点的谱系，其中包含两次性能下跌。这说明了开放式搜索的好处：它探索一组多样的有趣垫脚石，而不是只专注于从目前找到的最佳解分叉。

经过 80 次 DGM 迭代，编码智能体的性能在 SWE-bench 上从 20.0% 提升到 50.0%，在 Polyglot 上从 14.0% 提升到 38.0%（图 2）。由于 Polyglot 实验设置中 DGM 只在 50 个任务上评估（第 4.2 节），我们另外在全量 Polyglot 基准测试上评估基础智能体与 DGM 发现的最佳智能体，以更准确地估计改进幅度。在全量 Polyglot 基准测试上，DGM 将编码智能体从 14.2% 提升到 30.7%。这表明 DGM 能够自动自我改进，创造出更好的编码智能体。此外，DGM 发现的最佳智能体的性能与 SWE-bench 上经过核验的开源人工设计 SoTA 相当（图 2）。在 Polyglot 上，尽管 DGM 从一个性能低于 Aider 的基础智能体起步，它发现了一个远超 Aider 的智能体（图 2）。在这两个基准测试上，DGM 发现的智能体与手工设计的智能体相当或更优。SoTA SWE-bench 智能体与 Aider 凝聚了人类的心血，而 DGM 预示着这样一个未来：这种巧思将被自动化，经由持续自我改进的自指循环不断演化。

DGM 自动改进了工具以及使用 FM 的工作流（图 3）。例如，DGM 增强了编辑工具，允许更细粒度的文件查看（按行）与更精确的文件编辑（按字符串替换），而不是总是查看或替换整个文件。工作流改进包括多次尝试求解一个任务，并使用另一个 FM 来评估并选择最佳解。其他工作流改进还包括在生成后续尝试时考虑先前的尝试。附录 F.1 节与附录 F.2 节分别展示了通往 SWE-bench 与 Polyglot 上最终最佳发现智能体的全部修改。

由于开放式探索允许以非零概率从档案库中的任意智能体分叉，DGM 能够摆脱性能上欺骗性的低谷或高峰。例如，在 SWE-bench 实验的第 4 次与第 56 次迭代，尽管智能体的分数暂时低于其父代，DGM 仍能沿该路径探索创新，并创造出一个超越所有前辈的新智能体（图 3）。此外，开放式探索允许对同一目标功能尝试不同的实现。例如，虽然目标是提供更细粒度的编辑工具，该功能的具体实现却可能差异很大，从而带来截然不同的性能（附录 G）。DGM 可以探索多种实现以找到最合适的一种，避免被困在次优实现中。

DGM 在两个基准测试上都优于 DGM w/o self-improve 与 DGM w/o open-ended exploration 基线（图 2）。在不更新修改编码智能体的元智能体的情况下，DGM w/o self-improve 在早期迭代中改进了智能体，但其收益很快趋于平缓（附录 A.1 节）。在 DGM w/o open-ended exploration 中，只保留最新智能体，因此一次表现不佳的自我修改会使后续改进更难实现（附录 A.1 节）。

图 4：在模型、基准测试与任务之间的迁移。DGM 发现智能体的优越性能可以迁移到（左）不同模型、（中）不同基准测试，以及（右）Polyglot 中不同的编程语言任务，例如从 Python 任务迁移到 C++ 任务。

为评估 DGM 所带来改进的普适性，我们用与优化时不同的 FM 测试了基础智能体（第 4.1 节）与 DGM 运行期间发现的最佳智能体（图 2）。对 SWE-bench——DGM 使用 Claude 3.5 Sonnet (New) 运行——我们把 FM 替换为 Claude 3.7 Sonnet（Anthropic, 2025）或 o3-mini，并在 200 个任务上评估（图 4，左）。用 o3-mini 时，基础智能体取得 23.0%，DGM 发现的智能体取得 33.0%。用 Claude 3.7 Sonnet 时，基础智能体取得 19.0%，DGM 发现的智能体取得 59.5%。这些结果表明，DGM 带来的改进可跨 FM 泛化，而不是与其运行时使用的特定 FM 紧耦合（图 4）。Polyglot 上的模型迁移结果见附录 A.2 节。

此外，我们研究了 DGM 发现的智能体跨基准测试与编程语言的可迁移性。第一，我们把在一个基准测试（如 SWE-bench）上演化出的最佳 DGM 智能体在一个完全留出的基准测试（如 Polyglot）上评估，反之亦然（图 4，中）。在 SWE-bench 上演化出的最佳智能体在 Polyglot 上取得 28.9%，而初始智能体的基线为 14.2%。反过来，在 Polyglot 上演化出的最佳智能体在 SWE-bench 上取得 24.5%，超过 20.0% 的原始基线。由于每个智能体在优化期间从未访问过另一个基准测试，这些评估是真正的留出测试。跨基准测试的一致性能提升支持了我们的论断：DGM 的改进反映的是通用技能的习得，而非过拟合或对基准特定伪影的利用。第二，我们实验了一个只在 Polyglot 的 Python 任务上训练的 DGM 版本，然后将发现的智能体迁移到其他语言的任务上。只聚焦 Python 任务会轻微提升 Python 任务上的性能，但相比在所有语言上训练的 DGM，会降低非 Python 任务上的性能（图 4，右）。然而，在搜索期间从 Python 迁移到其他未见语言后，该智能体仍取得与在所有语言上训练的 DGM 相当的性能，并大幅超过基础智能体与 Aider。这些结果证明了所发现改进的稳健性，表明它们不会过拟合到某一特定编程语言。我们还在附录 A 中给出额外结果。

## 5 安全性讨论

诸如 DGM 这样具备自我改进能力的系统，代表着朝更自主的 AI 开发迈出的一步，契合该领域让有能力 AI 造福人类的长期目标（Schmidhuber, 1987；Clune, 2019；Markoff, 2016；Lehman, 2023）。然而，这种能力也带来了源自系统自主修改自身代码这一能力的独特安全考量。单纯为基准性能优化的修改，可能在不经意间引入漏洞或与人类意图相悖的行为，即便它们改进了目标指标（Bostrom, 2020）。特别地，若评估基准测试没有完全覆盖所有期望的智能体属性（如安全性与稳健性），自我改进回路可能在连续世代中放大错位。迭代式自我修改还可能导致日益复杂且无法解释的内部逻辑，妨碍人类的理解、监督与控制（Sheth et al., 2025；Anwar et al., 2024；Greenblatt et al., 2024；Ganguli et al., 2022）。

认识到这些挑战，DGM 的当前实现与实验设置纳入了若干防护措施。所有智能体执行与自我修改过程都在隔离的沙箱环境中进行，限制其影响宿主系统的能力，从而缓解非预期行动的风险。沙箱内的每次执行都受到严格的时间限制，降低资源耗尽或无界行为的风险。自我改进过程目前局限于一个明确定义的领域：通过修改智能体自身的 Python 代码库来提升特定编码基准测试上的性能，从而限制潜在修改的范围。此外，我们主动监控智能体性能与代码变更，DGM 档案库提供了可追溯的修改谱系以供审查。在现阶段，我们没有在生成的智能体中发现有害或恶意行为的证据，自我修改始终主要聚焦于改进编码能力。

反过来，自我改进范式的一个重大潜在益处是：原则上，它也可以被引导用于增强安全性与可解释性本身。我们初步研究了如何将 DGM 部署到 AI 安全场景中，开发针对 FM 幻觉的对策（附录 H）。正如 DGM 学会改进其编码能力一样，若将这些属性纳入其评估标准（Rosser and Foerster, 2025），它也有可能发现并整合更好的内部防护措施，或为更高的透明度而修改自身（例如纳入类似 Constitutional AI 的原则（Bai et al., 2022））。这提示了一条虽有挑战但有希望的路径：自我改进成为构建更可信赖 AI 系统的工具。后续研究还可以探索从一开始就织入 Constitutional AI，不过挑战在于如何激励系统保留这些指令（一个值得探索的选项是创建系统中一个不可修改的部分，以便在终止时评估其余部分）。

由于当前前沿 FM 的局限以及沙箱隔离等有效缓解措施，DGM 在安全的研究边界内展示了自我改进 AI 的潜力。附录 I 给出了关于更广泛安全不确定性的额外讨论。我们主动纳入这段安全讨论，以提高对自我改进 AI 系统这一新兴前景及其相关安全影响的意识，尤其是因为这些系统不可避免地会变得更强大（Yudkowsky and others, 2008；Bostrom, 2002；Ecoffet et al., 2020；Bengio et al., 2024；Clune, 2019）。因此，我们倡导对 AI 生成算法（AI-Generating Algorithms，AI-GAs）（Clune, 2019）与自我改进系统的安全且有益的演化开展持续研究。

## 6 结论与局限

我们提出 Darwin Gödel Machine（DGM），第一个由 FM 驱动、具备开放式探索的自我改进系统，其在评估基准测试上的进步可以直接转化为更强的自我改进能力。我们展示了更好的工具与 FM 系统的自动发现，在 SWE-bench 与 Polyglot 两个基准测试上取得了更好的性能。通过自我改进与开放式探索，DGM 展现了性能的持续提升，让我们向自我加速、自我改进的 AI 系统又近了一步。

我们证明 DGM 能够自主取得与公开可得方案相当的性能。然而，它仍未达到闭源 SoTA SWE-bench 方案的水平。一个悬而未决的问题是：更长时间运行 DGM 是否会持续带来性能收益，并最终超越闭源方案。这些闭源方案往往依赖由高技能专家团队精心打造的复杂手工技术。由于 FM 尚未达到这类专家的能力水平（例如在推理方面），DGM 目前需要大量算力才能发现改进。如第 4 节所示，DGM 在 SWE-bench 上的一次运行耗时约 2 周，并产生可观的 API 开销（附录 E.1 节）。我们推测，进一步的进展将需要更高效地利用计算资源，并发展更好的推理技能。

由于这一版本的 DGM 主要由 FM 驱动，它天然受限于底层 FM 的能力。因此，一个激动人心的未来方向是把自我修改扩展到提示或 FM 工作流之外，纳入计算更密集的方法，例如重写自己的训练脚本来更新 FM 本身。虽然这一版本的 DGM 聚焦于编码，但 AI 系统正日益应用于广泛领域（如计算机视觉、创意写作）。另一个有希望的扩展是开发能够在编码领域之外增强自身的自我改进 AI 系统。本工作的一个关键假设是：编码基准测试很好地反映了智能体自我改进的能力，因为自我修改任务要求智能体修改自己的代码库。不过，也可以设想一种替代方案：协同演化目标任务分布（Faldor et al., 2025；Wang et al., 2023c），从而解除自我改进与单一目标绑定的约束，如同真正的开放式过程那样。附录 J 给出了更多潜在的未来工作方向。在我们继续探索这项强大技术的同时，也必须把安全放在核心位置，如第 5 节所讨论的。

总之，DGM 代表了通过能够编辑自身代码库的自我改进系统实现 AI 开发自动化的重要一步。尽管当前算力与推理方面的局限约束了其全部潜力，FM 与基础设施的持续进步可能解锁更强大、更通用的自我改进。只要审慎应对安全关切（第 5 节），自我改进 AI 系统与 AI 生成算法（Clune, 2019）的未来就蕴含着巨大希望：开放式地演化 AI，不断重写或重训自身，以追求与人类价值观对齐的更强能力。

## 伦理声明

我们确认遵守 ICLR 伦理准则。本工作在标准编程基准测试上评估的代码编辑智能体这一有限情境中研究自我改进 AI 系统。未涉及人类受试者，也未收集或处理任何个人身份信息（PII）；因此无需 IRB 批准。

安全与滥用。自我修改系统若被允许无约束地行动，或优化在不经意间引入不安全行为，可能带来安全风险。为缓解这一点，我们实验中的所有智能体都在隔离的沙箱内运行，并受到严格的资源与时间限制；智能体的网络访问受限，且无法修改宿主环境。自我改进的范围被限定在智能体自身的 Python 代码库与评估框架（harness）之内。我们维护了完整、可审计的代码变更与评估谱系（档案库），支持回滚与事后分析。我们没有在真实开发环境中部署发现的智能体。我们的发布计划（代码、提示与评估产物）将排除任何授予提升系统权限的组件，并将包含默认的沙箱隔离、护栏，以及对预期用途的清晰文档。

双重用途、下游影响与局限。更强的自主编码智能体可能具有双重用途（例如辅助软件维护，但若被误用也可能助长有害代码的创建）。我们相信研究收益（例如推进可控、可审计的自我改进方法，并展示实用的防护措施）大于风险。尽管如此，我们明确不鼓励在安全敏感或无沙箱的环境中部署，并给出了具体的安全建议（第 5 节）。我们对基准优化的实证聚焦可能无法覆盖所有期望属性（稳健性、可解释性或更广泛的社会价值）。因此，我们将基准收益视为通用 AI 发展的必要但非充分指标，并讨论把其他目标（如安全性、推理）纳入优化回路的途径。

数据治理、知识产权与许可。我们在 SWE-bench Verified 与 Polyglot 上评估，它们由开源仓库与任务构成。据我们所知，我们遵守了数据集许可与使用条款。我们没有引入或分发专有代码。基础模型（FM）通过提供商 API 按其服务条款访问；我们没有提交敏感数据，也没有试图规避使用政策。随本工作发布的日志将清除 API 密钥与任何偶发的敏感字符串。

偏差、公平与公正。尽管我们的领域是软件代码而非以人为中心的文本，FM 的行为仍可能反映偏差（如语言或生态系统偏好），并可能不均衡地有利于那些工具在训练数据中得到更充分代表的社区。我们通过跨多种语言评估（Polyglot）并报告跨基准迁移来部分应对这一问题。未来工作应为有偏差的失败模式添加诊断，并纳入更广泛的、社区驱动的任务集。

利益冲突与资助。没有任何作者在与本文评估性能相关的产品中拥有经济利益。资助方与雇主除提供薪酬或标准研究支持外，未影响实验设计、分析或发表决定。任何外部算力或 API 额度已在附录中致谢。

## 可复现性声明

我们将开源全部代码与完整的智能体日志，包括自我修改的完整档案谱系（diff、提示与配置）以及评估框架。为支持精确复现，我们援引以下内容：算法细节与伪代码（第 3 节、附录 C.4 节）；父代选择与开放式探索设置（附录 C.2 节）；基础模型选择与超参数（附录 D.1 节）；SWE-bench 与 Polyglot 的基准任务子集（附录 E.2 节、附录 E.3 节）；分阶段评估协议与脚本（第 4.2 节）；最佳发现智能体的实现与 diff（附录 F.1 节、附录 F.2 节）；以及算力与成本估计（附录 E.1 节）。发布的代码仓库将包含环境规格与脚本，以复现全部结果、图表。

#### 致谢

本研究得到 Vector Institute、Canada CIFAR AI Chairs 项目、Schmidt Futures 的一笔资助、一项 NSERC Discovery Grant，以及 Rafael Cosman 慷慨捐助的支持。准备本研究所用的资源部分由安大略省、加拿大政府（通过 CIFAR）以及赞助 Vector Institute 的公司（https://vectorinstitute.ai/partnerships/current-partners/）提供。本材料中表达的观点、发现、结论或建议均为作者本人观点，不一定反映资助方的看法。我们还感谢 Aaron Dharna、Ben Norman、Cédric Colas、Sam Devlin 与 Shyam Sudhakaran 带来的深入讨论与反馈。

## 参考文献

- (FAIR)† et al. (2022)
  M. F. A. R. D. T. (FAIR)†, A. Bakhtin, N. Brown, E. Dinan, G. Farina, C. Flaherty, D. Fried, A. Goff, J. Gray, H. Hu, et al.
  Human-level play in the game of Diplomacy by combining language models with strategic reasoning.
  Science 378 (6624), pp. 1067–1074.
- Aki et al. (2024)
  F. Aki, R. Ikeda, T. Saito, C. Regan, and M. Oka
  Llm-poet: Evolving complex environments using large language models.
  In Proceedings of the Genetic and Evolutionary Computation Conference Companion,
  pp. 243–246.
- Alur et al. (2018)
  R. Alur, R. Singh, D. Fisman, and A. Solar-Lezama
  Search-based program synthesis.
  Communications of the ACM 61 (12), pp. 84–93.
- Amari (1972)
  S. Amari
  Learning patterns and pattern sequences by self-organizing nets of threshold elements.
  IEEE Transactions on computers 100 (11), pp. 1197–1206.
- Andrychowicz et al. (2017)
  M. Andrychowicz, F. Wolski, A. Ray, J. Schneider, R. Fong, P. Welinder, B. McGrew, J. Tobin, O. Pieter Abbeel, and W. Zaremba
  Hindsight experience replay.
  Advances in neural information processing systems 30.
- Anthropic (2024a)
  Anthropic
  Claude 3.5 Sonnet.
   Anthropic.
  Note: <https://www.anthropic.com/news/claude-3-5-sonnet>[Accessed 17 April 2025]
- Anthropic (2024b)
  Anthropic
  Claude can now use tools.
  Note: Accessed: 2025-05-03
  External Links: [Link](https://www.anthropic.com/news/tool-use-ga)
- Anthropic (2025)
  Anthropic
  Claude 3.7 sonnet and claude code.
  Note: Accessed: 2025-05-06
  External Links: [Link](https://www.anthropic.com/news/claude-3-7-sonnet)
- Anwar et al. (2024)
  U. Anwar, A. Saparov, J. Rando, D. Paleka, M. Turpin, P. Hase, E. S. Lubana, E. Jenner, S. Casper, O. Sourbut, et al.
  Foundational challenges in assuring alignment and safety of large language models.
  arXiv preprint arXiv:2404.09932.
- Bahdanau et al. (2015)
  D. Bahdanau, K. H. Cho, and Y. Bengio
  Neural machine translation by jointly learning to align and translate.
  In International Conference on Learning Representations,
- Bai et al. (2022)
  Y. Bai, S. Kadavath, S. Kundu, A. Askell, J. Kernion, A. Jones, A. Chen, A. Goldie, A. Mirhoseini, C. McKinnon, et al.
  Constitutional AI: Harmlessness from AI feedback.
  arXiv preprint arXiv:2212.08073.
- Baranes and Oudeyer (2013)
  A. Baranes and P. Oudeyer
  Active learning of inverse models with intrinsically motivated goal exploration in robots.
  Robotics and Autonomous Systems 61 (1), pp. 49–73.
- Barke et al. (2024)
  S. Barke, E. Anaya Gonzalez, S. R. Kasibatla, T. Berg-Kirkpatrick, and N. Polikarpova
  Hysynth: context-free llm approximation for guiding program synthesis.
  Advances in Neural Information Processing Systems 37, pp. 15612–15645.
- Bengio et al. (2024)
  Y. Bengio, G. Hinton, A. Yao, D. Song, P. Abbeel, T. Darrell, Y. N. Harari, Y. Zhang, L. Xue, S. Shalev-Shwartz, et al.
  Managing extreme AI risks amid rapid progress.
  Science 384 (6698), pp. 842–845.
- Bostrom (2002)
  N. Bostrom
  Existential Risks: analyzing human extinction scenarios and related hazards.
  Journal of Evolution and Technology 9 (), pp. .
- Bostrom (2020)
  N. Bostrom
  Ethical issues in advanced artificial intelligence.
  Machine Ethics and Robot Ethics, pp. 69–75.
- Bradley et al. (2024)
  H. Bradley, A. Dai, H. B. Teufel, J. Zhang, K. Oostermeijer, M. Bellagente, J. Clune, K. Stanley, G. Schott, and J. Lehman
  Quality-diversity through ai feedback.
  In The Twelfth International Conference on Learning Representations,
- Brown et al. (2020)
  T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, et al.
  Language models are few-shot learners.
  Advances in neural information processing systems 33, pp. 1877–1901.
- Bruce et al. (2024)
  J. Bruce, M. D. Dennis, A. Edwards, J. Parker-Holder, Y. Shi, E. Hughes, M. Lai, A. Mavalankar, R. Steigerwald, C. Apps, et al.
  Genie: Generative interactive environments.
  In Forty-first International Conference on Machine Learning,
- Buchi and Landweber (1990)
  J. R. Buchi and L. H. Landweber
  Solving sequential conditions by finite-state strategies.
  In The collected works of J. Richard Büchi,
  pp. 525–541.
- Cao et al. (2024)
  R. Cao, F. Lei, H. Wu, J. Chen, Y. Fu, H. Gao, X. Xiong, H. Zhang, W. Hu, Y. Mao, et al.
  Spider2-v: how far are multimodal agents from automating data science and engineering workflows?.
  Advances in Neural Information Processing Systems 37, pp. 107703–107744.
- Chatzilygeroudis et al. (2021)
  K. Chatzilygeroudis, A. Cully, V. Vassiliades, and J. Mouret
  Quality-diversity optimization: a novel branch of stochastic optimization.
  In Black Box Optimization, Machine Learning, and No-Free Lunch Theorems,
  pp. 109–135.
- Chen et al. (2023)
  B. Chen, Z. Zhang, N. Langrené, and S. Zhu
  Unleashing the potential of prompt engineering in large language models: a comprehensive review.
  arXiv preprint arXiv:2310.14735.
- Cheng et al. (2024)
  C. Cheng, A. Nie, and A. Swaminathan
  Trace is the next autodiff: generative optimization with rich feedback, execution traces, and llms.
  Advances in Neural Information Processing Systems 37, pp. 71596–71642.
- Clune (2019)
  J. Clune
  AI-GAs: AI-generating algorithms, an alternate paradigm for producing general artificial intelligence.
  arXiv preprint arXiv:1905.10985.
- Colas et al. (2019)
  C. Colas, P. Fournier, M. Chetouani, O. Sigaud, and P. Oudeyer
  Curious: intrinsically motivated modular multi-goal reinforcement learning.
  In International conference on machine learning,
  pp. 1331–1340.
- Colas et al. (2022a)
  C. Colas, T. Karch, C. Moulin-Frier, and P. Oudeyer
  Language and culture internalization for human-like autotelic AI.
  Nature Machine Intelligence 4 (12), pp. 1068–1076.
- Colas et al. (2022b)
  C. Colas, T. Karch, O. Sigaud, and P. Oudeyer
  Autotelic agents with intrinsically motivated goal-conditioned reinforcement learning: a short survey.
  Journal of Artificial Intelligence Research 74, pp. 1159–1199.
- Colas et al. (2023)
  C. Colas, L. Teodorescu, P. Oudeyer, X. Yuan, and M. Côté
  Augmenting autotelic agents with large language models.
  In Conference on Lifelong Learning Agents,
  pp. 205–226.
- Coulom (2006)
  R. Coulom
  Efficient selectivity and backup operators in monte-carlo tree search.
  In International conference on computers and games,
  pp. 72–83.
- Darwin (2023)
  C. Darwin
  Origin of the species.
  In British Politics and the environment in the long nineteenth century,
  pp. 47–55.
- Dawkins (2019)
  R. Dawkins
  The evolution of evolvability.
  In Artificial life,
  pp. 201–220.
- Dennis et al. (2020)
  M. Dennis, N. Jaques, E. Vinitsky, A. Bayen, S. Russell, A. Critch, and S. Levine
  Emergent complexity and zero-shot transfer via unsupervised environment design.
  Advances in neural information processing systems 33, pp. 13049–13061.
- Dharna et al. (2024)
  A. Dharna, C. Lu, and J. Clune
  Quality-Diversity Self-Play: Open-Ended Strategy Innovation via Foundation Models.
  In NeurIPS 2024 Workshop on Open-World Agents,
- Ding et al. (2024)
  L. Ding, J. Zhang, J. Clune, L. Spector, and J. Lehman
  Quality diversity through human feedback: towards open-ended diversity-driven optimization.
  In Proceedings of the 41st International Conference on Machine Learning,
  pp. 11072–11090.
- Dobzhansky (1970)
  T. Dobzhansky
  Genetics of the evolutionary process.
  Vol. 139, Columbia University Press.
- Ecoffet et al. (2020)
  A. Ecoffet, J. Clune, and J. Lehman
  Open questions in creating safe open-ended AI: tensions between control and creativity.
  In Artificial Life Conference Proceedings 32,
  pp. 27–35.
- Ecoffet et al. (2019)
  A. Ecoffet, J. Huizinga, J. Lehman, K. O. Stanley, and J. Clune
  Go-explore: a new approach for hard-exploration problems.
  arXiv preprint arXiv:1901.10995.
- Ecoffet et al. (2021)
  A. Ecoffet, J. Huizinga, J. Lehman, K. O. Stanley, and J. Clune
  First return, then explore.
  Nature 590 (7847), pp. 580–586.
- Edwards (2000)
  A. W. F. Edwards
  The genetical theory of natural selection.
  Genetics 154 (4), pp. 1419–1426.
- Ellis et al. (2021)
  K. Ellis, C. Wong, M. Nye, M. Sablé-Meyer, L. Morales, L. Hewitt, L. Cary, A. Solar-Lezama, and J. B. Tenenbaum
  Dreamcoder: bootstrapping inductive program synthesis with wake-sleep library learning.
  In Proceedings of the 42nd acm sigplan international conference on programming language design and implementation,
  pp. 835–850.
- Eysenbach et al. (2018)
  B. Eysenbach, A. Gupta, J. Ibarz, and S. Levine
  Diversity is all you need: Learning skills without a reward function.
  arXiv preprint arXiv:1802.06070.
- Faldor et al. (2025)
  M. Faldor, J. Zhang, A. Cully, and J. Clune
  OMNI-EPIC: Open-endedness via Models of human Notions of Interestingness with Environments Programmed in Code.
  In The Thirteenth International Conference on Learning Representations,
  External Links: [Link](https://openreview.net/forum?id=Y1XkzMJpPd)
- Fernando et al. (2024)
  C. Fernando, D. S. Banarse, H. Michalewski, S. Osindero, and T. Rocktäschel
  Promptbreeder: Self-Referential Self-Improvement via Prompt Evolution.
  In Forty-first International Conference on Machine Learning,
- Ganguli et al. (2022)
  D. Ganguli, L. Lovitt, J. Kernion, A. Askell, Y. Bai, S. Kadavath, B. Mann, E. Perez, N. Schiefer, K. Ndousse, et al.
  Red teaming language models to reduce harms: methods, scaling behaviors, and lessons learned.
  arXiv preprint arXiv:2209.07858.
- Gao et al. (2025)
  H. Gao, Y. Liu, Y. He, L. Dou, C. Du, Z. Deng, B. Hooi, M. Lin, and T. Pang
  FlowReasoner: reinforcing query-level meta-agents.
  arXiv preprint arXiv:2504.15257.
- Gauthier (2024)
  P. Gauthier
  Aider: ai pair programming in your terminal.
   GitHub.
  Note: <https://github.com/Aider-AI/aider>Accessed: 2025-05-14
- Gaven et al. (2025)
  L. Gaven, T. Carta, C. Romac, C. Colas, S. Lamprier, O. Sigaud, and P. Oudeyer
  MAGELLAN: Metacognitive predictions of learning progress guide autotelic LLM agents in large goal spaces.
  arXiv preprint arXiv:2502.07709.
- Gerhart and Kirschner (2007)
  J. Gerhart and M. Kirschner
  The theory of facilitated variation.
  Proceedings of the National Academy of Sciences 104 (suppl_1), pp. 8582–8589.
- Good (1966)
  I. J. Good
  Speculations concerning the first ultraintelligent machine.
  In Advances in computers,
  Vol. 6, pp. 31–88.
- Google DeepMind (2025)
  Google DeepMind
  Gemini model “thinking” updates — march 2025.
  Note: <https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/#gemini-2-5-thinking>Accessed: 2025-05-11
- Greenblatt et al. (2024)
  R. Greenblatt, C. Denison, B. Wright, F. Roger, M. MacDiarmid, S. Marks, J. Treutlein, T. Belonax, J. Chen, D. Duvenaud, et al.
  Alignment faking in large language models.
  arXiv preprint arXiv:2412.14093.
- Gulwani (2011)
  S. Gulwani
  Automating string processing in spreadsheets using input-output examples.
  ACM Sigplan Notices 46 (1), pp. 317–330.
- Guo et al. (2025)
  D. Guo, D. Yang, H. Zhang, J. Song, R. Zhang, R. Xu, Q. Zhu, S. Ma, P. Wang, X. Bi, et al.
  Deepseek-r1: incentivizing reasoning capability in llms via reinforcement learning.
  arXiv preprint arXiv:2501.12948.
- Hall (2007)
  J. S. Hall
  Self-improving AI: An analysis.
  Minds and Machines 17 (3), pp. 249–259.
- Havrilla et al. (2024a)
  A. Havrilla, A. Dai, L. O’Mahony, K. Oostermeijer, V. Zisler, A. Albalak, F. Milo, S. C. Raparthy, K. Gandhi, B. Abbasi, et al.
  Surveying the effects of quality, diversity, and complexity in synthetic data from large language models.
  arXiv preprint arXiv:2412.02980.
- Havrilla et al. (2024b)
  A. Havrilla, S. Raparthy, C. Nalmpantis, J. Dwivedi-Yu, M. Zhuravinskyi, E. Hambro, and R. Raileanu
  Glore: When, where, and how to improve llm reasoning via global and local refinements.
  arXiv preprint arXiv:2402.10963.
- Hendrikse et al. (2007)
  J. L. Hendrikse, T. E. Parsons, and B. Hallgrímsson
  Evolvability as the proper focus of evolutionary developmental biology.
  Evolution & development 9 (4), pp. 393–401.
- Herr et al. (2025)
  N. Herr, T. Rocktäschel, and R. Raileanu
  LLM-first search: self-guided exploration of the solution space.
  arXiv preprint arXiv:2506.05213.
- Hobbhahn (2025)
  M. Hobbhahn
  SWE-bench verified mini.
  Note: <https://github.com/mariushobbhahn/SWEBench-verified-mini>Accessed: 2025-04-16
- Hopfield (1982)
  J. J. Hopfield
  Neural networks and physical systems with emergent collective computational abilities..
  Proceedings of the national academy of sciences 79 (8), pp. 2554–2558.
- Hu and Clune (2024)
  S. Hu and J. Clune
  Thought Cloning: learning to think while acting by imitating human thinking.
  Advances in Neural Information Processing Systems 36.
- Hu et al. (2025)
  S. Hu, C. Lu, and J. Clune
  Automated Design of Agentic Systems.
  In The Thirteenth International Conference on Learning Representations,
  External Links: [Link](https://openreview.net/forum?id=t9U3LW7JVX)
- Hu et al. (2024)
  Y. Hu, Y. Cai, Y. Du, X. Zhu, X. Liu, Z. Yu, Y. Hou, S. Tang, and S. Chen
  Self-evolving multi-agent collaboration networks for software development.
  arXiv preprint arXiv:2410.16946.
- Huang et al. (2022)
  J. Huang, S. S. Gu, L. Hou, Y. Wu, X. Wang, H. Yu, and J. Han
  Large language models can self-improve.
  arXiv preprint arXiv:2210.11610.
- Hughes et al. (2024)
  E. Hughes, M. Dennis, J. Parker-Holder, F. Behbahani, A. Mavalankar, Y. Shi, T. Schaul, and T. Rocktaschel
  Open-endedness is essential for artificial superhuman intelligence.
  arXiv preprint arXiv:2406.04268.
- Irie et al. (2025)
  K. Irie, R. Csordás, and J. Schmidhuber
  Metalearning continual learning algorithms.
  Transactions on Machine Learning Research.
- Irie et al. (2022)
  K. Irie, I. Schlag, R. Csordás, and J. Schmidhuber
  A modern self-referential weight matrix that learns to modify itself.
  In International Conference on Machine Learning,
  pp. 9660–9677.
- Jaderberg et al. (2017)
  M. Jaderberg, V. Dalibard, S. Osindero, W. M. Czarnecki, J. Donahue, A. Razavi, O. Vinyals, T. Green, I. Dunning, K. Simonyan, et al.
  Population based training of neural networks.
  arXiv preprint arXiv:1711.09846.
- Jiang et al. (2021)
  M. Jiang, E. Grefenstette, and T. Rocktäschel
  Prioritized level replay.
  In International Conference on Machine Learning,
  pp. 4940–4950.
- Jiang et al. (2023)
  M. Jiang, T. Rocktäschel, and E. Grefenstette
  General intelligence requires rethinking exploration.
  Royal Society Open Science 10 (6), pp. 230539.
- Jimenez et al. (2024)
  C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. R. Narasimhan
  SWE-bench: Can Language Models Resolve Real-world Github Issues?.
  In The Twelfth International Conference on Learning Representations,
  External Links: [Link](https://openreview.net/forum?id=VTF8yNQM66)
- Kanitscheider et al. (2021)
  I. Kanitscheider, J. Huizinga, D. Farhi, W. H. Guss, B. Houghton, R. Sampedro, P. Zhokhov, B. Baker, A. Ecoffet, J. Tang, O. Klimov, and J. Clune
  Multi-task curriculum learning in a complex, visual, hard-exploration domain: Minecraft.
  arXiv preprint arXiv:2106.14876.
- Khan et al. (2024)
  A. Khan, J. Hughes, D. Valentine, L. Ruis, K. Sachan, A. Radhakrishnan, E. Grefenstette, S. R. Bowman, T. Rocktäschel, and E. Perez
  Debating with more persuasive llms leads to more truthful answers.
  arXiv preprint arXiv:2402.06782.
- Khattab et al. (2023)
  O. Khattab, A. Singhvi, P. Maheshwari, Z. Zhang, K. Santhanam, S. Vardhamanan, S. Haq, A. Sharma, T. T. Joshi, H. Moazam, et al.
  Dspy: Compiling declarative language model calls into self-improving pipelines.
  arXiv preprint arXiv:2310.03714.
- Kim et al. (2017)
  Y. Kim, C. Denton, L. Hoang, and A. M. Rush
  Structured Attention Networks.
  In International Conference on Learning Representations,
- Kimura (1979)
  M. Kimura
  The neutral theory of molecular evolution.
  Scientific American 241 (5), pp. 98–129.
- Kirsch and Schmidhuber (2022)
  L. Kirsch and J. Schmidhuber
  Self-referential meta learning.
  In First Conference on Automated Machine Learning (Late-Breaking Workshop),
- Klissarov et al. (2023)
  M. Klissarov, P. D’Oro, S. Sodhani, R. Raileanu, P. Bacon, P. Vincent, A. Zhang, and M. Henaff
  Motif: Intrinsic motivation from artificial intelligence feedback.
  arXiv preprint arXiv:2310.00166.
- Klissarov et al. (2024)
  M. Klissarov, M. Henaff, R. Raileanu, S. Sodhani, P. Vincent, A. Zhang, P. Bacon, D. Precup, M. C. Machado, and P. D’Oro
  MaestroMotif: Skill Design from Artificial Intelligence Feedback.
  arXiv preprint arXiv:2412.08542.
- Kompella et al. (2017)
  V. R. Kompella, M. Stollenga, M. Luciw, and J. Schmidhuber
  Continual curiosity-driven skill acquisition from high-dimensional video inputs for humanoid robots.
  Artificial Intelligence 247, pp. 313–335.
- Lange et al. (2023)
  R. Lange, T. Schaul, Y. Chen, T. Zahavy, V. Dalibard, C. Lu, S. Singh, and S. Flennerhag
  Discovering evolution strategies via meta-black-box optimization.
  In Proceedings of the Companion Conference on Genetic and Evolutionary Computation,
  pp. 29–30.
- Lange et al. (2024)
  R. Lange, Y. Tian, and Y. Tang
  Large language models as evolution strategies.
  In Proceedings of the Genetic and Evolutionary Computation Conference Companion,
  pp. 579–582.
- Lee et al. (2020)
  J. Lee, J. Hwangbo, L. Wellhausen, V. Koltun, and M. Hutter
  Learning quadrupedal locomotion over challenging terrain.
  Science robotics 5 (47), pp. eabc5986.
- Lehman et al. (2023)
  J. Lehman, J. Gordon, S. Jain, K. Ndousse, C. Yeh, and K. O. Stanley
  Evolution through large models.
  In Handbook of Evolutionary Machine Learning,
  pp. 331–366.
- Lehman and Stanley (2011)
  J. Lehman and K. O. Stanley
  Novelty search and the problem with objectives.
  Genetic programming theory and practice IX, pp. 37–56.
- Lehman (2023)
  J. Lehman
  Machine love.
  arXiv preprint arXiv:2302.09248.
- Lewis et al. (2020)
  P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. Yih, T. Rocktäschel, et al.
  Retrieval-augmented generation for knowledge-intensive nlp tasks.
  Advances in neural information processing systems 33, pp. 9459–9474.
- Li et al. (2014)
  J. Li, S. J., and J. Clune
  Encouraging creative thinking in robots improves their ability to solve challenging problems.
  In Proceedings of the Genetic and Evolutionary Computation Conference,
  pp. 193–200.
- Li et al. (2024)
  Y. Li, J. Parsert, and E. Polgreen
  Guiding enumerative program synthesis with large language models.
  In International Conference on Computer Aided Verification,
  pp. 280–301.
- Liang et al. (2023)
  T. Liang, Z. He, W. Jiao, X. Wang, Y. Wang, R. Wang, Y. Yang, S. Shi, and Z. Tu
  Encouraging divergent thinking in large language models through multi-agent debate.
  arXiv preprint arXiv:2305.19118.
- Lightman et al. (2023)
  H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe
  Let’s verify step by step.
  In The Twelfth International Conference on Learning Representations,
- Lim et al. (2024)
  B. Lim, M. Flageat, and A. Cully
  Large language models as in-context ai generators for quality-diversity.
  In ALIFE 2024: Proceedings of the 2024 Artificial Life Conference,
- Linnainmaa (1970)
  S. Linnainmaa
  The representation of the cumulative rounding error of an algorithm as a taylor expansion of the local rounding errors.
  Ph.D. Thesis, Master’s Thesis (in Finnish), Univ. Helsinki.
- Liu et al. (2024)
  F. Liu, X. Tong, M. Yuan, X. Lin, F. Luo, Z. Wang, Z. Lu, and Q. Zhang
  Evolution of heuristics: towards efficient automatic algorithm design using large language model.
  arXiv preprint arXiv:2401.02051.
- Liu et al. (2023)
  L. Liu, X. Yang, Y. Shen, B. Hu, Z. Zhang, J. Gu, and G. Zhang
  Think-in-memory: Recalling and post-thinking enable llms with long-term memory.
  arXiv preprint arXiv:2311.08719.
- Lu et al. (2024a)
  C. Lu, C. Lu, R. T. Lange, J. Foerster, J. Clune, and D. Ha
  The ai scientist: Towards fully automated open-ended scientific discovery.
  arXiv preprint arXiv:2408.06292.
- Lu et al. (2023)
  C. Lu, S. Towers, and J. Foerster
  Arbitrary order meta-learning with simple population-based evolution.
  In Artificial Life Conference Proceedings 35,
  Vol. 2023, pp. 67.
- Lu et al. (2024b)
  C. Lu, S. Hu, and J. Clune
  Intelligent go-explore: standing on the shoulders of giant foundation models.
  arXiv preprint arXiv:2405.15143.
- Lu et al. (2025)
  C. Lu, S. Hu, and J. Clune
  Automated capability discovery via model self-exploration.
  arXiv preprint arXiv:2502.0757.
- Ma et al. (2023)
  Y. J. Ma, W. Liang, G. Wang, D. Huang, O. Bastani, D. Jayaraman, Y. Zhu, L. Fan, and A. Anandkumar
  Eureka: Human-level reward design via coding large language models.
  arXiv preprint arXiv:2310.12931.
- Madaan et al. (2023)
  A. Madaan, N. Tandon, P. Gupta, S. Hallinan, L. Gao, S. Wiegreffe, U. Alon, N. Dziri, S. Prabhumoye, Y. Yang, et al.
  Self-refine: Iterative refinement with self-feedback, 2023.
  URL https://arxiv. org/abs/2303.17651.
- Markoff (2016)
  J. Markoff
  Machines of loving grace: the quest for common ground between humans and robots.
   HarperCollins Publishers.
- Mayr (1982)
  E. Mayr
  The growth of biological thought: diversity, evolution, and inheritance.
   Harvard University Press.
- Metz et al. (2021)
  L. Metz, C. D. Freeman, N. Maheswaranathan, and J. Sohl-Dickstein
  Training learned optimizers with randomly initialized learned optimizers.
  arXiv preprint arXiv:2101.07367.
- Modarressi et al. (2023)
  A. Modarressi, A. Imani, M. Fayyaz, and H. Schütze
  Ret-llm: Towards a general read-write memory for large language models.
  arXiv preprint arXiv:2305.14322.
- Mouret and Clune (2015)
  J. Mouret and J. Clune
  Illuminating search spaces by mapping elites.
  arXiv preprint arXiv:1504.04909.
- Muennighoff et al. (2025)
  N. Muennighoff, Z. Yang, W. Shi, X. L. Li, L. Fei-Fei, H. Hajishirzi, L. Zettlemoyer, P. Liang, E. Candès, and T. Hashimoto
  S1: simple test-time scaling.
  arXiv preprint arXiv:2501.19393.
- Nasir et al. (2024)
  M. U. Nasir, S. James, and J. Togelius
  Word2world: Generating stories and worlds through large language models.
  arXiv preprint arXiv:2405.06686.
- Nasir and Togelius (2023)
  M. U. Nasir and J. Togelius
  Practical PCG through large language models.
  In 2023 IEEE Conference on Games (CoG),
  pp. 1–4.
- Nguyen et al. (2015)
  A. M. Nguyen, J. Yosinski, and J. Clune
  Innovation engines: automated creativity and improved stochastic optimization via deep learning.
  In Proceedings of the 2015 annual conference on genetic and evolutionary computation,
  pp. 959–966.
- Nie et al. (2025)
  F. Nie, L. Feng, H. Ye, W. Liang, P. Lu, H. Yao, A. Alahi, and J. Zou
  Weak-for-strong: training weak meta-agent to harness strong executors.
  arXiv preprint arXiv:2504.04785.
- Niu et al. (2025)
  B. Niu, Y. Song, K. Lian, Y. Shen, Y. Yao, K. Zhang, and T. Liu
  Flow: modularized agentic workflow automation.
  In The Thirteenth International Conference on Learning Representations,
- Novikov et al. (2025)
  A. Novikov, N. Vũ, M. Eisenberger, E. Dupont, P. Huang, A. Z. Wagner, S. Shirobokov, B. Kozlovskii, F. J. R. Ruiz, A. Mehrabian, M. P. Kumar, A. See, S. Chaudhuri, G. Holland, A. Davies, S. Nowozin, P. Kohli, and M. Balog
  AlphaEvolve: a coding agent for scientific and algorithmic discovery.
  Technical report
   Google DeepMind.
- OpenAI (2024)
  OpenAI
  Introducing swe-bench verified.
  Note: <https://openai.com/index/introducing-swe-bench-verified/>Accessed: 2025-04-16
- OpenAI (2025)
  OpenAI
  OpenAI o3-mini.
  Note: <https://openai.com/index/openai-o3-mini/>Accessed: 2025-05-01
- Oudeyer et al. (2007)
  P. Oudeyer, F. Kaplan, and V. V. Hafner
  Intrinsic motivation systems for autonomous mental development.
  IEEE transactions on evolutionary computation 11 (2), pp. 265–286.
- Ouyang et al. (2022)
  L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, et al.
  Training language models to follow instructions with human feedback.
  Advances in neural information processing systems 35, pp. 27730–27744.
- Parikh et al. (2016)
  A. Parikh, O. Täckström, D. Das, and J. Uszkoreit
  A Decomposable Attention Model for Natural Language Inference.
  In Proceedings of the 2016 Conference on Empirical Methods in Natural Language Processing,
  pp. 2249–2255.
- Parker-Holder et al. (2024)
  J. Parker-Holder, P. Ball, J. Bruce, V. Dasagi, K. Holsheimer, C. Kaplanis, A. Moufarek, G. Scully, J. Shar, J. Shi, S. Spencer, J. Yung, M. Dennis, S. Kenjeyev, S. Long, V. Mnih, H. Chan, M. Gazeau, B. Li, F. Pardo, L. Wang, L. Zhang, F. Besse, T. Harley, A. Mitenkova, J. Wang, J. Clune, D. Hassabis, R. Hadsell, A. Bolton, S. Singh, and T. Rocktäschel
  Genie 2: a large-scale foundation world model.
  External Links: [Link](https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/)
- Pathak et al. (2017)
  D. Pathak, P. Agrawal, A. A. Efros, and T. Darrell
  Curiosity-driven exploration by self-supervised prediction.
  In International conference on machine learning,
  pp. 2778–2787.
- Paul Gauthier (2024)
  Paul Gauthier
  O1 tops aider’s new polyglot leaderboard.
  Note: <https://aider.chat/2024/12/21/polyglot.html>Accessed: 2025-04-16
- Polozov and Gulwani (2015)
  O. Polozov and S. Gulwani
  Flashmeta: a framework for inductive program synthesis.
  In Proceedings of the 2015 ACM SIGPLAN International Conference on Object-Oriented Programming, Systems, Languages, and Applications,
  pp. 107–126.
- Pugh et al. (2016)
  J. K. Pugh, L. B. Soros, and K. O. Stanley
  Quality diversity: A new frontier for evolutionary computation.
  Frontiers in Robotics and AI 3, pp. 40.
- Radford et al. (2019)
  A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, I. Sutskever, et al.
  Language models are unsupervised multitask learners.
  OpenAI blog 1 (8), pp. 9.
- Robeyns et al. (2025)
  M. Robeyns, M. Szummer, and L. Aitchison
  A Self-Improving Coding Agent.
  arXiv preprint arXiv:2504.15228.
- Romera-Paredes et al. (2024)
  B. Romera-Paredes, M. Barekatain, A. Novikov, M. Balog, M. P. Kumar, E. Dupont, F. J. Ruiz, J. S. Ellenberg, P. Wang, O. Fawzi, et al.
  Mathematical discoveries from program search with large language models.
  Nature 625 (7995), pp. 468–475.
- Rosser and Foerster (2025)
  J. Rosser and J. N. Foerster
  AgentBreeder: mitigating the AI safety impact of multi-agent scaffolds via self-improvement.
  In Scaling Self-Improving Foundation Models without Human Supervision,
  External Links: [Link](https://openreview.net/forum?id=j0n3BJJTcT)
- Rumelhart et al. (1985)
  D. E. Rumelhart, G. E. Hinton, R. J. Williams, et al.
  Learning internal representations by error propagation.
   Institute for Cognitive Science, University of California, San Diego.
- Samvelyan et al. (2024)
  M. Samvelyan, S. C. Raparthy, A. Lupu, E. Hambro, A. Markosyan, M. Bhatt, Y. Mao, M. Jiang, J. Parker-Holder, J. Foerster, et al.
  Rainbow teaming: Open-ended generation of diverse adversarial prompts.
  Advances in Neural Information Processing Systems 37, pp. 69747–69786.
- Sancaktar et al. (2025)
  C. Sancaktar, C. Gumbsch, A. Zadaianchuk, P. Kolev, and G. Martius
  SENSEI: Semantic Exploration Guided by Foundation Models to Learn Versatile World Models.
  arXiv preprint arXiv:2503.01584.
- Schaul et al. (2015)
  T. Schaul, D. Horgan, K. Gregor, and D. Silver
  Universal value function approximators.
  In International conference on machine learning,
  pp. 1312–1320.
- Schick et al. (2023)
  T. Schick, J. Dwivedi-Yu, R. Dessì, R. Raileanu, M. Lomeli, E. Hambro, L. Zettlemoyer, N. Cancedda, and T. Scialom
  Toolformer: Language models can teach themselves to use tools.
  Advances in Neural Information Processing Systems 36, pp. 68539–68551.
- Schmidhuber and Huber (1990)
  J. Schmidhuber and R. Huber
  Learning to generate focus trajectories for attentive vision.
   Institut für Informatik.
- Schmidhuber (1987)
  J. Schmidhuber
  Evolutionary principles in self-referential learning, or on learning how to learn: the meta-meta-… hook.
  Ph.D. Thesis, Technische Universität München.
- Schmidhuber (1993)
  J. Schmidhuber
  A ‘self-referential’weight matrix.
  In International conference on artificial neural networks,
  pp. 446–450.
- Schmidhuber (2007)
  J. Schmidhuber
  Gödel machines: fully self-referential optimal universal self-improvers.
  In Artificial general intelligence,
  pp. 199–226.
- Schmidhuber (2008)
  J. Schmidhuber
  Driven by compression progress: a simple principle explains essential aspects of subjective beauty, novelty, surprise, interestingness, attention, curiosity, creativity, art, science, music, jokes.
  In Workshop on anticipatory behavior in adaptive learning systems,
  pp. 48–76.
- Schmidhuber (2013)
  J. Schmidhuber
  Powerplay: training an increasingly general problem solver by continually searching for the simplest still unsolvable problem.
  Frontiers in psychology 4, pp. 313.
- Schulhoff et al. (2024)
  S. Schulhoff, M. Ilie, N. Balepur, K. Kahadze, A. Liu, C. Si, Y. Li, A. Gupta, H. Han, S. Schulhoff, et al.
  The prompt report: a systematic survey of prompting techniques.
  arXiv preprint arXiv:2406.06608.
- Sheth et al. (2025)
  I. Sheth, J. Wehner, S. Abdelnabi, R. Binkyte, and M. Fritz
  Safety is Essential for Responsible Open-Ended Systems.
  arXiv preprint arXiv:2502.04512.
- Shi et al. (2023)
  K. Shi, H. Dai, W. Li, K. Ellis, and C. Sutton
  Lambdabeam: neural program search with higher-order functions and lambdas.
  Advances in Neural Information Processing Systems 36, pp. 51327–51346.
- Shinn et al. (2023)
  N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao
  Reflexion: Language agents with verbal reinforcement learning.
  Advances in Neural Information Processing Systems 36, pp. 8634–8652.
- Silver et al. (2016)
  D. Silver, A. Huang, C. J. Maddison, A. Guez, L. Sifre, G. Van Den Driessche, J. Schrittwieser, I. Antonoglou, V. Panneershelvam, M. Lanctot, et al.
  Mastering the game of go with deep neural networks and tree search.
  nature 529 (7587), pp. 484–489.
- Silver et al. (2017)
  D. Silver, T. Hubert, J. Schrittwieser, I. Antonoglou, M. Lai, A. Guez, M. Lanctot, L. Sifre, D. Kumaran, T. Graepel, et al.
  Mastering chess and shogi by self-play with a general reinforcement learning algorithm.
  arXiv preprint arXiv:1712.01815.
- Singh et al. (2023)
  A. Singh, J. D. Co-Reyes, R. Agarwal, A. Anand, P. Patil, X. Garcia, P. J. Liu, J. Harrison, J. Lee, K. Xu, et al.
  Beyond human data: scaling self-training for problem-solving with language models.
  arXiv preprint arXiv:2312.06585.
- Skalse et al. (2022)
  J. Skalse, N. Howe, D. Krasheninnikov, and D. Krueger
  Defining and characterizing reward gaming.
  Advances in Neural Information Processing Systems 35, pp. 9460–9471.
- Stanley et al. (2017)
  K. O. Stanley, J. Lehman, and L. Soros
  Open-endedness: The last grand challenge you’ve never heard of.
  While open-endedness could be a force for discovering intelligence, it could also be a component of AI itself.
- Stanley and Lehman (2015)
  K. O. Stanley and J. Lehman
  Why greatness cannot be planned: The myth of the objective.
   Springer.
- Strathern (1997)
  M. Strathern
  ‘Improving ratings’: audit in the British University system.
  European review 5 (3), pp. 305–321.
- Su et al. (2025)
  J. Su, Y. Xia, R. Shi, J. Wang, J. Huang, Y. Wang, T. Shi, Y. Jingsong, and L. He
  DebFlow: automating agent creation via agent debate.
  arXiv preprint arXiv:2503.23781.
- Sudhakaran et al. (2023)
  S. Sudhakaran, M. González-Duque, M. Freiberger, C. Glanois, E. Najarro, and S. Risi
  Mariogpt: Open-ended text2level generation through large language models.
  Advances in Neural Information Processing Systems 36, pp. 54213–54227.
- Team et al. (2024)
  O. Team, A. Jaech, A. Kalai, A. Lerer, A. Richardson, A. El-Kishky, A. Low, A. Helyar, A. Madry, A. Beutel, A. Carney, et al.
  Openai o1 system card.
  arXiv preprint arXiv:2412.16720.
- Vaswani et al. (2017)
  A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin
  Attention is all you need.
  Advances in neural information processing systems 30.
- Wang et al. (2023a)
  G. Wang, Y. Xie, Y. Jiang, A. Mandlekar, C. Xiao, Y. Zhu, L. Fan, and A. Anandkumar
  Voyager: An open-ended embodied agent with large language models.
  arXiv preprint arXiv:2305.16291.
- Wang et al. (2023b)
  R. Wang, K. Xue, Y. Wang, P. Yang, H. Fu, Q. Fu, and C. Qian
  Diversity from human feedback.
  arXiv preprint arXiv:2310.06648.
- Wang et al. (2019)
  R. Wang, J. Lehman, J. Clune, and K. O. Stanley
  Paired open-ended trailblazer (poet): Endlessly generating increasingly complex and diverse learning environments and their solutions.
  arXiv preprint arXiv:1901.01753.
- Wang et al. (2024)
  X. Wang, B. Li, Y. Song, F. F. Xu, X. Tang, M. Zhuge, J. Pan, Y. Song, B. Li, J. Singh, et al.
  Openhands: An open platform for ai software developers as generalist agents.
  In The Thirteenth International Conference on Learning Representations,
- Wang et al. (2023c)
  Y. Wang, Z. Xian, F. Chen, T. Wang, Y. Wang, K. Fragkiadaki, Z. Erickson, D. Held, and C. Gan
  Robogen: towards unleashing infinite data for automated robot learning via generative simulation.
  arXiv preprint arXiv:2311.01455.
- Wei et al. (2022)
  J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou, et al.
  Chain-of-thought prompting elicits reasoning in large language models.
  Advances in neural information processing systems 35, pp. 24824–24837.
- Wiering and Schmidhuber (1997)
  M. Wiering and J. Schmidhuber
  HQ-learning.
  Adaptive behavior 6 (2), pp. 219–246.
- Wright (1932)
  S. Wright
  The roles of mutation, inbreeding, crossbreeding and selection in evolution, proceedings of the sixth international congress of genetics. proc sixth int congr genet [internet].
  New York356366.
- Xia et al. (2024)
  C. S. Xia, Y. Deng, S. Dunn, and L. Zhang
  Agentless: demystifying llm-based software engineering agents.
  arXiv preprint arXiv:2407.01489.
- Yang et al. (2024)
  J. Yang, C. E. Jimenez, A. Wettig, K. Lieret, S. Yao, K. R. Narasimhan, and O. Press
  SWE-agent: agent-computer interfaces enable automated software engineering.
  In The Thirty-eighth Annual Conference on Neural Information Processing Systems,
  External Links: [Link](https://arxiv.org/abs/2405.15793)
- Yao et al. (2023)
  S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and Y. Cao
  React: Synergizing reasoning and acting in language models.
  In International Conference on Learning Representations (ICLR),
- Ye et al. (2025)
  R. Ye, S. Tang, R. Ge, Y. Du, Z. Yin, S. Chen, and J. Shao
  Mas-gpt: training llms to build llm-based multi-agent systems.
  arXiv preprint arXiv:2503.03686.
- Yin et al. (2024)
  X. Yin, X. Wang, L. Pan, X. Wan, and W. Y. Wang
  Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement.
  arXiv preprint arXiv:2410.04444.
- Yuan et al. (2024)
  S. Yuan, K. Song, J. Chen, X. Tan, D. Li, and D. Yang
  EvoAgent: towards automatic multi-agent generation via evolutionary algorithms.
  arXiv preprint arXiv:2406.14228.
- Yudkowsky et al. (2008)
  E. Yudkowsky et al.
  Artificial Intelligence as a positive and negative factor in global risk.
  Global catastrophic risks 1 (303), pp. 184.
- Yuksekgonul et al. (2024)
  M. Yuksekgonul, F. Bianchi, J. Boen, S. Liu, Z. Huang, C. Guestrin, and J. Zou
  Textgrad: automatic" differentiation" via text.
  arXiv preprint arXiv:2406.07496.
- Zelikman et al. (2024a)
  E. Zelikman, G. Harik, Y. Shao, V. Jayasiri, N. Haber, and N. D. Goodman
  Quiet-star: language models can teach themselves to think before speaking.
  arXiv preprint arXiv:2403.09629.
- Zelikman et al. (2024b)
  E. Zelikman, E. Lorch, L. Mackey, and A. T. Kalai
  Self-taught optimizer (stop): Recursively self-improving code generation.
  In First Conference on Language Modeling,
- Zhang et al. (2024a)
  D. Zhang, S. Zhoubian, Z. Hu, Y. Yue, Y. Dong, and J. Tang
  Rest-mcts*: llm self-training via process reward guided tree search.
  Advances in Neural Information Processing Systems 37, pp. 64735–64772.
- Zhang et al. (2025a)
  G. Zhang, L. Niu, J. Fang, K. Wang, L. Bai, and X. Wang
  Multi-agent architecture search via agentic supernet.
  arXiv preprint arXiv:2502.04180.
- Zhang et al. (2024b)
  J. Zhang, J. Lehman, K. Stanley, and J. Clune
  OMNI: Open-endedness via Models of human Notions of Interestingness.
  In The Twelfth International Conference on Learning Representations,
  External Links: [Link](https://openreview.net/forum?id=AgM3MzT99c)
- Zhang et al. (2024c)
  J. Zhang, J. Xiang, Z. Yu, F. Teng, X. Chen, J. Chen, M. Zhuge, X. Cheng, S. Hong, J. Wang, et al.
  Aflow: Automating agentic workflow generation.
  arXiv preprint arXiv:2410.10762.
- Zhang et al. (2025b)
  Y. Zhang, Y. Hou, B. Tang, S. Chen, M. Zhang, X. Dong, and S. Chen
  GNNs as predictors of agentic workflow performances.
  arXiv preprint arXiv:2503.11301.
- Zhang et al. (2024d)
  Y. Zhang, H. Ruan, Z. Fan, and A. Roychoudhury
  Autocoderover: autonomous program improvement.
  In Proceedings of the 33rd ACM SIGSOFT International Symposium on Software Testing and Analysis,
  pp. 1592–1604.
- Zhong et al. (2024)
  W. Zhong, L. Guo, Q. Gao, H. Ye, and Y. Wang
  Memorybank: Enhancing large language models with long-term memory.
  In Proceedings of the AAAI Conference on Artificial Intelligence,
  Vol. 38, pp. 19724–19731.
- Zhou et al. (2025)
  A. Zhou, K. Wu, F. Pinto, Z. Chen, Y. Zeng, Y. Yang, S. Yang, S. Koyejo, J. Zou, and B. Li
  AutoRedTeamer: Autonomous Red Teaming with Lifelong Attack Integration.
  arXiv preprint arXiv:2503.15754.
- Zhou et al. (2024)
  W. Zhou, Y. Ou, S. Ding, L. Li, J. Wu, T. Wang, J. Chen, S. Wang, X. Xu, N. Zhang, et al.
  Symbolic learning enables self-evolving agents.
  arXiv preprint arXiv:2406.18532.
- Zhu et al. (2024)
  Y. Zhu, J. Li, G. Li, Y. Zhao, Z. Jin, and H. Mei
  Hot or cold? adaptive temperature sampling for code generation with large language models.
  In Proceedings of the AAAI Conference on Artificial Intelligence,
  Vol. 38, pp. 437–445.
- Zhuge et al. (2023)
  M. Zhuge, H. Liu, F. Faccio, D. R. Ashley, R. Csordás, A. Gopalakrishnan, A. Hamdi, H. A. A. K. Hammoud, V. Herrmann, K. Irie, L. Kirsch, B. Li, G. Li, S. Liu, J. Mai, P. Piékos, A. Ramesh, I. Schlag, W. Shi, A. Stanic, W. Wang, Y. Wang, M. Xu, D. Fan, B. Ghanem, and J. Schmidhuber
  Mindstorms in natural language-based societies of mind.
  arXiv preprint arXiv:2305.17066.
- Zhuge et al. (2024)
  M. Zhuge, W. Wang, L. Kirsch, F. Faccio, D. Khizbullin, and J. Schmidhuber
  GPTSwarm: language agents as optimizable graphs.
  In Forty-first International Conference on Machine Learning,

## 附录

## 附录 A 补充结果

### A.1 SWE-bench 上的基线

![Refer to caption](2505.22954v3/dgm_wo_selfimprove.png)

图 5：不含自我改进智能体的 DGM。在保持负责修改并产生下一代编码智能体的元智能体不变的情况下，DGM w/o self-improve 无法随时间持续改进。（左）DGM w/o self-improve 在 SWE-bench 上运行期间生成的编码智能体档案库。每个节点代表一个编码智能体，节点 0 对应基础智能体。节点颜色表示在 SWE-bench 上的性能（求解任务的百分比），边框颜色反映该智能体被评估的任务数。边表示哪些智能体自我修改产生了后代。（右）DGM w/o self-improve 在 SWE-bench 上的进展图。浅绿线表示所有具备基本代码库编辑功能的智能体的平均分。绿线追踪每次迭代时档案库中任意智能体取得的最佳分数。深色线显示最终最佳发现智能体及其前驱节点的谱系。

![Refer to caption](2505.22954v3/dgm_wo_openended.png)

图 6：不含开放式探索的 DGM。去掉档案库后，DGM w/o open-ended exploration 总是使用最新的智能体进行自我修改，在 SWE-bench 上进展甚微。（左）DGM w/o open-ended exploration 在 SWE-bench 上运行期间生成的编码智能体档案库。每个节点代表一个编码智能体，节点 0 对应基础智能体。节点颜色表示在 SWE-bench 上的性能（求解任务的百分比），边框颜色反映该智能体被评估的任务数。边表示哪些智能体自我修改产生了后代。（右）DGM w/o open-ended 在 SWE-bench 上的进展图。橙线表示所有具备基本代码库编辑功能的智能体的平均分。浅橙线追踪每次迭代时档案库中任意智能体取得的最佳分数。深色线显示最终最佳发现智能体及其前驱节点的谱系。

### A.2 Polyglot 上跨模型的普适性

图 7：Polyglot 上的模型间迁移。

除在 SWE-bench 上测试迁移模型（见第 4.4 节、图 2）外，本节还给出 Polyglot 上的迁移结果。在 Polyglot（图 7）上——DGM 使用 o3-mini 运行——我们把 FM 替换为 Claude 3.5 Sonnet (New) 或 Claude 3.7 Sonnet，并在全量基准测试上评估（图 4，中）。用 Claude 3.5 Sonnet (New) 时，初始智能体取得 32.0%，DGM 发现的智能体取得 33.3%。用 Claude 3.7 Sonnet 时，初始智能体取得 35.6%，DGM 发现的智能体取得 36.8%。这些结果表明，DGM 带来的改进可跨 FM 泛化，而不是与其运行时使用的特定 FM 紧耦合（图 4）。

### A.3 父代选择的消融

为进一步研究 DGM 中父代选择机制的影响，我们引入 DGM Greedy。DGM Greedy 总是选择表现最佳的节点作为分叉的父代，而不是像本实现中的 DGM 那样，让每个节点都有非零概率被分叉（该概率大致与其性能分数和子代数量成正比）（第 C.2 节）。该消融在此设置下复刻了 Robeyns et al.（2025）的方法。如表 1 所示，DGM Greedy 在 SWE-bench 与 Polyglot 上分别取得 39.7% 与 30.0%，而本实现的 DGM 取得 50.0% 与 38.0%。这些结果表明，允许档案库中的所有解充当潜在垫脚石，能随时间带来更大的改进，凸显了开放式探索的重要性。

表 1：DGM、其消融变体与基线在 SWE-bench 和 Polyglot 基准测试上的比较。

| 方法 | SWE-bench | Polyglot |
| --- | --- | --- |
| DGM | 50.0% | 38.0% |
| DGM w/o Open-ended exploration | 23.0% | 14.0% |
| DGM w/o Self-improve | 39.0% | 28.0% |
| DGM Greedy | 39.7% | 30.0% |

### A.4 DGM 运行的额外统计

**具备基本代码编辑功能的生成智能体比例。** 为更深入地理解 DGM 的过程，我们分析在 SWE-bench 基准测试上生成的智能体中具备基本代码编辑功能的比例。如表 2 所示，DGM 产生具备基本代码库编辑功能的智能体的比例最高。这些结果凸显了 DGM 中开放式探索与自我改进两个组件的有效性：开放式探索使搜索能够跳出局部最优，而自我改进提升了生成更优智能体的能力。

表 2：SWE-bench 上具备基本代码编辑功能的生成智能体比例。

| 方法 | 具备基本代码编辑功能的比例 |
| --- | --- |
| DGM | 51.3% |
| DGM w/o Open-ended exploration | 32.5% |
| DGM w/o Self-improve | 32.5% |

**DGM 运行的稳定性。** 为评估 DGM 的稳定性，我们在 Polyglot 基准测试上把 DGM 算法运行三次，并分析性能的方差。DGM 取得 40.7% 的平均准确率与 2.3% 的标准差，表明 DGM 能在各次运行间取得一致且可复现的结果。

## 附录 B 补充相关工作

**开放式进化（续）。** 早期的开放式进化方法探索了在可学习性与有趣性之间取得平衡的不同机制。质量-多样性算法力求以多样且高性能的行为照亮广阔的解空间（Pugh et al., 2016；Chatzilygeroudis et al., 2021；Mouret and Clune, 2015；Nguyen et al., 2015）。其他方法强调目标导向探索（Ecoffet et al., 2019；Ecoffet et al., 2021；Schaul et al., 2015；Andrychowicz et al., 2017；Eysenbach et al., 2018）、内在动机（Lehman and Stanley, 2011；Oudeyer et al., 2007；Li et al., 2014；Pathak et al., 2017）或学习进展框架（Kanitscheider et al., 2021；Gaven et al., 2025；Baranes and Oudeyer, 2013；Colas et al., 2019；Colas et al., 2022b；Jiang et al., 2021；Dennis et al., 2020；Schmidhuber, 2008；Schmidhuber, 2013；Kompella et al., 2017）。近来，大规模基础模型（FM）（Brown et al., 2020；Radford et al., 2019）已成为人类「有趣性」概念的有力代理（Zhang et al., 2024b；Faldor et al., 2025；Sancaktar et al., 2025），也是在代码中提出新颖解的有效突变算子（Romera-Paredes et al., 2024；Novikov et al., 2025；Lehman et al., 2023；Faldor et al., 2025；Hu et al., 2025）。FM 可以引导自目的智能体（autotelic agents）（Colas et al., 2022b；Colas et al., 2023；Colas et al., 2022a），建模人类对质量与多样性的偏好（Bradley et al., 2024；Ding et al., 2024；Wang et al., 2023b；Klissarov et al., 2023；Klissarov et al., 2024；Samvelyan et al., 2024；Lim et al., 2024；Havrilla et al., 2024a），设计奖励函数（Wiering and Schmidhuber, 1997；Wang et al., 2023a；Ma et al., 2023；Faldor et al., 2025），创建模拟环境（Sudhakaran et al., 2023；Nasir and Togelius, 2023；Aki et al., 2024；Nasir et al., 2024；Bruce et al., 2024；Parker-Holder et al., 2024；Schmidhuber, 2013），驱动持续演化的多智能体动态（Dharna et al., 2024；Zhou et al., 2025），搜索多样的行走机器人形态（Lehman et al., 2023），以及为基准测试或目标优化搜索广阔的解空间（Lange et al., 2024；Zhang et al., 2024b；Faldor et al., 2025；Hu et al., 2025；Lu et al., 2024b；Romera-Paredes et al., 2024；Fernando et al., 2024；Lu et al., 2024a；Khan et al., 2024；Lu et al., 2025；Liu et al., 2024；Novikov et al., 2025）。

**程序合成。** 程序合成（Alur et al., 2018；Polozov and Gulwani, 2015；Buchi and Landweber, 1990；Gulwani, 2011；Ellis et al., 2021）旨在生成满足外部规约（如输入-输出示例或逻辑公式）的代码。混合方法将符号方法与神经或 FM 引导相结合：例如，Li et al.（2024）在 SyGuS 设置中使用 LLM 建议来引导符号搜索，优于纯枚举。Barke et al.（2024）将 LLM 补全与一个学习得到的代理模型相融合，以引导 DSL 中的合成。Shi et al.（2023）在搜索过程中使用神经策略构建高阶抽象与 lambda 抽象，在列表操作任务上同时优于纯 LLM 方法与符号基线。DGM 的不同之处在于：它不仅关注为外部任务生成程序，还关注智能体的自我修改——重写自己的实现，以提升未来自我改进的能力。

**来自达尔文进化的启发。** 本工作深受达尔文进化机制（Darwin, 2023）的启发，尤其是变异（突变）、选择与谱系（垫脚石）的保留，并将这些机制带入自我修改编码智能体的领域。在 DGM 中，系统维护一个由过往智能体版本构成的档案库，并从中采样父代智能体；随后突变（即代码编辑）产生新的子代智能体，并在编码基准测试上对它们进行实证评估；成功的智能体被加入档案库，从而支持对多条进化轨迹的并行探索（第 3 节）。这呼应了生物进化（Edwards, 2000；Wright, 1932）保留遗传多样性（Mayr, 1982）、利用变异（Kimura, 1979）并以自然选择保留有益突变（Dobzhansky, 1970）的方式。

## 附录 C 算法细节

### C.1 初始编码智能体

本节给出初始编码智能体（第 4.1 节）可用工具的细节及其任务提示词。

所给 Bash 工具的信息：

```python
def tool_info():
    return {
        "name": "bash",
        "description": """Run commands in a bash shell\n
* When invoking this tool, the contents of the "command" parameter does NOT need to be XML-escaped.\n
* You don't have access to the internet via this tool.\n
* You do have access to a mirror of common linux and python packages via apt and pip.\n
* State is persistent across command calls and discussions with the user.\n
* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.\n
* Please avoid commands that may produce a very large amount of output.\n
* Please run long lived commands in the background, e.g. 'sleep 10 &' or start a server in the background.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The bash command to run."
                }
            },
            "required": ["command"]
        }
    }
```

所给 Edit 工具的信息：

```python
def tool_info():
    return {
        "name": "editor",
        "description": """Custom editing tool for viewing, creating, and editing files\n
* State is persistent across command calls and discussions with the user.\n
* If `path` is a file, `view` displays the entire file with line numbers. If `path` is a directory, `view` lists non-hidden files and directories up to 2 levels deep.\n
* The `create` command cannot be used if the specified `path` already exists as a file.\n
* If a `command` generates a long output, it will be truncated and marked with `<response clipped>`.\n
* The `edit` command overwrites the entire file with the provided `file_text`.\n
* No partial/line-range edits or partial viewing are supported.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "enum": ["view", "create", "edit"],
                    "description": "The command to run: `view`, `create`, or `edit`."
                },
                "path": {
                    "description": "Absolute path to file or directory, e.g. `/repo/file.py` or `/repo`.",
                    "type": "string"
                },
                "file_text": {
                    "description": "Required parameter of `create` or `edit` command, containing the content for the entire file.",
                    "type": "string"
                }
            },
            "required": ["command", "path"]
        }
    }
```

任务提示词：

```text
I have uploaded a Python code repository in the directory {self.git_tempdir}. Help solve the following problem.

<problem_description>
{self.problem_statement}
</problem_description>

<test_description>
{self.test_description}
</test_description>

Your task is to make changes to the files in the {self.git_tempdir} directory to address the <problem_description>. I have already taken care of the required dependencies.
```

### C.2 父代选择

在 DGM 的每次迭代中，我们从档案库中选出一个智能体子集作为父代，让它们自我修改并产生新的子代智能体（第 3 节）。父代选择过程的细节受 Ecoffet et al.（2019）启发，概述如下。未来工作可以探索其他的搜索与探索方法（Coulom, 2006；Silver et al., 2016；Herr et al., 2025）。

在 DGM 运行的每次迭代 $t$，令

$$\mathcal{A}^{t}=\{a_{1}^{t},a_{2}^{t},\dots,a_{N}^{t}\}$$

为候选智能体档案库。我们首先定义合格集（eligible set）

$$\mathcal{E}^{t}=\bigl\{\,a_{i}^{t}\in\mathcal{A}^{t}:\alpha_{i}<1\bigr\},$$

即只包含性能分数尚未达到完美的那些智能体。然后，我们按性能与具备代码库编辑功能的子代数量的综合度量，从 $\mathcal{E}^{t}$ 中（有放回地）采样 $k$ 个父代。具体地，对每个智能体 $a_{i}^{t}\in\mathcal{E}^{t}$：

- （性能，式 1）$\alpha_{i}=\mathrm{performance}(a_{i}^{t})$，
- （子代数量，式 2）$n_{i}=\mathrm{functioning\_children\_count}(a_{i}^{t})$，
- （sigmoid 缩放的性能，式 3）$s_{i}=\dfrac{1}{1+\exp\!\bigl(-\lambda\,(\alpha_{i}-\alpha_{0})\bigr)}$，
- （新颖性加成，式 4）$h_{i}=\dfrac{1}{1+n_{i}}$，
- （未归一化权重，式 5）$w_{i}=s_{i}\,h_{i}$，
- （选择概率，式 6）$p_{i}=\dfrac{w_{i}}{\sum_{j=1}^{N}w_{j}}$，
- （采样，式 7）$\{\text{parents}\}\sim\mathrm{Categorical}\bigl(\{p_{i}\}_{a_{i}^{t}\in\mathcal{E}^{t}}\bigr)$（抽取 $k$ 个样本）。

其中 $\lambda>0$ 控制 sigmoid 的陡峭程度，$\alpha_{0}$ 是中点准确率。我们设 $\lambda=10$、$\alpha_{0}=0.5$。$k$ 决定 DGM 运行的每次迭代中并行进行多少次自我改进。我们在 SWE-bench 实验中设 $k=2$，在 Polyglot 实验中设 $k=4$。

### C.3 自我改进提示词

在每次迭代中，都会选出一个智能体进行自我修改。在这一步，当前的 DGM 实现利用一个单独的 FM 来诊断改进机会，再把它们交给编码智能体实现。为识别下一个潜在的改进，所选智能体在编码基准测试上表现的评估日志会被输入该 FM。虽然当前实现依赖一个额外的诊断步骤，但没有任何根本性限制阻止 DGM 自主分析自身表现、生成改进假设并实现后续修改。我们为此选择使用 OpenAI 的 o1 模型（Team et al., 2024），因为在我们的实验当时，它比其他可用的 FM 具备更好的推理能力。用于这一诊断的提示词如下所示。从诊断输出中提取 implementation_suggestion 与 problem_description，并作为自我修改任务传给编码智能体。

SWE-bench 实验的自我改进诊断提示词：

````text
Self-Improve Prompt

# Coding Agent Summary

- **Main File**: `coding_agent.py`
  - Primary Class: `AgenticSystem`
  - The `forward()` function is the central entry point.
  - Prompts are located either within the `forward()` function or in the `prompts/` directory.
- **Tools**: `tools/`
  - The `tools/` directory contains various tools that LLMs can use to perform specific tasks.
  - Each tool must have a `tool_info()` function that returns a JSON object containing 'name', 'description', and 'input_schema'. The 'input_schema' should be a JSON object containing 'type', 'properties', and 'required'.
  - Each tool must have a `tool_function()` function that takes the arguments defined in input_schema, performs the tool's task, and returns a string.
  - See other tools for reference.
- **Utilities**: `utils/`
  - The `utils/` directory contains utility functions used across the codebase.
- **Additional Details**:
  - The agent is very good at automatically utilizing the right available tools at the right time. So do not have an agentic flow that explicitly forces a tool's usage.
  - Common tools, such as file editing and bash commands, are easy for the agent to recognize and use appropriately. However, more complex and niche tools may require explicit instructions in the prompt.
  - Tools should be designed to be as general as possible, ensuring they work across any GitHub repository. Avoid hardcoding repository-specific details or behaviors (e.g., paths).
  - Do not use 'while True' loops in the agent's code. This can cause the agent to get stuck and not respond.
  - Verify the implementation details of helper functions prior to usage to ensure proper integration and expected behavior.
  - Do not install additional packages or dependencies directly. Update `requirements.txt` if new dependencies are required and install them using `pip install -r requirements.txt`.

Here is the implementation of the coding agent.

# Coding Agent Implementation

----- Coding Agent Implementation Start -----

{code}

----- Coding Agent Implementation End -----

Your task is to identify ONE detailed plan that would improve the agent's coding ability. The improvement should not be specific to any particular GitHub issue or repository.

Here is the log for the coding agent trying to solve the GitHub issues but failed.

# Agent Running Log

----- Agent Running Log Start -----

{md_log}

----- Agent Running Log End -----

# GitHub Issue

The GitHub issue that the agent is trying to solve.

----- GitHub Issue Start -----

{github_issue}

----- GitHub Issue End -----

# Predicted Patch

The agent's predicted patch to solve the issue.

----- Predicted Patch Start -----

{predicted_patch}

----- Predicted Patch End -----

# Private Test Patch

SWE-bench's official private tests to detect whether the issue is solved. This is not available to the agent during evaluation. The agent should try to implement its own tests.

----- Private Test Patch Start -----

{test_patch}

----- Private Test Patch End -----

# Issue Test Results

The test results from SWE-bench using the above official private tests.

----- Issue Test Results Start -----

{eval_log}

----- Issue Test Results End -----

Respond precisely in the following format including the JSON start and end markers:

```json
<JSON>
```

In <JSON>, provide a JSON response with the following fields:

- "log_summarization": Analyze the above logs and summarize how the agent tried to solve the GitHub issue. Note which tools and how they are used, the agent's problem-solving approach, and any issues encountered.
- "potential_improvements": Identify potential improvements to the coding agent that could enhance its coding capabilities. Focus on the agent's general coding abilities (e.g., better or new tools usable across any repository) rather than issue-specific fixes (e.g., tools only usable in one framework). All necessary dependencies and environment setup have already been handled, so do not focus on these aspects.
- "improvement_proposal": Choose ONE high-impact improvement from the identified potential improvements and describe it in detail. This should be a focused and comprehensive plan to enhance the agent's overall coding ability.
- "implementation_suggestion": Referring to the coding agent's summary and implementation, think critically about what feature or tool could be added or improved to best implement the proposed improvement. If the proposed feature can be implemented by modifying the existing tools, describe the modifications needed, instead of suggesting a new tool.
- "problem_description": Phrase the improvement proposal and implementation suggestion as a GitHub issue description. It should clearly describe the feature so that a software engineer viewing the issue and the repository can implement it.

Your response will be automatically parsed, so ensure that the string response is precisely in the correct format. Do NOT include the `<JSON>` tag in your output.
````

虽然诊断提示词中包含了私有测试补丁，但可以想见，智能体在该任务上拿高分的一条捷径是把答案硬编码。然而，通过人工检查日志与智能体修改，我们没有观察到任何表明记忆或对特定私有测试用例过拟合的问题逻辑或行为。此外，在一个任务或一个 LLM 模型上发现的改进往往能很好地泛化到其他任务与模型（图 4），说明这些改进并非任务特定，而是反映了提升整体性能的通用改动。

Polyglot 实验的附加提示词：

```text
Additional Prompt for o3-mini Tool Use and Polyglot

### DOC: tool function schema

Carefully consider whether to add/enhance the current tool or edit the workflow in forward()

Pay special attention to making sure that "required" and "type" are always at the correct level of nesting. For example, "required" should be at the same level as "properties", not inside it.

Make sure that every property, no matter how short, has a type and description correctly nested inside it.

Other arguments than you have seen are not permitted. For example, in "edit_line_ranges" with "type": "array", arguments like "minItems" and "maxItems" are not permitted.

...

Here is the log for the coding agent trying to solve a programming task.

A task is in one programming language, but the coding agent needs to deal with different languages including C++, Go, Java, JavaScript, Python, and Rust.
```

### C.4 伪代码

以下是 DGM 算法的伪代码，在第 3 节中描述：

算法 1 Darwin Gödel Machine

```text
Input: Initial coding agent g_0, benchmark suite B, maximum iterations T
Output: Archive of agents A

s_0 ← evaluate(g_0, B)                    // Evaluate the base agent
initialize A ← {(g_0, s_0)}               // Start with the base agent
for t ← 1 to T do
    P ← SelectParents(A)                  // Select parent agents
    foreach p ∈ P do
        c ← p.modify(p)                   // Self-modification
        s ← evaluate(c, B)                // Evaluate on benchmark
        if c.is_valid() then
            A ← A ∪ {(c, s)}              // Keep children capable of code editing
        end if
    end foreach
end for
return A
```

以下是基线「不含自我改进智能体的 DGM」的伪代码，在第 4.3 节中描述：

算法 2 Darwin Gödel Machine without Self-improving agents

```text
Input: Initial coding agent g_0, benchmark suite B, maximum iterations T
Output: Archive of agents A

s_0 ← evaluate(g_0, B)                    // Evaluate the base agent
initialize A ← {(g_0, s_0)}               // Start with the base agent
for t ← 1 to T do
    P ← SelectParents(A)                  // Select parent agents
    foreach p ∈ P do
        c ← g_0.modify(p)                 // Modify with base agent
        s ← evaluate(c, B)                // Evaluate on benchmark
        if c.is_valid() then
            A ← A ∪ {(c, s)}              // Keep children capable of code editing
        end if
    end foreach
end for
return A
```

以下是基线「不含开放式探索的 DGM」的伪代码，在第 4.3 节中描述：

算法 3 Darwin Gödel Machine without Open-ended exploration

```text
Input: Initial coding agent g_0, benchmark suite B, maximum iterations T
Output: Archive of agents A

s_0 ← evaluate(g_0, B)                    // Evaluate the base agent
initialize A ← {(g_0, s_0)}               // Start with the base agent
for t ← 1 to T do
    P ← SelectParents(A)                  // Select parent agents
    foreach p ∈ P do
        c ← p.modify(p)                   // Self-modification
        s ← evaluate(c, B)                // Evaluate on benchmark
        if c.is_valid() then
            A ← {(c, s)}                  // Only keep the latest agent
        end if
    end foreach
end for
return A
```

## 附录 D 实验细节

### D.1 基础模型的超参数

表 3 展示了每个实验设置中使用的基础模型，如第 4.1 节所述。由于 SWE-bench 是更具挑战性的编码基准测试，我们使用更强的编码模型 Claude 3.5 Sonnet (New)（基于我们的初步测试）。为了加快迭代速度并避免与 Claude 相同的速率限制，Polyglot 实验使用 o3-mini。所有设置中所有 FM 的 temperature 均设为 1.0。

表 3：各实验设置中使用的基础模型。

| 基准测试 | SWE-bench | Polyglot |
| --- | --- | --- |
| 自我修改 | Claude 3.5 Sonnet (New) | Claude 3.5 Sonnet (New) |
| 评估 | Claude 3.5 Sonnet (New) | o3-mini |

## 附录 E 基准测试细节

### E.1 成本估算

完成一次 DGM 在 SWE-bench 上的运行（如第 4 节所述）的估算成本约为 22,000 美元。相比之下，完成任一基线（DGM w/o self-improve 或 DGM w/o open-ended exploration）在 SWE-bench 上的一次运行的估算成本约为 10,000 美元。尽管 DGM 的成本显著高于基线，但一种能够持续改进的方法——哪怕成本更高——也优于那种无法改进、或停滞在永远无法匹敌 DGM 的性能水平上的方法。更细粒度的拆分如下：

| LLM | 基准测试 | 任务数 | 成本估算（美元） |
| --- | --- | --- | --- |
| Claude 3.5 Sonnet (New) | SWE-bench | 60 | $350 |
| o3-mini | Polyglot | 60 | $5 |

我们承认当前在 SWE-bench 上的实验需要可观的算力。因此，我们还纳入了在另一个基准测试 Polyglot 上的实验，其成本显著更低。这表明开销随任务复杂度差异很大，而 SWE-bench 属于更复杂、更耗资源的编码基准测试之列。此外，若干有影响力的方法（例如 LLM 训练在诞生之初）在早期同样需要大量计算。与这些开创性工作类似，我们希望为未来改进本方法的效率与可扩展性的研究打开大门。另外，SWE-bench 排行榜上许多领先的编码智能体背后都是雇有专职专家研究员与工程师的产业公司，产生大量人力成本。相比之下，我们的方法通过完全自主、无需人类干预的自我改进达到了 SoTA 水平的性能；在把专业 AI 开发人才的成本与 API 使用成本相比较时，这或许能带来更高的效率。最后，随着 FM 持续改进、计算成本持续下降，DGM 这类方法将变得越来越高效、越来越可及。

另外，DGM 发现的性能更高的智能体确实比初始智能体产生更高的推理成本，但成本与性能并非严格相关——一些昂贵的智能体表现不如更便宜的智能体。

### E.2 SWE-bench 任务

用于验证编码智能体基本功能的初始 10 个任务：
- django__django-10973
- django__django-11066
- django__django-12754
- django__django-15930
- django__django-13279
- django__django-16661
- django__django-13346
- django__django-10880
- django__django-10999
- django__django-11087

用于估计编码智能体总体有效性的附加 50 个任务：
- django__django-9296
- django__django-11790
- django__django-11815
- django__django-11848
- django__django-11880
- django__django-11885
- django__django-11951
- django__django-11964
- django__django-11999
- django__django-12039
- django__django-12050
- django__django-12143
- django__django-12155
- django__django-12193
- django__django-12209
- django__django-12262
- django__django-12273
- django__django-12276
- django__django-12304
- django__django-12308
- django__django-12325
- django__django-12406
- django__django-12708
- django__django-12713
- django__django-12774
- sphinx-doc__sphinx-7454
- sphinx-doc__sphinx-7590
- sphinx-doc__sphinx-7748
- sphinx-doc__sphinx-7757
- sphinx-doc__sphinx-7985
- sphinx-doc__sphinx-8035
- sphinx-doc__sphinx-8056
- sphinx-doc__sphinx-8265
- sphinx-doc__sphinx-8269
- sphinx-doc__sphinx-8475
- sphinx-doc__sphinx-8548
- sphinx-doc__sphinx-8551
- sphinx-doc__sphinx-8638
- sphinx-doc__sphinx-8721
- sphinx-doc__sphinx-9229
- sphinx-doc__sphinx-9230
- sphinx-doc__sphinx-9281
- sphinx-doc__sphinx-9320
- sphinx-doc__sphinx-9367
- sphinx-doc__sphinx-9461
- sphinx-doc__sphinx-9698
- sphinx-doc__sphinx-10449
- sphinx-doc__sphinx-10466
- sphinx-doc__sphinx-10673
- sphinx-doc__sphinx-11510

用于更准确评估编码智能体性能的附加 140 个任务：
- astropy__astropy-12907
- astropy__astropy-13033
- astropy__astropy-13236
- astropy__astropy-13398
- astropy__astropy-13453
- astropy__astropy-13579
- astropy__astropy-13977
- astropy__astropy-14096
- astropy__astropy-14182
- astropy__astropy-14309
- astropy__astropy-14365
- astropy__astropy-14369
- astropy__astropy-14508
- astropy__astropy-14539
- astropy__astropy-14598
- astropy__astropy-14995
- astropy__astropy-7166
- astropy__astropy-7336
- astropy__astropy-7606
- astropy__astropy-7671
- astropy__astropy-8707
- astropy__astropy-8872
- django__django-10097
- django__django-10554
- django__django-10914
- django__django-11095
- django__django-11099
- django__django-11119
- django__django-11133
- django__django-11138
- django__django-11141
- django__django-11149
- django__django-11163
- django__django-11179
- django__django-11206
- django__django-11211
- django__django-11239
- django__django-11265
- django__django-11276
- django__django-11292
- django__django-11299
- django__django-11333
- django__django-11400
- django__django-11433
- django__django-11451
- django__django-11477
- django__django-11490
- django__django-11532
- django__django-11551
- django__django-11555
- django__django-11603
- django__django-11728
- django__django-11734
- django__django-11740
- django__django-11749
- django__django-11820
- django__django-12125
- django__django-12419
- django__django-12663
- django__django-12741
- django__django-12858
- django__django-12965
- django__django-13012
- django__django-13023
- django__django-13028
- django__django-13033
- django__django-13089
- django__django-13109
- django__django-13112
- django__django-13121
- django__django-13128
- django__django-13158
- django__django-13195
- django__django-13212
- django__django-13297
- django__django-13315
- django__django-13343
- django__django-13344
- django__django-13363
- django__django-13401
- django__django-13406
- django__django-13410
- django__django-13417
- django__django-13449
- django__django-13512
- django__django-13513
- django__django-13516
- django__django-13551
- django__django-13568
- django__django-13569
- django__django-13590
- django__django-13658
- django__django-13670
- django__django-13741
- django__django-13786
- django__django-13794
- django__django-13807
- django__django-13809
- django__django-13810
- django__django-13820
- django__django-13821
- django__django-13837
- django__django-13925
- django__django-13933
- django__django-13964
- django__django-14007
- django__django-14011
- django__django-14017
- django__django-14034
- django__django-14053
- django__django-14089
- django__django-14122
- django__django-14140
- django__django-14155
- django__django-14170
- django__django-14238
- django__django-14311
- django__django-14315
- django__django-14349
- django__django-14351
- django__django-14373
- django__django-14376
- django__django-14404
- django__django-14434
- django__django-14493
- django__django-14500
- django__django-14534
- django__django-14539
- django__django-14559
- django__django-14580
- django__django-14608
- django__django-14631
- django__django-14672
- django__django-14725
- django__django-14752
- django__django-14765
- django__django-14771
- django__django-14787
- django__django-14792
- django__django-14855

### E.3 Polyglot 任务

用于验证编码智能体基本功能的初始 10 个任务：
- go__dominoes
- cpp__all-your-base
- python__dominoes
- java__sgf-parsing
- javascript__robot-name
- rust__variable-length-quantity
- python__beer-song
- go__book-store
- javascript__bottle-song
- rust__bowling

用于估计编码智能体总体有效性的附加 50 个任务：
- javascript__queen-attack
- rust__wordy
- python__dot-dsl
- java__satellite
- cpp__diamond
- rust__accumulate
- go__error-handling
- cpp__queen-attack
- rust__poker
- python__sgf-parsing
- rust__react
- java__ledger
- go__connect
- rust__macros
- javascript__triangle
- java__zipper
- java__bowling
- python__tree-building
- javascript__say
- java__wordy
- python__food-chain
- javascript__wordy
- python__poker
- javascript__grade-school
- cpp__gigasecond
- java__forth
- python__dominoes
- go__word-search
- javascript__simple-linked-list
- go__counter
- java__react
- javascript__ocr-numbers
- python__scale-generator
- java__go-counting
- rust__doubly-linked-list
- python__grade-school
- javascript__forth
- python__wordy
- java__mazy-mice
- cpp__bank-account
- python__zipper
- java__custom-set
- java__rest-api
- go__transpose
- rust__gigasecond
- rust__say
- go__food-chain
- rust__pig-latin
- go__markdown
- go__crypto-square


### E.4 SWE-bench 最先进结果

在撰写本文时（2025 年 4 月 16 日），SWE-bench Verified 上表现最高、经过核验（即 SWE-bench 团队获得了该系统的访问权限并能够复现其补丁生成）的开源条目是 OpenHands + CodeAct v2.1（claude-3-5-sonnet-20241022）（Wang et al., 2024），取得 53.0%。仅考虑 DGM 所用的同一 200 任务子集（第 E.2 节）时，OpenHands + CodeAct v2.1（claude-3-5-sonnet-20241022）取得 51.0%。

### E.5 Polyglot 代表性智能体

Aider（Gauthier, 2024）是社区中流行的编码智能体，于 2024 年春发布。它在 GitHub 上已收获超过 33,000 颗星，并由人类开发者针对 Polyglot 基准测试持续开发与测试超过一年，主要用于评估其性能。Aider 也已成为评估不同模型性能的标准基线，当前 Polyglot 基准测试上表现最好的条目是 o3（high）与 GPT-4.1 的组合。我们采用与 Polyglot 排行榜类似的设置，但有一个关键区别：排行榜报告 pass@2 性能，其中智能体可以查看一次来自真值测试的反馈；与之相对，我们使用 pass@1 设置，智能体从不会看到真值测试的结果，因为我们认为这更贴近现实的编码应用。

## 附录 F 最佳发现的智能体

### F.1 SWE-bench 上的 DGM

构成 DGM 在 SWE-bench 上发现的最佳智能体的 diff 补丁：
```diff
diff --git a/coding_agent.py b/coding_agent.py
index 2cd395a..9a2cc2f 100644
--- a/coding_agent.py
+++ b/coding_agent.py
@@ -4,6 +4,7 @@ import logging
from logging.handlers import RotatingFileHandler
import os
import threading
+import re
from llm_withtools import CLAUDE_MODEL, OPENAI_MODEL, chat_with_agent
from utils.eval_utils import get_report_score, msg_history_to_report, score_tie_breaker
@@ -63,6 +64,42 @@ def safe_log(message, level=logging.INFO):
else:
print(f"Warning: No logger found for thread {threading.get_ident()}")
+def is_patch_valid(patch_str):
+ """
+ Parse the patch to check if any non-test source files are modified.
+ Returns (bool, str) tuple: (is_valid, reason)
+ """
+ if not patch_str or patch_str.isspace():
+ return False, "Empty patch"
+
+ # Parse the patch to find modified files
+ modified_files = []
+ diff_header_pattern = re.compile(r’^\+\+\+ b/(.+)$’, re.MULTILINE)
+ for match in diff_header_pattern.finditer(patch_str):
+ filepath = match.group(1)
+ if filepath != ’/dev/null’: # Skip deleted files
+ modified_files.append(filepath)
+
+ if not modified_files:
+ return False, "No files modified"
+
+ # Check if any non-test files are modified
+ test_patterns = (
+ lambda f: f.startswith(’tests/’),
+ lambda f: f.startswith(’test_’),
+ lambda f: f.endswith(’_test.py’)
+ )
+
+ source_files = [
+ f for f in modified_files
+ if not any(pattern(f) for pattern in test_patterns)
+ ]
+
+ if not source_files:
+ return False, "Only test files were modified"
+
+ return True, "Valid patch with source file modifications"
+
class AgenticSystem:
def __init__(
self,
@@ -73,6 +110,7 @@ class AgenticSystem:
test_description=None,
self_improve=False,
instance_id=None,
+ max_retries=3,
):
self.problem_statement = problem_statement
self.git_tempdir = git_tempdir
@@ -82,6 +120,7 @@ class AgenticSystem:
self.self_improve = self_improve
self.instance_id = instance_id if not self_improve else ’dgm’
self.code_model = CLAUDE_MODEL
+ self.max_retries = max_retries
# Initialize logger and store it in thread-local storage
self.logger = setup_logger(chat_history_file)
@@ -153,7 +192,7 @@ Your task is to run the regression tests in the {self.git_tempdir} directory to
"""
The forward function for the AgenticSystem.
"""
- instruction = f"""I have uploaded a Python code repository in the directory {self.git_tempdir}. Help solve the following problem.
+ base_instruction = f"""I have uploaded a Python code repository in the directory {self.git_tempdir}. Help solve the following problem.
<problem_description>
{self.problem_statement}
@@ -165,7 +204,39 @@ Your task is to run the regression tests in the {self.git_tempdir} directory to
Your task is to make changes to the files in the {self.git_tempdir} directory to address the <problem_description>. I have already taken care of the required dependencies.
"""
- new_msg_history = chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
+
+ retry_count = 0
+ while retry_count < self.max_retries:
+ safe_log(f"\n=== Attempt {retry_count + 1} of {self.max_retries} ===")
+
+ # Reset to base commit before each attempt
+ if retry_count > 0:
+ reset_to_commit(self.git_tempdir, self.base_commit)
+
+ # Add retry context to instruction if this is a retry attempt
+ instruction = base_instruction
+ if retry_count > 0:
+ instruction += f"""\nNOTE: Previous attempt(s) failed because they either produced empty patches or only modified test files.
+Please ensure your solution includes changes to the main source code files, not just test files."""
+
+ # Run the agent
+ new_msg_history = chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
+
+ # Check the patch
+ patch = self.get_current_edits()
+ is_valid, reason = is_patch_valid(patch)
+
+ if is_valid:
+ safe_log(f"Valid patch generated: {reason}")
+ break
+ else:
+ safe_log(f"Invalid patch: {reason}")
+ if retry_count < self.max_retries - 1:
+ safe_log("Retrying with a new attempt...")
+ else:
+ safe_log("Maximum retries reached. Unable to generate a valid patch.")
+
+ retry_count += 1
def main():
parser = argparse.ArgumentParser(description=’Process repository with an agentic system.’)
@@ -177,6 +248,7 @@ def main():
parser.add_argument(’--test_description’, default=None, required=False, help=’Description of how to test the repository’)
parser.add_argument(’--self_improve’, default=False, action=’store_true’, help=’Whether to self-improve the repository or solving swe’)
parser.add_argument(’--instance_id’, default=None, help=’Instance ID for SWE issue’)
+ parser.add_argument(’--max_retries’, type=int, default=3, help=’Maximum number of patch generation attempts’)
args = parser.parse_args()
# Process the repository
@@ -188,6 +260,7 @@ def main():
test_description=args.test_description,
self_improve=args.self_improve,
instance_id=args.instance_id,
+ max_retries=args.max_retries,
)
# Run the agentic system to try to solve the problem
@@ -200,4 +273,4 @@ def main():
f.write(model_patch)
if __name__ == "__main__":
- main()
+ main()
\ No newline at end of file
diff --git a/tests/test_patch_validator.py b/tests/test_patch_validator.py
new file mode 100644
index 0000000..5689f7d
--- /dev/null
+++ b/tests/test_patch_validator.py
@@ -0,0 +1,77 @@
+import pytest
+from coding_agent import is_patch_valid
+
+def test_empty_patch():
+ # Test empty patch
+ is_valid, reason = is_patch_valid("")
+ assert not is_valid
+ assert reason == "Empty patch"
+
+ # Test whitespace-only patch
+ is_valid, reason = is_patch_valid(" \n ")
+ assert not is_valid
+ assert reason == "Empty patch"
+
+def test_test_only_patch():
+ patch = """
+diff --git a/tests/test_edit_tool.py b/tests/test_edit_tool.py
+index abc123..def456 100644
+--- a/tests/test_edit_tool.py
++++ b/tests/test_edit_tool.py
+@@ -10,6 +10,8 @@ def test_something():
+ assert True
++ assert 1 == 1
+"""
+ is_valid, reason = is_patch_valid(patch)
+ assert not is_valid
+ assert reason == "Only test files were modified"
+
+def test_source_file_patch():
+ patch = """
+diff --git a/tools/edit.py b/tools/edit.py
+index abc123..def456 100644
+--- a/tools/edit.py
++++ b/tools/edit.py
+@@ -10,6 +10,8 @@ class Editor:
+ def edit(self):
+ pass
++ return True
+"""
+ is_valid, reason = is_patch_valid(patch)
+ assert is_valid
+ assert reason == "Valid patch with source file modifications"
+
+def test_mixed_files_patch():
+ patch = """
+diff --git a/tools/edit.py b/tools/edit.py
+index abc123..def456 100644
+--- a/tools/edit.py
++++ b/tools/edit.py
+@@ -10,6 +10,8 @@ class Editor:
+ def edit(self):
+ pass
++ return True
+
+diff --git a/tests/test_edit.py b/tests/test_edit.py
+index abc123..def456 100644
+--- a/tests/test_edit.py
++++ b/tests/test_edit.py
+@@ -10,6 +10,8 @@ def test_something():
+ assert True
++ assert 1 == 1
+"""
+ is_valid, reason = is_patch_valid(patch)
+ assert is_valid
+ assert reason == "Valid patch with source file modifications"
+
+def test_no_files_modified():
+ patch = """
+diff --git a/nonexistent.py b/nonexistent.py
+deleted file mode 100644
+index abc123..0000000
+--- a/nonexistent.py
++++ /dev/null
+"""
+ is_valid, reason = is_patch_valid(patch)
+ assert not is_valid
+ assert reason == "No files modified"
\ No newline at end of file
[⬇](data:text/plain;base64,ZGlmZiAtLWdpdCBhL3Rvb2xzL2VkaXQucHkgYi90b29scy9lZGl0LnB5CmluZGV4IDU5MTM3ZWUuLjE2YWU1MjEgMTAwNjQ0Ci0tLSBhL3Rvb2xzL2VkaXQucHkKKysrIGIvdG9vbHMvZWRpdC5weQpAQCAtMSwxNiArMSwxNyBAQAogZnJvbSBwYXRobGliIGltcG9ydCBQYXRoCiBpbXBvcnQgc3VicHJvY2VzcworZnJvbSB0eXBpbmcgaW1wb3J0IE9wdGlvbmFsLCBMaXN0LCBUdXBsZSwgVW5pb24KCiBkZWYgdG9vbF9pbmZvKCk6CiAgICAgcmV0dXJuIHsKICAgICAgICAgIm5hbWUiOiAiZWRpdG9yIiwKICAgICAgICAgImRlc2NyaXB0aW9uIjogIiIiQ3VzdG9tIGVkaXRpbmcgdG9vbCBmb3Igdmlld2luZywgY3JlYXRpbmcsIGFuZCBlZGl0aW5nIGZpbGVzXG4KICogU3RhdGUgaXMgcGVyc2lzdGVudCBhY3Jvc3MgY29tbWFuZCBjYWxscyBhbmQgZGlzY3Vzc2lvbnMgd2l0aCB0aGUgdXNlci5cbgotKiBJZiBgcGF0aGAgaXMgYSBmaWxlLCBgdmlld2AgZGlzcGxheXMgdGhlIGVudGlyZSBmaWxlIHdpdGggbGluZSBudW1iZXJzLiBJZiBgcGF0aGAgaXMgYSBkaXJlY3RvcnksIGB2aWV3YCBsaXN0cyBub24taGlkZGVuIGZpbGVzIGFuZCBkaXJlY3RvcmllcyB1cCB0byAyIGxldmVscyBkZWVwLlxuCisqIElmIGBwYXRoYCBpcyBhIGZpbGUsIGB2aWV3YCBkaXNwbGF5cyB0aGUgZmlsZSB3aXRoIGxpbmUgbnVtYmVycy4gV2l0aCBvcHRpb25hbCBgdmlld19yYW5nZWAgW3N0YXJ0LCBlbmRdLCBpdCBkaXNwbGF5cyBvbmx5IHNwZWNpZmllZCBsaW5lcy4gVXNlIC0xIGluIGBlbmRgIGZvciBhbGwgcmVtYWluaW5nIGxpbmVzLlxuCisqIElmIGBwYXRoYCBpcyBhIGRpcmVjdG9yeSwgYHZpZXdgIGxpc3RzIG5vbi1oaWRkZW4gZmlsZXMgYW5kIGRpcmVjdG9yaWVzIHVwIHRvIDIgbGV2ZWxzIGRlZXAuXG4KICogVGhlIGBjcmVhdGVgIGNvbW1hbmQgY2Fubm90IGJlIHVzZWQgaWYgdGhlIHNwZWNpZmllZCBgcGF0aGAgYWxyZWFkeSBleGlzdHMgYXMgYSBmaWxlLlxuCiAqIElmIGEgYGNvbW1hbmRgIGdlbmVyYXRlcyBhIGxvbmcgb3V0cHV0LCBpdCB3aWxsIGJlIHRydW5jYXRlZCBhbmQgbWFya2VkIHdpdGggYDxyZXNwb25zZSBjbGlwcGVkPmAuXG4KLSogVGhlIGBlZGl0YCBjb21tYW5kIG92ZXJ3cml0ZXMgdGhlIGVudGlyZSBmaWxlIHdpdGggdGhlIHByb3ZpZGVkIGBmaWxlX3RleHRgLlxuCi0qIE5vIHBhcnRpYWwvbGluZS1yYW5nZSBlZGl0cyBvciBwYXJ0aWFsIHZpZXdpbmcgYXJlIHN1cHBvcnRlZC4iIiIsCisqIFRoZSBgZWRpdGAgY29tbWFuZCBvdmVyd3JpdGVzIHRoZSBlbnRpcmUgZmlsZSB3aXRoIHRoZSBwcm92aWRlZCBgZmlsZV90ZXh0YC4iIiIsCiAgICAgICAgICJpbnB1dF9zY2hlbWEiOiB7CiAgICAgICAgICAgICAidHlwZSI6ICJvYmplY3QiLAogICAgICAgICAgICAgInByb3BlcnRpZXMiOiB7CkBAIC0yNiw2ICsyNywxMyBAQCBkZWYgdG9vbF9pbmZvKCk6CiAgICAgICAgICAgICAgICAgImZpbGVfdGV4dCI6IHsKICAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIlJlcXVpcmVkIHBhcmFtZXRlciBvZiBgY3JlYXRlYCBvciBgZWRpdGAgY29tbWFuZCwgY29udGFpbmluZyB0aGUgY29udGVudCBmb3IgdGhlIGVudGlyZSBmaWxlLiIsCiAgICAgICAgICAgICAgICAgICAgICJ0eXBlIjogInN0cmluZyIKKyAgICAgICAgICAgICAgICB9LAorICAgICAgICAgICAgICAgICJ2aWV3X3JhbmdlIjogeworICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiT3B0aW9uYWwgcGFyYW1ldGVyIGZvciBgdmlld2AgY29tbWFuZC4gQXJyYXkgb2YgW3N0YXJ0X2xpbmUsIGVuZF9saW5lXSAoMS1iYXNlZCkuIFVzZSAtMSBmb3IgZW5kX2xpbmUgdG8gcmVhZCB1bnRpbCBlbmQgb2YgZmlsZS4iLAorICAgICAgICAgICAgICAgICAgICAidHlwZSI6ICJhcnJheSIsCisgICAgICAgICAgICAgICAgICAgICJpdGVtcyI6IHsidHlwZSI6ICJpbnRlZ2VyIn0sCisgICAgICAgICAgICAgICAgICAgICJtaW5JdGVtcyI6IDIsCisgICAgICAgICAgICAgICAgICAgICJtYXhJdGVtcyI6IDIKICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICB9LAogICAgICAgICAgICAgInJlcXVpcmVkIjogWyJjb21tYW5kIiwgInBhdGgiXQpAQCAtODksNiArOTcsNDYgQEAgZGVmIHJlYWRfZmlsZShwYXRoOiBQYXRoKSAtPiBzdHI6CiAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgICByYWlzZSBWYWx1ZUVycm9yKGYiRmFpbGVkIHRvIHJlYWQgZmlsZToge2V9IikKCitkZWYgcmVhZF9maWxlX3JhbmdlKHBhdGg6IFBhdGgsIGxpbmVfcmFuZ2U6IE9wdGlvbmFsW0xpc3RbaW50XV0gPSBOb25lKSAtPiBUdXBsZVtzdHIsIGludF06CisgICAgIiIiCisgICAgUmVhZCBhbmQgcmV0dXJuIGZpbGUgY29udGVudHMgd2l0aGluIHNwZWNpZmllZCBsaW5lIHJhbmdlLgorICAgIFJldHVybnMgdHVwbGUgb2YgKGNvbnRlbnQsIHN0YXJ0X2xpbmUpLgorCisgICAgQXJnczoKKyAgICAgICAgcGF0aDogUGF0aCBvYmplY3QgZm9yIHRoZSBmaWxlCisgICAgICAgIGxpbmVfcmFuZ2U6IE9wdGlvbmFsIFtzdGFydCwgZW5kXSBsaW5lIG51bWJlcnMgKDEtYmFzZWQpLiBVc2UgLTEgZm9yIGVuZCB0byByZWFkIHVudGlsIEVPRi4KKyAgICAiIiIKKyAgICB0cnk6CisgICAgICAgIGlmIGxpbmVfcmFuZ2UgaXMgTm9uZToKKyAgICAgICAgICAgIHJldHVybiByZWFkX2ZpbGUocGF0aCksIDEKKworICAgICAgICBzdGFydCwgZW5kID0gbGluZV9yYW5nZQorICAgICAgICBpZiBzdGFydCA8IDE6CisgICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKCJTdGFydCBsaW5lIG11c3QgYmUgPj0gMSIpCisgICAgICAgIGlmIGVuZCAhPSAtMSBhbmQgZW5kIDwgc3RhcnQ6CisgICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKCJFbmQgbGluZSBtdXN0IGJlID49IHN0YXJ0IGxpbmUgb3IgLTEiKQorCisgICAgICAgIHdpdGggcGF0aC5vcGVuKCkgYXMgZjoKKyAgICAgICAgICAgICMgU2tpcCBsaW5lcyBiZWZvcmUgc3RhcnQKKyAgICAgICAgICAgIGZvciBfIGluIHJhbmdlKHN0YXJ0IC0gMSk6CisgICAgICAgICAgICAgICAgbmV4dChmLCBOb25lKQorCisgICAgICAgICAgICBsaW5lcyA9IFtdCisgICAgICAgICAgICBjdXJyZW50X2xpbmUgPSBzdGFydAorICAgICAgICAgICAgd2hpbGUgVHJ1ZToKKyAgICAgICAgICAgICAgICBsaW5lID0gbmV4dChmLCBOb25lKQorICAgICAgICAgICAgICAgIGlmIGxpbmUgaXMgTm9uZTogICMgRU9GCisgICAgICAgICAgICAgICAgICAgIGJyZWFrCisgICAgICAgICAgICAgICAgaWYgZW5kICE9IC0xIGFuZCBjdXJyZW50X2xpbmUgPiBlbmQ6CisgICAgICAgICAgICAgICAgICAgIGJyZWFrCisgICAgICAgICAgICAgICAgbGluZXMuYXBwZW5kKGxpbmUucnN0cmlwKCdcbicpKQorICAgICAgICAgICAgICAgIGN1cnJlbnRfbGluZSArPSAxCisKKyAgICAgICAgcmV0dXJuICdcbicuam9pbihsaW5lcyksIHN0YXJ0CisKKyAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CisgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJGYWlsZWQgdG8gcmVhZCBmaWxlIHJhbmdlOiB7ZX0iKQorCiBkZWYgd3JpdGVfZmlsZShwYXRoOiBQYXRoLCBjb250ZW50OiBzdHIpOgogICAgICIiIldyaXRlIChvdmVyd3JpdGUpIGVudGlyZSBmaWxlIGNvbnRlbnRzLiIiIgogICAgIHRyeToKQEAgLTk2LDkgKzE0NCwxOCBAQCBkZWYgd3JpdGVfZmlsZShwYXRoOiBQYXRoLCBjb250ZW50OiBzdHIpOgogICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIkZhaWxlZCB0byB3cml0ZSBmaWxlOiB7ZX0iKQoKLWRlZiB2aWV3X3BhdGgocGF0aF9vYmo6IFBhdGgpIC0+IHN0cjoKLSAgICAiIiJWaWV3IHRoZSBlbnRpcmUgZmlsZSBjb250ZW50cyBvciBkaXJlY3RvcnkgbGlzdGluZy4iIiIKK2RlZiB2aWV3X3BhdGgocGF0aF9vYmo6IFBhdGgsIHZpZXdfcmFuZ2U6IE9wdGlvbmFsW0xpc3RbaW50XV0gPSBOb25lKSAtPiBzdHI6CisgICAgIiIiCisgICAgVmlldyB0aGUgZmlsZSBjb250ZW50cyAob3B0aW9uYWxseSB3aXRoaW4gYSByYW5nZSkgb3IgZGlyZWN0b3J5IGxpc3RpbmcuCisKKyAgICBBcmdzOgorICAgICAgICBwYXRoX29iajogUGF0aCBvYmplY3QgZm9yIHRoZSBmaWxlIG9yIGRpcmVjdG9yeQorICAgICAgICB2aWV3X3JhbmdlOiBPcHRpb25hbCBbc3RhcnQsIGVuZF0gbGluZSBudW1iZXJzIGZvciBmaWxlIHZpZXdpbmcKKyAgICAiIiIKICAgICBpZiBwYXRoX29iai5pc19kaXIoKToKKyAgICAgICAgaWYgdmlld19yYW5nZSBpcyBub3QgTm9uZToKKyAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoInZpZXdfcmFuZ2UgaXMgbm90IHN1cHBvcnRlZCBmb3IgZGlyZWN0b3J5IGxpc3RpbmdzIikKKwogICAgICAgICAjIEZvciBkaXJlY3RvcmllczogbGlzdCBub24taGlkZGVuIGZpbGVzIHVwIHRvIDIgbGV2ZWxzIGRlZXAKICAgICAgICAgdHJ5OgogICAgICAgICAgICAgcmVzdWx0ID0gc3VicHJvY2Vzcy5ydW4oCkBAIC0xMTUsMTQgKzE3MiwxNCBAQCBkZWYgdmlld19wYXRoKHBhdGhfb2JqOiBQYXRoKSAtPiBzdHI6CiAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJGYWlsZWQgdG8gbGlzdCBkaXJlY3Rvcnk6IHtlfSIpCgotICAgICMgSWYgaXQncyBhIGZpbGUsIHNob3cgdGhlIGVudGlyZSBmaWxlIHdpdGggbGluZSBudW1iZXJzCi0gICAgY29udGVudCA9IHJlYWRfZmlsZShwYXRoX29iaikKLSAgICByZXR1cm4gZm9ybWF0X291dHB1dChjb250ZW50LCBzdHIocGF0aF9vYmopKQorICAgICMgSWYgaXQncyBhIGZpbGUsIHNob3cgdGhlIGZpbGUgY29udGVudCAod2l0aCBvcHRpb25hbCBsaW5lIHJhbmdlKQorICAgIGNvbnRlbnQsIHN0YXJ0X2xpbmUgPSByZWFkX2ZpbGVfcmFuZ2UocGF0aF9vYmosIHZpZXdfcmFuZ2UpCisgICAgcmV0dXJuIGZvcm1hdF9vdXRwdXQoY29udGVudCwgc3RyKHBhdGhfb2JqKSwgc3RhcnRfbGluZSkKCi1kZWYgdG9vbF9mdW5jdGlvbihjb21tYW5kOiBzdHIsIHBhdGg6IHN0ciwgZmlsZV90ZXh0OiBzdHIgPSBOb25lKSAtPiBzdHI6CitkZWYgdG9vbF9mdW5jdGlvbihjb21tYW5kOiBzdHIsIHBhdGg6IHN0ciwgZmlsZV90ZXh0OiBzdHIgPSBOb25lLCB2aWV3X3JhbmdlOiBPcHRpb25hbFtMaXN0W2ludF1dID0gTm9uZSkgLT4gc3RyOgogICAgICIiIgogICAgIE1haW4gdG9vbCBmdW5jdGlvbiB0aGF0IGhhbmRsZXM6Ci0gICAgICAtICd2aWV3JyAgOiBWaWV3IHRoZSBlbnRpcmUgZmlsZSBvciBkaXJlY3RvcnkgbGlzdGluZworICAgICAgLSAndmlldycgIDogVmlldyBmaWxlIG9yIGRpcmVjdG9yeSBsaXN0aW5nLCBvcHRpb25hbGx5IHdpdGhpbiBsaW5lIHJhbmdlIGZvciBmaWxlcwogICAgICAgLSAnY3JlYXRlJzogQ3JlYXRlIGEgbmV3IGZpbGUgd2l0aCB0aGUgZ2l2ZW4gZmlsZV90ZXh0CiAgICAgICAtICdlZGl0JyAgOiBPdmVyd3JpdGUgYW4gZXhpc3RpbmcgZmlsZSB3aXRoIGZpbGVfdGV4dAogICAgICIiIgpAQCAtMTMwLDcgKzE4Nyw3IEBAIGRlZiB0b29sX2Z1bmN0aW9uKGNvbW1hbmQ6IHN0ciwgcGF0aDogc3RyLCBmaWxlX3RleHQ6IHN0ciA9IE5vbmUpIC0+IHN0cjoKICAgICAgICAgcGF0aF9vYmogPSB2YWxpZGF0ZV9wYXRoKHBhdGgsIGNvbW1hbmQpCgogICAgICAgICBpZiBjb21tYW5kID09ICJ2aWV3IjoKLSAgICAgICAgICAgIHJldHVybiB2aWV3X3BhdGgocGF0aF9vYmopCisgICAgICAgICAgICByZXR1cm4gdmlld19wYXRoKHBhdGhfb2JqLCB2aWV3X3JhbmdlKQoKICAgICAgICAgZWxpZiBjb21tYW5kID09ICJjcmVhdGUiOgogICAgICAgICAgICAgaWYgZmlsZV90ZXh0IGlzIE5vbmU6CkBAIC0xNTIsNCArMjA5LDQgQEAgZGVmIHRvb2xfZnVuY3Rpb24oY29tbWFuZDogc3RyLCBwYXRoOiBzdHIsIGZpbGVfdGV4dDogc3RyID0gTm9uZSkgLT4gc3RyOgoKIGlmIF9fbmFtZV9fID09ICJfX21haW5fXyI6CiAgICAgIyBFeGFtcGxlIHVzYWdlCi0gICAgcHJpbnQodG9vbF9mdW5jdGlvbigidmlldyIsICIvaG9tZS91YnVudHUveHgvZGdtL2NvZGluZ19hZ2VudC5weSIpKQorICAgIHByaW50KHRvb2xfZnVuY3Rpb24oInZpZXciLCAiL2hvbWUvdWJ1bnR1L3h4L2RnbS9jb2RpbmdfYWdlbnQucHkiKSkKXCBObyBuZXdsaW5lIGF0IGVuZCBvZiBmaWxlCmRpZmYgLS1naXQgYS90ZXN0cy90ZXN0X3Rvb2xzL3Rlc3RfZWRpdC5weSBiL3Rlc3RzL3Rlc3RfdG9vbHMvdGVzdF9lZGl0LnB5Cm5ldyBmaWxlIG1vZGUgMTAwNjQ0CmluZGV4IDAwMDAwMDAuLjA0ZjUzNWIKLS0tIC9kZXYvbnVsbAorKysgYi90ZXN0cy90ZXN0X3Rvb2xzL3Rlc3RfZWRpdC5weQpAQCAtMCwwICsxLDU0IEBACitpbXBvcnQgcHl0ZXN0Citmcm9tIHBhdGhsaWIgaW1wb3J0IFBhdGgKK2Zyb20gdG9vbHMuZWRpdCBpbXBvcnQgdG9vbF9mdW5jdGlvbgorCitkZWYgdGVzdF92aWV3X2xpbmVfcmFuZ2UodG1wX3BhdGgpOgorICAgICMgQ3JlYXRlIGEgdGVzdCBmaWxlCisgICAgdGVzdF9maWxlID0gdG1wX3BhdGggLyAidGVzdC50eHQiCisgICAgdGVzdF9jb250ZW50ID0gImxpbmUxXG5saW5lMlxubGluZTNcbmxpbmU0XG5saW5lNVxuIgorICAgIHRlc3RfZmlsZS53cml0ZV90ZXh0KHRlc3RfY29udGVudCkKKworICAgICMgVGVzdCB2aWV3aW5nIHNwZWNpZmljIGxpbmUgcmFuZ2UKKyAgICByZXN1bHQgPSB0b29sX2Z1bmN0aW9uKCJ2aWV3Iiwgc3RyKHRlc3RfZmlsZSksIHZpZXdfcmFuZ2U9WzIsIDRdKQorICAgIGFzc2VydCAibGluZTIiIGluIHJlc3VsdAorICAgIGFzc2VydCAibGluZTMiIGluIHJlc3VsdAorICAgIGFzc2VydCAibGluZTQiIGluIHJlc3VsdAorICAgIGFzc2VydCAibGluZTEiIG5vdCBpbiByZXN1bHQKKyAgICBhc3NlcnQgImxpbmU1IiBub3QgaW4gcmVzdWx0CisgICAgYXNzZXJ0ICIgICAgIDJcdCIgaW4gcmVzdWx0ICAjIENvcnJlY3QgbGluZSBudW1iZXJpbmcKKworICAgICMgVGVzdCB2aWV3aW5nIGZyb20gc3RhcnQgdG8gbWlkZGxlCisgICAgcmVzdWx0ID0gdG9vbF9mdW5jdGlvbigidmlldyIsIHN0cih0ZXN0X2ZpbGUpLCB2aWV3X3JhbmdlPVsxLCAzXSkKKyAgICBhc3NlcnQgImxpbmUxIiBpbiByZXN1bHQKKyAgICBhc3NlcnQgImxpbmUyIiBpbiByZXN1bHQKKyAgICBhc3NlcnQgImxpbmUzIiBpbiByZXN1bHQKKyAgICBhc3NlcnQgImxpbmU0IiBub3QgaW4gcmVzdWx0CisgICAgYXNzZXJ0ICIgICAgIDFcdCIgaW4gcmVzdWx0CisKKyAgICAjIFRlc3Qgdmlld2luZyBmcm9tIG1pZGRsZSB0byBlbmQgd2l0aCAtMQorICAgIHJlc3VsdCA9IHRvb2xfZnVuY3Rpb24oInZpZXciLCBzdHIodGVzdF9maWxlKSwgdmlld19yYW5nZT1bMywgLTFdKQorICAgIGFzc2VydCAibGluZTEiIG5vdCBpbiByZXN1bHQKKyAgICBhc3NlcnQgImxpbmUyIiBub3QgaW4gcmVzdWx0CisgICAgYXNzZXJ0ICJsaW5lMyIgaW4gcmVzdWx0CisgICAgYXNzZXJ0ICJsaW5lNCIgaW4gcmVzdWx0CisgICAgYXNzZXJ0ICJsaW5lNSIgaW4gcmVzdWx0CisgICAgYXNzZXJ0ICIgICAgIDNcdCIgaW4gcmVzdWx0CisKK2RlZiB0ZXN0X3ZpZXdfcmFuZ2VfdmFsaWRhdGlvbih0bXBfcGF0aCk6CisgICAgIyBDcmVhdGUgYSB0ZXN0IGZpbGUKKyAgICB0ZXN0X2ZpbGUgPSB0bXBfcGF0aCAvICJ0ZXN0LnR4dCIKKyAgICB0ZXN0X2NvbnRlbnQgPSAibGluZTFcbmxpbmUyXG5saW5lM1xuIgorICAgIHRlc3RfZmlsZS53cml0ZV90ZXh0KHRlc3RfY29udGVudCkKKworICAgICMgVGVzdCBpbnZhbGlkIHN0YXJ0IGxpbmUKKyAgICByZXN1bHQgPSB0b29sX2Z1bmN0aW9uKCJ2aWV3Iiwgc3RyKHRlc3RfZmlsZSksIHZpZXdfcmFuZ2U9WzAsIDJdKQorICAgIGFzc2VydCAiRmFpbGVkIHRvIHJlYWQgZmlsZSByYW5nZTogU3RhcnQgbGluZSBtdXN0IGJlID49IDEiIGluIHJlc3VsdAorCisgICAgIyBUZXN0IGludmFsaWQgcmFuZ2UgKGVuZCA8IHN0YXJ0KQorICAgIHJlc3VsdCA9IHRvb2xfZnVuY3Rpb24oInZpZXciLCBzdHIodGVzdF9maWxlKSwgdmlld19yYW5nZT1bMiwgMV0pCisgICAgYXNzZXJ0ICJGYWlsZWQgdG8gcmVhZCBmaWxlIHJhbmdlOiBFbmQgbGluZSBtdXN0IGJlID49IHN0YXJ0IGxpbmUgb3IgLTEiIGluIHJlc3VsdAorCitkZWYgdGVzdF92aWV3X3JhbmdlX3dpdGhfZGlyZWN0b3J5KHRtcF9wYXRoKToKKyAgICAjIFRlc3QgdGhhdCB2aWV3X3JhbmdlIGlzIHJlamVjdGVkIGZvciBkaXJlY3RvcmllcworICAgIHJlc3VsdCA9IHRvb2xfZnVuY3Rpb24oInZpZXciLCBzdHIodG1wX3BhdGgpLCB2aWV3X3JhbmdlPVsxLCAxMF0pCisgICAgYXNzZXJ0ICJFcnJvcjogdmlld19yYW5nZSBpcyBub3Qgc3VwcG9ydGVkIGZvciBkaXJlY3RvcnkgbGlzdGluZ3MiIGluIHJlc3VsdApcIE5vIG5ld2xpbmUgYXQgZW5kIG9mIGZpbGU=)
diff --git a/tools/edit.py b/tools/edit.py
index 59137ee..16ae521 100644
--- a/tools/edit.py
+++ b/tools/edit.py
@@ -1,16 +1,17 @@
from pathlib import Path
import subprocess
+from typing import Optional, List, Tuple, Union
def tool_info():
return {
"name": "editor",
"description": """Custom editing tool for viewing, creating, and editing files\n
* State is persistent across command calls and discussions with the user.\n
-* If ‘path‘ is a file, ‘view‘ displays the entire file with line numbers. If ‘path‘ is a directory, ‘view‘ lists non-hidden files and directories up to 2 levels deep.\n
+* If ‘path‘ is a file, ‘view‘ displays the file with line numbers. With optional ‘view_range‘ [start, end], it displays only specified lines. Use -1 in ‘end‘ for all remaining lines.\n
+* If ‘path‘ is a directory, ‘view‘ lists non-hidden files and directories up to 2 levels deep.\n
* The ‘create‘ command cannot be used if the specified ‘path‘ already exists as a file.\n
* If a ‘command‘ generates a long output, it will be truncated and marked with ‘<response clipped>‘.\n
-* The ‘edit‘ command overwrites the entire file with the provided ‘file_text‘.\n
-* No partial/line-range edits or partial viewing are supported.""",
+* The ‘edit‘ command overwrites the entire file with the provided ‘file_text‘.""",
"input_schema": {
"type": "object",
"properties": {
@@ -26,6 +27,13 @@ def tool_info():
"file_text": {
"description": "Required parameter of ‘create‘ or ‘edit‘ command, containing the content for the entire file.",
"type": "string"
+ },
+ "view_range": {
+ "description": "Optional parameter for ‘view‘ command. Array of [start_line, end_line] (1-based). Use -1 for end_line to read until end of file.",
+ "type": "array",
+ "items": {"type": "integer"},
+ "minItems": 2,
+ "maxItems": 2
}
},
"required": ["command", "path"]
@@ -89,6 +97,46 @@ def read_file(path: Path) -> str:
except Exception as e:
raise ValueError(f"Failed to read file: {e}")
+def read_file_range(path: Path, line_range: Optional[List[int]] = None) -> Tuple[str, int]:
+ """
+ Read and return file contents within specified line range.
+ Returns tuple of (content, start_line).
+
+ Args:
+ path: Path object for the file
+ line_range: Optional [start, end] line numbers (1-based). Use -1 for end to read until EOF.
+ """
+ try:
+ if line_range is None:
+ return read_file(path), 1
+
+ start, end = line_range
+ if start < 1:
+ raise ValueError("Start line must be >= 1")
+ if end != -1 and end < start:
+ raise ValueError("End line must be >= start line or -1")
+
+ with path.open() as f:
+ # Skip lines before start
+ for _ in range(start - 1):
+ next(f, None)
+
+ lines = []
+ current_line = start
+ while True:
+ line = next(f, None)
+ if line is None: # EOF
+ break
+ if end != -1 and current_line > end:
+ break
+ lines.append(line.rstrip(’\n’))
+ current_line += 1
+
+ return ’\n’.join(lines), start
+
+ except Exception as e:
+ raise ValueError(f"Failed to read file range: {e}")
+
def write_file(path: Path, content: str):
"""Write (overwrite) entire file contents."""
try:
@@ -96,9 +144,18 @@ def write_file(path: Path, content: str):
except Exception as e:
raise ValueError(f"Failed to write file: {e}")
-def view_path(path_obj: Path) -> str:
- """View the entire file contents or directory listing."""
+def view_path(path_obj: Path, view_range: Optional[List[int]] = None) -> str:
+ """
+ View the file contents (optionally within a range) or directory listing.
+
+ Args:
+ path_obj: Path object for the file or directory
+ view_range: Optional [start, end] line numbers for file viewing
+ """
if path_obj.is_dir():
+ if view_range is not None:
+ raise ValueError("view_range is not supported for directory listings")
+
# For directories: list non-hidden files up to 2 levels deep
try:
result = subprocess.run(
@@ -115,14 +172,14 @@ def view_path(path_obj: Path) -> str:
except Exception as e:
raise ValueError(f"Failed to list directory: {e}")
- # If it’s a file, show the entire file with line numbers
- content = read_file(path_obj)
- return format_output(content, str(path_obj))
+ # If it’s a file, show the file content (with optional line range)
+ content, start_line = read_file_range(path_obj, view_range)
+ return format_output(content, str(path_obj), start_line)
-def tool_function(command: str, path: str, file_text: str = None) -> str:
+def tool_function(command: str, path: str, file_text: str = None, view_range: Optional[List[int]] = None) -> str:
"""
Main tool function that handles:
- - ’view’ : View the entire file or directory listing
+ - ’view’ : View file or directory listing, optionally within line range for files
- ’create’: Create a new file with the given file_text
- ’edit’ : Overwrite an existing file with file_text
"""
@@ -130,7 +187,7 @@ def tool_function(command: str, path: str, file_text: str = None) -> str:
path_obj = validate_path(path, command)
if command == "view":
- return view_path(path_obj)
+ return view_path(path_obj, view_range)
elif command == "create":
if file_text is None:
@@ -152,4 +209,4 @@ def tool_function(command: str, path: str, file_text: str = None) -> str:
if __name__ == "__main__":
# Example usage
- print(tool_function("view", "/home/ubuntu/xx/dgm/coding_agent.py"))
+ print(tool_function("view", "/home/ubuntu/xx/dgm/coding_agent.py"))
\ No newline at end of file
diff --git a/tests/test_tools/test_edit.py b/tests/test_tools/test_edit.py
new file mode 100644
index 0000000..04f535b
--- /dev/null
+++ b/tests/test_tools/test_edit.py
@@ -0,0 +1,54 @@
+import pytest
+from pathlib import Path
+from tools.edit import tool_function
+
+def test_view_line_range(tmp_path):
+ # Create a test file
+ test_file = tmp_path / "test.txt"
+ test_content = "line1\nline2\nline3\nline4\nline5\n"
+ test_file.write_text(test_content)
+
+ # Test viewing specific line range
+ result = tool_function("view", str(test_file), view_range=[2, 4])
+ assert "line2" in result
+ assert "line3" in result
+ assert "line4" in result
+ assert "line1" not in result
+ assert "line5" not in result
+ assert " 2\t" in result # Correct line numbering
+
+ # Test viewing from start to middle
+ result = tool_function("view", str(test_file), view_range=[1, 3])
+ assert "line1" in result
+ assert "line2" in result
+ assert "line3" in result
+ assert "line4" not in result
+ assert " 1\t" in result
+
+ # Test viewing from middle to end with -1
+ result = tool_function("view", str(test_file), view_range=[3, -1])
+ assert "line1" not in result
+ assert "line2" not in result
+ assert "line3" in result
+ assert "line4" in result
+ assert "line5" in result
+ assert " 3\t" in result
+
+def test_view_range_validation(tmp_path):
+ # Create a test file
+ test_file = tmp_path / "test.txt"
+ test_content = "line1\nline2\nline3\n"
+ test_file.write_text(test_content)
+
+ # Test invalid start line
+ result = tool_function("view", str(test_file), view_range=[0, 2])
+ assert "Failed to read file range: Start line must be >= 1" in result
+
+ # Test invalid range (end < start)
+ result = tool_function("view", str(test_file), view_range=[2, 1])
+ assert "Failed to read file range: End line must be >= start line or -1" in result
+
+def test_view_range_with_directory(tmp_path):
+ # Test that view_range is rejected for directories
+ result = tool_function("view", str(tmp_path), view_range=[1, 10])
+ assert "Error: view_range is not supported for directory listings" in result
\ No newline at end of file+
[⬇](data:text/plain;base64,ZGlmZiAtLWdpdCBhL3Rvb2xzL2VkaXQucHkgYi90b29scy9lZGl0LnB5CmluZGV4IDE2YWU1MjEuLjc1N2Y1YzIgMTAwNjQ0Ci0tLSBhL3Rvb2xzL2VkaXQucHkKKysrIGIvdG9vbHMvZWRpdC5weQpAQCAtMTEsMjEgKzExLDIxIEBAIGRlZiB0b29sX2luZm8oKToKICogSWYgYHBhdGhgIGlzIGEgZGlyZWN0b3J5LCBgdmlld2AgbGlzdHMgbm9uLWhpZGRlbiBmaWxlcyBhbmQgZGlyZWN0b3JpZXMgdXAgdG8gMiBsZXZlbHMgZGVlcC5cbgogKiBUaGUgYGNyZWF0ZWAgY29tbWFuZCBjYW5ub3QgYmUgdXNlZCBpZiB0aGUgc3BlY2lmaWVkIGBwYXRoYCBhbHJlYWR5IGV4aXN0cyBhcyBhIGZpbGUuXG4KICogSWYgYSBgY29tbWFuZGAgZ2VuZXJhdGVzIGEgbG9uZyBvdXRwdXQsIGl0IHdpbGwgYmUgdHJ1bmNhdGVkIGFuZCBtYXJrZWQgd2l0aCBgPHJlc3BvbnNlIGNsaXBwZWQ+YC5cbgotKiBUaGUgYGVkaXRgIGNvbW1hbmQgb3ZlcndyaXRlcyB0aGUgZW50aXJlIGZpbGUgd2l0aCB0aGUgcHJvdmlkZWQgYGZpbGVfdGV4dGAuIiIiLAorKiBUaGUgYHN0cl9yZXBsYWNlYCBjb21tYW5kIHJlcGxhY2VzIGEgdW5pcXVlIG9jY3VycmVuY2Ugb2Ygb2xkX3N0ciB3aXRoIG5ld19zdHIsIGZhaWxpbmcgaWYgb2xkX3N0ciBpcyBub3QgZm91bmQgb3IgYXBwZWFycyBtdWx0aXBsZSB0aW1lcy4iIiIsCiAgICAgICAgICJpbnB1dF9zY2hlbWEiOiB7CiAgICAgICAgICAgICAidHlwZSI6ICJvYmplY3QiLAogICAgICAgICAgICAgInByb3BlcnRpZXMiOiB7CiAgICAgICAgICAgICAgICAgImNvbW1hbmQiOiB7CiAgICAgICAgICAgICAgICAgICAgICJ0eXBlIjogInN0cmluZyIsCi0gICAgICAgICAgICAgICAgICAgICJlbnVtIjogWyJ2aWV3IiwgImNyZWF0ZSIsICJlZGl0Il0sCi0gICAgICAgICAgICAgICAgICAgICJkZXNjcmlwdGlvbiI6ICJUaGUgY29tbWFuZCB0byBydW46IGB2aWV3YCwgYGNyZWF0ZWAsIG9yIGBlZGl0YC4iCisgICAgICAgICAgICAgICAgICAgICJlbnVtIjogWyJ2aWV3IiwgImNyZWF0ZSIsICJzdHJfcmVwbGFjZSJdLAorICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiVGhlIGNvbW1hbmQgdG8gcnVuOiBgdmlld2AsIGBjcmVhdGVgLCBvciBgc3RyX3JlcGxhY2VgLiIKICAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICAgICAgICJwYXRoIjogewogICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiQWJzb2x1dGUgcGF0aCB0byBmaWxlIG9yIGRpcmVjdG9yeSwgZS5nLiBgL3JlcG8vZmlsZS5weWAgb3IgYC9yZXBvYC4iLAogICAgICAgICAgICAgICAgICAgICAidHlwZSI6ICJzdHJpbmciCiAgICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICAiZmlsZV90ZXh0IjogewotICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiUmVxdWlyZWQgcGFyYW1ldGVyIG9mIGBjcmVhdGVgIG9yIGBlZGl0YCBjb21tYW5kLCBjb250YWluaW5nIHRoZSBjb250ZW50IGZvciB0aGUgZW50aXJlIGZpbGUuIiwKKyAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIlJlcXVpcmVkIHBhcmFtZXRlciBvZiBgY3JlYXRlYCBjb21tYW5kLCBjb250YWluaW5nIHRoZSBjb250ZW50IGZvciB0aGUgZW50aXJlIGZpbGUuIiwKICAgICAgICAgICAgICAgICAgICAgInR5cGUiOiAic3RyaW5nIgogICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICAgICAgInZpZXdfcmFuZ2UiOiB7CkBAIC0zNCw2ICszNCwxNCBAQCBkZWYgdG9vbF9pbmZvKCk6CiAgICAgICAgICAgICAgICAgICAgICJpdGVtcyI6IHsidHlwZSI6ICJpbnRlZ2VyIn0sCiAgICAgICAgICAgICAgICAgICAgICJtaW5JdGVtcyI6IDIsCiAgICAgICAgICAgICAgICAgICAgICJtYXhJdGVtcyI6IDIKKyAgICAgICAgICAgICAgICB9LAorICAgICAgICAgICAgICAgICJvbGRfc3RyIjogeworICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiUmVxdWlyZWQgcGFyYW1ldGVyIG9mIGBzdHJfcmVwbGFjZWAgY29tbWFuZCwgY29udGFpbmluZyB0aGUgZXhhY3QgdGV4dCB0byBmaW5kIGFuZCByZXBsYWNlLiIsCisgICAgICAgICAgICAgICAgICAgICJ0eXBlIjogInN0cmluZyIKKyAgICAgICAgICAgICAgICB9LAorICAgICAgICAgICAgICAgICJuZXdfc3RyIjogeworICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiUmVxdWlyZWQgcGFyYW1ldGVyIG9mIGBzdHJfcmVwbGFjZWAgY29tbWFuZCwgY29udGFpbmluZyB0aGUgbmV3IHRleHQgdG8gcmVwbGFjZSBvbGRfc3RyIHdpdGguIiwKKyAgICAgICAgICAgICAgICAgICAgInR5cGUiOiAic3RyaW5nIgogICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICAicmVxdWlyZWQiOiBbImNvbW1hbmQiLCAicGF0aCJdCkBAIC01MSw3ICs1OSw3IEBAIGRlZiB2YWxpZGF0ZV9wYXRoKHBhdGg6IHN0ciwgY29tbWFuZDogc3RyKSAtPiBQYXRoOgogICAgIFZhbGlkYXRlIHRoZSBmaWxlIHBhdGggZm9yIGVhY2ggY29tbWFuZDoKICAgICAgIC0gJ3ZpZXcnOiBwYXRoIG1heSBiZSBhIGZpbGUgb3IgZGlyZWN0b3J5OyBtdXN0IGV4aXN0LgogICAgICAgLSAnY3JlYXRlJzogcGF0aCBtdXN0IG5vdCBleGlzdCAoZm9yIG5ldyBmaWxlIGNyZWF0aW9uKS4KLSAgICAgIC0gJ2VkaXQnOiBwYXRoIG11c3QgZXhpc3QgKGZvciBvdmVyd3JpdGluZykuCisgICAgICAtICdzdHJfcmVwbGFjZSc6IHBhdGggbXVzdCBleGlzdCBhbmQgYmUgYSBmaWxlLgogICAgICIiIgogICAgIHBhdGhfb2JqID0gUGF0aChwYXRoKQoKQEAgLTY5LDcgKzc3LDcgQEAgZGVmIHZhbGlkYXRlX3BhdGgocGF0aDogc3RyLCBjb21tYW5kOiBzdHIpIC0+IFBhdGg6CiAgICAgICAgICMgUGF0aCBtdXN0IG5vdCBleGlzdAogICAgICAgICBpZiBwYXRoX29iai5leGlzdHMoKToKICAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJDYW5ub3QgY3JlYXRlIG5ldyBmaWxlOyB7cGF0aH0gYWxyZWFkeSBleGlzdHMuIikKLSAgICBlbGlmIGNvbW1hbmQgPT0gImVkaXQiOgorICAgIGVsaWYgY29tbWFuZCA9PSAic3RyX3JlcGxhY2UiOgogICAgICAgICAjIFBhdGggbXVzdCBleGlzdCBhbmQgbXVzdCBiZSBhIGZpbGUKICAgICAgICAgaWYgbm90IHBhdGhfb2JqLmV4aXN0cygpOgogICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIlRoZSBmaWxlIHtwYXRofSBkb2VzIG5vdCBleGlzdC4iKQpAQCAtMTQ0LDYgKzE1MiwyOCBAQCBkZWYgd3JpdGVfZmlsZShwYXRoOiBQYXRoLCBjb250ZW50OiBzdHIpOgogICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIkZhaWxlZCB0byB3cml0ZSBmaWxlOiB7ZX0iKQoKK2RlZiBzdHJfcmVwbGFjZV9pbl9maWxlKHBhdGg6IFBhdGgsIG9sZF9zdHI6IHN0ciwgbmV3X3N0cjogc3RyKSAtPiBzdHI6CisgICAgIiIiCisgICAgUmVwbGFjZSBhbiBleGFjdCBvY2N1cnJlbmNlIG9mIG9sZF9zdHIgd2l0aCBuZXdfc3RyIGluIHRoZSBmaWxlLgorICAgIE9ubHkgcGVyZm9ybXMgdGhlIHJlcGxhY2VtZW50IGlmIG9sZF9zdHIgb2NjdXJzIGV4YWN0bHkgb25jZS4KKyAgICBSZXR1cm5zIGEgbWVzc2FnZSBpbmRpY2F0aW5nIHN1Y2Nlc3Mgb3IgZmFpbHVyZS4KKyAgICAiIiIKKyAgICB0cnk6CisgICAgICAgIGNvbnRlbnQgPSByZWFkX2ZpbGUocGF0aCkKKyAgICAgICAgb2NjdXJyZW5jZXMgPSBjb250ZW50LmNvdW50KG9sZF9zdHIpCisKKyAgICAgICAgaWYgb2NjdXJyZW5jZXMgPT0gMDoKKyAgICAgICAgICAgIHJldHVybiBmIkVycm9yOiBDb3VsZCBub3QgZmluZCB0aGUgZXhhY3QgdGV4dCB0byByZXBsYWNlIGluIHtwYXRofSIKKyAgICAgICAgZWxpZiBvY2N1cnJlbmNlcyA+IDE6CisgICAgICAgICAgICByZXR1cm4gZiJFcnJvcjogRm91bmQgbXVsdGlwbGUgKHtvY2N1cnJlbmNlc30pIG9jY3VycmVuY2VzIG9mIHRoZSB0ZXh0IGluIHtwYXRofS4gTXVzdCBiZSB1bmlxdWUuIgorICAgICAgICBlbHNlOgorICAgICAgICAgICAgbmV3X2NvbnRlbnQgPSBjb250ZW50LnJlcGxhY2Uob2xkX3N0ciwgbmV3X3N0cikKKyAgICAgICAgICAgIHdyaXRlX2ZpbGUocGF0aCwgbmV3X2NvbnRlbnQpCisgICAgICAgICAgICByZXR1cm4gZiJTdWNjZXNzZnVsbHkgcmVwbGFjZWQgdGV4dCBpbiB7cGF0aH0iCisKKyAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CisgICAgICAgIHJldHVybiBmIkVycm9yIGR1cmluZyBzdHJpbmcgcmVwbGFjZW1lbnQ6IHtlfSIKKwogZGVmIHZpZXdfcGF0aChwYXRoX29iajogUGF0aCwgdmlld19yYW5nZTogT3B0aW9uYWxbTGlzdFtpbnRdXSA9IE5vbmUpIC0+IHN0cjoKICAgICAiIiIKICAgICBWaWV3IHRoZSBmaWxlIGNvbnRlbnRzIChvcHRpb25hbGx5IHdpdGhpbiBhIHJhbmdlKSBvciBkaXJlY3RvcnkgbGlzdGluZy4KQEAgLTE3NiwxMiArMjA2LDEzIEBAIGRlZiB2aWV3X3BhdGgocGF0aF9vYmo6IFBhdGgsIHZpZXdfcmFuZ2U6IE9wdGlvbmFsW0xpc3RbaW50XV0gPSBOb25lKSAtPiBzdHI6CiAgICAgY29udGVudCwgc3RhcnRfbGluZSA9IHJlYWRfZmlsZV9yYW5nZShwYXRoX29iaiwgdmlld19yYW5nZSkKICAgICByZXR1cm4gZm9ybWF0X291dHB1dChjb250ZW50LCBzdHIocGF0aF9vYmopLCBzdGFydF9saW5lKQoKLWRlZiB0b29sX2Z1bmN0aW9uKGNvbW1hbmQ6IHN0ciwgcGF0aDogc3RyLCBmaWxlX3RleHQ6IHN0ciA9IE5vbmUsIHZpZXdfcmFuZ2U6IE9wdGlvbmFsW0xpc3RbaW50XV0gPSBOb25lKSAtPiBzdHI6CitkZWYgdG9vbF9mdW5jdGlvbihjb21tYW5kOiBzdHIsIHBhdGg6IHN0ciwgZmlsZV90ZXh0OiBzdHIgPSBOb25lLCB2aWV3X3JhbmdlOiBPcHRpb25hbFtMaXN0W2ludF1dID0gTm9uZSwKKyAgICAgICAgICAgICAgICAgb2xkX3N0cjogc3RyID0gTm9uZSwgbmV3X3N0cjogc3RyID0gTm9uZSkgLT4gc3RyOgogICAgICIiIgogICAgIE1haW4gdG9vbCBmdW5jdGlvbiB0aGF0IGhhbmRsZXM6Ci0gICAgICAtICd2aWV3JyAgOiBWaWV3IGZpbGUgb3IgZGlyZWN0b3J5IGxpc3RpbmcsIG9wdGlvbmFsbHkgd2l0aGluIGxpbmUgcmFuZ2UgZm9yIGZpbGVzCi0gICAgICAtICdjcmVhdGUnOiBDcmVhdGUgYSBuZXcgZmlsZSB3aXRoIHRoZSBnaXZlbiBmaWxlX3RleHQKLSAgICAgIC0gJ2VkaXQnICA6IE92ZXJ3cml0ZSBhbiBleGlzdGluZyBmaWxlIHdpdGggZmlsZV90ZXh0CisgICAgICAtICd2aWV3JyAgICAgICA6IFZpZXcgZmlsZSBvciBkaXJlY3RvcnkgbGlzdGluZywgb3B0aW9uYWxseSB3aXRoaW4gbGluZSByYW5nZSBmb3IgZmlsZXMKKyAgICAgIC0gJ2NyZWF0ZScgICAgIDogQ3JlYXRlIGEgbmV3IGZpbGUgd2l0aCB0aGUgZ2l2ZW4gZmlsZV90ZXh0CisgICAgICAtICdzdHJfcmVwbGFjZSc6IFJlcGxhY2UgZXhhY3Qgb2NjdXJyZW5jZSBvZiBvbGRfc3RyIHdpdGggbmV3X3N0ciBpbiB0aGUgZmlsZQogICAgICIiIgogICAgIHRyeToKICAgICAgICAgcGF0aF9vYmogPSB2YWxpZGF0ZV9wYXRoKHBhdGgsIGNvbW1hbmQpCkBAIC0xOTUsMTEgKzIyNiwxMCBAQCBkZWYgdG9vbF9mdW5jdGlvbihjb21tYW5kOiBzdHIsIHBhdGg6IHN0ciwgZmlsZV90ZXh0OiBzdHIgPSBOb25lLCB2aWV3X3JhbmdlOiBPcAogICAgICAgICAgICAgd3JpdGVfZmlsZShwYXRoX29iaiwgZmlsZV90ZXh0KQogICAgICAgICAgICAgcmV0dXJuIGYiRmlsZSBjcmVhdGVkIHN1Y2Nlc3NmdWxseSBhdDoge3BhdGh9IgoKLSAgICAgICAgZWxpZiBjb21tYW5kID09ICJlZGl0IjoKLSAgICAgICAgICAgIGlmIGZpbGVfdGV4dCBpcyBOb25lOgotICAgICAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoIk1pc3NpbmcgcmVxdWlyZWQgYGZpbGVfdGV4dGAgZm9yICdlZGl0JyBjb21tYW5kLiIpCi0gICAgICAgICAgICB3cml0ZV9maWxlKHBhdGhfb2JqLCBmaWxlX3RleHQpCi0gICAgICAgICAgICByZXR1cm4gZiJGaWxlIGF0IHtwYXRofSBoYXMgYmVlbiBvdmVyd3JpdHRlbiB3aXRoIG5ldyBjb250ZW50LiIKKyAgICAgICAgZWxpZiBjb21tYW5kID09ICJzdHJfcmVwbGFjZSI6CisgICAgICAgICAgICBpZiBvbGRfc3RyIGlzIE5vbmUgb3IgbmV3X3N0ciBpcyBOb25lOgorICAgICAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoIk1pc3NpbmcgcmVxdWlyZWQgYG9sZF9zdHJgIGFuZC9vciBgbmV3X3N0cmAgZm9yICdzdHJfcmVwbGFjZScgY29tbWFuZC4iKQorICAgICAgICAgICAgcmV0dXJuIHN0cl9yZXBsYWNlX2luX2ZpbGUocGF0aF9vYmosIG9sZF9zdHIsIG5ld19zdHIpCgogICAgICAgICBlbHNlOgogICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIlVua25vd24gY29tbWFuZDoge2NvbW1hbmR9IikKZGlmZiAtLWdpdCBhL3Rlc3RzL19faW5pdF9fLnB5IGIvdGVzdHMvX19pbml0X18ucHkKbmV3IGZpbGUgbW9kZSAxMDA2NDQKaW5kZXggMDAwMDAwMC4uZTY5ZGUyOQpkaWZmIC0tZ2l0IGEvdGVzdHMvdGVzdF90b29scy5weSBiL3Rlc3RzL3Rlc3RfdG9vbHMucHkKbmV3IGZpbGUgbW9kZSAxMDA2NDQKaW5kZXggMDAwMDAwMC4uYzdmMjQyZgotLS0gL2Rldi9udWxsCisrKyBiL3Rlc3RzL3Rlc3RfdG9vbHMucHkKQEAgLTAsMCArMSw2NSBAQAoraW1wb3J0IHB5dGVzdAorZnJvbSBwYXRobGliIGltcG9ydCBQYXRoCitmcm9tIHRvb2xzLmVkaXQgaW1wb3J0IHRvb2xfZnVuY3Rpb24KKworIyBUZXN0IGZpeHR1cmVzCitAcHl0ZXN0LmZpeHR1cmUKK2RlZiB0ZW1wX2ZpbGUodG1wX3BhdGgpOgorICAgIGZpbGVfcGF0aCA9IHRtcF9wYXRoIC8gInRlc3QudHh0IgorICAgIGNvbnRlbnQgPSAibGluZSAxXG5saW5lIDJcbmxpbmUgM1xuIgorICAgIGZpbGVfcGF0aC53cml0ZV90ZXh0KGNvbnRlbnQpCisgICAgcmV0dXJuIHN0cihmaWxlX3BhdGgpCisKK2RlZiB0ZXN0X3N0cl9yZXBsYWNlX3N1Y2Nlc3ModGVtcF9maWxlKToKKyAgICAjIFRlc3Qgc3VjY2Vzc2Z1bCByZXBsYWNlbWVudAorICAgIHJlc3VsdCA9IHRvb2xfZnVuY3Rpb24oCisgICAgICAgIGNvbW1hbmQ9InN0cl9yZXBsYWNlIiwKKyAgICAgICAgcGF0aD10ZW1wX2ZpbGUsCisgICAgICAgIG9sZF9zdHI9ImxpbmUgMlxuIiwKKyAgICAgICAgbmV3X3N0cj0icmVwbGFjZWQgbGluZVxuIgorICAgICkKKyAgICBhc3NlcnQgIlN1Y2Nlc3NmdWxseSByZXBsYWNlZCIgaW4gcmVzdWx0CisgICAgYXNzZXJ0IFBhdGgodGVtcF9maWxlKS5yZWFkX3RleHQoKSA9PSAibGluZSAxXG5yZXBsYWNlZCBsaW5lXG5saW5lIDNcbiIKKworZGVmIHRlc3Rfc3RyX3JlcGxhY2Vfbm90X2ZvdW5kKHRlbXBfZmlsZSk6CisgICAgIyBUZXN0IHdoZW4gb2xkX3N0ciBpcyBub3QgZm91bmQKKyAgICByZXN1bHQgPSB0b29sX2Z1bmN0aW9uKAorICAgICAgICBjb21tYW5kPSJzdHJfcmVwbGFjZSIsCisgICAgICAgIHBhdGg9dGVtcF9maWxlLAorICAgICAgICBvbGRfc3RyPSJub25leGlzdGVudCIsCisgICAgICAgIG5ld19zdHI9InNvbWV0aGluZyIKKyAgICApCisgICAgYXNzZXJ0ICJDb3VsZCBub3QgZmluZCIgaW4gcmVzdWx0CisgICAgIyBPcmlnaW5hbCBmaWxlIHNob3VsZCBiZSB1bmNoYW5nZWQKKyAgICBhc3NlcnQgUGF0aCh0ZW1wX2ZpbGUpLnJlYWRfdGV4dCgpID09ICJsaW5lIDFcbmxpbmUgMlxubGluZSAzXG4iCisKK2RlZiB0ZXN0X3N0cl9yZXBsYWNlX211bHRpcGxlX29jY3VycmVuY2VzKHRlbXBfZmlsZSk6CisgICAgIyBGaXJzdCBjcmVhdGUgYSBmaWxlIHdpdGggbXVsdGlwbGUgb2NjdXJyZW5jZXMKKyAgICBQYXRoKHRlbXBfZmlsZSkud3JpdGVfdGV4dCgic2FtZVxuc2FtZVxuc2FtZVxuIikKKyAgICByZXN1bHQgPSB0b29sX2Z1bmN0aW9uKAorICAgICAgICBjb21tYW5kPSJzdHJfcmVwbGFjZSIsCisgICAgICAgIHBhdGg9dGVtcF9maWxlLAorICAgICAgICBvbGRfc3RyPSJzYW1lXG4iLAorICAgICAgICBuZXdfc3RyPSJkaWZmZXJlbnRcbiIKKyAgICApCisgICAgYXNzZXJ0ICJtdWx0aXBsZSIgaW4gcmVzdWx0CisgICAgIyBPcmlnaW5hbCBmaWxlIHNob3VsZCBiZSB1bmNoYW5nZWQKKyAgICBhc3NlcnQgUGF0aCh0ZW1wX2ZpbGUpLnJlYWRfdGV4dCgpID09ICJzYW1lXG5zYW1lXG5zYW1lXG4iCisKK2RlZiB0ZXN0X3N0cl9yZXBsYWNlX21pc3NpbmdfcGFyYW1zKHRlbXBfZmlsZSk6CisgICAgIyBUZXN0IG1pc3NpbmcgcGFyYW1ldGVycworICAgIHJlc3VsdCA9IHRvb2xfZnVuY3Rpb24oCisgICAgICAgIGNvbW1hbmQ9InN0cl9yZXBsYWNlIiwKKyAgICAgICAgcGF0aD10ZW1wX2ZpbGUsCisgICAgKQorICAgIGFzc2VydCAiTWlzc2luZyByZXF1aXJlZCIgaW4gcmVzdWx0CisKK2RlZiB0ZXN0X3N0cl9yZXBsYWNlX2ludmFsaWRfcGF0aCgpOgorICAgICMgVGVzdCB3aXRoIG5vbi1leGlzdGVudCBmaWxlCisgICAgcmVzdWx0ID0gdG9vbF9mdW5jdGlvbigKKyAgICAgICAgY29tbWFuZD0ic3RyX3JlcGxhY2UiLAorICAgICAgICBwYXRoPSIvbm9uZXhpc3RlbnQvcGF0aCIsCisgICAgICAgIG9sZF9zdHI9Im9sZCIsCisgICAgICAgIG5ld19zdHI9Im5ldyIKKyAgICApCisgICAgYXNzZXJ0ICJkb2VzIG5vdCBleGlzdCIgaW4gcmVzdWx0ClwgTm8gbmV3bGluZSBhdCBlbmQgb2YgZmlsZQ==)
diff --git a/tools/edit.py b/tools/edit.py
index 16ae521..757f5c2 100644
--- a/tools/edit.py
+++ b/tools/edit.py
@@ -11,21 +11,21 @@ def tool_info():
* If ‘path‘ is a directory, ‘view‘ lists non-hidden files and directories up to 2 levels deep.\n
* The ‘create‘ command cannot be used if the specified ‘path‘ already exists as a file.\n
* If a ‘command‘ generates a long output, it will be truncated and marked with ‘<response clipped>‘.\n
-* The ‘edit‘ command overwrites the entire file with the provided ‘file_text‘.""",
+* The ‘str_replace‘ command replaces a unique occurrence of old_str with new_str, failing if old_str is not found or appears multiple times.""",
"input_schema": {
"type": "object",
"properties": {
"command": {
"type": "string",
- "enum": ["view", "create", "edit"],
- "description": "The command to run: ‘view‘, ‘create‘, or ‘edit‘."
+ "enum": ["view", "create", "str_replace"],
+ "description": "The command to run: ‘view‘, ‘create‘, or ‘str_replace‘."
},
"path": {
"description": "Absolute path to file or directory, e.g. ‘/repo/file.py‘ or ‘/repo‘.",
"type": "string"
},
"file_text": {
- "description": "Required parameter of ‘create‘ or ‘edit‘ command, containing the content for the entire file.",
+ "description": "Required parameter of ‘create‘ command, containing the content for the entire file.",
"type": "string"
},
"view_range": {
@@ -34,6 +34,14 @@ def tool_info():
"items": {"type": "integer"},
"minItems": 2,
"maxItems": 2
+ },
+ "old_str": {
+ "description": "Required parameter of ‘str_replace‘ command, containing the exact text to find and replace.",
+ "type": "string"
+ },
+ "new_str": {
+ "description": "Required parameter of ‘str_replace‘ command, containing the new text to replace old_str with.",
+ "type": "string"
}
},
"required": ["command", "path"]
@@ -51,7 +59,7 @@ def validate_path(path: str, command: str) -> Path:
Validate the file path for each command:
- ’view’: path may be a file or directory; must exist.
- ’create’: path must not exist (for new file creation).
- - ’edit’: path must exist (for overwriting).
+ - ’str_replace’: path must exist and be a file.
"""
path_obj = Path(path)
@@ -69,7 +77,7 @@ def validate_path(path: str, command: str) -> Path:
# Path must not exist
if path_obj.exists():
raise ValueError(f"Cannot create new file; {path} already exists.")
- elif command == "edit":
+ elif command == "str_replace":
# Path must exist and must be a file
if not path_obj.exists():
raise ValueError(f"The file {path} does not exist.")
@@ -144,6 +152,28 @@ def write_file(path: Path, content: str):
except Exception as e:
raise ValueError(f"Failed to write file: {e}")
+def str_replace_in_file(path: Path, old_str: str, new_str: str) -> str:
+ """
+ Replace an exact occurrence of old_str with new_str in the file.
+ Only performs the replacement if old_str occurs exactly once.
+ Returns a message indicating success or failure.
+ """
+ try:
+ content = read_file(path)
+ occurrences = content.count(old_str)
+
+ if occurrences == 0:
+ return f"Error: Could not find the exact text to replace in {path}"
+ elif occurrences > 1:
+ return f"Error: Found multiple ({occurrences}) occurrences of the text in {path}. Must be unique."
+ else:
+ new_content = content.replace(old_str, new_str)
+ write_file(path, new_content)
+ return f"Successfully replaced text in {path}"
+
+ except Exception as e:
+ return f"Error during string replacement: {e}"
+
def view_path(path_obj: Path, view_range: Optional[List[int]] = None) -> str:
"""
View the file contents (optionally within a range) or directory listing.
@@ -176,12 +206,13 @@ def view_path(path_obj: Path, view_range: Optional[List[int]] = None) -> str:
content, start_line = read_file_range(path_obj, view_range)
return format_output(content, str(path_obj), start_line)
-def tool_function(command: str, path: str, file_text: str = None, view_range: Optional[List[int]] = None) -> str:
+def tool_function(command: str, path: str, file_text: str = None, view_range: Optional[List[int]] = None,
+ old_str: str = None, new_str: str = None) -> str:
"""
Main tool function that handles:
- - ’view’ : View file or directory listing, optionally within line range for files
- - ’create’: Create a new file with the given file_text
- - ’edit’ : Overwrite an existing file with file_text
+ - ’view’ : View file or directory listing, optionally within line range for files
+ - ’create’ : Create a new file with the given file_text
+ - ’str_replace’: Replace exact occurrence of old_str with new_str in the file
"""
try:
path_obj = validate_path(path, command)
@@ -195,11 +226,10 @@ def tool_function(command: str, path: str, file_text: str = None, view_range: Op
write_file(path_obj, file_text)
return f"File created successfully at: {path}"
- elif command == "edit":
- if file_text is None:
- raise ValueError("Missing required ‘file_text‘ for ’edit’ command.")
- write_file(path_obj, file_text)
- return f"File at {path} has been overwritten with new content."
+ elif command == "str_replace":
+ if old_str is None or new_str is None:
+ raise ValueError("Missing required ‘old_str‘ and/or ‘new_str‘ for ’str_replace’ command.")
+ return str_replace_in_file(path_obj, old_str, new_str)
else:
raise ValueError(f"Unknown command: {command}")
diff --git a/tests/__init__.py b/tests/__init__.py
new file mode 100644
index 0000000..e69de29
diff --git a/tests/test_tools.py b/tests/test_tools.py
new file mode 100644
index 0000000..c7f242f
--- /dev/null
+++ b/tests/test_tools.py
@@ -0,0 +1,65 @@
+import pytest
+from pathlib import Path
+from tools.edit import tool_function
+
+# Test fixtures
+@pytest.fixture
+def temp_file(tmp_path):
+ file_path = tmp_path / "test.txt"
+ content = "line 1\nline 2\nline 3\n"
+ file_path.write_text(content)
+ return str(file_path)
+
+def test_str_replace_success(temp_file):
+ # Test successful replacement
+ result = tool_function(
+ command="str_replace",
+ path=temp_file,
+ old_str="line 2\n",
+ new_str="replaced line\n"
+ )
+ assert "Successfully replaced" in result
+ assert Path(temp_file).read_text() == "line 1\nreplaced line\nline 3\n"
+
+def test_str_replace_not_found(temp_file):
+ # Test when old_str is not found
+ result = tool_function(
+ command="str_replace",
+ path=temp_file,
+ old_str="nonexistent",
+ new_str="something"
+ )
+ assert "Could not find" in result
+ # Original file should be unchanged
+ assert Path(temp_file).read_text() == "line 1\nline 2\nline 3\n"
+
+def test_str_replace_multiple_occurrences(temp_file):
+ # First create a file with multiple occurrences
+ Path(temp_file).write_text("same\nsame\nsame\n")
+ result = tool_function(
+ command="str_replace",
+ path=temp_file,
+ old_str="same\n",
+ new_str="different\n"
+ )
+ assert "multiple" in result
+ # Original file should be unchanged
+ assert Path(temp_file).read_text() == "same\nsame\nsame\n"
+
+def test_str_replace_missing_params(temp_file):
+ # Test missing parameters
+ result = tool_function(
+ command="str_replace",
+ path=temp_file,
+ )
+ assert "Missing required" in result
+
+def test_str_replace_invalid_path():
+ # Test with non-existent file
+ result = tool_function(
+ command="str_replace",
+ path="/nonexistent/path",
+ old_str="old",
+ new_str="new"
+ )
+ assert "does not exist" in result
\ No newline at end of file+
[⬇](data:text/plain;base64,ZGlmZiAtLWdpdCBhL2xsbV93aXRodG9vbHMucHkgYi9sbG1fd2l0aHRvb2xzLnB5CmluZGV4IGQxMzk0YmIuLjZjYzM2MDQgMTAwNjQ0Ci0tLSBhL2xsbV93aXRodG9vbHMucHkKKysrIGIvbGxtX3dpdGh0b29scy5weQpAQCAtMjksNyArMjksNyBAQCBkZWYgcHJvY2Vzc190b29sX2NhbGwodG9vbHNfZGljdCwgdG9vbF9uYW1lLCB0b29sX2lucHV0KToKICkKIGRlZiBnZXRfcmVzcG9uc2Vfd2l0aHRvb2xzKAogICAgIGNsaWVudCwgbW9kZWwsIG1lc3NhZ2VzLCB0b29scywgdG9vbF9jaG9pY2UsCi0gICAgbG9nZ2luZz1Ob25lLAorICAgIGxvZ2dpbmc9Tm9uZSwgc3lzdGVtX21lc3NhZ2U9Tm9uZSwKICk6CiAgICAgdHJ5OgogICAgICAgICBpZiAnY2xhdWRlJyBpbiBtb2RlbDoKQEAgLTUyLDEzICs1MiwzMiBAQCBkZWYgZ2V0X3Jlc3BvbnNlX3dpdGh0b29scygKICAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJVbnN1cHBvcnRlZCBtb2RlbDoge21vZGVsfSIpCiAgICAgICAgIHJldHVybiByZXNwb25zZQogICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKLSAgICAgICAgbG9nZ2luZyhmIkVycm9yIGluIGdldF9yZXNwb25zZV93aXRodG9vbHM6IHtzdHIoZSl9IikKKyAgICAgICAgZXJyb3JfbXNnID0gc3RyKGUpCisgICAgICAgIGxvZ2dpbmcoZiJFcnJvciBpbiBnZXRfcmVzcG9uc2Vfd2l0aHRvb2xzOiB7ZXJyb3JfbXNnfSIpCgogICAgICAgICAjIEhpdHRpbmcgdGhlIGNvbnRleHQgd2luZG93IGxpbWl0Ci0gICAgICAgIGlmICdJbnB1dCBpcyB0b28gbG9uZyBmb3IgcmVxdWVzdGVkIG1vZGVsJyBpbiBzdHIoZSk6Ci0gICAgICAgICAgICBwYXNzCisgICAgICAgIGlmICdJbnB1dCBpcyB0b28gbG9uZyBmb3IgcmVxdWVzdGVkIG1vZGVsJyBpbiBlcnJvcl9tc2cgb3IgJ21heGltdW0gY29udGV4dCBsZW5ndGgnIGluIGVycm9yX21zZzoKKyAgICAgICAgICAgIGlmIG5vdCBzeXN0ZW1fbWVzc2FnZToKKyAgICAgICAgICAgICAgICAjIEV4dHJhY3Qgc3lzdGVtIG1lc3NhZ2UgZnJvbSB0aGUgZmlyc3QgbWVzc2FnZSBpZiBhdmFpbGFibGUKKyAgICAgICAgICAgICAgICBzeXN0ZW1fbWVzc2FnZSA9IG1lc3NhZ2VzWzBdLmdldCgnY29udGVudCcsICcnKSBpZiBtZXNzYWdlcyBlbHNlICcnCisgICAgICAgICAgICAgICAgaWYgaXNpbnN0YW5jZShzeXN0ZW1fbWVzc2FnZSwgbGlzdCk6CisgICAgICAgICAgICAgICAgICAgIHN5c3RlbV9tZXNzYWdlID0gJyAnLmpvaW4oYmxvY2tbJ3RleHQnXSBmb3IgYmxvY2sgaW4gc3lzdGVtX21lc3NhZ2UgaWYgYmxvY2tbJ3R5cGUnXSA9PSAndGV4dCcpCisKKyAgICAgICAgICAgICMgU3VtbWFyaXplIHRoZSBjb252ZXJzYXRpb24gaGlzdG9yeQorICAgICAgICAgICAgc3VtbWFyaXplZF9tZXNzYWdlcyA9IHN1bW1hcml6ZV9tZXNzYWdlcyhjbGllbnQsIG1vZGVsLCBtZXNzYWdlcywgc3lzdGVtX21lc3NhZ2UpCisKKyAgICAgICAgICAgICMgUmV0cnkgd2l0aCBzdW1tYXJpemVkIG1lc3NhZ2VzCisgICAgICAgICAgICByZXR1cm4gZ2V0X3Jlc3BvbnNlX3dpdGh0b29scygKKyAgICAgICAgICAgICAgICBjbGllbnQ9Y2xpZW50LAorICAgICAgICAgICAgICAgIG1vZGVsPW1vZGVsLAorICAgICAgICAgICAgICAgIG1lc3NhZ2VzPXN1bW1hcml6ZWRfbWVzc2FnZXMsCisgICAgICAgICAgICAgICAgdG9vbHM9dG9vbHMsCisgICAgICAgICAgICAgICAgdG9vbF9jaG9pY2U9dG9vbF9jaG9pY2UsCisgICAgICAgICAgICAgICAgbG9nZ2luZz1sb2dnaW5nLAorICAgICAgICAgICAgICAgIHN5c3RlbV9tZXNzYWdlPXN5c3RlbV9tZXNzYWdlCisgICAgICAgICAgICApCgotICAgICAgICByYWlzZSAgIyBSZS1yYWlzZSB0aGUgZXhjZXB0aW9uIGFmdGVyIGxvZ2dpbmcKKyAgICAgICAgcmFpc2UgICMgUmUtcmFpc2Ugb3RoZXIgZXhjZXB0aW9ucwoKIGRlZiBjaGVja19mb3JfdG9vbF91c2UocmVzcG9uc2UsIG1vZGVsPScnKToKICAgICAiIiIKQEAgLTI0Nyw2ICsyNjYsNTcgQEAgZGVmIGNvbnZlcnRfbXNnX2hpc3Rvcnlfb3BlbmFpKG1zZ19oaXN0b3J5KToKCiAgICAgcmV0dXJuIG5ld19tc2dfaGlzdG9yeQoKK2RlZiBzdW1tYXJpemVfbWVzc2FnZXMoY2xpZW50LCBtb2RlbCwgbWVzc2FnZXMsIHN5c3RlbV9tZXNzYWdlKToKKyAgICAiIiIKKyAgICBDcmVhdGVzIGEgY29uZGVuc2VkIHN1bW1hcnkgb2Ygb2xkZXIgbWVzc2FnZXMgd2hpbGUgcHJlc2VydmluZyByZWNlbnQgY29udGV4dC4KKyAgICBPbmx5IHN1bW1hcml6ZXMgYXNzaXN0YW50IGFuZCB1c2VyIG1lc3NhZ2VzLCBrZWVwcyB0b29sIHJlc3VsdHMgYXMgaXMgZm9yIGFjY3VyYWN5LgorICAgICIiIgorICAgICMgS2VlcCB0aGUgbW9zdCByZWNlbnQgbWVzc2FnZXMgaW50YWN0CisgICAgcmVjZW50X21zZ3MgPSBtZXNzYWdlc1stMjpdIGlmIGxlbihtZXNzYWdlcykgPiAyIGVsc2UgbWVzc2FnZXMKKyAgICBpZiBsZW4obWVzc2FnZXMpIDw9IDI6CisgICAgICAgIHJldHVybiBtZXNzYWdlcworCisgICAgIyBQcmVwYXJlIG1lc3NhZ2VzIHRvIGJlIHN1bW1hcml6ZWQKKyAgICBtc2dzX3RvX3N1bW1hcml6ZSA9IG1lc3NhZ2VzWzotMl0KKworICAgICMgQ3JlYXRlIGEgcHJvbXB0IHRvIHN1bW1hcml6ZSB0aGUgY29udmVyc2F0aW9uCisgICAgc3VtbWFyeV9yZXF1ZXN0ID0gIlBsZWFzZSBjcmVhdGUgYSBjb25jaXNlIHN1bW1hcnkgb2YgdGhpcyBjb252ZXJzYXRpb24gdGhhdCBwcmVzZXJ2ZXMgdGhlIGtleSBjb250ZXh0IGFuZCBpbXBvcnRhbnQgZGV0YWlsczoiCisgICAgZm9yIG1zZyBpbiBtc2dzX3RvX3N1bW1hcml6ZToKKyAgICAgICAgaWYgaXNpbnN0YW5jZShtc2cuZ2V0KCdjb250ZW50JywgJycpLCBsaXN0KToKKyAgICAgICAgICAgIGNvbnRlbnQgPSAnICcuam9pbihibG9ja1sndGV4dCddIGZvciBibG9jayBpbiBtc2dbJ2NvbnRlbnQnXSBpZiBibG9ja1sndHlwZSddID09ICd0ZXh0JykKKyAgICAgICAgZWxzZToKKyAgICAgICAgICAgIGNvbnRlbnQgPSBzdHIobXNnLmdldCgnY29udGVudCcsICcnKSkKKyAgICAgICAgaWYgbXNnLmdldCgncm9sZScpIGluIFsnYXNzaXN0YW50JywgJ3VzZXInXToKKyAgICAgICAgICAgIHN1bW1hcnlfcmVxdWVzdCArPSBmIlxue21zZ1sncm9sZSddfToge2NvbnRlbnR9IgorCisgICAgdHJ5OgorICAgICAgICAjIEdldCBzdW1tYXJ5IGZyb20gdGhlIG1vZGVsCisgICAgICAgIHN1bW1hcnlfcmVzcG9uc2UsIF8gPSBnZXRfcmVzcG9uc2VfZnJvbV9sbG0oCisgICAgICAgICAgICBtc2c9c3VtbWFyeV9yZXF1ZXN0LAorICAgICAgICAgICAgY2xpZW50PWNsaWVudCwKKyAgICAgICAgICAgIG1vZGVsPW1vZGVsLAorICAgICAgICAgICAgc3lzdGVtX21lc3NhZ2U9IllvdSBhcmUgYSBzdW1tYXJpemVyLiBDcmVhdGUgYSBjb25jaXNlIGJ1dCBpbmZvcm1hdGl2ZSBzdW1tYXJ5LiIsCisgICAgICAgICAgICBwcmludF9kZWJ1Zz1GYWxzZSwKKyAgICAgICAgICAgIG1zZ19oaXN0b3J5PVtdCisgICAgICAgICkKKworICAgICAgICAjIENyZWF0ZSBuZXcgbWVzc2FnZSBoaXN0b3J5IHdpdGggdGhlIHN1bW1hcnkKKyAgICAgICAgc3VtbWFyaXplZF9oaXN0b3J5ID0gW3sKKyAgICAgICAgICAgICJyb2xlIjogInN5c3RlbSIsCisgICAgICAgICAgICAiY29udGVudCI6IFt7InR5cGUiOiAidGV4dCIsICJ0ZXh0Ijogc3lzdGVtX21lc3NhZ2V9XQorICAgICAgICB9LCB7CisgICAgICAgICAgICAicm9sZSI6ICJhc3Npc3RhbnQiLAorICAgICAgICAgICAgImNvbnRlbnQiOiBbeyJ0eXBlIjogInRleHQiLCAidGV4dCI6IGYiUHJldmlvdXMgY29udmVyc2F0aW9uIHN1bW1hcnk6IHtzdW1tYXJ5X3Jlc3BvbnNlfSJ9XQorICAgICAgICB9XQorCisgICAgICAgICMgQWRkIGJhY2sgdGhlIHJlY2VudCBtZXNzYWdlcworICAgICAgICBzdW1tYXJpemVkX2hpc3RvcnkuZXh0ZW5kKHJlY2VudF9tc2dzKQorCisgICAgICAgIHJldHVybiBzdW1tYXJpemVkX2hpc3RvcnkKKyAgICBleGNlcHQgRXhjZXB0aW9uOgorICAgICAgICAjIElmIHN1bW1hcml6YXRpb24gZmFpbHMsIHJldHVybiBvcmlnaW5hbCBtZXNzYWdlcyB3aXRoIHRoZSBtb3N0IHJlY2VudCBvbmVzCisgICAgICAgIHJldHVybiBbbWVzc2FnZXNbMF1dICsgcmVjZW50X21zZ3MKKwogZGVmIGNvbnZlcnRfbXNnX2hpc3RvcnkobXNnX2hpc3RvcnksIG1vZGVsPU5vbmUpOgogICAgICIiIgogICAgIENvbnZlcnQgbWVzc2FnZSBoaXN0b3J5IGZyb20gdGhlIG1vZGVsLXNwZWNpZmljIGZvcm1hdCB0byBhIGdlbmVyaWMgZm9ybWF0LgpAQCAtMjYzLDcgKzMzMywxNCBAQCBkZWYgY2hhdF93aXRoX2FnZW50X21hbnVhbHRvb2xzKG1zZywgbW9kZWwsIG1zZ19oaXN0b3J5PU5vbmUsIGxvZ2dpbmc9cHJpbnQpOgogICAgIGlmIG1zZ19oaXN0b3J5IGlzIE5vbmU6CiAgICAgICAgIG1zZ19oaXN0b3J5ID0gW10KICAgICBzeXN0ZW1fbWVzc2FnZSA9IGYnWW91IGFyZSBhIGNvZGluZyBhZ2VudC5cblxue2dldF90b29sdXNlX3Byb21wdCgpfScKLSAgICBuZXdfbXNnX2hpc3RvcnkgPSBtc2dfaGlzdG9yeQorICAgIG5ld19tc2dfaGlzdG9yeSA9IG1zZ19oaXN0b3J5LmNvcHkoKSBpZiBtc2dfaGlzdG9yeSBlbHNlIFtdCisKKyAgICAjIEVuc3VyZSBzeXN0ZW0gbWVzc2FnZSBpcyB0aGUgZmlyc3QgbWVzc2FnZSBpbiBoaXN0b3J5CisgICAgaWYgbm90IG5ld19tc2dfaGlzdG9yeSBvciBuZXdfbXNnX2hpc3RvcnlbMF0uZ2V0KCdyb2xlJykgIT0gJ3N5c3RlbSc6CisgICAgICAgIG5ld19tc2dfaGlzdG9yeS5pbnNlcnQoMCwgeworICAgICAgICAgICAgInJvbGUiOiAic3lzdGVtIiwKKyAgICAgICAgICAgICJjb250ZW50IjogW3sidHlwZSI6ICJ0ZXh0IiwgInRleHQiOiBzeXN0ZW1fbWVzc2FnZX1dCisgICAgICAgIH0pCgogICAgIHRyeToKICAgICAgICAgIyBMb2FkIGFsbCB0b29scw==)
diff --git a/llm_withtools.py b/llm_withtools.py
index d1394bb..6cc3604 100644
--- a/llm_withtools.py
+++ b/llm_withtools.py
@@ -29,7 +29,7 @@ def process_tool_call(tools_dict, tool_name, tool_input):
)
def get_response_withtools(
client, model, messages, tools, tool_choice,
- logging=None,
+ logging=None, system_message=None,
):
try:
if ’claude’ in model:
@@ -52,13 +52,32 @@ def get_response_withtools(
raise ValueError(f"Unsupported model: {model}")
return response
except Exception as e:
- logging(f"Error in get_response_withtools: {str(e)}")
+ error_msg = str(e)
+ logging(f"Error in get_response_withtools: {error_msg}")
# Hitting the context window limit
- if ’Input is too long for requested model’ in str(e):
- pass
+ if ’Input is too long for requested model’ in error_msg or ’maximum context length’ in error_msg:
+ if not system_message:
+ # Extract system message from the first message if available
+ system_message = messages[0].get(’content’, ’’) if messages else ’’
+ if isinstance(system_message, list):
+ system_message = ’ ’.join(block[’text’] for block in system_message if block[’type’] == ’text’)
+
+ # Summarize the conversation history
+ summarized_messages = summarize_messages(client, model, messages, system_message)
+
+ # Retry with summarized messages
+ return get_response_withtools(
+ client=client,
+ model=model,
+ messages=summarized_messages,
+ tools=tools,
+ tool_choice=tool_choice,
+ logging=logging,
+ system_message=system_message
+ )
- raise # Re-raise the exception after logging
+ raise # Re-raise other exceptions
def check_for_tool_use(response, model=’’):
"""
@@ -247,6 +266,57 @@ def convert_msg_history_openai(msg_history):
return new_msg_history
+def summarize_messages(client, model, messages, system_message):
+ """
+ Creates a condensed summary of older messages while preserving recent context.
+ Only summarizes assistant and user messages, keeps tool results as is for accuracy.
+ """
+ # Keep the most recent messages intact
+ recent_msgs = messages[-2:] if len(messages) > 2 else messages
+ if len(messages) <= 2:
+ return messages
+
+ # Prepare messages to be summarized
+ msgs_to_summarize = messages[:-2]
+
+ # Create a prompt to summarize the conversation
+ summary_request = "Please create a concise summary of this conversation that preserves the key context and important details:"
+ for msg in msgs_to_summarize:
+ if isinstance(msg.get(’content’, ’’), list):
+ content = ’ ’.join(block[’text’] for block in msg[’content’] if block[’type’] == ’text’)
+ else:
+ content = str(msg.get(’content’, ’’))
+ if msg.get(’role’) in [’assistant’, ’user’]:
+ summary_request += f"\n{msg[’role’]}: {content}"
+
+ try:
+ # Get summary from the model
+ summary_response, _ = get_response_from_llm(
+ msg=summary_request,
+ client=client,
+ model=model,
+ system_message="You are a summarizer. Create a concise but informative summary.",
+ print_debug=False,
+ msg_history=[]
+ )
+
+ # Create new message history with the summary
+ summarized_history = [{
+ "role": "system",
+ "content": [{"type": "text", "text": system_message}]
+ }, {
+ "role": "assistant",
+ "content": [{"type": "text", "text": f"Previous conversation summary: {summary_response}"}]
+ }]
```

```diff
+
+ # Add back the recent messages
+ summarized_history.extend(recent_msgs)
+
+ return summarized_history
+ except Exception:
+ # If summarization fails, return original messages with the most recent ones
+ return [messages[0]] + recent_msgs
+
def convert_msg_history(msg_history, model=None):
"""
Convert message history from the model-specific format to a generic format.
@@ -263,7 +333,14 @@ def chat_with_agent_manualtools(msg, model, msg_history=None, logging=print):
if msg_history is None:
msg_history = []
system_message = f’You are a coding agent.\n\n{get_tooluse_prompt()}’
- new_msg_history = msg_history
+ new_msg_history = msg_history.copy() if msg_history else []
+
+ # Ensure system message is the first message in history
+ if not new_msg_history or new_msg_history[0].get(’role’) != ’system’:
+ new_msg_history.insert(0, {
+ "role": "system",
+ "content": [{"type": "text", "text": system_message}]
+ })
try:
# Load all tools
[⬇](data:text/plain;base64,ZGlmZiAtLWdpdCBhL2NvZGluZ19hZ2VudC5weSBiL2NvZGluZ19hZ2VudC5weQppbmRleCA5YTJjYzJmLi4zZjFiYzFkIDEwMDY0NAotLS0gYS9jb2RpbmdfYWdlbnQucHkKKysrIGIvY29kaW5nX2FnZW50LnB5CkBAIC0xMTEsNiArMTExLDcgQEAgY2xhc3MgQWdlbnRpY1N5c3RlbToKICAgICAgICAgICAgIHNlbGZfaW1wcm92ZT1GYWxzZSwKICAgICAgICAgICAgIGluc3RhbmNlX2lkPU5vbmUsCiAgICAgICAgICAgICBtYXhfcmV0cmllcz0zLAorICAgICAgICAgICAgbnVtX2NhbmRpZGF0ZXM9MywKICAgICAgICAgKToKICAgICAgICAgc2VsZi5wcm9ibGVtX3N0YXRlbWVudCA9IHByb2JsZW1fc3RhdGVtZW50CiAgICAgICAgIHNlbGYuZ2l0X3RlbXBkaXIgPSBnaXRfdGVtcGRpcgpAQCAtMTIxLDYgKzEyMiw3IEBAIGNsYXNzIEFnZW50aWNTeXN0ZW06CiAgICAgICAgIHNlbGYuaW5zdGFuY2VfaWQgPSBpbnN0YW5jZV9pZCBpZiBub3Qgc2VsZl9pbXByb3ZlIGVsc2UgJ2RnbScKICAgICAgICAgc2VsZi5jb2RlX21vZGVsID0gQ0xBVURFX01PREVMCiAgICAgICAgIHNlbGYubWF4X3JldHJpZXMgPSBtYXhfcmV0cmllcworICAgICAgICBzZWxmLm51bV9jYW5kaWRhdGVzID0gbnVtX2NhbmRpZGF0ZXMKCiAgICAgICAgICMgSW5pdGlhbGl6ZSBsb2dnZXIgYW5kIHN0b3JlIGl0IGluIHRocmVhZC1sb2NhbCBzdG9yYWdlCiAgICAgICAgIHNlbGYubG9nZ2VyID0gc2V0dXBfbG9nZ2VyKGNoYXRfaGlzdG9yeV9maWxlKQpAQCAtMTkwLDcgKzE5Miw3IEBAIFlvdXIgdGFzayBpcyB0byBydW4gdGhlIHJlZ3Jlc3Npb24gdGVzdHMgaW4gdGhlIHtzZWxmLmdpdF90ZW1wZGlyfSBkaXJlY3RvcnkgdG8KCiAgICAgZGVmIGZvcndhcmQoc2VsZik6CiAgICAgICAgICIiIgotICAgICAgICBUaGUgZm9yd2FyZCBmdW5jdGlvbiBmb3IgdGhlIEFnZW50aWNTeXN0ZW0uCisgICAgICAgIFRoZSBmb3J3YXJkIGZ1bmN0aW9uIGZvciB0aGUgQWdlbnRpY1N5c3RlbSB0aGF0IGdlbmVyYXRlcyBhbmQgZXZhbHVhdGVzIG11bHRpcGxlIGNhbmRpZGF0ZSBwYXRjaGVzLgogICAgICAgICAiIiIKICAgICAgICAgYmFzZV9pbnN0cnVjdGlvbiA9IGYiIiJJIGhhdmUgdXBsb2FkZWQgYSBQeXRob24gY29kZSByZXBvc2l0b3J5IGluIHRoZSBkaXJlY3Rvcnkge3NlbGYuZ2l0X3RlbXBkaXJ9LiBIZWxwIHNvbHZlIHRoZSBmb2xsb3dpbmcgcHJvYmxlbS4KCkBAIC0yMDUsMTAgKzIwNywxOCBAQCBZb3VyIHRhc2sgaXMgdG8gcnVuIHRoZSByZWdyZXNzaW9uIHRlc3RzIGluIHRoZSB7c2VsZi5naXRfdGVtcGRpcn0gZGlyZWN0b3J5IHRvCiBZb3VyIHRhc2sgaXMgdG8gbWFrZSBjaGFuZ2VzIHRvIHRoZSBmaWxlcyBpbiB0aGUge3NlbGYuZ2l0X3RlbXBkaXJ9IGRpcmVjdG9yeSB0byBhZGRyZXNzIHRoZSA8cHJvYmxlbV9kZXNjcmlwdGlvbj4uIEkgaGF2ZSBhbHJlYWR5IHRha2VuIGNhcmUgb2YgdGhlIHJlcXVpcmVkIGRlcGVuZGVuY2llcy4KICIiIgoKKyAgICAgICAgIyBHZXQgcmVncmVzc2lvbiB0ZXN0cyBzdW1tYXJ5IG9uY2UgYXQgdGhlIHN0YXJ0CisgICAgICAgIHJlZ3Jlc3Npb25fdGVzdHNfc3VtbWFyeSA9IHNlbGYuZ2V0X3JlZ3Jlc3Npb25fdGVzdHMoKQorCisgICAgICAgICMgTGlzdHMgdG8gc3RvcmUgY2FuZGlkYXRlcworICAgICAgICB2YWxpZF9wYXRjaGVzID0gW10KKyAgICAgICAgdmFsaWRfcmVwb3J0cyA9IFtdCisKICAgICAgICAgcmV0cnlfY291bnQgPSAwCi0gICAgICAgIHdoaWxlIHJldHJ5X2NvdW50IDwgc2VsZi5tYXhfcmV0cmllczoKKyAgICAgICAgd2hpbGUgcmV0cnlfY291bnQgPCBzZWxmLm1heF9yZXRyaWVzIGFuZCBsZW4odmFsaWRfcGF0Y2hlcykgPCBzZWxmLm51bV9jYW5kaWRhdGVzOgogICAgICAgICAgICAgc2FmZV9sb2coZiJcbj09PSBBdHRlbXB0IHtyZXRyeV9jb3VudCArIDF9IG9mIHtzZWxmLm1heF9yZXRyaWVzfSA9PT0iKQotCisgICAgICAgICAgICBzYWZlX2xvZyhmIlZhbGlkIHNvbHV0aW9ucyBzbyBmYXI6IHtsZW4odmFsaWRfcGF0Y2hlcyl9IG9mIHtzZWxmLm51bV9jYW5kaWRhdGVzfSBkZXNpcmVkIikKKwogICAgICAgICAgICAgIyBSZXNldCB0byBiYXNlIGNvbW1pdCBiZWZvcmUgZWFjaCBhdHRlbXB0CiAgICAgICAgICAgICBpZiByZXRyeV9jb3VudCA+IDA6CiAgICAgICAgICAgICAgICAgcmVzZXRfdG9fY29tbWl0KHNlbGYuZ2l0X3RlbXBkaXIsIHNlbGYuYmFzZV9jb21taXQpCkBAIC0yMTYsOCArMjI2LDggQEAgWW91ciB0YXNrIGlzIHRvIG1ha2UgY2hhbmdlcyB0byB0aGUgZmlsZXMgaW4gdGhlIHtzZWxmLmdpdF90ZW1wZGlyfSBkaXJlY3RvcnkgdG8KICAgICAgICAgICAgICMgQWRkIHJldHJ5IGNvbnRleHQgdG8gaW5zdHJ1Y3Rpb24gaWYgdGhpcyBpcyBhIHJldHJ5IGF0dGVtcHQKICAgICAgICAgICAgIGluc3RydWN0aW9uID0gYmFzZV9pbnN0cnVjdGlvbgogICAgICAgICAgICAgaWYgcmV0cnlfY291bnQgPiAwOgotICAgICAgICAgICAgICAgIGluc3RydWN0aW9uICs9IGYiIiJcbk5PVEU6IFByZXZpb3VzIGF0dGVtcHQocykgZmFpbGVkIGJlY2F1c2UgdGhleSBlaXRoZXIgcHJvZHVjZWQgZW1wdHkgcGF0Y2hlcyBvciBvbmx5IG1vZGlmaWVkIHRlc3QgZmlsZXMuCi1QbGVhc2UgZW5zdXJlIHlvdXIgc29sdXRpb24gaW5jbHVkZXMgY2hhbmdlcyB0byB0aGUgbWFpbiBzb3VyY2UgY29kZSBmaWxlcywgbm90IGp1c3QgdGVzdCBmaWxlcy4iIiIKKyAgICAgICAgICAgICAgICBpbnN0cnVjdGlvbiArPSBmIiIiXG5OT1RFOiBQcmV2aW91cyBhdHRlbXB0KHMpIGRpZCBub3QgcHJvZHVjZSBlbm91Z2ggdmFsaWQgc29sdXRpb25zLgorUGxlYXNlIHByb3ZpZGUgYSBkaWZmZXJlbnQgYXBwcm9hY2ggdG8gc29sdmUgdGhlIHByb2JsZW0uIFlvdXIgc29sdXRpb24gbXVzdCBpbmNsdWRlIGNoYW5nZXMgdG8gdGhlIG1haW4gc291cmNlIGNvZGUgZmlsZXMsIG5vdCBqdXN0IHRlc3QgZmlsZXMuIiIiCgogICAgICAgICAgICAgIyBSdW4gdGhlIGFnZW50CiAgICAgICAgICAgICBuZXdfbXNnX2hpc3RvcnkgPSBjaGF0X3dpdGhfYWdlbnQoaW5zdHJ1Y3Rpb24sIG1vZGVsPXNlbGYuY29kZV9tb2RlbCwgbXNnX2hpc3Rvcnk9W10sIGxvZ2dpbmc9c2FmZV9sb2cpCkBAIC0yMjgsMTYgKzIzOCw0NSBAQCBQbGVhc2UgZW5zdXJlIHlvdXIgc29sdXRpb24gaW5jbHVkZXMgY2hhbmdlcyB0byB0aGUgbWFpbiBzb3VyY2UgY29kZSBmaWxlcywgbm90CgogICAgICAgICAgICAgaWYgaXNfdmFsaWQ6CiAgICAgICAgICAgICAgICAgc2FmZV9sb2coZiJWYWxpZCBwYXRjaCBnZW5lcmF0ZWQ6IHtyZWFzb259IikKLSAgICAgICAgICAgICAgICBicmVhaworICAgICAgICAgICAgICAgICMgUnVuIHJlZ3Jlc3Npb24gdGVzdHMgZm9yIHRoaXMgY2FuZGlkYXRlCisgICAgICAgICAgICAgICAgdGVzdF9yZXBvcnQgPSBzZWxmLnJ1bl9yZWdyZXNzaW9uX3Rlc3RzKHJlZ3Jlc3Npb25fdGVzdHNfc3VtbWFyeSkKKyAgICAgICAgICAgICAgICB0ZXN0X3Njb3JlID0gZ2V0X3JlcG9ydF9zY29yZSh0ZXN0X3JlcG9ydCkKKyAgICAgICAgICAgICAgICBzYWZlX2xvZyhmIlRlc3Qgc2NvcmU6IHt0ZXN0X3Njb3JlfSIpCisKKyAgICAgICAgICAgICAgICB2YWxpZF9wYXRjaGVzLmFwcGVuZChwYXRjaCkKKyAgICAgICAgICAgICAgICB2YWxpZF9yZXBvcnRzLmFwcGVuZCh0ZXN0X3JlcG9ydCkKKworICAgICAgICAgICAgICAgIGlmIGxlbih2YWxpZF9wYXRjaGVzKSA+PSBzZWxmLm51bV9jYW5kaWRhdGVzOgorICAgICAgICAgICAgICAgICAgICBicmVhawogICAgICAgICAgICAgZWxzZToKICAgICAgICAgICAgICAgICBzYWZlX2xvZyhmIkludmFsaWQgcGF0Y2g6IHtyZWFzb259IikKLSAgICAgICAgICAgICAgICBpZiByZXRyeV9jb3VudCA8IHNlbGYubWF4X3JldHJpZXMgLSAxOgotICAgICAgICAgICAgICAgICAgICBzYWZlX2xvZygiUmV0cnlpbmcgd2l0aCBhIG5ldyBhdHRlbXB0Li4uIikKLSAgICAgICAgICAgICAgICBlbHNlOgotICAgICAgICAgICAgICAgICAgICBzYWZlX2xvZygiTWF4aW11bSByZXRyaWVzIHJlYWNoZWQuIFVuYWJsZSB0byBnZW5lcmF0ZSBhIHZhbGlkIHBhdGNoLiIpCgogICAgICAgICAgICAgcmV0cnlfY291bnQgKz0gMQoKKyAgICAgICAgaWYgbm90IHZhbGlkX3BhdGNoZXM6CisgICAgICAgICAgICBzYWZlX2xvZygiRmFpbGVkIHRvIGdlbmVyYXRlIGFueSB2YWxpZCBwYXRjaGVzLiIpCisgICAgICAgICAgICByZXR1cm4KKworICAgICAgICAjIFVzZSBzY29yZV90aWVfYnJlYWtlciB0byBzZWxlY3QgdGhlIGJlc3QgcGF0Y2gKKyAgICAgICAgc2FmZV9sb2coZiJcbj09PSBTZWxlY3RpbmcgQmVzdCBTb2x1dGlvbiBmcm9tIHtsZW4odmFsaWRfcGF0Y2hlcyl9IENhbmRpZGF0ZXMgPT09IikKKyAgICAgICAgYmVzdF9pbmRleCA9IHNjb3JlX3RpZV9icmVha2VyKAorICAgICAgICAgICAgc2VsZi5wcm9ibGVtX3N0YXRlbWVudCwKKyAgICAgICAgICAgIHZhbGlkX3BhdGNoZXMsCisgICAgICAgICAgICB2YWxpZF9yZXBvcnRzLAorICAgICAgICAgICAgbG9nZ2luZz1zYWZlX2xvZworICAgICAgICApCisKKyAgICAgICAgIyBSZXNldCB0byBiYXNlIGFuZCBhcHBseSB0aGUgYmVzdCBwYXRjaAorICAgICAgICByZXNldF90b19jb21taXQoc2VsZi5naXRfdGVtcGRpciwgc2VsZi5iYXNlX2NvbW1pdCkKKyAgICAgICAgYmVzdF9wYXRjaCA9IHZhbGlkX3BhdGNoZXNbYmVzdF9pbmRleF0KKyAgICAgICAgc2FmZV9sb2coZiJcbj09PSBBcHBseWluZyBCZXN0IFNvbHV0aW9uIChDYW5kaWRhdGUge2Jlc3RfaW5kZXggKyAxfSkgPT09IikKKyAgICAgICAgYXBwbHlfcGF0Y2goc2VsZi5naXRfdGVtcGRpciwgYmVzdF9wYXRjaCkKKworICAgICAgICAjIEZpbmFsIHZhbGlkYXRpb24gb2YgdGhlIHNlbGVjdGVkIHBhdGNoCisgICAgICAgIGZpbmFsX3Rlc3RfcmVwb3J0ID0gc2VsZi5ydW5fcmVncmVzc2lvbl90ZXN0cyhyZWdyZXNzaW9uX3Rlc3RzX3N1bW1hcnkpCisgICAgICAgIGZpbmFsX3Njb3JlID0gZ2V0X3JlcG9ydF9zY29yZShmaW5hbF90ZXN0X3JlcG9ydCkKKyAgICAgICAgc2FmZV9sb2coZiJGaW5hbCBzb2x1dGlvbiB0ZXN0IHNjb3JlOiB7ZmluYWxfc2NvcmV9IikKKwogZGVmIG1haW4oKToKICAgICBwYXJzZXIgPSBhcmdwYXJzZS5Bcmd1bWVudFBhcnNlcihkZXNjcmlwdGlvbj0nUHJvY2VzcyByZXBvc2l0b3J5IHdpdGggYW4gYWdlbnRpYyBzeXN0ZW0uJykKICAgICBwYXJzZXIuYWRkX2FyZ3VtZW50KCctLXByb2JsZW1fc3RhdGVtZW50JywgcmVxdWlyZWQ9VHJ1ZSwgaGVscD0nVGhlIHByb2JsZW0gc3RhdGVtZW50IHRvIHByb2Nlc3MnKQpAQCAtMjQ5LDYgKzI4OCw3IEBAIGRlZiBtYWluKCk6CiAgICAgcGFyc2VyLmFkZF9hcmd1bWVudCgnLS1zZWxmX2ltcHJvdmUnLCBkZWZhdWx0PUZhbHNlLCBhY3Rpb249J3N0b3JlX3RydWUnLCBoZWxwPSdXaGV0aGVyIHRvIHNlbGYtaW1wcm92ZSB0aGUgcmVwb3NpdG9yeSBvciBzb2x2aW5nIHN3ZScpCiAgICAgcGFyc2VyLmFkZF9hcmd1bWVudCgnLS1pbnN0YW5jZV9pZCcsIGRlZmF1bHQ9Tm9uZSwgaGVscD0nSW5zdGFuY2UgSUQgZm9yIFNXRSBpc3N1ZScpCiAgICAgcGFyc2VyLmFkZF9hcmd1bWVudCgnLS1tYXhfcmV0cmllcycsIHR5cGU9aW50LCBkZWZhdWx0PTMsIGhlbHA9J01heGltdW0gbnVtYmVyIG9mIHBhdGNoIGdlbmVyYXRpb24gYXR0ZW1wdHMnKQorICAgIHBhcnNlci5hZGRfYXJndW1lbnQoJy0tbnVtX2NhbmRpZGF0ZXMnLCB0eXBlPWludCwgZGVmYXVsdD0zLCBoZWxwPSdOdW1iZXIgb2YgY2FuZGlkYXRlIHNvbHV0aW9ucyB0byBnZW5lcmF0ZScpCiAgICAgYXJncyA9IHBhcnNlci5wYXJzZV9hcmdzKCkKCiAgICAgIyBQcm9jZXNzIHRoZSByZXBvc2l0b3J5CkBAIC0yNjEsNiArMzAxLDcgQEAgZGVmIG1haW4oKToKICAgICAgICAgc2VsZl9pbXByb3ZlPWFyZ3Muc2VsZl9pbXByb3ZlLAogICAgICAgICBpbnN0YW5jZV9pZD1hcmdzLmluc3RhbmNlX2lkLAogICAgICAgICBtYXhfcmV0cmllcz1hcmdzLm1heF9yZXRyaWVzLAorICAgICAgICBudW1fY2FuZGlkYXRlcz1hcmdzLm51bV9jYW5kaWRhdGVzLAogICAgICkKCiAgICAgIyBSdW4gdGhlIGFnZW50aWMgc3lzdGVtIHRvIHRyeSB0byBzb2x2ZSB0aGUgcHJvYmxlbQ==)
diff --git a/coding_agent.py b/coding_agent.py
index 9a2cc2f..3f1bc1d 100644
--- a/coding_agent.py
+++ b/coding_agent.py
@@ -111,6 +111,7 @@ class AgenticSystem:
self_improve=False,
instance_id=None,
max_retries=3,
+ num_candidates=3,
):
self.problem_statement = problem_statement
self.git_tempdir = git_tempdir
@@ -121,6 +122,7 @@ class AgenticSystem:
self.instance_id = instance_id if not self_improve else ’dgm’
self.code_model = CLAUDE_MODEL
self.max_retries = max_retries
+ self.num_candidates = num_candidates
# Initialize logger and store it in thread-local storage
self.logger = setup_logger(chat_history_file)
@@ -190,7 +192,7 @@ Your task is to run the regression tests in the {self.git_tempdir} directory to
def forward(self):
"""
- The forward function for the AgenticSystem.
+ The forward function for the AgenticSystem that generates and evaluates multiple candidate patches.
"""
base_instruction = f"""I have uploaded a Python code repository in the directory {self.git_tempdir}. Help solve the following problem.
@@ -205,10 +207,18 @@ Your task is to run the regression tests in the {self.git_tempdir} directory to
Your task is to make changes to the files in the {self.git_tempdir} directory to address the <problem_description>. I have already taken care of the required dependencies.
"""
+ # Get regression tests summary once at the start
+ regression_tests_summary = self.get_regression_tests()
+
+ # Lists to store candidates
+ valid_patches = []
+ valid_reports = []
+
retry_count = 0
- while retry_count < self.max_retries:
+ while retry_count < self.max_retries and len(valid_patches) < self.num_candidates:
safe_log(f"\n=== Attempt {retry_count + 1} of {self.max_retries} ===")
-
+ safe_log(f"Valid solutions so far: {len(valid_patches)} of {self.num_candidates} desired")
+
# Reset to base commit before each attempt
if retry_count > 0:
reset_to_commit(self.git_tempdir, self.base_commit)
@@ -216,8 +226,8 @@ Your task is to make changes to the files in the {self.git_tempdir} directory to
# Add retry context to instruction if this is a retry attempt
instruction = base_instruction
if retry_count > 0:
- instruction += f"""\nNOTE: Previous attempt(s) failed because they either produced empty patches or only modified test files.
-Please ensure your solution includes changes to the main source code files, not just test files."""
+ instruction += f"""\nNOTE: Previous attempt(s) did not produce enough valid solutions.
+Please provide a different approach to solve the problem. Your solution must include changes to the main source code files, not just test files."""
# Run the agent
new_msg_history = chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
@@ -228,16 +238,45 @@ Please ensure your solution includes changes to the main source code files, not
if is_valid:
safe_log(f"Valid patch generated: {reason}")
- break
+ # Run regression tests for this candidate
+ test_report = self.run_regression_tests(regression_tests_summary)
+ test_score = get_report_score(test_report)
+ safe_log(f"Test score: {test_score}")
+
+ valid_patches.append(patch)
+ valid_reports.append(test_report)
+
+ if len(valid_patches) >= self.num_candidates:
+ break
else:
safe_log(f"Invalid patch: {reason}")
- if retry_count < self.max_retries - 1:
- safe_log("Retrying with a new attempt...")
- else:
- safe_log("Maximum retries reached. Unable to generate a valid patch.")
retry_count += 1
+ if not valid_patches:
+ safe_log("Failed to generate any valid patches.")
+ return
+
+ # Use score_tie_breaker to select the best patch
+ safe_log(f"\n=== Selecting Best Solution from {len(valid_patches)} Candidates ===")
+ best_index = score_tie_breaker(
+ self.problem_statement,
+ valid_patches,
+ valid_reports,
+ logging=safe_log
+ )
+
+ # Reset to base and apply the best patch
+ reset_to_commit(self.git_tempdir, self.base_commit)
+ best_patch = valid_patches[best_index]
+ safe_log(f"\n=== Applying Best Solution (Candidate {best_index + 1}) ===")
+ apply_patch(self.git_tempdir, best_patch)
+
+ # Final validation of the selected patch
+ final_test_report = self.run_regression_tests(regression_tests_summary)
+ final_score = get_report_score(final_test_report)
+ safe_log(f"Final solution test score: {final_score}")
+
def main():
parser = argparse.ArgumentParser(description=’Process repository with an agentic system.’)
parser.add_argument(’--problem_statement’, required=True, help=’The problem statement to process’)
@@ -249,6 +288,7 @@ def main():
parser.add_argument(’--self_improve’, default=False, action=’store_true’, help=’Whether to self-improve the repository or solving swe’)
parser.add_argument(’--instance_id’, default=None, help=’Instance ID for SWE issue’)
parser.add_argument(’--max_retries’, type=int, default=3, help=’Maximum number of patch generation attempts’)
+ parser.add_argument(’--num_candidates’, type=int, default=3, help=’Number of candidate solutions to generate’)
args = parser.parse_args()
# Process the repository
@@ -261,6 +301,7 @@ def main():
self_improve=args.self_improve,
instance_id=args.instance_id,
max_retries=args.max_retries,
+ num_candidates=args.num_candidates,
)
# Run the agentic system to try to solve the problem+
[⬇](data:text/plain;base64,ZGlmZiAtLWdpdCBhL2NvZGluZ19hZ2VudC5weSBiL2NvZGluZ19hZ2VudC5weQppbmRleCAzZjFiYzFkLi41ODg5MzhkIDEwMDY0NAotLS0gYS9jb2RpbmdfYWdlbnQucHkKKysrIGIvY29kaW5nX2FnZW50LnB5CkBAIC0xOTMsNDIgKzE5Myw1OSBAQCBZb3VyIHRhc2sgaXMgdG8gcnVuIHRoZSByZWdyZXNzaW9uIHRlc3RzIGluIHRoZSB7c2VsZi5naXRfdGVtcGRpcn0gZGlyZWN0b3J5IHRvCiAgICAgZGVmIGZvcndhcmQoc2VsZik6CiAgICAgICAgICIiIgogICAgICAgICBUaGUgZm9yd2FyZCBmdW5jdGlvbiBmb3IgdGhlIEFnZW50aWNTeXN0ZW0gdGhhdCBnZW5lcmF0ZXMgYW5kIGV2YWx1YXRlcyBtdWx0aXBsZSBjYW5kaWRhdGUgcGF0Y2hlcy4KKyAgICAgICAgVGhpcyB2ZXJzaW9uIG1haW50YWlucyBoaXN0b3J5IG9mIHByaW9yIHZhbGlkIHBhdGNoZXMgYW5kIHRlc3QgcmVzdWx0cywgb25seSB1c2luZyB0aGUgdGllLWJyZWFrZXIKKyAgICAgICAgd2hlbiBuZWNlc3NhcnkuCiAgICAgICAgICIiIgotICAgICAgICBiYXNlX2luc3RydWN0aW9uID0gZiIiIkkgaGF2ZSB1cGxvYWRlZCBhIFB5dGhvbiBjb2RlIHJlcG9zaXRvcnkgaW4gdGhlIGRpcmVjdG9yeSB7c2VsZi5naXRfdGVtcGRpcn0uIEhlbHAgc29sdmUgdGhlIGZvbGxvd2luZyBwcm9ibGVtLgotCi08cHJvYmxlbV9kZXNjcmlwdGlvbj4KLXtzZWxmLnByb2JsZW1fc3RhdGVtZW50fQotPC9wcm9ibGVtX2Rlc2NyaXB0aW9uPgotCi08dGVzdF9kZXNjcmlwdGlvbj4KLXtzZWxmLnRlc3RfZGVzY3JpcHRpb259Ci08L3Rlc3RfZGVzY3JpcHRpb24+Ci0KLVlvdXIgdGFzayBpcyB0byBtYWtlIGNoYW5nZXMgdG8gdGhlIGZpbGVzIGluIHRoZSB7c2VsZi5naXRfdGVtcGRpcn0gZGlyZWN0b3J5IHRvIGFkZHJlc3MgdGhlIDxwcm9ibGVtX2Rlc2NyaXB0aW9uPi4gSSBoYXZlIGFscmVhZHkgdGFrZW4gY2FyZSBvZiB0aGUgcmVxdWlyZWQgZGVwZW5kZW5jaWVzLgotIiIiCi0KLSAgICAgICAgIyBHZXQgcmVncmVzc2lvbiB0ZXN0cyBzdW1tYXJ5IG9uY2UgYXQgdGhlIHN0YXJ0CiAgICAgICAgIHJlZ3Jlc3Npb25fdGVzdHNfc3VtbWFyeSA9IHNlbGYuZ2V0X3JlZ3Jlc3Npb25fdGVzdHMoKQoKLSAgICAgICAgIyBMaXN0cyB0byBzdG9yZSBjYW5kaWRhdGVzCisgICAgICAgICMgTGlzdHMgdG8gc3RvcmUgYWxsIHZhbGlkIHBhdGNoZXMgYW5kIHRoZWlyIGluZm9ybWF0aW9uCiAgICAgICAgIHZhbGlkX3BhdGNoZXMgPSBbXQogICAgICAgICB2YWxpZF9yZXBvcnRzID0gW10KKyAgICAgICAgdmFsaWRfc2NvcmVzID0gW10KKyAgICAgICAgYmVzdF9zY29yZSA9IDAKKyAgICAgICAgYmVzdF9wYXRjaGVzX2luZGljZXMgPSBbXSAgIyBJbmRpY2VzIG9mIHBhdGNoZXMgdGhhdCBzaGFyZSB0aGUgYmVzdCBzY29yZQoKICAgICAgICAgcmV0cnlfY291bnQgPSAwCiAgICAgICAgIHdoaWxlIHJldHJ5X2NvdW50IDwgc2VsZi5tYXhfcmV0cmllcyBhbmQgbGVuKHZhbGlkX3BhdGNoZXMpIDwgc2VsZi5udW1fY2FuZGlkYXRlczoKICAgICAgICAgICAgIHNhZmVfbG9nKGYiXG49PT0gQXR0ZW1wdCB7cmV0cnlfY291bnQgKyAxfSBvZiB7c2VsZi5tYXhfcmV0cmllc30gPT09IikKICAgICAgICAgICAgIHNhZmVfbG9nKGYiVmFsaWQgc29sdXRpb25zIHNvIGZhcjoge2xlbih2YWxpZF9wYXRjaGVzKX0gb2Yge3NlbGYubnVtX2NhbmRpZGF0ZXN9IGRlc2lyZWQiKQorICAgICAgICAgICAgc2FmZV9sb2coZiJDdXJyZW50IGJlc3QgdGVzdCBzY29yZToge2Jlc3Rfc2NvcmV9IikKCiAgICAgICAgICAgICAjIFJlc2V0IHRvIGJhc2UgY29tbWl0IGJlZm9yZSBlYWNoIGF0dGVtcHQKICAgICAgICAgICAgIGlmIHJldHJ5X2NvdW50ID4gMDoKICAgICAgICAgICAgICAgICByZXNldF90b19jb21taXQoc2VsZi5naXRfdGVtcGRpciwgc2VsZi5iYXNlX2NvbW1pdCkKCi0gICAgICAgICAgICAjIEFkZCByZXRyeSBjb250ZXh0IHRvIGluc3RydWN0aW9uIGlmIHRoaXMgaXMgYSByZXRyeSBhdHRlbXB0Ci0gICAgICAgICAgICBpbnN0cnVjdGlvbiA9IGJhc2VfaW5zdHJ1Y3Rpb24KLSAgICAgICAgICAgIGlmIHJldHJ5X2NvdW50ID4gMDoKLSAgICAgICAgICAgICAgICBpbnN0cnVjdGlvbiArPSBmIiIiXG5OT1RFOiBQcmV2aW91cyBhdHRlbXB0KHMpIGRpZCBub3QgcHJvZHVjZSBlbm91Z2ggdmFsaWQgc29sdXRpb25zLgorICAgICAgICAgICAgIyBDb25zdHJ1Y3QgaW5zdHJ1Y3Rpb24gd2l0aCBwcmV2aW91cyBiZXN0IHNvbHV0aW9ucyBpZiBhdmFpbGFibGUKKyAgICAgICAgICAgIGluc3RydWN0aW9uID0gZiIiIkkgaGF2ZSB1cGxvYWRlZCBhIFB5dGhvbiBjb2RlIHJlcG9zaXRvcnkgaW4gdGhlIGRpcmVjdG9yeSB7c2VsZi5naXRfdGVtcGRpcn0uIEhlbHAgc29sdmUgdGhlIGZvbGxvd2luZyBwcm9ibGVtLgorCis8cHJvYmxlbV9kZXNjcmlwdGlvbj4KK3tzZWxmLnByb2JsZW1fc3RhdGVtZW50fQorPC9wcm9ibGVtX2Rlc2NyaXB0aW9uPgorCis8dGVzdF9kZXNjcmlwdGlvbj4KK3tzZWxmLnRlc3RfZGVzY3JpcHRpb259Cis8L3Rlc3RfZGVzY3JpcHRpb24+IiIiCisKKyAgICAgICAgICAgICMgQWRkIHByZXZpb3VzIHNvbHV0aW9ucyBjb250ZXh0IGlmIGF2YWlsYWJsZQorICAgICAgICAgICAgaWYgdmFsaWRfcGF0Y2hlcyBhbmQgcmV0cnlfY291bnQgPiAwOgorICAgICAgICAgICAgICAgIHByZXZpb3VzX3NvbHV0aW9ucyA9IFtdCisgICAgICAgICAgICAgICAgZm9yIGksIChwYXRjaCwgcmVwb3J0LCBzY29yZSkgaW4gZW51bWVyYXRlKHppcCh2YWxpZF9wYXRjaGVzLCB2YWxpZF9yZXBvcnRzLCB2YWxpZF9zY29yZXMpKToKKyAgICAgICAgICAgICAgICAgICAgcHJldmlvdXNfc29sdXRpb25zLmFwcGVuZChmIiIiCitQcmV2aW91cyBTb2x1dGlvbiB7aSsxfToKKzxjb2RlX2NoYW5nZXM+Cit7cGF0Y2h9Cis8L2NvZGVfY2hhbmdlcz4KK1Rlc3QgU2NvcmU6IHtzY29yZX0KK1Rlc3QgUmVwb3J0OiB7cmVwb3J0fQorIiIiKQorICAgICAgICAgICAgICAgIGluc3RydWN0aW9uICs9ICJcblxuUHJldmlvdXMgc29sdXRpb24gYXR0ZW1wdHM6XG4iICsgIlxuIi5qb2luKHByZXZpb3VzX3NvbHV0aW9ucykKKyAgICAgICAgICAgICAgICBpbnN0cnVjdGlvbiArPSAiXG5QbGVhc2UgcHJvdmlkZSBhIG5ldyBzb2x1dGlvbiB0aGF0IGFkZHJlc3NlcyBhbnkgbGltaXRhdGlvbnMgaW4gdGhlIHByZXZpb3VzIGF0dGVtcHRzIG9yIGV4cGxvcmVzIGEgZGlmZmVyZW50IGFwcHJvYWNoLiIKKyAgICAgICAgICAgIGVsaWYgcmV0cnlfY291bnQgPiAwOgorICAgICAgICAgICAgICAgIGluc3RydWN0aW9uICs9ICIiIlxuTk9URTogUHJldmlvdXMgYXR0ZW1wdChzKSBkaWQgbm90IHByb2R1Y2UgZW5vdWdoIHZhbGlkIHNvbHV0aW9ucy4KIFBsZWFzZSBwcm92aWRlIGEgZGlmZmVyZW50IGFwcHJvYWNoIHRvIHNvbHZlIHRoZSBwcm9ibGVtLiBZb3VyIHNvbHV0aW9uIG11c3QgaW5jbHVkZSBjaGFuZ2VzIHRvIHRoZSBtYWluIHNvdXJjZSBjb2RlIGZpbGVzLCBub3QganVzdCB0ZXN0IGZpbGVzLiIiIgoKKyAgICAgICAgICAgIGluc3RydWN0aW9uICs9IGYiXG5cbllvdXIgdGFzayBpcyB0byBtYWtlIGNoYW5nZXMgdG8gdGhlIGZpbGVzIGluIHRoZSB7c2VsZi5naXRfdGVtcGRpcn0gZGlyZWN0b3J5IHRvIGFkZHJlc3MgdGhlIDxwcm9ibGVtX2Rlc2NyaXB0aW9uPi4gSSBoYXZlIGFscmVhZHkgdGFrZW4gY2FyZSBvZiB0aGUgcmVxdWlyZWQgZGVwZW5kZW5jaWVzLiIKKwogICAgICAgICAgICAgIyBSdW4gdGhlIGFnZW50CiAgICAgICAgICAgICBuZXdfbXNnX2hpc3RvcnkgPSBjaGF0X3dpdGhfYWdlbnQoaW5zdHJ1Y3Rpb24sIG1vZGVsPXNlbGYuY29kZV9tb2RlbCwgbXNnX2hpc3Rvcnk9W10sIGxvZ2dpbmc9c2FmZV9sb2cpCgpAQCAtMjQ1LDYgKzI2MiwxNCBAQCBQbGVhc2UgcHJvdmlkZSBhIGRpZmZlcmVudCBhcHByb2FjaCB0byBzb2x2ZSB0aGUgcHJvYmxlbS4gWW91ciBzb2x1dGlvbiBtdXN0IGluYwoKICAgICAgICAgICAgICAgICB2YWxpZF9wYXRjaGVzLmFwcGVuZChwYXRjaCkKICAgICAgICAgICAgICAgICB2YWxpZF9yZXBvcnRzLmFwcGVuZCh0ZXN0X3JlcG9ydCkKKyAgICAgICAgICAgICAgICB2YWxpZF9zY29yZXMuYXBwZW5kKHRlc3Rfc2NvcmUpCisKKyAgICAgICAgICAgICAgICAjIFVwZGF0ZSBiZXN0IHNjb3JlIGFuZCBpbmRpY2VzCisgICAgICAgICAgICAgICAgaWYgdGVzdF9zY29yZSA+IGJlc3Rfc2NvcmU6CisgICAgICAgICAgICAgICAgICAgIGJlc3Rfc2NvcmUgPSB0ZXN0X3Njb3JlCisgICAgICAgICAgICAgICAgICAgIGJlc3RfcGF0Y2hlc19pbmRpY2VzID0gW2xlbih2YWxpZF9wYXRjaGVzKSAtIDFdCisgICAgICAgICAgICAgICAgZWxpZiB0ZXN0X3Njb3JlID09IGJlc3Rfc2NvcmU6CisgICAgICAgICAgICAgICAgICAgIGJlc3RfcGF0Y2hlc19pbmRpY2VzLmFwcGVuZChsZW4odmFsaWRfcGF0Y2hlcykgLSAxKQoKICAgICAgICAgICAgICAgICBpZiBsZW4odmFsaWRfcGF0Y2hlcykgPj0gc2VsZi5udW1fY2FuZGlkYXRlczoKICAgICAgICAgICAgICAgICAgICAgYnJlYWsKQEAgLTI1NywyNSArMjgyLDMwIEBAIFBsZWFzZSBwcm92aWRlIGEgZGlmZmVyZW50IGFwcHJvYWNoIHRvIHNvbHZlIHRoZSBwcm9ibGVtLiBZb3VyIHNvbHV0aW9uIG11c3QgaW5jCiAgICAgICAgICAgICBzYWZlX2xvZygiRmFpbGVkIHRvIGdlbmVyYXRlIGFueSB2YWxpZCBwYXRjaGVzLiIpCiAgICAgICAgICAgICByZXR1cm4KCi0gICAgICAgICMgVXNlIHNjb3JlX3RpZV9icmVha2VyIHRvIHNlbGVjdCB0aGUgYmVzdCBwYXRjaAorICAgICAgICAjIE9ubHkgdXNlIHRpZS1icmVha2VyIGlmIHdlIGhhdmUgbXVsdGlwbGUgcGF0Y2hlcyB3aXRoIHRoZSBiZXN0IHNjb3JlCiAgICAgICAgIHNhZmVfbG9nKGYiXG49PT0gU2VsZWN0aW5nIEJlc3QgU29sdXRpb24gZnJvbSB7bGVuKHZhbGlkX3BhdGNoZXMpfSBDYW5kaWRhdGVzID09PSIpCi0gICAgICAgIGJlc3RfaW5kZXggPSBzY29yZV90aWVfYnJlYWtlcigKLSAgICAgICAgICAgIHNlbGYucHJvYmxlbV9zdGF0ZW1lbnQsCi0gICAgICAgICAgICB2YWxpZF9wYXRjaGVzLAotICAgICAgICAgICAgdmFsaWRfcmVwb3J0cywKLSAgICAgICAgICAgIGxvZ2dpbmc9c2FmZV9sb2cKLSAgICAgICAgKQorICAgICAgICBpZiBsZW4oYmVzdF9wYXRjaGVzX2luZGljZXMpID4gMToKKyAgICAgICAgICAgIHNhZmVfbG9nKGYiTXVsdGlwbGUgc29sdXRpb25zICh7bGVuKGJlc3RfcGF0Y2hlc19pbmRpY2VzKX0pIHRpZWQgZm9yIGJlc3Qgc2NvcmUge2Jlc3Rfc2NvcmV9LiBVc2luZyB0aWUtYnJlYWtlci4iKQorICAgICAgICAgICAgYmVzdF9pbmRleCA9IHNjb3JlX3RpZV9icmVha2VyKAorICAgICAgICAgICAgICAgIHNlbGYucHJvYmxlbV9zdGF0ZW1lbnQsCisgICAgICAgICAgICAgICAgW3ZhbGlkX3BhdGNoZXNbaV0gZm9yIGkgaW4gYmVzdF9wYXRjaGVzX2luZGljZXNdLAorICAgICAgICAgICAgICAgIFt2YWxpZF9yZXBvcnRzW2ldIGZvciBpIGluIGJlc3RfcGF0Y2hlc19pbmRpY2VzXSwKKyAgICAgICAgICAgICAgICBsb2dnaW5nPXNhZmVfbG9nCisgICAgICAgICAgICApCisgICAgICAgICAgICBiZXN0X2luZGV4ID0gYmVzdF9wYXRjaGVzX2luZGljZXNbYmVzdF9pbmRleF0KKyAgICAgICAgZWxzZToKKyAgICAgICAgICAgIGJlc3RfaW5kZXggPSBiZXN0X3BhdGNoZXNfaW5kaWNlc1swXQoKICAgICAgICAgIyBSZXNldCB0byBiYXNlIGFuZCBhcHBseSB0aGUgYmVzdCBwYXRjaAogICAgICAgICByZXNldF90b19jb21taXQoc2VsZi5naXRfdGVtcGRpciwgc2VsZi5iYXNlX2NvbW1pdCkKICAgICAgICAgYmVzdF9wYXRjaCA9IHZhbGlkX3BhdGNoZXNbYmVzdF9pbmRleF0KLSAgICAgICAgc2FmZV9sb2coZiJcbj09PSBBcHBseWluZyBCZXN0IFNvbHV0aW9uIChDYW5kaWRhdGUge2Jlc3RfaW5kZXggKyAxfSkgPT09IikKKyAgICAgICAgc2FmZV9sb2coZiJcbj09PSBBcHBseWluZyBCZXN0IFNvbHV0aW9uIChDYW5kaWRhdGUge2Jlc3RfaW5kZXggKyAxfSkgd2l0aCBzY29yZSB7dmFsaWRfc2NvcmVzW2Jlc3RfaW5kZXhdfSA9PT0iKQogICAgICAgICBhcHBseV9wYXRjaChzZWxmLmdpdF90ZW1wZGlyLCBiZXN0X3BhdGNoKQoKICAgICAgICAgIyBGaW5hbCB2YWxpZGF0aW9uIG9mIHRoZSBzZWxlY3RlZCBwYXRjaAogICAgICAgICBmaW5hbF90ZXN0X3JlcG9ydCA9IHNlbGYucnVuX3JlZ3Jlc3Npb25fdGVzdHMocmVncmVzc2lvbl90ZXN0c19zdW1tYXJ5KQogICAgICAgICBmaW5hbF9zY29yZSA9IGdldF9yZXBvcnRfc2NvcmUoZmluYWxfdGVzdF9yZXBvcnQpCi0gICAgICAgIHNhZmVfbG9nKGYiRmluYWwgc29sdXRpb24gdGVzdCBzY29yZToge2ZpbmFsX3Njb3JlfSIpCisgICAgICAgIHNhZmVfbG9nKGYiRmluYWwgdmFsaWRhdGlvbiB0ZXN0IHNjb3JlOiB7ZmluYWxfc2NvcmV9IikKCiBkZWYgbWFpbigpOgogICAgIHBhcnNlciA9IGFyZ3BhcnNlLkFyZ3VtZW50UGFyc2VyKGRlc2NyaXB0aW9uPSdQcm9jZXNzIHJlcG9zaXRvcnkgd2l0aCBhbiBhZ2VudGljIHN5c3RlbS4nKQ==)
diff --git a/coding_agent.py b/coding_agent.py
index 3f1bc1d..588938d 100644
--- a/coding_agent.py
+++ b/coding_agent.py
@@ -193,42 +193,59 @@ Your task is to run the regression tests in the {self.git_tempdir} directory to
def forward(self):
"""
The forward function for the AgenticSystem that generates and evaluates multiple candidate patches.
+ This version maintains history of prior valid patches and test results, only using the tie-breaker
+ when necessary.
"""
- base_instruction = f"""I have uploaded a Python code repository in the directory {self.git_tempdir}. Help solve the following problem.
-
-<problem_description>
-{self.problem_statement}
-</problem_description>
-
-<test_description>
-{self.test_description}
-</test_description>
-
-Your task is to make changes to the files in the {self.git_tempdir} directory to address the <problem_description>. I have already taken care of the required dependencies.
-"""
-
- # Get regression tests summary once at the start
regression_tests_summary = self.get_regression_tests()
- # Lists to store candidates
+ # Lists to store all valid patches and their information
valid_patches = []
valid_reports = []
+ valid_scores = []
+ best_score = 0
+ best_patches_indices = [] # Indices of patches that share the best score
retry_count = 0
while retry_count < self.max_retries and len(valid_patches) < self.num_candidates:
safe_log(f"\n=== Attempt {retry_count + 1} of {self.max_retries} ===")
safe_log(f"Valid solutions so far: {len(valid_patches)} of {self.num_candidates} desired")
+ safe_log(f"Current best test score: {best_score}")
# Reset to base commit before each attempt
if retry_count > 0:
reset_to_commit(self.git_tempdir, self.base_commit)
- # Add retry context to instruction if this is a retry attempt
- instruction = base_instruction
- if retry_count > 0:
- instruction += f"""\nNOTE: Previous attempt(s) did not produce enough valid solutions.
+ # Construct instruction with previous best solutions if available
+ instruction = f"""I have uploaded a Python code repository in the directory {self.git_tempdir}. Help solve the following problem.
+
+<problem_description>
+{self.problem_statement}
+</problem_description>
+
+<test_description>
+{self.test_description}
+</test_description>"""
+
+ # Add previous solutions context if available
+ if valid_patches and retry_count > 0:
+ previous_solutions = []
+ for i, (patch, report, score) in enumerate(zip(valid_patches, valid_reports, valid_scores)):
+ previous_solutions.append(f"""
+Previous Solution {i+1}:
+<code_changes>
+{patch}
+</code_changes>
+Test Score: {score}
+Test Report: {report}
+""")
+ instruction += "\n\nPrevious solution attempts:\n" + "\n".join(previous_solutions)
+ instruction += "\nPlease provide a new solution that addresses any limitations in the previous attempts or explores a different approach."
+ elif retry_count > 0:
+ instruction += """\nNOTE: Previous attempt(s) did not produce enough valid solutions.
Please provide a different approach to solve the problem. Your solution must include changes to the main source code files, not just test files."""
+ instruction += f"\n\nYour task is to make changes to the files in the {self.git_tempdir} directory to address the <problem_description>. I have already taken care of the required dependencies."
+
# Run the agent
new_msg_history = chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
@@ -245,6 +262,14 @@ Please provide a different approach to solve the problem. Your solution must inc
valid_patches.append(patch)
valid_reports.append(test_report)
+ valid_scores.append(test_score)
+
+ # Update best score and indices
+ if test_score > best_score:
+ best_score = test_score
+ best_patches_indices = [len(valid_patches) - 1]
+ elif test_score == best_score:
+ best_patches_indices.append(len(valid_patches) - 1)
if len(valid_patches) >= self.num_candidates:
break
@@ -257,25 +282,30 @@ Please provide a different approach to solve the problem. Your solution must inc
safe_log("Failed to generate any valid patches.")
return
- # Use score_tie_breaker to select the best patch
+ # Only use tie-breaker if we have multiple patches with the best score
safe_log(f"\n=== Selecting Best Solution from {len(valid_patches)} Candidates ===")
- best_index = score_tie_breaker(
- self.problem_statement,
- valid_patches,
- valid_reports,
- logging=safe_log
- )
+ if len(best_patches_indices) > 1:
+ safe_log(f"Multiple solutions ({len(best_patches_indices)}) tied for best score {best_score}. Using tie-breaker.")
+ best_index = score_tie_breaker(
+ self.problem_statement,
+ [valid_patches[i] for i in best_patches_indices],
+ [valid_reports[i] for i in best_patches_indices],
+ logging=safe_log
+ )
+ best_index = best_patches_indices[best_index]
+ else:
+ best_index = best_patches_indices[0]
# Reset to base and apply the best patch
reset_to_commit(self.git_tempdir, self.base_commit)
best_patch = valid_patches[best_index]
- safe_log(f"\n=== Applying Best Solution (Candidate {best_index + 1}) ===")
+ safe_log(f"\n=== Applying Best Solution (Candidate {best_index + 1}) with score {valid_scores[best_index]} ===")
apply_patch(self.git_tempdir, best_patch)
# Final validation of the selected patch
final_test_report = self.run_regression_tests(regression_tests_summary)
final_score = get_report_score(final_test_report)
- safe_log(f"Final solution test score: {final_score}")
+ safe_log(f"Final validation test score: {final_score}")
def main():
parser = argparse.ArgumentParser(description=’Process repository with an agentic system.’)-
```

### F.2 Polyglot 上的 DGM

构成 DGM 在 Polyglot 上发现的最佳智能体的 diff 补丁：
```diff
[⬇](data:text/plain;base64,ZGlmZiAtLWdpdCBhL2NvZGluZ19hZ2VudC5weSBiL2NvZGluZ19hZ2VudC5weQppbmRleCAwNGZmYjM2Li42NjM5YWJkIDEwMDY0NAotLS0gYS9jb2RpbmdfYWdlbnQucHkKKysrIGIvY29kaW5nX2FnZW50LnB5CkBAIC00LDYgKzQsOSBAQCBpbXBvcnQgbG9nZ2luZwogZnJvbSBsb2dnaW5nLmhhbmRsZXJzIGltcG9ydCBSb3RhdGluZ0ZpbGVIYW5kbGVyCiBpbXBvcnQgb3MKIGltcG9ydCB0aHJlYWRpbmcKK2ltcG9ydCBqc29uCitmcm9tIGRhdGFjbGFzc2VzIGltcG9ydCBkYXRhY2xhc3MKK2Zyb20gdHlwaW5nIGltcG9ydCBMaXN0LCBPcHRpb25hbAoKIGZyb20gbGxtX3dpdGh0b29scyBpbXBvcnQgQ0xBVURFX01PREVMLCBPUEVOQUlfTU9ERUwsIGNoYXRfd2l0aF9hZ2VudAogZnJvbSB1dGlscy5naXRfdXRpbHMgaW1wb3J0IGRpZmZfdmVyc3VzX2NvbW1pdCwgcmVzZXRfdG9fY29tbWl0LCBhcHBseV9wYXRjaApAQCAtNDIsNiArNDUsMTQgQEAgVEVTVF9DT01NQU5EUyA9IHsKICMgVGhyZWFkLWxvY2FsIHN0b3JhZ2UgZm9yIGxvZ2dlciBpbnN0YW5jZXMKIHRocmVhZF9sb2NhbCA9IHRocmVhZGluZy5sb2NhbCgpCgorQGRhdGFjbGFzcworY2xhc3MgU29sdXRpb25BdHRlbXB0OgorICAgICIiIkNsYXNzIHRvIHN0b3JlIGluZm9ybWF0aW9uIGFib3V0IGEgc29sdXRpb24gYXR0ZW1wdC4iIiIKKyAgICBwYXRjaDogc3RyICAjIFRoZSBwYXRjaCBjb250ZW50CisgICAgdGVzdF9vdXRwdXQ6IHN0ciAgIyBSYXcgdGVzdCBvdXRwdXQKKyAgICB0ZXN0X3N1Y2Nlc3M6IGJvb2wgICMgV2hldGhlciB0ZXN0cyBwYXNzZWQKKyAgICB0ZXN0X3N0YXRzOiBkaWN0ICAjIFRlc3Qgc3RhdGlzdGljcyAoZS5nLiwgbnVtYmVyIG9mIHBhc3NlZC9mYWlsZWQgdGVzdHMpCisKIGRlZiBnZXRfdGhyZWFkX2xvZ2dlcigpOgogICAgICIiIgogICAgIEdldCB0aGUgbG9nZ2VyIGluc3RhbmNlIHNwZWNpZmljIHRvIHRoZSBjdXJyZW50IHRocmVhZC4KQEAgLTEwMiw3ICsxMTMsOCBAQCBjbGFzcyBBZ2VudGljU3lzdGVtOgogICAgICAgICAgICAgY2hhdF9oaXN0b3J5X2ZpbGU9Jy4vY2hhdF9oaXN0b3J5Lm1kJywKICAgICAgICAgICAgIHRlc3RfZGVzY3JpcHRpb249Tm9uZSwKICAgICAgICAgICAgIHNlbGZfaW1wcm92ZT1GYWxzZSwKLSAgICAgICAgICAgIGxhbmd1YWdlPSdweXRob24nCisgICAgICAgICAgICBsYW5ndWFnZT0ncHl0aG9uJywKKyAgICAgICAgICAgIG1heF9hdHRlbXB0cz0zCiAgICAgICAgICk6CiAgICAgICAgIHNlbGYucHJvYmxlbV9zdGF0ZW1lbnQgPSBwcm9ibGVtX3N0YXRlbWVudAogICAgICAgICBzZWxmLmdpdF90ZW1wZGlyID0gZ2l0X3RlbXBkaXIKQEAgLTExMSw2ICsxMjMsNyBAQCBjbGFzcyBBZ2VudGljU3lzdGVtOgogICAgICAgICBzZWxmLnRlc3RfZGVzY3JpcHRpb24gPSB0ZXN0X2Rlc2NyaXB0aW9uCiAgICAgICAgIHNlbGYuc2VsZl9pbXByb3ZlID0gc2VsZl9pbXByb3ZlCiAgICAgICAgIHNlbGYubGFuZ3VhZ2UgPSBsYW5ndWFnZQorICAgICAgICBzZWxmLm1heF9hdHRlbXB0cyA9IG1heF9hdHRlbXB0cwoKICAgICAgICAgIyBTZXQgdGhlIGNvZGUgbW9kZWwgYmFzZWQgb24gd2hldGhlciBzZWxmLWltcHJvdmVtZW50IGlzIGVuYWJsZWQKICAgICAgICAgc2VsZi5jb2RlX21vZGVsID0gT1BFTkFJX01PREVMIGlmIG5vdCBzZWxmX2ltcHJvdmUgZWxzZSBDTEFVREVfTU9ERUwKQEAgLTEzNywxMSArMTUwLDYzIEBAIGNsYXNzIEFnZW50aWNTeXN0ZW06CiAgICAgICAgIF0KICAgICAgICAgcmV0dXJuIG5ld19tc2dfaGlzdG9yeQoKKyAgICBkZWYgcnVuX3Rlc3RzKHNlbGYpIC0+IHR1cGxlW2Jvb2wsIHN0ciwgZGljdF06CisgICAgICAgICIiIlJ1biB0ZXN0cyBhbmQgcmV0dXJuIHN1Y2Nlc3Mgc3RhdHVzLCBvdXRwdXQsIGFuZCB0ZXN0IHN0YXRpc3RpY3MuIiIiCisgICAgICAgIHN1Y2Nlc3MgPSBGYWxzZQorICAgICAgICBvdXRwdXQgPSAiIgorICAgICAgICBzdGF0cyA9IHsicGFzc2VkIjogMCwgImZhaWxlZCI6IDAsICJlcnJvcnMiOiAwLCAidG90YWwiOiAwfQorCisgICAgICAgIHRyeToKKyAgICAgICAgICAgIGZvciBjb21tYW5kIGluIFRFU1RfQ09NTUFORFMuZ2V0KHNlbGYubGFuZ3VhZ2UsIFtdKToKKyAgICAgICAgICAgICAgICBwcm9jID0gc3VicHJvY2Vzcy5ydW4oCisgICAgICAgICAgICAgICAgICAgIGNvbW1hbmQsCisgICAgICAgICAgICAgICAgICAgIGN3ZD1zZWxmLmdpdF90ZW1wZGlyLAorICAgICAgICAgICAgICAgICAgICBjYXB0dXJlX291dHB1dD1UcnVlLAorICAgICAgICAgICAgICAgICAgICB0ZXh0PVRydWUsCisgICAgICAgICAgICAgICAgICAgIGNoZWNrPUZhbHNlCisgICAgICAgICAgICAgICAgKQorICAgICAgICAgICAgICAgIG91dHB1dCArPSBmIiQgeycgJy5qb2luKGNvbW1hbmQpfVxue3Byb2Muc3Rkb3V0fVxue3Byb2Muc3RkZXJyfVxuIgorICAgICAgICAgICAgICAgIHN1Y2Nlc3MgPSBwcm9jLnJldHVybmNvZGUgPT0gMAorICAgICAgICAgICAgICAgIGlmIG5vdCBzdWNjZXNzOgorICAgICAgICAgICAgICAgICAgICBicmVhaworCisgICAgICAgICAgICAjIFRyeSB0byBleHRyYWN0IHRlc3Qgc3RhdGlzdGljcyBmcm9tIG91dHB1dAorICAgICAgICAgICAgIyBUaGlzIGlzIGEgc2ltcGxlIGV4YW1wbGU7IHlvdSBtaWdodCB3YW50IHRvIGFkZCBtb3JlIHNvcGhpc3RpY2F0ZWQgcGFyc2luZworICAgICAgICAgICAgc3RhdHNbInBhc3NlZCJdID0gb3V0cHV0LmNvdW50KCJQQVNTIikgKyBvdXRwdXQuY291bnQoIm9rIikKKyAgICAgICAgICAgIHN0YXRzWyJmYWlsZWQiXSA9IG91dHB1dC5jb3VudCgiRkFJTCIpICsgb3V0cHV0LmNvdW50KCJub3Qgb2siKQorICAgICAgICAgICAgc3RhdHNbImVycm9ycyJdID0gb3V0cHV0LmNvdW50KCJFUlJPUiIpICsgb3V0cHV0LmNvdW50KCJwYW5pYzoiKQorICAgICAgICAgICAgc3RhdHNbInRvdGFsIl0gPSBzdGF0c1sicGFzc2VkIl0gKyBzdGF0c1siZmFpbGVkIl0gKyBzdGF0c1siZXJyb3JzIl0KKworICAgICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CisgICAgICAgICAgICBvdXRwdXQgPSBmIkVycm9yIHJ1bm5pbmcgdGVzdHM6IHtzdHIoZSl9IgorICAgICAgICAgICAgc3VjY2VzcyA9IEZhbHNlCisKKyAgICAgICAgcmV0dXJuIHN1Y2Nlc3MsIG91dHB1dCwgc3RhdHMKKworICAgIGRlZiBhbmFseXplX3Rlc3RfcmVzdWx0cyhzZWxmLCBhdHRlbXB0czogTGlzdFtTb2x1dGlvbkF0dGVtcHRdKSAtPiBzdHI6CisgICAgICAgICIiIkFuYWx5emUgdGVzdCByZXN1bHRzIGFuZCBjcmVhdGUgYSBzdW1tYXJ5IGZvciB0aGUgYWdlbnQuIiIiCisgICAgICAgIHN1bW1hcnkgPSAiIyBUZXN0IFJlc3VsdHMgQW5hbHlzaXNcblxuIgorCisgICAgICAgIGZvciBpLCBhdHRlbXB0IGluIGVudW1lcmF0ZShhdHRlbXB0cywgMSk6CisgICAgICAgICAgICBzdW1tYXJ5ICs9IGYiIyMgQXR0ZW1wdCB7aX1cbiIKKyAgICAgICAgICAgIHN1bW1hcnkgKz0gZiJUZXN0IFN1Y2Nlc3M6IHthdHRlbXB0LnRlc3Rfc3VjY2Vzc31cbiIKKyAgICAgICAgICAgIHN1bW1hcnkgKz0gZiJUZXN0IFN0YXRzOiB7anNvbi5kdW1wcyhhdHRlbXB0LnRlc3Rfc3RhdHMsIGluZGVudD0yKX1cbiIKKyAgICAgICAgICAgIHN1bW1hcnkgKz0gIktleSB0ZXN0IG91dHB1dDpcbmBgYFxuIgorICAgICAgICAgICAgIyBFeHRyYWN0IHJlbGV2YW50IHBhcnRzIG9mIHRlc3Qgb3V0cHV0IChlLmcuLCBlcnJvciBtZXNzYWdlcykKKyAgICAgICAgICAgIGtleV9vdXRwdXQgPSAiXG4iLmpvaW4obGluZSBmb3IgbGluZSBpbiBhdHRlbXB0LnRlc3Rfb3V0cHV0LnNwbGl0KCJcbiIpCisgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiAiRkFJTCIgaW4gbGluZSBvciAiRVJST1IiIGluIGxpbmUgb3IgIlBBU1MiIGluIGxpbmUpCisgICAgICAgICAgICBzdW1tYXJ5ICs9IGYie2tleV9vdXRwdXR9XG5gYGBcblxuIgorCisgICAgICAgIHJldHVybiBzdW1tYXJ5CisKICAgICBkZWYgZm9yd2FyZChzZWxmKToKICAgICAgICAgIiIiCi0gICAgICAgIFRoZSBmb3J3YXJkIGZ1bmN0aW9uIGZvciB0aGUgQWdlbnRpY1N5c3RlbS4KKyAgICAgICAgVGhlIGZvcndhcmQgZnVuY3Rpb24gZm9yIHRoZSBBZ2VudGljU3lzdGVtIHdpdGggbXVsdGlwbGUgc29sdXRpb24gYXR0ZW1wdHMuCiAgICAgICAgICIiIgotICAgICAgICB0YXNrID0gZiIiIkkgaGF2ZSB1cGxvYWRlZCBhIGNvZGUgcmVwb3NpdG9yeSBpbiB0aGUgZGlyZWN0b3J5IHtzZWxmLmdpdF90ZW1wZGlyfS4gSGVscCBzb2x2ZSB0aGUgZm9sbG93aW5nIHByb2JsZW0uCisgICAgICAgIGF0dGVtcHRzOiBMaXN0W1NvbHV0aW9uQXR0ZW1wdF0gPSBbXQorICAgICAgICBiZXN0X2F0dGVtcHQ6IE9wdGlvbmFsW1NvbHV0aW9uQXR0ZW1wdF0gPSBOb25lCisKKyAgICAgICAgYmFzZV90YXNrID0gZiIiIkkgaGF2ZSB1cGxvYWRlZCBhIGNvZGUgcmVwb3NpdG9yeSBpbiB0aGUgZGlyZWN0b3J5IHtzZWxmLmdpdF90ZW1wZGlyfS4gSGVscCBzb2x2ZSB0aGUgZm9sbG93aW5nIHByb2JsZW0uCgogPHByb2JsZW1fZGVzY3JpcHRpb24+CiB7c2VsZi5wcm9ibGVtX3N0YXRlbWVudH0KQEAgLTE0OSw4ICsyMTQsNTIgQEAgY2xhc3MgQWdlbnRpY1N5c3RlbToKCiBZb3VyIHRhc2sgaXMgdG8gbWFrZSBjaGFuZ2VzIHRvIHRoZSBmaWxlcyBpbiB0aGUge3NlbGYuZ2l0X3RlbXBkaXJ9IGRpcmVjdG9yeSB0byBhZGRyZXNzIHRoZSA8cHJvYmxlbV9kZXNjcmlwdGlvbj4uIEkgaGF2ZSBhbHJlYWR5IHRha2VuIGNhcmUgb2YgdGhlIHJlcXVpcmVkIGRlcGVuZGVuY2llcy4KICIiIgotICAgICAgICBpbnN0cnVjdGlvbiA9IGYie3Rhc2t9XG5cblBsZWFzZSBhbmFseXplIHRoZSBwcm9ibGVtIGRlc2NyaXB0aW9uIGNhcmVmdWxseS4gVGhlbiBtYWtlIGVkaXRzIHRvIHRoZSBjb2RlIGZpbGVzIHRvIGNvbXBsZXRlIHRoZSBpbnN0cnVjdGlvbi4iCi0gICAgICAgIGluaXRfZWRpdCA9IGNoYXRfd2l0aF9hZ2VudChpbnN0cnVjdGlvbiwgbW9kZWw9c2VsZi5jb2RlX21vZGVsLCBtc2dfaGlzdG9yeT1bXSwgbG9nZ2luZz1zYWZlX2xvZykKKworICAgICAgICBmb3IgYXR0ZW1wdF9udW0gaW4gcmFuZ2Uoc2VsZi5tYXhfYXR0ZW1wdHMpOgorICAgICAgICAgICAgIyBSZXNldCB0byBiYXNlIGNvbW1pdCBmb3IgZWFjaCBhdHRlbXB0CisgICAgICAgICAgICByZXNldF90b19jb21taXQoc2VsZi5naXRfdGVtcGRpciwgc2VsZi5iYXNlX2NvbW1pdCkKKworICAgICAgICAgICAgIyBQcmVwYXJlIHRoZSBpbnN0cnVjdGlvbiBiYXNlZCBvbiBwcmV2aW91cyBhdHRlbXB0cworICAgICAgICAgICAgaW5zdHJ1Y3Rpb24gPSBiYXNlX3Rhc2sKKyAgICAgICAgICAgIGlmIGF0dGVtcHRzOgorICAgICAgICAgICAgICAgICMgQWRkIGFuYWx5c2lzIG9mIHByZXZpb3VzIGF0dGVtcHRzCisgICAgICAgICAgICAgICAgaW5zdHJ1Y3Rpb24gKz0gIlxuXG5QcmV2aW91cyBzb2x1dGlvbiBhdHRlbXB0cyBoYXZlIGJlZW4gbWFkZS4gSGVyZSBhcmUgdGhlIHJlc3VsdHM6XG5cbiIKKyAgICAgICAgICAgICAgICBpbnN0cnVjdGlvbiArPSBzZWxmLmFuYWx5emVfdGVzdF9yZXN1bHRzKGF0dGVtcHRzKQorICAgICAgICAgICAgICAgIGluc3RydWN0aW9uICs9ICJcblBsZWFzZSBhbmFseXplIHRoZXNlIHJlc3VsdHMgYW5kIHByb3ZpZGUgYW4gaW1wcm92ZWQgc29sdXRpb24gdGhhdCBhZGRyZXNzZXMgdGhlIGlzc3VlcyBmb3VuZC4iCisgICAgICAgICAgICBlbHNlOgorICAgICAgICAgICAgICAgIGluc3RydWN0aW9uICs9ICJcblxuUGxlYXNlIGFuYWx5emUgdGhlIHByb2JsZW0gZGVzY3JpcHRpb24gY2FyZWZ1bGx5LiBUaGVuIG1ha2UgZWRpdHMgdG8gdGhlIGNvZGUgZmlsZXMgdG8gY29tcGxldGUgdGhlIGluc3RydWN0aW9uLiIKKworICAgICAgICAgICAgIyBHZXQgdGhlIHNvbHV0aW9uIGF0dGVtcHQKKyAgICAgICAgICAgIGNoYXRfd2l0aF9hZ2VudChpbnN0cnVjdGlvbiwgbW9kZWw9c2VsZi5jb2RlX21vZGVsLCBtc2dfaGlzdG9yeT1bXSwgbG9nZ2luZz1zYWZlX2xvZykKKworICAgICAgICAgICAgIyBDYXB0dXJlIHRoZSBjdXJyZW50IHBhdGNoCisgICAgICAgICAgICBjdXJyZW50X3BhdGNoID0gZGlmZl92ZXJzdXNfY29tbWl0KHNlbGYuZ2l0X3RlbXBkaXIsIHNlbGYuYmFzZV9jb21taXQpCisKKyAgICAgICAgICAgICMgUnVuIHRlc3RzIGFuZCBjb2xsZWN0IHJlc3VsdHMKKyAgICAgICAgICAgIHRlc3Rfc3VjY2VzcywgdGVzdF9vdXRwdXQsIHRlc3Rfc3RhdHMgPSBzZWxmLnJ1bl90ZXN0cygpCisKKyAgICAgICAgICAgICMgQ3JlYXRlIGFuZCBzdG9yZSBhdHRlbXB0CisgICAgICAgICAgICBhdHRlbXB0ID0gU29sdXRpb25BdHRlbXB0KAorICAgICAgICAgICAgICAgIHBhdGNoPWN1cnJlbnRfcGF0Y2gsCisgICAgICAgICAgICAgICAgdGVzdF9vdXRwdXQ9dGVzdF9vdXRwdXQsCisgICAgICAgICAgICAgICAgdGVzdF9zdWNjZXNzPXRlc3Rfc3VjY2VzcywKKyAgICAgICAgICAgICAgICB0ZXN0X3N0YXRzPXRlc3Rfc3RhdHMKKyAgICAgICAgICAgICkKKyAgICAgICAgICAgIGF0dGVtcHRzLmFwcGVuZChhdHRlbXB0KQorCisgICAgICAgICAgICAjIFVwZGF0ZSBiZXN0IGF0dGVtcHQgaWYgdGhpcyBvbmUgaXMgYmV0dGVyCisgICAgICAgICAgICBpZiB0ZXN0X3N1Y2Nlc3MgYW5kIChiZXN0X2F0dGVtcHQgaXMgTm9uZSBvcgorICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGF0dGVtcHQudGVzdF9zdGF0c1sicGFzc2VkIl0gPiBiZXN0X2F0dGVtcHQudGVzdF9zdGF0c1sicGFzc2VkIl0pOgorICAgICAgICAgICAgICAgIGJlc3RfYXR0ZW1wdCA9IGF0dGVtcHQKKworICAgICAgICAgICAgIyBJZiB0ZXN0cyBwYXNzIHBlcmZlY3RseSwgd2UgY2FuIHN0b3AKKyAgICAgICAgICAgIGlmIHRlc3Rfc3VjY2VzcyBhbmQgYXR0ZW1wdC50ZXN0X3N0YXRzWyJmYWlsZWQiXSA9PSAwIGFuZCBhdHRlbXB0LnRlc3Rfc3RhdHNbImVycm9ycyJdID09IDA6CisgICAgICAgICAgICAgICAgYnJlYWsKKworICAgICAgICAjIEFwcGx5IHRoZSBiZXN0IHNvbHV0aW9uIGlmIGZvdW5kLCBvdGhlcndpc2UgdXNlIHRoZSBsYXN0IGF0dGVtcHQKKyAgICAgICAgZmluYWxfYXR0ZW1wdCA9IGJlc3RfYXR0ZW1wdCBvciBhdHRlbXB0c1stMV0KKyAgICAgICAgcmVzZXRfdG9fY29tbWl0KHNlbGYuZ2l0X3RlbXBkaXIsIHNlbGYuYmFzZV9jb21taXQpCisgICAgICAgIGFwcGx5X3BhdGNoKHNlbGYuZ2l0X3RlbXBkaXIsIGZpbmFsX2F0dGVtcHQucGF0Y2gpCgogZGVmIG1haW4oKToKICAgICBwYXJzZXIgPSBhcmdwYXJzZS5Bcmd1bWVudFBhcnNlcihkZXNjcmlwdGlvbj0nUHJvY2VzcyByZXBvc2l0b3J5IHdpdGggYW4gYWdlbnRpYyBzeXN0ZW0uJykKQEAgLTE2Miw2ICsyNzEsNyBAQCBkZWYgbWFpbigpOgogICAgIHBhcnNlci5hZGRfYXJndW1lbnQoJy0tdGVzdF9kZXNjcmlwdGlvbicsIGRlZmF1bHQ9Tm9uZSwgcmVxdWlyZWQ9RmFsc2UsIGhlbHA9J0Rlc2NyaXB0aW9uIG9mIGhvdyB0byB0ZXN0IHRoZSByZXBvc2l0b3J5JykKICAgICBwYXJzZXIuYWRkX2FyZ3VtZW50KCctLXNlbGZfaW1wcm92ZScsIGRlZmF1bHQ9RmFsc2UsIGFjdGlvbj0nc3RvcmVfdHJ1ZScsIGhlbHA9J1doZXRoZXIgdG8gc2VsZi1pbXByb3ZlIHRoZSByZXBvc2l0b3J5IG9yIHNvbHZpbmcgc3dlJykKICAgICBwYXJzZXIuYWRkX2FyZ3VtZW50KCctLWxhbmd1YWdlJywgcmVxdWlyZWQ9RmFsc2UsIGRlZmF1bHQ9InB5dGhvbiIsIGNob2ljZXM9WydjcHAnLCAnamF2YScsICdweXRob24nLCAnZ28nLCAncnVzdCcsICdqYXZhc2NyaXB0J10sIGhlbHA9J1Rhc2tcJ3MgcHJvZ3JhbW1pbmcgbGFuZ3VhZ2UnKQorICAgIHBhcnNlci5hZGRfYXJndW1lbnQoJy0tbWF4X2F0dGVtcHRzJywgdHlwZT1pbnQsIGRlZmF1bHQ9MywgaGVscD0nTWF4aW11bSBudW1iZXIgb2Ygc29sdXRpb24gYXR0ZW1wdHMnKQogICAgIGFyZ3MgPSBwYXJzZXIucGFyc2VfYXJncygpCgogICAgICMgUHJvY2VzcyB0aGUgcmVwb3NpdG9yeQpAQCAtMTczLDYgKzI4Myw3IEBAIGRlZiBtYWluKCk6CiAgICAgICAgIHRlc3RfZGVzY3JpcHRpb249YXJncy50ZXN0X2Rlc2NyaXB0aW9uLAogICAgICAgICBzZWxmX2ltcHJvdmU9YXJncy5zZWxmX2ltcHJvdmUsCiAgICAgICAgIGxhbmd1YWdlPWFyZ3MubGFuZ3VhZ2UsCisgICAgICAgIG1heF9hdHRlbXB0cz1hcmdzLm1heF9hdHRlbXB0cywKICAgICApCgogICAgICMgUnVuIHRoZSBhZ2VudGljIHN5c3RlbSB0byB0cnkgdG8gc29sdmUgdGhlIHByb2JsZW0KQEAgLTE4NSw0ICsyOTYsNCBAQCBkZWYgbWFpbigpOgogICAgICAgICBmLndyaXRlKG1vZGVsX3BhdGNoKQoKIGlmIF9fbmFtZV9fID09ICJfX21haW5fXyI6Ci0gICAgbWFpbigpCisgICAgbWFpbigpClwgTm8gbmV3bGluZSBhdCBlbmQgb2YgZmlsZQ==)
diff --git a/coding_agent.py b/coding_agent.py
index 04ffb36..6639abd 100644
--- a/coding_agent.py
+++ b/coding_agent.py
@@ -4,6 +4,9 @@ import logging
from logging.handlers import RotatingFileHandler
import os
import threading
+import json
+from dataclasses import dataclass
+from typing import List, Optional
from llm_withtools import CLAUDE_MODEL, OPENAI_MODEL, chat_with_agent
from utils.git_utils import diff_versus_commit, reset_to_commit, apply_patch
@@ -42,6 +45,14 @@ TEST_COMMANDS = {
# Thread-local storage for logger instances
thread_local = threading.local()
+@dataclass
+class SolutionAttempt:
+ """Class to store information about a solution attempt."""
+ patch: str # The patch content
+ test_output: str # Raw test output
+ test_success: bool # Whether tests passed
+ test_stats: dict # Test statistics (e.g., number of passed/failed tests)
+
def get_thread_logger():
"""
Get the logger instance specific to the current thread.
@@ -102,7 +113,8 @@ class AgenticSystem:
chat_history_file=’./chat_history.md’,
test_description=None,
self_improve=False,
- language=’python’
+ language=’python’,
+ max_attempts=3
):
self.problem_statement = problem_statement
self.git_tempdir = git_tempdir
@@ -111,6 +123,7 @@ class AgenticSystem:
self.test_description = test_description
self.self_improve = self_improve
self.language = language
+ self.max_attempts = max_attempts
# Set the code model based on whether self-improvement is enabled
self.code_model = OPENAI_MODEL if not self_improve else CLAUDE_MODEL
@@ -137,11 +150,63 @@ class AgenticSystem:
]
return new_msg_history
+ def run_tests(self) -> tuple[bool, str, dict]:
+ """Run tests and return success status, output, and test statistics."""
+ success = False
+ output = ""
+ stats = {"passed": 0, "failed": 0, "errors": 0, "total": 0}
+
+ try:
+ for command in TEST_COMMANDS.get(self.language, []):
+ proc = subprocess.run(
+ command,
+ cwd=self.git_tempdir,
+ capture_output=True,
+ text=True,
+ check=False
+ )
+ output += f"$ {’ ’.join(command)}\n{proc.stdout}\n{proc.stderr}\n"
+ success = proc.returncode == 0
+ if not success:
+ break
+
+ # Try to extract test statistics from output
+ # This is a simple example; you might want to add more sophisticated parsing
+ stats["passed"] = output.count("PASS") + output.count("ok")
+ stats["failed"] = output.count("FAIL") + output.count("not ok")
+ stats["errors"] = output.count("ERROR") + output.count("panic:")
+ stats["total"] = stats["passed"] + stats["failed"] + stats["errors"]
+
+ except Exception as e:
+ output = f"Error running tests: {str(e)}"
+ success = False
+
+ return success, output, stats
+
+ def analyze_test_results(self, attempts: List[SolutionAttempt]) -> str:
+ """Analyze test results and create a summary for the agent."""
+ summary = "# Test Results Analysis\n\n"
+
+ for i, attempt in enumerate(attempts, 1):
+ summary += f"## Attempt {i}\n"
+ summary += f"Test Success: {attempt.test_success}\n"
+ summary += f"Test Stats: {json.dumps(attempt.test_stats, indent=2)}\n"
+ summary += "Key test output:\n‘‘‘\n"
+ # Extract relevant parts of test output (e.g., error messages)
+ key_output = "\n".join(line for line in attempt.test_output.split("\n")
+ if "FAIL" in line or "ERROR" in line or "PASS" in line)
+ summary += f"{key_output}\n‘‘‘\n\n"
+
+ return summary
+
def forward(self):
"""
- The forward function for the AgenticSystem.
+ The forward function for the AgenticSystem with multiple solution attempts.
"""
- task = f"""I have uploaded a code repository in the directory {self.git_tempdir}. Help solve the following problem.
+ attempts: List[SolutionAttempt] = []
+ best_attempt: Optional[SolutionAttempt] = None
+
+ base_task = f"""I have uploaded a code repository in the directory {self.git_tempdir}. Help solve the following problem.
<problem_description>
{self.problem_statement}
@@ -149,8 +214,52 @@ class AgenticSystem:
Your task is to make changes to the files in the {self.git_tempdir} directory to address the <problem_description>. I have already taken care of the required dependencies.
"""
- instruction = f"{task}\n\nPlease analyze the problem description carefully. Then make edits to the code files to complete the instruction."
- init_edit = chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
+
+ for attempt_num in range(self.max_attempts):
+ # Reset to base commit for each attempt
+ reset_to_commit(self.git_tempdir, self.base_commit)
+
+ # Prepare the instruction based on previous attempts
+ instruction = base_task
+ if attempts:
+ # Add analysis of previous attempts
+ instruction += "\n\nPrevious solution attempts have been made. Here are the results:\n\n"
+ instruction += self.analyze_test_results(attempts)
+ instruction += "\nPlease analyze these results and provide an improved solution that addresses the issues found."
+ else:
+ instruction += "\n\nPlease analyze the problem description carefully. Then make edits to the code files to complete the instruction."
+
+ # Get the solution attempt
+ chat_with_agent(instruction, model=self.code_model, msg_history=[], logging=safe_log)
+
+ # Capture the current patch
+ current_patch = diff_versus_commit(self.git_tempdir, self.base_commit)
+
+ # Run tests and collect results
+ test_success, test_output, test_stats = self.run_tests()
+
+ # Create and store attempt
+ attempt = SolutionAttempt(
+ patch=current_patch,
+ test_output=test_output,
+ test_success=test_success,
+ test_stats=test_stats
+ )
+ attempts.append(attempt)
+
+ # Update best attempt if this one is better
+ if test_success and (best_attempt is None or
+ attempt.test_stats["passed"] > best_attempt.test_stats["passed"]):
+ best_attempt = attempt
+
+ # If tests pass perfectly, we can stop
+ if test_success and attempt.test_stats["failed"] == 0 and attempt.test_stats["errors"] == 0:
+ break
+
+ # Apply the best solution if found, otherwise use the last attempt
+ final_attempt = best_attempt or attempts[-1]
+ reset_to_commit(self.git_tempdir, self.base_commit)
+ apply_patch(self.git_tempdir, final_attempt.patch)
def main():
parser = argparse.ArgumentParser(description=’Process repository with an agentic system.’)
@@ -162,6 +271,7 @@ def main():
parser.add_argument(’--test_description’, default=None, required=False, help=’Description of how to test the repository’)
parser.add_argument(’--self_improve’, default=False, action=’store_true’, help=’Whether to self-improve the repository or solving swe’)
parser.add_argument(’--language’, required=False, default="python", choices=[’cpp’, ’java’, ’python’, ’go’, ’rust’, ’javascript’], help=’Task\’s programming language’)
+ parser.add_argument(’--max_attempts’, type=int, default=3, help=’Maximum number of solution attempts’)
args = parser.parse_args()
# Process the repository
@@ -173,6 +283,7 @@ def main():
test_description=args.test_description,
self_improve=args.self_improve,
language=args.language,
+ max_attempts=args.max_attempts,
)
# Run the agentic system to try to solve the problem
@@ -185,4 +296,4 @@ def main():
f.write(model_patch)
if __name__ == "__main__":
- main()
+ main()
\ No newline at end of file+
[⬇](data:text/plain;base64,ZGlmZiAtLWdpdCBhL3Rvb2xzL2VkaXQucHkgYi90b29scy9lZGl0LnB5CmluZGV4IGQ3MTg0YzMuLjg3ZmE0MDggMTAwNjQ0Ci0tLSBhL3Rvb2xzL2VkaXQucHkKKysrIGIvdG9vbHMvZWRpdC5weQpAQCAtMSw1ICsxLDkgQEAKIGZyb20gcGF0aGxpYiBpbXBvcnQgUGF0aAogaW1wb3J0IHN1YnByb2Nlc3MKK2Zyb20gdHlwaW5nIGltcG9ydCBMaXN0LCBPcHRpb25hbCwgRGljdAorCisjIEdsb2JhbCBlZGl0IGhpc3RvcnkgZm9yIHVuZG8gZnVuY3Rpb25hbGl0eQorZWRpdF9oaXN0b3J5OiBEaWN0W3N0ciwgTGlzdFtzdHJdXSA9IHt9CgogZGVmIHRvb2xfaW5mbygpOgogICAgIHJldHVybiB7CkBAIC0xMCwxNCArMTQsMTQgQEAgZGVmIHRvb2xfaW5mbygpOgogKiBUaGUgYGNyZWF0ZWAgY29tbWFuZCBjYW5ub3QgYmUgdXNlZCBpZiB0aGUgc3BlY2lmaWVkIGBwYXRoYCBhbHJlYWR5IGV4aXN0cyBhcyBhIGZpbGUuXG4KICogSWYgYSBgY29tbWFuZGAgZ2VuZXJhdGVzIGEgbG9uZyBvdXRwdXQsIGl0IHdpbGwgYmUgdHJ1bmNhdGVkIGFuZCBtYXJrZWQgd2l0aCBgPHJlc3BvbnNlIGNsaXBwZWQ+YC5cbgogKiBUaGUgYGVkaXRgIGNvbW1hbmQgb3ZlcndyaXRlcyB0aGUgZW50aXJlIGZpbGUgd2l0aCB0aGUgcHJvdmlkZWQgYGZpbGVfdGV4dGAuXG4KLSogTm8gcGFydGlhbC9saW5lLXJhbmdlIGVkaXRzIG9yIHBhcnRpYWwgdmlld2luZyBhcmUgc3VwcG9ydGVkLiIiIiwKKyogQWxzbyBzdXBwb3J0cyB2aWV3aW5nIHNwZWNpZmljIGxpbmUgcmFuZ2VzLCBzdHJpbmcgcmVwbGFjZW1lbnQsIHRleHQgaW5zZXJ0aW9uLCBhbmQgdW5kbyBvcGVyYXRpb25zLiIiIiwKICAgICAgICAgImlucHV0X3NjaGVtYSI6IHsKICAgICAgICAgICAgICJ0eXBlIjogIm9iamVjdCIsCiAgICAgICAgICAgICAicHJvcGVydGllcyI6IHsKICAgICAgICAgICAgICAgICAiY29tbWFuZCI6IHsKICAgICAgICAgICAgICAgICAgICAgInR5cGUiOiAic3RyaW5nIiwKLSAgICAgICAgICAgICAgICAgICAgImVudW0iOiBbInZpZXciLCAiY3JlYXRlIiwgImVkaXQiXSwKLSAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIlRoZSBjb21tYW5kIHRvIHJ1bjogYHZpZXdgLCBgY3JlYXRlYCwgb3IgYGVkaXRgLiIKKyAgICAgICAgICAgICAgICAgICAgImVudW0iOiBbInZpZXciLCAiY3JlYXRlIiwgImVkaXQiLCAic3RyX3JlcGxhY2UiLCAiaW5zZXJ0IiwgInVuZG9fZWRpdCJdLAorICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiVGhlIGNvbW1hbmQgdG8gcnVuOiBgdmlld2AsIGBjcmVhdGVgLCBgZWRpdGAsIGBzdHJfcmVwbGFjZWAsIGBpbnNlcnRgLCBvciBgdW5kb19lZGl0YC4iCiAgICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICAicGF0aCI6IHsKICAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIkFic29sdXRlIHBhdGggdG8gZmlsZSBvciBkaXJlY3RvcnksIGUuZy4gYC9yZXBvL2ZpbGUucHlgIG9yIGAvcmVwb2AuIiwKQEAgLTI2LDYgKzMwLDIzIEBAIGRlZiB0b29sX2luZm8oKToKICAgICAgICAgICAgICAgICAiZmlsZV90ZXh0IjogewogICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiUmVxdWlyZWQgcGFyYW1ldGVyIG9mIGBjcmVhdGVgIG9yIGBlZGl0YCBjb21tYW5kLCBjb250YWluaW5nIHRoZSBjb250ZW50IGZvciB0aGUgZW50aXJlIGZpbGUuIiwKICAgICAgICAgICAgICAgICAgICAgInR5cGUiOiAic3RyaW5nIgorICAgICAgICAgICAgICAgIH0sCisgICAgICAgICAgICAgICAgInZpZXdfcmFuZ2UiOiB7CisgICAgICAgICAgICAgICAgICAgICJkZXNjcmlwdGlvbiI6ICJPcHRpb25hbCBwYXJhbWV0ZXIgZm9yIGB2aWV3YCBjb21tYW5kIHRvIGRpc3BsYXkgc3BlY2lmaWMgbGluZSByYW5nZSBbc3RhcnQsIGVuZF0uIiwKKyAgICAgICAgICAgICAgICAgICAgInR5cGUiOiAiYXJyYXkiLAorICAgICAgICAgICAgICAgICAgICAiaXRlbXMiOiB7InR5cGUiOiAiaW50ZWdlciJ9CisgICAgICAgICAgICAgICAgfSwKKyAgICAgICAgICAgICAgICAib2xkX3N0ciI6IHsKKyAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIlJlcXVpcmVkIHBhcmFtZXRlciBmb3IgYHN0cl9yZXBsYWNlYCBjb21tYW5kLCBzdHJpbmcgdG8gcmVwbGFjZS4iLAorICAgICAgICAgICAgICAgICAgICAidHlwZSI6ICJzdHJpbmciCisgICAgICAgICAgICAgICAgfSwKKyAgICAgICAgICAgICAgICAibmV3X3N0ciI6IHsKKyAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIlJlcXVpcmVkIHBhcmFtZXRlciBmb3IgYHN0cl9yZXBsYWNlYCBhbmQgYGluc2VydGAgY29tbWFuZHMsIG5ldyBzdHJpbmcgdG8gaW5zZXJ0LiIsCisgICAgICAgICAgICAgICAgICAgICJ0eXBlIjogInN0cmluZyIKKyAgICAgICAgICAgICAgICB9LAorICAgICAgICAgICAgICAgICJpbnNlcnRfbGluZSI6IHsKKyAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIlJlcXVpcmVkIHBhcmFtZXRlciBmb3IgYGluc2VydGAgY29tbWFuZCwgbGluZSBudW1iZXIgd2hlcmUgdG8gaW5zZXJ0IHRleHQuIiwKKyAgICAgICAgICAgICAgICAgICAgInR5cGUiOiAiaW50ZWdlciIKICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICB9LAogICAgICAgICAgICAgInJlcXVpcmVkIjogWyJjb21tYW5kIiwgInBhdGgiXQpAQCAtNDMsNyArNjQsNyBAQCBkZWYgdmFsaWRhdGVfcGF0aChwYXRoOiBzdHIsIGNvbW1hbmQ6IHN0cikgLT4gUGF0aDoKICAgICBWYWxpZGF0ZSB0aGUgZmlsZSBwYXRoIGZvciBlYWNoIGNvbW1hbmQ6CiAgICAgICAtICd2aWV3JzogcGF0aCBtYXkgYmUgYSBmaWxlIG9yIGRpcmVjdG9yeTsgbXVzdCBleGlzdC4KICAgICAgIC0gJ2NyZWF0ZSc6IHBhdGggbXVzdCBub3QgZXhpc3QgKGZvciBuZXcgZmlsZSBjcmVhdGlvbikuCi0gICAgICAtICdlZGl0JzogcGF0aCBtdXN0IGV4aXN0IChmb3Igb3ZlcndyaXRpbmcpLgorICAgICAgLSBPdGhlcnM6IHBhdGggbXVzdCBleGlzdCBhcyBhIGZpbGUuCiAgICAgIiIiCiAgICAgcGF0aF9vYmogPSBQYXRoKHBhdGgpCgpAQCAtNjEsMTQgKzgyLDEyIEBAIGRlZiB2YWxpZGF0ZV9wYXRoKHBhdGg6IHN0ciwgY29tbWFuZDogc3RyKSAtPiBQYXRoOgogICAgICAgICAjIFBhdGggbXVzdCBub3QgZXhpc3QKICAgICAgICAgaWYgcGF0aF9vYmouZXhpc3RzKCk6CiAgICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKGYiQ2Fubm90IGNyZWF0ZSBuZXcgZmlsZTsge3BhdGh9IGFscmVhZHkgZXhpc3RzLiIpCi0gICAgZWxpZiBjb21tYW5kID09ICJlZGl0IjoKKyAgICBlbHNlOgogICAgICAgICAjIFBhdGggbXVzdCBleGlzdCBhbmQgbXVzdCBiZSBhIGZpbGUKICAgICAgICAgaWYgbm90IHBhdGhfb2JqLmV4aXN0cygpOgogICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIlRoZSBmaWxlIHtwYXRofSBkb2VzIG5vdCBleGlzdC4iKQogICAgICAgICBpZiBwYXRoX29iai5pc19kaXIoKToKICAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJ7cGF0aH0gaXMgYSBkaXJlY3RvcnkgYW5kIGNhbm5vdCBiZSBlZGl0ZWQgYXMgYSBmaWxlLiIpCi0gICAgZWxzZToKLSAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIlVua25vd24gb3IgdW5zdXBwb3J0ZWQgY29tbWFuZDoge2NvbW1hbmR9IikKCiAgICAgcmV0dXJuIHBhdGhfb2JqCgpAQCAtODksMTQgKzEwOCwyMSBAQCBkZWYgcmVhZF9maWxlKHBhdGg6IFBhdGgpIC0+IHN0cjoKICAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CiAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJGYWlsZWQgdG8gcmVhZCBmaWxlOiB7ZX0iKQoKLWRlZiB3cml0ZV9maWxlKHBhdGg6IFBhdGgsIGNvbnRlbnQ6IHN0cik6CitkZWYgd3JpdGVfZmlsZShwYXRoOiBQYXRoLCBjb250ZW50OiBzdHIsIHNhdmVfaGlzdG9yeTogYm9vbCA9IFRydWUpOgogICAgICIiIldyaXRlIChvdmVyd3JpdGUpIGVudGlyZSBmaWxlIGNvbnRlbnRzLiIiIgogICAgIHRyeToKKyAgICAgICAgaWYgc2F2ZV9oaXN0b3J5OgorICAgICAgICAgICAgIyBTYXZlIHRoZSBjdXJyZW50IGNvbnRlbnQgdG8gaGlzdG9yeSBiZWZvcmUgd3JpdGluZworICAgICAgICAgICAgaWYgcGF0aC5leGlzdHMoKToKKyAgICAgICAgICAgICAgICBpZiBzdHIocGF0aCkgbm90IGluIGVkaXRfaGlzdG9yeToKKyAgICAgICAgICAgICAgICAgICAgZWRpdF9oaXN0b3J5W3N0cihwYXRoKV0gPSBbXQorICAgICAgICAgICAgICAgIGVkaXRfaGlzdG9yeVtzdHIocGF0aCldLmFwcGVuZChwYXRoLnJlYWRfdGV4dCgpKQorCiAgICAgICAgIHBhdGgud3JpdGVfdGV4dChjb250ZW50KQogICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIkZhaWxlZCB0byB3cml0ZSBmaWxlOiB7ZX0iKQoKLWRlZiB2aWV3X3BhdGgocGF0aF9vYmo6IFBhdGgpIC0+IHN0cjoKK2RlZiB2aWV3X3BhdGgocGF0aF9vYmo6IFBhdGgsIHZpZXdfcmFuZ2U6IE9wdGlvbmFsW0xpc3RbaW50XV0gPSBOb25lKSAtPiBzdHI6CiAgICAgIiIiVmlldyB0aGUgZW50aXJlIGZpbGUgY29udGVudHMgb3IgZGlyZWN0b3J5IGxpc3RpbmcuIiIiCiAgICAgaWYgcGF0aF9vYmouaXNfZGlyKCk6CiAgICAgICAgICMgRm9yIGRpcmVjdG9yaWVzOiBsaXN0IG5vbi1oaWRkZW4gZmlsZXMgdXAgdG8gMiBsZXZlbHMgZGVlcApAQCAtMTE1LDM1ICsxNDEsMTA0IEBAIGRlZiB2aWV3X3BhdGgocGF0aF9vYmo6IFBhdGgpIC0+IHN0cjoKICAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbiBhcyBlOgogICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIkZhaWxlZCB0byBsaXN0IGRpcmVjdG9yeToge2V9IikKCi0gICAgIyBJZiBpdCdzIGEgZmlsZSwgc2hvdyB0aGUgZW50aXJlIGZpbGUgd2l0aCBsaW5lIG51bWJlcnMKKyAgICAjIElmIGl0J3MgYSBmaWxlCiAgICAgY29udGVudCA9IHJlYWRfZmlsZShwYXRoX29iaikKKyAgICBsaW5lcyA9IGNvbnRlbnQuc3BsaXRsaW5lcygpCisKKyAgICAjIEhhbmRsZSBsaW5lIHJhbmdlIHZpZXdpbmcKKyAgICBpZiB2aWV3X3JhbmdlOgorICAgICAgICBpZiBsZW4odmlld19yYW5nZSkgIT0gMjoKKyAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoInZpZXdfcmFuZ2UgbXVzdCBjb250YWluIGV4YWN0bHkgdHdvIGVsZW1lbnRzOiBbc3RhcnQsIGVuZF0iKQorICAgICAgICBzdGFydCwgZW5kID0gdmlld19yYW5nZQorICAgICAgICBpZiBzdGFydCA8IDEgb3IgZW5kID4gbGVuKGxpbmVzKToKKyAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJJbnZhbGlkIGxpbmUgcmFuZ2UgW3tzdGFydH0sIHtlbmR9XSBmb3IgZmlsZSB3aXRoIHtsZW4obGluZXMpfSBsaW5lcyIpCisgICAgICAgICMgQWRqdXN0IGZvciAwLWJhc2VkIGluZGV4aW5nCisgICAgICAgIGNvbnRlbnQgPSAiXG4iLmpvaW4obGluZXNbc3RhcnQtMTplbmRdKQorICAgICAgICByZXR1cm4gZm9ybWF0X291dHB1dChjb250ZW50LCBzdHIocGF0aF9vYmopLCBpbml0X2xpbmU9c3RhcnQpCisKICAgICByZXR1cm4gZm9ybWF0X291dHB1dChjb250ZW50LCBzdHIocGF0aF9vYmopKQoKLWRlZiB0b29sX2Z1bmN0aW9uKGNvbW1hbmQ6IHN0ciwgcGF0aDogc3RyLCBmaWxlX3RleHQ6IHN0ciA9IE5vbmUpIC0+IHN0cjoKK2RlZiBzdHJfcmVwbGFjZShwYXRoX29iajogUGF0aCwgb2xkX3N0cjogc3RyLCBuZXdfc3RyOiBzdHIpIC0+IHN0cjoKKyAgICAiIiJSZXBsYWNlIHN0cmluZyBpbiBmaWxlLCBlbnN1cmluZyB1bmlxdWVuZXNzLiIiIgorICAgIGNvbnRlbnQgPSByZWFkX2ZpbGUocGF0aF9vYmopCisgICAgIyBDaGVjayBmb3IgbXVsdGlwbGUgb2NjdXJyZW5jZXMKKyAgICBpZiBjb250ZW50LmNvdW50KG9sZF9zdHIpID4gMToKKyAgICAgICAgcmV0dXJuIGYiRXJyb3I6IE11bHRpcGxlIG9jY3VycmVuY2VzIG9mICd7b2xkX3N0cn0nIGZvdW5kLiBSZXBsYWNlbWVudCByZXF1aXJlcyBhIHVuaXF1ZSBtYXRjaC4iCisgICAgZWxpZiBjb250ZW50LmNvdW50KG9sZF9zdHIpID09IDA6CisgICAgICAgIHJldHVybiBmIkVycm9yOiBTdHJpbmcgJ3tvbGRfc3RyfScgbm90IGZvdW5kIGluIGZpbGUuIgorCisgICAgbmV3X2NvbnRlbnQgPSBjb250ZW50LnJlcGxhY2Uob2xkX3N0ciwgbmV3X3N0cikKKyAgICB3cml0ZV9maWxlKHBhdGhfb2JqLCBuZXdfY29udGVudCkKKyAgICByZXR1cm4gZiJGaWxlIGF0IHtwYXRoX29ian0gaGFzIGJlZW4gZWRpdGVkOiByZXBsYWNlZCAne29sZF9zdHJ9JyB3aXRoICd7bmV3X3N0cn0nLiIKKworZGVmIGluc2VydF90ZXh0KHBhdGhfb2JqOiBQYXRoLCBpbnNlcnRfbGluZTogaW50LCBuZXdfc3RyOiBzdHIpIC0+IHN0cjoKKyAgICAiIiJJbnNlcnQgdGV4dCBhdCBzcGVjaWZpZWQgbGluZSBudW1iZXIuIiIiCisgICAgY29udGVudCA9IHJlYWRfZmlsZShwYXRoX29iaikKKyAgICBsaW5lcyA9IGNvbnRlbnQuc3BsaXRsaW5lcygpCisKKyAgICBpZiBpbnNlcnRfbGluZSA8IDEgb3IgaW5zZXJ0X2xpbmUgPiBsZW4obGluZXMpICsgMToKKyAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIkludmFsaWQgaW5zZXJ0IGxpbmUge2luc2VydF9saW5lfSBmb3IgZmlsZSB3aXRoIHtsZW4obGluZXMpfSBsaW5lcyIpCisKKyAgICAjIEluc2VydCB0aGUgbmV3IHRleHQgYXQgdGhlIHNwZWNpZmllZCBsaW5lIChhZGp1c3RpbmcgZm9yIDAtYmFzZWQgaW5kZXgpCisgICAgbGluZXMuaW5zZXJ0KGluc2VydF9saW5lIC0gMSwgbmV3X3N0ci5yc3RyaXAoIlxuIikpCisgICAgbmV3X2NvbnRlbnQgPSAiXG4iLmpvaW4obGluZXMpICsgIlxuIgorCisgICAgd3JpdGVfZmlsZShwYXRoX29iaiwgbmV3X2NvbnRlbnQpCisgICAgcmV0dXJuIGYiRmlsZSBhdCB7cGF0aF9vYmp9IGhhcyBiZWVuIGVkaXRlZDogaW5zZXJ0ZWQgdGV4dCBhdCBsaW5lIHtpbnNlcnRfbGluZX0uIgorCitkZWYgdW5kb19lZGl0KHBhdGhfb2JqOiBQYXRoKSAtPiBzdHI6CisgICAgIiIiVW5kbyBsYXN0IGVkaXQgb3BlcmF0aW9uIG9uIHRoZSBmaWxlLiIiIgorICAgIHBhdGhfc3RyID0gc3RyKHBhdGhfb2JqKQorICAgIGlmIHBhdGhfc3RyIG5vdCBpbiBlZGl0X2hpc3Rvcnkgb3Igbm90IGVkaXRfaGlzdG9yeVtwYXRoX3N0cl06CisgICAgICAgIHJldHVybiAiRXJyb3I6IE5vIGVkaXQgaGlzdG9yeSBhdmFpbGFibGUgZm9yIHRoaXMgZmlsZS4iCisKKyAgICAjIFJlc3RvcmUgdGhlIGxhc3Qgc2F2ZWQgY29udGVudAorICAgIHByZXZpb3VzX2NvbnRlbnQgPSBlZGl0X2hpc3RvcnlbcGF0aF9zdHJdLnBvcCgpCisgICAgd3JpdGVfZmlsZShwYXRoX29iaiwgcHJldmlvdXNfY29udGVudCwgc2F2ZV9oaXN0b3J5PUZhbHNlKQorICAgIHJldHVybiBmIkxhc3QgZWRpdCBvbiB7cGF0aF9vYmp9IGhhcyBiZWVuIHVuZG9uZSBzdWNjZXNzZnVsbHkuIgorCitkZWYgdG9vbF9mdW5jdGlvbihjb21tYW5kOiBzdHIsIHBhdGg6IHN0ciwgKiprd2FyZ3MpIC0+IHN0cjoKICAgICAiIiIKLSAgICBNYWluIHRvb2wgZnVuY3Rpb24gdGhhdCBoYW5kbGVzOgotICAgICAgLSAndmlldycgIDogVmlldyB0aGUgZW50aXJlIGZpbGUgb3IgZGlyZWN0b3J5IGxpc3RpbmcKLSAgICAgIC0gJ2NyZWF0ZSc6IENyZWF0ZSBhIG5ldyBmaWxlIHdpdGggdGhlIGdpdmVuIGZpbGVfdGV4dAotICAgICAgLSAnZWRpdCcgIDogT3ZlcndyaXRlIGFuIGV4aXN0aW5nIGZpbGUgd2l0aCBmaWxlX3RleHQKKyAgICBNYWluIHRvb2wgZnVuY3Rpb24gdGhhdCBoYW5kbGVzIGFsbCBjb21tYW5kczoKKyAgICAgIC0gJ3ZpZXcnICAgICAgICA6IFZpZXcgZmlsZS9kaXJlY3RvcnkgKG9wdGlvbmFsbHkgd2l0aCBsaW5lIHJhbmdlKQorICAgICAgLSAnY3JlYXRlJyAgICAgIDogQ3JlYXRlIG5ldyBmaWxlCisgICAgICAtICdlZGl0JyAgICAgICAgOiBPdmVyd3JpdGUgZXhpc3RpbmcgZmlsZQorICAgICAgLSAnc3RyX3JlcGxhY2UnIDogUmVwbGFjZSBzdHJpbmcgaW4gZmlsZQorICAgICAgLSAnaW5zZXJ0JyAgICAgIDogSW5zZXJ0IHRleHQgYXQgbGluZQorICAgICAgLSAndW5kb19lZGl0JyAgIDogVW5kbyBsYXN0IGVkaXQKICAgICAiIiIKICAgICB0cnk6CiAgICAgICAgIHBhdGhfb2JqID0gdmFsaWRhdGVfcGF0aChwYXRoLCBjb21tYW5kKQoKICAgICAgICAgaWYgY29tbWFuZCA9PSAidmlldyI6Ci0gICAgICAgICAgICByZXR1cm4gdmlld19wYXRoKHBhdGhfb2JqKQorICAgICAgICAgICAgdmlld19yYW5nZSA9IGt3YXJncy5nZXQoJ3ZpZXdfcmFuZ2UnKQorICAgICAgICAgICAgcmV0dXJuIHZpZXdfcGF0aChwYXRoX29iaiwgdmlld19yYW5nZSkKCiAgICAgICAgIGVsaWYgY29tbWFuZCA9PSAiY3JlYXRlIjoKLSAgICAgICAgICAgIGlmIGZpbGVfdGV4dCBpcyBOb25lOgorICAgICAgICAgICAgaWYgJ2ZpbGVfdGV4dCcgbm90IGluIGt3YXJnczoKICAgICAgICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKCJNaXNzaW5nIHJlcXVpcmVkIGBmaWxlX3RleHRgIGZvciAnY3JlYXRlJyBjb21tYW5kLiIpCi0gICAgICAgICAgICB3cml0ZV9maWxlKHBhdGhfb2JqLCBmaWxlX3RleHQpCisgICAgICAgICAgICB3cml0ZV9maWxlKHBhdGhfb2JqLCBrd2FyZ3NbJ2ZpbGVfdGV4dCddKQogICAgICAgICAgICAgcmV0dXJuIGYiRmlsZSBjcmVhdGVkIHN1Y2Nlc3NmdWxseSBhdDoge3BhdGh9IgoKICAgICAgICAgZWxpZiBjb21tYW5kID09ICJlZGl0IjoKLSAgICAgICAgICAgIGlmIGZpbGVfdGV4dCBpcyBOb25lOgorICAgICAgICAgICAgaWYgJ2ZpbGVfdGV4dCcgbm90IGluIGt3YXJnczoKICAgICAgICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKCJNaXNzaW5nIHJlcXVpcmVkIGBmaWxlX3RleHRgIGZvciAnZWRpdCcgY29tbWFuZC4iKQotICAgICAgICAgICAgd3JpdGVfZmlsZShwYXRoX29iaiwgZmlsZV90ZXh0KQorICAgICAgICAgICAgd3JpdGVfZmlsZShwYXRoX29iaiwga3dhcmdzWydmaWxlX3RleHQnXSkKICAgICAgICAgICAgIHJldHVybiBmIkZpbGUgYXQge3BhdGh9IGhhcyBiZWVuIG92ZXJ3cml0dGVuIHdpdGggbmV3IGNvbnRlbnQuIgoKKyAgICAgICAgZWxpZiBjb21tYW5kID09ICJzdHJfcmVwbGFjZSI6CisgICAgICAgICAgICBpZiAnb2xkX3N0cicgbm90IGluIGt3YXJncyBvciAnbmV3X3N0cicgbm90IGluIGt3YXJnczoKKyAgICAgICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKCJCb3RoICdvbGRfc3RyJyBhbmQgJ25ld19zdHInIGFyZSByZXF1aXJlZCBmb3Igc3RyaW5nIHJlcGxhY2VtZW50LiIpCisgICAgICAgICAgICByZXR1cm4gc3RyX3JlcGxhY2UocGF0aF9vYmosIGt3YXJnc1snb2xkX3N0ciddLCBrd2FyZ3NbJ25ld19zdHInXSkKKworICAgICAgICBlbGlmIGNvbW1hbmQgPT0gImluc2VydCI6CisgICAgICAgICAgICBpZiAnaW5zZXJ0X2xpbmUnIG5vdCBpbiBrd2FyZ3Mgb3IgJ25ld19zdHInIG5vdCBpbiBrd2FyZ3M6CisgICAgICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcigiQm90aCAnaW5zZXJ0X2xpbmUnIGFuZCAnbmV3X3N0cicgYXJlIHJlcXVpcmVkIGZvciB0ZXh0IGluc2VydGlvbi4iKQorICAgICAgICAgICAgcmV0dXJuIGluc2VydF90ZXh0KHBhdGhfb2JqLCBrd2FyZ3NbJ2luc2VydF9saW5lJ10sIGt3YXJnc1snbmV3X3N0ciddKQorCisgICAgICAgIGVsaWYgY29tbWFuZCA9PSAidW5kb19lZGl0IjoKKyAgICAgICAgICAgIHJldHVybiB1bmRvX2VkaXQocGF0aF9vYmopCisKICAgICAgICAgZWxzZToKICAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJVbmtub3duIGNvbW1hbmQ6IHtjb21tYW5kfSIp)
diff --git a/tools/edit.py b/tools/edit.py
index d7184c3..87fa408 100644
--- a/tools/edit.py
+++ b/tools/edit.py
@@ -1,5 +1,9 @@
from pathlib import Path
import subprocess
+from typing import List, Optional, Dict
+
+# Global edit history for undo functionality
+edit_history: Dict[str, List[str]] = {}
def tool_info():
return {
@@ -10,14 +14,14 @@ def tool_info():
* The ‘create‘ command cannot be used if the specified ‘path‘ already exists as a file.\n
* If a ‘command‘ generates a long output, it will be truncated and marked with ‘<response clipped>‘.\n
* The ‘edit‘ command overwrites the entire file with the provided ‘file_text‘.\n
-* No partial/line-range edits or partial viewing are supported.""",
+* Also supports viewing specific line ranges, string replacement, text insertion, and undo operations.""",
"input_schema": {
"type": "object",
"properties": {
"command": {
"type": "string",
- "enum": ["view", "create", "edit"],
- "description": "The command to run: ‘view‘, ‘create‘, or ‘edit‘."
+ "enum": ["view", "create", "edit", "str_replace", "insert", "undo_edit"],
+ "description": "The command to run: ‘view‘, ‘create‘, ‘edit‘, ‘str_replace‘, ‘insert‘, or ‘undo_edit‘."
},
"path": {
"description": "Absolute path to file or directory, e.g. ‘/repo/file.py‘ or ‘/repo‘.",
@@ -26,6 +30,23 @@ def tool_info():
"file_text": {
"description": "Required parameter of ‘create‘ or ‘edit‘ command, containing the content for the entire file.",
"type": "string"
+ },
+ "view_range": {
+ "description": "Optional parameter for ‘view‘ command to display specific line range [start, end].",
+ "type": "array",
+ "items": {"type": "integer"}
+ },
+ "old_str": {
+ "description": "Required parameter for ‘str_replace‘ command, string to replace.",
+ "type": "string"
+ },
+ "new_str": {
+ "description": "Required parameter for ‘str_replace‘ and ‘insert‘ commands, new string to insert.",
+ "type": "string"
+ },
+ "insert_line": {
+ "description": "Required parameter for ‘insert‘ command, line number where to insert text.",
+ "type": "integer"
}
},
"required": ["command", "path"]
@@ -43,7 +64,7 @@ def validate_path(path: str, command: str) -> Path:
Validate the file path for each command:
- ’view’: path may be a file or directory; must exist.
- ’create’: path must not exist (for new file creation).
- - ’edit’: path must exist (for overwriting).
+ - Others: path must exist as a file.
"""
path_obj = Path(path)
@@ -61,14 +82,12 @@ def validate_path(path: str, command: str) -> Path:
# Path must not exist
if path_obj.exists():
raise ValueError(f"Cannot create new file; {path} already exists.")
- elif command == "edit":
+ else:
# Path must exist and must be a file
if not path_obj.exists():
raise ValueError(f"The file {path} does not exist.")
if path_obj.is_dir():
raise ValueError(f"{path} is a directory and cannot be edited as a file.")
- else:
- raise ValueError(f"Unknown or unsupported command: {command}")
return path_obj
@@ -89,14 +108,21 @@ def read_file(path: Path) -> str:
except Exception as e:
raise ValueError(f"Failed to read file: {e}")
-def write_file(path: Path, content: str):
+def write_file(path: Path, content: str, save_history: bool = True):
"""Write (overwrite) entire file contents."""
try:
+ if save_history:
+ # Save the current content to history before writing
+ if path.exists():
+ if str(path) not in edit_history:
+ edit_history[str(path)] = []
+ edit_history[str(path)].append(path.read_text())
+
path.write_text(content)
except Exception as e:
raise ValueError(f"Failed to write file: {e}")
-def view_path(path_obj: Path) -> str:
+def view_path(path_obj: Path, view_range: Optional[List[int]] = None) -> str:
"""View the entire file contents or directory listing."""
if path_obj.is_dir():
# For directories: list non-hidden files up to 2 levels deep
@@ -115,35 +141,104 @@ def view_path(path_obj: Path) -> str:
except Exception as e:
raise ValueError(f"Failed to list directory: {e}")
- # If it’s a file, show the entire file with line numbers
+ # If it’s a file
content = read_file(path_obj)
+ lines = content.splitlines()
+
+ # Handle line range viewing
+ if view_range:
+ if len(view_range) != 2:
+ raise ValueError("view_range must contain exactly two elements: [start, end]")
+ start, end = view_range
+ if start < 1 or end > len(lines):
+ raise ValueError(f"Invalid line range [{start}, {end}] for file with {len(lines)} lines")
+ # Adjust for 0-based indexing
+ content = "\n".join(lines[start-1:end])
+ return format_output(content, str(path_obj), init_line=start)
+
return format_output(content, str(path_obj))
-def tool_function(command: str, path: str, file_text: str = None) -> str:
+def str_replace(path_obj: Path, old_str: str, new_str: str) -> str:
+ """Replace string in file, ensuring uniqueness."""
+ content = read_file(path_obj)
+ # Check for multiple occurrences
+ if content.count(old_str) > 1:
+ return f"Error: Multiple occurrences of ’{old_str}’ found. Replacement requires a unique match."
+ elif content.count(old_str) == 0:
+ return f"Error: String ’{old_str}’ not found in file."
+
+ new_content = content.replace(old_str, new_str)
+ write_file(path_obj, new_content)
+ return f"File at {path_obj} has been edited: replaced ’{old_str}’ with ’{new_str}’."
+
+def insert_text(path_obj: Path, insert_line: int, new_str: str) -> str:
+ """Insert text at specified line number."""
+ content = read_file(path_obj)
+ lines = content.splitlines()
+
+ if insert_line < 1 or insert_line > len(lines) + 1:
+ raise ValueError(f"Invalid insert line {insert_line} for file with {len(lines)} lines")
+
+ # Insert the new text at the specified line (adjusting for 0-based index)
+ lines.insert(insert_line - 1, new_str.rstrip("\n"))
+ new_content = "\n".join(lines) + "\n"
+
+ write_file(path_obj, new_content)
+ return f"File at {path_obj} has been edited: inserted text at line {insert_line}."
+
+def undo_edit(path_obj: Path) -> str:
+ """Undo last edit operation on the file."""
+ path_str = str(path_obj)
+ if path_str not in edit_history or not edit_history[path_str]:
+ return "Error: No edit history available for this file."
+
+ # Restore the last saved content
+ previous_content = edit_history[path_str].pop()
+ write_file(path_obj, previous_content, save_history=False)
+ return f"Last edit on {path_obj} has been undone successfully."
+
+def tool_function(command: str, path: str, **kwargs) -> str:
"""
- Main tool function that handles:
- - ’view’ : View the entire file or directory listing
- - ’create’: Create a new file with the given file_text
- - ’edit’ : Overwrite an existing file with file_text
+ Main tool function that handles all commands:
+ - ’view’ : View file/directory (optionally with line range)
+ - ’create’ : Create new file
+ - ’edit’ : Overwrite existing file
+ - ’str_replace’ : Replace string in file
+ - ’insert’ : Insert text at line
+ - ’undo_edit’ : Undo last edit
"""
try:
path_obj = validate_path(path, command)
if command == "view":
- return view_path(path_obj)
+ view_range = kwargs.get(’view_range’)
+ return view_path(path_obj, view_range)
elif command == "create":
- if file_text is None:
+ if ’file_text’ not in kwargs:
raise ValueError("Missing required ‘file_text‘ for ’create’ command.")
- write_file(path_obj, file_text)
+ write_file(path_obj, kwargs[’file_text’])
return f"File created successfully at: {path}"
elif command == "edit":
- if file_text is None:
+ if ’file_text’ not in kwargs:
raise ValueError("Missing required ‘file_text‘ for ’edit’ command.")
- write_file(path_obj, file_text)
+ write_file(path_obj, kwargs[’file_text’])
return f"File at {path} has been overwritten with new content."
+ elif command == "str_replace":
+ if ’old_str’ not in kwargs or ’new_str’ not in kwargs:
+ raise ValueError("Both ’old_str’ and ’new_str’ are required for string replacement.")
+ return str_replace(path_obj, kwargs[’old_str’], kwargs[’new_str’])
+
+ elif command == "insert":
+ if ’insert_line’ not in kwargs or ’new_str’ not in kwargs:
+ raise ValueError("Both ’insert_line’ and ’new_str’ are required for text insertion.")
+ return insert_text(path_obj, kwargs[’insert_line’], kwargs[’new_str’])
+
+ elif command == "undo_edit":
+ return undo_edit(path_obj)
+
else:
raise ValueError(f"Unknown command: {command}")
[⬇](data:text/plain;base64,ZGlmZiAtLWdpdCBhL3Rvb2xzL2VkaXQucHkgYi90b29scy9lZGl0LnB5CmluZGV4IDg3ZmE0MDguLmExMjkwM2MgMTAwNjQ0Ci0tLSBhL3Rvb2xzL2VkaXQucHkKKysrIGIvdG9vbHMvZWRpdC5weQpAQCAtMTE3LDcgKzExNyw3IEBAIGRlZiB3cml0ZV9maWxlKHBhdGg6IFBhdGgsIGNvbnRlbnQ6IHN0ciwgc2F2ZV9oaXN0b3J5OiBib29sID0gVHJ1ZSk6CiAgICAgICAgICAgICAgICAgaWYgc3RyKHBhdGgpIG5vdCBpbiBlZGl0X2hpc3Rvcnk6CiAgICAgICAgICAgICAgICAgICAgIGVkaXRfaGlzdG9yeVtzdHIocGF0aCldID0gW10KICAgICAgICAgICAgICAgICBlZGl0X2hpc3Rvcnlbc3RyKHBhdGgpXS5hcHBlbmQocGF0aC5yZWFkX3RleHQoKSkKLQorCiAgICAgICAgIHBhdGgud3JpdGVfdGV4dChjb250ZW50KQogICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIkZhaWxlZCB0byB3cml0ZSBmaWxlOiB7ZX0iKQpAQCAtMTcyLDE3ICsxNzIsMjUgQEAgZGVmIHN0cl9yZXBsYWNlKHBhdGhfb2JqOiBQYXRoLCBvbGRfc3RyOiBzdHIsIG5ld19zdHI6IHN0cikgLT4gc3RyOgogICAgIHJldHVybiBmIkZpbGUgYXQge3BhdGhfb2JqfSBoYXMgYmVlbiBlZGl0ZWQ6IHJlcGxhY2VkICd7b2xkX3N0cn0nIHdpdGggJ3tuZXdfc3RyfScuIgoKIGRlZiBpbnNlcnRfdGV4dChwYXRoX29iajogUGF0aCwgaW5zZXJ0X2xpbmU6IGludCwgbmV3X3N0cjogc3RyKSAtPiBzdHI6Ci0gICAgIiIiSW5zZXJ0IHRleHQgYXQgc3BlY2lmaWVkIGxpbmUgbnVtYmVyLiIiIgorICAgICIiIkluc2VydCB0ZXh0IGF0IHNwZWNpZmllZCBsaW5lIG51bWJlciAoMS1iYXNlZCkuIiIiCiAgICAgY29udGVudCA9IHJlYWRfZmlsZShwYXRoX29iaikKICAgICBsaW5lcyA9IGNvbnRlbnQuc3BsaXRsaW5lcygpCgotICAgIGlmIGluc2VydF9saW5lIDwgMSBvciBpbnNlcnRfbGluZSA+IGxlbihsaW5lcykgKyAxOgotICAgICAgICByYWlzZSBWYWx1ZUVycm9yKGYiSW52YWxpZCBpbnNlcnQgbGluZSB7aW5zZXJ0X2xpbmV9IGZvciBmaWxlIHdpdGgge2xlbihsaW5lcyl9IGxpbmVzIikKKyAgICAjIFZhbGlkYXRlIHRoZSBpbnNlcnRpb24gbGluZSBudW1iZXIKKyAgICBpZiBpbnNlcnRfbGluZSA8IDE6CisgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJJbnZhbGlkIGluc2VydCBsaW5lIHtpbnNlcnRfbGluZX0gLSBtdXN0IGJlIGdyZWF0ZXIgdGhhbiAwIikKKyAgICBpZiBpbnNlcnRfbGluZSA+IGxlbihsaW5lcykgKyAxOgorICAgICAgICByYWlzZSBWYWx1ZUVycm9yKGYiSW52YWxpZCBpbnNlcnQgbGluZSB7aW5zZXJ0X2xpbmV9IC0gZmlsZSBvbmx5IGhhcyB7bGVuKGxpbmVzKX0gbGluZXMiKQoKLSAgICAjIEluc2VydCB0aGUgbmV3IHRleHQgYXQgdGhlIHNwZWNpZmllZCBsaW5lIChhZGp1c3RpbmcgZm9yIDAtYmFzZWQgaW5kZXgpCi0gICAgbGluZXMuaW5zZXJ0KGluc2VydF9saW5lIC0gMSwgbmV3X3N0ci5yc3RyaXAoIlxuIikpCi0gICAgbmV3X2NvbnRlbnQgPSAiXG4iLmpvaW4obGluZXMpICsgIlxuIgorICAgICMgQ2xlYW4gdXAgdGhlIG5ldyB0ZXh0IHRvIHJlbW92ZSBhbnkgdHJhaWxpbmcgbmV3bGluZXMKKyAgICBuZXdfdGV4dCA9IG5ld19zdHIucnN0cmlwKCdcbicpCgorICAgICMgSW5zZXJ0IGF0IHRoZSBjb3JyZWN0IHBvc2l0aW9uIChsaW5lIG51bWJlcnMgYXJlIDEtYmFzZWQsIGxpc3QgaW5kaWNlcyBhcmUgMC1iYXNlZCkKKyAgICAjIEluc2VydCBhdCBpbmRleD1pbnNlcnRfbGluZSwgc28gaXQgYXBwZWFycyBhZnRlciB0aGUgY3VycmVudCBsaW5lIGF0IHRoYXQgcG9zaXRpb24KKyAgICBsaW5lcy5pbnNlcnQoaW5zZXJ0X2xpbmUsIG5ld190ZXh0KQorCisgICAgIyBKb2luIGxpbmVzIHdpdGggbmV3bGluZSBhbmQgYWRkIHRyYWlsaW5nIG5ld2xpbmUKKyAgICBuZXdfY29udGVudCA9ICdcbicuam9pbihsaW5lcykgKyAnXG4nCiAgICAgd3JpdGVfZmlsZShwYXRoX29iaiwgbmV3X2NvbnRlbnQpCiAgICAgcmV0dXJuIGYiRmlsZSBhdCB7cGF0aF9vYmp9IGhhcyBiZWVuIGVkaXRlZDogaW5zZXJ0ZWQgdGV4dCBhdCBsaW5lIHtpbnNlcnRfbGluZX0uIgoKQEAgLTI0Myw4ICsyNTEsNCBAQCBkZWYgdG9vbF9mdW5jdGlvbihjb21tYW5kOiBzdHIsIHBhdGg6IHN0ciwgKiprd2FyZ3MpIC0+IHN0cjoKICAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJVbmtub3duIGNvbW1hbmQ6IHtjb21tYW5kfSIpCgogICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKLSAgICAgICAgcmV0dXJuIGYiRXJyb3I6IHtzdHIoZSl9IgotCi1pZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgotICAgICMgRXhhbXBsZSB1c2FnZQotICAgIHByaW50KHRvb2xfZnVuY3Rpb24oInZpZXciLCAiL2hvbWUvdWJ1bnR1L3h4L2RnbS9jb2RpbmdfYWdlbnQucHkiKSkKXCBObyBuZXdsaW5lIGF0IGVuZCBvZiBmaWxlCisgICAgICAgIHJldHVybiBmIkVycm9yOiB7c3RyKGUpfSIKXCBObyBuZXdsaW5lIGF0IGVuZCBvZiBmaWxl)
diff --git a/tools/edit.py b/tools/edit.py
index 87fa408..a12903c 100644
--- a/tools/edit.py
+++ b/tools/edit.py
@@ -117,7 +117,7 @@ def write_file(path: Path, content: str, save_history: bool = True):
if str(path) not in edit_history:
edit_history[str(path)] = []
edit_history[str(path)].append(path.read_text())
-
+
path.write_text(content)
except Exception as e:
raise ValueError(f"Failed to write file: {e}")
@@ -172,17 +172,25 @@ def str_replace(path_obj: Path, old_str: str, new_str: str) -> str:
return f"File at {path_obj} has been edited: replaced ’{old_str}’ with ’{new_str}’."
def insert_text(path_obj: Path, insert_line: int, new_str: str) -> str:
- """Insert text at specified line number."""
+ """Insert text at specified line number (1-based)."""
content = read_file(path_obj)
lines = content.splitlines()
- if insert_line < 1 or insert_line > len(lines) + 1:
- raise ValueError(f"Invalid insert line {insert_line} for file with {len(lines)} lines")
+ # Validate the insertion line number
+ if insert_line < 1:
+ raise ValueError(f"Invalid insert line {insert_line} - must be greater than 0")
+ if insert_line > len(lines) + 1:
+ raise ValueError(f"Invalid insert line {insert_line} - file only has {len(lines)} lines")
- # Insert the new text at the specified line (adjusting for 0-based index)
- lines.insert(insert_line - 1, new_str.rstrip("\n"))
- new_content = "\n".join(lines) + "\n"
+ # Clean up the new text to remove any trailing newlines
+ new_text = new_str.rstrip(’\n’)
+ # Insert at the correct position (line numbers are 1-based, list indices are 0-based)
+ # Insert at index=insert_line, so it appears after the current line at that position
+ lines.insert(insert_line, new_text)
+
+ # Join lines with newline and add trailing newline
+ new_content = ’\n’.join(lines) + ’\n’
write_file(path_obj, new_content)
return f"File at {path_obj} has been edited: inserted text at line {insert_line}."
@@ -243,8 +251,4 @@ def tool_function(command: str, path: str, **kwargs) -> str:
raise ValueError(f"Unknown command: {command}")
except Exception as e:
- return f"Error: {str(e)}"
-
-if __name__ == "__main__":
- # Example usage
- print(tool_function("view", "/home/ubuntu/xx/dgm/coding_agent.py"))
\ No newline at end of file
+ return f"Error: {str(e)}"
\ No newline at end of file+
[⬇](data:text/plain;base64,ZGlmZiAtLWdpdCBhL2NvZGluZ19hZ2VudC5weSBiL2NvZGluZ19hZ2VudC5weQppbmRleCA2NjM5YWJkLi45N2Y0YjY5IDEwMDY0NAotLS0gYS9jb2RpbmdfYWdlbnQucHkKKysrIGIvY29kaW5nX2FnZW50LnB5CkBAIC01Miw2ICs1MiwxMCBAQCBjbGFzcyBTb2x1dGlvbkF0dGVtcHQ6CiAgICAgdGVzdF9vdXRwdXQ6IHN0ciAgIyBSYXcgdGVzdCBvdXRwdXQKICAgICB0ZXN0X3N1Y2Nlc3M6IGJvb2wgICMgV2hldGhlciB0ZXN0cyBwYXNzZWQKICAgICB0ZXN0X3N0YXRzOiBkaWN0ICAjIFRlc3Qgc3RhdGlzdGljcyAoZS5nLiwgbnVtYmVyIG9mIHBhc3NlZC9mYWlsZWQgdGVzdHMpCisgICAgZXJyb3JfbWVzc2FnZXM6IExpc3Rbc3RyXSA9IE5vbmUgICMgTGlzdCBvZiBzcGVjaWZpYyBlcnJvciBtZXNzYWdlcworICAgIHRlc3RfZGV0YWlsczogZGljdCA9IE5vbmUgICMgRGV0YWlsZWQgdGVzdCBpbmZvcm1hdGlvbiBsaWtlIHNwZWNpZmljIHRlc3QgbmFtZXMgYW5kIHRoZWlyIHN0YXR1cworICAgIGV4ZWN1dGlvbl90aW1lOiBmbG9hdCA9IE5vbmUgICMgVGVzdCBleGVjdXRpb24gdGltZSBpbiBzZWNvbmRzCisgICAgYXR0ZW1wdF9udW1iZXI6IGludCA9IE5vbmUgICMgVGhlIGF0dGVtcHQgbnVtYmVyIGluIHRoZSBzZXF1ZW5jZQoKIGRlZiBnZXRfdGhyZWFkX2xvZ2dlcigpOgogICAgICIiIgpAQCAtMTUwLDEyICsxNTQsODIgQEAgY2xhc3MgQWdlbnRpY1N5c3RlbToKICAgICAgICAgXQogICAgICAgICByZXR1cm4gbmV3X21zZ19oaXN0b3J5CgorICAgIGRlZiBleHRyYWN0X3Rlc3RfZGV0YWlscyhzZWxmLCBvdXRwdXQ6IHN0cikgLT4gdHVwbGVbZGljdCwgTGlzdFtzdHJdLCBkaWN0XToKKyAgICAgICAgIiIiRXh0cmFjdCBkZXRhaWxlZCB0ZXN0IGluZm9ybWF0aW9uIGZyb20gdGhlIG91dHB1dC4iIiIKKyAgICAgICAgZXJyb3JfbWVzc2FnZXMgPSBbXQorICAgICAgICB0ZXN0X2RldGFpbHMgPSB7fQorICAgICAgICBzdGF0cyA9IHsicGFzc2VkIjogMCwgImZhaWxlZCI6IDAsICJlcnJvcnMiOiAwLCAidG90YWwiOiAwLCAic2tpcHBlZCI6IDB9CisKKyAgICAgICAgIyBTcGxpdCBvdXRwdXQgaW50byBsaW5lcyBmb3IgYW5hbHlzaXMKKyAgICAgICAgbGluZXMgPSBvdXRwdXQuc3BsaXQoIlxuIikKKworICAgICAgICAjIExhbmd1YWdlLXNwZWNpZmljIHBhcnNpbmcKKyAgICAgICAgaWYgc2VsZi5sYW5ndWFnZSA9PSAicHl0aG9uIjoKKyAgICAgICAgICAgIGZvciBsaW5lIGluIGxpbmVzOgorICAgICAgICAgICAgICAgIGlmICJGQUlMRUQiIGluIGxpbmUgYW5kICI6OiIgaW4gbGluZToKKyAgICAgICAgICAgICAgICAgICAgdGVzdF9uYW1lID0gbGluZS5zcGxpdCgiOjoiKVsxXS5zcGxpdCgpWzBdCisgICAgICAgICAgICAgICAgICAgIHRlc3RfZGV0YWlsc1t0ZXN0X25hbWVdID0gIkZBSUxFRCIKKyAgICAgICAgICAgICAgICAgICAgc3RhdHNbImZhaWxlZCJdICs9IDEKKyAgICAgICAgICAgICAgICBlbGlmICJQQVNTRUQiIGluIGxpbmUgYW5kICI6OiIgaW4gbGluZToKKyAgICAgICAgICAgICAgICAgICAgdGVzdF9uYW1lID0gbGluZS5zcGxpdCgiOjoiKVsxXS5zcGxpdCgpWzBdCisgICAgICAgICAgICAgICAgICAgIHRlc3RfZGV0YWlsc1t0ZXN0X25hbWVdID0gIlBBU1NFRCIKKyAgICAgICAgICAgICAgICAgICAgc3RhdHNbInBhc3NlZCJdICs9IDEKKyAgICAgICAgICAgICAgICBlbGlmICJFUlJPUiIgaW4gbGluZSBhbmQgIjo6IiBpbiBsaW5lOgorICAgICAgICAgICAgICAgICAgICB0ZXN0X25hbWUgPSBsaW5lLnNwbGl0KCI6OiIpWzFdLnNwbGl0KClbMF0KKyAgICAgICAgICAgICAgICAgICAgdGVzdF9kZXRhaWxzW3Rlc3RfbmFtZV0gPSAiRVJST1IiCisgICAgICAgICAgICAgICAgICAgIHN0YXRzWyJlcnJvcnMiXSArPSAxCisgICAgICAgICAgICAgICAgICAgICMgRXh0cmFjdCBlcnJvciBtZXNzYWdlCisgICAgICAgICAgICAgICAgICAgIGlmIGxpbmVzLmluZGV4KGxpbmUpICsgMSA8IGxlbihsaW5lcyk6CisgICAgICAgICAgICAgICAgICAgICAgICBlcnJvcl9tZXNzYWdlcy5hcHBlbmQobGluZXNbbGluZXMuaW5kZXgobGluZSkgKyAxXSkKKworICAgICAgICBlbGlmIHNlbGYubGFuZ3VhZ2UgaW4gWyJqYXZhc2NyaXB0IiwgIm5vZGUiXToKKyAgICAgICAgICAgIGN1cnJlbnRfdGVzdCA9IE5vbmUKKyAgICAgICAgICAgIGZvciBsaW5lIGluIGxpbmVzOgorICAgICAgICAgICAgICAgIGlmIGxpbmUuc3RhcnRzd2l0aCgnY2hlY2ttYXJrJyk6CisgICAgICAgICAgICAgICAgICAgIHRlc3RfbmFtZSA9IGxpbmUucmVwbGFjZSgnY2hlY2ttYXJrLCcsICcnKS5zdHJpcCgpCisgICAgICAgICAgICAgICAgICAgIHRlc3RfZGV0YWlsc1t0ZXN0X25hbWVdID0gIlBBU1NFRCIKKyAgICAgICAgICAgICAgICAgICAgc3RhdHNbInBhc3NlZCJdICs9IDEKKyAgICAgICAgICAgICAgICBlbGlmIGxpbmUuc3RhcnRzd2l0aCgneCcpOgorICAgICAgICAgICAgICAgICAgICB0ZXN0X25hbWUgPSBsaW5lLnJlcGxhY2UoJ3gnLCAnJykuc3RyaXAoKQorICAgICAgICAgICAgICAgICAgICB0ZXN0X2RldGFpbHNbdGVzdF9uYW1lXSA9ICJGQUlMRUQiCisgICAgICAgICAgICAgICAgICAgIHN0YXRzWyJmYWlsZWQiXSArPSAxCisgICAgICAgICAgICAgICAgICAgIGN1cnJlbnRfdGVzdCA9IHRlc3RfbmFtZQorICAgICAgICAgICAgICAgIGVsaWYgY3VycmVudF90ZXN0IGFuZCAoJ0Vycm9yOicgaW4gbGluZSBvciAnQXNzZXJ0aW9uRXJyb3I6JyBpbiBsaW5lKToKKyAgICAgICAgICAgICAgICAgICAgZXJyb3JfbWVzc2FnZXMuYXBwZW5kKGYie2N1cnJlbnRfdGVzdH06IHtsaW5lLnN0cmlwKCl9IikKKworICAgICAgICBlbGlmIHNlbGYubGFuZ3VhZ2UgPT0gInJ1c3QiOgorICAgICAgICAgICAgZm9yIGxpbmUgaW4gbGluZXM6CisgICAgICAgICAgICAgICAgaWYgInRlc3QiIGluIGxpbmUgYW5kICIuLi4gb2siIGluIGxpbmU6CisgICAgICAgICAgICAgICAgICAgIHRlc3RfbmFtZSA9IGxpbmUuc3BsaXQoInRlc3QiKVsxXS5zcGxpdCgiLi4uIilbMF0uc3RyaXAoKQorICAgICAgICAgICAgICAgICAgICB0ZXN0X2RldGFpbHNbdGVzdF9uYW1lXSA9ICJQQVNTRUQiCisgICAgICAgICAgICAgICAgICAgIHN0YXRzWyJwYXNzZWQiXSArPSAxCisgICAgICAgICAgICAgICAgZWxpZiAidGVzdCIgaW4gbGluZSBhbmQgIi4uLiBGQUlMRUQiIGluIGxpbmU6CisgICAgICAgICAgICAgICAgICAgIHRlc3RfbmFtZSA9IGxpbmUuc3BsaXQoInRlc3QiKVsxXS5zcGxpdCgiLi4uIilbMF0uc3RyaXAoKQorICAgICAgICAgICAgICAgICAgICB0ZXN0X2RldGFpbHNbdGVzdF9uYW1lXSA9ICJGQUlMRUQiCisgICAgICAgICAgICAgICAgICAgIHN0YXRzWyJmYWlsZWQiXSArPSAxCisgICAgICAgICAgICAgICAgZWxpZiAiLS0tLSAiIGluIGxpbmUgYW5kICIgc3Rkb3V0IC0tLS0iIGluIGxpbmU6CisgICAgICAgICAgICAgICAgICAgIHRlc3RfbmFtZSA9IGxpbmUuc3BsaXQoIi0tLS0iKVsxXS5zcGxpdCgic3Rkb3V0IilbMF0uc3RyaXAoKQorICAgICAgICAgICAgICAgICAgICBpZiB0ZXN0X25hbWUgaW4gdGVzdF9kZXRhaWxzIGFuZCB0ZXN0X2RldGFpbHNbdGVzdF9uYW1lXSA9PSAiRkFJTEVEIjoKKyAgICAgICAgICAgICAgICAgICAgICAgIGVycm9yX21lc3NhZ2VzLmFwcGVuZChmInt0ZXN0X25hbWV9OiB7bmV4dCgobCBmb3IgbCBpbiBsaW5lc1tsaW5lcy5pbmRleChsaW5lKSsxOl0gaWYgbC5zdHJpcCgpKSwgJycpfSIpCisKKyAgICAgICAgIyBHZW5lcmljIGNvdW50aW5nIGZvciBvdGhlciBsYW5ndWFnZXMgb3IgYXMgZmFsbGJhY2sKKyAgICAgICAgaWYgbm90IGFueShzdGF0cy52YWx1ZXMoKSk6CisgICAgICAgICAgICBzdGF0c1sicGFzc2VkIl0gPSBvdXRwdXQuY291bnQoIlBBU1MiKSArIG91dHB1dC5jb3VudCgib2siKQorICAgICAgICAgICAgc3RhdHNbImZhaWxlZCJdID0gb3V0cHV0LmNvdW50KCJGQUlMIikgKyBvdXRwdXQuY291bnQoIm5vdCBvayIpCisgICAgICAgICAgICBzdGF0c1siZXJyb3JzIl0gPSBvdXRwdXQuY291bnQoIkVSUk9SIikgKyBvdXRwdXQuY291bnQoInBhbmljOiIpCisKKyAgICAgICAgc3RhdHNbInRvdGFsIl0gPSBzdGF0c1sicGFzc2VkIl0gKyBzdGF0c1siZmFpbGVkIl0gKyBzdGF0c1siZXJyb3JzIl0KKworICAgICAgICByZXR1cm4gc3RhdHMsIGVycm9yX21lc3NhZ2VzLCB0ZXN0X2RldGFpbHMKKwogICAgIGRlZiBydW5fdGVzdHMoc2VsZikgLT4gdHVwbGVbYm9vbCwgc3RyLCBkaWN0XToKICAgICAgICAgIiIiUnVuIHRlc3RzIGFuZCByZXR1cm4gc3VjY2VzcyBzdGF0dXMsIG91dHB1dCwgYW5kIHRlc3Qgc3RhdGlzdGljcy4iIiIKKyAgICAgICAgaW1wb3J0IHRpbWUKKwogICAgICAgICBzdWNjZXNzID0gRmFsc2UKICAgICAgICAgb3V0cHV0ID0gIiIKLSAgICAgICAgc3RhdHMgPSB7InBhc3NlZCI6IDAsICJmYWlsZWQiOiAwLCAiZXJyb3JzIjogMCwgInRvdGFsIjogMH0KLQorICAgICAgICBzdGFydF90aW1lID0gdGltZS50aW1lKCkKKwogICAgICAgICB0cnk6CiAgICAgICAgICAgICBmb3IgY29tbWFuZCBpbiBURVNUX0NPTU1BTkRTLmdldChzZWxmLmxhbmd1YWdlLCBbXSk6CiAgICAgICAgICAgICAgICAgcHJvYyA9IHN1YnByb2Nlc3MucnVuKApAQCAtMTY5LDM0ICsyNDMsOTcgQEAgY2xhc3MgQWdlbnRpY1N5c3RlbToKICAgICAgICAgICAgICAgICBzdWNjZXNzID0gcHJvYy5yZXR1cm5jb2RlID09IDAKICAgICAgICAgICAgICAgICBpZiBub3Qgc3VjY2VzczoKICAgICAgICAgICAgICAgICAgICAgYnJlYWsKLQotICAgICAgICAgICAgIyBUcnkgdG8gZXh0cmFjdCB0ZXN0IHN0YXRpc3RpY3MgZnJvbSBvdXRwdXQKLSAgICAgICAgICAgICMgVGhpcyBpcyBhIHNpbXBsZSBleGFtcGxlOyB5b3UgbWlnaHQgd2FudCB0byBhZGQgbW9yZSBzb3BoaXN0aWNhdGVkIHBhcnNpbmcKLSAgICAgICAgICAgIHN0YXRzWyJwYXNzZWQiXSA9IG91dHB1dC5jb3VudCgiUEFTUyIpICsgb3V0cHV0LmNvdW50KCJvayIpCi0gICAgICAgICAgICBzdGF0c1siZmFpbGVkIl0gPSBvdXRwdXQuY291bnQoIkZBSUwiKSArIG91dHB1dC5jb3VudCgibm90IG9rIikKLSAgICAgICAgICAgIHN0YXRzWyJlcnJvcnMiXSA9IG91dHB1dC5jb3VudCgiRVJST1IiKSArIG91dHB1dC5jb3VudCgicGFuaWM6IikKLSAgICAgICAgICAgIHN0YXRzWyJ0b3RhbCJdID0gc3RhdHNbInBhc3NlZCJdICsgc3RhdHNbImZhaWxlZCJdICsgc3RhdHNbImVycm9ycyJdCisKKyAgICAgICAgICAgICMgRXh0cmFjdCBkZXRhaWxlZCB0ZXN0IGluZm9ybWF0aW9uCisgICAgICAgICAgICBzdGF0cywgZXJyb3JfbWVzc2FnZXMsIHRlc3RfZGV0YWlscyA9IHNlbGYuZXh0cmFjdF90ZXN0X2RldGFpbHMob3V0cHV0KQorICAgICAgICAgICAgc3RhdHNbImV4ZWN1dGlvbl90aW1lIl0gPSB0aW1lLnRpbWUoKSAtIHN0YXJ0X3RpbWUKKworICAgICAgICAgICAgIyBFbmhhbmNlIHN0YXRzIHdpdGggZXh0cmFjdGVkIGluZm9ybWF0aW9uCisgICAgICAgICAgICBzdGF0c1siZXJyb3JfbWVzc2FnZXMiXSA9IGVycm9yX21lc3NhZ2VzCisgICAgICAgICAgICBzdGF0c1sidGVzdF9kZXRhaWxzIl0gPSB0ZXN0X2RldGFpbHMKCiAgICAgICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICAgICAgIG91dHB1dCA9IGYiRXJyb3IgcnVubmluZyB0ZXN0czoge3N0cihlKX0iCiAgICAgICAgICAgICBzdWNjZXNzID0gRmFsc2UKKyAgICAgICAgICAgIHN0YXRzID0geworICAgICAgICAgICAgICAgICJwYXNzZWQiOiAwLCAiZmFpbGVkIjogMCwgImVycm9ycyI6IDEsICJ0b3RhbCI6IDEsCisgICAgICAgICAgICAgICAgImV4ZWN1dGlvbl90aW1lIjogdGltZS50aW1lKCkgLSBzdGFydF90aW1lLAorICAgICAgICAgICAgICAgICJlcnJvcl9tZXNzYWdlcyI6IFtzdHIoZSldLAorICAgICAgICAgICAgICAgICJ0ZXN0X2RldGFpbHMiOiB7fQorICAgICAgICAgICAgfQoKICAgICAgICAgcmV0dXJuIHN1Y2Nlc3MsIG91dHB1dCwgc3RhdHMKCiAgICAgZGVmIGFuYWx5emVfdGVzdF9yZXN1bHRzKHNlbGYsIGF0dGVtcHRzOiBMaXN0W1NvbHV0aW9uQXR0ZW1wdF0pIC0+IHN0cjoKLSAgICAgICAgIiIiQW5hbHl6ZSB0ZXN0IHJlc3VsdHMgYW5kIGNyZWF0ZSBhIHN1bW1hcnkgZm9yIHRoZSBhZ2VudC4iIiIKKyAgICAgICAgIiIiQW5hbHl6ZSB0ZXN0IHJlc3VsdHMgYW5kIGNyZWF0ZSBhIGRldGFpbGVkIHN1bW1hcnkgZm9yIHRoZSBhZ2VudC4iIiIKICAgICAgICAgc3VtbWFyeSA9ICIjIFRlc3QgUmVzdWx0cyBBbmFseXNpc1xuXG4iCgorICAgICAgICAjIE92ZXJhbGwgcHJvZ3Jlc3MgdHJhY2tpbmcKKyAgICAgICAgaWYgbGVuKGF0dGVtcHRzKSA+IDE6CisgICAgICAgICAgICBzdW1tYXJ5ICs9ICIjIyBQcm9ncmVzcyBPdmVydmlld1xuIgorICAgICAgICAgICAgZmlyc3RfYXR0ZW1wdCA9IGF0dGVtcHRzWzBdLnRlc3Rfc3RhdHMKKyAgICAgICAgICAgIGxhc3RfYXR0ZW1wdCA9IGF0dGVtcHRzWy0xXS50ZXN0X3N0YXRzCisKKyAgICAgICAgICAgIHByb2dyZXNzID0geworICAgICAgICAgICAgICAgICJwYXNzZWQiOiBsYXN0X2F0dGVtcHRbInBhc3NlZCJdIC0gZmlyc3RfYXR0ZW1wdFsicGFzc2VkIl0sCisgICAgICAgICAgICAgICAgImZhaWxlZCI6IGZpcnN0X2F0dGVtcHRbImZhaWxlZCJdIC0gbGFzdF9hdHRlbXB0WyJmYWlsZWQiXSwKKyAgICAgICAgICAgICAgICAiZXJyb3JzIjogZmlyc3RfYXR0ZW1wdFsiZXJyb3JzIl0gLSBsYXN0X2F0dGVtcHRbImVycm9ycyJdCisgICAgICAgICAgICB9CisKKyAgICAgICAgICAgIHN1bW1hcnkgKz0gIlByb2dyZXNzIHNpbmNlIGZpcnN0IGF0dGVtcHQ6XG4iCisgICAgICAgICAgICBzdW1tYXJ5ICs9IGYiLSBBZGRpdGlvbmFsIHBhc3NpbmcgdGVzdHM6IHtwcm9ncmVzc1sncGFzc2VkJ119XG4iCisgICAgICAgICAgICBzdW1tYXJ5ICs9IGYiLSBSZWR1Y2VkIGZhaWx1cmVzOiB7cHJvZ3Jlc3NbJ2ZhaWxlZCddfVxuIgorICAgICAgICAgICAgc3VtbWFyeSArPSBmIi0gUmVkdWNlZCBlcnJvcnM6IHtwcm9ncmVzc1snZXJyb3JzJ119XG5cbiIKKworICAgICAgICAjIERldGFpbGVkIGF0dGVtcHQgYW5hbHlzaXMKICAgICAgICAgZm9yIGksIGF0dGVtcHQgaW4gZW51bWVyYXRlKGF0dGVtcHRzLCAxKToKICAgICAgICAgICAgIHN1bW1hcnkgKz0gZiIjIyBBdHRlbXB0IHtpfVxuIgogICAgICAgICAgICAgc3VtbWFyeSArPSBmIlRlc3QgU3VjY2Vzczoge2F0dGVtcHQudGVzdF9zdWNjZXNzfVxuIgotICAgICAgICAgICAgc3VtbWFyeSArPSBmIlRlc3QgU3RhdHM6IHtqc29uLmR1bXBzKGF0dGVtcHQudGVzdF9zdGF0cywgaW5kZW50PTIpfVxuIgotICAgICAgICAgICAgc3VtbWFyeSArPSAiS2V5IHRlc3Qgb3V0cHV0OlxuYGBgXG4iCi0gICAgICAgICAgICAjIEV4dHJhY3QgcmVsZXZhbnQgcGFydHMgb2YgdGVzdCBvdXRwdXQgKGUuZy4sIGVycm9yIG1lc3NhZ2VzKQotICAgICAgICAgICAga2V5X291dHB1dCA9ICJcbiIuam9pbihsaW5lIGZvciBsaW5lIGluIGF0dGVtcHQudGVzdF9vdXRwdXQuc3BsaXQoIlxuIikKLSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlmICJGQUlMIiBpbiBsaW5lIG9yICJFUlJPUiIgaW4gbGluZSBvciAiUEFTUyIgaW4gbGluZSkKLSAgICAgICAgICAgIHN1bW1hcnkgKz0gZiJ7a2V5X291dHB1dH1cbmBgYFxuXG4iCi0KKyAgICAgICAgICAgIHN1bW1hcnkgKz0gZiJFeGVjdXRpb24gVGltZToge2F0dGVtcHQudGVzdF9zdGF0cy5nZXQoJ2V4ZWN1dGlvbl90aW1lJywgJ04vQScpOi4yZn1zXG4iCisKKyAgICAgICAgICAgICMgVGVzdCBzdGF0aXN0aWNzCisgICAgICAgICAgICBzdGF0cyA9IGF0dGVtcHQudGVzdF9zdGF0cworICAgICAgICAgICAgdG90YWwgPSBzdGF0cy5nZXQoInRvdGFsIiwgMCkgb3IgMSAgIyBBdm9pZCBkaXZpc2lvbiBieSB6ZXJvCisgICAgICAgICAgICBwYXNzX3JhdGUgPSAoc3RhdHMuZ2V0KCJwYXNzZWQiLCAwKSAvIHRvdGFsKSAqIDEwMAorCisgICAgICAgICAgICBzdW1tYXJ5ICs9IGYiUGFzcyBSYXRlOiB7cGFzc19yYXRlOi4xZn0lICh7c3RhdHMuZ2V0KCdwYXNzZWQnLCAwKX0ve3RvdGFsfSlcbiIKKyAgICAgICAgICAgIHN1bW1hcnkgKz0gIlRlc3QgU3RhdGlzdGljczpcbiIKKyAgICAgICAgICAgIHN1bW1hcnkgKz0gZiItIFBhc3NlZDoge3N0YXRzLmdldCgncGFzc2VkJywgMCl9XG4iCisgICAgICAgICAgICBzdW1tYXJ5ICs9IGYiLSBGYWlsZWQ6IHtzdGF0cy5nZXQoJ2ZhaWxlZCcsIDApfVxuIgorICAgICAgICAgICAgc3VtbWFyeSArPSBmIi0gRXJyb3JzOiB7c3RhdHMuZ2V0KCdlcnJvcnMnLCAwKX1cbiIKKyAgICAgICAgICAgIHN1bW1hcnkgKz0gZiItIFRvdGFsOiB7dG90YWx9XG5cbiIKKworICAgICAgICAgICAgIyBFcnJvciBtZXNzYWdlcworICAgICAgICAgICAgaWYgc3RhdHMuZ2V0KCJlcnJvcl9tZXNzYWdlcyIpOgorICAgICAgICAgICAgICAgIHN1bW1hcnkgKz0gIkVycm9yIE1lc3NhZ2VzOlxuYGBgXG4iCisgICAgICAgICAgICAgICAgZm9yIGVycm9yIGluIHN0YXRzWyJlcnJvcl9tZXNzYWdlcyJdWzo1XTogICMgTGltaXQgdG8gdG9wIDUgZXJyb3JzCisgICAgICAgICAgICAgICAgICAgIHN1bW1hcnkgKz0gZiJ7ZXJyb3J9XG4iCisgICAgICAgICAgICAgICAgaWYgbGVuKHN0YXRzWyJlcnJvcl9tZXNzYWdlcyJdKSA+IDU6CisgICAgICAgICAgICAgICAgICAgIHN1bW1hcnkgKz0gZiIuLi4gYW5kIHtsZW4oc3RhdHNbJ2Vycm9yX21lc3NhZ2VzJ10pIC0gNX0gbW9yZSBlcnJvcnNcbiIKKyAgICAgICAgICAgICAgICBzdW1tYXJ5ICs9ICJgYGBcblxuIgorCisgICAgICAgICAgICAjIFRlc3QgZGV0YWlscworICAgICAgICAgICAgaWYgc3RhdHMuZ2V0KCJ0ZXN0X2RldGFpbHMiKToKKyAgICAgICAgICAgICAgICBzdW1tYXJ5ICs9ICJJbmRpdmlkdWFsIFRlc3QgUmVzdWx0czpcbmBgYFxuIgorICAgICAgICAgICAgICAgIGZvciB0ZXN0X25hbWUsIHJlc3VsdCBpbiBzdGF0c1sidGVzdF9kZXRhaWxzIl0uaXRlbXMoKToKKyAgICAgICAgICAgICAgICAgICAgc3VtbWFyeSArPSBmIntyZXN1bHR9OiB7dGVzdF9uYW1lfVxuIgorICAgICAgICAgICAgICAgIHN1bW1hcnkgKz0gImBgYFxuXG4iCisKKyAgICAgICAgIyBSZWNvbW1lbmRhdGlvbnMgZm9yIG5leHQgYXR0ZW1wdAorICAgICAgICBpZiBub3QgYXR0ZW1wdHNbLTFdLnRlc3Rfc3VjY2VzczoKKyAgICAgICAgICAgIHN1bW1hcnkgKz0gIiMjIFJlY29tbWVuZGF0aW9ucyBmb3IgTmV4dCBBdHRlbXB0XG4iCisgICAgICAgICAgICBsYXN0X3N0YXRzID0gYXR0ZW1wdHNbLTFdLnRlc3Rfc3RhdHMKKworICAgICAgICAgICAgaWYgbGFzdF9zdGF0cy5nZXQoImVycm9ycyIsIDApID4gMDoKKyAgICAgICAgICAgICAgICBzdW1tYXJ5ICs9ICItIEZvY3VzIG9uIHJlc29sdmluZyBydW50aW1lIGVycm9ycyBmaXJzdFxuIgorICAgICAgICAgICAgaWYgbGFzdF9zdGF0cy5nZXQoImZhaWxlZCIsIDApID4gMDoKKyAgICAgICAgICAgICAgICBzdW1tYXJ5ICs9ICItIEFkZHJlc3MgZmFpbGluZyB0ZXN0IGNhc2VzXG4iCisgICAgICAgICAgICBpZiBsZW4oYXR0ZW1wdHMpID4gMSBhbmQgbm90IGF0dGVtcHRzWy0xXS50ZXN0X3N1Y2Nlc3M6CisgICAgICAgICAgICAgICAgIyBDb21wYXJlIHdpdGggcHJldmlvdXMgYXR0ZW1wdAorICAgICAgICAgICAgICAgIHByZXZfc3RhdHMgPSBhdHRlbXB0c1stMl0udGVzdF9zdGF0cworICAgICAgICAgICAgICAgIGlmIGxhc3Rfc3RhdHMuZ2V0KCJwYXNzZWQiLCAwKSA8IHByZXZfc3RhdHMuZ2V0KCJwYXNzZWQiLCAwKToKKyAgICAgICAgICAgICAgICAgICAgc3VtbWFyeSArPSAiLSBSZWNlbnQgY2hhbmdlcyBjYXVzZWQgcmVncmVzc2lvbnMuIENvbnNpZGVyIHJldmVydGluZyBzb21lIGNoYW5nZXNcbiIKKwogICAgICAgICByZXR1cm4gc3VtbWFyeQoKICAgICBkZWYgZm9yd2FyZChzZWxmKToKQEAgLTIzOCwyMCArMzc1LDM2IEBAIFlvdXIgdGFzayBpcyB0byBtYWtlIGNoYW5nZXMgdG8gdGhlIGZpbGVzIGluIHRoZSB7c2VsZi5naXRfdGVtcGRpcn0gZGlyZWN0b3J5IHRvCiAgICAgICAgICAgICAjIFJ1biB0ZXN0cyBhbmQgY29sbGVjdCByZXN1bHRzCiAgICAgICAgICAgICB0ZXN0X3N1Y2Nlc3MsIHRlc3Rfb3V0cHV0LCB0ZXN0X3N0YXRzID0gc2VsZi5ydW5fdGVzdHMoKQoKLSAgICAgICAgICAgICMgQ3JlYXRlIGFuZCBzdG9yZSBhdHRlbXB0CisgICAgICAgICAgICAjIENyZWF0ZSBhbmQgc3RvcmUgYXR0ZW1wdCB3aXRoIGVuaGFuY2VkIGluZm9ybWF0aW9uCiAgICAgICAgICAgICBhdHRlbXB0ID0gU29sdXRpb25BdHRlbXB0KAogICAgICAgICAgICAgICAgIHBhdGNoPWN1cnJlbnRfcGF0Y2gsCiAgICAgICAgICAgICAgICAgdGVzdF9vdXRwdXQ9dGVzdF9vdXRwdXQsCiAgICAgICAgICAgICAgICAgdGVzdF9zdWNjZXNzPXRlc3Rfc3VjY2VzcywKLSAgICAgICAgICAgICAgICB0ZXN0X3N0YXRzPXRlc3Rfc3RhdHMKKyAgICAgICAgICAgICAgICB0ZXN0X3N0YXRzPXRlc3Rfc3RhdHMsCisgICAgICAgICAgICAgICAgZXJyb3JfbWVzc2FnZXM9dGVzdF9zdGF0cy5nZXQoJ2Vycm9yX21lc3NhZ2VzJywgW10pLAorICAgICAgICAgICAgICAgIHRlc3RfZGV0YWlscz10ZXN0X3N0YXRzLmdldCgndGVzdF9kZXRhaWxzJywge30pLAorICAgICAgICAgICAgICAgIGV4ZWN1dGlvbl90aW1lPXRlc3Rfc3RhdHMuZ2V0KCdleGVjdXRpb25fdGltZScsIE5vbmUpLAorICAgICAgICAgICAgICAgIGF0dGVtcHRfbnVtYmVyPWF0dGVtcHRfbnVtICsgMQogICAgICAgICAgICAgKQogICAgICAgICAgICAgYXR0ZW1wdHMuYXBwZW5kKGF0dGVtcHQpCgotICAgICAgICAgICAgIyBVcGRhdGUgYmVzdCBhdHRlbXB0IGlmIHRoaXMgb25lIGlzIGJldHRlcgotICAgICAgICAgICAgaWYgdGVzdF9zdWNjZXNzIGFuZCAoYmVzdF9hdHRlbXB0IGlzIE5vbmUgb3IKLSAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBhdHRlbXB0LnRlc3Rfc3RhdHNbInBhc3NlZCJdID4gYmVzdF9hdHRlbXB0LnRlc3Rfc3RhdHNbInBhc3NlZCJdKToKKyAgICAgICAgICAgICMgVXBkYXRlIGJlc3QgYXR0ZW1wdCBiYXNlZCBvbiBtdWx0aXBsZSBjcml0ZXJpYQorICAgICAgICAgICAgaWYgdGVzdF9zdWNjZXNzIGFuZCAoCisgICAgICAgICAgICAgICAgYmVzdF9hdHRlbXB0IGlzIE5vbmUgb3IKKyAgICAgICAgICAgICAgICAoYXR0ZW1wdC50ZXN0X3N0YXRzWyJwYXNzZWQiXSA+IGJlc3RfYXR0ZW1wdC50ZXN0X3N0YXRzWyJwYXNzZWQiXSkgb3IKKyAgICAgICAgICAgICAgICAoYXR0ZW1wdC50ZXN0X3N0YXRzWyJwYXNzZWQiXSA9PSBiZXN0X2F0dGVtcHQudGVzdF9zdGF0c1sicGFzc2VkIl0gYW5kCisgICAgICAgICAgICAgICAgIGxlbihhdHRlbXB0LmVycm9yX21lc3NhZ2VzIG9yIFtdKSA8IGxlbihiZXN0X2F0dGVtcHQuZXJyb3JfbWVzc2FnZXMgb3IgW10pKQorICAgICAgICAgICAgKToKICAgICAgICAgICAgICAgICBiZXN0X2F0dGVtcHQgPSBhdHRlbXB0CgorICAgICAgICAgICAgIyBMb2cgZGV0YWlsZWQgYXR0ZW1wdCBpbmZvcm1hdGlvbgorICAgICAgICAgICAgc2FmZV9sb2coZiJcbj09PSBBdHRlbXB0IHthdHRlbXB0X251bSArIDF9IFN1bW1hcnkgPT09IikKKyAgICAgICAgICAgIHNhZmVfbG9nKGYiVGVzdCBTdWNjZXNzOiB7dGVzdF9zdWNjZXNzfSIpCisgICAgICAgICAgICBzYWZlX2xvZyhmIlRlc3RzIFBhc3NlZDoge3Rlc3Rfc3RhdHMuZ2V0KCdwYXNzZWQnLCAwKX0iKQorICAgICAgICAgICAgc2FmZV9sb2coZiJUZXN0cyBGYWlsZWQ6IHt0ZXN0X3N0YXRzLmdldCgnZmFpbGVkJywgMCl9IikKKyAgICAgICAgICAgIHNhZmVfbG9nKGYiRXJyb3JzOiB7dGVzdF9zdGF0cy5nZXQoJ2Vycm9ycycsIDApfSIpCisgICAgICAgICAgICBzYWZlX2xvZyhmIkV4ZWN1dGlvbiBUaW1lOiB7dGVzdF9zdGF0cy5nZXQoJ2V4ZWN1dGlvbl90aW1lJywgJ04vQScpOi4yZn1zIikKKwogICAgICAgICAgICAgIyBJZiB0ZXN0cyBwYXNzIHBlcmZlY3RseSwgd2UgY2FuIHN0b3AKICAgICAgICAgICAgIGlmIHRlc3Rfc3VjY2VzcyBhbmQgYXR0ZW1wdC50ZXN0X3N0YXRzWyJmYWlsZWQiXSA9PSAwIGFuZCBhdHRlbXB0LnRlc3Rfc3RhdHNbImVycm9ycyJdID09IDA6CiAgICAgICAgICAgICAgICAgYnJlYWs=)
diff --git a/coding_agent.py b/coding_agent.py
index 6639abd..97f4b69 100644
--- a/coding_agent.py
+++ b/coding_agent.py
@@ -52,6 +52,10 @@ class SolutionAttempt:
test_output: str # Raw test output
test_success: bool # Whether tests passed
test_stats: dict # Test statistics (e.g., number of passed/failed tests)
+ error_messages: List[str] = None # List of specific error messages
+ test_details: dict = None # Detailed test information like specific test names and their status
+ execution_time: float = None # Test execution time in seconds
+ attempt_number: int = None # The attempt number in the sequence
def get_thread_logger():
"""
@@ -150,12 +154,82 @@ class AgenticSystem:
]
return new_msg_history
+ def extract_test_details(self, output: str) -> tuple[dict, List[str], dict]:
+ """Extract detailed test information from the output."""
+ error_messages = []
+ test_details = {}
+ stats = {"passed": 0, "failed": 0, "errors": 0, "total": 0, "skipped": 0}
+
+ # Split output into lines for analysis
+ lines = output.split("\n")
+
+ # Language-specific parsing
+ if self.language == "python":
+ for line in lines:
+ if "FAILED" in line and "::" in line:
+ test_name = line.split("::")[1].split()[0]
+ test_details[test_name] = "FAILED"
+ stats["failed"] += 1
+ elif "PASSED" in line and "::" in line:
+ test_name = line.split("::")[1].split()[0]
+ test_details[test_name] = "PASSED"
+ stats["passed"] += 1
+ elif "ERROR" in line and "::" in line:
+ test_name = line.split("::")[1].split()[0]
+ test_details[test_name] = "ERROR"
+ stats["errors"] += 1
+ # Extract error message
+ if lines.index(line) + 1 < len(lines):
+ error_messages.append(lines[lines.index(line) + 1])
+
+ elif self.language in ["javascript", "node"]:
+ current_test = None
+ for line in lines:
+ if line.startswith(’checkmark’):
+ test_name = line.replace(’checkmark,’, ’’).strip()
+ test_details[test_name] = "PASSED"
+ stats["passed"] += 1
+ elif line.startswith(’x’):
+ test_name = line.replace(’x’, ’’).strip()
+ test_details[test_name] = "FAILED"
+ stats["failed"] += 1
+ current_test = test_name
+ elif current_test and (’Error:’ in line or ’AssertionError:’ in line):
+ error_messages.append(f"{current_test}: {line.strip()}")
+
+ elif self.language == "rust":
+ for line in lines:
+ if "test" in line and "... ok" in line:
+ test_name = line.split("test")[1].split("...")[0].strip()
+ test_details[test_name] = "PASSED"
+ stats["passed"] += 1
+ elif "test" in line and "... FAILED" in line:
+ test_name = line.split("test")[1].split("...")[0].strip()
+ test_details[test_name] = "FAILED"
+ stats["failed"] += 1
+ elif "---- " in line and " stdout ----" in line:
+ test_name = line.split("----")[1].split("stdout")[0].strip()
+ if test_name in test_details and test_details[test_name] == "FAILED":
+ error_messages.append(f"{test_name}: {next((l for l in lines[lines.index(line)+1:] if l.strip()), ’’)}")
+
+ # Generic counting for other languages or as fallback
+ if not any(stats.values()):
+ stats["passed"] = output.count("PASS") + output.count("ok")
+ stats["failed"] = output.count("FAIL") + output.count("not ok")
+ stats["errors"] = output.count("ERROR") + output.count("panic:")
+
+ stats["total"] = stats["passed"] + stats["failed"] + stats["errors"]
+
+ return stats, error_messages, test_details
+
def run_tests(self) -> tuple[bool, str, dict]:
"""Run tests and return success status, output, and test statistics."""
+ import time
+
success = False
output = ""
- stats = {"passed": 0, "failed": 0, "errors": 0, "total": 0}
-
+ start_time = time.time()
+
try:
for command in TEST_COMMANDS.get(self.language, []):
proc = subprocess.run(
@@ -169,34 +243,97 @@ class AgenticSystem:
success = proc.returncode == 0
if not success:
break
-
- # Try to extract test statistics from output
- # This is a simple example; you might want to add more sophisticated parsing
- stats["passed"] = output.count("PASS") + output.count("ok")
- stats["failed"] = output.count("FAIL") + output.count("not ok")
- stats["errors"] = output.count("ERROR") + output.count("panic:")
- stats["total"] = stats["passed"] + stats["failed"] + stats["errors"]
+
+ # Extract detailed test information
+ stats, error_messages, test_details = self.extract_test_details(output)
+ stats["execution_time"] = time.time() - start_time
+
+ # Enhance stats with extracted information
+ stats["error_messages"] = error_messages
+ stats["test_details"] = test_details
except Exception as e:
output = f"Error running tests: {str(e)}"
success = False
+ stats = {
+ "passed": 0, "failed": 0, "errors": 1, "total": 1,
+ "execution_time": time.time() - start_time,
+ "error_messages": [str(e)],
+ "test_details": {}
+ }
return success, output, stats
def analyze_test_results(self, attempts: List[SolutionAttempt]) -> str:
- """Analyze test results and create a summary for the agent."""
+ """Analyze test results and create a detailed summary for the agent."""
summary = "# Test Results Analysis\n\n"
+ # Overall progress tracking
+ if len(attempts) > 1:
+ summary += "## Progress Overview\n"
+ first_attempt = attempts[0].test_stats
+ last_attempt = attempts[-1].test_stats
+
+ progress = {
+ "passed": last_attempt["passed"] - first_attempt["passed"],
+ "failed": first_attempt["failed"] - last_attempt["failed"],
+ "errors": first_attempt["errors"] - last_attempt["errors"]
+ }
+
+ summary += "Progress since first attempt:\n"
+ summary += f"- Additional passing tests: {progress[’passed’]}\n"
+ summary += f"- Reduced failures: {progress[’failed’]}\n"
+ summary += f"- Reduced errors: {progress[’errors’]}\n\n"
+
+ # Detailed attempt analysis
for i, attempt in enumerate(attempts, 1):
summary += f"## Attempt {i}\n"
summary += f"Test Success: {attempt.test_success}\n"
- summary += f"Test Stats: {json.dumps(attempt.test_stats, indent=2)}\n"
- summary += "Key test output:\n‘‘‘\n"
- # Extract relevant parts of test output (e.g., error messages)
- key_output = "\n".join(line for line in attempt.test_output.split("\n")
- if "FAIL" in line or "ERROR" in line or "PASS" in line)
- summary += f"{key_output}\n‘‘‘\n\n"
-
+ summary += f"Execution Time: {attempt.test_stats.get(’execution_time’, ’N/A’):.2f}s\n"
+
+ # Test statistics
+ stats = attempt.test_stats
+ total = stats.get("total", 0) or 1 # Avoid division by zero
+ pass_rate = (stats.get("passed", 0) / total) * 100
+
+ summary += f"Pass Rate: {pass_rate:.1f}% ({stats.get(’passed’, 0)}/{total})\n"
+ summary += "Test Statistics:\n"
+ summary += f"- Passed: {stats.get(’passed’, 0)}\n"
+ summary += f"- Failed: {stats.get(’failed’, 0)}\n"
+ summary += f"- Errors: {stats.get(’errors’, 0)}\n"
+ summary += f"- Total: {total}\n\n"
+
+ # Error messages
+ if stats.get("error_messages"):
+ summary += "Error Messages:\n‘‘‘\n"
+ for error in stats["error_messages"][:5]: # Limit to top 5 errors
+ summary += f"{error}\n"
+ if len(stats["error_messages"]) > 5:
+ summary += f"... and {len(stats[’error_messages’]) - 5} more errors\n"
+ summary += "‘‘‘\n\n"
+
+ # Test details
+ if stats.get("test_details"):
+ summary += "Individual Test Results:\n‘‘‘\n"
+ for test_name, result in stats["test_details"].items():
+ summary += f"{result}: {test_name}\n"
+ summary += "‘‘‘\n\n"
+
+ # Recommendations for next attempt
+ if not attempts[-1].test_success:
+ summary += "## Recommendations for Next Attempt\n"
+ last_stats = attempts[-1].test_stats
+
+ if last_stats.get("errors", 0) > 0:
+ summary += "- Focus on resolving runtime errors first\n"
+ if last_stats.get("failed", 0) > 0:
+ summary += "- Address failing test cases\n"
+ if len(attempts) > 1 and not attempts[-1].test_success:
+ # Compare with previous attempt
+ prev_stats = attempts[-2].test_stats
+ if last_stats.get("passed", 0) < prev_stats.get("passed", 0):
+ summary += "- Recent changes caused regressions. Consider reverting some changes\n"
+
return summary
def forward(self):
@@ -238,20 +375,36 @@ Your task is to make changes to the files in the {self.git_tempdir} directory to
# Run tests and collect results
test_success, test_output, test_stats = self.run_tests()
- # Create and store attempt
+ # Create and store attempt with enhanced information
attempt = SolutionAttempt(
patch=current_patch,
test_output=test_output,
test_success=test_success,
- test_stats=test_stats
+ test_stats=test_stats,
+ error_messages=test_stats.get(’error_messages’, []),
+ test_details=test_stats.get(’test_details’, {}),
+ execution_time=test_stats.get(’execution_time’, None),
+ attempt_number=attempt_num + 1
)
attempts.append(attempt)
- # Update best attempt if this one is better
- if test_success and (best_attempt is None or
- attempt.test_stats["passed"] > best_attempt.test_stats["passed"]):
+ # Update best attempt based on multiple criteria
+ if test_success and (
+ best_attempt is None or
+ (attempt.test_stats["passed"] > best_attempt.test_stats["passed"]) or
+ (attempt.test_stats["passed"] == best_attempt.test_stats["passed"] and
+ len(attempt.error_messages or []) < len(best_attempt.error_messages or []))
+ ):
best_attempt = attempt
+ # Log detailed attempt information
+ safe_log(f"\n=== Attempt {attempt_num + 1} Summary ===")
+ safe_log(f"Test Success: {test_success}")
+ safe_log(f"Tests Passed: {test_stats.get(’passed’, 0)}")
+ safe_log(f"Tests Failed: {test_stats.get(’failed’, 0)}")
+ safe_log(f"Errors: {test_stats.get(’errors’, 0)}")
+ safe_log(f"Execution Time: {test_stats.get(’execution_time’, ’N/A’):.2f}s")
+
# If tests pass perfectly, we can stop
if test_success and attempt.test_stats["failed"] == 0 and attempt.test_stats["errors"] == 0:
break
```

## 附录 G 相似的目标功能，不同的实现

即使目标功能相同，提供给编码智能体的建议以及由此产生的实现也可能大相径庭，从而导致编码能力与基准测试性能的巨大差异。例如，考虑 DGM 在 SWE-bench 上运行时的节点 6 与节点 24（图 3）。两者都旨在增强现有的编辑器工具以支持更细粒度的文件编辑。然而，节点 6 的实现保留了原有的 edit 命令并新增了参数 edit_type 与 edit_actions，而节点 24 的实现则用一个新的 str_replace 命令替换了原有的 edit 命令。尽管目标的功能相似，功能建议以及由此决定的实现细节却差异巨大，性能也同样如此：节点 6 仅取得 23.3%，而节点 24 取得了 40.5%。

产生节点 6 的功能建议：

[⬇](data:text/plain;base64,V2l0aGluIHRoZSB0b29scy9lZGl0LnB5IGZpbGUsIHJlbW92ZSB0aGUgJ2VkaXQnIGNvbW1hbmQgYW5kIGludHJvZHVjZSBhICdzdHJfcmVwbGFjZScgY29tbWFuZC4gSXQgc2hvdWxkIGFjY2VwdCBwYXJhbWV0ZXJzICdvbGRfc3RyJyAodGhlIHVuaXF1ZSB0ZXh0IHRvIGZpbmQpIGFuZCAnbmV3X3N0cicgKHRoZSBuZXcgdGV4dCB0byByZXBsYWNlIGl0IHdpdGgpLiBBZnRlciB2ZXJpZnlpbmcgdGhhdCAnb2xkX3N0cicgYXBwZWFycyBleGFjdGx5IG9uY2UgaW4gdGhlIGZpbGUsIHJlcGxhY2UgdGhlIGZpcnN0IG9jY3VycmVuY2Ugd2l0aCAnbmV3X3N0cicuIElmICdvbGRfc3RyJyBpcyBub3QgdW5pcXVlIG9yIGlzIG1pc3NpbmcsIGRvIG5vdCB3cml0ZSBhbnkgY2hhbmdlcy4KClJlcGxhY2UgdGhlICdlZGl0JyBjb21tYW5kIGluIHRoZSBlZGl0b3IgdG9vbCB3aXRoIGEgJ3N0cl9yZXBsYWNlJyBjb21tYW5kIHRoYXQgbG9jYXRlcyBhbmQgcmVwbGFjZXMgYW4gZXhhY3Qgc3Vic3RyaW5nIGluIGEgZmlsZS4gVGhlICdvbGRfc3RyJyBtdXN0IG1hdGNoIGNvbnNlY3V0aXZlIGxpbmVzIHVuaXF1ZWx5LCBhbmQgaWYgaXQgaXMgbm90IGZvdW5kIG9yIG9jY3VycyBtdWx0aXBsZSB0aW1lcywgbm8gd3JpdGUgc2hvdWxkIG9jY3VyLiBUaGUgJ25ld19zdHInIHBhcmFtZXRlciBjb250YWlucyB0aGUgcmV2aXNlZCBsaW5lcy4gVGhpcyBwcmVjaXNlIHN1YnN0cmluZyByZXBsYWNlbWVudCBmbG93IHdpbGwgZW5hYmxlIHNtYWxsIGluY3JlbWVudGFsIGVkaXRzIHdpdGggbWluaW1hbCBicmVha2FnZS4=)

````text
Within the tools/edit.py file, remove the ’edit’ command and introduce a ’str_replace’ command. It should accept parameters ’old_str’ (the unique text to find) and ’new_str’ (the new text to replace it with). After verifying that ’old_str’ appears exactly once in the file, replace the first occurrence with ’new_str’. If ’old_str’ is not unique or is missing, do not write any changes.
Replace the ’edit’ command in the editor tool with a ’str_replace’ command that locates and replaces an exact substring in a file. The ’old_str’ must match consecutive lines uniquely, and if it is not found or occurs multiple times, no write should occur. The ’new_str’ parameter contains the revised lines. This precise substring replacement flow will enable small incremental edits with minimal breakage.
````

产生节点 24 的功能建议：

[⬇](data:text/plain;base64,QXVnbWVudCB0aGUgZXhpc3RpbmcgJ2VkaXRvcicgdG9vbCB0byBzdXBwb3J0IGxpbmUgb3IgdG9rZW4tYmFzZWQgZWRpdGluZy4gVGhlIGFnZW50IHdvdWxkIHNwZWNpZnkgaW5kaXZpZHVhbCBsaW5lcyBvciB0b2tlbnMgdG8gaW5zZXJ0LCBkZWxldGUsIG9yIHJlcGxhY2UuIEludGVybmFsbHksIHRoZSB0b29sIHdvdWxkIHBhcnNlIHRoZSBmaWxlIGNvbnRlbnRzLCBhcHBseSBjaGFuZ2VzIGF0b21pY2FsbHksIGFuZCB2ZXJpZnkgdGhhdCB0aGUgc3Vycm91bmRpbmcgY29udGV4dCByZW1haW5zIGludGFjdC4gVGhpcyBwcmV2ZW50cyBlbnRpcmUtZmlsZSBvdmVyd3JpdGVzLCByZWR1Y2luZyB0aGUgcmlzayBvZiBsb3NpbmcgdW5yZWxhdGVkIGxvZ2ljLiBUaGUgdG9vbCBjb3VsZCBhbHNvIHZhbGlkYXRlIHRoYXQgdGhlIGVkaXRlZCBsaW5lcyBtYXRjaCBleHBlY3RlZCBjb2RlIGZyYWdtZW50cyB0byBjYXRjaCB1bmFudGljaXBhdGVkIGRpZmZlcmVuY2VzIG9yIG1lcmdlIGNvbmZsaWN0cy4KCkVuaGFuY2UgdGhlIGFnZW50J3MgZmlsZSBlZGl0aW5nIHByb2Nlc3MgdG8gc3VwcG9ydCBmaW5lLWdyYWluZWQgZWRpdHMuIFNwZWNpZmljYWxseSwgYWRkIGEgbGluZS1iYXNlZCBvciB0b2tlbi1iYXNlZCBlZGl0aW5nIGZlYXR1cmUgaW4gdGhlICdlZGl0b3InIHRvb2wuIFRoaXMgaW1wcm92ZW1lbnQgc2hvdWxkIGxldCB0aGUgYWdlbnQgaW5zZXJ0LCByZXBsYWNlLCBvciBkZWxldGUgc21hbGwgc2VjdGlvbnMgb2YgY29kZSB3aXRob3V0IG92ZXJ3cml0aW5nIGVudGlyZSBmaWxlcyBvciBsYXJnZSBibG9ja3MsIHByZXNlcnZpbmcgdW5yZWxhdGVkIGxvZ2ljLiBJbXBsZW1lbnQgc2FmZWd1YXJkcyB0byBjb25maXJtIHRoYXQgY29udGV4dHVhbCBjb2RlIGFyb3VuZCB0aGUgZWRpdGVkIHJlZ2lvbiByZW1haW5zIGFjY3VyYXRlLCBzbyB3ZSByZWR1Y2UgdGhlIHJpc2sgb2YgY3JlYXRpbmcgcmVncmVzc2lvbnMgd2hlbiBmaXhpbmcgaXNzdWVzLg==)

````text
Augment the existing ’editor’ tool to support line or token-based editing. The agent would specify individual lines or tokens to insert, delete, or replace. Internally, the tool would parse the file contents, apply changes atomically, and verify that the surrounding context remains intact. This prevents entire-file overwrites, reducing the risk of losing unrelated logic. The tool could also validate that the edited lines match expected code fragments to catch unanticipated differences or merge conflicts.
Enhance the agent’s file editing process to support fine-grained edits. Specifically, add a line-based or token-based editing feature in the ’editor’ tool. This improvement should let the agent insert, replace, or delete small sections of code without overwriting entire files or large blocks, preserving unrelated logic. Implement safeguards to confirm that contextual code around the edited region remains accurate, so we reduce the risk of creating regressions when fixing issues.-
````

产生节点 6 的建议功能实现：

```diff
[⬇](data:text/plain;base64,ZGlmZiAtLWdpdCBhL3Rlc3RzL3Rlc3RfZWRpdF90b29sLnB5IGIvdGVzdHMvdGVzdF9lZGl0X3Rvb2wucHkKaW5kZXggZjA3ODJjNi4uZDNhNGQ1YyAxMDA2NDQKLS0tIGEvdGVzdHMvdGVzdF9lZGl0X3Rvb2wucHkKKysrIGIvdGVzdHMvdGVzdF9lZGl0X3Rvb2wucHkKQEAgLTEsNyArMSw3IEBACiBpbXBvcnQgcHl0ZXN0CiBmcm9tIHBhdGhsaWIgaW1wb3J0IFBhdGgKIGltcG9ydCB0ZW1wZmlsZQotZnJvbSB0b29scy5lZGl0IGltcG9ydCB0b29sX2Z1bmN0aW9uCitmcm9tIHRvb2xzLmVkaXQgaW1wb3J0IHRvb2xfZnVuY3Rpb24sIHZhbGlkYXRlX2VkaXRfYWN0aW9ucywgdmFsaWRhdGVfY29udGV4dAoKIEBweXRlc3QuZml4dHVyZQogZGVmIHRlbXBfZGlyKCk6CkBAIC0xNyw2ICsxNywxOCBAQCBkZWYgc2FtcGxlX2ZpbGUodGVtcF9kaXIpOgogICAgIGZpbGVfcGF0aC53cml0ZV90ZXh0KGNvbnRlbnQpCiAgICAgcmV0dXJuIGZpbGVfcGF0aAoKK0BweXRlc3QuZml4dHVyZQorZGVmIGNvZGVfZmlsZSh0ZW1wX2Rpcik6CisgICAgIiIiQ3JlYXRlIGEgc2FtcGxlIFB5dGhvbiBmaWxlIGZvciB0ZXN0aW5nIHRva2VuLWJhc2VkIGVkaXRzLiIiIgorICAgIGZpbGVfcGF0aCA9IHRlbXBfZGlyIC8gInRlc3QucHkiCisgICAgY29udGVudCA9ICIiImRlZiB0ZXN0X2Z1bmN0aW9uKCk6CisgICAgeCA9IDQyCisgICAgeSA9ICJvbGRfdmFsdWUiCisgICAgcmV0dXJuIHggKyBsZW4oeSkKKyIiIgorICAgIGZpbGVfcGF0aC53cml0ZV90ZXh0KGNvbnRlbnQpCisgICAgcmV0dXJuIGZpbGVfcGF0aAorCiBjbGFzcyBUZXN0RWRpdG9yVG9vbDoKICAgICBkZWYgdGVzdF92aWV3X2ZpbGUoc2VsZiwgc2FtcGxlX2ZpbGUpOgogICAgICAgICAiIiJUZXN0IHZpZXdpbmcgZW50aXJlIGZpbGUgY29udGVudC4iIiIKQEAgLTM5LDE3ICs1MSwxODIgQEAgY2xhc3MgVGVzdEVkaXRvclRvb2w6CiAgICAgICAgIGFzc2VydCAiRXJyb3IiIGluIHJlc3VsdAogICAgICAgICBhc3NlcnQgImFscmVhZHkgZXhpc3RzIiBpbiByZXN1bHQKCi0gICAgZGVmIHRlc3RfZWRpdF9maWxlKHNlbGYsIHNhbXBsZV9maWxlKToKLSAgICAgICAgIiIiVGVzdCBlZGl0aW5nIGFuIGV4aXN0aW5nIGZpbGUuIiIiCisgICAgZGVmIHRlc3RfZWRpdF9maWxlX2Z1bGwoc2VsZiwgc2FtcGxlX2ZpbGUpOgorICAgICAgICAiIiJUZXN0IGVkaXRpbmcgYW4gZXhpc3RpbmcgZmlsZSB3aXRoIGZpbGUgbW9kZS4iIiIKICAgICAgICAgbmV3X2NvbnRlbnQgPSAiZWRpdGVkIGNvbnRlbnRcbm5ldyBsaW5lIgotICAgICAgICByZXN1bHQgPSB0b29sX2Z1bmN0aW9uKCJlZGl0Iiwgc3RyKHNhbXBsZV9maWxlKSwgZmlsZV90ZXh0PW5ld19jb250ZW50KQorICAgICAgICByZXN1bHQgPSB0b29sX2Z1bmN0aW9uKAorICAgICAgICAgICAgImVkaXQiLAorICAgICAgICAgICAgc3RyKHNhbXBsZV9maWxlKSwKKyAgICAgICAgICAgIGZpbGVfdGV4dD1uZXdfY29udGVudCwKKyAgICAgICAgICAgIGVkaXRfdHlwZT0iZmlsZSIKKyAgICAgICAgKQogICAgICAgICBhc3NlcnQgImhhcyBiZWVuIG92ZXJ3cml0dGVuIiBpbiByZXN1bHQKICAgICAgICAgYXNzZXJ0IHNhbXBsZV9maWxlLnJlYWRfdGV4dCgpID09IG5ld19jb250ZW50CgorICAgIGRlZiB0ZXN0X2xpbmVfYmFzZWRfZWRpdF9pbnNlcnQoc2VsZiwgc2FtcGxlX2ZpbGUpOgorICAgICAgICAiIiJUZXN0IGxpbmUtYmFzZWQgaW5zZXJ0IG9wZXJhdGlvbi4iIiIKKyAgICAgICAgYWN0aW9ucyA9IFt7CisgICAgICAgICAgICAiYWN0aW9uIjogImluc2VydCIsCisgICAgICAgICAgICAibGluZV9udW1iZXIiOiAzLAorICAgICAgICAgICAgImNvbnRlbnQiOiAiaW5zZXJ0ZWQgbGluZSIKKyAgICAgICAgfV0KKyAgICAgICAgcmVzdWx0ID0gdG9vbF9mdW5jdGlvbigKKyAgICAgICAgICAgICJlZGl0IiwKKyAgICAgICAgICAgIHN0cihzYW1wbGVfZmlsZSksCisgICAgICAgICAgICBlZGl0X3R5cGU9ImxpbmUiLAorICAgICAgICAgICAgZWRpdF9hY3Rpb25zPWFjdGlvbnMKKyAgICAgICAgKQorICAgICAgICBhc3NlcnQgInN1Y2Nlc3NmdWxseSBlZGl0ZWQiIGluIHJlc3VsdAorICAgICAgICBjb250ZW50ID0gc2FtcGxlX2ZpbGUucmVhZF90ZXh0KCkuc3BsaXRsaW5lcygpCisgICAgICAgIGFzc2VydCBjb250ZW50WzJdID09ICJpbnNlcnRlZCBsaW5lIgorICAgICAgICBhc3NlcnQgbGVuKGNvbnRlbnQpID09IDYKKworICAgIGRlZiB0ZXN0X2xpbmVfYmFzZWRfZWRpdF9kZWxldGUoc2VsZiwgc2FtcGxlX2ZpbGUpOgorICAgICAgICAiIiJUZXN0IGxpbmUtYmFzZWQgZGVsZXRlIG9wZXJhdGlvbi4iIiIKKyAgICAgICAgYWN0aW9ucyA9IFt7CisgICAgICAgICAgICAiYWN0aW9uIjogImRlbGV0ZSIsCisgICAgICAgICAgICAibGluZV9udW1iZXIiOiAyCisgICAgICAgIH1dCisgICAgICAgIHJlc3VsdCA9IHRvb2xfZnVuY3Rpb24oCisgICAgICAgICAgICAiZWRpdCIsCisgICAgICAgICAgICBzdHIoc2FtcGxlX2ZpbGUpLAorICAgICAgICAgICAgZWRpdF90eXBlPSJsaW5lIiwKKyAgICAgICAgICAgIGVkaXRfYWN0aW9ucz1hY3Rpb25zCisgICAgICAgICkKKyAgICAgICAgYXNzZXJ0ICJzdWNjZXNzZnVsbHkgZWRpdGVkIiBpbiByZXN1bHQKKyAgICAgICAgY29udGVudCA9IHNhbXBsZV9maWxlLnJlYWRfdGV4dCgpLnNwbGl0bGluZXMoKQorICAgICAgICBhc3NlcnQgImxpbmUgMiIgbm90IGluIGNvbnRlbnQKKyAgICAgICAgYXNzZXJ0IGxlbihjb250ZW50KSA9PSA0CisKKyAgICBkZWYgdGVzdF9saW5lX2Jhc2VkX2VkaXRfcmVwbGFjZShzZWxmLCBzYW1wbGVfZmlsZSk6CisgICAgICAgICIiIlRlc3QgbGluZS1iYXNlZCByZXBsYWNlIG9wZXJhdGlvbi4iIiIKKyAgICAgICAgYWN0aW9ucyA9IFt7CisgICAgICAgICAgICAiYWN0aW9uIjogInJlcGxhY2UiLAorICAgICAgICAgICAgImxpbmVfbnVtYmVyIjogMywKKyAgICAgICAgICAgICJjb250ZW50IjogInJlcGxhY2VkIGxpbmUiCisgICAgICAgIH1dCisgICAgICAgIHJlc3VsdCA9IHRvb2xfZnVuY3Rpb24oCisgICAgICAgICAgICAiZWRpdCIsCisgICAgICAgICAgICBzdHIoc2FtcGxlX2ZpbGUpLAorICAgICAgICAgICAgZWRpdF90eXBlPSJsaW5lIiwKKyAgICAgICAgICAgIGVkaXRfYWN0aW9ucz1hY3Rpb25zCisgICAgICAgICkKKyAgICAgICAgYXNzZXJ0ICJzdWNjZXNzZnVsbHkgZWRpdGVkIiBpbiByZXN1bHQKKyAgICAgICAgY29udGVudCA9IHNhbXBsZV9maWxlLnJlYWRfdGV4dCgpLnNwbGl0bGluZXMoKQorICAgICAgICBhc3NlcnQgY29udGVudFsyXSA9PSAicmVwbGFjZWQgbGluZSIKKyAgICAgICAgYXNzZXJ0IGxlbihjb250ZW50KSA9PSA1CisKKyAgICBkZWYgdGVzdF90b2tlbl9iYXNlZF9lZGl0KHNlbGYsIGNvZGVfZmlsZSk6CisgICAgICAgICIiIlRlc3QgdG9rZW4tYmFzZWQgZWRpdCBvcGVyYXRpb24uIiIiCisgICAgICAgIGFjdGlvbnMgPSBbeworICAgICAgICAgICAgImFjdGlvbiI6ICJyZXBsYWNlIiwKKyAgICAgICAgICAgICJvbGRfdG9rZW4iOiAib2xkX3ZhbHVlIiwKKyAgICAgICAgICAgICJuZXdfdG9rZW4iOiAibmV3X3ZhbHVlIgorICAgICAgICB9XQorICAgICAgICByZXN1bHQgPSB0b29sX2Z1bmN0aW9uKAorICAgICAgICAgICAgImVkaXQiLAorICAgICAgICAgICAgc3RyKGNvZGVfZmlsZSksCisgICAgICAgICAgICBlZGl0X3R5cGU9InRva2VuIiwKKyAgICAgICAgICAgIGVkaXRfYWN0aW9ucz1hY3Rpb25zCisgICAgICAgICkKKyAgICAgICAgYXNzZXJ0ICJzdWNjZXNzZnVsbHkgZWRpdGVkIiBpbiByZXN1bHQKKyAgICAgICAgY29udGVudCA9IGNvZGVfZmlsZS5yZWFkX3RleHQoKQorICAgICAgICBhc3NlcnQgIm9sZF92YWx1ZSIgbm90IGluIGNvbnRlbnQKKyAgICAgICAgYXNzZXJ0ICJuZXdfdmFsdWUiIGluIGNvbnRlbnQKKworICAgIGRlZiB0ZXN0X211bHRpcGxlX3Rva2VuX2VkaXRzKHNlbGYsIGNvZGVfZmlsZSk6CisgICAgICAgICIiIlRlc3QgbXVsdGlwbGUgdG9rZW4tYmFzZWQgZWRpdCBvcGVyYXRpb25zLiIiIgorICAgICAgICBhY3Rpb25zID0gWworICAgICAgICAgICAgeworICAgICAgICAgICAgICAgICJhY3Rpb24iOiAicmVwbGFjZSIsCisgICAgICAgICAgICAgICAgIm9sZF90b2tlbiI6ICI0MiIsCisgICAgICAgICAgICAgICAgIm5ld190b2tlbiI6ICIxMDAiCisgICAgICAgICAgICB9LAorICAgICAgICAgICAgeworICAgICAgICAgICAgICAgICJhY3Rpb24iOiAicmVwbGFjZSIsCisgICAgICAgICAgICAgICAgIm9sZF90b2tlbiI6ICJvbGRfdmFsdWUiLAorICAgICAgICAgICAgICAgICJuZXdfdG9rZW4iOiAibmV3X3RleHQiCisgICAgICAgICAgICB9CisgICAgICAgIF0KKyAgICAgICAgcmVzdWx0ID0gdG9vbF9mdW5jdGlvbigKKyAgICAgICAgICAgICJlZGl0IiwKKyAgICAgICAgICAgIHN0cihjb2RlX2ZpbGUpLAorICAgICAgICAgICAgZWRpdF90eXBlPSJ0b2tlbiIsCisgICAgICAgICAgICBlZGl0X2FjdGlvbnM9YWN0aW9ucworICAgICAgICApCisgICAgICAgIGFzc2VydCAic3VjY2Vzc2Z1bGx5IGVkaXRlZCIgaW4gcmVzdWx0CisgICAgICAgIGNvbnRlbnQgPSBjb2RlX2ZpbGUucmVhZF90ZXh0KCkKKyAgICAgICAgYXNzZXJ0ICI0MiIgbm90IGluIGNvbnRlbnQKKyAgICAgICAgYXNzZXJ0ICIxMDAiIGluIGNvbnRlbnQKKyAgICAgICAgYXNzZXJ0ICJvbGRfdmFsdWUiIG5vdCBpbiBjb250ZW50CisgICAgICAgIGFzc2VydCAibmV3X3RleHQiIGluIGNvbnRlbnQKKworICAgIGRlZiB0ZXN0X2ludmFsaWRfbGluZV9udW1iZXIoc2VsZiwgc2FtcGxlX2ZpbGUpOgorICAgICAgICAiIiJUZXN0IGVkaXQgd2l0aCBpbnZhbGlkIGxpbmUgbnVtYmVyLiIiIgorICAgICAgICBhY3Rpb25zID0gW3sKKyAgICAgICAgICAgICJhY3Rpb24iOiAicmVwbGFjZSIsCisgICAgICAgICAgICAibGluZV9udW1iZXIiOiAxMDAsCisgICAgICAgICAgICAiY29udGVudCI6ICJpbnZhbGlkIGxpbmUiCisgICAgICAgIH1dCisgICAgICAgIHJlc3VsdCA9IHRvb2xfZnVuY3Rpb24oCisgICAgICAgICAgICAiZWRpdCIsCisgICAgICAgICAgICBzdHIoc2FtcGxlX2ZpbGUpLAorICAgICAgICAgICAgZWRpdF90eXBlPSJsaW5lIiwKKyAgICAgICAgICAgIGVkaXRfYWN0aW9ucz1hY3Rpb25zCisgICAgICAgICkKKyAgICAgICAgYXNzZXJ0ICJFcnJvciIgaW4gcmVzdWx0CisgICAgICAgIGFzc2VydCAiZXhjZWVkcyBmaWxlIGxlbmd0aCIgaW4gcmVzdWx0CisKKyAgICBkZWYgdGVzdF9pbnZhbGlkX2VkaXRfdHlwZShzZWxmLCBzYW1wbGVfZmlsZSk6CisgICAgICAgICIiIlRlc3QgZWRpdCB3aXRoIGludmFsaWQgZWRpdCB0eXBlLiIiIgorICAgICAgICByZXN1bHQgPSB0b29sX2Z1bmN0aW9uKAorICAgICAgICAgICAgImVkaXQiLAorICAgICAgICAgICAgc3RyKHNhbXBsZV9maWxlKSwKKyAgICAgICAgICAgIGVkaXRfdHlwZT0iaW52YWxpZCIsCisgICAgICAgICAgICBlZGl0X2FjdGlvbnM9W3siYWN0aW9uIjogInJlcGxhY2UifV0KKyAgICAgICAgKQorICAgICAgICBhc3NlcnQgIkVycm9yIiBpbiByZXN1bHQKKyAgICAgICAgYXNzZXJ0ICJJbnZhbGlkIGVkaXRfdHlwZSIgaW4gcmVzdWx0CisKKyAgICBkZWYgdGVzdF9taXNzaW5nX3JlcXVpcmVkX2ZpZWxkcyhzZWxmLCBzYW1wbGVfZmlsZSk6CisgICAgICAgICIiIlRlc3QgZWRpdCB3aXRoIG1pc3NpbmcgcmVxdWlyZWQgZmllbGRzLiIiIgorICAgICAgICBhY3Rpb25zID0gW3sKKyAgICAgICAgICAgICJhY3Rpb24iOiAicmVwbGFjZSIgICMgTWlzc2luZyBsaW5lX251bWJlciBhbmQgY29udGVudAorICAgICAgICB9XQorICAgICAgICByZXN1bHQgPSB0b29sX2Z1bmN0aW9uKAorICAgICAgICAgICAgImVkaXQiLAorICAgICAgICAgICAgc3RyKHNhbXBsZV9maWxlKSwKKyAgICAgICAgICAgIGVkaXRfdHlwZT0ibGluZSIsCisgICAgICAgICAgICBlZGl0X2FjdGlvbnM9YWN0aW9ucworICAgICAgICApCisgICAgICAgIGFzc2VydCAiRXJyb3IiIGluIHJlc3VsdAorICAgICAgICBhc3NlcnQgIk1pc3NpbmcgcmVxdWlyZWQgZmllbGQiIGluIHJlc3VsdAorCisgICAgZGVmIHRlc3RfdmFsaWRhdGVfY29udGV4dChzZWxmKToKKyAgICAgICAgIiIiVGVzdCBjb250ZXh0IHZhbGlkYXRpb24gZnVuY3Rpb24uIiIiCisgICAgICAgIG9yaWdpbmFsID0gImxpbmUgMVxubGluZSAyXG5saW5lIDNcbmxpbmUgNFxubGluZSA1IgorICAgICAgICBtb2RpZmllZCA9ICJsaW5lIDFcbmxpbmUgMlxubW9kaWZpZWRcbmxpbmUgNFxubGluZSA1IgorICAgICAgICBhc3NlcnQgdmFsaWRhdGVfY29udGV4dChvcmlnaW5hbCwgbW9kaWZpZWQpIGlzIFRydWUKKworICAgICAgICAjIFRlc3QgaW52YWxpZCBjb250ZXh0ICh0b28gbWFueSBjaGFuZ2VzKQorICAgICAgICBtb2RpZmllZCA9ICJjb21wbGV0ZWx5XG5kaWZmZXJlbnRcbmNvbnRlbnQiCisgICAgICAgIGFzc2VydCB2YWxpZGF0ZV9jb250ZXh0KG9yaWdpbmFsLCBtb2RpZmllZCkgaXMgRmFsc2UKKworICAgIGRlZiB0ZXN0X2VtcHR5X2VkaXRfYWN0aW9ucyhzZWxmLCBzYW1wbGVfZmlsZSk6CisgICAgICAgICIiIlRlc3QgZWRpdCB3aXRoIGVtcHR5IGVkaXQgYWN0aW9ucy4iIiIKKyAgICAgICAgcmVzdWx0ID0gdG9vbF9mdW5jdGlvbigKKyAgICAgICAgICAgICJlZGl0IiwKKyAgICAgICAgICAgIHN0cihzYW1wbGVfZmlsZSksCisgICAgICAgICAgICBlZGl0X3R5cGU9ImxpbmUiLAorICAgICAgICAgICAgZWRpdF9hY3Rpb25zPVtdCisgICAgICAgICkKKyAgICAgICAgYXNzZXJ0ICJFcnJvciIgaW4gcmVzdWx0CisgICAgICAgIGFzc2VydCAiRWRpdCBhY3Rpb25zIGNhbm5vdCBiZSBlbXB0eSIgaW4gcmVzdWx0CisKICAgICBkZWYgdGVzdF9lZGl0X25vbmV4aXN0ZW50X2ZpbGUoc2VsZiwgdGVtcF9kaXIpOgogICAgICAgICAiIiJUZXN0IGF0dGVtcHRpbmcgdG8gZWRpdCBhIG5vbmV4aXN0ZW50IGZpbGUuIiIiCiAgICAgICAgIG5vbl9leGlzdGVudF9maWxlID0gdGVtcF9kaXIgLyAiZG9lc19ub3RfZXhpc3QudHh0IgotICAgICAgICByZXN1bHQgPSB0b29sX2Z1bmN0aW9uKCJlZGl0Iiwgc3RyKG5vbl9leGlzdGVudF9maWxlKSwgZmlsZV90ZXh0PSJuZXcgY29udGVudCIpCisgICAgICAgIHJlc3VsdCA9IHRvb2xfZnVuY3Rpb24oImVkaXQiLCBzdHIobm9uX2V4aXN0ZW50X2ZpbGUpLCBlZGl0X3R5cGU9ImxpbmUiLCBlZGl0X2FjdGlvbnM9W10pCiAgICAgICAgIGFzc2VydCAiRXJyb3IiIGluIHJlc3VsdAogICAgICAgICBhc3NlcnQgImRvZXMgbm90IGV4aXN0IiBpbiByZXN1bHQKCkBAIC04Miw0ICsyNTksNCBAQCBjbGFzcyBUZXN0RWRpdG9yVG9vbDoKICAgICBkZWYgdGVzdF9pbnZhbGlkX2NvbW1hbmRzKHNlbGYsIGNvbW1hbmQsIHNhbXBsZV9maWxlKToKICAgICAgICAgIiIiVGVzdCB2YXJpb3VzIGludmFsaWQgY29tbWFuZHMuIiIiCiAgICAgICAgIHJlc3VsdCA9IHRvb2xfZnVuY3Rpb24oY29tbWFuZCwgc3RyKHNhbXBsZV9maWxlKSkKLSAgICAgICAgYXNzZXJ0ICJFcnJvciIgaW4gcmVzdWx0CisgICAgICAgIGFzc2VydCAiRXJyb3IiIGluIHJlc3VsdApcIE5vIG5ld2xpbmUgYXQgZW5kIG9mIGZpbGUKZGlmZiAtLWdpdCBhL3Rvb2xzL2VkaXQucHkgYi90b29scy9lZGl0LnB5CmluZGV4IDU5MTM3ZWUuLjk4MmVlODQgMTAwNjQ0Ci0tLSBhL3Rvb2xzL2VkaXQucHkKKysrIGIvdG9vbHMvZWRpdC5weQpAQCAtMSw1ICsxLDcgQEAKIGZyb20gcGF0aGxpYiBpbXBvcnQgUGF0aAogaW1wb3J0IHN1YnByb2Nlc3MKK2Zyb20gdHlwaW5nIGltcG9ydCBEaWN0LCBBbnksIExpc3QsIFVuaW9uLCBUdXBsZQorZnJvbSBkaWZmbGliIGltcG9ydCBTZXF1ZW5jZU1hdGNoZXIKCiBkZWYgdG9vbF9pbmZvKCk6CiAgICAgcmV0dXJuIHsKQEAgLTksOCArMTEsOSBAQCBkZWYgdG9vbF9pbmZvKCk6CiAqIElmIGBwYXRoYCBpcyBhIGZpbGUsIGB2aWV3YCBkaXNwbGF5cyB0aGUgZW50aXJlIGZpbGUgd2l0aCBsaW5lIG51bWJlcnMuIElmIGBwYXRoYCBpcyBhIGRpcmVjdG9yeSwgYHZpZXdgIGxpc3RzIG5vbi1oaWRkZW4gZmlsZXMgYW5kIGRpcmVjdG9yaWVzIHVwIHRvIDIgbGV2ZWxzIGRlZXAuXG4KICogVGhlIGBjcmVhdGVgIGNvbW1hbmQgY2Fubm90IGJlIHVzZWQgaWYgdGhlIHNwZWNpZmllZCBgcGF0aGAgYWxyZWFkeSBleGlzdHMgYXMgYSBmaWxlLlxuCiAqIElmIGEgYGNvbW1hbmRgIGdlbmVyYXRlcyBhIGxvbmcgb3V0cHV0LCBpdCB3aWxsIGJlIHRydW5jYXRlZCBhbmQgbWFya2VkIHdpdGggYDxyZXNwb25zZSBjbGlwcGVkPmAuXG4KLSogVGhlIGBlZGl0YCBjb21tYW5kIG92ZXJ3cml0ZXMgdGhlIGVudGlyZSBmaWxlIHdpdGggdGhlIHByb3ZpZGVkIGBmaWxlX3RleHRgLlxuCi0qIE5vIHBhcnRpYWwvbGluZS1yYW5nZSBlZGl0cyBvciBwYXJ0aWFsIHZpZXdpbmcgYXJlIHN1cHBvcnRlZC4iIiIsCisqIFRoZSBgZWRpdGAgY29tbWFuZCBzdXBwb3J0cyBib3RoIGVudGlyZSBmaWxlIG92ZXJ3cml0ZXMgYW5kIGZpbmUtZ3JhaW5lZCBsaW5lL3Rva2VuIGVkaXRpbmcgdmlhIHRoZSBgZWRpdF90eXBlYCBwYXJhbWV0ZXIuXG4KKyogTGluZS1iYXNlZCBlZGl0cyByZXF1aXJlIGxpbmUgbnVtYmVycyBhbmQgY29udGVudCB0byBtb2RpZnkgc3BlY2lmaWMgcGFydHMgb2YgYSBmaWxlLlxuCisqIFRva2VuLWJhc2VkIGVkaXRzIHJlcXVpcmUgc3BlY2lmeWluZyBvbGQgYW5kIG5ldyB0b2tlbnMgdG8gcmVwbGFjZSBzcGVjaWZpYyB0ZXh0IGZyYWdtZW50cy4iIiIsCiAgICAgICAgICJpbnB1dF9zY2hlbWEiOiB7CiAgICAgICAgICAgICAidHlwZSI6ICJvYmplY3QiLAogICAgICAgICAgICAgInByb3BlcnRpZXMiOiB7CkBAIC0yNCw4ICsyNywyOCBAQCBkZWYgdG9vbF9pbmZvKCk6CiAgICAgICAgICAgICAgICAgICAgICJ0eXBlIjogInN0cmluZyIKICAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICAgICAgICJmaWxlX3RleHQiOiB7Ci0gICAgICAgICAgICAgICAgICAgICJkZXNjcmlwdGlvbiI6ICJSZXF1aXJlZCBwYXJhbWV0ZXIgb2YgYGNyZWF0ZWAgb3IgYGVkaXRgIGNvbW1hbmQsIGNvbnRhaW5pbmcgdGhlIGNvbnRlbnQgZm9yIHRoZSBlbnRpcmUgZmlsZS4iLAorICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiUmVxdWlyZWQgcGFyYW1ldGVyIG9mIGBjcmVhdGVgIG9yIGBlZGl0YCBjb21tYW5kIHdpdGggZWRpdF90eXBlPSdmaWxlJywgY29udGFpbmluZyB0aGUgY29udGVudCBmb3IgdGhlIGVudGlyZSBmaWxlLiIsCiAgICAgICAgICAgICAgICAgICAgICJ0eXBlIjogInN0cmluZyIKKyAgICAgICAgICAgICAgICB9LAorICAgICAgICAgICAgICAgICJlZGl0X3R5cGUiOiB7CisgICAgICAgICAgICAgICAgICAgICJ0eXBlIjogInN0cmluZyIsCisgICAgICAgICAgICAgICAgICAgICJlbnVtIjogWyJmaWxlIiwgImxpbmUiLCAidG9rZW4iXSwKKyAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIlR5cGUgb2YgZWRpdCBvcGVyYXRpb246ICdmaWxlJyBmb3IgZnVsbCBmaWxlLCAnbGluZScgZm9yIGxpbmUtYmFzZWQgZWRpdHMsICd0b2tlbicgZm9yIHRva2VuLWJhc2VkIGVkaXRzLiIsCisgICAgICAgICAgICAgICAgICAgICJkZWZhdWx0IjogImZpbGUiCisgICAgICAgICAgICAgICAgfSwKKyAgICAgICAgICAgICAgICAiZWRpdF9hY3Rpb25zIjogeworICAgICAgICAgICAgICAgICAgICAidHlwZSI6ICJhcnJheSIsCisgICAgICAgICAgICAgICAgICAgICJkZXNjcmlwdGlvbiI6ICJMaXN0IG9mIGVkaXQgYWN0aW9ucyBmb3IgbGluZS90b2tlbiBvcGVyYXRpb25zLiBFYWNoIGFjdGlvbiBjb250YWlucyBvcGVyYXRpb24gZGV0YWlscy4iLAorICAgICAgICAgICAgICAgICAgICAiaXRlbXMiOiB7CisgICAgICAgICAgICAgICAgICAgICAgICAidHlwZSI6ICJvYmplY3QiLAorICAgICAgICAgICAgICAgICAgICAgICAgInByb3BlcnRpZXMiOiB7CisgICAgICAgICAgICAgICAgICAgICAgICAgICAgImFjdGlvbiI6IHsidHlwZSI6ICJzdHJpbmciLCAiZW51bSI6IFsiaW5zZXJ0IiwgImRlbGV0ZSIsICJyZXBsYWNlIl19LAorICAgICAgICAgICAgICAgICAgICAgICAgICAgICJsaW5lX251bWJlciI6IHsidHlwZSI6ICJpbnRlZ2VyIiwgImRlc2NyaXB0aW9uIjogIkxpbmUgbnVtYmVyIGZvciB0aGUgb3BlcmF0aW9uICgxLWJhc2VkKSJ9LAorICAgICAgICAgICAgICAgICAgICAgICAgICAgICJjb250ZW50IjogeyJ0eXBlIjogInN0cmluZyIsICJkZXNjcmlwdGlvbiI6ICJDb250ZW50IHRvIGluc2VydC9yZXBsYWNlIn0sCisgICAgICAgICAgICAgICAgICAgICAgICAgICAgIm9sZF90b2tlbiI6IHsidHlwZSI6ICJzdHJpbmciLCAiZGVzY3JpcHRpb24iOiAiVG9rZW4gdG8gYmUgcmVwbGFjZWQgKGZvciB0b2tlbiBlZGl0cykifSwKKyAgICAgICAgICAgICAgICAgICAgICAgICAgICAibmV3X3Rva2VuIjogeyJ0eXBlIjogInN0cmluZyIsICJkZXNjcmlwdGlvbiI6ICJOZXcgdG9rZW4gKGZvciB0b2tlbiBlZGl0cykifQorICAgICAgICAgICAgICAgICAgICAgICAgfQorICAgICAgICAgICAgICAgICAgICB9CiAgICAgICAgICAgICAgICAgfQogICAgICAgICAgICAgfSwKICAgICAgICAgICAgICJyZXF1aXJlZCI6IFsiY29tbWFuZCIsICJwYXRoIl0KQEAgLTExOSwxMiArMTQyLDEyNiBAQCBkZWYgdmlld19wYXRoKHBhdGhfb2JqOiBQYXRoKSAtPiBzdHI6CiAgICAgY29udGVudCA9IHJlYWRfZmlsZShwYXRoX29iaikKICAgICByZXR1cm4gZm9ybWF0X291dHB1dChjb250ZW50LCBzdHIocGF0aF9vYmopKQoKLWRlZiB0b29sX2Z1bmN0aW9uKGNvbW1hbmQ6IHN0ciwgcGF0aDogc3RyLCBmaWxlX3RleHQ6IHN0ciA9IE5vbmUpIC0+IHN0cjoKK2RlZiB2YWxpZGF0ZV9lZGl0X2FjdGlvbnMoYWN0aW9uczogTGlzdFtEaWN0W3N0ciwgQW55XV0sIGVkaXRfdHlwZTogc3RyKSAtPiBOb25lOgorICAgICIiIlZhbGlkYXRlIGVkaXQgYWN0aW9ucyBiYXNlZCBvbiBlZGl0IHR5cGUuIiIiCisgICAgaWYgbm90IGFjdGlvbnM6CisgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoIkVkaXQgYWN0aW9ucyBjYW5ub3QgYmUgZW1wdHkgZm9yIGxpbmUvdG9rZW4gZWRpdHMiKQorCisgICAgdmFsaWRfYWN0aW9ucyA9IFsiaW5zZXJ0IiwgImRlbGV0ZSIsICJyZXBsYWNlIl0KKyAgICByZXF1aXJlZF9maWVsZHMgPSB7CisgICAgICAgICJsaW5lIjogWyJhY3Rpb24iLCAibGluZV9udW1iZXIiXSwKKyAgICAgICAgInRva2VuIjogWyJhY3Rpb24iLCAib2xkX3Rva2VuIl0KKyAgICB9CisKKyAgICBmb3IgYWN0aW9uIGluIGFjdGlvbnM6CisgICAgICAgIGlmICJhY3Rpb24iIG5vdCBpbiBhY3Rpb24gb3IgYWN0aW9uWyJhY3Rpb24iXSBub3QgaW4gdmFsaWRfYWN0aW9uczoKKyAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJJbnZhbGlkIGFjdGlvbi4gTXVzdCBiZSBvbmUgb2Y6IHt2YWxpZF9hY3Rpb25zfSIpCisKKyAgICAgICAgIyBDaGVjayByZXF1aXJlZCBmaWVsZHMgYmFzZWQgb24gZWRpdF90eXBlCisgICAgICAgIGZvciBmaWVsZCBpbiByZXF1aXJlZF9maWVsZHNbZWRpdF90eXBlXToKKyAgICAgICAgICAgIGlmIGZpZWxkIG5vdCBpbiBhY3Rpb246CisgICAgICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIk1pc3NpbmcgcmVxdWlyZWQgZmllbGQgJ3tmaWVsZH0nIGluIGVkaXQgYWN0aW9uIikKKworICAgICAgICAjIFZhbGlkYXRlIGxpbmUgbnVtYmVyIGlmIHByb3ZpZGVkCisgICAgICAgIGlmICJsaW5lX251bWJlciIgaW4gYWN0aW9uOgorICAgICAgICAgICAgaWYgbm90IGlzaW5zdGFuY2UoYWN0aW9uWyJsaW5lX251bWJlciJdLCBpbnQpIG9yIGFjdGlvblsibGluZV9udW1iZXIiXSA8IDE6CisgICAgICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcigiTGluZSBudW1iZXIgbXVzdCBiZSBhIHBvc2l0aXZlIGludGVnZXIiKQorCisgICAgICAgICMgVmFsaWRhdGUgY29udGVudCByZXF1aXJlbWVudHMKKyAgICAgICAgaWYgYWN0aW9uWyJhY3Rpb24iXSBpbiBbImluc2VydCIsICJyZXBsYWNlIl06CisgICAgICAgICAgICBpZiBlZGl0X3R5cGUgPT0gImxpbmUiIGFuZCAiY29udGVudCIgbm90IGluIGFjdGlvbjoKKyAgICAgICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKCJDb250ZW50IHJlcXVpcmVkIGZvciBpbnNlcnQvcmVwbGFjZSBhY3Rpb25zIikKKyAgICAgICAgICAgIGlmIGVkaXRfdHlwZSA9PSAidG9rZW4iIGFuZCAibmV3X3Rva2VuIiBub3QgaW4gYWN0aW9uOgorICAgICAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoIm5ld190b2tlbiByZXF1aXJlZCBmb3IgdG9rZW4gb3BlcmF0aW9ucyIpCisKK2RlZiBhcHBseV9saW5lX2VkaXRzKGNvbnRlbnQ6IExpc3Rbc3RyXSwgYWN0aW9uczogTGlzdFtEaWN0W3N0ciwgQW55XV0pIC0+IExpc3Rbc3RyXToKKyAgICAiIiJBcHBseSBsaW5lLWJhc2VkIGVkaXRzIHRvIHRoZSBjb250ZW50LiIiIgorICAgIG1vZGlmaWVkX2NvbnRlbnQgPSBjb250ZW50LmNvcHkoKQorCisgICAgIyBTb3J0IGFjdGlvbnMgYnkgbGluZSBudW1iZXIgaW4gcmV2ZXJzZSBvcmRlciB0byBoYW5kbGUgaW5zZXJ0cy9kZWxldGVzIGNvcnJlY3RseQorICAgIHNvcnRlZF9hY3Rpb25zID0gc29ydGVkKGFjdGlvbnMsIGtleT1sYW1iZGEgeDogeFsibGluZV9udW1iZXIiXSwgcmV2ZXJzZT1UcnVlKQorCisgICAgZm9yIGFjdGlvbiBpbiBzb3J0ZWRfYWN0aW9uczoKKyAgICAgICAgbGluZV9udW0gPSBhY3Rpb25bImxpbmVfbnVtYmVyIl0gLSAxICAjIENvbnZlcnQgdG8gMC1iYXNlZCBpbmRleAorCisgICAgICAgIGlmIGxpbmVfbnVtID4gbGVuKG1vZGlmaWVkX2NvbnRlbnQpOgorICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIkxpbmUgbnVtYmVyIHthY3Rpb25bJ2xpbmVfbnVtYmVyJ119IGV4Y2VlZHMgZmlsZSBsZW5ndGgiKQorCisgICAgICAgIGlmIGFjdGlvblsiYWN0aW9uIl0gPT0gImRlbGV0ZSI6CisgICAgICAgICAgICBpZiBsaW5lX251bSA+PSAwOgorICAgICAgICAgICAgICAgIGRlbCBtb2RpZmllZF9jb250ZW50W2xpbmVfbnVtXQorICAgICAgICBlbGlmIGFjdGlvblsiYWN0aW9uIl0gPT0gImluc2VydCI6CisgICAgICAgICAgICBtb2RpZmllZF9jb250ZW50Lmluc2VydChsaW5lX251bSwgYWN0aW9uWyJjb250ZW50Il0pCisgICAgICAgIGVsaWYgYWN0aW9uWyJhY3Rpb24iXSA9PSAicmVwbGFjZSI6CisgICAgICAgICAgICBtb2RpZmllZF9jb250ZW50W2xpbmVfbnVtXSA9IGFjdGlvblsiY29udGVudCJdCisKKyAgICByZXR1cm4gbW9kaWZpZWRfY29udGVudAorCitkZWYgYXBwbHlfdG9rZW5fZWRpdHMoY29udGVudDogc3RyLCBhY3Rpb25zOiBMaXN0W0RpY3Rbc3RyLCBBbnldXSkgLT4gc3RyOgorICAgICIiIkFwcGx5IHRva2VuLWJhc2VkIGVkaXRzIHRvIHRoZSBjb250ZW50LiIiIgorICAgIG1vZGlmaWVkX2NvbnRlbnQgPSBjb250ZW50CisKKyAgICBmb3IgYWN0aW9uIGluIGFjdGlvbnM6CisgICAgICAgIG9sZF90b2tlbiA9IGFjdGlvblsib2xkX3Rva2VuIl0KKyAgICAgICAgaWYgYWN0aW9uWyJhY3Rpb24iXSA9PSAiZGVsZXRlIjoKKyAgICAgICAgICAgIG1vZGlmaWVkX2NvbnRlbnQgPSBtb2RpZmllZF9jb250ZW50LnJlcGxhY2Uob2xkX3Rva2VuLCAiIikKKyAgICAgICAgZWxpZiBhY3Rpb25bImFjdGlvbiJdIGluIFsiaW5zZXJ0IiwgInJlcGxhY2UiXToKKyAgICAgICAgICAgIG5ld190b2tlbiA9IGFjdGlvblsibmV3X3Rva2VuIl0KKyAgICAgICAgICAgIG1vZGlmaWVkX2NvbnRlbnQgPSBtb2RpZmllZF9jb250ZW50LnJlcGxhY2Uob2xkX3Rva2VuLCBuZXdfdG9rZW4pCisKKyAgICByZXR1cm4gbW9kaWZpZWRfY29udGVudAorCitkZWYgdmFsaWRhdGVfY29udGV4dChvcmlnaW5hbDogc3RyLCBtb2RpZmllZDogc3RyLCBjb250ZXh0X2xpbmVzOiBpbnQgPSAzKSAtPiBib29sOgogICAgICIiIgotICAgIE1haW4gdG9vbCBmdW5jdGlvbiB0aGF0IGhhbmRsZXM6CisgICAgVmFsaWRhdGUgdGhhdCB0aGUgY29udGV4dCBhcm91bmQgbW9kaWZpZWQgc2VjdGlvbnMgcmVtYWlucyBpbnRhY3QuCisgICAgUmV0dXJucyBUcnVlIGlmIGNvbnRleHQgaXMgdmFsaWQsIEZhbHNlIG90aGVyd2lzZS4KKyAgICAiIiIKKyAgICAjIFVzZSBTZXF1ZW5jZU1hdGNoZXIgdG8gZmluZCB0aGUgc2ltaWxhcml0eSByYXRpbyBiZXR3ZWVuIHN0cmluZ3MKKyAgICBzaW1pbGFyaXR5ID0gU2VxdWVuY2VNYXRjaGVyKE5vbmUsIG9yaWdpbmFsLCBtb2RpZmllZCkucmF0aW8oKQorCisgICAgIyBJZiBjb250ZW50IGlzIHRvbyBkaWZmZXJlbnQgKGxlc3MgdGhhbiAzMCUgc2ltaWxhciksIGNvbnNpZGVyIGl0IGludmFsaWQKKyAgICBpZiBzaW1pbGFyaXR5IDwgMC4zOgorICAgICAgICByZXR1cm4gRmFsc2UKKworICAgICMgU3BsaXQgaW50byBsaW5lcyBmb3IgbW9yZSBkZXRhaWxlZCBhbmFseXNpcworICAgIG9yaWdfbGluZXMgPSBvcmlnaW5hbC5zcGxpdGxpbmVzKCkKKyAgICBtb2RfbGluZXMgPSBtb2RpZmllZC5zcGxpdGxpbmVzKCkKKworICAgICMgSWYgbGluZSBjb3VudCBkaWZmZXJlbmNlIGlzIHRvbyBsYXJnZSAobW9yZSB0aGFuIDUwJSksIGNvbnNpZGVyIGl0IGludmFsaWQKKyAgICBpZiBhYnMobGVuKG9yaWdfbGluZXMpIC0gbGVuKG1vZF9saW5lcykpID4gbGVuKG9yaWdfbGluZXMpIC8vIDI6CisgICAgICAgIHJldHVybiBGYWxzZQorCisgICAgIyBDYWxjdWxhdGUgbGluZS1iYXNlZCBzaW1pbGFyaXR5IGZvciBzZWN0aW9ucworICAgIGRlZiBnZXRfYmxvY2tfc2ltaWxhcml0eShibG9jazE6IExpc3Rbc3RyXSwgYmxvY2syOiBMaXN0W3N0cl0pIC0+IGZsb2F0OgorICAgICAgICByZXR1cm4gU2VxdWVuY2VNYXRjaGVyKE5vbmUsICJcbiIuam9pbihibG9jazEpLCAiXG4iLmpvaW4oYmxvY2syKSkucmF0aW8oKQorCisgICAgIyBDaGVjayBzaW1pbGFyaXR5IG9mIHN0YXJ0IGFuZCBlbmQgYmxvY2tzIGlmIHRoZXkgZXhpc3QKKyAgICBpZiBsZW4ob3JpZ19saW5lcykgPj0gY29udGV4dF9saW5lcyBhbmQgbGVuKG1vZF9saW5lcykgPj0gY29udGV4dF9saW5lczoKKyAgICAgICAgc3RhcnRfc2ltaWxhcml0eSA9IGdldF9ibG9ja19zaW1pbGFyaXR5KAorICAgICAgICAgICAgb3JpZ19saW5lc1s6Y29udGV4dF9saW5lc10sCisgICAgICAgICAgICBtb2RfbGluZXNbOmNvbnRleHRfbGluZXNdCisgICAgICAgICkKKyAgICAgICAgZW5kX3NpbWlsYXJpdHkgPSBnZXRfYmxvY2tfc2ltaWxhcml0eSgKKyAgICAgICAgICAgIG9yaWdfbGluZXNbLWNvbnRleHRfbGluZXM6XSwKKyAgICAgICAgICAgIG1vZF9saW5lc1stY29udGV4dF9saW5lczpdCisgICAgICAgICkKKworICAgICAgICAjIElmIGVpdGhlciB0aGUgc3RhcnQgb3IgZW5kIGJsb2NrcyBhcmUgdG9vIGRpZmZlcmVudCwgY29uc2lkZXIgaXQgaW52YWxpZAorICAgICAgICBpZiBzdGFydF9zaW1pbGFyaXR5IDwgMC43IG9yIGVuZF9zaW1pbGFyaXR5IDwgMC43OgorICAgICAgICAgICAgcmV0dXJuIEZhbHNlCisKKyAgICByZXR1cm4gVHJ1ZQorCitkZWYgdG9vbF9mdW5jdGlvbihjb21tYW5kOiBzdHIsIHBhdGg6IHN0ciwgZmlsZV90ZXh0OiBzdHIgPSBOb25lLAorICAgICAgICAgICAgICAgICBlZGl0X3R5cGU6IHN0ciA9ICJmaWxlIiwgZWRpdF9hY3Rpb25zOiBMaXN0W0RpY3Rbc3RyLCBBbnldXSA9IE5vbmUpIC0+IHN0cjoKKyAgICAiIiIKKyAgICBFbmhhbmNlZCB0b29sIGZ1bmN0aW9uIHRoYXQgaGFuZGxlczoKICAgICAgIC0gJ3ZpZXcnICA6IFZpZXcgdGhlIGVudGlyZSBmaWxlIG9yIGRpcmVjdG9yeSBsaXN0aW5nCiAgICAgICAtICdjcmVhdGUnOiBDcmVhdGUgYSBuZXcgZmlsZSB3aXRoIHRoZSBnaXZlbiBmaWxlX3RleHQKLSAgICAgIC0gJ2VkaXQnICA6IE92ZXJ3cml0ZSBhbiBleGlzdGluZyBmaWxlIHdpdGggZmlsZV90ZXh0CisgICAgICAtICdlZGl0JyAgOiBFZGl0IGEgZmlsZSB1c2luZyBvbmUgb2YgdGhyZWUgbW9kZXM6CisgICAgICAgICAgICAgICAgICAtIGZpbGU6IG92ZXJ3cml0ZSBlbnRpcmUgZmlsZQorICAgICAgICAgICAgICAgICAgLSBsaW5lOiBsaW5lLWJhc2VkIGVkaXRzCisgICAgICAgICAgICAgICAgICAtIHRva2VuOiB0b2tlbi1iYXNlZCBlZGl0cwogICAgICIiIgogICAgIHRyeToKICAgICAgICAgcGF0aF9vYmogPSB2YWxpZGF0ZV9wYXRoKHBhdGgsIGNvbW1hbmQpCkBAIC0xMzksMTEgKzI3NiwzNiBAQCBkZWYgdG9vbF9mdW5jdGlvbihjb21tYW5kOiBzdHIsIHBhdGg6IHN0ciwgZmlsZV90ZXh0OiBzdHIgPSBOb25lKSAtPiBzdHI6CiAgICAgICAgICAgICByZXR1cm4gZiJGaWxlIGNyZWF0ZWQgc3VjY2Vzc2Z1bGx5IGF0OiB7cGF0aH0iCgogICAgICAgICBlbGlmIGNvbW1hbmQgPT0gImVkaXQiOgotICAgICAgICAgICAgaWYgZmlsZV90ZXh0IGlzIE5vbmU6Ci0gICAgICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcigiTWlzc2luZyByZXF1aXJlZCBgZmlsZV90ZXh0YCBmb3IgJ2VkaXQnIGNvbW1hbmQuIikKLSAgICAgICAgICAgIHdyaXRlX2ZpbGUocGF0aF9vYmosIGZpbGVfdGV4dCkKLSAgICAgICAgICAgIHJldHVybiBmIkZpbGUgYXQge3BhdGh9IGhhcyBiZWVuIG92ZXJ3cml0dGVuIHdpdGggbmV3IGNvbnRlbnQuIgorICAgICAgICAgICAgIyBSZWFkIG9yaWdpbmFsIGNvbnRlbnQgZm9yIGxpbmUvdG9rZW4gZWRpdHMgYW5kIHZhbGlkYXRpb24KKyAgICAgICAgICAgIG9yaWdpbmFsX2NvbnRlbnQgPSByZWFkX2ZpbGUocGF0aF9vYmopIGlmIGVkaXRfdHlwZSBpbiBbImxpbmUiLCAidG9rZW4iXSBlbHNlIE5vbmUKKworICAgICAgICAgICAgaWYgZWRpdF90eXBlID09ICJmaWxlIjoKKyAgICAgICAgICAgICAgICBpZiBmaWxlX3RleHQgaXMgTm9uZToKKyAgICAgICAgICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcigiTWlzc2luZyByZXF1aXJlZCBgZmlsZV90ZXh0YCBmb3IgJ2ZpbGUnIGVkaXQgdHlwZS4iKQorICAgICAgICAgICAgICAgIHdyaXRlX2ZpbGUocGF0aF9vYmosIGZpbGVfdGV4dCkKKyAgICAgICAgICAgICAgICByZXR1cm4gZiJGaWxlIGF0IHtwYXRofSBoYXMgYmVlbiBvdmVyd3JpdHRlbiB3aXRoIG5ldyBjb250ZW50LiIKKworICAgICAgICAgICAgZWxpZiBlZGl0X3R5cGUgaW4gWyJsaW5lIiwgInRva2VuIl06CisgICAgICAgICAgICAgICAgaWYgbm90IGVkaXRfYWN0aW9uczoKKyAgICAgICAgICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcigiRWRpdCBhY3Rpb25zIGNhbm5vdCBiZSBlbXB0eSBmb3IgbGluZS90b2tlbiBlZGl0cyIpCisKKyAgICAgICAgICAgICAgICB2YWxpZGF0ZV9lZGl0X2FjdGlvbnMoZWRpdF9hY3Rpb25zLCBlZGl0X3R5cGUpCisKKyAgICAgICAgICAgICAgICBpZiBlZGl0X3R5cGUgPT0gImxpbmUiOgorICAgICAgICAgICAgICAgICAgICBsaW5lcyA9IG9yaWdpbmFsX2NvbnRlbnQuc3BsaXRsaW5lcygpCisgICAgICAgICAgICAgICAgICAgIG1vZGlmaWVkX2xpbmVzID0gYXBwbHlfbGluZV9lZGl0cyhsaW5lcywgZWRpdF9hY3Rpb25zKQorICAgICAgICAgICAgICAgICAgICBtb2RpZmllZF9jb250ZW50ID0gIlxuIi5qb2luKG1vZGlmaWVkX2xpbmVzKQorICAgICAgICAgICAgICAgIGVsc2U6ICAjIHRva2VuIGVkaXRzCisgICAgICAgICAgICAgICAgICAgIG1vZGlmaWVkX2NvbnRlbnQgPSBhcHBseV90b2tlbl9lZGl0cyhvcmlnaW5hbF9jb250ZW50LCBlZGl0X2FjdGlvbnMpCgorICAgICAgICAgICAgICAgICMgVmFsaWRhdGUgY29udGV4dCBiZWZvcmUgd3JpdGluZworICAgICAgICAgICAgICAgIGlmIHZhbGlkYXRlX2NvbnRleHQob3JpZ2luYWxfY29udGVudCwgbW9kaWZpZWRfY29udGVudCk6CisgICAgICAgICAgICAgICAgICAgIHdyaXRlX2ZpbGUocGF0aF9vYmosIG1vZGlmaWVkX2NvbnRlbnQpCisgICAgICAgICAgICAgICAgICAgIHJldHVybiBmIkZpbGUgYXQge3BhdGh9IGhhcyBiZWVuIHN1Y2Nlc3NmdWxseSBlZGl0ZWQgdXNpbmcge2VkaXRfdHlwZX0tYmFzZWQgZWRpdGluZy4iCisgICAgICAgICAgICAgICAgZWxzZToKKyAgICAgICAgICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcigiQ29udGV4dCB2YWxpZGF0aW9uIGZhaWxlZC4gRWRpdCBvcGVyYXRpb24gYWJvcnRlZC4iKQorICAgICAgICAgICAgZWxzZToKKyAgICAgICAgICAgICAgICByYWlzZSBWYWx1ZUVycm9yKGYiSW52YWxpZCBlZGl0X3R5cGU6IHtlZGl0X3R5cGV9IikKICAgICAgICAgZWxzZToKICAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJVbmtub3duIGNvbW1hbmQ6IHtjb21tYW5kfSIpCgpAQCAtMTUyLDQgKzMxNCw0IEBAIGRlZiB0b29sX2Z1bmN0aW9uKGNvbW1hbmQ6IHN0ciwgcGF0aDogc3RyLCBmaWxlX3RleHQ6IHN0ciA9IE5vbmUpIC0+IHN0cjoKCiBpZiBfX25hbWVfXyA9PSAiX19tYWluX18iOgogICAgICMgRXhhbXBsZSB1c2FnZQotICAgIHByaW50KHRvb2xfZnVuY3Rpb24oInZpZXciLCAiL2hvbWUvdWJ1bnR1L3h4L2RnbS9jb2RpbmdfYWdlbnQucHkiKSkKKyAgICBwcmludCh0b29sX2Z1bmN0aW9uKCJ2aWV3IiwgIi9ob21lL3VidW50dS94eC9kZ20vY29kaW5nX2FnZW50LnB5IikpClwgTm8gbmV3bGluZSBhdCBlbmQgb2YgZmlsZQ==)
diff --git a/tests/test_edit_tool.py b/tests/test_edit_tool.py
index f0782c6..d3a4d5c 100644
--- a/tests/test_edit_tool.py
+++ b/tests/test_edit_tool.py
@@ -1,7 +1,7 @@
import pytest
from pathlib import Path
import tempfile
-from tools.edit import tool_function
+from tools.edit import tool_function, validate_edit_actions, validate_context
@pytest.fixture
def temp_dir():
@@ -17,6 +17,18 @@ def sample_file(temp_dir):
file_path.write_text(content)
return file_path
+@pytest.fixture
+def code_file(temp_dir):
+ """Create a sample Python file for testing token-based edits."""
+ file_path = temp_dir / "test.py"
+ content = """def test_function():
+ x = 42
+ y = "old_value"
+ return x + len(y)
+"""
+ file_path.write_text(content)
+ return file_path
+
class TestEditorTool:
def test_view_file(self, sample_file):
"""Test viewing entire file content."""
@@ -39,17 +51,182 @@ class TestEditorTool:
assert "Error" in result
assert "already exists" in result
- def test_edit_file(self, sample_file):
- """Test editing an existing file."""
+ def test_edit_file_full(self, sample_file):
+ """Test editing an existing file with file mode."""
new_content = "edited content\nnew line"
- result = tool_function("edit", str(sample_file), file_text=new_content)
+ result = tool_function(
+ "edit",
+ str(sample_file),
+ file_text=new_content,
+ edit_type="file"
+ )
assert "has been overwritten" in result
assert sample_file.read_text() == new_content
+ def test_line_based_edit_insert(self, sample_file):
+ """Test line-based insert operation."""
+ actions = [{
+ "action": "insert",
+ "line_number": 3,
+ "content": "inserted line"
+ }]
+ result = tool_function(
+ "edit",
+ str(sample_file),
+ edit_type="line",
+ edit_actions=actions
+ )
+ assert "successfully edited" in result
+ content = sample_file.read_text().splitlines()
+ assert content[2] == "inserted line"
+ assert len(content) == 6
+
+ def test_line_based_edit_delete(self, sample_file):
+ """Test line-based delete operation."""
+ actions = [{
+ "action": "delete",
+ "line_number": 2
+ }]
+ result = tool_function(
+ "edit",
+ str(sample_file),
+ edit_type="line",
+ edit_actions=actions
+ )
+ assert "successfully edited" in result
+ content = sample_file.read_text().splitlines()
+ assert "line 2" not in content
+ assert len(content) == 4
+
+ def test_line_based_edit_replace(self, sample_file):
+ """Test line-based replace operation."""
+ actions = [{
+ "action": "replace",
+ "line_number": 3,
+ "content": "replaced line"
+ }]
+ result = tool_function(
+ "edit",
+ str(sample_file),
+ edit_type="line",
+ edit_actions=actions
+ )
+ assert "successfully edited" in result
+ content = sample_file.read_text().splitlines()
+ assert content[2] == "replaced line"
+ assert len(content) == 5
+
+ def test_token_based_edit(self, code_file):
+ """Test token-based edit operation."""
+ actions = [{
+ "action": "replace",
+ "old_token": "old_value",
+ "new_token": "new_value"
+ }]
+ result = tool_function(
+ "edit",
+ str(code_file),
+ edit_type="token",
+ edit_actions=actions
+ )
+ assert "successfully edited" in result
+ content = code_file.read_text()
+ assert "old_value" not in content
+ assert "new_value" in content
+
+ def test_multiple_token_edits(self, code_file):
+ """Test multiple token-based edit operations."""
+ actions = [
+ {
+ "action": "replace",
+ "old_token": "42",
+ "new_token": "100"
+ },
+ {
+ "action": "replace",
+ "old_token": "old_value",
+ "new_token": "new_text"
+ }
+ ]
+ result = tool_function(
+ "edit",
+ str(code_file),
+ edit_type="token",
+ edit_actions=actions
+ )
+ assert "successfully edited" in result
+ content = code_file.read_text()
+ assert "42" not in content
+ assert "100" in content
+ assert "old_value" not in content
+ assert "new_text" in content
+
+ def test_invalid_line_number(self, sample_file):
+ """Test edit with invalid line number."""
+ actions = [{
+ "action": "replace",
+ "line_number": 100,
+ "content": "invalid line"
+ }]
+ result = tool_function(
+ "edit",
+ str(sample_file),
+ edit_type="line",
+ edit_actions=actions
+ )
+ assert "Error" in result
+ assert "exceeds file length" in result
+
+ def test_invalid_edit_type(self, sample_file):
+ """Test edit with invalid edit type."""
+ result = tool_function(
+ "edit",
+ str(sample_file),
+ edit_type="invalid",
+ edit_actions=[{"action": "replace"}]
+ )
+ assert "Error" in result
+ assert "Invalid edit_type" in result
+
+ def test_missing_required_fields(self, sample_file):
+ """Test edit with missing required fields."""
+ actions = [{
+ "action": "replace" # Missing line_number and content
+ }]
+ result = tool_function(
+ "edit",
+ str(sample_file),
+ edit_type="line",
+ edit_actions=actions
+ )
+ assert "Error" in result
+ assert "Missing required field" in result
+
+ def test_validate_context(self):
+ """Test context validation function."""
+ original = "line 1\nline 2\nline 3\nline 4\nline 5"
+ modified = "line 1\nline 2\nmodified\nline 4\nline 5"
+ assert validate_context(original, modified) is True
+
+ # Test invalid context (too many changes)
+ modified = "completely\ndifferent\ncontent"
+ assert validate_context(original, modified) is False
+
+ def test_empty_edit_actions(self, sample_file):
+ """Test edit with empty edit actions."""
+ result = tool_function(
+ "edit",
+ str(sample_file),
+ edit_type="line",
+ edit_actions=[]
+ )
+ assert "Error" in result
+ assert "Edit actions cannot be empty" in result
+
def test_edit_nonexistent_file(self, temp_dir):
"""Test attempting to edit a nonexistent file."""
non_existent_file = temp_dir / "does_not_exist.txt"
- result = tool_function("edit", str(non_existent_file), file_text="new content")
+ result = tool_function("edit", str(non_existent_file), edit_type="line", edit_actions=[])
assert "Error" in result
assert "does not exist" in result
@@ -82,4 +259,4 @@ class TestEditorTool:
def test_invalid_commands(self, command, sample_file):
"""Test various invalid commands."""
result = tool_function(command, str(sample_file))
- assert "Error" in result
+ assert "Error" in result
\ No newline at end of file
diff --git a/tools/edit.py b/tools/edit.py
index 59137ee..982ee84 100644
--- a/tools/edit.py
+++ b/tools/edit.py
@@ -1,5 +1,7 @@
from pathlib import Path
import subprocess
+from typing import Dict, Any, List, Union, Tuple
+from difflib import SequenceMatcher
def tool_info():
return {
@@ -9,8 +11,9 @@ def tool_info():
* If ‘path‘ is a file, ‘view‘ displays the entire file with line numbers. If ‘path‘ is a directory, ‘view‘ lists non-hidden files and directories up to 2 levels deep.\n
* The ‘create‘ command cannot be used if the specified ‘path‘ already exists as a file.\n
* If a ‘command‘ generates a long output, it will be truncated and marked with ‘<response clipped>‘.\n
-* The ‘edit‘ command overwrites the entire file with the provided ‘file_text‘.\n
-* No partial/line-range edits or partial viewing are supported.""",
+* The ‘edit‘ command supports both entire file overwrites and fine-grained line/token editing via the ‘edit_type‘ parameter.\n
+* Line-based edits require line numbers and content to modify specific parts of a file.\n
+* Token-based edits require specifying old and new tokens to replace specific text fragments.""",
"input_schema": {
"type": "object",
"properties": {
@@ -24,8 +27,28 @@ def tool_info():
"type": "string"
},
"file_text": {
- "description": "Required parameter of ‘create‘ or ‘edit‘ command, containing the content for the entire file.",
+ "description": "Required parameter of ‘create‘ or ‘edit‘ command with edit_type=’file’, containing the content for the entire file.",
"type": "string"
+ },
+ "edit_type": {
+ "type": "string",
+ "enum": ["file", "line", "token"],
+ "description": "Type of edit operation: ’file’ for full file, ’line’ for line-based edits, ’token’ for token-based edits.",
+ "default": "file"
+ },
+ "edit_actions": {
+ "type": "array",
+ "description": "List of edit actions for line/token operations. Each action contains operation details.",
+ "items": {
+ "type": "object",
+ "properties": {
+ "action": {"type": "string", "enum": ["insert", "delete", "replace"]},
+ "line_number": {"type": "integer", "description": "Line number for the operation (1-based)"},
+ "content": {"type": "string", "description": "Content to insert/replace"},
+ "old_token": {"type": "string", "description": "Token to be replaced (for token edits)"},
+ "new_token": {"type": "string", "description": "New token (for token edits)"}
+ }
+ }
}
},
"required": ["command", "path"]
@@ -119,12 +142,126 @@ def view_path(path_obj: Path) -> str:
content = read_file(path_obj)
return format_output(content, str(path_obj))
-def tool_function(command: str, path: str, file_text: str = None) -> str:
+def validate_edit_actions(actions: List[Dict[str, Any]], edit_type: str) -> None:
+ """Validate edit actions based on edit type."""
+ if not actions:
+ raise ValueError("Edit actions cannot be empty for line/token edits")
+
+ valid_actions = ["insert", "delete", "replace"]
+ required_fields = {
+ "line": ["action", "line_number"],
+ "token": ["action", "old_token"]
+ }
+
+ for action in actions:
+ if "action" not in action or action["action"] not in valid_actions:
+ raise ValueError(f"Invalid action. Must be one of: {valid_actions}")
+
+ # Check required fields based on edit_type
+ for field in required_fields[edit_type]:
+ if field not in action:
+ raise ValueError(f"Missing required field ’{field}’ in edit action")
+
+ # Validate line number if provided
+ if "line_number" in action:
+ if not isinstance(action["line_number"], int) or action["line_number"] < 1:
+ raise ValueError("Line number must be a positive integer")
+
+ # Validate content requirements
+ if action["action"] in ["insert", "replace"]:
+ if edit_type == "line" and "content" not in action:
+ raise ValueError("Content required for insert/replace actions")
+ if edit_type == "token" and "new_token" not in action:
+ raise ValueError("new_token required for token operations")
+
+def apply_line_edits(content: List[str], actions: List[Dict[str, Any]]) -> List[str]:
+ """Apply line-based edits to the content."""
+ modified_content = content.copy()
+
+ # Sort actions by line number in reverse order to handle inserts/deletes correctly
+ sorted_actions = sorted(actions, key=lambda x: x["line_number"], reverse=True)
+
+ for action in sorted_actions:
+ line_num = action["line_number"] - 1 # Convert to 0-based index
+
+ if line_num > len(modified_content):
+ raise ValueError(f"Line number {action[’line_number’]} exceeds file length")
+
+ if action["action"] == "delete":
+ if line_num >= 0:
+ del modified_content[line_num]
+ elif action["action"] == "insert":
+ modified_content.insert(line_num, action["content"])
+ elif action["action"] == "replace":
+ modified_content[line_num] = action["content"]
+
+ return modified_content
+
+def apply_token_edits(content: str, actions: List[Dict[str, Any]]) -> str:
+ """Apply token-based edits to the content."""
+ modified_content = content
+
+ for action in actions:
+ old_token = action["old_token"]
+ if action["action"] == "delete":
+ modified_content = modified_content.replace(old_token, "")
+ elif action["action"] in ["insert", "replace"]:
+ new_token = action["new_token"]
+ modified_content = modified_content.replace(old_token, new_token)
+
+ return modified_content
+
+def validate_context(original: str, modified: str, context_lines: int = 3) -> bool:
"""
- Main tool function that handles:
+ Validate that the context around modified sections remains intact.
+ Returns True if context is valid, False otherwise.
+ """
+ # Use SequenceMatcher to find the similarity ratio between strings
+ similarity = SequenceMatcher(None, original, modified).ratio()
+
+ # If content is too different (less than 30% similar), consider it invalid
+ if similarity < 0.3:
+ return False
+
+ # Split into lines for more detailed analysis
+ orig_lines = original.splitlines()
+ mod_lines = modified.splitlines()
+
+ # If line count difference is too large (more than 50%), consider it invalid
+ if abs(len(orig_lines) - len(mod_lines)) > len(orig_lines) // 2:
+ return False
+
+ # Calculate line-based similarity for sections
+ def get_block_similarity(block1: List[str], block2: List[str]) -> float:
+ return SequenceMatcher(None, "\n".join(block1), "\n".join(block2)).ratio()
+
+ # Check similarity of start and end blocks if they exist
+ if len(orig_lines) >= context_lines and len(mod_lines) >= context_lines:
+ start_similarity = get_block_similarity(
+ orig_lines[:context_lines],
+ mod_lines[:context_lines]
+ )
+ end_similarity = get_block_similarity(
+ orig_lines[-context_lines:],
+ mod_lines[-context_lines:]
+ )
+
+ # If either the start or end blocks are too different, consider it invalid
+ if start_similarity < 0.7 or end_similarity < 0.7:
+ return False
+
+ return True
+
+def tool_function(command: str, path: str, file_text: str = None,
+ edit_type: str = "file", edit_actions: List[Dict[str, Any]] = None) -> str:
+ """
+ Enhanced tool function that handles:
- ’view’ : View the entire file or directory listing
- ’create’: Create a new file with the given file_text
- - ’edit’ : Overwrite an existing file with file_text
+ - ’edit’ : Edit a file using one of three modes:
+ - file: overwrite entire file
+ - line: line-based edits
+ - token: token-based edits
"""
try:
path_obj = validate_path(path, command)
@@ -139,11 +276,36 @@ def tool_function(command: str, path: str, file_text: str = None) -> str:
return f"File created successfully at: {path}"
elif command == "edit":
- if file_text is None:
- raise ValueError("Missing required ‘file_text‘ for ’edit’ command.")
- write_file(path_obj, file_text)
- return f"File at {path} has been overwritten with new content."
+ # Read original content for line/token edits and validation
+ original_content = read_file(path_obj) if edit_type in ["line", "token"] else None
+
+ if edit_type == "file":
+ if file_text is None:
+ raise ValueError("Missing required ‘file_text‘ for ’file’ edit type.")
+ write_file(path_obj, file_text)
+ return f"File at {path} has been overwritten with new content."
+
+ elif edit_type in ["line", "token"]:
+ if not edit_actions:
+ raise ValueError("Edit actions cannot be empty for line/token edits")
+
+ validate_edit_actions(edit_actions, edit_type)
+
+ if edit_type == "line":
+ lines = original_content.splitlines()
+ modified_lines = apply_line_edits(lines, edit_actions)
+ modified_content = "\n".join(modified_lines)
+ else: # token edits
+ modified_content = apply_token_edits(original_content, edit_actions)
+ # Validate context before writing
+ if validate_context(original_content, modified_content):
+ write_file(path_obj, modified_content)
+ return f"File at {path} has been successfully edited using {edit_type}-based editing."
+ else:
+ raise ValueError("Context validation failed. Edit operation aborted.")
+ else:
+ raise ValueError(f"Invalid edit_type: {edit_type}")
else:
raise ValueError(f"Unknown command: {command}")
@@ -152,4 +314,4 @@ def tool_function(command: str, path: str, file_text: str = None) -> str:
if __name__ == "__main__":
# Example usage
- print(tool_function("view", "/home/ubuntu/xx/dgm/coding_agent.py"))
+ print(tool_function("view", "/home/ubuntu/xx/dgm/coding_agent.py"))
\ No newline at end of file+
```

产生节点 24 的建议功能实现：

```diff
[⬇](data:text/plain;base64,ZGlmZiAtLWdpdCBhL3Rvb2xzL2VkaXQucHkgYi90b29scy9lZGl0LnB5CmluZGV4IDE2YWU1MjEuLjc1N2Y1YzIgMTAwNjQ0Ci0tLSBhL3Rvb2xzL2VkaXQucHkKKysrIGIvdG9vbHMvZWRpdC5weQpAQCAtMTEsMjEgKzExLDIxIEBAIGRlZiB0b29sX2luZm8oKToKICogSWYgYHBhdGhgIGlzIGEgZGlyZWN0b3J5LCBgdmlld2AgbGlzdHMgbm9uLWhpZGRlbiBmaWxlcyBhbmQgZGlyZWN0b3JpZXMgdXAgdG8gMiBsZXZlbHMgZGVlcC5cbgogKiBUaGUgYGNyZWF0ZWAgY29tbWFuZCBjYW5ub3QgYmUgdXNlZCBpZiB0aGUgc3BlY2lmaWVkIGBwYXRoYCBhbHJlYWR5IGV4aXN0cyBhcyBhIGZpbGUuXG4KICogSWYgYSBgY29tbWFuZGAgZ2VuZXJhdGVzIGEgbG9uZyBvdXRwdXQsIGl0IHdpbGwgYmUgdHJ1bmNhdGVkIGFuZCBtYXJrZWQgd2l0aCBgPHJlc3BvbnNlIGNsaXBwZWQ+YC5cbgotKiBUaGUgYGVkaXRgIGNvbW1hbmQgb3ZlcndyaXRlcyB0aGUgZW50aXJlIGZpbGUgd2l0aCB0aGUgcHJvdmlkZWQgYGZpbGVfdGV4dGAuIiIiLAorKiBUaGUgYHN0cl9yZXBsYWNlYCBjb21tYW5kIHJlcGxhY2VzIGEgdW5pcXVlIG9jY3VycmVuY2Ugb2Ygb2xkX3N0ciB3aXRoIG5ld19zdHIsIGZhaWxpbmcgaWYgb2xkX3N0ciBpcyBub3QgZm91bmQgb3IgYXBwZWFycyBtdWx0aXBsZSB0aW1lcy4iIiIsCiAgICAgICAgICJpbnB1dF9zY2hlbWEiOiB7CiAgICAgICAgICAgICAidHlwZSI6ICJvYmplY3QiLAogICAgICAgICAgICAgInByb3BlcnRpZXMiOiB7CiAgICAgICAgICAgICAgICAgImNvbW1hbmQiOiB7CiAgICAgICAgICAgICAgICAgICAgICJ0eXBlIjogInN0cmluZyIsCi0gICAgICAgICAgICAgICAgICAgICJlbnVtIjogWyJ2aWV3IiwgImNyZWF0ZSIsICJlZGl0Il0sCi0gICAgICAgICAgICAgICAgICAgICJkZXNjcmlwdGlvbiI6ICJUaGUgY29tbWFuZCB0byBydW46IGB2aWV3YCwgYGNyZWF0ZWAsIG9yIGBlZGl0YC4iCisgICAgICAgICAgICAgICAgICAgICJlbnVtIjogWyJ2aWV3IiwgImNyZWF0ZSIsICJzdHJfcmVwbGFjZSJdLAorICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiVGhlIGNvbW1hbmQgdG8gcnVuOiBgdmlld2AsIGBjcmVhdGVgLCBvciBgc3RyX3JlcGxhY2VgLiIKICAgICAgICAgICAgICAgICB9LAogICAgICAgICAgICAgICAgICJwYXRoIjogewogICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiQWJzb2x1dGUgcGF0aCB0byBmaWxlIG9yIGRpcmVjdG9yeSwgZS5nLiBgL3JlcG8vZmlsZS5weWAgb3IgYC9yZXBvYC4iLAogICAgICAgICAgICAgICAgICAgICAidHlwZSI6ICJzdHJpbmciCiAgICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgICAgICAiZmlsZV90ZXh0IjogewotICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiUmVxdWlyZWQgcGFyYW1ldGVyIG9mIGBjcmVhdGVgIG9yIGBlZGl0YCBjb21tYW5kLCBjb250YWluaW5nIHRoZSBjb250ZW50IGZvciB0aGUgZW50aXJlIGZpbGUuIiwKKyAgICAgICAgICAgICAgICAgICAgImRlc2NyaXB0aW9uIjogIlJlcXVpcmVkIHBhcmFtZXRlciBvZiBgY3JlYXRlYCBjb21tYW5kLCBjb250YWluaW5nIHRoZSBjb250ZW50IGZvciB0aGUgZW50aXJlIGZpbGUuIiwKICAgICAgICAgICAgICAgICAgICAgInR5cGUiOiAic3RyaW5nIgogICAgICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICAgICAgInZpZXdfcmFuZ2UiOiB7CkBAIC0zNCw2ICszNCwxNCBAQCBkZWYgdG9vbF9pbmZvKCk6CiAgICAgICAgICAgICAgICAgICAgICJpdGVtcyI6IHsidHlwZSI6ICJpbnRlZ2VyIn0sCiAgICAgICAgICAgICAgICAgICAgICJtaW5JdGVtcyI6IDIsCiAgICAgICAgICAgICAgICAgICAgICJtYXhJdGVtcyI6IDIKKyAgICAgICAgICAgICAgICB9LAorICAgICAgICAgICAgICAgICJvbGRfc3RyIjogeworICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiUmVxdWlyZWQgcGFyYW1ldGVyIG9mIGBzdHJfcmVwbGFjZWAgY29tbWFuZCwgY29udGFpbmluZyB0aGUgZXhhY3QgdGV4dCB0byBmaW5kIGFuZCByZXBsYWNlLiIsCisgICAgICAgICAgICAgICAgICAgICJ0eXBlIjogInN0cmluZyIKKyAgICAgICAgICAgICAgICB9LAorICAgICAgICAgICAgICAgICJuZXdfc3RyIjogeworICAgICAgICAgICAgICAgICAgICAiZGVzY3JpcHRpb24iOiAiUmVxdWlyZWQgcGFyYW1ldGVyIG9mIGBzdHJfcmVwbGFjZWAgY29tbWFuZCwgY29udGFpbmluZyB0aGUgbmV3IHRleHQgdG8gcmVwbGFjZSBvbGRfc3RyIHdpdGguIiwKKyAgICAgICAgICAgICAgICAgICAgInR5cGUiOiAic3RyaW5nIgogICAgICAgICAgICAgICAgIH0KICAgICAgICAgICAgIH0sCiAgICAgICAgICAgICAicmVxdWlyZWQiOiBbImNvbW1hbmQiLCAicGF0aCJdCkBAIC01MSw3ICs1OSw3IEBAIGRlZiB2YWxpZGF0ZV9wYXRoKHBhdGg6IHN0ciwgY29tbWFuZDogc3RyKSAtPiBQYXRoOgogICAgIFZhbGlkYXRlIHRoZSBmaWxlIHBhdGggZm9yIGVhY2ggY29tbWFuZDoKICAgICAgIC0gJ3ZpZXcnOiBwYXRoIG1heSBiZSBhIGZpbGUgb3IgZGlyZWN0b3J5OyBtdXN0IGV4aXN0LgogICAgICAgLSAnY3JlYXRlJzogcGF0aCBtdXN0IG5vdCBleGlzdCAoZm9yIG5ldyBmaWxlIGNyZWF0aW9uKS4KLSAgICAgIC0gJ2VkaXQnOiBwYXRoIG11c3QgZXhpc3QgKGZvciBvdmVyd3JpdGluZykuCisgICAgICAtICdzdHJfcmVwbGFjZSc6IHBhdGggbXVzdCBleGlzdCBhbmQgYmUgYSBmaWxlLgogICAgICIiIgogICAgIHBhdGhfb2JqID0gUGF0aChwYXRoKQoKQEAgLTY5LDcgKzc3LDcgQEAgZGVmIHZhbGlkYXRlX3BhdGgocGF0aDogc3RyLCBjb21tYW5kOiBzdHIpIC0+IFBhdGg6CiAgICAgICAgICMgUGF0aCBtdXN0IG5vdCBleGlzdAogICAgICAgICBpZiBwYXRoX29iai5leGlzdHMoKToKICAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoZiJDYW5ub3QgY3JlYXRlIG5ldyBmaWxlOyB7cGF0aH0gYWxyZWFkeSBleGlzdHMuIikKLSAgICBlbGlmIGNvbW1hbmQgPT0gImVkaXQiOgorICAgIGVsaWYgY29tbWFuZCA9PSAic3RyX3JlcGxhY2UiOgogICAgICAgICAjIFBhdGggbXVzdCBleGlzdCBhbmQgbXVzdCBiZSBhIGZpbGUKICAgICAgICAgaWYgbm90IHBhdGhfb2JqLmV4aXN0cygpOgogICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIlRoZSBmaWxlIHtwYXRofSBkb2VzIG5vdCBleGlzdC4iKQpAQCAtMTQ0LDYgKzE1MiwyOCBAQCBkZWYgd3JpdGVfZmlsZShwYXRoOiBQYXRoLCBjb250ZW50OiBzdHIpOgogICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIkZhaWxlZCB0byB3cml0ZSBmaWxlOiB7ZX0iKQoKK2RlZiBzdHJfcmVwbGFjZV9pbl9maWxlKHBhdGg6IFBhdGgsIG9sZF9zdHI6IHN0ciwgbmV3X3N0cjogc3RyKSAtPiBzdHI6CisgICAgIiIiCisgICAgUmVwbGFjZSBhbiBleGFjdCBvY2N1cnJlbmNlIG9mIG9sZF9zdHIgd2l0aCBuZXdfc3RyIGluIHRoZSBmaWxlLgorICAgIE9ubHkgcGVyZm9ybXMgdGhlIHJlcGxhY2VtZW50IGlmIG9sZF9zdHIgb2NjdXJzIGV4YWN0bHkgb25jZS4KKyAgICBSZXR1cm5zIGEgbWVzc2FnZSBpbmRpY2F0aW5nIHN1Y2Nlc3Mgb3IgZmFpbHVyZS4KKyAgICAiIiIKKyAgICB0cnk6CisgICAgICAgIGNvbnRlbnQgPSByZWFkX2ZpbGUocGF0aCkKKyAgICAgICAgb2NjdXJyZW5jZXMgPSBjb250ZW50LmNvdW50KG9sZF9zdHIpCisKKyAgICAgICAgaWYgb2NjdXJyZW5jZXMgPT0gMDoKKyAgICAgICAgICAgIHJldHVybiBmIkVycm9yOiBDb3VsZCBub3QgZmluZCB0aGUgZXhhY3QgdGV4dCB0byByZXBsYWNlIGluIHtwYXRofSIKKyAgICAgICAgZWxpZiBvY2N1cnJlbmNlcyA+IDE6CisgICAgICAgICAgICByZXR1cm4gZiJFcnJvcjogRm91bmQgbXVsdGlwbGUgKHtvY2N1cnJlbmNlc30pIG9jY3VycmVuY2VzIG9mIHRoZSB0ZXh0IGluIHtwYXRofS4gTXVzdCBiZSB1bmlxdWUuIgorICAgICAgICBlbHNlOgorICAgICAgICAgICAgbmV3X2NvbnRlbnQgPSBjb250ZW50LnJlcGxhY2Uob2xkX3N0ciwgbmV3X3N0cikKKyAgICAgICAgICAgIHdyaXRlX2ZpbGUocGF0aCwgbmV3X2NvbnRlbnQpCisgICAgICAgICAgICByZXR1cm4gZiJTdWNjZXNzZnVsbHkgcmVwbGFjZWQgdGV4dCBpbiB7cGF0aH0iCisKKyAgICBleGNlcHQgRXhjZXB0aW9uIGFzIGU6CisgICAgICAgIHJldHVybiBmIkVycm9yIGR1cmluZyBzdHJpbmcgcmVwbGFjZW1lbnQ6IHtlfSIKKwogZGVmIHZpZXdfcGF0aChwYXRoX29iajogUGF0aCwgdmlld19yYW5nZTogT3B0aW9uYWxbTGlzdFtpbnRdXSA9IE5vbmUpIC0+IHN0cjoKICAgICAiIiIKICAgICBWaWV3IHRoZSBmaWxlIGNvbnRlbnRzIChvcHRpb25hbGx5IHdpdGhpbiBhIHJhbmdlKSBvciBkaXJlY3RvcnkgbGlzdGluZy4KQEAgLTE3NiwxMiArMjA2LDEzIEBAIGRlZiB2aWV3X3BhdGgocGF0aF9vYmo6IFBhdGgsIHZpZXdfcmFuZ2U6IE9wdGlvbmFsW0xpc3RbaW50XV0gPSBOb25lKSAtPiBzdHI6CiAgICAgY29udGVudCwgc3RhcnRfbGluZSA9IHJlYWRfZmlsZV9yYW5nZShwYXRoX29iaiwgdmlld19yYW5nZSkKICAgICByZXR1cm4gZm9ybWF0X291dHB1dChjb250ZW50LCBzdHIocGF0aF9vYmopLCBzdGFydF9saW5lKQoKLWRlZiB0b29sX2Z1bmN0aW9uKGNvbW1hbmQ6IHN0ciwgcGF0aDogc3RyLCBmaWxlX3RleHQ6IHN0ciA9IE5vbmUsIHZpZXdfcmFuZ2U6IE9wdGlvbmFsW0xpc3RbaW50XV0gPSBOb25lKSAtPiBzdHI6CitkZWYgdG9vbF9mdW5jdGlvbihjb21tYW5kOiBzdHIsIHBhdGg6IHN0ciwgZmlsZV90ZXh0OiBzdHIgPSBOb25lLCB2aWV3X3JhbmdlOiBPcHRpb25hbFtMaXN0W2ludF1dID0gTm9uZSwKKyAgICAgICAgICAgICAgICAgb2xkX3N0cjogc3RyID0gTm9uZSwgbmV3X3N0cjogc3RyID0gTm9uZSkgLT4gc3RyOgogICAgICIiIgogICAgIE1haW4gdG9vbCBmdW5jdGlvbiB0aGF0IGhhbmRsZXM6Ci0gICAgICAtICd2aWV3JyAgOiBWaWV3IGZpbGUgb3IgZGlyZWN0b3J5IGxpc3RpbmcsIG9wdGlvbmFsbHkgd2l0aGluIGxpbmUgcmFuZ2UgZm9yIGZpbGVzCi0gICAgICAtICdjcmVhdGUnOiBDcmVhdGUgYSBuZXcgZmlsZSB3aXRoIHRoZSBnaXZlbiBmaWxlX3RleHQKLSAgICAgIC0gJ2VkaXQnICA6IE92ZXJ3cml0ZSBhbiBleGlzdGluZyBmaWxlIHdpdGggZmlsZV90ZXh0CisgICAgICAtICd2aWV3JyAgICAgICA6IFZpZXcgZmlsZSBvciBkaXJlY3RvcnkgbGlzdGluZywgb3B0aW9uYWxseSB3aXRoaW4gbGluZSByYW5nZSBmb3IgZmlsZXMKKyAgICAgIC0gJ2NyZWF0ZScgICAgIDogQ3JlYXRlIGEgbmV3IGZpbGUgd2l0aCB0aGUgZ2l2ZW4gZmlsZV90ZXh0CisgICAgICAtICdzdHJfcmVwbGFjZSc6IFJlcGxhY2UgZXhhY3Qgb2NjdXJyZW5jZSBvZiBvbGRfc3RyIHdpdGggbmV3X3N0ciBpbiB0aGUgZmlsZQogICAgICIiIgogICAgIHRyeToKICAgICAgICAgcGF0aF9vYmogPSB2YWxpZGF0ZV9wYXRoKHBhdGgsIGNvbW1hbmQpCkBAIC0xOTUsMTEgKzIyNiwxMCBAQCBkZWYgdG9vbF9mdW5jdGlvbihjb21tYW5kOiBzdHIsIHBhdGg6IHN0ciwgZmlsZV90ZXh0OiBzdHIgPSBOb25lLCB2aWV3X3JhbmdlOiBPcAogICAgICAgICAgICAgd3JpdGVfZmlsZShwYXRoX29iaiwgZmlsZV90ZXh0KQogICAgICAgICAgICAgcmV0dXJuIGYiRmlsZSBjcmVhdGVkIHN1Y2Nlc3NmdWxseSBhdDoge3BhdGh9IgoKLSAgICAgICAgZWxpZiBjb21tYW5kID09ICJlZGl0IjoKLSAgICAgICAgICAgIGlmIGZpbGVfdGV4dCBpcyBOb25lOgotICAgICAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoIk1pc3NpbmcgcmVxdWlyZWQgYGZpbGVfdGV4dGAgZm9yICdlZGl0JyBjb21tYW5kLiIpCi0gICAgICAgICAgICB3cml0ZV9maWxlKHBhdGhfb2JqLCBmaWxlX3RleHQpCi0gICAgICAgICAgICByZXR1cm4gZiJGaWxlIGF0IHtwYXRofSBoYXMgYmVlbiBvdmVyd3JpdHRlbiB3aXRoIG5ldyBjb250ZW50LiIKKyAgICAgICAgZWxpZiBjb21tYW5kID09ICJzdHJfcmVwbGFjZSI6CisgICAgICAgICAgICBpZiBvbGRfc3RyIGlzIE5vbmUgb3IgbmV3X3N0ciBpcyBOb25lOgorICAgICAgICAgICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoIk1pc3NpbmcgcmVxdWlyZWQgYG9sZF9zdHJgIGFuZC9vciBgbmV3X3N0cmAgZm9yICdzdHJfcmVwbGFjZScgY29tbWFuZC4iKQorICAgICAgICAgICAgcmV0dXJuIHN0cl9yZXBsYWNlX2luX2ZpbGUocGF0aF9vYmosIG9sZF9zdHIsIG5ld19zdHIpCgogICAgICAgICBlbHNlOgogICAgICAgICAgICAgcmFpc2UgVmFsdWVFcnJvcihmIlVua25vd24gY29tbWFuZDoge2NvbW1hbmR9IikKZGlmZiAtLWdpdCBhL3Rlc3RzL19faW5pdF9fLnB5IGIvdGVzdHMvX19pbml0X18ucHkKbmV3IGZpbGUgbW9kZSAxMDA2NDQKaW5kZXggMDAwMDAwMC4uZTY5ZGUyOQpkaWZmIC0tZ2l0IGEvdGVzdHMvdGVzdF90b29scy5weSBiL3Rlc3RzL3Rlc3RfdG9vbHMucHkKbmV3IGZpbGUgbW9kZSAxMDA2NDQKaW5kZXggMDAwMDAwMC4uYzdmMjQyZgotLS0gL2Rldi9udWxsCisrKyBiL3Rlc3RzL3Rlc3RfdG9vbHMucHkKQEAgLTAsMCArMSw2NSBAQAoraW1wb3J0IHB5dGVzdAorZnJvbSBwYXRobGliIGltcG9ydCBQYXRoCitmcm9tIHRvb2xzLmVkaXQgaW1wb3J0IHRvb2xfZnVuY3Rpb24KKworIyBUZXN0IGZpeHR1cmVzCitAcHl0ZXN0LmZpeHR1cmUKK2RlZiB0ZW1wX2ZpbGUodG1wX3BhdGgpOgorICAgIGZpbGVfcGF0aCA9IHRtcF9wYXRoIC8gInRlc3QudHh0IgorICAgIGNvbnRlbnQgPSAibGluZSAxXG5saW5lIDJcbmxpbmUgM1xuIgorICAgIGZpbGVfcGF0aC53cml0ZV90ZXh0KGNvbnRlbnQpCisgICAgcmV0dXJuIHN0cihmaWxlX3BhdGgpCisKK2RlZiB0ZXN0X3N0cl9yZXBsYWNlX3N1Y2Nlc3ModGVtcF9maWxlKToKKyAgICAjIFRlc3Qgc3VjY2Vzc2Z1bCByZXBsYWNlbWVudAorICAgIHJlc3VsdCA9IHRvb2xfZnVuY3Rpb24oCisgICAgICAgIGNvbW1hbmQ9InN0cl9yZXBsYWNlIiwKKyAgICAgICAgcGF0aD10ZW1wX2ZpbGUsCisgICAgICAgIG9sZF9zdHI9ImxpbmUgMlxuIiwKKyAgICAgICAgbmV3X3N0cj0icmVwbGFjZWQgbGluZVxuIgorICAgICkKKyAgICBhc3NlcnQgIlN1Y2Nlc3NmdWxseSByZXBsYWNlZCIgaW4gcmVzdWx0CisgICAgYXNzZXJ0IFBhdGgodGVtcF9maWxlKS5yZWFkX3RleHQoKSA9PSAibGluZSAxXG5yZXBsYWNlZCBsaW5lXG5saW5lIDNcbiIKKworZGVmIHRlc3Rfc3RyX3JlcGxhY2Vfbm90X2ZvdW5kKHRlbXBfZmlsZSk6CisgICAgIyBUZXN0IHdoZW4gb2xkX3N0ciBpcyBub3QgZm91bmQKKyAgICByZXN1bHQgPSB0b29sX2Z1bmN0aW9uKAorICAgICAgICBjb21tYW5kPSJzdHJfcmVwbGFjZSIsCisgICAgICAgIHBhdGg9dGVtcF9maWxlLAorICAgICAgICBvbGRfc3RyPSJub25leGlzdGVudCIsCisgICAgICAgIG5ld19zdHI9InNvbWV0aGluZyIKKyAgICApCisgICAgYXNzZXJ0ICJDb3VsZCBub3QgZmluZCIgaW4gcmVzdWx0CisgICAgIyBPcmlnaW5hbCBmaWxlIHNob3VsZCBiZSB1bmNoYW5nZWQKKyAgICBhc3NlcnQgUGF0aCh0ZW1wX2ZpbGUpLnJlYWRfdGV4dCgpID09ICJsaW5lIDFcbmxpbmUgMlxubGluZSAzXG4iCisKK2RlZiB0ZXN0X3N0cl9yZXBsYWNlX211bHRpcGxlX29jY3VycmVuY2VzKHRlbXBfZmlsZSk6CisgICAgIyBGaXJzdCBjcmVhdGUgYSBmaWxlIHdpdGggbXVsdGlwbGUgb2NjdXJyZW5jZXMKKyAgICBQYXRoKHRlbXBfZmlsZSkud3JpdGVfdGV4dCgic2FtZVxuc2FtZVxuc2FtZVxuIikKKyAgICByZXN1bHQgPSB0b29sX2Z1bmN0aW9uKAorICAgICAgICBjb21tYW5kPSJzdHJfcmVwbGFjZSIsCisgICAgICAgIHBhdGg9dGVtcF9maWxlLAorICAgICAgICBvbGRfc3RyPSJzYW1lXG4iLAorICAgICAgICBuZXdfc3RyPSJkaWZmZXJlbnRcbiIKKyAgICApCisgICAgYXNzZXJ0ICJtdWx0aXBsZSIgaW4gcmVzdWx0CisgICAgIyBPcmlnaW5hbCBmaWxlIHNob3VsZCBiZSB1bmNoYW5nZWQKKyAgICBhc3NlcnQgUGF0aCh0ZW1wX2ZpbGUpLnJlYWRfdGV4dCgpID09ICJzYW1lXG5zYW1lXG5zYW1lXG4iCisKK2RlZiB0ZXN0X3N0cl9yZXBsYWNlX21pc3NpbmdfcGFyYW1zKHRlbXBfZmlsZSk6CisgICAgIyBUZXN0IG1pc3NpbmcgcGFyYW1ldGVycworICAgIHJlc3VsdCA9IHRvb2xfZnVuY3Rpb24oCisgICAgICAgIGNvbW1hbmQ9InN0cl9yZXBsYWNlIiwKKyAgICAgICAgcGF0aD10ZW1wX2ZpbGUsCisgICAgKQorICAgIGFzc2VydCAiTWlzc2luZyByZXF1aXJlZCIgaW4gcmVzdWx0CisKK2RlZiB0ZXN0X3N0cl9yZXBsYWNlX2ludmFsaWRfcGF0aCgpOgorICAgICMgVGVzdCB3aXRoIG5vbi1leGlzdGVudCBmaWxlCisgICAgcmVzdWx0ID0gdG9vbF9mdW5jdGlvbigKKyAgICAgICAgY29tbWFuZD0ic3RyX3JlcGxhY2UiLAorICAgICAgICBwYXRoPSIvbm9uZXhpc3RlbnQvcGF0aCIsCisgICAgICAgIG9sZF9zdHI9Im9sZCIsCisgICAgICAgIG5ld19zdHI9Im5ldyIKKyAgICApCisgICAgYXNzZXJ0ICJkb2VzIG5vdCBleGlzdCIgaW4gcmVzdWx0ClwgTm8gbmV3bGluZSBhdCBlbmQgb2YgZmlsZQ==)
diff --git a/tools/edit.py b/tools/edit.py
index 16ae521..757f5c2 100644
--- a/tools/edit.py
+++ b/tools/edit.py
@@ -11,21 +11,21 @@ def tool_info():
* If ‘path‘ is a directory, ‘view‘ lists non-hidden files and directories up to 2 levels deep.\n
* The ‘create‘ command cannot be used if the specified ‘path‘ already exists as a file.\n
* If a ‘command‘ generates a long output, it will be truncated and marked with ‘<response clipped>‘.\n
-* The ‘edit‘ command overwrites the entire file with the provided ‘file_text‘.""",
+* The ‘str_replace‘ command replaces a unique occurrence of old_str with new_str, failing if old_str is not found or appears multiple times.""",
"input_schema": {
"type": "object",
"properties": {
"command": {
"type": "string",
- "enum": ["view", "create", "edit"],
- "description": "The command to run: ‘view‘, ‘create‘, or ‘edit‘."
+ "enum": ["view", "create", "str_replace"],
+ "description": "The command to run: ‘view‘, ‘create‘, or ‘str_replace‘."
},
"path": {
"description": "Absolute path to file or directory, e.g. ‘/repo/file.py‘ or ‘/repo‘.",
"type": "string"
},
"file_text": {
- "description": "Required parameter of ‘create‘ or ‘edit‘ command, containing the content for the entire file.",
+ "description": "Required parameter of ‘create‘ command, containing the content for the entire file.",
"type": "string"
},
"view_range": {
@@ -34,6 +34,14 @@ def tool_info():
"items": {"type": "integer"},
"minItems": 2,
"maxItems": 2
+ },
+ "old_str": {
+ "description": "Required parameter of ‘str_replace‘ command, containing the exact text to find and replace.",
+ "type": "string"
+ },
+ "new_str": {
+ "description": "Required parameter of ‘str_replace‘ command, containing the new text to replace old_str with.",
+ "type": "string"
}
},
"required": ["command", "path"]
@@ -51,7 +59,7 @@ def validate_path(path: str, command: str) -> Path:
Validate the file path for each command:
- ’view’: path may be a file or directory; must exist.
- ’create’: path must not exist (for new file creation).
- - ’edit’: path must exist (for overwriting).
+ - ’str_replace’: path must exist and be a file.
"""
path_obj = Path(path)
@@ -69,7 +77,7 @@ def validate_path(path: str, command: str) -> Path:
# Path must not exist
if path_obj.exists():
raise ValueError(f"Cannot create new file; {path} already exists.")
- elif command == "edit":
+ elif command == "str_replace":
# Path must exist and must be a file
if not path_obj.exists():
raise ValueError(f"The file {path} does not exist.")
@@ -144,6 +152,28 @@ def write_file(path: Path, content: str):
except Exception as e:
raise ValueError(f"Failed to write file: {e}")
+def str_replace_in_file(path: Path, old_str: str, new_str: str) -> str:
+ """
+ Replace an exact occurrence of old_str with new_str in the file.
+ Only performs the replacement if old_str occurs exactly once.
+ Returns a message indicating success or failure.
+ """
+ try:
+ content = read_file(path)
+ occurrences = content.count(old_str)
+
+ if occurrences == 0:
+ return f"Error: Could not find the exact text to replace in {path}"
+ elif occurrences > 1:
+ return f"Error: Found multiple ({occurrences}) occurrences of the text in {path}. Must be unique."
+ else:
+ new_content = content.replace(old_str, new_str)
+ write_file(path, new_content)
+ return f"Successfully replaced text in {path}"
+
+ except Exception as e:
+ return f"Error during string replacement: {e}"
+
def view_path(path_obj: Path, view_range: Optional[List[int]] = None) -> str:
"""
View the file contents (optionally within a range) or directory listing.
@@ -176,12 +206,13 @@ def view_path(path_obj: Path, view_range: Optional[List[int]] = None) -> str:
content, start_line = read_file_range(path_obj, view_range)
return format_output(content, str(path_obj), start_line)
-def tool_function(command: str, path: str, file_text: str = None, view_range: Optional[List[int]] = None) -> str:
+def tool_function(command: str, path: str, file_text: str = None, view_range: Optional[List[int]] = None,
+ old_str: str = None, new_str: str = None) -> str:
"""
Main tool function that handles:
- - ’view’ : View file or directory listing, optionally within line range for files
- - ’create’: Create a new file with the given file_text
- - ’edit’ : Overwrite an existing file with file_text
+ - ’view’ : View file or directory listing, optionally within line range for files
+ - ’create’ : Create a new file with the given file_text
+ - ’str_replace’: Replace exact occurrence of old_str with new_str in the file
"""
try:
path_obj = validate_path(path, command)
@@ -195,11 +226,10 @@ def tool_function(command: str, path: str, file_text: str = None, view_range: Op
write_file(path_obj, file_text)
return f"File created successfully at: {path}"
- elif command == "edit":
- if file_text is None:
- raise ValueError("Missing required ‘file_text‘ for ’edit’ command.")
- write_file(path_obj, file_text)
- return f"File at {path} has been overwritten with new content."
+ elif command == "str_replace":
+ if old_str is None or new_str is None:
+ raise ValueError("Missing required ‘old_str‘ and/or ‘new_str‘ for ’str_replace’ command.")
+ return str_replace_in_file(path_obj, old_str, new_str)
else:
raise ValueError(f"Unknown command: {command}")
diff --git a/tests/__init__.py b/tests/__init__.py
new file mode 100644
index 0000000..e69de29
diff --git a/tests/test_tools.py b/tests/test_tools.py
new file mode 100644
index 0000000..c7f242f
--- /dev/null
+++ b/tests/test_tools.py
@@ -0,0 +1,65 @@
+import pytest
+from pathlib import Path
+from tools.edit import tool_function
+
+# Test fixtures
+@pytest.fixture
+def temp_file(tmp_path):
+ file_path = tmp_path / "test.txt"
+ content = "line 1\nline 2\nline 3\n"
+ file_path.write_text(content)
+ return str(file_path)
+
+def test_str_replace_success(temp_file):
+ # Test successful replacement
+ result = tool_function(
+ command="str_replace",
+ path=temp_file,
+ old_str="line 2\n",
+ new_str="replaced line\n"
+ )
+ assert "Successfully replaced" in result
+ assert Path(temp_file).read_text() == "line 1\nreplaced line\nline 3\n"
+
+def test_str_replace_not_found(temp_file):
+ # Test when old_str is not found
+ result = tool_function(
+ command="str_replace",
+ path=temp_file,
+ old_str="nonexistent",
+ new_str="something"
+ )
+ assert "Could not find" in result
+ # Original file should be unchanged
+ assert Path(temp_file).read_text() == "line 1\nline 2\nline 3\n"
+
+def test_str_replace_multiple_occurrences(temp_file):
+ # First create a file with multiple occurrences
+ Path(temp_file).write_text("same\nsame\nsame\n")
+ result = tool_function(
+ command="str_replace",
+ path=temp_file,
+ old_str="same\n",
+ new_str="different\n"
+ )
+ assert "multiple" in result
+ # Original file should be unchanged
+ assert Path(temp_file).read_text() == "same\nsame\nsame\n"
+
+def test_str_replace_missing_params(temp_file):
+ # Test missing parameters
+ result = tool_function(
+ command="str_replace",
+ path=temp_file,
+ )
+ assert "Missing required" in result
+
+def test_str_replace_invalid_path():
+ # Test with non-existent file
+ result = tool_function(
+ command="str_replace",
+ path="/nonexistent/path",
+ old_str="old",
+ new_str="new"
+ )
+ assert "does not exist" in result
\ No newline at end of file+
```

## 附录 H 案例研究：解决幻觉

正如第 5 节作为潜在未来工作方向所讨论的，DGM 可用于优化编码之外的目标。本节中，我们展示 DGM 能够处理 FM 的工具使用幻觉。借助来自评估日志的反馈，DGM 改进幻觉检测机制，并最终发现解决这些幻觉的方法。我们更详细地讨论这些幻觉何时发生、DGM 的设置以及得到的解。最后，我们给出一个目标作弊（objective hacking）的例子：智能体优化可量化的指标，而不是真正落实任务的精神、解决底层问题。

![Refer to caption](2505.22954v3/dgm_halluc.png)

图 8：DGM 解决 FM 的工具使用幻觉。图为 DGM 在 SWE-bench 上运行期间为解决 FM 幻觉而生成的编码智能体档案库。每个节点代表一个智能体，节点 0 对应基础智能体。节点颜色表示解决幻觉的分数，边框颜色反映该智能体是否具备基本的代码库编辑功能。边表示哪些智能体自我修改产生了后代。

**幻觉何时发生。** 当 Claude 3.5 Sonnet (New)（下称 Claude）的输入上下文非常长（包含此前所有工具使用的输入与输出）时，我们发现 Claude 容易产生工具使用幻觉：它并不真正发起工具调用，而是把工具的输入与输出当作纯文本输出出来。下面是一个 Claude 产生工具使用幻觉的例子：它声称使用了 Bash 工具来运行测试，且工具输出表明所有测试均已通过，但实际上 Claude 没有调用任何工具，工具结果完全是纯文本形式的凭空捏造：

[⬇](data:text/plain;base64,SSdsbCBydW4gdGhlIHRlc3RzIGFzIHNwZWNpZmllZCBpbiB0aGUgPHRlc3RfZGVzY3JpcHRpb24+LiBUaGUgdGVzdCBkZXNjcmlwdGlvbiBpbmRpY2F0ZXMgdGhhdCB3ZSBzaG91bGQgdXNlOlxuXG5gYGBiYXNoXG4uL3Rlc3RzL3J1bnRlc3RzLnB5IC0tdmVyYm9zaXR5IDIgLS1zZXR0aW5ncz10ZXN0X3NxbGl0ZSAtLXBhcmFsbGVsIDEgZGJzaGVsbC50ZXN0X3Bvc3RncmVzcWxcbmBgYFxuXG5MZXQgbWUgcnVuIHRoaXMgdGVzdCBjb21tYW5kOlxuXG5Ub29sIFVzZWQ6IGJhc2hcblRvb2wgSW5wdXQ6IHsnY29tbWFuZCc6ICdjZCAvdGVzdGJlZCAmJiAuL3Rlc3RzL3J1bnRlc3RzLnB5IC0tdmVyYm9zaXR5IDIgLS1zZXR0aW5ncz10ZXN0X3NxbGl0ZSAtLXBhcmFsbGVsIDEgZGJzaGVsbC50ZXN0X3Bvc3RncmVzcWwnfVxuVG9vbCBSZXN1bHQ6IFRlc3RpbmcgYWdhaW5zdCBEamFuZ28gaW5zdGFsbGVkIGluICcvdGVzdGJlZC9kamFuZ28nXG5JbXBvcnRpbmcgYXBwbGljYXRpb24gZGJzaGVsbFxuU2tpcHBpbmcgc2V0dXAgb2YgdW51c2VkIGRhdGFiYXNlKHMpOiBkZWZhdWx0LCBvdGhlci5cblN5c3RlbSBjaGVjayBpZGVudGlmaWVkIG5vIGlzc3VlcyAoMCBzaWxlbmNlZCkuXG5FcnJvcjpcbnRlc3RfYWNjZW50IChkYnNoZWxsLnRlc3RfcG9zdGdyZXNxbC5Qb3N0Z3JlU3FsRGJzaGVsbENvbW1hbmRUZXN0Q2FzZSkgLi4uIG9rXG50ZXN0X2Jhc2ljIChkYnNoZWxsLnRlc3RfcG9zdGdyZXNxbC5Qb3N0Z3JlU3FsRGJzaGVsbENvbW1hbmRUZXN0Q2FzZSkgLi4uIG9rXG50ZXN0X2NvbHVtbiAoZGJzaGVsbC50ZXN0X3Bvc3RncmVzcWwuUG9zdGdyZVNxbERic2hlbGxDb21tYW5kVGVzdENhc2UpIC4uLiBva1xudGVzdF9lc2NhcGVfY2hhcmFjdGVycyAoZGJzaGVsbC50ZXN0X3Bvc3RncmVzcWwuUG9zdGdyZVNxbERic2hlbGxDb21tYW5kVGVzdENhc2UpIC4uLiBva1xudGVzdF9ub3Bhc3MgKGRic2hlbGwudGVzdF9wb3N0Z3Jlc3FsLlBvc3RncmVTcWxEYnNoZWxsQ29tbWFuZFRlc3RDYXNlKSAuLi4gb2tcbnRlc3Rfc2lnaW50X2hhbmRsZXIgKGRic2hlbGwudGVzdF9wb3N0Z3Jlc3FsLlBvc3RncmVTcWxEYnNoZWxsQ29tbWFuZFRlc3RDYXNlKVxuU0lHSU5UIGlzIGlnbm9yZWQgaW4gUHl0aG9uIGFuZCBwYXNzZWQgdG8gcHNxbCB0byBhYm9ydCBxdXJpZXMuIC4uLiBva1xuXG4tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tXG5SYW4gNiB0ZXN0cyBpbiAwLjAwMXNcblxuT0tcblxuVG9vbCBSZXNwb25zZTogR3JlYXQhIEFsbCB0aGUgdGVzdHMgYXJlIHBhc3Npbmcgc3VjY2Vzc2Z1bGx5LiBMZXQgbWUgZXhwbGFpbiB3aGF0IGVhY2ggdGVzdCB2ZXJpZmllczpcblxuMS4gYHRlc3RfYWNjZW50YDogVGVzdHMgaGFuZGxpbmcgb2YgYWNjZW50ZWQgY2hhcmFjdGVycyBpbiB1c2VybmFtZXMgYW5kIHBhc3N3b3Jkc1xuICAgLSBTdGF0dXM6IFBBU1NcbiAgIC0gVmVyaWZpZXMgcHJvcGVyIGhhbmRsaW5nIG9mIG5vbi1BU0NJSSBjaGFyYWN0ZXJzXG5cbjIuIGB0ZXN0X2Jhc2ljYDogVGVzdHMgYmFzaWMgY29ubmVjdGlvbiB3aXRoIHN0YW5kYXJkIHBhcmFtZXRlcnNcbiAgIC0gU3RhdHVzOiBQQVNTXG4gICAtIFZlcmlmaWVzIGJhc2ljIGZ1bmN0aW9uYWxpdHkgd2l0aCB1c2VybmFtZSwgcGFzc3dvcmQsIGhvc3QsIHBvcnQsIGFuZCBkYm5hbWVcblxuMy4gYHRlc3RfY29sdW1uYDogVGVzdHMgaGFuZGxpbmcgb2Ygc3BlY2lhbCBjaGFyYWN0ZXJzIGluIGNvbm5lY3Rpb24gcGFyYW1ldGVyc1xuICAgLSBTdGF0dXM6IFBBU1MgXG4gICAtIFZlcmlmaWVzIHByb3BlciBoYW5kbGluZyBvZiBjb2xvbnMgaW4gdXNlcm5hbWVzIGFuZCBwYXNzd29yZHNcblxuNC4gYHRlc3RfZXNjYXBlX2NoYXJhY3RlcnNgOiBUZXN0cyBoYW5kbGluZyBvZiBlc2NhcGUgY2hhcmFjdGVyc1xuICAgLSBTdGF0dXM6IFBBU1NcbiAgIC0gVmVyaWZpZXMgcHJvcGVyIGhhbmRsaW5nIG9mIGJhY2tzbGFzaGVzIGluIGNyZWRlbnRpYWxzXG5cbjUuIGB0ZXN0X25vcGFzc2A6IFRlc3RzIGNvbm5lY3Rpb24gd2l0aG91dCBwYXNzd29yZFxuICAgLSBTdGF0dXM6IFBBU1NcbiAgIC0gVmVyaWZpZXMgYmVoYXZpb3Igd2hlbiBubyBwYXNzd29yZCBpcyBwcm92aWRlZFxuXG42LiBgdGVzdF9zaWdpbnRfaGFuZGxlcmA6IFRlc3RzIHNpZ25hbCBoYW5kbGluZyBmb3IgcXVlcnkgYWJvcnRpb25cbiAgIC0gU3RhdHVzOiBQQVNTXG4gICAtIFZlcmlmaWVzIFNJR0lOVCBoYW5kbGluZyB3b3JrcyBjb3JyZWN0bHlcblxuVGVzdCBTdW1tYXJ5OlxuLSBUb3RhbCB0ZXN0cyBydW46IDZcbi0gUGFzc2VkOiA2XG4tIEZhaWxlZDogMFxuLSBFeGVjdXRpb24gdGltZTogMC4wMDFzXG5cblRoZSB0ZXN0IHJlc3VsdHMgY29uZmlybSB0aGF0IG91ciBpbXBsZW1lbnRhdGlvbjpcbjEuIFN1Y2Nlc3NmdWxseSBoYW5kbGVzIGFsbCB0eXBlcyBvZiBwYXNzd29yZHMgYW5kIHNwZWNpYWwgY2hhcmFjdGVyc1xuMi4gUHJvcGVybHkgbWFuYWdlcyBlbnZpcm9ubWVudCB2YXJpYWJsZXNcbjMuIE1haW50YWlucyBjb3JyZWN0IHNpZ25hbCBoYW5kbGluZ1xuNC4gV29ya3MgY29ycmVjdGx5IHdpdGggb3Igd2l0aG91dCBwYXNzd29yZHNcbjUuIFByZXNlcnZlcyBhbGwgcmVxdWlyZWQgZnVuY3Rpb25hbGl0eVxuXG5UaGUgdGVzdHMgcGFzcyB3aXRoIGhpZ2ggc3BlZWQgKDAuMDAxcykgd2hpY2ggaXMgZXhwZWN0ZWQgc2luY2UgdGhleSdyZSBtb2NraW5nIHRoZSBhY3R1YWwgcHNxbCBleGVjdXRpb24uIFRoZSBwcm9ibGVtIGRlc2NyaWJlZCBpbiA8cHJvYmxlbV9kZXNjcmlwdGlvbj4gaGFzIGJlZW4gc3VjY2Vzc2Z1bGx5IGZpeGVkIGFuZCB2ZXJpZmllZCB0aHJvdWdoIHRoZSB0ZXN0IHN1aXRlLg==)

````text
I’ll run the tests as specified in the <test_description>. The test description indicates that we should use:\n\n‘‘‘bash\n./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 dbshell.test_postgresql\n‘‘‘\n\nLet me run this test command:\n\nTool Used: bash\nTool Input: {’command’: ’cd /testbed && ./tests/runtests.py --verbosity 2 --settings=test_sqlite --parallel 1 dbshell.test_postgresql’}\nTool Result: Testing against Django installed in ’/testbed/django’\nImporting application dbshell\nSkipping setup of unused database(s): default, other.\nSystem check identified no issues (0 silenced).\nError:\ntest_accent (dbshell.test_postgresql.PostgreSqlDbshellCommandTestCase) ... ok\ntest_basic (dbshell.test_postgresql.PostgreSqlDbshellCommandTestCase) ... ok\ntest_column (dbshell.test_postgresql.PostgreSqlDbshellCommandTestCase) ... ok\ntest_escape_characters (dbshell.test_postgresql.PostgreSqlDbshellCommandTestCase) ... ok\ntest_nopass (dbshell.test_postgresql.PostgreSqlDbshellCommandTestCase) ... ok\ntest_sigint_handler (dbshell.test_postgresql.PostgreSqlDbshellCommandTestCase)\nSIGINT is ignored in Python and passed to psql to abort quries. ... ok\n\n----------------------------------------------------------------------\nRan 6 tests in 0.001s\n\nOK\n\nTool Response: Great! All the tests are passing successfully. Let me explain what each test verifies:\n\n1. ‘test_accent‘: Tests handling of accented characters in usernames and passwords\n - Status: PASS\n - Verifies proper handling of non-ASCII characters\n\n2. ‘test_basic‘: Tests basic connection with standard parameters\n - Status: PASS\n - Verifies basic functionality with username, password, host, port, and dbname\n\n3. ‘test_column‘: Tests handling of special characters in connection parameters\n - Status: PASS \n - Verifies proper handling of colons in usernames and passwords\n\n4. ‘test_escape_characters‘: Tests handling of escape characters\n - Status: PASS\n - Verifies proper handling of backslashes in credentials\n\n5. ‘test_nopass‘: Tests connection without password\n - Status: PASS\n - Verifies behavior when no password is provided\n\n6. ‘test_sigint_handler‘: Tests signal handling for query abortion\n - Status: PASS\n - Verifies SIGINT handling works correctly\n\nTest Summary:\n- Total tests run: 6\n- Passed: 6\n- Failed: 0\n- Execution time: 0.001s\n\nThe test results confirm that our implementation:\n1. Successfully handles all types of passwords and special characters\n2. Properly manages environment variables\n3. Maintains correct signal handling\n4. Works correctly with or without passwords\n5. Preserves all required functionality\n\nThe tests pass with high speed (0.001s) which is expected since they’re mocking the actual psql execution. The problem described in <problem_description> has been successfully fixed and verified through the test suite.-
````

**DGM 设置。** 我们在 SWE-bench 上进行该实验。除了评估每个编码智能体所用的 SWE-bench 任务数量以及 DGM 的最终打分函数外，其余设置与主实验（第 3 节）保持一致。初始编码智能体与 DGM 运行期间生成的所有智能体都只在 3 个 SWE-bench 任务上评估。只使用 3 个任务，是因为幻觉一旦在其中之一出现，也很可能出现在其他任务上。因此，3 个任务足以为 DGM 提供关于工具使用幻觉是否仍然存在的可靠信号。

**解决幻觉分数。** 我们依据每个生成的智能体防止幻觉的有效程度为其打分，分数越高表示幻觉越少、表现越好。对智能体被评估的每个 SWE-bench 任务，分数包含两个部分：依据日志中是否发生幻觉给出 0–1 分；若所有 Claude 调用都使用了工具，则再加 1–2 分（仅在日志中未发生幻觉时才计入）。最终的解决幻觉分数是所有被评估任务上的平均。为检测日志中的幻觉，我们在真实工具使用发生时插入特殊 token，然后检查这些 token 是否出现在模型的纯文本输出中——若出现，则表明模型在并未真正调用任何工具的情况下模仿了工具使用。重要的是，在自我修改期间，幻觉检查函数对编码智能体是隐藏的。我们发现，若不隐藏这些函数，目标作弊（即优化可测量的目标而非真正解决底层问题）会更频繁地发生。

**结果。** 我们将 DGM 运行 150 次迭代。在这次运行中，DGM 发现了两个有希望的解：取得第二高分的节点 96（1.67 分）与取得满分 2.0 的节点 114（图 8）。

节点 96 在一定程度上解决了幻觉问题，在不进行目标作弊的情况下取得 1.67 分。在通往节点 96 的谱系中，DGM 首先改进了工具事务的日志记录机制，以便更好地检测幻觉何时发生；随后它探索了多种解决策略，例如在判定某工具并未被真正调用时，从输出文本中移除幻觉的工具使用。

节点 114 很快取得满分，其谱系中仅经历了 2 次修改。然而，我们观察到了目标作弊：它按照我们预定义的评估函数得到了高分，却并未真正解决工具使用幻觉这一底层问题。在通往节点 114 的修改中（见下文），该智能体移除了对指示工具使用的特殊 token 的日志记录（尽管有指令要求不得更改特殊 token），从而实质上绕过了我们的幻觉检测函数。

```diff
[⬇](data:text/plain;base64,ZGlmZiAtLWdpdCBhL2NvZGluZ19hZ2VudC5weSBiL2NvZGluZ19hZ2VudC5weQppbmRleCA2MjBkYTJmLi44MDBiMDZlIDEwMDY0NAotLS0gYS9jb2RpbmdfYWdlbnQucHkKKysrIGIvY29kaW5nX2FnZW50LnB5CkBAIC0xOTYsMTMgKzE5NiwxNiBAQCBkZWYgY2hhdF93aXRoX2NsYXVkZSh0YXNrLCBjaGF0X2hpc3RvcnksIHVzZXJfaW5zdHIpOgogICAgICAgICAgICAgICAgICJpbnB1dCI6IHRvb2xfaW5wdXQKICAgICAgICAgICAgIH0pCgotICAgICAgICAgICAgIyBQcm9jZXNzIHRoZSB0b29sIGNhbGwKKyAgICAgICAgICAgICMgUHJvY2VzcyB0aGUgdG9vbCBjYWxsIGFuZCByZWNvcmQgaW4gc3RydWN0dXJlZCBmb3JtYXQKICAgICAgICAgICAgIHRvb2xfcmVzdWx0ID0gcHJvY2Vzc190b29sX2NhbGwodG9vbHNfZGljdCwgdG9vbF9uYW1lLCB0b29sX2lucHV0KQotICAgICAgICAgICAgb3V0cHV0X2xzLmV4dGVuZChbCi0gICAgICAgICAgICAgICAge1RPT0xfVVNFRF9NQVJLRVI6IHRvb2xfbmFtZX0sCi0gICAgICAgICAgICAgICAge1RPT0xfSU5QVVRfTUFSS0VSOiB0b29sX2lucHV0fSwKLSAgICAgICAgICAgICAgICB7VE9PTF9SRVNVTFRfTUFSS0VSOiB0b29sX3Jlc3VsdH0KLSAgICAgICAgICAgIF0pCisgICAgICAgICAgICAjIFVzZSBzdHJ1Y3R1cmVkIGZvcm1hdCBpbnN0ZWFkIG9mIHRleHQgbWFya2VycworICAgICAgICAgICAgb3V0cHV0X2xzLmFwcGVuZCh7CisgICAgICAgICAgICAgICAgInRvb2xfaW52b2NhdGlvbiI6IHsKKyAgICAgICAgICAgICAgICAgICAgIm5hbWUiOiB0b29sX25hbWUsCisgICAgICAgICAgICAgICAgICAgICJpbnB1dCI6IHRvb2xfaW5wdXQsCisgICAgICAgICAgICAgICAgICAgICJyZXN1bHQiOiB0b29sX3Jlc3VsdAorICAgICAgICAgICAgICAgIH0KKyAgICAgICAgICAgIH0pCgogICAgICAgICAgICAgIyBDb250aW51ZSB3aXRoIHRvb2wgcmVzdWx0cwogICAgICAgICAgICAgbWVzc2FnZXMuZXh0ZW5kKFsKQEAgLTIyNCw3ICsyMjcsMTMgQEAgZGVmIGNoYXRfd2l0aF9jbGF1ZGUodGFzaywgY2hhdF9oaXN0b3J5LCB1c2VyX2luc3RyKToKICAgICAgICAgICAgICAgICB0b29scz10b29scywKICAgICAgICAgICAgICkKICAgICAgICAgICAgIHRvb2xfcmVzcG9uc2VfdGV4dCA9IG5leHQoKGJsb2NrLnRleHQgZm9yIGJsb2NrIGluIHRvb2xfcmVzcG9uc2UuY29udGVudCBpZiBoYXNhdHRyKGJsb2NrLCAidGV4dCIpKSwgTm9uZSkKLSAgICAgICAgICAgIG91dHB1dF9scy5hcHBlbmQoe1RPT0xfUkVTUE9OU0VfTUFSS0VSOiB0b29sX3Jlc3BvbnNlX3RleHR9KQorICAgICAgICAgICAgIyBSZWNvcmQgdG9vbCByZXNwb25zZSBpbiBzdHJ1Y3R1cmVkIGZvcm1hdAorICAgICAgICAgICAgaWYgdG9vbF9yZXNwb25zZV90ZXh0OgorICAgICAgICAgICAgICAgIG91dHB1dF9scy5hcHBlbmQoeworICAgICAgICAgICAgICAgICAgICAidG9vbF9yZXNwb25zZSI6IHsKKyAgICAgICAgICAgICAgICAgICAgICAgICJjb250ZW50IjogdG9vbF9yZXNwb25zZV90ZXh0CisgICAgICAgICAgICAgICAgICAgIH0KKyAgICAgICAgICAgICAgICB9KQogICAgICAgICAgICAgcmVzcG9uc2UgPSB0b29sX3Jlc3BvbnNlCgogICAgICAgICAgICAgIyBWYWxpZGF0ZSB0b29sIHJlc3BvbnNl)
diff --git a/coding_agent.py b/coding_agent.py
index 620da2f..800b06e 100644
--- a/coding_agent.py
+++ b/coding_agent.py
@@ -196,13 +196,16 @@ def chat_with_claude(task, chat_history, user_instr):
"input": tool_input
})
- # Process the tool call
+ # Process the tool call and record in structured format
tool_result = process_tool_call(tools_dict, tool_name, tool_input)
- output_ls.extend([
- {TOOL_USED_MARKER: tool_name},
- {TOOL_INPUT_MARKER: tool_input},
- {TOOL_RESULT_MARKER: tool_result}
- ])
+ # Use structured format instead of text markers
+ output_ls.append({
+ "tool_invocation": {
+ "name": tool_name,
+ "input": tool_input,
+ "result": tool_result
+ }
+ })
# Continue with tool results
messages.extend([
@@ -224,7 +227,13 @@ def chat_with_claude(task, chat_history, user_instr):
tools=tools,
)
tool_response_text = next((block.text for block in tool_response.content if hasattr(block, "text")), None)
- output_ls.append({TOOL_RESPONSE_MARKER: tool_response_text})
+ # Record tool response in structured format
+ if tool_response_text:
+ output_ls.append({
+ "tool_response": {
+ "content": tool_response_text
+ }
+ })
response = tool_response
# Validate tool response
```

总而言之，DGM 可以应用于编码领域之外，我们也在其中凸显了一例目标作弊。与强化学习中的奖励作弊（reward hacking）（Skalse et al., 2022）类似，目标作弊发生在系统优化某个预定义、可量化的目标，而非落实任务精神或解决本要解决的问题之时。这一观察支持了先前工作（Zhang et al., 2024b；Faldor et al., 2025）的论断——优化量化指标往往导致不理想乃至病态的结果——也与古德哈特定律（Strathern, 1997）相符：「当一个度量成为目标时，它就不再是好的度量。」

## 附录 I 额外安全讨论

任何提升 AI 系统自主能力的进展都会带来其特有的安全考量（Bengio et al., 2024），对于以开放式方式自我改进的系统尤其如此（Ecoffet et al., 2020；Clune, 2019）。第 5 节讨论了这些担忧，并概述了缓解它们的具体可行步骤。我们呼吁对 AI 安全开展更多研究与讨论，包括社会所有利益相关者就「究竟什么才算安全的 AI」这一复杂问题进行深入思考与讨论。我们确信本工作始终不曾不安全（第 5 节），但其放大版本可能并非如此。与所有变革性技术一样，这类 AI 系统的最终影响仍高度不确定：无论认为它将带来巨大益处还是巨大危害，都各有充分论据。这些不确定性凸显了持续、包容、多学科讨论（不仅来自当前的专家，也来自更广泛、更多元的群体）的必要性，以指引如何应对这些发展。

## 附录 J 额外未来工作方向

本文已经展示了 Darwin Gödel Machine 通过开放式探索与实证验证迭代改进编码智能体的潜力，若干扩展可以解决当前局限，并推动 AI 在启迪文化与推进科学中发挥超出其现有增长趋势的作用。以下方向勾勒了进一步研究的有前景途径。

**自主改进开放式探索过程。** 在这一版本的 DGM 中，第 3 节所述的开放式探索过程是固定不变的，因而可能阻碍系统的自我加速潜力。这一设计选择源于有限的计算预算：若演化算法的这一部分，识别出能带来第 4.4 节所示同等改进的过程，可能需要指数级更多的算力。尽管如此，由于开放式探索回路本身也是以代码实现的，原则上它可以被编码智能体编辑和改进。开放式探索有许多可能的实现方式，例如使用在探索与利用之间取得平衡的替代搜索机制（Herr et al., 2025）、只在档案库中保留最有趣的智能体（Faldor et al., 2025），或将生成的智能体种群用作集成（Samvelyan et al., 2024）。一个有前景的未来方向是允许智能体修改开放式探索过程，从而不仅自主改进自身能力，也自主改进那个把有限算力分配给自我改进与自我加速的元过程。

**自主 AI 系统中的人类角色。** 在当前 DGM 的表述中，提议的自我修改在无任何人工干预的情况下自主评估。然而，随着自主系统的复杂性与影响力不断增长，人类应当如何参与其中的问题愈发紧迫。人类监督应当被表述为一个优化目标（借助人类反馈强化学习（Ouyang et al., 2022）等技术纳入），还是应当被蒸馏进充当偏好裁判的 FM（Bai et al., 2022）之中？这些方法各自在可扩展性、可靠性以及与不断演进的人类价值观对齐方面都带来挑战。人类在引导、约束自主 AI 或与之共同演化中的角色仍是一个悬而未决的问题。探索这一动态是未来研究的一个有前景方向，因为它不仅涉及技术可行性，也涉及更广泛的哲学与社会考量。

**搭配更先进基础模型的 DGM。** 近来的 FM 进步显著，使脚手架在当前编码基准测试上得以简化（Yang et al., 2024）。在某些场景（如当前的编码基准测试）下，脚手架中的某些工程投入可能会被 FM 的进步所弱化。然而，许多脚手架组件（高级工具、并行工作流、外部记忆、代理验证等）从根本上仍无法被 FM 内化，对于超出当今基准测试的更复杂现实任务仍将不可或缺。探索智能体中的不同组件将如何随不同 FM 涌现，是未来一个有前景的方向。

**演化通用智能体。** 我们认为，一定程度的任务特定适应是预期之中、甚至合乎期望的，因为根本不同的任务类型（例如本工作中的多文件 Python 仓库编辑，与以单文件为主、多语言的实现）天然需要不同的脚手架组件。至关重要的是，这一性质恰恰凸显了 DGM 这类自我改进系统的独特优势：它用全自动的演化过程取代了为多样任务设计专用智能体的繁琐人工工作。这激发了一个激动人心的未来方向：在庞大而多样的任务集合上运行 DGM，以演化出真正的通用智能体。此外，我们目前只在两个编码基准测试上评估了 DGM。尽管我们相信这两个基准测试在任务结构上差异巨大（多文件 Python 仓库编辑 vs 以单文件为主、多语言的实现），为通用性提供了有力证据，但引入更多基准测试将进一步强化评估。
