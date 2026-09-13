---
title: "什么是扩散模型？"
title_en: "What are Diffusion Models?"
source: https://lilianweng.github.io/posts/2021-07-11-diffusion-models/
crawled: 2026-09-08
translated: 2026-09-08
---

# 什么是扩散模型？

> 原文：[What are Diffusion Models?](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/) · Lilian Weng（翁荔）

> 扩散模型是一类新型生成模型，足够灵活以学习任意复杂的数据分布，同时又可以解析地评估该分布。近期工作表明扩散模型能生成高质量图像，性能可与 SOTA GAN 竞争。

<span style="color: #286ee0;">[更新于 2021-09-19：强烈推荐 Yang Song（参考文献中多篇关键论文的作者）这篇关于[基于分数的生成建模](https://yang-song.github.io/blog/2021/score/)的博文。]</span>

到目前为止，我已写过三类生成模型：[GAN](https://lilianweng.github.io/posts/2017-08-20-gan/)、[VAE](https://lilianweng.github.io/posts/2018-08-12-vae/) 和[基于流](https://lilianweng.github.io/posts/2018-10-13-flow-models/)的模型。它们在生成高质量样本上都大获成功，但各有局限。GAN 因其对抗训练的性质，已知可能训练不稳定、生成多样性不足。VAE 依赖代理损失。流模型必须使用专门架构来构造可逆变换。

扩散模型受非平衡热力学启发。它们定义一条扩散步骤的马尔可夫链，逐步向数据添加随机噪声，然后学习逆转扩散过程，从噪声中构造想要的数据样本。与 VAE 或流模型不同，扩散模型以固定过程学习，且潜变量维度很高（与原始数据相同）。

![Overview](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/generative-overview.png)

图 1. 不同类型生成模型概览。

## 什么是扩散模型？

已有若干基于扩散的生成模型被提出，底层思想相似，包括*扩散概率模型*（diffusion probabilistic models；[Sohl-Dickstein et al., 2015](https://arxiv.org/abs/1503.03585)）、*噪声条件分数网络（noise-conditioned score network，NCSN*；[Yang & Ermon, 2019](https://arxiv.org/abs/1907.05600)）和*去噪扩散概率模型（denoising diffusion probabilistic models，DDPM*；[Ho et al. 2020](https://arxiv.org/abs/2006.11239)）。

### 前向扩散过程

给定从真实数据分布采样的数据点 $$\mathbf{x}_0 \sim q(\mathbf{x})$$，定义一个*前向扩散过程*：在 $$T$$ 步中向样本加入少量高斯噪声，产生一列带噪样本 $$\mathbf{x}_1, \dots, \mathbf{x}_T$$。步长由方差调度 $$\{\beta_t \in (0, 1)\}_{t=1}^t$$ 控制。

$$
q(\mathbf{x}_t \vert \mathbf{x}_{t-1}) = \mathcal{N}(\mathbf{x}_t; \sqrt{1 - \beta_t} \mathbf{x}_{t-1}, \beta_t\mathbf{I}) \quad
q(\mathbf{x}_{1:T} \vert \mathbf{x}_0) = \prod^T_{t=1} q(\mathbf{x}_t \vert \mathbf{x}_{t-1})
$$

随着步数 $$t$$ 变大，数据样本 $$\mathbf{x}_0$$ 逐渐失去可分辨特征。最终当 $$T \to \infty$$，$$\mathbf{x}_T$$ 等价于各向同性高斯分布。

![DDPM](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/DDPM.png)

图 2. 通过逐步加（去）噪生成样本的前向（反向）扩散过程的马尔可夫链。（图片来源：[Ho et al. 2020](https://arxiv.org/abs/2006.11239)，加了少量额外标注）

<a name="nice"/>上述过程的一个良好性质是：我们可以用[重参数化技巧](https://lilianweng.github.io/posts/2018-08-12-vae/#reparameterization-trick)以闭式在任意时间步 $$t$$ 采样 $$\mathbf{x}_t$$。设 $$\alpha_t = 1 - \beta_t$$，$$\bar{\alpha}_t = \prod_{i=1}^T \alpha_i$$：

$$
\begin{aligned}
\mathbf{x}_t 
&= \sqrt{\alpha_t}\mathbf{x}_{t-1} + \sqrt{1 - \alpha_t}\mathbf{z}_{t-1} & \text{ ;where } \mathbf{z}_{t-1}, \mathbf{z}_{t-2}, \dots \sim \mathcal{N}(\mathbf{0}, \mathbf{I}) \\
&= \sqrt{\alpha_t \alpha_{t-1}} \mathbf{x}_{t-2} + \sqrt{1 - \alpha_t \alpha_{t-1}} \bar{\mathbf{z}}_{t-2} & \text{ ;where } \bar{\mathbf{z}}_{t-2} \text{ merges two Gaussians (*).} \\
&= \dots \\
&= \sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t}\mathbf{z} \\
q(\mathbf{x}_t \vert \mathbf{x}_0) &= \mathcal{N}(\mathbf{x}_t; \sqrt{\bar{\alpha}_t} \mathbf{x}_0, (1 - \bar{\alpha}_t)\mathbf{I})
\end{aligned}
$$

(*) 回忆：合并两个不同方差的高斯 $$\mathcal{N}(\mathbf{0}, \sigma_1^2\mathbf{I})$$ 与 $$\mathcal{N}(\mathbf{0}, \sigma_2^2\mathbf{I})$$ 时，新分布为 $$\mathcal{N}(\mathbf{0}, (\sigma_1^2 + \sigma_2^2)\mathbf{I})$$。这里合并后的标准差为 $$\sqrt{(1 - \alpha_t) + \alpha_t (1-\alpha_{t-1})} = \sqrt{1 - \alpha_t\alpha_{t-1}}$$。

通常，样本噪声越大我们可以承受越大的更新步长，所以 $$\beta_1 < \beta_2 < \dots < \beta_T$$，因此 $$\bar{\alpha}_1 > \dots > \bar{\alpha}_T$$。

#### 与随机梯度朗之万动力学的联系

朗之万动力学是物理学的概念，为统计建模分子系统而发展。结合随机梯度下降，*随机梯度朗之万动力学*（stochastic gradient Langevin dynamics；[Welling & Teh 2011](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.226.363)）可以只用梯度 $$\nabla_\mathbf{x} \log p(\mathbf{x})$$，在马尔可夫链更新中从概率密度 $$p(\mathbf{x})$$ 产生样本：

$$
\mathbf{x}_t = \mathbf{x}_{t-1} + \frac{\epsilon}{2} \nabla_\mathbf{x} p(\mathbf{x}_{t-1}) + \sqrt{\epsilon} \mathbf{z}_t
,\quad\text{where }
\mathbf{z}_t \sim \mathcal{N}(\mathbf{0}, \mathbf{I})
$$

其中 $$\epsilon$$ 是步长。当 $$T \to \infty, \epsilon \to 0$$，$$\mathbf{x}_T$$ 等于真实概率密度 $$p(\mathbf{x})$$。

与标准 SGD 相比，随机梯度朗之万动力学向参数更新注入高斯噪声以避免塌缩到局部极小。

### 反向扩散过程

如果我们能逆转上述过程并从 $$q(\mathbf{x}_{t-1} \vert \mathbf{x}_t)$$ 采样，我们就能从高斯噪声输入 $$\mathbf{x}_T \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$ 重建真实样本。注意若 $$\beta_t$$ 足够小，$$q(\mathbf{x}_{t-1} \vert \mathbf{x}_t)$$ 也将是高斯。遗憾的是，我们无法轻易估计 $$q(\mathbf{x}_{t-1} \vert \mathbf{x}_t)$$，因为它需要用到整个数据集，因此需要学习一个模型 $$p_\theta$$ 来近似这些条件概率，以运行*反向扩散过程*。

$$
p_\theta(\mathbf{x}_{0:T}) = p(\mathbf{x}_T) \prod^T_{t=1} p_\theta(\mathbf{x}_{t-1} \vert \mathbf{x}_t) \quad
p_\theta(\mathbf{x}_{t-1} \vert \mathbf{x}_t) = \mathcal{N}(\mathbf{x}_{t-1}; \boldsymbol{\mu}_\theta(\mathbf{x}_t, t), \boldsymbol{\Sigma}_\theta(\mathbf{x}_t, t))
$$

![Diffusion model examples](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/diffusion-example.png)

图 3. 训练扩散模型建模 2D 瑞士卷数据的一个示例。（图片来源：[Sohl-Dickstein et al., 2015](https://arxiv.org/abs/1503.03585)）

值得注意的是，以 $$\mathbf{x}_0$$ 为条件时反向条件概率是可解的：

$$
q(\mathbf{x}_{t-1} \vert \mathbf{x}_t, \mathbf{x}_0) = \mathcal{N}(\mathbf{x}_{t-1}; \color{blue}{\tilde{\boldsymbol{\mu}}}(\mathbf{x}_t, \mathbf{x}_0), \color{red}{\tilde{\beta}_t} \mathbf{I})
$$

用贝叶斯规则，我们有：

$$
\begin{aligned}
q(\mathbf{x}_{t-1} \vert \mathbf{x}_t, \mathbf{x}_0) 
&= q(\mathbf{x}_t \vert \mathbf{x}_{t-1}, \mathbf{x}_0) \frac{ q(\mathbf{x}_{t-1} \vert \mathbf{x}_0) }{ q(\mathbf{x}_t \vert \mathbf{x}_0) } \\
&\propto \exp \Big(-\frac{1}{2} \big(\frac{(\mathbf{x}_t - \sqrt{\alpha_t} \mathbf{x}_{t-1})^2}{\beta_t} + \frac{(\mathbf{x}_{t-1} - \sqrt{\bar{\alpha}_{t-1}} \mathbf{x}_0)^2}{1-\bar{\alpha}_{t-1}} - \frac{(\mathbf{x}_t - \sqrt{\bar{\alpha}_t} \mathbf{x}_0)^2}{1-\bar{\alpha}_t} \big) \Big) \\
&= \exp\Big( -\frac{1}{2} \big( \color{red}{(\frac{\alpha_t}{\beta_t} + \frac{1}{1 - \bar{\alpha}_{t-1}})} \mathbf{x}_{t-1}^2 - \color{blue}{(\frac{2\sqrt{\alpha_t}}{\beta_t} \mathbf{x}_t + \frac{2\sqrt{\bar{\alpha}_t}}{1 - \bar{\alpha}_t} \mathbf{x}_0)} \mathbf{x}_{t-1} + C(\mathbf{x}_t, \mathbf{x}_0) \big) \Big)
\end{aligned}
$$

其中 $$C(\mathbf{x}_t, \mathbf{x}_0)$$ 是某个不涉及 $$\mathbf{x}_{t-1}$$ 的函数，细节略去。按标准高斯密度函数，均值与方差可参数化为：

$$
\begin{aligned}
\tilde{\beta}_t &= 1/(\frac{\alpha_t}{\beta_t} + \frac{1}{1 - \bar{\alpha}_{t-1}}) = \frac{1 - \bar{\alpha}_{t-1}}{1 - \bar{\alpha}_t} \cdot \beta_t \\
\tilde{\boldsymbol{\mu}}_t (\mathbf{x}_t, \mathbf{x}_0)
&= (\frac{\sqrt{\alpha_t}}{\beta_t} \mathbf{x}_t + \frac{\sqrt{\bar{\alpha}_t}}{1 - \bar{\alpha}_t} \mathbf{x}_0)/(\frac{\alpha_t}{\beta_t} + \frac{1}{1 - \bar{\alpha}_{t-1}}) 
= \frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t} \mathbf{x}_t + \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1 - \bar{\alpha}_t} \mathbf{x}_0\\
\end{aligned}
$$

多亏[良好性质](#nice)，我们可以表示 $$\mathbf{x}_0 = \frac{1}{\sqrt{\bar{\alpha}_t}}(\mathbf{x}_t - \sqrt{1 - \bar{\alpha}_t}\mathbf{z}_t)$$ 并代入上式得到：

$$
\begin{aligned}
\tilde{\boldsymbol{\mu}}_t
&= \frac{\sqrt{\alpha_t}(1 - \bar{\alpha}_{t-1})}{1 - \bar{\alpha}_t} \mathbf{x}_t + \frac{\sqrt{\bar{\alpha}_{t-1}}\beta_t}{1 - \bar{\alpha}_t} \frac{1}{\sqrt{\bar{\alpha}_t}}(\mathbf{x}_t - \sqrt{1 - \bar{\alpha}_t}\mathbf{z}_t) \\
&= \color{cyan}{\frac{1}{\sqrt{\alpha_t}} \Big( \mathbf{x}_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \mathbf{z}_t \Big)}
\end{aligned}
$$

如图 2 所示，这一设定与 [VAE](https://lilianweng.github.io/posts/2018-08-12-vae/) 非常相似，因此我们可以用变分下界优化负对数似然。

$$
\begin{aligned}
- \log p_\theta(\mathbf{x}_0) 
&\leq - \log p_\theta(\mathbf{x}_0) + D_\text{KL}(q(\mathbf{x}_{1:T}\vert\mathbf{x}_0) \| p_\theta(\mathbf{x}_{1:T}\vert\mathbf{x}_0) ) \\
&= -\log p_\theta(\mathbf{x}_0) + \mathbb{E}_{\mathbf{x}_{1:T}\sim q(\mathbf{x}_{1:T} \vert \mathbf{x}_0)} \Big[ \log\frac{q(\mathbf{x}_{1:T}\vert\mathbf{x}_0)}{p_\theta(\mathbf{x}_{0:T}) / p_\theta(\mathbf{x}_0)} \Big] \\
&= -\log p_\theta(\mathbf{x}_0) + \mathbb{E}_q \Big[ \log\frac{q(\mathbf{x}_{1:T}\vert\mathbf{x}_0)}{p_\theta(\mathbf{x}_{0:T})} + \log p_\theta(\mathbf{x}_0) \Big] \\
&= \mathbb{E}_q \Big[ \log \frac{q(\mathbf{x}_{1:T}\vert\mathbf{x}_0)}{p_\theta(\mathbf{x}_{0:T})} \Big] \\
\text{Let }L_\text{VLB} 
&= \mathbb{E}_{q(\mathbf{x}_{0:T})} \Big[ \log \frac{q(\mathbf{x}_{1:T}\vert\mathbf{x}_0)}{p_\theta(\mathbf{x}_{0:T})} \Big] \geq - \mathbb{E}_{q(\mathbf{x}_0)} \log p_\theta(\mathbf{x}_0)
\end{aligned}
$$

用 Jensen 不等式也能直接得到同样结果。设我们想最小化交叉熵作为学习目标，

$$
\begin{aligned}
L_\text{CE}
&= - \mathbb{E}_{q(\mathbf{x}_0)} \log p_\theta(\mathbf{x}_0) \\
&= - \mathbb{E}_{q(\mathbf{x}_0)} \log \Big( \int p_\theta(\mathbf{x}_{0:T}) d\mathbf{x}_{1:T} \Big) \\
&= - \mathbb{E}_{q(\mathbf{x}_0)} \log \Big( \int q(\mathbf{x}_{1:T} \vert \mathbf{x}_0) \frac{p_\theta(\mathbf{x}_{0:T})}{q(\mathbf{x}_{1:T} \vert \mathbf{x}_{0})} d\mathbf{x}_{1:T} \Big) \\
&= - \mathbb{E}_{q(\mathbf{x}_0)} \log \Big( \mathbb{E}_{q(\mathbf{x}_{1:T} \vert \mathbf{x}_0)} \frac{p_\theta(\mathbf{x}_{0:T})}{q(\mathbf{x}_{1:T} \vert \mathbf{x}_{0})} \Big) \\
&\leq - \mathbb{E}_{q(\mathbf{x}_{0:T})} \log \frac{p_\theta(\mathbf{x}_{0:T})}{q(\mathbf{x}_{1:T} \vert \mathbf{x}_{0})} \\
&= \mathbb{E}_{q(\mathbf{x}_{0:T})}\Big[\log \frac{q(\mathbf{x}_{1:T} \vert \mathbf{x}_{0})}{p_\theta(\mathbf{x}_{0:T})} \Big] = L_\text{VLB}
\end{aligned}
$$

为把方程中的每一项变成可解析计算的，目标可以进一步改写为若干 KL 散度项与熵项的组合（逐步详细过程见 [Sohl-Dickstein et al., 2015](https://arxiv.org/abs/1503.03585) 附录 B）：

$$
\begin{aligned}
L_\text{VLB} 
&= \mathbb{E}_{q(\mathbf{x}_{0:T})} \Big[ \log\frac{q(\mathbf{x}_{1:T}\vert\mathbf{x}_0)}{p_\theta(\mathbf{x}_{0:T})} \Big] \\
&= \mathbb{E}_q \Big[ \log\frac{\prod_{t=1}^T q(\mathbf{x}_t\vert\mathbf{x}_{t-1})}{ p_\theta(\mathbf{x}_T) \prod_{t=1}^T p_\theta(\mathbf{x}_{t-1} \vert\mathbf{x}_t) } \Big] \\
&= \mathbb{E}_q \Big[ -\log p_\theta(\mathbf{x}_T) + \sum_{t=1}^T \log \frac{q(\mathbf{x}_t\vert\mathbf{x}_{t-1})}{p_\theta(\mathbf{x}_{t-1} \vert\mathbf{x}_t)} \Big] \\
&= \mathbb{E}_q \Big[ -\log p_\theta(\mathbf{x}_T) + \sum_{t=2}^T \log \frac{q(\mathbf{x}_t\vert\mathbf{x}_{t-1})}{p_\theta(\mathbf{x}_{t-1} \vert\mathbf{x}_t)} + \log\frac{q(\mathbf{x}_1 \vert \mathbf{x}_0)}{p_\theta(\mathbf{x}_0 \vert \mathbf{x}_1)} \Big] \\
&= \mathbb{E}_q \Big[ -\log p_\theta(\mathbf{x}_T) + \sum_{t=2}^T \log \Big( \frac{q(\mathbf{x}_{t-1} \vert \mathbf{x}_t, \mathbf{x}_0)}{p_\theta(\mathbf{x}_{t-1} \vert\mathbf{x}_t)}\cdot \frac{q(\mathbf{x}_t \vert \mathbf{x}_0)}{q(\mathbf{x}_{t-1}\vert\mathbf{x}_0)} \Big) + \log \frac{q(\mathbf{x}_1 \vert \mathbf{x}_0)}{p_\theta(\mathbf{x}_0 \vert \mathbf{x}_1)} \Big] \\
&= \mathbb{E}_q \Big[ -\log p_\theta(\mathbf{x}_T) + \sum_{t=2}^T \log \frac{q(\mathbf{x}_{t-1} \vert \mathbf{x}_t, \mathbf{x}_0)}{p_\theta(\mathbf{x}_{t-1} \vert\mathbf{x}_t)} + \sum_{t=2}^T \log \frac{q(\mathbf{x}_t \vert \mathbf{x}_0)}{q(\mathbf{x}_{t-1} \vert \mathbf{x}_0)} + \log\frac{q(\mathbf{x}_1 \vert \mathbf{x}_0)}{p_\theta(\mathbf{x}_0 \vert \mathbf{x}_1)} \Big] \\
&= \mathbb{E}_q \Big[ -\log p_\theta(\mathbf{x}_T) + \sum_{t=2}^T \log \frac{q(\mathbf{x}_{t-1} \vert \mathbf{x}_t, \mathbf{x}_0)}{p_\theta(\mathbf{x}_{t-1} \vert\mathbf{x}_t)} + \log\frac{q(\mathbf{x}_T \vert \mathbf{x}_0)}{q(\mathbf{x}_1 \vert \mathbf{x}_0)} + \log \frac{q(\mathbf{x}_1 \vert \mathbf{x}_0)}{p_\theta(\mathbf{x}_0 \vert \mathbf{x}_1)} \Big]\\
&= \mathbb{E}_q \Big[ \log\frac{q(\mathbf{x}_T \vert \mathbf{x}_0)}{p_\theta(\mathbf{x}_T)} + \sum_{t=2}^T \log \frac{q(\mathbf{x}_{t-1} \vert \mathbf{x}_t, \mathbf{x}_0)}{p_\theta(\mathbf{x}_{t-1} \vert\mathbf{x}_t)} - \log p_\theta(\mathbf{x}_0 \vert \mathbf{x}_1) \Big] \\
&= \mathbb{E}_q [\underbrace{D_\text{KL}(q(\mathbf{x}_T \vert \mathbf{x}_0) \parallel p_\theta(\mathbf{x}_T))}_{L_T} + \sum_{t=2}^T \underbrace{D_\text{KL}(q(\mathbf{x}_{t-1} \vert \mathbf{x}_t, \mathbf{x}_0) \parallel p_\theta(\mathbf{x}_{t-1} \vert\mathbf{x}_t))}_{L_{t-1}} \underbrace{- \log p_\theta(\mathbf{x}_0 \vert \mathbf{x}_1)}_{L_0} ]
\end{aligned}
$$

把变分下界损失的各组件分别标记：

$$
\begin{aligned}
L_\text{VLB} &= L_T + L_{T-1} + \dots + L_0 \\
\text{where } L_T &= D_\text{KL}(q(\mathbf{x}_T \vert \mathbf{x}_0) \parallel p_\theta(\mathbf{x}_T)) \\
L_t &= D_\text{KL}(q(\mathbf{x}_t \vert \mathbf{x}_{t+1}, \mathbf{x}_0) \parallel p_\theta(\mathbf{x}_t \vert\mathbf{x}_{t+1})) \text{ for }1 \leq t \leq T-1 \\
L_0 &= - \log p_\theta(\mathbf{x}_0 \vert \mathbf{x}_1)
\end{aligned}
$$

$$L_\text{VLB}$$ 中的每个 KL 项（$$L_0$$ 除外）都比较两个高斯分布，因此可以[闭式计算](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence#Multivariate_normal_distributions)。$$L_T$$ 是常数，训练中可忽略，因为 $$q$$ 没有可学习参数且 $$\mathbf{x}_T$$ 是高斯噪声。[Ho et al. 2020](https://arxiv.org/abs/2006.11239) 用由 $$\mathcal{N}(\mathbf{x}_0; \boldsymbol{\mu}_\theta(\mathbf{x}_1, 1), \boldsymbol{\Sigma}_\theta(\mathbf{x}_1, 1))$$ 导出的独立离散解码器建模 $$L_0$$。

### 训练损失中 $$L_t$$ 的参数化

回忆我们需要学习一个神经网络来近似反向扩散过程中的条件概率分布，$$p_\theta(\mathbf{x}_{t-1} \vert \mathbf{x}_t) = \mathcal{N}(\mathbf{x}_{t-1}; \boldsymbol{\mu}_\theta(\mathbf{x}_t, t), \boldsymbol{\Sigma}_\theta(\mathbf{x}_t, t))$$。我们想训练 $$\boldsymbol{\mu}_\theta$$ 去预测 $$\tilde{\boldsymbol{\mu}}_t = \frac{1}{\sqrt{\alpha_t}} \Big( \mathbf{x}_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \mathbf{z}_t \Big)$$。因为 $$\mathbf{x}_t$$ 在训练时作为输入可用，我们可以改为重参数化高斯噪声项，使其从时间步 $$t$$ 的输入 $$\mathbf{x}_t$$ 预测 $$\mathbf{z}_t$$：

$$
\begin{aligned}
\boldsymbol{\mu}_\theta(\mathbf{x}_t, t) &= \color{cyan}{\frac{1}{\sqrt{\alpha_t}} \Big( \mathbf{x}_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \mathbf{z}_\theta(\mathbf{x}_t, t) \Big)} \\
\text{Thus }\mathbf{x}_{t-1} &= \mathcal{N}(\mathbf{x}_{t-1}; \frac{1}{\sqrt{\alpha_t}} \Big( \mathbf{x}_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \mathbf{z}_\theta(\mathbf{x}_t, t) \Big), \boldsymbol{\Sigma}_\theta(\mathbf{x}_t, t))
\end{aligned}
$$

损失项 $$L_t$$ 被参数化为最小化与 $$\tilde{\boldsymbol{\mu}}$$ 的差异：

$$
\begin{aligned}
L_t 
&= \mathbb{E}_{\mathbf{x}_0, \mathbf{z}} \Big[\frac{1}{2 \| \boldsymbol{\Sigma}_\theta(\mathbf{x}_t, t) \|^2_2} \| \color{blue}{\tilde{\boldsymbol{\mu}}_t(\mathbf{x}_t, \mathbf{x}_0)} - \color{green}{\boldsymbol{\mu}_\theta(\mathbf{x}_t, t)} \|^2 \Big] \\
&= \mathbb{E}_{\mathbf{x}_0, \mathbf{z}} \Big[\frac{1}{2  \|\boldsymbol{\Sigma}_\theta \|^2_2} \| \color{blue}{\frac{1}{\sqrt{\alpha_t}} \Big( \mathbf{x}_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \mathbf{z}_t \Big)} - \color{green}{\frac{1}{\sqrt{\alpha_t}} \Big( \mathbf{x}_t - \frac{\beta_t}{\sqrt{1 - \bar{\alpha}_t}} \boldsymbol{\mathbf{z}}_\theta(\mathbf{x}_t, t) \Big)} \|^2 \Big] \\
&= \mathbb{E}_{\mathbf{x}_0, \mathbf{z}} \Big[\frac{ \beta_t^2 }{2 \alpha_t (1 - \bar{\alpha}_t) \| \boldsymbol{\Sigma}_\theta \|^2_2} \|\mathbf{z}_t - \mathbf{z}_\theta(\mathbf{x}_t, t)\|^2 \Big] \\
&= \mathbb{E}_{\mathbf{x}_0, \mathbf{z}} \Big[\frac{ \beta_t^2 }{2 \alpha_t (1 - \bar{\alpha}_t) \| \boldsymbol{\Sigma}_\theta \|^2_2} \|\mathbf{z}_t - \mathbf{z}_\theta(\sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t}\mathbf{z}_t, t)\|^2 \Big] 
\end{aligned}
$$

#### 简化

经验上，[Ho et al. (2020)](https://arxiv.org/abs/2006.11239) 发现用忽略权重项的简化目标训练扩散模型效果更好：

$$
L_t^\text{simple} = \mathbb{E}_{\mathbf{x}_0, \mathbf{z}_t} \Big[\|\mathbf{z}_t - \mathbf{z}_\theta(\sqrt{\bar{\alpha}_t}\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_t}\mathbf{z}_t, t)\|^2 \Big]
$$

最终简化目标为：

$$
L_\text{simple} = L_t^\text{simple} + C
$$

其中 $$C$$ 是不依赖 $$\theta$$ 的常数。

![DDPM algorithm](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/DDPM-algo.png)

图 4. DDPM 中的训练与采样算法（图片来源：[Ho et al. 2020](https://arxiv.org/abs/2006.11239)）

#### 与噪声条件分数网络（NCSN）的联系

[Song & Ermon (2019)](https://arxiv.org/abs/1907.05600) 提出了基于分数的生成建模方法：用分数匹配估计的数据分布梯度，经[朗之万动力学](#connection-with-stochastic-gradient-langevin-dynamics)产生样本。每个样本 $$\mathbf{x}$$ 密度概率的分数定义为其梯度 $$\nabla_{\mathbf{x}} \log p(\mathbf{x})$$。训练一个分数网络 $$s_\theta: \mathbb{R}^D \to \mathbb{R}^D$$ 来估计它。为了在深度学习场景下对高维数据可扩展，他们提出用*去噪分数匹配*（向数据加预先指定的小噪声；[Vincent, 2011](http://www.iro.umontreal.ca/~vincentp/Publications/smdae_techreport.pdf)）或*切片分数匹配*（用随机投影；[Yang et al., 2019](https://arxiv.org/abs/1905.07088)）。

回忆朗之万动力学可以只用分数 $$\nabla_{\mathbf{x}} \log p(\mathbf{x})$$ 在迭代过程中从概率密度分布采样数据点。

然而按流形假设，尽管观测数据可能看起来任意高维，大部分数据预期集中在低维流形上。这给分数估计带来负面影响，因为数据点无法覆盖整个空间。在数据密度低的区域，分数估计不那么可靠。向数据加入小高斯噪声使扰动后的数据分布覆盖全空间 $$\mathbb{R}^D$$ 后，分数估计网络的训练变得更稳定。[Song & Ermon (2019)](https://arxiv.org/abs/1907.05600) 进一步改进：用*不同等级*的噪声扰动数据，并训练噪声条件分数网络来*联合*估计不同噪声等级下所有扰动数据的分数。

递增噪声等级的调度与前向扩散过程相似。

### $$\beta_t$$ 的参数化

[Ho et al. (2020)](https://arxiv.org/abs/2006.11239) 把前向方差设为线性递增的常数序列，从 $$\beta_1=10^{-4}$$ 到 $$\beta_T=0.02$$。相对 $$[-1, 1]$$ 之间归一化的图像像素值，它们相当小。其实验中的扩散模型样本质量很高，但模型对数似然仍无法与其他生成模型竞争。

[Nichol & Dhariwal (2021)](https://arxiv.org/abs/2102.09672) 提出若干改进技术帮助扩散模型获得更低 NLL。其中一项是使用基于余弦的方差调度。调度函数的选择可以是任意的，只要它在训练过程中期提供近似线性的下降，并在 $$t=0$$ 和 $$t=T$$ 附近变化细微。

$$
\beta_t = \text{clip}(1-\frac{\bar{\alpha}_t}{\bar{\alpha}_{t-1}}, 0.999) \quad\bar{\alpha}_t = \frac{f(t)}{f(0)}\quad\text{where }f(t)=\cos\Big(\frac{t/T+s}{1+s}\cdot\frac{\pi}{2}\Big)
$$

其中小偏移 $$s$$ 用于防止 $$\beta_t$$ 在接近 $$t=0$$ 时过小。

![betas](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/diffusion-beta.png)

图 5. 训练中 $$\beta_t$$ 的线性与余弦调度对比。（图片来源：[Nichol & Dhariwal, 2021](https://arxiv.org/abs/2102.09672)）

### 反向过程方差 $$\boldsymbol{\Sigma}_\theta$$ 的参数化

[Ho et al. (2020)](https://arxiv.org/abs/2006.11239) 选择把 $$\beta_t$$ 固定为常数而非可学习，并设 $$\boldsymbol{\Sigma}_\theta(\mathbf{x}_t, t) = \sigma^2_t \mathbf{I}$$，其中 $$\sigma_t$$ 不学习而是设为 $$\beta_t$$ 或 $$\tilde{\beta}_t = \frac{1 - \bar{\alpha}_{t-1}}{1 - \bar{\alpha}_t} \cdot \beta_t$$。因为他们发现学习对角方差 $$\boldsymbol{\Sigma}_\theta$$ 导致训练不稳定、样本质量更差。

[Nichol & Dhariwal (2021)](https://arxiv.org/abs/2102.09672) 提出通过模型预测混合向量 $$\mathbf{v}$$，把 $$\boldsymbol{\Sigma}_\theta(\mathbf{x}_t, t)$$ 学为 $$\beta_t$$ 与 $$\tilde{\beta}_t$$ 之间的插值：

$$
\boldsymbol{\Sigma}_\theta(\mathbf{x}_t, t) = \exp(\mathbf{v} \log \beta_t + (1-\mathbf{v}) \log \tilde{\beta}_t)
$$

然而简化目标 $$L_\text{simple}$$ 不依赖 $$\boldsymbol{\Sigma}_\theta$$。为加入依赖，他们构造混合目标 $$L_\text{hybrid} = L_\text{simple} + \lambda L_\text{VLB}$$，其中 $$\lambda=0.001$$ 很小，并在 $$L_\text{VLB}$$ 项中对 $$\boldsymbol{\mu}_\theta$$ 做停止梯度，使 $$L_\text{VLB}$$ 只引导 $$\boldsymbol{\Sigma}_\theta$$ 的学习。经验上他们观察到 $$L_\text{VLB}$$ 相当难优化，很可能是梯度有噪，因此提出用带重要性采样的时间平均平滑版 $$L_\text{VLB}$$。

![Improved DDPM](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/improved-DDPM-nll.png)

图 6. 改进 DDPM 与其他基于似然的生成模型的负对数似然对比。NLL 以 bits/dim 为单位。（图片来源：[Nichol & Dhariwal, 2021](https://arxiv.org/abs/2102.09672)）

## 加速扩散模型采样

按反向扩散过程的马尔可夫链从 DDPM 生成一个样本非常慢，因为 $$T$$ 可达一千或几千步。[Song et al. 2020](https://arxiv.org/abs/2010.02502) 的一个数据点："例如，在 Nvidia 2080 Ti GPU 上，从 DDPM 采样 5 万张 32 × 32 图像约需 20 小时，而 GAN 不到一分钟。"

一个简单方法是运行跨步采样调度（[Nichol & Dhariwal, 2021](https://arxiv.org/abs/2102.09672)），每 $$\lceil T/S \rceil$$ 步做一次采样更新，把过程从 $$T$$ 步减到 $$S$$ 步。生成的新采样调度为 $$\{\tau_1, \dots, \tau_S\}$$，其中 $$\tau_1 < \tau_2 < \dots <\tau_S \in [1, T]$$ 且 $$S < T$$。

另一个方法：依据[良好性质](#nice)，把 $$q_\sigma(\mathbf{x}_{t-1} \vert \mathbf{x}_t, \mathbf{x}_0)$$ 改写为用期望标准差 $$\sigma_t$$ 参数化：

$$
\begin{aligned}
\mathbf{x}_{t-1} 
&= \sqrt{\bar{\alpha}_{t-1}}\mathbf{x}_0 +  \sqrt{1 - \bar{\alpha}_{t-1}}\mathbf{z}_{t-1} \\
&= \sqrt{\bar{\alpha}_{t-1}}\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_{t-1} - \sigma_t^2} \mathbf{z}_t + \sigma_t\mathbf{z} \\
&= \sqrt{\bar{\alpha}_{t-1}}\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_{t-1} - \sigma_t^2} \frac{\mathbf{x}_t - \sqrt{\bar{\alpha}_t}\mathbf{x}_0}{\sqrt{1 - \bar{\alpha}_t}} + \sigma_t\mathbf{z} \\
q_\sigma(\mathbf{x}_{t-1} \vert \mathbf{x}_t, \mathbf{x}_0)
&= \mathcal{N}(\mathbf{x}_{t-1}; \sqrt{\bar{\alpha}_{t-1}}\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_{t-1} - \sigma_t^2} \frac{\mathbf{x}_t - \sqrt{\bar{\alpha}_t}\mathbf{x}_0}{\sqrt{1 - \bar{\alpha}_t}}, \sigma_t^2 \mathbf{I})
\end{aligned}
$$

回忆 $$q(\mathbf{x}_{t-1} \vert \mathbf{x}_t, \mathbf{x}_0) = \mathcal{N}(\mathbf{x}_{t-1}; \tilde{\boldsymbol{\mu}}(\mathbf{x}_t, \mathbf{x}_0), \tilde{\beta}_t \mathbf{I})$$，因此有：

$$
\tilde{\beta}_t = \sigma_t^2 = \frac{1 - \bar{\alpha}_{t-1}}{1 - \bar{\alpha}_t} \cdot \beta_t
$$

设 $$\sigma_t^2 = \eta \cdot \tilde{\beta}_t$$，这样我们可以调整 $$\eta \in \mathbb{R}^+$$ 作为控制采样随机性的超参数。$$\eta = 0$$ 的特例使采样过程*确定*。这样的模型被命名为*去噪扩散隐式模型（denoising diffusion implicit model，DDIM*；[Song et al., 2020](https://arxiv.org/abs/2010.02502)）。DDIM 有相同的边缘噪声分布，但把噪声确定性地映射回原始数据样本。

生成期间，我们只采样 $$S$$ 个扩散步的子集 $$\{\tau_1, \dots, \tau_S\}$$，推理过程变为：

$$
q_{\sigma, \tau}(\mathbf{x}_{\tau_{i-1}} \vert \mathbf{x}_{\tau_t}, \mathbf{x}_0)
= \mathcal{N}(\mathbf{x}_{\tau_{i-1}}; \sqrt{\bar{\alpha}_{t-1}}\mathbf{x}_0 + \sqrt{1 - \bar{\alpha}_{t-1} - \sigma_t^2} \frac{\mathbf{x}_{\tau_i} - \sqrt{\bar{\alpha}_t}\mathbf{x}_0}{\sqrt{1 - \bar{\alpha}_t}}, \sigma_t^2 \mathbf{I})
$$

虽然实验中所有模型都用 $$T=1000$$ 个扩散步训练，他们观察到 DDIM（$$\eta=0$$）在 $$S$$ 小时能产生最佳质量样本，而 DDPM（$$\eta=1$$）在小 $$S$$ 时差得多。当我们能负担完整反向马尔可夫扩散步（$$S=T=1000$$）时，DDPM 确实更好。有了 DDIM，可以用任意多前向步训练扩散模型，但生成过程只从步的子集采样。

![DDIM](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/DDIM-results.png)

图 7. 不同设定扩散模型在 CIFAR10 和 CelebA 数据集上的 FID 分数，包括 $$\color{cyan}{\text{DDIM}}$$（$$\eta=0$$）与 $$\color{orange}{\text{DDPM}}$$（$$\hat{\sigma}$$）。（图片来源：[Song et al., 2020](https://arxiv.org/abs/2010.02502)）

与 DDPM 相比，DDIM 能够：

1. 用少得多的步数生成更高质量的样本。
2. 具有"一致性"性质，因为生成过程是确定性的——以同一潜变量为条件的多个样本应有相似的高层特征。
3. 得益于一致性，DDIM 可以在潜变量中做语义上有意义的插值。

## 条件生成

在 ImageNet 数据上训练生成模型时，通常要生成以类别标签为条件的样本。为把类别信息显式纳入扩散过程，[Dhariwal & Nichol (2021)](https://arxiv.org/abs/2105.05233) 在带噪图像 $$\mathbf{x}_t$$ 上训练了一个分类器 $$f_\phi(y \vert \mathbf{x}_t, t)$$，并用梯度 $$\nabla_\mathbf{x} \log f_\phi(y \vert \mathbf{x}_t, t)$$ 引导扩散采样过程朝目标类别标签 $$y$$ 进行。他们的*消融扩散模型（ablated diffusion model，ADM）*以及带额外分类器引导的版本（**ADM-G**）取得了比 SOTA 生成模型（如 BigGAN）更好的结果。

![Conditioned DDPM](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/conditioned-DDPM.png)

图 8. 用分类器引导以 DDPM 和 DDIM 运行条件生成的算法。（图片来源：[Dhariwal & Nichol, 2021](https://arxiv.org/abs/2105.05233)）]

此外，通过对 UNet 架构的一些修改，[Dhariwal & Nichol (2021)](https://arxiv.org/abs/2105.05233) 展示了扩散模型优于 GAN 的性能。架构修改包括：更大的模型深度/宽度、更多注意力头、多分辨率注意力、用于上/下采样的 BigGAN 残差块、残差连接按 $$1/\sqrt{2}$$ 重缩放，以及自适应组归一化（AdaGN）。

## 快速总结

- **优点**：可解性与灵活性是生成建模中两个相互冲突的目标。可解的模型能被解析评估并廉价拟合数据（如通过高斯或拉普拉斯），但它们无法轻易描述丰富数据集中的结构。灵活的模型能拟合数据中的任意结构，但评估、训练或从这些模型采样通常昂贵。扩散模型既解析可解又灵活。

- **缺点**：扩散模型依赖长马尔可夫链的扩散步骤来生成样本，因此时间和计算上可能相当昂贵。已有新方法使过程快得多，但采样仍慢于 GAN。

---
引用格式：
```
@article{weng2021diffusion,
  title   = "What are diffusion models?",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2021",
  url     = "https://lilianweng.github.io/lil-log/2021/07/11/diffusion-models.html"
}
```

## 参考文献

[1] Jascha Sohl-Dickstein et al. ["Deep Unsupervised Learning using Nonequilibrium Thermodynamics."](https://arxiv.org/abs/1503.03585) ICML 2015.

[2] Max Welling & Yee Whye Teh. ["Bayesian learning via stochastic gradient langevin dynamics."](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.226.363) ICML 2011.

[3] Yang Song & Stefano Ermon. ["Generative modeling by estimating gradients of the data distribution."](https://arxiv.org/abs/1907.05600) NeurIPS 2019.

[4] Yang Song & Stefano Ermon. ["Improved techniques for training score-based generative models."](https://arxiv.org/abs/2006.09011)  NeuriPS 2020.

[5] Jonathan Ho et al. ["Denoising diffusion probabilistic models."](https://arxiv.org/abs/2006.11239) arxiv Preprint arxiv:2006.11239 (2020). [[code](https://github.com/hojonathanho/diffusion)]

[6] Jiaming Song et al. ["Denoising diffusion implicit models."](https://arxiv.org/abs/2010.02502) arxiv Preprint arxiv:2010.02502 (2020). [[code](https://github.com/ermongroup/ddim)]

[7] Alex Nichol & Prafulla Dhariwal. [" Improved denoising diffusion probabilistic models"](https://arxiv.org/abs/2102.09672) arxiv Preprint arxiv:2102.09672 (2021). [[code](https://github.com/openai/improved-diffusion)]

[8] Prafula Dhariwal & Alex Nichol. ["Diffusion Models Beat GANs on Image Synthesis."](https://arxiv.org/abs/2105.05233) arxiv Preprint arxiv:2105.05233 (2021). [[code](https://github.com/openai/guided-diffusion)]
