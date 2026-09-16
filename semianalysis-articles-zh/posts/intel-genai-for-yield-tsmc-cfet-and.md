---
title: "英特尔用 GenAI 提升良率、台积电 CFET 与 3D 堆叠、AMD 3D 器件建模、应用材料（Applied Materials）材料创新、SK 海力士 HBM4、美光 3D DRAM 与 FeRAM、混合键合 vs TCB——IEDM 2023"
title_en: "Intel GenAI For Yield, TSMC CFET & 3D Stacking, AMD 3D Device Modeling, Applied Materials Material Innovation, SK Hynix HBM4, Micron 3D DRAM & FeRAM, Hybrid Bonding vs TCB - IEDM 2023"
subtitle: "中国长鑫存储（CXMT）违反出口管制、三星 1000 层垂直 NAND（VNAND）、铠侠最高密度的 CMOS 键合到阵列（CBA）NAND、美光密度与性能兼具竞争力的非易失性 FeRAM"
date: 2024-01-03
source: https://newsletter.semianalysis.com/p/intel-genai-for-yield-tsmc-cfet-and
crawled: 2026-09-15
authors: ["Dylan Patel", "Jeff Koch", "Myron Xie", "Daniel Nishball", "Anand Chamarthy"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 英特尔用 GenAI 提升良率、台积电 CFET 与 3D 堆叠、AMD 3D 器件建模、应用材料（Applied Materials）材料创新、SK 海力士 HBM4、美光 3D DRAM 与 FeRAM、混合键合 vs TCB——IEDM 2023

> 原文：[Intel GenAI For Yield, TSMC CFET & 3D Stacking, AMD 3D Device Modeling, Applied Materials Material Innovation, SK Hynix HBM4, Micron 3D DRAM & FeRAM, Hybrid Bonding vs TCB - IEDM 2023](https://newsletter.semianalysis.com/p/intel-genai-for-yield-tsmc-cfet-and) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**中国长鑫存储（CXMT）违反出口管制、三星 1000 层垂直 NAND（VNAND）、铠侠最高密度的 CMOS 键合到阵列（CBA）NAND、美光密度与性能兼具竞争力的非易失性 FeRAM**

戈登·摩尔的精神仍在延续——整个行业仍在追逐更小、更密、更便宜、更快的半导体器件。了解这些进展的首要舞台是国际电子器件会议（IEDM），今天我们想为读者盘点本届 IEDM 上与半导体器件微缩未来相关的各项进展。[去年错过我们总结](https://www.semianalysis.com/p/iedm2022p1)的朋友可以补课，我们当时涵盖了许多重要话题。

今年 IEDM 上我们听到最多的主题是什么？

我们将覆盖几个 AI 不只是热词的话题（尽管它经常只是热词），包括 Intel 用扩散模型改进工艺良率的创新工作。

主要议题将是对台积电（TSMC）、Intel、三星（Samsung）在 2D 材料、CFET 和背面供电方面面向 2nm 以下先进逻辑进展的综述。应用材料（Applied Materials）展示了其用于 2nm 及以下金属互连的新工具套件，可能带动份额提升。

另一个最令人兴奋的领域是存储。美光（Micron）发表了一种非易失性 FeRAM，密度超过全世界最密的 DRAM，性能差距在一个数量级以内。中国领先的 DRAM 厂商长鑫存储（CXMT）则公然炫耀其违反多项出口管制的行为。

SK 海力士（SK Hynix）展示了 HBM4 在混合键合、倒装芯片 MR-MUF 与 TCB 之间的方案抉择；三星展示了通过多种晶圆堆叠形式通往 1000 层以上 NAND 的道路；铠侠（Kioxia）则发表了全球密度最高的大规模量产级 NAND 及其 CBA 方法。

我们还会介绍 Intel 的 DrGAN、IBM 的「EUV 的未来」（[印证了我们上个月报告中关于 High-NA 因剂量问题在中期缺乏竞争力的部分判断](https://www.semianalysis.com/p/asml-dilemma-high-na-euv-is-worse)），以及 SemiAnalysis 即将开始在技术会议上颁发的搞笑奖项。

## **Intel 用生成式 AI 提升工艺良率**

Intel 展示了用深度生成模型预测器件偏差的早期工作。每一代芯片，复杂度的增长都远超晶体管数量的增长，Cadence 仿真/模拟机柜的数量也在持续爆炸式增长。Nvidia 正试图引入 GPU 来改进这一流程。

现有 EDA 享有一个良性循环：更强的算力带来更好的建模，更好的建模又能生产出更强的算力。某种意义上，这与生成式 AI 的扩展定律（scaling law）如出一辙，只是目前温和得多。用 AI 设计更好的 AI 加速器芯片正在快速发生，Nvidia 和 Google 远超同侪。[Nvidia 的「光速行动」之所以可能，很大程度上正得益于此](https://www.semianalysis.com/p/nvidias-plans-to-crush-competition)。

把生成式 AI 引入工艺和器件建模是顺理成章的第一步，因为这是一项数据极度密集的任务，且芯片厂商手头就有大规模、高质量（相对其他应用而言）的数据集。工艺良率提升和周期缩短的收益易于量化，并能直接换算成营收。

虽然仍处于早期阶段，Intel 展示了为此部署 GenAI 模型的可喜成果。初始测试用了两类不同模型：生成式对抗网络（GAN）和扩散模型。

![](https://substack-post-media.s3.amazonaws.com/public/images/c33395b8-2216-46dc-99b4-cf6db106437f_1151x386.png)
*GAN 模型架构：生成器神经网络通过「骗过」判别器网络来学习合成数据*

GAN 是一种常用架构，广泛应用于图像、文本和音频生成器，用于生成高度逼真的合成样本。它由两个深度神经网络组成：生成器和判别器。生成器从随机噪声中生成假样本。这些假样本与真样本一起输入判别器，由判别器尝试分辨真假。本质上，生成器在不断尝试骗过判别器，这正是「生成式对抗网络」中「对抗」的由来。

经过训练，生成器输出样本的质量会逼近真样本，甚至难以分辨。然而 GAN 模型容易出现模式崩溃（mode collapse）：其输出无法复现输入分布函数的完整空间；简单说，就是产出结果会趋于雷同。这对图像生成等许多流行的消费应用不是问题，但对芯片设计和工艺建模并不可行。

关键区别在于：在这个建模场景中，工艺良率恰恰由分布的长尾决定——无法复现长尾，就意味着模型无法正确预测良率。

![](https://substack-post-media.s3.amazonaws.com/public/images/e9e7d5f3-bf08-4aa9-8a3b-f8925bf9a22a_561x572.png)
*GAN 无法复现真实数据的分布，因此不能用于预测工艺良率*

扩散网络则更适合这项任务。训练时使用加了噪声的真实样本，模型学习为它们去噪。关键在于，扩散网络在此应用中能够复现样本数据分布的长尾，从而提供准确的工艺良率预测。

![](https://substack-post-media.s3.amazonaws.com/public/images/8d468f47-616f-4573-9a3b-9bd8704a4a97_1568x584.png)
*用于神经网络训练的扩散模型*

在 Intel 的研究中，设计阶段用于器件仿真的 SPICE 参数被作为深度学习模型的输入。模型的输出是对器件制造出来后电学特性的预测，即 ETEST 指标。结果表明，该模型能够正确预测 ETEST 指标的分布。电路良率正是由这个分布的尾部决定的。因此，只要正确预测了 ETEST 指标的分布，模型就正确预测了良率。

这里的潜力显而易见：在设计阶段更好地优化芯片良率意味着更低的成本。更少的光罩改版、更短的开发周期、最终更高的良率，对于能把此类模型嵌入自家 PDK/设计流程的代工厂和设计团队来说，都将是强大的差异化优势。

![](https://substack-post-media.s3.amazonaws.com/public/images/72283712-ecd8-462f-9719-d338afcb5560_919x433.png)
*扩散模型紧密复现真实数据，并支持外推*

目前这些工作还处于研究阶段，但我们预计所有主要代工厂和设计公司都会致力于将类似技术产业化。这类底层数据被严加看管，初创公司、甚至无厂设计公司都很难拿到全套数据。从这个意义上说，作为 IDM 的 Intel 占据优势。如果能拿到数据，这是创业者开公司的绝佳切入点。我们自己肯定会在这一领域做天使/种子投资。

## **逻辑微缩——2D 材料**

多年来，逻辑微缩一直是这个行业的心脏。尽管近年来微缩的步伐有所放缓，但它仍是半导体经济性持续改善的关键驱动力之一。IEDM 历来是芯片厂商展示其工艺路线图进展的舞台。我们这就直接切入，如果你需要先从更高的层面补课，可以阅读我们之前的[《晶体管的未来》](https://www.semianalysis.com/p/the-future-of-the-transistor)。

当前的开发工作集中在两个方向：x、y 方向的传统水平微缩，以及 z 方向的 3D 堆叠。

![](https://substack-post-media.s3.amazonaws.com/public/images/6d115c09-bf55-47d8-8df1-4f3bd486178c_1200x678.jpeg)
*未来十年的水平与垂直微缩方案*

在水平方向上，就在 FinFET 后劲不足之际，环栅晶体管（GAA）将让微缩在「2nm」级节点上得以延续。这些 2nm 级节点将于 2025 年在 Intel 和台积电进入大批量生产。三星的 3nm 同样采用环栅晶体管，但尽管宣称已实现大批量生产，他们至今没有出货过任何功能完整的芯片，连自家智能手机里也没有。

许多新进展聚焦于进一步微缩 GAA 架构，因为现有材料在本十年末将难以为继。这将需要转向特殊的「2D」材料——先是过渡金属二硫属化物（TMD）单分子层，之后可能是碳纳米管。

在垂直方向上，第一批堆叠晶体管架构正在开花结果。我们会在介绍台积电、Intel 和三星的最新进展时逐一展开这些想法。

2D 沟道材料预计将成为 GAA 架构的下一个演进台阶。初期，GAA 工艺将沿用与传统 FinFET 相同的硅（Si）沟道。但随着尺寸缩小、Si 沟道的接触电阻和寄生电容上升，继续微缩将需要电气性能更佳的新材料。这一过渡可能最早在 10A（1nm）节点就势在必行，时间大约在 2030 年前后。

TMD 单分子层，俗称「2D 材料」，厚度只有几个原子层，其具备所需特性早已为人所知；随着开发走向 2D 材料制造工艺的产业化，各芯片厂商似乎已在 TMD 上收敛。答案不是常被视为圣杯的碳纳米管，而是 NMOS（N 型金属氧化物半导体）用 MoS2、PMOS（P 型金属氧化物）器件用 WSe2。

这些材料只有几个原子厚，制造难度自然极大，寻找规模化可靠生产方法的竞赛已经开始。去年，我们[详细讨论过「材料生长 vs 转移」之争](https://www.semianalysis.com/i/104268569/d-material-transfer)，但目前看来，由于[转移路线存在非常棘手的难题](https://www.semianalysis.com/i/104268569/direct-growth-vs-transfer)，各方正在向直接生长收敛。

台积电演示了以单层纳米片沟道制造的可工作纳米片晶体管（NSFET）。他们还展示了构建两层堆叠纳米片的能力，但没有提及在这些纳米片上做出任何可工作的晶体管。一个关键点是，2D 材料是通过化学气相沉积（CVD）直接生长的，而不是沿用此前额外的薄膜转移步骤。

生长是 2D 材料的*根本*难题。目前尚无任何方案能在不可忽略的表面积上可靠地生长 2D 材料。

台积电还展示了一种新颖的「C 形」接触方案——一种降低接触电阻的方法（接触电阻越低，器件性能越好）：C 形接触环绕沟道，提供了更大的接触面积，从而电阻更低。

台积电只详细介绍了一款 NMOS 器件，而 Intel 展示了采用 TMD 沟道的可工作 PMOS 和 NMOS 器件。此外，Intel 是在 300mm 晶圆中试线上制造的这些器件，而非仅停留在实验室规模。至少就已发表的研究而言，在通往 2D 材料的竞赛中，Intel 远遥领先台积电。但需要注意的是，这些只是简单的平面晶体管，没有采用 GAA 架构，间距也达不到几年后 14A+ 节点所需的水平。

令人意外的是，三星对 2D 材料几乎只字未提。三星代工业务总裁兼总经理 Choi 博士提到了 2D 沟道材料延续 GAA 微缩的可能性，但没有发表任何相关技术论文。尽管是 GAA 的「先行者」，他们似乎打算让别人去为 2D 蹚路。

奇怪的是，从 IEDM 的报告来看，Intel 和台积电的路线图已然明确，三星却似乎仍未想清楚三种不同背面供电方案中究竟要选哪一种。

![](https://substack-post-media.s3.amazonaws.com/public/images/f8d29125-ed0e-4ed3-8387-c345a7115337_767x296.png)
*三星代工工艺路线图*

无论进展如何，我们目前正处于水平微缩的长尾阶段：每前进一步，带来的收益都比上一步更少，开发时间却更长。3D 堆叠恰恰相反——仅第一代就有望实现 1.5-2 倍的密度提升。

传统上，芯片由单层 NMOS 加 PMOS 构成，必要的连接在其上方搭建。制造技术的进步，以及必须超越水平微缩寻找出路的现实，意味着在彼此之上堆叠多层晶体管正逐渐成为可能。

## **逻辑微缩——CFET**

第一步自然是把 1 个 NMOS + 1 个 PMOS 晶体管堆起来，原因在于两者相连即可构成反相器（非门）——数字电路的基本构件。更复杂的标准单元也将非常难以制造。台积电发表了一张漂亮的概念示意图，并附上展示实物、由透射电子显微镜（TEM）图像拼合的组图。

去年，这一领域的大部分工作来自大学实验室。今年，所有主要逻辑芯片玩家（连同 IMEC）都拿出了由内部研发组织主导的成果，这是迈向商业化的坚实一步。3D 堆叠有望在 10A 节点前后、即 2030 年左右导入。

总体来看，各家（四种路线）在架构决策和制造方案上似乎正在趋同。

![](https://substack-post-media.s3.amazonaws.com/public/images/f0e0a6d8-b8d4-4634-a620-b5d9e0e13ca1_1267x634.png)
**这份对比需要注意的是，Intel 的论文聚焦 CFET + 背面供电与接触的集成，而不只是微缩本身。2021 年，Intel 曾演示过栅极间距 55nm、栅长 19nm 的 CFET*

Intel 的集成方案尤为有趣、值得强调：它展示的不只是 CFET，还包括 NMOS 采用背面接触的背面供电、PMOS 采用 PowerVia 的背面供电。在 CFET 之下，供电问题变得极其棘手。

## **逻辑微缩——热极限与登纳德缩放定律**

未来值得关注的一个关键领域是热性能。我们看到不止一家芯片厂商发表了关于微缩使能技术（3D 晶体管堆叠、背面供电、先进封装等）的论文，声称热性能没有退化。AMD 的一篇论文则从客户视角非常明确地指出：热问题需要额外重视。

![](https://substack-post-media.s3.amazonaws.com/public/images/b47c70fa-2e63-41fc-a15e-7250511bb8eb_1789x792.png)

AMD 的仿真显示，使用背面供电时性能损失最高可达 5%，因为芯片必须降频以避免过热。罪魁祸首是晶圆减薄和键合工艺。虽然制造背面器件离不开这些工序，但其副作用是大幅降低了器件附近硅层的热导率，意味着器件无法像以前那样有效散热。

在需要整片晶圆减薄的场合，3D 封装也遇到了同样的问题：热点处降频导致最高 5% 的性能损失。

![](https://substack-post-media.s3.amazonaws.com/public/images/121aed7d-5b5f-40ce-b4ed-78ee26b7a5af_1810x490.png)
*传统 2D 与 3D 先进封装方案的仿真热性能对比*

注意，逻辑微缩可能会加剧这个问题，因为它对发热有复合效应。器件尺寸缩小时不仅电阻上升、发热增加，晶体管密度也在提高，因此单位面积产生的热量更高。[登纳德缩放定律](https://en.wikipedia.org/wiki/Dennard_scaling)早就失效，而且每一次微缩都在让问题愈发严重。CFET、3D 堆叠、背面供电等进一步微缩技术正在加剧这些问题。

这一结果有几个耐人寻味的推论。第一，芯片设计流程必须开始把这些当作「一等公民问题」对待，提供让设计师能够缓解这些问题的工具。第二，制造方法也应着手应对热挑战。据我们交流过的多位设计师反映，目前 Cadence 和 Synopsys 提供的 EDA 工具在这方面仍有欠缺。

## **逻辑微缩——3D 堆叠**

聚焦后一个议题——用先进封装实现的常规 3D 堆叠来对抗失控的热密度——的论文我们只看到一篇，而它可能正是 AMD 所揭示问题的完美解法。台积电展示了应对功率密度上升的两种方法，都试图提高晶圆-晶圆键合处的热导率，因为减薄后的硅在那里表现很差。

第一种是放置虚设铜热过孔——本质上是把热量从热点导走的微型「热管」。其热性能表现出色，但由于铜同样导电，即便不接入信号互连，这种做法仍对电气性能产生了负面影响。

第二种更有前景，是在键合晶圆之间使用高导热层。目前晶圆键合时中间是一层 SiO2 键合层。实验表明，用高热导率材料取而代之，可以在不产生电气副作用的情况下改善散热。

![](https://substack-post-media.s3.amazonaws.com/public/images/174db233-3b1e-4d61-b6a4-14064cacbdf7_585x232.png)
*仿真证明，采用高热导率材料的晶圆间键合层可以缓解热点*

好处显而易见，但这些高导热材料并不容易制备。会上展示了两种候选材料：AlN 和金刚石。台积电在实验室环境下演示了这两种材料，做到了亚微米厚度，热导率也足以实用。

虽然这一工艺似乎尚未产业化，但鉴于上述问题，它值得持续关注。我们认为很值得注意的是，这次会议上它没有获得更多关注——也许 ISSCC 或 VLSI 会议上会有更多人重视。

![](https://substack-post-media.s3.amazonaws.com/public/images/34ade217-9b0f-4b97-aa51-85051ae38691_281x324.png)
*Si 晶圆上实验室生长的金刚石，其热导率足以缓解热点*

从制造角度看，先替换背面供电中的纯熔融键合可能更合理，而混合键合中的键合层先不动，因为那里贸然更换可能引发键合问题。

## **逻辑微缩——互连/后道工序（BEOL）**

虽然器件微缩似乎占据了大部分注意力，但后道工序（BEOL）微缩同样重要，甚至更重要。如果信号和电力无法有效送达晶体管，晶体管密度的提升就毫无意义。最大的挑战之一，是[把理论上的晶体管密度提升转化为实际器件上布线后的密度提升](https://www.semianalysis.com/p/zen-4c-amds-response-to-hyperscale)。

微缩这些互连的一个关键挑战，是「导线」变细带来的电阻上升。事实上，这一挑战足以毁掉一整个制程节点：Intel 在 10nm 节点上的长期挣扎，很大程度上源于在最低几层金属层上试图从铜互连改用钴互连。在那种间距下，钴的电阻虽然低于传统的铜，但实施中问题丛生，最终这一选择被推翻。

后道微缩的设计决策一旦做错，可能给芯片厂商带来巨大的价值毁灭。因此，新的互连材料和制造方案值得关注。

Applied Materials 和 IMEC 都展示了各自的互连微缩方案。Applied Materials 于 2022 年首次推出氮化钛衬垫 + 钨填充，用于制造更细、更低电阻的互连。今年他们指出，该工艺已在一家主要逻辑芯片制造商处进入大批量生产。在此基础上，Applied Materials 发布了全钨互连方案，有望实现进一步的微缩。

这场报告显然是技术营销，但在场的台积电和 Intel 人士听得极为专注，提出的问题也非常到位。

值得注意的是，该方案可以在 Applied Materials 的 Endura 机台上原位（in-situ）完成，意味着在搭建互连的整个过程中晶圆完全不暴露于晶圆厂环境。氧气暴露会因互连氧化而导致性能退化，因此全程保持同一真空意味着好得多的结果：电阻比非原位工艺低 20% 以上。

Applied Materials 能以其他厂商做不到的方式把单一工艺模块的多种机台打包在一起，这让他们有机会在后道工序的最下面几层——即晶圆制造中成本最高的部分之一——从其他刻蚀、清洗和沉积设备供应商手中夺取份额。

## **存储微缩的未来——3D DRAM**

AI 时代无论是计算还是存储的内存需求都在爆炸式增长。一堵[限制着行业进步的巨大「内存墙」](https://www.semianalysis.com/i/97006309/the-memory-wall)横亘眼前。美光在一场主旨演讲中指出，数据增长正沿着与算力需求相似的轨迹加速，两条曲线的斜率都在变陡。

![](https://substack-post-media.s3.amazonaws.com/public/images/42c62375-8d8b-4f15-8e39-5b5c1f52fea9_1243x736.png)

与逻辑一样，存储也必须继续微缩，才能以经济的方式满足不断增长的数据需求。这需要在许多领域取得进展。用于控制存储阵列的逻辑电路需要相应微缩，FinFET 也已列上本十年末的路线图。

![](https://substack-post-media.s3.amazonaws.com/public/images/15d6818e-de11-4323-b534-dd1a9e4d6266_1294x730.png)

封装技术也将发挥作用，因为内存与计算更紧密的集成能带来更好的系统级性能（本文不深入展开封装；参见我们的[先进封装深度解析](https://www.semianalysis.com/p/advanced-packaging-part-1-pad-limited)，后续我们很快还会发布更多相关内容）。

![](https://substack-post-media.s3.amazonaws.com/public/images/cfdd44fd-aad4-40ba-a198-6abbfb522804_1303x727.png)

最后是存储阵列本身，其关键拐点是 3D DRAM 的导入。这里需要一些背景：传统上，DRAM 存储阵列由垂直电容器构成。与晶体管和逻辑一样，存储微缩大体上就是靠把器件做得越来越小。DRAM 电容器通常是又高又细的圆柱。缩小直径可以把它们以更高密度排布，但为了维持足够的电容，它们必须做得更高——换句话说，深宽比必须不断提高。

如今 DRAM 阵列的深宽比已经极高，制造难度非常大——这与逻辑芯片水平微缩逼近物理极限如出一辙。生产的主要难点在于：随着水平尺寸缩小、深宽比持续攀升，如何维持均匀性。

未来的某个时点，微缩将离不开 3D DRAM。概念很简单：如果电容器不能再做得更细/更高，那就把它们放倒，水平放置，然后大量堆叠。

这一转变的关键在于制造方法的差异。相对于现有的平面 DRAM，3D 可能减少 50% 的光刻用量，并大幅增加刻蚀和沉积设备。从 2D NAND 到 3D NAND 的转型中出现过类似的再平衡，这将对 DRAM 设备供应链产生强烈影响——等到 2025 年存储周期再次见顶时，这约是一个 300 亿美元（~$30B）的市场。

![](https://substack-post-media.s3.amazonaws.com/public/images/816396b3-02e4-42b6-969c-eadd1114f48a_1270x729.png)
*3D DRAM 的技术使能：生长 Si/SiGe 晶格、构建水平阵列、将存储阵列堆叠于 CMOS 之上*

那么，关键就在于这一转变何时发生。美光的主旨演讲者称之为「最典型的问题」（the quintessential question），给出的答案则是附带重重前提的「10 年之内」。很说明问题的是，各大存储厂商都没有在 IEDM 上发表严肃的 3D DRAM 论文，因为这是一场将改变市场份额格局的竞赛。今年只有旺宏（Macronix）发表了几篇相关论文，三星、SK 海力士、美光均缺席。美光分享的 IMEC 示例路线图给出的是 2030-2035 年之间一个模糊的时间段。换言之，短期内不必期待。

![](https://substack-post-media.s3.amazonaws.com/public/images/2a337326-3e6e-403a-afbb-3ba5913d63d6_1234x748.png)
*3D DRAM 导入暂定于 2030-2035 年*

## **存储微缩的未来——CXMT 3D DRAM 公然违反出口管制**

存储是实现「重新定义人类文明」的 AI 技术最重要的微缩方向之一。中国正在这些技术上投入巨资以求跃超世界其他地区，并且已开始将 LLM 用于宣传/干预选举等用途，也应用到了解放军内部。

就像在 Gina Raimondo 访华期间[华为公开发布 7nm 手机芯片麒麟 9000S](https://www.semianalysis.com/p/china-ai-and-semiconductors-rise) 一样，CXMT 也在旧金山 IEDM 上坦率地宣布了自己对美国出口管制的违反，[让我们颇为意外](https://twitter.com/dylan522p/status/1734340095753453960)。CXMT 发表了以 18nm 半间距制造的环栅垂直晶体管（Gate-All-Around Vertical Transistors）。

![](https://substack-post-media.s3.amazonaws.com/public/images/1aa9f8f5-9345-4197-820e-e6dd4fdc7fad_1063x810.png)
*CXMT 18nm 间距的垂直沟道晶体管，低于出口管制界限*

CXMT 同时触犯了美国出口管制的两个不同条款：美国设备不得出口给制造 18nm 半间距 DRAM 器件的公司；美国设备不得出口给制造环栅晶体管的公司。CXMT 在一个可工作的器件里同时踩了这两条红线。按照法律的写法，Applied Materials、Lam Research、KLA、Onto 等美国设备厂商从此不得再向 CXMT 制造这些器件的厂区出口设备。虽然上述器件是为了研究目的而生产、大规模量产还在后面，但法规并不会因此网开一面。CXMT 目前只有一座晶圆厂。

我们的晶圆厂设备模型和供应链信源显示，CXMT 明年在 DRAM 生产上的设备支出达 70 亿美元（$7 billion），其中 38 亿美元流向美国设备公司，Applied Materials 是最大贡献者，2024 年对 CXMT 的出货达 18 亿美元。这项支出高于美光的 DRAM 设备支出，原因是对 CXMT 政府支持的合资企业长鑫新桥最近的 50 亿美元（$5B）注资，资金来自中央和地方政府。

尽管 CXMT 在大批量生产级 DRAM 的工艺技术上仍落后几年，但在[大多数商用 DRAM 形态上只落后一年](https://www.trendforce.com/news/2023/12/01/news-cxmts-lpddr5-release-fuels-in-chinese-memory-market-spotlight-progress-of-global-memory-giants/)。我们还预计其面向 AI 的 HBM3E 将于 2025 年年中出货。

这些裁决的执行[可能继续失灵](https://www.semianalysis.com/p/china-ai-and-semiconductors-rise)，但按照现行法规的写法，CXMT 等于是在说：所有继续向其供货的美国设备公司都已违规。正因如此，他们公开承认这一点才令人意外。需要说明的是，他们能够突破限制本身并不令人震惊——在我们关于[美国制裁失败](https://www.semianalysis.com/p/china-ai-and-semiconductors-rise)的文章中，我们甚至专门点名过 CXMT。

## **存储微缩的未来——SK 海力士 HBM4 与 MR-MUF**

SK 海力士就 HBM 封装发表了多场报告，其中包括对其 MR-MUF 技术迄今最全面的介绍——我们此前的 [HBM 与 CoWoS 深度解析](https://www.semianalysis.com/i/135455698/veeco-phased-out-sk-hynixs-hbm-packaging-innovation)中已有覆盖。回顾一下：MR-MUF 代表「大规模回流焊–塑封底填」（Mass Reflow – Molded Underfill），SK 海力士此前使用 TC-NCF（热压–非导电膜），自 HBM2E 起改用 MR-MUF。

顾名思义，MR-MUF 采用传统的倒装芯片大规模回流焊工艺来堆叠裸片并形成连接。由于是批量工艺（整堆裸片的焊料回流一次完成），产能远高于[需要为堆叠的每一层单独键合的 TCB](https://www.semianalysis.com/p/advanced-packaging-part-3-intels)。

![](https://substack-post-media.s3.amazonaws.com/public/images/d0a79fc5-a00d-4a1b-b87c-bc94372d9312_1371x750.png)

这不仅是产能问题，MR-MUF 还能造出性能更高的 HBM。裸片之间采用环氧塑封料（EMC）作为缝隙填充材料，其热导率远高于 TC-NCF 中的非导电膜。这带来了更低结温，对于 GPU 这类高功率芯片而言，热管理至关重要，因此这对客户是重大利好。

![](https://substack-post-media.s3.amazonaws.com/public/images/0f479e94-00c5-4e48-8562-b24d82a6b56c_1391x764.png)

海力士深入剖析了 MR-MUF 的一些挑战——到目前为止，海力士是唯一攻克了这些挑战的供应商。他们与一家材料供应商联合工程开发，并签下了独家使用权。

![](https://substack-post-media.s3.amazonaws.com/public/images/0d645055-7e14-4d9e-a7e4-9a475c013651_1358x746.png)

第一个挑战是控制裸片翘曲：在堆叠层数高、裸片极薄的情况下尤甚。翘曲过大，形成的连接就会不良。[TCB 的优势正在于更善于对付翘曲](https://www.semianalysis.com/p/advanced-packaging-part-3-intels)，这也是 TCB 成为第一种 HBM 封装技术的原因。

这也解释了[为什么 Intel 与 OSAT 和代工厂封装生态的其他玩家不同，在封装中远为普遍地使用 TCB](https://www.semianalysis.com/p/advanced-packaging-part-3-intels)。细节披露不多（这属于他们的秘方），但海力士的做法是在晶圆背面沉积一层预应力膜来控制翘曲。Intel 的做法类似但又有不同，其[工艺流程同样有专利保护](https://patents.google.com/patent/US20150318258A1/en)。

![](https://substack-post-media.s3.amazonaws.com/public/images/3451d823-f20b-484b-91cd-0ce28b4a54aa_1380x763.png)

另一个挑战是点涂 EMC 填充裸片之间的缝隙并确保没有空洞。底填料的作用是为凸点提供结构支撑，但底填中的空洞会削弱这种支撑。HBM 的凸点更密、缝隙更窄，使底填点涂难度更高。

为此，海力士优化了塑封模具，并发现 EMC 的点涂图形同样关键。他们发现，芯片正面朝上的模具会产生无法避免的空洞，因此必须使用定制的正面朝下模具。此外，某些点涂图形的空洞率更低，例如图中展示最右侧的 Serpentine Imp.2 图形。还有一点：切勿把 EMC 填到堆叠体之间——那会阻碍气流，使结构中残留空气，进而产生空洞。

同样重要的是，SK 海力士还讨论了 HBM4 路线图。

本报告其余部分将涵盖：SK 海力士对 HBM4 混合键合与倒装/TCB 的取舍、美光密度超过 DRAM 且性能同量级的惊艳非易失 FeRAM、三星通往 1000 层以上 NAND 的道路、铠侠发表的全球密度最高的大规模量产级 NAND 及其 CBA 方法。

[领取团体订阅 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)

此外还将涵盖非存储类话题，例如 Intel DrGAN、IBM 的「EUV 的未来」——其印证了我们上个月报告中关于 High-NA 近期缺乏竞争力的部分判断——以及 SemiAnalysis 即将在技术会议上为演讲者颁发的搞笑奖项。
