---
title: "为什么 ReLU 函数在 x=0 处不可导？"
title_en: "Why is the ReLU function not differentiable at x=0?"
source: https://sebastianraschka.com/faq/docs/relu-derivative.html
crawled: 2026-09-06
translated: 2026-09-14
---

# 为什么 ReLU 函数在 x=0 处不可导？

导数存在的一个必要条件是给定函数连续。那么修正线性单元（ReLU）函数满足这个条件吗？为了回答这个问题，我们先来看一下 ReLU 函数的数学定义：

![](https://sebastianraschka.com/images/faq/relu-derivative/relu_1.png)

或者表示为分段定义函数：

![](https://sebastianraschka.com/images/faq/relu-derivative/relu_2.png)

对于上一个式子的上半部分和下半部分，都有 *f(0)=0*，因此我们可以清楚地看到 ReLU 函数是连续的。如果这一点还不够一目了然，那么画出 ReLU 函数的图像就能看得非常清楚：

![](https://sebastianraschka.com/images/faq/relu-derivative/relu_3.png)

**请注意，所有可导函数都是连续函数，但这一事实并不意味着每个连续函数都可导。**

ReLU 函数的导数在 *x=0* 处没有定义，原因用通俗的话说就是：该函数在 *x=0* 处不「光滑」。

更具体地说，一个函数要在某点可导，极限必须存在。而极限要存在，必须满足以下 3 个条件：

1. 左极限存在
2. 右极限存在
3. 左极限与右极限相等

在逐条讨论之前，请记住，要用导数的基本定义求函数 *f(x)* 的导数，我们使用下式：

![](https://sebastianraschka.com/images/faq/relu-derivative/deriv-1.png)

其中 Δx 是一个无穷小的、「几乎为零」的数。这基本上也就是所谓的「变化率」（即函数输入发生微小变化时，输出会变化多少）。

我们可以直接把 *f(x)* 替换成 *max(0, x)*，用它来计算 ReLU 函数在 *x != 0* 处的导数：

![](https://sebastianraschka.com/images/faq/relu-derivative/deriv-2.png)

然后，我们得到 **x > 0 时的导数**，

![](https://sebastianraschka.com/images/faq/relu-derivative/deriv-3.png)

以及 **x < 0 时的导数**，

![](https://sebastianraschka.com/images/faq/relu-derivative/deriv-4.png)

现在，为了理解为什么在零处的导数不存在（即 **f'(0)=DNE**），我们需要考察左极限和右极限。也就是说，让我们从左侧逼近「0」（即把 Δx 想象成一个无穷小的负数，然后把它代入前面的式子）：

![](https://sebastianraschka.com/images/faq/relu-derivative/deriv-2.png)

![](https://sebastianraschka.com/images/faq/relu-derivative/deriv-5.png)

然后我们对右极限做同样的事情：

![](https://sebastianraschka.com/images/faq/relu-derivative/deriv-2.png)

![](https://sebastianraschka.com/images/faq/relu-derivative/deriv-6.png)

可以看到，左极限和右极限并不相等，因此在 x=0 处不存在单一的导数；于是我们说导数 f'(x=0) 没有定义或不存在（DNE）：

![](https://sebastianraschka.com/images/faq/relu-derivative/deriv-7.png)

在实践中，深度学习场景里恰好遇到 x=0 的情况相当罕见，因此我们通常不必太担心 ReLU 在 x=0 处的导数。通常，我们会把它设为 0、1 或 0.5。
