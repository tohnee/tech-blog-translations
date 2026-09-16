---
title: "Tenstorrent Wormhole 解析——一套可能让英伟达陷入被动的机器学习横向扩展架构"
title_en: "Tenstorrent Wormhole Analysis - A Scale Out Architecture for Machine Learning That Could Put Nvidia On Their Back Foot"
date: 2021-06-25
source: https://newsletter.semianalysis.com/p/tenstorrent-wormhole-analysis-a-scale
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: everyone
paywalled: false
translated: 2026-09-15
---

# Tenstorrent Wormhole 解析——一套可能让英伟达陷入被动的机器学习横向扩展架构

> 原文：[Tenstorrent Wormhole Analysis - A Scale Out Architecture for Machine Learning That Could Put Nvidia On Their Back Foot](https://newsletter.semianalysis.com/p/tenstorrent-wormhole-analysis-a-scale) · SemiAnalysis

作为最炙手可热的 AI 初创公司之一，Tenstorrent 获得了大量媒体报道。除了颇具前景的软硬件设计外，部分热度来自他们拥有半导体界的泰斗级人物 Jim Keller。早在公司初创、他还在特斯拉（Tesla）任职时，就是其投资者。结束特斯拉的任期后，他先后任职于英特尔（Intel），最终于 2021 年初正式加盟，出任 CTO。

Tenstorrent 采取了软硬件深度交织的独特路线。硬件面向任务高度专用，软件却并不复杂得离谱。整个软件栈只有约 5 万行代码。与大多数需要定制开发管线的 AI 专用 ASIC 不同，Tenstorrent 在支持所有主流工具链、框架和运行时的同时，保持极强的适应性与灵活性。英伟达（Nvidia）最大的优势——开发极其容易——正受到挑战。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/333ce7d8-f5e8-4508-876a-21d3b77473dc_1024x527.jpeg)

要理解他们的架构和 Wormhole 处理器，我们不妨回溯其前代的历史与血脉。Jawbridge 是一颗小型测试芯片，作为该架构的概念验证而开发。它由一组 Tenstorrent 自研的「Tensix」处理核心组成，通过自研的片上网络（NOC）互连，再搭配授权而来的 I/O 模块，如 LPDDR 内存控制器和 PCIe 根复合体。片上 CPU 核心可以管理负载并运行 Linux。

Jawbridge 是一颗极小的芯片，功耗需求极低。凭借紧巴巴的预算，他们完成了这颗芯片的流片，并验证了其亮眼的功耗/性能宣称。有了这份概念验证打底，他们得以募集更多资金，向下一代推进。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/46d44cdb-8ab8-4f65-8678-ae6a9f7ecf49_1024x521.jpeg)

GraySkull 是下一步演进，而且是一款商业化产品。这颗芯片拥有 128 个 Tensix 核心，至关重要的 NOC 大幅扩展，I/O 规模也大得多。这颗芯片采用 GlobalFoundries 12nm 制程，面积为 620mm^2。Tenstorrent 设计功力的最好证明是：他们出货的是 A0 版硅片。这意味着他们把芯片设计对了，首次流片就没有发现任何勘误（erratum）。即使对 AMD、苹果（Apple）、英特尔、英伟达这些公司经验老到的团队而言，这样的壮举也相当罕见。

GraySkull 是一颗 65W 的芯片，而 PCIe 扩展卡的整卡功耗为 75W。这意味着它可以轻松插入现有服务器，无需任何额外的辅助供电。完成流片和送样之后，Tenstorrent 又筹集到更多资金投入下一代芯片。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/9d118b4d-f5b5-4566-9b6c-3dc252c06a90_2427x1197.jpeg)
![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b71208f7-225b-44d6-8c98-bef81189220b_2479x1202.jpeg)

于是我们来到了 Wormhole：同样基于 GlobalFoundries 12nm 制程节点、面积 670mm^2 的裸片（die）。尽管硅面积只小幅增加、制程节点不变，Tenstorrent 却显著提升了性能、I/O 和可扩展性。与以往设计相比，除了更强、更耗电之外，最大的变化是增加了 16 个 100Gb 以太网端口。这些以太网端口允许大量芯片互连，为大 型 AI 网络提供横向扩展（scale out）能力。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/46500da3-f75b-4843-acf1-d5300884637e_1024x461.jpeg)

除了通过以太网横向扩展，每个 Tensix 核心也迎来大幅升级：每核心配备了更多 SRAM，并能执行更复杂的数学和 SIMD 指令。Wormhole 配备 192 位 GDDR6 内存总线，内存带宽达 384GB/s。尽管矩阵运算性能翻倍、内存带宽接近 3 倍、并集成了 1.6Tbs 的网络交换能力，Wormhole 芯片的功耗也只是翻倍到 150W。

在同样的 12nm 工艺、裸片面积增加不到 10% 的条件下实现这些目标，Tenstorrent 堪称施了一道黑魔法。其片上网络（NOC）经过巧妙设计，可原生地经由以太网端口向外延伸。对于横向扩展的 AI 训练，芯片间通信的软件开销为 0。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/1cf2711b-2c70-4c6f-9f26-ee3e657868c9_1023x507.jpeg)

AI 训练负载的复杂度正在飙升。OpenAI 声称，训练最强大网络所需的算力每 3.5 个月翻一番。Facebook 最近宣布其新的生产级深度学习推荐系统达到 12 万亿参数，已经超过了 OpenAI 的趋势线。训练这些网络需要的不再是单台服务器，而是整柜的 AI 专用服务器。能够轻松横向扩展到超大规模网络，正是 Tenstorrent Wormhole 的一大核心优势。

Wormhole 芯片将提供两种形态。一种是 PCIe 扩展卡，可轻松插入服务器。而真正面对超大规模 AI 训练问题的客户会选择购买模块形态，它完整释放这颗芯片的全部能力，暴露所有以太网组网能力。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/18572716-d36b-4fef-a5cf-2ed0591fe371_1024x557.jpeg)

Tenstorrent 将 Nebula 设计为基础构建模块：一个 4U 服务器机箱，内部塞进了 32 颗 Wormhole 芯片。这些芯片在机箱内部以全互联（full mesh）方式连接，并能够以透明的方式把 mesh 轻松延伸到单台服务器之外。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f6fbc33e-abc2-4722-aa49-ba20993e0006_1023x533.jpeg)

好戏还没完：Tenstorrent 还展示了 Galaxy。它由 8 台 Nebula 以扩展 mesh 连接而成。这个机柜还包含 4 台 AMD Epyc 服务器和一个共享内存池，提供 >3TBs 的 GDDR6 和 256Gb 的外部以太网链路。通用性的 AMD Epyc 服务器和内存池都接入这套以太网 mesh。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/ce989e3a-fc33-48f4-ba85-5efa06f974c6_1024x507.jpeg)

Tenstorrent 清楚并非所有 AI 负载都是同质的。他们提供了一种 Wormhole 计算能力减半的机柜级服务器方案，AMD Epyc 服务器数量也减半。以计算换来的，是更大的内存池：每个机柜的内存增加到 8 倍。这类配置更适合内存密集型的模型，例如深度学习推荐系统。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/470b9cee-7f5f-44c7-9a94-2d9bb5183e2e_2509x1341.jpeg)
![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/e90151ed-18ee-4ebd-88cc-e16b62d5b407_2677x1245.png)

横向扩展能力还不止于此。Tenstorrent 支持机柜单元以 2D mesh 互连。其横向扩展真正关键的亮点在于软件的处理方式：在软件眼中，这就是一张巨大的同构 Tensix 核心网络。片上网络可以透明地扩展到多个机柜的服务器，无需任何痛苦的软件重写。他们的 mesh 网络在理论上可以扩展到无限大，且保持完整、均匀的带宽。这种拓扑不需要使用大量昂贵的以太网交换机，因为 Wormhole 的片上网络本身就是一个交换机。每台服务器顶部画的那台交换机只用于把这些服务器连接到外部世界，而不是网络内部。相比之下，英伟达的方案在扩展到 8 GPU 以上时就需要昂贵的英伟达自产交换机，超过 16 GPU 还要用到更昂贵的 InfiniBand 网卡和交换机。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/6e62e6c2-a6f5-48e0-8e9c-043b20760b50_1024x493.png)

Tenstorrent 支持多种拓扑，每一种各有利弊。许多数据中心流行的经典 leaf-spine 模型也得到完整支持。尽管各处组网能力并不均等，片上 NOC 仍能干净利落地延伸而不断裂，弹性和多租户架构也得到完整支持。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/06c1de6c-7e25-4387-b5bc-38acfb1b09d1_1024x582.png)

Wormhole 的做法是消除严格的层级。横向扩展服务器往往存在片内、片间、服务器间、机柜间的通信层级，体现在带宽、时延和编程层级上。Tenstorrent 声称找到了一种秘密武器，使这些不同层级的时延和带宽差异对软件变得无关紧要。而且在保持这种灵活性的同时，芯片利用率依然维持在高位。至于他们如何能做得如此干净，我们无疑心存怀疑。

编译器和模型设计者花费大量时间攻关横向扩展难题，而 Tenstorrent 却宣称手握灵丹妙药。编译器和研究者看到的是一条「无穷无尽的核心流」。他们不必再针对网络手工调优模型。正因如此，机器学习研究者获得了解放，需要的话可以把模型扩展到万亿参数。得益于这种灵活性，网络的规模日后也能轻松加大。

横向扩展问题非常困难，对定制 AI 芯片尤甚。即便是横向扩展硬件的领跑者英伟达，也迫使最大的模型开发者去应付带宽、时延和编程层级上的严格分层。如果 Tenstorrent 关于「把这一痛苦任务自动化」的宣称属实，那他们等于把整个行业掀了个底朝天。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/84c20596-e9c2-4877-a02f-b44c2f2b558d_1023x394.png)

要理解他们如何做到这一点，我们需要回顾横向扩展训练的历史。早期在 CPU 集群上做扩展时，通常做法是采用一个大 batch，再把它切分到集群各处，由一台中央参数服务器（parameter server）聚合各 batch。受带宽限制，这种方式扩展性不佳。

随后，GPU 集群配合 all-reduce 和更高的互连带宽带来了进一步进展。但它仍有局限，于是出现了在增大 batch、切分数据之外，尝试结合其他并行方式的早期探索。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/04d7343c-f779-4936-96e4-70e4facb4a52_1024x454.png)

最大的限制在于：batch size 终究会加不动。继续增大 batch size，模型将不再收敛、无法达到高精度。模型变大后，DRAM 容量又成为瓶颈，因为整个模型要在所有节点上各复制一份。中间计算结果甚至装不进片上 SRAM，需要大量 DRAM 带宽来存放这些中间量。DRAM 容量和带宽双双走高的结果，就是每个节点的成本飙升。这种扩展方式对小模型够用，但对更大的模型很快变得不经济。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/5e36e67c-e9c8-4d47-add2-00c6a01eb42d_1024x414.png)

随着更大的模型登场，面向高效扩展的库开始涌现。用户如今可以在服务器集群上指定并组合模型并行、流水线并行和切分式数据并行。本质上，用户把模型和网络的各层拆分到各个节点，模型因此得以继续扩展，因为不必在每个节点内复制整个模型。这种扩展形式最大的问题是必须手工完成：研究者必须自己选择哪些层映射到哪些硬件，并控制数据流动。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8f496d97-6644-4c75-9803-7019c84e6976_1023x441.png)

扩展一个模型时，你需要把模型的各层切分并映射到各个节点和硬件单元上。除了流水线并行之外，单个张量操作也可能大到单个张量核心硬件单元无法独立执行。一层之内位于同一节点上的这些张量操作，同样需要研究者手工切成迷你张量（mini-tensor）。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/59ec19e7-ef21-4fff-a8fb-d13c7caf8611_2627x1210.png)
![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/f8509db1-d5d9-43ed-a882-ee8d7a7e1c2a_2896x1293.png)

Tenstorrent 的目标是打造一种能原生地对迷你张量操作的计算图进行布局（place）、布线（route）和执行的架构。迷你张量是 Tenstorrent 架构的原生数据类型。这意味着研究者无需操心张量切分。每个迷你张量被当作一个单独的数据包（packet）处理。这些数据包带有数据负载和一个头部，头部用于在核心 mesh 中标识并路由该数据包。计算由 Tensix 核心直接在这些迷你张量数据包上完成，每个核心都内含一个路由器和一个包管理器，以及大量 SRAM。路由器和包管理器负责同步，并把算完的数据包沿 mesh 互连送出去——无论这条互连在片内，还是经由以太网跨片。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/22a0592a-5a13-4543-bc52-033b67be2133_1023x470.png)

从软件的视角看，数据包的传输在整个核心 mesh 上是均匀一致的。在同一颗芯片的核心之间发包，与在不同芯片的核心之间发包看起来毫无二致。由于每颗芯片和 NOC 本身都充当交换机，迷你张量数据包可以沿着核心 mesh 一路路由到它需要去的下一个核心。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/739f9d05-dd1e-4c7b-85c9-8ea12915c539_1024x459.png)

迷你张量数据包有 5 个关键原语。push/pop 用于在核心之间搬运数据包。copy、gather、scatter 和 shuffle 也都可用，并可按计算图中消费者/生产者的关系选择单播（unicast）或多播（multicast）。你可以手工把这些原语组合起来，原生地构建迷你张量的计算图。对多数人而言，更省力的路径是使用编译器：它可以直接接收 PyTorch 的输出，将其下层（lower）为由这些原语组成的图，然后在硬件上以 0 开销运行。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/02ea0896-a4d6-4145-af8a-6de8b141166e_2863x1349.png)
![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/8dbc8a7f-6a22-4d53-b81b-24e91c7aa4e9_2915x1342.png)

尽管实际包含着大量芯片、服务器和整柜整柜的 Wormhole，软件看到的却只有这一张核心 mesh。严格的层级被移除，模型开发者因此获得解放。编译器会根据网络拓扑，自动把迷你张量高效地布局和布线到整个网络中，而无需模型开发者操心。增加更多服务器只是延伸了 mesh，模型可以毫无顾虑地横向扩展。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/b87860bb-ac79-4c91-934e-41b29cbd3e7b_1024x464.png)

这些边界支持大规模的模型流水线并行。网络中的各层可以使用任意数量的资源来匹配算力需求：不需要多少算力的层可以只用半台服务器或半颗芯片，而需要大量算力的层则可以横跨多个机柜。第 4 个例子显示，只要你的 mesh 足够大，单单一层甚至可以被拉伸到多柜服务器上。编译器看得到 mesh 的规模，并依据各层的大小进行映射——无论这张核心 mesh 是 1 颗芯片，还是散布在众多服务器机柜上的 10,000 颗芯片。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/32b4b160-7f5a-472b-b4ff-f559f6fc36ea_1024x466.png)

与其他 mesh 架构相比，Tenstorrent 的 mesh 规模大得多、扩展性也强得多。FPGA 处在最细粒度的一端，需要耗费海量时间手工调优；CGRA 跑的是标量图，仍受诸多限制。Tenstorrent 的矩阵引擎拥有数万亿次浮点运算（teraflops）的算力和大得多的内存容量。NOC、包管理器和路由器智能地料理片内与片间通信，让模型开发者得以专注于拼图的其他部分。这使其在横向扩展 AI 负载上效率更高，开发起来也容易得多。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/a92373c5-b663-4f9b-8764-92634c4be37e_1024x480.png)

如果 Tenstorrent 的宣称兑现，他们可谓成就了一件真正的魔法。他们强大的 Wormhole 芯片可以通过集成以太网端口横向扩展到多芯片、多服务器、多机柜，软件开销为零。编译器看到的是一张没有严格层级的无限核心 mesh。这让模型开发者在大规模机器学习模型的横向扩展训练中，无需再为计算图切分或张量切分操心。

而 AI 软硬件的领导者英伟达，离解决这个问题还差得很远。他们提供了库、SDK 和优化支持，但他们的编译器无法自动完成这件事。对于 Tenstorrent 编译器能否完美地把 AI 网络中的各层布局并布线到核心 mesh、同时避开网络拥塞或瓶颈，我们持怀疑态度——这类瓶颈在 mesh 网络中司空见惯。但如果他们真的以零软件开销解决了横向扩展 AI 的问题，那么所有 AI 训练硬件都将迎来一记响亮的警钟。每一位从事超大模型研究的学者，都会因为易用性的飞跃而迅速涌向 Tenstorrent Wormhole 及其后续硬件。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

[分享](https://newsletter.semianalysis.com/p/tenstorrent-wormhole-analysis-a-scale?utm_source=substack&utm_medium=email&utm_content=share&action=share)

[发表评论](https://newsletter.semianalysis.com/p/tenstorrent-wormhole-analysis-a-scale/comments)

*本文最初于 2021 年 6 月 25 日发布于 [SemiAnalysis](https://semianalysis.com/tenstorrent-wormhole-analysis-a-scale-out-architecture-for-machine-learning-that-could-put-nvidia-on-their-back-foot/)。*

*SemiAnalysis 的客户及员工可能持有本文所提及公司的仓位。*

*[幻灯片来自 Linley Spring Processor Conference](https://www.youtube.com/watch?v=Id3enIOAY2Q)*
