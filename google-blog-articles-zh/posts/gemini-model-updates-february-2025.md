---
title: "Gemini 2.0 现已面向所有人开放"
title_en: "Gemini 2.0 is now available to everyone"
source: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-model-updates-february-2025/
site: google-blog
date: 2025-02-05
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 2.0 现已面向所有人开放

> 原文：[Gemini 2.0 is now available to everyone](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-model-updates-february-2025/) · Google

去年 12 月，我们发布了 Gemini 2.0 Flash 实验版，[开启了](https://blog.google/technology/google-deepmind/google-gemini-ai-update-december-2024/)智能体时代——这是我们面向开发者的高效主力模型，具有低延迟和增强的性能。今年早些时候，我们在 Google AI Studio 中更新了 [2.0 Flash Thinking Experimental](https://deepmind.google/technologies/gemini/flash-thinking/)，它将 Flash 的速度与推理更复杂问题的能力相结合，提升了性能。

上周，我们[向 Gemini 应用的所有用户](https://blog.google/feed/gemini-app-model-update-january-2025)在桌面端和移动端推送了更新版 2.0 Flash，帮助每个人发现与 Gemini 创作、互动和协作的新方式。

今天，我们通过 [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.0-flash) 和 [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio) 中的 Gemini API，正式发布（GA）更新版 Gemini 2.0 Flash。开发者现在可以用 2.0 Flash 构建生产级应用。

我们还发布了 Gemini 2.0 Pro 的实验版，这是我们在编程性能和复杂提示词方面迄今最出色的模型。它已在 [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.0-pro-exp-02-05) 和 [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio) 中可用，并面向 Gemini 应用的 Gemini Advanced 用户开放。

我们还将发布一个新模型 Gemini 2.0 Flash-Lite——这是迄今最具成本效益的模型——以公开预览版形式在 [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.0-flash-lite-preview-02-05) 和 [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio) 中提供。

最后，[2.0 Flash Thinking Experimental 将向 Gemini 应用](http://blog.google/feed/gemini-app-experimental-models)用户开放，可在桌面端和移动端的模型下拉菜单中选择。

所有这些模型发布时都将支持多模态输入与文本输出，更多模态将在未来几个月内陆续正式发布。更多信息（包括定价细节）可在 [Google for Developers 博客](https://developers.googleblog.com/en/gemini-2-family-expands)中查阅。展望未来，我们正在为 Gemini 2.0 模型家族开发更多更新和更强的能力。

## 2.0 Flash：面向正式发布的全新更新

Flash 系列模型[首次亮相](https://blog.google/technology/ai/google-gemini-update-flash-ai-assistant-io-2024/)于 2024 年 I/O 大会，作为强大的主力模型深受开发者欢迎，非常适合大规模的高吞吐、高频任务，并凭借 100 万 token 的上下文窗口，极擅长跨海量信息进行多模态推理。我们非常高兴看到它在开发者社区中获得[热烈反响](https://developers.googleblog.com/en/gemini-20-family-expands/)。

2.0 Flash 现已正式发布（GA），面向我们 AI 产品中的更多用户开放，同时在关键基准测试中性能有所提升，图像生成和文本转语音功能也将很快到来。

你可以在 [Gemini 应用](https://gemini.google.com/)中试用 Gemini 2.0 Flash，或在 [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.0-flash) 和 [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio) 中通过 Gemini API 使用。定价详情见 [Google for Developers 博客](https://developers.googleblog.com/en/gemini-2-family-expands)。

## 2.0 Pro Experimental：迄今编程性能和复杂提示词处理能力最强的模型

随着我们持续分享 Gemini 2.0 的早期实验版本，例如 [Gemini-Exp-1206](https://blog.google/feed/gemini-exp-1206/)，开发者就其优势与最佳用例（比如编程）给予了我们极佳的反馈。

今天，我们发布的 Gemini 2.0 Pro 实验版正是对这份反馈的回应。在我们迄今发布的所有模型中，它拥有最强的编程性能和处理复杂提示词的能力，对世界知识的理解与推理也更为出色。它配备我们最大的 200 万 token 上下文窗口，能够全面分析和理解海量信息，并具备调用 Google 搜索和代码执行等工具的能力。

![此表格对比了 Gemini 不同版本（包括 1.5 Flash、1.5 Pro、2.0 Flash-Lite、2.0 Flash 和 2.0 Pro）在各类基准测试上的能力。它展示了每个版本在常识、代码生成、推理、事实性、多语言理解、数学、长上下文理解、图像理解、音频翻译和视频分析等任务上的表现。](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini_benchmarks_cropped_light1x.gif)

Gemini 2.0 Pro 现已作为实验模型面向开发者开放，可在 [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.0-pro-exp-02-05) 和 [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio) 中使用，Gemini Advanced 用户也可在桌面端和移动端的模型下拉菜单中选择它。

## 2.0 Flash-Lite：迄今最具成本效益的模型

我们对 1.5 Flash 的价格和速度收到了大量积极反馈。我们希望在保持成本与速度的同时继续提升质量。因此今天，我们推出 2.0 Flash-Lite——一个质量优于 1.5 Flash、而速度和成本持平的新模型。它在大多数基准测试中都胜过 1.5 Flash。

与 2.0 Flash 一样，它拥有 100 万 token 的上下文窗口和多模态输入。例如，为大约 40,000 张不重复的照片生成贴切的一行说明文字，在 Google AI Studio 付费档下的成本不到一美元。

Gemini 2.0 Flash-Lite 已在 [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-2.0-flash-lite-preview-02-05) 和 [Vertex AI](https://console.cloud.google.com/freetrial?redirectPath=/vertex-ai/studio) 中以公开预览版形式提供。

## 我们的责任与安全工作

随着 Gemini 模型家族的能力不断增强，我们将继续投资于稳健的措施，确保安全可靠的使用。例如，我们的 Gemini 2.0 系列采用了新的强化学习技术，利用 Gemini 自身来评判其回复。这带来了更准确、更有针对性的反馈，进而提升了模型处理敏感提示词的能力。

我们还利用自动化红队测试来评估安全风险，包括间接提示词注入（indirect prompt injection）带来的风险——这是一种网络安全攻击，攻击者会将恶意指令隐藏在可能被 AI 系统检索到的数据之中。
