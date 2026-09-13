---
title: "Kimi K3 架构笔记"
title_en: "Kimi K3 Architecture Notes"
source: https://sebastianraschka.com/blog/2026/kimi-k3-architecture-notes.html
crawled: 2026-09-06
translated: 2026-09-06
---

# Kimi K3 架构笔记

> 原文：[Kimi K3 Architecture Notes](https://sebastianraschka.com/blog/2026/kimi-k3-architecture-notes.html)

以下是昨天重磅开放权重模型发布的 Kimi K3 架构图，以及一些观察和想法。

1. 是的，它看起来相当复杂，但本质上就是他们去年发布的 [Kimi Linear 模型](https://sebastianraschka.com/llm-architecture-gallery/#card-kimi-linear-48b-a3b)的生产级放大版（从 48B 扩展到 2.8T；K3 是目前最大的开放权重模型）。
2. 相比 Kimi Linear 唯一的新组件是 [LatentMoE](https://sebastianraschka.com/llm-architecture-gallery/latent-moe/)。由于下图已经非常拥挤，我在图中省略了它，但它本质上与 Nemotron 3 Ultra 中的 LatentMoE 相同（如果你好奇，可以在我的 [LLM Architecture Gallery](https://sebastianraschka.com/llm-architecture-gallery/) 里找到）。其思路是像[多头潜在注意力](https://sebastianraschka.com/llm-architecture-gallery/mla/)那样，对大的线性层进行压缩（降投影）。
3. Kimi K3 的总体趋势（与 Nemotron 3、DeepSeek V4 等类似）也是朝着更好的推理效率迈进。也就是说，许多组件都被替换成了效率调优版本。即 [MoE](https://sebastianraschka.com/llm-architecture-gallery/moe/) → LatentMoE，常规注意力 → 多头潜在注意力和 [Kimi Delta Attention](https://sebastianraschka.com/llm-architecture-gallery/hybrid-attention/)。（如果你对更多细节好奇，我的[图库](https://sebastianraschka.com/llm-architecture-gallery/)里也有简短教程和文章。）
4. 唯一一个不属于效率调优的组件改动是[注意力残差](https://sebastianraschka.com/llm-architecture-gallery/attention-residuals/)（attention residuals）。就像 DeepSeek V4 用 mHC（manifold-constrained Hyper-Connections）改进了残差路径一样，注意力残差也是一种改进残差路径的方式，但工作原理略有不同。mHC 是把残差路径变宽；而注意力残差（同样已包含在 Kimi Linear 中）是跨层连接残差，且这个连接本身用一个注意力分数作为重要性/贡献权重。根据技术报告，它能一致地改善验证损失和下游性能（幅度不大），但会增加约 4% 的训练成本和 2% 的推理成本。
5. 有意思的是，Kimi K3 去掉了所有 RoPE 层，改为在所有地方使用 [NoPE](https://sebastianraschka.com/llm-architecture-gallery/nope/)（无位置嵌入）。（这同样继承自 Kimi Linear。）其他架构近期的趋势是在局部注意力层（如[滑动窗口注意力](https://sebastianraschka.com/llm-architecture-gallery/swa/)）中使用 RoPE，在全局层中使用 NoPE。此前有少数架构在所有地方只用 NoPE，但据我所知，这是第一个达到前沿级别的。
6. Kimi K3 现在还支持原生多模态，这非常棒！

技术报告里还有几个其他有趣的训练细节，但架构方面目前就这些了。总体而言是一次非常出色的发布。

![Kimi K3 组合架构图：包含 Kimi Delta Attention、带门控的多头潜在注意力、注意力残差、LatentMoE 以及基准测试对比](https://sebastianraschka.com/images/blog/2026/kimi-k3-architecture-notes/kimi-k3-architecture.webp)

图 1. Kimi K3 架构与发布时基准测试对比。更多细节请见架构图库中的 [K3](https://sebastianraschka.com/llm-architecture-gallery/#card-kimi-k3)。

来源：我的 [Substack note](https://substack.com/@rasbt/note/c-303378576) 的网页版。
