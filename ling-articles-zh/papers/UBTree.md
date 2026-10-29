---
title: "UBTree：基于 Unigram 与 Bigram 模型的投机解码并行树起草"
title_en: "UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"
arxiv: 2609.39972
date: 2026-10-09
source: https://arxiv.org/abs/2609.39972
project: https://github.com/inclusionAI/ubtree
crawled: 2026-10-29
translated: 2026-10-29
---
# UBTree：基于 Unigram 与 Bigram 模型的投机解码并行树起草

> 原文：[UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding](https://arxiv.org/abs/2609.39972) · 蚂蚁集团 InclusionAI arXiv

## 摘要

投机解码（speculative decoding）通过在目标模型的一次前向中验证多个草稿 token 来加速语言模型推理。近期的并行起草器已在前沿生产模型上取得突破性性能，但由于草稿多样性不足，其效果会随目标分布熵的升高而退化。为了在不牺牲并行性的前提下突破这一瓶颈，我们提出 UBTree——一种将 unigram（一元）提议器与 bigram（二元）选择器相耦合以构建起草树的并行起草器。unigram 提议器以标准交叉熵目标训练，为每个位置独立生成候选 token；轻量级 bigram 选择器则预测相邻候选 token 对之间的转移分数。与提议器不同，选择器在高温数据上以重归一化 KL 目标训练。这种树原生（tree-native）训练将监督信号扩展到贪心路径之外，鼓励合理的备选分支，从而提高树验证中接受额外 token 的机会。在 Qwen3-4B 与 Qwen3-8B 的七个标准化基准上，UBTree 相对自回归解码取得 $5.84$–$6.94\times$ 的平均加速比，并在全部 28 项对比中胜过 DARTree。生产规模评测进一步表明 UBTree 相对 DSpark 等前沿基线具备优势。

††脚注：*共同一作。†通讯作者。本工作完成于 Chumeng 与 Linxuan 在 Inclusion AI 实习期间。

图 1：(a) Qwen3-8B 上的加速比：在 Qwen3-8B instruct 上、$T_{\mathrm{infer}}=1$ 时，七个基准上相对自回归解码的加速比。(b) Qwen3.8-27B 上的加速比：在 SGLang 中、Qwen3.8-27B 上 $T_{\mathrm{infer}}=1$ 时的服务加速比。(c) 长上下文接受情况：Ling3-Flash-124B 在 LongBench-v2 与 SWE-bench 上、不同上下文长度下的接受长度 $\tau$。在大多数基准与模型规模上，UBTree 均优于对比方法。

## 1 引言

投机解码（[Leviathan et al., 2023](#bib.bib8); [Chen et al., 2023](#bib.bib9)）提供了一种无损加速大语言模型（LLM）的方法：由轻量级起草器提出多个未来 token，目标模型在一次前向中一并验证，同时保持其输出分布不变。投机解码的收益不仅取决于目标模型对草稿的接受长度，还取决于计算开销。如果生成更长的被接受草稿本身会带来显著延迟，那么更长的被接受草稿未必带来更大的加速比。

投机解码近期的进展主要由并行起草的突破所驱动（[Liu et al., 2026](#bib.bib15); [Chen et al., 2026](#bib.bib5)）。自回归式起草器（[Li et al., 2024b](#bib.bib12); [Li et al., 2026d](#bib.bib6)）依序根据前面的选择生成每个草稿 token，而并行起草器则通过提议器骨干的单次前向，一次性预测起草块中的所有未来位置。并行性降低了使用更大提议器骨干带来的串行开销，从而提升了接受长度。然而，并行起草器缺乏草稿多样性。因此，当高熵的目标分布天然会产生不同路径时，其性能随之退化。此外，token 级依赖的缺失可能因混合这些不同路径而加剧退化。现有方法试图通过恢复 token 级依赖来弥补这一缺陷：或用轻量自回归修正头提高单路径草稿的精度（[Huang et al., 2026](#bib.bib7); [Cheng et al., 2026](#bib.bib16)），或采用骨干内设计（[Inco AI, 2026](#bib.bib17)）。然而，这些策略并未从根本上解决多样性瓶颈，因为所覆盖的仍然只有单一草稿路径。这尤其限制了并行起草器的进一步提升，以及其在高熵目标分布场景下的应用（[Devic et al., 2025](#bib.bib47); [Yang et al., 2026](#bib.bib28)）。草稿多样性因此成为当前并行投机解码的核心瓶颈。

解决该瓶颈的一个自然方案是树起草（tree drafting）（[Miao et al., 2024](#bib.bib11); [Cai et al., 2024](#bib.bib10); [Li et al., 2024a](#bib.bib13)）：将多条草稿路径保留为树分支，提高目标验证命中其中一条的概率。通过提供多样且合理的候选草稿，树起草在高熵场景下更为稳健。将树起草与并行起草器结合——即从预训练的块并行起草器构建预算树——已取得可观的加速（[Ringel and Romano, 2026](#bib.bib19); [Li et al., 2026c](#bib.bib18)）。尽管如此，这些方法存在两点局限。其一，token 级依赖与完全并行之间的张力，制约了草稿质量与起草延迟之间的权衡。现有基于树的方法使用自回归头刻画 token 级依赖，因而无法完全并行化；反之，省略 token 级依赖又会限制接受长度，进而限制端到端加速比。其二，基于树的并行方法存在训练–推理失配：它们把为单路径起草训练的并行起草器直接用于多路径树验证。这类起草器被优化为产出供单路径验证的最优草稿，却并不擅长为树验证提出多条合理路径。结果是，虽然草稿树中排名较低的备选项可以填充额外分支，它们既未被充分优化到与目标模型的备选项对齐，也不值得为其分配验证预算。

我们用 UBTree 来解决这些局限。UBTree 是一种基于树的起草器，以并行 bigram 选择器建模 token 级依赖，并以树原生训练弥合训练–推理差距。UBTree 中包含两项设计：

- **架构**。UBTree 将起草拆分为三个互补阶段，并保持全部神经计算并行。首先，我们使用 DFlash（[Chen et al., 2026](#bib.bib5)）作为 unigram 提议器，为起草块中的每个位置独立生成候选 token。其次，一个重新设计的 bigram 选择器在提议器隐藏状态的条件下为相邻候选 token 对打分：它通过两个独立的 MLP 从冻结的目标嵌入导出前驱与后继表示，并学习随深度变化的权重来组合提议器 logits 与选择器分数。最后，我们用所得的转移分数构建验证树。通过将 token 级依赖简化为 bigram 相关性，我们解决了树起草中 token 级依赖并行化的难题。
- **训练**。与其它在推理温度下基于目标模型重生成的 rollout 训练的起草器不同，我们在高温重生成的目标轨迹上使用重归一化 KL 训练目标，以多样化正训练标签。这种树原生训练策略把更多监督信号分配给目标分布中合理的备选路径，并使它们在树构建中更好地与低质量备选路径区分开，从而缓解树起草中的训练–推理失配。

我们在学术与生产规模基准上对 UBTree 进行了广泛评测。UBTree 在学术规模与生产基准上均优于所有现有方法。在 Qwen3-4B 与 Qwen3-8B 上，它以更高的接受长度取得相对自回归解码平均 $5.84$–$6.94\times$ 的解码加速比。在 Ling3-Flash-124B 等生产 LLM 的加速上，它亦可与 DSpark（[Cheng et al., 2026](#bib.bib16)）等前沿基线一较高下。此外，与基线相比，UBTree 在长上下文任务上表现出卓越的持久性。总而言之，UBTree 为在学术环境与生产环境中加速 LLM 提供了一个前沿解决方案。

## 2 背景

**投机解码**。给定已验证前缀 $x_{\leq t}$，一个轻量级草稿模型提出 $\gamma$ 个未来 token，由目标模型在一次前向中验证（[Leviathan et al., 2023](#bib.bib8); [Chen et al., 2023](#bib.bib9)）。每一轮从提议块的开头开始接受连续的草稿 token，直到首次被拒绝为止。记 $\tau\in[1,\gamma+1]$ 为每轮平均接受的 token 数（即接受长度，acceptance length），其中包含由最后一次验证预填充的一个 token $x_{0}$。以 $T_{\mathrm{draft}}$ 表示提议构建耗时、$T_{\mathrm{verify}}$ 表示验证与提交耗时，则平均每 token 延迟与加速比为（[Chen et al., 2026](#bib.bib5); [Huang et al., 2026](#bib.bib7)）

$$
L_{\mathrm{spec}}=\frac{T_{\mathrm{draft}}+T_{\mathrm{verify}}}{\tau},\qquad\eta=\frac{L_{\mathrm{target}}}{L_{\mathrm{spec}}},
\tag{1}
$$

其中 $L_{\mathrm{target}}$ 为仅用目标模型的自回归解码的每 token 延迟。

**DFlash 与 DFlash 2**。DFlash（[Chen et al., 2026](#bib.bib5)）并行提出一个 $\gamma$-token 块，通过一次目标预填充前向的 key-value 上下文以目标隐藏特征为条件。我们将预填充的 token $x_{0}$ 称为锚点 token（anchor token）。对每个未来起草位置 $i=1,...,\gamma$，提议器一次前向产生最终隐藏状态 $h_{i}$，随后经冻结的目标 LM head 映射为提议器 logit $u_{i}$。DFlash 的草稿 token 是在几乎不涉及 token 级依赖的掩码下并行预测的。DFlash 2（[Inco AI, 2026](#bib.bib17)）通过在 DFlash 骨干中加入卷积以及一个低秩 bigram 选择器解决了这一问题。对位置 $i$ 的前驱 $a$ 与后继 $b$，选择器分数 $\delta_{i}(a,b)$ 加到提议器 logit $u_{i}(b)$ 上，得到组合分数：

$$
\delta_{i}(a,b)=\bigl(P(h_{i})\odot\phi(a)\bigr)^{\top}\psi(b),\qquad u_{i}^{\prime}(a,b)=u_{i}(b)+\delta_{i}(a,b),
\tag{2}
$$

其中 $\odot$ 表示 Hadamard 积。这里线性投影 $P$ 将 $h_{i}$ 映射到低维空间，$\phi$ 与 $\psi$ 分别是前驱与后继 token 的低秩嵌入。该选择器对逐位置 top-$K$ 候选集合中的所有相邻对并行打分；随后按组合分数沿单条链选取 token。

**树起草**。DFlash 与 DFlash 2 是单路径起草方法，它们提出一条 $\gamma$-token 草稿路径去匹配 $\gamma$-token 目标路径，供目标模型验证。相比之下，树起草构建一棵存储多条候选草稿路径的草稿树。候选 token 作为节点，不同路径在具有公共前缀的延续之间共享节点。然后我们使用树注意力（tree attention）在一次目标模型前向中验证整棵草稿树，并选取树中被目标模型接受的最长 token 延续所对应的路径（[Miao et al., 2024](#bib.bib11); [Cai et al., 2024](#bib.bib10)）。该验证过程保持了投机解码的无损性质，被接受的路径不必是提议器排名最高的路径。

DDTree（[Ringel and Romano, 2026](#bib.bib19)）与 DARTree（[Li et al., 2026c](#bib.bib18)）从块并行提议构建预算树。DDTree 使用最佳优先搜索，按逐位置 token log 概率的累积值对路径排序。DARTree 用轻量自回归头修正 token log 概率，并以深度衰减和每层 $W$ 个节点的预算对累积 log 概率排序。这些保留的节点累积成最大深度为 $\gamma$ 的候选超树，再从中选出 $B$ 个得分最高的非根节点用于验证。下一深度的修正仍依赖于前一深度选出的 token，带来额外开销。

![Refer to caption](2609.39972v1/ubtree_diagram.png)

图 2：UBTree 总览。左：UBTree 架构。unigram 提议器在每个起草位置并行生成 top-$K$ 候选；bigram 选择器并行地为相邻候选转移打分，树构建利用这些预计算分数搭建验证树。右：树原生训练。我们的训练将高温目标轨迹与重归一化 KL 监督相结合，以鼓励合理的备选分支。

## 3 方法

UBTree 的两项关键设计是：1) 在树起草中并行化 token 级依赖建模；2) 让树起草器的训练面向最优的树起草。[第 3.1 节](#S3.SS1)首先说明我们如何在树起草中以完全并行的神经计算纳入 token 依赖：用两次并行神经前向在各块位置提出候选 token（[第 3.1.1 节](#S3.SS1.SSS1)），并在这些候选之间选取转移路径（[第 3.1.2 节](#S3.SS1.SSS2)）；随后由选择器选出的路径构建验证树（[第 3.1.3 节](#S3.SS1.SSS3)）。[第 3.2 节](#S3.SS2)给出我们的树原生训练：在高温下重生成训练用目标 rollout，并以重归一化 KL 目标训练起草器。我们在[图 2](#S2.F2)中总结了 UBTree 的这两项设计。

### 3.1 UBTree 架构

#### 3.1.1 Unigram 提议器

unigram 提议器的设计目标是在不考虑跨 token 依赖的前提下，为每个位置提出候选 token。令 $c$ 为来自已验证前缀的 key-value 上下文，$x_{0}$ 为预填充的锚点 token。unigram 提议器可形式化为

$$
q_{i}(x_{i}\mid x_{0},c)=\operatorname{softmax}(u_{i}(x_{0},c)),\quad i=1,2,...,\gamma,
\tag{3}
$$

其中 $i$ 表示块内位置。由于各位置的提议互不依赖，其神经前向可以轻易并行。实践中，我们部署一个预训练的 DFlash 骨干（[Chen et al., 2026](#bib.bib5)）作为 unigram 提议器，其输出 logits 为 $u_{i}(x_{0},c)$，概率为 $q_{i}(x_{i}\mid x_{0},c)$，预测的隐藏状态记为 $h_{i}$。我们不使用 DFlash2 骨干（[Inco AI, 2026](#bib.bib17)），因为它相对 DFlash 骨干的改动在于强化 token 级连接，而这并非我们 unigram 提议的任务。

**候选集合**。我们在每个位置取 $q_{i}$ 中概率 top-$K$ 的 token 作为该位置的候选 token $\mathcal{C}_{i}$，其中 $\mathcal{C}_{0}=\{x_{t}\}$。笛卡尔积 $\mathcal{C}_{1}\times\cdots\times\mathcal{C}_{\gamma}$ 构成 $K^{\gamma}$ 条候选路径。枚举这些路径并不可行，因此 UBTree 对相邻转移打分，并在下一节中由 bigram 选择器搜索一个有界子集。

#### 3.1.2 Bigram 选择器

受 DFlash 2（[Inco AI, 2026](#bib.bib17)）启发，我们引入一个轻量级 bigram 选择器，在后继位置提议器隐藏状态 $h_{i}$ 的条件下，为候选中相邻的前驱–后继 token 对打分。这一可训练的选择器以并行方式建模 token 级依赖。为进一步改进选择器，我们用深度码本与深度校准重新设计了其架构。

**深度码本**。对位置 $i$ 的前驱 token $a$ 与后继候选 $b$，DFlash 2 用两个嵌入层学习两个词表级码本 $\phi$ 与 $\psi$（见[式 (2)](#S2.E2)）。UBTree 则从冻结的目标 token 嵌入 $e_{v}\in\mathbb{R}^{d_{e}}$ 与两个无偏置 MLP 导出码本：

$$
\phi(v)=W_{\phi,2}\,\operatorname{SiLU}(W_{\phi,1}e_{v}),\qquad\psi(v)=W_{\psi,2}\,\operatorname{SiLU}(W_{\psi,1}e_{v}).
\tag{4}
$$

推理时，我们一次性预计算两个 MLP 并将其存为词表级查找表。在保持推理效率的同时，我们的深度码本引入了非线性并利用了目标嵌入中的特征，因而改进了选择器性能。

**深度校准**。DFlash 2 以固定的单位权重组合提议器 logits 与选择器分数。然而，二者的可靠性会随草稿深度变化。UBTree 因此学习两个正的、随深度变化的比例因子：

$$
s_{i}(a,b)=\alpha_{i}u_{i}(b)+\lambda_{i}\delta_{i}(a,b),\qquad\alpha_{i}=\exp(\rho_{i}),\quad\lambda_{i}=\exp(\kappa_{i}).
\tag{5}
$$

比值 $\lambda_{i}/\alpha_{i}$ 控制选择器分数相对提议器 logits 的权重，而二者的共同幅度控制归一化后继分布的集中程度。这些比例只依赖深度，保持了边打分的并行性。

**并行计算**。一旦提议器给出候选集合与隐藏状态，我们就对所有 $K+(\gamma-1)K^{2}$ 个前驱–后继 token 对并行计算转移分数。在深度 $i$，令 $\bm{\Phi}_{i-1}$ 的各行是前驱候选 $a\in\mathcal{C}_{i-1}$ 对应的 $\phi(a)^{\top}$，$\bm{\Psi}_{i}$ 的各行是后继候选 $b\in\mathcal{C}_{i}$ 对应的 $\psi(b)^{\top}$。结合后继位置处提议器的隐藏状态 $h_{i}$，我们得到

$$
\bm{\Delta}_{i}=\bm{\Phi}_{i-1}\operatorname{diag}\!\bigl(P(h_{i})\bigr)\bm{\Psi}_{i}^{\top}\in\mathbb{R}^{|\mathcal{C}_{i-1}|\times K}.
\tag{6}
$$

这里 $\operatorname{diag}(\cdot)$ 把输入向量放到对角线上。行对应 $a$、列对应 $b$ 的元素即选择器分数 $\delta_{i}(a,b)$。在按[式 (5)](#S3.E5)把 $\delta_{i}(a,b)$ 与提议器 logits $u_{i}(b)$ 组合之后，树构建可以逐深度串行推进，而无需任何神经计算。

#### 3.1.3 树构建与验证

有了 $C_{i-1}\times C_{i}$ 中每次转移 $s_{i}(a,b)$ 的唯一分数，我们无需神经计算即可为由这些转移构成的全部 $K^{\gamma}$ 条候选路径打分。具体而言，可以把 $s_{i}(a,b)$ 归一化为后继候选上的 log 概率，再按累积 log 概率对路径排序。不过，为了节省计算开销，我们沿用 DARTree 的逐深度递进式树构建与全局剪枝流程（[Li et al., 2026c](#bib.bib18)），而非遍历所有可能路径。树构建完成后，目标模型通过树注意力在一次前向中验证整棵树，并保留被接受的最长延续，实现无损加速。[附录 A](#A1)给出了归一化、路径打分、搜索与验证流程的细节。

### 3.2 树原生训练

树起草向目标验证推荐多条路径，而不只提出贪心路径。因此，我们需要多样化正训练信号，帮助选择器更好地识别贪心路径之外的合理备选路径。为此，我们用高于推理温度 $T_{\mathrm{infer}}$ 的训练温度 $T_{\mathrm{train}}$ 重新生成训练数据，并以重归一化 KL 目标监督训练。

**针对不同 $T_{\mathrm{infer}}$，以 $T_{\mathrm{train}}\geq T_{\mathrm{infer}}$ 训练**。训练温度 $T_{\mathrm{train}}$ 同时控制提议器与选择器所见到的延续分布，以及用于 KL 监督的目标分布。温度匹配的训练会设 $T_{\mathrm{train}}=T_{\mathrm{infer}}$。如上所述，选择器需要提升树中多条路径的合理性，而非只关注顶部路径。因此我们可以取 $T_{\mathrm{train}}\geq T_{\mathrm{infer}}$，使那些高概率备选路径更可区分。$T_{\mathrm{train}}$ 由此成为一个可经验调优的独立超参数。最优的 $T_{\mathrm{train}}$ 会放大合理选项与其他选项之间的概率差距。有趣的是，$T_{\mathrm{train}}$ 在某种程度上与 $T_{\mathrm{infer}}$ 解耦：在某个 $T_{\mathrm{train}}$ 上训练的一个 UBTree 起草器可用于不同的 $T_{\mathrm{infer}}$，这简化了起草器的适配。因此，实验中我们对 $T_{\mathrm{infer}}=0$ 与 $T_{\mathrm{infer}}=1$ 都使用在 $T_{\mathrm{train}}=1$ 下训练的同一起草器。

**重归一化 KL 损失**。为训练选择器更好地辨别顶部选项之外的备选项，我们在提议器的 top-$K$ 候选 token 上，使用目标与选择器的重归一化概率（[Zhu et al., 2026](#bib.bib20)）之间的前向 KL 散度，取代经典的交叉熵（CE）损失。对每个有效未来位置，令 $z_{i}(v)$ 为目标 logit，$s_{i}(y_{i-1}^{*},v)$ 为给定前驱 token $y_{i-1}^{*}$ 的选择器 logit。当 $T_{\mathrm{train}}>0$ 时，我们在 top-$K$ token 支撑集 $\mathcal{C}_{i}$ 上定义训练温度 $T_{\mathrm{train}}$ 下的重归一化目标概率 $\widetilde{p}_{i}(v)$ 与选择器概率 $\widetilde{q}_{i}(v)$：

$$
\widetilde{p}_{i}(v)=\frac{\exp(z_{i}(v)/T_{\mathrm{train}})}{\sum_{b\in\mathcal{C}_{i}}\exp(z_{i}(b)/T_{\mathrm{train}})},\qquad\widetilde{q}_{i}(v)=\frac{\exp(s_{i}(y_{i-1}^{*},v))}{\sum_{b\in\mathcal{C}_{i}}\exp(s_{i}(y_{i-1}^{*},b))}.
\tag{7}
$$

当 $T_{\mathrm{train}}=0$ 时，目标分布按极限 $T_{\mathrm{train}}\to 0^{+}$ 理解。$\widetilde{p}_{i}(v)$ 与 $\widetilde{q}_{i}(v)$ 之间的前向 KL 散度构成我们训练目标的主项。另有一个辅助交叉熵项（也用于第一阶段的提议器训练）仅作用于提议器 $q_{i}$，以维持候选分布。以权重 $\beta$ 平衡两项，联合目标为

$$
\mathcal{L}=\mathrm{KL}(\widetilde{p}_{i}|\widetilde{q}_{i})-\beta\log q_{i}(y_{i}^{*}\mid x_{\leq t}),\qquad\beta=0.1.
\tag{8}
$$

## 4 实验

我们在基准上评测 UBTree，并报告相对自回归基线的解码加速比 $\eta$ 与平均接受长度 $\tau$。「平均」指所有列出基准上的平均结果。

表 1：instruct 模型与推理模型上的加速比与平均接受长度（$\tau$）。所有 $\tau$ 值包含目标模型产出的奖励 token。M-500、HE、LCB、MT-B 分别表示 MATH-500、HumanEval、LiveCodeBench、MT-Bench。带 † 的数值取自原论文。

**Instruct 模型**

| 模型 | 方法 | GSM8K 加速比 | $\tau$ | M-500 加速比 | $\tau$ | AIME 加速比 | $\tau$ | HE 加速比 | $\tau$ | MBPP 加速比 | $\tau$ | LCB 加速比 | $\tau$ | MT-B 加速比 | $\tau$ | 平均加速比 | $\tau$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Qwen3-4B $T_{\mathrm{infer}}=0$** | **单路径** | | | | | | | | | | | | | | | | |
| | DFlash (16) | 5.95 | 8.57 | 5.76 | 8.34 | 4.45 | 6.34 | 4.28 | 6.08 | 4.03 | 5.82 | 3.83 | 5.39 | 2.69 | 4.60 | 4.43 | 6.45 |
| | Domino† (17) | 8.02 | 10.12 | 7.14 | 9.01 | 5.97 | 7.49 | 5.66 | 7.02 | 5.59 | 7.11 | 5.33 | 6.86 | 3.28 | 5.12 | 5.86 | 7.53 |
| | **基于树** | | | | | | | | | | | | | | | | |
| | EAGLE-3 (16) | 4.04 | 7.20 | 3.97 | 6.96 | 3.45 | 6.05 | 3.46 | 6.07 | 3.42 | 6.05 | 3.19 | 5.53 | 2.40 | 4.67 | 3.42 | 6.08 |
| | EAGLE-3 (64) | 4.42 | 7.97 | 4.45 | 7.85 | 4.02 | 7.11 | 4.00 | 7.07 | 3.95 | 7.11 | 3.75 | 6.58 | 2.80 | 5.46 | 3.91 | 7.02 |
| | DDTree (64) | 6.69 | 10.22 | 6.62 | 10.10 | 5.51 | 8.49 | 5.18 | 7.89 | 5.10 | 7.80 | 4.78 | 7.23 | 3.51 | 6.14 | 5.34 | 8.27 |
| | DARTree (64) | 7.89 | 12.50 | 7.63 | 11.90 | 6.55 | 10.37 | 6.09 | 9.78 | 6.33 | 10.07 | 5.75 | 9.04 | 3.93 | 7.23 | 6.31 | 10.13 |
| | UBTree (64) | 8.54 | 12.58 | 8.18 | 12.15 | 6.92 | 10.13 | 7.07 | 10.22 | 6.66 | 9.98 | 6.37 | 9.24 | 4.39 | 7.32 | 6.88 | 10.23 |
| **Qwen3-4B $T_{\mathrm{infer}}=1$** | **单路径** | | | | | | | | | | | | | | | | |
| | DFlash (16) | 5.28 | 7.67 | 4.56 | 6.89 | 3.10 | 4.64 | 4.09 | 5.86 | 3.84 | 5.52 | 3.25 | 4.62 | 2.52 | 4.26 | 3.81 | 5.64 |
| | Domino† (17) | 6.79 | 8.61 | 5.67 | 7.35 | 3.75 | 4.83 | 5.02 | 6.30 | 4.96 | 6.36 | 5.04 | 6.45 | 3.02 | 4.56 | 4.89 | 6.35 |
| | **基于树** | | | | | | | | | | | | | | | | |
| | EAGLE-3 (16) | 3.66 | 6.61 | 3.51 | 6.36 | 2.72 | 4.88 | 3.34 | 5.93 | 3.21 | 5.80 | 2.80 | 4.94 | 2.21 | 4.34 | 3.06 | 5.55 |
| | EAGLE-3 (64) | 4.13 | 7.66 | 3.96 | 7.29 | 3.20 | 6.00 | 3.75 | 6.84 | 3.71 | 6.92 | 3.27 | 5.96 | 2.54 | 5.12 | 3.51 | 6.54 |
| | DDTree (64) | 6.19 | 9.49 | 5.62 | 8.76 | 4.14 | 6.31 | 5.17 | 7.81 | 4.90 | 7.50 | 4.19 | 6.37 | 3.37 | 5.66 | 4.80 | 7.41 |
| | DARTree (64) | 6.94 | 11.01 | 6.05 | 9.73 | 4.10 | 6.99 | 5.84 | 9.10 | 5.76 | 9.28 | 4.71 | 7.33 | 3.64 | 6.53 | 5.29 | 8.57 |
| | UBTree (64) | 7.95 | 11.79 | 7.13 | 10.54 | 5.10 | 7.63 | 6.42 | 9.43 | 6.15 | 9.30 | 5.27 | 7.72 | 4.02 | 6.68 | 6.00 | 9.01 |
| **Qwen3-8B $T_{\mathrm{infer}}=0$** | **单路径** | | | | | | | | | | | | | | | | |
| | DFlash (16) | 5.98 | 8.59 | 5.84 | 8.51 | 4.75 | 6.73 | 4.46 | 6.31 | 4.07 | 5.87 | 3.91 | 5.48 | 2.64 | 4.54 | 4.52 | 6.58 |
| | Domino† (17) | 7.92 | 10.03 | 7.38 | 9.43 | 5.85 | 7.41 | 5.89 | 7.39 | 5.53 | 7.04 | 5.27 | 7.04 | 3.29 | 5.18 | 5.88 | 7.65 |
| | **基于树** | | | | | | | | | | | | | | | | |
| | EAGLE-3 (16) | 4.23 | 7.43 | 4.20 | 7.30 | 3.71 | 6.46 | 3.68 | 6.42 | 3.62 | 6.39 | 3.54 | 6.07 | 2.53 | 4.88 | 3.64 | 6.42 |
| | EAGLE-3 (64) | 4.57 | 8.20 | 4.66 | 8.11 | 4.34 | 7.51 | 4.23 | 7.39 | 4.13 | 7.39 | 4.11 | 7.10 | 2.99 | 5.77 | 4.15 | 7.35 |
| | DDTree (64) | 6.65 | 10.19 | 6.60 | 10.12 | 5.64 | 8.63 | 5.43 | 8.17 | 5.07 | 7.68 | 4.92 | 7.30 | 3.49 | 6.09 | 5.40 | 8.31 |
| | DARTree (64) | 8.26 | 12.49 | 7.61 | 12.13 | 6.71 | 10.37 | 6.41 | 10.09 | 6.32 | 10.02 | 5.88 | 9.19 | 4.01 | 7.33 | 6.46 | 10.23 |
| | UBTree (64) | 8.65 | 12.58 | 8.46 | 12.30 | 7.05 | 10.17 | 7.12 | 10.12 | 6.64 | 9.79 | 6.43 | 9.24 | 4.25 | 7.25 | 6.94 | 10.21 |
| **Qwen3-8B $T_{\mathrm{infer}}=1$** | **单路径** | | | | | | | | | | | | | | | | |
| | DFlash (16) | 5.05 | 7.37 | 4.57 | 6.77 | 2.99 | 4.47 | 3.74 | 5.26 | 3.64 | 5.20 | 3.14 | 4.41 | 2.34 | 3.96 | 3.64 | 5.35 |
| | Domino† (17) | 6.47 | 8.34 | 5.40 | 7.20 | 3.78 | 4.92 | 4.75 | 5.98 | 4.73 | 6.02 | 5.06 | 6.72 | 2.94 | 4.61 | 4.73 | 6.26 |
| | **基于树** | | | | | | | | | | | | | | | | |
| | EAGLE-3 (16) | 3.93 | 7.07 | 3.74 | 6.68 | 3.01 | 5.30 | 3.35 | 5.89 | 3.35 | 6.01 | 3.01 | 5.25 | 2.36 | 4.55 | 3.25 | 5.82 |
| | EAGLE-3 (64) | 4.39 | 8.05 | 4.23 | 7.65 | 3.51 | 6.34 | 3.88 | 7.00 | 3.88 | 7.14 | 3.53 | 6.32 | 2.73 | 5.45 | 3.73 | 6.85 |
| | DDTree (64) | 6.10 | 9.23 | 5.61 | 8.68 | 4.04 | 6.31 | 4.91 | 7.37 | 4.63 | 7.02 | 4.14 | 6.22 | 3.23 | 5.48 | 4.67 | 7.19 |
| | DARTree (64) | 7.04 | 11.01 | 5.86 | 9.59 | 4.48 | 7.21 | 5.26 | 8.36 | 5.53 | 8.91 | 4.45 | 7.06 | 3.59 | 6.48 | 5.17 | 8.37 |
| | UBTree (64) | 7.97 | 11.55 | 6.99 | 10.44 | 4.99 | 7.43 | 6.17 | 8.85 | 5.92 | 8.80 | 5.10 | 7.47 | 3.77 | 6.36 | 5.84 | 8.70 |

**推理模型**

| 模型 | 方法 | GSM8K 加速比 | $\tau$ | M-500 加速比 | $\tau$ | AIME 加速比 | $\tau$ | HE 加速比 | $\tau$ | MBPP 加速比 | $\tau$ | LCB 加速比 | $\tau$ | MT-B 加速比 | $\tau$ | 平均加速比 | $\tau$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Qwen3-4B $T_{\mathrm{infer}}=0$** | **单路径** | | | | | | | | | | | | | | | | |
| | DFlash (16) | 5.18 | 7.28 | 4.53 | 6.45 | 3.67 | 5.26 | 3.91 | 5.46 | 3.72 | 5.17 | 3.37 | 4.68 | 2.99 | 4.64 | 3.91 | 5.56 |
| | **基于树** | | | | | | | | | | | | | | | | |
| | EAGLE-3 (16) | 3.49 | 6.01 | 3.04 | 5.23 | 2.65 | 4.62 | 2.82 | 4.83 | 2.80 | 4.78 | 2.43 | 4.16 | 2.25 | 4.11 | 2.78 | 4.82 |
| | EAGLE-3 (64) | 4.19 | 7.24 | 3.75 | 6.48 | 3.29 | 5.77 | 3.52 | 6.05 | 3.51 | 6.04 | 3.04 | 5.28 | 2.74 | 5.07 | 3.44 | 5.99 |
| | DDTree (64) | 6.09 | 9.19 | 5.54 | 8.42 | 4.77 | 7.20 | 4.85 | 7.29 | 4.68 | 7.01 | 4.31 | 6.45 | 3.82 | 6.15 | 4.87 | 7.39 |
| | UBTree (64) | 7.64 | 10.95 | 6.99 | 10.01 | 5.73 | 8.53 | 6.21 | 8.85 | 5.98 | 8.54 | 5.45 | 7.75 | 4.71 | 7.22 | 6.10 | 8.84 |
| **Qwen3-4B $T_{\mathrm{infer}}=1$** | **单路径** | | | | | | | | | | | | | | | | |
| | DFlash (16) | 4.80 | 6.77 | 4.36 | 6.18 | 3.57 | 5.15 | 3.76 | 5.23 | 3.55 | 4.93 | 3.21 | 4.47 | 2.89 | 4.40 | 3.73 | 5.30 |
| | **基于树** | | | | | | | | | | | | | | | | |
| | EAGLE-3 (16) | 3.01 | 5.28 | 2.78 | 4.86 | 2.41 | 4.22 | 2.54 | 4.42 | 2.47 | 4.28 | 2.24 | 3.92 | 2.00 | 3.69 | 2.49 | 4.38 |
| | EAGLE-3 (64) | 3.64 | 6.57 | 3.34 | 6.00 | 2.98 | 5.37 | 3.17 | 5.66 | 3.06 | 5.48 | 2.77 | 4.99 | 2.35 | 4.49 | 3.04 | 5.51 |
| | DDTree (64) | 4.87 | 7.35 | 4.69 | 7.11 | 4.01 | 6.10 | 4.17 | 6.22 | 3.97 | 5.93 | 3.57 | 5.37 | 3.28 | 5.11 | 4.08 | 6.17 |
| | UBTree (64) | 6.56 | 9.50 | 6.12 | 8.78 | 5.12 | 7.47 | 5.44 | 7.74 | 5.18 | 7.41 | 4.57 | 6.61 | 4.10 | 6.17 | 5.30 | 7.67 |

### 4.1 学术规模实验

**基准**。我们在 Qwen3-4B 与 Qwen3-8B（[Yang et al., 2025a](#bib.bib49)）上（关闭思考模式，即 instruct 模型），以及 Qwen3-4B 上（开启思考模式，即推理模型），于 $T_{\mathrm{infer}}=\{0,1\}$ 下评测 UBTree。基准覆盖数学（GSM8K（[Cobbe et al., 2021](#bib.bib21)）、MATH-500（[Lightman et al., 2024](#bib.bib22)）与 AIME）、代码（HumanEval（[Chen et al., 2021](#bib.bib23)）、MBPP（[Austin et al., 2021](#bib.bib24)）与 LiveCodeBench（[Jain et al., 2025](#bib.bib25)））以及对话（MT-Bench（[Zheng et al., 2023](#bib.bib26)））。

**实现**。我们在 OpenPerfectBlend（[Xu et al., 2024](#bib.bib29)）上，以 $T_{\mathrm{train}}=1$ 重生成的目标响应训练 UBTree。我们先用 SpecForge（[Li et al., 2026b](#bib.bib30)）以块大小 16 重训 DFlash（[Chen et al., 2026](#bib.bib5)）提议器 6 个 epoch 直至收敛，然后联合训练提议器与选择器 2 个 epoch，选择器与骨干的学习率分别为 $6\times 10^{-4}$ 与 $2\times 10^{-5}$。与需要为不同解码温度 $T_{\mathrm{infer}}$ 使用不同检查点的基线不同，我们在 $T_{\mathrm{infer}}=\{0,1\}$ 下使用同一个在 $T_{\mathrm{train}}=1$ 下训练的 UBTree 检查点。评测使用 $1\times$ NVIDIA H200、batch size 为 1、transformers 后端。树构建方面，我们沿用 DARTree（[Li et al., 2026c](#bib.bib18)）的设置：非根节点数 $B=64$、搜索宽度 $W=12$、每位置候选 token 数 $K=64$，但深度加成取不同的 $\zeta=0$。训练与评测协议详见[附录 B](#A2)。

**基线**。我们将 UBTree 与单路径方法 DFlash（[Chen et al., 2026](#bib.bib5)）、Domino（[Huang et al., 2026](#bib.bib7)），以及基于树的 EAGLE-3（[Li et al., 2026d](#bib.bib6)）、DDTree（[Ringel and Romano, 2026](#bib.bib19)）和 DARTree（[Li et al., 2026c](#bib.bib18)）进行比较，预算见[表 1](#S4.T1)。我们在相同的 OpenPerfectBlend 数据集上、按对应 $T_{\mathrm{infer}}$ 重训 EAGLE-3 与 DFlash 各 6 个 epoch；Domino（块大小 17）的结果取自其原论文，同样在 OpenPerfectBlend 上训练。我们分别使用重训的 DFlash 与已发布的 Domino 检查点、按各自原始设置重新评测 DDTree 与 DARTree。由于缺少已发布的检查点，Domino 与 DARTree 仅在 instruct 模型上参与比较。为公平起见，我们将 DARTree 的最大草稿深度限制为 16，以与 DDTree 和 UBTree 对齐——因为其底层 Domino 检查点使用块大小 17，否则会允许更大的最大接受长度。

**结果**。[表 1](#S4.T1)显示，UBTree 在贪心解码下于 Qwen3-4B 与 Qwen3-8B 上分别取得 $6.88\times$ 与 $6.94\times$ 的平均加速比，在温度 1 采样下分别取得 $6.00\times$ 与 $5.84\times$。它在全部 28 项基准的加速比上都胜过 DARTree，平均提升 7.4–13.4%。在 Qwen3-4B 开启思考模式时，UBTree 在 $T_{\mathrm{infer}}=0$ 与 1 下分别比 DDTree 的平均加速比高出 25.3% 与 29.9%。我们的优势在 $T_{\mathrm{infer}}=1$ 下尤为突出，验证了高熵适配的有效性。

**并发服务**。[表 2](#S4.T2)在 SGLang（[Zheng et al., 2024](#bib.bib31)）中、客户端并发 $C\in\{1,8,16,32\}$ 下比较 UBTree 与各基线。所有方法在单张 NVIDIA H200 上以 BF16 运行 SGLang 并启用 CUDA Graphs。结果聚合自与[第 4.1 节](#S4.SS1)相同的基准。沿用 DARTree（[Li et al., 2026c](#bib.bib18)），我们采用自适应树策略：按服务负载选择不同的树预算 $B$ 与宽度 $W$。我们对每种方法与并发组合，使用相同的候选配置集与选择准则分别调优 $B/W$。在 $C\in\{1,8,16,32\}$ 下，UBTree 在 Qwen3-4B 上使用 $B/W=64/12,64/12,64/12,16/3$，在 Qwen3-8B 上使用 $B/W=64/12,64/12,16/12,16/3$；DARTree 在两个模型上均使用 $B/W=64/12,64/12,32/8,16/3$。UBTree 在所有设置下取得最高吞吐量，比次优方法高出 7.0–16.3%。在 $C=32$ 时，UBTree 在 Qwen3-4B 与 Qwen3-8B 上分别达到 6560.4 与 5851.4 tokens/s，超过最强单路径基线 7.3% 与 7.7%。

表 2：$T_{\mathrm{infer}}=1$ 下 Qwen3-4B 与 Qwen3-8B 的并发服务结果。每个单元格报告聚合输出 tokens/s / 相对同并发下 AR 基线行的加速比。

| 模型 | 方法 | $C=1$ | $C=8$ | $C=16$ | $C=32$ |
| --- | --- | --- | --- | --- | --- |
| Qwen3-4B | 自回归基线 | 253.5 / $1.00\times$ | 1404.9 / $1.00\times$ | 2208.3 / $1.00\times$ | 3307.4 / $1.00\times$ |
| | DFlash | 796.4 / $3.14\times$ | 2287.2 / $1.63\times$ | 3664.4 / $1.66\times$ | 6071.9 / $1.84\times$ |
| | Domino | 816.3 / $3.22\times$ | 2258.9 / $1.61\times$ | 3636.5 / $1.65\times$ | 6115.5 / $1.85\times$ |
| | DDTree | 844.6 / $3.33\times$ | 2390.8 / $1.70\times$ | 3669.8 / $1.66\times$ | 4810.4 / $1.45\times$ |
| | DARTree（自适应 $B/W$） | 978.5 / $3.86\times$ | 2405.1 / $1.71\times$ | 3770.3 / $1.71\times$ | 5619.9 / $1.70\times$ |
| | UBTree（自适应 $B/W$） | 1089.1 / $4.30\times$ | 2797.4 / $1.99\times$ | 4271.9 / $1.93\times$ | 6560.4 / $1.98\times$ |
| Qwen3-8B | 自回归基线 | 180.9 / $1.00\times$ | 1126.2 / $1.00\times$ | 1865.9 / $1.00\times$ | 2770.9 / $1.00\times$ |
| | DFlash | 634.7 / $3.51\times$ | 2181.7 / $1.94\times$ | 3596.0 / $1.93\times$ | 5265.4 / $1.90\times$ |
| | Domino | 676.2 / $3.74\times$ | 2137.9 / $1.90\times$ | 3582.7 / $1.92\times$ | 5435.2 / $1.96\times$ |
| | DDTree | 686.8 / $3.80\times$ | 2013.9 / $1.79\times$ | 3303.5 / $1.77\times$ | 3603.6 / $1.30\times$ |
| | DARTree（自适应 $B/W$） | 824.4 / $4.56\times$ | 2280.1 / $2.02\times$ | 3514.5 / $1.88\times$ | 4844.9 / $1.75\times$ |
| | UBTree（自适应 $B/W$） | 881.7 / $4.87\times$ | 2644.4 / $2.35\times$ | 4069.9 / $2.18\times$ | 5851.4 / $2.11\times$ |

表 3：生产规模模型上的加速比与接受长度（$\tau$）。每个基准报告加速比与平均接受长度，「平均」列为所有基准上的均值。M-500、HE、LCB、MT-B 分别表示 MATH-500、HumanEval、LiveCodeBench、MT-Bench。

| 模型 | 方法 | GSM8K 加速比 | $\tau$ | M-500 加速比 | $\tau$ | AIME 加速比 | $\tau$ | HE 加速比 | $\tau$ | MBPP 加速比 | $\tau$ | LCB 加速比 | $\tau$ | MT-B 加速比 | $\tau$ | 平均加速比 | $\tau$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Ling3-Flash | DSpark | 5.14 | 6.09 | 4.93 | 5.81 | 4.22 | 4.96 | 5.37 | 6.32 | 4.50 | 5.93 | 4.18 | 4.98 | 3.19 | 3.74 | 4.50 | 5.40 |
| | DFlash | 4.85 | 5.73 | 4.83 | 5.58 | 4.17 | 4.80 | 5.11 | 6.00 | 4.39 | 5.55 | 3.97 | 4.63 | 3.11 | 3.58 | 4.35 | 5.12 |
| | UBTree | 5.83 | 7.37 | 5.87 | 7.18 | 5.43 | 6.60 | 5.94 | 7.42 | 5.00 | 6.85 | 5.22 | 6.54 | 4.24 | 5.27 | 5.36 | 6.75 |
| Qwen3.8-27B | DSpark | 5.20 | 6.74 | 4.76 | 6.07 | 4.41 | 5.65 | 5.18 | 6.85 | 4.26 | 5.79 | 3.47 | 4.53 | 3.00 | 3.82 | 4.32 | 5.64 |
| | DFlash 2 | 4.65 | 6.29 | 4.67 | 6.29 | 4.48 | 6.00 | 5.06 | 6.98 | 4.30 | 6.11 | 3.55 | 4.82 | 2.92 | 3.95 | 4.24 | 5.78 |
| | UBTree | 5.05 | 7.59 | 5.28 | 7.50 | 5.07 | 7.33 | 5.14 | 7.66 | 4.67 | 7.32 | 4.44 | 6.54 | 3.84 | 5.61 | 4.78 | 7.08 |

### 4.2 生产规模实验

**评测**。我们在两个生产模型上评测 UBTree：Ling3-Flash（124B-A5.1B MoE）与 Qwen3.8-27B（[Qwen Team, 2026](#bib.bib48)），基准与[第 4.1 节](#S4.SS1)相同。在 Ling3-Flash 上，我们将 UBTree 与 DSpark（[Cheng et al., 2026](#bib.bib16)）和 DFlash（[Chen et al., 2026](#bib.bib5)）比较；在 Qwen3.8-27B 上与 DSpark 和 DFlash 2（[Inco AI, 2026](#bib.bib17)）比较。我们通过在关闭思考模式的解码下用各目标模型重生成响应，来构建目标专属训练集。基线与 UBTree 训练方面，Qwen3.8-27B 使用 OpenPerfectBlend（[Xu et al., 2024](#bib.bib29)）提示词，而 Ling3-Flash 使用包含 250 万样本、150 亿 token、64K 上下文长度的监督微调语料。对 Qwen3.8-27B，我们加载官方发布的 Qwen3.8-27B DFlash 2 检查点，并在我们重生成的 Qwen3.8-27B rollout 上以学习率 $3\times 10^{-4}$ 对 DFlash 2 选择器与 UBTree 选择器各微调 2 个 epoch。对 Ling3-Flash，我们以块大小 8、学习率 $2\times 10^{-5}$ 训练 DFlash 3 个 epoch，随后在 DFlash 基础上以学习率 $3\times 10^{-4}$ 训练 UBTree 2 个 epoch。树验证使用[第 4.1 节](#S4.SS1)的设置。

**SGLang 集成**。我们在 SGLang（[Zheng et al., 2024](#bib.bib31)）中实现 UBTree。DFlash 与 DSpark 使用 SGLang 官方实现，Qwen3.8-27B 的实现遵循官方 DFlash 2 代码库。我们在四张 H200 GPU 上使用 TP 度 4，目标与草稿模型使用相同度数。所有实验使用 batch size 1、贪心起草解码并关闭思考模式。Ling3-Flash 与 Qwen3.8-27B 分别使用混合注意力，含 Kimi Delta Attention（[Kimi Team et al., 2025](#bib.bib32)）与 Gated DeltaNet（[Yang et al., 2025b](#bib.bib33)）层。受 Bole（[Wang et al., 2026a](#bib.bib36)）启发，树验证中每个节点从其父节点继承循环状态与卷积状态，且只有被接受路径上的状态与 KV 条目会被提交。

**结果**。[表 3](#S4.T3)显示，UBTree 在全部 14 项模型–基准对比中取得最高接受长度，并在其中 12 项中取得最高加速比。在七个基准上平均，UBTree 在 Ling3-Flash 与 Qwen3.8-27B 上分别达到 $5.36\times$ 与 $4.78\times$ 的加速比。

### 4.3 长上下文任务

**设置**。我们在 Ling3-Flash 上评测接受长度：长输入用 LongBench-v2（[Bai et al., 2025](#bib.bib34)），长续写智能体（agentic）任务用 SWE-bench（[Jimenez et al., 2024](#bib.bib35)）。对 SWE-bench，所有方法回放相同的记录。评测协议详见[附录 B.3](#A2.SS3)。

**结果**。[图 1](#S0.F1)(c) 显示，UBTree 在每个上下文长度区间都取得最高接受长度，在 LongBench-v2 上超过最强基线 34.6–42.1%，在 SWE-bench 上超过 29.0–37.8%。这些结果表明，无论面对较长的初始提示词还是不断增长的智能体历史，UBTree 都能保持优势。定量结果见[附录 C.2](#A3.SS2)。

表 4：在关闭思考模式的 Qwen3-4B 上的选择器、训练温度与训练目标消融。上：$T_{\mathrm{infer}}=0$ 下的加速比与接受长度（$\tau$）。中：不同训练与推理温度下的接受长度，两个面板使用相同检查点评测。下：固定架构与训练温度下的训练目标消融。

**上：$T_{\mathrm{infer}}=0$ 下的加速比与接受长度**

| | GSM8K 加速比 | $\tau$ | M-500 加速比 | $\tau$ | AIME 加速比 | $\tau$ | HE 加速比 | $\tau$ | MBPP 加速比 | $\tau$ | LCB 加速比 | $\tau$ | MT-B 加速比 | $\tau$ | 平均加速比 | $\tau$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DFlash 2 选择器 + 树 | 7.58 | 11.08 | 7.42 | 10.87 | 6.13 | 8.98 | 5.88 | 8.48 | 5.64 | 8.44 | 5.40 | 7.77 | 3.60 | 6.15 | 5.95 | 8.82 |
| UBTree 选择器 + 树 | 8.16 | 12.11 | 7.83 | 11.67 | 6.79 | 10.06 | 6.73 | 9.61 | 6.21 | 9.54 | 6.04 | 8.78 | 4.26 | 7.23 | 6.57 | 9.86 |
| + $T_{\mathrm{train}}=1$ | 8.54 | 12.58 | 8.18 | 12.15 | 6.92 | 10.13 | 7.07 | 10.22 | 6.66 | 9.98 | 6.37 | 9.24 | 4.39 | 7.32 | 6.88 | 10.23 |

**中：不同训练与推理温度下的接受长度（左 8 列为 $T_{\mathrm{infer}}=0$，右 8 列为 $T_{\mathrm{infer}}=1$）**

| $T_{\mathrm{train}}$ | GSM8K | M-500 | AIME | HE | MBPP | LCB | MT-B | 平均 | GSM8K | M-500 | AIME | HE | MBPP | LCB | MT-B | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0.8 | 12.58 | 12.12 | 10.57 | 10.00 | 9.82 | 9.15 | 7.26 | 10.21 | 11.72 | 10.47 | 7.52 | 9.39 | 9.17 | 7.63 | 6.58 | 8.93 |
| 1.0 | 12.58 | 12.15 | 10.13 | 10.22 | 9.98 | 9.24 | 7.32 | 10.23 | 11.79 | 10.54 | 7.63 | 9.43 | 9.30 | 7.72 | 6.68 | 9.01 |
| 1.1 | 12.64 | 12.04 | 10.08 | 10.09 | 9.77 | 9.02 | 7.15 | 10.11 | 11.71 | 10.52 | 7.61 | 9.48 | 9.12 | 7.71 | 6.69 | 8.98 |
| 1.2 | 12.59 | 11.94 | 9.90 | 10.10 | 9.87 | 9.01 | 7.22 | 10.09 | 11.72 | 10.61 | 7.47 | 9.31 | 9.40 | 7.80 | 6.72 | 9.00 |

**下：训练目标消融（左 5 列为 $T_{\mathrm{infer}}=0$，右 5 列为 $T_{\mathrm{infer}}=1$）**

| $T_{\mathrm{infer}}$ | 选择器损失 | $\beta$ | 加速比 | $\tau$ | $T_{\mathrm{infer}}$ | 选择器损失 | $\beta$ | 加速比 | $\tau$ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 硬标签 CE | 0.1 | 6.84 | 10.08 | 1 | 硬标签 CE | 0.1 | 5.99 | 8.93 |
| 0 | 前向 KL | 0.1 | 6.88 | 10.23 | 1 | 前向 KL | 0.1 | 6.00 | 9.01 |
| 0 | 前向 KL | 0 | 6.87 | 10.14 | 1 | 前向 KL | 0 | 6.01 | 9.01 |

### 4.4 消融研究

**架构与高温训练**。我们首先在 $T_{\mathrm{infer}}=0$ 与[第 4.1 节](#S4.SS1)的设置下，于 Qwen3-4B 上对两项设计——选择器架构与高温训练温度——进行消融。如[表 4](#S4.T4)（上）所示，我们结合深度码本与深度校准的选择器架构在所有基准上同时提升加速比与接受长度，将平均值分别从 $5.95\times$ 提高到 $6.57\times$、从 8.82 提高到 9.86。更高的训练温度进一步将平均加速比与接受长度提升到 $6.88\times$ 与 10.23，验证了我们的树原生训练。

**训练温度扫描**。我们随后在 Qwen3-4B 上考察 UBTree 的最优训练温度 $T_{\mathrm{train}}$：在 $T_{\mathrm{train}}\in\{0.8,1.0,1.1,1.2\}$ 中变化，并在 $T_{\mathrm{infer}}\in\{0,1\}$ 下评测各检查点（[表 4](#S4.T4) 中）。在测试的温度中，$T_{\mathrm{train}}=1$ 在两个推理温度下都取得最高的平均接受长度。

**训练目标**。我们还在[表 4](#S4.T4)（下）中，按七个基准上的平均加速比与接受长度比较不同训练目标的选择。对选择器使用交叉熵（CE）损失、以及取消提议器的 CE 损失，都会在两个推理温度下降低接受长度。更多消融细节见[附录 B.4](#A2.SS4)。

## 5 相关工作

**并行起草与 token 级依赖**。DFlash 在起草块中并行生成 token（[Chen et al., 2026](#bib.bib5)）。Domino 与 DSpark 通过串行修正恢复 token 级依赖（[Huang et al., 2026](#bib.bib7); [Cheng et al., 2026](#bib.bib16)），而 DFlash 2 使用低秩选择器为单路径起草并行地为相邻候选对打分（[Inco AI, 2026](#bib.bib17)）。UBTree 保留了这一打分形式，但重新设计了 token 表示，并学习随深度变化的权重来组合提议器 logits 与选择器分数，用于树验证。

**基于树的投机解码**。SpecInfer 与 Medusa 保留多条草稿路径用于树验证（[Miao et al., 2024](#bib.bib11); [Cai et al., 2024](#bib.bib10)），EAGLE-2 则使树结构适配提议置信度（[Li et al., 2024a](#bib.bib13)）。DART 将 $n$-gram 引导的剪枝应用于并行预测（[Liu et al., 2026](#bib.bib15)）。DDTree 与 DARTree 分别使用逐位置概率与路径条件修正，从块并行提议构建树（[Ringel and Romano, 2026](#bib.bib19); [Li et al., 2026c](#bib.bib18)）。与现有树起草方法相比，UBTree 利用树原生训练，以备选项上的目标概率（而非单个采样 token）监督选择器。

## 6 结论

UBTree 为投机解码提供了一个新视角：树验证要求设计显式考虑多条合理的生成路径。其在各基准上的强劲表现证明了这一原则的有效性。我们还在[附录 D](#A4)中讨论了本工作的局限性。未来工作可以进一步推进推理时的树规模选择，使验证预算能随硬件、服务负载与延迟需求的不同，在候选覆盖与验证成本之间取得平衡。

## 参考文献
* An et al. (2026)
  Z. An, H. Bai, Z. Liu, D. Li, and E. Barsoum
  PARD: accelerating llm inference with low-cost parallel draft model adaptation.
  In International Conference on Learning Representations,
  Vol. 2026, pp. 144562–144579.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Arriola et al. (2025)
  M. Arriola, A. Gokaslan, J. T. Chiu, Z. Yang, Z. Qi, J. Han, S. S. Sahoo, and V. Kuleshov
  Block diffusion: interpolating between autoregressive and diffusion language models.
  In International Conference on Learning Representations,
  External Links: [Link](https://arxiv.org/abs/2503.09573)
  Cited by: [Appendix E](#A5.p3.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Austin et al. (2021)
  J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. Le, et al.
  Program synthesis with large language models.
  arXiv preprint arXiv:2108.07732.
  Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Bachmann et al. (2025)
  G. Bachmann, S. Anagnostidis, A. Pumarola, M. Georgopoulos, A. Sanakoyeu, Y. Du, E. Schönfeld, A. Thabet, and J. Kohler
  Judge decoding: faster speculative sampling requires going beyond model alignment.
  In International Conference on Learning Representations,
  External Links: [Link](https://proceedings.iclr.cc/paper_files/paper/2025/hash/656d6174fd5ffb01c843f269649ab5cb-Abstract-Conference.html)
  Cited by: [Appendix E](#A5.p2.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Bai et al. (2025)
  Y. Bai, S. Tu, J. Zhang, H. Peng, X. Wang, X. Lv, S. Cao, J. Xu, L. Hou, Y. Dong, et al.
  Longbench v2: towards deeper understanding and reasoning on realistic long-context multitasks.
  In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),
  pp. 3639–3664.
  Cited by: [§B.3](#A2.SS3.p2.1 "B.3 Long-context Evaluation Protocol ‣ Appendix B Experimental Setup Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.3](#S4.SS3.p1.1 "4.3 Long-context Tasks ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Cai et al. (2024)
  T. Cai, Y. Li, Z. Geng, H. Peng, J. D. Lee, D. Chen, and T. Dao
  Medusa: simple LLM inference acceleration framework with multiple decoding heads.
  In Forty-first International Conference on Machine Learning,
  External Links: [Link](https://openreview.net/forum?id=PEpbUobfJv)
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p3.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p2.1 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p2.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Chen et al. (2023)
  C. Chen, S. Borgeaud, G. Irving, J. Lespiau, L. Sifre, and J. Jumper
  Accelerating large language model decoding with speculative sampling.
  arXiv preprint arXiv:2302.01318.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p1.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p1.1 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Chen et al. (2026)
  J. Chen, Y. Liang, and Z. Liu
  DFlash: block diffusion for flash speculative decoding.
  In Forty-third International Conference on Machine Learning,
  External Links: [Link](https://openreview.net/forum?id=Oz335dV48X)
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [1st item](#S1.I1.i1.p1.1 "In 1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p1.1 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p1.2 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§3.1.1](#S3.SS1.SSS1.p1.2 "3.1.1 Unigram Proposer ‣ 3.1 UBTree Architecture ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.1](#S4.SS1.p2.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.1](#S4.SS1.p3.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.2](#S4.SS2.p1.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p1.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Chen et al. (2021)
  M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. D. O. Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, et al.
  Evaluating large language models trained on code.
  arXiv preprint arXiv:2107.03374.
  Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Cheng et al. (2026)
  X. Cheng, X. Yu, C. Shao, J. Li, Y. Xiong, Y. Qian, J. Zhu, S. Ma, X. Zhang, J. Ye, et al.
  DSpark: confidence-scheduled speculative decoding with semi-autoregressive generation.
  arXiv preprint arXiv:2607.05147.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p4.2 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.2](#S4.SS2.p1.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p1.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Cobbe et al. (2021)
  K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al.
  Training verifiers to solve math word problems.
  arXiv preprint arXiv:2110.14168.
  Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Devic et al. (2025)
  S. Devic, C. Peale, A. Bradley, S. Williamson, P. Nakkiran, and A. Gollakota
  Trace length is a simple uncertainty signal in reasoning models.
  arXiv preprint arXiv:2510.10409.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* DiffusionGemma Team et al. (2026)
  DiffusionGemma Team, A. A. Taïga, J. Assiene, D. Calandriello, R. Chaabouni, J. Gante, et al.
  DiffusionGemma technical report.
  arXiv preprint arXiv:2608.00146.
  External Links: [Link](https://arxiv.org/abs/2608.00146)
  Cited by: [Appendix E](#A5.p3.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Garipov et al. (2026)
  R. Garipov, F. Velikonivtsev, I. Ermakov, R. Svirschevski, V. Egiazarian, and M. Ryabinin
  Autojudge: judge decoding without manual annotation.
  Advances in Neural Information Processing Systems 38, pp. 94605–94642.
  Cited by: [Appendix E](#A5.p2.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Gloeckle et al. (2024)
  F. Gloeckle, B. Youbi Idrissi, B. Roziere, D. Lopez-Paz, and G. Synnaeve
  Better & faster large language models via multi-token prediction.
  In Proceedings of the 41st International Conference on Machine Learning,
  pp. 15706–15734.
  External Links: [Link](https://proceedings.mlr.press/v235/gloeckle24a.html)
  Cited by: [Appendix E](#A5.p3.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Holsman et al. (2025)
  M. Holsman, Y. Huang, and B. Dhingra
  Fuzzy speculative decoding for a tunable accuracy-runtime tradeoff.
  In Findings of the Association for Computational Linguistics: ACL 2025,
  pp. 26257–26273.
  External Links: [Document](https://dx.doi.org/10.18653/v1/2025.findings-acl.1346),
  [Link](https://aclanthology.org/2025.findings-acl.1346/)
  Cited by: [Appendix E](#A5.p2.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Huang et al. (2026)
  J. Huang, Y. Zhang, Q. Zhang, H. Lin, H. Xu, and L. Zhang
  Domino: decoupling causal modeling from autoregressive drafting in speculative decoding.
  arXiv preprint arXiv:2605.29707.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p1.1 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.1](#S4.SS1.p3.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p1.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Inception Labs et al. (2025)
  Inception Labs, S. Khanna, S. Kharbanda, S. Li, H. Varma, E. Wang, S. Birnbaum, Z. Luo, Y. Miraoui, A. Palrecha, S. Ermon, A. Grover, and V. Kuleshov
  Mercury: ultra-fast language models based on diffusion.
  arXiv preprint arXiv:2506.17298.
  External Links: [Link](https://arxiv.org/abs/2506.17298)
  Cited by: [Appendix E](#A5.p3.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Inco AI (2026)
  Inco AI
  DFlash 2: keep drafting parallel.
  External Links: [Link](https://inco.ai/blog/dflash2/)
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p1.2 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§3.1.1](#S3.SS1.SSS1.p1.2 "3.1.1 Unigram Proposer ‣ 3.1 UBTree Architecture ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§3.1.2](#S3.SS1.SSS2.p1.1 "3.1.2 Bigram Selector ‣ 3.1 UBTree Architecture ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.2](#S4.SS2.p1.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p1.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Jain et al. (2025)
  N. Jain, A. Gu, W. Li, F. Yan, T. Zhang, S. Wang, A. Solar-Lezama, K. Sen, and I. Stoica
  Livecodebench: holistic and contamination free evaluation of large language models for code.
  In International Conference on Learning Representations,
  Vol. 2025, pp. 58791–58831.
  Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Jimenez et al. (2024)
  C. E. Jimenez, J. Yang, A. Wettig, S. Yao, K. Pei, O. Press, and K. Narasimhan
  SWE-bench: can language models resolve real-world GitHub issues?.
  In International Conference on Learning Representations,
  Cited by: [§B.3](#A2.SS3.p3.1 "B.3 Long-context Evaluation Protocol ‣ Appendix B Experimental Setup Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.3](#S4.SS3.p1.1 "4.3 Long-context Tasks ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Kim et al. (2023)
  S. Kim, K. Mangalam, S. Moon, J. Malik, M. W. Mahoney, A. Gholami, and K. Keutzer
  Speculative decoding with big little decoder.
  In Advances in Neural Information Processing Systems,
  Vol. 36.
  External Links: [Link](https://proceedings.neurips.cc/paper_files/paper/2023/hash/7b97adeafa1c51cf65263459ca9d0d7c-Abstract-Conference.html)
  Cited by: [Appendix E](#A5.p2.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Kimi Team et al. (2025)
  Kimi Team, Y. Zhang, Z. Lin, X. Yao, J. Hu, F. Meng, et al.
  Kimi Linear: an expressive, efficient attention architecture.
  arXiv preprint arXiv:2510.26692.
  Cited by: [§4.2](#S4.SS2.p2.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Leviathan et al. (2023)
  Y. Leviathan, M. Kalman, and Y. Matias
  Fast inference from transformers via speculative decoding.
  In International conference on machine learning,
  pp. 19274–19286.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p1.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p1.1 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Li et al. (2026a)
  G. Li, Z. Fu, M. Fang, Q. Zhao, M. Tang, C. Yuan, and J. Wang
  Diffuspec: unlocking diffusion language models for speculative decoding.
  In Findings of the Association for Computational Linguistics: ACL 2026,
  pp. 20896–20910.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Li et al. (2026b)
  S. Li, C. Wang, Y. Zhu, Y. Wang, F. Yin, S. Shi, Y. Chen, X. Dong, Q. Chen, J. Pan, et al.
  SpecForge: a flexible and efficient open-source training framework for speculative decoding.
  arXiv preprint arXiv:2603.18567.
  Cited by: [§4.1](#S4.SS1.p2.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Li et al. (2026c)
  T. Li, Y. Luo, X. Shang, and Z. Shen
  DARTree: speculative diffusion decoding with autoregressive draft trees.
  arXiv preprint arXiv:2608.13524.
  Cited by: [Appendix A](#A1.p1.1 "Appendix A Tree Construction Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [Appendix A](#A1.p5.2 "Appendix A Tree Construction Details ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p3.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p3.1 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§3.1.3](#S3.SS1.SSS3.p1.1 "3.1.3 Tree Construction and Verification ‣ 3.1 UBTree Architecture ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.1](#S4.SS1.p2.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.1](#S4.SS1.p3.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.1](#S4.SS1.p5.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p2.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Li et al. (2024a)
  Y. Li, F. Wei, C. Zhang, and H. Zhang
  Eagle-2: faster inference of language models with dynamic draft trees.
  In Proceedings of the 2024 conference on empirical methods in natural language processing,
  pp. 7421–7432.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p3.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p2.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Li et al. (2024b)
  Y. Li, F. Wei, C. Zhang, and H. Zhang
  EAGLE: speculative sampling requires rethinking feature uncertainty.
  In Forty-first International Conference on Machine Learning,
  External Links: [Link](https://openreview.net/forum?id=1NdN7eXyb4)
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Li et al. (2026d)
  Y. Li, F. Wei, C. Zhang, and H. Zhang
  Eagle-3: scaling up inference acceleration of large language models via training-time test.
  Advances in Neural Information Processing Systems 38, pp. 136737–136756.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.1](#S4.SS1.p3.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Lightman et al. (2024)
  H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe
  Let’s verify step by step.
  In International Conference on Learning Representations,
  Vol. 2024, pp. 39578–39601.
  Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Liu et al. (2025)
  A. Liu, M. He, S. Zeng, S. Zhang, L. Zhang, C. Wu, W. Jia, Y. Liu, X. Zhou, and J. Zhou
  WeDLM: reconciling diffusion language models with standard causal attention for fast inference.
  arXiv preprint arXiv:2512.22737.
  External Links: [Link](https://arxiv.org/abs/2512.22737)
  Cited by: [Appendix E](#A5.p3.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Liu et al. (2026)
  F. Liu, X. Li, K. Zhao, Y. Gao, Z. Zhou, Z. Zhang, Z. Wang, W. Dou, S. Zhong, and C. Tian
  DART: diffusion-inspired speculative decoding for fast llm inference.
  arXiv preprint arXiv:2601.19278.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p2.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Miao et al. (2024)
  X. Miao, G. Oliaro, Z. Zhang, X. Cheng, Z. Wang, Z. Zhang, R. Y. Y. Wong, A. Zhu, L. Yang, X. Shi, et al.
  Specinfer: accelerating large language model serving with tree-based speculative inference and verification.
  In Proceedings of the 29th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 3,
  pp. 932–949.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p3.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p2.1 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p2.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Narasimhan et al. (2025)
  H. Narasimhan, W. Jitkrittum, A. S. Rawat, S. Kim, N. Gupta, A. K. Menon, and S. Kumar
  Faster cascades via speculative decoding.
  In International Conference on Learning Representations,
  External Links: [Link](https://proceedings.iclr.cc/paper_files/paper/2025/hash/6f43166f50f26e8d8f3edc5545b0749f-Abstract-Conference.html)
  Cited by: [Appendix E](#A5.p2.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Nie et al. (2026)
  S. Nie, F. Zhu, Z. You, X. Zhang, J. Ou, J. Hu, J. Zhou, Y. Lin, J. Wen, and C. Li
  Large language diffusion models.
  Advances in Neural Information Processing Systems 38, pp. 50608–50646.
  Cited by: [Appendix E](#A5.p3.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Qwen Team (2026)
  Qwen Team
  Qwen3.8-Max: a new bar for coding and cowork.
  External Links: [Link](https://qwen.ai/blog?id=qwen3.8)
  Cited by: [§4.2](#S4.SS2.p1.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Ringel and Romano (2026)
  L. Ringel and Y. Romano
  Accelerating speculative decoding with block diffusion draft trees.
  arXiv preprint arXiv:2604.12989.
  Cited by: [Appendix E](#A5.p1.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§1](#S1.p3.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§2](#S2.p3.1 "2 Background ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.1](#S4.SS1.p3.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§5](#S5.p2.1 "5 Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Wang et al. (2026a)
  L. Wang, Y. Su, X. Wu, C. You, Y. Liu, Z. Qiu, J. Zhang, J. Zheng, F. Liu, J. Zhang, et al.
  Bole: efficient tree speculation for hybrid-attention language models.
  arXiv preprint arXiv:2608.01651.
  Cited by: [§4.2](#S4.SS2.p2.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Wang et al. (2026b)
  Z. Wang, S. R. Kasa, A. M. S, S. K. Kasa, J. Zou, S. Negi, R. Zhang, N. Jiang, and Q. Song
  DIVERSED: relaxed speculative decoding via dynamic ensemble verification.
  In Proceedings of the 29th International Conference on Artificial Intelligence and Statistics,
  Vol. 300, pp. 2341–2349.
  External Links: [Link](https://proceedings.mlr.press/v300/wang26d.html)
  Cited by: [Appendix E](#A5.p2.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Xie et al. (2025)
  Z. Xie, J. Ye, L. Zheng, J. Gao, J. Dong, Z. Wu, X. Zhao, S. Gong, X. Jiang, Z. Li, et al.
  Dream-coder 7b: an open diffusion language model for code.
  arXiv preprint arXiv:2509.01142.
  Cited by: [Appendix E](#A5.p3.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Xu et al. (2024)
  T. Xu, E. Helenowski, K. A. Sankararaman, D. Jin, K. Peng, E. Han, S. Nie, C. Zhu, H. Zhang, W. Zhou, et al.
  The perfect blend: redefining rlhf with mixture of judges.
  arXiv preprint arXiv:2409.20370.
  Cited by: [§4.1](#S4.SS1.p2.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.2](#S4.SS2.p1.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Yang et al. (2025a)
  A. Yang, A. Li, B. Yang, B. Zhang, B. Hui, B. Zheng, B. Yu, C. Gao, C. Huang, C. Lv, et al.
  Qwen3 technical report.
  arXiv preprint arXiv:2505.09388.
  Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Yang et al. (2026)
  P. Yang, C. Du, F. Zhang, H. Wang, T. Pang, C. Du, and B. An
  LongSpec: long-context lossless speculative decoding with efficient drafting and verification.
  In Proceedings of the 64th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),
  pp. 1826–1844.
  Cited by: [§1](#S1.p2.1 "1 Introduction ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Yang et al. (2025b)
  S. Yang, J. Kautz, and A. Hatamizadeh
  Gated delta networks: improving mamba2 with delta rule.
  In International Conference on Learning Representations,
  Vol. 2025, pp. 29687–29707.
  Cited by: [§4.2](#S4.SS2.p2.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Zheng et al. (2023)
  L. Zheng, W. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. Xing, et al.
  Judging llm-as-a-judge with mt-bench and chatbot arena.
  Advances in neural information processing systems 36, pp. 46595–46623.
  Cited by: [§4.1](#S4.SS1.p1.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Zheng et al. (2024)
  L. Zheng, L. Yin, Z. Xie, C. Sun, J. Huang, C. H. Yu, S. Cao, C. Kozyrakis, I. Stoica, J. E. Gonzalez, et al.
  Sglang: efficient execution of structured language model programs.
  Advances in neural information processing systems 37, pp. 62557–62583.
  Cited by: [§4.1](#S4.SS1.p5.1 "4.1 Academic-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding"),
  [§4.2](#S4.SS2.p2.1 "4.2 Production-scale Experiment ‣ 4 Experiments ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Zhou et al. (2024)
  Y. Zhou, K. Lyu, A. S. Rawat, A. K. Menon, A. Rostamizadeh, S. Kumar, J. Kagy, and R. Agarwal
  DistillSpec: improving speculative decoding via knowledge distillation.
  In International Conference on Learning Representations,
  External Links: [Link](https://openreview.net/forum?id=rsY6J3ZaTF)
  Cited by: [Appendix E](#A5.p2.1 "Appendix E Additional Related Work ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").
* Zhu et al. (2026)
  S. Zhu, X. Ye, H. Lu, W. Shi, and G. Liu
  The many faces of on-policy distillation: pitfalls, mechanisms, and fixes.
  arXiv preprint arXiv:2605.11182.
  Cited by: [§3.2](#S3.SS2.p3.1 "3.2 Tree-native Training ‣ 3 Method ‣ UBTree: Parallel Tree Drafting via Unigram and Bigram Models for Speculative Decoding").

## 附录 A 树构建细节

UBTree 遵循 DARTree 剪枝变体的搜索流程（[Li et al., 2026c](#bib.bib18) 中的算法 1，已在[第 2 节](#S2)回顾）。DARTree 需要计算路径条件修正概率并在深度之间更新修正状态；UBTree 则直接提供预计算的提议器与选择器分数，因此无需这些修正状态更新。

**路径分数**。对固定的已验证上下文 $x_{\leq t}$，我们使用[第 3.1.1 节](#S3.SS1.SSS1)的候选集合与[式 (5)](#S3.E5)的组合分数。这些分数同时纳入了提议器 logits 与以提议器隐藏状态为条件的选择器分数。对每个前驱 $a\in\mathcal{C}_{i-1}$，在后继候选上做归一化即定义一个条件分布，其 log 概率沿候选路径累加：

$$
\begin{aligned}
q_{i}^{\mathrm{bi}}(b\mid a,x_{\leq t})&=\frac{\exp s_{i}(a,b)}{\sum_{v\in\mathcal{C}_{i}}\exp s_{i}(a,v)},\qquad b\in\mathcal{C}_{i},\\
\ell(y_{1:d})&=\sum_{i=1}^{d}\log q_{i}^{\mathrm{bi}}(y_{i}\mid y_{i-1},x_{\leq t}).
\end{aligned}
\tag{9}
$$

这里 $y_{0}=x_{t}$，$1\leq d\leq\gamma$ 为路径深度。根节点表示空草稿前缀 $\epsilon$，且 $\ell(\epsilon)=0$。每个非根节点由其完整草稿前缀 $y_{1:d}$ 标识；经不同父节点到达的相同 token 仍是不同的节点。

**深度加成**。沿用 DARTree 的打分形式，搜索在对树节点排序时允许一个非正的深度加成（depth bonus）。报告的 UBTree 评测使用 $\zeta=0$：

$$
\ell_{\zeta}(y_{1:d})=\ell(y_{1:d})+\zeta d,\qquad\zeta=0.
\tag{10}
$$

我们设 $\ell_{\zeta}(\epsilon)=0$，并用 $\zeta$ 将这一深度加成与训练损失权重 $\beta$ 区分开。加成在概率归一化之后作用于路径分数。它不改变各深度内部的排序，仅在 $\zeta<0$ 时于全局剪枝中惩罚更深的节点。

**逐深度扩展**。令 $\mathcal{F}_{d}$ 为深度 $d$ 处保留的前沿，初始化为 $\mathcal{F}_{0}=\{\epsilon\}$。在每个深度，我们用该位置的候选扩展每条保留路径，并选出得分最高的扩展：

$$
\begin{aligned}
\mathcal{E}_{d}&=\{y_{1:d}:y_{1:d-1}\in\mathcal{F}_{d-1},\ y_{d}\in\mathcal{C}_{d}\},\\
\mathcal{F}_{d}&=\operatorname{Top}_{W}(\mathcal{E}_{d};\ell_{\zeta}),\qquad d=1,\ldots,\gamma.
\end{aligned}
\tag{11}
$$

我们约定 $y_{1:0}=\epsilon$。算子 $\operatorname{Top}_{W}(\mathcal{E}_{d};\ell_{\zeta})$ 在深度 $d$ 的全部扩展中，保留深度惩罚后得分最大的至多 $W$ 个节点，而非每个父节点保留 $W$ 个子节点。对一个扩展打分，是用预计算的组合分数把[式 (9)](#A1.E9)的条件 log 概率与 $\zeta$ 加到其父节点的分数上，无需再进行选择器评估。

**全局剪枝**。保留的前沿构成候选超树。我们按同样的深度惩罚分数，从该超树中选出至多 $B$ 个非根节点：

$$
\mathcal{S}=\bigcup_{d=1}^{\gamma}\mathcal{F}_{d},\qquad\mathcal{T}=\{\epsilon\}\cup\operatorname{Top}_{B}(\mathcal{S};\ell_{\zeta}).
\tag{12}
$$

根节点单独保留，不计入 $B$。由于每个归一化概率至多为 1 且 $\zeta\leq 0$，有 $\ell_{\zeta}(y_{1:d})\leq\ell_{\zeta}(y_{1:d-1})$。因此，分数并列时优先选择祖先节点，即可保证每个被选节点保留其全部祖先，这遵循 [Li et al. (2026c)](#bib.bib18) 引理 1 中的前缀单调性论证。该选择限于已物化的超树 $\mathcal{S}$；有限宽度的扩展可能在全局剪枝之前丢弃部分路径。

**构建小结**。[算法 1](#alg1)总结了如何从预计算的提议器与选择器分数构建树，无需进一步的选择器评估。我们使用 $y_{1:0}=\epsilon$ 与 $y_{0}=x_{t}$。算子 $\operatorname{Top}_{m}$ 保留至多 $m$ 个得分最高的节点，分数并列时优先选择祖先。

算法 1　基于预计算分数的 UBTree 树构建

```
 1: 输入：已验证上下文 x_{≤t}，候选集 {C_i}_{i=1}^{γ}，
    预计算合并分数 {s_i}_{i=1}^{γ}，搜索宽度 W，非根节点预算 B。
 2: 输出：至多含 B 个非根节点的前缀封闭树 T。
 3: ζ ← 0
 4: 按式 (9) 预计算全部候选对的 log 概率 log q_i^{bi}
 5: F_0 ← {ε}，ℓ_ζ(ε) ← 0，S ← ∅
 6: for d = 1, …, γ do
 7:   E_d ← {y_{1:d} : y_{1:d-1} ∈ F_{d-1}, y_d ∈ C_d}
 8:   for all y_{1:d} ∈ E_d do
 9:     ℓ_ζ(y_{1:d}) ← ℓ_ζ(y_{1:d-1}) + log q_d^{bi}(y_d | y_{d-1}, x_{≤t}) + ζ
10:   end for
11:   F_d ← Top_W(E_d; ℓ_ζ)
12:   S ← S ∪ F_d
13: end for
14: T ← {ε} ∪ Top_B(S; ℓ_ζ)
15: return T
```

**经树注意力验证**。树构建完成后，我们在单次目标模型前向中、以树注意力验证这棵至多含 $B=64$ 个非根节点的前缀封闭草稿树。每个节点在其相应的自回归前缀下评估；验证沿每一步与目标模型采样一致的子节点进行，直到首次失配。首个未匹配的采样被保留为奖励 token（bonus token）。验证后，被接受路径上的 KV 缓存与循环状态延续到下一解码轮次，其余分支的全部状态则被丢弃。由于每个提交的 token 都是在与标准自回归解码完全相同的前缀下从目标模型采样得到的，该过程是无损的。

## 附录 B 实验设置细节

我们为[第 4 节](#S4)中的学术规模实验、长上下文评测与消融研究，提供补充的训练与评测设置。

### B.1 训练与推理配置

[表 5](#A2.T5)总结了学术规模实验的配置。我们将深度校准参数初始化为 $\rho_{i}=\kappa_{i}=0$，使提议器 logits 与选择器分数初始具有单位权重。学术规模推理以 BF16 加载目标与起草器权重，并将起草后处理捕获进单个 CUDA Graph。

表 5：除非另有说明，学术规模实验的 UBTree 配置。验证预算不含锚点。

| 设置 | 值 |
| --- | --- |
| 提议器训练 | 6 个 epoch |
| 提议器–选择器联合训练 | 2 个 epoch |
| 选择器秩 | 256 |
| 码本 MLP 隐藏宽度 | 1024 |
| 训练候选支撑集大小 | 256 |
| 起草深度 | 15 个未来位置加 1 个锚点 |
| 每位置候选 token 数 $K$ | 64 |
| 搜索宽度 $W$ | 12 |
| 验证预算 $B$ | 64 个非根节点 |
| 深度加成 $\zeta$ | 0 |

### B.2 评测与计时协议

在学术规模评测中，我们使用固定的 seed-0 子集，样本数见[表 6](#A2.T6)。每个配置在选定子集上评测一次。生成在 EOS 处或 2,048 个新 token 后停止。MT-Bench 包含 80 段两轮对话，合计 160 个被评测轮次。

对每个问题或对话轮次，每输出 token 时间（TPOT）由同一计时窗口内的解码耗时与输出 token 数计算。所有本地评测的方法与自回归基线使用相同的解码计时协议。在每个基准内，加速比为平均自回归 TPOT 与平均投机解码 TPOT 之比。接受长度在问题或对话轮次上取平均。

表 6：评测子集规模。MT-Bench 为两轮对话；其余计数指单个样本。

| 基准 | 样本数 / 对话数 |
| --- | --- |
| GSM8K | 128 |
| MATH-500 | 128 |
| AIME | 30 |
| HumanEval | 128 |
| MBPP | 128 |
| LiveCodeBench | 128 |
| MT-Bench | 80 |

### B.3 长上下文评测协议

**共享设置**。我们在 Ling3-Flash 上将 UBTree 与 DSpark 和 DFlash 比较，使用[第 4.2 节](#S4.SS2)的服务配置：四张 H200 GPU 上张量并行度 4、贪心解码、关闭思考模式。两项长上下文评测均使用并发 1 并禁用 CUDA Graphs。我们把含根节点的接受长度 $\tau$ 度量为每次目标验证调用生成的 token 数（含目标模型产出的 token）。所有方法使用最大草稿深度 7，因此最大接受长度为 8。DSpark 与 DFlash 验证单条链，而 UBTree 每轮使用 64 个非根树节点的预算。

**LongBench-v2**。我们在 LongBench-v2（[Bai et al., 2025](#bib.bib34)）上评测长输入生成。在 503 个源样本中，我们对所有方法保留相同的 401 条提示词 token 数不超过 260K 的请求。生成在 EOS 处或 2,048 个新 token 后停止。我们在生成前按提示词长度把请求分为六个上下文长度区间，上界分别为 32K、64K、96K、128K、192K 与 260K token。每个区间包含该长度范围内自然出现的基准输入。[表 8](#A3.T8)报告这些区间的接受长度与请求数，以及完整评测子集上的结果。

**SWE-bench**。我们在 SWE-bench（[Jimenez et al., 2024](#bib.bib35)）上评测随智能体历史增长的接受情况。我们首先对 30 个案例运行仅目标模型的推理，并冻结所得的 1,482 条完整请求。随后每种方法回放完全相同的已记录消息、工具调用与工具输出，生成上限固定为 256 个 token。这一共享回放协议使各方法在每个请求处的智能体上下文保持一致。为与[图 1](#S0.F1)(c) 的上下文长度轴对应，我们按提示词 token 相对该案例首个请求的增量对请求分组，区间为 $\leq 0$、0–4K、4–8K、8–16K、16–32K、32–64K 与 64–131K。$\leq 0$ 区间包含提示词长度不超过初始提示词的请求，含上下文截断或重构事件。[表 9](#A3.T9)报告各区间的接受长度与所覆盖案例数；其「总体」列报告全部 1,482 条请求上的按请求池化接受长度。

作为补充分析，我们按轨迹进度汇总相同的回放请求。我们把每个案例按时序划分为请求数大致相等的四个阶段：0–25%、25–50%、50–75% 与 75–100%。在每个案例的每个阶段内，接受长度按生成 token 总数除以目标验证调用总数计算，再在 30 个案例上等权平均。这些阶段度量的是智能体轨迹中的相对进度。由于每个请求新增的上下文量因案例与请求而异，阶段边界并不对应固定的上下文长度。

### B.4 消融协议

对[表 4](#S4.T4)的训练温度消融，我们在每个 $T_{\mathrm{train}}$ 下重生成目标响应，并将其同时用于提议器训练与提议器–选择器联合训练。每次联合训练都从对应温度下训练的提议器出发。KL 监督的目标分布使用相同的 $T_{\mathrm{train}}$，遵循[式 (7)](#S3.E7)。各温度之间，我们保持相同的选择器架构、训练配置与树搜索配置。每个得到的检查点都在 $T_{\mathrm{infer}}=0$ 与 $T_{\mathrm{infer}}=1$ 下评测。对训练目标消融，所有变体从同一提议器检查点出发并使用相同的训练响应。硬标签选择器 CE 排除采样目标 token 落在训练候选支撑集之外的位置，而前向 KL 监督所有有效位置。

## 附录 C 补充实验

### C.1 起草延迟分析

我们在 $T_{\mathrm{infer}}=0$ 下、于 128 道 GSM8K 问题上对 Qwen3-4B 进行性能分析，使用基于 Hugging Face Transformers 的实现与[第 4.1 节](#S4.SS1)的搜索预算。对每个问题，所有方法在同一张 H200 GPU 上以随机顺序运行，并在十次完整遍历上取平均。计时不含预填充与第一个完整的投机轮次。各阶段延迟用 CUDA event 测量，总轮次延迟则用同步墙钟时间独立测量。对 UBTree，起草后处理包括 LM head 投影、候选选择、选择器打分与树构建，它们被联合计时。ms/token 列报告在问题上取平均的 TPOT。

[表 7](#A3.T7)显示，UBTree 将起草后处理延迟从 DARTree 的每轮 3.36 ms 降至 1.38 ms，降幅 58.8%，而目标验证对两种方法均约 20.9 ms。因此，主要的延迟削减发生在并行选择器一侧。UBTree 在把每 token 解码延迟从 2.41 ms 降到 2.21 ms 的同时，取得了比 DARTree 更高的接受长度（12.58 对 12.50）。

表 7：Qwen3-4B 上的起草延迟分析。阶段与总延迟以每个验证轮次的 ms 计。

| 方法 | 提议器阶段 | 起草后处理 | 验证 | 其他 | 总计 | $\tau$ | ms/token |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DARTree | 3.51 | 3.36 | 20.94 | 1.64 | 29.47 | 12.50 | 2.41 |
| UBTree | 3.41 | 1.38 | 20.88 | 1.61 | 27.30 | 12.58 | 2.21 |

### C.2 长上下文任务

[表 8](#A3.T8)与[表 9](#A3.T9)给出了[图 1](#S0.F1)(c) 背后的定量结果，以及各基准上的总体接受长度。所有结果遵循[附录 B.3](#A2.SS3)的长上下文评测协议。

表 8：Ling3-Flash 在 LongBench-v2 上的接受长度（$\tau$），按请求起始提示词长度分组。所有方法使用相同的 401 条请求。「总体」列报告完整评测子集上的结果。加粗标记每列最佳接受长度。

| 提示词 token 数 | $\leq 32$K | 32–64K | 64–96K | 96–128K | 128–192K | 192–260K | 总体 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 请求数 | 109 | 71 | 47 | 69 | 73 | 32 | 401 |
| DSpark | 4.248 | 4.297 | 3.795 | 3.976 | 4.166 | 4.084 | 4.136 |
| DFlash | 4.020 | 4.046 | 3.578 | 3.678 | 3.944 | 3.919 | 3.898 |
| UBTree | 5.833 | 5.870 | 5.326 | 5.351 | 5.798 | 5.804 | 5.693 |

表 9：Ling3-Flash 在 SWE-bench 上的接受长度（$\tau$），按相对每个案例首个请求的累计提示词 token 分组。「覆盖案例」给出各区间覆盖的案例数。「总体」列报告 30 个案例共 1,482 条请求上的按请求池化接受长度。加粗标记每列最佳接受长度。

| 累计 token 数 | $\leq 0$ | 0–4K | 4–8K | 8–16K | 16–32K | 32–64K | 64–131K | 总体 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 覆盖案例 | 30 | 30 | 28 | 27 | 23 | 13 | 2 | 30 |
| DSpark | 3.718 | 3.743 | 4.023 | 3.998 | 4.089 | 4.023 | 3.965 | 3.981 |
| DFlash | 3.442 | 3.524 | 3.795 | 3.709 | 3.836 | 3.805 | 3.770 | 3.737 |
| UBTree | 4.842 | 4.829 | 5.447 | 5.389 | 5.516 | 5.408 | 5.465 | 5.341 |

**结果**。UBTree 在两个基准的每个上下文长度区间都取得最高接受长度。在 LongBench-v2 上，UBTree 达到 $\tau=5.326$–5.870，相对最强基线 DSpark 提升 34.6–42.1%。在 192–260K 提示词 token 下，UBTree 取得 $\tau=5.804$，而 DSpark 为 4.084、DFlash 为 3.919，仍几乎保持与最短区间相同的接受长度（5.833）。总体上，UBTree 取得 $\tau=5.693$，较 DSpark 提升 37.6%。在 SWE-bench 上，UBTree 在各累计上下文区间达到 $\tau=4.829$–5.516，超出 DSpark 29.0–37.8%。其总体按请求池化接受长度为 5.341，而 DSpark 为 3.981、DFlash 为 3.737，相对最强基线提升 34.2%。这些结果表明，无论面对长初始提示词还是不断增长的智能体历史，UBTree 都能保持接受优势。

**轨迹阶段结果**。在[附录 B.3](#A2.SS3)定义的补充轨迹阶段聚合下，UBTree 在 SWE-bench 四个连续阶段的接受长度分别为 5.043、5.364、5.348 与 5.476，而最强基线 DSpark 为 3.835、3.989、3.942 与 3.999。相应增益介于 31.5% 到 36.9% 之间。该汇总刻画了 UBTree 在智能体轨迹全程的优势；正文报告的 29.0–37.8% 增益对应[表 9](#A3.T9)中的累计上下文结果。两个区间是对同一回放负载在不同分组下的总结。

## 附录 D 局限性

尽管 UBTree 的经验表现强劲，仍存在两点局限。

**树起草对极高并发敏感**。投机解码的动机来自自回归推理受内存带宽限制时富余的计算资源，这在 LLM 解码中很常见。将多个草稿 token 放在一起验证，正是利用这部分资源来摊销内存访问成本。随着并发增加、推理变为计算受限，可用于投机的富余容量收缩，可能使单路径与基于树的方法都失去加速。对所有基于树的起草器而言，对这一转变的敏感性是共有的，并非 UBTree 特有。树验证在备选延续上花费额外计算，因此更偏向计算–带宽谱中富余计算更多的一端。自适应树起草可以通过随可用计算调整验证预算来缓解该局限：分支使得被验证候选的数量可以超出固定单路径块的 token 数，尽管提议器块大小仍然限制草稿深度。我们依赖负载的树预算已在测试的并发水平上保持加速（[表 2](#S4.T2)），更灵活的运行时自适应可进一步提升资源利用。UBTree 也可以服务富余计算充裕的低并发负载。因此，我们把这一局限视为对有利部署区间的约束，而非 UBTree 实用价值的根本障碍。

**自适应树策略依赖搜索得到的配置**。我们当前的自适应策略使用针对每个模型与并发水平、通过配置搜索选出的树预算 $B$ 与搜索宽度 $W$。这些设置对给定服务负载是固定的；它们并不根据每轮解码的转移分数分布来决定预算。尽管树的内容取决于预测分数，预算选择策略仍是经验调优的，在预测不确定性与可用计算变化时并无最优性保证。更有原则的策略应在每轮解码时，利用由转移分数导出的、经校准的接受收益估计，并结合反映硬件与服务负载的成本模型来选择树规模。我们把这类策略的开发与评估留作未来工作。

## 附录 E 补充相关工作

**投机解码**。除已提及的自回归（[Leviathan et al., 2023](#bib.bib8); [Chen et al., 2023](#bib.bib9)）、并行（[Chen et al., 2026](#bib.bib5); [Liu et al., 2026](#bib.bib15); [Inco AI, 2026](#bib.bib17)）、半自回归（[Huang et al., 2026](#bib.bib7); [Cheng et al., 2026](#bib.bib16)）与基于树（[Cai et al., 2024](#bib.bib10); [Miao et al., 2024](#bib.bib11); [Li et al., 2024a](#bib.bib13); [Li et al., 2026d](#bib.bib6); [Ringel and Romano, 2026](#bib.bib19); [Li et al., 2026c](#bib.bib18)）的起草方法外，已有研究还探索了投机解码的混合方法。PARD 将自回归模型适配用于并行 token 预测（[An et al., 2026](#bib.bib14)），而 DiffuSpec 使用预训练扩散语言模型作为起草器（[Li et al., 2026a](#bib.bib27)）。

**大语言模型的有损加速**。有损加速通过允许偏离目标模型的输出分布来降低推理成本。BiLD（[Kim et al., 2023](#bib.bib37)）通过基于置信度的回退与基于偏差的回滚来协调小模型与大模型。DistillSpec 的有损扩展（[Zhou et al., 2024](#bib.bib38)）用宽容因子放松 token 接受，而 Fuzzy Speculative Decoding（[Holsman et al., 2025](#bib.bib42)）依据草稿与目标分布间的散度决定接受。投机级联（speculative cascades）（[Narasimhan et al., 2025](#bib.bib39)）通过投机执行实现模型转交（deferral）规则，在草稿与目标分布之间进行选择；DIVERSED（[Wang et al., 2026b](#bib.bib43)）则学习随上下文变化的分布混合用于验证。Judge Decoding（[Bachmann et al., 2025](#bib.bib40); [Garipov et al., 2026](#bib.bib44)）用目标隐藏状态上的轻量正确性分类器接受原本会被拒绝的 token。与这些放松验证的方法不同，UBTree 在保持目标分布不变的验证的同时，通过提议器–选择器联合训练改进候选覆盖与路径质量。

**面向快速生成的多 token 语言模型**。另一条工作线将多 token 预测融入语言模型本身。[Gloeckle et al. (2024)](#bib.bib41) 在共享骨干上训练多个预测头，同时预测多个未来 token。扩散语言模型（包括 LLaDA（[Nie et al., 2026](#bib.bib1)）与 Dream（[Xie et al., 2025](#bib.bib2)））学习恢复被掩码的 token，并通过迭代式并行去噪生成文本。LLaDA 从零开始训练，而 Dream 适配预训练的自回归权重。块扩散（[Arriola et al., 2025](#bib.bib4)）把跨块的自回归生成与块内并行去噪相结合，支持灵活长度生成与前缀 KV 缓存。采用不同配方的大规模块扩散丰富了「驯服扩散以实现多 token 快速生成」的探索空间，包括 WeDLM（[Liu et al., 2025](#bib.bib3)）、Mercury（[Inception Labs et al., 2025](#bib.bib45)）与 DiffusionGemma（[DiffusionGemma Team et al., 2026](#bib.bib46)）。这些方法通过修改生成模型或其训练来实现多 token 生成，但存在样本质量退化的风险。
