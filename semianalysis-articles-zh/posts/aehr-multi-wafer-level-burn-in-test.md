---
title: "Aehr 面向碳化硅与硅光子学应用的多晶圆级老化测试"
title_en: "Aehr Multi-Wafer Level Burn-in Test for Silicon Carbide and Silicon Photonics Applications"
date: 2021-09-29
source: https://newsletter.semianalysis.com/p/aehr-multi-wafer-level-burn-in-test
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# Aehr 面向碳化硅与硅光子学应用的多晶圆级老化测试

> 原文：[Aehr Multi-Wafer Level Burn-in Test for Silicon Carbide and Silicon Photonics Applications](https://newsletter.semianalysis.com/p/aehr-multi-wafer-level-burn-in-test) · SemiAnalysis

半导体制造几乎是一门让石头思考的炼金术。在制造一颗芯片或器件的过程中，制造、封装和组装的每个环节都有持续的检查。在制造过程中和制造完成后对半导体进行「检查」的领域，活跃着众多公司。

「检查」的一个领域是量测（metrology）：KLA-Tencor $KLAC、Nova Measuring $NVMI、Onto $ONTO 和 Camtek $CAMT 等公司在半导体制造的每个工艺步骤之后测量结果和潜在问题。FormFactor $FORM、日本 Micronics（6871.JP）和 Technoprobe 制造定制探针卡，在晶圆制造工序完成后通过与晶圆的物理接触对其进行测试。Advantest $ATEYY 和泰瑞达（Teradyne）$TER 最为人熟知的是其自动化测试设备（ATE），用于在晶圆切割后测试芯片。Cohu $COHU 的业务主要在器件搬运（handler）领域，但也涉及测试和连接器。以上是这些公司经营的主要领域，不过它们都在不同程度上越出了这些框框。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6f6b4108-054a-42a8-8737-6dbfd90342cb_1024x555.png)

碳化硅（SiC）器件的制造和封装成本极高。在电动汽车、充电器和能源基础设施等终端市场，失效将是灾难性的。这些器件在常温下可能工作得完全正常，但在更极端的环境中，故障和异常就会显现出来。由于需要在极端温度下长时间工作的认证要求，测试环节没有任何偷工减料的余地。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ab898509-550a-4683-97e6-ca533fb34db2_1024x574.png)

对每个器件的单次测试可能持续两到四天，而测试成千上万个器件所需的场地空间是个天文数字。在多裸片模块中，一颗坏裸片会导致许多好裸片一起失效。SiC 存在许多与脆弱/易碎晶体结构相关的缺陷、掺杂相关缺陷以及沟槽失效。其良率相对其他半导体尤其低，约占最终器件成本的 30%。浴缸曲线同样适用于半导体：失效率在初期非常高，随后呈指数下降至稳态；在经历很长一段低失效率期后，最终又会重新上升。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/df7df77c-9abd-4174-a1e6-2fcbf35f4da1_1024x576.png)

Aehr 所处的领域颇为有趣，类似于 Advantest、泰瑞达和 Cascade Microtech（FormFactor 子公司）的某些测试相关细分市场。不过 Aehr 的方法完全是新颖的。他们不是制造在器件和模块层面测试的工具，而是在晶圆层面进行测试。这样可以减少不良器件流入封装环节，并缩短完整的测试周期。周期时间是 SiC 器件生产的主要制约因素，Aehr 缩短周期时间的解决方案前景可期。安森美半导体（On Semiconductor）$ON 是 Aehr 在 SiC 领域的第一个标志性客户，但他们也在与其他客户接触。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/62afaaa6-ea4d-4b0d-b08c-116b71b77b60_1024x573.png)

Aehr 开发了用于碳化硅晶圆老化（burn-in）测试的 FOX-XP 设备。每片晶圆可容纳多达一千颗 SiC 器件。FOX-XP 一次可测试 18 片晶圆。FOX-XP 在腔体内完成测试，该腔体充当高度受控的极端温度环境。可以把它想象成一台烤箱，只不过它还能耗散超过 18 kW 的功率。FOX-XP 设备售价约 $2.5M，必须与 WaferPak Contactor 配套使用。

WaferPak 类似于探针卡，但它还承载晶圆。WaferPak 被视为耗材，价格约 $1.5M。耗材是用完即换、产生持续性营收的产品，而不是像设备那样的一次性大额付款。它拥有 2048 个 I/O 引脚和 DPS 通道，每个通道都具备远程电压和接地侦测。每个通道可在 1024 个电压等级间切换，最高 29V，或输出高达 2A 的电流。这在细粒度测试和控制上不及高端探针卡，但能在高达 150 摄氏度的温度范围内进行一些基础测试。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/716f5a76-69b2-4c19-b0bd-d9f1c7aafbf2_1024x574.png)

最后一块拼图是自动化的 FOX-XP WaferPak Aligner（对准器），负责在 FOUP 或晶圆花篮与 WaferPak Contactor 之间装卸晶圆。WaferPak Aligner 的价格不到 $1M。整套系统自动装卸晶圆、连续测试数天并识别失效器件。采用晶圆级测试极大地缩减了 SiC 器件测试所占用的场地。不需要大量机器日复一日地并行测试众多单个器件，一台 FOX-XP 就能测试 18 片每片包含众多器件的晶圆。这大幅提升了吞吐量：仅用一台设备就能对超过 10,000 颗单个器件进行深度老化测试。成本也随之降低，因为不良器件可以在封装前就被剔除分级。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9433aeab-7d15-4c37-9a98-6c62f8ee5332_1024x575.png)

转向晶圆级老化测试的不止碳化硅半导体，硅光子学也在采纳这一做法。英特尔（Intel）是 Aehr 在光子学应用上的标志性客户，但 Aehr 表示在该领域还有另外 4 家客户。在这一应用中，老化测试针对的是激光器。英特尔先制造磷化铟（InP）激光器，再将其键合到每颗光子集成电路（PIC）上。英特尔的 400G 收发器将在一颗 PIC 上集成 4 颗这样的激光器，800G 将集成 8 颗。

每颗激光器的光束穿过 PIC，光流被编码上 100 gigabits 的数据。这些激光器必须具备极高的精度，才能可靠无误地传输数据。激光器工作状态的任何变化都会打乱这套精密调校的系统。激光器存在一种几乎与可靠性浴缸曲线类似的现象：在最初使用阶段存在衰减，输出光的波长会发生漂移；随后激光器在其使用寿命内保持稳定。英特尔和其他光子学制造商会在这段衰减期内对激光器进行老化。一旦波长停止漂移，他们就能识别失效、校准系统。下一步便是将 PIC/激光器封装到最终的收发器模块上。真正的引爆点在于，硅光子学的出货量正在 400G、800G 乃至最终的[共封装光子学](https://semianalysis.com/intels-trojan-horse-into-the-foundry-business-co-packaged-silicon-photonics-is-intels-path-forward-for-idm-2-0/)上爆发。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e41fd19b-188a-464e-bd53-a12ba61ee223_600x454.jpeg)

光子学应用的物理系统略有不同。每台 FOX-XP 可容纳 9 个 FOX Die-Pack Carrier（裸片承载器）。每个承载器最多可容纳 1024 颗裸片，每颗裸片可获得 2 W 的功率用于激光器老化，总计 18 kW。这里还有移动设备和传感器角度的故事。VCSEL 激光器可用于激光雷达（LiDAR）等市场的光学传感，这些传感器可应用于从汽车到 iPad 和 AR 的激光雷达。此外，还有可能用于[Rockley Photonics](https://semianalysis.substack.com/p/rockley-photonics-will-revolutionize)等健康应用中激光器的老化。

几十年来 Aehr 一直规模不大，但现在正进入一个拐点。随着向 400G、800G 和共封装光子学的迁移，激光器的数量和质量标准将爆炸式增长。英特尔的硅光子学出货量将飙升，这很可能意味着更多的 Aehr 系统。如果他们能说服尚处襁褓期的 SiC 行业把晶圆级老化测试纳入测试流程，随着出货量开始爆发，他们将斩获巨大的订单。当前估值已隐含 Aehr 将赢得更多订单并在现有客户上持续增长。我们无法确定 Aehr 能否拿下这些订单，但它绝对是一家值得留意的公司。最大的几家 SiC 玩家尚未做出承诺，可一旦他们点头，天花板将不可限量。对大多数大批量半导体而言，晶圆级老化测试过于昂贵，但化合物半导体和光子学彻底颠覆了这一范式。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

[分享](https://newsletter.semianalysis.com/p/aehr-multi-wafer-level-burn-in-test?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[发表评论](https://newsletter.semianalysis.com/p/aehr-multi-wafer-level-burn-in-test/comments)

*本文最初于 2021 年 9 月 29 日发布于 [SemiAnalysis](https://semianalysis.com/aehr-multi-wafer-level-burn-in-test-for-silicon-carbide-and-silicon-photonics-applications/)。*

*SemiAnalysis 的客户及员工可能持有本文所提及公司的仓位。*
