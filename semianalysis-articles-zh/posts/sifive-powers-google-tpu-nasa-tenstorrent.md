---
title: "SiFive 驱动谷歌 TPU、NASA、Tenstorrent、瑞萨、Microchip 等"
title_en: "SiFive Powers Google TPU, NASA, Tenstorrent, Renesas, Microchip, And More"
subtitle: "RISC-V 正成为非面向用户功能的标准"
date: 2022-09-16
source: https://newsletter.semianalysis.com/p/sifive-powers-google-tpu-nasa-tenstorrent
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# SiFive 驱动谷歌 TPU、NASA、Tenstorrent、瑞萨、Microchip 等

> 原文：[SiFive Powers Google TPU, NASA, Tenstorrent, Renesas, Microchip, And More](https://newsletter.semianalysis.com/p/sifive-powers-google-tpu-nasa-tenstorrent) · SemiAnalysis

**RISC-V 正成为非面向用户功能的标准。**

SiFive 拥有一套 CPU 核心 IP 产品组合，在边缘、物联网和 AI 芯片领域已有扎实斩获，拿下了谷歌（Google）、NASA、[Tenstorrent](https://semianalysis.substack.com/p/tenstorrent-blackhole-grendel-and)、瑞萨（Renesas）、Microchip、Kinara 等多家公司的重要设计导入。许多人以软件生态缺失为由，认为 RISC-V 在数据中心与客户端的普及面临重大阻碍，但在一切不直接暴露给操作系统的场景里，RISC-V 正在迅速成为标准。举例来说，苹果 A15 裸片上分布着十余颗 Arm CPU 核心，承担各类非面向用户的功能。SemiAnalysis 可以确认，在后续硬件世代中，这些核心正被积极转换为 RISC-V。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c9bb56af-aab5-4278-ab3e-a77449e3d339_3908x1725.jpeg)

SiFive 拥有多款核心 IP，其 E、S、U 系列核心取得了程度不等的成功。P 系列虽然[营销话术有些水分](https://twitter.com/dylan522p/status/1415395415000817664?s=20&t=M_DFSQyhBezIV9z8jCIN9w)，但高端 P 系列核心其实不算成功。今天我们想聊聊快速拿下多个设计导入的 X280 核心。虽然我们这些极客对 NASA 下一代高性能航天 CPU（High-Performance Space Flight CPU）情有独钟，但分量最重的赢家是谷歌。在本次 AI HW Summit 上，SiFive 宣布与谷歌在 TPU 上展开合作。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3c3dc85c-4366-4935-aa15-6067b895551e_3080x821.png)

这颗核心虽然是顺序执行（in-order）架构，性能却相当不错。其向量流水线非常宽，完整实现了 RISC-V Vector 1.0 规范。此外还有支持 bfloat、矩阵乘法和量化的扩展，使其可以针对 AI 优化。这颗 CPU 的性能足以在汽车应用中充当应用处理器，或在数据中心应用中充当 hypervisor。[Tenstorrent 的每一个 TenSix 处理器瓦片都包含 X280 CPU](https://semianalysis.substack.com/p/tenstorrent-blackhole-grendel-and)。甚至还有通过 ISO 认证、可以锁步（lockstep）模式运行的车规版本，我们相信它将部署于丰田汽车。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/233163f0-d660-406e-9d4b-438182547088_3013x830.jpeg)

SiFive 能提供 Arm 给不了的东西：灵活性。客户可以直接向向量寄存器堆中添加硬件加速器来修改核心。这可用于把 X280 核心扩展到 DSP、图像信号处理和 AI 等应用。这也正是谷歌合作切入的地方。

谷歌的 TPU 和 [VCU](https://semianalysis.substack.com/p/google-new-custom-silicon-replaces) 本就使用博通（Broadcom）的第三方 ASIC 设计服务。内部团队专注于对其用例真正形成差异化的部分。就 TPU 而言，那就是矩阵乘单元（MXU）和芯片间互连（Inter-Chip Interconnect）。谷歌对 TPU 采取的思路很务实：把重复性工作外包出去。他们不必再从零构建一切，今后将使用 X280 的 VCIX 模式。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8730bcb0-7242-4b11-b6c3-e097b9114c81_3010x840.png)

谷歌将利用 X280 的基础标量与向量能力，实现向量指令的压栈/出栈（push/pop）。这套更丰富的指令集让函数得以重叠（overlay）使用。可编程性大幅改善——现在可以直接执行 Python，也更容易运行条件路由。谷歌既保住了 MXU 的性能，又获得了 RISC-V 核心带来的可编程性和广为人知的 CPU 编程模型。MXU 的高延迟约 100 个周期，而 CPU 可以在区区几个周期内并发执行标量与向量代码。

我们借机问谷歌，为什么要在每一个加速器单元里都塞进一颗 CPU。这对面积的影响不小——每颗 CPU 核心约 0.5mm2。他们的 MXX 单元每单元约 1mm2，意味着 50% 的面积开销。对方的回答很有条理，核心围绕可编程性与灵活性。

> 我们本可以做一个糟糕的一次性定序器（sequencer）来替代，但你愿意用底层汇编来给你的机器编程吗？
>
> —— 谷歌 TPU 架构师、MLPerf 联合创始人 Cliff Young

RISC-V 将吞下非面向用户核心的世界，这一点已经相当清楚。最后把 Jim Keller 演讲中的这张幻灯片留给大家。

> RISC-V 将赢得下一个回合。RISC-V 能用。RISC-V 是开放的。RISC-V 是创新发生之地。RISC-V 的迭代速度将超过其他架构。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/de244f9b-5d4a-43b5-9b5d-ef39706e044c_1741x1375.jpeg)

如果你喜欢我们的内容，请分享！帮忙传出去！

[分享](https://newsletter.semianalysis.com/p/sifive-powers-google-tpu-nasa-tenstorrent?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[团体订阅享 8 折](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

SemiAnalysis 是一家精品半导体研究与咨询公司，专注于半导体供应链——从化学原料到晶圆厂，再到设计 IP 与战略。
