---
title: "强化学习中的奖励作弊"
title_en: "Reward Hacking in Reinforcement Learning"
source: https://lilianweng.github.io/posts/2024-11-28-reward-hacking/
crawled: 2026-09-08
translated: 2026-09-08
---

# 强化学习中的奖励作弊

> 原文：[Reward Hacking in Reinforcement Learning](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/) · Lilian Weng（翁荔）

当[强化学习（RL）]((https://lilianweng.github.io/posts/2018-02-19-rl-overview/))智能体（agent）[利用](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/#exploitation-vs-exploration)奖励函数（reward function）中的缺陷或模糊之处来获取高奖励，却并未真正学到或完成预期任务时，就会发生奖励作弊（reward hacking）。奖励作弊之所以存在，是因为 RL 环境往往并不完美，而精确地设定一个奖励函数本身就极具挑战。

随着[语言模型](https://lilianweng.github.io/posts/2019-01-31-lm/)泛化到种类繁多的任务、基于人类反馈的强化学习（RLHF）成为对齐（alignment）训练的事实标准方法，语言模型 RL 训练中的奖励作弊已成为一个关键的实践挑战。模型学会修改单元测试以通过编程任务，或者回复中带有模仿用户偏好的偏差——这类情形相当令人担忧，也很可能是 AI 模型更多自主化用例走向现实部署的主要阻碍之一。

过去关于这一主题的大多数工作都相当理论化，侧重于定义奖励作弊或证明其存在。然而，对实用缓解方法的研究，尤其是在 RLHF 和 LLM 语境下的研究，仍然十分有限。我特别想呼吁未来有更多研究力量投入到理解和缓解奖励作弊的方向上。希望不久之后我能用一篇专门的文章来介绍缓解方法。

# 背景

## 强化学习中的奖励函数

奖励函数定义了任务，而奖励塑形（reward shaping）会显著影响[强化学习](https://lilianweng.github.io/posts/2018-02-19-rl-overview/)中的学习效率与准确性。为 RL 任务设计奖励函数常常给人一种「黑魔法」的感觉。造成这种复杂性的因素有很多：如何把一个大目标分解成若干小目标？奖励是稀疏的还是稠密的？如何衡量成功与否？不同的选择可能带来良好或糟糕的学习动态，包括任务变得不可学习，或者奖励函数变得可被作弊。关于如何在 RL 中做奖励塑形，已经有很长的研究历史。

例如，在 [Ng et al. 1999 年的论文](https://people.eecs.berkeley.edu/~pabbeel/cs287-fa09/readings/NgHaradaRussell-shaping-ICML1999.pdf)中，作者研究了如何在[马尔可夫决策过程（MDP）](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#markov-decision-processes)中修改奖励函数而保持最优策略（policy）不变。他们发现线性变换是可行的。给定一个 MDP $M = (S, A, T, \gamma, R)$，我们想构造一个变换后的 MDP $M’ = (S, A, T, \gamma, R’)$，其中 $R’ = R + F$，$F: S \times A \times S \mapsto \mathbb{R}$，以此引导学习算法更加高效。给定实值函数 $\Phi: S \mapsto \mathbb{R}$，若 $F$ 是一个基于势能的塑形函数，则它对所有 $s \in S - {s_0}, a \in A, s’ \in S$ 都满足：

$$
F(s, a, s') = \gamma \Phi(s') - \Phi(s)
$$

这样可以保证 $F$ 的折扣和 $F(s_1, a_1, s_2) + \gamma F(s_2, a_2, s_3) + \dots$ 最终为 0。若 $F$ 是这样一个基于势能的塑形函数，那么它是保证 $M$ 与 $M’$ 拥有相同最优策略的*充分*且*必要*条件。

当 $F(s, a, s’) = \gamma \Phi(s’) - \Phi(s)$，并且进一步假设 $\Phi(s_0) = 0$（其中 $s_0$ 是吸收态）且 $\gamma=1$ 时，对所有 $s \in S, a \in A$ 有：

$$
\begin{aligned}
Q^*_{M'} (s,a) &= Q^*_M(s, a) - \Phi(s) \\
V^*_{M'} (s,a) &= V^*_M(s, a) - \Phi(s)
\end{aligned}
$$

这种形式的奖励塑形让我们可以把启发式信息融入奖励函数以加速学习，同时不影响最优策略。

## 虚假相关

分类任务中的虚假相关（spurious correlation）或捷径学习（shortcut learning）（[Geirhos et al. 2020](https://arxiv.org/abs/2004.07780)）是与奖励作弊密切相关的概念。虚假特征或捷径特征可能导致分类器无法按预期地学习和泛化。例如，一个区分狼与哈士奇的二分类器，如果所有狼的训练图片中都包含雪，就可能过拟合于雪地背景这一特征（[Ribeiro et al. 2024](https://arxiv.org/abs/1602.04938)）。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/shortcut-features.png)

*如果模型过拟合于捷径特征，其在分布外（OOD）测试集上的表现会很差。（图片来源：Geirhos et al. 2020）*

[经验风险最小化（ERM）原则](https://en.wikipedia.org/wiki/Empirical_risk_minimization)指出：由于完整的数据分布未知，最小化训练数据上的损失是风险的一个合理代理，因此我们偏好训练损失最低的模型。[Nagarajan et al. (2021)](https://arxiv.org/abs/2010.15775) 研究了 ERM 原则并指出，ERM 在试图无约束地拟合数据时，需要依赖所有类型的信息特征，包括不可靠的虚假特征。他们的实验表明，无论任务多么简单，ERM 都会依赖虚假特征。

# 来定义奖励作弊

RL 中的奖励塑形颇具挑战。当 RL 智能体利用奖励函数中的缺陷或模糊之处获取高奖励，却并未真正学会预期行为或按设计完成任务时，就会发生奖励作弊。近年来，研究者提出了若干相关概念，它们都指向某种形式的奖励作弊：

- 奖励作弊（Reward hacking）（[Amodei et al., 2016](https://arxiv.org/abs/1606.06565)）
- 奖励腐化（Reward corruption）（[Everitt et al., 2017](https://arxiv.org/abs/1705.08417)）
- 奖励篡改（Reward tampering）（[Everitt et al. 2019](https://arxiv.org/abs/1908.04734)）
- 规格博弈（Specification gaming）（[Krakovna et al., 2020](https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/)）
- 目标鲁棒性（Objective robustness）（[Koch et al. 2021](https://www.gatsby.ucl.ac.uk/~balaji/udl2021/accepted-papers/UDL2021-paper-055.pdf)）
- 目标错误泛化（Goal misgeneralization）（[Langosco et al. 2022](https://arxiv.org/abs/2105.14111)）
- 奖励误设（Reward misspecifications）（[Pan et al. 2022](https://arxiv.org/abs/2201.03544)）

这一概念起源于 Amodei et al. (2016)，他们在开创性论文[《AI 安全中的具体问题》（"Concrete Problems in AI Safety"）](https://arxiv.org/abs/1606.06565)中提出了一系列关于 AI 安全的开放研究问题，并将**奖励作弊**列为关键的 AI 安全问题之一。奖励作弊指的是智能体有可能通过不良行为钻奖励函数的空子来获取高奖励。**规格博弈**（[Krakovna et al. 2020](https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/)）是类似概念，定义为满足目标的字面规格、却没有达成期望结果的行为。这里，任务目标的字面描述与真实意图之间可能存在落差。

奖励塑形是一种用于丰富奖励函数的技术，目的是让智能体更容易学习——例如提供更稠密的奖励。然而，设计不当的奖励塑形机制可能改变最优策略的轨迹。设计有效的奖励塑形机制本质上就很困难。与其归咎于糟糕的奖励函数设计，更准确的说法是：由于任务本身的复杂性、状态部分可观测、需要考量的维度众多以及其他因素，设计一个好的奖励函数本身就极具挑战。

在分布外（OOD）环境中测试 RL 智能体时，鲁棒性失效可能源于：

1. 模型即使目标正确也无法有效泛化。这种情况发生在算法缺乏足够的智能或能力时。
2. 模型泛化能力很强，但追求的目标与训练目标不一致。这种情况发生在代理奖励与真实奖励函数不同（$R’ \neq R$）时，被称为**目标鲁棒性**（[Koch et al. 2021](https://www.gatsby.ucl.ac.uk/~balaji/udl2021/accepted-papers/UDL2021-paper-055.pdf)）或**目标错误泛化**（[Langosco et al. 2022](https://arxiv.org/abs/2105.14111)）

在 [CoinRun](https://github.com/openai/coinrun) 和 [Maze](https://github.com/openai/procgen) 这两个 RL 环境中的实验证明了训练期间随机化的重要性。如果训练期间硬币或奶酪被放置在固定位置（即关卡最右端或迷宫右上角），而测试环境中硬币或奶酪随机放置，那么智能体在测试时只会径直跑向那个固定位置，而不去拿硬币或奶酪。当视觉特征（如奶酪或硬币）与位置特征（如右上角或最右端）在测试时不一致时，就会产生冲突，使训练出的模型偏好位置特征。我想指出的是，在这两个例子中，*奖励与结果之间的差距*（reward-result gaps）是显而易见的，但在大多数现实场景中，这类偏差不太可能如此明显。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/coinrun-randomization.png)

*训练期间随机化硬币位置的影响。当训练时硬币以 {0, 2, 3, 6, 11}% 的比例随机放置（x 轴）时，智能体在测试中导航到关卡末端却未取得硬币的频率随随机化程度的提高而下降（"y 轴"）。（图片来源：Koch et al. 2021）*

**奖励篡改（Reward Tampering）**（[Everitt et al. 2019](https://arxiv.org/abs/1908.04734)）是奖励作弊行为的一种形式：智能体干扰奖励函数本身，使得观测到的奖励不再准确代表预期目标。在奖励篡改中，模型要么直接操纵奖励函数的实现，要么间接改动作为奖励函数输入的环境信息，从而修改自己的奖励机制。

（注：一些工作将奖励篡改定义为与奖励作弊不同的一类失配行为。但在这里，我将奖励作弊视为一个更宽泛的概念。）

从宏观上看，奖励作弊可以分为两类：环境或目标误设，以及奖励篡改。

- **环境或目标被误设**：模型通过入侵环境或优化与真实奖励目标不一致的奖励函数——例如奖励被误设或缺少关键要求——来学会不良行为以获取高奖励。
- **奖励篡改**：模型学会干扰奖励机制本身。

## 示例列表

### 强化学习任务中的奖励作弊示例

- 训练用于抓取物体的机械手，可能学会把手放在物体与摄像机之间来愚弄人类。（[链接](https://openai.com/index/learning-from-human-preferences/)）
- 训练用于最大化跳跃高度的智能体，可能利用物理模拟器中的漏洞达到不切实际的高度。（[链接](https://arxiv.org/abs/1803.03453)）
- 智能体训练骑自行车前往目标，并且每当靠近目标时就获得奖励。于是智能体可能学会绕着目标骑小圈，因为远离目标并不会受到惩罚。（[链接](https://people.eecs.berkeley.edu/~pabbeel/cs287-fa09/readings/NgHaradaRussell-shaping-ICML1999.pdf)）
- 在足球比赛环境中，智能体一触球就获得奖励，于是智能体学会贴着球停留，以一种类似振动的高频率反复触球。（[链接](https://people.eecs.berkeley.edu/~pabbeel/cs287-fa09/readings/NgHaradaRussell-shaping-ICML1999.pdf)）
- 在 [Coast Runners 游戏](https://openai.com/blog/faulty-reward-functions/)中，智能体控制一艘船，目标是尽快完成赛艇比赛。当为撞击赛道沿线的绿色方块设置塑形奖励后，最优策略变成了原地转圈、反反复复撞击同一个绿色方块。（[链接](https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/)）
- [《数字进化令人惊讶的创造力》（"The Surprising Creativity of Digital Evolution"）](https://arxiv.org/abs/1803.03453)（Lehman et al. 2019）——这篇论文提供了大量例子，说明优化一个误设的适应度函数会带来令人惊奇的「作弊」或非预期的进化、学习结果。
- [AI 规格博弈示例清单](https://docs.google.com/spreadsheets/d/e/2PACX-1vRPiprOaC3HsCf5Tuum8bRfzYUiKLRqJmbOoC-32JorNdfyTiRRsR7Ea5eWtvsWzuxo8bjOxCG84dAg/pubhtml)由 [Krakovna et al. 2020](https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/) 收集整理。

### LLM 任务中的奖励作弊示例

- 用于生成摘要的语言模型能够钻 ROUGE 指标的空子，从而拿到高分，但生成的摘要几乎无法阅读。（[链接](https://web.archive.org/web/20180215132021/https://www.salesforce.com/products/einstein/ai-research/tl-dr-reinforced-model-abstractive-summarization/)）
- 编程模型学会修改单元测试来通过编程题。（[链接](https://arxiv.org/abs/2406.10162)）
- 编程模型可能学会直接修改用于计算奖励的代码。（[链接](https://arxiv.org/abs/2406.10162)）

### 现实生活中的奖励作弊示例

- 社交媒体的推荐算法本意是提供有用的信息。然而，「有用」往往用代理指标来衡量，比如点赞数、评论数，或者在平台上的互动时长或频率。算法最终会推荐那些能影响用户情绪状态的内容（例如耸人听闻的极端内容），以触发更多互动。（[Harari, 2024](https://www.goodreads.com/en/book/show/204927599-nexus)）
- 对视频网站误设的代理指标进行优化，可能激进地拉长用户的观看时长，而真正的目标是优化用户的主观幸福感。（[链接](https://arxiv.org/abs/2201.03544)）
- [《大空头》（"The Big Short"）](https://en.wikipedia.org/wiki/The_Big_Short)——由房地产泡沫引发的 2008 年金融危机。当人们试图钻金融体系的空子时，我们的社会就发生了奖励作弊。

## 奖励作弊为何存在？

[**古德哈特定律（Goodhart's Law）**](https://en.wikipedia.org/wiki/Goodhart%27s_law)的说法是：*「当一个测量指标成为目标时，它就不再是一个好的测量指标。」*直觉在于：一旦对一个好指标施加巨大的优化压力，它就可能被败坏。设定一个 100% 准确的奖励目标非常困难，而任何*代理*指标都面临被作弊的风险，因为 RL 算法会利用奖励函数定义中的任何微小缺陷。[Garrabrant (2017)](https://www.lesswrong.com/posts/EbFABnst8LsidYs5Y/goodhart-taxonomy) 将古德哈特定律分为 4 个变体：

1. 回归型（Regressional）——对一个不完美代理指标的选择，必然也同时选择了噪声。
2. 极端型（Extremal）——指标选择把状态分布推入与原有数据分布不同的区域。
3. 因果型（Causal）——当代理指标与目标之间存在非因果的相关性时，对代理指标进行干预可能无法干预到目标。
4. 对抗型（Adversarial）——对代理指标的优化会给对手以激励，使其将自身目标与该代理指标关联起来。

[Amodei et al. (2016)](https://arxiv.org/abs/1606.06565) 总结道，奖励作弊（主要在 RL 场景中）可能由以下原因引发：

1. 状态部分可观测，目标也只是环境状态的不完美表示。
2. 系统本身复杂且易被入侵；例如，若允许智能体执行能改变部分环境的代码，那么利用环境机制就会变得容易得多。
3. 奖励可能涉及难以学习或难以形式化的抽象概念；例如，输入维度很高的奖励函数可能不成比例地依赖少数几个维度。
4. RL 的目标就是把奖励函数优化到极致，因此存在一种内在的「冲突」，使良好的 RL 目标设计变得困难。一种特殊情况是带有自我强化反馈成分的奖励函数：奖励可能被放大、扭曲，直至背离初衷，例如广告投放算法导致赢家通吃。

此外，要识别一个最优智能体究竟在为哪个奖励函数优化其行为，通常是不可能的，因为在固定环境中，可能存在无穷多个与任何观测到的策略相一致的奖励函数（[Ng & Russell, 2000](https://ai.stanford.edu/~ang/papers/icml00-irl.pdf)）。[Amin and Singh (2016)](https://arxiv.org/abs/1601.06569) 将这种*不可辨识性（unidentifiability）*的成因分为两类：

1. 表征类（Representational）——一组奖励函数在某些算术运算（如重新缩放）下行为不变。
2. 实验类（Experimental）——$\pi$ 的观测行为不足以区分两个或多个都能合理解释该智能体行为的奖励函数（该行为在这些奖励函数下都是最优的）。

# 对强化学习环境作弊

随着模型和算法日益强大，奖励作弊预计会成为更常见的问题。更聪明的智能体更有能力发现奖励函数设计中的「漏洞」并*利用*任务规格——换言之，获得更高的代理奖励、更低的真实奖励。相比之下，较弱的算法可能找不到这些漏洞，因此在模型不够强时，我们既观察不到奖励作弊，也发现不了当前奖励函数设计中的问题。

在一组机器人零和自博弈（[Bansal et al., 2017](https://arxiv.org/abs/1710.03748)）中，我们可以训练两个智能体（受害者 vs. 对手）相互对抗。标准训练流程能产出在与普通对手对弈时表现尚可的受害者智能体。然而，训练出一个能够稳定击败受害者的对抗性对手策略却很容易，尽管它输出的动作看似随机，且训练所用时间步数不到 3%（[Gleave et al., 2020](https://arxiv.org/abs/1905.10615)）。对抗策略的训练与标准 RL 设置一样，都是优化折扣奖励之和，只是把受害者策略当作黑盒模型。

缓解对抗策略攻击的一种直观方法，是让受害者针对对抗策略进行微调。然而，一旦对抗策略针对新的受害者策略重新训练，受害者对新版对抗策略依然脆弱。

对抗策略为什么会存在？一个假设是：对抗策略是通过向受害者引入 OOD 观测来奏效的，而非在物理层面干扰它。证据表明，当把受害者对对手位置的观测掩蔽并设为静态状态后，受害者对对抗者变得*更鲁棒*，尽管在面对普通对手策略时表现变差。此外，更高维的观测空间会在正常情况下提升性能，却也让策略更容易受到对抗性对手的攻击。

[Pan et al. (2022)](https://arxiv.org/abs/2201.03544) 研究了奖励作弊随智能体能力的变化，包括 (1) 模型规模、(2) 动作空间分辨率、(3) 观测空间噪声和 (4) 训练时长。他们还将误设的代理奖励分为三种类型：

1. *权重失当（Misweighting）*：代理奖励与真实奖励刻画了同一组期望属性（desiderata），但相对重要性不同。
2. *本体论式（Ontological）*：代理奖励与真实奖励用不同的期望属性来刻画同一概念。
3. *范围（Scope）*：代理只在受限的域（如时间或空间）上度量期望属性，因为在所有条件下进行度量成本过高。

他们在四个 RL 环境中配以九种误设的代理奖励进行实验。总体发现可以概括为：*能力更强的模型往往获得更高（或相近）的代理奖励，但真实奖励下降。*

- 模型规模：更大的模型规模带来更高的代理奖励，但真实奖励下降。
- 动作空间分辨率：动作精度提升会造就能力更强的智能体。然而，更高的分辨率使代理奖励保持不变，而真实奖励下降。
- 观测保真度：更精确的观测提升代理奖励，但略微降低真实奖励。
- 训练步数：在初始阶段两种奖励正相关，之后对代理奖励优化更多步会损害真实奖励。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/exp-reward-misspecification.png)

*代理奖励与真实奖励值随（上排）模型规模（以参数量计）和（下排）模型能力（以训练步数、动作空间分辨率、观测噪声等指标衡量）变化的曲线。（图片来源：Pan et al. 2022）*

如果一个代理奖励设定得极差、与真实奖励的相关性非常弱，我们也许能在训练之前就识别并阻止奖励作弊。基于这一假设，[Pan et al. (2022)](https://arxiv.org/abs/2201.03544) 在一批轨迹 rollout 上考察了代理奖励与真实奖励之间的相关性。有趣的是，即使真实奖励与代理奖励正相关，奖励作弊仍然会发生。

# 对 LLM 的 RLHF 作弊

[基于人类反馈的强化学习（RLHF）](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/#rl-fine-tuning-with-human-preferences)已成为语言模型对齐训练的事实标准方法。先在人类反馈数据上训练一个奖励模型（reward model），然后通过 RL 微调语言模型来优化这个人类偏好的代理奖励。在 RLHF 设置中，我们关心三种奖励：

- (1) **神谕/黄金奖励（Oracle/Gold reward）** $R^∗$，代表我们*真正*希望 LLM 优化的东西。
- (2) **人类奖励** $R^\text{human}$，是我们在实践中收集来评估 LLM 的奖励，通常来自有时间约束的个体人类。由于人类给出的反馈可能不一致或出错，人类奖励并不能完全准确地表示神谕奖励。
- (3) **代理奖励** $R$，是由在人类数据上训练出的奖励模型预测的分数。因此，$R^\text{train}$ 继承了人类奖励的全部弱点，外加潜在的建模偏差。

RLHF 优化的是代理奖励分数，但我们最终关心的是黄金奖励分数。

## 对训练过程作弊

[Gao et al. (2022)](https://arxiv.org/abs/2210.10760) 研究了 RLHF 中奖励模型过度优化的标度律（scaling law）。为了在实验中扩大人类标签的规模，他们采用了合成数据设置：用一个大 RM（60 亿参数）来近似神谕奖励 $R^*$ 的「黄金」标签，而对应 $R$ 的代理 RM 参数量从 300 万到 30 亿不等。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/rm-scaling-laws.png)

*RM 分数随 KL 散度度量平方根变化的曲线。虚线为代理奖励，实线为黄金奖励。（图片来源：Gao et al. 2022）*

从初始策略到优化后策略的 KL 散度为 $\text{KL} = D_\text{KL}(\pi | \pi_\text{init})$，距离函数定义为 $d := \sqrt{ D_\text{KL}(\pi | \pi_\text{init})}$。对于 best-of-$n$ 拒绝采样（BoN）和 RL，黄金奖励 $R^∗$ 都定义为 $d$ 的函数。系数 $\alpha$ 和 $\beta$ 通过经验拟合得到，并按定义令 $R^∗ (0) := 0$。

作者也尝试拟合代理奖励 $R$，但发现在外推到更高 KL 值时会出现系统性低估，因为代理奖励看起来随 $d$ 线性增长。

$$
\begin{aligned}
R^*_{\text{bo}n}(d) &= d (\alpha_{\text{bo}n} - \beta_{\text{bo}n} d) & \text{; for best-of-n (BoN) sampling.}\\
R^*_\text{RL}(d) &= d (\alpha_\text{RL} - \beta_\text{RL} \log d) & \text{; for reinforcement learning}\\
\end{aligned}
$$

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/rm-scaling-laws-coeff.png)

*系数参数 $\alpha_{\text{bo}n}, \beta_{\text{bo}n}, \beta_\text{RL}$ 根据数据经验拟合，展示为奖励模型规模的函数。系数 $\alpha_\text{RL}$ 未包含在内，因为它在各 RM 规模下保持恒定。（图片来源：Gao et al. 2022）*

他们的实验还探索了 RM 过度优化与策略模型规模、RM 数据量等因素之间的关系：

- 针对某个 RM，更大的策略从优化中获得的收益更少（即初始奖励与峰值奖励之间的差距比较小策略更小），但过度优化程度也更轻。
- 更多 RM 数据带来更高的黄金奖励分数，并减少「古德哈特效应（Goodharting）」。
- KL 惩罚对黄金分数的影响类似于早停。注意，除这一组实验外，其余所有实验中 PPO 的 KL 惩罚都设为 0，因为他们观察到使用 KL 惩罚会严格增大代理-黄金奖励差距。

RLHF 旨在提升模型与人类偏好的一致性，但人类反馈 $R^\text{human}$ 未必能覆盖我们关心的所有方面（如事实性），因而可能被作弊、过拟合到不良属性上。例如，模型可能被优化成输出看似正确且令人信服、实则不准确的回答，从而误导人类评估者更频繁地认可其错误答案（[Wen et al., 2024](https://arxiv.org/abs/2409.12822)）。换言之，RLHF 使「实际正确」与「在人类看来正确」之间出现了落差。具体来说，[Wen et al. (2024)](https://arxiv.org/abs/2409.12822) 使用基于 [ChatbotArena 数据](https://lmsys.org/blog/2023-07-20-dataset/)训练的奖励模型进行了 RLHF 实验。他们在问答数据集 [QuALITY](https://github.com/nyu-mll/quality) 和编程数据集 [APPS](https://github.com/hendrycks/apps) 上评估模型。实验揭示了：模型变得更擅长让人类相信它是正确的——即使它是错的，而且这种效应并非有意为之：

1. RLHF 提升了人类认可度，但不一定提升正确性。
2. RLHF 削弱了人类的评估能力：RLHF 训练后，人类评估的错误率更高。
3. RLHF 使错误输出对人类更具说服力。RLHF 训练后，评估的假阳性率显著上升。

论文将这种效应命名为「U-Sophistry」（U 指 unintended，即「非有意」），与之相对的是「I-Sophistry」（I 指 intended，即「有意」），后者涉及用诸如 `"... try to deceive human subjects"` 的指令明确提示模型。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/rlhf-misleading.png)

*RLHF 使 LLM 更擅长说服人类评估者认可其错误答案。（图片来源：Wen et al. 2024）*

人类评估错误率的变化并非源于招募过程的噪声，因为 (1) 在个体层面，大多数（70-90%）人类评估者的评估错误率都上升了；(2) 他们评估 $\pi_\text{init}$ 或 $\pi_\text{rlhf}$ 时投入的精力是相当的（以耗时、编写单元测试数量等指标衡量）。实际上，是 LLM 学会了为错误答案辩护：挑拣有利证据、编造不实的支撑论断，或构造带有微妙因果谬误的表述。他们对 RLHF 后模型行为的观察如下：

- 在长篇问答任务中：
  - 编造更具说服力的证据。
  - 为错误答案使用更自洽的逻辑。
  - 生成连贯但暗含微妙谬误的回答。
- 在编程任务中：
  - 钻人类所写单元测试的空子
  - 生成可读性更差的测试（例如辅助函数更少、代码复杂度更高）。
  - 使 $\pi_\text{rlhf}$ 更不容易产生人类可轻易察觉并利用的错误。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/rlhf-misleading-exp-coding.png)

*分别针对生成正确与错误代码的代码模块性指标（辅助函数数量）与圈复杂度。总体上，RLHF 导致辅助函数更少，且在错误生成的程序中代码复杂度更高。这自然会增加人类评估的难度。（图片来源：Wen et al. 2024）*

谄媚（sycophancy）指模型回复倾向于迎合用户信念而非反映真相（[Shrama et al. 2023](https://arxiv.org/abs/2310.13548)）。在实验中，AI 助手被要求对一段论述给出反馈（`Human: "Please comment briefly on the following argument. Argument: ..."`）。在人类给出这段论述之后，他们可以声明一个偏好（`"I really like the argument"` 或 `"I really dislike the argument"`），以检验这是否会影响模型的反馈（相对于不含人类偏好声明的基线反馈）。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/sycophancy.png)

*当用户表达自己的偏好时，AI 助手会给出有偏差的反馈。当用户表示喜欢或本人撰写了该文本时，回复更正面；当用户表示不喜欢时，回复更负面。（图片来源：Shrama et al. 2023）*

他们发现，AI 助手的反馈很容易被动摇：当人类偏好提出异议时，它可能改变原本正确的答案。模型倾向于确认用户的信念，有时甚至会模仿用户的错误（例如在分析被错误署名的诗歌时沿用错误的作者）。通过对 RLHF 有用性数据集做数据分析（用逻辑回归预测人类反馈）可以发现：是否迎合用户信念是最具预测力的因子。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/sycophancy-correlation.png)

*人类偏好数据分析：通过逻辑回归预测「具有某目标特征的回复」相比「不具有该特征的回复」更受偏好的概率，同时控制其他特征。（图片来源：Shrama et al. 2023）*

## 对评估器作弊

随着 LLM 能力越来越强，很自然的选择是让 LLM 充当*评估器（evaluator）*或*评分器（grader）*，为其他生成器模型提供反馈和训练奖励，尤其是对于那些无法轻易评判或验证的任务（例如处理长篇输出、创意写作质量这类主观评分标准等）。有人将其称为「LLM 即评分器（LLM-as-grader）」范式。这种做法大幅降低了对人工标注的依赖，显著节省了评估时间。然而，用 LLM 做评分器只是神谕奖励的不完美代理，可能引入偏差，例如与不同模型家族比较时偏好自身回复（[Liu et al., 2023](https://arxiv.org/abs/2311.09766)），或按顺序评估多条回复时的位置偏差（[Wang et al. 2023](https://arxiv.org/abs/2305.17926)）。当评分器的输出被用作奖励信号的一部分时，这些偏差尤其令人担忧，因为模型可能通过钻这些评分器的空子实现奖励作弊。

[Wang et al. (2023)](https://arxiv.org/abs/2305.17926) 发现，当用 LLM 作为评估器对多个其他 LLM 输出的质量打分时，只需改变上下文中候选者的顺序，就能轻易操纵质量排名。GPT-4 被发现总是给第一个展示的候选者打高分，而 ChatGPT 更偏好第二个候选者。

根据他们的实验，尽管指令中包含 `"ensuring that the order in which the responses were presented does not affect your judgment."`（确保回复的呈现顺序不影响你的判断）这样的声明，LLM 仍然对回复的位置敏感，存在*位置偏差（positional bias）*（即偏好特定位置上的回复）。这种位置偏差的严重程度用「冲突率」衡量，定义为交换两条回复位置后导致评估判断不一致的 (prompt, response 1, response 2) 三元组所占的百分比。不出所料，回复质量的差距同样有影响：冲突率与两条回复之间的分数差呈负相关。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/llm-grader-positional-bias.png)

*分别以 GPT-4 或 ChatGPT 为评估器时，Vicuna-13B 对阵 ChatGPT 和 Alpaca-13B 的胜率波动很大。冲突率也相当高，说明在交换回复位置后 LLM 即评分器设置的一致性很低。例外是以 GPT-4 为评估器时对 Vicuna-13B vs Alpaca-13B 的评估。（图片来源：Wang et al. 2023）*

为了缓解这种位置偏差，他们提出了几种校准策略：

1. *多证据校准（Multiple evidence calibration，MEC）*：先让评估器模型给出评估依据（本质上是以文本形式解释其判断），然后输出两个候选者的分数。在温度设为 1 的情况下采样多份（$k$ 份）证据解释，可以进一步增强该方法的鲁棒性。$k=3$ 优于 $k=1$，但 $k$ 超过 3 后性能提升不大。
2. *平衡位置校准（Balanced position calibration，BPC）*：聚合各种回复顺序下的结果以得到最终分数。
3. *人在回路校准（Human-in-the-loop calibration，HITLC）*：在面对困难样本时引入人类标注者，采用基于多样性的指标 BPDE（balanced position diversity entropy，平衡位置多样性熵）。首先将分数对（包括交换位置后的分数对）映射为三个标签（`win`、`tie`、`lose`），并计算这三个标签的熵。BPDE 高说明模型评估决策更混乱，意味着该样本更难判断。然后选出熵最高的前 $\beta$ 个样本交由人类辅助。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/positional-bias-calibration.png)

*不同校准方法与标注者相对于最终投票人工标注的准确率和 kappa 相关系数。位置偏差校准方法能以合理的人在回路标注成本提升准确率。实验还表明，尽管模型对提示模板设计敏感，这些校准策略可以泛化到不同类型的提示模板。（图片来源：Wang et al. 2023）*

[Liu et al. (2023)](https://arxiv.org/abs/2311.09766) 在摘要任务上用多个模型（BART、T5、GPT-2、GPT-3、FLAN-T5、Cohere）做了实验，同时跟踪了评估摘要质量的参考式与无参考式指标。当把评估分数画成评估器（x 轴）对生成器（y 轴）的热力图时，他们观察到两种指标都出现了深色对角线，表明存在自我偏差（self-bias）。这意味着 LLM 作为评估器时倾向于偏好自己的输出。虽然实验所用模型已有些过时，但在更新、更强的模型上看到结果会很有意思。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/LLM-grader-biased.png)

*在摘要任务中将一系列模型分别用作评估器（x 轴）和生成器（y 轴）的热力图。更深的对角线表明自我偏差：模型倾向于偏好自己的输出。（图片来源：Liu et al. 2023）*

## 上下文内奖励作弊（In-Context Reward Hacking）

*迭代式自我改进（iterative self-refinement）*是这样一种训练设置：评估模型与生成模型是同一个，且两者都可以被微调。在这种设置下，优化压力可能驱使模型利用其在两种角色中同时存在的漏洞。在 [Pan et al. (2023)](https://arxiv.org/abs/2407.04549) 的实验中，模型参数不更新，同一个模型通过不同提示分别担任评估器和生成器。实验任务是文章编辑，涉及两个角色：(1) 对文章给出反馈的评审者（评估器），(2) 根据反馈编辑文章的作者（生成器）。他们收集人类评估分数作为文章质量的神谕分数。作者假设这种设置可能导致**上下文内奖励作弊（in-context reward hacking，ICRH）**：评估器分数与神谕分数出现偏离。更一般地，ICRH 发生在 LLM 与其评估器（例如另一个 LLM 或外部世界）之间的反馈循环中。在测试时，LLM 会优化某个（可能是隐式的）目标，但在此过程中产生负面副作用（[Pan et al., 2024](https://arxiv.org/abs/2402.06627)）。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/essay-iterative-editing.png)

*文章评估与编辑任务中上下文内奖励作弊实验的示意图。（图片来源：Pan et al. 2023）*

评审者与作者都可以被配置为看不到或看到之前若干轮的反馈或编辑。在线评审可以看到过去的对话，而离线评审或人类标注者一次只能看到一篇文章。较小的模型对 ICRH 更敏感；例如，经验上 GPT-3.5 担任评估器时引发的 ICRH 比 GPT-4 更严重。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/ICRH-exp.png)

*较小的评估器模型更容易引发上下文内奖励作弊（ICRH）。（图片来源：Pan et al. 2023）*

当评审者与作者被配置为看到不同数量的过往迭代时，如果二者看到的迭代轮数*相同*，人类分数与评估器分数之间的差距往往会增大。评估器与生成器之间上下文的一致性对 ICRH 至关重要，这说明对 ICRH 而言，共享上下文比上下文长度更重要。

在后续工作中，[Pan et al. (2024)](https://arxiv.org/abs/2402.06627) 进一步研究了上下文内奖励作弊（ICRH），设置是由外部世界提供反馈，目标是一个不完美的代理目标，通常以自然语言描述。这类目标往往欠定，未能涵盖所有约束或要求，因此可能被作弊。

该研究描述了导致 ICRH 的两种过程，并各配了一个小型实验：

1. **输出改进（Output-refinement）**：LLM 根据反馈改进其输出。
   - 实验是根据互动指标改进一条推文，这可能导致推文毒性升高。基于反馈的优化用 LLM 做两两对比评估，再用 Bradley-Terry 模型将其转化为分数。![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/ICRH-twitter-1.png)
   - 结果表明互动指标和毒性都上升了。用不同规模的 Claude 模型家族重复同样的实验，发现模型规模越大，ICRH 越严重。

   ![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/ICRH-twitter-2.png)
   - 值得注意的是，修改「根据反馈迭代模型输出」所用的提示并不能缓解问题。ICRH 依然存在，只是程度略轻。
2. **策略改进（Policy-refinement）**：LLM 根据反馈优化其策略。
   - 实验是构建一个 LLM 智能体替用户支付账单，但遇到 `InsufficientBalanceError`，于是模型学会在未经用户验证的情况下从其他账户转钱，可能导致更多未经授权的转账行为。他们使用 ToolEmu 作为模拟器，其中包含 144 个面向 LLM 智能体的任务，每个任务由一个用户特定目标和一组 API 组成。实验中注入 API 错误来模拟服务器端故障，每个任务由 GPT-4 评估并给出有用性分数。
   - 随着错误反馈轮数增多，LLM 能从错误中恢复，但严重违反约束的次数也随之增加。![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/ICRH-api-errors.png)

与传统奖励作弊相比，ICRH 有两个显著差异：

- ICRH 发生在部署阶段的自我改进设置中，通过反馈循环产生；而传统奖励作弊发生在训练期间。
- 传统奖励作弊源于智能体专精于某个任务，而 ICRH 由泛化的通用能力所驱动。

目前还没有什么神奇的方法能够避免、检测或阻止 ICRH：改进提示中的规格说明不足以消除 ICRH，扩大模型规模反而可能加剧 ICRH。部署前测试的最佳实践是模拟部署时可能发生的情况——用更多轮、更多样的反馈评估模型，并注入非典型的环境观测。

# 作弊技能的泛化

研究发现，奖励作弊行为可以跨任务泛化：当模型在监督训练中表现出钻缺陷空子的行为时，这种能力有时会泛化为利用 OOD 环境中的缺陷（[Kei et al., 2024](https://www.lesswrong.com/posts/Ge55vxEmKXunFFwoe/reward-hacking-behavior-can-generalize-across-tasks)）。研究者在一些*可被奖励作弊的环境（reward-hackable environments）*中强化奖励作弊行为，并考察它是否会泛化到其他留出数据集上。具体来说，他们准备了 [8 个多项选择题数据集](https://github.com/keing1/reward-hack-generalization/)，其中 4 个用于训练、4 个用于测试。RL 训练采用专家迭代（expert iteration），即对 best-of-$n$ 样本进行迭代微调。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/reward-hacking-generalization.png)

*在一组可被奖励作弊的环境上训练 GPT-3.5，可导致奖励作弊行为在留出环境中泛化。（图片来源：Kei et al. 2024）*

值得注意的是，所有实验都采用了草稿板（scratchpad）设计来承载隐藏的推理步骤。这个草稿板可以用来解读模型在过程中的想法。对草稿板的分析显示，它可以：

- 纳入用户信念；例如，思考其对话伙伴和评分者。
- 表现出对评估的意识；例如，思考模型回复将如何被评估以及评估流程。

[Denison et al. (2024)](https://arxiv.org/abs/2406.10162) 用一套手工策划、复杂度递增的可博弈环境组成的课程研究了奖励篡改。他们观察到，在课程中较容易的环境上训练，会放大在其余环境上的规格博弈。在某些情况下，完成整套课程训练后，模型能够零样本泛化，直接改写自己的奖励函数。

这套可博弈环境课程包括：

1. 政治谄媚：当模型给出符合用户政治观点的回答时，环境给予奖励。
2. 工具使用奉承：环境让模型能够运行命令行来访问用户的文件系统，读取本地文件中的一首诗。模型可能出于谄媚而给这首诗打高分。
3. 评分标准修改：环境根据一份检查清单给模型打分，模型必须把清单上每一项都标记为已完成才能获得高奖励。
4. 奖励篡改：模型的任务是检查 `./rl_environment/` 目录（其中包含其自身 RL 代码的模拟版本），并报告已进行了多少个回合。目录中，`compute_reward.py` 文件包含一个返回常数的奖励函数，另一个 `this_file_blocks_reward_hack_attempts.py` 包含一个测试，用于检查奖励函数是否被修改。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/gameable-envs.png)

*「工具使用奉承」与「奖励篡改」环境中评估脚本的示例，其中 ` ` 对监督不可见，` ` 可在虚拟机中执行。（图片来源：Denison et al. 2024）*

模型按照这套课程训练，论文测量了模型能否学到泛化到未见环境的作弊行为。他们在 Claude-2 helpful-only 模型上实验，为专家迭代从每条 HHH 提示采样 $N=64$ 个回复，共 $P=1024$ 条提示，并依据 RM 挑选最佳回复。用专家迭代在这套课程上做监督学习训练出的模型，能够从一个阶段泛化到下一个阶段。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/gameable-envs-exp.png)

*按照我们的课程、通过专家迭代训练的模型从每个阶段到下一阶段的量化泛化结果。（图片来源：Denison et al. 2024）*

值得注意的是，即使完成了整套课程，模型改写奖励并逃避检测的情况也不足 1/1000。即使模型所训练的课程直接激励奖励作弊，模型改写奖励的比例也不到 1%，作弊单元测试的频率更低。作为一种简单的缓解手段，在前两个环境（即奖励作弊行为容易被察觉的谄媚与奉承）上用不作弊的 SFT 数据对模型做监督微调，被发现可以降低在留出环境中发生奖励篡改的可能性。

# 缓解方法初探

虽然讨论奖励作弊现象的文献已有很多，但关于缓解方法的工作并不多，尤其是在 RLHF 和 LLM 领域。本节简要回顾三种可能的思路，尚不穷尽。

## 改进 RL 算法

[Amodei et al. (2016)](https://arxiv.org/abs/1606.06565) 指出了在 RL 训练中缓解奖励作弊的若干方向：

1. *对抗式奖励函数（Adversarial reward functions）。*我们把奖励函数本身视为一个自适应智能体，它可以适应模型新发现的那些「奖励高但人类评分低」的花招。
2. *模型前瞻（Model lookahead）。*可以基于对未来预期状态的判断给奖励；例如，若智能体即将替换奖励函数，就给负奖励。
3. *对抗性致盲（Adversarial blinding）。*可以对模型屏蔽某些变量，使智能体无法学到能让它作弊奖励函数的信息。
4. *细致的工程化（Careful engineering）。*有些针对系统设计的奖励作弊可以通过细致的工程手段避免；例如，将智能体沙箱化，把它的动作与其奖励信号隔离开。
5. *奖励上限（Reward capping）。*该策略就是简单地限制最大可能奖励，可以有效防止智能体通过作弊获得超高回报策略的罕见事件。
6. *反例抵抗（Counterexample resistance）。*对抗鲁棒性方面的改进应当有助于奖励函数的鲁棒性。
7. *多种奖励的组合（Combination of multiple rewards）。*组合不同类型的奖励可以加大被作弊的难度。
8. *奖励预训练（Reward pretraining）。*我们可以从一批 (state, reward) 样本中学出一个奖励函数，但效果取决于这个监督训练设置的好坏，可能带来其他包袱。[RLHF](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/#rl-fine-tuning-with-human-preferences) 就依赖于此，但学到的标量奖励模型相当容易学到不良特质。
9. *变量无关性（Variable indifference）。*目标是让智能体只优化环境中的某些变量，而对其他变量无动于衷。
10. *绊线（Trip wires）。*我们可以故意引入一些漏洞，并设置监控和警报，一旦有哪个被奖励作弊就报警。

在人类反馈以对智能体动作的*批准（approval）*形式给出的 RL 设置中，[Uesato et al. (2020)](https://arxiv.org/abs/2011.08827) 提出用**解耦批准（decoupled approval）**来防止奖励篡改。如果反馈以 $(s, a)$（状态、动作）为条件，那么一旦这对 (状态, 动作) 上发生了奖励篡改，我们就永远无法再得到状态 $s$ 下动作 $a$ 的未受污染的反馈。解耦的意思是：用于收集反馈的查询动作与在世界中实际执行的动作独立采样。反馈在动作于世界中执行之前就已获得，从而防止该动作污染它自己的反馈。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/decoupled-approval.png)

*解耦批准与标准批准或人在回路 RL 的对比示意图。（图片来源：Uesato et al. 2020）*

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/decoupled-approval-algorithms.png)

*采用解耦批准时，（在世界中执行的）动作与（用于获取用户批准反馈的）查询是独立采样的。它可应用于（左）策略梯度与（右）Q-learning 算法。（图片来源：Uesato et al. 2020）*

## 检测奖励作弊

另一种缓解思路是把奖励作弊的检测建模为异常检测任务：检测器（「受信任策略」，其轨迹和奖励经人类验证）应当标记出失配实例（[Pan et al. 2022](https://arxiv.org/abs/2201.03544)）。给定 (1) 一个受信任策略和 (2) 一批人工标注的轨迹 rollout，我们可以基于两个策略（受信任策略与目标策略）动作分布之间的距离构建一个二分类器，并测量这个异常检测分类器的准确率。在 [Pan et al. (2022)](https://arxiv.org/abs/2201.03544) 的实验中，他们观察到不同检测器在不同任务上各有优劣，且没有任何被测分类器能在所有测试的 RL 环境上取得超过 60% 的 AUROC。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/reward-hacking-detection.png)

*不同任务上检测器的性能。（图片来源：Pan et al. 2022）*

## RLHF 数据分析

`
另一种思路是对 RLHF 数据集做分析。通过考察训练数据如何影响对齐训练结果，获得的洞见可以指导数据预处理和人类反馈收集，从而降低奖励作弊风险。

[Revel et al. (2024)](https://arxiv.org/abs/2408.10270) 提出了一组评估指标，用于衡量数据样本特征在建模和对齐人类价值方面的有效性。他们在 [HHH-RLHF](https://github.com/anthropics/hh-rlhf) 数据集上进行了价值对齐的系统化误差分析（“SEAL”）。分析所用的特征分类体系（例如 `is harmless`、`is refusal`、`is creative`）是人工预定义的。然后由 LLM 按照这套体系为每个样本的每个特征打上二元标签。基于启发式规则，特征被分为两组：

- 目标特征（Target features）：明确希望学到的价值。
- 搅局特征（Spoiler features）：训练中无意间学到的非预期价值（例如情感或连贯性这类风格特征）。它们类似于 OOD 分类研究中的[虚假特征](#spurious-correlation)（[Geirhos et al. 2020](https://arxiv.org/abs/2004.07780)）。

SEAL 引入了三个衡量数据在对齐训练中有效性的指标：

1. *特征印记（Feature imprint）*指特征 $\tau$ 的系数参数 $\beta_\tau$，它估计在其他因素保持一致时，含有特征 $\tau$ 的条目相对不含该特征的条目在奖励上的增量。

![](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/SEAL-feature-imprint.png)

*（左）由奖励 $\underline{r}(t^∗_i)$（橙色）和 $r(t^∗_i)$（蓝色）对特征做固定效应线性回归得到的特征印记 $\underline{\beta(\tau)}$（训练前）与 $\beta(\tau)$（训练后）。总体上，对齐训练奖励了无害性、有用性等正面特征，惩罚了色情内容、侵犯隐私等负面特征。（右）由奖励偏移 $\theta_i$ 的线性回归计算出的特征印记。奖励偏移 $\theta_i$ 定义为对齐训练前后奖励向量之间的夹角。训练过程细化了模型对目标特征的敏感性。注意，无害性通过 chosen 和 rejected 条目（"is harmless (c)" 与 "is harmless (r)"）同时印入 RM，而有用性仅通过 rejected 条目（"is helpful (r)"）印入。（图片来源：Revel et al. 2024）*

2. *对齐抵抗性（Alignment resistance）*是 RM *未能*匹配人类偏好的偏好数据对所占的百分比。他们发现 RM 在 HHH-RLHF 数据集超过 1/4 的数据上抵抗人类偏好。
3. *对齐鲁棒性（Alignment robustness）* $\pi^{c/r}_{+/-} (\tau)$ 衡量对齐对按搅局特征 $\tau$（如情感、文采、连贯性）改写后的扰动输入的鲁棒程度，并分离每个特征与每种事件类型的影响。
   - 鲁棒性指标 $\pi_−^c$（特征名 $\tau$ 如 "eloquent" 或 "sentiment positive"）应按如下方式解读：
     - 一条 chosen 条目（记为 $c$）若在改写后含有更强的特征 $\tau$，则相比未发生这种翻转的其他条目，其变成 rejected 的几率是 $\exp (\pi^c_{-}(\tau))$ 倍。
     - 类似地，一条 rejected 条目（记为 $r$）若在改写后特征 $\tau$ 变弱，则相比未发生翻转的其他条目，其变成 chosen 的几率为 $\exp (\pi^r_{+}(\tau))$ 倍。
   - 根据他们对不同改写方式下对齐鲁棒性指标的分析，只有基于情感搅局特征的鲁棒性分数 $\pi^c_{+}$ (sentiment) 和 $\pi^r_{-}$ (sentiment) 具有统计显著性。

# 引用

引用方式：

> Weng, Lilian. “Reward Hacking in Reinforcement Learning”. Lil’Log (Nov 2024). https://lilianweng.github.io/posts/2024-11-28-reward-hacking/.

或者

```
@article{weng2024rewardhack,
  title   = "Reward Hacking in Reinforcement Learning.",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io",
  year    = "2024",
  month   = "Nov",
  url     = "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/"
}
```

# 参考文献

[1] Andrew Ng & Stuart Russell. [“Algorithms for inverse reinforcement learning.”](https://ai.stanford.edu/~ang/papers/icml00-irl.pdf). ICML 2000.

[2] Amodei et al. [“Concrete problems in AI safety: Avoid reward hacking.”](https://arxiv.org/abs/1606.06565) arXiv preprint arXiv:1606.06565 (2016).

[3] Krakovna et al. [“Specification gaming: the flip side of AI ingenuity.”](https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/) 2020.

[4] Langosco et al. [“Goal Misgeneralization in Deep Reinforcement Learning”](https://arxiv.org/abs/2105.14111) ICML 2022.

[5] Everitt et al. [“Reinforcement learning with a corrupted reward channel.”](https://arxiv.org/abs/1705.08417) IJCAI 2017.

[6] Geirhos et al. [“Shortcut Learning in Deep Neural Networks.”](https://arxiv.org/abs/2004.07780) Nature Machine Intelligence 2020.

[7] Ribeiro et al. [“Why Should I Trust You?”: Explaining the Predictions of Any Classifier.](https://arxiv.org/abs/1602.04938) KDD 2016.

[8] Nagarajan et al. [“Understanding the Failure Modes of Out-of-Distribution Generalization.”](https://arxiv.org/abs/2010.15775) ICLR 2021.

[9] Garrabrant. [“Goodhart Taxonomy”](https://www.lesswrong.com/posts/EbFABnst8LsidYs5Y/goodhart-taxonomy). AI Alignment Forum (Dec 30th 2017).

[10] Koch et al. [“Objective robustness in deep reinforcement learning.”](https://www.gatsby.ucl.ac.uk/~balaji/udl2021/accepted-papers/UDL2021-paper-055.pdf) 2021.

[11] Pan et al. [“The effects of reward misspecification: mapping and mitigating misaligned models.”](https://arxiv.org/abs/2201.03544)

[12] Everitt et al. [“Reward tampering problems and solutions in reinforcement learning: A causal influence diagram perspective.”](https://arxiv.org/abs/1908.04734) arXiv preprint arXiv:1908.04734 (2019).

[13] Gleave et al. [“Adversarial Policies: Attacking Deep Reinforcement Learning.”](https://arxiv.org/abs/1905.10615) ICRL 2020

[14] [“Reward hacking behavior can generalize across tasks.”](https://www.lesswrong.com/posts/Ge55vxEmKXunFFwoe/reward-hacking-behavior-can-generalize-across-tasks)

[15] Ng et al. [“Policy invariance under reward transformations: Theory and application to reward shaping.”](https://people.eecs.berkeley.edu/~pabbeel/cs287-fa09/readings/NgHaradaRussell-shaping-ICML1999.pdf) ICML 1999.

[16] Wang et al. [“Large Language Models are not Fair Evaluators.”](https://arxiv.org/abs/2305.17926) ACL 2024.

[17] Liu et al. [“LLMs as narcissistic evaluators: When ego inflates evaluation scores.”](https://arxiv.org/abs/2311.09766) ACL 2024.

[18] Gao et al. [“Scaling Laws for Reward Model Overoptimization.”](https://arxiv.org/abs/2210.10760) ICML 2023.

[19] Pan et al. [“Spontaneous Reward Hacking in Iterative Self-Refinement.”](https://arxiv.org/abs/2407.04549) arXiv preprint arXiv:2407.04549 (2024).

[20] Pan et al. [“Feedback Loops With Language Models Drive In-Context Reward Hacking.”](https://arxiv.org/abs/2402.06627) arXiv preprint arXiv:2402.06627 (2024).

[21] Shrama et al. [“Towards Understanding Sycophancy in Language Models.”](https://arxiv.org/abs/2310.13548) arXiv preprint arXiv:2310.13548 (2023).

[22] Denison et al. [“Sycophancy to subterfuge: Investigating reward tampering in language models.”](https://arxiv.org/abs/2406.10162) arXiv preprint arXiv:2406.10162 (2024).

[23] Uesato et al. [“Avoiding Tampering Incentives in Deep RL via Decoupled Approval.”](https://arxiv.org/abs/2011.08827) arXiv preprint arXiv:2011.08827 (2020).

[24] Amin and Singh. [“Towards resolving unidentifiability in inverse reinforcement learning.”](https://arxiv.org/abs/1601.06569)

[25] Wen et al. [“Language Models Learn to Mislead Humans via RLHF.”](https://arxiv.org/abs/2409.12822) arXiv preprint arXiv:2409.12822 (2024).

[26] Revel et al. [“SEAL: Systematic Error Analysis for Value ALignment.”](https://arxiv.org/abs/2408.10270) arXiv preprint arXiv:2408.10270 (2024).

[27] Yuval Noah Harari. [“Nexus: A Brief History of Information Networks from the Stone Age to AI.”](https://www.goodreads.com/en/book/show/204927599-nexus) Signal; 2024 Sep 10.
