---
title: "Cerebras 晶圆级硬件碾压包括机器学习在内的高性能计算工作负载"
title_en: "Cerebras Wafer Scale Hardware Crushes High Performance Computing Workloads Including Machine Learning And Beyond"
date: 2021-06-30
source: https://newsletter.semianalysis.com/p/cerebras-wafer-scale-hardware-crushes
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# Cerebras 晶圆级硬件碾压包括机器学习在内的高性能计算工作负载

> 原文：[Cerebras Wafer Scale Hardware Crushes High Performance Computing Workloads Including Machine Learning And Beyond](https://newsletter.semianalysis.com/p/cerebras-wafer-scale-hardware-crushes) · SemiAnalysis

Cerebras Systems 及其晶圆级（wafer scale）硬件因其彻底打破常规的路线而备受业界瞩目。当其他 AI 玩家都在打造专用于机器学习的大芯片时，Cerebras 选择了完全不同的扩展路径：把整片晶圆做成一颗芯片。事实证明，这一硬件的通用性出人意料地强，甚至在其他高性能计算应用中也在创造突破性的收益。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1428c59f-8fde-4da7-90f3-d05ffe76cef0_1024x593.png)

这一切源于一个简单的观察：摩尔定律已显著放缓。要获得晶体管数量的巨大提升，唯一的途径就是增加每颗芯片的硅片用量。Cerebras 已经推出第二代产品 Cerebras WSE-2。这颗芯片的尺寸为 215mm x 215mm。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/66e754f8-ad1d-43b2-928f-c06b6d1b63b3_1024x636.png)
![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d6613d1b-cf9e-43bd-943f-0e135f2a9282_1023x294.png)

与目前最大的 GPU——英伟达（Nvidia）A100 相比，Cerebras 拥有巨大优势，尤其是将其片上 40GB 内存带宽与 A100 上尺寸相近的 HBM 内存相比时。Cerebras 的片上互联（fabric）带宽也高得惊人，远超 GPU 之间的互连。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/851c0b2f-a5f4-4026-9578-a2c8a9fde8c6_1024x549.png)

Cerebras 用水冷机箱驯服这头 20KW 的猛兽。作为参照，英伟达 A100 的功耗依配置不同为 250W 至 500W。打造这套散热方案需要倾注大量心血。由于这颗芯片的尺寸和功耗，硅与其他组件的差异化热膨胀等问题成了必须重点解决的难题。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3766cb24-1d73-46cb-b07d-6e88907ebdcf_1024x539.png)

长期以来，半导体制造的裸片（die）尺寸一直受限于光罩极限（reticle limit）。光罩极限为 33x26（mm），这是 ASML 浸没式光刻机在一片晶圆上所能曝光图案的最大尺寸。英伟达最大的芯片停留在 800mm^2 出头的水平，主要原因就是无法超越这一极限。

Cerebras WSE 实际上是把多颗符合光罩极限约束的芯片做在同一片晶圆上。他们不是沿芯片之间的切割道（scribe lines）把芯片切开来，而是开发了一种跨裸片走线（cross die wires）的方法。这些走线与芯片本身分开曝光，使各颗芯片得以互相连接。如此一来，芯片就能突破光罩极限继续扩展。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c90a83a9-5758-495e-8377-fa9a486b375f_1024x517.png)

以传统方式制造芯片，缺陷在所难免。因此，每片晶圆上总有一定数量的芯片必须报废，或者芯片中的部分单元必须被屏蔽。英伟达在其 GPU 上就普遍采用这种做法。屏蔽核心的比例一代比一代高，到当前的 Ampere 世代，约有 12% 的核心被屏蔽。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/38bbd1ca-da9e-45b7-8eb7-35f8890a1b94_1024x664.jpeg)

Cerebras 的应对办法是在每个光罩子芯片（reticle sub-chip）范围内额外增加 2 排核心。芯片内部的互连是一个 2D 网格（mesh），每个核心在垂直和水平方向各自相连，此外还有对角线方向核心之间的额外互连。这使得有缺陷的核心可以被绕开，软件仍能看到一个完整的 2D 网格。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9b8f1846-ab65-46a6-80f1-c44a00b2c045_1024x565.png)

在这个 2D 网格之内，Cerebras 有几个明确的目标。他们希望所有内存都留在片上，而不必等待缓慢的片外内存。唯一的外部连接是通向主机系统的。每个核心具有细粒度并行性，彼此之间不共享任何资源。它们是高能效的通用核心，支持 MIMD，并各自拥有本地内存。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/df8d3e51-a7fc-4369-8caf-ad90105a17d9_1023x583.png)

主要用例是机器学习训练或推理。网络的各层被映射到这片晶圆级芯片的各个区域。每个矩形块对应网络的一层，有趣的是它被称为一个「Colorado」。卷积、矩阵向量乘和矩阵乘法在每层内的核心上完成计算。2D 网格负责网络每层内部以及层与层之间的核心间通信。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/fab326be-bd7f-45ef-89a7-a1615bb84ee0_1024x652.png)

大多数通信一般是沿芯片的 X 或 Y 方向进行，但也有一些通信需要横跨芯片的巨大区域。网格能够从容处理而不发生拥塞。这使得网络中的各层不必连续排布或紧邻彼此。Cerebras 的软件栈负责这些层的布局与布线，同时保持核心与片上网络的高利用率。该软件既可以只把一个网络的少数几层放在单颗芯片上，也可以把整个网络的多个副本分布到整片芯片上以实现数据并行。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e9167829-3b7c-4e8d-98df-079d56eb98d5_1024x716.png)

Cerebras 已有客户在生产环境中运行晶圆级引擎。它们被用于多种工作负载，其中最有趣的之一是 CANDLE。WSE 被用于对药物组合及其对癌症效果的药物反应进行精确模拟，随后从模拟中筛选出最有希望的结果进入实验验证。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9e47b569-ba94-40de-9712-3741c9758f84_1024x573.png)

当前运行在这些芯片上的另一个用例是惯性约束聚变（internal confinement fusion）。它运行在一台大型超级计算机上，其中包含多台互连的 Cerebras WSE。这个巨型模拟的其中一个环节涉及原子与亚原子粒子之间的相互作用。这部分计算被替换为一个在 Cerebras 硬件上运行的大型预训练神经网络。这是一个只用到推理的用例：在模拟的每个时间步上都会被调用。数据从更大的超级计算机流向 Cerebras WSE，后者再回传这些原子与亚原子相互作用的结果。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d733d6de-23f0-422c-94f8-fdad4035bb8a_1024x551.png)

Cerebras 硬件的用途也远不止机器学习。Joule 超级计算机在传统硬件上以 3D 网格运行计算流体力学，但他们在两个层面遇到了扩展瓶颈：受网络带宽限制，性能无法随核心数量扩展；此外，由于缓存未命中而不得不访问内存，核心经常有大量性能被白白浪费，而内存又遭遇严重的带宽瓶颈。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8d9ba5e0-2848-4434-8ef1-2c4054a47bb6_1024x628.png)
![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c5b79f8f-3095-4210-ac96-b68bd15dda86_1024x435.png)

流体力学模型的 3D 网格被映射到 WSE 芯片的 2D 网格上。所需的操作包括邻居交换（neighbor exchange）、向量 AXPY，以及全局向量的点积——后者由局部点积和一次全局 all-reduce 构成。凭借海量的 SRAM 和每个核心相对较高的复杂度，这些操作都能轻松完成。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/28106272-7049-4e2f-b2b4-c8cacda92ad4_1024x537.png)

核心间通信量巨大，但片内网络足够强健，能够低延迟地消化它们。网络的做法是沿着称为「颜色（colors）」的虚拟通道发送消息，而不是发往预定地址。这种硬件级通信使数据能以每时钟周期 1 跳的速度横穿整片芯片。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c1e610e6-48a4-4b80-9395-88370e6cb75b_1024x476.png)

Allreduce 可以做得极快。每个核心把它的标量发给相邻核心；数据到达后，标量被相加再继续前传。芯片边缘的数据沿东西方向向中心汇聚；到达中心后，同样的过程改为南北方向进行。结果被汇总后再沿核心网格广播回去。仅需 1 微秒，这个 allreduce 即可完成。作为参照：一台典型的超级计算机集群完成一次从某个处理器到相邻处理器的单次 MPI 通信，大约就需要这么长时间。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b3c7b639-77de-40ed-9096-d23912b9b904_1024x641.png)

无论数据到达有多迟，计算都能以满带宽进行。路由器从每个相邻核心接收 4 组输入数据；此外，核心可以将自己的输出重新回送输入，从而无需存入 SRAM。核心可以同时运行多个线程：主线程拥有最高优先级，但一旦它在等待数据，其余线程就会继续推进。凭借大量 SRAM 维持的数据局部性和多线程架构，利用率得以保持在极高水平。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d13bb7eb-94ce-4b4e-b75e-205265f51906_1024x383.png)

这些底层硬件优化的成果，是计算流体力学获得 200 倍加速。对比对象是一个同样经过高度优化的大型超级计算机集群。除了速度之外，成本尤其是功耗也拥有巨大优势。这一优势某种意义上不言自明——毕竟被拿来对比的，是一颗单芯片（尽管是晶圆级的）对阵一整个超级计算机集群。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/db43aa60-fbc0-49b2-a20d-73cf4213f259_1024x574.png)

遗憾的是，软件尚未完全跟上。用于编写自定义核（kernel）操作的 beta 版 SDK 将于今年晚些时候推出。该语言将完全针对 WSE 的特定领域。他们会提供数学函数和通信库，有望减轻一些负担。除此之外还有一些辅助的特性和工具，但这仍将是高阶程序员的任务。不过，这是唯一能实现这种规模计算的硬件，对于真正需要这种性能级别的任务而言，这未必构成多高的进入门槛。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9115acd6-cc52-4628-a9fa-43ee6937e28b_1024x580.png)

Cerebras 正把实时计算流体力学宣传为下一个发挥 WSE 威力的工作负载。这很有希望开辟一个全新的用例。

我们期待基于 7nm 的 WSE2 全面铺开。SDK 能否让开发者开拓出更多让 WSE 带来数量级性能提升的工作负载，将是一大看点。AI 是 Cerebras 表现激进、最吸引眼球的领域，但晶圆级计算可能改变的远不止机器学习这一个行业。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

[分享](https://newsletter.semianalysis.com/p/cerebras-wafer-scale-hardware-crushes?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[发表评论](https://newsletter.semianalysis.com/p/cerebras-wafer-scale-hardware-crushes/comments)

*本文最初于 2021 年 6 月 30 日发布于 [SemiAnalysis](https://semianalysis.com/cerebras-wafer-scale-hardware-crushes-high-performance-computing-workloads-including-machine-learning-and-beyond/)。*

*SemiAnalysis 的客户及员工可能持有本文所提及公司的仓位。*
