---
title: "从提示到产品：Responses 的一周年"
title_en: "From prompts to products: One year of Responses"
source: https://developers.openai.com/blog/one-year-of-responses/
crawled: 2026-09-14
translated: 2026-09-14
---

# 从提示到产品：Responses 的一周年

> 原文：[From prompts to products: One year of Responses](https://developers.openai.com/blog/one-year-of-responses/) · OpenAI 开发者博客

一年前，我们推出了 [Responses API](https://developers.openai.com/api/reference/responses/overview)——它是开发者与企业构建实用且可靠的智能体的基石。为模型配备一组托管工具，让 AI 从聊天助手进化为能够代表你采取行动的系统。如今，Responses API 支持一系列驱动智能体工作流的工具，以及一套专为配合更强大模型构建而设计的新特性与基础原语（primitive）。

如今，成千上万的开发者正使用 Responses API 进行构建，在[客户支持](https://openai.com/index/klarna/)、[法律](https://openai.com/index/hebbia/)、[生命科学](https://openai.com/index/gpt-5-amgen/)、[旅游](https://openai.com/index/booking-com/)等行业提升生产力。在分享了众多来自这些行业的成功案例之后，今天我们要庆祝五个鲜有人讲述的故事，聚焦过去一年里基于 Responses API 开展构建的开发者们。

## 检测并修复 AI 智能体的故障

*作者：来自 [Raindrop AI](https://www.raindrop.ai) 的 Alexis Gauba 与 Ben Hylak*

**工具：** 自定义构建的工具

**模型：** GPT-5.2（正在测试 GPT-5.4）

Raindrop 是全球最具雄心的 AI 公司背后的监控平台，用于捕捉它们的智能体在生产环境中偏离轨道的时刻。随着智能体日益复杂，这些故障也变得愈发关键。

> 如果没有 Responses API，构建这样的监控系统会难得多，可靠性也会大打折扣。

该系统使用 Responses API（通过 Vercel AI SDK）运行后台分析，从而在不同模型提供商之间共享工具，并让系统在各环境中保持可移植。这些工作流能够发现异常行为。当出现问题时，系统会向开发者发出警报，并协助诊断底层问题。

该平台聚焦于三大核心系统：

1. 智能体行为监控
2. 故障检测与告警
3. 开发者排查与调试工具

这些系统协同工作，让团队能够在问题影响生产系统之前，发现、跟踪并修复 AI 智能体中的故障。

### 监控架构

这一架构让团队能够持续监控智能体行为，并在问题发生时快速响应。

### 1. 智能体行为监控

系统会持续评估智能体行为，以判断其是否按预期运行。

开发者可以针对不良结果设置条件，当这些条件被满足时，平台便会发出警报。

### 2. 故障检测与告警

一旦检测到异常，Raindrop 就会通知开发者，并呈现排查问题所需的相关上下文。

该平台提供以下工具：

- 跟踪不同智能体版本之间的行为变化
- 识别是哪些提示词或系统变更触发了故障
- 查看推理轨迹与工具调用

这让开发者能够快速定位故障的根本原因并部署修复。

### 3. 排查与调试工具

Raindrop 还提供帮助开发者诊断智能体工作流问题的工具。这些能力让团队能够将故障检测与系统改进联系起来。

Raindrop AI 使用 Responses API 驱动所有长时间运行的后台分析工作流。如果没有它，实现这些监控系统将困难得多。

## 面向复杂数据的深度推理工作流

*作者：来自 [Repo Prompt](https://repoprompt.com) 的 Eric Provencher*

**所用工具：** Codex（App Server + MCP）、网页搜索

**所用模型：** GPT-5.3-Codex

> 我们不让推理模型在规划或审查期间浪费上下文窗口去摸索上下文，而是利用一个单独的智能体提前整理上下文，让推理模型把尽可能多的推理能力投入到解决我们的任务上。

Eric Provencher 构建了一套系统，帮助开发者和研究者对大规模的文档、代码库与数据集集合进行深度分析。

[Repo Prompt](https://repoprompt.com) 专注于上下文工程（context engineering）——自动收集、组织和结构化相关信息，让推理模型能够有效地对其进行分析。

许多智能体系统专注于收集数据，而 Eric 的架构将上下文收集与深度推理分离开来。系统使用智能体工作流来汇集相关上下文，然后把整理好的信息交给一个专注于分析的推理模型。

该平台使用 OpenAI Responses API 来编排长时间运行的智能体工作流与推理任务，涵盖：

- 大型代码库分析与架构规划
- 深度代码审查工作流
- 针对大规模文档集合的研究分析
- 医学与科学文献分析

系统围绕三个核心组件构建：上下文构建智能体工作流、深度推理模型（"Oracle" 工作流），以及迭代式研究与分析循环。

### 1. 上下文构建智能体工作流

系统的第一阶段是上下文构建智能体。该工作流分析大型数据仓库，确定哪些信息与给定查询相关。

借助 Responses API 的工具与模型推理，智能体识别出相关文件、文档之间的关系以及关键信息段落。

这一阶段的输出是一个结构化的上下文包，作为推理阶段的输入。

### 2. “*Oracle*” 深度推理工作流

与上下文构建智能体不同，"Oracle" 模型（深度推理模型）不执行工具调用或额外的信息检索，而是完全专注于分析提供给它的整理后的上下文。

通过将研究与推理分离，模型可以把全部推理能力用于理解问题。在许多工作流中，推理阶段可以长时间运行，分析所提供上下文中的复杂关系。

### 3. 迭代式研究与分析循环

系统还支持迭代式推理循环。推理模型产出结果后，另一个智能体可以审查这些结果，判断是否需要进一步的调查。

如有需要，系统会启动新一轮的上下文收集与推理循环。这一循环支持长时间运行的调查，让系统逐步完善其分析。

#### 迭代工作流

系统依赖 Responses API 的多项能力：

- 后台任务（Background Jobs）：运行可持续数分钟或数小时的长时间推理任务
- 智能体编排（Agent Orchestration）：协调用于上下文收集、推理与验证的智能体循环
- 可观测性（Observability）：在长时间运行的推理工作流执行过程中对其进行监控与管理

该平台使用 Codex 模型收集并结构化相关上下文，然后将整理好的上下文交给能力更强的推理模型进行更深入的分析。这些能力支撑了该平台将智能体工作流与深度推理模型相结合的混合架构。

## 面向黑胶唱片收藏者的对话式界面

*作者：来自 [Collxn](https://www.collxn.com) 的 Ash Ryan Arnwine*

**工具：** 网页搜索与 16 个自定义工具

**模型：** GPT-5.4、GPT-5 nano

> 与构建完整的检索增强生成系统等替代方案相比，Responses API 感觉像是替我分担了工作。

Ash Ryan Arnwine 构建了 ["Collxn"](https://www.collxn.com)（取 collection 之意），这是一个使命重大的小服务：帮助黑胶收藏者重新发现架子上已有的唱片，并与自己的收藏互动。

收藏者通常在 Discogs 上管理庞大的收藏库，有时多达数千张唱片。Collxn 接入这份收藏，每天发送一封名为 "Daily Drop" 的邮件，聚焦一张不同的唱片并附上艺术家详情，帮助收藏者重温自己已拥有的音乐。

而且，既然能提问会让翻阅唱片更有乐趣，Collxn 便使用 OpenAI Responses API 驱动一个聊天界面，让用户真正可以与自己的唱片"对话"。

### 带工具调用的对话式界面

该应用使用 Responses API 提供一个名为 "Ask This Drop" 的聊天界面，用户可以就 Daily Drop 中的唱片提问。

模型被配置为可以访问 Discogs API 工具，在回答问题时直接从 Discogs 检索信息。

例如，用户可以提出这样的问题：

- 这张唱片目前的市场价是多少？
- 这位艺术家还发行过哪些专辑？
- 这个压盘版本有多稀有？

*Ask This Drop 为 Collxn 用户提供与黑胶唱片对话的聊天界面。*

收藏者只需提问，就能获得由实时 Discogs 数据与自己收藏背景相结合而生成的答案。

这种方式把静态的唱片收藏转变为与更广阔的音乐生态相连的对话式体验。

### Daily Drop 与艺术家新闻

Collxn 还使用 OpenAI Agents SDK 为 Daily Drop 邮件中推荐的艺术家生成"近期新闻"板块。

*Collxn Daily Drop 的艺术家新闻板块由 OpenAI Agents SDK 驱动。*

该功能部署一个由网页搜索驱动的智能体，查找有关该艺术家的近期文章或动态，并将这些内容加入每日邮件。在 beta 用户中，新闻功能迅速成为产品最受欢迎的部分之一，因为它以一种动态的方式把唱片收藏体验与外部世界连接起来。

最终，Ash 将 Collxn 迁移到 Responses API，推出了 "Ask This Drop"。这样一来，应用便能在对话式工作流中支持多步推理，以及内置与自定义工具调用。Collxn 的 Responses API 实现使用了内置网页搜索工具在聊天中搜索艺术家新闻，此外还有 16 个自定义工具，用于对接 Discogs API、查询用户的 Collxn 账户等。

*Collxn "Ask This Drop" 中的实时艺术家新闻查询由 Responses API 网页搜索工具驱动。*

Responses API 的有状态对话也让多轮聊天交互的处理变得更简单、更快捷。总体而言，Ash 指出，使用 Responses API 相比构建完整的检索增强生成（RAG）系统简化了架构。

## 把屏幕录制变成交互式产品演示

*作者：来自 [Arcade](https://www.arcade.software) 团队的 Nick Sorrentino 与 Pawel Wszola*

**工具：** 计算机操作（computer use）

**模型：** GPT-5.2、computer-use-preview

> 接入 API 驱动的内容生成后，发布一个演示所需的步骤数减少了 50%，显著提升了发布率与采用率。

Arcade 把大多数团队本来就在做的事情——录屏——变成精美、可交互的产品演示。团队无需再现场演示产品或撰写逐步说明文档，只需录制一次工作流，其余交给 Arcade 处理。

在底层，该平台分析录制内容，自动生成逐步引导式演示（guided walkthrough），解释每一步发生了什么。

### 演示生成工作流

在录制会话期间：

1. 用户在执行某个工作流的同时录制自己的屏幕。
2. 在桌面端或浏览器中，Arcade 直接捕获点击、输入、滚动等结构化交互。
3. 在移动端，由于 iOS 沙箱机制阻止应用捕获系统级交互，用户改为录制应用的普通屏幕视频。
4. 录制内容连同 computer-use 工具一起发送到 OpenAI Responses API，由其分析视觉帧并推断发生的交互。
5. 系统将这些推断出的操作转换为结构化步骤。
6. Arcade 生成引导观众浏览演示的叙述文字与交互热点。

这些步骤会自动成为用户看到的交互式引导演示。

随后，结构化的操作被传递给 Chat Completions API，由它生成贯穿整个演示的标题与热点描述。用户可以使用内置的 AI 编辑工具调整生成的文案，例如缩短或改写文本。

### 将演示创建工作量减半

演示叙述的自动化大幅减少了发布产品引导演示所需的工作量。

接入 API 驱动的工作流之后：

- 发布前所需操作数的中位数下降了 50%
- P80 操作数从约 230 降至约 120
- 发布率与产品采用率上升

通过消除演示创建流程中的摩擦，Arcade 让团队能够更快地把原始录制内容变成精美的交互式演示。

## 度量并提升品牌在 AI 输出中的可见度

*作者：来自 [Hexagon](https://joinhexagon.com) 的 Tunde Adeyinka 与 Ramon Silva*

**所用工具：** 网页搜索

**所用模型：** GPT-5.2 Chat

Tunde Adeyinka 与 Ramon Silva 创立 Hexagon，是为了回答一个面向零售商的新问题：*AI 助手会怎么谈论你的产品？*

随着 AI 助手日益影响产品发现的方式，Hexagon 帮助企业监控自己的品牌在 AI 生成答案中的呈现情况，并随时间不断改善这些结果。

该平台使用 OpenAI Responses API 驱动三大核心系统：

### 1. 回答模拟架构

Hexagon 每天运行一条模拟流水线，衡量 AI 助手如何回答与产品相关的问题。系统每天生成数千条真实的消费者提示、产品推荐提示与购物查询，然后通过 Responses API 发送。系统会分析返回的输出，跟踪品牌在 AI 生成答案中的可见度。

零售客户由此可以看到自家产品出现的频率，以及这些答案如何随时间变化。

### 2. 多智能体内容生成流水线

除了分析之外，Hexagon 还使用 Responses API 生成经过优化的内容，以提升品牌在 AI 答案中的可见度。

系统采用四智能体架构，每个智能体在流水线中执行一个专门的步骤，并将输出传递给下一阶段，直到最终内容生成并发布。各智能体通过非确定性循环进行沟通，在发布前反复迭代优化。

### 3. 仪表盘与客户工具

平台还包含 "Hexi"——一个通过 Responses API 的函数调用构建的聊天机器人。借助 Hexi，客户可以以对话方式探索分析数据，并以自助方式生成其 AI 可见度数据的摘要。Hexagon 通过一个零售商仪表盘呈现其分析，跟踪产品在 AI 生成答案中的出现方式。

Hexagon 依赖 Responses API 的几项关键能力，使其模拟在整个产品中既真实又有用：

- 网页搜索（Web search）：复现类似 ChatGPT 的开启浏览功能的回答。
- 用户位置参数（User Location Parameter）：模拟来自不同地区的查询，以测试地理差异。
- 推理力度（Reasoning Effort）：控制回答的深度与复杂度。
- 最大输出 Token 数（Max Output Tokens）：限制长篇输出的回答长度。
- 上下文持久化（Context Persistence）：在多次调用间保持上下文，支撑多智能体工作流。

> Responses API 提供了更好的回答质量以及跨多次调用的更强上下文持久化，这对驱动 Hexagon 平台的多步骤流水线至关重要。

## 结语

一年过去，[Responses API](https://developers.openai.com/api/reference/responses/overview) 已成为开发者构建智能体软件的核心基石。

这五个开发者故事展示了它在实践中的样貌：协调工具的多智能体系统、检测 bug、运行工作流，以及交付由 AI 驱动的产品。

平台本身也在快速演进——更好的编排和更丰富的[工具生态](https://developers.openai.com/api/docs/guides/tools)，新增了支持联网的 OpenAI 托管容器与 [shell 工具](https://developers.openai.com/api/docs/guides/tools-shell)。

更多工具。

更多能力。

更多开发者正在构建我们其他人还没想到的东西。

让我们期待开发者在第二年构建出什么。
