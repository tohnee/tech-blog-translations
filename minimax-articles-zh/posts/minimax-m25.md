---
title: "MiniMax M2.5：为真实世界的生产力而生。"
date: 2026-02-12
source: https://www.minimax.io/blog/minimax-m25
crawled: 2026-09-22
title_en: "MiniMax M2.5: Built for Real-World Productivity."
translated: 2026-09-22
---

# MiniMax M2.5：为真实世界的生产力而生。

> 原文：[MiniMax M2.5: Built for Real-World Productivity.](https://www.minimax.io/blog/minimax-m25) · MiniMax

2026-02-12

M2.5模型发布

[接入 API →](https://platform.minimax.io/docs/api-reference/text-anthropic-api)[Coding Plan 订阅 →](https://platform.minimax.io/subscribe/coding-plan)[立即体验 Agent →](https://agent.minimax.io/)

![MiniMax M2.5](https://file.cdn.minimax.io/public/60e15b62-aece-42ab-898f-ce97c59f3941.png)

![](https://file.cdn.minimax.io/public/97f76950-2c60-4a9b-bb96-228454afabe9.png)

今天我们推出最新模型 **MiniMax-M2.5。**
  
M2.5 在数十万个复杂真实世界环境中经过大量强化学习训练，在**编程、智能体工具使用与搜索、办公工作以及其他一系列具有经济价值的任务上达到 SOTA**，取得 **SWE-Bench Verified 80.2%**、**Multi-SWE-Bench 51.3%**、**BrowseComp 76.3%**（含上下文管理）的成绩。
  
M2.5 被训练为高效推理、最优分解任务，在执行复杂智能体任务时展现出惊人的速度，完成 SWE-Bench Verified 评测比 M2.1 **快 37%**，与 **Claude Opus 4.6** 的速度相当。
  
M2.5 是首个让用户无需为成本担忧的前沿模型，兑现了「智能便宜到无需计量」的承诺。**以每秒 100 个 token 的速率连续运行一小时，成本仅为 1 美元。** 在每秒 50 个 token 的速率下，成本降至 0.30 美元。我们希望 M2.5 的速度与成本效益能够催生创新的新型智能体应用。

### 编程

在编程评测中，MiniMax-M2.5 较前几代有大幅提升，达到 SOTA 水平。M2.5 在多语言编程任务上的表现尤为突出。

![](https://file.cdn.minimax.io/public/54ddb070-9654-47a0-83c4-1bbf7c7ff0d5.png)

与前几代相比的一项重大改进，是 M2.5 像架构师一样思考与规划的能力。模型的规格说明书（Spec）撰写倾向在训练中自然涌现：在编写任何代码之前，M2.5 会主动从一位经验丰富的软件架构师的视角，对项目的功能、结构与 UI 设计进行分解和规划。
  
M2.5 在超过 20 万个真实世界环境中、基于 10 余种语言（包括 Go、C、C++、TypeScript、Rust、Kotlin、Python、Java、JavaScript、PHP、Lua、Dart、Ruby）接受了训练。它远不止于修 bug，而是在复杂系统的整个开发生命周期中提供可靠表现：从 0 到 1 的系统设计与环境搭建，到 1 到 10 的系统开发，再到 10 到 90 的功能迭代，最后到 90 到 100 的全面代码评审与系统测试。它覆盖横跨 Web、Android、iOS、Windows 等多个平台的全栈项目，涵盖服务端 API、业务逻辑、数据库等，而不仅是前端网页 demo。
  
为了评估这些能力，我们还将 VIBE 基准升级为更复杂、更具挑战性的 Pro 版本，大幅提升了任务复杂度、领域覆盖面与评估精度。总体而言，M2.5 与 Opus 4.5 表现相当。

![](https://file.cdn.minimax.io/public/013a2750-d042-482b-a97f-d9c67906b286.png)

我们重点关注了模型在分布外脚手架（harness）上的泛化能力。我们使用不同的编程智能体脚手架在 SWE-Bench Verified 评测集上测试了性能。

- 在 Droid 上：79.7（M2.5）> 78.9（Opus 4.6）
- 在 OpenCode 上：76.1（M2.5）> 75.9（Opus 4.6）

### 搜索与工具调用

![](https://file.cdn.minimax.io/public/30812ab3-fa8d-439e-b731-c1f73b77c2ee.png)

高效的工具调用与搜索是模型自主处理更复杂任务的前提。在 BrowseComp 和 Wide Search 等基准评测中，M2.5 取得了业界领先的表现。与此同时，模型的泛化能力也有提升——面对陌生的脚手架环境时，M2.5 展现出更稳定的表现。
  
在专业人类专家执行研究任务时，使用搜索引擎只是整个过程中很小的一部分；大部分工作在于对信息密集的网页进行深度探索。为此，我们构建了 RISE（Realistic Interactive Search Evaluation，真实交互搜索评测）来衡量模型在真实专业任务上的搜索能力。结果表明，M2.5 在真实环境下擅长专家级搜索任务。
  
与前代相比，M2.5 在处理智能体任务时的决策能力也大幅提升：它学会了用更精确的搜索轮次和更高的 token 效率来解决问题。例如，在包括 BrowseComp、Wide Search 和 RISE 在内的多项智能体任务中，M2.5 用更少的轮次取得了更好的结果，轮次比 M2.1 减少约 20%。这表明模型不再只是把答案做对，而是在更高效的路径上推理出结果。

### 办公

M2.5 被训练为在办公场景中产出真正可交付的成果。为此，我们与**金融、法律、社会科学**等领域的资深专业人士深入合作。他们设计需求、提供反馈、参与制定标准，并直接参与数据构建，将各自行业的隐性知识带入模型的训练管线。基于这一基础，M2.5 在 Word、PowerPoint、Excel 财务建模等高价值办公场景中实现了显著的能力提升。在评测侧，我们构建了内部的 Cowork Agent 评测框架（GDPval-MM），通过两两对比同时评估交付成果的质量与智能体执行轨迹的专业度，并对整个工作流的 token 成本进行监控，以估算模型在真实世界中的生产力提升。与其他主流模型的对比中，它取得了 59.0% 的平均胜率。

![](https://file.cdn.minimax.io/public/0a215c3a-eb6d-422e-ad79-60b00b789608.png)

### 效率

因为真实世界充满截止日期与时间限制，任务完成速度是一种实际刚需。模型完成一项任务所需的时间取决于其任务分解效率、token 效率与推理速度。M2.5 以每秒 100 个 token 的速率原生提供服务，几乎是其他前沿模型的两倍。此外，我们的强化学习设置激励模型高效推理、最优地拆解任务。得益于这三点，M2.5 在复杂任务完成上节省了大量时间。
  
例如，在运行 SWE-Bench Verified 时，M2.5 每项任务平均消耗 352 万个 token。相比之下，M2.1 消耗 372 万个 token。同时，得益于并行工具调用等能力的改进，端到端运行时间从平均 31.3 分钟降至 22.8 分钟，速度提升 37%。这一运行时长与 Claude Opus 4.6 的 22.9 分钟相当，而每项任务的总成本仅为 Claude Opus 4.6 的 10%。

### 成本

我们设计 M2 系列基础模型的目标，是让复杂智能体的运行无需为成本担忧。我们相信 M2.5 已接近实现这一目标。我们发布两个版本的模型——M2.5 与 M2.5-Lightning——能力完全相同，速度有所差异。M2.5-Lightning 拥有每秒 100 个 token 的稳定吞吐，比其他前沿模型快两倍，价格为每百万输入 token 0.3 美元、每百万输出 token 2.4 美元。吞吐为每秒 50 个 token 的 M2.5，价格是其一半。两个版本均支持缓存。按输出价格计算，M2.5 的成本约为 Opus、Gemini 3 Pro 与 GPT-5 的十分之一到二十分之一。
  
以每秒 100 个输出 token 的速率连续运行一小时，M2.5 的成本为 1 美元。以每秒 50 个 token 的速率，价格降至 0.3 美元。直观地说：花 10,000 美元可以让四个 M2.5 实例连续运行一整年。我们相信，M2.5 为经济体中智能体的开发与运行提供了几乎无限的可能。对 M2 系列而言，唯一剩下的问题是如何持续推动模型能力的前沿。

### 改进速率

从 10 月下旬至今的三个半月中，我们相继发布了 M2、M2.1 与 M2.5，模型改进的节奏超出了我们最初的预期。例如，在广受关注的 SWE-Bench Verified 基准上，M2 系列的进步速度显著快于 Claude、GPT、Gemini 等同侪模型家族。

![](https://file.cdn.minimax.io/public/446f220e-cefd-459f-907d-ccbf535b7d15.png)

### 强化学习扩展（RL Scaling）

上述进展的关键驱动力之一是强化学习的扩展（scaling）。在我们训练模型的同时，我们也受益于模型的能力。我们公司的大部分任务与工作环境都已被改造成强化学习训练环境。迄今为止，这样的环境已有数十万个。与此同时，我们在智能体强化学习框架、算法、奖励信号与基础设施工程上做了大量工作，以支撑强化学习训练的持续扩展。

### Forge——智能体原生 RL 框架

我们自研了一个名为 Forge 的智能体原生强化学习框架，它引入了一个中间层，将底层训练-推理引擎与智能体完全解耦，支持接入任意智能体，使我们能够优化模型在智能体脚手架与工具上的泛化能力。为了提升系统吞吐，我们优化了异步调度策略，在系统吞吐与样本偏离度（off-policyness）之间取得平衡，并为训练样本设计了树状合并策略，实现了约 40 倍的训练加速。

![](https://file.cdn.minimax.io/public/d1bf56f3-3547-46d1-b901-785aab0b01b0.png)

### 智能体 RL 算法与奖励设计

在算法侧，我们继续使用去年年初提出的 CISPO 算法，以保证 MoE 模型在大规模训练中的稳定性。为了应对智能体 rollout 中长上下文带来的信用分配（credit assignment）难题，我们引入了过程奖励机制，对生成质量进行端到端监控。此外，为了与用户体验深度对齐，我们通过智能体轨迹评估任务完成时间，在模型智能与响应速度之间取得最优权衡。

![](https://file.cdn.minimax.io/public/ad0df79a-da5b-4432-b6d5-b5c53349a1e8.png)

我们很快会在一篇单独的技术博客中发布关于强化学习扩展更全面的介绍。

### MiniMax Agent：作为专业员工的 M2.5

M2.5 已全面部署到 MiniMax Agent，带来最佳的智能体体验。
  
我们将核心信息处理能力蒸馏为深度集成于 MiniMax Agent 的标准化 Office Skills（办公技能）。在 MAX 模式下，处理 Word 排版、PowerPoint 编辑、Excel 计算等任务时，MiniMax Agent 会根据文件类型自动加载相应的 Office Skills，提升任务产出的质量。
  
此外，用户可以将 Office Skills 与特定行业的领域专业知识结合，创建面向特定任务场景、可复用的 Experts（专家）。
  
以行业研究为例：将一套成熟的研究框架 SOP（标准作业程序）与 Word Skills 融合后，Agent 可以严格遵循既定框架自动抓取数据、梳理分析逻辑，并输出格式规范的研究报告——而不是仅仅生成一大段原始文字。在财务建模场景中，将机构自有的建模规范与 Excel Skills 结合，Agent 就能遵循特定的风控逻辑与计算标准，自动生成并校验复杂的财务模型，而不是简单地输出一个基础电子表格。
  
迄今为止，用户已在 MiniMax Agent 上构建了超过 10,000 个 Experts，且这一数字仍在快速增长。MiniMax 也围绕办公、金融、编程等高频场景，在 MiniMax Agent 上构建了多套深度优化的、开箱即用的 Expert 套件。
  
MiniMax 自身也率先受益于 M2.5 的能力。在公司日常运营中，30% 的整体任务由 M2.5 自主完成，横跨研发、产品、销售、HR、财务等职能——且渗透率仍在持续上升。编程场景中的表现尤为显著：M2.5 生成的代码占新提交代码的 80%。

### 附录

M2.5 的更多基准测试结果：

![](https://file.cdn.minimax.io/public/8c019213-b0d5-4ee8-9273-6d9b799abeae.png)

### 评测方法：

*- **SWE 基准：** SWE-bench Verified、SWE-bench Multilingual、SWE-bench-pro 与 Multi-SWE-bench 在内部基础设施上以 Claude Code 作为脚手架测试，覆盖默认系统提示词，结果为 4 次运行取平均。此外，SWE-bench Verified 也在 Droid 与 Opencode 脚手架上使用默认提示词进行了评测。
- **Terminal Bench 2：** 我们使用 Claude Code 2.0.64 作为评测脚手架测试了 Terminal Bench 2。我们修改了部分题目的 Dockerfile 以确保题目本身的正确性，将沙箱规格统一扩展为 8 核 CPU 与 16 GB 内存，超时时间统一设为 7,200 秒，并为每道题配备了基础工具集（ps、curl、git 等）。虽然不对超时进行重试，但我们增加了对脚手架空响应的检测机制，对最终响应为空的任务进行重试，以应对各种异常中断场景。最终结果为 4 次运行取平均。
- **VIBE-Pro：** 内部基准。使用 Claude Code 作为脚手架，自动验证程序的交互逻辑与视觉效果。所有得分均通过统一的流水线计算，包括需求集合、容器化部署与动态交互环境。最终结果为 3 次运行取平均。
- **BrowseComp：** 使用与 WebExplorer（Liu et al., 2025）相同的智能体框架。当 token 用量超过最大上下文的 30% 时，丢弃全部历史。
- **Wide Search：** 使用与 WebExplorer（Liu et al., 2025）相同的智能体框架。
- **RISE：** 内部基准。包含来自人类专家的真实问题，评估模型结合复杂网页交互的多步信息检索与推理能力。在 WebExplorer（Liu et al., 2025）智能体框架之上增加了基于 Playwright 的浏览器工具套件。
- **GDPval-MM：** 内部基准。基于开源 GDPval 测试集，使用定制的智能体评测框架，由 LLM-as-a-judge 对完整轨迹进行两两胜负/平局判定。每项任务的平均 token 成本基于各厂商官方 API 定价计算（不含缓存）。
- **MEWC：** 内部基准。基于 MEWC（Microsoft Excel World Championship，微软 Excel 世界锦标赛）构建，包含 2021–2026 年 Excel 电竞竞赛主赛区及其他地区赛区的 179 道题目。评估模型理解竞赛级 Excel 电子表格并使用 Excel 工具完成题目的能力。得分通过将输出与答案单元格逐一比对计算。
- **Finance Modeling：** 内部基准。主要包含由行业专家构建的财务建模题目，涉及通过 Excel 工具执行的端到端研究与分析任务。每道题使用专家设计的评分细则打分。最终结果为 3 次运行取平均。
- **AIME25 ~ AA-LCR：** 基于 Artificial Analysis Intelligence Index 榜单覆盖的公开评测集与评测方法，经内部测试获得。*
