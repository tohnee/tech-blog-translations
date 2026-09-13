---
title: "与 Jules 一起构建：你的异步编码智能体"
title_en: "Build with Jules, your asynchronous coding agent"
source: https://blog.google/innovation-and-ai/models-and-research/google-labs/jules/
site: google-blog
date: 2025-05-20
crawled: 2026-09-13
translated: 2026-09-13
---

# 与 Jules 一起构建：你的异步编码智能体

> 原文：[Build with Jules, your asynchronous coding agent](https://blog.google/innovation-and-ai/models-and-research/google-labs/jules/) · Google

去年 12 月，我们在 Google Labs 中推出了 [Jules](http://jules.google/)，作为对真正的编码智能体所能成为的样子的一次早期预览。它不是副驾驶，也不是代码补全的小助手，而是一个能够阅读你的代码、理解你的意图并着手干活的自主智能体。

今天，Jules 正式进入公开测试版（public beta），面向*所有人*开放。没有候补名单。在全球任何 [Gemini 模型可用的](https://ai.google.dev/gemini-api/docs/available-regions)地方均可使用。

### Jules 是什么？

Jules 是一个异步的智能体化编码助手，可直接与你现有的代码仓库集成。它将你的代码库克隆到一个安全的 Google Cloud 虚拟机（VM）中，理解你项目的完整上下文，并执行诸如以下任务：

- 编写测试
- 构建新功能
- 提供音频更新日志（audio changelogs）
- 修复 bug
- 升级依赖版本

Jules 以异步方式运行，当它在后台工作时，你可以专注于其他任务。完成后，它会呈现自己的计划、推理过程以及所做更改的 diff。Jules 默认为私有，不会用你的私有代码进行训练，你的数据也始终隔离在执行环境之内。

Jules 将代码库更新到新版 Node.js

我们正处在一个转折点：智能体化开发正在从原型走向产品，并迅速成为软件构建方式的核心。Jules 使用 Gemini 2.5 Pro，使其得以运用当今最先进的编码推理能力。配合其云端 VM 系统，它能够快速而精准地处理复杂的多文件更改和并发任务。

以下是你使用 Jules 能获得的功能一览：

- **适用于真实代码库**：Jules 不需要沙箱。它获取你现有项目的完整上下文，从而智能地推理各项更改。
- **并行执行：** 任务在云端 VM 内运行，支持并发执行。它可以同时处理多个请求。
- **可见的工作流程：** Jules 在进行更改之前会向你展示它的计划与推理。
- **GitHub 集成**：Jules 就在你熟悉的工作场景中运作，直接嵌入你的 GitHub 工作流。无需切换上下文，也无需额外配置。
- **用户可控性**：在执行之前、期间和之后都可以修改所呈现的计划，始终保持对你代码的掌控。
- **音频摘要：** Jules 提供近期提交的音频更新日志，把你的项目历史变成一份可以听的情境化更新日志。

![设置你的开发环境](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/set_up_environment.width-100.format-webp.webp)

设置你的开发环境

![连接 GitHub 并创建分支](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/connect_github_and_create_branch_.width-100.format-webp.webp)

连接 GitHub 并创建分支

![输入任务提示并批准 Jules 的计划](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/approve_plan.width-100.format-webp.webp)

输入任务提示并批准 Jules 的计划

![在 Jules 执行任务时给予反馈](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/give_feedback.width-100.format-webp.webp)

在 Jules 执行任务时给予反馈

![在面板中管理你的所有 Jules 任务](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/repoview.width-100.format-webp.webp)

在面板中管理你的所有 Jules 任务

在公开测试阶段，使用完全免费，但有用量限制。详情可在[此处](https://jules-documentation.web.app/)查阅。随着平台走向成熟，我们预计会在测试期结束后推出定价。

[立即开始使用 Jules](http://jules.google/)，并探索[文档](https://jules.google/docs)。
