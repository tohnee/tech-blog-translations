---
title: "注意力残差（AttnRes）"
title_en: "Attention Residuals (AttnRes)"
source: https://sebastianraschka.com/llm-architecture-gallery/attention-residuals/
crawled: 2026-09-06
translated: 2026-09-06
---

# 注意力残差（AttnRes）

> 原文：[Attention Residuals (AttnRes)](https://sebastianraschka.com/llm-architecture-gallery/attention-residuals/)

注意力残差（Attention Residuals）是一种改进残差路径的方法，但它的作用方式与近期其他针对残差路径的改动略有不同。[mHC](https://sebastianraschka.com/llm-architecture-gallery/mhc/) 把残差路径变宽了；而注意力残差（并且它已经被纳入 Kimi Linear）则是跨层连接残差，这种连接本身使用一个注意力分数作为重要性/贡献权重。

在常规 transformer 中，残差连接以贡献权重 1 累加此前所有的更新。注意力残差（简称 AttnRes）把这些固定权重替换为可学习的权重。[注意力残差论文](https://arxiv.org/abs/2603.15031)报告了在验证损失和下游性能上一致（但幅度不大）的提升，代价约为 4% 的训练开销和 2% 的推理开销。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[注意力残差论文](https://arxiv.org/abs/2603.15031)
[官方仓库](https://github.com/MoonshotAI/Attention-Residuals)

![标准残差与 Full 及 Block 注意力残差的对比](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/attention-residuals-overview.webp)

标准残差（左）、Full AttnRes（中）与 Block AttnRes（右）。Full AttnRes 在所有先前输出上学习权重；块版本在块内部保留常规加法，并在块表示之上执行注意力（原始出处
[Moonshot AI Attention Residuals 仓库](https://github.com/MoonshotAI/Attention-Residuals)）。

## 从固定求和到可学习权重

在标准 PreNorm transformer 中，第 \(l\) 个子层的输入是嵌入与此前所有注意力及前馈更新之和：

\[h\_l = \sum\_{i=0}^{l-1} v\_i\]

其中第一个值 \(v\_0\) 是 token 嵌入，此后的每个 \(v\_i\) 都来自更早的某个子层输出。AttnRes 使用同样的这些值，但学习每个值应当贡献多少：

\[h\_l = \sum\_{i=0}^{l-1} \alpha\_{i \rightarrow l} \cdot v\_i\]

在这里，较早的输出充当值（value），它们经 RMS 归一化后的版本充当键（key）。

如上图所示，每个权重的计算方式是：取归一化键与目标子层可学习伪查询（pseudo-query）之间的点积。然后沿模型深度方向对这些权重施加 softmax 函数进行归一化，得到归一化权重 \(\alpha\)。

最后一步就是计算 \(h\_l\)，它本质上是嵌入与较早子层输出的注意力加权版本。

对于给定的目标子层，伪查询在所有 token 之间共享。键仍然依赖于 token，因此权重依旧可以随 token 变化。零初始化的伪查询使得训练开始时所有可用输出都获得相同的权重。

## Full AttnRes 与 Block AttnRes

在常规自注意力中，权重连接的是输入序列中的各个位置；而 AttnRes 是在模型深度方向上，为同一个 token 混合较早子层的输出。常规的序列层，例如 [Kimi Delta Attention](https://sebastianraschka.com/llm-architecture-gallery/hybrid-attention/) 或 [MLA](https://sebastianraschka.com/llm-architecture-gallery/mla/)，保持不变。

Full AttnRes 会保留嵌入以及每一个较早子层的输出，这个列表随模型深度不断增长。Block AttnRes 则在每个块内部保留常规加法，只在块边界处存储一个表示。对于被划分为 \(N\) 个块的 \(L\) 个子层，每个 token 的存储量从 \(O(Ld)\) 降到 \(O(Nd)\)。大规模实验使用了大约 8 个块。

## 注意力残差与 mHC 的区别

两种方法都改动了残差路径，但作用在不同的轴上。

- 注意力残差：选择并组合来自较早深度的输出。
- mHC：在当前深度维护并混合多条残差流。

在注意力残差中，可学习的伪查询向量决定每个较早深度对当前表示的贡献程度。而在 [mHC](https://sebastianraschka.com/llm-architecture-gallery/mhc/) 中，模型在同一深度保留多条残差流，并学习这些流之间受约束的映射。

## 实验

完整规模的对比使用了两个 48B 模型，激活参数均为 3B。除残差连接外，两者拥有完全相同的架构和训练设置，并都在 1.4 万亿 token 上从零训练，其中包括 1 万亿预训练 token 和约 4000 亿更高质量的中期训练（mid-training）token。

![48B Kimi Linear 基线与 Block Attention Residuals 模型的训练动态](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/attention-residuals-kimi-linear-training-dynamics.webp)

前 1 万亿 token 上的训练动态（原始出处
[*Attention Residuals*](https://arxiv.org/abs/2603.15031)）。

在完成整套训练配方之后，Block AttnRes 在所有已报告的下游基准测试上都追平或超过了常规残差基线。

![Kimi Linear 基线与 Attention Residuals 模型的基准测试得分对比表](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/attention-residuals-kimi-linear-results.webp)

下游基准测试对比（原始出处
[*Attention Residuals*](https://arxiv.org/abs/2603.15031)）。

参考资料

[注意力残差论文](https://arxiv.org/abs/2603.15031)
[官方实现与图表](https://github.com/MoonshotAI/Attention-Residuals)
[Kimi Linear 论文](https://arxiv.org/abs/2510.26692)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
