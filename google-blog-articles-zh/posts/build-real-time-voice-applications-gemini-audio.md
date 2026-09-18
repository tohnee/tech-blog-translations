---
title: "使用 Gemini 3.8 Live 和 3.5 Transcribe 构建实时语音应用"
title_en: "Build real-time voice applications with Gemini 3.8 Live and 3.5 Transcribe"
source: https://blog.google/innovation-and-ai/technology/developers-tools/build-real-time-voice-applications-gemini-audio/
site: google-blog
date: 2026-09-15
crawled: 2026-09-18
translated: 2026-09-18
---

# 使用 Gemini 3.8 Live 和 3.5 Transcribe 构建实时语音应用

> 原文：[Build real-time voice applications with Gemini 3.8 Live and 3.5 Transcribe](https://blog.google/innovation-and-ai/technology/developers-tools/build-real-time-voice-applications-gemini-audio/) · Google

今天，我们在 [Gemini API](https://ai.google.dev/gemini-api/docs/live) 和 [Google AI Studio](http://ai.studio/live) 中[发布](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/)了新的 Gemini Live 模型，进一步扩展了我们用于构建实时、语音优先（voice-first）产品体验的开发者套件：

[**Gemini 3.8 Live**](https://aistudio.google.com/live?model=gemini-3.8-live) 和 [**3.8 Live Extended Thinking**](https://aistudio.google.com/live?model=gemini-3.8-live-extended-thinking)**：**Gemini 3.8 Live 为我们的原生语音转语音（speech-to-speech）模型带来了阶跃式提升，能够在保持对话的同时执行任务。面对复杂请求，3.8 Live Extended Thinking 可提供更深层的推理，在 Artificial Analysis 的 Speech-to-Speech 排行榜上排名第一。

[**Gemini 3.5 Transcribe**](https://aistudio.google.com/live?model=gemini-3.5-transcribe-live)：我们的专用语音转文本模型，可在 85+ 种语言中实现高度精确的转写。该模型于上个月发布，平均词错误率（Word Error Rate，WER）为 4.0%（流式）和 2.6%（非流式）。

## Gemini 3.8 Live 和 3.8 Live Extended Thinking：构建更智能的对话式智能体

我们的新模型 [Gemini 3.8 Live](https://aistudio.google.com/live?model=gemini-3.8-live) 和 [3.8 Live Extended Thinking](https://aistudio.google.com/live?model=gemini-3.8-live-extended-thinking) 让开发者能够构建在保持对话流畅的同时进行推理并执行任务的语音智能体。主要能力包括：

- **异步函数调用：** 在后台执行 API 和工具调用，同时继续向用户流式传输音频响应
- **视觉上下文：** 将对话锚定（grounding）于实时视觉输入，助力打造既能理解用户所说内容、*又*能看清眼前事物的智能体
- **字母数字精度：** 精确解析确认码、理赔编号和技术数据
- **多语言支持：** 覆盖 97+ 种语言并保持口音一致，触达全球受众
- **增量内容更新：** 将实时音频与结构化数据无缝合并，返回具备上下文感知能力的响应

3.8 Live Extended Thinking 还支持[可配置思考](https://ai.google.dev/gemini-api/docs/live-api/thinking)（configurable thinking），可在后台处理复杂的多步推理，同时在主对话中回应或播报自己的进度。这些模型相较于我们之前的 Live 模型实现了阶跃式跨越，也是级联架构（cascaded architectures）之外一种更精简的替代方案。

![Ambr AI 联合创始人兼技术与产品主管 Jamie Wood 表示："Ambr AI 通过逼真的 AI 模拟，训练企业团队学习谈判、领导和化解棘手的客户对话。切换到 Gemini 3.8 Live Extended Thinking 后，我们的模拟变得更快、更具表现力，也更擅长处理复杂对话。它还让我们能够通过单一集成以 70 多种语言交付培训，帮助客户在全球员工队伍中培养这些技能。"](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-liveapi-ambrai_1.width-1200.format-webp.webp)

Gemini 3.8 Live 和 Gemini 3.8 Live Extended Thinking 已通过 [Live API](https://ai.google.dev/gemini-api/docs/live) 提供。其[定价](http://ai.google.dev/gemini-api/docs/pricing#gemini-3.8-live)颇具竞争力：音频输入为 $0.005/分钟，音频输出为 $0.018/分钟
[1](#footnote-1)
，让开发者能够以业界领先的性能扩展语音应用。

![Artificial Analysis Speech-to-Speech 指数基准测试](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-audio__evals__S2S-inde.width-100.format-webp_VVJ0h6W.webp)

![智能体性能基准测试](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-audio__evals__agentic-.width-100.format-webp_y7iUxFh.webp)

![Tau-bench 排行榜基准测试](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-audio__evals__t3-banki.width-100.format-webp_PNTg1az.webp)

![Artificial Analysis 音频总成本](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-audio__evals__big-benc.width-100.format-webp_3GHiXLF.webp)

开发者还可以通过 [Agora](https://docs.agora.io/en/ai/models/mllm/gemini)、[Fishjam](https://docs.fishjam.io/tutorials/gemini-live-integration)、[LiveKit](https://docs.livekit.io/agents/models/realtime/plugins/gemini/)、[LangChain](https://docs.langchain.com/langsmith/trace-gemini-live)、[Pipecat](https://docs.pipecat.ai/pipecat/features/gemini-live)、[Vercel](https://vercel.com/docs/ai-gateway/modalities/realtime) 和 [Vision Agents](https://visionagents.ai/integrations/realtime/gemini) 使用这些模型——它们是我们的 Live API 集成合作伙伴，负责处理面向实际部署的媒体流式传输基础设施：

![Live API 合作伙伴包括 Pipecat、LiveKit、LangChain、Agora、Fishjam、Voximplant、Vercel 和 VisionAgents。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-live-api-partners-launch-.width-1200.format-webp.webp)

## Gemini 3.5 Transcribe：将流式语音转换为文本

实时语音理解对语音优先的界面至关重要。上个月，我们发布了 Gemini 3.5 Transcribe，提供低延迟、高精度的转写，实现了 4.0% 的 WER，并具备以下实用特性：

- **自动语码转换（code-switching）：** 无需手动配置，即可处理句内和句间的语码及语言切换
- **自定义词汇偏置（vocabulary biasing）：** 通过传入最多包含 1,000 个词项的 custom\_vocabulary 列表，将语音识别引导至领域专属术语、生僻行话、公司名称和专有名词
- **智能转写模式**：通过结构化排版、自我纠正以及可去除填充词（filler words）的不流利剔除，交付润色完毕、可直接阅读的转写文本

3.5 Transcribe 支持 85+ 种语言，为语音体验以及亚秒级字幕生成、呼叫中心智能体、实时音频分析等无状态任务提供了强大的聆听引擎。你还可以通过 Interactions API 使用该模型，转写最长 1 小时的音频文件，并获得结构化时间戳和说话人标注。欢迎阅读我们的[开发者指南](https://aistudio.google.com/learn/gemini-3-5-transcribe-developer-guide)了解更多。

## 面向开发者的完整音频套件

上手时，你可以在 [ai.studio/live](https://ai.studio/live) 中试用这些模型，从 [GitHub](https://github.com/google-gemini/gemini-live-api-examples) 克隆示例应用，或者为你的智能体配备我们的 [Live API 技能](https://ai.google.dev/gemini-api/docs/coding-agents#gemini-live-api-dev)。

你还可以使用我们的语音和音乐生成模型来创建音频体验，它们全部可在 Gemini API 中使用：

- [**Gemini 3.5 Live Translate**](https://ai.google.dev/gemini-api/docs/live-api/live-translate)：支持 70 多种语言的语音转语音翻译
- [**Gemini 3.1 Flash TTS**](https://ai.google.dev/gemini-api/docs/speech-generation)：高度可配置的语音生成（更多更新即将推出）
- [**Lyria 3.5**](https://ai.google.dev/gemini-api/docs/music-generation)：生产级音乐生成

麦克风已交到你手中，我们迫不及待想听到你构建的成果！
