---
title: "潜在 MoE"
title_en: "Latent MoE"
source: https://sebastianraschka.com/llm-architecture-gallery/latent-moe/
crawled: 2026-09-06
translated: 2026-09-06
---

# 潜在 MoE

> 原文：[Latent MoE](https://sebastianraschka.com/llm-architecture-gallery/latent-moe/)

潜在 MoE（Latent MoE）在更小的潜在空间中运行被路由的前馈专家。它仍然是一个稀疏专家混合（[MoE](https://sebastianraschka.com/llm-architecture-gallery/moe/)）层：路由器为每个 token 挑选少数几个专家，也只有这些专家处理该 token。Nemotron 3 和 Kimi K3 使用了不同的压缩比，但都采用这一基本布局。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[MoE 从零实现材料](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/07_moe)

![展示潜在 MoE 层的 Nemotron 3 Super 架构](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/latent-moe-nemotron-super.webp)

图 1. Nemotron 3 Super 120B-A12B 将潜在 MoE 与多 token 预测以及混合
Mamba-Transformer 堆叠结合在一起。被路由的专家在 4096 到 1024 的投影之后运行
（原始出处：
[*The Big LLM Architecture Comparison*](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)。）

基本思想

让被选中的专家在更窄的潜在空间中运行

压缩比

Nemotron 3：4 倍  
Kimi K3：2 倍

示例架构

[Nemotron 3 Super 120B-A12B](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-super-120b-a12b)  
[Nemotron 3 Ultra 550B-A55B](https://sebastianraschka.com/llm-architecture-gallery/#card-nemotron-3-ultra-550b-a55b)  
[Kimi K3](https://sebastianraschka.com/llm-architecture-gallery/#card-kimi-k3)

## 从常规 MoE 到潜在 MoE

MoE，即专家混合（Mixture of Experts），是一种集成模型：它在类 GPT 的解码器架构内部组合了多个较小的"专家"子网络，由路由器把每个 token 分配给这些专家的一个子集。其思路是，用多个较小的子网络替代一个大网络，从而更高效地分配计算资源。

"稀疏 MoE"中的"稀疏"指的是：在任一时刻，只有一部分专家层被实际用于处理某个 token。

在常规 MoE 层中，被路由的专家直接在模型宽度上运行。而在潜在 MoE 中，被路由的路径先被向下投影到一个更小的潜在空间，专家在那里运行，结果再被向上投影回来。

路由与潜在瓶颈影响的是计算的不同部分：路由控制运行多少个专家，瓶颈控制被选中的专家在多宽的维度上运行。投影层本身也要消耗计算，因此 4 倍更窄的潜在空间并不意味着整个模型有 4 倍的加速。

## Nemotron 3 中瓶颈的扩展

我觉得最有意思的部分，是 Nemotron 3 Super 中引入的潜在 MoE 思想。

对 Super 来说，这条路径是 `4096 -> 1024 -> 4096`；对 Ultra 则是 `8192 -> 2048 -> 8192`。

也就是说，4 倍的压缩比保持不变，但模型整体被大幅放大。Super 的总参数为 120B、激活参数 12B；Ultra 则增长到总参数 550B、激活参数 55B，同时保持了相同的瓶颈比例。

## Kimi K3 的 Stable LatentMoE

相比 Kimi Linear，新增的组件就是 LatentMoE。在 Kimi K3 的总览图中我省略了它，因为图已经非常拥挤，但它本质上与 Nemotron 3 Ultra 中的想法相同：像[多头潜在注意力](https://sebastianraschka.com/llm-architecture-gallery/mla/)那样，把大的线性层压缩（向下投影）。

Kimi K3 使用 `7168 -> 3584 -> 7168` 的路径，把宽度减半，形成 2 倍的瓶颈，而不是 Nemotron 的 4 倍。Moonshot 把它称为 Stable LatentMoE。它还在向上投影之前施加 RMSNorm，使用 SiTU-GLU 激活函数，并通过 Quantile Balancing 把每个 token 路由到 896 个专家中的 16 个。

参考资料

[The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
[LLMs-from-scratch MoE 章节](https://github.com/rasbt/LLMs-from-scratch/tree/main/ch04/07_moe)
[Nemotron 3 Ultra 说明](https://sebastianraschka.com/blog/2026/nemotron-3-ultra-latent-moe.html)
[Kimi K3 技术报告](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
