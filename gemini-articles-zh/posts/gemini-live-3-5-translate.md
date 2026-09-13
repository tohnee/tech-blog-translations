---
title: "Gemini 3.5 Live Translate 带来流畅自然的语音翻译"
title_en: "Fluid, natural voice translation with Gemini 3.5 Live Translate"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-live-3-5-translate/
site: gemini
date: 2026-06-09
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 3.5 Live Translate 带来流畅自然的语音翻译

> 原文：[Fluid, natural voice translation with Gemini 3.5 Live Translate](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-live-3-5-translate/) · Google

二十年前，[Google 的翻译](https://blog.google/products-and-platforms/products/translate/fun-facts-google-translate-20-years/)作为我们最早期的机器学习实验之一起步，目标是把语言的科学变成人与人连接的魔法。这项实验已经走过漫长的道路：如今每个月，我们的产品都在为全球数十亿用户翻译超过一万亿个词。

今天，我们迈出下一步，发布 Gemini 3.5 Live Translate——我们最新的实时语音到语音翻译音频模型。

该模型可自动检测 70 多种语言，生成流畅自然的翻译语音，保留说话者的语调、节奏和音高。与那些等说话者讲完再逐轮应答的系统不同，3.5 Live Translate 连续生成语音，在「等待更多上下文以提升质量」与「立即翻译以跟上说话者节奏」之间取得平衡。它输出的音频流畅自然、没有尴尬的停顿，并且在整场会话中只比说话者慢几秒。

Gemini 3.5 Live Translate 从今天起在 Google 各产品中开始推送：

- 开发者可通过 [Gemini Live API](https://ai.google.dev/gemini-api/docs/live-api/live-translate) 和 [Google AI Studio](https://aistudio.google.com/live?model=gemini-3.5-live-translate-preview) 以公开预览版使用
- 企业用户可从本月起在 [Google Meet](https://workspace.google.com/products/meet/) 中以私密预览版使用
- 所有人都可通过 [Android](https://play.google.com/store/apps/details?id=com.google.android.apps.translate&26hl=en) 和 [iOS](https://apps.apple.com/us/app/google-translate/id414706506) 上的 Google Translate 使用

## 用 3.5 Live Translate 进行构建

Gemini 3.5 Live Translate 在语音流式传输的同时进行处理，让跨语言连接更加无缝。该模型可以处理多语言输入，无需手动配置设置。与此同时，它的抗噪能力确保应用能够应对嘈杂、不可预测的环境。你可以利用这些能力，为多语言通话、会议、课程、直播等场景提供实时口译支持。

观看 Gemini Live API 的实际演示，实现配音和同步多语言翻译。欢迎深入探索 Gemini Cookbook 中的这个[演示](https://github.com/google-gemini/gemini-live-api-examples/tree/main/gemini-live-translate-livekit)和更多[示例代码](https://github.com/google-gemini/gemini-live-api-examples)。

借助 Gemini Live API，[Agora](https://docs.agora.io/en/conversational-ai/models/mllm/gemini)、[Fishjam](https://docs.fishjam.io/tutorials/gemini-live-integration)、[LiveKit](https://docs.livekit.io/agents/models/realtime/plugins/gemini/)、[Pipecat](https://docs.pipecat.ai/guides/features/gemini-live) 和 [Vision Agents](https://visionagents.ai/integrations/gemini) 等开发者平台让开发者能够轻松构建和部署语音翻译应用。这些集成处理了复杂的实时媒体流基础设施，开发者可以专注于用户体验。

我们的合作伙伴 Grab 正在测试该模型，让司机与乘客在接驾时实现近乎实时的多语言沟通。这些用户每个月通过 Grab 进行超过 1000 万次语音通话。

## 看看早期评价

除了 Grab 之外，CJ ENM、LiveKit 等公司也对 3.5 Live Translate 给出了积极反馈，称赞其出色的翻译质量、准确性和低延迟：

## 在视频会议中体验 3.5 Live Translate

Google Meet 中的[语音翻译](https://support.google.com/meet/answer/16221730?hl=en)即将采用 3.5 Live Translate，将通过以下方式改进体验：

- 提供 70 多种语言，而此前的上限只有 5 种语言；
- 支持在同一场会议中跨越 2000 多种语言组合进行交流，而此前只能在英语与其他语言之间互译；
- 更新界面，让语音翻译即点即用。

我们将于本月起面向选定的 Google Workspace 商业客户以私密预览版发布此更新，随后在今年晚些时候更广泛地推出。

## 在 Android 或 iOS 的 Google Translate 应用中获取 3.5 Live Translate

该模型也在全球范围的 Google Translate 应用中开始推送，覆盖 [Android](https://play.google.com/store/apps/details?id=com.google.android.apps.translate) 和 [iOS](https://apps.apple.com/us/app/google-translate/id414706506)。使用实时翻译（Live translate）功能时，只需连接任意一副耳机，即可体验更无缝的翻译，在 70 多种语言中还原说话者的语气。

针对 Android 用户，我们还将随 3.5 Live Translate 推出一项新的「聆听模式」，让你直接通过手机的听筒听到翻译。只需像平常打电话一样把手机贴在耳边，翻译音频就会直接流向你。当你想快速听到翻译又不想让旁人听到、而手边又没有耳机时，这个新体验会很有帮助。

使用新的聆听模式，用户可以直接通过手机听筒收听西班牙语导览的近乎实时的英语翻译。

## 经 SynthID 水印保护

我们模型生成的所有音频都带有 SynthID 水印。这种难以察觉的水印被直接编织进音频输出中，确保 AI 生成的内容仍可被检测，帮助防止虚假信息传播。关于我们安全与责任方案的详细信息，请查阅[模型卡](https://deepmind.google/models/model-cards/gemini-3-5-audio/)。
