---
title: "随着摩尔定律放缓，苹果被迫在非 Pro 机型 iPhone 上使用更便宜的芯片"
title_en: "As Moore’s Law Slows, Apple Is Forced To Use Cheaper Chipsets In Non-Pro iPhones"
subtitle: "对半导体行业而言的可怕含义"
date: 2022-03-14
source: https://newsletter.semianalysis.com/p/as-moores-law-slows-apple-is-forced
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 随着摩尔定律放缓，苹果被迫在非 Pro 机型 iPhone 上使用更便宜的芯片

> 原文：[As Moore’s Law Slows, Apple Is Forced To Use Cheaper Chipsets In Non-Pro iPhones](https://newsletter.semianalysis.com/p/as-moores-law-slows-apple-is-forced) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**对半导体行业而言的可怕含义**

苹果（Apple）一直在智能手机 SoC 领域持续驱动性能和智能手机能力的进步。iPhone 是最好的手机之一，而苹果卓越的芯片团队正是这一成就的主要功臣。每一代产品，苹果都在 CPU、GPU、视频录制和能效上稳居最佳。许多 iPhone 购买者甚至可能会争辩说，芯片每年的大幅提升已经无关紧要，因为 iPhone 早已远远越过了边际收益递减的临界点。

传奇的苹果供应链分析师郭明錤（Ming Chi Kuo）为果粉们带来了重磅消息。不太成功的 iPhone Mini 已经停产，苹果将转而以 [iPhone Max](https://twitter.com/mingchikuo/status/1503033674643939333?s=20&t=hS6vNUMnR_o3JEXEkeMdfA) 取而代之。这将是一款屏幕尺寸与旗舰 iPhone Pro Max 相近的更大屏 iPhone。此外，郭明錤表示 iPhone 14 和 iPhone 14 Max 将不会搭载今年发布的全新 A16 芯片，而是[继续沿用现有的 A15 芯片](https://twitter.com/mingchikuo/status/1503033974473760768)。他还指出，Pro 机型将配备 6GB LPDDR5，而非 Pro 机型 iPhone 那样的 6GB LPDDR4X。

摩尔定律已经放缓，尤其是在经济性意义上。2018 年是苹果最后一次实现每晶体管成本的大幅下降，得益于台积电（TSMC）从 N10 到 N7 制程节点的微缩。而从 N7 转向 N5 时，由于 [SRAM 微缩问题](https://semianalysis.com/apples-a14-packs-134-million-transistors-mm2-but-falls-far-short-of-tsmcs-density-claims/)，成本收益相对有限。N7 已进入其量产的第 5 个年头，N5 也已步入第 3 年，然而晶圆单价唯一的变化方向却与期望相反。迄今为止，苹果已经硬扛过了[现有的成本微缩](https://semianalysis.com/apple-a14-die-annotation-and-analysis-terrifying-implications-for-the-industry/)难题，在过去 3 年保持了 30% 的晶体管数量 CAGR。

这一切在 2022 年发生改变。

[台积电的 N3 已经延期](https://semianalysis.substack.com/p/tsmc-3nm-wafer-shipments-pushed-into)。苹果将首次在三代产品上使用同一档制程密度。苹果正在采用台积电的 N4 制程节点，就纯逻辑微缩而言，其密度提升仅有区区 5%。台积电在财报中将 N4 制程节点营收归入「N5」节点项下，因为它们属于同一节点家族，甚至共用相同的晶圆厂。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f5b86cb9-de0e-44ad-833a-8a7dda2a3195_1023x467.png)

苹果沿用同一节点是完全史无前例的，这意味着他们不得不直面艰难的抉择。[A15 的裸片面积已经达到了相当可观的 107mm²。](https://semianalysis.substack.com/p/apple-a15-die-shot-and-annotation)苹果面临两难：要么强迫各个 IP 团队遵守严苛的面积预算并影响长期设计，要么承受制造成本的大幅上升。[尽管苹果的 CPU 性能提升已经放缓](https://semianalysis.substack.com/p/apple-cpu-gains-grind-to-a-halt-and)，他们今年仍将实施一次大规模的核心架构变更。此外，GPU、NPU、媒体模块和 ISP 也将得到升级。为了容纳新架构，苹果将要投入多得多的晶体管。这很可能使晶体管数量升至约 ~190 亿颗，裸片面积达到 ~130mm²。

此外，苹果还需要提升其 SoC 的内存带宽。凭借[增大片上缓存并改进利用率](https://semianalysis.substack.com/p/apple-a15-die-shot-and-annotation)，苹果得以在 5 代产品上坚持使用 LPDDR4x。而在 A16 上，升级到 LPDDR5 带来了大幅的成本上升。由于三大 DRAM 厂商缓慢扩产的方式，DRAM 的每比特成本实际上并没有下降。内存价格是计算领域的一大拖累。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6561c07f-c794-4f50-a31b-19c3adf20970_1096x696.png)

iPhone 13 标配 4GB LPDDR4x，若同时升级到 6GB LPDDR5 和更大的 A16 芯片，成本将难以承受。这将导致物料清单（BOM）增加超过 $40。在供应链屡遭中断、能源和大宗商品成本上涨的背景下，让苹果再吞下不断膨胀的芯片成本，也是一剂难以下咽的苦药。苹果当然也可以涨价，但那很可能会侵蚀销量。

看起来苹果选择了折中方案：在 iPhone 14 和 iPhone 14 Max 上沿用 A15 芯片，同时将内存从 4GB 提升到 6GB。这很可能让苹果得以为 iPhone 14 维持 iPhone 13 的 $799 定价。iPhone 14 Max 则将以 $899 的价格和相同规格切入市场。iPhone 14 Pro 和 Pro Max 则很可能维持 $999 和 $1099 的价位不变。

iPhone SoC 的这种分层策略很可能会延续到可预见的未来。即便台积电的 N3 最终于 [2023 年初](https://semianalysis.substack.com/p/tsmc-3nm-wafer-shipments-pushed-into)出货，晶圆价格也将远超 $20k。N3 的晶体管成本微缩已不复存在，因此这个问题只会延续。台积电 N5 的良率极其出色，D0 约为 0.07，所以[采用先进封装的小芯片（chiplet）方案](https://semianalysis.substack.com/p/advanced-packaging-part-1-pad-limited)并不能解决问题。世界将不得不与这些成本微缩难题共存——[要么消化成本上涨](https://www.fabricatedknowledge.com/p/the-rising-tide-of-semiconductor)，要么放慢晶体管数量的增长。

在订阅专享部分，我们将讨论苹果向晶圆厂和内存厂商下达的订单，以及我们对晶圆厂设备（WFE）展望的看法。它已经变了。

[分享](https://newsletter.semianalysis.com/p/as-moores-law-slows-apple-is-forced?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)
