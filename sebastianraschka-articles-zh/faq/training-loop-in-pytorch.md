---
title: "PyTorch 中的训练循环长什么样？"
title_en: "How does a training loop in PyTorch look like?"
source: https://sebastianraschka.com/faq/docs/training-loop-in-pytorch.html
crawled: 2026-09-06
translated: 2026-09-14
---

# PyTorch 中的训练循环长什么样？

## PyTorch 中一个典型的训练循环

假设我们想训练一个用于监督学习的深度神经网络——它既可以是分类任务，也可以是回归任务。

在 [PyTorch](https://pytorch.org) 中，一个训练循环通常长这样：

```python
model = MyNeuralNetwork(...)
optimizer = torch.optim.SGD(
  model.parameters(), lr=0.01, momentum=0.9
)

for epoch in range(num_epochs):
    for batch_idx, (features, targets) in enumerate(train_loader):
            
        forward_pass_outputs = model(features)
        loss = loss_fn(forward_pass_outputs, targets)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```

在上面的伪代码中，我们用两个 for 循环来实现基于随机梯度下降优化的反向传播。内层 for 循环（`for batch_idx ...`）之下嵌套的代码定义了一个训练步（training step），也常被直接称为一次「迭代」（iteration）。每次迭代中，我们从训练集取出一个*批次*（batch），它由两个张量组成：模型输入（特征）和目标值。在图像分类场景下，模型输入是图像，目标值是对应的类别标签。例如，下图展示了一个批次（批大小任意取 7）中的特征和目标：

![Example batch showing input feature images paired with target labels](https://sebastianraschka.com/images/faq/training-loop-in-pytorch/targets-and-features.png)

（注意每张图像本身是一个 32x32x3 像素的张量，不过这可能过于细节了。）

接下来，`model(features)` 执行前向传播，计算模型输出，并在幕后构建一张计算图。这里的 `model` 是任意的监督学习模型。注意，我们在此刻意不对返回值 `forward_pass_outputs` 做具体说明，这个话题留到后面的章节再谈。下图在一个简单的概念性多层感知机中展示了前向传播：

![Simple multilayer perceptron showing the forward pass from inputs to outputs](https://sebastianraschka.com/images/faq/training-loop-in-pytorch/mlp-1.png)

然后，通过 `loss_fn`，我们执行一个度量模型输出与期望目标值之间差异的计算。这个计算同样会被加入幕后已有的计算图。与模型的返回值类似，我们刻意不给出损失函数的具体定义，因为我们要先建立整体图景。从技术上讲，我们可以把损失计算视为训练期间前向传播的一部分，如下图所示：

![Multilayer perceptron diagram extended with the loss computation during training](https://sebastianraschka.com/images/faq/training-loop-in-pytorch/mlp-2.png)

下面这几行是真正有意思的地方，它们定义了训练神经网络的[反向传播](https://sebastianraschka.com/blog/2021/dl-course.html#l09-multilayer-perceptrons-and-backpropration)过程：

```python
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

`optimizer` 通常是一个基于梯度下降的优化器对象，例如标准随机梯度下降、[ADAM](https://arxiv.org/abs/1412.6980) 等。

执行反向传播时，PyTorch 允许我们累积梯度——这是一个高级概念，只与某些类型的优化算法相关。不过，既然存在这个选项，我们就必须手动确保在每轮反向传播之前把梯度重置为零，这通过 `optimizer.zero_grad()` 完成。

调用 `loss.backward()` 会在前向传播（`model(features)` 与 `loss_fn(...)`）所定义的计算图上运行[反向模式自动微分](https://en.wikipedia.org/wiki/Automatic_differentiation#Reverse_accumulation)。调用 `loss.backward()` 会计算损失关于权重的梯度，这些梯度是用随机梯度下降更新权重所必需的，更新发生在下一步调用 `optimizer.step()` 时。

为了便于说明，下图勾画了反向传播步骤，高亮了计算第一个隐藏层中某个权重的梯度所涉及的所有连接（这一计算要用到多元链式法则）：

![Backpropagation diagram highlighting gradient flow through a multilayer perceptron](https://sebastianraschka.com/images/faq/training-loop-in-pytorch/mlp-3.png)

最后，外层 for 循环（`for epoch in range(num_epochs):`）对训练集进行多轮批次迭代和训练步（*epoch* 其实只是「完整遍历一遍训练集」的一个花哨说法，即每个训练样本恰好被访问一次。）

### 训练循环小结

回顾总结一下：PyTorch 中一个典型的训练循环会在给定 epoch 数内迭代各批次。在每次批次迭代中，我们先计算前向传播以获得神经网络输出：

```python
forward_pass_outputs = model(features)
loss = loss_fn(forward_pass_outputs, targets)
```

然后，我们重置上一次迭代的梯度并执行反向传播，得到损失关于模型权重的梯度：

```python
optimizer.zero_grad()
loss.backward()
```

最后，我们基于损失梯度用随机梯度下降更新权重：

```python
optimizer.step()
```

### 附加内容：PyTorch Lightning 中的训练循环

如果我们使用 [PyTorch Lightning](https://www.pytorchlightning.ai)，就不必操心定义训练循环，它会替我们处理好。

---

**什么是 PyTorch Lightning？**

PyTorch Lightning 是一个帮助你组织 PyTorch 代码、减少样板代码的库，它让日志记录、检查点保存、多 GPU 训练等多个最佳实践和高级实践变得更容易。

---

下面的最小示例把前面的 PyTorch 示例放到 PyTorch Lightning 环境中：

```python
import pytorch_lightning as pl

# LightningModule that receives a PyTorch model as input
class LightningModel(pl.LightningModule):
    def __init__(self, model, ...):
        super().__init__()
        ...
  
    def training_step(self, batch, batch_idx):
        features, targets = batch
        forward_pass_outputs = model(features)
        loss = loss_fn(forward_pass_outputs, targets)
				... 
        return loss  # this is passed to the optimzer for training

    ... 

    def configure_optimizers(self):
        optimizer = torch.optim.SGD(self.parameters(), lr=self.learning_rate)
        return optimizer
      
...
trainer = pl.Trainer(
    max_epochs=NUM_EPOCHS,
    ...
)

lightning_model = LightningModel(pytorch_model, ...)
trainer.fit(model=lightning_model, ...)
```

（如果你感兴趣，我在[这里](https://github.com/rasbt/deeplearning-models/blob/master/pytorch-lightning_ipynb/mlp/mlp-basic.ipynb)有一个完整、自包含的示例。）

在 PyTorch Lightning 中，我们在 `training_step` 方法内定义训练循环中一个步骤的代码。注意，这与我们前一节用来定义前向传播的伪代码相同。现在我们不必再操心反向传播，`Trainer` 会在我们调用 `trainer.fit(...)` 时自动处理它。
