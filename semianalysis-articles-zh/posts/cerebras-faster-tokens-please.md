---
title: "Cerebras——请给更快的 token"
title_en: "Cerebras — Faster Tokens Please"
subtitle: "OpenAI 与 AWS 的合作、Tokenomics 解读、架构深度解析、数据中心爬坡、技术路线图"
date: 2026-05-13
source: https://newsletter.semianalysis.com/p/cerebras-faster-tokens-please
crawled: 2026-09-15
authors: ["Myron Xie", "Jordan Nanos", "Max Kan", "Cam Quilici", "Tanj Bennett", "Ivan Chiam", "Louis Lu", "Zane Fong", "Gerald Wong", "Reyk Knuhtsen", "Nicolas Bontigui", "Wega Chu", "Dylan Patel", "Konrad Wang", "Oliver Shawa"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Cerebras——请给更快的 token

> 原文：[Cerebras — Faster Tokens Please](https://newsletter.semianalysis.com/p/cerebras-faster-tokens-please) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**OpenAI 与 AWS 的合作、Tokenomics 解读、架构深度解析、数据中心爬坡、技术路线图**

距离 Dylan 在 2021 年 6 月为本刊撰写[专门介绍 Cerebras 的文章](https://newsletter.semianalysis.com/p/cerebras-wafer-scale-hardware-crushes)已近 5 年。他当时 2 天发了 4 篇文章！时代真是变了。

变化的另一件事是 Cerebras 的命运。随着快 token 登上主舞台、以及与 OpenAI 签下 750MW 算力大单，Cerebras 觉得自己已经准备好接受公开市场的审视。而就在 6 个月前，我们还认为晶圆级引擎（Wafer Scale Engine）尽管创新大胆，却存在一些难以掩盖的技术短板——这也是 GPU、TPU 等 HBM 加速器持续流行的原因。多年来，Cerebras 的强项（也就是：速度）一直被忽视，行业更看重总吞吐量。但现在，随着前沿实验室为同一套模型权重推出 fast（快速）、priority（优先）、standard（标准）和 batch（批量）等不同档位，全世界已经用钱包表明了他们对快 token 的偏好。这让 Cerebras 的长处走到台前，也是 OpenAI 愿意为 Cerebras 算力掏出数百亿美元的关键原因。

需求强劲到让所有参与者都显得光鲜。

今天，在 Cerebras IPO 前夜，出于我们对晶圆的热爱，我们发布一篇相当于 4 篇普通文章篇幅的长文。文中我们将深入探讨：

1. 快速推理
2. WSE-3，Cerebras 独特的晶圆级芯片
3. CS-3，Cerebras 的系统及其独特架构
4. 提供 BOM 成本分析
5. 解释晶圆在快速推理中何时以及如何取胜
6. 描述晶圆的一些局限性，展示其中的取舍

对付费订阅者，我们还会展示这笔改变公司命运的 OAI 推理大单的经济学，并分享我们对 Cerebras 向新兴 GPU 云（neocloud）转型进度的看法（即到 2028 年为 OpenAI 落实所需的 750MW）。此外，我们还将讨论 Cerebras 未来的计划：把晶圆级光收发器混合键合到他们的 WSE 计算引擎上——他们声称这样做纯粹是出于对这项事业本身的热爱，因为 LLM 推理并不需要它，但老派 HPC（HPC boomer）负载需要。这些 HPC 客户在 NVIDIA 将其 GPU 上的原生 FP64 硬件削减到基本为零之后，实际上已被抛弃。

## 对速度的需求

快速推理已经到来。

尽管 SemiAnalysis 历来是「SRAM 机器」的黑粉，但当 NVIDIA 在 2025 年 12 月以「许可+收购+招聘」三合一的方式（licensiquihired）收编 Groq 之后，一切都变了。显然 Jensen 看到了至少 $20B 的价值，而仅仅几个月后，当我们迎来 [Claude Code 拐点](https://newsletter.semianalysis.com/p/claude-code-is-the-inflection-point)时，他也被证明是对的。如今，晶圆已在这行站稳了脚跟。

许多人（包括 [Andrej Karpathy](https://x.com/karpathy/status/1964036961750176232?s=20)）过去认为原始智能/能力远比速度重要，但我们最终用显示性偏好证明：有些时候恰恰相反。一旦智力越过某个门槛，开发者宁可要更快的 token，也不要更聪明的 token。而在 AI 已经渗透到工作流几乎每个环节的世界里，token 的生成速度可能成为「心流状态」（flow state）的瓶颈，也就是决定你能完成多少高效产出。

众所周知，Opus 4.6 fast 模式收取 6 倍的价格，换来 2.5 倍的交互速度（不过现在已经不到 2 倍，见下图）。4 月份，我们 80% 的 AI 支出（曾一度达到[年化 $10M](https://x.com/dylan522p/status/2047104466512400639?s=20)的峰值）都花在了 Opus 4.6 fast 上。当 Opus 4.7 发布时，我们的许多工程师拒绝切换，因为它不含 fast 模式。值得注意的是，这是我们第一次主动放弃前沿智能以换取更快的 token（而且还是以显著溢价！）。

顺带一提，Opus 4.6 fast 最近越来越不划算。标准版 Opus 4.6 在 Claude Code 中的交互速度稳定在约 40 tps（每秒 token 数）。Opus 4.6 fast 此前能提供 > 100 tps，兑现 2.5 倍提速的承诺。但最近已退化到约 70 tps（只有 1.75 倍提速）。我们最近与 OpenRouter 的朋友们合作，收集了 Claude Opus 两种运行模式的数据。

![](https://substack-post-media.s3.amazonaws.com/public/images/159ba52d-f46d-402a-9e50-35434689b48f_5525x1790.jpeg)
*来源：OpenRouter*

我们认为 Opus 4.6 Fast 是 Anthropic 毛利率最高的 SKU，也是其今年 ARR 爆炸式增长的重要原因。不过，考虑到速度变慢、4.7 支持延迟以及即将发布的 Mythos，这一判断能否持续还有待观察。关于 OpenAI/Anthropic 按模型细分的营收深度数据，请参阅我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)。

## 吞吐量-交互性前沿

要完整解释 Cerebras 在其晶圆级芯片上做出的架构决策，我们首先需要回顾推理的基本原理。

正如 Jensen 在今年 [GTC](https://www.youtube.com/watch?v=jw_o0xr8MWU&t=3684s) 上反复强调的，吞吐量（tokens/sec/gpu）与交互性（tokens/sec/user）是推理的根本性权衡。在我们最初的 [InferenceX 文章](https://newsletter.semianalysis.com/p/inferencemax-open-source-inference)中，我们把它比作公交车与法拉利：你可以选择慢速服务大量用户、快速服务单个用户，或介于两者之间的任何组合。

![](https://substack-post-media.s3.amazonaws.com/public/images/76b1bbd0-2e49-4be6-989d-4e9008bea906_2328x1712.png)
*来源：SemiAnalysis InferenceX*

当然，用户也愿意为更高的交互性支付更多费用，因此对于特定模型提供商来说，帕累托前沿上究竟哪个点能最大化推理的整体营收和盈利能力，目前尚不清楚。现实情况是，各家提供商目前正在部署多种选项，试图覆盖整个市场。fast 模式、priority 模式、batch 定价以及特定模型架构，都是 OpenAI 和 Anthropic 为找到最适合其用户群体的组合而进行的实验。

![](https://substack-post-media.s3.amazonaws.com/public/images/7dc6ebf5-3fdd-4192-b28b-a0350da6149a_2242x962.png)
*来源：SemiAnalysis Tokenomics 模型*

在给定硬件下，调整批大小（batch size，或称「并发数」，即同时服务的用户数）是沿曲线移动的主要手段。这正是 [InferenceX](https://inferencex.semianalysis.com) 的精妙之处。大多数其他公开推理基准测试只考虑单一交互性水平下的单一工作负载，而 InferenceX 为所有顶级开源模型构建了横跨 3 种输入/输出序列长度组合的完整帕累托前沿。这让你能绘制出如下图所示的图表：GB300 NVL72 在低交互性（40 tps）下实现比 H100 高 20 倍的吞吐量，在高交互性（120 tps）下则高出 100 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/a299e7d6-d298-4e7b-9727-28ee6afd82dc_2850x1710.png)
*来源：SemiAnalysis InferenceX 仪表盘*

或者，你也可以通过更换底层硬件沿前沿移动。这就是 Cerebras 和 Groq 这类 SRAM 机器的承诺。它们极高的内存带宽使其能够在高交互性下提升吞吐量，在极端情况下，甚至能达到 HBM 加速器根本无法企及的交互性水平。Cerebras 提供每秒数千 token 的速度，与我们在 InferenceX 中基准测试的加速器相比，这一速度完全超出了图表的坐标范围。

在人们愿意为更快 token 支付溢价的世界里，SRAM 机器看起来相当有吸引力，因为它们既能让你（a）以高端速度并发服务更多用户（把前沿「向上推」），也能（b）以更快、更昂贵的速度服务部分用户（把前沿「向右延伸」）。

## 晶圆级引擎

Cerebras 的根本性押注，是突破单颗硅片的光罩极限。不是把晶圆切割成多颗芯片，而是让整片晶圆成为一颗芯片。这种聪明的扩展方式是为了解决摩尔定律放缓带来的一大堆问题，以及硅片面积不得超过 858mm2 的硬约束——即基于光罩的光刻中单个光罩图形的尺寸。这颗晶圆尺寸的芯片就是他们的晶圆级引擎（Wafer Scale Engine，WSE）。

![](https://substack-post-media.s3.amazonaws.com/public/images/db7fdea3-ee52-4f19-9942-9a7a55ad7334_1078x1101.jpeg)
*来源：Cerebras*

WSE 是在整个晶圆上由 84 个完全相同的步进曝光图形/裸片（die）组成的 12 x 7 阵列，共同构成一片硅。每片晶圆（或称芯片）拥有一大池极快的 SRAM。50% 的硅面积用于 SRAM 单元，其余 50% 由计算核心组成。关键创新在于把计算硅片和内存放在同一片硅上，而不是把多颗不同的芯片互连起来。这节省了数据离开硅片或离开封装所带来的功耗、延迟和成本。

![](https://substack-post-media.s3.amazonaws.com/public/images/4c457cb1-4cd5-4c85-ba8d-7ad67ae58ad2_2194x1243.jpeg)
*来源：Cerebras*

「传统」GPU 和 XPU 需要先进封装和网络来获得更大规模的聚合算力和内存，这在功耗、速度以及更多网络设备方面都要付出代价。虽然这并非同类项的直接比较，但 Cerebras 基于这样一个假设，将其片上（晶圆上）数据流速度与 NVIDIA 的封装外纵向扩展带宽进行对比：数据可以留在 WSE 上，而 GPU 的数据必须移出封装。

![](https://substack-post-media.s3.amazonaws.com/public/images/57968e3f-9e92-4e21-880a-57ab4c34db8e_2238x452.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/cbaae31f-63b2-4217-b2d7-6c4135005a22_2230x370.png)
*来源：Nvidia、Groq、Amazon、Google、Cerebras、SemiAnalysis*

Cerebras 目前处于第三代产品 WSE-3，采用台积电（TSMC）N5 制程节点制造。一片 WSE-3 在整片晶圆（或「单颗芯片」）上拥有 44GB SRAM。这是非常多的 SRAM。典型的大型处理器的片上 SRAM 只有几百 MB。即便是 Groq 的 SRAM 机器，每颗 LPU3 也只有 500MB。SRAM 非常快，因此可以提供 21PB/s 的带宽，比 HBM 高出数千倍。同样，这也显著高于带宽本就很高的 Groq LPU，因为 WSE 拥有更多的 SRAM bank，且各 bank 的带宽聚合在一起。

虽然 Cerebras 为 WSE-3 宣传了很多 FLOPs：125 PFLOPs 的 FP16 算力，但这是稀疏数值，而非稠密数值。这是从 [Jensen 数学](https://newsletter.semianalysis.com/i/174558496/jensen-math-changes-every-year)的剧本里学了一手，而且玩得更狠。与 Nvidia 不同，Cerebras 在公开的 WSE 营销材料中实际上并未标明稠密 FLOPs。不过，Cerebras 在其稀疏数值中假设了 8:1 的非结构化稀疏度，因此稠密 FLOPS 实际上是其 1/8，即 15.6 PFLOPS 的 FP16 计算吞吐量。我们称之为「Feldman 公式」。对于 CS-2/WSE-2，当时假设的比例是 10:1——如下文所见，稀疏与稠密规格之间相差一个数量级。虽然 WSE-3 在绝对计算吞吐量上相对于其他芯片仍然胜出，但单位硅面积的计算能力并不那么亮眼，尤其是在今天。这很可能是因为每个核心都远小于 GPU 的功能阵列尺寸，而这是出于良率收割（yield harvesting）的必要考量，我们将在下文详述。

![](https://substack-post-media.s3.amazonaws.com/public/images/1a58af6b-07ad-4897-82aa-8d5067a45a16_3160x1758.jpeg)
*来源：Cerebras，HotChips 2023*

最后一部分是晶圆外网络，这是 WSE 最薄弱的环节。总带宽只有 150GB/s，仅是那些高度重视网络以扩展能力的 GPU/XPU 竞品的一小部分。我们将进一步讨论低 I/O 的影响，以及增加更多 I/O 的结构性困难。

总结一下：WSE 是一颗非常大的芯片，拥有大量 SRAM，算力总量尚可但相对于硅面积并不算多，网络则几乎为零。下面我们谈谈这些特性带来的影响。

## SRAM 机器

WSE 明显非常强的地方在于 SRAM 容量。与 Groq 的 LPU 一样，WSE 属于我们称之为「SRAM 机器」的加速器类别：更多硅面积被分配给超高速 SRAM，用作主存，存放模型权重和 KV 缓存。相比之下，TPU、Trainium 等主流 GPU 和 ASIC 使用 HBM 存储模型权重和 KV 缓存。它们也有 SRAM，只是更少。总体而言，用 SRAM 换 HBM 意味着高得多的带宽、更低的延迟和更快的 token 输出，但代价是容量，进而牺牲每{芯片、瓦特、美元}的总吞吐量。而且 SRAM 的每 bit 成本也要贵得多。下面是我们[近期关于 NVIDIA + Groq 使用 SRAM 的文章](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands)中的一张图表，对比了这两种技术：

![](https://substack-post-media.s3.amazonaws.com/public/images/e005710a-ca1e-407b-8b3b-fee7875d04f3_2188x350.png)
*来源：SemiAnalysis*

尽管 WSE-3 的 44GB SRAM 相对于任何其他芯片来说都是巨量，但相比单颗 HBM3E 12 层堆叠（12-Hi）提供的 36GB 也多不了多少。随着每颗加速器 8 颗 HBM 堆叠渐成常态，单个 GPU 或 TPU 封装就是 288GB（例如当前一代 Blackwell Ultra），是 WSE SRAM 容量的 6.5 倍。

一些读者可能已经注意到 [DRAM 需求火爆](https://newsletter.semianalysis.com/p/memory-mania-how-a-once-in-four-decades)，其中很大一部分原因是 AI 系统设计师在尽力塞入尽可能多的容量。系统中更多的内存让模型提供商能够：

1. 容纳更大的模型（更多参数）

2. 服务更多并发请求，即更多用户（更多 KV 缓存）

3. 支持更大的上下文窗口，即每请求更长的序列长度（更多 KV 缓存）

推理提供商把上述所有能力做成了一门生意，这就是单 GPU 内存容量不断增加的原因。不仅如此，可用内存并不局限于单个封装，因为工作负载可以分片到多颗芯片上，聚合内存可以在纵向扩展域网络中池化。正因如此，网络才成为所有 AI 硬件公司的关键竞争战场。也就是说，所有公司——除了 Cerebras，他们接受了几乎没有网络的权衡，并在设法绕开它。于是，在片上内存容量受限的情况下，通过联网更多晶圆来腾挪的逃生通道对 Cerebras 而言也窄得多。网络带宽的缺乏虽非致命，但绝对是 WSE-3 设计中的一大短板，阻碍 Cerebras 把业务推向平流层。

话虽如此，Cerebras 如今已走在健康且快速增长的轨道上，其 OAI 交易是改变格局的一笔：到 2028 年，Cerebras 需要交付的服务器数量将比公司成立以来交付的总和还高一个数量级。需求激增已经体现在台积电的晶圆投片中——为满足 OpenAI 的部署要求，投片量年内逐季度大幅攀升。我们预计 Cerebras 营收未来几年将出现急剧向上的拐点，OpenAI 是主要增长驱动力。

![](https://substack-post-media.s3.amazonaws.com/public/images/7471a61d-a155-4295-8839-a13ec0a3b390_1908x1062.png)
*来源：SemiAnalysis 加速器模型*
![](https://substack-post-media.s3.amazonaws.com/public/images/8ca14604-880f-4b74-94be-cb53709e80a8_1898x1112.png)
*来源：SemiAnalysis 加速器模型*

## Cerebras 的技术

走到今天这一步，Cerebras 解决了从硅片、系统到软件的诸多技术难题。必须承认，这里有大量专有硬件技术，尤其是与其他众多加速器初创公司拿出的创新（或创新匮乏）相比。晶圆是一次大胆的押注，在位者和竞争者都不容易复制。

Cerebras 的部分专有技术包括：

1. 跨裸片布线与走线。Cerebras 利用切割道（scribe lines）作为片上数据网络的布线，把所有裸片连接在一起。在典型晶圆中，切割道是禁布区，晶圆在那里被切割以分离出单颗裸片。

2. 冗余与失效绕行。为了获得可接受的良率，绕过缺陷核心重新走线的能力至关重要。缺陷不可避免，对于接近光罩极限大小的单元尤其如此。通常，接近光罩尺寸的高密度处理器的分类良率（sort yield）远低于 50%。出于冗余考虑，WSE 上总共有 970,000 个核心，其中 900,000 个被启用。为了更好地收割良率，每个核心都被刻意做得非常小。然而这并不简单，需要付出可观的额外成本。其中一件有意思的事情是，**每批次**晶圆的上层金属都会有定制光罩组。目的是让每批次有不同的布线，绕开所有有缺陷的瓦片。额外光罩的成本是在台积电名义晶圆价格之上的一笔可观加价。为什么要为每一批晶圆都这样做？原因在于批次内的工艺波动低于不同批次之间的波动。[点击此处了解半导体制造工艺波动的更多知识。](https://newsletter.semianalysis.com/p/embracing-chaos-the-imperfect-art?utm_source=publication-search)这样做的最终结果是晶圆级良率相当高。台积电产出的晶圆中，近 100% 都好到可以组装进量产服务器。

3. 供电与散热。Cerebras 解决的重大挑战之一，是向单片晶圆输送超过 20KW 的电力，而下一代还会更多。如此大的功率迫使其采用 Vicor 的定制供电方案。这些功率当然会转化为必须带走的热量，因此需要专门的散热。每台 CS 服务器中的供电与散热子部件被称为「发动机缸体」（engine block）。这是又一个关键部件，与 WSE 硅片本身一样，是为 Cerebras 独家定制的架构。

尽管取得了这些值得称道的技术成就，WSE 架构仍会遇到一些技术极限，制约着其技术路线图和供应 token 的能力。

### 热设计与散热

在单片 46,225 mm² 的晶圆上带走 25 kW 热量，是 CS-3 设计的核心热学难题，折算下来在考虑热点之前，裸片上平均功率密度约为 50 W/cm²。风冷方案被否决了，因为如果把 3D 均热板散热器（类似 HGX H100 服务器中的那种）放大到覆盖 21.5 cm 见方的裸片，会超出其吸液芯的毛细极限，在工作介质回到蒸发器之前就干涸了。CS-3 采用定制的液冷堆叠，其架构、流量和机柜级管路与人们更熟悉的 Nvidia 冷板式直冷单相部署方案有所不同。

散热方案 100% 定制，并与晶圆协同设计。硅片与其下方的 PCB 受热膨胀的速率不同，在 21.5x21.5cm 的晶圆上，这种失配足以让传统封装开裂。冷板、连接晶圆与 PCB 的连接器，以及装配工装，都必须从零打造。Cerebras 把这套系统称为「发动机缸体」（engine block），一个多层三明治结构，包括冷板、晶圆、柔性连接器、PCB，冷却歧管则贴合在冷板背面。下一节我们将更详细地介绍系统架构。

![](https://substack-post-media.s3.amazonaws.com/public/images/22f7c8c2-fd70-47d6-be88-4c99229baa81_1847x1321.jpeg)
*来源：Cerebras*

排热通过冷板进行。冷却液流经加工在铜板背面的微鳍片通道。铜板朝向晶圆的一面经过抛光，在预紧力下压在硅片上，让两者在以不同速率膨胀时可相对滑动，同时保持接触以传导热量。

在机柜与冷量分配单元（CDU）的接口处，我们发现了另一个架构挑战。GB200 NVL72 的 OCP/Nvidia 参考设计将设施侧流量定为约 1.5 LPM/kW。当今绝大多数 CDU 机队都是按这个常数选型的。WSE-3 在 25kW 下运行流量约 100 LPM，约合 4 LPM/kW，即 NVL72 参考值的约 3 倍。这一差距迫使运营商使用更大的水泵、更大的管道、超规格的 CDU，以及额定流量更高的快速接头。我们认为 CS-4 应会把机柜级流量拉回 1.5–1.7 LPM/kW，如果兑现，将使 Cerebras 回归标准化基础设施。

Cerebras 的主要散热合作伙伴之一是 LiquidStack，该公司于 2026 年 3 月被 Trane Technologies 收购。LiquidStack 与 Cerebras 最初从两相方案开始合作，随后联合开发了匹配 CS-3 流量与压力包络的 L2L（液到液）单相 CDU。

进水温度是 Cerebras 与其他芯片分道扬镳的最后一个维度。Cerebras 的俄克拉荷马设施运行一座 6,000 冷吨的冷水机组机房，产出 5°C（42°F）冷冻水，再经热交换器升温至约 21°C（约 70°F）后送入发动机缸体。相比之下，NVL72 的规格允许最高 45°C（113°F）的进水温度，让运营商在一年中更长时间采用自然冷却。CS-3 的晶圆级热流密度要求更冷的温度包络，代价则是严重依赖冷水机组的设施。

![](https://substack-post-media.s3.amazonaws.com/public/images/badcce69-3e79-4c94-b7f7-2a8a3f5ef07a_1736x1336.jpeg)
*俄克拉荷马城数据中心的冷水机组机房。来源：Matthew Berman*

### CS-3 架构与 BOM

让我们从液冷中抽身，把视野拉回到 Cerebras CS-3 系统整体。

每台 CS-3 包括以下部件：**一个 WSE-3 发动机缸体**、外围计算与 I/O 模块、两台机械泵、12 个 3.3kW 电源单元，以及液到风或液到液散热系统。

![](https://substack-post-media.s3.amazonaws.com/public/images/b4e18efa-908e-4600-90f4-e294c6e082be_1642x888.png)
*来源：Cerebras*
![](https://substack-post-media.s3.amazonaws.com/public/images/9f854ba6-ee22-4e53-b399-ef5fc0ab0793_1260x766.png)
*来源：Cerebras*

深入到 WSE-3 发动机缸体内部，WSE-3 发动机本身就吃进 25kW 功率。WSE-3 晶圆的供电与散热经过了极度的定制与创新。电力经由盲插电源连接器，从 12 个 3.3kW 电源单元送入 WSE-3 发动机缸体。PSU 以 50V 向 12 块水平堆叠的 PDB（电源分配板）供电。每块 PDB 板对应一排 7 个 Vicor 功率模块，再对应 WSE-3 晶圆上一排 7 个区块。12 块 PDB 板合计就是 84 个功率模块和 WSE-3 晶圆上的 84 个区块。随后，12V 电力被输送至 Vicor 的供电模块——它位于 PCB 上，WSE-3 晶圆就在 PCB 另一侧——Vicor 模块将电力转换为 1V 后送入晶圆。WSE-3 通过弹性体插座（elastomer socket）安装在定制 PCB 上。

![](https://substack-post-media.s3.amazonaws.com/public/images/9f92e984-eb98-4b15-80d2-1fb159adf31e_1847x1321.jpeg)
*来源：Cerebras*
![](https://substack-post-media.s3.amazonaws.com/public/images/fa57a709-356d-450a-8370-495e93d6fe53_1363x801.png)
*来源：Cerebras*

WSE-3 发动机缸体顶部是 I/O FPGA 模块，通过板对板连接器与 WSE-3 PCB 相连。这些 FPGA 本质上充当 NIC，把从晶圆引出的 Cerebras 专有 I/O 转换为用于横向扩展的以太网以及 PCIe。定制冷板分别贴附于 WSE-3 发动机、Vicor 供电模块、CPU 和 I/O FPGA。冷却回路连接到 WSE-3 发动机缸体右侧的歧管。歧管有 6 个接口，其中 4 个接水泵，2 个接液到风或液到液排热系统。

此外，每台 CS 服务器还有一个独立的「KVSS」节点。这是一个双路 AMD CPU 节点，配备 6TB DDR5 RDIMM，用于 KV 缓存卸载。在去年 Q4 开始的内存涨价之前，我们估计 CS-3 系统加 KVSS CPU 节点的 BOM 成本为每机柜 $350k。计入最新的内存涨价后，我们已将 CS-3 系统加 KVSS CPU 节点的 BOM 估计上调至每机柜 $450k。

这个成本非常高，尤其是相对于硅含量而言。名义上，加速器硅片——通常是服务器中最贵的部分——只是一片约 $20k 的台积电 N5 晶圆，但还有大量额外成本。每片晶圆都要定制光罩的要求显著推高了成本。另一大 BOM 项是 Vicor 的供电模块。这是一个需要向晶圆输送 25kW 并采用 VPD（垂直供电）的定制 VRM。其专属定制属性同样意味着高成本，我们认为每颗 WSE 中 VICR 的物料价值与台积电的相差无几。定制散热方案也是如此。组装与封装也由 Cerebras 自行完成，而非交由代工厂。还有一些外围部件，例如 12 个 100GbE Xilinx FPGA，实际充当 NIC，把 Cerebras 自有的 I/O 转换为以太网用于外部通信。

![](https://substack-post-media.s3.amazonaws.com/public/images/65156c7d-3462-4e72-bb26-98a3a60d5639_3143x1161.png)
*来源：SemiAnalysis 估算*
![](https://substack-post-media.s3.amazonaws.com/public/images/207e9fe1-6168-404e-bfea-71cf338e9a59_3142x1160.png)
*来源：SemiAnalysis 估算*

## 晶圆在哪里赢

要在正确的语境下理解 Cerebras 极高的内存带宽，必须戴上 LLM 推理性能工程师的帽子。对性能工程师而言，芯片只是工具。无论你用 10,000 颗 LPU、72 颗 GPU，还是 1 片晶圆来完成任务，重要的是芯片的「算术强度」（arithmetic intensity）——即芯片每与内存传输 1 字节能执行多少 FLOPs（FLOPs/byte）。下表列出了几款芯片的规格，以便将 WSE-3 置于语境中。注意，这些都是理论最大值。

![](https://substack-post-media.s3.amazonaws.com/public/images/0d76ea42-52e2-410d-9675-ec93373e8bfb_2250x354.png)
*来源：NVIDIA、Groq 和 Cerebras 的公开数据手册*

在相对意义上，AI 应用的性能取决于各个 kernel（即运行在设备而非主机 CPU 上的软件）在这些芯片上的表现。AI 中最典型的 kernel 是 GEMM（通用矩阵乘法）。GEMM 可以有不同的形状，由相乘矩阵的形状决定。某些形状在特定硬件上运行时可能受内存限制（即性能受可用带宽制约），或受计算限制（即性能受可用 FLOPs 制约）。

把 WSE-3 的 FLOPs 与 NVIDIA GPU 同口径对比，结果触目惊心。以稠密 FP16 或 INT8 FLOPS 计（也就是使用 Cerebras WSE 的开发者实际可用的 FLOPs），一整片 WSE-3 只有 15.625 PFLOPS。相比原生运行 FP4 的 NVIDIA GPU，B300 为 13.5 PFLOPS（GB300 为 15 PFLOPS），Rubin GPU 则有 35 PFLOPS。当然，细心的读者会指出 FP4 FLOPs 与 FP16 FLOPs 并非总能直接对比，但随着当今大多数生产推理转向 FP4，这是最贴近现实的比较。细心的读者还应留意 Cerebras 产品营销的影响。Cerebras 的营销材料以及他们的 S1 文件中宣称的每片晶圆 PFLOPs 远高于我们表格所示。多亏了「Feldman 公式」，他们用上了 8 倍系数（宣称 8:1 非结构化稀疏）来达到这一数字。这比 Jensen 数学的招牌 2:1 规则的稀疏系数还要大！

要把 Cerebras 与替代方案比较，芯片对芯片（或晶圆对芯片）的直接比较没有意义。下面我们用取整的数字展示一个更有用的比较，说明晶圆所处的位置。

![](https://substack-post-media.s3.amazonaws.com/public/images/f5532809-a0ab-4d74-9769-3a0b54b04dbe_3104x572.png)
*来源：NVIDIA、Groq 和 Cerebras 的公开数据手册*

最有启发性的是把单片晶圆的成本与性能，与约 $1M 的 HBM 和 SRAM 硬件做对比。即：2 套 NVIDIA HGX 系统（16 颗 GPU）、4 个 NVL72 刀片（16 颗 GPU），或约 50 颗 Groq LP30。因此，我们将在下面的图表中逐步叠加更多屋顶线（roofline）。

![](https://substack-post-media.s3.amazonaws.com/public/images/1c68e884-db3b-4979-beb9-5a2d0e1cf6d6_2800x1560.png)
*来源：NVIDIA、Groq 和 Cerebras 的公开数据手册*
![](https://substack-post-media.s3.amazonaws.com/public/images/10fcf32c-73d1-4e62-86b2-e05829fb8aa1_2800x1560.png)
*来源：NVIDIA、Groq 和 Cerebras 的公开数据手册*

这里我们看到单颗 Nvidia Rubin GPU 的 FLOP 碾压一整片 WSE-3：

![](https://substack-post-media.s3.amazonaws.com/public/images/cb70c652-71c2-4979-979e-19d6e24863a8_2800x1560.png)
*来源：NVIDIA、Groq 和 Cerebras 的公开数据手册*

最后，这张图展示了如何把该分析扩展到系统级（尽管方式比较朴素），将单片晶圆 SRAM 的屋顶线与 DGX 系统和 GB300 NVL72 机柜对比。必须假设零网络开销，并叠加多柜 GB300 NVL72，才能在同等算术强度的 kernel 上实现与 Cerebras 相同的 FLOPs。

![](https://substack-post-media.s3.amazonaws.com/public/images/c34918df-d59c-4a49-81d0-5afe0e82609b_2800x1560.png)
*来源：NVIDIA、Groq 和 Cerebras 的公开数据手册*

为了完整理解哪些 AI 工作负载适合 Cerebras，只需看看常见的 GEMM 形状即可。GEMM 通常采用「mnk」记法，即两个输入矩阵的规模分别为「m」和「n」，收缩维度为「k」。

![](https://substack-post-media.s3.amazonaws.com/public/images/4b833324-3a86-441c-ae1b-16bb37a24b41_1178x484.jpeg)
*来源：Pete Warden*

我们可以用以下公式计算给定 GEMM 的算术强度：

作为参考，下面是 LLM 推理中用到的一些 GEMM 形状示例：

![](https://substack-post-media.s3.amazonaws.com/public/images/caaa03ef-5196-4b05-a592-b367c63af339_2680x630.jpeg)
*来源：NVIDIA、Groq 和 Cerebras 的公开数据手册*

最后，下图展示这些 kernel 在不同芯片上的理论性能。只需沿着代表某个 kernel 算术强度的竖线从下往上描，就能看到给定芯片在该 GEMM 形状上能够实现的理论性能（以 TFLOPs 计）。

![](https://substack-post-media.s3.amazonaws.com/public/images/2155958a-7f7e-44a6-9173-364c6cc76e78_2800x1560.png)
*来源：NVIDIA、Groq 和 Cerebras 的公开数据手册*

从大局看，Cerebras 显然拥有非常独特的性能特征：在 WSE-3 的 SRAM 与 FP16 或 INT8 FLOPs 下，其最优算术强度为 0.74。而 HBM GPU 随时间推移走向另一个方向，即算术强度提高到 1000 以上，因此哪些 GEMM 形状（或更广义地说，哪些 kernel）能最高效地利用 Cerebras 硬件，存在明显分野。

为让读者感受某个解码 kernel 的实际可用 FLOPs 长什么样，不妨想象一个 (m=batch=1)、算术强度为 (AI=2) 的解码 kernel。这就是上一张图中最左边的那条竖线。当你沿这条线从下往上描时，会先越过许多芯片才轮到 Cerebras：所有 NVIDIA GPU 和 Groq LPU 在绝对最大、纯理论的情形下也只能实现几十或几百 TFLOPs。而 Cerebras 晶圆（同样是在理论上）可以实现完整的 15.625 PFLOPs。这就是晶圆的关键所在。晶圆上 44GB SRAM 带来的绝对海量的内存带宽，意味着解码 kernel 同样能释放出海量的性能。

回到性能工程师的本职，这意味着低算术强度的解码 kernel 在可实现 FLOPs 上有高得多的理论上限。SRAM 带宽跟得上算力，而运行同一 kernel 的 GPU 的 HBM 却会让 Blackwell SM100 FP4 张量核心吃不饱。因此，未来专为在 Cerebras WSE-3 上运行而设计的模型与工作负载类型——例如 GPT-5.3-Codex-Spark（其架构又名 gpt-oss-120b）——都将把晶圆的性能特征纳入设计考量。

这是软硬件协同设计的完美范例。

## 晶圆有所予，亦有所夺

WSE 有几个我们已提到的明显弱点。它拥有大量 SRAM，但由于 SRAM 在单位瓦特或单位美元上天生不密集，HBM GPU 和 XPU 在每瓦特或每美元上能提供远更多的内存容量。这些 HBM 目前被用于服务上下文更长的大模型，以及更大的用户批处理以提升吞吐量。而通过联网更多晶圆来克服单片内存不足，又受制于晶圆外带宽的匮乏。除非出现英雄般的技术突破（混合键合光收发器晶圆，了解一下？），这两个问题都是 Cerebras 架构中有意为之的部分，使得 Cerebras 难以经济地服务大模型、甚至难以经济地服务如今智能体工作负载所代表的长上下文中型模型。

为说明这一点，我们在 [tokenomics.info/cerebras](https://tokenomics.info/cerebras) 提供了一个交互式计算器。这是我们的 Tokenomics 订阅用户所获得的研究内容的一瞥。

![](https://substack-post-media.s3.amazonaws.com/public/images/c46b9c1e-cedf-4ddb-9333-407198586aa6_1110x775.jpeg)
*来源：Cerebras IPO | Tokenomics.info*

如上图所示，调整平均请求大小、支持的并发请求数、模型大小以及权重和 KV 缓存的量化方式时，运行推理所需的 WSE 总数会发生显著变化。这当然会带来不同的推理或解码性能特征，以及 $/Mtok 成本结论。

计算器中一个值得注意的假设，是我们采用的 96.3k 平均请求大小。Cerebras 选择围绕 64k 平均请求大小的假设为其客户构建推理产品，但我们认为这是运行上下文窗口仅 128k 的模型所留下的痕迹。换句话说，这是确认偏误（confirmation bias）的现实演绎。

![](https://substack-post-media.s3.amazonaws.com/public/images/d88eabe9-a77a-4276-b321-25acf081c32a_818x170.png)
*来源：OpenAI 的 GPT 5.3 Codex Spark 发布公告*

为了准确理解真实世界的流量模式，我们构建了一个代理，从 Claude Code、Codex、Cursor 和 OpenCode 等热门智能体编程工具中收集完全匿名的调用轨迹。这是为 InferenceX 离线回放而收集生产环境智能体轨迹的持续工作的一部分。

约 432k 条请求（约 80B token）的较大样本量让我们确信，典型的 P50 ISL（输入序列长度）约为 96.3k token，而不是 64k 或更少。我们还推断，P90 或 P95 请求的价值可能呈指数级高于初始请求，支持它们仍然至关重要。总体上，我们几乎 50% 的请求超过 128k，而这正是 Cerebras 目前在公开端点上支持的最大上下文窗口。我们看到许多会话的初始上下文长度就超过 100k token，原因包括工具调用上下文、系统提示词，以及 skills 和各种其他形式的引导上下文。

![](https://substack-post-media.s3.amazonaws.com/public/images/882523d5-64de-4ee7-897a-bdf05f3675ed_1201x766.jpeg)
*来源：SemiAnalysis InferenceX AgentX 仪表盘（即将公开发布！）*

此外，整个行业正趋向[无限增大](https://x.com/marmaduke091/status/2052060665120977047?s=20)的上下文窗口——128k 上下文肯定撑不了多久，尤其是在智能体工作负载盛行的当下。本分析的显然结论是：要面向真实流量模式、以完整上下文窗口运行最新开源模型，Cerebras 需要部署大量晶圆。

仅以上面的 DeepSeek v4 为例，一位 CS-3 客户拿 24 台 CS-3（的预算）本可以换成 5 个 GB300 机柜。每个机柜有 20TB HBM，轻松容纳模型权重后还剩超过 19TB 给 KV 缓存。这可是非常多的 KV 缓存，足以服务更多用户、支持更长序列长度，而且这样的机柜还有 5 个。虽然我们已经展示了速度差距有利于 Cerebras，但吞吐量差距就是这样稳稳地倒向 HBM GPU 一边。

## SRAM 微缩已死

可以说，Cerebras 是受 [SRAM 微缩之死](https://newsletter.semianalysis.com/p/tsmcs-3nm-conundrum-does-it-even?utm_source=publication-search)影响最大的公司：Cerebras 的核心卖点就是 SRAM，且 50% 的晶圆面积用于 SRAM。这已经体现在他们的路线图上。采用台积电 16nm 的 WSE-1 出货时带 18 GB SRAM；7nm 的 WSE-2 跳到 40 GB，代际提升 2.2 倍，尚属体面。5nm 的 WSE-3 却只推进到 44 GB。整整一个制程节点过渡只增长了 10%，而逻辑晶体管数量增长了约 50%。

![](https://substack-post-media.s3.amazonaws.com/public/images/9205200d-032e-4542-bbbd-543f893a4d19_1215x420.png)
*来源：SemiAnalysis、TSMC*

展望未来，情况只会更糟。可以看到，在 5nm（WSE-3 目前采用的制程）之后，SRAM 微缩基本彻底停滞。最常见的 3nm 版本 N3E 相对 N5 的 SRAM 面积缩小为零，而且 N2 及以后仍将如此。如今 Cerebras 增加 SRAM 容量的唯一途径，就是增加分配给 SRAM 的晶圆面积、牺牲计算面积。当芯片本身就是晶圆尺寸时，这是一道严格的取舍。这就是为什么下一代 CS-4 系统仍将使用基于 N5 的同款 WSE-3，只是功率更高以支撑更高的时钟频率和算力，SRAM 容量则原地踏步。

相比之下，这对 Groq 没那么致命，因为他们可以在 Z 方向扩展：利用混合键合叠加额外的 SRAM 小芯片，大幅扩展单封装 SRAM 容量，这已列入 Nvidia Groq LP40 的路线图。

合乎逻辑的路径是 Cerebras 如法炮制：晶圆对晶圆键合另一片晶圆，扩展每系统的 SRAM 和/或算力。Cerebras 正认真探索这一方向，并已展示将 DRAM 晶圆混合键合到 WSE 上以增加快速内存容量的概念。然而，考虑到一系列热-机械与键合波（bond-wave）挑战，其时间表和技术可行性令我们担忧。是的，晶圆对晶圆键合是成熟工艺，但整片晶圆作为一颗整体芯片缝合在一起的情况除外。Cerebras 过去曾克服过这类挑战，今后也需要持续创新。

### 孤岛问题——带宽即几何

尽管存在 SRAM 微缩问题，WSE 在单片硅上交付的计算与 SRAM 量仍碾压其他芯片。接下来是最大的取舍：网络。如前所述，每片 WSE 仅有 1.2 Tb/s（150GB/s）的封装外带宽。与普通加速器相比这已经很低，相对于 WSE 的算力则尤其低。不，这并不是因为 Cerebras 的架构师忽视了 I/O 对 AI 计算的重要性、忘了多加 SerDes，这只是晶圆级芯片与生俱来的必然取舍。

相比之下，NVIDIA 将量产的每颗 Groq LP30 都包含 96 条 112G SerDes 通道。也就是说，一颗小得多的芯片拥有进出 9.6 Tb/s 的管道。显然，它已为 [Jensen 今年 GTC 上首次亮相](https://newsletter.semianalysis.com/p/nvidia-the-inference-kingdom-expands)的 PDD + AFD 推理架构做好了准备。

![](https://substack-post-media.s3.amazonaws.com/public/images/02ec97bf-9d54-4d27-aea2-f77535bcc42e_2452x338.png)
*来源：SemiAnalysis 估算*

那为什么要做带宽取舍？按当前 150 GB/s（1.2 Tb/s）的晶圆外带宽算，每毫米边缘只有 0.17 GB/s，而 Nvidia 的片外 I/O 密度是它的 130 倍！

![](https://substack-post-media.s3.amazonaws.com/public/images/dcbbc4ef-7b2c-432c-9334-a9407a926a65_1880x436.png)
*来源：SemiAnalysis、Cerebras、Nvidia*

Cerebras「海岸线」密度的缺失，根源在于晶圆级架构与光罩步进问题。WSE 一次曝光一个光罩场，把同一光罩图形以 84 裸片阵列（WSE-3 上为 12 列 × 7 行）平铺在整个晶圆上。要让跨切割道互连正常工作，每一次光罩曝光都必须完全相同——相同的逻辑、相同的内存、相同的走线、相同的位置。正因如此，片上 2D mesh 网络才能均匀地跨越裸片边界延伸：每颗裸片的东边缘以匹配的引脚分配连接到邻居的西边缘。

这种一致性要求没有商量余地，对 I/O 而言后果严酷。你不能让一个光罩场专用于 PHY，而其余 83 个光罩场做计算。每个光罩场都必须是同一个光罩。所以，如果想在晶圆边缘获得更多 SerDes 通道，就必须在*每一个*光罩场里为 SerDes 花费面积，而不只是外围那些。这些 PHY 大多会位于晶圆中部，接触不到外部世界，无所事事。你要为困死在晶圆内部的 I/O 支付全额硅成本。

另一种方案是只在外围光罩场放 PHY，但那需要非均匀的步进图形，从工艺角度看不可行。那需要在已部分曝光的晶圆上更换光罩，会引入无法承受的工艺风险与复杂度，尤其考虑到所有光罩场需要彼此缝合，而这会破坏让晶圆级设计得以成立的跨切割道互连（也就是我们前文所称的「纵向扩展网络」）。

即便 Cerebras 接受困死的硅、在任何地方都为 PHY 烧掉面积，他们还会撞上第三个约束：片上数据流阻塞。推理期间，片上 2D mesh 网络在核心之间承载激活值、权重和梯度（这也是我们称之为纵向扩展网络的原因）。每个放置在光罩场内部的 PHY 模块都是 mesh 上的一个洞，一块计算与走线都无法存在的区域。PHY 很大（在 5nm 下高速 SerDes 每个 typically 1–3 mm²，包括不随逻辑等比例微缩的模拟电路），而且出于供电与电磁干扰（EMI）考量，其模拟电路对相邻数字逻辑不友好，需要隔离保护区。把 PHY 放在晶圆中部，意味着 2D mesh 网络必须绕行该区域，增加光罩场间延迟并降低总带宽。这种过量绕线一旦太多，就会违背走晶圆级路线的初衷，因为晶圆级的全部意义就是跨瓦片的快速、低功耗数据流。

总结：让晶圆级成为可能的均匀平铺（一个光罩图形、一个 mesh 网络），恰恰是增加 I/O 带宽如此困难的原因。Cerebras 想必正在寻找绕开这一限制的方法。

我们刚才描述的许多问题都源于电学领域数据搬运的现实，而光 I/O 可以绕开这些问题。Cerebras 正在研发的方案（这也再次证明 Cerebras 意识到了问题）是混合键合到 WSE 上的光子互连晶圆。正如用额外的 DRAM 晶圆解决内存约束一样，带宽约束也在用另一片晶圆来解决。

Cerebras 声称，就 LLM 推理而言他们并不需要更多带宽，大力投入混合键合晶圆级光 I/O 只是为了帮助他们的老派 HPC 客户。这些 HPC 客户在 NVIDIA 把 GPU 上的原生 FP64 硬件削减到基本为零之后，实际上已被抛弃。Cerebras 把资金全部激进地再投入到登月式研发而非股票回购，这一点很棒。对于有大量研发方向需要再投入的公司来说，回购并非好主意——例如，AMD 上季度做了约 $2.21 亿回购，但内部多个 AMD 团队至今仍缺乏互联 GPU 集群用于开发。

![](https://substack-post-media.s3.amazonaws.com/public/images/e4b58b10-9df0-4411-8773-dbf9d03feb9d_2350x1371.png)
*Cerebras 的光子晶圆概念。来源：SemiAnalysis、Cerebras*

这让数据可以沿 z 轴进出晶圆，而不必经由边缘。开发这片光子晶圆的光子学合作伙伴是 Ranovus。这再次引出了晶圆级硅的 WoW（晶圆对晶圆）混合键合问题。光学组件对温度敏感（不能太热也不能太冷），而它将被直接夹在一片高热的晶圆上。最后，还有光纤必须与晶圆完美耦合这一现实难题。这个问题即便在传统 CPO 的光引擎层面都还在摸索，更别说晶圆级的东西了。

把这一切记在心里，我们来看看该架构如何塑造推理工作负载。

#### 流水线并行是被迫的

我们已经强调过的、在任何推理部署中使用 Cerebras 的关键担忧之一，就是模型已经变得有多大。无论是总参数量（例如 DeepSeek V4 总参数达 1.6T），还是 KV 缓存（256k 上下文已成常态，DeepSeek V4 更首发 1M 上下文）。

WSE-3 单片 44GB 的有限 SRAM 容量与低 I/O 带宽相结合，导致高效服务这一规模的模型面临挑战。

每台 CS-3 只有 12x100GbE 的 I/O 带宽——整片晶圆约 150 GB/s。这只有 Blackwell 经 NVLink5 每 GPU 900 GB/s 纵向扩展带宽的六分之一，比 HBM 带宽低一个数量级。

正是这一带宽约束，让 Cerebras 难以服务更大参数规模的模型。任何要用到的大张量都必须驻留在晶圆上；I/O 这么少，流式进出晶圆是不可能的。同样，任何需要在每层进行高带宽集合通信的分片策略也被彻底排除。

唯一现实的选择是流水线并行：按层把模型切分到多片晶圆上，只在各级之间传输激活值，依据是激活值相对权重很小。这降低了网络需求，并让吃容量的组件（权重，以及部分 KV 缓存）保持静止，而不用在晶圆上/下搬运。例如，Cerebras 把 Llama3 70B 分片到 4 片 WSE-3 上，只在每片晶圆之间传输激活值，稳稳保持在可用的 1.2Tbps I/O 之内。

随着承载模型所用的晶圆数量增加，要扩大规模就必须应对几个因素。第一，**流水线气泡（pipeline bubble）**：要让 N 个流水线级保持忙碌，至少需要 N 个在途微批（microbatch）。4 级配置需要约 4 个在途微批；16 级配置需要约 16 个。第二，**每个在途微批都携带自己的 KV 缓存**，而在 Cerebras 上，这些 KV 缓存必须与权重挤在同一片 44GB 的片上 SRAM 里，而后者已大部分被权重吃掉。即便借助 DeepSeek V4 等新模型高度压缩的 KV，SRAM 容量够了，KV 缓存进出晶圆的传输时间仍然相当大。此外，模型规模越大，承载权重所需的晶圆数就越多，晶圆→晶圆激活传输延迟叠加进解码时间的次数也就越多。

总而言之，如今生产环境中晶圆的使用方式基本上违背了晶圆的全部初心。晶圆的全部意义就在于以小批处理跑得飞快！

## 算一笔账

让我们用几个开源模型架构做些餐巾纸背面的粗略计算，以更好理解不同模型如何映射到 Cerebras 的 SRAM 占用。下面是几个模型占用空间的粗略数字。

![](https://substack-post-media.s3.amazonaws.com/public/images/5eb9fe21-ec10-401e-b0d1-05655eb60961_1710x360.jpeg)
*来源：Llama、DeepSeek、OpenAI、SemiAnalysis*

再来看结合 WSE-3 规格的一些粗略数字。我们这里做了一些假设，包括传输将用满 12x100Gbps。

![](https://substack-post-media.s3.amazonaws.com/public/images/fadd60f2-e620-4a7b-98f6-91d456a5f1f9_1210x357.jpeg)
*来源：Llama、DeepSeek、OpenAI、SemiAnalysis*

这里我们定义的存储模型权重所需的最少晶圆数，是严格沿层边界分片的结果，且不包含存储 KV 缓存的空间。实践中可能会用更多晶圆，为 KV 缓存腾出更多空间。激活传输时间未计入，因为激活值实在太小，其传输将受限于 I/O 路径上的传播时间。

从表中可以清楚看到，DeepSeek 等近期发表的 KV 缓存压缩技术，或许能显著缓解 Cerebras 在长上下文服务上的困难。但 I/O 缓慢的问题并不会完全消失。首先，KV 在片上/片下的传输时间仍高达数毫秒，既影响 TTFT（首 token 时间），又因 KV 缓存存储与传输相关的批处理、流水线和延迟隐藏问题而更难实现高利用率。其次，激活传输的固定 I/O 延迟，必须按承载一个模型实例所用晶圆数的比例支付。这是 TPOT（每 token 时间）中的一项固定成本，随承载模型的晶圆数线性增长。

关键结论是：Cerebras 虽快，却要为数据进出晶圆支付高昂的延迟成本，因此其成本性能比（或每焦耳性能）将取决于他们能隐藏或最小化多少这类延迟。实践难度的线索也许体现在 Cerebras 推理云的模型产品上。最大的量产模型是 GPT-OSS，总参数仅 120B。预览版模型里有更大的，但顶格也就是 355B（GLM 4.7）。作为参照，据 Elon 透露，Sonnet 和 Opus 的参数分别为 1T 和 5T。值得注意的是，曾经流行的 Llama 70B 和 405B 模型也已被弃用，原因可能在于服务它们的经济性。

![](https://substack-post-media.s3.amazonaws.com/public/images/9f03f0ff-eee5-49bc-bc10-7534fc566704_2432x872.png)
*来源：Cerebras、Llama、OpenAI、DeepSeek、Llama、Qwen、SemiAnalysis*

同样值得强调的是，2025 年最受欢迎的两款前沿开源模型 DeepSeek V3 和 Kimi K2，从未在公开的 Cerebras 云上提供过。尽管 DeepSeek V3 因采用多头潜在注意力（MLA）而大幅缩减了 KV 缓存大小，本应拥有比 Llama 3 405B 更好的服务经济性。

话虽如此，我们上面的分析表明，更新的 DeepSeek V4 Pro 可以有与 Llama 405B（他们已在 Cerebras 云上服务过）相似的部署形态，且 KV 缓存小得多。因此，凭借现代 KV 缓存压缩技术和足够的并发度，即便对于 1T+ 的大模型，Cerebras 也可能确实颇具吸引力。

## Cerebras 与 OpenAI 的交易

OpenAI 在 Cerebras 的未来中扮演着巨大角色。它既是公司的有担保贷款方，又是其最大的认股权证持有人，还是其 $24.6B 在手订单（backlog）几乎全部的来源。OpenAI 对 Cerebras 的财务利益绑定，意味着 Cerebras 的命运通过三个同向联动的机制与单一交易对手捆在一起。如果这段关系成功：贷款将以交付算力而非现金偿还（按产能偿还部分的 6% 应计利息获豁免），认股权证归属并统一双方激励，营收扩张至数十亿美元量级。按完全摊薄计算，OpenAI 最多可持有 Cerebras 12% 的股份（不包括任何新发行与增发）。

具体细节如下：

> · 2025 年 12 月，Cerebras 与 OpenAI 签署了主关系协议（Master Relationship Agreement，MRA），OpenAI 承诺购买 750MW 的 AI 推理算力，2026–2028 年间分批部署，每批期限 3–4 年、可延长至五年。OpenAI 还持有一项额外购买 1.25GW 的选择权（而非义务），使总潜在规模达到 2GW。S-1 文件披露，截至 2025 年 12 月 31 日，剩余履约义务为 $24.6B。更重要的是，转嫁成本（数据中心租金、电费、租赁物改良、安保）由 OpenAI 报销，并按总额法确认为营收。
>
> · OpenAI 还通过一张年息 6% 的有担保本票，向 Cerebras 提供了 $1B 营运资金贷款。若 Cerebras 通过交付 MRA 项下的算力或硬件来偿还，利息可获豁免。还款计划为三年内等额分期摊还，自初始 250MW 的最后一批交付后开始。若 MRA 因 OpenAI 自身重大违约（未补救）以外的原因终止，Cerebras 可能须立即偿付全部未偿余额加应计利息。OpenAI 还保留指示托管银行停止遵循 Cerebras 资金部署指令、改由其直接控制资金处置的权利。
>
> · 与 MRA 同步，Cerebras 向 OpenAI 发行了一份认股权证，涉及 33,445,026 股 N 类（无投票权）普通股，行权价为每股 $0.00001，实际上等于免费。该权证分三个结构上不同的批次归属：4,459,337 股在 2026 年 1 月收到 $10 亿营运资金贷款时立即归属；5,574,171 股在 Cerebras 市值达到 $400 亿或 OAI 达成 MRA 项下指定费用支付里程碑（以较早者为准）时归属；其余 23,411,518 股在与产能交付挂钩的子批次中归属，分为*承诺产能*（Committed Capacity，绑定 MRA 中已有的确定交付日期）和*额外产能*（Additional Capacity，仅在 OAI 行权将交易扩大至全额 2GW 时才归属）。根据 S-1 文件，Cerebras 评估认为营运资金贷款批次、市值/支付门槛批次和承诺产能子批次归属「很可能」发生，而额外产能子批次「不太可能」（即 2GW 扩容尚未计入基准情形）。OAI 还持有随时要求注册权（demand registration rights），即可随时强制 Cerebras 为这些股份办理公开转售注册。该权证于 2035 年 12 月 24 日到期，或在 MRA 项下不再存续任何有约束力的承诺或付款后的五个工作日到期。
>
> · 根据 ASC 505-50，给予客户的股权被作为冲减营收（contra-revenue）在商业协议存续期内确认，而非在归属时、也非按市场价值确认。该数字锁定于授予日公允价值，无论股票日后在何价位交易。根据 S-1 文件，Cerebras 对权证的估值为截至 2025 年 12 月 31 日每股 $82.02，这可作为 OpenAI 交易授予日公允价值的有用代理。将每股 $82.02 应用于全部约 33.4M 股，得到约 $27.4 亿的理论最大冲减营收，约合 OpenAI 预期营收的 10%。我们假设已披露的 $24.6bn backlog 为扣除权证冲减营收后的净值。但现实中，只有「很可能」的批次按滑动比例计入冲减营收：营运资金贷款批次（约 $3.66 亿，2026 年 1 月已归属）、市值/支付门槛批次（约 $4.57 亿）和承诺产能子批次（规模未披露）。额外产能子批次只有在 OAI 行使 2GW 扩容选择权时（且仅在此时），才通过累计追补调整计入冲减营收。

尽管 Cerebras 基本错过了新兴 GPU 云（neocloud）的繁荣，OpenAI 二月发布的 GPT-5.3-Codex-Spark（一个采用 gpt-oss-120B 架构、从真正的 5.3 Codex 蒸馏而来的模型）正在扭转局面。Spark 在 Cerebras 上运行速度高达 2,000 tok/秒/用户，并促成两家公司宣布长期合作协议，推动其 IPO 前景（以及 sama 持股的价值）节节走高。

![](https://substack-post-media.s3.amazonaws.com/public/images/ec386635-41c7-4cf8-8055-c1ac405f4f9f_1233x521.png)
*来源：SemiAnalysis Tokenomics 仪表盘*

如今 Cerebras 的芯片在经济上只能服务相对较小的模型——至少从公开可见的产品来看是这样。例如 [GPT-5.3-Codex-Spark](https://openai.com/index/introducing-gpt-5-3-codex-spark/) 与完整版 GPT-5.3-Codex 完全不是一回事；它是在 GPT-5.3-codex 轨迹上微调的 gpt-oss-120b。换言之，这是一个缩小逾 10 倍的蒸馏模型。

虽然 GPT-5.3-Codex-Spark 非常快，但其 token 今天的价值恐怕不到 $10B。若 OpenAI 要在现代智能体工作负载模式下运行任何总参数超过 1T、上下文窗口 1M 的模型，他们将不得不在成本上接受重大折让（并通过以显著溢价出售这些 token 来收回成本），而且我们预计实际性能将低于 1000 tok/秒的交互速度。另一方面，算法进步必然会让小模型更聪明。距离在 120B 规格封装下达到 GPT 5.5 水平的智能，我们可能已不到一年。

如前所述，我们的许多工程师曾愿意放弃 Opus 4.7 的前沿智能，换取 Opus 4.6 fast 的更快 token。有了 GPT-5.5，OpenAI 终于有了 Opus 4.5 水平的模型。一年之后，即便真正的刀锋前沿已远远超越，人们还愿意为 GPT-5.5 水平的极速 token 付费吗？有史以来第一次，我们认为答案可能是肯定的。虽然首批 750MW 已经锁定，但如果 OAI 选择拿下全额 2GW 甚至更多，Cerebras 还有大得多的上行空间。而这一切都取决于他们能塞进 Cerebras 硬件的模型质量。

在付费墙之后，我们将深入剖析 OAI 交易对 Cerebras 的盈利能力，以及主要的执行风险——Cerebras 在落实数据中心（DC）产能方面进展到了哪一步。
