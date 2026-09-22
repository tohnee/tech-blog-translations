---
title: "Grok Voice Think Fast 1.0"
title_en: "Grok Voice Think Fast 1.0"
date: 2026-04-23
source: https://x.ai/news/grok-voice-think-fast-1
crawled: 2026-09-22
translated: 2026-09-22
---

# Grok Voice Think Fast 1.0

> 原文：[Grok Voice Think Fast 1.0](https://x.ai/news/grok-voice-think-fast-1) · xAI

2026 年 4 月 23 日

我们最强大的语音智能体现已通过 API 提供。

收听这篇博文

[![xAI Logo](/_next/static/media/xai.985f0fcf.svg)

Try it out

Open playground](https://console.x.ai/playground/voice/agent?campaign=think-fast-blog)[![Open book icon](/_next/static/media/docs.a3d5de8a.svg)

Docs

Get started](https://docs.x.ai/developers/model-capabilities/audio/voice-agent?campaign=think-fast-blog)

[![xAI Logo](/_next/static/media/xai.985f0fcf.svg)

Try it out

Open playground](https://console.x.ai/playground/voice/agent?campaign=think-fast-blog)[![Open book icon](/_next/static/media/docs.a3d5de8a.svg)

Docs

Get started](https://docs.x.ai/developers/model-capabilities/audio/voice-agent?campaign=think-fast-blog)

收听这篇博文

今天，我们很高兴地宣布 xAI 语音智能体能力的又一次跃升：推出 `grok-voice-think-fast-1.0`——我们的新旗舰语音模型。

这个新模型擅长客服、销售和企业应用中复杂、含糊、多步骤的工作流。它尤其适合那些要求精确数据录入和高频工具调用来满足用户请求的高风险场景。

真实客服工作流

Multiple tools • Ambiguous customer request • grok-voice-think-fast-1.0

#### 观看实际演示

按下播放，收听完整对话，并实时查看智能体的工具使用过程。

Play conversation

0.0s

## [为真实世界的混乱而生](#built-for-the-messiness-of-the-real-world)

我们通过与 Starlink 等合作伙伴的紧密协作打造了 `grok-voice-think-fast-1.0`，将顶尖智能与低响应延迟和自然的对话能力结合在一起。

我们的模型优先保证敏捷的响应和无与伦比的成本效益，同时在准确性和工具编排上毫不妥协。其成果是一个让团队有信心在几乎所有可以想到的用例中部署复杂多轮语音体验的模型：客户支持、电话销售、预约挂号、餐厅订位等等。

这个新模型在 τ-voice Bench 排行榜上位居榜首。该基准会在噪声、口音、打断和轮替（turn-taking）等真实条件下评测全双工语音智能体。[基准细节见此处](https://taubench.com/#leaderboard?benchmark=voice)。

### τ-voice 排行榜

### 零售（Retail）

嘈杂环境下的订单处理、退货与促销

Grok Voice Think Fast 1.0

Grok Voice Fast 1.0

Gemini 3.1 Flash Live

GPT Realtime 1.5

### 航空（Airline）

改签、延误与复杂行程

Grok Voice Think Fast 1.0

Grok Voice Fast 1.0

Gemini 3.1 Flash Live

GPT Realtime 1.5

### 电信（Telecom）

套餐变更、账单争议、技术排障

Grok Voice Think Fast 1.0

Grok Voice Fast 1.0

Gemini 3.1 Flash Live

GPT Realtime 1.5

Grok Voice Think Fast 1.0

Grok Voice Fast 1.0

Gemini 3.1 Flash Live

GPT Realtime 1.5

该模型已经在最严苛的真实条件下经受实战检验：电话音频、背景噪声、浓重口音和频繁打断。它原生支持 25 种以上语言，非常适合全球部署。

## [精确的数据录入与复述](#precise-data-entry-and-read-back)

收集并确认用户信息对许多工作流至关重要。Grok Voice 能够无缝收集电子邮件地址、实体街道地址、电话号码、全名、账号和其他结构化数据——即使信息说得很快或带有浓重口音。它能优雅地处理言语不流畅之处，并像人类一样接受自然的更正。

Processing user input

The model handles the spoken corrections and extracts the intended address.

Calling custom tool

Invoking the address lookup tool with the corrected query parameter.

Confirming the result

Reading back the normalized address with location for user confirmation.

## [零额外延迟的实时推理](#real-time-reasoning-with-zero-added-latency)

Grok Voice Think Fast 会在后台进行推理，使它能够实时思考棘手的查询和工作流，而完全不影响响应延迟。这让它既能给出聪明的回答，又保留了自然对话所需的敏捷。

## [更难被忽悠](#harder-to-fool)

语音模型往往会给出自信且听起来头头是道、实则完全错误的答案。我们让 `grok-voice-think-fast-1.0` 在回答前先推理边界情况，能抓住其他模型会犯下的明显错误。

Prompt

Which months of the year are spelled with the letter X?

grok-voice-think-fast-1.0

None of the months are spelled with the letter X. You can check them all, but X doesn't appear in any month name.

Other Models

Only one month is spelled with the letter X. It's February.

## [为 Starlink 的客户支持与销售提供支持](#powering-customer-support-and-sales-for-starlink)

Grok Voice 支撑着 Starlink 在 [+1 (888) GO STARLINK](tel:+18884678275) 的电话销售和客户支持体验。这需要跨多种语言工作，帮助客户完成支持场景，并通过销售完成新客户开通：

- **20% 转化率。** 每 5 次销售咨询中就有 1 次，客户在与 Grok 通话期间直接购买了 Starlink 服务。
- **70% 解决率。** 大多数客户支持咨询由 Grok Voice 智能体自主解决，全程无需人工介入。
- **28 个工具。** 这一个智能体在数百个支持与销售工作流中使用数十种不同的工具。
- **准确性至关重要。** Grok 处理的是高风险决策；该模型会自主执行硬件排障工作流、发放硬件更换并授予服务抵扣。

![Starlink 终端](/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fstarlink-terminal.2a4ead17.webp&w=3840&q=75)

[![xAI Logo](/_next/static/media/xai.985f0fcf.svg)

Open

Voice Playground](https://console.x.ai/playground/voice/agent?campaign=think-fast-blog)[![Open book icon](/_next/static/media/docs.a3d5de8a.svg)

Read

Voice API Docs](https://docs.x.ai/developers/model-capabilities/audio/voice-agent?campaign=think-fast-blog)

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
