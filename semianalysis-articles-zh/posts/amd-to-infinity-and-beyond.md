---
title: "AMD——飞向无穷，乃至更远"
title_en: "AMD – To Infinity And Beyond"
date: 2022-06-17
source: https://newsletter.semianalysis.com/p/amd-to-infinity-and-beyond
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AMD——飞向无穷，乃至更远

> 原文：[AMD – To Infinity And Beyond](https://newsletter.semianalysis.com/p/amd-to-infinity-and-beyond) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

自 Zen 架构发布以来，AMD 这几年的表现可谓大杀四方。它们吞噬英特尔（Intel）市场份额的样子，就像在吃周日廉价自助餐一样。而且这一势头毫无停止的迹象。AMD 自建并收购了世界级的 IP，这让 AMD 在未来几年的成功具有很高的能见度。AMD 的执行文化也是业内最令人惊叹的之一。

今天我们将梳理 AMD 在其财务分析师日（Financial Analyst Day）上披露的信息，涵盖从战略、产品、路线图、技术到财务的各项细节。我们也会在此之上给出自己的分析——总体而言我们的看法是正面的，但有些地方我们认为他们有所夸大和过度炒作。

AMD 的战略可以用苏姿丰（Lisa Su）的一句话来概括。

> 无论你是谁，无论你身处哪个行业，你都需要更多算力。
>
> AMD CEO 苏姿丰博士（Dr. Lisa Su）

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2a16e226-8ce0-4b89-88f9-b762324a114e_1024x564.png)

AMD 的演示开篇回顾了其在各大主要领域的领先地位。数据中心是其中最显眼的一块。最初的爬坡很慢：第一代 Naples 遇到了技术上的磨合问题，采用量寥寥。第二代 Rome 花了很长时间才完成客户认证和导入，而到了第三代 Milan，毫无疑问，从 HPC 到云，人人都想尽可能多地买。

在 PC 上，AMD 也完成了类似的转变，正在向价值链上游走。过去一年他们基本把低端市场让给了 Intel，其份额增长全部来自高端和企业级市场。游戏是我们不太认同 AMD 叙事的一点。他们的 GPU 不错，但谈不上突破性。他们在这一领域的超额表现大部分来自游戏主机。在游戏 GPU 市场，他们的增速跑输了大市，一部分原因是产品相对 Nvidia 缺乏吸引力，另一部分原因是供应严重不足。

56% 的营收 CAGR 惊艳至极。其中一部分来自疫情带来的终端市场红利，但很大一部分纯粹是牺牲 Intel 换来的 PC 和数据中心份额增长。

份额增长并非成功的唯一路径。当你审视 AMD 的总可服务市场（TAM）及其随时间的变迁时，未来增长变得更加具体。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e98055bf-97eb-4c27-b3a1-8c71b5f846c1_1024x566.png)

由于收购 Xilinx 以及部分终端市场的增长，AMD 2020 年的 TAM 远小于现在。展望 2027 年，这些 TAM 数字非常有意思，指向了 AMD 的雄心：借助自研、Xilinx 与 Pensando IP 的组合，从传统业务拓展到新业务。TAM 总计 $125B：其中 $61B 为 GPU 与 AI，$42B 为服务器 CPU，$13B 为 FPGA 与自适应 SoC，$6B 为 DPU 与基础设施加速。这些 TAM 大多可以触达，但也有一些不行。

接下来不再泛泛而谈，我们开始深入。

# **CPU**

AMD 领先地位的立身之本系于 CPU 主导权，其许多 TAM 扩张机会都依赖于 AMD 能向他人提供 CPU 和互连（fabric），让对方接入其定制 IP。Intel 采取的是同样的策略，因此 AMD 必须在这一领域保持领先。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f38ec58d-41c7-46c1-be84-b43e02241f19_1024x569.png)

首先，AMD 在每核心面积上对 Intel 有巨大优势，但他们的对比并不坦诚。比较不含 L3 缓存的单个核心是有缺陷的，因为 Intel 通常核心更大、L2 缓存更大而 L3 更小；AMD 则围绕更大的共享 L3 缓存做优化。他们的 Zen 3 8 核小芯片是 ~81mm2 的台积电（TSMC）N7 硅片。如果只算核心、忽略测试电路和裸片间连接，则是 67.85mm2。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/7d096c79-7e51-4697-ae1c-53de46d69a6b_1024x464.jpeg)

这个数字已包含核间环形总线（ring bus），但不包含 IO 裸片上互连部分的面积。Intel 的 Alder Lake 8 核含 L3 缓存及芯片整体环形总线约 ~84mm2，所以 Intel 的劣势远没有 AMD 渲染的那么大。功耗优势反而重要得多。此外，Intel 在其服务器核心上堆了更强的 mesh 互连、数据流加速器（DSA）、更多 AVX512 能力以及 AMX AI 加速器。这些让 Intel 在某些工作负载中取胜，但也使其下一代 Sapphire Rapids 相对 AMD 的 Milan 和 Genoa 在成本上很难看——正如我们在[这篇文章](https://semianalysis.substack.com/p/is-ampere-computings-cloud-native?s=w)中所展示的。AMD 目前的 TCO 好得多，而基于性能宣称、估算、爆料以及我们的服务器级成本模型，这一领先在下一代 Genoa 对阵 Sapphire Rapids 时还会扩大。至少到 2025 年，AMD 都会持续夺取份额。

至于 Zen 架构的其余部分，很高兴看到 AMD 公布的数字打脸了所有 YouTube 和 Twitter 上的「[爆料者](https://twitter.com/dylan522p/status/1535047412150042624?s=20&t=pKIOaYpqAiEPKlLbel-HHA)」。Zen 5 遵循 AMD 的 18 个月节奏，预计最先于 2024 年上半年问世。他们称其包含一些 AI 和机器学习优化，这非常有意思，因为 Zen 4 已经包含 VNNI。AMD 会不会像 Intel 有 AMX 那样，做一个 AI 协处理器？

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/0e073464-0444-442f-8762-bb6de567e8f3_1024x569.png)

TAM 拆分很有意思。这是我第一次看到三巨头（Intel、AMD、Nvidia）中的任何一家把云、企业、HPC 分开列。这个 HPC TAM 比我们想象的大不少，所以我猜他们很可能把许多未提交 Top 500 榜单的系统也算进去了。

AMD 在产品线上做架构差异化令人兴奋：Genoa 是当代 Milan 的直系继任者；Bergamo 则带来一颗采用改良 Zen 4 核心（名为 Zen 4C）的「云原生」CPU。如果你想知道这是营销话术还是真东西，请看我们[围绕 Ampere Computing 的拆解分析](https://semianalysis.substack.com/p/is-ampere-computings-cloud-native?s=w)，其中也包括一些纯粹的制造成本对比。Zen 4C 带着更大的向量单元、SMT 和更高性能，在通往云原生的路上走得没那么远，但它是一个低开销变体，让主核心阵营的竞争力大幅提升。

最后，AMD 透露了 Siena，你可以把它理解为半个 Genoa。它会有些不同的能力，但总体而言在各方面都是半个 Genoa。不过由于片上互连的缩放特性，功耗的降幅会略超过一半。

# **互连（Fabric）**

AMD 的互连（fabric）非常令人兴奋，在我们眼中是该公司最关键的部分。本文标题这么起是有原因的。纵观定制芯片业务，这正是决定订单成败的关键技术。与他们的封装能力一起，它也是 AMD 快速、高效整合全部现有 IP、在不付出巨额设计费用的情况下为每个市场打造最佳产品的方式。

AMD 可以做出世界上最好的 CPU、GPU 或 FPGA，但如果拿不出差异化的东西，客户照样会弃他们而去。产品将越来越针对特定应用量身定制。如果不发展小芯片和出色的互连，出货量会下滑、设计成本会上升。这两样 AMD 都有。

> 客户来问我们：嘿，你们能帮我们做出差异化吗？
>
> 我们不想做你们正在做的那些通用产品，因为在通用产品上你们有规模优势，但我们希望能加入我们的独门秘方。
>
> 我们已经拥有业界领先的小芯片平台，而我们要做的，就是让第三方 IP 和客户 IP 能更轻松地接入这个小芯片平台。
>
> AMD CEO 苏姿丰博士（Dr. Lisa Su）

AMD 互连的决定性时刻随 Infinity Fabric 4 而来。Infinity Fabric 通常运行在为 PCIe 标准设计的同一套 PHY 之上，但采用不同的协议。随着 CXL 和 UCIe 入局，情况变得微妙。CXL 对加速器与主机之间的一致性、内存池化以及总体上的解耦式服务器架构意义重大。AMD 想利用这一点，同时提供增强能力。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8572d580-36e1-4e66-8e71-6f7136921f73_1024x577.png)

AMD 的意思似乎是：他们的 Infinity 架构可以利用 PCIe 或 UCIe 物理层，同时兼容 PCIe、CXL 或他们自己的协议层。基本上，AMD 似乎想左右逢源。你想做独立的 PCIe 加速器，他们支持；你想做带 64 条 CXL 通道、符合 UCIe 标准的小芯片，他们支持；你想做同等位宽但更低延迟的 AMD 专有协议，他们也支持。然后还有层层向后兼容——如果对端不支持 Infinity Fabric，可以降落到 CXL 或 PCIe。

他们将把这一支持带给 Xilinx 小芯片、GPU 小芯片，以及想为 UCIe 或 Infinity 生态设计小芯片的第三方。这是相当漂亮的一步棋，我们相信只要 AMD 能执行到位，就能分到相当大的一块蛋糕。Intel 也将为第三方支持 UCIe 接入的小芯片，而且在大力推动。这让第三方可以用同一颗小芯片利用多个封装和服务器生态，并以具备一致性的方式与 Intel 或 AMD 协同工作。

AMD 的 Infinity Fabric 届时还应能支持[共封装光学（CPO）](https://semianalysis.substack.com/p/ayar-labs-co-packaged-optics-revolution?s=w)。正如我们[此前讨论](https://semianalysis.substack.com/p/ayar-labs-co-packaged-optics-revolution?s=w)并随后得到证实的，Nvidia 和 HPE 将通过 UCIe 使用 Ayar Labs 的共封装光学 tile，而由于 UCIe 标准是共享的，AMD 也能切入同一生态。届时 AMD 可以用 Infinity Fabric 协议与自家第一方封装互操作，甚至可以用 CXL 与 Intel、HPC 或 Nvidia 的封装互操作。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d95b06b0-7032-46d2-acb6-4596dd6440b2_1024x284.png)

真正的杀手锏当然在于这对超大规模云厂商、汽车公司、电信运营商和消费硬件公司意味着什么。超大规模云厂商可以把 AMD CPU、AMD GPU、Xilinx FPGA、Xilinx AI Engine、客户自研小芯片和第三方小芯片混搭组合，构建最优产品，最大化能效、性能和 TCO。

# **数据中心 GPU 与 AI**

这是我们最不看好的业务板块。AMD 在这里的 TAM 数字高达 $61B。目前 AMD 完全无法触及 AI 训练市场。Xilinx 产品在大多数推理工作负载中也没有多少竞争力，尽管 AMD 和 Xilinx 的幻灯片告诉你它们有。AMD GPU 目前存在的意义只有服务政府 HPC。

即便在这一点上，面对通用工作负载它们也难称合格。它们在深度调优的软件上运行出色，但那不是大多数工作负载。AMD 有出色的硬件，但软件跟不上。我们对 AMD 关于 ROCm 5 的承诺抱有希望，仅仅是因为 Nvidia 需要一个竞争者——但即便在问答环节，他们谈及 GPU 产品线的 ROCm 支持时的某些口吻也不那么令人放心。

话虽如此，AMD 有 5,000 名软件工程师而且在激进扩招，所以希望几年后他们会好很多。ROCm 5 应该终于能支持 RDNA 游戏 GPU 了，这意义重大。MI200 大概 $10k 以上，不是人人都愿意为一颗 GPU 掏这么多钱，或在开发期间支付云费用。RDNA 游戏 GPU 从 $250 起步，这会大大帮助初创公司、学生的开发，总体上让人们习惯在他们的软件栈上做开发。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1c85f038-4249-496a-9c17-320be5bd7c84_1023x571.png)

AMD 终于要提供一个用于开发和部署预优化 AI 模型的 SDK 了。最大的问题在于他们提供的优化水平如何、模型的广度/深度如何。乐观的看法是：业内许多人迫切希望有人挑战 Nvidia，所以会提供大量支持，包括政府、研究机构和超大规模云厂商。但大多数公司和个人还是会选最省事的选项，也就是 Nvidia。追赶需要很多年。

尽管 AMD 当代 GPU 的规格亮眼，其在数据中心 GPU 工作负载中的实际表现往往没那么惊艳。这还是建立在 AMD 用了近两倍的硅面积（2 颗大号 N7 裸片，对阵 Nvidia A100 的 1 颗大号 N7 裸片）、8 个 HBM 堆叠对阵 Nvidia 5 个 HBM 堆叠的基础上。这一切意味着 AMD 的相对制造成本要高得多。他们使用 ASE 的 FOEB 封装也不会显著改变这条成本曲线。

AMD 在这里的强项是硬件工程。AMD 下一代 MI300 是工程奇迹。AMD 宣称的每瓦性能非常亮眼。当 Intel 和 Nvidia 还停留在把 GPU 和 CPU 封装在一起的愿景上时，AMD 将于 2023 年下半年开始把它们装进下一代 HPC。而且 AMD 是在 1 个封装内实现这一切，配上真正统一的 HBM 内存。我们过去曾专门撰文介绍 MI300 的封装，它会很惊艳，远超 Intel 和 Nvidia 在同期交付的东西。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/66fee131-1350-44c3-b07e-cb26a6b13841_1024x571.png)

性能宣称看起来很惊艳，尤其是看 AMD 的一些脚注时。比如 8 倍 AI 性能、5 倍 AI 每瓦性能，简直疯狂！AMD 实测 MI250X 在 560W TDP 下达到 306.4 TFLOPS 的 FP16 性能，即理论峰值的 80%。AMD 对 MI300 性能的宣称用的是 FP8，鉴于数字格式不同，这样的对比有点不太厚道。但无论如何，按照 AMD 的宣称，MI300 需要在 900W TDP 下达到约 2400 TFLOPS 的 FP8，才能同时实现相对 MI250X 的 5 倍每瓦性能和 8 倍性能。Nvidia 的 Hopper GPU 单卡是 700W 下 2000 TFLOPS 的 FP8，但缺少 CPU 部分。一旦算上 Grace CPU 部分，功耗会升至约 900W，同时 CPU 核心也会带来小幅性能提升。原始的 TFLOPS/W 两者相近。

Nvidia 的 Grace Hopper 将于 2023 年上半年批量出货。得益于封装和制造成本上的差异，它也是一个能扩展到更高出货量的设计。主要缺点是 CPU 与 GPU 之间的数据传输仍必须进出封装。虽然这将是一条相对高带宽、低延迟的链路，但没有什么能与封装内传输相提并论。Grace 的规格已广为人知。而 MI300 方面，除了一个我们翻过但不想透露的公开 GitHub 仓库之外，没有任何公开的硬件规格。

单封装性能上 MI300 无疑更高，但对 AI 这样的大规模高性能计算而言，系统级扩展更为重要。Nvidia 的 NVLink 可以跨众多节点扩展，AMD 的 Infinity Fabric 无法以同样方式扩展。此外，AMD 的内存池相比 Nvidia 会小得多。对于商业部署，我们预计 AMD 成本更高，但在单芯片或单服务器基础上性能好得多。一旦应用扩展到数十或数百台服务器，Nvidia 很可能占优。当然，前提是 AMD 能把软件理顺。编程模型、真实应用中的性能以及这些应用中的功耗，将决定谁是赢家。

# **DPU 与基础设施处理**

我们在本通讯中写过很多关于 DPU 和 IPU 的文章，而 AMD 在这里看起来有竞争力的产品。云厂商在网络、安全、存储服务等基础设施服务上消耗大量算力。DPU 旨在解决这一问题，把这些负载卸载到网卡本身上——网卡将 CPU 核心与固定功能卸载能力、以及更标准的网络 IO 搭配在一起。Amazon 凭其 [Nitro DPU](https://semianalysis.substack.com/p/amazon-graviton-3-uses-chiplets-and) 走得最远，但 Nvidia、Marvell、Intel 和 AMD 都在竞赛之中。

目前 AMD 靠 Xilinx FPGA 表现不错。这是因为 FPGA 的可编程性和灵活性远胜一筹。例如，基于 FPGA 的网卡是高频交易事实上的标准。Microsoft 也在其 Project Catapult 网络基础设施中大量使用 FPGA，不过用的似乎不是 Xilinx 的。这些技术对 5G 和边缘也很好，但随着行业前行，这一优势会被边缘化——FPGA 不会永远统治这个领域，ASIC 终将登场。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/3dc5108e-153a-4a6b-9ff9-eea2fe5deb7d_1023x571.png)

这正是 Pensando 收购的意义所在。最难的部分是软件，而 FPGA 在这方面很糟糕。我们从实际使用该硬件的用户处听说，Pensando 拥有这个市场最好的软件之一。他们的网络流使用 P4 等开放标准。这笔收购想都不用想：Pensando 需要 AMD 的后盾，因为 Intel、Nvidia 和 Marvell 正在该领域的硬件和软件上重金投入；而 AMD 也需要这些 IP 用于数据中心和边缘。我们预计 Intel 凭其 Mount Evans ASIC 将成为 2023 年出货量最大的 DPU 供应商，但 DPU 市场仍处极早期，格局不断变化。

> x86 当然是我们很多计算方案的基础，但我们也都清楚 ARM 有很强的势头。坦率地说，我们的 Xilinx 路线图和 Pensando 路线图都会使用 ARM。在这种定制环境下我们也会用——说到底，技术选择权在客户。
>
> AMD CEO 苏姿丰博士（Dr. Lisa Su）

另外有个有趣的题外话：[Locuza](https://twitter.com/Locuza_/status/1535395024669749249?s=20&t=Zerg8R4eX2kFHkCN8rdm1Q) 发现 AMD 展示的那张裸片图（die shot）号称是 7nm Elba，实际上是 16nm Capri 芯片的。做这些幻灯片的营销人员该打手心了！

# **FPGA、自适应计算与 AI Engine**

总体而言，我们并不是 FPGA 最大的多头。纯 FPGA 业务——包括 Xilinx、Lattice 和 Intel 的 FPGA——增速应会跑输半导体大市。AMD 把这些终端市场吹得很响，但随着市场成熟并达到临界规模，更硬化的解决方案会被创造出来，承接该市场的采用与增量增长。这种事过去发生过很多次，而随着开放小芯片生态的到来，它只会加速。话虽如此，Xilinx 拥有的 IP 对赢得其他大得多的 TAM 至关重要。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d31aaa8a-59d9-4102-bcb1-a8dd6c4b9fab_1024x573.png)

Xilinx 开发的 AI Engine（AIE）将顺利切入众多市场。AMD 有多款包含该 AI 引擎的产品在开发中。这项工作早在 AMD 收购 Xilinx 之前就以授权合作的形式启动，所以产品会来得比较快：AMD 的消费级笔记本 SoC 明年搭载，数据中心 CPU 则在 2024 年搭载。

AIE 还打开了其他许多市场。电信市场可以通过 AMD 的电信 CPU 路线图及那里的半定制项目用上它。这个 AI 引擎对 FEC、波束赋形和许多其他用例都很有用。同样，它在数据中心和电信网络市场中也可用于安全和威胁检测。它还可以用于各种自动驾驶应用的半定制汽车项目。这个 IP 与 AMD 是天作之合——他们正缺 AI 能力，而它可以进入所有新兴的、新潮热词满天飞的环境，正是这些环境将让 AI 在未来成为一个庞大的产业。

这个 AI 引擎应该高度可扩展、速度快，并横跨许多不同产品品类通用。它是一种空间数据流（spatial data flow）架构，与包括 GPU 在内的许多现有 AI 加速器的运作方式截然不同。简言之，它是一种瓦片式（tiled）架构，带本地内存和本地 x、y 方向的数据移动。它可以向上扩展，但在为训练吞吐海量数据方面会比较吃力。它应该更擅长推理——而推理才是与 AIE 将进入的所有终端市场更相关的东西。

软件层面是最有趣也最重要的部分。如果 AMD 能搞定这一点，他们将打出一记全垒打。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/cf7ded2a-7389-42a6-8ccc-08602d9489c3_1024x574.png)

AMD 的 CPU、GPU 和 Xilinx AI 引擎各有独立的软件平台。他们宣布将把统一到面向 AI 开发者的 Unified Inference Frontend 之下。这有点像 Intel 在 OneAPI 上做的事（见幻灯片），但其实更接近 Intel 的 OpenVINO。OneAPI 反响寥寥，而 OpenVINO 则大获成功。AMD 要在这一领域追平还有很长的路，但这是一个扎实的计划。

第一代将统一剪枝、量化和推理部署，本质上是一个通用的模型优化框架。第二代将统一图编译器，并带来一个通用的推理算子库。要追上 Intel 的 OpenVINO 还有很多工作要做，尤其是应对栈更下层的严重碎片化，但这是一个扎实的开局。

从纯 FPGA 角度看，另一个有意思的披露是 Xilinx 将完全跳过 5nm。鉴于台积电 3nm 众所周知的问题，以及其 5nm 技术出色的爬坡和性能表现，这显得有些奇怪。Graphcore 也在做同样的事，跳过了 5nm。

# **客户端**

在我们看来，新的 $50B PC TAM 纯属扯淡。这需要 PC 市场达到 ~4.5 亿台的规模，在过去十年之后这很难想象。PC 的总 TAM 不会以 AMD 或 Intel 预期的速度扩张。这里我们没什么多说的，除了：AMD 会稳步获取份额，但速度远不及数据中心。这些增长几乎将全部来自笔记本市场的高端。

AMD 不会在低端与 Intel 打价格战，他们也不想。Phoenix 和 Strix 应该在能效和 GPU 方面击败 Intel，这会让他们在高端持续加速。AMD 理所当然地聚焦于能发挥其 IP 优势的地方——高端笔记本。笔记本市场的低端和大部分台式机市场，则是 Intel 可以继续秀 IDM 肌肉的地方。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a06c8dd6-089c-4f23-bee7-fa3a8e89b6a0_1024x558.png)

游戏业务不错，但关键要看 AMD 能否打破 Nvidia 的心智份额和功能优势。AMD 这一代没有性能领先，下一代也不会。除非连续几代占据「图腾」地位，否则这种心智份额不会打破。话虽如此，AMD 与 Nvidia 的硬件差距正在快速消散，但这正是 Nvidia 靠软件功能和心智份额遥遥领先的原因。

# **财务与该不该买？**

到这里要戴上金融的帽子了。我们将讨论为什么我们会在短期和长期内买或不买这只股票，以及围绕这只股票竞争格局的更多内容。这些将在仅限订阅者的章节中进行。

[分享](https://newsletter.semianalysis.com/p/amd-to-infinity-and-beyond?utm_source=substack&utm_medium=email&utm_content=share&action=share)
