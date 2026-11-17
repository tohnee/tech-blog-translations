---
title: "Claude Code 与 Slack"
title_en: "Claude Code and Slack"
date: 2025-12-08
source: https://claude.com/resources/articles/claude-code-and-slack
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude Code 与 Slack

> 原文：[Claude Code and Slack](https://claude.com/resources/articles/claude-code-and-slack) · Claude 博客

* 分类：[产品更新](/resources/product-updates)
* 产品：Claude Code
* 日期：2025 年 12 月 8 日
* 阅读时长：3 分钟

今天，我们推出直接从 Slack 向 Claude Code 委派任务的能力。该功能目前以研究预览（beta）形式提供，Claude 让把上下文从 Slack 对话转移到编码会话变得轻而易举。

## **从讨论到实现**

与工程工作相关的关键上下文常常存在于 Slack 中，包括 bug 报告、功能请求和工程讨论。当出现 bug 报告或队友需要修复代码时，你现在可以在 Slack 中 @Claude，让它利用周围的上下文自动启动一个 Claude Code 会话。它适用于：

* **Bug 调查与修复**：让 Claude 在 bug 被报告后立即调查并修复。
* **快速代码审查与修改**：让 Claude 根据团队反馈实现小型功能或重构代码。
* **协作调试**：当团队讨论提供了关键上下文——错误复现或用户报告——Claude 可以利用这些信息来指导其调试方式。

## **自动将任务路由到 Claude Code**

该功能建立在我们现有的 [Slack 版 Claude 应用](https://claude.com/resources/articles/claude-and-slack)之上，允许 Claude 把任务转交给 Claude Code on the web。当你在 Slack 中 @Claude 时，Claude 会检查你的消息，判断它是否属于编码任务。如果是，就会自动创建一个新的 Claude Code 会话。你也可以手动告诉 Claude 将请求作为编码任务处理。

Claude 会收集 Slack 中近期频道和线程消息的上下文，输入 Claude Code 会话。它会利用这些上下文，根据你已在 Claude Code on the web 中认证的仓库，自动选择在哪个仓库上运行任务。

随着 Claude Code 会话推进，Claude 会把状态更新发回你的 Slack 线程。完成后，你会看到完整会话的链接（可在此查看改动），以及一个直接打开拉取请求的链接。

## **开始使用**

要开始使用，请确保已通过 [Slack 应用市场](https://slack.com/marketplace/A08SF47R6P4)在你的 Slack 工作区中安装 Claude 应用。安装后，使用你的 Claude 账户完成认证，然后就可以 @Claude 处理编码任务。要让 Claude 路由编码任务，你需要拥有 [Claude Code on the web](https://claude.com/resources/articles/claude-code-on-the-web)的访问权限。

[查阅文档](https://code.claude.com/docs/en/slack)了解更多。

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
