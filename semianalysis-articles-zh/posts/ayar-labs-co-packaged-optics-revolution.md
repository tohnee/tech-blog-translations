---
title: "Ayar Labs | 共封装光学革命 | 手握 HPE 与 Nvidia 订单的最具前景硬件创业公司？"
title_en: "Ayar Labs | Co-packaged Optics Revolution | The Most Promising Hardware Startup With Wins At HPE And Nvidia?"
date: 2022-04-30
source: https://newsletter.semianalysis.com/p/ayar-labs-co-packaged-optics-revolution
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# Ayar Labs | 共封装光学革命 | 手握 HPE 与 Nvidia 订单的最具前景硬件创业公司？

> 原文：[Ayar Labs | Co-packaged Optics Revolution | The Most Promising Hardware Startup With Wins At HPE And Nvidia?](https://newsletter.semianalysis.com/p/ayar-labs-co-packaged-optics-revolution) · SemiAnalysis

Ayar Labs 是半导体世界里最有前景的半导体创业公司之一。公司成立于 2015 年，团队汇聚了来自 Intel、IBM、Micron、Penguin、MIT、伯克利（Berkeley）和斯坦福（Stanford）的众多顶尖技术专家。早在 2015 年，Ayar Labs 就洞察到业界最根本的难题之一，并开始从零起步工程设计一套解决方案。这与大多数硬件创业公司形成鲜明对比——后者往往专注于既没有真正竞争优势、也没有突破性路径的细分市场（大多数 AI 创业公司正是如此）。本文将讨论 Ayar Labs 的融资、他们正在解决的核心问题，并对他们的技术方案做一次深度解析。

去年，Ayar Labs 披露拿下一台定制 AI 机器超过 5000 颗的设计导入（design win），此后进展顺利。最新公告是 Ayar Labs 融资 1.3 亿美元。创业公司融资通常是件可以忽略的事，但 Ayar 的做法相当有意思。一些传统基金也出了钱，但我们了解到，Ayar Labs 是有意压低估值——拒绝了这些资金管理人想给的更多钱。

把饥渴的 VC 拒之门外是明智之举，因为即便是最成功的硬件创业公司，估值峰值一般也落在 10 亿到 20 亿美元区间。好的公司在此价位被收购，差的公司则要么遭遇估值下调轮，要么把人忽悠进一个永远兑现不了的高估值。关于私募半导体融资、时机与投资这个话题还有很多可谈，但我们留到日后再说。

Ayar Labs 反而似乎更专注于那些同时能做合作伙伴的战略投资者。过去这包括 GlobalFoundries、Intel、Lockheed Martin、Applied Materials 和 Dowing 等大牌。最近一轮 1.3 亿美元融资又把 Nvidia 和 HPE 拉进了阵营。我们相信，这些战略投资者大多至少带来了一些技术诀窍或合作伙伴关系。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

举例来说，GlobalFoundries 参与了种子轮。我们过去曾把他们描述为[领先的硅光子代工厂](https://semianalysis.substack.com/p/globalfoundries-fotonix-the-leading?s=w)，他们在 GFS [45CLO 工艺节点](https://semianalysis.substack.com/p/globalfoundries-is-a-leading-edge?s=r)上为 Ayar Labs 制造光子 IC。Intel 是 Ayar Labs [与 FPGA 共封装光子小芯片](https://fuse.wikichip.org/news/2540/darpa-eri-how-ayar-labs-collaboration-with-gf-produces-a-photonics-chiplet-that-can-supercharge-intel-fpgas/)的首个用户，这帮助 Ayar Labs 完成了方案的概念验证。[HPE 正在与 Ayar Labs 合作](https://www.hpe.com/us/en/newsroom/press-release/2022/02/hewlett-packard-enterprise-and-ayar-labs-announce-strategic-collaboration-and-investment-to-develop-next-generation-data-center-architectures-and-networking-with-optical-io.html)，开发构建在 Slingshot 之上、支持解耦式服务器设计的下一代高性能计算机互连方案。Nvidia 虽未确认其计划，但我们会在文后讨论他们与 Ayar Labs 的潜在打算。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8108c412-a29e-45d8-be1f-3ae608d17e10_1024x537.png)

首先，让我们从定义 Ayar Labs 着手解决的问题开始，并说明为什么他们的方案如此精妙。输入/输出（IO）一直是计算的制约因素。大多数时候处理器都在等数据，而不是真正在算。这一点我们在[先进封装系列第 1 部分](https://semianalysis.substack.com/p/advanced-packaging-part-1-pad-limited)中有详尽阐述，这里简单回顾：相对于计算侧的数据需求，半导体封装上可供数据进出的焊盘数量增长极其缓慢。因此业界转向更窄、极高速的数据 IO 方式。遗憾的是，数据速率同样没跟上，而且 IO 的功耗不成比例地上升。IO 与数据搬运功耗是服务器芯片功耗增长的首要驱动因素。这种功耗增速不可持续，也是计算中巨大的低效来源。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/bfee9c25-c50d-4a44-9ed4-71a4ac757ae8_1024x529.png)

Ayar Labs 决心打破这一范式。与其被封装间电互连的 IO 密度问题、数据速率扩展和能效不彰所限制，目标是将光通信直接做到封装上。Ayar Labs 的核心论点是：在 1cm 到 10cm 的传输范围内，光学 IO 比当前的电学体制更高效。破解数据搬运功耗膨胀问题的最佳方式是：一旦数据传输超出这一距离，就切换到光学。

> 我们应该造出所能造的最大芯片，然后把它们连接起来。这样做是因为它合乎情理。这正是芯片随时间越做越大的原因。它们并没有随时间变小，而是在变大。原因在于更大的芯片能受益于片上导线的高能效。无论芯间 SerDes 的能效做得多高，都永远比不上芯片上的一根导线。那不过是一小段细如发丝的导线。我们希望把芯片做得尽可能大，然后再把它们连接起来。我们称之为超级芯片（superchip）。
>
> 我相不相信小芯片（chiplet）？未来会出现一些可以直接接入我们芯片的小东西，这样一来，客户只需少量工程投入就能做出半定制芯片，把它接到我们的芯片上，以自己独特的方式在自家数据中心里实现差异化。没有人愿意花 1 亿美元去做差异化。他们乐意花 1000 万美元实现差异化，同时蹭别人那 1 亿美元的投资。NVLink 芯片间互连，以及未来的 UCIe，将会带来许多这样激动人心的机会。
>
> Jensen Huang，Nvidia 创始人兼 CEO

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e1b6cc5e-8187-49c1-b5a7-6c8ce83345f2_1023x514.png)

当前，计算、内存、加速器和网络都被严格分层地塞在相当小的服务器机箱里。服务器内与服务器外之间的边界，从效率角度看是一条极其昂贵的边界。各家厂商争相把封装越做越大，以继续扩展性能、减少与外部世界的高成本通信，但随着转向支撑这些大封装的特种封装技术，成本也极其高昂。因此 AMD、Intel、Nvidia 等公司都在克制封装尺寸的增长。即便封装是免费的，高性能计算与 AI 的问题规模也远远大到连晶圆级封装都装不下，例如 [Cerebras](https://semianalysis.substack.com/p/cerebras-wafer-scale-hardware-crushes?s=r)，或[晶圆级系统（System on Wafer）封装](https://semianalysis.substack.com/p/tesla-ai-day-supercomputer-chip-teaser)，如 [Tesla 的 Dojo AI 训练架构](https://semianalysis.substack.com/p/the-tesla-dojo-chip-is-impressive?s=r)。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9c124479-3b20-4f3b-894c-e2fcce1d4f7e_1024x531.png)

如果同一服务器内封装与封装之间、以及跨服务器与跨机柜之间的数据搬运功耗代价被拉平，服务器设计的整个系统架构都将改变。高性能应用的最佳方案将不再是把许多机柜的独立服务器互连起来当作一台机器，而是一个由内存、CPU、网络与加速器组成的高度可组合的巨大资源池。这片计算与内存的海洋在延迟视角上彼此都相当接近，同时也不付出巨大的功耗代价。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

从这个视角看，为什么全球最大的超级计算机承包商 HPE、以及在高性能计算领域拥有超过 95% 加速器份额的 Nvidia 会成为战略投资者，就显而易见了。他们需要把这项技术用于下一代高性能计算架构。Nvidia 作为战略投资者似乎有点奇怪，毕竟他们有超过一百人专注于光通信。Nvidia 在该领域还做了多次收购，但这恰恰印证了 Ayar 在此的技术实力。我们猜想这笔交易可能是某种授权方案，或短期的外部权宜之计。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2a499bfb-7444-4199-987a-9bd57c7cc9d4_1024x523.png)

转向共封装光学还有许多不那么直观的好处。数据不需要从处理器发往网卡、再穿过昂贵的光收发器。处理器本身也能省下大量成本，因为不必把那么多裸片面积留给大型高速电 SerDes。鉴于 Ayar Labs 已加入开放的 UCIe 标准，我们相信他们的小芯片将以该协议作为与外部公司芯片接口的基础层。UCIe 支持 Intel、ASE 和 TSMC 的多种封装选项。处理器一侧，Intel、AMD、Broadcom、Micron、Mediatek 和 GUC 都是联盟成员。UCIe 大幅降低了将第三方小芯片集成进封装的门槛，反过来也会降低 Ayar Labs 拿下设计导入的门槛。即便没有 UCIe，Ayar Labs 也明确支持高密度扇出、Intel 的 EMIB 以及其他硅中介层技术。

UCIe 与 Ayar Labs 方案的美妙之处在于协议无关。TeraPHY 小芯片如果愿意可以承载高延迟以太网，但真正的价值在于它能承载 PCIe 5.0、CXL 2.0，甚至 Nvidia NVLink 这类定制协议。Nvidia GPU 与 NVSwitch 上的 NVLink 看起来是完美的应用场景，因为 Hopper 的 NVLink fabric 可跨多个机柜纵向扩展至 256 颗 GPU。Nvidia 会在下一代上进一步增大这个数字。功耗预算显然在膨胀，H100 SXM5 GPU 与 NVSwitch 逐代都有相当大的提升。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d3023da2-bda5-4ac3-9dc6-87a12e5a4ee2_1024x529.png)

Ayar Labs 声称每比特传输功耗低于 5pJ，大约是下一代 800G 光收发器的 1/3。多数情况下，数据还要经过网络交换机以及更多跳的光收发器或直连铜缆，因此功耗差距还会更大。在这类场景下，Ayar Labs 方案相比传统以太网方案的能效可以高出一个数量级，延迟也更低。

当前一代 TeraPHY 是一颗仅 75mm2 的小裸片，可提供 2Tbps 的 IO。典型的 0.2Tbps 光收发器合计约 ~150mm2。达到同等 IO 速度，Ayar Labs 使用的硅面积远少于可插拔光收发器，这还没算处理器侧 SerDes 省下的面积。需要指出的是，Ayar Labs 的数字不含外部激光器，后文会对此讨论。2Tbps 的 TeraPhy 通过 8 根单模光纤传输。许多可插拔光收发器使用多模光纤，这是一项取舍。Ayar Labs 利用的每根单模光纤承载 8 通道 32Gbps NRZ。这也比更复杂的 PAM4 编码更高效。由于无需 FEC，NRZ 的延迟也更低。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

对一直在跟进的读者：这意味着每颗 TeraPHY 小芯片可提供共 64 条 PCIe 5.0 / CXL 通道。Ayar Labs 给出的示例是一颗处理器配 4 颗 TeraPHY 小芯片，理论上就是 256 条！未来几代可以沿多条轴线扩展：通过更多微环调制器增加每根光纤的通道数、把数据速率提升到 64Gbps，或者上更多光纤。既然也支持 Hyper X 拓扑，就可以构建一个由处理器、加速器与内存组成的高带宽、高端口数（radix）网络。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a69e2624-485a-4f02-987f-8acba686f71e_1024x524.png)

Ayar Labs 的秘方由几个要素构成。多数光芯片使用马赫-曾德尔调制器（Mach-Zehnder modulator）把数据编码进激光器发出的光，但这类调制器非常大，因而限制了密集布置大量通道的能力。Ayar Labs 则使用微环调制器（micro-ring modulator）。这种调制器小得多、也高效得多。调制器的差异，正是典型收发器相比 Ayar Labs TeraPHY 硅面积多出一倍、每比特传输功耗高 3 倍的主要原因。

微环调制器的问题在于其良率出了名地难做。这是因为微环结构上哪怕亚纳米级的变异，都会改变编码数据时输出的波长，甚至导致编码出错。此外，除了制造难度之外，微环对温度还极其敏感。Ayar Labs 声称已与制造伙伴 GlobalFoundries 解决了这一问题。他们没有告诉我们是怎么解决的，但我们认为是通过对微环调制器温度的有意控制。Ayar Labs 很可能在每个调制器周围布有电路，不断通断以精确升降微环调制器的温度，确保数据被编码到正确的波长且不出错。这一方案可让每个调制器单独调谐。这一方案可让每个调制器单独调谐。

除了光子 IC 与封装两者更紧密的集成之外，另一大优势是使用解耦的激光器。这与 Intel 形成鲜明对比——Intel 目前在光收发器领域握有很大的成本优势，其部分原因正是集成的键合激光器。Ayar Labs 认为自己因可靠性顾虑而占据优势。在可插拔光学时代，可靠性顾虑可以回避，因为收发器可以更换；而在共封装光学下，任何不可靠都会拖累整个封装的能力。

鉴于 Nvidia 当代 Hopper SXM5 据报道售价超过 2 万美元、顶级网络交换 ASIC 超过 4 万美元，希望你能明白哪怕 99% 的可靠性会有多糟。因此 Ayar 选择外置激光器模式，因为激光器是光学器件中最可能失效的部分。外置激光器已有名为 CW-WDM MSA 的开放标准，目前已有 49 家公司支持，Macom、Sivers Photonics 和 Lumentum 目前已有第三方激光器可供货。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/dd5362f5-0f60-4867-a083-e3e13e66fa44_1023x489.png)

Ayar Labs 已展现出令人惊叹的成功与实力，堪称最具前景的硬件创业公司。他们在 HPE 等公司拿下大单，Nvidia 的战略投资也足够抢眼。他们是共封装光学方案走得最远的厂商，通过支持开放标准与多种封装类型，他们为高性能计算架构的潜在革命打开了闸门。他们与 GlobalFoundries 在微环调制器上的创新意义重大，尤其是其可靠性声明——这将是大批量产品的业界首次。可插拔光学永远有其位置，但共封装光学在功耗、性能、带宽密度乃至成本上都有诸多明确优势。

[分享](https://newsletter.semianalysis.com/p/ayar-labs-co-packaged-optics-revolution?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

*SemiAnalysis 的客户与员工可能持有本文所提及公司的仓位*。
