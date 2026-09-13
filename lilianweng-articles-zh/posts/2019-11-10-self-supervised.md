---
title: "自监督表征学习"
title_en: "Self-Supervised Representation Learning"
source: https://lilianweng.github.io/posts/2019-11-10-self-supervised/
crawled: 2026-09-08
translated: 2026-09-08
---

# 自监督表征学习

> 原文：[Self-Supervised Representation Learning](https://lilianweng.github.io/posts/2019-11-10-self-supervised/) · Lilian Weng（翁荔）

> 自监督学习为更好地利用无标注数据打开了巨大机会，同时以监督学习的方式学习。本文涵盖图像、视频和控制问题上自监督学习任务的许多有趣想法。

<span style="color: #286ee0;">[更新于 2020-01-09：新增[对比预测编码](#contrastive-predictive-coding)一节。]</span>
<br/>
~~<span style="color: #286ee0;">[更新于 2020-04-13：新增关于 MoCo、SimCLR 和 CURL 的"动量对比"一节。]</span>~~
<br/>
<span style="color: #286ee0;">[更新于 2020-07-08：新增关于 DeepMDP 与 DBC 的["双模拟（Bisimulation）"](#bisimulation)一节。]</span>
<br/>
~~<span style="color: #286ee0;">[更新于 2020-09-12：在"动量对比"一节新增 [MoCo V2](https://lilianweng.github.io/posts/2021-05-31-contrastive/#moco--moco-v2) 和 [BYOL](https://lilianweng.github.io/posts/2021-05-31-contrastive/#byol)。]</span>~~
<br/>
<span style="color: #286ee0;">[更新于 2021-05-31：移除"动量对比"一节，新增指向完整文章["对比表征学习"](https://lilianweng.github.io/posts/2021-05-31-contrastive/)的链接。]</span>

给定一个任务和足够的标签，监督学习能把它解决得很好。好的性能通常需要相当数量的标签，但收集人工标签昂贵（如 ImageNet）且难以规模化。考虑到无标注数据（如自由文本、互联网上的所有图像）的量远超有限的人工标注数据集，不用它们有点浪费。然而，无监督学习并不容易，通常效率远低于监督学习。

如果能为无标注数据免费获得标签、以监督方式训练无标注数据集呢？我们可以通过把监督学习任务框定为特殊形式来实现——只用其余信息预测信息的某个子集。这样，所需的一切信息（输入与标签）都已提供。这就是*自监督学习（self-supervised learning）*。

这一思想已在语言建模中广泛使用。语言模型的默认任务是给定过去序列预测下一个词。[BERT](https://lilianweng.github.io/posts/2019-01-31-lm/#bert) 增加了两个辅助任务，二者都依赖自生成的标签。

![Self-supervised learning summary](https://lilianweng.github.io/posts/2019-11-10-self-supervised/self-sup-lecun.png)

*图 1：如何构建自监督学习任务的一个精彩总结。（图片来源：[LeCun 的演讲](https://www.youtube.com/watch?v=7I0Qt7GALVk)）*

[这里](https://github.com/jason718/awesome-self-supervised-learning)有一份精心整理的自监督学习论文列表。想深入阅读请查看。

注意本文不聚焦 NLP/[语言建模](https://lilianweng.github.io/posts/2019-01-31-lm/)或[生成建模](https://lilianweng.github.io/lil-log/tag/generative-model)。

## 为什么需要自监督学习？

自监督学习使我们能利用数据自带的多种免费标签。动机相当直接：生产带干净标签的数据集昂贵，而无标注数据每时每刻都在产生。要利用这量大得多的无标注数据，一条路是把学习目标设定得当，从数据本身获取监督。

*自监督任务（self-supervised task）*也称*前置任务（pretext task）*，引导我们得到一个监督损失函数。但我们通常并不关心这个虚构任务的最终表现，而是对学到的中间表示感兴趣，期望该表示携带良好的语义或结构含义、有益于多种实际下游任务。

例如，我们可以随机旋转图像并训练模型预测每张输入图像被旋转了多少。旋转预测任务是虚构的，实际准确率不重要（就像我们对辅助任务的态度）。但我们期望模型为真实任务学到高质量的潜在变量，例如用极少标注样本构建目标识别分类器。

宽泛地说，所有生成模型都可视为自监督的，但目标不同：生成模型专注于创造多样且真实的图像，而自监督表征学习关心产出通常对许多任务有帮助的良好特征。生成建模不是本文重点，欢迎查看我的[往期文章](https://lilianweng.github.io/lil-log/tag/generative-model)。

## 基于图像

图像自监督表征学习已有许多想法。常见工作流是：在无标注图像上用一个或多个前置任务训练模型，然后用该模型某个中间特征层喂给 ImageNet 分类上的多项逻辑回归分类器。最终分类准确率量化所学表示的好坏。

最近，一些研究者提出用共享权重同时在标注数据上训练监督学习、在无标注数据上训练自监督前置任务，如 [Zhai et al, 2019](https://arxiv.org/abs/1905.03670) 和 [Sun et al, 2019](https://arxiv.org/abs/1909.11825)。

### 形变

我们期望图像的小形变不改变其原始语义或几何形态。轻微形变的图像被视为与原图相同，因此学到的特征被期望对形变不变。

<mark><b>Exemplar-CNN</b></mark>（[Dosovitskiy et al., 2015](https://arxiv.org/abs/1406.6909)）用无标注图像块创建代理训练数据集：
1. 从不同图像以不同位置和尺度采样 $$N$$ 个 32 × 32 像素的块，只从含可观梯度的区域采（这些区域覆盖边缘、往往包含物体或物体部分）。它们是*"范例（exemplary）"*块。
2. 每个块通过施加多种随机变换（平移、旋转、缩放等）做形变。所有得到的形变块被视为属于*同一代理类*。
3. 前置任务是在一组代理类之间做判别。我们可以任意创建任意多的代理类。

![Examplar CNN](https://lilianweng.github.io/posts/2019-11-10-self-supervised/examplar-cnn.png)

*图 2：可爱鹿的原始块在左上角。施加随机变换产生多种形变块。在前置任务中它们都应被归入同一类。（图片来源：[Dosovitskiy et al., 2015](https://arxiv.org/abs/1406.6909)）*

整图<mark><b>旋转</b></mark>（[Gidaris et al. 2018](https://arxiv.org/abs/1803.07728)）是另一种有趣且廉价的修改输入图像的方式，同时语义内容不变。每张输入图像先随机旋转 $$90^\circ$$ 的倍数，对应 $$[0^\circ, 90^\circ, 180^\circ, 270^\circ]$$。模型被训练来预测施加了哪种旋转，因此是 4 分类问题。

要识别不同旋转下的同一图像，模型必须学会识别高层物体部位（如头、鼻子、眼睛）及这些部位的相对位置，而非局部模式。这一前置任务以这种方式驱动模型学习物体的语义概念。

![Self supervised by rotation prediction](https://lilianweng.github.io/posts/2019-11-10-self-supervised/self-sup-rotation.png)

*图 3：旋转整张输入图像的自监督学习示意图。模型学习预测施加了哪种旋转。（图片来源：[Gidaris et al. 2018](https://arxiv.org/abs/1803.07728)）*

### 图块

第二类自监督学习任务从一张图像提取多个块，让模型预测这些块之间的关系。

[Doersch et al. (2015)](https://arxiv.org/abs/1505.05192) 把前置任务形式化为预测一张图像两个随机块的<mark><b>相对位置</b></mark>。模型需要理解物体的空间上下文才能说出各部分之间的相对位置。

训练块按如下方式采样：
1. 不参照图像内容随机采样第一个块。
2. 设第一个块位于 3x3 网格中央，第二个块从其周围 8 个相邻位置采样。
3. 为避免模型只抓住低级平凡信号（如跨边界连接直线或匹配局部模式），引入额外噪声：
    - 块之间留间隙
    - 小幅抖动
    - 随机把部分块降采样到总共 100 像素再上采样，建立对像素化的鲁棒性
    - 把绿色和品红向灰色偏移，或随机丢弃 3 个颜色通道中的 2 个（见下文["色差"](#chromatic-aberration)）
4. 模型被训练来预测第二个块取自 8 个相邻位置中的哪一个，是 8 分类的分类问题。

![Self-supervised learning by context](https://lilianweng.github.io/posts/2019-11-10-self-supervised/self-sup-by-relative-position.png)

*图 4：通过预测两个随机块的相对位置做自监督学习的示意图。（图片来源：[Doersch et al., 2015](https://arxiv.org/abs/1505.05192)）*

<a href="#chromatic-aberration"></a>除边界模式或纹理延续这类平凡信号外，还发现了一个有趣且有点出人意料的平凡解，称为[*"色差"*](https://en.wikipedia.org/wiki/Chromatic_aberration)（chromatic aberration）。它由不同波长的光穿过镜头时焦距不同引发。过程中颜色通道之间可能存在小的偏移。于是模型可以仅通过比较绿色和品红在两个块中如何分离来判断相对位置。这是与图像内容无关的平凡解。把绿色和品红向灰色偏移或随机丢弃 3 个颜色通道中的 2 个进行预处理可以避免该平凡解。

![Chromatic aberration](https://lilianweng.github.io/posts/2019-11-10-self-supervised/chromatic-aberration.png)

*图 5：色差如何发生的示意图。（图片来源：[wikipedia](https://upload.wikimedia.org/wikipedia/commons/a/aa/Chromatic_aberration_lens_diagram.svg)）*

既然上面的任务已经为每张图像设置了 3x3 网格，何不用全部 9 个块而非只用 2 个来加大难度？沿这一思路，[Noroozi & Favaro (2016)](https://arxiv.org/abs/1603.09246) 设计了<mark><b>拼图</b></mark>游戏作为前置任务：模型被训练来把 9 个打乱的块放回原位。

一个卷积网络以共享权重独立处理每个块，输出预定义排列集合中每个块索引的概率向量。为控制拼图难度，论文提出按预定义排列集打乱块，并配置模型预测该集合上所有索引的概率向量。

因为输入块如何被打乱不改变要预测的正确顺序。一个加速训练的潜在改进是使用置换不变的图卷积网络（GCN），这样不必多次打乱同一组块，思路与这篇[论文](https://arxiv.org/abs/1911.00025)相同。

![Jigsaw puzzle](https://lilianweng.github.io/posts/2019-11-10-self-supervised/self-sup-jigsaw-puzzle.png)

*图 6：通过解拼图做自监督学习的示意图。（图片来源：[Noroozi & Favaro, 2016](https://arxiv.org/abs/1603.09246)）*

另一个想法是把"特征"或"视觉基元"视为可在多个块上求和、可跨块比较的标量值属性。于是块之间的关系可以由<mark><b>计数特征</b></mark>和简单算术定义（[Noroozi, et al, 2017](https://arxiv.org/abs/1708.06734)）。

论文考虑两种变换：
1. *缩放*：图像放大 2 倍，视觉基元数量应保持不变。
2. *平铺*：图像平铺成 2x2 网格，视觉基元数量应为总和，即原特征计数的 4 倍。

模型用上述特征计数关系学习特征编码器 $$\phi(.)$$。给定输入图像 $$\mathbf{x} \in \mathbb{R}^{m \times n \times 3}$$，考虑两类变换算子：
1. 降采样算子 $$D: \mathbb{R}^{m \times n \times 3} \mapsto \mathbb{R}^{\frac{m}{2} \times \frac{n}{2} \times 3}$$：降采样 2 倍
2. 平铺算子 $$T_i: \mathbb{R}^{m \times n \times 3} \mapsto \mathbb{R}^{\frac{m}{2} \times \frac{n}{2} \times 3}$$：从图像 2x2 网格中抽取第 $$i$$ 块。

我们期望学到：

$$
\phi(\mathbf{x}) = \phi(D \circ \mathbf{x}) = \sum_{i=1}^4 \phi(T_i \circ \mathbf{x})
$$

<a href="#counting-feature-loss" />于是 MSE 损失为：$$\mathcal{L}_\text{feat} = \|\phi(D \circ \mathbf{x}) - \sum_{i=1}^4 \phi(T_i \circ \mathbf{x})\|^2_2$$。为避免平凡解 $$\phi(\mathbf{x}) = \mathbf{0}, \forall{\mathbf{x}}$$，加入另一损失项鼓励不同图像特征之间的差异：$$\mathcal{L}_\text{diff} = \max(0, c -\|\phi(D \circ \mathbf{y}) - \sum_{i=1}^4 \phi(T_i \circ \mathbf{x})\|^2_2)$$，其中 $$\mathbf{y}$$ 是另一张不同于 $$\mathbf{x}$$ 的输入图像，$$c$$ 是标量常数。最终损失为：

$$
\mathcal{L} 
= \mathcal{L}_\text{feat} + \mathcal{L}_\text{diff} 
= \|\phi(D \circ \mathbf{x}) - \sum_{i=1}^4 \phi(T_i \circ \mathbf{x})\|^2_2 + \max(0, M -\|\phi(D \circ \mathbf{y}) - \sum_{i=1}^4 \phi(T_i \circ \mathbf{x})\|^2_2)
$$

![Counting features](https://lilianweng.github.io/posts/2019-11-10-self-supervised/self-sup-counting-features.png)

*图 7：通过计数特征做自监督表征学习。（图片来源：[Noroozi, et al, 2017](https://arxiv.org/abs/1708.06734)）*

### 着色

<mark><b>着色（Colorization）</b></mark>可用作强大的自监督任务：模型被训练为灰度输入图像着色；确切地说，任务是把图像映射到量化颜色值输出上的分布（[Zhang et al. 2016](https://arxiv.org/abs/1603.08511)）。

模型在 [CIE L*a*b* 颜色空间](https://en.wikipedia.org/wiki/CIELAB_color_space)中输出颜色。L*a*b* 颜色为逼近人类视觉而设计，相比之下 RGB 或 CMYK 建模物理设备的颜色输出。
- L* 分量匹配人对亮度的感知；L* = 0 为黑，L* = 100 为白。
- a* 分量表示绿（负）/品红（正）值。
- b* 分量建模蓝（负）/黄（正）值。

由于着色问题的多模态性质，分箱颜色值预测分布的交叉熵损失优于原始颜色值的 L2 损失。a*b* 颜色空间以桶大小 10 量化。

为在常见颜色（通常是低 a*b* 值，如云、墙壁、泥土等常见背景）与罕见颜色（很可能与图像中关键物体相关）之间取得平衡，损失函数用提升不 frequent 颜色桶损失的权重项做了再平衡。这就像信息检索模型中对词打分为什么需要 [tf 和 idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) 两者一样。权重项构造为：(1-λ) * 高斯核平滑的经验概率分布 + λ * 均匀分布，两个分布都定义在量化的 a*b* 颜色空间上。

### 生成建模

生成建模中的前置任务是重建原始输入，同时学习有意义的潜在表示。

<mark><b>去噪自编码器</b></mark>（[Vincent, et al, 2008](https://www.cs.toronto.edu/~larocheh/publications/icml-2008-denoising-autoencoders.pdf)）学习从部分损坏或含随机噪声的版本恢复图像。该设计的灵感来自：即使有噪声，人类也能轻易认出图中的物体，表明关键视觉特征可以与噪声分离开来提取。见我的[旧文](https://lilianweng.github.io/posts/2018-08-12-vae/#denoising-autoencoder)。

<mark><b>上下文编码器（context encoder）</b></mark>（[Pathak, et al., 2016](https://arxiv.org/abs/1604.07379)）被训练来填补图像中缺失的一块。设 $$\hat{M}$$ 为二值掩码，被丢弃像素为 0、保留输入像素为 1。模型以重建（L2）损失与对抗损失的组合作训练。掩码定义的移除区域可以是任何形状。

$$
\begin{aligned}
\mathcal{L}(\mathbf{x}) &= \mathcal{L}_\text{recon}(\mathbf{x}) + \mathcal{L}_\text{adv}(\mathbf{x})\\
\mathcal{L}_\text{recon}(\mathbf{x}) &= \|(1 - \hat{M}) \odot (\mathbf{x} - E(\hat{M} \odot \mathbf{x})) \|_2^2 \\
\mathcal{L}_\text{adv}(\mathbf{x}) &= \max_D \mathbb{E}_{\mathbf{x}} [\log D(\mathbf{x}) + \log(1 - D(E(\hat{M} \odot \mathbf{x})))]
\end{aligned}
$$

其中 $$E(.)$$ 是编码器，$$D(.)$$ 是解码器。

![Context encoder](https://lilianweng.github.io/posts/2019-11-10-self-supervised/context-encoder.png)

*图 8：上下文编码器示意图。（图片来源：[Pathak, et al., 2016](https://arxiv.org/abs/1604.07379)）*

对图像施加掩码时，上下文编码器移除了部分区域所有颜色通道的信息。那只隐藏一部分通道呢？<mark><b>裂脑自编码器（split-brain autoencoder）</b></mark>（[Zhang et al., 2017](https://arxiv.org/abs/1611.09842)）通过从其余通道预测一部分颜色通道来实现。设数据张量 $$\mathbf{x} \in \mathbb{R}^{h \times w \times \vert C \vert }$$（含 $$C$$ 个颜色通道）为网络第 $$l$$ 层的输入。它被切分为两个不相交的部分 $$\mathbf{x}_1 \in \mathbb{R}^{h \times w \times \vert C_1 \vert}$$ 和 $$\mathbf{x}_2 \in \mathbb{R}^{h \times w \times \vert C_2 \vert}$$，其中 $$C_1 , C_2 \subseteq C$$。然后训练两个子网络做两个互补预测：一个网络 $$f_1$$ 从 $$\mathbf{x}_1$$ 预测 $$\mathbf{x}_2$$，另一个网络 $$f_1$$ 从 $$\mathbf{x}_2$$ 预测 $$\mathbf{x}_1$$。损失为 L1 损失或（若颜色值量化）交叉熵。

切分可以在 RGB-D 或 L*a*b* 色彩空间上做一次，也可以在 CNN 网络的每一层做，此时通道数可以是任意的。

![Split-brain autoencoder](https://lilianweng.github.io/posts/2019-11-10-self-supervised/split-brain-autoencoder.png)

*图 9：裂脑自编码器示意图。（图片来源：[Zhang et al., 2017](https://arxiv.org/abs/1611.09842)）*

生成对抗网络（GAN）能学习从简单潜变量映射到任意复杂的数据分布。研究表明，这类生成模型的潜空间能捕捉数据中的语义变化；例如在人脸数据上训练 GAN 时，某些潜变量与表情、眼镜、性别等相关（[Radford et al., 2016](https://arxiv.org/abs/1511.06434)）。

<mark><b>双向 GAN（Bidirectional GANs）</b></mark>（[Donahue, et al, 2017](https://arxiv.org/abs/1605.09782)）引入额外的编码器 $$E(.)$$ 来学习从输入到潜变量 $$\mathbf{z}$$ 的映射。判别器 $$D(.)$$ 在输入数据与潜在表示的联合空间 $$(\mathbf{x}, \mathbf{z})$$ 中预测，区分生成对 $$(\mathbf{x}, E(\mathbf{x}))$$ 与真实对 $$(G(\mathbf{z}), \mathbf{z})$$。模型被训练来优化目标：$$\min_{G, E} \max_D V(D, E, G)$$，其中生成器 $$G$$ 和编码器 $$E$$ 学习生成足够逼真以迷惑判别器的数据与潜变量，同时判别器 $$D$$ 尽力区分真实与生成数据。

$$
V(D, E, G) = \mathbb{E}_{\mathbf{x} \sim p_\mathbf{x}} [ \underbrace{\mathbb{E}_{\mathbf{z} \sim p_E(.\vert\mathbf{x})}[\log D(\mathbf{x}, \mathbf{z})]}_{\log D(\text{real})} ] + \mathbb{E}_{\mathbf{z} \sim p_\mathbf{z}} [ \underbrace{\mathbb{E}_{\mathbf{x} \sim p_G(.\vert\mathbf{z})}[\log 1 - D(\mathbf{x}, \mathbf{z})]}_{\log(1- D(\text{fake}))}) ]
$$

![BiGAN](https://lilianweng.github.io/posts/2019-11-10-self-supervised/bi-GAN.png)

*图 10：双向 GAN 工作原理示意图。（图片来源：[Donahue, et al, 2017](https://arxiv.org/abs/1605.09782)）*

### 对比学习
<mark><b>对比预测编码（Contrastive Predictive Coding，CPC）</b></mark>（[van den Oord, et al. 2018](https://arxiv.org/abs/1807.03748)）是一种从高维数据做无监督学习的方法：把生成建模问题转化为分类问题。CPC 中的*对比损失（contrastive loss）*或 *InfoNCE 损失*受[噪声对比估计（NCE）](https://lilianweng.github.io/posts/2017-10-15-word-embedding/#noise-contrastive-estimation-nce)启发，用交叉熵损失度量模型在一组无关"负"样本中把"未来"表示分类出来的能力。这样的设计部分因为：像 MSE 这样的单峰损失容量不足，而学习完整生成模型又太昂贵。

![CPC on audio input](https://lilianweng.github.io/posts/2019-11-10-self-supervised/CPC-audio.png)

*图 11：在音频输入上应用对比预测编码的示意图。（图片来源：[van den Oord, et al. 2018](https://arxiv.org/abs/1807.03748)）*

CPC 用编码器压缩输入数据 $$z_t = g_\text{enc}(x_t)$$，用*自回归*解码器学习可能被未来预测共享的高层上下文 $$c_t = g_\text{ar}(z_{\leq t})$$。端到端训练依赖 NCE 启发的对比损失。

预测未来信息时，CPC 被优化以最大化输入 $$x$$ 与上下文向量 $$c$$ 之间的互信息：

$$
I(x; c) = \sum_{x, c} p(x, c) \log\frac{p(x, c)}{p(x)p(c)} = \sum_{x, c} p(x, c)\log\frac{p(x|c)}{p(x)}
$$

CPC 不直接建模未来观测 $$p_k(x_{t+k} \vert c_t)$$（可能相当昂贵），而是建模一个保持 $$x_{t+k}$$ 与 $$c_t$$ 之间互信息的密度函数：

$$
f_k(x_{t+k}, c_t) = \exp(z_{t+k}^\top W_k c_t) \propto \frac{p(x_{t+k}|c_t)}{p(x_{t+k})}
$$

其中 $$f_k$$ 可以未归一化，线性变换 $$W_k^\top c_t$$ 用于预测，每一步 $$k$$ 用不同的 $$W_k$$ 矩阵。

给定一组 $$N$$ 个随机样本 $$X = \{x_1, \dots, x_N\}$$，只含一个正样本 $$x_t \sim p(x_{t+k} \vert c_t)$$ 和 $$N-1$$ 个负样本 $$x_{i \neq t} \sim p(x_{t+k})$$，正确分类正样本（$$\frac{f_k}{\sum f_k}$$ 为预测）的交叉熵损失为：

$$
\mathcal{L}_N = - \mathbb{E}_X \Big[\log \frac{f_k(x_{t+k}, c_t)}{\sum_{i=1}^N f_k (x_i, c_t)}\Big]
$$

![CPC on images](https://lilianweng.github.io/posts/2019-11-10-self-supervised/CPC-image.png)

*图 12：在图像上应用对比预测编码的示意图。（图片来源：[van den Oord, et al. 2018](https://arxiv.org/abs/1807.03748)）*

在图像上使用 CPC 时（[Henaff, et al. 2019](https://arxiv.org/abs/1905.09272)），预测器网络应只能访问被掩码的特征集以避免平凡预测。确切地说：
1. 每张输入图像被分成一组重叠的块，每块由 resnet 编码器编码，得到压缩特征向量 $$z_{i,j}$$。
2. 一个掩码卷积网络带掩码做预测，使给定输出神经元的感受野只能看到图像中位于其上方的内容。否则预测问题就平凡了。预测可以双向进行（自上而下与自下而上）。
3. 从上下文 $$c_{i,j}$$ 预测 $$z_{i+k, j}$$：$$\hat{z}_{i+k, j} = W_k c_{i,j}$$。

对比损失量化这一预测，目标是在从同一图像其他块和同批次其他图像采样的负表示集 $$\{z_l\}$$ 中正确识别目标：

$$
\mathcal{L}_\text{CPC} 
= -\sum_{i,j,k} \log p(z_{i+k, j} \vert \hat{z}_{i+k, j}, \{z_l\}) 
= -\sum_{i,j,k} \log \frac{\exp(\hat{z}_{i+k, j}^\top z_{i+k, j})}{\exp(\hat{z}_{i+k, j}^\top z_{i+k, j}) + \sum_l \exp(\hat{z}_{i+k, j}^\top z_l)}
$$

更多对比学习内容请看["对比表征学习"](https://lilianweng.github.io/posts/2021-05-31-contrastive/)一文。

## 基于视频

视频包含一列语义相关的帧。相邻帧在时间上接近、比远处帧更相关。帧的顺序描述了某些推理规则和物理逻辑；如物体运动应当平滑、重力指向下方。

常见工作流是：在无标注视频上用一个或多个前置任务训练模型，然后把该模型某个中间特征层喂给下游任务（动作分类、分割或目标跟踪）微调一个简单模型。

### 跟踪

物体的运动由一列视频帧追踪。相邻帧中同一物体在画面上的差异通常不大，一般由物体或相机的小幅运动引起。因此，为相邻帧中同一物体学到的任何视觉表示在潜在特征空间中都应相近。受此启发，[Wang & Gupta, 2015](https://arxiv.org/abs/1505.00687) 提出通过在视频中<mark><b>跟踪运动物体</b></mark>来无监督学习视觉表示。

确切地说，在小时间窗（如 30 帧）内追踪有运动的块。选出第一个块 $$\mathbf{x}$$ 和最后一个块 $$\mathbf{x}^+$$ 用作训练数据点。若直接训练模型最小化两个块特征向量的差异，模型可能只学会把一切映射到相同值。为避免这种平凡解，与[上文](#counting-feature-loss)相同，加入随机第三个块 $$\mathbf{x}^-$$。模型通过强制两个被跟踪块之间的距离小于第一个块与随机块之间的距离来学习表示，$$D(\mathbf{x}, \mathbf{x}^-)) > D(\mathbf{x}, \mathbf{x}^+)$$，其中 $$D(.)$$ 是余弦距离，

$$
D(\mathbf{x}_1, \mathbf{x}_2) = 1 - \frac{f(\mathbf{x}_1) f(\mathbf{x}_2)}{\|f(\mathbf{x}_1)\| \|f(\mathbf{x}_2\|)}
$$

损失函数为：

$$
\mathcal{L}(\mathbf{x}, \mathbf{x}^+, \mathbf{x}^-) 
= \max\big(0, D(\mathbf{x}, \mathbf{x}^+) - D(\mathbf{x}, \mathbf{x}^-) + M\big) + \text{weight decay regularization term}
$$

其中 $$M$$ 是控制两个距离最小间隔的标量常数；论文中 $$M=0.5$$。最优情形下该损失强制 $$D(\mathbf{x}, \mathbf{x}^-) >= D(\mathbf{x}, \mathbf{x}^+) + M$$。

<a href="#triplet-loss" />这种形式的损失函数在人脸识别任务中也称为[三元组损失（triplet loss）](https://arxiv.org/abs/1503.03832)，其数据集包含多人在多个相机角度下的图像。设 $$\mathbf{x}^a$$ 为某个特定人的锚图像，$$\mathbf{x}^p$$ 为同一人另一角度的正图像，$$\mathbf{x}^n$$ 为不同人的负图像。在嵌入空间中，$$\mathbf{x}^a$$ 应比 $$\mathbf{x}^n$$ 更靠近 $$\mathbf{x}^p$$：

$$
\mathcal{L}_\text{triplet}(\mathbf{x}^a, \mathbf{x}^p, \mathbf{x}^n) = \max(0, \|\phi(\mathbf{x}^a) - \phi(\mathbf{x}^p) \|_2^2 -  \|\phi(\mathbf{x}^a) - \phi(\mathbf{x}^n) \|_2^2 + M)
$$

<a href="#n-pair-loss" />三元组损失的一个略微不同的形式称为 [n-pair 损失](https://papers.nips.cc/paper/6200-improved-deep-metric-learning-with-multi-class-n-pair-loss-objective)，也常用于机器人任务中学习观测嵌入。更多相关内容见[后面小节](#multi-view-metric-learning)。

![tracking videos](https://lilianweng.github.io/posts/2019-11-10-self-supervised/tracking-videos.png)

*图 13：通过在视频中跟踪物体学习表示的概览。(a) 在短轨迹中识别运动块；(b) 把两个相关块和一个随机块喂入共享权重的卷积网络；(c) 损失函数强制相关块之间的距离小于随机块之间的距离。（图片来源：[Wang & Gupta, 2015](https://arxiv.org/abs/1505.00687)）*

相关块通过两步无监督[光流](https://en.wikipedia.org/wiki/Optical_flow)方法跟踪与提取：
1. 获取 [SURF](https://www.vision.ee.ethz.ch/~surf/eccv06.pdf) 兴趣点，用 [IDT](https://hal.inria.fr/hal-00873267v2/document) 获取每个 SURF 点的运动。
2. 给定 SURF 兴趣点的轨迹，把光流幅值超过 0.5 像素的点分类为运动点。

训练时，给定一对相关块 $$\mathbf{x}$$ 和 $$\mathbf{x}^+$$，在同批次采样 $$K$$ 个随机块 $$\{\mathbf{x}^-\}$$ 组成 $$K$$ 个训练三元组。若干轮后应用*难负例挖掘*使训练更难更高效，即搜索使损失最大化的随机块并用它们做梯度更新。

### 帧序列

视频帧天然按时间顺序排列。研究者提出了若干自监督任务，动机是好的表示应能学到帧的*正确顺序*。

一个想法是<mark><b>验证帧顺序</b></mark>（[Misra, et al 2016](https://arxiv.org/abs/1603.08561)）。前置任务是判断视频中一列帧是否按正确的时间顺序放置（"temporal valid"）。模型需要跟踪并推理物体跨帧的小幅运动才能完成该任务。

训练帧从高运动窗口采样。每次采样 5 帧 $$(f_a, f_b, f_c, f_d, f_e)$$，时间戳有序 $$a < b < c < d < e$$。5 帧中构造一个正三元组 $$(f_b, f_c, f_d)$$ 和两个负三元组 $$(f_b, f_a, f_d)$$、$$(f_b, f_e, f_d)$$。参数 $$\tau_\max = \vert b-d \vert$$ 控制正训练实例的难度（越大越难），参数 $$\tau_\min = \min(\vert a-b \vert, \vert d-e \vert)$$ 控制负例难度（越小越难）。

视频帧顺序验证的前置任务被证明用作预训练步骤时能提升动作识别下游任务的性能。

![frame order validation](https://lilianweng.github.io/posts/2019-11-10-self-supervised/frame-order-validation.png)

*图 14：通过验证视频帧顺序学习表示的概览。(a) 数据采样过程；(b) 模型是三元组孪生网络，所有输入帧共享权重。（图片来源：[Misra, et al 2016](https://arxiv.org/abs/1603.08561)）*

*O3N*（Odd-One-Out Network；[Fernando et al. 2017](https://arxiv.org/abs/1611.06646)）的任务也基于视频帧序列验证。比上文更进一步，任务是从多个视频片段中<mark><b>挑出错误顺序的片段</b></mark>。

给定 $$N+1$$ 个输入视频片段，其中之一的帧被打乱（顺序错误），其余 $$N$$ 个保持正确时间顺序。O3N 学习预测"异类"视频片段的位置。他们的实验用 6 个输入片段，每段含 6 帧。

视频中的<mark><b>时间箭头（arrow of time）</b></mark>包含非常有信息量的内容，既关于低层物理（如重力把物体拉向地面；烟往上升；水往低处流），也关于高层事件推理（如鱼向前游；你可以打碎鸡蛋但不能复原）。于是另一个想法受此启发：通过预测时间箭头（AoT）——视频是正放还是倒放——来学习潜在表示（[Wei et al., 2018](https://www.robots.ox.ac.uk/~vgg/publications/2018/Wei18/wei18.pdf)）。

分类器应同时捕捉低层物理与高层语义才能预测时间箭头。所提出的 *T-CAM*（Temporal Class-Activation-Map）网络接受 $$T$$ 组输入，每组含若干帧光流。每组的卷积层输出被拼接并送入二元逻辑回归以预测时间箭头。

![Learning the arrow of time](https://lilianweng.github.io/posts/2019-11-10-self-supervised/learning-arrow-of-time.png)

*图 15：通过预测时间箭头学习表示的概览。(a) 多组帧序列的卷积特征被拼接；(b) 顶层含 3 个卷积层和平均池化。（图片来源：[Wei et al, 2018](https://www.robots.ox.ac.uk/~vgg/publications/2018/Wei18/wei18.pdf)）*

有趣的是，数据集中存在若干人工线索。若处理不当，它们会导向一个不依赖真实视频内容的平凡分类器：
- 由于视频压缩，黑边可能不是纯黑、可能含有时间顺序的信息。因此实验中应去除黑边。
- 大幅相机运动（如垂直平移或变焦）也为时间箭头提供强信号但与内容无关。处理阶段应稳定相机运动。

AoT 前置任务被证明用作预训练步骤时能提升动作分类下游任务的性能。注意仍需微调。

### 视频着色

[Vondrick et al. (2018)](https://arxiv.org/abs/1806.09594) 提出<mark><b>视频着色</b></mark>作为自监督学习问题，得到的丰富表示可用于视频分割和无人监督的视觉区域跟踪，*无须额外微调*。

与基于图像的[着色](#colorization)不同，这里的任务是利用颜色跨视频帧的天然时间连贯性（因此两帧在时间上不应相距太远），把颜色从彩色的正常参考帧复制到另一灰度目标帧。为一致地复制颜色，模型被设计为学会跟踪不同帧中相关的像素。

![Video colorization](https://lilianweng.github.io/posts/2019-11-10-self-supervised/video-colorization.png)

*图 16：把颜色从参考帧复制到灰度目标帧的视频着色。（图片来源：[Vondrick et al. 2018](https://arxiv.org/abs/1806.09594)）*

想法相当简单聪明。设 $$c_i$$ 为参考帧第 $$i-th$$ 个像素的真实颜色，$$c_j$$ 为目标帧第 $$j$$ 个像素的颜色。目标帧第 $$j$$ 个像素的预测颜色 $$\hat{c}_j$$ 是参考帧所有像素颜色的加权和，其中权重项度量相似度：

$$
\hat{c}_j = \sum_i A_{ij} c_i \text{ where } A_{ij} = \frac{\exp(f_i f_j)}{\sum_{i'} \exp(f_{i'} f_j)}
$$

其中 $$f$$ 是对应像素学到的嵌入；$$i’$$ 索引参考帧中的所有像素。权重项实现了一种基于注意力的指向机制，类似于[匹配网络](https://lilianweng.github.io/posts/2018-11-30-meta-learning/#matching-networks)和[指针网络](https://lilianweng.github.io/posts/2018-06-24-attention/#pointer-network)。由于完整相似度矩阵可能非常大，两帧都被降采样。$$c_j$$ 与 $$\hat{c}_j$$ 之间用量化颜色的分类交叉熵损失，如同 [Zhang et al. 2016](https://arxiv.org/abs/1603.08511)。

基于参考帧如何标记，模型可用于完成若干基于颜色的下游任务，如跟踪随时间的分割或人体姿态。无须微调。见图 15。

![Video colorization for tracking](https://lilianweng.github.io/posts/2019-11-10-self-supervised/video-colorization-examples.png)

*图 17：用视频着色随时间跟踪物体分割和人体姿态。（图片来源：[Vondrick et al. (2018)](https://arxiv.org/abs/1806.09594)）*

> 几点常见观察：
> - 组合多个前置任务提升性能；
> - 更深的网络提升表示质量；
> - 监督学习基线仍远胜它们所有。

## 基于控制

在真实世界运行 RL 策略（如基于视觉输入控制物理机器人）时，恰当跟踪状态、获得奖励信号或判断目标是否真正达成都不容易。视觉数据含大量与真实状态无关的噪声，因此状态的等价性无法从像素级比较推断。自监督表征学习在学习可直接用作控制策略输入的有用状态嵌入方面展现了巨大潜力。

本节讨论的所有案例都在机器人学习领域，主要是多相机视角的状态表示和目标表示。

### 多视角度量学习

度量学习的概念在[前文](#counting-feature-loss)[小节](#tracking)已多次提及。常见设定是：给定样本三元组（*锚* $$s_a$$、*正*样本 $$s_p$$、*负*样本 $$s_n$$），所学表示嵌入 $$\phi(s)$$ 满足 $$s_a$$ 在潜在空间中靠近 $$s_p$$ 而远离 $$s_n$$。

<a href="#grasp2vec" /><mark><b>Grasp2Vec</b></mark>（[Jang & Devin et al., 2018](https://arxiv.org/abs/1811.06964)）旨在从免费、无标注的抓取活动中为机器人抓取任务学习以物体为中心的视觉表示。所谓以物体为中心，指无论环境或机器人长什么样，若两张图像包含相似物品，就应映射到相似表示；否则嵌入应相距很远。

![Grasp2vec](https://lilianweng.github.io/posts/2019-11-10-self-supervised/grasp2vec.png)

*图 18：grasp2vec 如何学习以物体为中心的状态嵌入的概念图。（图片来源：[Jang & Devin et al., 2018](https://arxiv.org/abs/1811.06964)）*

抓取系统能判断它移动了一个物体，但说不出是哪个物体。架设相机拍摄整个场景和被抓物体的图像。早期训练中，执行抓取机器人随机抓取任意物体 $$o$$，产生图像三元组 $$(s_\text{pre}, s_\text{post}, o)$$：
- $$o$$ 是被抓举到相机前的物体图像；
- $$s_\text{pre}$$ 是*抓取前*的场景图像，托盘中有物体 $$o$$；
- $$s_\text{post}$$ 是同一场景*抓取后*的图像，托盘中没有物体 $$o$$。

要学习以物体为中心的表示，我们期望 $$s_\text{pre}$$ 与 $$s_\text{post}$$ 嵌入之差捕获被移除的物体 $$o$$。这个想法很有趣，类似于[词嵌入](https://lilianweng.github.io/posts/2017-10-15-word-embedding/)中观察到的关系，[例如](https://developers.google.com/machine-learning/crash-course/embeddings/translating-to-a-lower-dimensional-space) distance("king", "queen") ≈ distance("man", "woman")。

设 $$\phi_s$$ 和 $$\phi_o$$ 分别是场景和物体的嵌入函数。模型用 *n-pair 损失*最小化 $$\phi_s(s_\text{pre}) - \phi_s(s_\text{post})$$ 与 $$\phi_o(o)$$ 之间的距离来学习表示：

$$
\begin{aligned}
\mathcal{L}_\text{grasp2vec} &= \text{NPair}(\phi_s(s_\text{pre}) - \phi_s(s_\text{post}), \phi_o(o)) + \text{NPair}(\phi_o(o), \phi_s(s_\text{pre}) - \phi_s(s_\text{post})) \\
\text{where }\text{NPair}(a, p) &= \sum_{i<B} -\log\frac{\exp(a_i^\top p_j)}{\sum_{j<B, i\neq j}\exp(a_i^\top p_j)} + \lambda (\|a_i\|_2^2 + \|p_i\|_2^2)
\end{aligned}
$$

其中 $$B$$ 指一批（锚, 正）样本对。

把表示学习框定为度量学习时，[**n-pair 损失**](https://papers.nips.cc/paper/6200-improved-deep-metric-learning-with-multi-class-n-pair-loss-objective)是常见选择。与处理显式的（锚, 正, 负）三元组不同，n-pair 损失把一个 mini-batch 中跨对的所有其他正实例当作负例。

嵌入函数 $$\phi_o$$ 非常适合用图像呈现目标 $$g$$。量化实际抓到的物体 $$o$$ 与目标接近程度的奖励函数定义为 $$r = \phi_o(g) \cdot \phi_o(o)$$。注意计算奖励只依赖学到的潜在空间、不涉及真实位置，因此可用于真实机器人训练。

![Grasp2vec attention map](https://lilianweng.github.io/posts/2019-11-10-self-supervised/grasp2vec-attention-map.png)

*图 19：grasp2vec 嵌入的定位结果。在抓取前场景中定位目标物体的热图定义为 $$\phi_o(o)^\top \phi_{s, \text{spatial}} (s_\text{pre})$$，其中 $$\phi_{s, \text{spatial}}$$ 是最后一个 resnet 块经 ReLU 后的输出。第四列是失败案例，最后三列以真实图像为目标。（图片来源：[Jang & Devin et al., 2018](https://arxiv.org/abs/1811.06964)）*

除基于嵌入相似度的奖励函数外，grasp2vec 框架中训练 RL 策略还有几个技巧：
- *事后标注（Posthoc labeling）*：把随机抓到的物体标注为正确目标来增强数据集，类似 HER（Hindsight Experience Replay；[Andrychowicz, et al., 2017](https://papers.nips.cc/paper/7090-hindsight-experience-replay.pdf)）。
- *辅助目标增强*：用未达成目标重新标注转移来进一步增强回放缓冲区；确切地说，每次迭代采样两个目标 $$(g, g')$$，二者都用于向回放缓冲区添加新转移。

<a href="#tcn" />**TCN**（<mark><b>时间对比网络（Time-Contrastive Networks）</b></mark>；[Sermanet, et al. 2018](https://arxiv.org/abs/1704.06888)）从多相机视角视频学习，直觉是：同一场景同一时间步的不同视角应共享同一嵌入（如 [FaceNet](https://arxiv.org/abs/1503.03832)），而嵌入应随时间变化，即使是同一相机视角。因此嵌入捕捉的是底层状态的语义而非视觉相似性。TCN 嵌入用[三元组损失](#triplet-loss)训练。

训练数据通过同时从不同角度拍摄同一场景的视频收集。所有视频无标注。

![Time-contrastive network](https://lilianweng.github.io/posts/2019-11-10-self-supervised/TCN.png)

*图 20：时间对比方法学习状态嵌入的示意图。两个相机视角同一时间步选取的蓝色帧是锚样本与正样本，不同时间步的红色帧是负样本。*

TCN 嵌入提取对相机配置不变的视觉特征。它可以用于基于演示视频与观测在潜在空间中的欧氏距离，为模仿学习构建奖励函数。

对 TCN 的进一步改进是联合学习多帧而非单帧的嵌入，得到 **mfTCN**（<b><mark>多帧</mark>时间对比网络</b>；[Dwibedi et al., 2019](https://arxiv.org/abs/1808.00928)）。给定来自若干同步相机视角的一组视频 $$v_1, v_2, \dots, v_k$$，每段视频中时间 $$t$$ 的帧与按步幅 $$s$$ 选取的前 $$n-1$$ 帧被聚合并映射为一个嵌入向量，得到大小为 $(n−1) \times s + 1$ 的回看窗口。每帧先经过 CNN 提取低层特征，然后用 3D 时间卷积在时间上聚合帧。模型用 [n-pair 损失](#n-pair-loss)训练。

![mfTCN](https://lilianweng.github.io/posts/2019-11-10-self-supervised/mfTCN.png)

*图 21：训练 mfTCN 的采样过程。（图片来源：[Dwibedi et al., 2019](https://arxiv.org/abs/1808.00928)）*

训练数据按如下采样：
1. 首先构造两对视频片段。每对含来自不同相机视角但时间步同步的两个片段。这两组视频在时间上应相距很远。
2. 从每对中的每个视频片段以相同步幅同时采样固定数量的帧。
3. 相同时间步的帧在 n-pair 损失中作为正样本，跨对的帧为负样本。

mfTCN 嵌入能捕捉场景中物体的位置与速度（如倒立摆中），也可用作策略输入。

### 自主目标生成

**RIG**（<b>Reinforcement learning with <mark>Imagined Goals</mark></b>；[Nair et al., 2018](https://arxiv.org/abs/1807.04742)）描述了一种用无监督表示学习训练目标条件策略的方法。策略通过先想象"假"目标再尝试达成它们，从自监督练习中学习。

![RIG](https://lilianweng.github.io/posts/2019-11-10-self-supervised/RIG.png)

*图 22：RIG 的工作流程。（图片来源：[Nair et al., 2018](https://arxiv.org/abs/1807.04742)）*

任务是控制机械臂把桌上的小冰球推到期望位置。期望位置（即目标）以图像呈现。训练期间，它通过 $$\beta$$-VAE 编码器学习状态 $$s$$ 和目标 $$g$$ 的潜在嵌入，控制策略完全在潜在空间中运行。

设[$$\beta$$-VAE](https://lilianweng.github.io/posts/2018-08-12-vae/#beta-vae)有编码器 $$q_\phi$$ 把输入状态映射到由高斯分布建模的潜变量 $$z$$，解码器 $$p_\psi$$ 把 $$z$$ 映射回状态。RIG 的状态编码器设为 $$\beta$$-VAE 编码器的均值。

$$
\begin{aligned}
z &\sim q_\phi(z \vert s) = \mathcal{N}(z; \mu_\phi(s), \sigma^2_\phi(s)) \\
\mathcal{L}_{\beta\text{-VAE}} &= - \mathbb{E}_{z \sim q_\phi(z \vert s)} [\log p_\psi (s \vert z)] + \beta D_\text{KL}(q_\phi(z \vert s) \| p_\psi(s)) \\
e(s) &\triangleq \mu_\phi(s)
\end{aligned}
$$

奖励是状态与目标嵌入向量之间的欧氏距离：$$r(s, g) = -\|e(s) - e(g)\|$$。与 [grasp2vec](#grasp2vec) 类似，RIG 也用潜在目标重标注做数据增强：确切地说，一半目标从先验随机生成，另一半用 HER 选取。也和 grasp2vec 一样，奖励不依赖任何真实状态、只依赖学到的状态编码，因此可用于真实机器人训练。

![RIG algorithm](https://lilianweng.github.io/posts/2019-11-10-self-supervised/RIG-algorithm.png)

*图 23：RIG 的算法。（图片来源：[Nair et al., 2018](https://arxiv.org/abs/1807.04742)）*

RIG 的问题在于想象出的目标图像缺乏物体多样性。若 $$\beta$$-VAE 只用黑色冰球训练，它就无法创造含其他物体（如不同形状和颜色的积木）的目标。后续改进受 **CVAE**（Conditional VAE；[Sohn, Lee & Yan, 2015](https://papers.nips.cc/paper/5775-learning-structured-output-representation-using-deep-conditional-generative-models)）启发，用 **CC-VAE**（Context-Conditioned VAE；[Nair, et al., 2019](https://arxiv.org/abs/1910.11670)）替换 $\beta$-VAE 做目标生成。

![Context-conditional RIG](https://lilianweng.github.io/posts/2019-11-10-self-supervised/CC-RIG.png)

*图 24：上下文条件 RIG 的工作流程。（图片来源：[Nair, et al., 2019](https://arxiv.org/abs/1910.11670)）。*

CVAE 以上下文变量 $$c$$ 为条件。它训练编码器 $$q_\phi(z \vert s, c)$$ 和解码器 $$p_\psi (s \vert z, c)$$，注意二者都能访问 $$c$$。CVAE 损失惩罚信息经信息瓶颈从输入状态 $$s$$ 流过，但允许信息从 $$c$$ *不受限*地流向编码器与解码器。

$$
\mathcal{L}_\text{CVAE} = - \mathbb{E}_{z \sim q_\phi(z \vert s,c)} [\log p_\psi (s \vert z, c)] + \beta D_\text{KL}(q_\phi(z \vert s, c) \| p_\psi(s))
$$

为创造合理的目标，CC-VAE 以起始状态 $$s_0$$ 为条件，使生成的目标呈现与 $$s_0$$ 一致的物体类型。这种目标一致性是必要的；例如若当前场景有一个红色冰球而目标里是蓝色积木，会让策略困惑。

除状态编码器 $$e(s) \triangleq \mu_\phi(s)$$ 外，CC-VAE 训练第二个卷积编码器 $$e_0(.)$$ 把起始状态 $$s_0$$ 翻译成紧凑的上下文表示 $$c = e_0(s_0)$$。两个编码器 $$e(.)$$ 和 $$e_0(.)$$ 刻意不同、不共享权重，因为它们被期望编码图像变化的不同因子。除 CVAE 的损失函数外，CC-VAE 增加一个额外项学习把 $$c$$ 重建回 $$s_0$$，$$\hat{s}_0 = d_0(c)$$。

$$
\mathcal{L}_\text{CC-VAE} = \mathcal{L}_\text{CVAE} + \log p(s_0\vert c)
$$

![RIG goal samples](https://lilianweng.github.io/posts/2019-11-10-self-supervised/CC-RIG-goal-samples.png)

*图 25：CVAE 以上下文图像为条件生成的想象目标示例（第一行），而 VAE 未能捕捉物体一致性。（图片来源：[Nair, et al., 2019](https://arxiv.org/abs/1910.11670)）。*

### 双模拟

任务无关的表示（如打算表示系统中全部动力学的模型）可能干扰 RL 算法，因为无关信息也被呈现。例如，若只训练自编码器重建输入图像，无法保证整个学到的表示对 RL 有用。因此，若只想学习与控制相关的信息，就需要远离基于重建的表示学习——因为无关细节对重建仍然重要。

基于双模拟（bisimulation）的控制表示学习不依赖重建，而是旨在按状态在 MDP 中的行为相似性对状态分组。

**双模拟**（[Givan et al. 2003](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.61.2493&rep=rep1&type=pdf)）指两个具有相似长期行为的状态之间的等价关系。*双模拟度量（bisimulation metrics）*量化这一关系，使我们可以聚合状态、把高维状态空间压缩为更小的空间以更高效地计算。两个状态之间的*双模拟距离*对应这两个状态行为上的差异程度。

给定 [MDP](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#markov-decision-processes) $$\mathcal{M} = \langle \mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma \rangle$$ 和双模拟关系 $$B$$，在关系 $$B$$ 下相等的两个状态（即 $$s_i B s_j$$）应对所有动作有相同的即时奖励、对下一个双相似状态有相同的转移概率：

$$
\begin{aligned}
\mathcal{R}(s_i, a) &= \mathcal{R}(s_j, a) \; \forall a \in \mathcal{A} \\
\mathcal{P}(G \vert s_i, a) &= \mathcal{P}(G \vert s_j, a) \; \forall a \in \mathcal{A} \; \forall G \in \mathcal{S}_B
\end{aligned}
$$

其中 $$\mathcal{S}_B$$ 是状态空间在关系 $$B$$ 下的一个划分。

注意 $$=$$ 总是双模拟关系。最有趣的是极大双模拟关系 $$\sim$$，它定义了状态分组*最少*的划分 $$\mathcal{S}_\sim$$。

![DeepMDP](https://lilianweng.github.io/posts/2019-11-10-self-supervised/DeepMDP.png)

*图 26：DeepMDP 通过最小化奖励模型和动力学模型上的两个损失学习潜在空间模型。（图片来源：[Gelada, et al. 2019](https://arxiv.org/abs/1906.02736)）*

目标与双模拟度量相似，**DeepMDP**（[Gelada, et al. 2019](https://arxiv.org/abs/1906.02736)）简化 RL 任务中的高维观测，通过最小化两个损失学习潜在空间模型：
1. 奖励预测与
2. 下一潜在状态分布的预测。

$$
\begin{aligned}
\mathcal{L}_{\bar{\mathcal{R}}}(s, a) = \vert \mathcal{R}(s, a) - \bar{\mathcal{R}}(\phi(s), a) \vert \\
\mathcal{L}_{\bar{\mathcal{P}}}(s, a) = D(\phi \mathcal{P}(s, a), \bar{\mathcal{P}}(. \vert \phi(s), a))
\end{aligned}
$$

其中 $$\phi(s)$$ 是状态 $$s$$ 的嵌入；带横线的符号是同一 MDP 中但在低维潜在观测空间运行的函数（奖励函数 $$R$$ 与转移函数 $$P$$）。这里嵌入表示 $$\phi$$ 可与双模拟度量联系起来，因为双模拟距离被证明上界受潜在空间中的 L2 距离约束。

函数 $$D$$ 量化两个概率分布之间的距离，需谨慎选择。DeepMDP 聚焦 *Wasserstein-1* 度量（也称["推土机距离"](https://lilianweng.github.io/posts/2017-08-20-gan/#what-is-wasserstein-distance)）。度量空间 $$(M, d)$$（即 $$d: M \times M \to \mathbb{R}$$）上分布 $$P$$ 与 $$Q$$ 之间的 Wasserstein-1 距离为：

$$
W_d (P, Q) = \inf_{\lambda \in \Pi(P, Q)} \int_{M \times M} d(x, y) \lambda(x, y) \; \mathrm{d}x \mathrm{d}y
$$

其中 $$\Pi(P, Q)$$ 是 $$P$$ 与 $$Q$$ 所有[耦合](https://en.wikipedia.org/wiki/Coupling_(probability))的集合。$$d(x, y)$$ 定义把一个粒子从点 $$x$$ 移到点 $$y$$ 的代价。

根据 Monge-Kantorovich 对偶，Wasserstein 度量有对偶形式：

$$
W_d (P, Q) = \sup_{f \in \mathcal{F}_d} \vert \mathbb{E}_{x \sim P} f(x) - \mathbb{E}_{y \sim Q} f(y) \vert
$$

其中 $$\mathcal{F}_d$$ 是度量 $$d$$ 下 1-Lipschitz 函数的集合——$$\mathcal{F}_d = \{ f: \vert f(x) - f(y) \vert \leq d(x, y) \}$$。

DeepMDP 把模型推广到 Norm 最大均值差异（Norm-[MMD](https://en.wikipedia.org/wiki/Kernel_embedding_of_distributions#Measuring_distance_between_distributions)）度量，以改进其深度价值函数界的紧致性，同时节省计算（Wasserstein 计算昂贵）。实验中他们发现转移预测模型的架构对性能影响很大。在训练无模型 RL 智能体时把这些 DeepMDP 损失加为辅助损失，在多数 Atari 游戏上带来良好改进。

**Deep Bisimulation for Control**（简称 **DBC**；[Zhang et al. 2020](https://arxiv.org/abs/2006.10742)）学习对 RL 任务控制有用的观测潜在表示，无须领域知识或像素级重建。

![DBC algorithm](https://lilianweng.github.io/posts/2019-11-10-self-supervised/DBC-illustration.png)

*图 27：Deep Bisimulation for Control 算法通过学习奖励模型和动力学模型来学习双模拟度量表示。模型架构是孪生网络。（图片来源：[Zhang et al. 2020](https://arxiv.org/abs/2006.10742)）*

与 DeepMDP 类似，DBC 通过学习奖励模型和转移模型来建模动力学。两个模型都在潜在空间 $$\phi(s)$$ 中运行。嵌入 $$\phi$$ 的优化依赖 [Ferns, et al. 2004](https://arxiv.org/abs/1207.4114)（定理 4.5）和 [Ferns, et al 2011](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.295.2114&rep=rep1&type=pdf)（定理 2.6）的一个重要结论：

> 给定 $$c \in (0, 1)$$ 为折扣因子、$$\pi$$ 为持续被改进的策略、$$M$$ 为状态空间 $$\mathcal{S}$$ 上有界[伪度量](https://mathworld.wolfram.com/Pseudometric.html)的空间，可定义 $$\mathcal{F}: M \mapsto M$$：
>
> $$
> \mathcal{F}(d; \pi)(s_i, s_j) = (1-c) \vert \mathcal{R}_{s_i}^\pi - \mathcal{R}_{s_j}^\pi \vert + c W_d (\mathcal{P}_{s_i}^\pi, \mathcal{P}_{s_j}^\pi)
> $$
>
> 则 $$\mathcal{F}$$ 有唯一不动点 $$\tilde{d}$$，它是一个 $$\pi^*$$-双模拟度量，且 $$\tilde{d}(s_i, s_j) = 0 \iff s_i \sim s_j$$。

[证明并不平凡。我以后可能加也可能不加 \_(:3」∠)\_ ……]

给定一批观测对，$$\phi$$ 的训练损失 $$J(\phi)$$ 最小化同策略双模拟度量与潜在空间欧氏距离之间的均方误差：

$$
J(\phi) = \Big( \|\phi(s_i) - \phi(s_j)\|_1 - \vert \hat{\mathcal{R}}(\bar{\phi}(s_i)) - \hat{\mathcal{R}}(\bar{\phi}(s_j)) \vert - \gamma W_2(\hat{\mathcal{P}}(\cdot \vert \bar{\phi}(s_i), \bar{\pi}(\bar{\phi}(s_i))), \hat{\mathcal{P}}(\cdot \vert \bar{\phi}(s_j), \bar{\pi}(\bar{\phi}(s_j)))) \Big)^2
$$

其中 $$\bar{\phi}(s)$$ 表示带停止梯度的 $$\phi(s)$$，$$\bar{\pi}$$ 是策略输出的均值。学到的奖励模型 $$\hat{\mathcal{R}}$$ 是确定性的，学到的前向动力学模型 $$\hat{\mathcal{P}}$$ 输出高斯分布。

DBC 基于 SAC 但在潜在空间中运行：

![DBC algorithm](https://lilianweng.github.io/posts/2019-11-10-self-supervised/DBC-algorithm.png)

*图 28：Deep Bisimulation for Control 的算法。（图片来源：[Zhang et al. 2020](https://arxiv.org/abs/2006.10742)）*

---
引用格式：
```
@article{weng2019selfsup,
  title   = "Self-Supervised Representation Learning",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2019",
  url     = "https://lilianweng.github.io/lil-log/2019/11/10/self-supervised-learning.html"
}
```

## 参考文献

[1] Alexey Dosovitskiy, et al. ["Discriminative unsupervised feature learning with exemplar convolutional neural networks."](https://arxiv.org/abs/1406.6909) IEEE transactions on pattern analysis and machine intelligence 38.9 (2015): 1734-1747.

[2] Spyros Gidaris, Praveer Singh & Nikos Komodakis. ["Unsupervised Representation Learning by Predicting Image Rotations"](https://arxiv.org/abs/1803.07728) ICLR 2018.

[3] Carl Doersch, Abhinav Gupta, and Alexei A. Efros. ["Unsupervised visual representation learning by context prediction."](https://arxiv.org/abs/1505.05192) ICCV. 2015.

[4] Mehdi Noroozi & Paolo Favaro. ["Unsupervised learning of visual representations by solving jigsaw puzzles."](https://arxiv.org/abs/1603.09246) ECCV, 2016.

[5] Mehdi Noroozi, Hamed Pirsiavash, and Paolo Favaro. ["Representation learning by learning to count."](https://arxiv.org/abs/1708.06734) ICCV. 2017.

[6] Richard Zhang, Phillip Isola & Alexei A. Efros. ["Colorful image colorization."](https://arxiv.org/abs/1603.08511) ECCV, 2016.

[7] Pascal Vincent, et al. ["Extracting and composing robust features with denoising autoencoders."](https://www.cs.toronto.edu/~larocheh/publications/icml-2008-denoising-autoencoders.pdf) ICML, 2008.

[8] Jeff Donahue, Philipp Krähenbühl, and Trevor Darrell. ["Adversarial feature learning."](https://arxiv.org/abs/1605.09782) ICLR 2017.

[9] Deepak Pathak, et al. ["Context encoders: Feature learning by inpainting."](https://arxiv.org/abs/1604.07379) CVPR. 2016.

[10] Richard Zhang, Phillip Isola, and Alexei A. Efros. ["Split-brain autoencoders: Unsupervised learning by cross-channel prediction."](https://arxiv.org/abs/1611.09842) CVPR. 2017.

[11] Xiaolong Wang & Abhinav Gupta. ["Unsupervised Learning of Visual Representations using Videos."](https://arxiv.org/abs/1505.00687) ICCV. 2015.

[12] Carl Vondrick, et al. ["Tracking Emerges by Colorizing Videos"](https://arxiv.org/pdf/1806.09594.pdf) ECCV. 2018.

[13] Ishan Misra, C. Lawrence Zitnick, and Martial Hebert. ["Shuffle and learn: unsupervised learning using temporal order verification."](https://arxiv.org/abs/1603.08561) ECCV. 2016.

[14] Basura Fernando, et al. ["Self-Supervised Video Representation Learning With Odd-One-Out Networks"](https://arxiv.org/abs/1611.06646) CVPR. 2017.

[15] Donglai Wei, et al. ["Learning and Using the Arrow of Time"](https://www.robots.ox.ac.uk/~vgg/publications/2018/Wei18/wei18.pdf) CVPR. 2018.

[16] Florian Schroff, Dmitry Kalenichenko and James Philbin. ["FaceNet: A Unified Embedding for Face Recognition and Clustering"](https://arxiv.org/abs/1503.03832) CVPR.  2015.

[17] Pierre Sermanet, et al. ["Time-Contrastive Networks: Self-Supervised Learning from Video"](https://arxiv.org/abs/1704.06888) CVPR. 2018.

[18] Debidatta Dwibedi, et al. ["Learning actionable representations from visual observations."](https://arxiv.org/abs/1808.00928) IROS. 2018.

[19] Eric Jang & Coline Devin, et al. ["Grasp2Vec: Learning Object Representations from Self-Supervised Grasping"](https://arxiv.org/abs/1811.06964) CoRL. 2018.

[20] Ashvin Nair, et al. ["Visual reinforcement learning with imagined goals"](https://arxiv.org/abs/1807.04742) NeuriPS. 2018.

[21] Ashvin Nair, et al. ["Contextual imagined goals for self-supervised robotic learning"](https://arxiv.org/abs/1910.11670) CoRL. 2019.

[22] Aaron van den Oord, Yazhe Li & Oriol Vinyals. ["Representation Learning with Contrastive Predictive Coding"](https://arxiv.org/abs/1807.03748) arXiv preprint arXiv:1807.03748, 2018.

[23] Olivier J. Henaff, et al. ["Data-Efficient Image Recognition with Contrastive Predictive Coding"](https://arxiv.org/abs/1905.09272) arXiv preprint arXiv:1905.09272, 2019.

[24] Kaiming He, et al. ["Momentum Contrast for Unsupervised Visual Representation Learning."](https://arxiv.org/abs/1911.05722) CVPR 2020.

[25] Zhirong Wu, et al. ["Unsupervised Feature Learning via Non-Parametric Instance-level Discrimination."](https://arxiv.org/abs/1805.01978v1) CVPR 2018.

[26] Ting Chen, et al. ["A Simple Framework for Contrastive Learning of Visual Representations."]( https://arxiv.org/abs/2002.05709) arXiv preprint arXiv:2002.05709, 2020.

[27] Aravind Srinivas, Michael Laskin & Pieter Abbeel ["CURL: Contrastive Unsupervised Representations for Reinforcement Learning."](https://arxiv.org/abs/2004.04136) arXiv preprint arXiv:2004.04136, 2020.

[28] Carles Gelada, et al. ["DeepMDP: Learning Continuous Latent Space Models for Representation Learning"](https://arxiv.org/abs/1906.02736) ICML 2019.

[29] Amy Zhang, et al. ["Learning Invariant Representations for Reinforcement Learning without Reconstruction"](https://arxiv.org/abs/2006.10742) arXiv preprint arXiv:2006.10742, 2020.

[30] Xinlei Chen, et al. ["Improved Baselines with Momentum Contrastive Learning"](https://arxiv.org/abs/2003.04297) arXiv preprint arXiv:2003.04297, 2020.

[31] Jean-Bastien Grill, et al. ["Bootstrap Your Own Latent: A New Approach to Self-Supervised Learning"](https://arxiv.org/abs/2006.07733) arXiv preprint arXiv:2006.07733, 2020.

[32] Abe Fetterman & Josh Albrecht. ["Understanding self-supervised and contrastive learning with Bootstrap Your Own Latent (BYOL)"]( https://untitled-ai.github.io/understanding-self-supervised-contrastive-learning.html) Untitled blog. Aug 24, 2020.
