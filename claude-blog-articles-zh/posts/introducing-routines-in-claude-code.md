---
title: "在 Claude Code 中推出例行任务（routines）"
title_en: "Introducing routines in Claude Code"
source: https://claude.com/blog/introducing-routines-in-claude-code/
crawled: 2026-09-14
translated: 2026-09-14
---

# 在 Claude Code 中推出例行任务（routines）

> 原文：[Introducing routines in Claude Code](https://claude.com/blog/introducing-routines-in-claude-code/) · Claude 博客

今天，我们在 Claude Code 中以研究预览（research preview）的形式推出例行任务（routines）。例行任务是一项只需配置一次的 Claude Code 自动化——包含一个提示、一个仓库和若干连接器——之后可以按计划运行、由 API 调用触发，或在响应事件时运行。例行任务运行在 [Claude Code 的网页基础设施](https://code.claude.com/docs/en/claude-code-on-the-web)上，因此任何事情都不依赖于你的笔记本是否开机。

开发者已经在用 Claude Code 自动化软件开发周期，但在此之前，cron 任务、基础设施以及 MCP 服务器等额外工具都得自己管理。例行任务自带对你仓库和[连接器](https://claude.com/connectors)的访问能力，因此你可以把自动化打包起来，让它们按计划或触发条件运行。

## 工作原理

### 计划型例行任务

给 Claude Code 一个提示和一个节奏（每小时、每晚或每周），它就会按这个计划运行：

```
Every night at 2am: pull the top bug from Linear, attempt a fix, and open a draft PR.
```

如果你正在 CLI 中使用 [/schedule](https://code.claude.com/docs/en/scheduled-tasks#compare-scheduling-options)，那些任务现在就是计划型例行任务。

### API 例行任务

你还可以把例行任务配置为由 API 调用触发。每个例行任务都有自己的端点和 auth token。POST 一条消息，就能拿回一个会话 URL。把 Claude Code 接入你的告警系统、部署钩子、内部工具——任何能发起 HTTP 请求的地方：

```
Read the alert payload, find the owning service, and post a triage summary to #oncall with a proposed first step.
```

如果你是在 Claude Platform 上构建云端托管智能体，而不是在自动化 Claude Code，那么 [Claude Managed Agents 中的计划部署](https://claude.com/blog/whats-new-in-claude-managed-agents)可以让你自己的智能体获得同样的按计划运行行为。

### Webhook 例行任务，从 GitHub 开始

你可以把例行任务订阅为响应 GitHub 仓库事件自动启动。Claude 会为每个匹配你过滤条件的 PR 创建一个新会话，并运行你的例行任务。

```
Please flag PRs that touch the /auth-provider module. Any changes to this module need to be summarized and posted to #auth-changes.
```

Claude 为每个 PR 开启一个会话，并持续把该 PR 的更新喂给这个会话，因此它能处理评论、CI 失败等后续事项。

我们计划未来把基于 webhook 的例行任务扩展到更多事件来源。

## 各团队正在构建什么

在早期创建例行任务的用户中，已经浮现出几种常见模式：

- 待办管理：每晚分诊新 issue、打标签、指派，并把摘要发到 Slack
- 文档漂移：每周扫描已合并的 PR，标记引用了已变更 API 的文档，并开立更新 PR
- 部署验证：你的 CD 流水线在每次部署后发帖，Claude 对新构建运行冒烟检查、扫描错误日志中的回归，并向发布频道发出放行/中止（go/no-go）结论
- 告警分诊：把 Datadog 指向例行任务的端点，Claude 拉取调用链路（trace），将其与近期的部署关联起来，并在值班人员打开告警页之前就备好一份修复草案
- 反馈处理：文档反馈组件或内部仪表盘发出报告，Claude 针对该仓库开一个会话并带着问题上下文，起草修改

### GitHub 例行任务

- 库移植：每个合并进 Python SDK 的 PR 都会触发一个例行任务，把变更移植到对应的 Go SDK，并开一个对应的 PR
- 定制代码审查：PR 打开时，按你们团队自己的清单在安全与性能两方面逐一检查，在人类审查者介入之前留下行内评论

## 开始使用

例行任务现面向启用了 [Claude Code 网页版](https://code.claude.com/docs/en/claude-code-on-the-web#who-can-use-claude-code-on-the-web)的 Pro、Max、Team 和 Enterprise 计划 Claude Code 用户开放。前往 [claude.ai/code](http://claude.ai/code) 创建你的第一个例行任务，或在 CLI 中输入 /schedule。

例行任务与交互式会话一样消耗订阅用量限额。此外，例行任务还有每日上限：Pro 用户每天最多运行 5 个例行任务，Max 用户每天最多 15 个，Team 和 Enterprise 用户每天最多 25 个。超出这些限额后，你可以用额外用量运行更多例行任务。更多信息请[参阅文档](http://code.claude.com/docs/en/routines)。

FAQ（常见问题）
