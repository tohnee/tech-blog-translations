---
title: "新的生成式 AI 工具为音乐创作敞开大门"
title_en: "New generative AI tools open the doors of music creation"
source: https://deepmind.google/blog/new-generative-ai-tools-open-the-doors-of-music-creation/
site: deepmind
date: 2024-10-23
crawled: 2026-09-13
translated: 2026-09-13
---

# 新的生成式 AI 工具为音乐创作敞开大门

> 原文：[New generative AI tools open the doors of music creation](https://deepmind.google/blog/new-generative-ai-tools-open-the-doors-of-music-creation/) · Google DeepMind

**注（2025 年 5 月 1 日）：**这些工具现在由 Google DeepMind 开发的音乐生成模型 [Lyria](https://deepmind.google/models/lyria/) 和 [Lyria RealTime](https://deepmind.google/models/lyria/lyria-realtime/) 驱动。

我们最新的 AI 音乐技术现已在 MusicFX DJ、Music AI Sandbox 和 YouTube Shorts 中推出

近十年来，我们的团队一直在探索[人工智能（AI）如何支持创作过程](https://magenta.withgoogle.com/blog/2016/06/01/welcome-to-magenta/)，打造让爱好者和专业人士能够发现创意表达新形式的工具。

过去一年，我们通过[Music AI Incubator](https://blog.youtube/inside-youtube/partnering-with-the-music-industry-on-ai/) 等渠道与音乐行业的合作伙伴密切合作。他们的意见一直在指导我们最先进的生成式音乐实验，并帮助我们确保新的生成式 AI 工具负责任地为每个人敞开音乐创作的大门。

今天，与 [Google Labs](https://blog.google/technology/ai/jacob-collier-labs-sessions) 合作，我们发布了重新构想的 [MusicFX DJ](http://labs.google/musicfx) 体验，让任何人都能更轻松地实时交互式生成音乐。

我们还宣布了音乐 AI 工具包 [Music AI Sandbox](https://blog.google/technology/ai/google-generative-ai-veo-imagen-3/) 的更新，并在 [YouTube 的 Dream Track](https://deepmind.google/discover/blog/transforming-the-future-of-music-creation/) 中展示我们最新的 AI 音乐技术——这是一套实验套件，创作者可以用它为自己的 Shorts 和视频生成高质量器乐曲。

## 用 MusicFX DJ 生成现场音乐

在今年的 I/O 大会上，我们分享了 [MusicFX DJ 的早期预览](https://blog.google/technology/ai/google-labs-video-fx-generative-ai/)，这是一个任何人都可以像乐器一样演奏的数字工具，让现场音乐创作的乐趣惠及各种水平的人。

今天，我们对 MusicFX DJ 进行了一系列更新，包括扩展的直观控制集、重新设计的界面、改进的音质和新的模型行为。这些能力让玩家能够生成并引导连续的音乐流，与朋友分享自己的创作，并一起即兴合奏。

与六次荣获 GRAMMY 奖的歌手、词曲作者、制作人和多乐器演奏家 [Jacob Collier](https://www.youtube.com/watch?v=y7gKlzvg8xk&feature=youtu.be) 密切合作，我们设计了这些更新，让 MusicFX DJ 更易上手、更有用、更富启发性。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

与混合现成曲目的传统 DJ 工具不同，MusicFX DJ 通过允许玩家将音乐概念作为文本提示词进行混合来生成全新的音乐。借助 MusicFX DJ，玩家可以组合自己喜爱的流派、乐器和氛围来创造新风格，即兴表演一场现场 DJ set，或在制作中搜索新的旋律、音色和节奏。

虽然不是传统意义上的乐器，MusicFX DJ 却是进入现场音乐创作的易用且富有表现力的入口。无论音乐经验深浅，MusicFX DJ 都赋予玩家直观的控制，让他们生成并引导独特且持续演化的音乐声景。

> 你雕琢着这种实时的声音黏土，它令人惊喜不断，本质上是在试图将那些原本不太可能联系起来的事物点石成金般地联结起来。

Jacob Collier

两项新颖的方法支撑着 MusicFX DJ。第一，我们改造了一个离线生成式音乐模型来执行实时流式生成。我们通过训练它基于先前生成的音乐和玩家提供的文本提示词来生成下一段音乐片段。

第二，不像典型的文本到音乐模型那样只有一个固定的文本提示词，我们让玩家能够混合多个文本提示词，并随时间改变混合比例。模型通过混合每个提示词的表示（称为嵌入 embeddings）来实现这一点，每个嵌入的相对重要性由玩家用滑块选择。模型使用这些组合后的嵌入来引导音乐风格。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

流程图展示 MusicFX DJ 如何生成连续的音乐流，从之前的片段创建下一段，同时由文本提示词和用于加权其重要性的滑块引导。

### 打造更直观的控制

我们与 Jacob 一起探索并打造了那些对新手而言直观的专用控制，鼓励实验，并提供比单纯文本提示词更多样的创意表达途径。

借助 MusicFX DJ 的新控制，玩家可以指挥配器，通过移除和添加贝斯、鼓和其他乐器，轻松制造段落骤停（breakdown）和低音重击（bass drop）。他们可以调整音乐的质感，比如让它听起来更明亮或更暗沉、更重复或更随机、更平滑或更粗粝。

玩家还可以控制调性和节奏，这使得跟随现有音乐演奏以及长时间即兴合奏变得更容易。我们的团队非常享受将 MusicFX DJ 与传统乐器一起使用，我们迫不及待想听到其他人用这些新能力创作出什么。

第 1 页，共 4 页

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

### 生成制作级音质

作为合作的一部分，我们还探索了玩家如何既能把模型输出作为灵感来源，又能将其用于大型作品的一部分。但我们早期的模型缺乏创作专业音频所需的质量。得益于我们音频研究团队的最新创新，包括新的神经音频编解码器和优化的网络架构，MusicFX DJ 现在能够实时流式传输制作级 48 kHz 立体声音频。

### 分享与下载音频

受 Jacob 对创意合作的重视启发——无论是[与其他艺术家](https://www.npr.org/2024/04/01/1198910485/jacob-collier-album-djesse-volume-four)还是[与他的观众](https://www.youtube.com/watch?v=3KsF309XpJo)——我们希望让分享和互动 MusicFX DJ 创作的音乐变得更容易。玩家现在可以下载 60 秒的 MusicFX DJ 音频并与朋友分享会话，朋友们可以观看演奏回放，甚至可以随时接手控制——把音乐带向一个全新的方向。

## 扩展的 Music AI Sandbox 工具包

[Music AI Sandbox](https://blog.google/technology/ai/google-generative-ai-veo-imagen-3/) 是一套实验性的音乐 AI 工具，旨在为通过 YouTube 的 [Music AI Incubator](https://blog.youtube/inside-youtube/partnering-with-the-music-industry-on-ai/) 与我们合作的音乐家、制作人和词曲作者的工作流赋能。它是从音乐行业中多元的艺术家、词曲作者和合作伙伴那里收集对我们最新、最具实验性的生成式音乐工具反馈的宝贵试验场。虽然 Music AI Sandbox 目前尚未公开发布，这项工作的成功元素将被整合进广泛可用的 Google 产品中。

自今年 I/O 大会上公开展示 Music AI Sandbox 以来，我们还与 [Google 技术与社会团队](https://blog.google/technology/ai/artist-refik-anadol-ai-creativity-google/)密切合作，以改进用户体验并大规模联系艺术界收集反馈。这项工作帮助我们对此工具套件背后的模型做出了重大更新。

很快，受信任的测试者将能够勾勒一首歌曲，并使用多轨视图通过精确控制来组织和打磨作品。这个新版本的 Music AI Sandbox 集成了我们的最新技术，包括驱动 MusicFX DJ 的模型，以及循环生成、声音变换和修补（in-painting）等热门功能，帮助用户无缝连接其音乐曲目的各个部分。

![我们更新的 Music AI Sandbox 用户界面设计截图，具有多轨视图，可通过精确控制帮助组织和打磨作品。](https://lh3.googleusercontent.com/otfaldHsOzIe3YZYbnTgqhSfJFWRFpe0yQqvaou4XM2_4vmpzbcjHppFKF9mV2n5V6qcjvqycTK2FMxe7UCzpOtfPon7YDtIi5aLWLzdg5mVn7LFLg=w1440)

我们更新的 Music AI Sandbox 用户界面设计截图，具有多轨视图，可通过精确控制帮助组织和打磨作品。

## YouTube 的 Dream Track 实验现在可生成器乐配乐

在我们与 YouTube 持续合作的基础上，我们演进 了[Dream Track 实验](https://blog.youtube/inside-youtube/ai-and-music-experiment/)，让美国创作者可以探索一系列流派和提示词，用强大的文本到音乐模型生成器乐配乐。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![ Your browser does not support the video tag.](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

我们最新的音乐生成模型采用新颖的强化学习方法训练，拥有更高的音质，同时能更好地关注用户文本提示词的细微差别。负责任地部署生成式技术是我们[价值观](https://ai.google/responsibility/principles/)的核心，因此 MusicFX DJ 和 Dream Track 生成的所有音乐都使用 [SynthID](https://deepmind.google/technologies/synthid/) 添加水印。

## 共同构建音乐创作的未来

过去一年，我们很高兴与音乐界的合作伙伴携手，帮助打造既回应专业人士需求、又为下一代音乐人扩展创作机会的技术。

我们期待深化这些伙伴关系，共同构建音乐创作的未来，开发更好的工具来激发创造力。

[试试 MusicFX DJ](http://labs.google/musicfx)[观看我们与 Jacob Collier 的 Lab Sessions 视频](https://www.youtube.com/watch?v=y7gKlzvg8xk&feature=youtu.be)[进一步了解 Music AI Sandbox](https://deepmind.google/blog/transforming-the-future-of-music-creation/)

这项工作有赖于以下核心研究与工程努力：Andrea Agostinelli、Zalán Borsos、George Brower、Antoine Caillon、Cătălina Cangea、Noah Constant、Michael Chang、Chris Deaner、Timo Denk、Chris Donahue、Michael Dooley、Jesse Engel、Christian Frank、Beat Gfeller、Tobenna Peter Igwe、Drew Jaegle、Matej Kastelic、Kazuya Kawakami、Pen Li、Ethan Manilow、Yotam Mann、Colin McArdell、Brian McWilliams、Adam Roberts、Matt Sharifi、Ian Simon、Ondrej Skopek、Marco Tagliasacchi、Cassie Tarakajian、Alex Tudor、Victor Ungureanu、Mauro Verzetti、Damien Vincent、Luyu Wang、Björn Winkler、Yan Wu 和 Mauricio Zuluaga。

MusicFX DJ 由 Antoine Caillon、Noah Constant、Jesse Engel、Alberto Lalama、Hema Manickavasagam、Adam Roberts、Ian Simon 和 Cassie Tarakajian 开发，并与 Google Labs 的合作伙伴 Obed Appiah-Agyeman、Tahj Atkinson、Carlie de Boer、Phillip Campion、Sai Kiran Gorthi、Kelly Lau-Kee、Elias Roman、Noah Semus、Trond Wuellner、Kristin Yim 和 Jamie Zyskowski 协作完成。我们向 Jacob Collier、Ben Bloomberg 和 Fran Haincourt 致以最深切的感谢，感谢他们在整个开发过程中提供的宝贵反馈。

Music AI Sandbox 由 Andrea Agostinelli、George Brower、Ross Cairns、Michael Chang、Yeawon Choi、Chris Deaner、Jesse Engel、Reed Enger、Beat Gfeller、Tom Hume、Tom Jenkins、Max Edelmann、Drew Jaegle、Jacob Kelly、DY Kim、David Madras、Hema Manickavasagam、Ethan Manilow、Yotam Mann、Colin McArdell、Chris Reardon、Felix Riedel、Adam Roberts、Arathi Sethumadhavan、Eleni Shaw、Sage Stevens、Amy Stuart、Luyu Wang、Pawel Wluka 和 Yan Wu 开发，并与 YouTube 以及 Tech & Society 的合作伙伴协作完成。

Dream Track 由 Andrea Agostinelli、Zalán Borsos、Geoffrey Cideron、Timo Denk、Michael Dooley、Christian Frank、Sertan Girgin、Myriam Hamed Torres、Matej Kastelic、Pen Li、Brian McWilliams、Matt Sharifi、Ondrej Skopek、Marco Tagliasacchi、Mauro Verzetti、Mauricio Zuluaga 开发，并与 YouTube 的合作伙伴协作完成。

特别感谢 Aäron van den Oord、Tom Hume、Douglas Eck、Eli Collins、Mira Lane、Koray Kavukcuoglu 和 Demis Hassabis（德米斯·哈萨比斯）在整个研究过程中富有洞见的指导与支持。感谢 Mahyar Bordbar 和 DY Kim 协调这些工作，也感谢 YouTube 艺人合作团队对音乐行业合作的支持。

我们也感谢在 Google DeepMind 和 Alphabet 内部做出贡献的众多其他同事，包括我们在 YouTube 的合作伙伴。
