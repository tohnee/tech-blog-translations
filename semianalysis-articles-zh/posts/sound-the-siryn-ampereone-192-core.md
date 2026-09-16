---
title: "号角吹响：AmpereOne 192 核 CPU"
title_en: "Sound The Siryn: AmpereOne 192-Core CPU"
subtitle: "小芯片、先进封装与不诚实的性能宣传"
date: 2023-05-18
source: https://newsletter.semianalysis.com/p/sound-the-siryn-ampereone-192-core
crawled: 2026-09-15
authors: ["Dylan Patel", "Gerald Wong", "George Cozma"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 号角吹响：AmpereOne 192 核 CPU

> 原文：[Sound The Siryn: AmpereOne 192-Core CPU](https://newsletter.semianalysis.com/p/sound-the-siryn-ampereone-192-core) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**小芯片、先进封装与不诚实的性能宣传**

Ampere Computing 专注于云数据中心市场的 CPU。该公司已成功赢得可观的市场采用，包括阿里巴巴、Google、Microsoft、腾讯和 Oracle 在内的多家主要云厂商都在以不同数量采购 Ampere 的芯片用于其云业务。此外，Ampere 的芯片也出现在 Cruise 的自动驾驶汽车中。仅 2022 年一年，[SemiAnalysis 估计 Ampere 出货了超过 300,000 颗 CPU](https://www.semianalysis.com/i/108660819/arm-at-aws)。

![](https://substack-post-media.s3.amazonaws.com/public/images/cf264df7-7e8c-486b-bd36-b5f5f90b7554_4000x2250.png)

今天，Ampere Computing 发布其第三代数据中心 CPU——代号 Siryn 的 AmpereOne。这对该公司而言是一个重大转变，因为这是其首款采用自研架构的产品。Ampere Computing 此前使用 Arm 的 Neoverse 核心，但如今他们已成功挣脱 [Arm 昂贵且受限的核心授权条款](https://www.semianalysis.com/p/arms-nuclear-option-qualcomm-must)的枷锁，[转投自由度更大的 Arm 架构授权](https://www.semianalysis.com/p/arms-nuclear-option-qualcomm-must)。

今天我们将深入剖析 Ampere Computing 新 CPU 的性能、竞争定位、战略和财务细节，以及他们即将进行的 IPO。我们并不认同这家公司对外宣传的一切，认为他们的部分对比简直是不诚实的。在批判性分析他们的发布内容之前，先快速概览一下这家公司。

## **云原生——是营销话术吗？**

Ampere Computing 的主要战略是设计和交付专为云数据中心打造的 CPU。这一总体战略可以归结为两个字：「云原生」。AMD 和 Intel 必须让他们的 CPU 面向从各类企业级到云端的各种工作负载——从存储服务器、Web 服务器到基于加速器的 AI 系统。AMD 和 Intel 为这些应用设计的 CPU 核心，往往只需少量修改就能进入笔记本等客户端计算场景。Ampere 的主张是，他们可以只聚焦数据中心中增长最快的细分市场——云，并为之优化产品。

![](https://substack-post-media.s3.amazonaws.com/public/images/7fba4ff6-5826-407a-aae2-9565a8ab0c56_4000x2250.png)

他们相信，计算的未来将在很大程度上依赖微服务、容器化和 [serverless](https://en.wikipedia.org/wiki/Serverless_computing) 执行模式。这些概念的核心是通过大量小任务和小进程横向扩展性能，而不是过度执着于单线程 CPU 性能。AMD 和 Intel 未来一年内也将发布采用类似策略的 CPU。Ampere 认为他们的 CPU 在三个方面是「云原生」的：

1. 更高的单 CPU 性能
2. 可预测的性能
3. 可扩展性

下面拆解他们的架构如何实现这些目标。Ampere 相信，更高的核心数可以带来更高的性能。而更高的核心数只有通过有意识的工程取舍——采用比 Intel 和 AMD 更小的核心——才能实现。需要指出，在每线程性能尤其是浮点性能上，Ampere 核心显著落后于 AMD 和 Intel。他们押注的是：这些更小的核心带来更高的每晶体管性能和每瓦性能，从整颗芯片的全局视角看，就能实现更高的整体性能。我们将在报告的性能部分讨论这一判断是否成立。

Ampere 还相信，通过每核心只运行 1 个线程，他们能提供更可预测的性能。Intel 和 AMD 提供每核心 2 线程的同步多线程（[SMT](https://en.wikipedia.org/wiki/Simultaneous_multithreading)）。SMT 利用工作负载中的空隙（主要由[等待内存](https://www.semianalysis.com/i/97006309/the-memory-wall)造成），让硬件执行资源以更高利用率运转。SMT 在几乎不增加每核心硅面积和晶体管数的情况下提升性能。

SMT 的缺点是，多个线程共享核心资源可能导致性能不可预测。另一个潜在缺点是安全性。利用 SMT 漏洞是[侧信道攻击](https://en.wikipedia.org/wiki/Side-channel_attack)的常见手段，自 [Spectre](https://en.wikipedia.org/wiki/Spectre_(security_vulnerability)) 和 [Meltdown](https://en.wikipedia.org/wiki/Meltdown_(security_vulnerability)) 问世以来，这类攻击已大规模泛滥。

Ampere「更可预测性能」的宣传也延伸到其缓存架构。每个核心都有大容量私有 L2 缓存，而共享 L3 缓存则相当小。AMD 和 Intel 通常依赖更大的共享 L3 缓存，这在许多工作负载中有助性能，但也会损害性能的可预测性。

Ampere 还非常强调时钟频率的一致性。Intel 和 AMD 的 CPU 会根据正在使用的核心/线程数以及执行的代码类型大幅调整核心时钟频率。这帮助它们的 CPU 在给定功耗和散热预算内最大化性能，在许多工作负载中是巨大优势。

Ampere Computing 却舍弃了这一点，转而不论工作负载如何都保持时钟频率恒定，以提升性能可预测性。这一决策的理由是：云工作负载是多租户的。如果用户因时钟加速而获得了更高性能，他们可能习以为常。而当这些加速频率因「吵闹邻居」虚拟机的起停而被拿走时，用户的性能就会受影响。Ampere 通过锁定时钟频率，实际上是在对性能做出保证。新一代的时钟频率为 2.8GHz，较上一代略有下降。

「云原生」CPU 战略的许多要素正被 Intel 和 AMD 在即将推出的 Sierra Forest 和 Bergamo 产品架构中采纳。两者都瞄准云工作负载，并将在未来一年内发布。所有这些 CPU 的总体目标都是提升能效、提高性能、缩减数据中心的总足迹——随着数据中心功耗持续飙升，这一点必不可少。

## **AmpereOne——Siryn**

回到今天的发布：Ampere 沿着这条路线继续前行，推出了全新的 192 核 CPU，采用自研 CPU 核心，上一代为 80/128 核。Ampere 转向 DDR5 内存和 PCIe Gen 5，大幅提升了 IO 吞吐。此外，Ampere 还增加了大量提升一致性的特性，以及协助云厂商部署的高级机群与生命周期管理功能。

![](https://substack-post-media.s3.amazonaws.com/public/images/f1db1547-0274-4c87-b708-2b025d479eb7_4000x2250.png)

- Mesh 拥塞——当核间通信或核到内存/IO 的通信路径发生拥塞时，尝试经由 mesh 上其他较不拥塞的路径重新路由。
- 嵌套虚拟化支持——允许云厂商的租户在其已是虚拟化的环境中再运行虚拟机，且几乎没有性能损失。
- 电压跌落检测与工艺老化监控——协助管理芯片随使用逐渐老化的问题，防止不稳定。
- 安全——安全虚拟化、单密钥内存加密、内存标记等特性，让云租户在共享内存控制器和 DRAM 颗粒的情况下仍能确保数据安全。这些特性还有助于防范缓冲区溢出攻击，并提升数据库的数据完整性。

Ampere 新设计中最有趣的当属其架构。Ampere 转向了小芯片（chiplet）式架构，CPU 核心采用 TSMC 5nm，内存控制器和 PCIe 控制器则由 IO 裸片承担。其物理配置与 Amazon 的 Graviton3 类似，同样使用 AMBA CHI 连接各小芯片。

Ampere 采用小芯片式方案的意义在于：他们可以再设计一颗新的 CPU 核心裸片，明年推出核心数超过 192 的升级版。

![](https://substack-post-media.s3.amazonaws.com/public/images/7dd4234b-4e7c-4577-b713-fd44c5bba947_1953x2218.png)

[分享](https://newsletter.semianalysis.com/p/sound-the-siryn-ampereone-192-core?utm_source=substack&utm_medium=email&utm_content=share&action=share)

我们利用该公司在 [ISSCC 2022](https://youtu.be/C5-gM5xVHSI?t=1730) 上展示的 Altra 平面布局，对新 AmpereOne A192「Siryn」小芯片设计做了一个示意图。我们的示意图采用了与 Graviton3 相同的小芯片布局，因为两者使用类似的 mesh 和小芯片互连接口。这种配置在不同大小的虚拟机之间都提供了易于配置的性能和可预测的性能表现。4 核虚拟机换成 32 核虚拟机，CPU 吞吐量基本呈线性扩展。这与 AMD 采用的小芯片设计正好相反——AMD 是多颗核心小芯片环绕中央 IO 裸片。需要跨越多颗核心小芯片的大型虚拟机，相比能完整待在单颗小芯片内的虚拟机，会出现性能不一致。

值得注意的是，Ampere 声称这颗芯片已经打样一年，却直到现在才进入量产。这暗示[他们需要重新流片几次才能把芯片做对](https://www.semianalysis.com/p/the-dark-side-of-the-semiconductor)。虽然这很痛苦，但比起 Intel [把 Sapphire Rapids 做对](https://www.semianalysis.com/p/intel-emerald-rapids-backtracks-on)所经历的 [12 次重新流片和超过两年半时间](https://www.semianalysis.com/p/the-dark-side-of-the-semiconductor)还不算糟。

## **封装与热设计**

![](https://substack-post-media.s3.amazonaws.com/public/images/acf87bf3-1ac0-4f97-bb84-e373334b407a_624x590.png)

Ampere 现有的 Altra 产品线采用大型单片裸片，功耗水平也相对温和，因此不需要复杂的封装和热设计。裸片直接坐在普通有机基板（LGA 4926）上，裸片与大型集成散热顶盖（IHS）之间填充聚合物热界面材料（pTIM）来散热。

![](https://substack-post-media.s3.amazonaws.com/public/images/7597d70d-635b-4985-8794-cb8ebb654cb3_1096x869.png)

AmpereOne 改变了这一切。IHS 被取消，Ampere 改用裸片直触（Direct Die）接触设计，配上又大又厚的加固环，与我们在 GPU 和移动 CPU 上所见类似。但那些是焊接 BGA 封装，而 AmpereOne 要插入 LGA 5964 插槽。裸片直触方案让散热器冷板尽可能贴近发热的硅片，减少了热阻层，有利于温度控制。

随着使用功耗飙升至 350W、峰值功率场景下甚至更高，封装的热设计正受到更多审视。Amazon 在从 Graviton2 到 Graviton3 的换代中也从 IHS 转向了裸片直触。与此同时，数据中心 CPU 的在位厂商（Intel、AMD）暂时仍坚持带钎焊 TIM 的传统 IHS。

虽然 Ampere 说 Siryn 是小芯片设计，但封装的直观照片上只能看到单一的一颗大裸片。我们对这一观察的解释是：可见的只是一片载具晶圆（carrier wafer），位于所有小芯片之上。在先进封装过程中，所有小芯片先键合到载具晶圆上，随后切割并通过[细间距小芯片互连（InFO、CoWoS-R、FoCoS）](https://www.semianalysis.com/p/the-future-of-packaging-gets-blurry)贴装到基板上。

小芯片之上的这层结构硅不仅为第三方散热器安装所需的裸片直触设计提供了额外的结构刚性与耐久度，还充当硅质均热片，帮助熨平热点，把滚烫的核心小芯片上的热量摊到较冷的 IO 小芯片上。由于材料与下方计算和 IO 裸片相同，它在反复冷热循环中将热膨胀系数（CTE）失配降到最低，提升了结构可靠性。

虽然这层顶部硅让我们无法看到实际小芯片的裸片面积，但它确实显示出封装有多大。顶部裸片应已接近光罩极限，这意味着封装尺寸约为 90mm x 70mm。这比当前任何在售的数据中心 CPU 都大。他们在 OCP Summit 2022 上公布的 Mt. Mitchell 平台 LGA 5964 主板原理图也显示出插槽有多大。

![](https://substack-post-media.s3.amazonaws.com/public/images/9addad01-f93a-4122-a88c-33e137bbf3dc_868x913.jpeg)

此外，Mt. Mitchell 还将提供一个正在开发中的 12 通道 DDR5 版本的 AmpereOne，每插槽内存带宽提升 50%。

![](https://substack-post-media.s3.amazonaws.com/public/images/671f5e02-a55c-4f13-afba-13dd656515c3_823x868.png)

这个 12 通道版本的内存带宽将追平 AMD 的 Genoa 和 Bergamo。其核心数也将超过 192 核。

## **性能——不诚实且不公平的对比**

![](https://substack-post-media.s3.amazonaws.com/public/images/dcef04b3-18f6-4c11-9054-144bbba9d70c_4000x2250.png)

Ampere 从不喜欢谈单核或单插槽性能，而是偏爱坚守他们的「每机柜性能」指标。大多数较老的数据中心按每服务器机柜约 14 至 20 kW 的供电和散热能力设计。机柜能容纳的单元数各不相同，但通常在 42U 左右，单台服务器依系统架构占用 1U 到 8U。

随着 CPU TDP 飙升，这些典型数据中心机柜如今受限的更多是功率而非空间。把机柜塞满高功率 Xeon 的高密度刀片服务器，会把功率预算超支许多倍，需要散热能力更强的专用数据中心基础设施。Nvidia 的 AI 服务器也是如此。由于功耗巨大，其 DGX SuperPOD 设计无法在每个机柜内满配服务器。Nvidia AI 服务器通常高达 5U 到 6U，A100 DGX 服务器约 6.5 kW，H100 则是 10.2kW。

Ampere 声称，在行业标准 SPEC CPU2017 Integer Rate 工作负载下，AmpereOne A192 单插槽服务器功耗 434W，AMD EPYC 9654 Genoa 为 624W，Intel Xeon 8480+ Sapphire Rapids 为 534W。按每机柜 16.5 kW 功率预算计算，一个机柜可以带动 38 台 AmpereOne 服务器、30 台 Intel 服务器或 26 台 AMD 服务器。把每台服务器的 CPU 核心数乘以每机柜的服务器数，并假设采用单核虚拟机，就得到了他们的宣传口径：AmpereOne 可承载的虚拟机数量是 x86 阵营当前最佳产品的 2.92 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/0e9c9c6c-2afb-4911-a321-945191862111_1438x574.png)

虽然这个指标对那些追求在每台服务器机柜里塞进尽可能多虚拟机客户的人有用，但它忽略了性能维度——如果客户只需要「够用」的每核性能水平，那倒无妨。我们提取了 SPEC CPU2017 的提交结果，展示当前 Altra 与市面上 CPU 在每核整数性能上的悬殊差距。

[分享](https://newsletter.semianalysis.com/p/sound-the-siryn-ampereone-192-core?utm_source=substack&utm_medium=email&utm_content=share&action=share)

虽然 AmpereOne 的每核整数性能无疑会比 Altra 更好，但我们看不出它能接近 AMD 或 Intel 的水平。此外，竞争对手的 CPU 都是开箱即以最大单插槽性能和高功耗运行。人们总可以在性能/功耗曲线上找到一个更高效的点——多花钱、把功率调低，从而在每机柜塞进更多 CPU。

Ampere 没有披露 SPEC integer rate 成绩，但如果按每机柜性能来衡量，AmpereOne 会与竞争对手接近得多，尤其是面对即将推出的 128 核 Bergamo 处理器。另外请注意 Ampere 处理器的整数加权成绩。其瞄准的云原生工作负载主要侧重整数性能，这与 NVIDIA Grace 超级芯片应当擅长的 HPC 工作负载正好是两个极端。

![](https://substack-post-media.s3.amazonaws.com/public/images/896ab7e1-96a4-4348-8b02-8555ee375504_4000x2250.png)

到了这里，对比开始变得非常不公平。在 Stable Diffusion 测试中，AmpereOne 配置了 160 核、512GB DDR5 和 Linux 内核 6.1.10，而 AMD 的 Genoa 却被束缚了手脚：内存只有一半的 256GB，12 通道内存只插了 8 条，跑在更旧的 5.18.11 内核上。此外，他们给 Genoa 只开了 96 个线程，而给 AmpereOne 开了 160 个线程。Genoa 通常需要全部 12 通道内存和 192 个线程（利用 SMT）才能达到最高性能。

不诚实的设置还不止于此。在 DLRM 测试中还有一个额外差异：AmpereOne 使用 FP16 数据格式，而他们的 AMD 系统被配置为使用 FP32 数据格式。[更高精度的数据会给这些受内存限制的 AI 工作负载带来更大的内存压力](https://www.semianalysis.com/p/on-device-ai-double-edged-sword)，进一步损害性能。

这实在不可原谅，因为两款处理器都支持低精度的 BF16 格式，本可以使用。虽然我们预期 AmpereOne 的 AI 性能会很出色，但完全没有必要在测试设置上做手脚把差距拉得更大。Ampere，你真丢脸。

蹊跷的是，AmpereOne 在 AI 工作负载下的功耗远高于 SPEC integer rate：SPEC 下 192 核整机功耗 434W，而 Stable Diffusion 下 160 核功耗 534W。Genoa 却正相反：SPEC 下 624W，Stable Diffusion 下只有 484W。这表明两款处理器之间存在性能优化上的差距，也表明 Genoa 可能因 Ampere 的手脚而未被充分利用。

[分享](https://newsletter.semianalysis.com/p/sound-the-siryn-ampereone-192-core?utm_source=substack&utm_medium=email&utm_content=share&action=share)

## **核心微架构**

Ampere 的自研核心微架构，相对其此前从 ARM Ltd. 授权的 Neoverse N1 核心是一次有趣的混合改动。其一，他们把流水线数量从 8 条增加到 12 条：增加了第 5 个整数 ALU、2 个额外的 load/store AGU，以及一个专用浮点存储单元，该单元还能做浮点到整数的转换。为应对增加的流水线和执行单元，Ampere 重新调整了 N1 的调度器布局。

N1 上有 8 个独立调度器，而 AmpereOne 也有 8 个调度器，其中 4 个服务整数侧，2 个服务浮点和向量单元，2 个服务内存侧。参考 [LLVM 补丁](https://github.com/llvm/llvm-project/blob/64816e68f4419a9e14c23be8aa96fa412bed7e12/llvm/lib/Target/AArch64/AArch64SchedAmpere1.td)，我们认为调度器布局如下图所示。

![](https://substack-post-media.s3.amazonaws.com/public/images/ba36c029-4465-4bdd-8b19-7da1fe9429b6_935x230.png)

再看核心其余部分，AmpereOne 的重排序缓冲区（ROB）据报道为 174 项，对于现代高性能核心而言很小，但相比 N1 的 128 项 ROB 已是可观的提升。这让 AmpereOne 相比 N1 获得更好的指令级并行度，核心同一时间能处理更多操作。

在 load/store 系统方面，Neoverse N1 限于每周期 2 次 128b load，或 1 次 128b load 加 1 次 128b store。在 AmpereOne 上，这一上限提升到每周期 2 load 和 2 store。我们不知道 2 load 2 store 是否同样适用于 128b 操作，但我们认为 AmpereOne 很可能可以每周期做 2 次 128b load 和 2 次 128b store，让 load/store 带宽翻倍。

AmpereOne 的缓存子系统也有显著变化。L1 数据缓存与 Neoverse N1 一样是 64KB 4 路组相联，而 Ampere 把 L2 缓存从 1MB 8 路翻倍到 2MB 8 路，有助于把数据留在核心附近，这对云工作负载很重要。

Ampere 还改变了 L3 布局。Ampere 表示，他们的 64MB「L3 缓存」更像 Apple 的 SLC——它是一个内存侧缓存，而不是 AMD、Intel 使用的那种传统 L3 缓存。他们还表示使用的是 ARM 的 CMN mesh，但除了拥有 64 个分布式主节点和基于目录的侦听过滤器以实现核心间无缝连接之外，没有过多谈及 mesh 布局。他们如何做到 192 核配 64MB LLC，我们并不清楚，Ampere 此刻也没有给出答案。一种 L3 排布方式是沿用 Altra 的做法：把 L3 摊到 mesh 网络各处，但并非所有带 4 核集群的 mesh 节点都包含 L3。另一种是把所有 L3 成大块放在 DDR5 内存控制器旁边，类似于 AMD Infinity Cache 等其他内存侧缓存。

真正有趣的变化是 L1 指令缓存从 64KB 4 路缩减到 16KB 4 路。这是一个耐人寻味的举动，我不知道它是否有利于性能。传统上，更大的 L1 指令缓存（L1i）被认为是更好的，因为待在最靠近核心的缓存里，比跑到 L2 缓存等更高层级的缓存能效高得多，带宽也更高。

至于后一点——L1 带宽高于 L2——在 AmpereOne 上很可能不成立。我们不知道 L1i 缓存的带宽，也不知道 L2 与 L1i 之间的带宽，但从 L1i 到核心其余部分的带宽很可能是每周期 16 字节。大多数 ARM 指令长 4 字节，而 AmpereOne 是 4 宽解码。因此，为了让核心持续吃满新指令，AmpereOne 的取指带宽很可能是每周期 16 字节。L2 缓存到 L1i 的链路很可能也是每周期 16 字节，因为每周期 16 字节的 L1i 链路在现代 CPU 核心中相当常见。

![](https://substack-post-media.s3.amazonaws.com/public/images/ae601fad-2f14-44af-9cd9-8703f4efb994_1300x971.png)

但就前一点而言，我们不知道 Ampere 为什么砍掉 L1i 容量，但至少能想到两个原因。缩减 L1i 是为了省面积——L1i 使用的是可及性极高、密度很低的 SRAM，砍到 16KB 可以省下大量面积。另一个原因是，他们画像的负载从 16KB 到 32KB 再到 64KB 的收益递减明显，比如 SPEC INT 2017 在指令侧的负荷并不重。

我们怀疑，这很可能是这些因素与其他压力共同作用的结果。不过，这是一颗云端处理器，即便他们有重点关注的工作负载，它也必须是一颗对通用工作负载足够好的 CPU 核心。

## **IPO、超大规模厂商自研芯片与 AMD/Intel 竞争**

接下来我们想讨论 IPO、竞争加剧下的长期前景、AMD/Intel 的回应、RISC-V 生态，以及 Amazon、Google、Microsoft、阿里巴巴等超大规模厂商的自研路线图。
