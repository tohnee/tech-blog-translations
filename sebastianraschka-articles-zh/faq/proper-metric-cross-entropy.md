---
title: "交叉熵损失是合格的度量吗？"
title_en: "Is the cross-entropy loss a proper metric?"
source: https://sebastianraschka.com/faq/docs/proper-metric-cross-entropy.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 交叉熵损失是合格的度量吗？

考虑两个向量或点 \(\mathbf{v}\) 和 \(\mathbf{w}\)，以及它们的距离 \(d(\mathbf{v}, \mathbf{w})\)。

一个合格的度量（proper metric）需要满足以下准则：

1. 两点之间的距离总是非负的 \(d(\mathbf{v}, \mathbf{w}) \geq 0.\) 而且，距离只在两点完全相同时才为零，即 $\mathbf{v} = \mathbf{w}.$$
2. 距离是对称的，即 \(d(\mathbf{v}, \mathbf{w}) = d(\mathbf{w}, \mathbf{v}).\)
3. 距离函数对任意三点 \(\mathbf{v}, \mathbf{w}, \mathbf{x}\) 满足*三角不等式*，即
   \(d(\mathbf{v}, \mathbf{w}) \leq d(\mathbf{v}, \mathbf{x}) + d(\mathbf{x}, \mathbf{w}).\)

交叉熵用于衡量两个概率分布之间的距离。在机器学习语境中，当我们在由 *n* 个训练样本组成的数据集上训练逻辑回归或神经网络分类器时，使用类别标签 *y* 与预测概率 *p* 之间的离散交叉熵损失（CE）：

\[\mathrm{CE}(\mathbf{y}, \mathbf{p}) = -\frac{1}{n} \sum\_{i=1}^n y^{(i)} \cdot \log \left(p^{(i)}\right).\]

同样为简单起见，我们只看两个数据点之间的交叉熵函数（*H*）：

\[H(y, p) = - y \cdot \log(p).\]

**准则 1。** 交叉熵损失满足第一条准则的一半。距离总是非负的，因为概率得分是 [0, 1] 区间内的数。因此，\(\log(p)\) 的取值介于 \(-\infty\) 和 0 之间。关键在于 \*H\* 函数（见上文）带有一个负号。因此，交叉熵的取值介于 \(\infty\) 和 0 之间，从而满足准则 1 的一个方面。

然而，对于两个完全相同的点，交叉熵损失并不为零。例如 \(H(0.9, 0.9) = - 0.9 \log(0.9) = 0.095.\)

**准则 2。** 交叉熵损失违反了第二条准则，因为它不是对称的：\(- y \cdot \log(p) \neq - p \cdot \log(y).\)

我们用一个具体的数值例子来说明：

\[-1 \cdot \log(0.5) = 0.693\]
\[-0.5 \cdot \log(1) = 0.\]

**准则 3。** 交叉熵损失满足三角不等式吗，即
\(H(r, p) \geq H(r, q) + H(q, p)?\)

不满足。我们可以用一个例子说明。假设取 \(r=0.9, p=0.5, q=0.4.\) 我们有

\[H(0.9, 0.5) = 0.624\]
\[H(0.9, 0.4) = 0.825\]
\[H(0.4, 0.5) = 0.277.\]

可以看到 \(0.624 \geq 0.825 + 0.277\) 并不成立。

我们可以得出结论：交叉熵损失虽是通过（随机）梯度下降训练神经网络的一个有用的损失函数，但它并不是一个合格的距离度量，因为上述三条准则它一条都不满足。
