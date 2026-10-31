---
title: "IDM：内蕴分布匹配"
title_en: "IDM: Intrinsic Distribution Matching"
arxiv: 2610.39633
date: 2026-10-29
source: https://arxiv.org/abs/2610.39633
project: https://github.com/inclusionAI/IDM
crawled: 2026-10-31
translated: 2026-10-31
---
# IDM：内蕴分布匹配

> 原文：[IDM: Intrinsic Distribution Matching](https://arxiv.org/abs/2610.39633) · InclusionAI · 西湖大学 等 · arXiv

## 摘要

单步与少步文生图在可用的精细化机会有限的情况下，仍须准确渲染提示词中指定的细节。分布匹配蒸馏（distribution matching distillation，DMD）利用分数差把生成分布拉近到参考分布。延续先前工作，我们用生成器内部的两个速度分支估计这一差值，从而避免单独的伪分数网络（fake-score network）。我们提出这样一个问题：显式的矩约束能否改进这种学习出来的分数监督。通过把反向 KL 场分解为一个高斯矩分量与一个非高斯残差分量，我们识别出可以显式约束的统计量。我们提出内蕴分布匹配（Intrinsic Distribution Matching，IDM）：它保留完整的 DMD 校正，并利用生成器的指数滑动平均（EMA）副本匹配特征均值与逐坐标标准差，无需任何外部特征编码器。实验在 Z-Image-Turbo 6B 与 Qwen-Image 20B 上进行全参数与低秩适配（LoRA）微调。在两次网络前向评估（2 NFE）下，IDM 在 LongText-Bench 中文与英文子集上分别达到 94.25% 与 90.20%，是该预算下对比方法中的最高分。受控消融表明新增的矩损失带来提升，且在报告的五项指标上，生成器 EMA 特征与外部 DINOv2 编码器性能相当。代码见[此处](https://github.com/inclusionAI/IDM)。

††脚注：*共同一作。†通讯作者。

## 1 引言

扩散与流匹配模型能够生成高质量图像，但其反复的网络前向评估带来高昂的推理成本（[Ho et al., 2020](#bib.bib12)；[Song et al., 2020](#bib.bib13)；[Lipman et al., 2022](#bib.bib10)；[Liu et al., 2023](#bib.bib9)）。单步与少步生成通过学习一个短得多的采样过程来降低这一成本。其挑战在于：只用一次或几次采样步，仍要准确渲染提示词中指定的细节。长文本渲染让这一挑战变得具体：大量字符必须在一张连贯的图像中保持清晰可辨、准确无误（[Geng et al., 2025b](#bib.bib83)；[Wu et al., 2025a](#bib.bib33)）。因此，它构成一个严苛的测试：快速生成是否仍保留了细粒度的条件信息。

分布匹配蒸馏（DMD）训练一个快速生成器去匹配参考分布（[Yin et al., 2024b](#bib.bib16)；[Yin et al., 2024a](#bib.bib14)）。分数（score）描述对数密度局部增长的方向。一个预训练的教师模型提供参考分数，一个辅助的伪分数网络估计当前生成分布的分数，二者之差引导生成样本的更新。这些更新逐样本施加，但其方向同时依赖于两个分布。分布匹配可以与基于轨迹的训练互补：rCM 将分数正则与连续时间一致性训练相结合（[Zheng et al., 2025](#bib.bib66)）。

图 1：面向单步生成的 IDM 总览。多步采样迭代地精细化样本，而单步生成学习从噪声到数据的直接映射。IDM 将内部 DMD 损失与生成器 EMA 特征空间中的特征矩损失相结合。右面板示意单次前向评估推理下的理想化对齐。

TwinFlow 与 APEX 从生成器内部相互分离的速度分支中获得这一分数差（[Cheng et al., 2025](#bib.bib56)；[Liu et al., 2026a](#bib.bib61)）。模型分数的估计仍是学出来的，但不再需要单独的伪分数网络。我们采用这一内部构造，并进一步追问：生成器能否同时为跨样本的统计量提供显式约束。尽管精确的 DMD 场包含完整的分布信息，学习得到的分数估计与有限训练仍可能留下偏差，而一个额外的统计目标或许有助于缩小这些偏差。

为给这样的约束寻找动机，我们重新审视 DMD 背后的反向 KL 分数差。基于高斯加残差的分数表示（[Wang and Vastola, 2023](#bib.bib79)；[Wang and Vastola, 2024](#bib.bib80)），我们在[第 3.3 节](#S3.SS3)中把由均值与协方差决定的分量从其余分数结构中分离出来。这识别出可以显式约束的统计量，同时也说明了为什么单靠矩并不能确定完整分布。因此，我们保留完整的 DMD 校正并增加一个矩损失，并在共享训练设置下通过受控消融检验其收益。

我们提出内蕴分布匹配（IDM），它在内部 DMD 之上，在生成器自身的特征空间中加入矩匹配。生成器的指数滑动平均（EMA）副本为生成样本与参考样本提供共享表示；我们匹配这些特征的均值与逐坐标标准差。与从外部编码器或教师模型获取特征的目标（[Yang et al., 2026](#bib.bib65)；[Zhang et al., 2026b](#bib.bib67)）不同，这一设计让生成器同时承担分数估计与特征提取。两路训练信号都取自生成器及其 EMA 副本，无需单独的判别器、分数模型或外部特征编码器。

我们在[第 5 节](#S5)中以 Z-Image-Turbo 6B 与 Qwen-Image 20B、在全参数与 LoRA 微调下评测 IDM。LongText-Bench 评测上文强调的中英文长文本渲染保真度，其子集记为 LongText-CN 与 LongText-EN（[Geng et al., 2025b](#bib.bib83)）。在两次网络前向评估（2 NFE）下，IDM（Z-Image）在对比方法中取得最先进成绩：94.25% 与 90.20%，在[表 5](#S5.T5)中分别比 Z-Image-Turbo++ 高出 2.63 与 0.32 个百分点。

我们的主要贡献如下：

1. **内蕴的分布监督**。我们在内部 DMD 之上，对生成器 EMA 特征的均值与逐坐标标准差加入显式损失。这在无需单独外部特征编码器的情况下，补充了跨样本的统计监督。
2. **分布梯度解释**。基于高斯加残差的分数表示，我们为在完整 DMD 校正之外引入显式矩约束给出动机。
3. **少步训练与评测**。我们在 6B 与 20B 骨干上演示全参数与 LoRA 训练。消融评估新增的矩损失、EMA 特征与回归选择，LongText-Bench 评测细粒度文本保真度。

![Refer to caption](2610.39633v1/fig1_merged.png)

图 2：IDM（Z-Image），2 NFE。文本渲染与人像生成。

## 2 背景

**连续生成模型**。扩散与流匹配模型通过反复的网络前向评估把噪声变换为数据（[Ho et al., 2020](#bib.bib12)；[Song et al., 2020](#bib.bib13)；[Lipman et al., 2022](#bib.bib10)）。蒸馏学习一个更短的过程（[Salimans and Ho, 2022](#bib.bib54)；[Song et al., 2023](#bib.bib52)）。我们用 rectified flow 定义生成器，随后说明用于训练它的 DMD 监督。

**Rectified Flow 与少步生成**。令 $p_{z}=\mathcal{N}(\mathbf{0},\mathbf{I}_{d})$ 为噪声分布，$p_{r}$ 为参考数据分布。Rectified flow 使用路径 $\mathbf{x}_{r,t}=(1-t)\mathbf{x}_{r}+t\bm{\epsilon}$，其中 $\mathbf{x}_{r}\sim p_{r}$ 与 $\bm{\epsilon}\sim p_{z}$ 独立采样（[Liu et al., 2023](#bib.bib9)）。于是 $t=0$ 表示干净数据，$t=1$ 表示纯噪声。网络 $\bm{F}_{\theta}(\mathbf{x}_{r,t},t,\mathbf{c})$ 回归对速度（pair velocity）$\bm{\epsilon}-\mathbf{x}_{r}$，其中 $\mathbf{c}\in\mathcal{C}$ 是文本条件向量。在平方误差最优时，它恢复边际速度，即同一加噪输入与条件下对速度的条件平均。少步生成用少量前向欧拉步将该场从 $t=1$ 积分到 $t=0$。在一次网络前向评估下，生成器为 $G_{\theta}(\mathbf{z},\mathbf{c})=\mathbf{z}-\bm{F}_{\theta}(\mathbf{z},1,\mathbf{c})$，$\mathbf{z}\sim p_{z}$。

**分布匹配蒸馏**。生成器诱导分布 $p_{\theta}$。DMD 的目标是通过反向 KL 梯度使其匹配 $p_{r}$（[Wang et al., 2023](#bib.bib74)；[Yin et al., 2024b](#bib.bib16)）。在固定条件与噪声水平 $t\in(0,1)$ 下，令 $p_{\theta,t}$ 与 $p_{r,t}$ 为二者的加噪分布。分数 $\mathbf{s}_{i,t}=\nabla_{\mathbf{x}_{t}}\log p_{i,t}$ 局部指向对数密度增长的方向。在同一加噪模型样本处取值时，$\mathbf{s}_{r,t}-\mathbf{s}_{\theta,t}$ 指向模型对参考密度比更低的方向，见[第 3.1 节](#S3.SS1)。参考分数由一个冻结的预训练教师模型提供。由于生成器只给出样本而没有可解析求解的分数，DMD 在其输出上训练一个单独的*伪分数网络*。该网络估计生成分布；生成器本身产出图像。伪分数估计必须跟上不断变化的生成器。参考分数把样本引向目标支撑所在的区域，而模型分数则刻画生成器当前概率质量的集中位置。二者都进入分布式更新，因此即使去掉单独网络，模型分数仍须被学习。

**分数–速度恒等式**。对独立的 $\mathbf{x}\sim p$ 与 $\bm{\epsilon}\sim p_{z}$，设 $\mathbf{x}_{t}=(1-t)\mathbf{x}+t\bm{\epsilon}$。对 $t\in(0,1)$，分数 $\mathbf{s}_{t}:=\nabla_{\mathbf{x}_{t}}\log p_{t}$ 与边际速度 $\mathbf{v}_{t}^{*}(\mathbf{x}_{t}):=\mathbb{E}[\bm{\epsilon}-\mathbf{x}\mid\mathbf{x}_{t}]$ 满足

$$
\mathbf{s}_{t}(\mathbf{x}_{t})=-\frac{\mathbf{x}_{t}+(1-t)\mathbf{v}_{t}^{*}(\mathbf{x}_{t})}{t}\,.
\tag{1}
$$

于是一个速度估计同时也给出一个分数估计，见[附录 B.3](#A2.SS3)。在同一输入处把两个速度相减，即得一个缩放的分数差。

**内部分数估计**。TwinFlow 与 APEX 用同一个生成器的两个内部相互分离的速度分支来估计参考分数与模型分数（[Cheng et al., 2025](#bib.bib56)；[Liu et al., 2026a](#bib.bib61)）。这去掉了单独的伪分数网络，同时保留模型分数的学习。沿用 APEX，我们在[第 4.1 节](#S4.SS1)中把这一构造用于 DMD。接下来我们考察其目标场所代表的统计量，以从生成器的特征出发为额外监督寻找动机。

## 3 分布梯度视角

DMD 中的分数差定义了改变生成分布的一个方向。把均值与协方差的贡献从其余分数结构中分离出来，可以澄清矩匹配能约束什么、以及为什么仍需要完整的 DMD 校正。

### 3.1 反向 KL 场

单步生成器把 $\mathbf{z}\sim p_{z}$ 映射为 $\mathbf{x}_{\theta}=G_{\theta}(\mathbf{z},\mathbf{c})$，诱导 $p_{\theta}(\cdot\mid\mathbf{c})$；$p_{r}(\cdot\mid\mathbf{c})$ 为参考分布律。这里 $\mathbf{x}$ 是生成器输出表示中的一个样本，条件 $\mathbf{c}$ 独立于 $\mathbf{z}$ 服从 $p_{c}$。对可微的正密度，定义 $\mathbf{s}_{i}(\mathbf{x}\mid\mathbf{c}):=\nabla_{\mathbf{x}}\log p_{i}(\mathbf{x}\mid\mathbf{c})$，$i\in\{r,\theta\}$。在固定 $\mathbf{c}$ 下，反向 KL 为

$$
\mathcal{D}_{\mathrm{KL}}(p_{\theta}\|p_{r})=\int p_{\theta}(\mathbf{x}\mid\mathbf{c})\log\frac{p_{\theta}(\mathbf{x}\mid\mathbf{c})}{p_{r}(\mathbf{x}\mid\mathbf{c})}\,\mathrm{d}\mathbf{x}.
\tag{2}
$$

其在样本空间的分布梯度为

$$
\mathbf{g}_{\mathrm{KL}}(\mathbf{x}\mid\mathbf{c})=\mathbf{s}_{\theta}(\mathbf{x}\mid\mathbf{c})-\mathbf{s}_{r}(\mathbf{x}\mid\mathbf{c}).
\tag{3}
$$

下降方向为 $-\mathbf{g}_{\mathrm{KL}}=\mathbf{s}_{r}-\mathbf{s}_{\theta}$，局部指向模型对参考密度比更低的方向。它随生成分布的变化而变化。对 $p_{\theta,t}$ 与 $p_{r,t}$ 应用同一恒等式得 $\mathbf{g}_{\mathrm{KL},t}=\mathbf{s}_{\theta,t}-\mathbf{s}_{r,t}$，即 DMD 中估计的加噪场。下面我们在[附录 B.1](#A2.SS1)的正则性假设下，对干净分布律陈述这些恒等式；该分解同样适用于每个固定 $t$ 的加噪分布律，只是后者有自己的均值、协方差与分数残差。

图 3：反向 KL 场分解。完整场 $\mathbf{g}_{\mathrm{KL}}=\mathbf{s}_{\theta}-\mathbf{s}_{r}$（左）是高斯矩分量（中）与非高斯残差分量（右）之和。实线等高线为 $p_{i}$，虚线等高线为其矩匹配高斯 $q_{i}$，$i\in\{r,\theta\}$。均值与协方差相等可消除高斯分量，但仍可能留下非零残差。所有场使用相同的评估点与箭头比例。

### 3.2 参数梯度

上面的场规定的是样本更新。为把它与训练联系起来，考虑一个具有可微一阶变分势的差异泛函 $\mathcal{D}(p_{\theta},p_{r})$，该势描述概率质量的重新分布如何改变 $\mathcal{D}$。其空间梯度给出样本更新中使用的场：

$$
\mathbf{g}_{\mathcal{D}}(\mathbf{x}\mid\mathbf{c}):=\nabla_{\mathbf{x}}\frac{\delta\mathcal{D}(p_{\theta},p_{r})}{\delta p_{\theta}}(\mathbf{x}\mid\mathbf{c}).
\tag{4}
$$

在[附录 B.1](#A2.SS1)的假设下，

$$
\nabla_{\theta}\mathcal{D}(p_{\theta},p_{r})={\mathbb{E}}_{\mathbf{z}\sim p_{z}}\left[\underbrace{[J_{\theta}G_{\theta}(\mathbf{z},\mathbf{c})]^{\top}}_{\text{Jacobian 转置}}\underbrace{\mathbf{g}_{\mathcal{D}}(G_{\theta}(\mathbf{z},\mathbf{c})\mid\mathbf{c})}_{\text{分布梯度}}\right]\,.
\tag{5}
$$

其中 $J_{\theta}G_{\theta}:=\partial G_{\theta}/\partial\theta$；反向传播施加其转置，训练再对 $\mathbf{c}$ 取平均。对反向 KL，一阶变分为 $\log(p_{\theta}/p_{r})+1$，由此回到式 (3)。因此，分数差给出的正是穿过生成器回传的分布式方向。这把"降低差异的分布变化"与"实现该变化的参数更新"分离开来。下面的分解只涉及前者，不依赖特定的生成器结构。

### 3.3 反向 KL 场的分解

为识别该场包含哪些统计量，令 $p$ 为光滑正密度，具有有限二阶矩、均值 $\mu_{p}$ 与正定协方差 $\Sigma_{p}$。其矩匹配高斯为 $q_{p}:=\mathcal{N}(\mu_{p},\Sigma_{p})$，分数为 $\mathbf{s}_{q_{p}}(\mathbf{x})=-\Sigma_{p}^{-1}(\mathbf{x}-\mu_{p})$。$p$ 的分数可精确分解为

$$
\mathbf{s}_{p}(\mathbf{x})=\underbrace{\mathbf{s}_{q_{p}}(\mathbf{x})}_{=-\Sigma_{p}^{-1}(\mathbf{x}-\mu_{p})}+\underbrace{\bm{\eta}_{p}(\mathbf{x})}_{\text{非高斯分数残差}}\,,
\tag{6}
$$

其中 $\bm{\eta}_{p}:=\mathbf{s}_{p}-\mathbf{s}_{q_{p}}$ 收集该高斯近似之外的分数结构（[Wang and Vastola, 2023](#bib.bib79)；[Wang and Vastola, 2024](#bib.bib80)）。在固定 $\mathbf{c}$ 下，对条件分布律 $p_{i}(\cdot\mid\mathbf{c})$ 记 $q_{i}:=q_{p_{i}}$、$\bm{\eta}_{i}:=\bm{\eta}_{p_{i}}$，$i\in\{r,\theta\}$。将二者的分解相减得

$$
\mathbf{g}_{\mathrm{KL}}(\mathbf{x}\mid\mathbf{c})=\underbrace{\left(\mathbf{s}_{q_{\theta}}(\mathbf{x}\mid\mathbf{c})-\mathbf{s}_{q_{r}}(\mathbf{x}\mid\mathbf{c})\right)}_{\mathbf{g}_{\mathrm{KL}}^{\mathrm{G}}:\;\text{高斯矩分量}}+\underbrace{\left(\bm{\eta}_{\theta}(\mathbf{x}\mid\mathbf{c})-\bm{\eta}_{r}(\mathbf{x}\mid\mathbf{c})\right)}_{\mathbf{g}_{\mathrm{KL}}^{\mathrm{nG}}:\;\text{非高斯残差分量}}.
\tag{7}
$$

高斯分量只依赖均值与协方差。两个分布可以共享这些矩却形状不同，从而留下非零残差，见图 3。把 $p_{i}$ 换成 $p_{i,t}$，即得 DMD 所用加噪场的同样分解。

在[附录 B.2.2](#A2.SS2.SSS2)的可积性与边界条件下，

$$
\mathbb{E}_{p}[\bm{\eta}_{p}(\mathbf{x})]=\mathbf{0},\qquad\mathbb{E}_{p}[\bm{\eta}_{p}(\mathbf{x})\mathbf{x}^{\top}]=\mathbf{0}_{d\times d}.
\tag{8}
$$

每个分数残差在自身分布下与常数函数和线性函数正交；二者之差在任一分布下都未必正交。矩匹配高斯仅用于分析分数；并不假设生成样本服从高斯分布。残差并不对应某个单一的高阶矩：它收集的是减去对应分布的高斯分数后剩余的全部分数结构。

**对训练的启示**。精确的 DMD 已同时包含两个分量。实践中，学习得到的分数估计与有限训练未必能让所有统计量精确对齐。该分解指出矩是可以显式约束的量，而残差则解释了为什么只做矩匹配并不足够。因此，我们保留完整的 DMD 校正，并对特征均值与标准差额外施加损失。来自生成器 EMA 副本的特征提供了共享表示，且无需引入外部编码器。这是一个由该分解启发的、特征空间中的附加目标，而不是对其样本空间高斯分量或残差分量的单独估计。[第 5.3 节](#S5.SS3)的消融检验这一显式约束是否改进生成。

## 4 内蕴分布匹配

内蕴分布匹配（IDM）保留内部 DMD 监督，并加入[第 3.3 节](#S3.SS3)导出动机的特征矩约束。DMD 损失 $\mathcal{L}_{\text{score}}$ 使用完整的内部分数差估计；$\mathcal{L}_{\text{pop}}$ 显式匹配生成器 EMA 特征的统计量。我们首先定义 DMD 校正如何监督速度与端点预测，然后描述特征约束、经验矩估计，以及联合训练中使用的梯度。

### 4.1 DMD 损失

在固定条件 $\mathbf{c}$ 下，令 $p_{r,t}$ 与 $p_{\theta,t}$ 表示[第 2 节](#S2)线性加噪构造下的参考与模型边际，其分数为 $\mathbf{s}_{r,t},\mathbf{s}_{\theta,t}$，精确边际速度为 $\mathbf{v}^{*}_{r,t},\mathbf{v}^{*}_{\theta,t}$。在同一点 $\mathbf{x}_{t}$ 对二者应用式 (1)，得 $t\in(0,1)$：

$$
\mathbf{d}_{t}^{*}(\mathbf{x}_{t}):=\mathbf{v}^{*}_{\theta,t}(\mathbf{x}_{t})-\mathbf{v}^{*}_{r,t}(\mathbf{x}_{t})=\frac{t}{1-t}\left(\mathbf{s}_{r,t}(\mathbf{x}_{t})-\mathbf{s}_{\theta,t}(\mathbf{x}_{t})\right)\!,
\tag{9}
$$

于是 $\mathbf{g}_{\mathrm{KL},t}:=\mathbf{s}_{\theta,t}-\mathbf{s}_{r,t}=-\frac{1-t}{t}\,\mathbf{d}_{t}^{*}$，即式 (3) 在这些加噪边际上的反向 KL 场。

**内部速度分支**。沿用 APEX（[Liu et al., 2026a](#bib.bib61)），我们通过取条件向量的相反数来分离参考与模型速度分支：

$$
\widehat{\mathbf{v}}_{r,t}(\mathbf{x}_{t}\mid\mathbf{c}):=\bm{F}_{\theta}(\mathbf{x}_{t},t,\mathbf{c}),\qquad\widehat{\mathbf{v}}_{\theta,t}(\mathbf{x}_{t}\mid\mathbf{c}):=\bm{F}_{\theta}(\mathbf{x}_{t},t,-\mathbf{c}),
\tag{10}
$$

其中 $-\mathbf{c}$ 为条件 $\mathbf{c}$ 选择模型分支，而 $\widehat{\mathbf{d}}_{t}(\mathbf{x}_{t}\mid\mathbf{c}):=\widehat{\mathbf{v}}_{\theta,t}(\mathbf{x}_{t}\mid\mathbf{c})-\widehat{\mathbf{v}}_{r,t}(\mathbf{x}_{t}\mid\mathbf{c})$ 为二者的逐点差。这一解释要求两个分支都近似其边际速度。

**速度与端点回归**。同一 DMD 校正既可以监督速度预测，也可以监督其对应的干净样本端点。我们在[第 5.3 节](#S5.SS3)比较这些回归形式及其组合，以选择训练配置。

对固定输入 $\mathbf{x}_{t}$ 与时刻 $t\in(0,1]$，端点预测为 $\widehat{\mathbf{x}}_{0}(\mathbf{x}_{t},t,\mathbf{c}):=\mathbf{x}_{t}-t\bm{F}_{\theta}(\mathbf{x}_{t},t,\mathbf{c})$。在 $t=1$、$\mathbf{x}_{t}=\mathbf{z}$ 时它等于 $G_{\theta}(\mathbf{z},\mathbf{c})$；中间时刻的预测不必服从单步输出分布 $p_{\theta}$。记 $\operatorname{sg}$ 为 stop-gradient。令 $\widehat{\mathbf{x}}_{0}^{\operatorname{sg}}:=\operatorname{sg}(\widehat{\mathbf{x}}_{0}(\mathbf{x}_{t},t,\mathbf{c}))$，并将其重新加噪为 $\widehat{\mathbf{x}}_{0,t^{\prime}}^{\operatorname{sg}}:=(1-t^{\prime})\widehat{\mathbf{x}}_{0}^{\operatorname{sg}}+t^{\prime}\bm{\epsilon}$，其中重加噪时刻 $t^{\prime}\in(0,1)$ 与 $\bm{\epsilon}\sim p_{z}$ 相互独立地采样，且都独立于回归输入。在该重加噪预测处求分支差 $\widehat{\mathbf{d}}_{t^{\prime}}(\widehat{\mathbf{x}}_{0,t^{\prime}}^{\operatorname{sg}}\mid\mathbf{c})$。其加权、归一化后的值经 detach 得到 $\widehat{\mathbf{d}}_{t^{\prime}}^{\mathrm{DMD}}$；若不做这些处理，校正量即为 $\operatorname{sg}\!\left(\widehat{\mathbf{d}}_{t^{\prime}}(\widehat{\mathbf{x}}_{0,t^{\prime}}^{\operatorname{sg}}\mid\mathbf{c})\right)$。DMD 目标为

$$
\begin{aligned}
\mathbf{v}_{t}^{\mathrm{DMD}} &:=\operatorname{sg}\!\left(\bm{F}_{\theta}(\mathbf{x}_{t},t,\mathbf{c})-\widehat{\mathbf{d}}_{t^{\prime}}^{\mathrm{DMD}}\right),\\
\mathbf{x}_{0}^{\mathrm{DMD}} &:=\operatorname{sg}\!\left(\mathbf{x}_{t}-t\mathbf{v}_{t}^{\mathrm{DMD}}\right).
\end{aligned}
\tag{11}
$$

从速度目标中减去该校正，等价于向 detach 的干净样本预测加上 $t\widehat{\mathbf{d}}_{t^{\prime}}^{\mathrm{DMD}}$。因此，同一校正定义了两个目标。两个目标均 detach 的组合平方回归损失对条件、回归输入与时刻以及重加噪抽取取平均：

$$
\mathcal{L}_{\text{score}}(\theta):=\mathbb{E}\!\left[\underbrace{\|\bm{F}_{\theta}(\mathbf{x}_{t},t,\mathbf{c})-\mathbf{v}_{t}^{\mathrm{DMD}}\|_{2}^{2}}_{\ell_{v}(t)}+\underbrace{\|\widehat{\mathbf{x}}_{0}(\mathbf{x}_{t},t,\mathbf{c})-\mathbf{x}_{0}^{\mathrm{DMD}}\|_{2}^{2}}_{\ell_{x}(t)}\right].
\tag{12}
$$

在固定 $(\mathbf{x}_{t},t)$ 下，这两个平方损失满足 $\ell_{x}(t)=t^{2}\ell_{v}(t)$，因此等权相当于给速度回归一个有效因子 $1+t^{2}$，见[附录 B.4](#A2.SS4)。关于条件均值回归与协方差的进一步讨论见[附录 B.7](#A2.SS7)。

图 4：IDM 的内蕴损失。上：DMD 损失——对预测的干净样本重加噪，用内部速度差为式 (12) 的 $\mathcal{L}_{\text{score}}$ 构造 detach 的速度与端点目标。下：特征矩损失——用当前模型特征与 detach 的模型/参考队列 $\mathcal{Q}_{\theta},\mathcal{Q}_{r}$，按式 (13) 匹配 EMA 特征 $\mathbf{h}_{i}:=\phi_{\bar{\theta}}(\mathbf{x}_{i},\mathbf{c})$ 的均值与逐坐标标准差。省略基础目标。

### 4.2 特征矩损失

在学习得到的 DMD 校正之外，我们在生成器 EMA 副本的特征空间中比较生成样本与参考样本。EMA 提供表示，参考样本提供矩匹配的目标统计量。

**内蕴特征映射**。$\phi:=\phi_{\bar{\theta}}:\mathbb{R}^{d}\times\mathcal{C}\to\mathbb{R}^{d_{\phi}}$ 对生成器 EMA 副本最后一层的隐藏激活做均值池化，为每个样本得到一个特征向量。生成样本与参考样本均在高噪声水平下按[第 2 节](#S2)的加噪构造取用，$\phi$ 中省略加噪参数。这里 $\bar{\theta}$ 表示 EMA 参数，$d_{\phi}$ 为特征维度；每次更新固定 $\bar{\theta}$，但保留对输入的导数。我们在[第 5.3 节](#S5.SS3)将该选择与冻结编码器（[Yang et al., 2026](#bib.bib65)）、教师模型特征（[Zhang et al., 2026b](#bib.bib67)）以及实时自身特征等替代方案比较。

**匹配特征矩**。令 $\mu_{i}^{\phi}$ 与 $\nu_{i,j}^{\phi}$ 表示联合分布 $(\mathbf{x},\mathbf{c})\sim p_{i}(\cdot\mid\mathbf{c})p_{c}$ 下 $\phi(\mathbf{x},\mathbf{c})$ 的均值与逐坐标方差（同时对特征提取噪声取平均），$i\in\{r,\theta\}$。这些统计量跨条件池化，而非匹配条件分布。我们用

$$
\mathcal{L}_{\text{pop}}=\|\mu_{\theta}^{\phi}-\mu_{r}^{\phi}\|_{2}^{2}+\sum_{j=1}^{d_{\phi}}\left(\sqrt{\nu_{\theta,j}^{\phi}}-\sqrt{\nu_{r,j}^{\phi}}\right)^{2}\!.
\tag{13}
$$

匹配这些池化统计量。这是对角高斯 $\mathcal{N}(\mu_{i}^{\phi},\operatorname{diag}(\nu_{i}^{\phi}))$ 之间 2-Wasserstein 距离的平方；它非负，且当且仅当二者的特征均值与逐坐标标准差匹配时为零。在特征层面，均值项把平均值拉向参考均值，标准差项则调整围绕该平均值的散布。这些角色在[命题 B.20](#A2.Thmtheorem20)的经验梯度中是显式的。它们对图像的作用经由固定的 EMA 特征 Jacobian 与生成器传递，因此该目标并不规定逐像素的校正。非线性特征映射可以刻画原始样本均值与协方差无法确定的性质，因此匹配其矩就在一个学习到的表示中约束了统计量。该损失仍只使用池化的特征均值与逐坐标标准差；它既不估计样本空间的高斯分量，也不匹配完整的特征分布。

队列 $\mathcal{Q}_{\theta}$ 与 $\mathcal{Q}_{r}$ 分别最多存储 $K=16384$ 条 detach 的模型特征与参考特征。模型矩把 $B$ 条当前 batch 特征与 $\mathcal{Q}_{\theta}$ 合并计算；参考矩使用 $\mathcal{Q}_{r}$，队列满时分别有 $B+K$ 与 $K$ 条特征。由这些矩定义 $\widehat{\mathcal{L}}_{\text{pop}}$。队列条目来自更早的模型与 EMA 状态，因此这些矩近似当前的总体统计量。[命题 B.20](#A2.Thmtheorem20)在固定队列下给出经验损失的精确梯度，见[附录 B.6](#A2.SS6)。

### 4.3 训练目标

我们使用 RCGM 损失（[Sun and Lin, 2025](#bib.bib59)）——它通过递归一致速度场估计跨时间区间监督生成——作为 $\mathcal{L}_{\text{base}}$。主生成器目标为

$$
\mathcal{L}_{\text{IDM}}(\theta)=\mathcal{L}_{\text{base}}(\theta)+\lambda_{\text{score}}\mathcal{L}_{\text{score}}(\theta)+\lambda_{\text{pop}}\widehat{\mathcal{L}}_{\text{pop}}.
\tag{14}
$$

每次迭代生成当前样本并提取其高噪 EMA 特征。当前特征保留计算图，与 detach 的队列合并以计算 $\widehat{\mathcal{L}}_{\text{pop}}$。其梯度穿过固定的 EMA 网络传到当前样本与生成器；排队特征不接收梯度。跨迭代地，我们用 detach 的特征刷新队列，并按 $\bar{\theta}\leftarrow 0.99\bar{\theta}+0.01\theta$ 更新 EMA。权重 $\lambda_{\text{score}}$ 与 $\lambda_{\text{pop}}$ 在[第 5.1 节](#S5.SS1)中保持固定。特征提取与队列仅在训练时使用。冻结 EMA 参数并不会冻结当前特征：其取值随生成图像变化。若把这些特征也 detach，矩损失对生成器的梯度亦随之消失。detach 的队列提供历史统计量，而不保留先前迭代的计算图。辅助流匹配 $\mathcal{L}_{\text{fake}}$ 在 detach 的生成样本上训练内部模型速度分支，同时也会更新共享参数，见[附录 B.5](#A2.SS5)。单步推理一次前向生成 $\mathbf{x}_{\theta}=G_{\theta}(\mathbf{z},\mathbf{c})$；同一 checkpoint 也支持少步采样。

## 5 实验

我们的实验评估三件事：$\mathcal{L}_{\text{pop}}$ 相对内部 DMD 的附加价值、生成器 EMA 特征相对外部编码器的适用性，以及速度与端点回归的选择。系统级对比评估完整训练设置；受控消融则在共享的数据、骨干与采样预算下考察这些单项选择。本节中，$\mathcal{L}_{\text{pop}}$ 均指经验损失 $\widehat{\mathcal{L}}_{\text{pop}}$。

表 1：效率与质量的系统级对比。速度在单张 A100（BF16）上测得。吞吐量为样本/秒（batch=10）；延迟为秒（batch=1）。GenEval 衡量组合式提示词遵循；FID/CLIP 补充效率对比。LongText 结果见[表 5](#S5.T5)。† 表示不同 NFE 需要不同模型。‡ 标记非规范工作点或次级对比来源。§ 表示 LoRA 权重已并入基座权重后再计时。参数量（Params）：骨干规模（十亿）；LoRA 条目额外给出秩 $r$ 与可训练参数量（括号内）。蓝色/红色的骨干参数量分别表示全参/LoRA 微调。

| 方法 | NFE | 吞吐量（样本/秒） | 延迟（秒） | 参数量（B） | FID ↓ | CLIP ↑ | GenEval ↑ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **少步生成模型** | | | | | | | |
| SDXL-LCM（[Luo et al. (2023)](#bib.bib21)） | 2 | 2.89 | 0.40 | 0.9 | 18.11 | 27.51 | 0.44 |
| PixArt-LCM（[Chen et al. (2024c)](#bib.bib22)） | 2 | 3.52 | 0.31 | 0.6 | 10.33 | 27.24 | 0.42 |
| SD3.5-Turbo（[Esser et al., 2024](#bib.bib1)）‡ | 2 | 1.61 | 0.68 | 8.0 | 51.47 | 25.59 | 0.53 |
| PCM（[Wang et al. (2024a)](#bib.bib20)）† | 2 | 2.62 | 0.56 | 0.9 | 14.70 | 27.66 | 0.55 |
| SDXL-DMD2（[Yin et al. (2024a)](#bib.bib14)）† | 2 | 2.89 | 0.40 | 0.9 | 7.61 | 28.87 | 0.58 |
| FLUX-schnell（[Labs, 2024](#bib.bib18)） | 2 | 0.92 | 1.15 | 12.0 | 7.75 | 28.25 | 0.71 |
| Sana-Sprint（[Chen et al., 2025b](#bib.bib15)） | 2 | 6.46 | 0.25 | 0.6 | 6.54 | 28.40 | 0.76 |
| Sana-Sprint（[Chen et al., 2025b](#bib.bib15)） | 2 | 5.68 | 0.24 | 1.6 | 6.50 | 28.45 | 0.77 |
| Qwen-Image-Lightning（[ModelTC, 2025](#bib.bib38)）‡ | 2 | 3.15 | 0.48 | 20.0 (r=64,0.4)§ | 6.76 | 28.37 | 0.85 |
| TwinFlow (Qwen-Image)（[Cheng et al., 2025](#bib.bib56)） | 2 | 3.15 | 0.48 | 20.0 (r=64,0.4)§ | – | – | 0.87 |
| APEX (Qwen-Image)（[Liu et al., 2026a](#bib.bib61)） | 2 | 3.21 | 0.49 | 20.0 (r=32,0.2)§ | 6.72 | 28.71 | 0.87 |
| APEX (Qwen-Image)（[Liu et al., 2026a](#bib.bib61)） | 2 | 3.17 | 0.47 | 20.0 (r=64,0.4)§ | 6.51 | 28.42 | 0.89 |
| APEX (Qwen-Image)（[Liu et al., 2026a](#bib.bib61)） | 2 | 3.30 | 0.45 | 20.0 | 6.44 | 28.51 | 0.90 |
| IDM (Z-Image) | 2 | 5.18 | 0.30 | 6.0 (r=32,0.2)§ | 6.98 | 28.41 | 0.76 |
| IDM (Z-Image) | 2 | 5.18 | 0.30 | 6.0 (r=64,0.4)§ | 6.79 | 28.13 | 0.77 |
| IDM (Z-Image) | 2 | 5.18 | 0.30 | 6.0 | 6.71 | 28.22 | 0.78 |
| IDM (Qwen-Image) | 2 | 3.28 | 0.44 | 20.0 (r=32,0.2)§ | 6.62 | 28.76 | 0.89 |
| IDM (Qwen-Image) | 2 | 3.28 | 0.44 | 20.0 (r=64,0.4)§ | 6.41 | 28.47 | 0.90 |
| IDM (Qwen-Image) | 2 | 3.28 | 0.44 | 20.0 | 6.34 | 28.56 | 0.91 |
| SDXL-LCM（[Luo et al. (2023)](#bib.bib21)） | 1 | 3.36 | 0.32 | 0.9 | 50.51 | 24.45 | 0.28 |
| PixArt-LCM（[Chen et al. (2024c)](#bib.bib22)） | 1 | 4.26 | 0.25 | 0.6 | 73.35 | 23.99 | 0.41 |
| PixArt-DMD（[Chen et al., 2024b](#bib.bib19)；[Yin et al., 2024b](#bib.bib16)）† | 1 | 4.26 | 0.25 | 0.6 | 9.59 | 26.98 | 0.45 |
| SD3.5-Turbo（[Esser et al., 2024](#bib.bib1)）‡ | 1 | 2.48 | 0.45 | 8.0 | 52.40 | 25.40 | 0.51 |
| PCM（[Wang et al. (2024a)](#bib.bib20)）† | 1 | 3.16 | 0.40 | 0.9 | 30.11 | 26.47 | 0.42 |
| SDXL-DMD2（[Yin et al. (2024a)](#bib.bib14)）† | 1 | 3.36 | 0.32 | 0.9 | 7.10 | 28.93 | 0.59 |
| FLUX-schnell（[Labs, 2024](#bib.bib18)） | 1 | 1.58 | 0.68 | 12.0 | 7.26 | 28.49 | 0.69 |
| Sana-Sprint（[Chen et al., 2025b](#bib.bib15)） | 1 | 7.22 | 0.21 | 0.6 | 7.04 | 28.04 | 0.72 |
| Sana-Sprint（[Chen et al., 2025b](#bib.bib15)） | 1 | 6.71 | 0.21 | 1.6 | 7.69 | 28.27 | 0.76 |
| Qwen-Image-Lightning（[ModelTC, 2025](#bib.bib38)）‡ | 1 | 3.29 | 0.40 | 20.0 (r=64,0.4)§ | 7.06 | 28.35 | 0.85 |
| TwinFlow (Qwen-Image)（[Cheng et al., 2025](#bib.bib56)） | 1 | 3.29 | 0.40 | 20.0 (r=64,0.4)§ | – | – | 0.86 |
| APEX (Qwen-Image)（[Liu et al., 2026a](#bib.bib61)） | 1 | 3.29 | 0.39 | 20.0 (r=32,0.2)§ | 7.22 | 28.62 | 0.88 |
| APEX (Qwen-Image)（[Liu et al., 2026a](#bib.bib61)） | 1 | 3.27 | 0.39 | 20.0 (r=64,0.4)§ | 7.14 | 28.45 | 0.89 |
| APEX (Qwen-Image)（[Liu et al., 2026a](#bib.bib61)） | 1 | 3.50 | 0.34 | 20.0 | 6.87 | 28.66 | 0.89 |
| IDM (Z-Image) | 1 | 5.41 | 0.25 | 6.0 (r=32,0.2)§ | 7.49 | 28.33 | 0.75 |
| IDM (Z-Image) | 1 | 5.41 | 0.25 | 6.0 (r=64,0.4)§ | 7.40 | 28.16 | 0.76 |
| IDM (Z-Image) | 1 | 5.41 | 0.25 | 6.0 | 7.13 | 28.37 | 0.77 |
| IDM (Qwen-Image) | 1 | 3.44 | 0.35 | 20.0 (r=32,0.2)§ | 7.12 | 28.67 | 0.88 |
| IDM (Qwen-Image) | 1 | 3.44 | 0.35 | 20.0 (r=64,0.4)§ | 7.04 | 28.50 | 0.89 |
| IDM (Qwen-Image) | 1 | 3.44 | 0.35 | 20.0 | 6.77 | 28.71 | 0.90 |

### 5.1 实验设置

**骨干与微调**。我们从 Z-Image-Turbo 6B（[Team, 2025](#bib.bib49)）与 Qwen-Image 20B（[Wu et al., 2025a](#bib.bib33)）初始化 IDM，使用全参数微调以及秩为 32 与 64 的 LoRA。我们把所得模型记为 IDM（Z-Image）与 IDM（Qwen-Image）；前者使用 Turbo checkpoint，而非未蒸馏的 Z-Image 基座模型。

**训练数据**。定义 $p_{r}$ 的参考数据由 ShareGPT-4o（[Chen et al., 2025c](#bib.bib41)）、BLIP-3o（[Chen et al., 2025a](#bib.bib40)）以及用 Qwen-Image-2512 与 Z-Image-Turbo 合成的样本组成：60 万条来自 FLUX-Reason-6M 提示词（[Fang et al., 2025](#bib.bib48)），500 万条来自文本渲染提示词。与 APEX 所用的 20 万条海报提示词样本（[Liu et al., 2026a](#bib.bib61)）相比，这一更大的文本导向集合为密集文本渲染提供了更多训练样例。

**训练配置**。所有模型使用 BF16、FlashAttention4 与 FSDP2，全局 batch size 为 64。Z-Image-Turbo 6B 训练 15K 步，Qwen-Image 20B LoRA 训练 10K 步，分别使用 32×H100 80GB 与 8×A100 80GB GPU。默认权重为 $\lambda_{\text{score}}=1$ 与 $\lambda_{\text{pop}}=0.5$，训练全程固定。每个训练好的 checkpoint 都在 1 与 2 NFE 下评测，不针对任一采样预算修改训练损失权重。

**评测**。我们沿用与 APEX 对比相同的标准基准协议，按各方法声明的 NFE 预算报告结果。已发表的参考结果保留其训练数据与配置；IDM 内部消融使用上述共享配置。我们用 GenEval（[Ghosh et al., 2023](#bib.bib36)）评测组合式提示词遵循，在 MJHQ-30K（[Li et al., 2024a](#bib.bib35)）上计算 FID 与 CLIP score，用 DPG-Bench（[Hu et al., 2024](#bib.bib37)）评测细粒度提示词遵循，用 WISE（[Niu et al., 2025](#bib.bib45)）评测世界知识。Z-Image 对比与消融另报告 OneIG（[Chang et al., 2026](#bib.bib82)）与 LongText-Bench（[Geng et al., 2025b](#bib.bib83)）；LongText-CN 与 LongText-EN 分别评测中英文长文本渲染。

### 5.2 主对比

**长文本渲染**。在 2 NFE 下，IDM（Z-Image）在 LongText-CN 上取得 94.25%、LongText-EN 上取得 90.20%，是该预算下对比方法中的最高分，见[表 5](#S5.T5)。这分别比 Z-Image-Turbo++ 高 2.63 与 0.32 个百分点，比 APEX 高 3.87 与 1.44 个百分点。这直接支持了上文提出的细粒度文本渲染目标。该表把外部对比与受控消融放在一起，便于逐项考察每个损失的贡献。

**整体质量与效率**。在全参数微调下，IDM 在 2 NFE 时于 Z-Image 上取得 GenEval 0.78、于 Qwen-Image 上取得 0.91，见[表 1](#S5.T1)。在同一 NFE 与微调设置下的 Qwen-Image 上，APEX 为 0.90；FID 上 IDM 为 6.34、APEX 为 6.44，延迟分别为 0.44 与 0.45 秒。因此，质量提升的代价只是可比的采样延迟。在 1 NFE 下，Qwen-Image IDM 以每样本 0.35 秒达到 0.90 GenEval，用同一训练 checkpoint 提供更快的采样选项。

同一全参数 checkpoint 在两个骨干上都从 1 NFE 提升到 2 NFE：Z-Image 的 FID 从 7.13 降至 6.71，Qwen-Image 的 FID 从 6.77 降至 6.34，GenEval 各提升 0.01。因此，当采样预算允许一次额外的网络前向评估时，所学目标仍然有用。在秩 64 LoRA 下，Qwen-Image IDM 训练 0.4B 参数并在 2 NFE 达到 0.90 GenEval，而全参数微调为 0.91。该设置在只更新很少参数的情况下保留了大部分组合式性能。DPG-Bench 与 WISE 为提示词遵循与世界知识提供互补评测。[图 6](#S5.F6)给出跨采样预算的定性对比。

[表 2](#S5.T2)、[表 3](#S5.T3)与[表 4](#S5.T4)给出 GenEval、WISE 与 DPG-Bench 的分类别结果。

表 2：GenEval 定量评测。各模型标签中标注了 NFE，给出该预算下的分类别与总体分；未标注的已发表基线使用其报告的默认采样预算。Z-Image 为基座模型（~100 NFE），Z-Image-Turbo 为 8-NFE 蒸馏模型。

| 模型 | 单物体 | 双物体 | 计数 | 颜色 | 位置 | 属性绑定 | 总体↑ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Show-o（[Xie et al., 2024](#bib.bib23)） | 0.95 | 0.52 | 0.49 | 0.82 | 0.11 | 0.28 | 0.53 |
| Emu3-Gen（[Wang et al., 2024b](#bib.bib24)） | 0.98 | 0.71 | 0.34 | 0.81 | 0.17 | 0.21 | 0.54 |
| PixArt-α（[Chen et al., 2024d](#bib.bib25)） | 0.98 | 0.50 | 0.44 | 0.80 | 0.08 | 0.07 | 0.48 |
| SD3 Medium（[Esser et al., 2024](#bib.bib1)） | 0.98 | 0.74 | 0.63 | 0.67 | 0.34 | 0.36 | 0.62 |
| FLUX.1 [Dev]（[BlackForest, 2024](#bib.bib26)） | 0.98 | 0.81 | 0.74 | 0.79 | 0.22 | 0.45 | 0.66 |
| SD3.5 Large（[Esser et al., 2024](#bib.bib1)）‡ | 0.98 | 0.89 | 0.73 | 0.83 | 0.34 | 0.47 | 0.71 |
| JanusFlow（[Ma et al., 2025](#bib.bib27)） | 0.97 | 0.59 | 0.45 | 0.83 | 0.53 | 0.42 | 0.63 |
| Lumina-Image 2.0（[Qin et al., 2025](#bib.bib28)） | - | 0.87 | 0.67 | - | - | 0.62 | 0.73 |
| Janus-Pro-7B（[Chen et al., 2025d](#bib.bib29)） | 0.99 | 0.89 | 0.59 | 0.90 | 0.79 | 0.66 | 0.80 |
| HiDream-I1-Full（[Cai et al., 2025](#bib.bib30)） | 1.00 | 0.98 | 0.79 | 0.91 | 0.60 | 0.72 | 0.83 |
| GPT Image 1 [High]（[OpenAI, 2025](#bib.bib31)） | 0.99 | 0.92 | 0.85 | 0.92 | 0.75 | 0.61 | 0.84 |
| Seedream 3.0（[Gao et al., 2025](#bib.bib32)） | 0.99 | 0.96 | 0.91 | 0.93 | 0.47 | 0.80 | 0.84 |
| BAGEL（[Deng et al., 2025](#bib.bib44)） | 0.98 | 0.95 | 0.84 | 0.95 | 0.78 | 0.77 | 0.88 |
| Qwen-Image（[Wu et al., 2025a](#bib.bib33)） | 0.99 | 0.92 | 0.89 | 0.88 | 0.76 | 0.77 | 0.87 |
| Hyper-BAGEL（[Lu et al., 2025](#bib.bib43)） | 0.97 | 0.86 | 0.75 | 0.90 | 0.67 | 0.62 | 0.80 |
| Qwen-Image-Lightning（[ModelTC, 2025](#bib.bib38)；[Liu et al., 2026a](#bib.bib61)）‡ | 0.99 | 0.89 | 0.85 | 0.87 | 0.75 | 0.76 | 0.85 |
| Z-Image（[Team, 2025](#bib.bib49)）（基座；~100 NFE） | 1.00 | 0.94 | 0.78 | 0.93 | 0.62 | 0.77 | 0.84 |
| Z-Image-Turbo（[Team, 2025](#bib.bib49)；[Liu et al., 2026b](#bib.bib50)） | 1.00 | 0.89 | 0.72 | 0.85 | 0.46 | 0.59 | 0.75 |
| DMD2（[Yin et al., 2024a](#bib.bib14)；[Liu et al., 2026b](#bib.bib50)）（2 NFE） | 1.00 | 0.90 | 0.68 | 0.84 | 0.49 | 0.66 | 0.76 |
| TwinFlow（[Cheng et al., 2025](#bib.bib56)；[Liu et al., 2026b](#bib.bib50)）（2 NFE） | 1.00 | 0.87 | 0.68 | 0.85 | 0.40 | 0.55 | 0.72 |
| Z-Image-Turbo++（[Liu et al., 2026b](#bib.bib50)）（2 NFE） | 1.00 | 0.88 | 0.69 | 0.85 | 0.49 | 0.65 | 0.76 |
| TwinFlow (Qwen-Image)（[Cheng et al., 2025](#bib.bib56)）（1 NFE） | 1.00 | 0.91 | 0.84 | 0.90 | 0.75 | 0.74 | 0.86 |
| APEX (Qwen-Image) (LoRA r=32)（1 NFE） | 0.99 | 0.95 | 0.85 | 0.90 | 0.79 | 0.78 | 0.88 |
| APEX (Qwen-Image) (LoRA r=64)（1 NFE） | 0.99 | 0.94 | 0.88 | 0.90 | 0.85 | 0.78 | 0.89 |
| APEX (Qwen-Image) (Full)（1 NFE） | 0.99 | 0.92 | 0.83 | 0.91 | 0.86 | 0.81 | 0.89 |
| IDM (Z-Image) (LoRA r=32)（2 NFE） | 1.00 | 0.90 | 0.69 | 0.87 | 0.47 | 0.62 | 0.76 |
| IDM (Z-Image) (LoRA r=64)（2 NFE） | 1.00 | 0.90 | 0.70 | 0.87 | 0.49 | 0.64 | 0.77 |
| IDM (Z-Image) (Full)（2 NFE） | 1.00 | 0.91 | 0.71 | 0.88 | 0.51 | 0.66 | 0.78 |
| IDM (Z-Image) (LoRA r=32)（1 NFE） | 1.00 | 0.89 | 0.68 | 0.86 | 0.45 | 0.61 | 0.75 |
| IDM (Z-Image) (LoRA r=64)（1 NFE） | 1.00 | 0.90 | 0.69 | 0.87 | 0.47 | 0.63 | 0.76 |
| IDM (Z-Image) (Full)（1 NFE） | 1.00 | 0.90 | 0.70 | 0.87 | 0.49 | 0.64 | 0.77 |
| IDM (Qwen-Image) (LoRA r=32)（2 NFE） | 1.00 | 0.95 | 0.87 | 0.92 | 0.79 | 0.83 | 0.89 |
| IDM (Qwen-Image) (LoRA r=64)（2 NFE） | 1.00 | 0.95 | 0.88 | 0.92 | 0.81 | 0.84 | 0.90 |
| IDM (Qwen-Image) (Full)（2 NFE） | 1.00 | 0.96 | 0.89 | 0.93 | 0.83 | 0.86 | 0.91 |
| IDM (Qwen-Image) (LoRA r=32)（1 NFE） | 1.00 | 0.94 | 0.86 | 0.91 | 0.77 | 0.81 | 0.88 |
| IDM (Qwen-Image) (LoRA r=64)（1 NFE） | 1.00 | 0.95 | 0.87 | 0.92 | 0.79 | 0.83 | 0.89 |
| IDM (Qwen-Image) (Full)（1 NFE） | 1.00 | 0.95 | 0.88 | 0.92 | 0.81 | 0.84 | 0.90 |

表 3：WISE（[Niu et al., 2025](#bib.bib45)）定量评测。各领域与世界知识 grounding 总分。

| 模型 | 文化 | 时间 | 空间 | 生物 | 物理 | 化学 | 总体↑ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SD v1.5（[Rombach et al., 2022](#bib.bib3)） | 0.34 | 0.35 | 0.32 | 0.28 | 0.29 | 0.21 | 0.32 |
| SDXL（[Podell et al., 2023](#bib.bib2)） | 0.43 | 0.48 | 0.47 | 0.44 | 0.45 | 0.27 | 0.43 |
| SD3.5-Large（[Esser et al., 2024](#bib.bib1)）‡ | 0.44 | 0.50 | 0.58 | 0.44 | 0.52 | 0.31 | 0.46 |
| PixArt-α（[Chen et al., 2024d](#bib.bib25)） | 0.45 | 0.50 | 0.48 | 0.49 | 0.56 | 0.34 | 0.47 |
| Playground-v2.5（[Li et al., 2024a](#bib.bib35)） | 0.49 | 0.58 | 0.55 | 0.43 | 0.48 | 0.33 | 0.49 |
| FLUX.1 [Dev]（[BlackForest, 2024](#bib.bib26)） | 0.48 | 0.58 | 0.62 | 0.42 | 0.51 | 0.35 | 0.50 |
| Janus（[Wu et al., 2025b](#bib.bib39)） | 0.16 | 0.26 | 0.35 | 0.28 | 0.30 | 0.14 | 0.23 |
| VILA-u-7B-256（[Wu et al., 2024](#bib.bib47)） | 0.26 | 0.33 | 0.37 | 0.35 | 0.39 | 0.23 | 0.31 |
| Show-o（[Xie et al., 2024](#bib.bib23)） | 0.28 | 0.40 | 0.48 | 0.30 | 0.46 | 0.30 | 0.35 |
| Janus-Pro-7B（[Chen et al., 2025d](#bib.bib29)） | 0.30 | 0.37 | 0.49 | 0.36 | 0.42 | 0.26 | 0.35 |
| Emu3-Gen（[Wang et al., 2024b](#bib.bib24)） | 0.34 | 0.45 | 0.48 | 0.41 | 0.45 | 0.27 | 0.39 |
| MetaQuery-XL（[Pan et al., 2025](#bib.bib46)） | 0.56 | 0.55 | 0.62 | 0.49 | 0.63 | 0.41 | 0.55 |
| BAGEL（[Deng et al., 2025](#bib.bib44)） | 0.44 | 0.55 | 0.68 | 0.44 | 0.60 | 0.39 | 0.52 |
| GPT-Image-1（[OpenAI, 2025](#bib.bib31)） | 0.81 | 0.71 | 0.89 | 0.83 | 0.79 | 0.74 | 0.80 |
| TwinFlow (Qwen-Image; 1 NFE)（[Cheng et al., 2025](#bib.bib56)） | – | – | – | – | – | – | 0.54 |
| APEX (Qwen-Image) (LoRA r=32)（1 NFE） | – | – | – | – | – | – | – |
| APEX (Qwen-Image) (LoRA r=64)（1 NFE） | – | – | – | – | – | – | – |
| APEX (Qwen-Image) (Full)（1 NFE） | 0.53 | 0.54 | 0.66 | 0.48 | 0.61 | 0.41 | 0.54 |
| IDM (Z-Image) (LoRA r=32)（2 NFE） | 0.45 | 0.46 | 0.56 | 0.41 | 0.52 | 0.37 | 0.46 |
| IDM (Z-Image) (LoRA r=64)（2 NFE） | 0.46 | 0.47 | 0.58 | 0.42 | 0.54 | 0.37 | 0.47 |
| IDM (Z-Image) (Full)（2 NFE） | 0.47 | 0.48 | 0.59 | 0.43 | 0.55 | 0.38 | 0.48 |
| IDM (Z-Image) (LoRA r=32)（1 NFE） | 0.43 | 0.44 | 0.55 | 0.40 | 0.51 | 0.36 | 0.45 |
| IDM (Z-Image) (LoRA r=64)（1 NFE） | 0.44 | 0.45 | 0.56 | 0.41 | 0.52 | 0.36 | 0.46 |
| IDM (Z-Image) (Full)（1 NFE） | 0.46 | 0.47 | 0.58 | 0.42 | 0.54 | 0.37 | 0.47 |
| IDM (Qwen-Image) (LoRA r=32)（2 NFE） | 0.53 | 0.54 | 0.65 | 0.48 | 0.60 | 0.41 | 0.54 |
| IDM (Qwen-Image) (LoRA r=64)（2 NFE） | 0.54 | 0.55 | 0.67 | 0.49 | 0.62 | 0.41 | 0.55 |
| IDM (Qwen-Image) (Full)（2 NFE） | 0.55 | 0.56 | 0.68 | 0.50 | 0.63 | 0.42 | 0.56 |
| IDM (Qwen-Image) (LoRA r=32)（1 NFE） | 0.51 | 0.52 | 0.64 | 0.47 | 0.59 | 0.40 | 0.52 |
| IDM (Qwen-Image) (LoRA r=64)（1 NFE） | 0.53 | 0.54 | 0.65 | 0.48 | 0.60 | 0.41 | 0.54 |
| IDM (Qwen-Image) (Full)（1 NFE） | 0.54 | 0.55 | 0.67 | 0.49 | 0.62 | 0.41 | 0.55 |

表 4：DPG-Bench 定量评测。NFE 记法同[表 2](#S5.T2)。

| 模型 | 全局 | 实体 | 属性 | 关系 | 其他 | 总体↑ |
| --- | --- | --- | --- | --- | --- | --- |
| SD v1.5（[Rombach et al., 2022](#bib.bib3)） | 74.63 | 74.23 | 75.39 | 73.49 | 67.81 | 63.18 |
| PixArt-α（[Chen et al., 2024d](#bib.bib25)） | 74.97 | 79.32 | 78.60 | 82.57 | 76.96 | 71.11 |
| Lumina-Next（[Zhuo et al., 2024](#bib.bib42)） | 82.82 | 88.65 | 86.44 | 80.53 | 81.82 | 74.63 |
| SDXL（[Podell et al., 2023](#bib.bib2)） | 83.27 | 82.43 | 80.91 | 86.76 | 80.41 | 74.65 |
| Hunyuan-DiT（[Li et al., 2024b](#bib.bib34)） | 84.59 | 80.59 | 88.01 | 74.36 | 86.41 | 78.87 |
| Janus（[Wu et al., 2025b](#bib.bib39)） | 82.33 | 87.38 | 87.70 | 85.46 | 86.41 | 79.68 |
| PixArt-Σ（[Chen et al., 2024a](#bib.bib8)） | 86.89 | 82.89 | 88.94 | 86.59 | 87.68 | 80.54 |
| Emu3-Gen（[Wang et al., 2024b](#bib.bib24)） | 85.21 | 86.68 | 86.84 | 90.22 | 83.15 | 80.60 |
| Janus-Pro-1B（[Chen et al., 2025d](#bib.bib29)） | 87.58 | 88.63 | 88.17 | 88.98 | 88.30 | 82.63 |
| DALL-E 3（[OpenAI, 2023](#bib.bib17)） | 90.97 | 89.61 | 88.39 | 90.58 | 89.83 | 83.50 |
| FLUX.1 [Dev]（[BlackForest, 2024](#bib.bib26)） | 74.35 | 90.00 | 88.96 | 90.87 | 88.33 | 83.84 |
| SD3 Medium（[Esser et al., 2024](#bib.bib1)） | 87.90 | 91.01 | 88.83 | 80.70 | 88.68 | 84.08 |
| SD3.5-Turbo（[Esser et al., 2024](#bib.bib1)）‡ | 79.03 | 80.12 | 86.13 | 84.73 | 91.86 | 78.29 |
| SD3.5-Large（[Esser et al., 2024](#bib.bib1)）‡ | 83.21 | 84.27 | 88.99 | 87.35 | 93.28 | 80.35 |
| FLUX.1-schnell（[Labs (2024)](#bib.bib18)） | 84.94 | 86.62 | 90.82 | 88.35 | 93.45 | 82.00 |
| Janus-Pro-7B（[Chen et al., 2025d](#bib.bib29)） | 86.90 | 88.90 | 89.40 | 89.32 | 89.48 | 84.19 |
| HiDream-I1-Full（[Cai et al., 2025](#bib.bib30)） | 76.44 | 90.22 | 89.48 | 93.74 | 91.83 | 85.89 |
| Lumina-Image 2.0（[Qin et al., 2025](#bib.bib28)） | - | 91.97 | 90.20 | 94.85 | - | 87.20 |
| Seedream 3.0（[Gao et al., 2025](#bib.bib32)） | 94.31 | 92.65 | 91.36 | 92.78 | 88.24 | 88.27 |
| GPT Image 1 [High]（[OpenAI, 2025](#bib.bib31)） | 88.89 | 88.94 | 89.84 | 92.63 | 90.96 | 85.15 |
| Qwen-Image（[Wu et al., 2025a](#bib.bib33)） | 91.32 | 91.56 | 92.02 | 94.31 | 92.73 | 88.32 |
| Z-Image（[Team, 2025](#bib.bib49)）（基座；~100 NFE） | 93.39 | 91.22 | 93.16 | 92.22 | 91.52 | 88.14 |
| Z-Image-Turbo（[Team, 2025](#bib.bib49)；[Liu et al., 2026b](#bib.bib50)） | 91.29 | 89.59 | 90.14 | 92.16 | 88.68 | 84.86 |
| DMD2（[Yin et al., 2024a](#bib.bib14)；[Liu et al., 2026b](#bib.bib50)）（2 NFE） | 83.59 | 91.10 | 88.88 | 93.81 | 85.60 | 85.40 |
| TwinFlow（[Cheng et al., 2025](#bib.bib56)；[Liu et al., 2026b](#bib.bib50)）（2 NFE） | 81.46 | 91.83 | 89.02 | 94.16 | 87.60 | 85.98 |
| Z-Image-Turbo++（[Liu et al., 2026b](#bib.bib50)）（2 NFE） | 83.89 | 91.84 | 89.30 | 94.58 | 89.60 | 85.86 |
| TwinFlow (Qwen-Image)（[Cheng et al., 2025](#bib.bib56)）（1 NFE） | – | – | – | – | – | 86.52 |
| APEX (Qwen-Image) (LoRA r=32)（1 NFE） | 93.12 | 90.95 | 91.38 | 90.65 | 91.73 | 86.17 |
| APEX (Qwen-Image) (LoRA r=64)（1 NFE） | 92.46 | 91.14 | 90.71 | 91.30 | 91.98 | 85.77 |
| APEX (Qwen-Image) (Full)（1 NFE） | 93.25 | 89.76 | 90.65 | 91.17 | 90.75 | 84.59 |
| IDM (Z-Image) (LoRA r=32)（2 NFE） | 80.04 | 92.78 | 89.47 | 94.43 | 89.46 | 86.03 |
| IDM (Z-Image) (LoRA r=64)（2 NFE） | 80.46 | 92.94 | 89.59 | 94.52 | 89.74 | 86.44 |
| IDM (Z-Image) (Full)（2 NFE） | 80.85 | 93.08 | 89.70 | 94.60 | 90.00 | 86.82 |
| IDM (Z-Image) (LoRA r=32)（1 NFE） | 79.56 | 92.60 | 89.34 | 94.32 | 89.14 | 85.56 |
| IDM (Z-Image) (LoRA r=64)（1 NFE） | 79.96 | 92.75 | 89.45 | 94.41 | 89.40 | 85.95 |
| IDM (Z-Image) (Full)（1 NFE） | 80.33 | 92.89 | 89.55 | 94.49 | 89.65 | 86.31 |
| IDM (Qwen-Image) (LoRA r=32)（2 NFE） | 93.29 | 90.06 | 91.02 | 91.38 | 92.02 | 86.44 |
| IDM (Qwen-Image) (LoRA r=64)（2 NFE） | 93.68 | 90.20 | 91.13 | 91.46 | 92.28 | 86.82 |
| IDM (Qwen-Image) (Full)（2 NFE） | 94.03 | 90.33 | 91.23 | 91.53 | 92.52 | 87.16 |
| IDM (Qwen-Image) (LoRA r=32)（1 NFE） | 92.74 | 89.86 | 90.86 | 91.26 | 91.66 | 85.91 |
| IDM (Qwen-Image) (LoRA r=64)（1 NFE） | 93.12 | 90.00 | 90.97 | 91.34 | 91.92 | 86.28 |
| IDM (Qwen-Image) (Full)（1 NFE） | 93.46 | 90.12 | 91.07 | 91.41 | 92.14 | 86.61 |

### 5.3 关键消融

所有受控消融均使用 IDM（Z-Image）、全参数微调、2 NFE 以及上述共享训练配置。默认配置为等权的 DMD 速度与端点回归，加上使用生成器 EMA 特征的 $\mathcal{L}_{\text{pop}}$。

表 5：跨基准的总体消融结果（2 NFE）。分数为百分比。第 ① 行为完整配置及共享对照组；第 ②–⑪ 行改变损失、DMD 回归权重或特征映射。仅 v 与仅 x 对照组保留 $\mathcal{L}_{\text{pop}}$。APEX（[Liu et al., 2026a](#bib.bib61)）为其与 TwinFlow 对比中发表的 Z-Image 参考；第 ⑫–⑯ 行取自 [Liu et al. (2026b)](#bib.bib50)，其中第 ⑯ 行在 8 NFE 下评测。

| 序号 | 模型 | NFE | OneIG | GenEval | DPG-Bench | LongText-CN | LongText-EN |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **分布匹配损失消融** | | | | | | | |
| ② | 去掉 $\mathcal{L}_{\text{score}}$（DMD 损失） | 2 | 52.58 | 76.90 | 86.15 | 93.33 | 89.62 |
| ③ | 去掉 $\mathcal{L}_{\text{pop}}$（特征矩损失） | 2 | 52.87 | 77.46 | 86.54 | 93.87 | 89.79 |
| ④ | 同时去掉 $\mathcal{L}_{\text{score}}$ 与 $\mathcal{L}_{\text{pop}}$ | 2 | 52.25 | 76.24 | 85.68 | 92.70 | 88.88 |
| **DMD 回归消融** | | | | | | | |
| ⑤ | 仅 v 损失 | 2 | 52.43 | 76.64 | 85.93 | 93.03 | 89.17 |
| ⑥ | 仅 x 损失 | 2 | 52.78 | 77.26 | 86.42 | 93.71 | 89.74 |
| ⑦ | 2×x 损失+v 损失 | 2 | 53.01 | 77.71 | 86.75 | 94.17 | 90.13 |
| ⑧ | x 损失+2×v 损失 | 2 | 52.95 | 77.59 | 86.66 | 94.05 | 90.04 |
| **特征映射消融** | | | | | | | |
| ⑨ | DINOv2 | 2 | 53.00 | 77.75 | 86.71 | 94.13 | 90.09 |
| ⑩ | 教师模型特征 | 2 | 52.82 | 77.36 | 86.49 | 93.79 | 89.81 |
| ⑪ | 实时自身特征 | 2 | 52.91 | 77.51 | 86.60 | 93.95 | 89.95 |
| **对比方法** | | | | | | | |
| ① | IDM | 2 | 53.06 | 77.81 | 86.82 | 94.25 | 90.20 |
| ⑮ | Z-Image-Turbo | 2 | 50.94 | 76.53 | 85.78 | 78.48 | 72.89 |
| ⑬ | DMD2 | 2 | 50.70 | 76.12 | 85.40 | 85.30 | 80.99 |
| ⑭ | TwinFlow | 2 | 51.38 | 72.41 | 85.98 | 78.65 | 71.99 |
| Ⓐ | APEX | 2 | 52.60 | 77.23 | 88.64 | 90.38 | 88.76 |
| ⑫ | Z-Image-Turbo++ | 2 | 52.50 | 75.70 | 85.86 | 91.62 | 89.88 |
| **更高 NFE 基线** | | | | | | | |
| ⑯ | Z-Image-Turbo | 8 | 52.84 | 75.01 | 84.86 | 92.56 | 91.74 |

**特征矩匹配的附加价值**。在共享 DMD 对照上加入 $\mathcal{L}_{\text{pop}}$，GenEval 从 77.46 升至 77.81，LongText-CN 从 93.87 升至 94.25，LongText-EN 从 89.79 升至 90.20，五项总体指标全部提升。若去掉 $\mathcal{L}_{\text{score}}$，GenEval 为 76.90；两个损失都去掉则为 76.24。另外两项总体指标同样改善：OneIG 从 52.87 升至 53.06，DPG-Bench 从 86.54 升至 86.82。GenEval 细分进一步定位了 $\mathcal{L}_{\text{pop}}$ 的收益：颜色属性绑定从 65.25 升至 66.25，位置从 50.75 升至 51.25，计数从 70.94 升至 71.25，而单物体与双物体分数保持不变，见[表 6](#S5.T6)。去掉 DMD 造成的 GenEval 下降（0.91 分）大于去掉矩匹配（0.35 分）。矩匹配改进了这一 DMD 对照，而分数校正仍是核心。

**生成器 EMA 特征**。用 DINOv2 或生成器 EMA 特征做矩匹配，在五项指标上都优于内部 DMD 对照。从同一不含 $\mathcal{L}_{\text{pop}}$ 的对照出发，DINOv2 把 GenEval 从 77.46 提升至 77.75（+0.29 分），EMA 达到 77.81（+0.35）。二者的 LongText-CN 接近：94.13 与 94.25。实时自身特征与教师模型特征分别达到 77.51 与 77.36 GenEval。EMA 特征在内部 DMD 之上补充矩监督，性能接近 DINOv2，且无需外部特征编码器。

**速度与端点回归**。为选择 DMD 校正监督预测的方式，我们在保留 $\mathcal{L}_{\text{pop}}$ 的前提下比较 v 回归、x 回归及其组合。两个单回归对照因此都包含新增的矩约束，该组实验检验的是如何在组合目标内施加 DMD。由于式 (12) 中 $\ell_{x}(t)=t^{2}\ell_{v}(t)$，这些选择改变的是时间加权与更新幅度。等权 v+x 达到 77.81 GenEval，而仅 v 为 76.64、仅 x 为 77.26；2x+v 与 x+2v 分别为 77.71 与 77.59。等权在五项总体指标上领先，是我们的经验默认，不过 x+2v 的位置分数更高，52.00 对 51.25。混合损失只是对同一 detach 校正施加不同的加权；这些结果并未证明两个回归项含有独立的分布信息。

**与 APEX 及内部对照组的关系**。IDM 建立在 APEX 的内部速度差构造之上（[Liu et al., 2026a](#bib.bib61)），增加了端点回归与 EMA 特征矩匹配，见[图 5](#S5.F5)。已发表的 APEX 参考使用更小的训练集合，因此该对比反映的是完整训练设置。IDM 在 LongText-EN 上得 90.20，APEX 为 88.76；而 APEX 在 DPG-Bench 上领先，88.64 对 86.82。在 IDM 训练设置内部，去损失与特征映射对照把这些目标选择与训练数据的差异区分开来。

![Refer to caption](2610.39633v1/Ablation-idm-losses.png)

图 5：参考方法与 IDM 损失配置。两条提示词在 1 与 2 NFE 下评估。v+x 对照不含 $\mathcal{L}_{\text{pop}}$，完整 IDM 含 EMA 特征矩匹配。APEX 是在更小集合上训练的外部参考；IDM 损失消融共享同一训练设置。

**定性对比**。在[图 5](#S5.F5)的示例中，完整 IDM 在所示采样预算下对密集文本的保持更为一致，尤其在多行菜单中。该菜单把醒目的标题与数行小字结合在一起，是超越几个大字的文本渲染的严苛测试。其条目把中英文饮品名（包括美式咖啡 Americano 与拿铁 Latte）与价格配对。每一行都在黑板菜单的紧凑版面中同时混合两种文字、数字与货币符号。不含 $\mathcal{L}_{\text{pop}}$ 的 v+x 对照产生更饱和的颜色，在寿司海报的橙色与黄色区域最为明显。LongText 结果量化了基准上的文本保真度。

[表 6](#S5.T6)、[表 7](#S5.T7)与[表 8](#S5.T8)把[表 5](#S5.T5)中的基准分数展开为各自的类别。

表 6：GenEval 详细消融结果。分数为百分比；总体为六个类别分数的均值。配置、行分组与来源同[表 5](#S5.T5)。

| 序号 | 模型 | NFE | 总体 | 双物体 | 颜色属性 | 位置 | 计数 | 颜色 | 单物体 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **分布匹配损失消融** | | | | | | | | | |
| ② | 去掉 $\mathcal{L}_{\text{score}}$（DMD 损失） | 2 | 76.90 | 90.40 | 64.50 | 49.25 | 70.31 | 87.23 | 99.69 |
| ③ | 去掉 $\mathcal{L}_{\text{pop}}$（特征矩损失） | 2 | 77.46 | 90.91 | 65.25 | 50.75 | 70.94 | 87.23 | 99.69 |
| ④ | 同时去掉 $\mathcal{L}_{\text{score}}$ 与 $\mathcal{L}_{\text{pop}}$ | 2 | 76.24 | 90.15 | 63.75 | 49.25 | 68.44 | 86.17 | 99.69 |
| **DMD 回归消融** | | | | | | | | | |
| ⑤ | 仅 v 损失 | 2 | 76.64 | 90.40 | 64.00 | 50.00 | 69.06 | 86.70 | 99.69 |
| ⑥ | 仅 x 损失 | 2 | 77.26 | 90.66 | 65.50 | 50.50 | 70.00 | 87.23 | 99.69 |
| ⑦ | 2×x 损失+v 损失 | 2 | 77.71 | 91.16 | 65.75 | 51.25 | 70.63 | 87.77 | 99.69 |
| ⑧ | x 损失+2×v 损失 | 2 | 77.59 | 91.16 | 66.00 | 52.00 | 70.00 | 86.70 | 99.69 |
| **特征映射消融** | | | | | | | | | |
| ⑨ | DINOv2 | 2 | 77.75 | 91.16 | 65.75 | 51.75 | 70.94 | 87.23 | 99.69 |
| ⑩ | 教师模型特征 | 2 | 77.36 | 90.66 | 65.50 | 50.75 | 70.31 | 87.23 | 99.69 |
| ⑪ | 实时自身特征 | 2 | 77.51 | 90.91 | 66.00 | 51.25 | 70.00 | 87.23 | 99.69 |
| **对比方法** | | | | | | | | | |
| ① | IDM | 2 | 77.81 | 90.91 | 66.25 | 51.25 | 71.25 | 87.50 | 99.69 |
| ⑮ | Z-Image-Turbo | 2 | 76.53 | 89.39 | 57.75 | 50.50 | 74.38 | 87.77 | 99.38 |
| ⑬ | DMD2 | 2 | 76.12 | 90.40 | 65.50 | 49.00 | 67.50 | 84.31 | 100.00 |
| ⑭ | TwinFlow | 2 | 72.41 | 87.12 | 54.75 | 40.00 | 67.81 | 85.11 | 99.69 |
| Ⓐ | APEX | 2 | 77.23 | 90.66 | 65.50 | 50.25 | 70.31 | 86.97 | 99.69 |
| ⑫ | Z-Image-Turbo++ | 2 | 75.70 | 87.63 | 64.50 | 48.75 | 69.06 | 84.57 | 99.69 |
| **更高 NFE 基线** | | | | | | | | | |
| ⑯ | Z-Image-Turbo | 8 | 75.01 | 88.89 | 58.75 | 45.75 | 71.88 | 85.11 | 99.69 |

表 7：DPG-Bench 详细消融结果。分数为百分比。总体按基准题层级的标准提示级聚合计算，而非五个类别列的均值。配置、行分组与来源同[表 5](#S5.T5)。

| 序号 | 模型 | NFE | 总体 | 属性 | 全局 | 关系 | 其他 | 实体 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **分布匹配损失消融** | | | | | | | | |
| ② | 去掉 $\mathcal{L}_{\text{score}}$（DMD 损失） | 2 | 86.15 | 89.33 | 80.23 | 94.32 | 89.54 | 92.58 |
| ③ | 去掉 $\mathcal{L}_{\text{pop}}$（特征矩损失） | 2 | 86.54 | 89.54 | 79.94 | 94.48 | 89.41 | 92.88 |
| ④ | 同时去掉 $\mathcal{L}_{\text{score}}$ 与 $\mathcal{L}_{\text{pop}}$ | 2 | 85.68 | 89.07 | 80.01 | 94.12 | 89.37 | 92.23 |
| **DMD 回归消融** | | | | | | | | |
| ⑤ | 仅 v 损失 | 2 | 85.93 | 89.21 | 79.45 | 94.22 | 89.05 | 92.42 |
| ⑥ | 仅 x 损失 | 2 | 86.42 | 89.48 | 79.56 | 94.43 | 89.15 | 92.78 |
| ⑦ | 2×x 损失+v 损失 | 2 | 86.75 | 89.68 | 81.62 | 94.57 | 90.44 | 93.04 |
| ⑧ | x 损失+2×v 损失 | 2 | 86.66 | 89.64 | 80.79 | 94.55 | 89.92 | 92.99 |
| **特征映射消融** | | | | | | | | |
| ⑨ | DINOv2 | 2 | 86.71 | 89.66 | 82.26 | 94.56 | 90.85 | 92.87 |
| ⑩ | 教师模型特征 | 2 | 86.49 | 89.52 | 80.36 | 94.46 | 89.68 | 92.83 |
| ⑪ | 实时自身特征 | 2 | 86.60 | 89.58 | 80.97 | 94.51 | 90.08 | 92.91 |
| **对比方法** | | | | | | | | |
| ① | IDM | 2 | 86.82 | 89.70 | 80.85 | 94.60 | 90.00 | 93.08 |
| ⑮ | Z-Image-Turbo | 2 | 85.78 | 88.78 | 84.19 | 94.16 | 89.60 | 91.73 |
| ⑬ | DMD2 | 2 | 85.40 | 88.88 | 83.59 | 93.81 | 85.60 | 91.10 |
| ⑭ | TwinFlow | 2 | 85.98 | 89.02 | 81.46 | 94.16 | 87.60 | 91.83 |
| Ⓐ | APEX | 2 | 88.64 | 90.20 | 88.35 | 95.10 | 90.80 | 92.88 |
| ⑫ | Z-Image-Turbo++ | 2 | 85.86 | 89.30 | 83.89 | 94.58 | 89.60 | 91.84 |
| **更高 NFE 基线** | | | | | | | | |
| ⑯ | Z-Image-Turbo | 8 | 84.86 | 90.14 | 91.29 | 92.16 | 88.68 | 89.59 |

表 8：OneIG 详细消融结果。分数为百分比；总体为五个类别分数的均值。配置、行分组与来源同[表 5](#S5.T5)。

| 序号 | 模型 | NFE | 总体 | 对齐 | 文本 | 多样性 | 风格 | 推理 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **分布匹配损失消融** | | | | | | | | |
| ② | 去掉 $\mathcal{L}_{\text{score}}$（DMD 损失） | 2 | 52.58 | 86.13 | 97.09 | 12.74 | 38.04 | 28.90 |
| ③ | 去掉 $\mathcal{L}_{\text{pop}}$（特征矩损失） | 2 | 52.87 | 86.31 | 97.73 | 12.81 | 38.16 | 29.34 |
| ④ | 同时去掉 $\mathcal{L}_{\text{score}}$ 与 $\mathcal{L}_{\text{pop}}$ | 2 | 52.25 | 85.94 | 96.37 | 12.67 | 37.90 | 28.37 |
| **DMD 回归消融** | | | | | | | | |
| ⑤ | 仅 v 损失 | 2 | 52.43 | 86.04 | 96.76 | 12.71 | 37.97 | 28.67 |
| ⑥ | 仅 x 损失 | 2 | 52.78 | 86.25 | 97.53 | 12.79 | 38.12 | 29.21 |
| ⑦ | 2×x 损失+v 损失 | 2 | 53.01 | 86.39 | 98.06 | 12.84 | 38.22 | 29.54 |
| ⑧ | x 损失+2×v 损失 | 2 | 52.95 | 86.36 | 97.94 | 12.83 | 38.20 | 29.42 |
| **特征映射消融** | | | | | | | | |
| ⑨ | DINOv2 | 2 | 53.00 | 86.58 | 97.72 | 12.88 | 38.36 | 29.46 |
| ⑩ | 教师模型特征 | 2 | 52.82 | 86.28 | 97.62 | 12.80 | 38.14 | 29.26 |
| ⑪ | 实时自身特征 | 2 | 52.91 | 86.33 | 97.82 | 12.82 | 38.18 | 29.40 |
| **对比方法** | | | | | | | | |
| ① | IDM | 2 | 53.06 | 86.42 | 98.15 | 12.85 | 38.24 | 29.65 |
| ⑮ | Z-Image-Turbo | 2 | 50.94 | 83.92 | 92.85 | 13.85 | 36.25 | 27.86 |
| ⑬ | DMD2 | 2 | 50.70 | 85.21 | 90.82 | 12.75 | 36.77 | 27.93 |
| ⑭ | TwinFlow | 2 | 51.38 | 85.26 | 90.61 | 15.49 | 38.03 | 27.52 |
| Ⓐ | APEX | 2 | 52.60 | 86.10 | 97.05 | 12.70 | 38.00 | 29.15 |
| ⑫ | Z-Image-Turbo++ | 2 | 52.50 | 85.65 | 97.09 | 11.75 | 37.87 | 30.12 |
| **更高 NFE 基线** | | | | | | | | |
| ⑯ | Z-Image-Turbo | 8 | 52.84 | 84.03 | 99.32 | 13.85 | 36.81 | 30.19 |

![Refer to caption](2610.39633v1/NFE1.png)

图 6：Z-Image 上的采样预算对比。Z-Image-Turbo、DMD2、TwinFlow、APEX 与 IDM 在所示 NFE 预算下的最终输出，按两条提示词分组。每列表示一种采样预算，而非同一轨迹的中间状态。

### 5.4 定性结果

[图 6](#S5.F6)比较采样预算。[图 2](#S1.F2)展示文本渲染与人像；[图 7](#S5.F7)给出更多风格与内容的样例。

![Refer to caption](2610.39633v1/fig6.png)

![Refer to caption](2610.39633v1/fig9.png)

![Refer to caption](2610.39633v1/fig3.png)

![Refer to caption](2610.39633v1/fig4.png)

![Refer to caption](2610.39633v1/fig7.png)

![Refer to caption](2610.39633v1/fig8.png)

![Refer to caption](2610.39633v1/fig11.png)

![Refer to caption](2610.39633v1/fig12.png)

图 7：IDM（Z-Image），2 NFE。不同风格与内容的补充样例。每一面板使用相同模型与采样预算；该网格是输出图库，而非方法或 NFE 对比。

## 6 结论

我们提出了内蕴分布匹配（IDM），它在内部 DMD 之上对生成器 EMA 特征统计量加入显式约束。反向 KL 场分解为"保留完整分数差监督、同时额外匹配特征均值与标准差"提供了动机。受控消融表明 EMA 特征矩相对内部 DMD 基线带来提升，性能接近 DINOv2。在 Z-Image-Turbo 6B 上，IDM 在中英文 LongText-Bench 上分别达到 94.25% 与 90.20%，是所对比 2 NFE 方法中的最高分。在最大 20B 参数的骨干上的实验支持把生成器的预测与表示结合起来用于少步文生图。

## 参考文献

* Ambrosio and Savaré (2007)
  L. Ambrosio and G. Savaré
  Gradient flows of probability measures.
  In Handbook of differential equations: evolutionary equations,
  Vol. 3, pp. 1–136.
  Cited by: [§B.1.1](#A2.SS1.SSS1.p1.1 "B.1.1 First variation form ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* Arjovsky et al. (2017)
  M. Arjovsky, S. Chintala, and L. Bottou
  Wasserstein generative adversarial networks.
  In International conference on machine learning,
  pp. 214–223.
  Cited by: [§B.1.1](#A2.SS1.SSS1.Px1.p1.1 "On condition (b): when does the model law admit a density? ‣ B.1.1 First variation form ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* BlackForest (2024)
  BlackForest
  FLUX.
  Note: <https://github.com/black-forest-labs/flux>
  Cited by: [Table 2](#S5.T2.4.1.7.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.7.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.12.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Cai et al. (2025)
  Q. Cai, J. Chen, Y. Chen, Y. Li, F. Long, Y. Pan, Z. Qiu, Y. Zhang, F. Gao, P. Xu, et al.
  HiDream-i1: a high-efficient image generative foundation model with sparse diffusion transformer.
  arXiv preprint arXiv:2505.22705.
  Cited by: [Table 2](#S5.T2.4.1.12.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.18.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Chang et al. (2026)
  J. Chang, Y. Fang, P. Xing, S. Wu, W. Cheng, R. Wang, X. Zeng, G. Yu, and H. Chen
  Oneig-bench: omni-dimensional nuanced evaluation for image generation.
  Advances in Neural Information Processing Systems 38.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px5.p1.1 "Text Rendering in Image Generation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§5.1](#S5.SS1.SSS0.Px4.p1.1 "Evaluation. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Chen et al. (2026)
  C. Chen, H. Chen, K. Chen, Z. Cheng, L. Cui, R. Fang, Z. Gu, Z. Huang, Z. Lan, Y. Lei, et al.
  LLaDA-image: building strong image generators with fully open training recipes.
  arXiv preprint arXiv:2609.03796.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Chen et al. (2025a)
  J. Chen, Z. Xu, X. Pan, Y. Hu, C. Qin, T. Goldstein, L. Huang, T. Zhou, S. Xie, S. Savarese, et al.
  Blip3-o: a family of fully open unified multimodal models-architecture, training and dataset.
  arXiv preprint arXiv:2505.09568.
  Cited by: [§5.1](#S5.SS1.SSS0.Px2.p1.1 "Training data. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Chen et al. (2024a)
  J. Chen, C. Ge, E. Xie, Y. Wu, L. Yao, X. Ren, Z. Wang, P. Luo, H. Lu, and Z. Li
  PixArt-Σ\Sigma: weak-to-strong training of diffusion transformer for 4k text-to-image generation.
  arXiv preprint arXiv:2403.04692.
  Cited by: [Table 4](#S5.T4.4.1.8.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Chen et al. (2024b)
  J. Chen, C. Ge, E. Xie, Y. Wu, L. Yao, X. Ren, Z. Wang, P. Luo, H. Lu, and Z. Li
  Pixart-σ\sigma: weak-to-strong training of diffusion transformer for 4k text-to-image generation.
  arXiv preprint arXiv:2403.04692.
  Cited by: [Table 1](#S5.T1.8.1.24.1 "In 5 Experiments ‣ Intrinsic Distribution Matching").
* Chen et al. (2024c)
  J. Chen, Y. Wu, S. Luo, E. Xie, S. Paul, P. Luo, H. Zhao, and Z. Li
  Pixart-{\{\\backslashdelta}\}: fast and controllable image generation with latent consistency models.
  arXiv preprint arXiv:2401.05252.
  Cited by: [Table 1](#S5.T1.8.1.23.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.4.1 "In 5 Experiments ‣ Intrinsic Distribution Matching").
* Chen et al. (2025b)
  J. Chen, S. Xue, Y. Zhao, J. Yu, S. Paul, J. Chen, H. Cai, E. Xie, and S. Han
  SANA-sprint: one-step diffusion with continuous-time consistency distillation.
  arXiv preprint arXiv:2503.09641.
  Cited by: [Table 1](#S5.T1.8.1.10.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.29.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.30.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.9.1 "In 5 Experiments ‣ Intrinsic Distribution Matching").
* Chen et al. (2024d)
  J. Chen, J. Yu, C. Ge, L. Yao, E. Xie, Z. Wang, J. T. Kwok, P. Luo, H. Lu, and Z. Li
  PixArt-α\alpha: fast training of diffusion transformer for photorealistic text-to-image synthesis.
  In ICLR,
  Cited by: [Table 2](#S5.T2.4.1.5.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.5.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.3.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Chen et al. (2025c)
  J. Chen, Z. Cai, P. Chen, S. Chen, K. Ji, X. Wang, Y. Yang, and B. Wang
  ShareGPT-4o-image: aligning multimodal models with gpt-4o-level image generation.
  arXiv preprint arXiv:2506.18095.
  Cited by: [§5.1](#S5.SS1.SSS0.Px2.p1.1 "Training data. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Chen et al. (2025d)
  X. Chen, Z. Wu, X. Liu, Z. Pan, W. Liu, Z. Xie, X. Yu, and C. Ruan
  Janus-pro: unified multimodal understanding and generation with data and model scaling.
  arXiv preprint arXiv:2501.17811.
  Cited by: [Table 2](#S5.T2.4.1.11.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.11.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.10.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.17.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Cheng et al. (2025)
  Z. Cheng, P. Sun, J. Li, and T. Lin
  TwinFlow: realizing one-step generation on large models with self-adversarial flows.
  arXiv preprint arXiv:2512.05150.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§B.4](#A2.SS4.p2.1 "B.4 DMD Loss: Score-Difference Identity and Regression ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p3.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px5.p1.1 "Internal Score Estimation. ‣ 2 Background ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.12.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.32.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.22.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.24.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.16.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.26.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.28.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Deng et al. (2025)
  C. Deng, D. Zhu, K. Li, C. Gou, F. Li, Z. Wang, S. Zhong, W. Yu, X. Nie, Z. Song, G. Shi, and H. Fan
  Emerging properties in unified multimodal pretraining.
  arXiv preprint arXiv:2505.14683.
  Cited by: [Table 2](#S5.T2.4.1.15.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.14.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Deng et al. (2026)
  M. Deng, H. Li, T. Li, Y. Du, and K. He
  Generative modeling via drifting.
  arXiv preprint arXiv:2602.04770.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px3.p1.1 "Feature-Space Distribution Matching. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Esser et al. (2024)
  P. Esser, S. Kulal, A. Blattmann, R. Entezari, J. Müller, H. Saini, Y. Levi, D. Lorenz, A. Sauer, F. Boesel, et al.
  Scaling rectified flow transformers for high-resolution image synthesis.
  In International Conference on Machine Learning,
  Cited by: [Table 1](#S5.T1.8.1.25.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.5.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.6.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.8.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.4.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.13.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.14.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.15.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Fang et al. (2025)
  R. Fang, A. Yu, C. Duan, L. Huang, S. Bai, Y. Cai, K. Wang, S. Liu, X. Liu, and H. Li
  Flux-reason-6m & prism-bench: a million-scale text-to-image reasoning dataset and comprehensive benchmark.
  arXiv preprint arXiv:2509.09680.
  Cited by: [§5.1](#S5.SS1.SSS0.Px2.p1.1 "Training data. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Franceschi et al. (2023)
  J. Franceschi, M. Gartrell, L. Dos Santos, T. Issenhuth, E. de Bézenac, M. Chen, and A. Rakotomamonjy
  Unifying gans and score-based diffusion as generative particle models.
  Advances in Neural Information Processing Systems 36, pp. 59729–59760.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Frans et al. (2024)
  K. Frans, D. Hafner, S. Levine, and P. Abbeel
  One step diffusion via shortcut models.
  arXiv preprint arXiv:2410.12557.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Gao et al. (2025)
  Y. Gao, L. Gong, Q. Guo, X. Hou, Z. Lai, F. Li, L. Li, X. Lian, C. Liao, L. Liu, et al.
  Seedream 3.0 technical report.
  arXiv preprint arXiv:2504.11346.
  Cited by: [Table 2](#S5.T2.4.1.14.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.20.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Geng et al. (2025a)
  Z. Geng, M. Deng, X. Bai, J. Z. Kolter, and K. He
  Mean flows for one-step generative modeling.
  arXiv preprint arXiv:2505.13447.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Geng et al. (2026)
  Z. Geng, Y. Lu, Z. Wu, E. Shechtman, J. Z. Kolter, and K. He
  Improved mean flows: on the challenges of fastforward generative models.
  In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition,
  pp. 30467–30476.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Geng et al. (2025b)
  Z. Geng, Y. Wang, Y. Ma, C. Li, Y. Rao, S. Gu, Z. Zhong, Q. Lu, H. Hu, X. Zhang, et al.
  X-omni: reinforcement learning makes discrete autoregressive image generative models great again.
  arXiv preprint arXiv:2507.22058.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px5.p1.1 "Text Rendering in Image Generation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p1.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p6.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§5.1](#S5.SS1.SSS0.Px4.p1.1 "Evaluation. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Ghosh et al. (2023)
  D. Ghosh, H. Hajishirzi, and L. Schmidt
  Geneval: an object-focused framework for evaluating text-to-image alignment.
  Advances in Neural Information Processing Systems 36, pp. 52132–52152.
  Cited by: [§5.1](#S5.SS1.SSS0.Px4.p1.1 "Evaluation. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Goodfellow et al. (2014)
  I. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley, S. Ozair, A. Courville, and Y. Bengio
  Generative adversarial nets.
  In Advances in Neural Information Processing Systems,
  Cited by: [§B.1.3](#A2.SS1.SSS3.Px2.p1.3 "Scaled Jensen–Shannon / saturating GAN. ‣ B.1.3 Important special cases ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* Han et al. (2026a)
  J. Han, P. Li, Q. Guo, R. Xu, S. Ermon, and E. J. Candès
  One-step generative modeling via wasserstein gradient flows.
  arXiv preprint arXiv:2605.11755.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px3.p1.1 "Feature-Space Distribution Matching. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Han et al. (2026b)
  Y. Han, S. Liao, P. Sun, D. Liu, Y. Zhang, P. Wan, and T. Lin
  FlowCPO: a unified divergence view of preference alignment for flow models.
  arXiv preprint arXiv:2609.09905.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Heusel et al. (2017)
  M. Heusel, H. Ramsauer, T. Unterthiner, B. Nessler, and S. Hochreiter
  GANs trained by a two time-scale update rule converge to a local nash equilibrium.
  In Advances in Neural Information Processing Systems,
  Cited by: [Appendix A](#A1.SS0.SSS0.Px3.p1.1 "Feature-Space Distribution Matching. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Ho et al. (2020)
  J. Ho, A. Jain, and P. Abbeel
  Denoising diffusion probabilistic models.
  Advances in neural information processing systems 33, pp. 6840–6851.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px1.p1.1 "Continuous Generative Models. ‣ 2 Background ‣ Intrinsic Distribution Matching").
* Holderrieth and Erives (2025)
  P. Holderrieth and E. Erives
  An introduction to flow matching and diffusion models.
  arXiv preprint arXiv:2506.02070.
  Cited by: [§B.3](#A2.SS3.p1.1 "B.3 Score–Velocity Identity ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* Hu et al. (2024)
  X. Hu, R. Wang, Y. Fang, B. Fu, P. Cheng, and G. Yu
  Ella: equip diffusion models with llm for enhanced semantic alignment.
  arXiv preprint arXiv:2403.05135.
  Cited by: [§5.1](#S5.SS1.SSS0.Px4.p1.1 "Evaluation. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Labs (2024)
  B. F. Labs
  FLUX.
  External Links: [Link](https://blackforestlabs.ai/)
  Cited by: [Table 1](#S5.T1.8.1.28.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.8.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.16.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Li et al. (2017)
  C. Li, W. Chang, Y. Cheng, Y. Yang, and B. Póczos
  MMD GAN: towards deeper understanding of moment matching network.
  Advances in Neural Information Processing Systems 30.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px3.p1.1 "Feature-Space Distribution Matching. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Li et al. (2024a)
  D. Li, A. Kamko, E. Akhgari, A. Sabet, L. Xu, and S. Doshi
  Playground v2. 5: three insights towards enhancing aesthetic quality in text-to-image generation.
  arXiv preprint arXiv:2402.17245.
  Cited by: [§5.1](#S5.SS1.SSS0.Px4.p1.1 "Evaluation. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.6.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Li et al. (2015)
  Y. Li, K. Swersky, and R. Zemel
  Generative moment matching networks.
  In International Conference on Machine Learning,
  pp. 1718–1727.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px3.p1.1 "Feature-Space Distribution Matching. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Li et al. (2024b)
  Z. Li, J. Zhang, Q. Lin, J. Xiong, Y. Long, X. Deng, Y. Zhang, X. Liu, M. Huang, Z. Xiao, et al.
  Hunyuan-dit: a powerful multi-resolution diffusion transformer with fine-grained chinese understanding.
  arXiv preprint arXiv:2405.08748.
  Cited by: [Table 4](#S5.T4.4.1.6.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Lipman et al. (2022)
  Y. Lipman, R. T. Chen, H. Ben-Hamu, M. Nickel, and M. Le
  Flow matching for generative modeling.
  arXiv preprint arXiv:2210.02747.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px1.p1.1 "Continuous Generative Models. ‣ 2 Background ‣ Intrinsic Distribution Matching").
* Liu et al. (2026a)
  D. Liu, P. Sun, Y. Han, Z. Cheng, C. Chen, and T. Lin
  Self-adversarial one step generation via condition shifting.
  arXiv preprint arXiv:2604.12322.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§B.4](#A2.SS4.p2.1 "B.4 DMD Loss: Score-Difference Identity and Regression ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p3.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px5.p1.1 "Internal Score Estimation. ‣ 2 Background ‣ Intrinsic Distribution Matching"),
  [§4.1](#S4.SS1.SSS0.Px1.p1.1 "Internal velocity branches. ‣ 4.1 DMD Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching"),
  [§5.1](#S5.SS1.SSS0.Px2.p1.1 "Training data. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [§5.3](#S5.SS3.SSS0.Px4.p1.1 "Relation to APEX and the internal controls. ‣ 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.13.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.14.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.15.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.33.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.34.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.35.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.18.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 5](#S5.T5 "In 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Liu et al. (2025)
  D. Liu, P. Sun, X. Li, and T. Lin
  Efficient generative model training via embedded representation warmup.
  arXiv preprint arXiv:2504.10188.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px4.p1.1 "Gaussian Score Structure and Intrinsic Representations. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Liu et al. (2026b)
  D. Liu, R. Du, D. Liu, D. Jiang, L. Li, Q. Wu, Z. Li, S. C. Hoi, H. Li, and P. Gao
  High-fidelity two-step image generation via teacher-aligned end-to-end distillation.
  arXiv preprint arXiv:2606.12575.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px5.p1.1 "Text Rendering in Image Generation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.20.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.21.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.22.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.23.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.24.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.25.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.26.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.27.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 5](#S5.T5 "In 5.3 Key Ablations ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Liu et al. (2016)
  Q. Liu, J. Lee, and M. Jordan
  A kernelized stein discrepancy for goodness-of-fit tests.
  In International conference on machine learning,
  pp. 276–284.
  Cited by: [§B.2.2](#A2.SS2.SSS2.p1.1 "B.2.2 Orthogonality of the Residual ‣ B.2 Score Decomposition of the Reverse-KL Field ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* Liu et al. (2023)
  X. Liu, C. Gong, and Q. Liu
  Flow straight and fast: learning to generate and transfer data with rectified flow.
  In International Conference on Learning Representations,
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px2.p1.1 "Rectified Flow and Few-Step Generation. ‣ 2 Background ‣ Intrinsic Distribution Matching").
* Lu and Song (2024)
  C. Lu and Y. Song
  Simplifying, stabilizing and scaling continuous-time consistency models.
  arXiv preprint arXiv:2410.11081.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Lu et al. (2025)
  Y. Lu, X. Xia, M. Zhang, H. Kuang, J. Zheng, Y. Ren, and X. Xiao
  Hyper-bagel: a unified acceleration framework for multimodal understanding and generation.
  External Links: 2509.18824
  Cited by: [Table 2](#S5.T2.4.1.17.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Luo et al. (2023)
  S. Luo, Y. Tan, L. Huang, J. Li, and H. Zhao
  Latent consistency models: synthesizing high-resolution images with few-step inference.
  arXiv preprint arXiv:2310.04378.
  Cited by: [Table 1](#S5.T1.8.1.22.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.3.2 "In 5 Experiments ‣ Intrinsic Distribution Matching").
* Ma et al. (2025)
  Y. Ma, X. Liu, X. Chen, W. Liu, C. Wu, Z. Wu, Z. Pan, Z. Xie, H. Zhang, X. Yu, et al.
  Janusflow: harmonizing autoregression and rectified flow for unified multimodal understanding and generation.
  In Proceedings of the Computer Vision and Pattern Recognition Conference,
  pp. 7739–7751.
  Cited by: [Table 2](#S5.T2.4.1.9.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* ModelTC (2025)
  ModelTC
  Qwen-image-lightning.
   GitHub.
  Note: [GitHub-ModelTC/Qwen-Image-Lightning:Qwen-Image-Lightning:SpeedupQwen-Imagemodelwithdistilla](https://GitHub-ModelTC/Qwen-Image-Lightning:Qwen-Image-Lightning:SpeedupQwen-Imagemodelwithdistilla)
  Cited by: [Table 1](#S5.T1.8.1.11.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.31.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.18.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Niu et al. (2025)
  Y. Niu, M. Ning, M. Zheng, W. Jin, B. Lin, P. Jin, J. Liao, C. Feng, K. Ning, B. Zhu, et al.
  Wise: a world knowledge-informed semantic evaluation for text-to-image generation.
  arXiv preprint arXiv:2503.07265.
  Cited by: [§5.1](#S5.SS1.SSS0.Px4.p1.1 "Evaluation. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.2 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.3 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Nowozin et al. (2016)
  S. Nowozin, B. Cseke, and R. Tomioka
  F-gan: training generative neural samplers using variational divergence minimization.
  Advances in neural information processing systems 29.
  Cited by: [§B.1.2](#A2.SS1.SSS2.p2.1 "B.1.2 𝑓-divergence specialization ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* OpenAI (2023)
  OpenAI
  Dalle-3.
  External Links: [Link](https://openai.com/dall-e-3)
  Cited by: [Table 4](#S5.T4.4.1.11.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* OpenAI (2025)
  OpenAI
  GPT-image-1.
  External Links: [Link](https://openai.com/index/introducing-4o-image-generation/)
  Cited by: [Table 2](#S5.T2.4.1.13.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.15.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.21.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Pan et al. (2025)
  X. Pan, S. N. Shukla, A. Singh, Z. Zhao, S. K. Mishra, J. Wang, Z. Xu, J. Chen, K. Li, F. Juefei-Xu, et al.
  Transfer between modalities with metaqueries.
  arXiv preprint arXiv:2504.06256.
  Cited by: [Table 3](#S5.T3.4.1.13.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Podell et al. (2023)
  D. Podell, Z. English, K. Lacey, A. Blattmann, T. Dockhorn, J. Müller, J. Penna, and R. Rombach
  SDXL: improving latent diffusion models for high-resolution image synthesis.
  arXiv preprint arXiv:2307.01952.
  Cited by: [Table 3](#S5.T3.4.1.3.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.5.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Qin et al. (2025)
  Q. Qin, L. Zhuo, Y. Xin, R. Du, Z. Li, B. Fu, Y. Lu, J. Yuan, X. Li, D. Liu, et al.
  Lumina-image 2.0: a unified and efficient image generative framework.
  arXiv preprint arXiv:2503.21758.
  Cited by: [Table 2](#S5.T2.4.1.10.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.19.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Rombach et al. (2022)
  R. Rombach, A. Blattmann, D. Lorenz, P. Esser, and B. Ommer
  High-resolution image synthesis with latent diffusion models.
  In IEEE Conference on Computer Vision and Pattern Recognition,
  Cited by: [Table 3](#S5.T3.4.1.2.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.2.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Salimans and Ho (2022)
  T. Salimans and J. Ho
  Progressive distillation for fast sampling of diffusion models.
  arXiv preprint arXiv:2202.00512.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px1.p1.1 "Continuous Generative Models. ‣ 2 Background ‣ Intrinsic Distribution Matching").
* Sauer et al. (2024)
  A. Sauer, F. Boesel, T. Dockhorn, A. Blattmann, P. Esser, and R. Rombach
  Fast high-resolution image synthesis with latent adversarial diffusion distillation.
  arXiv preprint arXiv:2403.12015.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Sauer et al. (2023)
  A. Sauer, D. Lorenz, A. Blattmann, and R. Rombach
  Adversarial diffusion distillation.
  arXiv preprint arXiv:2311.17042.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Song et al. (2023)
  Y. Song, P. Dhariwal, M. Chen, and I. Sutskever
  Consistency models.
  In Proceedings of the 40th International Conference on Machine Learning,
  pp. 32211–32252.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px1.p1.1 "Continuous Generative Models. ‣ 2 Background ‣ Intrinsic Distribution Matching").
* Song et al. (2020)
  Y. Song, J. Sohl-Dickstein, D. P. Kingma, A. Kumar, S. Ermon, and B. Poole
  Score-based generative modeling through stochastic differential equations.
  arXiv preprint arXiv:2011.13456.
  Cited by: [§1](#S1.p1.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px1.p1.1 "Continuous Generative Models. ‣ 2 Background ‣ Intrinsic Distribution Matching").
* Sun et al. (2026a)
  P. Sun, Z. Cheng, D. Liu, J. Xie, X. Shang, and T. Lin
  Three-body scattering for generative modeling.
  arXiv preprint arXiv:2607.18198.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px3.p1.1 "Feature-Space Distribution Matching. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Sun and Lin (2025)
  P. Sun and T. Lin
  Any-step generation via n-th order recursive consistent velocity field estimation.
  Note: GitHub repository
  External Links: [Link](https://github.com/LINs-lab/RCGM)
  Cited by: [§4.3](#S4.SS3.p1.1 "4.3 Training Objective ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching").
* Sun et al. (2026b)
  P. Sun, X. Shang, T. Lin, and Z. Shen
  Duality models: an embarrassingly simple one-step generation paradigm.
  arXiv preprint arXiv:2602.17682.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Team (2025)
  Z. Team
  Z-image: an efficient image generation foundation model with single-stream diffusion transformer.
  arXiv preprint arXiv:2511.22699.
  Cited by: [§5.1](#S5.SS1.SSS0.Px1.p1.1 "Backbones and tuning. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.19.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.20.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.23.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.24.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Wang and Vastola (2023)
  B. Wang and J. J. Vastola
  The hidden linear structure in score-based models and its application.
  arXiv preprint arXiv:2311.10892.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px4.p1.1 "Gaussian Score Structure and Intrinsic Representations. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p4.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§3.3](#S3.SS3.p1.2 "3.3 Decomposition of the Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching").
* Wang and Vastola (2024)
  B. Wang and J. J. Vastola
  The unreasonable effectiveness of gaussian score approximation for diffusion models and its applications.
  arXiv preprint arXiv:2412.09726.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px4.p1.1 "Gaussian Score Structure and Intrinsic Representations. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p4.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§3.3](#S3.SS3.p1.2 "3.3 Decomposition of the Reverse-KL Field ‣ 3 A Distribution-Gradient View ‣ Intrinsic Distribution Matching").
* Wang et al. (2024a)
  F. Wang, Z. Huang, A. W. Bergman, D. Shen, P. Gao, M. Lingelbach, K. Sun, W. Bian, G. Song, Y. Liu, et al.
  Phased consistency model.
  arXiv preprint arXiv:2405.18407.
  Cited by: [Table 1](#S5.T1.8.1.26.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.6.1 "In 5 Experiments ‣ Intrinsic Distribution Matching").
* Wang et al. (2024b)
  X. Wang, X. Zhang, Z. Luo, Q. Sun, Y. Cui, J. Wang, F. Zhang, Y. Wang, Z. Li, Q. Yu, et al.
  Emu3: next-token prediction is all you need.
  arXiv preprint arXiv:2409.18869.
  Cited by: [Table 2](#S5.T2.4.1.4.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.12.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.9.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Wang et al. (2026)
  Y. Wang, W. Bai, D. Zhang, W. Luo, H. Sun, et al.
  Uni-instruct: one-step diffusion model through unified diffusion divergence instruction.
  Advances in Neural Information Processing Systems 38, pp. 57097–57132.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§B.1.3](#A2.SS1.SSS3.p1.1 "B.1.3 Important special cases ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* Wang et al. (2023)
  Z. Wang, C. Lu, Y. Wang, F. Bao, C. Li, H. Su, and J. Zhu
  ProlificDreamer: high-fidelity and diverse text-to-3d generation with variational score distillation.
  Advances in Neural Information Processing Systems 36, pp. 8406–8441.
  Cited by: [§2](#S2.SS0.SSS0.Px3.p1.1 "Distribution Matching Distillation. ‣ 2 Background ‣ Intrinsic Distribution Matching").
* Weber (2023)
  R. M. Weber
  The score-difference flow for implicit generative modeling.
  arXiv preprint arXiv:2304.12906.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Wu et al. (2025a)
  C. Wu, J. Li, J. Zhou, J. Lin, K. Gao, K. Yan, S. Yin, S. Bai, X. Xu, Y. Chen, et al.
  Qwen-image technical report.
  arXiv preprint arXiv:2508.02324.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px5.p1.1 "Text Rendering in Image Generation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p1.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§5.1](#S5.SS1.SSS0.Px1.p1.1 "Backbones and tuning. ‣ 5.1 Experimental Setup ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.16.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.22.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Wu et al. (2025b)
  C. Wu, X. Chen, Z. Wu, Y. Ma, X. Liu, Z. Pan, W. Liu, Z. Xie, X. Yu, C. Ruan, et al.
  Janus: decoupling visual encoding for unified multimodal understanding and generation.
  In Proceedings of the Computer Vision and Pattern Recognition Conference,
  pp. 12966–12977.
  Cited by: [Table 3](#S5.T3.4.1.8.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.7.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Wu et al. (2024)
  Y. Wu, Z. Zhang, J. Chen, H. Tang, D. Li, Y. Fang, L. Zhu, E. Xie, H. Yin, L. Yi, et al.
  Vila-u: a unified foundation model integrating visual understanding and generation.
  arXiv preprint arXiv:2409.04429.
  Cited by: [Table 3](#S5.T3.4.1.9.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Xie et al. (2024)
  J. Xie, W. Mao, Z. Bai, D. J. Zhang, W. Wang, K. Q. Lin, Y. Gu, Z. Chen, Z. Yang, and M. Z. Shou
  Show-o: one single transformer to unify multimodal understanding and generation.
  arXiv preprint arXiv:2408.12528.
  Cited by: [Table 2](#S5.T2.4.1.3.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 3](#S5.T3.4.1.10.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Xu et al. (2025)
  Y. Xu, W. Nie, and A. Vahdat
  One-step diffusion models with ff-divergence distribution matching.
  arXiv preprint arXiv:2502.15681.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§B.1.2](#A2.SS1.SSS2.p2.1 "B.1.2 𝑓-divergence specialization ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"),
  [§B.1.3](#A2.SS1.SSS3.p1.1 "B.1.3 Important special cases ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* Yang et al. (2026)
  J. Yang, Z. Geng, X. Ju, Y. Tian, and Y. Wang
  Representation fréchet loss for visual generation.
  arXiv:2604.28190.
  External Links: [Link](https://arxiv.org/abs/2604.28190)
  Cited by: [Appendix A](#A1.SS0.SSS0.Px3.p1.1 "Feature-Space Distribution Matching. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p5.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§4.2](#S4.SS2.SSS0.Px1.p1.1 "Intrinsic feature map. ‣ 4.2 Feature-Moment Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching").
* Yi et al. (2023)
  M. Yi, Z. Zhu, and S. Liu
  Monoflow: rethinking divergence gans via the perspective of wasserstein gradient flows.
  In International Conference on Machine Learning,
  pp. 39984–40000.
  Cited by: [§B.1.3](#A2.SS1.SSS3.p1.1 "B.1.3 Important special cases ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching").
* Yin et al. (2024a)
  T. Yin, M. Gharbi, T. Park, R. Zhang, E. Shechtman, F. Durand, and W. T. Freeman
  Improved distribution matching distillation for fast image synthesis.
  arXiv:2405.14867.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p2.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.27.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.7.1 "In 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 2](#S5.T2.4.1.21.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching"),
  [Table 4](#S5.T4.4.1.25.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").
* Yin et al. (2024b)
  T. Yin, M. Gharbi, R. Zhang, E. Shechtman, F. Durand, W. T. Freeman, and T. Park
  One-step diffusion with distribution matching distillation.
  In Proceedings of the IEEE/CVF conference on computer vision and pattern recognition,
  pp. 6613–6623.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [Appendix A](#A1.SS0.SSS0.Px2.p1.1 "Distribution Gradients and Internal Score Estimation. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§B.1.3](#A2.SS1.SSS3.Px1.p1.2 "Reverse KL / DMD. ‣ B.1.3 Important special cases ‣ B.1 Unified Gradient Structure ‣ Appendix B Theoretical Proofs ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p2.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§2](#S2.SS0.SSS0.Px3.p1.1 "Distribution Matching Distillation. ‣ 2 Background ‣ Intrinsic Distribution Matching"),
  [Table 1](#S5.T1.8.1.24.1 "In 5 Experiments ‣ Intrinsic Distribution Matching").
* Yu et al. (2024)
  S. Yu, S. Kwak, H. Jang, J. Jeong, J. Huang, J. Shin, and S. Xie
  Representation alignment for generation: training diffusion transformers is easier than you think.
  arXiv preprint arXiv:2410.06940.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px4.p1.1 "Gaussian Score Structure and Intrinsic Representations. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Zhang et al. (2026a)
  J. Zhang, K. Jiang, J. Chen, X. Wang, D. Liu, J. Li, D. Chen, M. Lin, J. Zhou, H. Jin, et al.
  Vidu s2: real-time interactive, editable, and spatial video generation.
  arXiv preprint arXiv:2609.11638.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching").
* Zhang et al. (2026b)
  Y. Zhang, C. Li, G. Ma, J. Zha, Y. Yang, B. Wang, W. Tang, W. Li, H. Huang, and N. Duan
  Teacher-feature drifting: one-step diffusion distillation with pretrained diffusion representations.
  arXiv preprint arXiv:2605.07327.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px3.p1.1 "Feature-Space Distribution Matching. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p5.1 "1 Introduction ‣ Intrinsic Distribution Matching"),
  [§4.2](#S4.SS2.SSS0.Px1.p1.1 "Intrinsic feature map. ‣ 4.2 Feature-Moment Loss ‣ 4 Intrinsic Distribution Matching ‣ Intrinsic Distribution Matching").
* Zheng et al. (2025)
  K. Zheng, Y. Wang, Q. Ma, H. Chen, J. Zhang, Y. Balaji, J. Chen, M. Liu, J. Zhu, and Q. Zhang
  Large scale diffusion distillation via score-regularized continuous-time consistency.
  arXiv preprint arXiv:2510.08431.
  Cited by: [Appendix A](#A1.SS0.SSS0.Px1.p1.1 "Fast Generative Models. ‣ Appendix A Related Work ‣ Intrinsic Distribution Matching"),
  [§1](#S1.p2.1 "1 Introduction ‣ Intrinsic Distribution Matching").
* Zhuo et al. (2024)
  L. Zhuo, R. Du, H. Xiao, Y. Li, D. Liu, R. Huang, W. Liu, X. Zhu, F. Wang, Z. Ma, et al.
  Lumina-next: making lumina-t2x stronger and faster with next-dit.
  Advances in Neural Information Processing Systems 37, pp. 131278–131315.
  Cited by: [Table 4](#S5.T4.4.1.4.1 "In General quality and efficiency. ‣ 5.2 Main Comparison ‣ 5 Experiments ‣ Intrinsic Distribution Matching").

## 附录 A 相关工作

**快速生成模型**。渐进蒸馏、一致性模型、shortcut 模型与 MeanFlow 通过学习生成轨迹上的转移或关系来减少采样步数（[Salimans and Ho, 2022](#bib.bib54)；[Song et al., 2023](#bib.bib52)；[Lu and Song, 2024](#bib.bib53)；[Frans et al., 2024](#bib.bib51)；[Geng et al., 2025a](#bib.bib55)；[Geng et al., 2026](#bib.bib62)）。Duality Models 用共享骨干同时预测速度与流映射（[Sun et al., 2026b](#bib.bib84)）。分布式方法使用对抗或基于分数的监督直接训练生成输出（[Sauer et al., 2023](#bib.bib7)；[Sauer et al., 2024](#bib.bib6)；[Yin et al., 2024b](#bib.bib16)；[Yin et al., 2024a](#bib.bib14)）。rCM 把连续时间一致性与分数正则相结合，并在大规模图像与视频模型上证明二者的互补性（[Zheng et al., 2025](#bib.bib66)）。LLaDA-Image-Turbo 支持两到四步推理，Vidu S2 则面向实时交互式视频生成与编辑（[Chen et al., 2026](#bib.bib87)；[Zhang et al., 2026a](#bib.bib85)）。IDM 研究来自生成器自身的分布式监督。

**分布梯度与内部分数估计**。DMD 用一个参考网络与一个在线伪分数模型估计加噪参考分布与生成分布之间的分数差（[Yin et al., 2024b](#bib.bib16)）；DMD2 增加了对抗监督与稳定少步蒸馏的技术（[Yin et al., 2024a](#bib.bib14)）。相关工作通过样本空间场把对抗更新与基于分数的更新联系起来（[Franceschi et al., 2023](#bib.bib76)；[Weber, 2023](#bib.bib77)），并把分布匹配推广到更广的散度族（[Xu et al., 2025](#bib.bib68)；[Wang et al., 2026](#bib.bib69)）。FlowCPO 为流模型的偏好对齐发展了一种离线前向 KL 表述（[Han et al., 2026b](#bib.bib86)）。TwinFlow 与 APEX 通过内部相互分离的速度分支估计分数差（[Cheng et al., 2025](#bib.bib56)；[Liu et al., 2026a](#bib.bib61)）。IDM 在内部 DMD 之上增加特征矩损失。

**特征空间分布匹配**。GMMN 与 MMD-GAN 使用矩差异或核差异进行生成训练（[Li et al., 2015](#bib.bib72)；[Li et al., 2017](#bib.bib73)）。FD-Loss 把全协方差高斯特征差异转化为训练目标，并用队列或 EMA 估计器把总体统计量与 batch 梯度联系起来（[Heusel et al., 2017](#bib.bib5)；[Yang et al., 2026](#bib.bib65)）。Three-Body Scattering 从冻结特征中的能量距离相互作用导出一步回归目标（[Sun et al., 2026a](#bib.bib81)）。Drifting 与 W-Flow 分别通过核相互作用与逐 batch 最优传输构造分布式更新（[Deng et al., 2026](#bib.bib64)；[Han et al., 2026a](#bib.bib63)），Teacher-Feature Drifting 则使用来自预训练教师模型的表示（[Zhang et al., 2026b](#bib.bib67)）。IDM 则在生成器的 EMA 特征空间中匹配特征均值与逐坐标标准差。

**高斯分数结构与内蕴表示**。[Wang and Vastola (2023)](#bib.bib79)；[Wang and Vastola (2024)](#bib.bib80)的高斯加残差分数表示是我们反向 KL 场分解的基础，也为额外的特征矩约束提供了动机。REPA 表明扩散 Transformer 的隐藏状态包含有用的语义信息，并可通过外部表示对齐予以强化（[Yu et al., 2024](#bib.bib11)）。Embedded Representation Warmup 在生成训练之前加入一个专门的表示对齐阶段（[Liu et al., 2025](#bib.bib60)）。我们的 EMA 特征映射复用了这类内部表示并随生成器演化；其效用与外部特征、教师模型特征及实时自身特征等替代方案在[第 5.3 节](#S5.SS3)中对比评估。

**图像生成中的文本渲染**。近期的文生图模型（包括 Qwen-Image 与 X-Omni）越来越重视准确的文本渲染（[Wu et al., 2025a](#bib.bib33)；[Geng et al., 2025b](#bib.bib83)）。LongText-Bench 在多种场景下评测中英文长文本（[Geng et al., 2025b](#bib.bib83)），与 OneIG 评估的更广维度形成互补（[Chang et al., 2026](#bib.bib82)）。Z-Image-Turbo++ 报告称 LongText 是有限采样预算下文本质量的敏感度量（[Liu et al., 2026b](#bib.bib50)）。我们关注 2 NFE 下的 LongText 表现。

## 附录 B 理论证明

**记号约定**。分布梯度与分数恒等式均在固定条件 $\mathbf{c}\sim p_{c}$ 下陈述，无歧义时省略条件；训练把所得的条件梯度对 $\mathbf{c}$ 取平均。与此相对，特征矩在联合分布 $p_{i}(\mathbf{x}\mid\mathbf{c})p_{c}(\mathbf{c})$ 上池化样本。下标 $t$ 表示加噪边际量，星号表示精确边际量，帽子表示学习或经验估计。因此 $\mathcal{L}_{\text{pop}}$ 表示总体矩损失，$\widehat{\mathcal{L}}_{\text{pop}}$ 为其经验对应物。对大小相等的满队列 $K$，模型估计器使用 $N_{\phi}=B+K$ 条特征（$B$ 为全局当前 batch 大小）；参考估计器使用 $K$ 条排队参考特征。

### B.1 统一梯度结构

#### B.1.1 一阶变分形式

我们给出正则性假设，并证明式 (5) 背后的一般恒等式。我们对服从连续性方程的密度泛函使用标准的一阶变分计算，即概率测度梯度流意义下的做法（[Ambrosio and Savaré, 2007](#bib.bib78)）。推前（pushforward）一步把样本空间积分转换为对噪声先验的期望，并厘清其对生成器参数的依赖。

###### 定义 B.1（分布梯度）

对存在可微一阶变分势 $\psi(\mathbf{x}):=\delta\mathcal{D}(p_{\theta},p_{r})/\delta p_{\theta}(\mathbf{x})$ 的分布差异 $\mathcal{D}(p_{\theta},p_{r})$，*样本空间分布梯度*定义为

$$
\mathbf{g}_{\mathcal{D}}(\mathbf{x}):=\nabla_{\mathbf{x}}\psi(\mathbf{x}).
\tag{15}
$$

###### 假设 1（一阶变分的正则性）

固定 $\mathbf{c}$，令 $G_{\theta}(\cdot,\mathbf{c})$ 把 $p_{z}$ 推前为 $p_{\theta}(\cdot\mid\mathbf{c})$。参考分布律 $p_{r}$ 固定，差异仅通过 $p_{\theta}$ 依赖于 $\theta$。对每个方向 $\Delta\theta$，定义 $\theta_{\epsilon}=\theta+\epsilon\Delta\theta$ 与 $p_{\theta_{\epsilon}}:=(G_{\theta_{\epsilon}}(\cdot,\mathbf{c}))_{\#}p_{z}$。

(a) $G_{\theta}$ 关于 $\theta$ 可微；

(b) $p_{\theta_{\epsilon}}$ 在 $\epsilon=0$ 附近存在光滑密度，且求导可与相关积分交换次序；

(c) 对下文使用的任意一阶变分势 $\psi$，分部积分中的边界项为零；例如 $\psi(\mathbf{x})p_{\theta}(\mathbf{x})\mathbf{u}(\mathbf{x})$ 在 $\|\mathbf{x}\|\to\infty$ 时衰减足够快。

##### 关于条件 (b)：模型律何时存在密度？

条件 (b) 是一个假设，而非生成器构造的推论。对局部 Lipschitz 的确定性映射 $G_{\theta}(\cdot,\mathbf{c}):\mathbb{R}^{d}\to\mathbb{R}^{d}$，面积公式表明：若 Jacobian $\partial G_{\theta}/\partial\mathbf{z}$ 在一个正 $p_{z}$ 测度集上奇异，则像分布律中会产生奇异分量。完整的模型律便不存在 Lebesgue 密度，其干净分数 $\mathbf{s}_{\theta}=\nabla_{\mathbf{x}}\log p_{\theta}$ 便不像假设的那样有定义。这并非病态情形：一个坍缩了种子空间某个方向的生成器——例如学会了忽略 $\mathbf{z}$ 的一部分——恰会产生这种退化。这正是 [Arjovsky et al. (2017)](#bib.bib57) 为隐式生成器指出的流形支撑障碍，他们因此主张用更弱的度量替代 f-散度；我们则保留散度，并显式携带密度假设。

因此，[第 3 节](#S3)的干净分布结果假设在公共定义域上存在光滑、严格正的密度，以及各条结果所需的可积性与边界条件。分解式 (5)、反向 KL 场 (3) 与分解 (7) 在该设定内是精确的。这一限制不同于加噪边际设定：加入独立的非退化高斯噪声后，即使干净律奇异，每个 $t\in(0,1)$ 也都有光滑正密度。因此[附录 B.3](#A2.SS3)的分数–速度恒等式不要求干净密度；其有限二阶矩假设足以支撑所述的速度回归。加噪反向 KL 目标还要求相关散度与梯度积分存在。[第 4 节](#S4)的实际损失无需计算干净分数即可求值。奇异的干净律使干净场的解释失效，但并不会自行使加噪分数场或特征矩目标失效。

###### 证明 B.2（式 (5) 的证明）

固定任意方向 $\Delta\theta$，写 $\theta_{\epsilon}=\theta+\epsilon\Delta\theta$。对 $\mathbf{x}=G_{\theta}(\mathbf{z},\mathbf{c})$，生成样本有一阶展开：

$$
\mathbf{x}_{\theta_{\epsilon}}=G_{\theta+\epsilon\Delta\theta}(\mathbf{z},\mathbf{c})=\mathbf{x}+\epsilon\mathbf{u}_{\mathbf{z}}+o(\epsilon),\qquad\mathbf{u}_{\mathbf{z}}:=J_{\theta}G_{\theta}(\mathbf{z},\mathbf{c})\Delta\theta.
\tag{16}
$$

对应的速度场是当前位于 $\mathbf{x}$ 的样本的条件平均位移：

$$
\mathbf{u}(\mathbf{x}):=\mathbb{E}\!\left[\mathbf{u}_{\mathbf{z}}\mid G_{\theta}(\mathbf{z},\mathbf{c})=\mathbf{x}\right].
\tag{17}
$$

我们首先识别该样本位移诱导的密度扰动。对任意光滑紧支撑的测试函数 $\varphi$，由推前定义与式 (16) 得

$$
\begin{aligned}
\frac{d}{d\epsilon}\int\varphi(\mathbf{x})p_{\theta_{\epsilon}}(\mathbf{x})\,\mathrm{d}\mathbf{x}\bigg|_{\epsilon=0}
&=\frac{d}{d\epsilon}\mathbb{E}_{\mathbf{z}}\left[\varphi(G_{\theta+\epsilon\Delta\theta}(\mathbf{z},\mathbf{c}))\right]\bigg|_{\epsilon=0}\\
&=\frac{d}{d\epsilon}\mathbb{E}_{\mathbf{z}}\left[\varphi(\mathbf{x}+\epsilon\mathbf{u}_{\mathbf{z}})\right]\bigg|_{\epsilon=0}\\
&=\mathbb{E}_{\mathbf{z}}\left[\nabla_{\mathbf{x}}\varphi(G_{\theta}(\mathbf{z},\mathbf{c}))^{\top}\mathbf{u}_{\mathbf{z}}\right]\\
&=\int\nabla_{\mathbf{x}}\varphi(\mathbf{x})^{\top}p_{\theta}(\mathbf{x})\mathbf{u}(\mathbf{x})\,\mathrm{d}\mathbf{x}.
\end{aligned}
\tag{18--21}
$$

最后一等式正是 $\mathbf{u}(\mathbf{x})$ 的条件期望定义。由于式 (21) 对所有这样的 $\varphi$ 成立，密度路径在弱意义下满足连续性方程：

$$
\partial_{\epsilon}p_{\theta_{\epsilon}}(\mathbf{x})\big|_{\epsilon=0}=-\nabla_{\mathbf{x}}\cdot(p_{\theta}(\mathbf{x})\mathbf{u}(\mathbf{x})).
\tag{22}
$$

现在考虑具有一阶变分的分布差异 $\mathcal{D}(p_{\theta},p_{r})$，

$$
\psi(\mathbf{x}):=\frac{\delta\mathcal{D}(p_{\theta},p_{r})}{\delta p_{\theta}}(\mathbf{x}),
\tag{23}
$$

其含义为：沿密度路径 $p_{\theta_{\epsilon}}$，

$$
\begin{aligned}
\frac{d}{d\epsilon}\mathcal{D}(p_{\theta_{\epsilon}},p_{r})\bigg|_{\epsilon=0}
&=\int\psi(\mathbf{x})\,\partial_{\epsilon}p_{\theta_{\epsilon}}(\mathbf{x})\big|_{\epsilon=0}\,\mathrm{d}\mathbf{x}\\
&=-\int\psi(\mathbf{x})\,\nabla_{\mathbf{x}}\cdot(p_{\theta}(\mathbf{x})\mathbf{u}(\mathbf{x}))\,\mathrm{d}\mathbf{x}\\
&=\int\nabla_{\mathbf{x}}\psi(\mathbf{x})\cdot p_{\theta}(\mathbf{x})\,\mathbf{u}(\mathbf{x})\,\mathrm{d}\mathbf{x},
\end{aligned}
\tag{24--26}
$$

其中最后一等式为分部积分，用到[假设 1](#Thminnerassumption1)(c) 中边界项为零。由式 (17)，任意可积向量场 $\mathbf{w}(\mathbf{x})$ 满足以下推前–期望恒等式（把 $p_{\theta}$ 下的期望转换为噪声先验下的期望）：

$$
\int p_{\theta}(\mathbf{x})\,\mathbf{w}(\mathbf{x})^{\top}\mathbf{u}(\mathbf{x})\,\mathrm{d}\mathbf{x}=\mathbb{E}_{\mathbf{z}}\left[\mathbf{w}(G_{\theta}(\mathbf{z},\mathbf{c}))^{\top}\mathbf{u}_{\mathbf{z}}\right].
\tag{27}
$$

在式 (27) 中取 $\mathbf{w}=\nabla_{\mathbf{x}}\psi$ 得

$$
\int p_{\theta}(\mathbf{x})\,\nabla_{\mathbf{x}}\psi(\mathbf{x})\cdot\mathbf{u}(\mathbf{x})\,\mathrm{d}\mathbf{x}=\mathbb{E}_{\mathbf{z}}\left[\nabla_{\mathbf{x}}\psi(G_{\theta}(\mathbf{z},\mathbf{c}))^{\top}\mathbf{u}_{\mathbf{z}}\right]=\mathbb{E}_{\mathbf{z}}\left[\nabla_{\mathbf{x}}\psi(G_{\theta}(\mathbf{z},\mathbf{c}))^{\top}J_{\theta}G_{\theta}(\mathbf{z},\mathbf{c})\Delta\theta\right].
\tag{28}
$$

结合式 (26) 与式 (28)，沿方向 $\Delta\theta$ 的方向导数为

$$
\frac{d}{d\epsilon}\mathcal{D}(p_{\theta_{\epsilon}},p_{r})\bigg|_{\epsilon=0}=\left\langle\mathbb{E}_{\mathbf{z}}\left[\bigl[J_{\theta}G_{\theta}(\mathbf{z},\mathbf{c})\bigr]^{\top}\nabla_{\mathbf{x}}\psi(G_{\theta}(\mathbf{z},\mathbf{c}))\right],\Delta\theta\right\rangle.
\tag{29}
$$

由于 $\Delta\theta$ 任意，

$$
\nabla_{\theta}\mathcal{D}(p_{\theta},p_{r})=\mathbb{E}_{\mathbf{z}}\left[\bigl[J_{\theta}G_{\theta}(\mathbf{z},\mathbf{c})\bigr]^{\top}\underbrace{\nabla_{\mathbf{x}}\psi(G_{\theta}(\mathbf{z},\mathbf{c}))}_{\mathbf{g}_{\mathcal{D}}(G_{\theta}(\mathbf{z},\mathbf{c}))}\right].
\tag{30}
$$

因此，只要差异具有一阶变分 $\psi=\delta\mathcal{D}(p_{\theta},p_{r})/\delta p_{\theta}$，式 (5) 的样本空间分布梯度即为 $\mathbf{g}_{\mathcal{D}}(\mathbf{x})=\nabla_{\mathbf{x}}\psi(\mathbf{x})$。

#### B.1.2 f-散度特化

这里 $\rho(\mathbf{x}):=p_{\theta}(\mathbf{x})/p_{r}(\mathbf{x})$ 表示密度比。

下面的模板是 [Xu et al. (2025)](#bib.bib68) 的 f-散度分布匹配结果，其变分形式可追溯至 f-GAN（[Nowozin et al., 2016](#bib.bib58)）。我们以本文记号重述，并在[附录 B.1.3](#A2.SS1.SSS3)补充一点区分：被识别出的 f-散度一阶变分与 detach 最优判别器的更新场，二者仅对特定生成器才一致。

###### 定理 B.3（f-散度的统一梯度模板）

设固定 $\mathbf{c}$ 下生成器为 $G_{\theta}(\mathbf{z},\mathbf{c})=\mathbf{x}$，$h:(0,\infty)\to\mathbb{R}$ 为二阶连续可微的凸散度生成子，且 $h(1)=0$，定义

$$
D_{h}(p_{\theta}\|p_{r})=\int p_{r}(\mathbf{x})h(\rho(\mathbf{x}))\,\mathrm{d}\mathbf{x},\qquad\rho(\mathbf{x}):=\frac{p_{\theta}(\mathbf{x})}{p_{r}(\mathbf{x})}.
\tag{31}
$$

假设[假设 1](#Thminnerassumption1)适用于 $\mathcal{L}[p_{\theta}]=D_{h}(p_{\theta}\|p_{r})$，并假设 $p_{\theta}$ 与 $p_{r}$ 在包含 $\operatorname{supp}(p_{\theta})$ 的某个开集上光滑且严格为正。则分布梯度为

$$
\mathbf{g}_{h}(\mathbf{x})=h^{\prime\prime}(\rho(\mathbf{x}))\,\rho(\mathbf{x})\,(\mathbf{s}_{\theta}(\mathbf{x})-\mathbf{s}_{r}(\mathbf{x})),
\tag{32}
$$

且

$$
\nabla_{\theta}D_{h}(p_{\theta}\|p_{r})={\mathbb{E}}_{\mathbf{z}\sim p_{z}}\left[\bigl[J_{\theta}G_{\theta}(\mathbf{z},\mathbf{c})\bigr]^{\top}\left[w(\mathbf{x})(\mathbf{s}_{\theta}(\mathbf{x})-\mathbf{s}_{r}(\mathbf{x}))\right]_{\mathbf{x}=G_{\theta}(\mathbf{z},\mathbf{c})}\right],
\tag{33}
$$

其中 $w(\mathbf{x})=h^{\prime\prime}(\rho(\mathbf{x}))\rho(\mathbf{x})$。

###### 证明 B.4

我们先固定 $p_{r}$，对模型密度 $p_{\theta}$ 计算一阶变分。设 $p_{\epsilon}=p_{\theta}+\epsilon\,\delta p$ 为允许的光滑扰动，$\int\delta p(\mathbf{x})\,\mathrm{d}\mathbf{x}=0$，并定义 $\rho_{\epsilon}(\mathbf{x}):=p_{\epsilon}(\mathbf{x})/p_{r}(\mathbf{x})$。由于 $p_{r}$ 固定，

$$
\rho_{\epsilon}(\mathbf{x})=\rho(\mathbf{x})+\epsilon\,\frac{\delta p(\mathbf{x})}{p_{r}(\mathbf{x})}.
\tag{34}
$$

因此导数为

$$
\begin{aligned}
\frac{d}{d\epsilon}D_{h}(p_{\epsilon}\|p_{r})\bigg|_{\epsilon=0}
&=\int p_{r}(\mathbf{x})\,\left[\frac{d}{d\epsilon}h\!\left(\rho_{\epsilon}(\mathbf{x})\right)\bigg|_{\epsilon=0}\,\right]\,\mathrm{d}\mathbf{x}\\
&=\int p_{r}(\mathbf{x})\,\left[\frac{d}{d\epsilon}h\!\left(\rho(\mathbf{x})+\epsilon\,\frac{\delta p(\mathbf{x})}{p_{r}(\mathbf{x})}\right)\bigg|_{\epsilon=0}\,\right]\,\mathrm{d}\mathbf{x}\\
&=\int p_{r}(\mathbf{x})\,h^{\prime}(\rho(\mathbf{x}))\,\frac{\delta p(\mathbf{x})}{p_{r}(\mathbf{x})}\,\mathrm{d}\mathbf{x}\\
&=\int h^{\prime}(\rho(\mathbf{x}))\,\delta p(\mathbf{x})\,\mathrm{d}\mathbf{x}.
\end{aligned}
\tag{35--38}
$$

按定义，一阶变分势是任意与每个允许密度扰动 $\delta p$ 配对都给出方向导数的函数 $\psi_{h}$：

$$
\frac{d}{d\epsilon}D_{h}(p_{\theta}+\epsilon\,\delta p\|p_{r})\bigg|_{\epsilon=0}=\int\psi_{h}(\mathbf{x})\,\delta p(\mathbf{x})\,\mathrm{d}\mathbf{x}.
\tag{39}
$$

把这一刻画式 (39) 与式 (38) 比较，可识别出

$$
\psi_{h}(\mathbf{x}):=\frac{\delta D_{h}}{\delta p_{\theta}}(\mathbf{x})=h^{\prime}(\rho(\mathbf{x})).
\tag{40}
$$

该识别在允许扰动的支撑上相差一个加性常数是唯一的，因为 $\int\delta p(\mathbf{x})\,\mathrm{d}\mathbf{x}=0$，且

$$
\int\bigl(\psi_{h}(\mathbf{x})+c_{0}\bigr)\delta p(\mathbf{x})\,\mathrm{d}\mathbf{x}=\int\psi_{h}(\mathbf{x})\delta p(\mathbf{x})\,\mathrm{d}\mathbf{x}
\tag{41}
$$

对任意标量常数 $c_{0}$（区别于条件向量 $\mathbf{c}$）成立。

现在计算样本空间场。由链式法则，

$$
\nabla_{\mathbf{x}}\psi_{h}(\mathbf{x})=h^{\prime\prime}(\rho(\mathbf{x}))\nabla_{\mathbf{x}}\rho(\mathbf{x}).
\tag{42}
$$

剩下把 $\nabla_{\mathbf{x}}\rho$ 用两个分数表示。由 $\rho=p_{\theta}/p_{r}$ 且两个密度均为正，

$$
\nabla_{\mathbf{x}}\rho(\mathbf{x})=\frac{\nabla_{\mathbf{x}}p_{\theta}(\mathbf{x})}{p_{r}(\mathbf{x})}-\frac{p_{\theta}(\mathbf{x})\nabla_{\mathbf{x}}p_{r}(\mathbf{x})}{p_{r}(\mathbf{x})^{2}}.
\tag{43}
$$

利用 $\nabla_{\mathbf{x}}p_{\theta}=p_{\theta}\mathbf{s}_{\theta}$ 与 $\nabla_{\mathbf{x}}p_{r}=p_{r}\mathbf{s}_{r}$，上式变为

$$
\begin{aligned}
\nabla_{\mathbf{x}}\rho(\mathbf{x})
&=\frac{p_{\theta}(\mathbf{x})\mathbf{s}_{\theta}(\mathbf{x})}{p_{r}(\mathbf{x})}-\frac{p_{\theta}(\mathbf{x})p_{r}(\mathbf{x})\mathbf{s}_{r}(\mathbf{x})}{p_{r}(\mathbf{x})^{2}}\\
&=\rho(\mathbf{x})\bigl(\mathbf{s}_{\theta}(\mathbf{x})-\mathbf{s}_{r}(\mathbf{x})\bigr).
\end{aligned}
\tag{44}
$$

把该恒等式代入式 (42) 得

$$
\nabla_{\mathbf{x}}\psi_{h}(\mathbf{x})=h^{\prime\prime}(\rho(\mathbf{x}))\,\rho(\mathbf{x})(\mathbf{s}_{\theta}(\mathbf{x})-\mathbf{s}_{r}(\mathbf{x})).
\tag{45}
$$

于是分布梯度为

$$
\mathbf{g}_{h}(\mathbf{x})=\nabla_{\mathbf{x}}\psi_{h}(\mathbf{x})=h^{\prime\prime}(\rho(\mathbf{x}))\,\rho(\mathbf{x})(\mathbf{s}_{\theta}(\mathbf{x})-\mathbf{s}_{r}(\mathbf{x})).
\tag{46}
$$

最后，把一般的一阶变分模板式 (30) 应用于 $\mathcal{L}[p_{\theta}]=D_{h}(p_{\theta}\|p_{r})$，得

$$
\begin{aligned}
\nabla_{\theta}D_{h}(p_{\theta}\|p_{r})
&={\mathbb{E}}_{\mathbf{z}\sim p_{z}}\left[\bigl[J_{\theta}G_{\theta}(\mathbf{z},\mathbf{c})\bigr]^{\top}\mathbf{g}_{h}(G_{\theta}(\mathbf{z},\mathbf{c}))\right]\\
&={\mathbb{E}}_{\mathbf{z}\sim p_{z}}\left[\bigl[J_{\theta}G_{\theta}(\mathbf{z},\mathbf{c})\bigr]^{\top}\left[h^{\prime\prime}(\rho(\mathbf{x}))\,\rho(\mathbf{x})(\mathbf{s}_{\theta}(\mathbf{x})-\mathbf{s}_{r}(\mathbf{x}))\right]_{\mathbf{x}=G_{\theta}(\mathbf{z},\mathbf{c})}\right].
\end{aligned}
\tag{47}
$$

取 $w(\mathbf{x})=h^{\prime\prime}(\rho(\mathbf{x}))\rho(\mathbf{x})$，这正是式 (33)。

#### B.1.3 重要特例

密度比加权形式 $w(\mathbf{x})(\mathbf{s}_{\theta}-\mathbf{s}_{r})$（其中 $w=h^{\prime\prime}(\rho)\rho$）是 [Xu et al. (2025)](#bib.bib68) 的一步 f-散度模板，后被 [Wang et al. (2026)](#bib.bib69) 推广到更广的散度族；把 GAN 的最优判别器场解读为加权分数差则源自 [Yi et al. (2023)](#bib.bib75)。

##### 反向 KL / DMD

取 $h(\rho)=\rho\log\rho$，有 $h^{\prime\prime}(\rho)=1/\rho$，故 $w=\rho h^{\prime\prime}(\rho)=1$。分布梯度因此为

$$
\mathbf{g}_{\mathrm{KL}}(\mathbf{x})=\mathbf{s}_{\theta}(\mathbf{x})-\mathbf{s}_{r}(\mathbf{x}).
\tag{48}
$$

这是理想的反向 KL 场；实际 DMD 用近似的参考模型与在线伪分数模型估计其加噪边际对应物，即分数差分量。它并非完整的 DMD 目标：原始方法还在预生成的教师样本对上使用 LPIPS 回归项，且其有限训练下的在线伪分数估计可能滞后或有偏（[Yin et al., 2024b](#bib.bib16)）。对应的样本空间下降方向为 $-\mathbf{g}_{\mathrm{KL}}=\mathbf{s}_{r}-\mathbf{s}_{\theta}$。

##### 缩放 Jensen–Shannon / 饱和 GAN

取两倍于常规等混合 JSD 的生成子（该缩放系数是为匹配饱和 GAN 场而选的），

$$
h_{\mathrm{JSD}}(\rho)=\rho\log\rho-(1+\rho)\log\frac{1+\rho}{2},
\tag{49}
$$

有

$$
h_{\mathrm{JSD}}^{\prime\prime}(\rho)=\frac{1}{\rho(1+\rho)},\qquad w_{\mathrm{JSD}}(\rho)=\frac{1}{1+\rho}=D^{*}(\mathbf{x}),
\tag{50}
$$

其中 $D^{*}(\mathbf{x})=p_{r}/(p_{r}+p_{\theta})$ 为最优真实概率判别器（[Goodfellow et al., 2014](#bib.bib4)）（此处上标 $*$ 表示最优性，与它处表示精确边际速度场的用法不同）。

##### detach 最优判别器的生成器更新

假设光滑正密度与精确的最优判别器。我们固定判别器参数，但保留对其输入的导数。在 $D^{*}(\mathbf{x})=p_{r}/(p_{r}+p_{\theta})$ 下，有 $1-D^{*}=p_{\theta}/(p_{r}+p_{\theta})$。对饱和目标 $\ell_{\mathrm{sat}}(\mathbf{x})=\log(1-D^{*}(\mathbf{x}))=\log p_{\theta}-\log(p_{r}+p_{\theta})$：

$$
\begin{aligned}
\nabla_{\mathbf{x}}\ell_{\mathrm{sat}}(\mathbf{x})
&=\mathbf{s}_{\theta}(\mathbf{x})-\frac{p_{r}\,\mathbf{s}_{r}(\mathbf{x})+p_{\theta}\,\mathbf{s}_{\theta}(\mathbf{x})}{p_{r}+p_{\theta}}\\
&=\mathbf{s}_{\theta}-D^{*}\mathbf{s}_{r}-(1-D^{*})\mathbf{s}_{\theta}=D^{*}(\mathbf{x})(\mathbf{s}_{\theta}(\mathbf{x})-\mathbf{s}_{r}(\mathbf{x}))\,.
\end{aligned}
\tag{51}
$$

对非饱和目标 $\ell_{\mathrm{ns}}(\mathbf{x})=-\log D^{*}(\mathbf{x})=\log(p_{r}+p_{\theta})-\log p_{r}$：

$$
\begin{aligned}
\nabla_{\mathbf{x}}\ell_{\mathrm{ns}}(\mathbf{x})
&=\frac{p_{r}\,\mathbf{s}_{r}(\mathbf{x})+p_{\theta}\,\mathbf{s}_{\theta}(\mathbf{x})}{p_{r}+p_{\theta}}-\mathbf{s}_{r}(\mathbf{x})\\
&=D^{*}\mathbf{s}_{r}+(1-D^{*})\mathbf{s}_{\theta}-\mathbf{s}_{r}=(1-D^{*}(\mathbf{x}))(\mathbf{s}_{\theta}(\mathbf{x})-\mathbf{s}_{r}(\mathbf{x}))\,.
\end{aligned}
\tag{52}
$$

饱和场与上文缩放 JSD 的分布梯度一致；非饱和场则是 detach 最优判别器的生成器更新。

##### 特例汇总

| 目标 / 散度 | $h(\rho)$ | $h^{\prime\prime}(\rho)$ | $w=h^{\prime\prime}(\rho)\cdot\rho$ |
| --- | --- | --- | --- |
| 反向 KL（DMD） | $\rho\log\rho$ | $1/\rho$ | $1$ |
| 缩放 JSD（$2\times$JSD） | $\rho\log\rho-(1{+}\rho)\log\frac{1{+}\rho}{2}$ | $\frac{1}{\rho(1{+}\rho)}$ | $\frac{1}{1{+}\rho}=D^{*}$ |
| NS-GAN detach 更新 | —† | — | $1-D^{*}$ |
| 饱和 GAN | 上行缩放 JSD | 同上 | $D^{*}$ |

这里 † 表示该行只是 detach 最优 $D^{*}$ 的生成器更新场，并非被识别出的 f-散度一阶变分；饱和 GAN 行即上一行中的缩放 $2{\times}$JSD 场。

### B.2 反向 KL 场的分数分解

#### B.2.1 分数分解恒等式

###### 定义 B.5（矩匹配高斯）

对 $\mathbb{R}^{d}$ 上任意具有有限一阶与二阶矩、且协方差正定的分布 $p$，定义其*矩匹配高斯*为

$$
q_{p}:=\mathcal{N}(\mu_{p},\Sigma_{p})\,,\qquad\mu_{p}:=\mathbb{E}_{p}[\mathbf{x}]\,,\quad\Sigma_{p}:=\operatorname{Cov}_{p}(\mathbf{x})\,.
\tag{53}
$$

###### 定义 B.6（非高斯分数残差）

对任意满足[定义 B.5](#A2.Thmtheorem5)的光滑分布 $p$，其分数为 $\mathbf{s}_{p}(\mathbf{x})=\nabla_{\mathbf{x}}\log p(\mathbf{x})$、矩匹配高斯为 $q_{p}$，定义非高斯分数残差为

$$
\bm{\eta}_{p}(\mathbf{x}):=\mathbf{s}_{p}(\mathbf{x})-\mathbf{s}_{q_{p}}(\mathbf{x})\,,
\tag{54}
$$

其中 $\mathbf{s}_{q_{p}}(\mathbf{x})=-\Sigma_{p}^{-1}(\mathbf{x}-\mu_{p})$。

于是，基于[定义 B.5](#A2.Thmtheorem5)与[定义 B.6](#A2.Thmtheorem6)，任意分布 $p$ 的分数函数可分解为

$$
\mathbf{s}_{p}(\mathbf{x})=\mathbf{s}_{q_{p}}(\mathbf{x})+\bm{\eta}_{p}(\mathbf{x})\,.
\tag{55}
$$

这就是正文式 (6) 中的*分数分解*。

#### B.2.2 残差的正交性

我们使用 Stein 恒等式的标量测试函数形式（[Liu et al., 2016](#bib.bib70)，定义 2.1 与引理 2.2）。若 $\varphi:\mathbb{R}^{d}\to\mathbb{R}$ 属于 $p$ 的 Stein 类，则

$$
\mathbb{E}_{p}[\mathbf{s}_{p}(\mathbf{x})\varphi(\mathbf{x})+\nabla_{\mathbf{x}}\varphi(\mathbf{x})]=\mathbf{0}.
\tag{56}
$$

[引理 B.7](#A2.Thmtheorem7)中的两个恒等式分别对应 $\varphi(\mathbf{x})=1$ 与 $\varphi(\mathbf{x})=x_{l}$。为清晰起见，我们给出逐坐标的证明。

###### 引理 B.7（分数 Stein 恒等式）

设 $p$ 为 $\mathbb{R}^{d}$ 上严格正的光滑密度，分数为 $\mathbf{s}_{p}(\mathbf{x})=\nabla_{\mathbf{x}}\log p(\mathbf{x})$。假设

$$
\mathbb{E}_{p}[\|\mathbf{s}_{p}(\mathbf{x})\|]<\infty,\qquad\mathbb{E}_{p}[\|\mathbf{x}\|\,\|\mathbf{s}_{p}(\mathbf{x})\|]<\infty.
\tag{57}
$$

对 $B_{R}=\{\mathbf{x}:\|\mathbf{x}\|\leq R\}$，令 $n_{k}$ 为 $\partial B_{R}$ 上单位外法向量的第 $k$ 个坐标。另假设对所有坐标 $(k,l)$，以下边界条件成立：

$$
\lim_{R\to\infty}\int_{\partial B_{R}}p(\mathbf{x})n_{k}\,\mathrm{d}S=0,\qquad\lim_{R\to\infty}\int_{\partial B_{R}}p(\mathbf{x})x_{l}n_{k}\,\mathrm{d}S=0.
\tag{58}
$$

则

$$
\mathbb{E}_{p}[\mathbf{s}_{p}(\mathbf{x})]=\mathbf{0},\qquad\mathbb{E}_{p}[\mathbf{s}_{p}(\mathbf{x})\mathbf{x}^{\top}]=-\mathbf{I}_{d}.
\tag{59}
$$

###### 证明 B.8

由于 $p(\mathbf{x})\mathbf{s}_{p}(\mathbf{x})=\nabla_{\mathbf{x}}p(\mathbf{x})$，$\mathbb{E}_{p}[\mathbf{s}_{p}(\mathbf{x})]$ 的第 $k$ 个坐标为

$$
\mathbb{E}_{p}[[\mathbf{s}_{p}(\mathbf{x})]_{k}]=\int\frac{\partial p(\mathbf{x})}{\partial x_{k}}\,\mathrm{d}\mathbf{x}.
\tag{60}
$$

在 $B_{R}$ 上用散度定理，

$$
\int_{B_{R}}\frac{\partial p(\mathbf{x})}{\partial x_{k}}\,\mathrm{d}\mathbf{x}=\int_{\partial B_{R}}p(\mathbf{x})n_{k}\,\mathrm{d}S.
\tag{61}
$$

由式 (57)，体积被积函数绝对可积。令 $R\to\infty$ 并使用式 (58) 的第一个极限，得

$$
\int\frac{\partial p(\mathbf{x})}{\partial x_{k}}\,\mathrm{d}\mathbf{x}=0.
\tag{62}
$$

由于这对每个 $k$ 都成立，

$$
\mathbb{E}_{p}[\mathbf{s}_{p}(\mathbf{x})]=\mathbf{0}.
\tag{63}
$$

对第二个恒等式，固定坐标 $(k,l)$。再次由散度定理，

$$
\int_{B_{R}}\frac{\partial}{\partial x_{k}}\!\left[p(\mathbf{x})x_{l}\right]\,\mathrm{d}\mathbf{x}=\int_{\partial B_{R}}p(\mathbf{x})x_{l}n_{k}\,\mathrm{d}S.
\tag{64}
$$

式 (57) 的第二个条件使展开后的导数可积。令 $R\to\infty$ 并使用式 (58) 的第二个极限，得

$$
\int\frac{\partial}{\partial x_{k}}\!\left[p(\mathbf{x})x_{l}\right]\,\mathrm{d}\mathbf{x}=0.
\tag{65}
$$

展开导数得

$$
\frac{\partial}{\partial x_{k}}\!\left[p(\mathbf{x})x_{l}\right]=\frac{\partial p(\mathbf{x})}{\partial x_{k}}x_{l}+p(\mathbf{x})\delta_{kl}=p(\mathbf{x})[\mathbf{s}_{p}(\mathbf{x})]_{k}x_{l}+p(\mathbf{x})\delta_{kl},
\tag{66}
$$

其中 $\delta_{kl}$ 为 Kronecker δ。积分并利用 $\int p(\mathbf{x})\,\mathrm{d}\mathbf{x}=1$，得

$$
\mathbb{E}_{p}\!\left[[\mathbf{s}_{p}(\mathbf{x})]_{k}x_{l}\right]+\delta_{kl}=0.
\tag{67}
$$

于是对所有 $(k,l)$ 有 $\mathbb{E}_{p}[[\mathbf{s}_{p}(\mathbf{x})]_{k}x_{l}]=-\delta_{kl}$，写成矩阵形式即

$$
\mathbb{E}_{p}[\mathbf{s}_{p}(\mathbf{x})\mathbf{x}^{\top}]=-\mathbf{I}_{d}.
\tag{68}
$$

###### 命题 B.9（非高斯分数残差的正交性）

设 $p$ 为 $\mathbb{R}^{d}$ 上严格正的光滑密度，具有有限二阶矩与正定协方差 $\Sigma_{p}$。假设可积性条件 (57) 与边界条件 (58)。由 Cauchy–Schwarz 不等式，有限 Fisher 信息加上有限二阶矩足以保证式 (57)。则非高斯分数残差 $\bm{\eta}_{p}=\mathbf{s}_{p}-\mathbf{s}_{q_{p}}$ 满足

(i) $\mathbb{E}_{p}[\bm{\eta}_{p}(\mathbf{x})]=\mathbf{0}$；

(ii) $\mathbb{E}_{p}[\bm{\eta}_{p}(\mathbf{x})\mathbf{x}^{\top}]=\mathbf{0}_{d\times d}$。

###### 证明 B.10

第一步：分数 Stein 恒等式。由[引理 B.7](#A2.Thmtheorem7)，

$$
\mathbb{E}_{p}[\mathbf{s}_{p}(\mathbf{x})]=\mathbf{0},\qquad\mathbb{E}_{p}[\mathbf{s}_{p}(\mathbf{x})\mathbf{x}^{\top}]=-\mathbf{I}_{d}.
\tag{69}
$$

第二步：矩匹配高斯在 $p$ 下满足同样的两个恒等式。由定义，$q_{p}=\mathcal{N}(\mu_{p},\Sigma_{p})$ 的分数为

$$
\mathbf{s}_{q_{p}}(\mathbf{x})=-\Sigma_{p}^{-1}(\mathbf{x}-\mu_{p}).
\tag{70}
$$

在 $p$ 下取期望得

$$
\mathbb{E}_{p}[\mathbf{s}_{q_{p}}(\mathbf{x})]=-\Sigma_{p}^{-1}\bigl(\mathbb{E}_{p}[\mathbf{x}]-\mu_{p}\bigr)=\mathbf{0}.
\tag{71}
$$

对一阶矩恒等式，

$$
\begin{aligned}
\mathbb{E}_{p}[\mathbf{s}_{q_{p}}(\mathbf{x})\mathbf{x}^{\top}]
&=-\Sigma_{p}^{-1}\mathbb{E}_{p}[(\mathbf{x}-\mu_{p})\mathbf{x}^{\top}]
=-\Sigma_{p}^{-1}\mathbb{E}_{p}[(\mathbf{x}-\mu_{p})((\mathbf{x}-\mu_{p})+\mu_{p})^{\top}]\\
&=-\Sigma_{p}^{-1}\left(\mathbb{E}_{p}[(\mathbf{x}-\mu_{p})(\mathbf{x}-\mu_{p})^{\top}]+\mathbb{E}_{p}[\mathbf{x}-\mu_{p}]\mu_{p}^{\top}\right)
=-\Sigma_{p}^{-1}\Sigma_{p}=-\mathbf{I}_{d}\,.
\end{aligned}
\tag{72}
$$

第三步：从真分数恒等式中减去高斯恒等式。由 $\bm{\eta}_{p}=\mathbf{s}_{p}-\mathbf{s}_{q_{p}}$，[引理 B.7](#A2.Thmtheorem7)与第二步蕴含

$$
\mathbb{E}_{p}[\bm{\eta}_{p}(\mathbf{x})]=\mathbb{E}_{p}[\mathbf{s}_{p}(\mathbf{x})]-\mathbb{E}_{p}[\mathbf{s}_{q_{p}}(\mathbf{x})]=\mathbf{0}.
\tag{73}
$$

类似地，

$$
\mathbb{E}_{p}[\bm{\eta}_{p}(\mathbf{x})\mathbf{x}^{\top}]=\mathbb{E}_{p}[\mathbf{s}_{p}(\mathbf{x})\mathbf{x}^{\top}]-\mathbb{E}_{p}[\mathbf{s}_{q_{p}}(\mathbf{x})\mathbf{x}^{\top}]=-\mathbf{I}_{d}-(-\mathbf{I}_{d})=\mathbf{0}_{d\times d}.
\tag{74}
$$

最后，合并 (i) 与 (ii) 得等价的中心化形式：

$$
\mathbb{E}_{p}[\bm{\eta}_{p}(\mathbf{x})(\mathbf{x}-\mu_{p})^{\top}]=\mathbb{E}_{p}[\bm{\eta}_{p}(\mathbf{x})\mathbf{x}^{\top}]-\mathbb{E}_{p}[\bm{\eta}_{p}(\mathbf{x})]\mu_{p}^{\top}=\mathbf{0}_{d\times d}.
\tag{75}
$$

#### B.2.3 反向 KL 场分解

###### 定理 B.11（反向 KL 场分解）

假设 $p_{\theta}$ 与 $p_{r}$ 为满足[定义 B.5](#A2.Thmtheorem5)的严格正光滑密度，对 $i\in\{r,\theta\}$ 记 $q_{i}:=q_{p_{i}}$、$\bm{\eta}_{i}:=\bm{\eta}_{p_{i}}$。对反向 KL 分布梯度 $\mathbf{g}_{\mathrm{KL}}(\mathbf{x})=\mathbf{s}_{\theta}(\mathbf{x})-\mathbf{s}_{r}(\mathbf{x})$，

$$
\mathbf{g}_{\mathrm{KL}}(\mathbf{x})=\underbrace{\left(\mathbf{s}_{q_{\theta}}(\mathbf{x})-\mathbf{s}_{q_{r}}(\mathbf{x})\right)}_{\mathbf{g}_{\mathrm{KL}}^{\mathrm{G}}(\mathbf{x}):\;\text{高斯矩分量}}+\underbrace{\left(\bm{\eta}_{\theta}(\mathbf{x})-\bm{\eta}_{r}(\mathbf{x})\right)}_{\mathbf{g}_{\mathrm{KL}}^{\mathrm{nG}}(\mathbf{x}):\;\text{非高斯残差分量}}
\tag{76}
$$

其中 $\mathbf{g}_{\mathrm{KL}}^{\mathrm{G}}(\mathbf{x})=-\Sigma_{\theta}^{-1}(\mathbf{x}-\mu_{\theta})+\Sigma_{r}^{-1}(\mathbf{x}-\mu_{r})$ 只依赖前两阶矩，而 $\mathbf{g}_{\mathrm{KL}}^{\mathrm{nG}}(\mathbf{x})=\bm{\eta}_{\theta}(\mathbf{x})-\bm{\eta}_{r}(\mathbf{x})$ 刻画其余分数结构。这一精确分解是对未加权的反向 KL 场陈述的。对一般的 f-散度场 $w(\mathbf{x})(\mathbf{s}_{\theta}-\mathbf{s}_{r})$，代数分解要乘上 $w(\mathbf{x})$，但加权之后残差的正交恒等式未必保持。

###### 证明 B.12

对 $\mathbf{s}_{\theta}$ 与 $\mathbf{s}_{r}$ 都应用式 (55) 的分数分解：

$$
\begin{aligned}
\mathbf{s}_{\theta}(\mathbf{x})-\mathbf{s}_{r}(\mathbf{x})
&=\left[\mathbf{s}_{q_{\theta}}(\mathbf{x})+\bm{\eta}_{\theta}(\mathbf{x})\right]-\left[\mathbf{s}_{q_{r}}(\mathbf{x})+\bm{\eta}_{r}(\mathbf{x})\right]\\
&=\underbrace{\left(\mathbf{s}_{q_{\theta}}(\mathbf{x})-\mathbf{s}_{q_{r}}(\mathbf{x})\right)}_{\mathbf{g}_{\mathrm{KL}}^{\mathrm{G}}}+\underbrace{\left(\bm{\eta}_{\theta}(\mathbf{x})-\bm{\eta}_{r}(\mathbf{x})\right)}_{\mathbf{g}_{\mathrm{KL}}^{\mathrm{nG}}}\,.
\end{aligned}
\tag{77}
$$

#### B.2.4 对角形式及其与估计器的联系

在对角情形 $\Sigma_{i}=\operatorname{diag}(\sigma_{i,1}^{2},\ldots,\sigma_{i,d}^{2})$，其中 $\sigma_{i,j}>0$ 为 $p_{i}$ 下坐标 $j$ 的标准差，$i\in\{r,\theta\}$，

$$
g^{\mathrm{G}}_{\mathrm{KL},j}(\mathbf{x}):=[\mathbf{g}_{\mathrm{KL}}^{\mathrm{G}}(\mathbf{x})]_{j}=[-\Sigma_{\theta}^{-1}(\mathbf{x}-\mu_{\theta})+\Sigma_{r}^{-1}(\mathbf{x}-\mu_{r})]_{j}=-\frac{x_{j}-\mu_{\theta,j}}{\sigma_{\theta,j}^{2}}+\frac{x_{j}-\mu_{r,j}}{\sigma_{r,j}^{2}}\,.
\tag{78}
$$

要求对一切 $\mathbf{x}$ 有 $g^{\mathrm{G}}_{\mathrm{KL},j}(\mathbf{x})=0$，迫使 $x_{j}$ 的系数为零：

$$
\frac{1}{\sigma_{r,j}^{2}}-\frac{1}{\sigma_{\theta,j}^{2}}=0\;\;\Longrightarrow\;\;\sigma_{\theta,j}=\sigma_{r,j}\,.
\tag{79}
$$

代回常数项得 $\mu_{\theta,j}=\mu_{r,j}$。在同一坐标空间中，这是对角高斯矩匹配的不动点条件；式 (13) 在池化特征矩上施加的是类似条件。在 $\phi$ 空间中，[命题 B.20](#A2.Thmtheorem20)的矩匹配梯度定义了一个由 $\mathbf{g}_{\mathrm{KL}}^{\mathrm{G}}$ 启发的池化特征空间正则项。在固定的特征映射参数与队列下，令 $\mathbf{h}_{k}=\phi_{\bar{\theta}}(\mathbf{x}_{k},\mathbf{c}_{k})$ 为一条当前模型特征。其经验样本梯度贡献为

$$
\frac{\partial\widehat{\mathcal{L}}_{\text{pop}}}{\partial\mathbf{x}_{k}}=\bigl[J_{\mathbf{x}}\phi_{\bar{\theta}}(\mathbf{x}_{k},\mathbf{c}_{k})\bigr]^{\top}\frac{\partial\widehat{\mathcal{L}}_{\text{pop}}}{\partial\mathbf{h}_{k}},
\tag{80}
$$

其中 $J_{\mathbf{x}}\phi_{\bar{\theta}}:=\partial\phi_{\bar{\theta}}/\partial\mathbf{x}$，特征导数由[命题 B.20](#A2.Thmtheorem20)给出。因此特征矩损失是一个由 $\mathbf{g}_{\mathrm{KL}}^{\mathrm{G}}$ 启发的池化特征空间矩正则项，而不是对它的估计。

[第 4.1 节](#S4.SS1)DMD 损失中的内部速度差，经由式 (9) 给出对完整加噪反向 KL 场（含矩分量与残差分量）的估计。特征矩损失在这一逐点信号之外，对池化特征统计量施加显式约束。该信号是否具有更低的经验梯度方差是一个实验问题，并非该分解的推论。

#### B.2.5 经 $L^{2}$ 投影的变分刻画

分数分解 (6) 有一个变分诠释，说明矩匹配高斯并非随意之选，而是唯一的最佳仿射近似。

假设 $p$ 满足[命题 B.9](#A2.Thmtheorem9)的正则条件，且具有有限 Fisher 信息：

$$
\mathbb{E}_{p}[\|\mathbf{s}_{p}(\mathbf{x})\|^{2}]=\mathbb{E}_{p}[\|\nabla_{\mathbf{x}}\log p(\mathbf{x})\|^{2}]<\infty.
\tag{81}
$$

这保证下述 $L^{2}(p)$ 优化问题是适定的。考虑在 $L^{2}(p)$ 中用仿射函数逼近分数函数 $\mathbf{s}_{p}$：

$$
\min_{\mathbf{A}\in\mathbb{R}^{d\times d},\mathbf{b}\in\mathbb{R}^{d}}\;\mathbb{E}_{p}[\|\mathbf{s}_{p}(\mathbf{x})-(\mathbf{A}\mathbf{x}+\mathbf{b})\|^{2}].
\tag{82}
$$

该最小二乘问题的一阶最优性条件（法方程）为：

$$
\mathbb{E}_{p}[\mathbf{s}_{p}(\mathbf{x})-(\mathbf{A}\mathbf{x}+\mathbf{b})]=\mathbf{0},\qquad\mathbb{E}_{p}[(\mathbf{s}_{p}(\mathbf{x})-(\mathbf{A}\mathbf{x}+\mathbf{b}))\mathbf{x}^{\top}]=\mathbf{0}.
\tag{83--84}
$$

这正是正交条件 (8)。为解出 $\mathbf{A}$ 与 $\mathbf{b}$，展开第一个条件：

$$
\mathbb{E}_{p}[\mathbf{s}_{p}(\mathbf{x})]=\mathbf{A}\mathbb{E}_{p}[\mathbf{x}]+\mathbf{b}.
\tag{85}
$$

由[引理 B.7](#A2.Thmtheorem7)的 Stein 恒等式，$\mathbb{E}_{p}[\mathbf{s}_{p}(\mathbf{x})]=\mathbf{0}$ 且 $\mathbb{E}_{p}[\mathbf{x}]=\mu_{p}$，故

$$
\mathbf{b}=-\mathbf{A}\mu_{p}.
\tag{86}
$$

代入第二个条件并展开：

$$
\begin{aligned}
\mathbb{E}_{p}[\mathbf{s}_{p}(\mathbf{x})\mathbf{x}^{\top}]
&=\mathbf{A}\mathbb{E}_{p}[\mathbf{x}\mathbf{x}^{\top}]+\mathbf{b}\mathbb{E}_{p}[\mathbf{x}]^{\top}
=\mathbf{A}\mathbb{E}_{p}[\mathbf{x}\mathbf{x}^{\top}]-\mathbf{A}\mu_{p}\mu_{p}^{\top}\\
&=\mathbf{A}(\mathbb{E}_{p}[\mathbf{x}\mathbf{x}^{\top}]-\mu_{p}\mu_{p}^{\top})
=\mathbf{A}\Sigma_{p}.
\end{aligned}
\tag{87--90}
$$

再次由 Stein 恒等式，$\mathbb{E}_{p}[\mathbf{s}_{p}(\mathbf{x})\mathbf{x}^{\top}]=-\mathbf{I}_{d}$，于是

$$
\mathbf{A}=-\Sigma_{p}^{-1}.
\tag{91}
$$

结合式 (86) 与式 (91) 即恢复

$$
\mathbf{s}_{q_{p}}(\mathbf{x})=\mathbf{A}\mathbf{x}+\mathbf{b}=-\Sigma_{p}^{-1}(\mathbf{x}-\mu_{p}),
\tag{92}
$$

这恰是矩匹配高斯 $q_{p}=\mathcal{N}(\mu_{p},\Sigma_{p})$ 的分数。

因此，$\mathbf{s}_{q_{p}}$ 是 $\mathbf{s}_{p}$ 在 $L^{2}(p)$ 仿射函数空间上的正交投影，残差 $\bm{\eta}_{p}:=\mathbf{s}_{p}-\mathbf{s}_{q_{p}}$ 与所有仿射函数正交。由此得到勾股（Pythagorean）能量分解：

$$
\mathbb{E}_{p}[\|\mathbf{s}_{p}\|^{2}]=\mathbb{E}_{p}[\|\mathbf{s}_{q_{p}}\|^{2}]+\mathbb{E}_{p}[\|\bm{\eta}_{p}\|^{2}].
\tag{93}
$$

##### 对场分解的含义

该投影性质在每个分布内部成立：$\bm{\eta}_{\theta}$ 是 $L^{2}(p_{\theta})$ 正交残差，$\bm{\eta}_{r}$ 是 $L^{2}(p_{r})$ 正交残差。勾股分解 (93) 在各自测度下对每个分数函数分别成立。

然而，差场 $\mathbf{g}_{\mathrm{KL}}=(\mathbf{s}_{\theta}-\mathbf{s}_{r})$ 并不自动继承这一正交结构。虽然每个残差在自身测度下均值为零，但 $\mathbf{g}_{\mathrm{KL}}^{\mathrm{G}}=(\mathbf{s}_{q_{\theta}}-\mathbf{s}_{q_{r}})$ 与 $\mathbf{g}_{\mathrm{KL}}^{\mathrm{nG}}=(\bm{\eta}_{\theta}-\bm{\eta}_{r})$ 之间的交叉项在 $p_{\theta}$ 或 $p_{r}$ 下都未必为零。当这些交叉矩存在时，任何一侧都不保证为零：

$$
\mathbb{E}_{p_{\theta}}[\mathbf{g}_{\mathrm{KL}}^{\mathrm{G}}\cdot\mathbf{g}_{\mathrm{KL}}^{\mathrm{nG}}]\;\text{可能非零},\quad\mathbb{E}_{p_{r}}[\mathbf{g}_{\mathrm{KL}}^{\mathrm{G}}\cdot\mathbf{g}_{\mathrm{KL}}^{\mathrm{nG}}]\;\text{可能非零}.
\tag{94}
$$

该分解在代数上精确，但在合成场中并非能量正交。因此，两个损失约束的是互补的*统计结构*，而非构成梯度方差的一个精确正交分解。

### B.3 分数–速度恒等式

本节对线性高斯路径证明式 (1) 的一般分数–速度恒等式。该恒等式是随机插值（stochastic-interpolant）表述中出现的高斯路径分数–速度转换的一个特化（[Holderrieth and Erives, 2025](#bib.bib71) 给出了教学性总结），对应 $\alpha_{t}=1-t,\;\beta_{t}=t$ 的情形。

###### 命题 B.13（线性高斯路径的分数–速度恒等式）

设 $\mathbf{x}\sim p$ 具有有限二阶矩，$\bm{\epsilon}\sim p_{z}=\mathcal{N}(\mathbf{0},\mathbf{I}_{d})$ 与之独立，定义 $\mathbf{x}_{t}=(1-t)\mathbf{x}+t\bm{\epsilon}$，$t\in(0,1)$。令 $p_{t}$ 表示 $\mathbf{x}_{t}$ 的边际密度，$\mathbf{s}_{t}(\mathbf{x}_{t}):=\nabla_{\mathbf{x}_{t}}\log p_{t}(\mathbf{x}_{t})$。对固定 $t$，边际速度场在可测向量场上是 $L^{2}(p_{t})$ 唯一的极小化子（至多差一个 $p_{t}$ 零测集）：

$$
\mathbf{v}_{t}^{*}\in\arg\min_{\mathbf{v}:\mathbb{R}^{d}\to\mathbb{R}^{d}}\mathbb{E}\!\left[\|\mathbf{v}(\mathbf{x}_{t})-(\bm{\epsilon}-\mathbf{x})\|_{2}^{2}\right],\qquad\mathbf{v}_{t}^{*}(\mathbf{x}_{t})=\mathbb{E}[\bm{\epsilon}-\mathbf{x}\mid\mathbf{x}_{t}].
\tag{95}
$$

则有以下恒等式：

$$
\mathbf{s}_{t}(\mathbf{x}_{t})=-\frac{\mathbf{x}_{t}+(1-t)\mathbf{v}_{t}^{*}(\mathbf{x}_{t})}{t}.
\tag{96}
$$

###### 证明 B.14

第一步：改写为加性高斯观测模型。OT 插值为 $\mathbf{x}_{t}=(1-t)\mathbf{x}+t\bm{\epsilon}$。定义 $\mathbf{x}^{\prime}:=(1-t)\mathbf{x}$。则 $\mathbf{x}_{t}=\mathbf{x}^{\prime}+t\bm{\epsilon}$，且 $\mathbf{x}_{t}\mid\mathbf{x}^{\prime}\sim\mathcal{N}(\mathbf{x}^{\prime},t^{2}\mathbf{I}_{d})$。

第二步：应用高斯后验均值恒等式。对高斯扰动模型 $\mathbf{y}=\mathbf{x}^{\prime}+\sigma\bm{\epsilon}$，对高斯卷积直接求导可得 $\mathbb{E}[\mathbf{x}^{\prime}\mid\mathbf{y}]=\mathbf{y}+\sigma^{2}\nabla_{\mathbf{y}}\log p_{Y}(\mathbf{y})$，其中 $p_{Y}$ 为观测密度。在本情形中 $\mathbf{y}=\mathbf{x}_{t}$、$\sigma=t$，故：

$$
\mathbb{E}[\mathbf{x}^{\prime}\mid\mathbf{x}_{t}]=\mathbf{x}_{t}+t^{2}\mathbf{s}_{t}(\mathbf{x}_{t})\,.
\tag{97}
$$

第三步：恢复 $\mathbb{E}[\mathbf{x}\mid\mathbf{x}_{t}]$。由 $\mathbf{x}^{\prime}=(1-t)\mathbf{x}$，有 $\mathbb{E}[\mathbf{x}\mid\mathbf{x}_{t}]=\mathbb{E}[\mathbf{x}^{\prime}\mid\mathbf{x}_{t}]/(1-t)$：

$$
\mathbb{E}[\mathbf{x}\mid\mathbf{x}_{t}]=\frac{\mathbf{x}_{t}+t^{2}\mathbf{s}_{t}(\mathbf{x}_{t})}{1-t}\,.
\tag{98}
$$

第四步：恢复 $\mathbb{E}[\bm{\epsilon}\mid\mathbf{x}_{t}]$。由 $\mathbf{x}_{t}=t\bm{\epsilon}+(1-t)\mathbf{x}$，有 $\bm{\epsilon}=(\mathbf{x}_{t}-(1-t)\mathbf{x})/t$。取条件期望：

$$
\begin{aligned}
\mathbb{E}[\bm{\epsilon}\mid\mathbf{x}_{t}]
&=\frac{1}{t}\left[\mathbf{x}_{t}-(1-t)\mathbb{E}[\mathbf{x}\mid\mathbf{x}_{t}]\right]
=\frac{1}{t}\left[\mathbf{x}_{t}-(1-t)\cdot\frac{\mathbf{x}_{t}+t^{2}\mathbf{s}_{t}(\mathbf{x}_{t})}{1-t}\right]\\
&=\frac{1}{t}\left[\mathbf{x}_{t}-\mathbf{x}_{t}-t^{2}\mathbf{s}_{t}(\mathbf{x}_{t})\right]
=-t\,\mathbf{s}_{t}(\mathbf{x}_{t})\,.
\end{aligned}
\tag{99}
$$

第五步：构造边际速度场。该场是目标 $\bm{\epsilon}-\mathbf{x}$ 的条件期望：

$$
\begin{aligned}
\mathbf{v}_{t}^{*}(\mathbf{x}_{t})
&=\mathbb{E}[\bm{\epsilon}-\mathbf{x}\mid\mathbf{x}_{t}]=\mathbb{E}[\bm{\epsilon}\mid\mathbf{x}_{t}]-\mathbb{E}[\mathbf{x}\mid\mathbf{x}_{t}]\\
&=-t\,\mathbf{s}_{t}(\mathbf{x}_{t})-\frac{\mathbf{x}_{t}+t^{2}\mathbf{s}_{t}(\mathbf{x}_{t})}{1-t}\,.
\end{aligned}
\tag{100}
$$

第六步：整理得恒等式。两边乘以 $(1-t)$：

$$
\begin{aligned}
(1-t)\mathbf{v}_{t}^{*}(\mathbf{x}_{t})
&=-t(1-t)\mathbf{s}_{t}(\mathbf{x}_{t})-\mathbf{x}_{t}-t^{2}\mathbf{s}_{t}(\mathbf{x}_{t})
=-t\mathbf{s}_{t}(\mathbf{x}_{t})\underbrace{[(1-t)+t]}_{=1}-\mathbf{x}_{t}\\
&=-t\mathbf{s}_{t}(\mathbf{x}_{t})-\mathbf{x}_{t}\,.
\end{aligned}
\tag{101}
$$

整理并除以 $-t$ 得

$$
\mathbf{s}_{t}(\mathbf{x}_{t})=-\frac{\mathbf{x}_{t}+(1-t)\mathbf{v}_{t}^{*}(\mathbf{x}_{t})}{t}\,.
\tag{102}
$$

###### 注 B.15（边界 $t=1$）

在 $t=1$ 处，无论干净分布 $p$ 如何，都有 $\mathbf{x}_{1}=\bm{\epsilon}\sim\mathcal{N}(\mathbf{0},\mathbf{I}_{d})$，故 $p_{1}=p_{z}$ 且 $\mathbf{s}_{1}(\mathbf{x}_{1})=-\mathbf{x}_{1}$。右边给出 $-(\mathbf{x}_{1}+0\cdot\mathbf{v}_{1}^{*}(\mathbf{x}_{1}))/1=-\mathbf{x}_{1}$，验证了 $t=1$ 处的恒等式。

###### 推论 B.16（边际速度差恢复分数差）

对 $i\in\{1,2\}$，设 $\mathbf{x}^{(i)}\sim p_{i}$ 具有有限二阶矩，$\bm{\epsilon}^{(i)}\sim p_{z}$ 与之独立，定义 $\mathbf{x}_{t}^{(i)}=(1-t)\mathbf{x}^{(i)}+t\bm{\epsilon}^{(i)}$，$t\in(0,1)$。令 $p_{i,t}$ 为 $\mathbf{x}_{t}^{(i)}$ 的边际密度，$\mathbf{s}_{i,t}(\mathbf{x}_{t}):=\nabla_{\mathbf{x}_{t}}\log p_{i,t}(\mathbf{x}_{t})$ 为其边际分数，并定义对应的边际速度场 $\mathbf{v}_{i,t}^{*}(\mathbf{x}_{t}):=\mathbb{E}[\bm{\epsilon}^{(i)}-\mathbf{x}^{(i)}\mid\mathbf{x}_{t}^{(i)}=\mathbf{x}_{t}]$。则对二者都有定义的每个 $\mathbf{x}_{t}$，

$$
\mathbf{v}_{1,t}^{*}(\mathbf{x}_{t})-\mathbf{v}_{2,t}^{*}(\mathbf{x}_{t})=-\frac{t}{1-t}\left(\mathbf{s}_{1,t}(\mathbf{x}_{t})-\mathbf{s}_{2,t}(\mathbf{x}_{t})\right).
\tag{103}
$$

###### 证明 B.17

对每个场分别应用分数–速度恒等式：

$$
\mathbf{s}_{1,t}(\mathbf{x}_{t})=-\frac{\mathbf{x}_{t}+(1-t)\mathbf{v}^{*}_{1,t}(\mathbf{x}_{t})}{t}\,,\qquad
\mathbf{s}_{2,t}(\mathbf{x}_{t})=-\frac{\mathbf{x}_{t}+(1-t)\mathbf{v}^{*}_{2,t}(\mathbf{x}_{t})}{t}\,.
\tag{104--105}
$$

用第一式减第二式：

$$
\begin{aligned}
\mathbf{s}_{1,t}(\mathbf{x}_{t})-\mathbf{s}_{2,t}(\mathbf{x}_{t})
&=-\frac{1}{t}\left[(\mathbf{x}_{t}+(1-t)\mathbf{v}^{*}_{1,t})-(\mathbf{x}_{t}+(1-t)\mathbf{v}^{*}_{2,t})\right]\\
&=-\frac{1-t}{t}\left[\mathbf{v}^{*}_{1,t}(\mathbf{x}_{t})-\mathbf{v}^{*}_{2,t}(\mathbf{x}_{t})\right]\,.
\end{aligned}
\tag{106}
$$

整理出速度差：

$$
\mathbf{v}^{*}_{1,t}(\mathbf{x}_{t})-\mathbf{v}^{*}_{2,t}(\mathbf{x}_{t})=-\frac{t}{1-t}\left(\mathbf{s}_{1,t}(\mathbf{x}_{t})-\mathbf{s}_{2,t}(\mathbf{x}_{t})\right)\,.
\tag{107}
$$

### B.4 DMD 损失：分数差恒等式与回归

沿用上文约定，$\mathbf{g}_{\mathrm{KL},t}(\mathbf{x}_{t}):=\mathbf{s}_{\theta,t}(\mathbf{x}_{t})-\mathbf{s}_{r,t}(\mathbf{x}_{t})$ 表示噪声水平 $t$ 下加噪边际 $p_{\theta,t}$ 与 $p_{r,t}$ 的反向 KL 场，即端点场 $\mathbf{g}_{\mathrm{KL}}=\mathbf{s}_{\theta}-\mathbf{s}_{r}$ 在时刻 $t$ 的类比。

###### 命题 B.18（加噪边际分数差）

令 $\mathbf{v}^{*}_{\theta,t}$ 与 $\mathbf{v}^{*}_{r,t}$ 为 $p_{\theta,t}$ 与 $p_{r,t}$ 的边际速度场，并在同一 $\mathbf{x}_{t}$ 处求值。则精确速度差

$$
\mathbf{d}_{t}^{*}(\mathbf{x}_{t}):=\mathbf{v}^{*}_{\theta,t}(\mathbf{x}_{t})-\mathbf{v}^{*}_{r,t}(\mathbf{x}_{t})
\tag{108}
$$

与加噪边际反向 KL 场成比例：

$$
\mathbf{d}_{t}^{*}(\mathbf{x}_{t})=\frac{t}{1-t}\left(\mathbf{s}_{r,t}(\mathbf{x}_{t})-\mathbf{s}_{\theta,t}(\mathbf{x}_{t})\right)=-\frac{t}{1-t}\,\mathbf{g}_{\mathrm{KL},t}(\mathbf{x}_{t}),
\tag{109}
$$

其中 $\mathbf{g}_{\mathrm{KL},t}:=\mathbf{s}_{\theta,t}-\mathbf{s}_{r,t}$。等价地，加噪边际分布梯度可恢复为

$$
\mathbf{g}_{\mathrm{KL},t}(\mathbf{x}_{t})=-\frac{1-t}{t}\mathbf{d}_{t}^{*}(\mathbf{x}_{t}).
\tag{110}
$$

###### 证明 B.19

由[推论 B.16](#A2.Thmtheorem16)取 $1=\theta$、$2=r$，

$$
\mathbf{d}_{t}^{*}
=\mathbf{v}^{*}_{\theta,t}-\mathbf{v}^{*}_{r,t}=-\frac{t}{1-t}(\mathbf{s}_{\theta,t}(\mathbf{x}_{t})-\mathbf{s}_{r,t}(\mathbf{x}_{t}))=\frac{t}{1-t}(\mathbf{s}_{r,t}(\mathbf{x}_{t})-\mathbf{s}_{\theta,t}(\mathbf{x}_{t}))\,.
\tag{111}
$$

由 $\mathbf{g}_{\mathrm{KL},t}=\mathbf{s}_{\theta,t}-\mathbf{s}_{r,t}$，有 $\mathbf{d}_{t}^{*}=-\frac{t}{1-t}\,\mathbf{g}_{\mathrm{KL},t}(\mathbf{x}_{t})$。整理即得式 (110)。

[命题 B.18](#A2.Thmtheorem18)仅当两个场在同一 $(\mathbf{x}_{t},t)$ 处都恢复各自的精确边际时，才对边际速度场与时刻 $t$ 的加噪边际精确成立。实际的神经分支与混合目标并不保证恢复这些精确的边际速度。TwinFlow 与 APEX 用内部相互分离的分支把这一转换变成实用的一步分布估计器（[Cheng et al., 2025](#bib.bib56)；[Liu et al., 2026a](#bib.bib61)）；我们采用 APEX 式的条件分离 $\mathbf{c}_{\mathrm{fake}}=-\mathbf{c}$，并使用[第 4.1 节](#S4.SS1)定义的损失。实践中，$\widehat{\mathbf{d}}_{t}(\mathbf{x}_{t}\mid\mathbf{c}):=\widehat{\mathbf{v}}_{\theta,t}(\mathbf{x}_{t}\mid\mathbf{c})-\widehat{\mathbf{v}}_{r,t}(\mathbf{x}_{t}\mid\mathbf{c})$ 近似 $\mathbf{d}_{t}^{*}(\mathbf{x}_{t})$。校正在 $\widehat{\mathbf{x}}_{0,t^{\prime}}^{\operatorname{sg}}$ 处查询该差值，并在加权与归一化后 detach 其结果。若两种处理都不做，则 $\widehat{\mathbf{d}}_{t^{\prime}}^{\mathrm{DMD}}=\operatorname{sg}\!\left(\widehat{\mathbf{d}}_{t^{\prime}}(\widehat{\mathbf{x}}_{0,t^{\prime}}^{\operatorname{sg}}\mid\mathbf{c})\right)$。在式 (11) 中，从速度目标减去 $\widehat{\mathbf{d}}_{t^{\prime}}^{\mathrm{DMD}}$，等价于向端点目标加上 $t\widehat{\mathbf{d}}_{t^{\prime}}^{\mathrm{DMD}}$。

##### detach DMD 回归的梯度

对固定 $\mathbf{x}_{t}$ 与 $t>0$，式 (11) 的两个目标在求导时均保持常数。其速度到端点的转换给出

$$
\widehat{\mathbf{x}}_{0}-\mathbf{x}_{0}^{\mathrm{DMD}}=-t\bigl(\bm{F}_{\theta}(\mathbf{x}_{t},t,\mathbf{c})-\mathbf{v}_{t}^{\mathrm{DMD}}\bigr),\qquad\ell_{x}(t)=t^{2}\ell_{v}(t).
$$

因此 $\nabla_{\theta}\ell_{x}(t)=t^{2}\nabla_{\theta}\ell_{v}(t)$，且式 (12) 的等权 DMD 损失满足

$$
\begin{aligned}
\mathcal{L}_{\text{score}}
&=\mathbb{E}\!\left[(1+t^{2})\ell_{v}(t)\right],\\
\nabla_{\theta}\mathcal{L}_{\text{score}}
&=2\mathbb{E}\!\left[(1+t^{2})[J_{\theta}\bm{F}_{\theta}(\mathbf{x}_{t},t,\mathbf{c})]^{\top}\widehat{\mathbf{d}}_{t^{\prime}}^{\mathrm{DMD}}\right].
\end{aligned}
$$

若校正确为精确、未加权的速度差 $\mathbf{d}_{t^{\prime}}^{*}(\widehat{\mathbf{x}}_{0,t^{\prime}}^{\operatorname{sg}})$，则由式 (109)与 $J_{\theta}\widehat{\mathbf{x}}_{0}=-tJ_{\theta}\bm{F}_{\theta}$ 得逐样本恒等式

$$
\nabla_{\theta}(\ell_{v}(t)+\ell_{x}(t))=\frac{2t^{\prime}(1+t^{2})}{t(1-t^{\prime})}[J_{\theta}\widehat{\mathbf{x}}_{0}]^{\top}\mathbf{g}_{\mathrm{KL},t^{\prime}}(\widehat{\mathbf{x}}_{0,t^{\prime}}^{\operatorname{sg}}).
$$

这是由 $p_{\theta,t^{\prime}}$ 与 $p_{r,t^{\prime}}$ 定义的场的逐点拉回。on-policy 的 KL 解释还要求被查询的预测分布与训练模型速度分支所用的模型分布一致。对[第 3.1 节](#S3.SS1)的单步分布，这一一致性在 $t=1$、$\mathbf{x}_{t}=\mathbf{z}$ 处直接成立，但对中间的回归输入并不蕴含。对上述平方损失，两个逐样本梯度共线，其组合只改变时间加权与幅度；在 $t=1$ 处 $\ell_{x}=\ell_{v}$。各自独立的、依赖残差的归一化会改变比例因子，在把该计算应用于归一化损失时必须计入。在分支近似与校正处理存在的情况下，式 (12) 一般与未加权、按时间平均的加噪反向 KL 具有不同的梯度。

### B.5 内部模型速度训练

独立抽取 $\mathbf{z},\bm{\epsilon}\sim p_{z}$，令 $\mathbf{x}_{\theta}^{\operatorname{sg}}:=\operatorname{sg}(G_{\theta}(\mathbf{z},\mathbf{c}))$、$\mathbf{x}_{\theta,t}^{\operatorname{sg}}:=(1-t)\mathbf{x}_{\theta}^{\operatorname{sg}}+t\bm{\epsilon}$，并最小化

$$
\mathcal{L}_{\text{fake}}(\theta)={\mathbb{E}}_{\mathbf{z},\bm{\epsilon},t,\mathbf{c}}\left[\|\widehat{\mathbf{v}}_{\theta,t}(\mathbf{x}_{\theta,t}^{\operatorname{sg}}\mid\mathbf{c})-(\bm{\epsilon}-\mathbf{x}_{\theta}^{\operatorname{sg}})\|_{2}^{2}\right]\,,
\tag{112}
$$

这里 $\mathbf{c}\sim p_{c}$，$\mathbf{z},\bm{\epsilon}\sim p_{z}$ 相互独立，$t$ 从支撑在 $(0,1)$ 上的分布独立采样。该辅助回归使用[第 3.1 节](#S3.SS1)定义的单步输出分布 $p_{\theta}$。梯度穿过模型速度分支，而生成样本与回归目标均 detach。两个分支共享 $\theta$，因此该辅助回归也会更新共享参数。

### B.6 特征矩损失的梯度

##### 固定特征的更新

在一次更新内，EMA 特征映射参数与排队特征固定，而穿过当前模型样本的导数保留。因此，特征矩损失无法通过在该次更新内直接改变特征映射参数来降低。这消除了单次更新中一条直接的特征坍缩捷径，但并不能排除 EMA 映射随训练演化而出现的缓慢退化。

###### 命题 B.20（特征矩损失的梯度）

令 $\mathbf{h}_{n}$（$n=1,\ldots,N_{\phi}$）为模型特征：当前条目 $\mathbf{h}_{n}=\phi(\mathbf{x}_{n},\mathbf{c}_{n})$ 保留梯度，队列中存储的条目均 detach。定义经验均值与有偏经验方差

$$
\widehat{\mu}_{\theta}^{\phi}:=N_{\phi}^{-1}\sum_{n}\mathbf{h}_{n}\,,\qquad\widehat{\nu}_{\theta,j}^{\phi}:=N_{\phi}^{-1}\sum_{n}(h_{n,j}-\widehat{\mu}_{\theta,j}^{\phi})^{2}\,,
$$

对排队参考特征，令 $\{\mathbf{h}_{k}^{r}\}_{k=1}^{K}$ 为 $\mathcal{Q}_{r}$ 中存储的 $K$ 条预计算特征向量（入队时按 $\phi(\mathbf{x}_{k},\mathbf{c}_{k})$ 计算并 detach），并定义

$$
\widehat{\mu}_{r}^{\phi}:=K^{-1}\!\sum_{k=1}^{K}\!\mathbf{h}_{k}^{r}\,,\qquad\widehat{\nu}_{r,j}^{\phi}:=K^{-1}\!\sum_{k=1}^{K}\!(h^{r}_{k,j}-\widehat{\mu}_{r,j}^{\phi})^{2}\,;
$$

假设 $\widehat{\nu}_{\theta,j}^{\phi}>0$。它们是[第 4.2 节](#S4.SS2)定义的总体量 $\mu_{i}^{\phi},\nu_{i,j}^{\phi}$ 的估计量。把这些经验矩代入式 (13) 的结果记为 $\widehat{\mathcal{L}}_{\text{pop}}$。其对某条当前特征 $\mathbf{h}_{k}$ 的梯度为

$$
\frac{\partial\widehat{\mathcal{L}}_{\text{pop}}}{\partial h_{k,j}}=\frac{2}{N_{\phi}}\!\left[(\widehat{\mu}_{\theta,j}^{\phi}-\widehat{\mu}_{r,j}^{\phi})+\frac{h_{k,j}-\widehat{\mu}_{\theta,j}^{\phi}}{\sqrt{\widehat{\nu}_{\theta,j}^{\phi}}}\left(\sqrt{\widehat{\nu}_{\theta,j}^{\phi}}-\sqrt{\widehat{\nu}_{r,j}^{\phi}}\right)\right]\!.
\tag{113}
$$

这是固定队列下经验目标的精确梯度；一般而言，它并非总体损失 $\mathcal{L}_{\text{pop}}$ 梯度的无偏估计。

###### 证明 B.21

经验损失分解为 $\widehat{\mathcal{L}}_{\text{pop}}=\mathcal{L}_{\mu}+\mathcal{L}_{\sigma}$，其中

$$
\mathcal{L}_{\mu}=\sum_{j}(\widehat{\mu}_{\theta,j}^{\phi}-\widehat{\mu}_{r,j}^{\phi})^{2}\,,\qquad
\mathcal{L}_{\sigma}=\sum_{j}(\sqrt{\widehat{\nu}_{\theta,j}^{\phi}}-\sqrt{\widehat{\nu}_{r,j}^{\phi}})^{2}\,.
\tag{114--115}
$$

(a) 均值项。由 $\partial\widehat{\mu}_{\theta,j}^{\phi}/\partial h_{k,j}=1/N_{\phi}$，

$$
\frac{\partial\mathcal{L}_{\mu}}{\partial h_{k,j}}=\frac{2}{N_{\phi}}(\widehat{\mu}_{\theta,j}^{\phi}-\widehat{\mu}_{r,j}^{\phi})\,.
\tag{116}
$$

(b) 方差项。由 $\widehat{\nu}_{\theta,j}^{\phi}=N_{\phi}^{-1}\sum_{n}(h_{n,j}-\widehat{\mu}_{\theta,j}^{\phi})^{2}$，

$$
\frac{\partial(h_{n,j}-\widehat{\mu}_{\theta,j}^{\phi})}{\partial h_{k,j}}=\delta_{nk}-\frac{1}{N_{\phi}}\,.
\tag{117}
$$

由链式法则与中心和恒等式，对 $n$ 求和得

$$
\frac{\partial\widehat{\nu}_{\theta,j}^{\phi}}{\partial h_{k,j}}=\frac{2}{N_{\phi}}(h_{k,j}-\widehat{\mu}_{\theta,j}^{\phi})\,.
\tag{118}
$$

对标准差应用链式法则得

$$
\frac{\partial\mathcal{L}_{\sigma}}{\partial h_{k,j}}=\frac{2}{N_{\phi}}\frac{h_{k,j}-\widehat{\mu}_{\theta,j}^{\phi}}{\sqrt{\widehat{\nu}_{\theta,j}^{\phi}}}(\sqrt{\widehat{\nu}_{\theta,j}^{\phi}}-\sqrt{\widehat{\nu}_{r,j}^{\phi}})\,.
\tag{119}
$$

合并。将 (a) 与 (b) 相加：

$$
\frac{\partial\widehat{\mathcal{L}}_{\text{pop}}}{\partial h_{k,j}}=\frac{2}{N_{\phi}}\left[(\widehat{\mu}_{\theta,j}^{\phi}-\widehat{\mu}_{r,j}^{\phi})+\frac{h_{k,j}-\widehat{\mu}_{\theta,j}^{\phi}}{\sqrt{\widehat{\nu}_{\theta,j}^{\phi}}}\left(\sqrt{\widehat{\nu}_{\theta,j}^{\phi}}-\sqrt{\widehat{\nu}_{r,j}^{\phi}}\right)\right]\!.
\tag{120}
$$

对带稳定项 $\sqrt{\widehat{\nu}_{i,j}^{\phi}+\delta}$（$\delta>0$ 为标量稳定子）的版本，同一推导把梯度中的每个标准差（包括分母）都换成其稳定值。上面给出的梯度是在所述正方差假设下针对未稳定目标的。

### B.7 回归下的协方差收缩

这一结果表明把平方误差回归解释为分布匹配的一个局限：条件均值预测器未必保持目标协方差。这是关于回归的一个独立观察，并非反向 KL 场分解的推论，也不是在断言 DMD 缺乏方差信息。

###### 命题 B.22（回归下的协方差收缩）

设 $(\mathbf{X},\mathbf{Y})$ 为任意平方可积的联合分布随机向量，$\mathbf{m}(\mathbf{Y}):=\mathbb{E}[\mathbf{X}\mid\mathbf{Y}]$ 为最优平方误差预测器。则

$$
\operatorname{Cov}(\mathbf{m}(\mathbf{Y}))\preceq\operatorname{Cov}(\mathbf{X}).
\tag{121}
$$

而且，只要 $\mathbb{E}[\operatorname{Tr}\operatorname{Cov}(\mathbf{X}\mid\mathbf{Y})]>0$，就有 $\operatorname{Tr}\operatorname{Cov}(\mathbf{m}(\mathbf{Y}))<\operatorname{Tr}\operatorname{Cov}(\mathbf{X})$。

###### 证明 B.23

由全协方差定律，

$$
\operatorname{Cov}(\mathbf{X})=\mathbb{E}[\operatorname{Cov}(\mathbf{X}\mid\mathbf{Y})]+\operatorname{Cov}(\mathbb{E}[\mathbf{X}\mid\mathbf{Y}])=\mathbb{E}[\operatorname{Cov}(\mathbf{X}\mid\mathbf{Y})]+\operatorname{Cov}(\mathbf{m}(\mathbf{Y})).
\tag{122}
$$

条件协方差项半正定，即得矩阵不等式；取迹即得严格版本。

该命题仅当训练好的预测器在所选平方误差耦合下实现条件均值时适用。严格的协方差收缩只在仍存在未解决的条件方差时发生。因此，它提示了含糊端点回归中可能出现的方差压制，但并不意味着确定性或单步生成器普遍低估方差。注意，精确分数差*确实*包含方差信息：取 $p_{\theta}=\mathcal{N}(0,\sigma_{\theta}^{2})$、$p_{r}=\mathcal{N}(0,\sigma_{r}^{2})$，

$$
\mathbf{s}_{\theta}(x)-\mathbf{s}_{r}(x)=-\frac{x}{\sigma_{\theta}^{2}}+\frac{x}{\sigma_{r}^{2}}\,,
\tag{123}
$$

故下降方向 $\mathbf{s}_{r}(x)-\mathbf{s}_{\theta}(x)=x(1/\sigma_{\theta}^{2}-1/\sigma_{r}^{2})$ 在 $\sigma_{\theta}<\sigma_{r}$ 时把样本向外推。然而，学习得到的逐点估计器可能带有噪声，因为它依赖所学速度分支的精度以及随机的时间/噪声样本。池化特征矩损失提供了显式的总体统计量校正。在一个近似独立、平稳特征且矩有限的理论化下，模型侧与参考侧均值估计的方差分别按 $O(1/N_{\phi})$ 与 $O(1/K)$ 量级缩放；这并不能证明其经验参数梯度方差低于 DMD 损失，而且队列陈旧性可能引入偏差。
