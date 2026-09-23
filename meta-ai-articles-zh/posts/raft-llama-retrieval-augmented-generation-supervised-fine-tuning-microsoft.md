---
title: "RAFT：让 Llama 驶向更好的领域特定 RAG"
title_en: "RAFT: Sailing Llama towards better domain-specific RAG"
date: 2024-05-07
source: https://ai.meta.com/blog/raft-llama-retrieval-augmented-generation-supervised-fine-tuning-microsoft
crawled: 2026-09-22
translated: 2026-09-22
---

# RAFT：让 Llama 驶向更好的领域特定 RAG

> 原文：[RAFT: Sailing Llama towards better domain-specific RAG](https://ai.meta.com/blog/raft-llama-retrieval-augmented-generation-supervised-fine-tuning-microsoft) · Meta AI（Wayback 存档）

2024 年 5 月 7 日

检索增强微调（Retrieval-Augmented Fine-Tuning，RAFT）结合了检索增强生成（RAG）与监督微调（SFT）的优势，实现更好的领域适应。原始 RAFT 博文见 Microsoft TechCommunity。

## 引言

像 Meta Llama 2 这样的预训练模型在广泛的主题上接受过训练，因此能够就广泛主题的查询生成信息丰富的回答。然而许多用例要求模型专门针对某个领域，并在生成回答时利用领域特定信息。目前有两种做法：

- 领域特定监督微调（DSF）：在一组代表领域特定知识的文档上训练现有的基础模型。
- 检索增强生成（RAG）：把这些文档存储在向量数据库中，在查询时检索与问题语义相似的文档，并用其内容作为大语言模型生成回答的上下文。

在本文中，我们将审视这两种方法的局限，以及加州大学伯克利分校的研究者 Tianjun Zhang 和 Shishir G. Patil 所在团队可能刚刚发现的一种更好方法。这个曾以 Gorilla LLM 闻名的团队在他们的 RAFT 论文（Retrieval Augmented Fine Tuning，检索增强微调）中展示了如何通过 MaaS 在 Azure AI Studio 上使用 Meta Llama 2 开展研究并实现他们的方法。伯克利团队还发表了一篇关于该论文的博文，解释了先前方法的优缺点，以及 RAFT 方法如何产生更有效的结果。RAFT 论文的实现已在他们的 GitHub 仓库提供。

我们先概览一下 RAFT 方法的工作原理。

## 理解 RAFT 方法

在传统 RAG 中，当模型收到一个查询时，它从索引中检索若干可能包含答案的文档，把这些文档作为上下文来生成对用户查询的回答。使用微调时，模型回答查询就像学生参加闭卷考试；使用 RAG 时，这个场景类似开卷考试——学生可以完全访问教科书来寻找答案。开卷考试比闭卷考试更容易解决，这解释了 RAG 的有效性和流行度。

两种方法都有局限。微调的模型不仅受限于其训练内容，还容易出现近似和幻觉。RAG 的模型是「接地」（grounded）的，即其回答基于语料库中的某些参考文档。这些参考文档是根据与查询的语义相似性检索的；模型其实并不知道哪些文档真正相关、哪些只是干扰项。这些「干扰」文档即使不是合理论证答案的好来源，也可能被拉进模型的上下文。

Tianjun 和 Shishir 希望改进 RAG 的这些缺陷。他们假设：在开卷考试之前学习过教科书的学生，比只在考试期间翻书的学生更可能表现更好。把这一点翻译回大语言模型：如果模型事先「学习」过这些文档，能否提升其 RAG 表现？他们的方法——检索增强微调——试图让模型在被用于 RAG 设置之前先学习或适应某个领域。

使用 Meta Llama 2 7B 语言模型，他们首先准备一个合成数据集，其中每个样本包含：

- 一个问题
- 一组参考文档，其中既有包含相关信息的文档，也有不包含任何与回答问题相关信息、因而可以安全忽略的文档
- 一个由这些文档生成的答案
- 一段思维链（Chain-of-Thought，CoT）解释，其中包含来自相关文档的摘录

该数据集用于以标准监督训练微调 Meta Llama 2 7B 模型。此时模型更好地适应了领域；它不仅让语气和风格与领域数据集对齐，也更擅长从检索到的上下文中提取有用的信息片段。思维链推理的加入防止了过拟合并提升了训练鲁棒性。

RAFT 位于 RAG 与 DSF 的中间地带。它既让大语言模型预先吸收领域知识和风格（类似 DSF），又提升从检索上下文生成答案的质量。由于 Meta Llama 2 等预训练模型在多样化的领域上训练，RAFT 之类的技术可以让它们更适合医疗、法律数据集这样的小众领域。

## 与 RAFT 研究者的问答

我们有机会向伯克利团队请教他们使用 Meta Llama 做 RAFT 的经验。

**你们为什么选择 Meta Llama 2 7B？**

**RAFT 研究者：** 我们选择 Meta Llama 2 7B，是因为我们关注 RAG 任务——这类任务要求模型兼具推理能力、语言理解能力、较低延迟的推理，以及对多样化场景的易适应性。Meta Llama 2 7B 很符合要求：它是很多通识问答任务的良好基础模型，数学能力令人鼓舞，而且凭借 4096 token 的上下文长度能够解析相当长的文档。Meta Llama 2 7B 也非常适合在四块 A100-40G GPU 上训练、在单块 GPU 上服务。在性能、部署便利性和合适许可证的帕累托曲线上，Meta Llama 2 模型非常适合 RAFT 任务。借助 Microsoft AI studio，我们也很乐意探索 Meta Llama 2 13B 或 70B。

**对想要微调 Meta Llama 的人，你们有什么建议？在微调大语言模型方面你们在实践中学到了哪些最佳实践？**

**RAFT 研究者：** 微调 Meta Llama 通常是一项复杂任务，涉及数据收集、数据清洗和实际微调。在数据方面，我们建议收集领域内多样化的问题，并构造思维链（CoT）答案（我们的 RAFT 论文中也有论述）。我们还建议保存中间检查点，这有助于早停。同样关键的是，把微调学习率设置为至少比预训练时低一个数量级。除此之外，通常的最佳实践也推荐：16 位精度、训练不超过 3 个 epoch、使用大批量。

**微调应该针对每个领域分别做吗？还是微调后的模型通常在多个领域的 RAG 上都更好？**

**RAFT 研究者：** 微调后模型的性能在知识上依赖于领域（它训练所用的文档），但在行为上能在一定程度上跨领域泛化。准确率与泛化之间存在轻微的权衡。通常针对一个领域微调是好做法，但针对有限的一组企业文档微调可能带来更好的性能，因为知识范围严格更窄。

## 结论

RAFT 方法是语言模型微调领域的重要一步。它不仅提升了生成答案的质量，还增强了模型从检索上下文中提取有用信息的能力。因此，它在各个领域的未来应用中潜力巨大。本研究对 Meta Llama 2 7B 语言模型的使用展示了该模型在处理多样化任务时的多功能性和适应性。团队的经验和建议为希望微调 Meta Llama 或类似模型的人提供了宝贵洞见。Azure AI Studio 进一步让最先进的生成式 AI 能力大众化。该平台简化了微调、测试和部署流程，让开发者和企业无需深厚的机器学习专业知识就能创建创新且定制的解决方案。

了解更多关于 RAFT 与 Azure 模型即服务（Models-as-a-Service）上的 Meta Llama：

- 关于 Meta Llama 的更多信息：Llama.meta.com
- 通过 MaaS 在 Azure AI Studio 上的 Llama-2-7b-chat
- 在 Azure 上微调 Meta Llama 2：在 Azure AI Studio 中微调 Llama 2 模型，或阅读其技术博客

## 作者

Suraj Subramanian

AI 倡导者，Meta

Cedric Vidal

首席 AI 倡导者，Microsoft
