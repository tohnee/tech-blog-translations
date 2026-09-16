---
title: "NVIDIA 的光学「怪兽」——NVL72、InfiniBand 横向扩展、800G 与 1.6T 爬坡"
title_en: "Nvidia’s Optical Boogeyman – NVL72, Infiniband Scale Out, 800G & 1.6T Ramp"
subtitle: "收发器与 GPU 之比、DSP 增长、揭示真正的怪兽"
date: 2024-03-25
source: https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# NVIDIA 的光学「怪兽」——NVL72、InfiniBand 横向扩展、800G 与 1.6T 爬坡

> 原文：[Nvidia’s Optical Boogeyman – NVL72, Infiniband Scale Out, 800G & 1.6T Ramp](https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**收发器与 GPU 之比、DSP 增长、揭示真正的怪兽**

在 GTC 上，NVIDIA 发布了 8 种以上基于 Blackwell 架构的不同 SKU 和配置。虽然存在一些芯片级差异（如显存和 CUDA 核心数量），但大多数配置差异在系统层面，比如外形规格、网络、CPU 和功耗。NVIDIA 提供了多种 8 GPU 基板风格的配置，但其在 GTC 上的主打重点是垂直整合的 DGX GB200 NVL72。

它不是我们习以为常的典型 8 GPU 服务器，而是一个单一整合机柜：72 张 GPU、36 颗 CPU、18 颗 NVSwitch、72 张用于后端网络的 InfiniBand NIC，以及 36 张用于前端网络的 Bluefield 3 以太网 NIC。

![](https://substack-post-media.s3.amazonaws.com/public/images/9dc1f225-78eb-4313-bddf-6e3e05f78127_2396x1248.png)
*NVIDIA*

## **光模块与 GB200 NVL72 恐慌**

上周主题演讲中发布 NVIDIA DGX GB200 NVL72 时——它能在同一机柜内以每 GPU 900GB/s 的 NVLink 5 连接 72 张 GPU——恐慌开始蔓延。各个光模块市场里的「游客」们在听完黄仁勋的话后反应剧烈，开始夺路而逃。

> 于是我们有了 5,000 根线缆，5,000 根 NVLink 线缆，总共 2 英里。接下来才是令人惊叹的地方。如果我们不得不用光互连，就得用上收发器和重定时器（retimer）。而光是这些收发器和重定时器本身就要耗掉 20,000 瓦——20 千瓦，仅仅为了驱动 NVLink spine。结果，我们通过 NVLink 交换机完全免费地做到了这一点，省下的 20 千瓦可以留给计算。
>
> 黄仁勋

![](https://substack-post-media.s3.amazonaws.com/public/images/c40e4946-a6b2-4053-bfa0-09b3a8f252de_4032x3024.jpeg)
*每台 NVSwitch 连接 288 根铜缆*

这些惊慌失措的观察者们把「用 5,184 根直驱铜缆把 NVLink 纵向扩展到 72 张 GPU」看作前来搅局各家光模块供应链厂商的光学怪兽。许多人辩称，由于 NVLink 网络连接了机柜内的全部 72 张 GPU，实现集群内 GPU 互连所需的光模块就更少了。这些光学「游客」以为光模块强度——也就是每个 NVIDIA GPU 集群所需的光收发器数量——会大幅下降。

这是错的，他们误解了黄仁勋的话。光模块数量并不会下降。

![](https://substack-post-media.s3.amazonaws.com/public/images/f0e64656-fc49-409b-a401-c3979812fd8b_2480x1456.png)
*NVIDIA*

DGX H100 和 DGX GB200 NVL 利用三张不同的网络：一张跑以太网的前端网络，每 NIC 对应 2 或 4 张 GPU；一张跑 400G 或 800G 的后端横向扩展 InfiniBand 或以太网网络（视配置而定），但始终是每 GPU 对应 1 张 NIC；还有一张后端纵向扩展的 NVLink 网络，把全部 8 张或 72 张 GPU 连在一起。

![](https://substack-post-media.s3.amazonaws.com/public/images/41f6bfad-c9b3-40d2-90ea-06418048f45f_1225x990.png)
*NVIDIA*

至于后端横向扩展网络——GTC 上展示的 NVL72 机柜仍然有 72 个 400G/800G 的 OSFP 端口——每张 GPU 一个——这与 H100 上实现的连接方式完全相同——也就是说光收发器与 GPU 之比不变。随着 GPU 网络规模扩大，所需的光收发器数量也同步扩大。

![](https://substack-post-media.s3.amazonaws.com/public/images/2deb5e62-4783-4975-a6ff-9f0b694c38f9_1495x895.png)
*为简化起见假设顶层满配，完整光模块模型的范围延伸到 100k GPU*

唯一不往 GB200 NVL72 的 72 个 OSFP 端口插满收发器的情形，是你计划只买一台 GB200 NVL72 机柜。需要说明，没有人会只买 1 台机柜，因为那样还不如直接买 8 GPU 基板。其次，部署灵活性就是一切：短期内你可能打算让一台服务器或一个机柜专用于某种用途，但这个用途会随时间改变，比例也就随之改变。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

NVL72 并不是人们该担心的那个光学怪兽，还有另一个真实得多的光学怪兽。

这个光学怪兽会大幅削减收发器数量，而且明年就要大批量出货。下面我们将解释它是什么、如何实现、以及削减多少。
