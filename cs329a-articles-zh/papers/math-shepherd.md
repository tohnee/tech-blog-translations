---
title: "Math-Shepherd：无需人工标注即可逐步验证与强化大语言模型"
title_en: "Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations"
arxiv: 2312.08935
source: https://arxiv.org/abs/2312.08935
crawled: 2026-09-23
translated: 2026-09-23
---

# Math-Shepherd：无需人工标注即可逐步验证与强化大语言模型

> 原文：[Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations](https://arxiv.org/abs/2312.08935) · Stanford CS329A 指定阅读

Peiyi Wang（注：在 DeepSeek-AI 实习期间做出贡献。所属：北京大学多媒体信息处理全国重点实验室；邮箱：[wangpeiyi9979@gmail.com](mailto:)）
Lei Li（所属：香港大学；邮箱：[nlp.lilei@gmail.com](mailto:)）
Zhihong Shao（所属：清华大学；邮箱：[li.14042@osu.edu](mailto:)）
R.X. Xu（所属：DeepSeek-AI；邮箱：[szf@pku.edu.cn](mailto:)）
Damai Dai（所属：北京大学多媒体信息处理全国重点实验室）
Yifei Li（所属：俄亥俄州立大学）
Deli Chen、Y. Wu、Zhifang Sui（所属：北京大学多媒体信息处理全国重点实验室；DeepSeek-AI）

###### 摘要

本文提出了一种创新性的、面向过程的数学过程奖励模型 Math-Shepherd，它为数学问题解答的每一个步骤赋予奖励分数。
Math-Shepherd 的训练使用自动构建的过程级监督数据完成，打破了现有工作严重依赖人工标注的瓶颈。
我们在两种场景下探索 Math-Shepherd 的有效性：
1) 验证：Math-Shepherd 用于对大型语言模型（LLM）生成的多个输出进行重排序；
2) 强化学习：Math-Shepherd 用于通过逐步的近端策略优化（PPO）强化 LLM。
在 Math-Shepherd 的帮助下，一系列开源 LLM 展现了出色的表现。
例如，配合 Math-Shepherd 的逐步 PPO 显著提升了 Mistral-7B 的准确率（GSM8K 上 77.9%→84.1%，MATH 上 28.6%→33.0%）。
在 Math-Shepherd 的验证下，GSM8K 和 MATH 上的准确率可进一步提升至 89.1% 和 43.5%。
我们相信自动过程监督对 LLM 的未来演进具有重大潜力。

|  |
| --- |
|  |

![[Uncaptioned image]](2312.08935v3/fig/bianmu.png)

项目主页：[Math-Shepherd](https://achieved-bellflower-4d6.notion.site/Math-Shepherd-Verify-and-Reinforce-LLMs-Step-by-step-without-Human-Annotations-41b6e73c860840e08697d347f8889bac?pvs=4)

图 1：我们评估了各 LLM 配合 Math-Shepherd 在 GSM8K 和 MATH 数据集上的表现。所有基座模型均用 MetaMath 数据集微调（Yu et al., 2023b）。+SHEPHERD 结果是使用 Math-Shepherd 从 256 个候选中选出最佳者得到的。我们观察到 Math-Shepherd 与不同的 LLM 兼容。GPT-4（早期）的结果来自 Bubeck et al. (2023)。

## 1 引言

大型语言模型（LLM）已在各类任务中展现出卓越能力（Park et al., 2023；Kaddour et al., 2023；Song et al.；Li et al., 2023a；Wang et al., 2023a；Chen et al., 2023；Zheng et al., 2023；Wang et al., 2023c）。
然而，即使是最先进的 LLM，在复杂的多步数学推理问题上仍面临挑战（Lightman et al., 2023；Huang et al., 2023）。
为解决这一问题，先前研究探索了不同的方法路线，如预训练（Azerbayev et al., 2023）、微调（Luo et al., 2023；Yu et al., 2023b；Wang et al., 2023b）、提示（Wei et al., 2022；Fu et al., 2022）以及验证（Wang et al., 2023d；Li et al., 2023b；Zhu et al., 2023；Leviathan et al., 2023）。
在这些技术中，验证近来已成为一种备受青睐的方法。
验证背后的动机是：仅依赖 top-1 结果并不总能产生可靠的输出。验证模型可以对候选回答进行重排序，确保 LLM 输出更高的准确性和一致性。
此外，一个好的验证模型还能为进一步改进 LLM 提供宝贵的反馈（Uesato et al., 2022；Wang et al., 2023b；Pan et al., 2023）。

验证模型大体分为结果奖励模型（ORM）（Cobbe et al., 2021；Yu et al., 2023a）与过程奖励模型（PRM）（Li et al., 2023b；Uesato et al., 2022；Lightman et al., 2023；Ma et al., 2023）。ORM 基于整个生成序列赋予一个置信分数，而 PRM 则逐步评估推理路径。PRM 因若干令人信服的理由而具有优势。其主要好处之一是能够通过定位可能出现的任何错误的具体位置来提供精确反馈，这在强化学习和自动纠错中是宝贵的信号。此外，PRM 在评判推理问题时表现出与人类行为的相似性。如果任何步骤含有错误，最终结果更可能不正确，这与人类判断的运作方式如出一辙。
然而，收集训练 PRM 的数据可能是一个艰辛的过程。Uesato et al. (2022) 和 Lightman et al. (2023) 利用人类标注者提供过程监督标注，以提升 PRM 的表现。
尽管如此，人工标注——尤其对于需要高水平标注技能的复杂多步推理任务——成本相当高昂，这阻碍了 PRM 的发展与实际应用。

为解决这一问题，本文提出一个自动过程标注框架。受蒙特卡洛树搜索启发（Kocsis & Szepesvári, 2006；Coulom, 2006；Silver et al., 2016；Świechowski et al., 2023），我们将一个中间步骤的质量定义为它推导出正确最终答案的潜力。
通过利用答案的正确性，我们可以自动收集步级监督。
具体而言，给定一道带有标准答案的数学题和一个逐步解答，为获得某个特定步骤的标签，我们利用一个微调过的 LLM 从该步骤解码出多条后续推理路径。
我们进一步验证解码得到的最终答案是否与标准答案匹配。
如果某条推理步骤比另一条能推导出更多正确答案，它将被赋予更高的正确性分数。

我们用这种自动方式构建 Math-Shepherd 的训练数据，并在两个广泛使用的数学基准 GSM8K（Cobbe et al., 2021）和 MATH（Hendrycks et al., 2021）上验证我们的想法。
我们在两种场景下探索 Math-Shepherd 的有效性：
1) 验证：Math-Shepherd 用于对 LLM 生成的多个输出进行重排序；
2) 强化学习：Math-Shepherd 用于通过逐步的近端策略优化（PPO）强化 LLM。
在 Math-Shepherd 的验证下，从 7B 到 70B 的一系列开源 LLM 展现了出色的表现。
例如，配合 Math-Shepherd 的逐步 PPO 显著提升了 Mistral-7B 的准确率（GSM8K 上 77.9%→84.1%，MATH 上 28.6%→33.0%）。
借助验证，GSM8K 和 MATH 上的准确率可进一步提升至 89.1% 和 43.5%。
DeepSeek 67B（DeepSeek, 2023）在 Math-Shepherd 验证下于 GSM8K 数据集上达到 93.3%、于 MATH 数据集上达到 48.1% 的准确率。
据我们所知，对于不依赖额外工具的开源模型而言，这些结果前所未有。

我们的主要贡献如下：

1) 我们提出了一个无需人工标注、面向数学推理任务自动构建过程监督数据集的框架。

2) 我们在逐步验证和强化学习两种场景下评估我们的方法。在两个广泛使用的数学基准 GSM8K 和 MATH 上、以及在从 7B 到 70B 的一系列 LLM 上开展的大量实验，证明了我们方法的有效性。

3) 我们实证分析了训练高性能过程奖励模型的关键因素，为借助自动逐步验证与监督提升推理能力的未来方向提供了启示。

## 2 相关工作

##### 提升与激发 LLM 的数学推理能力。

数学推理任务是 LLM 最具挑战性的任务之一。
研究者提出了多种提升或激发 LLM 数学推理能力的方法，大体可分为三组：
1) 预训练：预训练方法（OpenAI, 2023；Anil et al., 2023；Touvron et al., 2023；Azerbayev et al., 2023）在与数学问题相关的大量数据集（如 Proof-Pile 和 ArXiv（Azerbayev et al., 2023））上以简单的下一 token 预测目标预训练 LLM。
2) 微调：微调方法（Yu et al., 2023b；Luo et al., 2023；Yue et al., 2023；Wang et al., 2023b；Gou et al., 2023）同样可以增强 LLM 的数学推理能力。
微调的核心通常在于构建带有思维链推理过程的高质量问答对数据集。
3) 提示：提示方法（Wei et al., 2022；Zhang et al., 2023；Fu et al., 2022；Bi et al., 2023）旨在通过设计提示策略、在不更新模型参数的情况下激发 LLM 的数学推理能力，这非常便捷且实用。

##### 面向 LLM 的数学推理验证。

除了直接提升和激发 LLM 的数学推理潜力之外，
还可以通过额外的验证器从多个解码候选中选出最佳答案，从而提升推理结果。
验证器有两种主要类型：结果奖励模型（ORM）和过程奖励模型（PRM）。ORM 为整个解答分配分数，而 PRM 为推理过程中的每个单独步骤分配分数。
Lightman et al. (2023) 最近的发现表明 PRM 优于 ORM。
除验证之外，奖励模型还能为生成器的进一步训练提供宝贵反馈（Uesato et al., 2022；Pan et al., 2023）。
与 ORM 相比，PRM 提供更细致的反馈，展现出更大的增强生成器的潜力（Wu et al., 2023）。
然而，训练 PRM 需要昂贵的人工标注数据集（Uesato et al., 2022；Lightman et al., 2023），这阻碍了 PRM 的发展与实际应用。
因此，本文旨在构建一个无需人工标注的面向数学推理的 PRM，并在验证和强化学习两种场景下探索该自动 PRM 的有效性。

## 3 方法

本节中，我们首先给出评估奖励模型表现的任务形式化（3.1 节）。
随后，我们概述两类典型的奖励模型：ORM 与 PRM（3.2 节）。
接着，我们介绍自动构建 PRM 训练数据集的方法（3.3 节），打破现有工作严重依赖人工标注的瓶颈（Uesato et al., 2022；Lightman et al., 2023）。

### 3.1 任务形式化

我们在两种场景下评估奖励模型的表现：

##### 验证

遵循 Lightman et al. (2023)，我们考虑 best-of-N 选择的评估范式。
具体而言，给定测试集中的一道问题 $p$，我们从生成器采样 N 个候选解答。这些候选随后由奖励模型打分，得分最高的解答被选为最终答案。
更强的奖励模型提升了选中包含正确答案的解答的可能性，从而提高 LLM 求解数学题的成功率。

##### 强化学习

我们还使用自动构建的 PRM 以逐步 PPO 监督 LLM。在该场景下，我们评估 LLM 贪心解码输出的准确率。
更强的奖励模型有助于训练更高性能的 LLM。

### 3.2 数学问题的奖励模型

##### ORM

给定数学问题 $p$ 及其解答 $s$，ORM（$P\times S\to\mathbb{R}$）为 $s$ 赋予单个实数值以指示 $s$ 是否正确。
ORM 通常用交叉熵损失训练（Cobbe et al., 2021；Li et al., 2023b）：

$$
\mathcal{L}_{ORM}=y_{s}\log r_{s}+(1-y_{s})\log(1-r_{s}), \tag{1}
$$

其中 $y_{s}$ 是解答 $s$ 的标准答案标签：若 $s$ 正确则 $y_{s}=1$，否则 $y_{s}=0$。$r_{s}$ 是 ORM 为 $s$ 赋予的 sigmoid 分数。
奖励模型的成功取决于高质量训练数据集的有效构建。由于数学问题通常有确定的答案，我们可以通过两步自动构建 ORM 的训练集：1) 从生成器为某道题采样若干候选解答；2) 通过检查每个采样解答的答案是否正确来为其赋予标签。
尽管用错误推理得到正确答案的假阳性解答会被误判，先前研究已证明这对于训练一个好的 ORM 仍然有效（Lightman et al., 2023；Yu et al., 2023a）。

##### PRM

更进一步，PRM（$P\times S\to\mathbb{R}^{+}$）为 $s$ 的每个推理步骤赋予分数，通常用如下方式训练：

$$
\mathcal{L}_{PRM}=\sum_{i=1}^{K}y_{s_{i}}\log r_{s_{i}}+(1-y_{s_{i}})\log(1-r_{s_{i}}), \tag{2}
$$

其中 $y_{s_{i}}$ 是 $s_{i}$（$s$ 的第 $i$ 步）的标准答案标签，$r_{s_{i}}$ 是 PRM 为 $s_{i}$ 赋予的 sigmoid 分数，$K$ 是 $s$ 的推理步数。Lightman et al. (2023) 还将 PRM 训练概念化为一个三分类问题，其中每一步被分类为「好」「中性」或「坏」。在本文中，我们发现二分类与三分类之间没有太大差异，因此我们将 PRM 训练视为二分类。
与 ORM 相比，PRM 能提供更细致、更可靠的反馈（Lightman et al., 2023）。
然而，目前尚无自动方法可用于构建高质量的 PRM 训练数据集。
先前工作（Uesato et al., 2022；Lightman et al., 2023）通常求助于昂贵的人工标注。虽然 PRM 的表现胜过 ORM（Lightman et al., 2023），但标注成本始终阻碍着 PRM 的发展与应用。

图 2：先前的自动结果标注与我们的自动过程标注之对比。(a)：自动结果标注依据答案的正确性为整个解答 $S$ 赋予一个标签；(b) 自动过程标注使用一个「补全器」（completer）为一个中间步骤（图中为 $s_{1}$）完成 N 个推理过程（图中 N=3），随后基于所有解码答案使用硬估计（HE）与软估计（SE）为该步骤标注。

### 3.3 自动过程标注

本节中，我们提出一个自动过程标注框架，以缓解 PRM 相关的标注成本问题。我们首先定义推理步骤的质量，随后介绍免于人工标注的方案。

#### 3.3.1 定义

受蒙特卡洛树搜索启发（Kocsis & Szepesvári, 2006；Coulom, 2006；Silver et al., 2016；Świechowski et al., 2023），我们将一个推理步骤的质量定义为其推导出正确答案的潜力。
这一判据源于推理过程的首要目标——推理本质上是一种帮助人类或智能体得出有充分依据的结果的认知过程（Huang & Chang, 2023）。因此，一个有潜力推导出有充分依据结果的步骤可以被视为一个好的推理步骤。与 ORM 类似，这一定义也引入了一定程度的噪声。尽管如此，我们发现它有利于有效训练一个好的 PRM。

#### 3.3.2 方案

##### 补全

为量化并估计给定推理步骤 $s_{i}$ 的潜力，
如图 2 所示，
我们使用一个「补全器」从该步骤完成 N 个后续推理过程：$\{(s_{i+1,j},\cdots,s_{K_{j},j},a_{j})\}_{j=1}^{N}$，其中 $a_{j}$ 和 $K_{j}$ 分别是第 $j$ 个已完成解答的解码答案和总步数。
然后，我们基于所有解码答案 $A=\{a_{j}\}_{j=1}^{N}$ 的正确性来估计该步骤的潜力。

##### 估计

本文使用两种方法估计步骤 $s_{i}$ 的质量 $y_{s_{i}}$：硬估计（HE）与软估计（SE）。HE 假设一个推理步骤只要能到达正确答案 $a^{*}$ 就是好的：

$$
y_{s_{i}}^{HE}=\left\{\begin{aligned} 1&&\exists a_{j}\in A,a_{j}=a^{*}\\ 0&&\mathrm{Otherwise}\\ \end{aligned}\right. \tag{3}
$$

SE 将步骤的质量假设为其到达正确答案的频率：

$$
y_{s_{i}}^{SE}=\frac{\sum_{j=1}^{N}\mathbb{I}(a_{j}=a^{*})}{N}. \tag{4}
$$

一旦我们收集到每个步骤的标签，就可以用交叉熵损失训练 PRM。
总之，我们的自动过程标注框架将步骤的质量定义为其推导正确答案的潜力，并通过补全和估计获得每个步骤的标签。

### 3.4 面向验证的排序

遵循 Lightman et al. (2023)，我们使用所有步骤中的最低分来表示 PRM 为一个解答赋予的最终分数。我们还遵循 Li et al. (2023b) 探索自洽性与奖励模型的组合。在这一情境下，我们首先根据最终答案将解答划分为不同的组。随后，我们计算每组的总分。
形式上，基于 N 个候选解答的最终预测答案是：

$$
a_{sc+rm}=\argmax_{a}\sum_{i=1}^{N}\mathbb{I}(a_{i}=a)\cdot RM(p,S_{i}). \tag{5}
$$

其中 $RM(p,S_{i})$ 是 ORM 或 PRM 为问题 $p$ 的第 $i$ 个解答赋予的分数。

### 3.5 基于过程监督的强化学习

获得 PRM 之后，我们采用强化学习训练 LLM。我们以逐步的方式实现近端策略优化（PPO）。
该方法不同于使用 ORM 的 PPO 的常规策略——后者只在回答结束时给出奖励。相反，我们的逐步 PPO 在每个推理步骤结束时给出奖励。

## 4 实验

##### 数据集

我们使用两个广泛使用的数学推理数据集 GSM8K（Cobbe et al., 2021）和 MATH（Hendrycks et al., 2021）开展实验。
对 GSM8K 数据集，我们在验证和强化学习两种场景下均使用完整测试集。
对 MATH 数据集，在验证场景下，
由于计算成本，我们采用与 Lightman et al. (2023) 测试集相同的子集 MATH500。该子集由 500 道代表性问题组成，我们发现子集评估与全量评估产生相似的结果。
为评估不同验证方法，我们为每道测试题生成 256 个候选解答。
我们报告 3 组采样结果的平均准确率。
在强化学习场景下，我们使用完整测试集评估模型表现。
我们使用 MetaMATH（Yu et al., 2023b）训练 LLM。

|  |  |  |  |
| --- | --- | --- | --- |
| 模型 | 验证器 | GSM8K | MATH500 |
| LLaMA2-70B: MetaMATH | 自洽性 | 88.0 | 39.4 |
| ORM | 91.8 | 40.4 |
| 自洽性 + ORM | 92.0 | 42.0 |
| Math-Shepherd（本文） | 93.2 | 44.5 |
| 自洽性 + Math-Shepherd（本文） | 92.4 | 45.2 |
| LLemma-34B: MetaMATH | 自洽性 | 82.6 | 44.2 |
| ORM | 90.0 | 43.7 |
| 自洽性 + ORM | 89.6 | 45.4 |
| Math-Shepherd（本文） | 90.9 | 46.0 |
| 自洽性 + Math-Shepherd（本文） | 89.7 | 47.3 |
| DeepSeek-67B: MetaMATH | 自洽性 | 88.2 | 45.4 |
| ORM | 92.6 | 45.3 |
| 自洽性 + ORM | 92.4 | 47.0 |
| Math-Shepherd（本文） | 93.3 | 47.0 |
| 自洽性 + Math-Shepherd（本文） | 92.5 | 48.1 |

表 1：不同 LLM 在 GSM8K 和 MATH 上使用不同验证策略的表现。奖励模型分别基于 LLama2-70B 和 LLemma-34B 在 GSM8K 和 MATH 上训练。验证基于 256 个输出。

##### 参数设置

我们的实验基于一系列大型语言模型：LLaMA2-7B/13B/70B（Touvron et al., 2023）、LLemma-7B/34B（Azerbayev et al., 2023）、Mistral-7B（Jiang et al., 2023）和 DeepSeek-67B（DeepSeek, 2023）。
我们在 MetaMATH 上训练生成器和补全器各 3 个 epoch。
Mistral-7B 的训练学习率为 5e-6。
其他模型的学习率分别设为：7B/13B 用 2e-5，34B 用 1e-5，67B/70B 用 6e-6。
为构建 ORM 和 PRM 的训练数据集，我们在 GSM8K 和 MATH 训练集上训练 7B 和 13B 模型各 1 个 epoch。随后，我们从每个模型为每道题采样 15 个解答构成训练集。接着，我们去除重复解答并为每个解答的每一步标注。
我们使用 LLemma-7B 作为补全器，解码数量 N=8。
最终，我们为 GSM8K 获得约 17 万个解答，为 MATH 获得约 27 万个解答。
对于验证，
我们选择 LLaMA2-70B 和 LLemma-34B 作为基座模型，分别训练 GSM8K 和 MATH 的奖励模型。
对于强化学习，
我们选择 Mistral-7B 作为基座模型训练奖励模型，并用它监督 LLama2-7B 和 Mistral-7B 生成器。
奖励模型训练 1 个 epoch，学习率 1e-6。
为方便起见，我们使用硬估计版本训练 PRM，因为它允许我们通过选择两个特殊 token 表示「有潜力」和「无潜力」标签来利用标准的语言建模流水线，从而无需任何特定的模型改动。
强化学习中，LLaMA2-7B 和 Mistral-7B 的学习率分别为 4e-7 和 1e-7。
Kullback-Leibler 系数设为 0.04。
我们实现余弦学习率调度器，最小学习率设为 1e-8。
我们使用 hfai（<https://doc.hfai.high-flyer.cn/index.html>）提供的 3D 并行来训练所有模型，最大序列长度为 512。

##### 基线与指标

在验证场景下，遵循 Lightman et al. (2023)，我们通过将我们的奖励模型与自洽性（多数投票）及结果奖励模型比较来评估其表现。best-of-N 解答的准确率用作评估指标。
对 PRM，采用所有步骤中的最低分来表示一个解答的最终分数。
在强化学习场景下，我们将我们的逐步监督与 ORM 提供的结果监督以及拒绝采样微调（RFT）（Yuan et al., 2023）进行比较，我们为 MetaMATH 中的每个问题采样 8 个回答用于 RFT。
我们使用 LLM 贪心解码输出的准确率来评估表现。

### 4.1 主要结果

##### Math-Shepherd 作为验证器

表 1 展示了各方法在 GSM8K 和 MATH 上的表现比较。
我们发现：
1) 作为验证器，Math-Shepherd 在两个数据集上、配合所有生成器均一致优于自洽性和 ORM。具体而言，在 Math-Shepherd 的加持下，DeepSeek-67B 在 GSM8K 和 MATH 上分别达到 93.3% 和 48.1% 的准确率；
2) 与 GSM8K 相比，PRM 在更具挑战性的 MATH 数据集上相对 ORM 取得更大优势；
这一结果与 Uesato et al. (2022) 和 Lightman et al. (2023) 的发现一致。前者发现 PRM 与 ORM 在 GSM8K 上产生相似结果，而后者表明 PRM 在 MATH 数据集上显著优于 ORM。
这可归因于 GSM8K 数据集相对 MATH 较为简单，即 GSM8K 数据集解题所需步骤更少。
因此，ORM 在处理这一特定数据集时运作良好；
3) 在 GSM8K 中，与自洽性结合时性能有所下降，而在 MATH 中性能提升。这些结果表明，如果奖励模型对某项任务已足够强大，将其与自洽性结合可能损害验证表现。

|  |  |  |
| --- | --- | --- |
| 模型 | GSM8K | MATH |
| LLaMA2-7B: MetaMATH | 66.6 | 19.2 |
| + RFT | 68.5 | 19.9 |
| + ORM-PPO | 70.8 | 20.8 |
| + Math-Shepherd-逐步-PPO（本文） | 73.2 | 21.6 |
| Mistral-7B: MetaMATH | 77.9 | 28.6 |
| + RFT | 79.0 | 29.9 |
| + ORM-PPO | 81.8 | 31.3 |
| + Math-Shepherd-逐步-PPO（本文） | 84.1 | 33.0 |

表 2：不同 7B 模型在 GSM8K 和 MATH 上贪心解码的表现。我们使用 MetaMATH 中的问题进行 RFT 和 PPO 训练。LLaMA2-7B 和 Mistral-7B 均由 Mistral-7B-ORM 和 Mistral-7B-Math-Shepherd 监督。

##### Math-Shepherd 作为强化学习中的奖励模型

表 2 展示了不同 LLM 贪心解码输出的表现。
如表所示：
1) 逐步 PPO 显著提升了两个监督微调模型的性能。
例如，配合逐步 PPO 的 Mistral-7B 在 GSM8K 和 MATH 数据集上分别达到 84.1% 和 33.0%；
2) RFT 仅轻微提升模型性能，我们相信这是因为 MetaMATH 已经实施了一些类似 RFT 的数据增广策略；
3) 使用 ORM 的普通 PPO 也能提升模型性能。
然而，它的表现不如由 Math-Shepherd 监督的逐步 PPO，展示了逐步监督的潜力。

##### Math-Shepherd 同时作为奖励模型与验证器

我们还把强化学习与验证结合起来。
如表 3 所示：
1) 强化学习与验证互补。例如在 MATH 上，以自洽性为验证器时，逐步 PPO 的 Mistral-7B 比监督微调的 Mistral-7B 高出 7.2% 的准确率；
这一差距甚至大于贪心解码结果的差距，即 4.4%；
2) 强化学习之后，仅用奖励模型的普通验证方法劣于自洽性，我们认为原因是初始奖励模型已不足以监督 PPO 之后更强大的模型。
这些结果也展示了迭代强化学习的潜力，我们将其留给未来工作。

## 5 分析

### 5.1 不同候选解答数量下的表现

图 3 展示了各种策略应用于 1 到 256 不同数量候选时在两个基准上的表现比较。关键观察如下：
1) 与 ORM 和多数投票相比，PRM 展现出一致更优的表现，且这种优越程度随 N 增大而更加显著。
2) 在 MATH 上，我们自动标注的数据集优于人工标注的 PRM800K（Lightman et al., 2023）。我们将这一优势归因于分布差距和数据量。具体而言，PRM800K 基于 GPT-4 的输出标注，因此对在 MetaMath 上微调的开源 LLaMA 模型的输出存在偏差。此外，就数据量而言，我们的自动奖励模型数据兼具高可扩展性和更低的标注成本。因此，我们的数据集比 PRM800K 提供的大四倍。
总体而言，这些结果进一步凸显了我们方法的有效性与潜力。

|  |  |  |  |
| --- | --- | --- | --- |
| 模型 | 验证器 | GSM8K | MATH500 |
| Mistral-7B: MetaMATH | 自洽性 | 83.9 | 35.1 |
| ORM | 86.2 | 36.4 |
| 自洽性 + ORM | 86.6 | 38.0 |
| Math-Shepherd（本文） | 87.1 | 37.3 |
| 自洽性 + Math-Shepherd（本文） | 86.3 | 38.3 |
| Mistral-7B: MetaMATH | 自洽性 | 87.4 | 42.3 |
| ORM | 87.6 | 41.3 |
| +逐步 PPO（本文） | 自洽性 + ORM | 89.0 | 43.1 |
| Math-Shepherd（本文） | 88.4 | 41.1 |
|  | 自洽性 + Math-Shepherd（本文） | 89.1 | 43.5 |

表 3：强化学习与验证组合的结果。奖励模型基于 Mistral-7B 训练。验证基于 256 个输出。

### 5.2 自动过程标注的质量

本节中，我们探究自动 PRM 数据集的质量。
为此，我们人工标注从 GSM8K 训练集采样的 160 个步骤，并使用不同的补全器从每个步骤推断以获得其标签。我们发现：

图 3：LLaMA2-70B 在 GSM8K 和 MATH 上、不同数量解答候选下使用不同验证策略的表现。

##### 自动过程标注质量令人满意。

图 4(a) 表明，使用在 MetaMATH 上训练的 LLaMA2-70B 作为补全器时，硬估计（HE）的准确率在 N 等于 4 时达到 86%。这表明我们自动构建的数据集质量很高。然而，我们观察到随着 N 进一步增大，所构建数据集的准确率有所下降。我们的分析表明，更大的 N 值可能导致假阳性。

图 4(b) 展示了 SE 与 HE 标签相对人工标注分布的交叉熵损失：随着 N 增大，SE 逐渐更贴近标准分布，而 HE 则未表现出类似行为。
需要指出的是，在 N=4 时 HE 达到 86% 的准确率。理论上，我们可以通过使用 SE 获得超过 86% 准确率的更高质量数据。
然而，我们发现无论用 SE 还是 HE 训练，验证器的表现都没有实质差异。这可能归因于 HE 已经提供了高质量的标注。

此外，我们还深入考察了其他自动过程标注方法。例如，Li et al. (2023b) 使用自然语言推理（NLI）模型和字符串匹配规则来标注给定步骤。
基于 NLI 的方法在某一步与参考解答中的任何一步构成蕴含关系时将其标注为正确。
基于规则的方法在某一步的支持数字与参考解答中任何一步精确匹配时将其标注为正确。
如表 4 所示，我们的标注策略相对这两种方法展现出显著优势。

图 4：GSM8K 上过程标注的质量。(a)：使用不同补全器时过程标注的准确率；(b)：使用不同补全器时过程标注的损失；(c)：使用相同补全器、不同训练数据时过程标注的损失。

| 方法 | 模型 | 准确率（%） | 损失 |
| --- | --- | --- | --- |
| DIVERSE-NLI（Li et al., 2023b） | DeBERTa（He et al., 2020） | 61.3 | 5.43 |
| DIVERSE-NLI（Li et al., 2023b） | LLaMA2-13B | 75.6 | 3.27 |
| DIVERSE-Rule（Li et al., 2023b） | - | 75.0 | 3.43 |
| Math-Shepherd | LLaMA2-13B（N = 4） | 85.0 | 2.05 |

表 4：Li et al. (2023b) 的 NLI/规则自动过程标注方法与我们方法的比较。

##### LLM 补全器的能力对数据质量至关重要。

我们使用补全器为给定步骤完成多条后续推理过程。
因此，我们研究了 LLM 补全器的影响。

图 4(b) 展示了在 MetaMath 上训练的不同补全器的交叉熵损失。结果表明，更大的补全器擅长生成质量更高的数据集。
图 4(c) 描绘了用不同数据集训练的 LLaMA2-70B 的交叉熵损失。「Normal」表示原始 GSM8K 训练数据集；「Weak」指从 Normal 集中剔除问题出现在我们 160 步评估集中的样本后的集合；「Augmented」代表 MetaMath，即 Normal 集的增广版本。

这些发现表明，高质量的训练集使模型能更好地胜任补全器。重要的是，「Weak」集的损失明显大于其他数据集。这一洞察促使我们推断：LLM 应预先学习过相关问题，才能提升其作为补全器的表现。
我们还可以推测，更强的基础模型配合更优的训练数据，可以进一步提升自动标注的质量。

### 5.3 预训练基础模型的影响

图 5：不同尺寸生成器与验证器上不同验证策略的表现。

为对 Math-Shepherd 的有效性开展穷尽评估，我们使用 7B、13B 和 70B 三种模型尺寸进行了多样化的实验。

图 5(a)、5(b) 和图 3(a) 分别展示了 7B、13B 和 70B 生成器搭配同等尺寸奖励模型的结果。显而易见，PRM 在所有尺寸的基座模型上都优于自洽性和 ORM。此外，更大的奖励模型被证明更稳健；例如，70B 奖励模型的准确率随候选解答数量增加而上升，而 7B 奖励模型则呈下降趋势。

图 5(c) 和 5(d) 展示了 7B 与 70B 生成器搭配不同尺寸奖励模型时的表现。这些发现表明，用更大的奖励模型校验较小生成器的输出能显著提升表现。相反，当用较小的奖励模型校验较大生成器的输出时，验证过程相对 SC 反而损害模型表现。
这些结果证实，我们应当使用更强大的奖励模型来校验或监督生成器。

### 5.4 数据数量的影响

我们通过使用不同数量的训练数据，更深入地分析 PRM 与 ORM。如图 6(a) 所示，显然 PRM 展现出更优的数据效率。具体而言，在使用规模适中的训练数据集（即 1 万个实例）时，它比 ORM 高出约 4% 的准确率。此外，PRM 似乎比 ORM 拥有更高的潜力上限。这些观察凸显了 PRM 用于验证的效力。

图 6：(a)：使用不同数量训练数据的不同奖励模型的表现；(b) 不同验证策略在分布外匈牙利全国考试上的表现。

### 5.5 分布外表现

为进一步证明我们方法的有效性，我们在匈牙利全国期末考试（<https://huggingface.co/datasets/keirp/hungarian_national_hs_finals_exam）上开展分布外评估，该考试由 33 道题组成，总分 100 分。
我们用在 MetaMATH 上训练的 LLemma-34B 作为生成器，为每道题生成 256 个候选解答。我们使用 LLemma-34B-ORM 和 LLemma-34B-PRM 为每道题选择解答。
如图 6(b) 所示：1) LLemma-34B-ORM 和 LLemma-34B-PRM 均优于原始 LLemma-34B，表明奖励模型能泛化到其他领域；2) PRM 比 ORM 高出 9 分，进一步证明了 PRM 的优越性。

我们还进行了案例研究，以直观展示 Math-Shepherd 的有效性。
如表 5 所示，面对一道来自匈牙利全国期末考试的问题，我们的 Math-Shepherd 从 256 个候选解答中准确选中了正确解答，而 ORM 则失败了。
此外，Math-Shepherd 展现出卓越的辨别力，精确识别出 ORM 所选解答中的错误步骤。值得注意的是，它识别出第 2 步、第 6 步、第 9 步等处的错误，并随后为这些步骤赋予低于正确解答中各步骤的分数。

| Question | The first term of an arithmetic sequence is 18. The sum of the first six terms of the sequence is equal to the sum of the first seven terms. Show that the sum of the first 13 terms of the sequence is 0 and calculate the 13th term of the sequence. |
| --- | --- |
| Math-Shepherd | Step 1: Let the common difference of the arithmetic sequence be $d$. Math-Shepherd: 0.99. |
|  | Step 2: The sum of the first six terms of the sequence is $18+(18+d)+(18+2d)+(18+3d)+(18+4d)+(18+5d)=108+30d$. Math-Shepherd: 0.85. |
|  | …… |
|  | Step 6: Therefore, $d=-3$. Math-Shepherd: 0.85. |
|  | …… |
|  | Step 8: The 13th term of the sequence is $18-36=-18$. Math-Shepherd: 0.93. ORM Score: 0.73. |
| ORM | Step 1: Let the common difference of the arithmetic sequence be $d$. Math-Shepherd: 0.99. |
|  | Step 2: The sum of the first six terms is $18+(18+d)+(18+2d)+(18+3d)+(18+4d)+(18+5d)=$ 90 + $15d$. Math-Shepherd: 0.53. |
|  | …… |
|  | Step 6: Dividing by $-6$, we find that $d=-2$. Math-Shepherd: 0.38. |
|  | …… |
|  | Step 9: The 13th term of the sequence is $18-26=-8$. Math-Shepherd: 0.38. ORM Score: 0.84. |

表 5：来自匈牙利全国考试的一个案例研究（模型输出展品保留英文原文）。红色文本表示 ORM 未能检测到的错误。

## 6 局限性

本文存在一些局限，我们留给未来工作：

##### 补全过程的计算成本。

为确定每个推理步骤的标签，我们使用「补全器」解码 N 个后续推理过程。我们观察到，随着 N 增大，自动标注的质量也随之提高。然而，这一补全过程需要大量计算资源，可能对我们方法的使用构成限制。尽管存在这一局限，其成本仍显著低于人工标注。
此外，我们乐观地认为，高效推理技术的进步，如投机解码（Xia et al., 2022；Leviathan et al., 2023）和 vLLM（Kwon et al., 2023），可以缓解这一限制。

##### 自动过程标注包含噪声。

与自动结果标注类似，我们的自动过程标注也含有噪声。
尽管如此，我们的实验验证了我们方法训练 PRM 的有效性。特别是，在我们数据集上训练的 PRM 优于人工标注的 PRM800K 数据集（训练出的模型）。
然而，PRM800K 与本研究中所用开源模型生成的候选回答之间存在明显差距，这可能导致 PRM800K 失效。
因此，这种潜在噪声对 PRM 表现的影响仍未确定。人工标注与自动标注的全面比较留待未来研究。此外，我们主张将人工与自动过程标注相结合，可以在构建稳健而高效的过程监督中发挥重要作用。

## 7 结论

本文介绍了一个名为 Math-Shepherd 的面向过程的数学验证器，它为 LLM 在数学问题上的输出的每个步骤赋予奖励分数。Math-Shepherd 的训练使用自动构建的过程级监督数据完成，从而免除了费时费力的人工标注。值得注意的是，这一自动方法与人工标注高度相关。在验证和强化学习两种场景下的大量实验证明了我们方法的有效性。

## 参考文献

- Anil et al. (2023)

  Rohan Anil, Andrew M Dai, Orhan Firat, Melvin Johnson, Dmitry Lepikhin, Alexandre Passos, Siamak Shakeri, Emanuel Taropa, Paige Bailey, Zhifeng Chen, et al.
  Palm 2 technical report.
  *arXiv preprint arXiv:2305.10403*, 2023.
- Azerbayev et al. (2023)

  Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster, Marco Dos Santos, Stephen McAleer, Albert Q Jiang, Jia Deng, Stella Biderman, and Sean Welleck.
  Llemma: An open language model for mathematics.
  *arXiv preprint arXiv:2310.10631*, 2023.
- Bi et al. (2023)

  Zhen Bi, Ningyu Zhang, Yinuo Jiang, Shumin Deng, Guozhou Zheng, and Huajun Chen.
  When do program-of-thoughts work for reasoning?
  *arXiv preprint arXiv:2308.15452*, 2023.
- Bubeck et al. (2023)

  Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric Horvitz, Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg, et al.
  Sparks of artificial general intelligence: Early experiments with gpt-4.
  *arXiv preprint arXiv:2303.12712*, 2023.
- Chen et al. (2023)

  Liang Chen, Yichi Zhang, Shuhuai Ren, Haozhe Zhao, Zefan Cai, Yuchi Wang, Peiyi Wang, Tianyu Liu, and Baobao Chang.
  Towards end-to-end embodied decision making via multi-modal large language model: Explorations with gpt4-vision and beyond.
  *arXiv preprint arXiv:2310.02071*, 2023.
- Cobbe et al. (2021)

  Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, et al.
  Training verifiers to solve math word problems.
  *arXiv preprint arXiv:2110.14168*, 2021.
- Coulom (2006)

  Rémi Coulom.
  Efficient selectivity and backup operators in monte-carlo tree search.
  In *International conference on computers and games*, pp. 72–83. Springer, 2006.
- DeepSeek (2023)

  DeepSeek.
  Deepseek llm: Let there be answers.
  <https://github.com/deepseek-ai/DeepSeek-LLM>, 2023.
- Fu et al. (2022)

  Yao Fu, Hao Peng, Ashish Sabharwal, Peter Clark, and Tushar Khot.
  Complexity-based prompting for multi-step reasoning.
  *arXiv preprint arXiv:2210.00720*, 2022.
- Gou et al. (2023)

  Zhibin Gou, Zhihong Shao, Yeyun Gong, Yujiu Yang, Minlie Huang, Nan Duan, Weizhu Chen, et al.
  Tora: A tool-integrated reasoning agent for mathematical problem solving.
  *arXiv preprint arXiv:2309.17452*, 2023.
- He et al. (2020)

  Pengcheng He, Xiaodong Liu, Jianfeng Gao, and Weizhu Chen.
  Deberta: Decoding-enhanced bert with disentangled attention.
  *arXiv preprint arXiv:2006.03654*, 2020.
- Hendrycks et al. (2021)

  Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt.
  Measuring mathematical problem solving with the math dataset.
  *arXiv preprint arXiv:2103.03874*, 2021.
- Huang & Chang (2023)

  Jie Huang and Kevin Chen-Chuan Chang.
  Towards reasoning in large language models: A survey.
  In Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki (eds.), *Findings of the Association for Computational Linguistics: ACL 2023*, pp. 1049–1065, Toronto, Canada, July 2023. Association for Computational Linguistics.
  doi: 10.18653/v1/2023.findings-acl.67.
  URL <https://aclanthology.org/2023.findings-acl.67>.
- Huang et al. (2023)

  Jie Huang, Xinyun Chen, Swaroop Mishra, Huaixiu Steven Zheng, Adams Wei Yu, Xinying Song, and Denny Zhou.
  Large language models cannot self-correct reasoning yet.
  *arXiv preprint arXiv:2310.01798*, 2023.
- Jiang et al. (2023)

  Albert Q Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, et al.
  Mistral 7b.
  *arXiv preprint arXiv:2310.06825*, 2023.
- Kaddour et al. (2023)

  Jean Kaddour, Joshua Harris, Maximilian Mozes, Herbie Bradley, Roberta Raileanu, and Robert McHardy.
  Challenges and applications of large language models.
  *arXiv preprint arXiv:2307.10169*, 2023.
- Kocsis & Szepesvári (2006)

  Levente Kocsis and Csaba Szepesvári.
  Bandit based monte-carlo planning.
  In *European conference on machine learning*, pp. 282–293. Springer, 2006.
- Kwon et al. (2023)

  Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica.
  Efficient memory management for large language model serving with pagedattention.
  In *Proceedings of the 29th Symposium on Operating Systems Principles*, pp. 611–626, 2023.
- Leviathan et al. (2023)

  Yaniv Leviathan, Matan Kalman, and Yossi Matias.
  Fast inference from transformers via speculative decoding.
  In *International Conference on Machine Learning*, pp. 19274–19286. PMLR, 2023.
- Li et al. (2023a)

  Lei Li, Yuwei Yin, Shicheng Li, Liang Chen, Peiyi Wang, Shuhuai Ren, Mukai Li, Yazheng Yang, Jingjing Xu, Xu Sun, et al.
  M3it: A large-scale dataset towards multi-modal multilingual instruction tuning.
  *arXiv preprint arXiv:2306.04387*, 2023a.
- Li et al. (2023b)

  Yifei Li, Zeqi Lin, Shizhuo Zhang, Qiang Fu, Bei Chen, Jian-Guang Lou, and Weizhu Chen.
  Making language models better reasoners with step-aware verifier.
  In Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki (eds.), *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pp. 5315–5333, Toronto, Canada, July 2023b. Association for Computational Linguistics.
  doi: 10.18653/v1/2023.acl-long.291.
  URL <https://aclanthology.org/2023.acl-long.291>.
- Lightman et al. (2023)

  Hunter Lightman, Vineet Kosaraju, Yura Burda, Harri Edwards, Bowen Baker, Teddy Lee, Jan Leike, John Schulman, Ilya Sutskever, and Karl Cobbe.
  Let’s verify step by step.
  *arXiv preprint arXiv:2305.20050*, 2023.
- Luo et al. (2023)

  Haipeng Luo, Qingfeng Sun, Can Xu, Pu Zhao, Jianguang Lou, Chongyang Tao, Xiubo Geng, Qingwei Lin, Shifeng Chen, and Dongmei Zhang.
  Wizardmath: Empowering mathematical reasoning for large language models via reinforced evol-instruct.
  *arXiv preprint arXiv:2308.09583*, 2023.
- Ma et al. (2023)

  Qianli Ma, Haotian Zhou, Tingkai Liu, Jianbo Yuan, Pengfei Liu, Yang You, and Hongxia Yang.
  Let’s reward step by step: Step-level reward model as the navigators for reasoning.
  *arXiv preprint arXiv:2310.10080*, 2023.
- OpenAI (2023)

  OpenAI.
  GPT-4 technical report.
  *CoRR*, abs/2303.08774, 2023.
  doi: 10.48550/arXiv.2303.08774.
  URL <https://doi.org/10.48550/arXiv.2303.08774>.
- Pan et al. (2023)

  Sarah Pan, Vladislav Lialin, Sherin Muckatira, and Anna Rumshisky.
  Let’s reinforce step by step.
  *arXiv preprint arXiv:2311.05821*, 2023.
- Park et al. (2023)

  Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel Morris, Percy Liang, and Michael S Bernstein.
  Generative agents: Interactive simulacra of human behavior.
  In *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology*, pp. 1–22, 2023.
- Silver et al. (2016)

  David Silver, Aja Huang, Chris J Maddison, Arthur Guez, Laurent Sifre, George Van Den Driessche, Julian Schrittwieser, Ioannis Antonoglou, Veda Panneershelvam, Marc Lanctot, et al.
  Mastering the game of go with deep neural networks and tree search.
  *nature*, 529(7587):484–489, 2016.
- (29)

  Yifan Song, Weimin Xiong, Dawei Zhu, Cheng Li, Ke Wang, Ye Tian, and Sujian Li.
  Restgpt: Connecting large language models with real-world applications via restful apis. corr, abs/2306.06624, 2023. doi: 10.48550.
  *arXiv preprint arXiv.2306.06624*.
- Świechowski et al. (2023)

  Maciej Świechowski, Konrad Godlewski, Bartosz Sawicki, and Jacek Mańdziuk.
  Monte carlo tree search: A review of recent modifications and applications.
  *Artificial Intelligence Review*, 56(3):2497–2562, 2023.
- Touvron et al. (2023)

  Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al.
  Llama 2: Open foundation and fine-tuned chat models.
  *arXiv preprint arXiv:2307.09288*, 2023.
- Uesato et al. (2022)

  Jonathan Uesato, Nate Kushman, Ramana Kumar, Francis Song, Noah Siegel, Lisa Wang, Antonia Creswell, Geoffrey Irving, and Irina Higgins.
  Solving math word problems with process-and outcome-based feedback.
  *arXiv preprint arXiv:2211.14275*, 2022.
- Wang et al. (2023a)

  Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, and Anima Anandkumar.
  Voyager: An open-ended embodied agent with large language models.
  *arXiv preprint arXiv:2305.16291*, 2023a.
- Wang et al. (2023b)

  Peiyi Wang, Lei Li, Liang Chen, Feifan Song, Binghuai Lin, Yunbo Cao, Tianyu Liu, and Zhifang Sui.
  Making large language models better reasoners with alignment.
  *arXiv preprint arXiv:2309.02144*, 2023b.
- Wang et al. (2023c)

  Peiyi Wang, Lei Li, Liang Chen, Dawei Zhu, Binghuai Lin, Yunbo Cao, Qi Liu, Tianyu Liu, and Zhifang Sui.
  Large language models are not fair evaluators.
  *arXiv preprint arXiv:2305.17926*, 2023c.
- Wang et al. (2023d)

  Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V. Le, Ed H. Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou.
  Self-consistency improves chain of thought reasoning in language models.
  In *The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023*. OpenReview.net, 2023d.
  URL <https://openreview.net/pdf?id=1PL1NIMMrw>.
- Wei et al. (2022)

  Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, and Denny Zhou.
  Chain-of-thought prompting elicits reasoning in large language models.
  In *NeurIPS*, 2022.
  URL <http://papers.nips.cc/paper_files/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.html>.
- Wu et al. (2023)

  Zeqiu Wu, Yushi Hu, Weijia Shi, Nouha Dziri, Alane Suhr, Prithviraj Ammanabrolu, Noah A Smith, Mari Ostendorf, and Hannaneh Hajishirzi.
  Fine-grained human feedback gives better rewards for language model training.
  *arXiv preprint arXiv:2306.01693*, 2023.
- Xia et al. (2022)

  Heming Xia, Tao Ge, Furu Wei, and Zhifang Sui.
  Lossless speedup of autoregressive translation with generalized aggressive decoding.
  *arXiv preprint arXiv:2203.16487*, 2022.
- Yu et al. (2023a)

  Fei Yu, Anningzhe Gao, and Benyou Wang.
  Outcome-supervised verifiers for planning in mathematical reasoning.
  *arXiv preprint arXiv:2311.09724*, 2023a.
- Yu et al. (2023b)

  Longhui Yu, Weisen Jiang, Han Shi, Jincheng Yu, Zhengying Liu, Yu Zhang, James T Kwok, Zhenguo Li, Adrian Weller, and Weiyang Liu.
  Metamath: Bootstrap your own mathematical questions for large language models.
  *arXiv preprint arXiv:2309.12284*, 2023b.
- Yuan et al. (2023)

  Zheng Yuan, Hongyi Yuan, Chengpeng Li, Guanting Dong, Chuanqi Tan, and Chang Zhou.
  Scaling relationship on learning mathematical reasoning with large language models.
  *arXiv preprint arXiv:2308.01825*, 2023.
- Yue et al. (2023)

  Xiang Yue, Xingwei Qu, Ge Zhang, Yao Fu, Wenhao Huang, Huan Sun, Yu Su, and Wenhu Chen.
  Mammoth: Building math generalist models through hybrid instruction tuning.
  *arXiv preprint arXiv:2309.05653*, 2023.
- Zhang et al. (2023)

  Yifan Zhang, Jingqin Yang, Yang Yuan, and Andrew Chi-Chih Yao.
  Cumulative reasoning with large language models.
  *arXiv preprint arXiv:2308.04371*, 2023.
- Zheng et al. (2023)

  Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al.
  Judging llm-as-a-judge with mt-bench and chatbot arena.
  *arXiv preprint arXiv:2306.05685*, 2023.
- Zhu et al. (2023)

  Xinyu Zhu, Junjie Wang, Lin Zhang, Yuxiang Zhang, Yongfeng Huang, Ruyi Gan, Jiaxing Zhang, and Yujiu Yang.
  Solving math word problems via cooperative reasoning induced language models.
  In Anna Rogers, Jordan Boyd-Graber, and Naoaki Okazaki (eds.), *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pp. 4471–4485, Toronto, Canada, July 2023. Association for Computational Linguistics.
  doi: 10.18653/v1/2023.acl-long.245.
  URL <https://aclanthology.org/2023.acl-long.245>.
