---
title: "PolyNorm"
title_en: "PolyNorm"
source: https://sebastianraschka.com/llm-architecture-gallery/polynorm/
crawled: 2026-09-06
translated: 2026-09-06
---

# PolyNorm

> 原文：[PolyNorm](https://sebastianraschka.com/llm-architecture-gallery/polynorm/)

PolyNorm 是一种可训练的激活函数，它把同一个预激活值分别归一化后的线性、二次与三次变换混合在一起。在 [Motif 3 Beta](https://sebastianraschka.com/llm-architecture-gallery/#card-motif-3-beta) 中，它替换了常规 SwiGLU 风格前馈模块中的 SiLU 部分。

[架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
[PolyCom 论文](https://arxiv.org/abs/2411.03884)
[PolyCom 代码](https://github.com/BryceZhuo/PolyCom)
[Motif 3 Beta 模型](https://huggingface.co/Motif-Technologies/Motif-3-Beta)

![SwiGLU 对其门投影施加固定的 SiLU 激活，而 PolyNorm 学习分别做 RMS 归一化的线性、二次与三次项的混合](https://sebastianraschka.com/llm-architecture-gallery/images/concepts/polynorm-gated-ffn.webp)

SwiGLU 在门分支上使用固定的 SiLU 函数；PolyNorm 则学习三个混合系数和一个偏置，同时保持周边投影矩阵不变。

## 从 GELU 到 PolyNorm 的演进

早期 GPT 架构使用 GELU。为什么现在用 Swish 而不是 GELU？Swish（也称为 sigmoid 线性单元，即 SiLU）被认为在计算上稍微便宜一点，在我看来原因仅此而已。我认为这两种函数之间报告的性能差异太小，不足以推广；它们大概在标准误差范围之内，实际效果会因超参数敏感性而异。

激活函数曾经是热烈争论的话题，直到十多年前深度学习社区大体上固定使用 ReLU。此后，研究者提出并尝试了许多曲线更平滑的 ReLU 类变体，最终留下来的是 GELU 和 Swish。

早期 GPT 架构使用 GELU，其定义为 `0.5x * [1 + erf(x / sqrt(2))]`。这里的 `erf`（误差函数的缩写）是高斯函数的积分，需要用高斯积分的多项式近似来计算，因此它比 Swish 中使用的 sigmoid 这类更简单的函数计算开销更大，而 Swish 就是简单的 `x * sigmoid(x)`。

在实践中，Swish 的计算比 GELU 稍便宜，这大概是它在多数较新模型中取代 GELU 的主要原因。我不会仅凭建模表现上的微小差异在两者之间做选择；可以说这些收益往往在标准误差范围之内，胜负将在很大程度上取决于超参数调优。

如今大多数架构使用 Swish。不过 GELU 并没有被完全遗忘，例如 Google 的 Gemma 模型仍在使用 GELU。

更值得注意的是，前馈模块（一个小型多层感知机）被替换为带门的“GLU”对应版本，其中 GLU 指门控线性单元（gated linear unit），由一篇 [2020 年论文](https://arxiv.org/abs/2002.05202)提出。具体而言，两个全连接层被替换为三个全连接层。

乍看之下，GEGLU/SwiGLU 变体似乎比常规前馈层更好，因为额外的层带来了更多参数。但这是有迷惑性的：实践中，SwiGLU/GEGLU 中的 `W` 和 `V` 权重层通常各自只有传统前馈层中 `W_1` 层的一半大小。

SwiGLU 对门分支施加 SiLU。PolyNorm 用一个学习得到的混合替换这个固定函数，同时保持 gate、up 和 down 投影的尺寸不变。设 `g = W_gate h`、`u = W_up h`，SwiGLU 风格的模块计算

```python
output = W_down(SiLU(g) ⊙ u)
```

Motif 只改变门分支上的激活：

```python
output = W_down(s · PolyNorm(g) ⊙ u)
```

## 归一化多项式

PolyNorm 先构造 `x`、`x²` 和 `x³`，并对每一项分别做 RMS 归一化：

```python
norm(z) = z / sqrt(mean(z²) + ε)
```

然后混合三个归一化后的幂次项：

```python
PolyNorm(x) = a₃ · norm(x³) + a₂ · norm(x²) + a₁ · norm(x) + b
```

三个可学习的系数混合这些项，一个可学习的偏置平移结果。分开归一化很重要，因为它防止三次项更大的原始量级直接决定其重要性。

Motif 对系数参数施加 sigmoid，把偏置限制在正负 0.5 之间，并将激活乘以 0.5。这些稳定化选择属于 Motif 的实现细节，而非 PolyNorm 的一般定义。

## Motif 3 Beta 中的分组 PolyNorm

Motif 3 Beta 有 384 个路由专家，每个 token 选出 8 个。每个路由专家拥有自己的三个 PolyNorm 系数和一个偏置。这为每个 MoE 层增加 1536 个标量，与投影矩阵相比微不足道。发布的激活函数包为专家专属计算提供了一个分组 CUDA 算子。

![Motif 3 Beta 架构图，展示其专家混合前馈模块内部的 Grouped PolyNorm](https://sebastianraschka.com/llm-architecture-gallery/images/architectures/motif-3-beta.webp)

Motif 3 Beta 在门控乘法之前，于每个被选中的专家中应用各自独立的 Grouped PolyNorm 参数。

## 证据与成本

[PolyCom 论文](https://arxiv.org/abs/2411.03884)测试了稠密的 1B 模型和稀疏的 7B-A1B 模型。其多项式激活比所测试的固定激活改善了验证损失和困惑度。三阶与四阶变体的收敛情况相近，因此三次形式是更便宜的实际选择。

额外的参数可以忽略不计，但逐元素计算并非免费。PolyNorm 需要计算三个幂次和三次 RMS 归一化。它并不能减少 MoE 层中的大型矩阵乘法，因此要高效使用，有赖于融合 kernel。

来源

[Polynomial Composition Activations 论文](https://arxiv.org/abs/2411.03884)
[PolyCom 参考代码](https://github.com/BryceZhuo/PolyCom)
[Motif 模型实现](https://huggingface.co/Motif-Technologies/Motif-3-Beta/blob/main/modeling_motif.py)
[Motif 模型配置](https://huggingface.co/Motif-Technologies/Motif-3-Beta/blob/main/config.json)
[Motif 激活函数 kernel](https://huggingface.co/Motif-Technologies/activation)

[返回架构画廊](https://sebastianraschka.com/llm-architecture-gallery/)
