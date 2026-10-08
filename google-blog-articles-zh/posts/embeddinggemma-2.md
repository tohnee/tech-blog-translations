---
title: "EmbeddingGemma 2：开放、轻量的多模态嵌入模型"
title_en: "EmbeddingGemma 2: an open, lightweight multimodal embedding model"
source: https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2/
site: google-blog
date: 2026-10-06
crawled: 2026-10-08
translated: 2026-10-08
---

# EmbeddingGemma 2：开放、轻量的多模态嵌入模型

> 原文：[EmbeddingGemma 2: an open, lightweight multimodal embedding model](https://blog.google/innovation-and-ai/technology/developers-tools/embeddinggemma-2/) · Google

去年，我们推出了 [EmbeddingGemma](https://developers.googleblog.com/en/introducing-embeddinggemma/)，为高质量文本嵌入提供一个轻量级选择，帮助你的应用直接在消费级硬件上组织、搜索和连接信息。开发者社区的反响远超我们的预期：下载量已超过 2,000 万，开发者们用它驱动更智能的端侧（on-device）搜索工具与隐私优先（privacy-first）的检索增强生成（RAG）流水线。

今天，我们正式发布 EmbeddingGemma 2，将统一范围从文本扩展到代码、图像、视频与音频，全部纳入同一共享嵌入空间。EmbeddingGemma 2 基于 Gemma 4 架构构建，以商业友好的 Apache 2.0 许可证发布，拥有 7.4 亿参数，是端侧推理的理想之选。它可以帮你从语音备忘录中找到特定的视频片段，或根据文本查询搜索数小时的录音——这一切都由单一的原生多模态模型处理。

EmbeddingGemma 2 与 Gemini Embedding 模型同源，具备以下特性：

- **同级最优：**在 MTEB（Massive Text Embedding Benchmark）Code 与 MAEB（Massive Audio Embedding Benchmark）等基准测试中，取得同尺寸（sub-1B）多模态嵌入模型中的领先分数，并在文本、视觉与音频任务上持平或超越许多更大的模型。
- **模块化设计：**纯文本工作负载最低仅需 270M 参数，可选配视觉（170M）与音频（300M）编码器以获得完整多模态支持。
- **存储高效：**借助 Matryoshka 表示学习（MRL），开发者可以将输出向量从 768 维动态截断至 512、256 或 128 维，为本地向量数据库与内存占用带来最高 6 倍的存储缩减。
- **针对端侧性能优化：**在严苛的资源约束下高效运行。经量化后，在 Google Pixel 11 Pro 上，EmbeddingGemma 2 的纯文本权重仅需约 191MB 活动内存（RAM），完整多模态模型约需 567MB。
- **支持扩展上下文：**具备 8K token 上下文窗口（是 EmbeddingGemma 1 的 4 倍），可直接在本地硬件上处理最长 5.5 分钟的音频、29 张图像、58 帧视频，或它们的交错组合。

## 在代码、视觉与音频上达到顶级质量

EmbeddingGemma 2 延续了 EmbeddingGemma 出色的多语言文本性能，同时代码性能显著提升 9.92 分（MTEB Code 从 68.76 升至 78.68），非常适合本地代码库索引、语义代码搜索与编程智能体检索。在图像、视频、文档与音频方面，它为 sub-1B 模型树立了单位参数质量的新标准，甚至超越了一些体积超过其两倍的专用模型。

![大规模文本嵌入基准（Code）](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Massive_Text_Embedding_Benchmark_.width-100.format-webp.webp)

![大规模图像嵌入基准（Lite）](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Massive_Image_Embedding_Benchmark.width-100.format-webp.webp)

![大规模音频嵌入基准](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Massive_Audio_Embedding_Benchmark.width-100.format-webp.webp)

完整评测指标与模型信息见 [EmbeddingGemma 2 模型卡](https://ai.google.dev/gemma/docs/embeddinggemma/model_card_2)。

## 完全在端侧实现语义搜索、路由与检索

EmbeddingGemma 2 将强大能力直接带到边缘硬件上。在本地生成嵌入有助于保障数据隐私、降低流水线延迟，并让开发者能够构建完全离线运行的跨模态搜索与检索。

与 Gemma 4 等生成式模型搭配时，EmbeddingGemma 2 可以构建能够理解复杂多模态数据的端侧 RAG 流水线。由于 EmbeddingGemma 2 基于 Gemma 4 构建，并共享其文本分词器与音频编码器，开发者可以将两个模型在统一流水线中一同运行，合计内存占用更低。

用文本或图像在媒体库中按语义相似度找到最匹配的结果。可在 [Google AI Edge Gallery](https://developers.google.com/edge/gallery) 的 Instant Media Search 中试用。

使用文本或音频查询定位视频中的特定时刻。可在 [Google AI Edge Gallery](https://developers.google.com/edge/gallery) 的 Video Moments Finder 中试用。

将 EmbeddingGemma 2 用于本地文件检索，并搭配 Gemma 4 进行情境推理。可在 [Google AI Edge Foresight](https://developers.google.com/edge/foresight) 应用中试用。

通过 [MediaPipe Decision Task API](https://developers.google.com/edge/mediapipe/solutions/decision/decision_maker) 创建实时决策引擎，利用多模态上下文实现分类、路由与预测能力。

想了解如何用 LiteRT 构建端侧搜索与 RAG 系统，请阅读 [Google AI Edge 博客文章](http://developers.googleblog.com/google-ai-edge-with-embeddinggemma-2)。

## 开始使用 EmbeddingGemma 2

我们与以下伙伴紧密合作，确保 EmbeddingGemma 2 在你构建之处即刻可用：

- **下载模型：**模型权重可在 [Hugging Face](https://huggingface.co/google/embeddinggemma-2) 与 [Kaggle](https://www.kaggle.com/models/google/embeddinggemma-2) 获取，Gemini Enterprise Agent Platform Model Garden 即将上线。如需针对端侧优化的模型，请访问 [Hugging Face 上的 LiteRT Community](https://huggingface.co/litert-community)。
- **端侧部署：**使用 Google AI Edge [MediaPipe](https://developers.google.com/edge/mediapipe/solutions/decision/decision_maker) 开箱即用地完成嵌入、检索与决策任务，或使用 [LiteRT](https://developers.google.com/edge/litert-lm) 进行自定义模型集成，开发跨平台应用。也可用 transformers.js 或 [WebGPU](https://huggingface.co/spaces/webml-community/embeddinggemma-2-webgpu) 为浏览器构建。
- **使用你偏好的开发工具：**通过 transformers、sentence-transformers、[MLX](https://github.com/Blaizzy/mlx-vlm)、vLLM、[llama.cpp](https://huggingface.co/ggml-org/embeddinggemma-2-GGUF)、SGLang、[Ollama](http://ollama.com/library/embeddinggemma-2) 与 LMStudio 高效部署模型。用 [Qdrant](https://qdrant.tech/blog/embeddinggemma-2/) 存储你的嵌入向量。
- **微调：**按照 [Unsloth](https://unsloth.ai/docs/models/embeddinggemma-2) 的指南，针对你的用例微调 EmbeddingGemma 2。

欢迎探索我们的[开发者指南](https://developers.googleblog.com/en/embeddinggemma-2-the-developer-guide/)、[文档](https://ai.google.dev/gemma/docs/embeddinggemma)，以及[推理](https://ai.google.dev/gemma/docs/embeddinggemma/inference-embeddinggemma-with-sentence-transformers)与[微调](https://ai.google.dev/gemma/docs/embeddinggemma/fine-tuning-embeddinggemma-with-sentence-transformers)指南。
