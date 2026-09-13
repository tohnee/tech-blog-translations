---
title: "What is the difference between covariance and correlation?"
source: https://sebastianraschka.com/faq/docs/covariance-vs-correlation.html
crawled: 2026-09-06
---

# What is the difference between covariance and correlation?

The covariance is a measure for how two variables are related to each other, i.e., how two variables vary with each other.

Let \(n\) be the population size, \(x\) and \(y\) two different features (variables), and \(\mu\) the population mean; the covariance can then be formally defined as:

\[\sigma\_{x y}=\frac{1}{n} \sum\_{i}^{n}\left(x^{(i)}-\mu\_{x}\right)\left(y^{(i)}-\mu\_{y}\right).\]

A covariance of 0 indicates that two variables are totally unrelated. If the covariance is positive, the variables increase in the same direction, and if the covariance is negative, the variables change in opposite directions. As it can be seen in the equation above, the magnitude of the covariance depends on the scale of each variable (the size of the population or sample mean).

Pearson’s \(\rho\) or “r” (or typically just called “correlation coefficient”) is measures the linear correlation between two features and is closely related to the covariance. In fact, it’s a normalized version of the covariance as shown below:

\[\rho=\frac{\sum\_{i=1}^{n}\left[\left(x^{(i)}-\mu\_{x}\right)\left(y^{(i)}-\mu\_{y}\right)\right]}{\sqrt{\sum\_{i=1}^{n}\left(x^{(i)}-\mu\_{x}\right)^{2}} \sqrt{\sum\_{i=1}^{n}\left(y^{(i)}-\mu\_{y}\right)^{2}}}=\frac{\sigma\_{x y}}{\sigma\_{x} \sigma\_{y}}\]

(Note that we dropped the \(1/n\) term as it cancels.)

By dividing the covariance by the features’ standard deviations, we ensure that the correlation between two features is in the range [-1, 1], which makes it more interpretable than the unbounded covariance. However, note that the covariance and correlation are exactly the same if the features are normalized to unit variance (e.g., via standardization or z-score normalization).
Two features are perfectly positively correlated if \(\rho=1\) and pefectly negatively correlated if \(\rho=-1\). No correlation is observed if \(\rho=0\).

## Covariance and correlation for standardized features

We can show that the correlation between two features is in fact equal to the covariance of two standardized features. To show this, let us first standardize the two features, \(x\) and \(y\), to obtain their z-scores, which we will denote as \(x'\) and \(y'\) , respectively:

\[x^{\prime}=\frac{x-\mu\_{x}}{\sigma\_{x}}, \quad y^{\prime}=\frac{y-\mu\_{y}}{\sigma\_{y}}.\]

As you recall, the (population) covariance between two features is computed as follows:

\[\sigma\_{x y}=\frac{1}{n} \sum\_{i}^{n}\left(x^{(i)}-\mu\_{x}\right)\left(y^{(i)}-\mu\_{y}\right).\]

Since standardization performs mean-centering, we can rewrite the previous equation as

\[\sigma\_{x y}^{\prime}=\frac{1}{n} \sum\_{i}^{n}\left(x^{\prime (i)}-0\right)\left(y^{\prime (i)}-0\right).\]

Now, if we resubstitute those terms using the defnitions of the standardized features, we get:

\[\begin{equation}
\begin{aligned} & \frac{1}{n} \sum\_{i}^{n}\left(\frac{x-\mu\_{x}}{\sigma\_{x}}\right)\left(\frac{y-\mu\_{y}}{\sigma\_{y}}\right) \\ &= \frac{1}{n \cdot \sigma\_{x} \sigma\_{y}} \sum\_{i}^{n}\left(x^{(i)}-\mu\_{x}\right)\left(y^{(i)}-\mu\_{y}\right), \end{aligned}
\end{equation}\]

which simplifies to

\[\sigma\_{x y}^{\prime}=\frac{\sigma\_{x y}}{\sigma\_{x} \sigma\_{v}}\]

and concludes the proof that covariance and correlation are the same if the features are standardized.
