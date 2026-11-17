---
title: "管理 Claude Code 在 Google Cloud 上的成本并证明 ROI"
title_en: "Manage costs and demonstrate ROI for Claude Code on Google Cloud"
date: 2026-10-27
source: https://claude.com/resources/articles/how-to-manage-costs-and-demonstrate-roi-for-claude-code-on-google-cloud
crawled: 2026-11-17
translated: 2026-11-17
---

# 管理 Claude Code 在 Google Cloud 上的成本并证明 ROI

> 原文：[Manage costs and demonstrate ROI for Claude Code on Google Cloud](https://claude.com/resources/articles/how-to-manage-costs-and-demonstrate-roi-for-claude-code-on-google-cloud) · Claude 博客

*管理 Claude Code 在 Google Cloud 上的成本、衡量投资回报率的最佳实践。*

随着组织把越来越多的工作交给 Claude Code，支出也随之增长，平台团队需要一种既能控制成本、又能理解影响的办法。受近期与 Google Cloud 合办的一场[网络研讨会](https://www.anthropic.com/webinars/how-to-control-costs-and-show-roi-for-claude-code-on-google-cloud)的启发，我们在此分享使用 Claude Code 的组织如何在 Google Cloud 上更好地跟踪和优化这些考量，其中包括三个核心杠杆：控制（control）、跟踪（track）、证明（prove）。

## 管理 Claude Code 支出的控制手段

Google Cloud 上的 Claude 采用按用量计费（consumption-based pricing），因此你的账单就是一份读数，反映开发者在你的 Google Cloud 环境中使用了多少 Claude。采用率驱动用量；用量是你付费的东西，也是价值显现的地方。

你的 Claude Code 账单，取决于任务消耗多少 token 以及由哪些模型来处理。token 消耗随任务复杂度和对话长度增长。Chat 是一种问答式对话。像 Claude Code 这样的智能体工具，每个任务消耗的 token 比 Chat 更多，因为它在做多步骤工作：读取文件、运行工具、在整个任务范围内推理。与此同时，每个模型都有自己的每 token 价格，因此[让模型与任务匹配](https://claude.com/blog/claude-model-and-effort-level-in-claude-code)是另一项主要的成本控制手段。

通过 [Claude 应用网关](https://claude.com/blog/introducing-the-claude-apps-gateway)（Claude apps gateway）和 Google Cloud 服务，你可以看清每月有哪些 token 和模型选择在影响你组织的账单。你可以通过三个相互独立的杠杆来治理支出、管理成本：

* **控制（Control）**：设置防护栏，引导使用方式，而不是过度限制访问、无意中把人挡在外面。
* **跟踪（Track）**：在账单到来之前，细粒度地掌握支出发生在哪里、还将继续流向哪里。
* **证明（Prove）**：弄清组织花这些 token 获得了什么价值，并精确归因这份价值来自何处。

下面介绍如何把“控制 → 跟踪 → 证明”这一框架应用到你自己在 Google Cloud 上的 Claude Code 部署中。

![展示 control - track - prove 三个类别以及各自所用工具的示意图](https://assets.claude.com/50faca60a22f422f7c0f5e9d2f4177a1ea483448.png)

### **治理工具箱**

Google Cloud 上的 Claude 自带一系列工具和能力，用于控制、跟踪你的支出并证明其价值。

![展示 Google Cloud 原生能力以及 Claude Code + Claude 应用网关新增能力的示意图](https://assets.claude.com/b3266f5cebd6e2613593339d21200b3a7c034b9a.png)

Google Cloud 本身已经提供了许多原生能力，可用于跟踪和控制你的 Claude 支出：

* **按项目计费（Per-project billing）**。允许你为 Claude Code 托管一个专属项目，作为跟踪成本的干净方式。
* **账单预算与提醒**。允许你设置预算提醒，在实际支出越过你设定的阈值时收到通知。
* **支出上限（Spend caps，预览版）**。允许你在服务级别强制执行 Google Cloud 支出预算，并可手动解除上限。
* **BigQuery 导出**。让你可以把 Claude 支出与其他云成本放在一起分析。
* **配额**。Google Cloud 上的 Claude 模型，针对每个模型家族和端点位置，对请求数、输入 token 和输出 token 设有每分钟限额。
* **预配吞吐量**。为预留容量支付固定费用，而不是按量付费。

Claude Code 和 Claude 应用网关则增加了它们自己的跟踪与控制能力。网关是一个自托管服务，随开发者已经在用的同一个 `claude` 二进制文件一起发布，运行在你的 Google Cloud 项目中，位于 Claude Code 与 Google Cloud 上的 Claude 之间。开发者通过你的身份提供商（例如 Google Workspace）登录，因此每个请求都携带经过验证的身份。这让你可以按 IdP 组设置模型允许列表，并按用户、IdP 组或组织设置支出上限——可按天、按周或按月。

下面介绍如何选择和组合这些能力，来管理这三个杠杆——它们衡量的是你组织在 Google Cloud 上使用 Claude 的 AI 投入背后的成本与 ROI：

#### 杠杆一：控制

控制杠杆的核心在于提供防护栏，引导开发者使用 Claude Code，而不是用随意的上限去限制他们。

“引导而非限制”很重要，因为高成本会话并不一定是坏事——事实上它们往往价值很高，在 Claude Code 中尤其如此。这些会话通常来自你处于最前沿的重度用户：他们尝试新工作流，从 Claude 身上获得大量价值，也完成了大量工作。

浪费往往出现在支出大户的“长长的中间部分”。例如，他们每天用 Fable 跑一个 Sonnet 就能轻松处理的固定流程；又或者他们忘了某个自己已经不再关心的定时任务，但它仍然在自动运行。

以下四项功能为你提供防护栏，用来引导而不是限制你的用户：

* **[花费限额](https://code.claude.com/docs/en/claude-apps-gateway-spend-limits)**。Claude 应用网关允许你按用户、按 IdP 组或全组织设置支出上限，可按天、按周或按月。组和组织的上限是每位开发者各自继承的默认值，而不是共享池。
* **阈值提醒**。与 Claude 应用网关配合使用时，Google Cloud 上的 Claude Code 会在开发者接近上限时发出警告，先在超过 75% 时提醒一次，在超过 95% 时再提醒一次。这些是给开发者看的 CLI 内警告，而 Google Cloud 账单提醒是给管理员看的。达到上限时，网关会返回 429，直到周期重置或管理员提高上限；你可以通过网关的管理 API 用脚本提高上限。
* **模型默认值与允许列表**。通过 Claude 应用网关按 IdP 组指定哪些模型可用，网关会在服务端对每个请求强制执行允许列表。我们发现设置模型默认值效果非常好，因为大多数人会沿用模型默认值；如果他们想换模型，通常是有理由的。你可以把模型默认值与模型允许列表一起使用，也可以只使用其中之一。
* **网关管理 API**。网关提供用于[花费限额](https://code.claude.com/docs/en/claude-apps-gateway-spend-limits)的管理 API，因此你可以用程序化的方式设置和调整上限，例如通过工单工作流。

![展示支出上限生命周期各阶段的示意图](https://assets.claude.com/d1ded8cd5410c90e62905f650bf2a4e09df4cdce.png)

把这些能力组合起来控制你的总体账单，但要记住：控制只是第一个杠杆。每 token 价格并不能给出全貌。最重要的指标是每任务成本（cost per task），而这需要通过跟踪用量来监控和分析。

#### 杠杆二：跟踪

这个杠杆的核心是看清支出流向哪里、如何被使用。好消息是，你可以跨整个组织跟踪 Claude Code 的用量、成本和工具活动。主要的跟踪策略包括：

* **用量与成本可观测性**。[Claude Code 的 OpenTelemetry 指标与事件](https://code.claude.com/docs/en/monitoring-usage)会上报用量和估算成本，并按技能、插件、智能体和 MCP 服务器细分。通过 OpenTelemetry 收集器，或经 Claude 应用网关转发（用于集中式 OpenTelemetry 配置），用 OpenTelemetry Protocol（OTLP）把它们发送到你已经在用的工具，例如 Google Cloud Monitoring。
* **终端用户用量视图**。开发者可以直接在 Claude Code 中看到自己的支出，并在触及限额之前收到用量警告。
* **导出数据到你现有系统**。Google Cloud 账单导出到 BigQuery 后，你可以按模型和 token 类型筛选 Claude 的 SKU，把 Claude 支出与其他云和 AI 支出并列查看。OTel 数据流入你的可观测性（O11y）技术栈，网关管理 API 则可以把花费限额状态直接送进你的工单系统。

![展示 Google Cloud 上 Claude Code 遥测能力的示意图](https://assets.claude.com/f2ab59204d683994ef32ddc5b4e6f1167389a800.png)

无论 Claude Code 运行在开发者本机还是云工作站上，只要启用，它就能导出 OpenTelemetry 数据，包括会话、活跃时间、代码行数、提交、拉取请求、token 和成本，并按用户、团队和模型细分。最新版本的 Claude Code 还会按技能、插件、智能体和 MCP 服务器细分用量，因此你不仅能看到 Claude Code 的整体使用情况，还能看到组织内部哪些技能和插件被采用了。使用 Claude 应用网关后，你不需要逐台机器配置：在网关上设置一个遥测目标，它就会为已登录的开发者打开遥测。它还会给每次导出打上开发者在登录时经过验证的邮箱和 IdP 组，而不是客户端侧配置的值。

要把用量归因到你自己的成本中心和部门，请设置 `OTEL_RESOURCE_ATTRIBUTES` 环境变量（例如 `department=engineering,cost_center=eng-123`）。Claude Code 会把这些标签加到每个指标和事件上，因此你可以按它们筛选和聚合。指标会带着这些自定义属性落入 Google Cloud Monitoring（或 Grafana、Splunk 等其他监控方案）。

![某仪表盘的截图](https://assets.claude.com/201a89049ce753ac7e42f8518d1db7908b40a91a.png)

Cloud Monitoring 中的一个 Claude Code 用量仪表盘，基于 Claude Code 的 OpenTelemetry 指标构建。图中为使用示例数据做的示意性重建。

一个典型的采用情况视图会展示活跃开发者数、过去 24 小时的会话数，以及消耗的 token 总量。橙色框显示的是开发者触及网关强制支出上限时被拦截的请求。这个指标与现有的工单系统很搭，可以形成一条让开发者申请提高上限的工作流。

如果需要一个现成的 Cloud Monitoring 仪表盘，可以参考 [Claude Code Monitoring 模板](https://github.com/GoogleCloudPlatform/monitoring-dashboard-samples/tree/master/dashboards/claude-code)，它把 Claude Code 的 OpenTelemetry 指标整合成一个视图，涵盖采用情况、编码活动、token 用量与估算支出，这样你在 Google Cloud 上推广 Claude Code 的过程中就能按用户和模型跟踪用量与成本。你可以直接在 Cloud Monitoring 控制台内复制这个模板。

要在 Google Cloud 上搭建自定义的 Claude Code 遥测，可以从 [Claude Code OTel 快速入门](https://github.com/Google-Cloud-AI/partner-ai-anthropic/tree/main/01-quickstart/otlp-to-telemetry-api)开始。用它来配置 Claude Code，把 OpenTelemetry 直接导出到 Google Cloud Observability 套件，包括 Cloud Logging 和 Cloud Monitoring。这个快速入门还会把日志路由到分区化的 BigQuery 表，每种事件类型一张表（API 请求、工具决策、工具结果、助手响应、已完成的 hook 执行），并附带现成的 SQL 查询，用于分析每位开发者/每个模型的支出、工具成功率与延迟、hook 等待时间，以及按回合和按会话的分析。

#### 杠杆三：证明

控制杠杆治理并分配用量与成本；跟踪杠杆让你把支出可视化；证明杠杆则是把用量映射为 Google Cloud 上 Claude Code 的 ROI。

平台工程师在 Claude Code 中最关心的度量指标，可以归入三个维度：用量、开发者满意度和影响。

**采用与用量**指标衡量你组织中人们如何使用 Claude，包括已激活用户及其每周、每日用量。它们能揭示使用深度、用户随时间的留存情况，以及谁是你的 Claude Code 重度用户。这些指标全部来自 Claude Code 的 OTel 数据。

**满意度**指标监控你工程师的用户体验，包括他们对 Claude Code 的满意度、感知到的时间节省、对输出的信心，以及可能遇到的任何摩擦。满意度指标来自推广前后各做的一次简短问卷，之后是持续的用户回访。

**影响**指标评估 Claude 带来了多少可衡量的工程成果，把吞吐量、周期时间和评审速度与基线对比，另外还包括针对具体工作内容的定性度量。

### **一组起步用的影响指标**

下面是一组起步用的影响指标，分为三个领域：时间、投入和产出量。

**时间**衡量工作交付有多快：从开启到合并的 PR 周期时间，以及代码评审的周转时间。

**投入**衡量每个改动需要多少工作：每个 PR 的评审轮次、每个 PR 的评审意见数与返工量。

**产出量**衡量释放出来的产能交付了什么：每位工程师的 PR 数、部署频率，以及有名有姓的工作内容——你的团队用释放出的产能交付了哪些具体的待办事项。这些为数字之外补充了定性的视角。

这些是指引性的参考点，不是硬性规则，但是衡量 Claude Code 在你组织中影响的一个不错的起点。你需要的基线已经存在：版本控制和工单系统里的交付历史。

### **定义你的工作单元**

这些指标大多在数 PR，但修一个拼写错误和发布一个功能都算一个 PR。因此，应改为统计某一确定类别中已合并的 PR：Claude 开启 PR，由人决定是否交付。像 hotfix 或 feature release 这样的标签、工单 ID，以及 Claude 是否参与，都能让你在现有系统中轻松找到这些 PR。并非每个工作单元都是 PR；服务切换、或某个事故被根治后关闭，都是例子。同一条规则同样适用：数一件完成的事，就在它落地的地方数。

## Claude Code 原生遥测

在把成本治理和用量跟踪落实到位之后，下一步是把它们映射到 ROI。Claude Code 的原生遥测帮助你捕获贡献度和生产力指标，用来记录你的组织正在获得的价值。

![展示 Claude Code 原生遥测的示意图，分三列：Usage、Cost、Contribution / Productivity。](https://assets.claude.com/5d1a4e740237e04f4524c9ff169e0f70def7c5ab.png)

Claude Code 的 OTel 指标让你可以跟踪或推导出：代码建议采纳率、修改的代码行数、创建的提交数、创建的 PR 数、每单位产出的成本，以及每位用户的 PR 数。

这些原生指标都提供了有用且可据此行动的信息。当它们与记录下来的事件——例如用户提示和工具决策——结合时，这些信息会更有价值，而这些事件可通过 Google Cloud 上的 Claude Code 遥测捕获。例如，记录用户提示是了解你的用户群体想要构建什么的好办法，因为并非每个工作单元都一定是 PR。请注意，由于内容可能敏感，用户提示不会被自动记录；你必须明确选择启用。

举例来说：如果你是一名 SRE，用 Claude Code 排查事故；或者你是一名售前工程师，用它生成实时演示的样本数据。这些会话不会产出 PR，但它们确实加速了那些团队的工作流。请记住，Claude Code 的 PR 指标统计的是 Claude Code *创建*的 PR，而不是最终合并的 PR。版本控制和工单系统仍然是“交付了什么”的权威记录，所以要把 Claude Code 遥测与 GitHub 或 GitLab 以及你的工单跟踪器关联起来，才能看到全貌。

以下是一些使用 Google Cloud 上 Claude 的客户借助 Claude Code 所取得的可衡量影响。

* [Delivery Hero](https://claude.com/customers/delivery-hero) 有一个团队重构了覆盖 100 个 UI 组件的一套设计系统。Claude Code 在几分钟内完成了通常要花一名工程师一周时间的工作。
* [Shopify](https://claude.com/customers/shopify) 的工程师用 Claude Code 更快地构建，但非工程师也在用几分钟而不是几天来构建内部工具。Claude Code 在 Shopify 扩大的是“谁能构建”，而不只是让已经在构建的人更快。
* [Fifth Dimension](https://cloud.google.com/customers/fifth-dimension-anthropic) 的工程师普遍在 Google Cloud 上使用 Claude Code。他们合计每月编写超过 30 万行代码，采纳率达到 98%。

## 开始上手

本文的目标，是让你对现有的工具和能力感到心里有底——它们能帮你管理 Claude Code 在 Google Cloud 上的成本并证明 ROI。作为平台工程师，这套体系不仅用于发现和观察用户群体的行为，它还为你提供必要的知识，以便动态调整治理策略和设置。

这是一个持续循环：先设定合理的默认值，例如全组织的支出上限、一个默认模型和一个模型允许列表，然后随着用量数据的积累，按角色和团队细化。通过跟踪实际使用并把指标与你从 Claude Code 获得的价值关联起来，你就可以把这些交给需要分析 Claude Code 的 ROI 与业务影响的相关方。

![展示 Control - Track - Prove 框架持续循环的示意图](https://assets.claude.com/9a83ef407d2df018b107f8108d1955ad70702d7f.png)

随着我们交给 Claude 的工作在数量和类型上不断加深、日益多样，组织在 Google Cloud 上使用 Claude Code 的方式、以及由此获得的价值，都会持续演化。这里概述的**控制 → 跟踪 → 证明**框架，是衡量你 Claude Code 部署各方面与各项成果的一个稳定起点。

以下资源可供你上手：

* [高效管理成本](https://code.claude.com/docs/en/costs)
* [监控用量与成本](https://code.claude.com/docs/en/monitoring-usage)
* [Claude 应用网关花费限额](https://code.claude.com/docs/en/claude-apps-gateway-spend-limits)
* [在 Google Cloud 上部署 Claude 应用网关](https://code.claude.com/docs/en/claude-apps-gateway-on-gcp)
* [创建、编辑或删除预算与预算提醒](https://code.claude.com/docs/en/claude-apps-gateway-on-gcp)
* [管理支出上限预算 | Cloud Billing](https://docs.cloud.google.com/billing/docs/how-to/budgets-spend-caps)
