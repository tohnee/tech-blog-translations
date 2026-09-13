---
title: "损失函数学习笔记"
title_en: "Losses Learned"
source: https://sebastianraschka.com/blog/2022/losses-learned-part1.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 损失函数学习笔记

> 原文：[Losses Learned](https://sebastianraschka.com/blog/2022/losses-learned-part1.html)

交叉熵损失是我们训练基于深度学习的分类器时的首选损失函数。在本文中，我将带你快速浏览我们通常如何计算交叉熵损失，以及在 PyTorch 中如何计算它。这个主题分为两部分，这里我们先来看二分类的情境。

你可能好奇为什么要费劲写这篇文章；计算交叉熵损失应该相当简单直接吧！？可以说是，也可以说不是。我们可以用一行代码计算交叉熵损失，但由于底层的数值优化，这里有一个常见的坑。（而且是的，当我不够小心时，我自己有时也会犯这个错误。）所以，在这篇文章中，让我给你讲一点深度学习行话、如何改善数值性能，以及可能出什么岔子。

## 随堂小测

让我们以一个小测验开始本文。假设我们想用 PyTorch 实现一个深度神经网络分类器。代码如下：

![Losses learned part1 quiz1](https://sebastianraschka.com/images/blog/2022/losses-learned-part1/quiz1.webp)

![Losses learned part1 quiz2](https://sebastianraschka.com/images/blog/2022/losses-learned-part1/quiz2.webp)

哦不，两个关键部分缺失了！现在，有多种选项可以填补 (a) 和 (b) 两个框中缺失的代码，其中 *blank* 表示不需要额外的代码。

如果你处理的是二分类任务（例如，预测一封电子邮件是不是垃圾邮件），下面是一些可供选择的选项：

**二分类**

1. (a) blank & (b) `nn.BCELoss()`
2. (a) blank & (b) `nn.BCEWithLogitsLoss()`
3. (a) `nn.Sigmoid` & (b) `nn.BCELoss()`
4. (a) `nn.Sigmoid` & (b) `nn.BCEWithLogitsLoss()`
5. (a) `nn.LogSigmoid` & (b) `nn.BCELoss()`
6. (a) `nn.LogSigmoid` & (b) `nn.BCEWithLogitsLoss()`

（注意 `BCELoss` 是 *binary-cross entropy loss*（二元交叉熵损失）的缩写。）

接下来是挑战！

**问题 1：**上面六个选项中哪一个是最佳做法？

**问题 2：**这些选项中哪些可以接受但并不理想？

**问题 3：**哪些选项是错误的？

接下来，让我们在多分类设定下重复这个游戏，比如对 MNIST 中的九个不同手写数字进行分类。有如下选项：

**多分类**

1. (a) blank & (b) `nn.NLLLoss()`
2. (a) blank & (b) `nn.CrossEntropyLoss()`
3. (a) `self.layers.append(nn.Softmax())` & (b) `nn.NLLLoss()`
4. (a) `self.layers.append(nn.Softmax())` & (b) `nn.CrossEntropyLoss()`
5. (a) `self.layers.append(nn.LogSoftmax())` & (b) `nn.NLLLoss()`
6. (a) `self.layers.append(nn.LogSoftmax())` & (b) `nn.CrossEntropyLoss()`

（注意 `NLLLoss` 是 *negative log-likelihood loss*（负对数似然损失）的缩写。）

如果你对自己的答案很有信心、并且能够解释它们，那你可能不需要读这篇文章剩下的部分。不过，如果你不确定，我鼓励你继续读下去。

## 二元交叉熵损失

上一节的小测介绍了两个损失，`NLLLoss`（*negative log-likelihood loss*，负对数似然损失的缩写）和 `CrossEntropyLoss`。从概念上讲，负对数似然损失和交叉熵损失是一回事。为了理解它们之间的关系、看清这些概念如何联系起来，让我们退一步，从一个二分类问题开始。这里*二元*意味着分类问题只有两个唯一的类别标签（例如，垃圾邮件分类，两种可能的标签是 *spam* 和 *not spam*）。

### 二分类与逻辑损失函数

在统计学中，我们经常谈到最大似然估计的概念，它是一种估计概率分布或模型参数的方法。具体来说，我们给定一个数据样本，希望找到使[似然](https://sebastianraschka.com/faq/docs/probability-vs-likelihood.html)函数最大化的模型参数。由于数值上的优点，我们通常对似然函数做对数变换。（因为对数函数是单调递增函数，使似然最大化的参数同样使对数似然最大化。）此外，我们喜欢把对数似然乘以 \((-1)\)，使它变成*负*对数似然。这样就把最大化问题（最大化对数似然）变成了最小化问题（最小化[负对数似然](https://sebastianraschka.com/faq/docs/negative-log-likelihood-logistic-loss.html)）。

所以，为了找到最优参数，我们可以最大化对数似然，也可以最小化负对数似然。如果这听起来令人困惑，可以想想分类准确率和分类错误率。如果一个分类器的准确率是 \(80\%\)，那么它的分类错误率就是 \(100\% - 80\%= 20\%\)。最大化准确率与最小化错误率服务于同一个目标。

回顾一下，

- 我们有一个似然函数 \(\mathcal{L}\left(\mathbf{w} \; \vert \; x^{(1)}, ..., x^{(n)}\right)\)，其中 \(\mathbf{w}\) 是在给定一组数据点 \(x^{(1)}, ..., x^{(n)}\) 时我们试图优化的参数向量。
- 我们做对数变换并乘以 \((-1)\)，从而得到负对数似然 \(- \log \mathcal{L}\left(\mathbf{w} \; \vert \; x^{(1)}, ..., x^{(n)}\right)\)。

现在，负对数似然可以改写如下：

\[-\log \mathcal{L}\left(\mathbf{w} \; \vert \; x^{(1)}, ..., x^{(n)}\right) = - \sum\_{i=1}^{n} \log \mathcal{p}\left(x^{(i)}\vert \mathbf{w}\right),\]

其中 \(\mathcal{p}(x^{(i)}\vert \mathbf{w})\) 是来自（例如）概率密度函数的一个量。

在机器学习和分类器的语境下，我们通常还会涉及类别标签 \(y^{(1)} ... y^{(n)}\)。考虑一个逻辑回归分类器，我们要对第 *i* 个训练样本在给定模型参数 \(\mathbf{w}\) 下的类别归属概率 \(\mathcal{p}(y^{(i)} \vert \mathbf{x}^{(i)} , \mathbf{w})\) 进行建模（为了保持记号简单，请假设偏置单元包含在权重向量 \(\mathbf{w}\) 中）。

于是，负对数似然损失变为

\[- \log \mathcal{L}\left( \mathbf{w} \; \vert \; \mathbf{X}, \mathbf{y}\right) = - \sum\_{i=1}^{n} \log \mathcal{p}\left(y^{(i)} \; \vert \; \mathbf{x}^{(i)}; \mathbf{w}\right).\]

为简洁起见跳过若干步骤（更多细节见我的[书](https://www.amazon.com/Machine-Learning-PyTorch-Scikit-Learn-scikit-learn-ebook-dp-B09NW48MR1/dp/B09NW48MR1/) 😉），对于逻辑回归，它展开为如下形式：

\[- \log \mathcal{L}\left( \mathbf{w} \; \vert \; \mathbf{X}, \mathbf{y}\right) = - \sum\_{i=1}^{n}\left[y^{(i)} \log \left(\sigma\left(z^{(i)}\right)\right) + \left(1-y^{(i)}\right) \log \left(1-\sigma\left(z^{(i)}\right)\right)\right].\]

上式中的 \(z^{(i)}\) 用于简化记号，其中

- \(z^{(i)}\) 表示加权输入，\(z^{(i)}\ = \mathbf{w}^{\top} \mathbf{x}^{(i)} + b\)，它们也常被称为 *logits*。（\(b\) 是偏置单元，我们此前为了记号更简单而把它省略了。）
- \(\sigma(\cdot)\) 是[逻辑 sigmoid 函数](https://en.wikipedia.org/wiki/Sigmoid_function)，\(\sigma(z) = 1 / (1 + e^{-z}).\)

在实践中，我们也把上面这个方程称为*逻辑损失函数*（logistic loss function）或[*二元交叉熵*](https://en.wikipedia.org/wiki/Cross_entropy#Cross-entropy_loss_function_and_logistic_regression)。总结一下：所谓逻辑损失函数就是逻辑回归模型的负对数似然。而最小化负对数似然与最小化交叉熵是一回事。[交叉熵是如何推导出来的](https://en.wikipedia.org/wiki/Cross_entropy)，那是另一个故事了。

此外，我们通常还会加一个缩放因子 \(\frac{1}{n}\)，以对训练集大小或批大小取平均，并将其写成加权输入 \(\mathbf{Z}\) 和对应标签 \(\mathbf{y}\) 的函数：

\[L\_\mathbf{w}\left( \mathbf{y} , \mathbf{Z} \right) = - \frac{1}{n} \sum\_{i=1}^{n}\left[y^{(i)} \log \left(\sigma\left(z^{(i)}\right)\right) + \left(1-y^{(i)}\right) \log \left(1-\sigma\left(z^{(i)}\right)\right)\right].\]

顺便说一下，对于任何类型的用于二分类的多层神经网络，我们通常使用同一个损失函数。我们在输出层使用逻辑 sigmoid 函数 \(\sigma(\cdot)\)，而 logits $z$ 就是输出层处的加权输入，如下图所示：

![Losses learned part1 likelihood loss nn 1](https://sebastianraschka.com/images/blog/2022/losses-learned-part1/likelihood-loss-nn-1.webp)

（注意，上图中的上标索引的是层，而不是训练样本。）

### 从零实现二元交叉熵损失

（你可以在[这里](https://github.com/rasbt/machine-learning-notes/blob/main/losses/pytorch-loss-functions/binary-cross-entropy-in-pytorch.ipynb)找到包含以下代码片段的 Jupyter notebook。）

上一节展示了负对数似然损失的来龙去脉，在二分类情境下，它与逻辑损失和二元交叉熵损失是同义词。

在本节中，我们将为二分类设定实现逻辑损失函数——也就是我们有两个类别标签 0 和 1 的场景。从零实现概念是我最喜欢用来巩固理解的方式。

不过在开始之前，你有没有注意到逻辑损失

\[L\_\mathbf{w}\left( \mathbf{y} , \mathbf{Z} \right) = - \frac{1}{n} \sum\_{i=1}^{n}\left[y^{(i)} \log \left(\sigma\left(z^{(i)}\right)\right) + \left(1-y^{(i)}\right) \log \left(1-\sigma\left(z^{(i)}\right)\right)\right],\]

由两部分组成？即

**第 1 部分：** \(y^{(i)} \log \left(\sigma\left(z^{(i)}\right)\right),\) 以及  
**第 2 部分：** \(\left(1-y^{(i)}\right) \log \left(1-\sigma\left(z^{(i)}\right)\right)\)。

如果 \(y^{(i)}=0\)，那么左边的部分 \(y^{(i)} \log \left(\sigma\left(z^{(i)}\right)\right)\) 就消去了，因为 \(0\times\) *任何东西* 等于 \(0\)。反过来，如果 \(y^{(i)}=1\)，那么第二个表达式 \(\left(1-y^{(i)}\right) \log \left(1-\sigma\left(z^{(i)}\right)\right)\) 就消去了，因为 \(\left(1-y^{(i)}\right)=(1-1)=0\)。

这让我们可以用一个 Python for 循环（做求和）加上 if-else 语句，从零实现逻辑损失（从现在起我们称之为二元交叉熵）。就我个人而言，当我尝试实现一个新概念时，我常常先选择朴素的实现方式，再去优化，例如运用线性代数的概念。这通常帮助我更好地理解问题，也让代码更容易调试（至少对我来说）。

那么，为了说明上面的二元交叉熵损失概念，让我们定义一个由五个训练样本组成的小型玩具数据集。我们有一个带单个输出节点的任意神经网络分类器，如下图所示：

![Losses learned part1 sigmoid network](https://sebastianraschka.com/images/blog/2022/losses-learned-part1/sigmoid-network.webp)

或者，更具体一点，考虑一个用 PyTorch 实现的多层感知器（如上图所示）：

![Losses learned part1 sigmoid network pytorch](https://sebastianraschka.com/images/blog/2022/losses-learned-part1/sigmoid-network-pytorch.webp)

我们假设我们给这个网络喂入了一个包含五个训练样本的批次，它返回了五个输出，如上图所示。为了让代码示例更精简，我们跳过这一步，直接硬编码神经网络的输出——`logits` 和 `probas`——如下所示：

**In:**

```python
import torch

y_targets = torch.tensor([1., 1., 0., 0., 0.])

logits = torch.tensor([1.1, 2.2, 0.5, -1.1, -2.2])
probas = torch.sigmoid(logits)
print(probas)
```

**Out:**

```python
tensor([0.7503, 0.9002, 0.6225, 0.2497, 0.0998])
```

现在，铺垫工作都做完了，让我们进入从零实现——正如前面承诺的，使用 Python for 循环的朴素版本：

**In:**

```python
def binary_logistic_loss_v1(probas, y_targets):
    res = 0.
    for i in range(y_targets.shape[0]):
        if y_targets[i] == 1.:
            res += torch.log(probas[i])
        elif y_targets[i] == 0.:
            res += torch.log(1-probas[i])            
        else:
            raise ValueError(f'Value {y_targets[i]} not allowed')
    res *= -1
    res /= y_targets.shape[0]

    return res

binary_logistic_loss_v1(probas, y_targets)
```

**Out:**

```python
tensor(0.3518)
```

在上面的代码实现中，我们遍历训练样本，然后根据类别标签，用我们前面定义的两部分之一来计算损失。

**第 1 部分：**
\(y^{(i)} \log \left(\sigma\left(z^{(i)}\right)\right),\) 以及

**第 2 部分：**
\(\left(1-y^{(i)}\right) \log \left(1-\sigma\left(z^{(i)}\right)\right)\)。

我们把所有 \(n\) 个训练样本的损失项加起来（其中 \(n=\)`y_targets.shape[0]`），然后返回损失的平均值。Python 函数 `binary_logistic_loss_v1` 非常啰嗦，但同时它非常易读、易于推理。起草这样一个函数是确保它产生我们所期望结果的绝佳方式。

### 利用线性代数概念改进我们的从零实现

在上一节中，我们用 Python for 循环从零实现了二元交叉熵损失。根据我的经验，这往往是一个很好的起点。在本节中，我们现在来看看如何让这个实现更高效。

在实践中，我们常常可以用线性代数的概念替代昂贵的 for 循环。例如，我们可以使用向量点积（通过 PyTorch 的 `matmul`，即矩阵乘法 matrix-multiplication 的缩写）来实现前一个函数：

我们假设我们给这个网络喂入了一个包含五个训练样本的批次，它返回了五个输出，如上图所示。为了让代码示例更精简，我们跳过这一步，直接硬编码神经网络的输出——`logits` 和 `probas`——如下所示：

**In:**

```python
def binary_logistic_loss_v2(probas, y_targets):
    first = -y_targets.matmul(torch.log(probas))
    second = -(1 - y_targets).matmul(torch.log(1 - probas))
    return (first + second) / y_targets.shape[0]

binary_logistic_loss_v2(probas, y_targets)
```

**Out:**

```python
tensor(0.3518)
```

在上面，我们用点积替代了 for 循环。例如，

```python
res = 0.
for i in range(y_targets.shape[0]):    
    if y_targets[i] == 1.:
        res += torch.log(probas[i])
```

变成了

```python
first = -y_targets.matmul(torch.log(probas))
```

这是因为点积等价于一个加权和：

\[\mathbf{a}^{\top} \mathbf{b} = \sum\_i a\_i b\_i.\]

而且正如我们前面讨论的，对于第一项，\(y=0\) 的情形由于乘以 \(0\) 得到的乘积为 \(0\)，不会影响求和。（等价地，第二项通过 \(1 - y\) 这一项跳过了 \(y=1\) 的情形。）

`binary_logistic_loss_v2` 函数不仅比 `_v1` 更紧凑，而且更快。你可以在 Jupyter notebook 中运行下面这些 `%timeit` 代码行，亲自验证：

**In:**

```python
%timeit binary_logistic_loss_v1(probas, y_targets)
```

**Out:**

```python
38 µs ± 286 ns per loop (mean ± std. dev. of 7 runs, 10,000 loops each)
```

就我而言，即使输入向量只有 5 个元素这么小，`_v2` 在我的笔记本上也比 `_v1` 快约 \(5\times\)（10.6 µs 对 38 µs）：

**In:**

```python
%timeit binary_logistic_loss_v2(probas, y_targets)
```

**Out:**

```python
10.6 µs ± 81.9 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)
```

虽然从零实现损失函数是很好的学习练习，但在真实世界的应用中，我们通常希望使用成熟深度学习库中的高效实现。从零实现的目的在于：我们可以证明逻辑损失（我们实现为 `binary_logistic_loss_v`）与 PyTorch 中的二元交叉熵实现产生相同的结果，后者我们稍后就会在本节中介绍。这让我们确信自己理解了二元交叉熵公式，而且它确实与逻辑损失或负对数似然是同一个概念。

### 在 PyTorch 中使用二元交叉熵损失

现在，让我们看看如何在 PyTorch 中实现二元交叉熵损失。常见的方式是使用 `torch.nn` 中的损失类：

**In:**

```python
bce = torch.nn.BCELoss()
bce(probas, y_targets)
```

**Out:**

```python
tensor(0.3518)
```

（在稍后的一节中，我们将看到 `torch.nn.functional` 中还有"函数式"版本。）

从上面的代码输出可以看到，PyTorch 的 `BCELoss` 产生的结果与我们自己的 `binary_logistic_loss_v` 函数完全相同。太好了！

使用面向对象的 API，我们首先通过 `BCELoss` 实例化损失，然后像使用函数一样使用它。这之所以可行，是因为 `BCELoss` 以及 PyTorch 中的其他损失都有一个底层的 `forward()` 方法，它在调用 `bce(...)` 时被执行。

在底层，我们可以把它想象成这样：

**In:**

```python
class MyBCELoss(torch.nn.Module):
    def __init__(self):
        super().__init__()
 
    def forward(self, inputs, targets):        
        return binary_logistic_loss_v2(inputs, targets)
    
    
my_bce = MyBCELoss()
my_bce(probas, y_targets)
```

**Out:**

```python
tensor(0.3518)
```

### 为什么 PyTorch 中有两个二元交叉熵损失？

在继续把二元交叉熵损失扩展到多分类设定之前，还有一件事值得一提。当我们使用 `BCELoss` 时，输入是类别归属概率（`probas`），与我们自己的 `binary_cross_entropy_v` 函数类似。有趣的是，还存在第二个二元交叉熵损失实现，即 `BCELossWithLogits`：

**In:**

```python
bce_logits = torch.nn.BCEWithLogitsLoss()
bce_logits(logits, y_targets)
```

**Out:**

```python
tensor(0.3518)
```

如我们所见，结果仍然相同。区别在于 `BCELossWithLogits` 接受的是 logits（输出层的加权输入）而不是类别归属概率。与其让我们把 logits 通过逻辑 sigmoid 函数，

**In:**

```python
bce = torch.nn.BCELoss()
bce(torch.sigmoid(logits), y_targets)
```

**Out:**

```python
tensor(0.3518)
```

`BCEWithLogitsLoss` 会在内部应用 sigmoid 函数。

那么，为什么 PyTorch 要实现两个版本的二元交叉熵损失，我们又应该使用哪一个？我猜它实现 `BCELoss` 是因为这是规范形式，是大多数人熟悉的形式。然而在实践中，如果你在使用二元交叉熵（在下一部分中，我们还将看到如何使用常规的 `CrossEntropyLoss`）做二分类，我强烈建议你考虑使用 `BCEWithLogitsLoss`。

我们想使用 `BCEWithLogitsLoss` 的原因是，借助 [log-sum-exp 技巧](https://gregorygundersen.com/blog/2020/02/09/log-sum-exp/)可以改善数值稳定性。（你可以在[这里](https://github.com/pytorch/pytorch/blob/35fed93b1ef05175143f883c6f89f06c6dd9429b/aten/src/ATen/native/Loss.cpp#L96-L112)找到源码实现。）总的来说，使用 PyTorch（或任何深度学习库，真的）时的另一个重要概念是利用融合算子（fused operators）。一个例子是 `logsigmoid(z)` 函数，我们可以用它替代 `log(sigmoid(z))`——[算子融合能让代码运行快得多，尤其是在 GPU 上](https://horace.io/brrr_intro.html)。

回顾一下我们自己的二元交叉熵损失实现，再次展示如下：

**In:**

```python
def binary_logistic_loss_v2(probas, y_targets):
    first = -y_targets.matmul(torch.log(probas))
    second = -(1 - y_targets).matmul(torch.log(1 - probas))
    return (first + second) / y_targets.shape[0]

binary_logistic_loss_v2(probas, y_targets)
```

**Out:**

```python
tensor(0.3518)
```

我们可以把 `torch.log(probas)` 替换为 `torch.nn.functional.logsigmoid(logits)`，如下所示：

**In:**

```python
import torch.nn.functional as F

def binary_logistic_loss_v3(logits, y_targets):
    first = -y_targets.matmul(F.logsigmoid(logits))
    second = -(1 - y_targets).matmul(F.logsigmoid(logits) - logits)
    return (first + second) / y_targets.shape[0]

binary_logistic_loss_v3(logits, y_targets)
```

**Out:**

```python
tensor(0.3518)
```

（顺便说一下，我不知道为什么 `torch.sigmoid` 不像 `logsigmoid` 那样放在 `torch.nn.functional` 下面。）

为什么 `first = ...` 中的替换相当直白，你可能想知道 `second = ...` 中发生了什么，也就是为什么 `torch.log(1 - probas)` 变成了 `F.logsigmoid(logits) - logits)`。这样做是允许的，因为

\[\begin{aligned}
&\log \left(1-\frac{1}{1+e^{-z}}\right) \\
&=\log \left(1-\frac{e^{z}}{1+e^{z}}\right) \\
&=\log \left(\frac{1}{1+e^{z}}\right) \\
&=\log \left(\frac{e^{z}}{1+e^{z}}\right)-\log \left(e^{z}\right) \\
&=\log \left(\frac{1}{1+e^{-z}}\right)-z \\
&=\log (\sigma(z))-z.
\end{aligned}\]

（顺便说一下，我们在 [Deep Neural Networks for Rank-Consistent Ordinal Regression Based On Conditional Probabilities](https://arxiv.org/abs/2111.08851) 一文的 CORN 损失中也使用了这个技巧。）

顺带一提，从技术上讲，反向传播过程也可以加以简化。不过这应该是两个版本的损失内部都已经在做的事情。

例如，与其让自动微分引擎为三个项分别计算数值梯度，再把它们按如下方式组合起来，
\(\frac{\partial L}{\partial w\_{j}}= \frac{\partial L}{\partial a} \frac{d a}{d z} \frac{\partial z}{\partial w\_{j}} = \frac{a-y}{a-a^{2}} a \cdot (1-a) x\_j,\)
我们可以计算简化后的形式
\(\frac{\partial L}{\partial w\_j} = (a-y) x\_j.\)
简化形式的计算应该更快，数值上也更稳定。我们可以如下图所示推导出它：

![Losses learned part1 simplify backward](https://sebastianraschka.com/images/blog/2022/losses-learned-part1/simplify-backward.webp)

### PyTorch 的两个二元交叉熵实现在实践中的表现

上一节解释了 PyTorch 中存在两个二元交叉熵实现：`BCELoss` 和 `BCEWithLogitsLoss`。我们讨论过，由于 log-sum 技巧带来的数值稳定性改善，推荐使用 `BCEWithLogitsLoss` 而非 `BCELoss`。为了看看这在实践中是否真的有区别，我实现了一个 [VGG-16 卷积神经网络](https://arxiv.org/abs/1409.1556)，并在 [CelebA 人脸图像](https://mmlab.ie.cuhk.edu.hk/projects/CelebA.html)上训练它来预测一个人是否在微笑。

值得再次强调的是，区别不在于计算速度，而在于数值稳定性。例如，用 `Logits`+`BCEWithLogitsLoss` 训练的分类器（[vgg16-bcewithlogitsloss.ipynb](https://github.com/rasbt/machine-learning-notes/blob/main/losses/pytorch-loss-functions/vgg16-smile-classifier/vgg16-bcewithlogitsloss.ipynb)）在 4 个 epoch 后达到约 92% 的准确率，而 `Sigmoid`+`BCELoss` 版本（[vgg16-bceloss.ipynb](https://github.com/rasbt/machine-learning-notes/blob/main/losses/pytorch-loss-functions/vgg16-smile-classifier/vgg16-bceloss.ipynb)）在相同的超参数设置下甚至无法收敛。

## PyTorch 的函数式 API 与面向对象 API

在上一节中，我们使用了 PyTorch 面向对象的二元交叉熵损失实现。这里的面向对象是指它们被实现为 Python 类，我们必须实例化对象才能使用它们。如果我们需要跟踪内部状态（比如模型权重和梯度），面向对象范式非常合适。

然而，对于不需要内部状态的东西，比如损失函数，我们也可以使用函数式 API，省去实例化损失的额外步骤。换句话说，PyTorch 的函数式 API 通过 `torch.nn.functional` 子模块提供没有内部状态的实现。

我们前面使用的损失函数的"函数式"等价形式如下：

**二元交叉熵**

```python
import torch.nn.functional as F

F.binary_cross_entropy(probas, y_targets)
```

**Out:**

```python
tensor(0.3518)
```

**带 logits 的二元交叉熵**

**In:**

```python
import torch.nn.functional as F

F.binary_cross_entropy_with_logits(logits, y_targets)
```

**Out:**

```python
tensor(0.3518)
```

## PyTorch 损失函数速查表（截至目前）

让我们总结一下到目前为止的内容。Python 中有两个二元交叉熵损失函数——实际上有四个，如果我们区分面向对象版本和函数式版本的话。下表总结了本文第一部分中到目前为止介绍的损失函数：

![Losses learned part1 loss cheatsheet binary](https://sebastianraschka.com/images/blog/2022/losses-learned-part1/loss-cheatsheet-binary.webp)

我希望你现在能自信地回答 **Binary classification（二分类）** 部分的测验了。

## 接下来

在下一部分中，我们将扩展本文的概念，研究面向多个类别的交叉熵损失。最后，我们还会了解 PyTorch API 中一些声名狼藉的不一致之处，并补齐解决随堂小测所需的全部剩余细节 😉。

![Losses learned part1 loss cheatsheet multi](https://sebastianraschka.com/images/blog/2022/losses-learned-part1/loss-cheatsheet-multi.webp)

感谢阅读。如果你喜欢这篇文章，也可以[在 Twitter 上找到我](https://twitter.com/rasbt)，我在那里分享更多有用的内容。

## 花絮：被删掉的章节

在第一稿中，我还没写到原本打算写的正文部分，就已经写了 3600 个词。

![Losses learned part1 old draft](https://sebastianraschka.com/images/blog/2022/losses-learned-part1/old-draft.webp)

我不确定各位之中是否有人有耐力把那些全部读完。而且，数学太多，代码太少。博客文章应该有趣！

所以，为了让内容更精炼，我把那些全部删掉，从头再来。第二次动笔时，我做了几个假设：

1. 我假设你已经知道[似然](https://sebastianraschka.com/faq/docs/probability-vs-likelihood.html)是什么。
2. 另外，你已经熟悉我们训练深度神经网络时最小化的[负对数似然损失](https://sebastianraschka.com/faq/docs/negative-log-likelihood-logistic-loss.html)。
3. 而且你可能听说过，*负对数似然损失*和[*交叉熵损失*](https://www.youtube.com/watch?v=icQaFxKa_J0)是同一回事。
4. 你也知道[典型的 PyTorch 训练循环](https://sebastianraschka.com/faq/docs/training-loop-in-pytorch.html)长什么样。
5. 顺便说一下，我还假设你熟悉 logits 的概念以及 [softmax 激活](https://sebastianraschka.com/faq/docs/softmax_regression.html)函数。

我很高兴我们都在同一页上 😊。
