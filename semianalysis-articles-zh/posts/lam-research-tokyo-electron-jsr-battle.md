---
title: "Lam Research、Tokyo Electron、JSR 在 $5B+ 的 EUV 光刻胶与涂布显影机市场激战 – CAR vs MOR vs 干式光刻胶"
title_en: "Lam Research, Tokyo Electron, JSR Battle It Out In The $5B+ EUV Photoresist, Coater, and Developer Market - CAR vs MOR vs Dry Resist"
date: 2021-11-18
source: https://newsletter.semianalysis.com/p/lam-research-tokyo-electron-jsr-battle
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Lam Research、Tokyo Electron、JSR 在 $5B+ 的 EUV 光刻胶与涂布显影机市场激战 – CAR vs MOR vs 干式光刻胶

> 原文：[Lam Research, Tokyo Electron, JSR Battle It Out In The $5B+ EUV Photoresist, Coater, and Developer Market - CAR vs MOR vs Dry Resist](https://newsletter.semianalysis.com/p/lam-research-tokyo-electron-jsr-battle) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

EUV 光刻以光刻图形化分辨保真度的阶跃式提升，从根本上推动了半导体行业向前。分辨率的提升并非免费。向 EUV 过渡还必须伴随许多相关技术的进步。这些变化涵盖光罩制造、光罩膜（pellicle）、沉积、刻蚀机、硬掩模和光刻胶。虽然 EUV 本身由 ASML 主导，但这一转变在制造流程的相邻环节——尤其是光刻胶行业——掀起了一场数十亿美元级的高风险之战。

日本在这一领域长期称王：Tokyo Electron（TOELY / 8035.JP）占据 EUV 光刻胶涂布显影机（coater/developer）100% 的份额。凭借涂布显影机垄断地位带来的刻蚀与清洗关联订单，这个市场**当前年化营收已达 $5B**！此外，其他日本公司早已以约 75% 的份额垄断了光刻胶市场。JSR（4185.JP）和 Tokyo Ohka Kogyo（4186.JP）是领军者。它们出货了绝大多数专用于 EUV 的化学放大光刻胶。然而，这些市场正遭到 Lam Research 的攻击。

本文将包含免费的技术细节讲解，但结论部分将设付费墙，供投资者和好奇心旺盛的读者参考。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c68dbba2-a33a-487e-b97e-886f26a0609f_907x1024.png)

在深入即将到来的光刻胶战争的细节之前，先对光刻图形化工艺做一个简单的概览。一切从清洗晶圆开始，确保没有尘埃微粒或前道工序残留化学品之类的异物。在更先进的节点上，光刻工艺之前会在晶圆上沉积若干底层、中间层和硬掩模。这样沉积是为了让最终刻蚀能更精确地受控，这个话题改日再谈。

最简单的光刻形式称为湿法光刻胶单次图形化。清洗后的晶圆被放入 Tokyo Electron 的涂布显影机。设备在晶圆上方沉积**化学放大光刻胶（chemically amplified resist，CAR）**。CAR 悬浮于液体溶液中，晶圆被高速旋转以完成涂布。旋转过程也通过离心力甩掉大部分液体，留下一薄层光刻胶。随后还有一道叫前烘（prebake）的工序，用来烘干最后一点液体，某些情况下还为接下来的反应做化学准备。

晶圆进入 ASML 光刻设备，光线穿过光罩照射到光刻胶上，引发化学反应。晶圆再被送回 Tokyo Electron 的涂布显影机。显影部把光刻胶洗掉。如果这是正性光刻胶，被曝光的部分会发生反应变成可溶，从而被洗掉。如果是负性光刻胶，被曝光的部分反应后不再可溶，未曝光的光刻胶被洗掉。这只是光刻工艺本身，此外还有多重图形化技术、刻蚀、侧墙（spacer）等相关工艺，但今天我们先聚焦光刻流程。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/344aa06d-99d0-4d01-9af8-38d9ba33592e_1024x578.png)

上述光刻胶工艺几十年来运转得极其出色，但正开始遭遇重大问题。这些问题涉及线边缘粗糙度（line edge roughness）、灵敏度、分辨率和产能。EUV 光刻以相对 DUV 极短的波长轰击晶圆。更短波长的极紫外光，代价是产生起来困难得多。

[EUV 存在产能问题](https://semianalysis.substack.com/p/asmls-euv-tools-have-a-throughput)。问题的核心在于：相同剂量下，打到晶圆上的光子数只有 DUV 的 1/14。因此 EUV 的剂量必须提高，而这又通过拉长曝光时间降低了产能。产能问题导致晶圆产出受到严重限制、成本上升。为了最大化产能，剂量被压到最低，这带来了与图形保真度相关的一系列问题。

一个解决方案是多买机器、调高光源功率。机器单价约 $150M，极其昂贵，而 ASML 的产出能力高度受限。提高光源功率难度极大，而且 ASML 的功率提升路线图远远跟不上新节点上 EUV 层数爬坡的速度。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

除了曝光光刻胶的光子更少，EUV 光刻胶对光子的吸收也更少。光刻胶溶液是光酸产生剂（photo-acid generator）、附着促进剂和稳定剂极其精密的混合物。搞错了就是代价高昂的事故。[2019 年，台积电（TSMC）的 Fab 14B 在光刻胶上出了问题，让台积电实实在在地损失了 $550M。](https://www.anandtech.com/show/13975/tsmcs-fab-14b-photoresist-material-incident-550-million-in-lost-revenue) 到了 EUV 光刻胶，这种配比方更加严苛，而特定配比又导致吸收率更低。EUV 需求的高涨，加上「光子更少、吸收更少」的组合双拳，为传统光刻胶行业被颠覆创造了成熟的时机。干式光刻胶和 Lam Research 登场。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6e3607cb-ff96-4da3-ad1e-f3869fcc8f02_1024x578.png)

Lam Research 试图颠覆整个技术栈。他们不用旋涂式涂布的湿法光刻胶技术，而是用化学气相沉积工艺逐层沉积金属光刻胶。Lam Research 声称，干式光刻胶技术相对湿法光刻胶有若干优势。由于是致密沉积的金属，它不像湿法那样混入那么多其他化学品。这让金属光刻胶可以做到只含吸收剂。回到产能话题，这意味着每次晶圆通过的剂量与功耗减半。每台 EUV 设备的产能接近翻倍，将大幅降低成本。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/659552d8-3919-46a2-9fb0-291519453a3a_1024x575.png)

灵敏度不是唯一的优势。Lam 的干式光刻胶也用干法显影。湿法显影中，光刻胶被水或酸清洗。随着光刻胶被溶解，由于毛细作用力，已成形的线条等图形可能坍塌。随着最小金属间距（MMP）向 28nm 以内微缩，这日益成为问题。台积电的 N5 和 N4 制程节点的 MMP 分别为 30nm 和 28nm，当前出货的节点正贴着悬崖边缘。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/4ea78682-0267-4a2f-870a-c85f2a5091bd_1024x576.png)

不过，Tokyo Electron 手里还有创新。虽然他们承认现有的显影冲洗工艺在超过 28nm 间距（14nm 关键尺寸）时确实会导致线条坍塌，但他们已找到一种可微缩至约 24nm（12nm 关键尺寸）的新溶剂冲洗工艺。这将让湿法光刻胶方法得以延伸到 24nm。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/db7aa1a6-481c-4dde-832f-b609614ce163_1024x574.png)

但湿法光刻胶的问题并未全部解决，因为很难把光刻胶全部冲洗干净。如果光刻胶没有被冲净，后续工序就会出问题。残留的光刻胶可能让刻蚀出的孔彼此「接吻」，残留物也可能让这些孔彻底消失。Tokyo Electron 眼下的解决办法是干脆把残余光刻胶刻蚀掉。方案虽简单，却可能带来并发症：它会让孔变大或出现斜角。斜角效应未必是坏事，但也不是在所有用例中都最优。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a17f678a-7639-4552-bbe3-973e9774776a_1024x575.png)

Lam Research 声称，其工艺能以比现有湿法光刻胶工艺低得多的波动、更宽的工艺窗口，完成 5nm 节点使用的现有 32nm 间距。Lam Research 给出的硬数字无可辩驳。当晶圆厂追求特征尺寸、性能和功耗时，干法工艺整体更优。不过 Lam Research 做的对比可以说不太厚道，因为那是拿当前已部署的工具和工艺，去对比尚未问世的方案。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/dfadb23c-f4f5-4f52-8019-a83d0bf6a2e2_1024x574.png)

与此同时，Tokyo Electron 在竭尽全力延长现有装机群的寿命。Clean Track Lithius Pro Z 与每一台 ASML EUV 光刻机配套使用。在最初的 EUV 节点上，它已被证明可靠且高效，但随着行业推进到超越 EUV 单次图形化，化学放大光刻胶（CAR）显然正在触及极限。在其他条件相同的情况下，干式光刻胶将在先进制程和最小特征尺寸上胜出。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/02d576cf-c66f-40c6-ab6c-38d45b9d4495_1024x571.png)

Lam Research 最初瞄准的是 5nm IMEC 节点（对应代工厂的 3nm）上的应用。他们正与 IMEC 和 ASML 合作进一步开发该技术。Lam 还与 Samsung、Intel、台积电和 SKHynix 合作，推动该技术在逻辑节点和 DRAM 节点上的商业化。前景显然可期，SemiAnalysis 的渠道调研显示业界兴趣浓厚。

Tokyo Electron 和光刻胶在位者并未举手投降、坐等被颠覆。**这正是 Inpria 登场的地方。他们开发了一种新型光刻胶——金属氧化物光刻胶。** Inpria 于 2007 年脱胎于俄勒冈州立大学的研究中心。此后，Inpria 获得了 Samsung、Intel、Applied Materials、台积电、SKHynix、JSR 和 TOK 的重大投资。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5d42b95a-2591-4aa8-abad-9664c946a155_1024x571.png)

Inpria 的投资者个个是行业巨头，其中包括正与 Lam Research 合作商业化干式光刻胶的全部 4 家公司。名单还包括前面提到的两大 CAR 光刻胶领军者 JSR 和 TOK。JSR 在 2017 年和 2020 年参与了 Inpria 的融资轮，最近更是咬紧牙关，以 $514M 全资收购了该公司，对应估值 $742M。对一家在产生营收之前阶段开发化学品的工业公司来说，这个估值令人叹服。

很显然，这家公司拥有价值不菲的 IP。JSR 管理层向来保守，这足以说明正在发生的颠覆有多猛烈。光刻胶行业与 Tokyo Electron 已合作数十年，JSR/Inpria 正延续这种紧密无间的伙伴关系。双方共同开发光刻胶、工艺和涂布显影机。商业化将在下一个制程节点到来。

MOR 的流程步骤与现有光刻工艺类似。它仍悬浮于溶液中旋涂到晶圆上。同一台 Tokyo Electron Clean Track Lithius Pro Z 经升级即可使用。升级不需要多少资本开支，而且 CAR 或 MOR 光刻胶都能用。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9a01c013-18bf-4040-9b95-e3d8369fc007_1024x574.png)

MOR 仍是湿法的，这意味着某些问题依然存在，尤其是沉积的选择性。光刻胶在晶圆上潜在的不均匀沉积，会给曝光和烘烤工序步骤带来问题。Lam Research 干式光刻胶技术的最大优势之一，正是采用化学气相沉积（CVD）工艺来沉积光刻胶，从而对光刻胶的波动和厚度实现精细得多的控制。

光刻胶的厚度拿捏至关重要。如果是一层极薄的膜，光刻设备的性能和产能更高，因为需要曝光的光刻胶更少。反过来，薄膜在刻蚀时可能受损（负性光刻胶）。厚光刻胶层不仅导致产能下降，还可能引起图形坍塌，以及显影后光刻胶残留在孔中。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

Tokyo Electron 和 JSR 声称，他们为金属氧化物光刻胶开发了一种新的曝光后烘烤（post exposure bake）工艺，有助于提升光刻胶灵敏度。这意味着晶圆厂可以大幅降低对 EUV 光刻机的剂量需求，从而提高产能。Tokyo Electron 声称剂量可降低 38%，而 Lam Research 对干式光刻胶的声称是降低 50%。Tokyo Electron 还声称，新的曝光后烘烤能实现极其均匀的光刻胶厚度和低金属污染。如果这些声称成立，湿法光刻胶的寿命便可延长。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a8ea2546-0b7d-49c9-9c72-fe6b6dbf2918_1024x577.png)

同理，Tokyo Electron 和 JSR 有一套能对抗柱体坍塌问题的新湿法显影工艺。36nm 柱体经常坍塌，这是 DRAM 电容微缩的最大挑战之一。新显影工艺同样适用于更低的 EUV 剂量，并降低最终特征的厚度波动。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/0ed0b6f0-1188-4941-87b2-e584ceb3b749_1024x574.png)

凭借 MOR，Tokyo Electron 正致力于优化从涂布、烘烤、显影一直到刻蚀的整套工艺流程。他们声称已达到每平方厘米 0.1 个缺陷的缺陷密度。听着很美，但这个缺陷密度意味着每片 300mm 晶圆 70.6 个缺陷。先进制程晶圆上光刻工序要做 70 多次，N3 制程每片晶圆要做 20 多次 EUV 浸没式曝光。这些缺陷真的会层层叠加、摧毁良率。MOR 仍有一些坎要过。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/05a121db-b4dc-4673-ae18-0b8ccfba6b94_1024x578.png)

优化工艺流程的想法并非全然新颖。工艺模块优化是 Applied Materials 在其整套互连工艺流程和设备产品线上做了很久的事。这让 Tokyo Electron 得以凭借其在光刻胶涂布显影机上的主导地位，在刻蚀和清洗上抢占份额。Lam Research 同样想渗透光刻技术栈，提供从硬掩模、光刻胶沉积与显影一直到刻蚀的全套技术。多工序流程优化能带来更低的线边缘粗糙度、更好的均匀性、更少的缺陷，以及终端用户芯片和工艺更高的可靠性。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ad62cc53-6415-4080-a53c-253014bdcb0b_1023x541.png)

干法工艺的化学品消耗显著更低，旋涂光刻胶和显影环节尤其如此。光刻胶无需悬浮在溶液中即可沉积，也没有湿法工艺那样的甩料浪费。显影过程不需要用大量酸或超纯水冲洗晶圆来溶解光刻胶。这反过来让所需功耗减半。

这场战争谁胜谁负尚待分晓，MOR 和干式光刻胶各有好处。SemiAnalysis 掌握更多数据点，能让这场战局的走向更清晰。最重要的是：财务上意味着什么？
