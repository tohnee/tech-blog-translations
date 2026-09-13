---
title: "Cross-Entropy Loss in PyTorch and Its Alternatives"
source: https://sebastianraschka.com/faq/docs/pytorch-crossentropy.html
crawled: 2026-09-06
---

# Cross-Entropy Loss in PyTorch and Its Alternatives

The reasons why PyTorch implements different variants of the cross entropy loss are convenience and computational efficiency.

Remember that we are usually interested in maximizing the likelihood of the correct class. Maximizing likelihood is often reformulated as maximizing the log-likelihood, because taking the log allows us to replace the product over the features into a sum, which is numerically more stable/easier to optimize. For related reasons, we minimize the *negative* log likelihood instead of maximizing the log likelihood. (You can find more details in my [lecture slides](https://github.com/rasbt/stat479-deep-learning-ss19/blob/master/L08_logistic/L08_logistic_slides.pdf).)

Let’s summarize this briefly.

- Let $a$ be a placeholder variable for the logistic sigmoid function output:

\[a := h(\mathbf{x})=\frac{1}{1+e^{- \mathbf{w}^\top \mathbf{x}}}.\]

- We want

\[\begin{array}{ll}{P(y=0 | \mathbf{x}) \approx 1} & {\text { if } y=0} \\ {P(y=1 | \mathbf{x}) \approx 1} & {\text { if } y=1}\end{array},\]

which can be written more compactly as
\(P(y | \mathbf{x})=a^{y}(1-a)^{(1-y)}.\)

- To achieve this, we maximize the likelihood over all training examples $1, …, n$:

\[P\left(y^{[i]}, \ldots, y^{[n]} | \mathbf{x}^{[1]}, \ldots, \mathbf{x}^{[n]}\right)=\prod\_{i=1}^{n} P\left(y^{[i]} | \mathbf{x}^{[i]}\right).\]

for which we can define the Likelihood function $L$:

\[\begin{aligned} L(\mathbf{w}) &=P(\mathbf{y} | \mathbf{x} ; \mathbf{w}) \\ &=\prod\_{i=1}^{n} P\left(y^{(i)} | x^{(i)} ; \mathbf{w}\right) \\ &=\prod\_{i=1}^{n}\left(\sigma\left(z^{(i)}\right)\right)^{y^{(i)}}\left(1-\sigma\left(z^{(i)}\right)\right)^{1-y^{(i)}} \end{aligned}\]

- By taking the log, we arive at an objective that is easier to optmize:

\[\begin{aligned} l(\mathbf{w}) &=\log L(\mathbf{w}) \\ &=\sum\_{i=1}^{n}\left[y^{(i)} \log \left(\sigma\left(z^{(i)}\right)\right)+\left(1-y^{(i)}\right) \log \left(1-\sigma\left(z^{(i)}\right)\right)\right] \end{aligned}.\]

- Finally, to turn this maximization problem into a minimization problem that lets us use stochastic gradient descent optimizers in PyTorch, we are interested in the *negative* log likelihood:

\[\begin{aligned} \mathcal{L}(\mathbf{w}) &=-l(\mathbf{w}) \\ &=-\sum\_{i=1}^{n}\left[y^{(i)} \log \left(\sigma\left(z^{(i)}\right)\right)+\left(1-y^{(i)}\right) \log \left(1-\sigma\left(z^{(i)}\right)\right)\right] \end{aligned}.\]

This is equivalent to the the binary cross entropy:

\[H\_{\mathbf{a}}(\mathbf{y})=-\sum\_{i}\left(y^{[i]} \log \left(a^{[i]}\right)+\left(1-y^{[i]}\right) \log \left(1-a^{[i]}\right)\right)\]

And the generalized form of the cross entropy is extending this concept to $K$ classes (which are assumed to have a one-hot encoded form):

\[H\_{\mathbf{a}}(\mathbf{y})=\sum\_{i=1}^{n} \sum\_{k=1}^{K}-y\_{k}^{[i]} \log \left(a\_{k}^{[i]}\right).\]

(This is similar to the multinomial logistic loss, also known as softmax regression.)

In short, cross-entropy is exactly the same as the negative log likelihood (these were two concepts that were originally developed independently in the field of computer science and statistics, and they are motivated differently, but it turns out that they compute excactly the same in our classification context.)

PyTorch mixes and matches these terms, which in theory are interchangeable. In PyTorch, these refer to implementations that accept different input arguments (but compute the same thing). This is summarized below.

## PyTorch Loss-Input Confusion (Cheatsheet)

- `torch.nn.functional.binary_cross_entropy` takes logistic sigmoid values as inputs
- `torch.nn.functional.binary_cross_entropy_with_logits` takes logits as inputs
- `torch.nn.functional.cross_entropy` takes logits as inputs (performs log\_softmax internally)
- `torch.nn.functional.nll_loss` is like cross\_entropy but takes log-probabilities (log-softmax) values as inputs

And here a quick demonstration:

Note the main reason why PyTorch merges the `log_softmax` with the cross-entropy loss calculation in `torch.nn.functional.cross_entropy` is numerical stability. It just so happens that the derivative of the loss with respect to its input and the derivative of the log-softmax with respect to its input simplifies nicely (this is outlined in more detail in my lecture notes.)

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
