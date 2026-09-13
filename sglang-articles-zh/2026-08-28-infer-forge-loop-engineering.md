---
title: "Infer-forge:围绕 SGLang 的执行框架、循环与图工程"
title_en: "Infer-forge: Harness, Loop, and Graph Engineering Around SGLang"
author: "Tianyu Zhang, Hanlin Gao, Yusong Gao, Yun Zhang"
date: "August 28, 2026"
previewImg: /images/blog/infer-forge-loop/cover.png
type: blog
source: https://lmsys.org/blog/2026-08-28-infer-forge-loop-engineering/
translated: 2026-09-12
---

# Infer-forge:围绕 SGLang 的执行框架、循环与图工程

> 原文:[Infer-forge: Harness, Loop, and Graph Engineering Around SGLang](https://lmsys.org/blog/2026-08-28-infer-forge-loop-engineering/) · LMSYS Blog · Tianyu Zhang, Hanlin Gao, Yusong Gao, Yun Zhang

## 1. 引言

**推理优化在代码层面看似是局部改动,但其有效性是全局性的。**一处算子(kernel)、通信路径或调度上的改动,只有在由模型、负载、SLO、服务拓扑、运行时版本与加速器平台共同定义的特定部署点上才有意义。同一个补丁可能改善一个部署点,却让另一个部署点出现回退。借助 Agent 的探索会产出更多的环境、实验、测量结果和被否决的路径,而这一切都必须保持可复现。

**因此,第一项要求是可靠的执行。**复现一个部署点所需的不只是模型能力:工具、环境、上下文、记忆、验证(Verification)与安全边界都必须保持稳定。**执行框架工程(Harness Engineering)**将上述外围条件转化为一个可复现、可审查的执行系统——这正是 **Agent = Model + Harness** 这一抽象的基础<sup>[1](#ref-1),[2](#ref-2),[3](#ref-3),[6](#ref-6)</sup>。

**可靠的执行还必须在时间维度上保持连贯。**推理工程任务往往横跨多轮反复的调查、实现、部署、评估、失败与恢复。**循环工程(Loop Engineering)**将先后多次执行衔接起来,使一个任务能够守住自己的任务契约(Task Contract)、吸收新证据,并最终通过产出经过验证的交付物(Deliverable)或可靠的后续交接(Follow-up Handoff)来满足其退出标准(Exit Criteria)<sup>[4](#ref-4),[5](#ref-5),[7](#ref-7)</sup>。

**项目规模的工作超出了单个任务的边界。**多个任务必须并行推进、交换交付物、共享状态、触发返工(Rework),并随着证据积累而调整方向。**图工程(Graph Engineering)**将各自独立收敛的任务循环组织进一个不断演化的**任务图(Task Graph)**。任务图让已发布和已否决的路径始终与其依赖、约束和证据相连,从而使项目决策保持可解释<sup>[10](#ref-10),[11](#ref-11),[12](#ref-12),[13](#ref-13)</sup>。

**Infer-forge 将这一递进结构应用于围绕 SGLang 展开的推理工程。**其覆盖范围伴随一次工程改动贯穿整个推理栈:从算子与通信库,经由引擎集成与部署,直到评估与在线诊断。一个共享工作区加上三种不断累积的执行结构,让这条端到端路径保持连贯:

- **MonoRepo** 为跨仓库工程建立一个可复现的工作区。
- **Harness** 提供可复用的执行能力、记忆、验证与安全边界。
- **任务循环(Task Loop)**让一个长时间运行的任务持续推进,直至达到其退出标准。
- **任务图(Task Graph)**将各自独立收敛的任务连接成更大的目标,包括项目交付与能力演化。

### 1.1 实现状态与可用性

**Infer-forge 是围绕 SGLang 独立开发的内部工程系统,并非 SGLang 或 LMSYS 的官方组件。**

| 范围 | 当前状态 |
|---|---|
| MonoRepo 工作区、任务与 Journal 记录,以及任务/图的 schema、CLI 与校验器 | 已实现并在内部使用 |
| 任务循环的生命周期流转与交接 | 部分自动化,有工具支持 |
| 任务生成与自适应任务图演化 | 已实现并在内部使用;infer-forge 从用户目标派生任务,将其连入任务图,并在执行过程中随任务被接受、放弃或改向而更新任务图 |
| 能力触发输入与生命周期操作 | 已实现并需显式调用 |
| 任务的接受或放弃、人工门控(Human Gate)与发布决策 | 由人主导;这些决策会反馈进任务图的演化 |

**Infer-forge 目前并未开源,因为其核心组件与我们的内部仓库、基础设施、工作流和安全控制深度耦合,当前代码库在我们的环境之外可移植性有限。**

**本文选择将构建方法论公开。**我们的目标是让团队和个人把这套方法论交给 AI 编程工具,补充自己系统的上下文,快速构建出适配自身环境的 infer-forge 实现。

**Infer-forge 已从工作流设计阶段进入持续的工程使用阶段。**在一名工程师 4 月至 7 月的记录中,观测到的**在飞任务(Tasks in flight)**峰值从 **2** 升至 **9**。在一个 DeepSeek-V4-Pro 推理服务项目中,**横跨七种任务类型的 38 个可独立验证的任务节点**以任务图的形式得到协同调度。这些记录共同表明,infer-forge 已在四个月的工程记录和项目级的任务图中得到持续使用。

**能力强的 Agent 可以让一次执行成功;而工程系统的设计目标是让成功的工作可复现。**Infer-forge 并不承诺每个任务都能更快完成。它提供的结构,用于保全每个部署点的来源脉络、支撑长时间运行任务中可验证的工作,并在任务边界之间协同证据。

## 2. 推理即部署空间

<div align="center">
  <img src="/images/blog/infer-forge-loop/fig-01-inference-deployment-space.svg" alt="The inference deployment space stacks five layers of static configuration. Model shows Ling, Qwen, DeepSeek, Kimi, GLM, and MiniMax. Serving Scenario runs Modality (text, image, video) into Traffic Shape (input and output length, media count, resolution, QPS, concurrency, cache reuse) into SLO (TTFT, TPOT, throughput, E2E latency). Serving Topology separates Deployment Architecture—Colocated PD, PD Disaggregation, and EPD Disaggregation, each listing the node roles it is built from — Prefill and Decode together, then Prefill and Decode as separate roles, then Encoder alongside them — from Parallelism—TP, PP, DP, and EP—because the two are chosen independently. Versioned Runtime Profiles is a stack of tabbed cards labelled Service A rev. 12, Service B rev. 7, and Service C rev. 21, plus a fourth paler card behind them all, blank and showing only its top edge, whose narrow tab carries an ellipsis for the profiles not drawn, the front card holding an Engine Configuration and a Container Image whose digest is pinned alongside its Framework, Device Runtime, and Collectives. Accelerator Platforms groups placeholder GPUs under Vendor A, B, and C. Arrows between the layers carry configuration dependency, not runtime data flow" />
  <br>
  <em>图 1:推理部署点背后的约束链。</em>
</div>

图 1 把上文引入的部署点具体化为一条约束链。**模型(Model)**决定支持的模态和模型特定的执行路径。**服务场景(Serving Scenario)**将**模态(Modality)**与**流量形态(Traffic Shape)**转化为 **SLO**。该 SLO 约束**服务拓扑(Serving Topology)**,在拓扑中,**部署架构(Deployment Architecture)**与**并行(Parallelism)**策略相互组合。拓扑随后通过**版本化运行时配置档(Versioned Runtime Profile)**落地,它为特定服务版本固定引擎配置与容器镜像。最后,完整的运行时必须在某个**加速器平台(Accelerator Platform)**上构建并验证。一个部署点是贯穿这条链的完整路径——而非任何单独一层。

**不存在脱离上下文的推理优化。**不同的服务目标和 SLO 可能要求截然不同的部署路径,包括 `Colocated PD`(PD 共置)、`PD Disaggregation`(PD 分离)和 `EPD Disaggregation`(EPD 分离)。每种架构都会改变阶段边界、通信路径、资源平衡,以及可行的并行策略集合。这些决策会传导到运行时配置档以及必须加以验证的加速器特定实现中。只有当完整的部署点复现了某项算子改进,并通过吞吐量、延迟、正确性与稳定性关卡后,它才算转化为推理服务成果。**脱离部署点,任何性能论断都无法被复现、比较或继承下去。**

**Infer-forge 并不消除这一组合空间;它让在其中走过的每一步都显式、可验证。**我们不再要求 Agent「优化 DeepSeek-V4-Pro」,而是定义一个任务,记录当前部署点、限定它允许改动的维度子集,并在执行开始前固定验证关卡。一个任务可以在保持服务场景、拓扑和加速器不变的前提下替换 MoE 后端,最终产出一个被采纳的改进或一份留档的否决。两种结果都能为下一个任务降低不确定性。但无论哪种结果,要被复现,其部署点背后的确切跨仓库代码状态必须先被固定下来。这正是 MonoRepo 的角色。

## 3. MonoRepo

### 3.1 为什么需要 MonoRepo

**推理优化跨越仓库边界,但它最终必须作为一个连贯的系统交付。**一处改动可能始于某个算子库,依赖某个通信后端,经由引擎集成进入 SGLang,最后还需要配套的部署配置。当这些仓库分散在各自独立的工作区中时,它们之间的关系就成了转瞬即逝的知识,工程师和 Agent 不得不反复重建。一个缺失的分支或一个不兼容的版本就足以让结果作废。

**Infer-forge 把这张依赖地图变成一个共享工作区。**Git 子模块把相关仓库置于同一根目录之下,同时保留它们各自独立的历史、分支策略、访问控制和发布流程。这个根目录为工程师和 Agent 提供了推理栈的稳定地图,以及一个可以开发和验证跨仓库工作的统一入口。

这一结构从三个方面改变跨仓库工作:

- **整条技术栈尽收眼底。**仓库边界依然清晰,但它们之间的工程关系在一个工作区内即可见。
- **上下文保持有界。**Agent 可以浏览完整的仓库地图,同时只加载当前任务所需的仓库。
- **集成就地展开。**相关分支可以被开发、组合和验证,而无需反复定位仓库或凭记忆重建它们的关系。

**工作区负责协调改动;任务记录让改动留痕持久。**每个任务记录下该项工作使用的分支、commit 与执行状态,完成后由 Journal 归档这份记录。各仓库可以继续演化,而不会抹去已经验证并交付的工作的来源脉络。

### 3.2 仓库地图

<div align="center">
  <img src="/images/blog/infer-forge-loop/fig-02-monorepo.svg" alt="The infer-forge MonoRepo contains three groups: a Built-in Workspace; Inference Stack Repos centered on SGLang, including Dynamo, DeepGEMM, DeepEP, FlashMLA, FlashInfer, Humming, and Mooncake; and Harness Repos" />
  <br>
  <em>图 2:Infer-forge MonoRepo。</em>
</div>

**一个工作区并不意味着一个不加区分的代码库。**Infer-forge 按仓库在工程中扮演的角色对它们加以区分:**内置工作区(Built-in Workspace)**负责协调跨仓库工作,**推理栈仓库(Inference Stack Repos)**承载被改动的服务系统,**Harness 仓库(Harness Repos)**则把这些改动从执行一路带到经过验证的证据。

#### 内置工作区(Built-in Workspace)

**内置工作区是 infer-forge 的协调层,而不是又一个实现仓库。**代码仍留在所属的仓库中。根目录只存放那些需要跨越仓库边界运作的机制:

- **任务系统(Task System)**将一个任务所需的工作区实体化:相关仓库、环境入口、记录位置,以及在需要隔离时的专属 worktree 和 Agent 会话。
- **跨库管理(Cross-lib Management)**让仓库图变得可操作。它维护仓库位置、默认分支,以及用于同步和整合改动的操作。一项工作实际使用的分支和 commit 属于任务记录,并被归档进 Journal。
- **Skills** 让能力在其所属的层级暴露出来。根目录提供任务生命周期与跨仓库协调相关的 Skills;每个仓库则保留其领域专属的 Skills。

#### 推理栈仓库(Inference Stack Repos)

**推理栈仓库是服务行为与性能真正发生改变的地方。**[SGLang](https://github.com/sgl-project/sglang) 是整条栈的中心,而 [Dynamo](https://github.com/ai-dynamo/dynamo) 将多个 SGLang 实例组织成一个分布式服务。[DeepGEMM](https://github.com/deepseek-ai/DeepGEMM)、[FlashMLA](https://github.com/deepseek-ai/FlashMLA)、[FlashInfer](https://github.com/flashinfer-ai/flashinfer) 与 [Humming](https://github.com/inclusionAI/humming) 提供专门的计算算子。[DeepEP](https://github.com/deepseek-ai/DeepEP) 与 [Mooncake](https://github.com/kvcache-ai/Mooncake) 提供专家并行通信和跨节点 KV 传输。这些仓库独立演化,但一项推理服务成果可能同时依赖其中多个仓库的改动。

#### Harness 仓库(Harness Repos)

**代码不会仅仅因为 Agent 能够编辑它,就变成一项工程成果。**Harness 仓库提供让改动走完生命周期剩余环节的能力:寻找计算资源、准备环境、部署服务、运行性能与正确性评估、诊断故障与线上行为、保存长期记录,以及执行安全边界。它们把原本彼此割裂的运维步骤,变成一条从代码改动到经过验证的交付物的可重复路径。

**三组仓库共同构成一条完整的工程路径:内置工作区准备并协调工作,推理栈仓库提供被改动的系统,Harness 仓库则把改动送往验证。**Infer-forge 把它们纳入同一个工作区,却不强迫它们进入同一个仓库历史、归属模型或发布流程。

## 4. 任务循环(Task Loop)

**MonoRepo 提供工作区;任务循环则规定工作如何随时间推进。**推理工程往往需要多轮的研究、实现、部署、评估与恢复。任务循环让这些执行始终对齐同一个目标与任务契约,直到它们通过经过验证的交付物或可靠的后续交接满足自己的退出标准。

**「万物皆任务(Everything Can Be a Task)」适用于可独立验证的工作单元,而非每一个动作。**一个任务需要自己的目标、范围、验收标准、验证路径与退出标准。命令和中间实验作为循环块(Loop Block)实例或工具调用留在任务内部。一旦某个工作单元能够独立完成或交接,它就可以成为更大任务图中的一个任务节点。

### 4.1 总览

<div align="center">
  <img src="/images/blog/infer-forge-loop/fig-03-task-loop-overview.svg" alt="The Task Loop moves from Task Definition into Main Loop, uses Task Goal Met? to continue or satisfy Exit Criteria, preserves Task Memory, and draws on four Harness capabilities" />
  <br>
  <em>图 3:任务循环总览。</em>
</div>

**任务循环保持自身边界稳定,同时允许执行路径灵活调整。****任务定义(Task Definition)**确立任务类型、起始上下文(Starting Context)、任务契约与退出标准。**主循环(Main Loop)**通过一序列**循环块**实例推进工作,并用**任务目标是否达成?(Task Goal Met?)**来判断是退出还是继续。**任务记忆(Task Memory)**在各轮迭代之间保存当前状态、下一个子目标(Sub-target)、执行记录(Execution Records)与交接。

**Harness 是环绕循环的外层,而不是循环内部的又一个阶段。**它提供执行期间所需的资源、方法、记忆系统、验证入口和安全边界。不同任务可以按不同顺序使用这些能力,而不必被迫穿过一条固定的流水线。

### 4.2 任务定义

<div align="center">
  <img src="/images/blog/infer-forge-loop/fig-04-task-definition.svg" alt="Task Definition consists of Task Type, Starting Context, Task Contract, and Exit Criteria" />
  <br>
  <em>图 4:任务定义。</em>
</div>

**任务循环始于一个可检验的承诺,而非始于动作本身。**在 Agent 检索代码库、发起部署或占用评估资源之前,任务必须先说清楚它想完成什么、结果将如何被评判。**任务定义**确立四个锚点:

- **任务类型(Task Type)**选定一份默认的 Playbook(预置操作手册)。
- **起始上下文(Starting Context)**记录执行开始时的状态。
- **任务契约(Task Contract)**固定目标(Goal)、范围(Scope)、验收标准(Acceptance)与验证(Verification)。
- **退出标准(Exit Criteria)**定义执行必须产出的持久**交付物(Deliverable)**或**后续交接(Follow-up Handoff)**。

#### 4.2.1 任务类型(Task Type)

**Playbook 把以往实践转化为先发优势。**它为每种任务类型提供一份轻量、可调整的模板:哪些仓库可能相关,哪些 **Skills**、**Tools & CLI** 和验证入口可用,以及哪些安全边界适用。这缩小了 Agent 在开展有效工作之前必须搜索的空间。

**Playbook 标准化的是起步方式,而不是完整的执行路径。**随着**任务契约**和新证据的要求,Agent 可以改变方法、引入新的循环块实例,或使用模板之外的能力。它减少重复摸索,但不取代工程判断。

**每种任务类型都对应推理工程中一类可验证工作的独特单元:**

- **规划(Plan)**定义目标、约束与拆解方式,并为下游任务产出可执行的计划。
- **研究(Research)**调查一个有界的不确定性,评估可得证据,并给出带有明确局限性的结论。
- **编码(Code)**实现任何范围内的代码改动,并连同其验证证据一起交付。
- **集成(Integration)**汇集来自多个上游任务的改动(包括跨仓库或跨组件的改动),并验证组合后的系统。
- **评估(Evaluation)**运行功能、性能、精度、压力与稳定性测试,并交付对照验收标准的证据。
- **发布(Release)**推动通过验证的候选版本走完审批、金丝雀发布、扩大放量或回滚流程,并记录结果。
- **在线诊断(Online Diagnosis)**在只读边界内调查生产问题,并把所需的改动移交给下游任务。
- **能力(Capability)**通过 `Add`、`Update`、`Merge`、`Retire` 或 `No Change` 维护带版本的 **Skills & Tools** 集合。
- **+ 自定义(+ Custom)**处理没有可复用 Playbook 的可验证工作,同时保持同样的任务定义结构。

**这套分类法是靠反复实践挣来的。**只有当某类活动的起步惯例、验收边界和交付物足够稳定、能够指导后续工作时,它才会成为内置任务类型。标准化追随已被证明的实践,而不试图提前预测每一条路径。

#### 4.2.2 起始上下文(Starting Context)

**起始上下文划清了已知状态与假设之间的界限。**一个任务可能从空白状态、准备好的环境或上游结果开始。关键在于,该状态的来源与验证状态必须保持显式。

- **自定义准备(Custom Setup)**记录为当前任务准备的条件,例如模型、容器镜像、部署配置档、仓库版本、数据集或实验入口。
- **导入上下文(Imported Context)**承接上游环境、中间结果或**后续交接**,连同其来源与验证状态一并带入。

#### 4.2.3 任务契约(Task Contract)

**任务契约让目标保持不动,而执行可以灵活变通。****目标**陈述期望的成果,**范围**框定工作的边界,**验收标准**陈述成功所需的可观察条件,**验证**则定义评判它们所需的证据<sup>[6](#ref-6)</sup>。没有这道边界,Agent 只需在看到结果之后改一改问题本身,就能显得成功了。

对一个推理优化任务而言,契约可以固定模型与权重格式、硬件部署位置、服务拓扑、运行时版本、负载矩阵与基线。验收标准随之可以要求在不损害精度或稳定性的前提下取得更好的吞吐量、TTFT 或 TPOT。在看到结果之后再更改拓扑、GPU 型号或负载,那是变更契约——而不是优化成果。

**证据可以改变主循环的方向,但绝不能悄悄挪动终点线。**不实质性改变目标、范围或验收标准的澄清必须显式记录;而其中任何一项的实质性变更都意味着开启一个新任务。

#### 4.2.4 退出标准(Exit Criteria)

**一个任务并不因为活动停止而结束;它在其状态可以被验证或可以安全延续时才结束。**

- **交付物**把完成的结果连同足以验证任务契约的证据一起打包。
- **后续交接**在需要另一个任务继续推进时,保留已完成的工作、当前状态、未解决的问题和下一个入口。

**退出标准把执行转化为持久的工程状态:要么是一个可验证的结果,要么是下一个任务的可靠起点。**

### 4.3 循环执行

<div align="center">
  <img src="/images/blog/infer-forge-loop/fig-05-loop-execution.svg" alt="Loop Execution defines a Loop Block, uses Execution Routing to choose Model Tier and Agent Topology independently, executes the block, and uses Task Goal Met? to exit or continue while Task Memory carries the Current Loop Block, a Loop Block Handoff, and the Next Loop Block across iterations" />
  <br>
  <em>图 5:循环执行。</em>
</div>

**任务的规模取决于其工程目标,而不是运行时会话的时长。**任务契约定义完整目标;主循环随着证据的浮现,通过一个或多个**循环块**实例将其实现。用户在定义任务时,无需预测它能否在单次持续运行的循环内完成。

**任务是连续性的单位;循环块是执行的单位。**每个循环块拥有一个子目标、一个退出条件、一次路由决策和一组执行记录。Claude Code 的 `/loop` 和 Codex 的 `/goal` 是当前的执行入口,但它们都不决定任务的范围。

#### 4.3.1 主循环(Main Loop)

**主循环把一个开放式的任务变成一串不断产出证据的循环块:**

- **定义循环块(Define Loop Block)**选定当前子目标与退出条件。
- **执行路由(Execution Routing)**为该子目标选择模型档位(Model Tier)与 Agent 拓扑(Agent Topology)。
- **执行循环块(Execute Loop Block)**通过某个可用的持续执行入口运行该循环块。
- **任务目标是否达成?**将积累的状态与任务契约对照,决定退出还是再定义下一个循环块。

**完成一个循环块不等于完成任务。**一个循环块可能确认一个假设、否决一条路线,或暴露一个新约束。它的退出条件只关闭那一个局部工作单元;**任务目标是否达成?**才决定积累的证据是否满足整个任务契约。「是」分支走向退出标准,「否」分支则基于已产出的证据定义下一个循环块。

#### 4.3.2 任务记忆(Task Memory)

**任务记忆让循环块序列持久且可追溯。**它保存已完成的循环块和正在进行的当前循环块,包括各自的子目标与退出条件。只有在当前循环块结束、且**任务目标是否达成?**判定任务必须继续之后,才会记录下一个循环块。

**执行记录捕捉 Agent 在每一步做了什么、产出了什么结果。**它们让执行可审计、可追溯、可复现。

**循环块交接在单个任务内部传递状态;图级交接边(Handoff edge)连接的是相互独立的任务节点实例。**

#### 4.3.3 执行路由(Execution Routing)

**执行路由为当前循环块做两个相互正交的选择:**

- **模型档位(Model Tier)**跟随推理难度。不确定性、推理深度和所需的专业知识决定该循环块使用**低档(Lower-tier)**、**中档(Mid-tier)**还是**最强可用(Strongest Available)**的模型。
- **Agent 拓扑(Agent Topology)**跟随内容体量与预期的上下文长度。能够可靠容纳在单个上下文内的工作使用**单 Agent(Single Agent)**;必须拆分到多个上下文的工作使用**多 Agent(Multi-Agent)**<sup>[14](#ref-14)</sup>。

一个困难但紧凑的问题可以用**最强可用**搭配**单 Agent**。一个庞大但常规的评估矩阵可以用**低档**或**中档**搭配**多 Agent**。模型档位提供推理能力;Agent 拓扑管理上下文负载。

图 5 展示了一种可能的**多 Agent** 拓扑:**协调者(Coordinator)**与 Infra、Code、Eval 协同工作,而**审查者(Reviewer)**在主执行链之外审视结果<sup>[7](#ref-7)</sup>。这些角色仅作示意;实际拆分取决于当前循环块的内容与上下文需求。

如果模型档位选择或子 Agent 不可用,循环块将以运行时提供的能力继续执行,并把这一降级情况保留在其执行记录中。

### 4.4 Harness(执行框架)

**只有 Harness 能支撑起执行,任务循环才能持续推进。**没有稳定的 Harness,每个循环块都得重新寻找机器、重建环境、定位命令、找回证据、重新协商安全边界。Infer-forge 则提供一个由**节点注册表(Node Registry)**、**Skills & Tools**、**Journal** 和**安全护栏(Safety Guard)**构成的统一执行底座。

**价值在于组合,而非任何单项能力。**完成任务定义之后,Agent 就可以查看资源状态、准备环境、部署负载、修改并评估系统,必要时在另一个节点上恢复。节点状态、操作方法、执行历史与安全约束在整个过程中保持关联,因此人不必在每个步骤之间重新铺路。

#### 4.4.1 节点注册表(Node Registry)

<div align="center">
  <img src="/images/blog/infer-forge-loop/fig-06-node-registry.svg" alt="Node Registry combines periodic runtime and GPU observations to determine claim cleanup eligibility." />
  <br>
  <em>图 6:节点注册表。</em>
</div>

**资源自主必须从可证明的归属开始,而不是靠猜。****节点注册表**是一本以 Git 为底座的台账,记录每一次任务对节点的占用声明(claim)。采集器定期把运行时进程与 GPU 活动的观测写入注册表,形成连续、可审计的历史。GPU 遥测只是信号之一;任何单个采样都无法断定一个任务已经结束。

**清理默认从严(fail-closed)。**只有当新鲜、无缺口的观测显示运行时与 GPU 活动在一段可配置的策略窗口内持续空闲时,占用声明才有资格进入清理。缺失、过期、有缺口或相互矛盾的证据都会阻止清理;运行时仍活跃/GPU 空闲的节点需要人工审查。

**获得资格不等于执行,清理不等于复用。**清理必须被显式触发,而且只移除注册表中的占用声明。它既不会终止负载,也不能证明任务已完成。在节点被复用之前,其当前机器状态必须重新验证。

**节点注册表不是调度器,也不启动负载。它的角色更窄——也更为基础:维护一种可审计的资源状态,让清理、分配与部署决策可以信赖。**

#### 4.4.2 Skills & Tools

<div align="center">
  <img src="/images/blog/infer-forge-loop/fig-07-skills-and-tools.svg" alt="Skills are organized across SGLang Upstream, Cross-lib, Task, and Ops, while Tools & CLI include Deploy, Build, Pull Weights, Sync Code, Evaluate, Profile, Diagnose Online, and Monitor" />
  <br>
  <em>图 7:Skills & Tools。</em>
</div>

**一个有能力的 Agent 不应该在每个任务里都重新摸索同一件工程工作怎么做。****Skills** 在 SGLang Upstream、跨库(Cross-lib)、任务(Task)和运维(Ops)四个范围内保存可复用的方法。**Tools & CLI** 为部署、构建、权重与代码同步、评估、性能剖析(profiling)、在线诊断和监控暴露稳定、可记录的接口。

Playbook 为当前任务类型选取相关的子集。Skills 缩小决策空间;Tools & CLI 把选定的决策变成一个输入输出都能进入执行记录的动作。Agent 从积累的实践出发,而不必被迫走一条固定的路径。

**Skills & Tools 是一个带版本的能力基线,而不是越堆越高的指令堆。**普通任务使用当前基线。能力任务(Capability Task)利用 Journal 证据,并在 `Model or runtime change`(模型或运行时变更)之后进行复核,以决定哪些应当新增、更新、合并、退役或保持不变。

#### 4.4.3 Journal(工程日志)

<div align="center">
  <img src="/images/blog/infer-forge-loop/fig-08-journal.svg" alt="Journal uses LLM-wiki to connect records from multiple Tasks and Multi-dim Index fields such as Model, Type, and GPU to support Retrieve, Compare, and Filter" />
  <br>
  <em>图 8:Journal。</em>
</div>

**只有当下一个任务能够找到并复用证据时,证据才会产生复利。**任务记忆保存单个任务的执行状态;**Journal** 则让证据跨越任务流动。**LLM-wiki** 把任务记录连成一个知识网络;**多维索引(Multi-dim Index)**按模型、任务类型、GPU 等维度组织它们。二者共同支持检索(Retrieve)、比较(Compare)与过滤(Filter),不必让每个任务都重新发现同样的事实。

在 SGLang OpenAI 兼容 chat 基准处理器的早期版本中,流式返回的 `delta.reasoning_content` 未被计入 TTFT 与输出统计(已在 [sgl-project/sglang#23954](https://github.com/sgl-project/sglang/pull/23954) 修复);非流式处理则在 [#25298](https://github.com/sgl-project/sglang/pull/25298) 中单独解决。Journal 在后来的一个任务中把这条历史记录重新翻了出来,避免了一次测量误差被误判为引擎回退。

**Journal 保存证据;它不能把证据直接拔擢为可执行的能力。**对 Skills & Tools 基线的任何更改都必须经过能力任务和验证。

#### 4.4.4 安全护栏(Safety Guard)

<div align="center">
  <img src="/images/blog/infer-forge-loop/fig-09-safety-guard.svg" alt="Safety Guard constrains execution through Push Guard, Traceable Path, Env Isolation, Production Read-only Access, Secrets, Data, Human Gate, and Cross-Model Adversarial Review" />
  <br>
  <em>图 9:安全护栏。</em>
</div>

**随着 Agent 执行变得更长、更并发,一个未被拦截的错误可以传播得更远。**因此,**安全护栏**施加任何 Playbook 或循环块都不得绕过的约束:

- **推送护栏(Push Guard)**与**可追溯路径(Traceable Path)**约束代码改动的流动方式。
- **环境隔离(Env Isolation)**与**生产环境只读访问(Production Read-only Access)**约束环境与生产操作。
- **密钥(Secrets)**与**数据(Data)**约束对凭据和受管数据集的访问。
- **人工门控(Human Gate)**要求高风险动作必须获得批准。
- **跨模型对抗式审查(Cross-Model Adversarial Review)**实行 `reviewer ≠ coder`(审查者与编码者使用不同模型),以减少自我审查的盲区<sup>[6](#ref-6)</sup>。

**安全护栏约束行动;验证约束论断。**在一个算子优化任务中,一个候选版本看似达到了 `72.30 TFLOPS`,比对照点提升 `5.7%`。后续验证暴露了一个竞态:聚合统计看似稳定,但个别元素已经损坏。该候选在进入集成之前就被否决。

**可靠的自主体不仅以它完成了什么来衡量,也以它拒绝推进什么来衡量。**在推理工程中,拦下一个虚假的性能提升,可能比再产出一个补丁更有价值。

## 5. 任务图(Task Graphs)

<div align="center">
  <img src="/images/blog/infer-forge-loop/fig-10-task-graph.svg" alt="Task Graph defines Task node, Shared repo, and External system as graph elements, shows Verification before Handoff, and distinguishes Handoff edge, State edge, and Control edge" />
  <br>
  <em>图 10:任务图:元素、交接与边类型。</em>
</div>

**一个项目的扩展并非仅仅靠创建更多任务;当依赖、共享状态和控制决策变得显式时,扩展才会发生。**任务循环给单个任务一条独立走向收敛的路径;任务图把这些收敛单元连接起来,却不消解它们各自的验证边界。

**任务图不是固定的工作流模板,也不是封闭的分类体系。**只要多个任务需要显式的依赖、经过验证的交接、共享状态或控制关系,它们就可以被组织成一个任务图。任务图可以服务于一个项目、一项调查、一次发布,或任何超出单个任务边界的目标。

**交付图(Delivery Graph)与能力图(Capability Graph)是两个反复出现的例子,并非唯一有效的图结构。**我们用它们在两种常见情境下演示同一套图语言:协调共同改动推理系统的多个任务,以及维护未来任务要用的能力。

**图的正确性始于把执行与状态、外部控制区分开。**只有**任务节点(Task node)**执行工作并运行任务循环。**共享仓库(Shared repo)**存储持久状态,但不运行循环。**外部系统(External system)**表示从 infer-forge 之外与图交互的人或平台。

边的类型说明跨越每条边界的是什么:

- **交接边(Handoff edge)**承载经过验证的交付物或后续交接,它们将成为后继任务的导入上下文。
- **状态边(State edge)**表示对共享仓库的一次读或写;它并不意味着任务完成或已验证。
- **控制边(Control edge)**触发工作、将其退回修改或改变其方向,但不承载经过验证的结果。

**一次写入不是交接;一次触发不是交付物;仅仅连通并不等于经过验证的进展。**

### 5.1 交付图(Delivery Graph)

<div align="center">
  <img src="/images/blog/infer-forge-loop/fig-11-delivery-graph.svg" alt="Delivery Graph fans a Plan Task out to parallel Code Tasks, converges them through Integration, Evaluation, and Release Tasks, and uses external Signals plus Feedback, Rework, and Hotfix to change subsequent work" />
  <br>
  <em>图 11:交付图:交付生命周期。</em>
</div>

**推理交付是一个收敛问题,而不是一张核对清单。**一个规划任务可以把目标拆分为预填充(prefill)、解码(decode)、算子、通信和部署等工作线(workstream)。研究与编码任务随后各自独立、并行推进,每一个都在自己的任务契约下产出证据。

**集成是并行工作汇聚成一个可运行部署点的地方。**它把横跨引擎、库、镜像和部署配置的改动装配到一起。组合后的候选随后进入评估,模型、服务场景、硬件、性能、精度与稳定性条件全部固定。失败的结果经由 `Rework`(返工)退回,而不是以部分成功蒙混过关。

**发布是一次经过验证的状态迁移,而不是图上的最后一个方框。**只有通过评估的候选才能经由后续交接抵达发布。外部 `Signals`(信号)可能触发在线诊断;诊断发现经由 `Feedback`(反馈)回流,或通过 `Hotfix`(热修复)启动一个编码任务。这些控制边可以改变工作方向,但不能绕过集成或评估。

**交付图强迫每条路径都经由证据收敛,从而让并行变得有用。**

### 5.2 能力图(Capability Graph)

<div align="center">
  <img src="/images/blog/infer-forge-loop/fig-12-capability-graph.svg" alt="In the Capability Graph, Journal commit event, Scheduled trigger, and Model or runtime change wake Capability Task; it scans evidence, reconciles the current Skills & Tools baseline, and after Verification produces Add, Update, Merge, Retire, or No Change, with Follow-up Handoff available for further Tasks" />
  <br>
  <em>图 12:能力图:能力演化。</em>
</div>

**交付图改变的是推理系统;能力图改变的是执行这项工作的系统本身。**任务执行使用当前的 Skills & Tools 基线,并把实践中的证据记入 Journal。跨任务来看,重复的步骤、可复用的命令、工作流模式和已被证明有效的修复,都会成为能力维护的候选。

**Journal 是证据,不是权威。**`Journal commit event`(Journal 提交事件)、`Scheduled trigger`(定时触发)和 `Model or runtime change`(模型或运行时变更)都可以唤醒一个能力任务,但它们哪一个都不能证明可执行行为就该改变。该任务扫描 Journal 增量、读取当前基线,并通过验证产出 `Add`、`Update`、`Merge`、`Retire` 或 `No Change`。

**每一项能力都有携带成本和保质期。**有些 Skills 保存持久的项目知识;另一些则是为特定模型或运行时打的补丁。随着这些系统的改进,旧的脚手架可能消耗上下文(Context)、与较新的行为冲突,或束缚判断。Claude Code 团队报告,针对新模型删掉了系统提示词的 80% 以上,而在编程评测中没有可测量的损失<sup>[15](#ref-15)</sup>。Boris Cherny 也单独倡导定期修剪 `CLAUDE.md` 文件、Skills 和 hooks<sup>[16](#ref-16)</sup>。

因此,`Model or runtime change` 会触发对当前基线的复核。能力移除是一种证据驱动的消融方法,而不是一揽子删除;除非证据支持修改,安全边界和已验证的不变式保持不变。**一个只支持 `Add` 的能力集合不会演化——它只会积累债务。**

如果某个候选需要实现、评估或发布工作,能力任务会产出一个指向相应任务的后续交接。**能力图既防止原始经验直接变异可执行行为,又确保经过验证的经验不会滞留在 Journal 里。**

## 6. 一名工程师,多条循环

**本章跟随一名 AI 基础设施工程师,从持续的任务执行走向并行工作与项目级协同。**

### 6.1 从执行到判断

<div align="center">
  <img src="/images/blog/infer-forge-loop/fig-13-parallel-task-loops.svg" alt="One Human and four Agents share a single left-to-right timeline, each on its own lane. The Human lane is one continuous track carrying Define Task A, Define Task B, and Define Task C, then a plain grey block with no label for a stretch of unrelated engineering work, then Review Evidence A and Define Task D. Each Define Task block is filled with the colour of the Agent it starts, and a dashed vertical line in that same colour runs from its lower right corner down to the top left corner of the matching Execute Task bar; where such a line crosses a bar that is still running, it is drawn over a white channel so it stays legible. The four Agent lanes are each labelled simply Agent — the letters belong to the Tasks, not to the Agents — and are told apart by colour. Execute Task A runs from the end of its definition through the whole stretch in which the Human defines two more Tasks and turns to other work, and a green arrow rises from the bar's right edge — the moment it finishes — to Review Evidence A, closing one loop. Execute Task B, Execute Task C, and Execute Task D all continue to the right edge of the time axis, so they are still running when the figure ends. A faded lane labelled More Agents holds dashed placeholder bars, showing that more can be started" />
  <br>
  <em>图 13:一名工程师指挥多条持续运行的任务循环。</em>
</div>

**当工程师不在场时执行仍能继续,AI 基础设施工程就发生了改变。**一旦工程师完成任务定义并设置好必要的人工门控,Agent 就能在数小时乃至数天里,把工作推进过环境搭建、部署、评估、恢复与迭代。任务循环让这些执行始终与任务契约、其证据以及下一个决策保持连接。

图 13 展示了由此形成的工作模式。当一个任务循环仍在执行时,工程师可以定义另一个任务、审查已完成的证据,或转身去做不相关的工程工作。工程师不再需要亲自推进每一条命令序列;稀缺的注意力从执行转向判断:设定约束、评估证据、解决取舍,以及决定下一步该推进什么。

**因此,一名工程师可以指挥多条持续运行的任务循环,同时不模糊每个任务的边界。**Harness 负责把执行向前推进;工程师把注意力集中在能改变项目走向的地方。

### 6.2 在飞任务观测数据

<div align="center">
  <img src="/images/blog/infer-forge-loop/fig-14-task-activity.svg" alt="Archived Task Lifetimes plots each of the 86 archived Tasks as one horizontal bar running from its creation to its archive time, between April 7 and July 30, 2026. Bars are packed into nine lanes by earliest free lane, and are coloured across all nine Task Types—Plan, Research, Code, Integration, Evaluation, Release, Online Diagnosis, Capability and + Custom. A dark slate dashed line at July 6, drawn over a white underlay so it stays legible where it crosses coloured bars, marks the peak, where nine Tasks are in flight; its label reads Peak in flight: 9. Three cards below the timeline give the summary statistics: 90 Tasks created, 86 valid archived lifetimes, and 91% in flight with others — the last one filled solid because it is the conclusion the other two support" />
  <br>
  <em>图 14:在飞任务,2026 年 4 月至 7 月。</em>
</div>

**图 14 展示了四个月里该工程师在飞任务的变化。**每根横条从一个任务的创建时间戳延伸到其归档时间戳,峰值则是这些区间在任一时刻的最大重叠数。观测窗口内创建的 90 个任务中,86 个已归档任务具有有效时间戳并被纳入统计;三个在截止时点仍未关闭;另有一条记录因归档时间戳早于创建时间戳而被排除。

在 4 月至 7 月的记录中,已归档任务的生命周期中位数逐月上升:4 月约 **10 小时**、5 月约 **14 小时**、6 月约 **20 小时**、7 月约 **28 小时**。各月的**在飞任务**峰值分别为 **2**、**2**、**6** 和 **9**。

### 6.3 项目级协同

<div align="center">
  <img src="/images/blog/infer-forge-loop/fig-15-deepseek-v4-pro-task-graph.svg" alt="A Task Graph from one DeepSeek-V4-Pro serving delivery connects SERVING BASELINE, PREFILL, DECODE, and RELEASE; dashed nodes mark paths that did not enter the final release, adjacent labels explain each outcome, an amber Control edge records a cross-workstream constraint, and SHARED STATE connects Journal, Capability Task, and Skills & Tools" />
  <br>
  <em>图 15:一个任务图协同一次项目级的服务交付。</em>
</div>

**一名工程师通过横跨七种任务类型的 38 个可独立验证的任务节点,协调完成了[*Pushing the Limits of Serving DeepSeek-V4-Pro*](https://www.lmsys.org/blog/2026-08-19-deepseek-v4-pro-engine-optimization-h20)<sup>[18](#ref-18)</sup> 一文所述的工作。**任务图组织了四条服务工作线——短上下文预填充、长上下文预填充、低延迟解码和高吞吐解码——使它们能够独立推进,同时共享同一次发布所需的决策、约束与验证证据。四条工作线分别收敛到四个不同的部署点,而不是一个放之四海皆准的最优解。

一个解码任务保持开启长达 **9 天**,而其他工作线在图中其他位置继续推进。任务图避免了这一长时间运行的任务阻塞整个项目。没有哪个 Agent 或任务需要独自保有整个项目的上下文:每条工作线都可以对照自己的任务契约走向收敛,然后把经过验证的交付物贡献给更大的发布。

**该项目产出了四个已发布的服务配置档,并保留了七条未进入最终发布的路径。**这些路径本身就是工程成果的一部分:它们记录了评估过什么、为何没有继续推进,以及下游任务不必再重新发现的东西。

**这套运行模式就是这样扩展的:一名工程师可以指挥多条持续运行的任务循环,通过任务图使它们收敛,并同时保全已发布的系统和其背后的决策。**

## 7. 层层累积

<div align="center">
  <img src="/images/blog/infer-forge-loop/fig-16-layers-accumulate.svg" alt="Context becomes the execution core of Harness, Harness remains inside Task Loop, and Task nodes that preserve these layers compose into Task Graph" />
  <br>
  <em>图 16:层层累积:从上下文到任务图。</em>
</div>

**Harness 把一次执行本地的上下文(Context),转化为让必须延续的工作得以依托的持久结构。**上下文保存一次执行所需的目标、代码、当前状态与工作中的判断。Harness 挑选出值得超越单次执行而存续的内容,将其外化以供复用,并提供稳定的工具、环境、记忆、验证入口与安全边界<sup>[9](#ref-9)</sup>。图 16 描绘的是一种累积,而非更替:上下文成为 Harness 的执行核心;Harness 依然是每个任务循环的承重地基;任务图则把这些任务循环连接成项目规模的工作。每一个更高的层都扩展了下层的覆盖范围,而不移除它们的能力或约束。

**抽象可以在数月间更迭;可靠性却要一层一层挣得。**本文引用的代表性文章在短短五个多月里,帮助把执行框架工程、循环工程与图工程凝结为一种共享词汇<sup>[2](#ref-2),[4](#ref-4),[13](#ref-13)</sup>;但它们之间的依赖是根本性的,而不是时间先后的。不完整的上下文会危及一次执行。Harness 中的一个弱点——过时的知识、有缺陷的工具或缺失的约束——会在整个任务循环中反复出现,并在任务图中传播。更高的层会同时放大其下各层的优点与缺点。**循环工程与图工程并不取代执行框架工程;它们只是让更多的东西依赖于它。**

## 8. 经验教训

### 8.1 任务粒度

**任务边界应画在验证能够独立成立的地方。**一个任务需要自己的任务契约——目标、范围、验收标准与验证——以及自己的退出标准。在任务契约保持不变的前提下,只改变子目标或退出条件的工作,应归入另一个循环块。需要实质性不同的目标、范围或验收标准的工作,应归入一个新任务。过大的任务会掩盖彼此独立的证据;过小的任务则把执行变成协调开销。

那个为期 9 天的解码任务带来的教训,并不是「9 天本身就太长了」。受同一套性能、精度与稳定性契约约束的实验,本应放在前后相继的循环块中;而需要独立目标、范围或验收标准的方向,本应各自成为独立的任务。一个实用的检验是问:失败之后,执行应该回到哪里——下一个循环块,还是一份新的任务定义?

**按契约的变化切分,而不是按时间的流逝切分。**

### 8.2 证据驱动的任务图

**任务图应该吸收证据,而不是冻结假设。**规划任务定义的是当前最可信的初始拆解,但任务图必须能随证据变化而演化<sup>[13](#ref-13)</sup>。研究可能否决一条路径,评估可能产出 `Rework` 或一个新的编码任务,在线诊断的反馈可能改变后续工作的范围。作为对经过验证的证据的回应,任务图可以增加、移除或重排任务节点。

下游任务可以更早被规划,但在上游结果通过验证、跨过一条交接边之前,它不得导入该结果。在 DeepSeek-V4-Pro 的任务图中,被否决的方向、`Rework` 路径和跨工作线约束在最初计划里并不存在;它们是在执行产出证据之后才进入图中的。

**一张规划之后就无法变更的图,记录的是意图,而不是工程。**

### 8.3 证据完整性

**证据的可信度不会超过生产它的 Harness。**评估工具、配置和数据路径本身就是结果的一部分。它们需要与被测代码同样的版本管理、审查和验证。

**交付物必须保留复现路径,而不仅仅是一个结论。**对推理工作而言,它应包含足够的信息来重建部署点,并将基线与候选进行对比:确切的代码与运行时版本、镜像、部署与负载配置、命令、结果,以及失败的尝试。一份后续交接说明什么已完成、证据存放在哪里、哪些判断依然成立,以及下一个任务应从哪里开始。这份包裹一经验证并被导入,就成为导入上下文(Imported Context)。

**如果下一个任务必须重建环境、或只能相信一句断言,那么这项工作就没有被交付。**

## 9. 结语

**Infer-forge 并不降低推理工程的复杂性;它让贯穿这种复杂性的工作变得可审查、可续行、可验证。**它让每一处改动都与自己的部署点、代码来源和证据绑定,贯穿多个仓库、多轮执行和多次后续交接,使经过验证的交付物与留档的否决都能被复现、重访和继承。

**Infer-forge 支撑这样一种运行模式:一名 AI 基础设施工程师可以指挥多条持续运行的任务循环。**我们四个月的记录显示,观测到的**在飞任务**峰值从 **2** 增长到 **9**。我们正在探索自主程度越来越高的任务图协同,同时保持验证边界、人工门控与工程判断。我们希望 infer-forge 体现的实践,能帮助团队和个人把执行框架工程、循环工程与图工程应用于大规模复杂系统。

## 致谢

我们感谢 SGLang 团队和更广泛的 SGLang 社区开发并开放分享那些支撑 Agent 辅助 SGLang 开发的 Skills<sup>[8](#ref-8)</sup>。我们也感谢 SGLang 社区的 **Peng Zhang**。我们特别感谢 **Xiaoyu Zhang (BBuf)** 创建并分享 `AI-Infra-Auto-Driven-SKILLS` 集合<sup>[17](#ref-17)</sup>。

我们同样感谢本文引用的研究者与工程团队。他们在执行框架工程、循环工程与图工程上的工作,帮助塑造了 infer-forge 背后的概念与方法。

## 参考文献

1. <a id="ref-1"></a>Vivek Trivedy — [The Anatomy of an Agent Harness](https://www.langchain.com/blog/the-anatomy-of-an-agent-harness), LangChain, March 10, 2026.
2. <a id="ref-2"></a>Ryan Lopopolo — [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering/), OpenAI, February 11, 2026.
3. <a id="ref-3"></a>Birgitta Böckeler — [Harness engineering for coding agent users](https://martinfowler.com/articles/harness-engineering.html), Martin Fowler, April 2, 2026.
4. <a id="ref-4"></a>Addy Osmani — [Loop Engineering](https://addyosmani.com/blog/loop-engineering/), June 7, 2026.
5. <a id="ref-5"></a>Sydney Runkle — [The Art of Loop Engineering](https://www.langchain.com/blog/the-art-of-loop-engineering), LangChain, June 16, 2026.
6. <a id="ref-6"></a>Prithvi Rajasekaran — [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps), Anthropic, March 24, 2026.
7. <a id="ref-7"></a>Erik Schluntz and Barry Zhang — [Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents), Anthropic, December 19, 2024.
8. <a id="ref-8"></a>SGLang Team — [Agent-Assisted SGLang Development: An Initial Exploration](https://www.lmsys.org/blog/2026-07-02-agent-assisted-sglang-development), LMSYS Org, July 2, 2026.
9. <a id="ref-9"></a>Lilian Weng — [Harness Engineering for Self-Improvement](https://lilianweng.github.io/posts/2026-07-04-harness/), Lil'Log, July 4, 2026.
10. <a id="ref-10"></a>Boye Niu et al. — [Flow: Modularized Agentic Workflow Automation](https://arxiv.org/abs/2501.07834), arXiv:2501.07834, 2025.
11. <a id="ref-11"></a>Andy Xu and Yu-Wing Tai — [Meta-Agent: From Task Descriptions to Verified Multi-Agent Systems](https://arxiv.org/abs/2605.25233), arXiv:2605.25233, 2026.
12. <a id="ref-12"></a>Ao Li et al. — [GraphFlow: A Graph-Based Workflow Management for Efficient LLM-Agent Serving](https://arxiv.org/abs/2605.22566), arXiv:2605.22566, 2026.
13. <a id="ref-13"></a>Sydney Runkle and Harrison Chase — [3 Years of Graph Engineering with LangGraph](https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph), LangChain, July 22, 2026.
14. <a id="ref-14"></a>Nelson F. Liu et al. — [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172), TACL 2023 / arXiv:2307.03172.
15. <a id="ref-15"></a>Thariq Shihipar — [The New Rules of Context Engineering for Claude 5 Generation Models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models), Claude, July 24, 2026.
16. <a id="ref-16"></a>Boris Cherny and Diana Hu — [Boris Cherny: Building Claude Code](https://www.ycrootaccess.com/p/boris-cherny-building-claude-code), Y Combinator Startup School, July 27, 2026.
17. <a id="ref-17"></a>Xiaoyu Zhang (BBuf) — [AI-Infra-Auto-Driven-SKILLS](https://github.com/BBuf/AI-Infra-Auto-Driven-SKILLS), GitHub.
18. <a id="ref-18"></a>Tianyu Zhang, Yusong Gao, Yun Zhang — [Pushing the Limits of Serving DeepSeek-V4-Pro on Compute-Constrained NVIDIA H20](https://www.lmsys.org/blog/2026-08-19-deepseek-v4-pro-engine-optimization-h20), LMSYS Org, August 19, 2026.
