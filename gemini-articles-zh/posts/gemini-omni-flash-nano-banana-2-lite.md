---
title: "使用 Nano Banana 2 Lite 与 Gemini Omni Flash 开始构建"
title_en: "Start building with Nano Banana 2 Lite and Gemini Omni Flash"
source: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni-flash-nano-banana-2-lite/
site: gemini
date: 2026-06-30
crawled: 2026-09-13
translated: 2026-09-13
---

# 使用 Nano Banana 2 Lite 与 Gemini Omni Flash 开始构建

> 原文：[Start building with Nano Banana 2 Lite and Gemini Omni Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni-flash-nano-banana-2-lite/) · Google

今天，我们通过两项重要发布，让你的创意实验、打磨和规模化变得更快、更轻松：

- **推出** [**Nano Banana 2 Lite：**](https://deepmind.google/models/gemini-image/flash-lite/)Nano Banana 家族迄今最快、成本效益最高的图像模型，为高吞吐量、速度和规模而生。Nano Banana 2 Lite 从今天起已在 [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-3.1-flash-lite-image)、[Gemini API](https://ai.google.dev/gemini-api/docs/image-generation) 和 [Gemini Enterprise Agent Platform](https://console.cloud.google.com/agent-platform/studio/multimodal?model=gemini_omni_flash_preview) 上可用。它也在今天开始登陆 Google 的消费者平台，包括 Search 中的 AI Mode、Gemini 应用以及众多其他产品。
- **[Gemini Omni Flash](http://deepmind.google/models/gemini-omni) 首次向开发者开放：**我们高质量、高成本效益的视频生成与对话式编辑模型，现在首次在 [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-omni-flash-preview&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)、[Gemini API](https://ai.google.dev/gemini-api/docs/omni) 和 [Gemini Enterprise Agent Platform](https://console.cloud.google.com/agent-platform/studio/multimodal?model=gemini_omni_flash_preview) 上可用。Omni Flash 也可在 [Gemini 应用](http://gemini.google/)和 [Google Flow](http://flow.google/) 中使用。

使用生成式媒体进行构建，往往是创意迭代的过程。借助这两个模型，开发者可以构建端到端的完整多媒体体验，把快速图像生成与视频创作和编辑连接起来。无论你的工作流需要生成数千张图像，还是编辑多轮视频序列，现在你都有两个新模型来加快构建速度、无缝迭代，并把创意愿景变为现实。

## Nano Banana 2 Lite：我们最快、最具成本效益的 Gemini Image 模型

观看一段并排对比视频，展示 Nano Banana 2 Lite 与 Nano Banana 2 在一个简单提示词下的图像生成速度与质量。

Nano Banana 2 Lite（gemini-3.1-flash-lite-image）专为快速构思和高流速的开发者管线而设计，这类场景中速度和成本是首要约束。对于目前仍在使用第一代 Nano Banana（gemini-2.5-flash-image）的开发者，我们推荐以它作为替代——现在就可以替换，立即在关键性能维度上获益。

Nano Banana 2 与 2 Lite 相较竞品 AI 图像模型的性能基准，评估生成/编辑质量（Elo 分数）、处理延迟与单张 1K 分辨率图像成本之间的取舍。

![一张动图，展示图像生成与编辑对照延迟和价格的对比](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/nb2-lite__benchmark_blog.gif)

### Nano Banana 2 Lite 的亮点：

- **延迟：**4 秒内交付文生图输出。这使它成为交互式原型设计和快速视觉草稿的理想之选。
- **成本效益（每张 1K 图像 0.034 美元）：**对专注于草稿、构思、管理运营预算或低带宽使用的开发者而言，是高成本效益的选择。

尽管优先考虑速度，Nano Banana 2 Lite 依然保持着可靠的提示词遵循能力、强大的角色一致性以及清晰可读的图内文字渲染。

### 认识 [Nano Banana](https://ai.google.dev/gemini-api/docs/image-generation) 家族

![一张模型对比表格图，比较 Nano Banana 2 Lite、Nano Banana 2 和 Nano Banana Pro](https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/Copy_of_nb2-lite__model_table_light_V2.gif)

- **Nano Banana 2 Lite（Gemini 3.1 Flash Lite Image）：**为速度而生。针对近乎实时、高流量的工作流优化，超低延迟是这些场景的关键。
- **Nano Banana 2（Gemini 3.1 Flash Image）：**全能型主力。以更低延迟交付高质量，是性能与成本的最佳平衡。
- **Nano Banana Pro（Gemini 3 Pro Image）：**为复杂的专业用例优化。它为准确性重于速度的任务提供最强大的控制力和先进的推理能力。
- **Nano Banana（Gemini 2.5 Flash Image）：**我们的旧一代模型。我们建议升级到 Nano Banana 2 Lite，以获得更好的质量、更快的速度和更低的成本。

要查看模型能力的完整列表及集成方法，请查阅开发者[文档](https://ai.google.dev/gemini-api/docs/omni)。

在开发者平台发布的同时，Nano Banana 2 Lite 也将登陆 Google 的消费者平台，包括 Search 中的 AI Mode、Gemini 应用、NotebookLM、Google Photos、Stitch、Google Flow 和 Google Ads。

## 用 Gemini Omni Flash 体验高质量、高成本效益的视频编辑与生成

观看有人使用 Gemini Omni 表演四个数字魔术，比如从手机里拉出一个 3D 气球文字，或把水从屏幕倒进玻璃杯。角落里有一段小小的「原始」视频，展示了她实际拍摄这些魔术的过程——那是在 Omni 生成的特效添加之前。

在 Google I/O 上，我们发布了 [Gemini Omni Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/)——一个将 Gemini 的多模态推理与视频生成和编辑相结合的模型。今天，Gemini Omni Flash（gemini-omni-flash-preview）开始通过 Gemini API 和 Google AI Studio 面向开发者推送，原生支持从文本、图像和视频输入组合生成高质量视频并进行对话式编辑。该模型定价具有竞争力，为每秒视频输出 0.10 美元，与 Veo 3.1 Fast 相同。

Omni Flash 的亮点：

- **对话式视频编辑：**用自然语言来精修和编辑视频。
- **多模态引用：**组合图像、文本和视频等输入，保持对场景的控制和一致性。
- **真实世界知识：**Omni 借助 Gemini 的知识——如历史、生物学和叙事逻辑——来构建引人入胜的视频。
- **文字与动作同步：**通过简单的提示词，将文字和图形直接连接到视频动作。

欲了解全面的基准测试信息，请访问 Google DeepMind 的 [Gemini Omni](https://deepmind.google/models/gemini-omni/) 网页。

![一张关于视频编辑的基准测试图表](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Video_Editing__-_Descending_-_Ch.width-1200.format-webp.webp)

限制：

- Omni 目前支持 10 秒视频生成，更长时长即将推出。
- 该模型在 Gemini API 中尚不支持上传音频参考和场景扩展。
- 视频参考在 API 架构上可接受最长 3 秒的时长，但目前模型无法正确处理。
- 更换场景或平移运镜时的角色一致性尚有一些限制，我们正在努力改进。

Gemini Omni 从今天起在 Google AI Studio 和 Gemini API 中以公开预览版提供。要查看模型能力的完整列表和各地区的具体限制，请查阅开发者[文档](https://ai.google.dev/gemini-api/docs/omni)。

## 今天就用这两个模型开始构建

真正的魔力在于把这两个模型串联起来。用 Nano Banana 2 Lite 作为高速图像生成模型，然后把生成的图像作为参考传给 Gemini Omni Flash，让它动起来成为高质量视频。此外，通过使用 [Interactions API](https://ai.google.dev/api/interactions-api) 来构建这类多轮体验，你可以维持会话历史和上下文，让用户最多叠加三次连续编辑。

为帮助你上手，我们创建了几个可供改造的演示应用，让你体验如何把 Nano Banana 2 Lite 和 Gemini Omni Flash 搭配进同一个工作流。

[Anywhere](https://aistudio.google.com/apps/bundled/anywhere) 是一个为展示两个模型强大能力而构建的演示应用。自拍或上传一张照片，应用会用 Nano Banana 2 Lite 瞬间把你传送到数十个标志性地标。然后，点击生成的图像时，Omni Flash 会把图像变成该地点的动画片段。

[Space Lift](https://aistudio.google.com/apps/bundled/space-lift) 是一个由 Nano Banana 2 Lite 和 Gemini Omni 驱动的室内设计演示应用，上传一张照片即可瞬间重新构想任何房间。应用会自动生成覆盖各种设计美学的完整概念方案。找到你喜爱的风格后，点击视频按钮，观看 Omni 以电影般的展示让设计活起来，让它在成为现实之前先在动态中体验你的新空间。

[Omni product studio](https://aistudio.google.com/apps/bundled/omni-product-studio) 是一个演示应用，把 Nano Banana 2 Lite 创建的静态图像转换成由 Gemini Omni 制作的电商级电影感视频。这个演示展示了如何通过快速交互合并多模态输入、输出从图像到视频的成果，从而构建交互式媒体。

![来自 Astrocade 联合创始人兼 CTO Ali Sadeghian 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-omni-flash__blog-testimoni.width-100.format-webp.webp)

![来自 AI Lab (HubX) CAIO Yunus Emra 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-omni-flash__blog-testimoni.width-100.format-webp_9ojqAYU.webp)

![来自 Latitude CEO 兼联合创始人 Nick Walton 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-omni-flash__blog-testimoni.width-100.format-webp_p9M5qxu.webp)

![来自 Stan 创始人兼 CEO Path Chadha 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-omni-flash__blog-testimoni.width-100.format-webp_cTixMlp.webp)

![来自 Magnific CEO 兼创始人 Joaquin Cuenca 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-omni-flash__blog-testimoni.width-100.format-webp_RxcxodD.webp)

![来自 Agent Opus 产品负责人 Ada Liu 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-omni-flash__blog-testimoni.width-100.format-webp_FC4Jx5D.webp)

![来自 Cartwheel 联合创始人 Andrew Carr 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-omni-flash__blog-testimoni.width-100.format-webp_E4dbiGT.webp)

![来自 Flora 应用 AI 负责人 Alec Jo 的评价](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/gemini-omni-flash__blog-testimoni.width-100.format-webp_NSVqwjq.webp)

## 以安全与透明为本进行构建

Gemini Omni 和 Nano Banana 2 Lite 构建在 Google 安全的基础设施之上，并使用 [SynthID](https://deepmind.google/blog/identifying-ai-generated-images-with-synthid/) 水印。你可以通过 Gemini 应用、Chrome 中的 Gemini 或 Search 验证 AI 内容。[进一步了解](https://blog.google/innovation-and-ai/products/identifying-ai-generated-media-online)我们如何扩展验证工具，帮助你在全网理解内容是如何被创建和编辑的。

## 今天就启动你的项目

Nano Banana 2 Lite 资源：

- 前往 [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-3.1-flash-lite-image)，在 playground 中试用该模型。
- 深入阅读我们的 [Gemini API 文档](https://ai.google.dev/gemini-api/docs/image-generation)。
- 查看我们的 Nano Banana [提示词指南](https://ai.google.dev/gemini-api/docs/image-generation#prompt-guide)，其中满是最佳实践和示例提示词。

Gemini Omni Flash 资源：

- 前往 [Google AI Studio](https://aistudio.google.com/prompts/new_chat?model=gemini-omni-flash-preview&utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)，在 playground 中试用该模型。
- 深入阅读我们的 [Gemini API 文档](https://ai.google.dev/gemini-api/docs/omni)。
- 查看我们的 Gemini Omni Flash [提示词指南](https://ai.google.dev/gemini-api/docs/omni#prompt-guide)，其中满是最佳实践和示例提示词。
