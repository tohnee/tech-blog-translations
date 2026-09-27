---
title: "英特尔 Panther Lake 拆解"
title_en: "Intel Panther Lake Teardown"
subtitle: "深入英特尔最新消费级芯片与 18A 制程节点内部"
date: 2026-09-26
source: https://newsletter.semianalysis.com/p/intel-panther-lake-teardown
crawled: 2026-09-15
authors: ["Adith Shankar", "Daniel Sanchez", "Allison Elliott", "Sarah Lawrence", "Afzal Ahmad", "Andrew Wagner", "STEEL Team", "Dylan Patel"]
tags: ["Hardware Architecture", "Chip Design", "Foundries"]
audience: only_paid
paywalled: true
translated: 2026-09-27
---

# 英特尔 Panther Lake 拆解

> 原文：[Intel Panther Lake Teardown](https://newsletter.semianalysis.com/p/intel-panther-lake-teardown) · SemiAnalysis
> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**深入英特尔最新消费级芯片与 18A 制程节点内部**

Panther Lake 首次把背面供电（BSPDN）推向商业化落地，引入了英特尔（Intel）第一代环栅晶体管（GAA），并以 Foveros-S 封装展示了其先进封装能力。随着 Panther Lake，英特尔的制造轨迹从虚无缥缈的路线图转向了实际出货的硅片——这是它重返竞争性半导体制造漫长道路上的一个重要里程碑。为了评估英特尔翻身的成色，我们对 Panther Lake 做了拆解。

![](https://substack-post-media.s3.amazonaws.com/public/images/e91f7b46-2f79-4ce2-814c-4ed684985a3e_1591x1290.png)
*英特尔 Core Ultra 7 365（Panther Lake）。来源：SemiAnalysis*

***SemiAnalysis STEEL 拆解实验室剖析先进数据中心与 AI 硬件。欲了解我们的拆解管线或委托定制拆解，请联系 [sales@semianalysis.com](mailto:sales@semianalysis.com)。***

***我们在招人：架构、版图、封装、制造与实验室专家。机会覆盖从系统到晶体管及其间的每一个环节。欢迎查看我们的[招聘页面](https://semianalysis.com/semianalysis-careers/)。***

我们的拆解从 18A 的四纳米片 RibbonFET（英特尔对 GAAFET 的营销命名）与栅叠层出发，一路追踪接触孔、正面与背面布线，直至键合的承载片。我们会解释这些材料与集成选择如何改善栅控、降低电阻，同时又引入额外的电容、热阻与工艺复杂度。我们的测量显示，Panther Lake 的 18A 计算逻辑与台积电（TSMC）N3E GPU 逻辑的逻辑密度相当。不过，在峰值密度上，18A 并不领先台积电 N3P、N2 或三星（Samsung）SF2。Panther Lake 的 CPU 核心只是渐进式更新，高端 GPU 依然采用台积电 N3E。

![](https://substack-post-media.s3.amazonaws.com/public/images/d2a71a33-864f-4814-9e63-efeb211025a8_640x302.gif)
*英特尔 Panther Lake 封装 X-ray 图。来源：SemiAnalysis*

Panther Lake 采用英特尔 Foveros-S 先进封装，把一颗计算小芯片（compute tile）、一颗 GPU 小芯片与一颗 I/O 小芯片组装在一块无源基础小芯片之上。两种计算小芯片版本均采用 Intel 18A。Xe3 GPU 有两种选择：Intel 3 上的 4 核 GT1 小芯片，以及台积电 N3E 上更大的 12 核 GT2 小芯片。两种 I/O 小芯片版本均采用台积电 N6。[1], [2]

![](https://substack-post-media.s3.amazonaws.com/public/images/70f41d1d-51ef-401b-81f5-cabe50f2b0e9_1349x769.png)
*Panther Lake 配置。PTL-U（3xx，左）、PTL-H（3x6H，中）、带 Arc B390/B370 的 PTL-H（X 档，3x8H，右）。来源：SemiAnalysis*

我们的分析以 PTL-U 计算小芯片、4 核与 12 核两种 GPU 小芯片，以及 12 通道 I/O 小芯片为中心。

# PowerVia

在传统芯片中，电源与信号都要经由同一套正面金属堆叠布线到器件前端。电源轨在晶体管附近挤占本就紧张的布线资源，而高耸的过孔堆叠则把 VDD 与 VSS 从上层粗线径金属送到局部电源轨。背面供电（BSPD）把主供电网络移到晶体管层的另一侧——晶圆背面，从而与正面信号布线分离。我们在 2024 年曾详细介绍过 BSPD 及其影响。[3], [4], [5] 英特尔的 BSPD 实现名为「PowerVia」，通过专用的背面金属把电力输送到纳米硅通孔（nano-TSV），再由后者把这些电源轨连接到局部源/漏（S/D）接触孔。

![](https://substack-post-media.s3.amazonaws.com/public/images/3333a960-a4cb-4310-95fe-91efaf9da41f_1493x851.png)
*保留的承载片、器件与正面/背面互连的示意方位。层数仅为示意；不按比例。来源：SemiAnalysis*

实现这种分离，要求英特尔从晶圆两侧分别构建互连堆叠：正面为 M0–M14 信号堆叠，背面为 BM0–BM5 供电堆叠。M0 与 BM0 分别最靠近晶体管。

![](https://substack-post-media.s3.amazonaws.com/public/images/877a2e36-a956-4c1a-befe-39823e6ab5fc_1441x1404.png)
*PowerVia 通用工艺序列，以及埋入式电源轨、PowerVia 与直接背面接触方案的对比。集成细节与层数仅为示意；示意图不按比例。来源：SemiAnalysis*

纳米硅通孔连接晶圆两侧，但英特尔是在形成接触孔之后，再从正面完成每个通孔的图形化与刻蚀。一条狭窄的通孔从接触孔侧壁一路深入硅衬底。随后英特尔完成正面信号金属堆叠，把晶圆键合到承载片上、翻转，并去除原始衬底，直到埋层通孔的顶端露出，再在露出的通孔上直接沉积背面金属堆叠。

纳米硅通孔与背面通孔的轮廓朝相反方向收窄，因为英特尔是从晶圆两侧分别加工它们的。晶体管结构构成 FEOL（前道工序）。局部接触孔与纳米硅通孔把器件连接到布线。M0 则是正面互连堆叠的起点。

硅承载片仍保留在正面互连的上方。它在衬底去除与背面加工过程中支撑器件晶圆，并保留为成品芯片散热路径的一部分。

PowerVia 把主配电网络从拥挤的正面金属中移出，改由更短、更宽的背面导线输送电力。其横向落点仍要占用标准单元内的面积，因此相比直接背面接触方案，它节省的单元面积要少一些。[3] 逻辑器件旁的纳米硅通孔把 VDD 或 VSS 从背面供电网络引下来，而信号连接则继续经由正面金属向上走线。

![](https://substack-post-media.s3.amazonaws.com/public/images/d416cb6f-2dd4-4e0a-b046-791f0a12823b_1431x918.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/e07f47dd-574d-47bb-aa0d-b399e2445562_714x460.png)
*英特尔 18A RibbonFET 与纳米硅通孔的 XTEM（上）与 EDS（下）图像。来源：SemiAnalysis*

## 背面互连

本文同时纳入三星 SF2 的数据与 Panther Lake 对比。SF2 是当前已量产的 GAA 代工节点，但没有背面供电，因而是评估 18A 的一个有用参照。对采用 SF2 制造的三星 S26 系列产品的完整拆解即将分享。纳米片截面 EDS 对比。

![](https://substack-post-media.s3.amazonaws.com/public/images/518abef6-0eaf-41ba-9bb1-59fe4088bdc1_2200x1270.png)
*英特尔 18A Panther Lake P 核逻辑（左）与三星 SF2 Exynos 2600 C1-Ultra 逻辑（右）。HFW 550 nm（英特尔）与 423 nm（三星）。来源：SemiAnalysis*

PowerVia 的供电通路从背面 Cu 电源轨出发，经 Mo 内衬的 W 纳米硅通孔，到达局部晶体管接触孔。在本截面中，这段收窄的连接从接触孔层到 BM0 约 150 nm。Ta 内衬约束 Cu 并增强与周围叠层的附着力；AlOₓ 刻蚀停止层则控制电源轨上方下一层介质的刻蚀。纳米片下方的介质把器件与背面布线电学隔离，并去除了沟道下方的导电硅体。[6]

![](https://substack-post-media.s3.amazonaws.com/public/images/5ae0c0e2-440b-4937-bf39-6afa3549f20c_2065x1024.png)
*英特尔 18A Mo 内衬 W 纳米硅通孔与 Cu BM0 电源轨。来源：SemiAnalysis*

AlOₓ 作为刻蚀停止层（ES），可实现刻蚀终点检测并保护下方各层。低挥发性的氟化铝反应产物能够抗含氟等离子体，使一层薄 AlOₓ 膜在周围 low-k 介质被去除的同时保护金属。[6], [7] BM0 以及 M1 线上方各层呈现双层 AlOₓ，而我们的 [SMIC N+3 拆解](https://newsletter.semianalysis.com/i/199606144/process-flow) 中是单层 AlOₓ。SMIC 用的是更简单的局部 AlOₓ 子叠层，其余的帽层与刻蚀序列则提供了所需的落点保护。

![](https://substack-post-media.s3.amazonaws.com/public/images/4363b1d8-2954-4dd8-8e0d-6ffedec7317a_1050x176.png)
*英特尔 18A 背面金属化材料。来源：SemiAnalysis*

那么为什么要双层？紧密排列的 AlOₓ 双层在刻蚀序列中提供了两个受保护的终点。英特尔的一份文献描述了 AlOₓ/SiN/AlOₓ 叠层，正好解释了这样做的收益：主介质等离子体刻蚀在第一层 AlOₓ 膜上停止；选择性湿法清洗打开该膜；第二次等离子体刻蚀去除中间的 SiN 并在第二层 AlOₓ 膜上停止；最后一步湿法清洗露出金属落点表面。在英特尔公开的示例中，SiN 是中间介质层。[8]

第二个停止点在帽层开窗（cap breakthrough）过程中保护金属。宽开孔的刻蚀可能快于窄开孔，且刻蚀深度随晶圆位置而异。若非如此，先被刻穿的开孔下方的金属，会在其他开孔还需要继续刻蚀时就暴露出来。分级保护扩大了工艺窗口，减少了金属侵蚀、腐蚀与空洞形成。[8]

台积电的文献描述了 Cu 上方的 AlN/AlOₓ/SiOC/AlOₓ 叠层，其中 AlN 阻挡 Cu 扩散；还有一个省去一层 AlOₓ 膜的简化变体 AlN/SiOC/AlOₓ。[9] 开孔尺寸、深宽比、图形密度与帽层材料不同的金属层需要不同的刻蚀裕量。在多一个受保护终点值得为此增加工艺的前提下，双层 AlOₓ 停止层便有用武之地。

多出来的薄膜增加了成膜、选择性开窗与清洗步骤，还多出一批需要控制附着力、水汽与应力的界面。这些整面（blanket）薄膜通过已有的通孔图形开窗，因此每层膜并不需要额外增加一张光刻掩模。AlOₓ 取代更低 k 的介质时会引入寄生电容；不过两层薄 AlOₓ 膜的 AlOₓ 总量仍可能少于一层厚膜。总厚度、摆放位置以及中间介质层共同决定了电学代价。沉积化学还会改变 AlOₓ 的介电常数与残余羟基含量，后者可能氧化下方金属。[7], [8], [10], [11]

背面堆叠分为靠近器件、相对较细的 BM0–BM2 布线和更粗的 BM3–BM5 配电。间距增幅最大的一级出现在 BM2 与 BM3 之间。BM0 的间距与逻辑行高基本匹配，使局部供电恰好契合单元行。越往上层，越多的电流经由更大的导体汇聚：随着网络接近封装，布线密度的重要性便让位于低电阻与大电流容量。这套层级结构为供电网络提供了宽大的电源布线，又不挤占紧张的正面信号布线资源。[3]

![](https://substack-post-media.s3.amazonaws.com/public/images/b8aa7ad4-7dd0-4f61-ac5a-42fe2ffb6298_945x301.png)
*英特尔 18A BM0–BM5 实测最小间距。来源：SemiAnalysis*

***SemiAnalysis STEEL 拆解实验室剖析先进数据中心与 AI 硬件。欲了解我们的拆解管线或委托定制拆解，请联系 [sales@semianalysis.com](mailto:sales@semianalysis.com)。***

***我们在招人：架构、版图、封装、制造与实验室专家。机会覆盖从系统到晶体管及其间的每一个环节。欢迎查看我们的[招聘页面](https://semianalysis.com/semianalysis-careers/)。***

## 正面互连

英特尔 18A 把 Mo 内衬 W 接触孔与纳米硅通孔，同一套独立的背面 Cu 供电网络结合在一起。三星 SF2 则把供电留在正面，采用 Ti 基接触界面、Ta 基阻挡层，以及 Cu 布线周围的 Co 内衬。

在 18A 的标准单元行里，背面电源轨经由单元内部的纳米硅通孔向器件供电，释放了正面布线资源。三星的 M0 则要同时容纳电源与信号连接。

![](https://substack-post-media.s3.amazonaws.com/public/images/97e3382a-e1ee-4cbe-b924-8e1090cc570b_945x624.png)
*英特尔 18A M0–M14 实测最小间距。来源：SemiAnalysis*

从器件到 M0，连接依次经过 Ti 基 S/D 界面、W 接触孔填充、Mo 内衬 W 通孔和 Cu M0 导线。Mo 为 W 提供导电的成核与附着层，取代了传统 W 集成中电阻较大的 TiN 内衬。这增大了特征结构内的有效导电体积，同时保留了 W 填充及其成熟的抛光、清洗与刻蚀工艺。英特尔的 Mo/W 专利描述了这一集成取舍。纳米硅通孔在背面供电通路中采用了同样的 Mo 内衬 W 结构。[12]

![](https://substack-post-media.s3.amazonaws.com/public/images/f116d635-da7e-4106-8025-7b6aac641a3f_1188x313.png)
*英特尔 18A 与三星 SF2 的接触孔与通孔材料。来源：SemiAnalysis*

从 TiN 到 Mo 是一次渐进式改动。虽然全 Co 或全 Mo 填充同样能减少极小特征结构中耗损在内衬上的体积，但那需要全新的集成方案，复杂度与风险都更高。Cu 因电阻低，在较宽的导线上依然有吸引力。随着导线与通孔尺寸缩小，扩散阻挡层在其横截面中的占比越来越大。[12], [12], [14]

![](https://substack-post-media.s3.amazonaws.com/public/images/febf286e-3662-4147-812d-cc37e96d2731_6060x2251.png)
*英特尔 18A Panther Lake P 核逻辑（上）与三星 SF2 C1U 逻辑（下）的互连 EDS 元素面分布图。从左到右依次为 Cu、Ta、Co、Ru 与 Co/Nb 合成图。来源：SemiAnalysis*

英特尔在 M0–M1 使用 Co/Ru 内衬，M2–M4 使用 Co，M5–M9 使用 Nb。较低层级的内衬帮助 Cu 附着，并减少沟槽填充时的空洞形成。应用材料（Applied Materials）的 Endura 设备新增了热控制来配合润湿工艺，薄膜连续性足够好，合适的毛细压力足以把 Cu 原子驱动到通孔底部而不产生空洞。

英特尔选用 Nb 特别值得玩味。英特尔的 Nb 专利描述了一种导电扩散阻挡层，旨在相对传统 Ta 基阻挡层降低阻挡层对电阻的贡献，尤其是在全部电流都要穿过阻挡层的通孔底部。该专利把 Nb 用于较粗的金属层，并可选择成本更低的 PVD 工艺。[15], [16]

上层金属能够接受覆盖性与均匀性较差、但更厚的物理气相沉积（PVD）阻挡层；下层金属则需要通过保形原子层沉积（ALD）形成的更薄阻挡层。Co/Ru 多出一个材料界面，要求受控的沉积与 Cu 填充。按金属层级更换内衬与阻挡层，让英特尔得以在互连电阻、工艺复杂度与可靠性之间做优化。[15, 16]

![](https://substack-post-media.s3.amazonaws.com/public/images/f0faf32e-6f06-4087-8fc5-e5b8862893a9_1600x542.png)
*英特尔 18A 与三星 SF2 M0–M9 的内衬、填充与刻蚀停止层材料。来源：SemiAnalysis*

# RibbonFET

RibbonFET 是英特尔对其环栅晶体管（GAAFET）的命名，它以四片水平堆叠的硅纳米片取代 FinFET 的垂直鳍形，让栅极得以从四面环绕沟道。通往 GAAFET 的道路要从平面晶体管讲起。

![](https://substack-post-media.s3.amazonaws.com/public/images/714d286b-6d60-4d1a-8d35-8a31935de9a7_1151x410.png)
*平面 NMOS 结构（左）与 CMOS 反相器（右）。来源：SemiAnalysis*

平面 MOSFET 把栅极放在源极与漏极之间的沟道上方。把一个 NMOS 与一个 PMOS 晶体管配对，就得到 CMOS 反相器：输入为高时 NMOS 把输出拉低，输入为低时 PMOS 把输出拉高。栅极必须对沟道保持静电控制，才能保证干净的开关动作。随着栅长不断缩短，漏极开始与栅极争夺这一控制权，关态漏电随之增大。

随后的一次架构演进恢复了静电控制：把沟道抬升为垂直的鳍，让栅极包裹其三面。这一名为「FinFET」的新架构在更小的占位内装进了更多有效沟道宽度。但进一步微缩之后，要在更小的单元内同时维持驱动电流与漏电指标愈发困难，平面 MOSFET 遇到过的问题再度出现。纳米片 GAAFET 用一叠水平纳米片取代垂直鳍形，补上了第四面，每一片纳米片都被栅极环绕。更紧的静电控制抑制了更短栅长下的漏电，而堆叠又在单元占位内增加了有效沟道宽度。

![](https://substack-post-media.s3.amazonaws.com/public/images/5c40c53f-5c63-4e12-abc6-feeb8fdce130_1183x635.png)
*通过架构演进控制栅极漏电。来源：SemiAnalysis*

在 FinFET 工艺中，沟道宽度只能按台阶式变化，设计师必须增减整条鳍。纳米片宽度则可以在工艺设计规则内连续调节。更宽的片提高驱动电流，更窄的片降低电容但牺牲驱动电流。英特尔 18A 每叠使用四片纳米片，并在逻辑与 SRAM 之间采用不同的片宽。在工艺层面，每叠增加片数会提高有效沟道宽度与驱动电流，但也会使制造更复杂。

## RibbonFET 对比 MBCFET

三星于 2022 年以 SF3E 开始 GAAFET 量产，随后是 SF3，如今到了 SF2。其「MBCFET」为对比英特尔首代 RibbonFET 实现提供了很好的结构参照。[17] STEEL 正在深入剖析用于 Exynos 2600 的 SF2，以及用于苹果（Apple）A20 Pro 的台积电 GAAFET 节点 N2，相关内容将在后续文章中发布。我们也在 X 上陆续放料。下面就把三星 SF2 的 MBCFET 与英特尔 18A 的 RibbonFET 放在一起比较。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

即便外行也能一眼看出英特尔多出的那片纳米片：英特尔堆叠四条 ribbon，三星是三条。在这些视场里，三星的片要宽得多，所以片数与片宽共同决定了可用的沟道周长。片宽还会改变哪些硅表面承载电流。在常规 (001) 硅上，宽纳米片以宽大的顶面和底面为主，有利于电子输运；窄片中侧壁的贡献占比更大，有利于空穴输运。更薄的片改善栅控，但会加剧限制效应与散射。于是，片宽与片厚连同应力、阈值电压一起，成为 NMOS/PMOS 均衡的一部分。[18], [19]

像 18A 这样的 GAAFET 设计，NMOS 与 PMOS 使用不同的功函数金属（WFM）叠层。每条 ribbon 周围，一层薄 SiOx 界面层把硅沟道与 HfOx high-k 介质隔开，La 提供偶极调谐，WFM 包裹着介质。NMOS 采用 TiAl 基叠层，PMOS 采用 TiN WFM。W 填充剩余的栅极沟槽，在不再需要功函数层的位置提供一条低电阻率通路。在这个视场中，PMOS 叠层在 ribbon 之间为 W 留出了空间，而 NMOS 叠层占据了这些间隙中更多的部分。一种硅基介质标记出 P/N 边界，使共用同一栅极沟槽的 PMOS 与 NMOS 栅得以顺序加工。

快速逻辑路径、保持电路与 SRAM 需要一族阈值选项。在不大幅改变器件尺寸、电容或制造复杂度的前提下改变阈值，价值可观。FinFET 工艺通常依靠不同的功函数金属叠层实现。在四条 ribbon 的 GAA 叠层里，片与片之间的窄间隙限制了每条沟道周围能容纳多少 WFM。栅介质中的 La 在 SiOx/HfOx 界面形成界面偶极，移动有效功函数、调谐阈值电压。这给了英特尔在 NMOS/PMOS WFM 叠层之外的又一个控制手段。低阈值器件改善关键路径驱动，较高阈值降低其他地方的漏电。偶极调谐在 GAA 中尤其有用，因为它不必用更厚的 WFM 去挤占本就狭窄的片间间隙，就能改变阈值。

精确控制 La 的掺入、扩散与界面质量长期以来都是难题，曾限制其在大规模量产中的可行性，但如今每一家先进代工厂都在采用。英特尔的专利描述了在 HfOx 上方沉积一层可形成偶极的氧化物，并在完成功函数金属与填充金属之前，将其退火推向界面氧化层。这把阈值调谐与金属可用空间解耦。较新的研究则处理热预算问题：imec 2026 年的 dipole-middle（偶极居中）研究把偶极移位层插在两次 HfOx 沉积之间，在缩短扩散路径的同时，于图形化过程中保护 SiOx。[20], [21] 匹配截面 EDS：英特尔 18A（左）对比三星 SF2（右）。

![](https://substack-post-media.s3.amazonaws.com/public/images/f3325ca6-4a44-4e9a-ae33-69ba59f57406_2832x2486.png)
*上：片截面，英特尔 P 核逻辑与标记为 CU 的三星逻辑视场。下：栅截面，英特尔 P 核逻辑与三星 NPU 逻辑。截面方向已对齐匹配；单元功能与驱动目标不同。比例尺以各图为准。来源：SemiAnalysis*

英特尔在接触孔下方保留了抬升的源/漏外延，三星则把 W 深深凹入外延，形成 V 形 Ti 内衬界面。更深的接触增大了金属-半导体接触面积、缩短了下方各片流出的电流路径，降低了接触电阻与扩展电阻。但它也去掉了外延体积，并使接触孔刻蚀更靠近沟道端。保留更多外延则保住了可用于应力传递的材料，尤其是从 SiGe 传入 PMOS 的应力。两种几何形态在接触可达性、应力工程与刻蚀裕量之间各自取得平衡。[22], [23]

三星堆叠三片对英特尔的四条 ribbon，两种工艺都利用片宽调谐驱动强度。在我们的三星截面中，NPU 行的片宽大致在 19 到 30 nm 之间，CU 单元中为 37 到 50 nm。三星的纳米片呈渐缩形，最宽的片在最下方、最窄的在最上方。两种工艺都采用 HfOx 栅介质与 Ti 基功函数叠层，NMOS 叠层中含 Al。在此展示的三星器件中，介质与 WFM 占据了片间间隙，W 只留在最顶片上方。英特尔的 PMOS 叠层在 ribbon 之间留出更多空间，W 填满这些间隙；而更厚的 NMOS 叠层让 W 主要留在上部沟槽。栅叠层 EDS 元素面分布图。

![](https://substack-post-media.s3.amazonaws.com/public/images/7c00f05f-2aaf-43ea-8718-d2a616b3d5d0_6076x2424.png)
*上：英特尔 18A P 核逻辑。下：三星 SF2 CU 逻辑。来源：SemiAnalysis*

英特尔 PMOS ribbon 之间的 W，提供了一条贴近下方栅极的导电通路。当 WFM 填满整个间隙时，栅极仍然环绕沟道，但电压要经过电阻更大的功函数膜才能到达栅极。更薄的 WFM 与偶极调谐为低电阻率填充保留了空间；Mo 与 Ru 是为后续微缩正在开发的替代填充金属。[24]

一种带掩模的顺序式 WFM 流程，可以解释不同的栅极高度与纳米片间填充的差异。下面给出的推测序列展示了分开的 NMOS 与 PMOS 功函数步骤如何形成这种几何形态。

![](https://substack-post-media.s3.amazonaws.com/public/images/041768b6-ca30-4eba-8a2d-f9e786e10cba_1260x1165.png)
*推测的英特尔 18A NMOS 与 PMOS WFM 集成序列。来源：SemiAnalysis*

得益于 BSPDN 工艺，英特尔用介质取代了高密度逻辑区的硅 subfin（子鳍），消除了 ribbon 下方的寄生导电通路，降低了与衬底相关的电容。如经典非 SOI 的平面与 FinFET 设计那样保留硅体，就需要结工程与穿通截止（punchthrough-stop）工程来抑制漏电。介质隔离使该漏电对 subfin 掺杂剖面的敏感度下降，但增加了去除与填充步骤。它还削弱了穿过硅的直接导热路径，使接触孔、金属堆叠与封装在散热中的分量更重。[24], [26]

元素面分布图中，氟集中在英特尔部分选定的器件结构周围。WF6 是 W 成核与填充的标准前驱体，阻挡膜则保护相邻介质免受氟的攻击。低氟 W 工艺降低残余氟的负担。氯化物基前驱体可避免在 W 沉积中引入 F，但需要对氯的侵蚀、成核与填充质量加以控制。集成目标是一条连续、低电阻的 W 通路，配以薄薄一层保护性内衬，并把对周围叠层的化学损伤降到最低。[20], [27], [28]

![](https://substack-post-media.s3.amazonaws.com/public/images/e13daab3-c017-4c12-a531-a91839c58c3f_1435x2196.png)
*推测的 GAAFET 工艺流程。来源：SemiAnalysis*

***SemiAnalysis STEEL 拆解实验室剖析先进数据中心与 AI 硬件。欲了解我们的拆解管线或委托定制拆解，请联系 [sales@semianalysis.com](mailto:sales@semianalysis.com)。***

***我们在招人：架构、版图、封装、制造与实验室专家。机会覆盖从系统到晶体管及其间的每一个环节。欢迎查看我们的[招聘页面](https://semianalysis.com/semianalysis-careers/)。***

# 单元库分析

我们在下文所示的 XTEM 位置测量了单元高度、栅极间距、金属几何形状与 ribbon 尺寸。各表按取样位置与器件极性分组列出这些尺寸。我们的「片截面（sheet cut）」垂直穿过硅沟道，从端面方向看 ribbon；「栅截面（gate cut）」则沿沟道方向穿过连续的多个栅极。

![](https://substack-post-media.s3.amazonaws.com/public/images/4ca26391-75aa-4ca5-ba84-b3c047155b38_1666x1712.png)
*实测单元库尺寸。*Intel 18A PDK 给出的 M0 间距为 32 nm，但 Panther Lake 的 HP（高性能）单元库出货为 36 nm，**第三方披露。来源：SemiAnalysis*

18A 的逻辑单元尺寸指向一个五轨（track）逻辑库，而 N3E 与 Intel 3 的单元尺寸表明是七轨逻辑库。DDR-PHY 使用的 M0 导线比核心逻辑更宽、间距也大得多。这是用布线密度换取更低的导线电阻以及相邻网络间更弱的耦合。这样的几何形状适合模拟、时钟与 I/O 电路的电流输送和耦合要求。

PowerVia 把主电源轨移出信号布线轨道，让 18A 得以把紧凑的单元高度与更宽的 M0 几何形状结合起来。这在保持小单元占位的同时，放松了局部金属微缩的压力。单元高度与栅极间距决定几何密度；引脚可达性与可布线性则决定一个真实模块实际能用上其中多少。[29]

栅极间距测量最大的结论是：在 Bohr 代表单元模型下，英特尔 18A 计算逻辑与台积电 N3E GPU 逻辑密度相当。18A 样本比 Intel 3 GPU 样本密 18.6%。三个取样点的栅极间距几乎一致，因此差异主要来自单元高度。

Bohr 模型把一个跨三个栅极间距的四晶体管 NAND2 与一个跨十九个间距的 32 晶体管扫描触发器（SFF）组合起来，按 60:40 对两者的密度加权。敏感性一列显示，单元高度与栅极间距各自独立变化 ±1 nm 时结果如何改变。这里比较的是代表性单元的几何；整颗裸片的密度还取决于单元组合与布局。

![](https://substack-post-media.s3.amazonaws.com/public/images/b8012b4b-76c8-4ed5-b7c5-a0ffb9b953a3_1809x445.png)
*代表单元密度与输入敏感性。来源：SemiAnalysis*

18A P 核的 M0 金属横截面明显大于 N3E 向量引擎。把每个轮廓按梯形计算，每条线的面积为 2.63 倍，按布线间距归一化后为 1.84 倍。更大的截面降低了导线电阻中的几何分量，并在给定电流下降低了电流密度。更高更宽的导线也会增加电容，因此电路延迟取决于电阻与电容的平衡。DDR-PHY 的单位布线宽度金属面积小于 18A 核心视场，但仍高于 N3E。[30]

![](https://substack-post-media.s3.amazonaws.com/public/images/7e3fd4d0-e346-4acb-831f-238795842d53_1274x349.png)
*M0 截面几何。来源：SemiAnalysis*

面积 = 高度 ×（顶部 CD + 底部 CD）/ 2，含内衬层。面积/间距按布线宽度归一化。锥度（taper）为侧壁相对垂直方向的对称倾角，其中角度最大的是 DDR-PHY。

## 计算小芯片

![](https://substack-post-media.s3.amazonaws.com/public/images/0c91f14b-ede6-4f5a-ba74-17cbcdf9dd14_2895x2009.png)
*计算小芯片 XTEM 取样位置。来源：SemiAnalysis*

这些测量显示了 ribbon 尺寸与栅叠层几何如何在计算小芯片内部、以及 NMOS 与 PMOS 之间变化，从而在逻辑、SRAM 与 DDR-PHY 之间平衡沟道驱动、栅极负载以及介质/WFM 叠层所需的空间。片宽主要改变可用沟道周长；片厚还会改变静电控制与载流子限制；栅叠层厚度则决定了留给低电阻率填充的空间

![](https://substack-post-media.s3.amazonaws.com/public/images/52a1dad6-3279-42de-abb4-14c9de265f01_1710x606.png)
*Ribbon 尺寸。来源：SemiAnalysis*

### P 核与 LP E 核逻辑

P 核与 LP E 核都使用多种纳米片宽度。宽度在高倍 XTEM 图像上测量，而更大视场的图像展示了 LP E 核内更多的宽度选择。即便在一个 LP E 核内部，出现多种宽度也在意料之中。时序关键路径、缓冲器以及不同扇出的单元需要不同的驱动强度。低倍视场展示了表格量化位置之外的这种宽度多样性。

### L2 与 L3 SRAM

GAA 给 SRAM 设计师提供了另一种平衡上拉（PU）、传输门（PG）与下拉（PD）晶体管的方式。FinFET 位单元靠鳍数设定器件强度，GAA 则增加了纳米片宽度这一尺寸调节旋钮。在 6T SRAM 单元中，相对传输门更强的下拉限制读扰动，而相对上拉更强的传输门改善可写性。写入时，传输门与写驱动器把存储「1」的节点拉到反相器翻转点以下；读取时，下拉管把存储「0」的节点保持在低电平。偏置、阈值电压、失配与辅助电路决定其余的裕量。FinFET 大电流单元通常采用 1:2:2 的 PU:PG:PD 鳍数配比，这是器件尺寸比而非电流比。

![](https://substack-post-media.s3.amazonaws.com/public/images/290da0e9-8b7f-4f12-b480-2dfc9f6b3db6_1488x655.png)
*英特尔 18A SRAM 位单元特性。来源：Intel，ISSCC 2025（© IEEE）。[31]*

Ribbon 宽度让英特尔无需增加整条鳍就能平衡 SRAM 的强度。L2 单元把最窄的 ribbon 用于 PU、最宽的用于 PD，分别改善可写性与读稳定性。英特尔披露的 HCC（高电流单元）无需辅助电路即可工作；密度更高的 HDC（高密度单元）则采用负位线写辅助。把选中的位线短暂拉到地电位以下，可增大传输门过驱动，使其在更低的电源电压下也能压过上拉管。这换来了密度与低压可写性，代价则是升压电路、开关能量以及必须受控的额外电压应力。[31], [32]

四条矩形 ribbon 的周长 = 8 ×（宽 + 厚），未计圆角。PG/PU 为 1.49，PD/PG 为 1.16。

L3 结构在布局与单元高度上与 L2 非常接近。表中列出的 L3 纳米片宽度较少，是因为可用的高倍图像更少。

### DDR PHY

DDR-PHY 用密度换取可控的模拟行为与可靠的片外信号传输。它包含驱动器、接收器、延迟电路与校准逻辑，用于设定驱动强度、采样时序与电压裕量。宽度相近、四片一组的重复器件，正适合用规则的晶体管单元实现匹配与可编程驱动。它更宽的局部布线为电流输送与敏感信号隔离留出了空间，但比致密的核心逻辑网格更占面积。这样的布局在满足内存通道电气要求的同时，也兼顾了数字逻辑密度。[33]

![](https://substack-post-media.s3.amazonaws.com/public/images/88d6334e-d412-47d4-bfa8-65653b442347_2048x2048.png)
*DDR PHY。来源：SemiAnalysis*

***SemiAnalysis STEEL 拆解实验室剖析先进数据中心与 AI 硬件。欲了解我们的拆解管线或委托定制拆解，请联系 [sales@semianalysis.com](mailto:sales@semianalysis.com)。***

***我们在招人：架构、版图、封装、制造与实验室专家。机会覆盖从系统到晶体管及其间的每一个环节。欢迎查看我们的[招聘页面](https://semianalysis.com/semianalysis-careers/)。***

### Intel 3 GPU 器件

![](https://substack-post-media.s3.amazonaws.com/public/images/066f4605-8131-4de5-8f71-ab74b69a0568_2465x1290.png)
*Intel 3 GT1 GPU：取样位置与器件视场。来源：SemiAnalysis*

#### *向量引擎逻辑*

Intel 3 的 XVE 逻辑采用双鳍 PMOS 与 NMOS 器件，电源轨位于 M0。其单元高度与 M0 间距构成七轨几何，比 18A 逻辑多两个轨道。双鳍器件之间也出现了一鳍的组合。

#### *Intel 3 L2 SRAM*

Intel 3 L2 SRAM 采用熟悉的 HCC 尺寸配比：一条 PU 鳍、两条 PG 鳍、两条 PD 鳍。

![](https://substack-post-media.s3.amazonaws.com/public/images/6cfdec65-5e08-46de-a569-ec139002c164_2068x2068.png)
*Intel 3 L2 SRAM。来源：SemiAnalysis*

### N3E GPU 器件

![](https://substack-post-media.s3.amazonaws.com/public/images/dcc1dd16-e652-4654-812d-30661fad6a5c_2525x2231.png)
*N3E GT2 GPU 取样位置。来源：SemiAnalysis*

#### *向量引擎逻辑*

![](https://substack-post-media.s3.amazonaws.com/public/images/b36ce4c2-ce55-4f6d-ab60-5ab48bb15b30_2068x2068.png)
*N3E 向量引擎逻辑截面。来源：SemiAnalysis*

N3E 的 XVE 视场是重复的双鳍器件与七轨单元几何。N3E 仍是 FinFET 工艺，这让 Panther Lake 提供了一个 FinFET 与 RibbonFET 的直接对比。

#### *N3E L2 SRAM*

N3E L2 SRAM 采用同样的 1:2:2 PU:PG:PD 鳍数配比。

![](https://substack-post-media.s3.amazonaws.com/public/images/f24a24b3-f827-4b29-ac49-2f067db39f61_2068x2068.png)
*N3E 向量引擎逻辑截面。来源：SemiAnalysis*

# 版图分析

![](https://substack-post-media.s3.amazonaws.com/public/images/377bc2eb-a382-4a12-9fcb-fc2f2efed37a_5022x1948.png)
*英特尔 Lunar Lake（左）与 Panther Lake-U（右）版图。来源：SemiAnalysis*

Panther Lake-U 的版图与 Lunar Lake 相当接近。两者都是 4 个 P 核配 4 个 LP E 核，NPU、媒体与显示引擎的位置也相似。Lunar Lake 同样采用 Xe2——Panther Lake Xe3 GPU 的直系前代。这使 Lunar Lake 成为最直接的比较基准。Arrow Lake 核心数不同，且采用更老的 Xe-LPG GPU 架构，因此我们只在它能提供更直接的部件级对比时才用到它。

![](https://substack-post-media.s3.amazonaws.com/public/images/e85ce992-989f-48e9-a8f1-4a588c2ea798_1712x804.png)
*Lunar Lake、Panther Lake 8 核、Panther Lake 16 核/12-Xe 与 Arrow Lake-H 配置。来源：Intel*

## 计算小芯片

即便在发布数月之后，Panther Lake 计算小芯片的版图照片依然稀少。英特尔 18A 的背面金属与介质叠层必须在不损伤下方结构的前提下去除，才能拍到干净的晶体管级版图。大多数已公开的裸片图（die shot）都隐藏或重度处理了背景，而我们对自己拍出的这张裸片图相当自豪，很高兴在此展示我们的成果。

![](https://substack-post-media.s3.amazonaws.com/public/images/55cad0f3-f2e4-4f5a-b607-9311fececde7_2476x2082.png)
*Panther Lake-U 4+0+4 计算小芯片标注图。来源：SemiAnalysis*

我们测量了计算小芯片上关键部件的面积，并与它们在台积电 N3B 上的 Lunar Lake 前代对比。这有助于我们捕捉模块面积的变化，并跨制程节点与设计比较这两颗芯片。

我们的小芯片总面积不含划片道（scribe line）区域。下面的「计算+GPU」小计使用 PTL-U 计算小芯片与 GT1 GPU，不含 I/O 小芯片与无源基础小芯片。各模块面积以版图上标注的边界为准

![](https://substack-post-media.s3.amazonaws.com/public/images/5a78ff7a-30a1-4bb6-91bf-56f3859e9a87_1600x1589.png)
*Panther Lake 4+0+4 计算小芯片面积与 Lunar Lake 对比。来源：SemiAnalysis*

「计算+GPU」一行由所列 PTL-U 与 GT1 面积重新计算得出。各部件行采用其声明的分区数量，并不是对小芯片整体的加和拆分。

![](https://substack-post-media.s3.amazonaws.com/public/images/01032afd-9c69-4b3d-a103-26a24e01ae21_2386x1380.png)
*Lunar Lake Lion Cove（左）与 Panther Lake Cougar Cove（右）P 核。来源：SemiAnalysis*

从 Lunar Lake 到 Panther Lake，P 核面积几乎未变，尽管 L2 容量从 2.5 MiB 增加到了 3 MiB。Arrow Lake 使用与 Lunar Lake 相同的 Lion Cove 核心，但 L2 同样是 3 MiB。Cougar Cove 在相同的 P 核面积里装下了多 20% 的 L2。更大的私有缓存让每个核心更多的工作集保持在执行单元近旁，减少对共享 L3 与 DRAM 的访问。额外容量会增加存储漏电与查找能耗，因此设计师要在其与省下的低层级访问之间权衡。P 核共享的 L3 缓存也缩小了 14.8%。[2]

Cougar Cove 在相近的占位面积之上，叠加了英特尔宣称的能效改进。RibbonFET 更紧的沟道控制降低了漏电，PowerVia 则减小了供电跌落（droop），允许更紧的电压保护带（guardband）。[1]

![](https://substack-post-media.s3.amazonaws.com/public/images/30fe82f2-6be2-4de2-88bc-f57b6c47914d_2729x1466.png)
*Lunar Lake Skymont（左）与 Darkmont（右）LP E 核集群。来源：SemiAnalysis*

Darkmont 的四核 LP E 核集群比 Lunar Lake 上的 Skymont 小 5.0%，减量主要来自 L2 区域。1 MiB 区域缩小 8.4%，1.5 MiB 区域缩小 14.9%。标签阵列也少了一行可见行。标签用于标识数据阵列中存放的是哪些内存地址，因此重排它们改变的是缓存的布局与连线，而不必减少数据容量。[2]

LP E 核共享一个 L2。这汇聚了容量、避免了整套缓存机构的重复，但四个核要争用它的 bank 与带宽。它们独立的集群还把轻负载挡在性能集群及其 L3 之外，让那个更大的域得以休眠。[1], [2]

缓存面积不只是存储单元。标签标识每一行，译码器选择行，灵敏放大器读取位线上的微弱信号，导线把各个 bank 连接起来。把阵列拆成更小的分段可以缩短字线与位线、提高访问速度，但会复制外围电路。因此，Panther Lake 更小的缓存区域反映的是完整的存储器实现，包括每个区域中有多大比例用于存储。[34]

与 Meteor Lake 和 Arrow Lake 不同，Panther Lake 没有独立的 SoC 小芯片。NPU、LP E 核、内存控制器、PHY、媒体与显示引擎如今都集中在计算小芯片上。这去掉了一颗有源裸片（die），也让 CPU 的内存流量留在同一颗裸片上。代价是把 PHY 与 I/O 相关电路搬上了 18A：驱动器、接收器与模拟电路仍必须满足外部电压、负载与信号完整性要求，所以它们的面积不会像致密数字逻辑那样缩小。[1], [2]

缩得最厉害的是 NPU，面积减少了 36.9%。NPU 5 把总量不变的 INT8 MAC 收敛到数量减半的神经计算引擎中。三个 NCE 各自配备更大的 MAC 阵列，使完整的 NCE 外包络比一个 NPU 4 引擎大 22.6%。这次整合还把便签存储器（scratchpad）与 SHAVE DSP 的数量从 12 个减半到 6 个。MAC 阵列负责矩阵乘法与卷积，SHAVE 则执行不太适合放进阵列的向量与自定义运算。[1], [2], [35]

![](https://substack-post-media.s3.amazonaws.com/public/images/7bff1891-aabd-4e2d-9358-45793075a886_2382x1433.png)
*Lunar Lake NPU 4（左）与 Panther Lake NPU 5（右）。来源：SemiAnalysis*

配对版图标识了每个 NCE 外包络及其 scratchpad、MAC 与 SHAVE 区域。在下面的面积统计中，每个实测 MAC 多边形按每个 NCE 计一次。

![](https://substack-post-media.s3.amazonaws.com/public/images/ea1093cf-6bcd-44e8-aec5-a96f4f15de77_1664x393.png)
*来自实测版图区域的 NPU 面积节省。子区域已计入 NCE 小计。来源：SemiAnalysis*

便签存储器在 MAC 阵列近旁存放权重、激活值与中间结果，供反复使用而无需再从 DRAM 搬取。数量减半带来了实测中最大的一笔面积节省，但在 MAC 总数不变的情况下，本地存储变少了。放不进本地存储的层需要更小的计算分块，或更多的中间数据搬运。收益取决于让扩大后的阵列保持忙碌，同时管好更紧的存储预算。[36]

NPU 5 还新增了原生 FP8。以 FP16 一半的操作数宽度，存储与搬运需求随之下降，帮助负载塞进更小的本地存储预算。更低的精度与依赖格式的动态范围，使量化缩放与模型验证成为部署工作的一部分。硬件激活函数进一步减少了原本会占用可编程 DSP 的工作。[1], [2]

微软（Microsoft）要求 Copilot+ PC 的 NPU 至少提供 40 TOPS。Lunar Lake 与 Panther Lake 都满足这一门槛，但 Panther Lake 使用的硅面积明显更少。

## GPU 小芯片

Panther Lake 是英特尔首个搭载 Xe3——其最新 GPU 架构——的产品。它提供两种 GPU 小芯片：较小的 GT1 小芯片，在 Intel 3 上集成 4 个 Xe3 核心；以及较大的 GT2 小芯片，在台积电 N3E 上集成 12 个 Xe3 核心。

Panther Lake 让我们能把同一 GPU 架构在 Intel 3 与台积电 N3E 之间对比。Wildcat Lake 又添了 Intel 18A 上的第三个 Xe3 实现。后续文章将详述 Xe3 及其在全部三个制程节点上的实现差异。

![](https://substack-post-media.s3.amazonaws.com/public/images/00b74ae9-3a90-41c4-b954-42d368f939de_1906x981.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/8a70b129-6de6-4449-8e5a-cac7b7a99c10_1761x1475.png)
*英特尔 Panther Lake GT1（Intel 3，4 个 Xe 核心）与 GT2（台积电 N3E，12 个 Xe 核心）GPU 小芯片版图。来源：SemiAnalysis*

GT2 把 Xe3 扩展到另一种物理布局：渲染切片（render slice）改为纵向排布，而不是 GT1 的横向排布。切片的位置决定了到共享缓存 bank 与 D2D 接口的距离。这些导线消耗面积并增加延迟，因此扩展 Xe 核心数量也要求在缓存摆放、布线与时序之间重新找到平衡。[1]

一眼可见的是，台积电 N3E 上的 GT2 小芯片，其 Xe 核心比 GT1 小得多。这些模块面积包含逻辑、缓存与布线。

![](https://substack-post-media.s3.amazonaws.com/public/images/34458780-2d3f-4f4f-b8f1-f0992b0a1dc8_1600x489.png)
*Panther Lake GPU 小芯片面积与 Lunar Lake 对比。来源：SemiAnalysis*

GT1 小芯片上的一个 Xe 核心比 Lunar Lake 上的大约 ~69%，比 GT2 上的大约 ~55%。因此，Intel 3 每个 Xe 核心消耗的面积显著更多。模块面积的差距超过了实测的逻辑与 SRAM 密度差距，于是布线、时序目标、单元组合与版图分配都被纳入比较。

实测的向量/矩阵引擎区域在 Lunar Lake 与 Panther Lake GT2 小芯片之间几乎不变。Xe3 每个核心仍保留八个 512 位向量引擎与八个 2048 位 XMX 引擎。其收益同样来自更有效地喂养这些引擎：更多驻留线程隐藏了停顿，可变寄存器分配让着色器在每线程寄存器数量与保持活跃的线程数之间权衡。[1]

共享 L1/SLM 容量从 192 KiB 增加 33% 到 256 KiB，而面积只增加 5%，有效密度因此提高 27%。L1 留住被复用的缓存行，软件管理的 SLM（共享本地内存）则让线程组在本地共享数据。两者都减少了去往更远端内存的流量。但每组分配更多 SLM 也会限制一个核心上同时驻留的组数。[1], [37]

GT1 小芯片配备 4 MiB L2，GT2 为 16 MiB。GT1 把 L2 缓存分成四个 1 MiB bank，GT2 则用八个 2 MiB bank。每个 bank 含 128 个宏（macro），但每个 N3E 宏存储 16 KiB，是 Intel 3 宏 8 KiB 容量的两倍。N3E 宏只大 54% 却装下了双倍的位元，密度高出 30%：约 23.7 Mbit/mm² 对 18.3 Mbit/mm²。计入 bank 级电路后，差距进一步拉大：GT2 约 16.9 Mbit/mm²，GT1 约 10.4 Mbit/mm²。

![](https://substack-post-media.s3.amazonaws.com/public/images/c856024b-1cd3-4088-9ac2-b8b0ef954918_1600x329.png)
*Panther Lake Intel 3（GT1）与台积电 N3E（GT2）面积对比。来源：SemiAnalysis*

GT2 的密度收益，来自其宏在单位面积上存储更多位元，且这些宏在每个缓存 bank 中的占比更高。更大的宏把译码器与灵敏放大器的开销分摊到更多存储上，更紧凑的 bank 布局又降低了控制与布线的占比。折中则是更长的字线与位线，带来更多电容。[34]

## I/O 小芯片

Panther Lake 使用两种 I/O 小芯片，均在台积电 N6 上制造。较小的一种提供 4 条 PCIe 5.0 与 8 条 PCIe 4.0 通道，服务于较低档位的系统以及不带独立 GPU 的机型；较大的一种再加 8 条 PCIe 5.0 通道、合计 20 条，用于独显连接。搭载较大 10 或 12 Xe GPU 的 Panther Lake SKU 使用较小的 I/O 小芯片。[38]

![](https://substack-post-media.s3.amazonaws.com/public/images/ea5fd8fb-d7d4-4a0d-bc3b-61a71e59325a_1909x615.png)
*Panther Lake 12 通道 I/O 小芯片版图。来源：SemiAnalysis*

较小的 I/O 小芯片在 Lunar Lake 的 I/O 布局之上增加了一个 PCIe 4.0 模块和一个 Thunderbolt 模块，多提供 4 条 PCIe 4.0 通道和另一个 Thunderbolt 4 端口。其中重复使用的 N6 模块面积与布局几乎原样保留。复用这些久经考验的 PHY 与控制器，避免了把外部接口移植到 18A 并重新认证——对这些受片外链路约束的电路而言，更快的数字逻辑收益有限。[38]

![](https://substack-post-media.s3.amazonaws.com/public/images/e504db0a-5851-45f8-8c27-8cc96a0ac5fe_1600x655.png)
*Panther Lake 12 通道 I/O 小芯片面积与 Lunar Lake 对比。来源：SemiAnalysis*

***SemiAnalysis 的拆解实验室（STEEL）深入剖析*** **全球最先进的数据中心与 AI 硬件。欲了解更多** ***关于*** **我们的拆解管线或委托定制拆解，请联系 [sales@semianalysis.com](mailto:sales@semianalysis.com)。***

***我们正在招聘从系统到晶体管及其间每一个环节的技术专家。欢迎查看我们的[招聘页面](https://semianalysis.com/semianalysis-careers/)。***

# Foveros-S

Panther Lake 通过解耦式封装提供可扩展性与模块化：把计算、GPU 与 I/O 硅片拆分为独立小芯片，从而支持一整套小芯片组合。这种划分让封装成为英特尔节点经济学的一部分——它决定了每款产品消耗多少先进制程晶圆面积、哪些功能可以留在其他工艺上，以及英特尔能从一组共享小芯片中提供多大的配置自由度。

此外，分开制造计算与 GPU 小芯片，把全新的 18A 工艺限定在计算小芯片内，让图形与 I/O 得以使用其他更成熟、更具成本效益的工艺。在 Panther Lake 上，GPU 与 I/O 小芯片与计算小芯片一起，通过 Foveros-S 组装在一块无源硅基底上。

英特尔当前的技术简介给 Foveros-S 列出的标称间距为 36 µm。基底中的硅通孔（TSV）把上方的细线径布线连接到下方更大的封装连接。各功能小芯片以 2.5D 形式并排坐落在这块无源基底上。[39]

![](https://substack-post-media.s3.amazonaws.com/public/images/2a11c35f-101e-404d-815d-f75ba672170b_1216x503.png)
*Foveros-S 封装示意图：有源小芯片通过微凸点连接到无源硅基底。来源：SemiAnalysis*

我们穿过计算与 GPU 小芯片的截面，展示了封装的布线层级。微凸点把每颗有源小芯片连接到无源硅基底；基底上精细的重布线层（RDL）承载短而密的小芯片间连线。TSV 把连接穿过基底送到封装基板，再由基板扇出到粗得多的主板焊点。基底只提供互连，计算仍留在其上方的有源小芯片中。[39]

在计算小芯片边缘，高倍插图显示局部微凸点间距约 25.24 µm，特征宽度为 12.33 µm。

![](https://substack-post-media.s3.amazonaws.com/public/images/10a5b31b-6002-4da0-81f7-9903e64f7648_4892x1572.png)
*Panther Lake 封装穿过计算与图形小芯片的截面。来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/2135ac47-dab7-4b8b-9ed3-a74786ec0c5e_2852x2102.png)
*Panther Lake 俯视图，标出截面取样位置。来源：SemiAnalysis*

这些局部间距比英特尔的 Foveros-S 标称值更密。X-ray 视场进一步证实相邻凸点更紧密，且这一现象在每颗小芯片上的每个芯片间（D2D）区域均一致。更多 X-ray 分析在付费墙后提供。

![](https://substack-post-media.s3.amazonaws.com/public/images/7b3cb654-3821-4b60-8d79-1b1810a6af47_688x362.png)
*标注了局部相邻间距的 GPU D2D 区域。来源：SemiAnalysis*

把内存控制器放在 CPU 旁边，免去了 Meteor Lake 与 Arrow Lake 中 CPU 内存请求必须经过的 D2D 传输。这避免了额外的发送器、接收器与链路穿越，节省了接口能耗与延迟。Panther Lake 独立的 GPU 仍要跨过一条 D2D 链路才能到达 DRAM，因此其更大的本地缓存也有助于控制封装内的流量。[1], [40]

更小的裸片含有随机致命缺陷的概率更低，而组装前先行筛选，可以避免一颗坏小芯片糟蹋一整包好硅。复用还把设计与认证工作分摊到更多产品上。与这些收益相对，英特尔要为无源基底、D2D 电路、额外的键合与测试步骤以及组装损耗买单。以「每个能正常工作的产品的成本」计，才能完整捕捉晶圆良率、复用、测试与组装的综合效果。[29]

## Wildcat Lake 封装

2026 年 4 月 16 日，英特尔发布了面向入门级移动与边缘系统的 Core Series 3（原 Wildcat Lake）。Wildcat Lake 保留 18A，但去掉了无源基底，把更多功能合并到一颗裸片上以简化封装。这两款产品因此揭示了同一种先进制程的两种不同商业化路径。[41]

![](https://substack-post-media.s3.amazonaws.com/public/images/b8585318-1938-4fab-b4eb-a7176d587e1f_1664x384.png)
*Panther Lake 与 Wildcat Lake 封装对比。来源：SemiAnalysis*

Wildcat Lake 的 18A 裸片整合了最多两个 Cougar Cove P 核、四个 Darkmont LP E 核、两个 Xe3 核心与一个更小的 NPU。一颗独立的平台控制器裸片提供 I/O，通过 UCIe 连接——这是英特尔首次在处理器产品中实现该标准。把图形合并进来，去掉了一道小芯片边界与无源基底，为这款带宽要求不高的入门级产品降低了组装复杂度。但它也把 CPU 与图形的扩展绑在了同一颗裸片上，放弃了 Panther Lake 换用大得多 GPU 的灵活性。[42], [43]

![](https://substack-post-media.s3.amazonaws.com/public/images/fb5655a5-b55b-46d4-898c-f192d0abed89_5569x5697.jpeg)
*Wildcat Lake 裸片图。来源：SemiAnalysis*

# 英特尔的制造复苏

2021 年 7 月，英特尔 CEO Pat Gelsinger 提出了一份雄心勃勃的工艺路线图，目标是在 2025 年前重夺工艺性能领先，后来被概括为「四年五个节点」。五年过去、换过一位 CEO 之后，英特尔的翻身故事并不像 Pat 当初期望的那样毫不含糊地乐观。[44], [45]

英特尔曾为工艺技术定调，比业内其他玩家早数年把 high-k 金属栅技术与 FinFET 带入量产。其 22 nm FinFET 工艺随 2012 年的 Ivy Bridge 到达消费者手中。[46] 英特尔的 IDM（垂直整合制造）模式让架构师与工艺工程师得以对产品和工艺进行协同优化。从 Sandy Bridge 开始，英特尔统治了 x86，而 AMD 还在 Bulldozer 中挣扎。

这份领先在 14 nm 上步履蹒跚，在 10 nm 上彻底断裂。英特尔原本定下高达 2.7 倍的密度提升目标，但该节点迟到数年，又经历多次修订，才撑得起英特尔的完整产品线。这次延误迫使英特尔把 14 nm 拉长到六代产品，与此同时，台积电在工艺技术上完成了超越，AMD 也在 x86 上恢复了元气。

到 2019 年，英特尔大部分产品线仍在出货 14 nm，10 nm 的客户端爬坡集中在 Ice Lake 移动处理器上。彼时，台积电已在出货 N7 与 N7+，AMD 的 Zen 2 计算小芯片（chiplet）也用 N7 提高了核心数并改善了能效。

工艺失利是英特尔衰落的核心，但不明智的商业决策进一步加速了下滑。产品延误与产品失误叠加，把客户端、服务器与 FPGA 路线图全部拖期。数次进军 AI（Nervana 与 Gaudi）和网络（Tofino）的尝试，也未能建立起长久的事业。

英特尔的复苏集中在消费级 CPU 与先进封装上。Tiger Lake、Alder Lake、Lunar Lake 以及如今的 Panther Lake 重建了英特尔的消费级路线图。工艺方面，Intel 4 随 Meteor Lake 出货，Intel 3 随 Granite Rapids 与 Sierra Forest 出货，Intel 18A 随 Panther Lake 出货。英特尔还把先进封装纳入了其代工业务。然而，英特尔在服务器上仍在追赶。数代 Xeon 迟到数年，在性能、能效与核心数上落后于同时期的 AMD 与 Arm 服务器 CPU。工艺路线图是回来了，但英特尔已不再拥有 10 nm 之前那种工艺技术领先地位。

环栅纳米片与背面供电的引入，是十年来晶体管集成领域最大的两项变革。英特尔一次扛下了两项：18A 在 Panther Lake 上把首代 RibbonFET 与 PowerVia 组合在了一起。

Panther Lake 是一个分量十足的制造里程碑。我们的截面展示了 RibbonFET 与 PowerVia 如何重塑局部接触与布线，版图分析则展示了架构整合与工艺选择在哪里省下了面积。能否维持持续的竞争领先，取决于产品性能、成本、良率，以及下一次落地。

***SemiAnalysis STEEL 拆解实验室剖析先进数据中心与 AI 硬件。欲了解我们的拆解管线或委托定制拆解，请联系 [sales@semianalysis.com](mailto:sales@semianalysis.com)。***

***我们在招人：架构、版图、封装、制造与实验室专家。机会覆盖从系统到晶体管及其间的每一个环节。欢迎查看我们的[招聘页面](https://semianalysis.com/semianalysis-careers/)。***

# 参考文献

[1] Intel, “Intel Tech Tour 2025 Panther Lake recap,” Doc. 866361, 2025. Accessed: Sep. 14, 2026. [Online]. Available: <https://cdrdv2-public.intel.com/866361/ITT_2025_Panther_Lake_Recap1.pdf>

[2] Intel, “Core Ultra processors Series 3 datasheet, volume 1,” Doc. 872188-001, Jan. 2026. Accessed: Sep. 14, 2026. [Online]. Available: <https://cdrdv2-public.intel.com/872188/872188-001.pdf>

[3] N. Horiguchi and E. Beyne, “Backside power delivery: How to power chips from the backside,” *imec Reading Room*, Nov. 25, 2022. Accessed: Sep. 14, 2026. [Online]. Available: <https://www.imec-int.com/en/articles/how-power-chips-backside>

[4] W. Hafez *et al.*, “Intel PowerVia technology: Backside power delivery for high density and high-performance computing,” in *Proc. IEEE Symp. VLSI Technol. Circuits*, Kyoto, Japan, Jun. 2023, pp. 1–2, doi: [10.23919/vlsitechnologyandcir57934.2023.10185208](https://doi.org/10.23919/vlsitechnologyandcir57934.2023.10185208).

[5] K. Fischer *et al.*, “Intel 18A platform technology featuring RibbonFET (GAA) and PowerVia for advanced high-performance computing,” in *Proc. Symp. VLSI Technol. Circuits*, Kyoto, Japan, Jun. 2025, pp. 1–3, doi: [10.23919/vlsitechnologyandcir65189.2025.11075006](https://doi.org/10.23919/vlsitechnologyandcir65189.2025.11075006).

[6] K.-F. Cheng, C.-L. Teng, H.-Y. Huang, and H.-C. Chen, “Metal oxide composite as etch stop layer,” U.S. Patent 12 176 247 B2, Dec. 24, 2024. Accessed: Sep. 14, 2026. [Online]. Available: <https://patents.google.com/patent/US12176247B2/en>

[7] S. W. King, “Dielectric barrier, etch stop, and metal capping materials for state of the art and beyond metal interconnects,” *ECS J. Solid State Sci. Technol.*, vol. 4, no. 1, pp. N3029–N3047, 2015, doi: [10.1149/2.0051501jss](https://doi.org/10.1149/2.0051501jss).

[8] A. V. Mule’, D. J. Towner, D. Seghete, C. R. Ryder, and A. A. Gonzalez, “Multi-layer etch stop layers for advanced integrated circuit structure fabrication,” U.S. Patent Appl. 20220102343 A1, Mar. 31, 2022. Accessed: Sep. 14, 2026. [Online]. Available: <https://patents.google.com/patent/US20220102343A1/en>

[9] C.-C. Wang and J. H. Wang, “Interconnect structure with dielectric cap layer and etch stop layer stack,” U.S. Patent Appl. 20230253247 A1, Aug. 10, 2023. Accessed: Sep. 14, 2026. [Online]. Available: <https://patents.google.com/patent/US20230253247A1/en>

[10] Y. J. Wu, K.-F. Cheng, C.-C. Lee, H.-K. Chang, and H.-Y. Huang, “Etch stop layer for interconnect structures,” U.S. Patent Appl. 20240332070 A1, Oct. 3, 2024. Accessed: Sep. 14, 2026. [Online]. Available: <https://patents.google.com/patent/US20240332070A1/en>

[11] M. G. Rainville, N. Shankar, K. S. Reddy, and D. M. Hausmann, “Deposition of aluminum oxide etch stop layers,” U.S. Patent Appl. 20180197770 A1, Jul. 12, 2018. Accessed: Sep. 14, 2026. [Online]. Available: <https://patents.justia.com/patent/20180197770>

[12] J. S. Leib *et al.*, “Conductive lines having molybdenum liner and tungsten fill for advanced integrated circuit structure fabrication,” U.S. Patent Appl. 20240429126 A1, Dec. 26, 2024. Accessed: Sep. 14, 2026. [Online]. Available: <https://patents.justia.com/patent/20240429126>

[13] M. Naik, “Cobalt enables power and performance scaling at single-digit logic nodes,” *Applied Materials*, Dec. 17, 2018. Accessed: Sep. 14, 2026. [Online]. Available: <https://www.appliedmaterials.com/us/en/blog/blog-posts/cobalt-enables-power-and-performance-scaling-at-single-digit-logic-nodes.html>

[14] Lam Research, “Breaking through AI’s invisible barrier with molybdenum,” *Lam Research Newsroom*, May 6, 2025. Accessed: Sep. 14, 2026. [Online]. Available: <https://newsroom.lamresearch.com/molybdenum-metallization-ai-revolution>

[15] P. Yashar, G. Malyavanatham, and H. Vijwani, “Integrated circuit interconnect structures with niobium barrier materials,” U.S. Patent Appl. 20240112951 A1, Apr. 4, 2024. Accessed: Sep. 14, 2026. [Online]. Available: <https://patents.google.com/patent/US20240112951A1/en>

[16] Applied Materials, “Applied Materials unveils chip wiring innovations for more energy-efficient computing,” *Applied Materials Investor Relations*, Jul. 8, 2024. Accessed: Sep. 14, 2026. [Online]. Available: <https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-unveils-chip-wiring-innovations-more-energy>

[17] Samsung, “Samsung showcases AI-era vision and latest foundry technologies at SFF 2024,” *Samsung Semiconductor*, Jun. 13, 2024. Accessed: Sep. 14, 2026. [Online]. Available: <https://semiconductor.samsung.com/news-events/news/samsung-showcases-ai-era-vision-and-latest-foundry-technologies-at-sff-2024/>

[18] C. W. Yeung *et al.*, “Channel geometry impact and narrow sheet effect of stacked nanosheet,” in *Proc. IEEE Int. Electron Devices Meeting (IEDM)*, Dec. 2018, pp. 28.6.1–28.6.4, doi: [10.1109/iedm.2018.8614608](https://doi.org/10.1109/iedm.2018.8614608).

[19] S. Mochizuki *et al.*, “Evaluation of (110) versus (001) channel orientation for improved nFET/pFET device performance trade-off in gate-all-around nanosheet technology,” in *Proc. Int. Electron Devices Meeting (IEDM)*, Dec. 2023, pp. 1–4, doi: [10.1109/iedm45741.2023.10413854](https://doi.org/10.1109/iedm45741.2023.10413854).

[20] D. G. Ouellette *et al.*, “Fabrication of gate-all-around integrated circuit structures having molybdenum nitride metal gates and gate dielectrics with a dipole layer,” U.S. Patent 12 051 698 B2, Jul. 30, 2024. Accessed: Sep. 14, 2026. [Online]. Available: <https://patents.google.com/patent/US12051698B2/en>

[21] imec, “Advancing the CFET-based device roadmap with novel integration modules and standard-cell architectures,” *imec*, 2026. Accessed: Sep. 14, 2026. [Online]. Available: <https://www.imec-int.com/en/articles/advancing-cfet-based-device-roadmap-novel-integration-modules-and-standard-cell>

[22] A. Reznicek, X. Miao, C. Lee, and J. Zhang, “Wrap around contact for nanosheet source drain epitaxy,” U.S. Patent 11 302 813 B2, Apr. 12, 2022. Accessed: Sep. 14, 2026. [Online]. Available: <https://patents.google.com/patent/US11302813B2/en>

[23] J. A. Kittl, J. G. Hong, D. R. Palle, and M. S. Rodder, “Methods for varied strain on nano-scale field effect transistor devices,” U.S. Patent 9 978 833 B2, May 22, 2018. Accessed: Sep. 14, 2026. [Online]. Available: <https://patents.google.com/patent/US9978833B2/en>

[24] S. Gandikota *et al.*, “Method of reducing metal gate resistance for next generation NMOS device application,” Int. Patent Appl. WO 2024/137272 A1, Jun. 27, 2024. Accessed: Sep. 14, 2026. [Online]. Available: <https://patents.google.com/patent/WO2024137272A1/en>

[25] J. Zhang *et al.*, “Full bottom dielectric isolation to enable stacked nanosheet transistor for low power and high performance applications,” in *Proc. IEEE Int. Electron Devices Meeting (IEDM)*, Dec. 2019, pp. 11.6.1–11.6.4, doi: [10.1109/iedm19573.2019.8993490](https://doi.org/10.1109/iedm19573.2019.8993490).

[26] C. Yoo, J. Chang, Y. Seon, H. Kim, and J. Jeon, “Analysis of self-heating effects in multi-nanosheet FET considering bottom isolation and package options,” *IEEE Trans. Electron Devices*, vol. 69, no. 3, pp. 1524–1531, Mar. 2022, doi: [10.1109/ted.2022.3141327](https://doi.org/10.1109/ted.2022.3141327).

[27] S. S. Pradhan, D. B. Bergstrom, J.-S. Chun, and J. Chiu, “Tungsten gates for non-planar transistors,” European Patent Appl. EP 3 506 367 A1, Jul. 3, 2019. Accessed: Sep. 14, 2026. [Online]. Available: <https://patents.google.com/patent/EP3506367A1/en>

[28] L. Schloss and X. Ba, “Tungsten films having low fluorine content,” U.S. Patent 9 754 824 B2, Sep. 5, 2017. Accessed: Sep. 14, 2026. [Online]. Available: <https://patents.google.com/patent/US9754824B2/en>

[29] Intel Foundry, “Accelerating AI and HPC with advanced process and packaging technologies,” Doc. 367370-001US, Jun. 2026. Accessed: Sep. 14, 2026. [Online]. Available: <https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-11/intel-foundry-hpc-ai-brief.pdf>

[30] M. Lofrano, X. Chang, H. Oprins, and Z. Tokei, “Mitigating the thermal bottleneck in advanced interconnects,” *imec*, Sep. 28, 2023. Accessed: Sep. 14, 2026. [Online]. Available: <https://www.imec-int.com/en/articles/mitigating-thermal-bottleneck-advanced-interconnects>

[31] S. Bair, “Intel at ISSCC 2025: Navid Shahriari invited talk, eight papers, forums, panelist & product details,” *Intel Community*, Feb. 19, 2025. Accessed: Sep. 14, 2026. [Online]. Available: <https://community.intel.com/t5/Blogs/Tech-Innovation/Edge-5G/Intel-at-ISSCC-2025-Navid-Shahriari-Invited-Talk-Eight-Papers/post/1667592>

[32] D. Chandra, E. Potladhurthi, D. R. S. Reddy, and K. S. Rengarajan, “Tunable negative bitline write assist and boost attenuation circuit,” U.S. Patent Appl. 20160203857 A1, Jul. 14, 2016. Accessed: Sep. 14, 2026. [Online]. Available: <https://patents.google.com/patent/US20160203857A1/en>

[33] Synopsys, “Advantages of firmware-based training in high-speed DDR IP,” *Synopsys IP Technical Bulletin*. Accessed: Sep. 14, 2026. [Online]. Available: <https://www.synopsys.com/articles/firmware-based-training-ddr-ip.html>

[34] N. Muralimanohar, R. Balasubramonian, and N. P. Jouppi, “CACTI 6.0: A tool to understand large caches,” Hewlett-Packard Laboratories, 2009. Accessed: Sep. 14, 2026. [Online]. Available: <https://users.cs.utah.edu/~rajeev/cacti6/cacti6-tr.pdf>

[35] Intel, “Intel Tech Tour 2024 Lunar Lake AI hardware accelerators,” Doc. 824436, 2024. Accessed: Sep. 14, 2026. [Online]. Available: <https://cdrdv2-public.intel.com/824436/2024_Intel_Tech%20Tour%20TW_Lunar%20Lake%20AI%20Hardware%20Accelerators.pdf>

[36] Y.-H. Chen, J. Emer, and V. Sze, “Eyeriss: A spatial architecture for energy-efficient dataflow for convolutional neural networks,” in *Proc. 43rd ACM/IEEE Annu. Int. Symp. Comput. Archit. (ISCA)*, Jun. 2016, pp. 367–379, doi: [10.1109/isca.2016.40](https://doi.org/10.1109/isca.2016.40).

[37] Intel, “Introduction to the Xe-HPG architecture,” Doc. 758306, Nov. 4, 2022. Accessed: Sep. 14, 2026. [Online]. Available: <https://www.intel.com/content/www/us/en/developer/articles/technical/introduction-to-the-xe-hpg-architecture.html>

[38] Intel, “Core Ultra processors Series 3 for the edge,” Doc. 855291. Accessed: Sep. 14, 2026. [Online]. Available: <https://cdrdv2-public.intel.com/855291/Intel%C2%AE%20Core%E2%84%A2%20Ultra%20Processors%20Series%203%20for%20Edge%20Overview_2.pdf>

[39] Intel Foundry, “Foveros technology brief,” Doc. 366411-001US, Feb. 2026. Accessed: Sep. 14, 2026. [Online]. Available: <https://www.intel.com/content/dam/www/central-libraries/us/en/documents/2025-07/foveros-25d-product-brief.pdf>

[40] D. Das Sharma, “UCIe: Building an open chiplet ecosystem,” UCIe Consortium, 2022. Accessed: Sep. 14, 2026. [Online]. Available: <https://www.uciexpress.org/_files/ugd/0c1418_c5970a68ab214ffc97fab16d11581449.pdf>

[41] Intel, “Intel launches Intel Core Series 3 processors,” *Intel Newsroom*, Apr. 16, 2026. Accessed: Sep. 14, 2026. [Online]. Available: <https://www.intel.com/content/www/us/en/newsroom/news/client-computing/intel-launches-intel-core-series-3-processors-changing-the-game-for-everyday-computing.html>

[42] Intel, “Core Series 3 launch press deck,” Apr. 2026. Accessed: Sep. 14, 2026. [Online]. Available: <https://download.intel.com/newsroom/2026/Intel-Core-Series-3/Intel-Core-Series-3-Launch-Press-Deck.pdf>

[43] Intel, “Intel outlines architectures for agentic AI at Hot Chips 2026,” *Intel Newsroom*, Aug. 24, 2026. Accessed: Sep. 14, 2026. [Online]. Available: <https://www.intel.com/content/www/us/en/newsroom/news/client-computing/intel-outlines-architectures-for-agentic-ai-at-hot-chips-2026.html>

[44] Intel, “Intel accelerates process and packaging innovations,” *Intel Investor Relations*, Jul. 26, 2021. Accessed: Sep. 14, 2026. [Online]. Available: <https://www.intc.com/filings-reports/all-sec-filings/content/0001193125-21-224438/d199788dex991.htm>

[45] Intel, “Intel reports third-quarter 2021 financial results,” *Intel Investor Relations*, Oct. 21, 2021. Accessed: Sep. 14, 2026. [Online]. Available: <https://www.intc.com/news-events/press-releases/detail/1505/intel-reports-third-quarter-2021-financial-results>

[46] Intel, “3rd generation Intel Core processors bring exciting new experiences and fun to the PC,” *Intel Investor Relations*, Apr. 23, 2012. Accessed: Sep. 14, 2026. [Online]. Available: <https://www.intc.com/news-events/press-releases/detail/577/3rd-generation-intel-core-processors-bring-exciting>

# 延伸：承载片与键合叠层细节
