---
title: "提示工程"
title_en: "Prompt Engineering"
source: https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/
crawled: 2026-09-08
translated: 2026-09-08
---

**提示工程（Prompt Engineering）**，也称**上下文提示（In-Context Prompting）**，指如何与 LLM 沟通以引导其行为获得期望结果的方法——*无须*更新模型权重。它是一门经验科学，提示工程方法的效果因模型而异，因此需要大量实验与启发式。

> 原文：[Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) · Lilian Weng（翁荔）

本文只聚焦自回归语言模型的提示工程，不涉及完形填空测试、图像生成或多模态模型。其核心，提示工程的目标是对齐与模型可操控性。请看我关于可控文本生成的[前文](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/)。

[我的个人辣评] 在我看来，有些提示工程论文不值 8 页篇幅，因为那些技巧一两句话就能讲清，其余全是基准测试。一个易用且共享的基准基础设施对社区更有益。迭代式提示或外部工具使用的搭建并不平凡，让整个研究社区采纳它同样不简单。

# 基础提示

零样本与少样本学习是两种最基础的提示模型方式，由众多 LLM 论文开创，常用于 LLM 性能基准测试。

## 零样本

**零样本学习（Zero-shot learning）**是简单地把任务文本喂给模型并要求结果。

（所有情感分析示例均来自 SST-2）

```
Text: i'll bet the video game is a lot more fun than the film.
Sentiment:
```

## 少样本

**少样本学习（Few-shot learning）**在目标任务上呈现一组高质量示范，每个由输入与期望输出组成。由于模型先看到好例子，它能更好理解人类意图与"想要什么样的答案"的标准。因此，少样本学习常比零样本性能更好。但代价是消耗更多 token，且输入输出文本较长时可能触及上下文长度限制。

```
Text: (lawrence bounces) all over the stage, dancing, running, sweating, mopping his face and generally displaying the wacky talent that brought him fame in the first place.
Sentiment: positive

Text: despite all evidence to the contrary, this clunker has somehow managed to pose as an actual feature movie, the kind that charges full admission and gets hyped on tv and purports to amuse small children and ostensible adults.
Sentiment: negative

Text: for the first time in years, de niro digs deep emotionally, perhaps because he's been stirred by the powerful work of his co-stars.
Sentiment: positive

Text: i'll bet the video game is a lot more fun than the film.
Sentiment:
```

许多研究考察了如何构造上下文示例以最大化性能，并观察到**提示格式、训练示例的选择及示例顺序可导致截然不同的性能**——从接近随机猜测到接近 SoTA。

[Zhao et al. (2021)](https://arxiv.org/abs/2102.09690) 研究了少样本分类的情形，提出 LLM（实验用 GPT-3）的几种偏差导致如此高的方差：(1) 若示例间标签分布不平衡，存在*多数标签偏差（Majority label bias）*；(2) *近因偏差（Recency bias）*指模型可能重复末尾标签的倾向；(3) *常见 token 偏差（Common token bias）*表明 LLM 倾向更常产生常见 token 而非罕见 token。为克服这类偏差，他们提出一种方法：当输入字符串为 `N/A` 时，把模型输出的标签概率校准为均匀。

### 示例选择技巧

- 用嵌入空间中的 $k$-NN 聚类选择与测试示例语义相似的示例（[Liu et al., 2021](https://arxiv.org/abs/2101.06804)）
- 为选出多样且有代表性的示例集，[Su et al. (2022)](https://arxiv.org/abs/2209.01975) 提出基于图的方法：(1) 首先基于样本间嵌入（如 [SBERT](https://arxiv.org/abs/1908.10084) 或[其他](https://arxiv.org/abs/2201.10005)[嵌入](https://platform.openai.com/docs/guides/embeddings)[模型](https://openai.com/blog/new-and-improved-embedding-model)）余弦相似度构造有向图 $G=(V, E)$，每个节点指向其 $k$ 个最近邻；(2) 从已选样本集 $\mathcal{L}=\emptyset$ 与剩余样本集 $\mathcal{U}$ 出发，每个样本 $u \in \mathcal{U}$ 按 $$
\text{score}(u) = \sum_{v \in \{v \mid (u, v) \in E, v\in \mathcal{U}\}} s(v)\quad\text{where }s(v)=\rho^{- \vert \{\ell \in \mathcal{L} \vert (v, \ell)\in E \}\vert},\quad\rho > 1
$$ 打分，使得 $v$ 的许多邻居被选中时 $s(v)$ 低，从而打分鼓励挑选多样样本。
- [Rubin et al. (2022)](https://arxiv.org/abs/2112.08633) 提出针对一个训练数据集，通过[对比学习](https://lilianweng.github.io/posts/2021-05-31-contrastive/)训练专门用于上下文学习样本选择的嵌入。给定每个训练对 $(x, y)$，一个示例 $e_i$（格式化的输入-输出对）的质量可用 LM 赋予的条件概率度量：$\text{score}(e_i) = P_\text{LM}(y \mid e_i, x)$。我们可以为每个训练对识别分数 top-$k$ 与 bottom-$k$ 的其他示例分别作为正负候选集，用于对比学习。
- 一些研究者尝试用 [Q-Learning](https://lilianweng.github.io/posts/2018-02-19-rl-overview/#q-learning-off-policy-td-control) 做样本选择。（[Zhang et al. 2022](https://arxiv.org/abs/2211.04486)）
- 受基于不确定性的[主动学习](https://lilianweng.github.io/posts/2022-02-20-active-learning/)启发，[Diao et al. (2023)](https://arxiv.org/abs/2302.12246) 建议识别多次采样试验间分歧高或熵高的示例，然后标注这些示例用于少样本提示。

### 示例排序技巧

- 一般建议：保持所选示例多样、与测试样本相关、并以随机顺序排列，以避免多数标签偏差与近因偏差。
- 增大模型规模或纳入更多训练示例并不会降低上下文示例不同排列间的方差。同一顺序对一个模型可能好用、对另一个可能糟糕。验证集有限时，考虑选择使模型不产生极端不平衡预测、也不过度自信的顺序。（[Lu et al. 2022](https://arxiv.org/abs/2104.08786)）

# 指令提示

在提示中呈现少样本示例的目的是向模型解释我们的意图；换言之，以示范的形式向模型描述任务指令。然而少样本在 token 用量上昂贵，且受上下文长度限制而限制输入长度。那么，为什么不直接给出指令？

*指令 LM（Instructed LM）*（如 [InstructGPT](https://openai.com/research/instruction-following)、[natural instruction](https://github.com/allenai/natural-instructions)）用高质量的（任务指令, 输入, 真值输出）元组微调预训练模型，使 LM 更好理解用户意图并遵循指令。[RLHF](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/#rl-fine-tuning-with-human-preferences)（基于人类反馈的强化学习）是常见方法。指令跟随式微调的收益是使模型更对齐人类意图，并大幅降低沟通成本。

与指令模型交互时，我们应详细描述任务需求，力求*具体*且*精确*，避免说"不要做什么"，而要指明要做什么。

```
Please label the sentiment towards the movie of the given movie review. The sentiment label should be "positive" or "negative". 
Text: i'll bet the video game is a lot more fun than the film. 
Sentiment:
```

说明期望的受众是给指令的另一种聪明方式

- 例如为孩子生成教育材料，

```
Describe what is quantum physics to a 6-year-old.
```

- 以及安全内容，

```
... in language that is safe for work.
```

*上下文指令学习（In-context instruction learning）*（[Ye et al. 2023](https://arxiv.org/abs/2302.14691)）把少样本学习与指令提示结合。它在提示中纳入跨多个任务的多个示范，每个示范由指令、任务输入与输出组成。注意他们的实验只在分类任务上，且指令提示包含所有标签选项。

```
Definition: Determine the speaker of the dialogue, "agent" or "customer".
Input: I have successfully booked your tickets.
Ouput: agent

Definition: Determine which category the question asks for, "Quantity" or "Location".
Input: What's the oldest building in US?
Ouput: Location

Definition: Classify the sentiment of the given movie review, "positive" or "negative".
Input: i'll bet the video game is a lot more fun than the film.
Output:
```

# 自洽采样

**自洽采样（Self-consistency sampling）**（[Wang et al. 2022a](https://arxiv.org/abs/2203.11171)）以温度 > 0 采样多个输出，然后从这些候选中选出最佳。
选最佳候选的标准因任务而异。一般方案是**多数投票**。对易于验证的任务（如带单元测试的编程题），我们可以直接跑解释器并用单元测试验证正确性。

# 思维链（CoT）

**思维链提示（Chain-of-thought，CoT prompting）**（[Wei et al. 2022](https://arxiv.org/abs/2201.11903)）生成一列短句逐步描述推理逻辑（称*推理链*或*理据/rationales*），最终导出最终答案。CoT 的收益在**复杂推理任务**上、使用**大模型**（如参数超过 50B）时更明显。简单任务从 CoT 提示中获益甚微。

## CoT 提示的类型

两种主要的 CoT 提示：

- **少样本 CoT**。用若干示范提示模型，每个示范含手工编写（或模型生成）的高质量推理链。

（所有数学推理示例来自 [GSM8k](https://github.com/openai/grade-school-math)）

```
Question: Tom and Elizabeth have a competition to climb a hill. Elizabeth takes 30 minutes to climb the hill. Tom takes four times as long as Elizabeth does to climb the hill. How many hours does it take Tom to climb up the hill?
Answer: It takes Tom 30*4 = <<30*4=120>>120 minutes to climb the hill.
It takes Tom 120/60 = <<120/60=2>>2 hours to climb the hill.
So the answer is 2.
===
Question: Jack is a soccer player. He needs to buy two pairs of socks and a pair of soccer shoes. Each pair of socks cost $9.50, and the shoes cost $92. Jack has $40. How much more money does Jack need?
Answer: The total cost of two pairs of socks is $9.50 x 2 = $<<9.5*2=19>>19.
The total cost of the socks and the shoes is $19 + $92 = $<<19+92=111>>111.
Jack need $111 - $40 = $<<111-40=71>>71 more.
So the answer is 71.
===
Question: Marty has 100 centimeters of ribbon that he must cut into 4 equal parts. Each of the cut parts must be divided into 5 equal parts. How long will each final cut be?
Answer:
```

- **零样本 CoT**。用 `Let's think step by step` 这类自然语言语句显式鼓励模型先生成推理链，再用 `Therefore, the answer is` 提示产生答案（[Kojima et al. 2022](https://arxiv.org/abs/2205.11916)）。或类似语句 `Let's work this out it a step by step to be sure we have the right answer`（[Zhou et al. 2022](https://arxiv.org/abs/2211.01910)）。

```
Question: Marty has 100 centimeters of ribbon that he must cut into 4 equal parts. Each of the cut parts must be divided into 5 equal parts. How long will each final cut be?
Answer: Let's think step by step.
```

## 技巧与扩展

- [自洽采样](#self-consistency-sampling)可通过采样多个多样答案再取多数投票来提升推理准确率。（[Wang et al. 2022a](https://arxiv.org/abs/2203.11171)）
- 集成学习的另一做法是在多次采样试验中改变示例顺序或用模型生成的理据替换人写的，以引入随机性。然后用多数投票聚合模型输出得到最终答案。（[Wang et al. 2022b](https://arxiv.org/abs/2207.00747)）
- 若训练示例只有真答案（易于验证！）而无理据，我们可以遵循 *STaR*（Self-Taught Reasoner；[Zelikman et al. 2022](https://arxiv.org/abs/2203.14465)）方法：(1) 让 LLM 生成推理链，只保留导向正确答案的那些；(2) 然后用生成的理据微调模型并重复该过程直至收敛。注意温度越高越可能生成"答案对但理据错"。若训练示例没有真值答案，或许可考虑用多数投票作为"正确"答案。
- 带更高推理复杂度示范的提示能取得更好性能，复杂度按链中推理步数度量。分离推理步骤时，换行符 `\n` 比 `step i`、句号 `.` 或分号 `;` 效果更好。（[Fu et al. 2023](https://arxiv.org/abs/2210.00720)）
- *基于复杂度的一致性（Complexity-based consistency）*是在全部生成中只对最复杂的前 $k$ 条链做多数投票，显式偏好复杂链。（[Fu et al. 2023](https://arxiv.org/abs/2210.00720)）
- 后来，[Shum et al. (2023)](https://arxiv.org/abs/2302.12822) 发现在他们的实验中，只含复杂示例的 CoT 提示能提升复杂问题的准确率，但在简单问题上表现差；证据见 GSM8k。
- 把 `Q:` 改为 `Question:` 被发现有帮助。（[Fu et al. 2023](https://arxiv.org/abs/2210.00720)）
- [Ye & Durrett (2022)](https://arxiv.org/abs/2205.03401) 发现在涉及文本推理的 NLP 任务（即 QA 与 NLI）上，提示中纳入解释的收益为小到中等，且效果因模型而异。他们观察到解释更可能不真实而非不一致（即解释是否蕴含预测）。不真实的解释很可能导致错误预测。
- *Self-Ask*（[Press et al. 2022](https://arxiv.org/abs/2210.03350)）是一种反复提示模型*提出后续问题*以迭代构建思路的方法。后续问题可由搜索引擎结果回答。类似地，*IRCoT*（Interleaving Retrieval CoT；[Trivedi et al. 2022](https://arxiv.org/abs/2212.10509)）与 *ReAct*（Reason + Act；[Yao et al. 2023](https://arxiv.org/abs/2210.03629)）把迭代 CoT 提示与对 Wikipedia API 的查询结合，搜索相关实体与内容再加回上下文。

![](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/SelfAsk-search.png)

*Self-Ask 如何配合外部搜索查询。（图片来源：Press et al. 2022 ）。*

- *思维树（Tree of Thoughts）*（[Yao et al. 2023](https://arxiv.org/abs/2305.10601)）扩展 CoT，在每步探索多种推理可能。它先把问题分解为多个思考步骤并每步生成多个思考，本质上是创建一棵树。搜索过程可用 BFS 或 DFS，每个状态由分类器（经提示）或多数投票评估。

![](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/tree-of-thoughts.png)

*Self-Ask 如何配合外部搜索查询。（图片来源：Yao et al. 2022 ）。*

# 自动提示设计

提示是一段前缀 token 序列，能提高给定输入得到期望输出的概率。因此我们可以把它们视为可训练参数，经梯度下降在嵌入空间[直接优化](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/#smart-prompt-design)，如 **AutoPrompt**（[Shin et al., 2020](https://arxiv.org/abs/2010.15980)）、**Prefix-Tuning**（[Li & Liang (2021)](https://arxiv.org/abs/2101.00190)）、**P-tuning**（[Liu et al. 2021](https://arxiv.org/abs/2103.10385)）与 **Prompt-Tuning**（[Lester et al. 2021](https://arxiv.org/abs/2104.08691)）。[我的"可控神经文本生成"一文的相关小节](https://lilianweng.github.io/posts/2021-01-02-controllable-text-generation/#smart-prompt-design)对它们有良好覆盖。从 AutoPrompt 到 Prompt-Tuning 的趋势是设定逐渐简化。

**APE**（Automatic Prompt Engineer；[Zhou et al. 2022](https://arxiv.org/abs/2211.01910)）是在模型生成的指令候选池上搜索，然后按选定评分函数过滤候选集，最终选出得分最高的最佳候选。

1. 提示 LLM 基于一小组输入-输出对形式的示范生成指令候选。如 `{{Given desired input-output pairs}}\n\nThe instruction is`。
2. 给定数据集 $\mathcal{D}_\text{train} = \{(x, y)\}$，我们想找指令 $\rho$ 使 $\rho^* = \arg\max_\rho \mathbb{E}_{(x, y) \in \mathcal{D}_\text{train}} [f(\rho, x, y)]$，其中 $f(.)$ 是逐样本评分函数，如执行准确率 $\mathbb{1}[\text{LM}(.\vert \rho, x)=y]$ 或对数概率 $p_\text{LM}(y \mid \rho, x)$。
3. 用迭代蒙特卡洛搜索改进最佳候选，通过类似 `Generate a variation of the following instruction while keeping the semantic meaning.\n\nInput: ...\n\nOutput:...` 的提示提出语义相近的变体。

为自动构造思维链提示，[Shum et al. (2023)](https://arxiv.org/abs/2302.12822) 提出"增强-剪枝-选择"三步流程：

1. *增强（Augment）*：给定问题，用少样本或零样本 CoT 提示生成多条伪思维链；
2. *剪枝（Prune）*：按生成答案是否匹配真值来剪除伪链。
3. *选择（Select）*：应用方差缩减的策略梯度策略学习所选示例上的概率分布，把示例上的概率分布视为策略、验证集准确率视为奖励。

[Zhang et al. (2023)](https://arxiv.org/abs/2210.03493) 则采用*聚类*技术采样问题再生成链。他们观察到 LLM 倾向犯某些类型的错误。一类错误在嵌入空间中可能相似从而聚在一起。只从高频错误簇中采样一两个，可以避免同一错误类型的错误示范过多，并收集多样的示例集。

1. *问题聚类*：嵌入问题并运行 $k$-means 聚类。
2. *示范选择*：从每个簇选一组代表性问题；即一个簇一个示范。每个簇中样本按到簇质心的距离排序，靠近质心的先被选中。
3. *理据生成*：用零样本 CoT 为所选问题生成推理链，构造少样本提示做推理。

# 增强语言模型

[Mialon et al. (2023)](https://arxiv.org/abs/2302.07842) 的增强语言模型综述很好地覆盖了多类带推理技能与外部工具使用能力的语言模型。推荐阅读。

## 检索

我们常需完成那些要求模型预训练截止时间之后的最新知识、或内部/私有知识库的任务。此时若不在提示中显式提供，模型不会知道上下文。许多[开放域问答](https://lilianweng.github.io/posts/2020-10-29-odqa/)方法依赖先在知识库上检索、再把检索到的内容作为提示的一部分。该过程的准确性取决于检索与生成两步的质量。

[Lazaridou et al. (2022)](https://arxiv.org/abs/2203.05115) 研究了如何用 Google Search 做文档检索来增强 LLM。给定问题 $q$，从 Google 返回的 20 个 URL 中抽取干净文本，得到一组文档。由于这些文档很长，每篇被切成 6 句的段落 $\{p\}$。按证据段落与查询间基于 TF-IDF 的余弦相似度对段落排序。只有最相关的段落用于提示以产生答案 $a$。

对闭卷 QA，每个示范格式如下以构造少样本提示。把证据与问题对调（问题与答案距离更远）被发现一致地在所有数据集上产生更低结果。

```
Evidence: ...
Question: ...
Answer: ...
```

答案概率用三种方式计算：

1. [RAG](https://lilianweng.github.io/posts/2020-10-29-odqa/#RAG) 式，$p(a_i \mid q) = \sum_{i=1}^n p_\text{tf-idf} (p_i \mid q) \cdot p_\text{LM}(a_i \mid q, p_i)$，其中 $p_\text{tf-idf} (p_i \mid q)$ 是 TF-IDF 段落与问题表示间归一化的余弦相似度。
2. 噪声信道推断，$p(a_i\mid q) = \frac{p_\text{LM}(q \mid a_i, p_i) \cdot p_\text{LM}(a_i \mid p_i)}{p_\text{LM}(q \mid p_i)}$
3. 专家乘积（Product-of-Experts，PoE），组合上述全部概率并外加 $p_\text{LM}(p_i \mid q)$。

根据他们在生成与分类任务上的实验，三种答案重排分数中 PoE > 噪声信道 > RAG。在单个概率中，$p_\text{LM}(a \mid q, p_i)$ 与 $p_\text{LM}(q \mid p_i, a)$ 被发现信息量最大。$p_\text{LM}(q \mid p_i, a)$ 刻画给定证据段落与答案时 LM 能多好地解释问题，可可靠地用于重排答案候选。

对基于不同日期提问的 [SituatedQA](https://situatedqa.github.io/) 数据集的一个观察是：尽管 LM（预训练截止为 2020 年）可以通过 Google Search 获取最新信息，它在 2020 年后问题上的表现仍比 2020 年前问题*差*得多。这表明上下文信息与模型内部知识之间存在某种分歧或参数冲突。

有趣的是，即使只有"内部检索"也被发现有益——即在回答问题前先生成关于某主题的知识（[Liu et al. 2022](https://arxiv.org/abs/2110.08387)）。首先可用以下模板抽取知识：

```
Generate some knowledge about the input. Examples:

Input: What type of water formation is formed by clouds?
Knowledge: Clouds are made of water vapor.

Input: {question}
Knowledge:
```

然后带着模型生成的知识，进一步提示 LM 得到答案。

## 编程语言

**PAL**（Program-aided language models；[Gao et al. 2022](https://arxiv.org/abs/2211.10435)）与 **PoT**（Program of Thoughts prompting；[Chen et al. 2022](https://arxiv.org/abs/2211.12588)）都要求 LLM 生成编程语言语句来解决自然语言推理问题，从而把求解步骤交给 Python 解释器等运行时。该设定把复杂计算与推理解耦。它依赖编码能力足够好的 LM。

![](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/PoT.png)

*CoT 与 PoT 的对比。（图片来源：Chen et al. 2022 ）。*

## 外部 API

**TALM**（Tool Augmented Language Models；[Parisi et al. 2022](https://arxiv.org/abs/2205.12255)）是用文本到文本 API 调用增强的语言模型。LM 被引导在任务输入文本条件下生成 `|tool-call` 与 `tool input text` 来构造 API 调用请求。当 `|result` 出现时，调用指定的工具 API，返回结果被追加到文本序列。最终输出跟在 `|output` token 之后生成。

![](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/TALM.png)

*TALM 中 API 调用的格式。（图片来源：Parisi et al. 2022 ）。*

TALM 采用自我博弈方法，迭代地自举工具使用示例数据集并用其微调 LM。这一自我博弈（定义为模型与工具 API 交互）根据新增工具 API 是否能改进模型输出来迭代扩充数据集。Toolformer 也采用了同样思想，下文详述。该管线粗略模仿 RL 过程：LM 是策略网络，用带二值奖励信号的策略梯度训练。

![](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/TALM-iteration.png)

*自我博弈迭代帮助提升模型性能。（图片来源：Parisi et al. 2022 ）。*

**Toolformer**（[Schick et al. 2023](https://arxiv.org/abs/2302.04761)）是一个能通过简单 API 使用外部工具的 LM，以自监督方式构建，每个 API 只需少量示范。Toolformer 的工具箱包括：

- *计算器*，弥补 LM 缺乏精确数学技能；
- *问答系统*，帮助应对不忠实内容与幻觉；
- *搜索引擎*，提供预训练截止时间之后的最新信息；
- *翻译系统*，提升低资源语言上的性能；
- *日历*，让 LM 感知时间推移。

![](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/toolformer.png)

*如何构建 Toolformer 的示意图。（图片来源：Schick et al. 2023 ）。*

Toolformer 的训练方式如下：

1. *提示标注潜在 API 调用*。让预训练 LM 通过少样本学习、用 API 调用使用示例标注数据集。格式示例：

   ![](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/toolformer-annotation.png)

   *数据集如何被标注做 API 调用。（图片来源：Schick et al. 2023 ）。*

```
- Each API call is represented as a tuple of (API name, corresponding input), $c=(a_c, i_c)$ and its corresponding result is denoted as $r$. The API call sequences with and without results are labeled as follows, respectively:

    <div>
    $$
    \begin{aligned}
    e(c) &= \langle\texttt{API}\rangle a_c(i_c) \langle\texttt{/API}\rangle \\
    e(c, r) &= \langle\texttt{API}\rangle a_c(i_c) \to r \langle\texttt{/API}\rangle
    \end{aligned}
    $$
    </div>

- Sample API calls based on the probabilities $p_\text{LM}(\langle\texttt{API}\rangle \mid \text{prompt}(\mathbf{x}), \mathbf{x}_{1:i})$ and select top $k$ candidate positions for doing API calls at position $i$ if the probability is larger than a threshold.

- Then we sample potential API calls from the LM given the sequence $[\text{prompt}(\mathbf{x}), x_1, \dots, x_{i-1}, \langle\texttt{API}\rangle]$ as prefix and $\langle\texttt{/API}\rangle$ as suffix.
```

2. *按 API 调用是否帮助模型预测未来 token 过滤标注*。用自监督损失决定哪些 API 调用真正有帮助。

   - 执行每个 API 调用 $c_i$ 得到对应结果 $r_i$。
   - 计算模型以提示为前缀时，LM 在 token $x_i, \dots, x_n$ 上的加权交叉熵损失。计算两个版本，一个带 API 结果，另一个带空序列 $\varepsilon$。

     $$
  \begin{aligned}
  L^+_i &= L_i(e(c_i, r_i)) \\
  L^-_i &= \min(L_i(\varepsilon), L_i(e(c_i, \varepsilon))) \\
  \end{aligned}
  $$

     只保留 $L^-_i - L^+_i$ 大于阈值的 API 调用，意味着加入该 API 调用及其结果帮助模型预测未来 token。
3. *在该标注数据集上微调 LM*。新训练序列构造为 $\mathbf{x}^* = x_{1:i-1}, e(c_i, r_i), x_{i:n}$。训练数据是原始数据集（如论文中 CCNet 的子集）与其增强版本的组合。

推理时，解码运行到模型产生 "$\to$ " token 为止，表示它预期接下来是某次 API 调用的响应。

Toolformer 目前不支持链式工具使用（即用一个工具的输出作为另一工具的输入）或交互式使用（即人工选择后采纳 API 响应）。两者都是扩展模型的有趣未来方向。

# 引用

引用格式：

> Weng, Lilian. (Mar 2023). Prompt Engineering. Lil'Log. https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/.

或

```
@article{weng2023prompt,
  title   = "Prompt Engineering",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io",
  year    = "2023",
  month   = "Mar",
  url     = "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/"
}
```

# 有用资源

- [OpenAI Cookbook](https://github.com/openai/openai-cookbook) 有许多如何高效利用 LLM 的深入示例。
- [LangChain](https://langchain.readthedocs.io/en/latest/)，一个把语言模型与其他组件结合构建应用的库。
- [Prompt Engineering Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) 仓库包含相当全面的提示工程教育材料合集。
- [learnprompting.org](https://learnprompting.org/docs/intro)
- [PromptPerfect](https://promptperfect.jina.ai)
- [Semantic Kernel](https://github.com/microsoft/semantic-kernel)

# 参考文献

[1] Zhao et al. ["Calibrate Before Use: Improving Few-shot Performance of Language Models."](https://arxiv.org/abs/2102.09690) ICML 2021

[2] Liu et al. ["What Makes Good In-Context Examples for GPT-3?"](https://arxiv.org/abs/2101.06804) arXiv preprint arXiv:2101.06804 (2021).

[3] Lu et al. ["Fantastically Ordered Prompts and Where to Find Them: Overcoming Few-Shot Prompt Order Sensitivity."](https://arxiv.org/abs/2104.08786) ACL 2022

[4] Ye et al. ["In-Context Instruction Learning."](https://arxiv.org/abs/2302.14691) arXiv preprint arXiv:2302.14691 (2023).

[5] Su et al. ["Selective annotation makes language models better few-shot learners."](https://arxiv.org/abs/2209.01975) arXiv preprint arXiv:2209.01975 (2022).

[6] Rubin et al. ["Learning to retrieve prompts for in-context learning."](https://arxiv.org/abs/2112.08633) NAACL-HLT 2022

[7] Wei et al. ["Chain of thought prompting elicits reasoning in large language models."](https://arxiv.org/abs/2201.11903) NeurIPS 2022

[8] Wang et al. ["Self-Consistency Improves Chain of Thought Reasoning in Language Models."](https://arxiv.org/abs/2203.11171) ICLR 2023.

[9] Diao et al. ["Active Prompting with Chain-of-Thought for Large Language Models."](https://arxiv.org/abs/2302.12246) arXiv preprint arXiv:2302.12246 (2023).

[10] Zelikman et al. ["STaR: Bootstrapping Reasoning With Reasoning."](https://arxiv.org/abs/2203.14465) arXiv preprint arXiv:2203.14465 (2022).

[11] Ye & Durrett. ["The unreliability of explanations in few-shot in-context learning."](https://arxiv.org/abs/2205.03401) arXiv preprint arXiv:2205.03401 (2022).

[12] Trivedi et al. ["Interleaving retrieval with chain-of-thought reasoning for knowledge-intensive multi-step questions."](https://arxiv.org/abs/2212.10509) arXiv preprint arXiv:2212.10509 (2022).

[13] Press et al. ["Measuring and narrowing the compositionality gap in language models."](https://arxiv.org/abs/2210.03350) arXiv preprint arXiv:2210.03350 (2022).

[14] Yao et al. ["ReAct: Synergizing reasoning and acting in language models."](https://arxiv.org/abs/2210.03629) ICLR 2023.

[15] Fu et al. ["Complexity-based prompting for multi-step reasoning."](https://arxiv.org/abs/2210.00720) arXiv preprint arXiv:2210.00720 (2022).

[16] Wang et al. ["Rationale-augmented ensembles in language models."](https://arxiv.org/abs/2207.00747) arXiv preprint arXiv:2207.00747 (2022).

[17] Zhang et al. ["Automatic chain of thought prompting in large language models."](https://arxiv.org/abs/2210.03493) arXiv preprint arXiv:2210.03493 (2022).

[18] Shum et al. ["Automatic Prompt Augmentation and Selection with Chain-of-Thought from Labeled Data."](https://arxiv.org/abs/2302.12822) arXiv preprint arXiv:2302.12822 (2023).

[19] Zhou et al. ["Large Language Models Are Human-Level Prompt Engineers."](https://arxiv.org/abs/2211.01910) ICLR 2023.

[20] Lazaridou et al. ["Internet augmented language models through few-shot prompting for open-domain question answering."](https://arxiv.org/abs/2203.05115) arXiv preprint arXiv:2203.05115 (2022).

[21] Chen et al. ["Program of Thoughts Prompting: Disentangling Computation from Reasoning for Numerical Reasoning Tasks."](https://arxiv.org/abs/2211.12588) arXiv preprint arXiv:2211.12588 (2022).

[22] Gao et al. ["PAL: Program-aided language models."](https://arxiv.org/abs/2211.10435) arXiv preprint arXiv:2211.10435 (2022).

[23] Parisi et al. ["TALM: Tool Augmented Language Models"](https://arxiv.org/abs/2205.12255) arXiv preprint arXiv:2205.12255 (2022).

[24] Schick et al. ["Toolformer: Language Models Can Teach Themselves to Use Tools."](https://arxiv.org/abs/2302.04761) arXiv preprint arXiv:2302.04761 (2023).

[25] Mialon et al. ["Augmented Language Models: a Survey"](https://arxiv.org/abs/2302.07842) arXiv preprint arXiv:2302.07842 (2023).

[26] Yao et al. ["Tree of Thoughts: Deliberate Problem Solving with Large Language Models."](https://arxiv.org/abs/2305.10601) arXiv preprint arXiv:2305.10601 (2023).
