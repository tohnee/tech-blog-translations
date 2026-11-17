---
title: "在 Foundation Models 框架中通过 Claude 为 Apple 平台构建智能应用"
title_en: "Building intelligent apps for Apple platforms with Claude in the Foundation Models framework"
date: 2026-06-08
source: https://claude.com/resources/articles/claude-for-foundation-models
crawled: 2026-11-17
translated: 2026-11-17
---

# 在 Foundation Models 框架中通过 Claude 为 Apple 平台构建智能应用

> 原文：[Building intelligent apps for Apple platforms with Claude in the Foundation Models framework](https://claude.com/resources/articles/claude-for-foundation-models) · Claude 博客

* 分类：[产品更新](/resources/product-updates)
* 产品：Claude Platform、Claude apps
* 日期：2026 年 6 月 8 日
* 阅读时长：3 分钟

今天我们通过一个新的 Swift 包发布对 Claude 的 Foundation Models 框架支持，让 Apple 开发者可以使用 Apple 的 Foundation Models 框架调用 Claude，以应对更复杂的工作流。

![](https://assets.claude.com/2c536ac9545ae24001d8f6d0ce604702e7f27eee.png)

Apple 的 Foundation Models 框架让开发者可以从 Swift 原生接入模型。它非常易用，只需三行代码，就能通过引导式生成（guided generation）返回类型化的 Swift 值。开发者可以用它接入 Apple 的设备端模型，处理摘要或抽取这类快速的本地任务。

现在，当请求需要多步推理、代码生成等能力时，开发者可以使用 Apple 的 Foundation Models 框架把任务移交给 Claude。Claude 还可以搜索网络获取最新信息，并执行代码进行数据分析。Claude 的响应会以流式方式回传到同一个视图。

由于 Apple 的框架会通过 @Generable 注解返回类型化的 Swift 值，开发者在发起 Claude API 调用时拿到的是干净的输入，而不是原始的用户文本。

## 这解锁了什么

Foundation Models 框架已经支撑了一系列智能设备端功能——呈现个性化提示的日记应用、总结合同的文档应用、按学生水平解释概念的学习应用。加入 Claude 可以延伸上述每一种模式。

![](https://assets.claude.com/1fe4afefb5a24989001f5b36f9a211f597442586.png)

日记应用可以在设备端生成每日提示，然后请 Claude 在数月的条目中找出线索。学习应用可以在设备端定义术语，当学生追问“这对我们已经学过的其他内容为什么重要？”时再移交给 Claude。

对用户来说，这是一个统一的体验，而每一步都由合适的模型支撑。

## 开始使用

对 Claude 的 Foundation Models 框架支持将于明天推出，可在 iOS 27、iPadOS 27、macOS 27、visionOS 27 和 watch OS 27 上通过 Apple 的 Foundation Models 框架使用。把它加入你的项目，使用 Anthropic API key 登录，再把 Apple 设备端处理产生的类型化输出传入 Claude 请求——这个包会负责流式传输、工具调用，以及把结构化响应返回给你的 SwiftUI 视图。

## 相关文章

探索更多产品动态，以及为使用 Claude 构建的团队准备的最佳实践。

*2026 年 11 月 12 日 · 文章*

### [在你的安全边界内运行 Claude Managed Agents](/resources/articles/self-hosted-claude-managed-agents)

推出自托管 Claude Managed Agents。现在，你可以在自己的环境中运行智能体，无论是自有云还是本地部署。智能体、凭证和会话历史都由你托管，并可自行选择向 Claude 发送请求的位置。

Claude Platform、Claude Managed Agents

*2026 年 11 月 12 日 · 文章*

### [推出 Claude for Manufacturing](/resources/articles/claude-for-manufacturing)

一个包含 17 项技能和四个连接器的新插件，帮助制造商基于现有系统起草报价、质量报告和供应商询价。

*2026 年 11 月 12 日 · 文章*

### [推出 Claude Meetings](/resources/articles/claude-meetings)

将 Claude 加入视频通话，一边交谈一边推进工作

*2026 年 11 月 10 日 · 文章*

### [你的应用现在可以在 Claude 中打开，Claude 也能在其中工作](/resources/articles/interactive-connectors-full-tool)

合作伙伴现在可以将应用直接嵌入 Claude，让你和 Claude 在同一工具、同一屏幕上协作，无需切换标签页。

Claude apps、MCP
