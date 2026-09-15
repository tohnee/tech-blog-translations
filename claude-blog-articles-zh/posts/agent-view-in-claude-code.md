---
title: "Claude Code 中的 Agent view"
title_en: "Agent view in Claude Code"
source: https://claude.com/blog/agent-view-in-claude-code/
crawled: 2026-09-14
translated: 2026-09-14
---

# Claude Code 中的 Agent view

> 原文：[Agent view in Claude Code](https://claude.com/blog/agent-view-in-claude-code/) · Claude 博客

今天我们推出 Claude Code 中的 agent view（智能体视图）：一个管理你所有 Claude Code 会话的地方。

过去并行运行智能体时，你可能不得不应付多个终端标签页、一个 tmux 网格，以及一份超载的「接下来要处理什么」的心记账本。

有了 Claude Code 的 agent view，你可以启动新的智能体、把它们发送到后台，只在 Claude 需要你的时候介入。哪些智能体在等你、哪些还在工作、哪些已经完成，一眼就能看清，从而轻松地同时驾驭多个智能体。

## 工作原理

Agent view 改进了在 CLI 中可视化并交互你的 Claude Code 会话的方式。

### 一屏尽览

从任意会话按左方向键，或在终端运行 `claude agents`，即可打开 agent view。每一行显示会话、它是否需要你的输入、其最后一次响应的内容，以及你上一次与它交互的时间。

### 不离开界面即可查看与回复

选中一个会话即可查看（peek）最近一轮对话。如果某个会话在等你做决定，直接在线回答，会话就会继续推进。按回车可以直接附着（attach）到你想浏览完整记录的会话上。

### 任何东西都能进后台

最后，用户可以把任何已有的会话用 `/bg` 加入 agent view，或者用 `claude --bg [task]` 完全跳过前台，直接启动一个全新会话。

## 开发者如何使用 agent view

我们从早期用户那里看到的几种模式：

- **扩展并发会话数量：**一次性派发多个想法，每个可选搭配一个 skill，然后回来查看一份待审查的 pull request 列表。
- **管理长时间运行的智能体：**PR 看护者、仪表盘更新器以及其他循环任务，都会在列表中直接显示下一次运行时间。
- **在不同会话之间导航：**当你正处于某个会话中，按左方向键，启动一个相关任务或一个快速的代码库提问，然后按右方向键回到你正在做的事情上。答案返回时，peek 会显示出来。
- **看清交付了什么：**每行的状态指示器加上 peek 中的标题，让你轻松扫出哪些会话产出了 PR。

## 开始使用

Agent view 现已作为研究预览（Research Preview）面向 Pro、Max、Team、Enterprise 和 Claude API 计划开放。运行 `claude agents` 即可选择加入。常规速率限制适用。更多信息请参阅[文档](https://code.claude.com/docs/en/agent-view)。

FAQ（常见问题）
