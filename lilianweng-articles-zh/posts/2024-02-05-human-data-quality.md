---
title: "关于高质量人类数据的思考"
title_en: "Thinking about High-Quality Human Data"
source: https://lilianweng.github.io/posts/2024-02-05-human-data-quality/
crawled: 2026-09-08
translated: 2026-09-08
---

[特别感谢 [Ian Kivlichan](https://scholar.google.com/citations?user=FRBObOwAAAAJ&hl=en) 提供许多有用的线索（如那篇 100 多年前的 Nature 论文 "Vox populi"）与精彩反馈。🙏 ]

> 原文：[Thinking about High-Quality Human Data](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/) · Lilian Weng（翁荔）

高质量数据是现代深度学习模型训练的燃料。大多数任务专属标注数据来自人工标注，如分类任务，或用于 LLM 对齐训练的 [RLHF](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/#rl-fine-tuning-with-human-preferences) 标注（可构造为分类格式）。本文中的许多 ML 技术可以帮助提升数据质量，但从根本上说，人类数据收集离不开对细节的关注与细致执行。社区知道高质量数据的价值，但不知为何我们有种微妙的印象："人人都想做模型工作，而不是数据工作"（[Sambasivan et al. 2021](https://dl.acm.org/doi/abs/10.1145/3411764.3445518)）。

![](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/overview.png)

*通往高数据质量的两个方向。*

# 人类标注者 ↔ 数据质量

收集人类数据涉及一组操作步骤，每一步都贡献于数据质量：

1. 任务设计：设计任务流程以提升清晰度、降低复杂度。详细的指南有帮助，但很长很复杂的指南需要相当多的培训才能发挥作用。
2. 选择并培训标注者池：选择技能匹配、一致性好的标注者。培训环节是必要的。入职后，还需定期反馈与校准会议。
3. 收集与聚合数据。这一阶段可以应用更多 ML 技术来清洗、过滤并聪明地聚合数据以识别真值标签。

![](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/qualit_assurance.png)

*质量保证指通过对质量模型中识别出的质量属性采取行动来提升质量的一组动作。（图片来源：Daniel et al. 2018 ）*

## 群体智慧

[Vox populi](https://en.wikipedia.org/wiki/Vox_populi)（原为 "Vox populi, vox Dei"）是拉丁语，意为人民的声音。一篇同名短文于 1907 年发表在 Nature 上。它追踪了一场年度展览上的活动：一头肥牛被选出，人们猜测牛的重量，猜得接近真实数字者获奖。居中的估计被视为"vox populi"，结果与真值非常接近。作者总结道：*"我认为，这一结果比预期更能证明民主判断的可信度。"* 这大概是关于众包（"群体智慧"）如何奏效的最早记载。

近 100 年后，[Callison-Burch (2009)](https://aclanthology.org/D09-1030/) 做了早期研究：用 Amazon Mechanical Turk（AMT）对机器翻译（MT）任务做非专家人工评估，甚至依靠非专家创建新的黄金参考翻译。人工评估的设定很简单：每位 turker 看到一个源句、一个参考翻译及来自 5 个 MT 系统的 5 个翻译，被要求把 5 个翻译从最好到最差排序。每个任务由 5 位 turker 完成。

不出意料，有垃圾制造者为凑量而产出低质量标注。因此在度量专家与非专家的一致性时，需要应用不同加权方案以降低垃圾制造者的权重：(1) "按专家加权"：用在 10 个示例的黄金集上与专家的一致率；(2) "按非专家加权"：靠与全集上其他 turker 的一致率。

在更难的任务中，非专家标注者被要求创建新的黄金参考翻译。Callison-Burch 把任务设计为两阶段：第一阶段参照 MT 输出创作新翻译，第二阶段过滤可能看似由 MT 系统生成的翻译。专家与众包翻译之间的相关性高于专家与 MT 系统输出之间的相关性。

![](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/AMT_exp.png)

*(左) 一致率通过比较每对翻译句（"A > B"、"A=B"、"A < B"）度量，因此随机一致为 1/3。上界由专家-专家一致率设定。(右) 不同来源翻译的 BLEU 分数对比。LDC（Linguistic Data Consortium）译者提供专家翻译。（图片来源：Callison-Burch 2009 ）*

## 标注者一致性

我们常把标注视为针对单一真值，并试图以一致的标准对照一个黄金答案评估质量。寻找可靠真值标签的常见做法是从多个标注者收集多个标签。假设每个标注者的质量水平不同，我们可以用标注的加权平均、按熟练度分数加权。该分数常用一个标注者与他人一致的频率来近似。

**多数投票（Majority Voting）**：取多数票是最简单的聚合方式，等价于取一组标签的[众数](https://en.wikipedia.org/wiki/Mode_(statistics))。此设定下每个标注者贡献均等。

**原始一致率（Raw agreement）**（[Tratz & Hovy, 2010](https://aclanthology.org/P10-1070/)）：原始一致率统计同意某人的他人比例。这与多数投票间接相关，因为多数类的所有成员预期获得更高的标注者间一致率。

**Cohen's Kappa**（[Landis & Koch, 1977](https://www.jstor.org/stable/2529310)）：Cohen's kappa 以 $\kappa = (p_o - p_e) / (1 - p_c)$ 的形式度量标注者间一致性，其中 $p_o$ 是原始一致率，$p_e$ 是随机一致。Cohen's kappa 对随机一致有矫正项，但当某一标签更普遍时该矫正可能被高估。

**概率图建模**：有一批工作依靠[概率图建模](https://en.wikipedia.org/wiki/Graphical_model)来建模标注决策中的不同因素，如任务难度、任务潜在主题、标注者偏差、标注者信心，然后据此预测真值标签。[Zheng et al. (2017)](https://dl.acm.org/doi/abs/10.14778/3055540.3055547) 比较了 17 种众包真值推断算法，其中多数是概率图模型。

- **MACE**（Multi-Annotator Competence Estimation；[Hovy et al. 2013](https://aclanthology.org/N13-1132)）是早期用图建模估计某人像"垃圾制造者"那样提供随机标签之可能性的例子。不出意料，激励错位时一些标注者可能表现为"垃圾制造者"以优化完成的任务量来赚更多报酬。MACE 的目标就是识别垃圾制造者。给定任务 $i$ 与标注者 $j$，$T_i$ 是真值标签，$A_{ij}$ 是分配的标签，$S_{ij}$ 建模标注者 $j$ 制造垃圾的概率。生成过程可表示如下。参数 $\theta_j$ 定义标注者 $j$ 的可信度（不制造垃圾的概率），参数 $\xi_j$ 定义标注者制造垃圾时的行为。

$$
\begin{align}
& \text{for } i = 1 \dots N : \\
& \quad T_i \sim \text{Uniform} \\
& \quad \text{for } j = 1 \dots M : \\
& \quad \quad S_{ij} \sim \text{Bernoulli}(1 - \theta_j) \\
& \quad \quad \text{if } S_{ij} = 0 : \\
& \quad \quad \quad A_{ij} = T_i \\
& \quad \quad \text{else } : \\
& \quad \quad \quad A_{ij} \sim \text{Multinomial}(\xi_j) \\
\end{align}
$$

然后我们可以学习 $\theta, \xi$ 以最大化观测数据，形式为边缘数据似然，其中 $A$ 是标注矩阵，$S$ 是能力指示矩阵，$T$ 是真值标签矩阵：

$$
P(A; \theta, \xi) = \sum_{T, S} \big[ \prod_{i=1}^N P(T_i) \cdot \prod_{j=1}^M P(S_{ij}; \theta_j) \cdot P(A_{ij} \vert S_{ij}, T_i; \xi_j) \big]
$$

可用 EM（期望最大化）或 VB（变分贝叶斯）最大化上述边缘似然。EM 优化的 M 步中，归一化前向分数计数加一个固定值 $\delta$。VB 训练中，他们对 $\theta_j$ 施加对称 Beta 先验、对 $\xi_j$ 施加对称 Dirichlet 先验。恢复正确答案时，可以取按标注者 $\theta$ 估计加权的多数票。

## 标注者分歧与两种范式

上述聚合过程依赖于一个假设：存在*唯一*的底层黄金答案，从而我们可以据此评估标注者的表现。然而在许多主题上，尤其是安全、社会或文化领域，人们会有分歧，且这种分歧往往是合理的，于是问题归结为：我们要多大程度施加严格规则，还是拥抱多样性。

[Aroyo & Welty (2015)](https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/2564) 讨论了人工标注收集实践中的一组"迷思"，发现它们都有失准确，关键发现包括：

- 一些样本常常有不止一种正确解读。我们需要多样视角，例如让多人审查标注质量。
- 分歧不总是坏事。我们应减少由错误或流程设计不良导致的分歧，但其他分歧能给我们丰富信息。
  - 若分歧源于任务定义不清，我们应增强指令。然而更详细的指南并不能解决观点间的天然多样性。
- 专家未必总比外行好，但他们在"什么重要"的考量上会有大差距。
- 真值标注会随时间变化，尤其是那些与时事或新闻相关的。

后来，[Rottger et al. (2021)](https://arxiv.org/abs/2112.07475) 把差异形式化为主观 NLP 任务数据标注的两种对立范式。

|  | 描述式（Descriptive） | 规定式（Prescriptive） |
| --- | --- | --- |
| 定义 | 鼓励标注者主观性，尝试建模多种信念。 | 不鼓励标注者主观性，尝试一致地应用单一信念。 |
| 优点 | - 能帮助识别哪些条目更主观；- 拥抱多样性 | - 更贴合标准 NLP 设定。- 更容易通过度量分歧或做标签聚合来做 QC。 |
| 缺点 | - 标注者分歧等指标无法用于度量数据质量或标注者表现；- 不能用于训练优化为输出单一预设行为的模型。 | - 高质量标注指南昂贵且难创建，实践中永远不完美；- 培训标注者熟悉指南以正确应用同样困难；- 无法捕捉可解释的信念多样性，也无法一致地编码某一特定信念。 |

描述式范式让我们能理解若干重要效应并兼顾不同视角。例如，标注者身份（如非裔美国人、LGBTQ）被发现是他们如何把身份相关内容标注为毒性的统计显著因素（[Goyal et al. 2022](https://arxiv.org/abs/2205.00501)）。主题可以是多样观点的另一主要驱动。[Wang et al. (2023)](https://research.google/pubs/all-that-agrees-is-not-gold-evaluating-ground-truth-labels-and-dialogue-content-for-safety/) 研究了 AI 对话系统安全性的人工评估流程，比较了信任与安全（T&S）专业人员的标签与众包标注者的结果。他们有意收集了与众包标注者关联的丰富元数据，如人口统计或行为信息。比较 T&S 专家标签与大众标注，他们发现一致率随语义主题与严重程度而变：

- 不同主题间一致率差异很大：从暴力/血腥上的 0.96 到个人话题上的 0.25。
- 在"极端"与"良性"对话上一致率更高——给定"良性"、"有争议"、"中度"到"极端"四个标签选项。

![](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/topic_agreement.png)

*非专家与专家标注间的相关性随主题差异很大。（图片来源：Wang et al. 2023 ）*

[Zhang et al. (2023)](https://arxiv.org/abs/2311.04345) 提出了标注者分歧的分类法来分析根因。在所列原因中，由随机误差或个体层面的不一致导致的分歧应避免。当一个标注者被多次问同一任务而给出不同标签时，其中一些很可能是人为失误。基于这一直觉，分歧去卷积方法（disagreement deconvolution；[Gordon et al. 2021](https://dl.acm.org/doi/abs/10.1145/3411764.3445423)）通过把每个人的观点锚定到其自身的主标签，从而鼓励标注者*内部*一致性，把稳定观点与失误分离。

![](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/taxonomy.png)

*标注者分歧原因的分类法。（图片来源：Zhang et al. 2023 ）*

分歧去卷积依靠概率图建模：

1. 估计一个标注者返回非主标签的频率 $p_\text{flip}$
2. 逐样本地，基于 $p_\text{flip}$ 得到主标签的调整后标签分布 $p^*$
3. 从 $p^*$ 采样作为新测试集。
4. 用新测试集度量性能指标。

给定 $C$ 类分类，生成模型的采样过程表述如下：

$$
\begin{aligned}
y^*\mid x &\sim \text{Categorial}([C], p^*(y\mid x)) \\
y_\text{other}\mid y^* &\sim \text{Categorial}([C]\setminus\{y^*\}, \frac{1}{C-1}) \\
z_\text{flip} \mid x &\sim \text{Bernoulli}(p_\text{flip}(x)) \\
y\mid y^*, y_\text{other}, z_\text{flip} &= y^* (1 - z_\text{flip}) + y_\text{other} z_\text{flip}
\end{aligned}
$$

给定可从数据估计的真 $p(y\mid x)$ 与 $p_\text{flip}$，我们更新主标签的标签分布：

$$
p^*(y\mid x) = \frac{p(y\mid x) - \frac{p_\text{flip}(x)}{C-1}}{1 - \frac{C \cdot p_\text{flip}(x)}{C - 1}}
$$

从 $p^*(y \mid x)$ 采样的新测试集代表去除了个体不一致噪声的主标签，可用作评估的无噪测试集。

为了在学习预测标签时捕捉标注者间的系统性分歧，[Davani et al. (2021)](https://arxiv.org/abs/2110.05719) 实验了多标注者模型，把预测每个标注者的标签视为一个子任务。设分类任务定义在标注数据集 $D=(X, A, Y)$ 上，其中 $X$ 是文本实例，$A$ 是标注者集合，$Y$ 是标注矩阵，$y_{ij} \in Y$ 表示 $a_j \in A$ 给样本 $x_i \in X$ 的二值标签。$x_i$ 的多数票记为 $\bar{y}_{i,}$。实验在预训练 BERT 模型上训练一个分类头并比较 4 种设定：

- 基线：直接预测多数票 $\bar{y}_i$，不使用完整标注矩阵 $Y$。
- 集成：每位标注者单独训练一个模型预测 $y_{ij}$，然后用多数票聚合。
- 多标签：学习预测 $\vert A \vert$ 个标签表示每样本所有标注者的标签 $\langle y_{i1}, \dots, y_{i\vert A \vert} \rangle$，共享一个 MLP 层，然后聚合输出。
- 多任务：类似多标签，但每位标注者的预测头由独立的 MLP 层学习，从而分配额外算力学习标注者之间的差异。

在 [GHC（Gab Hate Corpus）](https://osf.io/edua3/)数据集上的实验结果显示，多任务模型取得最佳 F1 分数，且能自然提供与标注分歧相关的预测不确定性估计。

![](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/multi_annotator_model.png)

*建模多标注者标签的不同架构示意。（图片来源：Davani et al. 2021 ）*

陪审团学习（Jury Learning；[Gordon et al. 2022](https://arxiv.org/abs/2202.02950)）通过建模不同标注者以其特征为条件的标注行为来模仿[陪审团流程](https://www.uscourts.gov/services-forms/jury-service/juror-selection-process)。从带标签与每位标注者人口统计特征的数据集出发，我们训练一个模型学习预测每位个体标注者（每位都是潜在陪审员）所做的标签。决策时，从业者可以指定一组陪审员的组成来确定采样策略。最终决策由多次试验中陪审员标签聚合做出。

![](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/jury.png)

*陪审团学习工作方式示意。（图片来源：Gordon et al. 2022 ）*

陪审团学习模型是 [DCN（Deep & Cross network）](https://arxiv.org/abs/2008.13535)——常用于推荐场景——联合训练学习评论嵌入、标注者嵌入与组（标注者特征）嵌入。文本内容由预训练 BERT 处理，也联合微调但时间较短以避免过拟合。

![](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/jury_model.png)

*陪审团学习的 DCN 模型架构。（图片来源：Gordon et al. 2022 ）*

他们的实验在[毒性多样性数据集](https://data.esrg.stanford.edu/study/toxicity-perspectives)上运行，把陪审团学习与不用元数据、微调 BERT 预测个体标注者标签的基线模型比较。性能用 MAE（平均绝对误差）度量。陪审团学习在完整测试集及每个组段上都一致优于标注者无关基线。

![](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/jury_exp.png)

*标注者无关基线与陪审团学习的实验结果对比。（图片来源：Gordon et al. 2022 ）*

# 数据质量 ↔ 模型训练

数据集构建完成后，许多方法可以依据训练动态帮助识别错误标注。注意我们只聚焦于寻找并排除标签可能错误的数据点的方法，不涉及[如何用噪声数据训练模型](https://lilianweng.github.io/posts/2022-04-15-data-gen/#training-with-noisy-data)。

## 影响函数

**影响函数（Influence functions）**是鲁棒统计学的经典技术（[Hampel, 1974](https://www.jstor.org/stable/2285666)），通过描述当我们把某个训练点的权重提升无穷小量时模型参数如何变化来度量训练数据点的作用。[Koh & Liang (2017)](https://arxiv.org/abs/1703.04730) 把该概念引入深度神经网络。

给定训练集的 $n$ 个数据样本 $z_i = (x_i, y_i)$（$i =1, \dots, n$），模型参数 $\theta$ 优化以最小化损失：$\hat{\theta} = \arg\min_{\theta \in \Theta} \frac{1}{n}\sum_{i=1}^n \mathcal{L}(z_i, \theta)$。移除单个数据点 $z$ 后模型参数的变化记为 $\hat{\theta}_{-z} - \hat{\theta}$，其中 $\hat{\theta}_{-z} = \arg\min_{\theta \in \Theta} \frac{1}{n} \sum_{z_i \neq z} \mathcal{L}(z_i, \theta)$。然而对每个样本都字面地计算太昂贵。一种近似方法是计算给 $z$ 一个小升权 $\epsilon$ 时的参数变化。按定义，把 $z$ 升权 $\epsilon$ 的影响为：

$$
\mathcal{I}_{\text{up,params}}(z) = \frac{d\hat{\theta}_{\epsilon,z}}{d\epsilon}\bigg\vert_{\epsilon=0}=-\mathbf{H}^{-1}_{\hat{\theta}} \nabla_\theta \mathcal{L}(z, \hat{\theta})
$$

其中 $\hat{\theta}_{\epsilon,z} = \arg\min_{\theta \in \Theta} \frac{1}{n}\sum_{i=1}^n \mathcal{L}(z_i, \theta) + \epsilon L(z, \theta)$，$\mathbf{H}^{-1}_{\hat{\theta}} = \frac{1}{n}\sum_{i=1}^n \nabla^2_\theta \mathcal{L}(z_i, \hat{\theta})$。
移除数据点 $x$ 等价于把升权设为 $\epsilon = -\frac{1}{n}$，因此 $\hat{\theta}_{-z} - \hat{\theta} \approx -\frac{1}{n} \mathcal{I}_{\text{up,params}}(z)$。

把 $z$ 升权对测试点 $z_\text{test}$ 处损失的影响由链式法则给出：

$$
\begin{aligned}
\mathcal{I}_{\text{up,loss}}(z, z_\text{test}) 
&= \frac{d \mathcal{L}(z_\text{test}, \hat{\theta}_{\epsilon,z})}{d\epsilon}\bigg\vert_{\epsilon=0} \\
&= \nabla_\theta \mathcal{L}(z_\text{test}, \hat{\theta})^\top \frac{d \hat{\theta}_{\epsilon,z}}{d\epsilon}\bigg\vert_{\epsilon=0} \\
&= - \nabla_\theta \mathcal{L}(z_\text{test}, \hat{\theta})^\top \mathbf{H}^{-1}_{\hat{\theta}} \nabla_\theta \mathcal{L}(z, \hat{\theta})
\end{aligned}
$$

用影响函数我们可以闭式度量单个数据点对模型参数与损失函数的作用。它能帮助近似留一重训练而无须实际运行全部重训练。为识别错标数据，我们可以度量 $\mathcal{I}_\text{up,loss}(z_i, z_i)$，近似若 $z_i$ 从训练集中移除后在 $z_i$ 上的预测误差。

![](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/influence.png)

*影响函数值与 10 类 MNIST 上留一训练结果吻合。（图片来源：Kohn & Liang, 2017 ）*

尽管有闭式，影响函数仍难扩展，因为逆 Hessian 向量积难以计算。[Grosse et al. (2023)](https://arxiv.org/abs/2308.03296) 实验了 EK-FAC（Eigenvalue-corrected Kronecker-Factored Approximate Curvature；[George et al. 2018](https://arxiv.org/abs/1806.03884)）近似。

## 训练过程中的预测变化

另一类方法追踪训练过程中模型预测的变化以识别似乎难以学习的样本。**数据地图（Data Maps）**（[Swayamdipta et al. 2020](https://arxiv.org/abs/2009.10795)）追踪训练期间模型行为动态的两个属性来分析数据集质量：

1. **置信度（Confidence）**：模型对真标签的置信度，定义为各轮次上真标签模型概率的均值。他们还用了粗粒度指标"正确率"，定义为各轮次上模型预测正确标签的比例。
2. **可变性（Variability）**：置信度的波动，定义为各轮次上真标签模型概率的标准差。

![](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/data_map.png)

*基于 RoBERTa 分类器的 SNLI 训练集数据地图。（图片来源：Swayamdipta et al. 2020 ）*

难学（低置信、低可变性）样本更可能被错标。他们在带 1% 翻转标签数据的 WinoGrande 数据集上做实验。重训后，被翻转的实例移到低置信、略高可变性区域，表明难学区域含错标样本。据此，我们可以只用置信度分数在等量的标签翻转与干净样本上训练一个分类器（不确定论文为何不同时用置信度与可变性作特征）。这个简单的噪声分类器随后可用于原数据集以识别潜在错标实例。

![](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/flip_exp.png)

*原本高置信、低可变性的数据点在标签翻转后移到低置信、略高可变性区域。（图片来源：Swayamdipta et al. 2020 ）*

然而，我们不应把所有难学样本都视为错误。事实上，论文假设模糊（高可变性）与难学（低置信、低可变性）样本对学习更有信息量。实验表明它们有利于 OOD 泛化，在 OOD 评估上给出更好结果，甚至优于 100% 训练集。

为研究神经网络是否有**遗忘**已学信息的倾向，[Toneva et al. (2019)](https://arxiv.org/abs/1812.05159) 设计了一个实验：追踪训练过程中每个样本的模型预测，统计每个样本从被正确分类到错误分类（或相反）的转移。然后据此归类样本：

- *可遗忘（多余）样本*：若类别标签在训练各轮间变化。
- *不可遗忘样本*：若类别标签分配在训练各轮间一致。这些样本一旦学会就永不遗忘。

他们发现有大量一旦学会就永不遗忘的不可遗忘样本。带噪声标签的样本或有"不常见"特征（视觉上难分类）的图像属于最容易被遗忘的样本。实验经验性地验证了不可遗忘样本可以安全移除而不损害模型性能。

实现中，遗忘事件只在样本被纳入当前训练批次时计数；即他们计算同一样本在后续 mini-batch 中的呈现之间的遗忘。每样本的遗忘事件数在不同随机种子间相当稳定，且可遗忘样本略有在训练后期才首次学会的倾向。遗忘事件还被发现可在训练期间与架构之间迁移。

[Pleiss, et al. (2020)](https://arxiv.org/abs/2001.10528) 开发了 **AUM（Area under the Margin，边缘下面积）**方法，基于如下假设发现错误标签：设一张 BIRD（鸟）图被误标为 DOG（狗）。梯度更新会鼓励从其他 BIRD 图泛化到这张 BIRD 图，而 DOG 标签提供错误的监督信号驱使更新走向另一方向。于是，泛化与（错误）预测在梯度更新信号中存在张力。

给定分类数据集 $(\mathbf{x}, y) \in \mathcal{D}_\text{train}$，设 $z^{(t)}_i(\mathbf{x}) \in \mathbb{R}$ 为第 $t$ 轮对应类 $i$ 的 logit。第 $t$ 轮的边缘（margin）是所赋 logit 与次大 logit 之差：

$$
M^{(t)}(\mathbf{x}, y) = z_y^{(t)}(\mathbf{x}) - \max_{i \neq y} z^{(t)}_i(\mathbf{x}),\quad
\text{AUM}(\mathbf{x}, y) = \frac{1}{T} \sum^T_{t=1} M^{(t)}(\mathbf{x}, y)
$$

负边缘表示错误预测，大正边缘表明对正确预测的高置信。假设是：由于其他样本触发的 SGD 泛化张力，错标样本的边缘会小于正确样本。

为确定阈值，他们插入称为"阈值样本"的假数据来确定阈值：

1. 创建阈值样本子集 $\mathcal{D}_\text{thr}$。若 $C$ 类有 $N$ 个训练样本，随机采样 $N/(C+1)$ 个样本并把其标签全部换为假的新类 $C+1$。
2. 把阈值样本并入原数据集：$\mathcal{D}’ = { (\mathbf{x}, C+1): \mathbf{x} \in \mathcal{D}_\text{thr}} \cup (\mathcal{D} \setminus\mathcal{D}_\text{thr})$；
3. 在 $\mathcal{D}’$ 上训练模型并度量全部数据的 AUM；
4. 以阈值样本 AUM 的第 99 百分位计算阈值 $\alpha$；
5. 用 $\alpha$ 作阈值识别错标数据：${(\mathbf{x}, y) \in \mathcal{D} \setminus \mathcal{D}_\text{thr}: \text{AUM}_{\mathbf{x}, y} \leq \alpha}$

![](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/AUM_threshold.png)

*阈值样本的 AUM 如何帮助分离出错标样本。（图片来源：Pleiss et al. 2020 ）*

![](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/AUM_exp.png)

*带随机错标样本的 CIFAR 10/100 上的测试误差，比较不同的数据过滤或噪声数据训练方法。（图片来源：Pleiss et al. 2020 ）*

## 噪声交叉验证

**NCV（Noisy Cross-Validation，噪声交叉验证）**方法（[Chen et al. 2019](https://arxiv.org/abs/1905.05040)）把数据集随机一分为二，若某样本的标签与仅在另一半数据集上训练的模型所预测的标签一致，则识别为"干净"。干净样本预期更可信。INCV（迭代噪声交叉验证）迭代运行 NCV，把更多干净样本加入可信候选集 $\mathcal{C}$、移除更多噪声样本。

![](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/INCV_algo.png)

*INCV（迭代噪声交叉验证）算法。（图片来源：Chen et al. 2019 ）*

# 引用

引用格式：

> Weng, Lilian. (Feb 2024). "Thinking about High-Quality Human Data". Lil'Log. https://lilianweng.github.io/posts/2024-02-05-human-data-quality/.

或

```
@article{weng2024humandata,
  title   = "Thinking about High-Quality Human Data",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io",
  year    = "2024",
  month   = "Feb",
  url     = "https://lilianweng.github.io/posts/2024-02-05-human-data-quality/"
}
```

# 参考文献

[1] Francis Galton ["Vox populi"](https://www.nature.com/articles/075450a0) Nature 75, 450-451 (1907).

[2] Sambasivan et al. ["Everyone wants to do the model work, not the data work": Data Cascades in High-Stakes AI"](https://dl.acm.org/doi/10.1145/3411764.3445518) CHI 2021

[3] Chris Callison-Burch. ["Fast, Cheap, and Creative: Evaluating Translation Quality Using Amazon's Mechanical Turk"](https://aclanthology.org/D09-1030/) EMNLP 2009

[4] Rottger et al. ["Two Contrasting Data Annotation Paradigms for Subjective NLP Tasks"](https://arxiv.org/abs/2112.07475) NAACL 2022.

[5] Aroyo & Welty ["Truth Is a Lie: Crowd Truth and the Seven Myths of Human Annotation"](https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/2564) AI Magazine 36.1: 15-24 (2015).

[6] Hovy et al. ["Learning Whom to Trust with MACE"](https://aclanthology.org/N13-1132.pdf) NAACL-HLT 2013.

[7] Wang et al. ["All that Agrees Is Not Gold: Evaluating Ground Truth Labels and Dialogue Content for Safety"](https://research.google/pubs/all-that-agrees-is-not-gold-evaluating-ground-truth-labels-and-dialogue-content-for-safety/) 2023.

[8] Zhang et al. ["A Taxonomy of Rater Disagreements: Surveying Challenges & Opportunities from the Perspective of Annotating Online Toxicity"](https://arxiv.org/abs/2311.04345) arXiv preprint arXiv:2311.04345 (2023).

[9] Davani et al. ["Dealing with disagreements: Looking beyond the majority vote in subjective annotations"](https://arxiv.org/abs/2110.05719) ACL 2022.

[10] Gordon et al. ["Jury Learning: Integrating Dissenting Voices into Machine Learning Models"](https://arxiv.org/abs/2202.02950) CHI 2022.

[11] Gordon et al. ["The Disagreement Deconvolution: Bringing Machine Learning Performance Metrics In Line With Reality"](https://dl.acm.org/doi/abs/10.1145/3411764.3445423) CHI 2021

[12] Daniel et al. 2018 ["Quality Control in Crowdsourcing: A Survey of Quality Attributes, Assessment Techniques, and Assurance Actions"](https://arxiv.org/abs/1801.02546) ACM Computing Surveys (CSUR), 51(1), 1-40 (2018).

[13] Koh & Liang. ["Understanding Black-box Predictions via Influence Functions"](https://arxiv.org/abs/1703.04730) ICML 2017.

[14] Grosse et al. ["Studying Large Language Model Generalization with Influence Functions"](https://arxiv.org/abs/2308.03296) arXiv preprint arXiv:2308.03296 (2023).

[15] Swayamdipta et al. ["Dataset Cartography: Mapping and Diagnosing Datasets with Training Dynamics"](https://arxiv.org/abs/2009.10795) EMNLP 2020.

[16] Toneva, et al. ["An Empirical Study of Example Forgetting during Deep Neural Network Learning"](https://arxiv.org/abs/1812.05159) ICLR 2019.

[17] Pleiss, et al. ["Identifying Mislabeled Data using the Area Under the Margin Ranking"](https://arxiv.org/abs/2001.10528) NeuriPS 2020.

[18] Chen et al. ["Understanding and utilizing deep neural networks trained with noisy labels"](https://arxiv.org/abs/1905.05040) ICML 2019.
