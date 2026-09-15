---
title: "用 Claude Code 预览、评审与合并"
title_en: "Preview, review, and merge with Claude Code"
source: https://claude.com/blog/preview-review-and-merge-with-claude-code/
crawled: 2026-09-14
translated: 2026-09-14
---

# 用 Claude Code 预览、评审与合并

> 原文：[Preview, review, and merge with Claude Code](https://claude.com/blog/preview-review-and-merge-with-claude-code/) · Claude 博客

今天，我们发布了多项 Claude Code 改进：预览运行中的应用、自动评审代码、自动修复并合并 PR，以及在桌面端、移动端和 CLI 之间无缝切换。这些更新合在一起，能让你把更少的时间花在围绕代码的琐事上，把更多时间花在你享受的部分。

## **写代码，看它跑起来**

桌面版 Claude Code 现在可以启动开发服务器，并直接在桌面界面中预览正在运行的应用。Claude 会查看 webapp 的 UI、读取控制台日志、捕捉错误并持续迭代，你不必切到浏览器里，再手动向 Claude 描述你看到的现象。你还可以在预览中选中视觉元素，把反馈直接传给 Claude 进行迭代。

## **推送之前先评审代码**

当改动看起来没问题后，可以用新的「Review code（评审代码）」按钮请 Claude 评审。Claude 会检查你的本地 diff，直接在桌面端的 diff 视图里留下评论，标出 bug、提出建议，并就地发现潜在问题。

在任何东西离开你的电脑之前，你立刻就多了一双眼睛帮你抓住明显的问题；你还可以让 Claude 处理这些行内评论并做出修改。

## **不离开应用也能监控 PR**

对于托管在 GitHub 上的代码，你还可以直接在桌面应用中监控 pull request 状态。在你打开一个 PR 之后，Claude Code 会在底层借助 GitHub CLI 追踪它的状态，包括 CI 检查的通过与失败。

你还可以启用自动修复（auto-fix），让 Claude 自动尝试修复它检测到的任何 CI 失败。如果启用自动合并（auto-merge），一旦所有检查通过，Claude 还会尝试合并 PR。

你可以在一个 Claude Code 会话里完成一项任务并开出 PR，然后转去做新任务。在后台，Claude Code 会持续监控原任务的 PR，并尝试修复 CI 失败，等你切回那项任务时，PR 已就绪可合并（或已自动合并）。

## **从上次中断的地方继续**

会话现在可以跟着你走。当你在 CLI 中用 Claude Code 开启一个会话后，运行 `/desktop` 即可把完整的会话上下文带进桌面应用。

你也可以使用「Continue with Claude Code on the web（在网页版 Claude Code 中继续）」按钮，把本地桌面应用的会话迁移到云端。在桌面应用上开始一项任务，然后在网页上，或用 Claude 移动应用在手机上接着做。

## **开始使用**

这些更新现已向所有用户开放。更新或下载[桌面版 Claude Code](https://claude.com/download) 即可开始使用。浏览[文档](https://code.claude.com/docs/en/desktop)了解更多。

FAQ（常见问题）
