---
title: "推进音频生成的前沿"
title_en: "Pushing the frontiers of audio generation"
source: https://deepmind.google/blog/pushing-the-frontiers-of-audio-generation/
site: deepmind
date: 2024-10-30
crawled: 2026-09-13
translated: 2026-09-13
---

# 推进音频生成的前沿

> 原文：[Pushing the frontiers of audio generation](https://deepmind.google/blog/pushing-the-frontiers-of-audio-generation/) · Google DeepMind

我们开创性的语音生成技术，正在帮助世界各地的人们与更自然、更具对话性、更直观的数字助手和 AI 工具交互。

语音是人类联结的核心。它帮助世界各地的人们交换信息和想法、表达情感并建立相互理解。随着我们为生成自然、动态的语音而打造的技术不断进步，我们正在解锁更丰富、更具吸引力的数字体验。

在过去几年里，我们一直在推进音频生成的前沿，开发能够从文本、节奏控制和特定音色等多种输入生成高质量、自然语音的模型。这项技术为众多 Google 产品和实验中的单说话人音频提供支持——包括 [Gemini Live](https://blog.google/products/gemini/made-by-google-gemini-ai-updates/)、[Project Astra](https://deepmind.google/technologies/gemini/project-astra/)、[Journey Voices](https://cloud.google.com/text-to-speech/docs/voice-types) 和 [YouTube 的自动配音](https://blog.youtube/news-and-events/made-on-youtube-2024/)——并正在帮助世界各地的人们与更自然、更具对话性、更直观的数字助手和 AI 工具交互。

通过与 Google 各部门的合作伙伴共同努力，我们近期协助开发了两个能够生成长篇、多说话人对话的新功能，让复杂内容更容易理解：

- [NotebookLM Audio Overviews](https://notebooklm.google/) 将上传的文档转化为引人入胜的生动对话。只需一键，两位 AI 主持人就会总结用户的材料、在不同主题之间建立联系并你来我往地交谈。
- [Illuminate](https://illuminate.google.com/) 围绕研究论文创建正式的 AI 生成讨论，帮助让知识更易于获取和消化。

在这里，我们对支撑上述所有产品和实验工具的最新语音生成研究做一个概览。

## 开创性的音频生成技术

多年来，我们一直投资音频生成研究，探索在产品和实验工具中生成更自然对话的新方法。在之前关于 [SoundStorm](https://research.google/blog/soundstorm-efficient-parallel-audio-generation/) 的研究中，我们首次展示了生成多说话人之间 30 秒自然对话片段的能力。

这延伸了我们早期的 [SoundStream](https://research.google/blog/soundstream-an-end-to-end-neural-audio-codec/) 和 [AudioLM](https://google-research.github.io/seanet/audiolm/examples/) 工作，它们让我们得以将许多基于文本的语言建模技术应用于音频生成问题。

SoundStream 是一种神经音频编解码器，能够高效地压缩和解压缩音频输入，而不损害其质量。作为训练过程的一部分，SoundStream 学会了如何将音频映射为一系列声学 token。这些 token 捕捉了以高保真度重建音频所需的全部信息，包括[韵律](https://en.wikipedia.org/wiki/Prosody_(linguistics))和[音色](https://en.wikipedia.org/wiki/Timbre)等属性。

AudioLM 将音频生成视为语言建模任务，以生成 SoundStream 等编解码器的声学 token。因此，AudioLM 框架对所生成音频的类型或构成不做任何假设，可以灵活处理各种声音而无需调整架构——这使其成为多说话人对话建模的理想选择。

Your browser does not support the audio element.

两位说话人表达惊讶与难以置信的音频样本。

Your browser does not support the audio element.

两位说话人语音重叠的音频样本。

Your browser does not support the audio element.

两位说话人讲一个有趣故事的音频片段，在笑点处伴有笑声。

Your browser does not support the audio element.

两位说话人对一场惊喜生日派对表达兴奋的音频片段。

Your browser does not support the audio element.

NotebookLM Audio Overview 基于几份与土豆相关的文档生成的多说话人对话示例。

在这一研究基础上，我们最新的语音生成技术在给定对话脚本和说话人轮换标记时，能够生成 2 分钟的对话，并在自然度、说话人一致性和声学质量上均有提升。该模型还能在单块[张量处理单元（TPU）v5e 芯片](https://cloud.google.com/tpu/docs/v5e)上、单次推理中在 3 秒内完成这一任务。这意味着它生成音频的速度超过实时的 40 倍。

## 扩展我们的音频生成模型

把单说话人生成模型扩展到多说话人模型，随后就成了数据和模型容量的问题。为了让最新的语音生成模型产出更长的语音片段，我们创建了一个更高效的语音编解码器，能将音频压缩为 token 序列，码率低至每秒 600 比特，且不损害输出质量。

我们的编解码器生成的 token 具有层次结构，并按时间帧分组。每组中靠前的 token 捕捉语音和韵律信息，而靠后的 token 则编码精细的声学细节。

即便有了新的语音编解码器，生成 2 分钟对话仍需要生成 5,000 多个 token。为了建模这些长序列，我们开发了一种专门的 [Transformer](https://research.google/blog/transformer-a-novel-neural-network-architecture-for-language-understanding/) 架构，能够高效处理信息的层次结构，与我们声学 token 的结构相匹配。

借助这项技术，我们可以在单次自回归推理中高效生成对应对话的声学 token。生成之后，这些 token 可以用我们的语音编解码器解码回音频波形。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

动画展示我们的语音生成模型如何自回归地产出音频 token 流，再将其解码回由两人对话组成的波形。

为了让我们的模型学会如何生成多说话人之间逼真的交流，我们先在数十万小时的语音数据上对其进行预训练。然后，我们在一个小得多的数据集上微调，该数据集由多位配音演员的真实即兴对话组成，具有高声学质量和精确的说话人标注，并包含真实的[不流畅现象](https://en.wikipedia.org/wiki/Speech_disfluency)——真实对话中的"嗯"和"啊"。这一步教会了模型如何在生成的对话中可靠地在说话人之间切换，并只输出录音室级别的音频，带有逼真的停顿、语调和时机。

遵循我们的[AI 原则](https://ai.google/responsibility/principles/)以及负责任地开发和部署 AI 技术的承诺，我们正在引入 SynthID 技术为这些模型生成的非瞬态 AI 音频内容添加水印，以帮助防范这项技术可能被滥用。

## 语音新体验在前方

我们现在专注于改进模型的流畅度和声学质量，并为韵律等特性添加更多细粒度控制，同时探索如何将这些进展与视频等其他模态最好地结合。

先进语音生成的潜在应用是巨大的，尤其是与我们的 Gemini 系列模型结合时。从增强学习体验到让内容更普适可及，我们很期待继续拓展语音技术的可能性边界。

[试试 NotebookLM](https://notebooklm.google.com/)[试试 Illuminate](https://illuminate.google.com/)[试试 Gemini Live](https://support.google.com/gemini/answer/15274899?hl=en)

**致谢**

本工作的作者：Zalán Borsos、Matt Sharifi、Brian McWilliams、Yunpeng Li、Damien Vincent、Félix de Chaumont Quitry、Martin Sundermeyer、Eugene Kharitonov、Alex Tudor、Victor Ungureanu、Karolis Misiunas、Sertan Girgin、Jonas Rothfuss、Jake Walker 和 Marco Tagliasacchi。

我们感谢 Leland Rechis、Ralph Leith、Paul Middleton、Poly Pata、Minh Truong 和 RJ Skerry-Ryan 在对话数据方面的关键付出。

我们非常感谢 Labs、Illuminate、Cloud、Speech 和 YouTube 各团队的出色工作，将这些模型带入产品。

我们还感谢 Françoise Beaufays、Krishna Bharat、Tom Hume、Simon Tokumine、James Zhao 对项目的指导。
