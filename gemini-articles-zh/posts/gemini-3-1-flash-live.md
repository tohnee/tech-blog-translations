---
title: "Gemini 3.1 Flash Live：让音频 AI 更自然、更可靠"
title_en: "Gemini 3.1 Flash Live: Making audio AI more natural and reliable"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-live/
site: gemini
date: 2026-03-26
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 3.1 Flash Live：让音频 AI 更自然、更可靠

> 原文：[Gemini 3.1 Flash Live: Making audio AI more natural and reliable](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-live/) · Google

今天，我们通过 Gemini 3.1 Flash Live 进一步提升 Gemini 的实时对话能力，这是我们迄今为止质量最高的音频与语音模型。它提供了下一代语音优先（voice-first）AI 所需的速度和自然节奏，为开发者、企业和普通用户带来更直观的体验。

3.1 Flash Live 已在 Google 各产品中可用：

- 面向开发者：通过 [Google AI Studio](http://ai.studio/live) 中的 [Gemini Live API](https://ai.google.dev/gemini-api/docs/live) 提供预览版
- 面向企业：通过 [Gemini Enterprise for Customer Experience](https://cloud.google.com/products/gemini-enterprise-for-customer-experience?e=48754805) 提供
- 面向所有人：通过 [Search Live](https://blog.google/products-and-platforms/products/search/search-live-global-expansion) 和 [Gemini Live](https://gemini.google/overview/gemini-live/) 提供

## 面向开发者：稳健的推理与任务执行

我们提升了 3.1 Flash Live 的整体质量，让开发者和企业能够更可靠地构建可大规模完成复杂任务的语音优先智能体。在 [ComplexFuncBench Audio](https://github.com/zai-org/ComplexFuncBench?tab=readme-ov-file)——一个衡量带各种约束的多步函数调用的基准测试——上，它以 90.8% 的分数领先于我们的上一代模型。

![ComplexFuncBench audio 柱状图](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_flash_live__complexfuncbench__eval__light_Web.gif)

![BigBenchAudio 柱状图](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_flash_live__bigbenchaudio__eval__light_Web.gif)

在 Scale AI 的 [Audio MultiChallenge](https://labs.scale.com/leaderboard/audiomc) 上，Gemini 3.1 Flash Live 在开启「思考」模式的情况下以 36.1% 的分数位居榜首。该基准专门测试在真实世界音频中常见的打断和犹豫情境下，模型对复杂指令的遵循能力和长程推理能力。

![AudioMultiChallenge 柱状图](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_flash_live__audiomultichallenge__eval__light_Web.gif)

3.1 Flash Live 还改进了对语调的理解，从而带来更自然的对话。在 [Gemini Enterprise for Customer Experience](https://cloud.google.com/products/gemini-enterprise-for-customer-experience?e=48754805) 中，它比 2.5 Flash Native Audio 更能识别音高、语速等声学上的细微差别，也更善于根据用户表达的沮丧或困惑动态调整回复。

3.1 Flash Live 让你能够构建在嘈杂环境中处理复杂任务的语音智能体。

使用 Gemini 3.1 Pro 构建的演示示例，由 Gemini 3.1 Flash Live 驱动。

3.1 Flash Live 让你可以用语音进行 vibe code（氛围编程）并快速迭代。

使用 Gemini 3.1 Pro 构建的演示示例，由 Gemini 3.1 Flash Live 驱动。

Verizon、LiveKit 和 The Home Depot 等公司对 3.1 Flash Live 在其工作流程中的表现给予了积极反馈，特别强调了它改进后的自然对话能力。

![The Home Depot 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_live_Enterprises.width-100.format-webp.webp)

![Verizon 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_live_Enterprises.width-100.format-webp_Cc2KmJB.webp)

![LiveKit 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_live_Developers_.width-100.format-webp.webp)

![Wavera 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_live_Developers_.width-100.format-webp_NV2mIWo.webp)

![Stream 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_live_Developers_.width-100.format-webp_7gtqzd5.webp)

![YouTube 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-3.1-flash_live_Enterprises.width-100.format-webp_fbYyeA9.webp)

## 面向所有人：更自然、更直观的交互

在 Gemini Live 和 Search Live 中，3.1 Flash Live 模型能给出更有帮助、更自然的回复，无论你是在询问日常的简单问题，还是进行更复杂的对话。

在 3.1 Flash Live 模型的加持下，Gemini Live 相比上一代模型响应更快，并且能够跟上你对话脉络的时间是原来的两倍，让你在更长的头脑风暴中思路不断。

3.1 Flash Live 让 Gemini Live 更快、更有帮助

3.1 Flash Live 本身还具备多语言能力，这也支撑了本周 [Search Live 的全球扩张](https://blog.google/products-and-platforms/products/search/search-live-global-expansion)。随着此次发布，200 多个国家和地区的用户现在可以用自己偏好的语言与 Search 进行实时的多模态对话。

在 Search Live 中使用 3.1 Flash Live 获取实时排障帮助

## 试用 Gemini 3.1 Flash Live

3.1 Flash Live 生成的所有音频都带有 SynthID 水印。这种不可感知的水印直接交织在音频输出中，能够可靠地检测 AI 生成的内容，帮助防止错误信息传播。欲了解我们在安全与责任方面的方法，请参阅[模型卡](https://deepmind.google/models/model-cards/gemini-3-1-flash-live)。

从今天起，来体验 3.1 Flash Live 的自然与可靠。我们期待看到你与它交互、用它构建的种种可能。
