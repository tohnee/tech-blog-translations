---
title: "逻辑 sigmoid 函数的导数是什么？"
title_en: "What is the derivative of the logistic sigmoid function?"
source: https://sebastianraschka.com/faq/docs/logistic-sigmoid-derivative.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 逻辑 sigmoid 函数的导数是什么？

逻辑 sigmoid 函数

\[\sigma(x) = \frac{1}{1 + e^{-x}},\]

的导数为

\[\frac{d}{dx} = \frac{e^{-x}}{(1 + e^{-x})^2}.\]

下面我们一步步地走一遍推导过程。
\(\begin{align}
\frac{d}{dx}\sigma(x) & = \frac{d}{dx} \frac{1}{1+e^{-x}}\\
& = \frac{d}{dx}\big( 1+ e^{-x} \big) ^{-1} \quad[\text{apply chain rule}]\\
& = -(1 + e^{-x})^{-2} \cdot \frac{d}{dx}(1+e^{-x}) \quad[\text{apply sum rule}] \\
& = -(1 + e^{-x})^{-2} \cdot \bigg(\frac{d}{dx}1 + \frac{d}{dx}e^{-x}\bigg) \\
& = -(1 + e^{-x})^{-2} \cdot \frac{d}{dx}e^{-x} \quad[\text{apply chain rule}]\\
& = -(1 + e^{-x})^{-2} \cdot e^{-x}\frac{d}{dx} (-x)\\
& = -(1 + e^{-x})^{-2} \cdot \big(- e^{-x} \big)\\
& = \frac{1}{(1 + e^{-x})^{2}} \cdot e^{-x} \\
& = \frac{e^{-x}}{(1 + e^{-x})^{2}}
\end{align}\)

我们还可以把导数进一步化简为表达式 \(\sigma(x)(1-\sigma(x))\)：
\(\begin{align}
\frac{e^{-x}}{(1 + e^{-x})^{2}} &= \frac{e^{-x}}{1 + e^{-x}}\cdot\frac{1}{1 + e^{-x}} \\
& = \frac{-1 + 1 + e^{-x}}{1 + e^{-x}}\cdot\frac{1}{1 + e^{-x}}\\
& = \bigg(\frac{-1 }{1 + e^{-x}} + \frac{1 + e^{-x} }{1 + e^{-x}} \bigg)\cdot\frac{1}{1 + e^{-x}}\\
& = \bigg(\frac{-1 }{1 + e^{-x}} + 1 \bigg)\cdot\frac{1}{1 + e^{-x}}\\
& = \bigg(1 - \frac{1 }{1 + e^{-x}} \bigg)\cdot\frac{1}{1 + e^{-x}}\\
& = \big(1-\sigma(x)\big) \cdot \sigma(x)
\end{align}\)
