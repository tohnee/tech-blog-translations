---
title: "PyTorch 中的交叉熵损失及其替代方案"
title_en: "Cross-Entropy Loss in PyTorch and Its Alternatives"
source: https://sebastianraschka.com/faq/docs/pytorch-crossentropy.html
crawled: 2026-09-06
translated: 2026-09-14
---

# PyTorch 中的交叉熵损失及其替代方案

PyTorch 之所以实现了多种交叉熵损失的变体，原因在于便利性和计算效率。

请记住，我们通常感兴趣的是最大化正确类别的似然。最大化似常常被改写为最大化对数似然，因为取对数可以把对特征的乘积变成求和，这在数值上更稳定、也更容易优化。出于类似的原因，我们最小化*负*对数似然而不是最大化对数似然。（更多细节可以参看我的[授课讲义](https://github.com/rasbt/stat479-deep-learning-ss19/blob/master/L08_logistic/L08_logistic_slides.pdf)。）

让我们简要总结一下。

- 设 $a$ 为 logistic sigmoid 函数输出的占位变量：

\[a := h(\mathbf{x})=\frac{1}{1+e^{- \mathbf{w}^\top \mathbf{x}}}.\]

- 我们希望

\[\begin{array}{ll}{P(y=0 | \mathbf{x}) \approx 1} & {\text { if } y=0} \\ {P(y=1 | \mathbf{x}) \approx 1} & {\text { if } y=1}\end{array},\]

这可以更紧凑地写作
\(P(y | \mathbf{x})=a^{y}(1-a)^{(1-y)}.\)

- 为此，我们在所有训练样本 $1, …, n$ 上最大化似然：

\[P\left(y^{[i]}, \ldots, y^{[n]} | \mathbf{x}^{[1]}, \ldots, \mathbf{x}^{[n]}\right)=\prod\_{i=1}^{n} P\left(y^{[i]} | \mathbf{x}^{[i]}\right).\]

为此我们可以定义似然函数 $L$：

\[\begin{aligned} L(\mathbf{w}) &=P(\mathbf{y} | \mathbf{x} ; \mathbf{w}) \\ &=\prod\_{i=1}^{n} P\left(y^{(i)} | x^{(i)} ; \mathbf{w}\right) \\ &=\prod\_{i=1}^{n}\left(\sigma\left(z^{(i)}\right)\right)^{y^{(i)}}\left(1-\sigma\left(z^{(i)}\right)\right)^{1-y^{(i)}} \end{aligned}\]

- 取对数后，我们得到一个更容易优化的目标：

\[\begin{aligned} l(\mathbf{w}) &=\log L(\mathbf{w}) \\ &=\sum\_{i=1}^{n}\left[y^{(i)} \log \left(\sigma\left(z^{(i)}\right)\right)+\left(1-y^{(i)}\right) \log \left(1-\sigma\left(z^{(i)}\right)\right)\right] \end{aligned}.\]

- 最后，为了把这个最大化问题变成最小化问题，以便使用 PyTorch 中的随机梯度下降优化器，我们关心的是*负*对数似然：

\[\begin{aligned} \mathcal{L}(\mathbf{w}) &=-l(\mathbf{w}) \\ &=-\sum\_{i=1}^{n}\left[y^{(i)} \log \left(\sigma\left(z^{(i)}\right)\right)+\left(1-y^{(i)}\right) \log \left(1-\sigma\left(z^{(i)}\right)\right)\right] \end{aligned}.\]

这等价于二元交叉熵：

\[H\_{\mathbf{a}}(\mathbf{y})=-\sum\_{i}\left(y^{[i]} \log \left(a^{[i]}\right)+\left(1-y^{[i]}\right) \log \left(1-a^{[i]}\right)\right)\]

而交叉熵的一般形式则是把这个概念扩展到 $K$ 个类别（假设采用独热编码形式）：

\[H\_{\mathbf{a}}(\mathbf{y})=\sum\_{i=1}^{n} \sum\_{k=1}^{K}-y\_{k}^{[i]} \log \left(a\_{k}^{[i]}\right).\]

（这类似于多项逻辑损失（multinomial logistic loss），也称为 softmax 回归。）

简而言之，交叉熵与负对数似然完全相同（这两个概念最初分别在计算机科学和统计学中独立发展，动机也不同，但事实证明在我们的分类语境中它们计算出的结果完全一样。）

PyTorch 把这些理论上可以互换的术语混合搭配使用。在 PyTorch 中，这些名称指的是接受不同输入参数（但计算同一件事）的实现。总结如下。

## PyTorch 损失输入混淆（速查表）

- `torch.nn.functional.binary_cross_entropy` 接受 logistic sigmoid 值作为输入
- `torch.nn.functional.binary_cross_entropy_with_logits` 接受 logit 作为输入
- `torch.nn.functional.cross_entropy` 接受 logit 作为输入（内部执行 log\_softmax）
- `torch.nn.functional.nll_loss` 类似于 cross\_entropy，但接受对数概率（log-softmax）值作为输入

下面是一个简短的演示：

注意，PyTorch 在 `torch.nn.functional.cross_entropy` 中把 `log_softmax` 与交叉熵损失计算合并，主要原因在于数值稳定性。恰好在数学上，损失对其输入的导数与 log-softmax 对其输入的导数可以漂亮地化简（我的课堂笔记中有更详细的推导。）

```python
## BINARY LABELS
>>> import torch

>>> labels = torch.tensor([1, 0, 1, 1, 1, 0], dtype=torch.float)
>>> logits = torch.tensor([2.5, -1.1, 1.2, 2.2, 0.1, -0.5], dtype=torch.float)
>>> torch.nn.functional.binary_cross_entropy_with_logits(logits, labels)
tensor(0.3088)
>>> torch.nn.functional.binary_cross_entropy(torch.sigmoid(logits), labels)
tensor(0.3088)

## MULTICLASS
import torch

>>> labels = torch.tensor([1, 0, 2], dtype=torch.long)
>>> logits = torch.tensor([[2.5, -0.5, 0.1],
...                        [-1.1, 2.5, 0.0],
...                        [1.2, 2.2, 3.1]], dtype=torch.float)
>>> torch.nn.functional.cross_entropy(logits, labels)
tensor(2.4258)
>>> torch.nn.functional.nll_loss(torch.nn.functional.log_softmax(logits, dim=1), labels)
tensor(2.4258)

## BINARY CROSS ENTROPY VS MULTICLASS IMPLEMENTATION
>>> import torch
>>> labels = torch.tensor([1, 0, 1], dtype=torch.float)
>>> probas = torch.tensor([0.9, 0.1, 0.8], dtype=torch.float)
>>> torch.nn.functional.binary_cross_entropy(probas, labels)
tensor(0.1446)

>>> labels = torch.tensor([1, 0, 1], dtype=torch.long)
>>> probas = torch.tensor([[0.1, 0.9],
...                        [0.9, 0.1],
...                        [0.2, 0.8]], dtype=torch.float)
>>> torch.nn.functional.nll_loss(torch.log(probas), labels)
tensor(0.1446)
```
