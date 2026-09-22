---
title: "Qwen2 技术报告"
title_en: "Qwen2 Technical Report"
arxiv: 2407.10671
date: 2024-07-15
source: https://arxiv.org/abs/2407.10671
crawled: 2026-09-22
translated: 2026-09-22
---

# Qwen2 技术报告

> 原文：[Qwen2 Technical Report](https://arxiv.org/abs/2407.10671) · Qwen 团队 arXiv

An Yang, Baosong Yang, Binyuan Hui, Bo Zheng, Bowen Yu, Chang Zhou, Chengpeng Li, Chengyuan Li, Dayiheng Liu, Fei Huang, Guanting Dong, Haoran Wei, Huan Lin, Jialong Tang, Jialin Wang, Jian Yang, Jianhong Tu, Jianwei Zhang, Jianxin Ma, Jianxin Yang, Jin Xu, Jingren Zhou, Jinze Bai, Jinzheng He, Junyang Lin, Kai Dang, Keming Lu, Keqin Chen, Kexin Yang, Mei Li, Mingfeng Xue, Na Ni, Pei Zhang, Peng Wang, Ru Peng, Rui Men, Ruize Gao, Runji Lin, Shijie Wang, Shuai Bai, Sinan Tan, Tianhang Zhu, Tianhao Li, Tianyu Liu, Wenbin Ge, Xiaodong Deng, Xiaohuan Zhou, Xingzhang Ren, Xinyu Zhang, Xipin Wei, Xuancheng Ren, Xuejing Liu, Yang Fan, Yang Yao, Yichang Zhang, Yu Wan, Yunfei Chu, Yuqiong Liu, Zeyu Cui, Zhenru Zhang, Zhifang Guo, and Zhihao Fan

Qwen 团队

阿里巴巴集团

注：作者按名字（first name）的字母顺序排列。

###### 摘要

本报告介绍 Qwen2 系列，它是我们大语言模型与大多模态模型的最新成员。我们发布了一套完整的基础（foundational）与指令微调（instruction-tuned）语言模型，参数范围从 0.5B 到 72B，同时涵盖稠密模型与一个专家混合（MoE）模型。Qwen2 超越了包括前代 Qwen1.5 在内的大多数先前开放权重模型，并在语言理解、生成、多语言能力、编程、数学与推理等多种基准上表现出与专有模型相竞争的性能。

旗舰模型 Qwen2-72B 展现了卓越的性能：作为基础语言模型，在 MMLU 上取得 84.2，GPQA 上 37.9，HumanEval 上 64.6，GSM8K 上 89.5，BBH 上 82.4。指令微调版本 Qwen2-72B-Instruct 在 MT-Bench 上取得 9.1，Arena-Hard 上 48.1，LiveCodeBench 上 35.7。此外，Qwen2 展现了稳健的多语言能力，精通约 30 种语言，涵盖英语、中文、西班牙语、法语、德语、阿拉伯语、俄语、韩语、日语、泰语、越南语等，凸显了其多样性与全球覆盖面。

为促进社区创新与可及性，我们已在 Hugging Face（<https://huggingface.co/Qwen>）与 ModelScope（<https://modelscope.cn/organization/qwen>）上开放 Qwen2 模型权重，并在 GitHub（<https://github.com/QwenLM/Qwen2>）上提供包括示例代码在内的补充材料。这些平台还提供量化、微调与部署方面的资源，便于开展广泛的应用与研究工作。

## 1 引言

自 ChatGPT（[OpenAI, 2022](#bib.bib50)）问世以来，全球对大语言模型（LLM）的热情持续升温。Llama 系列（[Touvron et al., 2023](#bib.bib68)）的发布进一步点燃了开源社区的兴趣，尤其是对 GPT 级别本地 LLM 的关注。最近，Claude-3 Opus（[Anthropic, 2024](#bib.bib5)）与 GPT-4o (omni)（[OpenAI, 2024](#bib.bib52)）——ChatGPT 的升级模型——相继登上 Chatbot Arena（[Chiang et al., 2024](#bib.bib16)）的榜首。该平台以其对 LLM 的人工评测而广受认可。此外，Llama-3（[AI@Meta, 2024](#bib.bib2)）已成为最先进的开放权重模型系列，缩小了与领先专有模型的性能差距，并被广泛认为达到 GPT-4 水平。越来越多有竞争力的 LLM 正在追寻 OpenAI GPT 系列所取得的类似进展。其中许多模型，包括 Qwen（[Bai et al., 2023a](#bib.bib7)）、Mistral（[Jiang et al., 2023a](#bib.bib31)）、Gemma（[Mesnard et al., 2024](#bib.bib47)）等，都以开放权重形式发布。

近几个月来，我们相继推出了 Qwen 系列（[Bai et al., 2023a](#bib.bib7)）并演进到 Qwen1.5（[Qwen Team, 2024a](#bib.bib56)）。与此同时，我们发布了视觉-语言模型 Qwen-VL（[Bai et al., 2023b](#bib.bib8)），并推出了音频-语言模型 Qwen-Audio（[Chu et al., 2023](#bib.bib17)）。在本工作中，我们介绍 Qwen 大语言模型与大多模态模型家族的最新成员：Qwen2。Qwen2 是一系列基于 Transformer 架构（[Vaswani et al., 2017](#bib.bib69)）、使用下一 token 预测训练的 LLM。该模型系列既包含基础模型（即基础语言模型，经过预训练但未对齐人类偏好），也包含指令微调模型（使用适用于对话与智能体场景的单轮及多轮指令遵循数据集微调）。我们的发布包括四个稠密模型，参数量分别为 0.5B、1.5B、7B 与 72B，另有一个总参数量 57B、每 token 激活 14B 的专家混合（MoE）模型。较小的模型，即 Qwen2-0.5B 与 Qwen2-1.5B，专为智能手机、耳机、智能眼镜等便携设备上的便捷部署而设计；较大的模型则面向不同规模 GPU 上的部署。

所有模型都在高质量、大规模的数据集上预训练，该数据集包含超过 7 万亿 token，覆盖广泛的领域与语言。与此前版本的 Qwen 相比，Qwen2 纳入了更广泛的语言数据，并提升了代码与数学内容的数量与质量。我们推测这种充实能够提升 LLM 的推理能力。在后训练方面，所有模型都经过了监督微调与直接偏好优化（DPO，[Rafailov et al., 2023](#bib.bib59)），通过学习人类反馈使其与人类偏好对齐。这一过程赋予模型有效遵循指令的能力。

我们对 Qwen2 以及一组基线模型（包括开放权重模型与可通过 API 访问的专有模型）进行了全面评测。Qwen2 在基础语言能力与指令微调功能的评测中均优于竞争模型。具体而言，我们的指令微调版本 Qwen2-72B-Instruct 在 MT-Bench（[Zheng et al., 2023](#bib.bib79)）上得分 9.1，Arena-Hard（[Chiang et al., 2024](#bib.bib16)）上 48.1，LiveCodeBench（[Jain et al., 2024](#bib.bib30)）上 35.7。同时，基础语言模型 Qwen2-72B 在 MMLU（[Hendrycks et al., 2021a](#bib.bib27)）上取得 84.2，GPQA（[Rein et al., 2023](#bib.bib62)）上 37.9，HumanEval（[Chen et al., 2021](#bib.bib13)）上 64.6，GSM8K（[Cobbe et al., 2021](#bib.bib19)）上 89.5，BBH（[Suzgun et al., 2023](#bib.bib67)）上 82.4。

## 2 分词器与模型

本节介绍 Qwen2 的分词器与模型设计。我们将详述模型架构以及不同模型规模下的配置。

### 2.1 分词器

沿袭 Qwen（[Bai et al., 2023a](#bib.bib7)），我们采用相同的基于字节级字节对编码的分词器。值得注意的是，该分词器展现出很高的编码效率，其压缩率优于其他替代方案，为 Qwen2 的多语言能力提供了支撑。

所有规模的模型共用一个词表，由 151,643 个常规 token 与 3 个控制 token 组成。更多信息请参阅 [Bai et al. (2023a)](#bib.bib7)。需要说明的是，出于分布式训练的考虑，embedding 的有效规模更大。

### 2.2 模型架构

Qwen2 系列本质上是基于 Transformer 架构、采用带因果掩码的自注意力（[Vaswani et al., 2017](#bib.bib69)）的大语言模型。具体而言，该系列包含 4 个规模的稠密语言模型与一个专家混合（MoE）模型。我们先介绍稠密模型的细节，再深入探讨 MoE 模型的独特之处。

#### 2.2.1 Qwen2 稠密模型

Qwen2 稠密模型的架构由多个 Transformer 层组成，每层配备因果注意力机制与前馈神经网络（FFN）。与 Qwen 的关键差异如下：

##### 分组查询注意力

我们采用分组查询注意力（GQA，[Ainslie et al., 2023](#bib.bib3)）来取代传统的多头注意力（MHA）。GQA 优化了推理时的 KV 缓存占用，显著提升吞吐量。各模型规模的 KV 头配置详见 2.2.3 节。

##### 结合 YARN 的双块注意力

为扩展 Qwen2 的上下文窗口，我们实现了双块注意力（DCA，[An et al., 2024](#bib.bib4)），它将长序列切分为长度可控的块。如果输入可以在单个块内处理，DCA 会产生与原始注意力相同的结果；否则，DCA 能够有效捕获块内与跨块的 token 间相对位置信息，从而提升长上下文性能。此外，我们还采用 YARN（[Peng et al., 2023](#bib.bib54)）对注意力权重进行重新缩放，以获得更好的长度外推。

另外，我们沿袭 Qwen 的做法：使用 SwiGLU（[Dauphin et al., 2017](#bib.bib21)）作为激活，旋转位置编码（RoPE，[Su et al., 2024](#bib.bib66)）作为位置编码，注意力中使用 QKV 偏置（[Su, 2023](#bib.bib65)），并使用 RMSNorm（[Jiang et al., 2023b](#bib.bib33)）与预归一化以保证训练稳定。

#### 2.2.2 Qwen2 专家混合模型

Qwen2 MoE 模型的架构与 Qwen1.5-MoE-A2.7B（[Qwen Team, 2024c](#bib.bib58)）高度一致。作为对原始 FFN 的替代，MoE FFN 由 $n$ 个独立的 FFN 组成，每个 FFN 充当一个专家。每个 token 依据门控网络 $G$ 所分配的概率被路由到特定专家 $E_i$ 进行计算：

$$
\mathbf{p}=\mathrm{softmax}\left(G\left(\mathbf{x}\right)\right), \tag{1}
$$

$$
\mathbf{y}=\sum\nolimits_{i\in\text{top}_{k}\left(\mathbf{p}\right)}\mathbf{p}_{i}E_{i}(\mathbf{x}). \tag{2}
$$

下面我们介绍 Qwen2 MoE 的关键设计考量。

表 1：Qwen2 稠密与 MoE 模型的架构。对于 MoE 模型，57B-A14B 表示模型总参数量为 57B、每 token 激活 14B 参数；Intermediate size（中间层大小）指每个专家的大小；# Activated Experts（激活专家数）不含共享专家。

| 配置 | 0.5B | 1.5B | 7B | 72B | 57B-A14B |
| --- | --- | --- | --- | --- | --- |
| 隐藏层大小 | 896 | 1,536 | 3,584 | 8,192 | 3,584 |
| 层数 | 24 | 28 | 28 | 80 | 28 |
| Query 头数 | 14 | 12 | 28 | 64 | 28 |
| KV 头数 | 2 | 2 | 4 | 8 | 4 |
| 头大小 | 64 | 128 | 128 | 128 | 128 |
| 中间层大小 | 4,864 | 8,960 | 18,944 | 29,568 | 2,560 |
| 路由专家数 | - | - | - | - | 64 |
| 激活专家数 | - | - | - | - | 8 |
| 共享专家数 | - | - | - | - | 8 |
| Embedding 权重共享 | 是 | 是 | 否 | 否 | 否 |
| 词表大小 | 151,646 | 151,646 | 151,646 | 151,646 | 151,646 |
| 训练 token 数 | 12T | 7T | 7T | 7T | 4.5T |

##### 专家粒度

MoE 模型与稠密模型的关键结构差异在于 MoE 层纳入多个 FFN，每个充当独立专家。因此，从稠密架构过渡到 MoE 架构的一种直接策略，是令每个专家的参数量等于原始稠密模型中单个 FFN 的参数量。例如，从 Mistral-7B（[Jiang et al., 2023a](#bib.bib31)）过渡到 Mixtral 8x7B（[Jiang et al., 2024](#bib.bib32)），涉及每次激活八个专家中的两个。与之不同，我们的模型采用细粒度专家（[Dai et al., 2024](#bib.bib20)），构建更小规模的专家，同时激活更多数量的专家。在专家总参数量与激活参数量相同的前提下，细粒度专家提供了更丰富的专家组合方式。借助这些细粒度专家，Qwen2 MoE 促成了更多样、更动态的专家利用，从而提升整体性能与适应性。

##### 专家路由

专家路由机制的设计对于提升 MoE 模型的性能至关重要。近来，在 MoE 层中同时整合共享专家与路由专用专家已成为显著趋势（[Rajbhandari et al., 2022](#bib.bib60)；[Dai et al., 2024](#bib.bib20)）。我们采用了这一做法，因为它便于将共享专家应用于各种任务，同时将其他专家保留给特定路由场景择机使用。共享专家与专门化专家的引入，为开发 MoE 路由机制提供了一种更灵活、更高效的方法。

##### 专家初始化

我们以类似于 upcycling（[Komatsuzaki et al., 2023](#bib.bib35)）的方式，借助稠密模型的权重来初始化专家。与之不同的是，我们的方法强调细粒度专家之间的多样化，以增强模型的表征广度。给定指定的专家中间层大小 $h_{\text{E}}$、专家数量 $n$ 以及原始 FFN 中间层大小 $h_{\text{FFN}}$，FFN 会被复制 $\left\lceil n\times h_{\text{E}}/h_{\text{FFN}} \right\rceil$ 次。这一复制策略确保与指定专家数量兼容，同时可容纳任意专家中间层大小。为促进每个 FFN 副本内部的多样性，参数沿中间维度进行了随机重排。这保证每个细粒度专家都展现独特特性，即便身处不同的 FFN 副本。随后，从这些 FFN 副本中抽取专家，并丢弃多余的维度。对于每个细粒度专家，其 50% 的参数被随机重新初始化。该过程为专家初始化引入额外随机性，有可能增强模型在训练中的探索能力。

#### 2.2.3 模型配置

下面我们提供 Qwen2 系列的关键配置与信息。

Qwen2 系列由 5 种规模的模型组成，即 Qwen2-0.5B、Qwen2-1.5B、Qwen2-7B、Qwen2-57B-A14B 与 Qwen2-72B。表 1 列出了超参数与重要信息，例如预训练 token 数量。特别地，Qwen2-57B-A14B 由 Qwen2-7B 放大（upscale）而来。值得注意的是，Qwen2 模型每 token 的 Key-Value（KV）大小显著低于 Qwen1.5 模型。这一特性转化为更低的内存占用，在长上下文推理任务中尤为有利。

## 3 预训练

在 Qwen2 的预训练中，我们的工作重心放在精炼数据集以及研究有效处理更长上下文长度的方法上。

### 3.1 预训练数据

Qwen2 模型的预训练涉及构建一个新的、大规模、高质量的多语言数据集。相比此前 Qwen 与 Qwen1.5 模型所用的语料（[Bai et al., 2023a](#bib.bib7)；[Qwen Team, 2024a](#bib.bib56)），该数据集在若干关键方面提升了预训练数据的规模、质量与多样性：

##### 质量提升

过滤算法经过精炼，加入了额外的启发式与基于模型的方法，包括使用 Qwen 模型过滤低质量数据。此外，这些模型还被用于合成高质量预训练数据。

##### 数据扩充

与 Qwen1.5（[Qwen Team, 2024a](#bib.bib56)）相比，我们收集了规模显著更大的高质量代码、数学与多语言数据，增强了模型在相应领域的能力。新数据集支持约 30 种语言，如英语、中文、西班牙语、法语、德语、阿拉伯语、俄语、韩语、日语、泰语与越南语。

##### 分布改进

为确保模型学习到贴近人类学习方式的数据分布，我们在缩小规模的模型上开展实验，以优化来自不同来源与领域的数据混合。

基于这些改进，预训练数据从 Qwen1.5（[Qwen Team, 2024a](#bib.bib56)）的 3 万亿 token 扩充到 7 万亿 token。进一步放宽质量阈值的尝试得到了 12 万亿 token 的数据集，但在该数据集上训练的模型相较 7 万亿 token 模型并未显现显著的性能提升。可以怀疑，单纯增加数据量未必有益于模型预训练。考虑到训练成本，我们选择使用质量更高的 7 万亿 token 数据集来训练较大的模型，把进一步的探索留给未来的模型迭代。

除 Qwen2-0.5B 外，所有 Qwen2 稠密模型都在这个超过 7 万亿 token 的大规模数据集上预训练。Qwen2-0.5B 使用 12 万亿 token 数据集预训练。MoE 模型遵循 upcycling 原则，追加了 4.5 万亿 token 的预训练。与以往的 Qwen 模型类似，高质量多任务指令数据被纳入 Qwen2 预训练过程，以增强上下文学习与指令遵循能力。

### 3.2 长上下文训练

为增强 Qwen2 的长上下文能力，我们在预训练的收尾阶段将上下文长度从 4,096 token 扩增到 32,768 token。这一扩展伴随着大幅增加的高质量长文本数据。与此同时，我们将 RoPE 的基础频率从 10,000 改为 1,000,000，以优化长上下文场景下的表现（[Xiong et al., 2023](#bib.bib71)）。

为充分发挥模型的长度外推潜力，我们采用了 YARN 机制（[Peng et al., 2023](#bib.bib54)）与双块注意力机制（[An et al., 2024](#bib.bib4)）。这些策略使模型能够处理最长 131,072 token 的序列并保持高性能，初步实验中极小的困惑度退化即是明证。

## 4 后训练

在广泛的大规模预训练之后，我们对 Qwen2 开展后训练阶段。这一过程对于提升其在编程、数学、逻辑推理、指令遵循与多语言理解等广泛领域的熟练度至关重要。此外，它确保模型的生成与人类价值相协调，使其有用、诚实且无害。与严重依赖大量人工监督的传统方法不同，我们的方法聚焦于以最少人工标注实现可扩展的对齐（[Cao et al., 2024](#bib.bib11)）。具体而言，我们研究了为监督微调（SFT）与基于人类反馈的强化学习（RLHF）获取高质量示范数据与偏好数据的方法，旨在将人工标注的需求降到最低，同时最大化数据的质量与可靠性。

### 4.1 后训练数据

后训练数据主要由两部分组成：示范数据 $\mathcal{D}=\{(x_{i},y_{i})\}$ 与偏好数据 $\mathcal{P}=\{(x_{i},y_{i}^{+},y_{i}^{-})\}$，其中 $x_{i}$ 表示指令，$y_{i}$ 表示一个令人满意的回复，$y_{i}^{+}$ 与 $y_{i}^{-}$ 是对 $x_{i}$ 的两个回复，且 $y_{i}^{+}$ 比 $y_{i}^{-}$ 更受偏好。集合 $\mathcal{D}$ 用于 SFT，而 $\mathcal{P}$ 用于 RLHF。

训练数据的构建包含两个步骤：协同数据标注与自动化数据合成。首先，我们从大规模指令语料中抽取数据本体，得到一套广泛而多样高质量指令。这些指令被系统性地增强以纳入更高的复杂度。通过人工标注，我们获得目标回复 $y_{i}$ 及其正负对照 $(y_{i}^{+},y_{i}^{-})$。随后，采用多种自动化对齐策略，在代码、数学、指令遵循、创作、角色扮演与安全等领域合成大量人工标注式数据。

#### 4.1.1 协同数据标注

##### 自动本体抽取

该流程始于应用 InsTag（[Lu et al., 2024c](#bib.bib46)）——一个开放集细粒度标注器——从大规模指令数据集中抽取底层本体。随后经人工精修，确保抽取本体的准确性。

##### 指令筛选

对每条带标签的指令，从标签多样性、语义丰富度、复杂度与意图完整性等方面进行评估。基于这些标准，我们选出一组具有代表性的指令（[Dong et al., 2023](#bib.bib22)）。

##### 指令演化

为丰富指令数据集，我们采用自我演化策略（[Zhao et al., 2024](#bib.bib78)），提示 Qwen 模型为既有指令添加约束或要求，从而提高其复杂度，并确保数据集中难度层次的多样性。

##### 人工标注

使用多样的生成策略与不同规模的 Qwen 模型，获得同一指令的多个回复。标注者依据自身偏好对这些回复排序，确保最佳回复符合既定标准，由此同时得到示范数据与偏好数据。

#### 4.1.2 自动化数据合成

在大规模场景下，对指令回复的标注质量进行维护极具挑战，尤其是那些需要专业知识、经验、细心或耐心的任务。为应对这些挑战，我们设计了多种自动化对齐策略来规模化合成数据。

##### 拒绝采样

对于数学等具有确定性最终答案的任务，应用拒绝采样（[Yuan et al., 2023](#bib.bib75)）来提升解答质量。让大语言模型（LLM）为每条指令生成多个回复，即多条推理路径。得到正确结论且被模型认为合理的路径被保留，作为示范数据。偏好数据则通过对比正确与错误路径来生成。

##### 执行反馈

对于编程任务，让 LLM 生成解答及配套测试用例。通过编译并在测试用例上执行来评估这些解答的有效性，从而构造示范与偏好数据。该方法同样适用于评估指令遵循（[Dong et al., 2024](#bib.bib23)）。对于每条带约束（如长度限制）的指令，让 LLM 生成一个 Python 校验函数，以确保回复符合指令要求。

##### 数据再利用

对于文学写作任务，缺乏专门训练的标注者很难创作出娴熟的回复。为解决这一问题，我们从公共领域聚合高质量文学作品，并利用 LLM 编写详细程度各异的指令。这些指令与原作配对，作为示范数据。例如，为编纂带有生动、吸引人回复的角色扮演数据，我们从 Wikipedia 等知识库获取详细的人物档案，并指示 LLM 生成相应的指令与回复（[Lu et al., 2024b](#bib.bib45)）。这一过程类似阅读理解任务，确保人物档案的完整性得以维持。

##### 宪法式反馈

宪法式 AI（Constitutional AI）指依据预定义原则集合引导 LLM 生成回复的过程（[Bai et al., 2022](#bib.bib9)）。为确保对安全与价值观等准则的遵循，我们编纂了一套宪法（constitution）数据集。该数据集界定了应遵循与应规避的原则，用于指示 LLM 生成符合或偏离这些准则的回复，作为示范与偏好数据的参照。

### 4.2 监督微调

我们汇集了一个规模庞大的指令数据集，包含超过 500,000 个样本，覆盖指令遵循、编程、数学、逻辑推理、角色扮演、多语言与安全等技能。我们的模型以 32,768 token 的序列长度微调了两个 epoch。为优化学习，学习率从 $7\times 10^{-6}$ 逐步降至 $7\times 10^{-7}$。为应对过拟合，我们施加 0.1 的权重衰减，并将梯度裁剪的最大值设为 1.0。

### 4.3 基于人类反馈的强化学习

我们的 RLHF 训练方案包含先后两个阶段：离线与在线训练。在离线训练阶段，我们使用预编译的偏好数据集 $\mathcal{P}$，通过直接偏好优化（DPO，[Rafailov et al., 2023](#bib.bib59)）最大化 $y_{i}^{+}$ 与 $y_{i}^{-}$ 之间的似然差。在在线训练阶段，模型借助奖励模型的即时反馈，实时迭代改进其表现。具体而言，我们从当前策略模型采样多个回复，奖励模型选出最受与最不受偏好的回复，构成用于每轮 DPO 的偏好对。此外，我们采用 Online Merging Optimizer（[Lu et al., 2024a](#bib.bib44)）来缓解对齐税（alignment tax），即模型生成与人类偏好对齐时伴随的性能退化。

## 5 评测

为全面评估由基础模型与指令微调模型组成的 Qwen2 系列，我们实施了一套完整的评测协议。该协议考察多方面能力，包括通用知识理解、语言理解、生成、编程、数学、推理以及其他专业领域。具体而言，基础模型使用面向大语言模型（LLM）的既有基准数据集评估，除另有说明外，均通过 few-shot 提示引出回复。对于指令微调模型，除基准评测外，我们还将人工偏好评估置于优先位置。

### 5.1 基础语言模型

在本节中，我们展示 Qwen2 系列基础语言模型的评测。具体而言，我们在知识与基础能力的基准数据集上评估模型，并应用多语言基准数据集来评估其对语言的支持。由于存在多种模型规模，我们将它们与相近或更大规模的最先进（SOTA）模型进行比较。

#### 5.1.1 核心能力

表 2：70B+ 模型的性能。我们将 Qwen2-72B 与基线进行比较，包括 Mixtral-8x22B、Llama-3-70B、Qwen1.5-110B 与 Qwen1.5-72B。在大多数数据集上，Qwen2-72B 相较基线展现出优势。

| 数据集 | Mixtral-8x22B | Llama-3-70B | Qwen1.5-72B | Qwen1.5-110B | Qwen2-72B |
| --- | --- | --- | --- | --- | --- |
| 英语 | | | | | |
| MMLU | 77.8 | 79.5 | 77.5 | 80.4 | 84.2 |
| MMLU-Pro | 49.5 | 52.8 | 45.8 | 49.4 | 55.6 |
| GPQA | 34.3 | 36.3 | 36.3 | 35.9 | 37.9 |
| Theorem QA | 35.9 | 32.3 | 29.3 | 34.9 | 43.1 |
| BBH | 78.9 | 81.0 | 65.5 | 74.8 | 82.4 |
| HellaSwag | 88.7 | 88.0 | 86.0 | 87.5 | 87.6 |
| Winogrande | 85.0 | 85.3 | 83.0 | 83.5 | 85.1 |
| ARC-C | 70.7 | 68.8 | 65.9 | 69.6 | 68.9 |
| TruthfulQA | 51.0 | 45.6 | 59.6 | 49.6 | 54.8 |
| 编程 | | | | | |
| HumanEval | 46.3 | 48.2 | 46.3 | 54.3 | 64.6 |
| MBPP | 71.7 | 70.4 | 66.9 | 70.9 | 76.9 |
| EvalPlus | 54.1 | 54.8 | 52.9 | 57.7 | 65.4 |
| MultiPL-E | 46.7 | 46.3 | 41.8 | 52.7 | 59.6 |
| 数学 | | | | | |
| GSM8K | 83.7 | 83.0 | 79.5 | 85.4 | 89.5 |
| MATH | 41.7 | 42.5 | 34.1 | 49.6 | 51.1 |
| 中文 | | | | | |
| C-Eval | 54.6 | 65.2 | 84.1 | 89.1 | 91.0 |
| CMMLU | 53.4 | 67.2 | 83.5 | 88.3 | 90.1 |
| 多语言 | | | | | |
| 考试 | 63.5 | 70.0 | 66.4 | 75.6 | 76.6 |
| 理解 | 77.7 | 79.9 | 78.2 | 78.2 | 80.7 |
| 数学 | 62.9 | 67.1 | 61.7 | 64.4 | 76.0 |
| 翻译 | 23.3 | 38.0 | 35.6 | 36.2 | 37.8 |

##### 基准与评测协议

评估基础语言模型核心能力的常见做法，是使用带 few-shot 或 zero-shot 提示的基准数据集评测。评估主要聚焦于模型在自然语言理解、通用问答、编程、数学、科学知识、推理等方面的表现。评测数据集包括 MMLU（[Hendrycks et al., 2021a](#bib.bib27)）（5-shot）、MMLU-Pro（[Wang et al., 2024](#bib.bib70)）（5-shot）、GPQA（[Rein et al., 2023](#bib.bib62)）（5-shot）、Theorem QA（[Chen et al., 2023a](#bib.bib14)）（5-shot）、BBH（[Suzgun et al., 2023](#bib.bib67)）（3-shot）、HellaSwag（[Zellers et al., 2019](#bib.bib76)）（10-shot）、Winogrande（[Sakaguchi et al., 2021](#bib.bib64)）（5-shot）、TruthfulQA（[Lin et al., 2022a](#bib.bib40)）（0-shot）、ARC-C（[Clark et al., 2018](#bib.bib18)）（25-shot）、HumanEval（[Chen et al., 2021](#bib.bib13)）（0-shot）、MBPP（[Austin et al., 2021](#bib.bib6)）（0-shot）、EvalPlus（[Liu et al., 2023a](#bib.bib42)）（0-shot）、MultiPL-E（[Cassano et al., 2023](#bib.bib12)）（0-shot，语言为 Python、C++、Java、PHP、TypeScript、C#、Bash 与 JavaScript）、GSM8K（[Cobbe et al., 2021](#bib.bib19)）（5-shot）、MATH（[Hendrycks et al., 2021b](#bib.bib28)）（4-shot）、C-Eval（[Huang et al., 2023](#bib.bib29)）（5-shot）与 CMMLU（[Li et al., 2023](#bib.bib37)）（5-shot）。

多语言数据集可分为四类：(a) 考试：M3Exam（5-shot，仅选取无需图像的样本）、IndoMMLU（[Koto et al., 2023](#bib.bib36)）（3-shot）、ruMMLU（[Fenogenova et al., 2024](#bib.bib24)）（5-shot）与翻译版 MMLU（[Chen et al., 2023b](#bib.bib15)）（5-shot，语言为阿拉伯语、西班牙语、法语、葡萄牙语、德语、意大利语、日语与韩语）；(b) 理解：BELEBELE（[Bandarkar et al., 2023](#bib.bib10)）（5-shot）、XCOPA（[Ponti et al., 2020](#bib.bib55)）（5-shot）、XWinograd（[Muennighoff et al., 2023](#bib.bib48)）（5-shot）、XStoryCloze（[Lin et al., 2022b](#bib.bib41)）（0-shot）与 PAWS-X（[Yang et al., 2019](#bib.bib72)）（5-shot）；(c) 数学：MGSM（[Goyal et al., 2022](#bib.bib26)）（8-shot CoT）；(d) 翻译：Flores-101（[Goyal et al., 2022](#bib.bib26)）（5-shot）。

表 3：30B+ 稠密模型与 40B+ MoE 模型的性能。Qwen2-57B-A14B 是一个总参数量 57B、激活参数量 14B 的 MoE 模型，其设计目标是对标 30B 参数稠密模型的性能。此番比较包括稠密模型基线 Yi-1.5-34B 与 Qwen1.5-32B，以及 MoE 基线 Mixtral-8x7B 与 Jamba。结果表明 Qwen2-57B-A14B 整体表现具有竞争力，并在编程与数学任务上优势显著。

| 数据集 | Jamba | Mixtral-8x7B | Yi-1.5-34B | Qwen1.5-32B | Qwen2-57B-A14B |
| --- | --- | --- | --- | --- | --- |
| 架构 | MoE | MoE | Dense | Dense | MoE |
| 激活参数量 | 12B | 12B | 32B | 34B | 14B |
| 参数量 | 52B | 47B | 32B | 34B | 57B |
| 英语 | | | | | |
| MMLU | 67.4 | 71.8 | 77.1 | 74.3 | 76.5 |
| MMLU-Pro | - | 41.0 | 48.3 | 44.0 | 43.0 |
| GPQA | - | 29.2 | - | 30.8 | 34.3 |
| Theorem QA | - | 23.2 | - | 28.8 | 33.5 |
| BBH | 45.4 | 50.3 | 76.4 | 66.8 | 67.0 |
| HellaSwag | 87.1 | 86.5 | 85.9 | 85.0 | 85.2 |
| Winogrande | 82.5 | 81.9 | 84.9 | 81.5 | 79.5 |
| ARC-C | 64.4 | 66.0 | 65.6 | 63.6 | 64.1 |
| TruthfulQA | 46.4 | 51.1 | 53.9 | 57.4 | 57.7 |
| 编程 | | | | | |
| HumanEval | 29.3 | 37.2 | 46.3 | 43.3 | 53.0 |
| MBPP | - | 63.9 | 65.5 | 64.2 | 71.9 |
| EvalPlus | - | 46.4 | 51.9 | 50.4 | 57.2 |
| MultiPL-E | - | 39.0 | 39.5 | 38.5 | 49.8 |
| 数学 | | | | | |
| GSM8K | 59.9 | 62.5 | 82.7 | 76.8 | 80.7 |
| MATH | - | 30.8 | 41.7 | 36.1 | 43.0 |
| 中文 | | | | | |
| C-Eval | - | - | - | 83.5 | 87.7 |
| CMMLU | - | - | 84.8 | 82.3 | 88.5 |
| 多语言 | | | | | |
| 考试 | - | 56.1 | 58.3 | 61.6 | 65.5 |
| 理解 | - | 70.7 | 73.9 | 76.5 | 77.0 |
| 数学 | - | 45.0 | 49.3 | 56.1 | 62.3 |
| 翻译 | - | 29.8 | 30.0 | 33.5 | 34.5 |

##### Qwen2-72B

对于 Qwen2 中最大的模型，我们将 Qwen2-72B 与有竞争力的开源基线模型比较，包括 Mixtral-8x22B（[Jiang et al., 2024](#bib.bib32)）、Llama-3-70B（[AI@Meta, 2024](#bib.bib2)），以及 Qwen1.5-72B（[Qwen Team, 2024a](#bib.bib56)）与 Qwen1.5-110B（[Qwen Team, 2024b](#bib.bib57)）。结果报告于表 2。在通用知识理解方面，Qwen2-72B 在 MMLU 与 MMLU-Pro 上均优于 Llama-3-70B，准确率分别提升 4.7 与 2.8。在科学评估中，Qwen2-72B 在 GPQA 与 Theorem QA 上分别以 1.6 与 9.8 的优势超越 Llama-3-70B。在充实编程数据之后，Qwen2-72B 在 HumanEval 与 MBPP 评测上分别以 18.3 与 10.0 个百分点的优势领先 Qwen1.5-72B。增强的数学相关数据使 Qwen2-72B 在 GSM8K 与 MATH 基准上分别以 10.0 与 17.0 个百分点超越 Qwen1.5-72B。就 BBH、Winogrande 与 ARC-C 而言，Qwen2-72B 展现出与 Llama-3-70B 相当的推理能力，这要归功于其改进的编程与数学数据。在中文语言理解评估中，Qwen2-72B 显著优于 Mixtral-8x22B 与 Llama-3-70B，也优于 Qwen1.5-72B。

##### Qwen2-57B-A14B

对于 MoE 模型的评测，我们将 Qwen2-57B-A14B 与相近规模的基线进行比较。这些基线包括其他 MoE 模型，如 Mixtral-8x7B（[Jiang et al., 2024](#bib.bib32)）与 Jamba（[Lieber et al., 2024](#bib.bib39)），以及稠密模型，如 Yi-1.5-34B（[Young et al., 2024](#bib.bib73)）与 Qwen1.5-32B（[Qwen Team, 2024a](#bib.bib56)），两者均有约 300 亿参数。结果见表 3。我们预期激活 140 亿参数的 Qwen2-57B-A14B 能够对标 300 亿参数等效稠密 Qwen2 模型的性能。我们的评测显示，Qwen2-57B-A14B 在自然语言理解任务上与 Yi-1.5-34B 表现相当。此外，它在编程与数学任务上优于基线模型。另外，Qwen2-57B-A14B 展现了稳健的中文理解能力，可与更大的 Qwen2-72B 模型比肩。本质上，Qwen2-57B-A14B 是一个高效模型——每次前向仅激活 140 亿参数，却保持了 300 亿参数稠密模型的性能水准。

表 4：7B+ 模型的性能。我们将 Qwen2-7B 与此前发布的最先进 7B+ 模型进行比较，包括 Mistral-7B、Gemma-7B、Llama-3-8B 以及我们前代的 Qwen1.5-7B。Qwen2-7B 在大多数评测数据集上相对基线展现出显著优势。

| 数据集 | Mistral-7B | Gemma-7B | Llama-3-8B | Qwen1.5-7B | Qwen2-7B |
| --- | --- | --- | --- | --- | --- |
| 英语 | | | | | |
| MMLU | 64.2 | 64.6 | 66.6 | 61.0 | 70.3 |
| MMLU-Pro | 30.9 | 33.7 | 35.4 | 29.9 | 40.0 |
| GPQA | 24.7 | 25.7 | 25.8 | 26.7 | 31.8 |
| Theorem QA | 19.2 | 21.5 | 22.1 | 14.2 | 31.1 |
| BBH | 56.1 | 55.1 | 57.7 | 40.2 | 62.6 |
| HellaSwag | 83.2 | 82.2 | 82.1 | 78.5 | 80.7 |
| Winogrande | 78.4 | 79.0 | 77.4 | 71.3 | 77.0 |
| ARC-C | 60.0 | 61.1 | 59.3 | 54.2 | 60.6 |
| TruthfulQA | 42.2 | 44.8 | 44.0 | 51.1 | 54.2 |
| 编程 | | | | | |
| HumanEval | 29.3 | 37.2 | 33.5 | 36.0 | 51.2 |
| MBPP | 51.1 | 50.6 | 53.9 | 51.6 | 65.9 |
| Evalplus | 36.4 | 39.6 | 40.3 | 40.0 | 54.2 |
| MultiPL-E | 29.4 | 29.7 | 22.6 | 28.1 | 46.3 |
| 数学 | | | | | |
| GSM8K | 52.2 | 46.4 | 56.0 | 62.5 | 79.9 |
| MATH | 13.1 | 24.3 | 20.5 | 20.3 | 44.2 |
| 中文 | | | | | |
| C-Eval | 47.4 | 43.6 | 49.5 | 74.1 | 83.2 |
| CMMLU | - | - | 50.8 | 73.1 | 83.9 |
| 多语言 | | | | | |
| 考试 | 47.1 | 42.7 | 52.3 | 47.7 | 59.2 |
| 理解 | 63.3 | 58.3 | 68.6 | 67.6 | 72.0 |
| 数学 | 26.3 | 39.1 | 36.3 | 37.3 | 57.5 |
| 翻译 | 23.3 | 31.2 | 31.9 | 28.4 | 31.5 |

##### Qwen2-7B

7B 模型使用广泛，因为它能够在配备 16GB 显存的加速器上以 16 位浮点运行。我们的重点是将其与其他领先的 7B 模型比较，包括近期在 Chatbot Arena（[Chiang et al., 2024](#bib.bib16)）上表现卓越的 Llama-3-8B。比较对象还包括 Mistral-7B-v0.2（[Jiang et al., 2023a](#bib.bib31)）、Gemma-7B（[Mesnard et al., 2024](#bib.bib47)）以及我们的前代 Qwen1.5-7B（[Qwen Team, 2024a](#bib.bib56)）。结果见表 4。与其他模型相比，Qwen2-7B 在大多数数据集上表现出更优的性能，尤其在编程任务、数学与中文任务上出类拔萃。它在多语言理解与考试方面也表现强劲。这表明 Qwen2-7B 已在广泛的语言与逻辑类任务上得到优化，展现了其多样性与先进能力。

表 5：较小模型的性能。我们将 Qwen2-0.5B 与 Qwen2-1.5B 和此前的 SOTA 小模型进行比较，包括 Phi-2、Gemma-2B 与 Qwen1.5-1.8B。Qwen2-0.5B 以小得多的模型规模取得有竞争力的性能，而 Qwen2-1.5B 显著超越 Qwen2-0.5B。

| 数据集 | Phi-2 | Gemma-2B | Qwen1.5-1.8B | Qwen2-0.5B | Qwen2-1.5B |
| --- | --- | --- | --- | --- | --- |
| 非嵌入参数量 | 2.5B | 2.0B | 1.2B | 0.3B | 1.2B |
| MMLU | 52.7 | 42.3 | 46.8 | 45.4 | 56.5 |
| MMLU-Pro | - | 15.9 | - | 14.7 | 21.8 |
| Theorem QA | - | - | - | 8.9 | 15.0 |
| BBH | 43.4 | 35.2 | 24.2 | 28.4 | 37.2 |
| HellaSwag | 73.1 | 71.4 | 61.4 | 49.3 | 66.6 |
| Winogrande | 74.4 | 66.8 | 60.3 | 56.8 | 66.2 |
| ARC-C | 61.1 | 48.5 | 37.9 | 31.5 | 43.9 |
| TruthfulQA | 44.5 | 33.1 | 39.4 | 39.7 | 45.9 |
| HumanEval | 47.6 | 22.0 | 20.1 | 22.0 | 31.1 |
| MBPP | 55.0 | 29.2 | 18.0 | 22.0 | 37.4 |
| GSM8K | 57.2 | 17.7 | 38.4 | 36.5 | 58.5 |
| MATH | 3.5 | 11.8 | 10.1 | 10.7 | 21.7 |
| C-Eval | 23.4 | 28.0 | 59.7 | 58.2 | 70.6 |
| CMMLU | 24.2 | - | 57.8 | 55.1 | 70.3 |

##### Qwen2-1.5B 与 Qwen2-0.5B

为评估我们较小模型（具体为 Qwen2-1.5B 与 Qwen2-0.5B）的性能，我们将它们与既有基线比较：Phi-2（[Abdin et al., 2024](#bib.bib1)）、Gemma-2B（[Mesnard et al., 2024](#bib.bib47)）与 Qwen1.5-1.8B（[Qwen Team, 2024a](#bib.bib56)）。结果见表 5。在语言理解方面，Qwen2-1.5B 胜过使用教科书式数据训练的 Phi-2。在编程任务上，Qwen2-0.5B 与 Gemma-2B 及 Qwen1.5-1.8B 相当，而 Qwen2-1.5B 超越这些基线（Phi-2 除外）。两个 Qwen2 模型在数学方面均表现出优于对手的性能。在通用推理方面，我们发现 Phi-2 总体上优于其他所有模型，这在某种程度上反映了教科书数据对推理能力的重要性。在 TruthfulQA 上，Qwen2-1.5B 表现最佳，说明较小的模型未必更受幻觉困扰。在中文理解方面，两个 Qwen2 模型均优于所有其他模型，这一趋势与其各自比较中更大模型的趋势一致。

总体而言，Qwen2 系列在不同模型规模上都展现出优于基线的表现。值得注意的是，Qwen2-72B 在所有 Qwen2 模型中性能最高，凸显了模型规模放大的有效性。

### 5.2 指令微调模型

为审慎评估指令微调模型，我们实施了多方位的方法。基础技能与人类偏好的评估使用开放数据集与基准进行。我们细致的内部测评进一步探究模型在关键领域的能力。其中尤其关注长上下文能力的评估。安全措施包括多语言安全评估与红队测试。以下各节详述评估方法及其结果。

#### 5.2.1 开放基准评测

为全面评估指令微调模型的质量，我们结合自动与人工评测来评估能力与人类偏好。对于基础能力的评估，我们采用与预训练模型评测相似的数据集，聚焦自然语言理解、编程、数学与推理。具体而言，语言理解与知识方面评测 MMLU、MMLU-Pro、GPQA 与 Theorem QA；编程方面评测 HumanEval、MBPP、MultiPL-E 与 LiveCodeBench v1（[Jain et al., 2024](#bib.bib30)）；数学方面评测 GSM8K 与 MATH。此外，我们通过评测 MT-Bench（[Zheng et al., 2023](#bib.bib79)）、Arena-Hard（[Li et al., 2024](#bib.bib38)）、AlignBench（[Liu et al., 2023b](#bib.bib43)）、结果近似 Chatbot Arena 的 MixEval（[Ni et al., 2024](#bib.bib49)），以及指令遵循基准 IFEval（[Zhou et al., 2023](#bib.bib80)）来评估人类偏好对齐与指令遵循的表现；为简洁起见，我们报告其 strict-prompt 子集的结果。

表 6：70B+ 指令微调模型的性能。我们将 Qwen2-72B-Instruct 与 Mixtral-8x22B-Instruct、Llama-3-70B-Instruct、Qwen1.5-72B-Chat 及 Qwen1.5-110B-Chat 进行比较。表中省略了「-Instruct」或「-Chat」后缀。Qwen2-72B-Instruct 在核心能力上具备优势，并在人类偏好对齐上表现卓越。

| 数据集 | Mixtral-8x22B | Llama-3-70B | Qwen1.5-72B | Qwen1.5-110B | Qwen2-72B |
| --- | --- | --- | --- | --- | --- |
| 英语 | | | | | |
| MMLU | 74.0 | 82.0 | 75.6 | 76.5 | 82.3 |
| MMLU-Pro | 56.1 | 56.2 | 51.7 | 50.5 | 64.4 |
| GPQA | 49.7 | 41.9 | 39.4 | 32.8 | 42.4 |
| Theorem QA | 40.8 | 42.5 | 28.8 | 18.8 | 44.4 |
| 编程 | | | | | |
| HumanEval | 73.8 | 81.7 | 71.3 | 74.4 | 86.0 |
| MBPP | 75.9 | 82.3 | 71.9 | 76.4 | 80.2 |
| MultiPL-E | 61.1 | 63.4 | 48.1 | 55.4 | 69.2 |
| LiveCodeBench v1 | 21.8 | 29.3 | 17.9 | 25.3 | 35.7 |
| 数学 | | | | | |
| GSM8K | 89.1 | 93.0 | 82.7 | 84.5 | 93.2 |
| MATH | 47.4 | 50.4 | 42.5 | 42.0 | 69.0 |
| 对齐 | | | | | |
| MT-Bench | 8.66 | 8.95 | 8.61 | 8.88 | 9.12 |
| MixEval | 82.3 | 84.0 | 84.1 | 85.7 | 86.7 |
| Arena-Hard | 36.4 | 41.1 | 36.1 | 39.8 | 48.1 |
| IFEval strict-prompt | 67.1 | 77.3 | 55.8 | 57.5 | 77.6 |
| AlignBench | - | 7.42 | 7.28 | 7.87 | 8.27 |

##### Qwen2-72B-Instruct

我们将 Qwen2-72B-Instruct 与指令微调模型进行比较，包括 Mixtral-8x22B-Instruct、Llama-3-70B-Instruct 以及 Qwen1.5-72B-Chat。结果见表 6。可以发现，强大的基础语言模型有助于提升指令微调模型的下游表现。具体而言，Qwen2-72B-Instruct 在语言理解、编程与数学等领域胜过同侪（GPQA 与 MBPP 除外）。在人类偏好对齐与指令遵循方面，Qwen2-72B 相较基线具有显著优势。我们认为这一成就既归功于高质量的预训练模型，也归功于后训练在数据与训练技术上的改进。

表 7：30B+ 稠密与 40B+ MoE 指令微调模型的性能。我们将 Qwen2-57B-A14B-Instruct 与相近规模的 MoE 模型 Mixtral-8x7B-Instruct、30B 稠密模型如 Yi-1.5-34B-Chat 与 Qwen1.5-32B-Chat 进行比较。表中省略了「-Instruct」或「-Chat」后缀。Qwen2-57B-A14B-Instruct 与近期 SOTA 的 30B 稠密模型相比具有竞争力，并显著胜过 MoE 基线。

| 数据集 | Mixtral-8x7B | Yi-1.5-34B | Qwen1.5-32B | Qwen2-57B-A14B |
| --- | --- | --- | --- | --- |
| 架构 | MoE | Dense | Dense | MoE |
| 激活参数量 | 12B | 32B | 34B | 14B |
| 参数量 | 47B | 32B | 34B | 57B |
| 英语 | | | | |
| MMLU | 71.4 | 76.8 | 74.8 | 75.4 |
| MMLU-Pro | 43.3 | 52.3 | 46.4 | 52.8 |
| GPQA | - | - | 30.8 | 34.3 |
| Theorem QA | - | - | 30.9 | 33.1 |
| 编程 | | | | |
| HumanEval | 45.1 | 75.2 | 68.3 | 79.9 |
| MBPP | 59.5 | 74.6 | 67.9 | 70.9 |
| MultiPL-E | - | - | 50.7 | 66.4 |
| LiveCodeBench v1 | 12.3 | - | 15.2 | 25.5 |
| 数学 | | | | |
| GSM8K | 65.7 | 90.2 | 83.6 | 85.3 |
| MATH | 30.7 | 50.1 | 42.4 | 49.1 |
| 对齐 | | | | |
| MT-Bench | 8.30 | 8.50 | 8.30 | 8.55 |
| MixEval | 70.0 | 81.7 | 81.0 | 82.3 |
| IFEval strict-prompt | - | - | 50.3 | 59.9 |
| AlignBench | 5.70 | 7.20 | 7.19 | 7.36 |

##### Qwen2-57B-A14B-Instruct

对于中等规模模型，我们将 Qwen2-57B-A14B-Instruct 与另一个 MoE 基线 Mixtral-8x7B-Instruct，以及参数量超过 300 亿的稠密 SOTA 模型（如 Yi-1.5-34B-Chat 与 Qwen1.5-32B-Chat）进行比较。结果见表 7。与 Qwen1.5-32B-Chat 相比，Qwen2-57B-A14B-Instruct 在几乎所有基准上取得更优表现；与 30B SOTA 模型 Yi-1.5-34B-Chat 相比，Qwen2-57B-A14B-Instruct 在除数学外的大多数评测中取得优势。在对齐评测方面，Qwen2-57B-A14B-Instruct 的优势尤为明显。

表 8：7B+ 指令微调模型的性能。我们将 Qwen2-7B-Instruct 与近期 7-9B 参数的 SOTA 模型进行比较，包括 Llama-3-8B-Instruct、Yi-1.5-9B-Chat、GLM-4-9B-Chat 与 Qwen1.5-7B-Chat。表中省略了「-Instruct」或「-Chat」后缀。Qwen2-7B-Instruct 与 Llama-3-8B-Instruct 相比表现出有竞争力的性能。

| 数据集 | Llama-3-8B | Yi-1.5-9B | GLM-4-9B | Qwen1.5-7B | Qwen2-7B |
| --- | --- | --- | --- | --- | --- |
| 英语 | | | | | |
| MMLU | 68.4 | 69.5 | 72.4 | 59.5 | 70.5 |
| MMLU-Pro | 41.0 | - | - | 29.1 | 44.1 |
| GPQA | 34.2 | - | - | 27.8 | 34.3 |
| Theorem QA | 23.0 | - | - | 14.1 | 25.3 |
| 编程 | | | | | |
| HumanEval | 62.2 | 66.5 | 71.8 | 46.3 | 79.9 |
| MBPP | 67.9 | - | - | 48.9 | 67.2 |
| MultiPL-E | 48.5 | - | - | 27.2 | 59.1 |
| LiveCodeBench v1 | 17.3 | - | - | 6.0 | 26.6 |
| 数学 | | | | | |
| GSM8K | 79.6 | 84.8 | 79.6 | 60.3 | 85.7 |
| MATH | 30.0 | 47.7 | 50.6 | 23.2 | 52.9 |
| 对齐 | | | | | |
| MT-Bench | 8.05 | 8.20 | 8.35 | 7.60 | 8.41 |
| MixEval | 75.0 | 74.2 | - | 71.4 | 76.5 |
| IFEval strict-prompt | 72.1 | - | 69.0 | 38.3 | 54.7 |
| AlignBench | 6.20 | 6.90 | 7.01 | 6.20 | 7.21 |

##### Qwen2-7B-Instruct

在 7B 到 9B 模型的区间内，我们将 Qwen2-7B-Instruct 与 Llama-3-8B-Instruct、Yi-1.5-9B-Chat、GLM-4-9B-Chat 及 Qwen1.5-7B-Chat 进行比较。结果见表 8。与前代 Qwen1.5-7B-Chat 相比，Qwen2-7B-Instruct 在全面评测中取得长足进步，尤其在编程与数学相关任务上得分更高。与近期 SOTA 模型 Llama-3-8B-Instruct 相比，Qwen2-7B-Instruct 表现出有竞争力的性能，尤其在编程上更胜一筹。不过，在指令遵循方面，Qwen2-7B-Instruct 明显落后于对手。为解决这一局限，我们计划通过提升后训练数据质量来增强 7B 模型的指令遵循能力，确保其对复杂命令有更稳健的理解与执行。

表 9：较小指令微调模型的性能。我们将 Qwen2-0.5B-Instruct 与 Qwen2-1.5B-Instruct 分别和 Qwen1.5-0.5B-Chat 与 Qwen2-1.8B-Chat 进行比较。表中省略了「-Instruct」或「-Chat」后缀。与相近规模的基线相比，Qwen2 显著超越 Qwen1.5 的性能。

| 数据集 | Qwen1.5-0.5B | Qwen2-0.5B | Qwen1.5-1.8B | Qwen2-1.5B |
| --- | --- | --- | --- | --- |
| MMLU | 35.0 | 37.9 | 43.7 | 52.4 |
| HumanEval | 10.4 | 29.9 | 27.4 | 47.0 |
| MBPP | 14.5 | 37.8 | 28.6 | 51.9 |
| GSM8K | 11.3 | 40.1 | 35.3 | 61.6 |
| IFEval strict-prompt | 14.6 | 20.0 | 16.8 | 29.0 |

##### Qwen2-1.5B-Instruct 与 Qwen2-0.5B-Instruct

在较小模型的语境下，我们将 Qwen2-0.5B-Instruct 与 Qwen1.5-0.5B-Chat 比较，将 Qwen2-1.5B-Instruct 与 Qwen1.5-1.8B-Chat 比较。值得注意的是，某些面向较大模型设计的数据集复杂度超出了这些较小模型的能力范围，因此我们的分析聚焦于精选的子集。如表 9 所示，Qwen2 模型在核心能力与指令遵循任务上都明显优于前代。这一成就主要归功于预训练数据的规模放大。因此，我们的结果印证了数据规模放大仍是提升模型性能的有效策略，即便在十亿参数以内的模型领域亦是如此。

#### 5.2.2 内部自动评测

表 10：Qwen2-Instruct 模型在我们内部中文自动评测基准上的表现。Qwen2 模型超越相近规模 Qwen1.5 对应模型的分数以粗体标出。Qwen2-57B-A14B-Instruct 与 Qwen1.5-32B-Chat 比较。

| 模型 | 知识 | 考试 | 理解 | 编程 | 数学 | 推理 | 平均 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 专有 LLM | | | | | | | |
| GPT-4o-2024-05-13 | 66.68 | 69.04 | 76.85 | 59.58 | 71.16 | 69.94 | 68.87 |
| Qwen-Max-0428 | 76.65 | 74.80 | 73.66 | 49.48 | 66.01 | 70.84 | 68.57 |
| Qwen1.5 系列 | | | | | | | |
| Qwen1.5-0.5B-Chat | 28.55 | 36.99 | 29.70 | 3.82 | 13.10 | 25.47 | 22.94 |
| Qwen1.5-1.8B-Chat | 30.31 | 44.98 | 44.81 | 6.86 | 29.85 | 34.61 | 31.90 |
| Qwen1.5-4B-Chat | 33.67 | 47.17 | 50.44 | 14.05 | 36.20 | 39.98 | 36.92 |
| Qwen1.5-MoE-A2.7B-Chat | 52.76 | 60.49 | 52.84 | 19.34 | 38.45 | 43.07 | 44.49 |
| Qwen1.5-7B-Chat | 56.77 | 59.36 | 55.50 | 18.85 | 46.41 | 48.77 | 47.61 |
| Qwen1.5-14B-Chat | 63.35 | 66.13 | 60.06 | 28.19 | 54.80 | 50.20 | 53.79 |
| Qwen1.5-32B-Chat | 68.63 | 67.59 | 64.67 | 35.28 | 60.62 | 62.87 | 59.94 |
| Qwen1.5-72B-Chat | 71.52 | 70.04 | 66.70 | 38.22 | 63.09 | 61.30 | 61.81 |
| Qwen1.5-110B-Chat | 76.26 | 74.00 | 71.25 | 44.25 | 64.92 | 64.47 | 65.86 |
| Qwen2 系列 | | | | | | | |
| Qwen2-0.5B-Instruct | 28.18 | 38.09 | 35.90 | 9.40 | 21.20 | 25.61 | 26.40 |
| Qwen2-1.5B-Instruct | 35.46 | 51.93 | 44.70 | 14.05 | 34.58 | 35.94 | 36.11 |
| Qwen2-7B-Instruct | 61.54 | 66.66 | 59.63 | 34.74 | 60.99 | 58.22 | 56.96 |
| Qwen2-57B-A14B-Instruct | 64.15 | 73.67 | 67.52 | 40.66 | 63.90 | 59.89 | 61.63 |
| Qwen2-72B-Instruct | 76.19 | 75.65 | 74.72 | 49.53 | 70.80 | 70.59 | 69.58 |

表 11：Qwen2-Instruct 模型在我们内部英文自动评测基准上的表现。Qwen2 模型超越相近规模 Qwen1.5 与 Llama-3 对应模型的分数以粗体标出。Qwen2-57B-A14B-Instruct 与 Qwen1.5-32B-Chat 比较。

| 模型 | 知识 | 理解 | 编程 | 数学 | 平均 |
| --- | --- | --- | --- | --- | --- |
| 专有 LLM | | | | | |
| GPT-4o-2024-05-13 | 87.29 | 76.30 | 55.87 | 84.99 | 76.11 |
| Qwen-Max-0428 | 80.73 | 71.63 | 48.76 | 79.12 | 70.06 |
| Qwen1.5 系列 | | | | | |
| Qwen1.5-0.5B-Chat | 30.12 | 25.44 | 1.78 | 15.48 | 18.21 |
| Qwen1.5-1.8B-Chat | 40.37 | 41.87 | 4.99 | 29.71 | 29.23 |
| Qwen1.5-4B-Chat | 51.44 | 50.16 | 15.45 | 44.83 | 40.47 |
| Qwen1.5-MoE-A2.7B-Chat | 61.64 | 54.79 | 21.28 | 50.46 | 47.04 |
| Qwen1.5-7B-Chat | 64.86 | 58.61 | 20.79 | 54.24 | 49.62 |
| Qwen1.5-14B-Chat | 74.41 | 59.80 | 28.18 | 66.91 | 57.32 |
| Qwen1.5-32B-Chat | 76.38 | 64.70 | 37.39 | 73.04 | 62.88 |
| Qwen1.5-72B-Chat | 77.59 | 67.58 | 37.30 | 73.76 | 64.06 |
| Qwen1.5-110B-Chat | 78.29 | 70.17 | 44.12 | 78.87 | 67.86 |
| Llama-3 系列 | | | | | |
| Llama-3-8B-Instruct | 71.01 | 64.71 | 42.56 | 65.82 | 61.03 |
| Llama-3-70B-Instruct | 83.06 | 76.31 | 57.18 | 79.70 | 74.06 |
| Qwen2 系列 | | | | | |
| Qwen2-0.5B-Instruct | 43.19 | 29.57 | 6.95 | 31.52 | 27.81 |
| Qwen2-1.5B-Instruct | 56.03 | 45.08 | 17.61 | 50.44 | 42.29 |
| Qwen2-7B-Instruct | 73.75 | 63.09 | 36.41 | 75.67 | 62.23 |
| Qwen2-57B-A14B-Instruct | 76.80 | 67.92 | 42.37 | 77.04 | 66.03 |
| Qwen2-72B-Instruct | 83.00 | 73.58 | 53.03 | 82.15 | 72.94 |

尽管已有不少开放基准数据集可用于评测，我们相信这仍远不足以全面理解 LLM 的能力。为此，我们制作了一系列内部数据集，用于评估模型的不同能力，如知识理解、文本生成、编程等。评测涵盖中文与英文。结果分别汇总于表 10 与表 11。

##### 中文评测

对于中文评测，我们重点比较 Qwen2 模型与 Qwen1.5 对应模型的表现。对于小模型，Qwen2-1.5B-Instruct 即便参数更少，也在几乎所有评测中胜过 Qwen1.5-1.8B-Chat。就 7B 模型的比较而言，Qwen2 的优势更为显著。值得注意的是 Qwen2-72B 优于 Qwen1.5-110B-Chat，尽管后者参数量大得多。MoE 模型在除知识理解外的大多数领域表现优于 Qwen1.5-32B-Chat。这一差距可能归因于预训练 token 的欠缺。在不久的将来，我们将继续对该 MoE 模型进行预训练，以探究其缩放行为。

##### 英文评测

对于英文，我们将 Qwen2 与 Qwen1.5 和 Llama-3 同时比较。类似地，Qwen2 的小模型显著胜过 Qwen1.5 对应模型。然而，与 Llama-3-70B 相比，Qwen2-72B-Instruct 以微弱差距落后，尤其在理解与编程方面。我们认为，预训练英文 token 的数量以及后训练数据的数量与多样性共同导致了英文上的性能差距。

#### 5.2.3 长上下文能力

我们采用三种方法评估长上下文能力：大海捞针（Needle in a Haystack，NIAH，[Kamradt, 2023](#bib.bib34)）、NeedleBench（[OpenCompass Contributors, 2023](#bib.bib53)）与 LV-Eval（[Yuan et al., 2024](#bib.bib74)）。

##### 大海捞针

该实验考察模型在浩瀚文本中精确定位事实的能力。我们构造了长度为 8K、16K、……、128K token 的文本，并将事实策略性地置于不同深度。每个深度区间（如 0% 到 10%）包含两个实例。对于超过 32K 的上下文，评测中应用了 YARN（[Peng et al., 2023](#bib.bib54)）。如图 1 所示，Qwen2-72B-Instruct 在整个 128K 上下文中检索信息表现出卓越的准确率。结合其固有优势，在资源充足的前提下，该模型是处理长文本的最优选择。此外，同系列模型在不同上下文长度下也展现出出色表现。具体而言，Qwen2-7B-Instruct 在处理最长 128K token 的上下文时保持高准确率；Qwen2-57B-A14B-Instruct 能熟练处理最长 64K token 的上下文；而 Qwen2 系列中两个较小的模型可支持 32K token 的上下文。

![Refer to caption](2407.10671v4/needle_in_haystack.png)

图 1：Qwen2 指令微调模型在大海捞针测试中的表现。所有支持 32k token 以上上下文长度的模型均集成了 YARN 机制。

表 12：Qwen2-72B-Instruct 与 Qwen2-7B-Instruct 在 NeedleBench 和 LV-Eval 上的性能。+YARN+DCA 不改变模型在 32k token 以内的行为。

| 数据集 | NeedleBench 8k | NeedleBench 32k | NeedleBench 128k | NeedleBench 256k | LV-Eval 16k | LV-Eval 32k | LV-Eval 64k | LV-Eval 128k | LV-Eval 256k |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ChatGLM4-9B-1M | 56.61 | 49.15 | 44.30 | 45.29 | 46.40 | 43.23 | 42.92 | 40.41 | 36.95 |
| Qwen2-7B-Instruct | 87.07 | 73.64 | 38.77 | 2.92 | 49.77 | 46.93 | 28.03 | 11.01 | 0.55 |
| + YARN + DCA | | | 66.32 | 60.71 | | | 42.14 | 36.64 | 34.72 |
| Qwen2-72B-Instruct | 91.90 | 92.01 | 73.05 | 17.13 | 58.82 | 56.70 | 42.92 | 31.79 | 2.88 |
| + YARN + DCA | | | 90.27 | 85.21 | | | 53.03 | 48.83 | 42.35 |

##### NeedleBench

NeedleBench 在 NIAH 的基础上加大难度，在段落中纳入多个事实（两到五个），要求同时进行识别与多跳推理。表 12 表明，YARN 与 DCA（[An et al., 2024](#bib.bib4)）的集成显著提升了 Qwen2 模型的长上下文能力。Qwen2-7B-Instruct 超越了宣称支持 1M 上下文长度的 ChatGLM4-9B-1M（[Zeng et al., 2024](#bib.bib77)）。此外，Qwen2-72B-Instruct 表现强劲，相较 ChatGLM4-9B-1M 的准确率下降仅为 6 个百分点，而后者下降了更明显的 11 个百分点，尤其是考虑到其初始准确率本就更低。

##### LV-Eval

LV-Eval 包含 11 个多样的问答数据集，要求同时理解多条证据。为纠正其原始指标过于严苛、导致高假阴性率的问题，我们采用关键词召回率作为报告分数。如表 12 所示，集成 YARN 与 DCA 大幅增强了 Qwen2 模型在 LV-Eval 上的长上下文能力。Qwen2-7B-Instruct 与 ChatGLM4-9B-1M 相当，不过在更长上下文下降幅更明显。此外，Qwen2-72B-Instruct 在所有长度上都表现出强劲性能，印证了其处理长上下文任务的娴熟程度。

#### 5.2.4 多语言评测

对于多语言评测，我们实施了全面的人工评估来考察多语言能力。具体而言，我们设计了考察大语言模型不同能力的多样测试用例，并以多种语言准备测试用例。至于标注者，我们为每种语言邀请一位以该语言为专业的专业标注员进行评测。对于每个测试用例，标注员以 1 到 5 分为模型的回复打分。

表 13：Qwen2-72B-Instruct 与专有 LLM 在多语言人工评测中的表现。我们将 Qwen2-72B-Instruct 与 GPT-3.5-Turbo-1106、GPT-4-Turbo-0409、GPT-4o-0513、Claude-3-Opus-0229 进行比较。分数范围为 1 到 5。总体而言，Qwen2-72B-Instruct 显著优于 GPT-3.5-Turbo，但与最近 6 个月内发布的专有模型竞争仍有进步空间。

| 语言 | GPT-3.5-Turbo | GPT-4-Turbo | GPT-4o | Claude-3-Opus | Qwen2-72B-Instruct |
| --- | --- | --- | --- | --- | --- |
| 阿拉伯语 | 2.52 | 3.44 | 3.55 | 4.15 | 3.86 |
| 法语 | 3.47 | 4.19 | 4.16 | 4.23 | 4.01 |
| 印尼语 | 3.56 | 4.09 | 4.39 | 4.40 | 3.83 |
| 日语 | 2.75 | 3.68 | 3.72 | 3.85 | 3.63 |
| 韩语 | 2.37 | 4.24 | 4.40 | 4.23 | 4.14 |
| 葡萄牙语 | 3.37 | 3.86 | 3.89 | 4.09 | 3.97 |
| 俄语 | 3.24 | 4.27 | 4.32 | 4.25 | 4.15 |
| 西班牙语 | 4.07 | 4.08 | 4.26 | 4.31 | 4.10 |
| 泰语 | 3.38 | 4.11 | 4.09 | 4.01 | 3.75 |
| 越南语 | 3.90 | 3.84 | 4.14 | 3.98 | 3.91 |
| 平均 | 3.16 | 3.98 | 4.09 | 4.15 | 3.93 |

我们报告了我们的模型与基线在不同语言评测中的结果。由表 13 可以发现，平均而言 Qwen2-72B-Instruct 显著优于 GPT-3.5-Turbo，与 GPT-4-Turbo 相当，并略逊于 Claude-3-Opus。这表明我们的多语言预训练与指令微调数据为 Qwen2-72B-Instruct 的多语言能力作出了贡献，使其可与大多数最先进的专有 LLM 竞争。

#### 5.2.5 安全与责任

表 14：模型在安全评测中的表现。我们将 Qwen2-72B-Instruct 与 GPT-4 和 Mixtral-8x22B-Instruct 进行比较。数值越低越好。Qwen2-72B-Instruct 比对手拒绝了更多带风险的提示。

| 风险类别 | GPT-4 | Mixtral-8x22B | Qwen2-72B-Instruct |
| --- | --- | --- | --- |
| 违法 | 00.00 | 06.87 | 00.00 |
| 欺诈 | 03.40 | 08.49 | 02.41 |
| 色情 | 23.63 | 33.82 | 22.91 |
| 隐私 | 03.37 | 15.03 | 02.47 |

开放权重的 LLM 有效加速了研究及其应用的发展。同时，我们相信构建安全、负责任的 LLM 至关重要，如此才能显著减轻 AI 技术被滥用的效应。

我们实施了多语言安全评测，以不同语言测试 LLM。具体而言，我们评估模型在违法行为、欺诈、色情与隐私等话题上的安全表现。我们收集了易于被越狱的提示，并用它们测试模型能否通过拒绝来给出安全回应。

结果见表 14，其中展示了模型生成的有害回复比例，数值越低越好。可以观察到，Qwen2-72B-Instruct 的表现优于专有模型 GPT-4，并显著优于开放权重模型 Mixtral-8x22B-Instruct。然而，我们认为模型仍有很大改进空间才能更加安全、更负责任，尤其是在色情类别上——即便对人类而言，这也是传统上难以甄别的类别。

表 15：污染分析。本表中的污染样本采用严格标准判定：任何与预训练或后训练数据存在 13-gram 重叠的测试样本均被视为污染。我们报告污染样本的百分比，以及模型在原始与去污染测试集上的表现。

| 测试集 | 污染样本比例 | Qwen2-72B-Instruct 原始 | Qwen2-72B-Instruct 去污染 | Δ | Qwen2-7B-Instruct 原始 | Qwen2-7B-Instruct 去污染 | Δ |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MMLU | 11.2% | 82.3 | 83.2 | 0.9 | 70.5 | 71.3 | 0.8 |
| MMLU-Pro | 11.6% | 64.4 | 65.6 | 1.2 | 44.1 | 46.5 | 2.4 |
| GPQA | 1.0% | 42.4 | 41.8 | 0.6 | 34.3 | 34.1 | -0.2 |
| HumanEval | 75.0% | 86.0 | 87.0 | 1.0 | 79.9 | 87.8 | 7.9 |
| MBPP | 29.6% | 80.2 | 79.7 | 0.5 | 67.2 | 69.0 | 1.8 |
| MultiPL-E | 37.7% | 69.2 | 69.2 | 0.0 | 59.1 | 58.9 | -0.2 |
| GSM8k | 0.7% | 93.2 | 92.8 | -0.4 | 85.7 | 85.6 | -0.1 |
| Math | 31.7% | 69.0 | 74.6 | 5.6 | 52.9 | 57.6 | 4.7 |
| IFEval | 0.9% | 77.6 | 77.4 | -0.2 | 54.7 | 53.7 | -1.0 |

#### 5.2.6 污染分析

对于大语言模型而言，什么算作污染以及如何进行污染分析仍是一个活跃的研究领域（[Ravaut et al., 2024](#bib.bib61)；[Golchin & Surdeanu, 2024](#bib.bib25)；[Sainz et al., 2023](#bib.bib63)）。下面我们首先介绍我们如何尝试针对评测数据集对训练语料去污染，然后估计基准得分在多大程度上受剩余污染的影响。

在构建预训练与后训练数据集期间，我们使用 n-gram 匹配排除可能被污染的数据。然而我们发现，这种方法可能导致较高的假阴性率，因为可能存在常用表述，尤其是在数学与编程数据中。因此，我们还施加了另一条基于最长公共子序列（LCS）的约束。具体而言，我们先从测试与训练序列中移除所有符号与标点并进行分词。对于训练序列 $\mathbf{s}_{t}$，若存在测试序列 $\mathbf{s}_{e}$ 满足 $|\text{LCS}(\mathbf{s}_{t},\mathbf{s}_{e})|\geq 13$ 且 $|\text{LCS}(\mathbf{s}_{t},\mathbf{s}_{e})|\geq 0.6\times\min(|\mathbf{s}_{t}|,|\mathbf{s}_{e}|)$，则将其移除。

为评估数据泄露对测试表现的潜在影响，我们沿袭 [OpenAI (2023)](#bib.bib51) 的做法，构建了一个严格的未污染测试集，以检验严格去污染后是否存在显著的性能退化。具体而言，我们通过排除任何与预训练或后训练数据存在 13-gram 重叠的样本（不对 LCS 施加约束）来构建未污染测试集，然后在该测试集上计算相应指标。

结果见表 15。尽管某些数据集在严格标准下表现出较高的污染比例，我们注意到大多数被识别为污染的样本实为假阳性，主要来自数学与编程数据集。某些代码片段与数学公式可能如此常见，以至于它们并不能为解答测试数据提供任何有意义的优势。此外，我们的分析表明，Qwen2 模型在原始与未污染测试数据上的表现保持一致，这表明潜在的数据污染问题并未显著影响模型的性能。

## 6 结论

本技术报告介绍了 Qwen2 系列——一套参数量从 0.5B 到 72B、兼具基础与指令微调的语言模型，包含稠密与专家混合架构的模型。Qwen2 优于以往的开放权重模型，尤其是其前代 Qwen1.5，并在语言理解、生成、多语言能力、编程、数学与推理等广泛基准上表现出与专有模型相竞争的性能。在本次更新中，我们格外关注长上下文、多语言、编程、数学能力以及安全与责任。本着促进社区创新与可及性的承诺，我们开放了 Qwen2 模型权重，使研究者与开发者能够在各类应用与研究项目中充分发挥 Qwen2 的潜力。通过这些努力，我们希望为 AI 技术的进步及其对社会的积极影响贡献力量。

## 参考文献

- Abdin et al. (2024)

  Marah Abdin, Jyoti Aneja, Sebastien Bubeck, Caio César Teodoro Mendes, Weizhu Chen, Allie Del Giorno, Ronen Eldan, Sivakanth Gopi, Suriya Gunasekar, Mojan Javaheripi, Piero Kauffmann, Yin Tat Lee, Yuanzhi Li, Anh Nguyen, Gustavo de Rosa, Olli Saarikivi, Adil Salim, Shital Shah, Michael Santacroce, Harkirat Singh Behl, Adam Taumann Kalai, Xin Wang, Rachel Ward, Philipp Witte, Cyril Zhang, and Yi Zhang.
  Phi-2: The surprising power of small language models, 2024.
  URL <https://www.microsoft.com/en-us/research/blog/phi-2-the-surprising-power-of-small-language-models/>.
- AI@Meta (2024)

  AI@Meta.
  Llama 3 model card, 2024.
  URL <https://github.com/meta-llama/llama3/blob/main/MODEL_CARD.md>.
- Ainslie et al. (2023)

  Joshua Ainslie, James Lee-Thorp, Michiel de Jong, Yury Zemlyanskiy, Federico Lebrón, and Sumit Sanghai.
  GQA: Training generalized multi-query Transformer models from multi-head checkpoints.
  In *EMNLP*, pp. 4895–4901. Association for Computational Linguistics, 2023.
- An et al. (2024)

  Chenxin An, Fei Huang, Jun Zhang, Shansan Gong, Xipeng Qiu, Chang Zhou, and Lingpeng Kong.
  Training-free long-context scaling of large language models.
  *CoRR*, abs/2402.17463, 2024.
- Anthropic (2024)

  Anthropic.
  The Claude 3 model family: Opus, Sonnet, Haiku.
  Technical report, Anthropic, AI, 2024.
  URL <https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf>.
- Austin et al. (2021)

  Jacob Austin, Augustus Odena, Maxwell I. Nye, Maarten Bosma, Henryk Michalewski, David Dohan, Ellen Jiang, Carrie J. Cai, Michael Terry, Quoc V. Le, and Charles Sutton.
  Program synthesis with large language models.
  *CoRR*, abs/2108.07732, 2021.
- Bai et al. (2023a)

  Jinze Bai, Shuai Bai, Yunfei Chu, Zeyu Cui, Kai Dang, Xiaodong Deng, Yang Fan, Wenbin Ge, Yu Han, Fei Huang, Binyuan Hui, Luo Ji, Mei Li, Junyang Lin, Runji Lin, Dayiheng Liu, Gao Liu, Chengqiang Lu, Keming Lu, Jianxin Ma, Rui Men, Xingzhang Ren, Xuancheng Ren, Chuanqi Tan, Sinan Tan, Jianhong Tu, Peng Wang, Shijie Wang, Wei Wang, Shengguang Wu, Benfeng Xu, Jin Xu, An Yang, Hao Yang, Jian Yang, Shusheng Yang, Yang Yao, Bowen Yu, Hongyi Yuan, Zheng Yuan, Jianwei Zhang, Xingxuan Zhang, Yichang Zhang, Zhenru Zhang, Chang Zhou, Jingren Zhou, Xiaohuan Zhou, and Tianhang Zhu.
  Qwen technical report.
  *CoRR*, abs/2309.16609, 2023a.
- Bai et al. (2023b)

  Jinze Bai, Shuai Bai, Shusheng Yang, Shijie Wang, Sinan Tan, Peng Wang, Junyang Lin, Chang Zhou, and Jingren Zhou.
  Qwen-VL: A frontier large vision-language model with versatile abilities.
  *CoRR*, abs/2308.12966, 2023b.
- Bai et al. (2022)

  Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones, Anna Chen, Anna Goldie, Azalia Mirhoseini, Cameron McKinnon, Carol Chen, Catherine Olsson, Christopher Olah, Danny Hernandez, Dawn Drain, Deep Ganguli, Dustin Li, Eli Tran-Johnson, Ethan Perez, Jamie Kerr, Jared Mueller, Jeffrey Ladish, Joshua Landau, Kamal Ndousse, Kamile Lukosiute, Liane Lovitt, Michael Sellitto, Nelson Elhage, Nicholas Schiefer, Noemí Mercado, Nova DasSarma, Robert Lasenby, Robin Larson, Sam Ringer, Scott Johnston, Shauna Kravec, Sheer El Showk, Stanislav Fort, Tamera Lanham, Timothy Telleen-Lawton, Tom Conerly, Tom Henighan, Tristan Hume, Samuel R. Bowman, Zac Hatfield-Dodds, Ben Mann, Dario Amodei, Nicholas Joseph, Sam McCandlish, Tom Brown, and Jared Kaplan.
  Constitutional AI: Harmlessness from AI feedback.
  *CoRR*, abs/2212.08073, 2022.
- Bandarkar et al. (2023)

  Lucas Bandarkar, Davis Liang, Benjamin Muller, Mikel Artetxe, Satya Narayan Shukla, Donald Husa, Naman Goyal, Abhinandan Krishnan, Luke Zettlemoyer, and Madian Khabsa.
  The Belebele benchmark: A parallel reading comprehension dataset in 122 language variants.
  *CoRR*, abs/2308.16884, 2023.
- Cao et al. (2024)

  Boxi Cao, Keming Lu, Xinyu Lu, Jiawei Chen, Mengjie Ren, Hao Xiang, Peilin Liu, Yaojie Lu, Ben He, Xianpei Han, Le Sun, Hongyu Lin, and Bowen Yu.
  Towards scalable automated alignment of LLMs: A survey.
  *CoRR*, abs/2406.01252, 2024.
- Cassano et al. (2023)

  Federico Cassano, John Gouwar, Daniel Nguyen, Sydney Nguyen, Luna Phipps-Costin, Donald Pinckney, Ming-Ho Yee, Yangtian Zi, Carolyn Jane Anderson, Molly Q. Feldman, Arjun Guha, Michael Greenberg, and Abhinav Jangda.
  MultiPL-E: A scalable and polyglot approach to benchmarking neural code generation.
  *IEEE Trans. Software Eng.*, 49(7):3675–3691, 2023.
- Chen et al. (2021)

  Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Pondé de Oliveira Pinto, Jared Kaplan, Harrison Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Joshua Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba.
  Evaluating large language models trained on code.
  *CoRR*, abs/2107.03374, 2021.
- Chen et al. (2023a)

  Wenhu Chen, Ming Yin, Max Ku, Pan Lu, Yixin Wan, Xueguang Ma, Jianyu Xu, Xinyi Wang, and Tony Xia.
  TheoremQA: A theorem-driven question answering dataset.
  In *EMNLP*, pp. 7889–7901. Association for Computational Linguistics, 2023a.
- Chen et al. (2023b)

  Zhihong Chen, Shuo Yan, Juhao Liang, Feng Jiang, Xiangbo Wu, Fei Yu, Guiming Hardy Chen, Junying Chen, Hongbo Zhang, Li Jianquan, Wan Xiang, and Benyou Wang.
  MultilingualSIFT: Multilingual supervised instruction fine-tuning, 2023b.
  URL <https://github.com/FreedomIntelligence/MultilingualSIFT>.
- Chiang et al. (2024)

  Wei-Lin Chiang, Lianmin Zheng, Ying Sheng, Anastasios Nikolas Angelopoulos, Tianle Li, Dacheng Li, Hao Zhang, Banghua Zhu, Michael I. Jordan, Joseph E. Gonzalez, and Ion Stoica.
  Chatbot arena: An open platform for evaluating LLMs by human preference.
  *CoRR*, abs/2403.04132, 2024.
- Chu et al. (2023)

  Yunfei Chu, Jin Xu, Xiaohuan Zhou, Qian Yang, Shiliang Zhang, Zhijie Yan, Chang Zhou, and Jingren Zhou.
  Qwen-Audio: Advancing universal audio understanding via unified large-scale audio-language models.
  *CoRR*, abs/2311.07919, 2023.
- Clark et al. (2018)

  Peter Clark, Isaac Cowhey, Oren Etzioni, Tushar Khot, Ashish Sabharwal, Carissa Schoenick, and Oyvind Tafjord.
  Think you have solved question answering? Try ARC, the AI2 reasoning challenge.
  *CoRR*, abs/1803.05457, 2018.
- Cobbe et al. (2021)

  Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman.
  Training verifiers to solve math word problems.
  *CoRR*, abs/2110.14168, 2021.
- Dai et al. (2024)

  Damai Dai, Chengqi Deng, Chenggang Zhao, R. X. Xu, Huazuo Gao, Deli Chen, Jiashi Li, Wangding Zeng, Xingkai Yu, Y. Wu, Zhenda Xie, Y. K. Li, Panpan Huang, Fuli Luo, Chong Ruan, Zhifang Sui, and Wenfeng Liang.
  DeepSeekMoE: Towards ultimate expert specialization in mixture-of-experts language models.
  *CoRR*, abs/2401.06066, 2024.
- Dauphin et al. (2017)

  Yann N. Dauphin, Angela Fan, Michael Auli, and David Grangier.
  Language modeling with gated convolutional networks.
  In *ICML*, volume 70 of *Proceedings of Machine Learning Research*, pp. 933–941. PMLR, 2017.
- Dong et al. (2023)

  Guanting Dong, Hongyi Yuan, Keming Lu, Chengpeng Li, Mingfeng Xue, Dayiheng Liu, Wei Wang, Zheng Yuan, Chang Zhou, and Jingren Zhou.
  How abilities in large language models are affected by supervised fine-tuning data composition.
  *CoRR*, abs/2310.05492, 2023.
- Dong et al. (2024)

  Guanting Dong, Keming Lu, Chengpeng Li, Tingyu Xia, Bowen Yu, Chang Zhou, and Jingren Zhou.
  Self-play with execution feedback: Improving instruction-following capabilities of large language models.
  *CoRR*, abs/2406.13542, 2024.
- Fenogenova et al. (2024)

  Alena Fenogenova, Artem Chervyakov, Nikita Martynov, Anastasia Kozlova, Maria Tikhonova, Albina Akhmetgareeva, Anton A. Emelyanov, Denis Shevelev, Pavel Lebedev, Leonid Sinev, Ulyana Isaeva, Katerina Kolomeytseva, Daniil Moskovskiy, Elizaveta Goncharova, Nikita Savushkin, Polina Mikhailova, Denis Dimitrov, Alexander Panchenko, and Sergey Markov.
  MERA: A comprehensive LLM evaluation in russian.
  *CoRR*, abs/2401.04531, 2024.
- Golchin & Surdeanu (2024)

  Shahriar Golchin and Mihai Surdeanu.
  Time travel in llms: Tracing data contamination in large language models.
  In *ICLR*. OpenReview.net, 2024.
- Goyal et al. (2022)

  Naman Goyal, Cynthia Gao, Vishrav Chaudhary, Peng-Jen Chen, Guillaume Wenzek, Da Ju, Sanjana Krishnan, Marc’Aurelio Ranzato, Francisco Guzmán, and Angela Fan.
  The Flores-101 evaluation benchmark for low-resource and multilingual machine translation.
  *Trans. Assoc. Comput. Linguistics*, 10:522–538, 2022.
- Hendrycks et al. (2021a)

  Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt.
  Measuring massive multitask language understanding.
  In *ICLR*. OpenReview.net, 2021a.
- Hendrycks et al. (2021b)

  Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, and Jacob Steinhardt.
  Measuring mathematical problem solving with the MATH dataset.
  In *NeurIPS Datasets and Benchmarks*, 2021b.
- Huang et al. (2023)

  Yuzhen Huang, Yuzhuo Bai, Zhihao Zhu, Junlei Zhang, Jinghan Zhang, Tangjun Su, Junteng Liu, Chuancheng Lv, Yikai Zhang, Jiayi Lei, Yao Fu, Maosong Sun, and Junxian He.
  C-Eval: A multi-level multi-discipline chinese evaluation suite for foundation models.
  In *NeurIPS*, 2023.
- Jain et al. (2024)

  Naman Jain, King Han, Alex Gu, Wen-Ding Li, Fanjia Yan, Tianjun Zhang, Sida Wang, Armando Solar-Lezama, Koushik Sen, and Ion Stoica.
  LiveCodeBench: Holistic and contamination free evaluation of large language models for code.
  *CoRR*, abs/2403.07974, 2024.
- Jiang et al. (2023a)

  Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de Las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux, Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed.
  Mistral 7B.
  *CoRR*, abs/2310.06825, 2023a.
- Jiang et al. (2024)

  Albert Q. Jiang, Alexandre Sablayrolles, Antoine Roux, Arthur Mensch, Blanche Savary, Chris Bamford, Devendra Singh Chaplot, Diego de Las Casas, Emma Bou Hanna, Florian Bressand, Gianna Lengyel, Guillaume Bour, Guillaume Lample, Lélio Renard Lavaud, Lucile Saulnier, Marie-Anne Lachaux, Pierre Stock, Sandeep Subramanian, Sophia Yang, Szymon Antoniak, Teven Le Scao, Théophile Gervet, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed.
  Mixtral of experts.
  *CoRR*, abs/2401.04088, 2024.
- Jiang et al. (2023b)

  Zixuan Jiang, Jiaqi Gu, Hanqing Zhu, and David Z. Pan.
  Pre-RMSNorm and Pre-CRMSNorm Transformers: Equivalent and efficient pre-LN Transformers.
  *CoRR*, abs/2305.14858, 2023b.
- Kamradt (2023)

  Gregory Kamradt.
  Needle in a haystack - pressure testing LLMs, 2023.
  URL <https://github.com/gkamradt/LLMTest_NeedleInAHaystack>.
- Komatsuzaki et al. (2023)

  Aran Komatsuzaki, Joan Puigcerver, James Lee-Thorp, Carlos Riquelme Ruiz, Basil Mustafa, Joshua Ainslie, Yi Tay, Mostafa Dehghani, and Neil Houlsby.
  Sparse upcycling: Training mixture-of-experts from dense checkpoints.
  In *ICLR*. OpenReview.net, 2023.
- Koto et al. (2023)

  Fajri Koto, Nurul Aisyah, Haonan Li, and Timothy Baldwin.
  Large language models only pass primary school exams in Indonesia: A comprehensive test on IndoMMLU.
  In *EMNLP*, pp. 12359–12374. Association for Computational Linguistics, 2023.
- Li et al. (2023)

  Haonan Li, Yixuan Zhang, Fajri Koto, Yifei Yang, Hai Zhao, Yeyun Gong, Nan Duan, and Timothy Baldwin.
  CMMLU: Measuring massive multitask language understanding in Chinese.
  *CoRR*, abs/2306.09212, 2023.
- Li et al. (2024)

  Tianle Li, Wei-Lin Chiang, Evan Frick, Lisa Dunlap, Tianhao Wu, Banghua Zhu, Joseph E. Gonzalez, and Ion Stoica.
  From crowdsourced data to high-quality benchmarks: Arena-Hard and BenchBuilder pipeline.
  *CoRR*, abs/2406.11939, 2024.
- Lieber et al. (2024)

  Opher Lieber, Barak Lenz, Hofit Bata, Gal Cohen, Jhonathan Osin, Itay Dalmedigos, Erez Safahi, Shaked Meirom, Yonatan Belinkov, Shai Shalev-Shwartz, Omri Abend, Raz Alon, Tomer Asida, Amir Bergman, Roman Glozman, Michael Gokhman, Avashalom Manevich, Nir Ratner, Noam Rozen, Erez Shwartz, Mor Zusman, and Yoav Shoham.
  Jamba: A hybrid Transformer-Mamba language model.
  *CoRR*, abs/2403.19887, 2024.
- Lin et al. (2022a)

  Stephanie Lin, Jacob Hilton, and Owain Evans.
  TruthfulQA: Measuring how models mimic human falsehoods.
  In *ACL (1)*, pp. 3214–3252. Association for Computational Linguistics, 2022a.
- Lin et al. (2022b)

  Xi Victoria Lin, Todor Mihaylov, Mikel Artetxe, Tianlu Wang, Shuohui Chen, Daniel Simig, Myle Ott, Naman Goyal, Shruti Bhosale, Jingfei Du, Ramakanth Pasunuru, Sam Shleifer, Punit Singh Koura, Vishrav Chaudhary, Brian O’Horo, Jeff Wang, Luke Zettlemoyer, Zornitsa Kozareva, Mona T. Diab, Veselin Stoyanov, and Xian Li.
  Few-shot learning with multilingual generative language models.
  In *EMNLP*, pp. 9019–9052. Association for Computational Linguistics, 2022b.
- Liu et al. (2023a)

  Jiawei Liu, Chunqiu Steven Xia, Yuyao Wang, and Lingming Zhang.
  Is your code generated by ChatGPT really correct? Rigorous evaluation of large language models for code generation.
  In *NeurIPS*, 2023a.
- Liu et al. (2023b)

  Xiao Liu, Xuanyu Lei, Shengyuan Wang, Yue Huang, Zhuoer Feng, Bosi Wen, Jiale Cheng, Pei Ke, Yifan Xu, Weng Lam Tam, Xiaohan Zhang, Lichao Sun, Hongning Wang, Jing Zhang, Minlie Huang, Yuxiao Dong, and Jie Tang.
  AlignBench: Benchmarking Chinese alignment of large language models.
  *CoRR*, abs/2311.18743, 2023b.
- Lu et al. (2024a)

  Keming Lu, Bowen Yu, Fei Huang, Yang Fan, Runji Lin, and Chang Zhou.
  Online merging optimizers for boosting rewards and mitigating tax in alignment.
  *CoRR*, abs/2405.17931, 2024a.
- Lu et al. (2024b)

  Keming Lu, Bowen Yu, Chang Zhou, and Jingren Zhou.
  Large language models are superpositions of all characters: Attaining arbitrary role-play via self-alignment.
  *CoRR*, abs/2401.12474, 2024b.
- Lu et al. (2024c)

  Keming Lu, Hongyi Yuan, Zheng Yuan, Runji Lin, Junyang Lin, Chuanqi Tan, Chang Zhou, and Jingren Zhou.
  #InsTag: Instruction tagging for analyzing supervised fine-tuning of large language models.
  In *ICLR*. OpenReview.net, 2024c.
- Mesnard et al. (2024)

  Thomas Mesnard, Cassidy Hardin, Robert Dadashi, Surya Bhupatiraju, Shreya Pathak, Laurent Sifre, Morgane Rivière, Mihir Sanjay Kale, Juliette Love, Pouya Tafti, Léonard Hussenot, Pier Giuseppe Sessa, Aakanksha Chowdhery, Adam Roberts, Aditya Barua, Alex Botev, Alex Castro-Ros, Ambrose Slone, Amélie Héliou, Andrea Tacchetti, Anna Bulanova, Antonia Paterson, Beth Tsai, Bobak Shahriari, Charline Le Lan, Christopher A. Choquette-Choo, Clément Crepy, Daniel Cer, Daphne Ippolito, David Reid, Elena Buchatskaya, Eric Ni, Eric Noland, Geng Yan, George Tucker, George-Christian Muraru, Grigory Rozhdestvenskiy, Henryk Michalewski, Ian Tenney, Ivan Grishchenko, Jacob Austin, James Keeling, Jane Labanowski, Jean-Baptiste Lespiau, Jeff Stanway, Jenny Brennan, Jeremy Chen, Johan Ferret, Justin Chiu, Justin Mao-Jones, Katherine Lee, Kathy Yu, Katie Millican, Lars Lowe Sjoesund, Lisa Lee, Lucas Dixon, Machel Reid, Maciej Mikuła, Mateo Wirth, Michael Sharman, Nikolai Chinaev, Nithum Thain, Olivier Bachem, Oscar Chang,
  Oscar Wahltinez, Paige Bailey, Paul Michel, Petko Yotov, Rahma Chaabouni, Ramona Comanescu, Reena Jana, Rohan Anil, Ross McIlroy, Ruibo Liu, Ryan Mullins, Samuel L Smith, Sebastian Borgeaud, Sertan Girgin, Sholto Douglas, Shree Pandya, Siamak Shakeri, Soham De, Ted Klimenko, Tom Hennigan, Vlad Feinberg, Wojciech Stokowiec, Yu hui Chen, Zafarali Ahmed, Zhitao Gong, Tris Warkentin, Ludovic Peran, Minh Giang, Clément Farabet, Oriol Vinyals, Jeff Dean, Koray Kavukcuoglu, Demis Hassabis, Zoubin Ghahramani, Douglas Eck, Joelle Barral, Fernando Pereira, Eli Collins, Armand Joulin, Noah Fiedel, Evan Senter, Alek Andreev, and Kathleen Kenealy.
  Gemma: Open models based on Gemini research and technology.
  *CoRR*, abs/2403.08295, 2024.
- Muennighoff et al. (2023)

  Niklas Muennighoff, Thomas Wang, Lintang Sutawika, Adam Roberts, Stella Biderman, Teven Le Scao, M. Saiful Bari, Sheng Shen, Zheng Xin Yong, Hailey Schoelkopf, Xiangru Tang, Dragomir Radev, Alham Fikri Aji, Khalid Almubarak, Samuel Albanie, Zaid Alyafeai, Albert Webson, Edward Raff, and Colin Raffel.
  Crosslingual generalization through multitask finetuning.
  In *ACL (1)*, pp. 15991–16111. Association for Computational Linguistics, 2023.
- Ni et al. (2024)

  Jinjie Ni, Fuzhao Xue, Xiang Yue, Yuntian Deng, Mahir Shah, Kabir Jain, Graham Neubig, and Yang You.
  MixEval: Deriving wisdom of the crowd from LLM benchmark mixtures.
  *CoRR*, abs/2406.06565, 2024.
- OpenAI (2022)

  OpenAI.
  Introducing ChatGPT, 2022.
  URL <https://openai.com/index/chatgpt/>.
- OpenAI (2023)

  OpenAI.
  GPT4 technical report.
  *arXiv preprint arXiv:2303.08774*, 2023.
- OpenAI (2024)

  OpenAI.
  Hello GPT-4o, 2024.
  URL <https://openai.com/index/hello-gpt-4o/>.
- OpenCompass Contributors (2023)

  OpenCompass Contributors.
  OpenCompass: A universal evaluation platform for foundation models, 2023.
  URL <https://github.com/open-compass/opencompass>.
- Peng et al. (2023)

  Bowen Peng, Jeffrey Quesnelle, Honglu Fan, and Enrico Shippole.
  YaRN: Efficient context window extension of large language models.
  *CoRR*, abs/2309.00071, 2023.
- Ponti et al. (2020)

  Edoardo Maria Ponti, Goran Glavas, Olga Majewska, Qianchu Liu, Ivan Vulic, and Anna Korhonen.
  XCOPA: A multilingual dataset for causal commonsense reasoning.
  In *EMNLP (1)*, pp. 2362–2376. Association for Computational Linguistics, 2020.
- Qwen Team (2024a)

  Qwen Team.
  Introducing Qwen1.5, 2024a.
  URL <https://qwenlm.github.io/blog/qwen1.5/>.
- Qwen Team (2024b)

  Qwen Team.
  Qwen1.5-110B: The first 100B+ model of the Qwen1.5 series, 2024b.
  URL <https://qwenlm.github.io/blog/qwen1.5-110b/>.
- Qwen Team (2024c)

  Qwen Team.
  Qwen1.5-MoE: Matching 7B model performance with 1/3 activated parameters, 2024c.
  URL <https://qwenlm.github.io/blog/qwen-moe/>.
- Rafailov et al. (2023)

  Rafael Rafailov, Archit Sharma, Eric Mitchell, Christopher D. Manning, Stefano Ermon, and Chelsea Finn.
  Direct preference optimization: Your language model is secretly a reward model.
  In *NeurIPS*, 2023.
- Rajbhandari et al. (2022)

  Samyam Rajbhandari, Conglong Li, Zhewei Yao, Minjia Zhang, Reza Yazdani Aminabadi, Ammar Ahmad Awan, Jeff Rasley, and Yuxiong He.
  DeepSpeed-MoE: Advancing mixture-of-experts inference and training to power next-generation AI scale.
  In *ICML*, volume 162 of *Proceedings of Machine Learning Research*, pp. 18332–18346. PMLR, 2022.
- Ravaut et al. (2024)

  Mathieu Ravaut, Bosheng Ding, Fangkai Jiao, Hailin Chen, Xingxuan Li, Ruochen Zhao, Chengwei Qin, Caiming Xiong, and Shafiq Joty.
  How much are LLMs contaminated? A comprehensive survey and the llmsanitize library.
  *CoRR*, abs/2404.00699, 2024.
- Rein et al. (2023)

  David Rein, Betty Li Hou, Asa Cooper Stickland, Jackson Petty, Richard Yuanzhe Pang, Julien Dirani, Julian Michael, and Samuel R. Bowman.
  GPQA: A graduate-level Google-proof Q&A benchmark.
  *CoRR*, abs/2311.12022, 2023.
- Sainz et al. (2023)

  Oscar Sainz, Jon Ander Campos, Iker García-Ferrero, Julen Etxaniz, Oier Lopez de Lacalle, and Eneko Agirre.
  NLP evaluation in trouble: On the need to measure LLM data contamination for each benchmark.
  In *EMNLP (Findings)*, pp. 10776–10787. Association for Computational Linguistics, 2023.
- Sakaguchi et al. (2021)

  Keisuke Sakaguchi, Ronan Le Bras, Chandra Bhagavatula, and Yejin Choi.
  WinoGrande: An adversarial winograd schema challenge at scale.
  *Commun. ACM*, 64(9):99–106, 2021.
- Su (2023)

  Jianlin Su.
  The magical effect of the Bias term: RoPE + Bias = better length extrapolation, 2023.
  URL <https://spaces.ac.cn/archives/9577>.
- Su et al. (2024)

  Jianlin Su, Murtadha H. M. Ahmed, Yu Lu, Shengfeng Pan, Wen Bo, and Yunfeng Liu.
  Roformer: Enhanced Transformer with rotary position embedding.
  *Neurocomputing*, 568:127063, 2024.
- Suzgun et al. (2023)

  Mirac Suzgun, Nathan Scales, Nathanael Schärli, Sebastian Gehrmann, Yi Tay, Hyung Won Chung, Aakanksha Chowdhery, Quoc V. Le, Ed H. Chi, Denny Zhou, and Jason Wei.
  Challenging BIG-Bench tasks and whether chain-of-thought can solve them.
  In *ACL (Findings)*, pp. 13003–13051. Association for Computational Linguistics, 2023.
- Touvron et al. (2023)

  Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, Aurélien Rodriguez, Armand Joulin, Edouard Grave, and Guillaume Lample.
  LLaMA: Open and efficient foundation language models.
  *CoRR*, abs/2302.13971, 2023.
- Vaswani et al. (2017)

  Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia Polosukhin.
  Attention is all you need.
  In *NIPS*, pp. 5998–6008, 2017.
- Wang et al. (2024)

  Yubo Wang, Xueguang Ma, Ge Zhang, Yuansheng Ni, Abhranil Chandra, Shiguang Guo, Weiming Ren, Aaran Arulraj, Xuan He, Ziyan Jiang, Tianle Li, Max Ku, Kai Wang, Alex Zhuang, Rongqi Fan, Xiang Yue, and Wenhu Chen.
  MMLU-Pro: A more robust and challenging multi-task language understanding benchmark.
  *CoRR*, abs/2406.01574, 2024.
- Xiong et al. (2023)

  Wenhan Xiong, Jingyu Liu, Igor Molybog, Hejia Zhang, Prajjwal Bhargava, Rui Hou, Louis Martin, Rashi Rungta, Karthik Abinav Sankararaman, Barlas Oguz, Madian Khabsa, Han Fang, Yashar Mehdad, Sharan Narang, Kshitiz Malik, Angela Fan, Shruti Bhosale, Sergey Edunov, Mike Lewis, Sinong Wang, and Hao Ma.
  Effective long-context scaling of foundation models.
  *CoRR*, abs/2309.16039, 2023.
- Yang et al. (2019)

  Yinfei Yang, Yuan Zhang, Chris Tar, and Jason Baldridge.
  PAWS-X: A cross-lingual adversarial dataset for paraphrase identification.
  In *EMNLP/IJCNLP (1)*, pp. 3685–3690. Association for Computational Linguistics, 2019.
- Young et al. (2024)

  Alex Young, Bei Chen, Chao Li, Chengen Huang, Ge Zhang, Guanwei Zhang, Heng Li, Jiangcheng Zhu, Jianqun Chen, Jing Chang, Kaidong Yu, Peng Liu, Qiang Liu, Shawn Yue, Senbin Yang, Shiming Yang, Tao Yu, Wen Xie, Wenhao Huang, Xiaohui Hu, Xiaoyi Ren, Xinyao Niu, Pengcheng Nie, Yuchi Xu, Yudong Liu, Yue Wang, Yuxuan Cai, Zhenyu Gu, Zhiyuan Liu, and Zonghong Dai.
  Yi: Open foundation models by 01.AI.
  *CoRR*, abs/2403.04652, 2024.
- Yuan et al. (2024)

  Tao Yuan, Xuefei Ning, Dong Zhou, Zhijie Yang, Shiyao Li, Minghui Zhuang, Zheyue Tan, Zhuyu Yao, Dahua Lin, Boxun Li, Guohao Dai, Shengen Yan, and Yu Wang.
  LV-Eval: A balanced long-context benchmark with 5 length levels up to 256K.
  *CoRR*, abs/2402.05136, 2024.
- Yuan et al. (2023)

  Zheng Yuan, Hongyi Yuan, Chengpeng Li, Guanting Dong, Chuanqi Tan, and Chang Zhou.
  Scaling relationship on learning mathematical reasoning with large language models.
  *CoRR*, abs/2308.01825, 2023.
- Zellers et al. (2019)

  Rowan Zellers, Ari Holtzman, Yonatan Bisk, Ali Farhadi, and Yejin Choi.
  Hellaswag: Can a machine really finish your sentence?
  In *ACL (1)*, pp. 4791–4800. Association for Computational Linguistics, 2019.
- Zeng et al. (2024)

  Aohan Zeng, Bin Xu, Bowen Wang, Chenhui Zhang, Da Yin, Diego Rojas, Guanyu Feng, Hanlin Zhao, Hanyu Lai, Hao Yu, Hongning Wang, Jiadai Sun, Jiajie Zhang, Jiale Cheng, Jiayi Gui, Jie Tang, Jing Zhang, Juanzi Li, Lei Zhao, Lindong Wu, Lucen Zhong, Mingdao Liu, Minlie Huang, Peng Zhang, Qinkai Zheng, Rui Lu, Shuaiqi Duan, Shudan Zhang, Shulin Cao, Shuxun Yang, Weng Lam Tam, Wenyi Zhao, Xiao Liu, Xiao Xia, Xiaohan Zhang, Xiaotao Gu, Xin Lv, Xinghan Liu, Xinyi Liu, Xinyue Yang, Xixuan Song, Xunkai Zhang, Yifan An, Yifan Xu, Yilin Niu, Yuantao Yang, Yueyan Li, Yushi Bai, Yuxiao Dong, Zehan Qi, Zhaoyu Wang, Zhen Yang, Zhengxiao Du, Zhenyu Hou, and Zihan Wang.
  ChatGLM: A family of large language models from GLM-130B to GLM-4 all tools.
  *CoRR*, abs/2406.12793, 2024.
- Zhao et al. (2024)

  Yingxiu Zhao, Bowen Yu, Binyuan Hui, Haiyang Yu, Minghao Li, Fei Huang, Nevin L. Zhang, and Yongbin Li.
  Tree-Instruct: A preliminary study of the intrinsic relationship between complexity and alignment.
  In *LREC/COLING*, pp. 16776–16789. ELRA and ICCL, 2024.
- Zheng et al. (2023)

  Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica.
  Judging LLM-as-a-judge with MT-Bench and Chatbot Arena.
  In *NeurIPS*, 2023.
- Zhou et al. (2023)

  Jeffrey Zhou, Tianjian Lu, Swaroop Mishra, Siddhartha Brahma, Sujoy Basu, Yi Luan, Denny Zhou, and Le Hou.
  Instruction-following evaluation for large language models.
  *CoRR*, abs/2311.07911, 2023.
