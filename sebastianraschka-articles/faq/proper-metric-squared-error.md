---
title: "Is the squared error loss a proper metric?"
source: https://sebastianraschka.com/faq/docs/proper-metric-squared-error.html
crawled: 2026-09-06
---

# Is the squared error loss a proper metric?

Consider two vectors or points \(\mathbf{v}\) and \(\mathbf{w}\) and their distance \(d(\mathbf{v}, \mathbf{w}).\)

The following criteria are required for a proper metric:

1. The distance between two points is always non-negative \(d(\mathbf{v}, \mathbf{w}) \geq 0.\) Also, the distance can only be zero if the two points are identical, that is, $\mathbf{v} = \mathbf{w}.$$
2. The distance is symmetric, i.e., \(d(\mathbf{v}, \mathbf{w}) = d(\mathbf{w}, \mathbf{v}).\)
3. The distance function satisifies the *triangle inequality* for any three points: \(\mathbf{v}, \mathbf{w}, \mathbf{x},\) which means that
   \(d(\mathbf{v}, \mathbf{w}) \leq d(\mathbf{v}, \mathbf{x}) + d(\mathbf{x}, \mathbf{w}).\)

The mean squared error loss (MSE) computes the squared Euclidean distance between a target variable \(y\) and a predicted target value \(\hat{y}:\)

\[\mathrm{MSE}=\frac{1}{n} \sum\_{i=1}^n\left(y^{(i)} - \hat{y}^{(i)}\right)^2.\]

The index \(i\) denotes the \(i\text{-th}\) datapoint in the dataset or sample. For simplicity, we will consider the squared error (SE) loss between two data points (however, the insights below also hold for the MSE):

\[\mathrm{SE}(y, \hat{y})=\left(y - \hat{y}\right)^2.\]

**Criterion 1.** The SE satisfies the first part of the first criterion: *The distance between two points is always non-negative.* Since we are raising the difference to the power of 2, it cannot be negative.

**Criterion 2.** How about the second criterion, *the distance can only be zero if the two points are identical*? Due to the subtraction in the SE, it is intuitive to see that it can only be 0 if the prediction matches the target variable, \(y = \hat{y}.\)

We saw tha the SE satisfies the first criterion of a proper metric, and we can again use the *square* to confirm that it also satisfies the second criterion, *the distance is symmetric*. Due to the square, we have \(\left(y - \hat{y}\right)^2 = \left(\hat{y} - y\right)^2.\)

**Criterion 3.** At first glance, it seems that the squared error loss also satisfies the triangle inequality. Intuitively, you can check this by choosing three arbitrary numbers (here: 1, 2, 3):

1. \[(1-2)^{2} \leq (1-3)^{2} + (2-3)^{2}\]
2. \[(1-3)^{2} \leq (1-2)^{2} + (2-3)^{2},\]
3. \[(2-3)^{2} \leq (1-2)^{2} + (1-3)^{2}.\]

However, there are values where this is not true, [for example \(d(a,c) = 4\), \(d(a,b) = 2\), and \(d(b,c) = 3\)](https://gmd.copernicus.org/articles/7/1247/2014/), where \(4^2 \lneq 2^2 + 3^2.\) the triangle inequality does not hold.

In contrast, the root-mean squared error does satisfy the triangle inequality, and the example above works out: \(4 \lneq 2 + 3.\)

The root-squared error \(\sqrt{\left(y - \hat{y}\right)^2}\) is essentially the same as the \(L\_2\) or Euclidean distance between two points, [which is known to satisfy the triangle inequality](https://en.wikipedia.org/wiki/Euclidean_distance).

Since it does not satisfy the triangle inequality via the example above, we conclude that the (mean) squared error loss is not a proper metric.
