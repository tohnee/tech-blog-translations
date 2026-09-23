---
title: "Meta 面向闽南语的新型 AI 语音翻译系统，为无文字语言开创全新方法"
title_en: "Meta's new AI-powered speech translation system for Hokkien pioneers a new approach for an unwritten language"
date: 2022-10-19
source: https://ai.meta.com/blog/ai-translation-hokkien
crawled: 2026-09-22
translated: 2026-09-22
---

# Meta 面向闽南语的新型 AI 语音翻译系统，为无文字语言开创全新方法

> 原文：[Meta's new AI-powered speech translation system for Hokkien pioneers a new approach for an unwritten language](https://ai.meta.com/blog/ai-translation-hokkien) · Meta AI（Wayback 存档）

2022 年 10 月 19 日

迄今为止，AI 翻译主要聚焦于书面语言。然而，全世界 7000 多种现存语言中，近半数以口语为主，没有标准或广泛使用的书写系统。这使得用标准技术构建机器翻译工具成为不可能——那些技术需要海量书面文本来训练 AI 模型。为应对这一挑战，我们构建了首个面向闽南语（Hokkien）这一以口语为主的语言的 AI 翻译系统。闽南语在海外华人社群中被广泛使用，但缺乏标准书面形式。我们的技术让闽南语使用者能够与英语使用者对话。这个开源翻译系统是 Meta「通用语音翻译器」（Universal Speech Translator，UST）项目的一部分，该项目正在开发新的 AI 方法，希望最终能对所有现存语言（包括以口语为主的语言）实现实时语音到语音翻译。我们相信，口头交流能帮助打破隔阂，把世界各地的人连接在一起——甚至在元宇宙中也是如此。为开发这个纯语音翻译系统，Meta 的 AI 研究者必须克服传统机器翻译系统的诸多挑战，包括数据收集、模型设计和评测。要把 UST 扩展到更多语言，我们还有很多工作要做。但与说任何语言的人自如交谈是人们长期以来的梦想，我们很高兴离实现它又近了一步。我们不仅开源了闽南语翻译模型，还开源了评测数据集和研究论文，以便他人复现并在我们的工作之上继续构建。

（原文此处嵌入视频：Something Went Wrong We're having trouble playing this video. Learn more）

## 克服训练数据挑战

收集足够的数据是我们构建闽南语翻译系统时面临的一大障碍。闽南语是一种所谓的低资源语言，与西班牙语或英语等相比，现成可用的训练数据并不充裕。此外，英译闽南语的人工译员相对稀少，使得为训练模型收集并标注数据十分困难。我们利用普通话作为中间语言来构建伪标签和人工翻译：先把英语（或闽南语）语音翻译成普通话文本，再翻译成闽南语（或英语）并加入训练数据。这一方法通过借助相近的高资源语言的数据，大幅提升了模型性能。

语音挖掘（speech mining）是另一种生成训练数据的途径。借助预训练语音编码器，我们能把闽南语语音嵌入编码到与其他语言相同的语义空间，而无需闽南语具备书面形式。可以把语义嵌入相近的闽南语语音与英语语音及文本对齐。然后我们再从文本合成英语语音，得到平行的闽南语—英语语音。

## 一种全新的建模方法

许多语音翻译系统依赖转写文本，或是语音到文本系统。但由于以口语为主的语言没有标准书面形式，产出转写文本作为翻译结果行不通。因此我们专注于语音到语音翻译。我们采用语音到单元翻译（speech-to-unit translation，S2UT），把输入语音直接翻译为声学单元序列——这是 Meta 此前首创的技术路径——然后再从单元生成波形。此外，我们采用 UnitY 实现两遍解码机制：第一遍解码器生成一种相关语言（普通话）的文本，第二遍解码器生成单元。

## 评测准确性

语音翻译系统通常用名为 ASR-BLEU 的指标评测：先用自动语音识别（ASR）把翻译出的语音转写为文本，再把转写文本与人工翻译文本比较、计算 BLEU 分数（一个标准的机器翻译指标）。然而，评测闽南语这类口语语言的语音翻译的挑战之一，在于它没有标准书写系统。为了实现自动评测，我们开发了一个把闽南语语音转写为标准拼音记法「台罗」（Tâi-lô）的系统。这一技术使我们能在音节层面计算 BLEU 分数，方便地比较不同方法的翻译质量。

除了开发闽南语—英语语音翻译的评测方法，我们还基于名为 Taiwanese Across Taiwan 的闽南语语音语料库，创建了首个闽南语—英语双向语音到语音翻译基准数据集。该基准数据集将开源，以鼓励更多研究者投身闽南语语音翻译，共同推动该领域取得进一步进展。

## 展望翻译的未来

在当前阶段，我们的方法能让说闽南语的人与说英语的人交谈。虽然该模型仍在完善中，一次只能翻译一个完整句子，但这是朝着未来实现语言间同声传译迈出的一步。我们在闽南语上首创的技术可以扩展到许多其他有文字和无文字的语言。为此，我们发布 SpeechMatrix——一个用 Meta 创新的数据挖掘技术 LASER 挖掘出的大规模语音到语音翻译语料库——它将使研究者能够创建自己的语音到语音翻译（S2ST）系统并在我们的工作之上继续构建。

Meta 近期在无监督语音识别（wav2vec-U）和无监督机器翻译（mBART）方面的进展，将为今后翻译更多口语语言的工作提供借鉴。我们在无监督学习上的进展证明了在完全没有人工标注的情况下构建高质量语音到语音翻译模型的可行性。该系统显著降低了扩展低资源语言覆盖面的门槛，因为其中许多语言根本没有标注数据。

AI 研究正在帮助打破现实世界和元宇宙中的语言障碍，目标是促进连接与相互理解。我们期待拓展这项研究，并在未来把它带给更多人。

- 闽南语直接语音到语音翻译（Hokkien direct speech-to-speech translation）
- SpeechMatrix
- 无监督直接语音到语音翻译（Unsupervised direct speech-to-speech translation）
- UnitY 直接语音到语音翻译（UnitY direct speech-to-speech translation）

这项工作由一个跨学科团队承担，成员包括：Al Youngblood、Amanda Kallet、Ana Paula Kirschner Mofarrej、Andy Chung、Angela Fan、Ann Lee、Benjamin Peloquin、Benoît Sagot、Brian Bui、Brian O'Horo、Carleigh Wood、Changhan Wang、Chloe Meyere、Chris Summers、Christopher Johnson、David Wu、Diana Otero、Eric Kaplan、Ethan Ye、Gopika Jhala、Gustavo Gandia Rivera、Hirofumi Inaguma、Holger Schwenk、Hongyu Gong、Ilia Kulikov、Iska Saric、Janice Lam、Jeff Wang、Jingfei Du、Juan Pino、Julia Vargas、Justine Kao、Karla Caraballo-Torres、Kevin Tran、Koklioong Loa、Lachlan Mackenzie、Michael Auli、Michael Friedrichs、Natalie Hereth、Ning Dong、Oliver Libaw、Orialis Valentin、Paden Tomasello、Paul-Ambroise Duquenne、Peng-Jen Chen、Pengwei Li、Robert Lee、Safiyyah Saleem、Sascha Brodsky、Semarley Jarrett、Sravya Popuri、TJ Krusinski、Vedanuj Goswami、Wei-Ning Hsu、Xutai Ma、Yilin Yang 和 Yun Tang。
