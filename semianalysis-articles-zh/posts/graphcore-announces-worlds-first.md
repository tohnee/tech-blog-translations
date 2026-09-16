---
title: "Graphcore 发布全球首款 3D 晶圆对晶圆混合键合处理器"
title_en: "Graphcore Announces World’s First 3D Wafer On Wafer Hybrid Bond Processor "
subtitle: "Bow、Good Computer 与晶圆对晶圆混合键合解析"
date: 2022-03-03
source: https://newsletter.semianalysis.com/p/graphcore-announces-worlds-first
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Graphcore 发布全球首款 3D 晶圆对晶圆混合键合处理器

> 原文：[Graphcore Announces World’s First 3D Wafer On Wafer Hybrid Bond Processor](https://newsletter.semianalysis.com/p/graphcore-announces-worlds-first) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Bow、Good Computer 与晶圆对晶圆混合键合解析**

Graphcore 正在发布其最新的 AI 加速器 Bow。在很大程度上了，其架构与上一代完全相同，只在系统设计上有一处重大变化：引入 3D 晶圆对晶圆（wafer-on-wafer）堆叠。他们是台积电（TSMC）晶圆对晶圆 SoIC 技术的先锋客户。我们将在本文中深度解析这种封装技术，包括其目的、优势、成本、工艺流程，以及后续环节中用到了哪些半导体制造设备。

晶圆对晶圆技术让 Graphcore 在保持与上一代 MK2 相近成本的同时，将时钟频率和性能最高提升 40%。Graphcore 表示，这款芯片目前正出货给合作伙伴，包括但不限于美国能源部（US Department of Energy）以及两家云服务提供商 Cirrascale 和 G-Core Labs。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6b816dea-d987-4a86-af34-8aea5b623030_1024x683.jpeg)

眼尖的读者可能会注意到它看起来与上一代 IPU 几乎一模一样。这是因为其架构、裸片面积和晶体管数量实际上完全相同。该处理器仍采用相同的台积电 7nm 节点制造，只包含一些为启用混合键合而做的微调。最终用户将获得相对上一代最高 40% 的性能收益和最高 16% 的每瓦性能收益。时钟频率从 1.325GHz 提升到 1.85GHz。时钟频率的提升同时影响芯片的原始算力（flops）以及片上 SRAM 提供的带宽。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d4fbcddd-14da-4ace-9fcb-7b225e602ccc_1024x487.png)

Bow Pod 的规格在 CPU、内存和芯片间带宽方面完全相同。唯一的变化是将先前的加速器换成新的 Bow。得益于完全相同的架构，Graphcore 无需对软件做任何改动即可实现这一点。Graphcore 强调终端用户的成本没有任何增加。成本未增加的原因将在后文的 3D 封装部分解释。40% 的时钟频率提升转化为其工作负载套件中 30% 到 40% 的性能提升。考虑到芯片间带宽完全没有扩展，Graphcore 第一方基准测试中的性能扩展相当惊艳。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/307d8dd3-e2f9-4015-a5ff-401358387883_1024x472.png)

尽管时钟频率提高了 40%，每瓦性能却仍有小幅改善。这非常出人意料，因为芯片仍在使用相同的制程节点。按照电压-频率曲线的指数特性，人们本会预期每瓦性能变差。这一关系被 3D 晶圆对晶圆堆叠带来的供电优化整体平移了。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b95ee0be-f4b3-4d70-92c1-2ad671a50ee1_1024x542.png)

与上一代完全的软件兼容性是 Bow 芯片最大的亮点之一。因为除了软件变化和对用户不可见的 3D 堆叠变化之外架构完全相同，一切都可以无缝迁移。当然，软件生态方面仍存在一些疑问，尤其是相对于 Nvidia 这样的竞争对手而言。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9e03af73-103c-44ae-bc24-10fb1ffdc0ab_1023x588.png)

Graphcore 宣称在训练时间和 TCO 上拥有巨大优势，但[我们此前关于 Graphcore 的文章](https://semianalysis.substack.com/p/graphcore-looks-like-a-complete-failure?s=w)中的每一条论点仍然成立。

1. 他们用 16 颗由台积电制造的 7nm 823mm² IPU 对比 8 颗由台积电制造的 7nm 826mm² A100。即便不含 HBM，拿两倍的硅片面积作对比也相当不厚道。
2. Graphcore 系统的内存容量小得多，尤其是高带宽内存池。他们用一个较小的模型作为对比点来掩盖这一短板。
3. Graphcore 特意选用了 80GB 的 A100 而非 40GB 版本，前者价格高出 1.5 倍。
4. Graphcore 特意选用了 Nvidia 的 DGX 系统——包含 Nvidia 直接技术支持——而非 OEM 的现货系统。SuperMicro 采用 40GB A100 的可比系统价格约为 ~$125,000。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ef68ea8a-d116-45e1-af76-6b85945a9dfd_1024x567.png)

尽管有这些反驳意见，Graphcore 的改进幅度相当可观，而且在很多工作负载上 Bow 的 TCO 确实很可能击败 Nvidia 的 A100。唯一的问题是，Nvidia 向特定合作伙伴出货下一代 Hopper GPU 的数量已经超过 Graphcore 出货 Bow 的数量。他们本月就将在 GTC 上发布下一代 Hopper GPU。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

Nvidia 要想在 MLPerf 套件这类小模型上保住优势，只需在相同成本下将每 GPU 性能最高提升 40%、能效最高提升 16%。鉴于 Nvidia 历来的进步幅度以及[与性能和功耗相关的泄露信息](https://semianalysis.substack.com/p/nvidia-hacked-a-national-security)，这似乎非常容易实现。除非 Hopper 在这方面带来重大架构改进，否则 Graphcore 在某些使用场景（尤其是低 batch size 场景）仍将胜出。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/77b9e7b1-2cda-48db-b4d3-29848be222fb_1024x499.png)

Graphcore 还发布了「Good Computer」，这是一种由众多服务器和机柜组成的整机柜级完整解决方案。它将获得其广受欢迎的 SDK 的全面支持。这一点非常重要，因为 AI 训练领域正在迅速变成一个交钥匙解决方案的问题。单卖芯片甚至单卖服务器已经不够。[最好的 AI 训练芯片必须能够纵向扩展和横向扩展](https://semianalysis.substack.com/p/tenstorrent-wormhole-analysis-a-scale)到海量服务器规模，以应对最大的数万亿参数问题。

在性能方面，这台「Good Computer」甚至超过了特斯拉（Tesla）已发布但[尚未建成](https://semianalysis.substack.com/p/the-tesla-dojo-chip-is-impressive)的 [Tesla Dojo 超级计算机](https://semianalysis.substack.com/p/tesla-dojo-unique-packaging-and-chip)。在 AI 性能和能力上，只有基于 Fujitsu 和 Nvidia 的超级计算机能与「Good Computer」匹敌。我们对此感到兴奋，但考虑到芯片间带宽的限制，我们对其完美的强扩展与弱扩展持保留态度。Graphcore 表示，其未来几代 AI 加速器将更直接地解决芯片间带宽问题。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/4720b7a8-3b38-4022-b7c2-51c63fcd2d99_1024x461.png)

这颗芯片最激动人心的部分是 3D 封装。正是它在架构和节点不变、成本相同的情况下，实现了 40% 的时钟频率提升和能效改善。先进逻辑芯片的一个普遍问题是瞬时电流尖峰。平滑的供电至关重要，往往正是限制更高时钟频率的瓶颈。Graphcore 证明了仅仅通过平滑和改善供电，就能在不降低每瓦性能的前提下获得大幅的时钟频率提升。

Graphcore 的实现方式是在第二片晶圆上实现大量深槽电容（deep trench capacitor），并利用台积电的 SoIC 晶圆对晶圆混合键合技术将两片晶圆集成到一起。大多数设计会在片上甚至封装内放置一些深槽电容，但这是深槽电容首次以 3D 混合键合的方式实现。这些嵌入式深槽电容类似于以往 DRAM 工艺中的深槽电容。这一封装创新带来的深槽电容容量，比以往任何高性能先进制程芯片都高出多个数量级。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2b5e9f7b-3ec8-41ac-9084-31328a18d6c2_640x608.png)

我们在[先进封装系列的第二部分](https://semianalysis.substack.com/p/advanced-packaging-part-2-review)中提到过，台积电的晶圆上芯片-基板技术（CoWoS）在几年前首次将这类技术引入 2.5D 封装。[英特尔的 Foveros 也在基础裸片上提供深槽电容](https://semianalysis.substack.com/p/advanced-packaging-part-3-intels)。这些电容位于基础裸片上，通过缩小瞬时尖峰的幅度来平滑供电并提高稳定性。用外行的话说，电容用于储能。当芯片的电流需求快速变化时，它们能减少电压跌落并平滑供电。当然，背后的实际科学原理要复杂得多。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/238275bb-4707-4326-ac8e-0ec8a5684a96_828x409.jpeg)

Graphcore 是台积电这项技术的先锋客户。这里的混合键合工艺是晶圆对晶圆（wafer-on-wafer），而非晶圆上芯片（chip-on-wafer）。这为封装密度带来了巨大收益。AMD 的 3D V-Cache 技术使用[台积电的晶圆上芯片键合，TSV 间距为 17 微米](https://semianalysis.substack.com/p/advanced-packaging-part-2-review?s=w)。而晶圆对晶圆混合键合技术能够以 1/10 的间距提供 TSV。换句话说，在晶圆上芯片混合键合能提供 100 个 TSV 的面积内，晶圆对晶圆技术可以提供 10,000 个。

除了密度和集成度的提升，封装的产能也大幅提高。不再需要逐个拾取、抛光、切割、清洗和放置单颗裸片，晶圆对晶圆允许整片晶圆一次性键合。这极大提升了产能并降低了成本。良率问题则通过在架构上增强设计的可修复性来解决。

[索尼的图像传感器](https://semianalysis.substack.com/p/advanced-packaging-part-1-pad-limited)和长江存储（YMTC）的 NAND 也使用晶圆对晶圆混合键合技术。台积电的晶圆对晶圆技术与 Xperi 的 DBI 有很大不同，但这个话题我们留到下周发布的混合键合深度解析中再谈。订阅我们的 newsletter，不要错过。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

台积电晶圆对晶圆混合键合的工艺非常有趣：它始于两片晶圆之间的熔融硅氧化物键合。其中一片包含 Graphcore 上一代 MK2 芯片的微调版本，另一片则带有深槽电容。键合后的晶圆对随后被一路研磨减薄，直到带电容的顶层晶圆只剩 10 微米厚。带逻辑电路的晶圆提供结构刚性。随后晶圆对经过离子刻蚀工艺，刻蚀到 TSV。接着 TSV 以 ~1 微米间距的量级穿过第二片晶圆构建而成。虽然 Graphcore 在第二片晶圆上没有使用任何晶体管，但他们表示未来会使用。

这类晶圆对晶圆混合键合的工艺相当独特，因此也拥有独特的供应链。我们将在订阅专享部分进一步讨论该工艺、成本，以及该流程中涉及的半导体制造设备供应商。

[分享](https://newsletter.semianalysis.com/p/graphcore-announces-worlds-first?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)
