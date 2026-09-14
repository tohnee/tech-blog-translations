---
title: "tanh 与 Logistic Sigmoid 之间的关系"
title_en: "The Relationship Between Tanh and the Logistic Sigmoid"
source: https://sebastianraschka.com/faq/docs/tanh-sigmoid-relationship.html
crawled: 2026-09-06
translated: 2026-09-14
---

# tanh 与 Logistic Sigmoid 之间的关系

简短的回答是：是的！

双曲正切（tanh）和 logistic sigmoid（$\sigma$）函数定义如下：

\[\tanh(z) = \frac{e^x - e^{-x}}{e^x + e^{-x}}, \quad \sigma(x) = \frac{1}{1+e^{-x}}.\]

如果把这两个函数并排画出来，它们的关系几乎一眼就能看出来：

![../../images/faq/tanh-sigmoid-relationship/tanh-sigmoid.png](https://sebastianraschka.com/images/faq/tanh-sigmoid-relationship/tanh-sigmoid.png)

由于 logistic sigmoid 函数关于原点对称并返回 [0, 1] 范围内的值，我们可以写出如下关系：

\[1 - \sigma(x) = \sigma(-x),\]

即，

\[1 - \frac{1}{1+e^{-x}} = \frac{1}{1+e^{x}}.\]

现在，为了看清 tanh 与 $\sigma$ 之间的关系，我们把 tanh 函数整理成相似的形式：

\[\begin{align}
\tanh(x) &= \frac{e^x - e^{-x}}{e^x + e^{-x}} \\\\
&= \frac{e^x + e^{-x} - 2e^{-x}}{e^x + e^{-x}} \\\\
&= 1 + \frac{-2e^{-x}}{e^x + e^{-x}} \\\\
&= 1 - \frac{2}{e^{2x}+ 1}
\end{align}\]

再从 logistic sigmoid 的角度看，我们有：

\[\begin{align}
\tanh(x) = 1 - \frac{2}{e^{2x}+ 1} &= 1 - 2\sigma(-2x) \\
&= 1 - 2 (1 - \sigma(2x)) \\
&= 1 - 2 + 2\sigma(2x) \\
&= 2 \sigma(2x) -1 \\
\end{align}\]

因此我们可以得出结论：tanh 函数只是 logistic sigmoid 函数的一个重新缩放版本。
