---
title: "新一轮对华光刻管制的缺口——ASML、SMEE、Nikon、Canon、EUV、DUV、ArFi、ArF Dry、KrF 与光刻胶"
title_en: "The Gaps In The New China Lithography Restrictions – ASML, SMEE, Nikon, Canon, EUV, DUV, ArFi, ArF Dry, KrF, and Photoresist"
date: 2023-01-29
source: https://newsletter.semianalysis.com/p/the-gaps-in-the-new-china-lithography
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 新一轮对华光刻管制的缺口——ASML、SMEE、Nikon、Canon、EUV、DUV、ArFi、ArF Dry、KrF 与光刻胶

> 原文：[The Gaps In The New China Lithography Restrictions – ASML, SMEE, Nikon, Canon, EUV, DUV, ArFi, ArF Dry, KrF, and Photoresist](https://newsletter.semianalysis.com/p/the-gaps-in-the-new-china-lithography) · SemiAnalysis

[经济冷战](https://www.semianalysis.com/p/china-and-usa-are-officially-at-economic)仍在延续。数十年来，中国国家支持的企业窃密、黑客攻击、倾销，以及以市场准入换取强制技术转让等严苛做法，招致了针对中国获取**21 世纪最重要产业——半导体**的报复性制裁。去年 10 月，美国对 [AI 芯片](https://www.semianalysis.com/p/how-chinas-biren-is-attempting-to)和[半导体制造设备](https://www.semianalysis.com/p/china-and-usa-are-officially-at-economic)实施了限制，但并未完全解决所有关切。

过去几个月里，[其中一部分缺口得到了部分弥补](https://www.federalregister.gov/documents/2022/12/19/2022-27151/additions-and-revisions-to-the-entity-list-and-conforming-removal-from-the-unverified-list)，但最大的缺口仍未闭合。美国在晶圆制造设备领域居于领先地位，在沉积、刻蚀、过程控制、CMP 和离子注入等环节均占多数份额，但 Applied Materials、Lam Research、KLA 等许多美国设备厂商一直在抱怨：美国的限制措施会让荷兰 ASM International、日本 Tokyo Electron 等海外竞争对手攫取市场份额，从而钝化技术限制的冲击。

此外，[全球最大的设备制造商 ASML](https://www.semianalysis.com/p/asml-and-the-semiconductor-market) 一直态度强硬地拒绝跟随美国的技术限制。

> 作为一家总部位于欧洲的公司，我们的系统中美国技术含量有限，ASML 可以继续从荷兰向中国出货所有非 EUV 光刻系统。
>
> [Peter Wennink，ASML CEO](https://www.asml.com/-/media/asml/files/investors/financial-results/q-results/2022/q3/investor-call-prepared-remarks.pdf?rev=39ae2eaeab37427a88d128a8ccc4d0cf#:~:text=Net%20income%20in%20Q3%20was,level%20of%203.4%20billion%20euros.)

尽管 ASML 的光源工程是由其收购的美国公司 Cymer 在圣迭戈完成的。

![](https://substack-post-media.s3.amazonaws.com/public/images/de949071-ea42-4cc4-becc-47fe415089f5_3435x1902.png)

此外，运行光刻设备所需的光罩相关软件和 OPC 软件同样是在美国开发的。虽然凭借设备中较高的美国技术含量，美国当然有手段让 ASML 遵从技术限制，但美国选择了外交路线。

过去几个月，美国、日本和荷兰一直在就限制中国获取光刻设备进行磋商。上周五，[有新闻披露三国已就光刻设备的某些限制达成一致](https://www.bloomberg.com/news/articles/2023-01-27/japan-netherlands-to-join-us-in-chip-export-controls-on-china)。问题在于：这些限制走得多远、包含哪些内容？据我们了解，这些限制极其有限，只涉及 ArFi 光刻机。该协议目前仍停留在口头层面，但我们相信三国已同意在此基础上推进。据称协议还包含一些非光刻类设备。今天我们将讨论新达成的光刻限制在设备、化学品和零部件供应链上留下的诸多巨大缺口。

## **设备供应链**

限制中国获取半导体的首要途径是设备。尽管三方协议封堵的是 DUV 光刻，但协议完全没有说明限制的回溯范围。DUV 是一个非常宽泛的技术类别，包括氟化氪（KrF）、氟化氩（ArF）和氟化氩浸没式（ArFi）光刻。

![](https://substack-post-media.s3.amazonaws.com/public/images/9e9b6aad-c10d-47a6-abdb-f8aef3356e03_685x368.png)

Nikon 于 1988 年发布了首款 DUV 设备 NSR-1505EX，采用 KrF 光刻。其初始分辨率为 500nm，但随着时间推移已升级到[250nm 分辨率、100nm 套刻精度](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=b819ca5055576d79426c7b9d7b9652334e4a7dac)。美、荷、日新达成的限制并不覆盖这么老的技术。另一端，ASML 2022 年发布的 NXT 2100i 套刻精度为 1.5nm，可以图形化先进节点所需的最小特征。

如果目标是阻止中国获得 14nm、7nm 或 5nm 制程技术，那么禁令必须覆盖到能够加工这些节点特征的不同档次设备。例如，TSMC 的 16nm 和 12nm 制程技术的最小金属间距为 64nm。TSMC 的 7nm 制程技术最小金属间距为 40nm。TSMC 的 5nm 制程技术最小金属间距为 28nm。

任何对光刻设备的禁令都必须以这些最小金属间距作为禁止设备的规格基准。

在[瑞利判据方程](https://www.asml.com/en/technology/lithography-principles/rayleigh-criterion)（CD = k1 · λ / NA）中，CD 是关键尺寸（critical dimension），即可实现的最小特征尺寸。λ 是所用光的波长。NA 是光学的数值孔径，决定了光学系统可以收集多少光。最后，k1（即 k1 系数）是一个取决于芯片制造过程诸多因素的系数。[光刻的物理极限是 k1 = 0.25。](https://www.asml.com/en/technology/lithography-principles/rayleigh-criterion)

自对准四重图形化（SAQP）通常被认为是在经济上把一代 DUV 光刻「压榨」到极限的方式。虽然还存在更复杂的光刻方案，我们只讨论今天在经济上可行的做法。TSMC 和[中国的 SMIC 已经在没有 EUV 的情况下，用氟化氩浸没式（ArFi）光刻加 SAQP 实现了 7nm 制程技术](https://www.semianalysis.com/p/chinas-smic-is-shipping-7nm-foundry)，但这并不是经济上可实现的极限。

TSMC N5 所用的 28nm 最小金属间距可以不用 EUV 制造。采用 ArFi 光刻（NA=1.35，λ=193nm）的 SAQP 可以在 k1=0.391 下产出该特征尺寸。如果目标是阻止中国实现 5nm 制程技术，那么 ArFi 的出货必须被封堵。ASML 和 Nikon 都能制造可以实现 28nm 最小金属间距的 ArFi 光刻机。虽然经济性不如 EUV，但对中国这样的国家行为体而言，这一差距并非不可逾越。

如果目标是阻止中国实现大批量 7nm 制程技术，那么所有能够实现 TSMC 7nm 级制程技术所用的 40nm 最小金属间距的设备都必须被封堵。新限制会涵盖 ArFi 光刻，但还需要延伸得更远。采用干式氟化氩 ArF 光刻（NA=0.93，λ=193nm）的 SAQP 可以在 k1=0.385 下产出该特征尺寸。同样，这不会像 Intel、TSMC 和 SMIC 用 ArFi DUV 做的「7nm」那样经济，但它是可以实现的，尤其是考虑到国家安全的重要性。其成本差[远低于美国一座核电站所获得的补贴](https://apnews.com/article/business-environment-united-states-georgia-atlanta-7555f8d73c46f0e5513c15d391409aa3)。

![](https://substack-post-media.s3.amazonaws.com/public/images/971e19ab-b0eb-454d-af31-224e6af0f77c_2048x932.jpeg)

如果目标是阻止中国扩充其大批量 14nm 制程技术，那么所有能够实现 64nm 最小金属间距的设备都必须被封堵——TSMC 的 16nm/12nm 和 Samsung 的 14nm 等节点使用的正是这一间距。这些限制（若得到充分执行）不仅应涵盖 ArF 光刻设备，还需要进一步延伸到某些类型的氟化氪（KrF）设备。氟化氪的 λ=248nm，但其镜头组有多代产品，NA 逐代从 0.6 提升到 0.8 再到 0.93。

采用最先进 KrF 光刻（NA=0.93，λ=248nm）的 SAQP 可以在 k1=0.48 下产出该特征尺寸。采用中档 KrF 光刻（NA=0.8，λ=248nm）的 SAQP 可以在 k1=0.413 下产出该特征尺寸。用 ASML、Nikon 或 Canon 的设备，这些都是非常容易实现的。再说一次，经济性不会最优，但即便 14nm 级节点的光刻成本翻倍，每片晶圆的成本也只会增加约 19%。以中国给予本土企业的国家补贴力度，这在经济上已经可行。

应当指出，监管方在决定限制哪些设备时还应关注套刻精度（overlay）规格。在光刻中，套刻指制造过程中不同层之间的对准精度，即一层图形对准到另一层的定位精度。我们的每个算例都使用了自对准四重图形化（SAQP），意味着需要对准 4 层光刻图形，因此套刻控制至关重要。

ASML 最先进的 EUV 光刻机套刻精度为 1.1nm。上一代 3400C——2021 年 ASML 出货的主力 EUV 设备——套刻精度为 1.5nm，还不如 ASML 最先进的 DUV 设备 2100i。今天我们不会过多展开我们认为 14nm、7nm 和 5nm 出口管制的套刻精度门槛应画在哪里，那对大多数读者来说过于繁琐。

## **化学品供应链**

新出口管制的下一个缺口是化学品供应链，即光刻胶（photoresist）。我们[在此对光刻胶做过深度解析](https://www.semianalysis.com/p/lam-research-tokyo-electron-jsr-battle)，概括地说：光刻设备需要光刻胶才能在晶圆上图形化出特征。全球绝大部分光刻胶由[少数几家日本公司](https://www.semianalysis.com/p/lam-research-tokyo-electron-jsr-battle)制造，美国的 Dupont 是差距悬殊的第四名。光刻胶的化学配方在许多情况下需要针对终端客户的光刻类型、制程节点、特征类型和特征尺寸做大量精细调校。此外，[用于涂布、显影和烘烤光刻胶的设备也完全是日本货](https://www.semianalysis.com/p/lam-research-tokyo-electron-jsr-battle)。

如果日本限制光刻胶出货，[世界上任何国家都可能被切断全部光刻、进而切断半导体制造](https://www.semianalysis.com/p/austrias-silent-monopolies-on-advanced)。光刻胶完全不受限制，是政府监管尚未考虑到的重大缺口。

仅 SMIC 一家就已经拥有超过一百台 DUV 设备。这些设备可以重新组织调配，转用于不同制程节点的制造。SMIC 仅凭现有 DUV 设备就可以实现每月远超 100,000 片晶圆的 7nm 代工产能。这已经高于 Samsung 与 Intel 先进节点（<=7nm）代工产能之和。如果华虹（HuaHong）、上海华力（Shanghai Huali）、YMTC、CXMT、GTA Semi、Nexchip、燕东（Yandong）、Nexperia、CR Micro、Sien、Fulsemi、SEMC、NSEMI 等中国厂商的 DUV 设备全部划归 SMIC 调配，他们能建成的 7nm 产能将远超 TSMC 的 7nm。

如果目标是限制中国制造先进半导体，仅封堵新设备的出货是不够的。光刻胶的出货也必须停止，因为西方政府并不知道现有的 DUV 设备正在被用于哪个制程节点。

## **零部件供应链**

这就引出最后一个缺口：零部件供应链。DUV 设备必须由 ASML、Nikon 和 Canon 定期提供备件维修服务。如果目标是将中国的先进节点产能遏制住，这些设备的服务也必须被封锁。

虽然中国的光刻领军企业 [SMEE 已被列入制裁名单](https://www.federalregister.gov/documents/2022/12/19/2022-27151/additions-and-revisions-to-the-entity-list-and-conforming-removal-from-the-unverified-list)，但 SMEE 已出货可工作的 I-Line 光刻设备。其氟化氩 DUV 光刻机对前道晶圆制造而言仍未达到量产就绪状态。这并不意味着他们无法追赶。ASML 光刻供应链中的许多企业（如 Zeiss）仍在通过合资和技术转让继续在华扩张。考虑到中国的军民融合，这些技术从缝隙中流入 SMEE 之手是轻而易举的事。

最后，光罩相关设备也完全没有限制，这同样是一个缺口。

[分享](https://newsletter.semianalysis.com/p/the-gaps-in-the-new-china-lithography?utm_source=substack&utm_medium=email&utm_content=share&action=share)

上游零部件供应链限制的缺失，是美日荷三方协议的一个重大缺口。如果目标是限制 5nm、7nm 和 14nm 制程技术，那么 KrF 和 ArF 光刻设备、光刻胶以及子部件都必须加以限制，否则中国将能够重新配置现有设备，并加速光刻设备的国产化进程。
