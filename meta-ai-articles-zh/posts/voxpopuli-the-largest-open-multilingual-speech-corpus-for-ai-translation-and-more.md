---
title: "VoxPopuli：面向 AI 翻译等任务的最大开源多语言语音语料库"
title_en: "VoxPopuli: The largest open multilingual speech corpus for AI translation and more"
date: 2021-08-02
source: https://ai.facebook.com/blog/voxpopuli-the-largest-open-multilingual-speech-corpus-for-ai-translation-and-more
crawled: 2026-09-22
translated: 2026-09-22
---

# VoxPopuli：面向 AI 翻译等任务的最大开源多语言语音语料库

> 原文：[VoxPopuli: The largest open multilingual speech corpus for AI translation and more](https://ai.facebook.com/blog/voxpopuli-the-largest-open-multilingual-speech-corpus-for-ai-translation-and-more) · Meta AI（Wayback 存档）

2021 年 8 月 2 日

**研究内容：** 语音识别与翻译技术正被广泛采用，以实现人机交互、实时的人际沟通，以及无语言障碍地访问多媒体内容。然而这些技术目前仅支持少数几种广泛使用的语言，而全球约有 6500 种语言。要变得更有用，这些 AI 系统需要支持更多语言。为加速创建可在世界更多地区使用的新自然语言处理（NLP）系统，Facebook AI 发布 VoxPopuli——一个大规模多语言录音语料库，提供 23 种语言共 40 万小时的无标注语音数据。它是迄今为止为自监督学习和半监督学习发布的最大开源数据集。VoxPopuli 还包含 15 种语言共 1800 小时的带转写演讲，并把它们的口译整合为 15 种目标语言、总计 1.73 万小时的数据，且带有语句级（utterance level）对齐（可以是一个词、一句话，或「嗯」这样的独立声音）。

实现数十种语言的高级 NLP 这一现实目标，是一项耗时的工程。近期的自动化进展（wav2vec 2.0 和 wav2vec-U）在减少甚至消除构建这些技术所需的标注数据方面显示出可期的结果，它们基于从大规模无标注数据学习。以往的开源语音数据集（如 Libri-light）在规模或语言覆盖上有限，制约了这些技术的全部潜力。AI 研究社区就是需要更多语言数据——多得多。VoxPopuli 为每种语言提供 9000 到 1.8 万小时的无标注语音；以往数据集每种语言只有约 130 小时。这一大批新的语音到语音翻译数据，将成为 CoVoST V2 等现有语音到文本翻译语料库的重要补充。

**工作原理：** 我们从公开的欧洲议会活动录音中收集了 23 种语言的数据，并构建处理流水线：按说话人或静音切分语音音频，将其与转写或翻译正确对齐，并过滤掉转写不准确的样本。我们提供了语音识别（ASR）基线，用于在具有挑战性的域外设置下，基准测试并验证 VoxPopuli 无标注数据在半监督 ASR 和语音到文本翻译中的多功能性。我们表明，VoxPopuli 中无标注数据量与语言覆盖的增加，对从质量和鲁棒性两方面改进自监督模型都非常有帮助。团队还在语音翻译基准上评估了自动语音到语音对齐，发现其质量很高。

**为什么重要：** 让高级语音技术支持更多语言，需要的不仅是有限的标注数据，还有大规模的无标注数据集。VoxPopuli 通过提供英语之外更大规模的数据，推动了这些前景广阔的研究方向——例如罗马尼亚语（3000 万使用者）和希腊语（1350 万使用者），这些语言使用者众多却缺乏开放数据（甚至无标注数据）。VoxPopuli 还以大量标注数据解锁了直接语音到语音翻译的开放研究。我们期待看到 AI 研究社区的其他人如何利用 VoxPopuli，创建服务全球更多人的新 NLP 系统。

在 GitHub 上获取 | 阅读论文

**作者**
- Changhan Wang，研究工程师
- Morgane Riviere，研究工程师
- Ann Lee，研究科学家
- Anne Wu，AI 驻留研究者
- Chaitanya Talnikar，AI 驻留研究者
- Daniel Haziza，软件工程师
- Mary Williamson，研究工程经理
- Juan Pino，研究科学家
- Emmanuel Dupoux，研究科学家
