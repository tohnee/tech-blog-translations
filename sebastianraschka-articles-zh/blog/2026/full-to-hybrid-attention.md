---
title: "LLM 从完整注意力走向混合注意力"
title_en: "From Full to Hybrid Attention in LLMs"
source: https://sebastianraschka.com/blog/2026/full-to-hybrid-attention.html
crawled: 2026-11-16
translated: 2026-11-16
---

# LLM 从完整注意力走向混合注意力

> 原文：[From Full to Hybrid Attention in LLMs](https://sebastianraschka.com/blog/2026/full-to-hybrid-attention.html) · Sebastian Raschka's Blog

目前我正在准备一篇更大的开放 LLM 汇总文章。不过在此之前，先说一个很突出的有趣趋势：从完整注意力（full attention）向混合注意力（hybrid attention）的转变似乎仍在继续。

2025 年，仍有大量完整注意力模型，同时开始转向「部分完整注意力」的混合模型。

2026 年上半年，向「部分完整注意力」混合模型发展的趋势仍在延续。

而到了 2026 年下半年，「部分完整注意力」混合模型与完全不再使用完整注意力的模型已经各占一半。是的，完整注意力模型也已经没有了。

这里的图例含义是：

* Full attention throughout（全程完整注意力）= 每一层都是 Global MHA、GQA、稠密 MLA、CCA。
* Some full attention（部分完整注意力）= 全局长注意力与以下机制混合：sliding-window/chunked attention、Gated DeltaNet、KDA、Mamba-2、Lightning Attention、卷积、稀疏注意力。
* No full attention（无完整注意力）= 没有任何稠密全局层。

主要含义是，这一趋势正朝着降低长上下文使用成本的方向发展。这意味着这些架构更适合长文档与长对话、大型代码库，当然也适合依赖大量工具调用的智能体用例。

具体来说，这里有两项不同的效率收益：

1. 注意力计算更少：稀疏注意力等方法会从上下文中选取 token 或块，只在选出的子集上执行昂贵的注意力运算。（注意，它仍然可以从远处位置检索信息。）
2. 在某些架构中，保留上下文所需的内存更少：Gated DeltaNet 这类循环层维护固定大小的状态。当然，这节省了内存，但压缩历史会给精确检索带来挑战，因此它们通常会与传统注意力方法（稀疏或完整）交错使用。

[![Mistral Small 4、Kimi K3 与 MiniMax-M3.1-Flash 的架构图，上方是堆叠柱状图，比较三组模型发布中完整注意力的覆盖比例](/images/blog/2026/full-to-hybrid-attention/full-to-hybrid-attention.webp)](/images/blog/2026/full-to-hybrid-attention/full-to-hybrid-attention.png)

全程完整注意力、部分完整注意力与无完整注意力模型的比例，并附有来自 [LLM Architecture Gallery](/llm-architecture-gallery/) 的架构示例。点击图片查看全分辨率版本。

来源：我的 [Substack note](https://substack.com/@rasbt/note/c-383850419) 的网页版，略有编辑。
