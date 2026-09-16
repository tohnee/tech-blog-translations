---
title: "拥抱混沌：半导体制造与光刻的不完美艺术"
title_en: "Embracing Chaos: The Imperfect Art of Semiconductor Manufacturing And Lithography"
subtitle: "5 只做多标的、Intel EUV 再度延期，以及更多"
date: 2023-02-27
source: https://newsletter.semianalysis.com/p/embracing-chaos-the-imperfect-art
crawled: 2026-09-15
authors: ["Dylan Patel", "Afzal Ahmad"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 拥抱混沌：半导体制造与光刻的不完美艺术

> 原文：[Embracing Chaos: The Imperfect Art of Semiconductor Manufacturing And Lithography](https://newsletter.semianalysis.com/p/embracing-chaos-the-imperfect-art) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**5 只做多标的、Intel EUV 再度延期，以及更多**

世界上一切制造业，都是靠把多个具有不同公差与波动范围的工艺和系统层层叠加，才能持续产出合格产品。这一点在半导体制造上体现得最为极致——它是全球最复杂、容错率最低的单一制造工艺。尽管挑战重重，半导体行业还是层层堆叠起数百个抽象层，让软件世界看到一致的器件。而随着这些层层剥开，海量的波动便显露出来。

晶圆厂产出的每一颗芯片，即便是同一设计，在任一给定性能水平下的功耗都不相同。许多芯片会带有缺陷，最终以屏蔽若干「核心」和 IO 的方式收获良率（yield harvested）。例如，所有 Nvidia A100 和 H100 GPU 出厂时都屏蔽了约 10% 的芯片。原因就埋在现代高性能半导体数十亿颗晶体管与互连之中的制造波动——它们由数千个不同的工艺步骤造就。每颗晶体管的开关所需电压各不相同。每一段互连、通孔和接触孔的电阻也各不相同。

![](https://substack-post-media.s3.amazonaws.com/public/images/1e81b104-c738-4b52-9879-ad963ad36368_2000x1125.png)

来看 EUV 光刻——它是制造先进半导体的核心技术之一。我们的读者大概不需要光刻速成课，但如果你需要，请看这些文章。[1](https://www.semianalysis.com/p/lam-research-tokyo-electron-jsr-battle), [2](https://www.semianalysis.com/p/die-size-and-reticle-conundrum-cost?utm_source=%2Fsearch%2Fasml&utm_medium=reader2), [3](https://www.semianalysis.com/p/i-semiconductor-the-regionalization?utm_source=%2Fsearch%2Fasml&utm_medium=reader2), [4](https://www.semianalysis.com/p/lithography-intensity-and-long-term?utm_source=%2Fsearch%2Fasml&utm_medium=reader2), [5](https://www.semianalysis.com/p/asml-and-the-semiconductor-market?utm_source=%2Fsearch%2Fasml&utm_medium=reader2), [6](https://www.semianalysis.com/p/the-gaps-in-the-new-china-lithography?utm_source=%2Fsearch%2Fasml&utm_medium=reader2), [7](https://www.semianalysis.com/p/austrias-silent-monopolies-on-advanced)。从 EUV 光源到镜组系统，到光掩膜，到对准系统，到晶圆载台，到光刻胶化学配方，到涂胶显影机，到量测，再到每一片晶圆，无不如此。

![](https://substack-post-media.s3.amazonaws.com/public/images/121fb98e-da70-45c5-9cb2-c93758e73f03_1939x1094.png)

EUV 是一个充满复杂性、不确定性与不完美、却实实在在运转着的工艺。TSMC、Samsung 和 SK Hynix 都已在不同规模上量产 EUV。Intel 也私下表示其 Intel 4 工艺节点已具备 EUV 光刻的量产就绪。对此我们并不太相信：我们获得的内部文件显示，Intel 第一款大规模采用 EUV 的产品 Meteor Lake 再度延期，「可发货」（ready-to-ship）日期至少推迟到 2023 年第 52 周。这表明 Intel 在把一个量产级设计导入 EUV 工艺技术上正遭遇挑战。

[Share](https://newsletter.semianalysis.com/p/embracing-chaos-the-imperfect-art?utm_source=substack&utm_medium=email&utm_content=share&action=share)

![](https://substack-post-media.s3.amazonaws.com/public/images/c1679b9c-2614-4c1d-ae40-1709c752fa81_978x447.png)
*Frederick Chen*

单个工艺步骤中微小波动的累积，可能叠加成与期望结果的显著偏差，最终导致成品失效。例如，飞机发动机的激光钻孔或精密铸造出现问题，可能导致一片涡轮叶片失衡。失衡的涡轮会带来额外振动，降低效率，最终使发动机提前磨损、提前失效。而现在请想想：飞机制造发动机在制造精度、工艺波动容忍范围、化学、物理和步骤数量上都比半导体简单得多。

先进制程晶圆厂里的大多数设备，可以以区区几个原子的精度沉积、抛光或刻蚀材料。在成千上万台设备/工艺步骤构成的链条中，后续每一台设备的工艺参数都会被不断微调。这些条件与微调由工艺控制（process control）决定。工艺控制包括量测/检测设备以及控制它们的软件。晶圆厂每年在工艺控制上的花费超过 200 亿美元。

如果一台刻蚀机有四个腔体，工艺控制智能系统与厂内网络调度会根据该工艺步骤的设备可用性和良率指标，决定把晶圆送去四个腔体中的哪一个。系统还会调整腔体状态，并监测是否需要维护。事实上，[即便是成熟制程晶圆厂，也会针对每一片晶圆或每一批次微调设备参数](https://www.semianalysis.com/p/lynceus-inline-real-time-ai-based)，以把每个特征累积的公差范围控制在最低可行规格之内。

为了强调这一点：波动与不确定性无处不在，以至于量产晶圆厂会用多台不同的 EUV 光刻机测试同一张光掩膜。这些量产厂可能只把那张光掩膜放到某一台良率最高或缺陷最易管控的特定 EUV 光刻机上运行。注意，一个现代 TSMC 5nm 设计约有 81 张掩膜版，而一座晶圆厂一年要运行数十乃至数百个设计。此外，掩膜与 EUV 光刻机的匹配还要定期重测，因为掩膜必须半定期地进行维护或重制。

![](https://substack-post-media.s3.amazonaws.com/public/images/b7e734e9-d53f-4794-973d-7c573bee1acf_12000x6750.png)

类似地，即便同类量测/检测设备产自同一工厂、同一批出货，由于设备间波动（tool-to-tool variation）在测量仅几个原子大小的特征时实在太大，它们也可能只被用于特定层次。事实上在某些情况下，误差预算（叠加波动）的 25% 以上被量测与检测成像工具自身的不确定性吃掉。这些本应为在制程中调整设备和工艺提供数据的工具，自身也极不完美——就像在黑夜里飞行。

晶圆厂必须跨越重重门槛，才能相信自家量测设备给出的确实是对其加工晶圆真实情况的准确描绘。许多误差和缺陷源自 EUV 设备与工艺。在相同剂量下，EUV 打到晶圆上的光子数只有 DUV 的 1/14。因此，光子数量更少、分布更随机，带来了数量可观的随机性（stochastic）缺陷。EUV 光刻中的随机性指的是图形中可能出现的随机波动。

![](https://substack-post-media.s3.amazonaws.com/public/images/a2930d03-9015-46bb-a17f-5176a7842f7f_12000x6750.png)

这些随机性缺陷是晶圆制造行业价值数十亿美元级的问题。行业斥资数百亿美元，用量测和检测工具来刻画波动。所得数据再以逐晶圆、逐设计、逐设备的视角，反馈用于修正工艺或设备参数。没有两片晶圆、两台设备或两个设计是完全相同的，一张晶圆厂网络中每一处都有海量的调整与优化。

![](https://substack-post-media.s3.amazonaws.com/public/images/5dfc07f6-a1fc-4bb4-87c0-81a24684fc95_12000x6750.png)

一座超级晶圆厂（gigafab）要在约 25 万片在制品晶圆上运行数千个步骤：每月约有 10 万片完成，又有新的 10 万片开始。其调度、优化与决策的物流挑战怎么强调都不为过。

> 随机性不只是随关键尺寸线性增长，而是作为我们所打印关键尺寸的百分比呈指数增长。
>
> Chris Mack

![](https://substack-post-media.s3.amazonaws.com/public/images/6be20d42-6200-48a6-959c-23e2497668b7_12000x6750.jpeg)

我们有机会与 Chris Mack——人称「光刻大师」（Litho Guru）——聊了行业面临的诸多难题以及已发展出的一些解决方案。不了解的读者可以了解一下：Chris Mack 曾在 SPIE 光刻与先进图形化会议上以一辆 Lotus Elise 打赌 EUV 无法在某个日期前就绪，此举广为人知。另一个有趣的故事是，他曾在该会议上制作并戴着一顶红色的「Make EUV Great Again」帽子当玩笑。

SPIE 光刻与先进图形化会议就在本周举行。我们定期参会，因为它涵盖光刻胶、光掩膜、量测、检测和光刻领域的全部最新进展。如果你本周也在 SPIE 光刻与图形化会议现场，请告诉我们，可以当面聊聊！

![](https://substack-post-media.s3.amazonaws.com/public/images/852c8072-f258-46f6-b1df-e75308a68ec1_12000x6750.png)

波动与缺陷主要有几大类。它们都可能增大导线电阻、栅极漏电，甚至造成短路或其他令芯片报废的缺陷。

## **套刻（Overlay）/ 局部边缘位置误差**

如前所述，TSMC 5nm 工艺约有 81 张光掩膜。这意味着 81 次完整走完整个光刻流程。此外，其间还穿插数千个其他制造步骤。

![](https://substack-post-media.s3.amazonaws.com/public/images/9d5f9e7d-fa99-4bd9-aaf8-a5cffb622d03_1017x291.jpeg)

套刻（overlay）或局部边缘位置误差（local edge placement error）是指一次沉积/光刻/刻蚀循环所产生的特征，摆放到前一轮循环已有特征之上时的位置波动。某一层 +1nm 的对位偏差，叠加下一层 -1nm 的对位偏差，累积起来就是特征位置上 2nm 的差异。这类误差会在许多步骤中不断累积叠加，后果可能是灾难性的。

我们此前讨论过的一个例子是 [TSMC 与 Intel 的自对准接触孔](https://www.semianalysis.com/i/100427011/tsmc-nm-self-aligned-contacts-nb-paper)，它通过让图形化特征对位置误差更不敏感，来缓解套刻误差的部分叠加。

## **局部关键尺寸均匀性（CDU）**

另一大波动来源是局部关键尺寸均匀性（critical dimension uniformity）。理想情况下，彼此相邻的特征应当均匀一致，但很多时候并非如此。在这个例子里，让我们把视野放大到连接芯片各金属层的通孔和接触孔上。

![](https://substack-post-media.s3.amazonaws.com/public/images/0754a7fa-d2eb-416a-abf2-eb47ff04f520_2000x1125.png)

当这些随机性波动大到一定程度，就会导致缺陷：特征缺失或粘连——接触孔缺失、桥连，以及线条的断裂，还有线与线之间的间距变化。而如果一颗芯片上有 1000 亿个接触孔/通孔，其中一个缺失，整颗芯片就报废了（当然会内建一定冗余）。对于直径只有几十纳米的特征，行业必须做到大约千亿分之一（one in 100 billion）的缺陷率。

## **线边缘粗糙度（LER）**

线边缘粗糙度（Line Edge Roughness，LER）是特征边缘的波动。LER 可以定义为图形化特征（如线条或沟槽）边缘的粗糙或不规则，它可能导致实际关键尺寸偏离设计值。

LER 对最终产品的性能和可靠性影响重大。例如，对晶体管栅极而言，LER 的波动会影响晶体管的电学特性，导致漏电流增大、器件性能下降等问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/b1e48cd7-9928-4434-ab5d-86995a3cb2ec_448x166.jpeg)

## **线宽粗糙度（LWR）**

LWR 可以定义为特征（如线条或沟槽）宽度上的粗糙或不规则，它同样可能导致关键尺寸偏离设计值。对金属互连而言，LWR 的波动会影响线条电阻，导致功耗上升或器件性能下降等问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/95ae0c26-8d16-437b-85ac-d324aa006d5d_599x284.jpeg)

## **光学邻近效应校正（OPC）**

光掩膜可以看作芯片的镂空模板。光掩膜由电子束图形化，放入光刻机内。光掩膜随后吸收或散射光子，或者让光子透过到达晶圆——晶圆上的图形便由此产生。

OPC（光学邻近效应校正）旨在纠正光刻过程中图形化特征发生的畸变或变形。通过对这些畸变进行补偿，制造商可以在图形化特征上实现更高的精度与一致性，从而提升最终产品的性能与可靠性。下图是一种早期的 OPC 形式，配合更先进的条件——包括在 TSMC 大规模使用的[曲线 ILT 掩膜](https://www.spiedigitallibrary.org/conference-proceedings-of-spie/11855/118550U/Curvilinear-masks-an-overview/10.1117/12.2601916.short)。

![](https://substack-post-media.s3.amazonaws.com/public/images/3477b9e0-a22b-4a3a-8656-37d274e0f119_997x442.png)

我们还将分享 5 家可能从光刻的混沌与工艺控制艺术中获得超额收益的上市公司。如果你猜是 ASML 或 KLAC——都不是。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
