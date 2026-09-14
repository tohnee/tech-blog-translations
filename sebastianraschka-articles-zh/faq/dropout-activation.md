---
title: "dropout 是在非线性激活函数之前还是之后施加？"
title_en: "Is dropout applied before or after the non-linear activation function?"
source: https://sebastianraschka.com/faq/docs/dropout-activation.html
crawled: 2026-09-06
translated: 2026-09-14
---

# dropout 是在非线性激活函数之前还是之后施加？

> 原文：[Is dropout applied before or after the non-linear activation function?](https://sebastianraschka.com/faq/docs/dropout-activation.html) · Sebastian Raschka's FAQ

通常，dropout 施加在非线性激活函数之后（a）。不过，在使用修正线性单元（ReLU）时，出于计算效率的考虑（取决于具体的代码实现），把 dropout 施加在非线性激活之前（b）也可能是合理的。

> (a)：全连接、线性激活 -> ReLU -> Dropout -> …  
> (b)：全连接、线性激活 -> Dropout -> ReLU -> …

为什么在使用 ReLU 时 (a) 和 (b) 会产生相同的结果？让我们用一个简单的例子来回答这个问题，起点是如下 *logits*（全连接层线性激活的输出）：

> `[-1, -2, -3, 4, 5, 6]`

我们先走一遍场景 (a)，先施加 ReLU 激活。非线性 ReLU 函数的输出如下：

> `[0, 0, 0, 4, 5, 6]`

记住，ReLU 激活函数定义为 \(f(x) = max(0, x)\)；因此，所有负值都会被变成零。现在，以 50% 的概率施加 dropout，假设被停用的单元是第 2、4、6 个单元：

> `[0*2, 0, 0*2, 0, 0*2, 0] = [0, 0, 0, 0, 10, 0]`

注意，在 dropout 中，单元默认是随机停用的。在上面的例子里，我们假设第 2、4、6 个单元在该次训练迭代中被停用。另外，由于我们以 50% 的 dropout 概率施加 dropout，我们把保留的单元放大了 2 倍。

现在来看场景 (b)。同样，我们假设 dropout 比率为 50%，且第 2、4、6 个单元被停用：

> `[-1, -2, -3, 4, 5, 6] -> [-1*2, 0, -3*2, 0, 5*2, 0]`

现在，如果把这个数组传入 ReLU 函数，得到的数组会与场景 (a) 中的完全一样：

> `[-2, 0, -6, 0, 10, 0] -> [0, 0, 0, 0, 10, 0]`
