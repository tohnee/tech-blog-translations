---
title: "对比表征学习"
title_en: "Contrastive Representation Learning"
source: https://lilianweng.github.io/posts/2021-05-31-contrastive/
crawled: 2026-09-08
translated: 2026-09-08
---

# 对比表征学习

> 原文：[Contrastive Representation Learning](https://lilianweng.github.io/posts/2021-05-31-contrastive/) · Lilian Weng（翁荔）

> 对比学习（contrastive learning）的主要思想是学习这样的表征：相似的样本彼此靠近，不相似的样本相互远离。对比学习既可以应用于监督数据，也可以应用于无监督数据，并且已在多种视觉和语言任务上取得了良好性能。


对比表征学习（contrastive representation learning）的目标是学习一个这样的嵌入空间：相似的样本对彼此靠近，而不相似的样本对相互远离。对比学习既可以用于监督设置，也可以用于无监督设置。在处理无监督数据时，对比学习是[自监督学习](https://lilianweng.github.io/posts/2019-11-10-self-supervised/)中最强大的方法之一。





## 对比训练目标

在早期的对比学习损失函数版本中，只涉及一个正样本（positive sample）和一个负样本（negative sample）。近期训练目标的趋势是在一个批次中纳入多组正、负样本对。


### 对比损失

**对比损失（contrastive loss）**（[Chopra et al. 2005](http://yann.lecun.com/exdb/publis/pdf/chopra-05.pdf)）是最早以对比方式进行深度度量学习（deep metric learning）的训练目标之一。

给定一组输入样本 $$\{ \mathbf{x}_i \}$$，每个样本都有一个对应的标签 $$y_i \in \{1, \dots, L\}$$，类别总数为 $$L$$。我们希望学习一个函数 $$f_\theta(.): \mathcal{X}\to\mathbb{R}^d$$，将 $$x_i$$ 编码为一个嵌入向量，使得来自同一类别的样本拥有相似的嵌入，而来自不同类别的样本的嵌入差异很大。因此，对比损失接收一对输入 $$(x_i, x_j)$$：当二者来自同一类别时最小化嵌入距离，否则最大化该距离。

$$
\mathcal{L}_\text{cont}(\mathbf{x}_i, \mathbf{x}_j, \theta) = \mathbb{1}[y_i=y_j] \| f_\theta(\mathbf{x}_i) - f_\theta(\mathbf{x}_j) \|^2_2 + \mathbb{1}[y_i\neq y_j]\max(0, \epsilon - \|f_\theta(\mathbf{x}_i) - f_\theta(\mathbf{x}_j)\|_2)^2
$$


其中 $$\epsilon$$ 是一个超参数，定义了不同类别样本之间距离的下界。



### 三元组损失

**三元组损失（triplet loss）** 最初在 FaceNet（[Schroff et al. 2015](https://arxiv.org/abs/1503.03832)）论文中提出，用于学习识别不同姿态、不同角度下的同一个人。


![Triplet loss](https://lilianweng.github.io/posts/2021-05-31-contrastive/triplet-loss.png)

图 1. 每个锚点配一个正样本和一个负样本时的三元组损失示意图。（图片来源：[Schroff et al. 2015](https://arxiv.org/abs/1503.03832)）



给定一个锚点（anchor）输入 $$\mathbf{x}$$，我们选取一个正样本 $$\mathbf{x}^+$$ 和一个负样本 $$\mathbf{x}^-$$，也就是说 $$\mathbf{x}^+$$ 与 $$\mathbf{x}$$ 属于同一类别，而 $$\mathbf{x}^-$$ 采样自另一个不同的类别。三元组损失学习同时最小化锚点 $$\mathbf{x}$$ 与正样本 $$\mathbf{x}^+$$ 之间的距离，并最大化锚点 $$\mathbf{x}$$ 与负样本 $$\mathbf{x}^-$$ 之间的距离，公式如下：

$$
\mathcal{L}_\text{triplet}(\mathbf{x}, \mathbf{x}^+, \mathbf{x}^-) = \sum_{\mathbf{x} \in \mathcal{X}} \max\big( 0, \|f(\mathbf{x}) - f(\mathbf{x}^+)\|^2_2 - \|f(\mathbf{x}) - f(\mathbf{x}^-)\|^2_2 + \epsilon \big)
$$

其中间隔参数 $$\epsilon$$ 被设置为相似对与不相似对距离之间的最小偏移量。

挑选有难度的 $$\mathbf{x}^-$$ 对于真正提升模型至关重要。


### 提升结构损失（Lifted Structured Loss）

**提升结构损失（Lifted Structured Loss）**（[Song et al. 2015](https://arxiv.org/abs/1511.06452)）利用一个训练批次内的所有成对边，以获得更好的计算效率。

![Lifted structured loss](https://lilianweng.github.io/posts/2021-05-31-contrastive/lifted-structured-loss.png)

图 2. 对比损失、三元组损失与提升结构损失的对比示意图。红色和蓝色的边分别连接相似与不相似的样本对。（图片来源：[Song et al. 2015](https://arxiv.org/abs/1511.06452)）



令 $$D_{ij} = \| f(\mathbf{x}_i) - f(\mathbf{x}_j) \|_2$$，结构化损失函数定义如下：

$$
\begin{aligned}
\mathcal{L}_\text{struct} &= \frac{1}{2\vert \mathcal{P} \vert} \sum_{(i,j) \in \mathcal{P}} \max(0, \mathcal{L}_\text{struct}^{(ij)})^2 \\
\text{where } \mathcal{L}_\text{struct}^{(ij)} &= D_{ij} + \color{red}{\max \big( \max_{(i,k)\in \mathcal{N}} \epsilon - D_{ik}, \max_{(j,l)\in \mathcal{N}} \epsilon - D_{jl} \big)}
\end{aligned}
$$

其中 $$\mathcal{P}$$ 包含正样本对的集合，$$\mathcal{N}$$ 是负样本对的集合。注意，稠密的成对平方距离矩阵可以在每个训练批次内轻松计算出来。

$$\mathcal{L}_\text{struct}^{(ij)}$$ 中<span color='red'>红色</span>的部分用于挖掘难负样本（hard negative）。然而，它并不平滑，实践中可能导致收敛到糟糕的局部最优。因此，将其松弛为：

$$
\mathcal{L}_\text{struct}^{(ij)} = D_{ij} + \log \Big( \sum_{(i,k)\in\mathcal{N}} \exp(\epsilon - D_{ik}) + \sum_{(j,l)\in\mathcal{N}} \exp(\epsilon - D_{jl}) \Big)
$$

论文中还提出，在给定若干随机正样本对的情况下，通过主动引入困难负样本来提升每个批次中负样本的质量。


### N-pair 损失

**多类 N-pair 损失（Multi-Class N-pair loss）**（[Sohn 2016](https://papers.nips.cc/paper/2016/hash/6b180037abbebea991d8b1232f8a8ca9-Abstract.html)）将三元组损失泛化为与多个负样本进行比较。

给定一个 $$(N + 1)$$ 元组的训练样本 $$\{ \mathbf{x}, \mathbf{x}^+, \mathbf{x}^-_1, \dots, \mathbf{x}^-_{N-1} \}$$，其中包含一个正样本和 $$N-1$$ 个负样本，N-pair 损失定义如下：

$$
\begin{aligned}
\mathcal{L}_\text{N-pair}(\mathbf{x}, \mathbf{x}^+, \{\mathbf{x}^-_i\}^{N-1}_{i=1}) 
&= \log\big(1 + \sum_{i=1}^{N-1} \exp(f(\mathbf{x})^\top f(\mathbf{x}^-_i) - f(\mathbf{x})^\top f(\mathbf{x}^+))\big) \\
&= -\log\frac{\exp(f(\mathbf{x})^\top f(\mathbf{x}^+))}{\exp(f(\mathbf{x})^\top f(\mathbf{x}^+)) + \sum_{i=1}^{N-1} \exp(f(\mathbf{x})^\top f(\mathbf{x}^-_i))}
\end{aligned}
$$

如果每个类别只采样一个负样本，它就等价于多分类的 softmax 损失。


### NCE

**噪声对比估计（Noise Contrastive Estimation）**，简称 **NCE**，是一种估计统计模型参数的方法，由 [Gutmann & Hyvarinen](http://proceedings.mlr.press/v9/gutmann10a.html) 于 2010 年提出。其思想是通过运行逻辑回归来把目标数据与噪声区分开。关于 NCE 如何用于学习词嵌入，可以在[这里](https://lilianweng.github.io/posts/2017-10-15-word-embedding/#noise-contrastive-estimation-nce)阅读更多内容。

令 $$\mathbf{x}$$ 为目标样本 $$\sim P(\mathbf{x} \vert C=1; \theta) = p_\theta(\mathbf{x})$$，$$\tilde{\mathbf{x}}$$ 为噪声样本 $$\sim  P(\tilde{\mathbf{x}} \vert C=0) = q(\tilde{\mathbf{x}})$$。注意，逻辑回归建模的是 logit（即对数几率），而在本例中，我们想建模的是来自目标数据分布（而非噪声分布）的样本 $$u$$ 的 logit：

$$
\ell_\theta(\mathbf{u}) = \log \frac{p_\theta(\mathbf{u})}{q(\mathbf{u})} = \log p_\theta(\mathbf{u}) - \log q(\mathbf{u})
$$

用 sigmoid $$\sigma(.)$$ 把 logit 转换成概率之后，我们就可以应用交叉熵损失：

$$
\begin{aligned}
\mathcal{L}_\text{NCE} &= - \frac{1}{N} \sum_{i=1}^N \big[ \log \sigma (\ell_\theta(\mathbf{x}_i)) + \log (1 - \sigma (\ell_\theta(\tilde{\mathbf{x}}_i))) \big] \\
\text{ where }\sigma(\ell) &= \frac{1}{1 + \exp(-\ell)} = \frac{p_\theta}{p_\theta + q}
\end{aligned}
$$

这里我列出的是 NCE 损失的原始形式，它只处理一个正样本和一个噪声样本。在许多后续工作中，纳入多个负样本的对比损失也被广泛地称为 NCE。


### InfoNCE

CPC（[对比预测编码](https://lilianweng.github.io/posts/2019-11-10-self-supervised/#contrastive-predictive-coding)；[van den Oord, et al. 2018](https://arxiv.org/abs/1807.03748)）中的 **InfoNCE 损失**受 [NCE](#NCE) 启发，使用类别交叉熵损失从一组互不相关的噪声样本中识别出正样本。

给定一个上下文向量 $$\mathbf{c}$$，正样本应从条件分布 $$p(\mathbf{x} \vert \mathbf{c})$$ 中抽取，而 $$N-1$$ 个负样本则从提议分布 $$p(\mathbf{x})$$ 中抽取，且与上下文 $$\mathbf{c}$$ 相互独立。为简洁起见，我们把所有样本记为 $$X=\{ \mathbf{x}_i \}^N_{i=1}$$，其中只有 $$\mathbf{x}_\texttt{pos}$$ 一个是正样本。我们正确检测出正样本的概率为：

$$
p(C=\texttt{pos} \vert X, \mathbf{c}) 
= \frac{p(x_\texttt{pos} \vert \mathbf{c}) \prod_{i=1,\dots,N; i \neq \texttt{pos}} p(\mathbf{x}_i)}{\sum_{j=1}^N \big[ p(\mathbf{x}_j \vert \mathbf{c}) \prod_{i=1,\dots,N; i \neq j} p(\mathbf{x}_i) \big]}
= \frac{ \frac{p(\mathbf{x}_\texttt{pos}\vert c)}{p(\mathbf{x}_\texttt{pos})} }{ \sum_{j=1}^N \frac{p(\mathbf{x}_j\vert \mathbf{c})}{p(\mathbf{x}_j)} }
= \frac{f(\mathbf{x}_\texttt{pos}, \mathbf{c})}{ \sum_{j=1}^N f(\mathbf{x}_j, \mathbf{c}) }
$$

其中打分函数为 $$f(\mathbf{x}, \mathbf{c}) \propto \frac{p(\mathbf{x}\vert\mathbf{c})}{p(\mathbf{x})}$$。

InfoNCE 损失优化的是将正样本正确分类的负对数概率：

$$
\mathcal{L}_\text{InfoNCE} = - \mathbb{E} \Big[\log \frac{f(\mathbf{x}, \mathbf{c})}{\sum_{\mathbf{x}' \in X} f(\mathbf{x}', \mathbf{c})} \Big]
$$

$$f(x, c)$$ 估计密度比 $$\frac{p(x\vert c)}{p(x)}$$ 这一事实，与互信息（mutual information）优化存在关联。为了最大化输入 $$x$$ 与上下文向量 $$c$$ 之间的互信息，我们有：

$$
I(\mathbf{x}; \mathbf{c}) = \sum_{\mathbf{x}, \mathbf{c}} p(\mathbf{x}, \mathbf{c}) \log\frac{p(\mathbf{x}, \mathbf{c})}{p(\mathbf{x})p(\mathbf{c})} = \sum_{\mathbf{x}, \mathbf{c}} p(\mathbf{x}, \mathbf{c})\log\color{blue}{\frac{p(\mathbf{x}|\mathbf{c})}{p(\mathbf{x})}}
$$

其中<span color='blue'>蓝色</span>的对数项由 $$f$$ 来估计。

对于序列预测任务，CPC 并不直接建模未来的观测 $$p_k(\mathbf{x}_{t+k} \vert \mathbf{c}_t)$$（这可能相当昂贵），而是建模一个密度函数来保持 $$\mathbf{x}_{t+k}$$ 与 $$\mathbf{c}_t$$ 之间的互信息：

$$
f_k(\mathbf{x}_{t+k}, \mathbf{c}_t) = \exp(\mathbf{z}_{t+k}^\top \mathbf{W}_k \mathbf{c}_t) \propto \frac{p(\mathbf{x}_{t+k}\vert\mathbf{c}_t)}{p(\mathbf{x}_{t+k})}
$$

其中 $$\mathbf{z}_{t+k}$$ 是编码后的输入，$$\mathbf{W}_k$$ 是一个可训练的权重矩阵。


### 软最近邻损失（Soft-Nearest Neighbors Loss）

**软最近邻损失（Soft-Nearest Neighbors Loss）**（[Salakhutdinov & Hinton 2007](http://proceedings.mlr.press/v2/salakhutdinov07a.html)、[Frosst et al. 2019](https://arxiv.org/abs/1902.01889)）将其扩展为包含多个正样本。

给定一个批次的样本 $$\{\mathbf{x}_i, y_i)\}^B_{i=1}$$，其中 $$y_i$$ 是 $$\mathbf{x}_i$$ 的类别标签，再给定一个用于度量两个输入之间相似度的函数 $$f(.,.)$$，温度为 $$\tau$$ 的软最近邻损失定义如下：

$$
\mathcal{L}_\text{snn} = -\frac{1}{B}\sum_{i=1}^B \log \frac{\sum_{i\neq j, y_i = y_j, j=1,\dots,B} \exp(- f(\mathbf{x}_i, \mathbf{x}_j) / \tau)}{\sum_{i\neq k, k=1,\dots,B} \exp(- f(\mathbf{x}_i, \mathbf{x}_k) /\tau)}
$$

温度 $$\tau$$ 用于调节特征在表征空间中的集中程度。例如，在低温下，损失由小距离主导，相距很远的表征贡献甚微、几乎变得无关紧要。


### 通用设置

我们可以放宽软最近邻损失中「类别」和「标签」的定义，从而从无监督数据中构造正、负样本对，例如通过数据增强（data augmentation）来创建原始样本的噪声版本。

大多数最新研究遵循如下对比学习目标的定义，以便纳入多个正样本和负样本。按照（[Wang & Isola 2020](https://arxiv.org/abs/2005.10242)）中的设置，令 $$p_\texttt{data}(.)$$ 为 $$\mathbb{R}^n$$ 上的数据分布，$$p_\texttt{pos}(., .)$$ 为 $$\mathbb{R}^{n \times n}$$ 上正样本对的分布。这两个分布应满足：

- 对称性：$$\forall \mathbf{x}, \mathbf{x}^+, p_\texttt{pos}(\mathbf{x}, \mathbf{x}^+) = p_\texttt{pos}(\mathbf{x}^+, \mathbf{x})$$
- 边际匹配：$$\forall \mathbf{x}, \int p_\texttt{pos}(\mathbf{x}, \mathbf{x}^+) d\mathbf{x}^+ = p_\texttt{data}(\mathbf{x})$$

为了学习一个能输出 *L2 归一化特征向量* 的编码器 $$f(\mathbf{x})$$，对比学习目标为：

$$
\begin{aligned}
\mathcal{L}_\text{contrastive} 
&= \mathbb{E}_{(\mathbf{x},\mathbf{x}^+)\sim p_\texttt{pos}, \{\mathbf{x}^-_i\}^M_{i=1} \overset{\text{i.i.d}}{\sim} p_\texttt{data} } \Big[ -\log\frac{\exp(f(\mathbf{x})^\top f(\mathbf{x}^+) / \tau)}{ \exp(f(\mathbf{x})^\top f(\mathbf{x}^+) / \tau) + \sum_{i=1}^M \exp(f(\mathbf{x})^\top f(\mathbf{x}_i^-) / \tau)} \Big] & \\
&\approx \mathbb{E}_{(\mathbf{x},\mathbf{x}^+)\sim p_\texttt{pos}, \{\mathbf{x}^-_i\}^M_{i=1} \overset{\text{i.i.d}}{\sim} p_\texttt{data} }\Big[ - f(\mathbf{x})^\top f(\mathbf{x}^+) / \tau + \log\big(\sum_{i=1}^M \exp(f(\mathbf{x})^\top f(\mathbf{x}_i^-) / \tau)\big) \Big] & \scriptstyle{\text{; Assuming infinite negatives}} \\
&= -\frac{1}{\tau}\mathbb{E}_{(\mathbf{x},\mathbf{x}^+)\sim p_\texttt{pos}}f(\mathbf{x})^\top f(\mathbf{x}^+) + \mathbb{E}_{ \mathbf{x} \sim p_\texttt{data}} \Big[ \log \mathbb{E}_{\mathbf{x}^- \sim p_\texttt{data}} \big[ \sum_{i=1}^M \exp(f(\mathbf{x})^\top f(\mathbf{x}_i^-) / \tau)\big] \Big] &
\end{aligned}
$$


## 关键要素


### 大量数据增强

给定一个训练样本，需要借助数据增强技术来创建它自身的噪声版本，作为正样本送入损失函数。恰当的数据增强设置对于学习良好且可泛化的嵌入特征至关重要。它在不改变语义的前提下为样本引入非本质的变化，从而鼓励模型去学习表征中的本质部分。例如，[SimCLR](#simclr) 的实验表明，随机裁剪与随机颜色失真的组合，对于在图像视觉表征学习上取得良好性能至关重要。


### 大批次大小

训练时使用大的批次大小（batch size）是许多对比学习方法（例如 [SimCLR](#simclr)、[CLIP](#clip)）成功的另一个关键要素，在依赖批内负样本时尤其如此。只有批次足够大，损失函数才能覆盖足够多样的负样本集合，给模型足够的挑战，使其学习有意义的表征来区分不同样本。


### 难负样本挖掘

难负样本应与锚点样本具有不同的标签，但其嵌入特征与锚点嵌入非常接近。在监督数据集中可以访问真实标签时，很容易识别任务特定的难负样本。例如，在学习句子嵌入时，我们可以把 NLI 数据集中标注为「矛盾（contradiction）」的句对当作难负样本对（例如 [SimCSE](#dropout-and-cutoff)），或者使用 BM25 返回的、匹配关键词最多的那些错误候选作为难负样本（[DPR](https://lilianweng.github.io/posts/2020-10-29-odqa/#DPR)；[Karpukhin et al., 2020](https://arxiv.org/abs/2004.04906)）。

然而，当我们希望保持无监督时，难负样本挖掘就变得比较棘手。增大训练批次或[记忆库](#memory-bank)的规模会隐式地引入更多难负样本，但副作用是带来沉重的内存占用负担。

[Chuang et al. (2020)](https://arxiv.org/abs/2007.00224) 研究了对比学习中的采样偏差（sampling bias），并提出了去偏损失。在无监督设置下，由于不知道真实标签，我们可能会不小心采样到假负样本（false negative）。采样偏差可能导致显著的性能下降。

![Sampling bias](https://lilianweng.github.io/posts/2021-05-31-contrastive/contrastive-sampling-bias.png)

*图 3. 采样偏差指对比学习中的假负样本，可能导致很大的性能下降。（图片来源：[Chuang et al., 2020](https://arxiv.org/abs/2007.00224)）*



让我们假设锚点类别 $$c$$ 的概率是均匀的 $$\rho(c)=\eta^+$$，而观测到不同类别的概率为 $$\eta^- = 1-\eta^+$$。

- 观测到 $$\mathbf{x}$$ 的某个正样本的概率为 $$p^+_x(\mathbf{x}')=p(\mathbf{x}'\vert \mathbf{h}_{x'}=\mathbf{h}_x)$$；
- 得到 $$\mathbf{x}$$ 的某个负样本的概率为 $$p^-_x(\mathbf{x}')=p(\mathbf{x}'\vert \mathbf{h}_{x'}\neq\mathbf{h}_x)$$。

当我们采样 $$\mathbf{x}^-$$ 时，无法访问真实的 $$p^-_x(\mathbf{x}^-)$$，因此 $$\mathbf{x}^-$$ 可能采自（不希望出现的）锚点类别 $$c$$，概率为 $$\eta^+$$。实际的采样数据分布变为：


$$
p(\mathbf{x}') = \eta^+ p^+_x(\mathbf{x}') + \eta^- p_x^-(\mathbf{x}')
$$

因此，我们可以用 $$p^-_x(\mathbf{x}') = (p(\mathbf{x}') - \eta^+ p^+_x(\mathbf{x}'))/\eta^-$$ 来采样 $$\mathbf{x}^-$$，从而对损失去偏。有了 $$N$$ 个样本 $$\{\mathbf{u}_i\}^N_{i=1}$$（采自 $$p$$）和 $$M$$ 个样本 $$\{ \mathbf{v}_i \}_{i=1}^M$$（采自 $$p^+_x$$），我们就可以估计对比学习损失分母中第二项的期望 $$\mathbb{E}_{\mathbf{x}^-\sim p^-_x}[\exp(f(\mathbf{x})^\top f(\mathbf{x}^-))]$$：


$$
g(\mathbf{x}, \{\mathbf{u}_i\}^N_{i=1}, \{\mathbf{v}_i\}_{i=1}^M) = \max\Big\{ \frac{1}{\eta^-}\Big( \frac{1}{N}\sum_{i=1}^N \exp(f(\mathbf{x})^\top f(\mathbf{u}_i)) - \frac{\eta^+}{M}\sum_{i=1}^M \exp(f(\mathbf{x})^\top f(\mathbf{v}_i)) \Big), \exp(-1/\tau) \Big\}
$$

其中 $$\tau$$ 是温度，$$\exp(-1/\tau)$$ 是 $$\mathbb{E}_{\mathbf{x}^-\sim p^-_x}[\exp(f(\mathbf{x})^\top f(\mathbf{x}^-))]$$ 的理论下界。

最终的去偏对比损失形如：

$$
\mathcal{L}^{N,M}_\text{debias}(f) = \mathbb{E}_{\mathbf{x},\{\mathbf{u}_i\}^N_{i=1}\sim p;\;\mathbf{x}^+, \{\mathbf{v}_i\}_{i=1}^M\sim p^+} \Big[ -\log\frac{\exp(f(\mathbf{x})^\top f(\mathbf{x}^+)}{\exp(f(\mathbf{x})^\top f(\mathbf{x}^+) + N g(x,\{\mathbf{u}_i\}^N_{i=1}, \{\mathbf{v}_i\}_{i=1}^M)} \Big]
$$



![Debiased t-SNE vis](https://lilianweng.github.io/posts/2021-05-31-contrastive/contrastive-debias-t-SNE.png)

*图 4. 使用去偏对比学习学到的表征的 t-SNE 可视化。（图片来源：[Chuang et al., 2020](https://arxiv.org/abs/2007.00224)）*



沿用上述记号，[Robinson et al. (2021)](https://arxiv.org/abs/2010.04592) 修改了采样概率以瞄准难负样本：将概率 $$p^-_x(x')$$ 上调，使之与该样本和锚点样本的相似度成正比。新的采样概率 $$q_\beta(x^-)$$ 为：


$$
q_\beta(\mathbf{x}^-) \propto \exp(\beta f(\mathbf{x})^\top f(\mathbf{x}^-)) \cdot p(\mathbf{x}^-)
$$

其中 $$\beta$$ 是一个需要调节的超参数。

我们可以用重要性采样来估计分母中的第二项 $$\mathbb{E}_{\mathbf{x}^- \sim q_\beta} [\exp(f(\mathbf{x})^\top f(\mathbf{x}^-))]$$，其中两个配分函数 $$Z_\beta, Z^+_\beta$$ 都可以经验地估计。

$$
\begin{aligned}
\mathbb{E}_{\mathbf{u} \sim q_\beta} [\exp(f(\mathbf{x})^\top f(\mathbf{u}))] &= \mathbb{E}_{\mathbf{u} \sim p} [\frac{q_\beta}{p}\exp(f(\mathbf{x})^\top f(\mathbf{u}))] = \mathbb{E}_{\mathbf{u} \sim p} [\frac{1}{Z_\beta}\exp((\beta + 1)f(\mathbf{x})^\top f(\mathbf{u}))] \\
\mathbb{E}_{\mathbf{v} \sim q^+_\beta} [\exp(f(\mathbf{x})^\top f(\mathbf{v}))] &= \mathbb{E}_{\mathbf{v} \sim p^+} [\frac{q^+_\beta}{p}\exp(f(\mathbf{x})^\top f(\mathbf{v}))] = \mathbb{E}_{\mathbf{v} \sim p} [\frac{1}{Z^+_\beta}\exp((\beta + 1)f(\mathbf{x})^\top f(\mathbf{v}))]
\end{aligned}
$$


![Pseudo code](https://lilianweng.github.io/posts/2021-05-31-contrastive/contrastive-hard-negatives-code.png)

*图 5. 设 $$M=1$$ 时，计算 NCE 损失、去偏对比损失与难负样本目标的伪代码。（图片来源：[Robinson et al., 2021](https://arxiv.org/abs/2010.04592) ）*



## 视觉：图像嵌入

### 图像增强

视觉领域中大多数对比表征学习方法都依赖于一连串数据增强技术来创建样本的噪声版本。增强应显著改变图像的视觉外观，但保持语义不变。

#### 基础图像增强

在保留语义的前提下修改图像的方式有很多。我们可以使用以下任意一种增强，或多种操作的组合。

- 随机裁剪，然后缩放回原始尺寸。
- 随机颜色失真
- 随机高斯模糊
- 随机颜色抖动
- 随机水平翻转
- 随机灰度化
- 多裁剪增强（Multi-crop augmentation）：使用两个标准分辨率的裁剪，并额外采样一组只覆盖图像局部区域的低分辨率裁剪。使用低分辨率裁剪可以降低计算成本。（[SwAV](#swav)）
- 以及更多……


#### 增强策略

有许多框架专为学习好的数据增强策略（即多种变换的组合）而设计。下面列举几个常见的。

- [AutoAugment](https://lilianweng.github.io/posts/2019-05-05-domain-randomization/#AutoAugment)（[Cubuk, et al. 2018](https://arxiv.org/abs/1805.09501)）：受 [NAS](https://lilianweng.github.io/posts/2020-08-06-nas/) 启发，AutoAugment 将为图像分类学习最佳数据增强操作（如错切、旋转、反色等）的问题建模为一个强化学习问题，并寻找能在评估集上取得最高准确率的组合。
- RandAugment（[Cubuk et al., 2019](https://arxiv.org/abs/1909.13719)）：RandAugment 通过用单一幅度参数控制不同变换操作的强度，大幅缩小了 AutoAugment 的搜索空间。
- PBA（基于种群的增强，Population based augmentation；[Ho et al., 2019](https://arxiv.org/abs/1905.05393)）：PBA 将 PBT（[Jaderberg et al, 2017](https://arxiv.org/abs/1711.09846)）与 AutoAugment 相结合，使用进化算法并行训练一个种群的子模型，以进化出最佳的增强策略。
- UDA（无监督数据增强，Unsupervised Data Augmentation；[Xie et al., 2019](https://arxiv.org/abs/1904.12848)）：在一组候选增强策略中，UDA 选择能最小化「模型对未标注样本预测的分布」与「对其未标注增强版本预测的分布」之间 KL 散度的策略。


#### 图像混合

图像混合方法可以从现有数据点构造新的训练样本。
- Mixup（[Zhang et al., 2018](https://arxiv.org/abs/1710.09412)）：它进行全局层面的混合，将两张现有图像 $$I_1$$ 和 $$I_2$$ 逐像素加权组合：$$I_\text{mixup} \gets \alpha I_1 + (1-\alpha) I_2$$，其中 $$\alpha \in [0, 1]$$。
- Cutmix（[Yun et al., 2019](https://arxiv.org/abs/1905.04899)）：Cutmix 进行区域层面的混合，把一张图像的局部区域与另一张图像的其余部分组合起来生成新样本：$$I_\text{cutmix} \gets \mathbf{M}_b \odot I_1 + (1-\mathbf{M}_b) \odot I_2$$，其中 $$\mathbf{M}_b \in \{0, 1\}^I$$ 是二值掩码，$$\odot$$ 表示逐元素相乘。这等价于用另一张图像中的同一区域去填充 cutout（[DeVries & Taylor 2017](https://arxiv.org/abs/1708.04552)）区域。
- MoCHi（「Mixing of Contrastive Hard Negatives」，对比难负样本混合；[Kalantidis et al. 2020](https://arxiv.org/abs/2010.01028)）：给定一个查询 $$\mathbf{q}$$，MoCHi 维护一个包含 $$K$$ 个负特征的队列 $$Q=\{\mathbf{n}_1, \dots, \mathbf{n}_K \}$$，并按这些负特征与查询的相似度 $$\mathbf{q}^\top \mathbf{n}$$ 降序排序。队列中前 $$N$$ 项被认为是最难的负样本 $$Q^N$$。然后可以通过 $$\mathbf{h} = \tilde{\mathbf{h}} / \|\tilde{\mathbf{h}}\|$$ 生成合成的难样本，其中 $$\tilde{\mathbf{h}} = \alpha\mathbf{n}_i + (1-\alpha) \mathbf{n}_j$$，$$\alpha \in (0, 1)$$。还可以通过与查询特征混合来创建更难的样本：$$\mathbf{h}' = \tilde{\mathbf{h}'} / \|\tilde{\mathbf{h}'}\|_2$$，其中 $$\tilde{\mathbf{h}'} = \beta\mathbf{q} + (1-\beta) \mathbf{n}_j$$，$$\beta \in (0, 0.5)$$。


### 并行增强

这类方法为一张锚点图像产生两个噪声版本，目标是学到使这两个增强样本共享同一嵌入的表征。


#### SimCLR
**SimCLR**（[Chen et al, 2020](https://arxiv.org/abs/2002.05709)）提出了一个简单的视觉表征对比学习框架。它通过在潜空间中以对比损失最大化同一样本的不同增强视图之间的一致性，来学习视觉输入的表征。


![SimCLR](https://lilianweng.github.io/posts/2021-05-31-contrastive/SimCLR.png)

*图 6. 一个简单的视觉表征对比学习框架。（图片来源：[Chen et al, 2020](https://arxiv.org/abs/2002.05709)）*



1) 随机采样一个含 $$N$$ 个样本的小批量，并对每个样本施加两种不同的数据增强操作，最终共得到 $$2N$$ 个增强样本。

$$
\tilde{\mathbf{x}}_i = t(\mathbf{x}),\quad\tilde{\mathbf{x}}_j = t'(\mathbf{x}),\quad t, t' \sim \mathcal{T}
$$

其中两个独立的数据增强算子 $$t$$ 和 $$t'$$ 采样自同一个增强族 $$\mathcal{T}$$。数据增强包括随机裁剪、缩放加随机翻转、颜色失真以及高斯模糊。

2) 给定一个正样本对，其余 $$2(N-1)$$ 个数据点被视为负样本。表征由基础编码器 $$f(.)$$ 产生：

$$
\mathbf{h}_i = f(\tilde{\mathbf{x}}_i),\quad \mathbf{h}_j = f(\tilde{\mathbf{x}}_j)
$$

3) 对比学习损失用余弦相似度 $$\text{sim}(.,.)$$ 定义。注意，该损失作用在表征的额外投影层 $$g(.)$$ 上，而非直接作用在表征空间上。但只有表征 $$\mathbf{h}$$ 会用于下游任务。

$$
\begin{aligned}
\mathbf{z}_i &= g(\mathbf{h}_i),\quad
\mathbf{z}_j = g(\mathbf{h}_j) \\
\mathcal{L}_\text{SimCLR}^{(i,j)} &= - \log\frac{\exp(\text{sim}(\mathbf{z}_i, \mathbf{z}_j) / \tau)}{\sum_{k=1}^{2N} \mathbb{1}_{[k \neq i]} \exp(\text{sim}(\mathbf{z}_i, \mathbf{z}_k) / \tau)}
\end{aligned}
$$

其中 $$\mathbb{1}_{[k \neq i]}$$ 是指示函数：当 $$k\neq i$$ 时取 1，否则取 0。

SimCLR 需要很大的批次大小来纳入足够多的负样本，以取得良好的性能。


![SimCLR Algorithm](https://lilianweng.github.io/posts/2021-05-31-contrastive/SimCLR-algo.png)

*图 7. SimCLR 的算法。（图片来源：[Chen et al, 2020](https://arxiv.org/abs/2002.05709)）。*



#### Barlow Twins

**Barlow Twins**（[Zbontar et al. 2021](https://arxiv.org/abs/2103.03230)）将样本的两个失真版本送入同一个网络提取特征，并学习使这两组输出特征之间的*互相关矩阵（cross-correlation matrix）*接近单位矩阵。其目标是让一个样本不同失真版本的表征向量保持相似，同时最小化这些向量之间的冗余。


![Barlow twins](https://lilianweng.github.io/posts/2021-05-31-contrastive/barlow-twins.png)

*图 8. Barlow Twins 学习流程示意图。（图片来源：[Zbontar et al. 2021](https://arxiv.org/abs/2103.03230)）。*



令 $$\mathcal{C}$$ 为沿批次维度在两个相同网络的输出之间计算得到的互相关矩阵。$$\mathcal{C}$$ 是一个方阵，尺寸与特征网络的输出维度相同。矩阵中的每个元素 $$\mathcal{C}_{ij}$$ 是网络输出向量在索引 $$i, j$$ 的维度、批次索引 $$b$$ 上的余弦相似度，即 $$\mathbf{z}_{b,i}^A$$ 与 $$\mathbf{z}_{b,j}^B$$ 之间的余弦相似度，取值介于 -1（完全负相关）与 1（完全正相关）之间。

$$
\begin{aligned}
\mathcal{L}_\text{BT} &= \underbrace{\sum_i (1-\mathcal{C}_{ii})^2}_\text{invariance term} + \lambda \underbrace{\sum_i\sum_{i\neq j} \mathcal{C}_{ij}^2}_\text{redundancy reduction term} \\ \text{where } \mathcal{C}_{ij} &= \frac{\sum_b \mathbf{z}^A_{b,i} \mathbf{z}^B_{b,j}}{\sqrt{\sum_b (\mathbf{z}^A_{b,i})^2}\sqrt{\sum_b (\mathbf{z}^B_{b,j})^2}}
\end{aligned}
$$

Barlow Twins 可与自监督学习的 SOTA 方法相媲美。它天然地避免了平凡常数（即坍塌的表征），并且对不同的训练批次大小都很稳健。


![Barlow twins algo](https://lilianweng.github.io/posts/2021-05-31-contrastive/barlow-twins-algo.png)

*图 9. Barlow Twins 的 PyTorch 风格伪代码算法。（图片来源：[Zbontar et al. 2021](https://arxiv.org/abs/2103.03230)）。*



#### BYOL
与上述方法不同、且颇为有趣的是，**BYOL**（Bootstrap Your Own Latent，自举你自己的潜变量；[Grill, et al 2020](https://arxiv.org/abs/2006.07733)）声称*不使用负样本*也能取得新的 SOTA 结果。它依赖两个神经网络，分别称为*在线（online）网络*与*目标（target）网络*，二者相互作用、彼此学习。目标网络（参数为 $$\xi$$）与在线网络（参数为 $$\theta$$）架构相同，但其权重是在线网络权重的 Polyak 平均：$$\xi \leftarrow \tau \xi + (1-\tau) \theta$$。


其目标是学习可用于下游任务的表征 $$y$$。参数为 $$\theta$$ 的在线网络包含：
- 一个编码器 $$f_\theta$$；
- 一个投影器 $$g_\theta$$；
- 一个预测器 $$q_\theta$$。

目标网络具有相同的网络架构，但参数 $$\xi$$ 不同，它通过对 $$\theta$$ 做 Polyak 平均来更新：$$\xi \leftarrow \tau \xi + (1-\tau) \theta$$。


![BYOL](https://lilianweng.github.io/posts/2021-05-31-contrastive/BYOL.png)

*图 10. BYOL 的模型架构。训练结束后，我们只关心 $$f_\theta$$，用它来生成表征 $$y=f_\theta(x)$$，其余部分都会被丢弃。$$\text{sg}$$ 表示停止梯度（stop gradient）。（图片来源：[Grill, et al 2020](https://arxiv.org/abs/2006.07733)）*



给定一张图像 $$\mathbf{x}$$，BYOL 损失按如下方式构造：
- 创建两个增强视图：$$\mathbf{v}=t(\mathbf{x}); \mathbf{v}'=t'(\mathbf{x})$$，增强算子采样自 $$t \sim \mathcal{T}, t' \sim \mathcal{T}'$$；
- 然后将它们编码为表征：$$\mathbf{y}_\theta=f_\theta(\mathbf{v}), \mathbf{y}'=f_\xi(\mathbf{v}')$$；
- 再将它们投影为潜变量：$$\mathbf{z}_\theta=g_\theta(\mathbf{y}_\theta), \mathbf{z}'=g_\xi(\mathbf{y}')$$；
- 在线网络输出一个预测 $$q_\theta(\mathbf{z}_\theta)$$；
- 将 $$q_\theta(\mathbf{z}_\theta)$$ 和 $$\mathbf{z}'$$ 都做 L2 归一化，得到 $$\bar{q}_\theta(\mathbf{z}_\theta) = q_\theta(\mathbf{z}_\theta) / \| q_\theta(\mathbf{z}_\theta) \|$$ 和 $$\bar{\mathbf{z}'} = \mathbf{z}' / \|\mathbf{z}'\|$$；
- 损失 $$\mathcal{L}^\text{BYOL}_\theta$$ 是 L2 归一化后的预测 $$\bar{q}_\theta(\mathbf{z})$$ 与 $$\bar{\mathbf{z}'}$$ 之间的 MSE；
- 另一个对称损失 $$\tilde{\mathcal{L}}^\text{BYOL}_\theta$$ 可以通过交换 $$\mathbf{v}'$$ 与 $$\mathbf{v}$$ 得到，即把 $$\mathbf{v}'$$ 送入在线网络、把 $$\mathbf{v}$$ 送入目标网络。
- 最终损失为 $$\mathcal{L}^\text{BYOL}_\theta + \tilde{\mathcal{L}}^\text{BYOL}_\theta$$，并且只优化参数 $$\theta$$。

与大多数流行的基于对比学习的方法不同，BYOL 不使用负样本对。大多数自举（bootstrapping）方法依赖伪标签或聚类索引，而 BYOL 直接对潜在表征进行自举。

相当有趣且令人惊讶的是，*在没有*负样本的情况下，BYOL 依然有效。后来我读到 Abe Fetterman 与 Josh Albrecht 写的这篇[文章](https://untitled-ai.github.io/understanding-self-supervised-contrastive-learning.html)，他们在尝试复现 BYOL 时强调了两个令人惊讶的发现：
1. 当*移除批归一化（batch normalization）*时，BYOL 的表现通常并不比随机更好。
2. 批归一化的存在隐式地引发了一种形式的对比学习。
他们认为，使用负样本对于避免模型坍塌很重要（试想：如果对每个数据点都使用全零表征会怎样？）。批归一化会*隐式地*注入对负样本的依赖，因为无论一批输入多么相似，它们的取值都会被重新分布（散布成 $$\sim \mathcal{N}(0, 1$$)），因此批归一化能防止模型坍塌。如果你正在这个方向工作，强烈建议阅读[全文](https://untitled-ai.github.io/understanding-self-supervised-contrastive-learning.html)。


### 记忆库

在每个批次中为大量负样本计算嵌入的开销极高。一种常见做法是把表征存储在内存中，用数据陈旧换取更廉价的计算。


#### 基于记忆库的实例判别

**实例对比学习**（[Wu et al, 2018](https://arxiv.org/abs/1805.01978v1)）将类别级监督推向极致：把每个实例都视为*独立的一个类别*。这意味着「类别」的数量将与训练集中样本的数量相同。因此，训练一个带这么多输出头的 softmax 层并不可行，但可以用 [NCE](#nce) 来近似。


![Instance contrastive learning](https://lilianweng.github.io/posts/2021-05-31-contrastive/instance-level-discrimination.png)

*图 11. 实例级对比学习的训练流程。学到的嵌入经过 L2 归一化。（图片来源：[Wu et al, 2018](https://arxiv.org/abs/1805.01978v1)）*



令 $$\mathbf{v} = f_\theta(x)$$ 为要学习的嵌入函数，其输出向量归一化为 $$\|\mathbf{v}\|=1$$。一个非参数分类器预测样本 $$\mathbf{v}$$ 属于类别 $$i$$ 的概率，其中使用温度参数 $$\tau$$：

$$
P(C=i\vert \mathbf{v}) = \frac{\exp(\mathbf{v}_i^\top \mathbf{v} / \tau)}{\sum_{j=1}^n \exp(\mathbf{v}_j^\top \mathbf{v} / \tau)}
$$

他们没有每次都为所有样本计算表征，而是实现了一个**记忆库（Memory Bank）**，把过去迭代中的样本表征存入数据库。令 $$V=\{ \mathbf{v}_i \}$$ 为记忆库，$$\mathbf{f}_i = f_\theta(\mathbf{x}_i)$$ 为网络前向计算生成的特征。在比较成对相似度时，我们可以使用来自记忆库的表征 $$\mathbf{v}_i$$，而不是网络前向输出的特征 $$\mathbf{f}_i$$。

从理论上讲，分母需要访问所有样本的表征，但这在实践中太昂贵了。我们可以改用蒙特卡洛近似，选取 $$M$$ 个索引的随机子集 $$\{j_k\}_{k=1}^M$$ 来估计它。

$$
P(i\vert \mathbf{v}) 
= \frac{\exp(\mathbf{v}^\top \mathbf{f}_i / \tau)}{\sum_{j=1}^N \exp(\mathbf{v}_j^\top \mathbf{f}_i / \tau)}
\simeq \frac{\exp(\mathbf{v}^\top \mathbf{f}_i / \tau)}{\frac{N}{M} \sum_{k=1}^M \exp(\mathbf{v}_{j_k}^\top \mathbf{f}_i / \tau)}
$$

由于每个类别只有一个实例，训练不稳定、波动很大。为了提升训练的平滑度，他们基于[近端优化方法](https://web.stanford.edu/~boyd/papers/prox_algs.html)在损失函数中为正样本引入了一个额外项。最终的 NCE 损失目标形如：

$$
\begin{aligned}
\mathcal{L}_\text{instance} &= - \mathbb{E}_{P_d}\big[\log h(i, \mathbf{v}^{(t-1)}_i) - \lambda \|\mathbf{v}^{(t)}_i - \mathbf{v}^{(t-1)}_i\|^2_2\big] - M\mathbb{E}_{P_n}\big[\log(1 - h(i, \mathbf{v}'^{(t-1)})\big] \\
h(i, \mathbf{v}) &= \frac{P(i\vert\mathbf{v})}{P(i\vert\mathbf{v}) + MP_n(i)} \text{ where the noise distribution is uniform }P_n = 1/N
\end{aligned}
$$

其中 $$\{ \mathbf{v}^{(t-1)} \}$$ 是记忆库中存储的上一次迭代的嵌入。随着学到的嵌入逐渐收敛，迭代之间的差异 $$\|\mathbf{v}^{(t)}_i - \mathbf{v}^{(t-1)}_i\|^2_2$$ 会逐渐消失。



#### MoCo 与 MoCo-V2
**动量对比（Momentum Contrast，MoCo）**（[He et al, 2019](https://arxiv.org/abs/1911.05722)）提供了一个框架，把无监督视觉表征学习视为*动态字典查询*。该字典被组织成一个大的 FIFO 队列，存放数据样本的编码表征。

给定一个查询样本 $$\mathbf{x}_q$$，我们通过编码器得到查询表征 $$\mathbf{q} = f_q(\mathbf{x}_q)$$。字典中的一列键（key）表征 $$\{\mathbf{k}_1, \mathbf{k}_2, \dots \}$$ 由动量编码器编码：$$\mathbf{k}_i = f_k (\mathbf{x}^k_i)$$。假设字典中恰有一个*正*键 $$\mathbf{k}^+$$ 与 $$\mathbf{q}$$ 匹配。论文中，$$\mathbf{k}^+$$ 的构造方式是对 $$\mathbf{x}_q$$ 施加不同的[增强](#image-augmentations)、得到其噪声副本。然后，使用带温度 $$\tau$$ 的 [InfoNCE](#infonce) 对比损失来处理 1 个正样本和 $$N-1$$ 个负样本：


$$
\mathcal{L}_\text{MoCo} = - \log \frac{\exp(\mathbf{q} \cdot \mathbf{k}^+ / \tau)}{\sum_{i=1}^N \exp(\mathbf{q} \cdot \mathbf{k}_i / \tau)}
$$

与[记忆库](#instance-discrimination-with-memoy-bank)相比，MoCo 中基于队列的字典让我们能够复用紧邻的前几个小批量数据的表征。

MoCo 的字典以队列形式存在、不可微，因此我们不能依靠反向传播来更新键编码器 $$f_k$$。一种朴素做法是让 $$f_q$$ 和 $$f_k$$ 共用同一个编码器。MoCo 则不同，它提出使用带动量系数 $$m \in [0, 1)$$ 的基于动量的更新。设 $$f_q$$ 和 $$f_k$$ 的参数分别为 $$\theta_q$$ 和 $$\theta_k$$。


$$
\theta_k \leftarrow m \theta_k + (1-m) \theta_q
$$


![MoCo](https://lilianweng.github.io/posts/2021-05-31-contrastive/MoCo.png)

*图 12. 动量对比（MoCo）如何学习视觉表征的示意图。（图片来源：   [He et al, 2019](https://arxiv.org/abs/1911.05722)）*


相比 [SimCLR](#simclr)，MoCo 的优势在于将批次大小与负样本数量解耦；而 SimCLR 需要很大的批次大小才能有足够的负样本，且当批次大小减小时会出现性能下降。

SimCLR 中的两项设计，即 (1) MLP 投影头和 (2) 更强的数据增强，被证明非常有效。**MoCo V2**（[Chen et al, 2020](https://arxiv.org/abs/2003.04297)）结合了这两项设计，在不依赖超大批次大小的情况下取得了更好的迁移性能。



#### CURL

**CURL**（[Srinivas, et al. 2020](https://arxiv.org/abs/2004.04136)）将上述思想应用于[强化学习](https://lilianweng.github.io/posts/2018-02-19-rl-overview/)。它通过对比损失匹配两个数据增强版本 $$o_q$$ 和 $$o_k$$（均来自原始观测 $$o$$）的嵌入，来为 RL 任务学习视觉表征。CURL 主要依赖随机裁剪数据增强。其键编码器实现为动量编码器，权重是查询编码器权重的 EMA，与 [MoCo](#moco--moco-v2) 中相同。

RL 与监督视觉任务之间的一个显著区别是：RL 依赖连续帧之间的*时间一致性*。因此，CURL 对每一叠帧一致地施加增强，以保留观测时间结构的信息。


![CURL](https://lilianweng.github.io/posts/2021-05-31-contrastive/CURL.png)

*图 13. CURL 的架构。（图片来源：[Srinivas, et al. 2020](https://arxiv.org/abs/2004.04136)）*



### 特征聚类

#### DeepCluster

**DeepCluster**（[Caron et al. 2018](https://arxiv.org/abs/1807.05520)）通过 k-means 迭代地对特征聚类，并使用聚类分配结果作为伪标签来提供监督信号。

![DeepCluster](https://lilianweng.github.io/posts/2021-05-31-contrastive/deepcluster.png)

*图 14. DeepCluster 方法示意图：迭代地聚类深度特征，并将聚类分配结果用作伪标签。（图片来源：[Caron et al. 2018](https://arxiv.org/abs/1807.05520)）*



在每次迭代中，DeepCluster 使用先前的表征对数据点聚类，然后产生新的聚类分配，作为新表征的分类目标。然而，这一迭代过程容易陷入平凡解。虽然它避免了使用负样本对，但需要一个代价高昂的聚类阶段，并且需要特定的防范措施来避免坍塌到平凡解。


#### SwAV

**SwAV**（*多视图分配交换*，Swapping Assignments between multiple Views；[Caron et al. 2020](https://arxiv.org/abs/2006.09882)）是一种在线对比学习算法。它从图像的一个增强版本计算出一个编码（code），并尝试用同一图像的另一个增强版本来预测这个编码。

![SwAV](https://lilianweng.github.io/posts/2021-05-31-contrastive/SwAV.png)

*图 15. SwAV 与[实例对比学习](#instance-discrimination-with-memoy-bank)的对比。（图片来源：[Caron et al. 2020](https://arxiv.org/abs/2006.09882)）*



给定两种不同增强下图像的特征 $$\mathbf{z}_t$$ 和 $$\mathbf{z}_s$$，SwAV 计算相应的编码 $$\mathbf{q}_t$$ 和 $$\mathbf{q}_s$$，损失通过交换两个编码来量化拟合程度，其中用 $$\ell(.)$$ 度量一个特征与一个编码之间的拟合度。

$$
\mathcal{L}_\text{SwAV}(\mathbf{z}_t, \mathbf{z}_s) = \ell(\mathbf{z}_t, \mathbf{q}_s) + \ell(\mathbf{z}_s, \mathbf{q}_t)
$$


交换后的拟合预测依赖于预测编码与一组 $$K$$ 个可训练原型向量 $$\mathbf{C} = \{\mathbf{c}_1, \dots, \mathbf{c}_K\}$$ 之间的交叉熵。原型向量矩阵在不同批次之间共享，表示每个实例应归属的*锚点簇*。

$$
\ell(\mathbf{z}_t, \mathbf{q}_s) = - \sum_k \mathbf{q}^{(k)}_s\log\mathbf{p}^{(k)}_t \text{ where } \mathbf{p}^{(k)}_t = \frac{\exp(\mathbf{z}_t^\top\mathbf{c}_k  / \tau)}{\sum_{k'}\exp(\mathbf{z}_t^\top \mathbf{c}_{k'} / \tau)}
$$

在一个包含 $$B$$ 个特征向量 $$\mathbf{Z} = [\mathbf{z}_1, \dots, \mathbf{z}_B]$$ 的小批量中，特征与原型向量之间的映射矩阵定义为 $$\mathbf{Q} = [\mathbf{q}_1, \dots, \mathbf{q}_B] \in \mathbb{R}_+^{K\times B}$$。我们希望最大化特征与原型之间的相似度：


$$
\begin{aligned}
\max_{\mathbf{Q}\in\mathcal{Q}} &\text{Tr}(\mathbf{Q}^\top \mathbf{C}^\top \mathbf{Z}) + \varepsilon \mathcal{H}(\mathbf{Q}) \\
\text{where }\mathcal{Q} &= \big\{ \mathbf{Q} \in \mathbb{R}_{+}^{K \times B} \mid \mathbf{Q}\mathbf{1}_B = \frac{1}{K}\mathbf{1}_K, \mathbf{Q}^\top\mathbf{1}_K = \frac{1}{B}\mathbf{1}_B \big\}
\end{aligned}
$$

其中 $$\mathcal{H}$$ 是熵，$$\mathcal{H}(\mathbf{Q}) = - \sum_{ij} \mathbf{Q}_{ij} \log \mathbf{Q}_{ij}$$，控制编码的平滑度。系数 $$\epsilon$$ 不应太大；否则所有样本都会被均匀地分配到所有簇上。$$\mathbf{Q}$$ 的候选解集要求每个映射矩阵的每一行求和为 $$1/K$$、每一列求和为 $$1/B$$，从而强制每个原型平均至少被选中 $$B/K$$ 次。

SwAV 依赖迭代的 Sinkhorn-Knopp 算法（[Cuturi 2013](https://arxiv.org/abs/1306.0895)）来求解 $$\mathbf{Q}$$。


### 利用监督数据集

#### CLIP

**CLIP**（*对比语言-图像预训练*，Contrastive Language-Image Pre-training；[Radford et al. 2021](https://arxiv.org/abs/2103.00020)）在一个预测「哪段文字对应哪张图像」的预训练任务上，联合训练一个文本编码器和一个图像特征提取器。


![CLIP](https://lilianweng.github.io/posts/2021-05-31-contrastive/CLIP.png)

*图 16. CLIP 在文本-图像对上进行对比预训练的示意图。（图片来源：[Radford et al. 2021](https://arxiv.org/abs/2103.00020)）*



给定一批 $$N$$ 个（图像，文本）对，CLIP 计算批内所有 $$N\times N$$ 种可能（图像，文本）候选之间的稠密余弦相似度矩阵。文本与图像编码器被联合训练，以通过对该稠密矩阵的对称交叉熵损失，最大化 $$N$$ 个正确（图像，文本）关联之间的相似度，同时最小化 $$N(N-1)$$ 个错误对之间的相似度。

CLIP 的 numpy 风格伪代码见图 17。

![CLIP pseudo code](https://lilianweng.github.io/posts/2021-05-31-contrastive/CLIP-algo.png)

*图 17. CLIP 算法的 Numpy 风格伪代码。（图片来源：[Radford et al. 2021](https://arxiv.org/abs/2103.00020)）*



与上面其他学习良好视觉表征的方法相比，CLIP 真正特别的地方在于*「对使用自然语言作为训练信号的重视」*。它确实需要访问监督数据集，即我们知道哪段文本与哪张图像匹配。它在从互联网收集的 4 亿（文本，图像）对上训练。查询列表包含英文版维基百科中出现至少 100 次的所有单词。有趣的是，他们发现基于 Transformer 的语言模型在零样本 ImageNet 分类上比词袋（BoW）文本编码器慢 3 倍。使用对比目标，而不是试图预测与图像相关的确切单词（即图像描述预测任务常用的方法），还能再带来 4 倍的数据效率提升。


![CLIP efficiency](https://lilianweng.github.io/posts/2021-05-31-contrastive/CLIP-efficiency.png)

*图 18. 使用词袋文本编码与对比训练目标可带来数倍的数据效率提升。（图片来源：[Radford et al. 2021](https://arxiv.org/abs/2103.00020)）*



CLIP 学到的视觉表征可以迁移到许多 CV 基准数据集并取得与监督基线相当的结果。在测试过的迁移任务中，CLIP 在非常细粒度的分类以及抽象或系统性任务（如数物体数量）上表现吃力。CLIP 模型的迁移性能与模型计算量平滑相关。


#### 监督对比学习

交叉熵损失存在若干已知问题，例如对噪声标签缺乏鲁棒性，以及可能出现较差的间隔。现有的对交叉熵损失的改进包括策划更好的训练数据，如标签平滑和数据增强。**监督对比损失（Supervised Contrastive Loss）**（[Khosla et al. 2021](https://arxiv.org/abs/2004.11362)）旨在比交叉熵更有效地利用标签信息，约束同类样本的归一化嵌入比不同类样本的嵌入更接近。


![SupCon](https://lilianweng.github.io/posts/2021-05-31-contrastive/sup-con.png)

*图 19. 监督对比损失与自监督对比损失。除增强版本之外，监督对比学习还将同类的不同样本视为正样本。（图片来源：[Khosla et al. 2021](https://arxiv.org/abs/2004.11362)）*



给定一组随机采样的 $$n$$ 个（图像，标签）对 $$\{\mathbf{x}_i, y_i\}_{i=1}^n$$，对每个样本施加两种随机增强，即可创建 $$2n$$ 个训练对 $$\{\tilde{\mathbf{x}}_i, \tilde{y}_i\}_{i=1}^{2n}$$。

监督对比损失 $$\mathcal{L}_\text{supcon}$$ 利用多个正样本和负样本，与[软最近邻损失](#soft-nearest-neighbors-loss)非常相似：

$$
\mathcal{L}_\text{supcon} = - \sum_{i=1}^{2n} \frac{1}{2 \vert N_i \vert - 1} \sum_{j \in N(y_i), j \neq i} \log \frac{\exp(\mathbf{z}_i \cdot \mathbf{z}_j / \tau)}{\sum_{k \in I, k \neq i}\exp({\mathbf{z}_i \cdot \mathbf{z}_k / \tau})}
$$

其中 $$\mathbf{z}_k=P(E(\tilde{\mathbf{x}_k}))$$，$$E(.)$$ 是编码器网络（把增强图像映射为向量），$$P(.)$$ 是投影网络（把一个向量映射为另一个向量）。$$N_i= \{j \in I: \tilde{y}_j = \tilde{y}_i \}$$ 包含标签为 $$y_i$$ 的样本的索引集合。把更多正样本纳入集合 $N_i$ 会带来更好的结果。


根据他们的实验，监督对比损失：
- 确实优于基础交叉熵，但幅度不大。
- 在鲁棒性基准（ImageNet-C，它对 ImageNet 数据集施加常见的自然发生的扰动，如噪声、模糊和对比度变化）上优于交叉熵。
- 对超参数变化不那么敏感。


 
## 语言：句子嵌入

本节聚焦于如何学习句子嵌入。

### 文本增强

视觉应用中的大多数对比方法依赖为每张图像创建增强版本。然而，构造不改变句子语义的文本增强更具挑战性。本节将考察三种增强文本序列的方法：词汇编辑、回译以及应用 cutoff 或 dropout。


#### 词汇编辑

**EDA**（*简单数据增强*，Easy Data Augmentation；[Wei & Zou 2019](https://arxiv.org/abs/1901.11196)）定义了一组简单而强大的文本增强操作。给定一个句子，EDA 随机选择并应用以下四种简单操作之一：

1. 同义词替换（Synonym replacement，SR）：用同义词替换 $$n$$ 个随机的非停用词。
2. 随机插入（Random insertion，RI）：把随机选定的非停用词的一个随机同义词插入到句子中的随机位置。
3. 随机交换（Random swap，RS）：随机交换两个词，并重复 $$n$$ 次。
4. 随机删除（Random deletion，RD）：以概率 $$p$$ 随机删除句子中的每个词。

其中 $$p=\alpha$$、$$n=\alpha \times \text{sentence_length}$$，直觉是：更长的句子在保持原标签的同时能吸收更多噪声。超参数 $$\alpha$$ 大致表示一次增强可能改变一个句子中单词的百分比。

实验表明，与不使用 EDA 的基线相比，EDA 在多个分类基准数据集上提升了分类准确率。训练集越小时，性能提升越明显。EDA 的四种操作都有助于提升分类准确率，但各自在不同的 $$\alpha$$ 值上达到最优。

![EDA classification](https://lilianweng.github.io/posts/2021-05-31-contrastive/EDA-exp1.png)

*图 20. EDA 在多个分类基准上带来性能提升。（图片来源：[Wei & Zou 2019](https://arxiv.org/abs/1901.11196)）*



在**上下文增强（Contextual Augmentation）**（[Sosuke Kobayashi, 2018](https://arxiv.org/abs/1805.06201)）中，词 $$w_i$$ 在位置 $$i$$ 上的新替换词可以从给定的概率分布 $$p(.\mid S\setminus\{w_i\})$$ 中平滑地采样得到，该分布由 BERT 这样的双向语言模型预测。



#### 回译

**CERT**（*对比自监督 Transformer 编码器表征*，Contrastive self-supervised Encoder Representations from Transformers；[Fang et al. (2020)](https://arxiv.org/abs/2005.12766)；[代码](https://github.com/UCSD-AI4H/CERT)）通过**回译（back-translation）**生成增强句子。可以使用面向不同语言的各种翻译模型来创建不同版本的增强。一旦有了文本样本的噪声版本，上面介绍的许多对比学习框架（例如 [MoCo](#moco--moco-v2)）都可以用来学习句子嵌入。


#### Dropout 与 Cutoff

[Shen et al. (2020)](https://arxiv.org/abs/2009.13818) 受[跨视图训练](https://lilianweng.github.io/posts/2019-01-31-lm/#cross-view-training)启发，提出将 **Cutoff（截断）** 应用于文本增强。他们提出了三种 cutoff 增强策略：
1. *Token cutoff（词元截断）*：移除若干选定 token 的信息。为确保不发生数据泄漏，输入嵌入、位置嵌入以及其他相关嵌入矩阵中对应的 token 都应被置零。
2. *Feature cutoff（特征截断）*：移除若干特征列。
3. *Span cutoff（片段截断）*：移除一段连续的文本。


![Text cutoff](https://lilianweng.github.io/posts/2021-05-31-contrastive/text-cutoff.png)

*图 21. token、feature 与 span 三种 cutoff 增强策略的原理示意图。（图片来源：[Shen et al. 2020](https://arxiv.org/abs/2009.13818)）*


可以为一个样本创建多个增强版本。训练时，[Shen et al. (2020)](https://arxiv.org/abs/2009.13818) 额外应用了一个 KL 散度项来度量不同增强样本的预测之间的一致性。


**SimCSE**（[Gao et al. 2021](https://arxiv.org/abs/2104.08821)；[代码](https://github.com/princeton-nlp/SimCSE)）从无监督数据中学习：仅用 **dropout** 噪声来预测句子自身。换句话说，他们把 dropout 当作文本序列的数据增强。把一个样本以不同的 dropout 掩码送入编码器两次，这两个版本构成正样本对，而批内其他样本被视为负样本对。这与 cutoff 增强感觉相当相似，但 dropout 更灵活，被掩蔽内容在语义上不那么明确。


![SimCSE](https://lilianweng.github.io/posts/2021-05-31-contrastive/SimCSE.png)

*图 22. SimCSE 通过施加不同的 dropout 掩码创建增强样本。监督版本利用 NLI 数据集，在给定句子对时预测正（蕴含）或负（矛盾）。（图片来源：[Gao et al. 2021](https://arxiv.org/abs/2104.08821)）*



他们在 7 个 STS（语义文本相似度，Semantic Text Similarity）数据集上进行了实验，计算句子嵌入之间的余弦相似度。他们还尝试了一个可选的 MLM 辅助目标损失，以帮助避免 token 级知识的灾难性遗忘。结果发现，这个辅助损失有助于提升迁移任务上的性能，但在主要的 STS 任务上却带来一致的下降。


![SimCSE experiments](https://lilianweng.github.io/posts/2021-05-31-contrastive/SimCSE-STS-exp.png)

*图 23. SimCSE 在一组 STS 基准上的实验数值。（图片来源：[Gao et al. 2021](https://arxiv.org/abs/2104.08821)）*



### 来自 NLI 的监督

人们发现，未经任何微调的预训练 BERT 句子嵌入在语义相似度任务上表现很差。我们不能直接使用原始嵌入，而需要通过进一步微调来精炼嵌入。

**自然语言推理（Natural Language Inference，NLI）**任务是学习句子嵌入的主要监督信号数据源，例如 [SNLI](https://nlp.stanford.edu/projects/snli/)、[MNLI](https://cims.nyu.edu/~sbowman/multinli/) 和 [QQP](https://www.kaggle.com/c/quora-question-pairs)。


#### Sentence-BERT

**SBERT（Sentence-BERT）**（[Reimers & Gurevych, 2019](https://arxiv.org/abs/1908.10084)）依靠孪生网络与三元组网络架构来学习句子嵌入，使句子相似度可以通过嵌入对之间的余弦相似度来估计。注意，训练 SBERT 依赖监督数据，因为它是在多个 NLI 数据集上微调的。

他们在 BERT 模型之上实验了几种不同的预测头：
- Softmax 分类目标：孪生网络的分类头构建在两个嵌入 $$f(\mathbf{x}), f(\mathbf{x}')$$ 与 $$\vert f(\mathbf{x}) - f(\mathbf{x}') \vert$$ 的拼接之上。预测输出为 $$\hat{y}=\text{softmax}(\mathbf{W}_t [f(\mathbf{x}); f(\mathbf{x}'); \vert f(\mathbf{x}) - f(\mathbf{x}') \vert])$$。他们发现，最重要的成分是逐元素差异 $$\vert f(\mathbf{x}) - f(\mathbf{x}') \vert$$。
- 回归目标：这是 $$\cos(f(\mathbf{x}), f(\mathbf{x}'))$$ 上的回归损失，其中池化策略影响很大。实验中他们观察到，`max` 的表现远差于 `mean` 和 `CLS`-token。
- 三元组目标：$$\max(0, \|f(\mathbf{x}) - f(\mathbf{x}^+)\|- \|f(\mathbf{x}) - f(\mathbf{x}^-)\| + \epsilon)$$，其中 $$\mathbf{x}, \mathbf{x}^+, \mathbf{x}^-$$ 分别是锚点句、正样本句和负样本句的嵌入。

实验中，哪种目标函数效果最好取决于数据集，因此没有普适的赢家。


![SBERT](https://lilianweng.github.io/posts/2021-05-31-contrastive/SBERT.png)

*图 24. 带 softmax 分类头与回归头的 Sentence-BERT 训练框架示意图。（图片来源：[Reimers & Gurevych, 2019](https://arxiv.org/abs/1908.10084)）*

[SentEval](https://github.com/facebookresearch/SentEval) 库（[Conneau and Kiela, 2018](https://arxiv.org/abs/1803.05449)）通常用于评估所学句子嵌入的质量。在当时（2019 年 8 月），SBERT 在 7 项任务中的 5 项上超过了其他基线。

![SBERT SentEval results](https://lilianweng.github.io/posts/2021-05-31-contrastive/SBERT-SentEval.png)

*图 25. Sentence-BERT 在 SentEval 基准上的性能。（图片来源：[Reimers & Gurevych, 2019](https://arxiv.org/abs/1908.10084)）*



#### BERT-flow

<a name='isotropy' />如果嵌入在每个维度上都均匀分布，则称嵌入表征空间是*各向同性（isotropic）*的；否则就是*各向异性（anisotropic）*的。[Li et al, (2020)](https://arxiv.org/abs/2011.05864) 表明，预训练 BERT 学到的是一个非平滑、*各向异性*的句子嵌入语义空间，因此在没有微调的情况下，文本相似度任务表现很差。经验上，他们观察到 BERT 句子嵌入存在两个问题：
词频会使嵌入空间产生偏置。高频词靠近原点，而低频词远离原点。
低频词稀疏分散。低频词的嵌入往往离其 $$k$$-NN 近邻更远，而高频词的嵌入则更加稠密地集中。

**BERT-flow**（[Li et al, 2020](https://arxiv.org/abs/2011.05864)；[代码](https://github.com/bohanli/BERT-flow)）被提出来，通过[归一化流](https://lilianweng.github.io/posts/2018-10-13-flow-models/#what-is-normalizing-flows)将嵌入变换为平滑且各向同性的高斯分布。


![BERT-flow](https://lilianweng.github.io/posts/2021-05-31-contrastive/BERT-flow.png)

*图 26. BERT-flow 中对原始句子嵌入空间进行基于流的校准的示意图。（图片来源：[Li et al, 2020](https://arxiv.org/abs/2011.05864)）*


令 $$\mathcal{U}$$ 为观测到的 BERT 句子嵌入空间，$$\mathcal{Z}$$ 为期望的潜空间，即标准高斯分布。于是 $$p_\mathcal{Z}$$ 是高斯密度函数，$$f_\phi: \mathcal{Z}\to\mathcal{U}$$ 是一个可逆变换：


$$
\mathbf{z}\sim p_\mathcal{Z}(\mathbf{z}) \quad 
\mathbf{u}=f_\phi(\mathbf{z}) \quad
\mathbf{z}=f^{-1}_\phi(\mathbf{u}) 
$$


基于流的生成模型通过最大化 $$\mathcal{U}$$ 的边际似然来学习这个可逆映射函数：


$$
\max_\phi\mathbb{E}_{\mathbf{u}=\text{BERT}(s), s\sim\mathcal{D}} \Big[ \log p_\mathcal{Z}(f^{-1}_\phi(\mathbf{u})) + \log\big\vert\det\frac{\partial f^{-1}_\phi(\mathbf{u})}{\partial\mathbf{u}}\big\vert \Big]
$$

其中 $$s$$ 是从文本语料 $$\mathcal{D}$$ 中采样的一句话。只优化流参数 $$\phi$$，预训练 BERT 中的参数保持不变。

结果表明，无论是否使用 NLI 数据集的监督，BERT-flow 都能提升大多数 STS 任务上的性能。由于学习用于校准的归一化流不需要标签，它可以使用包括验证集和测试集在内的整个数据集。


#### 白化操作

[Su et al. (2021)](https://arxiv.org/abs/2103.15316) 应用**白化（whitening）**操作来提升所学表征的[各向同性](#isotropy)，同时降低句子嵌入的维度。

他们把句子向量的均值变换为 0、协方差矩阵变换为单位矩阵。给定一组样本 $$\{\mathbf{x}_i\}_{i=1}^N$$，令 $$\tilde{\mathbf{x}}_i$$ 和 $$\tilde{\Sigma}$$ 为变换后的样本及相应的协方差矩阵：



$$
\begin{aligned}
\mu &= \frac{1}{N}\sum_{i=1}^N \mathbf{x}_i \quad \Sigma = \frac{1}{N}\sum_{i=1}^N (\mathbf{x}_i - \mu)^\top (\mathbf{x}_i - \mu) \\
\tilde{\mathbf{x}}_i &= (\mathbf{x}_i - \mu)W \quad \tilde{\Sigma} = W^\top\Sigma W = I \text{ thus } \Sigma = (W^{-1})^\top W^{-1}
\end{aligned}
$$

如果我们对 $$\Sigma = U\Lambda U^\top$$ 做 [SVD](https://en.wikipedia.org/wiki/Singular_value_decomposition) 分解，就会得到 $$W^{-1}=\sqrt{\Lambda} U^\top$$ 和 $$W=U\sqrt{\Lambda^{-1}}$$。注意在 SVD 中，$$U$$ 是列向量为特征向量的正交矩阵，$$\Lambda$$ 是对角矩阵，其对角元为排序后的正特征值。

一种降维策略是只取前 $$k$$ 列来截断 $$W$$，称为 `Whitening`-$$k$$。

![Whitening-SBERT](https://lilianweng.github.io/posts/2021-05-31-contrastive/whitening-SBERT.png)

*图 27. whitening-$$k$$ 操作的伪代码。（图片来源：[Su et al. 2021](https://arxiv.org/abs/2103.15316)）*


结果表明，白化操作优于 BERT-flow，并且在有无 NLI 监督的许多 STS 基准上，以 256 维的句子嵌入取得了 SOTA。



### 无监督句子嵌入学习

#### 上下文预测

**Quick-Thought（QT）向量**（[Logeswaran & Lee, 2018](https://arxiv.org/abs/1803.02893)）把句子表征学习表述为一个*分类*问题：给定一个句子及其上下文，分类器基于向量表征把上下文句子与其他对比句子区分开（[「完形测试」](https://lilianweng.github.io/posts/2019-01-31-lm/#MLM)）。这样的表述去掉了会导致训练变慢的 softmax 输出层。


![Quick-Thought vectors](https://lilianweng.github.io/posts/2021-05-31-contrastive/quick-thought.png)

*图 28. Quick-Thought 句子嵌入向量如何学到的示意图。（图片来源：[Logeswaran & Lee, 2018](https://arxiv.org/abs/1803.02893)）*



令 $$f(.)$$ 和 $$g(.)$$ 为把句子 $$s$$ 编码为定长向量的两个函数。令 $$C(s)$$ 为 $$s$$ 上下文中的句子集合，$$S(s)$$ 为候选句子集合，其中只包含一个句子 $$s_c \in C(s)$$ 以及许多非上下文的负样本句。Quick Thoughts 模型学习优化预测唯一真正的上下文句子 $$s_c \in S(s)$$ 的概率。本质上，当把句对 $$(s, s_c)$$ 视为正样本对、其余句对 $$(s, s')$$（其中 $$s' \in S(s), s'\neq s_c$$）视为负样本时，这就是 NCE 损失。

$$
\mathcal{L}_\text{QT} 
= - \sum_{s \in \mathcal{D}} \sum_{s_c \in C(s)} \log p(s_c \vert s, S(s)) 
= - \sum_{s \in \mathcal{D}} \sum_{s_c \in C(s)}\frac{\exp(f(s)^\top g(s_c))}{\sum_{s'\in S(s)} \exp(f(s)^\top g(s'))}
$$


#### 互信息最大化

**IS-BERT（Info-Sentence BERT）**（[Zhang et al. 2020](https://arxiv.org/abs/2009.12061)；[代码](https://github.com/yanzhangnlp/IS-BERT)）采用基于*互信息最大化*的自监督学习目标，以*无监督*的方式学习良好的句子嵌入。


![IS-BERT](https://lilianweng.github.io/posts/2021-05-31-contrastive/IS-BERT.png)

*图 29. Info-Sentence BERT 示意图。（图片来源：[Zhang et al. 2020](https://arxiv.org/abs/2009.12061)）*



IS-BERT 的工作流程如下：
1. 用 BERT 把输入句子 $$s$$ 编码为长度为 $$l$$ 的 token 嵌入 $$\mathbf{h}_{1:l}$$。

2. 然后使用不同卷积核尺寸（如 1、3、5）的一维卷积网络处理 token 嵌入序列，以捕获 n-gram 局部上下文依赖：$$\mathbf{c}_i = \text{ReLU}(\mathbf{w} \cdot \mathbf{h}_{i:i+k-1} + \mathbf{b})$$。输出序列会被填充（pad）到与输入相同的长度。
3. 第 $$i$$ 个 token 的最终局部表征 $$\mathcal{F}_\theta^{(i)} (\mathbf{x})$$ 是不同卷积核尺寸的表征的拼接。
4. 全局句子表征 $$\mathcal{E}_\theta(\mathbf{x})$$ 通过对 token 表征 $$\mathcal{F}_\theta(\mathbf{x}) = \{\mathcal{F}_\theta^{(i)} (\mathbf{x}) \in \mathbb{R}^d\}_{i=1}^l$$ 施加逐时间步平均池化（mean-over-time pooling）层计算得到。

由于互信息估计对于连续、高维的随机变量通常不可解，IS-BERT 依赖 Jensen-Shannon 估计器（[Nowozin et al., 2016](https://arxiv.org/abs/1606.00709)、[Hjelm et al., 2019](https://arxiv.org/abs/1808.06670)）来最大化 $$\mathcal{E}_\theta(\mathbf{x})$$ 与 $$\mathcal{F}_\theta^{(i)} (\mathbf{x})$$ 之间的互信息。


$$
I^\text{JSD}_\omega(\mathcal{F}_\theta^{(i)} (\mathbf{x}); \mathcal{E}_\theta(\mathbf{x})) = \mathbb{E}_{\mathbf{x}\sim P} [-\text{sp}(-T_\omega(\mathcal{F}_\theta^{(i)} (\mathbf{x}); \mathcal{E}_\theta(\mathbf{x})))] \\ - \mathbb{E}_{\mathbf{x}\sim P, \mathbf{x}' \sim\tilde{P}} [\text{sp}(T_\omega(\mathcal{F}_\theta^{(i)} (\mathbf{x}'); \mathcal{E}_\theta(\mathbf{x})))]
$$

其中 $$T_\omega: \mathcal{F}\times\mathcal{E} \to \mathbb{R}$$ 是一个参数为 $$\omega$$ 的可学习网络，生成判别器分数。负样本 $$\mathbf{x}'$$ 采样自分布 $$\tilde{P}=P$$。$$\text{sp}(x)=\log(1+e^x)$$ 是 softplus 激活函数。

在 SentEval 上，IS-BERT 的无监督成绩优于大多数无监督基线（2020 年 9 月），但不出所料地弱于有监督的结果。使用带标签的 NLI 数据集时，IS-BERT 取得了与 SBERT 相当的结果（见图 25 与图 30）。


![IS-BERT SentEval results](https://lilianweng.github.io/posts/2021-05-31-contrastive/IS-BERT-SentEval.png)

*图 30. IS-BERT 在 SentEval 基准上的性能。（图片来源：[Zhang et al. 2020](https://arxiv.org/abs/2009.12061)）*



---
引用格式：
```
@article{weng2021contrastive,
  title   = "Contrastive Representation Learning",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2021",
  url     = "https://lilianweng.github.io/lil-log/2021/05/31/contrastive-representation-learning.html"
}
```

## 参考文献


[1] Sumit Chopra, Raia Hadsell and Yann LeCun. ["Learning a similarity metric discriminatively, with application to face verification."](http://yann.lecun.com/exdb/publis/pdf/chopra-05.pdf) CVPR 2005.

[2] Florian Schroff, Dmitry Kalenichenko and James Philbin. ["FaceNet: A Unified Embedding for Face Recognition and Clustering."](https://arxiv.org/abs/1503.03832) CVPR 2015.

[3] Hyun Oh Song et al. ["Deep Metric Learning via Lifted Structured Feature Embedding."](https://arxiv.org/abs/1511.06452) CVPR 2016. [[code](https://github.com/rksltnl/Deep-Metric-Learning-CVPR16)]

[4] Ruslan Salakhutdinov and Geoff Hinton. ["Learning a Nonlinear Embedding by Preserving Class Neighbourhood Structure"](http://proceedings.mlr.press/v2/salakhutdinov07a.html) AISTATS 2007.

[5] Michael Gutmann and Aapo Hyvärinen. ["Noise-contrastive estimation: A new estimation principle for unnormalized statistical models."](http://proceedings.mlr.press/v9/gutmann10a.html) AISTATS 2010.

[6] Kihyuk Sohn et al. ["Improved Deep Metric Learning with Multi-class N-pair Loss Objective"](https://papers.nips.cc/paper/2016/hash/6b180037abbebea991d8b1232f8a8ca9-Abstract.html) NIPS 2016.

[7] Nicholas Frosst, Nicolas Papernot and Geoffrey Hinton. ["Analyzing and Improving Representations with the Soft Nearest Neighbor Loss."](http://proceedings.mlr.press/v97/frosst19a.html) ICML 2019

[8] Tongzhou Wang and Phillip Isola. ["Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere."](https://arxiv.org/abs/2005.10242) ICML 2020. [[code](https://ssnl.github.io/hypersphere/)]

[9] Zhirong Wu et al. ["Unsupervised feature learning via non-parametric instance-level discrimination."](https://arxiv.org/abs/1805.01978) CVPR 2018.

[10] Ekin D. Cubuk et al. ["AutoAugment: Learning augmentation policies from data."](https://arxiv.org/abs/1805.09501) arXiv preprint arXiv:1805.09501 (2018).

[11] Daniel Ho et al. ["Population Based Augmentation: Efficient Learning of Augmentation Policy Schedules."](https://arxiv.org/abs/1905.05393) ICML 2019.

[12] Ekin D. Cubuk & Barret Zoph et al. ["RandAugment: Practical automated data augmentation with a reduced search space."](https://arxiv.org/abs/1909.13719) arXiv preprint arXiv:1909.13719 (2019).

[13] Hongyi Zhang et al. ["mixup: Beyond Empirical Risk Minimization."](https://arxiv.org/abs/1710.09412) ICLR 2017.

[14] Sangdoo Yun et al. ["CutMix: Regularization Strategy to Train Strong Classifiers with Localizable Features."](https://arxiv.org/abs/1905.04899) ICCV 2019.

[15] Yannis Kalantidis et al. ["Mixing of Contrastive Hard Negatives"](https://arxiv.org/abs/2010.01028) NeuriPS 2020.

[16] Ashish Jaiswal et al. ["A Survey on Contrastive Self-Supervised Learning."](https://arxiv.org/abs/2011.00362) arXiv preprint arXiv:2011.00362 (2021)

[17] Jure Zbontar et al. ["Barlow Twins: Self-Supervised Learning via Redundancy Reduction."](https://arxiv.org/abs/2103.03230) arXiv preprint arXiv:2103.03230 (2021) [[code](https://github.com/facebookresearch/barlowtwins)]

[18] Alec Radford, et al. ["Learning Transferable Visual Models From Natural Language Supervision"](https://arxiv.org/abs/2103.00020) arXiv preprint arXiv:2103.00020 (2021)

[19] Mathilde Caron et al. ["Unsupervised Learning of Visual Features by Contrasting Cluster Assignments (SwAV)."](https://arxiv.org/abs/2006.09882) NeuriPS 2020.

[20] Mathilde Caron et al. ["Deep Clustering for Unsupervised Learning of Visual Features."](https://arxiv.org/abs/1807.05520) ECCV 2018.

[21] Prannay Khosla et al. ["Supervised Contrastive Learning."](https://arxiv.org/abs/2004.11362) NeurIPS 2020.

[22] Aaron van den Oord, Yazhe Li & Oriol Vinyals. ["Representation Learning with Contrastive Predictive Coding"](https://arxiv.org/abs/1807.03748) arXiv preprint arXiv:1807.03748 (2018).

[23] Jason Wei and Kai Zou. ["EDA: Easy data augmentation techniques for boosting performance on text classification tasks."](https://arxiv.org/abs/1901.11196)  EMNLP-IJCNLP 2019.

[24] Sosuke Kobayashi. ["Contextual Augmentation: Data Augmentation by Words with Paradigmatic Relations."](https://arxiv.org/abs/1805.06201) NAACL 2018

[25] Hongchao Fang et al. ["CERT: Contrastive self-supervised learning for language understanding."](https://arxiv.org/abs/2005.12766) arXiv preprint arXiv:2005.12766 (2020).

[26] Dinghan Shen et al. ["A Simple but Tough-to-Beat Data Augmentation Approach for Natural Language Understanding and Generation."](https://arxiv.org/abs/2009.13818) arXiv preprint arXiv:2009.13818 (2020) [[code](https://github.com/dinghanshen/cutoff)]

[27] Tianyu Gao et al. ["SimCSE: Simple Contrastive Learning of Sentence Embeddings."](https://arxiv.org/abs/2104.08821) arXiv preprint arXiv:2104.08821 (2020). [[code](https://github.com/princeton-nlp/SimCSE)]

[28] Nils Reimers and Iryna Gurevych. ["Sentence-BERT: Sentence embeddings using Siamese BERT-networks."](https://arxiv.org/abs/1908.10084) EMNLP 2019.

[29] Jianlin Su et al. ["Whitening sentence representations for better semantics and faster retrieval."](https://arxiv.org/abs/2103.15316) arXiv preprint arXiv:2103.15316 (2021). [[code](https://github.com/bojone/BERT-whitening)]

[30] Yan Zhang et al. ["An unsupervised sentence embedding method by mutual information maximization."](https://arxiv.org/abs/2009.12061) EMNLP 2020. [[code](https://github.com/yanzhangnlp/IS-BERT)]

[31] Bohan Li et al. ["On the sentence embeddings from pre-trained language models."](https://arxiv.org/abs/2011.05864) EMNLP 2020.

[32] Lajanugen Logeswaran and Honglak Lee. ["An efficient framework for learning sentence representations."](https://arxiv.org/abs/1803.02893) ICLR 2018. 

[33] Joshua Robinson, et al. ["Contrastive Learning with Hard Negative Samples."](https://arxiv.org/abs/2010.04592) ICLR 2021.

[34] Ching-Yao Chuang et al. ["Debiased Contrastive Learning."](https://arxiv.org/abs/2007.00224) NeuriPS 2020.
