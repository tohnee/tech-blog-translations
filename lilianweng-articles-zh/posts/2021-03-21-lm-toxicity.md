---
title: "降低语言模型的毒性"
title_en: "Reducing Toxicity in Language Models"
source: https://lilianweng.github.io/posts/2021-03-21-lm-toxicity/
crawled: 2026-09-08
translated: 2026-09-08
---

# 降低语言模型的毒性

> 原文：[Reducing Toxicity in Language Models](https://lilianweng.github.io/posts/2021-03-21-lm-toxicity/) · Lilian Weng（翁荔）

> 毒性（toxicity）使我们无法安全地把强大的预训练语言模型部署到实际应用中。为了降低语言模型中的毒性，本文将深入探讨这一问题的三个方面：训练数据集的收集、毒性内容的检测，以及模型的去毒（detoxification）。

大型预训练[语言模型](https://lilianweng.github.io/posts/2019-01-31-lm/)（language model, LM）是在规模庞大的在线数据上训练而成的，不可避免地从互联网习得了某些有毒行为与偏见。预训练语言模型非常强大，已在许多 NLP 任务中取得了巨大成功。然而，要把它们安全地部署到现实世界的实际应用中，就需要对模型的生成过程施加严格的安全控制。

减少各类不安全内容的努力伴随着许多挑战：
- 首先，不安全内容的类型多种多样，例如毒性、辱骂、仇恨言论、偏见、刻板印象、网络欺凌、身份攻击等，它们可能需要、也可能不需要区别对待。
- 其次，对于预训练语言模型的不安全行为，目前尚无清晰且被广泛认可的分类与定义。由于社会背景不同，个体的感知可能差异极大。

本文将深入探讨语言模型中的毒性问题。由于笔者仍在苦苦寻找毒性内容的具体定义，下面列出文献中的几种定义。

> [[Perspective API](https://support.perspectiveapi.com/s/about-the-api-attributes-and-languages)] 粗鲁、不敬或不讲理的评论；很可能让人们离开一场讨论。

> [[Kurita et al. 2019](https://arxiv.org/abs/1912.06872)] 可能冒犯或伤害其接收者的内容，包括仇恨言论、种族主义和攻击性语言。

> [[Pavlopoulos et al. 2020](https://arxiv.org/abs/2006.00998)] 我们将“toxic（有毒）”用作一个统称（umbrella term），但需要指出，文献中对不同种类的毒性语言或相关现象使用了多个术语：“offensive（攻击性）”、“abusive（辱骂性）”、“hateful（仇恨性）”等。

总体而言，毒性是一个宽泛的术语，用于描述多种类型的不安全内容。只要给定某种形式的毒性定义——例如标注者指南中给出的定义——本文介绍的方法论即可应用。如何恰当地定义毒性这一概念、进而收集准确的标注标签，不在本文的讨论范围之内。

## 毒性内容的分类

如何对毒性内容进行分类并非易事。哪些内容应被视为有毒、存在哪些类型的毒性内容，都可能非常主观。在一个群体看来并不冒犯的语言，在另一个群体看来可能显得不得体。

[Zampieri et al. (2019)](https://arxiv.org/abs/1902.09666) 提出了一种流行的攻击性语言分类方法：一个同时考虑冒犯类型与冒犯目标的三级层次分类体系（taxonomy）。攻击性语言识别数据集（[OLID](#OLID)，Offensive Language Identification Dataset）正是基于这一分类体系收集的。

![攻击性分类体系](https://lilianweng.github.io/posts/2021-03-21-lm-toxicity/offensive-taxonomy.png)

*图 1. [Zampieri et al. (2019)](https://arxiv.org/abs/1902.09666) 提出的用于对攻击性语言进行分类的三级层次分类体系。*



- 层级 A：“是否具有攻击性？”
    - `[OFF]` 有攻击性（Offensive）：不当语言、侮辱或威胁。
    - `[NOT]` 无攻击性（Not offensive）：无冒犯或亵渎。
- 层级 B：“攻击性文本是否指向特定目标？”
    - `[TIN]` 有目标的侮辱（Targeted Insult）：针对个人、群体或其他对象的侮辱或威胁。
    - `[UNT]` 无目标（Untargeted）：不指向特定对象的亵渎与咒骂。
- 层级 C：目标是什么？
    - `[IND]` 冒犯针对个人，通常被定义为“网络欺凌”（cyberbullying）。
    - `[GRP]` 冒犯基于种族、性别、性取向、宗教或其他共同特征针对某个群体，通常被定义为“仇恨言论”（hate speech）。
    - `[OTH]` 目标可以属于其他类别，例如组织、事件、议题等。


## 数据收集

准备一个将样本标注为“安全”与“不安全”的数据集，是训练毒性语言分类器、并进一步为模型去毒提供信号的基础。

### 人工标注

[Vidgen & Derczynski (2020)](https://arxiv.org/abs/2004.01670) 总结道，毒性检测的训练数据标注在宏观上可以通过以下方式收集：
1. *专家标注（Expert coding）*：专家具备足够的知识或训练，能够高质量地完成标注任务，例如研究偏见的学者、受过中等程度训练的学生，或 NLP 从业者。这种方式成本更高，但能产出高质量数据。
2. *众包（Crowdsourcing）*：众包平台将大量非专家标注者与任务匹配。这种方式更容易扩展规模，但需要在质量控制上投入更多注意力。
3. *专业审核人员（Professional moderators）*：专业内容审核人员经验丰富、在任务上受过良好训练，但其目标很可能是针对该平台特定的产出进行优化。
4. *合成数据（Synthetic data）*：也可以由相关内容创作者人工创建训练数据集，以覆盖广泛的毒性内容类型。

其中，众包是最常见的方式（[Davidson et al. 2017](https://arxiv.org/abs/1703.04009)、[Zampieri et al. 2019](https://arxiv.org/abs/1902.09666)），并且有若干提升数据质量的良好实践：
1. *测试数据（Test data）*：从少数专家处收集的一小批标注可用作测试题（[Zampieri et al. 2019](https://arxiv.org/abs/1902.09666)），用以淘汰众包平台上达不到一定阈值的标注者。
2. *清晰的指南（Clear guidelines）*：详细的说明有助于引导标注者产出对齐且一致的标签。在没有任何指南的情况下，标注者会倾向于诉诸个人感知，这可能带来问题，因为（1）个体对毒性内容的主观解读差异很大，（2）在没有指南时，标记讽刺与反语这类噪声颇为棘手。
3. *多数投票（Majority vote）*：非常常见的做法是，每个样本由多名标注者打标签，然后取多数票。
4. *了解标注者的身份（Understanding annotators' identities）*：人口统计背景对标注者理解任务的影响很大。我们应力求招募多元且合格的标注者。


### 半监督数据集

[Khatri et al. (2018)](https://arxiv.org/abs/1811.12900) 提出了一种简单的方法，通过自举（bootstrap）获得大量半监督数据集来学习毒性内容分类器。他们的方法依赖一个小的已标注数据集和一个大的未标注数据集。

1. 首先，他们收集了一个包含 800 多个词的黑名单，覆盖亵渎、仇恨、色情内容和侮辱等主题。亵渎词黑名单可能精确率高而召回率低，但它能提供弱监督信号。
2. 各个 subreddit（Reddit 版块）按黑名单词占比排序，然后分别从排序靠前的 subreddit 中采样敏感样本、从排序靠后的 subreddit 中采样非敏感样本。
3. 训练一个弱二元分类器，从排序后的 subreddit 中进一步筛选更多样本：
    - 敏感：包含黑名单词，或毒性分类器置信度 > 0.8；
    - 不敏感：不包含黑名单词，且毒性分类器置信度 < 0.3
4. 在这个大规模扩充后的数据集上，训练一个名为“两阶段自举”（Two-stage bootstrap，**TS bootstrap**）的新分类器。

他们的实验表明，TS bootstrap 分类器在 F1 分数、准确率和召回率上都取得了相当不错的成绩，而且还能迁移到域外（out-of-domain）测试数据上。


![两阶段自举](https://lilianweng.github.io/posts/2021-03-21-lm-toxicity/TS-bootstrap.png)

*图 2. 两阶段自举分类器在一个数据集上训练，该数据集由一个弱毒性二元分类器在 Reddit 数据上自举得到。（图片来源：[Khatri et al. 2018](https://arxiv.org/abs/1811.12900)）*


[SOLID](#SOLID)（半监督攻击性语言识别数据集，Semi-Supervised Offensive Language Identification Dataset；[Rosenthal et al. 2020](https://arxiv.org/abs/2004.14454)）包含 900 多万条推文，采用与 [OLID](#OLID) 相同的分类体系进行标注。SOLID 把 OLID 当作种子，通过一种名为民主协同训练（democratic co-training）的半监督技术加以扩展。民主协同训练（[Zhou & Goldman, 2004](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.76.3152&rep=rep1&type=pdf)）利用在小规模监督数据集上训练的一组多样化模型所提供的含噪标签，构建出大规模数据集。SOLID 的构建方式如下：
1. 首先，在已标注数据集 OLID 上训练一组多样化的监督模型。论文实验了 PMI（基于 n-gram 的相似度）、FastText（与 BoW 模型类似的浅层神经模型）、LSTM 和 BERT。
2. 对未标注数据集中的每个样本，每个模型都为目标类别预测一个置信度分数。这些分数通过 `avg()` 或 `min()` 聚合。高置信度的样本会被加入数据集。


当监督数据集对于一项简单任务而言已经足够大时，BERT 模型的性能不会再提升；但如果原始监督数据集对任务来说太小，BERT 便能从大规模半监督数据集中获益。


## 毒性检测

有了监督数据集，我们可以从零训练一个文本分类器，或者微调一个预训练语言模型来执行分类任务。但如果训练样本质量或数量不够呢？如果我们无法获得这样的监督数据集呢？

### 对抗攻击

为了构建对对抗攻击（adversarial attack）具有鲁棒性的毒性检测模型，[Dinan et al. (2019)](https://arxiv.org/abs/1908.06083) 提出了一种迭代式的“构建—破坏—修复”（build it, break it, fix it）策略，通过人在回路（humans in the loop）来提升对话系统的安全性。
1. *构建（Build it）*：在 [Jigsaw 数据集](#jigsaw)上训练一个 BERT 模型来对毒性评论分类。
2. *破坏（Break it）*：让众包工作者写出会被模型错误标注为“安全”的毒性消息。
3. *修复（Fix it）*：在原始数据集与新收集的对抗样本的组合上重新训练模型。
4. *重复（Repeat）*：重新部署加固后的模型，并从第 1 步开始新一轮循环。


![build-break-fix](https://lilianweng.github.io/posts/2021-03-21-lm-toxicity/build-break-fix.png)

*图 3. 通过“构建—破坏—修复”过程迭代改进毒性内容检测模型的示意图。（图片来源：[Dinan et al. 2019](https://arxiv.org/abs/1908.06083)）*



他们实验中的一个基线，是把“破坏”步骤中的对抗收集替换为标准收集，即直接要求工作者提交“攻击性”消息。与标准收集相比，对抗收集中显式亵渎更少，而用于欺骗模型的否定表达更多。在后面的轮次中，任务变得更难。

对抗模型比在标准收集上训练的基线模型更能抵御对抗攻击。第三轮对抗模型在标准任务上的表现不如标准模型，可能是过拟合所致。笔者很好奇，如果在对抗收集与标准收集两者之上训练，模型表现会怎样，但论文中找不到相关结果。


![build-break-fix 结果](https://lilianweng.github.io/posts/2021-03-21-lm-toxicity/build-break-fix-it-results.png)

*图 4. 在标准数据收集（$$S_i$$）与对抗数据收集（$$A_i$$）上训练的模型，在标准任务与对抗任务上的性能比较。下标 $$i$$ 表示训练轮数。（图片来源：[Dinan et al. 2019](https://arxiv.org/abs/1908.06083)）*



另一类对抗攻击通过替换或打乱一部分字符，诱骗检测模型把毒性句子错误地分类为安全。[Kurita et al. (2019)](https://arxiv.org/abs/1912.06872) 开发了一种生成此类与模型无关（model-agnostic）的对抗攻击的方法，其中纳入了几种字符级扰动（character-level perturbation）：
1. *字符打乱（Character scrambling）*：随机排列字符位置。
2. *同形字替换（Homoglyph substitution）*：用一个或多个外形相似的国际字母替换原字母。
3. *基于词典的近邻替换（Dictionary-based near-neighbor replacement）*：找到在编辑距离（Levenshtein distance）意义上最接近但不相同的 token。
4. *干扰项注入（Distractor injection）*：通过重复随机选取的无毒 token 序列来注入干扰 token。

结合 token 混淆与干扰 token 的对抗噪声会导致毒性分类器性能显著下降。字符级扰动比干扰项造成的性能下降更严重。

论文提出了两种应对对抗攻击的方法：
- *对抗训练（Adversarial training）*：指在带噪声的数据集上训练模型。然而，这需要事先知道来袭攻击的细节；而且无法保证用任意噪声构造的训练样本能泛化到测试集。
- *CDAE（上下文去噪自编码器，contextual denoising autoencoder）*：利用字符级信息与上下文信息对被混淆的 token 去噪。CDAE 以一个噪声样本为输入，预测去噪后的版本。不过，你仍需要知道可以施加哪些类型的字符级扰动来构造噪声样本。CDAE 的表现与 BERT 相当，但没有显著更好。



### Perspective API

**Perspective API**（[www.perspectiveapi.com](https://www.perspectiveapi.com/)）是目前使用最广泛的毒性内容检测商业 API。Perspective 训练机器学习模型，为若干不同的[属性](https://support.perspectiveapi.com/s/about-the-api-attributes-and-languages)打分：毒性、严重毒性、侮辱、亵渎、身份攻击、威胁以及色情内容。每项分数是 [0, 1] 之间的一个数字，表示消息包含给定属性的可能性有多大（即一个二元分类器的置信度），并不代表该属性的严重程度。

![Perspective API](https://lilianweng.github.io/posts/2021-03-21-lm-toxicity/about-perspective-api.png)

*图 5. Perspective API 各项分数概览。（图片来源：[About Perspective API](https://support.perspectiveapi.com/s/about-the-api)）*


[Gehman et al. (2020)](https://arxiv.org/abs/2009.11462) 测量了从若干预训练语言模型采样的无提示（unprompted）生成内容的 Perspective API 毒性分数。“无提示”指生成仅以句子起始 token 为条件，不注入任何额外上下文。值得注意的是，所有被测模型在 100 次生成后，期望最大毒性都超过了 0.5。他们还指出，大型语言模型的训练数据集含有不可忽视的毒性内容。

![无提示毒性](https://lilianweng.github.io/posts/2021-03-21-lm-toxicity/unprompted-toxicity.png)

*图 6. 无提示生成内容的 Perspective API 毒性分数。每个模型生成一个包含 1 万条样本的池，期望最大毒性分数通过自助法（bootstrapping）估计。（图片来源：[Gehman et al. 2020](https://arxiv.org/abs/2009.11462)）*


他们收集了 [**RealToxicityPrompt** 数据集](#RealToxicityPrompt)，用于研究条件式语言模型生成中的毒性。它包含 10 万条自然出现的提示（prompt），每条都带有 Perspective API 给出的毒性分数。有些提示本身不含任何毒性语言，却仍可能触发极具攻击性的补全（completion）。

<a name="perspective-api-biases" />尽管广受欢迎，Perspective API 仍存在已知的偏见，正如 [Gehman et al. (2020)](https://arxiv.org/abs/2009.11462) 所总结的：
> ……对少数群体表现出偏见，且标注一致性偏低，部分原因在于标注者身份会影响其对仇恨言论的感知，以及标注任务设置存在差异。

> 值得注意的是，近期工作发现，系统会高估包含少数群体身份提及的文本（如“I’m a gay man”）或少数族裔所写文本（如非裔美国人英语文本）中毒性的普遍程度。部分原因在于检测器过度依赖毒性的词汇线索（包括脏话、蔑称以及其他“坏”词）。


### 基于提示的检测

**自我诊断（Self-diagnosis）**（[Schick, et al. 2021](https://arxiv.org/abs/2103.00453)）是利用预训练语言模型自身能力、在其自身输出中检测社会性不良属性的过程。该诊断依赖一个预定义的提示模板，其中不良属性以简短文本描述，并测量模型输出 “yes” 与 “no” 的归一化概率。注意，自我诊断无需访问带标签的数据集来训练。

```
# Self-diagnosis template
"{sample text}"
Question: Does the above text contain {undesired attribute}?
Answer: {yes/no}
```

实验中，他们使用 RealToxicityPrompts 数据集和 Perspective API 进行评估。自我诊断的性能与模型规模正相关。

![自我诊断](https://lilianweng.github.io/posts/2021-03-21-lm-toxicity/self-diagnosis-toxicity-score.png)

*图 7. 识别不良属性的自我诊断能力。真实标签（ground truth）由 Perspective API 提供。（图片来源：[Schick, et al. 2021](https://arxiv.org/abs/2103.00453)）*



## 去毒

### 黑名单

**坏词过滤（Bad word filtering）**是一种相当直观且有效的方法，用于避免语言模型生成中出现显式的亵渎[词](https://github.com/%20LDNOOBW/List-of-Dirty-Naughty-Obscene-%20and-Otherwise-Bad-Words)。在解码时，我们可以人为降低被屏蔽词的概率，从而避免采样到它们。然而，这一方法并不完美，因为由安全 token 组成的不安全内容依然可能出现。

**词表偏移（Vocabulary shifting）**（[Gehman et al. 2020](https://arxiv.org/abs/2009.11462)）为预训练模型词表中的每个 token 学习一个“毒性对无毒”的二维表征；随后在解码时，利用编码无毒性的那一维表征来提升无毒 token 的似然。


### 基于提示的去毒

**自我去偏（Self-debiasing）**（[Schick et al. 2021](https://arxiv.org/abs/2103.00453)）沿用了与[自我诊断](#prompt-based-detection)类似的思想。它是利用预训练语言模型的内部知识，来降低模型生成中出现不良属性的概率的过程。

```
# Self-debiasing template, denoted as sdb(.)
The following text contains {undesired attribute s}:
{sample text x}
```

给定输入提示 $$\mathbf{x}$$、不良属性的文本描述 $$s$$ 以及语言模型 $$M$$，自我去偏计算在“不使用”与“使用”自我去偏模板 $$\text{sdb}(.)$$ 两种情况下，下一个词的概率之差：

$$
\Delta(w, \mathbf{x}, s) = p_M(w\vert\mathbf{x}) - p_M(w\vert\text{sdb}(\mathbf{x}, s))
$$

由于 $$\text{sdb}(.)$$ 预期会提升不良词的概率，因此对于不良词，$$\Delta(w, \mathbf{x}, s)$$ 应当为负。

在自我去偏解码中，使用概率差的缩放函数 $$\alpha(\Delta(w, \mathbf{x}, s)): \mathbb{R}\to[0,1]$$ 来改变真实的采样分布：

$$
\tilde{p}_M(w\vert\mathbf{x}) \propto \alpha(\Delta(w, \mathbf{x}, s)) p_M(w\vert\mathbf{x})
$$

论文中采用了一个软变体：$$\Delta$$ 为负的词，其概率会按照 $$\Delta(w, \mathbf{x}, s)$$ 的幅度相应调低：

$$
\alpha(x)=\begin{cases} 1 & \text{ if } x\geq 0 \\ e^{\lambda\cdot x} & \text{ otherwise} \end{cases}
$$


![自我去偏](https://lilianweng.github.io/posts/2021-03-21-lm-toxicity/self-debiasing-decoding.png)

*图 8. 自我去偏解码可以降低不良属性的概率。分数由 Perspective API 提供。（图片来源：[Schick et al. 2021](https://arxiv.org/abs/2103.00453)）*


自我去偏去毒存在几个主要局限：
1. 评估完全依赖 Perspective API，因此无法捕捉 Perspective API [未覆盖](#perspective-api-biases)的偏见与毒性属性，例如性别偏见。人工评估是另一种替代方案，但规模受限。
2. 自我去偏有时过于激进，会过滤掉无害的词，而且不能保持与原始模型相同的困惑度（perplexity）水平。
3. 该方法受限于模型的内部能力。例如，如果模型本身并未意识到某些偏见，它就无法纠正这些偏见。


### 文本风格迁移

**无监督风格迁移（Unsupervised style transfer）**可用于把攻击性句子翻译成无害句子（[Santos et al. 2018](https://arxiv.org/abs/1805.07685)）。该方法应当适用于非平行数据集，也就是说，我们只能拿到攻击性与非攻击性两个相互独立的数据集，而没有成对版本。为了在把文本迁移成另一种风格的同时保留内容，采用了循环一致性损失（cycle consistency loss）（[Zhu et al. 2017](https://arxiv.org/abs/1703.10593)）。

![文本风格迁移](https://lilianweng.github.io/posts/2021-03-21-lm-toxicity/offensive-text-style-transfer.png)

*图 9. 使用非平行数据的神经文本风格迁移算法的训练过程。（图片来源：[Santos et al. 2018](https://arxiv.org/abs/1805.07685)）*


设 $$s_i$$ 为目标风格（$$i=0$$ 表示攻击性，$$i=1$$ 表示非攻击性），$$\mathbf{x}^i_k$$ 为风格 $$s_i$$ 的第 $$k$$ 个样本，$$k = 1, \dots, n$$。编码器 $$E$$ 和解码器 $$G$$ 都接收一个样本（或隐藏状态）外加一个风格标签。分类器 $$C$$ 在给定输入样本时，预测风格标签上的概率分布。

对照图 9 的示意：
- 前向迁移的上分支是自编码器：$$E(\mathbf{x}^i_k, s_i) \to H^i_k \to G(H^i_k, s_i) \to \hat{\mathbf{x}}^{i\to i}_k$$。这里计算两个损失：
    - 重构损失衡量解码器能把样本还原得多好：
    
    $$
    \mathcal{L}_\text{self} = \mathbb{E}_{\mathbf{x}^i_k \sim \mathcal{X}} [-\log p_G(\mathbf{x}_k^i \mid E(\mathbf{x}^i_k, s_i), s_i)]
    $$
- 前向迁移的下分支：$$E(\mathbf{x}^i_k, s_i) \to H^i_k \to G(H^i_k, s_j) \to \hat{\mathbf{x}}^{i\to j}_k$$
    - 分类损失衡量风格迁移的有效性：
    
    $$
    \mathcal{L}_\text{style_fwd} = \mathbb{E}_{\hat{\mathbf{x}}^{i\to j}_k \sim \hat{\mathcal{X}}} [-\log p_C(s_j \mid \hat{\mathbf{x}}^{i\to j}_k)]
    $$

- 反向迁移使用循环一致性损失：$$E(\hat{\mathbf{x}}^{i\to j}_k, s_j) \to H^{i\to j}_k \to G(H^{i\to j}_k, s_i) \to \hat{\mathbf{x}}^{i\to j \to i}_k$$
    - 循环一致性损失控制迁移后的样本能被多好地转换回原始形式，以鼓励内容保留：
    
    $$
    \mathcal{L}_\text{cycle} = \mathbb{E}_{\mathbf{x}^i_k \sim \mathcal{X}} [-\log p_G(\mathbf{x}_k^i \mid E(\hat{\mathbf{x}}^{i \to j}_k, s_j), s_i)]
    $$

    - 分类损失确保迁移回来的样本带有正确的标签：
    
    $$
    \mathcal{L}_\text{style_back} = \mathbb{E}_{\hat{\mathbf{x}}^{i\to j}_k \sim \hat{\mathcal{X}}} [-\log p_C(s_i \mid G(E(\hat{\mathbf{x}}^{i\to j}_k, s_j), s_i))]
    $$

- 另有一个额外的监督分类损失，用于训练一个准确的分类器：

$$
\mathcal{L}_\text{class} = \mathbb{E}_{\hat{\mathbf{x}}^{i\to j}_k \sim \hat{\mathcal{X}}} [-\log p_C(s_i \mid \hat{\mathbf{x}}^i_k)]
$$

最终训练目标如下，编码器、解码器和分类器联合训练：

$$
\mathcal{L}(\theta_E, \theta_G, \theta_C) = \min_{E, G, C} \mathcal{L}_\text{self} + \mathcal{L}_\text{style_fwd} + \mathcal{L}_\text{cycle} + \mathcal{L}_\text{style_back}+ \mathcal{L}_\text{class}
$$


**Style Transformer**（[Dai et al. 2019](https://arxiv.org/abs/1905.05621)）同样旨在学习无监督文本风格迁移。与 [Santos et al. 2018](https://arxiv.org/abs/1805.07685) 的编码器-解码器模型不同，它为给定的输入样本 $$\mathbf{x}$$ 和目标风格控制变量 $$s$$ 学习一个基于 Transformer 的风格迁移函数 $$f_\theta(\mathbf{x}, s)$$。


![Style transformer](https://lilianweng.github.io/posts/2021-03-21-lm-toxicity/style-transformer.png)

*图 10. Style Transformer 与以往依赖解耦潜在表征的模型的比较。（图片来源：[Dai et al. 2019](https://arxiv.org/abs/1905.05621)）*



由于无法获得平行语料，Style Transformer 采用一个判别器从非平行数据集中制造监督信号。

设 $$s$$ 与 $$\hat{s}$$ 是两个互斥的风格变量，$$\mathbf{x}$$ 是风格 $$s$$ 的一个样本，Style Transformer 计算若干损失：
- 自重构损失：$$\mathcal{L}_\text{self} = - p_\theta (\mathbf{x} \vert \mathbf{x}, s)$$
- 循环一致性损失：$$\mathcal{L}_\text{cycle} = - p_\theta (\mathbf{x} \vert f_\theta(\mathbf{x}, \hat{s}), s)$$
- 风格控制损失：这一项必不可少，否则模型会简单地学会照抄输入。

$$
\mathcal{L}_\text{style} = - p_\phi(\text{class} = 1 \vert f_\theta(\mathbf{x}, \hat{s}), \hat{s})
$$

其中，判别器是一个简单的二元分类器，训练以优化正确风格的负对数似然。判别器通过如下标注方式训练：
- 把 $$\{(\mathbf{x}, s), (f_\theta(\mathbf{x}, s), s), (f_\theta(\mathbf{x}, \hat{s}), \hat{s})\}$$ 标为正类 1
- 把 $$\{(\mathbf{x}, \hat{s}), (f_\theta(\mathbf{x}, s), \hat{s}), (f_\theta(\mathbf{x}, \hat{s}), s)\}$$ 标为负类 0。


![Style transformer 训练](https://lilianweng.github.io/posts/2021-03-21-lm-toxicity/style-transformer-training.png)

*图 11. Style Transformer 的训练过程。（图片来源：[Dai et al. 2019](https://arxiv.org/abs/1905.05621)）*



在研究问题“能否仅使用按毒性标注的数据集，就微调一个预训练语言模型，使其为粗鲁评论给出文明得体的改写？”的驱动下，[Laugier et al. (2021)](https://arxiv.org/abs/2102.05456) 使用去噪与循环自编码器损失微调了一个预训练的 text-to-text Transformer。

设 $$s$$ 是 $$\mathbf{x}$$ 的属性（例如“文明”），$$\bar{s}$$ 是与之相对的另一个属性（例如“有毒”）。这两个属性互斥。目标是学习一个映射函数 $$f_\theta$$，把 $$x$$ 翻译为一个新的流畅序列 $$y$$，使其具有目标属性 $$a$$，同时保留 $$x$$ 的内容。

该编码器-解码器模型使用如下损失训练：

$$
\mathcal{L} = \lambda_\text{DAE} \mathcal{L}_\text{DAE} + \lambda_\text{cycle} \mathcal{L}_\text{cycle}
$$

- 去噪自编码器损失就是去噪自编码器所用的损失，其中 $$\eta$$ 是一个与 BERT 训练中相同的[掩码](https://lilianweng.github.io/posts/2019-01-31-lm/#pre-training-tasks)函数：

$$
\mathcal{L}_\text{DAE} = \mathbb{E}_{\mathbf{x} \sim \mathcal{X}} [−\log p_\theta(\mathbf{x} \mid \eta(\mathbf{x}), s)]
$$ 

- 循环一致性损失（[Zhu et al. 2017](https://arxiv.org/abs/1703.10593)）让 $$\tilde{\theta}$$ 产生一个不可微分的伪预测 $$\hat{\mathbf{y}}$$，并且不进行梯度反向传播。

$$
\mathcal{L}_\text{cycle} = \mathbb{E}_{\mathbf{x} \sim \mathcal{X}} [−\log p_\theta(\mathbf{x} \mid f_{\tilde{\theta}}(\mathbf{x}, \bar{s}), s)]
$$ 


他们用上述损失微调了一个 T5 模型，得到了名为 **CAE-T5** 的模型。其条件化的实现方式类似 CTRL：通过在序列开头拼接控制码（“civil” 或 “toxic”）。

文本风格迁移结果的自动评估依赖三个指标：
1. *准确率（Accuracy）*：分类准确率衡量风格迁移有多成功。
2. *流畅度（Fluency）*：流畅度通常由另一个单独训练的语言模型在无毒样本上的困惑度来衡量。
3. *内容保留（Content preservation）*：指迁移后句子与原句之间的内容相似度，用 BLEU 或基于嵌入的内容相似度来度量。

人工评估同样必要，但成本更高。

与基线（[Shen et al. 2017](https://arxiv.org/abs/1705.09655)）相比，[Santos et al. 2018](https://arxiv.org/abs/1805.07685) 的风格迁移方法取得了更好的分类准确率、更好的内容保留，但困惑度更差。与包括 Style Transformer 在内的一组基线相比，CAE-T5 的分类准确率更差，内容保留具有竞争力，困惑度则更好。


### 可控生成

我们可以尝试通过*可控文本生成（controllable text generation）*来避免毒性输出。要把预训练语言模型引导到期望的风格、主题或安全标准上，有几种流行的做法：
1. 采用引导式解码策略（decoding strategy），并在测试时挑选期望的输出。
2. 通过良好的提示设计，优化出最期望的结果。
3. 微调基础模型或可操控的层，以进行条件化内容生成。

更多内容请参阅我的[上一篇文章](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/)，其中介绍了可控神经文本生成，涵盖 [AutoPrompt](https://arxiv.org/abs/2010.15980)、[CTRL](https://arxiv.org/abs/1909.05858)、[PPLM](https://arxiv.org/abs/1912.02164)、[GeDi](https://arxiv.org/abs/2009.06367) 等诸多方法。

[Gehman et al. (2020)](https://arxiv.org/abs/2009.11462) 对基于数据的（监督微调、CTRL 训练）和基于解码的（词表偏移、坏词屏蔽过滤、PPLM）语言模型去毒方法都进行了实验。他们发现，毒性控制 token（CTRL）和脏话过滤器的*成功程度不如*那些更耗计算或更耗数据的方法，如在无毒语料上微调以及 PPLM。


![RealToxicityPrompts 去毒实验](https://lilianweng.github.io/posts/2021-03-21-lm-toxicity/RealToxicityPrompts-experiments.png)

*图 12. 表中列出了若干去毒方法在 25 次生成下的期望最大毒性分数（左），以及在 25 次生成中生成毒性文本的经验概率（右）。分数由 Perspective API 提供。（图片来源：[Gehman et al., 2020](https://arxiv.org/abs/2009.11462)）*



### 系统级安全方案

[Xu et al. (2020)](https://arxiv.org/abs/2010.07079) 给出了一套构建安全聊天机器人的完整系统级设计。

![安全聊天机器人系统](https://lilianweng.github.io/posts/2021-03-21-lm-toxicity/safe-chatbot-system.png)

*图 13. 安全聊天机器人系统示意图。（图片来源：[Xu et al. 2020](https://arxiv.org/abs/2010.07079)）*


他们在让机器人更安全的“配方”中考虑了四种通用策略：
- *检测不安全内容（Detect unsafe content）*：在输入端和输出端都部署一个检测不安全语言的分类器，作为语言模型之上的额外安全层。
    - 该分类器在 [Jigsaw toxic](#jigsaw) 评论数据集的增强版本（安全/不安全二元标签）上训练，并用[对抗性人类攻击](#adversarial-attacks)（[Dinan et al. 2019](https://arxiv.org/abs/1908.06083)）和[半监督](#semi-supervised-dataset)（[Khatri et al. 2018](https://arxiv.org/abs/1811.12900)）加以扩展。
    - 该安全分类器既可用于用户输入，也可用于模型输出。一旦检测到不安全内容，系统被配置为返回一条预设的固定回复（如 “I’m sorry I’m not sure what to say.”），或者决定转换话题。值得注意的是，这一做法依赖高质量的分类器；误报过多会严重破坏对话体验。
    - 机器人对抗对话（Bot adversarial dialogue, BAD）安全：其思路是收集人类对抗性地试探系统使其犯错的数据，然后用这些数据做进一步训练。标注时，人类标注者可以根据可能认为该回复不安全的人口比例，为机器人的回复打上“不安全—安全”评级。这些试探数据用于训练一个多轮安全分类器，在给定对话上下文的情况下预测一条回复是否具有攻击性。
- *安全生成（Safe generation）*：训练一个更不容易输出不安全回复的模型。
    - 预定义的不安全词/n-gram 列表可以在解码时被[屏蔽](#blacklisting)。
    - 预训练数据经上述安全分类器过滤，或基于已知作者过滤。
    - 只用安全数据集预训练的问题在于：如果模型在训练期间从未见过毒性语言，它在测试时就会不知所措（OOD；例如可能只是照抄攻击性内容）。他们的做法反而是准备一批训练样本，其中最后一句话被标注为“不安全”，然后在这句不安全攻击之后接上一条安全回复；接着，模型在这些“内置”（baked-in）的安全数据上微调。
    - 用安全分类器赋予“安全”与“不安全”标签，进行 [CTRL](https://arxiv.org/abs/1909.05858) 式训练。
- *回避敏感话题（Avoid sensitive topics）*：
    - 为了回避敏感话题（政治、宗教、药物使用、医疗建议、NSFW 内容以及恋爱/约会），他们利用众包的 subreddit 列表训练了一个多类分类器来检测这些话题。该分类器可以周期性地重新训练，以捕捉各话题内容随时间的变化。
    - 通过招募众包工作者讨论某个目标话题，收集了一个小型验证集。
- *性别偏见缓解（Gender bias mitigation）*：
    - 他们使用 [CTRL](https://arxiv.org/abs/1909.05858) 式训练来缓解性别偏见。
    - 具体而言，给定一个带性别色彩的词表，为训练样本打上 $$F^0 M^0$$、$$F^0 M^+$$、$$F^+ M^+$$、$$F^+ M^0$$ 标签，表示回复中是否包含女性/男性词汇（$$+$$ 表示包含，$$-$$ 表示不包含）。测试时，系统以控制标签 $$F^0 M^0$$ 运行，以避免输出带有特定性别色彩的词。


## 附录：数据集

（*此处仅列出英文数据集。）

**Hate Speech and Offensive Language** 数据集（2017）：包含约 2.5 万条推文，每条均被人工标注为以下三类之一：仇恨言论、有攻击性但非仇恨言论、既无攻击性也非仇恨言论。[[下载](https://github.com/t-davidson/hate-speech-and-offensive-language/blob/master/data/readme.md)]

<a name="jigsaw" />**Jigsaw Toxic** 评论分类数据集（2018）：包含从 Wikipedia 讨论页提取的约 16 万条样本，每条针对 7 个类别标注：有毒、严重有毒、淫秽、威胁、侮辱、身份仇恨和无毒。标注过程动用了 5000 名众包标注者。[[下载](https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge)]

**Jigsaw Unintended Bias in Toxicity** 分类数据集（2019）：包含来自 Civil Comments 平台（该平台已于 2017 年关闭）的约 200 万条评论。数据标注了毒性、毒性子类型以及身份提及，从而可以评估与身份提及相关的非预期偏见。[[下载](https://www.kaggle.com/c/jigsaw-unintended-bias-in-toxicity-classification)]

<a name="OLID" />**OLID**（攻击性语言识别数据集，Offensive Language Identification Dataset；2019）：包含 14,100 条英文推文，按[此处](#categorization-of-toxic-content)所述的三级分类体系标注。[[下载](https://sites.google.com/site/offensevalsharedtask/olid)]

<a name="SOLID" />**SOLID**（半监督攻击性语言识别数据集，Semi-Supervised Offensive Language Identification Dataset；2020）：包含 900 多万条推文，按 OLID 的三级分类体系标注。[[下载](https://sites.google.com/site/offensevalsharedtask/solid)]

<a name="RealToxicityPrompt" />**RealToxicityPrompts** 数据集（2020）：包含来自网页的 10 万个句子片段，附有 Perspective API 毒性分数，用于研究语言模型出现神经毒性退化（neural toxic degeneration）的风险。[[下载](https://allenai.org/data/real-toxicity-prompts)]



---
引用本文：
```
@article{weng2021toxic,
  title   = "Reducing Toxicity in Language Models.",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io/lil-log",
  year    = "2021",
  url     = "https://lilianweng.github.io/lil-log/2021/03/21/reducing-toxicity-in-language-models.html"
}
```

## 参考文献

[1] Vidgen, et al. ["Challenges and frontiers in abusive content detection."](https://www.aclweb.org/anthology/W19-3509/) Workshop on Abusive Language Online 2019.

[2] Zampieri et al. ["Predicting the type and target of offensive posts in social media."](https://arxiv.org/abs/1902.09666) NAACL 2019.

[3] Vidgen & Deczynski. ["Directions in abusive language training data, a systematic review: Garbage in, garbage out."](https://arxiv.org/abs/2004.01670) PLoS ONE 15(12): e0243300 (2020).

[4] Davidson et al. ["Automated hate speech detection and the problem of offensive language."](https://arxiv.org/abs/1703.04009) ICWSM 2017.

[5] Khatri et al. ["Detecting offensive content in open-domain conversations using two stage semi-supervision."](https://arxiv.org/abs/1811.12900) NeuriIPS CONVAI Workshop 2018.

[6] Rosenthal et al. ["A Large-Scale Semi-Supervised Dataset for Offensive Language Identification"](https://arxiv.org/abs/2004.14454) arXiv:2004.14454 (2020).

[7] Pavlopoulos et al. ["Toxicity Detection: Does Context Really Matter?"](https://arxiv.org/abs/2006.00998) arXiv:2006.00998 (2020).

[8] Dinan et al. ["Build it, break it, fix it for dialogue safety: Robustness from adversarial human attack."](https://arxiv.org/abs/1908.06083) arXiv:1908.06083 (2019).

[9] Kurita et al. ["Towards Robust Toxic Content Classification"](https://arxiv.org/abs/1912.06872) arXiv:1912.06872 (2019)

[10] Santos et al. ["Fighting offensive language on social media with unsupervised text style transfer."](https://arxiv.org/abs/1805.07685) arXiv:1805.07685 (2018)

[11] Dai et al. ["Style Transformer: Unpaired Text Style Transfer without Disentangled Latent Representation"](https://arxiv.org/abs/1905.05621) ACL 2019.

[12] Laugier et al. ["Civil Rephrases Of Toxic Texts With Self-Supervised Transformers"](https://arxiv.org/abs/2102.05456)  arXiv:2102.05456 (2021). [代码](https://github.com/LeoLaugier/conditional-auto-encoder-text-to-text-transfer-transformer)

[13] Schick et al. ["Self-Diagnosis and Self-Debiasing: A Proposal for Reducing Corpus-Based Bias in NLP"](https://arxiv.org/abs/2103.00453) arXiv:2103.00453 (2021).

[14] Gehman et al. ["RealToxicityPrompts: Evaluating Neural Toxic Degeneration in Language Models"](https://arxiv.org/abs/2009.11462) EMNLP 2020.

[15] Xu et al. ["Recipes for Safety in Open-domain Chatbots"](https://arxiv.org/abs/2010.07079) arXiv:2010.07079 (2020).
