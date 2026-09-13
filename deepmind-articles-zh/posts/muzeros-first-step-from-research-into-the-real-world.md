---
title: "MuZero 从研究走向现实世界的第一步"
title_en: "MuZero's first step from research into the real world"
source: https://deepmind.google/blog/muzeros-first-step-from-research-into-the-real-world/
site: deepmind
date: 2022-02-11
crawled: 2026-09-13
translated: 2026-09-13
---

# MuZero 从研究走向现实世界的第一步

> 原文：[MuZero's first step from research into the real world](https://deepmind.google/blog/muzeros-first-step-from-research-into-the-real-world/) · Google DeepMind

与 YouTube 合作，在开源 VP9 编解码器中优化视频压缩。

2016 年，我们推出了 [AlphaGo](https://deepmind.com/research/case-studies/alphago-the-story-so-far)——首个在围棋这一古老棋类中战胜人类的人工智能程序。它的后继者 [AlphaZero](https://deepmind.com/blog/article/alphazero-shedding-new-light-grand-games-chess-shogi-and-go) 以及后来的 [MuZero](https://deepmind.com/blog/article/muzero-mastering-go-chess-shogi-and-atari-without-rules)，都在追求通用算法的道路上各自迈出了重要一步，以更少的预置知识掌握了更多的游戏。例如，MuZero 无需被告知规则就掌握了国际象棋、围棋、将棋和 Atari 游戏。但到目前为止，这些智能体专注于解决游戏。如今，在践行 DeepMind 破解智能使命的过程中，MuZero 通过优化 YouTube 上的视频，向掌握一项现实世界任务迈出了第一步。

在[发表于 arXiv 的预印本](https://arxiv.org/abs/2202.06626)中，我们详细介绍了与 YouTube 的合作，探索 MuZero 改进视频压缩的潜力。[分析机构预测](https://www.cisco.com/c/dam/m/en_us/solutions/service-provider/vni-forecast-highlights/pdf/Global_2021_Forecast_Highlights.pdf)，流媒体视频在 2021 年已占互联网流量的绝大多数。随着 COVID-19 疫情期间视频流量激增，以及预计未来互联网总流量还将继续增长，视频压缩正成为一个日益重要的问题——也是将强化学习（RL）应用于在具有挑战性的领域中超越现有水平的天然阵地。自部署到 YouTube 部分实时流量以来，我们在一大批多样的视频上展示了平均 4% 的码率降低。

大多数在线视频都依赖一个称为编解码器（codec）的程序，在源头对视频进行压缩或编码，通过互联网传输给观众，然后解压或解码以供播放。这些编解码器要为视频的每一帧做出多个决策。数十年的手工工程投入已用于优化这些编解码器，它们支撑着如今互联网上许多视频体验——包括点播视频、视频通话、电子游戏和虚拟现实。不过，由于 RL 特别适合解决编解码器中那类序贯决策问题，我们正在探索 RL 习得的算法能如何提供帮助。

我们最初聚焦于 VP9 编解码器（具体来说是开源版本 [libvpx](https://github.com/webmproject/libvpx)），因为它被 YouTube 和其他流媒体服务广泛使用。与其他编解码器一样，使用 VP9 的服务提供商需要考虑码率（bitrate）——发送视频每一帧所需的 0 和 1 的数量。码率是服务与存储视频所需算力和带宽的主要决定因素，影响从视频加载时长到分辨率、缓冲和数据用量的一切。

![概念图，展示 VP9 编解码器如何随时间压缩视频帧。顶部三幅连续视频帧描绘一辆汽车从左向右驶过静止的树和云。每帧下方有一个箭头指向蓝色的"VP9"处理图标，图标之间水平相连以表示顺序编码。最右侧一个箭头指向一组堆叠的重叠帧，标注为"压缩视频"（Compressed video），叠加在汽车运动路径之上，对应底部说明："VP9 参照先前的帧压缩视频帧。"](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6224b3fd1ef1ea596a41d25a_VP920compression.gif)

在编码视频时，编解码器利用先前帧的信息来减少后续帧所需的比特数。

在 VP9 中，码率最直接的优化途径是码率控制模块中的量化参数（QP）。对每一帧，这个参数决定施加的压缩程度。在给定目标码率的情况下，视频各帧的 QP 按顺序决定，以最大化整体视频质量。直观上，复杂场景应分配更高的码率（更低的 QP），静态场景应分配更低的码率（更高的 QP）。QP 选择算法要推理一帧的 QP 值如何影响其余视频帧的码率分配和整体视频质量。RL 在解决这类序贯决策问题时尤其有用。

![流程图，说明 MuZero-RC 如何与 VP9 视频压缩编解码器集成。顶行是三幅连续视频帧，描绘一辆汽车从左向右移动。每帧下方有一个蓝色 VP9 编码图标按顺序处理视频。每个 VP9 图标下方是一个对应的蓝色图标，标注为"MuZero-RC"，通过垂直双向箭头与 VP9 相连，其中一条标注"QP"的箭头指回 VP9，表示码率控制决策。最终压缩输出显示在最右侧，是一组标注为"压缩视频"（Compressed video）的重叠帧。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/6224b41588a4994b5c6efc29_MuZero.gif)

对 VP9 处理的每一帧视频，MuZero-RC——取代 VP9 默认的码率控制机制——决定施加的压缩程度，以更低的码率实现相近的质量。

MuZero 通过将搜索的力量与学习环境模型并据此规划的能力相结合，在各类任务上取得超越人类的性能。这在庞大的组合式动作空间中尤其有效，使它成为视频压缩中码率控制问题的理想候选方案。然而，要让 MuZero 在这个现实世界应用中运转，需要解决一整套全新的问题。例如，上传到 YouTube 这类平台的视频在内容和质量上千差万别，任何智能体都需要跨视频泛化，包括部署后出现的全新视频。相比之下，棋盘游戏往往只有一个已知的环境。此外还有许多其他指标和约束影响最终的用户体验和码率节省，例如 PSNR（峰值信噪比）和码率约束。

为了让 MuZero 应对这些挑战，我们创建了一个名为自我竞争（self-competition）的机制，通过将智能体的当前表现与其历史表现比较，把视频压缩这一复杂目标转化为简单的胜/负信号。这让我们能把丰富的编解码器需求集合转化为一个可供智能体优化的简单信号。

通过学习视频编码的动力学并确定分配比特的最佳方式，我们的 MuZero 码率控制器（MuZero-RC）能够在不损失质量的前提下降低码率。QP 选择只是编码过程中众多编码决策之一。尽管数十年的研究和工程已经产生了高效的算法，我们设想的是单一算法能够自动学习做出这些编码决策，以获得最优的率失真权衡。

超越视频压缩，这将是 MuZero 走出研究环境的第一步，也是我们的 RL 智能体能够解决现实世界问题的一个范例。通过打造具备一系列新能力、可跨领域改进产品的智能体，我们可以帮助各种计算机系统变得更快、更省资源、更自动化。我们的长期愿景是开发出单一算法，能够跨多个领域优化数以千计的现实世界系统。

欢迎收听 Jackson Broshear 和 David Silver 与 Hannah Fry 在《DeepMind：播客》第 5 集中讨论 MuZero。在你喜爱的播客应用中搜索"DeepMind: The Podcast"即可收听。

**注记**

本工作由以下贡献者合作完成：Chenjie Gu、Anton Zhernov、Amol Mandhane、Maribeth Rauh、Miaosen Wang、Flora Xue、Wendy Shang、Derek Pang、Rene Claus、Ching-Han Chiang、Cheng Chen、Jingning Han、Angie Chen、Daniel J. Mankowitz、Julian Schrittwieser、Thomas Hubert、Oriol Vinyals、Jackson Broshear、Timothy Mann、Robert Tung、Steve Gaffney、Carena Church
