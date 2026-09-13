---
title: "标度律，需谨慎"
title_en: "Scaling Laws, Carefully"
source: https://lilianweng.github.io/posts/2026-06-24-scaling-laws/
crawled: 2026-09-08
translated: 2026-09-08
---

# 标度律，需谨慎

> 原文：[Scaling Laws, Carefully](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/) · Lilian Weng（翁荔）

标度律（scaling law）是深度学习中最关键的实证发现之一。其观察形式很简单：训练损失 $L$ 随着模型规模 $N$、数据集规模 $D$ 和计算量 $C$ 的增大而以可预测的方式下降，遵循幂律（power law）曲线——在双对数图上呈现为一条直线。我们可以把标度律视为一个描述计算量、损失、模型规模与数据之间关系的框架；其核心在于如何在 $N$ 与 $D$ 之间最优地分配宝贵的计算资源。

这种可预测性使标度律在实践中极具价值。一种常见的工作流是：先在少量小规模训练上拟合标度律，然后外推以估计更大模型所需的 token 数与计算量。

| 符号 | 说明 |
| --- | --- |
| $N$ | 模型规模，以参数量计量。 |
| $D$ | 训练数据集规模，通常以 token 数计量。 |
| $C$ | 以 FLOPs 计的训练计算量。一个有用的近似是 $C \approx 6ND$（[Kaplan et al. 2020](https://arxiv.org/abs/2001.08361)），其中 $2ND$ 对应前向传播，$4ND$ 对应反向传播。 |
| $E$ | 不可约损失（irreducible loss）。 |
| $L, \hat{L}(.)$ | 测试损失 / 测试损失预测函数；由于两者高度相关，也可指训练损失。 |
| $\epsilon$ | 泛化误差（generalization error）。 |

# 早期：机器学习损失的可预测性

在标度律成为主流概念之前，泛化误差随规模变化的可预测性就已被研究过。

[Amari et al. (1992)](https://ieeexplore.ieee.org/document/6796972) 使用贝叶斯方法和退火近似（annealed approximation）推导出了四类学习曲线（learning curve）。

1. 确定性学习算法、无噪声数据、唯一解：$\epsilon \sim c \cdot D^{-1}$，其中 $c$ 为某个常数。
2. 确定性学习算法、无噪声数据、多个等价解：$\epsilon \sim c \cdot D^{-2}$；每新增一个数据点，学习都收敛得更快，因为模型只需学习最优的参数流形，而不必寻找单一的解点。
3. 确定性学习算法、有噪声数据：$\epsilon \sim c \cdot D^{-1/2}$；数据中的噪声使学习更困难。
4. 随机学习算法、有噪声数据：$\epsilon \sim c \cdot D^{-1} + E$；这里不可约损失 $E$ 是随机学习器无法进一步降低的残余误差，例如模型在大规模数据上容量耗尽时。
   上述四类学习曲线都遵循幂律：

$$
\epsilon \sim c \cdot D^\alpha + E
$$

其中 $E$ 可以为 0，$\alpha = -2, -1, -1/2$。尽管其理论设定基于一个简化的二分类任务，但它为构建实证的机器学习损失预测模型指明了有用的方向。

[Hestness et al. (2017)](https://arxiv.org/abs/1712.00409) 最早的实证研究之一阐释了泛化误差、模型规模与数据之间的关系。对每个给定的训练数据规模，他们通过网格搜索确定最适配的模型规模，然后绘制损失随训练数据集规模变化的曲线。在深度学习的四个不同领域（神经机器翻译、图像分类、语言建模、语音识别）中，都反复观察到如下模式：

- 泛化误差在一组因子（如数据规模）上呈幂律伸缩。
- 模型的改进会移动误差曲线，但似乎不影响幂律指数。
- 有趣的是，架构会改变幂律拟合的偏移量（$E$），却不改变指数（$\alpha$）。幂律的斜率看来是问题域的属性，而非模型架构的属性。
- 拟合规模为 $D$ 的数据集所需的模型参数量 $N$ 也呈幂律伸缩。

![](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/hestness-1.png)

*（左）Deep-Speech-2（DS2）与注意力语音模型、（右）不同规模 DS2 模型的学习曲线。当训练数据变大时，小模型的损失进入平台期。（图片来源：Hestness et al. 2017）*

一个概念性图示把学习曲线分为三个阶段。在小数据区域，学习信号不足，模型仅比随机猜测略好；在中间的"幂律区域"，我们观察到损失、数据与模型规模之间的幂律关系；最后的不可约误差区域可归因于数据中的噪声等因素。

![](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/hestness-2.png)

*幂律学习曲线各阶段示意图。（图片来源：Hestness et al. 2017）*

[Rosenfeld et al. (2020)](https://arxiv.org/abs/1909.12673) 更进一步，尝试把误差建模为模型规模 $N$ 与数据规模 $D$ 的联合函数，实验覆盖多种架构（ResNet、WRN、LSTM、Transformer）与优化器（Adam、SGD 变体）。他们实证观察到：固定其中一个轴，误差随另一个轴呈幂律衰减：

$$
\hat{L}(D,N) \approx \frac{A}{N^{\alpha}} + E_N,\quad 
\hat{L}(D,N) \approx \frac{B}{D^{\beta}} + E_D
$$

二者可合并为一个联合形式：

$$
\hat{L}(D, N) \approx \frac{A}{N^{\alpha}} + \frac{B}{D^{\beta}} + E
$$

其中 $A > 0, B > 0, \alpha \geq 0, \beta \geq 0$ 为标量常数，$E$ 不依赖于 $N$ 或 $D$。

![](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/rosenfeld-1.png)

*数据规模、模型规模与泛化误差在 log-log-log 尺度下的三维等高线图。蓝点来自实证实验，曲面是蓝点之间的线性插值。（图片来源：Rosenfeld et al. 2020）*

这样，他们就可以构建一个形式简单的参数化预测模型，参数为 $\boldsymbol{\theta} = \langle A, B, E, \alpha, \beta \rangle$，只需在一组较小的训练配置（$(D, N)$ 小于特定阈值）上训练，即可预测 $(D, N)$ 大于特定阈值时的期望损失。

![](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/rosenfeld-2.png)

*在小规模配置上拟合参数化误差模型并外推到更大的模型/数据规模：(a) 实验设置示意图；(b) ImageNet、(c) WikiText-103 与 (d) CIFAR100 上的实验结果——使用三种架构（WRN、VGG、DenseNet）与两种优化器（SGD、Adam）做误差估计。（图片来源：Rosenfeld et al. 2020）*

题外话：这些早期工作依赖经典学习理论的直觉，例如用 [VC 维](https://en.wikipedia.org/wiki/Vapnik%E2%80%93Chervonenkis_dimension)（模型所能打散的最大点集的基数）作为容量的代理指标；但在现代深度学习工作中，VC 维往往过于粗糙、难以解释实际行为，而实证幂律被证明比理论给出的最坏情形界更干净、更实用。

# 数据无限区域的标度律

## Kaplan et al. 的标度律

[Kaplan et al. (2020)](https://arxiv.org/abs/2001.08361) 让标度律的概念在语言建模社区广为流行。他们发现，交叉熵（cross-entropy）测试损失 $L$ 与模型规模 $N$（不含嵌入层）、数据集规模 $D$、训练计算量 $C$ 各自都呈幂律关系，跨越多个数量级。这些发现与上一节的早期工作一致，但 Kaplan et al. 将概念形式化，聚焦于 Transformer 语言模型并开展了更大规模的实证实验：模型规模从 768M 到 1.5B 非嵌入参数，数据集规模从 22M 到 23B token。论文中所有训练都使用如下学习率调度：3000 步线性预热（warmup），随后余弦衰减（cosine decay）至零。

关键发现列表：

- 损失 $L$ 分别与 $N$、$D$、$C$ 呈幂律关系；要获得最优性能，三者必须同步扩大。
- 训练曲线遵循可预测的幂律，其参数大致与模型规模无关。
- 更大的模型样本效率更高，也就是说，比起小模型，它们以更少的优化步数和更少的数据点就能达到给定损失。
- 架构细节（宽度、长宽比等）远不如纯粹的规模重要。
- 训练损失与测试损失正相关。（听起来理所当然，但这是预训练工作的基础。另一方面，预训练损失的改进能否迁移到后训练评估，则需要另行研究。）
- 在固定计算预算下，训练一个很大的模型并在收敛*之前*停止，比把一个较小的模型一路训练到收敛更高效。**这正是 Chinchilla 标度律（下一节）不认同的发现：Kaplan et al. 高估了最优模型规模，因为他们拟合出的指数偏大。**

他们把对 $N$ 与 $D$ 的联合依赖总结为一个方程：

$$
\hat{L}(N,D) = \left[ \left(\frac{a}{N}\right)^{\frac{\alpha}{\beta}} + \frac{b}{D} \right]^{\beta}
$$

这一形式的一个漂亮推论是：过拟合程度（即模型复杂或数据偏少）主要取决于比值 $N^{\alpha / \beta} / D$，这表明数据需要按特定比例随模型规模的增长而增长，以避免训练受数据限制。

![](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/kaplan-1.png)

*测试损失与计算量、数据集规模、参数量的幂律关系，跨越多个数量级。（图片来源：Kaplan et al. 2020）*

最具影响力、事后看来也最具争议的结论是计算最优（compute-optimal）分配。Kaplan et al. 发现 $N_\text{opt} \propto C^{0.73}$，并得出模型规模应比数据集规模增长更快的结论。具体而言，计算量增加 10 倍时，他们建议模型规模扩大约 5.5 倍，而训练 token 只增加约 1.8 倍。Chinchilla 论文后来推翻了这一建议，认为它会让大模型严重*训练不足（undertrained）*。

Kaplan et al. 中另一项有用的分析是基于 $D$ 与 $N$ 估算所需的训练 FLOPs。每次乘加运算计为约 2 FLOPs。

![](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/kaplan-2.png)

*给定层数 $n_\text{layer}$、模型宽度 $d_\text{model}$（= $d_\text{embed}$；原表中的记号并不一致）、前馈层维度 $d_\text{ff}$（通常等价于 $4 d_\text{model}$）、注意力维度 $d_\text{attn}$（通常等价于 $d_\text{model}$）、上下文长度 $n_\text{ctx}$ 与词表规模 $n_\text{vocab}$ 时，Transformer 各架构组件的参数量与计算量估算。（图片来源：Kaplan et al. 2020）*

给定标准配置 $d_\text{attn} = d_\text{model} = d_\text{ff}/4$，并把嵌入层从 $N$ 与每 token 前向计算中排除：

$$
\begin{align}
N &= n_\text{layer} d_\text{model} 3 d_\text{attn} + n_\text{layer} d_\text{attn} d_\text{model} + n_\text{layer} 2 d_\text{model} d_\text{ff} & \small{\text{; no embedding layer}} \\
&= 2\;n_\text{layer} d_\text{model}(2d_\text{attn} + d_\text{ff}) & \\
&= 12\;n_\text{layer} d_\text{model}^2 & \\
\\
C_\text{fwd} &= 2 n_\text{layer} (d_\text{model} 3 d_\text{attn} + n_\text{ctx}d_\text{attn} + d_\text{attn}d_\text{embed} + 2 d_\text{model} d_\text{ff}) & \\
&= 2 n_\text{layer} (12 d_\text{model}^2 + n_\text{ctx}d_\text{attn}) & \\
&= 2N + 2 n_\text{layer}n_\text{ctx}d_\text{attn} & \\
&\approx 2N \quad\quad \small{\text{; assuming }n_\text{ctx} < 12 d_\text{model} \text{ and the }n_\text{ctx}\text{ term is relatively small.}}\\
\end{align}
$$

然后，我们把反向传播的 FLOPs 计为前向传播的两倍，因为反向传播需要做两次矩阵乘法，分别求出相对于输入激活和权重的梯度。因此，总计下来每个 token 的训练 FLOPs 约为 $6N$，在 $D$ 个 token 上训练的总 FLOPs 为 $C \approx 6ND$。

## Chinchilla 标度律

Chinchilla 论文（[Hoffmann et al. 2022](https://arxiv.org/abs/2203.15556)）以更谨慎的实验设计，研究了在*固定*计算预算 $C$ 下最优模型规模 $N$（总参数量，*包含*嵌入）与 token 数 $D$ 之间的关系，并得出了与 Kaplan et al. 略有不同的答案。

![](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/animal.png)

*你应该知道龙猫长什么样 😊（图片来源：ChatGPT 生成）*

核心问题是在约束 $\text{FLOPs}(N, D) = C \approx 6ND$ 下的最优资源分配策略。换言之，当我们只有有限的 FLOPs（给定数量的 GPU 运行给定时长）时，应如何在更多数据 token 与更多模型参数之间做选择？

$$
N_\text{opt}(C), D_\text{opt}(C) = \operatorname*{arg\,min}_{\text{s.t. } \text{FLOPs}(N,D) = C} \hat{L}(N, D)
$$

Chinchilla 论文给出了三种设计精巧的标度律拟合方法。

实证实验扫描了 400 多个模型，参数规模从 70M 到超过 16B，训练 token 从 5B 到 500B。实验假设每个训练 token 都是唯一的（无限数据情形）。所有训练都使用余弦学习率调度，在整个训练过程中衰减 10 倍。对模型规模进行扫描即可勾勒出计算最优前沿。

### 方法 1：固定模型规模，改变 token 预算

对每个参数量 $N$，以不同的 token 预算训练多个 run，并记录每个 FLOP 预算 $C$ 下达到的最小损失。

![](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/chinchilla-1.png)

*Chinchilla 方法 1：一系列模型规模在不同 FLOP 预算下的训练损失曲线。（图片来源：Hoffmann et al. 2022）*

### 方法 2：IsoFLOP 剖面

固定一个计算预算 $C$，绘制最终损失随参数量 $N$ 变化的曲线。每条 iso-FLOP 曲线在对数空间中大致是一条抛物线，其最低点标示出该计算预算下的最优模型规模。然后在多个预算上重复这一过程，便在图中勾勒出一条幂律直线。

![](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/chinchilla-2.png)

*Chinchilla 方法 2：IsoFLOP 抛物线；每条曲线的最低点即该预算下计算最优的模型规模。（图片来源：Hoffmann et al. 2022）*

### 方法 3：参数化拟合

直接拟合与 [Rosenfeld et al. (2020)](https://arxiv.org/abs/1909.12673) 相同的参数化函数，

$$
\hat{L}(N, D) = \frac{A}{N^\alpha} + \frac{B}{D^\beta} + E
$$

实际上，我们可以通过在约束 $\text{FLOPs}(N,D) = C \approx 6ND$ 下最小化 $\hat{L}(N, D)$，得到最优 $N_\text{opt}(C), D_\text{opt}(C)$ 的闭式近似。

首先把表达式化简为只含 $N$：

$$
\begin{align}
\hat{L}(N) &= A N^{-\alpha} + B \Big(\frac{C}{6}\Big)^{-\beta}N^\beta + E \\
\hat{L}'(N) &= -\alpha A N^{-\alpha-1} + \beta B \Big(\frac{C}{6}\Big)^{-\beta} N^{\beta -1} = 0 & \small{\text{; derivative wrt }N\text{ should be zero.}} \\
\text{Thus}\quad & \alpha A N^{-\alpha-1} = \beta B \Big(\frac{C}{6}\Big)^{-\beta} N^{\beta -1} \\
& \alpha A = \beta B \Big(\frac{C}{6}\Big)^{-\beta} N^{\alpha + \beta} \\
& N_\text{opt} = \Big(\frac{\alpha A}{\beta B}\Big)^{\frac{1}{\alpha + \beta}} \Big(\frac{C}{6}\Big)^{\frac{\beta}{\alpha+\beta}} \\
& D_\text{opt} = \frac{C}{6 N_\text{opt}} = \Big(\frac{\beta B}{\alpha A}\Big)^{\frac{1}{\alpha + \beta}} \Big(\frac{C}{6}\Big)^{\frac{\alpha}{\alpha+\beta}}
\end{align}
$$

当 $\alpha \approx \beta$ 时，模型规模与训练 token 应以相同的速率增长。

为找到最优的 $\boldsymbol{\theta} = \langle A, B, E, \alpha, \beta\rangle$，Chinchilla 论文采用了 [Huber 损失](https://en.wikipedia.org/wiki/Huber_loss)（对离群值稳健；$\delta=10^{-3}$）与 [L-BFGS 算法](https://en.wikipedia.org/wiki/Limited-memory_BFGS)（适合参数量很少的曲线拟合）。

$$
\begin{align}
\min_{A,B,E,\alpha,\beta} \sum_{\text{runs }\{i\}} \text{Huber}_\delta (\log \hat{L}(N_i, D_i) - \log L_i) \\
\text{ where }\text{Huber}_\delta (x) = \begin{cases}\frac{1}{2} x^2 & \text{for }\vert x \vert \leq \delta \\ \delta \cdot (\vert x \vert - \frac{1}{2}\delta), & \text{otherwise.}\end{cases}
\end{align}
$$

Chinchilla 通过三种互补的方法得出结论，且三种方法的最终结果彼此一致，这正是该结果颇具说服力的部分原因。

![](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/chinchilla-3.png)

*三种方法都指向 $N_\text{opt} \propto C^{0.5}$ 的计算最优前沿，彼此一致，但与 Kaplan et al. 相左。注意方法 3 的结果与另外两种略有偏差，后文会解释原因。（图片来源：Hoffmann et al. 2022）*

![](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/chinchilla-4.png)

*三种不同方法得到的 Chinchilla 预测，以及 Kaplan et al. (2020) 的预测。三种方法都表明当时若干主流 LLM 训练不足。（图片来源：Hoffmann et al. 2022）*

Chinchilla 论文"大多数大模型（当时约 2022 年）训练不足"的论断有一个著名的实证支撑：在与 Gopher（[Rae et al. 2021](https://arxiv.org/abs/2112.11446)；280B 参数量、300B token 预算）相同的计算预算下，他们训练了 Chinchilla（70B 参数量、1.4T token 预算）——该模型小 4 倍，却在多约 4 倍的 token 上训练，并全面超越了 Gopher。

## 调和 Kaplan 与 Chinchilla

Chinchilla 标度律与 Kaplan et al. 的分歧如下：

- 不是"让模型比数据增长更快"（$N_\text{opt} \propto C^{0.73}$），而是模型规模每翻一倍，训练 token 数也应翻倍（$N_\text{opt} \propto C^{0.5}$）。
- 不是"训练一个大模型并在收敛前停止"，而是用更多数据训练一个更小的模型。

两篇论文在底层原理上仍然一致，但在"规模与 token 的最优权衡点在哪里"上存在分歧。为什么它们的分歧如此之大？

**差异 1：Kaplan et al. 的实验主要在小模型上进行。**
Kaplan et al. 的实验大多在较小的模型上进行，而 Chinchilla 论文的实验规模大了 10 倍以上。当我们在双对数空间中做外推时，拟合上的小差异可能导致巨大的差异（见[玩具模拟](#toy-simulation)）。

**差异 2：嵌入参数量对小模型很重要。**
在小参数区间，嵌入（embedding）参数占总量的比例不可忽略，因此是否计入它们会影响结果。[Pearce & Song (2024)](https://arxiv.org/abs/2406.12907) 沿这条思路做了彻底的分析。我们用 $N_{\setminus E}, C_{\setminus E}$ 表示排除嵌入后的模型规模与计算量，用 $N, C$ 表示总参数口径。

- Kaplan et al.：$N^*_{\setminus E} \propto C^{0.73}_{\setminus E}$（非嵌入）
- Chinchilla：$N^* \propto C^{0.50}$（总量）

为在两者之间架起桥梁，他们拟合了总参数 $N_T$ 与非嵌入参数 $N_{\setminus E}$ 之间的关系，其中 $\omega$ 为某个常数：

$$
N = N_{\setminus E} + \omega\, N_{\setminus E}^{1/3}.
$$

这一形式有良好的性质：严格递增，且 $\lim_{N \to \infty} N = N_{\setminus E}$（因为 $\frac{N}{N_{\setminus E}} = 1 + \omega {N_{\setminus E}}^{- \frac{2}{3}}, \lim_{N_{\setminus E} \to \infty} \frac{N}{N_{\setminus E}} = 1$）。

把它代入 Chinchilla 定律方程，

$$
\begin{align}
L(N_{\setminus E}, C_{\setminus E}) &= A(N_{\setminus E} + \omega\, N_{\setminus E}^{1/3})^{-\alpha} + B \Big(\frac{C_{\setminus E}}{6}\Big)^{-\beta} N_{\setminus E}^\beta + E \\
L'(N_{\setminus E}, C_{\setminus E}) &= - \alpha A (N_{\setminus E} + \omega N_{\setminus E}^{1/3})^{-\alpha -1}(1 + \frac{\omega}{3}N_{\setminus E}^{-2/3}) + \beta B \Big(\frac{C_{\setminus E}}{6}\Big)^{-\beta} N_{\setminus E}^{\beta -1} = 0 & \small{\text{; derivative wrt }N_{\setminus E}\text{ should be zero.}} \\
\text{Rearrange to get }& \alpha A (N^{*}_{\setminus E} + \omega {N^{*}_{\setminus E}}^{1/3})^{-\alpha -1}(1 + \frac{\omega}{3} {N^{*}_{\setminus E}}^{-2/3}) = \beta B \Big(\frac{C_{\setminus E}}{6}\Big)^{-\beta} {N^{*}_{\setminus E}}^{\beta -1} \\
& 6^{-\beta}\frac{\alpha A}{\beta B} ({N^{*}_{\setminus E}} + \omega {N^{*}_{\setminus E}}^{1/3})^{-\alpha -1}(1 + \frac{\omega}{3}{N^{*}_{\setminus E}}^{-2/3}) {N^{*}_{\setminus E}}^{1 - \beta} = C_{\setminus E}^{-\beta} \\
& 6 \Big(\frac{\beta B}{\alpha A}\Big)^{\frac{1}{\beta}} ({N^{*}_{\setminus E}} + \omega {N^{*}_{\setminus E}}^{1/3})^{\frac{1 + \alpha}{\beta}} ({N^{*}_{\setminus E}} + \frac{\omega}{3}{N^{*}_{\setminus E}}^{1/3})^{-\frac{1}{\beta}} {N^{*}_{\setminus E}} = C_{\setminus E} \\
\end{align}
$$

上式中 $C_{\setminus E}$ 与 $N_{\setminus E}$ 的关系不再是干净的幂律。我们只能把它局部近似为 $N^*_{\setminus E} \overset{\propto}{\sim} C_{\setminus E}^g$，其中 $g$ 是基于一阶导数（$\overset{\propto}{\sim}$）的局部指数，而非全局幂律指数，即 $g = \frac{\mathrm{d} \log C_{\setminus E}}{\mathrm{d} \log N_{\setminus E}}$。指数 $g$ 如何近似求解的完整细节见 [Pearce & Song (2024)](https://arxiv.org/abs/2406.12907) 的附录 A.1。

![](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/pearce-1.png)

*局部幂律指数 $g$ 随 $C_{\setminus E}$ 增长的可视化。（图片来源：Pearce & Song 2024）*

如上图所示，随着 $C_{\setminus E}$ 变大，$g$ 收敛到 Chinchilla 的估计值。通过用上式生成合成训练曲线，在 768M 到 1.5B 的模型规模区间（与 Kaplan et al. 相同），他们估计该区间内 $g$ 接近 Kaplan 的系数 0.73。

## 为什么是幂律？

幂律在 AI 之外的许多领域也被广泛观察到，例如 [Zipf 定律](https://en.wikipedia.org/wiki/Zipf%27s_law)、[无标度网络](https://en.wikipedia.org/wiki/Scale-free_network)、[城市标度律](https://en.wikipedia.org/wiki/Urban_scaling)以及许多其他复杂系统。反复出现的模式是：大事件稀少、小事件常见，而规模与频率的关系在双对数尺度下常呈一条直线。

**为什么 LLM 的标度律也呈幂律形状？**

部分受不同领域表现出不同指数的现象启发（[Hestness et al. 2017](https://arxiv.org/abs/1712.00409)），[Sharma & Kaplan (2020)](https://arxiv.org/abs/2004.10802) 提出的一种早期解释假设：语言建模可视为在数据的低维流形上做回归。更多的模型参数能诱导对数据流形更细的划分，从而带来更小的泛化误差。用最简单的话说，若有效规模为 $N$ 的模型把 $d$ 维流形划分为 $O(N)$ 个区域，则典型线性分辨率按 $\sim N^{-1/d}$ 伸缩。这与上面的标度律有相似的幂律形式。该理论在无限数据、欠拟合的情形下最干净地成立，但现实中估计数据流形的本征维度相当困难。

一个较晚出现的假设（[Michaud et al. 2023](https://arxiv.org/abs/2303.13506)、[Brill 2024](https://arxiv.org/abs/2412.07942)）认为，知识或技能是以离散块（"量子化"）的形式学得的，而这些技能的频率分布遵循幂律。模型先学会常见技能、后学会罕见技能，从而带来损失的平滑幂律衰减。

这里只列出了两种假设，但还有更多研究尝试通过数据的谱尾、核特征值、自然语言统计或训练动态中的相变来解释幂律伸缩的形状。

# 数据受限区域的标度律

经典标度律假设实际上是*无限的不重复数据*：没有重复、也没有多轮（multi-epoch）训练。随着模型规模显著增长，高质量的不重复 token 正在被耗尽。事实上，一些关于 AI 规模化还能持续多久的论证，正是围绕我们是否正在撞上"数据墙（data wall）"展开的。

同样值得强调的是，$D$ 背后的数据集理应已经过清洗。预训练数据管线往往是有效预训练管线的重要组成部分，常见步骤包括去重（精确与模糊）、质量过滤、样板文本移除、安全过滤、PII/版权遮蔽、基准测试去污染，以及按语言、质量、内容类型等对数据混合组分做细致的重新加权。即使两个数据集包含相同的 token 数 $D$，一个高质量数据集与一个互联网糟粕数据集也可能带来截然不同的计算效率。

[Hernandez et al. (2022)](https://arxiv.org/abs/2205.10487) 的研究聚焦于一个受控版本：以不重复数据为主、掺入小比例重复数据的数据集。从一个大数据集出发，数据混合保留 90% 不重复数据，其余 10% 替换为对原数据中一小部分的重复。通过在 100B token 上训练 Transformer 模型，他们观察到了双下降（double descent）现象：测试损失随重复数据被强调程度的变化先变*差*、再变好，且随着重复比例增大，这一效应更加明显。

![](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/hernandez-1.png)

*重复比例增加时测试损失的双下降（左图 90% 重复，右图 50% 重复）。（图片来源：Hernandez et al. 2022）*

训练中段的平坦或上升趋势可能来自对重复数据的记忆。具有这类形状的学习曲线会降低标度律拟合的准确性。他们还得出结论：重复数据会损害某些分布外（OOD）评估与下游微调。不过，他们的数据混合是在较接近实验室环境的设置下构造的，而真实世界数据中的重复往往更加微妙（例如不同数据有不同程度的重复、语义重复等）。

与其断言数据重复伤害训练，我们更关心的是：在高质量不重复数据并非无限、训练中很可能不得不重复数据的前提下，如何拟合标度律。

[Muennighoff et al. (2023)](https://arxiv.org/abs/2305.16264) 承接了这一研究问题：当模型训练受数据限制时，计算应如何最优分配。具体而言，他们通过约 400 次实验实证研究了数据重复的影响，覆盖 10M–9B 参数、最高 900B token 的数据规模、最多 1500 个 epoch。每个 epoch 重复完全相同的数据集，epoch 之间重新打乱，并在留出测试集上评估。

关键的建模调整是把总 token 数 $D$ 分解为两部分：(i) 不重复 token 数 $U_D$ 与 (ii) 重复次数 $R_D$（即 epoch 数 - 1）。于是有 $D = U_D(1 + R_D)$。给定不重复数据预算 $D_\text{uniq}$，按定义 $U_D = \min \{{ D_\text{uniq}, D\}}$、$R_D = (D / U_D) - 1$。他们用 Chinchilla 标度律求出拟合 $U_D$ 所需的最优模型规模 $U_N$，并通过重复定义过剩模型规模 $R_N = (N / U_N) - 1$。

随后他们更新 Chinchilla 参数化拟合（[方法 3](#chinchilla-method3)），用有效（折损后的）数据 $D’$ 与模型规模 $N’$ 代替原始数量：

$$
\hat{L}(N, D) = \frac{A}{N'^\alpha} + \frac{B}{D'^\beta} + E
\quad\text{ where }
D' = U_D + U_D\, r_D\left(1 - \exp\!\left(-\frac{R_D}{r_D}\right)\right).
$$

直觉是：一个 token 被重复时，其价值呈*指数*衰减。在他们的建模中，每次重复都会使该 token 损失其剩余价值的 $(1 - 1/r_D)$ 比例，其中 $r_D$ 是可学习的"半衰期"参数。当 $R_D = 0$ 或 $R_D \ll r_D$ 时，我们恢复 $D’ \approx D$。

一个对称的公式处理过剩模型规模：$N’ = U_N + U_N r_N(1 - \exp(-R_N / r_N))$，它捕捉的想法是"更大的模型在重复数据上过拟合更快"以及"模型相对于其数据集可能过大"。这一组成部分的直觉性较差，我没能找到为何模型规模需要以与重复数据对称的形式出现的满意解释。[Lovelace et al. (2026)](https://arxiv.org/abs/2605.01640) 的后续工作改变了这一假设。

他们的实证拟合发现，*过剩参数的价值衰减快于重复数据*，$r_N < r_D$，因此我们应把更多资源投入更多 epoch，而非更多模型参数。正如作者自己也指出的，这一建模的一个弱点是：它会显著低估"失败模型"（即训练中途损失上升的模型，如训练了 44 个 epoch 的模型）的最终测试损失。

![](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/muennighoff-1.png)

*考虑重复的数据受限伸缩比无视数据重复的拟合更好地刻画实验结果；重复 token 的价值呈指数衰减并趋于上限。epoch 越多拟合越差，因为高重复会导致测试损失在训练中途上升，这一点未在图中描绘。（图片来源：Muennighoff et al. 2023）*

最近，[Lovelace et al. (2026)](https://arxiv.org/abs/2605.01640) 用不同的方法重新审视了同一问题。他们不再把过参数化建模为有效模型规模的收益递减，而是显式建模模型规模 $\times$ 数据重复之间的交互。实证上，他们训练了约 300 个模型，覆盖 15M 到 1B 参数、50M 到 6B 不重复 token。

当他们为固定的模型规模绘制不同数据重复水平下的拟合残差时，观察很直观：epoch 越多损害越大，而且有趣的是，*更大的模型对重复更敏感*。这暗示损失惩罚很可能是模型规模与数据规模两者的函数。

![](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/lovelace-1.png)

*有效规模拟合的残差揭示：过拟合损害随 epoch 数与模型规模同时增长。（图片来源：Lovelace et al. 2026）*

他们引入了一个显式的过拟合惩罚项，围绕*容量比* $N / U_D$（参数量与不重复 token 数之比）构建：

$$
\hat{L}(N, U_D, R_D) = E + \frac{A}{N^\alpha} + \frac{B}{\big(U_D (1 + R_D)\big)^\beta} + \color{red}{P \cdot R_D^\delta \cdot \left(\frac{N}{U_D}\right)^\kappa}
$$

其中：

- $R_D$ 是重复次数；
- 标量 $P$ 是一个可学习参数；
- 指数 $\kappa$（第二个可学习参数）使惩罚随容量比 $N / U_D$ 非线性伸缩；
- 重复次数上的独立指数 $\delta$（第三个可学习参数）把重复的非线性与 $\kappa$ 解耦。

新增项（红色）是一个直接的过拟合惩罚，它随数据重复的次数以及模型相对可用不重复数据的过参数化程度同时增长。

他们还做了一个关于权重衰减如何在数据受限约束下影响训练的案例研究，发现强权重衰减能降低数据重复造成的过拟合惩罚。

![](https://lilianweng.github.io/posts/2026-06-24-scaling-laws/lovelace-2.png)

*强权重衰减降低了数据重复带来的过拟合惩罚。（图片来源：Lovelace et al. 2026）*

Muennighoff et al. 与 Lovelace et al. 的两种建模方法都源自实证曲线拟合，因此数据受限标度律为何恰好应取这些形式、每个自由参数为何必要，目前仍不清楚。期待沿这一方向出现更多理论工作。

# 现实中拟合标度律的微妙之处

尽管形式干净，实践中标度律拟合对看似琐碎的流程选择可能出奇地敏感，例如如何统计参数、如何做精度舍入、如何对损失求和或求平均，等等。

因为标度律只能在（相对小、相对便宜的）我们负担得起的模型上拟合，而预测却要*外推*到大几个数量级的模型上。在这种设置下，看似舍入误差级别的选择可能导致预测结果的巨大差异。

同时，标度律拟合假设唯一变化的因子是*规模*，这意味着模型架构、优化器、学习率调度、批大小爬坡、数据混合、分词器及其他设计选择都应保持不变。另一个隐含假设是所有这些设置都应经过仔细调优，因为像模型训练不足这类情况可能导致不同的结论。

Kaplan et al. 与 Chinchilla 结果之间的分歧，就是展示标度律拟合之微妙的一个例子。

第二个例子是一项后续分析，研究为什么 Chinchilla [方法 3](#method-3-parametric-fit) 与另外两种方法略有偏差。[Besiroglu et al. (2024)](https://arxiv.org/abs/2404.10102) 从 Hoffmann et al. (2022) 的图 4 中提取了原始 $(N, D, L)$ 数据点，并重新运行了方法 3 的参数化拟合。他们发现了几个具体问题：

- L-BFGS-B 最小化器中的损失尺度偏高，原因是把各样本的 Huber 损失取了平均而非求和，这导致优化过早终止。原始拟合与自助法（bootstrapping）过程中损失最小化的提前停止，产生了不一致的估计与窄得难以置信的置信区间。
- 论文报告的 $\alpha$ 与 $\beta$ 被舍入到 2 位精度，这使得导出的 $A, B$ 看起来比实际情况偏差更大。

## 玩具模拟

下面是一个由 ChatGPT 创建的玩具模拟小部件，用于演示三种具体的失败模式。

我们假设真值函数为：

$$
\hat{L}(N, D) = 482.01 \cdot N^{-0.3478} + 2085.43 D^{-0.3658} + 1.8172
$$

于是 $N_\text{opt} \propto C^{0.5126}, D_\text{opt} \propto C^{0.4874}$。这是 [Besiroglu et al. (2024)](https://arxiv.org/abs/2404.10102) 给出的估计。

该模拟绘制损失预测 $\hat{L}$ 相对数据集规模 $D$ 的变化，并提供一组滑块来演示：

- 损失精度：把损失舍入到越来越少的小数位，会改变拟合出的参数值。
- 损失噪声：仅以毫损失（0.001）单位量级的乘数扰动损失值，就会得到不同的拟合。
- 拟合区域敏感性：只拟合小模型、只拟合中等模型或拟合全部模型，会得到不同的表观标度律。

# 引用

请按如下方式引用本文：

> Weng, Lilian. “Scaling Laws, Carefully”. Lil’Log (Jun 2026). https://lilianweng.github.io/posts/2026-06-24-scaling-laws/

或使用 BibTeX 引用：

```
@article{weng2026scaling,
 title = {Scaling Laws, Carefully},
 author = {Weng, Lilian},
 journal = {lilianweng.github.io},
 year = {2026},
 month = {June},
 url = "https://lilianweng.github.io/posts/2026-06-24-scaling-laws/"
}
```

# 参考文献

[1] S. Amari, N. Fujita, and S. Shinomoto. [“Four Types of Learning Curves. Neural Computation.”](https://ieeexplore.ieee.org/document/6796972) 4(4):605–618, 1992.

[2] Hestness et al. [“Deep Learning Scaling is Predictable, Empirically.”](https://arxiv.org/abs/1712.00409) arXiv preprint arXiv:1712.00409, 2017.

[3] Rosenfeld et al. [“A Constructive Prediction of the Generalization Error Across Scales.”](https://arxiv.org/abs/1909.12673) ICLR 2020.

[4] Kaplan et al. [“Scaling Laws for Neural Language Models.”](https://arxiv.org/abs/2001.08361) arXiv preprint arXiv:2001.08361, 2020.

[5] Hoffmann et al. [“Training Compute-Optimal Large Language Models.”](https://arxiv.org/abs/2203.15556) NeurIPS 2022.

[6] Pearce and Song. [“Reconciling Kaplan and Chinchilla Scaling Laws.”](https://arxiv.org/abs/2406.12907) TMLR 2024.

[7] Bahri et al. [“Explaining Neural Scaling Laws.”](https://arxiv.org/abs/2102.06701) arXiv preprint arXiv:2102.06701, 2021.

[8] Sharma and Kaplan. [“A Neural Scaling Law from the Dimension of the Data Manifold.”](https://arxiv.org/abs/2004.10802) arXiv preprint arXiv:2004.10802, 2020.

[9] Hernandez et al. [“Scaling Laws and Interpretability of Learning from Repeated Data.”](https://arxiv.org/abs/2205.10487) arXiv preprint arXiv:2205.10487, 2022.

[10] Muennighoff et al. [“Scaling Data-Constrained Language Models.”](https://arxiv.org/abs/2305.16264) NeurIPS 2023.

[11] Lovelace et al. [“Prescriptive Scaling Laws for Data Constrained Training.”](https://arxiv.org/abs/2605.01640) arXiv preprint arXiv:2605.01640, 2026.

[12] Besiroglu et al. [“Chinchilla Scaling: A Replication Attempt.”](https://arxiv.org/abs/2404.10102) arXiv preprint arXiv:2404.10102, 2024.

[13] Michaud et al. [“The Quantization Model of Neural Scaling”](https://arxiv.org/abs/2303.13506) NeurIPS 2023.

[14] Brill. [“Neural Scaling Laws Rooted in the Data Distribution.”](https://arxiv.org/abs/2412.07942) arXiv preprint arXiv:2412.07942, 2024.

[15] Rae et al. [“Scaling Language Models: Methods, Analysis & Insights from Training Gopher.”](https://arxiv.org/abs/2112.11446) arXiv preprint arXiv:2112.11446, 2021.
