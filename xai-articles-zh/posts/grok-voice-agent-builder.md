---
title: "推出 Voice Agent Builder"
title_en: "Introducing the Voice Agent Builder"
date: 2026-07-01
source: https://x.ai/news/grok-voice-agent-builder
crawled: 2026-09-22
translated: 2026-09-22
---

# 推出 Voice Agent Builder

> 原文：[Introducing the Voice Agent Builder](https://x.ai/news/grok-voice-agent-builder) · xAI

[返回新闻列表](/news)

2026 年 7 月 1 日

不到 2 分钟即可创建一个个性化的语音智能体，无需编写一行代码。

[免费试用](https://console.x.ai/team/default/voice/agents?campaign=agent-builder-blog&builder=1)[了解 Voice Agents](/voice)

今天，我们宣布推出测试版 Voice Agent Builder：一个在 [Grok Voice](/news/grok-voice-think-fast-1) 上配置生产级语音智能体的无代码平台。

它面向那些需要高并发生产语音智能体、但不想从零构建周边技术栈的运营者和开发者。开箱即用，你可以在一处获得电话接入、知识检索、工具、护栏（guardrails）、MCP 和可观测性。你也可以保留现有的东西：通过 SIP 迁移已有电话号码，把工具接入你的 API 和 MCP 服务器，或通过 WebSocket 连接你自己的客户端。

大多数语音技术栈是把三个 API——语音转文字、语言模型、文字转语音——拼接在一起，而且每个环节往往由不同的提供商托管。每一次跳转都会增加成本、延迟和新的故障模式。Voice Agent Builder 是构建在为 Grok Voice 打造的语音到语音（speech-to-speech）通路上的单一界面，与模型紧密耦合，而非由三部分拼装而成。

[Your browser does not support the video tag.](https://data.x.ai/releases/voice/agent-builder/builder-demo.mp4)

## [用我们所能找到的最难的通话来训练](#trained-on-the-hardest-calls-we-could-find)

真实的通话伴随着低质量的电话音频、背景噪声、浓重的口音、打断，以及话说到一半改主意的来电者。通话背后的工作流含糊不清、要跨越数十个工具，还可能使用 25 种以上的任意一种语言。

我们正是用这些通话训练 [Grok Voice](/news/grok-voice-think-fast-1) 的。τ-voice Bench 会在同样的条件下衡量智能体。

τ-voice Bench 排行榜

Grok Voice Think Fast 1.0

67.367.3%

Gemini 3.1 Flash Live

43.843.8%

GPT Realtime 1.5

35.335.3%

OverallRetailAirlineTelecom

## [两分钟得到一个智能体](#two-minutes-to-an-agent)

设置很简单：用平实的语言描述通话应该如何进行，然后挂上你的文档、工具和护栏。大约两分钟内，你就可以从零得到一个可用的智能体。

### [教它你的业务](#teach-it-your-business)

一个智能体始于一段描述通话应如何展开的提示词。模型会实时推理，因此能够遵循长篇指令并处理含糊的请求。

它*知道*的东西来自**知识库**。你上传常见格式（纯文本、Markdown、Word、PowerPoint、Excel、HTML、JSON 等）的文档，智能体在通话过程中从中检索。文档被组织成**集合（collection）**，你可以把一个集合挂到一个或多个智能体上，也可以在智能体之间共享，这样政策、产品规格和运维手册只需保存在一处，而不必粘贴进每个提示词。

### [采取行动](#take-action)

了解业务只是客服或销售通话的一半。智能体还需要**行动**。它们要查询信息、修改记录、转接人工，或在对话结束后闭环收尾。

**工具（tools）** 和**连接器（connectors）** 就是实现这一切的方式。在一条预约热线上，智能体可以在 Google Calendar 或 Outlook Calendar 里安排预约，然后通过你的邮件服务商发送确认。在客服场景，一个 API 请求就可以在你自己的系统里查询订单状态或发起退款。当答案不只在你的文档里时，网络搜索或 X 搜索可以拉取最新的公开信息。工单可以在 Linear 或 Notion 中管理，文件则来自 Google Drive 或 OneDrive。

如果来电者需要人工服务，智能体可以把通话转接给你的团队。任务完成后，它可以干净利落地结束通话。在整个对话过程中，它会发送实时通知，让你的团队随时了解智能体做了什么，并在需要时介入。

search_help_center

transfer_to_human

### [给它一个声音和一个号码](#give-it-a-voice-and-a-number)

智能体可以使用 80 多个内置声音中的任意一个，也可以使用由约两分钟音频克隆而来的你的品牌声音。每个账号附带一个免费电话号码，从第一次测试通话到生产流量都可直接使用；直连 SIP 则可以接入来自任何主流电话服务商的现有号码。你也可以不用电话，直接在浏览器中测试改动。

### [回顾通话](#review-the-calls)

每一通电话都会被录音并转录。你可以回放音频、阅读转录文本，并查看智能体使用了哪些工具。护栏为智能体设定不该做的事情的边界，比如复述卡号或讨论脚本之外的话题。

## [费用几何](#what-it-costs)

我们相信定价应该简单透明。智能体按我们的 API 费率计费（目前为[每分钟音频 $0.05](https://docs.x.ai/developers/pricing#voice-api-pricing)），声音已包含在内，无单独的平台费。免费分配号码上的电话接入为额外的每分钟 $0.01。

其他语音技术栈通常对每个单独组件（识别、推理、合成和平台）分别计费，各自有独立的计量和定价。我们想要的是极少数几个计量项，乘以通话量就完事。

## [试试看](#try-it)

语音智能体，耳朵比基准测试更能说明问题。构建一个，把你最难的工作流交给它，然后打个电话试试。

[免费试用](https://console.x.ai/team/default/voice/agents?campaign=agent-builder-blog&builder=1)[了解 Voice Agents](/voice)
