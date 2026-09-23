---
title: "教 AI 像孩子那样学习语音"
title_en: "Teaching AI to learn speech the way children do"
date: 2019-01-28
source: https://ai.facebook.com/blog/zerospeech-2019-challenge
crawled: 2026-09-22
translated: 2026-09-22
---

# 教 AI 像孩子那样学习语音

> 原文：[Teaching AI to learn speech the way children do](https://ai.facebook.com/blog/zerospeech-2019-challenge) · Meta AI（Wayback 存档）

2019 年 1 月 28 日

**挑战是什么：** 这是由 Facebook AI Research（FAIR，Meta 基础人工智能研究院）与巴黎文理研究大学（Paris Sciences & Lettres University）合作举办、并获微软研究院额外赞助的竞赛，旨在挑战其他研究者教会 AI 系统以一种更接近幼儿学习方式的方法学习语音。ZeroSpeech 2019 挑战赛（建立在 2015 年和 2017 年前两届的基础上）要求参赛者仅用音频输入构建一个语音合成器，不使用任何文本或音素标签。

**运作方式：** 挑战的核心任务是构建一个 AI 系统，能够在一种未知语言中发现相当于音素标签文本的机器对应物，并用它们以给定嗓音重新合成一句话。本质上，系统必须发现属于自己的离散「正字法」记法——它可能与语言学定义的子词单元（如辅音、元音和音节）相对应，也可能不对应。参赛者会得到原始音频，以及一个基线系统——其中一个组件执行子词发现，另一个执行语音合成。参赛者既可以用新的端到端系统替换基线，也可以改进基线的一个组件，以生成更高质量的波形。参赛作品将依据所发现标签集合的比特率以及整体波形质量来评估。提交截止日期为 3 月 15 日。得分最高或论文最具创新性的团队将被选中在 9 月的 Interspeech 会议上展示。

**为什么重要：** 复现儿童在学会读写之前先学会说话的方式，将有助于改进与数千种「低资源」语言相关的广泛 AI 任务——这些语言可用于训练 AI 系统的语言学或文本资源十分有限。这项挑战不仅将探索无监督学习技术（这是通向多功能、可扩展 AI 的重要追求方向），还将帮助把自动翻译和自然语言理解相关研究从以英语为中心的工作转向更具全球性的视角与能力。

更多细节与报名信息：ZeroSpeech 2019: "TTS without T"
