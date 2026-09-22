---
title: "模块化流形"
title_en: "Modular Manifolds"
date: 2026-08-31
source: https://thinkingmachines.ai/blog/modular-manifolds/
crawled: 2026-09-22
translated: 2026-09-22
---

# 模块化流形

> 原文：[Modular Manifolds](https://thinkingmachines.ai/blog/modular-manifolds/) · Thinking Machines Lab

训练大型神经网络时，我们需要让它们保持「健康」。我们不希望网络中的张量——无论是权重、激活还是梯度——变得过大或过小。极小和极大的张量会引发各种问题，且并不限于数值下溢和上溢。例如，权重矩阵在训练过程中不断改变规模，会让训练算法更难设计——因为更新相对于权重的规模对学习速度有显著影响。

保持张量健康的黄金标准是对它们做归一化（normalization）。对激活向量做归一化十分常见，我们使用 [layer norm](https://arxiv.org/abs/1607.06450) 等技术，在把激活传给下一层之前将它们调整到合适的尺度。对梯度更新做归一化也很常见，比如可以把 [Muon 优化器](https://kellerjordan.github.io/posts/muon/) 这类快速训练算法理解为对更新做谱归一化。归一化让我们对张量的规模有了确定性——无需去查 Wandb！——而在训练由许多相互作用的组件构成的大型神经网络时，对网络内部状态的确定性是很有价值的。

归一化较少应用于权重矩阵，但也并非没有先例。例如，[EDM2](https://github.com/NVlabs/edm2) 扩散模型代码库使用了权重约束，作者在[他们的论文](https://arxiv.org/abs/2312.02696)中报告了收益；[BiT](https://arxiv.org/abs/1912.11370) 使用了[权重标准化](https://arxiv.org/abs/1903.10520)（weight standardization）。人们还提出过其他各种技术，但它们并未成为现代大规模训练中的常见做法。（更多例子见 [Salimans et al, 2016](https://arxiv.org/abs/1602.07868)、[Miyato et al, 2018](https://arxiv.org/abs/1802.05957)，以及我们的论文 [Liu et al, 2021](https://arxiv.org/abs/2102.07227)。）约束权重矩阵可能是个好主意，理由有几点：权重约束让我们更容易理解优化更新的相对规模；它们消除了权重范数爆炸的问题；它们让我们把超参数调优的精力集中到规模最关键的那些张量上；它们可以迫使矩阵拥有较小的[条件数](https://en.wikipedia.org/wiki/Condition_number)，使其行为更可预测；与此相关地，权重约束还有助于获得对扰动鲁棒的 [Lipschitz 保证](https://theses.hal.science/tel-04674274v1)。

本文介绍一种约束神经网络权重矩阵的颇具吸引力的方式——让每层的张量被约束在子流形上。这为重新思考优化打开了大门，因为我们可以让优化算法与这些流形约束协同设计。作为例子，我们提出 Muon 优化器的一个流形版本（该算法建立在 Jianlin Su 与 Franz Louis Cesista 的工作之上，下文将进一步讨论。），其权重被约束在 Stiefel 流形上：即条件数等于 1 的矩阵所构成的流形。文章最后，我们定义*模块化流形*（modular manifold）的概念——一种可组合的流形，试图让大型网络的扩展与训练变得更容易。

我们撰写这篇文章的目标，是介绍一个令我们兴奋的研究方向，并指出许多可供未来努力的方向。我们非常乐意看到社区在文末提到的这些主题上做出更多工作！

## 流形优化器的形状

本节演练在流形上学习的最简单例子：一个被约束在 R^d 中超球面上的向量参数。该向量参数经过训练，以最小化定义在整个空间 R^d 上的损失函数。这一设定对诸如 transformer 模型中的单个嵌入向量之类的场景可能有用。本节是很好的热身，为下一节考虑矩阵参数的[流形 Muon](#muon-on-the-stiefel-manifold) 做铺垫。

这里我们不会对流形的定义过于形式化：把流形理解为一张弯曲的曲面，放大到足够近时它看起来是平的，就足够了。流形上一点处的局部平坦近似称为该流形的*切空间*（tangent space），如[图](#fig:tangent-space)所示：

三维球面——或高维空间中的超球面——是一个流形。流形上一点处的局部平坦近似称为该流形的切空间，在图中可视化为红色平面。

我们可以把 d 维超球面刻画为 R^d 中欧氏范数为 1 的点 w 的集合。而超球面上一点 w 处的切空间，是与 w 正交的所有向量 a ∈ R^d 构成的集合。

为了让权重保持在流形上，我们可以使用非流形优化器，在每一步之后把权重投影回流形。但我们更感兴趣的是设计直接在切空间中迈步的方法。原因在于，我们希望让优化器的学习率等同于优化步的实际长度。但如果优化步显著指向流形之外、然后再被投影回来，这个好性质就不成立了。[EDM2 论文](https://arxiv.org/abs/2312.02696)的第 2.3 节给出了类似的动机。

在设计适用于这个流形的训练算法之前，我们需要决定的一件重要事情是如何在切空间中度量距离（一个流形要成为「黎曼（Riemannian）」流形，其距离度量必须由内积诱导。[欧氏（ℓ₂）范数](https://en.wikipedia.org/wiki/Euclidean_distance)由内积诱导，而[曼哈顿（ℓ₁）距离](https://en.wikipedia.org/wiki/Taxicab_geometry)则不是。）。常见的选择是欧氏距离，但我们也可以选择用其他方式度量距离，如[图](#fig:inscribed-norm-balls)所示。在下一节中，我们将讨论如何基于模块的功能来选择距离度量。

在切空间中为不同距离度量内切单位球。ℓ₂（欧氏）单位球是一个圆，而 ℓ₁（曼哈顿）单位球是一个菱形。

关键在于，距离度量的选择会改变最优优化步的方向。如果距离度量是非欧氏的，那么对于固定长度的步，不严格沿梯度方向走，反而可能让我们在梯度方向（这里所说的梯度，指损失对权重的偏导数。数学家在黎曼几何中把「梯度」一词留给[别的对象](https://en.wikipedia.org/wiki/Gradient#Riemannian_manifolds)。）上前进得更远！这一概念如[图](#fig:tangent-space-with-gradient)所示。

几何如何影响最优优化步的方向。粉色箭头表示原始梯度——即损失对权重的偏导数。黄色菱形表示 ℓ₁ 单位球。绿色箭头是在梯度方向上指向最远的单位向量。注意绿色箭头并不平行于粉色箭头。（实践中，粉色箭头不必位于切空间中，而绿色箭头按构造必然落在切空间中。）试着拖动粉色箭头，看看最优更新方向如何变化。

要用数学看清这一点，我们可以把「给定流形约束与距离度量后的最优更新方向」本身表述为一个约束优化问题来求解。我们以配备欧氏范数的超球面为例进行演示。设 g 表示梯度，w 表示超球面上的当前点，a 表示更新方向，η 表示学习率，我们需要求解：

min_{a∈R^d}　aᵀg（损失的线性变化），约束为　‖a‖₂ = η（尺寸约束）且 aᵀw = 0（切向约束）。　(⋆)

映射回前面几幅图的视觉语言：这个公式说的是，绿色箭头（a 的最优值）必须属于红色切超平面（aᵀw = 0），并且还必须位于半径为 η 的黄色圆周上（‖a‖₂ = η）。要求解 (⋆)，可以应用[拉格朗日乘子法](https://en.wikipedia.org/wiki/Lagrange_multiplier)。相关的拉格朗日函数为：

L(a, λ, μ) = aᵀg + (λ/2)·(aᵀa − η) + μ·(aᵀw)，

其中 λ 和 μ 是拉格朗日乘子。令拉格朗日函数对 a 的导数为零，并应用各约束求解 λ 与 μ，最优更新 a_opt 最终由下式给出：

a_opt = −η × (g − wwᵀg) / ‖g − wwᵀg‖₂.

用文字来说，最优更新是：从梯度中减去径向分量，归一化，再乘以学习率。由于这一更新位于切空间中，实际上只需要一个非常小的修正（对学习率 η，收缩映射的效应是 O(η²) 量级，所以学习率*几乎*等于步长。）就能保持在流形上。这个修正被称为「收缩映射」（retraction map），如[图](#fig:retraction-map)所示：

收缩映射的可视化。绿色箭头是在切空间中走出的更新。由于步长较大时切空间开始偏离流形，我们需要用收缩映射把更新后的权重投影回流形——由紫色箭头示意。

对[图](#fig:retraction-map)应用勾股定理即可求出收缩映射。对于单位超球面和长度为 η 的步，斜边长度为 √(1+η²)，因此配备欧氏范数的超球面的收缩映射，就是简单地用 √(1+η²) 去除更新后的权重。把所有内容组合起来，完整的流形优化算法为：

w ← (1/√(1+η²))·[w − η × (g − wwᵀg) / ‖g − wwᵀg‖₂].

作为留给读者的练习：试着计算更新后权重向量的欧氏范数，验证更新后的权重向量确实位于超球面上。

总结本节：一阶流形优化器有三个步骤：

1. 找到在梯度方向上前进最远的单位长度切向量；
2. 将该方向乘以学习率，并从权重中减去；
3. 将更新后的权重收缩回流形。

应用这一流程需要做两个决策：使用什么流形约束，以及如何度量长度。通过做出不同的决策，我们可以生成不同的优化算法，如下表所示。

| 流形 | 范数 | 优化器 |
| --- | --- | --- |
| 欧氏空间 R^n | 欧氏范数 | 朴素梯度下降 |
| 欧氏空间 R^n | 无穷范数 | 符号梯度下降 |
| 超球面 S^n | 欧氏范数 | 超球面下降 |
| 矩阵空间 R^(m×n) | 谱范数 | Muon |
| Stiefel 流形 ⊂ R^(m×n) | 谱范数 | 流形 Muon |

我们将在下一节推导表中的最后一个算法——流形 Muon。要为矩阵参数设计流形约束与距离函数，我们需要仔细思考权重矩阵在神经网络中所扮演的角色。

## 流形 Muon

transformer 中一个典型的权重矩阵 W 是一个「向量乘子」，也就是说，它把输入向量 x 变换为输出向量 y = Wx。我们将设计一个流形约束和一个距离函数，使矩阵以良好的方式作用于输入向量：矩阵不应产生过小或过大的输出，对矩阵的更新也不应让输出向量变化过大或过小。

理解矩阵如何作用于向量的一个好方法是通过[奇异值分解](https://en.wikipedia.org/wiki/Singular_value_decomposition)（SVD），如[图](#fig:svd)所示。SVD 对矩阵的分解方式，能告诉我们矩阵沿不同轴向拉伸输入向量的程度。

![](svgs/svd.svg)

奇异值分解。一个秩为 k 的矩阵 M ∈ R^(m×n) 总是可以分解为 M = UΣVᵀ，其中 U ∈ R^(m×k) 与 V ∈ R^(n×k) 具有正交列，Σ ∈ R^(k×k) 是只含正元素的对角矩阵。Σ 的元素称为 M 的奇异值。奇异值度量了矩阵对与 U、V 相应列对齐的向量的拉伸效应。

我们希望矩阵的拉伸效应接近 1，因此我们将选择一个所有奇异值都恰好为 1 的矩阵流形。这个矩阵流形的正式名称是 [*Stiefel 流形*](https://en.wikipedia.org/wiki/Stiefel_manifold)。我们可以不失一般性地假设处理的是高矩阵（m ≥ n），于是 Stiefel 流形可以等价地定义为如下集合：

Stiefel(m, n) := {W ∈ R^(m×n) | WᵀW = I_n}.

此外，[可以证明](https://cseweb.ucsd.edu/classes/sp24/cse291-e/papers/StiefelManifold/StiefelNotes.pdf)：矩阵 A ∈ R^(m×n) 与 Stiefel 流形在矩阵 W 处相切（注意，Stiefel 约束 WᵀW = I_n 直接推广了上一节的超球面约束 wᵀw = 1；类似地，切空间条件也推广了超球面的条件 aᵀw = 0。），当且仅当：

AᵀW + WᵀA = 0.

要为 Stiefel 流形设计流形优化器，剩下要做的只是选择一个距离函数。为了限制权重更新对输入向量可能产生的最大拉伸效应，我们将选择*谱范数*（spectral norm），它度量矩阵的最大奇异值。虽然这只限制了更新可能产生的最大效应，但由于我们推导出的优化器会让该约束达到饱和（取等），它最终也会防止更新的最小效应过小。（这一说法存在一些例外，例如当权重矩阵的 fan-out 小于 fan-in 时，矩阵及其更新不可避免地存在零空间，会把某些输入映射为零。）

在谱范数约束下做梯度下降的思想，正是 [Muon 优化器](https://jeremybernste.in/writing/deriving-muon)的来源；再与 Stiefel 流形约束相结合，我们得到一个将被称为*流形 Muon*（manifold Muon）的问题：

min_{A∈R^(m×n)}　trace(GᵀA)（损失的线性变化），约束为　‖A‖_spectral ≤ η（尺寸约束）且 AᵀW + WᵀA = 0（切向约束）。　(†)

流形 Muon 问题 (†) 直接推广了上一节的问题 (⋆)。求解 (†) 比求解 (⋆) 更难，这里我们将给出一个数值解，其灵感来自 Jianlin Su 和 Franz Louis Cesista 的工作（去年年底，我[找到了](https://docs.modula.systems/algorithms/manifold/orthogonal/)方阵情形下流形 Muon 的解法，但未能解决完整的矩形情形，于是把它作为开放问题[发布](https://docs.modula.systems/algorithms/manifold/orthogonal/#open-problem-extending-to-the-stiefel-manifold)在 Modula 文档上。今年夏天，Jianlin Su 采用拉格朗日方法并对最优性条件构造不动点迭代，[解决了这个问题](https://kexue.fm/archives/11221)。我看到了 Jianlin 工作的一个早期版本（当时还不能完全用），也看到了 Franz Louis Cesista 的[相关工作](https://leloykun.github.io/ponder/steepest-descent-stiefel/)，由此得到了本文所给出的对偶上升算法。）。

我们的关键洞察是：(†) 是一个凸优化问题，可以用一种称为[*对偶上升*](https://www.cs.cmu.edu/~pradeepr/convexopt/Lecture_Slides/dual-ascent.pdf)（dual ascent）的标准方法求解。这里我们只概述主要思想，更详细的推导可以在[这个页面](https://docs.modula.systems/algorithms/manifold/stiefel/)找到。

与 Jianlin 的方法类似，我们引入一个拉格朗日乘子矩阵 Λ ∈ R^(n×n)。然后我们应用一系列变换，把问题 (†) 从*约束最小化问题*转换为*无约束最大化问题*：

(†) = min_{‖A‖_spectral ≤ η} max_Λ　trace GᵀA + trace Λᵀ(AᵀW + WᵀA)　(1)
　　= min_{‖A‖_spectral ≤ η} max_Λ　trace Aᵀ(G + 2W(Λ + Λᵀ))　(2)
　　= max_Λ min_{‖A‖_spectral ≤ η}　trace Aᵀ(G + 2W(Λ + Λᵀ))　(3)
　　= max_Λ　−η × ‖G + 2W(Λ + Λᵀ)‖_nuclear.　(4)

式 (1) 把问题重述为一个[鞍点问题](https://www-cs.stanford.edu/people/davidknowles/lagrangian_duality.pdf)：每当切空间条件被违反，对 Λ 的最大化都会把目标值推向无穷。式 (2) 由迹的性质得出，式 (3) 由 Sion 极小极大定理得出。式 (3) 中的内层最小化通过设 A_opt(Λ) = −η × msign(G + 2W(Λ + Λᵀ)) 求解，其中 msign 是[矩阵符号函数](https://docs.modula.systems/algorithms/newton-schulz/)（矩阵符号函数把矩阵的奇异值「吸附」到 1。它可以通过 Newton–Schulz 迭代或近期的 [Polar Express](https://arxiv.org/abs/2505.16932) 算法在 GPU 上高效计算。）。把这个表达式代入式 (3) 中的 A_opt(Λ)，便得到式 (4)。式 (4) 被称为 (†) 的「对偶问题」，我们可以用梯度上升来求解它。经过一些推导，对偶函数的梯度为：

H(Λ) := −η × ∇_Λ ‖G + W(Λ + Λᵀ)‖_nuclear = −η × [Wᵀmsign(G + 2W(Λ + Λᵀ)) + msign(G + 2W(Λ + Λᵀ))ᵀW]，

其中核范数 ‖·‖_nuclear 度量矩阵奇异值之和。

最后，我们可以写出流形 Muon 算法（注意，该算法与 [Jianlin Su 的解法](https://kexue.fm/archives/11221)密切相关：在我们运行对偶上升之处，Jianlin 的解法相当于通过不动点迭代求解对偶函数的最大值，即 H(Λ) = 0。）：

1. 对对偶变量运行梯度上升 Λ ← Λ + α × H(Λ)，求解 Λ_opt；
2. 计算更新 A_opt = −η × msign(G + 2W(Λ_opt + Λ_optᵀ))；
3. 将更新应用于权重 W ← W + A_opt；
4. 将权重收缩回流形 W ← msign(W)。

我们做了一个非常小规模的实验来对算法进行健全性检验，并为学生和研究者提供一个可以动手把玩的最小实现。每次训练运行不到一分钟即可完成。代码在[这里](https://github.com/thinking-machines-lab/manifolds/)，实验设置与结果见[图](#fig:cifar10)。

![](svgs/cifar10.svg)

在 CIFAR-10 数据集上训练一个小型 MLP 3 个 epoch。不同的浅蓝色曲线对应 AdamW 的不同权重衰减设置。结果为 3 个随机种子的平均。流形 Muon 优化器获得了比 AdamW 更高的训练与测试准确率。第三幅图展示了最优学习率下第一个权重矩阵最终的奇异值分布：用流形 Muon 训练后的奇异值全都接近 1。与 AdamW 相比，流形 Muon 增加了每步的墙上时间，不过这一点可以通过减少对偶上升的步数、或给算法加入动量并在线运行对偶上升来改进。取决于其他系统瓶颈，这点开销可能并不成问题。

## 模块化流形

到目前为止，本文讨论了针对单个参数张量的流形约束，并为这些约束协同设计了优化逻辑。一个我们尚未回答的问题是：当我们把多层组合成网络时会怎样？我们可以孤立地思考单个层——还是需要小心处理层与层之间的交互，并相应地修改优化逻辑？本节的目标是指出：存在一种方式，可以把前两节引入的推理扩展到整个网络的情形，我们称之为*模块化流形理论*（模块化流形理论建立在我与我的朋友 Tim Large、博后导师 Phillip Isola、博士导师 Yisong Yue 以及许多出色合作者的研究之上。本节末尾我们提供了一些可进一步了解的链接。）。

模块化流形的思想是构建一个抽象，告诉我们如何在各层之间分配学习率。每层内部的实际优化逻辑最终与我们已经推导出的相同，只是每层的学习率会根据该层在网络中出现的位置而被修改。这个抽象建立在我们关于[模块化范数](https://arxiv.org/abs/2405.14813)（modular norm）论文中的一个关键观察之上：分配学习率——无论是跨层分配，还是在放大单个层时——与理解网络输出对权重的 Lipschitz 敏感度紧密相关。这个抽象在构建网络的过程中追踪这一敏感度，而流形约束帮助我们更紧地把握它。

这个抽象的出发点，是把任何神经网络模块——从一层到整个 transformer——看作一个具有三个属性的数学对象：

1. 前向函数 f: W × X → Y，从参数空间 W = R^d 与输入空间 X 映射到输出空间 Y；
2. 权重空间的一个子流形 M ⊂ W，权重被约束在其中；
3. 一个范数 ‖·‖: W → R，充当权重空间上的量尺。

例如，一个配备谱范数、约束在 Stiefel 流形上的线性模块——我们已经为它推导出了优化器——可以写成：

StiefelLinear = { (W, x) ↦ Wx,（前向函数）Stiefel(m, n),（流形）‖·‖_spectral（范数）}

只要输入到 StiefelLinear 模块的 x 具有单位 ℓ₂ 范数，那么 StiefelLinear 在该模块所指派的范数下，对其权重以 Lipschitz 常数 1 满足 Lipschitz 性质（这一论证可以推广到输入上的 RMS 范数与权重上的 RMS–RMS 算子范数。）：

‖(W + ΔW)x − Wx‖₂ ≤ ‖ΔW‖_spectral × ‖x‖₂ = ‖ΔW‖_spectral.

这类 Lipschitz 论断帮助我们理解如何缩放施加给该模块的权重更新，因为它给出了当我们扰动权重时输出最多会变化多少的界。但当我们组合两个模块时，能否自动为新模块的联合权重空间「编译」出一条 Lipschitz 论断？答案是可以，只要我们遵循特殊的规则来构建新模块：

1. 新的前向函数 f₃ 由既有的两个前向函数 f₁ 与 f₂ 复合而成：
   f₃((w₁, w₂), x) := f₂(w₂, f₁(w₁, x)).
2. 新的流形约束 M₃ 就是既有的两个流形 M₁ 与 M₂ 的笛卡尔积（一个有趣的例子见[图](#fig:product-manifold)）：
   M₃ = M₁ × M₂.
3. 新的范数函数是既有的两个范数函数以特殊标量系数 s₁ 与 s₂ 加权后取最大值。设 ‖·‖₁ 表示第一个模块的范数，‖·‖₂ 表示第二个模块的范数，新的范数 ‖·‖₃ 为：
   ‖(w₁, w₂)‖₃ := max(s₁·‖w₁‖₁, s₂·‖w₂‖₂).

当我们用这个复合范数来推导优化器——遵循本文前两节用过的同一套流程——最终会为每一层推导出各自的优化器，而标量系数 sᵢ 负责在各层之间分配学习率。

关于这一构造的更多细节，包括将其扩展到其他组合模块的方式，见我们关于[模块化范数](https://arxiv.org/abs/2405.14813)的论文——不过那篇论文并不涉及流形优化。你也可以参阅我们关于[模块化对偶](https://arxiv.org/abs/2410.21265)（modular duality）的论文，了解在模块化范数下构建优化器的更多内容。[Modula 项目](https://modula.systems)正朝着以程序化方式实现这一构造的方向推进。

![](svgs/product-manifold.svg)

笛卡尔积是把两个流形粘合起来的一种简单方式。例如，一条直线与一个圆盘的乘积是一个圆柱面：直线上的每一点都有一个圆盘的副本。

## 未来工作方向

我们对任何试图让神经网络训练变得像前向传播一样有原理、自动化的研究都感到兴奋。本文中的想法从与 Jianlin Su、Franz Louis Cesista 等外部研究者的交流中获益良多。我们非常乐意看到社区在这些主题上做出更多工作。

一些可能的未来工作方向：

- **模块化。** 注意力头应该「生活」在什么流形上？嵌入（embedding）是否应该与反嵌入（unembedding）采用不同的约束？我们可以在网络的不同部分混搭不同的约束，或者让某些张量不受约束。
- **数值计算。** 流形约束同时也约束了单个权重元素可取的数值范围。这会影响数值计算吗？会让低精度训练更容易吗？
- **凸优化。** 流形 Muon 算法涉及运行对偶上升。我们能否应用更精巧的凸优化技术，来更快、更可靠地求解对偶问题？
- **收敛性分析。** 这些算法收敛有多快？权重矩阵良好的条件数是否有利于收敛？理论上我们还能说出更多东西吗？
- **正则化。** 流形约束会隐式地正则化模型。我们能否设计约束或调整其半径，以改善泛化？
- **架构-优化器协同设计。** 硬流形约束最终未必是约束权重矩阵的正确方式，但它们体现了把优化算法与架构组件深度协同设计的思想。这里还有更多机会吗？
- **非黎曼几何。** 大多数流形优化的工作都处在黎曼世界里：距离由内积诱导，范数球是椭球。但神经网络不同：矩阵作为算子起作用，而谱范数这类算子范数并不来自内积。这意味着，例如，范数球可以带有尖角，而且梯度流并不唯一。在这个非黎曼的世界里，还有更多等待发现的东西吗？
- **实用实现。** 要大规模应用这些技术，需要在 GPU 上高效的流形运算。近期的 [Polar Express](https://arxiv.org/abs/2505.16932) 论文显示了快速矩阵符号计算的前景。我们还需要哪些算法创新？

## 延伸阅读

- **流形优化。** [Absil, Mahony & Sepulchre](https://press.princeton.edu/absil) 的教科书是标准参考。专门针对 Stiefel 流形，可参见 [Edelman et al, 1998](https://math.mit.edu/~edelman/publications/geometry_of_algorithms.pdf)。这些工作都处在黎曼世界中。类似地，大多数考虑 Stiefel 流形上优化的机器学习论文也采取黎曼视角，例子可参见 [Li et al, 2020](https://arxiv.org/abs/2002.01113)、[Kong et al, 2022](https://arxiv.org/abs/2205.14173) 与 [Park et al, 2025](https://arxiv.org/abs/2508.17901)。
- **机器学习中的非黎曼几何。** Thomas Flynn 2017 年关于对偶结构梯度下降（duality structure gradient descent）的[论文](https://arxiv.org/abs/1708.00523)把神经网络权重空间刻画为*芬斯勒流形*（Finsler manifold），即配备了范数的流形，非常值得一读。另见 Jianlin Su 关于 Stiefel Muon 的[近期博客文章](https://kexue.fm/archives/11221)，以及 Franz Louis Cesista 关于 Stiefel 流形上 Muon 启发式解法的[博客文章](https://leloykun.github.io/ponder/steepest-descent-stiefel/)。Franz 还写了一篇[后续博客](https://leloykun.github.io/ponder/steepest-descent-finsler/)，把这里给出的解法做了推广。[Scion 论文](https://arxiv.org/abs/2502.07529)通过凸组合以另一种方式施加权重约束，而 [Carlson et al, 2015](https://papers.nips.cc/paper_files/paper/2015/hash/f50a6c02a3fc5a3a5d4d9391f05f3efc-Abstract.html) 较早地研究了（无约束的）谱下降（spectral descent）。
- **Modula 项目。** Modula 项目的目标是构建一个库，为通用架构自动编译最速下降优化器及相应的 Lipschitz 论断。可访问项目页面 <https://modula.systems>，以及我们关于[模块化范数](https://arxiv.org/abs/2405.14813)与[模块化对偶](https://arxiv.org/abs/2410.21265)的论文。我们的[优化文选](https://arxiv.org/abs/2409.20325)也为进入这一思想空间提供了一条平易近人的路径。
- **Lipschitz 约束深度学习。** 这一主题已有大量工作。例如，可查阅 [Louis Béthune](https://theses.hal.science/tel-04674274v1) 与 [Tsui-Wei Weng](https://dspace.mit.edu/bitstream/handle/1721.1/129313/1227782217-MIT.pdf?sequence=1&isAllowed=y) 的博士论文。这一主题的工作通常不会把权重的 Lipschitz 性与优化器设计联系起来。另见 [Anil et al, 2018](https://arxiv.org/abs/1811.05381) 与我们的论文 [Newhouse et al, 2025](https://arxiv.org/abs/2507.13338)。

## 引用

请按如下方式引用本文：

```
Jeremy Bernstein, "Modular Manifolds",
Thinking Machines Lab: Connectionism, Sep 2025.
```

或使用 BibTeX 引用：

```
@article{bernstein2025manifolds,
  author = {Jeremy Bernstein},
  title = {Modular Manifolds},
  journal = {Thinking Machines Lab: Connectionism},
  year = {2025},
  note = {https://thinkingmachines.ai/blog/modular-manifolds/},
  doi = {10.64434/tml.20250926}
}
```
