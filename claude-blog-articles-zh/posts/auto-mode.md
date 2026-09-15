---
title: "Claude Code 的自动模式"
title_en: "Auto mode for Claude Code"
source: https://claude.com/blog/auto-mode/
crawled: 2026-09-14
translated: 2026-09-14
---

# Claude Code 的自动模式

> 原文：[Auto mode for Claude Code](https://claude.com/blog/auto-mode/) · Claude 博客

***更新****：自动模式（auto mode）现已在 Claude Code 中面向所有用户正式可用。（2026 年 7 月 10 日）*

今天，我们推出自动模式（auto mode），这是 Claude Code 中一种新的权限模式：由 Claude 代表你做出权限决策，同时有安全防护机制在动作运行之前对其进行监控。它目前以研究预览（research preview）的形式面向 Team 计划开放，并将在未来几天内推向 Enterprise 计划和 API 用户。

## 工作原理

Claude Code 的默认权限设置是刻意保守的：每次文件写入和 bash 命令都需要请求批准。这是一个安全的默认值，但也意味着你无法启动一个大任务然后走开，因为 Claude 会在过程中频繁请求人工批准。虽然有些开发者选择用 --dangerously-skip-permissions 绕过权限检查，但跳过权限可能导致危险且具有破坏性的后果，不应在隔离环境之外使用。

自动模式是一条中间路线，让你以更少的打断运行更长的任务，同时比跳过全部权限引入更少的风险。在每次工具调用运行之前，分类器（classifier）会审查它，以[检查潜在的破坏性动作](https://code.claude.com/docs/en/permission-modes#what-the-classifier-blocks-by-default)，比如批量删除文件、敏感数据外泄或恶意代码执行。

被分类器判定为安全的动作会自动执行，有风险的动作则会被阻止，并引导 Claude 改用其他方法。如果 Claude 坚持执行持续被阻止的动作，它最终会向用户触发一次权限提示。

## 预期表现

与 --dangerously-skip-permissions 相比，自动模式降低了风险，但并未完全消除风险，我们仍建议在隔离环境中使用它。分类器仍可能放行某些有风险的动作：例如，当用户意图不明确，或者 Claude 对你的环境缺乏足够上下文、无法判断某个动作可能带来额外风险时。它也可能偶尔误拦无害动作。我们会随着时间推移持续改进这一体验。

自动模式可能会对工具调用的 token 消耗、成本和延迟产生小幅影响。

## 开始使用

自动模式现已作为研究预览面向 Claude Team 用户在 Claude Code 中开放，并将在未来几天内推广到 Enterprise 和 API 用户。它同时兼容 Claude Sonnet 4.6 和 Opus 4.6。

- **面向管理员**：自动模式很快将对 Enterprise、Team 和 Claude API 计划上的所有 Claude Code 用户开放。要在 CLI 和 VS Code 扩展中禁用它，请在你的托管设置（managed settings）中设置 "disableAutoMode": "disable"。在 Claude 桌面应用中，自动模式默认关闭，可以通过 Organization Settings -> Claude Code 开启。
- **面向开发者**：运行 `claude --enable-auto-mode` 启用自动模式，然后用 Shift+Tab 切换到该模式。在桌面端和 VS Code 扩展中，先在 Settings -> Claude Code 中开启自动模式，然后在会话中的权限模式下拉菜单中选择它。

更多信息请[查阅文档](https://code.claude.com/docs/en/permission-modes#eliminate-prompts-with-auto-mode)。

FAQ（常见问题）
