---
title: "推出 Grok Voice Transcribe 2.0"
title_en: "Introducing Grok Voice Transcribe 2.0"
date: 2026-09-18
source: https://x.ai/news/grok-voice-transcribe-2
crawled: 2026-09-22
translated: 2026-09-22
---

# 推出 Grok Voice Transcribe 2.0

> 原文：[Introducing Grok Voice Transcribe 2.0](https://x.ai/news/grok-voice-transcribe-2) · xAI

[返回新闻列表](/news)

2026 年 9 月 18 日

发布 SpaceXAI 最新的语音转文字模型，具备无与伦比的准确性与成本效益。

[在线试用](https://console.x.ai/team/default/voice/speech-to-text?campaign=voice-transcribe-2-blog&utm_source=website&utm_medium=referral&utm_campaign=voice-transcribe-2-blog)[查看文档](https://docs.x.ai/developers/model-capabilities/audio/speech-to-text?campaign=voice-transcribe-2-blog)

今天我们发布 Grok Voice Transcribe 2.0——我们最新的语音转文字模型。在我们的一系列真实世界评测中，Grok Voice Transcribe 2.0 是当今最准确的转录模型之一，准确率是 Grok Voice Transcribe 1.0 的两倍，而价格不变。

Grok Voice Transcribe 2.0 构建在 Grok Voice 背后的音频基础模型之上。Grok Voice 目前每天支撑数万通客户支持电话，转录数百万小时的视频旁白，并在实体产品中运行语音智能体——包括 Tesla 车辆中的 Grok 助手。它的训练数据是一份独特的实况、嘈杂、多语言音频集，录制自多种多样的环境，并经过后训练（post-training）精心打磨。

其成果是当今在真实场景下最准确的转录模型之一。

## [准确性](#accuracy)

大多数转录模型在干净的单说话人音频上表现不错。真实世界的音频则难得多：时断时续的电话线路、多个交叠的人声、地方口音，以及口述的电话号码或电子邮件地址。我们为各种条件和环境下最困难的音频打造了 Grok Voice Transcribe 2.0。

在公开的 Artificial Analysis 排行榜上，Grok Voice Transcribe 2.0 在 32 个流式模型中准确率排名第一。

### 准确率 vs 价格

越靠右上越好。

StreamingBatch

2%3%4%5%6%7%8%$0$3$6$9$12$15$18Word Error Rate (%) • Better →Price ($ / 1,000 min) • Better →Grok Voice Transcribe 2.0Grok Voice Transcribe 1.0Muse Voice TranscribeScribe v2 RealtimeGPT Live TranscribeGemini 3.5 Transcribe LiveUniversal-3.5 Realtime ProChirp 3 StreamingAzure STT Real-timeNova-3 RealtimeFlux

数据来源：[Artificial Analysis](https://artificialanalysis.ai/speech-to-text/streaming)

### [内部评测](#internal-evaluations)

除公开基准外，我们还在四个取自生产流量的内部数据集上测量词错误率：客户支持通话的电话音频、与 Grok 的对话、口述凭据（如账号和电子邮件地址），以及多语言短语音指令。Grok Voice Transcribe 2.0 在全部四项上都优于 Grok Voice Transcribe 1.0，而在电话音频上领先我们测试过的所有模型。

### 电话音频（8 kHz）

Customer support calls · English

### 对话

Conversations with Grok · English

### 凭据

Phone numbers, emails, addresses · English

### 短语

Voice-assistant utterances · 19 languages

## [多语言](#multilingual)

Grok Voice Transcribe 2.0 可转录数十种语言，自动检测语言，并在一次处理中跟上录音中途的语言切换。多语言准确性是它相对 Grok Voice Transcribe 1.0 最大的改进。

### 转录准确率

Word Error Rate (%)。越低越好。

Grok Voice Transcribe 2.0

Grok Voice Transcribe 1.0

ElevenLabs Scribe v2

Deepgram Nova-3

车载指令之类的短语给模型识别语言留下的上下文很少。在我们的短语句集上，词错误率从 20.6% 降到了 6.8%。

## [功能](#features)

Grok Voice Transcribe 2.0 支持高级配置与控制。现有的 Speech-to-Text API 集成无需改动任何代码即可获得准确性提升：

- **批量与流式。** 转录已录制的文件和 URL，或实时转录音频流。
- **词级时间戳。** 每个词都有精确的起止时间和置信度分数。
- **说话人分离。** 在转录文本中标注每一位说话人，无需额外费用。
- **多声道转录。** 最多可独立转录 8 个声道。
- **关键词加权（key term biasing）。** 每次请求最多传入 100 个领域术语，如产品名称或医学词汇。
- **文本格式化。** 数字、日期、货币、电话号码和电子邮件地址以书面形式返回。
- **填充词移除。** 从转录文本中省略「嗯」「呃」等填充词。
- **智能断句检测。** 为语音智能体检测说话人一轮发言的结束。

## [Grok Voice 为 Atlassian Loom 提供支持](#grok-voice-powers-atlassian-loom)

[Atlassian Loom](https://www.loom.com/) 被广泛用于录制和分享屏幕录像。Atlassian 发现 Grok Voice Transcribe 2.0 比其现有方案更准确，现在用它转录每一条视频。准确的转录开启了新的 AI 工作流：在 Loom 里录下行动计划，把转录文本送入 Cursor，它就能直接完成代码修改。

> 「我们一直相信，推进工作最好的方式是把上下文捕获一次，然后让它流向四面八方。Grok 驱动 Loom 的语音转文字，Cursor 再把它变成代码——我们正在打通从上下文到代码的闭环：录下你的想法，工作就此完成。这是 AI 辅助开发走向未来的一个缩影。」

Sanchan Saxena，Atlassian Teamwork Collection 高级副总裁

## [价格](#price)

Grok Voice Transcribe 2.0 的定价与 Grok Voice Transcribe 1.0 完全相同。批量转录仍为每音频小时 $0.10，流式为每音频小时 $0.20，说话人分离、时间戳和关键词均已包含在内。

### 批量

每音频小时美元

### 流式

每音频小时美元

Grok Voice Transcribe 2.0 很快将成为 Speech-to-Text API 的默认模型，Grok Voice Transcribe 1.0 将在未来几周内弃用。若想在过渡期间继续使用 1.0，请固定使用 `grok-voice-transcribe-1.0`。

## 开始使用 Grok Voice Transcribe 构建

[在线试用](https://console.x.ai/team/default/voice/speech-to-text?campaign=voice-transcribe-2-blog&utm_source=website&utm_medium=referral&utm_campaign=voice-transcribe-2-blog)[查看文档](https://docs.x.ai/developers/model-capabilities/audio/speech-to-text?campaign=voice-transcribe-2-blog)
