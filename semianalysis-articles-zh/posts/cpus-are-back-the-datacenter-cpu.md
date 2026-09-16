---
title: "CPU 强势回归：2026 年数据中心 CPU 格局"
title_en: "CPUs are Back: The Datacenter CPU Landscape in 2026"
subtitle: "RL 与智能体应用、上下文内存存储、DRAM 价格影响、CPU 互连演进、AMD Venice、Verano、Florence，Intel Diamond Rapids、Coral Rapids，Arm Phoenix + Venom、Graviton 5、Axion"
date: 2026-02-09
source: https://newsletter.semianalysis.com/p/cpus-are-back-the-datacenter-cpu
crawled: 2026-09-15
authors: ["Gerald Wong", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# CPU 强势回归：2026 年数据中心 CPU 格局

> 原文：[CPUs are Back: The Datacenter CPU Landscape in 2026](https://newsletter.semianalysis.com/p/cpus-are-back-the-datacenter-cpu) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**RL 与智能体应用、上下文内存存储、DRAM 价格影响、CPU 互连演进、AMD Venice、Verano、Florence，Intel Diamond Rapids、Coral Rapids，Arm Phoenix + Venom、Graviton 5、Axion**

![](https://substack-post-media.s3.amazonaws.com/public/images/3f9507d8-140b-4db8-9fd6-2ac28050a1ea_2016x1344.png)

2023 年以来，数据中心的故事很简单：GPU 和网络为王。AI 训练与推理的到来及其随后的爆发，把计算需求从 CPU 身上转移了出去。这意味着，作为服务器 CPU 主要供应商的英特尔（Intel）没能搭上数据中心建设与支出浪潮的顺风车。当超大规模云厂商和新兴 GPU 云（neocloud）把重心放在 GPU 和数据中心基础设施上时，服务器 CPU 营收一直相对停滞。

与此同时，这些超大规模云厂商还在为自家云计算服务打造自研的 ARM 架构数据中心 CPU，把一块可观的可服务市场对英特尔关上了门。而在自家的 x86 地盘上，英特尔疲软的执行力以及相对 AMD 缺乏竞争力的性能，也进一步侵蚀了市场份额。由于拿不出有竞争力的 AI 加速器产品，当行业其余玩家大快朵颐时，英特尔只能原地踩水。

过去 6 个月里，这一切发生了巨大变化。我们已在[核心研究（Core Research）](https://semianalysis.com/core-research/)和 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)中发布多篇关于 CPU 需求飙升的报告。我们展示并建模的主要驱动力，是强化学习（RL）和氛围编程（vibe coding）对 CPU 的惊人需求。我们还报道了多家厂商与 AI 实验室达成的大型 CPU 云协议，并对部署了多少颗、哪些类型的 CPU 建有模型。

![](https://substack-post-media.s3.amazonaws.com/public/images/9c9e56be-fcab-4b4a-9a66-0ead1858e8d9_1648x1629.png)
*英特尔 2025 年第四季度 DCAI 营收。来源：Intel*

不过，英特尔近期的股价回升以及 2025 年下半年需求信号的变化表明，CPU 重新变得重要起来。在最新的第四季度财报中，英特尔看到 2025 年底数据中心 CPU 需求意外上扬，因此上调 2026 年代工工具方面的资本开支指引，并把晶圆投片从 PC 优先转向服务器，以缓解服务这一新需求时的供应紧张。这标志着 CPU 在数据中心角色的拐点——AI 模型训练与推理正在更密集地使用 CPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/066448fc-f72e-4159-aa67-e0192e2ff2ea_3023x1461.png)
*数据中心 CPU 核心数趋势。来源：SemiAnalysis 估算*

2026 年是数据中心 CPU 令人兴奋的一年：在需求暴涨之际，各家厂商都有许多新世代产品在今年发布。因此，本文旨在描绘 2026 年的 CPU 格局。我们会先打好基础，回顾数据中心 CPU 的历史和不断演进的需求驱动力，并深入解析英特尔和 AMD 多年来的数据中心 CPU 架构变迁。

随后我们聚焦 2026 年的 CPU，全面拆解 Intel 的 Clearwater Forest、Diamond Rapids 和 AMD 的 Venice，探讨它们在设计上有趣的趋同（与分歧），讨论性能差异，并预览我们的 CPU 成本分析。

接下来，我们详述 ARM 阵营的竞争，包括 NVIDIA 的 Grace 与 Vera、Amazon 的 Graviton 系列、Microsoft 的 Cobalt、Google 的 Axion 系列 CPU，Ampere Computing 的商用 ARM 芯片之路及其被软银（Softbank）收购，ARM 自家的 Phoenix CPU 设计，并审视华为自研鲲鹏（Kunpeng）CPU 的努力。

为订阅用户，我们提供截至 2028 年的数据中心 CPU 路线图，并详述 AMD、Intel、ARM 和 Qualcomm 2026 年以后的数据中心 CPU。随后我们展望数据中心 CPU 的未来，讨论 DRAM 短缺的影响、NVIDIA Bluefield-4 上下文内存存储（Context Memory Storage）平台对通用 CPU 前景意味着什么，以及未来 CPU 市场和 CPU 设计中值得关注的关键趋势。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

# 数据中心 CPU 的角色与演进

## PC 时代

![](https://substack-post-media.s3.amazonaws.com/public/images/91d101af-061a-4c19-8b95-81be8c05e26f_2718x1849.png)
*Intel Pentium Pro。来源：Intel*

现代意义上的数据中心 CPU 可以追溯到 1990 年代，此前十年个人电脑大获成功，把基础计算带进了家庭。随着 PC 处理能力伴随 Intel 的 i386、i486 和 Pentium 世代不断增强，许多原本由 DEC、IBM 等公司的高级工作站和大型主机完成的计算任务，转而在 PC 上以低得多的成本完成。为回应这种对更高性能"大型主机替代品"的需求，Intel 开始发布性能更强、缓存更大、价格更高的 PC 处理器变种，起点是 1995 年的 Pentium Pro——它将多颗 L2 缓存裸片（die）与 CPU 共同封装在多芯片模块（MCM）中。随后 Xeon 品牌于 1998 年跟进，Pentium II Xeon 同样在 CPU 处理器插槽中加入了多颗 L2 缓存裸片。大型主机至今仍以 IBM Z 系列的形式延续，用于银行交易核验等场景，但它们仍是市场的一个小众角落，本文不再展开。

## 互联网泡沫（Dot Com）时代

2000 年代带来了互联网时代：Web 2.0、电子邮件、电子商务、Google 搜索、配备 3G 宽带数据的智能手机相继涌现，万物上线催生了对数据中心 CPU 承载全球互联网流量的需求。数据中心 CPU 成长为一个数十亿美元的细分市场。在设计层面，随着 Dennard 缩放定律终结、GHz 大战落幕，重心转向多核 CPU 和更高的集成度。AMD 把内存控制器集成进 CPU 芯片，高速 IO（PCIe）也直接从 CPU 引出。多核 CPU 尤其适合数据中心工作负载，因为许多任务可以在不同核心上并行运行。

我们将在下文的互连一节详述这些核心如何连接的演进。同一时期，AMD 和 Intel 都引入了同步多线程（SMT），把一个核心划分为两个可独立运行、共享核心大部分资源的逻辑线程，进一步提升了可并行化数据中心工作负载的性能。追求更高性能的用户会转向多路（Multi-socket）CPU 服务器，Intel 的快速通道互连（QPI）和 AMD Opteron CPU 中的 HyperTransport 直连架构为每台服务器最多 8 个插槽之间提供一致性互连。

## 虚拟化与云计算超大规模时代

下一个重大拐点伴随 2000 年代末的云计算而来，并成为整个 2010 年代数据中心 CPU 销量的主要增长驱动力。就像今天 GPU 新兴云（neocloud）的运作方式一样，当客户把资本开支（capex）换成运营开支（opex），计算资源开始向 Amazon Web Services（AWS）等公有云提供商和超大规模云厂商集中。在大衰退的影响下，许多企业已买不起也养不起自购的服务器来运行其软件与服务。

云计算提供了一种可口得多的"按用付费"商业模式：租用计算实例、在第三方硬件上运行工作负载，支出得以随时间变化的使用量动态调整。这种可扩展性比自购服务器更有利——后者必须时刻满负荷利用才能最大化 ROI。云还催生了更精简的服务，例如 AWS Lambda 之类的无服务器计算，可自动把软件分配到计算资源上，免去客户在运行特定任务前决定该启动多少实例的烦恼。几乎一切都在幕后由云厂商打理，云把计算变成了大宗商品。

![](https://substack-post-media.s3.amazonaws.com/public/images/5e31aa5b-fd56-4674-9895-2576e448e40f_1479x1986.png)
*Pat Gelsinger，VMware CEO（2012–2021），Intel CEO（2021–2024）。来源：X @PGelsinger*

安全且资源高效的云能够运转的关键，在于 CPU 硬件虚拟化。本质上，虚拟化允许单颗 CPU 运行多个相互独立且安全的虚拟机（VM）实例，并通过 VMware ESXi 等虚拟机管理程序（hypervisor）来编排。多核 CPU 可以被划分，使每个 VM 被分配到单个核心或逻辑线程上；hypervisor 还能把实例迁移到不同的核心、插槽，或经由网络迁移到其他服务器，以优化 CPU 稼动率，同时保证数据与指令不被同一颗 CPU 上运行的其他实例窥探。

云对虚拟化的需求，加上 CPU 设计者用 SMT 提升性能，最终在 2018 年被 Spectre 和 Meltdown 漏洞所利用。当两个实例运行在同一物理核心的两个线程上时，攻击者有可能利用 CPU 核心的分支预测功能窥探并拼凑出另一个线程的数据——分支预测是一种提升性能的技术，会在运行中的程序之前猜测、预取并执行指令，让 CPU 保持忙碌。云的安全性可能因此失守，云厂商纷纷紧急禁用 SMT 以封堵这一攻击路径。尽管有补丁和硬件修复，失去 SMT 后高达 30% 的性能损失一直困扰着 Intel，并在日后不合时宜的设计决策中显现，下文将详述。

## AI GPU 与 CPU 整合时代

新冠（COVID）热潮带来了多得多的 Zoom 通话、电子商务和线上时间，推高互联网流量，数据中心 CPU 增长随后达到历史峰值。在 2022 年 11 月 ChatGPT 发布前的五年里，Intel 向云和企业数据中心出货了超过 1 亿颗 Xeon Scalable CPU。

从那时起，AI 模型训练和推理服务颠覆了 CPU 在数据中心的角色，引发 CPU 部署与设计策略的广泛变化。AI 模型计算需要大量矩阵乘法，这种运算极易并行化，并可在 GPU 上大规模执行——GPU 拥有庞大的向量单元阵列，最初用于为游戏和可视化渲染 3D 图形。

虽然加速器节点仍然使用主机 CPU，但高度结构化、相对简单的计算需求并不能发挥 CPU 运行分支密集、延迟敏感代码的能力。而且与 GPU 上数以千计的向量单元相比，CPU 只有几十个，性能和效率相差 100-1000 倍，尤其是当专为 AI 设计的 GPU 又加入专注矩阵乘法的张量核心（Tensor Core）之后。尽管 Intel 通过翻倍 AVX512 端口和加入专用 AMX 加速引擎来增强向量与矩阵支持，CPU 还是被贬到了数据中心的配角位置。然而，互联网仍需有人服务，而数据中心的功率又被优先分给 GPU 计算。于是，CPU 随时代演进，分化为两类。

### 头节点（Head Node）

头节点 CPU 的职责是管理所挂载的 GPU 并持续为其喂数据。需要高单核性能、大缓存以及高带宽内存和 IO，以把尾延迟压到最低。NVIDIA 的 Grace 这类专用设计具备一致性内存访问，让 GPU 可以把 CPU 内存用作模型上下文 KV 缓存的扩展，因此需要极高的 CPU 到 GPU 带宽。对于头节点，每个计算节点通常以 1 颗 CPU 搭配 2 或 4 颗 GPU。例如：

- 每颗 superchip 中 1 颗 Vera CPU 对应 2 颗 Rubin GPU
- 每个计算托盘（compute tray）中 1 颗 Venice CPU 对应 4 颗 MI455X GPU
- 每个计算托盘中 1 颗 Graviton5 CPU 对应 4 颗 Trainium3
- 每节点 2 颗 x86 CPU 对应 8 颗 TPUv7

### 云原生插槽整合（Socket Consolidation）

随着 GPU 吞掉越来越多的数据中心功率预算，尽可能高效地服务互联网其余部分的需求，加速了"云原生"CPU 的开发。目标是以最优效率（每瓦吞吐量）实现单插槽吞吐量和服务的请求数最大化。不是靠增加更多、更新的 CPU 来提升总吞吐量，而是把老旧低效的服务器退役，换成数量少得多、却能满足总吞吐量要求的云原生 CPU——功耗只占一小部分，从而降低运营成本，为更多 GPU 计算腾出功率预算。

![](https://substack-post-media.s3.amazonaws.com/public/images/be59d15e-c167-4a38-b904-c6f6e4efa593_2821x1421.png)
*AMD Turin Dense 7:1 插槽整合。来源：AMD*

10:1 甚至更高的插槽整合比都可以实现。新冠期间云支出高峰购买的数百万台 Intel Cascade Lake 服务器正在退役，换上最新的 AMD 和 Intel CPU——同等性能水平下功耗不到原来的五分之一。

在设计上，这些云原生 CPU 以面积与功耗高效的中型核心堆高核心数，缓存和 IO 能力则少于传统 CPU。Intel 用 Sierra Forest 把 Atom 核心带进数据中心；AMD 的 Bergamo 采用了其 Zen4 核心的一种更省面积、更省电的布局。以能效见长的 ARM 架构设计如 AWS Graviton 大获成功，Ampere Computing 则以 Altra 和 AmpereOne 系列瞄准云原生计算。

## RL 与智能体时代

![](https://substack-post-media.s3.amazonaws.com/public/images/0ad2959c-94f2-4096-a61c-c40e46ee0dff_3092x949.png)
*微软（Microsoft）"Fairwater" 数据中心的 GPU 与 CPU 建筑。来源：Google Earth*

如今，CPU 用量再度加速增长，以支撑头节点之外的 AI 训练与推理。微软为 OpenAI 建设的 "Fairwater" 数据中心已经给出了证据：这里一栋 48MW 的 CPU 与存储建筑支撑着主 295MW GPU 集群。这意味着如今需要数万颗 CPU 来处理和管理 GPU 产生的 PB 级数据——如果没有 AI，本不会有这种使用场景。

AI 计算范式的演进造成了 CPU 使用强度的提升。在预训练和模型微调中，CPU 用于存储、分片（shard）和索引将要喂给 GPU 集群做矩阵乘法的数据。CPU 也用于多模态模型的图像与视频解码，不过更多固定功能的媒体加速正被直接集成到 GPU 中。

![](https://substack-post-media.s3.amazonaws.com/public/images/4658580c-c8cb-4753-b21a-a39831d9a3a8_2052x1554.png)
*强化学习训练循环。RL 环境（绿色）中使用的 CPU。来源：SemiAnalysis*

使用强化学习技术来改进模型，进一步推高了 CPU 需求。根据我们对强化学习的深度解析，在 RL 训练循环中，"RL 环境"需要执行模型生成的动作并计算相应的奖励。在编程和数学等领域要做到这一点，需要大量 CPU 并行执行代码编译、验证、解释和工具调用。CPU 还深度参与复杂物理仿真，以及以高精度校验生成的合成数据。因此，为进一步扩展模型而日益复杂的 RL 环境，需要在主 GPU 集群附近部署大型高性能 CPU 集群，让 GPU 保持满负荷、把空闲时间压到最少。训练循环中对 RL 和 CPU 的依赖与日俱增，正在制造一个新的瓶颈：AI 加速器的每瓦性能改进速度远快于 CPU，这意味着 Rubin 这样的未来 GPU 世代可能需要比上文 Fairwater 的 1:6 更高的 CPU 与 GPU 功率配比。

在推理侧，检索增强生成（RAG）模型会搜索并使用互联网，智能体模型会调用工具、查询数据库，它们的兴起大幅增加了服务这些请求所需的通用 CPU 算力。凭借向多个来源发起 API 调用的能力，每个智能体对互联网的使用强度本质上远超人类做简单 Google 搜索的强度。面对互联网流量的这种成倍暴涨，AWS 和 Azure 一方面大规模扩建自家 Graviton 和 Cobalt 系列 CPU，另一方面采购更多 x86 通用服务器。

随着 2026 年推进，对数据中心 CPU 和 DRAM 的需求只会愈发强劲。前沿 AI 实验室的 RL 训练需求正在耗尽 CPU 供应，它们直接与云厂商争夺通用 x86 CPU 服务器来抢产能配给。面对 CPU 库存的意外耗尽，Intel 计划全线上调 Xeon 价格，同时增加设备投入以加强 CPU 生产。AMD 则在持续提升供应能力，以在一个其认为 2026 年将实现"强劲两位数"增长的服务器 CPU 总可服务市场（TAM）中扩张并夺取份额。我们将在下文为订阅用户讨论 2026 年之后 CPU 格局如何演进。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

# 多核 CPU 互连的历史

要理解 2026 年 CPU 的设计变化与设计哲学，我们必须了解多核 CPU 的工作原理，以及核心数增长过程中互连技术的演进。有了多个核心，就需要把它们连接起来。2005 年 Intel 的 Pentium D 和 Xeon Paxville 等早期双核设计只是把两个独立的单核凑在一起，核间通信要经由封装外的前端总线（FSB）连到同样承载内存控制器的北桥芯片。同样在 2005 年，AMD 的 Athlon 64 X2 才算是真正的双核处理器：两个核心与集成内存控制器（IMC）位于同一裸片上，核心之间以及核心与内存、IO 控制器之间的通信，可以直接在芯片内部通过片上 NoC（Network on Chip）数据总线网络完成。

![](https://substack-post-media.s3.amazonaws.com/public/images/3fc1fbd3-39c1-4650-ab74-54f841f233fc_2329x1801.png)
*Intel Tulsa 裸片图（die shot）。来源：Intel，Hot Chips 2006*

Intel 随后的 Tulsa 世代在两个核心之间共享 16MB L3 缓存，起到片上核间数据总线的作用。后文将会看到，当核心数增长到数百个时，这些片上数据总线将成为数据中心 CPU 设计的关键因素。

## 交叉开关（Crossbar）的极限

当设计者试图进一步增加核心数时，他们撞上了这些早期互连的扩展极限。由于追求最低延迟和均匀性，交叉开关（crossbar）设计以全连通（all-to-all）方式使用，即每个核心都与片上其他所有核心有一条专用链路。然而链路数量随核心数急剧增加，复杂度也随之上升。

2 核：1 条连接

4 核：6 条连接

6 核：15 条连接

8 核：28 条连接

大多数设计的实用上限止步于 4 核，更高核心数的处理器靠多芯片模块以及核心对之间共享 L2 缓存和数据总线的双核模块来实现。交叉开关的布线通常做在共享 L3 缓存上方的金属层里，以节省面积。Intel 2008 年的 6 核 Dunnington 使用了三个双核模块，共享 16MB L3。

![](https://substack-post-media.s3.amazonaws.com/public/images/26443b09-cd4f-4635-8189-0a85234e9709_1504x2079.png)
*AMD Opteron Istanbul 6 核裸片。来源：AMD*

AMD 于 2009 年推出 6 核 Istanbul，采用 6 路交叉开关和 6MB L3。2010 年的 12 核 Magny-Cours 使用两颗 6 核裸片，16 核 Interlagos 则由两颗各含四个 Bulldozer 双核模块的裸片组成。

## Intel 的环形总线（Ring Bus）

![](https://substack-post-media.s3.amazonaws.com/public/images/e4c3bb6f-9b4b-47c6-9b22-a50aecc28ea0_2424x1789.png)
*Intel Nehalem-EX 环形互连。来源：Intel，Hot Chips 2009*

为了突破这一极限，Intel 在 2010 年的 Nehalem-EX（Beckton）Xeon 中实现了环形总线架构，把 8 个核心连同集成内存控制器和插槽间 QPI 链路装进单一裸片。环形总线更早曾用于 ATi Radeon GPU 和 IBM Cell 处理器，它把所有节点排成一个环，环上站点（ring stop）集成在各个 L3 缓存切片中，布线位于缓存上方的金属层。缓存代理（Caching Agent）和主代理（Home Agent）负责核心之间的内存窥探以及与内存控制器的一致性。

来自每个环站的核心和 L3 缓存切片的数据排队注入环中，数据每个时钟前进一站，直至目标目的地。这意味着核间访问延迟不再均匀：位于环两侧相对位置的核心，比直接相邻的核心要多等若干时钟周期。为缓解延迟和拥塞，实现了两条反向旋转的环，并根据地址和环负载选择最优行进方向。布线复杂度得到控制后，Intel 在 Nehalem-EX 上把核心数扩展到 8 个，Westmere-EX 达到 10 个。然而，若用单环继续扩展，环会变得过长，导致一致性和延迟问题。

### Ivy Bridge-EX 虚拟环

![](https://substack-post-media.s3.amazonaws.com/public/images/0830e24f-4740-4e69-8707-090b48c6ec4c_2332x1803.png)
*Intel Ivytown 虚拟环。来源：Intel，Hot Chips 2014*

为了在 Ivy Bridge 世代把核心数提升到 15，Intel 不得不在路由拓扑上动脑筋。核心排成三列、每列五个，三条"虚拟环"绕列循环。环站中的交换开关控制沿半环的行进方向，构成"虚拟"三环配置。

### Haswell 与 Broadwell 双环

![](https://substack-post-media.s3.amazonaws.com/public/images/5b1e5413-09bc-46c0-9cd2-64e233a613ab_2987x1679.png)
*Haswell HCC 双环形总线。来源：Intel*

2014 年，Intel 再次更换拓扑：18 核 Haswell HCC 裸片采用两条独立反向旋转的环形总线，由一对双向缓冲交换开关连接。内存控制器分置于两条环上，8 核环还承载 IO 环站。MCC 裸片变体则把单条半环首尾相接。2015 年发布的 Broadwell HCC 用双 12 核环形总线把核心数提升到 24。

把多条环拼接在一起的缺点，是核间和内存访问延迟的波动加大，尤其当一条环上的核心访问另一条环的内存时。这种非统一内存访问（NUMA）对延迟敏感、核间交互频繁的程序性能不利。

为此，Intel 在 BIOS 中提供"Cluster on Die"配置选项，把两条环视为独立处理器。操作系统会把该 CPU 显示为两个 NUMA 节点，各自直接访问一半的本地内存和 L3 缓存。[CoD 模式下的测试](https://old.chipsandcheese.com/2023/11/07/core-to-core-latency-data-on-large-systems/)表明，每条环内部的延迟保持在 50ns 以下，而访问另一条环超过 100ns，可见经过缓冲交换开关的延迟代价。

这些方法虽然帮助 Intel 把核心数提高到 24，但既不优雅也不可扩展。再加第三条环和两组缓冲交换开关会过于复杂、不切实际，并制造出许多 NUMA 簇。要支持更多核心，必须采用新的互连架构。

## Intel 的网格（Mesh）架构

![](https://substack-post-media.s3.amazonaws.com/public/images/216a402f-a60c-42f3-b7e4-00546356b555_3010x1685.png)
*Intel Knights Landing 网格互连。来源：Intel，Hot Chips 2016*

为解决可扩展性问题，Intel 把 2016 年 Xeon Phi "Knights Landing" 处理器采用的网格互连架构，移植到 2017 年的主力 Skylake-X Xeon Scalable CPU，在 XCC 裸片上实现 28 核。虽然核心数相比 Broadwell 提升不大，但这一设计奠定了之后十年核心数扩展的基础。

在网格架构中，核心排成网格阵列，每一列和每一行用半环连接，形成二维网格。每个网格站点可容纳核心和 L3 缓存切片、PCIe IO、IMC 以及加速器。核心之间的路由按环形方式进行，数据先沿垂直方向传输，再水平横穿。缓存代理和主代理连同其窥探过滤器，现在分布到所有环站，以实现全网的内存一致性。

由于采用网格网络且多个内存控制器位于裸片两侧，大规模网格下内存访问和核间延迟会显著波动。与更早的 Cluster on Die 方案类似，Intel 提供了多种聚类模式，把网格切分为象限以实现 Sub-NUMA Clustering（SNC，子 NUMA 聚类），以把每个处理器当作多个插槽、每个 NUMA 节点只有更小的 L3 和内存访问池为代价，降低平均延迟。

在 Knights Landing 中，每个网格站点容纳两个核心，共享一个 L2 缓存。网格为 6 列 × 9 行，顶行和底行主要是 IO 和 MCDRAM。网格网络运行在自己的时钟上，可动态调节网格时钟以省电。Knights Landing 的网格运行在 1.6GHz。

![](https://substack-post-media.s3.amazonaws.com/public/images/fb55424a-5436-4909-83f4-57f750341ca1_1951x1654.png)
*Skylake-SP 网格示意图。来源：Intel*

在 Skylake-X 上，28 个核心排成 6x6 网格，北边是 IO 顶帽（IO cap），两侧各有 2 个 IMC 位点。由于核心更大——增加了更多 L2 缓存并加入 AVX-512 扩展以提升浮点性能——网格阵列反而更小。若再加一行或一列，裸片面积就会超出 26 x 33 mm 的光罩极限。凭借更小的网格和高达 4.5GHz 的 CPU 频率，网格时钟提高到 2.4GHz，实现了与 Broadwell 双环相当的平均延迟。

随后的 Cascade Lake 和 Cooper Lake 处理器变化不大，仍是 28 核布局。顺带一提，为应对 AMD 携 EPYC 重返数据中心，Intel 在 Cascade Lake-AP 中做了 56 核双裸片 MCM，并取消了 Cooper Lake CPX-4 的类似版本。

![](https://substack-post-media.s3.amazonaws.com/public/images/3aeb2086-3dc2-4707-b47a-1b04ce197224_2176x1604.png)
*Ice Lake XCC 40 核网格示意图。来源：Intel*

下一代 Ice Lake 受益于制程从 14nm 微缩到 10nm，核心数得以在 8x7 网格中增加到 40 核——这是光罩极限内的最大值。然而，下一代 Sapphire Rapids 仍将采用同一制程且功能更多。这让 Intel 在如何再次提升核心数的问题上进退两难。

### 跨 EMIB 的解耦网格

![](https://substack-post-media.s3.amazonaws.com/public/images/224c3b3b-2f89-4983-baa8-ba2dfbf79771_2979x1661.png)
*Xeon 走向小芯片（chiplet）的解耦之路。来源：Intel*
![](https://substack-post-media.s3.amazonaws.com/public/images/cd750739-7f96-4cdb-b968-d5fccfcd99c2_2197x1895.png)
*Sapphire Rapids XCC 拓扑。来源：Intel*

Sapphire Rapids 加入了用于矩阵乘法和 AI 的高级矩阵扩展（AMX）引擎，核心面积进一步增大。这意味着单一单片裸片只能容纳 34 核，比 Ice Lake 还退步。要把核心数提升到 60，Intel 别无选择，只能再次把核心拆分到多颗裸片上。但他们想让芯片保持"逻辑上单片"，即处理器的表现和性能与单一裸片完全一致。

于是，Sapphire Rapids 首发了 Intel 的 EMIB 先进封装技术，让网格架构得以跨越多颗裸片。两对镜像的 15 核裸片通过模块化裸片总线（Modular Die Fabric）缝合，在四个象限上构成大得多的 8x12 网格，硅片面积接近 1600 mm2。为应对 PCIe 5.0 吞吐量翻倍和新增数据加速器模块带来的数据流量增长，IO 需要双排网格站点。

由于网格横跨多颗裸片、规模大得多，平均核间延迟从 Skylake 的 47ns 恶化到 59ns。为了尽可能少用网格网络，Intel 把每核私有 L2 缓存加大到 2MB，使片上 L2 缓存超过 L3 缓存（120MB 对 112.5MB）。同时也更推荐启用 Sub-NUMA Clustering（SNC），把每颗裸片当作独立象限。

尽管这是 Intel 首次转向小芯片（chiplet），Sapphire Rapids 却因多年延期和无数次修订而声名狼藉。或许由于让网格跨 EMIB 正常工作的性能问题，或是其他执行问题，最终版本一路改到 E5 步进，才于 2023 年初发布。原路线图定的是 2021 年。

2023 年底随后的 Emerald Rapids 更新保持了相同的核心架构和制程，但裸片数减到 2 颗。由于花在 EMIB 裸片间链路上的硅面积减少，Intel 得以把核心数从 60 提高到 66（出于良率最多启用 64 核），同时把 L3 缓存近乎翻了三倍，达到 320MB。关于这些设计决策，我们此前有更多论述。

### Xeon 6 上的异构解耦

![](https://substack-post-media.s3.amazonaws.com/public/images/b7e1a665-9bf8-4dd2-873a-4de31bd70c7e_2802x1562.png)
*Xeon 6 平台特性。来源：Intel*
![](https://substack-post-media.s3.amazonaws.com/public/images/b4873f4f-99fa-4a9f-9389-b3c1a35f46c6_2510x1047.png)
*Xeon 6 计算裸片与 IO 裸片示意图。来源：Intel*

突破光罩极限之外，转向多裸片小芯片设计的另一个好处，是可以混合搭配裸片、在不同变种和配置间共享设计。对于 2024 年的下一代 Xeon 6 平台，Intel 选择了异构解耦，把 IO 与核心、内存分离开来。这样 IO 裸片可以留在较老的 Intel 7 制程，而计算裸片升级到 Intel 3。Intel 由此得以复用从 Sapphire Rapids 开发的 IO IP，同时节省成本——因为 IO 从更先进制程获得的收益没那么大。与此同时，计算裸片可以在 P 核 Granite Rapids 和 E 核 Sierra Forest 配置之间混搭：旗舰 Granite Rapids-AP Xeon 6900P 系列最多 3 颗计算裸片，在 5 颗裸片上构成 10x19 的大型网格，连接 132 核，出于良率最多启用 128 核。

![](https://substack-post-media.s3.amazonaws.com/public/images/f31bc7da-3964-4e1a-a65c-22d17a7473d4_3102x2196.png)
*Xeon 6 计算裸片拼图。左上起顺时针：UCC 44 核、HCC 50 核、HDCC 152 核、LCC 20 核。来源：Intel，SemiAnalysis 估算*

在 144 核的 Sierra Forest 上，E 核按 4 核一簇分组、共享一个网格站点，排成 8x6 网格，印刷 152 核、最多 144 核可用。虽然 Sierra Forest 是应超大规模云厂商对每核 TCO 更低的"云原生"CPU 的需求而生，但 Intel 已承认其采用有限——超大规模厂商已经在采用 AMD 并自研 ARM 架构 CPU，而 Intel 的传统企业客户对它不感兴趣。结果，双裸片 288 核 Sierra Forest-AP（Xeon 6900E）SKU 未能大规模上市，只以低产量、路线图外的型号存在，服务少数下单的超大规模客户。

### Clearwater Forest 的失败

![](https://substack-post-media.s3.amazonaws.com/public/images/9e7b64d4-593a-4b8e-a26c-3ddba7850e97_2543x2621.png)
*18A 制程上 12 颗 24 核 Clearwater Forest 计算裸片。来源：Intel，SemiAnalysis*

IO 裸片也将在即将推出的 Xeon 6+ Clearwater Forest-AP E 核处理器中复用。计算裸片首发 Intel 的 Foveros Direct 混合键合技术，把 18A 制程的核心裸片堆叠在包含网格、L3 缓存和内存接口的基础裸片之上，把核心数提升到 288。垂直解耦让计算核心得以迁移到最新的 18A 逻辑制程，而扩展性没那么好的网格、缓存和 IO 则留在较老的 Intel 3 制程上。

![](https://substack-post-media.s3.amazonaws.com/public/images/f9fc472b-1964-4d8a-9743-0610dd8a10ba_2966x1415.png)
*Clearwater Forest 性能预测。来源：Intel*

然而，Intel 的执行问题在 Clearwater Forest 上再度浮现，上市时间从 2025 年下半年推迟到 2026 年上半年。Intel 把延误归咎于 Foveros Direct 集成难题——在 Intel 摸索混合键合技术时，由如此复杂的服务器芯片打头阵，出问题并不意外。或许正因如此，垂直解耦互连的带宽相对较低，每个 4 核簇访问基础裸片的 L3 和网格网络只有 35GB/s。

尽管相隔两年、换上新核心微架构、新制程、新先进封装，成本也更高，Intel 展示的 Clearwater Forest 在相同核心数下只比 Sierra Forest 快 17%。混合键合良率偏低导致成本大幅上升，性能增益却如此有限，难怪 Intel 在最新的 2025 年第四季度财报中几乎不提 Clearwater Forest。我们的看法是：Intel 并不想大批量生产这种伤害毛利率的芯片，宁愿把它当作 Foveros Direct 的良率爬坡学习载体。

## AMD 的 Zen 互连架构

![](https://substack-post-media.s3.amazonaws.com/public/images/7520d55a-ba5b-466e-9799-72fe683a1923_2860x1588.png)
*AMD EPYC CPU 世代。来源：AMD*
![](https://substack-post-media.s3.amazonaws.com/public/images/c704a28b-2774-4428-9745-2cfdcf1f1573_2775x1508.png)
*Intel 对 AMD Naples 的批评。来源：Intel*

2017 年，AMD 携 EPYC Naples 7001 系列重返数据中心 CPU 市场，引发不小轰动，Intel 嘲讽该设计是"四颗粘在一起的桌面裸片"、性能忽高忽低。实际上，AMD 规模不大的设计团队必须精打细算，只流片得起一颗裸片，它要同时用于桌面 PC、服务器甚至嵌入式领域，还在同一裸片上集成了 10Gbit 以太网。

![](https://substack-post-media.s3.amazonaws.com/public/images/f6de7f59-7300-4154-aba5-836eae048878_3025x1693.png)
*AMD Zeppelin SoC 架构。来源：AMD，ISSCC 2018*

Naples 采用 4 裸片 MCM，每颗 "Zeppelin" 裸片含 8 核，让 AMD 以 32 核超过 Intel 的 28 核。每颗裸片有 2 个核心复合体（CCX），各含 4 核和 8MB L3，经交叉开关连接。片上的可扩展数据总线（Scalable Data Fabric）负责 CCX 间通信。封装内 Infinity Fabric（IFOP）链路把每颗裸片与封装内其他 3 颗相连，插槽间 Infinity Fabric（IFIS）链路则支持双路设计。Infinity Fabric 实现了裸片间的一致性内存共享，脱胎于 AMD 早期的 HyperTransport 技术。

这种架构意味着没有统一的 L3 缓存，核间延迟差异很大：从一颗裸片上某个 CCX 的核心到另一颗裸片的核心需要多跳。一台典型的双路服务器最终有四种 NUMA 域：CCX 内、CCX 间、MCM 裸片间、插槽间。性能也如实反映了这一点：核间和内存访问很少、高度可并行的任务（如渲染）表现良好，而更依赖核间通信的内存敏感、延迟敏感任务表现糟糕。由于大多数软件也不感知 NUMA，Intel "性能不一致"的批评有了一定道理。

### EPYC Rome 的中心化 IO

![](https://substack-post-media.s3.amazonaws.com/public/images/89034fe0-5221-40fe-9936-7e7e779456d6_2830x1602.png)
*Rome 与 Milan SoC 架构。来源：AMD*

2019 年的 Rome 世代对裸片布局进行了彻底重构，利用异构解耦打造出 64 核产品，把还卡在 28 核的 Intel 远远甩开。8 颗 8 核核心计算裸片（CCD）环绕中央 IO 裸片，后者包含内存和 PCIe 接口；CCD 升级到最新的 TSMC N7 制程，而 IO 裸片留在 GlobalFoundries 的 12nm。CCD 仍由两个 4 核 CCX 组成，但彼此不再直接通信，所有 CCX 间流量都经 IO 裸片路由，信号通过全局内存互连（GMI）链路在封装基板上传输。这意味着 Rome 在功能上呈现为 16 个 4 核 NUMA 节点，好在 NUMA 域只有 2 个。

与之前的 Naples 一样，在 Rome 上创建的 VM 必须控制在 4 核以内，以避免跨裸片通信带来的性能损失。这一问题在 2021 年的 Milan 世代得到解决：转用环形总线架构，把 CCX 规模提升到 8 核，同时复用与 Rome 相同的 IO 裸片。

![](https://substack-post-media.s3.amazonaws.com/public/images/053b0db0-b10d-46be-ab7c-6826eeb1b607_2777x1154.png)
*AMD Turin-Dense。来源：AMD*

尽管最初计划采用先进封装，AMD 在接下来两代仍沿用这一熟悉的设计：2022 年的 Genoa 增加到 12 颗 CCD，2024 年的 Turin 在 128 核 EPYC 9755 上最多 16 颗 CCD，全部环绕在升级了 DDR5 和 PCIe5 接口的中央 IO 裸片周围。

这种小芯片设计的关键优势，是只需一次流片就能实现核心数的可扩展。AMD 只需设计一颗 CCD，通过搭载不同数量的 CCD，就能覆盖整个 SKU 阵容的全部核心数。每颗 CCD 裸片面积小，也有助于良率，并在转向新制程节点时更早上市。这与网格设计形成鲜明对比——后者使用接近光罩极限的大裸片，且每种较小网格的核心数配置都需要单独流片。不同的 CCD 设计也可以在共享同一 IO 裸片和插槽平台的前提下替换，AMD 用紧凑型 Zen 4c 核心打造了 Bergamo，又用 Zen 5c 核心打造 192 核 Turin 变种。我们此前撰文介绍过这种面向高效云计算的新核心变种。解耦还允许做出更小的版本：EPYC 8004 Siena 处理器只用 4 颗 Zen 4c CCD，搭配 6 通道内存平台。

# Intel Diamond Rapids 架构变化

![](https://substack-post-media.s3.amazonaws.com/public/images/73fc256f-03cf-47b4-9ac5-a6240b0c9de0_2786x1606.png)
*Diamond Rapids 概览。来源：HEPiX via @InstLatX64*

乍看之下，Diamond Rapids 几乎就是 AMD 设计的翻版：计算裸片环绕中央 IO 裸片。看来，要把单一网格网络扩展到 Granite Rapids 10x19 之外以继续增加核心数实在太难，这意味着 Intel 终于向多个 NUMA 节点和多个 L3 域低头。4 颗核心构建模块（CBB）裸片夹着中间 2 颗 IO 与内存枢纽（IMH）裸片。

在每颗 CBB 内，32 个基于 Intel 18A-P 的双核模块（DCM）经混合键合安放在包含 L3 缓存和本地网格互连的 Intel 3-PT 基础裸片上。为减少网格站点数量并降低网络流量，每个 DCM 中的两个核心现在共享一个 L2 缓存——让人想起 2008 年的 Dunnington 世代。虽然这意味着 Diamond Rapids 总共有 256 核，但主力 SKU 似乎最多只启用 192 核，更高的核心数推测因良率较低而留给路线图外的订单。

IMH 裸片包含 16 通道 DDR5 内存接口、支持 CXL3 的 PCIe6，以及 Intel 数据路径加速器（QAT、DLB、IAA、DSA）。

有意思的是，裸片间互连似乎不再需要 EMIB 先进封装：封装基板上的长走线把每颗 CBB 裸片连到两颗 IMH 裸片，使每颗 CBB 都能直接访问全部内存和 IO 接口，无需再经一跳到另一颗 IMH。这也保证任意 CBB 间通信最多只需 2 次跨裸片跳数。不过，由于放弃先进封装并把核心分到 4 颗裸片，我们预计跨 CBB 延迟会明显更差，与留在同一裸片内相比延迟差距很大。

![](https://substack-post-media.s3.amazonaws.com/public/images/e49ef13f-5a91-465a-af7e-3caabc9c651a_2942x1627.png)
*Intel 在其 P 核上移除 SMT。来源：Intel*

尽管延迟变糟已经够呛，Diamond Rapids 最严重的问题还是缺少 SMT。Spectre 和 Meltdown 漏洞对 Intel 的冲击在根本上大于 AMD，受此惊吓，其核心设计团队开始设计不带 SMT 的 P 核，从 2024 年客户端 PC 的 Lion Cove 开始。Intel 当时的说辞是，移除 SMT 功能省下的面积可以换来更好的能效，代价是原始吞吐量。对 PC 设计来说这没问题，因为旁边还集成了 E 核来补强多线程性能。

但对数据中心 CPU 而言，最大吞吐量至关重要，这严重拖累了 Diamond Rapids。与现有的 128 核 256 线程 Granite Rapids 相比，我们预计主力 192 核 192 线程的 Diamond Rapids 只快 40% 左右，暴露出 Intel 又一代产品性能低于 AMD。

在一次仓促的调整中，Intel 彻底取消了主流 8 通道 Diamond Rapids-SP 平台，使其出货量最大的核心市场至少到 2028 年都没有新一代产品。虽然这有助于精简 Intel 臃肿的 SKU 阵容，但我们认为这是错误之举：AI 工具调用和上下文存储所需的通用计算，更需要连接性好的主流 CPU，而不是单插槽性能巨兽。

# AMD Venice 架构变化

![](https://substack-post-media.s3.amazonaws.com/public/images/5ccdb80a-accb-4092-90d4-09ebda6b6953_1530x1600.png)
*AMD Venice 裸片布局。来源：@HighYieldYT*

当 Intel 抛弃 EMIB 时，AMD 终于在 Venice 上采用了对等的先进封装技术，用高速短距链路把 CCD 连到 IO 裸片。相关出货量数据见我们的[加速器、HBM 与先进封装模型](https://semianalysis.com/accelerator-hbm-model/)。

CCD 链路所需的额外裸片边缘占掉了额外宽度，迫使中央 IO 枢纽拆成 2 颗裸片。这就产生了又一次裸片到裸片的跳数来跨越芯片的两个半区，形成 Intel 方案所避免的又一个 NUMA 域。IO 裸片现在总共有 16 个内存通道，比 2022 年 Genoa 的 12 个更多。AMD 也终于追上 Intel，开始支持更高带宽的多路复用内存：16 通道 MRDIMM-12800 可提供 1.64TB/s，是 Turin 的 2.67 倍。

AMD 还在 CCD 内部转向网格网络，32 个 Zen6c 核心排成 4x8 阵列，不过可能还额外预留了一个用于良率恢复的备用核心。8 颗 TSMC N2 CCD 把核心数带到 256，比 192 核的 Turin-Dense 3nm EPYC 9965 增加三分之一。Zen6c 恢复了每核完整的 4MB L3 缓存（此前在 Zen5c 上被砍半），每颗 CCD 形成高达 128MB 的缓存区域。

面向 AI 头节点、核心数更低且频率优化的 "-F" SKU 将采用与消费级桌面和移动 PC 产品线相同的 12 核 Zen6 CCD 设计，8 颗 CCD 最多 96 核。虽然相比 128 核的 Turin-Classic 4nm EPYC 9755 有所退步，但比高频 64 核的 EPYC 9575F 多出 50% 的核心。

最后，在 IO 裸片旁、紧挨 DDR5 接口引出的位置，可以看到 8 颗小裸片。它们是集成无源器件（IPD），用于在 IO 极度密集的区域平滑芯片供电——那里 SP7 封装布线已被内存通道扇出占满。

![](https://substack-post-media.s3.amazonaws.com/public/images/e982a29b-8dbe-48a8-b2d8-a5a595d09ffe_3053x1668.png)
*AMD Venice 性能宣称。来源：AMD*

性能方面，AMD 宣称旗舰 256 核变种的每瓦性能在 SPECrate®2017_int_base 中比旗舰 192 核 Turin 高出 1.7 倍以上，这意味着凭借每时钟指令数（IPC）更高的新 Zen 6 核心微架构，单核性能也进一步提升。Zen 6 还为 AI 数据类型引入了新指令，包括 AVX512_FP16、AVX_VVNI_INT8，以及用于位矩阵乘法和位反转操作的新指令 AVX512_BMM，运行于 CPU 的浮点单元上。

对于 BMM，FPU 寄存器存储 16x16 二值矩阵，用 OR 和 XOR 运算完成 BMM 累加。二值矩阵的计算远比浮点矩阵容易，对能用上它的软件（如 Verilog 仿真）可带来大幅能效提升。然而 BMM 的精度不足以支撑 LLM，因此我们认为这条指令的采用会很有限。

由于 AMD 的单核性能已显著高于 Intel（96 核 Turin 可匹敌 128 核 Granite Rapids），在 2026 到 2028 世代的数据中心 CPU 上，AMD Venice 与 Intel Diamond Rapids 的性能差距还会进一步拉大。得益于新的裸片间互连和更大的核心域，Venice 的核间延迟应该会比 Turin 有所改善。

AMD 还在 Intel 撤退的方向上加倍下注。当 Intel 取消 8 通道处理器时，AMD 将推出新的 8 通道 Venice SP8 平台，接棒 EPYC 8004 Siena 系列的低功耗、小插槽产品线，同时仍带来最多 128 个高密度 Zen 6c 核心。凭此，AMD 将在企业市场——Intel 的传统堡垒——斩获大量份额。

# 2026 年 CPU 成本分析

![](https://substack-post-media.s3.amazonaws.com/public/images/8c0105ff-d533-4e0b-b724-ed097370cf6f_1065x1901.png)
*AMD Venice 物料清单（BoM）成本。来源：SemiAnalysis 估算 sales@semianalysis.com*

*SemiAnalysis 基于我们对供应链的深入了解，提供详细的物料清单（BOM）成本分析。如需了解确切的裸片面积、配置、拓扑、性能估算以及与超大规模厂商 ARM CPU 的竞争力对比，请致信 [Sales@SemiAnalysis.com](mailto:Sales@SemiAnalysis.com) 洽谈定制咨询与竞争分析服务。我们对 AMD Turin、Venice，Intel Granite Rapids、Diamond Rapids，NVIDIA Grace、Vera，以及 AWS、Microsoft、Google 等超大规模厂商的 ARM CPU 均有详细的成本测算与拆解。*

# NVIDIA Grace

![](https://substack-post-media.s3.amazonaws.com/public/images/56be8f6f-b46d-4a8c-b042-449a59a8fe0c_1999x1018.png)
*NVIDIA Grace CPU 的连接。来源：NVIDIA*
![](https://substack-post-media.s3.amazonaws.com/public/images/5e6f2555-0038-48f1-945e-f48bdc05c2f7_1846x1046.png)
*NVIDIA Grace 可扩展一致性总线（Scalable Coherency Fabric）。来源：NVIDIA*

与本文讨论的大多数通用 CPU 不同，NVIDIA 的 CPU 从头节点和 GPU 扩展内存（Extended GPU Memory）的用途出发设计，NVLink-C2C 是它的杀手锏。这条 900GB/s（双向）高速链路让所连接的 Hopper 或 Blackwell GPU 能以全带宽访问 CPU 内存，每颗 Grace CPU 最高 480GB 内存，缓解了 HBM 容量偏低的限制。Grace 还采用移动级 LPDDR5X 内存，在 512 位宽内存总线上维持 500GB/s 高带宽的同时压低非 GPU 功耗。最初的 Grace Hopper superchip 每颗 GPU 配 1 颗 Grace，后来的 Grace Blackwell 世代则由 2 颗 GPU 共享 1 颗 CPU。NVIDIA 还为需要高内存带宽的 HPC 客户提供双 Grace superchip CPU。

在 CPU 核心方面，NVIDIA 采用高性能 ARM Neoverse V2 设计，每核 1MB 私有 L2 缓存，布置在 6x7 网格网络上，容纳 76 核和 117MB L3 缓存，出于良率最多启用 72 核。每个网格站点上的缓存交换节点（CSN）最多连接 2 个核心和若干 L3 切片。NVIDIA 强调网格网络高达 3.2TB/s 的对分带宽（bisection bandwidth），可见 Grace 专注于数据流动而非原始 CPU 性能。

性能方面，Grace 有一个源自 Neoverse V2 核心的古怪微架构瓶颈，使未优化的 HPC 代码运行缓慢。根据 NVIDIA 的 [Grace 性能调优指南](https://docs.nvidia.com/dccpu/grace-perf-tuning-guide/compilers.html)，优化大型应用以获得更好的代码局部性，可带来 50% 的加速。原因在于核心分支预测引擎在提前存储和预取指令方面的限制。在 Grace 上，指令被组织为 32 个 2MB 的虚拟地址空间。

当分支目标缓冲区填充超过 24 个区域时，性能开始大幅下滑——热点代码霸占缓冲区并加剧指令流动，导致更多分支预测错误。若程序超过 32 个区域，整个 64MB 缓冲区会被清空，分支预测器忘掉之前所有分支指令来容纳新指令。分支预测器一旦失效，CPU 核心前端就会卡住整个运作，ALU 只能干坐着空等指令执行。

这正是目前 GB200 和 GB300 中的 Grace CPU 拖慢 AI 工作负载的原因。

### NVIDIA Vera

2026 年，Vera 为 Rubin 平台更进一步：C2C 带宽翻倍至 1.8TB/s，内存位宽也翻倍，采用 8 个 128 位宽的 SOCAMM 192GB 模块，以 1.2TB/s 带宽提供 1.5TB 内存。网格设计保留，为 7x13 阵列、容纳 91 核，最多 88 核可用。L3 缓存增加到 162MB。NVIDIA 现在把外围内存和 IO 区域解耦为独立小芯片，总计 6 颗裸片以 CoWoS-R 封装（1 颗 3nm 光罩级大小的计算裸片带 NVLink-C2C、4 颗 LPDDR5 内存裸片和 1 颗 PCIe6/CXL3 IO 裸片）。

![](https://substack-post-media.s3.amazonaws.com/public/images/36a84fe6-b848-4374-9c7f-245cc317e0a3_1989x1851.png)
*Vera Rubin NVLink C2C 示意图。来源：NVIDIA*
![](https://substack-post-media.s3.amazonaws.com/public/images/ebce2cd3-75fb-44fe-aa0b-35a191131a98_3119x1925.png)
*Vera CPU 规格。来源：NVIDIA*
![](https://substack-post-media.s3.amazonaws.com/public/images/24ed62c6-9b02-438e-8acb-1868bfd4ee81_3000x3040.jpeg)
*Vera 版图标注。来源：NVIDIA，SemiAnalysis 估算*

也许是领教了 ARM Neoverse 核心性能瓶颈的苦头，NVIDIA 重新召回了自研 ARM 核心设计团队，推出支持 SMT 的新 Olympus 核心，实现 88 核 176 线程。NVIDIA 上一次自研核心还是 8 年前 Tegra Xavier SoC 中的 10 发射宽 Carmel 核心。ARMv9.2 的 Olympus 核心把浮点单元拓宽到 6 个 128 位宽端口（Neoverse V2 为 4 个），并支持 ARM 的 SVE2 FP8 运算。每核配备 2MB 私有 L2 缓存，比 Grace 翻倍。总体而言，NVIDIA 宣称转向 Vera 带来 2 倍性能提升。

# AWS Graviton5

![](https://substack-post-media.s3.amazonaws.com/public/images/af081f84-4b44-4861-83b9-7467a1b74f89_2964x1485.png)
*Graviton CPU 历代沿革。来源：AWS*

Amazon Web Services（AWS）是第一家成功为云自研并部署自有 CPU 的超大规模云厂商。凭借收购 Annapurna Labs 芯片设计团队以及 ARM 的 Neoverse 计算子系统（CSS）参考设计，AWS 可以直接找 TSMC 和 OSAT 封测伙伴生产芯片，毛利结构更优，从而以更低价格提供 EC2 云实例，而不必购买 Intel Xeon。

Graviton 的强力推进始于新冠热潮期间的 Graviton2 世代，当时 AWS 大幅打折，吸引云客户把程序从 x86 移植到 ARM 生态。虽然单核性能不及 Intel 的 Cascade Lake 世代，但 Graviton2 以零头的价格带来 64 个 Neoverse N1 核心，每美元性能显著更高。

2021 年底预览的 Graviton3 带来了多项变化，重点是把单核性能提升到有竞争力的水平。AWS 转用 ARM 的 Neoverse V1——一个比 N1 大得多、浮点性能翻倍的 CPU 核心——同时核心数保持在 64。采用 10x7 核心网格网络（CMN），片上印刷 65 核，留出 1 核可屏蔽用于分级筛选（binning）。AWS 还把设计解耦为小芯片：4 个 DDR5 内存小芯片和 2 个 PCIe5 IO 小芯片环绕 TSMC N5 的中央计算裸片，全部经 Intel 的 EMIB 先进封装连接。由于 Intel Sapphire Rapids 一再延期，Graviton3 成为首批部署 DDR5 和 PCIe5 的数据中心 CPU 之一，比 AMD 和 Intel 整整早了一年，我们当时曾撰文分析。

Graviton4 继续扩展，采用更新的 Neoverse V2 核心，核心数和内存通道各增加 50%，分别达到 96 核和 12 通道，比上一代提速 30-45%。PCIe5 通道数从 32 条翻了三倍到 96 条，大幅增强网络和存储连接能力。Graviton4 还支持双路配置，实例核心数可以更高。

![](https://substack-post-media.s3.amazonaws.com/public/images/caa991f9-af71-4c1d-b519-c7aa45b5bfac_2732x1472.png)
*Graviton5 核心示意图。来源：AWS*

自 2025 年 12 月起进入预览的 Graviton5 性能再创新高：192 个 Neoverse V3 核心，是上一代的两倍，在 TSMC 3nm 制程上集成 172 亿个晶体管。每核 L2 缓存维持 2MB，共享 L3 缓存则从 Graviton4 寒酸的 36MB 增加到体面的 192MB——在核心数翻倍而内存带宽只提升 57%（12 通道 DDR5-8800）的情况下，多出来的缓存起到缓冲作用。

正如我们在[核心研究（Core Research）](https://semianalysis.com/core-research/)中讨论过的，Graviton5 的封装非常独特，对供应链上的几家供应商影响重大。

有意思的是，虽然 PCIe 升级到 Gen6，通道数却从 Graviton4 的 96 条倒退到 Graviton5 的 64 条，因为 AWS 的部署配置显然普遍用不满所有 PCIe 通道。这项成本优化在不影响性能的情况下为 Amazon 省下大量 TCO。

Graviton5 采用演进的小芯片架构与互连，现在 2 个核心共享同一网格站点，排成 8x12 网格。虽然 AWS 这次没有展示封装和裸片配置，但确认 Graviton5 确实采用了新颖的封装策略，且 CPU 核心网格分布在多颗计算裸片上。

![](https://substack-post-media.s3.amazonaws.com/public/images/9280a965-5af9-4c30-8ae0-b107f9248e48_2697x1149.png)
*Graviton 流片前设计。来源：AWS*

在 CPU 使用方面，AWS 自豪地提到，他们内部已在 CI/CD 设计集成流程中使用数千颗 Graviton CPU，并运行 EDA 工具来设计和验证未来的 Graviton、Trainium 和 Nitro 芯片，形成"Graviton 设计 Graviton"的内部自用（dogfooding）循环。AWS 还宣布 Trainium3 加速器将采用 Graviton CPU 作头节点，1 颗 CPU 对 4 颗 XPU。初期版本搭配 Graviton4，未来的 Trainium3 集群将由 Graviton5 驱动。

# Microsoft Cobalt 200

![](https://substack-post-media.s3.amazonaws.com/public/images/9634fe8d-37d6-4a92-87a5-1b371d9a6a4f_1920x1080.png)
*Microsoft Cobalt 200 服务器。来源：Microsoft*
![](https://substack-post-media.s3.amazonaws.com/public/images/80839a8f-c1e0-44fe-ab4e-310b4427ccd1_2608x1427.png)
*Cobalt 200 SoC 布局。来源：Microsoft*

继 Microsoft 2023 年首款 Cobalt 100 CPU（我们在上文已有介绍）之后，Cobalt 200 于 2025 年底发布，带来多项升级。核心数增加不多，从 128 到 132，但得益于 Neoverse V3 设计，每个核心比上一代的 Neoverse N2 强大得多。每核拥有非常大的 3MB L2 缓存，通过标准 ARM Neoverse CMN S3 网格网络跨两颗 TSMC 3nm 计算裸片相连，裸片之间采用定制高带宽互连。从示意图看，每颗裸片为 8x8 网格，配备 6 通道 DDR5 和 64 条支持 CXL 的 PCIe6 通道。每个网格站点共享 2 核，每颗裸片共印刷 72 核，出于良率启用 66 核。192MB 共享 L3 缓存也分布在网格各处。凭借这些升级，Cobalt 200 比 Cobalt 100 提速 50%。

与 Graviton5 不同，Cobalt 200 只用于 Azure 的通用 CPU 计算服务，不会被用作 AI 头节点。Microsoft 的 Maia 200 机柜级系统采用的是 Intel 的 Granite Rapids CPU。

# Google Axion C4A、N4A

![](https://substack-post-media.s3.amazonaws.com/public/images/05f65e22-af68-4a66-8471-20eb13de627b_3005x1594.png)
*Axion C4A 晶圆与封装。来源：Hajime Oguri，Google Cloud Next '24*
![](https://substack-post-media.s3.amazonaws.com/public/images/7cca6b00-0503-42dd-b09d-15a595e864d9_1844x1814.png)
*Axion N4A CPU。来源：Google*

Axion 系列于 2024 年发布、2025 年正式商用，标志着 Google 切入为 GCP 云服务自研 CPU 的领域。Axion C4A 实例在标准网格网络上最多配备 72 个 Neoverse V2 核心，在一颗大型单片 5nm 裸片上提供 8 通道 DDR5 和 PCIe5 连接。根据 Google Cloud Next 2024 上展示的 Axion 晶圆特写图片，该裸片似乎以 9x9 网格印刷了 81 核，留出 9 核可屏蔽以保证良率。因此我们认为，2025 年底进入预览的 96 核 C4A 裸金属实例采用了一颗新设计的 3nm 裸片。

面向更具成本效益的横向扩展 Web 与微服务，Google 的 Axion N4A 实例现已进入预览，配备 64 个性能较低的 Neoverse N3 核心，裸片小得多，可在 2026 年实现可观的放量爬坡。Axion N4A 芯片是 Google 在 TSMC 3nm 制程上的全定制设计。随着 Google 把内部基础设施迁移到 ARM，Gmail、YouTube、Google Play 等服务将与 x86 并行运行在 Axion 上。未来，Google 还将设计用作 Gemini 背后 TPU 集群头节点的 Axion CPU。

# AmpereOne 与软银收购

![](https://substack-post-media.s3.amazonaws.com/public/images/ae88cb59-dfc9-4ef0-82db-daeb13090a11_2774x1467.png)
*AmpereOne 2024 路线图。来源：Ampere Computing*
![](https://substack-post-media.s3.amazonaws.com/public/images/9bd4b346-265c-417c-8de2-3bb02f84db2d_2618x1683.png)
*Ampere Altra Max（左）与 Altra（右）。来源：Ampere Computing*
![](https://substack-post-media.s3.amazonaws.com/public/images/14200e92-bb26-47b1-89d4-c52dc20cccd8_1500x1852.png)
*开盖的 AmpereOne CPU。来源：Brendan Crain，Wikimedia*
![](https://substack-post-media.s3.amazonaws.com/public/images/9c471082-f099-457c-bc01-5aa2deb081cb_2923x1573.png)
*AmpereOne 网格架构。来源：Ampere Computing，Hot Chips 2024*

Ampere Computing 是商用（merchant）ARM 芯片最初的旗手，作为第三方芯片供应商直接与 AMD、Intel 争夺 OEM 服务器订单。凭借与 Oracle（甲骨文）的紧密合作，Ampere 锣鼓喧天地推出 80 核 Altra 和 128 核 Altra Max 系列 CPU，誓以高性价比 ARM CPU 颠覆 x86 双寡头。Ampere Altra 采用 Neoverse N1 核心和自研网格互连，核心按 4 核一簇分组，在单一 TSMC 7nm 裸片上配备 8 通道 DDR4 和 128 条 PCIe4 通道。

下一代 AmpereOne CPU 把核心数提升到 192，得益于转向 5nm 制程和新颖的小芯片设计——IO 解耦为独立的 DDR5 和 PCIe 裸片，以无需中介层的 MCM 形式封装。Ampere 还转向自研 ARM 核心，为核心密度而非绝对性能设计，搭配超大的 2MB L2 缓存，以尽量减少"吵闹邻居"（相邻核心上运行的其他 VM 霸占共享网格互连流量）带来的性能损失。类似的 4 核簇实现在 9x8 网格网络上。总体而言，整数性能比 Altra Max 翻倍。

小芯片设计让同一颗计算裸片可以在其他变种中复用：12 通道的 AmpereOne-M 增加 2 颗内存控制器裸片；未来的 AmpereOne-MX 复用相同 IO 小芯片，换上 256 核的 3nm 计算裸片。其 2024 年路线图还披露了未来的 AmpereOne Aurora 芯片，拥有 512 核和 AI 训练与推理能力。

然而，随着 Ampere Computing 于 2025 年被软银以 65 亿美元收购，这份路线图已不再有效。诚然，孙正义（Masayoshi Son）想要 Ampere 的 CPU 设计人才来充实 Stargate 项目的 CPU 设计，但收购的另一推动力是 Oracle 想从这门惨淡的生意中抽身。由于时机和执行问题，Ampere 的 CPU 从未上量到足够高的规模。

Altra 世代是他们首次大举进入市场，但来得太早，当时大多数软件还不是 ARM 原生。超大规模厂商可以快速改造内部工作负载以适配自家 ARM 芯片，通用和企业 CPU 市场的转向则慢得多。此后，AmpereOne 世代屡遭延期，Oracle Cloud A2 和 CPU 直到 2024 年下半年才可用。届时超大规模厂商的 ARM CPU 项目已全面铺开，而 AMD 也能匹配 Ampere 的 192 核，单核性能却高出 3-4 倍。尽管 Oracle 以每核许可费减半来推广 Ampere 实例，这些 CPU 还是没能火起来，订单逐渐枯竭。Oracle 从未用完其对 Ampere CPU 的全部预付款，采购额从 2023 财年的 4,800 万美元萎缩到 2024 年的 300 万美元和 2025 年的 370 万美元。

如今在软银旗下，Ampere 在 CPU 之外也在研发 AI 芯片。

# ARM Phoenix

![](https://substack-post-media.s3.amazonaws.com/public/images/44e44d5f-8aeb-4974-9868-cd834fe74993_2560x1440.png)
*ARM 的 CSS 产品在定制化与开发成本之间取得平衡。来源：ARM*

ARM 的核心 IP 授权业务在数据中心市场非常成功，几乎每家超大规模厂商的自研 CPU 都采用了其 Neoverse CSS 设计。迄今为止，已有超过 10 亿个 Neoverse 核心部署在数据中心 CPU 和 DPU 中，12 家公司共签署了 21 份 CSS 授权。随着核心数增加和超大规模 ARM CPU 放量，数据中心版税收入同比增长超过一倍，ARM 预计未来几年 CSS 将占版税收入的 50% 以上。阅读我们的相关文章，可进一步了解 ARM 的商业模式以及 CSS 如何榨取更多价值。

不过，ARM 将在 2026 年更进一步，提供完整的数据中心 CPU 设计，首家客户是 Meta。这颗代号 Phoenix 的 CPU 改变了商业模式——ARM 亲自下场做芯片厂商，从核心到封装设计整颗芯片。这意味着 ARM 将与授权 Neoverse CSS 架构的客户直接竞争。由软银控股的 ARM 还在为 OpenAI 设计定制 CPU，作为 Stargate（OpenAI 与软银合资项目）的一部分。Cloudflare 也有意成为 Phoenix 的客户。我们在[核心研究（Core Research）](https://semianalysis.com/core-research/)中有详细的 COGS、利润率和营收分析。

Phoenix 采用标准的 Neoverse CSS 设计和布局，与 Microsoft 的 Cobalt 200 相似。128 个 Neoverse V3 核心通过 ARM 的 CMN 网格网络分布在两颗 TSMC 3nm 半光罩尺寸裸片上。内存与 IO 方面，Phoenix 配备 12 通道 DDR5-8400 MT/s 和 96 条 PCIe Gen 6 通道。能效具有竞争力，CPU TDP 可配置为 250W 到 350W。

至此，Meta 拥有了自己的 ARM CPU，可与 Microsoft、Google、AWS 比肩。作为 AI 头节点，Phoenix 可通过加速器使能套件（Accelerator Enablement Kit）经 PCIe6 与挂载的 XPU 实现一致性共享内存。我们将在下文为订阅用户详述下一代 ARM "Venom" CPU 设计，包括一项重大内存变化。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

# 华为鲲鹏（Kunpeng）

中国自研 CPU 的步伐持续推进，龙芯（Loongson）和阿里巴巴的倚天（Yitian）系列都提供了本土设计的选项。但市场上最大的玩家是华为，其数据中心 CPU 路线图已聚焦到鲲鹏（Kunpeng）处理器系列。华为的海思（HiSilicon）团队拥有一些最有能力的设计工程师，其自研的 TaiShan CPU 核心和数据总线值得关注。

华为最初几代数据中心 CPU 使用标准的移动级 ARM Cortex 核心。2015 年的 Hi1610 有 16 个 A57 核心；2016 年的 Hi1612 核心数翻倍到 32；2017 年的鲲鹏 916 把核心架构更新为 Cortex-A72。这三代都由 TSMC 16nm 制造。

![](https://substack-post-media.s3.amazonaws.com/public/images/9050cd76-7b26-4fa8-b999-8b5a81a3a501_1306x2336.png)
*鲲鹏 920 裸片图。来源：万扯淡*

2019 年问世的鲲鹏 920 采用雄心勃勃的多小芯片设计和 64 个自研核心。两颗 TSMC 7nm 计算裸片各含 8 个簇、每簇 4 个基于 ARM v8.2 ISA 的 TaiShan V110 核心。簇经环形总线连接到同裸片上的 4 通道 DDR4，两颗计算裸片合计 8 通道。鲲鹏 920 是首个采用 TSMC CoWoS-S 先进封装的 CPU，大型硅中介层把 2 颗计算裸片与 1 颗 IO 裸片相连，后者提供 40 条 PCIe Gen 4 通道和双集成 100 Gigabit 以太网控制器，裸片间使用定制接口。虽然鲲鹏 920 集成了许多新颖技术，但美国对华为的制裁切断了其 TSMC 供应，打乱了 CPU 路线图——下一代鲲鹏 930 未能在 2021 年发布。

![](https://substack-post-media.s3.amazonaws.com/public/images/c84b6c66-8fe3-4f33-812d-aa3ddfd7c144_1300x1833.png)
*鲲鹏 920B 裸片图。来源：Kurnal*

取而代之的是，升级版鲲鹏 920B 于 2024 年悄然发布，带来多项升级。TaiShan V120 核心现支持 SMT，两颗计算裸片各 10 个 4 核簇，共 80 核 160 线程。核心互连和布局与鲲鹏 920 相似，计算裸片上配备 8 通道 DDR5。IO 裸片如今拆成两半，计算裸片居中。我们认为，两代 CPU 之间 5 年的空窗，是美国制裁以及不得不为 SMIC N+2 制程重新设计芯片的结果。

![](https://substack-post-media.s3.amazonaws.com/public/images/fa36c618-5da3-4cc3-9235-a3b4f5322892_3035x1034.png)
*华为鲲鹏 CPU 路线图。来源：华为*
![](https://substack-post-media.s3.amazonaws.com/public/images/651c2acf-e470-4797-b124-9cdd060ca65d_3065x778.png)
*华为 TaiShan 950 SuperPoD。来源：华为*

2026 年，华为将携鲲鹏 950 再次更新其 CPU 产品线，并以 TaiShan 950 SuperPoD 机柜形态用于通用计算。鲲鹏 950 宣称凭借其专有的 GaussDB Multi-Write 分布式数据库架构，OLTP 数据库性能比鲲鹏 920B 提升 2.9 倍。为此，核心数翻倍有余，达到 192 核，采用保留 SMT 支持的新 LinxiCore 核心，还将生产较小的 96 核版本。每个 TaiShan 950 SuperPoD 机柜容纳 16 台双路服务器、最多 48TB DDR5 内存，表明其为 12 通道内存设计。这些机柜还集成了存储和网络，将被 Oracle 的 Exadata 数据库服务器采用，并供中国金融行业使用。该设计很可能由 SMIC 刚在麒麟 9030 智能手机芯片上首发的 N+3 制程生产。

华为的路线图延续到 2028 年的鲲鹏 960 系列。这一代延续设计一分为二的趋势：面向 AI 头节点和数据库的 96 核 192 线程高性能版本，宣称单核性能提升 50% 以上；面向虚拟化和云计算的高密度型号则把核心数提高到 256 核，甚至可能更多。届时，我们预计华为将在中国超大规模厂商的 CPU 部署中拿走可观份额。

下文我们将呈现截至 2028 年的 CPU 路线图，详述 2026 年之后数据中心 CPU 的关键特性与架构变化，包括 AMD 的 Verano 与 Florence、Intel 的 Coral Rapids 及已取消的 CPU 产品线、ARM Venom 的规格、Qualcomm 携 SD2 重返数据中心 CPU 市场，并把 NVIDIA 的 Bluefield-4 纳入其中，作为 CPU 部署未来演进的一个标志。随后我们将讨论 DRAM 短缺对各个数据中心 CPU 细分市场的影响，展望未来 CPU 趋势，点出将塑造未来十年 CPU 的关键设计要点。
