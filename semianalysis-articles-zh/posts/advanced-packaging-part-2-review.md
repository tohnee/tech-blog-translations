---
title: "先进封装第二部 – 盘点 Intel、TSMC、Samsung、AMD、ASE、Sony、Micron、SKHynix、YMTC、Tesla 和 Nvidia 的方案与应用"
title_en: "Advanced Packaging Part 2 - Review Of Options/Use From Intel, TSMC, Samsung, AMD, ASE, Sony, Micron, SKHynix, YMTC, Tesla, and Nvidia"
date: 2022-01-06
source: https://newsletter.semianalysis.com/p/advanced-packaging-part-2-review
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 先进封装第二部 – 盘点 Intel、TSMC、Samsung、AMD、ASE、Sony、Micron、SKHynix、YMTC、Tesla 和 Nvidia 的方案与应用

> 原文：[Advanced Packaging Part 2 - Review Of Options/Use From Intel, TSMC, Samsung, AMD, ASE, Sony, Micron, SKHynix, YMTC, Tesla, and Nvidia](https://newsletter.semianalysis.com/p/advanced-packaging-part-2-review) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

先进封装存在于一条「成本和产能 vs 性能与密度」的连续谱上。[在本系列第一部中，我们讲透了先进封装的必要性。](https://semianalysis.substack.com/p/advanced-packaging-part-1-pad-limited)尽管先进封装的需求显而易见，但市面上的先进封装类型和品牌名多到令人咋舌：Intel（EMIB、Foveros、Foveros Omni、Foveros Direct）、TSMC（InFO-OS、InFO-LSI、InFO-SOW、InFO-SoIS、CoWoS-S、CoWoS-R、CoWoS-L、SoIC）、Samsung（FOSiP、X-Cube、I-Cube、HBM、DDR/LPDDR DRAM、CIS）、ASE（FoCoS、FOEB）、Sony（CIS）、Micron（HBM）、SKHynix（HBM）和 YMTC（Xtacking）。从 AMD、Nvidia 到其他众多厂商，我们喜爱的公司都在使用这些封装类型。在第二部中，我们将逐一解释这些封装类型及其用途。[在深度解析的第三部](https://semianalysis.substack.com/p/advanced-packaging-part-3-intels)中，我们分析了 TCB 市场，包括 Intel 的角色、HBM、ASM Pacific、Besi 和 Kulicke and Soffa。

提醒一下邮件列表的读者，请[在浏览器中阅读本文](https://semianalysis.substack.com/p/advanced-packaging-part-2-review)，因为邮件会被截断且看不到更新。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b45d1a4d-b790-48b1-947e-fbfe4bcf56a3_1024x454.png)

倒装芯片（flip chip）是引线键合（wire bonding）之后最常见的封装形式之一。提供倒装芯片的厂商众多，涵盖代工厂、IDM（垂直整合制造商）和委外封测厂。在倒装芯片工艺中，PCB、封装基板或另一片晶圆上会有着陆焊盘（landing pad）。芯片随后被精确放置其上，凸点（bump）与着陆焊盘接触。芯片被送入回流焊炉，加热整个组件使凸点回流，将两者键合在一起。之后清洗掉助焊剂，并在间隙中沉积底部填充（underfill）。这只是基本流程，倒装芯片还有很多不同变体，包括但不限于无助焊剂（fluxless）方案。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6c7cc58a-6728-4bb6-89f3-160d9d7587e3_631x538.png)

虽然倒装芯片极为常见，但间距小于 100 微米的先进版本就没那么普遍了。按照[我们在第一部中确立的先进封装定义](https://semianalysis.substack.com/p/advanced-packaging-part-1-pad-limited)，只有 TSMC、Samsung、Intel、Amkor 和 ASE 在用倒装芯片技术做超大批量的逻辑先进封装。这五家里有三家同时制造完整的硅晶圆，另外两家则是委外封测（OSAT）厂商。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

从这里开始，各种不同类型的倒装芯片封装便蜂拥而至。我们以 TSMC 为例展开，再把其他公司的封装方案与 TSMC 的做对比。TSMC 各封装选项之间最大的差异在于基板材料、尺寸、RDL 和堆叠方式。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9565ddec-afba-4a3e-a401-7a374db45bd4_900x493.jpeg)

在标准倒装芯片中，最常见的基板通常是有机层压板，外面包覆铜。然后围绕核心在两侧构建布线，被讨论得最多的是味之素积层膜（ABF）。核心之上会叠加许多层，这些层负责在整个封装内重分配信号和电源。这些承载信号的层采用干膜压合工艺构建，并用 CO2 激光或 UV 激光进行图案化。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/cb5f7e0e-9c5e-4cda-abf5-5309503d76f4_1024x537.png)

这正是 TSMC 凭借集成扇出（InFO）开始施展拳脚的地方。TSMC 不用 ABF 膜的标准流程，而是采用一种与硅制造结合更紧密的工艺。TSMC 会使用东京电子（Tokyo Electron）的涂胶/显影机、Veeco 光刻机、Applied Materials 的铜沉积设备来光刻定义再布线层（RDL）。这些再布线层比大多数 OSAT 能做到的更小、更密，因此能够承载更复杂的布线。这一工艺称为晶圆级扇出封装（FOWLP）。最大的 OSAT 厂商 ASE 提供FoCoS（fan out chip on substrate，基板上的扇出芯片），它是 FOWLP 的一种，同样运用硅制造技术。Samsung 也有自己的扇出系统级封装（FOSiP），主要用于智能手机、智能手表、通信和汽车。大多数智能手机都包含来自 ASE、Amkor、Samsung 或 TSMC 的扇出封装。

借助 InFO-R（RDL），TSMC 可以封装具有高 IO 密度、复杂布线和/或多颗芯片的芯片。使用 InFO-R 最常见的产品是 Apple iPhone 和 Mac 芯片，但移动芯片、通信平台、加速器甚至网络交换 ASIC 的种类也很繁多。Samsung 也凭借 Cisco Silicon One 在网络交换 ASIC 扇出封装市场上有所斩获。InFO-R 未来的进步主要体现在向更大封装尺寸、更高功耗和更多 IO 的扩展上。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2c824a15-3d80-4e8f-9bc7-e1f933f8290a_1024x851.png)

4 月更新：坊间有不少传闻称 AMD 将在其下一代 Zen 4 客户端（见上图）和服务器 CPU 上转向扇出封装。SemiAnalysis 曾试图确认基于 Zen 4 的桌面和服务器产品将采用扇出封装。该封装随后再以传统方式封装在标准有机基板上，基板底部带有 LGA 引脚。封装这些产品的厂商以及转向或不转向扇出的技术原因，将在付费墙后揭晓。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/29febe14-d620-49be-852d-3256c0400a61_1023x333.png)

标准封装在核心基板两侧各有 2 到 5 层再布线层（RDL），更先进的集成扇出也是如此。TSMC 的 InFO-SoIS（system on integrated substrate，集成基板系统）将这一概念推向了新高度。它提供多达 14 层再布线层（RDL），可实现裸片间极为复杂的布线。基板上靠近裸片处还有一层密度更高的布线层。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1a707218-34fb-44dc-86fb-12becf5a00bf_1023x544.png)

TSMC 还提供 [InFO-SOW](https://semianalysis.com/tesla-ai-day-supercomputer-chip-teaser-is-this-the-first-deployment-of-tsmc-info_sow/)（system on wafer，晶圆级系统），它可以做到整片晶圆大小的扇出封装，塞进几十颗芯片。[我们写过采用这种特殊封装形式的 Tesla Dojo 1](https://semianalysis.com/tesla-dojo-ai-super-computer-unique-packaging-and-chip-design-allow-an-order-magnitude-advantage-over-competing-ai-hardware/)。我们还在去年 Tesla 于 AI Day 正式发布[之前数周，独家披露了这项技术的使用](https://semianalysis.com/tesla-ai-day-supercomputer-chip-teaser-is-this-the-first-deployment-of-tsmc-info_sow/)。Tesla 的 HW 4.0 将采用 Samsung 的 FOSiP。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/65c77a82-a597-4a00-b30b-80caf8439e9c_1024x576.jpeg)

最后，在 TSMC 的集成扇出产品线中还有 InFO-LSI（local silicon interconnect，局部硅互连）。InFO-LSI 就是 InFO-R，但在多颗裸片下方垫了一块硅。这个局部硅互连起初只是多颗裸片间的无源互连，但未来可以演化为有源的（包含晶体管和各类 IP）。它最终还会微缩到 25 微米，但我们认为第一代不会。首个采用这种封装的公开产品将在付费墙后揭晓。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

脑子里蹦出来的直接对比，很可能是 Intel 的 EMIB（嵌入式多裸片互连桥），但那其实不是最佳参照。它更像 Intel 的 Foveros Omni 或 ASE 的 FOEB。容我们解释。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/cde00900-0cd1-40dd-a24e-fde85e1e3c08_1024x546.png)

Intel 的嵌入式多裸片互连桥被放入传统有机基板的空腔（cavity）中，然后基板继续向上构建。这既可以由 Intel 自己完成，EMIB 的放置和基板堆叠也可以由传统有机基板供应商来做。由于 EMIB 裸片上的着陆焊盘很大，且层压布线和通孔的沉积方式所致，不需要极其精确地把裸片放到基板上。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a22aae59-491d-4855-aa17-d5877cb3c435_1024x683.png)

Intel 通过继续使用现有的有机层压板和 ABF 供应链，避开了更昂贵的硅基板材料和硅制造工艺。总体而言，这条供应链已是充分商品化的大宗市场，[尽管当前因短缺而相当紧张](https://fortune.com/2021/09/16/chip-shortage-supplier-component-abf-substrate-shares/)。Intel 的 EMIB 自 2018 年起就开始出货，产品包括 Kaby Lake G、多款 FPGA、Xe HP GPU，以及包括 Sapphire Rapids 在内的部分云服务器 CPU。目前所有 EMIB 产品都使用 55 微米间距，第二代是 45 微米，第三代是 40 微米。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/55f4a35e-c54b-43bb-869d-8e6e58dfce8b_800x572.jpeg)

Intel 可以穿过这颗桥接裸片向上方的有源裸片供电。Intel 还保有灵活性，可以让封装在没有 EMIB 和某些小芯片（chiplet）的情况下照常工作。对 Intel FPGA 的一些拆解发现，如果出货的 SKU 不需要，Intel 就不会放置 EMIB 和有源裸片。这使他们能针对特定市场段优化物料清单（BOM）。最后，只在需要的地方使用硅桥，Intel 还能省下制造成本。这与 TSMC 的 CoWoS 形成对照——后者是把所有裸片都放在一整块巨大的无源硅桥之上。这个稍后再展开；TSMC 的 InFO-LSI 与 Intel 的 EMIB 之间最大的差异化因素，在于基板材料和制造工艺的选择。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/107976cd-bf21-4c89-9e75-d7124349f8eb_1023x571.jpeg)

让事情更复杂的是，ASE 也有自己的 2.5D 封装技术，而且与 Intel 的 EMIB 和 TSMC 的 InFO-LSI 都截然不同。它正被用于 AMD 的 MI200 GPU，后者将进入多台高性能计算机，包括美国能源部的 Frontier 百亿亿次（exascale）系统。ASE 的 FOEB 封装技术与 TSMC 的 InFO-LSI 更相似，因为它也是扇出型。TSMC 用标准硅制造技术构建 RDL，而一个重大区别在于 ASE 用的是玻璃载板（panel）而非硅。这是一种更便宜的材料，但它还有一些别的好处，我们稍后讨论。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/bb29a460-21b4-40a2-b3cd-f98a16bd1c77_814x488.jpeg)

ASE 不是把无源互连裸片嵌入基板空腔，而是先放置裸片，构建铜柱加焊料帽（solder cap），然后构建整个 RDL。在 RDL 之上，再用微凸点（micro-bump）连接放置有源硅 GPU 裸片和 HBM 裸片。随后用激光剥离（laser release）工艺把玻璃中介层从封装上移除，完成封装另一面的工序，最后用标准倒装芯片工艺安装到有机基板上。

ASE 就 FOEB 对比 EMIB 做了许多宣称，但有些完全是错的。ASE 需要营销自己的方案，这可以理解，但让我们拨开噪音。EMIB 的良率不在 80% 到 90% 之间，而是接近 100%。第一代 EMIB 在裸片数量上确实有扩展限制，但第二代没有。事实上，Intel 即将发布有史以来最大的封装产品——一颗 92mm × 92mm BGA 封装的先进封装，用的就是第二代 EMIB。FOEB 通过在整个封装中使用扇出和光刻定义的 RDL，确实在布线密度和裸片到封装的凸点尺寸上保有优势，但那也更贵。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

对比 TSMC，最大的区别似乎在于起初的玻璃基板材料 vs 硅。其中一部分原因可能是 ASE 的成本约束更紧。ASE 必须靠以更低价格提供好技术来赢得客户。TSMC 是玩硅的大师，专注于自己最擅长的技术——硅。TSMC 有把技术推向极限的文化，在这次冲锋中选硅对他们更合适。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/fcb6b2e1-1fb0-4b45-9073-372062de0d46_1024x537.png)

现在回到 TSMC 的其他先进封装选项，因为还有几个要讲。CoWoS 平台还有 CoWoS-R 和 CoWoS-L，它们与 InFO-R 和 InFO-L（原文如此）几乎一一对应。两者的区别更多在工艺上。InFO 是芯片先行（chip first）工艺：先放芯片，再围绕它构建 RDL。CoWoS 则是先构建 RDL，再放芯片。对大多数想理解先进封装的人来说，这个区别没那么重要，所以我们今天就一笔带过。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d9f19dd7-c917-4670-b18f-2cb8ad6ae7f0_1024x443.jpeg)

真正的大明星是 CoWoS-S（硅中介层）。它把一颗已知良好裸片（known good die）倒装封装到一片内含图案化布线的无源晶圆上。CoWoS 的名字正由此而来——Chip on Wafer on Substrate（基板上的晶圆上的芯片）。它是目前出货量最大的 2.5D 封装平台，而且遥遥领先。如第一部所述，这是因为 Nvidia 的数据中心 GPU——P100、V100 和 A100——都使用 CoWoS-S。虽然 Nvidia 一直是出货量最大的，但 Broadcom、Google TPU、Amazon Trainium、NEC Aurora、Fujitsu A64FX、AMD Vega、Xilinx FPGA、Intel Spring Crest 和 Habana Labs Gaudi，只是 CoWoS 使用者中另外一些著名例子。大多数带 HBM 的重计算芯片，包括各家创业公司的 AI 训练芯片，都用 CoWoS。

为了进一步把 CoWoS 的无处不在钉死在棺材板上，这里引用 Alchip 的几句话。Alchip 是一家台湾的设计与 IP 公司，主要协助 EDA、物理设计以及与采用 TSMC CoWoS 平台相关的产能工作。这些引语来自 Alchip，但是 [Fabricated Knowledge 的 Doug O'laughlin 在他的精彩分析中提醒我们注意的。](https://www.fabricatedknowledge.com/p/on-semi-and-nxpi-alchip-onto-and)

> 由于 TSMC 要求我们不要向市场传递任何数字化指引，我们不被允许给出（财务指引）。

Alchip 是一家上市公司，却因为 TSMC 的一句话而不能给指引……

> 量产预测方面，我们从关键客户那里收到了极其巨大的量。数字大到难以消化。老实说，如果我们能达成——只要供应商能支持我们满足他们预测的 50%，我们就能轻松再来一记全垒打。是的，老实说，我们收到的 NP 预测高得离谱。

Alchip 的产能受到极大限制，确切地说是 CoWoS。

> 事实上，如果（单一云）客户单独去找他们（TSMC），他们会拒绝所有会面，但他们仍然和 Alchip 合作。他们愿意和我们合作的原因是我们代表着 30 多家客户。所以他们需要——他们也需要分散自己的业务集中度。所以我们可以说我们得到了很好的支持，但当然不是 100%。因为所有产能都已被 Daniel 之前提到的一线客户（tier 1）订光了。

TSMC 甚至不接每一个与 CoWoS 产能相关的会议，因为 TSMC 早就把产出的东西全卖光了，而且支持那么多设计要占用太多工程时间。另一方面，TSMC 的客户集中度高（Nvidia），所以 TSMC 想与其他公司合作。Alchip 某种程度上充当着中间人，即便一线客户（Nvidia）已包下一切，Alchip 仍能拿到一些产能。即便如此，他们也只拿到想要的 50%。

再掉头看看 Nvidia 在干什么。Q3，他们的长期供应义务跳升到 $6.9B，更重要的是，Nvidia 支付了 $1.64B 预付款，未来还将再支付 $1.79B。Nvidia 正在大口吞下供应，特别是 CoWoS。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2813f02b-d0d5-438f-a994-75bf40823c0b_700x392.png)

回到技术上，CoWoS-S 这些年经历了一场进化。主旋律是中介层面积越做越大。由于 CoWoS 平台使用硅制造技术，它受一条称为光罩极限（reticle limit）的原则约束。193nm ArF 光刻机能印制的芯片最大尺寸是 33mm × 26mm（858mm2）。硅中介层的主要用途同样由光刻定义——承载连接其上芯片的极密布线。Nvidia 的芯片早就逼近光罩极限本身，却还要连接封装内的 HBM。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/16022b6e-9fe3-43db-8b5b-ef1119605eeb_1024x541.jpeg)

上图中是一颗 Nvidia V100——Nvidia 四年前的 GPU，面积 815mm2。算上 HBM 之后，它就超出了光刻机可印制的光罩极限，但 TSMC 想出了连接办法。TSMC 靠的是一种叫光罩拼接（reticle stitching）的技术。TSMC 在这方面的能力不断增长，硅中介层已经可以做到 3 倍光罩尺寸。考虑到光罩拼接的局限，Intel EMIB、TSMC LSI 和 ASE FOEB 这些路线各有其价值，它们也不必承担大尺寸硅中介层的那份开销。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5fab5469-75a8-4c3e-aa9f-533bf0eab4a3_720x540.jpeg)

除了加大光罩尺寸，他们还做了其他改进，比如把微凸点从焊料换成铜以提升性能/能效、[iCap](https://en.wikichip.org/wiki/tsmc/cowos#Integrated_Capacitor_.28iCAP.29)（集成电容）、新的 TIM/盖板封装等等。

关于 TIM/盖板封装有个有意思的故事。在 Nvidia V100 时代，Nvidia 有一个遍布各地的 HGX 平台，会发货给许多服务器 ODM，再流向数据中心。散热器螺丝要达到正确安装压力所需的扭矩非常讲究。这些服务器 ODM 把散热器拧得过紧，弄裂了这些 $10k GPU 上的裸片。Nvidia 在 A100 上转向了带盖板（lid）的封装，而不是裸片直触散热。当 Nvidia 的 A100 和未来的 Hopper 数据中心 GPU 仍需要散发巨量热量时，这类封装的问题就冒出来了。为此 TSMC 和 Nvidia 在封装上做了大量优化。总之，关于下一代 Hopper GPU 的封装和功耗要求，我们会在付费墙后提供一些信息。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

Samsung 也有自己的 I-Cube 技术，类似 CoWoS-S。Samsung 这项封装的唯一大客户是 Baidu，用在其 AI 加速器上。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1e623ace-eb2a-4b3d-ab0f-8178984a6005_1024x524.jpeg)

接下来是 Foveros。这是 Intel 的 3D 芯片堆叠技术。不是一颗有源裸片叠在一颗本质上只是密布导线的裸片上，Foveros 的两颗裸片都含有源元件。Intel 的第一代 Foveros 于 2020 年 6 月随 Lakefield 混合架构 CPU SoC 问世。这颗芯片出货量不算大，也不算惊艳，但它为 Intel 开创了多个第一：3D 封装，以及他们首个混合 CPU 核心架构——一个大性能核加若干小能效核。它采用 50 微米凸点间距。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8b859268-b09b-441a-8d1b-851d2bf6f58a_1024x576.png)

下一款 Foveros 产品是 Ponte Vecchio GPU，历经多次延期后，应该会在今年面世。它将包含 47 颗不同的有源小芯片（chiplet），用 EMIB 和 Foveros 封装在一起。Foveros 的裸片间连接采用 36 微米凸点间距。

未来，Intel 客户端产品线的大部分都将使用 3D 堆叠技术，包括代号 Meteor Lake、Arrow Lake、Lunar Lake 的客户端产品。[Meteor Lake 将是第一款采用 Foveros Omni 和 36 微米凸点间距的产品。](https://fuse.wikichip.org/news/5949/intel-unveils-foveros-omni-and-foveros-direct-leveraging-hybrid-bonding/)第一款包含 3D 堆叠技术的数据中心 CPU 代号 Diamond Rapids，排在 Granite Rapids 之后。[这些产品各自采用什么节点，以及 Intel 与 TSMC 的关系，我们在本文中讨论。](https://semianalysis.substack.com/p/tsmc-wants-to-make-intel-dependent)

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b46f041d-63ec-4d76-b287-939ffe0a96c0_970x509.png)

Foveros Omni 的全称是 Foveros Omni-Directional Interconnect（ODI，全向互连）。它弥合了 EMIB 与 Foveros 之间的鸿沟，还提供一些新特性。Foveros Omni 既可以作为两颗芯片之间的有源桥接裸片，也可以作为完全位于另一颗裸片下方的有源裸片，或是叠在另一颗裸片上但悬伸出边缘。[David Schor 在这里把各种类型拆解得很好。](https://fuse.wikichip.org/news/2503/intel-introduces-co-emib-to-stitch-multiple-3d-die-stacks-together-adds-omni-directional-interconnects/)

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/50a758d8-1788-4f2d-b91c-4dd4cf87217d_817x241.png)

Foveros Omni 从不像 EMIB 那样嵌在基板内部，它在任何情形下都是完整地坐在基板之上。这类堆叠方式带来了一个问题：封装基板到其上芯片的连接高度不一。Intel 开发了一种铜柱技术，让他们能把信号和电源输送到不同的 z 轴高度并穿过裸片，芯片设计师在设计 3D 异构芯片时因此获得更大自由。Foveros Omni 将从 36 微米凸点间距起步，并在未来一代微缩到 25 微米。

我们要指出，DRAM 也在使用先进 3D 封装。HBM 多年来一直在 Samsung、SK Hynix 和 Micron 那里使用先进封装。存储单元先制造并连接到硅通孔（TSV），随后 TSV 露出并形成微凸点。最近，Samsung 甚至开始推出 DDR5 和 LPDDR5X 堆叠，用类似的堆叠技术把容量堆得更高。SK Hynix 的 HBM3 将从 12 颗 DRAM 裸片垂直堆叠起步，[每颗 DRAM 裸片厚度 30 微米。](https://news.skhynix.com/sk-hynix-announces-development-of-hbm3-dram/)SK Hynix 最终还将在 HBM3 中引入混合键合（hybrid bonding），届时将把 16 颗芯片键合在一起，每颗裸片还要更薄。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/19578691-f944-4d59-99cc-349eceaebd11_1024x319.jpeg)

混合键合是这样一种技术：不用凸点，芯片通过硅通孔直接连接。回顾倒装芯片流程，这里没有凸点成型、助焊剂、回流，也没有填充芯片间隙的底填胶。铜与铜直接相接，就这么简单。实际工艺非常困难，上文有部分详解。我们将在本系列下一部分深入讨论混合键合的设备生态和类型。混合键合能实现比此前所述任何封装方法更密的集成。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/841eab1c-3df5-49f6-a0f8-8e37c92e90ad_1024x576.jpeg)

最有名的混合键合芯片，当然是最近发布、定于今年晚些时候上市的 AMD 3D 堆叠缓存（3D V-Cache）。它采用 TSMC 的 SoIC 技术。Intel 给混合键合的品牌名是 Foveros Direct，Samsung 的版本叫 X-Cube。[GlobalFoundries 公开展示过与 Arm 用混合键合合作的测试芯片。](https://fuse.wikichip.org/news/2680/globalfoundries-arm-demonstrate-high-density-3d-stacked-mesh-interconnect-for-hpc-applications/)出货量最大的混合键合半导体公司不是 TSMC，今年不是，明年甚至也不是。混合键合芯片出货量最大的公司其实是 Sony，靠的是他们的 CMOS 图像传感器。事实上，只要你用的是高端手机，你口袋里大概率就有一台含混合键合 CMOS 图像传感器的设备。如第一部详述，Sony 已把间距微缩到 6.3 微米，而 AMD 的 V-Cache 是 17 微米间距。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/62d18cb2-3bca-40c9-9e93-09f966042d42_1024x556.jpeg)

目前 Sony 出货 2 层堆叠和 3 层堆叠版本。2 层堆叠中，像素位于电路之上。3 层堆叠版本中，像素叠在 DRAM 缓存之上，DRAM 又叠在电路之上。进步还在继续：Sony 正致力于把像素晶体管从电路中拆分出来，打造最多 4 层硅的更先进相机。上图展示的是 Sony 的顺序堆叠（sequential stacking），间距做到 0.7 微米！

混合键合另一个即将放量的应用来自[长江存储（YMTC）的 Xtacking](https://semianalysis.com/the-impending-chinese-nand-apocalypse-ymtc-128-layer-nand-is-the-first-semiconductor-where-china-is-technologically-competitive/)。YMTC 用晶圆对晶圆（wafer to wafer）键合技术把 CMOS 外围电路堆叠在 NAND 栅极下方。我们[在此详细分析过这项技术的好处](https://semianalysis.com/the-impending-chinese-nand-apocalypse-ymtc-128-layer-nand-is-the-first-semiconductor-where-china-is-technologically-competitive/)，简而言之：在给定 NAND 层数下，它让 YMTC 能塞进比任何其他 NAND 厂商——包括 Samsung、SK Hynix、Micron、Kioxia 和 Western Digital——更多的 NAND 单元。

关于各种类型的倒装芯片、热压键合和混合键合设备，还有很多可讲，但我们留到后续几部分。投资圈对 Besi Semiconductor、ASM Pacific、Kulicke and Soffa、EV Group、Suss Microtec、SET、Shinkawa、Shibaura、Xperi 和 Applied Materials 的普遍认知并不正确，各家公司在各种封装类型上的设备使用差异非常宽泛。赢家并不像看起来那么一目了然。

付费墙后是关于 InFO-LSI 首个客户/产品、Zen 4 封装、Nvidia Hopper 细节（包括节点、功耗、封装）等更多内容。

[分享](https://newsletter.semianalysis.com/p/advanced-packaging-part-2-review?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)
