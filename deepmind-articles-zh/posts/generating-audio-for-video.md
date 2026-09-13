---
title: "为视频生成音频"
title_en: "Generating audio for video"
source: https://deepmind.google/blog/generating-audio-for-video/
site: deepmind
date: 2024-06-17
crawled: 2026-09-13
translated: 2026-09-13
---

# 为视频生成音频

> 原文：[Generating audio for video](https://deepmind.google/blog/generating-audio-for-video/) · Google DeepMind

视频转音频（V2A）研究利用视频像素和文本提示词生成丰富的配乐

视频生成模型正以惊人的速度进步，但目前的许多系统只能生成无声输出。让生成的电影变得鲜活起来的下一个重大步骤之一，就是为这些无声视频创建配乐。

今天，我们分享视频转音频（V2A）技术的进展，它让同步的视听生成成为可能。V2A 将视频像素与自然语言文本提示词相结合，为屏幕上的动作生成丰富的声景。

我们的 V2A 技术可以与 [Veo](https://deepmind.google/technologies/veo/) 等视频生成模型搭配使用，创建带有戏剧性配乐、逼真音效或与视频角色和基调相匹配的对白的镜头。

它还可以为一系列传统素材生成配乐，包括档案资料、无声电影等——开启更广泛的创作机会。

音频提示词：Cinematic, thriller, horror film, music, tension, ambience, footsteps on concrete

音频提示词：Cute baby dinosaur chirps, jungle ambience, egg cracking

音频提示词：Jellyfish pulsating under water, marine life, ocean

音频提示词：A drummer on a stage at a concert surrounded by flashing lights and a cheering crowd

音频提示词：Cars skidding, car engine throttling, angelic electronic music

音频提示词：A slow mellow harmonica plays as the sun goes down on the prairie

音频提示词：Wolf howling at the moon

## 增强的创意控制

重要的是，V2A 能够为任意视频输入生成无限数量的配乐。用户还可以选择性地定义"正向提示词"来引导生成输出趋向想要的声音，或定义"负向提示词"来引导它远离不想要的声音。

这种灵活性让用户对 V2A 的音频输出拥有更多控制，能够快速试验不同的音频输出并挑选最匹配的一种。

音频提示词：A spaceship hurtles through the vastness of space, stars streaking past it, high speed, Sci-fi

音频提示词：Ethereal cello atmosphere

音频提示词：A spaceship hurtles through the vastness of space, stars streaking past it, high speed, Sci-fi

## 工作原理

我们试验了自回归和扩散两种方法来寻找最具可扩展性的 AI 架构，其中基于扩散的音频生成方法在同步视频与音频信息方面给出了最逼真、最令人信服的结果。

我们的 V2A 系统首先将视频输入编码为压缩表示。然后，扩散模型从随机噪声开始迭代地细化音频。这一过程由视觉输入和自然语言提示词引导，生成与提示词高度契合的同步、逼真音频。最后，音频输出被解码、转换为音频波形，并与视频数据结合。

![V2A 技术工作流程图：输入视频像素和文本提示词（正向与负向）经过编码器、扩散模型和解码器处理，生成音频波形。](https://lh3.googleusercontent.com/4UXuyvSiMGMU26kS2cFxP-1bl40KD8QOsGF_XquqUPAJ-5xq8wCrT00ioneRu0EhOuRsE0iJ3tjLCDpBLtKOeGe4bt9rv6DS2QZ2q97zcRaBuKeFzc0=w1440)

我们的 V2A 系统示意图：接收视频像素和音频提示词输入，生成与底层视频同步的音频波形。首先，V2A 对视频和音频提示词输入进行编码，并让其在扩散模型中迭代运行。然后它生成压缩音频，再解码为音频波形。

为了生成更高质量的音频，并增加引导模型生成特定声音的能力，我们在训练过程中加入了更多信息，包括带有详细声音描述的 AI 生成标注以及口头对白的转录文本。

通过在视频、音频和这些额外标注上训练，我们的技术学会将特定音频事件与各种视觉场景关联起来，同时响应标注或转录文本中提供的信息。

## 更多研究正在进行中

我们的研究有别于现有的视频转音频方案，因为它可以理解原始像素，而且文本提示词是可选的。

此外，该系统不需要手动对齐生成的声音与视频——那需要繁琐地调整声音、视觉和时机的各种元素。

不过，还有许多其他局限我们正在设法解决，相关研究正在进行中。

由于音频输出的质量取决于视频输入的质量，视频中处于模型训练分布之外的伪影或失真可能导致音质明显下降。

我们还在改进涉及语音的视频的唇形同步。V2A 尝试根据输入转录文本生成语音，并将其与角色的唇部动作同步。但配对的视频生成模型可能并未以转录文本为条件。这会造成不匹配，常常导致诡异的唇形同步，因为视频模型生成的嘴部动作与转录文本不一致。

![](https://lh3.googleusercontent.com/_i0NHcAzCbB1pjGV06l3eqe3B0nOYEdQGWNLWivwqVaNFtcemyRdwZNFiRg8bkliL50WNwpxSTV5lL_bJGt80dvaByTTOZXHuuB8KESlqZJTgHBf6A=w1440-h810-n-nu)

音频提示词：Music，转录文本："this turkey looks amazing, I'm so hungry"

## 我们对安全与透明的承诺

我们致力于负责任地开发和部署 AI 技术。为了确保我们的 V2A 技术能对创意社区产生积极影响，我们正在向领先的创作者和电影制作人收集多元的观点与洞见，并利用这些宝贵的反馈来指导我们持续的研究与开发。

我们还将 [SynthID](https://deepmind.google/technologies/synthid/) 工具包纳入了 V2A 研究，为所有 AI 生成内容添加水印，以帮助防范这项技术被滥用的可能。

在我们考虑向更广泛的公众开放之前，我们的 V2A 技术将经过严格的安全评估与测试。初步结果表明，这项技术将成为让生成的电影鲜活起来的有前途的方法。

注：所有示例均由我们的 V2A 技术生成，该技术与我们最强大的生成式视频模型 [Veo](https://deepmind.google/technologies/veo/) 搭配使用。

[了解 Veo](https://deepmind.google/models/veo/)[探索我们的 SynthID 工具包](https://deepmind.google/models/synthid/)

**致谢**

这项工作有赖于以下人员的贡献：Ankush Gupta、Nick Pezzotti、Pavel Khrushkov、Tobenna Peter Igwe、Kazuya Kawakami、Mateusz Malinowski、Jacob Kelly、Yan Wu、Xinyu Wang、Abhishek Sharma、Ali Razavi、Eric Lau、Serena Zhang、Brendan Shillingford、Yelin Kim、Eleni Shaw、Signe Nørly、Andeep Toor、Irina Blok、Gregory Shaw、Pen Li、Scott Wisdom、Aren Jansen、Zalán Borsos、Brian McWilliams、Salah Zaiem、Marco Tagliasacchi、Ron Weiss、Manoj Plakal、Hakan Erdogan、John Hershey、Jeff Donahue、Vivek Kumar 和 Matt Sharifi。

我们向 Benigno Uria、Björn Winckler、Charlie Nash、Conor Durkan、Cătălina Cangea、David Ding、Dawid Górny、Drew Jaegle、Ethan Manilow、Evgeny Gladchenko、Felix Riedel、Florian Stimberg、Henna Nandwani、Jakob Bauer、Junlin Zhang、Luis C. Cobo、Mahyar Bordbar、Miaosen Wang、Mikołaj Bińkowski、Sander Dieleman、Will Grathwohl、Yaroslav Ganin、Yusuf Aytar 和 Yury Sulsky 致谢。

特别感谢 Aäron van den Oord、Andrew Zisserman、Tom Hume、RJ Mical、Douglas Eck、Nando de Freitas、Oriol Vinyals、Eli Collins、Koray Kavukcuoglu 和 Demis Hassabis（德米斯·哈萨比斯）在整个研究过程中富有洞见的指导与支持。

我们也感谢在 Google DeepMind 以及 Google 合作伙伴中做出贡献的众多其他同事。
