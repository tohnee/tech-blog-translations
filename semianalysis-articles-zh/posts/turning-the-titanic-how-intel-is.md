---
title: "掉转泰坦尼克号——英特尔如何用软件收购与强化问责来拯救这艘正在下沉的巨轮"
title_en: "Turning The Titanic – How Intel Is Using Software Acquisitions And Increased Accountability To Attempt To Save The Sinking Ship"
date: 2022-05-18
source: https://newsletter.semianalysis.com/p/turning-the-titanic-how-intel-is
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 掉转泰坦尼克号——英特尔如何用软件收购与强化问责来拯救这艘正在下沉的巨轮

> 原文：[Turning The Titanic – How Intel Is Using Software Acquisitions And Increased Accountability To Attempt To Save The Sinking Ship](https://newsletter.semianalysis.com/p/turning-the-titanic-how-intel-is) · SemiAnalysis

英特尔（Intel）未来几年日子不好过早已不是秘密：AMD、Nvidia、Marvell 在蚕食它的份额，苹果、亚马逊、谷歌、微软和 Meta 的自研芯片努力也在分食。由于设计整合放缓与工艺技术延迟的双重打击，英特尔毛利率已从 60% 的长期目标跌至 50%，同时份额不断失血。

英特尔处境艰难，但它们正在[倾尽所有](https://semianalysis.substack.com/p/intel-is-throwing-the-kitchen-sink?s=w)，试图扭转滑向边缘化的颓势：多招聘了 10,000 多名工程师、增加晶圆厂开支、加码研发，并收购了 Tower Semiconductor 等公司。我们已经对[所有这些努力以及每个业务单元和文化转变做过深度解析](https://semianalysis.substack.com/p/intel-is-throwing-the-kitchen-sink?s=w)。

> 我们对这一切能否落地深表怀疑。其困难程度怎么强调都不为过，但这也是唯一的前路。英特尔本可以走 IBM、通用电气等许多美国巨头的老路：缓缓滑向无足轻重，不断剥离业务，让曾经的美国创新骄傲蒙羞。一言以蔽之：失败。Pat Gelsinger 和英特尔对这条路说不。
>
> SemiAnalysis（2021）

在这篇文章中，我们想聚焦更宏大的层面：英特尔如何通过公司重组、在整个组织内推动问责来校正航向。我们也想讨论英特尔过去一年收购的软件公司。先从软件说起。

上周的 Intel Vision 2022 活动上，我们有机会向 Pat Gelsinger 请教软件战略。讨论围绕这些先前的收购、英特尔是否会与自己的客户竞争、英特尔如何决定开源、闭源或对其软件收费，以及英特尔未来在自研 vs 合作伙伴 vs 收购之间的取舍。

> 我们会做更多 SAAS，做更多 SAAS 收购。硅片加 SAAS 等于完整的解决方案。
>
> Pat Gelsinger，英特尔 CEO

在回答中，Pat 感叹英特尔开发出了如此多构成云计算基石的技术，却从未被好好变现——倒是英特尔的客户把这些软件和中间件变成了钱。看起来他们的判断是：英特尔可以把自己开发的东西以服务的形式变现，这有助于正确地对齐激励。Pat 表示，英特尔会继续做开源软件、继续做支撑自家芯片的闭源软件，但同时也会向软件即服务的方向推进。

> 我们签下了一笔 1 亿美元以上的软件收入大单，而我们其实还没真正开始卖……但今年，我要把它提高到大约 1.5 亿美元，而且我们认为假以时日还能做得更多。
>
> Greg Lavender，英特尔 CTO

相对年营收超过 700 亿美元的芯片业务，这 1.5 亿美元只是个零头，但 50% 的同比增长不容小觑。这是有机增长，加上英特尔为提升软件收入而进行的收购。有机开发的大部分精力似乎放在打造安全中间件上，以确保应用与数据安全，例如英特尔的「Project Amber」。英特尔已经开始悄悄收购软件公司。仅过去一年，他们就收购了 Ananki、Granulate、Linutronix、Screenovate Technologies 和 RemoteMyApp。单看没有一笔是颠覆性的，但它们在合理的价位补进了 SAAS 业务。这些收购也不会与云服务商或大多数企业客户直接竞争。我们[此前已深度解析过收购 Tower Semiconductor 一案](https://semianalysis.substack.com/p/intel-is-throwing-the-kitchen-sink?s=w)，本文只对英特尔的软件收购做简要点评。

**Granulate** 是这批软件收购中最大的一笔：一家约 120 名员工的初创公司卖了约 6.5 亿美元。他们的软件非常有意思，卖点是不需要客户修改代码，就能在运行时自主、持续地优化软件。任何认识软件开发者的人都知道，99% 的代码优化得一塌糊涂。随着摩尔定律逼近极限，要继续降低计算成本，就需要硬件架构与软件协同设计的创新。与传统超大规模云厂商（如亚马逊或 Meta）相比，普通企业更不具备这种能力，因此英特尔需要让这些企业继续觉得本地部署（On-Premises）有吸引力。各种优化或许已经内置进最新版的 Linux、框架和运行时库，但应用所运行的旧版本因为兼容性或工程资源不足而享受不到。Granulate 对这类遗留软件问题帮助巨大，因为它同样能在那里做优化。更多信息可查看这些[演示](https://www.youtube.com/channel/UCLy8LLcP0oqzbqPMooMb9vQ/videos)。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

**Linutronix** 看来是一笔漂亮的收购。他们开发运行于 Linux 之上的实时方案 PREEMPT_RT，以及用于工业应用的其他服务。他们的技术能够管理中断和锁，将 CPU 延迟降到最低等功能。英特尔表示他们会作为独立的软件业务运营，这是项不错的服务，但 Linutronix 同时也让英特尔的网络与边缘事业部（NEX）获得了竞争优势。鉴于价格未披露，这笔收购应该相当便宜。总体而言，这似乎既赋能了客户，又找到了把软件工作变现的路子，还不会与客户竞争。

**Ananki** 加上**开放网络基金会（ONF）**内部开发团队的大多数成员，是目前我们最喜欢的一笔。Ananki 是从开放网络基金会剥离出来的公司，把 ONF 的技术栈产品化并在此基础上构建。ONF 与英特尔都致力于打破网络世界的专有壁垒。这种[开放的软件打法](https://semianalysis.substack.com/p/how-nvidias-empire-could-be-eroded)正是在网络领域击败博通（Broadcom）、并在 AI 与加速计算领域整体对抗英伟达的剧本。与这笔收购同步，英特尔开源了一大波优秀的软件方案：公有 5G（SD-Core、SD-RAN）、私有 5G 网络（Aether）、软件定义宽带（SEBA/VOLTHA）以及 P4 可编程网络（SD-Fabric、PINS）。网络软件与架构领域正在发生的这场革命，我们日后大概率会再深入探讨。

**RemoteMyApp** 是最让我们看不懂的一笔收购。英特尔收购了一家游戏流媒体公司，以增强云游戏串流和就近计算机本地/区域资源共享两方面的能力。他们为此专门启动了「Project Endgame」。英特尔明确表示不打算像英伟达的 GeForce Now 那样运营游戏串流平台，而是想把技术授权给别人。有意思的是，这项技术可以实现去中心化系统：空闲的计算机可以替别人跑游戏，不一定非要经由云服务器环境。我们之所以不喜欢这笔收购，是因为云游戏的世界早已挤满了全球最大的那些科技公司。

**Screenovate** 是一笔 1 亿到 1.5 亿美元的收购。它连续多年盈利，在小型软件收购中相当罕见。Screenovate 是无线设备虚拟化与跨平台屏幕共享领域的技术领先者和 IP 持有者。坦白说，在我们看来这是笔无聊的收购，因为其协同似乎主要限于客户端计算。好的一面是，它也基本不与客户竞争。

# **问责**

英特尔有 20,000 名软件工程师，比任何一家纯半导体公司都多。这是巨额的软件投入，激励必须对齐。团队需要有自己的预算和可证明的目标。在合理的地方注入 SAAS 商业模式，这些软件团队就能拥有自己的损益表，可以有可量化的绩效目标，而不是淹没在庞大组织的海洋里。另一方面，硅片与产品团队在合理的情况下也可以继续自设软件团队，让软件直接服务于卖更多芯片。

英特尔进行了公司层面的重组，让团队有更直接的目标。英特尔重新搬出了安迪·格鲁夫（Andy Grove）著名的 OKR 方法，把财务激励和晋升与「目标与关键成果」的达成情况挂钩。产品负责人和经理（在合理范围内）从产品孕育到整个生命周期一路跟进，这让他们对产品的成败更负责任。

最重要的变化是各事业部的划分更加清晰。数据中心与人工智能事业部（DCAI）如今与加速计算系统与图形事业部（AXG）、网络与边缘事业部（NEX）分得更开。销售组织在很大程度统一负责销售与定价，但仍与各事业部深度协作。当我们深入剖析加速计算事业部或英特尔代工业务等单元时，这些变化会更加明显。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5a89496b-9ad4-4c7e-988b-e54dc0e445e4_1024x593.png)

AXG 有必须深耕的明确纵向领域：一切与 GPU 相关的东西，外加高性能计算。他们的任务是把这门技术做起来并产品化。很好，它有自己的损益表，妙极了。第一个麻烦在于：英特尔目前出货的图形技术大部分其实是随消费级 CPU 走的。这怎么算？

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7af443fd-e1ca-46e2-8b5d-fbf2092476f9_1024x189.png)

细看注释就会发现：英特尔让客户端计算事业部在 2021 年做 7 亿美元的公司内部收入划转，到 2026 年放大到 10 亿美元，以补偿加速计算与图形团队的工作。这反过来给了该团队一个交付客户端图形 IP 的收入基础。团队有了明确的起步预算。Raja Koduri 和他的团队有清晰定义的目标，必须在此基础上增长。正如英特尔一季度财报所示，该部门非 GAAP 口径下在 2.19 亿美元收入的基础上录得 3.9 亿美元巨额经营亏损。其中大部分来自致力于让 HPC、AI 和游戏 GPU 落地的庞大团队。这些短期亏损是被理解且被接受的。

从长期看，这些领域的投入可以被清楚地追踪，其成败可以明确归因到 Raja Koduri 和他的团队头上，公司内部和外部投资者都可以做到这一点。当团队犯错或摔跟头时，问责才会真正开足马力。AXG 接二连三的跳票就是明证。

Ponte Vecchio 高性能计算 GPU 和 Alchemist 游戏 GPU 最初都定在 2021 年，结果双双跳票。Ponte Vecchio 现在看来要 2023 年才能发布，相对最初计划延迟了 2 年。很难看。此外，Alchemist GPU 也才刚刚起步。许多玩家甚至会争辩说它压根还没发布。代号 DG2 的 Alchemist GPU 至今没有进入 PC DIY 市场，看样子要拖到三季度，比最初计划的发布时间晚了将近一年。

为什么延迟？英特尔最初把 Ponte Vecchio 的第一次跳票归咎于工艺技术，但把 Alchemist 的问题归咎于软件，这就相当奇怪了。我们的朋友 [Chips and Cheese](https://chipsandcheese.com/) 对英特尔驱动做了一番侦查，结果显示 DG2_G10 和 G11（Alchemist）分别有从 A0 一路到 C1 和 C0 的多个步进（stepping）。这可能暗示除软件问题之外，还存在没有被摆到台面上讨论的硅工程问题。

我们不是要声讨 AXG。他们的任务极其艰巨：被要求从近乎零开始建立一整个 GPU 业务。这是漫长的旅程，可以说是一场奥德赛，所以在下判断之前，不妨再给他们几年时间。关键在于产品相对较少，每个团队和负责人在英特尔内部、在外部股东眼里都能被更密切地追踪。

英特尔代工服务（Intel Foundry Services）业务同样在公司重组中被拆分出来。它既包含现有的代工业务（如 Achronix 和思科），也包含与[亚马逊](https://semianalysis.substack.com/p/amazon-graviton-3-uses-chiplets-and)的先进封装业务。英特尔甚至可以沿用同一套剧本：把所有晶圆厂划归代工服务业务，各事业部必须向代工组织做公司内部收入划转来获取芯片供应与封装。这样一来，将来出售部分晶圆厂、甚至让它整体上市，就是最顺理成章的剧本。

在我们与英特尔人士的多场交流中，问责是贯穿始终的主题。虽然从来没有人明说，但种种迹象——更强的责任、更有意义的可量化目标——正在被层层压到组织深处。这种改变是必需的，英特尔才不会是一头泰坦尼克般迟缓的巨兽，而是一台更轻快敏捷的机器。

[分享](https://newsletter.semianalysis.com/p/turning-the-titanic-how-intel-is?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[发表评论](https://newsletter.semianalysis.com/p/turning-the-titanic-how-intel-is/comments)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)
