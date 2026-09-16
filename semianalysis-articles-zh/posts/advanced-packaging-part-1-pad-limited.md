---
title: "先进封装第一部 – 焊盘受限设计、半导体经济性微缩的崩坏、异构计算与小芯片（chiplet）"
title_en: "Advanced Packaging Part 1 – Pad Limited Designs, Breakdown Of Economic Semiconductor Scaling, Heterogeneous Compute, and Chiplets"
date: 2021-12-15
source: https://newsletter.semianalysis.com/p/advanced-packaging-part-1-pad-limited
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 先进封装第一部 – 焊盘受限设计、半导体经济性微缩的崩坏、异构计算与小芯片（chiplet）

> 原文：[Advanced Packaging Part 1 – Pad Limited Designs, Breakdown Of Economic Semiconductor Scaling, Heterogeneous Compute, and Chiplets](https://newsletter.semianalysis.com/p/advanced-packaging-part-1-pad-limited) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

过去几年，先进封装在半导体领域日益成为热点。在这个多部分系列中，SemiAnalysis 将拆解这一大趋势。我们将深度解析支撑先进封装的各项技术，例如高精度倒装芯片（flip chip）、热压键合（thermocompression bonding，TCB）以及各种类型的混合键合（hybrid bonding，HB）。在深度解析的第一部中，我们聚焦这项技术的必要性，以及为什么整个行业正大举转向先进封装。

[在深度解析的第二部](https://semianalysis.substack.com/p/advanced-packaging-part-2-review)中，我们分析了各家代工厂、IDM、OSAT 和无厂设计公司的使用现状、设备采购情况与技术路线差异，涉及 Intel、台积电（TSMC）、Samsung、ASE、Sony、美光（Micron）、SKHynix 和 YMTC。[在深度解析的第三部](https://semianalysis.substack.com/p/advanced-packaging-part-3-intels)中，我们分析了 TCB 市场，包括 Intel 的角色、HBM、ASM Pacific、Besi 和 Kulicke and Soffa。在[第四部](https://www.semianalysis.com/p/the-future-of-packaging-gets-blurry)中，我们讨论了扇出（fanout）、有机中介层和硅桥（silicon bridge），作为绕开昂贵无源中介层的路径。第五部我们将深入混合键合，包括其用途、设计、落地，以及 Besi Semiconductor、ASM Pacific、Kulicke and Soffa、EV Group、Suss Microtec、SET、Shinkawa、Shibaura、Xperi 和 Applied Materials 各自的角色。我们还将深入电学测试（electrical test）与光学检测（optical inspection）生态。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9efabe53-b8a6-445b-aaa6-05988546ab77_1023x576.png)

先来谈谈先进封装的必要性。摩尔定律曾以狂奔的速度前进。自台积电在 32nm 上失手之后，直到当前的 5nm 制程节点，台积电的晶体管密度以每年 2 倍的速度增长。尽管如此，真实芯片的密度大约每 3 年才翻一倍。[这一放缓的部分原因在于 SRAM 微缩的停滞](https://semianalysis.com/apple-a14-die-annotation-and-analysis-terrifying-implications-for-the-industry/)、供电和热密度，但这些问题大多与数据的输入/输出有关。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d52a255f-a15e-4ace-9a45-3a3b786ec61f_1024x554.png)

芯片上数据的输入/输出（IO）是计算的命脉。把内存做到裸片上有助于通过减少通信开销来降低 IO 需求，但归根结底，这条微缩之路是有限的。处理器必须与外部世界交互来收发数据。摩尔定律让行业的晶体管密度大约每 2 年翻一倍，而 IO 数据速率的翻倍却要每 4 年一次。数十年来，晶体管密度与 IO 数据速率之间的这一差距已严重背离。[共封装光学（co-packaged optics）只是解决此问题的方案之一，而且它并非孤军奋战。](https://semianalysis.substack.com/p/intels-trojan-horse-into-the-foundry)

从根本上说，芯片必须容纳更多的通信点或 IO 才能跟上步伐。不幸的是，这方面上一次阶跃式的提升，还要追溯到 90 年代转向倒装芯片封装。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/56bd4d5b-44c8-41a5-9a9b-6e7c7fb0785e_936x527.png)

传统倒装芯片封装的凸点间距在 150 微米到 200 微米量级。这意味着在裸片底面，每个 IO 单元之间相距 150 到 200 微米。这方面有过一些渐进式改进：台积电的 N7 把凸点间距降到 130 微米，Intel 的 10nm 降到 100 微米。这些进步被称为精细间距倒装芯片（fine pitch flip chip）。并非要贬低这些进步——它们是更强处理器的巨大助推器——但 2000 年的封装技术与 2021 年的在本质上别无二致。

2000 年的一颗 250mm2 裸片与 2022 年的一颗 250mm2 裸片，在晶体管数量、能力和成本上有着天壤之别。按摩尔定律每 2 年翻一倍推算，晶体管数量应该有超过 2,000 倍的增长。现实显然没有这么美好，但晶体管数量的增加仍高出好几个数量级。而硬币的另一面，封装并没有享受到同等级别的增长。

AMD 在台积电 N7 节点上把凸点间距从约 200 微米缩到 130 微米，IO 只多了 2.35 倍。如前所述，Intel 在 10nm 上从约 200 微米缩到 100 微米，缩得稍多一些。即便如此，IO 也只提升了 4 倍。相对晶体管数量的增长，2.35 倍或 4 倍的提升不过是个舍入误差。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a49a8aec-a309-42df-8885-08e1d92dec55_1024x765.png)

这就引出了「焊盘受限（pad limited）设计」的概念。把老设计迁移到新制程节点时，设计本身可以大幅缩小，但 IO 需求会拖住芯片尺寸能缩多小。由于 IO 的需要，裸片尺寸必须维持在更大，还留有空白区域。这类情况被称为焊盘受限，而且相当常见。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

顺带一提，这不仅与使用先进封装的先进制程相关，也关乎围绕汽车芯片和整个成熟制程半导体短缺的讨论。Intel 的 Pat Gelsinger 一直主张，这些陷入短缺的公司应转向 Intel 16nm 代工服务。

> 今天，我们宣布在爱尔兰工厂推出 Intel 16 及其他节点的欧洲代工服务，我们相信这有机会帮助加速结束供应短缺，我们正在与汽车及其他行业合作，帮助他们在这些能力上继续建设。但我也想说，有人可能会反驳：那些汽车芯片大多在老节点上，我们难道不需要一些老节点的新晶圆厂吗？我们是想投资过去，还是想投资未来？
>
> 一座新晶圆厂要 4、5 年才能建成并达到可量产的水平。这不是解决当下危机的选项。投资未来，不要向后投资。相反，我们应该把所有设计都迁移到新的现代节点上，为未来供应和灵活性的提升做好准备。
>
> Pat Gelsinger - Intel CEO

Intel 这套说辞的问题在于：把这些设计从古老节点迁到相对现代的节点时会变成焊盘受限。由于焊盘受限，芯片面积无法很好缩小，每 mm2 成本更高，单位成本经济性根本算不过来。除了这些成本，把古老芯片重新设计到更新的节点、再加上整套重新认证流程，还带来高额的一次性成本。把老芯片搬到新节点这条解决方案并不可行。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/164719be-ac38-4e7c-9749-872ee3c74b21_1024x524.png)

那么，要怎么提高 IO 数量？

一条路子是想方设法把芯片做大。面积越大，留给 IO 的空间就越多。这并非最佳路线，但设计者常常会增加裸片上的内存，让更多数据存在片上，这反过来在一定程度上降低了 IO 需求。AMD 近年的架构就是绝佳例证，他们的 CPU 和 GPU 都配上了巨大的缓存。

AMD 把它命名为 Infinity Cache。这个方案的思路是在处理器内提供大容量片上 SRAM 池，存储计算上最相关的数据，从而降低内存带宽需求。在 GPU 领域，AMD 明确表示，通过增加 Infinity Cache，能把 GDDR6 总线位宽从 384 bit 缩到 256 bit。[Apple 在这方面同样激进，在自研处理器上塞入了海量缓存。](https://semianalysis.substack.com/p/apple-a15-die-shot-and-annotation) 这些设计选择中有一部分与功耗有关，但很大一部分也源于焊盘限制。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/4f0e9d86-0b29-4bfe-978b-489021387f2c_1024x554.jpeg)

另一条路是加入各种应用专用电路来提升芯片效率。异构计算中这样的例子俯拾皆是。回到我们的 [Apple A15 裸片分析](https://semianalysis.substack.com/p/apple-a15-die-shot-and-annotation)，CPU 或 GPU 占据的面积少得惊人，而这恰恰是人们谈论最多的两个方面。Apple 没有把精力放在这些营销卖点 上，而是把大量面积留给其他功能。虽然没有标注，右下角大部分是图像信号处理器。裸片的这一大块在干与拍照、录像相关的计算。还有另一个未标注的模块，负责媒体编解码相关的计算。环顾整个 SOC，随处可见这些相当小的整齐矩形，那就是 SRAM 缓存，让更多数据留在片上，而不必去内存里取。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/fd6d84d2-a85d-4768-973e-5f8ca3eb1e76_695x1024.png)

这些工作负载无法在传统 CPU 上运行。AI 模型的规模正膨胀到荒诞的地步。Facebook 的深度学习推荐系统模型参数超过 12 万亿。那膨胀的模型就是专门为了让你在 App 上停留更久、点更多广告。Google 为 AI 模型的训练和推理开发了自研芯片 TPU。他们还进一步扩大了自研芯片的版图：随着 [VCU 的问世——一种新型处理器，若专注于同一任务，一颗可以取代 1,000 万颗 CPU。](https://semianalysis.substack.com/p/google-new-custom-silicon-replaces?s=09)

Amazon 拥有[同时运行其 hypervisor 和管理栈的自研网络芯片](https://semianalysis.substack.com/p/amazon-graviton-3-uses-chiplets-and)。他们还有专门用于 AI 训练、AI 推理、[存储控制和 CPU](https://semianalysis.substack.com/p/amazon-graviton-3-uses-chiplets-and) 的自研芯片。看看 Marvell 和 Broadcom 的 ASIC 服务都聚焦在什么方向，墙上的字迹已经很清楚：硬件设计与架构的解聚合只会愈演愈烈。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c1fb046e-5353-475d-9fb1-5a75123290fd_1024x576.jpeg)

就连 Intel——那家傲慢到多年来坚信所有工作负载都该跑在 CPU 上的公司——也承认唯一的出路是异构设计。业界不再为每项任务打造通用的 CPU 硬件，而是把常见工作负载拎出来，为它们专门打造芯片。这让架构师能从每单位硅片上榨出更多性能。

长话短说：CPU 之外、应用专用集成电路的异构整合正大行其道。但更多内存和更多异构计算并不是万灵药。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

通过增加内存和异构计算来扩大裸片面积，对消除焊盘限制和提升能效来说妙不可言，但这些都是要花钱的。

而且是花大钱。

更大的裸片面积意味着更多引脚、更多集成功能，但它也是成本失控的绝佳配方。而且裸片尺寸已经到了极限。举个例子，看看 Nvidia 或 Intel 的数据中心产品线，两家都已在「光罩极限」附近徘徊了 5 年以上。就算他们想，也没法继续把芯片做大了。制程微缩的大幅放缓又在助长这一问题。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9ca77cea-7438-415d-9eb8-62f5d2684baf_1024x577.png)

于是，微缩放缓了，芯片尺寸没法再大多少，设计还受焊盘限制。问题就这些吗？

不幸的是，并非如此。硅的单位经济性也撞上了路障。半导体行业及其下游产业一手为整个经济创造了通缩环境，抵消了其他地方的通胀行为。若非如此，美国和欧洲自 80 年代起就会陷入无尽的滞胀。然而，这股颠覆性的通缩力量正在撞上路障。半导体的单位经济性不再改善。事实上，要把晶体管做得更小，情况甚至还在恶化。制造一颗大芯片不仅昂贵，而且比上一代更贵。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c3c50db3-49e5-48b4-ae4f-dafec5de3c8a_1024x578.png)

AMD 的这张图表勾勒出一幅相当惨淡的图景。虽然每次节点转换并不对等，但很明显，在 7nm 和 5nm，行业撞上了拐点。不再是每单位良品 mm2 成本的小幅上升，而是大幅跃升。尽管各次节点转换的密度收益相近，甚至因 [SRAM 微缩的放缓](https://semianalysis.com/apple-a14-die-annotation-and-analysis-terrifying-implications-for-the-industry/)而更差，成本涨幅却完全不成比例。每晶体管成本相关趋势的逆转令整个行业震惊。这一逆转影响深远，甚至[让不明就里的银行家拿它当理由，把台积电下调评级为估值过高。](https://semianalysis.substack.com/p/morgan-stanley-just-reduced-tsmcs)

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d438e543-4bd6-4c73-9010-2a73c68d2236_1024x250.png)
> [Morgan Stanley 认为](https://semianalysis.substack.com/p/morgan-stanley-just-reduced-tsmcs)，由于摩尔定律放缓、晶体管成本微缩停滞，台积电的定价压力将会减弱。Morgan Stanley 拿出了一张可笑的图表来支撑观点，图上显示 5nm 的晶体管成本低于 7nm。这与行业专家的认知形成鲜明对比。每晶体管成本在 FinFET 节点引入时便已停滞，7nm 完全见顶，到 5nm 更是有史以来最高。我们的读者可以自己算算：N7 晶圆约 $9,500 一片，N5 晶圆约 $16,000 一片。Apple 的裸片面积几乎没有下降，却掏了更多的钱。

所以每晶体管成本仍在上升，而对算力的需求比以往任何时候都涨得更凶。我们转向异构架构来反击，但如今硅设计流程变得艰难得多。行业必须依靠许多拥有不同 IP 的团队按时交付，并把这一切整合到一起。Synopsys、Cadence 等 EDA 厂商的辅助工作做得非常出色，但还不够。对任何没有超过 10M 台出货量用例的公司来说，一个能购买应用专用 IP 或芯片并整合进自家硬件设计的开放生态是必需的。即便对那些大公司，小芯片式的系统架构也是答案。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ce1be050-b76c-46b3-a120-2cdb5fc43d88_1024x768.jpeg)
*AMD Rome/Milan*

随着我们继续微缩，预期良率会缓慢下降。这是个合乎逻辑的结论，因为每一代节点会增加约 35% 的工序步骤。当先进制程以数千道工序计，误差开始迅速叠加。工业企业爱吹捧「六西格玛」，但对半导体制造来说这远远不够。假设一个 2,000 道工序的制程，每道工序在每 cm2 缺陷数上都做到 6 个西格玛，那么 D0（行业术语，每 cm2 缺陷率）最终将是 0.678。裸片越大，出现缺陷的概率就越高。

如果这个假想制程在造 Intel 的旗舰服务器 CPU Ice Lake，结果是每片晶圆只有 4 颗好裸片、76 颗缺陷裸片。再想想这个分析是在 cm2 层面做的，而先进制程节点上每 cm2 有数十亿颗晶体管。半导体行业远比六西格玛强大。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

除了在皮米量级上追求完美，还有什么解法？

小芯片（chiplet）！把大芯片拆成许多小芯片。

AMD 是最广为人知的例子，但这是全行业的趋势。AMD 只需设计 3 颗芯片——1 颗 CPU 核心小芯片和 2 颗 IO 裸片——就能覆盖很大一部分市场。而 Intel 要设计 2 颗 Alder Lake 桌面芯片和 3 颗 Ice Lake 服务器芯片，才能覆盖同样的可服务市场。如此一来，AMD 省下了设计成本，造出了核心数比 Intel 更多的 CPU，还在良率上省了钱。

为演示良率论证，请看下表。AMD 把 CPU 核心分散在 8 颗 CPU 核心小芯片上。如果良率是 100%，Intel 本可以比 AMD 更低的每 CPU 核心成本制造核心。但现实是，Intel 在每颗 CPU 核心上的花费反而更高，因为更大的芯片缺陷更多。下表有几个显而易见的注意事项，最大的是假设缺陷裸片的降级利用为 0，以及 Intel 与台积电的 D0 相同。这两个假设都不成立，此推演仅作演示之用。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/45b8546f-dd0c-45a1-a01a-25a93539f037_1024x542.png)

小芯片很棒，但它不是孤立的解药。我们仍会撞上许多同样的问题。每晶体管成本仍在上涨，设计成本飙升，小芯片因为需要更多 IO 与其他芯片互连而同样焊盘受限。芯片的某些部分受 IO 约束无法拆分，所以芯片尺寸仍在见顶。

那解药是什么？

先进封装！

这里我们要指出，有些设备厂商把所有倒装芯片封装都称作「先进封装」。SemiAnalysis 和业内多数下游玩家不会这么说。因此，我们要稍微正一下名：我们把所有凸点尺寸小于 100 微米的封装称为「先进」。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/44c6b994-b19d-4cb3-aad3-63aa85b851e7_1024x662.jpeg)

最常见的一类先进封装叫扇出（fan out）。有人甚至主张它根本算不上先进封装，这些人大错特错。仍以 Apple 为例，他们会让台积电把应用处理器裸片以 90 微米到 60 微米量级的更密凸点，封装到重构或载板晶圆/面板上。这比传统倒装芯片封装的凸点密度高出约 8 倍。

这块重构或载板晶圆/面板随后把 IO 进一步铺开，「扇出」之名由此而来。扇出封装之后再安装到主板上。硅裸片的设计可以更少顾虑焊盘受限，因为扇出上的焊盘更小。这种封装上还可以封装 DRAM 内存、NAND 存储和 PMIC。集成扇出不仅密度出色，还把大量芯片间 IO 留在了封装内。这些 IO 若非如此，就不得不通过主板以大得多的 IO 间距互联。

集成扇出在高性能应用中正越来越普遍，不再只属于移动端。增长最快的用例在网络一侧，那里的设计已被焊盘限制折腾了十多年。AMD 将在其服务器 CPU 和 GPU 上相当激进地采用扇出。[Tesla Dojo 1](https://semianalysis.substack.com/p/tesla-dojo-unique-packaging-and-chip) 是集成扇出封装的另一个高知名度例子，只不过是晶圆级（wafer scale）的。[顺带一提，SemiAnalysis 在官宣之前就率先泄露了 Tesla 会采用这种封装类型](https://semianalysis.substack.com/p/tesla-ai-day-supercomputer-chip-teaser)。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/52c3d881-4620-45bb-899a-721b3f433b6b_1024x545.png)

先进封装之中有 2.5D 和 3D 封装。2.5D 是把硅封装在另一块硅之上，但下方的硅裸片专用于布线，没有有源晶体管。这通常以 55 微米到 50 微米的间距完成，凸点密度约高 16 倍。最常见、出货量最大的用例，是 Nvidia 数据中心 GPU 采用的台积电 CoWoS（chip on wafer on substrate）。台积电把有源芯片封装到一块只有互连和微凸点（micro-bump）的晶圆上，然后把这一摞芯片用传统方法封装到基板上。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

其他例子基本涵盖所有带 HBM 的处理器。HBM 诞生的初衷，就是在传统形态的 DRAM 之上阶跃式提升内存带宽。它靠宽得多的内存总线来实现。这些宽总线带来了 IO 数量的问题，但 HBM 从设计之初就打算与处理器同封装共置。这既绕开了 IO 问题，又实现了更紧密的整合。

2.5D 的更多例子还有基于 Intel EMIB 的产品、Xilinx 的 FPGA、AMD 最新的数据中心 GPU，以及 [Amazon Graviton 3。](https://semianalysis.substack.com/p/amazon-graviton-3-uses-chiplets-and)

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/14383844-678e-4767-80c0-57c1a0d7a25e_1024x576.jpeg)
*Nvidia A100*

3D 封装则是把一颗有源裸片封装到另一颗有源裸片之上。这最初由 Intel 以 55 微米间距出货逻辑硅，但大批量用例将落在 36 微米及以下。台积电和 AMD 将以 17 微米间距出货 3D 堆叠的 V-Cache。这项技术从凸点转向硅通孔（TSV），而且还有大得多的微缩空间。

其他应用，比如 Sony 生产的 CMOS 图像传感器，已经做到 6.3 微米间距。继续做对比：36 微米间距的凸点密度高 31 倍，17 微米间距实现的铜 TSV 的 IO 密度高 138 倍，而 Sony 6.3 微米间距的 CMOS 图像传感器相对标准倒装芯片的 IO 密度高 567 倍。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2248a9b0-1a29-47cb-aef2-1cfe1191bb67_943x1024.png)
*Sony 2017 年 IEDM CMOS 图像传感器 TSV*

以上只是对主要封装类型的基础讲解，本系列后续将对不同类型深入展开。各家公司在未来的封装类型、工具以及向哪些工具供应商下注上，做出了相当不同的选择。设备和 IP 这一侧的精彩程度远超人们第一眼的想象，但得先把基础讲清楚，我们才能往深处走。

在这片即将到来的创新之海中，有大量可投资的观点与角度。激进变革正由摩尔定律的放缓所驱动。我们正处于由先进封装推动向前的半导体设计文艺复兴之中。

本文付费墙后没有内容，但随着我们进入具体公司，后续会有更多。提醒一下各位可以期待什么：以往的付费墙内容中，我们[独家披露了 Graviton 3 的封装供应商（某家蓝色公司）](https://semianalysis.substack.com/p/amazon-graviton-3-uses-chiplets-and)，并[讨论过与金属氧化物光刻胶和干式光刻胶相关的制程导入胜局。](https://semianalysis.substack.com/p/lam-research-tokyo-electron-jsr-battle)

[分享](https://semianalysis.substack.com/p/amazon-graviton-3-uses-chiplets-and?utm_source=substack&utm_medium=email&utm_content=share&action=share&token=eyJ1c2VyX2lkIjoyMTc4MzMwMiwicG9zdF9pZCI6NDQ4NzQzMDksImlhdCI6MTYzOTU5MDkzMywiaXNzIjoicHViLTMyOTI0MSIsInN1YiI6InBvc3QtcmVhY3Rpb24ifQ.dOAjYRLygP4eYRf99GTS1fsNv3uePaZR3tZ10yYpsVs)

[赠送订阅](https://newsletter.semianalysis.com/subscribe?&gift=true)

[分享 SemiAnalysis](https://semianalysis.substack.com/?utm_source=substack&utm_medium=email&utm_content=share&action=share)
