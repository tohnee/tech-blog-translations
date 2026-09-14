---
title: "人工神经网络的激活函数"
title_en: "Activation Functions for Artificial Neural Networks"
source: https://sebastianraschka.com/faq/docs/activation-functions.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 人工神经网络的激活函数

> 原文：[Activation Functions for Artificial Neural Networks](https://sebastianraschka.com/faq/docs/activation-functions.html) · Sebastian Raschka's FAQ

激活函数将神经元的加权输入（通常写作 `z = wᵀx + b`）变换为该神经元的输出。非线性激活让神经网络得以学习非线性关系。如果没有非线性激活，一串全连接的线性层最终仍会塌缩为一个单一的线性变换（若各层使用偏置，则再加上一个偏置项）。

如何选择取决于函数的使用位置。隐藏层需要有用的梯度来进行训练。而在输出层，激活函数还会决定预测值的取值范围。例如，sigmoid 可以把二分类得分映射到 0 到 1 之间，而线性输出则可以表示任意实数值的回归预测。

## 常见激活函数

这里，`exp` 是指数函数，`log` 是自然对数。在零处的取值属于约定惯例；下表采用的是下方原始图表中的定义。

在窄屏设备上，可以左右滚动表格以查看所有列。

| 函数 | 公式 | 典型用途或局限 |
| --- | --- | --- |
| 单位阶跃（Unit step） | `z < 0` 时为 `0`，零处为 `0.5`，`z > 0` 时为 `1` | 感知机变体中的阈值决策。其导数在不连续点之外处处为零，因此不适合常规的反向传播。 |
| 符号函数（Sign） | `z < 0` 时为 `-1`，零处为 `0`，`z > 0` 时为 `1` | 带正负号的阈值决策；与阶跃函数有同样的梯度局限。 |
| 线性（Linear） | `z` | 不受限的回归输出，包括线性回归和 Adaline。 |
| 截断线性（Clipped linear） | `min(1, max(0, z + 0.5))` | 有界的分段线性响应。在线性区域之外梯度为零。 |
| Logistic sigmoid | `1 / (1 + exp(-z))` | 二分类概率与门控。输入为很大的正值或负值时梯度很小。 |
| 双曲正切（tanh） | `(exp(z) - exp(-z)) / (exp(z) + exp(-z))` | 输出介于 -1 和 1 之间，包括循环网络的状态。输入幅度很大时同样会饱和。 |
| ReLU | `max(0, z)` | 常见的隐藏层激活。输入为正时梯度保持为 1；输入为负时梯度为 0。 |
| Softplus | `log(1 + exp(z))` | ReLU 的平滑替代方案，输出恒为正。 |

## 实践中如何选择激活函数

对于一个基础的前馈网络，ReLU 是合理的隐藏层起点。它计算开销很小，但一个只接收到负输入的单元可能因为梯度为零而停止学习。[ReLU 导数 FAQ](https://sebastianraschka.com/faq/docs/relu-derivative.html) 解释了这一行为，包括在零处采用的约定。

在 PyTorch 中做二分类时，应将输出 logit 直接传入 [`BCEWithLogitsLoss`](https://docs.pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html)。该损失函数以数值稳定的方式将 sigmoid 与二元交叉熵结合在一起。只有在把 logit 转换为预测概率时，才需要单独应用 sigmoid。

对于类别互斥的多分类任务，[softmax](https://sebastianraschka.com/faq/docs/softmax.html) 会把得分向量转换为总和为 1 的概率。它与表中逐元素（elementwise）作用的函数不同，因为每个 softmax 输出都依赖于向量中的所有得分。

## 原始视觉参考

下面这张 2016 年的图表包含两处错误。tanh 的分母应为 `exp(z) + exp(-z)`，如上表以及 [PyTorch tanh 定义](https://docs.pytorch.org/docs/stable/generated/torch.nn.Tanh.html)所示。此外，截断线性函数并不是标准的 SVM 决策函数；SVM 是使用其决策得分的符号来进行分类的。

![Original 2016 activation-function chart; the tanh formula and SVM example are corrected in the text above](https://sebastianraschka.com/images/faq/activation-functions/activation-functions.png)
