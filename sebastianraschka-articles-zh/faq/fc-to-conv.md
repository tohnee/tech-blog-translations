---
title: "全连接层可以被卷积层替代吗？"
title_en: "Can Fully Connected Layers be Replaced by Convolutional Layers?"
source: https://sebastianraschka.com/faq/docs/fc-to-conv.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 全连接层可以被卷积层替代吗？

> 原文：[Can Fully Connected Layers be Replaced by Convolutional Layers?](https://sebastianraschka.com/faq/docs/fc-to-conv.html) · Sebastian Raschka's FAQ

可以，你可以在卷积神经网络中用卷积层替代全连接层，甚至能得到完全相同的行为或输出。有两种方法可以做到这一点：1) 选择一个与输入特征图尺寸相同的卷积核；或者 2) 使用多通道的 1x1 卷积。

为了说明并演示这一点，假设我们有一个 2x2 的输入图像：

```python
import torch
inputs = torch.tensor([[[[1., 2.],
                         [3., 4.]]]])

inputs.shape
```

```python
torch.Size([1, 1, 2, 2])
```

## 全连接层

一个将 4 个输入特征映射到 2 个输出的全连接层，其计算方式如下：

```python
fc = torch.nn.Linear(4, 2)

weights = torch.tensor([[1.1, 1.2, 1.3, 1.4],
                        [1.5, 1.6, 1.7, 1.8]])
bias = torch.tensor([1.9, 2.0])
fc.weight.data = weights
fc.bias.data = bias
```

```python
torch.relu(fc(inputs.view(-1, 4)))
```

```python
tensor([[14.9000, 19.0000]], grad_fn=<ReluBackward0>)
```

## 方法 1：使用与输入尺寸相同的卷积核

![](https://sebastianraschka.com/images/faq/fc-to-conv/fc-to-conv-1.png)

如果我们使用卷积核尺寸与输入特征数组大小相同的卷积层，就可以得到相同的输出：

```python
conv = torch.nn.Conv2d(in_channels=1,
                       out_channels=2,
                       kernel_size=inputs.squeeze(dim=(0)).squeeze(dim=(0)).size())
print(conv.weight.size())
print(conv.bias.size())
```

```python
torch.Size([2, 1, 2, 2])
torch.Size([2])
```

```python
conv.weight.data = weights.view(2, 1, 2, 2)
conv.bias.data = bias
```

```python
torch.relu(conv(inputs))
```

```python
tensor([[[[14.9000]],

         [[19.0000]]]], grad_fn=<ReluBackward0>)
```

## 方法 2：使用 1x1 卷积核

![](https://sebastianraschka.com/images/faq/fc-to-conv/fc-to-conv-2.png)

类似地，当我们将输入图像重塑为 num\_inputs x 1 x 1 的图像时，也可以用卷积层替代全连接层：

```python
conv = torch.nn.Conv2d(in_channels=4,
                       out_channels=2,
                       kernel_size=(1, 1))

conv.weight.data = weights.view(2, 4, 1, 1)
conv.bias.data = bias
torch.relu(conv(inputs.view(1, 4, 1, 1)))
```

```python
tensor([[[[14.9000]],

         [[19.0000]]]], grad_fn=<ReluBackward0>)
```
