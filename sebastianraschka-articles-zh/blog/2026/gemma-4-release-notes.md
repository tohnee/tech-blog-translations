---
title: "Gemma 4 架构与基准测试笔记"
title_en: "Gemma 4 Architecture and Benchmark Notes"
source: https://sebastianraschka.com/blog/2026/gemma-4-release-notes.html
crawled: 2026-09-06
translated: 2026-09-06
---

# Gemma 4 架构与基准测试笔记

> 原文：[Gemma 4 Architecture and Benchmark Notes](https://sebastianraschka.com/blog/2026/gemma-4-release-notes.html)

旗舰开放权重模型发布日总是令人兴奋。对于 Gemma 4，我首先把 31B 配置和 Gemma 3 27B 放在一起对比。两者的家族相似性一目了然，不过还是有一些长上下文方面的改进，值得与保持不变的部分区分开来。

完整的 [Gemma 4 家族](https://ai.google.dev/gemma/docs/core/model_card_4)包含五个尺寸。本文聚焦于稠密的 31B 模型和 26B-A4B 专家混合（MoE）变体。两者都接受文本和图像输入。更小的 E2B、E4B 和 12B 模型则覆盖一些不同的边缘端和多模态使用场景。

## 31B 文本解码器

根据 [31B 配置文件](https://huggingface.co/google/gemma-4-31B-it/blob/main/config.json)，文本解码器有 60 层。Google 标注该模型为 307 亿参数。解码器的嵌入宽度为 5,376，前馈隐藏维度为 21,504。词表包含 262,144 个 token。

注意力层排布遵循熟悉的 Gemma 模式：每五个滑动窗口层之后跟一个完整注意力层，如此在堆叠中重复。这样得到 50 个局部层和 10 个全局层。最后一层是全局层，局部窗口覆盖 1,024 个 token。

Gemma 4 还保留了来自 Gemma 3 的分组查询注意力（GQA）、QK-Norm，以及不常见的前置与后置 RMSNorm 组合。局部层使用 16 个键值头；全局层把这一数量减少到 4 个，使用统一的键和值，并应用比例式 RoPE。256K 的[上下文窗口](https://sebastianraschka.com/glossary/#context-length "Context Length")是 Gemma 3 27B 的 128K 上限的两倍。

这些对于长上下文使用来说是有意义的改动，同时基础的 transformer 块依然可以一眼认出来。Gemma 4 还附带一个专用的草稿模型（draft model），用于多 token 预测和投机解码。那条辅助路径与下文的文本解码器图示是分开的。

图中聚焦的是语言模型主干。完整的 31B 检查点还包含一个约 5.5 亿参数的视觉编码器，用于图像输入。它不包含某些更小的 Gemma 4 变体中提供的原生音频编码器。

## [基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")跳升告诉我们什么

[Google 模型卡](https://ai.google.dev/gemma/docs/core/model_card_4)报告了相对 Gemma 3 27B 的大幅提升。Gemma 4 31B 在 MMLU-Pro 上得分 85.2，而 Gemma 3 为 67.6。在 LiveCodeBench v6 上，报告的分数分别是 80.0 和 29.1。GPQA Diamond 从 42.4 提升到 84.3。

这些 Gemma 4 的结果与 [Qwen3.5-27B 模型卡](https://huggingface.co/Qwen/Qwen3.5-27B)中几个相同基准测试上的数值很接近。Qwen 报告的是 MMLU-Pro 86.1、LiveCodeBench v6 80.7、GPQA Diamond 85.5。

我仍然把这当作一个粗略对比。Gemma 和 Qwen 的数字分别来自各自的模型提供方，而不是同一个独立评测执行框架（harness）。Google 的表格还把 Gemma 3 基线标注为 `no think`，而 Gemma 4 有可配置的思考模式。因此这张图并不能把架构、数据、[预训练](https://sebastianraschka.com/glossary/#pretraining "Pretraining")或后训练各自的影响分离出来。

我的猜测是，训练数据和训练配方贡献了大部分提升，因为核心解码器模板的变化幅度小于分数的变化幅度。公开发布材料中没有任何消融实验，能让我们把收益的某个百分比归因于某个单一因素。

## 26B-A4B [MoE](https://sebastianraschka.com/glossary/#moe "Mixture of Experts (MoE)") 替代方案

Gemma 4 还包含一个 [26B-A4B 配置](https://huggingface.co/google/gemma-4-26B-A4B-it/blob/main/config.json)。它有 252 亿总参数，每个 token 约使用 38 亿。每个 MoE 层从 128 个专家池中选择 8 个路由专家，同时使用 1 个共享专家。

该模型有 30 个解码器层，排布为 25 个滑动窗口层和 5 个全局注意力层。换句话说，它保持了同样的 5:1 注意力排布，只是把稠密的前馈计算换成了稀疏的专家路由。

其报告分数在若干任务上仅略低于稠密的 31B 模型：MMLU-Pro 是 82.6 对 85.2，LiveCodeBench v6 是 77.1 对 80.0，GPQA Diamond 是 82.3 对 84.3。它的实际吸引力在于更低的有效前馈计算量，不过完整的专家权重仍然需要存储。

为了保持主图的可读性，我没有把 MoE 架构放进主图。两个模型都可以在 [LLM Architecture Gallery 对比](https://sebastianraschka.com/llm-architecture-gallery/?compare=gemma-4-31b,gemma-4-26b-a4b#architecture-diff-tool)中查看，[26B-A4B 卡片](https://sebastianraschka.com/llm-architecture-gallery/#card-gemma-4-26b-a4b)也链接到它的配置和原始资料。

## 许可证变更

Gemma 4 以 [Apache License 2.0](https://ai.google.dev/gemma/docs/core/model_card_4) 发布。Gemma 3 使用的是定制的 Gemma 条款。改用标准的开源许可证，让许多研究和商业项目更容易评估其使用条件。

[![Gemma 4 31B 架构图与基准测试对比](https://sebastianraschka.com/images/blog/2026/gemma-4-release-notes/hero.webp)](https://sebastianraschka.com/llm-architecture-gallery/?compare=gemma-4-31b,gemma-3-27b#architecture-diff-tool)

图 1. Gemma 4 31B 保持了 Gemma 3 27B 的 5:1 局部-全局注意力排布。右上角的对比展示了变化的上下文长度、层配方和 KV 缓存估计。基准测试柱状图使用的是提供方报告的结果，而非同一套评测运行。

来源：我的 [Substack note](https://substack.com/@rasbt/note/c-237278550) 的扩展网页版。更多细节见 [Gemma 4 技术报告](https://arxiv.org/abs/2607.02770)。
