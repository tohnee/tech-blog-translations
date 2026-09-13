---
title: "What is the derivative of the Mean Squared Error?"
source: https://sebastianraschka.com/faq/docs/mse-derivative.html
crawled: 2026-09-06
---

# What is the derivative of the Mean Squared Error?

The partial derivative of the mean squared error with respect to a weight parameter \(w\_j\) is very simple to compute, as I outlined verbosely below:

\[\begin{align}
\frac{\partial E}{\partial w\_j} &= \frac{\partial}{\partial w\_j} \frac{1}{2n} \sum\_{i=1}^{n} (t\_i - o\_i)^2 \\
&= \frac{1}{2n} \sum\_{i=1}^{n} \frac{\partial}{\partial w\_j} (t\_i - o\_i)^2 \quad [\text{chain rule}] \\
&= \frac{1}{2n} \sum\_{i=1}^{n} 2 (t\_i - o\_i) \frac{\partial}{\partial w\_j} (t\_i - o\_i) \quad [\text{sum rule}] \\
&= \frac{1}{n} \sum\_{i=1}^{n} (t\_i - o\_i) \left( \frac{\partial}{\partial w\_j} t\_i - \frac{\partial}{\partial w\_j} o\_i \right)\\
&= - \frac{1}{n} \sum\_{i=1}^{n} (t\_i - o\_i) \frac{\partial}{\partial w\_j} o\_i.
\end{align}\]

Supposing that the “output” is probably computed by some activation function that takes the weighted inputs “net,” we end up with something like this, if we were to expand \(\frac{\partial o\_i}{\partial w\_j}\):

\[\begin{align}
\frac{\partial E}{\partial w\_j} &= - \frac{1}{n} \sum\_{i=1}^{n} (t\_i - o\_i) \frac{\partial}{\partial w\_j} o\_i\\
& = - \frac{1}{n} \sum\_{i=1}^{n} (t\_i - o\_i) \frac{\partial o\_i}{\partial \text{net}\_i}\frac{\partial\text{net}\_i}{\partial {w\_j}}.
\end{align}\]
