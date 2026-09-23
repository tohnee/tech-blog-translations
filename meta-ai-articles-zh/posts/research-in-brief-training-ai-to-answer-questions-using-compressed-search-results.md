---
title: "研究简报：训练 AI 利用压缩后的搜索结果回答问题"
title_en: "Research in Brief: Training AI to Answer Questions Using Compressed Search Results"
date: 2019-03-15
source: https://ai.facebook.com/blog/research-in-brief-training-ai-to-answer-questions-using-compressed-search-results
crawled: 2026-09-22
translated: 2026-09-22
---

# 研究简报：训练 AI 利用压缩后的搜索结果回答问题

> 原文：[Research in Brief: Training AI to Answer Questions Using Compressed Search Results](https://ai.facebook.com/blog/research-in-brief-training-ai-to-answer-questions-using-compressed-search-results) · Meta AI（Wayback 存档）

**研究内容：** 一种通过让长文本问答（QA）系统更高效地搜索相关文本来提升其性能的新方法。该方法建立在 Facebook AI 长文本问答工作之上——这是一项自然语言处理（NLP）研究任务，模型必须利用网络搜索前 100 条结果来回答诸如「阿尔伯特·爱因斯坦因何闻名？」这样的自然语言问题。虽然答案通常就存在于这些结果之中，但序列到序列（seq2seq）模型难以分析如此大量的数据——这需要处理数十万个词。通过把文本压缩为知识图谱并引入更细粒度的注意力机制，我们的技术让模型能够利用全部网络搜索结果来解读相关信息。

**工作原理：** 我们的方法分为两步：先凝缩可用的训练数据，再提取最相关的信息。第一步使用开放信息抽取系统分析网络搜索的结果。该系统识别「三元组」，即包含主语、关系以及一个或多个宾语的句子成分。例如，句子「广义相对论是一种引力理论」被转换为「广义相对论」（主语）、「是」（关系）和「一种引力理论」（宾语）。系统把这些三元组转换为局部知识图谱，主语和宾语表示为节点，连接它们的关系作为边。随着系统分析更多搜索结果，它会丢弃无关和冗余的信息。这一方法把模型必须处理的文本量减少了近 30 倍——从 30 万词降到 1 万词——同时还提升了准确性。

（原文此处嵌入视频：Something Went Wrong We're having trouble playing this video. Learn more）

随后，知识图谱被线性化为序列，交给标准的 seq2seq 模型来生成对原始问题的回答。我们修改了 seq2seq 模型的注意力机制，进一步让模型聚焦于最显著的信息，而非序列中的所有位置。这种知识凝缩与蒸馏的过程，使系统能把来自多种来源的众多事实转化为一段连贯的多句回答，例如：「阿尔伯特·爱因斯坦对物理学领域做出了许多贡献，包括广义相对论。广义相对论是对万有引力定律的精炼，把引力描述为时空的一种性质。」

**为什么重要：** 通过更高效、更有效地搜索互联网来回答长文本问题，这项工作有望催生大规模文本处理方式与人类从多个来源提炼答案或摘要的方式相近的 AI 助手，其答案比现有技术所能产出的更细致、更有用。我们的成果还可以让其他类型的在线文本——尤其是包含相关与无关细节的各种长文本来源——对训练 NLP 模型更有用，并有望为各类 AI 系统带来更好的阅读理解能力。论文见下方；参加 EMNLP 2019 的读者可在当地时间 11 月 6 日（周三）16:30 至 18:00 的会议第 8 场（「机器学习」）了解更多。

阅读完整论文：Using local knowledge graph construction to scale seq2seq models to multi-document inputs（利用局部知识图谱构建将 seq2seq 模型扩展到多文档输入）

## 作者

Angela Fan

研究助理，Facebook AI
