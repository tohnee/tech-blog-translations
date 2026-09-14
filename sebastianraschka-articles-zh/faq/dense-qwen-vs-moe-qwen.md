---
title: "稠密 Qwen 与专家混合（MoE）Qwen 模型"
title_en: "Dense Qwen vs. Mixture-of-Experts Qwen Models"
source: https://sebastianraschka.com/faq/docs/dense-qwen-vs-moe-qwen.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 稠密 Qwen 与专家混合（MoE）Qwen 模型

> 原文：[Dense Qwen vs. Mixture-of-Experts Qwen Models](https://sebastianraschka.com/faq/docs/dense-qwen-vs-moe-qwen.html) · Sebastian Raschka's FAQ

**稠密 Qwen 模型**与**专家混合（MoE）Qwen 模型**的区别主要在每个 transformer 块的前馈部分。注意力层和整体解码器结构可以保持相似。

在稠密模型中，每个 token 都经过同一个前馈模块。该模块中的全部权重都参与每个 token 的计算。这使模型的执行模式很规整，参数量也相对容易解读。

MoE 层存储多个前馈模块（称为专家），外加一个路由器。路由器把每个 token 分配给其中一小部分专家。未被该 token 选中的专家不参与它的前馈计算。

![仓库中的 Qwen 概览表明该系列同时包含稠密与 MoE 两种变体，而非单一的架构形式](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/qwen/qwen-overview.webp)

Qwen3 让命名规则变得具体。其最初系列既包括参数量从 0.6B 到 32B 的稠密检查点，也包括 Qwen3 30B-A3B 和 Qwen3 235B-A22B 两款 MoE 模型。在 `30B-A3B` 中，30B 指大致的总参数量，A3B 表示单个 token 大约有 3B 参数处于激活状态。第二个数字是对激活参数量的估计，而不是存储在内存中的检查点大小。

这种分离让 MoE 模型可以在不把每个 token 的计算量按同一倍数放大的情况下，增加专家总容量。但它仍须加载或分布全部专家权重。因此，一个 30B-A3B 检查点所需的内存要与其总权重相称，尽管它每个 token 的算术运算量更接近于激活的那部分子集。

![仓库中的 MoE 示意图解释了其底层机制：存储很多专家，但路由让 token 级计算保持稀疏](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/moe-memory/1.webp)

激活参数数也只是对成本的一种近似，因为注意力、嵌入、路由以及模型的其他共享部分始终处于激活状态。实际速度取决于具体实现。专家路由可能带来设备间通信、专家负载不均衡以及不太方便的内存访问。好的 MoE 内核和专家并行在实践中非常重要。

对于本地部署或直接微调，我通常认为稠密模型更好上手。当可用硬件能装下全部专家权重、且推理服务栈能高效处理稀疏路由时，MoE 模型就变得有吸引力了。它以更低的激活计算预算提供更大的总参数容量，代价是额外的部署复杂度。

两种变体都仍然是纯解码器（decoder-only）transformer。架构上的变化主要局限在前馈模块：稠密计算被替换为依赖 token 的专家路由。
