---
title: "Caliptra——首个进入所有数据中心芯片的开源硅 IP"
title_en: "Caliptra – First Open-Source Silicon Going Into All Datacenter Chips"
subtitle: "Microsoft、Google、AMD 和 Nvidia 的每一颗芯片"
date: 2022-10-25
source: https://newsletter.semianalysis.com/p/caliptra-first-open-source-silicon
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# Caliptra——首个进入所有数据中心芯片的开源硅 IP

> 原文：[Caliptra – First Open-Source Silicon Going Into All Datacenter Chips](https://newsletter.semianalysis.com/p/caliptra-first-open-source-silicon) · SemiAnalysis

**Microsoft、Google、AMD 和 Nvidia 的每一颗芯片**

开源驱动着整个科技行业。哪怕只是读到这篇文章，数据就已经流经了从网络到操作系统再到浏览器的许多层开源组件。然而，尽管开源在软件的生产部署中无处不在，在消费级或数据中心应用中实际量产的开源硅 IP 几乎为零。

这种开源硅 IP 缺位的局面将很快改变，这要归功于 [Caliptra](https://www.opencompute.org/documents/caliptra-silicon-rot-services-09012022-pdf)——开源革命终于降临到硅片上的第一个实例。虽然此前也有一些学术性、小批量的开源尝试，但 Caliptra 将被多家供应商实装到芯片中，并部署到世界各地的数据中心。

在 2022 年 Open Compute Project（OCP）大会上，Caliptra 由 Microsoft、Google 和 AMD 联合发布。Nvidia 不久前也加入了该项目并将开始贡献力量。在 OCP 上与几位参与该项目的工程师交流后，有一点似乎很清楚：Microsoft 和 Google 将把「实装基于 Caliptra 的开源可信根（silicon root of trust）」作为一项硬性要求，覆盖供其数据中心使用的全部计算、网络以及内存/存储控制器芯片。

这个项目的动因在于，Microsoft 和 Google 希望在自研及合作伙伴的硅片中实装不同形态的可信根。我们的理解是，AMD 接下了这些需求，并希望把各家伙伴拉到一起。三家公司携手打造了一个类似 Titan 的开放标准，但获得了更广泛的认同，并专注于开放式开发。Google 和 Microsoft 的目标是在 2024 年于自研硅片中实装 Caliptra，AMD 则紧随其后。

这个项目能否在上述 4 家巨头之外获得更广泛的采纳至关重要——既关乎安全，也关乎把开源 RTL 的理念带进先进半导体的更多环节，开启一个全新的创新时代。

[分享](https://newsletter.semianalysis.com/p/caliptra-first-open-source-silicon?utm_source=substack&utm_medium=email&utm_content=share&action=share)

# **什么是可信根（root of trust）？**

可信根是一块在启动过程中建立信任链的 IP。它确保 bootloader 加载的固件经过签名且可信。如果该固件可信，它才会继续加载其他软件，例如操作系统。每个可信根都有一个在制造过程中生成的唯一签名。可信根可以防范供应链层面的攻击，例如服务器中被植入未经授权的芯片以及固件被篡改等。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/20bd854e-588f-49cc-a28c-8bbe3369b1c1_1355x850.png)

目前，Microsoft、Google、HPE、Dell 等公司都会集成一颗独立的裸片，在服务器层面建立可信根，但在芯片层面仍然没有标准化的方案。随着 SOC 功能日益复杂、[可组合服务器架构逐渐普及](https://semianalysis.substack.com/p/cxl-deep-dive-future-of-composable)，安全问题将更难处理。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/eda7a4b7-ad62-470b-bb8c-c83b62b9c7fb_1353x856.png)

数据面中的每一颗处理器都必须有一种标准化的方法，来检测、度量、验证和测试该芯片及其上运行固件的安全性。Caliptra 项目希望把可信根的「保护与恢复」职能与「检测」职能解耦。可以把 Caliptra 想象成一座安全孤岛，由它来启动集成它的 SOC 的其余部分。由于可信根直接集成在 SOC 内部，想要通过固件攻击或供应链攻击欺骗总线、提取密码学签名都要困难得多。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6834bbcb-5c6d-4005-9a5d-d39f189e7104_1521x692.png)

这种拆分也让 Caliptra 的硬件架构能被各类无厂设计公司（fabless）轻松实现。设计公司无需再添加与更新、回退、A/B 恢复、TPM 以及所有权流转相关的功能。据一位参与该产品开发的工程师介绍，这种简洁性还使 Caliptra 的裸片面积在 7nm 级制程节点上远小于 1mm²。下面是这一硬件模块的框图。它是一座自成体系的孤岛，拥有自己的 RISC-V 核心、只读存储器、IO 和密码学子系统。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f29dab11-786a-4a7a-be8f-f57081e77908_1345x843.png)

Caliptra 的开源属性使其高度透明，并保证了实现的一致性。将范围限定在检测模型，使得它易于实现，并能跨设计高度复用。

> 这不是一个关于差异化的故事，而是一个关于一致性的故事。Caliptra 不是供应商「增值功能」的着陆台。
>
> Hemaprabhu Jayanna，AMD 产品安全总监 – 架构与工程

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c2f5fe1e-5518-4997-b5ed-18fdc2f995fc_1353x827.png)

部署路径有两条。无论哪条路径，Caliptra 都将持有并派生设备身份、度量并认证数据块（blob），并执行易失性所有权（volatile ownership）控制。在传统式服务器部署中，传统 SOC 的 BROM（boot ROM）是受信任的，并掌管固件加载顺序。而在新型部署中，Caliptra 开源可信根将掌管启动 IO、固件布局、SOC 时序、复位以及 DMA 孤岛。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/93832b56-7966-41ed-aca1-bb7a453824f2_1351x847.png)

专有的/经 OEM 签名的分叉固件是不被允许的。

> 制造商获得的能力是：确保其设备上只能运行正版代码；随后设备所有者获得的权利是：只有经过授权的正版代码才能在该设备上运行。Caliptra 不运行任何专门由 OEM 签名或由云厂商签名的专有固件。它始终包含设备制造商的参与，而且必须是开源固件。这条用于度量的信任路径的目标之一，就是确保一致性和透明度。我们希望避免碎片化、分叉，以及把其他能力塞进安全技术导致污染。我们经常看到，随着时间推移，出色的安全技术被管理层的好点子以及各种可以塞进安全边界之内的东西所侵蚀。不知不觉间，一项安全技术就开始膨胀，其安全态势也随之弱化——因为它做的已不只是安全这一件事。我们要让 Caliptra 保持纯净和精简。
>
> Bryan Kelly，Microsoft 主任固件工程师 – 首席硬件安全架构师

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1482f7af-4384-4f67-8716-99deb7c0ccd5_1351x847.png)

我们对此感到兴奋，并相信它将成为现实。如果你是一名硬件或安全架构师，应当认真考虑加入这个项目。最终，凡是卖给 Microsoft 和 Google 的未来设计，都必须实装 Caliptra。

如果你支持开源，请帮忙传播这个项目！

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
