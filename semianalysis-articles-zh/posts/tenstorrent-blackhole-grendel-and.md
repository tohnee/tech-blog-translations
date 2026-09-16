---
title: "Tenstorrent Blackhole、Grendel 与 Buda——面向稀疏性、条件执行与动态路由的横向扩展架构"
title_en: "Tenstorrent Blackhole, Grendel, And Buda - A Scale Out Architecture For Sparsity, Conditional Execution, And Dynamic Routing"
date: 2022-04-12
source: https://newsletter.semianalysis.com/p/tenstorrent-blackhole-grendel-and
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# Tenstorrent Blackhole、Grendel 与 Buda——面向稀疏性、条件执行与动态路由的横向扩展架构

> 原文：[Tenstorrent Blackhole, Grendel, And Buda - A Scale Out Architecture For Sparsity, Conditional Execution, And Dynamic Routing](https://newsletter.semianalysis.com/p/tenstorrent-blackhole-grendel-and) · SemiAnalysis

Tenstorrent 是领先的 AI 创业公司之一，拥有最有意思的架构与软件栈之一。他们身后有惊人的热度，部分因为其 CTO 是传奇人物 Jim Keller，也因为他们以一种独特的方式思考 AI 问题。多数 AI 创业公司在软件上疲于奔命，交付的硬件即便在最乐观的场景下也只是勉强超过 Nvidia，与此同时还完全无视神经网络与 AI 模型架构的演化方向。Tenstorrent 至少把这一切翻转了过来。他们对神经网络模型架构的未来、边缘与数据中心的矛盾、硬件性能/能效以及软件实力，做出了一些非常大胆的论断。此外，Tenstorrent 所讲的很多东西，与 Google 在其 5400 亿参数 PaLM 模型上分享的内容直接呼应。

我们推荐你阅读[我们去年关于 Tenstorrent 硬件、系统与软件架构的前作](https://semianalysis.substack.com/p/tenstorrent-wormhole-analysis-a-scale?s=w)。文中讨论了 TenSix 核心、Jawbridge、GraySkull 与 Wormhole 芯片架构的演化，还讨论了 Nebula 与 Galaxy 系统级设计，以及运行微型张量（mini-tensor）图的软件架构。独特的软硬件组合允许无约束的模型并行与流水线并行，不存在任何严格的层级。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/838d4bbb-a79d-4c08-95f7-24266cb7f29f_1024x569.jpeg)

先来谈谈当前的神经网络：它们正趋向更大更宽的模型，包含巨大的稠密矩阵乘法，例如多层感知机网络。其中有大量包含可学习参数的矩阵乘法，也有包含不可学习参数的矩阵乘法。还会有一些简单的变换，比如 SoftMax 函数，但在大多数情况下，最主要的限制因素是海量的矩阵乘法。

模型的演化总体上是在利用 GPU 硬件，而 GPU 也在演化以加速社区整体正在开发的那些模型。由此形成了一个反馈回路：模型架构朝着在 GPU 架构类型上表现最好的（可能的）局部最优点发展。大矩阵和高 batch size 被视为解决一切扩展问题的铁锤，好让模型规模得以继续指数级增长。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ff67028f-135e-4fd5-805b-ba68599b233b_1024x565.jpeg)

任何不聚焦于这些的 Nvidia 挑战者架构，都已被远远甩在身后。例如，Graphcore 的架构在分组卷积上表现极佳。他们的硬件能够以极低的 batch size 以及更小的矩阵尺寸进行训练而不摧毁利用率，但这无关紧要，因为大多数在研或生产中使用的模型，采用的是矩阵更大、batch size 更高的另一类模型架构。

这是一个对 AI 创业公司颇为不利的恶性循环。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ecab7735-59cd-48e6-88eb-51f6af0c8102_1023x547.jpeg)

Tenstorrent 相信神经网络正在迎来变化。他们认为，模型不会沿着当前大型 transformer 模型带我们走的那条路继续下去，而是会变得更具条件性——既混合当前的范式，也嵌入排序等程序化功能，后者需要矩阵乘法之外的更多异构计算。他们还相信，模型会演化出更多运行时条件路由：模型某一部分的计算结果，将决定数据随后被送入模型的哪一层。

这些具有更多条件路由的模型，对 GPU 而言可能是利好，因为 GPU 在时间上按顺序执行各层，可以轻松改变层序、做循环或任何其他条件操作。GPU 的许多问题都可以通过增大 batch size 来解决。而许多 AI 创业公司那样的流水线架构，要在不牺牲性能的前提下做条件路由，难度会大得多。这些创业公司往往把网络编译好，并按某种特定模式将其铺在裸片上。Tenstorrent 或许能在模型不同部分的细粒度路由上占据优势。这些操作需要片上更多的 SRAM，而 Nvidia 的 GPU 一般并没有巨大的 SRAM 池。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

条件路由如今在研究和使用上都还处于萌芽期，但 Tenstorrent 设想的未来是：构建一个单一的、规模极大的、高效的、但计算成本极其高昂的神经网络。这个模型运行在数据中心。而在边缘端，摄像头或传感器只搭载神经网络的一个片段，负责一些预处理，并自然地与该模型的其余部分对接。他们把这种架构比作人类或动物：眼睛与肢体自帶神经元，但大脑才是中枢。

> 这个世界将走向：全部周期中的 80%、90%，都将是运行在由数据编程的 AI 处理器上的 AI 周期。
>
> Jim Keller，Tenstorrent CTO

Tenstorrent 给出了一个智能零售中模型需要异构计算的例子：可以有一个视频解码阶段、一些模型处理、数据库读写、进一步的模型处理，然后是视频编码。有意思的是，Tenstorrent 给出了这个例子，因为如今能提供这种单芯片方案的，只有 Intel 的客户端/边缘 CPU、Nvidia 的 GPU 以及 AMD/Intel 的 FPGA。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/898d4303-9f33-4f9e-93ad-6ed2cbf17c16_1024x550.jpeg)

Tenstorrent 还做出了一个非常大胆的论断：不应该区分数据中心机器学习公司与边缘机器学习公司，市场需要的是端到端的机器学习公司。Tenstorrent 相信，训练面向未来的神经网络与为这些模型运行推理之间存在强烈的兼容性动力。他们相信，将会出现能实现 10 倍训练加速的架构特有特性，而这些特性在模型部署到边缘时必须得以保留。他们相信，任何成功的架构都必须能够从 100 毫瓦扩展到兆瓦级。我们并不确定 Tenstorrent 进入智能手机与嵌入式等低功耗领域的策略是什么。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9b23a7e6-5344-47cd-886e-44957c72ea0d_1024x550.jpeg)

关于模型规模，Tenstorrent 非常强烈地反对模型规模增长的趋势。他们认为，神经网络的规模不可能再出现一次 GPT3 式的跃升——GPT3 比 GPT2 大 1,000 倍——因为单次训练的成本已达数千万美元量级。我们认为这些成本估计偏大，因为即便是大得多的模型，如 DeepMind 的 Chinchilla，成本大概也在 1,000 万美元左右。

Tenstorrent 坚信，无条件稀疏、条件执行与动态路由可以带来计算量的大幅下降，因为大模型的整个模块都可以被跳过。任何乘法中只要含有 0，就没有必要把计算做下去——结果已经已知。结构化稀疏（即 0 的位置已知）已在 Nvidia 等厂商的硬件中实现。Tenstorrent 想要更上一层楼。他们还希望能够条件化地执行网络的各个部分，并在满足特定条件时，动态地路由经过网络中相关的部分。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/58b68dea-034a-46b2-9668-7e887ac39fda_1023x563.jpeg)

这背后的灵感又一次来自人脑。取决于手头的任务，只有一部分脑神经元处于活跃状态。在 MRI 下进行的实验会显示，你在各种各样的任务中用到了整个大脑，但取决于具体任务，只有特定区域会被点亮。从生物学上讲，人类极其擅长稀疏、条件执行与动态路由。

这又引回 Tenstorrent 的愿景：单一、极大、高效、但计算成本极高的神经网络。怀抱这一愿景的远不止他们一家，Google 已经表明正沿着这条路疾驰。他们最近公开了 [PaLM 模型](https://ai.googleblog.com/2022/04/pathways-language-model-palm-scaling-to.html)，其训练使用了迄今最大配置的自家 TPU——横跨两个 TPUv4 Pod 的 6,144 颗芯片。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1a44de46-e6a0-4382-9549-0cf22b6379b4_1024x373.gif)

Google 挑战了「训练越来越大的模型是浪费」这一核心信念。该研究的[结果](https://analyticsindiamag.com/google-introduces-pathways-language-model-with-540-bn-parameters/)重申：更大的模型比更小的模型采样效率更高，因为它们能更好地应用[迁移学习](https://analyticsindiamag.com/transfer-learning-vs-federated-learning-a-comparative-analysis/)。[1](https://analyticsindiamag.com/the-bigger-the-better-google-ais-new-540-billion-parameter-model-palm/) 通过「Pathways」的使用，单个 AI 模型可以泛化到许多任务上，并且比单一模型更快地学会它们。

正如人脑因为已泛化于如此之多的其他任务，而能极快地上手新任务，神经网络亦然。不必动用整个网络来解决问题，一条通路（pathway）可以把任务路由经过模型的一部分，从而让推理在能耗与数据上保持高效。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

Tenstorrent 想打造运行巨型模型的硬件：这类模型能够承接大量各不相同的任务、将其应用于各种判据，并以高度稀疏的方式进行自我训练——给定的输入在矩阵稀疏性或路由中拥有独一无二的路径。

> 我们大约 5 年前创立 Tenstorrent，心中装的就是这些想法。我们想要一台计算机，它能从不到 1 瓦的微型部署扩展到数据中心规模的部署，并由同一套编译器栈、同一套软件栈作为目标。我们想要一台能让人工神经网络做到我们大脑所做之事的计算机。也就是说，对任何给定输入，无论训练还是推理，只点亮模型的 2%。
>
> Ljubisa Bajic，Tenstorrent CEO

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/44457387-829f-4f48-880b-384c2751279c_1024x566.jpeg)

我们在[去年的这篇文章中](https://semianalysis.substack.com/p/tenstorrent-wormhole-analysis-a-scale?s=w)详细解释过 Tenstorrent 的硬件，这里概括一下他们的战略。Tenstorrent 采用通用的 LPDDR 或 GDDR 内存而非 HBM，以便把资金最大限度地花在计算上，同时保持高带宽与高能效。「TenSix」是一组 RISC-V 核心外加一个包管理器（packet manager）。它把片上网络（NOC）送来的微型张量包接收到本地 SRAM 并转换数据类型，随后由 RISC-V 核心处理数据。包管理器再将其重新打包，并经片上网络（NOC）推送到下一个目的地的 TenSix 核心。这一网络延伸到其 NOC 上的众多 TenSix 核心，而该 NOC 可以借助片上以太网交换机跨芯片延伸。理论上，Tenstorrent 可以无限扩展至数千套系统而不产生软件问题，因为这片计算之海仍会透明地充当一个巨大的 TenSix 核心网状结构。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/93a75572-92e7-4c6c-b69a-323f5885c7b8_1024x544.jpeg)

我们在[去年的文章](https://semianalysis.substack.com/p/tenstorrent-wormhole-analysis-a-scale?s=w)中深度解析过其前身 Jawbridge 以及 Grayskull 和 Wormhole。Grayskull 是第二代芯片，采用 GlobalFoundries 12nm 工艺。Tenstorrent 声称这颗芯片的性能与 Nvidia 的 A100 GPU 相当，密度翻倍，功耗略低。但我们从一个评估过 Grayskull 的大型超大规模云厂商处获悉，它比 Nvidia 那颗 4.5 年前问世的 V100 还要慢上不小一截。

Tenstorrent 表示，到今年年底，数据中心将安装超过 1,000 张双 Grayskull 芯片卡。Tenstorrent 还声称，2022 年 Q1 将有一台约 1,000 颗 Wormhole 芯片的机器安装于数据中心。

新的硬件信息披露是 TSMC 6nm 的 Blackhole 与 TSMC 4nm 的 Grendel。Blackhole 大幅增加算力，新增 24 个从 SiFive 获得授权的 RISC-V CPU 核心，并把 16x100G 以太网升级到 12x400G。Blackhole 还把内存从 GDDR6 换成了 DDR5。这颗芯片预计今年流片。

Grendel 芯片将进一步增加算力，并升级到 64 个 RISC-V CPU 核心。这些核心将是自研设计，因为 SiFive 核心的性能不及他们内部所能研发的水平。Jim Keller 在演讲中把上一代 SiFive 核心的性能具体评价为「不算差」。以太网交换能力将再次扩展到 16x400G。这颗芯片预计「在 Blackhole 之后大约一年」问世，这指向 2023 年流片。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/02b798f6-aa67-44e2-baea-c8edc338c753_1023x595.jpeg)

Tenstorrent 的自研核心是 64 位乱序执行，凭借两个 256 位向量单元而相当宽。他们评价其性能大约与 Apple 老的 Cyclone 核心处于同一水平。核心本身为 1.2mm2。构建该核心的团队主要来自 Apple、AMD、Arm、Nvidia 和 Intel。Tenstorrent 谈到了他们声称相当独特的验证流程。他们有核心的参考模型和一个性能模型，把架构跑在性能模型与框图上。他们声称这使他们能够在流程中更早的阶段进行测试和验证。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/bfc8eacf-bfb1-4a02-8971-ecb553c9b073_1023x537.jpeg)

这些核心将以 8 个一组进行集群，组内共享 8MB L2 缓存。路由器系统将与 TenSix AI 处理器上的完全相同，因此 CPU 核心可以直接集成到 fabric 上。这使 CPU 核心与内存控制器及 AI 处理器之间保持缓存一致。这样做最大的好处是，他们不必去应对复杂的驱动模型——不需要 GPU 写入主机上的共享内存、再与 CPU 打中断交道。延迟也应低得多。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/879619e4-72d9-46cf-aaf5-f965bbf102d8_1024x564.jpeg)

这些 CPU 核心的用途，将从在更先进的 AI 模型内部承担异构计算，延伸到网络加速、存储加速，并使他们得以扩展到任意数量的 Grendel 服务器。Tenstorrent 暗示，未来甚至可能把这一核心授权出去供他人使用。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/cf4b09c9-d637-4d33-975e-909dc865d984_1024x531.jpeg)

Tenstorrent 将他们的软件平台命名为 Buda，这明显是对 Nvidia 软件栈 CUDA 的文字游戏。Buda 只兼容 PyTorch。该模块让你可以把模型自动或手动地放置到一台机器上，而这台机器可以从单芯片扩展到数千芯片，且全部在同一个 Python 解释器内完成。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

有命令可以连接各个模块，并为其提供连接所用的源点（source point）与同步点（sync point）。同步是内建的，连接既可用于训练中的反向传播，也可用于推理中的前向传播。Tenstorrent 声称，它比各种 MPI 衍生方案以及 Nvidia 用于集合通信的 NCCL 都更易用。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/2ba1cb7a-bbe2-41ea-ab43-254e4d8893af_1024x532.jpeg)

Tenstorrent 的软件与 CPU 无关，因此宿主可以是 Intel 平台、AMD 平台，或未来几代中集成进去的自家 CPU 核心集群。他们支持承载其他框架的模块，包括通用 Python 代码甚至可执行文件。例如，可以编写一个 C 程序，通过管道接收输入并输出数据。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/66b4419d-45f2-448a-a012-369c9039b028_1023x551.jpeg)

视频解码流水线可以用 FFmpeg 搭建，数据库也可以与之对接。这些特性支撑起 Tenstorrent 为 AI 模型架构未来所设想的异构计算。随着在其可扩展的 NOC 上加入非常通用的 CPU 核心、并具备执行任意代码的能力，其方案的灵活性是巨大的。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ecbebcbd-3795-4b9d-9477-650b258509cc_1024x547.jpeg)

Batch size 为 1 的运算通常受限于内存访问——无论是新数据的载入，还是从一个全连接层到下一个全连接层。这些运算通常需要整颗芯片一起运行才能加速，但它们不能一直干等数据。GPU 凭借其大矩阵尺寸，可以迅速解决大张量数组的运算。而对于小张量数组的运算，你就会撞上瓶颈，必须用大 batch size 来弥补。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d3bea665-74ce-447d-a18d-9e8b15b447a1_1023x546.jpeg)

任何跨核心的流水线，都会让条件计算变得非常棘手。Tenstorrent 谈到把运算或模型的某些部分布置在特定的核心、芯片等之上。如果存在被条件路由绕开的未用运算，那些核心就只能闲置浪费。我们并不确定 Tenstorrent 对这一情况的解决方案是什么。GPU 则是用全部核心一次执行一个运算，逐层推进。如果某一层被条件跳过，就减少了总计算量，模型也随之加速。

Tenstorrent 声称，他们的硬件方法对软件是巨大优势。其他公司必须应对经典的 load-store 架构来传递数据，因此必须投入大量精力手工编写把运算融合在一起的内核。Tenstorrent 表示，编译器层面的高质量融合至今仍未真正实现。这就决定了融合必须手工完成。

> 这解释了一些 GPU 厂商与其他 GPU 厂商在机器学习性能上的巨大差距。过去五年甚至更久，有些厂商为很多东西手工融合了大量内核，有些则没有。
>
> Ljubisa Bajic，Tenstorrent CEO

很明显，Ljubisa 在此以外交辞令暗指 Nvidia 与 AMD 之争。他们声称，这可能需要多达 2,000 人的团队，这对一家创业公司并不可行，而这也正是把他们逼上如今这条道路的原因。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a541fae2-13e1-45ed-97f2-9b72cf8e5236_1024x536.jpeg)

归根结底，软件的故事虽然动听，仍需拭目以待。硬件其实也一样。为横向扩展而生、并在性能上击败 Nvidia 的说法很好，但需要落地兑现。这家公司背后的哲学及其在硬件与软件上的决策令人兴奋，所以我们心怀希望。如果这家创业公司展现出真正的前景，我们认为 AMD 应当收购他们。在对 Intel 完成复兴、并收购 Xilinx 与 Pensando 之后，AI 与软件功力差不多是 AMD 仅剩的缺口。

[分享](https://newsletter.semianalysis.com/p/tenstorrent-blackhole-grendel-and?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

我们也建议你看看我们其他 AI 芯片报道。

[Tenstorrent Wormhole 分析——一种可能让 Nvidia 陷入被动的机器学习横向扩展架构](https://semianalysis.substack.com/p/tenstorrent-wormhole-analysis-a-scale)

[Cerebras 晶圆级硬件碾压高性能计算工作负载，包括机器学习及其他](https://semianalysis.substack.com/p/cerebras-wafer-scale-hardware-crushes)

[高通一击制胜：Cloud AI 100——面向边缘的强大 AI 推理](https://semianalysis.substack.com/p/qualcomm-hits-a-homerun-ai-100-powerful)——Facebook 是我们在这篇文章中讨论的那个超大规模客户，他们最终因软件问题退出。

[Graphcore 在机器学习训练性能上看起来是一场彻底的失败](https://semianalysis.substack.com/p/graphcore-looks-like-a-complete-failure)

[Tesla AI Day 超级计算机芯片预告 | 这是 TSMC InFO_SoW 的首次部署吗？](https://semianalysis.substack.com/p/tesla-ai-day-supercomputer-chip-teaser)

[Tesla Dojo——独特的封装与芯片设计带来相对竞争 AI 硬件的数量级优势](https://semianalysis.substack.com/p/tesla-dojo-unique-packaging-and-chip)

[Tesla Dojo 芯片令人印象深刻，但存在一些重大技术问题](https://semianalysis.substack.com/p/the-tesla-dojo-chip-is-impressive)

[Graphcore 发布世界首个 3D 晶圆对晶圆混合键合处理器——Bow、Good Computer 与晶圆对晶圆混合键合分析](https://semianalysis.substack.com/p/graphcore-announces-worlds-first)

[Tenstorrent Blackhole、Grendel 与 Buda——面向稀疏性、条件执行与动态路由的横向扩展架构](https://semianalysis.substack.com/p/tenstorrent-blackhole-grendel-and?s=w)

另外请保持订阅，我们将对 Nvidia 的 Hopper 架构做一次极深度解析，从底层功能单元一直讲到疯狂的系统级设计。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

[分享](https://newsletter.semianalysis.com/p/tenstorrent-blackhole-grendel-and?utm_source=substack&utm_medium=email&utm_content=share&action=share)
