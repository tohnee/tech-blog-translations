---
title: "Grok Build 中的智能体仪表盘"
title_en: "Agent Dashboard in Grok Build"
date: 2026-06-15
source: https://x.ai/news/agent-dashboard
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok Build 中的智能体仪表盘

> 原文：[Agent Dashboard in Grok Build](https://x.ai/news/agent-dashboard) · xAI

[返回新闻列表](/news)

2026 年 6 月 15 日

同时管理多个编码会话。查看每个会话在做什么，回复需要你介入的那些，并派发新任务。

---

智能体仪表盘（Agent Dashboard）把每个 Grok Build 会话都放到同一块屏幕上。你可以查看每个会话在做什么、让它们并行运行，只在需要输入时才介入。

在 shell 中运行 `grok dashboard`，或在任意会话内使用 `/dashboard`（`Ctrl+\`）。

`$ curl -fsSL https://x.ai/cli/install.sh | bash`

智能体 3⋅2 运行中│◇1 空闲│[+ 新建智能体]

运行中 2

⋅

为公共 API 添加限流 · main · 自动批准

刚刚

思考中

⋅

排查不稳定的结账测试 · main · 自动批准

刚刚

正在运行：cargo test --workspace

空闲 1

◇

会话 019e7f5f · main · 自动批准

1 分钟

❯派发一个新会话…

↑/↓:导航│Enter:创建│Tab:列表│Ctrl+.:快捷键

## [一览所有会话](#see-every-session-at-a-glance)

仪表盘按状态对会话排序，任何等待输入的会话都会被置顶，因此你可以优先处理阻塞项、让其余会话继续运行。快速扫一眼就能看出每个会话在做什么、运行了多久，无需打开任何会话就能保持全局感知。

工作分散在多个仓库？用 `Ctrl+S` 按工作目录分组。子智能体会归拢到启动它的会话之下，列表里展示的是你派发的工作本身，而不是其下层的展开。

## [查看与回复](#peek-and-reply)

选中某一行即可在不离开仪表盘的情况下查看该会话的最新输出，并直接在原处回复。空闲会话会立即收到消息；活跃会话则会把你的消息排队，等当前轮次结束后再处理。

当某个会话请求批准或提出问题时，其选项会内联显示。用方向键或数字键作答即可继续。多段式问题会逐个出现。

智能体 3◆1 等待中│⋅1 运行中│◇1 空闲│[+ 新建智能体]

等待中 1

◆

为公共 API 添加限流 · main · 自动批准

刚刚

待处理：问题

运行中 1

⋅

排查不稳定的结账测试 · main · 自动批准

1 分钟

正在运行：cargo test --workspace

空闲 1

◇

会话 019e7f5f · main · 自动批准

3 分钟

▸ 限流器的计数器应该存在哪里？请选择一项（或选「其他」自行输入）：

▸1.Redis，滑动窗口

2.内存，按实例

3.Postgres

4.Memcached

5.其他（自行输入答案）

↑/↓:选择│Enter:回答│Esc:返回│Ctrl+.:快捷键

## [派发新会话](#dispatch-new-sessions)

底部的输入框用于启动新会话。`Enter` 派发会话并留在仪表盘；`Shift+Enter` 派发后立即打开它。发送之前，可以设置模型、以规划模式启动，或允许该会话自行批准自己的编辑。

## [接管任意会话](#take-over-any-session)

打开任意会话即可接管其完整对话。无需返回列表即可在各会话之间前后切换，处理完后再回到仪表盘。关闭仪表盘不会中断任何会话，重新打开时它们都还在。

## [开始使用](#get-started)

智能体仪表盘随 Grok Build 一并提供。用一条命令安装，然后运行 `grok dashboard`，或在你已打开的任意会话中使用 `/dashboard`。

`$ curl -fsSL https://x.ai/cli/install.sh | bash`
