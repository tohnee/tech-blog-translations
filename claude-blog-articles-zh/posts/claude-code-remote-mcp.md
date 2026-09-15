---
title: "Claude Code 支持远程 MCP"
title_en: "Remote MCP support in Claude Code"
source: https://claude.com/blog/claude-code-remote-mcp/
crawled: 2026-09-14
translated: 2026-09-14
---

# Claude Code 支持远程 MCP

> 原文：[Remote MCP support in Claude Code](https://claude.com/blog/claude-code-remote-mcp/) · Claude 博客

今天，我们宣布 Claude Code 开始支持远程 MCP 服务器。连接你喜爱的工具和数据源，个性化你的编码体验，而无需管理本地服务器。

### **将 Claude Code 作为你的主要开发界面**

Claude Code 可以访问 MCP 服务器暴露的工具和资源，从而能够从你的第三方服务（如开发工具、项目管理系统和知识库）中拉取上下文，并在这些服务中执行操作。

你可以将 Claude Code 与任何远程 MCP 服务器集成，而不断壮大的服务器生态意味着新能力在不断上线。

例如，将 Claude Code 与 Sentry MCP 服务器集成后，你可以访问 Sentry 中的错误和问题（issue）。然后，你可以借助这些问题的上下文进行调试，而不必离开终端。

你还可以将 Claude Code 与 Linear MCP 服务器集成，在活跃项目的上下文中开展工作。

Linear 工程主管 Tom Moor 分享道：「Linear 的 MCP 集成把 Linear 的项目和问题直接带进了 Claude Code。借助来自 Linear 的结构化实时上下文，Claude Code 可以拉取问题详情和项目状态——工程师在规划、写代码和管理问题之间切换时得以保持心流。更少的标签页，更少的复制粘贴。更好的软件，更快的交付。」

### **无缝连接，极简维护**

相比本地服务器，远程 MCP 服务器维护成本更低：只需把供应商的 URL 添加到 Claude Code——无需任何手动设置。更新、扩容和可用性都由供应商处理，你可以专注于构建，而不必操心服务器基础设施。

Claude Code 还为远程 MCP 服务器提供原生 OAuth 支持，确保与现有账户的安全连接。只需对你的服务器完成一次身份验证，其余都由 Claude Code 处理——无需管理 API 密钥，也无需存储凭据。

### **开始使用**

远程 MCP 服务器支持现已在 Claude Code 中可用。请查看[文档](https://docs.anthropic.com/en/docs/claude-code/mcp)开始使用，或浏览我们的 [MCP 目录](http://anthropic.com/partners/mcp)查看推荐的服务器。

FAQ（常见问题）
