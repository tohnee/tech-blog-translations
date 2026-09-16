---
title: "封装的未来变得模糊——扇出、ABF、有机中介层、嵌入式桥接——先进封装系列第 4 篇"
title_en: "The Future Of Packaging Gets Blurry – Fanouts, ABF, Organic Interposers, Embedded Bridges – Advanced Packaging Part 4"
subtitle: "先进封装系列第 4 篇"
date: 2022-11-01
source: https://newsletter.semianalysis.com/p/the-future-of-packaging-gets-blurry
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 封装的未来变得模糊——扇出、ABF、有机中介层、嵌入式桥接——先进封装系列第 4 篇

> 原文：[The Future Of Packaging Gets Blurry – Fanouts, ABF, Organic Interposers, Embedded Bridges – Advanced Packaging Part 4](https://newsletter.semianalysis.com/p/the-future-of-packaging-gets-blurry) · SemiAnalysis

**先进封装系列第 4 篇**

先进封装如今炙手可热；想要系统入门，可[阅读我们的多部分系列文章](https://www.semianalysis.com/p/advanced-packaging-part-1-pad-limited)。在本系列前面的文章中，我们讨论了[为什么需要先进封装](https://www.semianalysis.com/p/advanced-packaging-part-2-review)、[各家公司提供的各类先进封装](https://www.semianalysis.com/p/advanced-packaging-part-2-review)，以及[热压键合（TCB）设备市场，包括 Intel 的独特用例](https://www.semianalysis.com/p/advanced-packaging-part-3-intels)。本文是该系列第 4 篇，深入探讨 2.1D、2.3D 与 2.5D 先进封装之间日益模糊的边界。在 IMAPS 2022 上，该领域展示了许多进展，先进封装行业的未来非常活跃。先做个简要回顾：目前先进封装主要有四大类。

3D = 活性硅堆叠在活性硅之上——最著名的形态是[采用 TSMC SoIC CoW 的 AMD 3D V-Cache](https://www.semianalysis.com/p/packaging-developments-from-ectc?s=w) 和[采用 TSMC SoIC WoW 的 Graphcore IPU BOW](https://www.semianalysis.com/p/graphcore-announces-worlds-first?s=w)。

2.5D = 活性硅堆叠在无源硅之上——最著名的形态是[采用 TSMC CoWoS-S 封装 HBM 内存的 Nvidia AI GPU](https://www.semianalysis.com/p/nvidia-in-the-hot-seat) 和[采用 Intel Foveros 的 Intel Meteor Lake CPU](https://www.semianalysis.com/p/meteor-lake-die-shot-and-architecture)。

扇出 RDL（带环氧塑封料的层压基板）——最著名的形态是[用于 Apple A 系列、S 系列和 M 系列芯片的 TSMC InFO](https://www.semianalysis.com/p/apple-m2-die-shot-and-architecture)、ASE 的 FoCoS 以及 Amkor 的 WLFO。多家厂商正在开发面板级（panel level）方案。

积层 ABF 基板（铜核外覆味之素积层膜层与 RDL 层）——最著名的形态是 [Intel 与 AMD 的 PC 及数据中心芯片](https://www.semianalysis.com/p/advanced-packaging-part-2-review)。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/c80695c0-28cb-4b94-8969-affae1a9b67b_935x673.png)

在大多数先进封装场景中，仍会使用积层 ABF 基板。这类方案被称为混合基板（hybrid substrate）。

先进封装另一个容易引起歧义的地方在于，工程师们常说「有机基板」（organic substrate）这个词。ABF 基板和带核心层的扇出封装都含有有机环氧化学材料。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/333e628a-cc9c-43e1-992e-092d419db493_897x290.jpeg)

从 2.5D 到 3D 的分类看似简单，但封装形态的许多排列组合正在模糊 2.3D 与 2.1D 之间的界线。而且，随着这些 2.3D 和 2.1D 封装的能力不断提升，2.5D 将会让出部分市场份额。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/444bc464-2149-44d0-b4e5-8ef166fead08_2022x1348.png)

Intel 的 EMIB 是在积层 ABF 基板的开槽（cavity）中嵌入一块硅桥。其主要目的是避免使用昂贵的硅中介层，并让封装[突破光罩极限](https://www.semianalysis.com/p/die-size-and-reticle-conundrum-cost)继续增大。严格来说 EMIB 并不算 2.5D 封装，但它确实带来了 2.5D 所宣称的许多好处。与纯 2.5D 硅中介层或高密度扇出相比，它在成本和性能上如何？对于未来几代产品尚无定论，但第一代的对比结果并不占优。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/23801996-c530-4ace-ad58-0839701d22d6_1003x897.png)

AMD 的 MI250X GPU（见上图标注）和 Apple 的 M1 Ultra 是单一产品中融合多种封装类型的例子。它们没有用硅中介层来连接 GPU 裸片与 HBM，而是在 GPU 裸片与每颗 HBM 之间放置硅桥。带嵌入式桥的扇出封装与 Intel 的 EMIB 类似，但制造流程完全不同：一个是扇出 RDL，一个是积层基板。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a4f00408-d47e-4ab6-8609-ffb923fd5a17_842x319.jpeg)

在 MI250X 的案例中，两个各自带硅桥和 GPU/HBM 的独立扇出 RDL 组件，被封装在一块大型 ABF 基板之上。

从理论上讲，由于最大限度地减少了对昂贵硅中介层的使用，这种方案的成本更低，但其良率损失的概率高于传统 2.5D 硅中介层方案。

扇出 RDL 并非单一工艺。它可以用几种不同的材料类型来构建，而且流程既可以是先做 RDL（RDL-first），也可以是先贴芯片（chip-first）。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8152caca-45b3-46e6-a661-9fe33d741498_631x538.png)

无论扇出 RDL 采用 RDL-first 还是 chip-first 流程，做好的混合基板在裸片贴装之前都无法测试。如果扇出与基板的键合工序出问题，好的裸片也会随之报废。尽管扇出 RDL（尤其是面板级扇出）在理论上成本更低，良率损失仍是硅中介层持续被沿用的主要原因。这些良率问题还可能延伸到基板翘曲：扇出 RDL 材料、积层基板与硅之间的热膨胀系数（CTE）失配会引发翘曲。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/63aef1a1-717b-4811-a242-236cb3e4a464_1052x742.png)

Samsung、Shinko、Unimicron、SPIL 和 TSMC 一直在研究这样的封装流程：先制作扇出 RDL；然后将扇出 RDL 键合到积层 ABF 基板上；随后对键合好的混合基板进行测试；最后才把芯片键合上去。这被称为扇出（RDL-first 或 chip-last）、芯片后键合（Chip Bonding Last）。各家都有自己的调整，有的使用有机材料，有的使用无机材料。更高的组装良率，加上「合格基板」（known good substrate）物流体系，为先进封装带来了巨大优势。

数据中心和 PC 行业的传统供应链运作方式，就是让合格基板与合格裸片（known good die）相匹配。只要能以合理成本实现，RDL-First/Chip Last、芯片后键合就是最理想的封装方法。

采用扇出（chip-first）流程的 IC 集成比扇出（chip-last 或 RDL-first）流程更简单、成本更低。问题在于 chip-first 意味着会有更多合格裸片损耗在封装良率上。随着行业转向更昂贵的制程技术，这种封装良率损失日益成为封装工艺成本增加的主导因素。此外，扇出（chip-last）集成还有其他优势：更大的裸片尺寸、更大的封装尺寸、更小的裸片偏移（die shift）问题，以及更细的 RDL 金属线宽/线距（L/S）。L/S 指线宽/线距，即金属互连的宽度及其间距。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/810a4142-a0b3-4a0f-886a-5f1e456d2f51_1037x785.png)

与此同时，非扇出技术也在进步。Cisco 展示了与无芯有机基板相关的研究。制作这种有机中介层的主要制造步骤与积层封装基板相同，只是没有铜核。Cisco 演示了 10 层布线层，其 L/S 比标准的带芯积层 ABF 基板更密。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3d553074-859f-4ed9-bcc5-30f88d07904f_1506x841.png)

如今，积层 ABF 基板的 L/S 最密可达 10 微米；Cisco 的研究表明有机基板可以做到 6 微米 L/S。带芯扇出市场的 L/S 在 15 微米左右。一些先进扇出方案，例如 [AMD 的 RDNA 3 GPU](https://www.semianalysis.com/p/ada-lovelace-gpus-shows-how-desperate) 和[某款 MediaTek 网络处理器](https://www.semianalysis.com/p/packaging-developments-from-ectc?s=w)，可达 2 微米 L/S。EMIB 第一代达到 5 微米 L/S，传闻未来几代将达到 2 微米 L/S。

随着积层 ABF 基板的进步，带芯扇出与高密度扇出市场在移动应用之外正被一定程度上蚕食。就介质材料而言，光敏介质（photo-imageable dielectrics，PID）目前能够实现更细的节距。尽管如此，ABF 在表面平整度变化方面仍有诸多优势，Unimicron 的数据即是明证。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7b66e587-4d85-4be7-975d-fa307c5dbd1c_1496x732.png)

Unimicron 看起来将坚持采用改良型 ABF，因为这是其核心能力所在。细节距无芯 ABF 延续其现有商业模式——交付合格（混合）基板。他们可以实现 3 微米 L/S，且表面平整度变化更优，从而能够扩展到更多层数。其无芯 ABF 基板与当前的先进扇出方案相比可能极具竞争力。它采用面板工艺，因此既可与晶圆级竞争，又能逼近未来的面板级扇出。虽然它被限制在 3 层 RDL，但向更多层数扩展的路径比扇出 RDL 更容易。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b38cc4c7-42cf-4588-8550-78e0d9140b30_1017x687.png)

无芯 ABF 基板更厚，这对移动应用可能是个问题，但对高性能应用而言，其可靠性和性能应该更好。

在追求极致 L/S 方面，Amkor SLIM 和 ASE SPIL NTI 分别可以达到 0.4 微米和 0.5 微米。两者都仅能在第一层实现这样的细节距。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2cb12591-fa11-4731-94b4-2f0259745d93_792x595.png)

ASE SPIL 展示了其扇出 RDL 方案，称其在把 HBM 裸片连接到 SOC 方面比 2.5D 先进封装性能更强。ASE SPIL 声称其眼图高度更佳、损耗更小，从而能在封装内实现更高速的信令速率和更低的噪声。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/4dd4dc43-b0a9-48b6-a856-d0da019e7c09_3437x1986.png)

积层 ABF 基板仍将是先进封装市场的基础，但随着向无芯基板转型，其性能和密度正在提升。此外，正如 Cisco 所示，这类基于 ABF 的基板凭借 Unimicron 展示的更优表面平整度特性，可以达到更高的层数。在许多用例中，ABF 基板正在追赶并超越扇出 RDL。

随着 RDL 扇出向以往仅由 2.5D 中介层占据的应用领域上探，成本和良率也成为关键因素。带硅桥的扇出工艺已开始爬坡，而不用硅桥、直接将 ASIC 与 HBM 集成的新工艺也正在接近量产。扇出与 ABF 基板的这些进步，正在迅速模糊各类先进封装之间的界线。

评估 2.1D 到 2.5D 领域的先进 IC 封装时需要考虑多个变量。焊盘节距、L/S 和层数是关键因素，但可靠性、翘曲问题、封装成本、良率和封装尺寸同样在考量之列。未来，对某些用例而言，把无芯 ABF 基板封装在标准积层 ABF 基板之上的混合基板可能是最佳选择；而对另一些用例，把 chip-first 扇出 RDL 封装在标准积层 ABF 基板之上可能才是最优解。随着异构集成中裸片数量与类型的多样化，封装涉及的权衡取舍正变得越来越难以评估。

如果你觉得这篇文章不错，欢迎分享！

[分享](https://newsletter.semianalysis.com/p/the-future-of-packaging-gets-blurry?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

[赠送订阅](https://newsletter.semianalysis.com/subscribe?&gift=true)
