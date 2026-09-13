---
title: "Transformer 家族"
title_en: "The Transformer Family"
source: https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/
crawled: 2026-09-08
translated: 2026-09-08
---

# Transformer 家族

> 原文：[The Transformer Family](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/) · Lilian Weng（翁荔）

> 受近期各类增强版 Transformer 模型进展的启发，本文介绍如何改进朴素（vanilla）Transformer，以获得更长的注意力跨度、更少的内存与计算消耗、RL 任务求解能力等。

距我上一篇关于[注意力](https://lilianweng.github.io/posts/2018-06-24-attention/)的文章已近两年。新版与增强版 Transformer 的近期进展促使我就这一主题再写一篇，聚焦于如何改进朴素 Transformer，以实现更长的注意力跨度、更少的内存与计算消耗、RL 任务求解等。

### 符号

| 符号 | 含义 |
| --- | --- |
| $$d$$ | 模型尺寸 / 隐藏状态维度 / 位置编码尺寸。 |
| $$h$$ | 多头注意力层中的头数。 |
| $$L$$ | 输入序列的片段长度。 |
| $$\mathbf{X} \in \mathbb{R}^{L \times d}$$ | 输入序列，每个元素已被映射为形状 $$d$$（与模型尺寸相同）的嵌入向量。 |
| $$\mathbf{W}^k \in \mathbb{R}^{d \times d_k}$$ | 键权重矩阵。 |
| $$\mathbf{W}^q \in \mathbb{R}^{d \times d_k}$$ | 查询权重矩阵。 |
| $$\mathbf{W}^v \in \mathbb{R}^{d \times d_v}$$ | 值权重矩阵。通常 $$d_k = d_v = d$$。 |
| $$\mathbf{W}^k_i, \mathbf{W}^q_i \in \mathbb{R}^{d \times d_k/h}; \mathbf{W}^v_i \in \mathbb{R}^{d \times d_v/h}$$ | 每个头的权重矩阵。 |
| $$\mathbf{W}^o \in \mathbb{R}^{d_v \times d}$$ | 输出权重矩阵。 |
| $$\mathbf{Q} = \mathbf{X}\mathbf{W}^q \in \mathbb{R}^{L \times d_k}$$ | 查询嵌入输入。 |
| $$\mathbf{K} = \mathbf{X}\mathbf{W}^k \in \mathbb{R}^{L \times d_k}$$ | 键嵌入输入。 |
| $$\mathbf{V} = \mathbf{X}\mathbf{W}^v \in \mathbb{R}^{L \times d_v}$$ | 值嵌入输入。 |
| $$S_i$$ | 第 $$i$$ 个查询 $$\mathbf{q}_i$$ 所关注的键位置的集合。 |
| $$\mathbf{A} \in \mathbb{R}^{L \times L}$$ | 长度 $$L$$ 的输入序列与自身之间的自注意力矩阵。$$\mathbf{A} = \text{softmax}(\mathbf{Q}\mathbf{K}^\top / \sqrt{d_k})$$。 |
| $$a_{ij} \in \mathbf{A}$$ | 查询 $$\mathbf{q}_i$$ 与键 $$\mathbf{k}_j$$ 之间的标量注意力分数。  
| $$\mathbf{P} \in \mathbb{R}^{L \times d}$$ | 位置编码矩阵，第 $$i$$ 行 $$\mathbf{p}_i$$ 是输入 $$\mathbf{x}_i$$ 的位置编码。 |

## 注意力与自注意力

*注意力（Attention）*是神经网络中的一种机制，模型可以学会通过选择性地关注给定数据集来做预测。注意力的大小由学到的权重量化，因此输出通常形如加权平均。

*自注意力（Self-attention）*是一类注意力机制：模型利用同一样本观测的其他部分来预测该样本的一部分。概念上它与[非局部均值（non-local means）](https://en.wikipedia.org/wiki/Non-local_means)颇为相似。另注意自注意力是置换不变的；换言之，它是集合上的运算。

注意力/自注意力有多种形式，Transformer（[Vaswani et al., 2017](https://arxiv.org/abs/1706.03762)）依赖*缩放点积注意力*：给定查询矩阵 $$\mathbf{Q}$$、键矩阵 $$\mathbf{K}$$ 和值矩阵 $$\mathbf{V}$$，输出是值向量的加权和，其中分配给每个值槽位的权重由查询与相应键的点积确定：

$$
\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}(\frac{\mathbf{Q} {\mathbf{K}}^\top}{\sqrt{d_k}})\mathbf{V}
$$

对查询与键向量 $$\mathbf{q}_i, \mathbf{k}_j \in \mathbb{R}^d$$（查询与键矩阵中的行向量），有标量分数：

$$
a_{ij} = \text{softmax}(\frac{\mathbf{q}_i {\mathbf{k}_j}^\top}{\sqrt{d_k}})
= \frac{\exp(\mathbf{q}_i {\mathbf{k}_j}^\top)}{ \sqrt{d_k} \sum_{r \in S_i} \exp(\mathbf{q}_i {\mathbf{k}_r}^\top) }
$$ 

其中 $$S_i$$ 是第 $$i$$ 个查询关注的键位置集合。

感兴趣可看我旧[文](https://lilianweng.github.io/posts/2018-06-24-attention/#a-family-of-attention-mechanisms)中其他类型的注意力。

## 多头自注意力

*多头自注意力*模块是 Transformer 的关键组件。多头机制不是只计算一次注意力，而是把输入切分成更小的块，然后并行地在每个子空间上计算缩放点积注意力。各独立的注意力输出被简单拼接并线性变换到期望维度。

$$
\begin{aligned}
\text{MultiHeadAttention}(\mathbf{X}_q, \mathbf{X}_k, \mathbf{X}_v) &= [\text{head}_1; \dots; \text{head}_h] \mathbf{W}^o \\ 
\text{where head}_i &= \text{Attention}(\mathbf{X}_q\mathbf{W}^q_i, \mathbf{X}_k\mathbf{W}^k_i, \mathbf{X}_v\mathbf{W}^v_i)
\end{aligned}
$$

其中 $$[.;.]$$ 是拼接操作。$$\mathbf{W}^q_i, \mathbf{W}^k_i \in \mathbb{R}^{d \times d_k/h}, \mathbf{W}^v_i \in \mathbb{R}^{d \times d_v/h}$$ 是把大小 $$L \times d$$ 的输入嵌入映射为查询、键、值矩阵的权重矩阵。$$\mathbf{W}^o \in \mathbb{R}^{d_v \times d}$$ 是输出线性变换。所有权重都应在训练中学习。

![Multi-head scaled dot-product attention](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/multi-head-attention.png)

*图 1：多头缩放点积注意力机制示意图。（图片来源：[Vaswani, et al., 2017](https://arxiv.org/abs/1706.03762) 图 2）*

## Transformer

**Transformer**（为与其他增强版区分，下称"朴素 Transformer"；[Vaswani, et al., 2017](https://arxiv.org/abs/1706.03762)）模型采用编码器-解码器架构，与许多 [NMT](https://lilianweng.github.io/posts/2018-06-24-attention/#born-for-translation) 模型常用的一样。后来仅解码器 Transformer 被证明在语言建模任务上表现出色，如 [GPT 和 BERT](https://lilianweng.github.io/posts/2019-01-31-lm/#openai-gpt)。

**编码器-解码器架构**

**编码器**生成基于注意力的表示，能够从大上下文中定位特定信息。它由 6 个恒等模块堆叠组成，每个模块含两个子模块：*多头自注意力*层和*逐位置（point-wise）*全连接前馈网络。所谓逐位置，指对序列中每个元素施加相同的线性变换（相同权重）。这也可视为滤波器大小为 1 的卷积层。每个子模块有残差连接和层归一化。所有子模块输出同维度 $$d$$ 的数据。

Transformer **解码器**的功能是从编码表示中检索信息。架构与编码器相当相似，区别是每个重复模块中解码器含两个而非一个多头注意力子模块。第一个多头注意力子模块被*掩码*以防止位置关注未来。

![Transformer](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/transformer.png)

*图 2：朴素 Transformer 模型的架构。（图片来源：[图 17](https://lilianweng.github.io/posts/2018-06-24-attention/#full-architecture)）*

**位置编码**

由于自注意力运算是置换不变的，使用恰当的**位置编码**为模型提供*顺序信息*很重要。位置编码 $$\mathbf{P} \in \mathbb{R}^{L \times d}$$ 与输入嵌入同维度，因此可以直接加在输入上。朴素 Transformer 考虑了两类编码：

(1) *正弦位置编码*定义如下，给定 token 位置 $$i=1,\dots,L$$ 和维度 $$\delta=1,\dots,d$$：

$$
\text{PE}(i,\delta) = 
\begin{cases}
\sin(\frac{i}{10000^{2\delta'/d}}) & \text{if } \delta = 2\delta'\\
\cos(\frac{i}{10000^{2\delta'/d}}) & \text{if } \delta = 2\delta' + 1\\
\end{cases}
$$

这样，位置编码的每个维度对应不同维度上不同波长的正弦波，波长从 $$2\pi$$ 到 $$10000 \cdot 2\pi$$。

![Transformer](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/sinoidual-positional-encoding.png)

*图 3：$$L=32$$、$$d=128$$ 的正弦位置编码。取值在 -1（黑）与 1（白）之间，0 为灰色。*

(2) *学习式位置编码*，顾名思义，为每个元素分配一个学到的列向量，编码其*绝对*位置（[Gehring, et al. 2017](https://arxiv.org/abs/1705.03122)）。

**快速后续**

继朴素 Transformer 之后，[Al-Rfou et al. (2018)](https://arxiv.org/abs/1808.04444) 加入一组辅助损失，使深度 Transformer 模型在字符级语言建模上训练成为可能，且超越了 LSTM。使用的辅助任务有几类：
- 不只在序列末端产生一个预测，每个*中间位置*也被要求做出正确预测，强制模型在更小的上下文中预测（如上下文窗口开头的几个 token）。
- 每个中间 Transformer 层也用于预测。随着训练推进，较低层被加权为对总损失的贡献越来越小。
- 序列中每个位置可以预测多个目标，即未来 token 的两个或更多预测。

![Transformer](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/transformer-aux-losses.png)

*图 4：深度 Transformer 用于字符级语言建模的辅助预测任务。（图片来源：[Al-Rfou et al. (2018)](https://arxiv.org/abs/1808.04444)）*

## 自适应计算时间（ACT）

**自适应计算时间（Adaptive Computation Time**，简称 **ACT**；[Graves, 2016](https://arxiv.org/abs/1603.08983)）是动态决定循环神经网络需要多少计算步骤的机制。distill.pub 上有一篇关于 ACT 的精彩[教程](https://distill.pub/2016/augmented-rnns/#adaptive-computation-time)。

设有一个 RNN 模型 $$\mathcal{R}$$，由输入权重 $$W_x$$、参数化状态转移函数 $$\mathcal{S}(.)$$、一组输出权重 $$W_y$$ 和输出偏置 $$b_y$$ 组成。给定输入序列 $$(x_1, \dots, x_L)$$，输出序列 $$(y_1, \dots, y_L)$$ 计算为：

$$
s_t = \mathcal{S}(s_{t-1}, W_x x_t), \quad y_t = W_y s_t + b_y\quad\text{for }t=1, \dots, L
$$

ACT 使上述 RNN 设定对每个输入元素执行可变数量的步骤。多步计算产生一列中间状态 $$(s_t^1, \dots, s_t^{N(t)})$$ 和输出 $$(y_t^1, \dots, y_t^{N(t)})$$——它们共享同一状态转移函数 $$\mathcal{S}(.)$$，以及同样的输出权重 $$W_y$$ 和偏置 $$b_y$$：

$$
\begin{aligned}
s_t^0 &= s_{t-1} \\
s_t^n &= \mathcal{S}(s_{t}^{n-1}, x_t^n) = \mathcal{S}(s_{t}^{n-1}, x_t + \delta_{n,1}) \text{ for } n=1, \dots, N(t)\\
y_t^n &= W_y s_t^n + b_y
\end{aligned}
$$

其中 $$\delta_{n,1}$$ 是指示输入步是否已递增的二值标志。

步数 $$N(t)$$ 由一个额外的 sigmoid 停止单元 $$h$$ 决定，它带权重矩阵 $$W_h$$ 和偏置 $$b_h$$，对第 $$t$$ 个输入元素在中间步 $$n$$ 输出停止概率 $$p_t^n$$：

$$
h_t^n = \sigma(W_h s_t^n + b_h)
$$

为允许计算在单步后停止，ACT 引入小常数 $$\epsilon$$（如 0.01），每当累积概率超过 $$1-\epsilon$$，计算就停止。

$$
\begin{aligned}
N(t) &= \min(\min\{n': \sum_{n=1}^{n'} h_t^n \geq 1 -\epsilon\}, M) \\
p_t^n &= \begin{cases}
h_t^n & \text{if }n < N(t) \\
R(t) = 1 - \sum_{n=1}^{N(t)-1} h_t^n & \text{if }n= N(t)\\
\end{cases}
\end{aligned}
$$

其中 $$M$$ 是允许的中间步数上限。

最终状态和输出是平均场更新：

$$
s_t = \sum_{n=1}^{N(t)} p_t^n s_t^n,\quad y_t = \sum_{n=1}^{N(t)} p_t^n y_t^n
$$

![ACT computation graph](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/ACT-computation-graph.png)

*图 5：带 ACT 机制的 RNN 计算图。（图片来源：[Graves, 2016](https://arxiv.org/abs/1603.08983)）*

为避免对每个输入不必要的深思，ACT 在损失函数中加入*思考代价（ponder cost）* $$\mathcal{P}(x) = \sum_{t=1}^L N(t) + R(t) $$，以鼓励更少的中间计算步数。

## 改进注意力跨度

改进注意力跨度的目标是让自注意力可用的上下文更长、更高效、更灵活。

### 更长的注意力跨度（Transformer-XL）

朴素 Transformer 的注意力跨度固定且有限。模型每次更新只能关注同一片段内的其他元素，信息无法跨越分离的定长片段流动。

这种*上下文分割*带来几个问题：
- 模型无法捕捉极长的长期依赖。
- 每个片段开头的前几个 token 缺少或只有稀薄上下文，难以预测。
- 评估昂贵。片段每右移一位，新片段就要从头重新处理，尽管有大量重叠 token。

**Transformer-XL**（[Dai et al., 2019](https://arxiv.org/abs/1901.02860)；"XL" 意为 "extra long"）用两项主要修改解决上下文分割问题：
1. 片段间复用隐藏状态。
2. 采用适合复用状态的新位置编码。

**隐藏状态复用**

通过持续使用先前片段的隐藏状态，模型被引入片段间的循环连接。

![Training phrase of Transformer-XL](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/transformer-XL-training.png)

*图 6：朴素 Transformer 与 Transformer-XL（片段长度 4）训练阶段的对比。（图片来源：[Dai et al., 2019](https://arxiv.org/abs/1901.02860) 图 2 左半部分）。*

把模型第 $$(\tau + 1)$$ 个片段第 $$n$$ 层的隐藏状态记为 $$\mathbf{h}_{\tau+1}^{(n)} \in \mathbb{R}^{L \times d}$$。除同片段上一层的隐藏状态 $$\mathbf{h}_{\tau+1}^{(n-1)}$$ 外，它还依赖上一片段同层的隐藏状态 $$\mathbf{h}_{\tau}^{(n)}$$。通过纳入先前隐藏状态的信息，模型把注意力跨度在过去延伸得远得多，跨越多个片段。

$$
\begin{aligned}
\color{red}{\widetilde{\mathbf{h}}_{\tau+1}^{(n-1)}} &= [\text{stop-gradient}(\mathbf{h}_{\tau}^{(n-1)}) \circ \mathbf{h}_{\tau+1}^{(n-1)}] \\
\mathbf{Q}_{\tau+1}^{(n)} &= \mathbf{h}_{\tau+1}^{(n-1)}\mathbf{W}^q \\
\mathbf{K}_{\tau+1}^{(n)} &= \color{red}{\widetilde{\mathbf{h}}_{\tau+1}^{(n-1)}} \mathbf{W}^k \\
\mathbf{V}_{\tau+1}^{(n)} &= \color{red}{\widetilde{\mathbf{h}}_{\tau+1}^{(n-1)}} \mathbf{W}^v \\
\mathbf{h}_{\tau+1}^{(n)} &= \text{transformer-layer}(\mathbf{Q}_{\tau+1}^{(n)}, \mathbf{K}_{\tau+1}^{(n)}, \mathbf{V}_{\tau+1}^{(n)})
\end{aligned}
$$

注意键和值都依赖扩展后的隐藏状态，而查询只用当前步的隐藏状态。拼接操作 $$[. \circ .]$$ 沿序列长度维进行。

**相对位置编码**

为配合这种新形式的注意力跨度，Transformer-XL 提出了新型的位置编码。若沿用朴素 Transformer 的做法编码绝对位置，先前片段与当前片段会被赋予相同编码，这并不理想。

为使位置信息在片段间连贯流动，Transformer-XL 改为编码*相对*位置——因为对做出良好预测而言，知道键向量 $$\mathbf{k}_{\tau, j}$$ 与其查询 $$\mathbf{q}_{\tau, i}$$ 之间的位置偏移 $$i-j$$ 大概就足够了。

若省略标量 $$1/\sqrt{d_k}$$ 与 softmax 的归一化项但保留位置编码，我们可以把位置 $$i$$ 的查询与位置 $$j$$ 的键之间的注意力分数写为：

$$
\begin{aligned}
a_{ij} 
&= \mathbf{q}_i {\mathbf{k}_j}^\top = (\mathbf{x}_i + \mathbf{p}_i)\mathbf{W}^q ((\mathbf{x}_j + \mathbf{p}_j)\mathbf{W}^k)^\top \\
&= \mathbf{x}_i\mathbf{W}^q {\mathbf{W}^k}^\top\mathbf{x}_j^\top + \mathbf{x}_i\mathbf{W}^q {\mathbf{W}^k}^\top\mathbf{p}_j^\top + \mathbf{p}_i\mathbf{W}^q {\mathbf{W}^k}^\top\mathbf{x}_j^\top + \mathbf{p}_i\mathbf{W}^q {\mathbf{W}^k}^\top\mathbf{p}_j^\top
\end{aligned}
$$

Transformer-XL 把上述四项重参数化如下：

$$
a_{ij}^\text{rel} = 
\underbrace{ \mathbf{x}_i\mathbf{W}^q \color{blue}{ {\mathbf{W}_E^k}^\top } \mathbf{x}_j^\top }_\text{content-based addressing} + 
\underbrace{ \mathbf{x}_i\mathbf{W}^q \color{blue}{ {\mathbf{W}_R^k}^\top } \color{green}{\mathbf{r}_{i-j}^\top} }_\text{content-dependent positional bias} + 
\underbrace{ \color{red}{\mathbf{u}} \color{blue}{ {\mathbf{W}_E^k}^\top } \mathbf{x}_j^\top }_\text{global content bias} + 
\underbrace{ \color{red}{\mathbf{v}} \color{blue}{ {\mathbf{W}_R^k}^\top } \color{green}{\mathbf{r}_{i-j}^\top} }_\text{global positional bias}
$$

- 把 $$\mathbf{p}_j$$ 替换为相对位置编码 $$\mathbf{r}_{i-j} \in \mathbf{R}^{d}$$；
- 把 $$\mathbf{p}_i\mathbf{W}^q$$ 替换为两个不同项中的可训练参数 $$\mathbf{u}$$（用于内容）和 $$\mathbf{v}$$（用于位置）；
- 把 $$\mathbf{W}^k$$ 拆成两个矩阵：用于内容信息的 $$\mathbf{W}^k_E$$ 和用于位置信息的 $$\mathbf{W}^k_R$$。

### 自适应注意力跨度

Transformer 的一个关键优势是捕捉长期依赖的能力。视上下文而定，模型有时可能比其他时候更想往远处关注；或一个注意力头可能与另一个头有不同的注意力模式。如果注意力跨度能灵活调整长度、只在需要时才往回看更远，将有助于降低计算与内存开销，从而支持模型中更长的最大上下文尺寸。

这正是**自适应注意力跨度（Adaptive Attention Span）**的动机。[Sukhbaatar, et al., (2019)](https://arxiv.org/abs/1905.07799) 提出了一种寻找最优注意力跨度的自注意力机制。他们假设不同注意力头在同一上下文窗口内可能打出不同的分数（见图 7），因此最优跨度应每个头分别训练。

![Attention per head](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/attention-per-head.png)

*图 7：同一模型中的两个注意力头 A 与 B 在同一上下文窗口内分配不同的注意力。头 A 更多关注近处 token，头 B 均匀地回看更远的过去。（图片来源：[Sukhbaatar, et al. 2019](https://arxiv.org/abs/1905.07799)）*

给定第 $$i$$ 个 token，我们需要计算它与位置 $$j \in S_i$$ 上其他键之间的注意力权重，其中 $$S_i$$ 定义第 $$i$$ 个 token 的上下文窗口。

$$
\begin{aligned}
e_{ij} &= \mathbf{q}_i {\mathbf{k}_j}^\top \\ 
a_{ij} &= \text{softmax}(e_{ij}) = \frac{\exp(e_{ij})}{\sum_{r=i-s}^{i-1} \exp(e_{ir})} \\
\mathbf{y}_i &= \sum_{r=i-s}^{i-1}a_{ir}\mathbf{v}_r = \sum_{r=i-s}^{i-1}a_{ir}\mathbf{x}_r\mathbf{W}^v
\end{aligned}
$$

加入一个*软掩码函数* $$m_z$$ 来控制可调的有效注意力跨度，它把查询与键之间的距离映射为 [0, 1] 值。$$m_z$$ 由 $$z \in [0, s]$$ 参数化，$$z$$ 待学习：

$$
m_z(x) = \text{clamp}(\frac{1}{R}(R+z-x), 0, 1)
$$

其中 $$R$$ 是定义 $$m_z$$ 软度的超参数。

![Soft masking function](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/soft-masking-function.png)

*图 8：自适应注意力跨度中使用的软掩码函数。（图片来源：[Sukhbaatar, et al. 2019](https://arxiv.org/abs/1905.07799)。）*

软掩码函数施加于注意力权重的 softmax 元素上：

$$
a_{ij} = \frac{m_z(i-j)\exp(s_{ij})}{\sum_{r=i-s}^{i-1}m_z(i-r) \exp(s_{ir})}
$$

上式中 $$z$$ 可微，因此与模型其他部分联合训练。参数 $$z^{(i)}, i=1, \dots, h$$ *每个头分别*学习。此外，损失函数对 $$\sum_{i=1}^h z^{(i)}$$ 加了额外的 L1 惩罚。

借助[自适应计算时间](#adaptive-computation-time-act)，该方法可进一步增强为注意力跨度长度灵活、随当前输入动态自适应。时间 $$t$$ 某注意力头的跨度参数 $$z_t$$ 是 sigmoid 函数，$$z_t = S \sigma(\mathbf{v} \cdot \mathbf{x}_t +b)$$，其中向量 $$\mathbf{v}$$ 与标量偏置 $$b$$ 与其他参数联合学习。

在带自适应注意力跨度的 Transformer 实验中，[Sukhbaatar, et al. (2019)](https://arxiv.org/abs/1905.07799) 发现一个普遍趋势：较低的层不需要很长的注意力跨度，而较高层的少数注意力头可能使用格外长的跨度。自适应注意力跨度还大幅减少 FLOPS，尤其在注意力层多、上下文长度大的大模型中。

### 局部化注意力跨度（Image Transformer）

Transformer 最初也最流行的用例是语言建模。文本序列是按明确定义的时间顺序排列的一维序列，注意力跨度随上下文增大而线性增长。

然而若想把 Transformer 用于图像，如何定义上下文范围或顺序并不清楚。**Image Transformer**（[Parmer, et al 2018](https://arxiv.org/abs/1802.05751)）在 Transformer 框架内采用类似序列建模的图像生成表述。此外，Image Transformer 把自注意力跨度限制在*局部*邻域，使模型能扩展到并行处理更多图像，并保持似然损失可解。

图像条件生成仍保留编码器-解码器架构：
- 编码器生成源图像的上下文化逐像素通道表示；
- 解码器*自回归地*生成输出图像，每个时间步每像素一个通道。

把待生成的当前像素的表示记为查询 $$\mathbf{q}$$。其表示将被用于计算 $$\mathbf{q}$$ 的其他位置是键向量 $$\mathbf{k}_1, \mathbf{k}_2, \dots$$，它们共同构成记忆矩阵 $$\mathbf{M}$$。$$\mathbf{M}$$ 的范围定义像素查询 $$\mathbf{q}$$ 的上下文窗口。

Image Transformer 引入了两类局部化 $$\mathbf{M}$$，如下图所示。

![Attention patterns in Image Transformer](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/image-transformer-attention.png)

*图 9：Image Transformer 中视觉输入的一维与二维注意力跨度示意。黑线标记一个查询块，青色勾勒出像素 q 的实际注意力范围。（图片来源：[Parmer et al, 2018](https://arxiv.org/abs/1802.05751) 图 2）*

(1) *一维局部注意力*：输入图像按[光栅扫描](https://en.wikipedia.org/wiki/Raster_scan#Scanning_pattern)顺序（从左到右、从上到下）展平。线性化图像随后被划分为不重叠的查询块。上下文窗口由与 $$\mathbf{q}$$ 同一查询块中的像素加上该查询块之前生成的固定数量附加像素组成。

(2) *二维局部注意力*：图像被划分为多个不重叠的矩形查询块。查询像素可关注同一记忆块中的所有其他像素。为确保左上角像素也有有效上下文窗口，记忆块分别向上、向左、向右扩展固定量。

## 更少时间与内存开销

本节介绍为降低计算时间与内存消耗而对 Transformer 做的若干改进。

### 稀疏注意力矩阵分解（Sparse Transformers）

朴素 Transformer 的计算与内存开销随序列长度平方增长，因此难以应用于很长的序列。

**Sparse Transformer**（[Child et al., 2019](https://arxiv.org/abs/1904.10509)）通过稀疏矩阵分解引入*分解自注意力（factorized self-attention）*，使训练序列长度高达 16,384、数百层的稠密注意力网络成为可能——否则在现代硬件上不可行。

给定一组注意力连接模式 $$\mathcal{S} = \{S_1, \dots, S_n\}$$，每个 $$S_i$$ 记录第 $$i$$ 个查询向量关注的键位置集合。

$$
\begin{aligned}
\text{Attend}(\mathbf{X}, \mathcal{S}) &= \Big( a(\mathbf{x}_i, S_i) \Big)_{i \in \{1, \dots, L\}} \\
\text{ where } a(\mathbf{x}_i, S_i) &= \text{softmax}\Big(\frac{(\mathbf{x}_i \mathbf{W}^q)(\mathbf{x}_j \mathbf{W}^k)_{j \in S_i}^\top}{\sqrt{d_k}}\Big) (\mathbf{x}_j \mathbf{W}^v)_{j \in S_i}
\end{aligned}
$$

注意尽管 $$S_i$$ 的大小不固定，$$a(\mathbf{x}_i, S_i)$$ 的大小总是 $$d_v$$，因此 $$\text{Attend}(\mathbf{X}, \mathcal{S}) \in \mathbb{R}^{L \times d_v}$$。

在自回归模型中，一个注意力跨度定义为 $$S_i = \{j: j \leq i\}$$，允许每个 token 关注过去所有位置。

在分解自注意力中，集合 $$S_i$$ 被分解为依赖的*树*，使得对每对 $$(i, j)$$（$$j \leq i$$），存在一条把 $$i$$ 连回 $$j$$ 的路径，$$i$$ 可以直接或间接关注 $$j$$。

确切地说，集合 $$S_i$$ 被分成 $$p$$ 个*不重叠*子集，第 $$m$$ 个子集记作 $$A^{(m)}_i \subset S_i, m = 1,\dots, p$$。于是输出位置 $$i$$ 与任意 $$j$$ 之间的路径最大长度为 $$p + 1$$。例如，若 $$(j, a, b, c, \dots, i)$$ 是 $$i$$ 与 $$j$$ 之间的索引路径，则有 $$j \in A_a^{(1)}, a \in A_b^{(2)}, b \in A_c^{(3)}, \dots$$，依此类推。

**稀疏分解注意力**

Sparse Transformer 提出两类分解注意力。以 2D 图像输入为例结合图 10 理解这些概念更容易。

![Sparse attention](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/sparse-attention.png)

*图 10：上排展示 (a) Transformer、(b) 带跨步注意力的 Sparse Transformer、(c) 带固定注意力的 Sparse Transformer 的注意力连接模式。下排为相应的自注意力连接矩阵。注意上下两排比例不同。（图片来源：[Child et al., 2019](https://arxiv.org/abs/1904.10509) + 若干额外标注。）*

(1) *跨步（Strided）*注意力，步长 $$\ell \sim \sqrt{n}$$。这对图像数据很有效，因为结构与跨步对齐。图像情形下，每个像素关注光栅扫描顺序中前面全部 $$\ell$$ 个像素（自然覆盖图像整个宽度），然后这些像素关注同一列中的其他像素（由另一个注意力连接子集定义）。

$$
\begin{aligned}
A_i^{(1)} &= \{ t, t+1, \dots, i\} \text{, where } t = \max(0, i - \ell) \\
A_i^{(2)} &= \{j: (i-j) \mod \ell = 0\}
\end{aligned}
$$

(2) *固定（Fixed）*注意力。一小组 token 概括先前位置，并把该信息传播给所有未来位置。

$$
\begin{aligned}
A_i^{(1)} &= \{j: \lfloor \frac{j}{\ell} \rfloor = \lfloor \frac{i}{\ell} \rfloor \} \\
A_i^{(2)} &= \{j: j \mod \ell \in \{\ell-c, \dots, \ell-1\} \}
\end{aligned}
$$

其中 $$c$$ 是超参数。若 $$c=1$$，它会限制表示而许多位置依赖少数位置。论文对 $$\ell \in \{ 128, 256 \}$$ 选 $$c\in \{ 8, 16, 32 \}$$。

**在 Transformer 中使用分解自注意力**

有三种方式在 Transformer 架构中使用稀疏分解注意力模式：
1. 每个残差块一种注意力类型然后交错，<br/>
$$\text{attention}(\mathbf{X}) = \text{Attend}(\mathbf{X}, A^{(n \mod p)}) \mathbf{W}^o$$，其中 $$n$$ 是当前残差块的索引。
2. 设置一个关注所有分解头关注位置的单头，<br/>
$$\text{attention}(\mathbf{X}) = \text{Attend}(\mathbf{X}, \cup_{m=1}^p A^{(m)}) \mathbf{W}^o $$。
3. 使用多头注意力机制，但与朴素 Transformer 不同，每个头可采用上面的模式 1 或 2。=> 该选项通常表现最佳。

Sparse Transformer 还提出一组改动使 Transformer 能训练到数百层，包括梯度检查点、反向传播时重算注意力与 FF 层、混合精度训练、高效的块稀疏实现等。详情请看[论文](https://arxiv.org/abs/1904.10509)。

### 局部敏感哈希（Reformer）

**Reformer** 模型（[Kitaev, et al. 2020](https://arxiv.org/abs/2001.04451)）的改进旨在解决 Transformer 的以下痛点：
- $$N$$ 层模型的内存是单层模型的 $$N$$ 倍，因为反向传播需要存储激活值。
- 中间 FF 层往往很大。
- 长度 $$L$$ 序列上的注意力矩阵在内存和时间上都常需 $$O(L^2)$$。

Reformer 提出两项主要改动：
1. 用*局部敏感哈希（LSH）注意力*替换点积注意力，把复杂度从 $$O(L^2)$$ 降到 $$O(L\log L)$$。
2. 用*可逆残差层*替换标准残差块，训练时只需存储一次激活值而非 $$N$$ 次（即与层数成正比）。

<a name="LSH" />**局部敏感哈希注意力**

在[注意力公式](#attention-and-self-attention)的 $$\mathbf{Q} \mathbf{K}^\top$$ 部分，我们只关心最大的元素，因为 softmax 后只有大元素贡献多。对每个查询 $$\mathbf{q}_i \in \mathbf{Q}$$，我们要找 $$\mathbf{K}$$ 中离 $$\mathbf{q}_i$$ 最近的行向量。为在高维空间中快速找最近邻，Reformer 把[局部敏感哈希（LSH）](https://en.wikipedia.org/wiki/Locality-sensitive_hashing)纳入其注意力机制。

哈希方案 $$x \mapsto h(x)$$ 若保持数据点间的距离信息——近的向量得到相似哈希、远的向量哈希差异很大——则称*局部敏感*。Reformer 采用这样的哈希方案：给定固定随机矩阵 $$\mathbf{R} \in \mathbb{R}^{d \times b/2}$$（$$b$$ 是超参），哈希函数为 $$h(x) = \arg\max([xR; −xR])$$。

<!-- If we omit the scalar in self-attention and summarize the denominator into a normalizing term $$Z(.)$$, an normal attention output looks as follows:

$$
\mathbf{o}_i = \sum_{j \in S_i} \exp(\mathbf{q}_i \cdot \mathbf{k}_j - Z(i, S_i)) \mathbf{v}_j \text{, where } S_i = \{j: j \leq i\}
$$ 
-->

![LSH attention matrix](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/LSH-attention-matrix.png)

*图 11：局部敏感哈希（LSH）注意力示意图。（图片来源：[Kitaev, et al. 2020](https://arxiv.org/abs/2001.04451) 图 1 右半部分）。*

在 LSH 注意力中，查询只能关注同一哈希桶中的位置，$$S_i = \{j: h(\mathbf{q}_i) = h(\mathbf{k}_j)\}$$。它按如下过程进行（见图 11）：
- (a) 全量注意力的注意力矩阵往往是稀疏的。
- (b) 用 LSH，我们可以按键与查询的哈希桶排序对齐。
- (c) 设 $$\mathbf{Q} = \mathbf{K}$$（确切地说 $$\mathbf{k}_j = \mathbf{q}_j / \|\mathbf{q}_j\|$$），使一个桶中键与查询数量相等，便于分批。有趣的是，这种"共享-QK"配置不影响 Transformer 的性能。
- (d) 施加分批，把 $$m$$ 个连续查询的块分到一组。

![LSH attention](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/LSH-attention.png)

*图 12：LSH 注意力含 4 步：分桶、排序、分块与注意力计算。（图片来源：[Kitaev, et al. 2020](https://arxiv.org/abs/2001.04451) 图 1 左半部分）。*

**可逆残差网络**

Reformer 的另一项改进是使用*可逆残差层*（[Gomez et al. 2017](https://arxiv.org/abs/1707.04585)）。可逆残差网络的动机是以这样的方式设计架构：任意给定层的激活值可以仅用模型参数从下一层的激活值恢复。于是我们可以通过反向传播时重算激活值而非存储全部激活值来节省内存。

给定一层 $$x \mapsto y$$，普通残差层做 $$y = x + F(x)$$，而可逆层把输入和输出都拆成对 $$(x_1, x_2) \mapsto (y_1, y_2)$$，然后执行：

$$
y_1 = x_1 + F(x_2),\; y_2 = x_2 + G(y_1) 
$$

反转很容易：

$$
x_2 = y_2 - G(y_1), \; x_1 = y_1 − F(x_2)
$$

Reformer 把同一思想应用于 Transformer，把注意力（$$F$$）与前馈层（$$G$$）组合进一个可逆网络块：

$$
Y_1 = X_1 + \text{Attention}(X_2), \; Y_2 = X_2 + \text{FeedForward}(Y_1)
$$

通过分块前馈计算可进一步减少内存：
$$
Y_2 = [Y_2^{(1)}; \dots; Y_2^{(c)}] = [X_2^{(1)} + \text{FeedForward}(Y_1^{(1)}); \dots; X_2^{(c)} + \text{FeedForward}(Y_1^{(c)})]
$$

所得的可逆 Transformer 无须在每层存储激活值。

## 使其循环（Universal Transformer）

**Universal Transformer**（[Dehghani, et al. 2019](https://arxiv.org/abs/1807.03819)）把 Transformer 的自注意力与 RNN 的循环机制相结合，旨在兼得 Transformer 的长期全局感受野与 RNN 学到的归纳偏置。

Universal Transformer 不经过固定层数，而是用[自适应计算时间](#adaptive-computation-time-act)动态调整步数。若固定步数，Universal Transformer 等价于一个跨层共享参数的多层 Transformer。

高层来看，Universal Transformer 可视为学习每个 token 隐藏状态表示的循环函数。循环函数在各 token 位置并行演化，位置间的信息通过自注意力共享。

![Universal Transformer Recurrent Step](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/universal-transformer-loop.png)

*图 13：Universal Transformer 如何对每个位置并行地反复精炼一组隐藏状态表示。（图片来源：[Dehghani, et al. 2019](https://arxiv.org/abs/1807.03819) 图 1）。*

给定长度 $$L$$ 的输入序列，Universal Transformer 在第 $$t$$ 步迭代更新表示 $$\mathbf{H}^t \in \mathbb{R}^{L \times d}$$，步数可调。第 0 步，$$\mathbf{H}^0$$ 初始化为与输入嵌入矩阵相同。所有位置在多头自注意力机制中并行处理，然后经过一个循环转移函数。

$$
\begin{aligned}
\mathbf{A}^t &= \text{LayerNorm}(\mathbf{H}^{t-1} + \text{MultiHeadAttention}(\mathbf{H}^{t-1} + \mathbf{P}^t) \\
\mathbf{H}^t &= \text{LayerNorm}(\mathbf{A}^{t-1} + \text{Transition}(\mathbf{A}^t))
\end{aligned}
$$

其中 $$\text{Transition}(.)$$ 是[可分离卷积](https://arxiv.org/abs/1610.02357)或由两个逐位置（即单独应用于 $$\mathbf{A}^t$$ 每行）仿射变换 + 一个 ReLU 组成的全连接神经网络。

位置编码 $$\mathbf{P}^t$$ 使用正弦位置信号但带额外的时间维：

$$
\text{PE}(i, t, \delta) = 
\begin{cases}
\sin(\frac{i}{10000^{2\delta'/d}}) \oplus \sin(\frac{t}{10000^{2\delta'/d}}) & \text{if } \delta = 2\delta'\\
\cos(\frac{i}{10000^{2\delta'/d}}) \oplus \cos(\frac{t}{10000^{2\delta'/d}}) & \text{if } \delta = 2\delta' + 1\\
\end{cases}
$$

![Universal Transformer](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/universal-transformer.png)

*图 14：Universal Transformer 的简化示意图。编码器与解码器共享同一基本循环结构，但解码器还关注编码器的最终表示 $$\mathbf{H}^T$$。（图片来源：[Dehghani, et al. 2019](https://arxiv.org/abs/1807.03819) 图 2）*

在 Universal Transformer 的自适应版本中，循环步数 $$T$$ 由 [ACT](#adaptive-computation-time-act) 动态决定。每个位置配备动态 ACT 停止机制。一旦某个逐 token 的循环块停止，它不再接受更多循环更新，只把当前值复制到下一步，直到所有块停止或模型达到最大步数限制。

## 为 RL 稳定训练（GTrXL）

自注意力机制避免把整个过去压缩进固定大小的隐藏状态，也不像 RNN 那样严重受梯度消失或爆炸之苦。强化学习任务当然能从这些特性中受益。*然而*，Transformer 即使在监督学习中都相当难训练，更别提 RL 场景了。毕竟，稳定并训练一个 LSTM 智能体本身就相当有挑战。

**Gated Transformer-XL（GTrXL**；[Parisotto, et al. 2019](https://arxiv.org/abs/1910.06764)）是用 Transformer 做 RL 的一次尝试。GTrXL 在 [Transformer-XL](#longer-attention-span-transformer-xl) 之上以两项改动成功稳定了训练：
1. 层归一化只施加于残差模块的输入流，而不施加于捷径流。这一重排的关键好处是允许原始输入从第一层流到最后一层。
2. 残差连接替换为 GRU 风格（Gated Recurrent Unit；[Chung et al., 2014](https://arxiv.org/abs/1412.3555)）的*门控*机制。

$$
\begin{aligned}
r &= \sigma(W_r^{(l)} y + U_r^{(l)} x) \\
z &= \sigma(W_z^{(l)} y + U_z^{(l)} x - b_g^{(l)}) \\
\hat{h} &= \tanh(W_g^{(l)} y + U_g^{(l)} (r \odot x)) \\
g^{(l)}(x, y) &= (1-z)\odot x + z\odot \hat{h}
\end{aligned}
$$

门控函数参数被显式初始化为接近恒等映射——这就是为什么有 $$b_g$$ 项。$$b_g > 0$$ 极大帮助加速学习。

![GTrXL](https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/gated-transformer-XL.png)

*图 15：Transformer-XL、层归一化重排的 Transformer-XL 与 Gated Transformer-XL 的模型架构对比。（图片来源：[Parisotto, et al. 2019](https://arxiv.org/abs/1910.06764) 图 1）*

---
引用格式：
```
@article{weng2020transformer,
  title   = "The Transformer Family",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2020",
  url     = "https://lilianweng.github.io/lil-log/2020/03/27/the-transformer-family.html"
}
```

## 参考文献

[1] Ashish Vaswani, et al. ["Attention is all you need."](http://papers.nips.cc/paper/7181-attention-is-all-you-need.pdf) NIPS 2017.

[2] Rami Al-Rfou, et al. ["Character-level language modeling with deeper self-attention."](https://arxiv.org/abs/1808.04444) AAAI 2019.

[3] Olah & Carter, ["Attention and Augmented Recurrent Neural Networks"](http://doi.org/10.23915/disti), Distill, 2016. 

[4] Sainbayar Sukhbaatar, et al. ["Adaptive Attention Span in Transformers"](https://arxiv.org/abs/1905.07799). ACL 2019.

[5] Rewon Child, et al. ["Generating Long Sequences with Sparse Transformers"](https://arxiv.org/abs/1904.10509) arXiv:1904.10509 (2019).

[6] Nikita Kitaev, et al. ["Reformer: The Efficient Transformer"](https://arxiv.org/abs/2001.04451) ICLR 2020.

[7] Alex Graves. ("Adaptive Computation Time for Recurrent Neural Networks")[https://arxiv.org/abs/1603.08983]

[8] Niki Parmar, et al. ["Image Transformer"](https://arxiv.org/abs/1802.05751) ICML 2018.

[9] Zihang Dai, et al. ["Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context."](https://arxiv.org/abs/1901.02860) ACL 2019.

[10] Aidan N. Gomez, et al. ["The Reversible Residual Network: Backpropagation Without Storing Activations"](https://arxiv.org/abs/1707.04585) NIPS 2017.

[11] Mostafa Dehghani, et al. ["Universal Transformers"](https://arxiv.org/abs/1807.03819) ICLR 2019.

[12] Emilio Parisotto, et al. ["Stabilizing Transformers for Reinforcement Learning"](https://arxiv.org/abs/1910.06764) arXiv:1910.06764 (2019).
