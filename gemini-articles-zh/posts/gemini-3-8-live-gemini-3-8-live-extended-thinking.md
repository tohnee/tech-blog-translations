---
title: "Gemini 3.8 Live 与 3.8 Live Extended Thinking 现已发布"
title_en: "Introducing Gemini 3.8 Live and 3.8 Live Extended Thinking"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/
site: gemini
date: 2026-09-15
crawled: 2026-09-18
translated: 2026-09-18
---

# Gemini 3.8 Live 与 3.8 Live Extended Thinking 现已发布

> 原文：[Introducing Gemini 3.8 Live and 3.8 Live Extended Thinking](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-gemini-3-8-live-extended-thinking/) · Google

*2026 年 9 月 17 日更新*

今天，我们推出两款新模型，它们在近实时推理方面带来了进步，能够更有效地支撑语音智能体，并让与 AI 对话的体验更加直觉、更加智能。

- **Gemini 3.8 Live**：为规模化与成本效率而生，将对话智能与流畅对话和视觉锚定（visual grounding）相结合。
- **Gemini 3.8 Live Extended Thinking**：为高复杂度任务而生，具备更强的智能与多步推理能力。

对于开发者和企业来说，这些模型提供了构建可靠、可用于生产环境的语音智能体的基础组件。它们也让用户在 Gemini 应用、Google Workspace 和 Search 中与 Gemini 语音交流更加流畅、更富协作性——帮助你仅凭语音就能处理复杂任务。

## 体验更流畅、更智能的对话

Gemini 3.8 Live Extended Thinking 提供企业级的任务完成能力和智能水平，在 Artificial Analysis 的语音到语音质量指数（Speech to Speech Quality Index）中以 82.6 分位居总榜第一，并在智能体任务完成方面领先：在 *τ*-Voice 上取得 68.6%，在 Sierra 的 *τ*-Voice-banking 基准测试上取得 35.1%。它还具备强大的推理能力，在 Big Bench Audio 上取得 97.7% 的得分，同时与其他前沿模型相比保持着极具竞争力的价格。

Gemini 3.8 Live 在用户中获得了很高的偏好度，在[语音智能体竞技场（Speech Agent Arena）](https://artificialanalysis.ai/speech-to-speech?api-benchmarks=agentic-performance-vs-cost-to-run#speech-to-speech-arena-results-tabs)中位列第二。除这一表现外，它仍保持着极高的成本效益——为开发者和企业提供了一个为规模化而生、能力强且高效的模型。

![展示 Artificial Analysis 语音到语音指数的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-audio__evals__S2S-inde.width-100.format-webp_VVJ0h6W.webp)

![展示 Artificial Analysis 智能体表现的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-audio__evals__agentic-.width-100.format-webp_y7iUxFh.webp)

![展示 Sierra 基准测试的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-audio__evals__t3-banki.width-100.format-webp_PNTg1az.webp)

![展示 Artificial Analysis 每小时输入音频成本的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-audio__evals__big-benc.width-100.format-webp_3GHiXLF.webp)

在 ServiceNow 的 [EVA-Bench](https://servicenow.github.io/eva/#results)（一个用于评估语音智能体的基准测试）上，我们的模型通过成功平衡准确性与对话质量，推动了复杂工作流的 Pareto 前沿（Pareto Frontier）。

注：该测试是在 Gemini Enterprise Agent Platform 的 Live API 上运行的。

![展示 EVA-Bench 体验与任务完成度关系的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-audio__benchmarks__eva-be.width-1200.format-webp_W6vjSFt.webp)

Gemini 3.8 Live 以近实时的方式处理视觉输入，为对话注入上下文，从而给出更有帮助的回应。它可以在对话中途自动检测并在 97 种受支持语言之间切换。它还能在继续对话的同时于后台执行工具和 API 调用，因此模型可以先确认请求、继续交谈，而任务在后台同步完成。

*Gemini 3.8 Live 实时指导员工入职，利用视觉上下文即时解答现场提问。*

*观看 Gemini 3.8 Live 借助视觉上下文、推理和自然的对话流，以近实时方式下国际象棋。*

对于需要更深层次推理的任务，3.8 Live Extended Thinking 可以边推理边说话。它在为复杂工作流提供更强智能的同时保持不间断的对话流——通过*「让我查一下……」*这样的早期口头提示自然地确认请求，并以实时进度播报让用户随时了解多步后台任务的进展。

*观看 Gemini 3.8 Live Extended Thinking 将原始草图和近实时的语音反馈转化为可用的 React 组件。*

*见证 Gemini 3.8 Live Extended Thinking 协调多步骤预订与异步函数调用——全程不打断自然的实时对话。*

*观看 Gemini 3.8 Live 通过自然语音即时构建完整的商业计划和定制营销工具包。*

在 Google Workspace、Search 和 Gemini 应用中，我们的 Live 模型带来了更直觉化、更协作的体验——尤其是在处理你最复杂的任务时。

*在 Google Workspace 中通过 Docs Live、Gmail Live 和 Keep Live 体验 Gemini 3.8 Live Extended Thinking。*

*在 Search Live 中直接获得由 Gemini 3.8 Live 驱动的分步实时故障排查帮助。*

*在 Gemini 应用中使用 Gemini 3.8 Live Extended Thinking 管理你的一天——索取每日简报（Daily Brief）、边聊边清空收件箱，或者把待办事项交托出去。*

## 赋能开发者与企业语音生态

借助 [Gemini Live API](https://ai.google.dev/gemini-api/docs/live-api)，[Agora](https://docs.agora.io/en/ai/models/mllm/gemini)、[Fishjam](https://docs.fishjam.io/tutorials/gemini-live-integration)、[LangChain](https://docs.langchain.com/langsmith/trace-gemini-live)、[LiveKit](https://docs.livekit.io/agents/models/realtime/plugins/gemini/)、[Pipecat](https://docs.pipecat.ai/pipecat/features/gemini-live)、[Vercel](https://vercel.com/docs/ai-gateway/modalities/realtime) 和 [Vision Agents](https://visionagents.ai/integrations/realtime/gemini) 等开发者平台让开发者能够轻松构建并部署高性能的语音驱动界面。这些平台在幕后管理着复杂的实时媒体流基础设施，让开发者可以专注于打造用户体验。

我们还与 Salesforce、Genspark 和 Lumeris 等公司展开合作，它们对 3.8 Live 和 3.8 Live Extended Thinking 兴奋不已，并特别称赞了其令人印象深刻的延迟、流畅性和工具调用能力。

![Salesforce 评价引述](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-live__testimonial-sale.width-100.format-webp.webp)

![11Sight 评价引述](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-live__testimonial-11-s.width-100.format-webp.webp)

![Equal AI 评价引述](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-live__testimonial-equa.width-100.format-webp.webp)

![ServiceNow 评价引述](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-live__testimonial-serv.width-100.format-webp.webp)

![Genspark 评价引述](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-live__testimonial-gens.width-100.format-webp.webp)

![Lenskart 评价引述](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-live__testimonial-lens.width-100.format-webp.webp)

![Lumeris 评价引述](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-live__testimonial-lume.width-100.format-webp.webp)

![Agora 评价引述](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-live__testimonial-agor.width-100.format-webp.webp)

![Ambr AI 评价引述](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-live__testimonial-ambr.width-100.format-webp.webp)

![LiveKit 评价引述](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-live__testimonial-live.width-100.format-webp.webp)

![Casuu 评价引述](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3-8-live__testimonial-casu.width-100.format-webp.webp)

## 以 SynthID 水印确保透明度

我们的 AI 产品生成的所有音频都带有 [SynthID](https://deepmind.google/models/synthid/) 水印。这种不可感知的水印被直接织入音频输出之中，确保 AI 生成的内容保持可检测，帮助防止错误信息。有关我们安全与责任方针的详细信息，请查阅[模型卡片](https://deepmind.google/models/model-cards/gemini-3-8-audio/)。

## 开始使用我们最新的 Gemini Audio 模型：

3.8 Live 从今天起开始推送：

- **面向开发者**：在 [Gemini API](https://ai.google.dev/gemini-api/docs/live-api) 和 [Google AI Studio](https://aistudio.google.com/live) 中提供
- **面向企业**：在 [Gemini Enterprise](https://console.cloud.google.com/vertex-ai/studio/multimodal-live) 中以私有预览版提供，并将很快登陆 [Gemini Enterprise for Customer Experience](https://cloud.google.com/gemini-enterprise-cx)
- **面向所有人**：在 Search Live 中提供

3.8 Live Extended Thinking 从今天起开始推送：

- **面向开发者**：在 [Gemini API](https://ai.google.dev/gemini-api/docs/live-api) 和 [Google AI Studio](https://aistudio.google.com/live) 中提供
- **面向企业**：在 [Gemini Enterprise](https://console.cloud.google.com/vertex-ai/studio/multimodal-live) 中以私有预览版提供，并将很快登陆 [Gemini Enterprise for Customer Experience](https://cloud.google.com/gemini-enterprise-cx) 和 Google Workspace 商业客户
- **面向所有人**：在 Gemini Live 中提供；Workspace 中的 Docs 面向 Google AI Pro 和 Ultra 订阅用户，Gmail 和 Keep 则面向所有 Google AI 订阅用户
