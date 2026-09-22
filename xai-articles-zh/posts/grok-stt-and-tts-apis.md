---
title: "Grok 语音转文字与文字转语音 API"
title_en: "Grok Speech to Text and Text to Speech APIs"
date: 2026-04-17
source: https://x.ai/news/grok-stt-and-tts-apis
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok 语音转文字与文字转语音 API

> 原文：[Grok Speech to Text and Text to Speech APIs](https://x.ai/news/grok-stt-and-tts-apis) · xAI

2026 年 4 月 17 日

快速而准确。自然、富有表现力的声音。定价简单。支持多语言。

收听这篇博文

收听这篇博文

今天，我们很高兴地宣布推出两个强大的独立音频 API：**Grok Speech to Text（STT，语音转文字）** 和 **Grok Text to Speech（TTS，文字转语音）**。它们构建在与 Grok Voice、Tesla 车辆和 Starlink 客户支持相同的底层技术栈之上。

这些独立端点让开发者能够轻松地将高质量语音功能集成到任何应用中——无论你是在构建语音智能体、实时转录工具、无障碍解决方案、播客，还是交互式音频体验。

[开始使用](https://docs.x.ai/developers/model-capabilities/audio/speech-to-text?campaign=stt-tts-blog)[试用 Playground](https://console.x.ai/playground/voice/text-to-speech)

## [语音转文字](#speech-to-text)

高准确率，低延迟。

- 通过我们的 [REST API](https://docs.x.ai/developers/rest-api-reference/inference/voice#speech-to-text---rest)，在毫秒级时间内从大型音频文件生成转录文本
- 通过我们延迟最低的 [WebSocket API](https://docs.x.ai/developers/rest-api-reference/inference/voice#speech-to-text---streaming) 实时转录语音

我们加入了词级时间戳、说话人分离（diarization）和多声道支持等强大功能。它还包含智能逆文本规范化（Inverse Text Normalization），能够正确处理数字、日期、货币等内容。

xAI

VOICE IN VS TEXT OUT

Thank you for holding, Anghared Llewelyn Bowen. I see here your mortgage rate lock is set at 3.75% and is valid until March 10th, 2024. Oisin MacGiolla Phadraigh, once we receive your signed documents by February 15th, we can aim for a closing date on March 20th. If you have any concerns, please feel free to email me at a.bowen@bestbank.com.

Match

Incorrect

0 mistakes

Other Models

VOICE IN VS TEXT OUT

Thank you for holding,  Anherd Lualin Bowen. I see here your mortgage rate lock is set at 3.75% and is valid until 03/10/2024. Oysen Magilla Fadrig, once we receive your signed documents by February, 15, we can aim for a closing date on March 20. If you have any concerns, please feel free to email me at a dot bowen at bestbank dot com.

Match

Incorrect

6 mistakes

### [定价](#pricing)

我们的定价简单且可预期：语音转文字批量处理为每小时 $0.10，流式处理为每小时 $0.20。完整细节和当前速率限制请参阅 [xAI API 控制台](https://console.x.ai)。

### 每小时成本（批量）

### 每小时成本（流式）

### [企业级转录](#enterprise-grade-transcription)

Grok STT 在电话通话、会议、视频/播客和电话语音等场景下与顶级商用模型进行了评测。它在实体识别以及医疗、法律、金融等商业用例上表现出色。

| 领域（词错误率） | Grok STT | ElevenLabs | Deepgram | AssemblyAI |
| --- | --- | --- | --- | --- |
| 电话通话实体 | 5.0% | 12.0% | 13.5% | 21.3% |
| 视频/播客 | 2.4% | 2.4% | 3.0% | 3.2% |
| 会议 | 10.9% | 12.2% | 16.3% | 15.7% |
| 电话语音 | 9.3% | 9.4% | 11.0% | 11.2% |
| 总体 | 6.9% | 9.0% | 11.0% | 12.9% |

大多数转录模型只会给你原始的口述文字。Grok Speech to Text 更进一步。

启用格式化后，该 API 会执行高级**逆文本规范化**，智能地将口述语言转换为规范的结构化输出：

My name is John Smith and my phone number is 4145551234.

I saw a transaction for 6.99 on my account.

Raw input

### [多语言流畅性](#multilingual-fluency)

Grok Speech to Text API 对 25 种以上语言提供强大的多语言支持，可以在语言之间无缝切换，一个节拍都不落下。

### [多声道与说话人分离（说话人识别）](#multichannel--diarization-speaker-identification)

使用同一个 API 转录多声道音频文件，实现完美的说话人分离。

借助说话人分离功能，在预录制和实时流式两种模式下均可检测说话人，并提供词级说话人 ID。

Speaker 1

Hello thanks for calling how can I help you today?

Speaker 2

I just signed up for an account and cannot login.

Speaker 1

I am sorry to hear that, what is your email address so I can check on that for you?

Speaker 2

It's john.smith@gmail.com

Speaker 1

Thanks and can you confirm your date of birth so I can validate the account please?

Speaker 2

Sure, it's March 16th 1985

## [文字转语音](#text-to-speech)

快速、自然、富有表现力的声音，支持语音标签（Speech Tags）。

- 通过我们的 [REST API](https://docs.x.ai/developers/model-capabilities/audio/text-to-speech#quick-start) 将长文本转换为语音
- 通过我们的 [WebSocket API](https://docs.x.ai/developers/model-capabilities/audio/text-to-speech#streaming-tts-websocket) 实时生成语音

### [细粒度控制](#fine-grained-control)

使用简单的内联与包裹式语音标签增添自然的韵律和情绪：`[laugh]`、`[sigh]`、`[whisper]`、`<emphasis>`、`<slow>`、`<pause>` 等等。这些控制手段让你无需复杂的标记语言即可创造出引人入胜、栩栩如生的语音表达。

Have you heard the new Grok Voice?

whispers Let me tell you a secret... I am the smartest and best AI.

laugh Give it a go! Ask me anything.

I'll be your trusted personal assistant and closest companion.

ARA

### [定价](#pricing-1)

文字转语音定价为**每 100 万字符 $4.20**，采用简单的用量计费，没有任何隐藏费用。

### 每百万字符成本

[![xAI Logo](/_next/static/media/xai.985f0fcf.svg)

Open

Voice Playground](https://console.x.ai/playground/voice/text-to-speech?campaign=stt-tts-blog)[![Open book icon](/_next/static/media/docs.a3d5de8a.svg)

Read

Speech to Text Docs](https://docs.x.ai/developers/model-capabilities/audio/speech-to-text?campaign=stt-tts-blog)[![Open book icon](/_next/static/media/docs.a3d5de8a.svg)

Read

Text to Speech Docs](https://docs.x.ai/developers/model-capabilities/audio/text-to-speech?campaign=stt-tts-blog)

在以下平台试用 Grok

[Web](https://grok.com)

[iOS](https://apps.apple.com/app/apple-store/id6670324846?pt=126952307&ct=x.ai%20Direct%20Link&mt=8)

[Android](https://play.google.com/store/apps/details?id=ai.x.grok&hl=en)

[X 上的 Grok](https://x.com/i/grok)

产品

[Grok](/grok)

[𝕏](https://x.com)

[Grok 企业版](/grok/business)

[Grokipedia](https://grokipedia.com)

API

[概览](/api#capabilities)

[语音 API](/api/voice)

[Imagine API](/api/imagine)

[定价](https://docs.x.ai/developers/models?cluster=us-east-1#detailed-pricing-for-all-grok-models)

[API 控制台登录](https://console.x.ai)

[文档](https://docs.x.ai)

公司

[公司介绍](/company)

[招聘](/careers)

[联系我们](/contact)

[新闻](/news)

资源

[隐私政策](/privacy-policy)

[隐私门户](/privacy-portal)

[安全](/security)

[安全中心](/safety)

[法律](/legal)

[状态](https://status.x.ai)
