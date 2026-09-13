---
title: "用于视频生成的扩散模型"
title_en: "Diffusion Models for Video Generation"
source: https://lilianweng.github.io/posts/2024-04-12-diffusion-video/
crawled: 2026-09-08
translated: 2026-09-08
---

> 原文：[Diffusion Models for Video Generation](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/) · Lilian Weng（翁荔）

[扩散模型](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/)在过去几年已在图像合成上展示了强劲结果。如今研究社区开始攻一个更难的任务——用它做视频生成。该任务本身是图像情形的超集（图像即 1 帧的视频），但更具挑战，因为：

1. 它对帧间的时间一致性有额外要求，这天然需要把更多世界知识编码进模型。
2. 与文本或图像相比，收集大量高质量、高维的视频数据更难，更别说文本-视频对。

> **🥑 必读前置：继续阅读前，请确保已读过上一篇关于图像生成的博文["什么是扩散模型？"](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/)。**

# 从零构建视频生成模型

首先回顾从零设计与训练扩散视频模型的方法，即不依赖预训练图像生成器。

## 参数化与采样基础

这里我们用与[前文](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/)略不同的变量定义，但数学不变。设 $\mathbf{x} \sim q_\text{real}$ 为从真实数据分布采样的数据点。现在我们随时间加入少量高斯噪声，创建 $\mathbf{x}$ 的一系列带噪变体，记为 $\{\mathbf{z}_t \mid t =1 \dots, T\}$，$t$ 越大噪声越多，最后 $q(\mathbf{z}_T) \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$。加噪的前向过程是高斯过程。设 $\alpha_t, \sigma_t$ 定义该高斯过程的可微噪声调度：

$$
q(\mathbf{z}_t \vert \mathbf{x}) = \mathcal{N}(\mathbf{z}_t; \alpha_t \mathbf{x}, \sigma^2_t\mathbf{I})
$$

为表示 $0 \leq s < t \leq T$ 时的 $q(\mathbf{z}_t \vert \mathbf{z}_s)$，我们有：

$$
\begin{aligned}
\mathbf{z}_t &= \alpha_t \mathbf{x} + \sigma_t\boldsymbol{\epsilon}_t \\
\mathbf{z}_s &= \alpha_s \mathbf{x} + \sigma_s\boldsymbol{\epsilon}_s \\
\mathbf{z}_t &= \alpha_t \Big(\frac{\mathbf{z}_s - \sigma_s\boldsymbol{\epsilon}_s}{\alpha_s}\Big) + \sigma_t\boldsymbol{\epsilon}_t \\
\mathbf{z}_t &= \frac{\alpha_t}{\alpha_s}\mathbf{z}_s + \sigma_t\boldsymbol{\epsilon}_t - \frac{\alpha_t\sigma_s}{\alpha_s} \boldsymbol{\epsilon}_s \\
\text{Thus }q(\mathbf{z}_t \vert \mathbf{z}_s) &= \mathcal{N}\Big(\mathbf{z}_t; \frac{\alpha_t}{\alpha_s}\mathbf{z}_s, \big(1 - \frac{\alpha^2_t\sigma^2_s}{\sigma^2_t\alpha^2_s}\big)\sigma^2_t \mathbf{I}\Big)
\end{aligned}
$$

设对数信噪比为 $\lambda_t = \log[\alpha^2_t / \sigma^2_t]$，我们可以把 DDIM（[Song et al. 2020](https://arxiv.org/abs/2010.02502)）更新表示为：

$$
q(\mathbf{z}_t \vert \mathbf{z}_s) = \mathcal{N}\Big(\mathbf{z}_t; \frac{\alpha_t}{\alpha_s}\mathbf{z}_s, \sigma^2_{t\vert s} \mathbf{I}\Big) \quad
\text{where }\sigma^2_{t\vert s} = (1 - e^{\lambda_t - \lambda_s})\sigma^2_t
$$

有一种特殊的 $\mathbf{v}$-预测（$\mathbf{v} = \alpha_t \boldsymbol{\epsilon} - \sigma_t \mathbf{x}$）参数化，由 [Salimans & Ho (2022)](https://arxiv.org/abs/2202.00512) 提出。它被证明相比 $\boldsymbol{\epsilon}$-参数化有助于避免视频生成中的色偏。

$\mathbf{v}$-参数化用角坐标的技巧推导。首先定义 $\phi_t = \arctan(\sigma_t / \alpha_t)$，于是 $\alpha_\phi = \cos\phi, \sigma_t = \sin\phi, \mathbf{z}_\phi = \cos\phi \mathbf{x} + \sin\phi\boldsymbol{\epsilon}$。$\mathbf{z}_\phi$ 的速度可写作：

$$
\mathbf{v}_\phi = \nabla_\phi \mathbf{z}_\phi = \frac{d\cos\phi}{d\phi} \mathbf{x} + \frac{d\sin\phi}{d\phi}\boldsymbol{\epsilon} = \cos\phi\boldsymbol{\epsilon} -\sin\phi\mathbf{x}
$$

然后可以推出，

$$
\begin{aligned}
\sin\phi\mathbf{x} 
&= \cos\phi\boldsymbol{\epsilon}  - \mathbf{v}_\phi \\
&= \frac{\cos\phi}{\sin\phi}\big(\mathbf{z}_\phi - \cos\phi\mathbf{x}\big) - \mathbf{v}_\phi \\
\sin^2\phi\mathbf{x} 
&= \cos\phi\mathbf{z}_\phi - \cos^2\phi\mathbf{x} - \sin\phi \mathbf{v}_\phi \\
\mathbf{x} &= \cos\phi\mathbf{z}_\phi - \sin\phi\mathbf{v}_\phi \\
\text{Similarly }
\boldsymbol{\epsilon} &= \sin\phi\mathbf{z}_\phi + \cos\phi \mathbf{v}_\phi
\end{aligned}
$$

DDIM 更新规则相应更新：

$$
\begin{aligned}
\mathbf{z}_{\phi_s} 
&= \cos\phi_s\hat{\mathbf{x}}_\theta(\mathbf{z}_{\phi_t}) + \sin\phi_s\hat{\epsilon}_\theta(\mathbf{z}_{\phi_t}) \quad\quad{\small \text{; }\hat{\mathbf{x}}_\theta(.), \hat{\epsilon}_\theta(.)\text{ are two models to predict }\mathbf{x}, \boldsymbol{\epsilon}\text{ based on }\mathbf{z}_{\phi_t}}\\
&= \cos\phi_s \big( \cos\phi_t \mathbf{z}_{\phi_t} - \sin\phi_t \hat{\mathbf{v}}_\theta(\mathbf{z}_{\phi_t} ) \big) +
\sin\phi_s \big( \sin\phi_t \mathbf{z}_{\phi_t} + \cos\phi_t \hat{\mathbf{v}}_\theta(\mathbf{z}_{\phi_t} ) \big) \\
&= {\color{red} \big( \cos\phi_s\cos\phi_t + \sin\phi_s\sin\phi_t \big)} \mathbf{z}_{\phi_t} + 
{\color{green} \big( \sin\phi_s \cos\phi_t - \cos\phi_s \sin\phi_t \big)} \hat{\mathbf{v}}_\theta(\mathbf{z}_{\phi_t} ) \\
&= {\color{red} cos(\phi_s - \phi_t)} \mathbf{z}_{\phi_t} +
{\color{green} \sin(\phi_s - \phi_t)} \hat{\mathbf{v}}_\theta(\mathbf{z}_{\phi_t}) \quad\quad{\small \text{; trigonometric identity functions.}}
\end{aligned}
$$

![](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/v-param.png)

*可视化扩散更新步在角坐标中如何工作：DDIM 沿 $-\hat{\mathbf{v}}_{\phi_t}$ 方向移动 $\mathbf{z}_{\phi_s}$ 使其演化。（图片来源：Salimans & Ho, 2022 ）*

模型的 $\mathbf{v}$-参数化即预测 $\mathbf{v}_\phi = \cos\phi\boldsymbol{\epsilon} -\sin\phi\mathbf{x} = \alpha_t\boldsymbol{\epsilon} - \sigma_t\mathbf{x}$。

视频生成的情形下，我们需要扩散模型运行多步上采样来延长视频或提高帧率。这要求能以第一个视频 $\mathbf{x}^a$ 为条件采样第二个视频 $\mathbf{x}^b$，$\mathbf{x}^b \sim p_\theta(\mathbf{x}^b \vert \mathbf{x}^a)$，其中 $\mathbf{x}^b$ 可以是 $\mathbf{x}^a$ 的自回归延伸，也可以是低帧率视频 $\mathbf{x}^a$ 的帧间缺失帧。

$\mathbf{x}_b$ 的采样除自身对应的噪声变量外还需以 $\mathbf{x}_a$ 为条件。**视频扩散模型（Video Diffusion Models，VDM**；[Ho & Salimans, et al. 2022](https://arxiv.org/abs/2204.03458)）提出*重建引导（reconstruction guidance）*方法，使用调整后的去噪模型使 $\mathbf{x}^b$ 的采样能恰当以 $\mathbf{x}^a$ 为条件：

$$
\begin{aligned}
\mathbb{E}_q [\mathbf{x}_b \vert \mathbf{z}_t, \mathbf{x}^a] &= \mathbb{E}_q [\mathbf{x}^b \vert \mathbf{z}_t] + \frac{\sigma_t^2}{\alpha_t} \nabla_{\mathbf{z}^b_t} \log q(\mathbf{x}^a \vert \mathbf{z}_t) \\
q(\mathbf{x}^a \vert \mathbf{z}_t) &\approx \mathcal{N}\big[\hat{\mathbf{x}}^a_\theta (\mathbf{z}_t), \frac{\sigma_t^2}{\alpha_t^2}\mathbf{I}\big] & {\small \text{; the closed form is unknown.}}\\
\tilde{\mathbf{x}}^b_\theta (\mathbf{z}_t) &= \hat{\mathbf{x}}^b_\theta (\mathbf{z}_t) - \frac{w_r \alpha_t}{2} \nabla_{\mathbf{z}_t^b} \| \mathbf{x}^a - \hat{\mathbf{x}}^a_\theta (\mathbf{z}_t) \|^2_2 & {\small \text{; an adjusted denoising model for }\mathbf{x}^b}
\end{aligned}
$$

其中 $\hat{\mathbf{x}}^a_\theta (\mathbf{z}_t), \hat{\mathbf{x}}^b_\theta (\mathbf{z}_t)$ 是去噪模型提供的 $\mathbf{x}^a, \mathbf{x}^b$ 的重建。$w_r$ 是权重因子，发现较大的 $w_r >1$ 能改进样本质量。注意同一重建引导方法也可以同时以低分辨率视频为条件，把样本扩展到高分辨率。

## 模型架构：3D U-Net 与 DiT

与文生图扩散模型类似，U-net 与 Transformer 仍是两种[常见架构选择](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/#model-architecture)。Google 有一系列基于 U-net 架构的扩散视频建模论文，而 OpenAI 近期的 Sora 模型利用了 Transformer 架构。

**VDM**（[Ho & Salimans, et al. 2022](https://arxiv.org/abs/2204.03458)）采用标准扩散模型设定，但配以适合视频建模的改良架构。它把 [2D U-net](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/#model-architecture) 扩展到 3D 数据（[Cicek et al. 2016](https://arxiv.org/abs/1606.06650)），每个特征图表示帧 × 高 × 宽 × 通道的 4D 张量。该 3D U-net 在空间与时间上因子化，即每层只在空间或时间维度上操作，不同时兼顾：

- 处理*空间*：
  - 2D U-net 中的每个旧 2D 卷积层被扩展为仅空间的 3D 卷积；确切地说，3x3 卷积变成 1x3x3 卷积。
  - 每个空间注意力块仍是对空间的注意力，第一轴（`frames`）被视为批维。
- 处理*时间*：
  - 每个空间注意力块之后加一个时间注意力块。它对第一轴（`frames`）做注意力，把空间轴视为批维。用[相对位置](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/#relative-position-encoding)嵌入跟踪帧的顺序。时间注意力块对模型捕捉良好的时间连贯性很重要。

![](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/3D-U-net.png)

*3D U-net 架构。带噪视频 $\mathbf{z}_t$、条件信息 $\boldsymbol{c}$ 与对数信噪比（log-SNR）$\lambda_t$ 是网络输入。通道乘子 $M_1, \dots, M_K$ 表示各层的通道数。（图片来源：Salimans & Ho, 2022 ）*

**Imagen Video**（[Ho, et al. 2022](https://arxiv.org/abs/2210.02303)）构建在级联扩散模型之上以增强视频生成质量，升级到输出 1280x768、24 fps 的视频。Imagen Video 架构包含以下组件，共 7 个扩散模型。

- 一个冻结的 [T5](https://lilianweng.github.io/posts/2019-01-31-lm/#t5) 文本编码器，提供文本嵌入作为条件输入。
- 一个基础视频扩散模型。
- 一组交错的*空间与时间超分辨率*扩散模型级联，含 3 个 TSR（时间超分辨率）与 3 个 SSR（空间超分辨率）组件。

![](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/imagen-video.png)

*Imagen Video 的级联采样管线。实践中，文本嵌入被注入所有组件而非只有基础模型。（图片来源：Ho et al. 2022 ）*

基础去噪模型以共享参数同时对全部帧执行空间操作，然后时间层跨帧混合激活以更好捕捉时间连贯性——被发现优于帧自回归方法。

![](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/imagen-video-Unet-block.png)

*Imagen Video 扩散模型中一个时空可分块的架构。（图片来源：Ho et al. 2022 ）*

SSR 与 TSR 模型都以逐通道拼接了带噪数据 $\mathbf{z}_t$ 的上采样输入为条件。SSR 用[双线性缩放](https://chao-ji.github.io/jekyll/update/2018/07/19/BilinearResize.html)上采样，TSR 通过重复帧或填充空白帧上采样。

Imagen Video 还应用[渐进蒸馏](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/#prog-distll)加速采样，每次蒸馏迭代可使所需采样步数减半。他们的实验能把全部 7 个视频扩散模型蒸馏到每模型仅 8 步采样，感知质量无可察觉损失。

为获得更好的扩展效果，**Sora**（[Brooks et al. 2024](https://openai.com/research/video-generation-models-as-world-simulators)）利用在视频与图像潜在码的时空 patch 上运作的 [DiT（Diffusion Transformer）](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/#model-architecture)架构。视觉输入表示为时空 patch 序列，充当 Transformer 的输入 token。

![](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/sora.png)

*Sora 是一个扩散 transformer 模型。（图片来源：Brooks et al. 2024 ）*

# 改造图像模型生成视频

扩散视频建模的另一条主要途径是"膨胀（inflate）"预训练的文生图扩散模型——插入时间层，然后可以选择*只*在视频数据上微调新层，或完全避免额外训练。文本-图像对的先验知识被新模型继承，从而有助于缓解对文本-视频对数据的需求。

## 在视频数据上微调

**Make-A-Video**（[Singer et al. 2022](https://arxiv.org/abs/2209.14792)）用时间维度扩展预训练的扩散图像模型，含三个关键组件：

1. 在文本-图像对数据上训练的基础文生图模型。
2. 把网络扩展到时间维度的时空卷积与注意力层。
3. 用于高帧率生成的帧插值网络

![](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/make-a-video.png)

*Make-A-Video 管线示意图。（图片来源：Singer et al. 2022 ）*

最终的视频推理方案可形式化为：

$$
\hat{\mathbf{y}}_t = \text{SR}_h \circ \text{SR}^t_l \circ \uparrow_F \circ D^t \circ P \circ (\hat{\mathbf{x}}, \text{CLIP}_\text{text}(\mathbf{x}))
$$

其中：

- $\mathbf{x}$ 是输入文本。
- $\hat{\mathbf{x}}$ 是 BPE 编码的文本。
- $\text{CLIP}_\text{text}(.)$ 是 CLIP 文本编码器，$\mathbf{x}_e = \text{CLIP}_\text{text}(\mathbf{x})$。
- $P(.)$ 是先验，给定文本嵌入 $\mathbf{x}_e$ 与 BPE 编码文本 $\hat{\mathbf{x}}$ 生成图像嵌入 $\mathbf{y}_e$：$\mathbf{y}_e = P(\mathbf{x}_e, \hat{\mathbf{x}})$。该部分在文本-图像对数据上训练，不在视频数据上微调。
- $D^t(.)$ 是时空解码器，生成 16 帧的序列，每帧是低分辨率 64x64 RGB 图像 $\hat{\mathbf{y}}_l$。
- $\uparrow_F(.)$ 是帧插值网络，通过在生成帧间插值提高有效帧率。这是为视频上采样预测掩码帧任务微调的模型。
- $\text{SR}_h(.), \text{SR}^t_l(.)$ 是空间与时空超分辨率模型，分别把图像分辨率提升到 256x256 与 768x768。
- $\hat{\mathbf{y}}_t$ 是最终生成的视频。

时空 SR 层含伪 3D 卷积层与伪 3D 注意力层：

- 伪 3D 卷积层：每个空间 2D 卷积层（从预训练图像模型初始化）后接一个时间 1D 层（初始化为恒等函数）。概念上，2D 卷积层先生成多帧，然后帧被重整为视频片段。
- 伪 3D 注意力层：每个（预训练的）空间注意力层之后堆叠一个时间注意力层，用来近似完整的时空注意力层。

![](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/make-a-video-layers.png)

*伪 3D 卷积（左）与注意力（右）层的工作方式。（图片来源：Singer et al. 2022 ）*

它们可表示为：

$$
\begin{aligned}
\text{Conv}_\text{P3D} &= \text{Conv}_\text{1D}(\text{Conv}_\text{2D}(\mathbf{h}) \circ T) \circ T \\
\text{Attn}_\text{P3D} &= \text{flatten}^{-1}(\text{Attn}_\text{1D}(\text{Attn}_\text{2D}(\text{flatten}(\mathbf{h})) \circ T) \circ T)
\end{aligned}
$$

其中输入张量 $\mathbf{h} \in \mathbb{R}^{B\times C \times F \times H \times W}$（对应批大小、通道、帧、高与宽）；$\circ T$ 在时间与空间维度间交换；$\text{flatten}(.)$ 是把 $\mathbf{h}$ 变换为 $\mathbf{h}’ \in \mathbb{R}^{B \times C \times F \times HW}$ 的矩阵算子，$\text{flatten}^{-1}(.)$ 反向该过程。

训练时，Make-A-Video 管线的不同组件独立训练。

1. 解码器 $D^t$、先验 $P$ 与两个超分辨率组件 $\text{SR}_h, \text{SR}^t_l$ 先只在图像上训练，不带配对文本。
2. 接着加入新的时间层（初始化为恒等函数），然后在无标注视频数据上微调。

**Tune-A-Video**（[Wu et al. 2023](https://openaccess.thecvf.com/content/ICCV2023/html/Wu_Tune-A-Video_One-Shot_Tuning_of_Image_Diffusion_Models_for_Text-to-Video_Generation_ICCV_2023_paper.html)）膨胀预训练图像扩散模型以实现单样本视频调优：给定含 $m$ 帧的视频 $\mathcal{V} = \{v_i \mid i = 1, \dots, m\}$ 配描述性提示 $\tau$，任务是按稍作编辑的相关文本提示 $\tau^*$ 生成新视频 $\mathcal{V}^*$。例如 $\tau$ = `"A man is skiing"` 可扩展为 $\tau^*$=`"Spiderman is skiing on the beach"`。Tune-A-Video 面向物体编辑、背景替换与风格迁移。

除膨胀 2D 卷积层外，Tune-A-Video 的 U-Net 架构纳入 ST-Attention（时空注意力）块，通过查询先前帧中的相关位置捕捉时间一致性。给定帧 $v_i$、先前帧 $v_{i-1}$ 与第一帧 $v_1$ 的潜在特征投影为查询 $\mathbf{Q}$、键 $\mathbf{K}$ 与值 $\mathbf{V}$，ST-attention 定义为：

$$
\begin{aligned}
&\mathbf{Q} = \mathbf{W}^Q \mathbf{z}_{v_i}, \quad \mathbf{K} = \mathbf{W}^K [\mathbf{z}_{v_1}, \mathbf{z}_{v_{i-1}}], \quad \mathbf{V} = \mathbf{W}^V [\mathbf{z}_{v_1}, \mathbf{z}_{v_{i-1}}] \\
&\mathbf{O} = \text{softmax}\Big(\frac{\mathbf{Q} \mathbf{K}^\top}{\sqrt{d}}\Big) \cdot \mathbf{V}
\end{aligned}
$$

![](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/tune-a-video.png)

*Tune-A-Video 架构概览。它在采样阶段前先对单个视频跑轻量微调阶段。注意整个时间自注意力（T-Attn）层被微调（因为是新增的），但微调时只更新 ST-Attn 与 Cross-Attn 中的查询投影，以保留先验的文生图知识。ST-Attn 提升时空一致性，Cross-Attn 精炼文本-视频对齐。（图片来源：Wu et al. 2023 ）*

Runway 的 **Gen-1** 模型（[Esser et al. 2023](https://arxiv.org/abs/2302.03011)）针对按文本输入编辑给定视频的任务。它把生成条件分解为视频的*结构*与*内容* $p(\mathbf{x} \mid s, c)$。但对这两个方面做清晰分解并不容易。

- *内容* $c$ 指视频的外观与语义，从文本采样用于条件编辑。帧的 CLIP 嵌入是内容的良好表示，且与结构特征大体正交。
- *结构* $s$ 描绘几何与动态，包括物体的形状、位置、随时间的变化，$s$ 从输入视频采样。深度估计或其他任务专属边信息（如人体视频合成的身体姿态或面部关键点）可用。

Gen-1 的架构变化相当标准：残差块中每个 2D 空间卷积层后加 1D 时间卷积层，注意力块中每个 2D 空间注意力块后加 1D 时间注意力块。训练时，结构变量 $s$ 与扩散潜在变量 $\mathbf{z}$ 拼接，内容变量 $c$ 在交叉注意力层提供。推理时，通过一个先验把 CLIP 文本嵌入转换为 CLIP 图像嵌入。

![](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/gen-1.png)

*Gen-1 模型训练管线概览。（图片来源：Esser et al. 2023 ）*

**Video LDM**（[Blattmann et al. 2023](https://arxiv.org/abs/2304.08818)）先训练一个 [LDM](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/#latent-variable-space)（潜在扩散模型）图像生成器。然后微调模型加入时间维度以产生视频。微调只应用于编码图像序列上这些新增的时间层。Video LDM 的时间层 $\{l^i_\phi \mid i = \ 1, \dots, L\}$（见图 10）与既有空间层 $l^i_\theta$ 交错，后者在微调中保持*冻结*。也就是说，我们只微调新参数 $\phi$ 而非预训练图像骨干参数 $\theta$。Video LDM 管线先以低 fps 生成关键帧，然后经 2 步潜在帧插值提高 fps。

长度 $T$ 的输入序列被基础图像模型 $\theta$ 解释为一批图像（即 $B \cdot T$），然后为 $l^i_\phi$ 时间层重整为视频格式。有一条跳连，通过学到的合并参数 $\alpha$ 把时间层输出 $\mathbf{z}’$ 与空间输出 $\mathbf{z}$ 组合。实践中有两种时间混合层：(1) 时间注意力与 (2) 基于 3D 卷积的残差块。

![](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/video-LDM.png)

*把预训练的图像合成 LDM 扩展为视频生成器。$B, T, C, H, W$ 分别是批大小、序列长度、通道、高与宽。$\mathbf{c}_S$ 是可选的条件/上下文帧。（图片来源：Blattmann et al. 2023 ）*

然而，LDM 的预训练自编码器仍有个问题——它只见过图像从未见过视频。朴素地用它做视频生成可能在没有良好时间连贯性的情况下产生闪烁伪影。所以 Video LDM 向解码器加入额外时间层，并用基于 3D 卷积的逐块时间判别器在视频数据上微调，同时编码器保持不变使我们仍能复用预训练 LDM。时间解码器微调期间，冻结的编码器独立处理视频中每帧，并用视频感知的判别器强制跨帧的时间连贯重建。

![](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/video-LDM-autoencoder.png)

*视频潜在扩散模型中自编码器的训练管线。解码器带新的跨帧判别器微调以获得时间连贯性，编码器保持冻结。（图片来源：Blattmann et al. 2023 ）*

与 Video LDM 类似，**Stable Video Diffusion（SVD**；[Blattmann et al. 2023](https://arxiv.org/abs/2311.15127)）的架构设计也基于 LDM，在每个空间卷积与注意力层后插入时间层，但 SVD 微调整个模型。训练视频 LDM 有三个阶段：

1. *文生图预训练*重要，有助于同时提升质量与提示跟随。
2. *视频预训练*宜分开进行，最好在更大规模的精选数据集上。
3. *高质量视频微调*使用更小、预先配好字幕、高视觉保真的视频。

SVD 特别强调*数据集策展（dataset curation）*对模型性能的关键作用。他们应用镜头切换检测管线获得每视频更多切分，然后用三个不同的字幕模型：(1) CoCa 标注中间帧，(2) V-BLIP 做视频字幕，(3) 基于前两个字幕用 LLM 生成字幕。然后他们持续改进视频数据集：移除运动少的片段（用 2 fps 计算的低光流分数过滤）、文字过多的片段（用光学字符识别识别大量文字的视频）、或总体美学价值低的片段（用 CLIP 嵌入标注每片段的首、中、尾帧并计算美学分数与文图相似度）。实验表明，过滤后的更高质量数据集带来更好的模型质量，即使该数据集小得多。

先生成远处关键帧再用时间超分辨率加插值的关键挑战是如何维持高质量的时间一致性。**Lumiere**（[Bar-Tal et al. 2024](https://arxiv.org/abs/2401.12945)）改用**时空 U-Net（space-time U-Net，STUNet）**架构，单趟*一次性*生成视频的整个时长，移除了对 TSR（时间超分辨率）组件的依赖。STUNet 在时间与空间两个维度对视频下采样，于是昂贵的计算发生在紧凑的时空潜在空间中。

![](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/lumiere.png)

*Lumiere 移除 TSR（时间超分辨率）模型。膨胀后的 SSR 网络因内存限制只能在视频的短片段上运行，因此 SSR 模型在一组更短但重叠的视频小段上运行。（图片来源：Bar-Tal et al. 2024 ）*

STUNet 膨胀一个*预训练的*文生图 U-net，使其能在时间与空间维度对视频下采样与上采样。基于卷积的块由预训练文生图层后接因子化的时空卷积组成。最粗 U-Net 层级中基于注意力的块含预训练文生图后接时间注意力。进一步训练*只*发生在新增层。

![](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/lumiere-STUnet.png)

*(a) 时空 U-Net（STUNet）、(b) 基于卷积的块、(c) 基于注意力的块的架构。（图片来源：Bar-Tal et al. 2024 ）*

## 免训练改造

有些出人意料的是，可以把预训练文生图模型改造为输出视频而无需任何训练 🤯。

若我们朴素地随机采样一列潜在码再解码对应图像构造视频，无法保证物体与语义在时间上的一致。**Text2Video-Zero**（[Khachatryan et al. 2023](https://arxiv.org/abs/2303.13439)）通过为预训练图像扩散模型增强两个时间一致性关键机制，实现零样本、免训练的视频生成：

1. 带*运动动力学*地采样潜在码序列，保持全局场景与背景在时间上一致；
2. 用每帧对第一帧的*新跨帧注意力*重编程帧级自注意力，以保留前景物体的上下文、外观与身份。

![](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/text2video-zero.png)

*Text2Video-Zero 管线概览。（图片来源：Khachatryan et al. 2023 ）*

带运动信息地采样潜在变量序列 $\mathbf{x}^1_T, \dots, \mathbf{x}^m_T$ 的过程描述如下：

1. 定义方向 $\boldsymbol{\delta} = (\delta_x, \delta_y) \in \mathbb{R}^2$ 控制全局场景与相机运动；默认设 $\boldsymbol{\delta} = (1, 1)$。另定义控制全局运动量的超参数 $\lambda > 0$。
2. 首先随机采样第一帧的潜在码，$\mathbf{x}^1_T \sim \mathcal{N}(0, I)$；
3. 用预训练图像扩散模型（论文中如 Stable Diffusion（SD）模型）执行 $\Delta t \geq 0$ 步 DDIM 反向更新，得到对应潜在码 $\mathbf{x}^1_{T’}$，$T’ = T - \Delta t$。
4. 对潜在码序列的每帧，按 $\boldsymbol{\delta}^k = \lambda(k-1)\boldsymbol{\delta}$ 定义的扭曲操作施加相应运动平移，得 $\tilde{\mathbf{x}}^k_{T’}$。
5. 最后对所有 $\tilde{\mathbf{x}}^{2:m}_{T’}$ 施加 DDIM 前向步，得 $\mathbf{x}^{2:m}_T$。

$$
\begin{aligned}
\mathbf{x}^1_{T'} &= \text{DDIM-backward}(\mathbf{x}^1_T, \Delta t)\text{ where }T' = T - \Delta t \\
W_k &\gets \text{a warping operation of }\boldsymbol{\delta}^k = \lambda(k-1)\boldsymbol{\delta} \\
\tilde{\mathbf{x}}^k_{T'} &= W_k(\mathbf{x}^1_{T'})\\
\mathbf{x}^k_T &= \text{DDIM-forward}(\tilde{\mathbf{x}}^k_{T'}, \Delta t)\text{ for }k=2, \dots, m
\end{aligned}
$$

此外，Text2Video-Zero 把预训练 SD 模型中的自注意力层替换为参照*第一*帧的新跨帧注意力机制。动机是在整个生成视频中保留前景物体外观、形状与身份的信息。

$$
\text{Cross-Frame-Attn}(\mathbf{Q}^k, \mathbf{K}^{1:m}, \mathbf{V}^{1:m}) = \text{Softmax}\Big( \frac{\mathbf{Q}^k (\mathbf{K}^1)^\top}{\sqrt{c}} \Big) \mathbf{V}^1
$$

可选地，背景掩码可用于进一步平滑并改进背景一致性。设我们用某种既有方法得到第 $k$ 帧的前景掩码 $\mathbf{M}_k$，背景平滑在扩散步 $t$ 按背景矩阵融合实际与扭曲的潜在码：

$$
\bar{\mathbf{x}}^k_t = \mathbf{M}^k \odot \mathbf{x}^k_t + (1 − \mathbf{M}^k) \odot (\alpha\tilde{\mathbf{x}}^k_t +(1−\alpha)\mathbf{x}^k_t)\quad\text{for }k=1, \dots, m
$$

其中 $\mathbf{x}^k_t$ 是实际潜在码，$\tilde{\mathbf{x}}^k_t$ 是背景上扭曲的潜在码；$\alpha$ 是超参数，论文实验中设 $\alpha=0.6$。

Text2video-zero 可与 [ControlNet](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/#controlnet) 结合：在每个扩散时间步 $t = T , \dots, 1$ 对每个 $\mathbf{x}^k_t$（$k = 1, \dots, m$）逐帧应用 ControlNet 预训练复制分支，并把 ControlNet 分支输出加到主 U-net 的跳连中。

**ControlVideo**（[Zhang et al. 2023](https://arxiv.org/abs/2305.13077)）旨在按文本提示 $\tau$ 与运动序列（如深度或边缘图）$\mathbf{c} = \{c^i\}_{i=0}^{N-1}$ 为条件生成视频。它改编自 [ControlNet](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/#controlnet)，新增三个机制：

1. *跨帧注意力*：在自注意力模块中加入完全的跨帧交互。它把*所有时间步*的潜在帧映射进 $\mathbf{Q}, \mathbf{K}, \mathbf{V}$ 矩阵以引入所有帧之间的交互，不同于 Text2Video-zero 只配置所有帧关注*第一*帧。
2. *交错帧平滑器*是在交替帧上采用帧插值以减少闪烁效应的机制。每个时间步 $t$，平滑器插值偶数或奇数帧以平滑其对应的三帧片段。注意平滑步骤后帧数随时间减少。
3. *层级采样器*利用层级采样器，在内存约束下实现时间一致的长视频。长视频被切成多个短片段，各选一个关键帧。模型以完全跨帧注意力预生成这些关键帧以获得长期连贯性，每个对应短片段以关键帧为条件依次合成。

![](https://lilianweng.github.io/posts/2024-04-12-diffusion-video/control-video.png)

*ControlVideo 概览。（图片来源：Zhang et al. 2023 ）*

# 引用

引用格式：

> Weng, Lilian. (Apr 2024). Diffusion Models Video Generation. Lil'Log. https://lilianweng.github.io/posts/2024-04-12-diffusion-video/.

或

```
@article{weng2024video,
  title   = "Diffusion Models Video Generation.",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io",
  year    = "2024",
  month   = "Apr",
  url     = "https://lilianweng.github.io/posts/2024-04-12-diffusion-video/"
}
```

# 参考文献

[1] Cicek et al. 2016. ["3D U-Net: Learning Dense Volumetric Segmentation from Sparse Annotation."](https://arxiv.org/abs/1606.06650)

[2] Ho & Salimans, et al. ["Video Diffusion Models."](https://arxiv.org/abs/2204.03458) 2022 | [webpage](https://video-diffusion.github.io/)

[3] Bar-Tal et al. 2024 ["Lumiere: A Space-Time Diffusion Model for Video Generation."](https://arxiv.org/abs/2401.12945)

[4] Brooks et al. ["Video generation models as world simulators."](https://openai.com/research/video-generation-models-as-world-simulators) OpenAI Blog, 2024.

[5] Zhang et al. 2023 ["ControlVideo: Training-free Controllable Text-to-Video Generation."](https://arxiv.org/abs/2305.13077)

[6] Khachatryan et al. 2023 ["Text2Video-Zero: Text-to-image diffusion models are zero-shot video generators."](https://arxiv.org/abs/2303.13439)

[7] Ho, et al. 2022 ["Imagen Video: High Definition Video Generation with Diffusion Models."](https://arxiv.org/abs/2210.02303)

[8] Singer et al. ["Make-A-Video: Text-to-Video Generation without Text-Video Data."](https://arxiv.org/abs/2209.14792) 2022.

[9] Wu et al. ["Tune-A-Video: One-Shot Tuning of Image Diffusion Models for Text-to-Video Generation."](https://openaccess.thecvf.com/content/ICCV2023/html/Wu_Tune-A-Video_One-Shot_Tuning_of_Image_Diffusion_Models_for_Text-to-Video_Generation_ICCV_2023_paper.html) ICCV 2023.

[10] Blattmann et al. 2023 ["Align your Latents: High-Resolution Video Synthesis with Latent Diffusion Models."](https://arxiv.org/abs/2304.08818)

[11] Blattmann et al. 2023 ["Stable Video Diffusion: Scaling Latent Video Diffusion Models to Large Datasets."](https://arxiv.org/abs/2311.15127)

[12] Esser et al. 2023 ["Structure and Content-Guided Video Synthesis with Diffusion Models."](https://arxiv.org/abs/2302.03011)

[13] Bar-Tal et al. 2024 ["Lumiere: A Space-Time Diffusion Model for Video Generation."](https://arxiv.org/abs/2401.12945)
