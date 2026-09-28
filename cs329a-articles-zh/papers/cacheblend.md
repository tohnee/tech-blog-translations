---
title: "CacheBlend：面向 RAG 的高效大模型服务（缓存知识融合）"
title_en: "CacheBlend: Fast Large Language Model Serving for RAG with Cached Knowledge Fusion"
arxiv: 2405.16444
source: https://arxiv.org/abs/2405.16444
crawled: 2026-09-23
translated: 2026-09-23
---

# CacheBlend：面向 RAG 的高效大模型服务（缓存知识融合）

> 原文：[CacheBlend: Fast Large Language Model Serving for RAG with Cached Knowledge Fusion](https://arxiv.org/abs/2405.16444) · Stanford CS329A 指定阅读

会议：第二十届欧洲计算机系统会议（EuroSys '25），2025 年 3 月 30 日–4 月 3 日，荷兰鹿特丹。DOI：[10.1145/3689031.3696098](https://doi.org/10.1145/3689031.3696098)。ISBN：979-8-4007-1196-1/25/03。CCS 分类：计算方法论 自然语言处理；网络 云计算；信息系统 数据管理系统。

Jiayi Yao（芝加哥大学 / 香港中文大学（深圳））、
Hanchen Li（芝加哥大学）、
Yuhan Liu（芝加哥大学）、
Siddhant Ray（芝加哥大学）、
Yihua Cheng（芝加哥大学）、
Qizheng Zhang（斯坦福大学）、
Kuntai Du（芝加哥大学）、
Shan Lu（微软研究院 / 芝加哥大学）
与 Junchen Jiang（芝加哥大学）

###### 摘要

大型语言模型（LLM）常常会在输入中纳入多个文本块（text chunk），以提供必要的上下文。为了加速长 LLM 输入的预填充（prefill），可以预先计算某段文本的 KV 缓存，并在该文本作为另一条 LLM 输入的前缀被复用时直接复用这份 KV 缓存。然而，被复用的文本块并不总是位于输入的前缀位置，这使得预计算的 KV 缓存无法直接使用，因为它们忽略了该文本与其前面文本之间的交叉注意力（cross-attention）。因此，复用 KV 缓存所带来的收益在很大程度上仍未实现。

本文只解决一个挑战：当一条 LLM 输入包含多个文本块时，如何快速融合它们各自预计算的 KV 缓存，从而达到与昂贵的完全预填充（即不复用 KV 缓存）相同的生成质量？这一挑战自然出现在检索增强生成（RAG）中——输入由多条检索到的文本作为上下文补充而成。我们提出 CacheBlend，一种无论是否位于前缀位置都复用预计算 KV 缓存的方案，它选择性地重计算一小部分词元的 KV 值，以部分更新每份被复用的 KV 缓存。与此同时，重计算部分词元带来的少量额外延迟可以与同一作业内的 KV 缓存读取过程流水线化，使 CacheBlend 能够把 KV 缓存存储在容量更大但更慢的设备上，同时在读取时不增加推理延迟。通过在三种不同规模的开源 LLM 和四个不同任务的流行基准数据集上将 CacheBlend 与最先进的 KV 缓存复用方案进行比较，我们表明 CacheBlend 相对完全 KV 重计算将首词元延迟（TTFT）降低了 2.2–3.3×，将推理吞吐量提升了 2.8–5×，且不牺牲生成质量。代码已开源于 <https://github.com/LMCache/LMCache>。

###### 关键词：

Large Language Models, KV Cache, Retrieval-Augmented-Generation

## 1 引言

凭借出色的能力，大型语言模型（LLM）被广泛用于个人助理、AI 医疗和问答系统 [4, 1, 3, 9]。为确保回复的高质量与一致性，应用常常在用户查询之外补充额外文本，以提供领域知识或用户特有信息等必要上下文。一个典型的例子是检索增强生成（RAG）：用户查询会被前置上从数据库中检索到的多个文本块，共同构成 LLM 输入。

然而，这些上下文文本块会显著拖慢 LLM 推理。原因在于，在生成任何词元之前，LLM 首先要通过预填充（prefill）处理整条 LLM 输入以产生 KV 缓存——即与每个输入词元相关联的张量拼接，它编码了该词元对其前面词元的「注意力」。因此，预填充延迟决定了首词元时间（TTFT）。我们将其称为完全 KV 重计算（图 1(a)）。尽管已有大量优化，预填充的延迟与计算量仍随输入长度超线性增长，很容易拖慢服务，尤其是在长 LLM 输入（例如 RAG 场景）下 [60, 11, 53]。

图 1. 对比完全 KV 重计算、前缀缓存、完全 KV 复用与 CacheBlend 的选择性 KV 重计算。

那么，我们该如何加速 LLM 输入的预填充？近期的优化利用了这样一个事实：相同的上下文文本常常被不同的 LLM 输入复用。它们将这些文本的 KV 缓存预计算一次，并复用存储的 KV 缓存，以避免在这些被复用的文本上重复预填充。

**现有方法的局限：** 目前有两种 KV 缓存复用途径，但都存在局限。

第一，前缀缓存（prefix caching）只存储并复用 LLM 输入前缀部分的 KV 缓存 [42, 59, 36, 33, 41]（图 1(b)）。由于前缀的 KV 缓存不受后续文本影响，前缀缓存不会损害生成质量。然而，RAG 等许多应用会在 LLM 输入中纳入多个而非一个文本块，以提供全部必要上下文、确保良好的回复质量。于是只有第一个文本块是前缀，其他被复用文本的 KV 缓存无法被复用。结果，当输入由许多被复用的文本块组成时，前缀缓存的速度几乎与完全 KV 重计算一样慢。

第二，完全 KV 复用（full KV reuse）旨在弥补这一缺点（图 1(c)）。当被复用文本不在输入前缀位置时，它仍然复用其 KV 缓存，只是调整其位置编码，使 LLM 生成仍有意义的输出 [24]。然而，这种方法忽略了重要的交叉注意力——即一个文本块内的词元与其前面各文本块中词元之间的注意力。交叉注意力信息无法被预先计算，因为前面的文本块事先未知。可是，对于天然需要联合理解来自多个文本块信息（例如关于地理的文本块与关于政治的文本块）的查询（如地缘政治类问题），交叉注意力对回答可能至关重要。§3.3 给出了具体例子来说明前缀缓存与模块化缓存何时并不够用。

**我们的方法：** 本文只处理一个挑战：当一条 LLM 输入包含多个文本块时，如何快速融合它们各自预计算的 KV 缓存，以达到与昂贵完全预填充相同的生成质量？换言之，我们希望兼得完全 KV 复用的速度与完全 KV 重计算的生成质量。

我们提出 CacheBlend，一个融合多份预计算 KV 缓存的系统——无论是否处于前缀位置——其做法是依据具体 LLM 输入中前面的文本，选择性地重计算一小部分词元的 KV 缓存。我们称之为选择性 KV 重计算（selective KV recompute，图 1(d)）。总体而言，选择性 KV 重计算仍以传统的逐层方式对输入文本执行预填充；但在每一层，它只更新一小部分词元的 KV，同时复用其余词元的 KV。

与完全 KV 重计算相比，根据我们的经验，不到 15% 的更新比例通常就能生成同等质量的回复。只需更新一小部分 KV 的更深层原因在于注意力矩阵的稀疏性（见 §4.3）。

与完全 KV 复用相比，CacheBlend 以少量额外的 KV 更新换来了更高的生成质量。此外，这点少量额外计算并不会增加推理延迟，因为 CacheBlend 把一层的部分 KV 更新与下一层 KV 缓存取入 GPU 显存的过程并行化。这种流水线化使 CacheBlend 能够把 KV 缓存存放在较慢的非易失设备（如磁盘）上而不带来额外延迟，从而可以存储和复用更多 KV 缓存。

为定位我们的贡献：CacheBlend 使一条 LLM 输入中多个文本块的 KV 缓存复用成为可能，且不损害生成质量。这与近期降低 KV 缓存存储大小 [58, 43, 42, 28, 45, 35] 和优化 KV 缓存访问模式 [59, 33] 的工作互为补充。

我们在 vLLM 之上实现了 CacheBlend，并在三种不同规模的开源 LLM 与两个 LLM 任务（RAG 与问答）的三个流行基准数据集上，将 CacheBlend 与最先进的 KV 缓存复用方案进行了比较。结果表明：与前缀缓存相比，CacheBlend 将首词元延迟（TTFT）降低 2.2–3.3×，推理吞吐量提升 2.8–5×，且不牺牲生成质量、不增加存储成本。与完全 KV 复用相比，CacheBlend 的 TTFT 几乎相同，但在问答任务上 F1 分数绝对值高 0.1–0.2，在摘要任务上 Rouge-L 分数绝对值高 0.03–0.25。

## 2 背景

如今的大多数 LLM 服务都使用 transformer [52, 13, 16]。接收输入词元后，LLM 首先用预填充阶段（稍后解释）把词元变换为键（K）向量与值（V）向量，即 KV 缓存。预填充完成后，LLM 随后基于当前 KV 缓存迭代地解码（生成）下一个词元，并将新词元的新 K、V 向量追加进 KV 缓存以供下一轮迭代使用。

预填充阶段逐层计算 KV 缓存。每层上，输入词元的嵌入首先被变换为查询（Q）、键（K）、值（V）向量，其中 K 与 V 向量构成该层的 KV 缓存。然后 LLM 将 Q 与 K 向量相乘得到注意力矩阵——即每个词元对其前面词元的注意力——再将（归一化并掩码后的）注意力矩阵与 V 向量做另一次点积。所得向量经过多层神经网络，得到词元在下一层的嵌入。

当某个前缀的 KV 缓存可用时，预填充阶段在每层只需计算前向注意力矩阵（后缀词元与前缀词元之间），它直接影响生成的词元。

预填充阶段可能很慢，尤其是长输入。例如，在四千词元的输入（RAG 中典型的上下文长度 [33]）上，对 Llama-34B（或 Llama-70B）在一块 A40 GPU 上运行预填充可能需要三（或六）秒。这造成用户在看到第一个生成词之前必须等待可观的时间。近期工作还表明预填充可能成为吞吐瓶颈：去掉预填充阶段可以让 LLM 推理系统的吞吐量翻倍 [60]。

## 3 动机

### 3.1 复用 KV 缓存的机会

近期的系统尝试缓解预填充开销，其依据是这样一个观察：在许多 LLM 使用场景中，相同文本会在不同的 LLM 输入中被反复使用。这使得复用这些被复用文本的 KV 缓存成为可能（稍后解释）。

当相同文本被纳入 LLM 输入以提供必要上下文、确保高且一致的回复质量时，文本复用尤为普遍。为更具体地说明，考虑两个场景。

- 在一家用 LLM 管理内部记录的公司里，两个查询可能是「IT 部门里谁在上次全员会议上提议用 RAG 增强客户服务 X？」和「IT 部门里有哪些人是 Y 大学的毕业生？」这两个查询看似不同，但都需要 IT 部门的员工名单作为生成正确答案的必要上下文。
- 类似地，在一个总结 Arxiv 论文的 LLM 应用中，两个查询可能是「Arxiv 上流行的 RAG 技术有哪些？」和「最近 Arxiv 上用于评测 RAG 相关论文的数据集有哪些？」它们都需要近期关于 RAG 的 Arxiv 论文作为生成正确结果的必要上下文。

由于被复用的上下文通常比用户查询包含更多信息，输入中「上下文」部分的预填充构成了预填充开销的大头 [33, 22]。因此，理想的做法是存储并复用被复用文本的 KV 缓存，以避免这些文本再次出现在不同 LLM 输入中时的预填充开销。

### 3.2 为什么前缀缓存不够用？

确实，若干近期系统通过复用 KV 缓存来降低预填充延迟。例如在前缀缓存中，可复用文本块的 KV 缓存被预计算一次；若该文本块位于某条 LLM 输入的前缀，则可复用预计算的 KV 缓存来跳过对该前缀的预填充。前缀缓存的优势在于前缀的 KV 缓存不受后续文本影响，因此生成结果与完全 KV 重计算（不用 KV 缓存）完全一致。多个系统采用了这一思路，如 vLLM [36]、SGLang [59] 与 RAGCache [33]。

前缀缓存的缺点同样明显。为了回答一个查询，RAG 等应用往往在 LLM 输入前放置多个文本块，以提供回答该查询所需的各类上下文。¹ 结果，除第一个块之外，所有其他块的 KV 缓存都不会被复用，因为它们不是 LLM 输入的前缀。

**脚注 1：在 LLM 输入中前置全部上下文是增强用户查询的流行做法（如 Langchain 与 LlamaIndex 的「stuff」模式）。本文默认使用该模式。其他 RAG 方法如「MapReduce」或「Rerank」不属于此类：它们先分别处理每个上下文文本块，再合并各上下文的结果。由于每个块被单独处理时总是前缀，前缀缓存工作良好。但「MapReduce」很慢，因为它需要先总结每个块再从摘要生成答案；「Rerank」在多个块都含有相关信息时生成质量低下，因为它对每个块单独处理。我们也在 §7 中实证评估了这些方法并与 CacheBlend 比较。**

回想 §3.1 中的查询。要回答「IT 部门里谁在上次全员会议上提议用 RAG 增强客户服务 X？」，我们需要来自多个来源的上下文，包括 IT 部门员工、关于服务 X 的信息以及全员会议的会议纪要。类似地，在 Arxiv 总结应用中，回答示例查询需要 LLM 阅读若干篇近期 RAG 相关 Arxiv 论文作为上下文。这些上下文主题各异，不太可能一起出现在同一个文本块中。它们是只在回答特定查询时才被组合使用的多个独立文本块。

图 2. 检索的文本块越多，生成质量越好。

为实证说明在 LLM 输入中纳入多个文本块的必要性，我们使用两个流行的多跳问答数据集 Musique 与 2WikiMQA。这些数据集由查询以及回答查询所需的多个相关上下文文本组成。按照 RAG 的常见做法，我们先用 Langchain 的文本分块机制将上下文切分为 128 词元的块（一个常用数值 [29]）建立向量数据库 [5]。对每个查询，我们用 SentenceTransformers [49] 嵌入该查询，并基于查询与块的嵌入之间最小 L2 距离从数据库取回 top-k 相关块。图 2 展示了随着所选文本块数量增加、以标准 *F1 分数*衡量的生成质量。可以看到，随着检索来补充 LLM 输入的文本块增多，质量显著提升；不过纳入过多块会因著名的「迷失在中间」（lost-in-the-middle）问题而损害质量 [40, 54]。

简而言之，前缀缓存只能省下第一个文本块的预填充，因此当 LLM 输入包含更多文本块（即使它们被复用）时，节省也很有限。

### 3.3 为什么完全 KV 复用不够用？

完全 KV 复用正是为解决这一问题而提出的。该方法近期由 PromptCache [24] 开创。它借助缓冲区拼接各重复文本块独立预计算的 KV 缓存，以维持每个文本块位置的准确性。例如，要拼接块 $C_{1}$ 与 $C_{2}$ 的 KV 缓存，PromptCache 首先需要在一个假想输入上运行预填充来预计算 $C_{2}$ 的 KV 缓存——该假想输入在 $C_{2}$ 之前放置一个长度不小于 $C_{1}$ 的哑前缀。这样，即使 $C_{2}$ 不是前缀，我们仍然正确保留了 $C_{2}$ 的 KV 缓存中的位置信息，尽管每个块的 KV 缓存不得不被预计算多次。

然而，即便位置信息得以保留，一个更根本的问题是：非前缀文本块（如 $C_{2}$）的 KV 缓存忽略了该块与其前面文本（如 $C_{1}$）之间的交叉注意力。这是因为预计算 KV 缓存时前面的文本尚不可知。

忽略交叉注意力可能导致错误回答。图 3 给出了一个说明性例子：用户查询「在世界杯上 Messi 比 Cristiano Ronaldo 多进了多少球？」前面放置了两名球员职业生涯统计的文本块。使用完全预填充或前缀缓存时，结果清晰且正确。使用完全 KV 复用时，两个文本块的 KV 缓存各自预计算（每块都带有正确的位置编码），然后拼接成 KV 缓存。然而，如果 LLM 用这份 KV 缓存生成答案，它就会开始胡言乱语，给不出正确答案。

![Refer to caption](2405.16444v3/motivate_crossattention_v3.png)

图 3. 一个 LLM 输入的说明性例子：查询前放置了两个文本块。完全 KV 重计算（b）不复用 KV 缓存，虽慢但给出正确答案。而完全 KV 复用（c）给出错误答案，因为它忽略了块之间的交叉注意力（图 4）。

为理解原因，我们仔细考察注意力矩阵（§2 已解释），特别是两个讨论球员统计的文本块之间的交叉注意力。图 4 可视化了由原始（完全）预填充的 KV 缓存与完全 KV 复用的 KV 缓存分别得到的注意力矩阵。由于完全 KV 复用对每个块单独预计算，两块之间的交叉注意力在预计算 KV 缓存时被完全遗漏（从未计算）。在这个例子中，第一个块包含 Messi 的进球数，第二个块包含 Ronaldo 的进球数，而 LLM 被要求比较两者的进球数。忽略两块之间的交互（交叉注意力）就会导致有缺陷的回答。

平心而论，应当指出当块之间的交叉注意力较低时，完全 KV 复用确实可行。这常见于提示模板场景，那正是 PromptCache [24] 的主要目标应用。

![Refer to caption](2405.16444v3/attn_comparison_v4.png)

图 4. 对比 (a) 完全 KV 重计算与 (b) 完全 KV 复用的注意力矩阵。黄色方框高亮了交叉注意力。右侧图展示了由此得到的前向注意力矩阵，其差异源于两种方法不同的交叉注意力。

完全 KV 复用中交叉注意力缺失导致前向注意力矩阵（§2 已解释）出现显著偏差——该矩阵包含上下文词元与最后几个词元之间的注意力，直接影响生成的词元。

为展示多块 LLM 输入中交叉注意力的普遍性，图 2 对比了完全 KV 重计算（含交叉注意力）与完全 KV 复用（不含交叉注意力）的回复质量（F1 分数）。可以看到，随着相关块数量增加，完全预填充与模块化缓存之间的差距愈发明显。这是因为块数越多，输入不同部分之间的交叉引用与相互依赖（交叉注意力）总量越大。

## 4 快速 KV 缓存融合

鉴于完全 KV 重计算（即完全预填充或前缀缓存）可能太慢，而完全 KV 复用质量低下，一个自然的问题是如何同时拥有完全 KV 复用的速度与完全 KV 重计算的质量。因此，我们的目标如下：

###### 目标 0.

当一条 LLM 输入包含多个被复用的文本块时，如何快速更新预计算的 KV 缓存，使得前向注意力矩阵（以及随后的输出文本）与完全 KV 重计算产生的结果差异最小。

为达成目标，我们提出 CacheBlend：在每层重计算一个被挑选的词元子集的 KV，同时复用其他词元的 KV。² 本节分三部分解释 CacheBlend。我们先给出记号（§4.1），然后描述如何只重计算一小部分词元的 KV（§4.2），最后解释如何在每层挑选 KV 将被重计算的词元（§4.3）。

**脚注 2：为简单起见，我们混用 KV 与 KV 缓存两个术语。**

| 符号 | 描述 |
| --- | --- |
| $i$ / $j$ | 层索引 / 词元索引 |
| $KV$ | KV 缓存 |
| $KV_{i}$ | 第 $i$ 层的 KV |
| $KV_{i}[j]$ | 第 $i$ 层上词元 $j$ 的 KV |
| $KV^{\textrm{full}}$ | 完全重计算的 KV 缓存 |
| $KV^{\textrm{pre}}$ | 预计算的 KV 缓存 |
| $KV^{\textrm{new}}$ | CacheBlend 更新后的 KV 缓存 |
| $A_{i}$ | 第 $i$ 层的前向注意力矩阵 |
| $A_{i}^{\textrm{full}}$ | 完全 KV 重计算的前向注意力矩阵 |
| $A_{i}^{\textrm{pre}}$ | 完全 KV 复用的前向注意力矩阵 |
| $A_{i}^{\textrm{new}}$ | CacheBlend 的前向注意力矩阵 |
| $\Delta_{\textrm{kv}}(KV_{i},KV^{\textrm{full}}_{i})[j]$ | $KV_{i}[j]$ 与 $KV^{\textrm{full}}_{i}[j]$ 之间的 KV 偏差 |
| $\Delta_{\textrm{attn}}(A_{i},A^{\textrm{full}}_{i})$ | $A_{i}$ 与 $A^{\textrm{full}}_{i}$ 之间的注意力偏差 |

表 1. 术语汇总

### 4.1 术语

表 1 汇总了本节使用的记号。对给定的 $N$ 个文本块，我们用 $KV^{\textrm{full}}$ 表示完全 KV 重计算得到的 KV 缓存，$KV^{\textrm{pre}}$ 表示预计算的 KV 缓存，$KV^{\textrm{new}}$ 表示经 CacheBlend 更新后的 KV 缓存。这里每份 KV 缓存都是不同文本块对应 KV 缓存的拼接。KV 缓存的每一层 $i$（$KV_{i}$）产生前向注意力矩阵 $A_{i}$。

完全 KV 重计算（完全预填充）与完全 KV 复用之间的差异有两方面。

- KV 偏差：我们将某 KV 缓存 $KV$ 在第 $i$ 层词元 $j$ 上的 KV 偏差定义为 $KV_{i}[j]$ 与 $KV^{\textrm{full}}_{i}[j]$ 之间的绝对差，记作 $\Delta_{\textrm{kv}}(KV_{i},KV^{\textrm{full}}_{i})[j]$。它度量给定 KV 在特定词元与特定层上相对完全预填充 KV 缓存的差异程度。我们随后将用 KV 偏差来识别哪些词元的 KV 偏差较大、因而需要更新。
- 注意力偏差：类似地，对于第 $i$ 层的前向注意力矩阵 $A_{i}$，我们定义注意力偏差 $\Delta_{\textrm{attn}}(A_{i},A^{\textrm{full}}_{i})$ 为其与 $A^{\textrm{full}}_{i}$ 之差的 L-2 范数。回顾 §3.3，由于交叉注意力缺失，完全 KV 复用在前向注意力矩阵上存在偏差（如图 4 所示）。

利用这些记号，我们的目标可以表述为：如何快速把预计算的 KV 缓存 $KV^{\textrm{pre}}$ 更新为新的 KV 缓存 $KV^{\textrm{new}}$，使任意层 $i$ 上的注意力偏差 $\Delta_{\textrm{attn}}(A^{\textrm{new}}_{i},A^{\textrm{full}}_{i})$ 最小化。

### 4.2 选择性地重计算 KV 缓存

![Refer to caption](2405.16444v3/selective_recompute_arial.png)

图 5. 图解一层上 (a) 完全 KV 重计算与 (b) 选择性 KV 重计算的对比。

目前，先假设我们已经选定每层要重计算的词元子集（如何在 §4.3 解释）。这里描述 CacheBlend 如何在每层重计算这些被选词元的 KV。

**工作流程：** 预填充的默认实现（如图 5(a) 所示）并不在只计算一部分词元 KV 的同时「跳过」其他词元。相反，CacheBlend 运行以下步骤（如图 5(b) 所示）：

- 首先对第 $i$ 层的输入施加掩码，将其缩减为被选词元的子集。
- 然后将缩减后的输入变换为 $Q_{i}$、$K_{i}$、$V_{i}$ 向量，这些向量同样只限于被选词元。
- 接着通过复用第 $i$ 层上未被选词元对应的 KV 缓存条目来扩展 $K_{i}$ 与 $V_{i}$ 向量，使注意力矩阵涵盖被选词元与其他所有词元之间的注意力。
- 最后运行同样的注意力模块，产生下一层的输入。

这些改动几乎不依赖 transformer 具体流程的细节，可以集成进许多流行的 transformer 实现（细节见 §6）。值得注意的是，计算开销与被选词元数量成正比，因为只运行与被选词元相关的计算。若每层重计算 $r\%$ 的词元，总计算开销为完全预填充的 $r\%$。

### 4.3 选择重计算哪些词元

接下来，我们解释如何挑选每层上 KV 应被重计算的词元，以降低由 KV 偏差导致的各层注意力偏差。因此，我们的直觉是优先重计算 KV 偏差较高的词元的 KV。当然，这一直观方案并不可行，因为它需要知道完全预填充的 KV 缓存；我们稍后使其变得实用。

图 6. 每层重计算越多词元的 KV，注意力偏差越小。重要的是，注意力偏差最大的下降来自重计算 KV 偏差最高词元（即 HKVD 词元）的 KV。

为验证挑选高 KV 偏差词元的有效性，图 6 在 Musique 数据集上使用了三个模型（细节见 §7.1）。它展示了当我们用前述方案（§4.2）选出并重计算 KV 偏差 $\Delta_{\textrm{kv}}(KV_{i},KV^{\textrm{full}}_{i})[j]$ 最高的 $r\%$ 词元 $j$ 后，所有层 $i$ 上平均注意力偏差 $\Delta_{\textrm{attn}}(A_{i},A^{\textrm{full}}_{i})$ 的变化。随着重计算比例 $r$ 增大，注意力偏差逐渐降低，而最大的下降发生在重计算 KV 偏差最高的前几个词元时。经验上，这给出了如下洞见。

###### 洞见 1.

在第 $i$ 层，重计算 KV 偏差较高（即 $\Delta_{\textrm{kv}}(KV_{i},KV^{\textrm{full}}_{i})[j]$）的词元 $j$ 的 KV，能更大程度地降低注意力偏差（即 $\Delta_{\textrm{attn}}(A_{i},A^{\textrm{full}}_{i})$）。

因此，若我们要在第 $i$ 层重计算比如 10% 词元的 KV，就应选择 KV 偏差最高的那 10% 词元。³ 我们称这些词元为第 $i$ 层的高 KV 偏差（High-KV-Deviation，HKVD）词元。

**脚注 3：在预计算的 KV 缓存中，每个块的 K 向量必须调整为正确的位置编码。在最先进的位置编码方案（旋转位置编码 RoPE [50]）下，这一校正只需将 K 向量乘以旋转矩阵 $\begin{pmatrix}\cos m\theta&-\sin m\theta\\ \sin m\theta&\cos m\theta \end{pmatrix}$（$n$ 维情形见附录 A）。由于该乘法只执行一次，此步开销可忽略。**

既然知道应当为 HKVD 词元重计算 KV，两个自然的问题随之而来。

**我们是否需要为大多数词元重计算 KV？** 在 §7 中，我们实证表明选取 10–20% 的词元作为 HKVD 词元并重计算其 KV，就足以大幅降低注意力偏差并保持生成质量。

这可以用注意力稀疏性直观解释——这是先前研究在许多 transformer 模型中观察到的成熟性质 [43, 58, 15, 14]。该性质指出，在注意力矩阵中，高注意力通常只出现在少数词元与其前面的词元之间。为验证这一观察，图 7 使用与图 6 相同的模型与数据集，展示了某一层上 KV 偏差的分布。可以看到，约 10–15% 的一小部分词元的 KV 偏差远高于其他词元，这印证了交叉注意力的稀疏性。

若一个词元与其他块词元的注意力很低（即与其他块的交叉注意力低），那么 $A^{\textrm{pre}}$ 与 $A^{\textrm{full}}$ 之间的 KV 偏差就会很低，因此无需重计算。只有当一个词元与其他块有高注意力（相对真值的 KV 偏差高）时，其 KV 才应被重计算。

图 7. 某一层上不同词元的 KV 偏差分布。

**如何在不知道真实 KV 值或注意力矩阵的情况下识别 HKVD 词元？** 朴素地，要识别 HKVD 词元必须先知道每层完全重计算的 $KV^{\textrm{full}}_{i}$，但这样做太昂贵，也违背选择性 KV 重计算的初衷。我们转而观察到：不同层的 HKVD 词元并非相互独立：

###### 洞见 2.

在一层上 KV 偏差最高的词元，很可能在下一层也是 KV 偏差最高的词元。

例如，若第一层的 HKVD 词元是词元 2、3、5，那么这三个词元在第二层上也很可能比大多数其他词元具有更高的 KV 偏差。

图 8 使用与图 7 相同的设置，展示了相邻两层词元 KV 偏差之间的 Spearman 秩相关分数。图中显示不同层之间 HKVD 词元的一致相似性。⁴ 这一相关性背后的直觉来自先前的观察：transformer 模型中每个词元的输入嵌入在层间变化缓慢 [44, 47]。因此，层间 KV 缓存也应具有相似性，因为 KV 缓存是由输入嵌入经线性变换生成的。

**脚注 4：需要澄清的是，尽管 HKVD 词元在各层间相似，各层的注意力矩阵之间仍可能相当不同。**

图 8. 相邻两层之间每词元 KV 偏差的秩相关。

鉴于 HKVD 词元之间的显著相关性，一个直接的方案是：先在第一层执行预填充，挑出第一层的 HKVD 词元，然后在其他所有层只更新这些词元的 KV。由于 LLM 通常有超过 30 层，相比完全 KV 重计算，这一过程可省下大部分计算。话虽如此，仅用第一层不同词元的注意力偏差在统计上可能不足以可靠地挑选所有层（尤其是更深层）的 HKVD 词元。

![Refer to caption](2405.16444v3/selection_illustrated_arial.png)

图 9. CacheBlend 通过只计算从上一层选出的 HKVD 词元的 KV 偏差，并从中挑选 KV 偏差高的词元，来选出某一层的高 KV 偏差（HKVD）词元。

因此，我们采用渐进过滤方案（如图 9 所示）。如果平均而言我们想在每层挑选 $r\%$ 的 HKVD 词元，我们会先基于第一层的逐词元注意力偏差挑选 $r_{1}\%$ 的词元（$r_{1}$ 略高于 $r$），将它们作为第二层的 HKVD 词元；然后在第二层重计算这 $r_{1}\%$ HKVD 词元的 KV，并挑选逐词元注意力偏差最高的 $r_{2}\%$ 词元（$r_{2}$ 略低于 $r_{1}$）作为下一层的 HKVD 词元，依此类推。直观上，这一渐进过滤方案最终选出的 HKVD 词元不仅是在第一层、而是在多层上都具有高注意力偏差的词元，经验上这在统计上更可靠地识别出每层的 HKVD 词元。

虽然执行 HKVD 计算的第 $i$ 层的 KV 缓存空间同时容纳更新后的 KV 与预计算的 KV，但一旦推理进入第 $i+1$ 层，第 $i$ 层额外的预计算 KV 会被立即丢弃。因此 HKVD 带来的内存开销可忽略。

## 5 CacheBlend 系统设计

我们给出 CacheBlend 的一个具体系统设计，它利用以下基本洞见来降低选择性 KV 重计算的影响。

**基本洞见：** *如果选择性 KV 重计算（§4.3）的延迟快于 KV 载入 GPU 显存的延迟，那么将选择性 KV 重计算与 KV 载入适当流水线化，可使 KV 重计算的额外延迟可忽略。*

**将 KV 载入与重计算流水线化：** 在 CacheBlend 中，前一层的预计算 KV 缓存载入 GPU 后，该层的选择性重计算可以立即开始。这是因为某层上重计算哪些词元的 KV 只取决于前一层词元的 KV 偏差。于是，只要载入一层预计算 KV 的时间小于等于该层选择性 KV 重计算的时间，KV 载入延迟就应当能掩盖选择性重计算延迟，即不会给首词元延迟（TTFT）带来任何额外延迟。

以 Llama-7B 模型和 4K 长上下文为例，重计算 15% 的词元（默认重计算比例）每层只需 3 ms，而从 NVME SSD 载入一层 KV 缓存需 16 ms（§7）。此时，KV 载入可以掩盖 15% 词元 KV 重计算的延迟，即 KV 重计算不带来额外延迟。重计算更多词元（可略微提升生成质量）也可能不带来额外延迟，只要延迟低于 16 ms。相反，对另一个模型 Llama-70B，重计算 15% 词元需要 7 ms，而从 NVME SSD 载入一层 KV 只需 4 ms。此时 KV 载入无法完全掩盖重计算延迟。简而言之，需要一个控制器来智能地选择重计算比例以及（如果适用）KV 缓存的存放位置。

### 5.1 关键组件

为实现 KV 载入与重计算流水线化的收益，我们的系统有三大组件。

图 10. (a) 智能选择重计算比例不会带来额外延迟。(b) 智能选择存放 KV 的存储设备可以在不增加延迟的同时节省成本。

![Refer to caption](2405.16444v3/overview.png)

图 11. 面向单条请求的 LLM 上下文增强生成流程中的 CacheBlend 系统（绿色星标）。CacheBlend 使用检索器提供的文本，与存储设备交互，并在 LLM 推理引擎之上提供 KV 缓存。

**载入控制器（Loading Controller）：** 实践中我们面对两个设计问题。第一，*给定固定的可用存储设备，如何选择重计算比例（每层重计算 KV 的词元比例）而不给 TTFT 带来额外延迟？* 图 10(a) 给出了一个例子：若我们明智地选择重计算比例，当载入较慢时，重计算不会给载入造成*任何*额外延迟。

为此，控制器使用两个延迟估计器来寻找理想的重计算比例，使重计算延迟接近载入延迟。给定重计算比例 $r$、待载入上下文长度 $L$ 与 LLM，重计算延迟估计器计算期望延迟 $T_{recompute}(r\%,LLM,L)$。⁵ 载入延迟估计器基于 LLM、存储设备的速度（离线测得）与上下文长度 $L$，估计一层 KV 缓存的载入延迟 $T_{load}(LLM,L,storage\_device)$。⁶

**脚注 5：$T_{recompute}(r\%,LLM,L)=r\%\times Prefill(LLM,L)$。$Prefill(LLM,L)$ 为离线 profiling 得到。**

**脚注 6：$T_{load}(LLM,L,storage\_device)=\frac{PerTokenKVSize(LLM)\times L}{Throughput(storage\_device)}$。**

控制器计算一个理想重计算比例，使载入延迟能掩盖重计算延迟，同时不降低推理质量。它首先选出使 $T_{recompute}(r\%,LLM,L)$ 等于 $T_{load}(LLM,L,storage\_device)$ 的重计算比例 $r\%$，然后取 $r\%$ 与 $r^{*}\%$ 中的较大者，其中 $r^{*}\%$ 是经验上相对完全 KV 重计算质量下降可忽略的最小重计算比例。实践中，我们从图 16 发现 $r^{*}\%$ 为 15%。这意味着即使存储设备很快（例如 CPU RAM），延迟也会被保证质量所需的最小重计算量下界约束。

实践中，CacheBlend 还面临另一个挑战：开发者应使用哪种存储设备？为解决这一挑战，我们向载入控制器提出一个更形式化的问题：*若我们只以固定的选择性重计算比例（例如 15%）做 KV 重计算，如何选择正确的存储设备来存放 KV，才能不造成额外延迟？* 如图 10(b) 所示，在固定重计算比例下，控制器应在所有不增加延迟的设备中挑选最便宜的存储设备。

在 CacheBlend 中，系统开发者可以提供一份候选存储设备列表，控制器使用存储成本估计器基于 LLM、上下文长度 $L$ 与（若是云存储）所需存储时长 $T$，估计每种设备存放 KV 的成本 $C_{store}(LLM,L,T,storage\_device)$。然后它用 $T_{recompute}(15\%,LLM,L)$ 与 $T_{load}(LLM,L,storage\_device)$ 估计所有设备的重计算与载入延迟。最后，它找出满足 $T_{recompute}\geq T_{load}$ 的设备中最便宜的一个。这样，给定满足生成质量要求的固定重计算目标，开发者可以在不同存储设备间为 KV 缓存做出权衡。

**KV 缓存存储（将 LLM 输入映射到 KV 缓存）：** KV 缓存存储把一条 LLM 输入切分为多个文本块，每块可被复用或为新块。例如，RAG 输入通常由多个检索到的上下文块（很可能定长）与用户输入组成。LLM 输入的切分方式取决于具体应用，我们实现了与近期工作 [24, 38] 相同的策略。输入被切分为文本块后，对每块做哈希以查找其对应的 KV 缓存，方式与 vLLM [36] 中实现的块哈希相同。由融合器（稍后解释）生成的新块 KV 缓存会被加入设备。当存储设备写满时，我们逐出最近最少使用的 KV 缓存。本文只关注在单一级存储设备（如 CPU RAM 或 SSD）上存放 KV 缓存。

**融合器（Fusor）：** 缓存融合器（§4）通过选择性重计算合并预计算的 KV 缓存。回顾 §4.3，某一层需要重计算哪些词元取决于上一层的重计算结果。因此，融合器会等待上一层的重计算完成、且第 $i$ 层的 KV 缓存已载入 GPU 显存中的队列后，再按载入控制器算出的重计算比例 $r\%$ 执行选择性重计算。融合器重复此过程直到所有层都被重计算。

### 5.2 组合成整体

我们在图 11 中把关键组件组装进 LLM 推理流程。当 LLM 应用的用户提交问题时，会查询一份相关文本块列表。载入控制器随后向 KV 缓存管理器查询这些文本块的 KV 缓存是否存在以及存放位置。接着 KV 缓存管理器把信息返回给载入控制器，控制器计算理想的选择性重计算比例、发送给融合器，并把 KV 缓存载入 GPU 显存中的队列。KV 缓存融合器不断重计算队列中的 KV 缓存，直到所有层都被重计算。最后，融合后的 KV 缓存被输入 LLM 推理引擎，后者基于该 KV 缓存生成对用户问题的回答。

## 6 实现

我们在 vLLM 之上用约 3K 行 Python（基于 PyTorch v2.0）实现了 CacheBlend。

**把融合器集成进 LLM 服务引擎：** CacheBlend 通过三个接口以逐层方式执行部分预填充流程：

- fetch_kv(text, layer_id) -> KVCache：给定一段文本与层编号，CacheBlend 从 KV 存储把对应的 KV 缓存取入 GPU。若系统中没有该 KV 缓存则返回 -1。
- prefill_layer(input_dict, KVCache) -> output_dict：CacheBlend 接收该层的输入与 KV 缓存，对该层执行部分预填充流程。输出作为下一层的输入。
- synchronize()：CacheBlend 在预填充每层之前要求同步，以确保该层的 KV 缓存已经载入 GPU。

我们在 vLLM 内部实现了这三个接口。对 fetch_kv，我们先计算文本的哈希并检索它是否在 KV 存储系统中。若存在，当 KV 缓存在磁盘上时调用 torch.load() 载入 GPU 显存，当 KV 缓存在 CPU 内存中时使用 torch.cuda()。对 prefill_layer，我们在 vLLM 原有执行单层预填充的层函数之上实现该接口。input_dict 中记录三个键值对：(1) 预填充一个 LLM 层所需的原始输入数据 input_org（如 input_tensor、input_metadata）；(2) 指示本层是否将选取 HKVD 词元的 check_flag；(3) 跟踪 HKVD 词元索引的 HKVD_indices。若 check_flag 为 True，新计算的 KV 缓存与载入的 KV 缓存之间偏差最大的输入词元将被选为 HKVD 词元。若 check_flag 为 False，则只对 HKVD_indices 指示的当前 HKVD 词元执行部分预填充。每层只计算并更新 HKVD 词元的 KV 缓存。在第 $i$ 层的部分预填充中，用两个线程将第 $i$ 层的计算（prefill_layer）与下一层 $i+1$ 的 KV 缓存载入（fetch_kv）流水线化。prefill_layer 之前调用 synchronize，以确保预填充所需的 KV 缓存已载入 GPU。

**管理 KV 缓存：** CacheBlend 按如下方式管理 KV 缓存：若 KV 缓存不在系统中且由 LLM 引擎在运行时重计算，我们会用 torch.cpu() 把 KV 缓存移入 CPU，并开一个线程在后台用 torch.save() 写回磁盘。在 fetch_kv 期间，我们遍历哈希表为融合器取回 KV 缓存。哈希表因体量较小（一百万个块约 16MB）而保存在 CPU 中。

图 12. 在四个数据集与三个模型上，CacheBlend 相比完全 KV 重计算将 TTFT 降低 2.2–3.3×，质量下降可忽略。

图 13. Yi-34B 上 CacheBlend 与 MapReduce、MapRerank 的生成质量对比。

## 7 评测

评测的关键结论如下：

- **TTFT 降低：** 与完全 KV 重计算相比，CacheBlend 在多个模型与任务上将 TTFT 降低 2.2–3.3×。
- **高质量：** 与完全 KV 复用相比，CacheBlend 在 F1 分数与 Rouge-L 分数上提升 0.15 至 0.35；与完全 KV 重计算及前缀缓存相比，质量下降不超过 0.01–0.03。
- **更高吞吐：** 在相同 TTFT 下，CacheBlend 相比完全 KV 重计算可将吞吐提升至 5×，相比前缀缓存提升至 3.3×。

图 14. 在 RAG 场景下，CacheBlend 相比质量相近的基线实现了更低 TTFT 与更高吞吐。

图 15. CacheBlend 在不同块数、块长与批大小下均优于基线。

### 7.1 实验设置

**模型与硬件设置：** 我们在 Mistral-7B [30]、Yi-34B [56] 与 Llama-70B [2] 上评测 CacheBlend，以覆盖较宽的开源模型规模。注意我们对 Llama-70B 与 Yi-34B 应用了 8 位模型量化。我们在 Runpod GPU [10] 上运行端到端实验，配置为 128 GB RAM、2 块 Nvidia A40 GPU 与实测吞吐 4.8 GB/s 的 1TB NVME SSD。我们用 1 块 GPU 服务 Mistral-7B 与 Yi-34B，用 2 块 GPU 服务 Llama-70B。

**数据集：** 我们的评测覆盖以下数据集。

- 2WikiMQA⁷ [27]：该数据集旨在通过要求模型阅读多个段落来回答给定问题，测试 LLM 的推理能力。沿用先前工作的数据集规模，我们纳入 200 个测试用例 [12]。
- Musique⁷ [51]：这是一个多文档问答数据集，旨在测试 LLM 的多跳推理能力——其中一个推理步骤关键性地依赖来自另一个步骤的信息。包含 150 个测试用例。
- SAMSum [25]：该数据集由多对对话与摘要组成，要求 LLM 为新对话输出摘要。它旨在测试语言模型的少样本学习能力，包含 200 个测试用例。
- MultiNews [20]：该数据集由新闻文章与 newser.com 网站上对这些文章的人工撰写摘要组成。每份摘要由编辑专业撰写并包含所引用原文的链接。包含 60 个采样用例。

**脚注 7：由于 2WikiMQA 与 Musique 的标准答案均不超过 5 个词，我们在其提示词后追加「Answer within 5 words.」以减少 F1 分数计算中答案长度不匹配的影响。**

我们用 Langchain 将上下文切分为 512 词元的块，SAMSum 则使用原有的 200–400 词元块。我们还创建了一个合成数据集来模拟 RAG 场景中的块复用。具体而言，我们在 Musique 与 2WikiMQA 数据集中各随机抽取 1500 个查询，并用 Langchain [5] 把每个查询的上下文切分为 512 词元的块 [29] 建立上下文块数据库。对每个查询，我们用 GPT4 API 另生成 3 个相似查询。在这 6000 个查询（1500 原始 + 4500 模拟）中，我们基于 L2 距离以随机顺序检索 top-6 块。⁸ 我们称这些数据集为 *Musique extended* 与 *2WikiMQA extended*。我们只报告质量相近的基线结果，并跳过前 1K 个查询的结果，因为最初存储完全是空的。

**脚注 8：Llama-70B 输入词元上限内能容纳的最大块数。**

**质量指标：** 我们采用以下标准指标衡量生成质量。

- F1 分数 [6] 用于评测 2WikiMQA 与 Musique 数据集 [12]。它基于重叠词数衡量模型输出与问题标准答案之间的相似度。
- Rouge-L 分数 [39] 用于评测 MultiNews 与 SAMSum 数据集 [12]。它基于最长公共序列衡量模型输出与标准摘要之间的相似度。

**基线：** 我们将 CacheBlend 与以下基线比较：

- **完全 KV 重计算：** 原始文本直接作为 LLM 输入。LLM 在预填充期间计算所有词元的 KV 缓存。
- **前缀缓存** [33, 59, 36]：我们采用 SGLang [59] 的技术识别频繁使用的前缀块，并把它们的 KV 缓存存入 RAM 与 SSD。非前缀词元的 KV 缓存需在预填充期间计算。我们还做了一个有利于前缀缓存的理想化假设：从 RAM 或 SSD 到 GPU 没有载入延迟。该假设使其表现得比真实条件下更好。
- **完全 KV 复用** [24]：我们用 PromptCache [24] 提出的方法实现完全 KV 复用。我们在文本前附加缓冲区，以准备其 KV 缓存在不同位置使用时具有正确的位置编码。我们没有与 scaffolding 方案比较，因为它应用于 RAG 场景需要人类用户在运行时手动挑选重要块。
- **MapReduce** [7]：与传统 MapReduce [18] 不同，这是 LangChain 中的另一种 RAG 方法。LLM 首先并行地总结所有块并拼接，然后将拼接后的摘要再次输入 LLM 以生成最终答案。
- **MapRerank** [8]：这是 LangChain 中的又一种 RAG 方法。在 MapRerank 中，LLM 从每个块独立生成一个答案，并基于答案正确的置信度给出评分，取得分最高的答案作为最终输出。

图 16. 使用 Yi-34B 时，CacheBlend 以 5%–18% 的选择性重计算比例相对完全 KV 重计算只有极小的质量损失。

图 17. CacheBlend 在使用 RAM 与较慢磁盘时优于基线。

### 7.2 整体改进

**TTFT 降低且质量损失极小：** 图 12 比较了各请求的平均质量与 TTFT，其中每个请求的上下文由 SentenceTransformers [49] 生成的嵌入之间 L2 距离最低的 6 个 top 块组成（每块 512 词元）。如图所示，与完全 KV 重计算和前缀缓存相比，CacheBlend 的 F1 与 Rouge-L 分数降幅在 0.02 以内，同时在所有模型与数据集上将 TTFT 显著降低 2.2–3.3×。虽然由于选择性重计算，CacheBlend 比完全 KV 复用慢，但其质量稳定地以大幅优势胜过完全 KV 复用（多数情况下超过 2×）。

图 13 将 CacheBlend 与 MapReduce、MapRerank 等 RAG 方法比较。与 MapReduce 相比，CacheBlend 的 TTFT 低 2–5× 且 F1 分数更高。

**延迟更低且吞吐更高：** 在图 14 中，我们在不同请求速率下于 Musique extended 与 2WikiMQA 数据集上将 CacheBlend 与完全 KV 重计算和前缀缓存比较。在不同模型与数据集上，CacheBlend 以 2.8–5× 的更高吞吐实现了比所有基线更低的延迟。

**理解 CacheBlend 的改进：** CacheBlend 因不同原因优于所有基线。相比完全 KV 重计算，CacheBlend 只重计算少量词元，因此延迟低得多、吞吐更高。相比完全 KV 复用，虽然其延迟低于 CacheBlend，但质量大幅下降，因为完全 KV 复用不做任何重计算，从而缺失了不同块之间的交叉注意力。相比前缀缓存，CacheBlend 在吞吐与延迟上也更优，因为当同一块有不同前缀时，前缀缓存需要为它存储*多个版本*的 KV 缓存。因此，在总存储空间固定的条件下，前缀缓存会有更高的未命中率。最后，相比 MapReduce 与 MapRerank 等其他 RAG 方法，CacheBlend 在质量或延迟上也更优。对 MapReduce 而言，额外的 LLM 推理使其延迟高于 CacheBlend。MapRerank 的 TTFT 虽略低于 CacheBlend，但其质量差得多，因为单独处理各输入块忽略了块之间的依赖。

### 7.3 敏感性分析

为更好理解 CacheBlend，我们进一步分析不同配置对整体性能的影响。

**改变块数与块长：** 图 15a 与 15b 展示了 CacheBlend 在不同块数与块长设置下维持生成质量（F1 分数损失 ≤0.015）所需的最少计算时间。实验在 2WikiMQA 与 Mistral-7B 模型上进行。如图所示，计算时间缩减比例在不同块数与块长设置下保持相似。

**改变重计算比例：** 图 16 展示了重计算比例对 Yi-34B 模型上所有数据集的质量-TTFT 权衡的影响。在所有数据集上，以 5%~18% 的重计算比例，CacheBlend 相比完全 KV 重计算的生成质量损失至多 0.002 的 F1 或 Rouge-L 分数。把这个数字放进语境：5%~18% 的重计算比例可转化为相对完全 KV 重计算 4.1–6.6× 的 TTFT 降低，以及相对前缀缓存 3.4–6.1× 的 TTFT 降低。

**改变批大小：** 图 15c 展示了不同批大小下预填充阶段的计算时间。值得注意的是，批大小增大时解码阶段时间的增长慢于预填充阶段 [60, 36]，使预填充开销随批大小增大而占主导。因此，随着批大小增大，CacheBlend 对预填充阶段的改进在整体延迟降低中的作用更加突出。

**改变存储设备：** 为研究不同存储类型对 CacheBlend 的影响，我们修改每种方法的底层存储设备，并对 Yi-34B 模型与 2WikiMQA 数据集进行与图 12 类似的实验。如图 17 所示，当 KV 缓存存放在 RAM 或较慢的 SSD 设备上时，CacheBlend 始终以极小的质量退化降低 TTFT。注意，存储越慢，CacheBlend 与完全 KV 复用之间的延迟差距越小，因为此时 CacheBlend 的延迟更多由载入延迟而非部分 KV 重计算主导。

## 8 相关工作

**检索增强生成（RAG）：** RAG [46, 48, 22, 37, 23] 可以借助从外部来源获取的文本块提升 LLM 的准确性与可靠性。然而，在 LLM 中处理这些文本块可能耗时很久。CacheBlend 通过存储并复用这些文本块的 KV 缓存来降低这一开销。

**跨请求复用 KV 缓存：** 近期工作广泛研究了跨请求存储与复用 KV 缓存 [59, 42, 24, 41, 33]。其中大多数 [59, 42, 41, 33] 聚焦于仅前缀缓存。PromptCache [24] 允许 KV 缓存在不同位置被复用，但由于位置编码不准确且忽略交叉注意力，无法维持令人满意的生成质量。CacheBlend 采用新颖的部分重计算框架，更好地保留了位置准确性与交叉注意力。现有工作大多将 KV 缓存存放在易失性存储设备（如 GPU HBM、CPU DRAM）以保证性能。虽然有新兴研究尝试复用高速 NVME SSD 存放 KV 缓存 [21]，CacheBlend 的独特之处在于将载入与部分重计算流水线化，并可扩展到更慢的对象存储。

**通用 LLM 服务系统：** 已有众多通用 LLM 服务系统被开发 [57, 36, 11, 60]。Orca [57] 通过迭代级调度使多个请求得以并行处理。vLLM [36] 通过更高效的 GPU 内存管理进一步提升并行度。CacheBlend 与这些通用 LLM 服务系统互补，为它们赋予上下文复用能力。

**上下文压缩方法：** 上下文压缩技术 [58, 31, 32, 43, 19, 55] 可与 CacheBlend 互补。其中一些技术 [31, 32] 通过剪除不重要词元缩短提示长度。CacheBlend 与此类方法兼容——如 §7.3 所示，它可以接受不同的块长。另一类工作 [58, 43, 19] 聚焦于基于注意力矩阵丢弃不重要的 KV 向量，本质上缩减了 KV 缓存大小。CacheBlend 可以从这类技术中受益，通过存储与载入更少的 KV 缓存。

## 9 局限与未来工作

本文的方法（如 §4.3 的洞见）目前只适用于 transformer 结构的语言模型。我们留待未来研究 transformer 之外的架构，例如 Mamba [26] 与 Griffin [17]。

在评测中，我们尚未在更多模型与采用不同量化设置的数据集上测试 CacheBlend 的性能。为了更好地理解与改进该方法，我们已将工作开源，以促进这一方向的更多努力。

本文将 CacheBlend 集成到了 vLLM 中，但尚未在 Distserve [60] 或 StableGen [11] 等最新服务引擎上测试 CacheBlend 的性能，也没有研究如何将 CacheBlend 应用于跨计算节点共享 KV 缓存的工作负载。由于 CacheBlend 能够降低代价高昂的预填充阶段，我们相信将 CacheBlend 与这些新服务引擎结合可能带来更多节省。我们将 CacheBlend 与这些新推理框架的集成留作未来工作。

## 10 结论

我们提出 CacheBlend，一个在多条文本被拼接进同一 LLM 输入时融合多份预计算 KV 缓存的系统。为保持生成质量，CacheBlend 通过选择性重计算一小部分词元的 KV 缓存值来恢复这些文本之间的交叉注意力。在四个数据集与三个模型上的实验中，CacheBlend 相比完全 KV 重计算将 TTFT 降低 2.2–3.3×、吞吐提升 2.8–5×，而质量下降可忽略。代码开源于 <https://github.com/LMCache/LMCache>。

## 11 致谢

我们感谢所有匿名评审以及我们的 shepherd Thaleia Dimitra Doudali 提出的深刻反馈与建议。该项目受 NSF CNS-2146496、CNS-2131826、CNS-2313190、CNS-1901466、CNS-2313190、CCF-2119184、CNS-1956180，以及 Google、CERES Center、Conviva 与 Chameleon Cloud 的研究资助。

## 参考文献

- [1]

  12 Practical Large Language Model (LLM) Applications - Techopedia.
  <https://www.techopedia.com/12-practical-large-language-model-llm-applications>.
  (Accessed on 09/21/2023).
- [2]

  [2302.13971] llama: Open and efficient foundation language models.
  <https://arxiv.org/abs/2302.13971>.
  (Accessed on 09/21/2023).
- [3]

  7 top large language model use cases and applications.
  <https://www.projectpro.io/article/large-language-model-use-cases-and-applications/887>.
  (Accessed on 09/21/2023).
- [4]

  Applications of large language models - indata labs.
  <https://indatalabs.com/blog/large-language-model-apps>.
  (Accessed on 09/21/2023).
- [5]

  Chains.
  <https://python.langchain.com/docs/modules/chains/>.
- [6]

  Evaluating qa: Metrics, predictions, and the null response.
  <https://github.com/fastforwardlabs/ff14_blog/blob/master/_notebooks/2020-06-09-Evaluating_BERT_on_SQuAD.ipynb>.
- [7]

  Langchain: Map reduce.
  <https://api.python.langchain.com/en/latest/chains/langchain.chains.combine_documents.map_reduce.MapReduceDocumentsChain.html#langchain.chains.combine_documents.map_reduce.MapReduceDocumentsChain>.
- [8]

  Langchain: Map rerank.
  <https://api.python.langchain.com/en/latest/chains/langchain.chains.combine_documents.map_rerank.MapRerankDocumentsChain.html>.
- [9]

  Real-world use cases for large language models (llms) | by cellstrat | medium.
  <https://cellstrat.medium.com/real-world-use-cases-for-large-language-models-llms-d71c3a577bf2>.
  (Accessed on 09/21/2023).
- [10]

  Runpod: Cloud compute made easy.
  <https://www.runpod.io/>, 2024.
  Accessed: 2024-05-21.
- [11]

  Amey Agrawal, Ashish Panwar, Jayashree Mohan, Nipun Kwatra, Bhargav S. Gulavani, and Ramachandran Ramjee.
  Sarathi: Efficient llm inference by piggybacking decodes with chunked prefills, 2023.
- [12]

  Yushi Bai, Xin Lv, Jiajie Zhang, Hongchang Lyu, Jiankai Tang, Zhidian Huang, Zhengxiao Du, Xiao Liu, Aohan Zeng, Lei Hou, Yuxiao Dong, Jie Tang, and Juanzi Li.
  Longbench: A bilingual, multitask benchmark for long context understanding.
  arXiv preprint arXiv:2308.14508, 2023.
- [13]

  Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al.
  Language models are few-shot learners.
  Advances in neural information processing systems, 33:1877–1901, 2020.
- [14]

  Beidi Chen, Tri Dao, Eric Winsor, Zhao Song, Atri Rudra, and Christopher Ré.
  Scatterbrain: Unifying sparse and low-rank attention.
  Advances in Neural Information Processing Systems, 34:17413–17426, 2021.
- [15]

  Krzysztof Choromanski, Valerii Likhosherstov, David Dohan, Xingyou Song, Andreea Gane, Tamas Sarlos, Peter Hawkins, Jared Davis, Afroz Mohiuddin, Lukasz Kaiser, et al.
  Rethinking attention with performers.
  arXiv preprint arXiv:2009.14744, 2020.
- [16]

  Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, et al.
  Palm: Scaling language modeling with pathways.
  arXiv preprint arXiv:2204.02311, 2022.
- [17]

  Soham De, Samuel L. Smith, Anushan Fernando, Aleksandar Botev, George Cristian-Muraru, Albert Gu, Ruba Haroun, Leonard Berrada, Yutian Chen, Srivatsan Srinivasan, Guillaume Desjardins, Arnaud Doucet, David Budden, Yee Whye Teh, Razvan Pascanu, Nando De Freitas, and Caglar Gulcehre.
  Griffin: Mixing gated linear recurrences with local attention for efficient language models, 2024.
- [18]

  Jeffrey Dean and Sanjay Ghemawat.
  Mapreduce: simplified data processing on large clusters.
  Communications of the ACM, 51(1):107–113, 2008.
- [19]

  Harry Dong, Xinyu Yang, Zhenyu Zhang, Zhangyang Wang, Yuejie Chi, and Beidi Chen.
  Get more with less: Synthesizing recurrence with kv cache compression for efficient llm inference.
  arXiv preprint arXiv:2402.09398, 2024.
- [20]

  Alexander R Fabbri, Irene Li, Tianwei She, Suyi Li, and Dragomir R Radev.
  Multi-news: A large-scale multi-document summarization dataset and abstractive hierarchical model.
  arXiv preprint arXiv:1906.01749, 2019.
- [21]

  Bin Gao, Zhuomin He, Puru Sharma, Qingxuan Kang, Djordje Jevdjic, Junbo Deng, Xingkun Yang, Zhou Yu, and Pengfei Zuo.
  Attentionstore: Cost-effective attention reuse across multi-turn conversations in large language model serving, 2024.
- [22]

  Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai, Jiawei Sun, and Haofen Wang.
  Retrieval-augmented generation for large language models: A survey, 2023.
- [23]

  Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai, Jiawei Sun, and Haofen Wang.
  Retrieval-augmented generation for large language models: A survey.
  arXiv preprint arXiv:2312.10997, 2023.
- [24]

  In Gim, Guojun Chen, Seung seob Lee, Nikhil Sarda, Anurag Khandelwal, and Lin Zhong.
  Prompt cache: Modular attention reuse for low-latency inference, 2023.
- [25]

  Bogdan Gliwa, Iwona Mochol, Maciej Biesek, and Aleksander Wawer.
  Samsum corpus: A human-annotated dialogue dataset for abstractive summarization.
  arXiv preprint arXiv:1911.12237, 2019.
- [26]

  Albert Gu and Tri Dao.
  Mamba: Linear-time sequence modeling with selective state spaces, 2023.
- [27]

  Xanh Ho, Anh-Khoa Duong Nguyen, Saku Sugawara, and Akiko Aizawa.
  Constructing a multi-hop qa dataset for comprehensive evaluation of reasoning steps.
  arXiv preprint arXiv:2011.01060, 2020.
- [28]

  Coleman Hooper, Sehoon Kim, Hiva Mohammadzadeh, Michael W Mahoney, Yakun Sophia Shao, Kurt Keutzer, and Amir Gholami.
  Kvquant: Towards 10 million context length llm inference with kv cache quantization.
  arXiv preprint arXiv:2401.18079, 2024.
- [29]

  Muhammad Jan.
  Optimize rag efficiency with llamaindex: The perfect chunk size.
  <https://datasciencedojo.com/blog/rag-with-llamaindex/>, october 2023.
- [30]

  Albert Q Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, et al.
  Mistral 7b.
  arXiv preprint arXiv:2310.06825, 2023.
- [31]

  Huiqiang Jiang, Qianhui Wu, Chin-Yew Lin, Yuqing Yang, and Lili Qiu.
  Llmlingua: Compressing prompts for accelerated inference of large language models.
  arXiv preprint arXiv:2310.05736, 2023.
- [32]

  Huiqiang Jiang, Qianhui Wu, Xufang Luo, Dongsheng Li, Chin-Yew Lin, Yuqing Yang, and Lili Qiu.
  Longllmlingua: Accelerating and enhancing llms in long context scenarios via prompt compression, 2023.
- [33]

  Chao Jin, Zili Zhang, Xuanlin Jiang, Fangyue Liu, Xin Liu, Xuanzhe Liu, and Xin Jin.
  Ragcache: Efficient knowledge caching for retrieval-augmented generation.
  arXiv preprint arXiv:2404.12457, 2024.
- [34]

  Jeff Johnson, Matthijs Douze, and Hervé Jégou.
  Billion-scale similarity search with GPUs, 2017.
- [35]

  Hao Kang, Qingru Zhang, Souvik Kundu, Geonhwa Jeong, Zaoxing Liu, Tushar Krishna, and Tuo Zhao.
  Gear: An efficient kv cache compression recipe for near-lossless generative inference of llm, 2024.
- [36]

  Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica.
  Efficient memory management for large language model serving with pagedattention.
  In Proceedings of the 29th Symposium on Operating Systems Principles, pages 611–626, 2023.
- [37]

  Huayang Li, Yixuan Su, Deng Cai, Yan Wang, and Lemao Liu.
  A survey on retrieval-augmented text generation.
  arXiv preprint arXiv:2202.01110, 2022.
- [38]

  Chaofan Lin, Chengruidong Zhang Zhenhua Han, Yuqing Yang, Fan Yang, Chen Chen, and Lili Qiu.
  Parrot: Efficient serving of llm-based applications with semantic variable.
  In 18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24), Santa Clara, CA, July 2024. USENIX Association.
- [39]

  Chin-Yew Lin.
  ROUGE: A package for automatic evaluation of summaries.
  In Text Summarization Branches Out, pages 74–81, Barcelona, Spain, July 2004. Association for Computational Linguistics.
- [40]

  Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang.
  Lost in the middle: How language models use long contexts.
  arXiv preprint arXiv:2307.03172, 2023.
- [41]

  Shu Liu, Asim Biswal, Audrey Cheng, Xiangxi Mo, Shiyi Cao, Joseph E. Gonzalez, Ion Stoica, and Matei Zaharia.
  Optimizing llm queries in relational workloads, 2024.
- [42]

  Yuhan Liu, Hanchen Li, Kuntai Du, Jiayi Yao, Yihua Cheng, Yuyang Huang, Shan Lu, Michael Maire, Henry Hoffmann, Ari Holtzman, et al.
  Cachegen: Fast context loading for language model applications.
  arXiv preprint arXiv:2310.07240, 2023.
- [43]

  Zichang Liu, Aditya Desai, Fangshuo Liao, Weitao Wang, Victor Xie, Zhaozhuo Xu, Anastasios Kyrillidis, and Anshumali Shrivastava.
  Scissorhands: Exploiting the persistence of importance hypothesis for llm kv cache compression at test time.
  Advances in Neural Information Processing Systems, 36, 2024.
- [44]

  Zichang Liu, Jue Wang, Tri Dao, Tianyi Zhou, Binhang Yuan, Zhao Song, Anshumali Shrivastava, Ce Zhang, Yuandong Tian, Christopher Re, et al.
  Deja vu: Contextual sparsity for efficient llms at inference time.
  In International Conference on Machine Learning, pages 22137–22176. PMLR, 2023.
- [45]

  Zirui Liu, Jiayi Yuan, Hongye Jin, Shaochen Zhong, Zhaozhuo Xu, Vladimir Braverman, Beidi Chen, and Xia Hu.
  Kivi: A tuning-free asymmetric 2bit quantization for kv cache.
  arXiv preprint arXiv:2402.02750, 2024.
- [46]

  Yuning Mao, Pengcheng He, Xiaodong Liu, Yelong Shen, Jianfeng Gao, Jiawei Han, and Weizhu Chen.
  Generation-augmented retrieval for open-domain question answering.
  arXiv preprint arXiv:2009.08553, 2020.
- [47]

  Jason Phang, Haokun Liu, and Samuel R Bowman.
  Fine-tuned transformers show clusters of similar representations across layers.
  arXiv preprint arXiv:2109.08406, 2021.
- [48]

  Ori Ram, Yoav Levine, Itay Dalmedigos, Dor Muhlgay, Amnon Shashua, Kevin Leyton-Brown, and Yoav Shoham.
  In-context retrieval-augmented language models.
  Transactions of the Association for Computational Linguistics, 11:1316–1331, 2023.
- [49]

  Nils Reimers and Iryna Gurevych.
  Sentence-bert: Sentence embeddings using siamese bert-networks.
  In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing. Association for Computational Linguistics, 11 2019.
- [50]

  Jianlin Su, Murtadha Ahmed, Yu Lu, Shengfeng Pan, Wen Bo, and Yunfeng Liu.
  Roformer: Enhanced transformer with rotary position embedding.
  Neurocomputing, 568:127063, 2024.
- [51]

  Harsh Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal.
  Musique: Multihop questions via single-hop question composition, 2022.
- [52]

  Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia Polosukhin.
  Attention Is All You Need, 2023.
- [53]

  Bingyang Wu, Shengyu Liu, Yinmin Zhong, Peng Sun, Xuanzhe Liu, and Xin Jin.
  Loongserve: Efficiently serving long-context large language models with elastic sequence parallelism, 2024.
- [54]

  Peng Xu, Wei Ping, Xianchao Wu, Lawrence McAfee, Chen Zhu, Zihan Liu, Sandeep Subramanian, Evelina Bakhturina, Mohammad Shoeybi, and Bryan Catanzaro.
  Retrieval meets long context large language models.
  arXiv preprint arXiv:2310.03025, 2023.
- [55]

  Wangsong Yin, Mengwei Xu, Yuanchun Li, and Xuanzhe Liu.
  Llm as a system service on mobile devices, 2024.
- [56]

  Alex Young, Bei Chen, Chao Li, Chengen Huang, Ge Zhang, Guanwei Zhang, Heng Li, Jiangcheng Zhu, Jianqun Chen, Jing Chang, et al.
  Yi: Open foundation models by 01. ai.
  arXiv preprint arXiv:2403.04652, 2024.
- [57]

  Gyeong-In Yu, Joo Seong Jeong, Geon-Woo Kim, Soojeong Kim, and Byung-Gon Chun.
  Orca: A distributed serving system for {\{Transformer-Based}\} generative models.
  In 16th USENIX Symposium on Operating Systems Design and Implementation (OSDI 22), pages 521–538, 2022.
- [58]

  Zhenyu Zhang, Ying Sheng, Tianyi Zhou, Tianlong Chen, Lianmin Zheng, Ruisi Cai, Zhao Song, Yuandong Tian, Christopher Ré, Clark Barrett, et al.
  H2o: Heavy-hitter oracle for efficient generative inference of large language models.
  Advances in Neural Information Processing Systems, 36, 2024.
- [59]

  Lianmin Zheng, Liangsheng Yin, Zhiqiang Xie, Jeff Huang, Chuyue Sun, Cody Hao Yu, Shiyi Cao, Christos Kozyrakis, Ion Stoica, Joseph E Gonzalez, et al.
  Efficiently programming large language models using sglang.
  arXiv preprint arXiv:2312.07104, 2023.
- [60]

  Yinmin Zhong, Shengyu Liu, Junda Chen, Jianbo Hu, Yibo Zhu, Xuanzhe Liu, Xin Jin, and Hao Zhang.
  Distserve: Disaggregating prefill and decoding for goodput-optimized large language model serving.
  arXiv preprint arXiv:2401.09670, 2024.

## 附录 A N 维位置恢复

这里我们证明位置恢复方法在 $N$ 维场景下仍然有效。我们先给出 $N$ 维空间中 RoPE 的定义。

###### 定义 0（旋转位置编码 ROPE [50]）.

设向量 ${q},{k}\in\mathbb{R}^{d}$ 为需要嵌入到某个位置 $m$ 的查询向量与键向量，记嵌入后为 ${q}_{m},{k}_{m}\in\mathbb{R}^{d}$。RoPE 按下式编码位置信息：

$$
{q}_{m},{k}_{m}=\mathbb{R}^{d}_{\Theta,m}\{q,k\}
$$

其中

$$
\mathbb{R}^{d}_{\Theta,m}=\begin{pmatrix}\cos m\theta_{0}&-\sin m\theta_{0}&...&0&0\\ \sin m\theta_{0}&\cos m\theta_{0}&...&0&0\\ \vdots&\vdots&\ddots&\vdots&\vdots\\ 0&0&\vdots&\cos m\theta_{\frac{d}{2}-1}&-\sin m\theta_{\frac{d}{2}-1}\\ 0&0&\vdots&\sin m\theta_{\frac{d}{2}-1}&\cos m\theta_{\frac{d}{2}-1}\\ \end{pmatrix}
$$

是旋转矩阵，超参数 $\Theta\in\{\theta_{i}=10000^{-2id},i\in[0,1,...,\frac{d}{2}-1]\}$。

我们的位置恢复方法之所以可行，是因为一对词元之间的注意力分数对它们的绝对位置保持不变。以下给出该不变性的证明。

###### 命题 A.2（RoPE 只依赖相对位置）.

设向量 ${k}\in\mathbb{R}^{d}$ 为键向量，${k}_{m}\in\mathbb{R}^{d}$ 为嵌入到固定位置 $m$ 的键向量；设向量 ${q}\in\mathbb{R}^{d}$ 为查询向量，${q}_{m+l}\in\mathbb{R}^{d}$ 为嵌入到位置 $(m+l)$ 的查询向量。则注意力分数 ${q}_{m+l}{k}_{m}$ 推导如下：

$$
\begin{aligned}
(1)\qquad {q}_{m+l}{k}_{m} &= {(\mathbb{R}^{d}_{\Theta,m+l}q)}^{T}{(\mathbb{R}^{d}_{\Theta,m}k)}\\
&=\sum_{i=0}^{d/2-1}\left(q_{[2i]}k_{[2i]}\cos(m+l-m)\theta_{i}+q_{[2i+1]}k_{[2i+1]}\cos(m+l-m)\theta_{i}\right)\\
&=\sum_{i=0}^{d/2-1}\left(q_{[2i]}k_{[2i]}+q_{[2i+1]}k_{[2i+1]}\right)\cos l\theta_{i}
\end{aligned}
$$

其中 $\{q,k\}_{[i]}$ 表示向量 $\{q,k\}$ 的第 $i$ 个分量，${h}_{i}$ 表示点积 ${q}_{i}{k}_{i}$。注意力分数 ${q}_{m+l}{k}_{m}$ 只依赖相对距离 $l$ 而非绝对位置 $m$。
