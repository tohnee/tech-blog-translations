---
title: "基于流的深度生成模型"
title_en: "Flow-based Deep Generative Models"
source: https://lilianweng.github.io/posts/2018-10-13-flow-models/
crawled: 2026-09-08
translated: 2026-09-08
---

# 基于流的深度生成模型

> 原文：[Flow-based Deep Generative Models](https://lilianweng.github.io/posts/2018-10-13-flow-models/) · Lilian Weng（翁荔）

> 在这篇文章中，我们将探讨第三类生成模型：基于流的生成模型（flow-based generative models）。与 GAN 和 VAE 不同，这类模型会显式地学习输入数据的概率密度函数。

到目前为止，我已经写过两类生成模型：[GAN](https://lilianweng.github.io/posts/2017-08-20-gan/) 和 [VAE](https://lilianweng.github.io/posts/2018-08-12-vae/)。它们都没有显式地学习真实数据的概率密度函数 $$p(\mathbf{x})$$（其中 $$\mathbf{x} \in \mathcal{D}$$）——因为这实在是太难了！以带潜变量（latent variable）的生成模型为例，$$p(\mathbf{x}) = \int p(\mathbf{x}\vert\mathbf{z})p(\mathbf{z})d\mathbf{z}$$ 几乎无法计算，因为要遍历潜编码 $$\mathbf{z}$$ 的所有可能取值是不可解析处理（intractable）的。

基于流的深度生成模型借助[归一化流](https://arxiv.org/abs/1505.05770)（normalizing flow）——一种强大的密度估计统计工具——攻克了这个难题。对 $$p(\mathbf{x})$$ 的良好估计使我们能够高效地完成许多下游任务：采样未观测到但真实可信的新数据点（数据生成）、预测未来事件的稀有程度（密度估计）、推断潜变量、补全不完整的数据样本等。

## 生成模型的类型

下面快速总结一下 GAN、VAE 和基于流的生成模型之间的区别：
1. 生成对抗网络（GAN）：GAN 提供了一种聪明的方案，将数据生成这一无监督学习问题当作监督学习问题来建模。判别器模型学习区分真实数据与生成器模型产生的假样本，两个模型在一种[极小极大](https://en.wikipedia.org/wiki/Minimax)博弈中被训练。
2. 变分自编码器（VAE）：VAE 通过最大化证据下界（ELBO）来隐式地优化数据的对数似然。
3. 基于流的生成模型：基于流的生成模型由一系列可逆变换构成。与前两者不同，这类模型显式地学习数据分布 $$p(\mathbf{x})$$，因此损失函数就是负对数似然。

![生成模型的类别](https://lilianweng.github.io/posts/2018-10-13-flow-models/three-generative-models.png)

*图 1. 三类生成模型的对比。*

## 线性代数基础回顾

在深入了解基于流的生成模型之前，我们需要先理解两个关键概念：雅可比行列式（Jacobian determinant）和变量替换法则（change of variable rule）。内容非常基础，读者完全可以跳过。

### 雅可比矩阵与行列式

给定一个将 $$n$$ 维输入向量 $$\mathbf{x}$$ 映射到 $$m$$ 维输出向量的函数 $$\mathbf{f}: \mathbb{R}^n \mapsto \mathbb{R}^m$$，该函数的所有一阶偏导数构成的矩阵称为**雅可比矩阵（Jacobian matrix）** $$\mathbf{J}$$，其第 i 行第 j 列的元素为 $$\mathbf{J}_{ij} = \frac{\partial f_i}{\partial x_j}$$。

$$
\mathbf{J} = \begin{bmatrix}
\frac{\partial f_1}{\partial x_1} & \dots & \frac{\partial f_1}{\partial x_n} \\[6pt]
\vdots & \ddots & \vdots \\[6pt]
\frac{\partial f_m}{\partial x_1} & \dots & \frac{\partial f_m}{\partial x_n} \\[6pt]
\end{bmatrix}
$$

行列式是一个实数，由方阵的所有元素计算而来。注意，行列式*只对**方阵**存在*。行列式的绝对值可以看作是对「用该矩阵做乘法会让空间膨胀或收缩多少」的一种度量。

一个 n×n 矩阵 $$M$$ 的行列式为：

$$
\det M = \det \begin{bmatrix}
a_{11} & a_{12} & \dots & a_{1n} \\
a_{21} & a_{22} & \dots & a_{2n} \\
\vdots & \vdots & & \vdots \\
a_{n1} & a_{n2} & \dots & a_{nn} \\
\end{bmatrix} = \sum_{j_1 j_2 \dots j_n} (-1)^{\tau(j_1 j_2 \dots j_n)} a_{1j_1} a_{2j_2} \dots a_{nj_n}
$$

其中求和符号的下标 $$j_1 j_2 \dots j_n$$ 遍历集合 {1, 2, ..., n} 的所有排列，因此总共有 $$n!$$ 项；$$\tau(.)$$ 表示一个[排列的符号](https://en.wikipedia.org/wiki/Parity_of_a_permutation)（signature）。

方阵 $$M$$ 的行列式可以检验它是否可逆：如果 $$\det(M)=0$$，那么 $$M$$ 不可逆（一个*奇异*（singular）矩阵，其行或列线性相关，或者某一行或某一列全为 0）；否则，如果 $$\det(M)\neq 0$$，$$M$$ 可逆。

乘积的行列式等于行列式的乘积：$$\det(AB) = \det(A)\det(B)$$。（[证明](https://proofwiki.org/wiki/Determinant_of_Matrix_Product)）

### 变量替换定理

我们来专门在概率密度估计的语境下回顾变量替换定理（change of variable theorem），先从单变量的情形开始。

给定随机变量 $$z$$ 及其已知的概率密度函数 $$z \sim \pi(z)$$，我们想用一个一一映射函数 $$x = f(z)$$ 来构造一个新的随机变量。函数 $$f$$ 是可逆的，因此 $$z=f^{-1}(x)$$。现在的问题是*如何推断新变量未知的概率密度函数* $$p(x)$$？

$$
\begin{aligned}
& \int p(x)dx = \int \pi(z)dz = 1 \scriptstyle{\text{   ; Definition of probability distribution.}}\\
& p(x) = \pi(z) \left\vert\frac{dz}{dx}\right\vert = \pi(f^{-1}(x)) \left\vert\frac{d f^{-1}}{dx}\right\vert = \pi(f^{-1}(x)) \vert (f^{-1})'(x) \vert
\end{aligned}
$$

根据定义，积分 $$\int \pi(z)dz$$ 是无穷多个宽度为无穷小 $$\Delta z$$ 的矩形面积之和。这样一个矩形在位置 $$z$$ 处的高度就是密度函数 $$\pi(z)$$ 的值。当我们替换变量时，$$z = f^{-1}(x)$$ 给出 $$\frac{\Delta z}{\Delta x} = (f^{-1}(x))'$$ 以及 $$\Delta z =  (f^{-1}(x))' \Delta x$$。这里 $$\vert(f^{-1}(x))'\vert$$ 表示分别以变量 $$z$$ 和变量 $$x$$ 为坐标所定义的矩形面积之间的比率。

多变量版本的形式类似：

$$
\begin{aligned}
\mathbf{z} &\sim \pi(\mathbf{z}), \mathbf{x} = f(\mathbf{z}), \mathbf{z} = f^{-1}(\mathbf{x}) \\
p(\mathbf{x}) 
&= \pi(\mathbf{z}) \left\vert \det \dfrac{d \mathbf{z}}{d \mathbf{x}} \right\vert  
= \pi(f^{-1}(\mathbf{x})) \left\vert \det \dfrac{d f^{-1}}{d \mathbf{x}} \right\vert
\end{aligned}
$$

其中 $$\det \frac{\partial f}{\partial\mathbf{z}}$$ 是函数 $$f$$ 的雅可比行列式。多变量版本的完整证明不在本文范围之内；感兴趣的读者可以去问问 Google ;)

## 什么是归一化流？

有能力做出良好的密度估计，在许多机器学习问题中都有直接的用途，但这非常困难。例如，由于我们需要在深度学习模型中运行反向传播，模型中嵌入的概率分布（即后验 $$p(\mathbf{z}\vert\mathbf{x})$$）应当足够简单，以便轻松、高效地求导。这正是潜变量生成模型经常使用高斯分布的原因，尽管大多数现实世界的分布远比高斯分布复杂。

**归一化流（Normalizing Flow，NF）**模型应运而生，带来了更好、更强大的分布逼近能力。归一化流通过应用一系列可逆的变换函数，将一个简单分布变换成复杂分布。在沿着一条变换链「流动」的过程中，我们依据变量替换定理反复地用新变量替换旧变量，最终得到最终目标变量的概率分布。

![归一化流](https://lilianweng.github.io/posts/2018-10-13-flow-models/normalizing-flow.png)

*图 2. 归一化流模型示意图：将简单分布 $$p_0(\mathbf{z}_0)$$ 一步步变换为复杂分布 $$p_K(\mathbf{z}_K)$$。*

如图 2 所定义，

$$
\begin{aligned}
\mathbf{z}_{i-1} &\sim p_{i-1}(\mathbf{z}_{i-1}) \\
\mathbf{z}_i &= f_i(\mathbf{z}_{i-1})\text{, thus }\mathbf{z}_{i-1} = f_i^{-1}(\mathbf{z}_i) \\
p_i(\mathbf{z}_i) 
&= p_{i-1}(f_i^{-1}(\mathbf{z}_i)) \left\vert \det\dfrac{d f_i^{-1}}{d \mathbf{z}_i} \right\vert
\end{aligned}
$$

接下来让我们把方程转换成 $$\mathbf{z}_i$$ 的函数，这样就能用基础分布进行推断。

$$
\begin{aligned}
p_i(\mathbf{z}_i) 
&= p_{i-1}(f_i^{-1}(\mathbf{z}_i)) \left\vert \det\dfrac{d f_i^{-1}}{d \mathbf{z}_i} \right\vert \\
&= p_{i-1}(\mathbf{z}_{i-1}) \left\vert \det \color{red}{\Big(\dfrac{d f_i}{d\mathbf{z}_{i-1}}\Big)^{-1}} \right\vert & \scriptstyle{\text{; According to the inverse func theorem.}} \\
&= p_{i-1}(\mathbf{z}_{i-1}) \color{red}{\left\vert \det \dfrac{d f_i}{d\mathbf{z}_{i-1}} \right\vert^{-1}} & \scriptstyle{\text{; According to a property of Jacobians of invertible func.}} \\
\log p_i(\mathbf{z}_i) &= \log p_{i-1}(\mathbf{z}_{i-1}) - \log \left\vert \det \dfrac{d f_i}{d\mathbf{z}_{i-1}} \right\vert
\end{aligned}
$$

(\*) 关于*「反函数定理」*（inverse function theorem）的一点说明：如果 $$y=f(x)$$ 且 $$x=f^{-1}(y)$$，我们有：

$$
\dfrac{df^{-1}(y)}{dy} = \dfrac{dx}{dy} = (\dfrac{dy}{dx})^{-1} = (\dfrac{df(x)}{dx})^{-1}
$$

(\*) 关于*「可逆函数的雅可比矩阵」*的一点说明：可逆矩阵的逆矩阵的行列式等于行列式的逆：$$\det(M^{-1}) = (\det(M))^{-1}$$，[因为](#jacobian-matrix-and-determinant) $$\det(M)\det(M^{-1}) = \det(M \cdot M^{-1}) = \det(I) = 1$$。

给定这样一条概率密度函数链，我们知道了每一对相邻变量之间的关系。我们可以把输出 $$\mathbf{x}$$ 的方程一步步展开，直到回溯到初始分布 $$\mathbf{z}_0$$。

$$
\begin{aligned}
\mathbf{x} = \mathbf{z}_K &= f_K \circ f_{K-1} \circ \dots \circ f_1 (\mathbf{z}_0) \\
\log p(\mathbf{x}) = \log \pi_K(\mathbf{z}_K) 
&= \log \pi_{K-1}(\mathbf{z}_{K-1}) - \log\left\vert\det\dfrac{d f_K}{d \mathbf{z}_{K-1}}\right\vert \\
&= \log \pi_{K-2}(\mathbf{z}_{K-2}) - \log\left\vert\det\dfrac{d f_{K-1}}{d\mathbf{z}_{K-2}}\right\vert - \log\left\vert\det\dfrac{d f_K}{d\mathbf{z}_{K-1}}\right\vert \\
&= \dots \\
&= \log \pi_0(\mathbf{z}_0) - \sum_{i=1}^K \log\left\vert\det\dfrac{d f_i}{d\mathbf{z}_{i-1}}\right\vert
\end{aligned}
$$

随机变量 $$\mathbf{z}_i = f_i(\mathbf{z}_{i-1})$$ 所经由的路径就是**流（flow）**，而由一系列相继的分布 $$\pi_i$$ 构成的完整链条被称为**归一化流（normalizing flow）**。按照方程中计算的要求，变换函数 $$f_i$$ 应当满足两个性质：
1. 它易于求逆。
2. 它的雅可比行列式易于计算。

## 使用归一化流的模型

有了归一化流这件工具，输入数据的精确对数似然 $$\log p(\mathbf{x})$$ 就变得可解析处理（tractable）了。因此，基于流的生成模型的训练准则就是训练数据集 $$\mathcal{D}$$ 上的负对数似然（NLL）：

$$
\mathcal{L}(\mathcal{D}) = - \frac{1}{\vert\mathcal{D}\vert}\sum_{\mathbf{x} \in \mathcal{D}} \log p(\mathbf{x})
$$

### RealNVP

**RealNVP**（Real-valued Non-Volume Preserving，实值非体积保持；[Dinh et al., 2017](https://arxiv.org/abs/1605.08803)）模型通过堆叠一系列可逆的双射变换函数来实现归一化流。在每一个双射 $$f: \mathbf{x} \mapsto \mathbf{y}$$（被称为*仿射耦合层（affine coupling layer）*）中，输入的维度被拆分成两部分：
- 前 $$d$$ 维保持不变；
- 第二部分，即第 $$d+1$$ 到第 $$D$$ 维，经历一个仿射变换（「缩放加平移」），且缩放参数和平移参数都是前 $$d$$ 维的函数。

$$
\begin{aligned}
\mathbf{y}_{1:d} &= \mathbf{x}_{1:d} \\ 
\mathbf{y}_{d+1:D} &= \mathbf{x}_{d+1:D} \odot \exp({s(\mathbf{x}_{1:d})}) + t(\mathbf{x}_{1:d})
\end{aligned}
$$

其中 $$s(.)$$ 和 $$t(.)$$ 分别是*缩放（scale）*函数和*平移（translation）*函数，二者都完成 $$\mathbb{R}^d \mapsto \mathbb{R}^{D-d}$$ 的映射。$$\odot$$ 运算是逐元素乘积。

现在让我们检验这个变换是否满足流变换的两个基本性质。

**条件 1**：「它易于求逆。」

是的，而且相当直接。

$$
\begin{cases}
\mathbf{y}_{1:d} &= \mathbf{x}_{1:d} \\ 
\mathbf{y}_{d+1:D} &= \mathbf{x}_{d+1:D} \odot \exp({s(\mathbf{x}_{1:d})}) + t(\mathbf{x}_{1:d})
\end{cases}
\Leftrightarrow 
\begin{cases}
\mathbf{x}_{1:d} &= \mathbf{y}_{1:d} \\ 
\mathbf{x}_{d+1:D} &= (\mathbf{y}_{d+1:D} - t(\mathbf{y}_{1:d})) \odot \exp(-s(\mathbf{y}_{1:d}))
\end{cases}
$$

**条件 2**：「它的雅可比行列式易于计算。」

是的。这个变换的雅可比矩阵和行列式都不难求出。该雅可比矩阵是一个下三角矩阵。

$$
\mathbf{J} = 
\begin{bmatrix}
  \mathbb{I}_d & \mathbf{0}_{d\times(D-d)} \\[5pt]
  \frac{\partial \mathbf{y}_{d+1:D}}{\partial \mathbf{x}_{1:d}} & \text{diag}(\exp(s(\mathbf{x}_{1:d})))
\end{bmatrix}
$$

因此行列式简单地就是对角线上元素的乘积。

$$
\det(\mathbf{J}) 
= \prod_{j=1}^{D-d}\exp(s(\mathbf{x}_{1:d}))_j
= \exp(\sum_{j=1}^{D-d} s(\mathbf{x}_{1:d})_j)
$$

到目前为止，仿射耦合层看起来完美适合用来构造归一化流 :)

更妙的是，由于 (i) 计算 $$f^-1$$ 不需要计算 $$s$$ 或 $$t$$ 的逆，并且 (ii) 计算雅可比行列式也不涉及计算 $$s$$ 或 $$t$$ 的雅可比矩阵，这些函数可以*任意复杂*；也就是说，$$s$$ 和 $$t$$ 都可以用深度神经网络来建模。

在单个仿射耦合层中，总有一些维度（通道）保持不变。为了确保所有输入都有机会被改动，模型在每一层都反转维度的排序，使得每次保持不变的成分各不相同。遵循这样的交替模式，在一个变换层中保持不变的那组单元总会在下一层被修改。人们发现，批归一化（batch normalization）有助于训练耦合层堆叠非常深的模型。

此外，RealNVP 还可以采用多尺度架构（multi-scale architecture），为大型输入构建更高效的模型。多尺度架构在普通的仿射层上应用了若干种「采样」操作，包括空间棋盘格模式掩码、挤压操作（squeezing operation）以及通道维掩码。关于多尺度架构的更多细节，请阅读[论文](https://arxiv.org/abs/1605.08803)。

### NICE

**NICE**（Non-linear Independent Component Estimation，非线性独立分量估计；[Dinh, et al. 2015](https://arxiv.org/abs/1410.8516)）模型是 [RealNVP](#realnvp) 的前身。NICE 中的变换就是去掉缩放项的仿射耦合层，被称为*加性耦合层（additive coupling layer）*。

$$
\begin{cases}
\mathbf{y}_{1:d} &= \mathbf{x}_{1:d} \\ 
\mathbf{y}_{d+1:D} &= \mathbf{x}_{d+1:D} + m(\mathbf{x}_{1:d})
\end{cases}
\Leftrightarrow 
\begin{cases}
\mathbf{x}_{1:d} &= \mathbf{y}_{1:d} \\ 
\mathbf{x}_{d+1:D} &= \mathbf{y}_{d+1:D} - m(\mathbf{y}_{1:d})
\end{cases}
$$

### Glow

**Glow**（[Kingma and Dhariwal, 2018](https://arxiv.org/abs/1807.03039)）模型扩展了先前的可逆生成模型 NICE 和 RealNVP，并用可逆的 1x1 卷积取代通道排序上的反转置换操作，从而简化了架构。

![Glow 的一步](https://lilianweng.github.io/posts/2018-10-13-flow-models/one-glow-step.png)

*图 3. Glow 模型中的一步流。（图片来源：[Kingma and Dhariwal, 2018](https://arxiv.org/abs/1807.03039)）*

Glow 中的一步流包含三个子步骤。

子步骤 1：**激活归一化（Activation normalization）**（简称「actnorm」）

它使用逐通道的缩放参数和偏置参数执行仿射变换，类似于批归一化，但适用于大小为 1 的 mini-batch。这些参数是可训练的，但其初始化方式使得经过 actnorm 处理后的第一个 mini-batch 数据均值为 0、标准差为 1。

子步骤 2：**可逆 1x1 卷积（Invertible 1x1 conv）**

在 RealNVP 流的各层之间，通道的排序会被反转，从而使所有数据维度都有机会被改动。而输入和输出通道数相等的 1×1 卷积是通道排序*任意置换的一种推广*。

比方说，我们对一个 $$h \times w \times c$$ 的输入张量 $$\mathbf{h}$$ 做可逆 1x1 卷积，权重矩阵 $$\mathbf{W}$$ 的大小为 $$c \times c$$。输出是一个 $$h \times w \times c$$ 的张量，记为 $$f = \texttt{conv2d}(\mathbf{h}; \mathbf{W})$$。为了应用变量替换法则，我们需要计算雅可比行列式 $$\vert \det\partial f / \partial\mathbf{h}\vert$$。

这里 1x1 卷积的输入和输出都可以看作大小为 $$h \times w$$ 的矩阵。$$\mathbf{h}$$ 中的每个元素 $$\mathbf{x}_{ij}$$（$$i=1,\dots,h, j=1,\dots,w$$）都是一个 $$c$$ 通道的向量，每个元素分别乘以权重矩阵 $$\mathbf{W}$$，得到输出矩阵中对应的元素 $$\mathbf{y}_{ij}$$。每个元素的导数是 $$\partial \mathbf{x}_{ij} \mathbf{W} / \partial\mathbf{x}_{ij} = \mathbf{W}$$，这样的元素总共有 $$h \times w$$ 个：

$$
\log \left\vert\det \frac{\partial\texttt{conv2d}(\mathbf{h}; \mathbf{W})}{\partial\mathbf{h}}\right\vert
= \log (\vert\det\mathbf{W}\vert^{h \cdot w}\vert) = h \cdot w \cdot \log \vert\det\mathbf{W}\vert
$$

可逆 1x1 卷积的求逆依赖于逆矩阵 $$\mathbf{W}^{-1}$$。由于权重矩阵相对较小，矩阵行列式（[tf.linalg.det](https://www.tensorflow.org/api_docs/python/tf/linalg/det)）和矩阵求逆（[tf.linalg.inv](https://www.tensorflow.org/api_docs/python/tf/linalg/inv)）的计算量仍然处于可控范围。

子步骤 3：**仿射耦合层（Affine coupling layer）**

其设计与 RealNVP 中的相同。

![Glow 的三个子步骤](https://lilianweng.github.io/posts/2018-10-13-flow-models/glow-table.png)

*图 4. Glow 中一步流的三个子步骤。（图片来源：[Kingma and Dhariwal, 2018](https://arxiv.org/abs/1807.03039)）*

## 使用自回归流的模型

**自回归（autoregressive）**约束是对序列数据 $$\mathbf{x} = [x_1, \dots, x_D]$$ 建模的一种方式：每个输出只依赖于过去观测到的数据，而不依赖于未来的数据。换句话说，观测到 $$x_i$$ 的概率以 $$x_1, \dots, x_{i-1}$$ 为条件，这些条件概率的乘积给出了观测到完整序列的概率：

$$
p(\mathbf{x}) = \prod_{i=1}^{D} p(x_i\vert x_1, \dots, x_{i-1}) = \prod_{i=1}^{D} p(x_i\vert x_{1:i-1})
$$

如何对条件密度建模由你自己选择。它可以是一个一元高斯分布，其均值和标准差由 $$x_{1:i-1}$$ 的函数计算得到；也可以是一个以 $$x_{1:i-1}$$ 为输入的多层神经网络。

如果把归一化流中的一个流变换构建成一个自回归模型——即向量变量中的每个维度都以它之前的维度为条件——这就是一个**自回归流（autoregressive flow）**。

本节先介绍几个经典的自回归模型（MADE、PixelRNN、WaveNet），然后深入探讨自回归流模型（MAF 与 IAF）。

### MADE

**MADE**（Masked Autoencoder for Distribution Estimation，用于分布估计的掩码自编码器；[Germain et al., 2015](https://arxiv.org/abs/1502.03509)）是一种经过特殊设计的架构，用于*高效地*在自编码器中强制实现自回归属性。当使用自编码器来预测条件概率时，MADE 不需要把具有不同观测窗口的输入重复喂给自编码器 $$D$$ 次，而是通过乘上二值掩码矩阵来移除某些隐藏单元的贡献，从而在*单次前向传播*中、按*给定的*顺序，让每个输入维度只从它之前的维度重构而来。

比方说，在一个多层全连接神经网络中，我们有 $$L$$ 个隐藏层，权重矩阵为 $$\mathbf{W}^1, \dots, \mathbf{W}^L$$，以及一个权重矩阵为 $$\mathbf{V}$$ 的输出层。输出 $$\hat{\mathbf{x}}$$ 的每一维为 $$\hat{x}_i = p(x_i\vert x_{1:i-1})$$。

在没有任何掩码的情况下，逐层计算的形式如下：

$$
\begin{aligned}
\mathbf{h}^0 &= \mathbf{x} \\
\mathbf{h}^l &= \text{activation}^l(\mathbf{W}^l\mathbf{h}^{l-1} + \mathbf{b}^l) \\
\hat{\mathbf{x}} &= \sigma(\mathbf{V}\mathbf{h}^L + \mathbf{c})
\end{aligned}
$$

![MADE](https://lilianweng.github.io/posts/2018-10-13-flow-models/MADE.png)

*图 5. MADE 在一个三层前馈神经网络中工作方式的演示。（图片来源：[Germain et al., 2015](https://arxiv.org/abs/1502.03509)）*

为了把层间的一些连接置零，我们只需将每个权重矩阵与一个二值掩码矩阵逐元素相乘。每个隐藏节点都被赋予一个介于 $$1$$ 和 $$D-1$$ 之间的随机「连接整数（connectivity integer）」；第 $$l$$ 层中第 $$k$$ 个单元被赋予的值记为 $$m^l_k$$。二值掩码矩阵由两层中两个节点的取值逐元素比较确定。

$$
\begin{aligned}
\mathbf{h}^l &= \text{activation}^l((\mathbf{W}^l \color{red}{\odot \mathbf{M}^{\mathbf{W}^l}}) \mathbf{h}^{l-1} + \mathbf{b}^l) \\
\hat{\mathbf{x}} &= \sigma((\mathbf{V} \color{red}{\odot \mathbf{M}^{\mathbf{V}}}) \mathbf{h}^L + \mathbf{c}) \\
M^{\mathbf{W}^l}_{k', k} 
&= \mathbf{1}_{m^l_{k'} \geq m^{l-1}_k} 
= \begin{cases}
    1, & \text{if } m^l_{k'} \geq m^{l-1}_k\\
    0, & \text{otherwise}
\end{cases} \\
M^{\mathbf{V}}_{d, k} 
&= \mathbf{1}_{d \geq m^L_k} 
= \begin{cases}
    1, & \text{if } d > m^L_k\\
    0, & \text{otherwise}
\end{cases}
\end{aligned}
$$

当前层中的一个单元只能连接到上一层中编号小于或等于它的单元，而这种类型的依赖很容易在网络中逐层传播，直到输出层。一旦所有单元和所有层都被赋予了编号，输入维度的顺序就固定了下来，条件概率也据此产生。图 5 给出了精彩的图示。为了确保所有隐藏单元都通过某些路径与输入层和输出层相连，$$m^l_k$$ 的采样值会大于或等于上一层最小的连接整数 $$\min_{k'} m_{k'}^{l-1}$$。

MADE 的训练还可以通过以下方式进一步改善：
- *顺序无关训练（Order-agnostic training）*：打乱输入维度的顺序，使 MADE 能够建模任意排序；还可以在运行时据此创建一个自回归模型集成。
- *连接无关训练（Connectivity-agnostic training）*：为了避免模型被束缚在特定的连接模式约束上，每个训练 minibatch 都重新采样 $$m^l_k$$。

### PixelRNN

PixelRNN（[Oord et al, 2016](https://arxiv.org/abs/1601.06759)）是一种面向图像的深度生成模型。图像的生成一次只进行一个像素，每个新像素都以之前已经看过的像素为条件采样得到。

考虑一幅大小为 $$n \times n$$ 的图像 $$\mathbf{x} = \{x_1, \dots, x_{n^2}\}$$，模型从左上角开始生成像素，从左到右、从上到下依次进行（见图 6）。

![PixelRNN 中的上下文](https://lilianweng.github.io/posts/2018-10-13-flow-models/pixel-rnn-context.png)

*图 6. PixelRNN 中生成一个像素所依赖的上下文。（图片来源：[Oord et al, 2016](https://arxiv.org/abs/1601.06759)）*

每个像素 $$x_i$$ 都从以过去上下文为条件的概率分布中采样得到：即它上方的像素，以及同一行中它左侧的像素。这样的上下文定义看起来相当任意，因为视觉[注意力](https://lilianweng.github.io/posts/2018-06-24-attention/)关注一幅图像的方式要灵活得多。但不知为何，带有如此强假设的生成模型神奇地有效。

一种能够捕获完整上下文的实现是*对角 BiLSTM（Diagonal BiLSTM）*。首先应用**偏斜（skewing）**操作，把输入特征图的每一行相对于上一行偏移一个位置，从而使每一行的计算可以并行化。然后，依据当前像素和左侧的像素来计算 LSTM 状态。

![对角 BiLSTM](https://lilianweng.github.io/posts/2018-10-13-flow-models/diagonal-biLSTM.png)

*图 7. (a) 采用对角 BiLSTM 的 PixelRNN。(b) 偏斜操作，把特征图中的每一行相对于上一行偏移一位。（图片来源：[Oord et al, 2016](https://arxiv.org/abs/1601.06759)）*

$$
\begin{aligned}
\lbrack \mathbf{o}_i, \mathbf{f}_i, \mathbf{i}_i, \mathbf{g}_i \rbrack &= \sigma(\mathbf{K}^{ss} \circledast \mathbf{h}_{i-1} + \mathbf{K}^{is} \circledast \mathbf{x}_i) & \scriptstyle{\text{; }\sigma\scriptstyle{\text{ is tanh for g, but otherwise sigmoid; }}\circledast\scriptstyle{\text{ is convolution operation.}}} \\
\mathbf{c}_i &= \mathbf{f}_i \odot \mathbf{c}_{i-1} + \mathbf{i}_i \odot \mathbf{g}_i & \scriptstyle{\text{; }}\odot\scriptstyle{\text{ is elementwise product.}}\\
\mathbf{h}_i &= \mathbf{o}_i \odot \tanh(\mathbf{c}_i)
\end{aligned}
$$

其中 $$\circledast$$ 表示卷积运算，$$\odot$$ 是逐元素乘法。输入到状态的部分 $$\mathbf{K}^{is}$$ 是一个 1x1 卷积，而状态到状态的循环部分则通过一个核大小为 2x1 的按列卷积 $$\mathbf{K}^{ss}$$ 来计算。

对角 BiLSTM 层能够处理无界的上下文区域，但由于状态之间的顺序依赖，计算代价很高。一种更快的实现使用多个不带池化的卷积层来定义一个有界的上下文框。卷积核经过掩码处理，从而看不到未来的上下文，这与 [MADE](#MADE) 类似。这一卷积版本被称为 **PixelCNN**。

![PixelCNN](https://lilianweng.github.io/posts/2018-10-13-flow-models/pixel-cnn.png)

*图 8. PixelCNN 的掩码卷积是在应用卷积核之前，由掩码张量与卷积核做逐元素乘积构造出来的。（图片来源：http://slazebni.cs.illinois.edu/spring17/lec13_advanced.pdf）*

### WaveNet

**WaveNet**（[Van Den Oord, et al. 2016](https://arxiv.org/abs/1609.03499)）与 PixelCNN 非常相似，但应用于一维音频信号。WaveNet 由一堆*因果卷积（causal convolution）*构成，这种卷积操作的设计尊重顺序：某个时间戳处的预测只能使用过去观测到的数据，而不依赖未来。在 PixelCNN 中，因果卷积通过掩码卷积核来实现；而 WaveNet 中的因果卷积只是把输出向未来方向平移若干个时间戳，使输出与最后一个输入元素对齐。

卷积层的一大缺点是感受野非常有限。输出很难依赖于几百乃至几千个时间步之前的输入，而这对于长序列建模来说可能是至关重要的要求。因此，WaveNet 采用了*空洞卷积（dilated convolution）*（[动画演示](https://github.com/vdumoulin/conv_arithmetic#dilated-convolution-animations)），其卷积核作用于输入的一个大得多的感受野中均匀分布的样本子集。

![WaveNet](https://lilianweng.github.io/posts/2018-10-13-flow-models/wavenet.png)

*图 9. WaveNet 模型的可视化，分别展示了（上）因果卷积层的堆叠和（下）空洞卷积层的堆叠。（图片来源：[Van Den Oord, et al. 2016](https://arxiv.org/abs/1609.03499)）*

WaveNet 使用门控激活单元（gated activation unit）作为非线性层，因为人们发现它在一维音频数据建模上显著优于 ReLU。残差连接施加在门控激活之后。

$$
\mathbf{z} = \tanh(\mathbf{W}_{f,k}\circledast\mathbf{x})\odot\sigma(\mathbf{W}_{g,k}\circledast\mathbf{x})
$$

其中 $$\mathbf{W}_{f,k}$$ 和 $$\mathbf{W}_{g,k}$$ 分别是第 $$k$$ 层的卷积滤波器和门权重矩阵；二者都是可学习的。

### 掩码自回归流（MAF）

**掩码自回归流**（**MAF**；[Papamakarios et al., 2017](https://arxiv.org/abs/1705.07057)）是一类归一化流，其变换层被构建为一个自回归神经网络。MAF 与稍后介绍的**逆自回归流（Inverse Autoregressive Flow，IAF）**非常相似。关于 MAF 与 IAF 之间关系的更多讨论见下一节。

给定两个随机变量 $$\mathbf{z} \sim \pi(\mathbf{z})$$ 和 $$\mathbf{x} \sim p(\mathbf{x})$$，且概率密度函数 $$\pi(\mathbf{z})$$ 已知，MAF 的目标是学习 $$p(\mathbf{x})$$。MAF 在生成每个 $$x_i$$ 时，以之前的维度 $$\mathbf{x}_{1:i-1}$$ 为条件。

确切地说，条件概率是 $$\mathbf{z}$$ 的一个仿射变换，其中缩放项和平移项都是 $$\mathbf{x}$$ 已观测部分的函数。
- 数据生成，产生新的 $$\mathbf{x}$$：

$$x_i \sim p(x_i\vert\mathbf{x}_{1:i-1}) = z_i \odot \sigma_i(\mathbf{x}_{1:i-1}) + \mu_i(\mathbf{x}_{1:i-1})\text{, where }\mathbf{z} \sim \pi(\mathbf{z})$$

- 密度估计，给定已知的 $$\mathbf{x}$$：

$$p(\mathbf{x}) = \prod_{i=1}^D p(x_i\vert\mathbf{x}_{1:i-1})$$

生成过程是顺序进行的，因此天生就慢。而密度估计只需使用 [MADE](#MADE) 之类的架构单次通过网络。变换函数的求逆非常简单，雅可比行列式也很容易计算。

### 逆自回归流（IAF）
与 MAF 类似，**逆自回归流**（**IAF**；[Kingma et al., 2016](https://arxiv.org/abs/1606.04934)）同样将目标变量的条件概率建模为一个自回归模型，但流的方向相反，从而实现了高效得多的采样过程。

首先，我们把 MAF 中的仿射变换反过来：

$$
z_i = \frac{x_i - \mu_i(\mathbf{x}_{1:i-1})}{\sigma_i(\mathbf{x}_{1:i-1})} = -\frac{\mu_i(\mathbf{x}_{1:i-1})}{\sigma_i(\mathbf{x}_{1:i-1})} + x_i \odot \frac{1}{\sigma_i(\mathbf{x}_{1:i-1})}
$$

如果令：

$$
\begin{aligned}
& \tilde{\mathbf{x}} = \mathbf{z}\text{, }\tilde{p}(.) = \pi(.)\text{, }\tilde{\mathbf{x}} \sim \tilde{p}(\tilde{\mathbf{x}}) \\
& \tilde{\mathbf{z}} = \mathbf{x} \text{, }\tilde{\pi}(.) = p(.)\text{, }\tilde{\mathbf{z}} \sim \tilde{\pi}(\tilde{\mathbf{z}})\\
& \tilde{\mu}_i(\tilde{\mathbf{z}}_{1:i-1}) = \tilde{\mu}_i(\mathbf{x}_{1:i-1}) = -\frac{\mu_i(\mathbf{x}_{1:i-1})}{\sigma_i(\mathbf{x}_{1:i-1})} \\
& \tilde{\sigma}(\tilde{\mathbf{z}}_{1:i-1}) = \tilde{\sigma}(\mathbf{x}_{1:i-1}) = \frac{1}{\sigma_i(\mathbf{x}_{1:i-1})}
\end{aligned}
$$

那么我们就有，

$$
\tilde{x}_i \sim p(\tilde{x}_i\vert\tilde{\mathbf{z}}_{1:i}) = \tilde{z}_i \odot \tilde{\sigma}_i(\tilde{\mathbf{z}}_{1:i-1}) + \tilde{\mu}_i(\tilde{\mathbf{z}}_{1:i-1})
\text{, where }\tilde{\mathbf{z}} \sim \tilde{\pi}(\tilde{\mathbf{z}})
$$

IAF 的意图是在 $$\tilde{\pi}(\tilde{\mathbf{z}})$$ 已知的情况下估计 $$\tilde{\mathbf{x}}$$ 的概率密度函数。这个反向的流同样是一个自回归的仿射变换，与 MAF 中的一样，只不过缩放项和平移项是来自已知分布 $$\tilde{\pi}(\tilde{\mathbf{z}})$$ 的已观测变量的自回归函数。MAF 与 IAF 的对比见图 10。

![MAF 与 IAF](https://lilianweng.github.io/posts/2018-10-13-flow-models/MAF-vs-IAF.png)

*图 10. MAF 与 IAF 的对比。密度已知的变量用绿色表示，未知的变量用红色表示。*

各个元素 $$\tilde{x}_i$$ 的计算互不依赖，因此很容易并行化（使用 MADE 只需单次前向）。而对已知的 $$\tilde{\mathbf{x}}$$ 进行密度估计则效率不高，因为我们必须按顺序恢复 $$\tilde{z}_i$$ 的值，$$\tilde{z}_i = (\tilde{x}_i - \tilde{\mu}_i(\tilde{\mathbf{z}}_{1:i-1})) / \tilde{\sigma}_i(\tilde{\mathbf{z}}_{1:i-1})$$，因此总共要 D 次。

| | 基础分布 | 目标分布 | 模型 | 数据生成 | 密度估计 |
| ---------- | ---------- | ---------- | ---------- |---------- | ---------- |
| MAF | $$\mathbf{z}\sim\pi(\mathbf{z})$$ | $$\mathbf{x}\sim p(\mathbf{x})$$ | $$x_i = z_i \odot \sigma_i(\mathbf{x}_{1:i-1}) + \mu_i(\mathbf{x}_{1:i-1})$$ | 顺序进行；慢 | 单次前向；快 |
| IAF | $$\tilde{\mathbf{z}}\sim\tilde{\pi}(\tilde{\mathbf{z}})$$ | $$\tilde{\mathbf{x}}\sim\tilde{p}(\tilde{\mathbf{x}})$$ | $$\tilde{x}_i  = \tilde{z}_i \odot \tilde{\sigma}_i(\tilde{\mathbf{z}}_{1:i-1}) + \tilde{\mu}_i(\tilde{\mathbf{z}}_{1:i-1})$$ | 单次前向；快 | 顺序进行；慢 |
| ---------- | ---------- | ---------- | ---------- |---------- | ---------- |

## VAE + 流

在[变分自编码器](https://lilianweng.github.io/posts/2018-08-12-vae/#vae-variational-autoencoder)中，如果我们想把后验 $$p(\mathbf{z}\vert\mathbf{x})$$ 建模成一个比简单高斯分布更复杂的分布，直觉上，我们可以使用归一化流来变换基础高斯分布，以获得更好的密度逼近。这样一来，编码器将预测一组缩放项和平移项 $$(\mu_i, \sigma_i)$$，它们都是输入 $$\mathbf{x}$$ 的函数。感兴趣的读者可以阅读[论文](https://arxiv.org/abs/1809.05861)了解更多细节。

---

*如果您注意到本文中的错误，请随时联系我 [lilian dot wengweng at gmail dot com]，我会非常乐意立即修正！*

我们下一篇博文见 :D

---

引用格式：
```
@article{weng2018flow,
  title   = "Flow-based Deep Generative Models",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2018",
  url     = "http://lilianweng.github.io/lil-log/2018/10/13/flow-based-deep-generative-models.html"
}
```


## 参考文献

[1] Danilo Jimenez Rezende, and Shakir Mohamed. ["Variational inference with normalizing flows."](https://arxiv.org/abs/1505.05770) ICML 2015.

[2] [Normalizing Flows Tutorial, Part 1: Distributions and Determinants](https://blog.evjang.com/2018/01/nf1.html) by Eric Jang.

[3] [Normalizing Flows Tutorial, Part 2: Modern Normalizing Flows](https://blog.evjang.com/2018/01/nf2.html) by Eric Jang.

[4] [Normalizing Flows](http://akosiorek.github.io/ml/2018/04/03/norm_flows.html) by Adam Kosiorek.

[5] Laurent Dinh, Jascha Sohl-Dickstein, and Samy Bengio. ["Density estimation using Real NVP."](https://arxiv.org/abs/1605.08803) ICLR 2017.

[6] Laurent Dinh, David Krueger, and Yoshua Bengio. ["NICE: Non-linear independent components estimation."](https://arxiv.org/abs/1410.8516) ICLR 2015 Workshop track.

[7] Diederik P. Kingma, and Prafulla Dhariwal. ["Glow: Generative flow with invertible 1x1 convolutions."](https://arxiv.org/abs/1807.03039) arXiv:1807.03039 (2018).

[8] Germain, Mathieu, Karol Gregor, Iain Murray, and Hugo Larochelle. ["Made: Masked autoencoder for distribution estimation."](https://arxiv.org/abs/1502.03509) ICML 2015.

[9] Aaron van den Oord, Nal Kalchbrenner, and Koray Kavukcuoglu. ["Pixel recurrent neural networks."](https://arxiv.org/abs/1601.06759) ICML 2016.

[10] Diederik P. Kingma, et al. ["Improved variational inference with inverse autoregressive flow."](https://arxiv.org/abs/1606.04934) NIPS. 2016.

[11] George Papamakarios, Iain Murray, and Theo Pavlakou. ["Masked autoregressive flow for density estimation."](https://arxiv.org/abs/1705.07057) NIPS 2017.

[12] Jianlin Su, and Guang Wu. ["f-VAEs: Improve VAEs with Conditional Flows."](https://arxiv.org/abs/1809.05861) arXiv:1809.05861 (2018).

[13] Van Den Oord, Aaron, et al. ["WaveNet: A generative model for raw audio."](https://arxiv.org/abs/1609.03499) SSW. 2016.
