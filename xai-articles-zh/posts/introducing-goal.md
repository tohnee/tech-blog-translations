---
title: "推出 /goal"
title_en: "Introducing /goal"
date: 2026-06-22
source: https://x.ai/news/introducing-goal
crawled: 2026-09-22
translated: 2026-09-22
---

# 推出 /goal

> 原文：[Introducing /goal](https://x.ai/news/introducing-goal) · xAI

[返回新闻列表](/news)

2026 年 6 月 22 日

在 Grok Build 中使用 /goal 执行长时间运行的自主任务。

---

今天，我们在 Grok Build 中推出 `/goal`。这一新模式带来长时间运行的自主执行，帮助你把更大的实现任务交给智能体。

现已登陆 Grok Build。一条命令即可安装 CLI，并使用你的账号登录：

`$ curl -fsSL https://x.ai/cli/install.sh | bash`

[升级订阅](https://grok.com/supergrok?referrer=introducing-goal)

Introducing /goal

大多数编码会话都需要来回往复地执行和验证。有了 `/goal`，智能体会一直工作到任务完成并通过验证——无论是审查代码、检查网页，还是执行脚本。

## [一行设定目标](#set-a-goal-in-one-line)

给 `/goal` 一个目标，剩下的交给 Grok Build：

Copy

```
/goal Migrate the auth module to the new API
```

bash

它会规划方案、把工作拆解成进度清单，然后开始执行。在它工作的同时，你可以继续向智能体补充指令。

新模式还提供用于监控和引导长任务的附加命令：

Copy

```
/goal status     # see the live progress panel
/goal pause      # stop work, keep the goal
/goal resume     # pick back up
/goal clear      # drop the goal entirely
```

bash

目标完成后，面板会切换为 **Complete**，清单上的每一项都已勾选。

## [快速上手](#getting-started)

用上面的命令安装 Grok Build，然后调用 `/goal`，交出你的第一个长任务。
