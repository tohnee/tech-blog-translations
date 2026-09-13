---
title: "走进 LLM Architecture Gallery"
title_en: "Inside the LLM Architecture Gallery"
source: https://sebastianraschka.com/blog/2026/llm-architecture-gallery.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 走进 LLM Architecture Gallery

> 原文：[Inside the LLM Architecture Gallery](https://sebastianraschka.com/blog/2026/llm-architecture-gallery.html)

每当我研读一份新的模型报告，都会画架构图。它们帮助我回答具体的问题：有多少层使用完整注意力？专家混合（MoE）的路由发生在哪里？是不是每一层都会增加 [KV 缓存](https://sebastianraschka.com/glossary/#kv-cache "KV Cache")？

这些图在各自原文里很好用，但一旦分散在许多篇文章中，就变得难以查找。于是我搭建了 [LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/)，把它们集中放在一处。它最初收录的是 [The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison) 和 [A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight) 中的图，之后我陆续加入了来自新文章和独立技术报告的模型。

在本次更新时，图库收录了来自 42 篇源文章和报告的 93 张模型卡片。它涵盖常见的稠密架构（如 GPT-2 和 Llama 3）、近期的专家混合模型（如 DeepSeek V3 和 Kimi K2），以及把注意力与循环层或状态空间层相结合的混合架构。

[![LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/images/hero/architecture-gallery-hero.webp)](https://sebastianraschka.com/llm-architecture-gallery/)

图库中收录的部分架构图。点击图片可打开图库。

## 每张卡片包含什么

架构图是每张卡片的主体。点击它可打开高分辨率版本，通常比缩略图更易读。卡片还提供链接，指向我讨论该模型的具体文章章节。

下方的规格速览（fact sheet）汇总了我经常反复查找的细节，包括模型规模、上下文长度、[词表大小](https://sebastianraschka.com/glossary/#vocabulary-size "Vocabulary Size")、许可证、解码器类型、注意力机制以及层配方。当公开配置提供足够信息时，我还会给出每生成 token 的 KV 缓存增长的逻辑 batch-size-1 bf16 估计值。

对于被 Artificial Analysis 覆盖的模型，卡片会展示 AA Intelligence Index 及其 General、Scientific、Coding、Agents 分类画像。缺失的数据一律保持 `N/A` 标注——我更倾向于这样，而不是用无关来源的估计值来填补空白。

大多数卡片还包含公开的 `config.json`、技术报告，以及在有从零实现时提供相应实现链接。这样一来，你就可以从简化架构图直接过渡到底层配置，而不用再去搜索仓库。

## 对比两种架构

架构上的改动，放在直接对比中往往更容易看出来。图库的[差异对比工具](https://sebastianraschka.com/llm-architecture-gallery/#architecture-diff-tool)允许你选择两个模型，并把它们的架构图和规格速览字段并排展示。

DeepSeek V3 和 DeepSeek V3.2 就是一个有用的例子。两者的整体结构看起来相似，而注意力字段暴露出 V3.2 中新增的 [DeepSeek 稀疏注意力](https://sebastianraschka.com/glossary/#deepseek-sparse-attention "DeepSeek Sparse Attention")。同一视图也很适合对比同一家族内的稠密与 MoE 变体，或者检查两次发布之间层配方的变化。我还单独写过一篇[关于差异对比工具的短文](https://sebastianraschka.com/blog/2026/llm-architecture-gallery-diff-tool.html)，附有完整示例。

## 追查不熟悉的术语

由于版面空间有限，架构图使用了许多缩写。如果某张卡片提到了 GQA、MLA、滑动窗口注意力、NoPE、[KV 共享](https://sebastianraschka.com/glossary/#cross-layer-kv-sharing "Cross-Layer KV Sharing")或其他常见机制，相关的概念链接会带你进入一篇简短讲解。这些页面聚焦机制本身，并以具体模型作为示例。

图库还有两个跨模型汇总页面：[激活参数比例表](https://sebastianraschka.com/llm-architecture-gallery/active-parameter-ratio/)比较每个稀疏模型处理一个 token 时使用了多大比例的参数；[注意力机制分布](https://sebastianraschka.com/llm-architecture-gallery/attention-mechanism-distribution/)统计不同的注意力设计和层模式在整个图库中出现的频率。

## 范围与勘误

我聚焦于纯文本 LLM 以及多模态系统的语言模型主干。因此多模态发布的卡片描述的是其文本解码器，而不是视觉或音频组件。这些图是紧凑的阅读辅助，省略了许多不影响高层结构的训练细节和实现选择。

只要有新的技术报告和配置可用，我就会更新图库。这些更新有一个[变更日志](https://sebastianraschka.com/llm-architecture-gallery/changelog/)和一个专门的 [RSS feed](https://sebastianraschka.com/llm-architecture-gallery/rss.xml)。如果你发现错误的字段、标注错误的模块或失效的源链接，请使用[图库](https://sebastianraschka.com/llm-architecture-gallery/)页面顶部的 issue 链接反馈。
