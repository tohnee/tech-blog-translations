---
title: "DeepSeekMath：推动开放语言模型数学推理的极限"
title_en: "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models"
arxiv: 2402.03300
source: https://arxiv.org/abs/2402.03300
crawled: 2026-09-23
translated: 2026-09-23
---

# DeepSeekMath：推动开放语言模型数学推理的极限

> 原文：[DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models](https://arxiv.org/abs/2402.03300) · Stanford CS329A 指定阅读

报告编号 001

Zhihong Shao1,2∗†, Peiyi Wang1,3∗†, Qihao Zhu1,3∗†, Runxin Xu1, Junxiao Song1
  
Xiao Bi1,
Haowei Zhang1,
Mingchuan Zhang1,
Y.K. Li1,
Y. Wu1,
Daya Guo1∗
1DeepSeek-AI, 2清华大学, 3北京大学
  
{zhihongshao,wangpeiyi,zhuqh,guoday}@deepseek.com
  
<https://github.com/deepseek-ai/DeepSeek-Math>
通讯作者： ∗ 核心贡献者。
  
† 本工作完成于在 DeepSeek-AI 实习期间。

###### 摘要

数学推理因其复杂且结构化的性质，对语言模型构成了重大挑战。在本文中，我们提出 DeepSeekMath 7B，它以 120B 取自 Common Crawl 的数学相关 token，加上自然语言与代码数据，在 DeepSeek-Coder-Base-v1.5 7B 之上继续预训练。DeepSeekMath 7B 在竞赛级 MATH 基准测试上取得了 51.7% 的瞩目分数，且不依赖外部工具包与投票技术，接近 Gemini-Ultra 与 GPT-4 的性能水平。对 DeepSeekMath 7B 的 64 个样本做自洽性投票在 MATH 上达到 60.9%。DeepSeekMath 的数学推理能力归因于两个关键因素：第一，我们通过一套精心工程化的数据筛选流水线，挖掘了公开网络数据的巨大潜力；第二，我们提出组相对策略优化（Group Relative Policy Optimization，GRPO），它是近端策略优化（PPO）的一个变体，在提升数学推理能力的同时优化了 PPO 的显存占用。

![Refer to caption](2402.03300v3/figures/Math.png)

图 1：开源模型在竞赛级 MATH 基准测试（Hendrycks et al., 2021）上的 Top1 准确率，未使用外部工具包与投票技术。

## 1 引言

大型语言模型（LLM）彻底改变了人工智能进行数学推理的方式，推动定量推理基准（Hendrycks et al., 2021）与几何推理基准（Trinh et al., 2024）双双取得重大进展。此外，这些模型已被证明能有效地辅助人类求解复杂数学问题（Tao, 2023）。然而，GPT-4（OpenAI, 2023）与 Gemini-Ultra（Anil et al., 2023）等前沿模型并未公开，而当前可获取的开源模型在性能上明显落后。

在本研究中，我们提出 DeepSeekMath，一个领域专用语言模型，它显著超越开源模型的数学能力，并在学术基准上接近 GPT-4 的性能水平。为此，我们构建了 DeepSeekMath 语料库，一个由 120B 数学 token 组成的大规模高质量预训练语料库。该数据集使用基于 fastText 的分类器（Joulin et al., 2016）从 Common Crawl（CC）中抽取。在第一轮迭代中，分类器以 OpenWebMath（Paster et al., 2023）中的实例作为正例训练，同时纳入多样化的其他网页作为负例。随后，我们用该分类器从 CC 中挖掘更多正例，并通过人工标注进一步精炼。接着，我们用这个增强后的数据集更新分类器以提升其性能。评估结果表明，这一大规模语料库质量很高：我们的基础模型 DeepSeekMath-Base 7B 在 GSM8K（Cobbe et al., 2021）上取得 64.2%，在竞赛级 MATH 数据集（Hendrycks et al., 2021）上取得 36.2%，超越 Minerva 540B（Lewkowycz et al., 2022a）。此外，DeepSeekMath 语料库是多语言的，因此我们观察到中文数学基准（Wei et al., 2023；Zhong et al., 2023）上的提升。我们相信，我们在数学数据处理上的经验可以作为研究界的起点，未来仍有巨大的改进空间。

DeepSeekMath-Base 以 DeepSeek-Coder-Base-v1.5 7B（Guo et al., 2024）初始化，因为我们注意到，相比通用 LLM，从代码训练模型出发是更好的选择。此外，我们观察到数学训练还提升了模型在 MMLU（Hendrycks et al., 2020）与 BBH 基准（Suzgun et al., 2022）上的能力，表明它不仅增强模型的数学能力，也放大了一般推理能力。

预训练之后，我们用思维链（Wei et al., 2022）、程序思维（program-of-thought）（Chen et al., 2022；Gao et al., 2023）以及工具集成推理（Gou et al., 2023）数据对 DeepSeekMath-Base 进行数学指令微调。所得模型 DeepSeekMath-Instruct 7B 胜过所有 7B 同类模型，并与 70B 开源指令微调模型相当。

此外，我们提出组相对策略优化（GRPO），一种近端策略优化（PPO）（Schulman et al., 2017）的变体强化学习（RL）算法。GRPO 舍弃了 critic 模型，转而从组分数估计基线，显著降低了训练资源。仅使用一部分英文指令微调数据，GRPO 便在强大的 DeepSeekMath-Instruct 之上取得大幅提升，包括强化学习阶段中的域内（GSM8K：82.9% → 88.2%，MATH：46.8% → 51.7%）与域外数学任务（如 CMATH：84.6% → 88.8%）。我们还提供一个统一范式来理解不同方法，如拒绝采样微调（RFT）（Yuan et al., 2023a）、直接偏好优化（DPO）（Rafailov et al., 2023）、PPO 与 GRPO。基于这一统一范式，我们发现所有这些方法都可以被概念化为直接的或简化版的 RL 技术。我们还开展了大量实验，例如在线 vs. 离线训练、结果 vs. 过程监督、单轮 vs. 迭代 RL 等，以深入探究该范式的本质要素。最后，我们解释了我们的 RL 为何能提升指令微调模型的性能，并基于这一统一范式进一步总结了实现更有效 RL 的潜在方向。

### 1.1 贡献

我们的贡献包括可扩展的数学预训练，以及对强化学习的探索与分析。

大规模数学预训练

- 我们的研究提供了有力证据，表明公开可访问的 Common Crawl 数据中蕴含着有价值的数学信息。通过实施一套精心设计的数据筛选流水线，我们成功构建了 DeepSeekMath 语料库——一个从筛选出的数学网页中获得的高质量 120B token 数据集，其规模约为 Minerva（Lewkowycz et al., 2022a）所用数学网页的 7 倍，是近期发布的 OpenWebMath（Paster et al., 2023）的 9 倍。
- 我们预训练的基础模型 DeepSeekMath-Base 7B 取得了与 Minerva 540B（Lewkowycz et al., 2022a）相当的性能，表明参数数量并非数学推理能力的唯一关键因素。在高质量数据上预训练的小模型同样能取得强大性能。
- 我们分享数学训练实验的发现。数学训练之前进行代码训练，能提升模型在有工具与无工具两种条件下求解数学问题的能力。这为一个长期存在的问题提供了部分答案：代码训练能否提升推理能力？我们认为是能的，至少对数学推理而言如此。
- 尽管在 arXiv 论文上训练很常见，尤其是在许多数学相关论文中，但它在本论文采用的所有数学基准上均未带来显著提升。

强化学习的探索与分析

- 我们提出组相对策略优化（GRPO），一种高效且有效的强化学习算法。GRPO 舍弃 critic 模型，转而从组分数估计基线，与近端策略优化（PPO）相比显著降低了训练资源。
- 我们证明，仅使用指令微调数据，GRPO 便能显著提升我们的指令微调模型 DeepSeekMath-Instruct 的性能。此外，我们观察到强化学习过程中域外性能的提升。
- 我们提供一个统一范式来理解不同方法，如 RFT、DPO、PPO 与 GRPO。我们还开展了大量实验，例如在线 vs. 离线训练、结果 vs. 过程监督、单轮 vs. 迭代强化学习等，以深入探究该范式的本质要素。
- 基于我们的统一范式，我们探索了强化学习有效背后的原因，并总结了若干实现更有效 LLM 强化学习的潜在方向。

### 1.2 评测与指标概览

- 英文与中文数学推理：我们在英文与中文基准上对模型进行全面评估，覆盖从小学到大学程度的数学问题。英文基准包括 GSM8K（Cobbe et al., 2021）、MATH（Hendrycks et al., 2021）、SAT（Azerbayev et al., 2023）、OCW Courses（Lewkowycz et al., 2022a）、MMLU-STEM（Hendrycks et al., 2020）。中文基准包括 MGSM-zh（Shi et al., 2023）、CMATH（Wei et al., 2023）、Gaokao-MathCloze（Zhong et al., 2023）与 Gaokao-MathQA（Zhong et al., 2023）。我们评估模型在不使用工具的情况下生成自包含文本解答的能力，以及使用 Python 求解问题的能力。

  在英文基准上，DeepSeekMath-Base 与闭源的 Minerva 540B（Lewkowycz et al., 2022a）具有竞争力，并超越所有开源基础模型（如 Mistral 7B（Jiang et al., 2023）与 Llemma-34B（Azerbayev et al., 2023）），无论后者是否经过数学预训练，且往往领先幅度显著。值得注意的是，DeepSeekMath-Base 在中文基准上更为出色，这可能是因为我们没有像先前工作（Lewkowycz et al., 2022a；Azerbayev et al., 2023）那样只收集英文数学预训练数据，而是同时纳入了高质量的非英文数据。经过数学指令微调与强化学习，所得的 DeepSeekMath-Instruct 与 DeepSeekMath-RL 展现出强大性能，在开源社区中首次于竞赛级 MATH 数据集上取得超过 50% 的准确率。
- 形式数学：我们使用 Jiang et al. (2022) 的非正式到形式化定理证明任务，在 miniF2F（Zheng et al., 2021）上评估 DeepSeekMath-Base，并选用 Isabelle（Wenzel et al., 2008）作为证明助手。DeepSeekMath-Base 展现了强大的少样本自动形式化性能。
- 自然语言理解、推理与代码：为全面刻画模型的一般理解、推理与编程能力，我们在大规模多任务语言理解（MMLU）基准（Hendrycks et al., 2020）——涵盖 57 个不同学科多项选择任务、BIG-Bench Hard（BBH）（Suzgun et al., 2022）——由 23 个大多需要多步推理求解的挑战性任务组成，以及广泛用于评估代码语言模型的 HumanEval（Chen et al., 2021）与 MBPP（Austin et al., 2021）上评估 DeepSeekMath-Base。数学预训练对语言理解与推理性能均有益处。

## 2 数学预训练

### 2.1 数据收集与去污染

在本节中，我们将概述从 Common Crawl 构建 DeepSeekMath 语料库的过程。如图 2 所示，我们展示了一条迭代式流水线，说明如何从一个种子语料库（例如一个小而高质量的数学相关数据集合）出发，系统性地从 Common Crawl 收集大规模数学语料。值得注意的是，这一方法也适用于其他领域，例如代码。

![Refer to caption](2402.03300v3/pipeline.png)

图 2：从 Common Crawl 收集数学网页的迭代式流水线。

首先，我们选择 OpenWebMath（Paster et al., 2023）——一个高质量数学网页文本合集——作为初始种子语料库。利用该语料库，我们训练一个 fastText 模型（Joulin et al., 2016）来召回更多与 OpenWebMath 相似的数学网页。具体而言，我们从种子语料库中随机选取 500,000 个数据点作为正例训练样本，另从 Common Crawl 中选取 500,000 个网页作为负例。我们采用开源库 fastText（<https://fasttext.cc>）进行训练，将向量维度设为 256，学习率设为 0.1，词 n-gram 最大长度设为 3，词最小出现次数设为 3，训练轮数设为 3。为缩减原始 Common Crawl 的规模，我们采用基于 URL 的去重与近似去重技术，得到 40B 个 HTML 网页。随后，我们用 fastText 模型从去重后的 Common Crawl 中召回数学网页。为过滤低质量数学内容，我们根据 fastText 模型预测的分数对收集到的网页排序，只保留排名靠前的网页。保留数据量通过对 top 40B、80B、120B 与 160B token 的预训练实验来评估。在第一轮迭代中，我们选择保留 top 40B token。

第一轮数据收集之后，仍有许多数学网页未被收集到，主要因为 fastText 模型训练所用的正例集合缺乏足够多样性。因此，我们识别更多数学网络来源以扩充种子语料库，从而优化 fastText 模型。具体而言，我们首先将整个 Common Crawl 组织成互不相交的域；一个域定义为共享相同基础 URL 的网页集合。对每个域，我们计算第一轮迭代中被收集网页的百分比。超过 10% 网页被收集的域被归类为数学相关（如 [mathoverflow.net](https://mathoverflow.net)）。随后，我们人工标注这些被识别域中与数学内容相关联的 URL（如 [mathoverflow.net/questions](https://mathoverflow.net/questions)）。链接到这些 URL 但尚未被收集的网页将被加入种子语料库。这一方法使我们能收集更多正例，从而训练一个改进的 fastText 模型，在下一轮迭代中召回更多数学数据。经过四轮数据收集迭代，我们最终获得 35.5M 个数学网页，共计 120B token。在第四轮迭代中，我们注意到近 98% 的数据已在第三轮迭代中被收集，因此决定停止数据收集。

为避免基准污染，我们遵循 Guo et al. (2024) 的做法，过滤掉包含英文数学基准（如 GSM8K（Cobbe et al., 2021）与 MATH（Hendrycks et al., 2021））以及中文基准（如 CMATH（Wei et al., 2023）与 AGIEval（Zhong et al., 2023））中题目或答案的网页。过滤标准如下：任何包含与评测基准中任一子串完全匹配的 10-gram 字符串的文本段，都将从我们的数学训练语料库中移除。对于长度不足 10-gram 但至少 3-gram 的基准文本，我们采用精确匹配来过滤受污染网页。

### 2.2 验证 DeepSeekMath 语料库的质量

我们运行预训练实验，考察 DeepSeekMath 语料库与近期发布的数学训练语料库的对比：

- MathPile（Wang et al., 2023c）：一个多来源语料库（8.9B token），从教科书、Wikipedia、ProofWiki、CommonCrawl、StackExchange 与 arXiv 聚合而来，其中大部分（超过 85%）来自 arXiv；
- OpenWebMath（Paster et al., 2023）：经过数学内容过滤的 CommonCrawl 数据，共计 13.6B token；
- Proof-Pile-2（Azerbayev et al., 2023）：由 OpenWebMath、AlgebraicStack（10.3B token 数学代码）与 arXiv 论文（28.0B token）组成的数学语料库。在 Proof-Pile-2 上实验时，我们遵循 Azerbayev et al. (2023) 使用 2:4:1 的 arXiv:Web:Code 比例。

#### 2.2.1 训练设定

我们将数学训练应用于一个拥有 1.3B 参数的通用预训练语言模型，它与 DeepSeek LLM（DeepSeek-AI, 2024）共享同一框架，记作 DeepSeek-LLM 1.3B。我们在每个数学语料库上分别训练一个模型 150B token。所有实验均使用高效轻量的 HAI-LLM（High-flyer, 2023）训练框架进行。遵循 DeepSeek LLM 的训练实践，我们使用 AdamW 优化器（Loshchilov and Hutter, 2017），$\beta_{1}=0.9$、$\beta_{2}=0.95$、$\mathrm{weight\_decay}=0.1$，并采用多步学习率调度：学习率经 2,000 步预热达到峰值，在训练进程 80% 处降至 31.6%，在训练进程 90% 处进一步降至峰值的 10.0%。我们将学习率最大值设为 5.3e-4，使用 4M token 的批次大小与 4K 上下文长度。

| 数学语料 | 规模 | GSM8K | MATH | OCW | SAT | MMLU-STEM | CMATH | Gaokao-MathCloze | Gaokao-MathQA |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 无数学训练 | N/A | 2.9% | 3.0% | 2.9% | 15.6% | 19.5% | 12.3% | 0.8% | 17.9% |
| MathPile | 8.9B | 2.7% | 3.3% | 2.2% | 12.5% | 15.7% | 1.2% | 0.0% | 2.8% |
| OpenWebMath | 13.6B | 11.5% | 8.9% | 3.7% | 31.3% | 29.6% | 16.8% | 0.0% | 14.2% |
| Proof-Pile-2 | 51.9B | 14.3% | 11.2% | 3.7% | 43.8% | 29.2% | 19.9% | 5.1% | 11.7% |
| DeepSeekMath 语料库 | 120.2B | 23.8% | 13.6% | 4.8% | 56.3% | 33.1% | 41.5% | 5.9% | 23.6% |

表 1：DeepSeek-LLM 1.3B 在不同数学语料库上训练后的性能，采用少样本思维链提示评测。语料库规模使用我们词表大小为 100K 的分词器计算。

![Refer to caption](2402.03300v3/figures/corpus_comparisons.png)

图 3：DeepSeek-LLM 1.3B 在不同数学语料库上训练的基准曲线。

#### 2.2.2 评测结果

DeepSeekMath 语料库质量高、覆盖多语言数学内容，且规模最大。

- 高质量：我们使用少样本思维链提示（Wei et al., 2022）在 8 个数学基准上评估下游性能。如表 1 所示，在 DeepSeekMath 语料库上训练的模型有明显性能领先。图 3 显示，在 50B token 处（Proof-Pile-2 的完整一个 epoch），在 DeepSeekMath 语料库上训练的模型已表现出优于 Proof-Pile-2 的性能，表明 DeepSeekMath 语料库的平均质量更高。
- 多语言：DeepSeekMath 语料库包含多种语言的数据，以英文与中文两大语言为主要代表。如表 1 所示，在 DeepSeekMath 语料库上训练能同时提升英文与中文的数学推理性能。相比之下，现有以英文为中心的数学语料库改进有限，甚至可能阻碍中文数学推理的性能。
- 大规模：DeepSeekMath 语料库比现有数学语料库大数倍。如图 3 所示，在 DeepSeekMath 语料库上训练的 DeepSeek-LLM 1.3B 呈现更陡的学习曲线以及更持久的改进。相比之下，基线语料库要小得多，在训练期间已被重复多轮，所得模型性能很快达到平台期。

### 2.3 训练与评估 DeepSeekMath-Base 7B

在本节中，我们介绍 DeepSeekMath-Base 7B，一个具有强大推理能力（尤其是数学方面）的基础模型。我们的模型以 DeepSeek-Coder-Base-v1.5 7B（Guo et al., 2024）初始化，训练 500B token。数据分布如下：56% 来自 DeepSeekMath 语料库，4% 来自 AlgebraicStack，10% 来自 arXiv，20% 为 Github 代码，其余 10% 为来自 Common Crawl 的英文与中文自然语言数据。我们主要采用第 2.2.1 节中指定的训练设定，仅将学习率最大值设为 4.2e-4、批次大小使用 10M token。

我们对 DeepSeekMath-Base 7B 的数学能力进行了全面评估，聚焦于三方面：在不依赖外部工具的情况下生成自包含数学解答的能力、使用工具求解数学问题的能力，以及进行形式化定理证明的能力。除数学之外，我们还提供了基础模型更全面的画像，包括其自然语言理解、推理与编程技能的表现。

##### 逐步推理求解数学问题

我们使用少样本思维链提示（Wei et al., 2022）评估 DeepSeekMath-Base 在中英文共八个基准上求解数学问题的表现。这些基准涵盖定量推理（如 GSM8K（Cobbe et al., 2021）、MATH（Hendrycks et al., 2021）与 CMATH（Wei et al., 2023））与多项选择题（如 MMLU-STEM（Hendrycks et al., 2020）与 Gaokao-MathQA（Zhong et al., 2023）），覆盖从小学到大学复杂度的各个数学领域。

如表 2 所示，DeepSeekMath-Base 7B 在全部八个基准上均领先于开源基础模型（包括广泛使用的通用模型 Mistral 7B（Jiang et al., 2023），以及在 Proof-Pile-2（Azerbayev et al., 2023）上经过数学训练的近期发布的 Llemma 34B（Azerbayev et al., 2023））。值得注意的是，在竞赛级 MATH 数据集上，DeepSeekMath-Base 以超过 10% 的绝对优势超越现有开源基础模型，并胜过 Minerva 540B（Lewkowycz et al., 2022a）——一个比它大 77 倍的闭源基础模型，该模型基于 PaLM（Lewkowycz et al., 2022b）并在数学文本上进一步训练。

| 模型 | 规模 | GSM8K | MATH | OCW | SAT | MMLU-STEM | CMATH | Gaokao-MathCloze | Gaokao-MathQA |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 闭源基础模型 | | | | | | | | | |
| Minerva | 7B | 16.2% | 14.1% | 7.7% | - | 35.6% | - | - | - |
| Minerva | 62B | 52.4% | 27.6% | 12.0% | - | 53.9% | - | - | - |
| Minerva | 540B | 58.8% | 33.6% | 17.6% | - | 63.9% | - | - | - |
| 开源基础模型 | | | | | | | | | |
| Mistral | 7B | 40.3% | 14.3% | 9.2% | 71.9% | 51.1% | 44.9% | 5.1% | 23.4% |
| Llemma | 7B | 37.4% | 18.1% | 6.3% | 59.4% | 43.1% | 43.4% | 11.9% | 23.6% |
| Llemma | 34B | 54.0% | 25.3% | 10.3% | 71.9% | 52.9% | 56.1% | 11.9% | 26.2% |
| DeepSeekMath-Base | 7B | 64.2% | 36.2% | 15.4% | 84.4% | 56.5% | 71.7% | 20.3% | 35.3% |

表 2：DeepSeekMath-Base 7B 与强大基础模型在英文与中文数学基准上的比较。模型采用思维链提示评测。Minerva 结果引自 Lewkowycz et al. (2022a)。

##### 使用工具求解数学问题

我们使用少样本程序思维提示（Chen et al., 2022；Gao et al., 2023）评估 GSM8K 与 MATH 上的程序辅助数学推理。模型被提示通过编写 Python 程序求解每道题，程序中可使用 math、sympy 等库进行复杂计算。程序的执行结果作为答案被评估。如表 3 所示，DeepSeekMath-Base 7B 胜过此前最先进的 Llemma 34B。

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| 模型 | 规模 | 工具辅助解题 | | 非正式到形式化证明 | |
| | | GSM8K+Python | MATH+Python | miniF2F-valid | miniF2F-test |
| Mistral | 7B | 48.5% | 18.2% | 18.9% | 18.0% |
| CodeLlama | 7B | 27.1% | 17.2% | 16.3% | 17.6% |
| CodeLlama | 34B | 52.7% | 23.5% | 18.5% | 18.0% |
| Llemma | 7B | 41.0% | 18.6% | 20.6% | 22.1% |
| Llemma | 34B | 64.6% | 26.3% | 21.0% | 21.3% |
| DeepSeekMath-Base | 7B | 66.9% | 31.4% | 25.8% | 24.6% |

表 3：基础模型使用工具求解数学问题能力与在 Isabelle 中进行非正式到形式化定理证明能力的少样本评估。

##### 形式数学

形式化证明自动化有助于确保数学证明的准确性与可靠性并提升效率，近年来受到越来越多关注。我们在 Jiang et al. (2022) 的非正式到形式化证明任务上评估 DeepSeekMath-Base 7B：给定一个非正式陈述、该陈述的形式化对应物以及一个非正式证明，生成形式化证明。我们在 miniF2F（Zheng et al., 2021）——一个形式化奥赛级数学基准——上评估，并以少样本提示为每道题生成 Isabelle 形式化证明。遵循 Jiang et al. (2022)，我们让模型生成证明草图，然后执行现成的自动证明器 Sledgehammer（Paulson, 2010）来补全缺失细节。如表 3 所示，DeepSeekMath-Base 7B 在证明自动形式化上表现出色。

|  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- |
| 模型 | 规模 | MMLU | BBH | HumanEval (Pass@1) | MBPP (Pass@1) |
| Mistral | 7B | 62.4% | 55.7% | 28.0% | 41.4% |
| DeepSeek-Coder-Base-v1.5† | 7B | 42.9% | 42.9% | 40.2% | 52.6% |
| DeepSeek-Coder-Base-v1.5 | 7B | 49.1% | 55.2% | 43.2% | 60.4% |
| DeepSeekMath-Base | 7B | 54.9% | 59.5% | 40.9% | 52.6% |

表 4：在自然语言理解、推理与代码基准上的评估。DeepSeek-Coder-Base-v1.5† 是学习率衰减前、用于训练 DeepSeekMath-Base 的检查点。在 MMLU 与 BBH 上，我们使用少样本思维链提示。在 HumanEval 与 MBPP 上，我们分别在零样本与少样本设定下评估模型性能。

##### 自然语言理解、推理与代码

我们在 MMLU（Hendrycks et al., 2020）上评估自然语言理解性能，在 BBH（Suzgun et al., 2022）上评估推理性能，在 HumanEval（Chen et al., 2021）与 MBPP（Austin et al., 2021）上评估编程能力。如表 4 所示，DeepSeekMath-Base 7B 相较其前身 DeepSeek-Coder-Base-v1.5（Guo et al., 2024）在 MMLU 与 BBH 上表现出显著提升，说明数学训练对语言理解与推理的积极影响。此外，通过在持续训练中加入代码 token，DeepSeekMath-Base 7B 有效保持了 DeepSeek-Coder-Base-v1.5 在两个编程基准上的性能。总体而言，DeepSeekMath-Base 7B 在三个推理与编程基准上显著超越通用模型 Mistral 7B（Jiang et al., 2023）。

## 3 监督微调

### 3.1 SFT 数据构建

我们构建了一个覆盖中英文问题、跨越不同数学领域与复杂度层次的数学指令微调数据集：问题配有思维链（CoT）（Wei et al., 2022）、程序思维（PoT）（Chen et al., 2022；Gao et al., 2023）以及工具集成推理格式（Gou et al., 2023）的解答。训练样本总数为 776K。

- 英文数学数据集：我们为 GSM8K 与 MATH 问题标注工具集成解答，并采用 MathInstruct（Yue et al., 2023）的一个子集以及 Lila-OOD（Mishra et al., 2022）的训练集，其中问题以 CoT 或 PoT 求解。我们的英文合集覆盖多样的数学领域，如代数、概率、数论、微积分与几何。
- 中文数学数据集：我们收集了覆盖 76 个子话题（如线性方程）的中文 K-12 数学问题，解答以 CoT 与工具集成推理两种格式标注。

### 3.2 训练与评估 DeepSeekMath-Instruct 7B

在本节中，我们介绍基于 DeepSeekMath-Base 进行数学指令微调的 DeepSeekMath-Instruct 7B。训练样本被随机拼接，直至达到 4K token 的最大上下文长度。我们以 256 的批次大小、5e-5 的恒定学习率训练模型 500 步。

我们在中英文 4 个定量推理基准上评估模型不使用与使用工具的数学性能。我们将模型与当时的领先模型进行对比：

- 闭源模型包括：(1) GPT 家族，其中 GPT-4（OpenAI, 2023）与 GPT-4 Code Interpreter（<https://openai.com/blog/chatgpt-plugins##code-interpreter>）能力最强；(2) Gemini Ultra 与 Pro（Anil et al., 2023）；(3) Inflection-2（Inflection AI, 2023）；(4) Grok-1（<https://x.ai/model-card>），以及中国公司近期发布的模型，包括 (5) Baichuan-3（<https://www.baichuan-ai.com>）；(6) GLM 家族（Du et al., 2022）最新的 GLM-4（<https://open.bigmodel.cn/dev/api#glm-4>）。这些模型为通用目的，其中大多数经过一系列对齐流程。
- 开源模型包括：通用模型，如 (1) DeepSeek-LLM-Chat 67B（DeepSeek-AI, 2024）、(2) Qwen 72B（Bai et al., 2023）、(3) SeaLLM-v2 7B（Nguyen et al., 2023）与 (4) ChatGLM3 6B（ChatGLM3 Team, 2023）；以及在数学上增强的模型，包括 (5) InternLM2-Math 20B（<https://github.com/InternLM/InternLM-Math>），它基于 InternLM2，经过数学训练后再进行指令微调；(6) Math-Shepherd-Mistral 7B，它用过程监督奖励模型对 Mistral 7B（Jiang et al., 2023）进行 PPO 训练（Schulman et al., 2017）；(7) WizardMath 系列（Luo et al., 2023），它使用 evolve-instruct（即使用 AI 演化指令的指令微调版本）与 PPO 训练提升 Mistral 7B 与 Llama-2 70B（Touvron et al., 2023）的数学推理，训练题目主要来自 GSM8K 与 MATH；(8) MetaMath 70B（Yu et al., 2023），是在 GSM8K 与 MATH 增强版上微调的 Llama-2 70B；(9) ToRA 34B（Gou et al., 2023），是微调为进行工具集成数学推理的 CodeLlama 34B；(10) MAmmoTH 70B（Yue et al., 2023），是在 MathInstruct 上指令微调的 Llama-2 70B。

| 模型 | 规模 | GSM8K | MATH | MGSM-zh | CMATH |
| --- | --- | --- | --- | --- | --- |
| **思维链推理** | | | | | |
| 闭源模型 | | | | | |
| Gemini Ultra | - | 94.4% | 53.2% | - | - |
| GPT-4 | - | 92.0% | 52.9% | - | 86.0% |
| Inflection-2 | - | 81.4% | 34.8% | - | - |
| GPT-3.5 | - | 80.8% | 34.1% | - | 73.8% |
| Gemini Pro | - | 86.5% | 32.6% | - | - |
| Grok-1 | - | 62.9% | 23.9% | - | - |
| Baichuan-3 | - | 88.2% | 49.2% | - | - |
| GLM-4 | - | 87.6% | 47.9% | - | - |
| 开源模型 | | | | | |
| InternLM2-Math | 20B | 82.6% | 37.7% | - | - |
| Qwen | 72B | 78.9% | 35.2% | - | - |
| Math-Shepherd-Mistral | 7B | 84.1% | 33.0% | - | - |
| WizardMath-v1.1 | 7B | 83.2% | 33.0% | - | - |
| DeepSeek-LLM-Chat | 67B | 84.1% | 32.6% | 74.0% | 80.3% |
| MetaMath | 70B | 82.3% | 26.6% | 66.4% | 70.9% |
| SeaLLM-v2 | 7B | 78.2% | 27.5% | 64.8% | - |
| ChatGLM3 | 6B | 72.3% | 25.7% | - | - |
| WizardMath-v1.0 | 70B | 81.6% | 22.7% | 64.8% | 65.4% |
| DeepSeekMath-Instruct | 7B | 82.9% | 46.8% | 73.2% | 84.6% |
| DeepSeekMath-RL | 7B | 88.2% | 51.7% | 79.6% | 88.8% |
| **工具集成推理** | | | | | |
| 闭源模型 | | | | | |
| GPT-4 Code Interpreter | - | 97.0% | 69.7% | - | - |
| 开源模型 | | | | | |
| InternLM2-Math | 20B | 80.7% | 54.3% | - | - |
| DeepSeek-LLM-Chat | 67B | 86.7% | 51.1% | 76.4% | 85.4% |
| ToRA | 34B | 80.7% | 50.8% | 41.2% | 53.4% |
| MAmmoTH | 70B | 76.9% | 41.8% | - | - |
| DeepSeekMath-Instruct | 7B | 83.7% | 57.4% | 72.0% | 84.3% |
| DeepSeekMath-RL | 7B | 86.7% | 58.8% | 78.4% | 87.6% |

表 5：开源与闭源模型在英文与中文基准上采用思维链与工具集成推理两种方式的性能。灰色分数表示 32 个候选中的多数投票；其余为 Top1 分数。DeepSeekMath-RL 7B 胜过从 7B 到 70B 的所有开源模型以及多数闭源模型。尽管 DeepSeekMath-RL 7B 仅在 GSM8K 与 MATH 的思维链格式指令微调数据上进一步训练，它在所有基准上都比 DeepSeekMath-Instruct 7B 有所提升。

如表 5 所示，在不允许使用工具的评测设定下，DeepSeekMath-Instruct 7B 展现出强大的逐步推理性能。值得注意的是，在竞赛级 MATH 数据集上，我们的模型以至少 9% 的绝对优势超越所有开源模型与多数专有模型（如 Inflection-2 与 Gemini Pro）。即使面对规模大得多的模型（如 Qwen 72B）或经过数学专项强化学习增强的模型（如 WizardMath-v1.1 7B），也是如此。虽然 DeepSeekMath-Instruct 在 MATH 上与中国专有模型 GLM-4 和 Baichuan-3 相当，但仍逊于 GPT-4 与 Gemini Ultra。

在允许模型结合自然语言推理与基于程序的工具使用来解题的评测设定下，DeepSeekMath-Instruct 7B 在 MATH 上接近 60% 的准确率，超越所有现有开源模型。在其他基准上，我们的模型与此前最先进、规模大 10 倍的 DeepSeek-LLM-Chat 67B 具有竞争力。

## 4 强化学习

### 4.1 组相对策略优化

强化学习（RL）已被证明能在监督微调（SFT）阶段之后进一步提升 LLM 的数学推理能力（Wang et al., 2023b；Luo et al., 2023）。在本节中，我们介绍我们高效且有效的 RL 算法——组相对策略优化（GRPO）。

#### 4.1.1 从 PPO 到 GRPO

近端策略优化（PPO）（Schulman et al., 2017）是一种 actor-critic RL 算法，广泛应用于 LLM 的 RL 微调阶段（Ouyang et al., 2022）。特别地，它通过最大化以下代理目标来优化 LLM：

$$
\mathcal{J}_{PPO}(\theta)=\mathbb{E}{[q\sim P(Q),o\sim\pi_{\theta_{old}}(O|q)]}\frac{1}{|o|}\sum_{t=1}^{|o|}\min\left[\frac{\pi_{\theta}(o_{t}|q,o_{<t})}{\pi_{\theta_{old}}(o_{t}|q,o_{<t})}A_{t},\text{clip}\left(\frac{\pi_{\theta}(o_{t}|q,o_{<t})}{\pi_{\theta_{old}}(o_{t}|q,o_{<t})},1-\varepsilon,1+\varepsilon\right)A_{t}\right], \tag{1}
$$

其中 $\pi_{\theta}$ 与 $\pi_{\theta_{old}}$ 分别是当前与旧的策略模型，$q,o$ 分别是从问题数据集与旧策略 $\pi_{\theta_{old}}$ 中采样的问题与输出。$\varepsilon$ 是 PPO 中为稳定训练而引入的与裁剪相关的超参数。$A_{t}$ 是优势，基于奖励 $\{r_{\geq t}\}$ 与一个学习到的价值函数 $V_{\psi}$，通过应用广义优势估计（GAE）（Schulman et al., 2015）计算。因此，在 PPO 中，价值函数需要与策略模型一同训练，并且为缓解奖励模型的过度优化，标准做法是在每个 token 的奖励中加入来自参考模型的逐 token KL 惩罚（Ouyang et al., 2022），即

$$
r_{t}=r_{\varphi}(q,o_{\leq t})-\beta\log\frac{\pi_{\theta}(o_{t}|q,o_{<t})}{\pi_{ref}(o_{t}|q,o_{<t})}, \tag{2}
$$

其中 $r_{\varphi}$ 是奖励模型，$\pi_{ref}$ 是参考模型（通常是初始 SFT 模型），$\beta$ 是 KL 惩罚的系数。

图 4：PPO 与我们的 GRPO 示意图。GRPO 舍弃价值模型，转而从组分数估计基线，显著降低训练资源。

由于 PPO 中使用的价值函数通常是另一个与策略模型规模相当的模型，它带来了可观的显存与计算负担。此外，在 RL 训练中，价值函数在优势计算中被用作基线以降低方差。而在 LLM 场景下，通常只有最后一个 token 会被奖励模型赋予奖励分数，这可能使训练一个在每个 token 上都准确的价值函数变得复杂。为解决这一问题，如图 4 所示，我们提出组相对策略优化（GRPO），它免除了 PPO 中额外的价值函数近似，转而使用针对同一问题采样的多个输出的平均奖励作为基线。更具体地说，对每个问题 $q$，GRPO 从旧策略 $\pi_{\theta_{old}}$ 采样一组输出 $\{o_{1},o_{2},\cdots,o_{G}\}$，然后通过最大化以下目标来优化策略模型：

$$
\begin{split}\mathcal{J}_{GRPO}(\theta)&=\mathbb{E}{[q\sim P(Q),\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta_{old}}(O|q)]}\\ &\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|o_{i}|}\sum_{t=1}^{|o_{i}|}\left\{\min\left[\frac{\pi_{\theta}(o_{i,t}|q,o_{i,<t})}{\pi_{\theta_{old}}(o_{i,t}|q,o_{i,<t})}\hat{A}_{i,t},\text{clip}\left(\frac{\pi_{\theta}(o_{i,t}|q,o_{i,<t})}{\pi_{\theta_{old}}(o_{i,t}|q,o_{i,<t})},1-\varepsilon,1+\varepsilon\right)\hat{A}_{i,t}\right]-\beta\mathbb{D}_{KL}\left[\pi_{\theta}\Vert\pi_{ref}\right]\right\},\end{split} \tag{3}
$$

其中 $\varepsilon$ 与 $\beta$ 是超参数，$\hat{A}_{i,t}$ 是仅基于每组内部各输出的相对奖励计算的优势，将在后续小节详述。GRPO 计算优势所用的组相对方式，与奖励模型的比较式本质高度契合，因为奖励模型通常在「同一问题上输出之间的比较」数据集上训练。另需注意，GRPO 不是把 KL 惩罚加到奖励中，而是通过把训练策略与参考策略之间的 KL 散度直接加到损失中进行正则化，避免使 $\hat{A}_{i,t}$ 的计算复杂化。并且与式 (2) 中使用的 KL 惩罚项不同，我们用以下无偏估计量（Schulman, 2020）估计 KL 散度：

$$
\mathbb{D}_{KL}\left[\pi_{\theta}\Vert\pi_{ref}\right]=\frac{\pi_{ref}(o_{i,t}|q,o_{i,<t})}{\pi_{\theta}(o_{i,t}|q,o_{i,<t})}-\log\frac{\pi_{ref}(o_{i,t}|q,o_{i,<t})}{\pi_{\theta}(o_{i,t}|q,o_{i,<t})}-1, \tag{4}
$$

它保证为正。

算法 1　迭代式组相对策略优化

输入 初始策略模型 $\pi_{\theta_{\text{init}}}$；奖励模型 $r_{\varphi}$；任务提示 $\mathcal{D}$；超参数 $\varepsilon$、$\beta$、$\mu$

1: 策略模型 $\pi_{\theta}\leftarrow\pi_{\theta_{\text{init}}}$
2: for iteration = 1, …, I do
3: 　参考模型 $\pi_{ref}\leftarrow\pi_{\theta}$
4: 　for step = 1, …, M do
5: 　　从 $\mathcal{D}$ 中采样一个批次 $\mathcal{D}_{b}$
6: 　　更新旧策略模型 $\pi_{\theta_{old}}\leftarrow\pi_{\theta}$
7: 　　为每个问题 $q\in\mathcal{D}_{b}$ 采样 $G$ 条输出 $\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta_{old}}(\cdot\mid q)$
8: 　　运行 $r_{\varphi}$ 为每条采样输出 $o_{i}$ 计算奖励 $\{r_{i}\}_{i=1}^{G}$
9: 　　通过组相对优势估计为 $o_{i}$ 的第 $t$ 个 token 计算 $\hat{A}_{i,t}$
10: 　　for GRPO iteration = 1, …, $\mu$ do
11: 　　　通过最大化 GRPO 目标（式 (21)）更新策略模型 $\pi_{\theta}$
12: 　通过结合回放机制的持续训练更新 $r_{\varphi}$

输出 $\pi_{\theta}$

#### 4.1.2 GRPO 的结果监督 RL

形式上，对每个问题 $q$，从旧策略模型 $\pi_{\theta_{old}}$ 采样一组输出 $\{o_{1},o_{2},\cdots,o_{G}\}$。随后用奖励模型为这些输出打分，得到相应的 $G$ 个奖励 $\mathbf{r}=\{r_{1},r_{2},\cdots,r_{G}\}$。接着，这些奖励通过减去组平均值并除以组标准差进行归一化。结果监督在每个输出 $o_{i}$ 的末尾提供归一化奖励，并将输出中所有 token 的优势设为该归一化奖励，即 $\hat{A}_{i,t}=\widetilde{r}_{i}=\frac{r_{i}-{\rm mean}(\mathbf{r})}{{\rm std}(\mathbf{r})}$，然后通过最大化式 (3) 中定义的目标来优化策略。

#### 4.1.3 GRPO 的过程监督 RL

结果监督只在每个输出末尾提供奖励，在复杂数学任务中可能不足以高效地监督策略。遵循 Wang et al. (2023b)，我们还探索过程监督，它在每个推理步骤末尾提供奖励。形式上，给定问题 $q$ 与 $G$ 条采样输出 $\{o_{1},o_{2},\cdots,o_{G}\}$，用过程奖励模型为输出的每一步打分，得到相应奖励：$\mathbf{R}=\{\{r_{1}^{index(1)},\cdots,r_{1}^{index(K_{1})}\},\cdots,\{r_{G}^{index(1)},\cdots,r_{G}^{index(K_{G})}\}\}$，其中 $index(j)$ 是第 $j$ 步末 token 的索引，$K_{i}$ 是第 $i$ 条输出的总步数。我们同样用平均值与标准差对这些奖励归一化，即 $\widetilde{r}_{i}^{index(j)}=\frac{r_{i}^{index(j)}-{\rm mean(\mathbf{R})}}{{\rm std(\mathbf{R})}}$。随后，过程监督将每个 token 的优势计算为后续各步归一化奖励之和，即 $\hat{A}_{i,t}=\sum_{index(j)\geq t}\widetilde{r}_{i}^{index(j)}$，然后通过最大化式 (3) 中定义的目标来优化策略。

#### 4.1.4 GRPO 的迭代 RL

随着强化学习训练过程的推进，旧的奖励模型可能不足以监督当前的策略模型。因此，我们还探索带 GRPO 的迭代式 RL。如算法 1 所示，在迭代式 GRPO 中，我们基于策略模型的采样结果为奖励模型生成新训练集，并使用包含 10% 历史数据的回放机制持续训练旧奖励模型。然后，我们将参考模型设为策略模型，并用新奖励模型持续训练策略模型。

### 4.2 训练与评估 DeepSeekMath-RL

我们基于 DeepSeekMath-Instruct 7B 进行 RL。RL 的训练数据是 SFT 数据中与 GSM8K 和 MATH 相关的思维链格式问题，共约 144K 道题。我们排除其他 SFT 问题，以考察 RL 对整个 RL 阶段缺少数据的基准的影响。我们遵循 Wang et al. (2023b) 构建奖励模型的训练集。我们基于 DeepSeekMath-Base 7B、以 2e-5 的学习率训练初始奖励模型。对于 GRPO，我们将策略模型的学习率设为 1e-6，KL 系数为 0.04。对每个问题，我们采样 64 条输出。最大长度设为 1024，训练批次大小为 1024。每个探索阶段之后，策略模型只做单次更新。我们按照 DeepSeekMath-Instruct 7B 的方式在基准上评估 DeepSeekMath-RL 7B。对 DeepSeekMath-RL 7B 而言，采用思维链推理的 GSM8K 与 MATH 可视为域内任务，其余基准均可视为域外任务。

表 5 展示了开源与闭源模型在英文与中文基准上采用思维链与工具集成推理的性能。我们发现：
1) DeepSeekMath-RL 7B 使用思维链推理，在 GSM8K 与 MATH 上分别取得 88.2% 与 51.7% 的准确率。这一性能超越了 7B 到 70B 范围内的所有开源模型以及多数闭源模型。
2) 关键的是，DeepSeekMath-RL 7B 从 DeepSeekMath-Instruct 7B 出发，仅在 GSM8K 与 MATH 的思维链格式指令微调数据上训练。尽管训练数据范围受限，它在所有评测指标上都胜过 DeepSeekMath-Instruct 7B，展示了强化学习的有效性。

## 5 讨论

在本节中，我们将分享预训练与 RL 实验中的发现。

### 5.1 预训练中的经验教训

我们首先分享预训练方面的经验。除非另有说明，我们将遵循第 2.2.1 节中概述的训练设定。值得注意的是，本节提及 DeepSeekMath 语料库时，我们使用的是数据收集过程第二轮迭代得到的 89B token 数据集。

#### 5.1.1 代码训练有益于数学推理

一个流行但未经验证的假设认为，代码训练能提升推理。我们尝试对此给出部分回答，尤其是在数学领域：代码训练能提升模型在有工具与无工具两种条件下进行数学推理的能力。

为研究代码训练如何影响数学推理，我们实验了以下两阶段训练与一阶段训练设定：

两阶段训练

- 代码训练 400B token → 数学训练 150B token：我们先在 400B 代码 token 上训练 DeepSeek-LLM 1.3B，再在 150B 数学 token 上训练；
- 通用训练 400B token → 数学训练 150B token：作为对照实验，第一阶段改用通用 token（采样自 DeepSeek-AI 构建的大规模通用语料库）而非代码 token，以考察代码 token 相对通用 token 在提升数学推理上的优势。

一阶段训练

- 数学训练 150B token：我们在 150B 数学 token 上训练 DeepSeek-LLM 1.3B；
- 在 400B 代码 token 与 150B 数学 token 的混合数据上训练：数学训练接在代码训练之后会损害编程性能。我们考察将代码 token 与数学 token 混合用于一阶段训练，是否仍能提升数学推理并缓解灾难性遗忘问题。

| 训练设定 | 通用 | 代码 | 数学 | GSM8K | MATH | CMATH | GSM8K+Python | MATH+Python |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 无持续训练 | – | – | – | 2.9% | 3.0% | 12.3% | 2.7% | 2.3% |
| 两阶段训练 | | | | | | | | |
| 阶段 1：通用训练 | 400B | – | – | 2.9% | 3.2% | 14.8% | 3.3% | 2.3% |
| 阶段 2：数学训练 | – | – | 150B | 19.1% | 14.4% | 37.2% | 14.3% | 6.7% |
| 阶段 1：代码训练 | – | 400B | – | 5.9% | 3.6% | 19.9% | 12.4% | 10.0% |
| 阶段 2：数学训练 | – | – | 150B | 21.9% | 15.3% | 39.7% | 17.4% | 9.4% |
| 一阶段训练 | | | | | | | | |
| 数学训练 | – | – | 150B | 20.5% | 13.1% | 37.6% | 11.4% | 6.5% |
| 代码与数学混合训练 | – | 400B | 150B | 17.6% | 12.1% | 36.3% | 19.7% | 13.5% |

表 6：不同训练设定下代码如何影响数学推理的研究。我们使用 DeepSeek-LLM 1.3B 实验，分别通过少样本思维链提示与少样本程序思维提示评估其无工具与有工具的数学推理性能。

| 训练设定 | 通用 | 代码 | 数学 | MMLU | BBH | HumanEval (Pass@1) | MBPP (Pass@1) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 无持续训练 | – | – | – | 24.5% | 28.1% | 12.2% | 13.0% |
| 两阶段训练 | | | | | | | |
| 阶段 1：通用训练 | 400B | – | – | 25.9% | 27.7% | 15.2% | 13.6% |
| 阶段 2：数学训练 | – | – | 150B | 33.1% | 32.7% | 12.8% | 13.2% |
| 阶段 1：代码训练 | – | 400B | – | 25.0% | 31.5% | 25.0% | 40.0% |
| 阶段 2：数学训练 | – | – | 150B | 36.2% | 35.3% | 12.2% | 17.0% |
| 一阶段训练 | | | | | | | |
| 数学训练 | – | – | 150B | 32.3% | 32.5% | 11.6% | 13.2% |
| 代码与数学混合训练 | – | 400B | 150B | 33.5% | 35.6% | 29.3% | 39.4% |

表 7：代码与数学训练的不同设定如何影响模型语言理解、推理与编程性能的研究。我们使用 DeepSeek-LLM 1.3B 实验。我们在 MMLU 与 BBH 上使用少样本思维链提示评估模型。在 HumanEval 与 MBPP 上，我们分别进行零样本与少样本评估。

##### 结果

表 6 与表 7 展示了不同训练设定下的下游性能。

代码训练有益于程序辅助数学推理，在两阶段与一阶段训练设定下均如此。如表 6 所示，在两阶段训练设定下，仅代码训练就已显著提升使用 Python 求解 GSM8K 与 MATH 问题的能力，第二阶段的数学训练带来进一步提升。有趣的是，在一阶段训练设定下，混合代码 token 与数学 token 有效缓解了两阶段训练带来的灾难性遗忘问题，并使编程（表 7）与程序辅助数学推理（表 6）形成协同。

代码训练同样提升了无工具的数学推理。在两阶段训练设定下，初始的代码训练阶段已带来中等程度的提升，它还提高了后续数学训练的效率，最终带来最佳性能。然而，将代码 token 与数学 token 结合一阶段训练会损害无工具的数学推理。一种猜测是，DeepSeek-LLM 1.3B 由于规模有限，缺乏同时充分吸收代码与数学数据的能力。

| 模型 | 规模 | ArXiv 语料 | GSM8K | MATH | OCW | SAT | MMLU-STEM | CMATH | Gaokao-MathCloze | Gaokao-MathQA |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DeepSeek-LLM | 1.3B | 无数学训练 | 2.9% | 3.0% | 2.9% | 15.6% | 19.5% | 12.3% | 0.8% | 17.9% |
| | | MathPile | 2.7% | 3.3% | 2.2% | 12.5% | 15.7% | 1.2% | 0.0% | 2.8% |
| | | ArXiv-RedPajama | 3.3% | 3.4% | 4.0% | 9.4% | 9.0% | 7.4% | 0.8% | 2.3% |
| DeepSeek-Coder-Base-v1.5 | 7B | 无数学训练 | 29.0% | 12.5% | 6.6% | 40.6% | 38.1% | 45.9% | 5.9% | 21.1% |
| | | MathPile | 23.6% | 11.5% | 7.0% | 46.9% | 35.8% | 37.9% | 4.2% | 25.6% |
| | | ArXiv-RedPajama | 28.1% | 11.1% | 7.7% | 50.0% | 35.2% | 42.6% | 7.6% | 24.8% |

表 8：不同 arXiv 数据集上数学训练的效果。模型性能采用少样本思维链提示评估。

|  |  |  |
| --- | --- | --- |
| ArXiv 语料 | miniF2F-valid | miniF2F-test |
| 无数学训练 | 20.1% | 21.7% |
| MathPile | 16.8% | 16.4% |
| ArXiv-RedPajama | 14.8% | 11.9% |

表 9：不同 arXiv 语料上数学训练的效果，基础模型为 DeepSeek-Coder-Base-v1.5 7B。我们评估 Isabelle 中的非正式到形式化证明。

#### 5.1.2 arXiv 论文似乎无助于提升数学推理

arXiv 论文通常被纳入数学预训练数据的一个组成部分（Lewkowycz et al., 2022a；Polu and Sutskever, 2020；Azerbayev et al., 2023；Wang et al., 2023c）。然而，关于其对数学推理影响的详细分析尚未被广泛开展。或许与直觉相反，根据我们的实验，arXiv 论文似乎无助于提升数学推理。我们使用经过不同处理流水线的 arXiv 语料库，在不同规模的模型上实验，包括 DeepSeek-LLM 1.3B 与 DeepSeek-Coder-Base-v1.5 7B（Guo et al., 2024）：

- MathPile（Wang et al., 2023c）：一个 8.9B token 的语料库，采用清洗与过滤的启发式规则开发，其中超过 85% 为 arXiv 科学论文；
- ArXiv-RedPajama（Computer, 2023）：完整的 arXiv LaTeX 文件，移除了导言区、注释、宏与参考文献，共计 28.0B token。

在实验中，我们在每个 arXiv 语料库上分别训练 DeepSeek-LLM 1.3B 150B token、DeepSeek-Coder-Base-v1.5 7B 40B token。arXiv 论文似乎确实无助于提升数学推理。在仅含 arXiv 的语料库上训练时，两个模型在本研究所用不同复杂度的各类数学基准上均未显示出显著改进，甚至出现退化。这些基准包括定量推理数据集如 GSM8K 与 MATH（表 8）、多项选择挑战如 MMLU-STEM（表 8），以及形式数学如 miniF2F（表 9）。

然而，这一结论存在局限，应当有所保留地看待。我们尚未研究：

- arXiv token 对本研究未涵盖的特定数学相关任务的影响，例如定理的非形式化（将形式化陈述或证明转换为其非正式版本）；
- arXiv token 与其他类型数据结合使用时的效果；
- arXiv 论文的益处是否会在更大的模型规模上显现。

因此，还需要进一步探索，我们将其留作未来研究。

### 5.2 强化学习的洞见

#### 5.2.1 迈向统一范式

在本节中，我们提供一个统一范式来分析不同训练方法，如 SFT、RFT、DPO、PPO、GRPO，并进一步开展实验探索该统一范式的影响因素。一般而言，一个训练方法关于参数 $\theta$ 的梯度可以写成：

$$
\nabla_{\theta}\mathcal{J}_{\mathcal{A}}(\theta)=\mathbb{E}[\underbrace{(q,o)\sim\mathcal{D}}_{\text{数据来源}}]\left(\frac{1}{|o|}\sum_{t=1}^{|o|}\underbrace{GC_{\mathcal{A}}(q,o,t,\pi_{rf})}_{\text{梯度系数}}\nabla_{\theta}\log\pi_{\theta}(o_{t}|q,o_{<t})\right). \tag{5}
$$

其中存在三个关键组成部分：
1) 数据来源 $\mathcal{D}$，决定训练数据；
2) 奖励函数 $\pi_{rf}$，是训练奖励信号的来源；
3) 算法 $\mathcal{A}$：它把训练数据与奖励信号处理为梯度系数 $GC$，后者决定对数据的惩罚或强化幅度。我们基于这一统一范式分析若干代表性方法：

|  |  |  |  |
| --- | --- | --- | --- |
| 方法 | 数据来源 | 奖励函数 | 梯度系数 |
| SFT | $q,o\sim P_{sft}(Q,O)$ | - | 1 |
| RFT | $q\sim P_{sft}(Q)$, $o\sim\pi_{sft}(O\mid q)$ | 规则 | 式 (10) |
| DPO | $q\sim P_{sft}(Q)$, $o^{+},o^{-}\sim\pi_{sft}(O\mid q)$ | 规则 | 式 (14) |
| Online RFT | $q\sim P_{sft}(Q)$, $o\sim\pi_{\theta}(O\mid q)$ | 规则 | 式 (10) |
| PPO | $q\sim P_{sft}(Q)$, $o\sim\pi_{\theta}(O\mid q)$ | 模型 | 式 (18) |
| GRPO | $q\sim P_{sft}(Q)$, $\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta}(O\mid q)$ | 模型 | 式 (21) |

表 10：不同方法的数据来源与梯度系数。$P_{sft}$ 表示监督微调数据集的数据分布。$\pi_{\theta_{sft}}$ 与 $\pi_{\theta}$ 分别表示监督微调模型与在线训练过程中的实时策略模型。

- 监督微调（SFT）：SFT 在人工挑选的 SFT 数据上微调预训练模型。
- 拒绝采样微调（RFT）：RFT 在基于 SFT 问题从 SFT 模型采样的、经过筛选的输出上进一步微调 SFT 模型。RFT 根据答案的正确性筛选输出。
- 直接偏好优化（DPO）：DPO 通过在从 SFT 模型采样的增强输出上、使用成对 DPO 损失微调，进一步精炼 SFT 模型。
- 在线拒绝采样微调（Online RFT）：与 RFT 不同，Online RFT 用 SFT 模型初始化策略模型，并通过在从实时策略模型采样的增强输出上微调来精炼它。
- PPO/GRPO：PPO/GRPO 用 SFT 模型初始化策略模型，并用从实时策略模型采样的输出对其进行强化。

我们在表 10 中总结了这些方法的组成部分。更详细的推导过程请参见附录 A.1。

图 5：DeepSeekMath-Instruct 1.3B 模型经不同方法进一步训练后在两个基准上的性能。

图 6：DeepSeekMath-Instruct 7B 进行迭代式强化学习在两个基准上的性能。

##### 关于数据来源的观察

我们将数据来源分为两类：在线采样与离线采样。在线采样指训练数据来自实时训练的策略模型的探索结果，而离线采样指训练数据来自初始 SFT 模型的采样结果。RFT 与 DPO 采用离线风格，而 Online RFT 与 GRPO 采用在线风格。

如图 5 所示，我们发现 Online RFT 在两个基准上显著优于 RFT。具体而言，Online RFT 在训练早期与 RFT 相当，但在后期取得绝对优势，展示了在线训练的优越性。这很直观：在初始阶段，actor 与 SFT 模型高度相似，采样数据只揭示微小差异；而在后期，从 actor 采样的数据会呈现更显著的差异，实时数据采样将带来更大优势。

##### 关于梯度系数的观察

算法将奖励信号处理为梯度系数以更新模型参数。在实验中，我们把奖励函数分为「规则」与「模型」两类。规则指根据答案正确性判断回答质量，模型指我们训练一个奖励模型为每个回答打分。奖励模型的训练数据基于规则判断。式 (10) 与式 (21) 突出了 GRPO 与 Online RFT 之间的一个关键区别：GRPO 独特地根据奖励模型提供的奖励值调整其梯度系数，这允许根据回答的不同量级进行差异化强化与惩罚。相比之下，Online RFT 缺少这一特性：它不惩罚错误回答，并以相同的强化强度统一强化所有答案正确的回答。

如图 5 所示，GRPO 超越了 Online RFT，凸显了改变正负梯度系数的效率。此外，GRPO+PS 的性能优于 GRPO+OS，表明使用细粒度、步骤感知的梯度系数有好处。进一步地，我们探索了迭代式 RL，在实验中进行了两轮迭代。如图 6 所示，我们注意到迭代式 RL 显著提升了性能，尤其是在第一轮迭代。

图 7：SFT 与 RL 后的 DeepSeekMath 7B 在 GSM8K 与 MATH 上的 Maj@K 与 Pass@K（temperature 0.7）。可以看到 RL 提升了 Maj@K 但未提升 Pass@K。

#### 5.2.2 RL 为何有效？

在本文中，我们基于一部分指令微调数据进行强化学习，它在指令微调模型之上取得了显著的性能提升。为进一步解释强化学习为何有效，我们在两个基准上评估 Instruct 与 RL 模型的 Pass@K 与 Maj@K 准确率。如图 7 所示，RL 提升了 Maj@K 的性能但未提升 Pass@K。这些发现表明，RL 通过使输出分布更稳健来提升模型的整体表现，换句话说，改进似乎归因于从 TopK 中提升正确回答的概率，而非基本能力的增强。类似地，Wang et al. (2023a) 发现 SFT 模型在推理任务中存在错位问题，并表明可以通过一系列偏好对齐策略（Yuan et al., 2023b；Song et al., 2023；Wang et al., 2023a）提升 SFT 模型的推理性能。

#### 5.2.3 如何实现更有效的 RL？

我们证明了 RL 在数学推理任务中表现相当出色。我们还提供了一个统一范式来理解不同的代表性训练方法。在该范式下，所有方法都被概念化为直接的或简化版的 RL 技术。如式 (5) 所总结，存在三个关键组成部分：数据来源、算法与奖励函数。我们围绕这三个组成部分提供一些潜在的 future 方向。

##### 数据来源

数据来源是所有训练方法的原材料。在 RL 语境下，我们特指数据来源为无标注问题以及从策略模型采样的输出。在本文中，我们只使用指令微调阶段的问题，并用朴素的 nucleus 采样采样输出。我们认为这是我们的 RL 流水线只提升 Maj@K 性能的一个潜在原因。未来，我们将把我们的 RL 流水线探索到分布外问题提示上，并结合先进的采样（解码）策略，如基于树搜索的方法（Yao et al., 2023）。此外，决定策略模型探索效率的高效推理技术（Xia et al., 2023；Leviathan et al., 2023；Kwon et al., 2023；Xia et al., 2024）也发挥着极其重要的作用。

##### 算法

算法将数据与奖励信号处理为梯度系数以更新模型参数。基于式 (5)，在某种程度上，现有方法都完全「信任」奖励函数的信号来提高或降低某个 token 的条件概率。然而，无法保证奖励信号总是可靠，尤其是在极其复杂的任务中。例如，即使是由训练有素的标注者精心标注的 PRM800K 数据集（Lightman et al., 2023），仍包含约 20% 的错误标注（<https://github.com/openai/prm800k/issues/12#issuecomment-1728491852>）。为此，我们将探索对噪声奖励信号稳健的强化学习算法。我们相信这类「弱到强」（WEAK-TO-STRONG）（Burns et al., 2023）对齐方法将给学习算法带来根本性变化。

##### 奖励函数

奖励函数是训练信号的来源。在 RL 中，奖励函数通常是神经奖励模型。我们认为奖励模型存在三个重要方向：
1) 如何增强奖励模型的泛化能力。奖励模型必须有效泛化以处理分布外问题与先进解码输出；否则，强化学习可能只是稳定 LLM 的分布，而无法提升其基本能力；
2) 如何反映奖励模型的不确定性。不确定性有可能成为弱奖励模型与弱到强学习算法之间的连接桥梁；
3) 如何高效构建高质量的过程奖励模型，为推理过程提供细粒度训练信号（Lightman et al., 2023；Wang et al., 2023b）。

## 6 结论、局限与未来工作

我们提出了 DeepSeekMath，它在竞赛级 MATH 基准上超越所有开源模型，并接近闭源模型的性能。DeepSeekMath 以 DeepSeek-Coder-v1.5 7B 初始化，经过 500B token 的持续训练，训练数据的重要组成部分是取自 Common Crawl 的 120B 数学 token。我们广泛的消融研究表明，网页为高质量数学数据提供了巨大潜力，而 arXiv 可能并不像我们预期的那样有益。我们提出组相对策略优化（GRPO），近端策略优化（PPO）的一个变体，它能在更少显存消耗下显著提升数学推理能力。实验结果表明，即使 DeepSeekMath-Instruct 7B 已在基准上取得高分，GRPO 仍然有效。我们还提供了一个统一范式来理解一系列方法，并总结了实现更有效强化学习的若干潜在方向。

尽管 DeepSeekMath 在定量推理基准上取得了瞩目分数，其在几何与定理证明方面的能力相对闭源模型仍较弱。例如，在我们的试运行中，模型无法处理与三角形和椭圆相关的问题，这可能表明预训练与微调中的数据选择偏差。此外，受模型规模限制，DeepSeekMath 在少样本能力上不如 GPT-4。GPT-4 能借助少样本输入提升性能，而 DeepSeekMath 在零样本与少样本评测中表现相近。未来，我们将进一步改进工程化的数据筛选流水线，以构建更高质量的预训练语料库。此外，我们将探索第 5.2.3 节中的潜在方向，以实现更有效的 LLM 强化学习。

## 参考文献

- Anil et al. (2023)

  R. Anil, S. Borgeaud, Y. Wu, J. Alayrac, J. Yu, R. Soricut, J. Schalkwyk, A. M. Dai, A. Hauth, K. Millican, D. Silver, S. Petrov, M. Johnson, I. Antonoglou, J. Schrittwieser, A. Glaese, J. Chen, E. Pitler, T. P. Lillicrap, A. Lazaridou, O. Firat, J. Molloy, M. Isard, P. R. Barham, T. Hennigan, B. Lee, F. Viola, M. Reynolds, Y. Xu, R. Doherty, E. Collins, C. Meyer, E. Rutherford, E. Moreira, K. Ayoub, M. Goel, G. Tucker, E. Piqueras, M. Krikun, I. Barr, N. Savinov, I. Danihelka, B. Roelofs, A. White, A. Andreassen, T. von Glehn, L. Yagati, M. Kazemi, L. Gonzalez, M. Khalman, J. Sygnowski, and et al.
  Gemini: A family of highly capable multimodal models.
  *CoRR*, abs/2312.11805, 2023.
  [10.48550/ARXIV.2312.11805](https://doi.org/10.48550/ARXIV.2312.11805).
  URL <https://doi.org/10.48550/arXiv.2312.11805>.
- Austin et al. (2021)

  J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. Le, et al.
  Program synthesis with large language models.
  *arXiv preprint arXiv:2108.07732*, 2021.
- Azerbayev et al. (2023)

  Z. Azerbayev, H. Schoelkopf, K. Paster, M. D. Santos, S. McAleer, A. Q. Jiang, J. Deng, S. Biderman, and S. Welleck.
  Llemma: An open language model for mathematics.
  *arXiv preprint arXiv:2310.10631*, 2023.
- Bai et al. (2023)

  J. Bai, S. Bai, Y. Chu, Z. Cui, K. Dang, X. Deng, Y. Fan, W. Ge, Y. Han, F. Huang, et al.
  Qwen technical report.
  *arXiv preprint arXiv:2309.16609*, 2023.
- Burns et al. (2023)

  C. Burns, P. Izmailov, J. H. Kirchner, B. Baker, L. Gao, L. Aschenbrenner, Y. Chen, A. Ecoffet, M. Joglekar, J. Leike, et al.
  Weak-to-strong generalization: Eliciting strong capabilities with weak supervision.
  *arXiv preprint arXiv:2312.09390*, 2023.
- ChatGLM3 Team (2023)

  ChatGLM3 Team.
  Chatglm3 series: Open bilingual chat llms, 2023.
  URL <https://github.com/THUDM/ChatGLM3>.
- Chen et al. (2021)

  M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray, R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin, B. Chan, S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser, M. Bavarian, C. Winter, P. Tillet, F. P. Such, D. Cummings, M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss, W. H. Guss, A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Balaji, S. Jain, W. Saunders, C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra, E. Morikawa, A. Radford, M. Knight, M. Brundage, M. Murati, K. Mayer, P. Welinder, B. McGrew, D. Amodei, S. McCandlish, I. Sutskever, and W. Zaremba.
  Evaluating large language models trained on code.
  *CoRR*, abs/2107.03374, 2021.
  URL <https://arxiv.org/abs/2107.03374>.
- Chen et al. (2022)

  W. Chen, X. Ma, X. Wang, and W. W. Cohen.
  Program of thoughts prompting: Disentangling computation from reasoning for numerical reasoning tasks.
  *CoRR*, abs/2211.12588, 2022.
  [10.48550/ARXIV.2211.12588](https://doi.org/10.48550/ARXIV.2211.12588).
  URL <https://doi.org/10.48550/arXiv.2211.12588>.
- Cobbe et al. (2021)

  K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al.
  Training verifiers to solve math word problems.
  *arXiv preprint arXiv:2110.14168*, 2021.
- Computer (2023)

  T. Computer.
  Redpajama: an open dataset for training large language models, Oct. 2023.
  URL <https://github.com/togethercomputer/RedPajama-Data>.
- DeepSeek-AI (2024)

  DeepSeek-AI.
  Deepseek LLM: scaling open-source language models with longtermism.
  *CoRR*, abs/2401.02954, 2024.
  [10.48550/ARXIV.2401.02954](https://doi.org/10.48550/ARXIV.2401.02954).
  URL <https://doi.org/10.48550/arXiv.2401.02954>.
- Du et al. (2022)

  Z. Du, Y. Qian, X. Liu, M. Ding, J. Qiu, Z. Yang, and J. Tang.
  Glm: General language model pretraining with autoregressive blank infilling.
  In *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pages 320–335, 2022.
- Gao et al. (2023)

  L. Gao, A. Madaan, S. Zhou, U. Alon, P. Liu, Y. Yang, J. Callan, and G. Neubig.
  PAL: program-aided language models.
  In A. Krause, E. Brunskill, K. Cho, B. Engelhardt, S. Sabato, and J. Scarlett, editors, *International Conference on Machine Learning, ICML 2023, 23-29 July 2023, Honolulu, Hawaii, USA*, volume 202 of *Proceedings of Machine Learning Research*, pages 10764–10799. PMLR, 2023.
  URL <https://proceedings.mlr.press/v202/gao23f.html>.
- Gou et al. (2023)

  Z. Gou, Z. Shao, Y. Gong, Y. Shen, Y. Yang, M. Huang, N. Duan, and W. Chen.
  Tora: A tool-integrated reasoning agent for mathematical problem solving.
  *CoRR*, abs/2309.17452, 2023.
  [10.48550/ARXIV.2309.17452](https://doi.org/10.48550/ARXIV.2309.17452).
  URL <https://doi.org/10.48550/arXiv.2309.17452>.
- Guo et al. (2024)

  D. Guo, Q. Zhu, D. Yang, Z. Xie, K. Dong, W. Zhang, G. Chen, X. Bi, Y. Wu, Y. K. Li, F. Luo, Y. Xiong, and W. Liang.
  Deepseek-coder: When the large language model meets programming – the rise of code intelligence, 2024.
- Hendrycks et al. (2020)

  D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt.
  Measuring massive multitask language understanding.
  *arXiv preprint arXiv:2009.03300*, 2020.
- Hendrycks et al. (2021)

  D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt.
  Measuring mathematical problem solving with the math dataset.
  *arXiv preprint arXiv:2103.03874*, 2021.
- High-flyer (2023)

  High-flyer.
  Hai-llm: 高效且轻量的大模型训练工具, 2023.
  URL <https://www.high-flyer.cn/en/blog/hai-llm>.
- Inflection AI (2023)

  Inflection AI.
  Inflection-2, 2023.
  URL <https://inflection.ai/inflection-2>.
- Jiang et al. (2022)

  A. Q. Jiang, S. Welleck, J. P. Zhou, W. Li, J. Liu, M. Jamnik, T. Lacroix, Y. Wu, and G. Lample.
  Draft, sketch, and prove: Guiding formal theorem provers with informal proofs.
  *arXiv preprint arXiv:2210.12283*, 2022.
- Jiang et al. (2023)

  A. Q. Jiang, A. Sablayrolles, A. Mensch, C. Bamford, D. S. Chaplot, D. d. l. Casas, F. Bressand, G. Lengyel, G. Lample, L. Saulnier, et al.
  Mistral 7b.
  *arXiv preprint arXiv:2310.06825*, 2023.
- Joulin et al. (2016)

  A. Joulin, E. Grave, P. Bojanowski, M. Douze, H. Jégou, and T. Mikolov.
  Fasttext. zip: Compressing text classification models.
  *arXiv preprint arXiv:1612.03651*, 2016.
- Kwon et al. (2023)

  W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E. Gonzalez, H. Zhang, and I. Stoica.
  Efficient memory management for large language model serving with pagedattention.
  In *Proceedings of the ACM SIGOPS 29th Symposium on Operating Systems Principles*, 2023.
- Leviathan et al. (2023)

  Y. Leviathan, M. Kalman, and Y. Matias.
  Fast inference from transformers via speculative decoding.
  In *International Conference on Machine Learning*, pages 19274–19286. PMLR, 2023.
- Lewkowycz et al. (2022a)

  A. Lewkowycz, A. Andreassen, D. Dohan, E. Dyer, H. Michalewski, V. Ramasesh, A. Slone, C. Anil, I. Schlag, T. Gutman-Solo, et al.
  Solving quantitative reasoning problems with language models.
  *Advances in Neural Information Processing Systems*, 35:3843–3857, 2022a.
- Lewkowycz et al. (2022b)

  A. Lewkowycz, A. Andreassen, D. Dohan, E. Dyer, H. Michalewski, V. V. Ramasesh, A. Slone, C. Anil, I. Schlag, T. Gutman-Solo, Y. Wu, B. Neyshabur, G. Gur-Ari, and V. Misra.
  Solving quantitative reasoning problems with language models.
  In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors, *Advances in Neural Information Processing Systems 35: Annual Conference on Neural Information Systems 2022, NeurIPS 2022, New Orleans, LA, USA, November 28 - December 9, 2022*, 2022b.
  URL <http://papers.nips.cc/paper_files/paper/2022/hash/18abbeef8cfe9203fdf9053c9c4fe191-Abstract-Conference.html>.
- Lightman et al. (2023)

  H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe.
  Let's verify step by step.
  *arXiv preprint arXiv:2305.20050*, 2023.
- Loshchilov and Hutter (2017)

  I. Loshchilov and F. Hutter.
  Decoupled weight decay regularization.
  *arXiv preprint arXiv:1711.05101*, 2017.
- Luo et al. (2023)

  H. Luo, Q. Sun, C. Xu, P. Zhao, J. Lou, C. Tao, X. Geng, Q. Lin, S. Chen, and D. Zhang.
  Wizardmath: Empowering mathematical reasoning for large language models via reinforced evol-instruct.
  *arXiv preprint arXiv:2308.09583*, 2023.
- Mishra et al. (2022)

  S. Mishra, M. Finlayson, P. Lu, L. Tang, S. Welleck, C. Baral, T. Rajpurohit, O. Tafjord, A. Sabharwal, P. Clark, and A. Kalyan.
  LILA: A unified benchmark for mathematical reasoning.
  In Y. Goldberg, Z. Kozareva, and Y. Zhang, editors, *Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing, EMNLP 2022, Abu Dhabi, United Arab Emirates, December 7-11, 2022*, pages 5807–5832. Association for Computational Linguistics, 2022.
  [10.18653/V1/2022.EMNLP-MAIN.392](https://doi.org/10.18653/V1/2022.EMNLP-MAIN.392).
  URL <https://doi.org/10.18653/v1/2022.emnlp-main.392>.
- Nguyen et al. (2023)

  X. Nguyen, W. Zhang, X. Li, M. M. Aljunied, Q. Tan, L. Cheng, G. Chen, Y. Deng, S. Yang, C. Liu, H. Zhang, and L. Bing.
  Seallms - large language models for southeast asia.
  *CoRR*, abs/2312.00738, 2023.
  [10.48550/ARXIV.2312.00738](https://doi.org/10.48550/ARXIV.2312.00738).
  URL <https://doi.org/10.48550/arXiv.2312.00738>.
- OpenAI (2023)

  OpenAI.
  GPT4 technical report.
  *arXiv preprint arXiv:2303.08774*, 2023.
- Ouyang et al. (2022)

  L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, et al.
  Training language models to follow instructions with human feedback.
  *Advances in Neural Information Processing Systems*, 35:27730–27744, 2022.
- Paster et al. (2023)

  K. Paster, M. D. Santos, Z. Azerbayev, and J. Ba.
  Openwebmath: An open dataset of high-quality mathematical web text.
  *CoRR*, abs/2310.06786, 2023.
  [10.48550/ARXIV.2310.06786](https://doi.org/10.48550/ARXIV.2310.06786).
  URL <https://doi.org/10.48550/arXiv.2310.06786>.
- Paulson (2010)

  L. C. Paulson.
  Three years of experience with sledgehammer, a practical link between automatic and interactive theorem provers.
  In R. A. Schmidt, S. Schulz, and B. Konev, editors, *Proceedings of the 2nd Workshop on Practical Aspects of Automated Reasoning, PAAR-2010, Edinburgh, Scotland, UK, July 14, 2010*, volume 9 of *EPiC Series in Computing*, pages 1–10. EasyChair, 2010.
  [10.29007/TNFD](https://doi.org/10.29007/TNFD).
  URL <https://doi.org/10.29007/tnfd>.
- Polu and Sutskever (2020)

  S. Polu and I. Sutskever.
  Generative language modeling for automated theorem proving.
  *CoRR*, abs/2009.03393, 2020.
  URL <https://arxiv.org/abs/2009.03393>.
- Rafailov et al. (2023)

  R. Rafailov, A. Sharma, E. Mitchell, S. Ermon, C. D. Manning, and C. Finn.
  Direct preference optimization: Your language model is secretly a reward model.
  2023.
- Schulman (2020)

  J. Schulman.
  Approximating kl divergence, 2020.
  URL <http://joschu.net/blog/kl-approx.html>.
- Schulman et al. (2015)

  J. Schulman, P. Moritz, S. Levine, M. Jordan, and P. Abbeel.
  High-dimensional continuous control using generalized advantage estimation.
  *arXiv preprint arXiv:1506.02438*, 2015.
- Schulman et al. (2017)

  J. Schulman, F. Wolski, P. Dhariwal, A. Radford, and O. Klimov.
  Proximal policy optimization algorithms.
  *arXiv preprint arXiv:1707.06347*, 2017.
- Shi et al. (2023)

  F. Shi, M. Suzgun, M. Freitag, X. Wang, S. Srivats, S. Vosoughi, H. W. Chung, Y. Tay, S. Ruder, D. Zhou, D. Das, and J. Wei.
  Language models are multilingual chain-of-thought reasoners.
  In *The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023*. OpenReview.net, 2023.
  URL <https://openreview.net/pdf?id=fR3wGCk-IXp>.
- Song et al. (2023)

  F. Song, B. Yu, M. Li, H. Yu, F. Huang, Y. Li, and H. Wang.
  Preference ranking optimization for human alignment.
  *arXiv preprint arXiv:2306.17492*, 2023.
- Suzgun et al. (2022)

  M. Suzgun, N. Scales, N. Schärli, S. Gehrmann, Y. Tay, H. W. Chung, A. Chowdhery, Q. V. Le, E. H. Chi, D. Zhou, et al.
  Challenging big-bench tasks and whether chain-of-thought can solve them.
  *arXiv preprint arXiv:2210.09261*, 2022.
- Tao (2023)

  T. Tao.
  Embracing change and resetting expectations, 2023.
  URL <https://unlocked.microsoft.com/ai-anthology/terence-tao/>.
- Touvron et al. (2023)

  H. Touvron, L. Martin, K. Stone, P. Albert, A. Almahairi, Y. Babaei, N. Bashlykov, S. Batra, P. Bhargava, S. Bhosale, D. Bikel, L. Blecher, C. Canton-Ferrer, M. Chen, G. Cucurull, D. Esiobu, J. Fernandes, J. Fu, W. Fu, B. Fuller, C. Gao, V. Goswami, N. Goyal, A. Hartshorn, R. Hosseini, R. Hou, H. Inan, M. Kardas, V. Kerkez, M. Khabsa, I. Kloumann, A. Korenev, P. S. Koura, M. Lachaux, T. Lavril, J. Lee, D. Liskovich, Y. Lu, Y. Mao, X. Martinet, T. Mihaylov, P. Mishra, I. Molybog, Y. Nie, A. Poulton, J. Reizenstein, R. Rungta, K. Saladi, A. Schelten, R. Silva, E. M. Smith, R. Subramanian, X. E. Tan, B. Tang, R. Taylor, A. Williams, J. X. Kuan, P. Xu, Z. Yan, I. Zarov, Y. Zhang, A. Fan, M. Kambadur, S. Narang, A. Rodriguez, R. Stojnic, S. Edunov, and T. Scialom.
  Llama 2: Open foundation and fine-tuned chat models.
  *CoRR*, abs/2307.09288, 2023.
  [10.48550/arXiv.2307.09288](https://doi.org/10.48550/arXiv.2307.09288).
  URL <https://doi.org/10.48550/arXiv.2307.09288>.
- Trinh et al. (2024)

  T. H. Trinh, Y. Wu, Q. V. Le, H. He, and T. Luong.
  Solving olympiad geometry without human demonstrations.
  *Nature*, 625(7995):476–482, 2024.
- Wang et al. (2023a)

  P. Wang, L. Li, L. Chen, F. Song, B. Lin, Y. Cao, T. Liu, and Z. Sui.
  Making large language models better reasoners with alignment.
  *arXiv preprint arXiv:2309.02144*, 2023a.
- Wang et al. (2023b)

  P. Wang, L. Li, Z. Shao, R. Xu, D. Dai, Y. Li, D. Chen, Y. Wu, and Z. Sui.
  Math-shepherd: Verify and reinforce llms step-by-step without human annotations.
  *CoRR, abs/2312.08935*, 2023b.
- Wang et al. (2023c)

  Z. Wang, R. Xia, and P. Liu.
  Generative AI for math: Part I - mathpile: A billion-token-scale pretraining corpus for math.
  *CoRR*, abs/2312.17120, 2023c.
  [10.48550/ARXIV.2312.17120](https://doi.org/10.48550/ARXIV.2312.17120).
  URL <https://doi.org/10.48550/arXiv.2312.17120>.
- Wei et al. (2022)

  J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. H. Chi, Q. V. Le, and D. Zhou.
  Chain-of-thought prompting elicits reasoning in large language models.
  In *NeurIPS*, 2022.
  URL <http://papers.nips.cc/paper_files/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.html>.
- Wei et al. (2023)

  T. Wei, J. Luan, W. Liu, S. Dong, and B. Wang.
  Cmath: Can your language model pass chinese elementary school math test?, 2023.
- Wenzel et al. (2008)

  M. Wenzel, L. C. Paulson, and T. Nipkow.
  The isabelle framework.
  In O. A. Mohamed, C. A. Muñoz, and S. Tahar, editors, *Theorem Proving in Higher Order Logics, 21st International Conference, TPHOLs 2008, Montreal, Canada, August 18-21, 2008. Proceedings*, volume 5170 of *Lecture Notes in Computer Science*, pages 33–38. Springer, 2008.
  [10.1007/978-3-540-71067-7_7](https://doi.org/10.1007/978-3-540-71067-7_7).
  URL <https://doi.org/10.1007/978-3-540-71067-7_7>.
- Xia et al. (2023)

  H. Xia, T. Ge, P. Wang, S.-Q. Chen, F. Wei, and Z. Sui.
  Speculative decoding: Exploiting speculative execution for accelerating seq2seq generation.
  In H. Bouamor, J. Pino, and K. Bali, editors, *Findings of the Association for Computational Linguistics: EMNLP 2023*, pages 3909–3925, Singapore, Dec. 2023. Association for Computational Linguistics.
  [10.18653/v1/2023.findings-emnlp.257](https://doi.org/10.18653/v1/2023.findings-emnlp.257).
  URL <https://aclanthology.org/2023.findings-emnlp.257>.
- Xia et al. (2024)

  H. Xia, Z. Yang, Q. Dong, P. Wang, Y. Li, T. Ge, T. Liu, W. Li, and Z. Sui.
  Unlocking efficiency in large language model inference: A comprehensive survey of speculative decoding.
  *arXiv preprint arXiv:2401.07851*, 2024.
- Yao et al. (2023)

  S. Yao, D. Yu, J. Zhao, I. Shafran, T. L. Griffiths, Y. Cao, and K. Narasimhan.
  Tree of thoughts: Deliberate problem solving with large language models.
  *arXiv preprint arXiv:2305.10601*, 2023.
- Yu et al. (2023)

  L. Yu, W. Jiang, H. Shi, J. Yu, Z. Liu, Y. Zhang, J. T. Kwok, Z. Li, A. Weller, and W. Liu.
  Metamath: Bootstrap your own mathematical questions for large language models.
  *CoRR*, abs/2309.12284, 2023.
  [10.48550/ARXIV.2309.12284](https://doi.org/10.48550/ARXIV.2309.12284).
  URL <https://doi.org/10.48550/arXiv.2309.12284>.
- Yuan et al. (2023a)

  Z. Yuan, H. Yuan, C. Li, G. Dong, C. Tan, and C. Zhou.
  Scaling relationship on learning mathematical reasoning with large language models.
  *arXiv preprint arXiv:2308.01825*, 2023a.
- Yuan et al. (2023b)

  Z. Yuan, H. Yuan, C. Tan, W. Wang, S. Huang, and F. Huang.
  Rrhf: Rank responses to align language models with human feedback without tears.
  *arXiv preprint arXiv:2304.05302*, 2023b.
- Yue et al. (2023)

  X. Yue, X. Qu, G. Zhang, Y. Fu, W. Huang, H. Sun, Y. Su, and W. Chen.
  Mammoth: Building math generalist models through hybrid instruction tuning.
  *CoRR*, abs/2309.05653, 2023.
  [10.48550/ARXIV.2309.05653](https://doi.org/10.48550/ARXIV.2309.05653).
  URL <https://doi.org/10.48550/arXiv.2309.05653>.
- Zheng et al. (2021)

  K. Zheng, J. M. Han, and S. Polu.
  Minif2f: a cross-system benchmark for formal olympiad-level mathematics.
  *arXiv preprint arXiv:2109.00110*, 2021.
- Zhong et al. (2023)

  W. Zhong, R. Cui, Y. Guo, Y. Liang, S. Lu, Y. Wang, A. Saied, W. Chen, and N. Duan.
  AGIEval: A human-centric benchmark for evaluating foundation models.
  *CoRR*, abs/2304.06364, 2023.
  [10.48550/arXiv.2304.06364](https://doi.org/10.48550/arXiv.2304.06364).
  URL <https://doi.org/10.48550/arXiv.2304.06364>.

## 附录 A 附录

### A.1 强化学习分析

我们提供各种方法（包括 SFT、RFT、Online RFT、DPO、PPO 与 GRPO）的数据来源与梯度系数（算法与奖励函数）的详细推导。

#### A.1.1 监督微调

监督微调的目标是最大化以下目标函数：

$$
\mathcal{J}_{SFT}(\theta)=\mathbb{E}[q,o\sim P_{sft}(Q,O)]\left(\frac{1}{|o|}\sum_{t=1}^{|o|}\log\pi_{\theta}(o_{t}|q,o_{<t})\right). \tag{6}
$$

$\mathcal{J}_{SFT}(\theta)$ 的梯度为：

$$
\nabla_{\theta}\mathcal{J}_{SFT}=\mathbb{E}[q,o\sim P_{sft}(Q,O)]\left(\frac{1}{|o|}\sum_{t=1}^{|o|}\nabla_{\theta}\log\pi_{\theta}(o_{t}|q,o_{<t})\right). \tag{7}
$$

数据来源：SFT 所用的数据集。奖励函数：可视为人工挑选。梯度系数：恒为 1。

#### A.1.2 拒绝采样微调

拒绝采样微调首先为每道题从监督微调后的 LLM 采样多条输出，然后在答案正确的采样输出上训练 LLM。形式上，RFT 的目标是最大化以下目标函数：

$$
\mathcal{J}_{RFT}(\theta)=\mathbb{E}[q\sim P_{sft}(Q),o\sim\pi_{sft}(O|q)]\left(\frac{1}{|o|}\sum_{t=1}^{|o|}\mathbb{I}(o)\log\pi_{\theta}(o_{t}|q,o_{<t})\right). \tag{8}
$$

$\mathcal{J}_{RFT}(\theta)$ 的梯度为：

$$
\nabla_{\theta}\mathcal{J}_{RFT}(\theta)=\mathbb{E}[{q\sim P_{sft}(Q),o\sim\pi_{sft}(O|q)}]\left(\frac{1}{|o|}\sum_{t=1}^{|o|}{\mathbb{I}(o)}\nabla_{\theta}\log\pi_{\theta}(o_{t}|q,o_{<t})\right). \tag{9}
$$

数据来源：SFT 数据集中的问题以及从 SFT 模型采样的输出。奖励函数：规则（答案是否正确）。梯度系数：

$$
GC_{RFT}(q,o,t)=\mathbb{I}(o)=\left\{\begin{aligned} 1&&{\text{$o$ 的答案正确}}\\ 0&&{\text{$o$ 的答案错误}}\\ \end{aligned}\right. \tag{10}
$$

#### A.1.3 在线拒绝采样微调

RFT 与 Online RFT 的唯一区别在于，Online RFT 的输出是从实时策略模型 $\pi_{\theta}$ 采样，而非从 SFT 模型 $\pi_{\theta_{sft}}$ 采样。因此，Online RFT 的梯度为：

$$
\nabla_{\theta}\mathcal{J}_{OnRFT}(\theta)=\mathbb{E}[{q\sim P_{sft}(Q),o\sim\pi_{\theta}(O|q)}]\left(\frac{1}{|o|}\sum_{t=1}^{|o|}{\mathbb{I}(o)}\nabla_{\theta}\log\pi_{\theta}(o_{t}|q,o_{<t})\right). \tag{11}
$$

#### A.1.4 直接偏好优化（DPO）

DPO 的目标函数为：

$$
\begin{split}\mathcal{J}_{DPO}(\theta)=\mathbb{E}{[q\sim P_{sft}(Q),o^{+},o^{-}\sim\pi_{sft}(O|q)]}\log\sigma\left(\beta\frac{1}{|o^{+}|}\sum_{t=1}^{|o^{+}|}\log\frac{\pi_{\theta}(o^{+}_{t}|q,o^{+}_{<t})}{\pi_{\text{ref}}(o^{+}_{t}|q,o^{+}_{<t})}-\beta\frac{1}{|o^{-}|}\sum_{t=1}^{|o^{-}|}\log\frac{\pi_{\theta}(o^{-}_{<t}|q,o^{-}_{<t})}{\pi_{\text{ref}}(o^{-}_{<t}|q,o^{-}_{<t})}\right)\end{split} \tag{12}
$$

$\mathcal{J}_{DPO}(\theta)$ 的梯度为：

$$
\begin{split}\nabla_{\theta}\mathcal{J}_{DPO}(\theta)=\mathbb{E}{[q\sim P_{sft}(Q),o^{+},o^{-}\sim\pi_{sft}(O|q)]}&\left(\frac{1}{|o^{+}|}\sum_{t=1}^{|o^{+}|}GC_{DPO}(q,o,t)\nabla_{\theta}\log\pi_{\theta}(o^{+}_{t}|q,o^{+}_{<t})\right.\\ -&\left.\frac{1}{|o^{-}|}\sum_{t=1}^{|o^{-}|}GC_{DPO}(q,o,t)\nabla_{\theta}\log\pi_{\theta}(o^{-}_{t}|q,o^{-}_{<t})\right)\end{split} \tag{13}
$$

数据来源：SFT 数据集中的问题以及从 SFT 模型采样的输出。奖励函数：一般领域的人类偏好（在数学任务中可为「规则」）。梯度系数：

$$
GC_{DPO}(q,o,t)=\sigma\left(\beta\log\frac{\pi_{\theta}(o^{-}_{t}|q,o^{-}_{<t})}{\pi_{\text{ref}}(o^{-}_{t}|q,o^{-}_{<t})}-\beta\log\frac{\pi_{\theta}(o^{+}_{t}|q,o^{+}_{<t})}{\pi_{\text{ref}}(o^{+}_{t}|q,o^{+}_{<t})}\right) \tag{14}
$$

#### A.1.5 近端策略优化（PPO）

PPO 的目标函数为：

$$
\mathcal{J}_{PPO}(\theta)=\mathbb{E}{[q\sim P_{sft}(Q),o\sim\pi_{\theta_{old}}(O|q)]}\frac{1}{|o|}\sum_{t=1}^{|o|}\min\left[\frac{\pi_{\theta}(o_{t}|q,o_{<t})}{\pi_{\theta_{old}}(o_{t}|q,o_{<t})}A_{t},\text{clip}\left(\frac{\pi_{\theta}(o_{t}|q,o_{<t})}{\pi_{\theta_{old}}(o_{t}|q,o_{<t})},1-\varepsilon,1+\varepsilon\right)A_{t}\right]. \tag{15}
$$

为简化分析，假设模型在每个探索阶段之后只做单次更新，从而保证 $\pi_{\theta_{old}}=\pi_{\theta}$。此时可以去掉 $\min$ 与 $\text{clip}$ 操作：

$$
\mathcal{J}_{PPO}(\theta)=\mathbb{E}{[q\sim P_{sft}(Q),o\sim\pi_{\theta_{old}}(O|q)]}\frac{1}{|o|}\sum_{t=1}^{|o|}\frac{\pi_{\theta}(o_{t}|q,o_{<t})}{\pi_{\theta_{old}}(o_{t}|q,o_{<t})}A_{t}. \tag{16}
$$

$\mathcal{J}_{PPO}(\theta)$ 的梯度为：

$$
\begin{split}\nabla_{\theta}\mathcal{J}_{PPO}(\theta)=\mathbb{E}{[q\sim P_{sft}(Q),o\sim\pi_{\theta_{old}}(O|q)]}\frac{1}{|o|}\sum_{t=1}^{|o|}A_{t}\nabla_{\theta}\log\pi_{\theta}(o_{t}|q,o_{<t})\end{split} \tag{17}
$$

数据来源：SFT 数据集中的问题以及从策略模型采样的输出。奖励函数：奖励模型。梯度系数：

$$
GC_{PPO}(q,o,t,\pi_{\theta_{rm}})=A_{t}, \tag{18}
$$

其中 $A_{t}$ 是优势，基于奖励 $\{r_{\geq t}\}$ 与一个学习到的价值函数 $V_{\psi}$，通过应用广义优势估计（GAE）（Schulman et al., 2015）计算。

#### A.1.6 组相对策略优化（GRPO）

GRPO 的目标函数为（为简化分析假设 $\pi_{\theta_{old}}=\pi_{\theta}$）：

$$
\begin{split}\mathcal{J}_{GRPO}(\theta)&=\mathbb{E}{[q\sim P_{sft}(Q),\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta_{old}}(O|q)]}\\ &\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|o_{i}|}\sum_{t=1}^{|o_{i}|}\left[\frac{\pi_{\theta}(o_{i,t}|q,o_{i,<t})}{\pi_{\theta_{old}}(o_{i,t}|q,o_{i,<t})}\hat{A}_{i,t}-\beta(\frac{\pi_{ref}(o_{i,t}|q,o_{i,<t})}{\pi_{\theta}(o_{i,t}|q,o_{i,<t})}-\log\frac{\pi_{ref}(o_{i,t}|q,o_{i,<t})}{\pi_{\theta}(o_{i,t}|q,o_{i,<t})}-1)\right].\end{split} \tag{19}
$$

$\mathcal{J}_{GRPO}(\theta)$ 的梯度为：

$$
\begin{split}\nabla_{\theta}\mathcal{J}_{GRPO}(\theta)&=\mathbb{E}{[q\sim P_{sft}(Q),\{o_{i}\}_{i=1}^{G}\sim\pi_{\theta_{old}}(O|q)]}\\ &\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|o_{i}|}\sum_{t=1}^{|o_{i}|}\left[\hat{A}_{i,t}+\beta\left(\frac{\pi_{ref}(o_{i,t}|o_{i,<t})}{\pi_{\theta}(o_{i,t}|o_{i,<t})}-1\right)\right]\nabla_{\theta}\log\pi_{\theta}(o_{i,t}|q,o_{i,<t}).\end{split} \tag{20}
$$

数据来源：SFT 数据集中的问题以及从策略模型采样的输出。奖励函数：奖励模型。梯度系数：

$$
GC_{GRPO}(q,o,t,\pi_{\theta_{rm}})=\hat{A}_{i,t}+\beta\left(\frac{\pi_{ref}(o_{i,t}|o_{i,<t})}{\pi_{\theta}(o_{i,t}|o_{i,<t})}-1\right), \tag{21}
$$

其中 $\hat{A}_{i,t}$ 基于组奖励分数计算。

