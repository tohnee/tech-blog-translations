---
title: "CoVoST V2：扩展规模最大、最多样的多语言语音到文本翻译数据集"
title_en: "CoVoST V2: Expanding the largest, most diverse multilingual speech-to-text translation dataset"
date: 2020-07-21
source: https://ai.facebook.com/blog/covost-v2-expanding-the-largest-most-diverse-multilingual-speech-to-text-translation-data-set
crawled: 2026-09-22
translated: 2026-09-22
---

# CoVoST V2：扩展规模最大、最多样的多语言语音到文本翻译数据集

> 原文：[CoVoST V2: Expanding the largest, most diverse multilingual speech-to-text translation dataset](https://ai.facebook.com/blog/covost-v2-expanding-the-largest-most-diverse-multilingual-speech-to-text-translation-data-set) · Meta AI（Wayback 存档）

**这项研究是什么：**CoVoST V2 是对我们 CoVoST 数据集的扩展——一个面向多语言翻译的语音到文本翻译（ST）语料库。这次新发布提供了迄今最大的多语言 ST 数据集。CoVoST V2 将支持把 21 种语言翻译成英语，以及把英语翻译成 15 种语言。为了支持多语言语音翻译更广泛的研究与应用，我们以知识共享（CC0）许可证免费开放 CoVoST V2。

初版 CoVoST 于 2019 年开发，使用 Mozilla 开源的 Common Voice 众包语音录音数据库，创建了一个覆盖 11 种语言到英语的翻译语料库，说话人与口音多样。开发这第一版的目的是促进多对一多语言语音翻译的研究，因为以往的数据集要么局限于非常特定的领域、资源稀少，要么只包含以英语为源语言的语言对。

**工作原理：**CoVoST V1 涵盖超过 11000 名说话人和 60 种口音，共包含 708 小时的法语、德语、荷兰语、俄语、西班牙语、意大利语、土耳其语、波斯语、瑞典语、蒙古语和汉语样本。在 V2 中，我们新增了威尔士语、加泰罗尼亚语、斯洛文尼亚语、爱沙尼亚语、印尼语、阿拉伯语、泰米尔语、葡萄牙语、拉脱维亚语和日语的语音翻译数据。语料库现共收录 2900 小时语音。我们选择 Common Voice 数据库，是因为它提供了多样化的样本（不同性别、年龄段和口音），而且库中每段音频都经过 Common Voice 社区的仔细审查与验证。随后我们又应用了一系列自有的检查手段来把控翻译质量。

我们在以下任务上使用官方的训练-开发-测试划分提供了基线：自动语音识别、机器翻译和语音翻译。我们还评估了 CoVoST V1 在不同说话人间翻译同一短语时的准确性。Tatoeba 数据库提供了使用额外数据评估在 CoVoST 上训练的模型的选项。

**为什么重要：**借助 CoVoST V2，我们的目标是促进大规模多语言语音翻译研究，迈向覆盖众多语言对的单一模型。这样做将改善可维护性与质量——尤其是对数据较少的语言对。Facebook 上的人们使用或阅读 100 多种不同的语言。我们的目标是减少不同文化之间的在线交流障碍。除非一个人会说两种或多种语言，否则他们很难高效、有效地向他人发出自己的声音。我们希望不让任何一种语言掉队，这正是我们开源 CoVoST V2 的原因。凭借这一数据集和我们自己的基线结果，我们旨在为研究者和开发者奠定基础，创造新工具以消除语言障碍，为 Facebook 及整个互联网的用户打造全球化的交流体验。

阅读完整论文：CoVoST 2: A Massively Multilingual Speech-to-Text Translation Corpus
