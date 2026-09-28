---
title: "用弱验证器缩小生成与验证的差距"
title_en: "Shrinking the Generation-Verification Gap with Weak Verifiers"
arxiv: 2506.18203
source: https://arxiv.org/abs/2506.18203
crawled: 2026-09-23
translated: 2026-09-23
---

# 用弱验证器缩小生成与验证的差距

> 原文：[Shrinking the Generation-Verification Gap with Weak Verifiers](https://arxiv.org/abs/2506.18203) · Stanford CS329A 指定阅读

Jon Saad-Falcon†、E. Kelly Buchanan†∗、Mayee F. Chen†∗、Tzu-Heng Huang‡、Brendan McLaughlin†、Tanvir Bhathal†、Shang Zhu§、Ben Athiwaratkun§、Frederic Sala‡、Scott Linderman†、Azalia Mirhoseini†、Christopher Ré†

† 斯坦福大学；‡ 威斯康星大学麦迪逊分校；§ Together AI
注：同等贡献。通讯作者：<jonsaadfalcon,kelly.buchanan,mfchen>@stanford.edu

###### 摘要

验证器（verifier）可以通过对生成候选池中的回答打分与排序来提升语言模型（LM）的能力。目前，高质量的验证器要么不可扩展（如人类），要么用途受限（如用于形式化证明的 Lean 等工具）。虽然 LM 裁判（judge）与奖励模型作为通用验证器已经广为有用，但它们与 oracle 验证器（即具有完美准确率的验证器）之间仍存在显著的性能差距。为帮助缩小这一差距，我们提出 Weaver——一个通过组合多个弱的不完美验证器来设计强验证器的框架。我们首先发现，验证器的加权集成（通常需要从标注数据学习）由于验证器准确率之间的差异，显著优于无加权组合。为降低对标注数据的依赖，Weaver 利用弱监督（weak supervision）来估计每个验证器的准确率，并把它们的输出组合成一个能更好反映真实回答质量的统一分数。然而，直接应用弱监督算法面临若干挑战，包括验证器输出格式不一致以及低质量验证器的处理。Weaver 通过使用数据集统计量来归一化输出并过滤特定验证器，从而应对这些挑战。我们在测试时重复采样设置下研究 Weaver 的有效性：模型生成多个候选回答，并从中选择一个。我们的评估表明，Weaver 在多个推理与数学任务上显著超越 $Pass@1$（即直接选择第一个候选回答的表现）：以 Llama 3.3 70B Instruct（一个便宜得多的非推理模型）作为生成器、以 70B 及更小的裁判与奖励模型集成作为验证器（平均 87.7%），达到了 o3-mini 水准的准确率。这一增益堪比 GPT-4o 到 o3-mini 的跨越（69.0% 对 86.7%），而后者需要大量微调与后训练干预。为降低为 Weaver 运行验证器集成的计算成本，我们用 Weaver 的组合输出分数训练了一个紧凑的 400M 交叉编码器。这一蒸馏模型保留了 Weaver 全部准确率的 98.7%，同时将验证计算最多削减 99.97%。

## 1 引言

部署语言模型（LM）的一个核心挑战是验证：判定模型回答的质量或正确性。这一问题出现在 LM 流水线的各个环节，包括数据集整理、模型对齐与推理时决策。验证依赖验证器——为回答打分的函数。与重复采样（从 LM 生成多个候选回答）结合时，一个完美的验证器可用来选出正确的候选回答，显著增强模型在数学、代码与推理等任务上的能力（Snell et al., 2024；Brown et al., 2024；Puri et al., 2025）。例如，配上这些数学任务的完美验证器后，Llama 3.1 8B Instruct 可以在 MATH500（Hendrycks et al., 2021）与 MiniF2F（Zheng et al., 2022）上匹敌 Llama 3.1 70B Instruct 甚至 GPT-4o。然而，没有完美验证器时，就会出现生成-验证差距（generation-verification gap）（Song et al., 2025）：LM 能生成正确的回答，我们却无法识别它。

生成-验证差距普遍存在于数学、编程、科学推理、指令遵循等众多任务中。其中一些场景我们可以使用能完美识别正确回答的 oracle 验证器。突出的例子是 Lean，一个可用于 MiniF2F（Zheng et al., 2022）等问题的形式化定理证明器。但这往往是一个受限的设置，因为并非所有数学证明都能被 Lean 处理。或者，人类可以评判 LM 的回答，但人工评估往往昂贵、有噪声且难以规模化（Hosking et al., 2024；Clark et al., 2021；Karpinska et al., 2021）。相比之下，被提示为裁判的 LM（Chiang et al., 2024）与奖励模型（Lambert et al., 2024；Singhi et al., 2025；Liu et al., 2025）可以开箱即用地应用于数学、编程、科学推理、指令遵循等任务（Hendrycks et al., 2021；Rein et al., 2024；Jain et al., 2024；Li et al., 2024）。然而，这些弱验证器产生有噪声、不一致的分数，往往校准很差，且假阳性率很高（Stroebl et al., 2024）。我们要问：在重复采样机制下，我们能在多大程度上利用弱验证器来提升准确率？

我们探索扩展验证（scaling verification），具体而言是如何组合多个弱验证器以改进重复采样的回答选择。随着新的预训练模型不断出现，弱验证器池持续扩大，提供了多样化、互补的信号来源——只要能有效聚合，它们就能改进回答选择。近期工作已通过自验证或对 LM 裁判分数取平均等技术探索扩展验证（Lifshitz et al., 2025；Zhao et al.；Chen et al., 2025），但也有工作发现用弱验证器做回答选择时测试时计算的扩展存在局限（Stroebl et al., 2024）。我们观察到集成弱验证器的三个关键挑战：

![Refer to caption](2506.18203v3/weaver-revised.png)

图 1：Weaver 框架：我们提出 Weaver，一个组合多个弱验证器的框架，无需在真值标签上做参数微调即可有效扩展重复采样（左）。Weaver 显著优于多数投票，在 GPQA Diamond 及其他数据集上平均把模型的生成-验证差距缩小 14.5%（表 1）（中）。通过把 Weaver 从 70B 验证器集成蒸馏到单个 400M 交叉编码器，我们可以在把推理计算成本降低 99.97% 的同时保留 Weaver 98.2% 的准确率增益（右）。

1. 朴素地聚合弱验证器不足以实现可靠验证。诸如基于 LM 的裁判或奖励模型等弱验证器产生有噪声、有偏且校准不佳的分数，导致表现不稳定（Stroebl et al., 2024；Lambert et al., 2024；Chiang et al., 2024）。对验证器分数做朴素无加权平均虽然简单，却隐含假定各验证器质量均一，使低质量验证器占据主导并拉低整体准确率（Verga et al., 2024；Xu et al., 2024；Eisenstein et al., 2023）。此外，虽然先前工作假设更复杂的加权集成应当表现更好，这一论断尚未被研究过（Lifshitz et al., 2025）。
2. 在有限标注数据下做有效集成颇具挑战。更复杂的集成技术通常从标注数据学习验证器权重，而这类数据昂贵且难以获得。弱监督（Weak Supervision，WS）——一族为数据标注发展的统计技术——提供了一个可能的解决方案：其算法在只需少量标注数据的前提下聚合多个弱信号（如众包工人标注与专家定义的启发式）（Ratner et al., 2016；Ratner et al., 2019；Fu et al., 2020）。在传统 WS 中，从业者可以设计并塑造每个弱信号以确保足够质量（即迭代调整基于程序的启发式），WS 的保证依赖于一个基准质量水平。而我们的弱信号是固定的预训练语言模型验证器，其准确率差异悬殊——尤其在应用于分布外任务时——并可能输出互不兼容的形式（logits、二元分数、Likert 分数）（Lambert et al., 2024），我们无法轻易调整它们。由于这些条件，直接应用于验证时 WS 算法可能表现不佳。
3. 验证在推理时部署代价高昂。验证可能主导推理时成本（Singhi et al., 2025；Liu et al., 2025），因为每个验证器都必须同时处理问题及其候选回答（Lightman et al., 2023），且往往要评估中间步骤（Lightman et al., 2023）与多条解题路径（Snell et al., 2024）。事实上，要超过未验证生成（即多数投票）的增益，每个查询可能需要 10 倍到 128 倍的推理计算（Singhi et al., 2025；Lifshitz et al., 2025；Zhao et al.；Chen et al., 2025）。

在本工作中，我们提出 Weaver——一个无需在真值标签上做监督微调即可聚合弱验证器的框架（图 1）。首先，我们证明如果能获取大规模标注训练数据（例如 50,000 个查询-回答对），我们可以学出比朴素平均高出最多 11.2 个百分点的加权集成。这是因为加权集成利用了验证器准确率的巨大差异。然而，在许多现实场景中我们无法获得如此数量的标注数据。其次，为降低对标注数据的依赖，我们通过解决输出不一致与低准确率验证器周围的挑战，把弱监督适配到验证设置。Weaver 过滤掉无信息量的验证器、归一化验证器分数，并基于这些分数与未知真值标签构建一个隐变量模型，以估计验证器准确率作为集成的权重（Ratner et al., 2016；Hall, 2003）。

经验上，给定重复采样预算与一组验证器，Weaver 相比「验证器分数无加权平均的重复采样」提升 17.1%，相比多数投票提升 13.5%（表 1；图 3）。相比 LM 的 $Pass@1$，Weaver 使我们在推理与数学任务上为 8B 模型提升 17.9%、为 70B 模型提升 14.5%（表 1 与表 20）。这堪比 GPT-4o 到 o3-mini 的性能跳跃（73.9% 对 88.2%）——但只靠测试时增加采样，而非参数调优或后训练流程。我们还研究 Weaver 沿测试时计算的不同轴（生成、验证器、模型规模与推理预算）如何扩展（第 5.2 节）。我们发现，即便增加生成数量，许多标准验证基线（如多数投票）也很快进入平台期（图 3）。朴素集成饱和得更慢，但其增益受限于对模型选择与验证器数量的敏感性。

最后，为缓解为每个回答调用多个弱验证器的计算成本，我们扩展 Weaver：用 Weaver 选出的回答训练一个 400M 参数的交叉编码器验证器。我们证明，用蒸馏出的 Weaver 交叉编码器作为验证器可保留学习到的验证器集成 98.7% 的准确率增益，同时把计算成本降低三个数量级——节省 99.97% 的推理 FLOPs，且仍然捕获一种有效的验证策略（第 6 节）。总体而言，我们的发现凸显：即便缺乏真值标签，更可靠、可扩展的验证也是可能的——为更好的数据过滤、模型对齐与推理时决策铺平道路。

## 2 相关工作

LM 裁判与奖励模型：LM 裁判与奖励模型都是评估语言模型输出的有前景的方法，但其高假阳性率限制了可靠性（Stroebl et al., 2024）。LM 裁判无需额外训练即可评估输出（Liu et al., 2023；Wang et al., 2023；Fu et al., 2023），方法涵盖从简单提示到思维链推理（Liu et al., 2023）、专门微调（Saad-Falcon et al., 2023；Tang et al., 2024）再到多 LM 推理架构（Kalra & Tang, 2025；Verga et al., 2024）。然而它们面临跨上下文的糟糕泛化（Es et al., 2023；Saad-Falcon et al., 2023；Ravi et al., 2024）以及位置与自我偏好方面的系统性偏差（Chen et al., 2024；Pan et al., 2024；Zheng et al., 2023）。类似地，虽然奖励模型已成为模型对齐的核心（Christiano et al., 2017；Ouyang et al., 2022；Kirchner et al., 2024），它们受困于标注者间低一致率带来的噪声训练信号（Askell et al., 2021；Wang et al., 2024；Zheng et al., 2023；Dubois et al., 2024）以及偏好回答长度等属性的习得偏差（Lambert & Calandra, 2023；Singhal et al., 2023；Dubois et al., 2024）。近期工作通过更好的数据收集、思维链推理与自然语言单元测试改进了单个验证器的可靠性（Zhang et al., 2024；Yuan et al.；Saad-Falcon et al., 2024），但根本性挑战依然存在（Eisenstein et al., 2023；Chaudhari et al., 2024）。Weaver 超越这些方法的地方在于：以自适应加权组合多个验证信号，从而利用弱验证器的互补优势，同时抑制噪声、降低假阳性。

弱监督：Weaver 建立在弱监督的统计技术之上。弱监督作为一个通过聚合多个弱来源以程序化生成训练标签的框架而兴起（Ratner et al., 2016；Ratner et al., 2020）。虽然大部分工作聚焦分类任务（Ratner et al., 2019；Fu et al., 2020；Chen et al., 2022），近期进展已扩展到多任务设置（Shin et al.）与结构化预测（Vishwakarma & Sala, 2022）。弱监督还被应用于 LM 提示（Arora et al., 2022）与路由（Guha et al., 2024）。Weaver 把弱监督应用于回答验证，把二元的不完美验证信号（如奖励模型与 LM 裁判）视作把候选解答分类为正确/不正确的弱监督投票者。这一新颖应用通过把这些多样化信号转换为二元裁决来组合预测，使 Weaver 能从弱但互补的验证器中学习更好的验证策略。

验证作为另一条计算轴与聚合：近期工作已把验证探索为一条新的扩展轴（Lifshitz et al., 2025；Liu et al., 2025；Zhao et al.；Singhi et al., 2025；Stroebl et al., 2024；Chen et al., 2025）。然而这些工作把分析限制在单个验证器上，转而扩展验证次数（Zhao et al.）。确实利用多个验证器的方法往往依赖大量标注数据来做聚合或创建专门验证器（Qwen2.5-Math；Lifshitz et al., 2025）。借助 Weaver，我们表明即使验证器并非专门定制，也可以在没有真值标签的情况下组合它们。另一些工作聚焦于用多个验证器通过 RLHF 对基座模型做后训练（Wang et al., 2025；Eisenstein et al., 2023；Wang et al.）。

## 3 预备知识

首先，我们定义如何在重复样本中进行选择的问题。然后定义验证器与关键评估指标，包括生成-验证差距。

问题定义　设 $q\in\mathcal{Q}$ 为一个输入文本查询，$r\in\mathcal{R}\sim\mathcal{M}(q)$ 为以非零温度从语言模型 $\mathcal{M}$ 采样的对应回答。对给定的查询-回答对 $(q,r)$，定义 $y:\mathcal{Q}\times\mathcal{R}\rightarrow\{0,1\}$，使 $y(q,r)$ 是 $r$ 对 $q$ 的正确性标签。

给定一个无标注测试数据集 $\mathcal{D}^{\text{test}}=\{(q_{i},\bm{r_{i}})\}_{i=1}^{n}$，其中 $\bm{r_{i}}=\{r_{ij}\}_{j=1}^{K}$ 由 $\mathcal{M}$ 为每个 $q_{i}$ 重复采样的 $K$ 个回答组成。我们还假设可以访问一个小的有标注开发集 $\mathcal{D}^{\text{dev}}\subset\mathcal{D}^{\text{test}}$，占测试集的 1%（例如 5 到 10 个查询-回答对），用于估计诸如任务难度概率 $\Pr(y_{ij}=1)$ 之类的全局统计量。我们对 $\mathcal{D}^{\text{test}}\setminus\mathcal{D}^{\text{dev}}$ 中的任何 $i,j$ 都无法获得真值标签 $y_{ij}:=y(q_{i},r_{ij})$。

对每个 $(q_{i},\bm{r}_{i})\in\mathcal{D}^{\text{test}}$，我们的目标是选出一个满足 $y_{ij^{\star}}=1$ 的正确回答 $j^{\star}\in[K]$。我们可以用一个打分函数 $f:\mathcal{Q}\times\mathcal{R}\rightarrow\mathbb{R}$ 来宽泛地描述这一选择规则，即 $j^{\star}:=\arg\max_{j}f^{\star}(q_{i},r_{ij})$。

使用验证器　一个验证器——无论是奖励模型还是被提示为裁判的 LM——都可以表达为查询-回答对上的打分函数 $v:\mathcal{Q}\times\mathcal{R}\rightarrow\mathbb{R}$。对奖励模型，验证器分数是连续的；对 LM 裁判，验证器分数通常是离散的（在我们的设置中分别使用 $[0,1]$ 与 $\{0,1\}$）。我们假设可以访问多个验证器 $\mathcal{V}=\{v_{1},\dots,v_{m}\}$。我们把 $m$ 个验证器应用于每个 $(q_{i},r_{ij})$，在 $\mathcal{D}^{\text{test}}$ 上共得到 $nmK$ 个分数，记 $s_{ijk}:=v_{k}(q_{i},r_{ij})$。我们旨在用 $\mathcal{V}$ 构造一个验证策略 $f$。

评估指标　$Pass@1$ 指标是 LM 第一个回答正确的概率。$Pass@K$ 推广了该指标，定义为 $K$ 个生成回答中存在正确回答的概率：$Pass@K=\frac{1}{n}\sum_{i=1}^{n}\mathbf{1}(\exists j\in[K]:y_{ij}=1)$。该指标与验证策略无关，取决于 $\mathcal{M}$、$K$ 与任务数据集的选择。验证策略 $\hat{f}$ 的成功率是 $\frac{1}{n}\sum_{i=1}^{n}y_{i\hat{j}}$，其中 $\hat{j}=\arg\max_{j\in[k]}\hat{f}(q_{i},r_{ij})$。成功率依赖验证策略且以 Pass@K 为上界，oracle 验证（即 $\hat{f}=f^{\star}$，只要存在正确 $j$ 就总能选出）时取得等号。

我们把生成-验证差距定义为 Pass@K 减去成功率。较大的正差距意味着：虽然生成了正确答案，验证策略却无法持续选中它们。我们的目标是缩小这一差距，并将用它评估验证策略。

## 4 Weaver：一个弱验证器聚合框架

在第 4.1 节中，我们证明朴素地平均多个验证器分数来选择回答显著逊于加权集成；然而计算权重的常见方法需要标注数据（Schapire, 2013；Ying et al., 2015）。我们提出 Weaver（第 4.2 节），一个用最少数据对验证器分数做加权聚合的方法，其灵感来自弱监督。与先前工作不同，Weaver 通过解决验证器聚合特有的挑战（如分数格式不一致、存在低质量或对抗性验证器）把弱监督适配到验证。据我们所知，这是首个成功把弱监督应用于集成验证器分数以做回答选择的框架。

### 4.1 如何聚合多个验证器：加权与无加权集成

使用多个验证器的一个直接做法是朴素集成——选择平均验证器分数最高的回答：$f(q_{i},r_{ij})=\frac{1}{m}\sum_{k=1}^{m}s_{ijk}$。这一方法（Lifshitz et al., 2025）没有考虑验证器的相对准确率。然而，我们观察到单个验证器的成功率存在显著差异——跨度可达 37.5%——表明朴素集成可能是次优的（表 16）。

另一种做法是使用加权集成。一种办法是用一个有标注数据集找出并使用表现最好的验证器，实际上等于给被舍弃的验证器赋权重 $0$。其他策略包括使用逻辑回归或朴素贝叶斯分类器，其中打分函数 $f(q_{i},r_{ij})$ 是概率 $\Pr(y_{ij}=1|s_{ij1},\dots,s_{ijm})$。这些分类器用标注数据拟合，可以分别建模为 logistic 函数或用贝叶斯法则与独立性假设做因子分解。

在图 2 中，我们比较了朴素集成与若干任务的加权集成，用 Llama 3.3 70B Instruct 生成回答，并使用 33 个 7B-72B 的奖励模型与 LM 裁判作为验证器（附录 C.1）。我们看到，使用加权集成可以比朴素集成高出最多 11.2 个百分点的成功率。然而，图中所有加权集成都是「oracle」方法：它们用到了所有 $i\in[n],j\in[K]$ 的 $y_{ij}$，而实践中这些标签对 $\mathcal{D}^{\text{test}}$ 是未知的。事实上，当我们改用 $0.01n$ 个标注样本时，准确率平均下降 20.1%（表 17）。这就提出了一个问题：如何在有限标注数据下最好地构造加权集成。

图 2：加权验证器集成优于朴素验证器集成：通过用 oracle 数据保留最好的验证器（即 top-$K$ 验证器集成）或为验证器学习聚合权重（即有监督加权集成），我们可以分别比现有验证器的朴素组合平均改进 3.6% 与 7.8%。

### 4.2 Weaver：用最少标注数据对验证器分数做加权集成

我们首先描述 Weaver 中用来在二元验证器分数上构造加权集成的 WS 方法。由于验证器往往产生格式不一致的分数且准确率低——这些是传统 WS 中通常不会遇到的挑战——我们在附录 B.2 与 B.3 中引入一个二值化与验证器丢弃策略，以丢弃低质量验证器，并确保只有足够可靠的二元分数被用作 WS 方法的输入。

#### 4.2.1 弱监督算法

在弱监督中，输入是一个无标注数据集，其中每个条目对真值标签有多个二元「投票」。应用到我们的设置：每个条目是一个查询-回答对，构成大小为 $nK$ 的数据集；验证器分数 $s_{ijk}$ 被二值化为投票 $\bar{s}_{ijk}\in\{0,1\}$（对所有 $i,j,k$）。我们的目标是预测回答正确的概率 $\Pr(y_{ij}=1|s_{ij1},\dots,s_{ijm})$（对所有 $i,j$）。

##### WS 模型

我们可以把所有查询-回答对上的 $y_{ij}$ 视为未知随机变量 $Y$ 的样本，把每个 $i,j$ 上的 $\bar{s}_{ijk}$ 视为随机变量 $S_{k}$ 的样本。WS 随后在随机二元向量 $\{Y,S_{1},\dots,S_{m}\}$ 上定义一个隐变量图模型，其中 $Y$ 是隐变量而 $S_{1},\dots S_{m}$ 可观测。虽然现有 WS 方法假设了多种模型，一个常见假设是对每个 $S_{i},S_{j}$ 有 $S_{i}\perp S_{j}|Y$。也就是说，给定 $Y$ 时 $S_{i}$ 与 $S_{j}$ 条件独立；直觉上，每个验证器被假定捕获回答正确性的不同独立侧面（附录 C.4 中的图 22）。在该假设下，对给定的二元验证器分数 $\{\bar{s}_{1},\dots,\bar{s}_{m}\}$，我们可以把正确生成的后验概率写为：

$$
\Pr(Y=1|S_{1}=\bar{s}_{1},\dots,S_{m}=\bar{s}_{m})=\frac{\prod_{i=1}^{m}\Pr(S_{i}=\bar{s}_{i}|Y=1)\Pr(Y=1)}{\Pr(S_{1}=\bar{s}_{1},\dots,S_{m}=\bar{s}_{m})}. \tag{1}
$$

于是每个查询-回答对的加权集成分数可以用以下几项表达：1) $\Pr(S_{1}=\bar{s}_{1},\dots,S_{m}=\bar{s}_{m})$，对大的 $m$ 从数据计算不可行；2) $\Pr(Y=1)$，可以从 $\mathcal{D}^{\text{dev}}$ 估计；3) $\Pr(S_{i}=\bar{s}_{i}|Y=1)$，等价地 $\Pr(S_{i}=1|Y=1)$，即验证器的「准确率参数」——由于我们无法访问 $Y$，它无法直接计算。接下来我们讨论如何在没有标签的情况下估计这些准确率参数 $\Pr(S_{i}=1|Y=1)$。

##### WS 参数估计

我们概述一个最早在（Ratner et al., 2020）中引入的参数估计技术。由于假设 $S_{i}\perp S_{j}|Y$，以下等式成立：

$$
\Pr(S_{i},S_{j})=\Pr(S_{i},S_{j}|Y=1)\Pr(Y=1)+\Pr(S_{i},S_{j}|Y=0)\Pr(Y=0)
$$

$$
=\Pr(S_{i}|Y=1)\Pr(S_{j}|Y=1)\Pr(Y=1)+\Pr(S_{i}|Y=0)\Pr(S_{j}|Y=0)\Pr(Y=0). \tag{2}
$$

注意 $\Pr(S_{i},S_{j})$ 可以从已知的验证器分数计算，而 $\Pr(Y=1)$ 从 $\mathcal{D}^{\text{dev}}$ 估计。于是式 (2) 是关于准确率参数的二次方程。我们可以对每对 $S_{i},S_{j}$、以及它们可取的每对取值 $\{0,1\}^{2}$ 写出该方程。此外，我们还可以写出关于准确率参数的另一类方程：

$$
\Pr(S_{i}=1)=\Pr(S_{i}=1|Y=1)\Pr(Y=1)+\Pr(S_{i}=1|Y=0)\Pr(Y=0). \tag{3}
$$

这是一个无论条件独立假设是否成立都成立的一致性性质，我们可以对 $m$ 个 $S_{i}$ 中的每一个写出该方程。因为我们知道准确率参数应当满足式 (2) 与式 (3)，我们可以构造一个目标函数，旨在最小化这些等式左右两边之差。我们用矩阵记号高效地写出它。设 $P\in\mathbb{R}^{2\times 2}$ 为对角元为 $[\Pr(Y=0)\;\Pr(Y=1)]$ 的对角矩阵。定义 $\mu\in\mathbb{R}^{m\times 2}$ 为准确率参数矩阵，定义 $O\in\mathbb{R}^{2m\times 2m}$ 为 $S_{i},S_{j}$ 对的联合概率矩阵；更正式地：

$$
\mu_{2i-1:2i,1:2}={\tiny\begin{bmatrix}\Pr(S_{i}=0|Y=0)&\Pr(S_{i}=0|Y=1)\\ \Pr(S_{i}=1|Y=0)&\Pr(S_{i}=1|Y=1)\end{bmatrix}},\;\;O_{2i-1:2i,2i-1:2i}={\tiny\begin{bmatrix}\Pr(S_{i}=0)&0\\ 0&\Pr(S_{i}=1)\end{bmatrix}}\;\forall i\in[m]
$$

$$
O_{2i-1:2i,2j-1:2j}={\tiny\begin{bmatrix}\Pr(S_{i}=0,S_{j}=0)&\Pr(S_{i}=0,S_{j}=1)\\ \Pr(S_{i}=1,S_{j}=0)&\Pr(S_{i}=1,S_{j}=1)\end{bmatrix}}\;\forall i\neq j\in[m] \tag{4}
$$

设 off-diag 表示矩阵中位于其 $2\times 2$ 块对角之外的元素。那么，为估计同时满足式 (2) 与式 (3) 的 $\mu$，我们有以下目标：

$$
\text{minimize}_{\mu}\bigl\|\,O_{\text{off-diag}}-(\mu\,P\,\mu^{T})_{\text{off-diag}}\bigr\|^{2}+\bigl\|\,\mathrm{diag}(O)-\mu\,P\,\mathbf{1}^{T}\bigr\|^{2} \tag{5}
$$

我们用梯度下降优化式 (5) 来估计验证器准确率参数。这些估计随后被用于式 (1)，以选择估计后验最高的回答。为进一步改进验证器准确率的建模，我们探索了按经验难度划分查询分布是否能带来更好的弱监督估计。如附录 B.4 所详述，我们基于观察到的正确/错误生成比例对查询聚类，并在每个难度桶内拟合一个单独的 Weaver 模型。我们在 B.1 节提供更多细节。

## 5 结果

在第 5.1 节中，我们给出 Weaver 相对其他重复采样回答选择方法的经验结果。在第 5.2 节中，我们研究 Weaver 的表现如何沿几个轴扩展：回答数量、模型规模、验证器数量与推理计算。

数据集、验证器与基线　我们的奖励模型规模从 8B 到 72B，全部开源，取自 RewardBench（Lambert et al., 2024）——一个流行的奖励模型评估工具。我们提示来自 Chatbot Arena（Chiang et al., 2024）的开源语言模型充当裁判。除非特别说明，我们用 Llama 3.3 70B Instruct 生成回答并使用全部 33 个奖励模型与裁判。我们在 MATH500、GPQA Diamond、MMLU College 与 MMLU Pro 上评估。更多细节见 C.1 节。

我们把 Weaver 与免验证器基线及标准验证策略比较。首个样本（First Sample），又称 Pass@1，只使用第一个回答，不扩展测试时计算或验证。多数投票（Majority Voting）涉及重复采样但不做验证，从回答中挑选最常见的最终答案（Brown et al., 2024；Snell et al., 2024；Chen et al., 2024）。我们与 RewardBench 上得分最高的奖励模型以及 top-10 奖励模型的朴素集成比较。我们还评估两种近期提出的扩展验证、但不使用不同验证器模型或加权集成的方法：自验证（Self-Verification）（Zhao et al.）与多智能体验证（Multi-Agent Verification）（Lifshitz et al., 2025）。最后，我们报告 oracle Pass@K 率，它为这些验证策略的成功率建立了上界。

### 5.1 Weaver 缩小与前沿 LM 的差距

在表 1 中，我们评估 Weaver 与基线验证方法、前沿 LM 的首样本表现以及 Pass@100 指标。我们用 LlaMA 3.3 70B Instruct 为每个查询生成 $K=100$ 个回答。我们发现，Weaver 对多个验证器的加权集成使我们比多数投票高出 15.5%，并与 Pass@100 oracle 指标相差仅 4.2%。此外，Weaver 媲美前沿推理模型的表现——与 OpenAI 的 o3-mini（OpenAI, 2025）相差仅 0.5%——尽管我们用一个非推理模型做生成。

表 1：Weaver 优于基线验证方法并缩小与前沿 LM 的差距。

| | 方法 | 生成数 ($K$) | MATH500 | GPQA Diamond | MMLU College | MMLU Pro | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 基线 | 首个样本 | 1 | 78.0% | 42.9% | 82.6% | 69.9% | 68.4% |
| | 多数投票 | 100 | 83.0% | 47.4% | 84.1% | 74.4% | 72.2% |
| | RewardBench 最高分 RM（Tan et al., 2024；Lambert et al., 2024） | 100 | 78.2% | 49.7% | 86.0% | 77.0% | 72.7% |
| | RewardBench Top-10 RM 朴素集成（Lambert et al., 2024） | 100 | 75.4% | 41.3% | 88.1% | 71.4% | 69.1% |
| | 自验证（Zhao et al.） | 100 | 78.1% | 43.1% | 82.0% | 69.5% | 66.9% |
| | 多智能体验证（Lifshitz et al., 2025） | 100 | 81.3% | 47.8% | 84.1% | 72.6% | 71.6% |
| | **Weaver** | **100** | **93.4%** | **72.1%** | **94.9%** | **90.2%** | **87.7%** |
| 前沿方法 | GPT-4o（OpenAI, 2023） | 1 | 77.4% | 35.9% | 87.1% | 75.4% | 69.0% |
| | Claude 3.7 Sonnet（Anthropic, 2025） | 1 | 69.2% | 48.0% | 86.1% | 78.1% | 70.4% |
| | Llama 4 Maverick（Meta, 2025） | 1 | 87.6% | 68.9% | 91.1% | 81.0% | 82.2% |
| | o3-mini（OpenAI, 2025） | 1 | 94.4% | 74.0% | 92.2% | 86.0% | 86.7% |
| | Oracle 验证（Pass@100） | 100 | 98.6% | 81.0% | 96.0% | 92.0% | 91.9% |

### 5.2 Weaver 改进扩展的计算-准确率权衡

通过提议组合多个弱验证器而非单个，我们引入了又一条测试时扩展轴。本节研究用 Weaver 扩展验证与先前研究过的常见验证轴之间的交互，总结于表 2。

表 2：生成与验证模型的扩展维度

| 扩展维度 | 基座模型 | 验证器类型 | 图示 |
| --- | --- | --- | --- |
| 样本数：更多生成 | 基于温度的采样 | 多数投票、弱验证器、Top-K、Weaver | 图 3 |
| 模型规模：更大模型 | Llama 8B → 70B | RM-8B → RM-70B | 表 3 |
| 验证器数量：更多模型 | Llama 8B/70B | RM 与 LM 裁判 | 图 4 |
| 推理计算：生成/验证更多 FLOPs | 基于温度的采样 | 弱验证器 + Weaver | 图 5 |

（1）扩展候选生成：我们在图 3 中研究随重复样本数增加时验证方法的表现。基于先前工作（Christiano et al., 2017；Chen et al., 2021），随着回答数量增加，我们更可能看到正确回答（即 Pass@K 上升），因此在好的验证策略下也更有可能选出正确回答。然而，验证方式的差异转化为不同的扩展速率。我们评估 Weaver 与基线在 $K=2^{0}$ 到 $2^{10}$ 下的表现，并与 o3-mini 及 Pass@K 比较。在所有任务上，Weaver 在扩展生成数量时收益最大。Weaver 持续缩小与 oracle 上界（Pass@K）之间的生成-验证差距，而替代验证策略在少量生成后便进入平台期。这一效应在 GPQA 等困难任务上尤为明显。我们在 C.3 节详述图 3 中观察到的扩展趋势。

![Refer to caption](2506.18203v3/FP_and_Pass1_v2.png)

图 3：用 Weaver 扩展生成提升性能：增大 $K$ 并利用 Weaver 时生成-验证差距缩小，平均比替代验证方法高出 18.3%。

##### （2）扩展模型规模：

在表 3 中，我们研究把 Weaver 应用于较小模型（既用于验证器也用于生成回答）如何让我们匹敌较大模型的表现，实现弱到强验证。我们考虑一个 8B 设置——用 LlaMA 3.1 8B 生成回答并配 8B 验证器——并将其与 70B 设置（LlaMA 3.3 70B Instruct、8B-72B 验证器）以及 o3-mini 比较。我们看到 8B 规模的 Weaver 与 70B 规模的多数投票基线相差仅 1.6%，而 70B 的 Weaver 超过 o3-mini 1.0%，展示了弱到强验证现象。验证器校准细节见附录 C.5。

表 3：Weaver 缩小模型级别之间的差距：8B 与 70B 之间、70B 与前沿 LM 之间

| 生成器模型 | 验证器模型 | 聚合策略 | MATH | GPQA Diamond | MMLU College | MMLU Pro | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Llama 3.1 8B Instruct | 无 | 多数投票 | 69.0% | 30.5% | 72.7% | 56.4% | 57.2% |
| | 8B 及以下 | Weaver | 80.0% | 47.1% | 85.7% | 67.2% | 70.0% |
| | | $\Delta$（用 Weaver） | +11.0% | +16.6% | +13.0% | +10.2% | +12.8% |
| Llama 3.3 70B Instruct | 无 | 多数投票 | 83.0% | 44.9% | 84.1% | 74.4% | 71.6% |
| | 72B 及以下 | Weaver | 93.4% | 72.2% | 94.9% | 90.2% | 87.6% |
| | | $\Delta$（用 Weaver） | +10.4% | +27.3% | +10.8% | +15.8% | +16.0% |
| o3-mini | 无 | 首个样本 | 94.4% | 74.0% | 92.2% | 86.0% | 86.7% |

##### （3）扩展验证器数量：

扩展验证的两条轴是 (1) 使用的验证器数量与 (2) 从每个验证器采样的分数数量。图 4 展示了用朴素平均与 Weaver 集成 1 到 15 个验证器时表现的变化。验证器按单独准确率从高到低贪心加入。聚合更多验证器比 top-1 验证器最多提升 8.5%。如图 4 所示，在 Oracle Top-5 验证器与全部验证器两种配置下，Weaver 都持续优于朴素集成平均，在所有数据集上改进从 +2.4% 到 +10.1% 不等。收益在 GPQA Diamond（+10.1%）与 MMLU Pro（+5.1%）上尤为明显，证明 Weaver 通过学习的权重（而非简单平均）聚合验证器信号的效力。然而，随着加入更多模型，收益递减——这反映了经典的集成偏差-方差权衡：最初的改进来自方差缩减，而额外的验证器因在困难样本上相关的偏差而贡献冗余信号（Abe et al., 2024）。我们在附录 C.7 中比较了 Weaver 二元变换之外的替代分数校准策略，发现默认的二值化带来最强的下游选择表现。我们还在附录 C.5 中探索了通过提示调优或温度变化来扩展每个验证器的分数数量。虽然这带来适度改进，增加验证器数量仍是更有效的策略。话虽如此，两种方法是互补的，可以结合以获得进一步收益。

图 4：Weaver 在 Oracle Top-5 验证器与全部验证器配置下均优于朴素集成：结果展示 Oracle Top-5 验证器（用真值选出的数据集上表现最高的验证器）与全部验证器（所有可用验证器）的 Weaver 集成与朴素集成。Weaver 持续优于朴素集成平均，改进从 +2.4% 到 +10.1%。

![Refer to caption](2506.18203v3/Weaver_Scaling_Laws_fig.png)

图 5：Weaver 改进准确率-计算性能权衡。不同验证策略下成功率（%）随每查询总推理计算（生成与验证计算，对数标度）的变化。每个点代表不同的候选生成数（从 $2^{0}$ 到 $2^{7}$）。Weaver 取得最高准确率，虽然比多数投票需要更多计算，但展示了持续的扩展收益；而 Weaver Distilled 以 97.3% 的计算节省保留了 Weaver 大部分性能增益，并相对基线方法有显著的准确率改进。

##### （4）扩展测试时计算：

我们研究在验证与重复生成两者使用的总计算下表现如何扩展。图 5 展示了不同生成-验证系统的推理时计算与成功率之间的关系。对每种方法，我们把生成数从 1 指数扩展到 100，并绘制生成与验证合计所需推理计算对成功率的曲线。注意图 5 与图 3 不同，因为多数投票需要 0 次验证推理调用，而 Weaver 需要为弱验证器做 30 次以上调用。我们发现 Weaver 取得最高的最大成功率；值得注意的是，多数投票在每查询约 $2^{2}$ 到 $2^{3}$ ExaFLOPs 处进入平台期，而 Weaver 持续扩展直到 512 ExaFLOPs。然而，Weaver 所需的额外计算可能过高。我们在下一节探索如何在保留 Weaver 表现的同时降低这一计算负担。

## 6 Weaver 蒸馏：改进推理时的验证效率

我们探索把一个较小的 LM 微调为任务专属验证器的蒸馏策略。具体而言，我们训练交叉编码器；输入是拼接的查询-回答对，输出是 Weaver 由弱监督生成的伪标签，即 $\Pr(y_{ij}=1|s_{ij1},\dots,s_{ijm})$（见第 4 节）。模型方面，我们选择了 ModernBERT-Large（396M）（Warner et al., 2024）。更多细节见附录 C.6。

图 6：把 Weaver 蒸馏到 400M 交叉编码器几乎完全捕获 Weaver 的性能，带来 99.97% 的计算节省。∗我们在 80:20 划分上训练/评估。

图 6 展示了 Weaver 在 Llama-70B 生成上与交叉编码器在 GPQA Diamond 上的表现。跨任务地，我们发现蒸馏出的交叉编码器能捕获 Weaver 98.2% 的性能。用全部验证器运行 Weaver 时，每个查询的 100 个样本集合花费 35.35 exaFLOPs。运行一个 400M 交叉编码器评估 100 个样本花费 1.01 exaFLOPs，把计算成本降低超过三个数量级，节省了原本运行 70B 验证器所需 FLOPs 的 99.97%。我们还在只比生成回答多出 0.57% 推理成本的同时，比多数投票高出 23.2%。我们在图 22（C.6 节）中看到其他数据集的类似结果。

这些结果表明，通过蒸馏，我们可以捕获 Weaver 所用弱验证器的组合优势，并部署仅使用生成所用参数一小部分的、可泛化的轻量交叉编码器。这大大降低了我们的硬件约束：无需为每个 70B 验证器配备一个 8-GPU 节点（即 80GB 显存的 Nvidia H200），我们的交叉编码器只需一块 32GB 显存的 A100 GPU。

## 7 讨论

围绕 Weaver 仍有若干研究方向待探索：

1. 专门验证器研发：我们的工作凸显了不同弱验证器类别在各任务领域有效性的差异。未来研究应考察为特定任务定制的专门验证器架构，例如面向数值问题的更强数学推理能力（Yang et al.），或面向编程任务的更好代码执行模拟（Jain et al., 2024；Quan et al., 2025）。
2. 数据集分布：对特别困难的数据集（如 AIMO 2024），Weaver 难以选出正确答案，因为相对其他数据集正确回答太少（表 13；表 14）。通过扩展生成回答数量，我们能靠增加正确回答的绝对数量来提升表现（图 3），但对这些更难的任务，改进的生成技术、验证器打分与聚合技术能帮助我们更好地缩小与 $Pass@K$ 的差距。
3. 用 Weaver 做 RLHF：有了 Weaver 生成的预测，我们可以改进推理与数学上用于 RLHF 的标签质量，超越单个验证器。先前工作已探索面向 RLHF 的奖励模型集成方法，最小化表现差的 RM、同时最大化准确 RM 的互补优势（Wang et al., 2025；Eisenstein et al., 2023）。微调生成模型可以进一步改进 Weaver 的准确率-计算权衡，超越只蒸馏轻量验证器（第 6 节）的做法，改进正/负生成比例，从而使验证对 Weaver 模型而言成为更轻松的任务。
4. 多模态验证：把 Weaver 扩展到涉及图像、音频或视频的多模态任务将拓宽其适用性，但也带来跨模态验证的新挑战（Phan et al., 2025；Wang et al., 2020）。需要研究如何跨不同数据类型有效组合验证信号。

## 8 结论

本文提出 Weaver，一个通过有效验证策略应对扩展测试时计算这一根本挑战的框架。我们的贡献在三个关键维度上推进了认知。第一，我们确立了弱验证器的加权聚合在推理与数学任务上显著优于单个验证器与多数投票，加权聚合在我们探索的所有任务上平均超出多数投票 12.3%（表 1；图 2）。第二，我们发展了一种用弱监督无监督估计验证器准确率的有原则方法，无需在昂贵的真值标注上微调即可实现有效的集成加权。这使我们能为 8B 模型缩小生成-验证差距 12.8%、为 70B 模型缩小 16.0%（表 3）。借助 70B 模型上的 Weaver，我们在所探索任务上平均略微超过 OpenAI o3-mini 等前沿闭源模型（87.7% 对 86.7%）（表 1）。第三，我们通过把 Weaver 蒸馏为轻量 400M 参数交叉编码器改进了准确率-计算权衡。这些蒸馏模型保留 Weaver 98.2% 的性能，同时减少 99.97% 的推理计算（第 6 节）。这实现了高吞吐、低成本的验证而不牺牲准确率，并证明无需反复查询大模型也能实现可扩展的验证。这些发现表明，策略性地组合与蒸馏弱验证器能够实现可扩展、标签高效且计算高效的验证——为更好的数据过滤、模型对齐与推理时决策铺平道路，而无需额外训练基座生成模型。

## 9 致谢

我们感谢 Hazy Lab、Linderman Lab 与 Scaling Intelligence Lab 的成员在论文撰写期间的建设性反馈。特别感谢 Daniel Biderman、Bradley Brown、Ryan Ehrlich、Sabri Eyuboglu、Anna Goldie、Neel Guha、Simon Guo、Jordan Juravsky、Hermann Kumbong、Jerry Liu、Avanika Narayan、Anne Ouyang、Benjamin Spector、Shayan Talaei、Benjamin Viggiano 与 Michael Zhang。我们还感谢 Marlowe 与 Together AI 提供使我们的实验得以进行的计算资源。

我们衷心感谢以下支持：NIH（No. U54EB020405，Mobilize）；NSF（Nos. CCF2247015，Hardware-Aware；CCF1763315，Beyond Sparsity；CCF1563078，Volume to Velocity；1937301，RTML）；US DEVCOM ARL（Nos. W911NF-23-2-0184，Long-context；W911NF-21-2-0251，Interactive Human-AI Teaming）；ONR（No. N000142312633，Deep Signal Processing）；Stanford HAI（No. 247183）；Google DeepMind；Google Research；Google Cloud；NXP；Xilinx；LETI-CEA；Intel；IBM；Microsoft；NEC；Toshiba；TSMC；ARM；Hitachi；BASF；Accenture；Ericsson；Qualcomm；Analog Devices；Salesforce；Total；HAI-GCP Cloud Credits for Research 计划；斯坦福数据科学计划（SDSI）；斯坦福 DAWN 项目成员：Meta、Google 和 VMWare；以及斯坦福 SEAMS 项目成员：IBM 和 Felicis。美国政府被授权出于政府目的复制和分发重印本，尽管其上可能有任何版权标注。本材料中表达的观点、发现、结论或建议均为作者个人观点，不一定反映 NIH、ONR 或美国政府的观点、政策或背书，无论是明示还是暗示。

## 参考文献

- (1)

  Taiga Abe, E. Kelly Buchanan, Geoff Pleiss, and John Patrick Cunningham.
  Pathologies of predictive diversity in deep ensembles.
  Transactions on Machine Learning Research, 2024.
  Featured Certification.
- (2)

  Anthropic.
  Claude 3.7 sonnet and claude code, February 2025.
  Announcement blog post, 5 min read.
- (3)

  Simran Arora, Avanika Narayan, Mayee F. Chen, Laurel Orr, Neel Guha, Kush Bhatia, Ines Chami, Frederic Sala, and Christopher Ré.
  Ask me anything: A simple strategy for prompting language models, 2022.
- (4)

  Amanda Askell, Yuntao Bai, Anna Chen, Dawn Drain, Deep Ganguli, Tom Henighan, Andy Jones, Nicholas Joseph, Ben Mann, Nova DasSarma, et al.
  A General Language Assistant as a Laboratory for Alignment.
  ArXiv Preprint arXiv:2112.00861, 2021.
- (5)

  Ralph Allan Bradley and Milton E Terry.
  Rank Analysis of Incomplete Block Designs: I. The Method of Paired Comparisons.
  Biometrika, 39(3/4):324–345, 1952.
- (6)

  Bradley Brown, Jordan Juravsky, Ryan Ehrlich, Ronald Clark, Quoc V. Le, Christopher Ré, and Azalia Mirhoseini.
  Large language monkeys: Scaling inference compute with repeated sampling, 2024.
- (7)

  Zhe Cao, Tao Qin, Tie-Yan Liu, Ming-Feng Tsai, and Hang Li.
  Learning to rank: from pairwise approach to listwise approach.
  In Proceedings of the 24th international conference on Machine learning, pages 129–136, 2007.
- (8)

  Shreyas Chaudhari, Pranjal Aggarwal, Vishvak Murahari, Tanmay Rajpurohit, Ashwin Kalyan, Karthik Narasimhan, Ameet Deshpande, and Bruno Castro da Silva.
  RLHF Deciphered: A Critical Analysis of Reinforcement Learning from Human Feedback for LLMs, 2024.
- (9)

  Guiming Hardy Chen, Shunian Chen, Ziche Liu, Feng Jiang, and Benyou Wang.
  Humans or LLMs as the Judge? A Study on Judgement Bias.
  ArXiv Preprint arXiv:2402.10669, 2024.
- (10)

  Jiefeng Chen, Jie Ren, Xinyun Chen, Chengrun Yang, Ruoxi Sun, and Sercan Ö Arık.
  Sets: Leveraging self-verification and self-correction for improved test-time scaling.
  arXiv preprint arXiv:2501.19306, 2025.
- (11)

  Lingjiao Chen, Jared Quincy Davis, Boris Hanin, Peter Bailis, Ion Stoica, Matei Zaharia, and James Zou.
  Are more llm calls all you need? towards scaling laws of compound inference systems.
  arXiv preprint arXiv:2403.02419, 2024.
- (12)

  Lingjiao Chen, Jared Quincy Davis, Boris Hanin, Peter Bailis, Ion Stoica, Matei Zaharia, and James Zou.
  Are more llm calls all you need? towards scaling laws of compound inference systems, 2024.
- (13)

  Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba.
  Evaluating large language models trained on code, 2021.
- (14)

  Mayee F. Chen, Daniel Y. Fu, Dyah Adila, Michael Zhang, Frederic Sala, Kayvon Fatahalian, and Christopher Ré.
  Shoring up the foundations: fusing model embeddings and weak supervision.
  In James Cussens and Kun Zhang, editors, Proceedings of the Thirty-Eighth Conference on Uncertainty in Artificial Intelligence, volume 180 of Proceedings of Machine Learning Research, pages 357–367. PMLR, 01–05 Aug 2022.
- (15)

  Wei-Lin Chiang, Lianmin Zheng, Ying Sheng, Anastasios Nikolas Angelopoulos, Tianle Li, Dacheng Li, Hao Zhang, Banghua Zhu, Michael Jordan, Joseph E. Gonzalez, and Ion Stoica.
  Chatbot arena: An open platform for evaluating llms by human preference, 2024.
- (16)

  Paul F Christiano, Jan Leike, Tom Brown, Miljan Martic, Shane Legg, and Dario Amodei.
  Deep Reinforcement Learning from Human Preferences.
  Advances in Neural Information Processing Systems, 30, 2017.
- (17)

  Elizabeth Clark, Tal August, Sofia Serrano, Nikita Haduong, Suchin Gururangan, and Noah A. Smith.
  All that’s ’human’ is not gold: Evaluating human evaluation of generated text, 2021.
- (18)

  Ganqu Cui, Lifan Yuan, Zefan Wang, Hanbin Wang, Wendi Li, Bingxiang He, Yuchen Fan, Tianyu Yu, Qixin Xu, Weize Chen, et al.
  Process reinforcement through implicit rewards.
  arXiv preprint arXiv:2502.01456, 2025.
- (19)

  Nicolai Dorka.
  Quantile regression for distributional reward models in rlhf.
  arXiv preprint arXiv:2409.10164, 2024.
- (20)

  Yann Dubois, Balázs Galambosi, Percy Liang, and Tatsunori B Hashimoto.
  Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators.
  ArXiv Preprint arXiv:2404.04475, 2024.
- (21)

  Yann Dubois, Chen Xuechen Li, Rohan Taori, Tianyi Zhang, Ishaan Gulrajani, Jimmy Ba, Carlos Guestrin, Percy S Liang, and Tatsunori B Hashimoto.
  AlpacaFarm: A Simulation Framework for Methods that Learn from Human Feedback.
  Advances in Neural Information Processing Systems, 36, 2024.
- (22)

  Jacob Eisenstein, Jonathan Berant, Chirag Nagpal, Alekh Agarwal, Ahmad Beirami, Alexander Nicholas D’Amour, Krishnamurthy Dj Dvijotham, Katherine A Heller, Stephen Robert Pfohl, and Deepak Ramachandran.
  Reward Model Underspecification in Language Model Alignment.
  In NeurIPS 2023 Workshop on Distribution Shifts: New Frontiers with Foundation Models, 2023.
- (23)

  Jacob Eisenstein, Chirag Nagpal, Alekh Agarwal, Ahmad Beirami, Alex D’Amour, DJ Dvijotham, Adam Fisch, Katherine Heller, Stephen Pfohl, Deepak Ramachandran, et al.
  Helping or herding? reward model ensembles mitigate but do not eliminate reward hacking.
  arXiv preprint arXiv:2312.09244, 2023.
- (24)

  Shahul Es, Jithin James, Luis Espinosa-Anke, and Steven Schockaert.
  RAGAs: Automated Evaluation of Retrieval Augmented Generation.
  ArXiv Preprint arXiv:2309.15217, 2023.
- (25)

  Long Phan et al.
  Humanity’s last exam, 2025.
- (26)

  Daniel Fu, Mayee Chen, Frederic Sala, Sarah Hooper, Kayvon Fatahalian, and Christopher Ré.
  Fast and three-rious: Speeding up weak supervision with triplet methods.
  In International conference on machine learning, pages 3280–3291. PMLR, 2020.
- (27)

  Jinlan Fu, See-Kiong Ng, Zhengbao Jiang, and Pengfei Liu.
  GPTScore: Evaluate as You Desire.
  Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), 2023.
- (28)

  Neel Guha, Mayee F Chen, Trevor Chow, Ishan S Khare, and Christopher Re.
  Smoothie: Label free language model routing.
  In The Thirty-eighth Annual Conference on Neural Information Processing Systems, 2024.
- (29)

  Alastair R Hall.
  Generalized method of moments.
  A companion to theoretical econometrics, pages 230–255, 2003.
- (30)

  HazyResearch.
  metal.
  <https://https://github.com/HazyResearch/metal>, 2018.
- (31)

  Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt.
  Measuring mathematical problem solving with the math dataset.
  arXiv preprint arXiv:2103.03874, 2021.
- (32)

  Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, et al.
  Training compute-optimal large language models.
  arXiv preprint arXiv:2203.15556, 2022.
- (33)

  Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, Tom Hennigan, Eric Noland, Katie Millican, George van den Driessche, Bogdan Damoc, Aurelia Guy, Simon Osindero, Karen Simonyan, Erich Elsen, Jack W. Rae, Oriol Vinyals, and Laurent Sifre.
  Training compute-optimal large language models, 2022.
- (34)

  Tom Hosking, Phil Blunsom, and Max Bartolo.
  Human feedback is not gold standard, 2024.
- (35)

  Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica.
  Livecodebench: Holistic and contamination free evaluation of large language models for code, 2024.
- (36)

  Nimit Kalra and Leonard Tang.
  Verdict: A library for scaling judge-time compute, 2025.
- (37)

  Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B. Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei.
  Scaling laws for neural language models, 2020.
- (38)

  Marzena Karpinska, Nader Akoury, and Mohit Iyyer.
  The perils of using mechanical turk to evaluate open-ended text generation, 2021.
- (39)

  Omar Khattab, Arnav Singhvi, Paridhi Maheshwari, Zhiyuan Zhang, Keshav Santhanam, Sri Vardhamanan, Saiful Haq, Ashutosh Sharma, Thomas T. Joshi, Hanna Moazam, Heather Miller, Matei Zaharia, and Christopher Potts.
  Dspy: Compiling declarative language model calls into self-improving pipelines.
  arXiv preprint arXiv:2310.03714, 2023.
- (40)

  Diederik P. Kingma and Jimmy Ba.
  Adam: A method for stochastic optimization, 2017.
- (41)

  Jan Hendrik Kirchner, Yining Chen, Harri Edwards, Jan Leike, Nat McAleese, and Yuri Burda.
  Prover-verifier games improve legibility of llm outputs.
  arXiv preprint arXiv:2407.13692, 2024.
- (42)

  Nathan Lambert and Roberto Calandra.
  The alignment ceiling: Objective mismatch in reinforcement learning from human feedback.
  ArXiv Preprint arXiv:2311.00168, 2023.
- (43)

  Nathan Lambert, Valentina Pyatkin, Jacob Morrison, LJ Miranda, Bill Yuchen Lin, Khyathi Chandu, Nouha Dziri, Sachin Kumar, Tom Zick, Yejin Choi, Noah A. Smith, and Hannaneh Hajishirzi.
  RewardBench: Evaluating Reward Models for Language Modeling, 2024.
- (44)

  Xuechen Li, Tianyi Zhang, Yann Dubois, Rohan Taori, Ishaan Gulrajani, Carlos Guestrin, Percy Liang, and Tatsunori B. Hashimoto.
  Alpacaeval: An automatic evaluator of instruction-following models.
  <https://github.com/tatsu-lab/alpaca_eval>, 2023.
- (45)

  Shalev Lifshitz, Sheila A. McIlraith, and Yilun Du.
  Multi-agent verification: Scaling test-time compute with multiple verifiers, 2025.
- (46)

  Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe.
  Let’s verify step by step, 2023.
- (47)

  Chris Yuhao Liu and Liang Zeng.
  Skywork Reward Model Series.
  <https://huggingface.co/Skywork>, September 2024.
- (48)

  Chris Yuhao Liu, Liang Zeng, Jiacai Liu, Rui Yan, Jujie He, Chaojie Wang, Shuicheng Yan, Yang Liu, and Yahui Zhou.
  Skywork-reward: Bag of tricks for reward modeling in llms.
  arXiv preprint arXiv:2410.18451, 2024.
- (49)

  Runze Liu, Junqi Gao, Jian Zhao, Kaiyan Zhang, Xiu Li, Biqing Qi, Wanli Ouyang, and Bowen Zhou.
  Can 1b llm surpass 405b llm? rethinking compute-optimal test-time scaling, 2025.
- (50)

  Runze Liu, Junqi Gao, Jian Zhao, Kaiyan Zhang, Xiu Li, Biqing Qi, Wanli Ouyang, and Bowen Zhou.
  Can 1b llm surpass 405b llm? rethinking compute-optimal test-time scaling.
  arXiv preprint arXiv:2502.06703, 2025.
- (51)

  Yang Liu, Dan Iter, Yichong Xu, Shuohang Wang, Ruochen Xu, and Chenguang Zhu.
  G-eval: Nlg evaluation using gpt-4 with better human alignment.
  ArXiv Preprint arXiv:2303.16634, 2023.
- (52)

  Meta.
  The Llama 4 herd: The beginning of a new era of natively multimodal AI innovation, 4 2025.
  Accessed: 2025-05-12.
- (53)

  Xiaoyu Tan Minghao Yang, Chao Qu.
  Inf-orm-llama3.1-70b, 2024.
- (54)

  OpenAI.
  GPT-4 Technical Report.
  ArXiv Preprint arXiv:2303.08774, 2023.
- (55)

  OpenAI.
  Openai o3-mini system card.
  Technical report, OpenAI, January 2025.
  Publication.
- (56)

  Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al.
  Training language models to follow instructions with human feedback.
  Advances in Neural Information Processing Systems, 35:27730–27744, 2022.
- (57)

  Qian Pan, Zahra Ashktorab, Michael Desmond, Martín Santillán Cooper, James Johnson, Rahul Nair, Elizabeth Daly, and Werner Geyer.
  Human-Centered Design Recommendations for LLM-as-a-judge.
  In Proceedings of the 1st Human-Centered Large Language Modeling Workshop, pages 16–29, 2024.
- (58)

  Isha Puri, Shivchander Sudalairaj, Guangxuan Xu, Kai Xu, and Akash Srivastava.
  A probabilistic inference approach to inference-time scaling of llms using particle-based monte carlo methods, 2025.
- (59)

  Shanghaoran Quan, Jiaxi Yang, Bowen Yu, Bo Zheng, Dayiheng Liu, An Yang, Xuancheng Ren, Bofei Gao, Yibo Miao, Yunlong Feng, Zekun Wang, Jian Yang, Zeyu Cui, Yang Fan, Yichang Zhang, Binyuan Hui, and Junyang Lin.
  Codeelo: Benchmarking competition-level code generation of llms with human-comparable elo ratings, 2025.
- (60)

  Alexander Ratner, Stephen H Bach, Henry Ehrenberg, Jason Fries, Sen Wu, and Christopher Ré.
  Snorkel: rapid training data creation with weak supervision.
  The VLDB Journal, 29(2):709–730, 2020.
- (61)

  Alexander Ratner, Braden Hancock, Jared Dunnmon, Frederic Sala, Shreyash Pandey, and Christopher Ré.
  Training complex models with multi-task weak supervision.
  In Proceedings of the AAAI Conference on Artificial Intelligence, volume 33, pages 4763–4771, 2019.
- (62)

  Alexander J Ratner, Christopher M De Sa, Sen Wu, Daniel Selsam, and Christopher Ré.
  Data programming: Creating large training sets, quickly.
  Advances in neural information processing systems, 29, 2016.
- (63)

  Selvan Sunitha Ravi, Bartosz Mielczarek, Anand Kannappan, Douwe Kiela, and Rebecca Qian.
  Lynx: An Open Source Hallucination Evaluation Model, 2024.
- (64)

  Nils Reimers and Iryna Gurevych.
  Making monolingual sentence embeddings multilingual using knowledge distillation.
  In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, 11 2020.
- (65)

  David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian Michael, and Samuel R. Bowman.
  GPQA: A graduate-level google-proof q&a benchmark.
  In First Conference on Language Modeling, 2024.
- (66)

  Saharon Rosset, Ji Zhu, and Trevor Hastie.
  Margin maximizing loss functions.
  Advances in neural information processing systems, 16, 2003.
- (67)

  Jon Saad-Falcon, Omar Khattab, Christopher Potts, and Matei Zaharia.
  ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems.
  ArXiv Preprint arXiv:2311.09476, 2023.
- (68)

  Jon Saad-Falcon, Adrian Gamarra Lafuente, Shlok Natarajan, Nahum Maru, Hristo Todorov, Etash Guha, E Kelly Buchanan, Mayee Chen, Neel Guha, Christopher Ré, and Azalia Mirhoseini.
  Archon: An architecture search framework for inference-time techniques.
  arXiv preprint arXiv:2409.15254, 2024.
- (69)

  Jon Saad-Falcon, Rajan Vivek, William Berrios, Nandita Shankar Naik, Matija Franklin, Bertie Vidgen, Amanpreet Singh, Douwe Kiela, and Shikib Mehri.
  Lmunit: Fine-grained evaluation with natural language unit tests, 2024.
- (70)

  Robert E Schapire.
  Explaining adaboost.
  In Empirical inference: festschrift in honor of vladimir N. Vapnik, pages 37–52. Springer, 2013.
- (71)

  Changho Shin, Winfred Li, Harit Vishwakarma, Nicholas Roberts, and Frederic Sala.
  Universalizing weak supervision.
  arXiv preprint arXiv:2112.03865, 2021.
- (72)

  Prasann Singhal, Tanya Goyal, Jiacheng Xu, and Greg Durrett.
  A long way to go: Investigating length correlations in rlhf.
  ArXiv Preprint arXiv:2310.03716, 2023.
- (73)

  Nishad Singhi, Hritik Bansal, Arian Hosseini, Aditya Grover, Kai-Wei Chang, Marcus Rohrbach, and Anna Rohrbach.
  When to solve, when to verify: Compute-optimal problem solving and generative verification for llm reasoning, 2025.
- (74)

  Nishad Singhi, Hritik Bansal, Arian Hosseini, Aditya Grover, Kai-Wei Chang, Marcus Rohrbach, and Anna Rohrbach.
  When to solve, when to verify: Compute-optimal problem solving and generative verification for llm reasoning, 2025.
- (75)

  Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar.
  Scaling llm test-time compute optimally can be more effective than scaling model parameters, 2024.
- (76)

  Mingyang Song, Zhaochen Su, Xiaoye Qu, Jiawei Zhou, and Yu Cheng.
  Prmbench: A fine-grained and challenging benchmark for process-level reward models, 2025.
- (77)

  Yuda Song, Hanlin Zhang, Carson Eisenach, Sham Kakade, Dean Foster, and Udaya Ghai.
  Mind the gap: Examining the self-improvement capabilities of large language models, 2025.
- (78)

  Benedikt Stroebl, Sayash Kapoor, and Arvind Narayanan.
  Inference scaling flaws: The limits of llm resampling with imperfect verifiers, 2024.
- (79)

  Mirac Suzgun, Nathan Scales, Nathanael Schärli, Sebastian Gehrmann, Yi Tay, Hyung Won Chung, Aakanksha Chowdhery, Quoc V. Le, Ed H. Chi, Denny Zhou, and Jason Wei.
  Challenging big-bench tasks and whether chain-of-thought can solve them, 2022.
- (80)

  Liyan Tang, Philippe Laban, and Greg Durrett.
  MiniCheck: Efficient Fact-Checking of LLMs on Grounding Documents, 2024.
- (81)

  Pat Verga, Sebastian Hofstatter, Sophia Althammer, Yixuan Su, Aleksandra Piktus, Arkady Arkhangorodsky, Minjie Xu, Naomi White, and Patrick Lewis.
  Replacing judges with juries: Evaluating llm generations with a panel of diverse models, 2024.
- (82)

  Harit Vishwakarma and Frederic Sala.
  Lifting weak supervision to structured prediction.
  Advances in Neural Information Processing Systems, 35:37563–37574, 2022.
- (83)

  Binghai Wang, Rui Zheng, Lu Chen, Yan Liu, Shihan Dou, Caishuang Huang, Wei Shen, Senjie Jin, Enyu Zhou, Chenyu Shi, Songyang Gao, Nuo Xu, Yuhao Zhou, Xiaoran Fan, Zhiheng Xi, Jun Zhao, Xiao Wang, Tao Ji, Hang Yan, Lixing Shen, Zhan Chen, Tao Gui, Qi Zhang, Xipeng Qiu, Xuanjing Huang, Zuxuan Wu, and Yu-Gang Jiang.
  Secrets of RLHF in Large Language Models Part II: Reward Modeling, 2024.
- (84)

  Haoxiang Wang, Wei Xiong, Tengyang Xie, Han Zhao, and Tong Zhang.
  Interpretable preferences via multi-objective reward modeling and mixture-of-experts.
  ArXiv Preprint arXiv:2406.12845, 2024.
- (85)

  Jiaan Wang, Yunlong Liang, Fandong Meng, Zengkui Sun, Haoxiang Shi, Zhixu Li, Jinan Xu, Jianfeng Qu, and Jie Zhou.
  Is ChatGPT a good NLG Evaluator? A Preliminary Study.
  ArXiv Preprint arXiv:2303.04048, 2023.
- (86)

  Junlin Wang, Roy Xie, Shang Zhu, Jue Wang, Ben Athiwaratkun, Bhuwan Dhingra, Shuaiwen Leon Song, Ce Zhang, and James Zou.
  Improving model alignment through collective intelligence of open-source llms, 2025.
- (87)

  Xin Wang, Jiawei Wu, Junkun Chen, Lei Li, Yuan-Fang Wang, and William Yang Wang.
  Vatex: A large-scale, high-quality multilingual dataset for video-and-language research, 2020.
- (88)

  Yubo Wang, Xueguang Ma, Ge Zhang, Yuansheng Ni, Abhranil Chandra, Shiguang Guo, Weiming Ren, Aaran Arulraj, Xuan He, Ziyan Jiang, et al.
  Mmlu-pro: A more robust and challenging multi-task language understanding benchmark.
  arXiv preprint arXiv:2406.01574, 2024.
- (89)

  Zhilin Wang, Yi Dong, Jiaqi Zeng, Virginia Adams, Makesh Narsimhan Sreedhar, Daniel Egert, Olivier Delalleau, Jane Polak Scowcroft, Neel Kant, Aidan Swope, and Oleksii Kuchaiev.
  HelpSteer: Multi-Attribute Helpfulness Dataset for SteerLM, 2023.
- (90)

  Zihao Wang, Chirag Nagpal, Jonathan Berant, Jacob Eisenstein, Alex D’Amour, Sanmi Koyejo, and Victor Veitch.
  Transforming and combining rewards for aligning large language models.
  arXiv preprint arXiv:2402.00742, 2024.
- (91)

  Benjamin Warner, Antoine Chaffin, Benjamin Clavié, Orion Weller, Oskar Hallström, Said Taghadouini, Alexis Gallagher, Raja Biswas, Faisal Ladhak, Tom Aarsen, Nathan Cooper, Griffin Adams, Jeremy Howard, and Iacopo Poli.
  Smarter, better, faster, longer: A modern bidirectional encoder for fast, memory efficient, and long context finetuning and inference, 2024.
- (92)

  Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed Chi, Quoc Le, and Denny Zhou.
  Chain-of-thought prompting elicits reasoning in large language models, 2023.
- (93)

  Tengyu Xu, Eryk Helenowski, Karthik Abinav Sankararaman, Di Jin, Kaiyan Peng, Eric Han, Shaoliang Nie, Chen Zhu, Hejia Zhang, Wenxuan Zhou, Zhouhao Zeng, Yun He, Karishma Mandyam, Arya Talabzadeh, Madian Khabsa, Gabriel Cohen, Yuandong Tian, Hao Ma, Sinong Wang, and Han Fang.
  The perfect blend: Redefining rlhf with mixture of judges, 2024.
- (94)

  An Yang, Beichen Zhang, Binyuan Hui, Bofei Gao, Bowen Yu, Chengpeng Li, Dayiheng Liu, Jianhong Tu, Jingren Zhou, Junyang Lin, Keming Lu, Mingfeng Xue, Runji Lin, Tianyu Liu, Xingzhang Ren, and Zhenru Zhang.
  Qwen2.5-math technical report: Toward mathematical expert model via self-improvement.
  arXiv preprint arXiv:2409.12122, 2024.
- (95)

  LU Ying et al.
  Decision tree methods: applications for classification and prediction.
  Shanghai archives of psychiatry, 27(2):130, 2015.
- (96)

  Lifan Yuan, Wendi Li, Huayu Chen, Ganqu Cui, Ning Ding, Kaiyan Zhang, Bowen Zhou, Zhiyuan Liu, and Hao Peng.
  Free process rewards without process labels.
  arXiv preprint arXiv:2412.01981, 2024.
- (97)

  Lunjun Zhang, Arian Hosseini, Hritik Bansal, Mehran Kazemi, Aviral Kumar, and Rishabh Agarwal.
  Generative Verifiers: Reward Modeling as Next-Token Prediction, 2024.
- (98)

  Eric Zhao, Pranjal Awasthi, and Sreenivas Gollapudi.
  Sample, scrutinize and scale: Effective inference-time search by scaling verification.
  arXiv preprint arXiv:2502.01839, 2025.
- (99)

  Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
  Minif2f: a cross-system benchmark for formal olympiad-level mathematics, 2022.
- (100)

  Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric. P Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica.
  Judging llm-as-a-judge with mt-bench and chatbot arena, 2023.
- (101)

  Lianmin Zheng, Dacheng Xu, Jiajun Dong, Andy Zeng, Shuo Xie, Eric P Xing, and Percy Liang.
  Evaluation Biases for Large Language Models.
  ArXiv Preprint arXiv:2305.17926, 2023.
## 附录 A 目录

1. Weaver 方法论（附录 B）
   1. 已知难度的离散弱监督模型（附录 B.1）
   2. 把弱监督适配到验证设置（附录 B.2）
   3. 过滤低质量验证器（附录 B.2.3）
   4. 适配方法（附录 B.3）
   5. 按难度聚类以改进 Weaver（附录 B.4）
2. 实验（附录 C）
   1. 模型与数据集（附录 C.1）
   2. 验证基线（附录 C.2）
   3. Weaver 的扩展趋势（附录 C.3）
   4. 扩展候选生成（附录 C.4）
   5. 扩展验证器数量（附录 C.5）
   6. Weaver 蒸馏（附录 C.6）
   7. 单个验证器优化（附录 C.7）
3. 杂项（附录 D）
   1. 计算需求（附录 D.1）

## 附录 B Weaver 方法论

### B.1 弱监督模型

我们可以在回答正确性 $y$ 与二元验证器输出 $\bar{s}$ 上构造一个数据生成模型。模型定义为：

$$
\text{回答正确性：}\quad y_{ij}\sim\text{Bernoulli}(\pi)\;\forall i\in[n],j\in[K],
$$

$$
\text{验证器分数：}\quad \bar{s}_{ijk}\mid y_{ij}\sim\begin{cases}\text{Bernoulli}(w_{k,1}),&\text{若 }y_{ij}=1,\\ \text{Bernoulli}(1-w_{k,0}),&\text{若 }y_{ij}=0,\end{cases}\;\forall i\in[n],j\in[K],k\in[m]
$$

其中：

- $\pi$ 是回答正确的概率。
- $w_{k,1}$ 是验证器 $k$ 的真阳性率（TPR），$w_{k,0}$ 是真阴性率（TNR），我们称之为验证器的准确率参数。

这里每个验证器 $k$ 输出一个二元分数 $\bar{s}_{ijk}\in\{0,1\}$，被假定为回答 $y_{ij}$ 是否正确的含噪声指示。验证器二元输出 $X_{ijk}\in\{0,1\}$ 的似然为：

$$
\Pr(S_{k}=\bar{s}_{ijk}\mid Y=y_{ij})=\begin{cases}w_{k,1},&\text{若 }y_{ij}=1\text{ 且 }\bar{s}_{ijk}=1,\\ 1-w_{k,1},&\text{若 }y_{ij}=1\text{ 且 }\bar{s}_{ijk}=0,\\ w_{k,0},&\text{若 }y_{ij}=0\text{ 且 }\bar{s}_{ijk}=0,\\ 1-w_{k,0},&\text{若 }y_{ij}=0\text{ 且 }\bar{s}_{ijk}=1.\end{cases}
$$

我们希望基于多个验证器的评估 $\bar{s}_{ij}=\{\bar{s}_{ij1},\bar{s}_{ij2},\dots,\bar{s}_{ijm}\}$ 来估计回答 $y_{ij}\in\{0,1\}$ 的正确性。应用贝叶斯法则，得：

$$
\Pr(y_{ij}=1\mid S=\bar{s}_{ij})=\frac{\Pr(S=\bar{s}_{ij}\mid y_{ij}=1)\Pr(y_{ij}=1)}{\Pr(\bar{s}_{ij})} \tag{6}
$$

其中 $\Pr(\bar{s}_{ij})=\sum_{y^{\prime}\in\{0,1\}}\Pr(\bar{s}_{ij}\mid y_{ij}=y^{\prime})\Pr(y_{ij}=y^{\prime})$。

式 (6) 需要计算完整的条件似然：

$$
\Pr(S=\bar{s}_{ij}\mid y_{ij})=\Pr(S_{1}=\bar{s}_{ij1},S_{2}=\bar{s}_{ij2},\dots,S_{m}=\bar{s}_{ijm}\mid y_{ij}),
$$

这是 $m$ 个二元随机变量上的联合分布。由于每个验证器 $S_{k}\in\{0,1\}$ 是二元的，$S\in\{0,1\}^{m}$ 有 $2^{m}$ 种可能的验证器输出配置。这导致构造分布 $\Pr(S=\bar{s}_{ij}\mid y_{ij})$ 时每个类标签有 $2^{m}-1$ 个自由参数。

##### 条件独立假设

为避免这一指数爆炸，我们可以假设验证器提供条件独立的输出：

$$
P(S\mid y)=\prod_{k=1}^{m}P(S_{k}\mid y),
$$

在「每个验证器提供关于回答正确性的独特信息」的假设下，它把参数量从 $O(2^{m})$ 降到 $O(m)$ 并实现高效推断。

于是，式 (6) 简化为一个朴素贝叶斯式估计器：

$$
\Pr\bigl(y_{ij}=1\mid S=\bar{s}_{ij}\bigr)\;=\;\frac{\Pr(S_{1}=\bar{s}_{ij1},\dots,S_{m}=\bar{s}_{ijm}|y_{ij}=1)\Pr(y_{ij}=1)}{\Pr(S=\bar{s}_{ij})}
$$

$$
\;=\;\frac{\Pr(y_{ij}=1)\,\prod_{k=1}^{m}\,\Pr\bigl(S_{k}=\bar{s}_{ijk}\mid y_{ij}=1\bigr)}{\sum_{y^{\prime}\in\{0,1\}}\Pr(y_{ij}=y^{\prime})\,\prod_{k=1}^{m}\,\Pr\bigl(S_{k}=\bar{s}_{ijk}\mid y_{ij}=y^{\prime}\bigr)} \tag{7}
$$

式 (7) 中的参数包括：

- 正确性的先验概率 $\pi=\Pr(y_{ij}=1)$。
- 验证器专属的条件似然 $P(S_{k}\mid y_{ij})$。

#### B.1.1 参数估计

##### 有监督设置

当真值标签 $y_{ij}$ 可得时，参数估计归结为计算经验频率。我们可以把先验估计为：

$$
\hat{\pi}=\frac{1}{N}\sum_{i,j}\mathbf{1}\{y_{ij}=1\}
$$

对每个验证器 $k$，我们可以估计：

$$
\hat{w}_{k,1}
=\frac{\sum_{i,j}\mathbf{1}\{y_{ij}=1\}\cdot\mathbf{1}\{S_{k}=1\}}{\sum_{i,j}\mathbf{1}\{y_{ij}=1\}},
$$

$$
\hat{w}_{k,0}
=\frac{\sum_{i,j}\mathbf{1}\{y_{ij}=0\}\cdot\mathbf{1}\{S_{k}=0\}}{\sum_{i,j}\mathbf{1}\{y_{ij}=0\}}.
$$

##### 弱监督设置

当有少量标注的 $y_{ij}$ 时，我们可以用它估计 $\pi$，但仍需估计验证器准确率参数 $w_{k,1},w_{k,0}$ 以计算 $\prod_{k=1}^{m}\Pr(S_{k}=\bar{s}_{ijk}|y_{ij}=1)$。我们不用标注数据，而是用矩匹配（moment matching）估计准确率参数。具体而言，基于（HazyResearch, 2018）的方法，我们把验证器输出的可观测二阶矩与条件独立假设下模型隐含的矩相匹配。

##### 成对统计。

对每对验证器 $k_{1},k_{2}$ 与二元输出 $a,b\in\{0,1\}$，我们可以用边缘化法则与条件独立假设表达其输出的联合概率：

$$
\Pr(S_{k_{1}}=a,S_{k_{2}}=b) \tag{8}
$$

$$
=\Pr(S_{k_{1}}=a|Y=1)\Pr(S_{k_{2}}=a|Y=1)\Pr(Y=1)+\Pr(S_{k_{1}}=b|Y=0)\Pr(S_{k_{2}}=b|Y=0)\Pr(Y=0)
$$

其中验证器 $k$ 的条件分布为：

$$
\Pr(S_{k}=a\mid y=1)\;=\;\begin{cases}w_{k,1},&a=1,\\ 1-w_{k,1},&a=0,\end{cases}\quad\Pr(S_{k}=a\mid y=0)\;=\;\begin{cases}1-w_{k,0},&a=1,\\ w_{k,0},&a=0.\end{cases}
$$

##### 边缘统计。

类似地，每个验证器的边缘分布可以写为：

$$
\Pr(S_{k}=1)=\Pr(S_{k}=1|Y=1)\Pr(Y=1)+\Pr(S_{k}=1|Y=0)\Pr(Y=0) \tag{9}
$$

注意无论条件独立假设是否成立，该等式都成立。

##### 估计方法

- 构造二阶矩矩阵 $O\in\mathbb{R}^{(2m)\times(2m)}$，其中：

$$
O_{2i-1:2i,2i-1:2i}
={\tiny\begin{bmatrix}\Pr(S_{i}=0)&0\\ 0&\Pr(S_{i}=1)\end{bmatrix}}\;\forall i\in[m]
$$

$$
O_{2i-1:2i,2j-1:2j}
={\tiny\begin{bmatrix}\Pr(S_{i}=0,S_{j}=0)&\Pr(S_{i}=0,S_{j}=1)\\ \Pr(S_{i}=1,S_{j}=0)&\Pr(S_{i}=1,S_{j}=1)\end{bmatrix}}\;\forall i\neq j\in[m] \tag{10}
$$

- 构造条件概率矩阵 $\mu\in\mathbb{R}^{(2V)\times 2}$，每行编码：

$$
\mu_{2k+a,\,b}\;=\;\Pr\bigl(S_{k}=a\mid y=b\bigr)
$$

$$
\mu=\begin{bmatrix}w_{k_{1},0}&1-w_{k_{1},1}\\ 1-w_{k_{1},0}&w_{k_{1},1}\\ \dots&\dots\\ w_{k_{m},0}&1-w_{k_{m},1}\\ 1-w_{k_{m},0}&w_{k_{m},1}\end{bmatrix}
$$

- 标签先验矩阵 $P\in\mathbb{R}^{2\times 2}$ 是对角矩阵：

$$
P\;=\;\begin{bmatrix}\Pr(y_{ij}=0)&0\\ 0&\Pr(y_{ij}=1)\end{bmatrix}.
$$

于是，式 (8) 等价于在 $2\times 2$ 块对角之外的元素上 $O=\mu P\mu^{\top}$，而式 (9) 等价于 $\text{diag}(0)=\mu P\mathbb{1}^{\top}$。因此，我们优化以下损失来计算 $\mu$。

$$
\text{minimize}_{\mu}\bigl\|\,O_{\text{off-diag}}-(\mu\,P\,\mu^{T})_{\text{off-diag}}\bigr\|^{2}+\bigl\|\,\mathrm{diag}(O)-\mu\,P\,\mathbf{1}^{T}\bigr\|^{2},
$$

通过梯度下降求解，我们得到验证器准确率参数 $\{w_{k,1},w_{k,0}\}$ 的估计。

#### B.1.2 推断：计算回答正确性概率

一旦估计出准确率参数 $\{w_{k,1},w_{k,0}\}$、并从小的有标注开发集算出 $P(y_{ij}=1)$，我们就可以为每个回答计算后验正确性概率：

$$
\Pr(y_{ij}=1|S=\bar{s}_{ij})\propto\Pr(y_{ij}=1)\prod_{k=1}^{m}\Pr(S_{k}=\bar{s}_{ijk}|y_{ij}=1)
$$

$$
\Pr(y_{ij}=0|S=\bar{s}_{ij})\propto\Pr(y_{ij}=0)\prod_{k=1}^{m}\Pr(S_{k}=\bar{s}_{ijk}|y_{ij}=0)
$$

归一化后，我们得到完整的后验 $P(y_{ij}=1|S=\bar{s}_{ij})$，它提供了一个可以为每个查询选择回答的分数。

### B.2 把弱监督适配到验证设置

给定一组验证器，我们详细阐述第 4 节所述弱监督模型背后的设计选择。具体而言，我们描述围绕归一化、二值化与过滤低质量验证器的挑战。在 B.3 节中，我们描述 Weaver 归一化、二值化与过滤验证器的方法。

#### B.2.1 归一化

验证器输出在尺度、范围与分布上往往差异巨大。例如，一些验证器输出无界的实值分数（如对数似然），另一些输出归一化概率或学习到的回归值。该框架下的一些标准损失包括排序损失、二元分类损失与回归损失。例子包括：

- Bradley–Terry（排序）损失：$\mathcal{L}(s_{1},s_{0})=\log(1+\exp(s_{0}-s_{1}))$
- Logistic（二元分类）损失：$\mathcal{L}(s,y)=\log(1+\exp(-y^{\prime}s)),\quad y^{\prime}=2y-1$
- 平方（回归）损失：$\mathcal{L}(s,y)=(s-y)^{2}$

要组合可能在不同约束下训练的开箱即用验证器，验证器分数必须可比。我们注意到标准损失施加了不同但相关的不变性假设：

- 排序与二元分类损失：这些损失关注分数的相对次序，因此分数的相对排名在正仿射变换 $s\mapsto\alpha s+\beta$（$\alpha>0$）下保持不变。
- 回归损失：这些损失直接惩罚预测分数与目标值之差，因此分数的绝对尺度很重要。由于许多验证器输出近似正确性标签 $y\in[0,1]$，必须把分数约束到同一区间以确保比较有意义。

#### B.2.2 二值化

前一节描述的弱监督算法需要二元验证器输出。这天然适合裁判式验证器——如被提示回答是/否问题的语言模型——它们输出离散的 $\{0,1\}$ 标签。然而，许多验证器尤其是奖励模型输出连续分数，且尺度与校准各异。这带来一个关键设计问题：应当把这些分数原样输入弱监督模型，还是应当二值化？

使用连续分数保留了每个验证器置信度的细粒度信息。这可以改进 AUC 等基于排序的性能指标，并可能让弱监督模型更好地解决验证器之间的分歧。然而，它在组合校准或尺度不一致的验证器信号时带来挑战：0.8 的分数对不同验证器可能含义不同。如图 7 所示，即便评估同一组回答，不同验证器也展现出不同的分数分布。一些验证器呈尖锐双峰，另一些严重偏向低分或高分，还有一些产生近乎平坦或有噪声的分布。

为此，我们评估了把连续验证器分数转换为离散标签的若干二值化策略。图 8 比较了在验证器输出上训练的逻辑回归模型在四种二值化方法下的 AUC 表现：不二值化（连续分数）、固定阈值 0.5、基于类别平衡的阈值，以及分位数二值化。我们观察到，虽然连续分数在有充足训练数据时能取得强 AUC，简单的二值化策略——尤其是考虑分数分布偏斜的那些——表现相当，且在有限监督下更稳健。

图 9 显示不同二值化策略对选择准确率的差异不大。我们注意到，在高度不平衡的数据集（如 GPQA）中，简单的基于分位数的二值化表现尤其好，可能因为它调整了分数的偏斜分布，即丢弃了含糊的中段分数、只保留最自信的信号。

![Refer to caption](2506.18203v3/tables_and_figures/histogram_grid_by_verifier_GPQA-1K-v2-Diamond_70B_all_all_responses.png)

图 7：各验证器在 GPQA 数据集上的准确率。对每个验证器，我们计算其（按分数）排名第一的回答正确的题目比例。虽然一些验证器能持续选出高质量答案，另一些的表现接近随机甚至更差，这促使我们在应用弱监督之前过滤低质量验证器。

![Refer to caption](2506.18203v3/tables_and_figures/lr_binarization_grid_comparison_70B_seeds42-43-44-45-46-47-48-49-50-51_all_auc_test.png)

图 8：约定同图 9，所报性能为 ROC 曲线下面积。

![Refer to caption](2506.18203v3/tables_and_figures/lr_binarization_grid_comparison_70B_seeds42-43-44-45-46-47-48-49-50-51_all_results_test.png)

图 9：在验证器输出上训练的逻辑回归模型在不同二值化策略下的表现：(1) 无：使用原始连续分数、不二值化；(2) 固定阈值：对全部数据施加统一阈值；(3) 类别平衡：为每个验证器选择阈值，使正标签比例匹配真实类别分布；(4) 分位数：只给分数最高的 15% 赋正标签，聚焦高置信预测。结果覆盖四个数据集（GPQA-Diamond、MATH-500、MMLU-College、MMLU-Pro）与四个训练比例 $(1\%,5\%,10\%,20\%)$。对每个种子，我们用随机题目子集作为训练集，并在其余题目上报告表现。曲线报告多种子下的均值与标准差。表现为每题生成数（x 轴，对数标度）的函数。

.

#### B.2.3 过滤低质量验证器

准确率低或边缘分布极端（如近常数输出）的验证器不仅降低集成表现，还破坏弱监督算法的稳定性与可识别性，恶化估计误差。我们如何丢弃信号弱的验证器？

- 偏斜的边缘分布：考虑一个 $\Pr(y=1)\approx 0.5$ 的数据集，以及一个 $\Pr(S_{k}=1)\approx 0.99$ 的验证器。一个边缘极端（如来自朴素阈值二值化）且输出近乎恒定的偏斜验证器给集成增添的信息很少，主要增加式 (5) 目标中的噪声，因此应被丢弃。但并非所有边缘极端的验证器都信号很少；例如若 $\Pr(y=1)\approx 0.99$，一个偏斜的验证器可能高度准确。因此，低质量验证器的定义取决于正确回答的分布。
- 打破 WS 目标中的对称性：弱监督的一个常见假设是多数验证器的准确率好于随机（Fu et al., 2020）。否则 WS 算法可能给出非唯一解；式 (5) 中的项是验证器对的联合概率及其边缘，它们并不能唯一确定某个验证器是否满足 $w_{k,1},w_{k,0}>0.5$。因此，尽可能多地移除低准确率验证器、确保估计过程收敛到唯一解至关重要。

### B.3 适配方法

![Refer to caption](2506.18203v3/tables_and_figures/clustered_verifier_selection_accuracy_ALL_70B_all.png)

图 10：每个验证器在各题目与数据集上的选择准确率。

![Refer to caption](2506.18203v3/tables_and_figures/clustered_verifier_average_accuracy_ALL_70B_all.png)

图 11：给定 Llama-70B 回答分数，每个验证器在各题目与数据集上的平均准确率。

![Refer to caption](2506.18203v3/tables_and_figures/inverse_covariance_ALL_70B_all_binFalse_dropFalse.png)

图 12：给定 Llama-70B 回答分数，各验证器在各数据集上的逆协方差矩阵。

![Refer to caption](2506.18203v3/tables_and_figures/inverse_covariance_ALL_70B_all_binTrue_dropFalse.png)

图 13：给定 Llama-70B 回答分数，二值化后各验证器在各数据集上的逆协方差矩阵。

![Refer to caption](2506.18203v3/tables_and_figures/inverse_covariance_ALL_70B_all_binTrue_dropTrue.png)

图 14：给定 Llama-70B 回答分数，二值化并丢弃后各验证器在各数据集上的逆协方差矩阵。

我们现在描述所提的验证器归一化、二值化与过滤方法，之后即可应用附录 B.1 所述的弱监督算法。

1. 归一化：为使验证器输出可比，我们对每个验证器做 min-max 归一化：

$$
s^{\prime}=\frac{s-\min(s)}{\max(s)-\min(s)}\in[0,1].
$$

   这确保所有分数落在同一数值区间并保留相对次序。对回归式验证器，归一化使其输出与标签的尺度对齐，并避免无界分数范围带来的数值不稳定。若不归一化，聚合方法可能因分数量级失衡而变得有偏或病态。
2. 二值化：我们用少量标注样本 $\mathcal{D}^{\text{dev}}$（我们本来就用它计算 $\Pr(y=1)$）来确定把连续验证器输出转换为二元输出的阈值。图 13 展示了二值化后验证器分数的精度矩阵（逆协方差矩阵），显示大的非对角依赖被阻尼、条件数改善。表 4 表明，只用基准开发集的 5 到 10 个标注查询（≤ 评估集的 1%），我们估计的二值化阈值相对沿数据集分数中位数做二元切分，为 70B 模型平均提升 8.4% 的表现。
3. 过滤低质量验证器：为缓解低质量验证器的影响，我们按类别平衡剪除边缘行为极端的验证器。对估计类别平衡在 20% 到 80% 之间的数据集，我们过滤正例率超出该范围的验证器。若数据集整体正样本少于 20%，我们移除预测正例超过 80% 时间的验证器；反之，若正样本超过 80%，我们丢弃预测正例少于 20% 时间的验证器。

   图 14 展示了二值化并丢弃低信号或冗余验证器后验证器分数的精度矩阵。与图 13 相比，它显示非对角结构进一步衰减，说明丢弃对解相关验证器集合贡献显著，可改善下游弱监督的可识别性与数值稳定性。如表 5 所示，验证器剪除为 70B 模型设置带来 12.5% 的性能提升。

表 4：用于 Weaver 类别平衡估计的开发集消融：奖励模型阈值取默认值 $0.5$。

| 方法 | 模型规模 | 开发集规模 | MATH500 | GPQA Diamond | MMLU | MMLU Pro | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Weaver | 70B | 朴素阈值（0.5 阈值） | 88.1% | 52.0% | 92.4% | 83.5% | 79.0% |
| Weaver | 70B | 1% | 90.4% | 67.1% | 91.1% | 87.0% | 84.5% |
| Weaver | 70B | 5% | 92.4% | 72.7% | 93.5% | 90.4% | 87.5% |
| Weaver | 70B | 20% | 92.4% | 72.7% | 93.5% | 90.4% | 87.5% |
| Weaver | 70B | 100% | 92.4% | 72.7% | 93.5% | 90.4% | 87.5% |

表 5：Weaver 验证器选择策略消融：用每个验证器的边缘概率，按数据集比较不同的故障验证器丢弃策略。

| 方法 | 模型规模 | 验证器选择 | MATH500 | GPQA Diamond | MMLU | MMLU Pro | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Weaver | 70B | 不丢弃验证器 | 90.4% | 52.0% | 91.1% | 84.2% | 79.4% |
| Weaver | 70B | 丢弃低边缘（多为负的验证器） | 93.4% | 60.6% | 91.7% | 91.0% | 84.2% |
| Weaver | 70B | 丢弃高边缘（多为正的验证器） | 83.4% | 69.7% | 87.9% | 78.4% | 79.9% |
| Weaver | 70B | 丢弃极端边缘（多为正或负） | 90.8% | 72.7% | 92.4% | 85.0% | 85.2% |

表 6：Weaver 自适应阈值开发集规模消融。

| 方法 | 模型规模 | 自适应阈值开发集规模 | MATH500 | GPQA Diamond | MMLU | MMLU Pro | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Weaver | 70B | 0.01 | 92.4% | 72.7% | 93.5% | 90.4% | 87.5% |
| Weaver | 70B | 0.05 | 92.4% | 72.7% | 93.5% | 90.4% | 87.5% |
| Weaver | 70B | 0.2 | 92.4% | 72.7% | 93.5% | 90.4% | 87.5% |
| Weaver | 70B | 1.0 | 92.4% | 72.7% | 93.5% | 90.4% | 87.5% |

表 7：连续与离散逻辑回归的性能比较：对验证器分数做有监督微调时，连续模型在所有数据集上持续优于离散变体，因为它避免了离散变体所需的从浮点到二元投票的有损转换。

| 连续 vs. 离散逻辑回归性能（%） | | | | | |
| --- | --- | --- | --- | --- | --- |
| 方法 | MATH 500 | GPQA | MMLU College | MMLU Pro | BBH |
| 离散 LR | 93.1 | 74.3 | 87.5 | 87.1 | 90.1 |
| 连续 LR | 97.2 | 78.1 | 90.4 | 92.0 | 96.5 |
| 改进 | +4.1 | +3.8 | +2.9 | +4.9 | +6.4 |

表 8：每查询的唯一抽取答案数与正:负样本比例的相关性——Llama 3.1 Instruct 模型

| Llama 3.1 8B Instruct | | | |
| --- | --- | --- | --- |
| 相关性指标 | | | |
| 数据集 | Pearson | Spearman | Kendall's Tau |
| MATH 500 | -0.676 | -0.745 | -0.565 |
| GPQA | -0.312 | -0.117 | -0.096 |
| MMLU College | -0.595 | -0.700 | -0.591 |
| MMLU Pro | -0.590 | -0.555 | -0.425 |
| BBH | -0.365 | -0.386 | -0.300 |

| Llama 3.1 70B Instruct | | | |
| --- | --- | --- | --- |
| 相关性指标 | | | |
| 数据集 | Pearson | Spearman | Kendall's Tau |
| MATH 500 | -0.631 | -0.842 | -0.709 |
| GPQA | -0.148 | -0.093 | -0.089 |
| MMLU College | -0.551 | -0.862 | -0.769 |
| MMLU Pro | -0.446 | -0.693 | -0.585 |
| BBH | -0.268 | -0.594 | -0.474 |

### B.4 探索：按难度聚类以改进 Weaver

弱验证器在输入查询难度谱上的行为往往不一致。例如，多数验证器在简单查询上可能准确率很高，而在较难查询上准确率很低。图 11 与图 10 展示了每个验证器在多个题目与数据集上的平均与选择准确率，证实验证器表现在逐查询层面存在显著差异。为捕获这种异质性，我们探索按难度对查询聚类，并为每个簇独立拟合一个 Weaver 弱监督模型。

我们把查询难度定义为每个查询正确与错误生成的经验比率。以它作为题目难度的代理，我们沿难度分布把每个数据集划分为等大小的簇，并为每个簇学习单独的弱监督模型。这是在 oracle 设置下完成的：难度用真值正确性计算，但训练簇专属验证器模型时不使用任何标签信息。

这一方法在两个意义上是自适应的：(1) 我们使弱监督模型适配查询的难度类别；(2) 我们对每个奖励模型的阈值按簇独立适配，以更好反映局部验证器行为。对每个簇，我们在 0.05 到 0.95、步长 0.05 的范围内（共 19 个值）对奖励模型阈值做网格搜索，选出在留出开发集上准确率最大的阈值。我们尝试把每个数据集的查询聚成 1 到 5 个难度级别，用 oracle 难度分布把查询等分为大小相同的桶。虽然我们研究中的聚类使用 oracle 难度，未来工作可以探索无监督近似，或用小的有标注子集（如 10%）估计难度分布的半监督方法。

在表 9 与表 10 中，我们分析难度感知聚类与阈值适配如何影响 Weaver 在不同模型规模下的表现。

- 70B 模型：在这一规模，我们发现优化单个奖励模型阈值即可捕获大部分验证信号，聚类只带来边际收益（约 1%）。这表明在更高的模型能力下，验证器行为在查询难度间相对稳定。
- 8B 模型：相比之下，8B 设置从聚类与自适应阈值中获得更大增益（4.8%）。我们将其归因于三个关键因素：

  1. 更高的验证器方差：如表 16 所示，8B 设置下验证器质量在查询间波动更大，使簇专属模型更有益。
  2. 更少的正例生成：表 13 显示 8B 生成器整体产生的正确答案更少，加大了难度异质性。
  3. 更大的生成-验证差距：8B 的 Pass@1 到 Pass@K 差距更显著（如 MATH500 上 49.8% 到 99.2%），表明基于选择的方法有更大改进空间。

表 9 确认增加簇数能改进 8B 模型的准确率，但往往降低 70B 模型的准确率。这些结果表明，难度感知建模在验证器行为不稳定、生成模型产生的正确候选稀疏时尤其有用。

逐模型阈值的进一步收益。最后，在表 11 中我们引入一种更细粒度的调优策略：每个奖励模型获得自己的阈值，而非每簇一个全局阈值。该策略为 70B 模型带来适度但一致的改进（如 GPQA Diamond +0.5%、MMLU Pro +0.8%），并为 8B 模型在所有数据集上带来更显著的提升（+1.6% 到 +2.8%）。这些增益凸显了不仅按查询难度、还按验证器专属行为来适配验证器聚合策略的价值，尤其在噪声更明显的小模型规模上。

表 9：不同簇数下 Weaver 的表现：使用 Llama 3.1 70B Instruct 生成，验证器阈值在聚类前优化。我们按查询难度（每查询正确与错误生成的比率）创建簇，并从每个任务的分布等分创建簇。

| Weaver 数据集的簇数 | | | | | |
| --- | --- | --- | --- | --- | --- |
| 数据集 | 1 | 2 | 3 | 4 | 5 |
| MATH 500 | 93.4 | 87.6 | 83.8 | 82.8 | 81.2 |
| GPQA | 66.4 | 66.4 | 66.4 | 66.4 | 66.4 |
| MMLU College | 94.9 | 91.7 | 90.1 | 89.6 | 89.8 |
| MMLU Pro | 88.4 | 90.2 | 87.1 | 84.6 | 79.8 |
| 平均 | 85.8 | 84.0 | 81.9 | 80.9 | 79.3 |

表 10：优化 Weaver 的簇与自适应阈值。我们报告不同评估策略下的选择表现，包括有无基于难度的聚类与阈值调优。聚类基于 oracle 查询难度。阈值通过从 0.05 到 0.95、步长 0.05 的网格搜索选出。

| Llama 3.1 70B Instruct 下不同评估方法的表现 | | | |
| --- | --- | --- | --- |
| 数据集 | 无聚类 / 0.5 阈值 | 搜索找到的最佳值 | Pass@K |
| MATH 500 | 93.4% | 95.2% | 98.6% |
| GPQA Diamond | 72.4% | 74.1% | 81.0% |
| MMLU College | 94.9% | 95.1% | 96.0% |
| MMLU Pro | 90.2% | 90.2% | 92.0% |
| 平均 | 87.7% | 88.7% | 91.9% |

| Llama 3.1 8B Instruct 下不同评估方法的表现 | | | |
| --- | --- | --- | --- |
| 数据集 | 无聚类 / 0.5 阈值 | 搜索找到的最佳值 | Pass@K |
| MATH 500 | 80.0% | 84.3% | 99.2% |
| GPQA Diamond | 47.1% | 52.7% | 95.2% |
| MMLU College | 85.7% | 89.9% | 98.5% |
| MMLU Pro | 67.2% | 72.3% | 96.8% |
| 平均 | 70.0% | 74.8% | 97.4% |

表 11：优化 Weaver 的簇与逐模型自适应阈值。在此设置中，每个奖励模型获得自己的优化阈值（而非每簇一个全局阈值）。阈值通过从 0.05 到 0.95、步长 0.05 的网格搜索选出。聚类仍基于 oracle 查询难度。这种更细粒度的调优为 70B 模型带来小幅改进，为 8B 模型带来更显著的增益，尤其在验证器准确率高度可变之处。

| Llama 3.1 70B Instruct（逐模型阈值）下评估方法的表现 | | | |
| --- | --- | --- | --- |
| 数据集 | 无聚类 / 0.5 阈值 | 搜索找到的最佳值 | Pass@K |
| MATH 500 | 93.4% | 95.2% | 98.6% |
| GPQA Diamond | 72.4% | 74.6% | 81.0% |
| MMLU College | 94.9% | 95.1% | 96.0% |
| MMLU Pro | 90.2% | 91.0% | 92.0% |
| 平均 | 87.7% | 89.0% | 91.9% |

| Llama 3.1 8B Instruct（逐模型阈值）下评估方法的表现 | | | |
| --- | --- | --- | --- |
| 数据集 | 无聚类 / 0.5 阈值 | 搜索找到的最佳值 | Pass@K |
| MATH 500 | 80.0% | 86.5% | 99.2% |
| GPQA Diamond | 47.1% | 55.5% | 95.2% |
| MMLU College | 85.7% | 91.5% | 98.5% |
| MMLU Pro | 67.2% | 74.5% | 96.8% |
| 平均 | 70.0% | 77.0% | 97.4% |

## 附录 C 实验

### C.1 模型与数据集

基准：我们用若干覆盖指令遵循、推理、数学与编程的基准评估模型：MATH500（Hendrycks et al., 2021）、GPQA（Rein et al., 2024）、MMLU（Hendrycks et al., 2021）、MMLU Pro（Wang et al., 2024）与 BBH（Suzgun et al., 2022）。表 12 给出各数据集概览。对 MMLU，我们选取大学级别的题目评估：生物、化学、物理、数学、计算机科学与医学。对 MMLU Pro，我们从可用的 12K 查询中随机抽取 500 个。对 BBH，我们从 6K 查询的数据集中取四个任务：Penguins in a Table、Causal Judgement、Logical Deduction（Five Objects）与 Tracking Shuffled Objects（Five Objects）。

模型：我们用一系列弱验证器——即不完美但准确率好于随机的模型——评估候选生成。我们的验证系统 $\mathcal{V}$ 包括两大类弱验证器：奖励模型与 LM 裁判。

- 奖励模型：奖励模型（RM）是一个训练过的语言模型，依据候选回答与人类偏好的契合程度为其打标量分（Lambert et al., 2024；Song et al., 2025）。给定查询与候选回答，RM 输出一个 $V_{ij}\in[0,1]$，表示按正确性、有帮助性、安全性等标准估计的候选 $j$ 的质量。

  - 奖励模型的例子包括 RewardBench 排行榜（Lambert et al., 2024）上的 INF-ORM（Tan et al., 2024）、QRM Gemma（Dorka, 2024）与 Skywork Reward（Liu et al.）。我们还纳入过程奖励模型（PRM），它们为推理过程本身——强调逐步逻辑与连贯性——而非仅最终答案打分（Cui et al., 2025；Yuan et al.）。
  - 在我们的研究中，我们选择了 RewardBench 的 top-20 奖励模型与 Process Reward Bench（Song et al., 2025）的 top-20 过程奖励模型，覆盖 8B 与 70B 两种参数规模。我们剔除任何不能提供正向学习信号的 RM 或 PRM——即其在基准训练集上的排序不优于随机选择（附录 C.1）。
  - 这些奖励模型所用的多样训练目标与数据集带来了影响其验证能力的系统性偏差（Lambert et al., 2024；Song et al., 2025），损失函数各异——包括用于成对偏好的 Bradley-Terry 损失（Bradley & Terry, 1952）、用于固定分数差的间隔损失（Rosset et al., 2003），以及用于相对排序的成对排序损失（Cao et al., 2007）。
  - 先前工作已指出，组合奖励模型与裁判的输出并非易事，因为它们分别给出 logits 与二元决策规则（Verga et al., 2024；Xu et al., 2024）。我们发现可以用稳健百分位把所有 RM 分数归一化到 $[0,1]$：第 5 百分位映射到 0、第 95 百分位映射到 1。对提供多打分维度的模型（如 ArmoRM（Wang et al., 2024）），我们只用其主输出。
- LM 裁判：LM 裁判是一个用于评估候选回答正确性的语言模型，它生成二元裁决：$V_{ij}\in\{0,1\}$，其中 1 表示该回答被判定为正确。这些模型通常应用思维链（CoT）推理来得出结论（Wei et al., 2023）。每个 LM 裁判以查询与回答为输入，输出单个二元裁决。

  - 我们使用 ChatBotArena（Chiang et al., 2024）上知名的聊天模型作为 LM 裁判，它们以通用推理能力著称。为确保一致性与确定性，我们在生成裁决时使用贪心解码（温度 $T=0$）。

表 12：基准概览：MATH500、GPQA、MMLU、MMLU Pro 与 Big-Bench Hard（BBH）的评估配置。

| 基准 | 数据集规模 | 打分类型 | 指标 | 许可证 |
| --- | --- | --- | --- | --- |
| MATH500 | 500 | 标准答案 | Pass@1 | Apache 2.0 |
| GPQA | 646 | 标准答案 | Pass@1 | CC BY 4.0 |
| MMLU College | 719 | 标准答案 | Pass@1 | MIT |
| MMLU Pro | 500 | 标准答案 | Pass@1 | MIT |

![Refer to caption](2506.18203v3/tables_and_figures/Growth_of_RMs_and_LMs.png)

图 15：开源 RM 与 LM 的增长：随着越来越多的 RM 与 LM 裁判可用，对这些模型在测试时更好的选择与利用策略的需求持续增长。

表 13：Llama 3.1 8B Instruct 的生成准确率分布。每行显示落入各正确性十分位（即每查询 100 个样本中正确生成的比例）的查询占比。最后一列报告各数据集的总正确/错误（C/I）比。这些分布凸显了查询难度的差异，也促使我们在附录 B.4 中采用按难度聚类的方法。

| Llama 3.1 8B Instruct | | | | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 正确/错误生成的分布 | | | | | | | | | | | |
| 数据集 | 占数据集百分比：0.0-0.1 | 0.1-0.2 | 0.2-0.3 | 0.3-0.4 | 0.4-0.5 | 0.5-0.6 | 0.6-0.7 | 0.7-0.8 | 0.8-0.9 | 0.9-1.0 | C/I 比 |
| AIMO | 72.2% | 7.8% | 3.3% | 7.8% | 2.2% | 3.3% | 2.2% | 0.0% | 1.1% | 0.0% | 10.3% |
| MATH 500 | 12.2% | 11.4% | 11.6% | 8.2% | 6.4% | 8.0% | 8.4% | 6.60% | 11.2% | 15.0% | 49.9% |
| GPQA | 28.5% | 21.2% | 16.1% | 7.4% | 7.3% | 5.3% | 3.7% | 3.3% | 2.9% | 2.6% | 28.3% |
| MMLU College | 7.8% | 7.6% | 7.1% | 6.5% | 6.7% | 5.3% | 7.2% | 6.3% | 8.6% | 22.9% | 64.1% |
| MMLU Pro | 22.4% | 9.8% | 10.6% | 5.4% | 6.4% | 7.2% | 4.0% | 7.6% | 7.6% | 15.2% | 46.6% |
| BBH | 3.2% | 6.7% | 10.3% | 8.3% | 10.3% | 14.8% | 11.6% | 10.7% | 10.4% | 12.1% | 56.9% |

表 14：Llama 3.1 70B Instruct 的生成准确率分布。每行显示落入各正确性十分位（即每查询 100 个样本中正确生成的比例）的查询占比。最后一列报告各数据集的总正确/错误（C/I）比。这些分布凸显了查询难度的差异，也促使我们在附录 B.4 中采用按难度聚类的方法。

| Llama 3.1 70B Instruct | | | | | | | | | | | |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 正确/错误生成的分布 | | | | | | | | | | | |
| 数据集 | 占数据集百分比：0.0-0.1 | 0.1-0.2 | 0.2-0.3 | 0.3-0.4 | 0.4-0.5 | 0.5-0.6 | 0.6-0.7 | 0.7-0.8 | 0.8-0.9 | 0.9-1.0 | C/I 比 |
| MATH 500 | 7.0% | 4.2% | 3.8% | 2.0% | 2.2% | 3.8% | 4.2% | 4.0% | 7.8% | 61.0% | 78.0% |
| GPQA | 36.8% | 5.6% | 5.1% | 3.7% | 6.2% | 4.3% | 4.5% | 4.8% | 8.0% | 20.9% | 42.9% |
| MMLU College | 8.1% | 3.2% | 1.8% | 2.2% | 1.5% | 1.7% | 1.8% | 3.2% | 2.4% | 74.1% | 82.6% |
| MMLU Pro | 16.4% | 4.2% | 1.8% | 3.4% | 3.0% | 3.0% | 3.2% | 4.8% | 6.0% | 54.2% | 69.9% |

表 15：Weaver 测试的模型。

| | 模型 | 源码 | 参数量 | 许可证 | 损失函数 |
| --- | --- | --- | --- | --- | --- |
| LM 裁判 | Llama-3.1-70B-Instruct | 开源 | 70B | Llama 3.1 Community | 交叉熵损失 |
| | Llama-3.1-405B-Instruct | 开源 | 405B | Llama 3.1 Community | 交叉熵损失 |
| | Llama-3.3-70B-Instruct | 开源 | 70B | Llama 3.1 Community | 交叉熵损失 |
| | Meta-Llama-3.1-405B-Instruct-quantized.w8a16 | 开源 | 405B | Llama 3.1 Community | 交叉熵损失 |
| | DeepSeek LLM 67B Chat | 开源 | 67B | DeepSeek License | 交叉熵损失 |
| | DeepSeekLlama70B | 开源 | 70B | DeepSeek License | 交叉熵损失 |
| | DeepSeekQwen32B | 开源 | 32B | DeepSeek License | 交叉熵损失 |
| | DeepSeekLlama8B | 开源 | 8B | DeepSeek License | 交叉熵损失 |
| | DeepSeekQwen7B | 开源 | 7B | DeepSeek License | 交叉熵损失 |
| | Qwen2 72B Instruct | 开源 | 72B | Tongyi Qianwen | 交叉熵损失 |
| | Qwen2.5-72B-Instruct | 开源 | 72B | Tongyi Qianwen | 交叉熵损失 |
| | Qwen/Qwen2.5-72B-Instruct | 开源 | 72B | Tongyi Qianwen | 交叉熵损失 |
| | QwQ-32B | 开源 | 32B | Apache 2.0 | 交叉熵损失 |
| | Qwen1.5 110B Chat | 开源 | 110B | Tongyi Qianwen | 交叉熵损失 |
| | Qwen1.5 72B Chat | 开源 | 72B | Tongyi Qianwen | 交叉熵损失 |
| | Qwen-2.5-7B-Instruct | 开源 | 7B | Tongyi Qianwen | 交叉熵损失 |
| | Qwen-2.5-Math-7B-Instruct | 开源 | 7B | Tongyi Qianwen | 交叉熵损失 |
| | Mixtral 8x22B v0.1 | 开源 | 176B | Apache 2.0 | 交叉熵损失 |
| | Mixtral-8x22B-Instruct-v0.1 | 开源 | 176B | Apache 2.0 | 交叉熵损失 |
| | WizardLM 8x22B | 开源 | 176B | Apache 2.0 | 交叉熵损失 |
| | WizardLM-2-8x22B | 开源 | 176B | Apache 2.0 | 交叉熵损失 |
| | dbrx-instruct | 开源 | 132B | Databricks Open Model | 交叉熵损失 |
| | SkyT1 | 开源 | 32B | Apache 2.0 | 交叉熵损失 |
| RM（8B 及以下） | GRM-Llama3-8B-rewardmodel-ft | 开源 | 8B | MIT | 成对排序损失 |
| | GRM-Llama3.2-3B-rewardmodel-ft | 开源 | 3B | Apache 2.0 | 成对排序损失 |
| | GRM-Gemma2-2B-rewardmodel-ft | 开源 | 2B | Apache 2.0 | 成对排序损失 |
| | Skywork-Reward-Llama-3.1-8B-v0.2 | 开源 | 8B | Skywork License | 成对排序损失 |
| | QRM-Llama3.1-8B-v2 | 开源 | 8B | MIT | 分位数回归损失 |
| | URM-LLaMa-3.1-8B | 开源 | 8B | Skywork License | 不确定性感知损失 |
| | GPM-Llama-3.1-8B | 开源 | 8B | MIT | 成对排序损失 |
| | Llama-3-OffsetBias-RM-8B | 开源 | 8B | Llama 3.1 Community | 成对排序损失 |
| | ArmoRM-Llama3-8B-v0.1 | 开源 | 8B | Llama 3.1 Community | 成对排序损失 |
| | Qwen2.5-Math-PRM-7B | 开源 | 7B | Tongyi Qianwen | 交叉熵损失 |
| | EurusPRM-Stage1 | 开源 | 7B | Apache 2.0 | 交叉熵损失 |
| | EurusPRM-Stage2 | 开源 | 7B | Apache 2.0 | 交叉熵损失 |
| | internlm2-7b-reward | 开源 | 7B | Apache 2.0 | 成对排序损失 |
| | Decision-Tree-Reward-Llama-3.1-8B | 开源 | 8B | Skywork License | 决策树损失 |
| RM（27B–72B） | Skywork-Reward-Gemma-2-27B-v0.2 | 开源 | 27B | Skywork License | 成对排序损失 |
| | QRM-Gemma-2-27B | 开源 | 27B | MIT | 分位数回归损失 |
| | INF-ORM-Llama3.1-70B | 开源 | 70B | Custom License | 二元交叉熵损失 |
| | Qwen2.5-Math-RM-72B | 开源 | 72B | Tongyi Qianwen | 交叉熵损失 |
| | Qwen2.5-Math-PRM-72B | 开源 | 72B | Tongyi Qianwen | 交叉熵损失 |
| | internlm2-20b-reward | 开源 | 20B | Apache 2.0 | 成对排序损失 |
| | Decision-Tree-Reward-Gemma-2-27B | 开源 | 27B | Skywork License | 成对排序损失 |

表 16：Weaver 验证器准确率与分数相关性。我们报告单个验证器准确率的范围以及验证器分数之间的平均成对 Pearson 相关。每个验证器的输出在所有查询-候选对上展平，并在所有 $\binom{m}{2}$ 个验证器对上计算相关。较低的相关表明验证器打分方式的更大多样性，支持 Weaver 集成的有效性。

| 指标 | 模型规模 | MATH500 | GPQA | MMLU Pro | 平均 |
| --- | --- | --- | --- | --- | --- |
| 验证器准确率范围 | 8B | 34.2% | 40.7% | 36.4% | 37.1% |
| 平均分数相关 | 8B | 0.0253 | 0.0349 | 0.0312 | 0.0305 |
| 验证器准确率范围 | 70B | 27.4% | 29.0% | 31.6% | 29.3% |
| 平均分数相关 | 70B | 0.0211 | 0.0372 | 0.0240 | 0.0274 |

### C.2 验证基线

#### C.2.1 免验证器方法

首个样本（Pass@1）：该基线只使用第一个生成的回答，不带任何验证或选择机制。它代表模型生成单个回答的标准做法，为性能比较提供下界。该方法不扩展测试时计算，也不使用验证。

多数投票：一种免验证器方法，生成多个候选回答并选择所有回答中最常见的最终答案（Brown et al., 2024；Chen et al., 2024；Snell et al., 2024）。该方法利用重复采样，但不使用验证模型评估回答质量，而是依赖「正确答案在多次生成中比错误答案出现得更频繁」这一假设。

#### C.2.2 替代验证策略

朴素无加权聚合：我们考虑用 top-1、top-5 与 top-10 验证器（按与真值标签的一致率排名）的三种 oracle 配置。在所有数据集上，这些 oracle 集成大幅超过基线。平均而言，表现最好的无加权集成超过首样本表现 20.3%、超过多数投票 15.0%（见图 2）。对 GPQA 与 MMLU Pro 等较难的基准，top-5 与 top-10 集成持续优于 top-1，表明验证器多样性在困难样本上尤其有益。然而这些 oracle 集成依赖真值来给验证器排名，限制了实践可用性，也凸显了对无监督学习加权的需求。

朴素贝叶斯：我们实现一个朴素贝叶斯分类器，建模给定验证器分数下回答正确的概率：$P(y_{ij}=1|s_{ij1},...,s_{ijm})=\frac{P(s_{ij1},...,s_{ijm}|y_{ij}=1)P(y_{ij}=1)}{P(s_{ij1},...,s_{ijm})}$。在条件独立假设下，它因子分解为 $P(s_{ij1},...,s_{ijm}|y_{ij}=1)=\prod_{k=1}^{m}P(s_{ijk}|y_{ij}=1)$。我们用开发集的标注数据估计参数。该方法为聚合验证器输出提供了一个概率框架，但参数估计需要标注数据。

逻辑回归：我们训练一个逻辑回归分类器，输入特征是验证器分数 $[s_{ij1},...,s_{ijm}]$，输出是每个回答的正确性：$P(y_{ij}=1|\mathbf{s}{ij})=\sigma(\mathbf{w}^{T}\mathbf{s}{ij}+b)$，其中 $\sigma$ 是 sigmoid 函数。权重 $\mathbf{w}$ 与偏置 $b$ 用有标注训练数据学习。这种有监督方法能捕获验证器输出间比朴素平均更复杂的关系，但有效训练需要大量标注数据。

多智能体验证（MAV）（Lifshitz et al., 2025）：该方法组合多个「方面验证器」（Aspect Verifier，AV）——通过二元 True/False 批准被提示验证候选输出特定方面的现成 LLM。与奖励模型不同，AV 无需额外训练，且易于通过投票机制组合。MAV 框架使用 BoN-MAV（带多智能体验证的 Best-of-N），其流程为：(1) 从生成器 LLM 采样 $n$ 个候选输出；(2) 从在三个维度（基座 LLM、验证的方面、验证策略）上变化的多个方面验证器收集二元批准；(3) 选择批准数最多的输出。在我们的实现中，我们用 Llama 3.3 70B Instruct 作为裁判模型，而非原论文使用的 Gemini 1.5 Flash/Pro。

自验证（Zhao et al.）：该方法实现了一种复杂的基于采样的搜索：模型通过细致的自然语言分析验证自己的回答。它超越了简单的自我批评，使用结构化的验证提示：(1) 把候选回答改写为严格的数学定理-引理-证明格式；(2) 通过逐步分析系统扫描错误；(3) 比较多个回答以定位潜在错误。该方法利用两个关键原理：跨回答的比较提供关于错误位置的信号（因为模型难以自行回忆错误，但给定位置时能识别错误）；不同任务适用不同输出风格（生成用思维链，验证用严格数学格式）。该方法不同于朴素自验证之处在于使用结构化、多步的验证协议，而非简单的正确性判断。

表 17：逻辑回归与朴素贝叶斯在各数据集与开发集规模下的表现

| 数据集 | 方法 | 模型规模 | 0.01 | 0.05 | 0.2 | 0.5 | 1.0 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MATH-500 | 逻辑回归 | 70B | 70.5% | 74.7% | 81.4% | 93.1% | 97.2% |
| | 朴素贝叶斯 | 70B | 67.4% | 78.1% | 85.0% | 89.2% | 92.2% |
| GPQA Diamond | 逻辑回归 | 70B | 55.9% | 59.4% | 69.8% | 71.4% | 72.9% |
| | 朴素贝叶斯 | 70B | 47.2% | 49.2% | 57.6% | 62.1% | 64.3% |
| MMLU Pro | 逻辑回归 | 70B | 72.1% | 81.0% | 84.6% | 86.0% | 92.0% |
| | 朴素贝叶斯 | 70B | 60.2% | 73.1% | 73.1% | 78.6% | 78.6% |

（注：表头数字为开发集规模占数据集的比例。）

### C.3 Weaver 的扩展趋势

缩放定律描述准确率、样本效率或计算成本等性能指标如何随可控资源（即尝试次数 $K$、模型容量）的扩展而变化。（Kaplan et al., 2020）表明，对固定参数量的 Transformer 语言模型，交叉熵损失随模型规模与数据量呈幂律下降。该框架此后被扩展以探索模型与数据扩展之间的最优权衡（Hoffmann et al., 2022），以及多样本的推理时扩展（Chen et al., 2021；Brown et al., 2024）。

首先，我们确立 Pass@K 率的幂律扩展。假设第 $i$ 道题有未知的「难度」$p_{i}\in[0,1]$，即单个回答正确的概率。有 $K$ 个独立样本时，至少得到一个正确回答的概率是

$$
q_{i}(p_{i},K)=1-(1-p_{i})^{K}\approx 1-\exp(-p_{i}\cdot K)\quad\text{对小 }p_{i}
$$

定义指示变量：

$$
X_{i}=\begin{cases}1,&\text{若第 }i\text{ 个查询至少被解出一次（概率 }q_{i}\text{）},\\ 0,&\text{否则},\end{cases}
$$

并令被解题目的总数为 $Y=\sum_{i=1}^{N}X_{i}$。

期望覆盖率（Pass@K）是每题尝试 $K$ 次后被解题目比例的期望：

$$
\text{Pass@K}:=\mathbb{E}[Y]/N=\frac{1}{N}\sum_{i=1}^{N}(1-(1-p_{i})^{K})
$$

为建模题目难度的总体差异，我们假设每题的正确率 $p_{i}$ 服从 Beta 分布：$p_{i}\sim\text{Beta}(\alpha,\beta)$。这捕获了「一些题较容易（高 $p_{i}$）而另一些较难（低 $p_{i}$）」的想法，整体分布由形状参数 $\alpha,\beta$ 控制。于是，$K$ 次尝试内可被解题目的比例为，

$$
\text{Pass@K}
=\mathbb{E}_{p\sim\text{Beta}(\alpha,\beta)}[1-(1-p)^{K}]
$$

$$
=1-\mathbb{E}_{p\sim\text{Beta}(\alpha,\beta)}[(1-p)^{K}]=1-\frac{B(\alpha,\beta+K)}{B(\alpha,\beta)} \tag{11}
$$

依据 Beta 函数 $B(\cdot,\cdot)$ 的定义。取对数：

$$
\log\text{Pass@K}=\log\left(1-\frac{B(\alpha,\beta+K)}{B(\alpha,\beta)}\right)\approx-\frac{B(\alpha,\beta+K)}{B(\alpha,\beta)}
$$

这里用了 $x$ 小时 $\log(1-x)\approx-x$，对大的 $K$ 成立。然后用 Gamma 函数表达 Beta 函数可得：

$$
\log\text{Pass@K}\approx-\frac{\Gamma(\beta+K)\Gamma(\alpha+\beta)}{\Gamma(\beta)\Gamma(\alpha+\beta+K)}
$$

对大的 $K$，我们可以用 Gamma 函数的 Stirling 近似 $\log\Gamma(x)\approx x\log x-x+\frac{1}{2}\log(2\pi)+\frac{1}{2}\log x$：

$$
\log[-\log\text{Pass@K}]
=\log\Gamma(\beta+K)+\log\Gamma(\alpha+\beta)-\log\Gamma(\beta)-\log\Gamma(\alpha+\beta+K)
$$

$$
\approx(\beta+K)\log(\beta+K)-(\alpha+\beta+K)\log(\alpha+\beta+K)+\frac{1}{2}\log\left(\frac{\beta+K}{\alpha+\beta+K}\right)
$$

$$
\approx(\beta+K)\log K-(\alpha+\beta+K)\log K+\text{const}
$$

$$
=-\alpha\log K+\log\zeta
$$

这里保留了首阶项。相应地，期望覆盖率的对数随 $K$ 呈幂律，缩放为：

$$
\log\text{Pass@K}=-\exp\left(-\alpha\log K+\log\zeta\right)=-\zeta K^{-\alpha} \tag{12}
$$

##### 验证器成功建模

现在假设我们把 $K$ 个候选交给一个打分模型（「验证器」），由它选出得分最高的答案。验证过程成功需要 (i) 至少生成了一个正确答案，且 (ii) 验证器把某个正确答案排在最高。

$$
\text{Selection@1}(K):=\mathbb{P}[\text{得分最高的回答正确}] \tag{13}
$$

假设验证器打分使得正确回答来自分数分布 $f_{1}$、错误回答来自分布 $f_{0}$。令 $s^{(1)}=\{s_{j}:y_{j}=1\}$ 与 $s^{(0)}=\{s_{j}:y_{j}=0\}$ 分别表示正确与错误回答的分数。则一个查询被成功验证当：

$$
\text{Selection@1}=\mathbb{P}\left[\max s^{(1)}>\max s^{(0)}\right]
$$

我们的目标是计算「$c$ 个来自 $f_{1}$ 的独立同分布抽样的最大值超过 $K-c$ 个来自 $f_{0}$ 的抽样的最大值」的概率。

为建模回答的正确性，我们假设每个查询 $i$ 有隐含正确率 $p_{i}\sim\text{Beta}(\alpha,\beta)$，反映查询专属难度。给定 $p_{i}$，$K$ 个回答中的每一个独立采样为：

$$
y_{ij}\sim\text{Bernoulli}(p_{i}),\quad j=1,\dots,K
$$

这蕴含正确回答的数量服从二项分布：

$$
C_{i}=\sum_{j=1}^{K}y_{ij}\sim\text{Binomial}(K,p_{i})
$$

假设 (1) 给定 $p_{i}$ 时回答条件独立，(2) 同一查询内正确率相同，(3) 回答数量 $K$ 固定。

由于正确率 $p$ 在查询间变化，数据集层面的 Selection@1 曲线需要对 $p$ 做边缘化：

$$
\text{Selection@1}(K)=\mathbb{E}_{p\sim\text{Beta}(\alpha,\beta)}\left[\text{Selection@1}(K\mid p)\right]
$$

再加上对验证器分数做最大值比较的建模需求，使 Selection@1 的精确计算在解析上不可行。

为了对 Selection@1 做可解析、平滑的建模，我们引入以下参数形式：

$$
\text{Selection@1}(K)\approx\exp(-\zeta K^{-\alpha})\cdot\left(1-(1-\pi)^{K^{\gamma}}\right) \tag{14}
$$

- 覆盖项 $\exp(-\zeta K^{-\alpha})$ 近似「至少生成一个正确回答」的概率。
- 验证项 $1-(1-\pi)^{K^{\gamma}}$ 近似「在至少存在一个正确回答的条件下，得分最高的回答正确」的概率。参数 $\gamma$ 控制验证器表现随 $K$ 呈次线性还是超线性改进。参数 $\pi$ 表示「在回答正确且纳入候选集的条件下，被验证器成功选为最高分」的每回答有效概率。

为获得实用的扩展趋势，我们把式 (14) 的参数模型拟合到每个 $K$ 值下 55 次独立运行算得的经验平均值上，覆盖每个数据集与验证策略。具体而言，我们遵循（Hoffmann et al., 2022）用 L-BFGS-B 算法优化一个平滑近似。为确保对观测选择准确率中离群点或重尾噪声的数值稳定性与稳健性，我们最小化预测值与经验均值之间的 Huber 损失。Huber 损失对小残差呈二次、对大残差呈线性，使其比均方误差（MSE）对离群点更不敏感，同时保持梯度优化所需的平滑可微性。它定义为，

$$
L_{\delta}(r)=\begin{cases}\frac{1}{2}r^{2}&\text{若 }|r|\leq\delta\\ \delta\left(|r|-\frac{1}{2}\delta\right)&\text{否则}\end{cases}
$$

其中 $\delta>0$ 是控制两种状态间过渡的可调阈值。我们在 $\delta\in\{0.01,0.05,0.1,0.25,0.5\}$ 中搜索以选出拟合最好的值。

此外，我们引入下限与上限参数来约束预测值并建模饱和行为。下限考虑即使在高 $K$ 下也不可消除的失败率，而上限建模可实现表现的上界（如因不完美的验证器或含糊的题目）。最终拟合形式为：

$$
\text{Selection@1}(K)\approx\text{floor}+(\text{ceil}-\text{floor})\cdot\exp(-\zeta K^{-\alpha})\cdot\left(1-(1-\pi)^{K^{\gamma}}\right) \tag{15}
$$

当用固定验证器对回答排序时，我们可以如（Singhi et al., 2025）所述用无偏估计器评估 best-of-$k$ 选择准确率。但对 Weaver 而言，开发集占数据的 1%，且其本身是基于 $K$ 的值选出的。因此回答的排序不再独立于 $K$，给 best-of-$k$ 估计引入偏差。结果，我们转而依赖蒙特卡洛估计来近似 best-of-$k$ 表现：多次采样 $k$ 个回答并计算依赖 $K$ 的验证器下最高排名输出的平均准确率。覆盖率我们用如（Chen et al., 2021）所述的无偏估计器。

图 16 与图 17 以及表 18 展示了不同验证策略随生成数的扩展情况，以及对式 (14) 参数形式的拟合。每种方法都展现出与式 (14) 一致的特有扩展行为。Weaver 展示了对朴素集成与多数投票的改进。表 18 中拟合的参数定量地捕获了这些跨数据集的趋势，提供了式 (15) 参数形式紧密建模经验结果的证据。图 18 与图 19 以及表 19 展示了式 (15) 参数形式的预测表现，表明在 $K$ 的子集上拟合的模型可以外推到未见过的 $K$ 值。

![Refer to caption](2506.18203v3/tables_and_figures/70b_model_base.png)

图 16：70B 模型的 Weaver 扩展趋势拟合

![Refer to caption](2506.18203v3/tables_and_figures/8b_model_base.png)

图 17：8B 模型的 Weaver 扩展趋势拟合。

表 18：图 16 与图 17 中扩展趋势的拟合参数。

| 数据集 | 方法 | 方程 | floor | ceil | $\zeta$ | $\alpha$ | $\pi$ | $\gamma$ | R2 fit | MSE fit | $\delta$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPQA-v2-Diamond (70B) | Pass@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})$ | 0.0000 | 0.9429 | 0.7603 | 0.3475 | X | X | 0.9999 | 0.0000 | 0.5000 |
| GPQA-v2-Diamond (70B) | Weaver | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.3958 | 0.6728 | 0.7320 | 1.5865 | 0.3250 | 0.5053 | 0.9994 | 0.0000 | 0.1000 |
| GPQA-v2-Diamond (70B) | Majority1@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.4283 | 0.4710 | 0.0499 | 1.0000 | 0.1217 | 1.0091 | 0.8634 | 0.0000 | 0.0100 |
| GPQA-v2-Diamond (70B) | Naive Ensemble | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.3921 | 0.6071 | 0.6553 | 1.9147 | 0.4224 | 0.5000 | 0.9975 | 0.0000 | 0.2500 |
| MATH-500-v2 (70B) | Pass@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})$ | 0.6262 | 1.0000 | 0.8394 | 0.6427 | X | X | 0.9994 | 0.0000 | 0.2500 |
| MATH-500-v2 (70B) | Weaver | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.7870 | 0.9371 | 3.3908 | 3.0000 | 0.2869 | 0.5000 | 0.9958 | 0.0000 | 0.1000 |
| MATH-500-v2 (70B) | Majority1@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.7747 | 0.8238 | 10.0000 | 2.1433 | 0.0885 | 2.4951 | 0.8655 | 0.0001 | 0.1000 |
| MATH-500-v2 (70B) | Naive Ensemble | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.7883 | 0.9282 | 4.0033 | 3.0000 | 0.2573 | 0.5000 | 0.9961 | 0.0000 | 0.0100 |
| MMLU-Pro-v2 (70B) | Pass@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})$ | 0.0000 | 0.9828 | 0.3303 | 0.3465 | X | X | 0.9967 | 0.0000 | 0.2500 |
| MMLU-Pro-v2 (70B) | Weaver | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.6912 | 0.9148 | 1.5284 | 3.0000 | 0.2764 | 0.5000 | 0.9987 | 0.0000 | 0.1000 |
| MMLU-Pro-v2 (70B) | Majority1@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.6933 | 0.7399 | 0.0498 | 1.0001 | 0.1531 | 1.0123 | 0.9451 | 0.0000 | 0.0100 |
| MMLU-Pro-v2 (70B) | Naive Ensemble | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.6969 | 0.8874 | 1.7834 | 3.0000 | 0.2403 | 0.5000 | 0.9944 | 0.0000 | 0.2500 |
| MMLU-College-v2 (70B) | Pass@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})$ | 0.5924 | 0.9744 | 0.5071 | 0.5682 | X | X | 0.9982 | 0.0000 | 0.0100 |
| MMLU-College-v2 (70B) | Weaver | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.8234 | 0.9477 | 4.4129 | 3.0000 | 0.3622 | 0.5000 | 0.9987 | 0.0000 | 0.0100 |
| MMLU-College-v2 (70B) | Majority1@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.8197 | 0.8412 | 0.0498 | 1.0001 | 0.2057 | 1.0173 | 0.8912 | 0.0000 | 0.0100 |
| MMLU-College-v2 (70B) | Naive Ensemble | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.8235 | 0.9266 | 3.8766 | 3.0000 | 0.3012 | 0.5000 | 0.9925 | 0.0000 | 0.0500 |
| GPQA-v2-Diamond (8B) | Pass@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})$ | 0.2262 | 0.9926 | 2.5454 | 0.8474 | X | X | 0.9996 | 0.0000 | 0.1000 |
| GPQA-v2-Diamond (8B) | Weaver | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.2463 | 0.4549 | 0.0534 | 1.0020 | 0.1953 | 0.7089 | 0.9948 | 0.0000 | 0.0500 |
| GPQA-v2-Diamond (8B) | Majority1@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.2783 | 0.3029 | 1.2431 | 0.6756 | 0.0630 | 2.5000 | 0.5929 | 0.0000 | 0.0500 |
| GPQA-v2-Diamond (8B) | Naive Ensemble | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.2359 | 0.3727 | 0.0701 | 1.0016 | 0.3871 | 0.5000 | 0.9408 | 0.0001 | 0.0100 |
| MATH-500-v2 (8B) | Pass@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})$ | 0.4099 | 1.0000 | 1.7182 | 0.8949 | X | X | 0.9976 | 0.0001 | 0.0100 |
| MATH-500-v2 (8B) | Weaver | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.4110 | 0.7440 | 0.0785 | 1.0033 | 0.3333 | 0.5036 | 0.9984 | 0.0000 | 0.0100 |
| MATH-500-v2 (8B) | Majority1@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.5058 | 0.7038 | 5.1187 | 1.0175 | 0.0666 | 2.5000 | 0.9964 | 0.0000 | 0.0500 |
| MATH-500-v2 (8B) | Naive Ensemble | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.5071 | 0.7508 | 1.8068 | 3.0000 | 0.2890 | 0.5000 | 0.9796 | 0.0001 | 0.0100 |
| MMLU-Pro-v2 (8B) | Pass@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})$ | 0.3906 | 1.0000 | 1.9045 | 0.7590 | X | X | 0.9991 | 0.0000 | 0.0100 |
| MMLU-Pro-v2 (8B) | Weaver | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.4764 | 0.6846 | 2.7876 | 3.0000 | 0.2136 | 0.6141 | 0.9985 | 0.0000 | 0.2500 |
| MMLU-Pro-v2 (8B) | Majority1@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.4439 | 0.5662 | 0.1136 | 0.9916 | 0.2787 | 0.6659 | 0.9084 | 0.0001 | 0.0100 |
| MMLU-Pro-v2 (8B) | Naive Ensemble | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.4771 | 0.7025 | 2.8863 | 3.0000 | 0.1728 | 0.5181 | 0.9986 | 0.0000 | 0.1000 |
| MMLU-College-v2 (8B) | Pass@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})$ | 0.4316 | 0.9924 | 0.9887 | 0.9123 | X | X | 0.9994 | 0.0000 | 0.5000 |
| MMLU-College-v2 (8B) | Weaver | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.6226 | 0.8494 | 1.2646 | 3.0000 | 0.3346 | 0.5000 | 0.9958 | 0.0000 | 0.2500 |
| MMLU-College-v2 (8B) | Majority1@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.6359 | 0.7368 | 1.0929 | 0.5130 | 0.0576 | 2.5000 | 0.9949 | 0.0000 | 0.0500 |
| MMLU-College-v2 (8B) | Naive Ensemble | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.6283 | 0.8085 | 1.4279 | 3.0000 | 0.3914 | 0.5000 | 0.9845 | 0.0000 | 0.0100 |

![Refer to caption](2506.18203v3/tables_and_figures/70b_model_pred.png)

图 18：70B 模型的 Weaver 扩展趋势预测

![Refer to caption](2506.18203v3/tables_and_figures/8b_model_pred.png)

图 19：8B 模型的 Weaver 扩展趋势预测

表 19：用 90% 数据拟合的图 18 与图 19 中扩展趋势的参数。

| 数据集 | 方法 | 方程 | floor | ceil | $\zeta$ | $\alpha$ | $\pi$ | $\gamma$ | R2 fit | MSE fit | MSE pred | $\delta$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPQA-v2-Diamond (70B) | Pass@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})$ | 0.0000 | 0.9357 | 0.7534 | 0.3537 | X | X | 0.9999 | 0.0000 | 0.0000 | 0.1000 |
| GPQA-v2-Diamond (70B) | Weaver | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.4050 | 0.6756 | 0.9195 | 1.6227 | 0.3163 | 0.5000 | 0.9993 | 0.0000 | 0.0000 | 0.0500 |
| GPQA-v2-Diamond (70B) | Majority1@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.4320 | 0.4678 | 0.0707 | 0.9864 | 0.0414 | 1.6541 | 0.8601 | 0.0000 | 0.0001 | 0.0100 |
| GPQA-v2-Diamond (70B) | Naive Ensemble | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.3809 | 0.6061 | 0.5211 | 1.9075 | 0.4360 | 0.5000 | 0.9972 | 0.0000 | 0.0000 | 0.0500 |
| MATH-500-v2 (70B) | Pass@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})$ | 0.6639 | 0.9952 | 0.9836 | 0.6936 | X | X | 0.9995 | 0.0000 | 0.0000 | 0.0100 |
| MATH-500-v2 (70B) | Weaver | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.7869 | 0.9339 | 3.5000 | 3.0000 | 0.2985 | 0.5000 | 0.9954 | 0.0000 | 0.0000 | 0.0500 |
| MATH-500-v2 (70B) | Majority1@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.7747 | 0.8241 | 10.0000 | 2.1272 | 0.0888 | 2.4999 | 0.8560 | 0.0001 | 0.0000 | 0.0500 |
| MATH-500-v2 (70B) | Naive Ensemble | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.7879 | 0.9221 | 4.2081 | 3.0000 | 0.2789 | 0.5000 | 0.9966 | 0.0000 | 0.0000 | 0.1000 |
| MMLU-Pro-v2 (70B) | Pass@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})$ | 0.0000 | 0.9785 | 0.3263 | 0.3543 | X | X | 0.9959 | 0.0000 | 0.0000 | 0.1000 |
| MMLU-Pro-v2 (70B) | Weaver | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.6912 | 0.9148 | 1.5277 | 3.0000 | 0.2765 | 0.5000 | 0.9984 | 0.0000 | 0.0000 | 0.2500 |
| MMLU-Pro-v2 (70B) | Majority1@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.6923 | 0.7379 | 0.0495 | 1.0001 | 0.1711 | 1.0148 | 0.9481 | 0.0000 | 0.0000 | 0.0500 |
| MMLU-Pro-v2 (70B) | Naive Ensemble | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.6979 | 0.8907 | 1.8452 | 3.0000 | 0.2327 | 0.5000 | 0.9931 | 0.0000 | 0.0000 | 0.1000 |
| MMLU-College-v2 (70B) | Pass@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})$ | 0.7723 | 0.9655 | 1.3237 | 0.7746 | X | X | 0.9987 | 0.0000 | 0.0000 | 0.1000 |
| MMLU-College-v2 (70B) | Weaver | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.8184 | 0.9436 | 2.2897 | 2.0761 | 0.4148 | 0.5000 | 0.9979 | 0.0000 | 0.0000 | 0.2500 |
| MMLU-College-v2 (70B) | Majority1@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.8196 | 0.8413 | 0.0498 | 1.0001 | 0.2051 | 1.0153 | 0.8814 | 0.0000 | 0.0000 | 0.0100 |
| MMLU-College-v2 (70B) | Naive Ensemble | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.8234 | 0.9262 | 3.9001 | 3.0000 | 0.3036 | 0.5000 | 0.9909 | 0.0000 | 0.0000 | 0.1000 |
| GPQA-v2-Diamond (8B) | Pass@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})$ | 0.2223 | 0.9976 | 2.4975 | 0.8328 | X | X | 0.9996 | 0.0000 | 0.0000 | 0.2500 |
| GPQA-v2-Diamond (8B) | Weaver | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.2316 | 0.4678 | 0.0559 | 1.0027 | 0.2347 | 0.5940 | 0.9965 | 0.0000 | 0.0002 | 0.0100 |
| GPQA-v2-Diamond (8B) | Majority1@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.2773 | 0.2979 | 0.1335 | 0.9633 | 0.0479 | 2.5000 | 0.5476 | 0.0000 | 0.0001 | 0.0500 |
| GPQA-v2-Diamond (8B) | Naive Ensemble | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.2871 | 0.3845 | 8.5633 | 3.0000 | 0.2431 | 0.5000 | 0.9643 | 0.0000 | 0.0001 | 0.0100 |
| MATH-500-v2 (8B) | Pass@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})$ | 0.3986 | 1.0000 | 1.6393 | 0.8786 | X | X | 0.9976 | 0.0001 | 0.0001 | 0.0100 |
| MATH-500-v2 (8B) | Weaver | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.4149 | 0.7417 | 0.0750 | 1.0042 | 0.3261 | 0.5179 | 0.9981 | 0.0000 | 0.0000 | 0.0100 |
| MATH-500-v2 (8B) | Majority1@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.5061 | 0.6976 | 5.9901 | 1.1205 | 0.0782 | 2.5000 | 0.9960 | 0.0000 | 0.0000 | 0.0500 |
| MATH-500-v2 (8B) | Naive Ensemble | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.5009 | 0.7342 | 1.6358 | 3.0000 | 0.3321 | 0.5000 | 0.9803 | 0.0001 | 0.0005 | 0.0100 |
| MMLU-Pro-v2 (8B) | Pass@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})$ | 0.3877 | 1.0000 | 1.8798 | 0.7549 | X | X | 0.9990 | 0.0000 | 0.0000 | 0.1000 |
| MMLU-Pro-v2 (8B) | Weaver | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.4770 | 0.6937 | 3.1648 | 3.0000 | 0.2172 | 0.5705 | 0.9986 | 0.0000 | 0.0001 | 0.0500 |
| MMLU-Pro-v2 (8B) | Majority1@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.4663 | 1.0000 | 2.4923 | 0.1016 | 0.0362 | 2.5000 | 0.9600 | 0.0001 | 0.0002 | 0.0500 |
| MMLU-Pro-v2 (8B) | Naive Ensemble | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.4777 | 0.7207 | 3.0170 | 3.0000 | 0.1613 | 0.5000 | 0.9987 | 0.0000 | 0.0000 | 0.0100 |
| MMLU-College-v2 (8B) | Pass@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})$ | 0.4442 | 0.9912 | 1.0258 | 0.9265 | X | X | 0.9993 | 0.0000 | 0.0000 | 0.5000 |
| MMLU-College-v2 (8B) | Weaver | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.6178 | 0.8447 | 1.1473 | 3.0000 | 0.3523 | 0.5000 | 0.9957 | 0.0000 | 0.0001 | 0.2500 |
| MMLU-College-v2 (8B) | Majority1@K | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.6254 | 0.7186 | 0.5765 | 0.9281 | 0.2058 | 1.2287 | 0.9736 | 0.0000 | 0.0001 | 0.0100 |
| MMLU-College-v2 (8B) | Naive Ensemble | $y=\mathrm{floor}+(\mathrm{ceil}-\mathrm{floor})\cdot\exp(-\zeta\cdot K^{-\alpha})(1-(1-\pi)^{K^{\gamma}})$ | 0.6074 | 0.9813 | 1.2560 | 0.1636 | 0.3060 | 2.4651 | 0.9988 | 0.0000 | 0.0000 | 0.0100 |

### C.4 扩展候选生成

图 20：各验证系统的假阳性率

表 20：8B 模型的 Weaver 在所有数据集上超过多数投票与朴素集成：候选用 Llama 3.1 8B Instruct 生成，弱验证器为 8B 参数或更小。

| | 方法 | 生成数 ($K$) | MATH500 | GPQA | MMLU College | MMLU Pro | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 基线 | 首个样本 | 1 | 49.8% | 28.3% | 64.1% | 46.6% | 47.2% |
| | 多数投票 | 100 | 69.0% | 30.5% | 72.7% | 56.4% | 57.2% |
| | RewardBench 排名第一 RM（Lambert et al., 2024） | 100 | 73.8% | 25.4% | 70.1% | 53.4% | 55.7% |
| | RewardBench Top-10 RM 集成（Lambert et al., 2024） | 100 | 70.2% | 22.1% | 73.9% | 49.4% | 53.9% |
| | 多智能体验证（Lifshitz et al., 2025） | 100 | 65.4% | 31.4% | 70.5% | 55.2% | 55.6% |
| | 自验证（Zhao et al.） | 100 | 71.4% | 32.2% | 70.4% | 53.0% | 56.8% |
| | **Weaver** | **100** | **80.0%** | **47.1%** | **85.7%** | **67.2%** | **70.0%** |
| | GPT-4o-mini | 1 | 76.8% | 38.4% | 82.2% | 61.8% | 64.8% |
| | Claude 3.5 Haiku | 1 | 70.0% | 36.4% | 75.9% | 65.2% | 61.9% |
| | Oracle 验证器（Pass@100） | 100 | 99.2% | 95.2% | 98.5% | 96.8% | 97.4% |

![Refer to caption](2506.18203v3/8B_ScalingPlots_Fig.png)

图 21：Weaver 扩展——8B 生成与模型

### C.5 扩展验证器数量

在表 21 中，我们给出扩展验证器分数的结果。我们注意到，对通常确定性的奖励模型（RM）（Lambert et al., 2024；Song et al., 2025），必须通过改变提示获得多个分数；对 LM 裁判，我们可以改变提示或采样温度以从同一模型生成多样输出（表 21）。我们发现，对 RM 与 LM 裁判两类弱验证器，扩展模型数量都比通过提示调优或温度变化从同一模型采样多个评估带来更好的表现。不过我们注意到这些方法是互补的。

把弱验证器分为 RM 与 LM 裁判单独看时，我们发现增加 LM（裁判）平均分别带来 5.4% 与 6.1% 的增益（表 21）。相比之下，从单个 RM 或 LM 裁判采样更多分数平均只带来 0.8% 与 1.1% 的增益。这些结果表明，利用多个验证器的互补优势可能比从单个验证器引出多次判断更有效。C.7 节提供验证器提示的更多细节。最后，图 22 展示了「扩展验证器数量」与「增加单个验证器的分数数量」之间的权衡，表明当样本数增加、覆盖率上升时，扩展验证器是有帮助的。

表 21：多验证器集成优于单验证器增加采样：候选用 Llama 3.3 70B Instruct 生成，弱验证器规模从 8B 到 72B 参数。提示细节见附录 C.7。

| 方法 | MATH500 | GPQA | MMLU Pro |
| --- | --- | --- | --- |
| 首个样本 | 78.0% | 42.9% | 69.9% |
| 多数投票 | 83.0% | 47.4% | 74.4% |
| 最佳奖励模型（1 个分数） | 94.4% | 58.4% | 81.8% |
| 最佳奖励模型（5 个分数，5 个提示） | 93.2% | 55.3% | 82.5% |
| Top-5 最准确奖励模型 | 95.4% | 64.1% | 87.3% |
| 最佳 LM 裁判（1 个分数） | 90.2% | 61.1% | 79.5% |
| 最佳 LM 裁判（5 个分数，5 个提示） | 88.1% | 57.2% | 80.8% |
| Top-5 最准确 LM 裁判 | 93.4% | 65.2% | 85.4% |

![Refer to caption](2506.18203v3/tables_and_figures/heatmap_verifier_vs_samples_MMLU-Pro-v2_70B_verifierall_from_best.png)

图 22：Weaver 从扩展生成与验证器获得的性能改进：增加候选生成与可用弱验证器通常都能改进表现。

图 22 展示验证器数量与重复生成如何交互影响成功率。我们观察到，增加生成数量往往比只增加验证器数量更有效——但只有配上正确的验证策略才行。例如，验证器的朴素集成即便增加生成也会进入平台期，而 Weaver 沿两条轴都持续改进。这凸显了生成多样性是比验证器数量更强的性能驱动力，也凸显了 Weaver 这类弱监督方法对充分利用该多样性的必要性。我们在附录 C.3 中展示其他数据集的验证-生成权衡。

### C.6 Weaver 蒸馏

![Refer to caption](2506.18203v3/distillation_diagram_fig.png)

图 23：Weaver 蒸馏概览（第 6 节）

对 Weaver 蒸馏的损失函数，我们使用了带 Adam（Kingma & Ba, 2017）的交叉熵损失。我们的分类架构由单个线性分类层组成，输入施加 0.1 的 dropout，输入由 $[CLS]$ token 的最终隐状态组成。关于学习动态，我们通过 Sentence-Transformers 库（Reimers & Gurevych, 2020）实现了线性预热与线性衰减，在所有实验设置中采用 5e-6 的学习率与 64 的训练批大小。

![Refer to caption](2506.18203v3/WeaverDistilledParetoFrontiers_fig.png)

图 24：Weaver Distilled——帕累托前沿：∗我们在 80:20 划分上训练/评估。

表 22：不同训练集规模下 Weaver 与朴素集成的蒸馏比较

| 方法 | 数据集 | 训练集占整个数据集百分比：5% | 10% | 20% | 50% | 80% | 完整系统 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Weaver | MATH500 | 78.4% | 80.7% | 83.9% | 88.2% | 91.4% | 93.4% |
| | GPQA Diamond | 42.6% | 46.8% | 52.7% | 63.1% | 71.8% | 73.2% |
| | MMLU College | 83.5% | 85.2% | 87.6% | 91.0% | 93.1% | 94.9% |
| | MMLU Pro | 69.2% | 72.5% | 76.8% | 83.7% | 87.8% | 90.2% |
| 朴素集成 | MATH500 | 77.8% | 79.6% | 82.1% | 86.4% | 89.1% | 92.4% |
| | GPQA Diamond | 42.1% | 44.7% | 48.9% | 56.2% | 62.8% | 66.2% |
| | MMLU College | 84.0% | 85.3% | 87.2% | 90.8% | 93.5% | 95.1% |
| | MMLU Pro | 69.5% | 71.8% | 74.9% | 80.3% | 84.7% | 87.4% |

### C.7 单个验证器优化

虽然 Weaver 主要聚焦聚合多个弱验证器以改进整体验证质量，本附录探索优化单个验证器的互补技术。如论文前面所述，现有弱验证器往往受高假阳性率之苦（Stroebl et al., 2024），这会限制其效力——即便在集成内部。

随着我们扩展重复样本数量并使用多个验证器，每个验证器的精确率相对召回率变得越来越重要。当有许多候选解可用时，只要验证器的正例预测高度可靠（高精确率），它就可以承受漏掉一些正确解（假阴性）。

这一观察促使我们探索通过提示优化等方法增强单个验证器质量——以极少或零标注数据定制验证器提示，最大化（尤其是）精确率。

#### C.7.1 LM 裁判提示优化

LM 裁判常受位置偏差（偏好特定位置的答案）、冗长偏差（偏好更长的答案）与自我增强偏差（偏好与自身生成模式相似的答案）之苦（Zheng et al., 2023；Li et al., 2024），表明其对系统与输入提示设计的敏感性。

在我们的 Weaver 实验中，我们为 LM 裁判验证器使用了固定的手工提示。然而优化这些提示有可能改进单个验证器的精确率与可靠性。多智能体验证（Lifshitz et al., 2025）通过为特定验证方面精心设计专门提示展示了这一点。

我们探索用 DSPy（Khattab et al., 2023）系统地优化验证器提示——一个开源库，提供通过在度量函数引导下对提示候选做离散搜索来优化语言模型提示的算法。DSPy 优化的工作方式是生成、评估并精炼提示，以在小标注数据集上最大化任务表现。

实验设置：我们考察提示优化的两个维度：(1) 优化空间扩展，逐步扩大优化器可修改的范围，从仅系统指令（0-shot）到包含 3 个示范（3-shot）与 5 个示范（5-shot）；(2) 训练数据规模扩展，把标注数据从 1% 变到 16%，以确定有效提示优化需要多少数据。

我们的实验设置使用包含指令-生成对的训练样本。由于我们的数据集每条指令有多个生成（最多 100 个），我们在划分前按指令分组样本，以防止训练与验证集之间的数据泄漏。我们留出 50% 的数据集指令（每条配 100 个候选生成）用于评估。对优化空间扩展实验，我们随机选择 $n$ 个生成使 $n\times\text{len(dataset)}/2=250$，在保持训练集大小固定的同时最大化训练集多样性。对数据规模实验，我们按 $\lceil\text{num\_problems\_in\_dataset}\times(\text{train\_percentage}/100)\rceil$ 计算指令数，对每条指令选 $\text{samples}=\min(\max(4,\text{num\_problems}\times 2),20)$ 个重复样本以避免过拟合，在数据集的不同百分比（1%、2%、4%、16%）上训练。我们使用一致的随机种子，确保优化运行之间数据集划分一致。

![Refer to caption](2506.18203v3/tables_and_figures/LM_Judge_Prompt_Optimization_Shot_Scaling.png)

图 25：用 250 个标注样本做 LM 裁判提示优化持续带来精确率增益。基线方法（CoT 与 Custom）与不同示范数（0-shot、3-shot、5-shot）的 DSPy 优化提示比较。

结果：图 25 展示了不同数据集与优化配置下的结果。虽然我们没有在所有数据集上观察到清晰的扩展关系（可能由于基于 LLM 的优化的随机性增大），我们观察到最佳裁判相对思维链（CoT）基线裁判平均精确率增益 3.8%。MATH500 展示了最大的精确率跃升 9%，且随优化空间扩大精确率明显改进。

![Refer to caption](2506.18203v3/tables_and_figures/LM_Judge_Prompt_Optimization_Data_Scaling.png)

图 26：扩展 LM 裁判提示优化的训练数据带来适度精确率增益。x 轴为所用训练数据百分比（对数标度），y 轴为精确率。

随训练数据规模的扩展行为（图 26）显示，随训练数据增加精确率有轻微的对数线性改进，但增益因数据集而异。MMLU-College 从额外数据获益最少，其余数据集在训练数据规模从 1% 扩到 16% 时平均获得 3.2% 的精确率提升。

![Refer to caption](2506.18203v3/tables_and_figures/LM_Judge_Precision_Vs_FPR.png)

图 27：优化后的提示往往通过降低假阳性率改进 LM 裁判表现。

（图 27）显示，优化后的提示往往通过降低假阳性率同时改进精确率与准确率——本质上是让裁判在正确性判断上更保守。这在重复采样机制中尤其有价值，更高的精确率能改进整体验证质量。

这些发现表明，提示优化可以成为 Weaver 聚合方法的有价值补充。即便只有有限的标注数据，针对性的提示工程也能增强单个验证器质量，使整个集成受益。仍需进一步研究以定义更系统的验证器提示优化配方。此外，能否把提示优化扩展到判别式奖励模型以获得类似的性能增益，也仍是一个问题。

## 附录 D 杂项

### D.1 计算需求

硬件基础设施。我们的实验使用 4 个计算节点，每个配备 8 块 NVIDIA H100 GPU（每块 80GB HBM3 显存），共 32 块 H100。每个节点配置了 GPU 间的高带宽 NVLink 连接，节点间通信通过 NVIDIA NVLink Switch System 促进，以最小化分布式训练与推理期间的通信开销。

模型并行与分布。对我们的 72B 参数语言模型，我们采用了结合张量并行、流水线并行与数据并行的混合并行策略：

- 每节点内 GPU 间 8 路张量并行
- 跨节点 4 路流水线并行
- 用于批处理的数据并行

存储需求。处理 100GB+ 的数据集需要显著的存储基础设施：

- 每节点 4TB NVMe SSD 用于数据集缓存与检查点
- 100TB 共享网络存储用于完整数据集仓库

软件栈。我们的实验由以下软件支持：

- NVIDIA CUDA 12.2
- PyTorch 2.1 与 NVIDIA NCCL 用于分布式通信
- DeepSpeed ZeRO Stage 3 用于内存优化
- 以 webdataset 格式进行分布式数据加载以高效流式读取
