---
title: "Nvidia 收购 Illumina？医疗健康的 AI 代工厂——生命的硬件"
title_en: "Nvidia Buys Illumina? The AI Foundry for Healthcare – The Hardware of Life"
subtitle: "战胜反摩尔定律：以一场潜在收购让医疗健康重回摩尔定律轨道"
date: 2023-09-27
source: https://newsletter.semianalysis.com/p/nvidia-buys-illumina-the-ai-foundry
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball", "William March", "Deeran Patel, MD"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Nvidia 收购 Illumina？医疗健康的 AI 代工厂——生命的硬件

> 原文：[Nvidia Buys Illumina? The AI Foundry for Healthcare – The Hardware of Life](https://newsletter.semianalysis.com/p/nvidia-buys-illumina-the-ai-foundry) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**战胜反摩尔定律：以一场潜在收购让医疗健康重回摩尔定律轨道**

摩尔定律大家都熟悉——微芯片上的晶体管数量每两年翻一番这一观察。但我们怀疑，熟悉摩尔定律的「表亲」反摩尔定律（Eroom's Law）的读者并不多。

没错。Eroom's Law 字面上就是把 Moore 倒过来拼。

不。这不是我们编的，不过真希望是我们编的！

具有讽刺意味的是，[反摩尔定律](https://www.nature.com/articles/d41573-020-00059-3.epdf?no_publisher_access=1&r3_referer=nature)描述的是：开发一款新药的成本大约每九年翻一番。

![](https://substack-post-media.s3.amazonaws.com/public/images/d441a7fa-a5e1-4d41-8247-ddb3af4acc1e_1864x1796.png)
*来源：《诊断制药研发效率的下滑》—— 反摩尔定律 vs 摩尔定律：在摩尔定律下，单位美元随时间产出的晶体管越来越多；在反摩尔定律下，每次药物发现随时间花费的美元越来越多。*

摩尔定律与反摩尔定律考察的都是半导体与药物研发领域的三个共同要素：时间、金钱和产出单位。

半导体是现代一切技术进步的基石，得益于摩尔定律，其单位成本与能力呈指数级改善。而药物发现作为医疗健康中支出最大的领域之一，单位成本却在急剧膨胀，需要数十亿美元才能把一项新创新推向市场。

尽管许多人争论摩尔定律在半导体行业是否已死，反摩尔定律的精神显然在医疗健康领域活得很好。

要超越反摩尔定律，让医疗健康的进步重新跟上人类其他技术进步的步伐，人类需要把云、加速计算和 AI 的现有成果，释放在「生命的硬件」之上。

**医疗健康是经济中最大的领域，仅美国就超过 4 万亿美元。然而它至今仍基本被大型科技公司和摩尔定律带来的巨大技术进步所忽视。**

## **反摩尔定律在医疗健康各细分领域的体现**

尽管制药行业已采取多项措施改善药物发现流程、提高新治疗方式的成功率，但制药行业整体研发成本与营收之比仍在持续攀升。即便医疗健康成本（以及制药公司营收）的增速远高于消费者价格指数（CPI）均值，这一趋势依然延续。这在很大程度上是因为，由于我们对生物学以及各系统间相互作用的理解不足，很难预测一款药物能否通过极其漫长而昂贵的临床试验。

![](https://substack-post-media.s3.amazonaws.com/public/images/d950242c-741f-40b1-8828-b2de3cc646e4_1843x1177.png)
*来源：美国国会预算办公室（CBO）——制药行业的研究与开发*

近年来投资回报递减的一个重要原因是，药物发现与研究流程尚未充分利用技术进步的潜力，尤其是云计算和人工智能的应用。

反摩尔定律的一个实证体现是，医疗健康成果的投资回报递减：1960 至 2019 年间，美国人均医疗健康支出占 GDP 的比重从 [约 5% 升至约 20%](https://www.cms.gov/data-research/statistics-trends-and-reports/national-health-expenditure-data/historical)，但人均预期寿命仅从 70 岁提高到 79 岁。进入 21 世纪，成本呈指数级恶化，因而在发达国家越来越难以负担。

![](https://substack-post-media.s3.amazonaws.com/public/images/457a458b-760b-41ae-b4a2-48859b5a6a1f_2480x1354.png)
*来源：美国医保与医助服务中心（CMS）全国医疗健康支出*

医疗健康许多领域的改善程度都远低于其潜力。从病历到无处不在的 Apple Watch 和 Peloton 动感单车，数据量与利用这些数据的科学兴趣都在指数级增长，但拿得出手的成果寥寥。我们依然缺少关键的分析基础设施来处理这些数据、从噪声中甄别信号，从而对患者病史、生物信号（心率、血氧和血糖水平）以及环境对患者预后的影响提供实时洞察。

在病历领域，尽管医院对电子健康记录（EHR）的采用率[从 2008 年的 10% 升至 2014 年的 95%](https://www.healthit.gov/sites/default/files/page/2023-02/2022_ONC_Report_to_Congress.pdf)，但在从数据中提取洞察方面进展甚微——无论针对单个患者还是大规模患者群体皆然。电子健康记录中保存着结构化数据，如患者人口学信息、用药、诊断数据（检验、影像、微生物、病理等）和疫苗接种记录。

然而，EHR 中产生的大部分数据是[非结构化](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4287068/)数据，如医生笔记、保险公司数据和账单数据。据估计，到 2020 年已达到 [2,314 exabytes](https://catalyst.nejm.org/doi/full/10.1056/CAT.18.0290) 的海量医疗健康数据，大部分都未被利用。

![](https://substack-post-media.s3.amazonaws.com/public/images/b9e872dd-0346-4c4c-af18-77e65a21e7b9_2182x1084.png)
*来源：美国劳工统计局*

举例来说，急诊科医生最多只有 5-10 分钟，最危急的病例中甚至只有几秒钟，去研读这些以医生笔记和扫描件形式存在、可能长达数百页的非结构化数据。由于许多医院使用互不相同的电子健康记录（EHR）系统，无法便捷调取患者在其他医疗机构就诊的 EHR，也无法对海量 EHR 记录开展数据分析，这使医疗健康行业无法获得足以改变格局的数据，来推动药物开发和更好的临床治疗经验积累。

利用大语言模型（LLM）摄取电子健康记录中的海量非结构化数据，可以让这些信息用于诊断或治疗，尤其是在急诊和重症监护中，并可在研究场景中提供丰富洞察。LLM 也非常适合数据分类和简化数据可迁移性问题，有望改变当前患者的 EHR 分散在不同医院或诊所、各自孤岛林立的局面。

我们的朋友 Gaurav 在 [GettingClinical](https://gettingclinical.substack.com/) 上[更详细地阐述了这一想法](https://gettingclinical.substack.com/p/large-language-models-for-healthcare-c28)。在后续报告中，我们也将深入探讨 LLM 在医疗健康中的应用。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

## **剧本翻转：从反摩尔定律回到摩尔定律**

虽然医疗健康成本不断上涨，但医疗健康行业内部确实有一些领域展现了优于摩尔定律的缩放速度。第一个人类基因组于 2003 年完成测序，[耗资 30 亿美元、历时 13 年](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2011-12-8-125#:~:text=In%20fact%2C%20the%20cost%20of,and%2013%20years%20to%20complete.)、由多家机构共同完成。到 2008 年，全基因组测序成本降至 200 万美元；2014 年降至 1,000 美元；如今报价为 200-600 美元。

![](https://substack-post-media.s3.amazonaws.com/public/images/69c7750d-b57e-4ee5-8a01-a4517d7b1abb_2492x1362.png)
*来源：美国国立卫生研究院（NIH）——DNA 测序成本：数据*

单次测序成本的大幅下降带动基因组学数据指数级增长。这一改善并未放缓：基因组测序工具的领导厂商 Illumina 于 2022 年 9 月发布了 [NovaSeq X](https://www.genengnews.com/news/illumina-reveals-new-high-throughput-instrument-novaseq-x/#:~:text=Although%20the%20instruments%20have%20the,ultra%2Dhigh%20density%20flow%20cells.) 测序仪，再度压低上游测序成本。该仪器单次测序成本约 200 美元，较上一代工具下降 80%。尽管成本下降，测序时间仍是临床采纳的关键瓶颈——最新仪器完成测序仍需 [21-48 小时](https://www.illumina.com/systems/sequencing-platforms/novaseq-x-plus/specifications.html)的运行时间。

从 [2018 年（约 100 Petabytes）](https://s24.q4cdn.com/526396163/files/doc_presentations/ILMN-at-Barclays-13-March-2019.pdf)到 [2021 年（280 PB）](https://www.illumina.com/company/news-center/press-releases/2022/4ea79eed-e630-4f50-b6b3-c7f11a8780cc.html#:~:text=(Nasdaq%3A%20ILMN)%20will%20host,Time%20in%20San%20Diego%2C%20CA.)，基因测序机龙头 Illumina 所售仪器产生的数据的年复合增长率（CAGR）达 41%，即每两年翻一番。而且这一趋势还在加速。

![](https://substack-post-media.s3.amazonaws.com/public/images/4f7c2b0a-0674-452d-be51-93336f6526f5_2019x1107.png)
*来源：Illumina 公司概览（2022 年 12 月）、Illumina 2019 年巴克莱医疗健康会议演示材料*

基因组学项目产生的数据量极为庞大，据估计到 2025 年每年将需要多达 [40 Exabytes](https://www.genome.gov/about-genomics/fact-sheets/Genomic-Data-Science) 的[存储容量](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4494865/)——比 2025 年预计的 YouTube 年存储需求高出一个数量级，是存储[人类历史上说过的每一句话](https://blogs.nvidia.com/blog/2023/02/24/how-ai-is-transforming-genomics/)所需数据量的 8 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/ba36d525-b05d-4c47-9244-2bf90ef4f993_2227x739.png)
*来源：《大数据：是天文级，还是基因组级？》*

如果我们将数据视为新的石油，并考虑到大语言模型颠覆众多行业的潜力，那么基因组学将成为启动这一转型的最关键领域之一。而在基因组学领域，超过 90% 的已生成数据产自 Illumina 测序仪。

基因组学数据的激增有望解锁疾病诊断、个性化医疗、筛查与预防、疑难杂症的治愈、癌症治疗以及重症监护等场景的应用。需要指出的是，基因组数据目前与药物发现和反摩尔定律还没有直接关系，但它是一个影响因素，而且基因组学已经借助 [DECL（DNA 编码化学库）](https://en.wikipedia.org/wiki/DNA-encoded_chemical_library)等进展开始扭转曲线。此外，上市时间是药物开发中最大的成本项，基因组学的进展将帮助加速成本改善。

![](https://substack-post-media.s3.amazonaws.com/public/images/e276e4ee-5f8f-445e-8983-66bfcd5ef91a_1954x979.png)
*来源：Nvidia 2022 年投资者日*

正如 AI 需要摩尔定律把计算成本压到足够低，才先有 ImageNet、后有语言模型；如今，人类基因组测序的高单位成本已不再是制约进展的门槛，不再是过去的那个障碍。今天，[人类基因组测序总成本中不到 10%](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2011-12-8-125)与 DNA 测序这一实际动作相关，[超过 90%](https://genomebiology.biomedcentral.com/articles/10.1186/gb-2011-12-8-125)的成本来自样本采集、数据管理、数据缩减和二级分析。

![](https://substack-post-media.s3.amazonaws.com/public/images/a3c12385-79b9-4083-9d2c-ad909f0bb1ee_1356x858.png)
*来源：《测序的真实成本：比你想象的更高！》*

缺失的拼图在于进一步发展数据分析基础设施，并驾驭将各类研究成果推向大规模临床应用所需的加速计算能力。缺乏易用的平台和工具，是采纳率如此之低的主要原因之一。

例如，肿瘤学是一个高达 780 亿美元的基因组学市场机会，但基因组学在该领域的渗透率仅约 2%。

![](https://substack-post-media.s3.amazonaws.com/public/images/bfe379ce-e322-41a7-ada5-4cca3ed94581_2164x1178.png)
*来源：NHS、NSF、NIH、联合国、世界卫生组织（WHO）、Illumina*

全基因组测序的进一步普及打开了潘多拉魔盒。出于诊断或研究目的接受测序的患者越多，研究者就越能将基因突变与疾病关联起来并开发疗法，编出更全面的检测与治疗词典。测序流程在临床或诊断场景中对患者越有用，基因组学的使用需求就会越旺。

然而，我们对基因组学了解越多、针对基因突变开发的疗法越多，我们要问的问题也越多。基因组学只提供一种类型的洞察。

## **更多关于其他「组学」的话题：潘多拉魔盒**

从人类基因组到代谢通路，科学家对人体正获得越来越深入的理解。我们对基因组学、蛋白质组学等以往彼此割裂的学科所收集的数据，正日益交织在一起。

![](https://substack-post-media.s3.amazonaws.com/public/images/1fd1aa3a-ca6b-4a23-b784-79b686b1b515_2500x2236.jpeg)
*来源：AI 驱动的治疗靶点发现*

蛋白质组学（proteomics），即研究蛋白质结构与功能的学科，是另一个值得关注的领域。蛋白质与体内其他分子结合时，其结构可能发生显著变化。这对确定疗法靶点或理解细胞对既往治疗的响应至关重要。在加速计算出现之前，蛋白质结构分析是一项极其复杂、费力且耗时的工作。

只需看看 DeepMind 的 AlphaFold 对该领域的突破性影响便可明白。[DeepMind 的工作](https://www.deepmind.com/research/highlighted-research/alphafold/timeline-of-a-breakthrough)将生物学中存在 50 年之久的蛋白质折叠问题解决到前所未有的精度——误差小于 0.1 纳米。这些进展不仅解决了多个老问题，还照亮了一系列新机会。例如，AlphaFold 的后继者正在帮助研究者更好地理解如何、以及在何处递送疗法以最大化临床效用。

[表观基因组学](https://www.genome.gov/about-genomics/fact-sheets/Epigenomics-Fact-Sheet)研究基因如何因附着在 DNA 上的化合物或蛋白质所导致的变化（而非 DNA 序列本身的改变）而产生不同的表达。一个被广泛研究的例子是 DNA 甲基化：甲基基团（-CH3）附着到胞嘧啶碱基上，使细胞识别这一标记并对该基因区别对待。这些变化可能由环境/外部因素引起，其本身也可能致病。

历史上，这些彼此割裂的学科（各种「组学」）都在各自的孤岛中被探索。

*后续报告将深入探讨上述简要提及的各领域以及未提及领域的进展，尤其是 AI 的使用与需求。*

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

随着医疗健康行业开始拥抱这些关键使能趋势并持续统一各个研究领域，它正站在范式转变的悬崖边。从基因组学、基因疗法、药物开发到电子医疗数据的爆发，近期众多领域的进展已超出了行业充分利用这些变革性创新的能力。行业非但没有看到突破的加速，反而撞上了墙。而推翻反摩尔定律的潜力是清晰存在的。

随着云计算、大规模并行加速计算以及各类机器学习/大语言模型的出现，人类终于拥有了为医疗健康每个细分领域拆除这些路障的工具。克服这些障碍将引发加速计算/数据分析需求的巨大爆发，并为能够成为这些应用之 AI 代工厂（AI foundry）的公司创造庞大的收入机会。

AI 代工厂可以撬动美国超过 4 万亿美元的医疗健康市场，与行业合作，把研发工作整合进一个标准化、易用的技术栈，提供易获取、可负担、跨云/本地部署皆可的分析能力，进而在整个生态中形成规模经济，推动医疗健康成本下降。

在深入探讨 Nvidia 收购 Illumina 的具体协同效应与机会之前，先对基因组学做一个简要概览。我们的朋友 [Asianometry](https://www.youtube.com/@Asianometry) 提供了关于下一代测序历史的[详细概述](https://www.youtube.com/watch?v=pEwkpQV691A)，解释了为什么说 [Illumina 是基因组学界的 ASML](https://www.youtube.com/watch?v=pEwkpQV691A)。

## **基因组学：把模拟样本变成数字 DNA**

基因组学研究的是生物体 DNA 序列（即其「基因组」）的全貌。DNA 是世界上密度最高的数据形式，让 [3D NAND](https://www.semianalysis.com/p/nand-flash-monopoly-broken-tokyo) 等现代半导体相形见绌、如同儿戏。构成人类 DNA 的 32 亿个碱基对含有约 1.5GB 数据，编码在一条紧密缠绕、塞进宽度不足 [0.0002 英寸](https://nigms.nih.gov/education/Inside-Life-Science/Pages/Genetics-by-the-Numbers.aspx)空间里的分子链上。

样本形态、大小、状态各异。以其原有形态，我们审读样本、从中提炼洞察的能力有限。血是红的，唾液是湿的，组织是软的。我们喜欢把基因样本视为「模拟样本」，把测序视为一种模数转换。基因组学支撑着从 AlphaFold 到基因疗法的大量研究应用。

![](https://substack-post-media.s3.amazonaws.com/public/images/15d332ec-bd41-4d23-a74a-9fccb766b7fd_1920x1081.jpeg)
*来源：美国国家人类基因组研究所*

在人类基因组的 32 亿个碱基对中，只有 2% 真正包含约 20,000 个基因——这些基因构成合成氨基酸、进而合成[对身体执行关键功能和细胞过程至关重要](https://medlineplus.gov/genetics/understanding/howgeneswork/protein/)的蛋白质的指令。其余 98% 的 DNA 序列被称为「非编码」DNA。

过去人们认为这些非编码 DNA 没有功能，但科学家如今相信，基因组中的这一大部分对基因是否被激活、如何被激活仍至关重要。对非编码 DNA 的研究也加速了表观基因组学等领域的工作——该学科研究的是不直接改变 DNA 序列的修饰如何仍能影响基因活性。

## 长话短说：短读长与长读长测序

DNA 测序有两种不同的方法：短读长（short-read）与长读长（long-read）。

顾名思义，短读长测序每次只考察基因组的一小段，把整个基因组打断成长度介于 50 到 300 个碱基对的众多片段。长读长测序则如其名所示，能以更少的歧义提供更完整的基因组图景，每个片段可扫描 5,000 到 30,000 个碱基对。

在两种模式之间做选择，取决于用户要达成的具体目标。短读长测序凭借更高的准确性、更低的错误率、更快的测序时间和更低的成本主导着市场。长读长测序则有助于研究基因组的复杂区域，尤其是包含重复碱基对序列的区域，使这些区域的比对更无歧义。

市场总体由专注短读长机型的 Illumina 主导。英国竞争与市场管理局（CMA）估计，Illumina 在全球测序市场占有 80-90% 的份额。

![](https://substack-post-media.s3.amazonaws.com/public/images/920400f4-c7a4-46e4-b94d-8c6e6fec2bd9_2690x656.png)
*来源：英国竞争与市场管理局（CMA）——Illumina 拟收购 Pacific Biosciences 案*

长读长测序机市场则略显分散，参与者包括 Pacific BioSciences（PacBio）和 Oxford Nanopore 等公司。短读长市场的新锐包括 Element Biosciences、Singular Genomics 和 Ultima Genomics，而行业巨头 Thermo Fisher 则通过其 Ion Torrent 平台参与竞争。

*后续报告将更深入地探讨短读长与长读长市场及其竞争格局。*

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

尽管各平台各有优劣，但底层流程和工作流遵循相同的路径。流程中的两个关键瓶颈，一是碱基识别（base calling）与比对（alignment）过程中数据的互操作性，二是变异识别（variant calling）。

## **瓶颈累积：碱基识别、比对与变异识别**

> 随着测序成本下降，计算支出在我们总成本中的占比将与日俱增。
>
> —— Al Maynard，Illumina 软件工程副总监

面对以超过摩尔定律速度下降的人类基因组测序成本，上面这句话展现了非凡的远见。这一点叠加需求的价格弹性，带来数据产量的激增——如今人类基因组测序只需 200 美元。然而，测序仪产出的只是原始数据，这些收益如今撞上了反摩尔定律。科学家要依靠大量计算流程来获得上下文化的洞察与分析，即所谓的二级分析或下游分析。二级分析的成本和时间远超测序本身，这正是 Nvidia 在反摩尔定律面前*扭转剧本*的未来机会。

![](https://substack-post-media.s3.amazonaws.com/public/images/fd597c47-2c05-4b5f-a69f-643d33e99e8e_1941x1014.png)
*来源：《重症监护环境下的超快纳米孔基因组测序》*

**碱基识别（base calling）**是测序数据的第一步，即通过解读样本 DNA 产生的荧光信号或电信号（取决于所用技术），确定 DNA 序列上的各个字母（A、T、G 或 C）。然而，处理这些信号存在显著的[误差源](https://academic.oup.com/bioinformatics/article/27/17/2330/223750)。碱基识别的准确性对二级分析中所有后续步骤的质量起着决定性作用。常言道：「垃圾进，垃圾出。」一个高效的碱基识别器必须校正信号误差与噪声，准确输出基因组中序列的字母。深度神经网络非常适合碱基识别，因为它可以经过训练逼近几乎任意函数，从而校正这些误差与噪声，但实现这一方法需要可观的算力。

**比对（alignment）**是将扫描得到的 DNA 片段重新组装、确定这些片段源自基因组何处的过程，本质上是把数十万块拼图碎片拼回原始基因组的完整图景。

在重建样本的完整基因组**序列**后，便进入测序流程的下一阶段——**变异识别（variant calling）**。在变异识别过程中，我们检测测序 DNA 与参考基因组之间的差异（即「变异」）。这些变异使我们能够识别具有潜在功能影响的突变。该过程需要大量内存和并行化，因为来自序列的读取、参考基因组和随后的差异要被同时处理。

## **Nvidia 与 PacBio：长读长领域全栈化的收益**

长读长测序机的重要制造商 PacBio 近期推出了集成 Nvidia GPU 的新仪器 Revio。以下是 PacBio 对[通过与 Nvidia 合作所实现的全部收益](https://www.pacb.com/blog/scaling-long-read-sequencing-throughput-and-accessibility-with-deep-learning-and-nvidia/)的阐述：

> 借助 Nvidia 的先进 GPU，我们的团队开始**将工作负载迁移到 GPU，首先迁移的是 GPU 抛光（polish）步骤——该步骤此前消耗了 Sequel IIe 系统超过 80% 的 CPU 时间。**……我们的团队得以将更多计算步骤迁移到 GPU，最终**交付了一套能在 2.5 小时内完成任务的 CCS（环化共识测序）实现，为我们利用新增 GPU 带来的机载算力做更多事情留出了充足余量**。

![](https://substack-post-media.s3.amazonaws.com/public/images/d601a7ff-8bda-44c1-8217-8414bdb7a319_1489x763.png)
*来源：《用深度学习和 Nvidia 扩展长读长测序的吞吐量与可及性》*

集成 Nvidia GPU 为 PacBio 扭转了剧本。与前几代仪器相比，Revio 在时间减少 20% 的情况下产出 12 倍的数据量（快 15 倍）。作为对照，前文提到的 Illumina 新仪器 [NovaSeq X](https://www.genengnews.com/news/illumina-reveals-new-high-throughput-instrument-novaseq-x/#:~:text=Although%20the%20instruments%20have%20the,ultra%2Dhigh%20density%20flow%20cells.) 依靠 CPU 将数据产量提升到前代的 2.5 倍（16Tb 对 6Tb），但耗时反而多 10%（48 小时对 44 小时）。

![](https://substack-post-media.s3.amazonaws.com/public/images/83b40f39-9e97-4b26-83cb-0d3586476a62_2077x874.png)
*来源：PacBio Revio 系统*

上游流程的耗材成本在过去 20 年里从 30 亿美元一路暴跌至 200 美元，未来再想出现如此幅度的下降几乎不可能；相反，实现临床采纳的瓶颈正在转向二级分析。

## **重症监护室走向全栈化**

在临床场景中，基因组学是什么样子？它如何挽救生命？

2020 年末，斯坦福大学医学院的研究者对重症监护中的患者开展了[超快速全基因组测序](https://www.nejm.org/doi/10.1056/NEJMc2112090)，在数小时内诊断罕见遗传病，创下了世界纪录。

这一进步的核心是本机算力与云端算力的结合。工作流实时采集仪器的原始信号并传输到云存储，随后数据被分发到多个云计算实例上，进行近实时的碱基识别与比对。研究者将碱基识别与比对时间从**仅用本机算力的 18.5 小时，通过并行化缩短至 2 小时**。该工作流使用了 16 个实例，每个实例配备 48 颗 CPU 和 4 块 Tesla V100，而不是 PromethION 48（Oxford Nanopore）机载的 4 块 Tesla V100。

在[一个案例](https://www.youtube.com/watch?v=maKeF2FYtxc)中，一名 13 岁男孩因快速进展的心衰症状被送到斯坦福医院。可能的病因有两种：要么是不可逆的遗传性心脏缺陷、需要心脏移植，要么是常常可自限且可治疗的炎症性疾病——心肌炎。团队利用这一超快测序流程将测序时间做到 11.25 小时，比之前的世界纪录快 8 小时，比标准诊疗检测快近 2 个月。他们确认了心脏遗传缺陷的存在，患者随后成功接受心脏移植，最终保住了性命。在这个案例中，及时诊断对恰当且确定性的治疗至关重要，凸显了这项技术众多潜在用途中的一例。

![](https://substack-post-media.s3.amazonaws.com/public/images/15bbeb12-474e-4ed8-a406-1f4d164713c5_1375x693.png)
*来源：《超快纳米孔基因组测序在重症医学中的潜力》*

经计算，该快速测序流程的每患者成本约为 4,900 至 7,300 美元，其中计算成本平均每患者 568 美元，而这部分成本几乎完全来自碱基识别、比对和变异识别。

请注意，这用的是 6 年前的 V100 以及溢价价格。如今同样算力资源的成本要低得多。作者强调，该检测的成本远低于重症监护室每天 10,000 美元的护理费用，因此该检测流程在大规模应用时很可能具备经济性，并最终有望纳入保险报销。

## **基因组测序的计算瓶颈：GPU 来救场**

Nvidia 正通过其基因组学工作流 Parabricks 来解决碱基识别、比对和变异识别中的计算瓶颈。Parabricks 隶属于 Clara——Nvidia 面向医疗健康生态的 AI 加速解决方案套件。

一项由 [AWS 与 Nvidia 完成的研究](https://pages.awscloud.com/rs/112-TZM-766/images/AWS_NVIDIA%20Genomics%20Solution%20Brief_FINAL.pdf)详细对比了基于 CPU 的分析与基于 GPU 的分析。在基于 CPU 的 Amazon EC2 上需要 1,800 分钟的计算，在 Nvidia T4 GPU 上只需 76 分钟，在 Nvidia A100 GPU 上仅需 25 分钟。在基于 GPU 的 EC2 上运行时，总成本降低 90-95%。

![](https://substack-post-media.s3.amazonaws.com/public/images/73a63dec-fe79-4b4c-af39-246ae067d5fa_2514x510.png)
*来源：AWS 毫不妥协的加速基因组学分析*

把上述数据放到 Illumina 将 CPU 集成进其二级分析解决方案 DRAGEN 的框架里审视，人们不禁要思考：他们是否正在错过更大的图景？

整个医疗健康领域，尤其是基因组学，正日益成为一场计算挑战。要战胜反摩尔定律，我们需要打破现有孤岛、构建开放生态的综合解决方案，汇聚生物学、化学、计算、工程与 AI 的一流专长。

## **Nvidia 的医疗健康攻势——前排就座**

Nvidia 以仪器与设备层加速计算赋能者的身份进军医疗健康市场，同时提供以 AI 定义的软件解决方案为特色的生物学与生物信息学平台，以及在最前沿 GPU 硬件上一流实现这些解决方案的通道。

> 所以这就是为什么**我真的不把 Nvidia 描述为一家芯片公司，我们是一家加速计算数据中心公司。**要在那个层级上竞争非常、非常困难。我们以及生态系统合作伙伴在软件上的投资，才是真正让我们与众不同的所在，让我们能够持续——**让我们能够以光速持续创新，因为我们是一家全栈公司。**
>
> —— *Nvidia 于摩根大通医疗健康会议，2023 年 1 月 12 日*

**Nvidia 应对这一庞大数据分析与算力需求的方式是多管齐下的：**

1. 将 GPU 集成到设备中

   1. 长读长测序仪。[Oxford Nanopore](https://nanoporetech.com/about-us/news/oxford-nanopore-and-nvidia-collaborate-partner-dgx-ai-compute-system-ultra-high) 和 [PacBio](https://www.pacb.com/revio/) 均将 Nvidia GPU 集成到各自的仪器中，缩短测序时间并实现更强的数据提取能力。
   2. [Nvidia IGX](https://nvidianews.nvidia.com/news/nvidia-launches-igx-edge-ai-computing-platform-for-safe-secure-autonomous-systems)。IGX 提供安全、低延迟的 AI 推理，以满足医疗流程（如机器人辅助手术和患者监护）中各类仪器与传感器对瞬时洞察的临床需求。
2. 超级计算机。[Cambridge-1](https://nvidianews.nvidia.com/news/nvidia-launches-uks-most-powerful-supercomputer-for-research-in-ai-and-healthcare) 超级计算机是英国最强大的计算机，由 Nvidia 专门打造，用于加速数字生物学。AstraZeneca 与 Nvidia 合作构建了能够利用海量化学结构数据集的基于 transformer 的神经网络架构。[Oxford Nanopore 利用 Cambridge-1 把算法改进的时间从数天缩短到数小时](https://www.nvidia.com/en-gb/industries/healthcare-life-sciences/cambridge-1/)。[GSK、英国 NHS、Peptone 和 Alchemab](https://www.nvidia.com/en-gb/industries/healthcare-life-sciences/cambridge-1/) 也借助这台超级计算机在医疗健康相关应用上取得了多项突破。
3. [Nvidia Clara](https://www.nvidia.com/en-us/clara/) 提供横跨医疗健康生态的 AI 加速解决方案套件。

   1. 面向基因组学的 [Parabricks](https://www.nvidia.com/en-us/clara/genomics/)。Parabricks 于 2019 年被收购，为基因组测序流程中的二级分析提供一套 GPU 加速工具。它执行序列比对与组装等任务，帮助确定测序 DNA 中基因变异和突变的位置。这比使用 CPU 快得多、也便宜得多。
   2. 面向医学影像的 Nvidia [Holoscan](https://www.nvidia.com/en-us/clara/medical-devices/) 与 [MONAI](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/clara/containers/monai-toolkit)

      1. Holoscan 与 MONAI 均为面向医疗器械和医学影像的 AI 计算平台，融合了低延迟传感器与网络连接的硬件系统、面向推理优化的 AI 库，以及对来自设备或云端的数据进行实时处理的软件定义架构。
4. Nvidia 的 [BioNeMo](https://www.nvidia.com/en-us/gpu-cloud/bionemo/) LLM 于 2023 年 3 月发布，将大语言模型（LLM）应用于化学、蛋白质、RNA 和 DNA 研究，让开发者能够高效训练和部署拥有数十亿参数的生物学 LLM，产出的洞察可供研究者关联到生物学特性或功能、乃至人体健康状态。BioNeMo 提供的产品[包括](https://nvidianews.nvidia.com/news/nvidia-unveils-large-language-models-and-generative-ai-services-to-advance-life-sciences-r-d)：

   1. *AlphaFold2：一款深度学习模型，仅凭氨基酸序列即可将确定蛋白质结构的时间从数年缩短到几分钟甚至几秒，由 DeepMind 开发，已有超过一百万研究者使用。*
   2. *DiffDock：帮助研究者理解药物分子如何与靶蛋白结合，该模型以高精度和高计算效率预测小分子的三维取向与对接相互作用。*
   3. *ESMFold：该蛋白质结构预测模型使用 Meta AI 的 ESM2 蛋白质语言模型，可仅凭单条氨基酸序列估算蛋白质的三维结构，无需多条相似序列的样本。*
   4. *ESM2：该蛋白质语言模型用于推断蛋白质的机器表示，可用于蛋白质结构预测、性质预测和分子对接等下游任务。*
   5. *MoFlow：用于分子优化和小分子生成，这一生成式化学模型可从零开始创造分子，为潜在疗法提出多样化的化学结构。*
   6. *ProtGPT-2：该语言模型可生成全新的蛋白质序列，帮助研究者设计具有独特结构、性质与功能的蛋白质。*

这些平台为各类应用奠定了良好基础，但当其他生态掌控着其平台上处理的所有数据时，Nvidia 目前的布局中仍有许多缺口，尚不足以实现其成为医疗健康全栈供应商的雄心。

## **Illumina = 缺失的拼图**

> ***所以，基因组学是一种正在为医疗健康以及研究与药物发现创造巨大价值的方式（modality）。它是医疗健康领域最大的数据生成器，而且增长迅速。***我们正见证成本的持续下降，使大规模基因组学项目得以落地。然而，我们需要对这样一个事实保持敏感：很多时候，**你宣传的测序成本只是测序本身的成本，并不包含下游分析——而那才是我们照护患者、为药物发现提供洞察最终需要的东西***……***随着更多测序平台和方式进入市场，我们将把这 40 exabytes 的基因组数据推向世界。***
>
> —— *Nvidia 于摩根大通医疗健康会议，2023 年 1 月 12 日*

![](https://substack-post-media.s3.amazonaws.com/public/images/8cb2c200-501c-4709-a9d7-a498a24963ab_2142x1480.png)

Nvidia 收购 Illumina 将补齐其医疗健康攻势的拼图，把上游基因组学数据与下游 AI 驱动的分析连接起来，为医疗健康创造新的行业标准。

我们认为，收购 Illumina 可以回答以下关键问题：

1. 当 90% 的测序数据仅靠 CPU 完成采集、从而限制了新数据的生产时，如何在基因组学领域开发全栈解决方案？
2. 当 Illumina 工具的数据默认流向 Amazon 的云——一个攫取超高利润率却只提供非常薄弱的分析工具的准垄断者——时，如何在基因组学领域开发全栈解决方案？
3. 当数据和分析工具各自困于孤岛时，如何创造让医疗健康大众化的直觉式工作流？
4. 在一个天生不擅长构建软件的行业里，谁来统一并标准化这些分散的数据源和工作流？
5. 不构建能够横跨医疗健康生态的 AI 驱动解决方案，如何把剧本从反摩尔定律翻回摩尔定律？
6. 若不为人类最大、最重要的数据集——生命的硬件——提供加速计算，何以自称加速计算的供应者？

我们已经讨论过，将 GPU 集成到测序仪中将为 Illumina 带来测序时间和数据产量上的显著改善——在这方面它落后于竞争对手。当然，把 GPU 集成到其工具中只是唾手可得的成果，仅触及 Illumina 之所以构成一项变革性收购的表面——这场收购不仅改变 Illumina 和 Nvidia，也改变全人类。

收购 Illumina 的真正价值在于，它是补全 Nvidia 全栈解决方案拼图的缺失一块。以下为订阅者内容：**让我们深入真正的原因，讨论 Amazon Web Services Health Omics、云锁定、多云战略、对中立军火商的需求、Nvidia DGX Cloud、Nvidia 的软件即服务商业模式，以及成为世界 AI 代工厂的竞争。**

此外，**我们还将在下文分享一些治理与资本市场相关的原因，它们表明 Nvidia 与 Illumina 可能正在为此次收购尝试做准备。**

[团体订阅立减 20%](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
