---
title: "军用传感与通信系统的未来——共封装光学（CPO）使融合式射频相控阵成为可能"
title_en: "The Future Of Military Sensing And Communications Systems – Co-Packaged Optics Enable Converged RF Phased Arrays"
subtitle: "Lockheed Martin NGAD 背后的 Ayar Labs 技术"
date: 2022-11-02
source: https://newsletter.semianalysis.com/p/the-future-of-military-sensing-and
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 军用传感与通信系统的未来——共封装光学（CPO）使融合式射频相控阵成为可能

> 原文：[The Future Of Military Sensing And Communications Systems – Co-Packaged Optics Enable Converged RF Phased Arrays](https://newsletter.semianalysis.com/p/the-future-of-military-sensing-and) · SemiAnalysis

**Lockheed Martin NGAD 背后的 Ayar Labs 技术**

半导体与传感器的进步正在快速改变战争的形态。以往那种「巨额预算投给单一项目、花数十年时间只产出几百台装备」的模式正面临巨大压力。隐身技术、无人机以及精确制导导弹的大规模量产，正在迅速改写国防的攻防方程。当前，最先进的军队拥有数十或数百架战斗机与轰炸机，却拥有数以万计的无人机与导弹。现代军队能否以现有能力对抗、甚至可靠追踪高密度的这类新式武器蜂群，仍是未知数。

Ayar Labs 与 Lockheed Martin 发表了一篇颇具启发性的论文，探讨利用硅光子学实现通信的射频（RF）融合相控阵天线。这一方案有望解答上述问题。今天我们想讲解：当前国防系统的传感器与通信架构、这些架构在成本与性能上的问题、数字波束赋形、MIMO、射频相控阵，以及面向国防应用的硅光子学。特别感谢 SPIE Optics and Photonics 大会的演讲与论文，它们对本文的写作帮助巨大。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3a68cf43-e198-42be-9520-2b67329ed42e_958x611.png)

首先讨论现代传感器与通信架构。上图是 F-22 猛禽或 F-35 闪电 II 这类现代喷气式战斗机的示意模型。这类飞机使用由复杂传感器组成的阵列来完成瞄准、跟踪、通信等任务。以 F-35 为例，它是[红外传感器系统的先驱](https://www.lockheedmartin.com/en-us/products/f-35-lightning-ii-eots.html)。该系统利用多组电光（electro-optical）天线阵列，赋予飞机对周边 360 度的全方位视野，大幅提升了战斗机搜索与跟踪目标的能力。该系统最大的缺陷在于灵活性相当有限：整个子系统生活在自己的「气泡」里，拥有自己的处理管线。

> 每个孔径都与其对应的射频系统深度集成，若不物理上重新布线平台，或重新训练既有系统以适配另一系统的需求，就无法被其他系统利用。
>
> —— Lockheed Martin

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ce104109-4f4d-4eed-8d4d-899413bb89a2_1427x656.png)

要在国防应用中部署这些传感器，需要一整套高度定制的工作，从物理层的电光红外传感器研发，一直到处理与算法。开发这类系统成本极高，而且牵涉众多学科，必须长期协同才能做出完整系统。电光红外系统与另一套射频传感或通信系统彼此完全独立。

在很多情况下，每个传感器都针对特定用例做优化。一支现代化军队必须拥有多套射频系统，用于探测、跟踪、连接并与各类飞机、无人机、导弹、直升机、卫星、地面武器系统、舰艇、潜艇等通信。随着为对接战场上这些各式要素（敌我皆含）而建的射频子系统越来越多，复杂度与成本急剧攀升。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/47debceb-c761-4538-ab1f-cd5305b982f5_1357x735.png)

这些先进的军事应用开始需要数十种不同的子系统，成本随之膨胀。而且，任何一个子系统的延误都意味着整个平台的延误。F-35 就常因这些延误与成本受到批评。虽然各项延误的确切原因不得而知，但打造如此复杂系统所涉及的整体式（monolithic）规划与复杂性是罪魁祸首。如今 F-35 已经正常运转并形成部署，它被公认为领先世界上任何其他战斗机数个身位，而其射频子系统正是其中重要的一环。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ab8c525a-b6b3-4016-851b-935fdd800c94_1398x567.png)

设想一下，如果这许多不同的射频子系统能够以解耦（disaggregated）的方式开发与部署。与「传感器、射频处理、应用层全部为每个具体任务分别构建」的整体式子系统不同，解法空间被重新框定：少数几大类传感器可以针对射频增益、噪声及其他属性做优化，而不必为确切用例调校。射频处理算法可以按更快的节奏更新，基于这些射频单元输入与输出的数据引入新的传感与通信能力。应用算法也可以按独立的节奏更新，以应对不断演变的战场。先进技术落地的周期将从昂贵的 20 年级项目大幅缩短。

上图是 NGAD 战斗机的一个示意例子，只有两类传感器：高性能相控阵天线阵列与电光红外天线阵列。与 F-22/F-35 战斗机的示意相比，传感器种类显著减少。尽管传感器种类减少，但把传感器与处理解耦，将带来更强的能力：跟踪更多、更小、更隐身的目标。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/90baa2b6-a0c8-4c4b-88bc-17efbb912116_1423x717.png)

各路射频传感器将在处理之前先完成融合。借助 MIMO 与数字波束赋形等技术，可以获得更高的数据速率与更低噪声的信号。

数字波束赋形与 MIMO（多输入多输出）是早已应用的技术，但更复杂的算法与技术持续推高射频系统的性能。我们从未在公开报告中讲解过波束赋形或 MIMO，这里做一个快速入门。请注意我们做了极简化处理——关于这些主题足以写成许多本书。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5afb0b0e-699b-4375-924a-34e72fe04ebc_502x282.png)

MIMO 指收发设备具有多个输入与多个输出。它对总数据吞吐量的收益巨大。作为参照，5G 小基站的收发对数在 64 发 64 收的量级。既然消费市场已经验证了这些技术，下一代飞机海量数据进出通路的实现路径是清晰的。

MIMO 较不直观的一面在于射频传感应用。设想发射端是一架无人机或隐身飞机。敌方并不是在主动向战斗机发信号，而是在设法掩盖自己的雷达与红外特征。想象一下，要接收一个低雷达特征、覆盖雷达吸波材料的作战平台所发出或辐射的信号有多难。传感应用需要获知敌方的位置、航向、速度以及机动的变化率。传感系统把不明目标判别为鸟、无人机、隐身战斗机、隐身轰炸机还是导弹，对应的作战响应将完全不同。

MIMO 用于传感时，可以在更大的有效面积上接收到更宽的输出信号范围。这也正是[数字波束赋形](https://www.youtube.com/watch?v=A1n5Hhwtz78)登场的地方。与 MIMO 一样，它已在商业应用中使用，但军事应用的用例颇为独特。由于传播时延，所有接收天线阵列收到的信号在相位与幅度上会略有差异。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/bb6ad3c8-0f3e-447b-87bc-67162d8ee3fd_1531x1043.png)

当多个方向上存在目标与信号时，数字波束赋形让系统得以聚焦于某一特定信号。各接收天线通过给先收到信号的天线引入纳秒级时延，使其时序同步到某一特定方向与距离。一旦所有信号在该特定距离与方向上完全同步，各接收天线的输出便可直接相加。处于这些天线「焦点」上的目标信号会被放大，而其他所有目标则沦为噪声、可被滤除。更详细的解释可观看[这个视频](https://www.youtube.com/watch?v=A1n5Hhwtz78)。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/96a49429-60a0-41b1-a189-72f9f58bb78f_1822x962.png)

波束赋形可以是模拟的，也可以是数字的。数字波束赋形的优势在于：每个处理单元都能拿到原始数据，通过对数据集的分析用数字信号处理来操控波束指向。这一处理可以同时对许多不同焦点并行进行，从而能够探测由更小目标组成的蜂群，例如数千架无人机与导弹。

转向融合架构，要求遍布机身各处的天线阵列能够被集中处理，而不是在每个天线阵列处各自处理。请对比当前一代架构（第 1 张图）与下一代架构（第 2 张图）。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/15beec3c-4e79-49fb-aa31-257240a877d7_1427x656.png)
![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1e515dec-49f7-4bbd-9e43-1ac7f2f7a4af_1423x717.png)

下一代架构对 IO 的要求大幅提高。来自传感器的全部数百 GB/s 数据必须先送到一个中央交换机，再分发到各类处理单元，这对网络 IO 速度的要求是爆炸式的。

这一思路的关键在于：与其各自独立地建造孤立系统，不如构建一张可以协同完成所有任务的大型网络——而这只有在极高速度、极高效率的网络之下才可能实现。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/4c550d2f-392e-4b9f-95c4-7be1d059f953_1423x838.png)

这正是 [Ayar Labs 的共封装光学](https://www.semianalysis.com/p/ayar-labs-co-packaged-optics-revolution?s=w)切入的地方。作为背景复习，可参阅[我们此前关于该公司的报告，其中详述了其面向数据中心的共封装光学方案](https://www.semianalysis.com/p/ayar-labs-co-packaged-optics-revolution?s=w)。光学 IO 的效率远高于电学形态。Ayar Labs 与 Lockheed Martin 正在研究将 TeraPHY 共封装光学 IO 小芯片与 RFIC 集成，以构建具备这些能力的先进封装。理论上，传感器、交换机与处理单元都可以使用这种光学 IO，从而大幅降低功耗并提升带宽。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/4de7a67e-b8e5-48a4-9478-c976377e8c10_1427x803.png)

采用共封装光学 IO 的好处不止于更低功耗与更高带宽。其一是电磁干扰（EMI）大幅降低。基于铜的电互连必须应对更强的辐射、地球磁场或敌方对抗措施所带来的干扰，这些干扰会导致传输信号出错。部署于航空航天环境的铜缆布线需要大量屏蔽来防止这些问题。

此外，高速铜信号存在传播损耗与信号衰减问题，因此线缆走线长度受限。与损耗相关的问题靠更细线规（即更粗的线径）来补偿。这给航空航天应用带来麻烦：一架飞机上要布设成百上千根线缆。如果每一段走线都是带 EMI 屏蔽的粗线，这些布线将占掉可观的空间与重量预算。

这两个问题在共封装光学 IO 面前都大为缓解。玻璃光纤几乎不需要屏蔽，因为它对绝大多数 EMI 免疫。玻璃纤维更细、更轻、也更柔韧。这些特性使布线可以进入紧凑得多的空间。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/89c7b45a-e5cd-49b0-b358-4b69e1e533e8_757x772.png)

Ayar Labs 与 Lockheed Martin 将共封装光学 IO 与现有最先进的板载中（mid-board）光收发器做了对比。对比显示，共封装光学在功耗、面积、误码率上更低，性能更高。板载中收发器目前用于一些军事应用，但我们不确定具体用在哪里。各家供应商的财报里都有一个「国防」应用的筐。

这项研究的另一个有意思之处，是它可能与 Ayar Labs 当前在数据中心方向的推进形成协同。数据中心出于脆弱性与可靠性顾虑，一直对共封装光学持观望态度。Ayar Labs 将得以在一个苛刻得多的应用中验证其技术。湿度、G 力、激光器寿命与温度 swing（摆动）仍是重大挑战，但进展令人乐观。其中一些经验教训可以反哺规模大得多的数据中心通信市场。

如果你读得开心，请分享本文！这能帮助我们持续产出独特而小众的内容！

[分享](https://newsletter.semianalysis.com/p/the-future-of-military-sensing-and?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[赠送订阅](https://newsletter.semianalysis.com/subscribe?&gift=true)

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

[发表评论](https://newsletter.semianalysis.com/p/the-future-of-military-sensing-and/comments)
