---
title: "在机器学习中实现随机梯度下降"
title_en: "Implementing Stochastic Gradient Descent in Machine Learning"
source: https://sebastianraschka.com/faq/docs/sgd-methods.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 在机器学习中实现随机梯度下降

我经常收到关于随机梯度下降（SGD）在实践中如何实现的问题。实现方式有很多变体，比如有放回地每次抽取一个样本，或者按 epoch 迭代并无放回地抽取一个或多个训练样本。这篇短文的目标是简要概述各种做法，至于哪种是首选方法我不会深入讨论，因为通常各有取舍。

## 1) 随机梯度下降 v1

令

\[\mathcal{D}=\left(\left\langle\mathbf{x}^{[1]}, y^{[1]}\right\rangle,\left\langle\mathbf{x}^{[2]}, y^{[2]}\right\rangle, \ldots,\left\langle\mathbf{x}^{[n]}, y^{[n]}\right\rangle\right) \in\left(\mathbb{R}^{m} \times\{0,1\}\right)^{n}\]

为包含 \(n\) 个训练样本的数据集，其中特征为 \(x\_{j}^{[i]}\)，目标值或类别标签为 \(y^{[i]}\)。

如果想使用「真正的」随机梯度下降，我们要**有**放回地抽取随机样本。用伪代码表示，算法如下：

1. 初始化 \(\mathbf{w} :=0^{m-1}, b :=0\)
2. 对迭代 \(t \in [1, ..., T]\)：
   - 2.1. 有放回地抽取随机样本：\(\left\langle\mathbf{x}^{[i]}, y^{[i]}\right\rangle \in \mathcal{D}\)
   - 2.2. 计算预测 \(\hat{y}^{[i]}:= h(\mathbf{x}^{[i]})\)
   - 2.3. 计算损失 \(\mathcal{L}^{[i]}:= L(\hat{y}^{[i]}, y^{[i]})\)
   - 2.4. 计算梯度 \(\Delta \mathbf{w} := - \nabla\_{\mathcal{L}^{[i]}} \mathbf{w}, \; \Delta b := - \frac{\partial \mathcal{L}^{[i]}}{\partial b?}\)
   - 2.5. 更新参数 \(\mathbf{w} :=\mathbf{w}+\Delta \mathbf{w}, \; b :=+\Delta b\)

请注意，虽然由于采样时的独立性，这是「随机性最强」的变体，因此在统计学语境中是最有用的变体，但它通常不是计算机科学和机器学习中的惯用做法。（注意，这很可能是因为实践经验上的性能考虑与统计学保证之间的取舍。）

**个人看法**

如果你要在统计学中证明某些定理，你大概会想用这种。

## 2)（「在线」）随机梯度下降 v2

在实践中，由于我们通常面对的是固定规模的样本，并且希望尽可能充分利用所有可用的训练数据，我们通常会使用「epoch」的概念。在机器学习语境中，一个 *epoch* 指「完整遍历一遍训练数据集」。与前一小节 *1) 随机梯度下降 v1* 的不同之处在于，我们遍历训练集并**无**放回地抽取随机样本。算法如下：

1. 初始化 \(\mathbf{w} :=0^{m-1}, b :=0\)
2. 对 epoch \(e \in [1, ..., E]\)：
   - 2.1. 打乱 \(\mathcal{D}\) 以防止出现循环
   - 2.2. 对每个 \(\left\langle\mathbf{x}^{[i]}, y^{[i]}\right\rangle \in \mathcal{D}\)：
     - 2.2.3. 计算预测 \(\hat{y}^{[i]}:= h(\mathbf{x}^{[i]})\)
     - 2.2.4. 计算损失 \(\mathcal{L}^{[i]}:= L(\hat{y}^{[i]}, y^{[i]})\)
     - 2.2.5. 计算梯度 \(\Delta \mathbf{w} := - \nabla\_{\mathcal{L}^{[i]}} \mathbf{w}, \; \Delta b := - \frac{\partial \mathcal{L}^{[i]}}{\partial b?}\)
     - 2.2.6. 更新参数 \(\mathbf{w} :=\mathbf{w}+\Delta \mathbf{w}, \; b :=+\Delta b\)

注意，这种变体并没有被「正式」称为「在线」随机梯度下降。不过根据我的经验，使用 epoch 的做法是随机梯度下降最常见的变体。此外，在较老的文献中，如果我们在梯度下降中每次只用一个训练样本计算损失并更新参数，就会使用「在线（on-line）」这个词（这个词可能来源于：当我们通过在线应用等方式收集到新数据时，可以一次一个样本地随时更新模型）。

**个人看法**

如果我必须一次更新一个样本，我会用这种。另外，根据我的经验，它的表现比 1) 更好。注意，每次更新只用一个训练样本会带来非常嘈杂的梯度，因为损失只由一个训练样本近似。如果损失函数非凸、我们想跳出尖锐的局部极小值，嘈杂的梯度反而可能有用。

## 3)（批量）梯度下降

批量梯度下降（batch gradient descent），或者就叫「梯度下降」，是确定性（非随机）的变体。这里，我们根据在所有训练样本上计算出的损失来更新参数。虽然更新不带噪声，但每个 epoch 只做一次更新，如果数据集很大，速度会有点慢。算法如下：

1. 初始化 \(\mathbf{w} :=0^{m-1}, b :=0\)
2. 对 epoch \(e \in [1, ..., E]\)：
   - 2.1. 打乱 \(\mathcal{D}\) 以防止出现循环
   - 2.2. 对每个 \(\left\langle\mathbf{x}^{[i]}, y^{[i]}\right\rangle \in \mathcal{D}\)：
     - 2.2.1. 计算预测 \(\hat{y}^{[i]}:= h(\mathbf{x}^{[i]})\)
   - 2.3. 计算损失 \(\mathcal{L}:= \frac{1}{n} \sum\_{i=1}^{n} L(\hat{y}^{[i]}, y^{[i]})\)
   - 2.4. 计算梯度 \(\Delta \mathbf{w} := - \nabla\_{\mathcal{L}^{[i]}} \mathbf{w}, \; \Delta b := - \frac{\partial \mathcal{L}}{\partial b}\)
   - 2.5. 更新参数 \(\mathbf{w} :=\mathbf{w}+\Delta \mathbf{w}, \; b :=+\Delta b\)

**个人看法**

除非你的数据集很小，而且要优化的是凸损失函数，就像大多数传统机器学习（例如逻辑回归）那样，否则你多半不想用批量梯度下降。换句话说，在深度学习里你不用担心它。

## 4) 小批量（随机）梯度下降 v1

小批量梯度下降（minibatch gradient descent）是随机梯度下降的一个变体，它在「基于单个训练样本做更新的随机版本」与（批量）梯度下降之间提供了一个不错的折中（或者说是「最佳平衡点」）。这里，我们基于训练集的一个较小样本近似损失，这使我们相比批量梯度下降能在每个 epoch 内做更多次更新。另一方面，由于使用了更多训练样本，损失近似不像 1) 或 2) 那样嘈杂。最后，我们还能利用向量化代码（就像批量梯度下降那样）。

1. 初始化 \(\mathbf{w} :=0^{m-1}, b :=0\)
2. 对迭代 \(t \in [1, ..., T]\)：
   - 2.1. 对 \(i \in [1, ... ,m]\)（其中 \(m\) 为小批量大小）：
     - 2.1.1. 有放回地抽取随机样本：\(\langle \mathbf{x}^{[i]}, y^{[i]} \rangle \in \mathcal{D}\)
   - 2.2. 计算损失 \(\mathcal{L}:= \frac{1}{m} \sum\_{i=1}^{m} L(\hat{y}^{[i]}, y^{[i]})\)
   - 2.3. 计算梯度 \(\Delta \mathbf{w} := - \nabla\_{\mathcal{L}} \mathbf{w}, \; \Delta b := - \frac{\partial \mathcal{L}}{\partial b}\)
   - 2.4. 更新参数 \(\mathbf{w} :=\mathbf{w}+\Delta \mathbf{w}, \; b :=+\Delta b\)

**个人看法**

由于样本是有放回抽取的，某些定理的证明可能更偏好这种实现。但实践中并不常用，只出现在一些「偷懒」的实现里，因为从数组中随机抽取样本的代码，比每个 epoch 前先打乱数组再遍历它更容易写。

## 5) 小批量（随机）梯度下降 v2

最后，很可能是最常见、也可能是经验表现最好的随机梯度下降变体，是基于 epoch 的随机梯度下降（第 2 节）与小批量梯度下降（第 4 节）的混合。算法如下：

1. 初始化 \(\mathbf{w} :=0^{m-1}, b :=0\)
2. 对 epoch \(e \in [1, ..., E]\)：
   - 2.1. 打乱 \(\mathcal{D}\) 以防止出现循环
   - 2.2. 对 \(i \in [1, ... ,m]\)（其中 \(m\) 为小批量大小）：
     - 2.2.1. **无**放回地抽取随机样本：\(\langle \mathbf{x}^{[i]}, y^{[i]} \rangle \in \mathcal{D}\)
   - 2.3. 计算损失 \(\mathcal{L}:= \frac{1}{m} \sum\_{i=1}^{m} L(\hat{y}^{[i]}, y^{[i]})\)
   - 2.4. 计算梯度 \(\Delta \mathbf{w} := - \nabla\_{\mathcal{L}} \mathbf{w}, \; \Delta b := - \frac{\partial \mathcal{L}}{\partial b}\)
   - 2.5. 更新参数 \(\mathbf{w} :=\mathbf{w}+\Delta \mathbf{w}, \; b :=+\Delta b\)

**个人看法**

这大概是随机梯度下降最常见的变体了（至少在深度学习中如此）。这也是我通常编写代码的方式，以及 PyTorch 的 `DataLoader` 类的工作方式。
