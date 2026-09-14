---
title: "均方误差（MSE）的导数是什么？"
title_en: "What is the derivative of the Mean Squared Error?"
source: https://sebastianraschka.com/faq/docs/mse-derivative.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 均方误差（MSE）的导数是什么？

均方误差（MSE）关于某个权重参数 \(w\_j\) 的偏导数非常好算，下面我一步步详细推导：

\[\begin{align}
\frac{\partial E}{\partial w\_j} &= \frac{\partial}{\partial w\_j} \frac{1}{2n} \sum\_{i=1}^{n} (t\_i - o\_i)^2 \\
&= \frac{1}{2n} \sum\_{i=1}^{n} \frac{\partial}{\partial w\_j} (t\_i - o\_i)^2 \quad [\text{chain rule}] \\
&= \frac{1}{2n} \sum\_{i=1}^{n} 2 (t\_i - o\_i) \frac{\partial}{\partial w\_j} (t\_i - o\_i) \quad [\text{sum rule}] \\
&= \frac{1}{n} \sum\_{i=1}^{n} (t\_i - o\_i) \left( \frac{\partial}{\partial w\_j} t\_i - \frac{\partial}{\partial w\_j} o\_i \right)\\
&= - \frac{1}{n} \sum\_{i=1}^{n} (t\_i - o\_i) \frac{\partial}{\partial w\_j} o\_i.
\end{align}\]

假设"输出"大概是由某个接受加权输入 "net" 的激活函数计算得出，那么如果要展开 \(\frac{\partial o\_i}{\partial w\_j}\)，我们最终会得到类似这样的结果：

\[\begin{align}
\frac{\partial E}{\partial w\_j} &= - \frac{1}{n} \sum\_{i=1}^{n} (t\_i - o\_i) \frac{\partial}{\partial w\_j} o\_i\\
& = - \frac{1}{n} \sum\_{i=1}^{n} (t\_i - o\_i) \frac{\partial o\_i}{\partial \text{net}\_i}\frac{\partial\text{net}\_i}{\partial {w\_j}}.
\end{align}\]
