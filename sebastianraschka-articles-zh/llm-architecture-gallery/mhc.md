---
title: "流形约束超连接"
title_en: "Manifold-constrained hyper-connections"
source: https://sebastianraschka.com/llm-architecture-gallery/mhc/
crawled: 2026-09-06
translated: 2026-09-06
---

# 流形约束超连接

> 原文：[Manifold-constrained hyper-connections](https://sebastianraschka.com/llm-architecture-gallery/mhc/)

流形约束超连接（Manifold-constrained hyper-connections，mHC）改变的是 transformer 块内部的残差连接。它把单一残差流替换为多条并行的残差流以及它们之间可学习的映射，并对这些映射加以约束，以保持信号混合的稳定。

这要追溯到 DeepSeek 团队于 2025 年 12 月 31 日发布的一篇研究论文。不过在那篇论文中，该技术只在一个实验性的 27B 规模模型上做过测试。如今我们看到了它出现在他们的旗舰发布中，这是一个好迹象，说明这个想法在生产环境中确实行之有效。

mHC 背后的主要思想，是对 transformer 块内部残差连接的设计进行现代化改造，这一点令人耳目一新，因为架构上的改动通常都集中在注意力机制、归一化层的位置以及 MoE 部分上。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[门控残差](https://sebastianraschka.com/llm-architecture-gallery/gated-residuals/)
[文章章节](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A751-manifold-constrained-hyper-connections-mhc)
[mHC 论文](https://arxiv.org/abs/2512.24880)
[超连接论文](https://arxiv.org/abs/2409.19606)

![带有 mHC 混合器的 DeepSeek V4-Pro 架构](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/deepseek-v4-mhc-architecture.webp)

图 17. DeepSeek V4-Pro 把 mHC 混合器布置在注意力和 MoE 子层周围。该模型使用
4 条并行残差流，同时让注意力和 MoE 子层保持在正常的隐藏宽度上
（原始出处：
[*Recent Developments in LLM Architectures*](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures)。）

## 从残差连接到超连接

mHC 建立在 Zhu 等人 2024 年超连接（hyper-connections）工作的基础上。超连接的本质，是改造 transformer 块内部的单条残差流：用多条并行残差流以及它们之间的可学习映射来替换它。

（如果你还不熟悉残差连接，我很多年前做过一个[关于残差神经网络的视频](https://www.youtube.com/watch?v=q_IlqYlYhlo)，其中解释了它的总体机制。）

超连接的思想是拓宽残差流。我们可以把它理解为：保留多条并行的残差流，并额外引入一个 Res Mapping 线性变换，跨层混合这些流。由于注意力层或 MoE 层本身仍在正常的隐藏尺寸上运行，超连接还加入了一个 Pre Mapping，把并行残差流合并成该层所需的一个正常隐藏向量；以及一个 Post Mapping，把该层的输出分配回各条并行残差流。

![常规 transformer 块与使用超连接的 transformer 块的对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mhc-hyper-connections.webp)

图 18. 常规 transformer 块与使用超连接的 transformer 块的对比。Pre Mapping
从拓宽后的状态读取，子层在正常宽度上运行，Post Mapping 把输出写回
拓宽后的状态（原始出处：
[*mHC: Manifold-Constrained Hyper-Connections*](https://arxiv.org/abs/2512.24880)。）

图中聚焦的是 transformer 块中注意力层的部分，但同样的概念也适用于围绕 MoE 层的第二条残差分支。

超连接的目的，是在不把实际的注意力层或 MoE 层加宽的前提下，让残差通路更有表达力。它在 FLOPs 上只带来轻微的额外开销，因为这些额外的映射是在很小的残差流维度上运算的（例如 DeepSeek V4 中 n = 4），而不是在巨大的隐藏维度上。

在原始的超连接论文中，7B OLMo MoE 实验的每 token FLOPs 从 13.36G 变为 13.38G，基本没有变化。至于报告的收益，则是温和（但一致）的提升。

（不过，只看 FLOPs 有点过于简化。拓宽后的残差状态仍然需要被存储、在内存中搬运、混合等。因此实际开销更多可能来自内存流量和实现复杂度，而不是算术运算，这一点并未被明确测量。）

## 注意力残差与 mHC 的区别

两种方法都改动了残差路径，但方向不同。

- 注意力残差：选择并组合来自较早深度的输出。
- mHC：在当前深度维护并混合多条残差流。

[注意力残差](https://sebastianraschka.com/llm-architecture-gallery/attention-residuals/)对同一个 token 的较早子层输出使用可学习的注意力权重；mHC 则在当前深度保留多条残差流，并对这些流之间交换信息的方式加以约束。

## 流形约束带来了什么

从常规超连接（HC）到流形约束超连接（mHC）的主要变化，是这些映射不再被放任不管。在常规 HC 中，Res Mapping 是一个混合并行残差流的可学习矩阵，但堆叠许多这样的矩阵可能会不可预测地放大或缩小信号。

在 mHC 中，这个残差映射被投影到双随机矩阵（doubly stochastic matrices）的流形上，也就是说所有元素都非负，且每行每列的和都为 1。这使得残差混合的行为更像是一种跨流稳定的信息重新分配。Pre Mapping 和 Post Mapping 也被约束为非负有界，以避免在从拓宽的残差状态读取和写回时发生相互抵消。

![超连接与流形约束超连接的对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/mhc-manifold-constraint.webp)

图 20. mHC 保留了超连接的并行残差流，但对流间混合权重施加了约束。Res Mapping 变为双随机矩阵，而 Pre Mapping 与 Post Mapping 则是有界且非负的（原始出处：
[*mHC: Manifold-Constrained Hyper-Connections*](https://arxiv.org/abs/2512.24880)。）

在 mHC 论文中，DeepSeek 团队用 27B 参数模型做实验，其优化后的实现（包含融合、重计算和流水线调度）在整个 transformer 块中使用 4 条残差流（n = 4）的情况下，相对单流基线只增加了 6.7% 的额外训练时间开销。

总结一下，HC/mHC 通过把单一残差流替换为多条相互作用的残差流（mHC 还额外施加了稳定性约束），改变了信息在这些层之间被传递的方式。它与 CSA/HCA 注意力改动相互搭配，后者改变的是 transformer 块的其他部分。

参考资料

[Recent Developments in LLM Architectures](https://magazine.sebastianraschka.com/p/recent-developments-in-llm-architectures#%C2%A751-manifold-constrained-hyper-connections-mhc)
[mHC 论文](https://arxiv.org/abs/2512.24880)
[超连接论文](https://arxiv.org/abs/2409.19606)
[DeepSeek V4 技术报告](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/DeepSeek_V4.pdf)
[DeepSeek V4-Pro config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro/blob/main/config.json)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
