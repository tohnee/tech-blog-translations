---
title: "Ada Lovelace GPU 暴露了英伟达的窘迫——与 AMD RDNA 3 的成本对比"
title_en: "Ada Lovelace GPUs Shows How Desperate Nvidia Is - AMD RDNA 3 Cost Comparison"
subtitle: "十年来英伟达首次对 AMD 处于成本劣势"
date: 2022-09-23
source: https://newsletter.semianalysis.com/p/ada-lovelace-gpus-shows-how-desperate
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# Ada Lovelace GPU 暴露了英伟达的窘迫——与 AMD RDNA 3 的成本对比

> 原文：[Ada Lovelace GPUs Shows How Desperate Nvidia Is - AMD RDNA 3 Cost Comparison](https://newsletter.semianalysis.com/p/ada-lovelace-gpus-shows-how-desperate) · SemiAnalysis

**十年来英伟达首次对 AMD 处于成本劣势**

英伟达（Nvidia）本周发布了新一代 Ada Lovelace GPU 产品线。总体而言性能提升巨大：在大量使用光线追踪与 AI 渲染技术的次世代游戏中，性能最高可达 2 倍到 4 倍；采用传统光栅化技术的上一代游戏则有 1.5 倍到 1.7 倍的性能提升。这些性能提升表面上看很可观，但伴随着制造成本的大幅上升，既束缚了产品定位，也引出了可疑的营销操作。英伟达的竞争态势将处于十年来最弱的一档。我们估算的成本拆解（见文后图表）显示，英伟达相对 AMD 的 RDNA 3 可能处于成本劣势。这是绿色阵营（team green）近十年来首次在成本结构上落于下风。

提醒一下，[我们 4 月给出的 Ada Lovelace 规格信息](https://semianalysis.substack.com/p/nvidia-ada-lovelace-leaked-specifications?s=w)与英伟达本周公布的几乎完全一致。此外，[我们 4 月的裸片面积估算与实际 AD102、AD103 裸片面积相差 1%，与 AD104 相差在 2% 以内](https://semianalysis.substack.com/p/nvidia-ada-lovelace-leaked-specifications?s=w)。这让我们对本报告其余关于未发布产品线的内容相当有底气。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3420c590-8d18-4d63-966d-e4701cefb734_1433x401.png)

单看裸片面积并不算太大，但只看这个数字会产生误导——必须结合每片晶圆成本的差异：Ampere 用的是三星 8nm，Ada Lovelace 用的是台积电（TSMC）N4，而 AMD 的 RDNA 3 用的是台积电 N5/N6。

> 「今天一片 12 英寸晶圆贵得多，」他援引不断上升的芯片制造成本回应道，「摩尔定律已死……彻底结束了。」这位高管还表示，业内指望以相近成本获得两倍性能的时代「已成过去」。
>
> —— 黄仁勋，引自 [Barrons](https://www.barrons.com/articles/nvidia-graphic-card-prices-moores-law-51663778838?mod=hp_DAY_Theme_1_1)

SemiAnalysis 的信源显示，台积电 N5/N4 的晶圆成本是三星 8nm 的 2.2 倍以上。与晶圆成本上升相伴的是 2.7 倍的晶体管密度提升。英伟达的顶级裸片从每平方毫米 45 百万晶体管（MTr/mm2）提升到 125 MTr/mm2。这一密度增幅惊人，更接近跨越两个制程节点而非一个。黄仁勋说每晶体管成本的改善已显著放缓，这话没错。

由于晶圆成本高企，GPU 裸片成本大幅上涨，但裸片只是 GPU 整体物料清单（BOM）的一部分。GPU 的 BOM 还包括内存、封装、供电模块（VRM）、散热以及各种板级成本。从上一代 3090/3090ti（GA102）换到新 4090（AD102）时，这些板级成本保持不变。因此，建议零售价（MSRP）从 $1499 涨到 $1599，已足够英伟达维持利润率并带来可观的每美元性能提升。这个 MSRP 不能直接对比，因为 3090ti 如今售价 $999 甚至更低，也就是说传统光栅化渲染下的每美元性能基本持平。

再往下看 379mm2 的 AD103 和 295mm2 的 AD104，问题就严重了。这正是英伟达成本吃紧的地方。AD103 和 AD104 连同其配套的封装、内存、VRM、板卡与散热 BOM，必须以高端 GPU 的价格卖出，英伟达才能保住利润率。英伟达通常会把不同裸片分层对应到不同 GPU 档位。到了 RTX 4000 这一代，英伟达面临一个非常艰难的抉择：它没有把 AD103 放进 4080 系列并把 AD104 放进 4070 系列，而是把这两颗截然不同的裸片冠以同一个 GPU 档位。这种欺骗性营销把 AD103 命名为 4080 16GB，把 AD104 命名为 4080 12GB。必须说清楚：这是两颗差异巨大的 GPU。即便我们认为英伟达是受制于制造成本才走这条路，这一营销决策也应该受到谴责。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d10f3dea-6880-489b-a261-1d34c64ba85d_1075x391.png)

发烧友 PC 玩家社区已经坚持把 4080 12GB 称作 4070，有人甚至将其归为 xx60 级 GPU。过去，英伟达 GPU 中像 4090 那样配备 384-bit 显存位宽的被视为旗舰级（halo tier），256-bit 为高端，192-bit 则是主流 xx60 GPU。位宽并非衡量 GPU 档位的唯一标准——制造成本和性能才是。但无论如何，发烧友玩家社区对英伟达的观感正在恶化。[近期的 EVGA 风波](https://www.igorslab.de/en/evga-pulls-the-plug-with-loud-bang-yet-it-has-long-been-editorial/)也是如此：EVGA 退出 GPU 业务后，玩家把矛头指向英伟达，却没有认识到 [EVGA 本身经营不善](https://twitter.com/dylan522p/status/1570895166827024385?s=20&t=lYN0f4yvfmZOwzteBcBFKQ)——其利润率不可持续，远低于华硕（Asus）、微星（MSI）和技嘉（Gigabyte）等其他台湾厂商。

如果你喜欢我们的内容，请分享！帮忙传出去！

[分享](https://newsletter.semianalysis.com/p/ada-lovelace-gpus-shows-how-desperate?utm_source=substack&utm_medium=email&utm_content=share&action=share)

玩家把 4080 12GB 视为英伟达对他们的羞辱。按英伟达第一方数据，它在传统光栅化游戏中的表现[大致与 3080ti 相当](https://twitter.com/SkyJuice60/status/1572288601781866498?s=20&t=jeLtrm_Smo3TJnexQgTz3g)。虽然英伟达的 BOM 逐代下降，但这个 MSRP 无视了玩家眼前的市场行情。英伟达 3000 系列生产过剩，英伟达及其合作伙伴已对该档 GPU 大幅降价，英伟达甚至[计提了可观的库存减值](https://s22.q4cdn.com/364334381/files/doc_financials/2023/Q223/Q2FY23-CFO-Commentary-FINAL-with-update-for-web-post-include-tables.pdf)。市面上有大量全新与二手 RTX 3000 系列库存正以深度折扣出售。$899 的 4080 12GB 定价与全新的 3000 系列相当，且远高于挖矿退役的二手货。我们甚至听到传闻称，英伟达将 Ada Lovelace GPU 的生产推迟了一个季度，以帮助消化供应链中积压的 GPU 库存。

把 AMD 11 月 3 日将要发布的因素考虑进来，英伟达在游戏 GPU 上的处境更令人担忧。[Angstronomics 公布了 AMD 下一代 RDNA 3 架构的准确细节](https://www.angstronomics.com/p/amds-rdna-3-graphics)。这些细节得到一位 AMD 员工的独立证实，其表示封装、裸片面积与架构细节均属实。在独立第三方评测出来之前，我们先不做性能对比，但想帮大家框定英伟达相对 AMD Navi 31、Navi 32、Navi 33 的成本劣势。下表数字均以基于 AD104 的 4080 12GB 为基准（相对值）。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/bf202911-e5ce-4590-9261-f7dd1b136e72_1113x537.png)

虽然我们做了美元金额的估算，但我们不想把这些美元数字公开——否则人们会把它们外推到无穷无尽。裸片成本之上会被英伟达和 AMD 加上一层很高的毛利率。这些加价后的裸片再与内存及各种板级成本组装，华硕等厂商还会再加一层较小的组装与销售利润。我们的数字未计入这些额外利润，也未计入 VRM、散热器等板级 BOM——因为各家板卡厂商的 GPU 变体五花八门。总体而言，这些板级成本会随功耗水平线性上升，而传闻 AMD 在功耗上有优势。

我们计算裸片成本时考虑了参数良率（parametric yield）和高比例裸片拣选（die harvesting）。我们还采用了从台积电某大客户处获得的 N6 与 N5 晶圆价格。我们假设 AMD 与英伟达的采购价格相近——两者体量相当（[英伟达不得不为这些晶圆预付超过 $1B](https://s22.q4cdn.com/364334381/files/doc_financials/2023/Q223/Q2FY23-CFO-Commentary-FINAL-with-update-for-web-post-include-tables.pdf)，而 AMD 作为台积电的优待客户并未大额预付）。封装与内存 BOM 也是通过访谈业内信源测算的。

简而言之，AMD 通过舍弃 AI 与光线追踪固定功能加速器、转向更小裸片加先进封装，在裸片成本上省下一大笔。AMD RDNA 3 的 N31 和 N32 GPU 的先进封装成本显著上升，但[小型扇出 RDL 封装相对而言仍然非常便宜](https://semiengineering.com/fan-out-packaging-gets-competitive/)，远不及晶圆与良率成本。归根结底，AMD 增加的封装成本，比起拆分内存控制器/无限缓存（Infinity Cache）、用更便宜的 N6 替代 N5 以及更高良率所带来的节省，完全不在一个量级。内存 BOM 方面，通过单面 16Gb G6 或 16Gb G6x 颗粒用满了全部显存位宽。

在传统光栅化游戏性能上，英伟达很可能近十年来首次处于成本结构劣势。英伟达不顾一切要保住利润率，AD104 冠以 4080 12GB 之名定价便可见一斑。他们渠道里的 GPU 还是太多了。如果英伟达想守住市场地位，市场营销与游戏合作团队就必须突出其 GPU 表现更好的领域，例如光追和 AI 渲染。我们预计 AMD 将凭借 N33 GPU 和更优的移动 APU 在笔记本市场拿到可观份额。在桌面端，份额变化将取决于 AMD 把多少晶圆分给游戏 GPU 而非 Genoa 和 Bergamo Zen 4 服务器 CPU。我们预计 AMD 在桌面独立 GPU 的份额将升至~~30% 到 35%~~ *20% 到 25%*。AMD 可以把利润率从历史水平激进拉升至远超 50%。虽然英伟达在光追与 AI 渲染技术上仍占优势，但许多玩家更在意的是今天玩的游戏，而非行业的走向。

2022 年 10 月 12 日编辑注：在看到 4090 的官方评测以及 RDNA 3 性能的进一步信源后，我们大幅下调了市场份额预估。抱歉抢跑了。

[分享](https://newsletter.semianalysis.com/p/ada-lovelace-gpus-shows-how-desperate?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

[团体订阅享 8 折](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

SemiAnalysis 是一家精品半导体研究与咨询公司，专注于半导体供应链——从化学原料到晶圆厂，再到设计 IP 与战略。
