---
title: "CSA 与 HCA"
title_en: "CSA and HCA"
source: https://sebastianraschka.com/llm-architecture-gallery/csa-hca/
crawled: 2026-09-06
translated: 2026-09-06
---

# CSA 与 HCA

> 原文：[CSA and HCA](https://sebastianraschka.com/llm-architecture-gallery/csa-hca/)

压缩稀疏注意力（Compressed Sparse Attention, CSA）与重度压缩注意力（Heavily Compressed Attention, HCA）通过缩短存储的历史来降低长上下文成本。它们把较早的一组组 token 池化为更少的键值（KV）条目。注意力层随后需要存储和处理的过去条目也随之减少。

这两种机制以不同的压缩率工作，并使用不同的查找策略。CSA 保留更多条目，并以稀疏选取的方式读取；HCA 把历史压缩得更短，并读取其全部压缩条目。[DeepSeek V4](https://arxiv.org/abs/2606.19348) 将两种方式结合在一起，支持最长一百万 token 的上下文长度。

这种序列压缩是对[多头潜在注意力（MLA）](https://sebastianraschka.com/llm-architecture-gallery/mla/)的补充。MLA 让每个 token 缓存的表示变小，但仍为每个 token 保留一个潜在条目；CSA 和 HCA 则进一步减少序列轴上的条目数量。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[文章章节](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A752-compressed-attention-via-csa-and-hca)
[DeepSeek V4 报告](https://arxiv.org/abs/2606.19348)
[MLA 讲解文章](https://sebastianraschka.com/llm-architecture-gallery/mla/)

![MLA 风格缓存、CSA 与 HCA 的概念对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/deepseek-v4-csa-hca-cache-comparison.webp)

图 1. MLA 使每个 token 存储的表示变小，CSA 与 HCA 还缩短了存储条目的序列长度。CSA 将中等压缩与稀疏 top-k 选取相结合，而 HCA 将更强的压缩与对所得缓存的稠密注意力相结合。（原始出处：[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)）。

变化点

较早的 token 被汇总为更少的压缩 KV 条目

实际收益

长上下文缓存变短，降低内存与注意力开销

示例架构

[DeepSeek V4-Pro](https://sebastianraschka.com/llm-architecture-gallery/#card-deepseek-v4-pro) 与
[DeepSeek V4-Flash](https://sebastianraschka.com/llm-architecture-gallery/#card-deepseek-v4-flash)

## 压缩序列轴

在本文语境下，KV 缓存有两个相关尺寸：一个是每个 token 所存表示的宽度，另一个是缓存中保留的 token 位置数量。MLA 主要解决前者，CSA 和 HCA 解决后者。

假设模型已处理完一篇长文档。传统缓存会为每个较早的 token 分配独立条目；采用序列压缩后，相邻的一块 token 会被合并为一个压缩条目。这会损失一部分细粒度历史，但直接缩短了缓存长度，也减少了注意力计算时需要考虑的位置数量。

DeepSeek V4 在两个尺度上应用这一思路：CSA 每 4 个 token 位置压缩为一个条目，再由 top-k 索引器从中稀疏选取一部分条目参与注意力；HCA 每 128 个位置压缩为一个条目，由于留下的历史远短得多，该层可以对全部压缩条目做稠密注意力。

![CSA 的稀疏选取与 HCA 对压缩历史的稠密注意力](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/deepseek-v4-csa-hca-attention-paths.webp)

图 2. CSA 从压缩历史块中稀疏选取一组；HCA 对一组数量更少、压缩程度更高的块做稠密注意力。两种机制都保留一个 128-token 的局部窗口，其中近期 token 使用未压缩的 KV 条目。（原始出处：[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)）。

## 为什么要两种压缩率？

CSA 保留了较旧上下文中相对细粒度的版本，其稀疏查找控制了搜索这段历史的开销；HCA 保留的摘要粗得多，从而使稠密注意力变得可行。两条路径让模型能够以不同的分辨率访问同一段长序列。

近期 token 单独处理：两种机制都包含一个 128-token 的局部窗口，其中保存未压缩的 KV 条目。因此模型可以在 token 级分辨率上检视最新的上下文，同时对远距离文本使用压缩摘要。

DeepSeek V4 在整个网络中交错部署 CSA 与 HCA 层，避免让每一层都在“保留细节”与“注意力开销”之间采用同一种权衡。

![DeepSeek V4 报告的 1M 上下文 FLOP 与 KV 缓存节省](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/deepseek-v4-csa-hca-efficiency.webp)

图 3. DeepSeek V4 论文报告的 1M 上下文效率数据（以 DeepSeek V3.2 为基准）：DeepSeek V4-Pro 的单 token 推理 FLOPs 为 27%，KV 缓存大小为 10%；DeepSeek V4-Flash 的 FLOPs 为 10%，KV 缓存大小为 7%。（原始出处：[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)）。

## 各组件如何配合

DeepSeek V4 将序列压缩与 MLA 风格的紧凑表示以及共享 KV 注意力结合在一起。画廊将这一组合简称为“MLA 风格的 CSA/HCA”。MLA 减小每个条目的大小，CSA/HCA 减少保留下来的历史条目数量。

CSA/HCA 属于注意力机制；[流形约束超连接（Manifold-Constrained Hyper-Connections, mHC）](https://sebastianraschka.com/llm-architecture-gallery/mhc/)处理的是模型的另一部分——它改变信息在注意力与专家混合（MoE）子层周围的残差路径中的流动方式。

## 效率与局限

在一百万 token 的上下文长度下，DeepSeek V4 报告将两个模型变体与 DeepSeek V3.2 进行对比：在该对比中，DeepSeek V4-Pro 使用 27% 的单 token 推理 FLOPs 和 10% 的 KV 缓存大小；DeepSeek V4-Flash 对应的数据为 10% 和 7%。

这些节省有明确的代价：较早的文本通过压缩块来表示，部分 token 级细节会消失。HCA 的权衡更为尖锐，因为每个条目概括的块要大得多。

我建议把报告的效率数值理解为整模型层面的结果。DeepSeek V4 还同时改变了训练数据、优化方法、残差连接、数值精度与系统实现。该对比展示的是完整设计所取得的成果，并未单独剥离出 CSA 或 HCA 各自贡献了多少收益。

来源

[Recent Developments in LLM Architectures](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A752-compressed-attention-via-csa-and-hca)
[DeepSeek V4 技术报告](https://arxiv.org/abs/2606.19348)
[MLA 讲解文章](https://sebastianraschka.com/llm-architecture-gallery/mla/)
[DeepSeek Sparse Attention 讲解文章](https://sebastianraschka.com/llm-architecture-gallery/deepseek-sparse-attention/)
[A Visual Guide to Attention Variants](https://magazine.sebastianraschka.com/p/visual-attention-variants)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
