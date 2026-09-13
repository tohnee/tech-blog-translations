---
title: "LLM Architecture Gallery 差异对比工具"
title_en: "LLM Architecture Gallery Diff Tool"
source: https://sebastianraschka.com/blog/2026/llm-architecture-gallery-diff-tool.html
crawled: 2026-09-06
translated: 2026-09-06
---

# LLM Architecture Gallery 差异对比工具

> 原文：[LLM Architecture Gallery Diff Tool](https://sebastianraschka.com/blog/2026/llm-architecture-gallery-diff-tool.html)

[LLM Architecture Gallery 差异对比工具](https://sebastianraschka.com/llm-architecture-gallery/?compare=deepseek-v3,deepseek-v3-2#architecture-diff-tool)可以并排比较两个模型架构栈。我添加这个功能，是因为相关的发布版本如果单独查看各自的规格卡片，看起来几乎一模一样。直接对比能让发生变化的模块更容易被发现。

选中两个模型后，工具会把它们的架构图并排摆放。四条摘要通道分别对比注意力模块、解码器类型、KV 缓存占用和层配方。规模和[上下文长度](https://sebastianraschka.com/glossary/#context-length "Context Length")显示在下方。如果任一模型有 Artificial Analysis 数据，对比中还会包含 AA Intelligence Index 及其分类画像。

每个字段都会标注 `Shared`（相同）或 `Different`（不同）。这很有用，因为相同的部分往往和变化的部分提供同样多的上下文。例如，如果两个 [MoE](https://sebastianraschka.com/glossary/#moe "Mixture of Experts (MoE)") 模型使用相同的规模和层配方，那么注意力上的改动就更容易被解读为一次有针对性的架构更新。

## DeepSeek V3 与 DeepSeek V3.2

DeepSeek V3 和 DeepSeek V3.2 是一个很好的实例。两者都有 6710 亿总参数，每个 token 激活 370 亿参数。它们共享 128,000 token 的上下文长度、稀疏 MoE 解码器、61 个 MLA 层，以及相同的每生成 token 68.6 KiB 逻辑 [bf16](https://sebastianraschka.com/glossary/#bfloat16 "bfloat16") KV 缓存估计。

在四条架构通道中，注意力模块是差异所在。DeepSeek V3 使用 [MLA](https://sebastianraschka.com/glossary/#mla "Multi-Head Latent Attention (MLA)")。DeepSeek V3.2 保留 MLA，并为长上下文处理增加了 [DeepSeek 稀疏注意力](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/)。把相同的字段放在这一改动旁边一起看，比单独阅读两份规格速览更有信息量。

目前的卡片还报告了不同的 AA Intelligence Index 结果。我把这些当作额外的背景信息，而不是"某个架构改动导致了分数差异"的证据。两个模型在发布时间和训练配方上也有差异，而图库对比并不是消融实验。

[![LLM Architecture Gallery 差异对比工具：DeepSeek V3 与 DeepSeek V3.2 的对比](https://sebastianraschka.com/images/blog/2026/llm-architecture-gallery-diff-tool/hero.webp)](https://sebastianraschka.com/llm-architecture-gallery/?compare=deepseek-v3,deepseek-v3-2#architecture-diff-tool)

图 1. DeepSeek V3 与 DeepSeek V3.2 在解码器类型、KV 缓存估计、层配方、规模和上下文长度上完全相同。注意力通道单独凸显出 [DeepSeek 稀疏注意力](https://sebastianraschka.com/glossary/#deepseek-sparse-attention "DeepSeek Sparse Attention")的新增。

## 选择与分享一组对比

你可以在工具顶部的两个选择器中挑选模型。另一种方式是使用各个图库卡片上的 `Model A` 和 `Model B` 按钮，这在浏览时发现有趣的模型时会很方便。`Swap` 按钮交换两栏位置，`Clear` 则重新开始。

选定的模型对会保存在页面 URL 中。因此复制地址即可把对比结果分享给他人。这个 [DeepSeek V3 与 V3.2 链接](https://sebastianraschka.com/llm-architecture-gallery/?compare=deepseek-v3,deepseek-v3-2#architecture-diff-tool)会打开上面展示的示例。

## 如何解读结果

这些标签来自图库规格速览中人工整理的字段。该工具不会检查模型权重，也不比较实现代码。在某字段上同被标为 `Shared` 的两个模型，仍可能在紧凑卡片未记录的更底层细节上存在差异。

KV 缓存数值也需要谨慎对待。它是基于已公开的缓存几何结构做出的逻辑 batch-size-1 bf16 估计，并不是对推理期间框架内存分配器占用的实测。`N/A` 表示公开报告或配置中没有提供足够信息来给出可靠条目。

做宏观对比时，我通常先看架构图和四条架构通道，然后再打开各个图库卡片，查看配置链接、技术报告，以及不熟悉机制背后的讲解页面。

来源：我的 [Substack note](https://substack.com/@rasbt/note/c-233727903) 的扩展网页版。
