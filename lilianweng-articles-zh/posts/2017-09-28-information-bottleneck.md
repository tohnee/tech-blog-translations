---
title: "用信息论解剖深度学习"
title_en: "Anatomize Deep Learning with Information Theory"
source: https://lilianweng.github.io/posts/2017-09-28-information-bottleneck/
crawled: 2026-09-08
translated: 2026-09-08
---

# 用信息论解剖深度学习

> 原文：[Anatomize Deep Learning with Information Theory](https://lilianweng.github.io/posts/2017-09-28-information-bottleneck/) · Lilian Weng（翁荔）

> 本文是对 Naftali Tishby 教授近期演讲"Information Theory in Deep Learning"的总结。演讲展示了如何应用信息论研究深度神经网络在训练过程中的生长与嬗变。

最近我观看了 Naftali Tishby 教授的演讲 ["Information Theory in Deep Learning"](https://youtu.be/bLqJHjXihK8)，觉得非常有意思。他展示了如何应用信息论来研究深度神经网络在训练过程中的生长与嬗变。利用[信息瓶颈（Information Bottleneck，IB）](https://arxiv.org/pdf/physics/0004057.pdf)方法，他为深度神经网络（DNN）提出了一种新的学习界——因为传统学习理论在参数量指数级庞大时已然失效。另一个敏锐的观察是：DNN 的训练包含两个截然不同的阶段：首先，网络被训练以完整地表征输入数据并最小化泛化误差；随后，它通过压缩输入的表征来学会遗忘无关的细节。

本文的大部分材料来自 Tishby 教授的演讲及[相关论文](https://lilianweng.github.io/posts/2017-09-28-information-bottleneck/#references)。

## 基础概念

[马尔可夫链](https://en.wikipedia.org/wiki/Markov_chain)

马尔可夫过程是一种["无记忆"](http://mathworld.wolfram.com/Memoryless.html)（也称"马尔可夫性"）的随机过程。马尔可夫链是一类包含多个离散状态的马尔可夫过程。也就是说，过程未来状态的条件概率只由当前状态决定，不依赖于过去的状态。

[Kullback–Leibler（KL）散度](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence)

KL 散度度量一个概率分布 $$p$$ 相对于另一个期望概率分布 $$q$$ 的偏离程度。它是不对称的。

$$
\begin{aligned}
D_{KL}(p \| q) &= \sum_x p(x) \log \frac{p(x)}{q(x)} \\
 &= - \sum_x p(x)\log q(x) + \sum_x p(x)\log p(x) \\
 &= H(P, Q) - H(P)
\end{aligned}
$$

当处处 $$p(x)$$ == $$q(x)$$ 时，$$D_{KL}$$ 取得最小值零。

[互信息](https://en.wikipedia.org/wiki/Mutual_information)

互信息度量两个变量之间的相互依赖性。它量化了通过一个随机变量所获得的关于另一个随机变量的"信息量"。互信息是对称的。

$$
\begin{aligned}
I(X;Y) &= D_{KL}[p(x,y) \| p(x)p(y)] \\
 &= \sum_{x \in X, y \in Y} p(x, y) \log(\frac{p(x, y)}{p(x)p(y)}) \\
 &= \sum_{x \in X, y \in Y} p(x, y) \log(\frac{p(x|y)}{p(x)}) \\ 
 &= H(X) - H(X|Y) \\
\end{aligned}
$$

[数据处理不等式（Data Processing Inequality，DPI）](https://en.wikipedia.org/wiki/Data_processing_inequality)

对任意马尔可夫链：$$X \to Y \to Z$$，我们有 $$I(X; Y) \geq I(X; Z)$$。

深度神经网络可以被视为一条马尔可夫链，因此当我们在 DNN 中逐层向下移动时，各层与输入之间的互信息只会减少。

[重参数化不变性](https://en.wikipedia.org/wiki/Parametrization#Parametrization_invariance)

对两个可逆函数 $$\phi$$、$$\psi$$，互信息保持不变：$$I(X; Y) = I(\phi(X); \psi(Y))$$。

例如，如果我们打乱 DNN 某一层中的权重，并不会影响这一层与另一层之间的互信息。

## 作为马尔可夫链的深度神经网络

训练数据包含从 $$X$$ 和 $$Y$$ 的联合分布中采样的观测值。输入变量 $$X$$ 和隐藏层的权重都是高维随机变量。在分类任务设定下，真实目标 $$Y$$ 和预测值 $$\hat{Y}$$ 是维度较小的随机变量。

![DNN 结构](https://lilianweng.github.io/posts/2017-09-28-information-bottleneck/ib-dnn-structure.png)

*图 1：深度神经网络的结构，由目标标签 $$Y$$、输入层 $$X$$、隐藏层 $$h_1, \dots, h_m$$ 以及最终预测 $$\hat{Y}$$ 组成。（图片来源：[Tishby and Zaslavsky, 2015](https://arxiv.org/pdf/1503.02406.pdf)）*

如果如图 1 那样把 DNN 的隐藏层标记为 $$h_1, h_2, \dots, h_m$$，我们可以把每一层看作马尔可夫链的一个状态：$$ h_i \to h_{i+1}$$。根据 DPI，我们有：

$$
H(X) \geq I(X; h_1) \geq I(X; h_2) \geq \dots \geq I(X; h_m) \geq I(X; \hat{Y}) \\
I(X; Y) \geq I(h_1; Y) \geq I(h_2; Y) \geq \dots \geq I(h_m; Y) \geq I(\hat{Y}; Y)
$$

DNN 的设计目标是学习如何描述 $$X$$ 以预测 $$Y$$，并最终将 $$X$$ 压缩到只保留与 $$Y$$ 相关的信息。Tishby 将这一过程描述为*"相关信息的逐级提炼（successive refinement of relevant information）"*。

### 信息平面定理

DNN 拥有对 $$X$$ 的一系列连续内部表征，即隐藏层集合 $$\{T_i\}$$。*信息平面（information plane）*定理用编码器信息和解码器信息来刻画每一层。编码器是对输入数据 $$X$$ 的一种表征，而解码器把当前层中的信息翻译为目标输出 $$Y$$。

准确地说，在信息平面图中：
- **横轴**：$$T_i$$ 的样本复杂度由编码器互信息 $$I(X; T_i)$$ 决定。样本复杂度指达到一定精度和泛化能力需要多少样本。
- **纵轴**：精度（泛化误差）由解码器互信息 $$I(T_i; Y)$$ 决定。

![信息平面](https://lilianweng.github.io/posts/2017-09-28-information-bottleneck/ib-information-plane.png)

*图 2：50 次实验中 DNN 隐藏层的编码器与解码器互信息。不同层用不同颜色标记，绿色是紧邻输入的层，橙色是最远的层。分别为初始轮、400 轮和 9000 轮时的三个快照。（图片来源：[Shwartz-Ziv and Tishby, 2017](https://arxiv.org/pdf/1703.00810.pdf)）*

图 2 中的每个点标记了某一次网络仿真中某一隐藏层的编码器/解码器互信息（未应用正则化；无权重衰减、无 dropout 等）。它们如预期般向上移动，因为关于真实标签的知识在增加（精度提升）。在早期阶段，隐藏层对输入 $$X$$ 学习得很多，但随后它们开始压缩、遗忘一些关于输入的信息。Tishby 认为*"学习最重要的部分其实是遗忘"*。可以看看这个[不错的视频](https://youtu.be/P1A1yNsxMjc)，它演示了各层互信息度量如何随训练轮次变化。

![信息平面合并视图](https://lilianweng.github.io/posts/2017-09-28-information-bottleneck/ib-information-plane-merged.png)

*图 3：图 2 的聚合视图。压缩发生在泛化误差变得很小之后。（图片来源：[Tishby 演讲 15:15](https://youtu.be/bLqJHjXihK8?t=15m15s)）*

### 两个优化阶段

追踪每层权重的归一化均值和标准差随时间的变化，同样能揭示训练过程的两个优化阶段。

![均值与标准差](https://lilianweng.github.io/posts/2017-09-28-information-bottleneck/ib-mean-variation.png)

*图 4：每层权重梯度的均值和标准差的范数随训练轮次变化的函数。不同层用不同颜色标记。（图片来源：[Shwartz-Ziv and Tishby, 2017](https://arxiv.org/pdf/1703.00810.pdf)）*

在早期轮次中，均值比标准差大三个数量级。经过足够多的轮次后，误差饱和，标准差随后变得噪声大得多。一层离输出越远，噪声越大，因为噪声会在反向传播过程中被放大和累积（而不是由层的宽度决定）。

## 学习理论

### "旧"泛化界

经典学习理论定义的泛化界为：

$$
\epsilon^2 < \frac{\log|H_\epsilon| + \log{1/\delta}}{2m}
$$

- $$\epsilon$$：训练误差与泛化误差之差。泛化误差度量算法对从未见过的数据的预测有多准。
- $$H_\epsilon$$：假设类的 $$\epsilon$$-覆盖。通常我们假设其大小 $$\vert H_\epsilon \vert \sim (1/\epsilon)^d$$。
- $$\delta$$：置信度。
- $$m$$：训练样本数。
- $$d$$：假设的 VC 维。

这个定义说明：训练误差与泛化误差之差被假设空间大小和数据集大小的函数所约束。假设空间越大，泛化误差越大。如果你想阅读更多关于泛化界的内容，推荐这个 ML 理论教程：[part1](https://mostafa-samir.github.io/ml-theory-pt1/) 和 [part2](https://mostafa-samir.github.io/ml-theory-pt2/)。

然而，它对深度学习并不成立。网络越大，需要学习的参数越多。按照这个泛化界，更大的网络（更大的 $$d$$）会有更差的界。这与"更大的网络凭借更强的表达能力能取得更好性能"的直觉相矛盾。

### "新"输入压缩界

为了解决这一反直觉的观察，Tishby 等人为 DNN 提出了新的输入压缩界（input compression bound）。

首先，令 $$T_\epsilon$$ 为输入变量 $$X$$ 的一个 $$\epsilon$$-划分。该划分按照对标签的同质性把输入压缩成小单元，这些单元合起来可以覆盖整个输入空间。如果预测输出二值，我们可以用 $$2^{\vert T_\epsilon \vert}$$ 替换假设类的基数 $$\vert H_\epsilon \vert$$。

$$
|H_\epsilon| \sim 2^{|X|} \to 2^{|T_\epsilon|}
$$

当 $$X$$ 很大时，$$X$$ 的大小约为 $$2^{H(X)}$$。$$\epsilon$$-划分中的每个单元大小为 $$2^{H(X \vert T_\epsilon)}$$。因此我们有 $$\vert T_\epsilon \vert \sim \frac{2^{H(X)}}{2^{H(X \vert T_\epsilon)}} = 2^{I(T_\epsilon; X)}$$。于是输入压缩界变为：

$$
\epsilon^2 < \frac{2^{I(T_\epsilon; X)} + \log{1/\delta}}{2m}
$$

![IB 界](https://lilianweng.github.io/posts/2017-09-28-information-bottleneck/ib-bound.png)

*图 5：黑线是可达到的最优信息瓶颈（IB）极限。红线对应在有限样本集上训练时，样本外 IB 失真的上界。$$\Delta C$$ 是复杂度间隙，$$\Delta G$$ 是泛化间隙。（依据 [Tishby 演讲 24:50](https://youtu.be/bLqJHjXihK8?t=24m56s) 重绘）*

## 网络规模与训练数据规模

### 更多隐藏层的益处

拥有更多的层能带来计算上的收益，并加速训练过程以获得良好的泛化。

![层数](https://lilianweng.github.io/posts/2017-09-28-information-bottleneck/ib-layers.png)

*图 6：隐藏层越多，优化时间越短（轮次越少）。（图片来源：[Shwartz-Ziv and Tishby, 2017](https://arxiv.org/pdf/1703.00810.pdf)）*

**通过随机松弛实现压缩**：根据[扩散方程](https://en.wikipedia.org/wiki/Fokker%E2%80%93Planck_equation)，第 $$k$$ 层的松弛时间与该层压缩量 $$\Delta S_k$$ 的指数成正比：$$\Delta t_k \sim \exp(\Delta S_k)$$。我们可以把层压缩量计算为 $$\Delta S_k = I(X; T_k) - I(X; T_{k-1})$$。由于 $$\exp(\sum_k \Delta S_k) \geq \sum_k \exp(\Delta S_k)$$，我们可以预期隐藏层越多（$$k$$ 越大），训练轮次呈指数级下降。

### 更多训练样本的益处

拟合更多训练数据需要隐藏层捕获更多信息。随着训练数据规模增大，解码器互信息（回忆一下，它与泛化误差直接相关）$$I(T; Y)$$ 被推高，更接近理论上的信息瓶颈界。Tishby 强调，决定泛化的是互信息，而不是层的规模或 VC 维——这一点不同于标准理论。

![训练规模](https://lilianweng.github.io/posts/2017-09-28-information-bottleneck/ib-training-size.png)

*图 7：不同规模的训练数据用不同颜色标记。图中绘制了多个收敛网络的信息平面。训练数据越多，泛化越好。（图片来源：[Shwartz-Ziv and Tishby, 2017](https://arxiv.org/pdf/1703.00810.pdf)）*

---
引用格式：
```
@article{weng2017infotheory,
  title   = "Anatomize Deep Learning with Information Theory",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2017",
  url     = "http://lilianweng.github.io/lil-log/2017/09/28/anatomize-deep-learning-with-information-theory.html"
}
```

## 参考文献

[1] Naftali Tishby. [Information Theory of Deep Learning](https://youtu.be/bLqJHjXihK8)

[2] [Machine Learning Theory - Part 1: Introduction](https://mostafa-samir.github.io/ml-theory-pt1/)

[3] [Machine Learning Theory - Part 2: Generalization Bounds](https://mostafa-samir.github.io/ml-theory-pt2/)

[4] [New Theory Cracks Open the Black Box of Deep Learning](https://www.quantamagazine.org/new-theory-cracks-open-the-black-box-of-deep-learning-20170921/) by Quanta Magazine.

[5] Naftali Tishby and Noga Zaslavsky. ["Deep learning and the information bottleneck principle."](https://arxiv.org/pdf/1503.02406.pdf) IEEE Information Theory Workshop (ITW), 2015.

[6] Ravid Shwartz-Ziv and Naftali Tishby. ["Opening the Black Box of Deep Neural Networks via Information."](https://arxiv.org/pdf/1703.00810.pdf) arXiv preprint arXiv:1703.00810, 2017.
