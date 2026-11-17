---
title: "Claude Platform 上的智能体可观测性"
title_en: "Agent observability on the Claude Platform"
date: 2026-10-14
source: https://claude.com/resources/articles/agent-observability-on-the-claude-platform
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude Platform 上的智能体可观测性

> 原文：[Agent observability on the Claude Platform](https://claude.com/resources/articles/agent-observability-on-the-claude-platform) · Claude 博客

*宣布 Claude Platform 上的 Claude Managed Agents、Messages API 和 Anthropic SDK 支持 OpenTelemetry 追踪。*

你现在可以将来自 Claude Managed Agents、Messages API 和 Anthropic SDK 的 OpenTelemetry（OTel）追踪（trace）发送到任意 OTel 工具，并跟踪智能体执行的每一步。如果你已经在把 Claude Code 或 Cowork 的追踪发送到自己的可观测性工具，那么你在 Claude Platform 上构建的智能体也可以出现在同一个地方。

## 用 OpenTelemetry 追踪智能体

要给智能体更多访问权限，第一步就是追踪它的模型调用、工具使用和 MCP 服务器调用。查看它的追踪记录，随着它被证明可靠，再逐步扩大它的权限。

在 Claude Console 中添加一个目的地（destination），智能体的每一轮交互、每次模型调用和每次工具使用都会以标准 OpenTelemetry 追踪的形式到达你的可观测性工具，并带有延迟、token 和 ID 信息。

![OpenTelemetry 追踪的工作方式](https://assets.claude.com/28fe34519808d40faa51162351234a3790230860.png)

## 与你现有的可观测性工具配合

Claude 的追踪遵循 [OpenTelemetry GenAI 语义约定](https://github.com/open-telemetry/semantic-conventions-genai/)，因此来自 Claude 和其他提供商的数据可以在同一批工具和仪表盘中一起使用。

* **在你的其余技术栈旁边调试智能体。** 在 [Grafana Cloud](https://grafana.com/docs/grafana-cloud/observe-and-act/agent-observability/guides/send-claude-platform-traces/)、[Honeycomb](https://docs.honeycomb.io/send-data/use-cases/claude-platform)、[Sentry](https://sentry.io/cookbook/trace-claude-platform-with-opentelemetry/) 和 [Splunk](https://agent-observability-docs.splunk.com/sdk-api/third-party-integrations/claude) 中，智能体追踪与你的日志和指标放在一起，因此你能看出某个缓慢或失败的步骤来自哪个服务。
* **用生产数据改进智能体。** 借助 [Arize AI](https://arize.com/docs/ax/integrations/platforms/claude-managed-agents/claude-managed-agents-tracing)、[Braintrust](https://www.braintrust.dev/docs/integrations/ai-providers/anthropic#export-opentelemetry-traces-from-the-claude-api)、[Datadog](https://docs.datadoghq.com/llm_observability/instrument/otel_instrumentation/?tab=python#using-claude-managed-agents)、[Langfuse](https://langfuse.com/integrations/model-providers/claude-platform)、[LangChain 的 LangSmith](https://docs.langchain.com/langsmith/trace-anthropic)、[New Relic](https://newrelic.com/blog/news/anthropic-otel-ai-observability) 和 [PostHog](https://posthog.com/docs/ai-observability/installation/anthropic?tab=Claude+Platform&utm_source=anthropic&utm_campaign=anthropic-otel)，你可以把真实追踪转化为评估（evals）、发现质量问题，并衡量某项改动是否真的带来了改善。
* **跟踪整个组织的用量。** 将追踪发送到 [Databricks Unity Gateway](https://docs.databricks.com/aws/en/ai-gateway/unified-trace-table)，让平台团队和安全团队可以按团队查看 token 用量，并标记异常活动。

Claude 的追踪也适用于任何接受标准 OTLP 端点的其他 OpenTelemetry 工具。

## 开始使用

Claude Platform 上的 OpenTelemetry 追踪目前处于公开测试（public beta）阶段。Managed Agents 和 Messages API 需要在 Claude Console 中配置目的地，而 Anthropic SDK 会自动导出追踪。

参见[文档](https://platform.claude.com/docs/en/manage-claude/opentelemetry)开始使用。

![Foxglove](https://assets.claude.com/59150536fe838e40bd470d19ad4ab74ec3fa2d61.svg)

> "在 Foxglove，我们正在构建帮助机器人团队调试机器人的智能体。Claude Platform 原生的 OpenTelemetry 导出让我们可以在 PostHog 中把智能体交互与产品用量数据放在一起分析。这有助于我们评估智能体在实践中的表现，找出它们的短板，并为机器人团队的改进排定优先级。"

Roman Shtylman，联合创始人兼首席技术官

![Ramp](https://assets.claude.com/6db782273272dd89f11df7b54089328994fe718e.svg)

> "Claude 驱动着 Ramp 一些能力最强的内部智能体和面向客户的智能体。我们构建了 Reflect——一个智能体式系统，它给这些智能体的 Langfuse 追踪打分、找出反复出现的故障并提出修复方案。在某些智能体上，我们已把 token 用量降低了 10–20%，并让会话速度提升了 30%。但 Reflect 只能改进它观察到的东西。Claude API 原生的 OpenTelemetry 导出可以把高保真的埋点直接送入这个改进回路，无需额外步骤。"

David Traina，高级软件工程师

![Sterling Labs](https://assets.claude.com/0e7434aa92b7dbc6ea6bd4109a0b3602bcb2a22c.svg)

> "在 Sterling Labs，我们调校系统就像赛车队调校引擎。对于 7×24 小时分析实时市场的智能体来说，Langfuse 就是我们的维修区指挥台（pit wall）。Claude Platform 原生的 OpenTelemetry 导出让每条追踪都直接流入，无需编写自定义埋点，因此我的团队可以专注于竞争优势，而不是管道接线。"

Hyon Lee，首席技术官

![FloQast](https://assets.claude.com/37eab59899ee1b3f95d9bd8106e2708f2db42680.svg)

> "接触公司账簿的智能体必须像会计一样展示自己的工作过程。我们的智能体运行在 Claude Platform 上，遥测数据存放在 Grafana Cloud 中，而 Claude 原生的 OpenTelemetry 导出把每次模型调用放进了它所处的对账或日记账分录工作流的同一条追踪里。我们可以在其余技术栈之外，同时看到提示词版本、工具调用、延迟和 token 开销，因此当审计师问某个智能体做了什么、为什么这么做时，我们可以从同一条时间线上给出答案。"

Ankush Sharma，基础设施负责人
