---
title: "Gemini 3.1 Flash-Lite：为规模化智能而生"
title_en: "Gemini 3.1 Flash-Lite: Built for intelligence at scale"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-lite/
site: gemini
date: 2026-03-03
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 3.1 Flash-Lite：为规模化智能而生

> 原文：[Gemini 3.1 Flash-Lite: Built for intelligence at scale](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-flash-lite/) · Google

今天，我们推出 Gemini 3.1 Flash-Lite，这是 Gemini 3 系列中速度最快、性价比最高的模型。它专为大规模的高吞吐开发者工作负载而打造，在其价格和模型档位上提供了出色的质量。

从今天起，3.1 Flash-Lite 将以预览版形式推送：开发者可通过 [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-3.1-flash-lite-preview) 中的 Gemini API 使用，企业则可通过 [Vertex AI](https://console.cloud.google.com/vertex-ai/studio/multimodal?mode=prompt&model=gemini-3.1-flash-lite-preview) 使用。

## 无需妥协的成本效益

3.1 Flash-Lite 的价格仅为每百万输入 token 0.25 美元、每百万输出 token 1.50 美元，以更大型模型的一小部分成本提供增强的性能。根据 [Artificial Analysis 基准测试](https://artificialanalysis.ai/)，它的性能优于 2.5 Flash，首答案 token 生成时间（Time to First Answer Token）快 2.5 倍，输出速度提升 45%，同时保持相近或更优的质量。这种低延迟正是高频工作负载所需要的，使其成为开发者构建响应迅速的实时体验的理想模型。

![图片显示两张柱状图，标题为「Speed & Cost Efficiency」，将 Gemini 3.1 Flash-Lite 与其他几款模型（包括 Gemini 2.5 Flash-Lite、GPT-5 mini、Claude 4.5 Haiku 和 Grok 4.1 Fast）在「输出速度（越高越好）」和「价格（越低越好）」上进行比较。](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini-3.1_speed-cost_chart_1.gif)

Gemini 3.1 Flash-Lite 在速度和质量上都优于 2.5 Flash。

3.1 Flash-Lite 在 [Arena.ai 排行榜](http://arena.ai/leaderboard)上取得了令人瞩目的 1432 Elo 分数，并在推理和多模态理解基准测试中超越了其他同档位模型，包括 GPQA Diamond 86.9% 和 MMMU Pro 76.8%——甚至超过了 2.5 Flash 等上一代更大的 Gemini 模型。

![图片展示了一张多款 AI 模型的对比表，包括「Gemini 3.1 Flash-Lite」「Gemini 2.5 Dynamic」「Gemini 2.5 Flash-Lite」「GPT-5 mini」「Claude 4.5 Haiku」和「Grok 4.1 Fast」，涵盖输入/输出价格、输出速度以及各类学术、推理和事实性基准等多项指标。](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/gemini-3.1-flash-lite-table_1.gif)

## 面向开发者的规模化自适应智能

除了出色的原始性能之外，Gemini 3.1 Flash-Lite 在 AI Studio 和 Vertex AI 中还标配了思考等级（thinking levels），让开发者可以自主控制并灵活选择模型为一项任务「思考」多少，这对管理高频工作负载至关重要。3.1 Flash-Lite 能够大规模处理成本优先的任务，比如大批量翻译和内容审核；它也能处理需要更深入推理的更复杂工作负载，比如生成用户界面和仪表盘、创建模拟，或遵循复杂指令。

3.1 Flash-Lite 可以[用不同类别的数百种商品即时填充一个电商线框图](https://aistudio.google.com/apps/bundled/category_generator)。

3.1 Flash-Lite 能够[利用实时预报和历史数据实时生成动态天气仪表盘](https://aistudio.google.com/apps/bundled/weather_dashboard_agent)。

3.1 Flash-Lite 可以创建一个 SaaS 智能体，[为企业执行灵活多样的多步骤任务](https://aistudio.google.com/apps/bundled/versatile_execution_agent)。

3.1 Flash-Lite 能够快速分析和整理图像等大量内容。

在 AI Studio 和 Vertex AI 上的早期使用开发者，以及 Latitude、Cartwheel 和 Whering 等公司，已经在使用 3.1 Flash-Lite 大规模解决复杂问题。早期测试者强调了 3.1 Flash-Lite 的效率和推理能力，表示它能以更大型模型的精度处理复杂输入，还能遵循指令并保持良好的遵从性。

![Latitude 的 Kolby Nottingham 对 Google 模型指令遵循能力和速度的评价。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/3Flash-Lite_Blog_Quote_1.width-100.format-webp.webp)

![Cartwheel 的 Andrew Carr 对 3.1 Flash-Lite 速度和多模态标注能力的评价。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/3Flash-Lite_Blog_Quote_2.width-100.format-webp.webp)

![Whering 的 Bianca Rangecroft 关于使用 3.1 Flash-Lite 进行一致的商品打标和数据标注的评价。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/3Flash-Lite_Blog_Quote_3.width-100.format-webp.webp)

![HubX 的 Kaan Ortabas 对 Gemini 3.1 Flash-Lite 性能指标和成本效益的详细介绍。](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/3Flash-Lite_Blog_Quote_4.width-100.format-webp.webp)

我们期待看到你使用 3.1 Flash-Lite 以及 Gemini 3 系列的其他模型所构建的一切。
