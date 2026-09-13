---
title: "Gemini 3.1 Flash TTS：下一代富有表现力的 AI 语音"
title_en: "Gemini 3.1 Flash TTS: the next generation of expressive AI speech"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-tts/
site: gemini
date: 2026-04-15
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 3.1 Flash TTS：下一代富有表现力的 AI 语音

> 原文：[Gemini 3.1 Flash TTS: the next generation of expressive AI speech](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-tts/) · Google

今天，我们推出 Gemini 3.1 Flash TTS，这是最新的文本转语音（TTS）模型，带来了更强的可控性、表现力和质量——助力开发者、企业和普通用户构建下一代 AI 语音应用。

从今天起，3.1 Flash TTS 将开始推送：

- 面向开发者：通过 Gemini API 和 [Google AI Studio](http://aistudio.google.com/generate-speech) 提供预览版
- 面向企业：通过 [Vertex AI](https://console.cloud.google.com/vertex-ai/studio/media/speech) 提供预览版
- 面向 Workspace 用户：通过 [Google Vids](https://docs.google.com/videos/create?usp=blog) 提供

## 更出色的语音质量与可控性

我们全面提升了 Gemini 3.1 Flash TTS 的整体语音质量，使其成为迄今为止最自然、最具表现力的模型。在 [Artificial Analysis TTS 排行榜](https://artificialanalysis.ai/text-to-speech/models)——一个汇集了数千条人类盲测偏好的基准测试——上，3.1 Flash TTS 取得了高达 1,211 的 Elo 分数。

![展示 Artificial Analysis 文本转语音竞技场质量 Elo 的 GIF 动图](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_flash_tts_evals_blog.gif)

Artificial Analysis 还将 Gemini 3.1 Flash TTS 置于其「最具吸引力象限」中，因为它在高质量语音生成与低成本之间实现了理想平衡。该模型还凭借原生多说话人对话、支持 70 多种语言，以及通过自然语言实现细粒度创意控制而更加出众。

## 全新音频标签，带来更具表现力的语音生成

3.1 Flash TTS 还引入了音频标签（audio tags）——一种直观的方式来控制语音风格、节奏和表达方式。通过将自然语言指令直接嵌入文本输入中，你可以以更高的精细度引导 AI 语音输出。

## 3.1 Flash TTS 支持多种音频标签，为同义词寻宝应用增添细腻而引人入胜的表达。

你可以在 Google AI Studio 中开始试用这些音频标签，以及其他开发者体验方面的更新——这些可配置的控制项让开发者坐上「导演的椅子」：

- **场景指导（Scene direction）：** 通过定义环境并提供具体的对话指令来搭建舞台。这种世界构建式的上下文有助于角色保持「入戏」，并在多轮对话中自然地彼此回应。
- **说话人级别的精确控制：** 使用独特的音频配置文件（Audio Profiles）来「选角」，然后指定导演备注（Director's Notes）来调整语速、语调和口音。借助[内联标签](https://ai.google.dev/gemini-api/docs/speech-generation#transcript-tags)，说话人可以在这些高层设置的基础上，在句子中途切换表达方式。
- **无缝导出：** 一旦表演臻于完美，这些精确的参数就可以导出为 Gemini API 代码，确保在各个项目和平台上保持一致、可辨识的音色。

借助这些新配置，开发者可以针对特定场景提升精确度，打造令人难忘的角色和沉浸式音频体验。

在 [Google AI Studio Playground](http://aistudio.google.com/generate-speech) 中开始体验高保真语音生成。

## 为全球规模而打造

Gemini 3.1 Flash TTS 可在 70 多种语言中提供高保真语音和更精准的控制。这些核心优化将先进的风格、节奏和口音控制带给主要市场——帮助开发者为全球范围的用户打造本地化的、富有表现力的语音体验。

早期的开发者和企业测试者已经感受到了 3.1 Flash TTS 的影响力，并强调了它令人惊叹的可控性与表现力。他们告诉我们，音频标签带来了全新水平的创意精度，能将简单的文本转化为高保真的声音表演。

![StyleUAI 的 Jay 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_1.width-100.format-webp.webp)

![AIM Intelligence 的 CTO 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_4.width-100.format-webp.webp)

![Artlist 的 Idan Yonas 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_5.width-100.format-webp.webp)

![Sierra 的 Lydia Xu 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_6.width-100.format-webp.webp)

![Invideo AI 的 Shivam Rastogi 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_7.width-100.format-webp.webp)

![biia 的 Fernanda Bejarano 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_8.width-100.format-webp.webp)

![HeyGen 的 John Wu 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_9.width-100.format-webp.webp)

![You learn.AI 的 Soami Kapadia 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_1.width-100.format-webp_N5HV1Wc.webp)

![Sylph.ai 的 Angel Wen 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_2.width-100.format-webp.webp)

![Mindlid 的 Artugrul Cavusoglu 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_tts_blog_quote_3.width-100.format-webp.webp)

## 使用 SynthID 添加水印

Gemini 3.1 Flash TTS 生成的所有音频都带有 SynthID 水印。这种不可感知的水印直接交织在音频输出中，能够可靠地检测 AI 生成的内容，帮助防止错误信息传播。欲了解我们在安全与责任方面的方法，你可以查阅[模型卡](https://deepmind.google/models/model-cards/gemini-3-1-flash-audio/)。
