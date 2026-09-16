---
title: "三星电子（Samsung）的文化问题正在其代工、LSI 乃至 DRAM 存储业务中酿成灾难！"
title_en: "Samsung Electronics Cultural Issues Are Causing Disasters In Samsung Foundry, LSI, And Even DRAM Memory!"
date: 2022-04-17
source: https://newsletter.semianalysis.com/p/samsung-electronics-cultural-issues
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# 三星电子（Samsung）的文化问题正在其代工、LSI 乃至 DRAM 存储业务中酿成灾难！

> 原文：[Samsung Electronics Cultural Issues Are Causing Disasters In Samsung Foundry, LSI, And Even DRAM Memory!](https://newsletter.semianalysis.com/p/samsung-electronics-cultural-issues) · SemiAnalysis

三星电子（Samsung Electronics），更确切地说是三星旗下的各个半导体业务板块，正深陷困境。在上个十年之交，三星还站在世界之巅：代工份额快速提升，是代工领域最快完成多次逻辑制程节点转换的厂商；三星 LSI 设计团队产出的移动芯片设计业界最佳；Apple 所有关键部件的制造完全依赖三星；在 DRAM 生产成本上，三星领先其他厂商多年。这些技术优势正在全面瓦解。

三星电子存在一个动摇其根基的文化问题。三星在技术开发的方方面面都在滑坡，包括他们历史上碾压所有对手的那一个领域——DRAM。他们已不再能产出位居前三的移动 SOC，连 MediaTek 都已实现反超。代工业务在短短时间内连失两个最大客户，均转投 TSMC。有可信度较高的报告指出，三星代工业务内部存在谎言与欺瞒。甚至连 Intel 尚在初创期的新代工业务，也从三星代工撬走了一两个客户！

本文将报道韩国媒体披露的诸多症候，以及我们自己对该课题的部分研究。需要说明的是，来自韩媒的部分细节未经核实，但整体性的问题是清晰可见的。

三星电子显然出了问题。

这些问题直接源自三星的文化构成。在深入细节之前，我们认为总体趋势是：这些问题已积酿多年，而如今沸点已至。

先从这段故事里也许最温和的部分讲起，再推进到最严重的部分。三星曾有一项名为[「Game Optimizing Service」（游戏优化服务）](https://meeco.kr/ITplus/34754710)的服务，它对除常见基准测试之外的大多数应用进行限速，甚至包括 [Netflix 和 Instagram 等非游戏应用](https://meeco.kr/ITplus/34755550)。坦白说，我们对此并未感到愤怒，因为 Android OEM 在[基准测试作弊](https://www.anandtech.com/show/15703/mobile-benchmark-cheating-mediatek)方面[劣迹斑斑](https://www.anandtech.com/show/7187/looking-at-cpugpu-benchmark-optimizations-galaxy-s-4)。三星正因这一行为面临[集体诉讼](https://www.asiatoday.co.kr/view.php?key=20220318010010413)。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

三星为什么要启用这项「Game Optimizing Service」？当然是为了控制发热与功耗。随着三星的制程节点问题接连暴露，最近几代产品的发热与功耗一路失控。甚至追溯到多年前的三星自研 CPU，其设计就因领导不力而告失败。三星还有一个被砍掉的 GPU 团队。这两个案例又一次说明：自研芯片远比表面看起来困难。设计公司与晶圆厂的文化对成功至关重要。这些天才工程师需要正确的激励、方向和领导。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9106b83d-4bb1-4c19-90de-11268442955f_633x892.jpeg)

自研 GPU 架构失败后，许多三星的支持者对转向[采用 AMD 基于 RDNA 的 GPU IP](https://www.anandtech.com/show/14492/samsung-amds-gpu-licensing-an-interesting-collaboration)感到兴奋。这份兴奋非常短命。与代工和工艺节点相关的问题，在本代 [Exynos 2200](https://drive.google.com/file/d/1Bj58pQPiwS4y6cXyk2SFle9e8zzoLzPm/view) 上真正爆发。其每瓦性能极其糟糕。而基于 RDNA 的 GPU 的性能与功耗，并非这颗 SOC 唯一的问题。

三星最初计划在全球更大范围内启用 Exynos 芯片。一些分析师与行业刊物甚至预测，Galaxy S22 系列总出货量中高达 60% 将采用 Exynos 2200、40% 采用高通 S8G1。当然，结果成了一枚哑弹，Exynos 的实际出货量最终不足 25%。我们并不认为计划真到过 60%，但确实听说三星曾想把 Exynos 处理器的份额提升到 40%。出货量未达标主要归因于性能与良率。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/51804c13-f7d1-4af3-b3f6-3bd2521cb2f0_1024x655.png)

据报道，三星 Exynos 2200 的[良率极其惨淡](http://www.thelec.kr/news/articleView.html?idxno=16234)。这部分源于其采用的 4LPE 节点。该节点相对三星 7/5nm 家族的创新，在于[提供 198nm 的 UHD 单元高度](https://www.linkedin.com/posts/yuzo-fukuzaki-12408111_samsung-exynosabr2200-4lpe-activity-6917180674298761216-8yXC/?utm_source=linkedin_share&utm_medium=member_desktop_web)，而前代节点的 UHD 单元高度为 218nm。据传该节点的良率低至 20%。这一数字看起来过低，但我们了解到：虽然灾难性良率没有问题，参数良率（parametric yield）却相当糟糕。另一位消息人士告诉我们，最终出货的芯片以更高的功耗、调低的性能目标交付，参数良率约为 80%。无论如何，传闻称[高管之间存在协议](https://m.clien.net/service/board/park/16995380)：无论在经济性或功耗/性能上是否合理，都要尽可能用上最新的节点。自上而下的文化问题可见一斑。

简单解释一下：灾难性良率损失，指某个晶体管、通孔或某段金属层完全无法工作；参数良率损失，指它们能够工作，但问题是能否达到性能、功耗、电压等指标目标。Exynos 2200 的参数良率如此之低，芯片指标只能下调。事实上，[传闻指向](http://www.thelec.kr/news/articleView.html?idxno=16234)三星把 GPU 频率从计划的 [1.69GHz 下调至 1.49GHz，最终下调至 1.29GHz](https://n.news.naver.com/article/014/0004774178)。

问题并不止于代工与 SOC 团队未能达成技术目标。在面对失误时，其文化相当有害。据称这些部门正在彼此[推诿指责](https://www.greened.kr/news/articleView.html?idxno=295149)：三星 LSI（设计）怪罪三星代工，而三星移动（Mobile）怪罪 S.LSI。

在另一些案例中，三星 LSI 高管甚至似乎在归咎于[韩国劳动法的变化](http://m.thebell.co.kr/m/newsview.asp?svccode=00&newskey=202204091554435640102620)。员工每周工时本应被限制在最多 52 小时，而不是靠冲刺期让工程师连轴转、工作荒谬的时长。虽然我们听说这一规定并未被完全遵守，但它确实减少了三星众多工程师的过度劳动。三星方面的反弹如此强烈，以至于甚至有人在推动立法放宽这些劳动法。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

三星半导体的文化已经糟到这样的地步：代工部门据称[在良率上撒谎](https://www.fnnews.com/news/202202131249028377)。韩媒报道，管理层正在进行审查与审计。审查的结果很可能是管理层与团队的重组，类似去年无线业务部门的重组。[后续关于撒谎的报道](https://www.infostockdaily.co.kr/news/articleView.html?idxno=167041)甚至深入到指控三星代工在 5nm、4nm 和 3nm 良率问题上对客户和三星会长撒谎。鉴于韩国如此多的媒体报道、如此多的本地专家发声，这些报告看起来相当可信。我们甚至不会深入探讨三星在 FinFET 转型期间[对 TSMC 实施的商业间谍行为](https://www.theregister.com/2015/08/25/tsmc_samsung_espionage_judgment/)。

我们确切知道的是：高通对三星非常不满。[据 TechInsights](https://www.linkedin.com/posts/yuzo-fukuzaki-12408111_samsung-exynosabr2200-4lpe-activity-6917180674298761216-8yXC/?utm_source=linkedin_share&utm_medium=member_desktop_web)，高通采用的是三星 5nm 节点的一个变体，称为 4LPX，而非 Exynos 2200 所用的密度更高的 4LPE 节点。另有多个消息源告诉我们，S888 与 S8G1 处理器的参数良率相当差，导致高通不得不把这些 SOC 推到高得多的功耗水平，才能达到特定的性能目标。

虽然高通 S8G1 的报告良率不像 Exynos 2200 那么低，但也远远谈不上合格。顺带一提，这对高通（和 Nvidia）倒是无妨。我们被告知，这两家客户已谈成按良品裸片付费，而非按投片晶圆付费。

由于 S765G、S780G、S888 和 S8G1 的种种问题，高通决定在其高端 SOC 上彻底离开三星代工。高通甚至组建了专门团队，连载数月、夜以继日地为 TSMC 的 N4 工艺节点准备 S8G1+。在可预见的未来，S8G2 及后续的高通高端芯片都将由 TSMC 生产。尽管近几个月智能手机市场放缓，但由于高通带来的份额转移以及单机内容量的持续增长，TSMC 今明两年在智能手机业务上或许仍能保持增长。

随着 S.LSI 部门在智能手机 SOC 上举步维艰，三星移动一直在加紧寻找替代方案。[韩国的传闻](https://meeco.kr/mini/34835643)甚至称，三星已开始为 Galaxy A 系列评估 MediaTek 的 Dimensity 产品线。三星移动总裁 TM Roh 博士表示，将有[一款 Galaxy 手机专用的应用处理器](https://www.greened.kr/news/articleView.html?idxno=295149)。这一点相当奇怪，因为大多数 S.LSI 的 Exynos SOC 虽然对外销售，基本上却是三星 Galaxy 智能手机独占。这指向三星移动与 S.LSI 之间更多的内斗与纠葛。

三星代工的问题更深。[正如我们去年所报道](https://semianalysis.substack.com/p/samsung-foundry-3nm-gate-all-around?s=w)，其 3nm GAP 节点的代工产品直到最晚 2024 年才会向外部客户出货。3GAE，第一个环栅（GAA）节点，被一而再、再而三地悄悄推迟，[甚至可能被取消](https://biz.sbs.co.kr/article/20000055654)。据称其良率极其糟糕。如果有谁认为三星能借 TSMC 的 N3 问题以及 N2 要到 2025 年底才量产的机会赶上 TSMC，那就大错特错了。

三星昏招迭出，失去了其最大的代工客户高通，以及第二大代工客户 Nvidia。正如我们本周早些时候在[对 Nvidia 下一代 Ada Lovelace 游戏 GPU 的深度解析](https://semianalysis.substack.com/p/nvidia-ada-lovelace-leaked-specifications?s=w)中所报道的，其工艺技术是 TSMC N4 的定制衍生版，称为 4N。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

三星 LSI 也并非全然一团糟。他们正凭借设计精良、高效且价格合理的芯片，在 5G 基础设施市场不断扩大份额。他们还在车载信息娱乐系统上赢得不少设计，例如与[现代（Hyundai）](https://m.sedaily.com/NewsViewAmp/260V2GIB89)和[大众（Volkswagen）](https://m.etnews.com/20211130000125)的合作。S.LSI 似乎相当擅长与客户紧密协作，例如与 Google 合作 [Tensor 智能手机 SOC](https://www.anandtech.com/show/17032/tensor-soc-performance-efficiency)。尽管有这些成功，S.LSI 似乎在每个节点上都受到掣肘——三星代工似乎让他们丢掉了下一代 [Cisco Silicon One 网络 ASIC 的合同，而这份合同输给了 Intel！](https://semianalysis.substack.com/p/intel-is-throwing-the-kitchen-sink?utm_source=url)

S.LSI 多年来一直与 Tesla 紧密合作开发自动驾驶/ADAS 的 HW 3.0。这是一颗联合设计的芯片，由三星协助 Tesla 完成，[双方都为最终的芯片设计贡献了有分量的 IP](https://en.wikichip.org/wiki/tesla_(car_company)/fsd_chip)。该芯片设计已出货数百万颗，进入 Tesla 的车辆。HW 4.0 原定于去年底量产，但延误似乎使其拖到了今年。连同 Ambarella 在内，Tesla 是 S.LSI/代工业务仅存的主要外部客户。

S.LSI 近来还栽了其他跟头，例如在图像传感器市场。他们的 ISOCELL 智能手机传感器采用混合键合（hybrid bonding）的进度缓慢，不像 Sony [自 2017 年起就已大批量出货](https://semianalysis.substack.com/p/advanced-packaging-part-2-review)。此外，他们未能在中国智能手机厂商处赢得份额——后者在高端选用 Sony，在中低端选用 Omnivision。独立相机传感器与相机业务曾归入名为 Samsung NX 的独立部门，但[后来也被砍掉](https://m.etnews.com/20170405000273?obj=Tzo4OiJzdGRDbGFzcyI6Mjp7czo3OiJyZWZlcmVyIjtOO3M6NzoiZm9yd2FyZCI7czoxMzoid2ViIHRvIG1vYmlsZSI7fQ%3D%3D)——尽管三星在独立相机领域已投资数十年。

# **三星 DRAM 大溃败**

三星电子的现金牛——三星 DRAM——也并非一帆风顺。5 年前，三星在密度、性能与成本结构上无疑优于美光（Micron）和 SK 海力士（SK Hynix），一些估算认为当时他们领先多达一年半。如今，尽管出货量远大于这两家同行，三星在其中一些指标上可以说已经落后于 Micron 与 SK Hynix。罪魁祸首是三星在工艺开发上过于激进的做法，而这正源于其文化问题。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/39816318-fa7a-4f00-892f-323aceba6d4a_1024x587.png)

先做一点科普：随着电容微缩放缓，DRAM 的密度与成本微缩已大幅减速。1Xnm 代是这场大幅减速的第一个信号，自那以后，每代节点的成本微缩只有约 15%。密度增益如此乏力，以至于 DRAM 厂商改用字母作为节点后缀，而非 20nm 以前时代的数字。在 1Y 代，三星在成本、功耗与性能上相当领先于竞争对手。

这一切在 1Z 代发生改变。三星决定在 EUV 导入上非常激进。这是一个自上而下驱动的决策，而非工程决策。这类自上而下的决策在三星电子内部相当普遍，正是我们一直指出的文化问题的结果。在 1Z 代，三星宣布采用 EUV，大张旗鼓、广发新闻稿。三星对这项「成就」无比自豪。

三星吃下了早期 EUV 光刻机出货的约 50%，主导了早期分配。三星试图将 EUV 同时导入 DRAM 以及他们搞砸的早期 7nm 逻辑尝试。1Z DRAM 节点从未完全爬坡。这一趋势延续到了下一代 1 Alpha 节点——EUV 的使用进一步增加。据报道，该节点的开发耗时更长。虽然三星宣称 1 Alpha 已进入量产相当一段时间，其产量同样没有显著爬坡。与此同时，SK Hynix 与 Micron 凭借不采用 EUV 的 1Z 代，在成本、性能与功耗上实现了追赶。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a38be212-9220-477d-82a4-3d78c14add6b_1024x526.jpeg)

更进一步，到了 1 Alpha 代，Micron 继续只推进 DUV，而 SK Hynix 已开始导入 EUV。因此，Micron 的 1 Alpha 已在爬坡，而 SK Hynix 与三星的产量爬坡都相当乏力。SemiAnalysis 估计，Micron 目前在 DRAM 上拥有成本优势，因为他们能够把全部产量切换到 1 Alpha 代，并在其整个产品线上实现最佳密度与成本。

三星与 SK Hynix [的第一代 DDR5 仍在出货非 EUV 的 1Y](https://www.techinsights.com/blog/industry-leading-ddr5-technology)，而 Micron 正在碾压竞争对手，其第一代 DDR5 已出货 1Z 代产品。此外，Micron 还在 1 Alpha 工艺节点上快速跟进第二代 DDR5。需要说明的是，EUV 并非唯一的元凶，但它是最大的技术差异之一。

对三星而言，事情在这里急转直下。他们的 1Z 没能爬坡，1 Alpha 也没能爬坡，而现在[有报道](https://www.fnnews.com/ampNews/202204121844028873)称[他们已取消下一代 1 Beta 工艺节点的开发！](https://n.news.naver.com/article/014/0004819002)另有报道称，三星正在进行又一次自上而下的孤注一掷，[直接冲向 1 Gamma 节点](https://laoyaoba.com/html/share/news?source=h5&news_id=814707)。关于取消开发的报道可信度很高，因为它来自三星一位心怀不满的工程师，他甚至就此主题发布了一篇博客！

该工程师已被证实属于三星 DRAM 的工艺开发团队。他写了一封信给三星电子的两位首脑——会长李在镕（Lee Jae-yong）与 CEO Kye Hyun Kyung，陈述了失败与问题。博客随后被删除，但[韩国媒体留存了](http://news.tvchosun.com/mobile/svc/osmo_news_detail.html?contid=2022041390082)其中相当令人担忧的引述。

> 我听过不少关于「危机」的说法，但我认为此刻比以往任何时候都更加危险。在接连发生的事态之中，最高决策者似乎无法把握问题的根源。
>
> 三星 DRAM 工艺开发工程师（经 Google 翻译）

我们建议你去读一读原文，真正体会事态的严重性。一位任期 4 年、对工作怀有深厚热情的工程师如此公然发声抗议，是一个巨大的危险信号。考虑到韩国职场文化等级分明、层级森严，这一点加倍成立。过去一个月里，我们还看到若干三星 DRAM 工艺开发员工跳槽至 SK Hynix。这已超出正常的流失率。

文化问题在极深的程度上撼动了三星。尽管三星电子的许多板块仍是运转良好的执行机器，例如 Samsung Display、NAND、汽车与网络业务，但其最重要的业务正处于麻烦之中。这些文化问题的顶点是：三星失去了其在 DRAM 上的技术与成本优势，在先进制程竞赛中远远落后于 TSMC，失去了最大的代工客户，并在智能手机 SOC 设计上输给了高通与 MediaTek。

[分享](https://newsletter.semianalysis.com/p/samsung-electronics-cultural-issues?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

*SemiAnalysis 的客户与员工可能持有本文所提及公司的仓位*。
