---
title: "AI 音频系统的生成与训练大幅提速"
title_en: "Significantly faster generation and training for AI-based audio systems"
date: 2018-10-22
source: https://ai.meta.com/blog/significantly-faster-generation-and-training-for-ai-based-audio-systems-
crawled: 2026-09-22
translated: 2026-09-22
---

# AI 音频系统的生成与训练大幅提速

> 原文：[Significantly faster generation and training for AI-based audio systems](https://ai.meta.com/blog/significantly-faster-generation-and-training-for-ai-based-audio-systems-) · Meta AI（Wayback 存档）

2018 年 10 月 22 日

**这项研究是什么：** 一个神经音频合成器，可根据特定乐器、音高、力度（音符被弹奏的强弱）及其他输入生成音符。人类评估者评估了符号到乐器神经生成器（Symbol-to-Instrument Neural Generator，SING）创建的音符是否听起来自然——就像在真实的长笛、吉他或其他乐器上演奏的一样。在很多情况下，他们认为该系统比类似的 AI 网络听起来更逼真，尽管该系统所需的训练和音频生成时间只是后者的一小部分。一秒钟的计算中，SING 可以产生 512 秒的音频。

**工作原理：** 典型的基于 AI 的音频生成系统逐个创建音频样本。SING 使用同类训练数据——例如既有音乐音符录音的数据集——但以大得多的批次产出音频，一次最多可生成 1,024 个音频样本的波形。这种端到端训练过程显著减少了所需的计算能力。在使用 NSynth 数据集的测试中，SING 能够从近 1,000 种不同乐器生成音符，每种乐器有数十个音高和五个不同的力度级别。在一项实验中，与一个基于 WaveNet 的最先进编码器相比，该系统为训练中未见过的音高生成音符的能力在近 70% 的情况下被评为比 DeepMind 的 WaveNet 系统更接近真实值（ground truth）——但 SING 的生成时间快 2,500 倍，训练时间快 32 倍。

**为什么重要：** SING 为实时创建更接近真实乐器发声的高质量音频开辟了新机会，尤其是与传统合成器相比。这项研究潜在可用于把一首歌分离为每件乐器或人声各自的音频文件，甚至解读乐谱并以某位音乐家的风格产生音频。该系统更快的生成和训练时间，可以使此前计算密集的应用（如自动音乐生成）更容易被训练资源有限的研究者使用。

**阅读完整论文：** SING: Symbol-to-Instrument Neural Generator

**音频样本：**
1) 真实值（Ground Truth，CC-BY 4.0）：https://code.fb.com/wp-content/uploads/2018/10/flute_acoustic_027-077-050_gt-1.wav
2) SING：https://code.fb.com/wp-content/uploads/2018/10/flute_acoustic_027-077-050_sing-1.wav
3) NSynth Wavenet（CC-BY 4.0）：https://code.fb.com/wp-content/uploads/2018/10/flute_acoustic_027-077-050_nsynth.mp3

全部音频样本请点击此处。
