---
title: "Marvell 的 DSP 困局？由 Broadcom、Nvidia、Arista Networks、Microsoft、Meta、Macom 等引领的网络行业板块级剧变"
title_en: "Marvell's DSP Dilemma? Networking’s Tectonic Shift Led By Broadcom, Nvidia, Arista Networks, Microsoft, Meta, Macom, and more"
subtitle: "Marvell 最坚固的护城河会被攻破吗？$MRVL $AVGO $NVDA $ANET $MSFT $MTSI $META"
date: 2023-03-08
source: https://newsletter.semianalysis.com/p/marvells-dsp-dilemma-networkings
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Marvell 的 DSP 困局？由 Broadcom、Nvidia、Arista Networks、Microsoft、Meta、Macom 等引领的网络行业板块级剧变

> 原文：[Marvell's DSP Dilemma? Networking’s Tectonic Shift Led By Broadcom, Nvidia, Arista Networks, Microsoft, Meta, Macom, and more](https://newsletter.semianalysis.com/p/marvells-dsp-dilemma-networkings) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Marvell 最坚固的护城河会被攻破吗？$MRVL $AVGO $NVDA $ANET $MSFT $MTSI $META**

网络行业可能正在经历一场板块级剧变（tectonic shift），供应链中的众多玩家都已入局……唯独 Marvell 除外。这一变化将直接降低对数据最饥渴的工作负载——包括生成式 AI 模型的机器学习训练与推理，也包括通用计算——的延迟、功耗和成本。Marvell 过去几年最具变革意义的收购是 Inphi——PAM4 DSP（数字信号处理器）、TIA（跨阻放大器）和驱动器（driver）领域的领导者。得益于 Inphi 以及如今的 Marvell，数据中心内部的光网络速度取得了惊人的进步。

然而并非一片坦途。网络行业的所有其他巨头——包括 Broadcom、Nvidia、Arista Networks、Microsoft、Meta、Macom 等等——正齐心协力地把 Marvell 从设计中剔除出去（design out）。这场针对 Marvell 网络业务巨额盈利能力的攻击并非只是正面强攻，更像是千刀万剐式的凌迟。考虑到这些竞争对手在各个细分市场所占据的份额，这千刀中的某些甚至可以称作「武士刀式的斩击」。Marvell 不会坐以待毙，他们正在反击。

最大的问题在于：技术路线图、部署、市场份额和收入份额将走向何方。今天，我们想回答这些问题，并讨论 Marvell 面临的诸多挑战——这些挑战足以把他们当前的统治地位拉下几个台阶。

![](https://substack-post-media.s3.amazonaws.com/public/images/f0061a02-b5d2-43fc-bdea-c371f5bd5633_2098x648.png)

在深入探讨商业影响与技术变革之前，先解释一下数据中心网络的基础知识。如果你已了解这些内容，请直接下翻至「对 Marvell 的战争」（The War On Marvell）一节。本文的大部分内容讲的是当前与未来的市场/技术。

数据中心中几乎所有超过几米的通信都使用光纤。交换机等网络芯片的端口位于服务器背面，由一个称为收发器（transceiver）的模块把电信号转换为光信号。这个模块内有 6 个关键器件：

1. DSP（数字信号处理器）：DSP 接收来自交换 ASIC 的串行化输入，将其从模拟转换为数字，并执行信号调理、均衡、纠错和时钟/数据恢复等功能。随后它把这些数字信号转换回模拟信号并向前推送。
2. 驱动器（Driver）：驱动器接收模拟输入，为激光器提供产生所需光信号所必需的电流和电压。
3. 激光器（Laser）：激光器负责发射特定波长的光，其强度可以被调制，从而把数据编码到光信号上。
4. 发射光学器件（Transmit Optics）：发射光学器件负责把激光器产生的光信号整形并导向光纤。它可以包含透镜、镜面及其他光学元件。视光学架构而定，它也可以承担信号调制。
5. 接收光学器件（Receive Optics）：接收光学器件负责接收经网络传输而来的光信号，并将其聚焦到光电二极管上。它可以包含透镜、镜面及其他把入射光信号导向光电二极管的光学元件。
6. TIA（跨阻放大器）：TIA 把接收端光电二极管产生的电流信号转换为电压信号。它对该信号进行放大以改善信噪比，然后送入 DSP（数字信号处理器）做进一步处理。

光格式的技术种类繁多，但在数据中心内最重要的有 3 种。它们都以每 lambda（光的颜色）100G 为基础。可以此作为快速指南：

1. AOC 400G/800G——数字代表发射/接收对（transmit and receive pairs）的数量。AOC 是距离最短的标准，最长仅 30 米至 100 米，但功耗也最低。它使用较便宜的多模光纤和直接驱动的 VCSEL 激光器。
2. DR4/DR8 400G/800G——有 4 条或 8 条发射光纤及相应数量的接收光纤，合计 8 或 16 条光纤。它使用单模光纤。该标准存在多种版本，最大传输距离从 500 米到 2km 不等。
3. FR4/2xFR4/FR8 400G/800G——这些是在单模光纤上调制光的波长。存在多种版本，最大传输距离从 2km 到 10km 不等。由于把多路光复用到一根光纤会引入损耗，该标准的功耗最高。

接下来，我们谈谈其他网络巨头正在做的事情——这些动作可能严重削弱 Marvell 的市场地位。参与者包括 Broadcom、Nvidia、Arista Networks、Microsoft、Meta、Macom、Intel、Maxlinear、Coherent、Credo、Poet、Innolight、Hisense、Alphawave、Semtech、Accelink、Colorchip、Coherent、Eoptolink、Applied Optoelectronics 和 Cloud Light。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
