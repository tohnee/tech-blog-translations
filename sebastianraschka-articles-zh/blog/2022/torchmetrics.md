---
title: "TorchMetrics"
title_en: "TorchMetrics"
source: https://sebastianraschka.com/blog/2022/torchmetrics.html
crawled: 2026-09-06
translated: 2026-09-06
---

# TorchMetrics

> 原文：[TorchMetrics](https://sebastianraschka.com/blog/2022/torchmetrics.html)

[TorchMetrics](https://torchmetrics.readthedocs.io/en/latest/) 是一个非常优秀且便利的库，让我们能够以迭代的方式计算模型性能。它是为 [PyTorch](http://pytorch.org)（和 [PyTorch Lightning](https://www.pytorchlightning.ai)）设计的，但它是一个通用库，也兼容其他库和工作流。

如果我们想在迭代式训练或基于小批量（minibatch）的评估过程中跟踪模型（并可选地跨多个 GPU），这种迭代计算就非常有用。在深度学习中，这基本上是*时时刻刻都在发生*的事。就我个人而言，它帮我大幅减少了[我的样板代码](https://github.com/Raschka-research-group/corn-ordinal-neuralnet/blob/main/model-code/refactored-version/cnn-image/helper_files/trainingeval.py)。

**不过，使用 TorchMetrics 时一个常见的问题是：我们应该用 `.update()` 还是 `.forward()`？（这也是我刚开始使用时确实遇到过的疑问。）**

虽然[文档解释了](https://torchmetrics.readthedocs.io/en/latest/pages/implement.html#internal-implementation-details)调用 `.forward()` 时内部发生了什么，但在这篇博文中，用一个动手示例来补充说明可能更有帮助。

（PS：本篇博文的 Jupyter Notebook 版本可以在[这里](https://github.com/rasbt/torchmetrics-blog/blob/main/torchmetrics-update-forward.ipynb)找到。）

## 手动计算准确率作为对照

虽然 TorchMetrics 能计算更花哨的东西（例如，在我另一个 notebook 里可以查看混淆矩阵，见[这里](https://github.com/rasbt/deeplearning-models/blob/master/pytorch-lightning_ipynb/mlp/mlp-basichttps://github.com/rasbt/torchmetrics-blog/blob/main/mlp-basic.ipynb)），但这里我们还是用常规的分类准确率，因为它更简单、计算起来更直观。

另外，在深入 TorchMetrics 之前，让我们先***手动***计算准确率，确保理解 TorchMetrics 的工作方式时有个基准。

假设我们正在训练一个模型，一个 epoch 由 10 个小批量（minibatch，简称 *batch*）组成。在下面的代码中，我们用外层 for 循环（`for i in range(10):`）来模拟这一过程。

此外，我们不使用真实的数据集和模型，而是假设：

- `y_true = torch.randint(low=0, high=2, size=(10,))` 是一个包含当前小批量真实标签的张量，由十个 0 和 1 组成。
  （例如，它类似于
  `torch.tensor([0, 1, 1, 0, 1, 0, 1, 1, 0, 1])` 这样的东西。）
- `y_pred = torch.randint(low=0, high=2, size=(10,))` 是当前小批量的预测类别标签，它也是由十个 0 和 1 组成的张量，与 `y_true` 类似。

通过 `torch.manual_seed(123)`，我们保证代码可复现，每次执行下面的代码单元格都得到完全相同的结果：

**输入：**

```python
import torch

torch.manual_seed(123)

all_true, all_pred = [], []

for i in range(10):
    y_true = torch.randint(low=0, high=2, size=(10,))
    y_pred = torch.randint(low=0, high=2, size=(10,))
    all_true.append(y_true)
    all_pred.append(y_pred)

correct_pred = (torch.cat(all_true) == torch.cat(all_pred)).float()
    
acc = torch.mean(correct_pred)
print('Overall accuracy:', acc)
```

**输出：**

```python
Overall accuracy: tensor(0.5600)
```

所以，我们在上面做的是：收集所有真实类别标签 `all_true` 和 `all_pred`，然后计算预测正确的数量（真实标签与预测标签匹配的次数），并把这个数赋给 `correct_pred`。最后，我们计算正确预测的平均值，这就是准确率。

如果处理的是大型数据集，用 `all_true` 和 `all_pred` 累积所有标签会很浪费（最坏情况下可能超出 GPU 内存）。更聪明的做法是统计正确预测的数量，再除以训练样本总数，如下所示：

**输入：**

```python
torch.manual_seed(123)

num = 0
correct = 0.

for i in range(10):
    y_true = torch.randint(low=0, high=2, size=(10,))
    y_pred = torch.randint(low=0, high=2, size=(10,))
    correct += (y_true == y_pred).float().sum()
    num += y_true.numel()
    
acc = correct / num
print('Overall accuracy:', acc)
```

**输出：**

```python
Overall accuracy: tensor(0.5600)
```

## 使用 TorchMetrics

好，TorchMetrics 让我们能做到上一节做的事，也就是以迭代方式计算一个指标。

一般步骤如下：

1. 初始化想要计算的指标（这里是准确率）。
2. 在训练循环中调用 `.update()`。
3. 最后，在结束时调用 `.compute()` 得到最终的准确率值。

让我们看看这在代码里是什么样子：

**输入：**

```python
from torchmetrics.classification import Accuracy

train_acc = Accuracy()
torch.manual_seed(123)

for i in range(10):
    
    y_true = torch.randint(low=0, high=2, size=(10,))
    y_pred = torch.randint(low=0, high=2, size=(10,))
    
    abc = train_acc.update(y_true, y_pred)
    print('Batch accuracy:', abc)
    
print('Overall accuracy:', train_acc.compute())
```

**输出：**

```python
Batch accuracy: None
Batch accuracy: None
Batch accuracy: None
Batch accuracy: None
Batch accuracy: None
Batch accuracy: None
Batch accuracy: None
Batch accuracy: None
Batch accuracy: None
Batch accuracy: None
Overall accuracy: tensor(0.5600)
```

注意，总体准确率与上一节手动计算的结果相同。作为参考，我们还打印了每个小批量的准确率；不过这里没什么可看的，因为它总是 `None`。下面的代码示例会解释我们为什么要这么做。

于是在接下来的代码示例中，我们对训练循环做了一个小改动。现在调用的是 `train_acc.forward()`（更准确地说，是等价的简写 `train_acc()`），而不是 `train_acc.update()`。`.forward()` 调用在底层做了很多事情，我们稍后会讨论。现在先看看结果：

**输入：**

```python
train_acc = Accuracy()

torch.manual_seed(123)
for i in range(10):
    
    y_true = torch.randint(low=0, high=2, size=(10,))
    y_pred = torch.randint(low=0, high=2, size=(10,))
    
    # the following two lines are equivalent:
    # abc = train_acc.forward(y_true, y_pred) 
    abc = train_acc(y_true, pred) 
    
    print('Batch accuracy:', abc)
    
print('Overall accuracy:', train_acc.compute())
```

**输出：**

```python
Batch accuracy: tensor(0.7000)
Batch accuracy: tensor(0.7000)
Batch accuracy: tensor(0.5000)
Batch accuracy: tensor(0.6000)
Batch accuracy: tensor(0.4000)
Batch accuracy: tensor(0.4000)
Batch accuracy: tensor(0.6000)
Batch accuracy: tensor(0.6000)
Batch accuracy: tensor(0.5000)
Batch accuracy: tensor(0.6000)
Overall accuracy: tensor(0.5600)
```

如我们所见，总体准确率与之前相同（正如我们所料 😊）。不过，我们现在还得到了中间结果：各批准确率。批准确率指的是给定小批量的准确率。作为参考，下面是手动计算时的样子：

**输入：**

```python
torch.manual_seed(123)

num = 0
correct = 0.

for i in range(10):
    y_true = torch.randint(low=0, high=2, size=(10,))
    y_pred = torch.randint(low=0, high=2, size=(10,))
    
    correct_batch = (y_true == pred).float().sum()
    correct += correct_batch
    num += y_true.numel()
    
    abc = correct_batch / y_true.numel()
    print('Batch accuracy:', abc) 
    
acc = correct / num
print('Overall accuracy:', acc)
```

**输出：**

```python
Batch accuracy: tensor(0.7000)
Batch accuracy: tensor(0.7000)
Batch accuracy: tensor(0.5000)
Batch accuracy: tensor(0.6000)
Batch accuracy: tensor(0.4000)
Batch accuracy: tensor(0.4000)
Batch accuracy: tensor(0.6000)
Batch accuracy: tensor(0.6000)
Batch accuracy: tensor(0.5000)
Batch accuracy: tensor(0.6000)
Overall accuracy: tensor(0.5600)
```

如果我们关心的是验证集或测试集准确率，这个中间结果也许不是特别有用。不过，它在训练过程中跟踪训练集准确率时很方便，对损失函数之类的东西也很有用。这样，只需对训练集做一次遍历，就能同时画出每个小批量的中间损失和每个 epoch 的平均损失。

## .update() 与 .forward()——官方解释

在上一节我们看到，`.forward()` 和 `.update()` 做的事情略有不同。`.update()` 方法更简单：它只是更新指标。相比之下，`.forward()` 也会更新指标，但它还能让我们报告每次单独批更新的指标值。`.forward()` 本质上是一个更复杂的方法，它在底层使用了 `.update()`。

该用哪个方法？取决于使用场景。如果不关心跟踪或记录中间结果，用 `.update()` 就够了。然而，从训练深度神经网络的整体大局来看，调用 `.forward()` 的计算开销通常非常小，所以默认使用 `.forward()` 也无妨。

如果你对细节感兴趣，可以看看官方[文档](https://torchmetrics.readthedocs.io/en/latest/pages/implement.html#internal-implementation-details)中的这段摘录：

> `forward()` 方法通过按以下方式组合 `update` 和 `compute` 调用来实现这一点：

> 1. 调用 `update()` 更新全局指标状态（用于跨多个批次的累积）
> 2. 缓存全局状态
> 3. 调用 `reset()` 清除全局指标状态
> 4. 调用 `update()` 更新局部指标状态
> 5. 调用 `compute()` 计算当前批次的指标
> 6. 恢复全局状态

> 这个过程的后果是，在单次 `forward` 调用期间，用户定义的 `update` 会被调用两次（一次用于更新全局统计量，一次用于获取批统计量）。

## 附加内容：计算滚动平均值

正因为有独立的 `.update()` 和 `.compute()` 方法，我们才能计算指标的滚动平均值（而不是单个批次上的指标）。为此，我们可以在循环中加入一次 `.compute()` 调用：

**输入：**

```python
from torchmetrics.classification import Accuracy

train_acc = Accuracy()
torch.manual_seed(123)

for i in range(10):
    
    y_true = torch.randint(low=0, high=2, size=(10,))
    y_pred = torch.randint(low=0, high=2, size=(10,))
    
    train_acc.update(y_true, y_pred)
    abc = train_acc.compute()
    print('Running accuracy:', abc)
    
print('Overall accuracy:', train_acc.compute())
```

**输出：**

```python
Running accuracy: tensor(0.7000)
Running accuracy: tensor(0.7000)
Running accuracy: tensor(0.6333)
Running accuracy: tensor(0.6250)
Running accuracy: tensor(0.5800)
Running accuracy: tensor(0.5500)
Running accuracy: tensor(0.5571)
Running accuracy: tensor(0.5625)
Running accuracy: tensor(0.5556)
Running accuracy: tensor(0.5600)
Overall accuracy: tensor(0.5600)
```

上述代码等价于下面的手动计算：

**输入：**

```python
torch.manual_seed(123)

num = 0
correct = 0.

for i in range(10):
    y_true = torch.randint(low=0, high=2, size=(10,))
    y_pred = torch.randint(low=0, high=2, size=(10,))
    
    correct_batch = (y_true == y_pred).float().sum()
    correct += correct_batch
    num += y_true.numel()
    
    abc = correct / num
    print('Running accuracy:', abc) 
    
acc = correct / num
print('Overall accuracy:', acc)
```

**输出：**

```python
Running accuracy: tensor(0.7000)
Running accuracy: tensor(0.7000)
Running accuracy: tensor(0.6333)
Running accuracy: tensor(0.6250)
Running accuracy: tensor(0.5800)
Running accuracy: tensor(0.5500)
Running accuracy: tensor(0.5571)
Running accuracy: tensor(0.5625)
Running accuracy: tensor(0.5556)
Running accuracy: tensor(0.5600)
Overall accuracy: tensor(0.5600)
```
