---
title: "逼真到发丝的动画为这位 Googler 赢得奥斯卡金像奖"
title_en: "Hair-raising animation won this Googler an Academy Award"
source: https://blog.google/innovation-and-ai/technology/research/hair-raising-animation-won-googler-academy-award/
site: google-blog
date: 2021-02-18
crawled: 2026-09-13
translated: 2026-09-13
---

# 逼真到发丝的动画为这位 Googler 赢得奥斯卡金像奖

> 原文：[Hair-raising animation won this Googler an Academy Award](https://blog.google/innovation-and-ai/technology/research/hair-raising-animation-won-googler-academy-award/) · Google

2 月 13 日，Google Research 的 John Anderson 获得了奥斯卡科技成就奖（Academy Award for Technical Achievement）——该奖项每年颁发给[“推动电影工业进步”](https://www.oscars.org/sci-tech/technical#:~:text=Technical%20Achievement%20Awards%20are%20given,at%20an%20annual%20award%20ceremony.)的技术成就。John 获奖是表彰他在 Pixar 工作期间对 [Taz 毛发模拟系统](https://graphics.pixar.com/library/CurlyHairB/paper.pdf)的贡献。他的工作最著名的呈现是 Pixar 电影《勇敢传说》（Brave），为主角 Merida 富有弹性的卷发提供了动力。这是 John 在电影行业工作 14 年间的第二座奥斯卡奖。他的第一座奖于 2002 年获得，表彰他在 George Lucas 旗下工业光魔（Industrial Light and Magic）[生物动力学系统](https://www.ilm.com/awards/ilm-creature-dynamics-system-awards/)上的工作——该系统同样实现了毛发、皮肤和衣物的逼真运动动画，应用于《星球大战前传 1：幽灵的威胁》《木乃伊》和《巨猩乔扬》等电影。

Mark Meyer（左）——Pixar 研究组负责人，与 John Anderson（右）——Google Research 首席科学家，在二人共事于 Pixar 期间的合影。

![Mark Meyer（左）——Pixar 研究组负责人，与 John Anderson（右）——Google Research 首席科学家，在二人共事于 Pixar 期间的合影](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/AndersonJohn_00967_janders_fun.t.width-1200.format-webp.webp)

模拟是一个困难的计算问题，因为它试图用有限的算力重现一个连续的物理世界。为了让现实世界能被计算机处理，模拟的设计者必须把世界"离散化"，即切分成粗糙的小块，并计算这些小块之间的物理交互。在这些小块内部，模拟设计者必须"参数化"，即对世界的行为做出假设，因为再往下计算物理细节的成本会过于高昂。模拟的艺术，就在于调整这些假设，在重现物理世界的精度、规模与成本之间求得平衡。

Taz 毛发模拟系统输出的示例。

![Taz 毛发模拟系统输出的示例](https://storage.googleapis.com/gweb-uniblog-publish-prod/images/PixarTaz-Merida.width-1200.format-webp.webp)

对于像《勇敢传说》中 Merida 那样的卷发，任意时刻发丝之间都在发生无数次碰撞。更复杂的是每根发丝各自的物理特性——它们实际上就像一根根小弹簧。《勇敢传说》使用的毛发模拟技术采用了巧妙的数学方案，将计算成本保持在低位，让动画师得以快速高效地工作，同时保持高度的物理精确性，确保 Merida 紧致的卷发依然像真发一样弹跳、飘动。

在进入电影行业之前，John 曾在威斯康星大学麦迪逊分校担任了近 14 年的大气与海洋科学教授。正是这段物理学与计算流体动力学的经历，构成了他电影生涯中诸多贡献的基础。如今在 Google，John 专注于发挥他独特的背景，帮助世界应对当今最紧迫的议题之一：气候变化。John 领导着 Google Research 内部的一个团队，探索如何改进模拟，以便更好地为气候以及洪水、野火等因气候变化而加剧的现象建模。

正如毛发动画那样，大型气候模型依赖于小尺度过程之间的个体交互，例如单朵云的湍流或混沌运动。不过，John 的研究小组没有沿用 Merida 头发所用的那种巧妙数学方案，而是专注于用机器学习来预测物理动力学，让建模者既能改进那些"小块内部"假设的精度，也可以用机器学习得到的等价物完全取代原有模型。

John 的团队利用 Google 的 TPU 来生成[洪水](https://blog.google/technology/ai/flood-forecasts-india-bangladesh/)、野火和云的高分辨率重现。这些模拟的输出被用于训练机器学习模型，随后这些模型又可在后续模拟中发挥作用，以降低成本、提高精度。他的团队相信，通过将机器学习应用于模拟，我们将能够创建更高效的模型，加速我们预测和应对气候变化影响的能力。

从让动画和电影中最细微的细节栩栩如生，到改进全球气候与天气模型，John 的工作极大地推进了我们对物理世界动力学的理解。祝贺你，John！
