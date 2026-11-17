---
title: "为并行智能体重设计桌面版 Claude Code"
title_en: "Redesigning Claude Code on desktop for parallel agents"
date: 2026-04-14
source: https://claude.com/resources/articles/claude-code-desktop-redesign
crawled: 2026-11-17
translated: 2026-11-17
---

# 为并行智能体重设计桌面版 Claude Code

> 原文：[Redesigning Claude Code on desktop for parallel agents](https://claude.com/resources/articles/claude-code-desktop-redesign) · Claude 博客

今天，我们发布重新设计的 Claude Code 桌面应用，旨在帮助你同时运行更多 Claude Code 任务。

[下载应用](https://claude.com/download) · [阅读文档](https://docs.claude.com/claude-code)

它包含一个新的侧边栏，用于管理多个会话；一个可拖拽的布局，用于安排工作区；一个集成的终端和文件编辑器；此外还有性能与使用体验方面的改进。

## 全新的桌面体验

对许多开发者来说，智能体式工作的形态已经变了。你不再是一次输入一个提示词然后等待，而是在一个仓库中启动重构、在另一个仓库中修复 bug、在第三个仓库中编写测试，随着结果陆续返回逐一查看，在方向偏离时进行引导，并在发布前审查差异。

新应用正是为如今智能体式编程的真实感受而构建的：多件事情同时推进，而你坐在指挥者的位置上。

## 并行运行会话

新的侧边栏把所有活跃和最近的会话集中在一处。跨多个仓库启动工作，并在结果到达时在它们之间切换。

你可以按状态、项目或环境筛选，也可以按项目对侧边栏分组，以便更快地找到并恢复会话。当某个会话的 PR 合并或关闭后，它会自动归档，让侧边栏始终聚焦于仍在进行的工作。

当你在任务进行中需要提问时，可以打开侧边对话（⌘ + ; 或 Ctrl + ;）来分出分支。侧边对话从主线程获取上下文，但不会向主线程回写任何内容，以免干扰你的任务。

## 无需离开应用即可审查和发布

这次重新设计把更多常用工具带进了应用，让你无需切换到编辑器，就能审查、调整并发布 Claude 的工作成果：

* **集成终端**：在会话旁边运行测试或构建。
* **应用内文件编辑器**：打开文件、直接进行定点修改并保存更改。
* **更快的差异查看器**：为大型变更集重建了性能。
* **扩展的预览**：除了[在预览窗格中运行本地应用服务器](https://claude.com/resources/articles/preview-review-and-merge-with-claude-code)，现在还可在应用内打开 HTML 文件或 PDF。

每个窗格都支持拖拽。按你自己的工作方式，把终端、预览、差异查看器和聊天排成任意网格。

## 融入你的技术栈

桌面应用现在已与 CLI 插件能力对齐。如果你的组织集中管理 Claude Code 插件，或者你在本地安装了自己的插件，它们在桌面应用中的表现与终端中完全一致。

你仍然可以在本地或云端运行会话。SSH 支持现在从 Linux 扩展到 Mac，因此你可以在任一平台上将会话指向远程机器。

## 按你的工作方式定制

三种视图模式——Verbose、Normal 和 Summary——让你把界面从完整呈现 Claude 的工具调用细节，一路调节到只显示结果。新的键盘快捷键覆盖会话切换、创建和导航；按 `⌘ + /`（或 `Ctrl + /`）即可查看完整列表。新的用量按钮让你一眼看到上下文窗口和会话用量。

在底层，应用为了可靠性和速度进行了重建，现在会在 Claude 生成回复时实时流式传输。

## 开始使用

重新设计的桌面应用现已面向 Pro、Max、Ultra、Team 和 Enterprise 套餐的所有 Claude Code 用户开放，也可通过 Claude API 使用。

[下载应用](https://claude.com/download)，如果你已经安装，更新并重启即可。查阅[文档](https://docs.claude.com/claude-code)了解更多。
