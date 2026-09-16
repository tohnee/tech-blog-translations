---
title: "铜之外的互连、1,000 CFET、SK Hynix 下一代 NAND、2D 材料等更多"
title_en: "Interconnects Beyond Copper, 1,000 CFETs, SK Hynix Next-Gen NAND, 2D Materials, and More"
subtitle: "IEDM 2025 综述"
date: 2026-01-13
source: https://newsletter.semianalysis.com/p/interconnects-beyond-copper-1000
crawled: 2026-09-15
authors: ["Gerald Wong", "Jeff Koch", "Randy Chiang", "DC", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 铜之外的互连、1,000 CFET、SK Hynix 下一代 NAND、2D 材料等更多

> 原文：[Interconnects Beyond Copper, 1,000 CFETs, SK Hynix Next-Gen NAND, 2D Materials, and More](https://newsletter.semianalysis.com/p/interconnects-beyond-copper-1000) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**IEDM 2025 综述**

芯片制造业正处在一个奇特的时期。一方面，我们正在爬坡进入有史以来最大的超级周期。先进逻辑、DRAM、NAND 全面紧缺，客户拿不到足够的货，芯片制造商扩产速度怎么都快不过需求，我们甚至可能很快受制于晶圆厂设备（WFE）的供给。另一方面，scaling、功耗、芯片成本等方面的技术改进速度已放缓至近乎爬行。庞大的研究投入只换来微小的渐进收益。成本在上涨，改进却渐近天花板，scaling 在「底部」已无路可走——有时感觉摩尔定律已经变成了摩尔之墙。

好消息是：半导体行业有着让唱衰者最终出丑的悠久历史。工作台上摆满了有望支撑未来十年及更远的种种创新。与 [2022](https://open.substack.com/pub/semianalysis/p/iedm2022p1?utm_campaign=post-expanded-share&utm_medium=web)、[2023](https://open.substack.com/pub/semianalysis/p/intel-genai-for-yield-tsmc-cfet-and?utm_campaign=post-expanded-share&utm_medium=web)、[2024](https://open.substack.com/pub/semianalysis/p/iedm2024?utm_campaign=post-expanded-share&utm_medium=web) 年一样，本报告将覆盖 IEDM 2025 的亮点，看看芯片制造的未来可能是什么模样。

随着内存价格暴涨，3D NAND 技术突然又变得重要起来。我们将考察 SK Hynix 最新 V9 NAND 的技术与竞争力、三星（Samsung）利用钼（Mo）改进其现有 V9 产品的做法，以及我们可能在未来 SK Hynix 量产中看到的一项重大创新。在先进逻辑方面，我们将考察铜（Cu）之外的互连金属、2D 材料在晶体管中取代硅的潜力，以及 CFET 的进展——环栅（GAA）之后的下一个重大拐点。

## **3D NAND**

NAND scaling 眼下至关重要：需求飙升，却没有无尘室空间可用于扩建产能。存储器厂商只能升级现有产线，因此其供给受限于升级后制程的密度。对一线大厂而言，这就是 3xx 层的 3D NAND 制程，可产出约 20-30 Gb/mm2 的存储密度。折算下来，单片 12 英寸晶圆可产出 30+ TB 的存储容量（注意这些缩写中 (b)it 与 (B)yte 的区别）。

### **3D NAND：SK Hynix 321 层**

就 SK Hynix 而言，321 层制程每片晶圆的容量比上一代 238 层技术多 44%。如果你受限于无尘室空间、进而受限于能产出的晶圆数量，那么每片晶圆多 44% 的容量，让升级成为显而易见的选择。

我们曾详细撰文介绍 [NAND scaling 的路径](https://newsletter.semianalysis.com/i/175661041/the-avenues-of-nand-scaling)，这里快速回顾：

> 每片晶圆 NAND 闪存存储容量的扩展有 4 条主要路径。
>
> 1. 逻辑扩展（Logical scaling）——每个单元存储的位数。这要求每个单元存储 2^n 个电压层级。
>
> 2. 垂直扩展（Vertical scaling）——垂直堆叠的 NAND 单元数量
>
> 3. 横向扩展（Lateral scaling）——在二维平面上能容纳的单元尺寸/数量
>
> 4. 架构扩展（Architecture scaling）——各种提升密度、降低单元/外围电路开销的技术。

![](https://substack-post-media.s3.amazonaws.com/public/images/3106815d-d4bb-49e5-8e6e-d90f91a5258e_1345x893.jpeg)
*来源：Western Digital*

记住，NAND 的要义就是尽可能多地把存储单元塞到晶圆上。在 3D NAND 中，这表现为垂直的圆柱形沟道，像森林里的树木一样紧密排列。平坦的、导电与绝缘材料交替的层包围着这些沟道。在沟道与导电层的每一个交点处形成一个存储单元。

![](https://substack-post-media.s3.amazonaws.com/public/images/e2a6399f-c0b9-4267-bd08-e970df1839e9_2919x1501.jpeg)
*典型 3D NAND 架构。垂直沟道与导电/绝缘交替层相交。每个导电层交点处形成一个存储单元。来源：Lam Research*

存储单元的读写基于电荷俘获材料中保持的电荷——这层材料包围着每条垂直沟道。存储在那里的电荷会改变晶体管的阈值电压（即导通晶体管所需的最低电压）。单元依据其在给定阈值电压下是否导通而被读为 1 或 0。

如今存储器厂商主要专注于选项 2——垂直扩展，因为它最便宜。增加层数意味着每单位晶圆面积上有更多存储单元。

![](https://substack-post-media.s3.amazonaws.com/public/images/993de94d-7542-412b-a97f-83ddad6ed4d1_595x466.png)
*NAND 层数正在快速增长；这是目前扩展 NAND 密度最具成本效益的方式。来源：SK Hynix*

最便宜不等于最容易。增加 NAND 层数存在非常非常多的挑战，正因如此，当巨头之一分享其部分实现技巧时，就格外值得关注。

从 238 层 V8 代到 SK Hynix 321 层 V9 的主要变化，是增加了一组 deck（叠层）和 plug（栓塞）。deck 是一次性加工的一叠水平层，由导电与绝缘层交替构成。先沉积这些层，然后完成图形化和接触孔的部分刻蚀（每个导电层都需要一个接触孔来访问由该层作为栅极控制的晶体管——这就是存储器的字线 wordline），然后刻蚀沟道孔，并用多晶硅及其包裹的电荷俘获层将其填充。你在图中看到的「plug（栓塞）」一词，指的就是这个完工的、填充好的、把孔堵上的沟道。

这就是完成单个 deck 的工艺。通过在既有 deck 之上重复整套循环，可以制造更多 deck。这同样困难，因为各 deck 之间需要极佳的对准——新的 plug 必须直接建在既有 plug 之上——而随着数百层不完美的层彼此堆叠、应力不断累积，晶圆会开始翘曲和弯曲。

SK Hynix 这篇论文的大部分内容都在讲如何更好地连接各 deck，并应对新增的近 100 层。他们声称采用了低应力材料、改进的套刻（overlay）控制，以及「局部施力」控制（可能是背面应力控制膜）。

当你试图在单个 deck 里做更多层时，刻蚀和其他工艺步骤会变得越来越困难。SK Hynix 的极限似乎在 120 层左右。沟道刻蚀要刻出深宽比约 1:100 的笔直均匀圆柱体，很难保证良率。这需要高深宽比刻蚀设备——如今采用低温刻蚀（cryo etch）——该领域 [Lam 长期占据主导，而 TEL 正在蚕食](https://newsletter.semianalysis.com/p/nand-flash-monopoly-broken-tokyo)。这是 NAND 生产中最重要的设备之一，也是最难制造的设备之一。

当单个 deck 的层数无法再增加时，就只能增加 deck 的数量。这会新增大量工艺步骤。SK Hynix 表示，从 V8 到 V9，总工艺步骤增加 30%，刻蚀步骤增加 20%。WFE 多头们先别激动：层数增幅接近 35%，所以层数的增长仍快于工艺步骤的增长。

![](https://substack-post-media.s3.amazonaws.com/public/images/e84ba74b-fa14-4904-8069-77060cf93a06_772x483.png)
*SK Hynix 各代 NAND 并排对比。V8 之后 deck/plug 已无法再加高，只能增加第三个 deck，推高了复杂度和成本。来源：SK Hynix*
![](https://substack-post-media.s3.amazonaws.com/public/images/ce487726-7c0b-4d4a-9045-3dffb63015a5_3060x1600.png)
*SK Hynix 横向扩展：block 间距缩小 11%，狭缝（slit）之间做到 16 行、无虚设行（dummy row）。来源：SK Hynix*

技术固然有趣，但 SK Hynix 321 层 V9 产品的商业处境并不算好。其 21 Gb/mm2 与美光（Micron）276 层 G9 相当，但美光只用 2 个 deck 就实现了这一密度，成本将明显更低。而 Sandisk/铠侠（Kioxia）即将推出的 332 层 BiCS10 有 3 个 deck，密度将远超前者：TLC 达 29 Gb/mm2（TLC 的含义下文详解），QLC 已演示超过 37 Gb/mm2。不过，3 层 deck 堆叠带来的 WFE 强度提升和生产方法，在 SK Hynix、美光和三星之间应当大体相似。注意，三星完全跳过 3xx 层：从 V9 的 286 层、2 deck 直接迈向 V10 的 43x 层、3 deck。

### **3D NAND：三星的钼**

在 IEDM 上，三星展示了对其现有 V9 286 层技术的改进。从 V5 起，他们一直用钨（W）作为字线金属，也就是存储位单元中的栅极金属。这次，他们展示了改用钼（Mo）带来的显著性能提升。

相比用 W 制造，Mo 在几乎每个方面——化学、机械、电气——都更难。Mo 的 ALD 化学不如 W 成熟，而且容易氧化，导致性能劣化。沉积出来的 Mo 应力变化往往更大（部分源于 ALD 工艺不够成熟），更容易让晶圆翘曲甚至碎裂。

但好处值得这些麻烦：三星声称，采用 Mo 后接触电阻降低 40%——当你要读取一股本就微弱、却必须串联流过 300+ 个各自带接触电阻的单元的电流时，这一点至关重要。读取时间改善超过 30%，寿命测试中的失效率降低 94%。

他们没有详述 Mo 集成中的每一个挑战及其解法，但确实提到了 ALD 化学，这一点很有意思。他们不直接沉积金属钼，而是先生长一层 MoN 种子层，再将其转化为纯 Mo。在纯 Mo 种子层之上可以生长更厚的体材料，最终得到无衬层（linerless）的高质量 Mo 层。传统上需要衬层（liner）来防止金属迁移和随时间劣化，但衬层不导电且占据面积。无衬层工艺还能在未来节点带来更好性能和进一步微缩。

![](https://substack-post-media.s3.amazonaws.com/public/images/e954a11b-b41b-46db-9c59-caa433365be9_703x172.png)
*沉积无衬层 Mo 层的工艺。先沉积一层 MoN 衬层，再转化为纯 Mo。注意该工艺不需要氟，降低了对邻近介质材料的威胁。来源：三星*

Lam 正在主导 Mo 沉积设备，从 AMAT 的 W 设备手中夺取份额，并击败 TEL 等对手。

层数扩展是当下扩展 3D NAND 最容易、最具成本效益的方式，但芯片制造商仍在推进上面列出的其他路径。NAND 分会场最激动人心的论文正是关于另一条路径：SK Hynix 展示了一种新的逻辑扩展方法。

### **3D NAND：SK Hynix 多位点单元 / 每单元 5 比特**

前文谈到，NAND 位单元通过单元存取晶体管的阈值电压来编码信息。不同的阈值电压对应存储单元的不同状态，而阈值电压由晶体管沟道周围电荷俘获层中存储的电荷决定。如果你的单元有 2 个可区分的阈值电压，它就能存 1 位信息，因为它可以被读为开或关。编码 2 位需要具备 4 个可区分阈值电压的能力，3 位需要 8 个，以此类推。常用命名是：SLC（单层单元）每单元 1 位，MLC（多层单元）每单元 2 位，TLC（三层单元）3 位，QLC（四层单元）4 位。

好处在于：在单元中存更多位，不需要增加芯片面积或层数，就直接提升总存储容量。QLC 今天已经普及，但每单元 5 位连个通用缩写都没有，更遑论有人量产。

现在，SK Hynix 做到了。他们展示了一种实现每单元 5 位 NAND 的巧妙架构。关键概念是把沟道分成两个半圆柱形的「位点（site）」。每个位点可以充当一条独立沟道，相当于把沟道数量翻倍。这些半圆柱沟道的性能不如更大的完整圆柱，所以存储单元数量并不会直接翻倍。但每单元存 5 位变得容易得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/444859b7-1f83-46b9-a513-64c08a1f4628_704x301.png)
*从传统 NAND 单元读出 32 种不同状态几乎不可能，感测裕度太窄。从 2 个多位点单元各读 6 种则使其变得可行。来源：SK Hynix*

在传统架构中，要实现 5bpc 存储，每条沟道需要能存储 32 个可区分的阈值电压（Vt）层级。假如你把阈值电压的总范围想象为 1V，每个 Vt 台阶就只有 1/32 伏。而在这种多位点架构中，每个位点只需读出 6 个可区分的 Vt，通过成对读取一组 2 个位点，就足以得到 36 个可区分状态（足够 5bpc 还多出几个未用状态）。记住，2 个位点的占地大致与 1 条传统沟道相同，所以最终结果是 36 个容易读取的 Vt 状态，而不是 32 个极难读取的状态。

当然，有代价：这种结构制造起来很难（即昂贵）。刻蚀高深宽比沟道并向其中沉积多层高质量薄膜，本就是 3D NAND 的关键挑战之一。这种多位点工艺要求把每一个孔精确地一分为二，在中间沉积一道墙，然后再往一个奇怪、不对称的新形状里沉积传统材料。SK Hynix 已在研发环境中证明其可行，但目前来看该技术恐怕不具成本效益。

![](https://substack-post-media.s3.amazonaws.com/public/images/87226b05-02c9-4670-b0d7-0c3ea48c1743_406x504.png)
*SK Hynix 多位点单元 NAND 架构的制造概览。把一个椭圆一分为二、在高深宽比的不对称孔中沉积薄膜，将是大批量生产中良率的巨大挑战。来源：SK Hynix*
![](https://substack-post-media.s3.amazonaws.com/public/images/fe98ab61-b468-48fd-a633-33083343fdad_561x415.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/af08539a-0dcd-4c52-aeaa-0ca4faad7d45_561x415.png)
*尽管制造存在挑战，SK Hynix 仍成功在晶圆上做出了可工作的器件。此次演示的尺寸和存储密度未知。来源：SK Hynix*

## **下一代互连：三星的钌**

随着半导体节点微缩至 10 nm 以下，传统铜（Cu）互连遭遇了由「尺寸效应」引发的关键瓶颈：随着阻挡层与衬层的相对体积占比上升，电阻率急剧攀升。为应对这一挑战，业界已开始探索以钌（Ru）作为更优的替代方案。
三星介绍了通过钌原子层沉积（ALD）实现的晶粒取向工程（Grain Orientation Engineering），获得了 (001) 取向占比 99% 的高度织构薄膜。与传统的溅射（PVD）或常规 ALD 工艺相比，该方法显著降低了晶界处的电子散射。实验结果表明，在横截面积仅 300 nm² 的超精细互连中，采用取向工程制备的钌线电阻降低 46%。此外，在环栅（GAA）FET 结构上的 TCAD 仿真显示，采用高织构 Ru M1 线可实现 **26% 的 RC 降低**。

![](https://substack-post-media.s3.amazonaws.com/public/images/5d29ed9f-cecc-4a5b-be46-49b2440e92d8_447x317.png)
*为填充 3D 结构和超精细通孔（via），该研究团队开发了「无抑制剂」的区域选择性沉积（ASD）工艺。来源：三星*

通过精确设计的「超循环（super-cycle）」步骤，利用臭氧回刻（etch-back）去除侧壁上多余的成核点，实现完美的自底向上（bottom-up）填充。更重要的是，沉积出的钌在热处理后发生再结晶，合并为近乎单晶的结构。这使得垂直电流方向与低电阻的 c 轴完全平行，从而最大化器件的导电性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/2840cf54-a232-4921-895d-7a47babfb366_655x316.png)
*来源：三星*

## **下一代互连：IMEC 16nm 间距钌金属**

根据 imec 公布的路线图，存在两个关键拐点：

- A14 到 A10 节点：这标志着从铜到钌的过渡，至少从 M0 层开始，因为在极精细尺寸下，钌的电阻率敏感度低于铜。
- A7 节点：在这一代引入 18 nm 或 16 nm 间距。一旦达到 16 nm 间距，这可能代表单次曝光、高数值孔径（High-NA）EUV 光刻所能达到的实际极限。

![](https://substack-post-media.s3.amazonaws.com/public/images/dd4ecb2e-ce65-4e4c-b71f-75e397646b46_727x295.png)
*来源：imec*

为什么需要完全自对准通孔（Fully Self-Aligned Via）？
在 16 nm 间距下，通孔关键尺寸（CD）约为 8 nm，间距同样约为 8 nm。如此极端的尺寸带来重大挑战：

- 空气间隙保护：为优化 RC 延迟，钌互连通常需要空气间隙（air-gap）结构。如果通孔开孔过大，可能不慎击穿下方的空气间隙，导致失效。
- 可靠性：自对准可以显著改善 TDDB（经时介质击穿，Time-Dependent Dielectric Breakdown）寿命。

![](https://substack-post-media.s3.amazonaws.com/public/images/517f0b93-0926-4603-bcbc-701e52a0618a_592x441.png)
*来源：imec*

整体工艺流程如下：
首先用低 NA EUV 光刻对叠层和光刻胶进行图形化。接着，通过干法与湿法刻蚀的组合，把图形转移到硅层。然后进行间隔层（spacer）沉积和回刻，以实现双重图形化。之后进行 CMP（化学机械抛光）实现表面平坦化，最后选择性去除 SiN。

![](https://substack-post-media.s3.amazonaws.com/public/images/8a358a0c-9e63-4b73-bed2-d8e37f286142_613x307.png)
*来源：imec*
![](https://substack-post-media.s3.amazonaws.com/public/images/fdbd99cb-609e-4739-bf79-c969c03fb9b9_686x327.png)
*来源：imec*

两层金属工艺：

- M1 形成：钌刻蚀之后，填充氧化物并用 CMP 平坦化，选择性地停在 SiN 层上。
- 通孔开孔：沉积 5 nm TiN 硬掩模，进行光刻，然后先刻蚀 TiN，接着选择性刻蚀 SiN 以进行通孔刻蚀
- 自对准：结合温和氧化与湿法清洗去除沟槽底部，形成完全自对准的通孔。随后，沉积约 15 nm 的 CVD Ru 并进行 M2 图形化。

![](https://substack-post-media.s3.amazonaws.com/public/images/e6eafda4-673c-4b5f-a184-c5aac8ecf0b8_697x321.png)
*imec 成功在 16 nm 间距下实现两层钌互连，良率超过 80%。来源：imec*

## **2D 材料**

二维过渡金属硫族化合物（TMD）不断在逻辑器件的讨论中翻热，原因与硅在栅长推进到 10 nm 以下区间时不断受挫是一样的。一旦沟道与静电控制被迫进入超薄几何形态，关态泄漏就不再是设计层面的烦扰，而成了物理之墙——其驱动力是源漏直接隧穿。TMD 始终是控制泄漏的少数可行抓手之一，因为更大的带隙与更高的有效质量可以抑制隧穿。这恰恰在常规硅 FET 于极短栅长下开始严重泄漏之处显得重要。

问题在于，这已经不再是单层物理的故事，而是制造的故事。第一道闸门是量产制造：无论器件架构在纸面上多么优雅，只有能在 300 mm 产线上重复产出同样结果，行业才拿得到回报。许多用于获得高质量 2D 薄膜的合成条件都附带沉重的集成代价，包括可超过约 800 °C 的生长温度，以及与前驱体和化学试剂相关的更广泛的环境与安全问题。正因如此，近期的务实路径越来越强调相对低温的转移式集成，imec 今年重点推介了与 300 mm 兼容的干法转移，作为减少空洞形成、改善转移后均匀性的手段。与此同时，转移仍然难以扩展到真正的半导体量产规模。在 300 mm 目标晶圆上直接生长依旧是长期目标，而非可有可无的加分项。

![](https://substack-post-media.s3.amazonaws.com/public/images/8b2a2f8a-2305-410c-bea0-345b18beac1e_825x691.png)
*来源：Cheliotis & Zergioti，雅典国立技术大学（NTU Athens）*

一旦接受近期之战在集成，下一场战斗就更加不留情面：接触。性能必须提升以满足工业要求，而接触电阻一直是焦点，因为它决定了器件是否受接触限制。大量先前工作报道了 MoS₂ 在特定接触方案下的低 n 型接触电阻，但小字条款是：这些结果往往是在高 VGS 和 VDS 下演示的，而那并不是产品所在的工作区间。相关的目标区间是低压工作：|VGS| < 1 V、|VDS| < 0.1 V、接触电阻 Rc < 100 Ω·µm。这重新框定了目标：你需要在低偏压下就具备高载流子浓度，使 Rc 能在真实工作条件下（而不仅仅在过驱动下）向量子极限靠拢。

![](https://substack-post-media.s3.amazonaws.com/public/images/40e0e977-52c4-475f-b8dd-20c8ad0ed089_1220x970.png)
*来源：Pin-Chun Shen 等，「Ultralow contact resistance between semimetal and monolayer semiconductors」，Nature 593, 211–217 (2021)*

CMOS 可行性接着撞上熟悉的不对称问题。P 型 TMD FET 的性能仍然不足，普遍逊色于 n 型对应器件，而这一差距看起来更多源于工艺缺陷和界面物理，而非简单的投入不足。实践中，p 型行为可能因加工中引入的缺陷向 n 型漂移，这会损害空穴注入并推高 p 型 Rc。既有研究反复指出费米能级钉扎（Fermi-level pinning）是核心机制：钉扎倾向于把费米能级锚定在更靠近导带边而非价带边的位置。这抬高了有效的 p 型肖特基势垒高度，阻碍空穴注入。另一些工作则强调金属-TMD 界面处的界面偶极子是另一个多余势能偏移的来源，进一步压制 p 型注入。含义很直白：高 p 型 Rc 仍是第一性的瓶颈，p 型工程必须跟上，「TMD 版 CMOS」才能不只是一句口号。

![](https://substack-post-media.s3.amazonaws.com/public/images/8e617273-2079-459b-a7f4-75884e1d4c6b_816x674.png)
*来源：Yoon, H.H., Park, J.Y., Megra, Y.T. et al. Enabling the Angstrom Era: 2D material-based multi-bridge-channel complementary field effect transistors. npj 2D Mater Appl 9, 68 (2025).*

即使你解决了接触和极性对称，下一个约束也不是某个英雄式的单器件指标，而是由薄膜质量和层数控制主导的波动性（variability）。转移相关和制造相关的损伤依然可见：转移良率低，堆叠层错、空位等晶体缺陷常在加工过程中被引入。层数又增加了一个波动维度。随着层数增加，带隙普遍变窄，且常从直接带隙（单层）转向间接带隙（多层），电气特性随之发生实质改变。多层在制造过程中机械上更结实，多条输运路径也能降低对局部缺陷的表观敏感度。这正是多层看起来像一种务实工程折中的原因。问题在于，双层、三层或更厚 TMD 的生长控制仍然困难，常常产出单层/多层混合区域和堆叠顺序错误，即使平均器件看起来不错，也会拉宽器件分布。

![](https://substack-post-media.s3.amazonaws.com/public/images/20297eaf-b8b5-4e16-b68b-f4151bce1d6d_1002x632.png)
*来源：Thomas, Mathew, Nair, & O'Dowd，「2D MoS2: structure, mechanisms and photocatalytic applications」*

让 TMD 始终留在牌桌上的 scaling 论据，今年在环栅（GAA）纳米片晶体管的语境下被表述得更加明确。若想在物理栅长低于约 10 nm 时把亚阈值摆幅维持在约 70 mV/dec 以下，实际上迫使沟道厚度远低于约 5 nm。如果压不住亚阈值摆幅，你要么接受过大的关态泄漏，要么提高工作电压。这就是硅问题最具体的形态：在 10 nm 以下，常规硅 FET 因源漏隧穿急剧上升而关态泄漏飙升。TMD 被定位为通过带隙和有效质量来削弱隧穿的方案，在同一几何形态下保持更低的关态电流。

![](https://substack-post-media.s3.amazonaws.com/public/images/9953ea65-fcd3-4dad-91ce-4e14690e4839_764x616.png)
*来源：Hong, Lin, Chenguang, & Jing，「Two-Dimensional Transistors beyond Silicon Counterparts: From Theory to Experiment」*

阈值控制和掺杂随后成为下一道转译屏障，因为硅的工具箱无法干净地平移过来。TMD 至今仍没有一种逻辑行业会称为「可制造」级别的实用、可靠的替位掺杂技术，原因很可能在于掺杂剂的并入和稳定性欠佳。离子注入——硅制造的主力工艺——会严重损伤 2D 材料，引入降低迁移率和器件寿命的缺陷。在这种环境下，许多研究更依赖功函数工程和界面物理：为 n 型和 p 型器件仔细选择接触金属、通过金属-TMD 界面处的费米能级去钉扎来调节 Vt、以及利用栅介质带来的电荷转移效应取代经典掺杂。这一方向最明确的架构信号之一，是台积电（TSMC）2022 年报道的 GAA 单层 MoS₂ n 型 FET，被定位为 TMD 纳米片概念可以落地的证据——至少在 n 型一侧。在台积电 2025 年 IEDM 的 2D FET 研究中，改善 p 型性能的关键抓手，是在 2D 沟道与高 k 栅介质之间插入中间层（IL），以削弱原本拖累迁移率与稳定性的屏蔽与远程声子散射惩罚。他们把结果围绕 EOT 微缩与 IL 选择来表述：在恒定过驱动（Vov = 0.7 V）下把 EOT 从约 2 nm 缩到约 1 nm，强化了静电控制，带来约 2-3 倍的导通电流（ION）提升，迟滞（hysteresis）削减约 30-40%。但亚阈值摆幅（S.S.）的改善有限，仍远未达到硅的约 60 mV/dec 基准，2D 器件仍停留在约 1xx mV/dec 区间，这说明剩余的限制不仅在栅控，还在覆盖层堆叠与 2D 沟道/界面质量本身。在 IL 化学方面，氧基 IL 会损害 ION，他们主要将其归因于制造过程中引入的更高表面粗糙度导致 S.S. 变差，这促使他们把氮基 IL 作为主优化路径；再加上抑制缺陷驱动劣化的表面预处理，S.S. 和迟滞随处理强度的增加持续单调改善。终点信号是：单层 WSe₂ 的空穴迁移率可以超过 100 cm²/V·s，这把 IL 工程加上严格的表面处理，定位为弥合 p 型差距的一条可信路径。

![](https://substack-post-media.s3.amazonaws.com/public/images/8e3a9461-9a58-4068-add3-95e18e1592d6_722x494.png)
*来源：TSMC*
![](https://substack-post-media.s3.amazonaws.com/public/images/edf694c8-1bb0-48f2-9301-cab5a0bc3adf_724x490.png)
*来源：TSMC*

到了这一步，连接触的几何形态都不再是次要细节，因为它决定了「好接触」这一概念能否被大规模重复建立。最优接触几何仍有争议，纯顶接触或纯边接触的构型在生产中都可能难以稳健实现。一些工作提出碳（C）接触、混合或复合拓扑作为可制造路径，第一性原理计算提示类 C 接触构型（包括非范德华夹层接触）性能更优。方向是明确的：行业正收敛于以可制造性为导向的折中，理论理想的重要性不如能在工艺波动中存活、同时仍交付可接受 Rc 的几何形态。

![](https://substack-post-media.s3.amazonaws.com/public/images/85f74f6e-2af9-48cc-9432-bbbaedcb5c49_1244x192.png)
*来源：J. Kang, S. Tongay, J. Zhou, J. Li, and J. Wu，「Computational Study of Metal Contacts to Monolayer Transition-Metal Dichalcogenide Semiconductors」，Physical Review X 2014*
![](https://substack-post-media.s3.amazonaws.com/public/images/ecaaf3fb-6a4c-44c4-a839-5eede7669447_1034x422.png)
*来源：Hung 等，「Mechanics of Integration and Component Performance Step-up for Nanosheet Transistors with Ultrathin 2D Channel」，2025 IEEE International Electron Devices Meeting (IEDM) (2025)*

最后，2D TMD 的发展节奏受制于物理建模的成熟度——如果 2D 器件要从实验室周期走向产品周期，这是最不光鲜、却最具决定性的约束之一。业界需要计算成本低、更真实、有预测力的仿真。今天的主流方法有二：基于 TCAD 的器件仿真和第一性原理计算。TCAD 对硅是常规操作，但面向 2D 器件的专用 TCAD 模型将变得不可或缺，而它们今天仍受限于缺乏定义明确、物理上有据可依的 TMD 物理、化学与输运参数。第一性原理方法（包括 DFT）在机理理解上仍然不可或缺，但计算成本与原子级体系尺寸的限制，制约了它们向真实器件和波动性研究的推进。连接这两个世界的高效、基于物理的工具链不是可有可无的基础设施，而是更快迭代的前提。

综合来看，今年重点展示的 2D FET 成果，读起来不像是对一种新材料的礼赞，更像一张清单，列出了 2D 逻辑要真正成气候之前必须变得「乏味且可重复」的事项：晶圆级集成路径与转移扩展的硬极限；看起来像产品约束、而非实验室偏置点的低压接触电阻目标；作为由钉扎与界面效应驱动之第一性瓶颈（而非轻微滞后）的 p 型性能；即便标题曲线亮眼、也将主导器件分布的层数控制与缺陷损伤问题。即使 scaling 叙事仍锚定在堆叠 GAA 纳米片与隧穿抑制上，这些研究也默认承认 Vt 控制与掺杂尚不成熟，将需要基于界面与介质的策略。接触几何的务实取舍与建模工具链，是未来可信进展的使能基础设施。下一个有意义的里程碑不是又一条破纪录的转移曲线，而是一次晶圆级、低偏压、统计上可信的演示——其中集成、接触、极性对称与波动性同时朝着正确的方向迈进。

*接下来，我们将覆盖本次会议最重要的议题：先进逻辑在 GAA 之后的拐点——CFET。我们将介绍 imec 的路线图，包括 CFET 何时取代 GAA、以及它可能延伸多少个节点。另一篇 imec 论文详细介绍了一种巧妙的新集成方案，无需混合键合即可在 CFET 中同时最大化 p 型与 n 型晶体管的性能。但首先是最重要的一篇论文：台积电取得的进展远超所有人的预期……*

## **CFET：台积电环形振荡器与 SRAM**
