---
title: "中国长鑫存储（CXMT）即将挑战 DRAM 在位巨头"
title_en: "China's CXMT Is Set to Challenge DRAM Incumbents"
subtitle: "CXMT IPO、SK Hynix／Micron／Samsung 竞争、制程节点差距、中国 HBM、晶圆扩产、存储 LTA"
date: 2026-06-23
source: https://newsletter.semianalysis.com/p/chinas-cxmt-is-set-to-challenge-dram
crawled: 2026-09-15
authors: ["Ray Wang", "Myron Xie", "Dylan Patel", "Junsung Kim", "Sravan Kundojjala", "Louis Lu"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 中国长鑫存储（CXMT）即将挑战 DRAM 在位巨头

> 原文：[China's CXMT Is Set to Challenge DRAM Incumbents](https://newsletter.semianalysis.com/p/chinas-cxmt-is-set-to-challenge-dram) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**CXMT IPO、SK Hynix／Micron／Samsung 竞争、制程节点差距、中国 HBM、晶圆扩产、存储 LTA**

早在 2024 年底，我们就在本通讯中率先描述了 AI 在推理与智能体流程中永不餍足的用量所带来的存储短缺。此后我们已发布多篇存储深度文章，并对 CXMT 及中国算力做过详细报道。随着 CXMT 将在未来几个月内 IPO，我们认为有必要专门为它写一篇深度解析。该公司很可能成为中国规模最大的半导体 IPO，并标志着这家中国存储龙头迈出重要里程碑——而从现在起，它也注定与 Samsung、SK hynix、Micron 等领先存储供应商展开更激烈的竞争。

**我们的最新存储研究请见此处：**

**或阅读以下较早但同样精彩的存储及中国算力文章：**

1. [华为昇腾产能爬坡：裸片库存银行、台积电继续生产、HBM 是瓶颈](https://newsletter.semianalysis.com/p/huawei-ascend-production-ramp)
2. [华为 AI CloudMatrix 384——中国对 Nvidia GB200 NVL72 的回应](https://newsletter.semianalysis.com/p/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72)
3. [攀登内存墙：HBM 的崛起与路线图](https://newsletter.semianalysis.com/p/scaling-the-memory-wall-the-rise-and-roadmap-of-hbm)
4. [内存墙：DRAM 的过去、现在与未来](https://newsletter.semianalysis.com/p/the-memory-wall)
5. [Scaling Law——O1 Pro 架构、推理训练基础设施、Orion 与 Claude 3.5 Opus 的「失败」、测试时计算的推理 token 经济学](https://newsletter.semianalysis.com/p/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures)

CXMT 成立于 2016 年，即将登陆中国科创板。如今它已是中国的 DRAM 龙头，其历史展现出一条有趣的路径——技术转移、人才流动与国有风险资本的耐心——三者共同推动这家公司走向自主创新。

## **硅谷归来者**

CXMT 创始人[朱一明](https://baike.baidu.com/item/%E6%9C%B1%E4%B8%80%E6%98%8E/8904184)1994 年在清华大学获得物理学学士学位，随后前往纽约州立大学石溪分校（SUNY Stony Brook）攻读电气工程研究生。之后他在硅谷工作，并于 2001 年前后成为 MoSys（Monolithic System Technology）的项目负责人。2005 年，他带着一批 SRAM 专利和 10 万美元种子资金回到中国，创办了[兆易创新](https://www.21jingji.com/article/20260104/herald/67bbeabf0dd3a5bf0d973b49cd337caf.html)（GigaDevice）——这家无厂设计公司后来以 SPI NOR 闪存和微控制器闻名，成长为全球顶级 NOR 闪存供应商之一。但与 DRAM 或 NAND 闪存相比，全球 NOR 闪存市场要小得多。朱一明志向远大，他选择进军 DRAM 业务并不令人意外。

然而，DRAM 不是可以维持无厂模式的设计公司游戏。DRAM 吞噬资本、专利壁垒森严、且与制造深度绑定。到 2016 年，整个行业已被三家幸存者——Samsung、SK hynix 和 Micron——所主导，四十年积累的专利与资本构筑的壁垒从未被新进入者攻破。朱一明的 SRAM 专利和兆易创新的 NOR 业务，既给不了他 DRAM 存储单元，也给不了 DRAM 工艺，更无法提供对在位者专利的任何庇护。因此，当朱一明与合肥市政府于 2016 年启动这项 DRAM 创业——即后来成为 CXMT 的「506」项目——时，核心技术必须完全来自别处。

而它来自德国一家已死的公司。

## **DRAM 基石：继承奇梦达（Qimonda）**

这家已死的公司是[奇梦达（Qimonda）](https://zhuanlan.zhihu.com/p/83979732)。尽管该公司因 2008 年全球金融危机及随后剧烈的存储下行周期于 2009 年 1 月破产，它当时仍是欧洲领先的 DRAM 厂商。作为源自西门子的英飞凌（Infineon）的子公司，它提供了一个罕见的替代选项：深厚的 DRAM 专利库和一套存储单元架构，且二者都源自 Samsung-SK hynix-Micron 主导三角之外。2015 年 6 月，加拿大专利变现公司 WiLAN 旗下的 Polaris Innovations 以约 3,000 万欧元从英飞凌手中买下约 [7,000 项奇梦达专利及申请](https://www.eet-china.com/mp/a10024.html)。2019 年 12 月，[Polaris 与 CXMT 签署协议](https://www.prnewswire.com/news-releases/wilan-subsidiary-and-cxmt-enter-into-license-and-acquisition-agreements-300969655.html)：一大批 DRAM 专利的许可。CXMT 管理层曾公开声称获得了约 [2.8 TB 的奇梦达技术文档](https://xueqiu.com/7814068463/126783102)，这成为 CXMT DRAM 业务的基础。

CXMT 从奇梦达继承、继而自行发展的一项主要技术，是其 46nm 级 BWL（埋入式字线，buried wordline）存储单元，[CXMT 将其微缩到了 10nm 级](https://tech.ifeng.com/c/7q6EcdusERC)。BWL 是承重的核心思想。BWL 不再把存取晶体管的栅极布在晶圆表面，而是将其沉入位线下方的沟槽中。它把栅极从表面移走，使单元面积收缩到 6F2 布局（相比 8F2）。它还能在不消耗表面积的情况下加长沟道，抑制破坏数据保持特性的短沟道漏电。同时它降低了栅极与位线之间的寄生电容。埋入式字线加堆叠电容，正是当今三家 DRAM 巨头共同采用的架构。那家坚守沟槽路线的厂商死了，手中握着的正是堆叠电容/BWL 这条逃生通道——而这恰恰就是 CXMT 接手的东西。

**人才流动：从冻结的图纸到鲜活的研究开发**

除了专利，CXMT 从奇梦达崩溃中提取到的更耐用的东西是工程师。奇梦达西安研发中心拥有 400-500 名工程师，是奇梦达在德国以外建立的最大研发中心之一。奇梦达破产后，尽管西安研发中心整体被紫光集团收购，但个体人才的更广泛扩散让 CXMT 受益。此外，CXMT 还成功地把资深工程师 Karl-Heinz Kuesters 从奇梦达的德国基地吸引到了中国合肥。Kuesters 在 Siemens、Infineon 和 Qimonda 度过了 24 年的技术与预研副总裁生涯。Kuesters 主持的预研方向正是堆叠电容工作——也就是 CXMT 今天赖以构建的架构。他以技术顾问身份加入 CXMT，EE Times 因此称 Kuesters 为该公司的「底牌」（ace in the hole）。Kuesters 带来的是奇梦达遗产中专利和 2.8 TB 文档都无法承载的部分：隐性知识（tacit know-how）。拥有二十年 DRAM 开发领导经验的 Kuesters，能告诉 CXMT 的工程师奇梦达的哪些设计选择该保留、哪些该抛弃，以及如何把一个只在实验室里跑通的存储单元推向量产——那些整合与良率的判断力，任何专利里都不会记载。

美国方面呈现同样的模式。CXMT 负责未来技术评估的副总裁、也是公司路线图对外的代言人（「46nm 到 10nm 级」的说法即出自他）的 Ping Er-xuan，并非来自奇梦达，而是来自 Micron、SanDisk 和 Applied Materials 的美国职业生涯，在那里他执掌存储与材料技术。Ping 带来了工艺与材料的深度，以及一种新兴存储视角：单载流子迁移率（individual mobility）。

CXMT 还从韩国和台湾大量招人。韩国检方曾起诉向 CXMT 泄露技术的前 Samsung 员工，据报道有数十名韩国工程师曾在 CXMT 工作。台湾同样如此：CXMT 以有吸引力的薪酬包，持续挖角设备与工艺开发领域的顶尖工程师。

这才是与 CXMT 前行方向真正相关的部分。奇梦达专利从来都是一项有限的、会到期的资产。让 CXMT 得以不断前进——从 G4 到 G5、再到如今的 HBM——的不是那些文档，而是聚合起来的本土人才能力：曾在外国公司工作后归国的中国籍人才，以及部分来自外国公司的专家。继承只是起点。人才把一份外国遗产变成了自家的研发重器。然而，CXMT 花了将近十年才开始盈利。问题是：是谁在耐心地为 CXMT 的发展提供资金、并承受它近十年的亏损？

## **国有风险资本的耐心**

很难不把 CXMT 的成功至少部分归功于中国地方政府和中央政府的大力支持。合肥市政府就是最好的例子之一。合肥是中国的科技创新枢纽之一，以其[有耐心的国有风险资本](https://www.stcn.com/article/detail/3915165.html)闻名——过去二十年间，从京东方（BOE，全球领先的显示面板制造商）到蔚来（NIO，领先的电动车制造商），再到如今的 CXMT，培育出了一批成功企业。具体而言，合肥市政府为 CXMT 做了两件事。第一，合肥政府帮助 CXMT 在其晶圆厂周围建立起本地供应链。合肥的打法是入股一家「链主」企业的大量股权，然后把产业链其余环节吸引到它周围。该市在显示面板领域对 BOE、在电动车领域对蔚来就是这么做的，而从 2016 年起，它把同样的剧本复制到 CXMT 身上。围绕 CXMT 位于合肥临空工业园的工厂，政府打造了一个密集的本地集群。Peyton 和 Xinfeng 两家封测厂就坐落在距 CXMT 晶圆厂一街或一墙之隔的地方，其中 Xinfeng 超过 99% 的营收来自 CXMT。由 Guanggang 运营的现场大宗气体工厂供应 CXMT 的大部分需求，而至纯科技（Zhichun Technology，至纯科技）子公司 Zhiwei Semiconductors 的晶圆再生产能则位于合肥新站高新区。国有风险资本平台还直接控股了上游芯片塑封设备制造商 Wenyi Technology。这样一个本地供应链集群，为 CXMT 提供了本地化的产业基础。

此外，合肥的国有风险资本赔得起，而且能赔很久。私人风投基金要对 LP 负责，LP 期望按固定时间表获得回报；而合肥国资——其最终背后是市属及开发区国有主体——没有这样的时钟。它们持续为一家公司注资，而这家公司即便在 2025 年实现首次年度盈利之后，仍背负着近十年累积下来的约 [366.5 亿元人民币（RMB 36.65 billion）](https://www.stcn.com/article/detail/3915165.html)累计亏损。2016 年启动的最初「506」项目，起步阶段由合肥国资出资约[项目一期的 80%](https://finance.ifeng.com/c/8tmeeduFRlF)（180 亿元中的 144 亿元）。在历轮融资中，合肥各国资平台虽被稀释，但从未减持、从未退出。到 IPO 时，最大股东为[合肥的 Qinghui Jidian](https://static.sse.com.cn/stock/disclosure/announcement/c/202605/002170_20260517_MGLN.pdf)，持股 21.67%，[各国有风险资本平台合计持股超过 30%](https://news.10jqka.com.cn/20260608/c677286196.shtml)。这种把晶圆厂当作十年长赌、而非基金周期回报的意愿，正是技术与人才都赖以依存的催化剂。

## **从继承走向自主**

把这三条线索放在一起，CXMT 的第一个十年便归结为一条完整的弧线。奇梦达提供了地基——获得许可的专利库和一套来自在位者三角之外的存储单元架构。人才提供了动力——Kuesters 与 Ping 等关键人物，来自美国大厂的归国者，以及从韩国挖来的争议性雇员。这些人把一份冻结的图纸变成了能够持续微缩的工艺。然后，合肥政府提供了前两者需要却无法自行生成的东西：资本、耐心和本地化的供应链。三者任何单独一项都造不出一家 DRAM 厂商；三者合力做到了。

在接下来的章节中，我们将讨论 CXMT 的财务、技术与设备生态。

## **十年之后的下一步：超级周期中的 IPO**

CXMT 过去十年的历史虽然亮眼，但可能只是公司更长篇故事的早期章节。该公司目前正筹备的 IPO，将成为中国过去几十年规模最大的半导体 IPO 之一，也可能是今年全球最受关注的半导体上市。2024 到 2025 年间，市场长期盛传该公司准备上市；2025 年 12 月，随着上海证券交易所受理其科创板上市申请，CXMT 正式进入 IPO 申报阶段。更近一步，CXMT 于 5 月 27 日提交了中国证监会（CSRC）的注册申请，目前正处于最终审核之中，距离里程碑式的上市越来越近。

尽管理解 CXMT、YMTC 这类具有战略重要性且未上市的中国公司从来不易，但 CXMT 走向公开上市对我们大有帮助——其 IPO 招股书就公司的历史表现、未来轨迹、财务状况、市场定位与技术路线图披露了有价值的信息。将这些披露与我们的 **[Memory 模型](https://semianalysis.com/memory-model/)** 相结合，我们得以对 CXMT 的当前位置形成更准确的判断，并对其未来表现做出更稳健的预测。

从宏观层面看，以几乎所有指标衡量，CXMT 都显然已是全球第四大 DRAM 厂商，并且还在扩大对传统存储供应商的领先优势。全年来看，CXMT 营收同比增长 156% 至约 86 亿美元，高于 2024 年的约 33 亿美元和 2023 年的约 12 亿美元。净利润也首次转正，达到 10 亿美元，凸显该公司快速的规模扩张和不断改善的盈利能力。即便取得如此亮眼的成绩，CXMT 的 2025 自然年（CY25）营收仍明显落后于 Samsung（约 $72.3B）、SK hynix（约 $52.1B）和 Micron（约 $37.2B）的 DRAM 营收。

![](https://substack-post-media.s3.amazonaws.com/public/images/17bfbf22-acaf-43c3-886c-0841d99ea6e1_1862x1264.png)
*来源：SemiAnalysis Memory 模型 - sales@semanalysis.com*

2026 年一季度（1Q26），CXMT 报告营收 73 亿美元，同比增长约 700%，已接近公司 2025 年全年的营收。营业利润率也急剧扩张，达到约 70%。

但我们认为这仅仅是个开始。我们估计，至少在未来两年，该公司的表现会更好，甚至可以说是爆发式增长。仅根据其申报文件，公司 1H26 营收预计为去年同期的 7 倍，超过 160 亿美元。我们相信，2026 全年 CXMT 的营收可能突破 500 亿美元。若能实现，这意味着公司自 2023 年以来每年营收都翻了一倍以上，且 2026 年营收同比增长超过 6 倍，随着规模与盈利能力同步改善，其盈利轨迹还将显著加速。

在我们看来，CXMT 盈利如此可观的上行空间，显然更多由周期本身驱动，而非公司的技术或市场定位。只要细看 CXMT 的 ASP 轨迹与位元出货量之间的关联便会一目了然。1Q26 公司位元出货量仅增长 11%，而 ASP 上涨约 57%，此前 3Q25 和 4Q25 的 ASP 环比涨幅分别高达 63% 和 68%。换言之，真正推高公司盈利的是爆发式的 ASP 增长，而不是在全球 DRAM 终端市场上相对同业的大幅份额提升。按位元出货量计，我们建模显示 CXMT 的市场份额将从 2025 年的 9% 提升至 2027 年的 12%。3 个百分点的份额增益听起来微不足道，但对于一个我们测算 2027 年规模接近 $1T 的市场而言，意义非凡。

![](https://substack-post-media.s3.amazonaws.com/public/images/f78a6e80-e92e-4094-9328-f492f02abda4_3018x562.png)
*来源：SemiAnalysis Memory 模型 - sales@semianalysis.com*

足够令人意外的是，CXMT 迎来的强劲价格上扬并非特例。过去一年左右，我们在 DDR5、DDR4 乃至 DDR3 市场上，观察到先进制程与传统制程存储供应商都出现了类似的动态。正如我们在 2 月存储文章（文中我们将存储市场描述为进入「四十年一遇的短缺」）中所[指出](https://newsletter.semianalysis.com/p/memory-mania-how-a-once-in-four-decades)的，我们认为受这些产品类别持续的供需失衡驱动，DRAM 价格今年仍有望再度翻倍。自 2 月以来，我们对这一观点变得更有信心，并认为到年底其力度甚至可能超出我们的预期。

对于尚未密切关注 CXMT 或存储市场的读者来说，更有意思的或许是该公司的定价与行业龙头相比如何。根据我们的 Memory 模型，CXMT 的 DRAM ASP 挑战了一个常见误解——即中国存储在结构上更便宜、将以低价冲击市场、从而压制全球价格。虽然过去在某些情况下或许如此，但我们认为在本轮周期中这种说法并不准确，公司最新数据也支持同样的结论。

以 1Q26 为例，CXMT 的 DRAM ASP 在同一季度仅略低于 Samsung、SK hynix 和 Micron——差距约 5-10%。随着我们将其推演至 2026 年全年，我们认为方向上仍将如此，尽管差距会逐渐拉大。我们相信，未来几个季度差距的扩大，与其说源于固有的定价差异，不如说更多源于产品组合的变化。领先供应商的位元出货中服务器 DRAM 占比更高，且服务器 DRAM 相对消费 DRAM 的价格前景也更为有利，使它们持续受益。

因此，我们预计随着服务器在 DRAM 终端市场需求中的占比上升，这一组合比例未来几个季度还将进一步提高。到 2027 年底，我们预计服务器 DRAM 与 HBM 将合计占 DRAM 终端市场远超 50% 的份额。鉴于服务器 DRAM 和 HBM 的 $/GB 高于其他存储终端市场，随着服务器 DRAM 占比提升，这应能令领先存储供应商扩大相对 CXMT 的 ASP 差距——尤其是考虑到 2027 年 HBM 预期中的大幅涨价（我们的 [Accelerator & HBM 模型](https://semianalysis.com/accelerator-hbm-model/)与 [Memory 模型](https://semianalysis.com/memory-model/)中包含 2027 年 HBM 定价）。我们还掌握超大规模云厂商和 Nvidia 等主要存储买家 LTA 的细节。

![](https://substack-post-media.s3.amazonaws.com/public/images/840177b4-baad-4845-b4fe-d11e32963e33_1279x847.png)
*来源：SemiAnalysis Memory 模型 - sales@semianalysis.com*

强劲的 ASP 顺风显著改善了公司的利润率状况。CXMT 的 2025 财年（FY25）毛利率达到 37.8%，逼近 Samsung 的 39.4% 和 Micron 的 39.8%。但仍远低于 SK hynix 的 60.4%——SK hynix 受益于高得多的 HBM 组合占比，而 HBM 在去年带来了更高的 ASP 和利润率。CXMT 约 38% 的毛利率相较 FY23 的 -113% 和 FY24 的 -4.7% 是一次巨大的扭转。去年不仅是 CXMT 毛利率创历史新高之年，也是公司首次实现利润率转正之年。

![](https://substack-post-media.s3.amazonaws.com/public/images/1d9a20ac-f95d-494c-8db3-a72e65a36edd_3579x2195.png)
*来源：SemiAnalysis Memory 模型、公司报告 - sales@semianalysis.com*

随着 2026 年 DRAM ASP 持续上涨，CXMT 的利润率状况进一步改善。1Q26 其营业利润率达到 70%，同期 SK hynix 为 73%、Samsung 为 81%、Micron 为 84%。除强劲的 ASP 增长外，公司利润率的改善还得益于其几乎完全押注大宗 DRAM（commodity DRAM）——在当下，这类产品的利润率实际上已高于 HBM。根据其申报文件，公司位元销量几乎全部为传统 LPDDR 和 DDR 产品。HBM 对公司营收和利润的贡献仍然微乎其微。

![](https://substack-post-media.s3.amazonaws.com/public/images/29d2f013-7cf7-40a0-913a-7a6536d43523_3579x2195.png)
*来源：SemiAnalysis Memory 模型、公司报告 - sales@semianalysis.com*

当我们对四家存储供应商的 DDR5 产品做一个简单的每比特成本（cost-per-bit）分析时，这一点变得更加清晰。就 DDR5 而言，我们发现 CXMT 的每比特成本仍明显高于三家领先供应商——高出 30% 以上。然而，由于 1Q26 DDR5 定价已异常强劲，我们认为这仍将 CXMT 的毛利率推升到了 70% 以上。这表明 CXMT 利润率状况的改善主要是由定价驱动，而非产品竞争力或成本结构的实质性改善。

![](https://substack-post-media.s3.amazonaws.com/public/images/29a5424f-3557-44d3-b79c-05d617daeebf_1372x211.png)
*来源：SemiAnalysis Memory 模型 - sales@semianalysis.com*

除了刷出创纪录的盈利，我们认为公司也正在产能维度上攻城略地。到 2026 年底，我们预计 CXMT 将达到约 **350 kwspm**，仅略低于我们估计 Micron 的 **~385 kwspm**。若仅按晶圆产能排名，这将使 CXMT 接近成为业内第三大存储供应商。

![](https://substack-post-media.s3.amazonaws.com/public/images/3a6eff6b-99dd-4046-a19e-0955186169a4_2472x1022.png)
*来源：SemiAnalysis Memory 模型 - sales@semianalysis.com*

不过，CXMT 与两大 DRAM 龙头 Samsung 和 SK hynix 仍有明显差距——我们估计二者分别约为 **720 kwspm** 和 **595 kwspm**。明年，随着上海一期初步爬坡以及合肥、北京全面爬坡，CXMT 产能若按年末计可达 **420kwspm 区间**，占全球 DRAM 产能的 **约 17%**，高于 2025 年的 **约 13%**。按位元出货量计，CXMT 在全球位元出货中的份额预计将在 **2027 年从 9% 升至 12%**。

随着合肥基地全面达产以及上海基地两期项目在 2028 年前持续爬坡，CXMT 的全球产能份额还可能进一步上升。我们相信到 2028 年底，公司将拥有 500kwspm 的晶圆产能，约占全球 DRAM 供应的 17%，高于 2025 年的 11%。

![](https://substack-post-media.s3.amazonaws.com/public/images/f678b3c8-9498-4b55-bf67-68e2e3465182_1306x1008.png)
*来源：CXMT 合肥基地，SemiAnalysis Memory 模型 - sales@semianalysis.com*

鉴于 CXMT 在全球 DRAM 产能中日益扩大的角色，一如以往周期，投资者担忧中国玩家可能带来的供需冲击。这些担忧可以理解，但我们认为至少在未来两年内被夸大了。我们已经把 CXMT 及其他存储供应商的新增晶圆产能与位元出货纳入考量——并假设稼动率处于 95% 以上的高位区间——我们仍认为 DRAM 供应极度紧张。我们在存储模型中不断更新晶圆新增产能、需求与定价假设，更新速度远快于 TrendForce 或卖方银行。

![](https://substack-post-media.s3.amazonaws.com/public/images/4e7341ef-e3c9-4fa0-a8c7-66ce087b659d_2326x692.png)
*来源：SemiAnalysis Memory 模型 - sales@semianalysis.com*

单看 CXMT 的晶圆新增产能，与其他供应商相比，我们确实看到有分量的产能扩张。我们预计 CXMT 2026 至 2028 年每年分别新增约 85kwspm、70kwspm 和 80kwspm，相比之下 Samsung 为 15k/50k/110k，SK hynix 为 60k/60k/90k，Micron 为 30k/90k/115k。即便有这些晶圆新增，我们仍预计今年 DRAM 供应缺口在高个位数百分比，明年位元供应缺口将扩大至低两位数（low- to mid-teens）区间。我们在上一篇文章中已详细论述，为什么即使计入这些即将落地的新增晶圆产能，DRAM 供应紧张也可能持续到 2028 年。

我们认为，该公司几乎不可能以非理性的方式将产能扩张提速到当前节奏之上、从而实质性冲击这个正在提供极其有利定价环境的市场——因为晶圆厂的建设周期实在太长。这样的价格环境一直是公司盈利爆发式增长的主要驱动力，公司自然希望它延续。基于我们跟踪的晶圆厂建设进展，我们也尚未看到这种可能性的迹象，尽管我们想强调，上海基地在全面达产状态下的总晶圆产能可能超过 400kwspm。

具体到其晶圆产能，我们看到分配给 HBM 的晶圆相当有限。通过与其迄今为止的 IPO 相关申报文件相互印证，我们发现即便到今天，分配给 HBM 的晶圆也一直非常有限。到 2025 年底，我们认为 CXMT 约 265 kwspm 的产能中只有约 5 kwspm 分配给了 HBM。我们预计这一数字到 2026 年底和 2027 年底将分别增至近 30 kwspm 和约 55kwspm。这样的产能轨迹与 CXMT 的申报文件更相吻合——如前所述，2025 年公司约 99% 的营收来自 DDR 和 LPDDR 产品。

![](https://substack-post-media.s3.amazonaws.com/public/images/e1e3e7a4-6bfa-44ea-8684-9343fdde4e37_1592x1202.png)
*来源：SemiAnalysis Memory 模型 - sales@semianalysis.com*

不过，这一晶圆分配格局可能改变。我们认为，中国推动 AI 算力自给自足的更大布局，可能与公司的战略优先级发生冲突；而且鉴于前文讨论的 HBM 供应约束以及政府解决这一问题的决心，我们认为这一推动力度会随时间加强。

为此，在我们的估算中，我们纳入了政府的影响因素，即 CXMT 将随时间推移把更多晶圆产能分配给 HBM。因此，我们预计在 HBM 技术进步、且中国本土算力市场持续增长的支撑下，CXMT 的 HBM 晶圆产能将在 2027 和 2028 年显著加速。我们估计 CXMT 的 HBM 晶圆产能将在 **2027 年和 2028 年分别达到 55kwspm 和 100kwspm**。这将使该公司在全球 HBM 晶圆供应中的份额从 **2025 年的 1%** 升至 **2028 年的 12%**。

必须记住，与其他存储供应商不同，CXMT 对中国而言不仅是一家在经济与技术上都举足轻重的公司，更是一项国家可用于推进优先政策目标的战略资产。

不过从战略上讲，CXMT 近期把更多 DRAM 晶圆产能分配给大宗 DRAM 而非 HBM 是合理的。当前大宗 DRAM 的利润率显著高于 CXMT 的 HBM 产品，而且在同等条件下每片晶圆产出的位元数是后者的 3 倍以上。

鉴于 CXMT 的 HBM 技术尚未完全成熟，将大量晶圆产能分配给 HBM 很可能只产生有限的利润，同时却消耗了本可以更大规模支撑高利润率大宗 DRAM 的稀缺晶圆产能。在此背景下，优先大宗 DRAM 既符合经济理性，也更契合 CXMT 当前的制造能力与价格环境。不过中国必须把产能分配给 HBM，因为除了一些允许韩国厂商继续向中国出货的漏洞之外，HBM 对华销售仍相当受限。

在技术就绪度方面，我们认为 CXMT 仍在努力稳定 **HBM3 8 层（8-hi）** 的供应，**12 层（12-hi）** 面临的挑战更大。在前道（front end）环节，公司似乎已在稳定其 **第四代（G4）**、即 **1z 等效** DRAM 的生产上取得进展。我们相信今年 CXMT 的 DRAM 产出大部分将采用公司的 G4 制程节点制造。然而，HBM 所用核心 DRAM 裸片的前道晶圆测试（wafer-sort）良率仍应明显偏低，因为相对大宗 DRAM，其裸片面积更大、对单元性能和整体性能的要求更高。我们认为前道晶圆测试良率仍是公司的一大挑战，其与同业在这方面的差距依然很大。虽然我们相信 CXMT G4 节点的良率已有改善，但鉴于我们在 2024 和 2025 全年看到的较低利润率，我们怀疑其良率仍低于 1z 节点 85-90% 成熟良率的行业标准。这可能表明，设备限制与制造诀窍仍是 CXMT 需要克服的长期障碍。

![](https://substack-post-media.s3.amazonaws.com/public/images/551c5925-f110-4a9e-8bb4-f12b96e7c131_3006x804.png)
*来源：SemiAnalysis Memory 模型 - sales@semianalysis.com*

至于公司的下一代制程节点 G5、即 1a 等效 DRAM 节点，虽然理论上可以像 Micron 的 1a 节点那样在没有 EUV 的情况下继续推进，但它将面临越来越多的制造与设计挑战。当该节点应用于 HBM 的 DRAM 裸片时，这些挑战只会带来更大的制造与设计压力。更低的良率和更具挑战性的爬坡日程也可能影响公司的位元产出——尽管公司可以通过增加晶圆投片来弥补良率损失。

在此基础上，我们认为裸片堆叠仍是 CXMT HBM 的最大障碍。HBM 堆叠通常带来显著的技术难关，包括热应力、裸片开裂、翘曲、键合缺陷，以及跨多层堆叠裸片的良率损失。据我们了解，鉴于公司在 12 层及以上 HBM 方面的 know-how 和制造经验尚不充足，随着其尝试从 HBM3 8 层迈向 HBM3 12 层、并最终到 HBM3E，这些问题只会更加严重。

裸片堆叠并非 CXMT 独有的挑战。即便是领先的存储供应商也困难重重。我们了解到，对于 12 层 HBM4，供应商们仍在面临严重的堆叠相关问题，包括裸片开裂、热管理挑战和良率损失。

当存储供应商谋求生产 16 层乃至 20 层 HBM 时，这些挑战会更加突出。对于下一代的 HBM4E，我们注意到 Rubin Ultra 预计采用 12 层 HBM4E 而非 16 层，原因之一便是供应：16 层 HBM 需要更高的 DRAM 晶圆消耗强度，且制造工艺更难，可能导致更大的晶圆损耗和更低的 DRAM 位元有效供应。在 DRAM 供应高度紧张的环境下，这些条件让存储供应商和客户都陷入非常艰难的境地。

我们认为，CXMT 跳过 HBM3、转而聚焦 HBM3E 8 层和 12 层的可能性正在上升。我们相信这一潜在的路线图转变由两个因素驱动：1) 客户在 2027 年（'27）前后对更具竞争力 HBM 产品的需求；2) 主流加速器将配备 HBM3E、HBM4 和 HBM4E。

![](https://substack-post-media.s3.amazonaws.com/public/images/6fe5ef6c-f50b-4c1c-b0ba-3a2cbde34ae9_3052x406.png)
*来源：SemiAnalysis Memory 模型 - sales@semianalysis.com*

在后道（back end）环节，尽管 CXMT 采用的是 MR-MUF 还是 TC-NCF 仍存争议，我们认为封装挑战相对更可控，因为公司及其后道合作伙伴面临的出口管制约束较少。CXMT 已与通富微电（Tongfu Microelectronics）等领先 OSAT 合作一段时间，我们相信其后道能力应已逐步改善，不过相对领先存储制造商可能仍有差距。

考虑到这些既存的制造挑战，我们将 CXMT HBM3 8 层的前道与后道良率分别建模为约 35% 和 70%，意味着总良率仅约 25%。我们认为，鉴于裸片堆叠与键合难度更高，公司尝试生产 HBM3 12 层或 HBM3E 12 层时，这一数字还会更低。在这样的良率水平下，同等 DRAM 晶圆产能下 CXMT 的 HBM 产出将比领先存储供应商更加有限。更重要的是，由此产出的 HBM 可能利润率极低，尤其是在当前价格环境下与大宗 DRAM 相比。

CXMT 在 HBM 上的挣扎，持续体现在其在中国 AI 加速器市场有限的产品存在感和缓慢的渗透率上。我们认为只有华为、寒武纪（Cambricon）以及部分新兴中国 AI 芯片创业公司可能采用 CXMT 的 HBM，不过我们猜测采用幅度会很大。事实上，我们相信国内 AI 加速器厂商如果能通过任何可用渠道获得供应、或动用 2024 年 12 月出口管制之前囤积的库存，它们仍会更青睐外国 HBM3 乃至 HBM3E。随着中国本土 CSP 资本开支和更大范围的算力建设激增，国内 HBM 需求无疑也在快速增长，并将继续上升。

话虽如此，华为与 CXMT 将拥有不基于迟缓的 JEDEC 标准与物理层（phy）的定制 HBM，因此能够弥合带宽劣势。

我们认为，中国面临的 HBM 供应约束，可能比仅由本土 HBM 发展缓慢所隐含的程度更为严重。三大 HBM 供应商全面紧张的供应状况可能进一步加剧这一约束——根据美国 2024 年 12 月宣布的出口管制，这三家已被禁止向中国销售 HBM2E 同等或更先进的 HBM 产品。在供应紧张的环境下，这些供应商冒违反出口管制风险对华销售的意愿只会更低。

然而，HBM 的转口贸易与走私可能使这一结论复杂化。我们了解到，一些中国公司仍在从存储供应商处获得 HBM3——这一动态我们去年曾报道过，此后也得到了其他主流媒体的印证。我们相信如今依然如此。

根据我们与业内参与者的交流，通过位于第三国的海外办公室或合作公司进行转口，仍是中国公司获取 HBM 的路径之一。此外，第三国的一些下游 OSAT 或中间商似乎在为这些货流提供便利。一些实体可能以不被视作完整制造 GPU 或 ASIC 的形式发运部分组装的系统或模块，因而仍被允许运入中国，随后其中的 HBM 可被回收并重新封装到中国本土的 GPU 或 ASIC 上。

## IPO 结构揭示了什么

CXMT 有望成为中国最大的半导体 IPO 之一，而其股权结构比头条财务数字更重要。CXMT 报告的 2025 财年合并净利润为 71.4 亿元人民币，但归属母公司股东的仅 18.7 亿元，74% 归属少数股东权益。原因在于股权架构。CXMT 持有 Changxin Xinqiao 30.68% 的经济权益、Changxin Jidian Beijing 31.72% 的经济权益，却通过长期一致行动安排控制两者 73.01% 和 75.32% 的表决权。这使公司得以合并报表其大部分并不拥有的晶圆厂，因此合并口径数字把公众股东实际能拿到的东西夸大了约四倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/4397bb5c-3e31-4950-9c1b-bb71999e6b25_3641x2195.png)
*来源：SemiAnalysis Memory 模型、公司报告 - sales@semianalysis.com*

正是这一表决权结构，削弱了公司关于「无控股股东、无实际控制人」的声明——招股书将其列为正式的治理风险。CXMT 通过一致行动协议对其晶圆厂行使多数表决权，而国家大基金二期、合肥、安徽等国有主体即便在上市后合计持股也远超 30%。在 CXMT 与中国国家的关系受到最严密审视的当下，这一安排看起来是为管理出口管制与外国投资者认知而设计。

![](https://substack-post-media.s3.amazonaws.com/public/images/426898f7-e476-4457-a54e-cb4e4471bc0a_3174x2146.png)
*来源：SemiAnalysis Memory 模型、公司报告 - sales@semianalysis.com*

媒体报道的募资额将严重低估这次上市。CXMT 计划投入 295 亿元人民币（约 41 亿美元），同时发行上市后股本的 10% 至 15%。若完全通过 IPO 为这些用途融资，意味着按 10% 稀释发行价约为每股 4.41 元，按 15% 则约为 2.78 元，而 2025 年 6 月那轮融资的价格为 2.63 元。即便 1Q26 营收达 73 亿美元、净利润 48 亿美元，发行价下限所代表的每股增值也几乎为零。按 2.78 元计，CXMT 的估值约为 1,970 亿元人民币（270 亿美元），仅相当于 2026 年上半年年化归母盈利的 1.8 倍。这一算术底线远低于现实的书档询价估值。在我们看来，这太便宜了，估值理应高得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/eecda393-5735-4a35-ac4c-c8373cf1086b_3641x2195.png)
*来源：SemiAnalysis Memory 模型、公司报告 - sales@semianalysis.com*

募投资金的配置强化了 CXMT 当前的优先级。在计划募集的 295 亿元净额中，205 亿元（69.5%）投向晶圆产线与 DRAM 技术升级，90 亿元（30.5%）用于前瞻性 DRAM 研究。招股书未披露专门的 HBM 项目，甚至没有提及 HBM。其项目描述聚焦于更新的工艺平台、产品迭代，以及现有产线向中高端 DRAM 的迁移。因此，此次 IPO 主要强化的是 CXMT 的核心 DRAM 制造与技术基础，没有任何已披露的针对近期 HBM 扩产的资金承诺。

![](https://substack-post-media.s3.amazonaws.com/public/images/8cb018a5-1574-4796-b9a0-c4bc276821cc_3641x2195.png)
*来源：SemiAnalysis Memory 模型、公司报告 - sales@semianalysis.com*

盈利变动之巨，值得就周期时点打上一个标记。CXMT 在 2025 年 12 月的申报文件中指引 2025 财年归母亏损 6 亿至 16 亿元人民币。五个月后，招股书报告了 18.7 亿元的盈利，合并利润超过了此前指引上限的两倍。这也显示了 DRAM 峰值定价能以多快的速度向任一方向撬动估值分母。

最后，阿里巴巴在股权结构表中的位置，改变了解读 CXMT 需求的方式。阿里云既是锚定超大规模云客户，又是持股近 4% 的股东和背书者，与董事长朱一明自己的无厂设计公司兆易创新（持股 1.8%）并列。本土销量因此获得了实质性保障——这是韩国在位者在其本土市场从未有过的条件，其意义远超这些小百分比所显示的。

面向付费订阅者，我们将深入解析 CXMT、中国更广泛的晶圆厂设备（WFE）生态、出口管制的影响，以及对中国存储与算力雄心的意涵。我们也将在付费部分更详细地讨论 HBM。

## **出口管制下的 CXMT 设备生态：国产对进口，以及国产化曲线**
