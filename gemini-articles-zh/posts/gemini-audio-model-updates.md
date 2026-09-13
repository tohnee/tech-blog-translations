---
title: "升级的 Gemini 音频模型，带来更强大的语音交互"
title_en: "Improved Gemini audio models for powerful voice interactions"
source: https://blog.google/products-and-platforms/products/gemini/gemini-audio-model-updates/
site: gemini
date: 2025-12-12
crawled: 2026-09-13
translated: 2026-09-13
---

# 升级的 Gemini 音频模型，带来更强大的语音交互

> 原文：[Improved Gemini audio models for powerful voice interactions](https://blog.google/products-and-platforms/products/gemini/gemini-audio-model-updates/) · Google

本周早些时候，我们升级了 [Gemini 2.5 Pro 和 Flash 文本转语音模型](https://blog.google/technology/developers/gemini-2-5-text-to-speech)，为音频生成带来了更强的控制力。

但生成富有表现力的语音只是对话的一面。今天，我们发布了面向实时语音智能体的更新版 Gemini 2.5 Flash Native Audio。这次更新提升了模型处理复杂工作流、遵循用户指令以及进行自然对话的能力。

Gemini 2.5 Flash Native Audio 现已在 [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.5-flash-native-audio-preview-12-2025)、[Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/gemini-live-api-available-on-vertex-ai) 等 Google 产品中可用，并已开始在 [Gemini Live](https://gemini.google/overview/gemini-live/) 和 [Search Live](https://blog.google/products/search/live-audio-gemini-model-update/) 中推送，首次将原生音频的自然感带到 Search Live。这意味着你可以更高效地与 Gemini 进行实时头脑风暴，在 Search Live 中获得实时帮助，或者构建下一代可服务于企业的客服智能体。

除了为各类实用智能体提供动力之外，原生音频还为全球沟通解锁了新的可能。我们推出实时语音翻译（live speech translation）功能，可为耳机提供流式的语音到语音翻译，并保留说话者的语调、节奏和音高。这项测试版体验从今天开始将在 [Google Translate 应用](https://blog.google/products/search/gemini-capabilities-translation-upgrades/)中推送。

## 实时语音智能体

为了支持跨界面、跨产品的广泛用例，我们在三个关键方面改进了 Gemini 2.5 Native Audio：

- **更精准的函数调用：** 我们提高了模型触发外部函数时的可靠性。它现在能更准确地判断何时需要在对话中获取实时信息，并将这些数据无缝地编织回音频回复之中，而不打断对话流。在捕捉带多种约束的多步骤函数调用的评测 [ComplexFuncBench Audio](https://github.com/zai-org/ComplexFuncBench?tab=readme-ov-file#citatio) 上，Gemini 2.5 Native Audio 以 71.5% 的成绩位居第一。
- **更稳健的指令遵循：** 模型现在更善于处理复杂指令，内容完整性方面的用户满意度有所提升。它对开发者指令的遵循率达到 90%（此前为 84%），输出更加可靠。
- **更流畅的对话：** 我们在多轮对话质量上取得了显著提升。Gemini 2.5 Flash Native Audio 能够更有效地利用此前轮次的上下文，让对话更加连贯。

更新后的 Gemini 2.5 Flash Native Audio 与此前版本及业界竞品在 [ComplexFuncBench](https://github.com/zai-org/ComplexFuncBench?tab=readme-ov-file#citatio) 上的性能对比

![更新后的 Gemini 2.5 Flash Native Audio 与此前版本及业界竞品的性能对比](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini-audio_blog_light_blue_16x9_v1_25-12-12_1.gif)

### 客户怎么评价

[Google Cloud 的客户](https://cloud.google.com/blog/products/ai-machine-learning/gemini-live-api-available-on-vertex-ai)已经在使用 Gemini 的原生音频能力推动真实的业务成果，从按揭贷款处理到客户通话不一而足。

- *「用户在使用 Sidekick 的一分钟内常常就忘记了自己是在和 AI 通话，有些人在长时间聊天后甚至向机器人道谢……通过 Gemini [2.5 Flash Native Audio] 提供的全新 Live API AI 能力，我们的商家能够赢得竞争。」* —— Shopify 产品副总裁 David Wurtz
- *「通过集成 Gemini 2.5 Flash Native Audio 模型……自 2025 年 5 月上线以来，我们显著增强了 Mia 的能力。这一强大组合帮助我们为经纪人合作伙伴生成了超过 14,000 笔贷款。」* —— United Wholesale Mortgage（UWM）首席技术官 Jason Bressler
- *「通过 Vertex AI 使用 Gemini 2.5 Flash Native Audio 模型，让 Newo.ai 的 AI 前台接待员实现了无与伦比的对话智能……它们即使在嘈杂环境中也能识别主说话人，可以在对话中途切换语言，并且听起来非常自然、富有情感表现力。」* —— Newo.ai 联合创始人 David Yang

## 实时语音翻译

Gemini 现已原生支持全新的实时语音到语音翻译能力，可同时应对持续收听和双向对话两种场景。

在持续收听模式下，Gemini 会自动把多种语言的语音翻译成单一目标语言。这样你只需戴上耳机，就能用母语听到你身边的世界。

在双向对话模式下，Gemini 的实时语音翻译可以在两种语言之间实时互译，并根据说话者自动切换输出语言。例如，你说英语，想和一位说印地语的人交谈，你会在耳机里实时听到英语翻译，而当你说完之后，手机会播报印地语。

Gemini 的实时语音翻译具备多项在真实场景中非常有用的关键能力：

- **语言覆盖**：结合 Gemini 模型的世界知识与多语言能力以及其原生音频能力，可翻译超过 70 种语言、2000 个语言对的语音
- **风格迁移**：捕捉人类语音的细微之处，保留说话者的语调、节奏和音高，使译文听起来自然。
- **多语言输入**：在同一次会话中同时理解多种语言，无需反复调语言设置就能听懂多语言对话。
- **自动检测**：识别所讲的语言并自动开始翻译，因此你甚至不需要知道对方说的是什么语言。
- **抗噪能力**：过滤环境噪音，让你即使在嘈杂的户外环境中也能从容交谈。

从今天起，你可以在 Google Translate 应用的一项全新测试版体验中试用该功能：把耳机连接到设备并点按「Live translate」，即可[在耳机中获得实时翻译](https://blog.google/products/search/gemini-capabilities-translation-upgrades/)。该体验正向美国、墨西哥和印度的所有 Android 设备推送，对 iOS 及更多地区的支持即将推出。

我们会根据反馈持续迭代这一体验，并在 2026 年把它带到包括 Gemini API 在内的更多 Google 产品上。

## 今天就开始

现在就用 Gemini 2.5 Flash Native Audio 开始构建语音智能体吧，它已在 [Vertex AI](https://cloud.google.com/blog/products/ai-machine-learning/gemini-live-api-available-on-vertex-ai) 上正式发布（GA），并在 [Gemini API](https://ai.google.dev/gemini-api/docs/live) 中以预览版提供。你也可以在 [Google AI Studio](https://ai.dev/prompts/new_chat?model=gemini-2.5-flash-native-audio-preview-12-2025) 中试用。

Gemini 2.5 Flash 与 2.5 Pro 文本转语音模型同样可通过 Google AI Studio 中的 Gemini API 使用。欢迎从[语音生成文档](https://ai.google.dev/gemini-api/docs/speech-generation)入手，浏览[提示词指南](https://ai.google.dev/gemini-api/docs/speech-generation#prompting-guide)，或查看 [Gemini API Cookbook](https://github.com/google-gemini/cookbook/blob/main/quickstarts/Get_started_TTS.ipynb) 快速上手。
