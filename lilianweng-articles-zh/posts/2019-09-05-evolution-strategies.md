---
title: "进化策略"
title_en: "Evolution Strategies"
source: https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/
crawled: 2026-09-08
translated: 2026-09-08
---

# 进化策略

> 原文：[Evolution Strategies](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/) · Lilian Weng（翁荔）

> 在学习最优模型参数时，梯度下降并不是唯一的选择。当我们不知道目标函数的精确解析形式、或无法直接计算梯度时，进化策略（Evolution Strategies，ES）往往能有很好的效果。本文深入介绍几种经典的 ES 方法，以及 ES 如何应用于深度强化学习。



随机梯度下降是优化深度学习模型的通用选择，但它并不是唯一的选项。借助黑盒优化（black-box optimization）算法，你可以评估目标函数 $$f(x): \mathbb{R}^n \to \mathbb{R}$$，即使你并不知道 $$f(x)$$ 的精确解析形式、因而无法计算梯度或海森矩阵（Hessian matrix）。黑盒优化方法包括[模拟退火](https://en.wikipedia.org/wiki/Simulated_annealing)、[爬山法](https://en.wikipedia.org/wiki/Hill_climbing)和 [Nelder-Mead 方法](https://en.wikipedia.org/wiki/Nelder%E2%80%93Mead_method)等。

**进化策略（Evolution Strategies，ES）**是一类黑盒优化算法，诞生于**进化算法（Evolutionary Algorithms，EA）**家族。在本文中，我会深入探讨几种经典的 ES 方法，并介绍 ES 在深度强化学习中的若干应用。





## 什么是进化策略？

进化策略（ES）属于进化算法这个大家族。ES 的优化目标是实数向量 $$x \in \mathbb{R}^n$$。

进化算法指的是一类基于种群的优化算法，其灵感来自*自然选择*（natural selection）。自然选择的理念是：拥有有利于生存的性状的个体能够存活繁衍，并把优良特性传给下一代。进化在选择过程中逐渐发生，种群对环境的适应也随之越来越好。


![EA](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/EA-illustration.png)

*图 1. 自然选择如何起作用。（图片来源：可汗学院：[达尔文、进化与自然选择](https://www.khanacademy.org/science/biology/her/evolution-and-natural-selection/a/darwin-evolution-natural-selection)）*

进化算法可以按以下[格式](https://ipvs.informatik.uni-stuttgart.de/mlr/marc/teaching/13-Optimization/06-blackBoxOpt.pdf)总结为一种通用的优化解决方案：

假设我们想优化一个函数 $$f(x)$$，并且无法直接计算梯度，但给定任意 $$x$$ 我们仍然可以评估 $$f(x)$$，而且结果是确定性的。我们用一个概率分布来表达「$$x$$ 是 $$f(x)$$ 优化问题的好解」这一置信程度，该分布为 $$p_\theta(x)$$，由 $$\theta$$ 参数化。目标是找到 $$\theta$$ 的最优配置。

> 这里，在给定固定分布形式（即高斯分布）的前提下，参数 $$\theta$$ 承载着关于最优解的知识，并随着世代迭代更新。


从 $$\theta$$ 的初始值开始，我们可以通过循环以下三个步骤来不断更新 $$\theta$$：
1. 生成一个样本种群 $$D = \{(x_i, f(x_i)\}$$，其中 $$x_i \sim p_\theta(x)$$。
2. 评估 $$D$$ 中样本的「适应度」（fitness）。
3. 选出最优的个体子集，用它们来更新 $$\theta$$，一般依据适应度或排名。

在 EA 的另一个流行子类——**遗传算法（Genetic Algorithms，GA）**——中，$$x$$ 是一个二进制编码序列，$$x \in \{0, 1\}^n$$；而在 ES 中，$$x$$ 只是一个实数向量，$$x \in \mathbb{R}^n$$。



## 简单高斯进化策略

[这里](http://blog.otoro.net/2017/10/29/visual-evolution-strategies/)介绍的是最基础、最经典的进化策略版本。它将 $$p_\theta(x)$$ 建模为一个 $$n$$ 维各向同性高斯分布，其中 $$\theta$$ 只跟踪均值 $$\mu$$ 和标准差 $$\sigma$$。

$$
\theta = (\mu, \sigma),\;p_\theta(x) \sim \mathcal{N}(\mathbf{\mu}, \sigma^2 I) = \mu + \sigma \mathcal{N}(0, I)
$$

给定 $$x \in \mathcal{R}^n$$，简单高斯 ES 的流程如下：
1. 初始化 $$\theta = \theta^{(0)}$$ 和代数计数器 $$t=0$$
2. 通过从高斯分布中采样，生成大小为 $$\Lambda$$ 的子代种群：<br/><br/>$$D^{(t+1)}=\{ x^{(t+1)}_i \mid x^{(t+1)}_i = \mu^{(t)} + \sigma^{(t)} y^{(t+1)}_i \text{ where } y^{(t+1)}_i \sim \mathcal{N}(x \vert 0, \mathbf{I}),\;i = 1, \dots, \Lambda\}$$<br/>。
3. 选出 $$f(x_i)$$ 最优的 $$\lambda$$ 个样本构成的子集，该子集被称为**精英（elite）**集合。不失一般性，我们可以把 $$D^{(t+1)}$$ 中前 $$k$$ 个样本视为属于精英组——我们将它们标记为<br/><br/>$$D^{(t+1)}_\text{elite} = \{x^{(t+1)}_i \mid x^{(t+1)}_i \in D^{(t+1)}, i=1,\dots, \lambda, \lambda\leq \Lambda\}$$<br/>。
4. 然后我们用精英集合为下一代估计新的均值和标准差：<br/><br/>
$$
\begin{aligned}
\mu^{(t+1)} &= \text{avg}(D^{(t+1)}_\text{elite}) = \frac{1}{\lambda}\sum_{i=1}^\lambda x_i^{(t+1)} \\
{\sigma^{(t+1)}}^2 &= \text{var}(D^{(t+1)}_\text{elite}) = \frac{1}{\lambda}\sum_{i=1}^\lambda (x_i^{(t+1)} -\mu^{(t)})^2
\end{aligned}
$$<br/>
5. 重复步骤 (2)-(4)，直到结果足够好 ✌️



## 协方差矩阵自适应进化策略（CMA-ES）

标准差 $$\sigma$$ 决定了探索的程度：$$\sigma$$ 越大，我们能够从中采样子代种群的搜索空间就越大。在[朴素 ES](#simple-gaussian-evolution-strategies) 中，$$\sigma^{(t+1)}$$ 与 $$\sigma^{(t)}$$ 高度相关，因此算法无法在需要时（即置信水平变化时）快速调整探索空间。

[**CMA-ES**](https://en.wikipedia.org/wiki/CMA-ES)，全称*「协方差矩阵自适应进化策略」（Covariance Matrix Adaptation Evolution Strategy）*，通过用协方差矩阵 $$C$$ 跟踪分布中样本之间的两两依赖关系来解决这个问题。新的分布参数变为：


$$
\theta = (\mu, \sigma, C),\; p_\theta(x) \sim \mathcal{N}(\mu, \sigma^2 C) \sim \mu + \sigma \mathcal{N}(0, C)
$$

其中 $$\sigma$$ 控制分布的整体尺度，通常被称为*步长*（step size）。

在深入研究 CMA-ES 的参数如何更新之前，最好先回顾一下协方差矩阵在多元高斯分布中是如何起作用的。作为一个实对称矩阵，协方差矩阵 $$C$$ 具有以下良好性质（见[证明](http://s3.amazonaws.com/mitsloan-php/wp-faculty/sites/30/2016/12/15032137/Symmetric-Matrices-and-Eigendecomposition.pdf)与[证明](http://control.ucsd.edu/mauricio/courses/mae280a/lecture11.pdf)）：
- 它总是可以对角化。
- 总是半正定的。
- 其所有特征值都是实的非负数。
- 其所有特征向量都相互正交。
- 它的特征向量构成了 $$\mathbb{R}^n$$ 的一组标准正交基。

设矩阵 $$C$$ 有一组*标准正交的*特征向量基 $$B = [b_1, \dots, b_n]$$，对应的特征值为 $$\lambda_1^2, \dots, \lambda_n^2$$。设 $$D=\text{diag}(\lambda_1, \dots, \lambda_n)$$。


$$
C = B^\top D^2 B
= \begin{bmatrix} 
\mid & \mid &  & \mid \\
b_1 & b_2 & \dots & b_n\\
\mid & \mid &  & \mid \\
\end{bmatrix}
\begin{bmatrix}
\lambda_1^2 & 0 & \dots & 0 \\
0 & \lambda_2^2 & \dots & 0 \\
\vdots & \dots & \ddots & \vdots \\
0 & \dots & 0 & \lambda_n^2
\end{bmatrix}
\begin{bmatrix} 
- & b_1 & - \\
- & b_2 & - \\
  & \dots & \\
- & b_n & - \\
\end{bmatrix}
$$

$$C$$ 的平方根为：

$$
C^{\frac{1}{2}} = B^\top D B
$$



| 符号 | 含义 |
| ---------- | ---------- |
| $$x_i^{(t)} \in \mathbb{R}^n$$ | 第 (t) 代的第 $$i$$ 个样本 |
| $$y_i^{(t)} \in \mathbb{R}^n$$ | $$x_i^{(t)} = \mu^{(t-1)} + \sigma^{(t-1)} y_i^{(t)} $$ |
| $$\mu^{(t)}$$ | 第 (t) 代的均值 |
| $$\sigma^{(t)}$$ | 步长 |
| $$C^{(t)}$$ | 协方差矩阵 |
| $$B^{(t)}$$ | 由 $$C$$ 的特征向量作为行向量组成的矩阵 |
| $$D^{(t)}$$ | 以 $$C$$ 的特征值为对角元的对角矩阵。 |
| $$p_\sigma^{(t)}$$ | 第 (t) 代 $$\sigma$$ 的进化路径 |
| $$p_c^{(t)}$$ | 第 (t) 代 $$C$$ 的进化路径 |
| $$\alpha_\mu$$ | $$\mu$$ 更新的学习率 |
| $$\alpha_\sigma$$ | $$p_\sigma$$ 的学习率 |
| $$d_\sigma$$ | $$\sigma$$ 更新的阻尼因子 |
| $$\alpha_{cp}$$ | $$p_c$$ 的学习率 |
| $$\alpha_{c\lambda}$$ | $$C$$ 的 rank-min(λ, n) 更新的学习率 |
| $$\alpha_{c1}$$ | $$C$$ 的 rank-1 更新的学习率 |



### 更新均值

$$
\mu^{(t+1)} = \mu^{(t)} + \alpha_\mu \frac{1}{\lambda}\sum_{i=1}^\lambda (x_i^{(t+1)} - \mu^{(t)})
$$

CMA-ES 有一个学习率 $$\alpha_\mu \leq 1$$ 来控制均值 $$\mu$$ 的更新速度。它通常被设为 1，此时该公式就变得与朴素 ES 中的相同，即 $$\mu^{(t+1)} = \frac{1}{\lambda}\sum_{i=1}^\lambda (x_i^{(t+1)}$$。



### 控制步长

采样过程可以与均值和标准差解耦：

$$
x^{(t+1)}_i = \mu^{(t)} + \sigma^{(t)} y^{(t+1)}_i \text{, where } y^{(t+1)}_i = \frac{x_i^{(t+1)} - \mu^{(t)}}{\sigma^{(t)}} \sim \mathcal{N}(0, C)
$$


参数 $$\sigma$$ 控制分布的整体尺度。它被从协方差矩阵中分离出来，这样我们改变步长的速度就能快于改变完整协方差的速度。更大的步长意味着更快的参数更新。为了评估当前步长是否合适，CMA-ES 通过对一连串移动步 $$\frac{1}{\lambda}\sum_{i}^\lambda y_i^{(j)}, j=1, \dots, t$$ 求和来构造一条*进化路径*（evolution path）$$p_\sigma$$。通过将这条路径的长度与随机选择（即各单步之间不相关）情形下的期望长度进行比较，我们就能够相应地调整 $$\sigma$$（见图 2）。


![CMA-ES step size](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/CMA-ES-step-size-path.png)

*图 2. 单步之间以不同方式相关的三种情形及其对步长更新的影响。（图片来源：在 [CMA-ES 教程](https://arxiv.org/abs/1604.00772)论文图 5 基础上添加标注）*

进化路径每次都用同一代中移动步 $$y_i$$ 的平均值来更新。

$$
\begin{aligned}
&\frac{1}{\lambda}\sum_{i=1}^\lambda y_i^{(t+1)} 
= \frac{1}{\lambda} \frac{\sum_{i=1}^\lambda x_i^{(t+1)} - \lambda \mu^{(t)}}{\sigma^{(t)}}
= \frac{\mu^{(t+1)} - \mu^{(t)}}{\sigma^{(t)}} \\
&\frac{1}{\lambda}\sum_{i=1}^\lambda y_i^{(t+1)} 
\sim \frac{1}{\lambda}\mathcal{N}(0, \lambda C^{(t)}) 
\sim \frac{1}{\sqrt{\lambda}}{C^{(t)}}^{\frac{1}{2}}\mathcal{N}(0, I) \\
&\text{Thus } \sqrt{\lambda}\;{C^{(t)}}^{-\frac{1}{2}} \frac{\mu^{(t+1)} - \mu^{(t)}}{\sigma^{(t)}} \sim \mathcal{N}(0, I)
\end{aligned}
$$


> 通过乘以 $$C^{-\frac{1}{2}}$$，进化路径被变换为与其方向无关。$${C^{(t)}}^{-\frac{1}{2}} = {B^{(t)}}^\top {D^{(t)}}^{-\frac{1}{2}} {B^{(t)}}$$ 这一变换的作用方式如下：
1. $${B^{(t)}}$$ 由 $$C$$ 的特征向量按行组成。它将原空间投影到相互垂直的主轴上。
2. 然后 $${D^{(t)}}^{-\frac{1}{2}} = \text{diag}(\frac{1}{\lambda_1}, \dots, \frac{1}{\lambda_n})$$ 将各主轴的长度缩放为相等。
3. $${B^{(t)}}^\top$$ 将空间变换回原坐标系。

为了给较近的世代赋予更高的权重，我们使用 Polyak 平均（polyak averaging）以学习率 $$\alpha_\sigma$$ 更新进化路径。同时，权重经过平衡，使得 $$p_\sigma$$ 在一次更新前后都[共轭](https://en.wikipedia.org/wiki/Conjugate_prior)，即 $$\sim \mathcal{N}(0, I)$$。


$$
\begin{aligned}
p_\sigma^{(t+1)} 
& = (1 - \alpha_\sigma) p_\sigma^{(t)} + \sqrt{1 - (1 - \alpha_\sigma)^2}\;\sqrt{\lambda}\; {C^{(t)}}^{-\frac{1}{2}} \frac{\mu^{(t+1)} - \mu^{(t)}}{\sigma^{(t)}} \\
& = (1 - \alpha_\sigma) p_\sigma^{(t)} + \sqrt{c_\sigma (2 - \alpha_\sigma)\lambda}\;{C^{(t)}}^{-\frac{1}{2}} \frac{\mu^{(t+1)} - \mu^{(t)}}{\sigma^{(t)}}
\end{aligned}
$$


随机选择下 $$p_\sigma$$ 的期望长度为 $$\mathbb{E}\|\mathcal{N}(0,I)\|$$，即 $$\mathcal{N}(0,I)$$ 随机变量的 L2 范数的期望。按照图 2 的思路，我们根据比值 $$\|p_\sigma^{(t+1)}\| / \mathbb{E}\|\mathcal{N}(0,I)\|$$ 来调整步长：


$$
\begin{aligned}
\ln\sigma^{(t+1)} &= \ln\sigma^{(t)} + \frac{\alpha_\sigma}{d_\sigma} \Big(\frac{\|p_\sigma^{(t+1)}\|}{\mathbb{E}\|\mathcal{N}(0,I)\|} - 1\Big) \\
\sigma^{(t+1)} &= \sigma^{(t)} \exp\Big(\frac{\alpha_\sigma}{d_\sigma} \Big(\frac{\|p_\sigma^{(t+1)}\|}{\mathbb{E}\|\mathcal{N}(0,I)\|} - 1\Big)\Big)
\end{aligned}
$$

其中 $$d_\sigma \approx 1$$ 是一个阻尼参数，调节 $$\ln\sigma$$ 变化的快慢。



### 协方差矩阵的自适应

对于协方差矩阵，可以用精英样本的 $$y_i$$ 从头开始估计（回顾 $$y_i \sim \mathcal{N}(0, C)$$）：

$$
C_\lambda^{(t+1)} 
= \frac{1}{\lambda}\sum_{i=1}^\lambda y^{(t+1)}_i {y^{(t+1)}_i}^\top
= \frac{1}{\lambda {\sigma^{(t)}}^2} \sum_{i=1}^\lambda (x_i^{(t+1)} - \mu^{(t)})(x_i^{(t+1)} - \mu^{(t)})^\top
$$

上述估计只有在选出的种群足够大时才可靠。然而，我们又确实希望每代只用*小*种群样本来*快速*迭代。正因如此，CMA-ES 发明了一种更可靠但也更复杂的 $$C$$ 更新方法。它包含两条独立的路线：
- *rank-min(λ, n) 更新（Rank-min(λ, n) update）*：使用 $$\{C_\lambda\}$$ 的历史，其中每一项都是在一代中从头估计的。
- *rank-1 更新（Rank-one update）*：从历史中估计移动步 $$y_i$$ 及其符号信息。

第一条路线考虑从 $$\{C_\lambda\}$$ 的全部历史中估计 $$C$$。例如，如果我们已经历了大量世代，那么 $$C^{(t+1)} \approx \text{avg}(C_\lambda^{(i)}; i=1,\dots,t)$$ 就是一个不错的估计量。与 $$p_\sigma$$ 类似，我们也使用带学习率的 Polyak 平均来纳入历史信息：

$$
C^{(t+1)} 
= (1 - \alpha_{c\lambda}) C^{(t)} + \alpha_{c\lambda} C_\lambda^{(t+1)}
= (1 - \alpha_{c\lambda}) C^{(t)} + \alpha_{c\lambda} \frac{1}{\lambda} \sum_{i=1}^\lambda y^{(t+1)}_i {y^{(t+1)}_i}^\top
$$

学习率的一个常见选择是 $$\alpha_{c\lambda} \approx \min(1, \lambda/n^2)$$。

第二条路线试图解决 $$y_i{y_i}^\top = (-y_i)(-y_i)^\top$$ 会丢失符号信息的问题。与调整步长 $$\sigma$$ 的方式类似，这里使用一条进化路径 $$p_c$$ 来跟踪符号信息，其构造方式保证 $$p_c$$ 在新旧两代之间都共轭，即 $$\sim \mathcal{N}(0, C)$$。

我们可以把 $$p_c$$ 看作计算 $$\text{avg}_i(y_i)$$ 的另一种方式（注意两者都 $$\sim \mathcal{N}(0, C)$$），但它使用了全部历史并且保留了符号信息。注意，我们在[上一节](#controlling-the-step-size)已经知道 $$\sqrt{k}\frac{\mu^{(t+1)} - \mu^{(t)}}{\sigma^{(t)}} \sim \mathcal{N}(0, C)$$，

$$
\begin{aligned}
p_c^{(t+1)} 
&= (1-\alpha_{cp}) p_c^{(t)} + \sqrt{1 - (1-\alpha_{cp})^2}\;\sqrt{\lambda}\;\frac{\mu^{(t+1)} - \mu^{(t)}}{\sigma^{(t)}} \\
&= (1-\alpha_{cp}) p_c^{(t)} + \sqrt{\alpha_{cp}(2 - \alpha_{cp})\lambda}\;\frac{\mu^{(t+1)} - \mu^{(t)}}{\sigma^{(t)}}
\end{aligned}
$$

然后根据 $$p_c$$ 更新协方差矩阵：

$$
C^{(t+1)} = (1-\alpha_{c1}) C^{(t)} + \alpha_{c1}\;p_c^{(t+1)} {p_c^{(t+1)}}^\top
$$

据称，当 $$k$$ 较小时，*rank-1 更新*方法相比 *rank-min(λ, n) 更新*能带来显著提升，因为移动步的符号以及连续步之间的相关性都被利用起来并逐代传递。

最终我们将两种方法结合在一起，

$$
C^{(t+1)} 
= (1 - \alpha_{c\lambda} - \alpha_{c1}) C^{(t)}
+ \alpha_{c1}\;\underbrace{p_c^{(t+1)} {p_c^{(t+1)}}^\top}_\textrm{rank-one update}
+ \alpha_{c\lambda} \underbrace{\frac{1}{\lambda} \sum_{i=1}^\lambda y^{(t+1)}_i {y^{(t+1)}_i}^\top}_\textrm{rank-min(lambda, n) update}
$$


![CMA-ES Algorithm](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/CMA-ES-algorithm.png)


在上述所有例子中，每个精英样本被认为贡献相同的权重 $$1/\lambda$$。这一过程可以很容易地扩展到根据表现给选出的样本赋予不同权重 $$w_1, \dots, w_\lambda$$ 的情形。更多细节见[教程](https://arxiv.org/abs/1604.00772)。


![CMA-ES Illustration](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/CMA-ES-illustration.png)

*图 3. CMA-ES 在一个 2D 优化问题上的工作原理示意（颜色越浅越好）。黑点是同一代中的样本。起初样本更加分散，而在后期模型对找到好解更有信心之后，样本变得非常集中在全局最优点附近。（图片来源：[维基百科 CMA-ES](https://en.wikipedia.org/wiki/CMA-ES)）*



## 自然进化策略

自然进化策略（Natural Evolution Strategies，**NES**；[Wierstra, et al, 2008](https://arxiv.org/abs/1106.4487)）在参数的搜索分布上进行优化，并沿着由*自然梯度*（natural gradient）所指明的高适应度方向移动该分布。


### 自然梯度

给定一个由 $$\theta$$ 参数化的目标函数 $$\mathcal{J}(\theta)$$，假设我们的目标是找到使目标函数值最大化的最优 $$\theta$$。*普通梯度*（plain gradient）寻找的是在距当前 $$\theta$$ 很小欧几里得距离范围内的最陡方向；这一距离约束作用在参数空间上。换句话说，我们计算普通梯度时依据的是 $$\theta$$ 绝对值的微小变化。最优步长为：


$$
d^{*} = \operatorname*{argmax}_{\|d\| = \epsilon} \mathcal{J}(\theta + d)\text{, where }\epsilon \to 0
$$

与此不同，*自然梯度*作用于由 $$\theta$$ 参数化的概率[分布](https://arxiv.org/abs/1301.3584v7)[空间](https://wiseodd.github.io/techblog/2018/03/14/natural-gradient/) $$p_\theta(x)$$（在 NES [论文](https://arxiv.org/abs/1106.4487)中称为「搜索分布」）。它在分布空间中寻找小步长内的最陡方向，其中距离由 KL 散度度量。有了这一约束，我们就能确保每次更新都以恒定速度沿分布流形移动，而不会因其曲率而变慢。


$$
d^{*}_\text{N} = \operatorname*{argmax}_{\text{KL}[p_\theta \| p_{\theta+d}] = \epsilon} \mathcal{J}(\theta + d)
$$



### 使用 Fisher 信息矩阵进行估计

但是，如何精确计算 $$\text{KL}[p_\theta \| p_{\theta+\Delta\theta}]$$？通过在 $$\theta$$ 处对 $$\log p_{\theta + d}$$ 做泰勒展开，我们得到：


$$
\begin{aligned}
& \text{KL}[p_\theta \| p_{\theta+d}] \\
&= \mathbb{E}_{x \sim p_\theta} [\log p_\theta(x) - \log p_{\theta+d}(x)] & \\
&\approx \mathbb{E}_{x \sim p_\theta} [ \log p_\theta(x) -( \log p_{\theta}(x) + \nabla_\theta \log p_{\theta}(x) d + \frac{1}{2}d^\top \nabla^2_\theta \log p_{\theta}(x) d)] & \scriptstyle{\text{; Taylor expand }\log p_{\theta+d}} \\
&\approx - \mathbb{E}_x [\nabla_\theta \log p_{\theta}(x)] d - \frac{1}{2}d^\top \mathbb{E}_x [\nabla^2_\theta \log p_{\theta}(x)] d & 
\end{aligned}
$$

其中

$$
\begin{aligned}
\mathbb{E}_x [\nabla_\theta \log p_{\theta}] d 
&= \int_{x\sim p_\theta} p_\theta(x) \nabla_\theta \log p_\theta(x) & \\
&= \int_{x\sim p_\theta} p_\theta(x) \frac{1}{p_\theta(x)} \nabla_\theta p_\theta(x) & \\
&= \nabla_\theta \Big( \int_{x} p_\theta(x) \Big) & \scriptstyle{\textrm{; note that }p_\theta(x)\textrm{ is probability distribution.}} \\
&= \nabla_\theta (1) = 0
\end{aligned}
$$

最终我们得到：

$$
\text{KL}[p_\theta \| p_{\theta+d}] = - \frac{1}{2}d^\top \mathbf{F}_\theta d 
\text{, where }\mathbf{F}_\theta = \mathbb{E}_x [(\nabla_\theta \log p_{\theta}) (\nabla_\theta \log p_{\theta})^\top]
$$

其中 $$\mathbf{F}_\theta$$ 称为 **[Fisher 信息矩阵](http://mathworld.wolfram.com/FisherInformationMatrix.html)**，并且由于 $$\mathbb{E}[\nabla_\theta \log p_\theta] = 0$$，它[正是](https://wiseodd.github.io/techblog/2018/03/11/fisher-information/) $$\nabla_\theta \log p_\theta$$ 的协方差矩阵。

以下优化问题：

$$
\max \mathcal{J}(\theta + d) \approx \max \big( \mathcal{J}(\theta) + {\nabla_\theta\mathcal{J}(\theta)}^\top d \big)\;\text{ s.t. }\text{KL}[p_\theta \| p_{\theta+d}] - \epsilon = 0
$$

其解可以借助拉格朗日乘子求得：

$$
\begin{aligned}
\mathcal{L}(\theta, d, \beta) &= \mathcal{J}(\theta) + \nabla_\theta\mathcal{J}(\theta)^\top d - \beta (\frac{1}{2}d^\top \mathbf{F}_\theta d + \epsilon) = 0 \text{ s.t. } \beta > 0 \\
\nabla_d \mathcal{L}(\theta, d, \beta) &= \nabla_\theta\mathcal{J}(\theta) - \beta\mathbf{F}_\theta d = 0 \\
\text{Thus } d_\text{N}^* &= \nabla_\theta^\text{N} \mathcal{J}(\theta) = \mathbf{F}_\theta^{-1} \nabla_\theta\mathcal{J}(\theta) 
\end{aligned}
$$

其中 $$d_\text{N}^*$$ 只提取 $$\theta$$ 上最优移动步的方向，忽略标量 $$\beta^{-1}$$。


![Plain vs natural coordinates](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/CMA-ES-coordinates.png)

*图 4. 右图中的自然梯度样本（黑色实线箭头）是左图中的普通梯度样本（黑色实线箭头）乘以其协方差的逆得到的。这样一来，不确定性高的梯度方向（以与其他样本的高协方差来体现）会受到小权重的惩罚。因此，聚合后的自然梯度（红色虚线箭头）比自然梯度（绿色实线箭头）更值得信赖。（图片来源：在 [NES](https://arxiv.org/abs/1106.4487) 论文图 2 基础上添加标注）*



### NES 算法

一个样本所对应的适应度记为 $$f(x)$$，$$x$$ 上的搜索分布由 $$\theta$$ 参数化。NES 期望通过优化参数 $$\theta$$ 来实现最大的期望适应度：

$$
\mathcal{J}(\theta) = \mathbb{E}_{x\sim p_\theta(x)} [f(x)] = \int_x f(x) p_\theta(x) dx
$$

使用与 [REINFORCE](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/#reinforce) 中相同的对数似然[技巧](http://blog.shakirm.com/2015/11/machine-learning-trick-of-the-day-5-log-derivative-trick/)：

$$
\begin{aligned}
\nabla_\theta\mathcal{J}(\theta) 
&= \nabla_\theta \int_x f(x) p_\theta(x) dx \\
&= \int_x f(x) \frac{p_\theta(x)}{p_\theta(x)}\nabla_\theta p_\theta(x) dx \\
& = \int_x f(x) p_\theta(x) \nabla_\theta \log p_\theta(x) dx \\
& = \mathbb{E}_{x \sim p_\theta} [f(x) \nabla_\theta \log p_\theta(x)]
\end{aligned}
$$      


![NES](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/NES-algorithm.png)



除了自然梯度之外，NES 还采用了一些重要的启发式技巧来使算法表现更加稳健。
- <a name="fitness-shaping"></a>NES 采用**基于排名的适应度整形（rank-based fitness shaping）**，即使用适应度值单调递增下的*排名*，而不是直接使用 $$f(x)$$。也可以使用排名的函数（「效用函数」），它被视为 NES 的一个自由参数。
- NES 采用**自适应采样（adaptation sampling）**来在运行时调整超参数。当改变 $$\theta \to \theta’$$ 时，从 $$p_\theta$$ 中抽取的样本会与从 $$p_{\theta’}$$ 中抽取的样本通过 [Mann-Whitney U-test(https://en.wikipedia.org/wiki/Mann%E2%80%93Whitney_U_test)] 进行比较；如果结果呈现正或负的符号，目标超参数就按一个乘法常数相应减小或增大。注意，样本 $$x’_i \sim p_{\theta’}(x)$$ 的分数会施加重要性采样权重 $$w_i’ = p_\theta(x) / p_{\theta’}(x)$$。





## 应用：深度强化学习中的 ES


### 用于 RL 的 OpenAI ES

在强化学习中使用进化算法的思想可以追溯到[很久以前](https://arxiv.org/abs/1106.0221)，但由于计算能力的限制，当时只局限于表格型 RL（tabular RL）。

受 [NES](#natural-evolution-strategies) 启发，OpenAI 的研究人员（[Salimans, et al. 2017](https://arxiv.org/abs/1703.03864)）提出将 NES 作为一种无梯度的黑盒优化器，来寻找使回报函数 $$F(\theta)$$ 最大化的最优策略参数 $$\theta$$。其关键是在模型参数 $\theta$ 上添加高斯噪声 $\epsilon$，然后利用对数似然技巧将其写成高斯概率密度函数的梯度。最终只剩下噪声项，作为实测性能的加权标量。

设当前参数值为 $$\hat{\theta}$$（加上帽子是为了将该值与随机变量 $$\theta$$ 区分开）。$$\theta$$ 的搜索分布被设计为一个均值为 $$\hat{\theta}$$、协方差矩阵固定为 $$\sigma^2 I$$ 的各向同性多元高斯分布，


$$
\theta \sim \mathcal{N}(\hat{\theta}, \sigma^2 I) \text{ equivalent to } \theta = \hat{\theta} + \sigma\epsilon, \epsilon \sim \mathcal{N}(0, I)
$$

$$\theta$$ 更新的梯度为：

$$
\begin{aligned}
& \nabla_\theta \mathbb{E}_{\theta\sim\mathcal{N}(\hat{\theta}, \sigma^2 I)} F(\theta) \\
&= \nabla_\theta \mathbb{E}_{\epsilon\sim\mathcal{N}(0, I)} F(\hat{\theta} + \sigma\epsilon) \\
&= \nabla_\theta \int_{\epsilon} p(\epsilon) F(\hat{\theta} + \sigma\epsilon) d\epsilon & \scriptstyle{\text{; Gaussian }p(\epsilon)=(2\pi)^{-\frac{n}{2}} \exp(-\frac{1}{2}\epsilon^\top\epsilon)} \\
&= \int_{\epsilon} p(\epsilon) \nabla_\epsilon \log p(\epsilon) \nabla_\theta \epsilon\;F(\hat{\theta} + \sigma\epsilon) d\epsilon & \scriptstyle{\text{; log-likelihood trick}}\\
&= \mathbb{E}_{\epsilon\sim\mathcal{N}(0, I)} [ \nabla_\epsilon \big(-\frac{1}{2}\epsilon^\top\epsilon\big) \nabla_\theta \big(\frac{\theta - \hat{\theta}}{\sigma}\big) F(\hat{\theta} + \sigma\epsilon) ] & \\
&= \mathbb{E}_{\epsilon\sim\mathcal{N}(0, I)} [ (-\epsilon) (\frac{1}{\sigma}) F(\hat{\theta} + \sigma\epsilon) ] & \\
&= \frac{1}{\sigma}\mathbb{E}_{\epsilon\sim\mathcal{N}(0, I)} [ \epsilon F(\hat{\theta} + \sigma\epsilon) ] & \scriptstyle{\text{; negative sign can be absorbed.}}
\end{aligned}
$$

在一代中，我们可以采样多个 $$epsilon_i, i=1,\dots,n$$ 并*并行*评估适应度。一个精妙的设计是：无需共享大型模型参数。工作节点之间只通信随机种子，就足以让主节点完成参数更新。这一方法后来被扩展为自适应地学习损失函数；参见我之前关于 [Evolved Policy Gradient](https://lilianweng.github.io/posts/2019-06-23-meta-rl/#meta-learning-the-loss-function) 的文章。


![ES for RL](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/OpenAI-ES-algorithm.png)

*图 5. 使用进化策略训练 RL 策略的算法。（图片来源：[ES-for-RL](https://arxiv.org/abs/1703.03864) 论文）*

为了让表现更加稳健，OpenAI ES 采用了虚拟批归一化（virtual batch normalization，即固定用于计算统计量的小批量的 BN）、镜像采样（mirror sampling，即采样一对 $$(-\epsilon, \epsilon)$$ 用于评估）以及[适应度整形](#fitness-shaping)。





### 基于 ES 的探索

探索（[与利用](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/#exploitation-vs-exploration)的权衡）是 RL 中的一个重要话题。[上文中](TBA) ES 算法的优化方向仅从累积回报 $$F(\theta)$$ 中提取。若没有显式的探索，智能体可能会陷入局部最优。



新颖性搜索 ES（Novelty-Search ES，**NS-ES**；[Conti et al, 2018](https://arxiv.org/abs/1712.06560)）通过朝着最大化*新颖性*（novelty）分数的方向更新参数来鼓励探索。新颖性分数依赖于一个领域特定的行为表征函数 $$b(\pi_\theta)$$。$$b(\pi_\theta)$$ 的选择与任务相关，看起来有些任意；例如，在论文的 Humanoid 运动任务中，$$b(\pi_\theta)$$ 是智能体的最终 $$(x,y)$$ 位置。
1. 每个策略的 $$b(\pi_\theta)$$ 都会被加入一个存档集合 $$\mathcal{A}$$。
2. 策略 $$\pi_\theta$$ 的新颖性由 $$b(\pi_\theta)$$ 与 $$\mathcal{A}$$ 中所有其他条目之间的 k 近邻分数来度量。
（存档集合的这一用法听起来与[情景记忆](https://lilianweng.github.io/posts/2019-06-23-meta-rl/#episodic-control)颇为相似。）


$$
N(\theta, \mathcal{A}) = \frac{1}{\lambda} \sum_{i=1}^\lambda \| b(\pi_\theta), b^\text{knn}_i \|_2
\text{, where }b^\text{knn}_i \in \text{kNN}(b(\pi_\theta), \mathcal{A})
$$

ES 的优化步骤依赖新颖性分数而非适应度：

$$
\nabla_\theta \mathbb{E}_{\theta\sim\mathcal{N}(\hat{\theta}, \sigma^2 I)} N(\theta, \mathcal{A})
= \frac{1}{\sigma}\mathbb{E}_{\epsilon\sim\mathcal{N}(0, I)} [ \epsilon N(\hat{\theta} + \sigma\epsilon, \mathcal{A}) ]
$$

NS-ES 维护一组 $$M$$ 个独立训练的智能体（「元种群」，meta-population），$$\mathcal{M} = \{\theta_1, \dots, \theta_M \}$$，并按与新颖性分数成正比的方式挑选其中一个来推进。最终我们选出最佳策略。这一过程等价于集成（ensembling）；同样的思想也可见于 [SVPG](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/#svpg)。

$$
\begin{aligned}
m &\leftarrow \text{pick } i=1,\dots,M\text{ according to probability}\frac{N(\theta_i, \mathcal{A})}{\sum_{j=1}^M N(\theta_j, \mathcal{A})} \\
\theta_m^{(t+1)} &\leftarrow \theta_m^{(t)} + \alpha \frac{1}{\sigma}\sum_{i=1}^N \epsilon_i N(\theta^{(t)}_m + \epsilon_i, \mathcal{A}) \text{ where }\epsilon_i \sim \mathcal{N}(0, I)
\end{aligned}
$$

其中 $$N$$ 是高斯扰动噪声向量的数量，$$\alpha$$ 是学习率。

NS-ES 完全抛弃了奖励函数，只对新颖性进行优化，以避免欺骗性局部最优。为了把适应度重新纳入公式，又有两种变体被提出。

**NSR-ES**：

$$
\theta_m^{(t+1)} \leftarrow \theta_m^{(t)} + \alpha \frac{1}{\sigma}\sum_{i=1}^N \epsilon_i \frac{N(\theta^{(t)}_m + \epsilon_i, \mathcal{A}) + F(\theta^{(t)}_m + \epsilon_i)}{2}
$$


**NSRAdapt-ES（NSRA-ES）**：自适应权重参数初始为 $$w = 1.0$$。如果性能在若干代内保持停滞，我们开始减小 $$w$$；而当性能开始提升时，我们停止减小 $$w$$，转而增大它。这样一来，当性能停止增长时偏好适应度，其他情况下则偏好新颖性。

$$
\theta_m^{(t+1)} \leftarrow \theta_m^{(t)} + \alpha \frac{1}{\sigma}\sum_{i=1}^N \epsilon_i \big((1-w) N(\theta^{(t)}_m + \epsilon_i, \mathcal{A}) + w F(\theta^{(t)}_m + \epsilon_i)\big)
$$


![NS-ES Experiments](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/NS-ES-experiments.png)

*图 6.（左）环境为带三面墙的 Humanoid 运动任务，这三面墙充当制造局部最优的欺骗性陷阱。（右）实验比较了 ES 基线与其他鼓励探索的变体。（图片来源：[NS-ES](https://arxiv.org/abs/1712.06560) 论文）*



### CEM-RL

![CEM-RL](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/CEM-RL.png)

*图 7. (a) CEM-RL 与 (b) [ERL](https://papers.nips.cc/paper/7395-evolution-guided-policy-gradient-in-reinforcement-learning.pdf) 两种算法的架构（图片来源：[CEM-RL](https://arxiv.org/abs/1810.01222) 论文）*


CEM-RL 方法（[Pourchot & Sigaud, 2019](https://arxiv.org/abs/1810.01222)）将交叉熵方法（Cross Entropy Method，CEM）与 [DDPG](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/#ddpg) 或 [TD3](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/#td3) 相结合。这里的 CEM 与[上文](#simple-gaussian-evolution-strategies)描述的简单高斯 ES 基本相同，因此同一功能也可以用 CMA-ES 来替代实现。CEM-RL 建立在*进化强化学习*（*Evolutionary Reinforcement Learning*，*ERL*；[Khadka & Tumer, 2018](https://papers.nips.cc/paper/7395-evolution-guided-policy-gradient-in-reinforcement-learning.pdf)）框架之上：标准 EA 算法选择并进化一个 actor 种群，过程中产生的 rollout 经验随后被加入回放缓冲区，用于训练 RL 的 actor 网络和 critic 网络。

工作流程：
- 1) CEM 种群的均值 actor $$\pi_\mu$$ 用一个随机 actor 网络初始化。
- 2) critic 网络 $$Q$$ 也同时初始化，它将由 DDPG/TD3 更新。
- 3) 重复直到满意：
    - a. 采样一个 actor 种群 $$\sim \mathcal{N}(\pi_\mu, \Sigma)$$。
    - b. 评估种群中的一半成员。它们的适应度分数被用作累积奖励 $$R$$ 并加入回放缓冲区。
    - c. 另一半成员与 critic 一起更新。
    - d. 用表现最好的精英样本计算新的 $$\pi_mu$$ 和 $$\Sigma$$。参数更新也可以使用 [CMA-ES](#covariance-matrix-adaptation-evolution-strategies-cma-es)。



## 扩展：深度学习中的 EA

（本节内容并非关于进化策略，但仍是有趣且相关的阅读材料。）


*进化算法*已被应用于许多深度学习问题。POET（[Wang et al, 2019](https://arxiv.org/abs/1901.01753)）是一个基于 EA 的框架，尝试在求解问题的同时生成各种不同的任务。POET 已在我上一篇关于元强化学习的[文章](https://lilianweng.github.io/posts/2019-06-23-meta-rl/#task-generation-by-domain-randomization)中介绍过。进化强化学习（ERL）是另一个例子；见图 7 (b)。

下面我想更详细地介绍两个应用：*基于种群的训练（Population-Based Training，PBT）*和*权重无关神经网络（Weight-Agnostic Neural Networks，WANN）*。


### 超参数调优：PBT

![PBT](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/PBT.png)

*图 8. 不同超参数调优方式的范式对比。（图片来源：[PBT](https://arxiv.org/abs/1711.09846) 论文）*

基于种群的训练（Population-Based Training，[Jaderberg, et al, 2017](https://arxiv.org/abs/1711.09846)），简称 **PBT**，将 EA 应用于超参数调优问题。它联合训练一个模型种群及相应的超参数，以获得最优性能。

PBT 从一组随机候选开始，每个候选包含一对模型权重初始化和超参数，$$\{(\theta_i, h_i)\mid i=1, \dots, N\}$$。每个样本并行训练，并周期性地异步评估自身性能。一旦某个成员被认为就绪（即经过了足够的梯度更新步数，或性能足够好），它就有机会通过与整个种群的比较来得到更新：
- **`exploit()`**：当该模型表现不佳时，其权重可以被替换为表现更好的模型的权重。
- **`explore()`**：如果模型权重被覆盖，`explore` 步骤会用随机噪声扰动超参数。

在这个过程中，只有有前景的模型与超参数对才能存活并继续演化，从而更好地利用计算资源。


![PBT Algorithm](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/PBT-algorithm.png)

*图 9. 基于种群的训练的算法。（图片来源：[PBT](https://arxiv.org/abs/1711.09846) 论文）*


### 网络拓扑优化：WANN

*权重无关神经网络*（Weight Agnostic Neural Networks，简称 **WANN**；[Gaier & Ha 2019](https://arxiv.org/abs/1906.04358)）尝试搜索在不训练网络权重的情况下就能达到最优性能的最小网络拓扑。由于不考虑网络权重的最优配置，WANN 更加侧重架构本身，这使其关注点不同于 [NAS](http://openaccess.thecvf.com/content_cvpr_2018/papers/Zoph_Learning_Transferable_Architectures_CVPR_2018_paper.pdf)（神经架构搜索）。WANN 深受一种经典的网络拓扑进化遗传算法——*NEAT*（"Neuroevolution of Augmenting Topologies"；[Stanley & Miikkulainen 2002](http://nn.cs.utexas.edu/downloads/papers/stanley.gecco02_1.pdf)）——的启发。

WANN 的工作流程与标准 GA 基本相同：
1. 初始化：创建一个由极小网络组成的种群。
2. 评估：用一系列*共享的*权重值进行测试。
3. 排名与选择：按性能和复杂度排名。
4. 变异：通过改变最佳网络来创建新种群。


![Mutation operations in WANN](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/WANN-mutations.png)

*图 10. WANN 中用于搜索新网络拓扑的变异操作（图片来源：[WANN](https://arxiv.org/abs/1906.04358) 论文）*


在「评估」阶段，所有网络权重都被设为相同的值。这样，WANN 实际上是在搜索能用最小描述长度（minimal description length）描述的网络。在「选择」阶段，网络连接和模型性能都会被考虑在内。


![WANN results](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/WANN-results.png)

*图 11. WANN 找到的网络拓扑在不同 RL 任务上的性能，与文献中常用的基线前馈（FF）网络进行比较。"Tuned Shared Weight"（调优的共享权重）只需调节一个权重值。（图片来源：[WANN](https://arxiv.org/abs/1906.04358) 论文）*

如图 11 所示，WANN 的结果分别用随机权重和共享权重（单一权重）进行了评估。有趣的是，即使对所有权重强制共享并只调节这一个参数，WANN 也能发现取得相当不错性能的拓扑结构。


---
引用本文：
```
@article{weng2019ES,
  title   = "Evolution Strategies",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2019",
  url     = "https://lilianweng.github.io/lil-log/2019/09/05/evolution-strategies.html"
}
```

## 参考文献

[1] Nikolaus Hansen. ["The CMA Evolution Strategy: A Tutorial"](https://arxiv.org/abs/1604.00772) arXiv preprint arXiv:1604.00772 (2016).

[2] Marc Toussaint. [Slides: "Introduction to Optimization"](https://ipvs.informatik.uni-stuttgart.de/mlr/marc/teaching/13-Optimization/06-blackBoxOpt.pdf)

[3] David Ha. ["A Visual Guide to Evolution Strategies"](http://blog.otoro.net/2017/10/29/visual-evolution-strategies/) blog.otoro.net. Oct 2017.

[4] Daan Wierstra, et al. ["Natural evolution strategies."](https://arxiv.org/abs/1106.4487) IEEE World Congress on Computational Intelligence, 2008.

[5] Agustinus Kristiadi. ["Natural Gradient Descent"](https://wiseodd.github.io/techblog/2018/03/14/natural-gradient/) Mar 2018.

[6] Razvan Pascanu & Yoshua Bengio. ["Revisiting Natural Gradient for Deep Networks."](https://arxiv.org/abs/1301.3584v7) arXiv preprint arXiv:1301.3584 (2013).

[7] Tim Salimans, et al. ["Evolution strategies as a scalable alternative to reinforcement learning."](https://arxiv.org/abs/1703.03864) arXiv preprint arXiv:1703.03864 (2017).

[8] Edoardo Conti, et al. ["Improving exploration in evolution strategies for deep reinforcement learning via a population of novelty-seeking agents."](https://arxiv.org/abs/1712.06560) NIPS. 2018.

[9] Aloïs Pourchot & Olivier Sigaud. ["CEM-RL: Combining evolutionary and gradient-based methods for policy search."](https://arxiv.org/abs/1810.01222) ICLR 2019.

[10] Shauharda Khadka & Kagan Tumer. ["Evolution-guided policy gradient in reinforcement learning."](https://papers.nips.cc/paper/7395-evolution-guided-policy-gradient-in-reinforcement-learning.pdf) NIPS 2018.

[11] Max Jaderberg, et al. ["Population based training of neural networks."](https://arxiv.org/abs/1711.09846) arXiv preprint arXiv:1711.09846 (2017).

[12] Adam Gaier & David Ha. ["Weight Agnostic Neural Networks."](https://arxiv.org/abs/1906.04358) arXiv preprint arXiv:1906.04358 (2019).
