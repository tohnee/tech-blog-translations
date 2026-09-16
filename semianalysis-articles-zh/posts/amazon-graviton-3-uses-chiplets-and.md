---
title: "Amazon Graviton 3 用小芯片与先进封装把高性能 CPU 大宗商品化 | 首款 PCIe 5.0 与 DDR5 服务器 CPU"
title_en: "Amazon Graviton 3 Uses Chiplets & Advanced Packaging To Commoditize High Performance CPUs | The First PCIe 5.0 And DDR5 Server CPU"
date: 2021-12-02
source: https://newsletter.semianalysis.com/p/amazon-graviton-3-uses-chiplets-and
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Amazon Graviton 3 用小芯片与先进封装把高性能 CPU 大宗商品化 | 首款 PCIe 5.0 与 DDR5 服务器 CPU

> 原文：[Amazon Graviton 3 Uses Chiplets & Advanced Packaging To Commoditize High Performance CPUs | The First PCIe 5.0 And DDR5 Server CPU](https://newsletter.semianalysis.com/p/amazon-graviton-3-uses-chiplets-and) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

Amazon 的 AWS 平台一直在不断打破一切常规。硬件之旅始于 2015 年收购 Annapurna Labs。今天，Amazon 发布了 Graviton3 和一款自研 SSD 控制器。第一个令人印象深刻的自研动作是多年前的 AWS Nitro。Nitro 的版图从自研 hypervisor、一颗安全芯片，一直延伸到强大的 Nitro 网卡。Amazon 把所有商用芯片供应商的 SmartNIC 和 DPU 努力甩在身后，设计并实现了自己的定制硬件栈。这些 NIC 通过把 hypervisor 与应用层分离，带来了巨大的安全与运营效率优势。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2edeffab-d216-4eea-90e4-0005fe9f0929_1024x580.png)

Amazon 不必在每台物理服务器上划出专门的 CPU 核心来跑 AWS 管理栈，而是把这部分工作卸载到自研网卡上。这让每台物理服务器有更多核心可以直接租给客户。Amazon 将此转化为相对其他云服务商的运营优势，并把利润从 Intel 之流的手中留住。Google 才刚开始在其云服务栈中把这一做法标准化。Google 与 Intel 合作打造了名为 Mount Evans 的 NIC，而且到现在才刚开始启用类似 Amazon 弹性块存储的行为。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/09c94432-6639-4252-bed8-8e714721785b_678x381.jpeg)

横向扩展存储的运营优势相当可观。存储不必内建于每台服务器，而是可以放到专门的存储服务器中实现，再在运行时虚拟化分配、供给给各种实例。客户在功能上完全察觉不到自己的存储在另一台服务器里，而 AWS 得以更高效地利用全部存储。AWS 还能针对各种实例类型提供更灵活的存储容量选择。每台物理服务器不再有存储的超额配置，存储可以更轻松地以大型专用池管理。这方面的配置选择要细得多、也多变得多，但那是另一篇文章的事了。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

这就说到今天的发布：Amazon 推出了一款自研 SSD 控制器和 Graviton3 CPU。因为我们就是爱卖关子，先聊自研 SSD 控制器。转向自研 SSD 控制器让 Amazon 在性能波动和成本上获益巨大。成本方面显而易见：他们现在直接采购裸 NAND，与自家控制器一起封装。AWS 把供应链掌握在自己手里，不必向高度多变的控制器生态低头。SSD OEM 的利润率如今归了自家。AWS 还能在全部数据中心标准化控制器和性能特征。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/db97a83c-ec4f-4deb-80c7-224aa3b582d9_1024x576.jpeg)

SSD 的控制器把数据映射到 NAND 芯片上的物理地址。这层抽象叫闪存转换层（flash translation layer，FTL）。SSD 控制器需要管理垃圾回收、trim 和磨损均衡，才能维持峰值性能和最长寿命。其中一些任务会影响性能。Amazon 正把这件事接过来，把这类管理抽象成自己可控、可更新的软件。更高程度的控制让 Amazon 得以降低性能波动。这些管理功能不会再干扰客户对高性能存储的需求，可以在后台无缝运行，不打扰客户工作负载。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b2d8f222-aea8-4d3d-a40b-e75bb6bf5010_1024x768.jpeg)

Graviton3 当然才是全场主角。Amazon 在服务器 CPU 一侧一跃成为多项技术的首发者。他们采用小芯片（chiplet）设计，包含 7 颗不同的裸片。最引人注目的是这些裸片用先进封装封装。连接各裸片的微凸点尺寸 <=55um，而 Intel 和 AMD 的每颗 CPU 至今仍停留在 >=100um。Intel 和 AMD 要到下一代 CPU 才能追上。这使得 IO 从 CPU 解聚合的设计成为可能，而不会让功耗预算失控。AMD 在 Rome 和 Milan 服务器 CPU 上的 IO 裸片功耗高达 100W。这 100W 侵占了核心的功耗预算，无法用于计算。Graviton 在把整个 CPU 功耗控制在同样约 100W 量级的同时，实现了比 AMD Milan 高 50% 的内存带宽和 PCIe 5.0 连接。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/0ce40a8d-e103-4101-9d3e-4b2ceb3e3d83_1024x768.jpeg)

64 颗核心留在单一单片裸片上、采用先进制程节点，而 PCIe 5.0 和 DDR5 的 tile 则分别流片。这种系统设计也是 Amazon 能比 Intel 或 AMD 提前约 6 个月部署 PCIe 5.0 和 DDR5 的部分原因。Amazon 借助 ARM 的公版核心和 Synopsys / Cadence 的 IP 压低了 IP 侧成本。虽然 Amazon 没有明说核心型号，但 SemiAnalysis 可以确认，Amazon 用的是 Arm 的 Neoverse V1 核心。

64 核计算裸片约 282 mm²，128b 内存控制器 DDR5 裸片约 21.7 mm²，PCIe 5.0 控制器裸片约 43.6 mm²。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e2234025-5b43-4cb1-8cd5-86a3e05435e4_1024x768.jpeg)

这个核心的选择相当有意思。多数其他超大规模云厂商在等 Neoverse N2——Neoverse N1 的后继者。Neoverse N1 是 Graviton2 和 Ampere Altra 上用的核心。V1 此前只在欧洲、韩国和印度的本国超算项目上拿过设计导入，所以 Amazon 在此的核心选择相当耐人寻味。与 N1 和 N2 相比，V1 宽得多。它提供两倍的浮点执行单元，但代价是面积更大。核心的更换带来 SPECint 2017 性能提升 25%、SPECfp 2017 提升 60%。性能和 IO 的这一巨大跃升，是在功耗和时钟频率与 Graviton2 基本持平的情况下实现的。晶体管数量也只是从 30B 增长到 50B。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/96de63a8-e1db-4aa7-a3aa-3ebfbe7fbfa1_1024x663.jpeg)

Amazon 采取的是整体系统级思路，因此他们关注计算密度。与 AMD 和 Intel 那些功耗数百瓦的巨大封装不同，Amazon 正转向相反的方向。他们往一台风冷服务器里塞 3 颗 CPU。Intel 和 AMD 的下一代 CPU 正逼近 350W-400W，而 Amazon 的目标是这个数字的 1/3 到 1/4。Amazon 在机柜层面最大化性能、最小化成本。这通过几种方式实现。

随着我们迈入 400G 和 800G 时代，网络成本占服务器成本的比例正在膨胀。每颗 CPU 配一张独立网卡的成本高得离谱。商用芯片方案通常是 1 颗 CPU、偶尔 2 颗 CPU 共享一张 NIC。Graviton3 把这个比例倒转成每张 NIC 带 3 颗从属 CPU。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/dba87224-cb15-4884-b678-fcd26290b9ae_1024x576.jpeg)

Amazon 还做了一个聪明的决定：把这些处理器做成 BGA 封装。AMD 和 Intel 等商用芯片厂商使用插座。插座增加了复杂性和成本，多了一个故障点，还降低了 CPU 与主板连接的密度，需要占用更多主板空间。卖服务器 CPU 基本必须用插座，但 Amazon 凭借垂直整合可以弃之不用。BGA 是 Amazon 能往每台服务器单元塞 3 颗 CPU 的一个关键原因。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

这些 CPU 已在大规模生产环境中部署。Amazon 用了相当长一段时间，其一些大客户如 Epic Games、F1、Twitter 和 Honeycomb 也已将其投入生产。Graviton3 的势头迅猛，其成本/$ 优势不止来自垂直整合。驱动 Graviton3 的系统级选择，让它成为通用 CPU 计算实例的赢家。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8f67f11d-a75b-4f36-8772-94cf4cdc975f_1023x581.png)

x86 CPU 厂商将保住其每颗 CPU 峰值性能的领先，但 Intel 和 AMD 正忽视一场更重要的战争。这场战争争夺的是通用 CPU 在服务器和机柜层面、每单位算力的总拥有成本（TCO）。CPU 市场的大宗商品化已经到来，即便 Intel 和 AMD 的单个核心设计明显更好，也改变不了这个等式。Intel 和 AMD 在某些方面过度聚焦，这让他们错过了系统级设计中的关键因素：峰值功耗太高、密度太低、时钟频率推得太狠。

Graviton3 应该让 Intel 和 AMD 的高管们发抖。事实上，所有商用芯片供应商都该胆寒，因为 Microsoft、Facebook、Google 和中国巨头们想在网络、CPU、SSD、AI 推理和 AI 训练上全面复制这种垂直整合。这批超大规模公司增速远超市场其余部分，正如贪婪的巨兽般吞噬着花在计算上的美元。科技垄断巨头正在走向垂直化，而这股长期的滔天巨浪似乎没有什么能阻挡。

付费墙后，我们有一些与这颗 CPU 的封装相关的非常有趣的内容，还牵扯一家总在投资者心头萦绕的半导体公司。

[分享](https://newsletter.semianalysis.com/p/amazon-graviton-3-uses-chiplets-and?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[赠送订阅](https://newsletter.semianalysis.com/subscribe?&gift=true)

[分享 SemiAnalysis](https://semianalysis.substack.com/?utm_source=substack&utm_medium=email&utm_content=share&action=share)
