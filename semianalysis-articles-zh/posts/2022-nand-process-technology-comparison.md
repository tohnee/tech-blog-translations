---
title: "2022 NAND——制程技术对比：中国 YMTC 出货密度最高的 NAND、Chips 4 联盟、长期财务展望"
title_en: "2022 NAND – Process Technology Comparison, China's YMTC Shipping Densest NAND, Chips 4 Alliance, Long-term Financial Outlook"
date: 2022-08-12
source: https://newsletter.semianalysis.com/p/2022-nand-process-technology-comparison
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 2022 NAND——制程技术对比：中国 YMTC 出货密度最高的 NAND、Chips 4 联盟、长期财务展望

> 原文：[2022 NAND – Process Technology Comparison, China's YMTC Shipping Densest NAND, Chips 4 Alliance, Long-term Financial Outlook](https://newsletter.semianalysis.com/p/2022-nand-process-technology-comparison) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

NAND 是一个竞争惨烈、进步步伐永不停歇的市场。制造并出货的 NAND 位元数量以每年 30% 到 35% 的速度增长，每 2 到 3 年翻一番。乍看之下，这似乎需要投入大量资本购置新设备，但从 2017 年到 2022 年，尽管位元呈指数级增长，NAND 行业每年在晶圆制造设备上的支出却只有 $15B 到 $20B。NAND 的生产成本已快速下降。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/cbb91d9e-b257-425f-95ae-4a53edf5cb44_3252x2268.jpeg)

类似的成本缩微改善在几十年前的 DRAM 和逻辑等其他半导体技术中很常见，但在后摩尔定律时代，这些细分行业会把这种改善速率视作天方夜谭。生产力的提升主要来自泛林（Lam Research）刻蚀与沉积工具的改进，以及各制造商开发的制程节点。

纵观历史，每当半导体行业保持如此之快的创新速度时，许多公司都会在技术上被远远甩在身后。行业整合随之发生，只有少数强者胜出。今天的 3D NAND 正处于类似的境地，这个行业的未来经济学正在剧烈变动。Intel 卖掉了他们的 NAND 业务，而铠侠（Kioxia）和西部数据（Western Digital）内部则动荡不断。

在本报告中，我们想对三星（Samsung）、SK 海力士（SK Hynix）、美光（Micron）、Solidigm、YMTC、西部数据和铠侠的制程技术做一次状态检查。简要结论是：美光、SK 海力士和 YMTC 正在把其他公司甩在身后。与此同时，尽管三星就在几年前还是 NAND 技术的绝对领导者，如今却奇怪地落后了。[SemiAnalysis](http://semianalysis.com/) 与 [Angstronomics](https://www.angstronomics.com/) 共同编制了下表。表中有很多细节，将在报告中逐一解释。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/73fa6319-741c-44fd-b6d2-23352e7ad229_896x662.png)

最大的亮点是：中国的 YMTC（长江存储）目前出货的已是密度最高的 3D NAND。我们将独家详述 YMTC 最新制程技术的规格与细节——这些是他们在第一方材料中有意隐匿的信息。这类似于[中国的 SMIC，对其 7nm 制程技术未披露任何信息](https://semianalysis.substack.com/p/chinas-smic-is-shipping-7nm-foundry)。我们手上还有关于潜在制裁/设备禁令、Chips 4 联盟，以及 SK 海力士和三星在华现有 NAND 工厂的信息。

最后，我们还将详述 NAND 行业的财务前景，包括跨周期的长期盈利能力和自由现金流利润率。其中包括对西部数据和铠侠在 NAND 业务上摇摇欲坠的未来的讨论，以及一则收购要约的传闻。

# **潜在的对华设备禁令、Chips 4 联盟、在华现有工厂**

在进入技术与商业部分之前，我们想先讨论地缘政治动态。已有多篇报道提到美国正在考虑对华禁售 3D NAND 设备。去年，我们为一家 PAC 撰写过一份在华盛顿圈内传阅的报告，提出了这个想法及其影响。基本剧情是：泛林（Lam Research）及其他半导体制造设备公司的对华出口可能被叫停。如果这些设备被封锁，YMTC 以及三星和 SK 海力士当前的 3D NAND 扩产都将被叫停。

Chips 4 联盟是美国、日本、台湾地区和韩国之间一个潜在的联盟。这 4 个国家和地区在半导体供应链的每个环节都占据大部分市场份额，包括晶圆衬底、光刻胶、CMP 抛光液和刻蚀气体等供应链投入品。这些国家还代表着大部分晶圆制造设备、存储公司、代工厂和 IDM。

该联盟的目标是增强供应链安全、开展研发合作以及人才队伍建设。其明显的潜台词是：这个联盟将被用于遏制中国在半导体行业的快速崛起。韩国对加入联盟公开态度冷淡。据我们了解，韩国政府和民间已转向对华非常强硬，所以这可能只是一种姿态。

如果韩国选择不加入 Chips 4 联盟，我们听说美国甚至可能逼其就范。手段之一就是禁止 3D NAND 设备输华。三星和 SK 海力士都在中国设有 NAND 工厂。加上 YMTC 的产能，我们的数据显示，2022 年第三季度中国占全球 NAND 产量的 24%。此外，SK 海力士在中国还有 DRAM 工厂。美国的设备禁令将有效迫使韩国在半导体领域减少与中国的合作，因为这些工厂无法再扩产。

SK 海力士的处境非常艰难。他们当年是被可观的 DRAM 和 NAND 工厂补贴吸引到中国的，如今却在升级产线上遇到困难。存储业务依赖最先进的技术来压低每比特成本。在 DRAM 方面，SK 海力士最新的 DRAM 节点使用 EUV 光刻，而中国无法进口。这意味着他们在华 DRAM 工厂将慢慢落后。几年之内，其每比特制造成本将无法与中国以外的 SK 海力士工厂竞争。SK 海力士计划未来把在华现有 DRAM 工厂转为 3D NAND，因为 3D NAND 设备目前尚无出口管制。这将是一次代价高昂的资本转型，但这是已规划并预期多年的安排。如果 3D NAND 设备禁令落地，这些计划将全部改变。

如果无法向中国进口 3D NAND 设备，三星和 SK 海力士都将陷入非常艰难的境地。他们可以为新节点改造现有设施，但 3D NAND 制造的生产力提升有相当大一部分来自泛林的新工具或升级工具。禁止 3D NAND 设备输华将葬送 YMTC 的未来扩产，并使三星和 SK 海力士长期在华运营的成本变得高昂。如果美国落实这项禁令，可能会以在美补贴来缓和对三星和 SK 海力士的打击。

[分享](https://newsletter.semianalysis.com/p/2022-nand-process-technology-comparison?utm_source=substack&utm_medium=email&utm_content=share&action=share)

# **YMTC**

YMTC 对其新一代 NAND（以 Xtacking 3.0 之名营销）讳莫如深。他们不会在任何官方场合公布层数。官方口径仅止于把 Xtacking 3.0 宣传为业内密度最高的 1Tb TLC NAND。我们猜想 YMTC 之所以隐瞒这一技术细节，是出于对美国制裁的担忧。[SMIC 隐瞒其 7nm 技术、同时大批量爬坡 14nm](https://semianalysis.substack.com/p/chinas-smic-is-shipping-7nm-foundry) 的做法可以找到许多相似之处。在这个背景下，YMTC 的遮遮掩掩就说得通了。

YMTC 开发出了一些相当出色的制程技术。SemiAnalysis 可以独家详述 YMTC 未公布的规格。第一，Xtacking 3.0 是密度最高的商用 1Tb TLC NAND，达 15.2Gbit/mm2。第二，一位员工告诉我们它是「超过 230 层」；我们认为是 232 层。第三，其性能可与美光的 232 层 NAND 相媲美，采用类似的 6-plane 架构、2.4Gbps 数据速率。第四，它已在向合作伙伴出货。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/4895f8e5-71fa-4c09-b470-a3c34386b950_5313x3934.jpeg)

我们是在 [Angstronomics](https://www.angstronomics.com/) 的远程协助下通过测量一颗实体裸片确证上述事实的。拿到实体裸片也让我们确认了它是 6-plane 架构。我们还通过与员工的正式和非正式交谈获得了更多细节。我们在他们展台待的时间太长，以至于他们甚至请我们帮忙拍了公司合影。我们在一家第三方台湾公司的展台上发现了封装在 SSD 中的他们的新 NAND。对方很乐意告诉我们一些其他细节，包括出货时间。

未来，我们可能会专门写一篇关于其创新技术的文章，例如晶圆键合的 CMOS under Array（阵列上 CMOS）、居中驱动（center driver）的 XDEC，以及从正面深沟槽（Front Side Deep Trench）工艺向背面源极连接（Back Side Source Connect，BSSC）的转型。YMTC 还计划为实现内存计算（in-memory processing）部署更多逻辑电路，包括利用其堆叠 CMOS 技术实现类神经形态计算。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a6a10d87-7891-4062-be4d-327d9eec3073_6761x3739.jpeg)

YMTC 并不像许多人误以为的那样，只是一家拿着成熟制程技术照搬的模仿者——许多人正是这样误判中国半导体公司在先进制程上的表现。他们正在打造自己独一无二、具备创新性的产品。尽管他们严重依赖超过 240 亿美元的政府补贴、泛林的工艺设备，以及从 Adeia（Xperi）获得的关键技术授权，但凭借本土创新，他们已在 NAND 领域跑在其他玩家前面。

YMTC 的良率仍然落后，但一直在快速改善。几年之内，我们毫不怀疑 YMTC 的成本竞争力将追平业内最优秀的公司。他们将从根本上改变 NAND 行业。那些在技术上不具备持久优势、也没有大额补贴的公司，将面临[关于其未来业务存续性的末日审判](https://semianalysis.substack.com/p/the-impending-chinese-nand-apocalypse-e01)。YMTC 的第二座工厂设备几近装满，第三座工厂在建。据称第四座工厂的融资已经在推进，最早明年年中开工。YMTC 的每座工厂月产能均为 100,000 片晶圆。

# **铠侠与西部数据**

铠侠和西部数据在 3D NAND 的制造和技术开发上是合作关系，因此放在一起讨论。他们估计 2022 年将出货 1 个 Zettabyte 的 NAND。他们的 Flash Memory Summit 演讲涵盖了 3D NAND 缩微的一些权衡取舍。缩微有 4 个主要方向：纵向缩微、横向缩微、架构缩微和逻辑缩微。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/00f6a7e2-6431-440a-9930-815edca415d6_6826x4159.jpeg)

上面这张关于从 SLC、MLC、TLC、QLC 到 PLC 缩微路径的幻灯片很有意思。单元中存储的比特数越多，读取延迟越高、擦写循环耐久度越低。铠侠和西部数据正在探索使用每单元 4.5 比特或每 NAND 单元 3.5 比特，以在不那么牺牲延迟和耐久度的前提下提高密度、改善成本。

在 3D NAND 中，工程选择往往落在性能、成本和耐久度的光谱之间。容量越大、单位成本越低，但同等容量的 SSD 性能就越弱。单元尺寸越大性能越好，但难以向更高层数缩微，制造成本也就越高。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/555c904f-898c-413e-bb94-69fc1c1777c2_6597x1883.jpeg)

PCIe 在 3.0 上停滞了许多年，但近年来的代际升级明显提速。这带来了为充分利用可用带宽的大量创新。铠侠和西部数据表示，其 NAND 的接口带宽每代提升 30%。此外，他们引入了异步独立 plane 读取（asynchronous independent plane read），使每个 plane 内的读取可以更高效地打包（大多数竞争对手已引入或将在其下一代中引入）。得益于这些创新，随机读性能已显著改善。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/74234fbe-2881-41cd-83d3-ffd9d4de4dd8_3988x2268.jpeg)

西部数据和铠侠的路线图既包括层数缩微，也包括与层数无关的技术。晶圆键合被列为下一项将采用的技术，作为提高单元阵列效率的手段。而这正是 YMTC 借 Xtacking 3.0 已迭代到第三代的技术。PLC NAND 也在考虑之中。西部数据告诉我们，他们甚至在实验室里试验过每单元高达 7 比特（128 个电压等级）。它在实验室里是存在的，但需要液氮维持的极低温度。

铠侠和西部数据是仅有的把 PLC 电荷俘获（charge trap）存储放上路线图的公司。CMOS 缩微和单元间距缩微也在路线图上。他们讨论的最后一项技术是多级堆叠（multi-stacking）。CMOS 阵列和多个 NAND 阵列将通过顺序化的混合键合方法全部堆叠起来。这项技术的成本改善在理论上较为有限，但密度增益将非常可观。

铠侠和西部数据还开发出了第二代存储级内存，以 XL-FLASH-2 之名营销。由于成本更高，它能否上量还有待观察，但凭借 16-plane 和 MLC NAND，它的速度快得多。这种产品只有在更低延迟的 CXL 总线上的大规模部署才说得通，但那类工作负载往往更青睐 DRAM 池化/共享。

铠侠和西部数据的业务/财务状况将在本文后面单独讨论。

# **三星**

三星在 NAND 市场占有率上长期居首。他们在历史上的多次技术转型中都处于领先地位，这从[闪存的历史与时间线](https://semianalysis.substack.com/p/the-history-and-timeline-of-flash)中可见一斑。这一技术领先优势一直延续到其 128 层技术——全球出货量最大的 NAND 制程节点。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f66c9b81-f9a4-4381-bfda-5fe1c8892131_950x445.jpeg)

3D NAND 最关键的工艺步骤，是穿过许多层 NAND 的高深宽比刻蚀及随后的沉积步骤。虽然业内几乎所有人这些关键步骤的大部分都使用泛林的工具，但三星是唯一一家一次性刻蚀超过 120 层的公司。其他厂商在其超过 100 层的 NAND 架构上采用多个 deck，而三星的 128 层只用 1 个。例如，Solidigm 的 144 层 NAND 用了 3 个 deck。每多一个 deck 都会增加成本。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2633849d-f491-407b-9b81-1fa1156fb7be_4000x2250.png)

尽管在 128 层上领先，三星却已多年没有出货新的 NAND 制程技术。逆向工程公司和拆解机构都没有在任何 SSD 中发现他们的 176 层和 >200 层 NAND 制程技术。尽管他们宣称 2021 年就出货了 176 层消费级 SSD。官方原因未予披露，但很可能源于[文化问题引发的工艺麻烦](https://semianalysis.substack.com/p/samsung-electronics-cultural-issues)。三星仍然声称，第 7 代 V-NAND（176 层 512Gb TLC、2Gbps）是 2021 年的技术。他们还提到 176 层 1Tb QLC 即将推出。第 8 代 V-NAND 超过 200 层。三星称其将是 1Tb TLC 裸片、2.4Gbps，2022 年出货。第 8 代将同时实现横向缩微、更多层数和外围电路缩微。三星还把第 9 代 V-NAND 排在了 2023 年。鉴于第 7 代 V-NAND 的现状，我们对这些说法持怀疑态度。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/875b13c5-589e-4228-be16-486b5261f35e_6028x1705.png)

三星正处于一个微妙的位置：曾经落后的公司正在反超并开始取得更好的成本结构。层数并不是 NAND 缩微的全部，最终每比特成本还取决于许多其他因素。根据我们的成本模型，凭借长期沿用的 128 层制程节点带来的高资本效率和良率，三星仍拥有第二具成本效益的 NAND 制程技术。我们的理论是：三星之所以回避爬坡其 176 层 NAND，是因为转向 2-deck 架构后，它的成本效益不如 128 层。

如果三星继续推迟其新制程节点，就有进一步掉队的风险。顺带一提，我们在 Flash Memory Summit 上交谈过的多家竞争对手的工艺工程师，都对三星 NAND 制程节点的现状一头雾水。

# **SK 海力士与 Solidigm**

SK 海力士的相对位置一直在改善。他们快速爬坡了 176 层 TLC，176 层 1Tb QLC 将于第四季度量产。我们的成本模型把 SK 海力士列为第三具成本效益的 NAND 制程技术，而且他们甚至可能很快与三星互换位置。

SK 海力士的 238 层将于明年上半年以 512Gb TLC 裸片开始量产。SK 海力士称，新 NAND 技术将使每片晶圆产出多 34% 的比特、IO 速度快 50%、编程性能好 10%、读取能效好 21%。这款 NAND 的速度惊人，达 2.4Gbps。美光和 YMTC 在其 232 层技术中都只规划了 1Tb 裸片，而 SK 海力士用更小的 512Gb 裸片、只用 4-plane 而非 6-plane 就达到了同样的速度。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7e620420-fc75-45e1-b4cd-9a935bf06385_6560x1833.jpeg)

SK 海力士展示的未来路线图非常有意思。他们表示，在 238 层这一代之后，计划再沿用 CMOS under Array（阵列上 CMOS）NAND 3 代。特别是，下一 xxx 层 NAND 制程将是一次幅度更大的层数提升和更快的过渡。

SK 海力士为其长期创新取了个糟糕透顶的营销名字——4D^2。这些技术涉及共享位线（bit line）和更多行。他们讨论的方案不再是让单元彼此独立、以 8 个电压等级存储每单元 3 比特，而是用 2 个单元串联存储超过 6 比特数据。所有这些技术的焦点似乎都是往每一层里塞进更多比特。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3c143043-9bf3-4fce-8c4b-0c85fba3cc38_7039x1992.jpeg)

话题转到 Solidigm（原 Intel NAND 业务），其 NAND 架构有所不同。Solidigm 使用浮栅（floating gate）架构，而 SK 海力士使用电荷俘获（charge trap）。SK 海力士计划将自研的电荷俘获技术用于性能和主流市场，而 Solidigm 将用于价值和替代 HDD 的市场。SK 海力士与 Intel 交易条款的一部分是：Intel 的制程技术人员在几年后才转移过来，而非立即到岗。Solidigm 的中国大连工厂至少未来几年仍将运行 Intel 开发的制程技术。

Solidigm 的下一代浮栅节点是 192 层。我们认为这是一个 4-deck 设计，每个 deck 48 层。若搭配 TLC 架构，这一制程的成本效益将大有争议。这一成本劣势通过在每单元塞更多比特来缓解——这是浮栅架构相对电荷俘获架构的一项优势。虽然大多数电荷俘获产能是 TLC（每单元 3 比特），但 Solidigm 的节点聚焦 QLC 以换取产出量。

192 层 QLC 将带来 1.33Tb 的裸片容量。QLC 长期为糟糕的性能所困，因为要精确保持 16 个电压等级才能每单元存储 4 比特，而新节点声称解决了其中许多问题。第 4 代 QLC 有一些相当亮眼的数据：编程写入时间快 2.5 倍、随机读好 5 倍、第 99 百分位读取延迟好 1.5 倍。这些改进将使 Solidigm 192 层 QLC 的性能大幅逼近电荷俘获 TLC。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8fd92242-f3c3-4207-89e4-90965b9b4c63_7831x2271.jpeg)

更令人兴奋的变化是，192 层制程将带来首款上量的 PLC NAND，裸片容量 1.67Tb。在 PLC 下，单元必须能够精确保持 32 个电压等级，才能每单元存储 5 比特。这将把每片晶圆产出的比特数提升 25%，但牺牲了性能。鉴于 SK 海力士把 PLC NAND 定位为替代 HDD 的技术，性能损失恐怕不小。一个有趣的噱头是，Solidigm 团队用一块采用 192 层 PLC NAND 的外置 SSD 播放了整场演示。

# **美光**

美光一直是 NAND 行业中浴火重生的凤凰。几年前，他们还与 Intel 在 IMFT 合资项目中紧密捆绑，使用浮栅架构——无论每比特成本还是性能都不如电荷俘获。他们的 DRAM 制程技术也落后三星几年。

美光做出了一些大刀阔斧的改变，如今已是存储行业的领导者。Sanjay Mehrotra 是 SanDisk 的联合创始人兼 CEO，SanDisk 以 $19B 卖给了西部数据。不久之后，他受聘出任美光 CEO。与 Intel 的合资公司（IMFT）解散，NAND 架构从浮栅转向电荷俘获。3D XPoint 内存的开发也被叫停。

美光一些底层的工艺和文化问题得到了修复。美光的 3D NAND 成本结构从最差之一变成了最好。同样，他们的 DRAM 从密度最低、每比特制造成本最高，变成了出货密度最高的 DRAM、成本结构第二好。

美光的大部分产能是 176 层，且正在爬坡出货 232 层 NAND。美光的战略一直是基本保持晶圆投片量不变，靠好得多的制程技术来拉动比特出货增长。这让他们得以压低资本开支（CAPEX）的同时保住市场份额。随着总额 $40B 的全新建厂（greenfield）投资可能因《芯片法案》落地美国，这一战略或将转变。

美光的 6-plane、2.4Gbps、1Tb TLC 232 层 NAND 出现在多家 SSD 和控制器公司的展台上。这些第三方公司告诉我，他们预计爬坡会很快，232 层明年将占美光出货量的大头。关于其规模处于勉强及格边缘的问题确实存在，但更多内容留待后文。

# **长期财务展望与西部数据、铠侠的未来**

NAND 行业整体的长期自由现金流利润率，以及西部数据和铠侠各自的未来，将在仅限订阅者的部分讨论。我们拿到的一条独家消息与一项非正式的**对西部数据 NAND 业务的收购要约**有关。

感谢阅读 SemiAnalysis。如果你喜欢这篇内容，请分享给其他可能喜欢的读者。

[分享](https://newsletter.semianalysis.com/p/2022-nand-process-technology-comparison?utm_source=substack&utm_medium=email&utm_content=share&action=share)
