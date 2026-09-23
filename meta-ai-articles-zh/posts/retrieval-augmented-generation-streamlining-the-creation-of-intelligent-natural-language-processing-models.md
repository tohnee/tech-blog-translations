---
title: "检索增强生成：简化智能自然语言处理模型的创建"
title_en: "Retrieval Augmented Generation: Streamlining the creation of intelligent natural language processing models"
date: 2020-09-28
source: https://ai.meta.com/blog/retrieval-augmented-generation-streamlining-the-creation-of-intelligent-natural-language-processing-models
crawled: 2026-09-22
translated: 2026-09-22
---

# 检索增强生成：简化智能自然语言处理模型的创建

> 原文：[Retrieval Augmented Generation: Streamlining the creation of intelligent natural language processing models](https://ai.meta.com/blog/retrieval-augmented-generation-streamlining-the-creation-of-intelligent-natural-language-processing-models) · Meta AI（Wayback 存档）

2020 年 9 月 28 日

教计算机理解人类的书写和言说——即自然语言处理（NLP）——是 AI 研究中最古老的挑战之一。然而过去两年，研究方式发生了显著变化。过去研究专注于为特定任务开发特定框架，而今天，强大的通用语言模型可以针对多种不同任务进行微调。这些努力虽有前景，但迄今为止都是把这些通用模型应用于人类无需额外背景知识即可解决的任务（如情感分析）。构建一个会研究和建立语境的模型更具挑战性，但对未来的进步至关重要。

我们最近在这一领域取得了实质性进展：我们的检索增强生成（Retrieval Augmented Generation，RAG）架构，是一个端到端可微模型，把信息检索组件（Facebook AI 的稠密段落检索系统）与 seq2seq 生成器（我们的双向自回归 Transformer [BART] 模型）相结合。RAG 可以在知识密集型下游任务上微调，取得甚至超越最大预训练 seq2seq 语言模型的最先进结果。而且与这些预训练模型不同，RAG 的内部知识可以随时轻松更改甚至补充，让研究员和工程师得以控制 RAG 知道什么、不知道什么，而不必浪费时间和算力重训整个模型。

## 结合「开卷」与「闭卷」的优势

RAG 的外观和行为都像标准 seq2seq 模型——输入一个序列，输出对应的序列。但有一个中间步骤，使 RAG 区别并超越于普通 seq2seq 方法。RAG 不是把输入直接传给生成器，而是用输入检索一组相关文档——在我们的场景中来自维基百科。例如，给定提示「第一只哺乳动物何时出现在地球上？」，RAG 可能调出「哺乳动物」「地球历史」「哺乳动物演化」的文档。这些支撑文档随后与原始输入拼接为上下文，喂给产出实际输出的 seq2seq 模型。

因此 RAG 有两个知识来源：seq2seq 模型存储在其参数中的知识（参数化记忆），以及存储在 RAG 检索段落的语料库中的知识（非参数化记忆）。这两个来源相辅相成。我们发现，RAG 用非参数化记忆来「提示」seq2seq 模型生成正确回答，实质上把「闭卷」（纯参数化）方法的灵活性与「开卷」（基于检索）方法的性能结合了起来。

RAG 采用一种后期融合（late fusion）形式来整合所有检索文档中的知识：它对「文档-问题」对分别做出回答预测，然后聚合最终预测得分。关键在于，后期融合让我们可以把输出中的误差信号反向传播到检索机制，从而大幅提升端到端系统的性能。

（原文此处嵌入视频：Something Went Wrong We're having trouble playing this video. To watch the video, please upgrade your web browser. Learn more）

即使在纯抽取式任务（如开放域 NaturalQuestions 任务）中，把基于检索的组件与生成式组件相结合也有优势。当 RAG 能接触到包含正确答案线索但从未逐字给出答案的文档时，性能会提升；而且在某些情况下，即使正确答案在任何检索到的文档中都找不到，RAG 也能生成正确答案。我们用 RAG 在 NaturalQuestions、CuratedTrec 和 WebQuestions 上取得了非常强的结果，证明用生成式（而非抽取式）阅读器也能达到最先进的机器阅读性能。

不过，RAG 真正出色的是知识密集型自然语言生成，我们通过生成《危险边缘！》（Jeopardy!）问题进行了探索。RAG 生成的《危险边缘！》问题比同类最先进 seq2seq 模型更具体、更多样、更符合事实。我们的推测是，这得益于 RAG 综合来自多个来源的不同信息片段来合成回答的能力。

RAG 的真正优势在于其灵活性。改变预训练语言模型所知的内容，需要用新文档重训整个模型。而用 RAG，我们只需更换它用于知识检索的文档，就能控制它知道什么。我们测试了这一行为：把原来的维基百科数据集换成更旧的版本，然后问「冰岛总理是谁？」等问题。结果表明，尽管参数化知识保持不变，RAG 利用换入语料库中的知识调整了回答。这种自适应方式在事实（或我们对事实的理解）随时间演变的情况下极为宝贵。

## 为研究卸下训练负担

如果 AI 助手要在日常生活中发挥更大作用，它们不仅要能访问海量信息，更重要的是能访问正确的信息。鉴于世界变化之快，这对需要为哪怕微小变化进行持续算力密集型重训的预训练模型来说是重大挑战。RAG 让 NLP 模型绕过重训步骤，访问并利用最新信息，再用最先进的 seq2seq 生成器输出结果。这种交汇应能让未来的 NLP 模型更具适应性；事实上，我们已在一个相关的 Facebook AI 研究项目 Fusion-in-Decoder 中看到了强劲结果。

我们看到 RAG 的广泛潜力，这也是我们今天把它作为 Hugging Face transformer 库组件发布的原因。Hugging Face 的 Transformers 凭借低门槛和对最先进模型的覆盖，已成为开源 NLP 的事实标准，并与新的 Datasets 库集成，提供 RAG 所依赖的索引化知识源。现在随着 RAG 的加入，我们相信共同体将能把基于检索的生成应用于我们已探索过的知识密集型任务，以及一些我们尚未想象到的任务。RAG 让研究员和工程师只需五行代码，就能快速开发并部署针对自身知识密集型任务的解决方案。我们预见，未来的知识密集型任务研究有望像今天的情感分析等轻知识任务一样简单易行，潜力可期。

我们将于 12 月在 NeurIPS 2020 上展示 RAG，期间也期待看到共同体的反响。我们还计划继续深化这些想法：改进 RAG 的检索组件、扩展检索语料库和模型，并提升 RAG 在知识基准（如我们最近发布的 KILT 基准）上的整体性能。

## 作者

Sebastian Riedel

研究经理

Douwe Kiela

研究科学家

Patrick Lewis

FAIR 博士生

Aleksandra Piktus

软件工程师
