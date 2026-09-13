---
title: "Is the cross-entropy loss a proper metric?"
source: https://sebastianraschka.com/faq/docs/proper-metric-cross-entropy.html
crawled: 2026-09-06
---

# Is the cross-entropy loss a proper metric?

Consider two vectors or points \(\mathbf{v}\) and \(\mathbf{w}\) and their distance \(d(\mathbf{v}, \mathbf{w}).\)

The following criteria are required for a proper metric:

1. The distance between two points is always non-negative \(d(\mathbf{v}, \mathbf{w}) \geq 0.\) Also, the distance can only be zero if the two points are identical, that is, $\mathbf{v} = \mathbf{w}.$$
2. The distance is symmetric, i.e., \(d(\mathbf{v}, \mathbf{w}) = d(\mathbf{w}, \mathbf{v}).\)
3. The distance function satisifies the *triangle inequality* for any three points: \(\mathbf{v}, \mathbf{w}, \mathbf{x},\) which means that
   \(d(\mathbf{v}, \mathbf{w}) \leq d(\mathbf{v}, \mathbf{x}) + d(\mathbf{x}, \mathbf{w}).\)

Cross-entropy is used to measure the distance between two probability distributions. In machine learning contexts, we use the discrete cross-entropy loss (CE) between class label *y* and the predicted probability *p* when we train logistic regression or neural network classifiers on a dataset consisting of *n* training examples:

\[\mathrm{CE}(\mathbf{y}, \mathbf{p}) = -\frac{1}{n} \sum\_{i=1}^n y^{(i)} \cdot \log \left(p^{(i)}\right).\]

Again, for simplicity, we will look at the cross-entropy function (*H*) between only two data points:

\[H(y, p) = - y \cdot \log(p).\]

**Criterion 1.** The cross-entropy loss satisfies one part of the first criterion. The distance is always non-negative because the probability score is a number in the range [0, 1]. Hence, \(\log(p)\) ranges between 44-\infty\(and 0. The important part is that the \*H\* function (see above) includes a negative sign. Hence, the cross-entropy ranges between\)\infty$$ and 0 and thus satisfies one aspect of criterion 1.

However, the cross entropy loss is not zero for two identical points. For example \(H(0.9, 0.9) = - 0.9 \log(0.9) = 0.095.\)

**Criterion 2.** The second criterion is violated by the cross-entropy loss because it’s not symmetric: \(- y \cdot \log(p) \neq - p \cdot \log(y).\)

Let’s illustrate this with a concrete, numeric example:

\[-1 \cdot \log(0.5) = 0.693\]
\[-0.5 \cdot \log(1) = 0.\]

**Criterion 3.** Does the cross-entropy loss satisfy the triangle inequality,
\(H(r, p) \geq H(r, q) + H(q, p)?\)

It does not. We can illustrate this with an example. Suppose we choose \(r=0.9, p=0.5, q=0.4.\) We have

\[H(0.9, 0.5) = 0.624\]
\[H(0.9, 0.4) = 0.825\]
\[H(0.4, 0.5) = 0.277.\]

We can see that \(0.624 \geq 0.825 + 0.277\) does not hold.

We can conclude that while the cross-entropy loss is a useful loss function for training neural networks via (stochastic) gradient decent, it is not a proper distance metric as it does not satisfy any of the three criteria above.
