---
title: "Grok Voice Agent API"
title_en: "Grok Voice Agent API"
date: 2025-12-17
source: https://x.ai/news/grok-voice-agent-api
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok Voice Agent API

> 原文：[Grok Voice Agent API](https://x.ai/news/grok-voice-agent-api) · xAI

2025 年 12 月 17 日

将 Grok Voice 的强大能力带给所有开发者。

收听这篇博文

收听这篇博文

今天，我们很高兴地推出 Grok Voice Agent API，让开发者能够构建会说数十种语言、能调用工具、能搜索实时数据的语音智能体。

Grok Voice Agent API 构建在与我们移动应用和 Tesla 车辆中服务数百万用户的 Grok Voice 相同的技术栈之上。我们非常高兴能通过 xAI API 把这项久经验证的技术开放给所有人。

Eve.Leo.Rex.Ara.Sal.

Rex

## [又聪明又快](#smart-and-fast)

Grok Voice Agents 是当前市场上最快、最智能的语音智能体。

我们完全自主构建了整个语音技术栈，从零训练了自己的语音活动检测（VAD）、tokenizer 和音频模型。对技术栈中每一个组件的细粒度掌控，使我们能够快速迭代，持续提升 Grok 的智能与速度。

Grok Voice Agent API 在 [Big Bench Audio](https://artificialanalysis.ai/models/speech-to-speech) 上排名第一——这是衡量语音智能体解决复杂问题能力的领先音频推理基准。Grok 的平均首音频时间（time-to-first-audio）不到 1 秒，比最接近的竞争对手快近 5 倍。

### Big Bench Audio：智能 vs 延迟

音频推理基准（由 Artificial Analysis 独立验证）

Score(%)

95%

Time to First Audio(s)

5 s

## [定价](#pricing)

Grok Voice Agent API 在成本效率上领先业界。开发者只需按连接时长以简单的固定费率每分钟 $0.05 计费。

### 每分钟成本

* OpenAI 按输入和输出 token 计费。$0.10/min 是一个极为保守的混合估算。在实际生产中，价格通常超过 $0.10/min。

## [多语言流畅性](#multilingual-fluency)

Grok Voice Agents 能以母语水平说数十种语言，准确把握方言和发音中的细微差别。Grok Voice Agents 经过训练，可以自动以用户所说的语言回应，并能在对话中途无缝切换语言。开发者也可以通过系统提示词指示 Grok 始终以特定语言回应。

在与 OpenAI Realtime API 的盲测正面人评中，Grok 在发音、口音、韵律等维度上一直被评为更受青睐的模型。

### 多语言表现

相对 OpenAI Realtime API 的胜率（盲测人评）

Grok

OpenAI Realtime API

## [Tesla 中的 Grok Voice](#grok-voice-in-tesla)

Tesla 是 Grok Voice Agent API 的关键设计合作伙伴，该 API 现已为数百万辆车上的 Grok 提供支持。

得益于一系列专用工具——让 Grok 能够查看车辆状态、查询路线、控制导航——Grok 就像是你的 Tesla 的自然延伸。Grok 会组合使用这些工具，提供无缝的路线规划体验。例如，让 Grok 规划一次公路旅行，它会在 X 上搜索推荐、计算最优路线并添加途经点，几秒钟内生成完整行程。

[](https://data.x.ai/grok-in-tesla.mp4)

Grok Voice Agents 可以执行任务并实时查询信息。通过我们的 API，开发者可以轻松集成自己的自定义工具，或使用 xAI 强大的实时搜索能力（覆盖 X 和整个网络）。

json

```
{
    "type": "session.update",
    "session": {
        "instructions": "You're an in-car assistant for Tesla.",
        "voice": "Ara",
        "tools": [
            { "type": "web_search" },
            { "type": "x_search" },
            {
                "type": "function",
                "name": "nav_search",
            }
        ]
    }
}
```

## [自然、富有表现力的声音](#natural-expressive-voices)

我们很高兴为 Grok Voice Agent API 提供多个富有表现力的声音，包括 Ara、Eve 和 Leo。我们的声音在日常对话中听起来自然，同时在医疗、金融、法律等领域也能出色地读出专业术语。

Customer Support

Finance

Healthcare

Legal

Customer Support

为了增强真实感，开发者甚至可以通过提示词让模型使用听觉线索，例如 `[whisper]`、`[sigh]` 和 `[laugh]`。

Have you heard the new Grok Voice?

whispers Let me tell you a secret... I am the smartest and best AI.

laugh Give it a go! Ask me anything.

I'll be your trusted personal assistant and closest companion.

ARA

## [开始构建](#start-building)

Grok Voice Agent API 兼容 OpenAI Realtime API 规范，也可以通过官方 [xAI LiveKit Plugin](https://docs.livekit.io/agents/integrations/xai/) 使用。

我们还构建了一个[语音 playground](https://console.x.ai/team/default/voice)，你可以直接在浏览器中测试各种声音。

我们会继续快速迭代。未来几周内，我们还将发布：

- 独立的文字转语音与语音转文字端点
- 在发音和延迟上表现更强的音频模型

我们迫不及待想听到你构建的成果！

### 试用我们的语音 playground

通过 xAI Cloud Console 与 Grok Voice Agent 对话

[打开 playground](https://console.x.ai/team/default/voice)

[![xAI Logo](/_next/static/media/xai.985f0fcf.svg)

xAI Cloud Console

Generate API key](https://console.x.ai)[![Book icon](/_next/static/media/docs.a3d5de8a.svg)

Read

Voice Agent API Docs](https://docs.x.ai/docs/guides/voice)[![Livekit Logo](/_next/static/media/livekit.0f6cec71.svg)

View

LiveKit Plugin](https://docs.livekit.io/agents/integrations/xai/)

在以下平台试用 Grok

[Web](https://grok.com)

[iOS](https://apps.apple.com/app/apple-store/id6670324846?pt=126952307&ct=x.ai%20Direct%20Link&mt=8)

[Android](https://play.google.com/store/apps/details?id=ai.x.grok&hl=en)

[X 上的 Grok](https://x.com/i/grok)

产品

[Grok](/grok)

[𝕏](https://x.com)

[API](/api)

[Grok 企业版](/grok/business)

[Grokipedia](https://grokipedia.com)

公司

[公司介绍](/company)

[招聘](/careers)

[联系我们](/contact)

[新闻](/news)

资源

[文档](https://docs.x.ai)

[隐私政策](/privacy-policy)

[安全](/security)

[安全中心](/safety)

[法律](/legal)

[状态](https://status.x.ai)
