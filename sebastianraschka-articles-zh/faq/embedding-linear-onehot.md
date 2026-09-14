---
title: "嵌入层即作用于独热 token 上的线性层"
title_en: "Embedding Layers as Linear Layers on One-Hot Tokens"
source: https://sebastianraschka.com/faq/docs/embedding-linear-onehot.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 嵌入层即作用于独热 token 上的线性层

> 原文：[Embedding Layers as Linear Layers on One-Hot Tokens](https://sebastianraschka.com/faq/docs/embedding-linear-onehot.html) · Sebastian Raschka's FAQ

当线性层接收的输入是独热（one-hot）编码的 token 时，嵌入查表与一个不带偏置的线性层会给出相同的结果。两种实现存储的是同一组学习到的数值，区别主要在于访问这些数值的方式。

假设一个分词器的词表大小为 \(V\)，我们想要的嵌入维度为 \(d\)。嵌入层存储

\[E \in \mathbb{R}^{V \times d}.\]

对于 token ID \(i\)，查表返回 \(E\) 的第 \(i\) 行。这就是把嵌入层看作一张学习得到的表的常见视角。

![嵌入查表为一个批次的 token 索引从嵌入矩阵中选取相应的行](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/embeddings-and-linear-layers/3.png)

我们也可以把 token ID \(i\) 表示为独热向量

\[e\_i \in \mathbb{R}^{V}.\]

\(e\_i\) 中除了位置 \(i\) 上的元素外全为零。与嵌入矩阵相乘得到

\[e\_i^\top E = E\_i.\]

这些零把所有未被选中的行从求和中消去，唯一的 1 保留了第 \(i\) 行。因此结果与 `E[i]` 完全相同。

对于一个批次或序列，把独热向量堆叠成一个矩阵即可。该矩阵与 \(E\) 相乘会为每个 token 位置选取一行嵌入，产生的张量与批次化的嵌入查表相同。

![独热编码的 token 向量乘以权重矩阵，选出与嵌入查表相同的行](https://sebastianraschka.com/images/LLMs-from-scratch-images/bonus/embeddings-and-linear-layers/4.png)

转置通常是在代码中造成困惑的部分。在 PyTorch 中，`nn.Linear(V, d, bias=False)` 以 \(d \times V\) 的形状存储其权重，并计算输入乘以转置后的权重。因此，为了匹配形状为 \(V \times d\) 的嵌入矩阵，线性层的权重要设为 \(E^\top\)。

在实践中我们使用嵌入操作，因为构造独热向量会很浪费。对于一个 50,000 大小的词表，每个 token 都会变成一个长度为 50,000、包含 49,999 个零的向量。嵌入层跳过了这种表示，直接收集所需的行。

梯度也遵循同样的等价关系。只有被批次中 token 选中的行会收到更新，重复出现的 token ID 会把各自的贡献累积到同一行上。

有一个限定条件值得牢记：查表相对于独热向量是线性的，但它并不是整数 token ID 的线性函数，因为 token ID 是类别型标签，其数值大小顺序没有几何意义。
