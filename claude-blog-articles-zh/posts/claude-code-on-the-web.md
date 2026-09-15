---
title: "网页版 Claude Code"
title_en: "Claude Code on the web"
source: https://claude.com/blog/claude-code-on-the-web/
crawled: 2026-09-14
translated: 2026-09-14
---

# 网页版 Claude Code

> 原文：[Claude Code on the web](https://claude.com/blog/claude-code-on-the-web/) · Claude 博客

***更新：*** *除 Pro 和 Max 用户之外，网页版 Claude Code 现已面向拥有高级席位（premium seat）的 Team 和 Enterprise 用户开放研究预览（research preview）。对这些用户，网页版 Claude Code 默认开启，账户管理员可以在 Claude 设置中切换访问权限。2025 年 11 月 12 日*

今天，我们推出网页版 Claude Code：一种直接从浏览器委派编码任务的新方式。

现以研究预览形式进入 beta 阶段，你可以把多个编码任务指派给 Claude，让它们运行在 Anthropic 托管的云基础设施上——非常适合清理 bug 积压、处理例行修复，或开展并行开发工作。

## 并行运行编码任务

网页版 Claude Code 让你无需打开终端就能启动编码会话。连接你的 GitHub 仓库，描述你的需求，Claude 便会完成实现。

每个会话都在自己的隔离环境中运行，并提供实时进度跟踪；在 Claude 处理任务的过程中，你还可以主动引导它调整方向。

有了在云端运行的 Claude Code，你现在可以在单一界面中**跨不同仓库并行运行多个任务**，并通过自动创建 PR 和清晰的变更摘要来**更快交付**。

## 适配每一种工作流

网页界面是你现有 Claude Code 工作流的补充。在云端运行任务对以下场景尤其有效：

- 解答关于项目如何运作、仓库结构如何组织的问题
- bug 修复以及例行的、定义明确的任务
- 后端变更——Claude Code 可以用测试驱动开发（TDD）来验证变更

你还可以在移动端使用 Claude Code。作为本次研究预览的一部分，我们在 iOS 应用中提供了 Claude Code，让开发者可以随时随地与 Claude 一起编码。这是一个早期预览版，我们希望根据你的反馈快速打磨移动端体验。

## 安全优先的云端执行

每个 Claude Code 任务都运行在带有网络和文件系统限制的隔离沙箱环境中。Git 交互通过一个安全代理服务处理，确保 Claude 只能访问获得授权的仓库——帮助你的代码和凭据在整个工作流中始终受到保护。

你还可以添加自定义网络配置，选择 Claude Code 在其沙箱中可以连接哪些域名。例如，你可以允许 Claude 通过互联网下载 npm 软件包，以便它运行测试并验证变更。

深入了解 Claude Code 的沙箱机制，请阅读我们的[工程博客](https://www.anthropic.com/engineering/claude-code-sandboxing)与[文档](https://docs.claude.com/en/docs/claude-code/sandboxing)。

## 开始使用

网页版 Claude Code 现已面向 Pro 和 Max 用户开放研究预览。访问 [claude.com/code](http://claude.com/code)，连接你的第一个仓库，开始委派任务。

基于云端的会话与其他所有 Claude Code 用途共享速率限制。请[浏览我们的文档](https://docs.claude.com/en/docs/claude-code/claude-code-on-the-web)了解更多。

FAQ（常见问题）
