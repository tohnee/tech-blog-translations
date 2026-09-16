---
title: "华为昇腾产能爬坡：裸片库存、台积电持续代工，HBM 才是瓶颈"
title_en: "Huawei Ascend Production Ramp: Die Banks, TSMC Continued Production, HBM is The Bottleneck"
subtitle: "H20 出货、Blackwell B30A、中国芯片产能的瓶颈、出口管制、长鑫存储（CXMT）、中芯国际（SMIC）、寒武纪"
date: 2025-09-08
source: https://newsletter.semianalysis.com/p/huawei-ascend-production-ramp
crawled: 2026-09-15
authors: ["Dylan Patel", "AJ", "Myron Xie"]
tags: ["Supply Chain", "Accelerators", "AI Infrastructure", "Semiconductors", "Export Controls", "Foundries"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 华为昇腾产能爬坡：裸片库存、台积电持续代工，HBM 才是瓶颈

> 原文：[Huawei Ascend Production Ramp: Die Banks, TSMC Continued Production, HBM is The Bottleneck](https://newsletter.semianalysis.com/p/huawei-ascend-production-ramp) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**H20 出货、Blackwell B30A、中国芯片产能的瓶颈、出口管制、长鑫存储（CXMT）、中芯国际（SMIC）、寒武纪**

算力是 AI 的命脉。谁控制了~~香料，谁就控制了宇宙~~算力，谁就将掌控 token 的生产并收获 AI 的红利。没有算力，你就没有上桌的资格。美国科技界已全面押注算力与 AI 作为下一个平台，如今正以惊人的速度扩充算力。

竞争不仅来自企业，也来自*国家*，而美国政府已出台一系列出口管制，以限制中国不断增长的算力。如今，美国[以全球已部署 FLOPS 的 70% 以上](https://semianalysis.com/accelerator-model/)执掌算力，是无可争议的领导者。保持领先的途径之一，是一边全速前进，一边阻滞竞争对手。限制竞争对手国家的算力、进而限制其智能水平，正是当前在 AI 竞赛中保持领先的政策。

这些举措引发了反弹，包括中国切断对美国的稀土矿与磁体供应。商务部长[霍华德·卢特尼克（Howard Lutnick）表示](https://www.reuters.com/technology/nvidia-resume-h20-gpu-sales-china-2025-07-15/)，恢复 Nvidia GPU 对华销售，是促使中国恢复其关键供应链材料出货的必要条件。

但约束也催生了应变，中国企业已经做出了调整。超高批大小（batch size）与分离式服务便是两个例子。尽管有所进步，以 DeepSeek 为例，其大部分 token 仍在西方硬件上完成推理。我们在近期的 DeepSeek 复盘中分析过这一动态。[DeepSeek 下一代模型的训练也因使用华为芯片而被拖延](https://www.ft.com/content/eb984646-6320-4bfe-a78d-a1da2274b092)——这一点我们在该复盘中也有提及。

这并不是一个稳定的均衡。智能竞赛中的棋局始终在变动。北京着眼长远布局，深知必须把算力命运掌握在自己手中。这里有一丝讽刺：2010 年代，中国为构筑防火长城、扶持本土产业而把 Google 赶出门外；这一次，则是美国政府扣住硬件技术，不让他们夺取 AI 领先地位。

**我们认为，中国的核心诉求是不仅要控制其互联网与 AI，还要控制支撑二者的硬件。**从硅片到 token，中国寻求对技术栈每一层的主权，而且鉴于近代历史，它绝不愿再受制于外国势力。于是，华为登场。

中国崇尚国家级冠军企业，在其特有的资本主义模式下，倾向于把资源集中输送给少数几家国家冠军。今日的冠军很可能是 Nvidia 最强大的对手：华为。我们预计华为今年能够制造数百万颗芯片，而明年将受制于 HBM 瓶颈。今天我们想谈谈华为——这个名字大致可以译作“中国的成就”。

# 全押华为芯片

华为是中国算力命运的关键一子。华为的芯片生态系统垂直整合，由设备、晶圆厂与设计构成一张能力完备的网络，使其能够贯彻硬件的全栈愿景。这套硬件令人印象深刻，尽管效率不如西方硬件。

我们此前对华为晶圆厂网络的调查，正是其网络广泛触达的一个绝佳例证。

![](https://substack-post-media.s3.amazonaws.com/public/images/b7faa941-ca23-437e-a610-e1cf902f0f55_975x615.png)
*来源：SemiAnalysis*

华为想垂直整合整个制造流程。目标不仅是自主制造作为芯片大脑的逻辑裸片，还包括内存与封装。他们甚至创立了自己的设备公司 [SiCarrier（新凯来），用于复制外国厂商的设备](https://semianalysis.com/core-research/sicarrier-huawei-wfe-announcement/)。华为已采购[超过 $9B 的设备](https://semianalysis.com/wafer-fab-model/)投入自有晶圆厂，并用于逆向工程以实现复制。

他们的努力不容小觑。例如，SiCarrier 近期完成了 $2.8B 融资。这笔钱正用于建设专门服务华为、由华为员工运营的晶圆厂。[一些关于这些晶圆厂的报道](https://www.ft.com/content/64caeab8-a326-4626-98fb-e1bf665827d3)（我们认为这些厂由华为持有并运营）显示，到明年其合计产能可能全面超过 SMIC——当前的行业龙头，也是目前生产外包的去处。随着华为自有产能发力，SMIC 的产能配给可以腾出来给其他芯片，包括寒武纪（Cambricon）。[寒武纪芯片本身在中国公司中很受欢迎，尤其是字节跳动。](https://semianalysis.com/accelerator-hbm-model/)

华为自主运营晶圆厂，不仅将显著提升中国的产量，还将提升其迭代、掌控并改进工艺的能力。华为与 SMIC 将直接致力于提升良率、打磨下一节点的研发，并增强中国半导体制造能力。

目前，所有大批量芯片生产都外包给中国领先的纯代工厂 SMIC，其中包括昇腾（Ascend）系列加速芯片以及麒麟（Kirin）手机处理器。SMIC 7nm 级制程的良率不佳，原因是工艺不成熟、出口管制，以及昇腾这类大裸片本身的高良率难度。因此，SMIC 总产能中分配给昇腾裸片的比例相对较低，因为在此阶段生产更小的手机处理器在商业上更划算。但这种情况可以迅速改变。让我们来讨论华为的可能性……

![](https://substack-post-media.s3.amazonaws.com/public/images/0a96a4af-220b-4517-b075-b813a3e86779_1024x289.png)
*来源：SemiAnalysis*

# 华为产量数据与 SMIC 的爬坡

我们的数据显示，华为 **2024 年出货 507k 颗昇腾**，其中大部分是 910B；**今年出货 805k 颗，其中 653k 颗为 910C**。910C 是更先进的版本。这包括台积电（TSMC）和 SMIC 制造的裸片。

![](https://substack-post-media.s3.amazonaws.com/public/images/d1097703-5af3-4945-abd3-d177e0e4cce3_1024x557.png)

受出口管制掣肘，SMIC 的量产起步艰难。但在 SMIC 爬坡期间，华为把昇腾裸片放到了 TSMC 生产。这违反了出口管制，华为最终获得了**超过 2.9M 颗昇腾裸片，既可用于 910B 也可用于 910C。**[我们在此详细分析过。](https://semianalysis.com/2025/04/16/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72/)

正是这批来自 TSMC 的外国芯片“裸片库存”（Die Bank），帮他们撑过了 2024 和 2025 年。没有这批裸片库存，华为的昇腾产量会低得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/24bd087c-5279-42ab-a2db-d4dede2327d4_943x625.png)
*来源：SemiAnalysis*

我们预计 TSMC 裸片库存将在未来 9 个月内耗尽。不过，SMIC 如今已有足够充裕的产能来生产可观数量的芯片。我们预测，到年底其产能充分爬坡之后，SMIC 将不再是昇腾生产的瓶颈。

![](https://substack-post-media.s3.amazonaws.com/public/images/7e2d7db4-ca8d-4708-8692-ff52f8abd9c3_1024x628.png)
*来源：SemiAnalysis*

上图展示的是 SMIC 向昇腾适度增加产能配给的基准情形。每月生产数百万颗昇腾裸片，最多只需 SMIC 每月 20k 片晶圆（wspm）的产能。

作为参照，对 SMIC 先进制程（7nm 及以下）总产能的保守估计是：2025 年底 45k wspm，2026 年增至 60k wspm，2027 年 80k wspm。此外，华为正在建设自有晶圆厂（并非全部受出口管制约束），并与 SMIC 在工艺技术上合作，因此先进制程的产量还有更高的爬坡空间。

若把 100% 产能都分配给昇腾裸片，其年产能可达数千万颗。他们有望完全有能力支撑中国本土对国产计算裸片的庞大需求。

![](https://substack-post-media.s3.amazonaws.com/public/images/e783043c-c608-41d9-9485-463efd574b0f_1024x647.png)
*来源：SemiAnalysis*

我们上述预测对良率及其未来改进速度均采用保守估计。随着 SMIC 7nm 级节点走向成熟，其表现很可能超出这些预估。我们对 SMIC 良率的估计，低于 TSMC、Intel、三星（Samsung）、ASE、Amkor 等在前端晶圆和封装上的水平。

![](https://substack-post-media.s3.amazonaws.com/public/images/ab82fa42-76b8-4cf1-861d-2561586f98e8_1024x554.png)
*来源：SemiAnalysis*

的确，良率是可以在不追加产能配给的情况下提升产量的重要杠杆。只要良率小幅超出我们上述预测，SMIC 就能在比原本更低的配给量下生产数百万颗昇腾裸片。每一个百分点都举足轻重，SMIC 已派出最优秀的工程师专攻这一难题。

![](https://substack-post-media.s3.amazonaws.com/public/images/6489670c-ac91-4620-9a21-94f4a554b74b_1024x301.png)
*来源：SemiAnalysis*

换句话说，**SMIC 只需要很小的配给比例——低至个位数百分比——就能最早在明年初生产超过一百万颗裸片。**产量提升到两三百万颗也是可能的，需要的只是更多配给。基于上述理由，我们认为外界报道的 20 万颗（200k）昇腾芯片这一数字严重失准。

SMIC 正在扩张，且已不再是昇腾生产的瓶颈；与此同时，华为的长期抱负还包括自建晶圆厂网络。我们在[《晶圆厂打地鼠》（Fab Whack-A-Mole）报告](https://semianalysis.com/2024/10/28/fab-whack-a-mole-chinese-companies/)中指出：

> 华为显然在充分利用这一窗口：2024 年晶圆厂设备（WFE）支出达 $7.3B，同比增长 27%。他们从 2022 年的实际为零，两年内跃升为全球第四大 WFE 客户。

自我们于 2024 年秋发布该报告以来，华为的晶圆厂建设若有变化，那便是加速了。其半导体相关空壳公司的生态系统正在扩张。大规模的新洁净室建设正在进行。加之国产设备选项的改进，以及可能分流超过 $30B 的晶圆制造设备进口，意味着他们很可能也有能力为这些晶圆厂配置设备。个中细节足以另写一篇报告，但一言以蔽之：华为仍在以庞大而集中的投入，谋求掌控昇腾供应链的每一个垂直环节。

# TSMC 产能获取

华为目前仍在生产大量手机芯片，但从地缘政治战略角度看，完全没有理由这么做。OPPO 和小米目前都在 TSMC 投片手机 SoC，并正在扩大自研设计，以降低对联发科（MediaTek）、高通（Qualcomm）等公司的依赖。

华为可以削减其手机 SoC 生产，同时基本不占用 SMIC 的产能配给。其他中国实体持续获得 TSMC 产能，也减轻了 SMIC 生产手机 SoC 的压力，意味着更多产能可以分配给 AI 芯片。

由于其他公司可以获取 TSMC 产能，华为与 SMIC 在拉高 AI 芯片产量时，就不必担心要包揽全国的手机芯片需求。

## 出口管制的时滞利好 SMIC

SMIC 扩张策略的另一部分，是囤积大量半导体设备。管制措施按已公布的时间表出台，通常不难预判哪些内容会被纳入。

这源于他们可以钻管制落地时间差的空子。例如，美国通常将日本与荷兰公司排除在其设备出口管制之外。表面上的理由是：它们是盟国，拥有自己的出口管制体系和半导体产业。

但问题在于，当新的出口管制出台时，日本与荷兰**不会立即跟进。**许多情况下，对等管制会延迟 6 个月，甚至永远不会出台。中国企业可以紧急下单囤积数年份的设备，而美国厂商却被排除在这一过程之外。日本 WFE 厂商乐于填补这一空窗，并借加急订单把利润率养得肥厚。许多关键供应商来自中国的营收占比已远超 40%：

![](https://substack-post-media.s3.amazonaws.com/public/images/d375fbdb-a48c-4f70-8e46-74e42e8ad7e6_1024x382.png)
*来源：SemiAnalysis*

即便日荷确实跟进美国出台管制，它们对再出口（re-export）也没有任何对应管制。这意味着受限设备只要先经过第三国，就有可能流入中国。

此外，以“先进 IC”作为限制设备的门槛，也留下了可供操作的空间。[ASML 的 NXT:1980 光刻机完全有能力生产 7nm 级逻辑芯片](https://semianalysis.com/2023/01/29/the-gaps-in-the-new-china-lithography/)，而且如果经济性（产能与良率）可以无视或予以补贴，很可能还能更进一步。这些设备被允许进入中国，甚至进入 SMIC 的部分厂区。

如前所述，出口管制可以在严格执法既有机制之外进一步扩大，包括与盟国就更紧凑的对等管制时间表协调一致，并让它们接受对再出口的约束。

本届政府的[《行动计划》（Action Plan）](https://www.whitehouse.gov/wp-content/uploads/2025/07/Americas-AI-Action-Plan.pdf)令我们总体上深受鼓舞。举例来说，我们乐见其中点名了对半导体子系统的管制。这是 SemiAnalysis [一段时间以来](https://www.chinatalk.media/p/breaking-huawei-tariffs-done-right?utm_source=substack&utm_medium=email)[反复呼吁](https://semianalysis.com/2024/10/28/fab-whack-a-mole-chinese-companies/?utm_source=substack&utm_medium=email)的议题，我们认为方向正确。话虽如此，许多为西方厂商供应子系统的公司——例如瑞士的 VAT Group——在未受管制的情况下，仍将不受阻拦地向中国发运关键腔体。

《行动计划》还就全球协同防护措施提出了具体建议，我们认为若能落实，将大大缓解上文所述盟国出口管制滞后的问题。问题在于，SMIC 与 CXMT 之所以能持续扩产，是因为针对它们的制裁形同虚设。国际合作——尤其是与韩国伙伴的合作——是把事情办对的关键，必须确保中国的商业化瓶颈不被放松。韩国制造海量内存，三星历史上曾向中国大量供应内存，因此目标与执法上的紧密协同至关重要。

供应链中另一个同样关键的环节是内存。我们认为，关键约束正在于此。

# HBM 才是瓶颈

**我们认为 HBM 生产是瓶颈。中国也这样认为**——正因如此，他们才在近期的贸易谈判中要求美方官员[放松对 HBM 的管制](https://www.reuters.com/world/china/china-wants-us-relax-ai-chip-export-controls-trade-deal-ft-reports-2025-08-10/)。这一诉求没提到的东西很能说明问题：其中并不包括更多 TSMC 产能或光刻设备。北京明确要求的，是华盛顿放松对 HBM 的限制。

正如华为能够囤积 TSMC 逻辑晶圆库存一样，他们同样囤积了 HBM 库存。[三星由于未能打入西方芯片的加速器供应链](https://semianalysis.com/accelerator-model/#)，转而把产品卖给中国客户，这些库存再经中国客户之手流向华为。这正是今后必须与韩国就内存管制执法紧密合作的原因。

**仅三星一家就直接向中国供应了 1,140 万（11.4M）颗 HBM 堆叠，**其中**包括管制发布日与执法日之间那 1 个月空窗期内惊人的 700 万（7M）颗**。若计入其他供应商与其他出货途径，总数达 1,300 万（13M）颗 HBM 堆叠。

具体而言，2024 年 12 月 2 日，美国工业与安全局（BIS）宣布对 HBM2E 以上的更先进产品实施管制，并要求于 2024 年 12 月 31 日前完全合规。**三星在那一个季度里尽可能多地向中国出口。这构成了中国 HBM 库存的主体。**他们之所以能做到这一点，是因为美国政府和媒体在管制落地前数月就不断预告。

![](https://substack-post-media.s3.amazonaws.com/public/images/d8177c30-85ab-4e0e-8589-5caf37fa2468_1024x716.png)
*来源：SemiAnalysis*

管令生效之后，三星 HBM 仍流入了中国。[我们此前详述过](https://semianalysis.com/2025/04/16/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72/) CoAsia Electronics 与 Faraday 等公司如何以“非功能芯片带 HBM”的方式向中国供货；不过我们认为，由于我们在 1 月下旬的私下揭露及其后的公开披露，这一渠道如今已经停止，相关公司的营收数字也已回归正常。但这并不意味着 HBM 走私已完全绝迹，可能还有其他来源。

![](https://substack-post-media.s3.amazonaws.com/public/images/eacc8e8d-f8b4-4504-8a6d-01c9526bcb06_1024x707.png)
*来源：SemiAnalysis、公司报告*

总而言之，**中国已采购 1,300 万（13M）颗 HBM 堆叠，足以支撑 1.6M 个昇腾 910C 封装**。尽管如此，我们预计**到今年年底中国将因外国 HBM 耗尽而遭遇 HBM 瓶颈**。

![](https://substack-post-media.s3.amazonaws.com/public/images/0cd3fa39-d0d4-4cc2-80b7-239979c609ca_1024x509.png)
*来源：SemiAnalysis*

凭借 TSMC 和 SMIC 的产能，中国今年完全可以制造超过 **805k 颗华为昇腾**，**但他们不会这么做，因为 HBM 不够。**

我们预计 SMIC 今年将生产 1M 颗 910C 和近 50 万颗 910B，但由于 HBM 缺货，并非所有裸片都能做成 ASIC。如果有一部分 HBM 经走私渠道流入，华为就能生产更多昇腾 AI ASIC。

## 没有外国 HBM，中国就没有本土 AI 加速器产业

若无法获得更多外国 HBM，华为明年连 100 万颗昇腾芯片都造不出来。他们必须完全依赖国产供给，下文将详细展开。一旦这批 HBM 库存耗尽，Nvidia 与 AMD 在中国实际上将没有任何竞争。

中国的另一个选项是使用速率更慢的 GDDR 和 LPDDR 内存，但对于采用现代强化学习技术的前沿大模型、以及大规模推理部署而言，这些内存并不适用。

## 国产 HBM 产业——CXMT

中国最主要的 DRAM 厂商长鑫存储（CXMT）正快速追赶西方。这得益于几方面因素的叠加：极强的本土工程能力，从三星、SK 海力士、美光（Micron）挖角工程师，以及应用材料（Applied Materials）、泛林（Lam Research）、东京电子（Tokyo Electron）等一流设备厂商向其传授子工序。

CXMT 已能出货 DDR5 内存，仅落后 SK 海力士、美光、三星数年，此前专供 PC 和移动端的 DDR4 生产虽仍盈利，也正在收缩。虽然其 HBM 出货量还不大，但路线图非常激进。到明年，其产能将与美光比肩，但仍不足以拯救华为昇腾的产量。我们预计 2026 年其产量将达 257k WPM（每月晶圆投片量），接近全球 DRAM 产量的 15%；按我们的估算，到 2030 年将扩展至 490k。

![](https://substack-post-media.s3.amazonaws.com/public/images/a3181910-0872-4be2-90ff-d0e55d4dc206_1024x875.png)
*CXMT 位于合肥的 DRAM 与 HBM 生产厂区，全球规模最大之一。来源：SemiAnalysis。*

CXMT 的重心转移与产能爬坡，部分得益于来自官方的投资。2024 年 5 月启动的中国“大基金三期”向该公司投资了 $2B。CXMT 也在上海与北京两地扩张布局，并在上海设立 HBM 封装子公司。

CXMT 曾预期会被美国政府列入实体清单（最终得以避开），于 2024 年囤积了数年份的设备，并且很可能仍在追加 HBM 专用设备。CXMT 至今未被列入实体清单！尽管 HBM 被明确列为那轮管制的重点目标，上届政府却漏掉了中国的 HBM 头号选手。**特朗普政府需要立即纠正拜登政府留下的这一失误。**

囤货之所以重要，是因为先进设备（如韩美（Hanmi）用于 HBM3 的 TCB 键合机）已受管制，但这些设备并非不可或缺——旧款设备可以放慢速度运行，对成本影响不大。更重要的是，CXMT 仍可通过日本供应商，采购用于硅通孔（TSV）成形的前沿设备——这正是制造 HBM 的关键环节。此外，长电科技（JCET）、通富微电（Tong Fu）等中国 OSAT 厂也在加紧研发，并为承接 CXMT 前端 HBM 晶圆封装的关键 TSV 与堆叠工序扩建产能。这与西方内存巨头将这些工序垂直整合于自身内部的做法不同。这是中国产业发展的典型模式：鼓励多家玩家发展本土制造能力，形成加速发展速度的你死我活竞争。因此，管制不能只盯着 CXMT，而必须覆盖整个中国——因为关键工序总可以外包出去。

**由于前端逻辑芯片目前并非硬约束，北京在贸易协议中的主要诉求便集中于 HBM，以及放松针对这一类设备的管制**。鉴于 HBM 的重要性，必须理解 CXMT 在不同产能分配情形下的未来产量。

# CXMT 产量预测

事态有多种走向，取决于有多少晶圆产能划给 HBM。以不到 50% 的晶圆产能，中国就可以轻松生产数千万颗堆叠。CXMT 目前月产能略高于约 250,000 片，预计到年底达到 300,000 片。

目前他们尚未配齐把标准 DRAM 产线转换为 HBM 所需的设备，但这一转换不可避免。设计得当的精准制裁可以大幅拖慢这一转换。

![](https://substack-post-media.s3.amazonaws.com/public/images/99319b48-6c1d-41d4-9861-747155dadc24_1024x763.png)
*来源：SemiAnalysis*

不同的情形对应不同的华为昇腾产量。如前所述，SMIC 有能力生产与 HBM 供给相匹配的裸片。

![](https://substack-post-media.s3.amazonaws.com/public/images/42800f32-cc9b-4869-8ef9-2d1f176df486_1024x769.png)

需要说明，局势可能生变。如果 CXMT 继续囤积关键设备或显著提升良率，其产量增速还可能加快。中国制造能力与产能的潜力没有边界。我们的这一估计偏保守——CXMT 很可能在 2026 年就能生产能力强得多的 HBM3e。

**我们认为 CXMT 明年只能生产约 200 万（~2 million）颗 HBM 堆叠，仅够支撑 250,000-300,000 颗昇腾 910C。**良率提升与产能转换都需要时间，CXMT 才能押上可观产能。

![](https://substack-post-media.s3.amazonaws.com/public/images/3db74357-492f-4ef2-86e7-d554edefa682_1024x563.png)

如果所有前沿逻辑裸片产能都能配上 HBM，华为昇腾产量将从今年的 805k 增至 2025 年的 1,175k。更重要的是，**明年产量将从 300k 增长到超过 500 万（5 million）颗昇腾 910C！**

**我们的分析表明，出口管制在约束和限制中国芯片产能方面是有效的。**假设不存在走私，中国明年能造出的昇腾只会*更少*，而非更多。CXMT 被*卡得死死的*。倘若没有管制，昇腾的爬坡将完全兑现，中国模型将大规模运行在华为昇腾上，算力将充裕到 DeepSeek R2 和 V4 这类先进模型早已问世。更不用说，若产能更充裕，中国将更有条件用自家芯片输出其 AI。

因此，确保出口管制的落实、执法与持续更新，以阻止 CXMT 及相关实体扩产，绝对至关重要。如前所述，这不仅包括 CXMT，还包括与其合作的 OSAT 厂及子公司。其次，情报界追踪并识别任何 HBM 走私行为也很重要，[例如我们 1 月私下揭露、其后公开报道的 Faraday + CoAsia 方案](https://semianalysis.com/2025/04/16/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72/)。

**绝不应允许 HBM 被运进中国。**未来几年 AI 芯片的产量，在很大程度上取决于 CXMT 的爬坡与外国 HBM 的出货。

把 HBM 运进中国的动机极其强烈。这正是管制执法如此关键的原因。

中国生产战略还有另一个支柱，独立于内存与逻辑之外。这个支柱关乎芯片的互连组网，以及这些芯片在哪里制造。

# 网络与数据中心 CPU

芯片并非孤立存在。多年来我们一直主张，[系统比微架构更重要](https://semianalysis.com/2023/04/12/google-ai-infrastructure-supremacy/)。集群由数以万计互连的芯片组成，而它们如何互连至关重要。

我们在下文中详细解析了华为的 CloudMatrix 384（简称 CM384）系统。

我们认为，所用的网络设备——具体说是纵向扩展交换机——正通过空壳公司在 TSMC 而非 SMIC 生产。我们还认为他们正在囤积这类设备。

我们认为华为还成功在 TSMC 制造了其数据中心 CPU。这表明现行旨在限制华为获取 TSMC 产能的管制并不充分。昇腾 AI ASIC 是 7nm，但由于筛查不严，华为得以从更先进的 TSMC 5nm 节点获取技术。

![](https://substack-post-media.s3.amazonaws.com/public/images/37cae26b-6364-4944-b04b-907174bffdc8_1024x470.png)
*华为鲲鹏 930。来源：Kunal、SemiAnalysis*

把这些芯片放到 TSMC 生产，就腾出了 SMIC 的产能，意味着在 HBM 允许的前提下，可以把更多配给分给昇腾或[寒武纪](https://semianalysis.com/accelerator-hbm-model/)项目。正如本报告前文所述，这是一个关键变量。如果网络设备必须由 SMIC 生产，昇腾可获得的晶圆配给将被显著挤压。

中国有十足的动力把尽可能多的生产转移到 TSMC。他们过去就使用过空壳公司，且有充分证据表明如今仍在这么做。尽管围绕 KYC（了解你的客户）与危险信号（red flags）已实施了一些做法，我们认为现行框架仍不充分。

# Nvidia 与华为：Blackwell 和 H20

美国政府此前禁止 Nvidia H20 芯片进入中国，但最近表态将向 Nvidia 发放该芯片的出口许可。正如我们此前指出的，H20 是一款有实力的芯片，内存比被禁的 H100 更多，尽管 FLOPS 少得多。更大的内存对推理性能有帮助。

Nvidia 至少将出售其现有的 H20 和 H20E（内存更多的版本）库存。这将带来超过数十万颗芯片、数十亿美元的营收。

还有[报道称](https://www.reuters.com/world/china/nvidia-working-new-ai-chip-china-that-outperforms-h20-sources-say-2025-08-19/)将推出基于 Blackwell 系列的更先进版本。该芯片内存与 H20 相当，但 FLOPS 将显著更多。具体而言，B30A 的 FLOPS 可能是 H20 的 10 倍以上，远超出口管制阈值。B30A 或将定位为 B300 的一半价格、一半性能。应对之道相当简单：买两倍的芯片获得同等性能即可。鉴于[机器学习负载中强扩展与弱扩展的原理](https://hpc-wiki.info/hpc/Scaling#Strong_or_Weak_Scaling)，这是一条保持竞争力的可行路径。

支持向中国出货 B30A 的理由是：中国对 H20 的兴趣已然下降。这在很大程度上源于中国政府对主要科技公司的施压。尽管外界普遍宣称中国对 H20 的兴趣下降，我们并不相信这是事实。

具体而言，我们不认为这反映了中国对算力或外国芯片的真实需求。这是一项自上而下强推的错误政策，一旦华为耗尽 HBM、无法再生产更多昇腾芯片，它就会被逆转；甚至可能是一场精心编排的边缘政策，目的是为更强的芯片拿到放行许可。

这一消息紧随其他新闻而来，例如 [DeepSeek 无法在华为芯片上获得可接受的性能](https://www.ft.com/content/eb984646-6320-4bfe-a78d-a1da2274b092)。这并非巧合。出口管制正在起效，而进步的最大阻碍正是算力。

中国或许正试图通过心理战，让性能强劲得多的 Blackwell 芯片获批入华。H20 和 H20E 的软件比 910C 好得多得多，可以说它们同属一个量级；但 B30A 将独占一个量级，这一点毫无争议。鉴于 H20、H20E，尤其是 B30A 都擅长推理，这也让中国公司有更多算力来服务其模型与应用。

这将使他们能够在自有的硬件上输出中国 AI。这将扩大中国 AI 与中国应用的渗透，不可避免地抢占美国应用的市场份额。美国的 AI 技术栈是“运行在美国芯片上的美国 AI”，而不仅仅是芯片本身。

**美国需要在让中国留在美国 AI 技术栈上、放慢其自研步伐的同时，限制流入中国的芯片质量与数量**，在两者之间取得平衡。

H20 被允许进入中国，但**考虑到中国的国产能力，向中国出货更强芯片的进程必须受到严密守护与紧盯**。

**只有当中国显然能够大批量交付与 H20E 具竞争力的产品时，美国才应该上调输华芯片的档次。**

无论具体 SKU 为何，出口许可都带来以下几点影响，下面逐一讨论。

## 算力外交的影响

首先，这意味着 DeepSeek、阿里巴巴等头部玩家将有更多芯片用于强化学习（RL）。RL 是当前推动进步的重要引擎。RL 的算力消耗大部分是推理，而这正是 H20 尤其是 H20E 所擅长的。B30A 的表现还会更好。

DeepSeek 等玩家原本就有足够算力持续改进——R1 在类似 o1 -> o3 的时间线上，迎来了性能大幅提升的重要更新。不过我们坚信 GPT-5、Claude 4 和 Grok 4 仍显著领先于 R1，尤其是在智能体任务上。

然而，AI 的问题靠两样东西就能解决：**人才与算力**。DeepSeek 从来不缺前者，如今后者也将更加充裕。我们预计，随着任何进入中国的芯片大批量到位，DeepSeek 的进步速度将显著加快。DeepSeek 有意在 V4 中发布多模态模型，但算力匮乏正在拖慢进度。

阿里巴巴（Qwen）与月之暗面（Moonshot，Kimi K2）也尚未推出大型多模态模型，受算力所限目前主要专注于文本。它们今年将发布多模态模型，但在许多能力上仍明显落后于 OpenAI、Anthropic 和 Google。如果 Blackwell GPU 出货过早，将加速中国的步伐。

第二个重大影响是，中国将有更多算力向本国民众提供模型服务与推理。算力约束影响用户体验——DeepSeek 曾[刻意以低速向用户服务 R1，以节省算力](https://semianalysis.com/2025/07/03/deepseek-debrief-128-days-later/)。

算力不足带来的糟糕用户体验，极大限制了中国部署 AI 的能力。随着用户体验改善，普及率与 AI 的经济效益也将随之提升。很容易想象这样一个未来：模型在 H800 上预训练、在 H20 上后训练，再由昇腾和 H20 向民众提供服务。AI 产品的需求如此旺盛，只要服务这些模型的算力再多一点，立刻就会被填满。中国模型选择开源的原因之一，就是可以让别人替它们部署服务。一旦算力充裕，模型便可闭源，对美国供应商的依赖也可切断。

所谓“在某种芯片上训练的模型必须在同种芯片上推理”的说法完全错误。Anthropic 在 GPU 和 TPU 上分别完成了 Claude 4 不同阶段的研究与训练。此外，Claude 4 的推理服务[提供于 Nvidia GPU、Google TPU 和 Amazon Trainium 之上](https://semianalysis.com/2025/01/31/deepseek-debates/)。这一切复杂性之下，[Anthropic 仍是营收增长最快的 AI 公司](https://semianalysis.com/tokenomics-model/)，并拥有迄今软件工程能力最强的模型。

DeepSeek、阿里巴巴、月之暗面等主要在 Nvidia 芯片上训练模型，我们认为这一点短期内不会改变。如果 Blackwell 版本出货，各层面的收益将更加显著。

![](https://substack-post-media.s3.amazonaws.com/public/images/b8906e10-1743-4f4c-abb1-5d649fad9d3c_1024x661.png)
*来源：SemiAnalysis*

# 中国算力一览

随着 H20 获批，中国可获取的 FLOPS 与内存将显著增加。910C 将是中国本土生产在已实现 FLOPS 与内存方面首次有分量的成果。我们还预计各类不法行为者会经再出口渠道向中国输送芯片，构成可观数量的 H100 和少量 B200。

![](https://substack-post-media.s3.amazonaws.com/public/images/0f265adf-6ec0-4a78-8ab9-da60971e32ce_1024x697.png)
*来源：SemiAnalysis*

倘若 Blackwell 版本出货，FLOPS 方面的增益将更为显著，因为该芯片的 FLOPS 多得多。在那情形下，中国最终将拥有更多 FLOPS，外加更多内存。

![](https://substack-post-media.s3.amazonaws.com/public/images/e7efaeb9-6f42-45b4-8929-d028a9d45cdd_1024x694.png)
*来源：SemiAnalysis*

更不必说，中国玩家——包括字节跳动这样的巨头——仍可通过在非受限国家租用算力的方式获取计算资源。例如，字节跳动仍可从 Oracle 和 Google 等供应商处获取顶配 Blackwell GPU。我们此前详细报道过这层关系。毫无疑问，马来西亚已成为 Nvidia 的巨大市场。出口管制在确保局面维持现状方面同样有效——[马来西亚随即与任何围绕华为昇腾的动作划清界限](https://www.reuters.com/world/asia-pacific/malaysia-government-say-not-involved-local-ai-project-involving-huawei-chips-2025-05-21/)。

租用为中国依赖 Nvidia 开辟了一条无需 Nvidia 芯片进入中国的路径——这是可行的，因为芯片并不需要身处中国。**字节跳动的 Seed 模型就是在美国、通过美国云厂商训练的。**

在马来西亚查验 GPU 比在中国容易得多。因此，这是限制不法行为者未经授权再出口的有效手段——我们认为位置追踪等方法在技术上难以落实且容易绕过。请注意，租用仍将让中国保有训练先进模型的能力。如果允许将租用算力用于模型服务，中国就有机会通过新一代、更好的 AI 应用扩散其 AI，抢占美国产品的市场份额。但关键区别在于：这种获取渠道是可以被切断的。

话虽如此，中国不会允许其数据大规模出境，因此对本土 AI 能力仍有巨大需求。向中国出售芯片并不会改变中国对硅片完全自主的执念，只会在本土产能满足需求之前为其提供缓冲。

值得记住的是，中国对硅片自主的执着早于美国出口管制。“Blackwell 必须卖给中国”的论调是错误叙事，因为华为的 HBM 很快就会耗尽。向中国出售芯片只会起到救助作用，帮其撑到国产产能上量。在实现自给自足之前，产能爬坡不会放缓。Blackwell 的出货决策必须与对国产能力的密切关注相权衡。[如果华为、寒武纪和 CXMT 的产量加速超出预期，美国就应更早提高门槛。](https://semianalysis.com/accelerator-hbm-model/)

接下来，我们将深入分析 Nvidia 在中国的前景，包括 H20 的预期营收以及即将推出的新一代中国特供芯片。我们还将比较中美算力对比——在内存与 FLOPS 两方面，美国如何对中国形成绝对主导。
