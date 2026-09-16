---
title: "高通 MWC 2021——网络基础设施与边缘 5G 火力全开 | FSM200、DU X100 加速卡与一系列新特性"
title_en: "Qualcomm MWC 2021 - Network Infrastructure And Edge 5G Get Supercharged | FSM200, DU X100 Accelerator, And Range Of Features"
date: 2021-06-29
source: https://newsletter.semianalysis.com/p/qualcomm-mwc-2021-network-infrastructure
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 高通 MWC 2021——网络基础设施与边缘 5G 火力全开 | FSM200、DU X100 加速卡与一系列新特性

> 原文：[Qualcomm MWC 2021 - Network Infrastructure And Edge 5G Get Supercharged | FSM200, DU X100 Accelerator, And Range Of Features](https://newsletter.semianalysis.com/p/qualcomm-mwc-2021-network-infrastructure) · SemiAnalysis

尽管缺乏大型消费电子方面的发布，高通（Qualcomm）在 MWC 2021 上的表现依然可圈可点。他们展示了两款全新硬件平台，以及正在推向 5G 基础设施与边缘市场的一大批创新特性。这些方案的共同特点是功耗效率极高、成本相对低廉，却能大幅提升网络效率。虚拟化、可互操作、模块化，是高通此次发布与技术展示的主题。他们正在云原生电信基础设施的建设上引领方向。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/aa37b778-b165-46e9-8188-32a68dbac6ba_1024x568.png)

高通发布了 FSM200xx，这是其第二代小基站（small cell）解决方案。它采用三星（Samsung）4nm LPP 制程工艺制造，裸片（die）面积为上一代 FSM100xx 的一半。这款新品是市场上唯一全面支持 3GPP Release 16 全部特性的产品。此外，频谱支持较上代进一步扩充，新增 n259（41 GHz）、n258（26 GHz）毫米波频段和 FDD 频段。FSN200 提供 oRAN/vRAN 能力，实现最大灵活性。

FSM200 平台在毫米波上支持最高 8 Gbps 吞吐和 1 GHz 带宽，并支持跨 FDD 与 TDD 聚合 200 MHz 的 Sub-6 GHz 频谱，达到最高 4 Gbps 的数据速率。没有任何演示或官方说法明确指出这些是同时达到的。SemiAnalysis 认为该平台存在 10Gbps 的总网络带宽上限。

FSM 平台提供一项能大幅降低部署成本的独特功能：以太网供电（PoE）。PoE 能力允许从单一来源同时取电和回传，简化部署并降低成本。凭借平台的低成本和低功耗，它可以在室内和室外高密度部署。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/162e5e7c-d496-4eb6-8551-a62f1b6dbefc_1024x431.png)

FSM200 平台让运营商可以通过增加基站轻松扩展网络、增加容量和带宽，而 5G 分布式单元 X100 加速卡则简化了 vRAN/oRAN 的部署。它定位为一款在线（inline）加速器，负责高容量部署所需的解调、波束赋形、信道编码和 Massive MIMO 计算。

vRAN/oRAN 长期以来受制于标准 CPU 或错配的加速能力。RAN 协议栈的物理层以实时函数和复杂信号处理算法为特征。没有足够的加速，迁移到 vRAN/oRAN 平台就会损失性能或增加时延。

于是，业界一拥而上，用各种 FPGA 和 ASIC 来卸载各类 RAN 功能。早期的加速器主要以后视（look-aside）模式使用，即加速器只被主处理器调用。这对前向纠错（FEC）是行得通的，大多数基于 FPGA 的方案也正是部署在这一功能上。随着 5G 基础设施走向成熟，FPGA 在 5G 中的用量也随之等比例下降。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3bc6f0b2-2fbf-4ed8-b9ed-71040e7ffc5a_1000x406.png)

在线加速器则同时与主处理器和 RAN 直接交互。英伟达（Nvidia）也在尝试把 GPU 用作 5G 部署中的在线加速器。与高通更模块化、与整个生态更可互操作的方案相比，他们的推进方式给人一种方枘圆凿之感。我们已向英伟达发出问询以获取更多信息，因为他们关于 Aerial 的新闻稿留下了太多未解之问。高通的目标是让 DU X100 加速卡直接插入现有设计以增强既有部署能力，或者让电信合作伙伴购买后将其与通用低成本 CPU 平台搭配使用。

高通 5G DU X100 是一款 PCIe 在线加速卡，同时支持 Sub-6 GHz 和毫米波基带。它通过为 O-RAN 前传（fronthaul）和 5G NR Layer 1 High（L1 High）处理提供交钥匙方案来简化 5G 部署、即插即用。高通的开放路线深受运营商和 OEM 喜爱，因为它不会把用户硬塞进任何单一解决方案。他们可以针对具体部署场景选择硬件，而不是被迫接受一刀切的硬件平台。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/69c6b6b2-29c4-4b01-ae11-12bba2afd414_634x405.jpeg)

高通致力于在每一个 3GPP 大版本上都保持领先。其终端侧调制解调器和基础设施硬件都在每个版本上命中最新的特性集。除了今天发布的基础设施硬件，他们还演示了未来 3GPP Release 标准的原型。他们率先开拓的第一个（也是众多特性之一）是 5G NR Light（Red Gap）。在 Release 17 中，sub 7GHz 频段的带宽可以下探到 20MHz；Release 18 将进一步降到 5MHz。带宽下探可大幅降低发射功率并缓解网络拥塞。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/57495a89-9aed-415d-b758-3a58077d09c1_1023x573.png)

5G NR Light 的引入将使接入 5G 网络的设备数量暴增：供应链传感器、资产追踪器、可穿戴设备、智能视频摄像头、各类传感器等等。除了让设备更小型化之外，即将到来的 3GPP 版本还将通过 Sidelink 支持中继（relay）。Sidelink 允许网络中的设备彼此直接通信。一个潜在用例是：货物上的供应链传感器连接到卡车内的中继节点，从而大幅降低功耗并延伸覆盖范围；当货物进入仓库或工厂时，再接入室内密度高得多的本地 5G 网络。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a7e95e3d-ff53-4ed7-ae99-9b2e8b343574_1024x571.png)

Sidelink 在其他方面同样大有用武之地。许多自动驾驶应用会希望使用高通的先进调制解调器进行 V2X 通信。这些调制解调器既能照常与公众网络通信，也能与其他 5G 设备直接通信。当车辆之间彼此共享地图与定位数据时，这些数据有助于构建更高精度的 3D 地图。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d499c777-b9a4-4792-8616-fec898ea3129_1024x575.png)

V2X 的美妙之处在于它运行在专用的 5.9GHz 频段上，无需任何电信订阅。这项技术已开始在中国部署，明年将在美国落地。凭借 Sidelink 的加持，行人与车辆安全可以得到极大提升。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/76bfaf6c-c370-4142-91a8-1612fe17ff5d_1024x573.png)

除了与其他设备通信，自动驾驶车辆还希望利用 5G 实现高精度定位。定位可以采用标准算法，利用往返时间（round trip time）和到达角（angle of arrival）来估计 3D 位置。这通常能达到约 2 米的精度，已远优于消费者可用的任何卫星 GPS 网络。

更进一步，高通利用机器学习，将 5G 定位数据与 GNSS 卫星定位及陀螺仪数据融合成传感器融合方案。神经网络如今可以把位置确定到 1 厘米以内。这项技术在室内、停车楼、甚至隧道中依然有效——而 GPS 卫星定位在这些场景下往往精度大打折扣。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1a6c4445-3a7c-4df8-9cdb-8fd59d1d29e3_1024x716.png)

高通正凭借 FSM200 等产品及其嵌入式芯片/调制解调器把 5G 推进工厂。Sidelink 和 5G 定位等特性尤其重要：它们让设备之间可以互相通信，让机器人能精确定位工厂内各种物件的准确位置。高通设想将其扩展现实（XR）技术引入工厂，让工人随时掌握关键信息，从而对任何故障或宕机快速响应。这些 XR 设备还能在工人作业时调出其正注视设备的相关信息，辅助工作。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/fe2611e3-a6ff-4127-b4bb-fcf68fd248bf_1024x577.png)

此外，他们还抢在所有人之前，为智能工厂再推出两项实用特性。时间敏感网络（TSN）可以让摄像头、机器人、执行器及其他机械或数据采集元件等各类设备实现亚微秒级同步。超可靠通信（URC）则融合 Sidelink 与多个发送接收点（TRP），绕开任何链路中断或信号干扰。这些特性使无线以太网能够支撑微秒级同步的时间敏感网络。借助 Sidelink、TSN、URC 和 5G 定位，机器人如今可以可靠地取放物件，推进制造流程。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/90324e3e-7cdb-4c74-9990-3362473f03ba_1024x572.png)

高通的工作不止步于行业标准。他们正尝试用机器学习方法重构整个协议栈。其中一些已成功演示并正在产品化。例如，最新一代毫米波波束赋形利用机器学习来提升在线时长并降低时延波动。神经网络通过在设备移动之前预判是否以及向何处进行波束赋形，来驱动更高质量的服务。神经网络的应用领域还包括信道状态信息反馈，以及定位与感知。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6ee4e78c-d664-47d1-8724-14b5bd981f42_1024x568.png)

高通还在用机器学习辅助网络规划与部署。他们的产品线覆盖无线回传基础设施、小基站和不同类型的中继器。他们利用 Google Maps、OpenStreetMap 等 GIS 公开数据，将数据送入网络以绘制建筑物、建材，以及标牌、电线、植被等物体。这些地图数据再与交通数据结合，从带宽、时延、密度和成本出发优化网络部署。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/98dd941c-f5f0-4fcd-93b8-203e7a575887_1024x567.png)

高通还推出了毫米波中继器。他们评估了 3 种不同形态。高通的构想是不必为每个站点单独铺设网络，而是用少数基站承担回传：这些基站可以直接服务网络中的设备，也可以连接各类中继器来增强信号。这能大幅降低 5G 毫米波网络的铺网成本。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/24c6d33a-5340-405b-b884-ebdeb72a6751_1024x567.png)

高通的 Boundless XR 演示是本次最令人印象深刻的技术展示之一。他们演示了 3 名用户同时在 VR 中交互，时延极低。这场演示仅使用单个毫米波基站、仅占用 100MHz 频谱，搭配一套基于英伟达 GPU 的边缘服务器系统。其中两名用户在 VR 聊天中互动，第三名用户游玩 PC 级 VR 游戏。所有用户都稳定保持 90FPS、每眼完整 2160x2160 分辨率。整套 5G 系统给「动作到渲染到光子」（motion to render to photon）时延指标增加的时延不到 20ms。高通表示，下一个 3GPP Release 将支持在单个小基站上、使用同样的 100MHz 频谱容纳超过 12 名用户，同时维持同样的低时延。我们期待这项技术扩展到城市级增强现实应用的那一天。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8c0fbe52-5b3f-4558-8a43-399e2f4351ba_1023x573.png)

总而言之，尽管在消费硬件上乏善可陈，今年的 MWC 发布可能是高通迄今最好的一届。他们展示了大量基础设施演示，并开始推出构建这些网络的能力。高通没有停留在举手宣称自己拥有最好的调制解调器，而是把其快速创新的引擎开进了网络基础设施。无论是凭借快速的硬件迭代、机器学习实力，还是射频前端功底，高通都已摆好架势，要在 5G 基础设施以及工厂、供应链、汽车等新兴 5G 应用中斩获大片份额！

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

[分享](https://newsletter.semianalysis.com/p/qualcomm-mwc-2021-network-infrastructure?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[发表评论](https://newsletter.semianalysis.com/p/qualcomm-mwc-2021-network-infrastructure/comments)

*本文最初于 2021 年 6 月 29 日发布于 [SemiAnalysis](https://semianalysis.com/qualcomm-mwc-2021-network-infrastructure-and-edge-5g-get-supercharged-fsm200-du-x100-accelerator-and-range-of-features/)。*

*SemiAnalysis 的客户及员工可能持有本文所提及公司的仓位。*
