---
title: "DAPO：一个开源的大规模 LLM 强化学习系统"
title_en: "DAPO: An Open-Source LLM Reinforcement Learning System at Scale"
arxiv: 2503.14476
source: https://arxiv.org/abs/2503.14476
crawled: 2026-09-23
translated: 2026-09-23
---

# DAPO：一个开源的大规模 LLM 强化学习系统

> 原文：[DAPO: An Open-Source LLM Reinforcement Learning System at Scale](https://arxiv.org/abs/2503.14476) · Stanford CS329A 指定阅读

<https://github.com/volcengine/verl>

2025 年 3 月 17 日

###### 摘要

推理规模化为 LLM 赋予了前所未有的推理能力，而强化学习是激发复杂推理的核心技术。然而，最先进推理 LLM 的关键技术细节被隐藏起来（例如 OpenAI o1 博客和 DeepSeek R1 技术报告），因此社区在复现其 RL 训练结果方面仍然举步维艰。
我们提出解耦裁剪与动态采样策略优化（Decoupled Clip and Dynamic sAmpling Policy Optimization，DAPO）算法，并完全开源一个最先进的大规模 RL 系统，该系统在 Qwen2.5-32B 基础模型上于 AIME 2024 取得 50 分。
与此前提细节的训练工作不同，我们介绍了使大规模 LLM RL 取得成功的四项关键技术。此外，我们开源了基于 verl 框架构建的训练代码，以及一个经过精心筛选与处理的数据集。我们开源系统的这些组件增强了可复现性，并支持未来在大规模 LLM RL 方向的研究。

††affiliation: ByteDance Seed　2Institute for AI Industry Research (AIR), Tsinghua University††affiliation: The University of Hong Kong††affiliation: SIA-Lab of Tsinghua AIR and ByteDance Seed††contribution: Full author list in Contributions††correspondence: , ††Project Page: <https://dapo-sia.github.io/>

图 1：DAPO 在 Qwen2.5-32B 基础模型上的 AIME 2024 分数，仅用 50% 的训练步数便超越了此前最先进的 DeepSeek-R1-Zero-Qwen-32B。横轴为梯度更新步数。

## 1 引言

以 OpenAI 的 o1（OpenAI, 2024）和 DeepSeek 的 R1（Guo et al., 2025）为代表的测试时计算扩展为大型语言模型（LLM）带来了深刻的范式转变（Brown et al., 2020；Chowdhery et al., 2023；OpenAI, 2023；Anthropic, 2024；Liu et al., 2024）。测试时计算扩展使更长的思维链（Chain-of-Thought）思考成为可能，并诱导出精巧的推理行为，使模型在 AIME 和 Codeforces 等竞赛级数学与编程任务中表现出色。

驱动这场革命的核心技术是大规模强化学习（RL），它激发出自验证、迭代精炼等复杂推理行为。然而，可扩展 RL 训练的实际算法与关键配方仍然是个谜，被隐去于现有推理模型的技术报告之外（OpenAI, 2024；Guo et al., 2025；xAI, 2024；Google DeepMind, 2024；Qwen, 2024；Kimi Team et al., 2025）。在本文中，我们揭示大规模 RL 训练中的重大障碍，并开源一个可扩展的 RL 系统，其算法、训练代码与数据集全部开源，提供达到工业级 RL 结果的普惠方案。

我们以 Qwen2.5-32B（Yang et al., 2024）作为 RL 的预训练模型开展实验。在我们最初的 GRPO 运行中，在 AIME 上仅取得 30 分——显著低于 DeepSeek 的 RL（47 分）。深入分析表明，朴素的 GRPO 基线存在若干关键问题，例如熵坍缩、奖励噪声和训练不稳定。更广泛的社区在复现 DeepSeek 结果时也遇到了类似挑战（Chen et al., 2025；Hu et al., 2025；Hu, 2025；Cui et al., 2025；Lee et al., 2024；Kazemnejad et al., 2024；Yuan et al., 2025），这表明 R1 论文可能遗漏了开发工业级、大规模、可复现 RL 系统所必需的关键训练细节。

为弥合这一差距，我们发布一个开源的最先进大规模 LLM RL 系统，它在 Qwen2.5-32B 模型基础上于 AIME 2024 取得 50 分，仅用 50% 的训练步数便超越了此前 DeepSeek-R1-Zero-Qwen-32B（Guo et al., 2025）取得的最先进结果（47 分）（图 1）。我们提出解耦裁剪与动态采样策略优化（DAPO）算法，并介绍使 RL 在长思维链 RL 场景中大放异彩的 4 项关键技术。细节见第 3 节。

1. Clip-Higher（抬高上裁剪界），提升系统多样性并避免熵坍缩；
2. Dynamic Sampling（动态采样），提升训练效率与稳定性；
3. Token-Level Policy Gradient Loss（词元级策略梯度损失），在长思维链 RL 场景中至关重要；
4. Overlong Reward Shaping（超长奖励整形），降低奖励噪声并稳定训练。

我们的实现基于 verl（Sheng et al., 2024）。通过完整发布这个包含训练代码与数据的最先进 RL 系统，我们希望揭示对大规模 LLM RL 有价值的洞见，使更广泛的社区受益。

## 2 预备知识

### 2.1 近端策略优化（PPO）

PPO（Schulman et al., 2017）为策略优化引入了裁剪的代理目标。通过用裁剪将策略更新约束在上一个策略的近端区域内，PPO 稳定了训练并提升了样本效率。具体而言，PPO 通过最大化以下目标来更新策略：

$$
\mathcal{J}_{\text{PPO}}(\theta)=\mathbb{E}_{(q,a)\sim\mathcal{D},\,o_{\leq t}\sim\pi_{\theta_{\text{old}}}(\cdot\mid q)}\Bigg[\min\Bigg(\frac{\pi_{\theta}(o_{t}\mid q,o_{<t})}{\pi_{\theta_{\text{old}}}(o_{t}\mid q,o_{<t})}\hat{A}_{t},\ \text{clip}\Bigg(\frac{\pi_{\theta}(o_{t}\mid q,o_{<t})}{\pi_{\theta_{\text{old}}}(o_{t}\mid q,o_{<t})},1-\varepsilon,1+\varepsilon\Bigg)\hat{A}_{t}\Bigg)\Bigg], \tag{1}
$$

其中 $(q,a)$ 是来自数据分布 $\mathcal{D}$ 的问答对，$\varepsilon$ 是重要性采样比率的裁剪范围，$\hat{A}_{t}$ 是时间步 $t$ 处优势函数的估计量。给定价值函数 $V$ 和奖励函数 $R$，$\hat{A}_{t}$ 使用广义优势估计（GAE）（Schulman et al., 2018）计算：

$$
\hat{A}_{t}^{\text{GAE}(\gamma,\lambda)}=\sum_{l=0}^{\infty}(\gamma\lambda)^{l}\delta_{t+l}, \tag{2}
$$

其中

$$
\delta_{l}=R_{l}+\gamma V(s_{l+1})-V(s_{l}),\quad 0\leq\gamma,\lambda\leq 1. \tag{3}
$$

### 2.2 组相对策略优化（GRPO）

与 PPO 相比，GRPO 去掉了价值函数，并以组相对的方式估计优势。对于一个特定的问答对 $(q,a)$，行为策略 $\pi_{\theta_{\text{old}}}$ 采样一组共 $G$ 条独立响应 $\{o_{i}\}_{i=1}^{G}$。随后，第 $i$ 条响应的优势通过对组级奖励 $\{R_{i}\}_{i=1}^{G}$ 做归一化计算得到：

$$
\hat{A}_{i,t}=\frac{r_{i}-\text{mean}(\{R_{i}\}_{i=1}^{G})}{\text{std}(\{R_{i}\}_{i=1}^{G})}. \tag{4}
$$

与 PPO 类似，GRPO 采用裁剪目标，并外加一个直接施加的 KL 惩罚项：

$$
\begin{aligned}
\mathcal{J}_{\text{GRPO}}(\theta)
&=\mathbb{E}_{(q,a)\sim\mathcal{D},\,\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta_{\text{old}}}(\cdot\mid q)}\\
&\quad\Bigg[\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|o_{i}|}\sum_{t=1}^{|o_{i}|}\Bigg(\min\Big(r_{i,t}(\theta)\hat{A}_{i,t},\ \text{clip}\Big(r_{i,t}(\theta),1-\varepsilon,1+\varepsilon\Big)\hat{A}_{i,t}\Big)-\beta D_{\text{KL}}(\pi_{\theta}\Vert\pi_{\text{ref}})\Bigg)\Bigg],
\end{aligned} \tag{5}
$$

其中

$$
r_{i,t}(\theta)=\frac{\pi_{\theta}(o_{i,t}\mid q,o_{i,<t})}{\pi_{\theta_{\text{old}}}(o_{i,t}\mid q,o_{i,<t})}. \tag{6}
$$

同样值得注意的是，GRPO 在样本层面计算目标。确切地说，GRPO 先在每条生成序列内部计算平均损失，再对不同样本的损失取平均。正如我们将在第 3.3 节讨论的，这种差异可能影响算法的性能。

（a）AIME 上的准确率。

（b）actor 模型的熵。

图 2：应用 Clip-Higher 策略前后，RL 训练过程中 AIME 测试集上的准确率与 actor 模型生成概率的熵。

### 2.3 移除 KL 散度

KL 惩罚项用于约束在线策略与冻结参考策略之间的散度。在 RLHF 场景（Ouyang et al., 2022）中，RL 的目标是让模型行为对齐、同时又不过度偏离初始模型。然而，在训练长思维链推理模型时，模型分布会显著偏离初始模型，因此这一限制并无必要。故我们将从所提算法中去掉 KL 项。

### 2.4 基于规则的奖励建模

使用奖励模型通常会受到奖励黑客（reward hacking）问题的困扰（Amodei et al., 2016；Everitt et al., 2017；Krakovna et al., 2020；Everitt et al., 2021；Gao et al., 2022；Weng, 2024）。作为替代，我们直接使用可验证任务的最终正确率作为结果奖励，按以下规则计算：

$$
R(\hat{y},y)=\begin{cases}1,&\texttt{is\_equivalent}(\hat{y},y)\\ -1,&\text{otherwise}\end{cases} \tag{7}
$$

其中 $y$ 是标准答案，$\hat{y}$ 是预测答案。这已被证明是激活基础模型推理能力的有效途径，在自动定理证明（Polu & Sutskever, 2020；Trinh et al., 2024；Trinh & Luong, 2024；AlphaProof & AlphaGeometry Teams, 2024）、计算机编程（Le et al., 2022；Shinn et al., 2023；Chen et al., 2023；Gehring et al., 2025）以及数学竞赛（Guo et al., 2025）等多个领域均有体现。

## 3 DAPO

我们提出解耦裁剪与动态采样策略优化（DAPO）算法。DAPO 为每个配有答案 $a$ 的问题 $q$ 采样一组输出 $\{o_{i}\}_{i=1}^{G}$，并通过以下目标优化策略：

$$
\begin{aligned}
\mathcal{J}_{\text{DAPO}}(\theta)
&=\mathbb{E}_{(q,a)\sim\mathcal{D},\,\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta_{\text{old}}}(\cdot\mid q)}\\
&\quad\Bigg[\frac{1}{\sum_{i=1}^{G}|o_{i}|}\sum_{i=1}^{G}\sum_{t=1}^{|o_{i}|}\min\Big(r_{i,t}(\theta)\hat{A}_{i,t},\ \text{clip}\Big(r_{i,t}(\theta),1-\varepsilon_{\text{low}},1+\varepsilon_{\text{high}}\Big)\hat{A}_{i,t}\Big)\Bigg]\\
\text{s.t.}\quad& 0<\Big|\{o_{i}\mid\texttt{is\_equivalent}(a,o_{i})\}\Big|<G,
\end{aligned} \tag{8}
$$

其中

$$
r_{i,t}(\theta)=\frac{\pi_{\theta}(o_{i,t}\mid q,o_{i,<t})}{\pi_{\theta_{\text{old}}}(o_{i,t}\mid q,o_{i,<t})},\quad\hat{A}_{i,t}=\frac{R_{i}-\text{mean}(\{R_{i}\}_{i=1}^{G})}{\text{std}(\{R_{i}\}_{i=1}^{G})}. \tag{9}
$$

完整算法见算法 1。本节将介绍与 DAPO 相关的关键技术。

### 3.1 抬高天花板：Clip-Higher

在我们最初使用朴素 PPO（Schulman et al., 2017）或 GRPO（Shao et al., 2024）的实验中，我们观察到熵坍缩现象：随着训练推进，策略的熵迅速下降（图 2(b)）。某些组的采样响应趋于几乎完全相同。这表明探索受限、策略过早确定化，会阻碍扩展过程。

我们提出 Clip-Higher 策略来解决这一问题。对重要性采样比率进行裁剪由裁剪式近端策略优化（PPO-Clip）（Schulman et al., 2017）引入，用于限制信赖域并增强 RL 的稳定性。我们发现，上裁剪界会限制策略的探索：让一个「利用」（exploitation）token 的概率变得更高容易得多，而一个不太可能出现的「探索」（exploration）token 的概率却被束缚得太紧而难以提升。

具体来说，当 $\varepsilon=0.2$（多数算法的默认值）且 $\hat{A}_{i,t}>0$（系统试图提高概率）时，考虑两个概率分别为 $\pi_{\theta_{\text{old}}}(o_{i}\mid q)=0.01$ 和 $0.9$ 的动作。提升后的概率 $\pi_{\theta}(o_{i}\mid q)$ 的上界分别为 $0.012$ 和 $1.08$（即 $\pi_{\theta_{\text{old}}}\cdot(1+\epsilon)$）。这意味着概率较高（例如 0.9）的「利用」token 不受约束，甚至可以达到 0.999 这样的极大概率。相反，对于低概率的「探索」token，要实现有实质意义的概率提升则困难得多。从经验上看，我们还观察到被上裁剪的 token 的平均概率很低：$\pi_{\theta}(o_{i}\mid q)<0.2$（图 3(a)）。这一发现支持了我们的直觉：上裁剪阈值确实限制了低概率「探索」token 的概率提升，从而可能约束系统的探索。

遵循 Clip-Higher 策略，我们将下裁剪界与上裁剪界解耦为 $\varepsilon_{\text{low}}$ 与 $\varepsilon_{\text{high}}$，如式 (10) 中所强调：

$$
\begin{aligned}
\mathcal{J}_{\text{DAPO}}(\theta)
&=\mathbb{E}_{(q,a)\sim\mathcal{D},\,\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta_{\text{old}}}(\cdot\mid q)}\\
&\quad\Bigg[\frac{1}{\sum_{i=1}^{G}|o_{i}|}\sum_{i=1}^{G}\sum_{t=1}^{|o_{i}|}\min\Big(r_{i,t}(\theta)\hat{A}_{i,t},\ \text{clip}\Big(r_{i,t}(\theta),1-\varepsilon_{\text{low}},1+\varepsilon_{\text{high}}\Big)\hat{A}_{i,t}\Big)\Bigg]\\
\text{s.t.}\quad& 0<\Big|\{o_{i}\mid\texttt{is\_equivalent}(a,o_{i})\}\Big|<G.
\end{aligned} \tag{10}
$$

我们增大 $\varepsilon_{\text{high}}$ 的值，为低概率 token 的提升留出更多空间。如图 2 所示，这一调整有效增强了策略的熵，并促进生成更多样的样本。我们保持 $\varepsilon_{\text{low}}$ 不变，因为增大它会将这些 token 的概率压制到 $0$，导致采样空间坍缩。

（a）被上裁剪概率的均值。

（b）正确率为 1 的样本占比。

图 3：被上裁剪概率的均值以及准确率 = 1 的提示占比。

### 3.2 多多益善：动态采样

现有 RL 算法在部分提示的准确率等于 1 时会遇到梯度衰减问题。以 GRPO 为例，若某个提示的全部输出 $\{o_{i}\}_{i=1}^{G}$ 都正确并获得相同奖励，则该组的优势为零。零优势导致零策略梯度，使批量梯度的幅值缩小、噪声敏感度增大，从而降低样本效率。从经验上看，准确率等于 1 的样本数量持续增加，如图 3(b) 所示。这意味着每个批次中有效提示的数量不断减少，可能导致梯度方差变大，并削弱模型训练的梯度信号。

为此，我们提出过采样并过滤掉准确率等于 1 和 0 的提示，如式 (11) 所示，使批次中所有提示都带有有效梯度，并保持提示数量恒定。每个批次的采样开销是动态的。训练之前，我们持续采样，直到批次完全由准确率既非 0 也非 1 的样本填满。

$$
\begin{aligned}
\mathcal{J}_{\text{DAPO}}(\theta)
&=\mathbb{E}_{(q,a)\sim\mathcal{D},\,\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta_{\text{old}}}(\cdot\mid q)}\\
&\quad\Bigg[\frac{1}{\sum_{i=1}^{G}|o_{i}|}\sum_{i=1}^{G}\sum_{t=1}^{|o_{i}|}\min\Big(r_{i,t}(\theta)\hat{A}_{i,t},\ \text{clip}\Big(r_{i,t}(\theta),1-\varepsilon_{\text{low}},1+\varepsilon_{\text{high}}\Big)\hat{A}_{i,t}\Big)\Bigg]\\
\text{s.t.}\quad& 0<\Big|\{o_{i}\mid\texttt{is\_equivalent}(a,o_{i})\}\Big|<G.
\end{aligned} \tag{11}
$$

注意，这一策略并不一定会妨碍训练效率，因为如果 RL 系统是同步的且生成阶段未做流水线化，生成时间通常由长尾样本的生成所主导。此外，我们发现采用动态采样后，实验更快地达到了相同性能，如图 6 所示。

### 3.3 再平衡之道：词元级策略梯度损失

原始 GRPO 算法采用样本层面的损失计算：先在每个样本内部按 token 平均损失，再跨样本汇总损失。在这种方式下，每条样本在最终损失计算中被赋予相同权重。然而，我们发现这种损失归约方式在长思维链 RL 场景中带来若干挑战。

由于所有样本在损失计算中被赋予相同权重，较长响应（包含更多 token）中的 token 对总损失的贡献可能不成比例地偏低，这会导致两个不利影响。首先，对于高质量的长样本，这种效应会阻碍模型学习其中的推理相关模式。其次，我们观察到过长样本往往表现出低质量模式，如乱码与重复词。因此，样本层面的损失计算由于无法有效惩罚长样本中的这些不良模式，导致熵与响应长度不健康地增长，如图 4(a) 与图 4(b) 所示。

（a）actor 模型生成概率的熵。

（b）actor 模型生成响应的平均长度。

图 4：actor 模型概率分布的熵以及响应长度的变化。

为解决上述局限，我们在长思维链 RL 场景中引入词元级策略梯度损失（Token-level Policy Gradient Loss）：

$$
\begin{aligned}
\mathcal{J}_{\text{DAPO}}(\theta)
&=\mathbb{E}_{(q,a)\sim\mathcal{D},\,\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta_{\text{old}}}(\cdot\mid q)}\\
&\quad\Bigg[\frac{1}{\sum_{i=1}^{G}|o_{i}|}\sum_{i=1}^{G}\sum_{t=1}^{|o_{i}|}\min\Big(r_{i,t}(\theta)\hat{A}_{i,t},\ \text{clip}\Big(r_{i,t}(\theta),1-\varepsilon_{\text{low}},1+\varepsilon_{\text{high}}\Big)\hat{A}_{i,t}\Big)\Bigg],\\
\text{s.t.}\quad& 0<\Big|\{o_{i}\mid\texttt{is\_equivalent}(a,o_{i})\}\Big|<G.
\end{aligned} \tag{12}
$$

在这种设定下，较长的序列比较短的序列对整体梯度更新有更大的影响。此外，从单个 token 的视角看，如果某种生成模式能带来奖励的增加或减少，它将被同等地促进或抑制，无论它出现在多长的响应中。

### 3.4 捉迷藏：超长奖励整形

在 RL 训练中，我们通常为生成设置最大长度，超长样本随之被截断。我们发现，对截断样本的不当奖励整形会引入奖励噪声，并显著扰乱训练过程。

默认情况下，我们给截断样本分配惩罚性奖励。这种做法可能给训练过程引入噪声，因为一个合理的推理过程可能仅仅因为过长而受到惩罚。这种惩罚可能使模型对自己的推理过程是否有效产生困惑。

为研究这种奖励噪声的影响，我们首先应用超长过滤（Overlong Filtering）策略，对截断样本的损失进行掩码。我们发现该策略显著稳定了训练并提升了性能，如图 5 所示。

（a）AIME 上的性能。

（b）actor 模型的熵。

图 5：应用超长奖励整形策略前后，actor 模型在 AIME 上的准确率及其生成概率的熵。

|  |
| --- |
| 算法 1　DAPO：解耦裁剪与动态采样策略优化 |
| 输入 初始策略模型 $\pi_{\theta}$；奖励模型 $R$；任务提示 $\mathcal{D}$；超参数 $\varepsilon_{\mathtt{low}},\varepsilon_{\mathtt{high}}$ |
| 1: for step = 1,…,M do |
| 2: 　　从 $\mathcal{D}$ 中采样一个批次 $\mathcal{D}_{b}$ |
| 3: 　　更新旧策略模型 $\pi_{\theta_{old}}\leftarrow\pi_{\theta}$ |
| 4: 　　为每个问题 $q\in\mathcal{D}_{b}$ 采样 $G$ 条输出 $\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta_{\text{old}}}(\cdot\mid q)$ |
| 5: 　　运行 $R$ 为每条采样输出 $o_{i}$ 计算奖励 $\{r_{i}\}_{i=1}^{G}$ |
| 6: 　　过滤掉 $o_{i}$ 并将其余样本加入动态采样缓冲区（动态采样，式 (11)） |
| 7: 　　if 缓冲区大小 $n_{b}<N$: |
| 8: 　　　　continue |
| 9: 　　对缓冲区中的每个 $o_{i}$，为其第 $t$ 个 token 计算 $\hat{A}_{i,t}$（式 (9)） |
| 10: 　for iteration = 1, …, $\mu$ do |
| 11: 　　　　通过最大化 DAPO 目标更新策略模型 $\pi_{\theta}$（式 (8)） |
| 输出 $\pi_{\theta}$ |

表 1：

此外，我们提出软超长惩罚（Soft Overlong Punishment，式 (13)），一种长度感知的惩罚机制，用于对截断样本的奖励进行整形。具体而言，当响应长度超过预设最大值时，我们定义一个惩罚区间。在该区间内，响应越长，受到的惩罚越大。该惩罚被加到原始的基于规则的正确性奖励之上，从而向模型发出避免过长响应的信号。

$$
R_{\text{length}}(y)=\begin{cases}0,&|y|\leq L_{\text{max}}-L_{\text{cache}}\\ \frac{(L_{\text{max}}-L_{\text{cache}})-|y|}{L_{\text{cache}}},&L_{\text{max}}-L_{\text{cache}}<|y|\leq L_{\text{max}}\\ -1,&L_{\text{max}}<|y|\end{cases} \tag{13}
$$

### 3.5 数据集变换

我们的数据集通过网页抓取与人工标注相结合的方式，来源于网络与各官方竞赛主页。数学数据集的答案通常有多种格式，如表达式、公式和数字，这使得设计全面的规则来解析它们颇具挑战。为了用规则提供准确的奖励信号并尽量减少公式解析器引入的错误，受 AIME 启发，我们选择并将答案变换为易于解析的整数。例如，若原始答案以 $\frac{a+\sqrt{b}}{c}$ 的形式表示，我们就指示 LLM 修改题目，使期望答案变为 $a+b+c$。经过筛选与变换，我们得到了 DAPO-Math-17K 数据集，由 17K 条提示组成，每条提示配一个整数作为答案。

## 4 实验

### 4.1 训练细节

在本工作中，我们专门聚焦数学任务来评估我们的算法，该算法可以直接迁移到其他任务。我们采用 verl 框架（Sheng et al., 2024）进行训练。我们使用朴素 GRPO（Shao et al., 2024）作为基线算法，并使用组奖励归一化来估计优势。

关于超参数，我们使用 AdamW（Loshchilov & Hutter, 2019）优化器，恒定学习率为 $1\times 10^{-6}$，并在 20 个 rollout 步上做线性预热。对于 rollout，提示批次大小为 512，每个提示采样 16 条响应。对于训练，mini-batch 大小设为 512，即每个 rollout 步做 16 次梯度更新。对于超长奖励整形，我们将期望最大长度设为 16,384 个 token，并额外分配 4,096 个 token 作为软惩罚缓存。因此，生成的最大 token 数设为 20,480。至于 Clip-Higher 机制，我们将裁剪参数 $\varepsilon_{\text{low}}$ 设为 0.2，$\varepsilon_{\text{high}}$ 设为 0.28，这有效平衡了探索与利用之间的取舍。在 AIME 的评测上，我们将评测集重复 32 次并报告 avg@32 以保证结果稳定性。评测的推理超参数设为 temperature 1.0 与 top-p 0.7。

图 6：在基线设定下应用动态采样前后的训练进程。

### 4.2 主要结果

在 AIME 2024 上的实验表明，DAPO 成功地将 Qwen-32B 基础模型训练成一个强大的推理模型，取得的性能超越了 DeepSeek 用 R1 方法在 Qwen2.5-32B 上的实验。在图 1 中，我们观察到 AIME 2024 上的性能大幅提升，准确率从接近 0% 提高到 50%。值得注意的是，这一提升仅用 DeepSeek-R1-Zero-Qwen-32B 所需训练步数的 50% 便已实现。

我们分析了方法中每项训练技术的贡献，详见表 1。观察到的提升证明了这些技术在 RL 训练中的有效性，每项都为 AIME 2024 贡献了数个准确率百分点。值得注意的是，在朴素 GRPO 设定下，从 Qwen2.5-32B 基础模型训练只能达到 30% 的准确率。

对于词元级损失，尽管它带来的性能提升较少，我们发现它增强了训练稳定性，并使长度的增长更加健康。

应用动态采样时，尽管由于过滤掉零梯度数据需要采样更多数据，总训练时间并未受到显著影响。如图 6 所示，尽管采样次数增加，但由于所需的训练步数更少，模型的收敛时间甚至有所缩短。

表 1：DAPO 渐进式应用各技术的主要结果

|  |  |
| --- | --- |
| 模型 | $\textbf{AIME24}_{\text{avg@32}}$ |
| DeepSeek-R1-Zero-Qwen-32B | 47 |
| 朴素 GRPO | 30 |
| + 超长过滤（Overlong Filtering） | 36 |
| + Clip-Higher | 38 |
| + 软超长惩罚（Soft Overlong Punishment） | 41 |
| + 词元级损失（Token-level Loss） | 42 |
| + 动态采样（Dynamic Sampling，DAPO） | 50 |

### 4.3 训练动态

大型语言模型上的强化学习不仅是一个前沿研究方向，本质上也是一项复杂的系统工程挑战，其特征在于各子系统之间相互依赖。对任何单一子系统的修改都可能在整个系统中传播，由于这些组件之间错综复杂的相互作用而导致不可预见的后果。即使是初始条件的细微变化（如数据和超参数的变化），也可能通过迭代式的强化学习过程被放大，导致结果的巨大偏差。这种复杂性常使研究者陷入两难：即使经过细致分析、并有充分理由预期某项修改将改善训练过程的某些方面，实际结果也常常偏离预期轨迹。因此，对实验过程中关键中间结果的监控至关重要，它有助于迅速定位偏差的来源，并最终完善系统。

（a）平均响应长度。

（b）奖励分数。

（c）生成熵。

（d）平均概率。

图 7：DAPO 的响应长度、奖励分数、生成熵以及平均概率的指标曲线，展示了 RL 训练的动态，是识别潜在问题的重要监控指标。

- 生成响应的长度是与训练稳定性和性能密切相关的指标，如图 7(a) 所示。长度的增加为模型提供了更大的探索空间，使更复杂的推理行为得以被采样并在训练中逐渐强化。然而需要注意的是，长度在训练中并不总是保持持续上升趋势。在相当长的某些时期，它可能呈现停滞甚至下降的趋势，这一点在 Guo et al. (2025) 中也有展示。我们通常将长度与验证准确率结合使用，作为评估实验是否恶化的指标。
- 训练过程中奖励的动态一直是强化学习中最关键监控指标之一，如图 7(b) 所示。在我们的大多数实验中，奖励增长的趋势相对稳定，不会因实验设定的调整而显著波动或下降。这表明，给定可靠的奖励信号，语言模型能够稳健地拟合训练集的分布。然而，我们发现训练集上的最终奖励往往与验证集上的准确率相关性很小，这表明存在对训练集的过拟合。
- actor 模型的熵与生成概率与模型的探索能力相关，是我们在实验中密切监控的关键指标。直观上，模型的熵需要维持在适当范围内。熵过低表明概率分布过于尖锐，导致探索能力丧失；相反，熵过高往往与过度探索的问题相关，如乱码和重复生成。对于生成概率，情况恰好相反。如第 3.1 节所示，通过应用 Clip-Higher 策略，我们有效解决了熵坍缩问题。在后续实验中，我们发现保持熵缓慢上升趋势有利于模型性能的提升，见图 7(c) 与图 7(d)。

### 4.4 案例研究

|  |
| --- |
| Question: |
| Given that the base $ABC$ of the tetrahedron $S-ABC$ is an equilateral triangle, the projection $H$ of point $A$ on the face $SBC$ is the orthocenter of $\triangle SBC$, the dihedral angle $H-AB-C$ is $30^{\circ}$, and $SA=2$, find the volume of the tetrahedron. The answer is in the form $\frac{k}{m}$, so give the value of $k+m$. |
| Response: |
| Let us consider the given problem: We need to determine … |
| … |
| Next, let $S$ have coordinates $(x_{0},y_{0},z_{0})$. Since $SA=2$, the distance formula gives us $\sqrt{(x_{0})^{2}+(y_{0})^{2}+(z_{0})^{2}}=2$, so we can write $x_{0}^{2}+y_{0}^{2}+z_{0}^{2}=4$. Now, remember that $H$ is the orthogonal projection of |
| … |
| However, wait a moment, let's rethink about the dihedral angle involving planes in a more thoughtful geometric way. Consider the plane $\alpha_{1}=ABC$, which lies entirely on the xy coordinate plane (as $z=0$). Let the plane $\alpha_{2}=SBC$. The point $A$ projected perpendicularly to plane $\alpha_{2}$ lands on $H$. The line $l=AB$ … |
| … |

表 2：强化学习中反思行为的涌现

在 RL 训练过程中，我们观察到一个有趣的现象：actor 模型的推理模式随时间动态演化。具体而言，算法不仅强化了已有的、有助于正确解题的推理模式，还逐渐催生出最初完全不存在的新型推理方式。这一发现揭示了 RL 算法的适应性与探索能力，为理解模型的学习机制提供了新洞见。

例如，在模型训练的早期阶段，几乎不存在对先前推理步骤进行检查与反思的现象。然而，随着训练推进，模型表现出明显的反思与回溯行为，如表 2 所示。这一观察为进一步探索解释 RL 期间推理能力的涌现提供了线索，我们将其留作未来研究。

## 5 结论

在本文中，我们发布了一个完全开源的大规模 LLM RL 系统，包括算法、代码基础设施与数据集。该系统取得了最先进的大规模 LLM RL 性能（使用 Qwen-32B 预训练模型在 AIME 上取得 50 分）。我们提出解耦裁剪与动态采样策略优化（DAPO）算法，并介绍了使 RL 在长思维链 RL 场景中强大高效的 4 项关键技术。此外，通过开源训练代码与数据集，我们为更广泛的研究界与社会提供了可扩展强化学习解决方案的实际获取途径，使所有人都能从这些进步中受益。

## 贡献

项目负责人

Qiying Yu1,2,4

算法

Qiying Yu1,2,4, Zheng Zhang1, Ruofei Zhu1, Yufeng Yuan1, Xiaochen Zuo1, Yu Yue1

基础设施∗

Weinan Dai1,2,4, Tiantian Fan1, Gaohong Liu1, Juncai Liu1, Lingjun Liu1, Xin Liu1, Haibin Lin1, Zhiqi Lin1, Bole Ma1, Guangming Sheng1,3, Yuxuan Tong1,2,4, Qiying Yu1,2,4, Chi Zhang1, Mofan Zhang1, Ru Zhang1, Wang Zhang1, Hang Zhu1, Jinhua Zhu1

∗按姓氏字母序排列

数据集

Jiaze Chen1, Jiangjie Chen1,4, Chengyi Wang1, Hongli Yu1,2,4, Yuxuan Song1,2,4, Xiangpeng Wei1, Qiying Yu1,2,4

指导

Hao Zhou2,4, Jingjing Liu2,4, Wei-Ying Ma2,4, Ya-Qin Zhang2,4, Lin Yan1,4, Mu Qiao1,4, Yonghui Wu1, Mingxuan Wang1,4

所属机构

1ByteDance Seed

2清华大学智能产业研究院（AIR）

3香港大学

4清华大学 AIR 与 ByteDance Seed 联合 SIA-Lab

## 致谢

我们感谢 Zhengyin Du、Shengding Hu、Kai Shen、Tianyang Zhan、Zhen Xiao、Renjie Zheng、Li Han、Kaihua Jiang 以及字节跳动的其他同事对 DAPO 项目的支持。

## 参考文献

- [1]

  OpenAI.
  Learning to reason with llms, 2024.
- [2]

  Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al.
  Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning.
  arXiv preprint arXiv:2501.12948, 2025.
- [3]

  OpenAI.
  GPT4 technical report.
  arXiv preprint arXiv:2303.08774, 2023.
- [4]

  Anthropic.
  Claude 3.5 sonnet, 2024.
- [5]

  Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al.
  Language models are few-shot learners.
  Advances in neural information processing systems, 33:1877–1901, 2020.
- [6]

  Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, et al.
  Palm: Scaling language modeling with pathways.
  Journal of Machine Learning Research, 24(240):1–113, 2023.
- [7]

  Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, et al.
  Deepseek-v3 technical report.
  arXiv preprint arXiv:2412.19437, 2024.
- [8]

  XAI.
  Grok 3 beta — the age of reasoning agents, 2024.
- [9]

  Google DeepMind.
  Gemini 2.0 flash thinking, 2024.
- [10]

  Qwen.
  Qwq-32b: Embracing the power of reinforcement learning, 2024.
- [11]

  Kimi Team, Angang Du, Bofei Gao, Bowei Xing, Changjiu Jiang, Cheng Chen, Cheng Li, Chenjun Xiao, Chenzhuang Du, Chonghua Liao, et al.
  Kimi k1. 5: Scaling reinforcement learning with llms.
  arXiv preprint arXiv:2501.12599, 2025.
- [12]

  An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, et al.
  Qwen2. 5 technical report.
  arXiv preprint arXiv:2412.15115, 2024.
- [13]

  Zhipeng Chen, Yingqian Min, Beichen Zhang, Jie Chen, Jinhao Jiang, Daixuan Cheng, Wayne Xin Zhao, Zheng Liu, Xu Miao, Yang Lu, et al.
  An empirical study on eliciting and improving r1-like reasoning models.
  arXiv preprint arXiv:2503.04548, 2025.
- [14]

  Jingcheng Hu, Yinmin Zhang, Qi Han, Daxin Jiang, and Heung-Yeung Shum Xiangyu Zhang.
  Open-reasoner-zero: An open source approach to scaling reinforcement learning on the base model.
  <https://github.com/Open-Reasoner-Zero/Open-Reasoner-Zero>, 2025.
- [15]

  Jian Hu.
  Reinforce++: A simple and efficient approach for aligning large language models.
  arXiv preprint arXiv:2501.03262, 2025.
- [16]

  Ganqu Cui, Lifan Yuan, Zefan Wang, Hanbin Wang, Wendi Li, Bingxiang He, Yuchen Fan, Tianyu Yu, Qixin Xu, Weize Chen, et al.
  Process reinforcement through implicit rewards.
  arXiv preprint arXiv:2502.01456, 2025.
- [17]

  Jung Hyun Lee, June Yong Yang, Byeongho Heo, Dongyoon Han, and Kang Min Yoo.
  Token-supervised value models for enhancing mathematical reasoning capabilities of large language models.
  arXiv preprint arXiv:2407.12863, 2024.
- [18]

  Amirhossein Kazemnejad, Milad Aghajohari, Eva Portelance, Alessandro Sordoni, Siva Reddy, Aaron Courville, and Nicolas Le Roux.
  Vineppo: Unlocking rl potential for llm reasoning through refined credit assignment.
  arXiv preprint arXiv:2410.01679, 2024.
- [19]

  Yufeng Yuan, Yu Yue, Ruofei Zhu, Tiantian Fan, and Lin Yan.
  What's behind ppo's collapse in long-cot? value optimization holds the secret.
  arXiv preprint arXiv:2503.01491, 2025.
- [20]

  Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin Wu, Wang Zhang, Ru Zhang, Yanghua Peng, Haibin Lin, and Chuan Wu.
  Hybridflow: A flexible and efficient rlhf framework.
  arXiv preprint arXiv:2409.19256, 2024.
- [21]

  John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov.
  Proximal policy optimization algorithms.
  arXiv preprint arXiv:1707.06347, 2017.
- [22]

  John Schulman, Philipp Moritz, Sergey Levine, Michael Jordan, and Pieter Abbeel.
  High-dimensional continuous control using generalized advantage estimation, 2018.
- [23]

  Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell, Peter Welinder, Paul F Christiano, Jan Leike, and Ryan Lowe.
  Training language models to follow instructions with human feedback.
  In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors, Advances in Neural Information Processing Systems, volume 35, pages 27730–27744. Curran Associates, Inc., 2022.
- [24]

  Dario Amodei, Chris Olah, Jacob Steinhardt, Paul Christiano, John Schulman, and Dan Mané.
  Concrete problems in ai safety, 2016.
- [25]

  Tom Everitt, Victoria Krakovna, Laurent Orseau, Marcus Hutter, and Shane Legg.
  Reinforcement learning with a corrupted reward channel, 2017.
- [26]

  Victoria Krakovna, Jonathan Uesato, Vladimir Mikulik, Matthew Rahtz, Tom Everitt, Ramana Kumar, Zac Kenton, Jan Leike, and Shane Legg.
  Specification gaming: the flip side of ai ingenuity, 2020.
- [27]

  Tom Everitt, Marcus Hutter, Ramana Kumar, and Victoria Krakovna.
  Reward tampering problems and solutions in reinforcement learning: A causal influence diagram perspective, 2021.
- [28]

  Leo Gao, John Schulman, and Jacob Hilton.
  Scaling laws for reward model overoptimization, 2022.
- [29]

  Lilian Weng.
  Reward hacking in reinforcement learning.
  lilianweng.github.io, Nov 2024.
- [30]

  Stanislas Polu and Ilya Sutskever.
  Generative language modeling for automated theorem proving, 2020.
- [31]

  Trieu H Trinh, Yuhuai Wu, Quoc V Le, He He, and Thang Luong.
  Solving olympiad geometry without human demonstrations.
  Nature, 625(7995):476–482, 2024.
- [32]

  Trieu Trinh and Thang Luong.
  Alphageometry: An olympiad-level ai system for geometry, 2024.
- [33]

  AlphaProof and AlphaGeometry Teams.
  Ai achieves silver-medal standard solving international mathematical olympiad problems, 2024.
- [34]

  Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio Savarese, and Steven Chu Hong Hoi.
  Coderl: Mastering code generation through pretrained models and deep reinforcement learning.
  Advances in Neural Information Processing Systems, 35:21314–21328, 2022.
- [35]

  Noah Shinn, Federico Cassano, Edward Berman, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao.
  Reflexion: Language agents with verbal reinforcement learning, 2023.
- [36]

  Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou.
  Teaching large language models to self-debug, 2023.
- [37]

  Jonas Gehring, Kunhao Zheng, Jade Copet, Vegard Mella, Quentin Carbonneaux, Taco Cohen, and Gabriel Synnaeve.
  Rlef: Grounding code llms in execution feedback with reinforcement learning, 2025.
- [38]

  Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Mingchuan Zhang, YK Li, Y Wu, and Daya Guo.
  Deepseekmath: Pushing the limits of mathematical reasoning in open language models.
  arXiv preprint arXiv:2402.03300, 2024.
- [39]

  Ilya Loshchilov and Frank Hutter.
  Decoupled weight decay regularization.
  In International Conference on Learning Representations, 2019.

## 附录 A 数据集变换

下面是一个数据变换的例子，我们展示了原始问题、变换后的问题以及变换过程中模型的输出（原文为 markdown 文本，此处为提高可读性做了渲染）。

为确保模型能高准确率地完成这一任务，我们的目标是让它进行全面的推理同时避免幻觉。我们通过提供一个清晰的思考框架来鼓励彻底的推理来实现这一点。具体而言，我们采用思维链（CoT）推理以及四个明确定义的步骤：提取答案格式、改写题面、求解修改后的问题并给出整数作为最终答案。对于每个步骤，我们提供少样本解答或详细的指导方针来引导模型的推理。

通过这种方法，我们观察到在大多数情况下，LLM 生成的改写在格式与质量上都是令人满意的。

### 原始问题

Let $x$ and $y$ be real numbers such that $x^{2}+y^{2}-22x-16y+113=0.$ Determine the smallest possible value of $x.$ Answer: $11-2\sqrt{6}$

### 变换后的问题

Let $x$ and $y$ be real numbers such that $x^{2}+y^{2}-22x-16y+113=0.$ Determine the smallest possible value of $x$. The original answer is in the form $k-m\sqrt{n}$, where $k$, $m$, and $n$ are integers. Please find the value of $k+m+n$. Answer: $19$

### 模型输出（Markdown 文本）

#### Transformation Thought Process

The original answer to the problem is an algebraic expression $11-2\sqrt{6}$.
We need to transform this into an integer form. First, note that the answer consists of an integer part and a square root term. According to the given rule, we replace the integer and square root components with undetermined coefficients. The original problem uses $x$ and $y$ as variables, so we choose other letters as undetermined coefficients. We express the answer in the form
$k-m\sqrt{n}$
and require the student to find $k+m+n$.

#### Answer Format

$k-m\sqrt{n}$

#### Transformed Problem

Let $x$ and $y$ be real numbers such that
$x^{2}+y^{2}-22x-16y+113=0.$
Determine the smallest possible value of $x$. The original answer is in the form $k-m\sqrt{n}$, where $k$, $m$, and $n$ are integers. Please find the value of $k+m+n$.

#### Answer Calculation for the Transformed Problem

- 原始答案为：$11-2\sqrt{6}$。
- 要求的格式为：$k-m\sqrt{n}$。
- 匹配系数：$k=11$，$m=2$，$n=6$。
- 最终结果为：$k+m+n=11+2+6=19$。

#### Final Answer

$19$

## 附录 B 补充案例

|  |
| --- |
| Question: |
| Among the 900 residents of Aimeville, there are 195 who own a diamond ring, 367 who own a set of golf clubs, and 562 who own a garden spade. In addition, each of the 900 residents owns a bag of candy hearts. There are 437 residents who own exactly two of these things, and 234 residents who own exactly three of these things. Find the number of residents of Aimeville who own all four of these things. |
| Response: |
| Step by Step Solution: |
| 1. Let's define the following variables: |
| Let $A$ be the set of residents who own a diamond ring. |
| Let $B$ be the set of residents who own a set of golf clubs. |
| Let $C$ be the set of residents who own a garden spade. |
| Let $D$ be the set of residents who own a bag of candy hearts. Since all 900 residents own a bag of candy hearts, $|D|=900$. |
| Let $a_{i}$ denote the number of residents who own exactly $i$ out of the 4 items. |
| Let's use the principle of inclusion-exclusion for the union of 4 sets $A,B,C,D$. |
| … |
| $a_{4}=\frac{-219}{-4}=\frac{219}{4}=54.75$. |
| Since $a_{4}$, the number of people owning all four items, must be a whole number, our current approach needs to be reconsidered in terms of the combinatorial counting of people owning different combinations of the items. Instead of directly using the inclusion-exclusion principle, we can use a different approach involving the number of people owning combinations of the items $A$, $B$, $C$, and $D$. |
| Let $x_{i}$ be the number of people owning exactly $i$ item among $A$, $B$, $C$ (excluding the item $D$ which everyone owns). |
| Then the total number of people owning exactly $k$ items among the $A$, $B$, $C$, and $D$ can be broken down: |
| … |

表 3：反思行为涌现的一个案例。
