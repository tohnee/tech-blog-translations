---
title: "Claude 现在可以连接你的世界了"
title_en: "Claude can now connect to your world"
date: 2025-05-01
source: https://claude.com/resources/articles/integrations
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude 现在可以连接你的世界了

> 原文：[Claude can now connect to your world](https://claude.com/resources/articles/integrations) · Claude 博客

Claude 现在可以通过 Integrations 连接你的应用和工具；同时，高级版 Research 会检索网络、Google Workspace 以及已连接的服务，快速交付全面的报告。

今天我们宣布推出 Integrations——一种将你的应用和工具连接到 Claude 的新方式。我们同时扩展了 Claude 的 [Research](https://www.anthropic.com/news/research) 能力，新增一个高级模式，可检索网络、你的 Google Workspace，现在还加上你的 Integrations。Claude 可以研究长达 45 分钟，然后交付一份带引用的全面报告。除了这些更新，我们还向所有付费套餐的 Claude 用户全球开放网络搜索。

### Integrations

去年 11 月，我们发布了[模型上下文协议](https://www.anthropic.com/news/model-context-protocol)（Model Context Protocol，MCP）——一个将 AI 应用连接到工具与数据的开放标准。在此之前，对 MCP 的支持仅限于 Claude Desktop，且通过本地服务器实现。今天，我们推出 Integrations，让 Claude 可以在网页版和桌面应用中与远程 MCP 服务器无缝协作。开发者可以构建并托管增强 Claude 能力的服务器，用户可以发现有这些服务器并把任意多个连接到 Claude。

当你把工具连接到 Claude，它就能深入理解你的工作上下文——包括项目历史、任务状态和组织知识——并能在各个界面上采取行动。Claude 成为更了解情况的协作者，帮助你在一个地方执行复杂项目，每一步都有专家级协助。

一开始，你可以从 10 个热门服务的 Integrations 中选择，包括 [Atlassian 的 Jira 和 Confluence](https://www.atlassian.com/platform/remote-mcp-server)、[Zapier](https://zapier.com/mcp)、[Cloudflare](https://github.com/cloudflare/mcp-server-cloudflare/tree/main)、[Intercom](https://www.intercom.com/blog/introducing-model-context-protocol-fin)、[Asana](https://developers.asana.com/docs/using-asanas-model-control-protocol-mcp-server)、[Square](https://developer.squareup.com/docs/mcp)、[Sentry](https://docs.sentry.io/product/sentry-mcp/)、[PayPal](https://www.paypal.ai/)、[Linear](https://linear.app/changelog/2025-05-01-mcp) 和 [Plaid](https://api.dashboard.plaid.com/mcp/sse)——Stripe、GitLab 和 Box 等公司还会陆续带来更多。开发者也可以依照我们的文档，或借助 [Cloudflare](https://blog.cloudflare.com/remote-model-context-protocol-servers-mcp/) 等提供内置 OAuth 认证、传输处理和集成部署的解决方案，在短短 30 分钟内创建自己的 Integrations。

每一个集成都能大幅扩展 Claude 能做的事。例如，Zapier 通过预构建的工作流连接数千个应用，自动化你整个软件栈中的流程。借助 [Zapier Integration](https://zapier.com/mcp)，Claude 可以通过对话访问这些应用和你的自定义工作流——甚至自动从 [HubSpot](https://developers.hubspot.com/mcp) 拉取销售数据，并根据你的日历准备会议简报。

借助对 Atlassian Jira 和 Confluence 的访问，Claude 可以与你一起构建新产品、更有效地管理任务，并通过一次性总结和创建多个 Confluence 页面与 Jira 工作项来扩展你的工作。

连接 Intercom 可以更快回应用户反馈。Intercom 的 AI 智能体 Fin 现在是 MCP 客户端，可以在用户报告问题时采取行动，比如在 Linear 中提交 bug。与 Claude 对话，利用 Intercom 的对话历史和用户属性识别模式并进行调试——在一段对话中管理从用户反馈到 bug 解决的整个工作流。

### 高级版 Research

我们在近期发布的 [Research](https://www.anthropic.com/news/research) 能力基础上推出若干新更新。Claude 现在可以在数百个内部和外部来源中开展更深入的调查，在 5 到 45 分钟内交付更全面的报告。

开启 Research 按钮后即可使用更复杂的研究能力：Claude 会把你的请求拆解成更小的部分，逐一深入调查，然后汇编成一份全面报告。大多数报告在 5 到 15 分钟内完成，对于更复杂的调查，Claude 最多可能花 45 分钟——这类工作通常需要人工研究数小时。

我们还扩展了 Claude 的数据访问范围。发布 Research 时它支持网络搜索和 Google Workspace，而现在有了 Integrations，Claude 还能检索你连接的任何应用。

当 Claude 采用来自来源的信息时，它会提供清晰的引用，直接链接到原始材料。这种透明度确保你可以放心使用 Claude 的研究结果，确切知道每条洞见来自何处。

### 开始使用

Integrations 和高级版 Research 现已在 Max、Team 和 Enterprise 套餐中以 beta 版提供，并将很快在 Pro 套餐中提供。网络搜索现已向所有 [Claude.ai](http://claude.ai) 付费套餐全球开放。有关 Integrations、MCP 服务器入门，以及将数据源连接到 Claude 时的安全与隐私实践的更多信息，请访问我们的[帮助中心](https://support.anthropic.com/en/articles/11175166-about-integrations-using-remote-mcp)。***‍***

***更新：**扩大了可用范围。（2025 年 6 月 3 日）*

Integrations 和 Research 现已在 Pro、Max、Ultra、Team 和 Enterprise 套餐中提供。网络搜索已在所有 Claude 套餐中全球可用。
