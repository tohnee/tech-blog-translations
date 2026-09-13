---
title: "强化学习中的课程"
title_en: "Curriculum for Reinforcement Learning"
source: https://lilianweng.github.io/posts/2020-01-29-curriculum-rl/
crawled: 2026-09-08
translated: 2026-09-08
---

# 强化学习中的课程

> 原文：[Curriculum for Reinforcement Learning](https://lilianweng.github.io/posts/2020-01-29-curriculum-rl/) · Lilian Weng（翁荔）

> 课程（curriculum）是人类从简单概念渐进学习到困难问题的高效工具。它通过提供一系列难度递增的学习步骤来分解复杂知识。本文将考察课程思想如何帮助强化学习模型学会解决复杂任务。

<span style="color: #286ee0;">[更新于 2020-02-03：在"任务专属课程"一节提及 <a href="#pcg">PCG</a>。</span><br/>
<span style="color: #286ee0;">[更新于 2020-02-04：新增<a href="#curriculum-through-distillation">"通过蒸馏的课程"</a>一节。</span>

如果我们想教一个连基本算术都不会的 3 岁孩子积分或导数，这听起来像不可能的任务。这正是教育重要的原因：它提供了分解复杂知识的系统方法，以及从易到难教授概念的良好像课程。课程使人类学习困难事物变得更容易、更可接近。那么，机器学习模型呢？我们能否用课程更高效地训练模型？能否设计课程来加速学习？

早在 1993 年，Jeffrey Elman 就提出了用课程训练神经网络的想法。他在学习简单语言语法上的早期工作展示了这种策略的重要性：从受限的简单数据集开始，逐渐增加训练样本的复杂度；否则模型根本学不会。

与无课程的训练相比，我们期望采用课程能加快收敛速度，最终模型性能可能提高也可能不变。设计高效有效的课程并不容易。记住，糟糕的课程甚至可能妨碍学习。

接下来，我们将考察课程学习的几个类别（见图 1）。大多数案例应用于强化学习，少数应用于监督学习。

![Types of curriculum](https://lilianweng.github.io/posts/2020-01-29-curriculum-rl/types-of-curriculum-2.png)

*图 1：强化学习的五类课程。*

在 "The importance of starting small" 论文（[Elman 1993](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.128.4487&rep=rep1&type=pdf)）中，我特别喜欢开头的句子，觉得它们既富启发又打动人心：

> "人类在许多维度上与其他物种不同，但有两点特别值得注意。人类展现出非凡的学习能力；人类达到成熟所需的异常漫长的时间也令人瞩目。学习的适应性优势是明确的，而且可以说，通过文化，学习创造了非基因传承行为的基础，这可能加速了我们物种的演化。"

的确，学习大概是我们人类拥有的最好的超能力。

## 任务专属课程

[Bengio, et al. (2009)](https://www.researchgate.net/profile/Y_Bengio/publication/221344862_Curriculum_learning/links/546cd2570cf2193b94c577ac/Curriculum-learning.pdf) 对早期的课程学习做了很好的综述。论文用手工设计的任务专属课程做了两个带玩具实验的想法：
1. 更干净的样本可能更快带来更好的泛化。
2. 逐渐引入更难的样本加速在线训练。

有些课程策略可能无用甚至有害是说得通的。该领域要回答的一个好问题是：*使某些课程策略比其他更有效的一般原则可能是什么？* Bengio 2009 论文假设：让学习聚焦于既不太难也不太容易的"有趣"样本会有益。

如果我们的朴素课程是在复杂度逐渐增加的样本上训练模型，我们首先需要一种量化任务难度的方法。一个想法是用它相对于另一个模型的最小损失，而该模型在其他任务上预训练过（[Weinshall, et al. 2018](https://arxiv.org/abs/1802.03796)）。这样，预训练模型的知识可以通过建议训练样本的排序迁移到新模型。图 2 展示了 `curriculum` 组（绿色）相对 `control`（随机顺序；黄色）和 `anti`（逆序；红色）组的有效性。

![Curriculum by transfer learning](https://lilianweng.github.io/posts/2020-01-29-curriculum-rl/curriculum-by-transfer-learning.png)

*图 2：测试图像集上的图像分类准确率（CIFAR100 中"小型哺乳动物"的 5 个成员类）。有 4 个实验组：(a) `curriculum`：按另一个已训练分类器的置信度排序标签（如 SVM 的间隔）；(b) `control-curriculum`：随机排序标签；(c) `anti-curriculum`：逆序排序标签；(d) `None`：无课程。（图片来源：[Weinshall, et al. 2018](https://arxiv.org/abs/1802.03796)）*

[Zaremba & Sutskever (2014)](https://arxiv.org/abs/1410.4615) 做了一个有趣的实验：训练 LSTM 预测短 Python 数学运算程序的输出，而不实际执行代码。他们发现课程对学习是必要的。程序复杂度由两个参数控制：`length` ∈ [1, a] 和 `nesting` ∈ [1, b]。考虑三种策略：
1. 朴素课程：先增大 `length` 直到达到 `a`；然后增大 `nesting` 并把 `length` 重置为 1；重复此过程直到两者都达最大。
2. 混合课程：采样 `length` ~ [1, a] 和 `nesting` ~ [1, b]。
3. 组合：朴素 + 混合。

他们注意到组合策略总是优于朴素课程，且通常（但不总是）优于混合策略——表明训练中混入简单任务对*避免遗忘*相当重要。

<a name="pcg" />程序化内容生成（[PCG](https://en.wikipedia.org/wiki/Procedural_generation)）是创建各种难度视频游戏的流行方法。PCG 涉及算法随机性以及设计游戏元素与其依赖关系的大量人类专业知识。程序化生成的关卡已被引入若干基准环境，用于评估 RL 智能体能否泛化到未训练过的新关卡（[元强化学习](https://lilianweng.github.io/posts/2019-06-23-meta-rl/)！），如 [GVGAI](http://www.gvgai.net/)、OpenAI [CoinRun](https://openai.com/blog/quantifying-generalization-in-reinforcement-learning/) 和 [Procgen benchmark](https://openai.com/blog/procgen-benchmark/)。使用 GVGAI，[Justesen, et al. (2018)](https://arxiv.org/abs/1806.10729) 证明 RL 策略容易过拟合到特定游戏，而按简单课程随模型性能同步提升任务难度地训练有助于其泛化到新的人工设计关卡。CoinRun 中也发现了类似结果（[Cobbe, et al. 2018](https://arxiv.org/abs/1812.02341)）。POET（[Wang et al, 2019](https://arxiv.org/abs/1901.01753)）是利用进化算法和程序化生成游戏关卡提升 RL 泛化的又一例子，我在[元强化学习文章](https://lilianweng.github.io/posts/2019-06-23-meta-rl/#evolutionary-algorithm-on-environment-generation)中详细描述过。

要沿袭上述课程学习方法，通常我们需要在训练过程中解决两个问题：
1. 设计一个度量来量化任务有多难，以便据此排序任务。
2. 训练期间向模型提供难度递增的任务序列。

然而，任务的顺序不必是串行的。在我们的魔方论文（[OpenAI et al, 2019](https://arxiv.org/abs/1910.07113.)）中，我们依靠*自动域随机化（Automatic domain randomization，ADR）*，通过增长复杂度递增的环境分布来生成课程。每个任务的难度（即在一系列环境中解魔方）取决于各种环境参数的随机化范围。即使假设所有环境参数互不相关这一简化假设，我们也能为机器人手学习该任务创建出不错的课程。

## 教师引导的课程

<a name="grave-et-al-2017" />*自动课程学习（Automatic Curriculum Learning）*的思想稍早由 [Graves, et al. 2017](https://arxiv.org/abs/1704.03003) 提出。它把 $$N$$ 任务课程视为一个 [$$N$$ 臂老虎机](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/)问题，以及一个学习优化该老虎机回报的自适应策略。

论文考虑了两类学习信号：
1. 损失驱动的进展：一次梯度更新前后损失函数的变化。这类奖励信号跟踪学习过程的速度，因为任务损失下降最大等价于学习最快。
2. 复杂度驱动的进展：网络权重上后验与先验分布之间的 KL 散度。这类学习信号受 [MDL](https://en.wikipedia.org/wiki/Minimum_description_length)（最小描述长度）原则启发："把模型复杂度增加一定量，只有当它把数据压缩得更多时才值得"。因此，期望模型复杂度在模型很好地泛化到训练样本时增长最多。

<a name="TSCL" />这一通过另一个 RL 智能体自动提出课程的框架被形式化为*师生课程学习（Teacher-Student Curriculum Learning，TSCL*；[Matiisen, et al. 2017](https://arxiv.org/abs/1707.00183)）。在 TSCL 中，*学生（student）*是完成实际任务的 RL 智能体，*教师（teacher）*是选择任务的策略。学生旨在掌握一个可能难以直接学习的复杂任务。为使该任务更易学，我们设置教师智能体通过挑选恰当的子任务来引导学生的训练过程。

![Teacher-student curriculum](https://lilianweng.github.io/posts/2020-01-29-curriculum-rl/teacher-student-curriculum.png)

*图 3：师生课程学习的设定。（图片来源：[Matiisen, et al. 2017](https://arxiv.org/abs/1707.00183) + 我用红色做的标注。）*

在此过程中，学生应学习的任务：
1. 能帮助学生取得最快学习进展，或
2. 有被遗忘的风险。

> 注：把教师模型框定为 RL 问题的设定感觉与神经架构搜索（NAS）很相似，但不同在于 TSCL 中的 RL 模型在任务空间上运作，而 NAS 在主模型架构空间上运作。

训练教师模型是解一个 [POMDP](https://en.wikipedia.org/wiki/Partially_observable_Markov_decision_process) 问题：
- 未观测的 $$s_t$$ 是学生模型的完整状态。
- 观测 $$o = (x_t^{(1)}, \dots, x_t^{(N)})$$ 是 $$N$$ 个任务的分数列表。
- 动作 $$a$$ 是挑选一个子任务。
- 每步奖励是分数增量 $$r_t = \sum_{i=1}^N x_t^{(i)} - x_{t-1}^{(i)}$$（即等价于最大化情节结束时所有任务的分数）。

从有噪的任务分数估计学习进展、同时平衡探索与利用的方法可以借鉴非平稳多臂老虎机问题——用 [ε-贪婪](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/#ε-greedy-algorithm)或[汤普森采样](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/#thompson-sampling)。

核心思想总结起来：用一个策略为另一个策略提出任务以学得更好。有趣的是，上述两项工作（在离散任务空间中）都发现从所有任务中均匀采样是一个出奇强的基准。

如果任务空间是连续的呢？[Portelas, et al. (2019)](https://arxiv.org/abs/1910.07224) 研究了连续的师生框架，教师必须从连续任务空间采样参数以生成学习课程。给定新采样的参数 $$p$$，绝对学习进展（absolute learning progress，缩写 ALP）度量为 $$\text{ALP}_p = \vert r - r_\text{old} \vert$$，其中 $$r$$ 是与 $$p$$ 关联的情节奖励，$$r_\text{old}$$ 是与 $$p_\text{old}$$ 关联的奖励。这里 $$p_\text{old}$$ 是任务空间中离 $$p$$ 最近的先前采样参数，可用最近邻检索。注意该 ALP 分数与上文 [TSCL](#TSCL) 或 [Grave, et al. 2017](#grave-et-al-2017) 中学习信号的不同：ALP 分数量化两个任务之间的奖励差，而非同一任务两个时间步之间的表现。

在任务参数空间之上，训练一个高斯混合模型拟合 $$\text{ALP}_p$$ 随 $$p$$ 的分布。采样任务时用 ε-贪婪：以一定概率采样随机任务；否则按 GMM 模型的 ALP 分数比例采样。

![ALP-GMM](https://lilianweng.github.io/posts/2020-01-29-curriculum-rl/ALP-GMM-algorithm.png)

*图 4：ALP-GMM（绝对学习进展高斯混合模型）算法。（图片来源：[Portelas, et al., 2019](https://arxiv.org/abs/1910.07224)）*

## 通过自我博弈的课程

与师生框架不同（两个智能体做的事很不一样），教师在不了解实际任务内容的情况下学会为学生挑任务。如果我们想让两者都直接在主任务上训练呢？甚至让它们互相竞争如何？

[Sukhbaatar, et al. (2017)](https://arxiv.org/abs/1703.05407) 提出了通过**非对称自我博弈（asymmetric self-play）**做自动课程学习的框架。两个智能体 Alice 和 Bob 玩同一任务但目标不同：Alice 挑战 Bob 达到同一状态，Bob 则尽可能快地完成它。

![Self-play experiments in MazeBase](https://lilianweng.github.io/posts/2020-01-29-curriculum-rl/self-play-maze.png)

*图 5：训练两个智能体时自我博弈设定的示意图。示例任务是 [MazeBase](https://github.com/facebook/MazeBase)：智能体被要求在带灯开关、钥匙和带门之墙的迷宫中到达目标旗。切换钥匙开关可开闭门，关灯后只有发光的灯开关对智能体可用。（图片来源：[Sukhbaatar, et al. 2017](https://arxiv.org/abs/1703.05407)）*

把 Alice 和 Bob 视为同一个 RL 智能体在同一环境中训练的两个独立副本，但"大脑"不同。它们各有独立参数和损失目标。自我博弈驱动的训练由两类情节组成：
- 在*自我博弈情节*中，Alice 把状态从 $$s_0$$ 改到 $$s_t$$，然后 Bob 被要求把环境恢复到原始状态 $$s_0$$ 以获得内部奖励。
- 在*目标任务情节*中，Bob 访问目标旗则获得外部奖励。

注意，由于 B 必须重复 A 在同一对 $$(s_0, s_t)$$ 之间的动作，该框架只在可逆或可复位的环境中有效。

Alice 应学会把 Bob 推出舒适区，但不给他不可能的任务。Bob 的奖励设为 $$R_B = -\gamma t_B$$，Alice 的奖励为 $$R_A = \gamma \max(0, t_B - t_A)$$，其中 $$t_B$$ 是 B 完成任务的总时间，$$t_A$$ 是 Alice 执行 STOP 动作前的时间，$$\gamma$$ 是把奖励重标定为可与外部任务奖励比较的标量常数。若 B 失败一个任务，$$t_B = t_\max - t_A$$。
两个策略都是目标条件的。损失蕴含：
1. B 想尽快完成任务。
2. A 偏好耗费 B 更多时间的任务。
3. B 失败时 A 不想走太多步。

这样，Alice 与 Bob 之间的交互自动构建出难度递增的课程。同时，由于 A 在把任务提给 B 之前自己已做过，任务保证可解。

A 提任务、B 解任务的范式听起来确实与师生框架相似。但在非对称自我博弈中，扮演教师角色的 Alice 也在同一任务上工作、为 Bob 寻找有挑战性的案例，而非显式优化 B 的学习过程。

## 自动目标生成

RL 策略常常需要能执行一组任务。目标应被谨慎选择，使每个训练阶段对当前策略既不太难也不太容易。目标 $$g \in \mathcal{G}$$ 可定义为一组状态 $$S^g$$，只要智能体到达其中任一状态就算达成目标。

生成式目标学习（Generative Goal Learning；[Florensa, et al. 2018](https://arxiv.org/abs/1705.06366)）依靠 **Goal GAN** 自动生成期望目标。他们的实验中，奖励非常稀疏，只有目标是否达成的二值标志，策略以目标为条件，

$$
\begin{aligned}
\pi^{*}(a_t\vert s_t, g) &= \arg\max_\pi \mathbb{E}_{g\sim p_g(.)} R^g(\pi) \\
\text{where }R^g(\pi) &= \mathbb{E}_\pi(.\mid s_t, g) \mathbf{1}[\exists t \in [1,\dots, T]: s_t \in S^g]
\end{aligned}
$$

这里 $$R^g(\pi)$$ 是期望回报，也等价于成功概率。给定当前策略采样的轨迹，只要有任何状态属于目标集，回报即为正。

他们的方法迭代 3 步直到策略收敛：
1. 根据一组目标对当前策略而言难度是否恰当来标注它们。
- 难度恰当的目标集称为 **GOID**（"Goals of Intermediate Difficulty"，中等难度目标的缩写）。<br/>$$\text{GOID}_i := \{g : R_\text{min} \leq R^g(\pi_i) \leq R_\text{max} \} \subseteq G$$
- 这里 $$R_\text{min}$$ 和 $$R_\text{max}$$ 可解释为 T 个时间步内到达目标的最小和最大概率。
2. 用第 1 步标注的目标训练 Goal GAN 模型以产生新目标。
3. 用这些新目标训练策略，改进其覆盖目标。

Goal GAN 自动生成课程：
- 生成器 $$G(z)$$：产生新目标。=> 期望是从 $$GOID$$ 集合均匀采样的目标。
- 判别器 $$D(g)$$：评估目标能否被达成。=> 期望是判断目标是否来自 $$GOID$$ 集合。

Goal GAN 的构造类似 LSGAN（Least-Squared GAN；[Mao et al., (2017)](https://arxiv.org/abs/1611.04076)），相比朴素 GAN 有更好的学习稳定性。按 LSGAN，我们应分别为 $$D$$ 和 $$G$$ 最小化以下损失：

$$
\begin{aligned}
\mathcal{L}_\text{LSGAN}(D) &= \frac{1}{2} \mathbb{E}_{g \sim p_\text{data}(g)} [ (D(g) - b)^2] + \frac{1}{2} \mathbb{E}_{z \sim p_z(z)} [ (D(G(z)) - a)^2] \\
\mathcal{L}_\text{LSGAN}(G) &= \frac{1}{2} \mathbb{E}_{z \sim p_z(z)} [ (D(G(z)) - c)^2]
\end{aligned}
$$

其中 $$a$$ 是假数据标签，$$b$$ 是真数据标签，$$c$$ 是 $$G$$ 希望 $$D$$ 对假数据相信的值。LSGAN 论文的实验中用 $$a=-1, b=1, c=0$$。

Goal GAN 引入额外的二值标志 $$y_b$$ 指示目标 $$g$$ 是真（$$y_g = 1$$）还是假（$$y_g = 0$$），使模型能用负样本训练：

$$
\begin{aligned}
\mathcal{L}_\text{GoalGAN}(D) &= \frac{1}{2} \mathbb{E}_{g \sim p_\text{data}(g)} [ (D(g) - b)^2 + (1-y_g) (D(g) - a)^2] + \frac{1}{2} \mathbb{E}_{z \sim p_z(z)} [ (D(G(z)) - a)^2] \\
\mathcal{L}_\text{GoalGAN}(G) &= \frac{1}{2} \mathbb{E}_{z \sim p_z(z)} [ (D(G(z)) - c)^2]
\end{aligned}
$$

![Generative goal learning](https://lilianweng.github.io/posts/2020-01-29-curriculum-rl/generative-goal-learning-algorithm.png)

*图 6：生成式目标学习的算法。（图片来源：[Florensa, et al. 2018](https://arxiv.org/abs/1705.06366)）*

沿同一想法，[Racaniere & Lampinen, et al. (2019)](https://arxiv.org/abs/1909.12892) 设计了一种使目标生成器目标更精细的方法。他们的方法包含三个组件，与上文生成式目标学习相同：
- **求解器（Solver）**/策略 $$\pi$$：每个情节中，求解器开头得到目标 $$g$$，结尾得到单次二值奖励 $$R^g$$。
- **裁判（Judge）**/判别器 $$D(.)$$：预测二值奖励（目标能否达成）的分类器；确切地说它输出达成给定目标概率的 logit，$$\sigma(D(g)) = p(R^g=1\vert g)$$，其中 $$\sigma$$ 是 sigmoid 函数。
- **出题器（Setter）**/生成器 $$G(.)$$：目标出题器以期望可行性分数 $$f \in \text{Unif}(0, 1)$$ 为输入并生成 $$g = G(z, f)$$，其中潜变量 $$z$$ 由 $$z \sim \mathcal{N}(0, I)$$ 采样。目标生成器被设计为可逆，因此 $$G^{-1}$$ 能把目标 $$g$$ 反向映射回潜变量 $$z = G^{-1}(g, f)$$。

生成器以三个目标优化：
- (1) 目标**有效性**：提出的目标应能被专家策略达成。相应的生成损失被设计为增大生成"求解器策略以前达成过的目标"的可能性（类似 [HER](https://arxiv.org/abs/1707.01495)）。
    - $$\mathcal{L}_\text{val}$$ 是生成目标过去被求解器解出的负对数似然。
    - $$
    \begin{align*}
    \mathcal{L}_\text{val} = \mathbb{E}_{\substack{
      g \sim \text{ achieved by solver}, \\
      \xi \in \text{Uniform}(0, \delta), \\
      f \in \text{Uniform}(0, 1)
    }} \big[ -\log p(G^{-1}(g + \xi, f)) \big]
    \end{align*}
    $$

- (2) 目标**可行性**：提出的目标应能被当前策略达成；即难度应恰当。
    - $$\mathcal{L}_\text{feas}$$ 要求裁判模型 $$D$$ 对生成目标 $$G(z, f)$$ 的输出概率匹配期望的 $f$。
    - $$
    \begin{align*}
    \mathcal{L}_\text{feas} = \mathbb{E}_{\substack{
      z \in \mathcal{N}(0, 1), \\
      f \in \text{Uniform}(0, 1)
    }} \big[ D(G(z, f)) - \sigma^{-1}(f)^2 \big]
    \end{align*}
    $$
- (3) 目标**覆盖度**：我们应最大化生成目标的熵以鼓励多样目标、改进目标空间上的覆盖。
    - $$
    \begin{align*}
    \mathcal{L}_\text{cov} = \mathbb{E}_{\substack{
      z \in \mathcal{N}(0, 1), \\
      f \in \text{Uniform}(0, 1)
    }} \big[ \log p(G(z, f)) \big]
    \end{align*}
    $$

他们的实验表明复杂环境需要上述全部三个损失。当环境在情节间变化时，目标生成器和判别器都需要以环境观测为条件才能产生更好的结果。若有期望的目标分布，可以增加一个用 Wasserstein 距离匹配期望目标分布的额外损失。用上该损失，生成器能更高效地把求解器推向掌握期望任务。

![Goal setter and judge models](https://lilianweng.github.io/posts/2020-01-29-curriculum-rl/setter-judge-goal-generation.png)

*图 7：(a) 求解器/策略、(b) 裁判/判别器、(c) 出题器/目标生成器模型的训练示意图。（图片来源：[Racaniere & Lampinen, et al., 2019](https://arxiv.org/abs/1909.12892)）*

## 基于技能的课程

另一个视角是把智能体能完成的事分解为多种技能，每个技能集可映射为一个任务。设想当智能体以无监督方式与环境交互时，有没有办法从这种交互中发现有用的技能，并通过课程进一步构建更复杂任务的解？

[Jabri, et al. (2019)](https://arxiv.org/abs/1912.04226) 开发了自动课程 **CARML**（"Curricula for Unsupervised Meta-Reinforcement Learning" 的缩写），把无监督轨迹建模到潜在技能空间，专注于训练[元强化学习](https://lilianweng.github.io/posts/2019-06-23-meta-rl/)策略（即可迁移到未见任务）。CARML 训练环境的设定类似 [DIAYN](https://lilianweng.github.io/posts/2019-06-23-meta-rl/#learning-with-random-rewards)。不同在于，CARML 在像素级观测上训练，而 DIAYN 在真实状态空间上运作。RL 算法 $$\pi_\theta$$（由 $$\theta$$ 参数化）通过无监督交互训练，交互被形式化为 CMP 加上学到的奖励函数 $$r$$。该设定天然适合元学习目的，因为定制的奖励函数可以只在测试时给出。

![CARML](https://lilianweng.github.io/posts/2020-01-29-curriculum-rl/CARML.png)

*图 8：CARML 示意图，含两步：(1) 把经验数据组织到潜在技能空间；(2) 用从学到的技能构造的奖励函数做策略元训练。（图片来源：[Jabri, et al 2019](https://arxiv.org/abs/1912.04226)）*

CARML 被框定为[变分期望最大化（EM）](https://chrischoy.github.io/research/Expectation-Maximization-and-Variational-Inference/)。

(1) **E 步**：这是组织经验数据的阶段。收集的轨迹用潜在分量的混合建模，构成*技能*的[基](https://en.wikipedia.org/wiki/Basis_(linear_algebra))。

设 $$z$$ 为潜在任务变量，$$q_\phi$$ 为 $$z$$ 的变分分布——可以是离散 $$z$$ 的混合模型或连续 $$z$$ 的 VAE。变分后验 $$q_\phi(z \vert s)$$ 像一个分类器，给定状态预测技能，我们想最大化 $$q_\phi(z \vert s)$$ 以尽可能区分不同技能产生的数据。E 步中，$$q_\phi$$ 被拟合到 $$\pi_\theta$$ 产生的一组轨迹。

确切地说，给定轨迹 $$\tau = (s_1,\dots,s_T)$$，我们想找到 $$\phi$$ 使得

$$
\max_\phi \mathbb{E}_{z\sim q_\phi(z)} \big[ \log q_\phi(\tau \vert z) \big]
= \max_\phi \mathbb{E}_{z\sim q_\phi(z)} \big[ \sum_{s_i \in \tau} \log q_\phi(s_i \vert z) \big]
$$

这里做了忽略一条轨迹中状态顺序的简化假设。

(2) **M 步**：这是用 $$\pi_\theta$$ 做元强化学习训练的阶段。学到的技能空间被视为训练任务分布。CARML 不关心用于策略参数更新的元强化学习算法类型。

给定轨迹 $$\tau$$，策略最大化 $$\tau$$ 与 $$z$$ 之间的互信息 $$I(\tau;z) = H(\tau) - H(\tau \vert z)$$ 是合理的，因为：
- 最大化 $$H(\tau)$$ => 策略数据空间的多样性；期望大。
- 最小化 $$H(\tau \vert z)$$ => 给定技能，行为应受限；期望小。

于是有，

$$
\begin{aligned}
I(\tau; z) 
&= \mathcal{H}(z) - \mathcal{H}(z \vert s_1,\dots, s_T) \\
&\geq \mathbb{E}_{s \in \tau} [\mathcal{H}(z) - \mathcal{H}(z\vert s)] & \scriptstyle{\text{; discard the order of states.}} \\
&= \mathbb{E}_{s \in \tau} [\mathcal{H}(s_t) - \mathcal{H}(s\vert z)] & \scriptstyle{\text{; by definition of MI.}} \\
&= \mathbb{E}_{z\sim q_\phi(z), s\sim \pi_\theta(s|z)} [\log q_\phi(s|z) - \log \pi_\theta(s)] \\
&\approx \mathbb{E}_{z\sim q_\phi(z), s\sim \pi_\theta(s|z)} [\color{green}{\log q_\phi(s|z) - \log q_\phi(s)}] & \scriptstyle{\text{; assume learned marginal distr. matches policy.}}
\end{aligned}
$$

我们可以把奖励设为 $$\log q_\phi(s \vert z) - \log q_\phi(s)$$，即上式中<span style="color: green;">绿色</span>部分。为在任务专属探索（下文<span style="color: red;">红色</span>）与潜在技能匹配（下文<span style="color: blue;">蓝色</span>）之间取得平衡，加入参数 $$\lambda \in [0, 1]$$。每个 $$z \sim q_\phi(z)$$ 的实现诱导一个奖励函数 $$r_z(s)$$（记住 奖励 + CMP => MDP）如下：

$$
\begin{aligned}
r_z(s)
&= \lambda \log q_\phi(s|z) - \log q_\phi(s) \\
&= \lambda \log q_\phi(s|z) - \log \frac{q_\phi(s|z) q_\phi(z)}{q_\phi(z|s)} \\
&= \lambda \log q_\phi(s|z) - \log q_\phi(s|z) - \log q_\phi(z) + \log q_\phi(z|s) \\
&= (\lambda - 1) \log \color{red}{q_\phi(s|z)} + \color{blue}{\log q_\phi(z|s)} + C
\end{aligned}
$$

![CARML algorithm](https://lilianweng.github.io/posts/2020-01-29-curriculum-rl/CARML-algorithm.png)

*图 9：CARML 算法。（图片来源：[Jabri, et al 2019](https://arxiv.org/abs/1912.04226)）*

学习潜在技能空间有多种方式，如 [Hausman, et al. 2018](https://openreview.net/forum?id=rk07ZXZRb)。他们方法的目标是学习任务条件策略 $$\pi(a \vert s, t^{(i)})$$，其中 $$t^{(i)}$$ 来自 $$N$$ 个任务的离散列表 $$\mathcal{T} = [t^{(1)}, \dots, t^{(N)}]$$。然而，与其为每个任务学习 $$N$$ 个独立解，不如学习一个潜在技能空间，使每个任务能表示为技能上的分布，从而技能*在任务间复用*。策略定义为 $$\pi_\theta(a \vert s,t) = \int \pi_\theta(a \vert z,s,t) p_\phi(z \vert t)\mathrm{d}z$$，其中 $$\pi_\theta$$ 和 $$p_\phi$$ 分别是要学习的策略网络和嵌入网络。若 $$z$$ 离散（即取自 $$K$$ 个技能的集合），策略成为 $$K$$ 个子策略的混合。策略训练用 [SAC](http://127.0.0.1:4000/lil-log/2018/04/07/policy-gradient-algorithms.html#sac)，对 $$z$$ 的依赖被引入熵项。

## 通过蒸馏的课程

[这个节名我想了一会儿，在克隆、继承和蒸馏之间抉择。最终选了蒸馏，因为它听起来最酷 B-)]

**渐进神经网络（progressive neural network**，[Rusu et al. 2016](https://arxiv.org/abs/1606.04671)）架构的动机是在不同任务间高效迁移已学技能，同时避免灾难性遗忘。课程通过一组渐进堆叠的神经网络塔（论文中称"列/columns"）实现。

渐进网络有如下结构：
1. 从含 $$L$$ 层神经元的单列开始，对应激活层标记为 $$h^{(1)}_i, i=1, \dots, L$$。我们先在单列网络上训练一个任务至收敛，得到参数配置 $$\theta^{(1)}$$。
2. 切换到下一任务时，我们加一个新列以适应新上下文，同时冻结 $$\theta^{(1)}$$ 锁定前一任务已学技能。新列激活层标记为 $$h^{(2)}_i, i=1, \dots, L$$，参数为 $$\theta^{(2)}$$。
3. 每个新任务重复第 2 步。第 $$k$$ 列的第 $$i$$ 层激活依赖所有已存在列中先前的激活层：

    $$
    h^{(k)}_i = f(W^{(k)}_i h^{(k)}_{i-1} + \sum_{j < k} U_i^{(k:j)} h^{(j)}_{i-1})
    $$

    其中 $$W^{(k)}_i$$ 是第 $$k$$ 列第 $$i$$ 层的权重矩阵；$$U_i^{(k:j)}, j < k$$ 是把第 $$j$$ 列第 $$i-1$$ 层投影到第 $$k$$ 列第 $$i$$ 层的权重矩阵（$$j < k$$）。上述权重矩阵应被学习。$$f(.)$$ 是自选的非线性激活函数。

![Progressive networks](https://lilianweng.github.io/posts/2020-01-29-curriculum-rl/progressive-networks.png)

*图 10：渐进神经网络架构。（图片来源：[Rusu, et al. 2017](https://arxiv.org/abs/1610.04286)）*

论文用 Atari 游戏做实验，在多个游戏上训练渐进网络，检验一个游戏学到的特征能否迁移到另一个。确实如此。不过有趣的是，学习到对先前列特征的高依赖并不总表示在新任务上有好的迁移表现。一个假设是旧任务学到的特征可能给新任务引入偏差，导致策略困在次优解。总体而言，渐进网络优于只微调顶层，能达到与微调整个网络相近的迁移性能。

渐进网络的一个用例是 sim2real 迁移（[Rusu, et al. 2017](https://arxiv.org/abs/1610.04286)）：第一列在模拟器中用大量样本训练，然后加额外的列（可为不同真实世界任务）用少量真实数据样本训练。

[Czarnecki, et al. (2018)](https://arxiv.org/abs/1806.01780) 提出了另一个 RL 训练框架 **Mix & Match**（缩写 **M&M**），通过在智能体间复制知识提供课程。给定从简到繁的智能体序列 $$\pi_1, \dots, \pi_K$$，各自以部分共享权重参数化（如共享较低的公共层）。M&M 训练一个智能体混合，但只有最复杂的 $$\pi_K$$ 的最终性能重要。

同时，M&M 学习一个类别分布 $$c \sim \text{Categorical}(1, \dots, K \vert \alpha)$$，[pmf](https://en.wikipedia.org/wiki/Probability_mass_function) 为 $$p(c=i) = \alpha_i$$，决定给定时刻用哪个策略。混合的 M&M 策略是简单加权和：$$\pi_\text{mm}(a \vert s) = \sum_{i=1}^K \alpha_i \pi_i(a \vert s)$$。课程学习通过动态调整 $$\alpha_i$$（从 $$\alpha_K=0$$ 到 $$\alpha_K=1$$）实现。$$\alpha$$ 的调整可手工进行或通过[基于种群的训练](https://lilianweng.github.io/posts/2019-09-05-evolution-strategies/#hyperparameter-tuning-pbt)。

为鼓励策略间合作而非竞争，除 RL 损失 $$\mathcal{L}_\text{RL}$$ 外，还加了另一个类似[蒸馏](https://arxiv.org/abs/1511.06295)的损失 $$\mathcal{L}_\text{mm}(\theta)$$。知识迁移损失 $$\mathcal{L}_\text{mm}(\theta)$$ 度量两个策略之间的 KL 散度，$$\propto D_\text{KL}(\pi_{i}(. \vert s) \| \pi_j(. \vert s))$$（$$i < j$$）。它鼓励复杂智能体早期去匹配简单智能体。最终损失为 $$\mathcal{L} = \mathcal{L}_\text{RL}(\theta \vert \pi_\text{mm}) + \lambda \mathcal{L}_\text{mm}(\theta)$$。

![Mix & Match](https://lilianweng.github.io/posts/2020-01-29-curriculum-rl/mix-and-match.png)

*图 11：训练策略混合的 Mix & Match 架构。（图片来源：[Czarnecki, et al., 2018](https://arxiv.org/abs/1806.01780)）*

---
引用格式：
```
@article{weng2020curriculum,
  title   = "Curriculum for Reinforcement Learning",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2020",
  url     = "https://lilianweng.github.io/lil-log/2020/01/29/curriculum-for-reinforcement-learning.html"
}
```

## 参考文献

[1] Jeffrey L. Elman. ["Learning and development in neural networks: The importance of starting small."](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.128.4487&rep=rep1&type=pdf) Cognition 48.1 (1993): 71-99.

[2] Yoshua Bengio, et al. ["Curriculum learning."](https://www.researchgate.net/profile/Y_Bengio/publication/221344862_Curriculum_learning/links/546cd2570cf2193b94c577ac/Curriculum-learning.pdf) ICML 2009.

[3] Daphna Weinshall, Gad Cohen, and Dan Amir. ["Curriculum learning by transfer learning: Theory and experiments with deep networks."](https://arxiv.org/abs/1802.03796) ICML 2018.

[4] Wojciech Zaremba and Ilya Sutskever. ["Learning to execute."](https://arxiv.org/abs/1410.4615) arXiv preprint arXiv:1410.4615 (2014).

[5] Tambet Matiisen, et al. ["Teacher-student curriculum learning."](https://arxiv.org/abs/1707.00183) IEEE Trans. on neural networks and learning systems (2017).

[6] Alex Graves, et al. ["Automated curriculum learning for neural networks."](https://arxiv.org/abs/1704.03003) ICML 2017.

[7]  Remy Portelas, et al. [Teacher algorithms for curriculum learning of Deep RL in continuously parameterized environments](https://arxiv.org/abs/1910.07224). CoRL 2019.

[8] Sainbayar Sukhbaatar, et al. ["Intrinsic Motivation and Automatic Curricula via Asymmetric Self-Play."](https://arxiv.org/abs/1703.05407) ICLR 2018.

[9] Carlos Florensa, et al. ["Automatic Goal Generation for Reinforcement Learning Agents"](https://arxiv.org/abs/1705.06366) ICML 2019.

[10] Sebastien Racaniere & Andrew K. Lampinen, et al. ["Automated Curriculum through Setter-Solver Interactions"](https://arxiv.org/abs/1909.12892) ICLR 2020.

[11] Allan Jabri, et al. ["Unsupervised Curricula for Visual Meta-Reinforcement Learning"](https://arxiv.org/abs/1912.04226) NeuriPS 2019.

[12] Karol Hausman, et al. ["Learning an Embedding Space for Transferable Robot Skills "](https://openreview.net/forum?id=rk07ZXZRb) ICLR 2018.

[13] Josh Merel, et al. ["Reusable neural skill embeddings for vision-guided whole body movement and object manipulation"](https://arxiv.org/abs/1911.06636) arXiv preprint arXiv:1911.06636 (2019).

[14] OpenAI, et al. ["Solving Rubik's Cube with a Robot Hand."](https://arxiv.org/abs/1910.07113) arXiv preprint arXiv:1910.07113 (2019).

[15] Niels Justesen, et al. ["Illuminating Generalization in Deep Reinforcement Learning through Procedural Level Generation"](https://arxiv.org/abs/1806.10729) NeurIPS 2018 Deep RL Workshop.

[16] Karl Cobbe, et al. ["Quantifying Generalization in Reinforcement Learning"](https://arxiv.org/abs/1812.02341) arXiv preprint arXiv:1812.02341 (2018).

[17] Andrei A. Rusu et al. ["Progressive Neural Networks"](https://arxiv.org/abs/1606.04671) arXiv preprint arXiv:1606.04671 (2016).

[18] Andrei A. Rusu et al. ["Sim-to-Real Robot Learning from Pixels with Progressive Nets."](https://arxiv.org/abs/1610.04286) CoRL 2017.

[19] Wojciech Marian Czarnecki, et al. ["Mix & Match – Agent Curricula for Reinforcement Learning."](https://arxiv.org/abs/1806.01780) ICML 2018.
