---
title: "Gemini 推出智能体化视频理解能力"
title_en: "Introducing agentic video understanding with Gemini"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-agentic-video-in-gemini/
site: gemini
date: 2026-09-01
crawled: 2026-09-13
translated: 2026-09-13
---

# Gemini 推出智能体化视频理解能力

> 原文：[Introducing agentic video understanding with Gemini](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-agentic-video-in-gemini/) · Google

今天，我们在最新模型上全面推出[智能体化视频理解（agentic video understanding）](https://ai.google.dev/gemini-api/docs/video-understanding#agentic-video-understanding)：Gemini 3.7 Flash、3.6 Flash 和 3.5 Flash-Lite。这项新能力在提升准确度的同时，大幅降低了视频分析的 token 用量和成本。与结合了代码执行和 Gemini 模型原生图像理解的[智能体化视觉（agentic vision）](https://blog.google/innovation-and-ai/technology/developers-tools/agentic-vision-gemini-3-flash/)类似，智能体化视频理解利用 Gemini 的原生视频工具来提升性能，并为视频处理解锁新能力，例如亚秒级时刻检索、更精确的异常检测、精确计数等。

该功能今天即可通过 Google AI Studio 和 Gemini Enterprise Agent Platform 中的 Gemini API，用于视频上传和 YouTube 视频。

## 基准测试

与当前“静态”处理方式不同——静态处理中模型以固定帧率摄取视频（默认 1 FPS，可通过 API 调整）——智能体化视频理解将模型的核心推理与原生视频工具相结合，跨视觉帧、音频和转录文本动态地搜索、扫描和检视目标视频片段。在标准视频分析基准上，启用智能体化视频理解的 Gemini 模型**最多可将分析成本降低 66%、token 消耗降低 88%，同时将准确度提升最高 7%。**

这些效率提升在长视频上尤为显著（从 10 分钟的使用指南，到 90 分钟的讲座，再到数小时的录像），因为在静态处理下，开发者要么承受高昂的 token 成本，要么采用会丢失关键细节的技巧，二者只能取其一。

启用智能体化视频理解后，Gemini 3.7 Flash 的 token 消耗最多可降低 88%，准确度最高可提升 7%。

![分析 token 效率与准确度提升的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/agentic-video__evals.width-1200.format-webp.webp)

虽然这些提升覆盖全部三个支持的模型，但启用智能体化理解的 Gemini 3.7 Flash 在整体质量上表现最佳，也是质量与成本效率的最佳组合，在受测的视频理解模型中处于准确度-成本的帕累托前沿。

使用智能体化视频理解，使 Gemini 3.7 Flash 在视频分析上处于准确度-成本的帕累托前沿。

![横轴为“每次查询成本”、纵轴为“准确度”的图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/agentic-video__evals_table2.width-1200.format-webp.webp)

## 工作原理

静态处理是模型以固定帧率摄取媒体流，而智能体化视频理解则让 Gemini 以主动的、目标导向的方式决定*看什么*、以*什么速度*看、以及通过*哪种模态*看（帧、音频还是转录文本），只获取所需的时刻和信号。开发者以前也可以手动完成这些操作，但借助智能体化视频理解，Gemini 可以通过一个智能体化循环来实现——调用内部工具加载视频文件的相关部分，从而显著降低开发开销。

![从查询到输出的流程图](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/agentic-video__diagram.width-1200.format-webp.webp)

## 能力与应用场景

智能体化视频理解改变了开发者处理长视频内容的方式，适用于多种高要求应用。

- **亚秒级时刻检索**：精确定位在 1 FPS 下容易错过的瞬时状态变化和紧凑的剪切边界，让精确的自动化视频剪辑成为可能。
- **长视频大海捞针式检索**：在数小时的视频上回答复杂查询，而无需消耗数百万 token。
- **异常检测**：以更高的帧率对感兴趣的时间窗口重新采样，以检视快速运动和细微的视觉伪影。
- **动作与物体计数**：随时间推移准确追踪重复的肢体动作和不同的物体。

***节省 token 的长视频分析***

*看看 Gemini 3.7 Flash 在长视频理解基准 LongVideoBench 上启用与不启用智能体化视频理解的差异。注意 token 的大幅减少和准确度的提升。*

***借助动态帧率实现精确的快速动作分析***

*借助智能体化视频理解，3.7 Flash 能够按需以不同帧率扫描和反复观看视频，从而准确统计一个快节奏动作的次数。*

**节省 token 的大海捞针式检索**

*借助智能体化视频理解，Gemini 3.7 能够基于视频内容准确回答复杂问题，同时 token 消耗远低于静态分析。*

## 真实世界成效

许多早期体验合作伙伴在测试智能体化视频理解时都看到了出色表现。以下是他们的反馈：

![来自 Ponder 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/agentic-video-understanding__test.width-100.format-webp.webp)

![来自 Revyl 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/agentic-video-understanding__test.width-100.format-webp_IH5FVna.webp)

![来自 Mosaic 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/agentic-video-understanding__test.width-100.format-webp_JwIFAZ5.webp)

![来自 Resemble.AI 的引言](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/agentic-video-understanding__test.width-100.format-webp_HHQ7484.webp)

## 快速上手

智能体化视频理解现可通过 [Google AI Studio](https://ai.google.dev/gemini-api/docs/video-understanding#agentic-video-understanding) 和 [Gemini Enterprise Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/capabilities/video-understanding) 中的 Gemini API 使用，覆盖 Gemini 3.7 Flash、3.6 Flash 和 3.5 Flash-Lite。它采用标准 Gemini API token 定价，不收取额外功能费。

要启用该功能，只需在 API 配置中将 processing 设为 "agentic"。请阅读我们的[开发者指南](http://ai.dev/learn/agentic-video-understanding-with-gemini)，深入了解这项功能以及如何上手。

```py
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        {
            "type": "video",
            "uri": "https://youtu.be/7Z5Vy9JBANs",
            "processing": "agentic"
        },
        {
            "type": "text",
            "text": "What are the 3 most important announcements in this keynote?",
        },
    ],
)

print(interaction.output_text)
```

我们还将把智能体化视频理解带来的效率与质量提升带给 Google 各产品中的数十亿用户。该功能很快将向 Gemini 应用中 Flash 和 Flash-Lite 模型的所有用户推送。而在未来几个月，智能体化视频理解还将为视频观看页面的 YouTube「[Ask YouTube](https://support.google.com/youtube/answer/14110396?hl=en&co=GENIE.Platform%3DAndroid)」功能提供支持，借助 Gemini 基于画面内容给出更高质量的回答。

***感谢以下人员对这项工作的贡献：*** *Sergi Caelles、Filip Pavetić、Ahmet Iscen、Suhas Yogin，以及智能体化视觉（Agentic Vision）团队。*
