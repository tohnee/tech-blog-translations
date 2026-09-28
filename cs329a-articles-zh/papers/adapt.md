---
title: "ADaPT：用语言模型按需分解与规划"
title_en: "ADaPT: As-Needed Decomposition and Planning with Language Models"
arxiv: 2311.05772
source: https://arxiv.org/abs/2311.05772
crawled: 2026-09-23
translated: 2026-09-23
---

# ADaPT：用语言模型按需分解与规划

> 原文：[ADaPT: As-Needed Decomposition and Planning with Language Models](https://arxiv.org/abs/2311.05772) · Stanford CS329A 指定阅读

Archiki Prasad
所属机构：UNC Chapel Hill
  
Alexander Koller
所属机构：萨尔兰大学
  
Mareike Hartmann
所属机构：萨尔兰大学
  
Peter Clark
所属机构：Allen Institute for AI
  
Ashish Sabharwal
所属机构：Allen Institute for AI
  
Mohit Bansal
所属机构：UNC Chapel Hill
  
Tushar Khot
所属机构：Allen Institute for AI

###### 摘要

大型语言模型（LLM）正日益被用于需要规划与环境适应的交互式决策任务。近期工作大致以两种方式把 LLM 用作智能体：迭代地决定下一个动作（迭代执行器），或先生成计划再用 LLM 执行子任务（计划-执行）。然而，这些方法在任务复杂度面前会遇到困难，因为任何一个子任务无法执行都可能导致任务失败。为解决这些不足，我们提出面向复杂任务的按需分解与规划（As-Needed Decomposition and Planning for complex Tasks，ADaPT），一种*按需*显式规划并分解复杂子任务的方法，即在 LLM 无法执行它们时才进行分解。ADaPT 递归地分解子任务，以同时适应任务复杂度与 LLM 能力。我们的结果表明，ADaPT 大幅超越已有的强基线，在 ALFWorld 上成功率高出最多 28.3%，在 WebShop 上高出 27%，在我们提出的一个新组合式数据集 TextCraft 上高出 33%。通过广泛的分析，我们阐明了多级分解的重要性，并证明 ADaPT 能动态地适配执行器 LLM 的能力以及任务复杂度。1
注 1：项目主页：<https://allenai.github.io/adaptllm>

![Refer to caption](2311.05772v2/intro.png)

图 1：
左上：迭代执行器（如 ReAct，Yao et al., 2023b）直接与环境交互，隐式地进行规划。右上：计划-执行方法（如 Yang et al., 2023）为任务创建一个固定计划，未考虑执行步骤 1 的复杂度。下方：ADaPT 根据执行器的成功与否动态分解。

## 1 引言

大型语言模型（LLM）的最新进展将其应用从传统 NLP 任务扩展到涉及数学、符号与常识推理的更复杂任务（Wei et al., 2022；Huang and Chang, 2023）。近期的模型甚至被应用于决策任务，如做家务、浏览网页等，这些任务需要与外部环境或工具交互（Yao et al., 2023b；Qin et al., 2023）。

先前使用 LLM 进行决策的工作，如 ReAct（Yao et al., 2023b），在给定动作与观察历史的情况下迭代地生成要在环境中执行的下一个动作（见图 1；左上）。然而，随着任务变得更复杂，LLM 会因其有限的组合能力（Dziri et al., 2023）以及处理长动作-观察轨迹中干扰项的无能为力（Shi et al., 2023）而陷入困境。

为缓解这一问题，模块化方法（Khot et al., 2023；Yang et al., 2023；Sun et al., 2023）引入一个单独的规划器模块，利用 LLM 创建高层计划。2
注 2：我们所说的「规划」指的是设计一个子任务列表来完成复杂任务这一通俗概念，而非经典 AI 规划文献中的用法。例如，「做千层面」的一个「计划」可以是：煮意面、做酱汁、分层铺放原料、然后烘烤。然后规划器把较简单的子任务委托给执行器 LLM 模块，从而降低执行器所需的组合复杂度与动作轨迹长度。我们宽泛地把这一类方法称为*计划-执行*（plan-and-execute）方法（见图 1；右上）。虽然计划使这些方法能够指导执行并跟踪进度（Wang et al., 2023b），但其非自适应的性质在面对无法实现的子任务时构成局限。如图 1（右上）所示，这些方法本质上缺乏适应任务复杂度与管理执行失败的灵活性，仅仅一个过于复杂的子任务就会导致整体任务失败。

为解决此类失败，我们提出面向复杂任务的按需分解与规划（ADaPT），一种*在必要时*进一步分解子任务的递归算法，以动态适应任务复杂度。我们在框架中使用独立的*规划器*与*执行器* LLM 模块，但*只有*当执行器 LLM 检测到失败时，才用规划器分解任务。如图 1 所示，在陌生家庭中把一个干净马克杯放到桌上这一整体任务对模型而言过于复杂，导致迭代执行器失败。而计划-执行式的方法最初把任务拆成三个子任务，却未能考虑到「找到马克杯」的复杂度。而且，事先预判这样一个子任务的难度本身就很困难，因为执行器可能第一次尝试就找到马克杯，也可能要找遍隐蔽角落。因此，ADaPT 利用其递归结构来*动态适应*（由 LLM 评估的）执行失败，通过规划器*进一步分解*「找到马克杯」这个复杂子任务。

在实证上，我们在三个涉及交互式环境的数据集上展示 ADaPT 的有效性：ALFWorld（Shridhar et al., 2021）、WebShop（Yao et al., 2022），以及一个新的用于合成 Minecraft 配方的组合式文字游戏 *TextCraft*（第 4.1 节）。以 GPT-3.5 作为底层 LLM，ADaPT 胜过强基线（在第 4.2 节讨论），如 ReAct（Yao et al., 2023b）与 Plan-and-Solve（Wang et al., 2023b），在 ALFWorld、WebShop 与 TextCraft 上分别高出最多 28.3%、27% 与 33% 个绝对百分点（第 5 节）。与 Reflexion（Shinn et al., 2023）——一种处理*整个任务轨迹失败*的自适应方法——相比，ADaPT 在 ALFWorld、WebShop 与 TextCraft 上分别取得高 14.1%、9% 与 20% 的成功率。通过对 ADaPT 的广泛分析，我们确立了递归分解的重要性（第 6.1 节），并展示了其对执行器 LLM 能力（包括 LLaMA-2（Touvron et al., 2023）与 Lemur（Xu et al., 2023）等开源模型）的动态适配（第 6.2 节）。最后，我们证明 ADaPT 会把任务复杂度纳入考量（第 6.3 节），其中递归分解的程度与任务的内在复杂度相吻合。总结而言，我们的贡献是：

1. 我们提出 ADaPT，一种按需动态分解复杂子任务的递归算法，即*只在任务对执行器过于复杂时才介入*。
2. 在 ALFWorld、WebShop 与 TextCraft 三个多样的数据集上，ADaPT 将 GPT-3.5 的成功率相对先前方法分别提升最多 28.3%、27% 与 33% 个百分点。
3. 对 ADaPT 的分析强调了递归分解的意义，以及动态适应不同 LLM 执行能力与任务复杂度的能力。

## 2 相关工作

#### 用于决策的 LLM。

LLM 已被成功用作智能体来执行各种决策任务，如机器人导航（Ahn et al., 2022；Huang et al., 2023b；Singh et al., 2023）、Minecraft 等复杂多模态游戏（Fan et al., 2022；Wang et al., 2023a）、基于文本的环境（Shridhar et al., 2021；Liu et al., 2023）。虽然这些工作大多聚焦于从轨迹中学习，ReAct（Yao et al., 2023b）使用少样本提示构建一个智能体，在给定先前动作与观察的情况下，对当前状态进行推理（思考）并在环境中生成下一个动作。其迭代式方法（见图 1；左上）能处理失败，但它们必须在决定每个局部动作时*隐式*地跟踪整个计划（对比附录 A 图 9 中的 ADaPT）。通过把规划与执行纳入独立模块并实现动态适应，我们能够取得更高的成功率（参见第 5 节）。

若干后续工作通过在未来尝试中纳入反馈（Madaan et al., 2023；Shinn et al., 2023），或使用 LLM 为搜索开发启发式（Yao et al., 2023a；Zhou et al., 2023）来改进 ReAct 框架。与 ADaPT 相比，它们不采用任务分解，导致不必要的计算，因为它们即使 LLM 只是在某一个子任务上遇到困难，也要为整个任务探索多条轨迹或多次尝试。这类工作与 ADaPT 互补，可以并入规划器或执行器模块以增强 LLM 性能（正如它们被并入 ReAct 一样）。

#### 分解与模块化。

我们的工作遵循 NLP 中关于把任务分解为神经模块（Andreas et al., 2016；Gupta et al., 2019；Jiang and Bansal, 2019）或 seq2seq 模型（Min et al., 2019；Talmor and Berant, 2018；Khot et al., 2021；Perez et al., 2020；Saha et al., 2023b）的大量文献。随着少样本提示的黑盒 LLM 的出现，这种程序化分解为 LLM 的范式变得更加流行（Yao et al., 2023b；Khot et al., 2023；Wang et al., 2023b 等），被称为 LLM 程序（Schlag et al., 2023；Dohan et al., 2022）。此外，程序综合方面的过去工作（Murali et al., 2018；Nye et al., 2019；Zheng et al., 2023）也采用任务分解，即在程序生成前先生成「程序草图」。

ADaPT 不仅通过规划器模块分解任务并委托给执行器模块，还能在执行器失败时*自动*通过*按需*进一步分解复杂任务来适应。这种动态能力使 ADaPT 区别于先前具有非自适应结构的工作。ADaPT 扩展了 Khot et al. (2023) 的递归与层级分解，实现了模块间通信以及对执行失败的稳健策略，在在线购物等真实世界文本环境中表现出色。

#### 层级化问题求解。

在 AI 问题求解中，层级化任务分解在规划（Ghallab et al., 2004；Georgievski and Aiello, 2014；Höller et al., 2020）、强化学习（Sutton et al., 1999；Barto and Mahadevan, 2003；Nachum et al., 2018；Zhang et al., 2021）与导航（She et al., 2014；Sharma et al., 2022；Blukis et al., 2022；Min et al., 2022；Song et al., 2023）中有着悠久的传统。这些方法（如层级任务网络（Erol et al., 1994））利用领域知识（例如手工指定的计划库）把复杂问题拆成更简单的任务。我们的工作继承了这一传统，但通过探索 LLM 如何利用其广泛的世界知识自主分解任务而与众不同，无需预定义的计划库。最后，ADaPT 通过其递归结构执行动态层级规划。

## 3 方法

我们提出面向复杂任务的按需分解与规划（ADaPT），一种模块化的决策方法，把 LLM 作为*执行器*与*规划器*（第 3.1 与 3.2 节）集成到一个称为控制器（controller）的 LLM 程序中（第 3.3 节）。在图 1 中，当 ADaPT 收到一个复杂任务时，它首先通过迭代运行执行器尝试完成整个任务，若执行器失败则求助于 LLM 规划器进一步分解为子任务。随后，对每个子任务递归调用 ADaPT 以确保其成功完成，最终带来整体任务的成功。

![Refer to caption](2311.05772v2/overall.png)

图 2：
ADaPT 流水线的框图，附一个 ALFWorld 示例。左：将 LLM 用作执行器与环境迭代交互，附一条示例执行轨迹。中：嵌入执行器与规划器的整体递归算法（深度 $k\leq d_{\mathrm{max}}$），细节见算法 1。右：将 LLM 用作规划器生成子任务（步骤）以及组合它们的逻辑算子的示意。

### 3.1 LLM 作为执行器

#### 概述。

在给定环境中，执行器获得一个简洁的自然语言任务规范，如图 2（左）所示。遵循 Yao et al. (2023b)，执行器通过 LLM 生成的动作与环境迭代交互。这一交互持续到任务完成或达到预设的最大迭代次数上限。与 Ahn et al. (2022) 一致，我们为 LLM 提供环境特有的低层「原子」技能的上下文演示（列于附录 A 的表 5），例如知道如何在 ALFWorld 中正确加热物体。这一做法有两个优势：(i) 它使所有基线（第 4.2 节）都能使用同一个具备环境特定知识的执行器；(ii) 它使规划器（在第 3.2 节讨论）能在更高的抽象层次上工作，利用 LLM 的一般世界知识。

#### LLM 的执行能力。

至少，LLM 执行器应能可靠地执行原子技能。虽然我们提供了成功执行原子技能的演示，但 LLM 可以通过组合多个技能来适应失败、执行复杂任务，如第 6.2 节所讨论。例如，在图 2（左）中，我们展示 LLM 成功清洗它正携带的马克杯（一个原子技能）。一个先进的执行器可以把「找到马克杯」与「清洗」技能组合来完成「找一个干净马克杯」，而无需显式规划器。

#### 自生成成功启发式。

为了根据执行器的能力进行分解，我们需要判断执行器能否独立完成给定（子）任务，还是需要进一步分解。为此，我们让执行器 LLM 来判断（子）任务的完成情况，而*不依赖环境*获取（子）任务的金标准奖励。我们在执行器提示中加入一条简单指令：若它判定已成功则输出 *"task completed"*，否则若无法继续则输出 *"task failed"*。示例见图 2（左）。我们的成功启发式与 Shinn et al. (2023) 采用的二分类模型一致，提供了一种模拟中间奖励的方式，与任务结束时的环境奖励互补（Rengarajan et al., 2022）。我们在附录 F 中研究这一 LLM 生成的启发式，并表明它与金标准奖励高度吻合。

### 3.2 LLM 作为规划器

#### 概述。

规划器的目标是把复杂任务拆解成更小的子任务。为此，我们指示 LLM 生成一个简洁而全面的计划，由少数几步组成（通常 3-5 步），如图 2（右）所示。我们选择更短、更抽象的计划，因为期望一开始就给出详细、细粒度的计划并不现实，尤其是在未探索的环境中。例如，在不知道马克杯位置的情况下，为「把一个干净马克杯放到桌上」设计一个 10 步计划，可能因错误假设而引发级联错误。因此，我们让 LLM 生成短计划，并根据执行器的能力，在后续迭代中保留*进一步分解的灵活性*。

#### 子任务的组合逻辑。

除子任务外，我们还提示规划器生成逻辑算子，以组合计划中的各个子任务来完成该任务。我们允许两种逻辑算子：「And」与「Or」。当子任务必须顺序执行任务才能成功时，用 And 连接。而在需要探索的场景（如在未知房间中找到某物品），我们用 Or 算子模拟条件检查，此时只要任一子任务成功，任务即成功。例如在图 1 中，「*找到一个马克杯*」的计划可以是「*在台面上找到一个马克杯*」Or「*在柜子里找到一个马克杯*」。只有当智能体尚未找到马克杯时才执行后者。虽然图 1 与图 2 中的示例展示的是同质逻辑，ADaPT 可以处理附录 B 中描述的复杂逻辑表达式。

### 3.3 控制器——LLM 程序

#### 整体流水线。

到目前为止，我们描述了两个能分别承担低层执行与高层规划角色的 LLM 模块。我们通过控制器把这些模块纳入 ADaPT，控制器是一个预先确定的递归算法——使 ADaPT 的整体流水线成为一个 LLM 程序（Schlag et al., 2023；Dohan et al., 2022），见算法 1。控制器程序的总体流程如下：(i) 给定输入任务，控制器调用执行器检查它能否直接成功执行该任务；(ii) 若执行器未成功，控制器把分解复杂任务的工作委托给规划器，并对每个子任务递归调用 ADaPT，直到达到终止条件，即达到最大深度 $d_{\mathrm{max}}$（$\geq 1$）。

图 2（中）展示了 ADaPT 的控制流。一个诸如「把一个干净马克杯放到桌上」的复杂任务首先被分配给执行器。若执行器未成功，ADaPT 调用规划器把该任务分解为子任务，并附带一个逻辑算子（And 或 Or）说明如何组合它们。然后每个子任务（在图 2 中称为「step」）被递归地分配给 ADaPT，并用逻辑算子组合。最终，递归分解后各子任务的成功确保了整体任务的成功（规划器与执行器的展开调用见图 1）。

## 4 实验设置

我们描述实验所用的数据集以及与 ADaPT 对比的基线。

### 4.1 数据集

我们采用 LLM 智能体在以下三个环境中执行任务，并在第 5 与 6 节使用任务成功率作为评估指标。

#### ALFWorld。

ALFWorld（Shridhar et al., 2021）是具身 ALFRED 基准（Shridhar et al., 2020）的文本游戏版本，在 TextWorld 环境（Côté et al., 2019）中实现。它包含 6 种不同的任务类型，智能体需要在模拟家庭中通过基于文本的动作进行导航与交互来完成高层任务，环境会向智能体给出文本反馈（例如前文图 2 讨论的*把一个干净马克杯放到桌上*）。遵循 Shridhar et al. (2021)，我们在 134 个未见评测游戏（测试集）上报告结果，并从见过的评测游戏划分中为每类任务取 10 个游戏作为单独的开发集。除原子技能外，遵循 Yao et al. (2023b)，我们在执行器提示中为两个任务加入了金标准轨迹示例：加热与查看。3
注 3：与 Yao et al. (2023b) 不同，我们对所有 ALFWorld 任务使用统一的执行器提示，避免智能体预先知道任务类型。附录 C 的表 7 进一步表明，ADaPT 相对任务专属执行器仍有提升。

#### WebShop。

WebShop（Yao et al., 2022）是一个在线购物网站环境，收录 118 万件真实商品，测试集包含 500 条用户查询。它作为一个具有实际应用的复杂决策环境，智能体必须通过各种命令浏览网站，购买符合用户规格的商品（例如*价格低于 300 美元、快速配送的灰色组合沙发*）。遵循 Shinn et al. (2023)，我们在 100 条用户指令上报告性能，并使用另外 40 条查询的子集作为开发集。

#### TextCraft。

我们创建了一个新的纯文本环境，用于合成 Minecraft（注 4：<https://www.minecraft.net>）物品，类似于 WordCraft（Coenen et al., 2021）。与现有的智能体环境不同，TextCraft 中的任务呈现出自然的组合结构，类似包含复杂度各异步骤的烹饪食谱，其中一些子任务更繁琐（如给千层面分层），另一些则更简单（如烘烤）。

![Refer to caption](2311.05772v2/game.png)

图 3：TextCraft 中一个配方深度为 2 的任务的金标准轨迹示例。

| 方法（$d_{\mathrm{max}}=3$） | Pick | Clean | Heat | Cool | Look | Pick2 | All |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ReAct | 33.3 | 67.7 | 43.5 | 33.3 | 55.6 | 11.8 | 43.3 |
| Plan-and-Execute | 29.2 | 61.3 | 47.8 | 38.1 | 61.1 | 11.8 | 43.3 |
| Try Again with ReAct | 50.0 | 51.6 | 60.8 | 47.6 | 61.1 | 5.9 | 47.8 |
| Reflexion | 70.8 | 61.3 | 61.0 | 66.7 | 61.1 | 5.9 | 57.5 |
| ADaPT（本文） | 87.5 | 80.6 | 60.8 | 76.2 | 61.1 | 52.9 | 71.6 |

表 1：
在 ALFWorld（测试划分）上，ADaPT 相比先前工作的基线（在第 4.2 节讨论）取得最高的总体成功率（%）。最佳（最高）成功率以粗体标出，次高以下划线标出。

|  |  |  |
| --- | --- | --- |
| 方法 | WebShop | TextCraft |
| ReAct | 32.0 | 19.0 |
| Plan-and-Execute | 17.0 | 27.0 |
| Try Again with ReAct | 30.0 | 15.0 |
| Reflexion | 35.0† | 32.0 |
| LATS（Zhou et al., 2023） | 38.0† | − |
| ADaPT（本文） | 44.0 | 52.0 |

表 2：ADaPT 在 WebShop 与 TextCraft（测试划分）上以 $d_{\mathrm{max}}=3$ 与 4 分别取得最高成功率。†为 Zhou et al. (2023) 报告的性能。

TextCraft 中的任务天然可分解。在图 3 中，合成蜂箱需要先合成其原料（如木板与蜜脾），后者可能还需进一步分解。智能体因此需要识别并适应不同的任务复杂度，例如合成木板比合成蜂箱*更容易*。此外，一些配方允许使用某一类别中的任意物品。例如，合成蜂箱使用木板（一个类别），要求智能体运用语言知识正确选择物品（例如选择橡木木板，即木板类别中的一个具体物品）。我们在一个包含 200 个任务的测试集上评估我们的方法，目标物品的配方树深度分别为 2、3 与 4（深度为 2 的示例树见图 3）。我们在测试集中使用配方树深度为 3 的物品（123 个任务）、深度为 4 的物品（11 个任务）与深度为 2 的物品（297 个中的 77 个），其余深度为 2 的任务构成开发集。创建环境的更多细节见附录 E。

### 4.2 基线方法

我们将 ADaPT 与以下四类基线方法进行比较。

#### 仅迭代执行器（ReAct）。

在此设定中，我们采用执行器与环境迭代交互，沿用 ReAct（Yao et al., 2023b）的思考-行动-观察提示风格。下文讨论的所有方法（包括 ADaPT）共享*同一个*执行器，从而在比较第 5 节的相对性能时，确保执行器强度与设计选择的影响标准化。当 $d_{\mathrm{max}}=1$ 时，ADaPT 仅依赖该执行器。

#### 计划-执行。

如图 1 所示，在此设定中，我们先生成一个计划，然后把每个子任务分配给执行器。该方法只规划一次，因此具有非自适应结构（与 Wang et al. (2023b)；Yang et al. (2023)；Sun et al. (2023) 一致）。为确保每个计划步骤无需进一步分解即可执行，我们设计了包含更详细计划的新提示。注意，$d_{\mathrm{max}}=2$ 的 ADaPT 不同于计划-执行，因为它是自适应的，即只在执行器失败时分解，并生成相对更短的计划（参见附录 B）。

#### 用 ReAct 重试。

按设计，ADaPT 会多次调用执行器模块，只是每次面对的是不同的（子）任务。与 Yang et al. (2023) 类似，我们设计了一个简单的控制器，要求执行器在总共 $d_{\mathrm{max}}$ 次独立尝试中重试任务，然后对每个任务实例采用表现最好的那次尝试。

#### Reflexion。

Shinn et al. (2023) 先执行整个任务，若不成功，则反思并把反馈存入记忆，供后续 $d_{\mathrm{max}}-1$ 次尝试使用。虽然自适应，但即使只有一个子任务失败，该方法也会重复整个尝试，冗余地重新执行先前已成功的子任务。

#### ADaPT 与共享的实现细节。

遵循 Yao et al. (2023b)；Shinn et al. (2023)；Zhou et al. (2023)，默认情况下我们在 ADaPT 与其他基线中均使用 GPT-3.5（Ouyang et al., 2022）LLM 进行规划与执行。我们对 ALFWorld 与 TextCraft 使用补全式模型，对 WebShop 使用聊天式模型。5
注 5：我们使用补全模型，因为 GPT-3.5 的聊天变体一致地逊于其补全对应版本（Liu et al., 2023；Yang et al., 2023）。我们在第 6.2 节讨论 ADaPT 在不同 LLM 上的有效性。此外，我们对 ALFWorld 与 WebShop 使用 $d_{\mathrm{max}}=3$ 的 ADaPT（及其他基线），对 TextCraft 提高到 $d_{\mathrm{max}}=4$ 以容纳深度为 4 的配方（第 4.1 节）。更多细节见附录 A。我们将 ReAct 基线的最大迭代次数提高 $d_{\mathrm{max}}$ 倍，并确保所有基线使用可比数量的 LLM 调用（第 6.5 节）。

## 5 主要结果

以 GPT-3.5 作为底层 LLM，在本节中，我们表明 ADaPT 在 ALFWorld、WebShop 与 TextCraft 数据集上取得相比先前工作基线的最高成功率。

#### ALFWorld。

在表 2 中，我们观察到 ADaPT 取得*最高的总体成功率*，而仅用 ReAct 的总体表现最低。通过利用自适应分解，ADaPT 相对 ReAct 的性能提升 28.3 个（绝对）百分点，相对 Plan-and-Execute 与 Try Again 分别提升 28.3 与 23.8 个百分点。最后，我们发现 ADaPT 的总体成功率比 Reflexion 高 14.1 个百分点，尽管后者拥有专用记忆与自然语言反馈。具体而言，我们发现基线在「pick2」任务上结果不佳（成功率 <12%），因为这类任务要求智能体组合两个「pick」式任务，涉及更长的动作历史。而 ADaPT 在这类任务上取得显著提升（超过 4×）。

图 4：ADaPT 的成功率随最大深度 $d_{\mathrm{max}}$ 的增加而在所有数据集（开发划分）上提升。

#### WebShop。

表 2 展示了类似趋势，*ADaPT 超越所有基线*并取得最高成功率。ADaPT 胜过 ReAct、Plan-and-Execute 与 Try-Again 基线最多 27 个百分点。我们印证了 Shinn et al. (2023) 的发现，观察到自然语言反馈带来的性能提升有限，相比之下 ADaPT（超越 Reflexion 9 个百分点）。此外，我们与近期基于搜索的基线 LATS（Zhou et al., 2023）比较，发现 ADaPT 的成功率比 LATS 高 6 个百分点。

#### TextCraft。

我们在 TextCraft 上的结果总结于表 2。首先，我们观察到 ADaPT 相比 ReAct 执行器*取得 33% 的提升*。与 Plan-and-Execute（即从固定计划出发）相比，ADaPT 拥有适应复杂子任务（此处即合成复杂原料）的动态能力，性能提升 25 个百分点。最后，ADaPT 胜过 Reflexion 20 个百分点，凸显了自适应与按需规划的重要性。我们假设 ADaPT 在各数据集上一致超越 Reflexion，是因为后者依赖基于整个轨迹错误生成反馈。相比之下，凭借其设计，ADaPT 往往能处理小子任务的失败，并以调用规划器进行分解的形式把更多资源导向具有挑战性的子任务。

## 6 分析与讨论

我们通过在开发数据划分上回答以下研究问题，对 ADaPT 进行详细分析。

### 6.1 ADaPT 的性能如何随分解深度扩展？

#### 设置。

为评估自适应分解的影响，我们在对 ALFWorld、WebShop 与 TextCraft 的三种设定下研究 ADaPT，最大深度递增 $d_{\mathrm{max}}\in\{1,2,3\}$。注意 $d_{\mathrm{max}}=1$ 的设定对应仅迭代执行器基线（ReAct）。

#### 结果。

图 4 表明，在所有数据集上，ADaPT 的性能随最大深度 $d_{\mathrm{max}}$ 的增加而扩展。一致地，我们发现从 $d_{\mathrm{max}}=1$ 到 $d_{\mathrm{max}}=2$ 成功率显著提升，即在执行器失败时加入规划器分解复杂任务被证明是有效的。最后，从 $d_{\mathrm{max}}=2$ 到 $d_{\mathrm{max}}=3$ 的性能提升验证了我们的假设：一些子任务对 LLM 直接成功执行而言过于困难，进一步分解它们能提升整体性能。

### 6.2 ADaPT 能否适配不同的 LLM 执行能力？

图 5：ADaPT 在刻画不同执行器能力（即仅执行器性能）的多种设定下提升 ALFWorld（开发集）成功率。

图 6：ADaPT 提升 GPT-3.5、GPT-4、LLaMA 与 Lemur LLM 在各数据集上的（测试）性能。

#### 同一 LLM，不同执行能力。

我们在 ALFWorld 上以三种不同的执行器提示运行 ADaPT：(i) 任务专属金标准轨迹；(ii) 第 5 节使用的原子技能与 2 个任务的通用金标准轨迹（混合）；(iii) 仅原子技能。使用金标准轨迹与推理时的任务高度对齐，因此应表现出高性能。相反，仅使用原子技能的执行器依赖 LLM 固有的组合能力，性能较弱。我们在此考察 ADaPT 能否在全部三种设定下提升成功率。

#### 结果。

在图 5 中，我们观察到 ADaPT 在*所有多样的执行器设定*下均一致超越仅执行器基线。正如预期，以任务专属轨迹提示的执行器表现最好（左），仅原子技能的执行器表现最差（右）。值得注意的是，ADaPT 大幅提升了相对较弱的执行器的性能，把成功率从 3.3% 提高到 41.7%。

#### 使用不同 LLM 的 ADaPT。

我们研究 ADaPT 在不同 LLM（作为规划器与执行器）上提升性能的能力：(i) GPT-3.5；(ii) GPT-4（OpenAI, 2023）；(iii) LLaMA-2 70B（Touvron et al., 2023）；(iv) Lemur 70B（Xu et al., 2023），在所有数据集的测试划分上。

#### 结果。

图 6 表明，ADaPT 在*全部三个*数据集上对*所有*模型都一致提升下游性能。与 Liu et al. (2023) 一致，我们发现门控 GPT 模型在绝对成功率上胜过开源模型。尽管如此，ADaPT 对各种 LLM 都有效，将最强的 LLM GPT-4 的性能在 TextCraft 数据集上提升最多 37%，将表现最弱的 LLM LLaMA 提升最多 15%。

### 6.3 ADaPT 能否应对任务复杂度？

#### 设置。

凭借 TextCraft 的组合式设计，数据集中每个任务的复杂度可以用合成配方的深度来定义，即深度更高的配方更难合成。我们在 TextCraft 测试集上评估 ADaPT 与 ReAct 基线在配方深度递增时的有效性。6
注 6：由于深度为 4 的任务只有 11 个，我们将其排除在本分析之外。此外，虽然我们给 ADaPT 的最大预算为 $d_{\mathrm{max}}=4$，我们研究 ADaPT 成功所用的最大分解深度（$k_{\mathrm{max}}$）如何随任务复杂度变化。

| 方法 | 配方深度 | $\boldsymbol{k_{\mathrm{max}}}$ | 成功率 |
| --- | --- | --- | --- |
| ReAct | 2 | 1.0 | 26.9 |
| ADaPT（$d_{\mathrm{max}}=4$） | 2 | 1.9 | 78.2 |
| ReAct | 3 | 1.0 | 1.8 |
| ADaPT（$d_{\mathrm{max}}=4$） | 3 | 2.8 | 38.7 |

表 3：即使配方深度增加，ADaPT 仍提升 TextCraft（测试）性能。ADaPT 成功完成任务所用的最大分解深度（$k_{\mathrm{max}}$）也随配方深度扩展。

#### 结果。

在表 3 中，我们观察到相比 ReAct 基线，ADaPT 把配方深度为 2 的游戏成功率从 26.9% 提升到 78.2%，深度为 3 的从 1.8% 提升到 38.7%。正如预期，仅执行器无法应对深度 $\geq 3$ 的复杂配方，但在 ADaPT 的帮助下性能显著提升。此外，给定相同预算 $d_{\mathrm{max}}=4$，当配方深度（复杂度）从 2 增加到 3 时，ADaPT 的分解层级（$k_{\mathrm{max}}$）也从 1.9 提升到 2.8。这展示了 ADaPT 利用按需分解来应对任务复杂度。

### 6.4 我们能否在 ADaPT 内使用不同的规划器与执行器 LLM？

#### 设置。

ADaPT 的规划器与执行器模块不必使用相同的底层模型。遵循 Lin et al. (2023)，我们探索能否用相对较小的 LLM 在执行器中执行局部动作，而用更先进的 LLM 制定计划。为此，我们在 ALFWorld 上探索规划器与执行器 LLM 的不同组合，后者同时使用门控与开源模型。

#### 结果。

表 4 表明，ADaPT 可以成功地用一个 LLM 生成对另一个（可能更小的）执行器 LLM 有用的计划，相比仅执行器（ReAct）设定，成功率提升最多 19.9%。有趣的是，使用开源模型（如 LLaMA-2-70B-chat（Touvron et al., 2023））作为执行器、配合 GPT-3.5 等更先进的 LLM，可将成功率提升 22.9 个百分点。由于规划器 LLM 的使用频率较低，开源执行器可以大幅降低使用 ADaPT 的货币或计算成本。我们将更强与更弱 LM 的知识在 ADaPT 内的结合留作未来工作，如数学推理语境下所考察的（Fu et al., 2023；Saha et al., 2023a）。

| 执行器 LM | 规划器 LM | 成功率 |
| --- | --- | --- |
| GPT-3.5 | − | 38.4 |
| GPT-3.5 | GPT-3.5 | 58.3 |
| LLaMA-2-70B | − | 20.4 |
| LLaMA-2-70B | GPT-3.5 | 43.3 |

表 4：使用不同规划器与执行器 LLM 时，ADaPT 提升 ALFWorld（开发集）性能。

### 6.5 在 LLM 调用次数上，ADaPT 与基线相比如何？

#### 设置。

决策智能体的性能可以通过增加允许的 LLM 调用次数来增强，例如 Reflexion 的重试次数。为验证 ADaPT 的增益并非单纯来自更多的 LLM 调用，我们比较 ADaPT 与基线的平均 LLM 调用次数。

图 7：包括 ADaPT 与第 4.2 节讨论的基线在内的每种方法使用 GPT-3.5 LLM 在各数据集上的平均 LLM 调用次数。

#### 结果。

图 7 表明，ADaPT 使用的 LLM 调用次数与 Try-Again 及 Reflexion 基线相当，同时取得了第 5 节讨论的性能提升（表 2）。注意，虽然包括 ReAct 与 Plan-and-Execute 基线在内的所有方法都被提供了可比的计算预算，但后者实际使用的 LLM 调用次数往往更低，因为它们无法处理中间执行失败。这强化了 ADaPT 有效性论证——其提升并非仅仅源于对 LLM 的调用次数大幅增加。

## 7 结论

我们提出 ADaPT，一种旨在利用 LLM 规划能力的递归算法，在作为执行器的 LLM 遇到挑战时动态分解复杂任务。我们在 ALFWorld、WebShop 与 TextCraft 三个多样的决策任务上的评估揭示了 ADaPT 的出色性能，分别以最多 28.3%、27% 与 33% 个百分点的幅度超越现有基线。这不仅凸显了 ADaPT 的有效性，也突显了按需分解对提升任务性能的意义。此外，我们的发现表明，ADaPT 不仅适应底层执行器 LLM 的能力，还考虑单个任务实例的复杂度，展示了其多功能性与有效性。

## 致谢

本工作的一部分在 AI2 实习期间完成，在 UNC 的部分受到 NSF-CAREER Award 1846185、NSF-AI Engage Institute DRL-2112635、DARPA Machine Commonsense (MCS) Grant N66001-19-2-4031 的部分支持。我们衷心感谢 Bodhisattwa Prasad Majumder、Chris Callison-Burch、Shashank Gupta、Peter Jansen、Bill Yuchen Lin 以及 Aristo 团队的宝贵反馈。我们还感谢 Swarnadeep Saha、Elias Stengel-Eskin 与 Peter Hase 的反馈。

## 局限性

ADaPT 依赖执行器 LLM 生成的成功启发式来判断模型能否执行复杂任务。对于本工作研究的决策任务，我们发现 LLM 能够基于过去的动作轨迹与环境的文本反馈可靠地判断任务成功（见附录 F）。然而，Huang et al. (2023a)；Stechly et al. (2023) 讨论了 LLM 自我评估与自我精炼能力的局限。在这些情况下，未来工作可以额外采用外部验证器（Lightman et al., 2023；Shridhar et al., 2023）、多个 LM 间的心智理论策略（Saha et al., 2023a），以及其他校准与自我评估技术（Kadavath et al., 2022）。这些改进的自我评估技术可能有助于把我们的框架扩展到问答等非决策任务。

## 参考文献

- Ahn et al. (2022)

  Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Chuyuan Fu, Keerthana Gopalakrishnan, Karol Hausman, et al. 2022.
  Do as i can, not as i say: Grounding language in robotic affordances.
  *arXiv preprint arXiv:2204.01691*.
- Andreas et al. (2016)

  Jacob Andreas, Marcus Rohrbach, Trevor Darrell, and Dan Klein. 2016.
  Neural module networks.
  In *Proceedings of the IEEE conference on computer vision and pattern recognition*, pages 39–48.
- Barto and Mahadevan (2003)

  Andrew G Barto and Sridhar Mahadevan. 2003.
  Recent advances in hierarchical reinforcement learning.
  *Discrete event dynamic systems*, 13(1-2):41–77.
- Blukis et al. (2022)

  Valts Blukis, Chris Paxton, Dieter Fox, Animesh Garg, and Yoav Artzi. 2022.
  A persistent spatial semantic representation for high-level natural language instruction execution.
  In *Conference on Robot Learning*, pages 706–717. PMLR.
- Coenen et al. (2021)

  Andy Coenen, Luke Davis, Daphne Ippolito, Emily Reif, and Ann Yuan. 2021.
  Wordcraft: a human-ai collaborative editor for story writing.
  *arXiv preprint arXiv:2107.07430*.
- Côté et al. (2019)

  Marc-Alexandre Côté, Akos Kádár, Xingdi Yuan, Ben Kybartas, Tavian Barnes, Emery Fine, James Moore, Matthew Hausknecht, Layla El Asri, Mahmoud Adada, et al. 2019.
  Textworld: A learning environment for text-based games.
  In *Computer Games: 7th Workshop, CGW 2018, Held in Conjunction with the 27th International Conference on Artificial Intelligence, IJCAI 2018, Stockholm, Sweden, July 13, 2018, Revised Selected Papers 7*, pages 41–75. Springer.
- Dohan et al. (2022)

  David Dohan, Winnie Xu, Aitor Lewkowycz, Jacob Austin, David Bieber, Raphael Gontijo Lopes, Yuhuai Wu, Henryk Michalewski, Rif A Saurous, Jascha Sohl-Dickstein, et al. 2022.
  Language model cascades.
  *arXiv preprint arXiv:2207.10342*.
- Dziri et al. (2023)

  Nouha Dziri, Ximing Lu, Melanie Sclar, Xiang Lorraine Li, Liwei Jian, Bill Yuchen Lin, Peter West, Chandra Bhagavatula, Ronan Le Bras, Jena D Hwang, et al. 2023.
  Faith and fate: Limits of transformers on compositionality.
  *arXiv preprint arXiv:2305.18654*.
- Erol et al. (1994)

  Kutluhan Erol, James Hendler, and Dana S Nau. 1994.
  Htn planning: Complexity and expressivity.
  In *AAAI*, volume 94, pages 1123–1128.
- Fan et al. (2022)

  Linxi Fan, Guanzhi Wang, Yunfan Jiang, Ajay Mandlekar, Yuncong Yang, Haoyi Zhu, Andrew Tang, De-An Huang, Yuke Zhu, and Anima Anandkumar. 2022.
  Minedojo: Building open-ended embodied agents with internet-scale knowledge.
  *Advances in Neural Information Processing Systems*, 35:18343–18362.
- Fu et al. (2023)

  Yao Fu, Hao Peng, Litu Ou, Ashish Sabharwal, and Tushar Khot. 2023.
  Specializing smaller language models towards multi-step reasoning.
  *arXiv preprint arXiv:2301.12726*.
- Georgievski and Aiello (2014)

  Ilche Georgievski and Marco Aiello. 2014.
  An overview of hierarchical task network planning.
  *arXiv preprint arXiv:1403.7426*.
- Ghallab et al. (2004)

  Malik Ghallab, Dana Nau, and Paolo Traverso. 2004.
  *Automated Planning: theory and practice*.
  Elsevier.
- Gupta et al. (2019)

  Nitish Gupta, Kevin Lin, Dan Roth, Sameer Singh, and Matt Gardner. 2019.
  Neural module networks for reasoning over text.
  In *International Conference on Learning Representations*.
- Höller et al. (2020)

  Daniel Höller, Gregor Behnke, Pascal Bercher, Susanne Biundo, Humbert Fiorino, Damien Pellier, and Ron Alford. 2020.
  Hddl: An extension to pddl for expressing hierarchical planning problems.
  In *Proceedings of the AAAI conference on artificial intelligence*, pages 9883–9891.
- Huang and Chang (2023)

  Jie Huang and Kevin Chen-Chuan Chang. 2023.
  [Towards reasoning in large language models: A survey](https://doi.org/10.18653/v1/2023.findings-acl.67).
  In *Findings of the Association for Computational Linguistics: ACL 2023*, pages 1049–1065, Toronto, Canada. Association for Computational Linguistics.
- Huang et al. (2023a)

  Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny Zhou. 2023a.
  Large language models cannot self-correct reasoning yet.
  *arXiv preprint arXiv:2310.01798*.
- Huang et al. (2023b)

  Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, et al. 2023b.
  Inner monologue: Embodied reasoning through planning with language models.
  In *Conference on Robot Learning*, pages 1769–1782. PMLR.
- Jiang and Bansal (2019)

  Yichen Jiang and Mohit Bansal. 2019.
  [Self-assembling modular networks for interpretable multi-hop reasoning](https://doi.org/10.18653/v1/D19-1455).
  In *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP)*, pages 4474–4484, Hong Kong, China. Association for Computational Linguistics.
- Kadavath et al. (2022)

  Saurav Kadavath, Tom Conerly, Amanda Askell, Tom Henighan, Dawn Drain, Ethan Perez, Nicholas Schiefer, Zac Hatfield-Dodds, Nova DasSarma, Eli Tran-Johnson, et al. 2022.
  Language models (mostly) know what they know.
  *arXiv preprint arXiv:2207.05221*.
- Khot et al. (2021)

  Tushar Khot, Daniel Khashabi, Kyle Richardson, Peter Clark, and Ashish Sabharwal. 2021.
  [Text modular networks: Learning to decompose tasks in the language of existing models](https://doi.org/10.18653/v1/2021.naacl-main.99).
  In *Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies*, pages 1264–1279, Online. Association for Computational Linguistics.
- Khot et al. (2023)

  Tushar Khot, Harsh Trivedi, Matthew Finlayson, Yao Fu, Kyle Richardson, Peter Clark, and Ashish Sabharwal. 2023.
  [Decomposed prompting: A modular approach for solving complex tasks](https://openreview.net/forum?id=_nGgzQjzaRy).
  In *The Eleventh International Conference on Learning Representations*.
- Lightman et al. (2023)

  Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe. 2023.
  Let's verify step by step.
  *arXiv preprint arXiv:2305.20050*.
- Lin et al. (2023)

  Bill Yuchen Lin, Yicheng Fu, Karina Yang, Prithviraj Ammanabrolu, Faeze Brahman, Shiyu Huang, Chandra Bhagavatula, Yejin Choi, and Xiang Ren. 2023.
  Swiftsage: A generative agent with fast and slow thinking for complex interactive tasks.
  *arXiv preprint arXiv:2305.17390*.
- Liu et al. (2023)

  Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan Yang, et al. 2023.
  Agentbench: Evaluating llms as agents.
  *arXiv preprint arXiv:2308.03688*.
- Madaan et al. (2023)

  Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, et al. 2023.
  Self-refine: Iterative refinement with self-feedback.
  *arXiv preprint arXiv:2303.17651*.
- Min et al. (2019)

  Sewon Min, Victor Zhong, Luke Zettlemoyer, and Hannaneh Hajishirzi. 2019.
  [Multi-hop reading comprehension through question decomposition and rescoring](https://doi.org/10.18653/v1/P19-1613).
  In *Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics*, pages 6097–6109, Florence, Italy. Association for Computational Linguistics.
- Min et al. (2022)

  So Yeon Min, Devendra Singh Chaplot, Pradeep Kumar Ravikumar, Yonatan Bisk, and Ruslan Salakhutdinov. 2022.
  Film: Following instructions in language with modular methods.
  In *International Conference on Learning Representations*.
- Murali et al. (2018)

  Vijayaraghavan Murali, Letao Qi, Swarat Chaudhuri, and Chris Jermaine. 2018.
  [Neural sketch learning for conditional program generation](https://openreview.net/forum?id=HkfXMz-Ab).
  In *International Conference on Learning Representations*.
- Nachum et al. (2018)

  Ofir Nachum, Shixiang Shane Gu, Honglak Lee, and Sergey Levine. 2018.
  Data-efficient hierarchical reinforcement learning.
  *Advances in neural information processing systems*, 31.
- Nye et al. (2019)

  Maxwell Nye, Luke Hewitt, Joshua Tenenbaum, and Armando Solar-Lezama. 2019.
  Learning to infer program sketches.
  In *International Conference on Machine Learning*, pages 4861–4870. PMLR.
- OpenAI (2023)

  OpenAI. 2023.
  [Gpt-4 technical report](http://arxiv.org/abs/2303.08774).
- Ouyang et al. (2022)

  Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. 2022.
  Training language models to follow instructions with human feedback.
  *Advances in Neural Information Processing Systems*, 35:27730–27744.
- Perez et al. (2020)

  Ethan Perez, Patrick Lewis, Wen-tau Yih, Kyunghyun Cho, and Douwe Kiela. 2020.
  [Unsupervised question decomposition for question answering](https://doi.org/10.18653/v1/2020.emnlp-main.713).
  In *Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)*, pages 8864–8880, Online. Association for Computational Linguistics.
- Qin et al. (2023)

  Yujia Qin, Shihao Liang, Yining Ye, Kunlun Zhu, Lan Yan, Yaxi Lu, Yankai Lin, Xin Cong, Xiangru Tang, Bill Qian, et al. 2023.
  Toolllm: Facilitating large language models to master 16000+ real-world apis.
  *arXiv preprint arXiv:2307.16789*.
- Rengarajan et al. (2022)

  Desik Rengarajan, Gargi Vaidya, Akshay Sarvesh, Dileep Kalathil, and Srinivas Shakkottai. 2022.
  [Reinforcement learning with sparse rewards using guidance from offline demonstration](https://openreview.net/forum?id=YJ1WzgMVsMt).
  In *International Conference on Learning Representations*.
- Saha et al. (2023a)

  Swarnadeep Saha, Peter Hase, and Mohit Bansal. 2023a.
  Can language models teach weaker agents? teacher explanations improve students via theory of mind.
  *arXiv preprint arXiv:2306.09299*.
- Saha et al. (2023b)

  Swarnadeep Saha, Shiyue Zhang, Peter Hase, and Mohit Bansal. 2023b.
  [Summarization programs: Interpretable abstractive summarization with neural modular trees](https://openreview.net/forum?id=ooxDOe7ZtBe).
  In *The Eleventh International Conference on Learning Representations*.
- Schlag et al. (2023)

  Imanol Schlag, Sainbayar Sukhbaatar, Asli Celikyilmaz, Wen-tau Yih, Jason Weston, Jürgen Schmidhuber, and Xian Li. 2023.
  Large language model programs.
  *arXiv preprint arXiv:2305.05364*.
- Sharma et al. (2022)

  Pratyusha Sharma, Antonio Torralba, and Jacob Andreas. 2022.
  [Skill induction and planning with latent language](https://doi.org/10.18653/v1/2022.acl-long.120).
  In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 1713–1726, Dublin, Ireland. Association for Computational Linguistics.
- She et al. (2014)

  Lanbo She, Shaohua Yang, Yu Cheng, Yunyi Jia, Joyce Chai, and Ning Xi. 2014.
  Back to the blocks world: Learning new actions through situated human-robot dialogue.
  In *Proceedings of the 15th annual meeting of the special interest group on discourse and dialogue (SIGDIAL)*, pages 89–97.
- Shi et al. (2023)

  Freda Shi, Xinyun Chen, Kanishka Misra, Nathan Scales, David Dohan, Ed Huai hsin Chi, Nathanael Scharli, and Denny Zhou. 2023.
  [Large language models can be easily distracted by irrelevant context](https://api.semanticscholar.org/CorpusID:256459776).
  In *International Conference on Machine Learning*.
- Shinn et al. (2023)

  Noah Shinn, Federico Cassano, Beck Labash, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. 2023.
  Reflexion: Language agents with verbal reinforcement learning.
  *arXiv preprint arXiv:2303.11366*, 14.
- Shridhar et al. (2023)

  Kumar Shridhar, Koustuv Sinha, Andrew Cohen, Tianlu Wang, Ping Yu, Ram Pasunuru, Mrinmaya Sachan, Jason Weston, and Asli Celikyilmaz. 2023.
  The art of llm refinement: Ask, refine, and trust.
  *arXiv preprint arXiv:2311.07961*.
- Shridhar et al. (2020)

  Mohit Shridhar, Jesse Thomason, Daniel Gordon, Yonatan Bisk, Winson Han, Roozbeh Mottaghi, Luke Zettlemoyer, and Dieter Fox. 2020.
  Alfred: A benchmark for interpreting grounded instructions for everyday tasks.
  In *Proceedings of the IEEE/CVF conference on computer vision and pattern recognition*, pages 10740–10749.
- Shridhar et al. (2021)

  Mohit Shridhar, Xingdi Yuan, Marc-Alexandre Côté, Yonatan Bisk, Adam Trischler, and Matthew Hausknecht. 2021.
  [ALFWorld: Aligning Text and Embodied Environments for Interactive Learning](https://arxiv.org/abs/2010.03768).
  In *Proceedings of the International Conference on Learning Representations (ICLR)*.
- Singh et al. (2023)

  Ishika Singh, Valts Blukis, Arsalan Mousavian, Ankit Goyal, Danfei Xu, Jonathan Tremblay, Dieter Fox, Jesse Thomason, and Animesh Garg. 2023.
  Progprompt: Generating situated robot task plans using large language models.
  In *2023 IEEE International Conference on Robotics and Automation (ICRA)*, pages 11523–11530. IEEE.
- Song et al. (2023)

  Chan Hee Song, Jiaman Wu, Clayton Washington, Brian M Sadler, Wei-Lun Chao, and Yu Su. 2023.
  Llm-planner: Few-shot grounded planning for embodied agents with large language models.
  In *Proceedings of the IEEE/CVF International Conference on Computer Vision*, pages 2998–3009.
- Stechly et al. (2023)

  Kaya Stechly, Matthew Marquez, and Subbarao Kambhampati. 2023.
  Gpt-4 doesn't know it's wrong: An analysis of iterative prompting for reasoning problems.
  *arXiv preprint arXiv:2310.12397*.
- Sun et al. (2023)

  Simeng Sun, Y. Liu, Shuo Wang, Chenguang Zhu, and Mohit Iyyer. 2023.
  [Pearl: Prompting large language models to plan and execute actions over long documents](https://api.semanticscholar.org/CorpusID:258866190).
  *ArXiv*, abs/2305.14564.
- Sutton et al. (1999)

  Richard S Sutton, Doina Precup, and Satinder Singh. 1999.
  Between mdps and semi-mdps: A framework for temporal abstraction in reinforcement learning.
  *Artificial intelligence*, 112(1-2):181–211.
- Talmor and Berant (2018)

  Alon Talmor and Jonathan Berant. 2018.
  [The web as a knowledge-base for answering complex questions](https://doi.org/10.18653/v1/N18-1059).
  In *Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long Papers)*, pages 641–651, New Orleans, Louisiana. Association for Computational Linguistics.
- Touvron et al. (2023)

  Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. 2023.
  Llama 2: Open foundation and fine-tuned chat models.
  *arXiv preprint arXiv:2307.09288*.
- Wang et al. (2023a)

  Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar. 2023a.
  Voyager: An open-ended embodied agent with large language models.
  *arXiv preprint arXiv:2305.16291*.
- Wang et al. (2023b)

  Lei Wang, Wanyu Xu, Yihuai Lan, Zhiqiang Hu, Yunshi Lan, Roy Ka-Wei Lee, and Ee-Peng Lim. 2023b.
  [Plan-and-solve prompting: Improving zero-shot chain-of-thought reasoning by large language models](https://doi.org/10.18653/v1/2023.acl-long.147).
  In *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 2609–2634, Toronto, Canada. Association for Computational Linguistics.
- Wei et al. (2022)

  Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al. 2022.
  Chain-of-thought prompting elicits reasoning in large language models.
  *Advances in Neural Information Processing Systems*, 35:24824–24837.
- Wolf et al. (2019)

  Thomas Wolf, Lysandre Debut, Victor Sanh, Julien Chaumond, Clement Delangue, Anthony Moi, Pierric Cistac, Tim Rault, Rémi Louf, Morgan Funtowicz, et al. 2019.
  Huggingface's transformers: State-of-the-art natural language processing.
  *arXiv preprint arXiv:1910.03771*.
- Xu et al. (2023)

  Yiheng Xu, Hongjin Su, Chen Xing, Boyu Mi, Qian Liu, Weijia Shi, Binyuan Hui, Fan Zhou, Yitao Liu, Tianbao Xie, Zhoujun Cheng, Siheng Zhao, Lingpeng Kong, Bailin Wang, Caiming Xiong, and Tao Yu. 2023.
  [Lemur: Harmonizing natural language and code for language agents](http://arxiv.org/abs/2310.06830).
- Yang et al. (2023)

  John Yang, Akshara Prabhakar, Karthik Narasimhan, and Shunyu Yao. 2023.
  Intercode: Standardizing and benchmarking interactive coding with execution feedback.
  *arXiv preprint arXiv:2306.14898*.
- Yao et al. (2022)

  Shunyu Yao, Howard Chen, John Yang, and Karthik Narasimhan. 2022.
  Webshop: Towards scalable real-world web interaction with grounded language agents.
  *Advances in Neural Information Processing Systems*, 35:20744–20757.
- Yao et al. (2023a)

  Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L Griffiths, Yuan Cao, and Karthik Narasimhan. 2023a.
  Tree of thoughts: Deliberate problem solving with large language models.
  *arXiv preprint arXiv:2305.10601*.
- Yao et al. (2023b)

  Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and Yuan Cao. 2023b.
  [React: Synergizing reasoning and acting in language models](https://openreview.net/forum?id=WE_vluYUL-X).
  In *The Eleventh International Conference on Learning Representations*.
- Zhang et al. (2021)

  Jesse Zhang, Haonan Yu, and Wei Xu. 2021.
  Hierarchical reinforcement learning by discovering intrinsic options.
  In *International Conference on Learning Representations*.
- Zheng et al. (2023)

  Wenqing Zheng, SP Sharan, Ajay Kumar Jaiswal, Kevin Wang, Yihan Xi, Dejia Xu, and Zhangyang Wang. 2023.
  Outline, then details: Syntactically guided coarse-to-fine code generation.
  In *International Conference on Machine Learning*, pages 42403–42419. PMLR.
- Zhou et al. (2023)

  Andy Zhou, Kai Yan, Michal Shlapentokh-Rothman, Haohan Wang, and Yu-Xiong Wang. 2023.
  Language agent tree search unifies reasoning acting and planning in language models.
  *arXiv preprint arXiv:2310.04406*.

## 附录 A ADaPT 实现细节

|  | 原子技能 | 描述 |
| --- | --- | --- |
| ALFWorld | put | 假设机器人正携带一个物体，将其放到给定收纳位置上。 |
| take | 从指定收纳位置取走指定物体。 |
| clean/heat/cool | 假设机器人正携带一个物体，对该物体进行清洗/加热/冷却。 |
| examine | 假设机器人在一个有台灯的书桌旁，使用台灯查看一个物体。 |
| WebShop | search | 在搜索框中输入给定查询，返回一个包含商品列表的页面。 |
| shortlist | 基于搜索页面与查询，获取任何匹配商品的列表。 |
| match | 给定商品 ID 与查询，导航到商品页面并验证其匹配查询。 |
| buy | 给定商品 ID 与查询，通过选择相关选项购买商品。 |
| TextCraft | craft | 假设智能体库存中已有全部原料，从合成命令列表中选择合适的命令来合成目标物品。 |
| fetch | 在库存中寻找给定物体，或直接从环境中获取它。 |
| inventory | 查看游戏库存。 |

表 5：第 3.1 节所用原子技能概览。

#### 执行器。

我们对每个数据集使用一个通用的 ReAct 执行器。为此，我们在执行器中为 LLM 提供每个原子技能的上下文示例轨迹（完整列表见表 5）。原子技能本质上依赖于任务，因此随底层环境而变化。对于 ALFWorld（智能体需要在家庭中导航并执行任务），原子技能包括：拿取物体、把它放到某处、清洗、加热等。另一方面，WebShop 的目标是根据用户查询购买商品，因此原子技能包括：搜索指定查询、基于搜索页面筛选商品、检查商品是否满足条件、以及购买商品。最后，TextCraft 的原子技能是从环境中获取物体，以及在给定配方与原料的情况下合成它们。遵循 Yao et al. (2023b)，我们在 ALFWorld 的执行器提示中为两个任务（加热与查看）加入金标准轨迹，并为 TextCraft 加入一条完整的金标准轨迹。

#### 规划器。

我们为 LLM 提供原子技能的简要描述以及每个数据集的少量任务分解上下文演示。

- ALFWorld：规划器包含针对一个家庭配置的 6 个任务分解演示。具体而言，*「find」*不是执行器的原子技能，因此需要由规划器处理（参见图 2）。
- WebShop：规划器通过 2 个上下文演示，把给定任务按表 5 描述的原子技能拆解。
- TextCraft：规划器判断每件物品所需的原料，并制定获取原料再合成该物品的计划，通过 2 个使用不同合成命令的示例加以说明。

| 方法 | Pick | Clean | Heat | Cool | Look | Pick2 | All |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ReAct | 66.7 | 41.9 | 47.8 | 80.9 | 83.3 | 23.5 | 56.7 |
| Plan-and-Execute | 87.5 | 58.1 | 73.9 | 52.4 | 83.3 | 17.6 | 63.4 |
| Try Again with ReAct | 75.0 | 38.7 | 60.9 | 76.2 | 66.7 | 23.5 | 56.7 |
| Reflexion | 83.3 | 61.3 | 73.9 | 85.7 | 61.1 | 29.4 | 67.2 |
| ADaPT（本文） | 91.7 | 67.7 | 78.3 | 81.0 | 100 | 64.7 | 79.8 |

表 6：在 ALFWorld（测试划分）上，ADaPT 与其他先前工作基线使用 Yao et al. (2023b) 的执行器所取得的成功率（%）比较。

| 方法 | 分数 | 成功率 |
| --- | --- | --- |
| 仅迭代执行器 | 42.1 | 29.0 |
| 静态分解 | 27.7 | 17.0 |
| 重试执行 | 45.4 | 30.0 |
| 朴素 | 58.3 | 24.0 |
| Reflexion* | 64.2 | 35.0 |
| LATS（Zhou et al., 2023）* | 75.9 | 38.0 |
| ADaPT（本文） | 60.0 | 44.0 |

表 7：WebShop 上不同方法的性能比较。

1:

function ADaPT(Task $T$, Current depth $k$)

2:

　

// ADaPT$(\cdot)$ 为任务 $T$ 生成成功启发式值 $completed$。初始化时 $k=1$。

3:

　

// 基例：达到最大深度时终止

4:

　

if $k>d_{\mathrm{max}}$ then return $False$

5:

　

// 执行任务/子任务，以 LLM 生成的 $success$ 评估 LLM 能否直接完成它。

6:

　

$completed\leftarrow\boldsymbol{\mathrm{executor}_{\textsc{llm}}}(T)$

7:

　

// 只在执行器失败时规划。

8:

　

if $completed\text{ is }False$ then

9:

　　

// 使用 LLM 把任务分解为子任务集合 $\mathcal{P}$，以及一个组合子任务输出的布尔函数 $logic(\cdot)$。

10:

　　

$\mathcal{P},logic\leftarrow\boldsymbol{\mathrm{planner}_{\textsc{llm}}}(T)$

11:

　　

// 获取各子任务的输出

12:

　　

$\mathcal{O}=\{\textbf{{ADaPT}{}}(T_{\mathrm{sub}},k+1)|{T_{\mathrm{sub}}\in\mathcal{P}}\}$

13:

　　

// 组合各子任务的输出

14:

　　

$completed\leftarrow logic(\mathcal{O})$

15:

　

return $completed$

算法 1　ADaPT 算法

#### 控制器。

控制器在 ADaPT 的整体运行中扮演两个关键角色。首先，它充当规划器与执行器之间的*通信桥梁*，根据任务在两者之间传播显著信息。其次，由于 ADaPT 是递归算法，控制器利用来自规划器的逻辑表达式与来自执行器的成功启发式，或在达到最大深度 $d_{\mathrm{max}}$（$\geq 1$）时，决定*终止条件*。控制器传播的依赖任务的信息如下所述：

- ALFWorld：在控制器中，我们把上一次执行运行中最后一个成功的动作传播给后续的执行器调用。注意，信息只从成功的子任务传播。对于通过「Or」连接的子任务，每个都从控制器接收相同的信息。与 Shinn et al. (2023) 不同，执行器不会获得先前失败的文本反馈。
- WebShop：我们把智能体当前可见的页面连同先前未成功的执行器任务（不带任何理由说明）传播给规划器。一旦找到匹配商品，我们还在未来的执行器调用中传播该商品 ID。
- TextCraft：我们把智能体的当前库存传播给执行器。这类似于执行器以 inventory 命令作为第一步开始，以掌握哪些物品缺失、需要获取或合成。

ADaPT 的部分展开轨迹见图 9、图 10 与图 11。规划器与执行器之间的通信以灰色框突出显示。

#### LLM 相关超参数。

遵循先前工作（Shinn et al., 2023；Liu et al., 2023），我们对 ALFWorld 使用 OpenAI API 的 text-davinci-003。对 WebShop，我们使用 gpt-3.5-turbo 模型；对 TextCraft，我们使用 gpt-3.5-turbo-instruct 模型。所有执行器都有与环境交互并执行任务的最大迭代预算。我们对 ALFWorld、WebShop 与 TextCraft 分别将该预算设为 20、15 与 20。对于用 ReAct 重试，我们以 0.7 的温度采样额外轨迹。如第 4.2 节所讨论，我们对 ALFWorld、WebShop 与 TextCraft 分别以 60、45、60 次迭代运行仅迭代执行器基线。在第 6.2 节中，我们使用 Huggingface（Wolf et al., 2019）上公开可用的 LLaMA 70B（注 7：<https://huggingface.co/meta-llama/Llama-2-70b-hf>）与 Lemur 70B（注 8：<https://huggingface.co/OpenLemur/lemur-70b-chat-v1>）检查点。对于规划器与执行器模块，我们对每个数据集使用由少量上下文示例（如上所述）组成的固定提示。我们在附录 G 中展示给 LLM 的所有执行器与规划器提示。由于成本限制，我们在第 5 与 6 节中报告每个 LLM 单次运行的成功率。

图 8：示意 ADaPT 的多级计划如何在非自适应设定（如计划-执行基线所用，第 4.2 节）中坍缩为一份详细计划。我们的控制器可以处理复杂的（非同质）逻辑表达式。

## 附录 B 处理计划中的复杂逻辑

虽然图 1 与图 2 中的示例展示的是计划中子任务间的同质逻辑，我们的控制器可以处理包含「And」与「Or」两种算子的复杂逻辑表达式。具体而言，我们指示规划器在计划末尾以固定前缀「Execution Order」输出该逻辑表达式。然后我们构建一个确定性解析器，能够解析控制器可以处理的复杂逻辑表达式。我们通过把逻辑表达式拆分为一系列同质表达式、每个传给 ADaPT 来实现。每当交给 ADaPT 的任务包含由（单一）逻辑算子连接的多个子任务时，我们会按该逻辑表达式自动分解此任务。例如在图 8 中，计划-执行基线（在第 4.2 节讨论）所用的详细计划包含同时使用 And 与 Or 算子的逻辑表达式。因此，解析器会自动把它拆成多个层级，即 Step 6 == Step 1 Or Step 2 Or Step 3，随后 Step 6 And Step 4 And Step 5。虽然这样的复杂逻辑表达式大多与计划-执行基线相关，它们也可以轻松用于 ADaPT 框架内。此外，这使计划-执行基线能够通过详细计划模拟多级规划结构，而无需对执行器自适应。

![Refer to caption](2311.05772v2/react_vs_adapt.png)

图 9：ReAct 等迭代执行器与 ADaPT 的比较。左侧，ReAct 使用交错的「thought」语句设定里程碑并跟踪进度。然而，由于动作历史过长，它难以严格遵循计划并幻觉出错误物体（红色高亮）。右侧的 ADaPT 在执行器失败时把复杂任务分解为更小的子任务，从而得到更短、更易执行的动作轨迹。

![Refer to caption](2311.05772v2/web_roll.png)

图 10：WebShop 上 ADaPT 的部分展开轨迹。在灰色框中，我们向规划器传达智能体当前可见的（搜索）页面，一旦找到匹配商品，我们将其传播到未来的执行器运行。注意「match on search page」对应表 5 中的 shortlist 技能，「detail match on product page」对应 match 技能。

![Refer to caption](2311.05772v2/text_roll.png)

图 11：TextCraft 上使用 ADaPT 的部分展开轨迹。在灰色框中，我们把智能体的库存传播给后续执行器调用。注意「diorite」并不直接存在于环境中，即它需要被合成。执行器 LLM 能够固有地组合技能来获取它，而无需进一步分解。

## 附录 C ALFWorld 中的任务专属执行器

在表 2 中，我们使用了一个带原子技能上下文演示与两条金标准轨迹的标准化执行器。虽然这允许不同子任务共享一个通用执行器，任务专属执行器在特定子任务上会取得更高性能。我们现在表明，ADaPT 也可以在 Yao et al. (2023b) 所用的任务专属执行器之上使用。结果示于表 7。首先，我们观察到 ADaPT 的总体成功率提升最多 23.1 个百分点，并在除 1 类任务外的所有任务类型上超越基线。有趣的是，我们发现在使用更强执行器时（相比表 2），计划-执行基线表现强劲，可能因为这样的执行器能更好地处理复杂子任务。与表 2 一致，尽管缺少专用记忆与自然语言反馈，ADaPT 仍比 Reflexion 高 12.6 个百分点。

图 12：LLM 生成的成功启发式与金标准环境奖励在计算所有数据集成功率上的比较。

## 附录 D 额外的 WebShop 实验

#### 评估指标。

我们聚焦成功率而非（软）分数作为该任务的主要指标，因为朴素地购买一件商品也可能得到非零分数。为此，我们构建了一个朴素执行器，把用户查询输入搜索框并购买第一个可用商品。表 7 表明，虽然该基线的成功率最低，其分数却出人意料地高达 58.3。相比之下，我们的执行器常常不购买商品，尤其是当前面子目标失败时，这会损害分数，尽管成功率不受影响。因此，与先前工作（Zhou et al., 2023）不同，我们主张优化成功率而非分数。

#### ADaPT 适应任务复杂度。

默认情况下，Yao et al. (2023b) 使用只显示前 3 条搜索结果的搜索页面。直觉上，增加搜索页面上的商品数量要求模型从更广的商品阵列中选择，并跟踪它们的全部信息以确定对用户查询的最佳匹配，使整体任务更难。因此，我们在 WebShop 的两种设定（每个搜索页面 3 件与 10 件商品）上应用 ADaPT。

| 方法 | 商品数 | 成功率 |
| --- | --- | --- |
| ReAct | 3 | 27.5 |
| ADaPT（$d_{\mathrm{max}}=3$） | 3 | 47.5 |
| ReAct | 10 | 20.0 |
| ADaPT（$d_{\mathrm{max}}=3$） | 10 | 42.5 |

表 8：无论搜索页面选择多少商品（3 或 10），ADaPT 均提升 WebShop（开发集）性能。

#### 结果。

从表 8 中，我们观察到 ADaPT 相对 ReAct 基线，在 3 件与 10 件商品设定下分别有效提升成功率 20.0% 与 22.5%。两种设定下 ReAct 表现的差异印证了我们的假设：在其他条件相同的情况下，增加搜索页面上的商品数量会增加任务复杂度。值得注意的是，我们表明 ADaPT 在*更复杂*的任务设定下取得*更高*的提升。

## 附录 E TextCraft

#### TextCraft：环境细节。

在 TextCraft 中，目标是通过用环境中可用的物品合成来获得目标 Minecraft 物品。我们定义了一个包含三个动作的环境：craft <item> using <ingredients>、get <item> 与 inventory。我们利用 Minecraft 的合成配方来指定可合成物品及其原料，假设其他所有物品都可以从环境中获取。与 ALFWorld 类似，我们的智能体可以在具身游戏中直接执行这些操作。游戏开始时向智能体提供一列合成命令，详述可用于合成最终目标的配方、其原料以及一些干扰项（细节见附录 E）。当目标物品被加入智能体库存时产生 1 的奖励。TextCraft 的一条示例金标准轨迹见图 3。

我们使用 Minecraft v1.16.5 的配方创建 TextCraft 环境。我们只考虑可用工作台合成的配方。我们同时考虑无形状（只计数量）与有形状（原料位置重要）配方，并把它们转换为合成命令（例如 craft 4 sticks using 2 planks）。没有任何配方的物品被视为可通过 get 命令获取，例如 get 4 diamond。

由于全部合成命令无法放入现代 LLM 的上下文，我们为每个任务创建一组相关合成命令。除了金标准合成命令集合（即配方树中所有物品的合成命令）外，我们还加入最多 10 条干扰命令。为构建该干扰集，我们对金标准配方树配方中的每种原料下采样最多 10 个配方。最后，我们再从整个集合中下采样最多 10 个干扰项，以确保合理的上下文大小。注意，我们不提供有效的 get 命令列表，因为它可以从 craft 命令推断。

## 附录 F 成功启发式的评估

在第 3.1 节中，我们描述了 ADaPT 使用的执行器模块。对分配给执行器的任务，我们提示 LLM 生成一个二元的成功启发式。我们反复使用该启发式来评估（子）任务是否需要进一步分解。我们现在研究 LLM 在所有数据集上生成该成功启发式的能力。为此，我们运行 ADaPT，并在结束时比较使用 LLM 自评任务成功的成功率与环境金标准奖励（图 12）。在 ALFWorld 与 TextCraft 上，我们发现 LLM 略微高估其整体任务成功。这在预期之内，因为底层任务的主观性极低（例如，智能体的库存中要么有某物品，要么没有）。然而在 WebShop 上，商品可以在不同程度上（部分或完全）匹配用户标准，我们发现 LLM 的评估相比环境奖励显著虚高（>30 个百分点）。这种不完美的反馈会影响 ADaPT 的下游性能，因为算法在还需要进一步分解时即终止。我们把解决 LLM 自评缺陷的工作留作未来（Huang et al., 2023a；Stechly et al., 2023）。

## 附录 G 提示词

我们在以下页面中给出 ALFWorld、WebShop 与 TextCraft 数据集的规划器与执行器模块所用的全部提示（提示词展品为英文原文，整块保留不译）。

Here is a demo of actions you can perform.

You are in the middle of a room. Looking quickly around you, you see a desk 1, microwave 1, a cabinet 3, a cabinet 9, a drawer 2, a coffeemachine 1, a stoveburner 4, a drawer 5, a cabinet 11, a drawer 3, a stoveburner 1, a drawer 1, a toaster 1, a fridge 1, a stoveburner 2, a cabinet 6, a cabinet 10, a countertop 1, a cabinet 13, a cabinet 7, a garbagecan 1, a cabinet 2, a cabinet 8, a cabinet 12, a drawer 4, a cabinet 1, a sinkbasin 1, a cabinet 5, a stoveburner 3, and a cabinet 4.

Your task is to: Put a tomato in cabinet 1.

> think: Input assumption: I am carrying a tomato. Now I need to verify this.

OK.

> inventory

You are carrying: a tomato 1.

> examine tomato 1

There's nothing special about tomato 1.

> think: Based on previous context assumption is true, now I can proceed.

> go to cabinet 1

The cabinet 1 is closed.

> open cabinet 1

You open the cabinet 1. The cabinet 1 is open. In it, you see a candle 1, and a spraybottle 2.

> put tomato 1 in/on cabinet 1

You put the tomato 1 in/on the cabinet 1.

> think: End state: Now I put tomato (1) in cabinet (1). Task completed!

Your task is to: Take a mug from cabinet 5

> think: Input assumption: None

OK.

> go to cabinet 5

The cabinet 5 is closed.

> open cabinet 5

You open the cabinet 5. The cabinet 5 is open. In it, you see a mug 3.

> take mug 3 from cabinet 5

You pick up the mug 3 from the cabinet 5.

> think: End state: Now I take a mug (3) from cabinet (5). Task completed!

Your task is to: Heat an egg.

> think: Input assumption: I am carrying an egg. Now I need to verify this.

OK.

> inventory

You are carrying: a egg 2.

> examine egg 2

There's nothing special about egg 2.

> think: Based on previous context assumption is true, now I can proceed.

OK.

> go to microwave 1

The microwave 1 is closed.

> heat egg 2 with microwave 1

You heat the egg 2 using the microwave 1.

> think: End state: Now I heat a egg (2). Task completed!

Your task is to: Cool a mug.

> think: Input assumption: I am carrying a mug. Now I need to verify this.

OK.

> inventory

You are carrying: a mug 3.

> examine mug 3

There's nothing special about mug 3.

> think: Based on previous context assumption is true, now I can proceed.

OK.

> go to fridge 1

The fridge 1 is closed.

> cool mug 3 with fridge 1

You cool the mug 3 using the fridge 1.

> think: End state: Now I cool a mug (3). Task completed!

Your task is to: Clean a lettuce.

> think: Input assumption: I am carrying a lettuce. Now I need to verify this.

OK.

> inventory

You are carrying: a lettuce 1.

> examine lettuce 1

There's nothing special about lettuce 1.

> think: Based on previous context assumption is true, now I can proceed.

OK.

> go to sinkbasin 1

On the sinkbasin 1, you see a apple 2, a ladle 2, a spoon 1, and a tomato 3.

> clean lettuce 1 with sinkbasin 1

You clean the lettuce 1 using the sinkbasin 1.

> think: End state: Now I clean a lettuce (1). Task completed!

ALFWorld Hybrid Executor Prompt

Your task is to: Use a desklamp to look at tomato 1.

> think: Input assumption: I am at the location that contains desklamp (1). Now I need to verify this.

OK.

> inventory

You are carrying: a tomato 1.

> look

You are facing desk 1. Next to it, you see nothing.

> examine desk 1

On desk 1, you see a spoon 1, a desklamp 1, and a pencil 2.

> think: Based on previous context assumption is true, now I can proceed.

OK.

> use desklamp 1

You turn on the desklamp 1.

> think: Now I use desklamp (1). Task completed!

Here are two example tasks.

You are in the middle of a room. Looking quickly around you, you see a cabinet 13, a cabinet 12, a cabinet 11, a cabinet 10, a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 1, a diningtable 1, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.

Your task is to: put a hot apple in fridge.

> think: To solve the task, I need to find and take an apple, then heat it with microwave, then put it in fridge.

OK.

> think: First I need to find an apple. An apple is more likely to appear in fridge (1), diningtable (1), coffeetable (1), drawer (1), cabinet (1-13), garbagecan (1). I can check one by one, starting with fridge 1.

OK.

> go to fridge 1

The fridge 1 is closed.

> open fridge 1

You open the fridge 1. The fridge 1 is open. In it, you see a cup 1, and a egg 1.

> go to diningtable 1

On the diningtable 1, you see a apple 1, a bread 1, a fork 3, a fork 2, a fork 1, a mug 2, a peppershaker 3, a plate 2, a pot 1, a soapbottle 3, a spatula 1, a spoon 3, a spoon 2, a spoon 1, a winebottle 3, and a winebottle 2.

> think: Now I find an apple (1). Next, I need to take it.

OK.

> take apple 1 from diningtable 1

You pick up the apple 1 from the diningtable 1.

> think: Now I take an apple (1). Next, I need to go to a microwave (1) and heat it.

OK.

> go to microwave 1

The microwave 1 is closed.

> heat apple 1 with microwave 1

You heat the apple 1 using the microwave 1.

> think: Now I heat an apple (1). Next, I need to put it in/on fridge 1.

OK.

> go to fridge 1

The fridge 1 is open. In it, you see a cup 1, and a egg 1.

> put apple 1 in/on fridge 1

You put the apple 1 in/on the fridge 1.

> think: Task completed!

You are in the middle of a room. Looking quickly around you, you see a bed 1, a desk 1, a drawer 3, a drawer 2, a drawer 1, a garbagecan 1, a safe 1, a shelf 5, a shelf 4, a shelf 3, a shelf 2, a shelf 1, a sidetable 2, and a sidetable 1.

Your task is to: look at bowl under the desklamp.

> think: To solve the task, I need to find and take a bowl, then find and use a desklamp.

OK.

> think: First I need to find a bowl. A bowl is more likely to appear in drawer shelf (1-5), drawer (1-3). I can check one by one, starting with drawer 1.

OK.

> go to shelf 1

On the shelf 1, you see nothing.

> go to shelf 2

On the shelf 2, you see a bowl 1.

> think: Now I find a bowl (1). Next, I need to take it.

OK.

> take bowl 1 from shelf 2

You pick up the bowl 1 from the shelf 2.

> think: Now I take a bowl (1). Next, I need to find a desklamp. A desklamp is more likely to appear in desk (1), sidetable (1-2), and drawer (1-3). I can check one by one, starting with desk 1.

OK.

> go to desk 1

On the desk 1, you see a alarmclock 2, a book 1, a cellphone 1, a keychain 1, a laptop 2, a laptop 1, and a pen 3.

> go to sidetable 1

On the sidetable 1, you see a cd 1, a pen 1, and a pencil 1.

> go to sidetable 2

On the sidetable 2, you see a alarmclock 1, a desklamp 1, and a pen 2.

> think: Now I find a desklamp (1). Next, I need to use it.

OK.

> use desklamp 1

You turn on the desklamp 1.

> think: Task completed!

ALFWorld Hybrid Executor Prompt (cont.)

Here are some examples.

You are in the middle of a room. Looking quickly around you, you see a desk 1, microwave 1, a cabinet 3, a cabinet 9, a drawer 2, a coffeemachine 1, a stoveburner 4, a drawer 5, a cabinet 11, a drawer 3, a stoveburner 1, a drawer 1, a toaster 1, a fridge 1, a stoveburner 2, a cabinet 6, a cabinet 10, a countertop 1, a cabinet 13, a cabinet 7, a garbagecan 1, a cabinet 2, a cabinet 8, a cabinet 12, a drawer 4, a cabinet 1, a sinkbasin 1, a cabinet 5, a stoveburner 3, and a cabinet 4.

Goal: Put a mug in/on desk.

Come up with an abstract plan to perform this task in a couple of steps.

# Think: To perform this task, I need to find and take mug and then put it on desk. First, I will focus on finding mug.

Step 1: Find and take mug

# Think: Now that I am carrying mug, I will focus on putting it in/on desk.

Step 2: Put mug in/on desk

Execution Order: (Step 1 AND Step 2)

Goal: Clean mug and put it in/on desk.

Come up with an abstract plan to perform this task in a couple of steps.

# Think: To perform this task, I need to find and take mug, clean it, and then put it on desk. First, I will focus on finding mug.

Step 1: Find and take mug

# Think: Now that I am carrying mug, I will focus on cleaning it.

Step 2: Clean mug with sinkbasin

# Think: Now that I have cleaned mug, I will focus on putting it in/on desk.

Step 3: Put cleaned mug in/on desk

Execution Order: (Step 1 AND Step 2 AND Step 3)

Goal: Cool mug and put it in/on desk.

Come up with an abstract plan to perform this task in a couple of steps.

# Think: To perform this task, I need to find and take mug, cool it, and then put it on desk. First, I will focus on finding mug.

Step 1: Find and take mug

# Think: Now that I am carrying mug, I will focus on cooling it.

Step 2: Cool mug with fridge

# Think: Now that I have cooled mug, I will focus on putting it in/on desk.

Step 3: Put cooled mug in/on desk

Execution Order: (Step 1 AND Step 2 AND Step 3)

Goal: Heat mug and put it in/on desk.

Come up with an abstract plan to perform this task in a couple of steps.

# Think: To perform this task, I need to find and take mug, heat it, and then put it on desk. First, I will focus on finding mug.

Step 1: Find and take mug

# Think: Now that I am carrying mug, I will focus on heating it.

Step 2: Heat mug with microwave

# Think: Now that I have heated mug, I will focus on putting it in/on desk.

Step 3: Put heated mug in/on desk

Execution Order: (Step 1 AND Step 2 AND Step 3)

Goal: Look at mug under desklamp.

Come up with an abstract plan to perform this task in a couple of steps.

# Think: To perform this task, I need to find and take mug, and then go to the desklamp and use it. First, I will focus on finding mug.

Step 1: Find and take mug

# Think: Now that I have found and taken mug, I will focus on using the desklamp.

Step 2: Use the desklamp

Execution Order: (Step 1 AND Step 2)

Goal: Find and take mug

Come up with an abstract plan to perform this task in a couple of steps.

# Think: To perform this task I need to find mug in the room. mug is likely to be in desk, cabinet, countertop, or drawer. Now I will focus on finding mug in each of these locations one by one.

Step 1: Find and take mug from desk

# Think: If mug not found so far, I will next look in the cabinet.

Step 2: Find and take mug from cabinet

# Think: If mug not found so far, I will next look in the countertop.

Step 3: Find and take mug from countertop

# Think: If mug not found so far, I will next look in the drawer.

Step 4: Find and take mug from drawer

Execution Order: (Step 1 OR Step 2 OR Step 3 OR Step 4)

Here is the goal.

<room>

Goal: <task>.

Come up with an abstract plan to perform this task in a couple of steps. Constraints: The robot can hold/take/put only one object at a time to a location.

Ensure each step can be understood independently and mentions the name of object.

When stating the execution order, ensure that 'AND'/'OR' statements are properly nested using brackets '()'.

ALFWorld Planner Prompt

Instruction: Buy product [B078GWRC1J] that matches criteria: 3 ounce bottle of bright citrus deodorant for sensitive skin, and price lower than 50.00 dollars

Action: think['I should be on the search page where I can see a list of products, I should verify that.']

Observation: OK.

Action: load

Observation:

[Back to Search]

Page 1 (Total results: 50)

[Next >]

[B078GWRC1J]

Bright Citrus Deodorant by Earth Mama | Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce

$10.99

[B08KBVJ4XN]

Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack)

$35.95

[B078GTKVXY]

Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce

$10.99

Action: think['I can spot product [B078GWRC1J] and it is a clickable link since its enclosed in square brackets. I should click on it.]

Observation: OK.

Action: click[B078GWRC1J]

Observation:

[Back to Search]

[< Prev]

scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]

size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]

Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce

Price: $10.99

Rating: N.A.

[Description]

[Features]

[Reviews]

[Buy Now]

Action: think[I'm already on the product page. I see multiple possible options enclosed in '[]' for scent and size for this product. To match the input criteria, I should click on options '[bright citrus]' for scent and '[3 ounce (pack of 1)]' for size one by one and then buy in the end.]

Observation: OK.

Action: click[bright citrus]

Observation: You have clicked bright citrus.

Action: click[3 ounce (pack of 1)]

Observation: You have clicked 3 ounce (pack of 1).

Action: think[My task is to buy the product, for it should to click 'buy now']

Observation: OK.

Action: click[Buy Now]

Observation: You have clicked buy now.

Action: think[I finished buying the product. Task completed!]

Here is another task in which you need to buy a product. When you finish buying the product with the most relevant choices, use 'think[Task completed']. If you cannot find the matching options or proceed, think['Task failed']. Note that you can only click on text enclosed in '[]' on the webpage. Everything else is only a description, not valid with the "click" action.

Instruction: Buy product [{}] that matches the criteria: {}

WebShop Executor Prompt: Buy

You are given a webpage of an item on an online shopping website and a criteria. Your task is to answer if the product on the page exactly matches the criteria. Not the criteria could have multiple requirements that should be checked one by one and all must satisfy for an exact match.

Here are a few examples:

Criteria: 3 ounce bottle of citrus deodorant for sensitive skin that is priced lower than $30 and natural.

Item Page:

[Back to Search]

[< Prev]

scent [assorted scents][bright citrus][calming lavender][ginger fresh][simply non-scents]

size [travel set (4-pack)][3 ounce (pack of 1)][3-ounce (2-pack)]

Bright Citrus Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce

Price: $10.99

Rating: N.A.

[Description]

Features:

NEW from Earth Mama (formerly Earth Mama Angel Baby), formulated especially for pregnancy, breastfeeding and sensitive skin

Contains organic grapefruit, tangerine and calendula

NO propylene glycol, artificial fragrance, parabens or aluminum

Dermatologist tested and clinically tested for irritation

Better than natural organic! NSF/ANSI 305 Certified by Oregon Tilth

[Reviews]

[Attributes]

[Buy Now]

Answer: The product is available in 3 ounce size, is citrus and suitable for sensitive skin. It is also organic or natural. Its price is $10.99 which is less than $30.

Thus, the answer is True (exact match).

Criteria: 3 ounce bottle of citrus deodorant for sensitive skin that is priced lower than $30 and natural.

Item Page:

[Back to Search]

[< Prev]

size [3 ounce][3 ounce (pack of 1)]

unit count [2.0][3.0]

Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack)

Price: $15.95

Rating: N.A.

[Description]

Features:

About this item WHY ALUMINUM-FREE DEODORANT? Aluminum-free deodorants use more natural ingredients unlike antiperspirants, which use chemicals to block sweat. Safely fight odor for 24 hours with Barrel & Oak's deodorantsour gentle formula is easy on sensitive skin. START SMELLING LIKE THE MAN YOU WANT TO BE: Our mountain sage aluminum-free men's deodorant is naturally fragranced with an outdoorsy scent of crisp conifer, sage, & citrus. Think sweet notes of citrus with earthy tones of cedar & patchouli. PREMIUM INGREDIENTS FOR NATURAL FRAGRANCES: Our deodorants for men are composed of natural, essential oil-based scents. These natural fragrance deodorants are more subtle than their synthetic counterparts, but they're better for you & the planet. DESIGNED FOR THE MODERN MAN: Barrel & Oak has a full spectrum of grooming & body care products that are designed with function, fragrance, & effective ingredients for the health-conscious & practical modern man. Give your body what it deserves. EARTH-FRIENDLY, YOU-FRIENDLY, WALLET-FRIENDLY: Our premium products for men are scented with natural fragrances & essential oils, free of parabens, phthalates, & SLS, packaged in recyclable materials, cruelty-free, & vegan or vegetarian.

[Reviews]

[Attributes]

[Buy Now]

Answer: The product is not citrus in nature. It does not match the criteria. It's price is $15.95 which is less than $30.

Thus, the answer is False (not an exact match).

Now here is the criteria and item page for the another task. Try you best to determine exact match, otherwise, respond with "False", i.e., no exact match. Generate an explanation before the answer to justify your decision.

Criteria: {}

Item Page:

{}

Answer:

WebShop Executor Prompt: Match (cont.)

You are given a search page on an online shopping site with a list of products along with name and price. Based on this information, your task is return a list of product IDs (enclosed in []) of all products that exactly match all requirements in the criteria. If the information provided is not enough to make a determination, return an empty list.

Here are a few examples.

Search Page:

[Back to Search]

Page 1 (Total results: 50)

[Next >]

[B078GWRC1J]

Bright Citrus Deodorant by Earth Mama | Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce

$10.99

[B08KBVJ4XN]

Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack)

$35.95

[B078GTKVXY]

Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce

$10.99

[B08SMG4WB9]

Each & Every 2-Pack Natural Aluminum-Free Deodorant for Sensitive Skin with Essential Oils, Plant-Based Packaging (Citrus & Vetiver, 2.5 Ounce (Pack of 2))

$25.0

[B08KVCCSD6]

Each & Every 3-Pack, Natural Aluminum-Free Deodorant for Sensitive Skin Made with Essential Oils, 2.5 Oz. (Lavender & Lemon, Citrus & Vetiver, and Coconut & Lime)

$35.0

Criteria: less than 5 ounce citrus deodorant sensitive skin, price less than $30.

Answer: My requirements are 5 ounce, citrus deodrant, suitable for sensitive skin, and price less than $30. Looks like this information is available on the search page, so I can proceed.

Products B078GWRC1J, B08SMG4WB9 look suitable as they are less than 5 ounce, citrus and have price 10.99 and $25 less than $30. Thus, shortlisted IDs are shortlisted=['B078GWRC1J', 'B08SMG4WB9']

Criteria: less than 5 ounce citrus deodorant sensitive skin, cruelty free.

Answer: My requirements are 5 ounce, citrus deodrant, suitable for sensitive skin, and cruelty-free. Since there is no information about cruelty free on the search page, I cannot proceed. Task failed!

Here is another task with a different search page and criteria. List all the product ids (enclosed in []) from the search page that match ALL the requirements in the criteria. Name this list shortlisted. If you cannot make the determination about even 1 sub-criteria, do not make a guess, output "task failed!". Generate an explanation before the answer to justify your decision.

Search Page:

{}

Criteria: {}

Answer:

WebShop Executor Prompt: Shortlist (cont.)

Write an abstract plan to successfully complete the goal. In each step of the plan mention which module (including arguments) that need to be called. Learn from and incorporate information from previous runs, e.g. do not repeat previously successful or unsuccesful commands. Here are some examples:Information from previous run: -

Goal: Buy 3 ounce bottle of citrus deodorant for sensitive skin, that is natural and priced less than 50.00 dollars.

# Think: Based on the criteria and the search bar, I should query 3 ounce citrus deodorant sensitive skin. I have the following constraints: natural and price lower than $30 which I can use to narrow down search results.

Step 1: Search[3 ounce citrus deodorant sensitive skin]

# Think: Now I will need to narrow down the search results for price lower than $30 and natural

Step 2: SimpleMatch[3 ounce citrus deodorant sensitive skin with price lower than $50 and natural]

# Think: Since it returns a list of up to 3 products, I will pick the first suitable product. For now, Ill denote its id as prod_id for placeholder.

Step 3: Buy[prod_id, "3 ounce bottle of citrus deodorant for sensitive skin, that is natural and priced less than 30.00 dollars"]

#Think: My plan requrires all these steps to succeed sequentially, so I will use the "AND" operator.

Execution Order: (Step 1 AND Step 2 AND Step 3)

Information from previous run:

- Unable to get matching product using: SimpleMatch[3 ounce citrus deodorant sensitive skin with price lower than $30 and natural]

- Search results page:

[Back to Search]

Page 1 (Total results: 50)

[Next >]

[B078GWRC1J]

Bright Citrus Deodorant by Earth Mama | Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce

$10.99

[B08KBVJ4XN]

Barrel and Oak - Aluminum-Free Deodorant, Deodorant for Men, Essential Oil-Based Scent, 24-Hour Odor Protection, Cedar & Patchouli Blend, Gentle on Sensitive Skin (Mountain Sage, 2.7 oz, 2-Pack)

$35.95

[B078GTKVXY]

Ginger Fresh Deodorant by Earth Mama | Natural and Safe for Sensitive Skin, Pregnancy and Breastfeeding, Contains Organic Calendula 3-Ounce

$10.99

[B08SMG4WB9]

Each & Every 2-Pack Natural Aluminum-Free Deodorant for Sensitive Skin with Essential Oils, Plant-Based Packaging (Citrus & Vetiver, 2.5 Ounce (Pack of 2))

$25.0

[B08KVCCSD6]

Each & Every 3-Pack, Natural Aluminum-Free Deodorant for Sensitive Skin Made with Essential Oils, 2.5 Oz. (Lavender & Lemon, Citrus & Vetiver, and Coconut & Lime)

$35.0

[B087WKSR2G]

Goal: Narrow down search results for 3 ounce bottle of citrus deodorant for sensitive skin that is priced lower than $30 and natural. You cannot search again.

#Think: Based on the search results and previous information, SimpleMatch failed because my criteria was too complex. Price constraint is easy to verify, I will narrow down based on that first then examine in detail for natural constraint

#Think: Based on price, I narrow down my search to B078GWRC1J, B08SMG4WB9 as they look suitable. These are on my shortlist to examine the natural constraint in detail one by one.

Step 1: DetailMatch[B078GWRC1J, 3 ounce bottle of for sensitive skin, that is natural and priced less than 30.00 dollars]

Step 2: DetailMatch[B08SMG4WB9, 3 ounce bottle of citrus deodorantcitrus deodorant for sensitive skin, that is natural and priced less than 30.00 dollars]

#Think: If none of the products exactly match my criteria, I will search again with a new query that includes the natural criteria too. This ensures my plan is compelete.

Step 3: Search[3 ounce citrus deodrant natural and sensitive skin]

#Think: Since these steps are linked by an if condition, I only need one of them to succeed. I will connect them using the "OR" operator.

Execution Order: (Step 1 OR Step 2 OR Step 3)

Here is a new goal. Write an abstract plan to successfully complete the goal. In each step of the plan mention which module (including arguments) that need to be called. Learn from and incorporate information from previous runs, e.g. do not repeat previously successful or unsuccesful commands. In the end, output the intended execution order.

Information from previous run: {}

Goal: {}

WebShop Planner Prompt

You are given few useful crafting recipes to craft items in Minecraft. Crafting commands are of the format "craft [target object] using [input ingredients]". You can either "fetch" an object (ingredients) from the inventory or the environment or "craft" (target) using any of the crafting commands. You can use ONLY these crafting commands provided, do not use your own crafting commands. However, if the crafting command uses a generic ingredient like "planks", you can use special types of the same ingredient e.g. "dark oak planks" in the command instead. For any other natural language or thoughts, use prefix 'think: '.

Here is a demo of how to fetch and craft objects.
Crafting commands:
craft 3 dark oak sign using 6 dark oak planks, 1 stick
craft 4 dark oak planks using 1 dark oak log
craft 1 stick using 1 planks
craft 4 stick using 2 bamboo
craft 4 oak planks using 1 oak log
craft 1 dark oak fence using 2 stick, 4 dark oak planks
craft 1 warped stairs using 6 warped planks
craft 3 oak sign using 6 oak planks, 1 stick
Goal: craft dark oak sign
> think: I should check if I can fetch dark oak sign directly from the environment or the inventory.
OK.
> inventory:
Inventory: [stick] (1) [dark oak planks] (8)
> get dark oak sign
Could not find dark oak sign
> think: I cannot get dark oak sign directly, I need to craft it. From the crafting commands, I can use: craft dark oak sign using 6 dark oak planks, 1 stick. Ingredients needed: 6 dark oak planks, 1 stick. Input assumption: I have all the neccessary ingredients in my inventory. Let me verify this first.
OK.
> inventory
Inventory: [stick] (1) [dark oak planks] (8)
> think: I found my ingredients: 6 dark oak planks, 1 stick in my inventory. My assumption is true, I can proceed. I will use the crafting command: craft dark oak sign using 6 dark oak planks
OK.
> craft 1 dark oak sign using 6 dark oak planks, 1 stick
Crafted 1 minecraft:dark_oak_sign
> inventory
Inventory: [dark oak sign] (1)
> think: I now have dark oak sign in my inventory. Task Completed!
OK.

Goal: fetch 2 dark oak logs.
> think: I should check my inventory first, to see if I already have dark oak sign. Otherwise, I will directly try to get it from the environment.
OK.
> inventory
Inventory: [stick] (1)
> get 2 dark oak logs.
Got 2 dark oak logs
> inventory
Inventory: [dark oak log] (2) [stick] (1)
> think: I have 2 dark oak logs in my inventory. Task Completed!
OK.

TextCraft Executor Prompt

Here is an example of a complex goal.
Goal: craft 2 oak planks
> think: I should check if I can fetch dark oak sign directly from the environment or the inventory.
OK.
> inventory:
Inventory: [stick] (1)
> get 2 oak planks
Could not find 2 oak planks
> think: I cannot get oak planks directly, I need to craft it. From the crafting commands, I can use: craft 4 oak planks using 1 oak log. Ingredients needed: 1 dark oak log. Input assumption: I have the ingredients needed in my inventory. Let me verify this first.
OK.
> inventory
Inventory: [stick] (1)
> think: My assumption is false. I need to get the ingredients: 1 oak log first.
OK.
> get 1 oak log
Got 1 oak log
> craft 4 oak planks using 1 oak log
Crafted 4 minecraft:oak_planks
> inventory
Inventory: [stick] (1) [oak_planks] (4)
> think: I now have 2 oak planks in my inventory. Task Completed!
OK.
Now here is a different goal. You can use these crafting commands to accomplish the goal. When you the desired item in your inventory, think: Task Completed! If you have tried your best but cannot proceed, think: task failed!

TextCraft Executor Prompt (cont.)

Your task is to come up with a short plan to help me accomplish my goal in a couple of steps using at most ONE of the provided crafting commands. You can take the help of crafting commands below to create new objects.

Craft command can be understood as follows: craft [target] using [ingredients], where target is item/object generated by the craft command as output and ingredient are the inputs. You are given an agent that can "craft" or "fetch" objects.

Here is are some examples.

Crafting commands:

craft 3 dark oak sign using 6 dark oak planks, 1 stick

craft 4 dark oak planks using 1 dark oak log

craft 1 stick using 1 planks

craft 4 stick using 2 bamboo

craft 4 oak planks using 1 oak log

craft 1 dark oak fence using 2 stick, 4 dark oak planks

craft 1 warped stairs using 6 warped planks

craft 3 oak sign using 6 oak planks, 1 stick

Goal: craft dark oak sign.

# Think: My target is a dark oak sign. From the list of crafting commands, only 1 command generates my target: craft 3 dark oak sign using 6 oak planks, 1 stick. I will use this command to devise a plan. My ingredients are: 6 dark oak planks, 1 stick. I should first get all the ingredients and then use the crafting command.

Step 1: fetch 6 dark oak planks

Step 2: fetch 1 stick

# Think: Now that I have collected the input ingredients, I can craft the dark oak sign using given command.

Step 3: craft dark oak sign using 6 dark oak planks, 1 stick

# Think: To succeed, I need to perform all these steps, one after the other. So I need to use the "AND" operator.

Execution Order: (Step 1 AND Step 2 AND Step 3)

Goal: fetch 6 dark oak planks.

# Think: My target is 6 dark oak planks. From the list of crafting commands, only 1 command generates my target: craft 4 dark oak planks using 1 dark oak log. My ingredients are: 1 dark oak log. To successfully accomplish the goal, I should first get all the ingredients and then use the crafting command.

Step 1: fetch 1 dark oak log

# Think: Now that I have collected the input ingredients, I can craft dark oak planks using given command. I know that I cannot use a partial recipe.

Step 2: craft 4 dark oak planks using 1 dark oak log

# Think: This gives me 4 dark oak planks which is less than my desired 6 dark oak planks. I know that I cannot use a partial recipe. So my goal is not satisfied, I need to craft more dark oak planks by repeating Step 2 one more time.

Step 3: craft 4 dark oak planks using 1 dark oak log

# Think: To succeed, I need to perform all these steps, one after the other. So I need to use the "AND" operator.

Execution Order: (Step 1 AND Step 2 AND Step 3)

Here is a different goal with different craft commands. Your task is to come up with a short plan to help me accomplish my goal in a couple of steps using at most ONE of the provided crafting commands. You can take the help of crafting commands below to create new objects. Keep in mind that:

- It is okay to generate more target objects than your goal.

- Be very careful with the count of objects, SAME object counts mentioned in the input crafting command.

- You cannot use a partial crafting command recipe, i.e. if the recipe generates 2 objects you CANNOT alter it to produce just 1.

- Also, you can use ONLY 1 crafting command in your plan.

TextCraft Planner Prompt


