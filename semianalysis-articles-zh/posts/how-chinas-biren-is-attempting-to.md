---
title: "中国壁仞（Biren）如何试图规避美国制裁"
title_en: "How China’s Biren Is Attempting To Evade US Sanctions"
subtitle: "新规形同瑞士奶酪，漏洞终将被堵上"
date: 2022-10-24
source: https://newsletter.semianalysis.com/p/how-chinas-biren-is-attempting-to
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 中国壁仞（Biren）如何试图规避美国制裁

> 原文：[How China’s Biren Is Attempting To Evade US Sanctions](https://newsletter.semianalysis.com/p/how-chinas-biren-is-attempting-to) · SemiAnalysis

**新规形同瑞士奶酪，漏洞终将被堵上**

壁仞（Biren）是中国的人工智能硬件头部企业，目前正在设法规避制裁。Bloomberg 一篇仅基于单一信源的报道错误地声称，由于出口管制存在一个「关键缺口」，TSMC 仍将[向壁仞供货](https://www.bloomberg.com/news/articles/2022-10-21/one-chinese-chip-startup-shows-key-gap-in-biden-export-curbs)。Bloomberg 随后[又用「霰弹枪式」报道法发出了内容相反的报道](https://www.bloomberg.com/news/articles/2022-10-22/tsmc-said-to-suspend-work-for-chinese-chip-startup-amid-us-curbs?)，同样只依赖单一信源。与其争论媒体的报道质量，不如拆解一下当前局势，并独家详解壁仞规避制裁的具体手法。

先介绍一些壁仞的背景。虽然中国有许多公司都在开发并出货面向高性能计算和人工智能的芯片，但壁仞拥有其中最先进的架构和已量产的最先进芯片。我们独立与多位 Nvidia 员工交流过壁仞的情况，他们的评价都是正面的。其中一位甚至告诉我们，他们认为对 Nvidia AI 训练硬件主导地位的威胁中，壁仞比来自 [Intel](https://www.semianalysis.com/p/intel-is-throwing-the-kitchen-sink)、[AMD](https://www.semianalysis.com/p/amd-to-infinity-and-beyond)、[Graphcore](https://www.semianalysis.com/p/graphcore-announces-worlds-first)、[SambaNova](https://www.semianalysis.com/p/nvidia-in-the-hot-seat) 或 [Cerebras](https://www.semianalysis.com/p/cerebras-wafer-scale-hardware-crushes) 的竞争更大。看看壁仞的融资规模，以及其工程师中有多少人曾在西方大厂工作（包括一大批前 Nvidia 上海员工），听到这种评价并不令人意外。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a32f6ee7-cbce-4313-ac25-680d2cccee94_3004x1666.png)

壁仞设计了一款多芯片模块（MCM）方案，采用 TSMC N7 制程节点和 [TSMC CoWoS-S](https://www.semianalysis.com/p/advanced-packaging-part-2-review) 封装。虽然目前[中国境内还没有任何晶圆厂有能力制造](https://www.semianalysis.com/p/chinas-smic-is-shipping-7nm-foundry)如此先进的 AI 芯片，但中国已有多家公司掌握了 2.5D 集成能力。这颗裸片用于两款产品：一款是双裸片模块 BR100，另一款是单裸片模块 BR104。单颗裸片的最高规格为：INT8 算力 1024 TOPS、裸片间互连带宽 896GB/s、BLink 带宽 256GB/s、CXL 2.0 带宽 128GB/s。

正如我们在[对中美两项新规的全面解读](https://semianalysis.substack.com/p/china-and-usa-are-officially-at-economic)中所解释的，这将使 BR100 远超美国政府规定的性能门槛。

> 该测试针对同时满足 600 GB/s IO 和 [4800（性能×位宽）或 600 TOPS 性能] 的芯片。按此定义，Nvidia 的 A100、H100，AMD 的 MI250X，壁仞的 BR100，Graphcore 的 BOW，Cerebras 的 WSE 等均被覆盖。

这立即将 BR100 排除在外：它封装了 2 颗此类裸片，合计性能和 IO 水平为 INT8 算力 2048 TOPS、裸片间互连带宽 896GB/s、BLink 带宽 512GB/s、CXL 2.0 带宽 128GB/s。上述规格按计算单元 1GHz 时钟假设得出，但这些时钟频率很容易更改，这也凸显了管制规则的一个重大缺陷。

仅 BLink 与 CXL 2.0 合计就达到了 IO 速度限制的门槛。美国管制规则对 TOPS 的定义非常宽泛，与壁仞对 TOPS 数值的定义口径不同。

> 4800 bit×TOPS 的门槛，可通过 8 位精度下 600 万亿次整数运算，或 16 位精度下 300 tera FLOPS 来满足。
>
> 美国工业与安全局（BIS）

BR100 显然被排除在外，而 BR104 的大部分规格减半。仅就 TOPS 要求而言，它仍然明显超标。整颗芯片的带宽为：裸片间互连 896GB/s（未启用）、BLink 256GB/s、CXL 2.0 128GB/s、内存带宽 819GB/s。

> 集成电路若具有或可编程实现：向/来自除易失性存储器以外的其他集成电路的所有输入与输出端口的双向总传输速率达到 600 Gbyte/s [GB/s] 或以上
>
> 美国工业与安全局（BIS）

美国政府的定义并未把产品自身的内存带宽计入 IO。该规则的解读中也没有明确说明，这一指标指的是裸片/小芯片（chiplet），还是已完成的封装产品。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/26680f01-4879-4e57-823c-4a159635c0cd_3542x682.png)

壁仞试图通过更改产品规格来规避制裁。他们把 BR100 的 BLink 数量从 8 个削减到 7 个，使 BLink + CXL 2.0 合计带宽降至 576GB/s。壁仞认为这样一来就降到了制裁门槛之下。

管制出台之前，在 [AI Hardware Summit](https://www.semianalysis.com/p/meta-discusses-ai-hardware-and-co) 上，我们曾与一位壁仞员工交流过他们的网络拓扑，以及其 200 代产品外置交换机的设计。当时壁仞计划在 BR100 上将全部 8 个 BLink 同时用于节点内和节点间互连。制裁出台后，壁仞改变了说法，并更新了官网，希望通过削减产品规格来避开制裁。而美国政府并没有任何办法验证第 8 个 BLink 是否真的被禁用了。

无论如何，这种做法仍然回避了一个事实：每颗裸片都有一条 896GB/s 的裸片间互连，用于与同一封装内的另一颗裸片进行高速、低延迟连接。BR104 产品的裸片间互连在技术上并未启用，但该功能仍然存在于裸片上。美国政府文件中没有任何指引说明，芯片上处于启用还是未启用/被降 bin/被裁剪状态的部分是否属于管制范围。鉴于美国政府无法验证芯片的某一部分是否已被永久禁用，他们不敢冒这个险。

美国政府文件同样没有就「发晶圆还是发封装成品」给出任何指引。TSMC 的大部分收入来自向外包封测（OSAT）厂商发运晶圆，由后者为 TSMC 的最终客户做切割、封装和组装。以 Nvidia 的 A100、H100 GPU 以及壁仞为例，TSMC 负责切割和部分封装工序。Nvidia 目前大部分高端数据中心 GPU 的其余封装和组装工作是在中国完成的。

全球最强超算 Frontier 采用的是 AMD 的 MI250X，该产品并不使用 TSMC 的封装技术。AMD 使用 TSMC 的晶圆，随后发运给 OSAT 厂商 ASE，由其完成切割和封装。如果 TSMC 把成品晶圆发往中国，壁仞就可以利用中国本土的 OSAT 能力，使用 Besi、Veeco 等厂商目前不受限制的设备，制造出完整的 BR100。因此，成品晶圆也应受到限制。

最后，较低端的 BR104 产品的出货同样应当受到限制。中国的 OSAT 厂商完全有可能把 BR104 上的 [CoWoS-S](https://www.semianalysis.com/p/advanced-packaging-part-2-review) 封装拆开，再用这些拆解出来的裸片组装成 BR100——而且用 2010 年以前的设备就能做到。此外，只要修改芯片封装和引脚分布（pin-out），那 896GB/s 的裸片间互连依然可以被利用起来。

可以清楚地看到，壁仞正在试图规避制裁。

[分享](https://newsletter.semianalysis.com/p/how-chinas-biren-is-attempting-to?utm_source=substack&utm_medium=email&utm_content=share&action=share)

同样清楚的是，这轮制裁条款写得很不严谨，半导体设备部分尤甚。由于存在重大漏洞和执法难题，这些禁令很可能无法实现其目标。

最后，我们分享几张关于壁仞架构的幻灯片。在所有 AI 硬件初创公司中，这一架构与 Nvidia 的相似度最高。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ab1a3735-4277-45af-95db-616a566c326a_3022x1623.png)
![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1a457214-f7ff-4dc2-872f-c9eb3f72b154_3023x1618.png)
![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1f158df8-61cf-444b-bae4-5dda1c4e983b_3023x1618.png)

[赠送订阅](https://newsletter.semianalysis.com/subscribe?&gift=true)

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
