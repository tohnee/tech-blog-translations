---
title: "Grok Build 现已开源"
title_en: "Grok Build is Now Open Source"
date: 2026-07-15
source: https://x.ai/news/grok-build-open-source
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok Build 现已开源

> 原文：[Grok Build is Now Open Source](https://x.ai/news/grok-build-open-source) · xAI

[返回新闻列表](/news)

2026 年 7 月 15 日

探索我们编码智能体与 TUI 背后的框架。

[在 GitHub 上查看](https://github.com/xai-org/grok-build)[试用 Grok Build](https://x.ai/cli)

我们正在开源 Grok Build——SpaceXAI 的编码智能体和 TUI。源代码现已在 [GitHub](https://github.com/xai-org/grok-build) 上公开。

公开代码是迈向一个健壮可靠的智能体框架（harness）最直接的方式。你可以阅读源码，看清从上下文组装到工具调用分发的每一个环节究竟如何运作。

开源也让这个框架更易于探索和扩展：如果你在研究 skills、插件、hooks、MCP 服务器或子智能体，源码就是每种机制如何加载和调用的权威参考。

最后，Grok Build 现在可以完全本地优先地运行：自己编译，指向你自己的本地推理，一切由你的 `config.toml` 驱动。

## [关于这个代码库](#about-the-codebase)

公开的源码包括：

- 智能体循环：上下文如何组装、模型响应如何解析、工具调用如何分发
- 工具集：智能体如何读取、编辑和搜索代码，以及如何运行命令
- 终端 UI：渲染、输入处理、计划审查和内联 diff 查看器
- 扩展系统：skills、插件、hooks、MCP 服务器和子智能体

到 [GitHub](https://github.com/xai-org/grok-build) 上探索源码吧。

[### 在 GitHub 上查看

在 GitHub 上浏览源码。](https://github.com/xai-org/grok-build)[### 获取 Grok Build

一条命令安装，在终端中运行。](/cli)
