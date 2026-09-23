---
title: "SeamlessM4T：面向语音翻译的基础多模态模型"
title_en: "Bringing the world closer together with a foundational multimodal model for speech translation"
date: 2023-08-22
source: https://ai.meta.com/blog/seamless-m4t
crawled: 2026-09-22
translated: 2026-09-22
---

# SeamlessM4T：面向语音翻译的基础多模态模型

> 原文：[Bringing the world closer together with a foundational multimodal model for speech translation](https://ai.meta.com/blog/seamless-m4t) · Meta AI（Wayback 存档）

2023 年 8 月 22 日 · 7 分钟阅读

我们生活的世界从未如此互联——互联网、移动设备、社交媒体和通信平台在全球的普及，让人们能接触到比以往任何时候都多的多语言内容。在这样的背景下，按需用任何语言沟通和理解信息的能力变得越来越重要。虽然科幻作品长期以来一直梦想着这种能力，但 AI 正在把这一愿景变成技术现实。

今天，我们介绍 SeamlessM4T——一个跨语音与文本无缝翻译和转录的基础多语言多任务模型。SeamlessM4T 支持：

- 近 100 种语言的自动语音识别
- 近 100 种输入和输出语言的语音到文本翻译
- 语音到语音翻译，支持近 100 种输入语言和 35 种（+英语）输出语言
- 近 100 种语言的文本到文本翻译
- 文本到语音翻译，支持近 100 种输入语言和 35 种（+英语）输出语言

秉承我们开放科学的方针，我们以 CC BY-NC 4.0 许可公开发布 SeamlessM4T，供研究者和开发者在此基础上构建。我们还在发布 SeamlessAlign 的元数据——迄今最大的开放多模态翻译数据集，共计 27 万小时挖掘得到的语音与文本对齐。借助 SONAR（一整套语音与文本句子编码器）和 stopes（我们的多模态数据处理与平行数据挖掘库），社区可以轻松对自己的单语数据集进行挖掘。所有研究进展都由我们的下一代序列建模库 fairseq2 支撑。

构建一个通用语言翻译器——比如《银河系漫游指南》中虚构的巴别鱼（Babel Fish）——极具挑战性，因为现有的语音到语音和语音到文本系统只覆盖世界上语言的一小部分。SeamlessM4T 应对了语言覆盖有限以及依赖分离系统这两大挑战——后者把语音到语音翻译任务拆分为多个子系统的多个阶段——因而是语音到语音和语音到文本领域的重大突破。这些系统可以利用大量数据，但通常只在一种模态上表现良好。我们面临的挑战是创建一个无所不能的统一多语言模型。我们相信今天宣布的工作是这一征程上的重要一步。我们的单一模型提供按需翻译，让说不同语言的人们能够更有效地沟通。我们显著提升了所支持的低资源和中资源语言的性能——这些语言的数字语言足迹较小。同时我们在英语、西班牙语、德语等高资源语言上保持了强劲表现。SeamlessM4T 隐式识别源语言，无需单独的语言识别模型。

这项工作建立在 Meta 及其他机构多年来在创造通用翻译器方面的进展之上。去年，我们发布了 No Language Left Behind（NLLB）——一个支持 200 种语言的文本到文本机器翻译模型，此后已作为翻译提供方之一集成到维基百科中。几个月后，我们分享了通用语音翻译器（Universal Speech Translator）的演示——这是首个面向闽南语的直接语音到语音翻译系统，而闽南语是一种没有广泛使用的书写系统的语言。通过这项工作，我们开发了 SpeechMatrix——首个大规模多语言语音到语音翻译数据集，它源自 SpeechLASER——监督表示学习的一项突破。今年早些时候，我们还分享了大规模多语言语音（Massively Multilingual Speech），提供覆盖 1100 多种语言的自动语音识别、语言识别和语音合成技术。SeamlessM4T 汲取了所有这些项目的成果，以单一模型实现多语言多模态的翻译体验，构建于广泛的口语数据源之上，并取得了业界领先的结果。

## 我们的方法

构建统一模型需要一个轻量、且易于与 PyTorch 生态其他现代库组合的序列建模工具包。我们重新设计了最初的序列建模工具包 fairseq。凭借更高效的建模与数据加载 API，fairseq2 为 SeamlessM4T 背后的建模提供了动力。

在模型方面，我们采用多任务 UnitY 模型架构，它能够直接生成翻译文本和语音。这一新架构还支持自动语音识别、文本到文本、文本到语音、语音到文本和语音到语音翻译——这些已是原版 UnitY 模型的一部分。多任务 UnitY 模型由三个主要的顺序组件构成。文本和语音编码器的任务是识别近 100 种语言的语音输入。文本解码器随后把含义转换到近 100 种语言的文本，再由 text-to-unit 模型解码为 36 种语音语言的离散声学单元。自监督编码器、语音到文本、文本到文本翻译组件和 text-to-unit 模型都经过预训练，以提升模型质量和训练稳定性。解码得到的离散单元随后用多语言 HiFi-GAN unit 声码器转换为语音。

### 编码器如何处理语音

我们的自监督语音编码器 w2v-BERT 2.0——w2v-BERT 的改进版，提升了训练稳定性和表示质量——通过分析数百万小时的多语言语音，学会在语音中发现结构和含义。编码器接收音频信号，将其分解为更小的部分，并构建所说内容的内部表示。由于口语单词由许多这样的声音和字符组成，我们使用一个长度适配器把它们粗略映射到实际单词。

### 编码器如何处理文本

类似地，我们有一个基于 NLLB 模型的文本编码器。它经过训练，能理解近 100 种语言的文本并产生对翻译有用的表示。

### 生成文本

我们的文本解码器经过训练，可接收编码后的语音表示或文本表示。这既适用于同语言任务（如自动语音识别），也适用于多语言翻译任务。例如，某人可以用法语说出「bonjour」，并期望斯瓦希里语的译文是「habari」。通过多任务训练，我们利用强大的文本到文本翻译模型（NLLB）的优势，通过 token 级知识蒸馏来指导我们的语音到文本翻译模型。

### 生成语音

我们在目标侧使用声学单元来表示语音。UnitY 模型中的 text-to-unit（T2U）组件基于文本输出生成这些离散语音单元，并在 UnitY 微调之前先在 ASR 数据上预训练。随后使用多语言 HiFi-GAN unit 声码器把这些离散单元转换为音频波形。

## 数据扩展

像 SeamlessM4T 这样的数据驱动模型通常受益于大量高质量的端到端数据，即语音到文本和语音到语音数据。仅依赖人工转录和翻译的语音，无法扩展到 100 种语言语音翻译这一艰巨任务。我们在文本到文本挖掘（利用联合嵌入空间中的相似性度量）方面的开创性工作以及语音挖掘的初步工作之上，创建了训练 SeamlessM4T 模型的额外资源。首先，我们为 200 种语言构建了全新的大规模多语言多模态文本嵌入空间，命名为 SONAR（Sentence-level Multimodal and Language-Agnostic Representations，句子级模态与语言无关表示），它在多语言相似性搜索上大幅优于 LASER3 或 LaBSE 等现有方法。然后，我们采用教师-学生方法把这一嵌入空间扩展到语音模态，目前覆盖 36 种语言。挖掘在公开网络数据仓库（数百亿句子）和语音（400 万小时）数据上进行。我们总共自动对齐了超过 44.3 万小时的语音与文本，并创建了约 2.9 万小时的语音到语音对齐。这一被称为 SeamlessAlign 的语料库，就总体规模和语言覆盖而言是迄今最大的开放语音/语音和语音/文本平行语料库。

## 结果

在这些任务和语言上，SeamlessM4T 在近 100 种语言上取得了业界领先的结果，并在单一模型中支持自动语音识别、语音到文本、语音到语音、文本到语音和文本到文本翻译的多任务能力。我们还显著提升了所支持的低资源和中资源语言的性能，并在高资源语言上保持强劲表现。为了在不依赖文本指标的情况下更准确地评估系统，我们把我们的无文本指标扩展为 BLASER 2.0，现在可以在语音和文本单元之间进行评估，准确率与前代相当。

在鲁棒性测试中，与当前最先进模型相比，我们的系统在语音到文本任务中对背景噪声和说话人变化的表现更好（平均分别提升 37% 和 48%）。SeamlessM4T 也优于此前最先进的竞争者。

## 我们如何负责任地构建 SeamlessM4T

翻译系统的准确性至关重要。与所有 AI 系统一样，模型存在固有风险：可能错误转录人们想表达的内容，或生成有毒性或不准确的输出。在 Meta，我们的 AI 研发遵循由我们负责任 AI 五大支柱指导的框架。秉承我们对负责任 AI 的承诺，我们针对毒性和偏见开展了研究，帮助了解模型哪些区域可能敏感。

针对毒性，我们把高度多语言的毒性分类器扩展到语音，帮助从语音输入和输出中识别毒性词。我们过滤了训练数据中不平衡的毒性：如果输入或输出含有不同量的毒性，我们就移除该训练对。我们今天发布的演示展示了 SeamlessM4T 的能力，也是这项研究的重要组成部分。我们在演示中对输入和输出都进行毒性检测。如果只在输出中检测到毒性，则意味着毒性是被新增的。这种情况下，我们会给出警告且不显示输出。与最先进水平相比，我们的模型在语音到语音和语音到文本翻译上显著减少了新增毒性。

性别偏见——结果不公平地偏向某一性别、有时默认为性别刻板印象——是我们开始大规模评估的另一个领域。通过把此前设计的多语言 HolisticBias 数据集扩展到语音，我们现在能够量化数十个语音翻译方向上的性别偏见。我们在安全领域的工作仍在持续。我们将继续在这一领域研究并采取行动，持续改进 SeamlessM4T，减少我们在模型中看到的任何毒性实例。

## 开放我们的技术

凭借业界领先的结果，我们相信 SeamlessM4T 是 AI 社区追求通用多任务系统之路上的重要突破。秉承我们开放科学的方针，我们很高兴公开分享我们的模型，供研究者和开发者在这项技术之上构建。这只是我们持续构建跨语言连接人们的 AI 技术努力的最新一步。未来，我们想探索这一基础模型如何催生新的沟通能力——最终让我们更接近一个人人都能被理解的世界。

阅读论文 / 试用演示 / 下载代码、模型和数据 / 试用 Hugging Face 演示

这篇博文得益于以下同事的工作：Bapi Akula、Pierre Andrews、Can Balioglu、Loïc Barrault、Onur Çelebi、Peng-Jen Chen、Yu-An Chung、Mariano Cora Meglioli、David Dale、Ning Dong、Paul-Ambroise Duquenne、Naji El Hachem、Maha Elbayad、Brian Ellis、Hady Elsahar、Cynthia Gao、Hongyu Gong、Francisco Guzmán、Justin Haaheim、Prangthip Hansanti、Kevin Heffernan、John Hoffman、Russ Howes、Bernie Huang、Min-Jae Hwang、Hirofumi Inaguma、Somya Jain、Elahe Kalbassi、Amanda Kallet、Justine Kao、Christopher Klaiber、Ilia Kulikov、Janice Lam、Ann Lee、Daniel Li、Pengwei Li、Daniel Licht、Xutai Ma、Jean Maillard、Ruslan Mavlyutov、Gabriel Mejia Gonzalez、Alexandre Mourachko、Benjamin Peloquin、Juan Pino、Sravya Popuri、Marta R. Costa-jussà、Alice Rakotoarison、Kaushik Ram Sadagopan、Mohamed Ramadan、Abinesh Ramakrishnan、Christophe Ropers、Safiyyah Saleem、Holger Schwenk、Anna Sun、Paden Tomasello、Kevin Tran、Tuan Tran、Igor Tufanov、Vish Vogeti、Changhan Wang、Jeff Wang、Skyler Wang、Guillaume Wenzek、Carleigh Wood、Yilin Yang、Ethan Ye 和 Bokai Yu。
