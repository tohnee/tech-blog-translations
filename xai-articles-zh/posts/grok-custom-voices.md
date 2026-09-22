---
title: "自定义声音与声音库"
title_en: "Custom Voices and Voice Library"
date: 2026-04-30
source: https://x.ai/news/grok-custom-voices
crawled: 2026-09-22
translated: 2026-09-22
---

# 自定义声音与声音库

> 原文：[Custom Voices and Voice Library](https://x.ai/news/grok-custom-voices) · xAI

2026 年 4 月 30 日

你的声音，你的品牌。用一小段录音克隆声音，并在 xAI 控制台管理你的整个声音目录。

收听这篇博文

[克隆你的声音](https://console.x.ai/team/default/voice/voice-library?campaign=custom-voices-blog)[阅读文档](https://docs.x.ai/developers/model-capabilities/audio/custom-voices?campaign=custom-voices-blog)

[克隆你的声音](https://console.x.ai/team/default/voice/voice-library?campaign=custom-voices-blog)[阅读文档](https://docs.x.ai/developers/model-capabilities/audio/custom-voices?campaign=custom-voices-blog)

收听这篇博文

今天，我们推出**自定义声音（Custom Voices）**。只需几秒钟音频即可克隆你的声音，并即刻在 [Grok 文本转语音](https://docs.x.ai/developers/model-capabilities/audio/text-to-speech?campaign=custom-voices-blog)和 [语音智能体 API](https://docs.x.ai/developers/model-capabilities/audio/voice-agent?campaign=custom-voices-blog) 中使用。

Tyler

SpaceX 直播主持人

原声

克隆

与自定义声音同步亮相的还有全新的**声音库（Voice Library）**，让你的团队在 [xAI 控制台](https://console.x.ai/team/default/voice/voice-library?campaign=custom-voices-blog)中一站式浏览、试听和管理所有声音。

## [用例](#use-cases)

自定义声音解锁了一类全新的应用。

在线客服

I need help with my recent order.

Of course! Let me pull up your order details.

### 品牌语音智能体

为你的客服智能体赋予与品牌形象一致、可辨识的声音，而不是千篇一律的预设音色。

录制

00:42

In today's episode we dive deep into the future of AI and what it means for creators everywhere

### 内容创作者

用自己的声音大规模地为视频、播客和社交帖子配音，无需每次重新录制。

原声

保留

### 无障碍

为失去说话能力的人创建个性化声音，保留他们的声音身份。

🇺🇸

🇪🇸

🇫🇷

🇩🇪

🇨🇳

🇯🇵

🇺🇸English

🇪🇸Spanish

🇫🇷French

🇩🇪German

🇨🇳Chinese

🇯🇵Japanese

### 多语言团队

用每一种主流语言发表你的 CEO 主题演讲——英语、西班牙语、法语、德语、中文、日语等，皆自然流畅。

旁白The ancient door creaked open...

KiraWe need to move. Now.

ThaneI have a bad feeling about this.

### 游戏与娱乐

用独特的声音赋予角色生命，无需为每一句台词安排录音棚时间。

第 3 章

发现

She opened the notebook and found the handwriting unmistakably her own though she had no memory of writing it

4:1212:34

### 播客与有声书旁白

让你的叙事引人入胜。把脚本变成用你自己的声音逐章演绎的完整有声书，无需走进录音棚。

在线客服

I need help with my recent order.

Of course! Let me pull up your order details.

录制

00:42

In today's episode we dive deep into the future of AI and what it means for creators everywhere

原声

保留

🇺🇸

🇪🇸

🇫🇷

🇩🇪

🇨🇳

🇯🇵

🇺🇸English

🇪🇸Spanish

🇫🇷French

🇩🇪German

🇨🇳Chinese

🇯🇵Japanese

旁白The ancient door creaked open...

KiraWe need to move. Now.

ThaneI have a bad feeling about this.

第 3 章

发现

She opened the notebook and found the handwriting unmistakably her own though she had no memory of writing it

4:1212:34

### 品牌语音智能体

为你的客服智能体赋予与品牌形象一致、可辨识的声音，而不是千篇一律的预设音色。

## [自定义声音](#custom-voices)

**两分钟内克隆你的声音，随处可用。**

在 [xAI 控制台](https://console.x.ai/team/default/voice/voice-library?campaign=custom-voices-blog)录制约一分钟的自然语音。我们的流程会验证你是声音所有者，处理你的录音，并在两分钟内交付一个生产可用的声音模型。你的自定义声音继承全部 TTS 能力：[语音标签（speech tags）](https://docs.x.ai/developers/model-capabilities/audio/text-to-speech?campaign=custom-voices-blog)、多语言输出，以及 REST 与 WebSocket 双流式传输。

口令核验

录音

My voice is my key

第 1 步大声读出一句话口令以确认你的身份

自定义声音适用于我们内置声音可用的所有场合。把 `voice_id` 传给任何 [TTS 端点](https://docs.x.ai/developers/model-capabilities/audio/text-to-speech?campaign=custom-voices-blog)，或在 [语音智能体 API](https://docs.x.ai/developers/model-capabilities/audio/voice-agent?campaign=custom-voices-blog) 中使用它来构建实时对话智能体。

## [声音安全](#voice-safety)

每个自定义声音在创建前都要经过两阶段验证。首先，说话人朗读一句验证短语，我们的 STT 引擎实时转写并比对，确认意图与在场。然后我们分别从验证片段和完整录音计算说话人嵌入，确认二者属于同一个人。

你无法用既有录音克隆声音，也无法克隆别人的声音。

口令核验

录音

My voice is my key

### 口令核验

大声读出一句话口令。我们的 STT 引擎实时转写并比对，验证你的同意与在场。

说话人相似度

空闲

口令

–

录音

### 说话人相似度

比对来自口令和完整录音的说话人嵌入，确认它们属于同一个人。

## [声音库](#voice-library)

声音库是 [xAI 控制台](https://console.x.ai/team/default/voice/voice-library?campaign=custom-voices-blog)中的新板块，集中管理你的团队可用的所有声音，你的自定义创作与我们的内置声音并列一处。在单一页面上浏览、试听和管理声音。

我们已将内置声音目录扩展到覆盖 28 种语言的 80 余种声音。你可以在不同场景下试听任何声音，再为你的应用做出选择。

使用文本转语音或语音智能体 API 配合自定义声音无需额外费用。

🌐多语言🇸🇦Arabic🇧🇩Bengali🇪🇸Catalan🇨🇳Chinese🇩🇰Danish🇧🇪Dutch (BE)🇳🇱Dutch (NL)🇮🇪English (IE)🇬🇧English (UK)🇺🇸English (US)🇿🇦English (ZA)🇫🇮Finnish🇧🇪French (BE)🇩🇪German🇮🇳Hindi🇭🇺Hungarian🇮🇩Indonesian🇮🇹Italian🇰🇷Korean🇵🇱Polish🇵🇹Portuguese🇷🇺Russian🇪🇸Spanish🇸🇪Swedish🇹🇭Thai🇹🇷Turkish🇻🇳Vietnamese

Ara

female

Eve

female

Leo

male

Rex

male

Sal

male

[声音库](https://console.x.ai/team/default/voice/voice-library?campaign=custom-voices-blog)[自定义声音文档](https://docs.x.ai/developers/model-capabilities/audio/custom-voices?campaign=custom-voices-blog)[语音智能体 API](https://docs.x.ai/developers/model-capabilities/audio/voice-agent?campaign=custom-voices-blog)

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
