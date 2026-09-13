---
title: "Implementing Stochastic Gradient Descent in Machine Learning"
source: https://sebastianraschka.com/faq/docs/sgd-methods.html
crawled: 2026-09-06
---

# Implementing Stochastic Gradient Descent in Machine Learning

Often, I receive questions about how stochastic gradient descent is implemented in practice. There are many different variants, like drawing one example at a time with replacements or iterating over epochs and drawing one or more training examples without replacement. The goal of this quick write-up is to outline the different approaches briefly, and I won’t go into detail about which one is the preferred method as there is usually a trade-off.

## 1) Stochastic gradient descent v1

Let

\[\mathcal{D}=\left(\left\langle\mathbf{x}^{[1]}, y^{[1]}\right\rangle,\left\langle\mathbf{x}^{[2]}, y^{[2]}\right\rangle, \ldots,\left\langle\mathbf{x}^{[n]}, y^{[n]}\right\rangle\right) \in\left(\mathbb{R}^{m} \times\{0,1\}\right)^{n}\]

be the dataset consisting of \(n\) training examples with features \(x\_{j}^{[i]}\) and targets or class labels \(y^{[i]}\).

If we want to use “true” stochastic gradient descent, we draw random examples **with** replacement. In pseudo-code, the algorithm looks like this:

1. Initialize \(\mathbf{w} :=0^{m-1}, b :=0\)
2. for iteration \(t \in [1, ..., T]\):
   - 2.1. draw random example with replacement: \(\left\langle\mathbf{x}^{[i]}, y^{[i]}\right\rangle \in \mathcal{D}\)
   - 2.2. compute prediction \(\hat{y}^{[i]}:= h(\mathbf{x}^{[i]})\)
   - 2.3. compute loss \(\mathcal{L}^{[i]}:= L(\hat{y}^{[i]}, y^{[i]})\)
   - 2.4. compute gradients \(\Delta \mathbf{w} := - \nabla\_{\mathcal{L}^{[i]}} \mathbf{w}, \; \Delta b := - \frac{\partial \mathcal{L}^{[i]}}{\partial b?}\)
   - 2.5. update parameters \(\mathbf{w} :=\mathbf{w}+\Delta \mathbf{w}, \; b :=+\Delta b\)

Please note that while this is the “most stochastic” variant due to the independence during sampling, which is thus the most useful variant in the context of Statistics, it is usually not how it’s usually used in Computer Science and Machine Learning. (Note that this is likely due to empirical performance reasons versus statistical guarantees.)

**Opinion**

You probably want to use that one if you are proofing certain theorems in Stats.

## 2) (“On-line”) Stochastic gradient descent v2

In practice, since we usually work with a fixed-size samples and want to make best use of all training data available, we usually use the concept of “epochs.” In the context of machine learning, an *epoch* means “one pass over the training dataset.” In particular, what’s different from the previous section, *1) Stochastic gradient descent v1* is that we iterate through the training set and draw a random examples **without** replacement. The algorithm looks like this:

1. Initialize \(\mathbf{w} :=0^{m-1}, b :=0\)
2. for epoch \(e \in [1, ..., E]\):
   - 2.1. shuffle \(\mathcal{D}\) to prevent cycles
   - 2.2. for every \(\left\langle\mathbf{x}^{[i]}, y^{[i]}\right\rangle \in \mathcal{D}\):
     - 2.2.3. compute prediction \(\hat{y}^{[i]}:= h(\mathbf{x}^{[i]})\)
     - 2.2.4. compute loss \(\mathcal{L}^{[i]}:= L(\hat{y}^{[i]}, y^{[i]})\)
     - 2.2.5. compute gradients \(\Delta \mathbf{w} := - \nabla\_{\mathcal{L}^{[i]}} \mathbf{w}, \; \Delta b := - \frac{\partial \mathcal{L}^{[i]}}{\partial b?}\)
     - 2.2.6. update parameters \(\mathbf{w} :=\mathbf{w}+\Delta \mathbf{w}, \; b :=+\Delta b\)

Note that this variant is not “officially” called “on-line” stochastic gradient descent. However, based on my experience, the approach using epochs is the most common variant of stochastic gradient descent. Also, in older literature, the term “on-line” is used in the context of gradient descent if we only use one training example at a time for computing the loss and updating the parameters (likely, the term “on-line” comes from the fact that we can readily update our model one example at a time when we collect new data, for example, via an online app).

**Opinion**

I’d use this one if I had to update one example at a time. Also, empirically, it performs better than 1) in my experience. Note that using only one training example per update results in very noisy gradients since the loss is approximated from one training example only. Noisy gradients can be useful if we have non-convex loss functions and want to escape sharp local minima.

## 3) (Batch) gradient descent

Batch gradient descent or just “gradient descent” is the determinisic (not stochastic) variant. Here, we update the parameters with respect to the loss calculated on all training examples. While the updates are not noisy, we only make one update per epoch, which can be a bit slow if our dataset is large. The algorithm is as follows:

1. Initialize \(\mathbf{w} :=0^{m-1}, b :=0\)
2. for epoch \(e \in [1, ..., E]\):
   - 2.1. shuffle \(\mathcal{D}\) to prevent cycles
   - 2.2. for every \(\left\langle\mathbf{x}^{[i]}, y^{[i]}\right\rangle \in \mathcal{D}\):
     - 2.2.1. compute prediction \(\hat{y}^{[i]}:= h(\mathbf{x}^{[i]})\)
   - 2.3. compute loss \(\mathcal{L}:= \frac{1}{n} \sum\_{i=1}^{n} L(\hat{y}^{[i]}, y^{[i]})\)
   - 2.4. compute gradients \(\Delta \mathbf{w} := - \nabla\_{\mathcal{L}^{[i]}} \mathbf{w}, \; \Delta b := - \frac{\partial \mathcal{L}}{\partial b}\)
   - 2.5. update parameters \(\mathbf{w} :=\mathbf{w}+\Delta \mathbf{w}, \; b :=+\Delta b\)

**Opinion**

Unless you have a small dataset and a convex loss function that you want to optimize like in most traditional machine learning (e.g., logistic regression), you probably don’t want to use batch gradient descent. In other words, in deep learning, you don’t need to worry about it.

## 4) Minibatch (stochastic) gradient descent v1

Minibatch gradient descent is a variant of stochastic gradient descent that offers a nice trade-off (or rather “sweet spot”) between the stochastic versions that perform updates based on the 1-training example and (batch) gradient descent. Here, we are approximating the loss based on a smaller sample of the training set, which allows us to make more updates per epoch compared to batch gradient descent. On the other hand, the loss approximation is not as noisy as in 1) or 2) since we are using more training examples. Lastly, we can also make use of vectorized code (like on batch gradient descent).

1. Initialize \(\mathbf{w} :=0^{m-1}, b :=0\)
2. for iteration \(t \in [1, ..., T]\):
   - 2.1. for \(i \in [1, ... ,m]\) (where \(m\) is the minibatch size):
     - 2.1.1. draw random example with replacement: \(\langle \mathbf{x}^{[i]}, y^{[i]} \rangle \in \mathcal{D}\)
   - 2.2. compute loss \(\mathcal{L}:= \frac{1}{m} \sum\_{i=1}^{m} L(\hat{y}^{[i]}, y^{[i]})\)
   - 2.3. compute gradients \(\Delta \mathbf{w} := - \nabla\_{\mathcal{L}} \mathbf{w}, \; \Delta b := - \frac{\partial \mathcal{L}}{\partial b}\)
   - 2.4. update parameters \(\mathbf{w} :=\mathbf{w}+\Delta \mathbf{w}, \; b :=+\Delta b\)

**Opinion**

This implementation may be preferred in certain theorems since the examples are drawn with replacement. However, it is not often used in practice except in “lazy” implementations, since it is easier to write code that draws random examples from an array rather than shuffling an array before each epoch and iterating through it.

## 5) Minibatch (stochastic) gradient descent v2

Lastly, the probably most common variant of stochastic gradient descent – likely due to superior empirical performance – is a mix between the stochastic gradient descent algorithm based on epochs (section 2) and minibatch gradient descent (section 4). The algorithm is as follows:

1. Initialize \(\mathbf{w} :=0^{m-1}, b :=0\)
2. for epoch \(e \in [1, ..., E]\):
   - 2.1. shuffle \(\mathcal{D}\) to prevent cycles
   - 2.2. for \(i \in [1, ... ,m]\) (where \(m\) is the minibatch size):
     - 2.2.1. draw random example **without** replacement: \(\langle \mathbf{x}^{[i]}, y^{[i]} \rangle \in \mathcal{D}\)
   - 2.3. compute loss \(\mathcal{L}:= \frac{1}{m} \sum\_{i=1}^{m} L(\hat{y}^{[i]}, y^{[i]})\)
   - 2.4. compute gradients \(\Delta \mathbf{w} := - \nabla\_{\mathcal{L}} \mathbf{w}, \; \Delta b := - \frac{\partial \mathcal{L}}{\partial b}\)
   - 2.5. update parameters \(\mathbf{w} :=\mathbf{w}+\Delta \mathbf{w}, \; b :=+\Delta b\)

**Opinion**

This is probably the most common variant of stochastic gradient descent (at least in deep learning). Also, this is how I usually write/wrote my code and how PyTorch’s `DataLoader` class works.
