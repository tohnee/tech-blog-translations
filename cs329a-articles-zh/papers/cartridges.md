---
title: "Cartridges：通过自学习实现轻量通用长上下文表示"
title_en: "Cartridges: Lightweight and general-purpose long context representations via self-study"
arxiv: 2506.06266
source: https://arxiv.org/abs/2506.06266
crawled: 2026-09-23
translated: 2026-09-23
---

# Cartridges：通过自学习实现轻量通用长上下文表示

> 原文：[Cartridges: Lightweight and general-purpose long context representations via self-study](https://arxiv.org/abs/2506.06266) · Stanford CS329A 指定阅读

Sabri Eyuboglu *（斯坦福大学，[eyuboglu@stanford.edu](mailto:eyuboglu@stanford.edu)）

Ryan Ehrlich *（斯坦福大学，[rehrlich@stanford.edu](mailto:rehrlich@stanford.edu)）

Simran Arora（斯坦福大学 / Caltech，[simarora@stanford.edu](mailto:simarora@stanford.edu)，代码：<https://github.com/HazyResearch/cartridges>）

Neel Guha（斯坦福大学）

Dylan Zinsley（纽约州立大学布法罗分校）* 贡献相同

Emily Liu（斯坦福大学）

Will Tennien（斯坦福大学）

Atri Rudra（纽约州立大学布法罗分校）* 贡献相同

James Zou（斯坦福大学）

Azalia Mirhoseini（斯坦福大学）

Christopher Ré（斯坦福大学）

###### 摘要

大型语言模型常被用来回答基于大型文本语料（如代码库、法律文件或聊天记录）的问题，其做法是将整个语料放入上下文窗口并利用上下文学习（ICL）。尽管当前模型已支持 100K–1M 词元的上下文，这种用法的服务成本高昂，因为 KV 缓存的内存消耗随输入长度而增长。我们探索另一种途径：在每个语料上离线训练一个更小的 KV 缓存。推理时，我们载入这个训练好的 KV 缓存——我们称之为 Cartridge——并解码出回答。关键在于，训练 Cartridge 的成本可以在引用同一语料的所有查询间摊销。然而我们发现，用下一词元预测目标在语料上训练 Cartridge 的朴素方法并不能与 ICL 竞争。我们转而提出 Self-Study（自学习）：一种先围绕语料生成合成对话、再用上下文蒸馏目标训练 Cartridge 的训练配方。我们发现，用自学习训练的 Cartridge 复现了 ICL 的功能，而服务成本显著更低。在具有挑战性的长上下文基准上，用自学习训练的 Cartridge 在内存占用减少 38.6×、峰值吞吐提升 26.4× 的同时匹配了 ICL 的性能。自学习还扩展了模型的有效上下文长度（例如在 MTOB 上从 128k 扩展到 484k 词元），并且令人惊讶地，得到的 Cartridge 可以在推理时直接组合而无需重新训练。

## 1 引言

大型语言模型（LLM）的用户经常把大型文本语料放进上下文窗口。例如，用户或组织可能用 LLM 来理解代码库 [63]、金融文档 [38]、法律文本 [32, 118]、教科书 [68] 或个人文件 [7]。得益于上下文学习（ICL），LLM 在这类场景中表现出色，能够对多样化的查询（如事实问答、摘要、代码生成）给出准确回答 [24]。

尽管灵活，这一使用范式的服务成本高昂。ICL 需要维护随输入长度线性增长的 KV 缓存。例如，LLaMA 70B 在 16 位精度下需要 84 GB 内存才能在 128k 词元上下文上回答单个问题 [25]。这严重限制了用户吞吐：在单块 H100 GPU 上，把上下文从 1k 增加到 120k 词元时，LLaMA 8B 的峰值吞吐（词元/秒）下降 77×（图 3）。

因此，先前工作探索了降低 KV 缓存内存占用的方法。例如，提示压缩方法通过摘要或自信息过滤减少缓存中存储的词元数 [42, 55, 21]，而 KV 缓存压缩技术则直接压缩存储的键值对 [27, 114, 84, 67]。遗憾的是，这些方法伴随着内存-质量权衡：在具有挑战性的长上下文任务实验中，我们发现当这些方法的压缩比超过 2× 时性能迅速退化（见图 4）。

受到「准备 KV 缓存的成本可以在引用同一语料的众多查询间摊销」这一观察的启发，我们探索了一种基于离线训练的互补途径。给定一个特定文本语料（如某位患者的病历），我们冻结 LLM，通过把损失反向传播到键值向量中，离线训练一个更小的 KV 缓存——这一过程本质上等价于前缀微调（prefix tuning）[54, 51]。我们把这个代表语料的训练后 KV 缓存称为「Cartridge」。推理时，我们载入训练好的 Cartridge，追加用户消息，然后解码。由于用户会反复引用相同语料（如 SEC 文件、代码库、个人文件），每个 Cartridge 可以离线训练一次并被反复复用。这一途径还能与现有推理服务器无缝集成——它们本就为管理按用户的 KV 缓存而设计 [50, 117, 45, 103]。

![Refer to caption](2506.06266v3/banner-fig.png)

图 1：
通过自学习制作 Cartridge。对给定文档语料，我们通过一个称为 Self-Study（自学习）的过程把语料蒸馏进一个参数化的 KV 缓存，以此训练一个 Cartridge。推理时，该 Cartridge 可被载入 LLM，进而用于回答关于该语料的多样化查询，在模拟对语料的上下文内分析的同时只需显著更少的内存。

要达到与 ICL 等价的功能，Cartridge 需满足两个非平凡的要求。第一，Cartridge 应当复现 ICL 的通用性，对多样化的用户提示给出准确回答 [24]。第二，Cartridge 应当复现 ICL 的结构感知力——即对文档结构进行推理、理解语料中相距遥远的部分如何相互关联或依赖的能力（这一能力在使用有损 KV 缓存压缩方法时会退化）。是否存在一个能满足这些要求同时提供内存效率的流程，并不清楚。

最自然的基线方法是在原始语料上用下一词元预测目标训练 Cartridge。令人兴奋的是，这样得到的 Cartridge 能以比 KV 缓存少 107× 的内存完美记忆语料。然而，得到的 Cartridge 并不通用——它们削弱了 LM 回答多样化问题的能力，只会复述语料（图 3）。

为了解决这些挑战、为任意文本语料产出通用且具结构感知力的 Cartridge，我们提出一种名为 Self-Study（自学习）的自动化方法。自学习有两个步骤：

1. 合成数据生成（§4.1）：我们通过提示模型对语料内容自测来生成合成训练数据，得到一条合成对话轨迹。在这些数据上训练使我们避免对完全相同的文本多次训练，并提升通用性（见图 3）。为支持超出模型有效上下文长度的语料，我们在生成合成对话时对语料分块。我们还策划了一组种子提示（seed prompt），使合成对话偏向全局推理并提升结构感知力（见图 6 右）。
2. 上下文蒸馏（§4.2）：我们用上下文蒸馏目标 [13, 79] 在合成对话上训练，使 Cartridge 增强后模型的下一词元分布与语料在上下文中的模型分布对齐。我们发现，相比下一词元预测，上下文蒸馏显著提升了 Cartridge 的质量（见图 6 中）。

总结而言，给定一个大型文本语料，我们的目标是训练一个小的虚拟 KV 缓存——称为 Cartridge——使其被模型使用时，模拟模型把整个语料放入上下文时的对话行为。为此，我们生成合成对话，并用上下文蒸馏目标在这些对话上训练 Cartridge——这一配方我们称之为自学习（Self-Study）。

**评测。** 我们在一组具有挑战性的基准上评测用自学习训练的 Cartridge，这些基准将单个大型文本语料（100k–484k 词元）与一组多样化查询配对 [38, 2, 85]。我们提出三点主张。第一，Cartridge 拓展了质量-内存前沿——在各基准上平均而言，用自学习产出的 Cartridge 在消耗 38.6× 更少内存的同时匹配 ICL 质量，并在服务许多使用不同语料的用户时实现 26.4× 的峰值吞吐（词元/秒）提升。这些内存缩减与加速相对最先进的缓存压缩基线（如 DuoAttention [95]）有一个数量级的改进。第二，Cartridge 支持上下文长度外推。在 MTOB 基准 [85] 上——模型须将 Kalamang（一种低资源语言）翻译成英语——我们用自学习配合 Llama-8B 从一本 484k 词元的教科书构建了一个小 Cartridge。该 Cartridge 在教科书前 130,000 词元上比 ICL 高出 11.0 chrF 分，并在教科书的一个精选子集上匹配 ICL 性能。第三，自学习产出的 Cartridge 无需联合优化即可组合：多个 Cartridge 可以拼接在一起被共同查询，模拟 ICL 灵活回答针对上下文中拼接的多个文档的查询的能力（见图 7）。

此外，我们仔细消融了自学习与 Cartridge 中的设计决策（§5.3 与附录 A）。值得注意的是，我们将参数化为 KV 缓存的 Cartridge [54] 与参数化为 LoRA [36] 的 Cartridge 进行比较，发现 KV 缓存参数化在域内与域外任务上都表现更好。

在本工作中，我们展示了离线 KV 缓存训练如何显著降低在「用户反复把相同文本语料放入上下文」场景下服务语言模型的成本。我们希望这些成本降低能够催生当前不可行的新应用，例如拥有整仓上下文的编程智能体或聊天机器人中的长期记忆。

## 2 预备知识

| 方法 | 消耗有限内存 | 保留语料信息 | 支持多样提示 |
| --- | --- | --- | --- |
| 上下文学习（ICL） | ✗ | ✓ | ✓ |
| 提示 / KV 缓存压缩 | ✓ | ✗ | ✓ |
| Cartridge + 下一词元预测 | ✓ | ✓ | ✗ |
| Cartridge + 自学习（Self-Study） | ✓ | ✓ | ✓ |

图 2：比较各种 KV 缓存策略。Cartridge 提升了内存效率，同时在广泛提示上保留了上下文学习的质量。✓ 表示优势，✗ 表示局限。

我们首先讨论相关工作（§2.1），形式化我们的问题（§2.2），并给出语言模型与 KV 缓存的背景（§2.3）。

### 2.1 相关工作

先前工作的详细讨论见附录 B。

##### 参数高效微调与知识注入

为了让语言模型适配特定任务或领域，从业者通常训练少量参数来增强或修改原模型 [36, 54, 51, 61, 107]。其中，低秩适配（LoRA）[36]——用低秩更新适配线性层——是事实上的参数高效微调技术。在本工作中，我们基于一种不那么流行的技术：前缀微调（prefix-tuning）[54, 51]，即对输入之前的一组「虚拟」词元优化其内部激活。

近期的知识注入工作应用 LoRA（或其变体 [60]）把文本语料存储进少量参数 [113, 93, 48, 60, 81]。这使模型能以参数化知识而非 ICL 来回答查询。这条工作线上最早的方法用语料上的下一词元预测目标注入知识 [113, 93, 49]。令人兴奋的是，近期与同期工作也展示了合成数据 [60, 81] 与上下文蒸馏目标 [48, 15] 在知识注入中的威力。与我们的工作不同，这些论文不关注知识注入带来的内存缩减或吞吐提升。此外，它们不使用前缀微调参数化，不把合成数据生成形式化为对话，也不使用多样化的种子提示来启动对话——我们发现这些对长上下文任务的性能与域外泛化至关重要。

与我们对 Cartridge 组合的分析相关的，是若干通过各类聚合操作组合多个不同参数高效适配器的工作 [116, 37, 94, 115, 97, 92, 30, 53]。

##### 提示与 KV 缓存压缩

由于 KV 缓存的大小是语言模型服务成本的主要决定因素，许多工作提出了缩减缓存大小的技术。一类方法着眼于让提示更小——显式方法通过摘要与过滤改变提示文本 [42, 55, 21, 109, 70]，隐式方法把提示表示压缩为一组「软」词元 [19, 104, 28, 62, 72, 51]。另一类方法利用对 KV 缓存结构的观察 [105, 16, 46]，通常发现由于少量键主导了后续查询的注意力分数，无影响力的键值对（或词元）可以被丢弃 [27, 114, 84, 67, 56] 或合并 [91, 112, 90]。与我们的工作相比，这些方法压缩 KV 缓存所用的计算量相对较少。我们关注的是这样一个场景：由于上下文被众多请求共享，扩大压缩 KV 缓存所用的计算量是合理的。

##### 架构改动

大量工作研究了针对原始多头注意力操作 [89] 的架构改动，目标是缩减 KV 缓存的内存占用或用恒定大小的内存对象替代它。与自学习及上述压缩方法不同——后两者可直接应用于任何预训练 Transformer——这些架构改动通常需要从头重训模型或使用复杂的架构转换技术 [108]。

为了缩减 KV 缓存的内存占用，这些架构利用稀疏性 [12, 20, 106, 86]、减少键值头数量 [78, 3]、把键值头低秩化 [57]，或用恒定大小的内存对象替代 KV 缓存 [111, 6, 31, 102, 99]。其中，分组查询注意力（grouped-query attention）[3] 是事实上的多头注意力变体，被 Llama 3 [25] 等前沿语言模型采用。我们的实验中与采用分组查询注意力的 ICL 进行了比较。其他变体——如多头潜在注意力（multi-head latent attention）[57] 或线性注意力 [6, 31]——正在流行，出现在大规模推理模型 [33] 与混合模型 [52, 14, 87] 中。

与我们工作最相关的是近期的一些架构（如 Titans [11]、TTT [82]），它们使用恒定大小的内存对象（如线性注意力中那样）但施加类梯度下降的内存更新 [82, 101, 9, 11, 10]。与我们的工作一样，这些架构的动机是「梯度下降在把文本压缩进恒定空间方面非常有效」这一观察，并展示了在测试时对长上下文任务使用梯度下降的前景。与我们的工作不同，这些架构需要从头训练，尚未在大规模模型上得到验证，且在召回密集型任务上无法匹配注意力的质量 [6, 9]。

图 3：
用自学习训练的 Cartridge 在通用性与内存消耗之间取得平衡。
我们在 GenConvo 数据集上比较四种方法：用语料 $\mathcal{C}$ 上的下一词元预测训练的 Cartridge、用自学习训练的 Cartridge、完整 ICL，以及截断 ICL（一种把 $\mathcal{C}$ 截断为前 $k$ 个词元的提示压缩方法）。
（左）我们在 GenConvo 数据集的不同切片上评测。用下一词元预测训练的 Cartridge 在与其训练分布相似的 memorization（记忆）类查询上表现良好，但无法像其他方法那样泛化到其他查询。
（中）$x$ 轴度量不同方法的 KV 缓存大小（GB）。
$y$ 轴显示 GenConvo 数据集上按查询类型平均的对数困惑度。
（右）在 1 块 H100 上用 SGLang [117] 测得 Llama-3B 与 Llama-8B 在不同缓存大小下的峰值吞吐（词元/秒）（见附录 A）。

### 2.2 问题设定

我们假设这样一个场景：用户针对一个公共文本语料发出一连串多样化查询。我们把语料记为 $\mathcal{C}$，查询集记为 $Q=\{q_{1},q_{2},\ldots,q_{m}\}$。$\mathcal{C}$ 的示例包括法律文件、金融文档、代码仓库、聊天记录与病历。

示例：金融分析

$\mathcal{C}$ 可以是 AMD 的 2022 年 Form 10-K 文件 [88]，约 100k 词元。分析师可能要求 LLM 就这份文件回答的查询是多样的，包括：(1) 回忆事实信息，(2) 对数值做数学推理，或 (3) 甚至基于 10-K 的信息生成创意回答（如一首诗）。

令 $R=\{r_{1},r_{2},\ldots,r_{m}\}$ 表示 LLM 针对这些查询产生的回答。我们有两个目标。第一，希望在某质量指标（如准确率）下最大化回答 $R$ 的质量。第二，希望在模型回答与该文档相关问题期间最小化 LLM 的内存占用。这是因为更大的内存占用会降低吞吐，并需要更多硬件来服务同样数量的用户（图 3，右）。

### 2.3 语言模型与 KV 缓存

回顾一下，LLM $\mathcal{F}$ 接受 $N$ 个词元的序列 $\mathbf{x}\in\mathcal{V}^{n}$ 作为输入，这些词元取自离散词表 $\mathcal{V}\subset\mathbb{Z}$，每个词元由唯一整数表示。输出 $\mathcal{F}(\cdot|\mathbf{x})$ 对应于在给定前缀 $\mathbf{x}\in\mathcal{V}^{n}$ 条件下对词表 $\mathcal{V}$ 的一个分类分布。

在语言模型内部，$\mathbf{x}$ 中的每个词元 $x[i]$ 被嵌入到 $d$ 维空间，得到矩阵 $\mathbf{u}\in\mathbb{R}^{n\times d}$。矩阵 $\mathbf{u}$ 经过 $L$ 层模型层，每层沿 $n$ 与 $d$ 维度混合该矩阵，第 $\ell$ 层输出 $\mathbf{y}^{l}\in\mathbb{R}^{n\times d}$。最终的 $\mathbf{y}^{L}$ 通过线性投影映射为 $\mathcal{V}$ 上的 logits。

大多数现代语言模型使用基于自注意力 [89] 的 Transformer 架构。给定序列长度 $n$、嵌入维度 $d$ 的输入 $\mathbf{u}\in\mathbb{R}^{n\times d}$，它通过投影 $\mathbf{q},\mathbf{k},\mathbf{v}=\mathbf{u}\mathbf{W}_{q},\mathbf{u}\mathbf{W}_{k},\mathbf{u}\mathbf{W}_{v}$ 上的 softmax 计算输出 $\mathbf{y}^{l}\in\mathbb{R}^{n\times d}$：

$$
\mathbf{y}[i]=\sum_{j=1}^{i}\frac{\exp(\mathbf{q}[i]^{\top}\mathbf{k}[j]/\sqrt{d})\mathbf{v}[j]}{\sum_{t=1}^{i}\exp(\mathbf{q}[i]^{\top}\mathbf{k}[t]/\sqrt{d})} \tag{1}
$$

其中每层的权重矩阵 ${\bm{W}}_{q}$、${\bm{W}}_{k}$ 与 ${\bm{W}}_{v}$ 在训练中学习。

从 $\mathcal{F}$ 生成时，我们每次从 $\mathcal{F}(\cdot\mid\mathbf{x})$ 采样一个词元并将其追加到 $\mathbf{x}$。关键在于，注意力算子是因果的：每个输出 $\mathbf{y}[i]$ 都以先前的词元为条件。这使我们不必为先前词元重算键和值，而是把它们存进一个随 $i$ 增长的 KV 缓存 $\{\mathbf{k}[j],\mathbf{v}[j]\}_{j=1}^{i}$。于是，生成分两个阶段：(1) 预填充（prefill），为初始提示 $\mathbf{x}$ 计算 KV 缓存；(2) 解码（decode），逐词元生成回答并追加到 KV 缓存。预填充之后，若 $\mathbf{x}$ 主要由语料 $\mathcal{C}$ 构成，则 KV 缓存实际上充当了语料 $\mathcal{C}$ 的一种表示。这就是把长语料 $\mathcal{C}$ 放进上下文 $\mathbf{x}$ 会产生巨大内存占用的原因：KV 缓存的大小随 $\mathbf{x}$ 的长度线性增长。

## 3 Cartridge 范式

本节描述 Cartridge 范式：我们通过训练离线生成语料 $\mathcal{C}$ 的表示，而非用预填充即时构建的标准做法。

### 3.1 形式化 Cartridge

我们的目标是为给定语料 $\mathcal{C}$ 训练一个 Cartridge。Cartridge 是一小组参数 $Z\in\mathbb{R}^{*}$（即适配器 [54, 36]），它增强 LLM $\mathcal{F}$，使其表现得如同上下文窗口中放有 $\mathcal{C}$。形式化地，令 $\mathcal{F}_{Z}(\cdot|q)$ 表示以 $Z$ 增强后的 $\mathcal{F}$ 在给定查询 $q$ 时的分布。对所有 $q\in Q$，我们希望确保按某个查询特定的评分函数，采样 $r_{Z}\sim\mathcal{F}_{Z}(\cdot|q)$ 与 ICL 采样 $r_{q}\sim\mathcal{F}(\cdot|\mathcal{C}\oplus q)$ 一样好或更好。为使 $\mathcal{F}_{Z}(\cdot|q)$ 匹配或超越 $\mathcal{F}(\cdot|\mathcal{C}\oplus q)$ 的行为，应满足三个重要标准。

- 展现通用性：由于 $Q$ 可能横跨多样的问题类型（如数学推理、事实召回理解、摘要等），$\mathcal{F}_{Z}$ 必须能在不同的 $q\in Q$ 之间泛化。这并不平凡，因为在离线学习 $Z$ 时 $Q$ 是未知的。若 $\mathcal{F}_{Z}$ 不能泛化，从业者可能需要为不同的查询分布学习不同的 $Z$，这会增加 Cartridge 的成本。理想情况下，$Z$ 只需学习一次即可服务多种类型的查询。
- 捕捉长程依赖：$Z$ 还应捕捉 $\mathcal{C}$ 内部的长程依赖。在许多场景下，正确回答不同的 $q\in Q$ 需要推理 $\mathcal{C}$ 中信息的呈现顺序。如何在 $Z$ 中捕捉这些依赖并不清楚。
- 可组合：理想情况下，$Z$ 的表示与 $\mathcal{F}$ 使用它的机制应允许组合，而无需对 Cartridge 做任何特定的联合训练。给定对应 $\mathcal{C}_{1}$ 与 $\mathcal{C}_{2}$ 的 $Z_{1}$ 与 $Z_{2}$，理想情况是 $\mathcal{F}_{[Z_{1},Z_{2}]}(q)$ 与 $\mathcal{F}(\cdot|\mathcal{C}_{1}\oplus\mathcal{C}_{2}\oplus q)$ 相似。

### 3.2 参数化 Cartridge

我们用简化版的前缀微调 [54] 参数化 $Z$。具体而言，我们分配一个由可训练键值向量 $\mathbf{z}_{\text{k}},\mathbf{z}_{\text{v}}\in\mathbb{R}^{p\times d}$ 组成的 KV 缓存。完整 $Z\in\mathbb{R}^{L\times p\times d\times 2}$ 的大小由超参数 $p$ 控制。$Z$ 的内存占用等价于一个 $p$ 词元提示的 KV 缓存。

在 ICL 中，$\mathcal{F}_{\mathcal{C}}(q)$（设 $\mathcal{C}$ 长度为 $n_{\mathcal{C}}$、$Q$ 长度为 $n_{Q}$）的 KV 缓存包含 $n_{\mathcal{C}}+n_{Q}$ 个键值对，前 $n_{\mathcal{C}}$ 个对应 $\mathcal{C}$，后 $n_{Q}$ 个对应 $Q$：

$$
\text{ICL KV 缓存}\quad \underbrace{(\mathbf{k}[1],\mathbf{v}[1]),\dots,(\mathbf{k}[{n_{\mathcal{C}}}],\mathbf{v}[{n_{\mathcal{C}}}])}_{\mathcal{C}\text{ 的 KV 对}},\underbrace{(\mathbf{k}[{n_{\mathcal{C}}+1}],\mathbf{v}[{n_{\mathcal{C}}+1}])\dots}_{q\text{ 的 KV 对}}
$$

$$
\text{Cartridge KV 缓存}\quad \underbrace{(\mathbf{z}_{\text{k}}[1],\mathbf{z}_{\text{v}}[1]),\dots,(\mathbf{z}_{\text{k}}[p],\mathbf{z}_{\text{v}}[p])}_{Z\text{ 中可训练的 KV 对}},\underbrace{(\mathbf{k}[{1}],\mathbf{v}[{1}])\dots}_{q\text{ 的 KV 对}}
$$

训练 Cartridge 时，我们把对应 $\mathcal{C}$ 的键值对替换为 $Z$，并通过把损失反向传播进键值向量直接优化它们。关键在于，我们冻结模型全部参数，只训练 $Z$ 中的键值向量。损失的选择在 §4.2 讨论。

##### 初始化

先前工作发现，优化随机初始化的缓存 $Z$ 不稳定且导致性能退化 [54]。这些工作转而用较小维度 $d$ 初始化可训练缓存，再用 MLP 重投影回原维度。相比之下，我们发现对 $Z$ 的恰当初始化使我们无需重参数化即可直接优化完整缓存。具体而言，我们把 $Z$ 初始化为语料 $\mathcal{C}$ 前 $p$ 个词元对应的 KV 缓存。另一种做法是使用语料摘要，或用现成的提示压缩策略过滤词元 [95]。在 §5.3 中，我们展示我们的初始化相比随机初始化带来更稳定的训练与更快的收敛。

**为什么选这种参数化？** 我们注意到，参数高效微调文献提供了用一组额外参数增强 LLM 的其他方式，尤其是低秩适配（LoRA）[54, 36, 51]。在 §5.3 中，我们对前缀微调参数化与 LoRA 参数化的 Cartridge 做了全面比较。

### 3.3 服务 Cartridge

只需对现有 LLM 推理服务器 [117, 50, 45] 做极小改动，即可高效服务 Cartridge。由于 Cartridge 本身就是一个 KV 缓存，它可以直接用现有的缓存前缀处理机制载入 KV 缓存槽位。LLM 推理服务器为管理多用户的各异 KV 缓存做了深度优化 [103]，这意味着用现有推理服务器即可高吞吐地服务 Cartridge。用 Cartridge 解码词元与服务一个长度为 $p$（Cartridge 中可训练词元数的超参数）的前缀请求完全相同。这与 LoRA 等其他方法形成对比——后者需要定制基础设施才能高效服务多用户 [18]。前缀长度与吞吐的关系见图 3。

## 4 Self-Study：一种训练 Cartridge 的自监督方法

本节描述 Self-Study（自学习）——一种在任何文本语料上训练 Cartridge $Z$ 的简单方法。自学习的设计动机来自实验：用更简单配方训练的 Cartridge 无法泛化到多样化的用户查询。

图 4：
Cartridges 以更低内存成本匹配 ICL 质量。
我们针对不同方法、不同 KV 缓存大小，度量 Llama-3B 的回答质量（$y$ 轴）与 KV 缓存内存（$x$ 轴）的关系。虚线标出标准 ICL 的质量。

##### 动机性观察

构建 Cartridge 的朴素方法是在语料文本上直接用下一词元预测目标微调 $Z$ 的参数。我们在图 3 中展示用该方法实验的结果，评测基于一个衍生自 FinanceBench [38] 的数据集，我们称之为 GenConvo（细节见附录 D）。GenConvo 包含多种类型的问题（如综合、推理）。我们发现，朴素下一词元预测方法能以近乎完美的困惑度记忆语料（图 3 左），同时消耗比 ICL 少 107× 的内存（图 3 中）。然而，如图 3 所示，对其他切片的泛化很差。我们寻求一种训练目标，使使用 Cartridge 的模型产生的回答能泛化到多样化的用户查询，就像 ICL 那样。

在这些观察的激励下，我们在 §4.1 描述一个合成数据生成配方，在 §4.2 描述一个上下文蒸馏目标。如图 3 所示，用该方法训练的 Cartridge 能对多种类型的查询生成质量匹配 ICL 的回答。Cartridge 方法的可视化见图 1。

### 4.1 用自监督合成数据避免过拟合

为了训练通用的 Cartridge，我们提议用 LLM 生成的合成数据来构建训练数据集 $\mathcal{D}_{\text{train}}$。

##### 总体合成数据管线

我们的总体管线把语料 $\mathcal{C}$ 的信息放入上下文，并提示模型与自身就该语料展开对话，以生成合成问答对，如算法 1 所示。我们用 $x\oplus y$ 表示两个向量的拼接。

**算法 1　Self-Study：数据生成**

输入：$\mathcal{C}$：语料；$\mathcal{F}$：模型

输出：$\{\mathbf{a}_{1},\mathbf{b}_{1},\dots,\mathbf{a}_{k},\mathbf{b}_{k}\}$：对话

1: $\tilde{\mathbf{c}}\leftarrow$ chunk$(\mathcal{C})$　⊳ (1) 取 $\mathcal{C}$ 的一个能放进上下文窗口的子语料

2: $\mathbf{s}\leftarrow$ get_seed_prompt()　⊳ (2) 取一个为 $A$ 的首条消息设定种子的提示

3: **for** $i=1$ **to** $k$ **do**　⊳ (3) 采样一段含 $k$ 个来回的对话

4: 　　$\mathbf{a}_{i}\sim\mathcal{F}(\cdot\mid\tilde{\mathbf{c}}\oplus\mathbf{s}\oplus\mathbf{a}_{1}\oplus\dots\oplus\mathbf{b}_{i-1})$　⊳ (3.1) 在上下文含 $\tilde{\mathbf{c}}$ 与 $\mathbf{s}$ 时采样 $A$ 的消息

5: 　　$\mathbf{b}_{i}\sim\mathcal{F}(\cdot\mid\tilde{\mathbf{c}}\oplus\mathbf{a}_{1}\oplus\dots\oplus\mathbf{b}_{i-1}\oplus\mathbf{a}_{i})$　⊳ (3.2) 在上下文含 $\tilde{\mathbf{c}}$ 时采样 $B$ 的消息

6: **end for**

7: **return** $\{\mathbf{a}_{1},\mathbf{b}_{1},\dots,\mathbf{a}_{k},\mathbf{b}_{k}\}$

对话通过迭代地从两个 LLM 参与者 $A$ 与 $B$（即同一个模型）采样生成而产生。我们维护两份不同的对话历史：$A$ 的历史以一条含种子提示 $s$ 的用户消息开头（例如 "Please start a conversation by asking a question about the document above."），随后是来自 $A$ 与 $B$ 的助手与用户消息交替；$B$ 的对话历史不含种子提示，包含与 $A$ 相同的消息但 $A$、$B$ 角色互换。两者的系统提示中都含有子语料 $\tilde{\mathbf{c}}$。为构建训练集，我们采样 $m_{\text{train}}$ 条独立对话，并把 $A$ 与 $B$ 的消息拼接成单个词元序列：

$$
\mathcal{D}_{\text{train}}=\{\mathbf{x}^{(j)}=\mathbf{a}_{1}^{(j)}\oplus\mathbf{b}_{1}^{(j)}\oplus\mathbf{a}_{2}^{(j)}\oplus\mathbf{b}_{2}^{(j)}\oplus\dots\oplus\mathbf{a}_{k}^{(j)}\oplus\mathbf{b}_{k}^{(j)}\}_{j=1}^{m_{\text{train}}} \tag{2}
$$

其中每个 $\mathbf{x}^{(j)}$ 是各消息的拼接。注意，我们在正文中评测的所有数据集都是单轮的。因此我们设 $k=1$，生成一条含一条用户消息与一条助手消息的合成对话。

注意，chunk 与 get_seed_prompt 这两个函数提供了控制合成数据分布的两种不同方式。我们发现这两个设计决策对用自学习训练高质量 Cartridge 至关重要。

##### 分块

我们使用较短的子语料 $\tilde{c}$（512 到 4096 词元之间），让 LLM 在生成数据时聚焦语料的不同部分。这受先前工作的观察启发 [59, 64]。此外，分块还使我们能在超出模型上下文窗口的语料上训练 Cartridge。

##### 种子提示

我们不止使用一条种子提示，而是策划了五种不同类型的种子提示：结构化（structuring）、摘要（summarization）、提问（question）、使用场景（use cases）与创意（creative）。实验所用种子提示的完整列表见附录 C。关键在于，我们所有实验中的种子提示都是通用的：它们不提及与我们评测语料相关的任何 specifics（例如不为 MTOB 提及翻译、不为 LongHealth 提及医学术语）。我们在所有主结果中使用同一组种子提示。在 §5.3 中，我们消融了多样种子提示的使用，发现相比单一通用种子提示，它带来高达 4.8 个准确率点的提升（LongHealth 上 43.6→48.4）。

### 4.2 自学习的上下文蒸馏目标

给定微调数据集 $\mathcal{D}_{\text{train}}$，我们借鉴模型蒸馏文献的标准技术 [47, 79, 48]。令 $\mathcal{F}(\cdot|\mathbf{x})$ 表示给定输入文本 $\mathbf{x}$ 时的下一词元分布。我们的教师是把子语料 $\tilde{\mathbf{c}}$ 放入上下文的模型 $\mathcal{F}(\cdot|\tilde{\mathbf{c}})$，学生是用可训练缓存适配的同一模型 $\mathcal{F}_{Z}(\cdot)$。我们使用经典蒸馏目标 [35]，在词元序列 $\mathbf{x}$ 与生成它们所用的子语料 $\tilde{\mathbf{c}}$ 上最小化教师与学生下一词元分布之间的 KL 散度：

$$
\underset{Z}{\arg\min}\quad\sum_{(\mathbf{x},\tilde{\mathbf{c}})\in\mathcal{D}_{\text{train}}}\sum_{i=1}^{|\mathbf{x}|}D_{\text{KL}}\bigg(\mathcal{F}(\cdot|\tilde{\mathbf{c}}\oplus\mathbf{x}[:i])\quad||\quad\mathcal{F}_{Z}(\cdot|\mathbf{x}[:i])\bigg) \tag{3}
$$

在附录 A 中，我们消融了上下文蒸馏目标的使用，并在控制合成数据量的前提下展示它带来准确率提升（例如 LongHealth 上 3.7 个准确率点）。

## 5 结果

图 5：扩展自学习的计算量。这些图展示了用自学习扩展训练计算时质量如何提升。所有图中，$x$ 轴为总全局训练步数（批大小 64，最大序列长度 1024）。不重复使用合成生成的数据（即训练只跑一个 epoch）。曲线对应不同大小的 Cartridge（$p\in\{128,512,2048,8192\}$）。（左）$y$ 轴为 Llama-8B 在 LongHealth [2] 上的准确率。（中）$y$ 轴为 Llama-3B 在 MTOB [85] 上的 chrF。（右）$y$ 轴为 Llama-3B 在 QASPER [23] 上的对数困惑度（越低越好）。

我们描述在各种长上下文场景下评测用自学习训练的 Cartridge 之有效性的实验。我们的结果支持以下主张。第一，用自学习训练的 Cartridge 能在保持通用性、降低服务成本的同时匹配或超越 ICL（§5.1）。第二，自学习在超出 LLM 上下文窗口的语料上仍然有效（§5.2）。第三，当我们把两个不同的 Cartridge 不经任何联合训练直接拼接时，模型能回答需要两个 Cartridge 信息的查询（§5.4）。最后，我们给出消融实验以评估自学习与 Cartridge 各方面的相对收益（§5.3）。

##### 数据集

我们研究由关于单份长文档的多样化 $(q,r)$ 对组成的数据集。各数据集的 $\mathcal{C}$ 介于 100k 到 484k 词元。我们的数据集取自流行的长上下文基准，其中一些按原样使用，另一些做了修改以符合这一结构。这些包括：LongHealth [2]、MTOB [85] 与 QASPER [23]。我们用准确率（LongHealth）、对数困惑度（QASPER）与字符 n-gram f 分数（chrF，MTOB）[85, 71] 评估 LLM 回答质量。由于每个数据集实际上只由「单份」文档构成，我们为每个数据集训练一个 Cartridge，并在查询-回答对 $(q,r)$ 上评测。更多细节见附录 D。

### 5.1 推进质量/成本权衡前沿

我们评估用自学习产出的 Cartridge 在 LongHealth 与 QASPER（Llama-3B）上相对各基线的质量与内存表现。两个数据集的 $\mathcal{C}$ 都放得进模型上下文窗口（128k 词元）。我们与传统 ICL、两个提示压缩基线（提示截断与用 GPT-4o 做提示摘要 [66]）以及一个最先进的 KV 缓存压缩基线（DuoAttention [43, 95]）比较。内存用量以 KV 缓存大小衡量：ICL 模型与提示压缩方法的 KV 缓存大小、Cartridge 的大小，以及 DuoAttention 等 KV 缓存压缩方法压缩后的 KV 缓存大小。

图 4 给出我们的主要结果。在 LongHealth 与 QASPER 上，我们都找到了 Cartridge 胜过 ICL 的缓存大小。与 ICL 相比，Cartridge 在相近性能下提供可观内存节省：LongHealth 上最高 10×，QASPER 上最高 100×。相比之下，压缩基线方法在低至 2× 的压缩因子下就出现性能退化。关键的是，Cartridge 的小内存占用带来了高得多的峰值吞吐（词元/秒）。如图 3（右）所示，性能匹配 ICL 的缓存大小可带来近 26× 的吞吐提升。

图 6：
消融 Cartridge 与自学习的设计选择。
消融在 MTOB 数据集上进行（完整消融实验见附录 A）。
（左）我们用两种不同参数化训练 Cartridge：简化版前缀微调（如 §3.2 所述）与低秩适配（LoRA）[36]。$x$ 轴为 MMLU 准确率，$y$ 轴为目标数据集准确率。每个点代表一个不同的 Cartridge 大小。
（中）我们用自学习配合两种损失函数训练 Cartridge：下一词元预测损失（绿色）与蒸馏损失（蓝色）。$x$ 轴为训练步数，$y$ 轴为准确率。每种色相代表一个不同的 Cartridge 大小。
（右）我们按算法 1 生成合成数据，并消融第 2 行采样的种子提示选择。我们考虑两种做法：使用单一宽泛种子提示（绿色），或从五种不同类型中随机采样一种（蓝色）。$x$ 轴为训练步数，$y$ 轴为准确率。

我们还观察到，随着增加自学习使用的计算量，Cartridge 性能相应扩展：Cartridge 训练越久，任务性能越高。图 5 绘出了不同大小 Cartridge 的性能随训练步数变化的曲线。在所有大小上，我们都观察到性能与计算量之间稳定的正相关。

### 5.2 扩展有效上下文窗口

我们评估自学习是否使我们能准确处理超出上下文窗口长度的语料。为此，我们考虑 MTOB 数据集与上下文窗口为 128k 词元的 Llama-8B。MTOB 提供两份不同的长文档：一份完整的 484k 词元 LaTeX 教科书，以及一份较短的 60k 词元版本（由数据集作者人工筛选、剔除了与翻译任务无关的内容）。尽管 484k 教科书比 Llama-8B 的上下文窗口长 356k 词元，我们可以用自学习的分块策略为完整教科书产出 Cartridge。

图 4（中图）展示了用自学习训练的各种大小 Cartridge 的性能。作为对比，我们给出各 KV 缓存基线方法在较小 60k 词元教科书上的结果，并附上长教科书截断版上的 ICL。与上文一样，我们观察到 Cartridge 能在人工筛选的 60k 词元版本上匹配 ICL 的性能，同时所需内存显著更少，且只能访问超出 Llama-8B 上下文窗口的 484k 词元版本。在每个 KV 缓存大小上，Cartridge 也胜过有竞争力的基线，最高领先 11.0 chrF 分。

### 5.3 消融自学习的设计选择

我们进行消融以研究自学习与 Cartridge 参数化的不同方面。完整结果见附录 A，关键发现在此处与图 6 中强调。

##### Cartridge 参数化

在 §3.2 中，我们讨论了如何用可训练 KV 缓存参数化 Cartridge——这等价于简化版前缀微调 [54]。还有许多其他参数化 Cartridge 的方式，尤其是极其流行的参数高效微调方法低秩适配（LoRA）[36]。

我们比较前缀微调参数化与 LoRA（完整结果见 §A.1）。首先，我们发现在与语料相关的查询上，前缀微调参数化比内存对齐的 LoRA 参数化更有效。例如，在 MTOB 上用约 0.6 GB 的 Cartridge 时，前缀微调比 LoRA 高 4.5 个 chrF 分。（LongHealth 与 QASPER 的结果见图 8。）更有意思的是两种参数化在与文档无关的查询（如 MMLU [34]）上的差距。使用 LoRA 参数化时，我们发现随着 Cartridge 大小从 0.15 GB 增至 1.06 GB，MMLU 准确率急剧下降（从 54.7 降到 45.3）。相比之下，前缀微调的准确率随大小（从 0.15 GB 到 0.96 GB）下降要慢得多（从 54.7 降到 54.3）。这些发现在 LongHealth、QASPER 与 MTOB 上的图示见图 8。我们还展示冻结注意力汇（attention sink，键值向量中的第一个词元）能提升训练稳定性（图 10）。

##### Cartridge 初始化

在使用前缀微调参数化时，我们比较三种初始化 KV 缓存的策略：(1) 随机向量（逐分量标准正态分布）；(2) 随机词元的键值向量；(3) 语料前 $p$ 个词元的键值向量。我们发现用真实词元的键值向量初始化（而非随机向量）对达到 ICL 级性能至关重要。在 LongHealth 上，随机向量达到 29.9% 的准确率，而随机词元的键值向量达到 51.3%。用前 $p$ 个词元初始化再带来 4 个百分点的提升，达到 55.3%。在原始前缀微调论文中，作者展示了在极小数据集上做监督微调时，从词元初始化能提升性能 [54]。我们的结果把这一发现扩展到自学习——我们在大型合成数据集上训练。

##### 自学习的种子提示

接下来，我们消融种子提示的选择（见算法 1 第 2 行）。我们比较两种做法：(1) 始终使用同一条种子提示（"Please generate a single chat message to begin a conversation about the information in the corpus. Ask a question about the corpus or make a request."）；(2) 从五种不同类型（如结构化、摘要；完整列表见附录 C）中随机采样一条。注意即使后者，种子提示也是通用的：所有语料使用同一组种子提示。在 MTOB 上，我们发现使用这小组种子提示比单一种子提示提升 7.9 个 chrF 分（24.1→32.0；见图 6 左）。在 LongHealth 上，提升为 4.8 个准确率点（43.6→48.4；见图 11）。有趣的是，在 QASPER 上我们没有看到使用多种种子提示的显著收益。这可能是因为相比 LongHealth 与 MTOB，QASPER 的查询对推理要求较低。

##### 自学习目标

最后，我们评估上下文蒸馏目标（定义见 §4.2）的重要性。在两个目标使用相同自学习合成数据的前提下，我们比较上下文蒸馏目标与更简单的下一词元预测目标。在 MTOB 上，我们发现对合成对话数据使用上下文蒸馏目标使 chrF 提升 8.6 分（24.9→33.5；见图 12 中）。我们在 LongHealth 与 QASPER 上也看到提升（见图 12）。

### 5.4 组合 Cartridge

![Refer to caption](2506.06266v3/x1.png)

图 7：
Cartridge 组合。
（左）Cartridge 组合的示意：两个独立训练的 Cartridge（一个对应 Pepsi 10-K，一个对应 AMD 10-K）不经任何额外训练直接拼接。
（中）我们在一个多文档问题数据集上用 Llama-3B 评测组合，这些问题需要两份约 100k 词元文档中的信息（见附录 D）。$x$ 轴为金标准答案上的对数困惑度（越低越好）。我们把 Cartridge 组合与两个基线比较：(a) ICL 基线，把文档截断以放进 128k 词元上下文；(b) Cartridge 基线，只放入其中一份文档的 Cartridge。
（右）用组合 Cartridge 回答多文档问题的示例。

我们评估独立训练的 Cartridge 能否被组合起来，以服务针对两个不同语料的查询（见图 7，左）。我们在 AMD、Pepsi、AMEX 与 Boeing 的长 10-K 文档 [38] 上训练大小为 $\{512,1024,2048,4096\}$ 的 Cartridge。对每一对 Cartridge（每个缓存大小 6 对），我们用一个多文档问题数据集评测，即需要两份 10-K 信息的问题。令人惊讶的是，我们发现组合不仅让 LLM 无需任何重训练即可开箱即用地产生连贯的生成（图 7，右），而且在多文档问题上大幅胜过只使用单个 Cartridge（如只用 AMD）或 ICL（后者受限于上下文长度限制）（图 7，中）。

## 6 讨论与结论

我们提出 Cartridge 作为 ICL 的替代方案，适用于许多不同用户消息引用同一大型文本语料的场景。我们在多样化的语言模型工作负载上展示：经自学习训练后，Cartridge 在大幅降低内存消耗（我们的评测中平均 38.6× 内存缩减）并提升峰值吞吐（26.4× 更高词元/秒）的同时，匹配 ICL 的回答质量。Cartridge 易于训练、可组合，并与现有 LLM 服务基础设施兼容。

不过，与 ICL 相比，自学习并非没有局限。用自学习产出 KV 缓存比直接运行标准 ICL 预填充昂贵得多。用我们未优化的实现，训练一个 ICL 质量的 Cartridge 在单台 8×H100 节点上约需 30 分钟（Llama-8B）。因此，我们的工作并非 ICL 的即插即用替代品，而是展示了在构建 KV 缓存时以更多计算换取更少内存的一种权衡方式。这一权衡在许多场景中极为有利：用户常常对同一语料发出许多查询，而自学习可以在空闲或未充分利用的计算资源上离线训练（例如在夜间用户负载低时 [39, 29]）。此外，还有很大的优化空间（如改进的共享前缀注意力核 [22, 103, 44]）可以让自学习训练流程更高效。

展望未来，我们设想 Cartridge 能催生一大类今天用 ICL 无法实现的上下文感知 AI 应用——从了解患者完整病史的医疗助理，到理解整个代码库的 LLM 驱动 IDE。

##### 致谢

我们感谢 Jordan Juravsky、Dan Biderman、Tri Dao、Bradley Brown、Mayee Chen、Avanika Narayan、Avner May、Bill Mark、Benjamin Spector、Roberto Garcia、Quinn Mcintyre、Yasa Baig、Geoff Angus、Kelly Buchanan、Mert Yuksekgonul、Eric Nguyen、Eric Wu、Kevin Wu、Owen Dugan、Jon Saad-Falcon、Simon Guo 以及 Zou、Hazy 与 Scaling Intelligence 全体实验室的有益讨论与反馈。我们衷心感谢 Modal、Prime Intellect、Voltage Park 与 Together AI 为本工作提供 GPU 支持。我们衷心感谢以下资助：NIH No. U54EB020405 (Mobilize)；NSF Nos. CCF2247015 (Hardware-Aware)、CCF1763315 (Beyond Sparsity)、CCF1563078 (Volume to Velocity) 与 1937301 (RTML)；US DEVCOM ARL Nos. W911NF-23-2-0184 (Long-context) 与 W911NF-21-2-0251 (Interactive Human-AI Teaming)；ONR No. N000142312633 (Deep Signal Processing)；Stanford HAI No. 247183；NXP、Xilinx、LETI-CEA、Intel、IBM、Microsoft、NEC、Toshiba、TSMC、ARM、Hitachi、BASF、Accenture、Ericsson、Qualcomm、Analog Devices、Google Cloud、Salesforce、Total、HAI-GCP Cloud Credits for Research 计划、Stanford Data Science Initiative (SDSI)、Stanford SEAMS 项目成员：IBM 与 Felicis，以及 Stanford DAWN 项目成员：Meta、Google 与 VMWare。SE 受 NSF 研究生奖学金资助。AR 的研究受 NSF 基金 CCF#2247014 资助。美国政府被授权为政府目的复制和分发重印本，不受其上任何版权标注的限制。本材料中表达的观点、发现、结论或建议均为作者个人观点，不一定反映 NIH、ONR 或美国政府的观点、政策或背书——无论明示或暗示。

##### 贡献

SE 与 RE 构思了 Cartridges 与 Self-Study。SE、RE 与 SA 设计了方法、实现了实验、撰写了稿件，并对项目做出同等贡献。NG 对项目结构与最终稿件做出重要贡献。EL 与 DZ 实现并运行了实验，并对稿件做出有意义的贡献。WT 实现了 LoRA 基线。DZ 与 AR 主导了理论分析。AR、JZ、AM 与 CR 指导了本项目。

## 参考文献

- [1]

  Marah Abdin, Jyoti Aneja, Harkirat Behl, Sébastien Bubeck, Ronen Eldan, Suriya Gunasekar, Michael Harrison, Russell J Hewett, Mojan Javaheripi, Piero Kauffmann, et al.
  Phi-4 technical report.
  arXiv preprint arXiv:2412.08905, 2024.
- [2]

  Lisa Adams, Felix Busch, Tianyu Han, Jean-Baptiste Excoffier, Matthieu Ortala, Alexander Löser, Hugo JWL Aerts, Jakob Nikolas Kather, Daniel Truhn, and Keno Bressem.
  Longhealth: A question answering benchmark with long clinical documents.
  arXiv preprint arXiv:2401.14490, 2024.
- [3]

  Joshua Ainslie, James Lee-Thorp, Michiel De Jong, Yury Zemlyanskiy, Federico Lebrón, and Sumit Sanghai.
  Gqa: Training generalized multi-query transformer models from multi-head checkpoints.
  arXiv preprint arXiv:2305.13245, 2023.
- [4]

  Anthropic.
  The Claude 3 Model Family: Opus, Sonnet, Haiku.
  arXiv preprint, 2024.
- [5]

  Simran Arora, Sabri Eyuboglu, Aman Timalsina, Isys Johnson, Michael Poli, James Zou, Atri Rudra, and Christopher Ré.
  Zoology: Measuring and improving recall in efficient language models, 2023.
- [6]

  Simran Arora, Sabri Eyuboglu, Michael Zhang, Aman Timalsina, Silas Alberti, Dylan Zinsley, James Zou, Atri Rudra, and Christopher Ré.
  Simple linear attention language models balance the recall-throughput tradeoff.
  arXiv preprint arXiv:2402.18668, 2024.
- [7]

  Simran Arora and Christopher Ré.
  Can foundation models help us achieve perfect secrecy?
  arXiv preprint arXiv:2205.13722, 2022.
- [8]

  Maximilian Beck, Korbinian Pöppel, Markus Spanring, Andreas Auer, Oleksandra Prudnikova, Michael Kopp, Günter Klambauer, Johannes Brandstetter, and Sepp Hochreiter.
  xlstm: Extended long short-term memory.
  arXiv preprint arXiv:2405.04517, 2024.
- [9]

  Ali Behrouz, Zeman Li, Praneeth Kacham, Majid Daliri, Yuan Deng, Peilin Zhong, Meisam Razaviyayn, and Vahab Mirrokni.
  Atlas: Learning to optimally memorize the context at test time.
  arXiv preprint arXiv:2505.23735, 2025.
- [10]

  Ali Behrouz, Meisam Razaviyayn, Peilin Zhong, and Vahab Mirrokni.
  It’s all connected: A journey through test-time memorization, attentional bias, retention, and online optimization.
  arXiv preprint arXiv:2504.13173, 2025.
- [11]

  Ali Behrouz, Peilin Zhong, and Vahab Mirrokni.
  Titans: Learning to memorize at test time.
  arXiv preprint arXiv:2501.00663, 2024.
- [12]

  Iz Beltagy, Matthew E Peters, and Arman Cohan.
  Longformer: The long-document transformer.
  arXiv preprint arXiv:2004.05150, 2020.
- [13]

  Aman Bhargava, Cameron Witkowski, Alexander Detkov, and Matt Thomson.
  Prompt baking.
  arXiv preprint arXiv:2409.13697, 2024.
- [14]

  Aaron Blakeman, Aarti Basant, Abhinav Khattar, Adithya Renduchintala, Akhiad Bercovich, Aleksander Ficek, Alexis Bjorlin, Ali Taghibakhshi, Amala Sanjay Deshmukh, Ameya Sunil Mahabaleshwarkar, et al.
  Nemotron-h: A family of accurate and efficient hybrid mamba-transformer models.
  arXiv preprint arXiv:2504.03624, 2025.
- [15]

  Lucas Caccia, Alan Ansell, Edoardo Ponti, Ivan Vulic, and Alessandro Sordoni.
  Training plug-n-play knowledge modules with deep context distillation.
  arXiv preprint arXiv:2503.08727, 2025.
- [16]

  Chi-Chih Chang, Wei-Cheng Lin, Chien-Yu Lin, Chong-Yan Chen, Yu-Fang Hu, Pei-Shuo Wang, Ning-Chi Huang, Luis Ceze, Mohamed S Abdelfattah, and Kai-Chiang Wu.
  Palu: Compressing kv-cache with low-rank projection.
  arXiv preprint arXiv:2407.21118, 2024.
- [17]

  Vivek Chari, Guanghui Qin, and Benjamin Van Durme.
  Kv-distill: Nearly lossless learnable context compression for llms.
  arXiv preprint arXiv:2503.10337, 2025.
- [18]

  Lequn Chen, Zihao Ye, Yongji Wu, Danyang Zhuo, Luis Ceze, and Arvind Krishnamurthy.
  Punica: Multi-tenant lora serving.
  Proceedings of Machine Learning and Systems, 6:1–13, 2024.
- [19]

  Alexis Chevalier, Alexander Wettig, Anirudh Ajith, and Danqi Chen.
  Adapting language models to compress contexts.
  arXiv preprint arXiv:2305.14788, 2023.
- [20]

  Rewon Child, Scott Gray, Alec Radford, and Ilya Sutskever.
  Generating long sequences with sparse transformers.
  arXiv preprint arXiv:1904.10509, 2019.
- [21]

  Yu-Neng Chuang, Tianwei Xing, Chia-Yuan Chang, Zirui Liu, Xun Chen, and Xia Hu.
  Learning to compress prompt in natural language formats.
  arXiv preprint arXiv:2402.18700, 2024.
- [22]

  Tri Dao, Dan Fu, Stefano Ermon, Atri Rudra, and Christopher Ré.
  Flashattention: Fast and memory-efficient exact attention with io-awareness.
  Advances in neural information processing systems, 35:16344–16359, 2022.
- [23]

  Pradeep Dasigi, Kyle Lo, Iz Beltagy, Arman Cohan, Noah A Smith, and Matt Gardner.
  A dataset of information-seeking questions and answers anchored in research papers.
  arXiv preprint arXiv:2105.03011, 2021.
- [24]

  Qingxiu Dong, Lei Li, Damai Dai, Ce Zheng, Jingyuan Ma, Rui Li, Heming Xia, Jingjing Xu, Zhiyong Wu, Tianyu Liu, et al.
  A survey on in-context learning.
  arXiv preprint arXiv:2301.00234, 2022.
- [25]

  Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Amy Yang, Angela Fan, et al.
  The Llama 3 Herd of Models.
  arXiv preprint arXiv:2407.21783, 2024.
- [26]

  Saumya Gandhi, Ritu Gala, Vijay Viswanathan, Tongshuang Wu, and Graham Neubig.
  Better synthetic data by retrieving and transforming existing datasets.
  arXiv preprint arXiv:2404.14361, 2024.
- [27]

  Suyu Ge, Yunan Zhang, Liyuan Liu, Minjia Zhang, Jiawei Han, and Jianfeng Gao.
  Model tells you what to discard: Adaptive kv cache compression for llms.
  arXiv preprint arXiv:2310.01801, 2023.
- [28]

  Tao Ge, Jing Hu, Lei Wang, Xun Wang, Si-Qing Chen, and Furu Wei.
  In-context autoencoder for context compression in a large language model.
  arXiv preprint arXiv:2307.06945, 2023.
- [29]

  Kanishk Goel, Jayashree Mohan, Nipun Kwatra, Ravi Shreyas Anupindi, and Ramachandran Ramjee.
  Niyama: Breaking the silos of llm inference serving.
  arXiv preprint arXiv:2503.22562, 2025.
- [30]

  Yunhao Gou, Zhili Liu, Kai Chen, Lanqing Hong, Hang Xu, Aoxue Li, Dit-Yan Yeung, James T Kwok, and Yu Zhang.
  Mixture of cluster-conditional lora experts for vision-language instruction tuning.
  arXiv preprint arXiv:2312.12379, 2023.
- [31]

  Albert Gu and Tri Dao.
  Mamba: Linear-time sequence modeling with selective state spaces.
  arXiv preprint arXiv:2312.00752, 2023.
- [32]

  Neel Guha, Julian Nyarko, Daniel Ho, Christopher Ré, Adam Chilton, Alex Chohlas-Wood, Austin Peters, Brandon Waldon, Daniel Rockmore, Diego Zambrano, et al.
  Legalbench: A collaboratively built benchmark for measuring legal reasoning in large language models.
  Advances in Neural Information Processing Systems, 36:44123–44279, 2023.
- [33]

  Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al.
  Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning.
  arXiv preprint arXiv:2501.12948, 2025.
- [34]

  Dan Hendrycks, Collin Burns, Steven Basart, Andy Zou, Mantas Mazeika, Dawn Song, and Jacob Steinhardt.
  Measuring massive multitask language understanding.
  arXiv preprint arXiv:2009.03300, 2020.
- [35]

  Geoffrey Hinton, Oriol Vinyals, and Jeff Dean.
  Distilling the knowledge in a neural network.
  arXiv preprint arXiv:1503.02531, 2015.
- [36]

  Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al.
  Lora: Low-rank adaptation of large language models.
  ICLR, 1(2):3, 2022.
- [37]

  Chengsong Huang, Qian Liu, Bill Yuchen Lin, Tianyu Pang, Chao Du, and Min Lin.
  Lorahub: Efficient cross-task generalization via dynamic lora composition.
  arXiv preprint arXiv:2307.13269, 2023.
- [38]

  Pranab Islam, Anand Kannappan, Douwe Kiela, Rebecca Qian, Nino Scherrer, and Bertie Vidgen.
  Financebench: A new benchmark for financial question answering.
  arXiv preprint arXiv:2311.11944, 2023.
- [39]

  Shashwat Jaiswal, Kunal Jain, Yogesh Simmhan, Anjaly Parayil, Ankur Mallick, Rujia Wang, Renee St Amant, Chetan Bansal, Victor Rühle, Anoop Kulkarni, et al.
  Serving models, fast and slow: optimizing heterogeneous llm inferencing workloads at scale.
  arXiv preprint arXiv:2502.14617, 2025.
- [40]

  Dulhan Jayalath, James Bradley Wendt, Nicholas Monath, Sandeep Tata, and Beliz Gunel.
  Long-range tasks using short-context llms: Incremental reasoning with structured memories.
  arXiv preprint arXiv:2412.18914, 2024.
- [41]

  Fengqing Jiang.
  Identifying and mitigating vulnerabilities in llm-integrated applications.
  Master’s thesis, University of Washington, 2024.
- [42]

  Huiqiang Jiang, Qianhui Wu, Chin-Yew Lin, Yuqing Yang, and Lili Qiu.
  Llmlingua: Compressing prompts for accelerated inference of large language models.
  arXiv preprint arXiv:2310.05736, 2023.
- [43]

  Huiqiang Jiang, Qianhui Wu, Chin-Yew Lin, Yuqing Yang, and Lili Qiu.
  LLMLingua: Compressing prompts for accelerated inference of large language models.
  In Houda Bouamor, Juan Pino, and Kalika Bali, editors, Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, pages 13358–13376, Singapore, December 2023. Association for Computational Linguistics.
- [44]

  Jordan Juravsky, Bradley Brown, Ryan Ehrlich, Daniel Y. Fu, Christopher Ré, and Azalia Mirhoseini.
  Hydragen: High-throughput llm inference with shared prefixes, 2024.
- [45]

  Jordan Juravsky, Ayush Chakravarthy, Ryan Ehrlich, Sabri Eyuboglu, Bradley Brown, Joseph Shetaye, Christopher Ré, and Azalia Mirhoseini.
  Tokasaurus: An llm inference engine for high-throughput workloads, June 2025.
- [46]

  Junhyuck Kim, Jongho Park, Jaewoong Cho, and Dimitris Papailiopoulos.
  Lexico: Extreme kv cache compression via sparse coding over universal dictionaries.
  arXiv preprint arXiv:2412.08890, 2024.
- [47]

  Yoon Kim and Alexander M Rush.
  Sequence-level knowledge distillation.
  In Proceedings of the 2016 conference on empirical methods in natural language processing, pages 1317–1327, 2016.
- [48]

  Kalle Kujanpää, Harri Valpola, and Alexander Ilin.
  Knowledge injection via prompt distillation.
  arXiv preprint arXiv:2412.14964, 2024.
- [49]

  Yuri Kuratov, Mikhail Arkhipov, Aydar Bulatov, and Mikhail Burtsev.
  Cramming 1568 tokens into a single vector and back again: Exploring the limits of embedding space capacity.
  arXiv preprint arXiv:2502.13063, 2025.
- [50]

  Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica.
  Efficient memory management for large language model serving with pagedattention.
  In Proceedings of the 29th Symposium on Operating Systems Principles, pages 611–626, 2023.
- [51]

  Brian Lester, Rami Al-Rfou, and Noah Constant.
  The power of scale for parameter-efficient prompt tuning.
  arXiv preprint arXiv:2104.08691, 2021.
- [52]

  Aonian Li, Bangwei Gong, Bo Yang, Boji Shan, Chang Liu, Cheng Zhu, Chunhao Zhang, Congchao Guo, Da Chen, Dong Li, et al.
  Minimax-01: Scaling foundation models with lightning attention.
  arXiv preprint arXiv:2501.08313, 2025.
- [53]

  Dengchun Li, Yingzi Ma, Naizheng Wang, Zhengmao Ye, Zhiyuan Cheng, Yinghao Tang, Yan Zhang, Lei Duan, Jie Zuo, Cal Yang, et al.
  Mixlora: Enhancing large language models fine-tuning with lora-based mixture of experts.
  arXiv preprint arXiv:2404.15159, 2024.
- [54]

  Xiang Lisa Li and Percy Liang.
  Prefix-tuning: Optimizing continuous prompts for generation.
  In Chengqing Zong, Fei Xia, Wenjie Li, and Roberto Navigli, editors, Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers), pages 4582–4597, Online, August 2021. Association for Computational Linguistics.
- [55]

  Yucheng Li.
  Unlocking context constraints of llms: Enhancing context efficiency of llms with self-information-based content filtering.
  arXiv preprint arXiv:2304.12102, 2023.
- [56]

  Yuhong Li, Yingbing Huang, Bowen Yang, Bharat Venkitesh, Acyr Locatelli, Hanchen Ye, Tianle Cai, Patrick Lewis, and Deming Chen.
  Snapkv: Llm knows what you are looking for before generation.
  Advances in Neural Information Processing Systems, 37:22947–22970, 2024.
- [57]

  Aixin Liu, Bei Feng, Bin Wang, Bingxuan Wang, Bo Liu, Chenggang Zhao, Chengqi Dengr, Chong Ruan, Damai Dai, Daya Guo, et al.
  Deepseek-v2: A strong, economical, and efficient mixture-of-experts language model.
  arXiv preprint arXiv:2405.04434, 2024.
- [58]

  Akide Liu, Jing Liu, Zizheng Pan, Yefei He, Gholamreza Haffari, and Bohan Zhuang.
  Minicache: Kv cache compression in depth dimension for large language models.
  Advances in Neural Information Processing Systems, 37, 2024.
- [59]

  Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang.
  Lost in the middle: How language models use long contexts.
  Transactions of the Association for Computational Linguistics, 12:157–173, 2024.
- [60]

  Yansheng Mao, Yufei Xu, Jiaqi Li, Fanxu Meng, Haotong Yang, Zilong Zheng, Xiyuan Wang, and Muhan Zhang.
  Lift: Improving long context understanding of large language models through long input fine-tuning.
  arXiv preprint arXiv:2502.14644, 2025.
- [61]

  Fanxu Meng, Zhaohui Wang, and Muhan Zhang.
  Pissa: Principal singular values and singular vectors adaptation of large language models.
  Advances in Neural Information Processing Systems, 37:121038–121072, 2024.
- [62]

  Jesse Mu, Xiang Li, and Noah Goodman.
  Learning to compress prompts with gist tokens.
  Advances in Neural Information Processing Systems, 36:19327–19352, 2023.
- [63]

  Daye Nam, Andrew Macvean, Vincent Hellendoorn, Bogdan Vasilescu, and Brad Myers.
  Using an llm to help with code understanding.
  In Proceedings of the IEEE/ACM 46th International Conference on Software Engineering, pages 1–13, 2024.
- [64]

  Avanika Narayan, Dan Biderman, Sabri Eyuboglu, Avner May, Scott Linderman, James Zou, and Christopher Re.
  Minions: Cost-efficient collaboration between on-device and cloud language models.
  arXiv preprint arXiv:2502.15964, 2025.
- [65]

  Nihal V Nayak, Yiyang Nan, Avi Trost, and Stephen H Bach.
  Learning to generate instruction tuning datasets for zero-shot task adaptation.
  arXiv preprint arXiv:2402.18334, 2024.
- [66]

  OpenAI.
  Gpt-4o system card, 2024.
- [67]

  Matanel Oren, Michael Hassid, Nir Yarden, Yossi Adi, and Roy Schwartz.
  Transformers are multi-state rnns.
  arXiv preprint arXiv:2401.06104, 2024.
- [68]

  Lisa Larrimore Ouellette, Amy Motomura, Jason Reinecke, and Jonathan S Masur.
  Can ai hold office hours?
  Available at SSRN 5166938, 2025.
- [69]

  Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G Patil, Ion Stoica, and Joseph E Gonzalez.
  Memgpt: Towards llms as operating systems.
  arXiv preprint arXiv:2310.08560, 2023.
- [70]

  Zhuoshi Pan, Qianhui Wu, Huiqiang Jiang, Menglin Xia, Xufang Luo, Jue Zhang, Qingwei Lin, Victor Rühle, Yuqing Yang, Chin-Yew Lin, et al.
  Llmlingua-2: Data distillation for efficient and faithful task-agnostic prompt compression.
  arXiv preprint arXiv:2403.12968, 2024.
- [71]

  Maja Popović.
  chrf: character n-gram f-score for automatic mt evaluation.
  In Proceedings of the tenth workshop on statistical machine translation, pages 392–395, 2015.
- [72]

  Guanghui Qin, Corby Rosset, Ethan C Chau, Nikhil Rao, and Benjamin Van Durme.
  Dodo: Dynamic contextual compression for decoder-only lms.
  arXiv preprint arXiv:2310.02409, 2023.
- [73]

  Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev, and Percy Liang.
  Squad: 100,000+ questions for machine comprehension of text.
  arXiv preprint arXiv:1606.05250, 2016.
- [74]

  Haris Riaz, Sourav Bhabesh, Vinayak Arannil, Miguel Ballesteros, and Graham Horwood.
  Metasynth: Meta-prompting-driven agentic scaffolds for diverse synthetic data generation.
  arXiv preprint arXiv:2504.12563, 2025.
- [75]

  Luka Ribar, Ivan Chelombiev, Luke Hudlass-Galley, Charlie Blake, Carlo Luschi, and Douglas Orr.
  Sparq attention: Bandwidth-efficient llm inference.
  arXiv preprint arXiv:2312.04985, 2023.
- [76]

  Melisa Russak, Umar Jamil, Christopher Bryant, Kiran Kamble, Axel Magnuson, Mateusz Russak, and Waseem AlShikh.
  Writing in the margins: Better inference pattern for long context retrieval.
  arXiv preprint arXiv:2408.14906, 2024.
- [77]

  Utkarsh Saxena, Gobinda Saha, Sakshi Choudhary, and Kaushik Roy.
  Eigen attention: Attention in low-rank space for kv cache compression.
  arXiv preprint arXiv:2408.05646, 2024.
- [78]

  Noam Shazeer.
  Fast transformer decoding: One write-head is all you need.
  arXiv preprint arXiv:1911.02150, 2019.
- [79]

  Charlie Snell, Dan Klein, and Ruiqi Zhong.
  Learning by distilling context.
  arXiv preprint arXiv:2209.15189, 2022.
- [80]

  Charlie Snell, Jaehoon Lee, Kelvin Xu, and Aviral Kumar.
  Scaling llm test-time compute optimally can be more effective than scaling model parameters.
  arXiv preprint arXiv:2408.03314, 2024.
- [81]

  Weihang Su, Yichen Tang, Qingyao Ai, Junxi Yan, Changyue Wang, Hongning Wang, Ziyi Ye, Yujia Zhou, and Yiqun Liu.
  Parametric retrieval augmented generation.
  arXiv preprint arXiv:2501.15915, 2025.
- [82]

  Yu Sun, Xinhao Li, Karan Dalal, Jiarui Xu, Arjun Vikram, Genghan Zhang, Yann Dubois, Xinlei Chen, Xiaolong Wang, Sanmi Koyejo, et al.
  Learning to (learn at test time): Rnns with expressive hidden states.
  arXiv preprint arXiv:2407.04620, 2024.
- [83]

  Sijun Tan, Xiuyu Li, Shishir Patil, Ziyang Wu, Tianjun Zhang, Kurt Keutzer, Joseph E Gonzalez, and Raluca Ada Popa.
  Lloco: Learning long contexts offline.
  arXiv preprint arXiv:2404.07979, 2024.
- [84]

  Jiaming Tang, Yilong Zhao, Kan Zhu, Guangxuan Xiao, Baris Kasikci, and Song Han.
  Quest: Query-aware sparsity for efficient long-context llm inference.
  arXiv preprint arXiv:2406.10774, 2024.
- [85]

  Garrett Tanzer, Mirac Suzgun, Eline Visser, Dan Jurafsky, and Luke Melas-Kyriazi.
  A benchmark for learning to translate a new language from one grammar book.
  arXiv preprint arXiv:2309.16575, 2023.
- [86]

  Gemma Team, Morgane Riviere, Shreya Pathak, Pier Giuseppe Sessa, Cassidy Hardin, Surya Bhupatiraju, Léonard Hussenot, Thomas Mesnard, Bobak Shahriari, Alexandre Ramé, et al.
  Gemma 2: Improving open language models at a practical size.
  arXiv preprint arXiv:2408.00118, 2024.
- [87]

  Jamba Team, Barak Lenz, Alan Arazi, Amir Bergman, Avshalom Manevich, Barak Peleg, Ben Aviram, Chen Almagor, Clara Fridman, Dan Padnos, et al.
  Jamba-1.5: Hybrid transformer-mamba models at scale.
  arXiv preprint arXiv:2408.12570, 2024.
- [88]

  U.S. Securities and Exchange Commission.
  How to read a 10-k, 2011.
  Accessed: 2025-05-14.
- [89]

  Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin.
  Attention is all you need.
  Advances in neural information processing systems, 30, 2017.
- [90]

  Zhongwei Wan, Xinjian Wu, Yu Zhang, Yi Xin, Chaofan Tao, Zhihong Zhu, Xin Wang, Siqi Luo, Jing Xiong, and Mi Zhang.
  D2o: Dynamic discriminative operations for efficient generative inference of large language models.
  arXiv preprint arXiv:2406.13035, 2024.
- [91]

  Zheng Wang, Boxiao Jin, Zhongzhi Yu, and Minjia Zhang.
  Model tells you where to merge: Adaptive kv cache merging for llms on long-context tasks.
  arXiv preprint arXiv:2407.08454, 2024.
- [92]

  Xun Wu, Shaohan Huang, and Furu Wei.
  Mixture of lora experts.
  arXiv preprint arXiv:2404.13628, 2024.
- [93]

  Chaojun Xiao, Zhengyan Zhang, Xu Han, Chi-Min Chan, Yankai Lin, Zhiyuan Liu, Xiangyang Li, Zhonghua Li, Zhao Cao, and Maosong Sun.
  Plug-and-play document modules for pre-trained models.
  arXiv preprint arXiv:2305.17660, 2023.
- [94]

  Chaojun Xiao, Zhengyan Zhang, Chenyang Song, Dazhi Jiang, Feng Yao, Xu Han, Xiaozhi Wang, Shuo Wang, Yufei Huang, Guanyu Lin, et al.
  Configurable foundation models: Building llms from a modular perspective.
  arXiv preprint arXiv:2409.02877, 2024.
- [95]

  Guangxuan Xiao, Jiaming Tang, Jingwei Zuo, Junxian Guo, Shang Yang, Haotian Tang, Yao Fu, and Song Han.
  Duoattention: Efficient long-context llm inference with retrieval and streaming heads.
  arXiv preprint arXiv:2410.10819, 2024.
- [96]

  Guangxuan Xiao, Yuandong Tian, Beidi Chen, Song Han, and Mike Lewis.
  Efficient streaming language models with attention sinks, 2024.
- [97]

  Prateek Yadav, Colin Raffel, Mohammed Muqeeth, Lucas Caccia, Haokun Liu, Tianlong Chen, Mohit Bansal, Leshem Choshen, and Alessandro Sordoni.
  A survey on model moerging: Recycling and routing among specialized experts for collaborative learning.
  arXiv preprint arXiv:2408.07057, 2024.
- [98]

  An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoran Wei, et al.
  Qwen2. 5 technical report.
  arXiv preprint arXiv:2412.15115, 2024.
- [99]

  Songlin Yang, Bailin Wang, Yikang Shen, Rameswar Panda, and Yoon Kim.
  Gated linear attention transformers with hardware-efficient training.
  In Proceedings of ICML, 2024.
- [100]

  Songlin Yang, Bailin Wang, Yu Zhang, Yikang Shen, and Yoon Kim.
  Parallelizing linear transformers with the delta rule over sequence length.
  arXiv preprint arXiv:2406.06484, 2024.
- [101]

  Songlin Yang, Bailin Wang, Yu Zhang, Yikang Shen, and Yoon Kim.
  Parallelizing linear transformers with the delta rule over sequence length, 2025.
- [102]

  Songlin Yang and Yu Zhang.
  Fla: A triton-based library for hardware-efficient implementations of linear attention mechanism, January 2024.
- [103]

  Zihao Ye, Lequn Chen, Ruihang Lai, Wuwei Lin, Yineng Zhang, Stephanie Wang, Tianqi Chen, Baris Kasikci, Vinod Grover, Arvind Krishnamurthy, and Luis Ceze.
  Flashinfer: Efficient and customizable attention engine for llm inference serving.
  arXiv preprint arXiv:2501.01005, 2025.
- [104]

  Howard Yen.
  Long-context language modeling with parallel context encoding.
  Master’s thesis, Princeton University, 2024.
- [105]

  Hao Yu, Zelan Yang, Shen Li, Yong Li, and Jianxin Wu.
  Effectively compress kv heads for llm.
  arXiv preprint arXiv:2406.07056, 2024.
- [106]

  Manzil Zaheer, Guru Guruganesh, Kumar Avinava Dubey, Joshua Ainslie, Chris Alberti, Santiago Ontanon, Philip Pham, Anirudh Ravula, Qifan Wang, Li Yang, et al.
  Big bird: Transformers for longer sequences.
  Advances in neural information processing systems, 33:17283–17297, 2020.
- [107]

  Elad Ben Zaken, Shauli Ravfogel, and Yoav Goldberg.
  Bitfit: Simple parameter-efficient fine-tuning for transformer-based masked language-models.
  arXiv preprint arXiv:2106.10199, 2021.
- [108]

  Michael Zhang, Simran Arora, Rahul Chalamala, Alan Wu, Benjamin Spector, Aaryan Singhal, Krithik Ramesh, and Christopher Ré.
  Lolcats: On low-rank linearizing of large language models.
  arXiv preprint arXiv:2410.10254, 2024.
- [109]

  Qianchi Zhang, Hainan Zhang, Liang Pang, Hongwei Zheng, and Zhiming Zheng.
  Adacomp: Extractive context compression with adaptive predictor for retrieval-augmented large language models.
  arXiv preprint arXiv:2409.01579, 2024.
- [110]

  Rongzhi Zhang, Kuang Wang, Liyuan Liu, Shuohang Wang, Hao Cheng, Chao Zhang, and Yelong Shen.
  Lorc: Low-rank compression for llms kv cache with a progressive compression strategy.
  arXiv preprint arXiv:2410.03111, 2024.
- [111]

  Yifan Zhang, Yifeng Liu, Huizhuo Yuan, Zhen Qin, Yang Yuan, Quanquan Gu, and Andrew Chi-Chih Yao.
  Tensor product attention is all you need.
  arXiv preprint arXiv:2501.06425, 2025.
- [112]

  Yuxin Zhang, Yuxuan Du, Gen Luo, Yunshan Zhong, Zhenyu Zhang, Shiwei Liu, and Rongrong Ji.
  Cam: Cache merging for memory-efficient llms inference.
  In Forty-first International Conference on Machine Learning, 2024.
- [113]

  Zhengyan Zhang, Zhiyuan Zeng, Yankai Lin, Huadong Wang, Deming Ye, Chaojun Xiao, Xu Han, Zhiyuan Liu, Peng Li, Maosong Sun, et al.
  Plug-and-play knowledge injection for pre-trained language models.
  arXiv preprint arXiv:2305.17691, 2023.
- [114]

  Zhenyu Zhang, Ying Sheng, Tianyi Zhou, Tianlong Chen, Lianmin Zheng, Ruisi Cai, Zhao Song, Yuandong Tian, Christopher Ré, Clark Barrett, et al.
  H2o: Heavy-hitter oracle for efficient generative inference of large language models.
  Advances in Neural Information Processing Systems, 36:34661–34710, 2023.
- [115]

  Ziyu Zhao, Leilei Gan, Guoyin Wang, Wangchunshu Zhou, Hongxia Yang, Kun Kuang, and Fei Wu.
  Loraretriever: Input-aware lora retrieval and composition for mixed tasks in the wild.
  arXiv preprint arXiv:2402.09997, 2024.
- [116]

  Ziyu Zhao, Tao Shen, Didi Zhu, Zexi Li, Jing Su, Xuwu Wang, Kun Kuang, and Fei Wu.
  Merging loras like playing lego: Pushing the modularity of lora to extremes through rank-wise clustering.
  arXiv preprint arXiv:2409.16167, 2024.
- [117]

  Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Chuyue Livia Sun, Jeff Huang, Cody Hao Yu, Shiyi Cao, Christos Kozyrakis, Ion Stoica, Joseph E Gonzalez, et al.
  Sglang: Efficient execution of structured language model programs.
  Advances in Neural Information Processing Systems, 37:62557–62583, 2024.
- [118]

  Lucia Zheng, Neel Guha, Javokhir Arifov, Sarah Zhang, Michal Skreta, Christopher D Manning, Peter Henderson, and Daniel E Ho.
  A reasoning-focused legal retrieval benchmark.
  In Proceedings of the 2025 Symposium on Computer Science and Law, pages 169–193, 2025.
- [119]

  Yuhao Zhou, Sirui Song, Boyang Liu, Zhiheng Xi, Senjie Jin, Xiaoran Fan, Zhihao Zhang, Wei Li, and Xuanjing Huang.
  Elitekv: Scalable kv cache compression via rope frequency selection and joint low-rank projection.
  arXiv preprint arXiv:2503.01586, 2025.

![Refer to caption](2506.06266v3/parameterization-fig.png)

图 8：
比较 Cartridge 参数化。
我们用自学习在 LongHealth（上）、QASPER（中）与 MTOB（下）的语料上以两种不同参数化训练 Cartridge：简化版前缀微调（如 §3.2 所述）与低秩适配（LoRA）[36]。
我们尝试不同的 Cartridge 大小，并选择使内存消耗对齐的 LoRA 秩与前缀微调缓存大小。
我们用与图 4 相同的协议在目标数据集（LongHealth 或 QASPER）的问题上评测 Cartridge 的性能，同时在与语料无关的 MMLU [34] 问题上评测。
（左）$x$ 轴为 MMLU 准确率，$y$ 轴为目标数据集准确率。每个点代表一个不同的 Cartridge 大小。
（中）$x$ 轴为 Cartridge 大小（GB），$y$ 轴为 MMLU 准确率。
（右）$x$ 轴为自学习时长（训练步数），$y$ 轴为 MMLU 准确率。点的深浅代表 Cartridge 的大小。

## 附录 A 扩展结果

在本节中，我们消融 Cartridges 与 Self-Study 的主要设计选择。

### A.1 Cartridge 设计选择：参数化与初始化

在我们的实验中，我们用简化版前缀微调参数化 Cartridge，并用截断的 KV 缓存初始化（见 §3.2）。本节描述支撑这些设计选择的消融实验。首先，我们比较两种不同的 Cartridge 参数化（图 8）：简化前缀微调 [54] 与低秩适配（LoRA）[36]。然后，我们展示恰当初始化 Cartridge 的重要性（图 9）。

##### 参数化

我们在 LongHealth 或 QASPER 的语料上训练 Cartridge，并在域内（即 LongHealth 或 QASPER 的问题）与域外（即来自无关基准 MMLU [34] 的问题）查询上评测。

我们发现，在域内与域外查询上，前缀微调参数化都比内存对齐的 LoRA 参数化更有效。如图 8（左）所示，前缀微调占据了图的右上角（在 MMLU 与目标数据集上准确率都高）。

值得注意的是，我们发现随着 LoRA 微调的 Cartridge 大小增大，域外查询（MMLU）的性能显著下降。在 1.06 GB（LoRA 秩 1632）时，MMLU 准确率从 60.0% 降至 45.3%。这一性能下降与 Cartridge 大小高度相关，表明 LoRA 不适合大 Cartridge——而我们在图 4 中展示大 Cartridge 对恢复 ICL 性能很重要。相比之下，前缀微调在 1.06 GB 时准确率只降到 54.3%。这一退化对 Cartridge 大小基本不变（0.15 GB 时 54.7%），说明域外性能在各 Cartridge 大小下都很稳健。

在域内查询上，前缀微调同样胜过 LoRA，但差距更小。在所有 Cartridge 大小中，前缀微调在 LongHealth 上取得的最佳准确率为 0.96 GB 时的 55.6%，而 LoRA 的最佳准确率为 0.26 GB 时的 47.25%。有趣的是，LoRA 在最大 Cartridge 大小下的准确率反而更低：0.96 GB 时 41.3%。这可能源于上文讨论的 LoRA 域外退化。由于 LongHealth 测试集中的查询与 Self-Study 生成的合成查询差别很大（例如它们是选择题且需要较复杂的推理轨迹），域外稳健性对「域内」性能可能也很重要。

目前尚不清楚为什么前缀微调对域外性能退化比 LoRA 稳健得多。考虑到 KV 缓存与 MLP 的相似性——两者都是由非线性隔开的线性变换——这令人意外。这可能源于激活函数的差异（SiLU 与 Softmax）。我们把对这一差异根因的更详细研究留作未来工作。

##### 初始化

图 9：消融 Cartridge 初始化。我们在 LongHealth 的语料上用 Self-Study 以 3 种不同初始化策略训练 Cartridge。$x$ 轴为训练步数，$y$ 轴为 LongHealth 准确率。蓝线是用文档前 $k$ 个词元的 KV 缓存初始化 Cartridge 的结果。紫线是用无关文本的 KV 缓存初始化 Cartridge。绿线是用随机向量初始化 Cartridge。用前 $k$ 个词元初始化比用随机文本的 KV 缓存初始化结果略强。这一差异在其他语料上（前 $k$ 个词元与解决下游任务更相关时）可能更明显。

我们主论文中初始化 $k$ 词元 Cartridge 的标准方式是使用源文档前 $k$ 个词元的 KV 缓存。在图 9 中，我们消融不同的初始化来源，尝试两种额外初始化：随机向量与随机词元。

对随机向量，我们简单地从逐分量标准正态分布初始化 Cartridge 的参数。对随机词元，我们把 Cartridge 初始化为任意文本（具体为[梯度的维基百科页面](https://en.wikipedia.org/wiki/Gradient)）前 $k$ 个词元的 KV 缓存。这两种策略的重要区别在于：对随机词元，初始 Cartridge 是模型产生的「有效」KV 缓存；而随机向量则不是。

图 10：冻结注意力汇。两图中 $y$ 轴为准确率，$x$ 轴为训练步数。绿线对应允许首个词元可训练的运行。（左）$y$ 轴为 MMLU 准确率。该图展示了我们在键值向量可训练时观察到的训练不稳定：MMLU 分数先跌到 30% 以下再恢复。（左）$y$ 轴为 LongHealth 问题的准确率。（译注：原文两处均标「左」，第二处按语义为右图。）

##### 冻结注意力汇

训练 Cartridge 的一个小而重要的细节是：我们不让第一个词元的键值向量可训练。如 [96] 所研究，第一个键向量对应序列起始词元，因此对每个序列都相同，充当「注意力汇」（attention sink）。我们观察到，训练 Cartridge 时若允许这些键值向量可训练会导致训练不稳定（见图 10）。例如，在某些运行中 MMLU 准确率会跌破 30%。

### A.2 Self-Study 设计选择：数据生成与目标

在 Self-Study 训练中，我们使用带种子的数据生成流程与上下文蒸馏训练目标（见 §4）。本节消融这些设计选择，并与使用更简单的数据生成和目标的 Self-Study 性能进行比较。

##### 数据生成

在 §4.1 中，我们描述了用算法 1 生成数据时如何使用五种不同的种子提示类型。这些提示类型（结构化、摘要、提问、使用场景、创意）在 §C.1 中有更详细的描述。

本节比较使用这五种提示类型的 Self-Study 与使用单条提示的 Self-Study："Please generate a single chat message to begin a conversation about the information in the corpus. Ask a question about the corpus or make a request."

在三个数据集上，我们发现 Self-Study 期间使用五种不同提示类型能产出更高质量的 Cartridge（见图 12）。在 MTOB 上（1024 词元 Cartridge），我们看到 7.9 个 chrF 分的提升（24.1→32.0）。在 LongHealth 上，提升为 5.5 个准确率点（45.8→51.3）。

有趣的是，在 QASPER 上我们没有看到使用五种不同提示类型的收益。这可能是因为 QASPER 数据集中的查询大多是事实性问题，不像 LongHealth 与 MTOB 那样需要复杂推理。

图 11：多样化种子提示提升质量。
我们按算法 1 生成合成数据，并消融第 2 行采样的种子提示选择。
我们考虑两种做法：使用单一宽泛种子提示（绿色）或从五种不同类型中随机采样一种（蓝色）。
我们在 LongHealth、MTOB 与 QASPER 语料上用这两种策略以自学习训练 Cartridge。
所有图中，$x$ 轴为训练步数，$y$ 轴为准确率（LongHealth 与 MTOB）或金标准答案上的困惑度（QASPER）。
Cartridge 大小为 1024 词元。

##### 训练目标

在 §4 中，我们描述了所用的上下文蒸馏目标 [79, 47, 13]。这一方法要求在数据生成期间从上下文内模型的输出分布收集 top 输出概率。一个更简单的替代是只用带交叉熵损失的下一词元预测目标。

在比较中，我们发现这个更简单的目标不如上下文蒸馏目标（见图 12）。最显著的是，在 MTOB 上（2048 词元 Cartridge），上下文蒸馏比下一词元预测高 8.3 个 chrF 分（24.9→33.2）。在 LongHealth 上，差距为 3.7 个准确率点（47.6→51.3）。

图 12：上下文蒸馏目标提升训练效率。我们在 LongHealth（左）、MTOB（中）与 QASPER（右）的语料上用 Self-Study 配合两种损失函数训练 Cartridge：下一词元预测损失（绿色）与蒸馏损失（蓝色）。我们用与图 5 相同的协议在目标数据集（LongHealth、MTOB 或 QASPER）的问题上评测 Cartridge 的性能。所有图中，$x$ 轴为训练步数，$y$ 轴为准确率（LongHealth 与 MTOB）或金标准答案上的困惑度（QASPER）。点的深浅代表 Cartridge 的大小。在各数据集与各 Cartridge 大小下，使用蒸馏损失都能取得更高准确率（QASPER 上更低困惑度）。

如图 12 所示，质量似乎随 Self-Study 计算量的增加持续提升。因此，有可能通过在下一词元预测目标上投入更多 Self-Study 计算来缩小差距。然而，在固定 Self-Study 计算量下，上下文蒸馏明显更有效。

这些结果展示了上下文蒸馏在用 Self-Study 高效恢复 ICL 性能中的重要作用。

### A.3 吞吐测量细节

我们提供图 3 中吞吐测量的细节。我们使用最先进的 SGLang 推理系统与默认参数 [117]。我们在单块 H100 GPU 上测量吞吐。

我们先确定给定 $k$ 词元缓存下能放进 GPU 内存的最大批大小 $b$。然后随机初始化 $b$ 个大小为 $k$ 的 Cartridge 并预载入 GPU 内存。最后测量每个序列解码 128 个词元所需时间。生成期间，Cartridge 与解码词元被追加进 KV 缓存。我们在 3 次热身迭代后报告 5 次迭代的平均值。

## 附录 B 扩展相关工作

在本节中，我们更深入地讨论我们的工作在更广泛文献中的位置。以下结构与正文对应：先讨论与 Cartridge 参数化和初始化相关的工作（§B.1），然后介绍启发 Self-Study 设计的工作（§B.2），最后描述其他旨在缩减 KV 缓存大小的方法（§B.3），其中许多我们在实验中与之比较。

### B.1 与 Cartridge 参数化相关的先前工作

下面我们讨论参数高效微调文献中启发我们参数化 Cartridge 方式的先前工作。

#### B.1.1 参数高效微调（PEFT）

为了以更省算力与内存的方式把大型语言模型（LLM）适配到特定领域或任务，学界发展出若干参数高效微调（PEFT）方法。使用最广泛的 PEFT 方法包括低秩适配（LoRA）[36]、前缀微调 [54] 与提示微调 [51]。

利用「微调后的语言模型呈现内在低秩结构」这一先前观察，Hu et al. 提出 LoRA：冻结模型参数，并在每个 transformer 层之间注入可训练的秩分解矩阵。LoRA 在微调质量持平或更优的同时，把可训练参数减少 10,000 倍、GPU 内存需求降低 3 倍 [36]。

Li et al. 与 Lester et al. 各自采取了另一种轻量微调途径，分别提出可调「前缀」与「软提示」置于查询之前以引导模型产生期望输出。Li et al. 提出前缀微调（prefix-tuning），为每个 transformer 层上前缀的激活学习连续表示，再把这些学到的激活前置到冻结 transformer 处理输入提示所得的激活之前。相比之下，Lester et al. 提出提示微调（prompt-tuning），在离散词元层面优化，在输入提示前前置一串可学习词元。两种方法都在大幅减少可学习参数数量、提升语言模型适配的计算与内存效率的同时展现了强劲性能。

主奇异值与奇异向量适配（PiSSA）[61] 是另一个较新的 PEFT 方法，试图缓解 LoRA 的慢收敛问题。PiSSA 用原矩阵的主成分初始化 LoRA 秩分解矩阵，在包括 GSM8K 与 MATH 在内的多个任务上比 LoRA 收敛更快、性能更强。

其中若干方法（尤其是 LoRA）已被专门改造用于把上下文中提供的知识蒸馏进语言模型参数。部分方法在下文各节描述，而本工作是前缀微调向长上下文任务的扩展。

#### B.1.2 参数高效适配器的组合与合并

许多工作探索了组合多个不同参数高效适配器（如 LoRA）的想法——把它们相加、拼接或使用动态专家混合 [116, 37, 94, 115, 97, 92, 30, 53]。例如，Huang et al. 提出 LoraHub，一个动态加权并组合多个语言模型适配器的框架 [37]。给定一组为不同上游任务训练的 LoRA 模块和一个带上下文示例的新未见任务，LoraHub 动态加权这些 LoRA 并为该任务组合出新的 LoRA 模块。类似地，Zhao et al. 提出为给定任务动态检索最相关语言模型 LoRA 的方法 [115]。

#### B.1.3 参数化知识注入

近期若干工作探索了把外部知识直接整合进模型参数的方法，称为参数化知识注入 [48, 60, 81, 15, 49]。据我们所知，这些研究与我们的工作在范围上最为接近。与我们的工作一样，它们处理参数化知识注入问题：如何把大型文本语料存储进语言模型的参数。其中一些使用简单的合成数据生成管线或上下文蒸馏目标。与我们的工作不同，这些研究没有强调参数化知识注入技术的内存缩减与吞吐优势。我们在下面指出其他差异。

Kujanpaa et al. 近期提出的一种参数化知识注入方法是提示蒸馏（prompt distillation）：一个能访问特权知识的教师模型生成问答对，再用蒸馏目标（即模仿教师的完整词元分布）为 student 模型（与教师模型相同但无法访问特权信息）训练 LoRA 适配器 [48]。这与我们的上下文蒸馏目标非常相似——我们也发现它优于下一词元预测。但与我们不同，Kujanpaa et al. 只训练单一大小（秩 1024）的 LoRA 适配器，且没有评估相对完整上下文学习的内存缩减。事实上，他们完全没有与长上下文 ICL 基线比较，而是聚焦于与 RAG 的比较。此外，他们评测的是一个相对简单的长上下文设置——SQuAD 段落的拼接 [73]——不像 MTOB 与 LongHealth 那样具有长程依赖或需要推理。

类似地，Mao et al. 提出长输入微调（Long Input Fine-tuning，LIFT），用语料重叠片段上的常规下一词元预测目标以及语料生成的问答对上的指令微调来微调语言模型。与我们不同，Mao et al. 发现合成问答对「收益极小，甚至可能因过拟合而损害性能」[60]。我们结论的差异可能因为：他们只生成十个合成样本，而我们生成数万个。此外，他们使用较弱的 ICL 基线（Llama 3 8B），其上下文只有 8k 词元，任何超过 8k 词元的上下文在送入 ICL 基线前都被截断。

一项关于深度上下文蒸馏的同期工作用合成数据与上下文蒸馏目标做知识注入 [15]。在该工作中，作者只报告 LoRA 适配器的性能，未探索前缀微调参数化。与我们的进一步差异是，他们的重点不在内存缩减或吞吐提升：只报告单一适配器大小（秩 16 LoRA 适配器）的性能，也不报告吞吐改进；该文强调的是方法的「即插即用」特性。

最后，Su et al. 提出参数化检索增强生成（Parametric RAG）：每份文档有对应的 LoRA 适配器，在由该文档、文档的改写版本以及从文档生成的问答对组成的增强数据集上训练。推理时用检索器确定相关文档并合并对应的 LoRA 适配器 [81]。该方法在包括 WikiMultihopQA 在内的多种任务上相对 RAG 展示了显著收益。

### B.2 与 Self-Study 相关的先前工作

#### B.2.1 自蒸馏与上下文蒸馏

自蒸馏是另一种把上下文中信息（如草稿、信息性指令）带来的性能增益内化进模型参数的方法。在 "Learning by Distilling Context" 中，作者通过先让模型以「[指令] + [任务输入]」为条件预测「[草稿] + [最终答案]」，再微调同一模型在只给定「[任务输入]」（不看「[指令」也不用「[草稿]」）时预测自己的「[最终答案]」，把上下文中带指令与草稿的模型蒸馏进参数 [80]。

#### B.2.2 合成数据生成

由于微调对高质量数据的普遍需求（例如配合上述方法使用），大量工作聚焦于生成高质量合成数据 [65] [1] [26] [74]。例如，Bonito 是一个微调用于生成合成数据的模型 [65]；MetaSynth 是 Riaz et al. 提出的用语言模型编排多个专家 LLM 做领域特定合成数据生成的方法 [74]。140 亿参数语言模型 Phi-4 的训练过程也纳入了大量合成生成的数据 [1]。合成数据与新的后训练技术相结合，使 Phi-4 在 STEM 问答任务上超越其教师模型，并在推理基准上以同等规模表现出色。这些工作展示了合成数据生成方法增强语言模型能力的潜力。

### B.3 缩减 KV 缓存的大小

在本节中，我们讨论缩减 KV 缓存大小的现有方法。

首先，在 §B.3.3 中，我们描述对多头注意力操作提出架构改动以缩减 KV 缓存内存占用的工作。接着在 §B.3.1 中，我们讨论提示压缩方法——它们通过把较长的输入嵌入序列转换为较短的序列来缩减 KV 缓存大小。这些方法可分为硬词元方法（从词表中输出离散词元）与软词元方法（输出不在词表中的新词元嵌入）。最后在 §B.3.2 中，我们描述 KV 缓存压缩方法。这些方法直接修改 KV 缓存中的键值矩阵。与提示压缩方法相比，它们表达能力更强，因为它们可以产生任何输入嵌入序列都无法产生的 KV 缓存。

我们提出的方法论依赖缓存微调（cache-tuning），可视为一种 KV 缓存压缩。

#### B.3.1 提示压缩

##### 硬词元提示压缩

一些工作旨在把较长文本转换为较短文本来缩减 KV 缓存大小 [42, 55, 21, 109, 70]。这些方法通常称为硬词元提示压缩方法，因为得到的 KV 缓存来自词表中的离散词元。与软词元方法相比，这些方法适用于黑盒 API 模型。

这些方法大致分为两类：过滤型与摘要型。过滤方法用自信息等启发式从原提示中删减文本。例如，LLMLingua 与 Selective-Context 用一个较小的 LLM 过滤长提示（如丢弃冗余词元），再传给主模型 [42, 55]。摘要方法把长提示改写为更少的词元 [21]。

##### 用适配 LLM 做软词元提示压缩

一条工作线上，研究者训练一个模型（通常是适配后的 LLM）把长提示压缩为更少的软词元 [19, 104, 28, 62, 72]。

例如，Autocompressors 与上下文自编码器（ICAE）是微调后能输出可用于软词元提示的嵌入的 LLM [19, 28]。Autocompressors 用全参数微调训练并利用递归策略生成软提示，而 ICAE 用 LoRA 训练并用单次前向传播生成软提示。近期方法 LLoCO 训练领域特定的 LoRA 适配器，使解码器能更好地利用 AutoCompressor 嵌入 [83]。这与 Cartridges 不同：LLoCO 的 LoRA 适配器是针对一个领域（如学术论文、新闻）训练的，而非针对特定文档。还有若干工作提出用辅助模型从长提示产生软词元 [28, 72]。Gisting 是另一种方法，与上述不同之处在于它用同一个 LLM 既压缩提示为软词元又生成回答 [62]。

##### 用梯度下降做软词元提示压缩

软词元也可以通过对输入词元嵌入做梯度下降优化来产生。这一称为提示微调（prompt tuning）的思想最初是为了让冻结的语言模型适配特定任务而提出 [51]。因此它是参数高效微调文献的重要部分，在 §B.1.1 中有更详细的讨论。此后，Li et al. 把前缀微调技术扩展到长上下文场景，提出前缀传播（prefix propagation）——让前缀以前面的隐藏状态为条件——在长文档任务上取得了优于前缀微调的性能 [53]。

#### B.3.2 KV 缓存压缩

##### 硬词元 KV 缓存压缩

受到「某些场景下少量键主导后续查询的注意力分数」这一观察的启发，若干工作提出了在生成期间动态丢弃键值的 KV 缓存逐出策略 [27, 114, 84, 67]。例如，H2O 基于历史注意力分数的滚动和从已生成词元中丢弃键值 [114]。类似地，SnapKV 基于提示末尾的一段查询窗口从提示词元中丢弃键值 [56]。

逐出方法的一个主要局限是一旦键被逐出便无法恢复。另一条工作线不永久逐出键，而是聚焦于从 KV 缓存向 SM 选择性加载键。这些工作虽未减少 KV 缓存的内存消耗，但能通过更好利用 GPU 内存带宽加速推理 [75, 84]。例如，Quest 方法在每个解码步估计关键词元并选择性加载到 SM [84]。

与硬词元提示压缩方法相比，KV 缓存压缩方法允许在注意力头粒度上细粒度控制。这意味着一个词元可以在一个注意力头中被丢弃而在另一个中保留。

##### 用合并做软词元 KV 缓存压缩

另一条工作线不逐出 KV 缓存中的词元，而是提出合并相似词元 [91, 112, 90, 58]。例如，Cache Merge（CaM）把标记为逐出的键改为合并，使用基于注意力的加权方案 [112]。Wang et al. 在此基础上基于余弦相似度把键状态聚类为「合并集」，并用高斯核加权方案合并集合内的状态——对与某个枢纽状态（选为总注意力分数最大的词元）更相似的状态加权更高 [91]。Wan et al. 以动态判别操作（D2O）扩展了这两项工作，在层与词元两个层面做优化：D2O 基于每层的注意力密度调整其 KV 缓存预算，并用指数移动平均机制动态判断某个先前丢弃的词元何时与保留词元足够相似以合并回来 [90]。这些工作都展示了可喜的结果：缓存大小缩减 50% 或更多时，在多个任务上性能与完整缓存相近或更优。不过仍有改进空间：这些方法在若干任务上仍无法匹配完整缓存性能，而且即便 50% 的缓存缩减对超大规模模型或超长上下文而言可能仍然过于昂贵。此外，这些工作未在长上下文场景下评估这些方法的有效性。

##### 用低秩投影做软词元 KV 缓存压缩

许多工作利用「KV 缓存呈现低秩结构」的观察来开发压缩方法 [105, 16, 110, 119, 77]。与基于合并的压缩方法类似，基于低秩适配的压缩方法在 50% 压缩下于多个任务取得与完整缓存相近或更优的性能，而进一步压缩则出现性能退化。

##### 用适配 LLM 做软词元 KV 缓存压缩

上文讨论了如何适配 LLM 以在给定长上下文时输出更短的软词元序列。类似地，也可以适配 LLM 在给定长上下文时输出更小的 KV 缓存。虽然相比对应的提示压缩途径探索较少，至少有一个已发表方法属于此类。在 KV-distill 中，作者给 LLM 的查询投影添加 LoRA 适配器，训练其产生能聚合先前词元信息的查询 [17]。适配器选择性地应用于部分词元，只有这些词元保留在 KV 缓存中。其思想是这些被选词元可以充当汇聚先前词元信息的槽（sink）。适配器用压缩与未压缩 KV 缓存之间的蒸馏目标训练。但与我们不同，KV-distill 不在测试时使用任何训练。

##### 用梯度下降做软词元 KV 缓存压缩

把 KV 缓存中的键值矩阵当作权重并用梯度下降训练的思想最早在前缀微调论文中讨论 [54]。在该工作中，该方法并未应用于长上下文，而是作为可应用于具有输入输出对训练集的参数高效微调方法，因此我们在 B.1.1 中更详细地讨论。此后，我们不知道有工作把该技术用于处理长上下文。

#### B.3.3 架构改动

许多工作提出了对原始多头注意力（MHA）操作 [89] 的架构改动以缩减 KV 缓存的内存占用。由于它们从根本上改变了架构，这些方法与使用标准 MHA 操作的预训练模型不能立即兼容。

这一方向最早的工作在注意力图中引入固定稀疏模式 [12, 20, 106]。例如，许多工作使用滑动窗口稀疏模式：每个词元只关注其周围固定窗口内的词元。这些方法缩减了 KV 缓存大小，因为只需在 KV 缓存中保留固定数量的词元。近期，一些大语言模型在部分层/头中采用了滑动窗口稀疏 [86]。

上述方法通过在词元层面引入稀疏性缩减缓存大小，另一类方法则改变注意力头的结构。多查询注意力（MQA）是最早的此类改动，使用多个查询头但只有一个键头与值头 [78]。MQA 大幅缩减了 KV 缓存大小，但可能导致模型表达能力显著下降。分组查询注意力（GQA）是 MQA 与 MHA 之间的折中，允许一组查询头关注单个键头与值头 [3]。许多前沿模型使用 GQA，包括我们实验中使用的 Llama 3 架构 [25, 41, 98]。近期还提出了其他若干架构改动，包括多头潜在注意力 [57] 与张量积注意力 [111]。

另一条工作线上，研究者观察到若去掉注意力机制中的 softmax（即线性化注意力算子），KV 缓存可以被固定大小矩阵 $K^{\top}V$ 忠实表示 [6]。这使我们能用一个大小与上下文长度无关的矩阵表示 KV 缓存。

事实上，大量工作聚焦于开发内存消耗固定的架构（即摒弃 KV 缓存的模型）。著名例子包括状态空间模型 [31]、RNN [8] 与其他线性注意力变体 [6, 100]。

先前工作表明，在控制计算量（即 FLOPs）的前提下，架构的内存消耗与模型执行召回密集任务的能力之间存在权衡 [6]。在此背景下，我们的工作表明：通过增加计算量（即 FLOPs），我们可以在不牺牲性能的情况下降低模型的内存消耗。在附录 E 中，我们提供把 Self-Study 与循环架构联系起来的初步理论分析。然而，未来工作应更深入地探索 Cartridges 与循环模型之间的关系。

与我们工作最相关的是近期的一些架构（如 Titans [11]、TTT [82]），它们使用恒定大小的内存对象（如线性注意力中那样）但施加类梯度下降的内存更新 [82, 101, 9, 11, 10]。与我们的工作一样，这些架构的动机是「梯度下降在把文本压缩进恒定空间方面非常有效」这一观察，并展示了在测试时对长上下文任务使用梯度下降的前景。与我们的工作不同，这些架构需要从头训练，尚未在大规模模型上得到验证，且在召回密集型任务上无法匹配注意力的质量 [6, 9]。

#### B.3.4 长上下文的编排

在本节中，我们描述通过编排对 LLM 的调用来管理长上下文的策略。例如，[76] 的方法涉及对上下文的各个块做摘要再合并这些摘要。类似地，PRISM [40] 把上下文视为块的序列，以结构化数据格式捕捉关键信息。MemGPT [69] 从操作系统获得灵感，引入了虚拟内存分页系统：当上下文长度逼近可用内存上限时，系统策略性地决定保留哪些信息。

#### B.3.5 合成数据生成

大量工作聚焦于生成合成训练数据 [65, 1, 26, 74]。例如，Bonito 是一个微调用于生成合成数据的模型 [65]；MetaSynth 是 Riaz et al. 提出的用语言模型编排多个专家 LLM 做领域特定合成数据生成的方法 [74]。140 亿参数语言模型 Phi-4 的训练过程也纳入了大量合成生成的数据 [1]。

## 附录 C 扩展方法描述

在本节中，我们详述用 Self-Study 训练 Cartridge 所用的种子提示与分块策略。

### C.1 Self-Study 种子提示

如算法 1 所讨论，我们用一个引发关于文档不同侧面对话的提示来为合成对话生成设定种子。对每段对话，我们随机采样以下函数之一并调用它来构造种子提示：

**结构化种子提示生成器**

```python
def structuring_seed_prompt(**kwargs):
    DATA_FORMATS = [
        "JSON",
        "YAML",
        "TOML",
        "INI",
        "XML",
        "plain text",
    ]

    data_format = random.choice(DATA_FORMATS)

    EXAMPLES = [
        (
            "Can you structure the information in {{subsection}} of {{document}} related to {{something specific}} "
            f"in the following format: {data_format}? "
            "Be sure to include precise information like any dates, times, names, and numerical values.'"
        ...
    ]

    example = random.choice(EXAMPLES)

    return (
        f"Please generate a single chat message instructing an LLM to structure the information in {data_format}. "
        "Output only the chat message itself and absolutely nothing else. "
        "Make sure it is clear what section and document you are asking about. "
        f"The message can follow the following template, filling in details from the corpus: \n\n'{example}'"
    )
```

**摘要种子提示生成器**

```python
def summarization_seed_prompt(**kwargs):
    prompts = [
        (
            "Please generate a single chat message instructing an LLM to summarize part of the corpus. "
            "Make sure the instruction is very explicit about the section of the corpus that you want to summarize. "
            "Include details (ids, names, titles, dates, etc.) that make it clear what you are asking about. "
        ),
        (
            "Please generate a single chat message instructing an LLM to summarize a section. "
            "Make sure the instruction is explicit about the section that should be summarized and the document it is from."
        ),
    ]
    prompt = random.choice(prompts)
    return prompt
```

**提问种子提示生成器**

```python
def question_seed_prompt(**kwargs):
    prompts = [
        (
            "Generate a question for an LLM that will test its knowledge of the information in the corpus above. "
            "In your question be sure to include details (ids, names, titles, dates, etc.) that make it clear what you are asking about. "
            "Output only a single question. Do NOT include any other text or explanation other than the question."
        ),
        (
            "Generate a message for an LLM that will test its knowledge of the information in the corpus above."
            "Be sure to include details (ids, names, titles, dates, etc.) in the question so that it can be answered without access to the corpus (i.e. closed-book setting). "
            "Output only a single question. Do NOT include any other text or explanation other than the question."
        ),
        (
            "You are helping to quiz a user about the information in the corpus. "
            "Please generate a question about the subsection of the corpus above. "
            "Be sure to include details (ids, names, titles, dates, etc.) in the question to make it clear what you are asking about. "
            "Answer only with the question, do not include any other text."
        ),
    ]
    prompt = random.choice(prompts)
    return prompt
```

**使用场景种子提示生成器**

```python
def use_case_seed_prompt(**kwargs):
    prompt = (
        "You are working to train a language model on the information in the following corpus. "
        "Your primary goal is to think about practical, real-world tasks or applications that someone could achieve using the knowledge contained within this corpus. "
        "Consider how a user might want to apply this information, not just recall it. "
        "After considering potential use cases, your task will be to generate a sample question that reflects one of these downstream applications. "
        "This question/instruction/task should be something a user, who has access to this corpus, might ask when trying to accomplish their specific goal. "
        "Output only a single question. Do NOT include any other text or explanation other than the question."
    )
    return prompt
```

**创意种子提示生成器**

```python
def creative_seed_prompt(**kwargs):
    prompt = [
        (
            "You are having a creative conversation inspired by the information in the corpus. "
            "Please generate a question for your conversation partner to start off the discussion. "
            "Answer only with the question, do not include any other text."
        ),
    ]
    return random.choice(prompt)
```

### C.2 Self-Study 分块

在 Self-Study 数据生成过程中，我们从输入语料 $\mathcal{C}$ 中抽取均匀随机的词元级块。生成种子提示时，通常在每个块 $\tilde{c}$ 前置一段相应的文字描述以为其提供语境。这一方式帮助模型聚焦语料的不同部分并生成多样的合成样本。具体的分块参数与描述按数据集定制：

- LongHealth：采样块的最小 512 词元、最大 4096 词元。伴随描述为：『Below is a section of a patient's medical record. It is part of a larger corpus of medical records for $N_{\text{patients}}$ different patients.』
- AMD/FinanceBench：使用 8192 词元的固定大小块。这些块前置的描述文字。
- MTOB：采样块的最小 512 词元、最大 4096 词元。所用描述为：『The following is an excerpt from a grammar book about the Kalamang language.』
- QASPER：按照我们的总体方法，采样块的最小 512 词元、最大 4096 词元。使用一段通用描述把块定位为研究论文节选，与 QASPER 数据集的性质一致。

## 附录 D 数据集

### D.1 GenConvo

为评测我们的方法处理长文档上多样化查询的能力，我们生成了 GenConvo 数据集。GenConvo 用 AMD 2022 年 10-K 文件（FinanceBench 语料库中的一份文档 [38]）创建。GenConvo 的主要目的是模拟用户可能要求模型在给定长文档时执行的广泛任务，从而测试模型的理解、推理与提取多样类型信息的能力。生成过程依赖 Claude Sonnet 3.7 [4]，流程如下：

1. 文档输入：把整个源文档（例如 AMD 2022 10-K，少于 200,000 词元，放得进模型上下文窗口）提供给 Claude Sonnet 3.7。
2. 问题生成：用一系列不同的提示模板（详见下文）来引出不同的推理轨迹（如事实召回、综合、多跳推理）以生成问题。对给定文档与每个提示模板，我们要求模型生成 16 个不重复的问题。这需要把完整文档内容连同具体的问题生成提示一起提供给模型。
3. 回答生成：随后，对每个生成的问题，再次以原始完整文档与该问题提示 Claude Sonnet 3.7 产生回答。这一流程确保回答立足于所提供的文档。

我们希望 GenConvo 提供一个超越简单事实检索的挑战性基准，评估模型在长上下文上深度理解与更复杂信息处理的能力。问题生成阶段使用了以下提示模板：

**事实提示模板**

Please generate a question to test someone's
ability to remember factual details from the document. The answer should be a few
tokens long and be a factual detail from the statement, such as a number, entity,
date, title, or name.
This question should not be common knowledge: instead, it should be something
that is only answerable via information in the document.

**知识提示模板**

Please generate a question that requires
combining information mentioned both inside and outside the document.
This question should require using a fact from the document and also a fact that
you are confident about, but is not mentioned in the document. For instance:
- What are the founding dates of the companies that got acquired this year?
This is a good question because the names of the acquired companies are
mentioned in the document and the founding dates are not mentioned.
- What is the name of the CEO's spouse? This is a good question because the
name of the CEO is mentioned in the document and the spouse's name is not
mentioned.
The answer should be a fact that is a few tokens long such as a number, entity,
date, title, or name.

**不相交提示模板**

Please generate a multi-hop question that
tests someone's ability to use factual information mentioned in at least two
very different sub-sections of the document.
This question shouldn't be a standard question about this kind of document.
Instead, it should ask about two particularly disconnected ideas, like
comparing information about the amount of owned space for the company
headquarters with the amount of dollars of estimated liability or comparing
the revenue number with the number of employees.
This question should also test one's ability to do retrieval: do not give
away part of the answer in the question. Ensure that for one to get the
correct answer to the question, they need to understand the document.
The answer should be a short: for example, a number, entity, date, title,
or name.

**综合提示模板**

Please generate a question that requires
synthesizing and aggregating information in the document.
For instance, you could ask someone to summarize a page of the document, list
all the key competitors mentioned in the document, or summarize the company's
business model.

**结构提示模板**

Please generate a question that requires
understanding the structure of the document.
This question should be more about the structure of the document, rather
than the precise statement details. For instance, you could ask someone
to list the titles of all the sections in the document, describe the
document structure, report the total number of pages, ask which section
amongst two sections comes first, or report the section with the largest
number of tables.

**创意提示模板**

Please generate a question about the
document to test someone's ability to comprehend the content of the document.
This question specifically should be focused on their ability to generalize
the information about the document to a strange question of sorts.
This question shouldn't be a standard question about this kind of document,
it should ask to do something abnormal and creative, like writing a poem
about a financial document.

**计数提示模板**

Please generate a question that requires
counting how frequently different events occur in the document.
This question should be about statistical properties of the document,
rather than the statement details. For instance, you could ask someone
to count the number of times the word "million" is mentioned or count
the length of the shortest section title.
The answer should be a number.

**推理提示模板**

Please generate a question that requires
mathematical reasoning over the values in the document.
This question should require going beyond the facts directly mentioned in the
statement, such as asking to compute the percentage increase in revenue
between two years, find the largest expense category, or calculate
difference in profit between two years.
The answer should be a number.

### D.2 LongHealth

LongHealth 是评估大型语言模型分析与解读长临床文本能力的基准 [2]。该基准由 20 份虚构临床病例报告（每份 5,090 至 6,754 词）与基于它们的 400 道选择题组成。

在我们的实验中，上下文 $\mathcal{C}$ 由一组 $n$ 位患者的报告构成。我们使用 $n=10$ 位患者，整组约 100k 词元，放得进 Llama 3 模型的上下文长度。

问题分为信息提取、否定与排序三类。

下面是一道排序题示例：

Please answer the question below about the following patient: ID patient_03, Name: Mr. John Williams, Birthday: 1956-08-08 00:00:00, Diagnosis: Multiple Myeloma
<question>

Mr. Williams received multiple radiologic examinations. In which order did she receive them?

</question>
<options>

CT Whole Body > MR Spine Scan > CT Spine Scan > PSMA-PET-CT Scan > CT Chest > CT Whole Body > Whole Body CT scan

Whole Body CT scan > CT Spine Scan > CT Whole Body > MR Spine Scan > CT Chest > PSMA-PET-CT Scan > CT Whole Body.

CT Whole Body > CT Whole Body > CT Chest > CT Chest > PSMA-PET-CT Scan > MR Spine Scan > CT Spine Scan > Whole Body CT scan > Chest X-ray

CT Chest > CT Spine Scan > CT Whole Body > Whole Body CT scan > PSMA-PET-CT Scan > MR Spine Scan > CT Whole Body

Whole Body CT scan > CT Spine Scan > CT Whole Body > MR Spine Scan > CT Chest > CT Whole Body > PSMA-PET-CT Scan

</options>
You should first think step by step. Then give your final answer exactly as it appears in the options. Your output should be in the following format:

<thinking> {{YOUR_THOUGHT_PROCESS}} </thinking>

<answer>

{YOUR_ANSWER}

</answer>

下面是一道否定题示例：

Please answer the question below about the following patient: ID patient_01, Name: Anna Sample, Birthday: 1970-01-01 00:00:00, Diagnosis: DLBCL
<question>

Which of these examinations were never performed in Mrs. Sample?

</question>
<options>

Bone marrow aspiration

CSF aspiration

MRI of the head

Pulmonary function testing Cardiac stress testing

</options>
You should first think step by step. Then give your final answer exactly as it appears in the options. Your output should be in the following format:

<thinking> {{YOUR_THOUGHT_PROCESS}} </thinking>

<answer>

{YOUR_ANSWER}

</answer>

### D.3 MTOB

单书机器翻译（Machine Translation from One Book，MTOB）基准测试大型语言模型学习英语与 Kalamang 之间翻译的能力——Kalamang 是一种几乎没有网络存在的低资源语言 [85]。核心任务主要依托一本全面的语法书与少量配套语言资源进行翻译（Kalamang 译英语、英语译 Kalamang）。本工作中我们聚焦 Kalamang 译英语。

MTOB 基准提供的源文档包括：

- 一本 Kalamang 语法书：全面的语法教科书，原始来源为 LaTeX 格式。该书详述 Kalamang 的音系、形态与句法。
- 双语词表（W）：带词性标注与英文释义的 Kalamang 词汇表。
- Kalamang-英语平行语料（S）：375 对 Kalamang-英语句子。

MTOB 作者为基线实验把语法教科书从原始 LaTeX 源预处理为若干纯文本切分。包括：

- $G^{m}$（中等长度块）：约 50k 词元的纯文本段，由概览章、语法书中的语素表与完整双语词表（W）组成。
- $G^{l}$（长块）：约 100k 词元的较大纯文本段，包含 MTOB 作者认为对翻译任务最重要的语法书章节。
- 完整纯文本教科书（G）：整本语法书的纯文本转换。

长块（$G^{l}$）、平行句集（S）与词表（W）的组合超出 Llama 3 模型的上下文窗口。我们用中等长度块 $G^{m}$ 与平行句表 $S$ 作为 ICL 基线的输入。

### D.4 QASPER

QASPER 是评估大型语言模型回答科学论文问题能力的基准 [23]。为构造一个类似 §2.2 所述设定的、具有挑战性的多查询长上下文场景，我们把 16 篇都与 QA NLP 模型相关的论文拼接成语料 $\mathcal{C}$。数据集中共有关于这 16 篇论文的 78 个问题，我们将其用作查询 $Q$。

由于该数据集只包含简短答案与含答案证据的金标准片段，我们用 GPT-4.1 把答案改写为更长、更对话式的格式，并在评测时将其作为目标。

## 附录 E 理论分析：注意力、线性注意力与 Cartridges 的关系

用自回归 Transformer 生成文本时，我们必须维护一个随输入与文本长度线性增长的 KV 缓存。在 §B.3.3 中，我们讨论了若干缩减 KV 缓存大小或彻底摒弃它的架构改动。特别地，用线性注意力生成文本时（如 [6]），我们只需在生成期间维护一个恒定大小的对象——KV 状态矩阵。

与线性注意力中的 KV 状态矩阵一样，Cartridges 消耗恒定的内存量（即其大小是超参数，可独立于输入长度设定）。但它们的更新方式不同于 KV 状态。本工作中，Cartridges 用 Self-Study（对合成生成数据做梯度下降）更新；而 KV 状态用线性注意力更新规则更新。

在本节中，我们将研究注意力、线性注意力与梯度下降应用于多查询关联召回（MQAR）问题 [5]——一个用于研究长上下文架构能力的流行合成基准任务——时的更新规则。特别地，我们考虑标准 MQAR 问题的一个键值对会重复出现的变体。首先，我们在输入键正交的受限情形下强调这些方法的更新规则之间的若干等价性。然后，在输入键处于 Johnson-Lindenstrauss 嵌入这一更具挑战性的情形下，我们给出一个分离结果：梯度下降更新规则能够精确求解一个线性注意力无法求解的 MQAR 问题。

这些理论结果为以下现象提供了直觉：恒定大小的 Cartridges 为何能在长上下文场景中匹配完整 KV 缓存的性能，而线性注意力架构一直难以做到。

### E.1 记号

所有向量均假定为行向量。

带括号的上标（如 ${\bm{k}}^{(1)}$）表示元素的时序属性。下标按惯例表示集合中的不同元素。

各变量的简要说明：

- $d$：模型（与词元）维度。
- $m$：不同键值对的数量。
- $n$：查询数量。
- $N$：流中键值对的数量。

### E.2 MQAR

我们定义多查询关联召回（MQAR）问题。

###### 定义 1.

存在键的宇宙：

$$
K\subset\mathbb{R}^{1\times d},
$$

与值的宇宙：

$$
V\subset\mathbb{R}^{1\times d}.
$$

###### 定义 2.

[5] 在 MQAR 问题中，输入为：

$$
({\bm{k}}^{(1)},{\bm{v}}^{(1)}),\ldots,({\bm{k}}^{(N)},{\bm{v}}^{(N)})\text{ where }({\bm{k}}^{(t)},{\bm{v}}^{(t)})\in K\times V\text{ for }1\leq t\leq N,
$$

其后是一组查询

$$
{\bm{q}}_{1},\ldots{\bm{q}}_{n}\text{ where }{\bm{q}}_{i}\in K\text{ for }1\leq i\leq n.
$$

然后对每个 $i\in[n]$，输出：

$$
\begin{cases}{\bm{v}}_{i^{*}}\text{ where }i^{*}=\max\{i\in[1,N]|{\bm{k}}_{i}={\bm{q}}_{j}\}\\ \bm{0}^{d}\text{ if no such }i\text{ exists.}\end{cases}
$$

### E.3 $m$-重复 MQAR

###### 定义 3.

$m$-重复 MQAR 是每个 $(K^{(t)},V^{(t)})\in S$ 的特殊情形，其中：

$$
S=\{({\bm{k}}_{1},{\bm{v}}_{1}),\ldots,({\bm{k}}_{m},{\bm{v}}_{m})\}.
$$

此外，${\bm{k}}_{i}$ 互不相同。

###### 定义 4.

为刻画这一点，$r_{i}^{(t)}$ 定义为 $({\bm{k}}_{i},{\bm{v}}_{i})$ 在时刻 $t$ 的流中出现的次数。

#### E.3.1 正交嵌入

首先，我们看所有限于正交键时的 MQAR 问题。

###### 定义 5.

我们称集合 $K$ 为正交的，若对所有 ${\bm{k}},{\bm{k}}^{\prime}\in K$：

$$
\langle{\bm{k}},{\bm{k}}^{\prime}\rangle=\begin{cases}0&\text{ if }{\bm{k}}\neq{\bm{k}}^{\prime}\\ 1&\text{ otherwise.}\end{cases}
$$

#### E.3.2 Johnson-Lindenstrauss 嵌入

接下来，我们看所有限于 JL 嵌入时的 MQAR 问题。

###### 定义 6.

设 $\epsilon>0$，我们称集合 $K$ 为 $\epsilon$-JL 的，若对所有 ${\bm{k}},{\bm{k}}^{\prime}\in K$：

$$
\langle{\bm{k}},{\bm{k}}^{\prime}\rangle=\begin{cases}[-\epsilon,\epsilon]&\text{ if }{\bm{k}}\neq{\bm{k}}^{\prime}\\ 1&\text{ otherwise.}\end{cases}
$$

### E.4 模型定义

下面我们描述三种不同的模型架构。尽管它们展现不同的性能与能力，但可以用一个关于 MQAR 问题的公共框架描述。

1. 状态（State）：模型如何存储键值对。
2. 更新规则（Update rule）：模型如何把新键值对纳入其状态。
3. 查询规则（Query rule）：模型如何用其状态应答一次值或查询的查找。

#### E.4.1 Transformer

1. 状态为：

$$
{\bm{W}}^{(t)}=({\bm{K}}^{(t)},{\bm{V}}^{(t)}),
$$

其中，

$$
{\bm{K}}^{(t)}\in\mathbb{R}^{t\times d},{\bm{V}}^{(t)}\in\mathbb{R}^{t\times d}.
$$

注意这会随上下文变长而消耗更多内存。

2. 更新规则为：

$$
{\bm{K}}^{(t+1)}={\bm{K}}^{(t)}\oplus{\bm{k}}^{(t+1)},{\bm{V}}^{(t+1)}={\bm{V}}^{(t)}\oplus{\bm{v}}^{(t+1)}
$$

3. 在查询 ${\bm{q}}\in K$ 上，返回：

$$
{\bm{q}}\left({\bm{K}}^{(t)}\right)^{\top}{\bm{V}}^{(t)}.
$$

这些规则定义了 MQAR 的 transformer 设定。

#### E.4.2 线性注意力

1. 状态：

$$
{\bm{W}}^{(t)}\in\mathbb{R}^{d\times d}.
$$

2. 更新规则定义为：

$$
{\bm{W}}^{(t+1)}={\bm{W}}^{(t)}+({\bm{k}}^{(t+1)})^{\top}({\bm{v}}^{(t+1)}).
$$

初始矩阵初始化为零，即 ${\bm{W}}^{(0)}=\bm{0}^{d\times d}$。

3. 在查询 $q$ 上，返回：

$$
{\bm{q}}{\bm{W}}^{(t)}.
$$

###### 引理 1.

[101] 若用损失函数 $-{\bm{k}}^{(t)}{\bm{W}}^{(t)}{\bm{v}}^{t}$ 做更新，会涌现线性注意力规则。

这里需要强调，我们不使用任何核函数的线性注意力。这些规则定义了 MQAR 的线性注意力设定。

###### 引理 2.

[101] 当使用梯度下降损失函数 $\frac{1}{2}||\bm{k}^{(t)}{\bm{W}}^{(t)}-{\bm{v}}^{(t)}||_{2}^{2}$ 时，涌现的更新规则为 ${\bm{W}}^{(t+1)}={\bm{W}}^{(t)}-\left({\bm{k}}^{(t)}\right)^{\top}{\bm{k}}^{(t)}{\bm{W}}^{(t)}+\left({\bm{k}}^{(t)}\right)^{\top}{\bm{v}}^{(t)}$。

###### 定义 7.

$$
\mathcal{L}=\frac{1}{2}||\bm{k}^{(t)}{\bm{W}}^{(t)}-{\bm{v}}^{(t)}||_{2}^{2}
$$

###### 证明.

一般地，梯度下降的更新规则为：

$$
{\bm{W}}^{(t+1)}={\bm{W}}^{(t)}-\eta\nabla_{{\bm{W}}^{(t)}}. \tag{4}
$$

对损失函数取梯度得：

$$
\begin{aligned}
\nabla_{{\bm{W}}}\frac{1}{2}||\bm{k}^{(t)}{\bm{W}}^{(t)}-{\bm{v}}^{(t)}||_{2}^{2} &=\left({\bm{k}}^{(t)}\right)^{\top}({\bm{k}}^{(t)}{\bm{W}}^{(t)}-{\bm{v}}^{(t)})\\
&=\left({\bm{k}}^{(t)}\right)^{\top}{\bm{k}}^{(t)}{\bm{W}}^{(t)}-\left({\bm{k}}^{(t)}\right)^{\top}{\bm{v}}^{(t)}.
\end{aligned}
$$

利用上式并取 $\eta=1$，我们由公式 4 得：

$$
\begin{aligned}
{\bm{W}}^{(t+1)} &={\bm{W}}^{(t)}-1\left(\left({\bm{k}}^{(t)}\right)^{\top}{\bm{k}}^{(t)}{\bm{W}}^{(t)}-\left({\bm{k}}^{(t)}\right)^{\top}{\bm{v}}^{(t)}\right)\\
&={\bm{W}}^{(t)}-\left({\bm{k}}^{(t)}\right)^{\top}{\bm{k}}^{(t)}{\bm{W}}^{(t)}+\left({\bm{k}}^{(t)}\right)^{\top}{\bm{v}}^{(t)}.
\end{aligned}
$$

∎

#### E.4.3 梯度下降

对缓存做梯度下降训练。我们考察该训练后的状态在某个输入上的能力。

1. 时刻 $t$ 的状态定义为：

$$
{\bm{W}}^{(t)}\in\mathbb{R}^{d\times d}.
$$

2. 由引理 2 得到的更新规则：

$$
{\bm{W}}^{(t+1)}={\bm{W}}^{(t)}-\left({\bm{k}}^{(t)}\right)^{\top}{\bm{k}}^{(t)}{\bm{W}}^{(t)}+\left({\bm{k}}^{(t)}\right)^{\top}{\bm{v}}^{(t)}.
$$

初始矩阵初始化为零，即 ${\bm{W}}^{(0)}=\bm{0}^{d\times d}$。

3. 在查询 $q$ 上，返回：

$$
{\bm{q}}{\bm{W}}^{(t)}.
$$

#### E.4.4 正交情形

我们现在看 $K$ 正交时三种模型在 $m$-重复 MQAR 上的表现。

**Transformer**

###### 引理 3.

对每个 MQAR 输入（甚至是 1-重复 MQAR 的输入），Transformer 的状态需要 $\Omega(Nd)$ 个参数。

直观上，每个时间步都会向状态追加 $d$ 个参数。在时刻 $t$，模型将有 $td$ 个参数。

**线性注意力**

###### 定理 1.

线性注意力可以对任意 $m\geq 1$ 与正交 $K$ 求解重复 MQAR（在用 ${\bm{k}}_{i}$ 查询 ${\bm{W}}^{(t)}$ 时产生 $r_{i}^{(t)}{\bm{v}}_{i}$，即差一个缩放因子），且所有键互异时只需 $O(d^{2})$ 个参数。

###### 证明.

我们先证明对任意 $t\geq 0$：

$$
{\bm{W}}^{(t)}=\sum_{i^{\prime}=1}^{m}r_{i^{\prime}}^{(t)}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}}. \tag{5}
$$

基础情形：初始时 ${\bm{W}}^{(0)}=\bm{0}^{d\times d}$。由此确实有：

$$
{\bm{W}}^{(0)}=\sum_{i^{\prime}=1}^{m}r_{i^{\prime}}^{(0)}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}},
$$

因为对所有 $i^{\prime}\in[m]$：

$$
r_{i^{\prime}}^{(0)}=0.
$$

归纳假设：设某个任意整数时刻 $t$ 的状态矩阵如所断言，即：

$$
{\bm{W}}^{(t)}=\sum_{i^{\prime}=1}^{m}r_{i^{\prime}}^{(t)}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}}.
$$

归纳步骤：
若 $({\bm{k}}^{(j)},{\bm{v}}^{(j)})$ 在时刻 $t+1$ 出现，更新规则为：

$$
\begin{aligned}
{\bm{W}}^{(t+1)} &={\bm{W}}^{(t)}+({\bm{k}}^{(t+1)})^{\top}{\bm{v}}^{(t)}\\
&={\bm{W}}^{(t)}+({\bm{k}}_{j})^{\top}{\bm{v}}_{j}
\end{aligned}
$$

由归纳假设，我们有：

$$
\begin{aligned}
{\bm{W}}^{(t+1)} &={\bm{W}}^{(t)}+{\bm{k}}_{j}({\bm{v}}_{j})^{\top}\\
&=\sum_{i^{\prime}=1}^{m}r_{i^{\prime}}^{(t)}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}}+{\bm{k}}_{j}({\bm{v}}_{j})^{\top}\\
&=\sum_{i^{\prime}=1}^{m}r_{i^{\prime}}^{(t+1)}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}}.
\end{aligned}
$$

最后一步来自：当 $({\bm{k}}^{(t+1)},{\bm{v}}^{(t+1)})=({\bm{k}}_{j},{\bm{v}}_{j})$ 时 $r_{j}^{(t+1)}=r_{j}^{(t)}+1$，且对所有 $i\neq j$ 有 $r_{i}^{(t+1)}=r_{i}^{(t)}$。
  
由此，公式 5 的证明由归纳法完成。

最后，在查询 ${\bm{k}}_{i}$ 上：

$$
\begin{aligned}
{\bm{k}}_{i}{\bm{W}}^{(t)} &={\bm{k}}_{i}\sum_{i^{\prime}=1}^{m}r_{i^{\prime}}^{(t)}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}}\\
&=\sum_{i^{\prime}=1}^{m}r_{i^{\prime}}^{(t)}{\bm{k}}_{i}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}}\\
&=\sum_{i^{\prime}\neq i}r_{i^{\prime}}^{(t)}{\bm{k}}_{i}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}}+r_{i}^{(t)}{\bm{k}}_{i}{\bm{k}}_{i}^{\top}{\bm{v}}_{i}\\
&=\sum_{i^{\prime}\neq i}r_{i^{\prime}}^{(t)}\cdot 0\cdot{\bm{v}}_{i^{\prime}}+r_{i}^{(t)}\cdot 1\cdot{\bm{v}}_{i}\\
&=r_{i}^{(t)}\cdot{\bm{v}}_{i},
\end{aligned}
$$

即为所需。上式中倒数第二个等号由定义 5 及所有 ${\bm{k}}_{i}$ 互异这一事实得出。

需要 $O(d^{2})$ 个参数，因为矩阵必须是 $d\times d$ 维。

∎

**梯度下降**

###### 定理 2.

梯度下降能够精确求解 $m$-重复 MQAR（在用 ${\bm{k}}_{i}$ 查询 ${\bm{W}}^{(t)}$ 时产生 ${\bm{v}}_{i}$），只需 $O(d^{2})$ 个参数。

###### 证明.

这里我们能处理重复，因为我们的更新规则包含一个「剥离」（peel）项。也就是说，它在用新值更新一个键之前先移除该键下当前存储的值。

我们用归纳法证明对所有 $t\geq 0$：

$$
{\bm{W}}^{(t)}=\sum_{i^{\prime}=1}^{m}\mathbb{1}_{r^{(t)}_{i^{\prime}}>0}\cdot{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}}.
$$

基础情形：初始时缓存矩阵全为零。由此自然有：

$$
{\bm{W}}^{(0)}=\sum_{i^{\prime}=1}^{m}0\cdot{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}},
$$

因为对所有 $i^{\prime}$：

$$
r^{(0)}_{i^{\prime}}=0.
$$

归纳假设：设在某个任意时刻 $t$，我们有：

$$
{\bm{W}}^{(t)}=\sum_{i^{\prime}}^{m}\mathbb{1}_{r^{(t)}_{i^{\prime}>0}}\cdot{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}}
$$

归纳步骤：
若 $({\bm{k}}_{\ell},{\bm{v}}_{\ell})$ 在时刻 $t+1$ 出现，更新为：

$$
\begin{aligned}
\sum_{i=1}^{m}\mathbb{1}_{r^{(t+1)}_{i>0}}{\bm{k}}_{i}^{\top}{\bm{v}}_{i} &=\left(\sum_{i^{\prime}=1}^{m}\mathbb{1}_{r^{(t)}_{i^{\prime}>0}}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}}\right)-\left(\sum_{i^{\prime}=1}^{m}\mathbb{1}_{r^{(t)}_{i^{\prime}>0}}{\bm{k}}_{\ell}^{\top}{\bm{k}}_{\ell}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}}\right)+{\bm{k}}_{\ell}^{\top}{\bm{v}}_{\ell}\\
&\quad\text{由于其他内积均为 0，第二项化简为只剥离与 } {\bm{k}}_{\ell} \text{ 相关的项（若存在），}\\
&=\left(\sum_{i^{\prime}=1}^{m}\mathbb{1}_{r^{(t)}_{i^{\prime}>0}}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}}\right)-\left(\mathbb{1}_{r^{(t)}_{\ell>0}}\cdot{\bm{k}}_{\ell}^{\top}{\bm{v}}_{\ell}\right)+{\bm{k}}_{\ell}^{\top}{\bm{v}}_{\ell}\\
&=\left(\sum_{i^{\prime}\neq\ell}^{m}\mathbb{1}_{r^{(t)}_{i^{\prime}>0}}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}}\right)+{\bm{k}}_{\ell}^{\top}{\bm{v}}_{\ell}
\end{aligned}
$$

这把与 ${\bm{k}}_{\ell}$ 关联的值替换为新值，同时保持其他一切不变。这正是我们想要的形式，因为只有当键是新键时我们才想添加它。

最后，在查询 ${\bm{k}}_{i}$ 上：

$$
\begin{aligned}
{\bm{k}}_{i}\cdot{\bm{W}}^{(t)} &={\bm{k}}_{i}\cdot\left(\sum_{i^{\prime}=1}^{m}\mathbb{1}_{r^{(t)}_{i^{\prime}>0}}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}}\right)\\
&=\left(\sum_{i^{\prime}=1}^{m}\mathbb{1}_{r^{(t)}_{i^{\prime}>0}}{\bm{k}}_{i}\cdot{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{i^{\prime}}\right)\\
&=\mathbb{1}_{r^{(t)}_{i>0}}\cdot 1\cdot{\bm{v}}_{i}\ \\
&=\mathbb{1}_{r^{(t)}_{i>0}}\cdot{\bm{v}}_{i}\
\end{aligned}
$$

同样，一个 $d\times d$ 维矩阵可以存储 $d$ 个正交向量。因此这需要 $O(d^{2})$ 个参数。

∎

#### E.4.5 JL 嵌入

我们现在看 $K$ 为 $\epsilon$-JL 时三种模型在 $m$-重复 MQAR 上的表现。

**Transformer**

###### 引理 4.

对每个 MQAR 输入（甚至是 1-重复 MQAR 的输入），Transformer 的状态需要 $\Omega(Nd)$ 个参数。

我们注意到，当 $K$ 为 $\epsilon$-JL 时，查询规则 ${\bm{k}}_{i}{\bm{W}}^{(t)}$ 不再可能得到精确答案。因此我们需要加一个解码步骤。

###### 定义 8.

输出解码步骤为 ${\bm{v}}_{i^{*}}$，其中：

$$
i^{*}=\arg\max_{i^{\prime}\in[m]}\langle{\bm{v}}_{i^{\prime}},{\bm{k}}_{i}{\bm{W}}^{(t)}\rangle.
$$

###### 定义 9.

对所有 $i,j\in[m]$，定义：

$$
{\epsilon}_{i,j}=\langle{\bm{k}}_{i},{\bm{k}}_{j}\rangle.
$$

**线性注意力**

###### 定理 3.

线性注意力（加上定义 8 的解码）无法求解 2-重复 MQAR（即使每个 ${\bm{v}}_{i}$ 为 one-hot 编码），除非 $K$ 是 $\omega\left(\frac{1}{N}\right)$-JL 的。

###### 证明.

由于不同键之间存在一致性（agreeance），查询键 $i$ 时，返回的除正确答案外还有来自其他键的噪声。虽然我们可以容忍一些误差，但该误差随模型见过某个键的次数增长。这使其不适用于更长的上下文或有很多重复的上下文。

首先注意，定理 1 中的基础情形公式 5 仍然成立。一般而言，这对所有 $K$ 都成立。

具体地，在查询 ${\bm{k}}_{1}$ 上我们有：

$$
{\bm{k}}_{1}{\bm{W}}^{(t)}=r_{1}^{(t)}\langle{\bm{k}}_{1},{\bm{k}}_{1}\rangle{\bm{v}}_{1}+r_{2}^{(t)}\langle{\bm{k}}_{1},{\bm{k}}_{2}\rangle{\bm{v}}_{2} =r_{1}^{(t)}{\bm{v}}_{1}+r_{2}^{(t)}{\epsilon}_{1,2}{\bm{v}}_{2}.
$$

现在，考虑一个 2-重复 MQAR 的输入使得

$$
r_{1}^{(t)}<r_{2}^{(t)}{\epsilon}_{1,2}.
$$

注意此时：

$$
r_{1}^{(t)}=\langle{\bm{v}}_{1},{\bm{k}}_{1}{\bm{W}}^{(t)}\rangle<\langle{\bm{v}}_{2},{\bm{k}}_{1}{\bm{W}}^{(t)}\rangle=r_{2}^{(t)}{\epsilon}_{1,2}
$$

因此我们会输出 ${\bm{v}}_{2}$ 而非 ${\bm{v}}_{1}$。

若嵌入是 $\omega(\frac{1}{N})$-JL 的，重复次数就无法克服 $\epsilon$ 值。

∎

**梯度下降**

###### 定理 4.

梯度下降（加上定义 8 的解码）能够精确求解 $m$-重复 MQAR（$O(d^{2})$ 个参数），对 $\epsilon$-JL 的 $K$，只要 $\epsilon\leq\frac{1}{m^{2}(m-1)}$ 且 $\alpha<\frac{m-1}{m+1}$。

###### 证明.

我们定义：

$$
C_{i,j}^{(t)}
$$

为 ${\bm{W}}^{(t)}$ 中与 ${\bm{k}}_{i}^{\top}{\bm{v}}_{j}$ 关联的系数。具体地，设

$$
{\bm{W}}^{(t)}=\sum_{i=1}^{m}\sum_{j=1}^{m}C_{i,j}^{(t)}{\bm{k}}_{i}^{\top}{\bm{v}}_{j} \tag{6}
$$

我们用归纳法证明：

$$
C_{i,j}^{(t)}=\mathbb{1}_{({\bm{k}}_{i},{\bm{v}}_{j})\text{ has occurred}}+\Delta^{(t)}_{i,j} \tag{7}
$$

其中，

$$
\left|\Delta_{i,j}^{(t)}\right|\leq\sum_{a=1}^{t}((m-1)\epsilon)^{a}. \tag{8}
$$

基础情形：初始时状态全为零。由此自然有所有 $C_{i,j}^{(t)}$ 为零。即公式 7 中：

$$
\Delta_{i,j}=0.
$$

归纳假设：设某个时刻 $t$ 与 $1\leq i,j\leq m$：

$$
C_{i,j}^{(t)}=\mathbb{1}_{({\bm{k}}_{i},{\bm{v}}_{j})\text{ has occurred}}+\Delta^{(t)}_{i,j},
$$

其中 $\Delta_{i,j}^{(t)}$ 满足公式 8。

归纳步骤：
若时刻 $t+1$ 给定 $({\bm{k}}_{\ell},{\bm{v}}_{\ell})$，由公式 6，更新形如：

$$
\begin{aligned}
{\bm{W}}^{(t+1)} &=\sum_{i=1}^{m}\sum_{j=1}^{m}C_{i,j}^{(t+1)}{\bm{k}}_{i}^{\top}{\bm{v}}_{j}\\
&=\sum_{i^{\prime}=1}^{m}\sum_{j^{\prime}=1}^{m}C_{i^{\prime},j^{\prime}}^{(t)}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{j^{\prime}}-\left(\sum_{i^{\prime}=1}^{m}\sum_{j^{\prime}=1}^{m}C_{i^{\prime},j^{\prime}}^{(t)}{\bm{k}}_{\ell}^{\top}{\bm{k}}_{\ell}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{j^{\prime}}\right)+{\bm{k}}_{\ell}^{\top}{\bm{v}}_{\ell}\\
&=\sum_{i^{\prime}=1}^{m}\sum_{j^{\prime}=1}^{m}C_{i^{\prime},j^{\prime}}^{(t)}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{j^{\prime}}-\left(\sum_{i^{\prime}=1}^{m}\sum_{j^{\prime}=1}^{m}{\epsilon}_{\ell,i^{\prime}}C_{i^{\prime},j^{\prime}}^{(t)}{\bm{k}}_{\ell}^{\top}{\bm{v}}_{j^{\prime}}\right)+{\bm{k}}_{\ell}^{\top}{\bm{v}}_{\ell}\\
&\quad\text{改变求和的结合顺序，}\\
&=\sum_{i^{\prime}=1}^{m}\sum_{j^{\prime}=1}^{m}C_{i^{\prime},j^{\prime}}^{(t)}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{j^{\prime}}-\left(\sum_{j^{\prime}=1}^{m}\left(\sum_{i^{\prime}=1}^{m}{\epsilon}_{\ell,i^{\prime}}C_{i^{\prime},j^{\prime}}^{(t)}\right){\bm{k}}_{\ell}^{\top}{\bm{v}}_{j^{\prime}}\right)+{\bm{k}}_{\ell}^{\top}{\bm{v}}_{\ell}\\
&\quad\text{这里把 } i^{\prime}=\ell \text{ 与 } i^{\prime}\neq\ell \text{ 的第一项分开，}\\
&=\sum_{i^{\prime}\neq\ell}^{m}\sum_{j^{\prime}=1}^{m}C_{i^{\prime},j^{\prime}}^{(t)}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{j^{\prime}}+\sum_{j^{\prime}=1}^{m}C_{\ell,j^{\prime}}^{(t)}{\bm{k}}_{\ell}^{\top}{\bm{v}}_{j^{\prime}}-\left(\sum_{j^{\prime}=1}^{m}\left(\sum_{i^{\prime}=1}^{m}{\epsilon}_{\ell,i^{\prime}}C_{i^{\prime},j^{\prime}}^{(t)}\right){\bm{k}}_{\ell}^{\top}{\bm{v}}_{j^{\prime}}\right)+{\bm{k}}_{\ell}^{\top}{\bm{v}}_{\ell}\\
&\quad\text{这里把 } i^{\prime}=\ell \text{ 与 } i^{\prime}\neq\ell \text{ 的第一项分开，}\\
&=\sum_{i^{\prime}\neq\ell}^{m}\sum_{j^{\prime}=1}^{m}C_{i^{\prime},j^{\prime}}^{(t)}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{j^{\prime}}+\sum_{j^{\prime}=1}^{m}C_{\ell,j^{\prime}}^{(t)}{\bm{k}}_{\ell}^{\top}{\bm{v}}_{j^{\prime}}-\left(\sum_{j^{\prime}=1}^{m}{\epsilon}_{\ell,\ell}C_{\ell,j^{\prime}}^{(t)}{\bm{k}}_{\ell}^{\top}{\bm{v}}_{j^{\prime}}\right)-\left(\sum_{j^{\prime}=1}^{m}\left(\sum_{i^{\prime}\neq\ell}{\epsilon}_{\ell,i^{\prime}}C_{i^{\prime},j^{\prime}}^{(t)}\right){\bm{k}}_{\ell}^{\top}{\bm{v}}_{j^{\prime}}\right)+{\bm{k}}_{\ell}^{\top}{\bm{v}}_{\ell}\\
&\quad\text{去掉 } {\epsilon}_{j,j}\text{，}\\
&=\sum_{i^{\prime}\neq\ell}^{m}\sum_{j^{\prime}=1}^{m}C_{i^{\prime},j^{\prime}}^{(t)}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{j^{\prime}}+\sum_{j^{\prime}=1}^{m}C_{\ell,j^{\prime}}^{(t)}{\bm{k}}_{\ell}^{\top}{\bm{v}}_{j^{\prime}}-\sum_{j^{\prime}=1}^{m}C_{\ell,j^{\prime}}^{(t)}{\bm{k}}_{\ell}^{\top}{\bm{v}}_{j^{\prime}}-\left(\sum_{j^{\prime}=1}^{m}\left(\sum_{i^{\prime}\neq\ell}{\epsilon}_{\ell,i^{\prime}}C_{i^{\prime},j^{\prime}}^{(t)}\right){\bm{k}}_{\ell}^{\top}{\bm{v}}_{j^{\prime}}\right)+{\bm{k}}_{\ell}^{\top}{\bm{v}}_{\ell}\\
&\quad\text{消去相同项，}\\
&=\sum_{i^{\prime}\neq\ell}^{m}\sum_{j^{\prime}=1}^{m}C_{i^{\prime},j^{\prime}}^{(t)}{\bm{k}}_{i^{\prime}}^{\top}{\bm{v}}_{j^{\prime}}-\left(\sum_{j^{\prime}=1}^{m}\left(\sum_{i^{\prime}\neq\ell}{\epsilon}_{\ell,i^{\prime}}C_{i^{\prime},j^{\prime}}^{(t)}\right){\bm{k}}_{\ell}^{\top}{\bm{v}}_{j^{\prime}}\right)+{\bm{k}}_{\ell}^{\top}{\bm{v}}_{\ell}.
\end{aligned}
$$

据此我们可以看到：

$$
C_{i,j}^{(t+1)} =\begin{cases}C_{i,j}^{(t)}&\text{ if }\ell\neq i\\ -\displaystyle\sum_{i^{\prime}\neq\ell}{\epsilon}_{\ell,i^{\prime}}C_{i^{\prime},j}^{(t)}+\mathbb{1}_{j=\ell}&\text{ if }\ell=i\end{cases}.
$$

于是，若 $i\neq\ell$，我们有：

$$
C_{i,j}^{(t+1)}=C_{i,j}^{(t)},
$$

对 $i\neq\ell$ 成立。归纳命题对这些对成立。现在考虑 $C_{\ell,j}^{(t+1)}$。若 $\ell=j$ 则：

$$
C_{\ell,\ell}^{(t+1)}=1+\Delta_{\ell,\ell}^{(t+1)}=\sum_{i^{\prime}\neq\ell}{\epsilon}_{\ell,i^{\prime}}C_{i^{\prime},j}^{(t)}+1
$$

并注意由三角不等式与定义 6：

$$
\begin{aligned}
\left|\Delta_{\ell,\ell}^{(t+1)}\right| &\leq\epsilon\sum_{i^{\prime}\neq\ell}\left|C_{i^{\prime},\ell}^{(t)}\right|\\
&\quad\text{由归纳假设，}\\
&\leq\epsilon\sum_{i^{\prime}\neq\ell}(1+\sum_{a=1}^{t}((m-1)\epsilon)^{a})\\
&=((m-1)\epsilon)(1+\sum_{a=1}^{t}((m-1)\epsilon)^{a})\\
&=(\sum_{a=1}^{t+1}((m-1)\epsilon)^{a}),
\end{aligned}
$$

即为所需。

然后对 $j\neq\ell$，我们有：

$$
\begin{aligned}
\left|\Delta^{(t+1)}_{j,\ell}\right| &=\left|C_{i,j}^{(t+1)}\right|\\
&=\left|\sum_{i^{\prime}\neq\ell}{\epsilon}_{\ell,i^{\prime}}C_{i^{\prime},j}^{(t)}\right|
\end{aligned}
$$

$\Delta_{\ell,j}^{(t)}$ 的界定与 $\ell=j$ 情形类似。

至此我们完成了关于误差项的归纳证明。

若我们设：

$$
\epsilon<\frac{1}{m^{2}(m-1)},
$$

则得到如下界：

$$
\Delta_{i,j}^{(t)} \leq\sum_{a=1}^{t}((m-1)\epsilon)^{a} \tag{9}
$$

$$
\leq\frac{(m-1)\epsilon}{1-(m-1)\epsilon} \tag{10}
$$

$$
<\frac{1}{m^{2}-1} \tag{11}
$$

在下一步之前，我们必须界定：

$$
\left|\langle{\bm{v}}_{i},{\bm{v}}_{j}\rangle\right|\leq\alpha \tag{12}
$$

对以 ${\bm{k}}_{i}$ 的查询，假设我们之前见过 ${\bm{k}}_{i}$，得到：

$$
{\bm{k}}_{i}\cdot{\bm{W}}^{(t)} ={\bm{v}}_{i}+\sum_{j^{\prime}\neq i}\Delta_{i,j^{\prime}}^{(t)}{\bm{v}}_{j^{\prime}}
$$

现在做解码步骤，对任意 ${\bm{v}}_{j}$ 我们得到：

$$
\langle{\bm{v}}_{j},{\bm{k}}_{i}\cdot{\bm{W}}^{(t)}\rangle =\langle{\bm{v}}_{j},{\bm{v}}_{i}\rangle+\langle{\bm{v}}_{j},\sum_{j^{\prime}\neq i}\Delta_{i,j^{\prime}}{\bm{v}}_{j^{\prime}}\rangle
$$

对 $i=j$ 的情形：

$$
\langle{\bm{v}}_{i},{\bm{k}}_{i}\cdot{\bm{W}}^{(t)}\rangle =1+\langle{\bm{v}}_{i},\sum_{j^{\prime}\neq i}\Delta_{i,j^{\prime}}{\bm{v}}_{j^{\prime}}\rangle \geq 1-\frac{1}{m+1}\alpha.
$$

这由公式 11 与公式 12 得出。

对 $i\neq j$ 的情形：

$$
\langle{\bm{v}}_{j},{\bm{k}}_{i}\cdot{\bm{W}}^{(t)}\rangle =\langle{\bm{v}}_{i},{\bm{v}}_{j}\rangle+\langle{\bm{v}}_{j},\sum_{j^{\prime}\neq i}\Delta_{i,j^{\prime}}{\bm{v}}_{j^{\prime}}\rangle \leq\alpha+\frac{1}{m+1}\alpha
$$

这由公式 11 与公式 12 得出。

因此，当 $\alpha<\frac{m-1}{m+1}$ 时我们总能选中正确的值。

∎
