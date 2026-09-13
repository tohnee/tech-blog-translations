---
title: "逐层嵌入（PLE）"
title_en: "Per-Layer Embeddings (PLE)"
source: https://sebastianraschka.com/llm-architecture-gallery/per-layer-embeddings/
crawled: 2026-09-06
translated: 2026-09-06
---

# 逐层嵌入（PLE）

> 原文：[Per-Layer Embeddings (PLE)](https://sebastianraschka.com/llm-architecture-gallery/per-layer-embeddings/)

Gemma 4 E2B 和 E4B 版本包含第二个面向效率的设计选择，称为逐层嵌入（per-layer embeddings，PLE）。它与[跨层 KV 共享](https://sebastianraschka.com/llm-architecture-gallery/kv-sharing/)方案是相互独立的。

KV 共享减小的是 KV 缓存；而 PLE 关注的是参数效率：它让小型 Gemma 4 模型能够利用更多 token 专属的信息，同时又不必让主 transformer 堆叠变得像同等总参数量的稠密模型那样昂贵。

举例来说，Gemma 4 E2B 和 E4B 中的"E"代表"有效（effective）"。具体而言，Gemma 4 E2B 标称 2.3B 有效参数；若把嵌入计算在内则为 5.1B 参数。类似地，Gemma 4 E4B 标称 4.5B 有效参数；含嵌入则为 8B 参数。

简而言之，在"E"系列模型中，主 transformer 堆叠的计算量更接近较小的那个数字，而较大的数字则包含了额外的嵌入表层。

从概念上看，新增的 PLE 路径如下所示。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[文章章节](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A72-per-layer-embeddings-and-effective-size-gemma-4-e2be4b)
[从零实现代码](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch05/17_gemma4)

![带逐层嵌入残差路径的简化 Gemma 4 块](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gemma4-ple-residual-path.webp)

图 6：带 PLE 残差路径的简化 Gemma 4 块。常规块先计算注意力
和前馈残差更新。所得的隐藏状态对层专属的 PLE 向量进行门控，
投影后的 PLE 更新作为额外的残差更新加在块末尾。

## PLE 路径的工作方式

PLE 向量本身是在重复的 transformer 块之外准备的。首先，token ID 经过一次逐层嵌入查找；其次，常规的 token 嵌入经过一次线性投影进入同一个打包的 PLE 空间。这两部分相加、缩放，并重塑成一个每层对应一个切片的张量。

在 transformer 块内部，常规的注意力和前馈分支照常运行。所得的隐藏状态对层专属的 PLE 向量进行门控。该向量随后被投影回模型隐藏尺寸，做归一化，并作为一个额外的残差更新加入。

![Gemma 4 逐层嵌入的简化构建方式](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/gemma4-ple-construction.webp)

图 7：token ID 提供逐层嵌入查找，而常规的
token 嵌入则被投影进同一空间。两路贡献被组合并重塑，
使每个 transformer 块都收到自己专属的 PLE 切片。

## 为什么要用 PLE？

这一点我们只能听 Google 自己的话：这是一个有效且值得的设计选择。如果能看到 E2B 与一个常规 2.3B 模型和一个常规 5.1B 模型的对比，会很有意思。

另外，PLE 并非天生只限于小模型。我们同样可以把逐层嵌入切片挂到更大的模型上。不过，较大的模型可能已经有足够的容量，这些额外的嵌入帮助不大。对更大的模型来说，我们还有 MoE 设计这条路：在保持计算足迹较小的情况下增加容量。

顺带一提，如果你对一个相对简单、易读的代码实现感兴趣，我在[这里](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch05/17_gemma4)从零实现了 Gemma 4 E2B 和 E4B 模型。

参考资料

[Recent Developments in LLM Architectures](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A72-per-layer-embeddings-and-effective-size-gemma-4-e2be4b)
[Gemma 4 模型卡](https://ai.google.dev/gemma/docs/core/model_card_4)
[LLMs-from-scratch Gemma 4 材料](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch05/17_gemma4)
[嵌入层与线性层对比笔记本](https://github.com/rasbt/LLMs-from-scratch/blob/main/ch02/03_bonus_embedding-vs-matmul/embeddings-and-linear-layers.ipynb)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
