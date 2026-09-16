---
title: "800VDC 革命内幕——第一部分"
title_en: "Inside the 800VDC Revolution – Part 1"
subtitle: "四阶段 800VDC 转型、电力机柜经济学、固态变压器（SST）、每 MW 设备价值量测算与供应商影响"
date: 2026-05-26
source: https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part
crawled: 2026-09-15
authors: ["Nicolas Bontigui", "Jeremie Eliahou Ontiveros", "Konrad Wang", "Aran Industries", "Derek Yin", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 800VDC 革命内幕——第一部分

> 原文：[Inside the 800VDC Revolution – Part 1](https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**四阶段 800VDC 转型、电力机柜经济学、固态变压器（SST）、每 MW 设备价值量测算与供应商影响**

![](https://substack-post-media.s3.amazonaws.com/public/images/afd57882-4edd-4d08-9ee9-923b94c43063_1672x941.png)

*我们要感谢 [DG Matrix](https://www.dgmatrix.com/)、[Novos Power](https://www.novospower.com/) 和 [Aran Industries](https://aranind.com/) 在本次深度解析撰写过程中提供的贡献与洞见。*

## **导言：欢迎登上电力链过山车**

2026 年上半年的各大行业会议上，我们的研究团队反复走过同一幕场景：一个展位前围着十几个人，人人侧耳倾听又一位数据中心设备"救世主"布道 800VDC 的福音。每次的说辞都一样：800VDC 即将改变数据中心的电气基础设施。

每一次架构变革起初看起来都显得过头。运营者们花了几十年把水和泄漏挡在数据机房之外，随后 GPU 的热密度却让冷却液直接贴着宝贵的硅片流动变得不可避免。但这些变革终究都发生了，因为物理规律和计算的经济学从不让步。下一个就是 800VDC，而且逻辑如出一辙：真正要紧的是每瓦特 token 数。

![](https://substack-post-media.s3.amazonaws.com/public/images/afb0968c-ec14-46c2-ad51-3b9165c49b52_1363x807.png)

来源：Nvidia、InferenceX

随着 GPU 集群密度越来越高——Kyber Ultra 单机柜已逼近 660kW——物理规律开始崩坏。电阻损耗随电流的平方增长，在这种功率水平下，铜的重量与热包络已经超出一个机柜所能容纳的极限。转向 800VDC 可以消除多个变换级、降低电阻损耗，并把设施级功耗削减约 5%。在 1GW 的 IT 负载下，这意味着超过 50MW 的持续节省——每年数千万美元的电费，或是等量解锁的新算力。对各位"推理之王"的拥护者来说：800VDC 是一场被物理强制、由系统经济学驱动的转型。

我们一直在通过 [InferenceX](https://inferencex.semianalysis.com/) 和 [Industrials Models](https://semianalysis.com/industrials-model/) 跟踪这场转型，它们提供了自下而上的视角，看清效率增益在哪里兑现、哪些设备品类在吸收这场颠覆。[Industrials Model](https://semianalysis.com/industrials-model/) 包含一个专门的 800VDC 模块，从各个加速器架构自下而上构建出 800VDC 渗透率、MW 采用量以及电力边柜（power sidecar）、固态变压器（SST）等设备市场规模的俯视全景。

![](https://substack-post-media.s3.amazonaws.com/public/images/63ebd75b-d4b1-40d4-8f0a-69cb97a6c04c_1890x1377.png)

[来源：SemiAnalysis Industrials Model](https://semianalysis.com/industrials-model/)

本次深度解析将逐阶段追踪这场转型：从边柜（sidecar）改造，到设施级直流配电，再到 SST 终局。针对每个阶段，我们分析物料清单（BoM），梳理每 MW 设备价值量的变化——什么得以幸存、什么被重新设计、什么被彻底淘汰。

800VDC 革命将显著改变某些供应商的营收轨迹。一年多来，我们一直在 [Industrials Model——它估算 20 多种数据中心设计的 BoM、拆解为 70 多类设备，并给出对 500 多家供应商的影响](https://semianalysis.com/industrials-model/)——中跟踪赢家与输家。它建立在我们业界领先的 [Datacenter Model](https://semianalysis.com/datacenter-industry-model/) 之上，后者按季度预测 6000 多座数据中心的 MW 需求，并预判设计变化。

这使我们得以抢在所有人之前，既成功点出真正的赢家，也点出被市场误判为输家的公司。如果你想知道 UPS 系统在即将到来的 800VDC 配电中还有没有位置、SST 的市场机会有多大、或者哪些供应商正在引领这场转型，请继续读下去。

![](https://substack-post-media.s3.amazonaws.com/public/images/cc242d80-4fda-4460-ae14-822da54d6dd3_1890x1267.png)

[来源：SemiAnalysis Industrials Model](https://semianalysis.com/industrials-model/)

***本篇为 800VDC 革命系列第一部分，覆盖数据中心布局与设备影响。第二部分将聚焦电力电子及其底层的半导体革命。***

## **理解基础：什么是 800VDC，它为何不可避免**

最简单地说，本文语境下的 800VDC 是指以约 800 伏直流电把电力配送穿过数据机房或机柜列并送入机柜，再在计算设备附近降压。800 这个数字并非随意选取：这一电压高到足以实质性降低电流（从而降低铜损与热负担），同时在许多司法辖区仍处于"低压直流"的宽泛监管与产品安全分类之内。作为参照，欧盟低电压指令（Low Voltage Directive）适用范围的相关规则所引用的直流设备额定值最高到 1,500 V DC（交流最高 1,000 V）。

当前的数据中心电气架构普遍在设施级依赖交流配电。今天的数据中心使用 415V 或 480V 三相交流电，拓扑依赖传统 UPS 架构，然后在机柜内配送 48-54V 直流。

这在今天的机柜功率水平下可行，但随着未来两年机柜密度逼近 ~600 kW+，这套体系将开始失效，原因有以下几点：

- **48–54 V 下铜变得无法管理。** 1 MW 机柜在 48–54 VDC 下需要约 200 kg 铜母排。放大到 1 GW 规模，那就是数百吨铜——对成本、重量、安装复杂度和走线空间都是重击。

![](https://substack-post-media.s3.amazonaws.com/public/images/888d7c8f-07ee-4e2e-a3fd-5d3cd58e0bbc_756x416.png)

来源：Microsoft

- **电源架挤占计算空间。** 今天的 NVL72 机柜已经用掉多达 8 个电源架（power shelf）。在 Kyber 级机柜功率下，48–54V 方案需要约 64U 等效的电源硬件——实际上就是整整一个机柜——没有留下任何空间给计算。
- **电流成为真正的限制因素。** 以 48–54 V 输送 600 kW 意味着约 12,500A 的电流。在 800 V 下，电流降至约 750 A（约减少 16.7 倍），导线/母排得以显著缩小，热应力也大幅降低。若导线电阻保持不变，I²R 损耗下降约 278 倍，因此实践中可以缩小铜截面，用损耗裕度"换取"尺寸与重量的削减。
- **变换损耗层层叠加，损害可靠性。** 层层堆叠的 AC-DC 与 DC-DC 变换级降低端到端效率、增加发热并引入故障点，推高冷却负载、停机风险与维护成本。

归根结底，800VDC 是 2,300W TDP 芯片和 600kW 机柜的物理使能者，而这些 600kW 机柜正是追求密度的直接后果，因为密度正是把每 token 成本打下来的关键。每 token 成本取决于你能在全 NVLink 带宽下构建多大的纵向扩展（scale-up）域：更大的域意味着更宽的专家并行（EP）/张量并行（TP）、MoE 路由走 NVLink 而非横向扩展网络，以及解码阶段更少的串行化。正如我们在 [Vera Rubin 深度解析](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution)和 [GTC 2026](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands) 两篇文章中阐述的，Nvidia 的设计规则是把算力排布得足够紧凑，让铜能在机柜内触达一切。Reiner Pope 几周前在我们朋友 Dwarkesh 的播客中把这层意思讲得很清楚：单个机柜限定了你所能构建的专家层规模，因为 all-to-all 通信一旦越过机柜边界，就会落到一条比 NVLink 慢约八倍的横向扩展网络上。

更大的纵向扩展域意味着更高密度的机柜，更高密度的机柜意味着 600kW 功耗包络，而 800VDC 正是让这些包络成为可能的所在。

![](https://substack-post-media.s3.amazonaws.com/public/images/e57debbb-8027-4f5a-8825-9812ecaf7d98_454x196.png)

[来源：SemiAnalysis AI Networking Model](https://semianalysis.com/ai-networking-model/)

## **HVDC 转型的四个篇章**

迈向 800VDC 是一场复杂的蜕变：它改写整个电气架构，引入新的安全标准，需要新的监管框架，而最重要的是，迫使运营者就何时弃用存量交流配电做出截然不同的战略选择。

![](https://substack-post-media.s3.amazonaws.com/public/images/ba1a5d07-d348-4dbc-acdb-bb2ef8c27688_1386x773.jpeg)

来源：SemiAnalysis

我们把 800VDC 转型划分为四个不同的阶段。第 1、2 阶段始于 2026 年末/2027 年初，通过电力机柜在机柜层面把存量交流配电改造为 800VDC。第 1 阶段是先行者阶段，由愿意为前瞻布局和效率收益买单的超大规模厂商驱动。第 2 阶段在 800VDC 原生系统开始规模出货时启动。第 3 阶段改写电气架构本身，把 800VDC 配电推向整个设施。第 4 阶段是终态，围绕一批有望让今天电气栈大部分作废的新设备构建。

![](https://substack-post-media.s3.amazonaws.com/public/images/2b3214ee-66d2-4c17-87c7-1ae1b2ebd33a_783x581.png)

[来源：SemiAnalysis Industrials Model](https://semianalysis.com/industrials-model/)

由此得到 800VDC 的渐进式采用曲线。我们预计到 2030 年，由 800VDC 供电的增量总容量将达到约 39GW。在第 1、2 阶段，全部可服务容量都由边柜承载，因为底层设施仍是交流配电，变换发生在电力机柜。2029 年结构出现拐点：设施级 HVDC 配电变得可行，首批 800VDC 原生站点上线，变换级从机柜上移到 SST 或中压整流器。

![](https://substack-post-media.s3.amazonaws.com/public/images/06965a33-fc34-4e70-9ca4-ec5107ff8c84_1890x1377.png)

[来源：SemiAnalysis Industrials Model](https://semianalysis.com/industrials-model/)

在深入数据中心布局如何变化之前，我们建议读者回顾[我们的数据中心解剖系列第 1 部分](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical)，其中解释了数据中心电气设备背后的许多核心概念。

### **第 1 阶段（2026/2027）：白区改造**

![](https://substack-post-media.s3.amazonaws.com/public/images/9428195a-e4da-4064-9dce-82254fc383ba_1386x520.png)

[来源：SemiAnalysis Industrials Model](https://semianalysis.com/industrials-model/)

HVDC 之旅主要由两家运营者开启：Google 和 Meta。两家都在 OCP（开放计算项目）工作组推动其 800VDC 架构超过 18 个月，最引人注目的是 Mt. Diablo 参考设计——2024 年 10 月首次宣布，2025 年 5 月作为开放规范发布。两家都不是被迫转型，而是要在即将到来的切换中抢占领先身位，并赶在市场其他人被迫追赶之前，从既有电力链中榨出每一兆瓦、每一个百分点的效率。

这一点很关键，因为 800VDC 尚不是硬性要求。2026 年末和 2027 年量产爬坡的芯片世代（如 Vera Rubin NVL72）机柜密度上限为 180-220kW，三相交流仍能胜任这一密度，不会触及导线截面或配电损耗的物理极限。因此第 1 阶段是自愿的前瞻布局，而非对硬件约束的被动应对。

这一初始阶段开启了"白区改造"（White Space Retrofit）时代。新的 HVDC 硬件——主要是一台称为 HVDC 电力机柜的列级柜体——叠加在现有白区基础设施之上，而非取而代之。数据中心的电气骨干保持原样：同样的变压器、同样的 UPS、同样的开关柜、同样的 ATS。

#### **HVDC 电力机柜的电力流概览**

在设施层面，中压交流进入灰区，经变压器降压为 415V 或 480V 三相交流，馈入执行双变换（AC-DC-AC）的 UPS，输出 415V 交流。交流电随后经母线槽配送穿过数据机房。到这里为止，都是[我们此前文章中详细覆盖过的](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical)传统电力流。

变化发生在靠近 IT 机柜处。交流馈电不再把 415V 直接送入机柜内电源单元，而是终结于一台名为 HVDC 电力机柜的独立 42U 柜体，部署在机柜列级别。

![](https://substack-post-media.s3.amazonaws.com/public/images/b13f6b9c-67c4-472c-b235-268f356b708d_746x505.png)

来源：SemiAnalysis

该机柜从顶部母线槽接收交流，通过线缆向相邻的 IT 机柜输出 800VDC。其内部完成三项工作：把 415V 交流整流为 800VDC、供停电期间渡越（ride-through）的 BBU 模块，以及（可选）在 GPU 负载尖峰期间提供暂态缓冲的电容器架。

#### **简而言之：电力机柜**

值得更细致地审视支撑 800VDC 转型第 1、2 阶段的基础构件：解耦式电力机柜。这是一台专用机柜，把 AC-DC 整流、储能（BBU 和/或电容组）与电源管理整合进单一单元，让计算机柜得以完全专用于 GPU、网络与散热。Microsoft 的 Mt Diablo 项目首创了这一概念[；由 Google、Meta 和 Microsoft 共同撰写的 OCP Diablo 400 规范](https://www.opencompute.org/documents/ocp-specification-diablo-400-v0p5p2-2025-05-30-pdf)将其标准化。

**边柜式电力机柜中常见的关键部件：**

![](https://substack-post-media.s3.amazonaws.com/public/images/6be0c5cc-7516-4959-a99d-6e86bba0340a_753x370.png)

来源：Rittal

![](https://substack-post-media.s3.amazonaws.com/public/images/187fa976-8d37-4386-beff-0b2fd1d02e6f_2944x1757.png)

来源：SemiAnalysis

但边柜概念并非一蹴而就，它经过了好几代 OCP 机柜与电源规范的演化。早期迭代（12V 的 ORv2、48V 的 ORv3，以及把单机柜 48V 设计推到约 190 kW 的 HPR V1/V2 变体——采用液冷母排和升级的 72 kW 电源架）已在[我们的数据中心解剖系列](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical)中覆盖。这里我们聚焦与 800VDC 直接相关的版本：发生电压变换的解耦式边柜设计。

![](https://substack-post-media.s3.amazonaws.com/public/images/c2c026fa-22b4-4d72-a550-cbbba77f7f4d_1386x1383.png)

来源：OCP

#### **ORv3 HPR V3：解耦的门槛（50V 边柜，最高 300 kW）**

HPR V3 是电力与计算真正分属不同机柜的起点，也是"边柜"概念的发端。PSU 与 BBU 架移入一台专用的 50VDC 侧挂电力机柜，通过两柜顶部与底部的水平母排与 IT 机柜相连。两者均保持 ORv3 HPR 标准形态。功率容量上限为 300 kW，受限因素是水平交叉连接和电力机柜内部的风冷垂直母排。

![](https://substack-post-media.s3.amazonaws.com/public/images/af3f744a-495f-41a7-9407-01c8fbb6d814_2079x1186.jpeg)

来源：OCP

其洞见在于：把电源变换硬件放进一台为电力优化、具备相应冷却、安全与可维护性的机柜，而不是塞进一台为计算优化的机柜。V3 电力机柜可以独立维护，缩小了电力侧故障的"爆炸半径"。但 V3 仍以 50VDC 配电，这意味着母排电流依然很高（300 kW 下为 6,000A），交叉连接成为瓶颈。

![](https://substack-post-media.s3.amazonaws.com/public/images/1c9fbf5b-dec2-4c3a-8a59-246c47722fcf_1386x865.png)

来源：SemiAnalysis

这一状况延续至今。即便是 VR NVL72 机柜，当由 800VDC（Nvidia 规范）或 ±400VDC（OCP 规范）的 HVDC 电力机柜馈电时，机柜内部仍通过 50V 母排配电。机柜内的 DC-DC 电源架在电力到达计算托盘之前，把高压直流降至 50VDC。在最末端，GPU 板上的 VRM 再把 50V 变换到 1V 以下。

我们在 [VR NVL72 元器件 BoM 与功率预算模型](https://semianalysis.com/vr-nvl72-model/)中提供了更详细的供电与架构细节。

#### **ORv3 HPR V4：±400VDC 的 HVDC 边柜（最高 800 kW）**

HPR V4 是把 OCP HPR 谱系接入 HVDC 时代的版本。它做了两项关键改变：电压从 50VDC 升至 +/-400VDC（总计 800V），基于母排的交叉连接被分立电力线缆取代。

- **架构**：PSU 与 BBU 架移入 +/-400VDC 侧挂电力机柜，机柜同时容纳交流输入与直流输出 PDU
- **电力输送**：电力机柜通过 16 条 50 kW HVDC 线缆（取代 V3 的水平母排）连接 IT 机柜，每条承载 +/-400VDC
- **功率容量**：最高 800 kW。若基于电容器的储能（CBU）占据一半 BBU 槽位，有效容量降至约 400 kW
- **交流输入**：来自分接箱（tap box）的 200A 单导线
- **形态**：与 V3 相同的 ORv3 HPR 机柜尺寸
- **为何用线缆而非母排**：在 V4 所面向的功率水平（400-800 kW）下，V3 的水平母排交叉连接会成为电流瓶颈。改用分立线缆后，每条线缆可以独立走线、独立熔断、独立管理，并消除了作为热与机械约束的单点母排

V4 实际上代表了 HVDC 边柜设计的"前 Diablo"状态，主要由 Meta 的机柜与电源团队开发。它验证了解耦式 HVDC 供电的概念，但当时尚未成为多供应商、多超大规模厂商的规范。

![](https://substack-post-media.s3.amazonaws.com/public/images/0b644aa9-b60e-41f9-9612-e756f8651db0_529x508.png)

来源：Meta

#### **Diablo 400 规范：HVDC 边柜的标准化**

Diablo 400 规范（得名于 Microsoft 最初的内部项目名 Mt Diablo）把 HPR V4 开创的 HVDC 边柜概念正式化并标准化。由 Google、Meta 和 Microsoft 共同撰写的 Diablo 400 于 2025 年 5 月发布了[草案规范（v0.5.2）](https://www.opencompute.org/documents/ocp-specification-diablo-400-v0p5p2-2025-05-30-pdf)，随后根据业界反馈推出了 [v0.7.0 修订版](https://www.opencompute.org/documents/ocp-specification-diablo-400-v0-7-0-final-pdf)。

**Diablo 400 相对 HPR V4 新增标准化的内容：**

- **多供应商互操作性**：标准化的电气与机械接口，使 Delta 的 PSU 架、Advanced Energy 的电源管理、TE Connectivity 的母排以及多家供应商的 BBU 都能在同一台机柜中协同工作
- **双电压支持**：基础规范定义 +/-400VDC 双极（bipolar）为标准配置（三线制：+400V、-400V，以及整流架输出端的 Common/中点/回流线），800VDC 单极（monopolar）为明确的设计选项（两线制：800VDC 与回流线，与 PE 地安全隔离）
- **功率范围**：每 IT 机柜 100 kW 至 1 MW
- **PSU 设计**：三相交流输入，+/-400VDC 输出。PSU 模块支持机柜前操作、热插拔与带电插拔，PSU 与电源架之间采用 droop 下垂均流与主动均流
- **线缆规范**：电力机柜与 IT 机柜之间的输出线缆在 5m 线长下的压降预算为 0.1%
- **保持时间（holdup time）**：100% 负载下、无储能时最少 20 ms；允许在 Diablo 400 机柜内的 AC/DC PSU 与位于机柜外的下游 DC/DC 变换器之间分布式实现
- **机械**：供大型构件（如 4OU BBU）推入/抽出的滑动架，供 PSU/BBU/CBU 热插拔、带固定导轨/滑动导轨的盲插连接器
- **七大标准化领域**：连接、电力机柜形态、AC-DC PSU 拓扑、DC-DC 模块、冗余架构（单/双馈电，N+x）、HVDC 与液冷系统的安全标准、数据/电源管理背板

选择 400VDC 作为标称电压是深思熟虑的结果。正如 Google 的工程师在 OCP EMEA 2025 上所说："选择 400 VDC 作为标称电压，让我们得以利用电动汽车行业已建立的供应链，获得更大的规模经济、更高效的制造，以及更好的质量与规模。"在双极配置下，每条独立轨道距接地点仅 400V，使系统处于成熟车规级电力电子（650V GaN FET、400V 级电容器、连接器与熔断器）可直接使用的电压范围之内。

#### **没有放之四海而皆准的方案**

不存在一刀切的 800VDC 电力机柜。没错，Diablo 400 提供了共享的基础规范，但落地现实是碎片化的。Nvidia 完全置身其外，正在开发 660kW 的单极 800V 参考设计：风冷样品与量产在 2026 年年中，液冷 VR Ultra 变体于 2026 年末送样。

即便在 Diablo 400 内部，三位共同作者也分歧明显。Meta 运行 600-800kW，采用 50kW HVDC 输出线缆和 8 条 200A 交流输入软线（whip）。Google 通过把机柜空间从 BBU 和超级电容槽位重新分配给 PSU，推到 900kW，使用 100kW 输出线缆，在 1.1MW 顶格点需要 12 条交流软线。Amazon 的设计落在 ±400V 的 800kW。Microsoft 共同撰写了规范，但我们认为其进度较慢。

此外，还有一种替代边柜拓扑，用低压输入 SST 取代传统的"整流器+PSU"栈，例如 DG Matrix 的 Interport Cell 系列。

![](https://substack-post-media.s3.amazonaws.com/public/images/ec9a3b5c-9d6c-49a5-8536-e4443d2ba29c_2079x1163.png)

来源：DG Matrix

#### **电力机柜的成本**

HVDC 电力机柜是早期改造阶段最受瞩目的新增设备成本。我们估计电力机柜的 ASP 将达到每台 $400-500k，约为标准交流电力机柜设备约 $40k ASP 的 10 倍。按部署 MW 口径，落在 $500k/MW 附近。

![](https://substack-post-media.s3.amazonaws.com/public/images/4827b631-2344-4950-ac59-ddb351fddc57_1890x1215.png)

[来源：SemiAnalysis Industrials Model](https://semianalysis.com/industrials-model/)

#### **边柜的市场机会与 TAM 测算**

[在我们的 SemiAnalysis Industrials Model 中](https://semianalysis.com/industrials-model/)，我们通过把上述逐阶段采用时间线应用于数据中心增量产能建设，并逐芯片 SKU 进行计算，测算了 800VDC 设备的 TAM，特别是边柜（电力机柜）与固态变压器（SST）。

我们预计边柜 TAM 将在 2028 年达到约 $11B 的峰值，随后随着第 3 阶段设施级 800VDC 抢占份额而下滑。我们假设电力机柜价值量为 $0.5M/MW。

![](https://substack-post-media.s3.amazonaws.com/public/images/780dbef4-3c5d-46ef-a6b8-0ea6df09d65b_1681x1268.png)

[来源：SemiAnalysis Industrials Model](https://semianalysis.com/industrials-model/)

#### **第 1 阶段小结**

相对当前架构，白区改造意味着每 MW 电气价值量的明确提升，因为第 1 阶段基本上什么都没有删掉。我们估计增量约为 +$400-500k/MW，其中 HVDC 电力机柜占绝大部分。

![](https://substack-post-media.s3.amazonaws.com/public/images/7bfbb2a8-ebbc-4484-823b-2854ef77494b_1386x966.png)

[来源：SemiAnalysis Industrials Model](https://semianalysis.com/industrials-model/)

### **第 2 阶段（2027/2028）：转折点随 800VDC 原生计算而来**

![](https://substack-post-media.s3.amazonaws.com/public/images/43db1495-028a-4d04-b48b-0463c4250d43_1386x520.png)

[来源：SemiAnalysis Industrials Model](https://semianalysis.com/industrials-model/)

第 1 阶段是改造时代的开端。真正的拐点随 800VDC 原生系统的到来而出现。届时，800VDC 不再是前瞻性试点，而是被物理与机柜密度强制的必然转型。为 Kyber Rack 供电的运营者在机柜进线处没有交流退路，我们预计 800VDC 渗透率将在此窗口内急剧飙升。由于 800VDC 原生芯片会先于设施级 800VDC 配电就绪，改造阶段将持续存在。

![](https://substack-post-media.s3.amazonaws.com/public/images/16cce021-8310-4ce7-baf5-ccaf9c299d3b_1102x956.png)

来源：SemiAnalysis

架构上，第 2 阶段与第 1 阶段非常相似。两者都用 HVDC 电力机柜改造白区，都保持灰区原样，都在列级电力机柜中把交流整流为直流。关键区别在于电压在哪里降到芯片可用水平。第 1 阶段（Oberon 机柜）中，IT 机柜内的电源架在电力到达计算托盘之前把 800VDC 变换为 ~50VDC。第 2 阶段（Kyber 机柜）中，800VDC 母排直达计算刀片，由刀片上的电源模块完成最后到 50V 的降压。

OCP 上展示的早期 Kyber 设计描绘了毗邻计算机柜的 DC-DC PSU 边柜，但我们现在认为该方案不太可能被大规模采用。独立边柜比把变换级集成进刀片本身消耗更多的总地面与机柜空间，而且电源模块形态已被证明在计算托盘的体积约束内可行。

![](https://substack-post-media.s3.amazonaws.com/public/images/7e19955d-8e2b-4f82-87d6-3c0c578f5961_736x416.png)

来源：Delta

由于大多数服务器和托盘仍接受约 ~50V 的输入，两种架构都保留了高功率的 800V 到 ~50V DC-DC 变换级。区别只是变换发生的位置。

业界也曾探讨过把 800VDC 直接送入计算托盘，先降到中间总线电压（IBV）再进一步变换到负载点（PoL）轨道。虽然 Kyber 的刀片电源模块确实接受 800V 输入，但它变换到的是既定的 ~50V 母线电平，而非 IBV 方案。鉴于空间与安全约束，在托盘内实现完整的 800V→IBV→PoL 架构仍然极具挑战。

#### **UPS 与电池储能会怎样**

传统集中式 UPS 系统大概是 800VDC 转型中最受争议的基础设施。在 800VDC 架构中，我们预计集中式低压 UPS 将逐渐失去作用，并最终被淘汰。在改造时代，电力机柜直接挂在 800VDC 母排上，容纳 BBU 模块与超级电容（稍后详述），两者都是原生直流耦合。BBU 在停电时桥接数秒到数分钟，超级电容吸收毫秒级的 GPU 负载暂态。两者合力，在没有 AC-DC-AC UPS 对那 2-3% 变换损耗的情况下，取代了集中式短期电池储能与 UPS 渡越功能。

正如我们在[电气深度解析](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical)中所覆盖的，Google 和 Meta 多年前就已采取这种激进路线，用"分布式 UPS"架构绕开集中式单体 UPS。在他们的架构中，交流电直接配电到机柜，机柜内 PSU 完成 AC-DC 变换，机柜级锂离子电池备份单元（BBU）提供短时桥接电力。这移除了集中式 UPS 的 AC-DC-AC 变换对并提升了效率，同时把数据中心所需的总电池容量减半——因为不再需要 A 侧和 B 侧两套 UPS。

![](https://substack-post-media.s3.amazonaws.com/public/images/478dd6fe-aa09-4cc9-b956-bc4ad2c256fe_1162x858.jpeg)

来源：SemiAnalysis

话虽如此，管理分布式 UPS 或电池备份在运营上比运行传统集中式 UPS 更具挑战。我们预计，除 Google 和 Meta 这类垂直整合的超大规模厂商之外，其他运营者至少在中期内仍会保留低压 UPS，用于冗余与负载波动管理。

![](https://substack-post-media.s3.amazonaws.com/public/images/136f5799-ef84-44c5-98cc-05f58a3cc3de_1386x907.png)

来源：SemiAnalysis

对托管（colocation）服务商尤其如此：它们优先考虑灵活性，需要支持混合负载——CPU 机柜、存储阵列、网络设备，以及仍运行在交流上的旧 GPU 机柜。保持灰区交流基础设施完好，可以让这些运营者为密度最高的 AI 机柜部署 800VDC，同时为其他一切负载运行标准交流配电。

我们预计不同运营者会采取不同的备份架构路线，新的替代方案也在涌现。中压 UPS 在 4.16-34.5 kV 电压、直接位于并网点运行，功能上类似机柜级电池机柜，但集中部署在电网接口，而非分布于数据机房。ABB 的 HiPerGuard 运行效率为 98%，已部署于 Applied Digital 位于北达科他州的 400MW AI 园区。ON.energy 数周前被授予一项美国专利，保护其 MV 双变换 UPS 架构。第二种替代方案是设施级 BESS，正如我们[在深度解析中所覆盖的](https://newsletter.semianalysis.com/p/ai-training-load-fluctuations-at-gigawatt-scale-risk-of-power-grid-blackout)，它在兆瓦到数百兆瓦规模运行，提供 1-4 小时的备份时长，并日益取代或缩减柴油发电机。

![](https://substack-post-media.s3.amazonaws.com/public/images/6fffb5d1-f88b-4f32-b529-370fe3077a0d_814x886.png)

来源：United States Patent and Trademark Office

### **第 3 阶段（2028 年末/2029）：以集中式整流器重构电气架构**

![](https://substack-post-media.s3.amazonaws.com/public/images/60b224eb-a095-46df-ac6b-36f6d93cebcc_1386x520.png)

[来源：SemiAnalysis Industrials Model](https://semianalysis.com/industrials-model/)

第 1、2 阶段中，AC-DC 变换发生在靠近机柜的列级 HVDC 电力机柜内。第 3 阶段改变数据中心布局本身，800VDC 成为整个建筑的电气核心。这是真正的拐点，事情开始变得有趣。让我们逐一拆解数据中心每个区域发生的变化。

#### **灰区发生了什么：配电走向直流**

第 3 阶段中，一台位于灰区或室外的专用上游整流器把 415V 交流变换为 800VDC，向整个机房配送直流。这是采用硅 IGBT 或晶闸管、额定 1200-1700V 的成熟设备。

灰区设备由此一分为二。连接数据中心与电网的中压变压器保持不变。中压开关柜保留，因为市电馈入仍是交流，而且随着设施扩展到吉瓦级集群，上游中压基础设施（11-34 kV）预计会变得更加复杂。低压变压器保留，把中压降到 415V 交流供上游整流器使用。低压变压器与 PDU 之间的 480V 交流开关柜，一旦 800VDC 流过母线槽便再无角色，交流机房 PDU 也随之淘汰，因为直流母线槽直接馈电电池机柜，中间不再有交流配电 PDU。总结：AC-DC 变换点以上的一切保留，以下为交流配电而设计的一切出局。

#### **理解直流配电：配电盘、母线槽与保护**

第 3 阶段中，交流配电盘"把一路馈电拆分为多路受保护输出"的功能必须落到某处。三类产品有望承接：(i) 带多路输出、每路集成 SSCB 保护的 MW 级整流器，使整流器本身成为自己的配电设备；(ii) 带断路器插接箱的直流母线槽，把保护保留在配电介质中——前提是具备充分灭弧能力的直流额定插接单元走向成熟；(iii) 预制灰区模块（pod），把整流器、配电盘与母线槽打包成工厂建造的撬块（skid），尤其面向超大规模厂商采购。

![](https://substack-post-media.s3.amazonaws.com/public/images/c35cd9ca-fc1d-414b-969c-0f3cf1019c76_985x1223.jpeg)

来源：SemiAnalysis

主要的交流配电盘在位厂商（Schneider Electric、ABB、Eaton、Vertiv）尚未发布分立的 800VDC 配电盘产品。ABB 2025 年 10 月与 Nvidia 的合作覆盖其"模块化电力模块（modular power block）"内部的配电，而非独立配电盘。EPEC Solutions 公开销售带高分断能力直流断路器的 800VDC 低压配电盘。我们预计分立配电盘将在使用现有单输出整流器的改造场景、以及运营者希望在整流器与保护层之间保持供应商中立的场合，保留一席之地。

电力整流之后，直流母线槽取代交流母线槽，承担机房级 800VDC 配电。在传统交流数据中心中，母线槽系统带有称为插接单元（tap-off）的模块化插接连接，把电力分支到单个机柜或机柜列，类似插线板上的插座，可以在母线槽带电时增删。相比之下，馈线式（feeder-only）母线槽没有中间开孔或插接单元：电力从一端进入，从另一端或预定义的端接点流出。

![](https://substack-post-media.s3.amazonaws.com/public/images/2fb08c19-b4b8-4824-a168-0633a067f566_1386x629.jpeg)

来源：SemiAnalysis

我们预计早期 800VDC 部署将使用馈线式母线槽，因为插接本质上变得更复杂了。在 800VDC 下，带载切断电流会产生无法自行熄灭的持续电弧（一种产生极端高温的等离子放电），因为直流没有过零点，而交流电弧随波形每秒自然过零熄灭 100-120 次。此外，具备充分灭弧能力的直流额定插接单元物理上更大，今天还难以实用。Delta 和 ABB 已公开披露 800VDC 母线槽项目，我们预计 Legrand、EAE 等其他主要母线槽厂商将在 2026 年跟进。

为应对这些挑战，该电压等级在相邻行业已有多种经过验证的保护范式。可能的实现会组合多种方法，其中之一是新一代断路器。更具体地说，沿着固态变压器已经开始的固态化趋势，固态断路器（SSCB）如今正在被采用。SSCB 使用 SiC 或 GaN 在微秒级切断故障电流。由于半导体开关可以直接停止导通、无需物理触点分离，根本就不存在需要熄灭的电弧。

![](https://substack-post-media.s3.amazonaws.com/public/images/37d8190a-4fb4-4530-8b1c-aba5bfebb503_907x518.png)

来源：VIOX

新一代断路器今天已经商业化。ABB 有用于光伏、储能或船舶的 Emax 2（1500V DC），以及 SACE Infinitus（固态，1000V/2500A，2025 年 10 月宣布与 Nvidia 合作进行数据中心适配）。LS Electric 拥有首款 UL 认证的 1500V 直流塑壳断路器，已列入数据中心应用目录。

![](https://substack-post-media.s3.amazonaws.com/public/images/c91e91c3-5245-4fbc-97f2-fda76ea549ea_907x372.png)

来源：ABB

#### **采用低压固态变压器的替代路径**

集中式 AC/DC 整流器的一个新兴替代方案是使用低压 SST。它执行同样的变换——在灰区或室外把 415V 交流变为 800VDC——但形态更紧凑、可编程。LV-SST 绕开了制约中压输入 SST 的 3,300V 级 SiC 供应约束，成为更早上市的 SST 变体。

#### **白区发生了什么：从电力机柜到电池机柜**

可以想见，第 3 阶段我们不再需要执行 800VDC 变换的电力机柜。取而代之，我们迎来一位新朋友：电池机柜。

电池机柜与电力机柜共享大部分部件与功能。主要区别在于它不再执行 AC-DC 整流，因为它直接从灰区接收 800VDC。三大部件保留：

- **DC/DC 配电单元：** 管理 800VDC 母排上的配电、开关与监控。它们不做降压。完整的 800VDC 从电池机柜直达计算刀片。
- **BBU 架：** 在供电中断期间提供渡越电力。
- **超级电容（可选）：** 吸收电池来不及响应的微秒到毫秒级暂态。它们位于直流母排与 BBU 之间，处理快速的电压偏移。

![](https://substack-post-media.s3.amazonaws.com/public/images/34d6f68c-9b87-41df-a49a-d2c3d56c1f31_1386x771.jpeg)

来源：SemiAnalysis

电池机柜通常位于它所取代的电力机柜相同的机柜列位置，不过也有运营者把它们部署在相邻灰区或室外柜体中。权衡很简单：整流器消失，BBU 与超级电容价值量上升。我们预计电池机柜的每 MW 价值量将达到约 $200k/MW。

我们在 [AI 训练负载波动深度解析](https://newsletter.semianalysis.com/p/ai-training-load-fluctuations-at-gigawatt-scale-risk-of-power-grid-blackout)中覆盖了超级电容的化学体系与技术规格。本系列第 2 部分将更深入探讨超级电容经济学、电芯化学、供应商格局以及生产环境部署的实际权衡。

#### **BBU 模块功率上调**

当前模块的额定功率约为 5.5kW。随着 Rubin Ultra 与 800VDC 架构到来，单模块功率升至 8-12kW。Infineon 于 2025 年 3 月发布的 BBU 路线图采用模块化 4kW 部分功率变换器（Partial Power Converter）卡，并联后每单元达 12kW，峰值效率最高 99.5%。

Delta 在 GTC 2026 上把这一步推进到机架层面：其新的 110kW 电源架各自嵌入 80kW 的 BBU 容量，六架一柜合计 480kW。更高的机柜功率要求每柜成比例配备更多备份能量，而更高功率的模块能以更少的物理模块交付这些能量，保留电力机柜中的空间。

![](https://substack-post-media.s3.amazonaws.com/public/images/1ce99f2b-349b-4d73-9e4f-f59ceebcf67d_817x466.png)

来源：Infineon

#### **设施层面发生了什么**

在分析完灰区与白区的完整转变之后，设施层面是变化最小的部分。

在这里，散热仍靠交流。冷水机组、水泵与风机仍由交流电机驱动，需要 DC-AC 逆变器。Delta 在 GTC 2026 上发布了支持 800VDC 的 2.4MW 列间 CDU，这是首个为原生直流设计的大型散热部件。但完整的技术栈（冷水机组、压缩机、水泵、楼宇控制）仍依赖交流，没有厂商销售集成的直流原生散热系统。

发电机架构在一些超大规模厂商处已经独立于 800VDC 开始松动。Meta 在新站点可能完全绕开发电机，Microsoft 的新设计采用部分发电机覆盖。800VDC 可能会加速这一方向，因为超级电容、BBU 与 BESS 构成了分布式备份层级，吸收了发电机过去独占的功能。

#### **中压整流器：容得下所有人吗？**

一个合理的问题是：为什么在低压级整流，而不是直接从中压整流？答案来自半导体额定值。从 13.8kV 或 34.5kV 整流需要额定 10kV 以上的器件，如今几乎没有商业化形态。话虽如此，差距正在缩小，Wolfspeed 的 10kV SiC MOSFET 自 2026 年 3 月起已以裸片（bare die）形式商业化供应。

![](https://substack-post-media.s3.amazonaws.com/public/images/c2b90ca4-19f8-4122-bf76-bdedbd15a5fd_455x336.png)

来源：Wolfspeed

10kV 以上 SiC MOSFET 的发展，为第 3 阶段的第二次演化打开了大门：连低压设备也退出主电力总线。延续这一趋势，更多变换级被折叠，带来新的效率增益。

![](https://substack-post-media.s3.amazonaws.com/public/images/326cfd75-b6d3-4761-a6f3-1aeb9cb39ced_907x420.png)

来源：Wolfspeed

我们 HVDC 时间线的终态将更进一步。尽管采用硅器件串联堆叠的传统整流器可以处理中压整流，但一种新兴技术有望以效率高得多、更紧凑、更快速的方式完成这件事。这项技术是我们旅程下一章的主角：固态变压器。

![](https://substack-post-media.s3.amazonaws.com/public/images/00ab48a9-5be0-4259-b897-652157d87f20_605x317.png)

来源：Infineon

### **第 4 阶段（>2029）：SST，终态**

![](https://substack-post-media.s3.amazonaws.com/public/images/d087f4a7-de52-454f-9e07-69816aed9df4_1386x520.png)

[来源：SemiAnalysis Industrials Model](https://semianalysis.com/industrials-model/https://semianalysis.com/industrials-model/)

终于，我们来到直流配电的圣杯：固态变压器（SST）。这是一类全新的电力电子设备，以高频、半导体化的变换器取代传统铁芯变压器。

![](https://substack-post-media.s3.amazonaws.com/public/images/4372ece2-1a67-47c7-baa1-f25eb3a12c78_331x387.png)

来源：DGMatrix

第 4 阶段及其数据中心布局与第 3 阶段非常相似。主要变化是 SST 以单一设备直接从中压变换到 800VDC，取代了低压 AC-DC 整流器与低压变压器。如果我们考虑上一节的结尾——使用直接从中压交流整流的中压整流器的可能性——那么架构本质上是一样的。

![](https://substack-post-media.s3.amazonaws.com/public/images/b266777c-3ca3-4bed-8452-62503eb520d6_1386x773.jpeg)

来源：SemiAnalysis

#### **简而言之：固态变压器**

##### **SST 简介**

SST 做的工作与每座数据中心灰区里那些庞大的铁铜变压器相同：把电网级中压降到 IT 设备可用的水平。传统变压器利用电网频率下的电磁感应，SST 则用半导体开关级，在远小于其体积的空间内完成同样的变换。

数据中心 SST 是一台三级设备。输入级把交流变为直流，使用额定 3,300V 或更高的 SiC MOSFET 处理危险的中压等级（13.8 至 45kV）。隔离级是体积缩减发生的地方：高频变压器负责降压，同时在电网/电源与数据中心之间提供电气隔离。输出级产生配电系统所需的最终 800VDC，无需逆变器。

![](https://substack-post-media.s3.amazonaws.com/public/images/46fce799-3e1c-4c14-bdbb-6e758b9c8ceb_673x331.png)

来源：ETH Zurich

##### **SST 的优缺点**

SST 的核心价值主张是能效，可直接转化为 OPEX 节省或解锁的算力。通过把中压变压器与整流器折叠为单一电力电子级，SST 从电气链中消除了两个变换级。各厂商的目标是高达 15% 的总系统效率提升，宣称路径从约 82-85% 升至 97% 以上。

SST 的体积也显著更小。传统变压器在 50 或 60 Hz 下运行，需要庞大的铁芯。SST 以 20,000 Hz 或更高的频率开关，铁芯缩小约 90%。这正是 Infineon 宣称的重量减轻 40 倍、体积缩小 14 倍（！）的来源。

![](https://substack-post-media.s3.amazonaws.com/public/images/bf7da904-41c4-4c9c-a180-68fbe8a1d67c_440x330.jpeg)

来源：EENews

此外，SST 是可编程的。传统变压器以固定匝比变压，SST 则主动调节输出，随负载动态调整。它还支持双向电力流动（在需求响应期间向电网送电，或为 BESS 充电）。话虽如此，具备双向能力与集成 BESS 的 SST 可能触发互联电网对其的 DER 重新分类，要求符合 IEEE 1547/2800。

SST 另一项重要价值主张是输入灵活性。一些 SST 架构把这种灵活性延伸为多端口拓扑：单一设备聚合多种输入（市电交流、现场发电、直流电源），并能在软件中跨多个输出路由电力，包括双向。多端口的理由在于，它能减少区域之间的搁浅电力（stranded power），让运营者跨站点编排潮流。

##### **可靠性**

传统变压器作为无源设备，寿命为 30-40 年。尚无 SST 厂商发布过数据中心规模的现场可靠性数据，时间最长的部署是运行于瑞士联邦铁路上的 Hitachi-ABB PETT，自 2011 年运行至今。SST 把热量集中在半导体结中，需要主动冷却，DG Matrix 采用集成液冷，Novos Power 采用基于专有绝缘的风冷。

ETH Zurich 的对比评估发现，工频变压器搭配 SiC 整流器即可匹敌 SST 的效率与功能。数据中心级 SST 依赖中压输入级的 3,300V+ SiC MOSFET，而后者仍处于有限量产阶段。GaN 大致封顶于 650V，只能服务于把 800VDC 变换到机柜级电压的下游各级。

##### **当前效率状态**

最好的公开 SST 基准来自 ETH Zurich：在 INTELEC 2025 上展示的 13.2kVAC 到 800VDC 原型中，400kW 下实现 98% 效率。Johann Kolar 把 98.0-98.5% 定义为当今全尺寸 SST 的技术状态（state of the art），99% 则是数据中心设备的下一个工程目标。

![](https://substack-post-media.s3.amazonaws.com/public/images/8a86f0e8-5162-4f44-9073-06b6648c1656_756x416.png)

来源：ETH Zurich

不同厂商如今正收敛于 98.5% 这一天花板：DG Matrix 的 Interport 平台宣称最高 98.5%，Amperesand 第三代系统宣称大于 98.5%，Heron Power 的 Heron Link 目标 MV 到机柜 98.5% 的效率。Novos Power 报告峰值效率超过 98%。这些数字令人鼓舞，但数据中心需要的是在持续负载下维持 99%+ 效率的 3-6MW 单元。

有两个数据点表明放大工作正在进行。中国行业媒体报道，中国西电（China XD Electric）已在"东数西算"工程下部署 2.4MW 数据中心 SST。NC State 的 FREEDM 系统中心（DG Matrix 的学术源头）已在 3.3kV SiC 上演示 210 kHz 开关，模块化 DC-DC SST 变体的效率目标为 99%。

##### **供应商格局**

![](https://substack-post-media.s3.amazonaws.com/public/images/3b95b712-76cb-4bbd-9459-45d71d908909_2838x2027.png)

[来源：SemiAnalysis Industrials Model](https://semianalysis.com/industrials-model/)

供应商格局变化很快。DG Matrix（ABB 投资背书，Infineon SiC 供货协议）正在出货预认证单元，目标在 2026 年二季度末取得 UL 认证。它是唯一被纳入 Nvidia MGX 参考架构的 SST。Amperesand 目标在 2026 年实现 30MW 商业化部署。Heron Power 正为其 4.2MW Heron Link 单元建造产能 40GW 的美国制造工厂。

在 SST 品类内部，产品正沿低压与中压输入走向分化。DG Matrix 与 Amperesand 两条腿走路：先推出今天即可与现有交流配电并行部署的低压输入 SST 撬块（3.2-4.8 MW），随后在 3,300V 级 SiC 成熟后跟进中压输入单元。Heron Power 与 Novos Power 则专注于直接中压输入单元，把低压变压器与整流器折叠进单一设备。两条路径在输出端都汇聚于 800VDC，但低压路径以保留上游 MV 到 LV 变压器为代价，换取更短的部署时间。

![](https://substack-post-media.s3.amazonaws.com/public/images/f824cdb8-82ca-4971-9bfc-09504959cb20_2079x1169.png)

来源：DG Matrix

Novos Power 宣称推出直接 MV 到 800VDC 的 SST，占地面积小 50%，采用风冷。在位厂商方面，Eaton 于 2025 年 8 月收购 Resilient Power Systems 以获取 SST 技术能力。截至 2026 年 3 月的十二个月内，超过 $320M 的资金流入了 SST 创业公司。

![](https://substack-post-media.s3.amazonaws.com/public/images/b2f2021b-9ca6-46cf-9fa0-d8e7b6480ced_756x521.png)

来源：Novos Power

#### **数据中心布局影响**

SST 消除了约 $0.55M/MW 的低压设备以及第 2 阶段约 $0.20M/MW 的整流器。按 SST 成本约 $1.0-1.5M/MW 估算，我们预计首批 SST 实例相对其直接替代的设备会带来前期 Capex 溢价。

![](https://substack-post-media.s3.amazonaws.com/public/images/f5b62e76-929d-457c-bebf-ed0e5b50778c_875x454.png)

来源：Novos Power

其余电气架构与第 3 阶段保持一致。用于散热、照明与设施系统的 480V 交流辅助母排原样保留。在 IT 机柜侧，我们预计到 SST 部署之时，计算托盘已经原生支持 800VDC。不过，我们也可能看到 SST 采用与 800V 微电网、以及使用 DC-DC 电源架变换器的 IT 机柜相结合的部署方式，这可能会加速采用。

关于第 4 阶段的时间表：这项新兴技术仍处于设计阶段，我们预计到 2029 年初之前不会有大规模的 SST 采用。话虽如此，我们了解到所有主要超大规模厂商都在与主要 SST 厂商进行试点与测试，商业合同已经就位。如下一节所述，技术发展本身并不是决定采用曲线的唯一因素，监管框架与标准是其中重要的一环。在 SST 领域，截至 2026 年 5 月，尚无厂商完成面向数据中心 SST 部署的 UL 认证。

### **SST 市场机会与 TAM 测算**

到 2030 年，我们预计 SST TAM 将达到约 $32B，捕获从边柜层转移过来的需求，加上增量的 MV 到 800VDC 变换。我们按 $1.25M/MW 的价值量测算。这部分机会中有一部分会受到中压整流器的争夺，但我们预计 SST 将拿下多数份额。

![](https://substack-post-media.s3.amazonaws.com/public/images/7b4948fe-0850-4ce8-a562-b003ab2976fe_2456x1834.png)

[来源：SemiAnalysis Industrials Model](https://semianalysis.com/industrials-model/)

**数据中心布局总结：总成本几乎不动，价值量迁移，效率攀升**

#### **电气系统成本**

在我们建模的五种架构中，有四种的每 MW 总电气价值量保持在 $3.6-4.8M 的区间。核心叙事是价值量从灰区向白区迁移，以及由此带来的设备组合变化。

![](https://substack-post-media.s3.amazonaws.com/public/images/d509581e-ad49-4ae5-9469-27d8f8abffb7_1890x1290.png)

[来源：SemiAnalysis Industrials Model](https://semianalysis.com/industrials-model/)

灰区价值量在第 2 阶段收缩，因为集中式 UPS（$1.2M）退出。白区价值量在第 1 阶段见顶，因为 HVDC 电力机柜到来。到第 4 阶段，总价值量攀升至 $4.0M，因为 SST 取代了低压变压器与整流器。

#### **电气系统效率**

我们计算出，基准交流电力路径跨七个变换级的累积效率为 82.0%。VRM（92%）与 PSU（94%）是两个最大的单级损耗来源。VRM 在每种架构中都保留，而 PSU 的损耗是 800VDC 转型所能消除的最大罚项。第 1 阶段仅小幅改善至估计的 83.7%：UPS 双变换环路仍吃掉 3 个百分点，而新的电力机柜整流器（97.5%）加 DC-DC 级（97.0%）只是勉强胜过旧的单级 PSU。

真正的跃升出现在第 2 阶段（86.5%），UPS 的取消把链条从七级砍到五级。第 3 阶段推进到 86.9%，因为集中式灰区整流器在 MW 规模运行（效率高于模块化的机柜安装单元），且 800VDC 机房级配电消除了交流的集肤效应与无功损耗。我们估计第 4 阶段达到 87.4%，因为 SST 以单一设备取代了两级。

在 1GW 的 IT 负载下，第 2 阶段的增益折合约 58MW 的持续电网电力节省。第 3 阶段扩展到 63MW，第 4 阶段到 69MW。Nvidia 引用了最高 5% 的效率提升，意味着 1GW 下约 50MW。我们计算的第 4 阶段相对基线 5% 的效率差值，与 Nvidia 报告的数字吻合。

## **800VDC 转型的另一面：挑战与局限**

到目前为止，我们描绘了一条充满希望的路径，但一如既往，途中会出现各种挑战。下面我们拆解将决定 800VDC 多快从小规模试点走向更广泛采用的四大障碍。

### **挑战 1：监管、安全与接地**

#### **监管**

由 NFPA 按三年周期出版的《美国国家电气规范》（NEC）管辖美国的电气安装。它被几乎每个州和市镇采纳为具有约束力的法律，决定了运营者是可以按标准设计建造，还是必须逐站点与当地有管辖权机构（AHJ）谈判。完整的 800VDC 规范支持目标落在 NEC 2029。因此，2029 年之前的部署需要定制化的 AHJ 批准以及 OEM 级的逐站点 UL 认证。这对拥有内部规范工程团队的超大规模厂商可行，但对托管运营商和较小的建设者可能构成实质性壁垒。

我们看到与电动汽车行业早期的一个有用类比：当年 Tesla 因为全行业标准尚未出现，自行设计并批准了自己的内部安全框架。2029 年前部署 800VDC 的超大规模厂商将处于类似境地。

以历史标准衡量，考虑到此前船舶、电信和 EV 领域的直流电力标准化时间线，NEC 2029 已经算快了。而且，五家超大规模厂商加上身兼需求创造者与方案架构师的 Nvidia 形成的极端买方集中度，以及 EV 800V 元器件供应链，都可能让时间线受益。

我们认为 NEC 2029 将实现部分条款落地，而规范的完全成熟可能要等到 NEC 2032 或 2035。"部分"的含义是基础框架已经存在（电压分类、导线截面、过流保护），但直流专用的电弧闪络 PPE 表、母线槽标准以及储能维护规程很可能缺席。

#### **安全**

最大的安全风险是电弧闪络（arc flash）。IEEE 1584 不覆盖直流，NFPA 70E 也没有针对 600-1000VDC 的 PPE 表。UL Solutions 已成立直流安全研究联盟（Direct Current Safety Research Consortium）来构建缺失的危害模型，并明确把 800V DC 数据中心架构列为目标应用之一。

即便撇开规范空白，日常现实可能更为艰难。在 48V 下，技术人员可以只穿最少 PPE 就热插拔服务器托盘。而在 800V 下，许多在 48V 属于常规操作的机柜旁任务，很可能按 NFPA 70E 要求由合格人员执行，穿戴耐弧服、额定 1000V 的绝缘手套和面罩。电容器组与 BBU 模块在断电后仍保留危险电荷，而针对交流的标准上锁挂牌（lockout-tagout）流程并未考虑储存的直流能量。维护之前，必须逐一验证多个电源均已去能。

Flex——Nvidia 的重要制造合作伙伴——已公开倡导在 800VDC 设施开展深入的危害识别与安全培训。

![](https://substack-post-media.s3.amazonaws.com/public/images/a5461320-f56e-474f-b358-2d3da8a9bd43_907x290.png)

来源：Flex

#### **接地**

接地会级联影响到保护器件数量、故障行为、绝缘监测、人员安全与供应商兼容性，这使其成为 800VDC 设施中影响最深远的早期设计选择之一。

Siemens/Nvidia 的论文《Protections for Data Centers Powered by Direct Current》给出了四个选项。±400V 系统可以采用高阻接地（HRG），容忍第一次接地故障、只要求在第二次故障时快速切断；或者采用直接接地，要求任何故障都立即清除。800V 单极系统可以浮空运行，在每个分支上做绝缘监测；或者采用直接接地的回流导体。

![](https://substack-post-media.s3.amazonaws.com/public/images/4c6cd4d7-a496-406f-961a-1a750f821b0b_907x436.png)

来源：Siemens、Nvidia

权衡在于成本。HRG 与浮空系统需要两根导体都配备按完整 800VDC 额定的保护器件，外加绝缘监测基础设施。直接接地回流减少了保护器件数量，但消除了并联变换器之间的电气隔离。OCP Diablo 400 同时允许 ±400V 双极与 800V 单极，把选择权留给运营者。

现实是业界尚无共识。SST 与电力电子厂商正围绕不同的接地假设进行优化，这使得该选择成为对供应商生态系统的承诺，而不仅仅是技术选择。

### **挑战 2：散热与交流辅助负载**

散热是 800VDC 数据中心中最大的交流负载，而且没有厂商销售直流原生的散热生态系统。Delta、Danfoss 等一些厂商正在取得进展。Danfoss 的 Turbocor 压缩机在数据中心冷水机组中占主导地位，内部以 700-813V 直流运行。Danfoss 还制造 VACON NXP 变频器，可直接接受 640-1200 VDC 输入，800V 正处于其工作范围之内。DCAirco 为电动出行领域出货 4-8kW 的 800V 直流冷水机组——比数据中心规模小 100-1000 倍，但证明了制冷循环可以在这一电压下工作。

散热之外，开关柜操动机构、照明、消防泵、楼宇管理传感器与安防系统都运行在交流上。正如 Nvidia 团队在 OCP Global Summit 2025 上所展示的，800VDC 参考架构将在 800VDC 计算配电之外保留一条交流辅助母排，正是出于这个原因。

话虽如此，供应链正在行动。上文提到的 Delta CDU 处于最前沿，但大多数辅助设备类别（照明、消防、安防）仍缺少直流变体。随着数据中心工业 capex 在 2026 年迈向超过 $400 billion、电气设备占比达到 30-35%，开发直流原生产品的激励正在增强。

![](https://substack-post-media.s3.amazonaws.com/public/images/fd764419-81ad-4080-af93-2cd649efb4fb_907x216.png)

来源：Delta

### **挑战 3：供应链标准**

直流配电的创新走在了成文规范之前，大多数 800VDC 设备品类的标准仍然滞后。母线槽是进展的一个好例子。管辖母线槽系统的标准 UL 857 最初把覆盖上限定在 600V，并以均方根值（RMS）定义数值。2025 年出版的第 14 版把上限提高到 1000VDC，开发中的第 15 版目标为 1500VDC。母线槽之外，认证路径仍然缺失，每个安装都变成定制工程项目：运营者必须逐案完成产品鉴定、谈判导线额定值，并获得 AHJ 批准。

![](https://substack-post-media.s3.amazonaws.com/public/images/6286e530-bd0e-4860-a636-292f1460e39a_687x330.png)

来源：UL Solutions

一份目标在 2026 年发布的 OCP 白皮书可能会有所帮助，OCP 工作组也正在与监管机构和认证机构协调，力争在 2026 年底前落地首批标准，但厂商们已经在展示各自的原型。Delta 在 OCP 2025 演示了 800VDC 风冷母线槽，LS Electric 在 DistribuTECH 2026 展出了直流电力设备，而且在团队近期参加的几乎所有会议上，800VDC 就绪的原型无疑都是主角。

![](https://substack-post-media.s3.amazonaws.com/public/images/846389b8-353b-4438-ada7-86da682a49b7_730x480.png)

来源：LS Electric

### **挑战 4：电网互联与监管压力**

正如我们在[吉瓦级 AI 训练负载波动深度解析](https://newsletter.semianalysis.com/p/ai-training-load-fluctuations-at-gigawatt-scale-risk-of-power-grid-blackout)中所覆盖的，电网扰动期间的数据中心失负荷事件已成为电网运营者的严重关切。800VDC 把面向电网的行为移入软件定义的电力电子（SST 控制算法、变换器限流、直流母排电容……），使问题更加尖锐。

电网运营者现在必须对这些动态进行建模和约束，监管门槛也在提高。NERC 于 2026 年 5 月发布了针对大型计算负载的三级 Essential Actions 警报（其最高级别），强制响应截止日期为 8 月 3 日，并提议设立计算负载实体（Computational Load Entity）注册制度，针对在 60kV+ 接入、聚合容量 20MW+ 中耗电 1MW+ 的数据中心。ERCOT 的 NOGRR282 增加了电压与频率渡越要求，并强制所有大型负载同时提供 PSS/E 与 PSCAD 电磁暂态模型。

#### **为什么 800VDC 加重了举证负担**

传统交流数据中心有一套规划者可以建模的"面向电网的词汇"：UPS 切换阈值、ATS 时序、电机负载行为、发电机控制，以及 CMPLDW 等复合负载模型。这些都无法刻画 800VDC 设施——其对电网电压跌落的响应，取决于 SST 控制算法（跟网型 vs 构网型）、BESS 荷电状态、瞬时 GPU 负载特征，以及多台并联 SST 之间的相互作用。

800VDC 还折叠了电力栈的多个层级。在交流设施中，电网公司研究互联与聚合负载，运营者则独立设计 UPS、开关柜与机柜配电。而在基于 SST 的 800VDC 设施中，同一套变换器控制决定着直流母排稳定性、故障渡越、限流、谐波注入与故障后负载恢复。互联因此变成了一项工程产品，需要横跨电力电子设计、电网级动态建模与监管沟通的 EPC 能力。这催生了 Aran Industries 等新进入者——构建 AI 原生 EPC，交付可 PE 盖章的 800VDC 工程包。

## **理解不那么基础的部分：800VDC 背后的物理**

### **为什么超高密度会让低压配电崩溃：热量与重量**

在功率固定时，把电压从 54V 提高到 800V，可使电流减少约 15 倍、电阻损耗减少约 220 倍。这正是让 800VDC 在铜重、热负载与配电成本上构成阶跃变化的原因。

从功率方程开始：

对于固定的机柜功率 P，提高 V 可线性降低 I。电流更低意味着导线更细、铜重更少、走线更容易。

欧姆定律给出电阻为 R 的导体两端的压降：

该压降就是导体中以热量形式耗散的能量。将其代入功率方程，即得到电阻损耗方程：

电流以平方形式出现，因此电压与损耗之间是二次关系而非线性关系。正是这个方程使 800VDC 成为必然。

以 600kW 机柜功率（Kyber 级，Vera Rubin Ultra NVL576）为例：

在 ~54 VDC（当今标准）下：

在 800 VDC 下：

电流减少了 14.8 倍。再套用损耗方程。对相同的导体电阻 R，I² 之比意味着：

同一导体在 54 V 下的阻性发热约是 800 V 下的 **219 倍**。在更常被引用的 48 V 对比中：

实践中，运营者并不会保留同样的导体、把 219-278 倍的损耗降低全部落袋。他们会缩小铜截面，用损耗裕度换取重量、成本和走线空间的削减。即便按 800V 重新选型之后，效率增益依然是变革性的。

### **800VDC vs. ±400VDC：悬而未决的拓扑**

"800 VDC"可能指两种不同的电气配置，这一区别对部署策略、安全工程以及下游半导体选型都至关重要。"800 VDC"既可以指单端（single-ended）800V 母线，也可以指双极（bipolar）±400V 母线（极间电压 800V）：

#### **单端 800V**

在单端 800VDC 架构中，母线是一根以回流线为参考的单一 800V 轨道，外加保护地。1MW 时母线承载 1,250A。电流更低意味着整条配电路径上导线更细、连接器更小、I²R 损耗更低。母线结构的实现也更简单，因为它不依赖维持两条轨道之间的对称性。功率级可以直接围绕完整母线电压设计，采用标准高压器件和常规变换器拓扑。没有需要检测、调节或控制的中点。

#### **双极 ±400V**

替代方案把 800V 拆分为围绕接地中点对称的两条 400V 轨道：三根电力导体（+400V、中点、-400V）加保护地。负载输入两端看到的仍是 800V，但每条轨道距地仅 400V。这里的核心论点不在电气而在经济。400V 电力电子之所以成熟，是因为电动汽车行业在 400V 平台上实现了规模化建设。Google 在 OCP EMEA 2025 上表示，选择 400VDC"让我们能够利用电动汽车行业已建立的供应链"。OCP Diablo 400 规范所考虑的是解耦式电力机柜，把三相交流变换为 ±400VDC，每柜 100kW 至 1MW。该规范同时把 800VDC 单极列为设计选项，留了一扇门。

这里同样存在权衡。第三根导体在电力路径上的每个点都必须走线、端接和保护。放到数千个机柜的规模上，它带来可观的铜量、连接器硬件与安装人工的增加，并使热插拔连接器设计复杂化——中点必须按受控顺序接通和断开触点，以避免瞬态电压尖峰。

![](https://substack-post-media.s3.amazonaws.com/public/images/423bf1e3-5ae5-44e6-9520-7aafe5525a60_907x510.png)

来源：OCP

在付费墙之后，我们将讨论 800VDC 革命的主要赢家与输家，以及谁更有条件从这场转型中获益。
