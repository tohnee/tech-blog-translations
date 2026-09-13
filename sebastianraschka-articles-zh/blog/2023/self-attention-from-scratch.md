---
title: "从零实现自注意力"
title_en: "Coding Self-Attention From Scratch"
source: https://sebastianraschka.com/blog/2023/self-attention-from-scratch.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 从零实现自注意力

> 原文：[Coding Self-Attention From Scratch](https://sebastianraschka.com/blog/2023/self-attention-from-scratch.html)

在本文中，我们将从零开始理解[自注意力](https://sebastianraschka.com/glossary/#mha "Multi-Head Attention (MHA)")的工作原理。这意味着我们会一步一步地亲手实现它。

自注意力机制自从在原始 Transformer 论文（[Attention Is All You Need](https://arxiv.org/abs/1706.03762)）中提出以来，已经成为许多最先进深度学习模型的基石，尤其是在自然语言处理（NLP）领域。既然自注意力如今无处不在，理解它的工作原理就非常重要。

![Self attention from scratch transformer](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/transformer.webp)

## 自注意力

深度学习中"注意力"这一概念[源于改进循环神经网络（RNN）以处理更长序列或句子的努力](https://arxiv.org/abs/1409.0473)。例如，考虑把一个句子从一种语言翻译成另一种语言：逐词翻译是行不通的。

![Self attention from scratch sentence](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/sentence.webp)

为了克服这个问题，注意力机制被引入，使模型在每个时间步都能访问所有序列元素。关键在于有选择地判断在特定上下文中哪些词最重要。2017 年，Transformer 架构引入了一种独立的自注意力机制，彻底摆脱了对 RNN 的需要。

（为了简洁起见，也为了让文章聚焦于自注意力的技术细节，我略去了部分动机介绍，但如果你有兴趣，我的[《Machine Learning with PyTorch and Scikit-Learn》](https://sebastianraschka.com/books/)一书第 16 章中有更多补充细节。）

[![Self attention from scratch paper](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/paper.webp)](https://arxiv.org/abs/1706.03762)

我们可以把自注意力看作这样一种机制：通过纳入输入的上下文信息，来增强输入嵌入的信息含量。换句话说，自注意力机制让模型能够衡量输入序列中不同元素的重要程度，并动态调整它们对输出的影响。这对语言处理任务尤其重要，因为一个词的含义会根据它在句子或文档中的上下文而改变。

注意，自注意力有许多变体。研究的重点之一是让自注意力更高效。然而，大多数论文仍然实现本文所讨论的原始缩放点积注意力机制，因为它通常能带来更优的准确率，而且对大多数训练大规模 Transformer 的公司来说，自注意力很少成为计算瓶颈。

在本文中，我们聚焦于原始的缩放点积注意力机制（即自注意力），它在实践中仍然是最流行、使用最广泛的注意力机制。不过，如果你对其他类型的注意力机制感兴趣，可以看看 [2020 年的 *Efficient Transformers: A Survey*](https://arxiv.org/abs/2009.06732) 和 [2023 年的 *A Survey on Efficient Training of Transformers*](https://arxiv.org/abs/2302.01107) 两篇综述，以及近期的 [FlashAttention](https://arxiv.org/abs/2205.14135) 论文。

## 对输入句子做嵌入

在开始之前，考虑一个我们想要送入自注意力机制的输入句子 *"Life is short, eat dessert first"*。与其他处理文本的建模方法（例如使用循环神经网络或卷积神经网络）类似，我们先创建一个句子嵌入。

为简单起见，这里的字典 `dc` 仅限于输入句子中出现的单词。在真实应用中，我们会考虑训练数据集中的所有单词（典型的词表规模在 3 万到 5 万之间）。

**输入：**

```python
sentence = 'Life is short, eat dessert first'

dc = {s:i for i,s in enumerate(sorted(sentence.replace(',', '').split()))}
print(dc)
```

**输出：**

```python
{'Life': 0, 'dessert': 1, 'eat': 2, 'first': 3, 'is': 4, 'short': 5}
```

接下来，我们用这个字典为每个单词分配一个整数索引：

**输入：**

```python
import torch

sentence_int = torch.tensor([dc[s] for s in sentence.replace(',', '').split()])
print(sentence_int)
```

**输出：**

```python
tensor([0, 4, 5, 2, 1, 3])
```

现在，利用输入句子的整数向量表示，我们可以使用一个[嵌入层](https://sebastianraschka.com/glossary/#token-embeddings "Token Embeddings")把输入编码成实数向量嵌入。这里我们使用 16 维嵌入，即每个输入单词由一个 16 维向量表示。由于这个句子由 6 个单词组成，我们将得到一个 \(6 \times 16\) 维的嵌入：

**输入：**

```python
torch.manual_seed(123)
embed = torch.nn.Embedding(6, 16)
embedded_sentence = embed(sentence_int).detach()

print(embedded_sentence)
print(embedded_sentence.shape)
```

**输出：**

```python
tensor([[ 0.3374, -0.1778, -0.3035, -0.5880,  0.3486,  0.6603, -0.2196, -0.3792,
          0.7671, -1.1925,  0.6984, -1.4097,  0.1794,  1.8951,  0.4954,  0.2692],
        [ 0.5146,  0.9938, -0.2587, -1.0826, -0.0444,  1.6236, -2.3229,  1.0878,
          0.6716,  0.6933, -0.9487, -0.0765, -0.1526,  0.1167,  0.4403, -1.4465],
        [ 0.2553, -0.5496,  1.0042,  0.8272, -0.3948,  0.4892, -0.2168, -1.7472,
         -1.6025, -1.0764,  0.9031, -0.7218, -0.5951, -0.7112,  0.6230, -1.3729],
        [-1.3250,  0.1784, -2.1338,  1.0524, -0.3885, -0.9343, -0.4991, -1.0867,
          0.8805,  1.5542,  0.6266, -0.1755,  0.0983, -0.0935,  0.2662, -0.5850],
        [-0.0770, -1.0205, -0.1690,  0.9178,  1.5810,  1.3010,  1.2753, -0.2010,
          0.4965, -1.5723,  0.9666, -1.1481, -1.1589,  0.3255, -0.6315, -2.8400],
        [ 0.8768,  1.6221, -1.4779,  1.1331, -1.2203,  1.3139,  1.0533,  0.1388,
          2.2473, -0.8036, -0.2808,  0.7697, -0.6596, -0.7979,  0.1838,  0.2293]])
torch.Size([6, 16])
```

## 定义权重矩阵

现在，我们来讨论被广泛使用的自注意力机制——缩放点积注意力（scaled dot-product attention），它被集成在 Transformer 架构之中。

自注意力使用三个权重矩阵，记作 \(\mathbf{W}\_q\)、\(\mathbf{W}\_k\) 和 \(\mathbf{W}\_v\)，它们作为模型参数在训练过程中被调整。这些矩阵的作用分别是把输入投影成序列的查询（query）、键（key）和值（value）分量。

相应的查询、键和值序列通过权重矩阵 \(\mathbf{W}\) 与嵌入输入 \(\mathbf{x}\) 之间的矩阵乘法得到：

- 查询序列：\(\mathbf{q}^{(i)}=\mathbf{W}\_q \mathbf{x}^{(i)}\)，其中 \(i \in[1, T]\)
- 键序列：\(\mathbf{k}^{(i)}=\mathbf{W}\_k \mathbf{x}^{(i)}\)，其中 \(i \in[1, T]\)
- 值序列：\(\mathbf{v}^{(i)}=\mathbf{W}\_v \mathbf{x}^{(i)}\)，其中 \(i \in[1, T]\)

索引 \(i\) 指输入序列中 token 的索引位置，序列长度为 \(T\)。

![Self attention from scratch attention matrices](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/attention-matrices.webp)

这里，\(\mathbf{q}^{(i)}\) 和 \(\mathbf{k}^{(i)}\) 都是维度为 \(d\_k\) 的向量。投影矩阵 \(\mathbf{W}\_{q}\) 和 \(\mathbf{W}\_{k}\) 的形状为 \(d\_k \times d\)，而 \(\mathbf{W}\_{v}\) 的形状为 \(d\_v \times d\)。

（需要注意，\(d\) 表示每个词向量 \(\mathbf{x}\) 的大小。）

由于我们要计算查询向量与键向量之间的点积，这两个向量必须含有相同数量的元素（\(d\_q = d\_k\)）。而值向量 \(\mathbf{v}^{(i)}\) 中的元素数量——它决定了最终上下文向量的大小——则是任意的。

所以，在接下来的代码演示中，我们设定 \(d\_q = d\_k = 24\)，并使用 \(d\_v = 28\)，按如下方式初始化投影矩阵：

**输入：**

```python
torch.manual_seed(123)

d = embedded_sentence.shape[1]

d_q, d_k, d_v = 24, 24, 28

W_query = torch.nn.Parameter(torch.rand(d_q, d))
W_key = torch.nn.Parameter(torch.rand(d_k, d))
W_value = torch.nn.Parameter(torch.rand(d_v, d))
```

## 计算未归一化的注意力权重

现在，假设我们想计算第二个输入元素的注意力向量——这里第二个输入元素充当查询：

![Self attention from scratch query](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/query.webp)

在代码中，如下所示：

**输入：**

```python
x_2 = embedded_sentence[1]
query_2 = W_query.matmul(x_2)
key_2 = W_key.matmul(x_2)
value_2 = W_value.matmul(x_2)

print(query_2.shape)
print(key_2.shape)
print(value_2.shape)
```

```python
torch.Size([24])
torch.Size([24])
torch.Size([28])
```

然后我们可以把它推广，为所有输入计算其余的键元素和值元素，因为下一步计算未归一化注意力权重 \(\omega\) 时会用到它们：

**输入：**

```python
keys = W_key.matmul(embedded_sentence.T).T
values = W_value.matmul(embedded_sentence.T).T

print("keys.shape:", keys.shape)
print("values.shape:", values.shape)
```

**输出：**

```python
keys.shape: torch.Size([6, 24])
values.shape: torch.Size([6, 28])
```

既然我们已经有了全部所需的键和值，就可以进入下一步，计算未归一化的注意力权重 \(\omega\)，如下图所示：

![Self attention from scratch omega](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/omega.webp)

如上图所示，我们把 \(\omega\_{i, j}\) 计算为查询序列与键序列之间的点积，\(\omega\_{i j}=\mathbf{q}^{(i)^{\top}} \mathbf{k}^{(j)}\)。

例如，我们可以按如下方式计算该查询与第 5 个输入元素（对应索引位置 4）之间的未归一化注意力权重：

**输入：**

```python
omega_24 = query_2.dot(keys[4])
print(omega_24)
```

**输出：**

```python
tensor(11.1466)
```

由于稍后计算注意力分数时需要用到它们，让我们按照前图所示，为所有输入 token 计算 \(\omega\) 值：

**输入：**

```python
omega_2 = query_2.matmul(keys.T)
print(omega_2)
```

**输出：**

```python
tensor([ 8.5808, -7.6597,  3.2558,  1.0395, 11.1466, -0.4800])
```

## 计算注意力分数

自注意力的下一步，是通过应用 softmax 函数把未归一化的注意力权重 \(\omega\) 归一化，得到归一化的注意力权重 \(\alpha\)。此外，在用 softmax 函数归一化之前，会先用 \(1/\sqrt{d\_k}\) 对 \(\omega\) 进行缩放，如下所示：

![Self attention from scratch attention scores](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/attention-scores.webp)

除以 \(d\_k\) 的平方根可以确保权重向量的欧氏长度大致处于同一量级。这有助于防止注意力权重变得过小或过大——过小或过大可能导致数值不稳定，或影响模型在训练中的收敛能力。

为什么恰好是 \(\sqrt{d\_k}\)？q 与 k 之间的点积是 \(d\_k\) 个独立项的和，每一项的方差约为 1。这意味着原始分数的方差会随 \(d\_k\) 线性增长。除以 \(\sqrt{d\_k}\) 就抵消了这种增长，把方差拉回约 1。

在代码中，我们可以按如下方式实现注意力权重的计算：

**输入：**

```python
import torch.nn.functional as F

attention_weights_2 = F.softmax(omega_2 / d_k**0.5, dim=0)
print(attention_weights_2)
```

**输出：**

```python
tensor([0.2912, 0.0106, 0.0982, 0.0625, 0.4917, 0.0458])
```

最后一步是计算上下文向量 \(\mathbf{z}^{(2)}\)，它是我们原始查询输入 \(\mathbf{x}^{(2)}\) 的一个按注意力加权后的版本，通过注意力权重把所有其他输入元素作为其上下文纳入进来：

![Self attention from scratch context vector](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/context-vector.webp)

在代码中，如下所示：

**输入：**

```python
context_vector_2 = attention_weights_2.matmul(values)

print(context_vector_2.shape)
print(context_vector_2)
```

**输出：**

```python
torch.Size([28])
tensor(torch.Size([28])
tensor([-1.5993,  0.0156,  1.2670,  0.0032, -0.6460, -1.1407, -0.4908, -1.4632,
         0.4747,  1.1926,  0.4506, -0.7110,  0.0602,  0.7125, -0.1628, -2.0184,
         0.3838, -2.1188, -0.8136, -1.5694,  0.7934, -0.2911, -1.3640, -0.2366,
        -0.9564, -0.5265,  0.0624,  1.7084])
```

注意，这个输出向量的维度（\(d\_v=28\)）比原始输入向量（\(d=16\)）更多，因为我们前面指定了 \(d\_v > d\)；不过嵌入大小的选择本来就是任意的。

## 多头注意力

在本文最开头的第一张图中，我们看到 Transformer 使用了一个叫*多头注意力*（multi-head attention）的模块。它与我们上面走查的自注意力机制（缩放点积注意力）是什么关系？

在缩放点积注意力中，输入序列通过三个分别代表查询、键和值的矩阵进行变换。在多头注意力的语境下，这三个矩阵可以被看作单个注意力头。下图总结了我们前面讲过的这个单一注意力头：

![Self attention from scratch single head](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/single-head.webp)

顾名思义，多头注意力包含多个这样的头，每个头都由查询、键和值矩阵组成。这一概念类似于卷积神经网络中使用多个卷积核的做法。

![Self attention from scratch multi head](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/multi-head.webp)

为了在代码中说明这一点，假设我们有 3 个注意力头，于是现在把 \(d' \times d\) 维的权重矩阵扩展为 \(3 \times d' \times d\)：

**输入：**

```python
h = 3
multihead_W_query = torch.nn.Parameter(torch.rand(h, d_q, d))
multihead_W_key = torch.nn.Parameter(torch.rand(h, d_k, d))
multihead_W_value = torch.nn.Parameter(torch.rand(h, d_v, d))
```

因此，每个查询元素现在是 \(3 \times d\_q\) 维的，其中 \(d\_q=24\)（这里，让我们聚焦于对应索引位置 2 的第 3 个元素）：

**输入：**

```python
multihead_query_2 = multihead_W_query.matmul(x_2)
print(multihead_query_2.shape)
```

**输出：**

```python
torch.Size([3, 24])
```

接下来，我们可以用类似的方式得到键和值：

**输入：**

```python
multihead_key_2 = multihead_W_key.matmul(x_2)
multihead_value_2 = multihead_W_value.matmul(x_2)
```

现在，这些键元素和值元素是专属于这个查询元素的。但与前面类似，我们还需要其他序列元素的键和值，才能计算该查询的注意力分数。做法之一是把输入序列嵌入扩展为大小 3，即注意力头的数量：

**输入：**

```python
stacked_inputs = embedded_sentence.T.repeat(3, 1, 1)
print(stacked_inputs.shape)
```

**输出：**

```python
torch.Size([3, 16, 6])
```

现在，我们可以通过 `via torch.bmm()`（批量矩阵乘法）计算所有的键和值：

**输入：**

```python
multihead_keys = torch.bmm(multihead_W_key, stacked_inputs)
multihead_values = torch.bmm(multihead_W_value, stacked_inputs)
print("multihead_keys.shape:", multihead_keys.shape)
print("multihead_values.shape:", multihead_values.shape)
```

**输出：**

```python
multihead_keys.shape: torch.Size([3, 24, 6])
multihead_values.shape: torch.Size([3, 28, 6])
```

现在我们得到了在第一个维度上代表三个注意力头的张量。第三个和第二个维度分别指单词数量和嵌入大小。为了让值和键更直观、易于解读，我们将交换第二个和第三个维度，得到与原始输入序列 `embedded_sentence` 具有相同维度结构的张量：

**输入：**

```python
multihead_keys = multihead_keys.permute(0, 2, 1)
multihead_values = multihead_values.permute(0, 2, 1)
print("multihead_keys.shape:", multihead_keys.shape)
print("multihead_values.shape:", multihead_values.shape)
```

**输出：**

```python
multihead_keys.shape: torch.Size([3, 6, 24])
multihead_values.shape: torch.Size([3, 6, 28])
```

然后，我们按照与之前相同的步骤计算未缩放的注意力权重 \(\omega\) 和注意力权重 \(\alpha\)，再进行缩放 softmax 计算，为输入元素 \(\mathbf{x}^{(2)}\) 得到一个 \(h \times d\_v\)（此处为 \(3 \times d\_v\)）维的上下文向量 \(\mathbf{z}\)。

## 交叉注意力

在上面的代码走查中，我们设定了 \(d\_q = d\_k = 24\) 和 \(d\_v=28\)。换句话说，我们对查询序列和键序列使用了相同的维度。虽然值矩阵 \(\mathbf{W}\_v\) 常被选为与查询和键矩阵相同的维度（例如 PyTorch 的 [MultiHeadAttention](https://pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html) 类中就是这样），但我们也可以为值维度任选一个大小。

由于这些维度有时不太好记，下面用一张图总结一下我们目前讲过的所有内容，它描绘了单个注意力头中的各种张量尺寸。

![Self attention from scratch summary](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/summary.webp)

上面这幅图对应的是 Transformer 中使用的*自*注意力机制。这种注意力机制还有一种变体我们尚未讨论，那就是*交叉*注意力（cross-attention）。

![Self attention from scratch cross attention](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/cross-attention.webp)

什么是交叉注意力？它与自注意力有何不同？

在自注意力中，我们处理的是同一个输入序列。而在交叉注意力中，我们把两个*不同*的输入序列混合或组合起来。在上面原始 Transformer 架构的例子中，就是左侧编码器模块返回的序列，与右侧解码器部分正在处理的输入序列。

注意，在交叉注意力中，两个输入序列 \(\mathbf{x}\_1\) 和 \(\mathbf{x}\_2\) 可以拥有不同数量的元素，但它们的嵌入维度必须一致。

下图展示了交叉注意力的概念。如果我们令 \(\mathbf{x}\_1 = \mathbf{x}\_2\)，这就等价于自注意力。

![Self attention from scratch cross attention summary](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/cross-attention-summary.webp)

（注意，查询通常来自解码器，而键和值通常来自编码器。）

这在代码中如何实现？之前在本文开头实现自注意力机制时，我们用以下代码计算第二个输入元素的查询，以及所有的键和值：

**输入：**

```python
torch.manual_seed(123)

d = embedded_sentence.shape[1]
print("embedded_sentence.shape:", embedded_sentence.shape:)

d_q, d_k, d_v = 24, 24, 28

W_query = torch.rand(d_q, d)
W_key = torch.rand(d_k, d)
W_value = torch.rand(d_v, d)

x_2 = embedded_sentence[1]
query_2 = W_query.matmul(x_2)
print("query.shape", query_2.shape)

keys = W_key.matmul(embedded_sentence.T).T
values = W_value.matmul(embedded_sentence.T).T

print("keys.shape:", keys.shape)
print("values.shape:", values.shape)
```

**输出：**

```python
embedded_sentence.shape: torch.Size([6, 16])
queries.shape: torch.Size([24])
keys.shape: torch.Size([6, 24])
values.shape: torch.Size([6, 28])
```

交叉注意力中唯一的变化是，我们现在有了第二个输入序列，例如一个有 8 个而非 6 个输入元素的第二个句子。这里，假设这是一个有 8 个 token 的句子。

**输入：**

```python
embedded_sentence_2 = torch.rand(8, 16) # 2nd input sequence

keys = W_key.matmul(embedded_sentence_2.T).T
values = W_value.matmul(embedded_sentence_2.T).T

print("keys.shape:", keys.shape)
print("values.shape:", values.shape)
```

**输出：**

```python
keys.shape: torch.Size([8, 24])
values.shape: torch.Size([8, 28])
```

注意，与自注意力相比，键和值现在有 8 行而不是 6 行。其他一切保持不变。

我们在上文谈了很多语言 Transformer。在原始 Transformer 架构中，交叉注意力在语言翻译场景下从输入句子生成输出句子时非常有用。输入句子代表一个输入序列，译文代表第二个输入序列（两个句子的单词数可以不同）。

另一个广泛使用交叉注意力的模型是 Stable Diffusion。如 [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) 所述，Stable Diffusion 在 U-Net 模型中生成的图像与用于条件控制的文本提示之间使用交叉注意力——这篇原始论文描述了 Stable Diffusion 模型，后来 Stability AI 采用它实现了广为人知的 Stable Diffusion 模型。

![Self attention from scratch diffusion](https://sebastianraschka.com/images/blog/2023/self-attention-from-scratch/diffusion.webp)

## 结论

在本文中，我们通过逐步编码的方式了解了自注意力是如何工作的。接着，我们把这一概念扩展到了多头注意力——大型语言 Transformer 中被广泛使用的组件。在讨论完自注意力和多头注意力之后，我们又引入了另一个概念：交叉注意力，它是自注意力的一种变体，可以应用在两个不同的序列之间。

这些信息量已经相当大了。就让我们把"如何用这个多头注意力模块训练神经网络"留到未来的文章中吧。
