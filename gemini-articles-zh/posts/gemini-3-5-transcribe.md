---
title: "Gemini 3.5 Transcribe 带来智能转录"
title_en: "Intelligent transcription with Gemini 3.5 Transcribe"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5-transcribe/
site: gemini
date: 2026-08-26
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 3.5 Transcribe 带来智能转录

> 原文：[Intelligent transcription with Gemini 3.5 Transcribe](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5-transcribe/) · Google

今天，我们推出 Gemini 3.5 Transcribe——迄今我们最精确的语音转文字模型，专为智能语音交互而设计。传统语音识别模型常常难以应对背景噪音、复杂行话和口语不流畅的清理，而 Gemini 3.5 Transcribe 能将原始音频直接转换为准确、润饰过且排版良好的文本。

在 Gemini 应用和 Android 等产品中，我们已经看到消费者通过 [Android 上的 Rambler](https://blog.google/products-and-platforms/platforms/android/gemini-intelligence/) 以及 macOS 版 Gemini 应用等新语音功能，从这款转录模型中获益。现在，开发者可以借助 [Google AI Studio 中的 Gemini API](https://aistudio.google.com/live?model=gemini-3.5-transcribe-live) 和 [Gemini Enterprise Agent Platform](https://console.cloud.google.com/agent-platform/studio/multimodal-live?model=gemini-3.5-transcribe-live-preview)，用 Gemini 3.5 Transcribe 构建类似的能力。

我们构建 3.5 Transcribe 的目标就是让它无缝接入你的开发工作流，无论你在构建语音智能体、实时字幕工具，还是通话后分析管道。该模型通过两个独立的 API 提供：

- **实时流式处理：**通过 [Live API](https://ai.google.dev/gemini-api/docs/live-api/live-transcribe) 使用 **`gemini-3.5-transcribe-live`**，以亚秒级延迟提供连续的双向流式传输，适合交互式语音应用。
- **预录音频处理：**通过 [Interactions API](https://ai.google.dev/gemini-api/docs/transcribe) 使用 **`gemini-3.5-transcribe`**，为录音、会议、通话记录等提供带说话人归属和词级时间戳的转录。

## 获得更精确、更智能的转录

Gemini 3.5 Transcribe 旨在捕捉你自然的说话风格，以更好地理解你的意图并识别自定义词汇，让你可以用语音执行任务。

- **智能转录：**无缝处理自我纠正（比如*“我们周二见——不，周三”*），去除填充词（“嗯”和“呃”），并自动排版文本。
- **函数调用：**模型可以通过函数调用把复杂任务（例如图像生成和文件分析）委派给其他 Gemini 模型。目前已在 [Gemini macOS 应用](https://blog.google/innovation-and-ai/products/gemini-app/speak-naturally-gemini-app-mac-os/)中可用。
- **更精确的转录：**按 Artificial Analysis 的测量，流式场景的平均词错误率（WER）为 4.0%，非流式场景为 2.6%。它在嘈杂的真实环境中表现出色，能准确捕捉邮政编码和订单号等字母数字实体。
- **自定义词汇：**通过无缝适配你提供的自定义词汇表，识别专业行话和特殊拼写。
- **全球语言支持：**自动检测并转录超过 85 种语言，从容应对各地口音和多样方言。
- **多说话人识别：**对预录音频准确归属说话人并附带时间戳，最多支持三位说话人（对 3 位以上说话人的支持为实验功能）。

Gemini 3.5 Transcribe 能应对实时的语言切换，并提供流畅的流式转录。

观看 Gemini 3.5 Transcribe 如何凭借智能转录能力清理口语中的不流畅之处。

3.5 Transcribe 提供带多说话人归属和词级时间戳的转录。

Gemini 3.5 Transcribe 的表现相比我们上一代转录模型 Chirp 3 是一次重大进步，带来了新能力、更低的词错误率和显著更好的延迟。按 Artificial Analysis 的测量，仅最终转录耗时一项就改善了 70%。在覆盖一批主流语言和地区的 FLEURS 基准上，该模型展现出精确的多语言表现，超越 Chirp 3，在流式模式下取得 5.50% 的 WER，在非流式场景中取得 5.04% 的 WER。

![流式语音识别准确度图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.5-audio-transcribe_fleur.width-100.format-webp.webp)

![流式语音识别准确度图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.5-audio-transcribe_fleur.width-100.format-webp_tK9W6V9.webp)

## 体验智能转录与高级听写

除了 Google AI Studio 和 Gemini Enterprise Agent Platform 中的 Gemini API 之外，3.5 Transcribe 还超越了标准语音转文字的范畴，让在 Google 各产品间的协作更加自然、直观。它把情境感知理解直接带入 Gboard、Antigravity、Gemini 应用和 Chrome 等日常界面，轻松捕捉语气细节、意图和行内编辑。

- 在 **Android 版 Gboard** 上，通过全新的 Rambler 功能，3.5 Transcribe 把口述的想法转化为格式良好的文本，并过滤掉填充词。你还可以用语音进行编辑、纠正拼写错误和改变写作风格。
- 在 **Google Antigravity** 上，经你授权后，3.5 Transcribe 会结合屏幕上下文和聊天历史，确保对文件名、智能体思路和活动文档的转录精确无误。
- 在 **Google AI Studio** 中，你可以在 Build 模式下使用 3.5 Transcribe，随口用语音即兴编写应用（vibe code）。
- 在 **macOS 版 Gemini 应用**中，3.5 Transcribe 不仅把你自然的口语转换为干净的格式化文本，还能启用可与屏幕上下文无缝配合的语音指令，驱动复杂工作流。通过在后台调用其他 Gemini 模型承担繁重工作，该模型让你只需动口就能总结本地文件、跨应用复用文本，或直接在光标处生成图像。
- 即将登陆 **Chrome**：你将可以在任何网页输入框中说话即打字——用你的声音更自然、更轻松地口述回复、起草帖子，或向 Chrome 中的 Gemini 下提示词。

Gemini 3.5 Transcribe 让你在 macOS 版 Gemini 应用中仅凭语音即可分析文件、生成图像和进行搜索。

看看 Gemini 3.5 Transcribe 如何在 Android 上借助 Rambler 自动去除填充词、清理口语表达。

Gemini 3.5 Transcribe 利用 Google Antigravity 的屏幕上下文确保转录的准确性。

## 看看早期的评价

借助 Gemini Live API，[Agora](https://docs.agora.io/en/ai/models/asr/gemini)、[Fishjam](https://docs.fishjam.io/tutorials/gemini-live-integration)、[LangChain](https://docs.langchain.com/langsmith/trace-gemini-live)、[LiveKit](https://docs.livekit.io/agents/models/stt/gemini/)、[Pipecat](https://docs.pipecat.ai/api-reference/server/services/stt/google)、[Vercel](https://vercel.com/docs/ai-gateway/modalities/speech-to-text) 和 [Vision Agents](https://visionagents.ai/integrations/stt/gemini) 等开发者平台让开发者能够轻松构建和部署高性能的语音驱动界面。这些平台在幕后管理复杂的实时媒体流基础设施，让开发者得以专注于打磨用户体验。

vivo、Intellitek Health 和 Lingopal 等公司也对 3.5 Transcribe 给予了积极反馈，重点提到了它出色的延迟、准确度和广泛的语言支持。

![vivo 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-5-transcribe__testimonia.width-100.format-webp.webp)

![IntelliTek 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-5-transcribe__testimonia.width-100.format-webp_dmRh7fs.webp)

![Lingopal 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-5-transcribe__testimonia.width-100.format-webp_5mPNtop.webp)

![Stream 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/stream_testimonial.width-100.format-webp.webp)

![Agora 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-5-transcribe__testimonia.width-100.format-webp_z2gdPBD.webp)

![fishjam 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-5-transcribe__testimonia.width-100.format-webp_WrvT9ED.webp)

### 立即开始使用 3.5 Transcribe

- **开发者**：已在 [Google AI Studio 的 Gemini API](https://aistudio.google.com/prompts/new_chat?model=gemini-3.5-transcribe) 和 [Google Antigravity](http://google.com/url?sa=j&url=https%3A%2F%2Fantigravity.google%2Fproduct%2Fantigravity-2&uct=1773758132&usg=eTZneyhE2yCXDuRpHPGTPF55jHQ.&opi=73833047&source=chat) 中进入公开预览。
- **企业**：已通过 [Gemini Enterprise Agent Platform](https://console.cloud.google.com/agent-platform/studio/multimodal-live?model=gemini-3.5-transcribe-live-preview) 进入公开预览，即将登陆 [Gemini Enterprise for Customer Experience](https://cloud.google.com/gemini-enterprise-cx)。
- **所有人**：macOS 版 Gemini 应用已支持英语；[Android 上的 Rambler](https://blog.google/products-and-platforms/platforms/android/gemini-intelligence/) 已在部分[国家和地区、语言](https://support.google.com/gboard/answer/17468539?hl=en#:~:text=Saturday%20to%20Sunday.%22-,Language%20support,-Rambler%20has%20been)推出；即将登陆 Chrome。
