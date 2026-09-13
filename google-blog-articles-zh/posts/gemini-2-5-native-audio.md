---
title: "Gemini 2.5 带来先进的音频对话与生成能力"
title_en: "Advanced audio dialog and generation with Gemini 2.5"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-2-5-native-audio/
site: google-blog
date: 2025-06-03
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 2.5 带来先进的音频对话与生成能力

> 原文：[Advanced audio dialog and generation with Gemini 2.5](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-2-5-native-audio/) · Google

Gemini 从底层设计上就是多模态的，能够原生地理解和生成文本、图像、音频、视频和代码。在 I/O 大会上，我们展示了 Gemini 2.5 如何凭借 AI 驱动的音频对话与生成新能力迈出重要一步。

我们已经在众多产品、原型和语言中运用这些模型，为全球用户带来音频体验。[NotebookLM 的 Audio Overviews（音频概览）](https://blog.google/technology/google-labs/notebooklm-audio-overviews-50-languages/)和 [Project Astra](https://deepmind.google/models/project-astra/) 只是其中的两个例子。下面深入了解一下 Gemini 2.5 的原生音频（native audio）能力能做些什么。

## 实时音频对话

人类的对话丰富而微妙，含义不仅由*说了什么*来传达，也由*怎么说*来传达——通过语气、口音，甚至笑声等非言语发声。我们相信，对话将成为我们与 AI 互动的关键方式。正因如此，Gemini 能够以音频形式原生地进行推理并生成语音，实现高效、实时的沟通。

Gemini 2.5 Flash 预览版的原生音频对话功能包括：

- **自然对话：** 高质量的语音交互、更具分寸感的表达力与韵律（节奏模式），并以极低延迟呈现，让你得以流畅交谈。
- **风格控制：** 借助自然语言提示词，你可以在对话过程中调整语音的表达方式，引导它采用特定口音、呈现多种语气与情感表达，甚至低声耳语。
- **工具集成：** Gemini 2.5 可以在对话中使用工具和函数调用。这使它能够整合来自 Google Search 等来源的实时信息，或使用开发者构建的自定义工具，让对话更加实用。
- **对话上下文感知（主动音频，proactive audio）：** 我们的系统经过训练，能够辨别并忽略背景语音、周围的对话和其他无关音频，只在适当时作出回应。从根本上说，它懂得何时*不该*说话。
- **音视频理解：** 凭借对流式音频和视频的原生支持，Gemini 2.5 可以就它在视频流或屏幕共享中看到的内容与你交谈。
- **多语言：** 可以用 24 种以上[受支持语言](https://ai.google.dev/gemini-api/docs/speech-generation#languages)中的任意一种进行对话，甚至可以在同一句话中轻松混用多种语言。
- **情感化对话：** Gemini 2.5 能感知用户的语气，明白同样的话以不同方式说出会带来截然不同的对话。
- **高级思考对话：** Gemini 的推理能力可以增强其对话表现，全面提升各项功能的表现。这带来更连贯、更智能的交互，尤其适用于复杂的推理任务。

## 可控文本转语音（TTS）

文本转语音技术正在快速演进，借助我们最新的模型，我们正在超越自然度，实现对生成音频前所未有的控制。现在，从简短片段到长篇叙事，你都可以生成任何内容，并精确指定风格、语调、情感表达和演绎方式——所有这些都可通过自然语言提示词来调控。

更多控制与能力包括：

- **动态演绎：** 这些模型能让文本鲜活起来，无论是诗歌、新闻播报还是引人入胜的故事讲述，都能进行富有表现力的朗读。它们还能按要求以特定情绪进行演绎，并呈现相应的口音。
- **更强的语速与发音控制：** 控制朗读速度，并确保发音更加准确，包括对特定词语的发音。
- **多说话人对话生成：** 该模型可以根据文本输入生成双人"[NotebookLM 风格](https://blog.google/technology/ai/notebooklm-audio-overviews/)"的音频概览，通过对话让内容更具吸引力。
- **多语言：** 借助 Gemini 2.5 轻松创建多语言音频内容，同样支持 24 种以上的[语言](https://ai.google.dev/gemini-api/docs/speech-generation#languages)。

对于可控语音生成（TTS），若要在复杂提示词下获得最先进的品质，可选择 Gemini 2.5 Pro Preview；若要面向高性价比的日常应用，可选择 Gemini 2.5 Flash Preview。这让开发者能够动态地为公告、故事、播客、视频游戏等创作音频。

## 安全与责任

在这些原生音频功能开发过程的每个阶段，我们都主动评估了潜在风险，并将所得经验用于制定缓解策略。我们通过严格的内部和外部安全评估来验证这些措施，包括为负责任部署而进行的全面[红队测试](https://blog.google/technology/safety-security/googles-ai-red-team-the-ethical-hackers-making-ai-safer/)。此外，我们模型的所有音频输出都嵌入了 [SynthID](https://deepmind.google/science/synthid)——我们的水印技术——通过让 AI 生成的音频可被识别来确保透明度。

## 面向开发者的原生音频能力

我们正在为 Gemini 2.5 模型带来原生音频输出，让开发者能够通过 [Google AI Studio](http://aistudio.google.com/) 或 [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio) 中的 Gemini API，构建更丰富、更具互动性的应用。

要开始探索，开发者可以在 Google AI Studio 的 [stream](https://aistudio.google.com/live) 标签页中试用 Gemini 2.5 Flash 预览版的原生音频对话。可控语音生成（TTS）现已在 Gemini 2.5 Pro 和 Flash 上以预览版形式提供，只需在 Google AI Studio 的 [generate media](http://aistudio.google.com/generate-speech) 标签页中选择语音生成即可。
