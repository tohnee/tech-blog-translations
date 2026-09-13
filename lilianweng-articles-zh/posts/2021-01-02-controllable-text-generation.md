---
title: "可控神经文本生成"
title_en: "Controllable Neural Text Generation"
source: https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/
crawled: 2026-09-08
translated: 2026-09-08
---

# 可控神经文本生成

> 原文：[Controllable Neural Text Generation](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/) · Lilian Weng（翁荔）

> 在众多 NLP 任务上取得 SOTA 结果的现代语言模型是在互联网大规模自由文本上训练的。要引导这样的模型生成具有期望属性的内容颇具挑战。尽管尚不完美，可控文本生成已有若干方法，如引导式或可学习的解码策略、聪明的提示设计，或用各种方法微调模型。

<span style="color: #286ee0;">[更新于 2021-02-01：更新至 2.0 版，补充若干工作并修正大量笔误。]</span>
<br />
<span style="color: #286ee0;">[更新于 2021-05-26：在["提示设计"](#gradient-based-search)一节新增 P-tuning 与 Prompt Tuning。]</span>
<br />
<span style="color: #286ee0;">[更新于 2021-09-19：新增["非似然训练"](##unlikelihood-training)。]</span>

网络上有海量自由文本，比标注基准数据集多几个数量级。最先进的语言模型（LM）用大规模无监督 Web 数据训练。通过迭代采样下一个 token 从 LM 生成样本时，我们对输出文本的属性（如主题、风格、情感等）没有太多控制。许多应用要求对模型输出的良好控制。例如，若我们打算用 LM 为孩子生成阅读材料，我们会希望引导输出的故事安全、有教育意义且易于儿童理解。

如何引导一个强大的无条件语言模型？本文将深入探讨用无条件语言模型做受控内容生成的几种方法。
注意，模型可操控性（steerability）仍是一个开放的研究问题。介绍的每种方法都各有优劣。

1. 应用引导式解码策略，在测试时选择期望的输出。
2. 通过良好的提示设计优化出最期望的结果。
3. 微调基础模型或可操控层，做条件内容生成。

以下讨论中，假设我们有一个预训练的生成式语言模型 $$p_\theta$$。该模型通过优化下一 token 预测学到了 token 序列上的分布：$$ \mathcal{L}_\text{ML} = - \sum_t \log p_\theta(x_t \vert x_{<t}) $$。

## 解码策略

通过采用不同的解码方法，我们可以在采样过程上施加限制或偏好，在不修改任何模型权重的情况下改变生成样本。尽管解码策略不改变任何可训练参数的取值，它仍是相当重要的组件。

### 常见解码方法

由于模型最后一层预测词表空间上的 logits $$o$$，下一个 token 可通过施加带温度 $$T$$ 的 softmax 采样。采样第 $$i$$ 个 token 的概率为

$$
p_i \propto \frac{\exp(o_i / T)}{\sum_j \exp(o_j/T)}
$$

低温使分布更尖锐，高温使它更平缓。

**贪婪搜索**：总是选择概率*最高*的下一个 token，等价于温度 $$T=0$$。然而它容易产生短语重复，即使对训练良好的模型亦然。

**束搜索**：本质上是每层树一个 token 的广度优先搜索，但带宽有限。在搜索树的每一层，束搜索跟踪 $$n$$ 个（称"束宽"）最佳候选并在下一层展开这些候选的所有后继。束搜索在命中 EOS（句尾）token 时可停止展开某节点。

然而，基于最大化的解码并不保证高质量生成。

<a name="beam-search-surprise" />
![Beam search probability](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/beam_search_less_surprising.png)

*图 1：束搜索与人类对下一个 token 分配的概率。人类所选 token 的预测概率方差大得多，因而更出人意料。（图片来源：[Holtzman et al. 2019](https://arxiv.org/abs/1904.09751)）*

**Top-k 采样**（[Fan et al., 2018](https://arxiv.org/abs/1805.04833)）：每个采样步只选出前 $$k$$ 个最可能的 token，概率质量在其中重新分配。[Fan et al., 2018](https://arxiv.org/abs/1805.04833) 提出*top-k 随机采样*：下一个 token 从前 $$k$$ 个最可能候选中随机选取，他们论证该方法比束搜索能生成更新颖、更少重复的内容。

**核采样（Nucleus sampling**，[Holtzman et al. 2019](https://arxiv.org/abs/1904.09751)）：也称 "Top-p 采样"。top-k 采样的一个缺点是预定义的数 $$k$$ 没有考虑概率分布可能有多*倾斜*。核采样选取累积概率超过阈值（如 0.95）的最小顶部候选集，然后在所选候选中重新缩放分布。

超参数得当时，top-k 与核采样的重复都更少。

**惩罚采样（Penalized sampling**，[Keskar et al. 2019](https://arxiv.org/abs/1909.05858)）：为避免生成重复子串这一常见失败情形，[CTRL](https://arxiv.org/abs/1909.05858) 论文提出一种新采样方法，通过折扣先前已生成 token 的分数来惩罚重复。带重复惩罚的下一 token 概率分布定义为：

$$
p_i = \frac{\exp(o_i / (T \cdot \mathbb{1}(i \in g)))}{\sum_j \exp(o_j / (T \cdot \mathbb{1}(j \in g)))} \quad
\mathbb{1}(c) = \theta \text{ if the condition }c\text{ is True else }1
$$

其中 $$g$$ 包含一组先前生成的 token，$$\mathbb{1}(.)$$ 是恒等函数。$$\theta=1.2$$ 被发现在少重复与忠实生成之间取得良好平衡。

### 引导式解码

上述所有标准解码策略都按预测概率采样 token，没有额外信息。我们关于主题或情感的偏好可以写进候选排序函数，通过改变候选排序分数来引导样本生成。每个解码步 token 选择的排序分数可设为 LM 对数似然与一组期望特征判别器的组合。特征通过启发式（[Ghazvininejad et al., 2017](https://www.aclweb.org/anthology/P17-4008/)）、监督学习（[Holtzman et al., 2018](https://arxiv.org/abs/1805.06087)）或 RL（[Li et al., 2017](https://arxiv.org/abs/1701.06549)）设计以量化人类偏好。

[Ghazvininejad et al. (2017)](https://www.aclweb.org/anthology/P17-4008/) 构建了一个名为 "Hafez" 的系统，通过在解码步调整束搜索中的采样权重，以期望风格生成诗歌。第 $$t$$ 步下一个 token $$x_{t+1}$$ 的采样似然由一个评分函数增强：

$$
\text{score}(x_{t+1}, b_t) = \text{score}(b_t) + \log p(x_{t+1}) + \color{green}{\sum_i \alpha_i f_i(x_{t+1})}
$$

其中 $$\log p(x_{t+1})$$ 是 LM 预测的对数似然。$$\text{score}(b_t)$$ 是当前束状态 $$b_t$$ 中已生成词的累计分数。绿色部分可以纳入许多不同的特征来引导输出风格。一组特征函数 $$f_i(.)$$ 定义偏好，相关权重 $$alpha_i$$ 像"控制旋钮"，可在解码时轻松定制。特征可以度量多种属性且易于组合；例如：
- $$x_{t+1}$$ 是否存在于期望或禁止的主题词袋中。
- $$x_{t+1}$$ 是否指示特定情感。
- $$x_{t+1}$$ 是否为重复 token（因此 $$f_i$$ 也需要以历史为输入）。
- 若特别偏好更长或更短的词，$$x_{t+1}$$ 的长度。

类似 Hafez，[Baheti et al. (2018)](https://arxiv.org/abs/1809.01215) 手工设计排序特征，通过附加上下文与补全的主题分布或嵌入间的相似度分数来改变采样分布。

[Holtzman et al. (2018)](https://arxiv.org/abs/1805.06087) 采用一组学到的判别器，各自专注一条受[格赖斯准则](https://en.wikipedia.org/wiki/Cooperative_principle)引导的交流原则：质量、数量、关联与方式。判别器分别通过度量重复、蕴含、相关性与词汇多样性来学习编码这些期望原则。给定一些真实补全，所有判别器模型被训练来最小化排序对数似然 $$\log\sigma(f_i(y_g) - f_i(y))$$，因为金标准续写 $$y_g$$ 应比生成的 $$y$$ 得到更高分数。这里权重系数 $$\alpha_i$$ 也被学习以最小化金标准与生成补全之间的分数差。判别对抗搜索（Discriminative Adversarial Search，DAS；[Scialom et al., 2020](https://arxiv.org/abs/2002.10375)）受 GAN 启发，训练判别器区分人类创作文本与机器生成文本。判别器为每个 token 而非整个序列预测标签。判别器对数概率被加进分数，引导采样朝人类书写风格进行。

[Meister et al. (2020)](https://arxiv.org/abs/2010.02650) 在正则化解码框架中研究束搜索：

$$
\mathbf{y}^* = \arg\max_{\mathbf{y}\in\mathcal{Y}} \big( \underbrace{\log p_\theta(\mathbf{y}\vert\mathbf{x})}_\text{MAP} - \underbrace{\lambda\mathcal{R}(\mathbf{y})}_\text{regularizer} \big)
$$

由于我们期望最大概率意味着最小意外，LM 在时间步 $$t$$ 的意外度（surprisal）可定义如下：

$$
\begin{aligned}
u_0(\texttt{BOS}) &= 0 \text{  ; BOS is a placeholder token for the beginning of a sentence.}\\
u_t(y) &= -\log P_\theta(y \vert \mathbf{x}, \mathbf{y}_{<t}) \text{ for }t \geq 1
\end{aligned}
$$

MAP（最大后验）部分要求给定上下文概率最大的序列，正则项引入其他约束。全局最优策略可能偶尔需要一个高意外度步骤，以便缩短输出长度或在之后产生更多低意外度步骤。

束搜索在 NLP 领域经受了时间考验。问题是：*若想把束搜索建模为正则化解码框架中的精确搜索，$$\mathcal{R}(\mathbf{y})$$ 应如何建模？* 论文提出了束搜索与*均匀信息密度（uniform information density，UID）*假设之间的联系。

> "均匀信息密度假设（UID；Levy and Jaeger, 2007）陈述：在语法的约束下，人类偏好把信息（信息论意义上）均匀分布到语言信号（如一个句子）上的句子。"

换言之，它假设人类偏好意外度均匀分布的文本。top-k 采样或核采样这类流行解码方法实际上过滤掉了高意外度选项，从而隐式鼓励输出序列的 UID 性质。

论文实验了若干形式的正则项：

1. *贪婪*：$$\mathcal{R}_\text{greedy}(\mathbf{y}) = \sum_{t=1}^{\vert\mathbf{y}\vert} \big(u_t(y_t) - \min_{y' \in \mathcal{V}} u_t(y') \big)^2$$；若设 $$\lambda \to \infty$$，得到贪婪搜索。注意逐步贪婪不保证全局最优。
2. *方差正则项*：$$\mathcal{R}_\text{var}(\mathbf{y}) = \frac{1}{\vert\mathbf{y}\vert}\sum_{t=1}^{\vert\mathbf{y}\vert} \big(u_t(y_t) - \bar{u} \big)^2$$，其中 $$\bar{u}$$ 是所有时间步的平均意外度。它直接编码 UID 假设。
3. *局部一致性*：$$\mathcal{R}_\text{local}(\mathbf{y}) = \frac{1}{\vert\mathbf{y}\vert}\sum_{t=1}^{\vert\mathbf{y}\vert} \big(u_t(y_t) - u_{t-1}(y_{t-1}) \big)^2$$；该解码正则项鼓励相邻 token 意外度相近。
4. *最大值正则项*：$$\mathcal{R}_\text{max}(\mathbf{y}) = \max_t u_t(y_t)$$ 惩罚意外度的最大补偿。
5. *平方正则项*：$$\mathcal{R}_\text{square}(\mathbf{y}) = \sum_{t=1}^{\vert\mathbf{y}\vert} u_t(y_t)^2$$ 鼓励所有 token 的意外度接近 0。

带贪婪正则项的实验表明，更大的 $$\lambda$$ 带来更好的性能（如 NMT 任务用 BLEU 度量）和更低的意外度标准差。

![Greedy regularizer](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/beam-search-greedy-regularizer.png)

*图 2：BLEU 与意外度标准差作为正则强度 $$\lambda$$ 的函数图像。灰色子图显示 BLEU 与意外度标准差的关系。（图片来源：[Meister et al. 2020](https://arxiv.org/abs/2010.02650)）*

束宽增大时，默认束搜索的文本生成质量下降。正则化束搜索极大缓解了该问题。组合正则项进一步提升性能。他们的 NMT 实验发现，贪婪 $$\lambda=5$$ 与平方 $$\lambda=2$$ 是最优组合正则项。

![Beam search size](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/beam-search-size-regularized.png)

*图 3：BLEU 作为束宽的函数图像（左）与不同正则化解码策略产生的翻译的 BLEU 分数。（图片来源：[Meister et al. 2020](https://arxiv.org/abs/2010.02650)）*

引导式解码本质上是运行一次更昂贵的束搜索，其采样概率分布被关于人类偏好的边信息改变。

### 可训练解码

给定一个训练好的语言模型，[Gu et al (2017)](https://arxiv.org/abs/1702.02429) 提出了**可训练贪婪解码（trainable greedy decoding）**算法，为采样序列最大化任意目标。该想法基于*噪声并行近似解码（noisy, parallel approximate decoding，[NPAD](https://arxiv.org/abs/1605.03835)）*。NPAD 向模型隐藏状态注入非结构化噪声并并行运行多次带噪解码以避免潜在退化。更进一步，可训练贪婪解码用可学习的随机变量替换非结构化噪声——由一个以先前隐藏状态、先前解码 token 和上下文为输入的 RL 智能体预测。换言之，解码算法学习一个 RL actor 来操纵模型隐藏状态以获得更好结果。

[Grover et al. (2019)](https://arxiv.org/abs/1906.09531) 训练一个二元分类器区分来自数据分布的样本与来自生成模型的样本。该分类器用于估计构造新未归一化分布的*重要性权重*。所提策略称为**免似然重要性加权（likelihood-free importance weighting，LFIW）**。

设 $$p$$ 为真实数据分布，$$p_\theta$$ 为学到的生成模型。用来自 $$p_\theta$$ 的样本评估给定函数 $$f$$ 在 $$p$$ 下期望的经典方法是重要性采样。

$$
\mathbb{E}_{\mathbf{x}\sim p} [f(\mathbf{x})] 
= \mathbb{E}_{\mathbf{x}\sim p_\theta} \Big[\frac{p(\mathbf{x})}{p_\theta(\mathbf{x})} f(\mathbf{x})\Big]
\approx \frac{1}{N} \sum_{i=1}^N w(\mathbf{x}_i)f(\mathbf{x}_i)
$$

然而 $$p(\mathbf{x})$$ 只能通过有限数据集估计。设 $$c_\phi: \mathcal{X} \to [0,1]$$ 为预测样本 $$\mathbf{x}$$ 是否来自真实数据分布（$$y=1$$）的概率二元分类器。$$\mathcal{X}\times\mathcal{Y}$$ 上的联合分布记为 $$q(\mathbf{x}, y)$$。

$$
q(\mathbf{x}\vert y) = \begin{cases}
p_\theta(\mathbf{x}) & \text{ if }y=0\text{; predicted to be generated data} \\
p(\mathbf{x}) & \text{ otherwise; from the true data distribution}
\end{cases}
$$

若 $$c_\phi$$ 是[贝叶斯最优](https://svivek.com/teaching/lectures/slides/prob-learning/bayes-optimal-classifier.pdf)，重要性权重可估计为：

$$
w_\phi(\mathbf{x}) 
= \frac{p(\mathbf{x})}{p_\theta(\mathbf{x})}
= \frac{q(\mathbf{x} \vert y=1)}{q(\mathbf{x} \vert y=0)}
= \frac{q(y=0)}{q(y=1)} \frac{q(y=1 \vert \mathbf{x})}{q(y=0 \vert \mathbf{x})}
= \gamma \frac{c_\phi(\mathbf{x})}{1 - c_\phi(\mathbf{x})}
$$

其中 $$\gamma = \frac{q(y=0)}{q(y=1)} > 0$$ 是固定的比值。

由于无法学到完美最优的分类器，重要性权重只能是一个估计 $$\hat{w}_\phi$$。可用几个实用技巧抵消分类器利用生成样本中的伪影做出非常自信预测（即非常小的重要性权重）的情形：

1. 自归一化：以总和归一化权重 $$\hat{w}_\phi(\mathbf{x}_i) / \sum_{j=1}^N \hat{w}_\phi(\mathbf{x}_j)$$。
2. 平滑：加幂缩放参数 $$\alpha > 0$$，$$\hat{w}_\phi(\mathbf{x}_i)^\alpha$$。
3. 截断：指定下界 $$\max(\hat{w}_\phi(\mathbf{x}_i), \beta)$$。

为从重要性重采样的生成模型采样 $$\mathbf{x}\sim p_{\theta, \phi}(\mathbf{x}) \propto p_\theta(\mathbf{x})\hat{w}_\phi(\mathbf{x})$$，他们采用 SIR（Sampling-Importance-Resampling），

![SIR importance resampling](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/SIR-importance-resampling.png)

*图 4：用 SIR 按重要性权重 $$\hat{w}(\mathbf{x}_i)$$ 从生成模型采样的算法。（图片来源：[Grover et al., 2019](https://arxiv.org/abs/1906.09531)）*

[Deng et al., 2020](https://arxiv.org/abs/2004.11714) 提出学习一个 EBM 在[残差空间](https://arxiv.org/abs/1906.03351)引导 LM，$$P_\theta(x) \propto P_\text{LM}(x)\exp(-E_\theta(x))$$，其中 $$P_\theta$$ 是联合模型；$$E_\theta$$ 是待学习的残差能量函数。若知道配分函数 $$Z$$，我们可以把生成序列 $$x_{p+1}, \dots, x_T$$ 的生成模型建模为：

$$
P_\theta(x_{p+1:T}\vert x_{1:p}) = \frac{P_\text{LM}(x_{p+1:T}\vert x_{1:p}) \exp(-E_\theta(x_{1:T}))}{Z_\theta(x_{1:p})}
$$

目标是学习能量函数 $$E_\theta$$ 的参数，使联合模型 $$P_\theta$$ 更接近期望数据分布。残差能量函数用噪声对比估计（[NCE](https://www.kdnuggets.com/2019/07/introduction-noise-contrastive-estimation.html)）训练——把 $$P_\theta$$ 视为模型分布、$$P_\text{LM}$$ 视为噪声分布：

$$
\theta = \arg\max_{\theta} \mathbb{E}_{x^+ \sim P_\text{data}} \log\frac{1}{1+\exp(E_\theta(x^+))} + \mathbb{E}_{x^- \sim P_\text{LM}} \log\frac{1}{1+\exp(-E_\theta(x^-))}
$$

然而配分函数在实践中不可解。论文提出一个简单方法：先从原始 LM 采样，再按能量函数从中重采样。遗憾的是这相当昂贵。

![Top k joint sampling](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/top-k-joint-sampling.png)

*图 5：从基础 LM 取 top-k 样本，再按残差能量函数重采样。（图片来源：[Deng et al., 2020](https://arxiv.org/abs/2004.11714)）*

## 聪明的提示设计

大语言模型已被证明在许多 NLP 任务上非常强大，即使只用*提示*而无任务专属微调（[GPT2](https://lilianweng.github.io/posts/2019-01-31-lm/#gpt-2)、[GPT3](https://lilianweng.github.io/posts/2019-01-31-lm/#gpt-3)）。提示设计对下游任务性能影响巨大且常需耗时的手工打磨。例如，事实性问题在"闭卷考试"中可通过聪明的提示设计大幅提升（[Shin et al., 2020](https://arxiv.org/abs/2010.15980)、[Jiang et al., 2020](https://arxiv.org/abs/1911.12543)）。我期待看到越来越多关于自动聪明提示设计的文献。

### 基于梯度的搜索

**AutoPrompt**（[Shin et al., 2020](https://arxiv.org/abs/2010.15980)；[代码](http://ucinlp.github.io/autoprompt)）是一种通过基于梯度的搜索为各类任务自动创建提示的方法。AutoPrompt 按模板 $$\lambda$$ 把原始任务输入 $$x$$ 与一组触发 token $$x_\text{trig}$$ 组合成提示。触发 token 在所有输入间共享，因此是*普适*有效的。

![AutoPrompt](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/autoprompt.png)

*图 6：AutoPrompt 概览。检索触发 token 以在所有输入上优化目标输出。（图片来源：[Shin et al., 2020](https://arxiv.org/abs/2010.15980)）*

普适触发 token 用与 [Wallace et al., 2019](https://arxiv.org/abs/1908.07125) 相同的梯度引导搜索策略识别。*普适*设定意味着触发 token $$x_\text{trig}$$ 能对数据集的所有输入优化目标输出 $$\tilde{y}$$：

$$
x_\text{trig} = \arg\min_{x’_\text{trig}} \mathbb{E}_{x\sim\mathcal{X}} [\mathcal{L}(\tilde{y}, f(x’_\text{trig}; x))]
$$

搜索在嵌入空间进行。每个触发 token 的嵌入 $$e_{\text{trig}_i}$$ 先初始化为默认值，然后更新以最小化任务专属损失在当前 token 嵌入处的一阶泰勒展开：

$$
e^{(t+1)}_\text{trig} = \arg\min_{e\in\mathcal{V}} [e - e^{(t)}_{\text{trig}_i}]^\top \nabla_{e^{(t)}_{\text{trig}_i}} \mathcal{L}
$$

其中 $$\mathcal{V}$$ 指所有 token 的嵌入矩阵。$$\nabla_{e^{(t)}_{\text{trig}_i}} \mathcal{L}$$ 是第 $$t$$ 次迭代一批数据上任务损失的平均梯度。我们可以用 $$\vert \mathcal{V} \vert d$$ 维点积暴力搜索最优 $$e$$，这很便宜且可并行计算。

![Universal adversarial trigger](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/universal-adv-triggers.png)

*图 7：我们通过用每批任务损失的梯度更新触发 token 的嵌入来搜索触发 token。（图片来源：[Wallace et al., 2019](https://arxiv.org/abs/1908.07125)）*

上述 token 替换方法可结合束搜索。寻找最优 token 嵌入 $$e$$ 时，我们可以选 top-$$k$$ 候选而非单个，从左到右搜索并用当前数据批上的 $$\mathcal{L}$$ 给每个束打分。

![AutoPrompt examples](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/autoprompt-examples.png)

*图 8：AutoPrompt 为不同任务发现的示例提示。（图片来源：[Shin et al., 2020](https://arxiv.org/abs/2010.15980)）*

聪明的提示设计本质上产生能导向期望补全的高效上下文。受此观察启发，[Li & Liang (2021)](https://arxiv.org/abs/2101.00190) 提出 **Prefix-Tuning**：在输入序列开头（称"前缀"）分配少量可训练参数来引导 LM，$$[\text{PREFIX}; x; y]$$。设 $$\mathcal{P}_\text{idx}$$ 为前缀索引集，$$\text{dim}(h_i)$$ 为嵌入大小。前缀参数 $$P_\theta$$ 的维度为 $$\vert\mathcal{P}_\text{idx}\vert \times \text{dim}(h_i) $$，隐藏状态形如：

$$
h_i = \begin{cases}
P_\theta[i,:], & \text{if }i \in \mathcal{P}_\text{idx}\\
\text{LM}_\phi(z_i, h_{<i}), & \text{otherwise}
\end{cases}
$$

注意只有 $$P_\theta$$ 可训练，LM 参数 $$\phi$$ 在训练中冻结。

![Prefix-tuning](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/prefix-tuning.png)

*图 9：微调与 prefix-tuning 对比示意。（图片来源：[Li & Liang 2021](https://arxiv.org/abs/2101.00190)）*

前缀参数不绑定到任何与真实词相关的嵌入，因此在引导上下文方面更有*表达力*。遗憾的是直接优化 $$P_\theta$$ 效果差。为降低高维训练的难度，矩阵 $$P_\theta$$ 被重参数化为更小的矩阵 $$P'_\theta \in \mathbb{R}^{\vert\mathcal{P}_\text{idx}\vert \times c}$$ 和一个大前馈网络 $$\text{MLP}_\theta \in \mathbb{R}^{c\times \text{dim}(h_i)}$$。

性能随前缀长度 $$\vert\mathcal{P}_\text{idx}\vert$$ 增长至某个值，该值随任务而变。

![Prefix-tuning](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/prefix-tuning-length.png)

*图 10：任务性能（左：摘要，右：表到文本）作为前缀长度的函数。（图片来源：[Li & Liang 2021](https://arxiv.org/abs/2101.00190)）*

其消融研究的其他有趣发现包括：
- 只调嵌入层（无前缀）表达力不足。
- 把可训练参数放在 $$x$$ 与 $$y$$ 之间 $$[x; \text{INFIX}; y]$$ 略逊于 prefix-tuning，可能因为它只影响 $$y$$ 的上下文而前缀两者都影响。
- $$P_\theta$$ 随机初始化导致低性能高方差。相比之下，用真实词的激活初始化 $$P_\theta$$ 改进生成，即使这些词与任务无关。

微调模型取得更好的任务性能，但在低数据区间可能失败。AutoPrompt 与 Prefix-Tuning 都被发现于训练集小（即 $$10^2-10^3$$ 样本）的区间优于微调。作为微调的替代，提示设计或学习上下文嵌入便宜得多。AutoPrompt 对情感分类准确率的提升远超手工提示，并取得与线性探查相近的性能。NLI 任务上 AutoPrompt 比线性探查准确率更高。它检索事实也比手工提示更准。低数据区间，Prefix-Tuning 在表到文本生成与摘要上取得与微调相当的性能。

两项后续工作，**P-tuning**（[Liu et al. 2021](https://arxiv.org/abs/2103.10385)；[代码](https://github.com/THUDM/P-tuning)）与 **Prompt Tuning**（[Lester et al. 2021](https://arxiv.org/abs/2104.08691)），沿袭显式训练连续提示嵌入的类似思想，但在可训练参数与架构上有不同选择。与 Prefix-Tuning 在 transformer 每层隐藏状态拼接连续提示 token 不同，P-tuning 与 Prompt Tuning 都非侵入式地*只在输入*加连续提示即可良好工作。

设 $$[P_i]$$ 为 **P-tuning**（[Liu et al. 2021](https://arxiv.org/abs/2103.10385)）提示模板中的第 $$i$$ 个 token，我们可以把提示记为序列 $$T=\{[P_{0:i}], \mathbf{x}, [P_{i+1:m}], \mathbf{y}\}$$。每个 token $$[P_i]$$ 不必是模型词表中的真实 token（"伪 token"），于是编码后的模板 $$T^e$$ 形如下式，伪 token 的隐藏状态可用梯度下降优化。

$$
T^e = \{ h_0, \dots, h_i, \text{embed}(\mathbf{x}), h_{i+1}, \dots, h_m, \text{embed}(\mathbf{y})\}
$$

![P-tuning](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/p-tuning.png)

*图 11：P-tuning 示意图。有时加入少量任务相关锚点 token（如图中 "capital"）可带来进一步提升。（图片来源：[Liu et al. 2021](https://arxiv.org/abs/2103.10385)）*

P-tuning 有两大优化挑战：
1. 离散性：预训练语言模型的词嵌入高度离散。若 $$h_i$$ 随机初始化，难以优化。
2. 关联性：$$h_i$$ 应相互依赖。因此他们开发了一种通过训练轻量 LSTM 提示编码器建模该依赖的机制：

$$
h_i = \text{MLP}([\text{LSTM}(h_{0:i}): \text{LSTM}(h_{i:m})])
$$

P-tuning 比 prefix-tuning 更灵活，因为它在提示中间而不只是开头插入可训练 token。任务专属锚点 token 的使用像是把手工提示工程与可训练提示结合。

**Prompt Tuning**（[Lester et al. 2021](https://arxiv.org/abs/2104.08691)）大幅简化了 prefix tuning 的思想：每个下游任务只允许额外的 $$k$$ 个可调 token 前置于输入文本。条件生成为 $$p_{\theta, \theta_P}(Y \vert [P; X])$$，其中 $$P$$ 是参数 $$\theta_P$$ 可经反向传播训练的"伪提示"。$$X$$ 与 $$P$$ 都是嵌入向量，$$X \in \mathbb{R}^{n \times d^e}, P \in \mathbb{R}^{k \times d^e}$$，$$[P;X] \in \mathbb{R}^{(n+k) \times d^e}$$，其中 $$d^e$$ 是嵌入空间维度。

- 模型变*大*（数十亿参数及以上）时，prompt tuning 产生与模型微调相当的结果。鉴于大模型微调与推理执行都很昂贵，这一结果尤其有趣。
- 带学到的任务专属参数，prompt tuning 在适应新领域时取得更好的迁移学习。它在领域偏移问题上优于微调。
- 他们还展示同一任务多提示的提示集成带来进一步提升。

![Prompt-tuning](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/prompt-tuning.png)

*图 12：Prompt Tuning 工作方式示意。（图片来源：[Lester et al. 2021](https://arxiv.org/abs/2104.08691)）*

实验考察了几种提示初始化方案：
1. 从 [-0.5, 0.5] 均匀采样随机初始化；
2. 采样 top 5000 常见 token 的嵌入；
3. 用类别标签字符串的嵌入值。若没有足够的类别标签初始化软提示，退回方案 2。
随机初始化明显差于另外两种。

![Prompt-tuning-exp1](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/prompt-tuning-exp1.png)

*图 13：(a) 不同提示初始化方案与 (b) 不同提示长度的影响。（图片来源：[Lester et al. 2021](https://arxiv.org/abs/2104.08691)）*

预训练目标对 prompt tuning 质量影响也很大。T5 的"span corruption"在这里不是好选项。

prompt tuning 被发现不太容易过拟合到特定数据集。为评估对数据偏移问题的鲁棒性，他们在某任务的一个数据集上训练模型，在*不同领域*的测试集上评估。prompt tuning 更有韧性，能更好地泛化到不同领域。

![Prompt-tuning-exp2](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/prompt-tuning-exp2.png)

*图 14：prompt tuning 对训练与测试集之间领域偏移更有韧性。（图片来源：[Lester et al. 2021](https://arxiv.org/abs/2104.08691)）*

### 基于启发式的搜索

改写（paraphrasing）是快速探索与已知版本相似提示的方法，可通过*回译*完成。用回译，初始提示被翻译成另一语言的 $$B$$ 个候选，再各自回译为原语言的 $$B$$ 个候选。所得共 $$B^2$$ 个候选按往返概率打分排序。

[Ribeiro et al (2018)](https://www.aclweb.org/anthology/P18-1079/) 通过生成输入 $$x$$ 的多种改写 $$\{x'\}$$ 直至触发目标函数 $$f$$ 的不同预测，识别*语义等价对抗样本（semantically equivalent adversaries，SEA）*：

$$
\begin{aligned}
SEA(x, x') &= \mathbb{1}[\text{SemEq}(x, x') \land f(x) \neq f(x')] \\
\text{where SemEq}(x, x') &= \mathbb{1}[\min\Big(1, \frac{p(x'\vert x)}{p(x\vert x)} \Big) \geq \tau]
\end{aligned}
$$

从 SEA 提取的规则被视为模型中的"bug"。把这些规则作为数据增强应用于模型训练有助于加固模型、修复 bug。

[Jiang et al (2020)](https://arxiv.org/abs/1911.12543) 尝试通过自动发现更好的提示来查询，验证训练好的语言模型是否知道某些知识。在知识检索范围内，事实知识以三元组 $$\langle x, r, y \rangle$$（主体、关系、客体）形式表示。提示可以从训练句子（如维基百科描述）中挖掘或经改写扩展。

有趣的是，提示中的一些小修改可能带来大收益，如图 X 所示。

![Small modifications](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/prompt-small-modifications.png)

*图 15：提示模板的小修改可带来大幅性能提升：蓝色为替换、绿色为插入、红色为删除。（图片来源：[Jiang et al., 2020](https://arxiv.org/abs/1911.12543)）*

## 微调

微调是引导 LM 输出期望内容的直观方式，通常通过在监督数据集上训练或用 RL。我们可以微调模型全部权重，或把微调限制在顶层或附加层。

### 条件训练

条件训练旨在学习以控制变量 $$z$$ 为条件的生成模型 $$p(y \vert x, z)$$。

[Fan et al (2018)](https://arxiv.org/abs/1805.04833) 训练了一个两步故事生成的条件语言模型。首先模型输出故事梗概，然后故事写作模型按梗概创作故事。以梗概为条件的机制由*融合（fusion）*模型架构实现。融合模型实施一种*残差学习*，使故事写作模型专注于学习第一个梗概生成模型所缺少的东西。同样用于故事生成，[Peng et al (2018)](https://www.aclweb.org/anthology/W18-1505/) 实验了以结局效价为条件的故事生成器 LM，$$p(x_t \vert x_{<t}, z)$$，其中 $$z$$ 是故事结局的标签（悲伤、快乐或中性）。其语言模型是双向 LSTM，标签被映射为学到的嵌入并融入 LSTM 单元。

<a name="ctrl" />**CTRL**（[Keskar et al., 2019](https://arxiv.org/abs/1909.05858)；[代码](https://github.com/salesforce/ctrl)）旨在用可控数据集训练一个以控制码 $$z$$ 为条件的语言模型。CTRL 通过在带*控制码前缀*（如 `[horror]`、`[legal]` 等）的原始文本序列上训练来学习条件分布 $$p(x \vert z)$$。然后学到的模型能按提示前缀生成文本。训练数据包含维基百科、OpenWebText、图书、亚马逊评论、reddit 语料等，每个数据集被分配一个控制码，reddit 语料中每个子版有其自身主题作为控制码。

![CTRL examples](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/CTRL-control-code.png)

*图 16：用于训练 CTRL 的数据集及关联控制码。（图片来源：改自 [Keskar et al., 2019](https://arxiv.org/abs/1909.05858) 表 7）*

控制码还可用于给定 token 的*领域标注*，因为 $$p(z \vert x) \propto p(x \vert z) p(z)$$（假设领域上先验均匀）。CTRL 的一个局限是缺乏对*不生成什么*的控制（如避免毒性）。

![CTRL examples](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/CTRL-examples.png)

*图 17：CTRL 条件样本生成示例。（图片来源：[Keskar et al., 2019](https://arxiv.org/abs/1909.05858)）*

注意 CTRL 从零训练一个 transformer 模型。然而，给同一数据集内的所有文本打同一控制码（如所有维基百科文章都用 "wikipedia" 作控制码）感觉相当受限。考虑到我们常常需要高度定制的控制码却只有有限的标注数据，我预期用小标注数据集按 CTRL 的方式微调一个无条件 LM 也能奏效。尽管需要多少数据、样本质量如何还有待实验。

### RL 微调

用 RL 针对任意且可能不可微的奖励函数微调序列模型，多年前已被证明有效（[Ranzato et al., 2015](https://arxiv.org/abs/1511.06732)）。RL 微调可解决*教师强制（teacher forcing）*方法的若干问题。教师强制下，模型训练时只在每个单独解码步最小化最大似然损失，测试时却被要求从头预测整个序列。训练与测试间的这种差异可能导致暴露偏差与误差累积。相比之下，RL 微调能在序列级直接优化任务专属指标，如翻译的 BLEU（[Ranzato et al., 2015](https://arxiv.org/abs/1511.06732)、[Wu et al., 2016](https://arxiv.org/abs/1609.08144)、[Nguyen et al., 2017](https://arxiv.org/abs/1707.07402)）、摘要的 ROUGE（[Ranzato et al., 2015](https://arxiv.org/abs/1511.06732)、[Paulus et al., 2017](https://arxiv.org/abs/1705.04304)、[Wu and Hu, 2018](https://arxiv.org/abs/1804.07036)）与故事生成的定制指标（[Tambwekar et al., 2018](https://arxiv.org/abs/1809.10736)）。

[Ranzato et al (2015)](https://arxiv.org/abs/1511.06732) 应用 REINFORCE 训练 RNN 模型做序列生成任务。模型先用交叉熵损失（ML 损失）训练预测下一 token，然后用 ML 损失与 REINFORCE（RL 损失）交替微调。第二微调阶段，下一 token 预测的训练步数逐渐减少直至为零，最终只用 RL 损失。实验表明这一序列级 RL 微调在当年带来对若干监督学习基线的巨大改进。

Google 在其神经机器翻译系统中实现了类似方法（[Wu et al., 2016](https://arxiv.org/abs/1609.08144)），[Paulus et al (2017)](https://arxiv.org/abs/1705.04304) 把该方法用于摘要任务。训练目标含两部分：下一 token 预测的 ML 损失 $$\mathcal{L}_\text{ML} = \sum_{(x, y^*)\sim\mathcal{D}} \log p_\theta(y^* \vert x)$$，与最大化期望奖励的 RL 损失 $$\mathcal{L}_\text{RL}$$——每序列奖励用 BLEU 或 ROUGE 度量。模型先用 $$\mathcal{L}_\text{ML}$$ 训练至收敛，然后用两损失的线性组合 $$\mathcal{L}_\text{mix} = \alpha \mathcal{L}_\text{ML} + (1 - \alpha)\mathcal{L}_\text{RL}$$ 微调。

Google NMT 的 RL 损失是最大化期望 BLEU 分数：

$$
\mathcal{L}_\text{RL} = - \sum_{(x, y^*)\sim\mathcal{D}} \mathbb{E}_{y\sim p_\theta(.\vert x)} [R(y, y^*)]
$$
其中 $$y$$ 是预测序列，$$y^*$$ 是真实标注。

[Paulus et al (2017)](https://arxiv.org/abs/1705.04304) 基于两个输出序列间的奖励差加了额外权重项——$$y$$ 按预测概率采样下一 token，$$\hat{y}$$ 贪婪取最可能 token。若采样序列 $$y$$ 获得比贪婪基线 $$\hat{y}$$ 更高的奖励，该 RL 损失最大化其条件似然：

$$
\mathcal{L}_\text{RL} = \sum_{(x, y^*)\sim\mathcal{D}} (R(\hat{y}, y^*) - R(y, y^*)) \sum_{t=1}^{n'} \log p(y_t \vert y_{<t}, x)
$$

### 用人类偏好做 RL 微调

奖励学习对定义人类偏好至关重要。BLEU 或 ROUGE 这类定量度量计算序列间词与 n 元短语的重叠，并不总与人类评判的更高质量相关。从人类反馈学习奖励（[Christiano et al., 2017](https://arxiv.org/abs/1706.03741)）是让"我们度量的"与"我们真正关心的"对齐的更好方式。人类反馈已被用于学习故事生成（[Yi et al., 2019](https://arxiv.org/abs/1904.13015)）与摘要（[Böhm et al., 2019](https://arxiv.org/abs/1909.01214)、[Ziegler et al., 2019](https://arxiv.org/abs/1909.08593)、[Stiennon et al., 2020](https://arxiv.org/abs/2009.01325)）等应用的奖励函数。

为生成更连贯的对话，[Yi et al (2019)](https://arxiv.org/abs/1904.13015) 收集了给定对话对（用户话语、系统回复）时 4 种二值人类反馈：系统回复是否 (1) 全面、(2) 切题、(3) 有趣、(4) 促成对话延续。
训练一个评估器预测人类反馈，然后用于重排束搜索样本、微调模型或两者兼用。（实际上他们没有用 RL 微调，而是用评估器在监督微调中提供判别器损失。）

设学到的、由 $$\psi$$ 参数化的奖励函数 $$R_\psi(x, y)$$ 作为给定输入 $$x$$ 时输出 $$y$$ 质量的度量。

为学习由人类判断定义的真实奖励 $$R^*$$，[Böhm et al (2019)](https://arxiv.org/abs/1909.01214) 比较了两种损失函数：

(1) 回归损失：简单最小化均方误差。

$$
\mathcal{L}^\text{MSE}_\text{rm} = [R^*(x, y) - R_\psi(x, y)]^2
$$

(2) 偏好损失：学习与真实奖励一致，

$$
\begin{aligned}
\mathcal{L}^\text{pref}_\text{rm} =& - \sum_{i,j} \big(\mathbb{1}[R^*(x, y_i) > R^*(x, y_j)] \log P(y_i \succ y_j) + \\
&\mathbb{1}[R^*(x, y_j) > R^*(x, y_i)] \log P(y_j \succ y_i) \big)\\ 
\text{where }P(y_i \succ y_j) =& \frac{\exp(R_\psi(x, y_i))}{\exp(R_\psi(x, y_i)) + \exp(R_\psi(x, y_j))}
\end{aligned}
$$

他们的实验表明*偏好损失*取得最佳性能，奖励模型是 BERT 句子嵌入之上的薄 MLP 层。

[Ziegler et al (2019)](https://arxiv.org/abs/1909.08593) 通过请人在给定输入 $$x \sim \mathcal{D}$$ 时从若干选项 $$\{y_i\}$$ 中选出最佳候选 $$y_b$$ 来收集人类标签。候选的采样方式为 $$y_0, y_1 \sim p(.\vert x), y_2, y_3 \sim \pi(.\vert x)$$。我们应注意当真值模糊时，人类标注可能有很高的分歧。

![Human feedback fine-tuning](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/finetune-human-feedback.png)

*图 18：用从人类反馈学到的奖励微调语言模型策略的训练框架概览。（图片来源：[Ziegler et al., 2019](https://arxiv.org/abs/1909.08593)）*

奖励模型由一个预训练语言模型加最终嵌入输出上的一个随机线性层实现。训练以最小化损失：

$$
\mathcal{L}_\text{rm} = -\mathbb{E}_{(x, \{y_i\}, b) \sim \mathcal{D}} \Big[ \log \frac{\exp(R_\psi(x, y_b))}{\sum_i \exp(R_\psi(x, y_i))} \Big]
$$

为保持训练中尺度一致，奖励模型被归一化为均值 0、方差 1。

<a name="kl-penalty" />RL 微调期间，策略 $$\pi$$（由预训练语言模型 $$p$$ 初始化）用上述学到的奖励模型经 [PPO](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/#ppo) 优化。为避免策略过度偏离其原始行为，加入 **KL 惩罚**：

$$
R(x, y) = R_\psi(x, y) - \beta\log\frac{\pi(y \vert x)}{p(y \vert x)}
$$

若运行在线数据收集，人类标签收集过程在 RL 微调期间持续，人类标注员可审阅最新策略生成的结果。人类标签数量在训练过程中均匀分布，同时奖励模型也周期性重训。在线数据收集对摘要任务重要、对文本续写任务不重要。他们的实验中，共享参数联合训练奖励模型与策略效果不佳，可能因数据集规模严重失衡导致过拟合。

后续工作（[Stiennon et al., 2020](https://arxiv.org/abs/2009.01325)）把人类标签收集进一步简化为在一对摘要 $$y_b \in\{y_0, y_1\}$$ 中选最佳。奖励模型损失更新为优化所选摘要的对数几率：

$$
\mathcal{L}_\text{rm} = \mathbb{E}_{(x, y_0, y_1, b)\sim\mathcal{D}} [\log(\sigma(r_\theta(x, y_b) − r_\theta(x, y_{1−b})))]
$$

![Human feedback fine-tuning 2](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/summarize-human-feedback.png)

*图 19：从人类反馈微调语言模型策略做摘要的概览，包括 (1) 人类反馈收集、(2) 奖励模型训练与 (3) 策略训练。（图片来源：[Stiennon et al., 2020](https://arxiv.org/abs/2009.01325)）*

### 用可操控层做引导微调

与其微调整个模型，只微调一小组额外参数、基础模型保持固定，在计算上更便宜。

<a name="pplm" />计算机视觉中，即插即用生成网络（plug-and-play generative networks，PPGN；[Nguyen et al., 2017](https://arxiv.org/abs/1612.00005)）通过把判别器 $$p(a \vert x)$$ 插入基础生成模型 $$p(x)$$ 生成带不同属性的图像。于是带期望属性 $$a$$ 的样本可从 $$p(x \vert a) \propto p(a \vert x)p(x)$$ 采样。受 PPGN 启发，**即插即用语言模型（plug-and-play language model，PPLM**；[Dathathri et al., 2019](https://arxiv.org/abs/1912.02164)）把一个或多个简单属性模型与预训练语言模型结合，做可控文本生成。

给定属性 $$a$$ 与生成样本 $$x$$，设属性模型为 $$p(a\vert x)$$。为控制内容生成，时间 $$t$$ 的当前潜在表示 $$H_t$$（含每层的键值对列表）可被 $$\Delta H_t$$ 沿两个梯度之和的方向移动：
- 一个朝 $$p(a \vert x)$$ 下属性 $$a$$ 的更高对数似然——使输出内容获得期望属性。
- 另一个朝未修改语言模型 $$p(x)$$ 的更高对数似然——使生成文本仍是流畅平滑的自然语言。

为移动输出，解码时 PPLM 运行一前向 → 一反向 → 一前向，共三趟：
1. 首先前向传播计算 $$p(a\vert x)$$ 下属性 $$a$$ 的似然；
2. 设 $$\Delta H_t$$ 为对隐藏状态 $$H_t$$ 的逐步更新，使 $$(H_t + \Delta H_t)$$ 把生成文本的分布移近具有属性 $$a$$。$$\Delta H_t$$ 初始化为零。
然后反向传播用属性模型的归一化梯度 $$\nabla_{\Delta H_t} \log p(a \vert H_t + \Delta H_t)$$ 更新 LM 隐藏状态：
$$
\Delta H_t \leftarrow \Delta H_t + \alpha \frac{\nabla_{\Delta H_t} \log p(a|H_t + \Delta H_t)}{\| \nabla_{\Delta H_t} \log p(a|H_t + \Delta H_t) \|^\gamma}
$$
其中 $$\gamma$$ 是归一化缩放系数，逐层设定。$$\alpha$$ 是步长。该更新可重复 $$m \in [3, 10]$$ 次。
3. 最终前向传播从更新后的潜在变量 $$\tilde{H}_t = H_t + \Delta H_t$$ 重算词表上的新分布。下一个 token 从更新后的分布采样。

![PPLM](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/PPLM.png)

*图 20：PPLM 如何运行三趟更新模型输出以提升期望属性似然的概览。（图片来源：[Dathathri et al., 2019](https://arxiv.org/abs/1912.02164)）*

生成时可用定制的权重混搭多个属性模型，充当一组"控制旋钮"。PPLM 论文探索了两类属性模型：
1. 最简单的属性模型基于预定义*词袋（bag of words，BoW）* $$\{w_1, \dots, w_k\}$$，指定感兴趣的主题。<br/>
$$
\log p(a \vert x) = \log\big( \sum_{i=1}^k p_{t+1} [w_i] \big)
$$
<br/>为鼓励模型至少输出一次期望词而非每步都输出，他们用最大梯度范数归一化梯度。
<br/>有趣的是，他们发现提升生成词袋中词的概率也提升生成同主题*相关*但不同词的概率。
2. 判别器属性模型基于学到的分类器，以分布而非硬样本定义偏好。

为确保语言流畅，PPLM 应用了两个额外设计：
1. 最小化修改与未修改 LM 之间的 KL 散度，常见于其他 RL 微调方法（见[上文](#kl-penalty)）。
2. 执行[后归一化融合（post-norm fusion）](https://arxiv.org/abs/1809.00125)持续把生成文本绑到无条件 LM $$p(x)$$，$$x_{t+1} \sim \frac{1}{\beta}(\tilde{p}_{t+1}^{\gamma_\text{gm}} p_{t+1}^{1-\gamma_\text{gm}})$$，其中 $$p_{t+1}$$ 与 $$\tilde{p}_{t+1}$$ 分别是未修改与修改后的输出分布。$$\beta$$ 是归一化因子。$$\gamma_\text{gm} \in [0.8, 0.95]$$ 平衡修改前后的模型预测。

![PPLM examples](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/PPLM-examples.png)

*图 21：PPLM 可控文本生成示例。（图片来源：[Dathathri et al., 2019](https://arxiv.org/abs/1912.02164)）*

有趣的是，他们发现各主题的可控程度方差很大。某些主题（宗教、科学、政治）比其他（计算机、太空）更易控制。

PPLM 的一个明显缺点是：每个解码步多趟传播使测试时计算昂贵得多。

类似 PPLM，**DELOREAN**（DEcoding for nonmonotonic LOgical REAsoNing；[Qin et al., 2020](https://arxiv.org/abs/2010.05906)）通过反向传播纳入未来上下文。给定输入文本 $$\mathbf{x}$$，DELOREAN 旨在生成续写补全 $$\mathbf{y} = [y_1, \dots, y_N]$$ 使 $$y$$ 满足由上下文 $$z$$ 定义的某些约束。为保持生成可微，跟踪 $$y$$ 的软表示 $$\tilde{\mathbf{y}}=(\tilde{y}_1, \dots, \tilde{y}_N)$$，其中 $$\tilde{y}_i \in \mathbb{R}^V$$ 是词表上的 logits。$$\tilde{\mathbf{y}}^{(t)}$$ 是第 $$t$$ 次迭代的软表示。

给定第 $$t$$ 次迭代的表示 $$\tilde{y}^{(t-1)}$$，它运行以下过程：
1. **反向**：约束表示为损失函数 $$\mathcal{L}(\mathbf{x}, \tilde{\mathbf{y}}^{(t-1)}, z))$$。logits 经梯度下降更新：$$\tilde{y}^{(t), b}_n = \tilde{y}_n^{(t-1)} - \lambda \nabla_{\tilde{y}_n} \mathcal{L}(\mathbf{x}, \tilde{\mathbf{y}}^{(t-1)}, z)$$。
2. **前向**：运行前向传播确保生成文本流畅。$$\tilde{y}^{(t),f}_n = \text{LM}(\mathbf{x}, \tilde{\mathbf{y}}^{(t)}_{1:n-1})$$。
3. 然后线性组合两个 logits 得到新表示 $$\tilde{y}^{(t)}_n = \gamma \tilde{y}^{(t), f}_n + (1-\gamma) \tilde{y}^{(t), b}_n$$。注意每个 $$\tilde{y}^{(t)}_n$$ 是采样下一个 $$\tilde{y}^{(t),f}_{n+1}$$ 所需的。

**Side-tuning**（[Zhang et al., 2019](https://arxiv.org/abs/1912.13503)）训练一个轻量侧网络，在原始模型输出之上学习残差，不修改预训练模型权重。与 PPLM 不同，隐藏状态上不做梯度更新。这是一个简单而有效的增量学习方法。基础模型被视为黑盒模型，未必是神经网络。Side-tuning 设定假设基础与侧模型喂完全相同的输入，侧模型独立学习。

![Side-tuning](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/side-tuning.png)

*图 22：固定权重、微调与 side-tuning 的对比。（图片来源：[Zhang et al., 2019](https://arxiv.org/abs/1912.13503)）*

论文探索了融合基础与侧模型预测的不同策略：`product` 最差，`sum`（$$\alpha$$-混合）、MLP 与 [FiLM](https://arxiv.org/abs/1709.07871) 相当。Side-tuning 在用中等量数据训练且基础网络大时能取得更好性能。

**辅助微调（Auxiliary tuning**，[Zeldes et al., 2020](https://arxiv.org/abs/2006.16823)）为原始预训练模型补充一个按目标任务偏移输出分布的*辅助*模型。基础与辅助模型输出在 logits 层合并。组合模型被训练以最大化目标输出的似然 $$p(x_t\vert x_{<t}, z)$$。

条件概率 $$p(x_t\vert x_{<t}, z)$$ 可分解为两部分：
1. $$p(x_t\vert x_{<t})$$ 给流畅 token 序列分配高概率；
2. $$p(x_t\vert x_{<t})$$ 向 $$p(x_t\vert x_{<t}, z)$$ 的偏移。

$$
p(x_t\vert x_{<t}, z) = \text{softmax}(\text{logits}_\text{LM}(x_t \vert x_{<t}) + \text{logits}_\text{aux}(x_t \vert x_{<t}, z))
$$

按贝叶斯规则，有

$$
p(x_t\vert x_{<t}, z)
= \frac{p(z \vert x_{\leq t})}{p(z)} p(x_t \vert x_{<t}) 
\propto p(z \vert x_{\leq t}) p(x_t \vert x_{<t})
$$

因此辅助模型 $$\text{logits}_\text{aux}(x_t \vert x_{<t}, z))$$ 实际上应学习预测 $$p(z \vert x_{\leq t})$$。[Zeldes et al., 2020](https://arxiv.org/abs/2006.16823) 的实验中，辅助模型可复用预训练 LM 的中间层做特征提取。

![Side auxiliary](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/side-auxiliary.png)

*图 23：辅助模型通过复用基础模型多层提取的特征训练。（图片来源：[Zeldes et al., 2020](https://arxiv.org/abs/2006.16823)）*

**GeDi**（[Kruse et al., 2020](https://arxiv.org/abs/2009.06367)）通过*生成式判别器（Generative Discriminator）*引导文本生成。判别器实现为类别条件语言模型（CC-LM）$$p_\theta(x_{1:t} \vert z)$$。判别器在每个解码步通过贝叶斯规则、在*两个*对比类别条件分布上归一化，为所有可能的下一 token 计算分类概率，以此引导生成：
1. 一个以期望属性的控制码 $$z$$ 为条件。
2. 另一个以非期望属性的反控制码 $$\bar{z}$$ 为条件。

GeDi 依赖 $$p_\theta(x_{1:t} \vert z)$$ 与 $$p_\theta(x_{1:t} \vert \bar{z})$$ 之间的对比计算序列属于期望类的概率。判别器损失最大化期望属性 $$z$$ 的概率：

$$
\begin{aligned}
p_\theta(z \vert x_{1:t}) &= \frac{p(z) p_\theta(x_{1:\tau} \vert z)^{\alpha/\tau}}{\sum_{z' \in \{z, \bar{z}\}} p(z') p_\theta(x_{1:\tau} \vert z')^{\alpha/\tau} } \\
\mathcal{L}_\text{desc} 
&= -\frac{1}{N} \sum_{i=1}^N \log p_\theta(z^{(i)} \vert x^{(i)}_{1:\tau_i}) \\
&= -\frac{1}{N} \sum_{i=1}^N \log \frac{p(z) p_\theta(x^{(i)}_{1:\tau_i} \vert z^{(i)})^{\alpha/t_i}}{\sum_{z' \in \{z, \bar{z}\} } p(z')p_\theta(x^{(i)}_{1:\tau_i} \vert z')^{\alpha/\tau_i}}
\end{aligned}
$$

其中 $$p(z) = \exp(b_z) / \sum_{z'} \exp(b_{z'})$$，$$b_z$$ 是学到的类先验。概率按当前序列长度 $$\tau$$ 归一化以加固变长序列的生成。$$\tau_i$$ 是数据集中第 $$i$$ 个输入 $$x^{(i)}$$ 的序列长度。

![GeDi](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/GeDi.png)

*图 24：GeDi 如何经贝叶斯规则工作的示意图。（图片来源：[Kruse et al., 2020](https://arxiv.org/abs/2009.06367)）*

他们用类似 [CTRL](#ctrl) 训练的控制码微调了一个 GPT2-medium 模型，用判别损失与生成损失的线性组合形成 CC-LM。该判别器模型随后作为 GeDi，引导 GPT2-XL 等更大语言模型生成。

从 GeDi 解码的一种方式是从加权后验 $$p^w(x_{t+1}\vert x_{1:t}, z) \propto p(z \vert x_{1:t+1})^w p(x_{t+1} \vert x_{1:t})$$ 采样，其中 $$w>1$$ 向期望类 $$z$$ 施加额外偏置。采样过程中只选择类概率或下一 token 概率大于某阈值的 token。

他们实验中 GeDi 引导生成表现出强可控性，且比 [PPLM](#pplm) 快 30 倍。

### 分布式方法

**带分布控制生成（Generation with Distributional Control，GDC**；[Khalifa, et al. 2020](https://arxiv.org/abs/2012.11635)）把受控文本生成框定为带约束的概率分布优化。它包含两大步骤。

**步骤 1：学习目标模型的 EBM**

把预训练 LM 记为 $$a$$，带期望特征的目标 LM 记为 $$p$$。期望特征可由一组预定义的实值特征函数 $$\phi_i(x), i=1,\dots,k$$（定义在 $$x \in X$$ 上，记为向量 $$\boldsymbol{\phi}$$）定义。当按期望模型 $$p$$ 采样序列 $$x \in X$$ 时，特征期望 $$\mathbb{E}_{x\sim p}\boldsymbol{\phi}(x)$$ 应接近 $$\bar{\boldsymbol{\mu}}$$，称"*矩约束（moment constraints）*"。特征函数 $$\phi_i$$ 可取离散值（如二元分类器的指示函数）或连续概率。同时，微调后的模型 $$p$$ 不应过度偏离 $$a$$——保持小的 KL 散度。

总之，给定预训练模型 $$a$$，我们想找到目标模型 $$p$$ 使得：

$$
\begin{aligned}
\bar{\boldsymbol{\mu}} &= \mathbb{E}_{x\sim p}\boldsymbol{\phi}(x) \\
p &= \arg\min_{c \in \mathcal{C}} D_\text{KL}(c, a)
\end{aligned}
$$

其中 $$\mathcal{C}$$ 是 $$X$$ 上满足矩约束的所有分布的集合。

按信息几何的定理，$$p$$ 可由一个 EBM（基于能量的模型；未归一化概率分布）$$P$$ 以指数函数形式近似，使 $$p(x) \propto P(x)$$ 且 $$p(x)=\frac{1}{Z}P(x)$$，其中 $$Z=\sum_x P(x)$$。该基于能量的模型可近似为：
$$
P(x)=a(x)\exp\big(\sum_i \lambda_i \phi_i(x)\big)=a(x)\exp(\boldsymbol{\lambda}\cdot\boldsymbol{\phi}(x))
$$
定义*重要性权重* $$w(x, \boldsymbol{\lambda}) = \frac{P(x)}{a(x)} = \exp\langle\boldsymbol{\lambda}\cdot\boldsymbol{\phi}(x)\rangle$$。给定从预训练模型采样的大量序列 $$x_1, \dots, x_N \sim a(x)$$，

$$
\begin{aligned}
\mu(\boldsymbol{\lambda}) 
&= \mathbb{E}_{x\sim p}\boldsymbol{\phi}(x)
= \mathbb{E}_{x\sim a} \frac{p(x)}{a(x)}\boldsymbol{\phi}(x)
= \frac{1}{Z}\mathbb{E}_{x\sim a} w(x, \boldsymbol{\lambda}) \boldsymbol{\phi}(x) \\
&= \frac{\mathbb{E}_{x\sim a} w(x, \boldsymbol{\lambda}) \boldsymbol{\phi}(x)}{\sum_{x\in X} P(x)}
= \frac{\mathbb{E}_{x\sim a} w(x, \boldsymbol{\lambda}) \boldsymbol{\phi}(x)}{\sum_{x\in X} w(x, \boldsymbol{\lambda})a(x)}
= \frac{\mathbb{E}_{x\sim a} w(x, \boldsymbol{\lambda}) \boldsymbol{\phi}(x)}{\mathbb{E}_{x\sim a} w(x, \boldsymbol{\lambda})} \\
&\simeq \frac{\sum_{i=1}^N w(x_i,\boldsymbol{\lambda}) \boldsymbol{\phi}(x_i)}{\sum_{i=1}^N w(x_i, \boldsymbol{\lambda})}
= \frac{\sum_{i=1}^N \exp\langle\boldsymbol{\lambda}\cdot\boldsymbol{\phi}(x)\rangle \boldsymbol{\phi}(x_i)}{\sum_{i=1}^N \exp\langle\boldsymbol{\lambda}\cdot\boldsymbol{\phi}(x)\rangle}
\end{aligned}
$$

在目标 $$\|\boldsymbol{\mu}(\boldsymbol{\lambda}) - \bar{\boldsymbol{\mu}}\|^2_2$$ 上用 SGD，我们可以得到 $$\boldsymbol{\lambda}$$ 的估计值与 $$P(x)=a(x)\exp\langle\boldsymbol{\lambda}\cdot\boldsymbol{\phi}(x)\rangle$$ 的表示。$$P(x)$$ 是序列 EBM，因为 $$a$$ 是自回归模型。

**步骤 2：学习目标概率分布**

EBM $$P(x)$$ 可计算两序列的概率比，但不知道 $$Z$$ 无法从 $$p(x)$$ 采样。为从序列 EBM 采样，论文提出用[分布式策略梯度（Distributional Policy Gradient）](https://arxiv.org/abs/1912.08517)（DPG；但不是这个 [DPG](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/#dpg)），目标是获得自回归策略 $$\pi_\theta$$，通过最小化交叉熵 $$H(p, \pi_\theta)$$ 近似目标分布 $$p$$。DPG 运行一系列迭代。每次迭代中，用提议分布 $$q$$ 采样，也可用重要性权重矫正交叉熵损失：

$$
\begin{aligned}
\nabla_\theta H(p, \pi_\theta) 
&= - \nabla_\theta \mathbb{E}_{x\sim p} \log \pi_\theta(x)
= - \mathbb{E}_{x\sim p} \nabla_\theta  \log \pi_\theta(x) \\
&= - \mathbb{E}_{x\sim q} \frac{p(x)}{q(x)} \nabla_\theta  \log \pi_\theta(x)
= - \frac{1}{Z}\mathbb{E}_{x\sim q} \frac{P(x)}{q(x)} \nabla_\theta  \log \pi_\theta(x)
\end{aligned}
$$

为学习这样的 $$\pi_\theta$$，论文采用 KL 自适应版 DPG：只在估计策略 $$\pi_\theta$$ 更接近 $$p$$ 时才更新 $$q$$。这一自适应步骤对快速收敛很重要。

![KL-adaptive DPG](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/GDC-KL-adaptive-DPG.png)

*图 25：使从 EBM $$P(x)$$ 采样成为可能的分布式策略梯度算法，其中 $$q$$ 初始化为 $$a$$。（图片来源：[Khalifa, et al. 2020](https://arxiv.org/abs/2012.11635)）*

该方法可用于建模可控文本生成中的多种约束：

1. 逐点约束：$$\phi_i$$ 是二元特征；如约束词的出现或不出现，或基于分类器的约束。
2. 分布约束：$$\phi_i$$ 表示概率分布；如约束性别、主题等的概率。他们的实验表明在维基百科传记语料上训练的 GPT-2 去偏方面进展巨大。生成的女性传记比例从 7.4% 提升到 35.6%。
3. 混合约束：通过简单相加组合多个约束。

![GDC debiasing](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/GDC-debiasing.png)

*图 26：用带各种约束的 GDC 做去偏实验。（图片来源：[Khalifa, et al. 2020](https://arxiv.org/abs/2012.11635)）*

与其他基线相比，用逐点约束的 GDC 偏离基础模型 $$a$$ 更少、曲线更平滑。

![GDC debiasing](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/GDC-ablation.png)

*图 27：逐点约束 GDC 与若干基线的对比。低 Self-BLEU-5 与高 Dist-1 表示高多样性。（图片来源：[Khalifa, et al. 2020](https://arxiv.org/abs/2012.11635)）*

- 直接优化奖励 $$\phi$$ 的 REINFORCE（图 X 中的 $$\text{REINFORCE}$$）无约束时收敛快，但与原始模型偏差大。
- 优化 $$P(x)$$ 的 REINFORCE（图 X 中的 $$\text{REINFORCE}_{P(x)}$$）样本多样性低。
- 与 [Ziegler et al., 2019](https://arxiv.org/abs/1909.08593) 相比，GDC 学习曲线更平滑、产生更丰富的词汇。

<a name="unlikelihood-training"></a>### 非似然训练

语言模型训练中最大化对数似然损失的标准方式导致[错误的 token 分布](#beam-search-surprise)，这无法仅靠聪明的解码方法修复。这样的模型倾向过频输出高频词、过稀输出低频词，尤其在使用确定性解码（如贪婪、束搜索）时。换言之，它们对自己的预测过度自信。

非似然训练（Unlikelihood training；[Welleck & Kulikov et al. 2019](https://arxiv.org/abs/1908.04319)）试图对抗这一点，把对*不想要*内容的偏好直接纳入训练目标。它组合两种更新：
- 常规的最大化似然更新，为真实 token 分配高概率；
- 一种新的非似然更新，避免不想要的 token 获得高概率。

给定 token 序列 $$(x_1, \dots, x_T)$$ 与第 $$t$$ 步的负候选 token 集 $$\mathcal{C}^t = \{c_1, \dots , c_m\}$$（每个 token $$x_i, c_j \in \mathcal{V}$$），第 $$t$$ 步的组合损失定义为：

$$
\mathcal{L}^t_\text{UL}(p_\theta (. \vert x_{<t}), \mathcal{C}^t)
= - \alpha \cdot \underbrace{\sum_{c \in \mathcal{C}^t} \log(1 - p_\theta(c \vert x_{<t}))}_\text{unlikelihood} - \underbrace{\log p_\theta (x_t \vert x_{<t})}_\text{likelihood}
$$

构造 $$\mathcal{C}^t$$ 的一种方法是从模型生成的序列中随机选择候选。

非似然训练可扩展到*序列*级，负续写由每步负候选集的序列定义。它们应被设计为惩罚我们不喜欢的性质。例如，可以如下惩罚重复 n-gram：

$$
\mathcal{C}^t_\text{repeat-n} = \{x_t\} \text{ if }(x_{t-i}, \dots, x_{t+j}) \in x_{<t-i} \text{ for any } (j-i)=n, i\leq n \leq j.
$$

他们的实验用非似然训练避免语言模型输出中的重复，确实比标准 MLE 训练在更少重复与更多独特 token 上展示出更好的结果。

---
引用格式：
```
@article{weng2021conditional,
  title   = "Controllable Neural Text Generation.",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2021",
  url     = "https://lilianweng.github.io/lil-log/2021/01/02/controllable-neural-text-generation.html"
}
```

## 参考文献

[1] Patrick von Platen. ["How to generate text: using different decoding methods for language generation with Transformers"](https://huggingface.co/blog/how-to-generate) Hugging face blog, March 18, 2020.

[2] Angela Fan, et al. ["Hierarchical Neural Story Generation/"](https://arxiv.org/abs/1805.04833) arXiv preprint arXiv:1805.04833 (2018).

[3] Ari Holtzman et al. ["The Curious Case of Neural Text Degeneration."](https://arxiv.org/abs/1904.09751) ICLR 2020.

[4] Marjan Ghazvininejad et al. ["Hafez: an interactive poetry generation system."](https://www.aclweb.org/anthology/P17-4008) ACL 2017.

[5] Ari Holtzman et al. ["Learning to write with cooperative discriminators."](https://arxiv.org/abs/1805.06087) ACL 2018.

[6] Ashutosh Baheti et al. ["Generating More Interesting Responses in Neural Conversation Models with Distributional Constraints."](https://arxiv.org/abs/1809.01215) EMNLP 2018.

[7] Jiatao Gu et al. ["Trainable greedy decoding for neural machine translation."](https://arxiv.org/abs/1702.02429) EMNLP 2017.

[8] Kyunghyun Cho. ["Noisy Parallel Approximate Decoding for Conditional Recurrent Language Model."](https://arxiv.org/abs/1605.03835) arXiv preprint arXiv:1605.03835. (2016).

[9] Marco Tulio Ribeiro et al. ["Semantically equivalent adversarial rules for debugging NLP models."](https://www.aclweb.org/anthology/P18-1079/) ACL 2018.

[10] Eric Wallace et al. ["Universal Adversarial Triggers for Attacking and Analyzing NLP."](https://arxiv.org/abs/1908.07125) EMNLP 2019. [[code](https://github.com/Eric-Wallace/universal-triggers)]

[11] Taylor Shin et al. ["AutoPrompt: Eliciting Knowledge from Language Models with Automatically Generated Prompts."](https://arxiv.org/abs/2010.15980) EMNLP 2020. [[code](http://ucinlp.github.io/autoprompt)]

[12] Zhengbao Jiang et al. ["How Can We Know What Language Models Know?"](https://arxiv.org/abs/1911.12543) TACL 2020.

[13] Nanyun Peng et al. ["Towards Controllable Story Generation."](https://www.aclweb.org/anthology/W18-1505/) NAACL 2018.

[14] Nitish Shirish Keskar, et al. ["CTRL: A Conditional Transformer Language Model for Controllable Generation"](https://arxiv.org/abs/1909.05858) arXiv preprint arXiv:1909.05858 (2019).[[code](https://github.com/salesforce/ctrl)]

[15] Marc'Aurelio Ranzato et al. ["Sequence Level Training with Recurrent Neural Networks."](https://arxiv.org/abs/1511.06732) ICLR 2016.

[16] Yonghui Wu et al. ["Google's Neural Machine Translation System: Bridging the Gap between Human and Machine Translation."](https://arxiv.org/abs/1609.08144) CoRR 2016.

[17] Romain Paulus et al. ["A Deep Reinforced Model for Abstractive Summarization."](https://arxiv.org/abs/1705.04304) ICLR 2018.

[18] Paul Christiano et al. ["Deep Reinforcement Learning from Human Preferences."](https://arxiv.org/abs/1706.03741) NIPS 2017.

[19] Sanghyun Yi et al. ["Towards coherent and engaging spoken dialog response generation using automatic conversation evaluators."](https://arxiv.org/abs/1904.13015) INLG 2019.

[20] Florian Böhm et al. ["Better rewards yield better summaries: Learning to summarise without references."](https://arxiv.org/abs/1909.01214) EMNLP 2019. [[code](https://github.com/yg211/summary-reward-no-reference)]

[21] Daniel M Ziegler et al. ["Fine-tuning language models from human preferences."](https://arxiv.org/abs/1909.08593) arXiv preprint arXiv:1909.08593 (2019). [[code](https://github.com/openai/lm-human-preferences)] 

[22] Nisan Stiennon, et al. ["Learning to summarize from human feedback."](https://arxiv.org/abs/2009.01325) arXiv preprint arXiv:2009.01325 (2020). 

[23] Sumanth Dathathri et al. ["Plug and play language models: a simple approach to controlled text generation."](https://arxiv.org/abs/1912.02164) ICLR 2020. [[code](https://github.com/uber-research/PPLM)]

[24] Jeffrey O Zhang et al. ["Side-tuning: Network adaptation via additive side networks"](https://arxiv.org/abs/1912.13503) ECCV 2020.

[25] Ben Kruse et al. ["GeDi: Generative Discriminator Guided Sequence Generation."](https://arxiv.org/abs/2009.06367) arXiv preprint arXiv:2009.06367.

[26] Yoel Zeldes et al. ["Technical Report: Auxiliary Tuning and its Application to Conditional Text Generatio."](https://arxiv.org/abs/2006.16823) arXiv preprint arXiv:2006.16823.

[27] Thomas Scialom, et al. ["Discriminative Adversarial Search for Abstractive Summarization"](https://arxiv.org/abs/2002.10375) ICML 2020.

[28] Clara Meister, et al. ["If beam search is the answer, what was the question?"](https://arxiv.org/abs/2010.02650) EMNLP 2020.

[29] Xiang Lisa Li and Percy Liang. ["Prefix-Tuning: Optimizing Continuous Prompts for Generation."](https://arxiv.org/abs/2101.00190) arXiv preprint arXiv:2101.00190 (2021).

[30] Lianhui Qin, et al. ["Back to the Future: Unsupervised Backprop-based Decoding for Counterfactual and Abductive Commonsense Reasoning."](https://arxiv.org/abs/2010.05906) arXiv preprint arXiv:2010.05906 (2020).

[31] Muhammad Khalifa, et al. ["A Distributional Approach to Controlled Text Generation"](https://arxiv.org/abs/2012.11635) Accepted by ICLR 2021.

[32] Aditya Grover, et al. ["Bias correction of learned generative models using likelihood-free importance weighting."](https://arxiv.org/abs/1906.09531) NeuriPS 2019.

[33] Yuntian Deng et al. ["Residual Energy-Based Models for Text Generation."](https://arxiv.org/abs/2004.11714) ICLR 2020.

[34] Brian Lester et al. ["The Power of Scale for Parameter-Efficient Prompt Tuning."](https://arxiv.org/abs/2104.08691) arXiv preprint arXiv:2104.08691 (2021).

[35] Xiao Liu et al. ["GPT Understands, Too."](https://arxiv.org/abs/2103.10385) arXiv preprint arXiv:2103.10385 (2021).

[36] Welleck & Kulikov et al. ["Neural Text Generation with Unlikelihood Training"](https://arxiv.org/abs/1908.04319) arXiv:1908.04319 (2019).
