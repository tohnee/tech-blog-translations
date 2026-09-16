---
title: "NVIDIA B100、B200、GB200——COGS、定价、利润率、爬坡——Oberon、Umbriel、Miranda"
title_en: "Nvidia B100, B200, GB200 - COGS, Pricing, Margins, Ramp - Oberon, Umbriel, Miranda"
subtitle: "这个 B 代表黄仁勋的恩泽"
date: 2024-03-18
source: https://newsletter.semianalysis.com/p/nvidia-b100-b200-gb200-cogs-pricing
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie", "Chaolien Tseng"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# NVIDIA B100、B200、GB200——COGS、定价、利润率、爬坡——Oberon、Umbriel、Miranda

> 原文：[Nvidia B100, B200, GB200 - COGS, Pricing, Margins, Ramp - Oberon, Umbriel, Miranda](https://newsletter.semianalysis.com/p/nvidia-b100-b200-gb200-cogs-pricing) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**这个 B 代表黄仁勋的恩泽**

NVIDIA 在 GTC 上发布了新一代 Blackwell GPU。我们急切等待完整架构白皮书的发布，以详细了解张量内存加速器（tensor memory accelerator）急需的改进，以及新 MX 数值格式的具体[实现——此前已在此讨论过](https://www.semianalysis.com/p/neural-network-quantization-and-number)。

我们在[这里](https://www.semianalysis.com/p/nvidias-plans-to-crush-competition)讨论过该架构的许多高层特性，如工艺节点、封装设计、HBM 容量、SerDes 速率，下面让我们更深入地探讨系统、爬坡、定价、利润率，以及黄仁勋的恩泽。

NVIDIA 如今站在世界之巅。尽管[超大规模云厂商的自研芯片正在爬坡](https://www.semianalysis.com/p/accelerator-model)，他们此刻仍握有至高无上的定价权。所有人都只能乖乖接受 NVIDIA 用银勺喂到嘴边的东西。头号例证就是 H100，其毛利率超过 85%。性能与 TCO 的优势依然成立，因为 B100 把 MI300X、Gaudi 3 和超大规模云厂商的自研芯片按在地上摩擦（[Google TPU 除外](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy)）。

订阅读者将看到爬坡、定价，以及新的 B100、B200 和 GB200。定价会让很多人大吃一惊，因此我们喜欢说这个 B 代表的是**恩泽（Benevolence）**而不是 Blackwell——因为我们主与救主黄仁勋的恩典正普照世界，尤其惠及[算力贫乏者（GPU-poor）](https://www.semianalysis.com/p/google-gemini-eats-the-world-gemini)。

## **B100 / B200 配置**

[如前所述](https://www.semianalysis.com/p/nvidias-plans-to-crush-competition)，Blackwell 拥有两颗光罩极限尺寸的 GPU 裸片。GPU 计算裸片将和 Hopper 一样停留在 4nm——这是 NVIDIA 第一次不为数据中心 GPU 选择制程节点迁移。这一点相当值得关注，因为 V100、A100 和 H100 的裸片面积都在约 800mm2 上下。如今无法通过缩小制程节点换取更大的晶体管预算，他们只能把硅片面积翻倍。这是[由于台积电初版 3nm（N3B）的问题](https://www.semianalysis.com/p/tsmcs-3nm-conundrum-does-it-even)。

此外，最多有 8 颗 8 层堆叠（8-hi）的 HBM3E，容量*最高* 192GB。SK 海力士（SK Hynix）和美光（Micron）都是供应商，其中绝大部分来自 SK 海力士。这与 H100 爬坡期 [SK 海力士独家供应](https://www.semianalysis.com/p/ai-server-cost-analysis-memory-is)的局面有所不同。三星（Samsung）尽管发布了开发「全球最快」HBM3E 的[公告](https://news.samsung.com/global/samsung-develops-industry-first-36gb-hbm3e-12h-dram)，依然继续掉队。三星热爱发新闻稿，但他们在客户认证（qualification）上正面临重大挑战。

GPU 路线图的趋势是：更大的封装里塞进更多硅片（逻辑与内存皆然），而硅中介层在尺寸上正逼近极限。尺寸增大会让硅片处理难度大增，从而毁掉良率。B100 封装大得多，因此它将是首个采用 [CoWoS-L](https://www.semianalysis.com/p/ai-capacity-constraints-cowos-and) 的重量级大批量产品。CoWoS-L 是一种带无源硅桥的有机 RDL 基板方案。

Blackwell 的第一个版本 B100，代号 Umbriel，主打上市速度，保留 PCIe Gen 5、400G 网络等。事实上，风冷 700W 的 B100 几乎无需任何改动就能插入现有的兼容 H100 和 H200 基板的服务器。尽管如此，机箱内的 NVLink 速率翻倍。

B200 随后很快跟进，功耗上限提高到 1,000W。这个版本需要重新设计服务器。根据我们台湾新分析师 Chaolien 的产业调研，1,000W 版本仍然可以风冷，这会让很多人意外。这两款都保留 PCIe Gen 5，每台服务器 3.2T 网络。

至于标准的纯 GPU 产品，Umbriel 之后是 Miranda。Miranda 启用 PCIe Gen 6 和最高 800G 网络，每台服务器 6.4T。路线图上它的显存最高 192GB。不过，SK 海力士和美光明年年初将要爬坡的 36GB HBM 供应已全部被 NVIDIA 买断。这意味着可能会有一款升级版（refresh），把每颗 GPU 的显存真正提升到 288GB。

[分享](https://newsletter.semianalysis.com/p/nvidia-b100-b200-gb200-cogs-pricing?utm_source=substack&utm_medium=email&utm_content=share&action=share)

供应链上下都在热议的产品是 Oberon GB200 平台。我们将在订阅版中讨论它的定价、COGS、利润率、爬坡，以及黄仁勋的恩泽。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
