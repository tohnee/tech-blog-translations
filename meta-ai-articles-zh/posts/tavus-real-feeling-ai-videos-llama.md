---
title: "Tavus 如何借助 Llama 让 AI 视频宛如真实对话"
title_en: "How Tavus is helping to make AI videos feel like real conversations"
date: 2025-04-02
source: https://ai.meta.com/blog/tavus-real-feeling-ai-videos-llama
crawled: 2026-09-22
translated: 2026-09-22
---

# Tavus 如何借助 Llama 让 AI 视频宛如真实对话

> 原文：[How Tavus is helping to make AI videos feel like real conversations](https://ai.meta.com/blog/tavus-real-feeling-ai-videos-llama) · Meta AI（Wayback 存档）

2025 年 4 月 2 日 · 6 分钟阅读

AI 视频研究公司 Tavus 利用先进的 AI 模型创造类人的数字交互，使其感觉与真实的人类对话一样自然。该平台集成了视觉问答与多图推理能力，让人们能够与数字复刻体（digital replica）进行引人入胜的实时互动。该公司使用 Llama 3.3 来支撑其对话视频界面（CVI）平台，开发者可以基于该平台构建与数字孪生之间丰富、逼真且实时的对话体验。

「引入 Llama 模型相当于同时赋予了数字复刻体『眼睛』和『大脑』——眼睛通过多图推理来解读视觉内容，大脑则提供细致入微、具备上下文感知的回应，」Tavus 联合创始人兼 CEO Hassaan Raza 说。这一方式使 Tavus 得以解决对话质量和视觉问答方面的关键难题，为每次交互带来栩栩如生的响应能力和连贯性。

## 选择 Llama

Tavus 的对话层运行在 Llama 之上，使平台能够处理实时的数字交互，而这在过去需要大量工程时间和多个模型才能实现。这套方案让一切更加高效，并确保响应快速、清晰。

团队选择 Llama 取代闭源 AI 模型，是因为它在对话质量、响应速度和灵活的开源设计方面更胜一筹。对 Tavus 而言，使用 Llama 这样的开源模型至关重要，因为它支持本地化部署与测试，相比闭源模型提升了速度、数据隐私和互操作性。开源社区和丰富的工具链让 Tavus 得以对模型进行实验和定制，带来更快的迭代，并更好地契合 Tavus 的具体用例。

Tavus 报告称效率和质量均有显著提升，Llama 的 70B 模型每秒可处理约 2000 个词元。公司将 Llama 模型用于若干关键功能：在对话式 AI 方面，Llama 模型实时提供响应迅速、具备上下文感知的交互，让数字复刻体能够流畅处理长篇对话；工具调用（tool calling）提升了响应能力，并支持带附加功能的动态交互；多图推理实现了视觉问答，能够基于视频中的视觉上下文给出准确回答。此外，通过集成经过微调的 Llama 模型并利用检索增强生成（RAG）技术，Tavus 允许客户使用自己的数据和检索源，定制 AI 以满足特定业务需求。

## 集成与实施

Tavus 顺利地完成了 Llama 的集成，使用了 8B 和 70B Instruct 版本，并进行了包括采用多级提示的高级提示工程在内的定制，以增强对话深度。基础设施最初同时在本地部署（vLLM）和托管云方案（Cerebras、Fireworks）上进行了测试。Tavus 还使用向量数据库和嵌入模型来优化存储与查询，Cerebras 和 Fireworks 等合作伙伴为云基础设施提供支持。

借助 Cerebras 的 Llama 实现，Tavus 相比高延迟模型取得了 440%–550% 的延迟改善，并比性能相当的 GPT 模型领先 25%–50%。「在我们整个 AI 技术栈中，Llama 一直是复杂度最低、可靠性最高的组件之一，」Raza 说，并指出它还受益于强大的社区支持以及与内部工作流的互操作性。

Llama 3.2 和 3.3（包括多模态能力以及适合端侧和边缘场景的小模型）正在帮助 Tavus 探索新的可能性。未来，公司希望扩展 CVI 平台内的功能，包括增强的语音识别、话轮检测（turn detection）和视觉问答。

了解更多关于 Tavus 的信息。

## 分享你的 Llama 故事

我们最新的动态会直接送达你的收件箱。订阅我们的新闻邮件，随时了解 Meta AI 的新闻、活动、研究突破等内容。与我们一起探索 AI 的无限可能。查看所有空缺职位
