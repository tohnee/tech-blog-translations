---
title: "Transformer 家族 2.0 版"
title_en: "The Transformer Family Version 2.0"
source: https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/
crawled: 2026-09-08
translated: 2026-09-08
---

# Transformer 家族 2.0 版

> 原文：[The Transformer Family Version 2.0](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/) · Lilian Weng（翁荔）

自我大约三年前写下[《Transformer 家族》](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/)一文以来，人们又提出了许多新的 Transformer 架构改进。本文对那篇 2020 年的博文做了一次大规模的重构与充实——重新组织了章节层级，并用更多新近的论文完善了许多小节。2.0 版是旧版的一个超集，篇幅约为旧版的两倍。

# 符号

| 符号 | 含义 |
| --- | --- |
| $d$ | 模型尺寸 / 隐藏状态维度 / 位置编码尺寸。 |
| $h$ | 多头注意力层中的头数。 |
| $L$ | 输入序列的片段长度。 |
| $N$ | 模型中注意力层的总数；不考虑 MoE。 |
| $\mathbf{X} \in \mathbb{R}^{L \times d}$ | 输入序列，其中每个元素都已被映射为形状为 $d$ 的嵌入向量，与模型尺寸相同。 |
| $\mathbf{W}^k \in \mathbb{R}^{d \times d_k}$ | 键权重矩阵。 |
| $\mathbf{W}^q \in \mathbb{R}^{d \times d_k}$ | 查询权重矩阵。 |
| $\mathbf{W}^v \in \mathbb{R}^{d \times d_v}$ | 值权重矩阵。通常 $d_k = d_v = d$。 |
| $\mathbf{W}^k_i, \mathbf{W}^q_i \in \mathbb{R}^{d \times d_k/h}; \mathbf{W}^v_i \in \mathbb{R}^{d \times d_v/h}$ | 每个头的权重矩阵。 |
| $\mathbf{W}^o \in \mathbb{R}^{d_v \times d}$ | 输出权重矩阵。 |
| $\mathbf{Q} = \mathbf{X}\mathbf{W}^q \in \mathbb{R}^{L \times d_k}$ | 查询嵌入输入。 |
| $\mathbf{K} = \mathbf{X}\mathbf{W}^k \in \mathbb{R}^{L \times d_k}$ | 键嵌入输入。 |
| $\mathbf{V} = \mathbf{X}\mathbf{W}^v \in \mathbb{R}^{L \times d_v}$ | 值嵌入输入。 |
| $\mathbf{q}_i, \mathbf{k}_i \in \mathbb{R}^{d_k}, \mathbf{v}_i \in \mathbb{R}^{d_v}$ | 查询、键、值矩阵 $\mathbf{Q}$、$\mathbf{K}$ 与 $\mathbf{V}$ 中的行向量。 |
| $S_i$ | 第 $i$ 个查询 $\mathbf{q}_i$ 所关注的键位置的集合。 |
| $\mathbf{A} \in \mathbb{R}^{L \times L}$ | 长度为 $L$ 的输入序列与自身之间的自注意力矩阵。$\mathbf{A} = \text{softmax}(\mathbf{Q}\mathbf{K}^\top / \sqrt{d_k})$。 |
| $a_{ij} \in \mathbf{A}$ | 查询 $\mathbf{q}_i$ 与键 $\mathbf{k}_j$ 之间的标量注意力分数。 |
| $\mathbf{P} \in \mathbb{R}^{L \times d}$ | 位置编码矩阵，其第 $i$ 行 $\mathbf{p}_i$ 是输入 $\mathbf{x}_i$ 的位置编码。 |

# Transformer 基础

**Transformer**（为与其他增强版本区分，下文称为「朴素 Transformer」；[Vaswani, et al., 2017](https://arxiv.org/abs/1706.03762)）模型采用编码器-解码器架构，这与许多 [NMT](https://lilianweng.github.io/posts/2018-06-24-attention/#born-for-translation)（神经机器翻译）模型中的常见做法一样。后来人们发现，简化版的 Transformer 在语言建模任务中同样能取得出色的表现，例如仅编码器的 [BERT](https://lilianweng.github.io/posts/2019-01-31-lm/#bert) 或仅解码器的 [GPT](https://lilianweng.github.io/posts/2019-01-31-lm/#openai-gpt)。

## 注意力与自注意力

**注意力（attention）**是神经网络中的一种机制：模型可以学会通过选择性地关注给定的一组数据来做出预测。注意力的多少由学习到的权重量化，因此输出通常以加权平均的形式构成。

**自注意力（self-attention）**是一种注意力机制：模型利用对同一样本观测的其他部分，来为该样本的某一部分做出预测。从概念上讲，它与[非局部均值（non-local means）](https://en.wikipedia.org/wiki/Non-local_means)颇为相似。另请注意，自注意力是置换不变的；换句话说，它是一种作用于集合的运算。

注意力/自注意力有各种各样的形式，Transformer（[Vaswani et al., 2017](https://arxiv.org/abs/1706.03762)）依赖的是*缩放点积注意力*：给定查询矩阵 $\mathbf{Q}$、键矩阵 $\mathbf{K}$ 和值矩阵 $\mathbf{V}$，输出是值向量的加权和，其中分配给每个值位置的权重由查询与相应键的点积确定：

$$
\text{attn}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}(\frac{\mathbf{Q} {\mathbf{K}}^\top}{\sqrt{d_k}})\mathbf{V}
$$

而对于查询与键向量 $\mathbf{q}_i, \mathbf{k}_j \in \mathbb{R}^d$（查询和键矩阵中的行向量），我们有标量分数：

$$
a_{ij} = \text{softmax}(\frac{\mathbf{q}_i {\mathbf{k}_j}^\top}{\sqrt{d_k}})
= \frac{\exp(\frac{\mathbf{q}_i {\mathbf{k}_j}^\top}{\sqrt{d_k}})}{ \sum_{r \in \mathcal{S}_i} \exp(\frac{\mathbf{q}_i {\mathbf{k}_r}^\top}{\sqrt{d_k}}) }
$$

其中 $\mathcal{S}_i$ 是第 $i$ 个查询所关注的键位置的集合。

如有兴趣，请参阅我以前的[博文，了解其他类型的注意力](https://lilianweng.github.io/posts/2018-06-24-attention/#a-family-of-attention-mechanisms)。

## 多头自注意力

**多头自注意力**模块是 Transformer 的关键组件。多头机制不是只计算一次注意力，而是将输入拆分成更小的块，然后在每个子空间上并行计算缩放点积注意力。各个独立的注意力输出直接拼接起来，再经过线性变换映射到期望的维度。

$$
\begin{aligned}
\text{MultiHeadAttn}(\mathbf{X}_q, \mathbf{X}_k, \mathbf{X}_v) &= [\text{head}_1; \dots; \text{head}_h] \mathbf{W}^o \\ 
\text{where head}_i &= \text{Attention}(\mathbf{X}_q\mathbf{W}^q_i, \mathbf{X}_k\mathbf{W}^k_i, \mathbf{X}_v\mathbf{W}^v_i)
\end{aligned}
$$

其中 $[.;.]$ 是拼接操作。$\mathbf{W}^q_i, \mathbf{W}^k_i \in \mathbb{R}^{d \times d_k/h}, \mathbf{W}^v_i \in \mathbb{R}^{d \times d_v/h}$ 是将尺寸为 $L \times d$ 的输入嵌入映射为查询、键、值矩阵的权重矩阵。$\mathbf{W}^o \in \mathbb{R}^{d_v \times d}$ 是输出线性变换。所有权重都应在训练中学习得到。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/multi-head-attention.png)

*多头缩放点积注意力机制示意图。（图片来源：Vaswani, et al., 2017 图 2）*

## 编码器-解码器架构

**编码器**生成基于注意力的表征，具备从大上下文中定位特定信息的能力。它由 6 个相同的模块堆叠而成，每个模块包含两个子模块：一个*多头自注意力*层和一个*逐点*全连接前馈网络。所谓逐点，是指它对序列中的每个元素应用相同的线性变换（权重相同）。这也可以看作滤波器尺寸为 1 的卷积层。每个子模块都配有残差连接与层归一化。所有子模块输出的数据维度相同，均为 $d$。

Transformer **解码器**的功能是从编码得到的表征中提取信息。其架构与编码器十分相似，不同之处在于每个重复的相同模块中，解码器包含两个（而非一个）多头注意力子模块。第一个多头注意力子模块是*带掩码的*，以防止各位置关注到未来的信息。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/transformer.png)

*朴素 Transformer 模型的架构。（图片来源：图 17）*

## 位置编码

由于自注意力运算是置换不变的，使用合适的**位置编码（positional encoding）**来为模型提供*顺序信息*就很重要。位置编码 $\mathbf{P} \in \mathbb{R}^{L \times d}$ 与输入嵌入维度相同，因此可以直接加在输入上。朴素 Transformer 考虑了两类编码：

### 正弦位置编码

给定 token 位置 $i=1,\dots,L$ 和维度 $\delta=1,\dots,d$，正弦位置编码定义如下：

$$
\text{PE}(i,\delta) = 
\begin{cases}
\sin(\frac{i}{10000^{2\delta'/d}}) & \text{if } \delta = 2\delta'\\
\cos(\frac{i}{10000^{2\delta'/d}}) & \text{if } \delta = 2\delta' + 1\\
\end{cases}
$$

这样，位置编码的每个维度都对应一条正弦曲线，不同维度上的波长各不相同，范围从 $2\pi$ 到 $10000 \cdot 2\pi$。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/sinoidual-positional-encoding.png)

*$L=32$、$d=128$ 的正弦位置编码。取值介于 -1（黑）与 1（白）之间，0 值以灰色表示。*

### 学习式位置编码

学习式位置编码为每个元素分配一个*学习得到的*列向量，用以编码其绝对位置（[Gehring, et al. 2017](https://arxiv.org/abs/1705.03122)）；进一步地，这种编码还可以按层以不同方式学习（[Al-Rfou et al. 2018](https://arxiv.org/abs/1808.04444)）。

### 相对位置编码

[Shaw et al. (2018)](https://arxiv.org/abs/1803.02155)) 将相对位置信息纳入 $\mathbf{W}^k$ 与 $\mathbf{W}^v$。最大相对位置被截断（clip）到最大绝对值 $k$，这种截断操作使模型能够泛化到未见过的序列长度。因此，共考虑 $2k + 1$ 个不同的边标签，并将 $\mathbf{P}^k, \mathbf{P}^v \in \mathbb{R}^{2k+1}$ 记为可学习的相对位置表示。

$$
A_{ij}^k = P^k_{\text{clip}(j - i, k)} \quad
A_{ij}^v = P^v_{\text{clip}(j - i, k)} \quad
\text{where }\text{clip}(x, k) = \text{clip}(x, -k, k)
$$

  

[Transformer-XL](#transformer-xl)（[Dai et al., 2019](https://arxiv.org/abs/1901.02860)）提出了一种基于键与查询点积重参数化的相对位置编码。为了让位置信息在片段之间连贯地流动，Transformer-XL 转而编码*相对*位置——因为对于做出好的预测而言，知道一个键向量 $\mathbf{k}_{\tau, j}$ 与其查询 $\mathbf{q}_{\tau, i}$ 之间的位置偏移（即 $i-j$）往往就足够了。

若省略标量 $1/\sqrt{d_k}$ 与 softmax 中的归一化项，但保留位置编码，我们可以把位置 $i$ 的查询与位置 $j$ 的键之间的注意力分数写成：

$$
\begin{aligned}
a_{ij} 
&= \mathbf{q}_i {\mathbf{k}_j}^\top = (\mathbf{x}_i + \mathbf{p}_i)\mathbf{W}^q ((\mathbf{x}_j + \mathbf{p}_j)\mathbf{W}^k)^\top \\
&= \mathbf{x}_i\mathbf{W}^q {\mathbf{W}^k}^\top\mathbf{x}_j^\top + \mathbf{x}_i\mathbf{W}^q {\mathbf{W}^k}^\top\mathbf{p}_j^\top + \mathbf{p}_i\mathbf{W}^q {\mathbf{W}^k}^\top\mathbf{x}_j^\top + \mathbf{p}_i\mathbf{W}^q {\mathbf{W}^k}^\top\mathbf{p}_j^\top
\end{aligned}
$$

Transformer-XL 将上述四项重参数化如下：

$$
a_{ij}^\text{rel} = 
\underbrace{ \mathbf{x}_i\mathbf{W}^q \color{blue}{ {\mathbf{W}_E^k}^\top } \mathbf{x}_j^\top }_\text{content-based addressing} + 
\underbrace{ \mathbf{x}_i\mathbf{W}^q \color{blue}{ {\mathbf{W}_R^k}^\top } \color{green}{\mathbf{r}_{i-j}^\top} }_\text{content-dependent positional bias} + 
\underbrace{ \color{red}{\mathbf{u}} \color{blue}{ {\mathbf{W}_E^k}^\top } \mathbf{x}_j^\top }_\text{global content bias} + 
\underbrace{ \color{red}{\mathbf{v}} \color{blue}{ {\mathbf{W}_R^k}^\top } \color{green}{\mathbf{r}_{i-j}^\top} }_\text{global positional bias}
$$

- 将 $\mathbf{p}_j$ 替换为相对位置编码 $\mathbf{r}_{i-j} \in \mathbf{R}^{d}$；
- 将 $\mathbf{p}_i\mathbf{W}^q$ 替换为两个可训练参数 $\mathbf{u}$（用于内容）和 $\mathbf{v}$（用于位置），分别置于不同的两项中；
- 将 $\mathbf{W}^k$ 拆分为两个矩阵：用于内容信息的 $\mathbf{W}^k_E$ 与用于位置信息的 $\mathbf{W}^k_R$。

### 旋转位置嵌入

旋转位置嵌入（rotary position embedding，*RoPE*；[Su et al. 2021](https://arxiv.org/abs/2104.09864)）用[旋转矩阵](https://en.wikipedia.org/wiki/Rotation_matrix)编码绝对位置，并将每个注意力层的键和值矩阵与该旋转矩阵相乘，从而在每一层注入相对位置信息。

在把相对位置信息编码进第 $i$ 个键与第 $j$ 个查询的内积时，我们希望把函数构造成使该内积只取决于相对位置 $i-j$ 的形式。旋转位置嵌入（RoPE）利用欧氏空间中的旋转操作，把相对位置嵌入表述为：简单地按与位置索引成比例的角度旋转特征矩阵。

给定向量 $\mathbf{z}$，若想将其逆时针旋转 $\theta$，可以乘一个旋转矩阵得到 $R\mathbf{z}$，其中旋转矩阵 $R$ 定义为：

$$
R = \begin{bmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{bmatrix}
$$

推广到高维空间时，RoPE 把 $d$ 维空间划分为 $d/2$ 个子空间，并为位置 $i$ 的 token 构造尺寸为 $d \times d$ 的旋转矩阵 $R$：

$$
R^d_{\Theta, i} = \begin{bmatrix}
\cos i\theta_1 & -\sin i\theta_1 & 0 & 0 & \dots & 0 & 0 \\
\sin i\theta_1 & \cos i\theta_1 & 0 & 0 & \dots & 0 & 0 \\
0 & 0 & \cos i\theta_2 & -\sin i\theta_2 & \dots & 0 & 0 \\
0 & 0 & \sin i\theta_2 & \cos i\theta_2 & \dots & 0 & 0 \\
\vdots & \vdots & \vdots & \vdots & \ddots & \vdots & \vdots \\
0 & 0 & 0 & 0 & \dots & \cos i\theta_{d/2} & -\sin i\theta_{d/2} \\
0 & 0 & 0 & 0 & \dots & \sin i\theta_{d/2} & \cos i\theta_{d/2} \\
\end{bmatrix}
$$

其中论文里取 $\Theta = {\theta_i = 10000^{-2(i−1)/d}, i \in [1, 2, …, d/2]}$。注意这本质上等价于正弦位置编码，只是表述成了旋转矩阵的形式。

然后，键和查询矩阵都通过与该旋转矩阵相乘来纳入位置信息：

$$
\begin{aligned}
& \mathbf{q}_i^\top \mathbf{k}_j = (R^d_{\Theta, i} \mathbf{W}^q\mathbf{x}_i)^\top (R^d_{\Theta, j} \mathbf{W}^k\mathbf{x}_j) = \mathbf{x}_i^\top\mathbf{W}^q R^d_{\Theta, j-i}\mathbf{W}^k\mathbf{x}_j \\
& \text{ where } R^d_{\Theta, j-i} = (R^d_{\Theta, i})^\top R^d_{\Theta, j}
\end{aligned}
$$

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/RoPE.png)

*旋转位置嵌入实现方式的直观示意。（图片来源：Su et al., 2021）注：与论文原图相比，我用 $i$ 而非 $m$ 表示位置索引。*

# 更长的上下文

Transformer 模型在推理时所能处理的输入序列长度，上界是训练时使用的上下文长度。天真地增大上下文长度会导致时间（$\mathcal{O}(L^2d)$）与内存（$\mathcal{O}(L^2)$）消耗剧增，而且可能因硬件限制而无法支持。

本节介绍 Transformer 架构上若干能更好地支持推理时长上下文的改进，例如使用额外的记忆（memory）、为更好的上下文外推而设计，或引入循环机制。

## 上下文记忆

朴素 Transformer 的注意力跨度（attention span）固定且有限。每次更新时，模型只能关注同一片段内的其他元素，信息无法跨越相互分离的定长片段流动。这种*上下文分段*（context segmentation）带来以下几个问题：

- 模型无法捕捉非常长期的依赖。
- 在没有上下文或上下文很少的情况下，每个片段开头的几个 token 很难预测。
- 评估代价高昂。每当片段向右移动一格，新片段都要从头重新处理，尽管两者之间存在大量重叠的 token。

**Transformer-XL**（[Dai et al., 2019](https://arxiv.org/abs/1901.02860)；「XL」意为「extra long」，超长）修改了架构，借助一段额外的记忆（memory）在片段之间复用隐藏状态。通过持续使用先前片段的隐藏状态，模型中被引入了片段间的循环连接。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/transformer-XL-training.png)

*朴素 Transformer 与 Transformer-XL 在片段长度为 4 时的训练过程对比。（图片来源：Dai et al., 2019 图 2 左半部分。）*

把模型中第 $(\tau + 1)$ 个片段第 $n$ 层的隐藏状态记为 $\mathbf{h}_{\tau+1}^{(n)} \in \mathbb{R}^{L \times d}$。除同片段上一层的隐藏状态 $\mathbf{h}_{\tau+1}^{(n-1)}$ 外，它还依赖上一片段同层的隐藏状态 $\mathbf{h}_{\tau}^{(n)}$。通过纳入先前隐藏状态的信息，模型把注意力跨度在过去延伸得远得多，跨越多个片段。

$$
\begin{aligned}
\color{red}{\widetilde{\mathbf{h}}_{\tau+1}^{(n-1)}} &= [\text{stop-gradient}(\mathbf{h}_{\tau}^{(n-1)}) \circ \mathbf{h}_{\tau+1}^{(n-1)}] \\
\mathbf{Q}_{\tau+1}^{(n)} &= \mathbf{h}_{\tau+1}^{(n-1)}\mathbf{W}^q \\
\mathbf{K}_{\tau+1}^{(n)} &= \color{red}{\widetilde{\mathbf{h}}_{\tau+1}^{(n-1)}} \mathbf{W}^k \\
\mathbf{V}_{\tau+1}^{(n)} &= \color{red}{\widetilde{\mathbf{h}}_{\tau+1}^{(n-1)}} \mathbf{W}^v \\
\mathbf{h}_{\tau+1}^{(n)} &= \text{transformer-layer}(\mathbf{Q}_{\tau+1}^{(n)}, \mathbf{K}_{\tau+1}^{(n)}, \mathbf{V}_{\tau+1}^{(n)})
\end{aligned}
$$

注意键和值都依赖扩展后的隐藏状态，而查询只使用当前步的隐藏状态。拼接操作 $[. \circ .]$ 沿序列长度维度进行。另外，Transformer-XL 需要使用[相对位置编码](#transformer-xl-encoding)，因为如果编码绝对位置，先前片段与当前片段会被赋予相同的编码，这并不理想。

**Compressive Transformer**（[Rae et al. 2019](https://arxiv.org/abs/1911.05507)）扩展了 Transformer-XL，通过压缩过去的记忆来支持更长的序列。它显式地为每层添加大小为 $m_m$ 的*记忆*槽位，用于保存该层过去的激活以保留长上下文。当某些过去的激活足够陈旧时，它们会被压缩并保存到每层额外的*压缩记忆*中，其大小为 $m_{cm}$。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/compressive-transformer.png)

*Compressive Transformer 维护两类记忆槽位——记忆与压缩记忆——以支持长上下文。（图片来源：Rae et al. 2019。）*

记忆与压缩记忆都是 FIFO（先进先出）队列。给定模型上下文长度 $L$，压缩率为 $c$ 的压缩函数定义为 $f_c: \mathbb{R}^{L \times d} \to \mathbb{R}^{[\frac{L}{c}] \times d}$，把最旧的 $L$ 个激活映射为 $[\frac{L}{c}]$ 个压缩记忆元素。压缩函数有多种选择：

1. 核与步长均为 $c$ 的最大/平均池化；
2. 核与步长均为 $c$ 的一维卷积（需要学习额外的参数）；
3. 膨胀卷积（需要学习额外的参数）。在他们的实验中，卷积压缩在 `EnWik8` 数据集上效果最好；
4. 最常被使用的记忆。

Compressive Transformer 还有两个额外的训练损失：

1. **自编码损失**（无损压缩目标）衡量我们能从压缩记忆中多好地重建原始记忆

   $$
 \mathcal{L}_{ac} = \| \textbf{old_mem}^{(i)} - g(\textbf{new_cm}^{(i)}) \|_2
 $$

   其中 $g: \mathbb{R}^{[\frac{L}{c}] \times d} \to \mathbb{R}^{L \times d}$ 是压缩函数 $f$ 的逆过程。
2. **注意力重建损失**（有损目标）在记忆与压缩记忆上分别重建基于内容的注意力，并最小化二者差异：

   $$
 \mathcal{L}_{ar} = \|\text{attn}(\mathbf{h}^{(i)}, \textbf{old_mem}^{(i)}) − \text{attn}(\mathbf{h}^{(i)}, \textbf{new_cm}^{(i)})\|_2
 $$

带大小为 $m$ 记忆的 Transformer-XL 的最大时间范围为 $m \times N$（其中 $N$ 是模型层数），注意力开销为 $\mathcal{O}(L^2 + Lm)$。相比之下，压缩 Transformer 的时间范围为 $(m_m + c \cdot m_{cm}) \times N$，注意力开销为 $\mathcal{O}(L^2 + L(m_m + m_{cm}))$。更大的压缩率 $c$ 能在时间范围长度与注意力开销之间取得更好的折中。

注意力权重按从旧到新的顺序存储在三个位置：压缩记忆 → 记忆 → 因果掩码序列。在实验中，他们观察到，从常规记忆中最旧的激活，到存储在压缩记忆中的激活，注意力权重有所增加，这意味着网络正在学会保留显著信息。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/compressive-transformer-memory.png)

*注意力权重（以一个标准差作为误差棒）随记忆位置的变化，从最旧（左）到最新（右）。（图片来源：Rae et al. 2019。）*

## 不可微的外部记忆

**$k$NN-LM**（[Khandelwal et al. 2020](https://arxiv.org/abs/1911.00172)）用一个独立的 $k$NN 模型增强预训练语言模型，做法是对两个模型预测的下一个 token 概率做线性插值。$k$NN 模型建立在外部键值存储之上，该存储可以容纳任意大的预训练数据集或 OOD（分布外）新数据集。这个数据存储库经预处理后保存了*大量*（上下文的 LM 嵌入表示, 下一个 token）对，最近邻检索发生在 LM 嵌入空间中。由于数据存储库可能非常庞大，我们需要依赖快速稠密向量检索库，例如 [FAISS](https://github.com/facebookresearch/faiss) 或 [ScaNN](https://github.com/google-research/google-research/tree/master/scann)。索引过程只需进行一次，且在推理时很容易实现并行。

推理时，下一个 token 的概率是两个预测的加权和：

$$
\begin{aligned}
p(y \vert \mathbf{x}) &= \lambda \; p_\text{kNN}(y \vert \mathbf{x}) + (1- \lambda) \; p_\text{LM}(y \vert \mathbf{x}) \\
p_\text{kNN}(y \vert \mathbf{x}) &\propto \sum_{(k_i, w_i) \in \mathcal{N}} \mathbb{1}[y = w_i] \exp(-d(k_i, f(\mathbf{x})))
\end{aligned}
$$

其中 $\mathcal{N}$ 包含 $k$NN 检索到的一组最近邻数据点；$d(., .)$ 是距离函数，例如 L2 距离。

实验表明，更大的数据存储库或更大的 $k$ 与更好的困惑度相关。加权标量 $\lambda$ 需要调优，但总体而言，域外数据所用的取值预计会比域内数据的大，而更大的数据存储库也能容纳更大的 $\lambda$。

**SPALM**（*Adaptive semiparametric language models*，自适应半参数语言模型；[Yogatama et al. 2021](https://arxiv.org/abs/2102.02557)）同时纳入：(1) Transformer-XL 式记忆，把来自外部上下文的隐藏状态作为短期记忆；(2) $k$NN-LM 式键值存储，作为长期记忆。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/SPALM2.png)

*SPALM 如何把过去隐藏状态的上下文记忆（短期记忆）与外部键值数据存储库（长期记忆）结合起来以支持更长上下文的示意图。（图片来源：Yogatama et al. 2021。）*

SPALM 运行 $k$NN 搜索来获取与上下文最相关的 $k$ 个 token。对每个 token，我们可以得到由某个预训练 LM 提供的相同嵌入表示，记为 $\{\mathbf{y}_i\}_{i=1}^k$。门控机制首先用一个简单的注意力层聚合检索到的 token 嵌入——以 $\mathbf{h}^R_t$（token $x_t$ 在第 $R$ 层的隐藏状态）为查询——然后学习门控参数 $\mathbf{g}_t$，在局部信息 $\mathbf{h}^R_t$ 与长期信息 $\mathbf{m}_t$ 之间取得平衡。

$$
\begin{aligned}
\mathbf{m}_t &= \sum_{i=1}^k \frac{\exp(\mathbf{y}_i^\top \mathbf{h}^R_t)}{\sum_{j=1}^k \exp(\mathbf{y}_j^\top \mathbf{h}^R_t)} \cdot \mathbf{y}_i \\
\mathbf{g}_t &= \sigma(\mathbf{w}_g^\top \mathbf{h}_t^R) \\
\mathbf{z}_t &= (1 - \mathbf{g}_t) \odot \mathbf{m}_t + \mathbf{g}_t \odot \mathbf{h}^R_t \\
p(x_{t+1}\mid \mathbf{x}_{\leq t}) &= \text{softmax}(\mathbf{z}_t; \mathbf{W})
\end{aligned}
$$

其中 $\mathbf{w}_g$ 是待学习的参数向量；$\sigma(.)$ 是 sigmoid；$\mathbf{W}$ 是输入与输出 token 共享的词嵌入矩阵。与 $k$NN-LM 不同，他们发现最近邻距离对检索 token 的聚合并没有帮助。

训练期间，长期记忆中的键表示保持不变（由一个预训练 LM 生成），但值编码器（即词嵌入矩阵）会得到更新。

**Memorizing Transformer**（[Wu et al. 2022](https://arxiv.org/abs/2203.08913)）在仅解码器 Transformer 靠近顶部的堆栈处添加了一个 $k$NN 增强的注意力层。这个特殊的层维护一个 Transformer-XL 式的 FIFO 缓存，保存过去的键值对。

局部注意力与 $k$NN 机制使用相同的 QKV 值。$k$NN 查找为输入序列中的每个查询返回 top-$k$（键, 值）对，然后它们经过自注意力堆栈处理，计算检索值的加权平均。两类注意力通过逐头可学习的门控参数结合在一起。为防止数值幅度出现大的分布偏移，缓存中的键和值都做了归一化。

他们在 Memorizing Transformer 实验中的发现：

- 一些实验观察到，先用小记忆训练、再用更大记忆微调，比从一开始就用大记忆训练效果更好。
- 记忆中仅有 8k token 的较小 Memorizing Transformer，可以匹敌可训练参数多 5 倍的更大朴素 Transformer 的困惑度。
- 增大外部记忆的尺寸能带来一致的收益，最大可到 262K。
- 不带记忆的 Transformer 也可以通过微调学会使用记忆。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/memorizing-transformer.png)

*用键值记忆微调朴素 Transformer，可以达到与从零训练 Memorizing Transformer 相当的性能。（图片来源：Wu et al. 2022。）*

## 距离增强的注意力分数

**Distance Aware Transformer**（**DA-Transformer**；[Wu, et al. 2021](https://aclanthology.org/2021.naacl-main.166)）与**带线性偏置的注意力（Attention with Linear Biases，ALiBi）**（[Press et al. 2022](https://arxiv.org/abs/2108.12409)）的动机相似——为了让模型能外推（extrapolate）到比训练时更长的上下文，我们可以依据键与查询 token 之间的距离，把位置信息显式地附加到每一对注意力分数上。

注意，朴素 Transformer 中默认的位置编码只把位置信息加到输入序列上，而后来改进的编码机制会改变每一层的注意力分数（例如[旋转位置嵌入](#rotary-position-embedding)），它们的形式与距离增强的注意力分数非常相似。

*DA-Transformer*（[Wu, et al. 2021](https://aclanthology.org/2021.naacl-main.166)）在每层用一个可学习偏置与注意力分数相乘，该偏置被表述为键与查询之间距离的函数。不同的注意力头使用不同的参数，以区分对短期与长期上下文的不同偏好。给定两个位置 $i, j$，DA-Transformer 使用以下加权函数来改变自注意力分数：

$$
\begin{aligned}
\mathbf{R}^{(i)} &= \alpha_i \mathbf{R} \quad \text{where }R_{ij} = \vert i-j \vert\\
f(\mathbf{R}^{(i)}; \beta_i) &= \frac{1 + \exp(\beta_i)}{1 + \exp(\beta_i - \mathbf{R}^{(i)})} \\
\text{attn}(\mathbf{Q}^{(i)}, \mathbf{K}^{(i)}, \mathbf{V}^{(i)}) &= \text{row-softmax}\Big(\frac{\text{ReLU}(\mathbf{Q}^{(i)}\mathbf{K}^{(i)\top})f(\mathbf{R}^{(i)})}{\sqrt{d}}\Big) \mathbf{V}^{(i)}
\end{aligned}
$$

其中 $\alpha_i$ 是可学习参数，用于让每个头（以上标 $^{(i)}$ 索引）对相对距离施加不同权重；$\beta_i$ 是可学习参数，用于控制第 $i$ 个注意力头相对于距离的上界与上升斜率。加权函数 $f(.)$ 的设计满足：(1) $f(0)=1$；(2) 当 $\mathbf{R}^{(i)} \to -\infty$ 时 $f(\mathbf{R}^{(i)}) = 0$；(3) 当 $\mathbf{R}^{(i)} \to +\infty$ 时 $f(\mathbf{R}^{(i)})$ 有界；(4) 尺度可调；(5) 函数单调。$f(\mathbf{R}^{(i)})$ 带来的额外时间复杂度为 $\mathcal{O}(L^2)$，相对自注意力 $\mathcal{O}(L^2 d)$ 的时间复杂度而言很小。额外的内存消耗也微乎其微，约 $\mathcal{O}(2h)$。

*ALiBi*（[Press et al. 2022](https://arxiv.org/abs/2108.12409)）不使用乘性系数，而是在查询-键注意力分数上加上一个与成对距离成比例的常数偏置项。该偏置引入强烈的近期偏好，并惩罚距离太远的键。惩罚的增速在不同的头中各不相同。

$$
\text{softmax}(\mathbf{q}_i \mathbf{K}^\top + \alpha_i \cdot [0, -1, -2, \dots, -(i-1)])
$$

其中 $\alpha_i$ 是每个头各自的加权标量。与 DA-Transformer 不同，$\alpha_i$ 不是学习得到的，而是固定为等比数列；例如对 8 个头，${\alpha_i} = {\frac{1}{2}, \frac{1}{2^2}, \dots, \frac{1}{2^8}}$。其总体思想与相对位置编码想要解决的问题非常相似。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/ALiBi-bias.png)

*ALiBi 如何用位置偏置项增强注意力分数的示意图。（图片来源：Press et al. 2021。）*

借助 ALiBi，[Press et al. (2022)](https://arxiv.org/abs/2108.12409) 训练了一个 1.3B 参数的模型，训练时上下文长度为 1024，推理时外推到 2046。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/ALiBi-exp.png)

*用不同配置的 Transformer 进行推理的外推实验，包括正弦位置编码、旋转位置编码、T5 的简化相对位置编码以及 ALiBi。所有模型都以较小的上下文长度训练，但推理时的上下文要长得多。（图片来源：Press et al. 2021。）*

## 使其循环

**Universal Transformer**（[Dehghani, et al. 2019](https://arxiv.org/abs/1807.03819)）将 Transformer 的自注意力与 RNN 的循环机制相结合，希望同时受益于 Transformer 长期的全局感受野与 RNN 学到的归纳偏置。Universal Transformer 不是穿过固定数量的层，而是借助[自适应计算时间](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/#adaptive-computation-time-act)动态调整步数。若固定步数，Universal Transformer 等价于一个各层共享参数的多层 Transformer。

从高层来看，Universal Transformer 可以被视为一个用于学习每个 token 隐藏状态表示的循环函数。该循环函数在各 token 位置上并行演进，位置之间的信息通过自注意力共享。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/universal-transformer-loop.png)

*Universal Transformer 如何对每个位置并行地反复精炼一组隐藏状态表示。（图片来源：Dehghani, et al. 2019 图 1。）*

给定长度为 $L$ 的输入序列，Universal Transformer 在第 $t$ 步迭代地更新表示 $\mathbf{h}^t \in \mathbb{R}^{L \times d}$，步数可调。第 0 步时，$\mathbf{h}^0$ 初始化为与输入嵌入矩阵相同。所有位置在多头自注意力机制中并行处理，然后经过一个循环转移函数。

$$
\begin{aligned}
\mathbf{A}^t &= \text{LayerNorm}(\mathbf{h}^{t-1} + \text{MultiHeadAttention}(\mathbf{h}^{t-1} + \mathbf{P}^t) \\
\mathbf{h}^t &= \text{LayerNorm}(\mathbf{A}^{t-1} + \text{Transition}(\mathbf{A}^t))
\end{aligned}
$$

其中 $\text{Transition}(.)$ 是一个[可分离卷积](https://arxiv.org/abs/1610.02357)或全连接神经网络，后者由两个逐位置（即单独应用于 $\mathbf{A}^t$ 的每一行）仿射变换加一个 ReLU 组成。

位置编码 $\mathbf{P}^t$ 使用[正弦位置信号](#sinusoidal-positional-encoding)，但额外增加了一个时间维度：

$$
\text{PE}(i, t, \delta) = 
\begin{cases}
\sin(\frac{i}{10000^{2\delta'/d}}) \oplus \sin(\frac{t}{10000^{2\delta'/d}}) & \text{if } \delta = 2\delta'\\
\cos(\frac{i}{10000^{2\delta'/d}}) \oplus \cos(\frac{t}{10000^{2\delta'/d}}) & \text{if } \delta = 2\delta' + 1\\
\end{cases}
$$

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/universal-transformer.png)

*Universal Transformer 的简化示意图。编码器与解码器共享相同的基本循环结构，但解码器还会关注编码器的最终表示 $\mathbf{h}^T$。（图片来源：Dehghani, et al. 2019 图 2。）*

在 Universal Transformer 的自适应版本中，循环步数 $T$ 由 [ACT](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/#adaptive-computation-time-act) 动态决定。每个位置都配备一个动态的 ACT 停止机制。一旦某个逐 token 的循环块停止，它便不再接受更多的循环更新，而只是把当前值复制到下一步，直到所有块都停止或模型达到最大步数限制。

# 自适应建模

自适应建模指的是一种能根据不同输入调整计算量的机制。例如，某些 token 可能只需要局部信息，因而需要更短的注意力跨度；或者某些 token 相对更容易预测，不需要穿过整个注意力堆栈。

## 自适应注意力跨度

Transformer 的一个关键优势是捕捉长期依赖的能力。视上下文而定，模型有时可能比其他时候更想关注远处的位置；或者某个注意力头的注意力模式可能与其他头不同。如果注意力跨度能够灵活调整长度、只在需要时才往回看得更远，将有助于降低计算与内存开销，从而支持模型中更长的最大上下文尺寸。

这正是**自适应注意力跨度（Adaptive Attention Span）**的动机。[Sukhbaatar et al (2019)](https://arxiv.org/abs/1905.07799) 提出了一种寻找最优注意力跨度的自注意力机制。他们假设不同的注意力头在同一上下文窗口内可能给出不同的分数（见图 14），因此最优跨度应按每个头分别训练。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/attention-per-head.png)

*同一模型中的两个注意力头 A 与 B 在同一上下文窗口内分配注意力的方式不同。头 A 更多关注近期的 token，而头 B 均匀地回看更远的过去。（图片来源：Sukhbaatar, et al. 2019。）*

给定第 $i$ 个 token，我们需要计算它与大小为 $s$ 的注意力跨度内其他键之间的注意力权重：

$$
\begin{aligned}
e_{ij} &= \mathbf{q}_i {\mathbf{k}_j}^\top \\ 
a_{ij} &= \text{softmax}(e_{ij}) = \frac{\exp(e_{ij})}{\sum_{r=i-s}^{i-1} \exp(e_{ir})} \\
\mathbf{y}_i &= \sum_{r=i-s}^{i-1}a_{ir}\mathbf{v}_r = \sum_{r=i-s}^{i-1}a_{ir}\mathbf{x}_r\mathbf{W}^v
\end{aligned}
$$

加入一个*软掩码函数* $m_z$ 来控制可调的有效注意力跨度，它把查询与键之间的距离映射为 [0, 1] 值。$m_z$ 由 $z \in [0, s]$ 参数化，$z$ 待学习：

$$
m_z(x) = \text{clip}(\frac{1}{R}(R+z-x), 0, 1)
$$

其中 $R$ 是定义 $m_z$ 软程度的超参数。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/soft-masking-function.png)

*自适应注意力跨度中使用的软掩码函数。（图片来源：Sukhbaatar, et al. 2019。）*

软掩码函数作用于注意力权重中的 softmax 元素：

$$
a_{ij} = \frac{m_z(i-j)\exp(s_{ij})}{\sum_{r=i-s}^{i-1}m_z(i-r) \exp(s_{ir})}
$$

在上式中，$z$ 可微，因此可与模型的其他部分联合训练。参数 $z^{(i)}, i=1, \dots, h$ 按*每个头分别*学习。此外，损失函数对 $\sum_{i=1}^h z^{(i)}$ 有额外的 L1 惩罚。

借助[自适应计算时间](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/#adaptive-computation-time-act)，该方法可进一步增强为注意力跨度长度灵活、随当前输入动态自适应。时间 $t$ 某注意力头的跨度参数 $z_t$ 是一个 sigmoid 型函数，$z_t = S \sigma(\mathbf{v} \cdot \mathbf{x}_t +b)$，其中向量 $\mathbf{v}$ 与偏置标量 $b$ 与其他参数联合学习。

在带自适应注意力跨度的 Transformer 实验中，[Sukhbaatar, et al. (2019)](https://arxiv.org/abs/1905.07799) 发现一个普遍趋势：较低的层不需要很长的注意力跨度，而较高层的少数注意力头可能使用格外长的跨度。自适应注意力跨度还能大幅减少 FLOPS 数量，尤其在注意力层多、上下文长度大的大模型中。

## 深度自适应 Transformer

推理时，很自然可以假设某些 token 更容易预测，因而并不需要与其他 token 同等的计算量。因此，我们可以只让预测经过有限数量的层，以在速度与性能之间取得良好的平衡。

**Depth-Adaptive Transformer**（[Elabyad et al. 2020](https://arxiv.org/abs/1910.10073)）与**置信自适应语言模型（Confident Adaptive Language Model，CALM）**（[Schuster et al. 2022](https://arxiv.org/abs/2207.07061)）都源于这一想法，二者都学习为不同的输入 token 预测所需的最佳层数。

*Depth-adaptive Transformer*（[Elabyad et al. 2020](https://arxiv.org/abs/1910.10073)）为每一层挂接一个输出分类器，基于该层的激活产生退出（exit）预测。分类器权重矩阵可以每层不同，也可以跨层共享。训练时，模型采样不同的退出序列，使得模型用不同层的隐藏状态进行优化。学习目标纳入了在不同层预测的似然概率，$n=1, \dots, N$：

$$
\text{LL}^n_t = \log p(y_t \vert \mathbf{h}^n_{t-1}) \quad
\text{LL}^n = \sum_{t=1}^{\vert\mathbf{y}\vert} LL^n_t
$$

自适应深度分类器输出一个参数化分布 $q_t$，用相对 oracle 分布 $q^*_t$ 的交叉熵损失训练。论文探索了学习这种分类器 $q_t$ 的三种配置。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/depth-adaptive-classifier.png)

*三类自适应深度分类器的示意图。（图片来源：Elabyad et al. 2020。）*

1. *序列级深度分类器*：同一序列的所有 token 共享同一个退出块。它依赖该序列编码器表示的平均。给定长度为 $L$ 的输入序列 $\mathbf{x}$，分类器以 $\bar{\mathbf{x}} = \frac{1}{L} \sum_{t=1}^L \mathbf{x}_t$ 为输入，输出 $N$ 维多项分布，对应 $N$ 个层。

   $$
 \begin{aligned}
 q(n \vert \mathbf{x}) &=\text{softmax}(\mathbf{W}_n \bar{\mathbf{x}} + b_n) \in \mathbb{R}^N \\
 q_\text{lik}^*(\mathbf{x}, \mathbf{y}) &= \delta(\arg\max_n \text{LL}^n - \lambda n) \\
 \text{or }q_\text{corr}^*(\mathbf{x}, \mathbf{y}) &= \delta(\arg\max_n C^n - \lambda n) \text{ where }C^n = \vert\{t \vert y_t = \arg\max_y p(y \vert \mathbf{h}^n_{t-1})\}\vert \\
 \end{aligned}
 $$

   其中 $\delta$ 是[狄拉克 delta（单位冲激）函数](https://en.wikipedia.org/wiki/Dirac_delta_function)，$-\lambda n$ 是鼓励从较低层退出的正则化项。真值 $q^*$ 有两种构造方式：基于极大似然的 $q_\text{lik}^*$ 或基于正确性的 $q_\text{corr}^*$。
2. *token 级深度分类器（多项式）*：每个 token 使用不同的退出块解码，预测以第一个解码器隐藏状态 $\mathbf{h}^1_t$ 为条件：

   $$
 q_t(n \vert \mathbf{x}, \mathbf{y}_{< t}) = \text{softmax}(\mathbf{W}_n \mathbf{h}^1_t + b_n)
 $$
3. *token 级深度分类器（类几何）*：每层每 token 做一个二值退出预测分布 $\mathcal{X}^n_t$。RBF 核 $\kappa(t, t’) = \exp(\frac{\vert t - t’ \vert^2}{\sigma})$ 用于平滑预测，以纳入当前决策对未来时间步的影响。

   $$
 \begin{aligned}
 \mathcal{X}^n_t &= \text{sigmoid}(\mathbf{w}_n^\top \mathbf{h}^n_t + b_n)\quad \forall n \in [1, \dots, N-1] \\
 q_t(n \vert \mathbf{x}, \mathbf{y}_{< t}) &= \begin{cases}
 \mathcal{X}^n_t \prod_{n' < n} (1 - \mathcal{X}^{n'}_t) & \text{if } n < N\\
 \prod_{n' < N} (1 - \mathcal{X}^{n'}_t) & \text{otherwise}
 \end{cases} \\
 q_\text{lik}^*(\mathbf{x}, \mathbf{y}) &= \delta(\arg\max_n \widetilde{\text{LL}}^n_t - \lambda n) \text{ where } \widetilde{\text{LL}}^n_t = \sum_{t'=1}^{\vert\mathbf{y}\vert}\kappa(t, t') LL^n_{t'} \\
 \text{or }q_\text{cor}^*(\mathbf{x}, \mathbf{y}) &= \delta(\arg\max_n \tilde{C}_t^n - \lambda n) \text{ where }C_t^n = \mathbb{1}[y_t = \arg\max_y p(y \vert \mathbf{h}^n_{t-1})],\; \tilde{C}^n_t = \sum_{t'=1}^{\vert\mathbf{y}\vert}\kappa(t, t') C^n_{t'} \\
 \end{aligned}
 $$

推理时，做出退出决策所用的置信度阈值需要校准。Depth-adaptive Transformer 通过网格搜索在验证集上找到这样的阈值。*CALM*（[Schuster et al. 2022](https://arxiv.org/abs/2207.07061)）应用 Learn then Test（LTT）框架（[Angelopoulos et al. 2021](https://arxiv.org/abs/2110.01052)）识别出一组有效阈值，并选取其中最小值作为推理阈值。除了训练逐层退出分类器，CALM 还探索了其他自适应深度预测方法，包括用 softmax 响应（即两个最高 softmax 输出之差）和隐藏状态饱和度（即 $\cos(\mathbf{h}^n_t, \mathbf{h}^{n+1}_t)$）作为退出决策的置信度分数。他们发现 softmax 响应带来最佳的推理加速。

# 高效注意力

朴素 Transformer 的计算与内存开销随序列长度呈平方增长，因此很难应用于很长的序列。Transformer 架构的许多效率改进都与自注意力模块有关——让它运行起来更便宜、更小或更快。参见 *Efficient Transformers* 综述论文（[Tay et al. 2020](https://arxiv.org/abs/2009.06732)）。

## 稀疏注意力模式

### 固定局部上下文

一个让自注意力更省资源的简单改动，是把每个 token 的注意力跨度限制在**局部**上下文，这样自注意力就随序列长度线性增长。

这一思想由 **Image Transformer**（[Parmer, et al 2018](https://arxiv.org/abs/1802.05751)）引入，它把图像生成表述为用编码器-解码器 Transformer 架构进行的序列建模：

- 编码器生成源图像的、逐像素通道的上下文化表示；
- 然后解码器自回归地生成输出图像，每个时间步生成每个像素的一个通道。

把当前待生成像素的表示记为查询 $\mathbf{q}$。其他位置中，其表示将用于计算 $\mathbf{q}$ 的是键向量 $\mathbf{k}_1, \mathbf{k}_2, \dots$，它们共同构成一个记忆矩阵 $\mathbf{M}$。$\mathbf{M}$ 的范围定义了像素查询 $\mathbf{q}$ 的上下文窗口。

Image Transformer 引入了两种局部化的 $\mathbf{M}$，如下图所示。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/image-transformer-attention.png)

*Image Transformer 中视觉输入的一维与二维注意力跨度示意图。黑线标记一个查询块，青色勾勒出像素 q 的实际注意力跨度。（图片来源：Parmer et al, 2018 图 2。）*

1. *一维局部注意力*：输入图像按[光栅扫描](https://en.wikipedia.org/wiki/Raster_scan#Scanning_pattern)顺序展平，即从左到右、从上到下。展平后的图像再被划分为不重叠的查询块。上下文窗口由与 $\mathbf{q}$ 同一查询块内的像素，以及在该查询块之前已生成的固定数量额外像素组成。
2. *二维局部注意力*：图像被划分为多个不重叠的矩形查询块。查询像素可以关注同一记忆块中的所有其他像素。为确保左上角的像素也有有效的上下文窗口，记忆块分别向上、向左、向右扩展固定的量。

### 跨步上下文

**Sparse Transformer**（[Child et al., 2019](https://arxiv.org/abs/1904.10509)）通过稀疏矩阵分解引入了*分解自注意力（factorized self-attention）*，使训练序列长度高达 16,384、数百层的稠密注意力网络成为可能——否则在现代硬件上并不可行。

给定一组注意力连接模式 $\mathcal{S} = \{S_1, \dots, S_n\}$，其中每个 $S_i$ 记录第 $i$ 个查询向量所关注的键位置集合。

$$
\begin{aligned}
\text{Attend}(\mathbf{X}, \mathcal{S}) &= \Big( a(\mathbf{x}_i, S_i) \Big)_{i \in \{1, \dots, L\}} \\
\text{ where } a(\mathbf{x}_i, S_i) &= \text{softmax}\Big(\frac{(\mathbf{x}_i \mathbf{W}^q)(\mathbf{x}_j \mathbf{W}^k)_{j \in S_i}^\top}{\sqrt{d_k}}\Big) (\mathbf{x}_j \mathbf{W}^v)_{j \in S_i}
\end{aligned}
$$

注意，虽然 $S_i$ 的大小不固定，$a(\mathbf{x}_i, S_i)$ 的尺寸总是 $d_v$，因此 $\text{Attend}(\mathbf{X}, \mathcal{S}) \in \mathbb{R}^{L \times d_v}$。

在自回归模型中，注意力跨度定义为 $S_i = \{j: j \leq i\}$，因为它允许每个 token 关注过去所有位置。

在分解自注意力中，集合 $S_i$ 被分解为一棵依赖*树*，使得对每对满足 $j \leq i$ 的 $(i, j)$，都存在一条把 $i$ 连回 $j$ 的路径，$i$ 可以直接或间接地关注 $j$。

确切地说，集合 $S_i$ 被划分为 $p$ 个*不重叠*的子集，第 $m$ 个子集记作 $A^{(m)}_i \subset S_i, m = 1,\dots, p$。因此，输出位置 $i$ 与任意 $j$ 之间的路径最大长度为 $p + 1$。例如，若 $(j, a, b, c, \dots, i)$ 是 $i$ 与 $j$ 之间的一条索引路径，则应有 $j \in A_a^{(1)}, a \in A_b^{(2)}, b \in A_c^{(3)}, \dots$，依此类推。

**稀疏分解注意力**

Sparse Transformer 提出两类分解注意力。结合图 10、以 2D 图像输入为例来理解这些概念会更容易。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/sparse-attention.png)

*上排展示 (a) Transformer、(b) 带跨步注意力的 Sparse Transformer、(c) 带固定注意力的 Sparse Transformer 的注意力连接模式。下排为相应的自注意力连接矩阵。注意上下两排比例不同。（图片来源：Child et al., 2019 + 若干额外标注。）*

1. *跨步（Strided）*注意力，步长 $\ell \sim \sqrt{n}$。这对图像数据很有效，因为图像结构与跨步对齐。图像情形下，每个像素关注光栅扫描顺序中前面全部 $\ell$ 个像素（自然覆盖图像整个宽度），然后这些像素再关注同一列中的其他像素（由另一个注意力连接子集定义）。

   $$
 \begin{aligned}
 A_i^{(1)} &= \{ t, t+1, \dots, i\} \text{, where } t = \max(0, i - \ell) \\
 A_i^{(2)} &= \{j: (i-j) \mod \ell = 0\}
 \end{aligned}
 $$
2. *固定（Fixed）*注意力。一小部分 token 汇总先前的位置，并把该信息传播给所有未来位置。

   $$
 \begin{aligned}
 A_i^{(1)} &= \{j: \lfloor \frac{j}{\ell} \rfloor = \lfloor \frac{i}{\ell} \rfloor \} \\
 A_i^{(2)} &= \{j: j \mod \ell \in \{\ell-c, \dots, \ell-1\} \}
 \end{aligned}
 $$

   其中 $c$ 是一个超参数。若 $c=1$，会限制表示，因为许多位置将依赖少数几个位置。论文在 $\ell \in \{ 128, 256 \}$ 时选取 $c\in \{ 8, 16, 32 \}$。

**在 Transformer 中使用分解自注意力**

有三种方式在 Transformer 架构中使用稀疏分解注意力模式：

1. 每个残差块用一种注意力类型，然后交替使用，
   $\text{attn}(\mathbf{X}) = \text{Attend}(\mathbf{X}, A^{(n \mod p)}) \mathbf{W}^o$，其中 $n$ 是当前残差块的索引。
2. 设置一个单独的头，关注全部分解头所关注的位置，
   $\text{attn}(\mathbf{X}) = \text{Attend}(\mathbf{X}, \cup_{m=1}^p A^{(m)}) \mathbf{W}^o $。
3. 使用多头注意力机制，但与朴素 Transformer 不同，每个头可采用上面的模式 1 或 2。$\rightarrow$ 这一选项通常效果最好。

Sparse Transformer 还提出了一组改动，以便把 Transformer 训练到数百层，包括梯度检查点、反向传播时重算注意力与前馈层、混合精度训练、高效的块稀疏实现等。更多细节请查阅[论文](https://arxiv.org/abs/1904.10509)，或我此前关于[规模化模型训练技术](https://lilianweng.github.io/posts/2021-09-25-train-large/)的博文。

**Blockwise Attention**（[Qiu et al. 2019](https://arxiv.org/abs/1911.02972)）引入*稀疏块矩阵*，只允许每个 token 关注一小部分其他 token。每个尺寸为 $L \times L$ 的注意力矩阵被划分为 $n \times n$ 个尺寸为 $\frac{L}{n}\times\frac{L}{n}$ 的小块，稀疏块矩阵 $\mathbf{M} \in \{0, 1\}^{L \times L}$ 由 ${1, \dots, n}$ 的一个置换 $\pi$ 定义，它记录块矩阵中每行的列索引。

$$
\begin{aligned}
\text{attn}(\mathbf{Q}, \mathbf{K}, \mathbf{V}, \mathbf{M}) &= \text{softmax}\Big(\frac{\mathbf{Q}\mathbf{K}^\top}{\sqrt{d}} \odot \mathbf{M}\Big)\mathbf{V} \\
(\mathbf{A} \odot \mathbf{M})_{ij} &= \begin{cases}
A_{ij} & \text{if }M_{ij} = 1 \\
-\infty & \text{if }M_{ij} = 0 \\
\end{cases} \\
\text{where } M_{ij} &= \begin{cases}
1 & \text{if }\pi\big(\lfloor\frac{(i-1)n}{L} + 1\rfloor\big) = \lfloor\frac{(j-1)n}{L} + 1\rfloor \\
0 & \text{otherwise}
\end{cases}
\end{aligned}
$$

Blockwise Attention 的实际实现只把 QKV 存为块矩阵，每块尺寸 $n\times n$：

$$
\text{Blockwise-attn}(\mathbf{Q}, \mathbf{K}, \mathbf{V}, \mathbf{M}) = \begin{bmatrix}
\text{softmax}\big(\frac{\hat{\mathbf{q}}_1\hat{\mathbf{k}}_{\pi(1)}^\top}{\sqrt{d}} \Big)\hat{\mathbf{v}}_{\pi(1)} \\
\vdots \\
\text{softmax}\big(\frac{\hat{\mathbf{q}}_n\hat{\mathbf{k}}_{\pi(n)}^\top}{\sqrt{d}} \odot \Big)\hat{\mathbf{v}}_{\pi(n)} \\
\end{bmatrix}
$$

其中 $\hat{\mathbf{q}}_i$、$\hat{\mathbf{k}}_i$ 与 $\hat{\mathbf{v}}_i$ 分别是 QKV 块矩阵的第 $i$ 行。每个 $\mathbf{q}_i\mathbf{k}_{\pi(i)}^\top, \forall i = 1, \dots, n$ 的尺寸为 $\frac{N}{n}\times\frac{N}{n}$，因此 Blockwise Attention 能把注意力矩阵的内存复杂度从 $\mathcal{O}(L^2)$ 降到 $\mathcal{O}(\frac{L}{n}\times\frac{L}{n} \times n) = \mathcal{O}(L^2/n)$。

### 局部与全局上下文的组合

**ETC**（*Extended Transformer Construction*；[Ainslie et al. 2019](https://aclanthology.org/2020.emnlp-main.19/)）、**Longformer**（[Beltagy et al. 2020](https://arxiv.org/abs/2004/05150)）与 **Big Bird**（[Zaheer et al. 2020](https://arxiv.org/abs/2007.14062)）模型在构建注意力矩阵时同时结合局部与全局上下文。所有这些模型都可以从现有的预训练模型初始化。

*ETC* 的**全局-局部注意力**（[Ainslie et al. 2019](https://aclanthology.org/2020.emnlp-main.19/)）接收两个输入：(1) 尺寸为 $n_l$ 的长输入 $\mathbf{x}^l$，即常规的输入序列；(2) 尺寸为 $n_g$ 的全局输入 $\mathbf{x}^g$，包含数量较少的辅助 token，$n_g \ll n_l$。于是注意力按这两个输入之间的方向性注意力拆分为四个部分：g2g、g2l、l2g 与 l2l。由于 l2l 注意力部分可能非常大，它被限制为半径 $w$ 的固定尺寸注意力跨度（即局部注意力跨度），l2l 矩阵可重塑为 $n_l \times (2w+1)$。

ETC 利用四个二值矩阵来处理结构化输入：$\mathbf{M}^{g2g}$、$\mathbf{M}^{g2l}$、$\mathbf{M}^{l2g}$ 与 $\mathbf{M}^{l2l}$。例如，g2g 注意力部分的注意力输出 $z^g = (z^g_1, \dots, z^g_{n_g})$ 中每个元素 $z^g_i \in \mathbb{R}^d$ 的形式为：

$$
\begin{aligned}
a^{g2g}_{ij} = \frac{1}{\sqrt{d}} x^g_i \mathbf{W}^Q (x^g_j \mathbf{W}^K + P^K_{ij})^\top - (1- M^{g2g}_{ij})C \\
A^{g2g}_{ij} = \frac{\exp(a^{g2g}_{ij})}{\sum_{k=1}^{n_g} \exp(a^{g2g}_{ik})} \quad
z^g_i = \sum^{n_g}_{j=1} A^{g2g}_{ij} x^g_j \mathbf{W}^V
\end{aligned}
$$

其中 $P^K_{ij}$ 是用于相对位置编码的可学习向量，$C$ 是一个非常大的常数（论文中 $C=10000$），用于在掩码关闭时抵消注意力权重。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/combined-attention.png)

*ETC、Longformer 与 Big Bird 的注意力模式。*

ETC 的另一项更新是：除了 [MLM](https://lilianweng.github.io/posts/2019-01-31-lm/#MLM) 任务之外，还在预训练阶段纳入一个使用 [NCE 损失](https://lilianweng.github.io/posts/2021-05-31-contrastive/#nce)的 CPC（contrastive predictive coding，对比预测编码）任务：某个句子的表示，应当与该句被掩码时其周围上下文的表示相似。

ETC 的全局输入 $\mathbf{x}^g$ 按如下方式构造：假设长输入中存在一些片段（例如按句子划分），每个片段挂接一个辅助 token 来学习全局输入。用[相对位置编码](#relative-position-encoding)把全局片段 token 与 token 位置关联标记。单方向的硬掩码（即前后的 token 标记不同）被发现能在某些数据集上带来性能提升。

Longformer 的注意力模式包含三个部分：

1. *局部注意力*：与 ETC 类似，局部注意力由固定大小 $w$ 的滑动窗口控制；
2. *预选 token 的全局注意力*：Longformer 为少数预先选定的 token（例如 `[CLS]` token）分配全局注意力跨度，即关注输入序列中的所有其他 token。
3. *膨胀注意力*：固定大小 $r$、膨胀间隔为 $d$ 的膨胀滑动窗口，与 Sparse Transformer 类似；

*Big Bird* 与 Longformer 十分相似，同时配备局部注意力与少数具有全局注意力跨度的预选 token，但 Big Bird 用一种新机制替换了膨胀注意力：所有 token 都关注一组随机 token。这一设计的动机在于，注意力模式可以被视为[有向图](https://en.wikipedia.org/wiki/Directed_graph)，而[随机图](https://en.wikipedia.org/wiki/Random_graph)具有信息能在任意一对节点之间快速流动的性质。

*Longformer* 在较低的层使用较小的窗口，在较高的层使用较大的窗口。消融实验表明，这种配置比反向或固定尺寸的配置效果更好。较低的层不使用膨胀滑动窗口，以便更好地学会利用紧邻的局部上下文。Longformer 还有分阶段的训练流程：起初用小窗口训练以从局部上下文学习，随后的训练阶段逐渐增大窗口并降低学习率。

## 基于内容的注意力

**Reformer**（[Kitaev, et al. 2020](https://arxiv.org/abs/2001.04451)）提出的改进旨在解决朴素 Transformer 的以下痛点：

- 自注意力模块内的时间与内存复杂度呈平方。
- 因为需要为反向传播存储激活，$N$ 层模型的内存是单层模型的 $N$ 倍。
- 中间的 FF 层往往非常大。

Reformer 提出了两项主要改动：

1. 用*局部敏感哈希（locality-sensitive hashing，LSH）注意力*替换点积注意力，把复杂度从 $\mathcal{O}(L^2)$ 降到 $\mathcal{O}(L\log L)$。
2. 用*可逆残差层*替换标准残差块，训练时只需存储一次激活而非 $N$ 次（即与层数成正比）。

**局部敏感哈希注意力**

在[注意力公式](#attention-and-self-attention)的 $\mathbf{Q} \mathbf{K}^\top$ 部分，我们只关心最大的元素，因为 softmax 之后只有大元素的贡献显著。对每个查询 $\mathbf{q}_i \in \mathbf{Q}$，我们要找 $\mathbf{K}$ 中离 $\mathbf{q}_i$ 最近的行向量。为了在高维空间中快速找到最近邻，Reformer 把[局部敏感哈希（LSH）](https://en.wikipedia.org/wiki/Locality-sensitive_hashing)纳入其注意力机制。

若哈希方案 $x \mapsto h(x)$ 能保持数据点之间的距离信息——相近的向量得到相似的哈希、远离的向量哈希差异很大——则称其为*局部敏感*的。Reformer 采用这样的哈希方案：给定固定随机矩阵 $\mathbf{R} \in \mathbb{R}^{d \times b/2}$（其中 $b$ 是超参数），哈希函数为 $h(x) = \arg\max([xR; −xR])$。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/LSH-attention-matrix.png)

*局部敏感哈希（LSH）注意力示意图。（图片来源：Kitaev, et al. 2020 图 1 右半部分。）*

在 LSH 注意力中，查询只能关注同一哈希桶中的位置，$S_i = \{j: h(\mathbf{q}_i) = h(\mathbf{k}_j)\}$。其流程如下（见图 20）：

- (a) 全量注意力的注意力矩阵往往是稀疏的。
- (b) 利用 LSH，我们可以按键与查询的哈希桶对二者排序对齐。
- (c) 令 $\mathbf{Q} = \mathbf{K}$（精确地说是 $\mathbf{k}_j = \mathbf{q}_j / |\mathbf{q}_j|$），使一个桶中键和查询的数量相等，便于分批。有趣的是，这种「共享 QK」配置并不影响 Transformer 的性能。
- (d) 应用批处理，把每 $m$ 个连续查询分为一组。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/LSH-attention.png)

*LSH 注意力包含 4 步：分桶、排序、分块与注意力计算。（图片来源：Kitaev, et al. 2020 图 1 左半部分。）*

**可逆残差网络**

Reformer 的另一项改进是使用*可逆残差层*（[Gomez et al. 2017](https://arxiv.org/abs/1707.04585)）。可逆残差网络的动机是按如下方式设计架构：任意给定层的激活都可以仅凭模型参数从下一层的激活中恢复。因此，我们可以在反向传播时重算激活而不是存储全部激活，从而节省内存。

给定层 $x \mapsto y$，普通残差层计算 $y = x + F(x)$，而可逆层把输入和输出都拆成对 $(x_1, x_2) \mapsto (y_1, y_2)$，然后执行：

$$
y_1 = x_1 + F(x_2),\; y_2 = x_2 + G(y_1) 
$$

而反推也很容易：

$$
x_2 = y_2 - G(y_1), \; x_1 = y_1 − F(x_2)
$$

Reformer 把同样的思想应用到 Transformer，在一个可逆网络块中组合注意力（$F$）与前馈层（$G$）：

$$
Y_1 = X_1 + \text{Attention}(X_2), \; Y_2 = X_2 + \text{FeedForward}(Y_1)
$$

通过把前馈计算分块可以进一步减少内存：

$$
Y_2 = [Y_2^{(1)}; \dots; Y_2^{(c)}] = [X_2^{(1)} + \text{FeedForward}(Y_1^{(1)}); \dots; X_2^{(c)} + \text{FeedForward}(Y_1^{(c)})]
$$

由此得到的可逆 Transformer 无需在每一层存储激活。

**Routing Transformer**（[Roy et al. 2021](https://arxiv.org/abs/2003.05997)）同样建立在键与查询的基于内容聚类之上。它不使用 LSH 那样的静态哈希函数，而是利用在线 $k$-means 聚类，并结合局部、时间上的稀疏注意力，把注意力复杂度从 $O(L^2)$ 降到 $O(L^{1.5})$。

在路由注意力中，键和查询都用 $k$-means 聚类方法聚类，并共享同一组质心 $\boldsymbol{\mu} = (\mu_1, \dots, \mu_k) \in \mathbb{R}^{k \times d}$。查询被路由到被分配到同一质心的键。总复杂度为 $O(Lkd + L^2d/k)$，其中 $O(Lkd)$ 用于聚类分配，$O(L^2d/k)$ 用于注意力计算。聚类质心用 EMA（指数移动平均）结合所有相关联的键和查询来更新。

在 Routing Transformer 的实验中，某些最佳配置只在模型最后两层以及一半的注意力头上启用路由注意力，另一半则使用局部注意力。他们还观察到，局部注意力是相当强的基线，而更大的注意力窗口总能带来更好的结果。

## 低秩注意力

**Linformer**（[Wang et al. 2020](https://arxiv.org/abs/2006.04768)）用*低秩*矩阵近似全量注意力矩阵，把时间与空间复杂度降为*线性*。Linformer 不用昂贵的 SVD 来求低秩分解，而是为键和值矩阵分别添加两个线性投影 $\mathbf{E}_i, \mathbf{F}_i \in \mathbb{R}^{L \times k}$，把它们的维度从 $L \times d$ 降到 $k \times d$。只要 $k \ll L$，注意力内存就能大幅降低。

$$
\begin{aligned}
\overline{\text{head}}_i 
&= \text{attn}(\mathbf{X}_q\mathbf{W}^q_i, \mathbf{E}_i\mathbf{X}_k\mathbf{W}^k_i, \mathbf{F}_i\mathbf{X}_v\mathbf{W}^v_i) \\
&= \underbrace{\text{softmax}\Big( \frac{\mathbf{X}_q\mathbf{W}^q_i (\mathbf{E}_i \mathbf{X}_k\mathbf{W}^k_i)^\top}{\sqrt{d}} \Big)}_{\text{low rank attention matrix }\bar{A} \in \mathbb{R}^{k \times d}} \mathbf{F}_i \mathbf{X}_v\mathbf{W}^v_i
\end{aligned}
$$

还可以应用一些额外技巧来进一步提升 Linformer 的效率：

- 投影层之间的参数共享，如按头共享、键值共享与按层（跨所有层）共享。
- 在不同的层使用不同的 $k$，因为较高层的头往往分布更偏斜（秩更低），因此较高的层可用更小的 $k$。
- 使用不同类型的投影；例如平均/最大池化、核与步长为 $L/k$ 的卷积层。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/linformer.png)

*(左) Informer 为键和值添加了两个投影层。(右) 推理时间随序列长度变化的曲线。（图片来源：Wang et al. 2020。）*

**随机特征注意力（Random Feature Attention，RFA）**（[Peng et al. 2021](https://arxiv.org/abs/2103.02143)）依赖*随机特征方法*（[Rahimi & Recht, 2007](https://people.eecs.berkeley.edu/~brecht/papers/07.rah.rec.nips.pdf)），用低秩特征映射近似自注意力中的 softmax 运算，以实现线性时间与空间复杂度。**Performers**（[Choromanski et al. 2021](https://arxiv.org/abs/2009.14794)）也采用随机特征注意力，并改进了核构造以进一步降低核近似误差。

RFA 背后的主要定理来自 [Rahimi & Recht, 2007](https://people.eecs.berkeley.edu/~brecht/papers/07.rah.rec.nips.pdf)：

> 设 $\phi: \mathbb{R}^d \to \mathbb{R}^{2D}$ 为一个非线性变换：
>
> $$
\phi(\mathbf{x}) = \frac{1}{\sqrt{D}}[\sin(\mathbf{w}_1^\top \mathbf{x}), \dots, \sin(\mathbf{w}_D^\top \mathbf{x}), \cos(\mathbf{w}_1^\top \mathbf{x}), \dots, \cos(\mathbf{w}_D^\top \mathbf{x})]^\top
$$
>
> 当 $d$ 维随机向量 $\mathbf{w}_i$ 独立同分布于 $\mathcal{N}(\mathbf{0}, \sigma^2\mathbf{I}_d)$ 时，
> $$
\mathbb{E}_{\mathbf{w}_i} [\phi(\mathbf{x}) \cdot \phi(\mathbf{y})] = \exp(-\frac{\| \mathbf{x} - \mathbf{y} \|^2}{2\sigma^2})
$$

$\exp(\mathbf{x} \cdot \mathbf{y})$ 的一个无偏估计为：

$$
\begin{aligned}
\exp(\mathbf{x} \cdot \mathbf{y} / \sigma^2) 
&= \exp(\frac{1}{2\sigma^2}(\|\mathbf{x}\|^2 + \|\mathbf{y}\|^2 - \|\mathbf{x} - \mathbf{y}\|^2) \\
&= \exp(\frac{\|\mathbf{x}\|^2}{2\sigma^2}) \exp(\frac{\|\mathbf{y}\|^2}{2\sigma^2}) ( - \frac{\|\mathbf{x} - \mathbf{y}\|^2}{2\sigma^2}) \\
&\approx \exp(\frac{\|\mathbf{x}\|^2}{2\sigma^2}) \exp(\frac{\|\mathbf{y}\|^2}{2\sigma^2})\;\phi(\mathbf{x})\cdot\phi(\mathbf{y}) \\
&= \exp(\frac{1}{\sigma^2})\;\phi(\mathbf{x})\cdot\phi(\mathbf{y}) & \text{; unit vectors}
\end{aligned}
$$

于是我们可以把注意力函数写成如下形式，其中 $\otimes$ 是外积运算，$\sigma^2$ 是温度：

$$
\begin{aligned}
\text{attn}(\mathbf{q}_t, \{\mathbf{k}_i\}, \{\mathbf{v}_i\}) 
&= \sum_i \frac{\exp(\mathbf{q}_t\cdot\mathbf{k}_i/\sigma^2)}{\sum_j \exp(\mathbf{q}_t\cdot\mathbf{k}_j/\sigma^2)}\mathbf{v}_i^\top
\approx \sum_i \frac{\phi(\mathbf{q}_t)\phi(\mathbf{k}_i)\mathbf{v}_i^\top}{\sum_j \phi(\mathbf{q}_t)\phi(\mathbf{k}_j)} \\
&= \color{green}{\frac{\phi(\mathbf{q}_t)^\top \sum_i \phi(\mathbf{k}_i)\otimes\mathbf{v}_i}{\phi(\mathbf{q}_t)^\top \sum_j \phi(\mathbf{k}_j)}
= \text{RFA}(\mathbf{q}_t, \{\mathbf{k}_i\}, \{\mathbf{v}_i\})}
\end{aligned}
$$

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/RFA.png)

*(左) 默认 softmax 运算的计算顺序。(右) 使用随机特征注意力时的计算顺序，比默认 softmax 便宜得多。（图片来源：Peng et al. 2021。）*

**因果注意力 RFA** 让时间步 $t$ 的 token 只关注更早的键和值 $\{\mathbf{k}_i\}_{i \leq t}, \{\mathbf{v}_i\}_{i \leq t}$。我们用一组变量 $(\mathbf{S}_t \in \mathbb{R}^{2D \times d}, \mathbf{z} \in \mathbb{R}^{2D})$ 来记录时间步 $t$ 的隐藏状态历史，类似于 RNN：

$$
\begin{aligned}
&\text{causal-RFA}(\mathbf{q}_t, \{\mathbf{k}_i\}_{i \leq t}, \{\mathbf{v}_i\}_{i \leq t}) = \frac{\phi(\mathbf{q}_t)^\top \mathbf{S}_t}{\phi(\mathbf{q}_t) \cdot \mathbf{z}_t} \\
&\text{where } 
\mathbf{S}_t = \mathbf{S}_{t-1} + \phi(\mathbf{k}_t)\otimes\mathbf{v}_t,
\quad 
\mathbf{z}_t = \mathbf{z}_{t-1} + \phi(\mathbf{k}_t)
\end{aligned}
$$

其中 $2D$ 是 $\phi(.)$ 的尺寸，为了得到合理的近似，$D$ 不应小于模型尺寸 $d$。

RFA 使自回归解码显著加速，内存复杂度主要取决于构造核 $\phi(.)$ 时 $D$ 的选择。

Performer 用正随机特征映射修改随机特征注意力以降低估计误差。它还让随机采样的 $\mathbf{w}_1, \dots, \mathbf{w}_D$ 保持正交，以进一步降低估计量的方差。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/performer.png)

*近似误差对比：(左) i.i.d 特征与正交特征；(右) sin/cos 特征与正随机特征。（图片来源：Choromanski et al. 2021。）*

# 用于强化学习的 Transformer

自注意力机制避免了把整个过去压缩进固定大小的隐藏状态，也不像 RNN 那样容易受梯度消失或梯度爆炸之苦。强化学习任务当然能从这些特性中受益。*然而*，即使在监督学习中 Transformer 也相当难训练，更不用说 RL 场景了。毕竟，稳定并训练一个 LSTM 智能体本身就已颇具挑战。

**Gated Transformer-XL**（**GTrXL**；[Parisotto, et al. 2019](https://arxiv.org/abs/1910.06764)）是用 Transformer 做 RL 的一次尝试。GTrXL 在 [Transformer-XL](#longer-attention-span-transformer-xl) 之上通过两项改动成功稳定了训练：

1. 层归一化只作用于残差模块中的输入流，而不作用于捷径流。这种重排的一个关键好处是允许原始输入从第一层一直流到最后一层。
2. 残差连接替换为 GRU 风格（Gated Recurrent Unit；[Chung et al., 2014](https://arxiv.org/abs/1412.3555)）的*门控*机制。

$$
\begin{aligned}
r &= \sigma(W_r^{(l)} y + U_r^{(l)} x) \\
z &= \sigma(W_z^{(l)} y + U_z^{(l)} x - b_g^{(l)}) \\
\hat{h} &= \tanh(W_g^{(l)} y + U_g^{(l)} (r \odot x)) \\
g^{(l)}(x, y) &= (1-z)\odot x + z\odot \hat{h}
\end{aligned}
$$

门控函数参数被显式初始化为接近恒等映射——这正是存在 $b_g$ 项的原因。$b_g > 0$ 极大地帮助加速学习。

![](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/gated-transformer-XL.png)

*Transformer-XL、层归一化重排后的 Transformer-XL 与 Gated Transformer-XL 的模型架构对比。（图片来源：Parisotto, et al. 2019 图 1。）*

**Decision Transformer**（**DT**；[Chen et al 2021](https://arxiv.org/abs/2106.01345)）把强化学习问题表述为*条件序列建模*的过程：在期望回报、过去状态与动作的条件下输出最优动作。因此，使用 Transformer 架构就成了顺理成章的选择。Decision Transformer 面向[离策略 RL](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#key-concepts)，模型只能访问由其他策略收集的固定轨迹集合。

为了鼓励模型学会如何行动以达成期望回报，它向模型输入期望的未来回报（return-to-go）$\hat{R} = \sum_{t’=t}^T r_{t’}$，而非当前奖励。轨迹由一系列三元组（return-to-go $\hat{R}_t$、状态 `s\_t`、动作 `a\_t`）组成，作为 Transformer 的输入序列：

$$
\tau = (\hat{R}_1, s_1, a_1, \hat{R}_2, s_2, a_2, \dots, \hat{R}_T, s_T, a_T)
$$

分别为 return-to-go、状态和动作添加并训练三个线性层以提取 token 嵌入。预测头学习预测与输入 token $s_t$ 对应的 $a_t$。训练对离散动作使用交叉熵损失，对连续动作使用 MSE。在他们的实验中，预测状态或 return-to-go 并未带来性能提升。

实验将 DT 与若干无模型 RL 算法基线进行了比较，结果表明：

- 在低数据量场景下，DT 比行为克隆更高效；
- DT 能很好地建模回报的分布；
- 拥有长上下文对取得好结果至关重要；
- DT 可以在稀疏奖励下工作。

# 引用

引用格式：

> Weng, Lilian. (Jan 2023). The transformer family version 2.0. Lil'Log. https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/.

或者

```
@article{weng2023transformer,
  title   = "The Transformer Family Version 2.0",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io",
  year    = "2023",
  month   = "Jan",
  url     = "https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/"
}
```

# 参考文献

[1] Ashish Vaswani, et al. [“Attention is all you need.”](http://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf) NIPS 2017.

[2] Rami Al-Rfou, et al. [“Character-level language modeling with deeper self-attention.”](https://arxiv.org/abs/1808.04444) AAAI 2019.

[3] Olah & Carter, [“Attention and Augmented Recurrent Neural Networks”](http://doi.org/10.23915/disti), Distill, 2016.

[4] Sainbayar Sukhbaatar, et al. [“Adaptive Attention Span in Transformers”](https://arxiv.org/abs/1905.07799). ACL 2019.

[5] Rewon Child, et al. [“Generating Long Sequences with Sparse Transformers”](https://arxiv.org/abs/1904.10509) arXiv:1904.10509 (2019).

[6] Nikita Kitaev, et al. [“Reformer: The Efficient Transformer”](https://arxiv.org/abs/2001.04451) ICLR 2020.

[7] Alex Graves. (“Adaptive Computation Time for Recurrent Neural Networks”)[https://arxiv.org/abs/1603.08983]

[8] Niki Parmar, et al. [“Image Transformer”](https://arxiv.org/abs/1802.05751) ICML 2018.

[9] Zihang Dai, et al. [“Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context.”](https://arxiv.org/abs/1901.02860) ACL 2019.

[10] Aidan N. Gomez, et al. [“The Reversible Residual Network: Backpropagation Without Storing Activations”](https://arxiv.org/abs/1707.04585) NIPS 2017.

[11] Mostafa Dehghani, et al. [“Universal Transformers”](https://arxiv.org/abs/1807.03819) ICLR 2019.

[12] Emilio Parisotto, et al. [“Stabilizing Transformers for Reinforcement Learning”](https://arxiv.org/abs/1910.06764) arXiv:1910.06764 (2019).

[13] Rae et al. [“Compressive Transformers for Long-Range Sequence Modelling.”](https://arxiv.org/abs/1911.05507) 2019.

[14] Press et al. [“Train Short, Test Long: Attention With Linear Biases Enables Input Length Extrapolation.”](https://arxiv.org/abs/2108.12409) ICLR 2022.

[15] Wu, et al. [“DA-transformer: Distance Aware Transformer”](https://aclanthology.org/2021.naacl-main.166) 2021.

[16] Elabyad et al. [“Depth-Adaptive Transformer.”](https://arxiv.org/abs/1910.10073) ICLR 2020.

[17] Schuster et al. [“Confident Adaptive Language Modeling”](https://arxiv.org/abs/2207.07061) 2022.

[18] Qiu et al. [“Blockwise self-attention for long document understanding”](https://arxiv.org/abs/1911.02972) 2019

[19] Roy et al. [“Efficient Content-Based Sparse Attention with Routing Transformers.”](https://arxiv.org/abs/2003.05997) 2021.

[20] Ainslie et al. [“ETC: Encoding Long and Structured Inputs in Transformers.”](https://aclanthology.org/2020.emnlp-main.19/) EMNLP 2019.

[21] Beltagy et al. [“Longformer: The long-document transformer.”](https://arxiv.org/abs/2004/05150) 2020.

[22] Zaheer et al. [“Big Bird: Transformers for Longer Sequences.”](https://arxiv.org/abs/2007.14062) 2020.

[23] Wang et al. [“Linformer: Self-Attention with Linear Complexity.”](https://arxiv.org/abs/2006.04768) arXiv preprint arXiv:2006.04768 (2020).

[24] Tay et al. 2020 [“Sparse Sinkhorn Attention.”](https://arxiv.org/abs/2002.11296) ICML 2020.

[25] Peng et al. [“Random Feature Attention.”](https://arxiv.org/abs/2103.02143) ICLR 2021.

[26] Choromanski et al. [“Rethinking Attention with Performers.”](https://arxiv.org/abs/2009.14794) ICLR 2021.

[27] Khandelwal et al. [“Generalization through memorization: Nearest neighbor language models.”](https://arxiv.org/abs/1911.00172) ICLR 2020.

[28] Yogatama et al. [“Adaptive semiparametric language models.”](https://arxiv.org/abs/2102.02557) ACL 2021.

[29] Wu et al. [“Memorizing Transformers.”](https://arxiv.org/abs/2203.08913) ICLR 2022.

[30] Su et al. [“Roformer: Enhanced transformer with rotary position embedding.”](https://arxiv.org/abs/2104.09864) arXiv preprint arXiv:2104.09864 (2021).

[31] Shaw et al. [“Self-attention with relative position representations.”](https://arxiv.org/abs/1803.02155) arXiv preprint arXiv:1803.02155 (2018).

[32] Tay et al. [“Efficient Transformers: A Survey.”](https://arxiv.org/abs/2009.06732) ACM Computing Surveys 55.6 (2022): 1-28.

[33] Chen et al., [“Decision Transformer: Reinforcement Learning via Sequence Modeling”](https://arxiv.org/abs/2106.01345) arXiv preprint arXiv:2106.01345 (2021).
