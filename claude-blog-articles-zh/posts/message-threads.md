---
title: "用 message threads 让长时间运行的智能体更快"
title_en: "Make long-running agents faster with message threads"
date: 2026-11-02
source: https://claude.com/resources/articles/message-threads
crawled: 2026-11-17
translated: 2026-11-17
---

# 用 message threads 让长时间运行的智能体更快

> 原文：[Make long-running agents faster with message threads](https://claude.com/resources/articles/message-threads) · Claude 博客

Messages API 的新功能：只需发送一次对话，此后 API 每一轮只接收新增内容。

* 分类：[产品更新](/resources/product-updates)
* 产品：Claude Platform
* 日期：2026 年 11 月 2 日
* 阅读时长：3 分钟

Message threads（消息线程）现已在 Claude Platform 上公测。借助 message threads，智能体不再需要在每一轮重新发送完整对话历史，从而降低长时间运行会话的延迟。

### message threads 如何工作

一个编程智能体在一次会话中可能发出数百个请求，而每个请求都会重新发送此前所有的消息和工具结果。一旦对话达到数十万 token，重发全部内容就会增加 Claude 开始响应前的等待时间。使用 message threads，智能体只需发送自上一轮以来的新增内容，从而降低首 token 时间（TTFT）。

对大多数 Claude Code 用户而言，message threads 已默认开启，500k 至 1M token 的请求其 TTFT 中位数下降约 35%。

要使用 message threads，请在 Messages API 请求中添加 `thread` 参数。第一个请求包含完整对话并开启一个线程。之后的每个请求只包含新消息和上一条响应的 ID。在轮次之间，我们把每个线程保存在内存中，在内存中加密，且不写入磁盘。线程在最后一次请求后 5 分钟过期，随后你的客户端会重新发送完整对话以开启新线程。虽然使用 message threads 后每个请求更小，但 Claude 每一轮仍会读取完整对话，因此 token 用量保持不变。

message threads 最适合延迟敏感的活跃会话，包括：

* **长时间运行的编程智能体**：每个工具结果或文件编辑都会加入对话。
* **计算机使用智能体**：截图留在会话线程中，而不是每一轮都重新上传。
* **文档和图片密集型工作流**：请求体积得以缩小。

智能体承载的上下文越多，message threads 能减少的首 token 时间就越多。

### 开始使用

message threads 现已在 Claude Platform 原生服务、Claude Platform on AWS、Claude in Microsoft Foundry，以及 [Google Cloud 上的 Claude 模型（Anthropic 托管）](https://claude.com/resources/articles/claude-models-on-google-cloud-anthropic-managed) 上公测。适用标准 Claude token 费率和现有速率限制。请参阅[文档](https://platform.claude.com/docs/en/build-with-claude/message-threads)开始使用。

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
