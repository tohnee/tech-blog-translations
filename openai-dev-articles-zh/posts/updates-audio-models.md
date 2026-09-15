---
title: "面向语音开发者的更新"
title_en: "Updates for developers building with voice"
source: https://developers.openai.com/blog/updates-audio-models/
crawled: 2026-09-14
translated: 2026-09-14
---

# 面向语音开发者的更新

> 原文：[Updates for developers building with voice](https://developers.openai.com/blog/updates-audio-models/) · OpenAI 开发者博客

AI 音频能力解锁了一个激动人心的用户体验新前沿。今年早些时候，我们发布了多款新的音频模型，包括 [`gpt-realtime`](https://platform.openai.com/docs/models/gpt-realtime)，以及[新的 API 功能](https://developers.openai.com/blog/realtime-api)，让开发者能够构建这些体验。

上周，我们发布了一批新的音频模型快照（snapshot），旨在通过提升生产级语音工作流——从转写（transcription）、文本转语音（text-to-speech）到实时、原生语音对语音（speech-to-speech）智能体——的可靠性与质量，来解决构建可靠音频智能体时的一些常见挑战。

这些更新包括：

- [`gpt-4o-mini-transcribe-2025-12-15`](https://platform.openai.com/docs/models/gpt-4o-mini-transcribe)：配合[转写（Transcription）](https://platform.openai.com/docs/guides/speech-to-text)或 [Realtime API](https://platform.openai.com/docs/guides/realtime-transcription) 用于语音转文本（speech-to-text）
- [`gpt-4o-mini-tts-2025-12-15`](https://platform.openai.com/docs/models/gpt-4o-mini-tts)：配合 [Speech API](https://platform.openai.com/docs/guides/text-to-speech) 用于文本转语音（text-to-speech）
- [`gpt-realtime-mini-2025-12-15`](https://platform.openai.com/docs/models/gpt-realtime-mini)：配合 [Realtime API](https://platform.openai.com/docs/guides/realtime) 用于原生、实时的语音对语音
- [`gpt-audio-mini-2025-12-15`](https://platform.openai.com/docs/models/gpt-audio-mini)：配合 [Chat Completions API](https://platform.openai.com/docs/api-reference/chat/create) 用于原生语音对语音

新快照带来了一些共同的改进：

**音频输入方面：**

- **更低的词错率（word-error rate）**：面向真实世界与嘈杂环境的音频
- **更少的幻觉**：在静音期间或存在背景噪音时

**音频输出方面：**

- **更自然、更稳定的语音输出**，包括使用 Custom Voices（定制音色）时

[定价](https://platform.openai.com/docs/pricing#audio-tokens)与之前的模型快照保持一致，因此我们建议切换到这些新快照，以同样的价格获得改进的性能。

如果你正在构建语音智能体、客户支持系统或品牌语音体验，这些更新将帮助你让生产部署更可靠。下面，我们将拆解这些新变化，以及这些改进如何体现在真实的语音工作流中。

## 语音对语音（Speech-to-speech）

我们正在部署新的 Realtime mini 与 Audio mini 模型，它们针对更好的工具调用与指令遵循做了优化。这些模型缩小了 mini 与全尺寸模型之间的智能差距，让一些应用可以通过迁移到 mini 模型来优化成本。

### `gpt-realtime-mini-2025-12-15`

`gpt-realtime-mini` 模型专为配合 [Realtime API](https://platform.openai.com/docs/guides/realtime) 使用——这是我们的低延迟、原生多模态交互 API。它支持音频流式输入输出、处理打断（可选语音活动检测），以及在模型持续说话的同时在后台进行函数调用等特性。

新的 Realtime mini 快照更适合实时智能体，在指令遵循与工具调用上有明显提升。在我们的内部语音对语音评测中，与上一个快照相比，指令遵循准确率提升了 18.6 个百分点，工具调用准确率提升了 12.9 个百分点，并且在 Big Bench Audio 基准测试上也有改进。

这些收益合在一起，让实时的低延迟场景中的多步交互更可靠、函数执行更一致。

对于智能体准确率值得付出更高成本的场景，`gpt-realtime` 仍然是我们表现最好的模型。但当成本与延迟最为关键时，`gpt-realtime-mini` 是一个绝佳选择，在真实场景中表现出色。

例如，[Genspark](https://www.genspark.ai/) 在双语翻译与智能意图路由上对它做了压力测试，除了语音质量的提升之外，他们发现延迟近乎即时，并且在快速来回对话中意图识别始终保持精准。

### `gpt-audio-mini-2025-12-15`

`gpt-audio-mini` 模型可以配合 [Chat Completions API](https://platform.openai.com/docs/api-reference/chat/create) 用于不要求实时交互的语音对语音用例。

两个新快照还配备了升级的解码器（decoder），让语音听起来更自然，并在使用 Custom Voices 时更好地保持音色一致性。

## 文本转语音（Text-to-speech）

我们最新的文本转语音模型 `gpt-4o-mini-tts-2025-12-15` 在准确率上实现了显著跃升，与上一代相比，在各标准语音基准上的词错率（WER）大幅降低。在 Common Voice 与 FLEURS 上，我们观察到 WER 大约降低 35%，在 Multilingual LibriSpeech 上也有持续的提升。

这些结果共同反映出，模型在广泛的语言范围内发音更准确、更稳健。

与新的 `gpt-realtime-mini` 快照类似，这个模型听起来自然得多，并且在与 Custom Voices 搭配时表现更好。

## 语音转文本（Speech-to-text）

最新的转写模型 `gpt-4o-mini-transcribe-2025-12-15` 在准确率与可靠性上都展现出强劲提升。在 Common Voice 与 FLEURS（不带语言提示）等标准 ASR 基准上，它的词错率低于以前的模型。我们针对真实对话场景中的行为对它做了优化，例如简短的用户话语与嘈杂的背景。在一项内部的*噪声致幻*（hallucination-with-noise）评测中——我们播放真实世界的背景噪音片段以及说话间隔各异（包括静音）的音频——与 Whisper v2 相比，该模型产生的幻觉减少了约 90%，与以前的 GPT-4o-transcribe 模型相比减少了约 70%。

这个模型快照在中文（普通话）、印地语、孟加拉语、日语、印尼语与意大利语上尤其出色。

## Custom Voices（定制音色）

Custom Voices 让组织能够用自己独特的品牌声音与客户沟通。无论你在构建客户支持智能体还是品牌形象化身（avatar），OpenAI 的定制语音技术都能让你轻松创建独特、逼真的声音。

这些新的语音对语音与文本转语音模型为定制音色带来了改进：更自然的音调、对原始样本更高的还原度，以及跨方言的更高准确率。

为确保这项技术的安全使用，Custom Voices 仅面向符合条件的客户开放。请联系你的客户经理或[联系我们的销售团队](https://openai.com/contact-sales/)了解更多。

## 从原型到生产

语音应用往往在同样的地方出问题：主要是长时间对话，或静音这类边界情况，以及语音智能体必须精准的工具驱动流程。这些更新正是聚焦于这些失败模式——更低的错误率、更少的幻觉、更一致的工具使用、更好的指令遵循。另外还有一份附赠福利：我们改进了输出音频的稳定性，让你的语音体验听起来更自然。

如果你今天就在发布语音体验，我们建议迁移到新的 `2025-12-15` 快照，并重新运行你的关键生产测试用例。
早期测试者已确认，无需更改指令、只需切换到新快照就能看到明显改进，但我们仍建议针对你自己的用例进行实验，并按需调整提示词。
