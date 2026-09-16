---
title: "NVIDIA GTC 2025：为推理而生——Vera Rubin、Kyber、CPO、Dynamo 推理、Jensen 数学、Feynman"
title_en: "NVIDIA GTC 2025 - Built For Reasoning, Vera Rubin, Kyber, CPO, Dynamo Inference, Jensen Math, Feynman"
subtitle: "英伟达下一代系统，从芯片到整机再到软件的推理全面优化：买得越多，赚得越多"
date: 2025-03-19
source: https://newsletter.semianalysis.com/p/nvidia-gtc-2025-built-for-reasoning-vera-rubin-kyber-cpo-dynamo-inference-jensen-math-feynman
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie", "Daniel Nishball", "Ivan Chiam", "Patrick Zhou", "Doug", "Wega Chu"]
tags: ["Hardware Architecture", "Networking", "Accelerators"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# NVIDIA GTC 2025：为推理而生——Vera Rubin、Kyber、CPO、Dynamo 推理、Jensen 数学、Feynman

> 原文：[NVIDIA GTC 2025 - Built For Reasoning, Vera Rubin, Kyber, CPO, Dynamo Inference, Jensen Math, Feynman](https://newsletter.semianalysis.com/p/nvidia-gtc-2025-built-for-reasoning-vera-rubin-kyber-cpo-dynamo-inference-jensen-math-feynman) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**英伟达下一代系统，从芯片到整机再到软件的推理全面优化：买得越多，赚得越多**

## **推理 token 的爆炸**

AI 模型的进步速度极快，过去六个月模型的提升幅度超过了再之前六个月。这一趋势还将持续，因为三条规模化定律（scaling law）正叠加在一起、协同发力：预训练规模化、后训练规模化以及[推理时规模化](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/)。

今年的 GTC 全部围绕应对这些新的规模化范式展开。

![](https://substack-post-media.s3.amazonaws.com/public/images/d108a7a2-436c-42e1-9763-b82291d624de_2219x1298.png)
*来源：Nvidia*

Claude 3.7 在软件工程上展现了惊人的性能。DeepSeek v3 表明，上一代模型能力的成本正在暴跌，进一步推动了普及。OpenAI 的 o1 和 o3 模型证明，更长的推理时间与搜索意味着好得多的答案。就像预训练定律的早期一样，为这些模型的后训练投入更多算力还看不到上限。今年 GTC 的重点是支撑智能与 token 的爆炸式增长。Nvidia 正聚焦于将推理成本大幅降低 35 倍，以支撑模型的训练与部署。

去年的口号是「买得越多，省得越多」，而今年的口号是**「省得越多，买得越多」**。Nvidia 路线图在硬件与软件两侧交付的推理效率，解锁了推理与智能体在模型低成本部署及各类变革性企业应用中的落地，使其得以大规模普及与部署——这是杰文斯悖论（Jevons' paradox）发挥作用的经典案例。或者用 Jensen 的说法：**「买得越多，赚得越多」**。

市场对此感到担忧。担心的点是：DeepSeek 式的软件优化加上 Nvidia 持续的硬件改进，带来了*太多*节省，意味着 AI 硬件的需求会下降、市场将陷入 token 过剩。价格确实影响需求；而随着智能的价格下降，智能能力的前沿继续推进，需求随之增长。今天的各项能力都受制于推理成本。AI 对我们生活的实际影响仍处于婴儿期。随着成本下降，净消费量反而会增加。

对 token 通货紧缩的担忧，就好比在讨论光纤泡沫时代每数据包互联网连接成本不断下降的同时，却忽视了网站和互联网应用最终将对我们的生活、社会与经济产生的影响。关键区别在于：带宽需求终归有约束，而随着能力大幅提升、成本下降，对智能的需求会趋向无穷。

Nvidia 给出了支持杰文斯悖论论点的数据。如今的模型需要 >100T token，而一个推理模型的 token 是 20 倍、计算是 150 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/fb751d51-0085-45ec-8b11-c12fb6177fe3_871x602.png)
*来源：Nvidia*

测试时计算每次查询要消耗数十万 token，而每月的查询多达数亿次。后训练规模化——也就是模型「上学」的阶段——每个模型需要数万亿 token，而后训练过的模型多达数十万个。此外，智能体 AI（agentic AI）意味着多个模型将协同工作，去解决越来越难的问题。

## **Jensen 数学每年都在变**

每年 Jensen 都会给行业抛出新的数学规则。Jensen 数学出了名的令人困惑，而今年为这份困惑又添一笔：我们如今观察到了第三条 Jensen 数学新规。

第一条 Jensen 数学规则：Nvidia 的标称 FLOPS 按 2:4 稀疏（*没人用这个*）口径报出，而非稠密 FLOPS——后者才是真实世界的性能指标——也就是说 H100 的 989.4 TFLOPs FP16 被标称为 1979.81 TFLOPs。

第二条 Jensen 数学规则：带宽应按双向口径报出。NVLink5 标称为 1.8TB/s，因为它是 900GB/s 发送加 900GB/s 接收。两者相加写进了规格表，但在网络行业，标准做法是报单向带宽。

如今，第三条 Jensen 数学规则出现了。GPU 数量按封装内的 GPU 裸片数计，而非封装数量。这一命名法将从 Rubin 开始采用。第一代 Vera Rubin 机柜将被称作 NVL144，尽管其系统架构与 GB200 NVL72 类似——同样的 Oberon 机柜、72 个 GPU 封装。这会让所有人都很难看懂、需要不断地澄清，但没办法，我们都只是活在 Jensen 的世界里。

好了，现在来过一遍路线图。

## GPU 与系统路线图

![](https://substack-post-media.s3.amazonaws.com/public/images/8103a7d6-b5e9-49cc-9e44-4b2a626617e7_1787x950.png)
*来源：Nvidia*

## Blackwell Ultra B300

![](https://substack-post-media.s3.amazonaws.com/public/images/3880684b-639a-4d70-9045-ae7ec3ed6cb8_1205x905.png)
*来源：Nvidia*

Blackwell Ultra 300 此前已经预览过，与我们去年圣诞分享的细节相比没有任何变化。重述主要规格：GB300 不会以板卡形式销售，而是以可揣进口袋的 SXM 模块形式搭载 B300 GPU 与 Grace CPU 出售，同时也会以可揣的 BGA 形式出售。性能方面，B300 相比对应的 B200 FP4 FLOPS 密度高出 50% 以上。内存容量升级到每封装 288GB（8 颗 12 层堆叠 HBM3E），但带宽维持 8TB/s 不变。

这是通过削减许多（但并非全部）FP64 ALU、换成 FP4 与 FP6 ALU 实现的。双精度工作负载主要是 HPC 与超算场景，而非 AI 工作负载。虽然这让 HPC 社区失望，但 Nvidia 是商业公司，重点押注 AI 这个更重要的市场。

B300 的 HGX 版本现在叫 B300 NVL16。它将采用此前被称为「B300A」的单 GPU Blackwell 变体，该变体现已更名为「B300」。它是双裸片 B300 的一半，而且由于没有把单个封装内两颗 GPU 裸片连起来的高速 D2D 接口，通信开销可能更高。

B300 NVL16 将取代 B200 HGX 形态，在基板上放 16 个封装与 GPU 裸片。为做到这一点，两颗单裸片封装会放在同一块 SXM 模块上（这样的模块共 8 块）。Nvidia 为什么走这条路而不是坚持 8 颗双裸片 B300，目前尚不清楚；我们怀疑更小的 CoWoS 模块与封装基板带来的良率提升是主要动因。注意，封装工艺将是 CoWoS-L 而非 CoWoS-S。这是一个重要决定。当初单裸片 B300A 的出现正是因为 CoWoS-S 的成熟度与产能。这次切换说明 CoWoS-L 已经快速成熟，良率相比其起步阶段的动荡已经稳定下来。

这 16 颗 GPU 将通过 NVLink 协议通信，而且与 B200 HGX 一样，两组 SXM 模块之间会放置两颗 NVSwitch 5.0 ASIC。

最后，一个新细节是：与此前几代 HGX 不同，B300 NVL16 将不再配备 Astera Labs 的重定时器（retimer）。不过部分超大规模云厂商会选择改用 PCIe 交换芯片[。这一点我们今年早些时候已向 Core Research 订阅读者率先披露](https://semianalysis.com/core-research/core-weekly-insights-03-14-25/)。

B300 的另一个重要细节是它将引入 CX-8 网卡（NIC），提供 4 条 200G 通道以实现总计 800G 的 InfiniBand 吞吐，相比 Blackwell 现有 CX-7 网卡，网络速度代际翻倍。

## Rubin 规格

![](https://substack-post-media.s3.amazonaws.com/public/images/45efcb00-7ef4-4a21-a4c6-5d9fedb867b5_1158x653.png)
*来源：Nvidia*
![](https://substack-post-media.s3.amazonaws.com/public/images/199f62e9-7afd-4ab2-85ea-6e7185bf14e7_1570x814.png)
*来源：SemiAnalysis*

Rubin 将在台积电（TSMC）3nm 上采用两颗光罩级计算裸片。这两颗计算裸片两侧搭配两颗 I/O 小芯片（tile），承载 NVLink、PCIe 与 NVLink C2C IP 的全部 SerDes，从而把主裸片上的空间腾出来用于更多计算。

Rubin 将提供高达 50 PFLOPS 的稠密 FP4 算力，较 B300 代际提升超过三倍。Rubin 是怎么做到的？Nvidia 同时拉高了几个重要维度：

1. 如上所述，I/O 裸片腾出了面积——可能有 20-30%——可以投入到更多流式多处理器与张量核心上。
2. Rubin 将采用 3nm 工艺制造，即 Nvidia 定制的 3NP 或标准 N3P。从 Blackwell 一代的 4NP 走到 3NP，逻辑密度大幅跃升，但 SRAM 几乎没有微缩。
3. 此外，Rubin 的 TDP 更高——我们估计为 1800W——甚至可能支撑更高的时钟频率。
4. 再就是架构层面的扩展。Nvidia 每一代都为张量核心采用更大的脉动阵列。我们认为脉动阵列从 Hopper 的 32x32 提升到了 Blackwell 的 64x64。Rubin 可能进一步加大到 128x128。更大的脉动阵列带来更好的数据复用与更低的控制复杂度，通常面积与功耗效率也更高。难点在于编程，这也正是 Nvidia 不像 Google TPU 那样做到 256x256 的原因。它对制造良率也不利。Nvidia 的光罩级单片裸片参数良率很高，因为其架构由许多更小的计算单元组成，内置冗余与可修复性。有缺陷的计算单元直接屏蔽，实现良率收割。TPU 则不同，它的张量核心数量更少但单个体积非常大，不具备同样的缺陷逻辑单元修复能力。

Rubin 将继续沿用 GB200/300 NVL72 所用的 Oberon 机柜架构。它将搭配 Vera CPU，即 Grace 的 3nm 后继者。注意 Vera 将采用 Nvidia 全自研设计的核心。Grace 则重度依赖 Arm 的 Neoverse V2 核心。Nvidia 还有自研的总线架构（fabric），让单个 CPU 核心在需要时可以访问更高的内存带宽——这一点 AMD 与 Intel 的 CPU 都很难做到。

新的命名法就在这里登场。新机柜将被命名为 **VR200 NVL144**，尽管它只有 72 个 GPU 封装——144 颗计算裸片（72 个封装 x 每封装 2 颗计算裸片）。Nvidia 真是一家革命性的公司，连我们数 GPU 的方式都要改！

*AMD 市场团队应该记好笔记。AMD 没有宣称 MI300X 家族可以纵向扩展到 64 GPU 的 world size（每系统 8 个封装 x 每封装 8 个 XCD 小芯片），白白把性能留在桌上，这是错失的一次关键机会。*

*/讽刺完毕……Lisa，请千万别学*

Nvidia 的 HBM 容量代际持平，维持 288GB，但升级到了 HBM4：8 颗 12 层堆叠、层密度同样为 24GB。转向 HBM4 带来了带宽提升，聚合带宽 20.5TB/s，主要来自总线宽度翻倍到 2048 位，引脚速率为 6.4Gbps——这是 JEDEC 标准当前的上限。

![](https://substack-post-media.s3.amazonaws.com/public/images/fc0619d4-02da-467c-8068-6d9cf758bca6_1826x1012.png)
*来源：SemiAnalysis*

Rubin 将搭载第六代 NVLink，速度翻倍到 3.6TB/s（双向）。提升来自通道数翻倍，Nvidia 继续沿用 224G SerDes。

回到 Oberon：背板仍是同样的铜背板，但我们认为线缆数量会随每 GPU 通道数翻倍而成比例翻倍。

NVSwitch 侧，NVSwitch ASIC 的聚合带宽同样翻倍，也是通过通道数翻倍实现。

## Rubin Ultra 规格：

![](https://substack-post-media.s3.amazonaws.com/public/images/67439399-3abb-4014-8687-89bce3544b06_1205x650.png)
*来源：Nvidia*

Rubin Ultra 才是性能真正起飞的地方。Nvidia 将从每封装 8 颗 HBM 直接跳到 16 颗。一排 4 颗光罩级 GPU，两侧各搭配 2 颗 I/O 小芯片。计算面积翻倍，计算性能翻倍到 100 PFLOPS 稠密 FP4。HBM 容量升到 1024GB，**是原版 Rubin 容量的 3.5 倍以上**。不仅是堆叠颗数翻倍，密度与层数也在提高。要在单个封装里做到 1TB 内存，将采用 16 颗 HBM4E，每颗为 16 层 32Gb DRAM 核心裸片。

我们认为这个封装会在基板上拆分为两个中介层，以避免使用单个非常大的中介层（接近 8 倍光罩面积）。中间的 2 颗 GPU 裸片将通过一颗带 D2D 接口的薄 I/O 裸片相互通信，通信经由基板完成。这将需要一块超出 JEDEC 当前封装尺寸限制（宽、高均为 120mm）的非常大的 ABF 基板。

系统共有 365TB 的「快速内存（Fast Memory）」，其中 HBM 147TB、LPDDR 218TB。每颗 Vera CPU 配 1.5TB LPDDR，由于共有 144 颗 Vera CPU，合计 218TB LPDDR。

![](https://substack-post-media.s3.amazonaws.com/public/images/3bba797f-6780-425c-8cbc-f570bf73b012_1024x503.png)
*来源：SemiAnalysis*

这也是我们将看到 Kyber 机柜架构登场的时候。

## Kyber 机柜架构

其中一个关键新特性就是 Kyber 机柜架构。Nvidia 通过把机柜旋转 90 度来提升密度。考虑到 NVL576（144 个 GPU 封装）配置，这是面向更大纵向扩展 world size 的又一次令人难以置信的密度提升。

![](https://substack-post-media.s3.amazonaws.com/public/images/c9a1db37-1166-422e-a85f-c21c17b7d9ca_1205x650.png)
*来源：Nvidia*

来看看 Oberon 机柜架构与 Kyber 机柜架构的关键差异：

![](https://substack-post-media.s3.amazonaws.com/public/images/7cca1b3a-c211-4197-9be4-5f502eedee62_3452x1239.png)
*来源：SemiAnalysis*

- 计算托盘旋转 90 度变成刀片（blade）形态，以实现更高的机柜密度。
- 每个机柜由 4 个计算舱（canister）组成，每舱 18 片计算刀片。

  - NVL576 配置下，每片计算刀片含 2 个 Rubin Ultra GPU 和 2 个 Vera CPU。
  - 每个计算舱共有 36 颗 R300 GPU（144 颗裸片）和 36 颗 Vera CPU
  - 这使机柜内 NVLink world size 总计 144 颗 GPU（576 颗裸片）
- PCB 背板取代铜缆背板，成为计算舱内 GPU 与 NVSwitch 之间的纵向扩展互连。

  - 这一转变主要是由于在更小的占用空间内布线的难度大增。
  - 机柜后部的 NVSwitch 刀片通过 PCB 背板的背面与计算刀片相连。
  - 各计算舱内的 NVSwitch 刀片之间如何互连、把全部 4 个计算舱连成单一 NVLink 域，目前仍不清楚。

    - 正在考虑的可行方案包括 DAC、ACC 和 AEC。
- 有人可能会问：计算刀片占满了整个机柜，电源、电池和交换机放在哪里？

  - 在未来的数据中心机房布局中，会有[独立电源机柜](https://semianalysis.com/2025/02/13/datacenter-anatomy-part-2-cooling-systems/)、独立散热机柜和独立交换机机柜。
  - 这也是 Nvidia 如此早地公布 Kyber 机柜架构路线图的主要原因之一——让供应链提前准备计算机房与机柜两级数据中心基础设施即将到来的变化。

![](https://substack-post-media.s3.amazonaws.com/public/images/e9b64962-1b35-4d53-ab0e-c47457d23bf9_1015x1024.png)
*来源：Nvidia*

有意思的是，供应链上出现了一个 VR300 NVL1,152（288 个 GPU 封装）Kyber 机柜变体的迹象（如果你去数上面 GTC 主题演讲里展示的那块晶圆，会数出 288 个红框标出的 GPU 封装）。我们认为这可能是一个在开发中的潜在 SKU，将在未来把机柜密度以及 NVLink world size 从 GTC 2025 展示的 NVL576（144 个 GPU 封装）翻倍到 NVL1,152（288 个封装）。

还会有新的第七代 NVSwitch，这值得关注。这是新一代 NVSwitch 首次采用「中置平台（mid-platform）」设计。这使得交换芯片的聚合带宽与端口数（radix）可以支撑在单一域内扩展到 576 颗 GPU 裸片（144 个封装），不过其拓扑可能不再是全互联、无阻塞、轨道优化的单层多平面拓扑，而可能是带收敛比（oversubscription）的多平面轨道优化两层网络拓扑，甚至非 CLOS 拓扑。

Kyber 机柜架构预计将于 2027 年随 Rubin Ultra 推出。GTC 展台上展示的实体机柜是基于 Blackwell 的测试载体，因此该架构尚未最终定稿。

## **Blackwell Ultra 强化的指数运算硬件单元**

所有类型的注意力机制——flash-attention、MLA、MQA、GQA——都需要**矩阵乘法**（matmul）与 **softmax 函数**（逐行归约与逐元素指数函数）。矩阵乘法称为 GEMM，即通用矩阵乘法，只对应神经网络计算中的矩阵乘法部分。

在 GPU 上，GEMM 由张量核心执行。张量核心每一代都在变快，但专注于逐元素指数运算（softmax）的多功能单元（MUFU）每一代的性能提升没有那么多。

在 bf16（bfloat16）的 Hopper 上，计算注意力层的 softmax 所需的周期数是 GEMM 的 50%。这需要内核工程师做计算重叠来「隐藏」softmax 的延迟，使内核编写变得困难。

![](https://substack-post-media.s3.amazonaws.com/public/images/727c5b2d-6252-4f46-8fd6-3326e8edb01e_937x481.png)
*来源：Tri Dao @ CUDA Mode Hackathon 2024*

在 FP8（浮点）的 Hopper 上，计算注意力层 softmax 消耗的周期数与 GEMM 完全相同。这意味着如果完全不做重叠，注意力层的耗时将**翻倍**。大约是 1536 个周期计算 matmul，再 1536 个周期计算 softmax。重叠正是提升吞吐的所在。由于 softmax 与 GEMM 耗费相同的周期数，内核工程师必须优化出完美重叠的内核。现实是完美重叠不可能做到，硬件会因 Amdahl 定律损失性能。

到目前为止我们所描述的挑战，都是围绕 Hopper 时代的 GPU 展开的。这个问题在第一代 Blackwell 上同样存在。Nvidia 在 Blackwell Ultra 上解决了它：重构了 SM 并新增指令。

在 Blackwell Ultra 上，计算注意力机制 softmax 部分的 MUFU 单元相比标准 Blackwell 提速 2.5 倍。这将缓解对完美重叠的要求——不再必须把 softmax 的计算隐藏进 GEMM 的计算里。有了 MUFU 的 2.5 倍加速，CUDA 开发者有了更大的重叠容错空间，而不会损失其注意力内核的性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/8007bb0a-e3f8-4466-a08f-4bd200360e54_1414x757.png)
*来源：Tri Dao @ CUDA Mode Hackathon 2024*

这正是 Nvidia 新推理栈与 Dynamo 大显身手的地方。

## 推理栈与 Dynamo

在去年的 GTC 上，Nvidia 讲到 GB200 NVL72 更大的 72-GPU 纵向扩展 world size 使其在 FP8 下相较 H200 带来 15 倍的推理吞吐提升。

![](https://substack-post-media.s3.amazonaws.com/public/images/bdc9823f-a477-419f-aef2-cd2e0ebdc8d3_975x634.png)
*来源：Nvidia*

Nvidia 没有放慢脚步，反而是在加速推理吞吐的提升——这次是多线并进，在硬件与软件领域都有新发布。

Blackwell Ultra GB300 NVL72 相比 GB200 NVL72 的 FP4 稠密 PFLOPS 高出 50%，HBM 容量也提升 50%——两者都会推高推理吞吐。路线图中 Rubin 一代在网络速度上的多次升级，也将带来有意义的推理吞吐改善。

硬件侧推理吞吐的下一跳将来自纵向扩展网络 world size 从 Rubin 的 144 颗 GPU 裸片扩展到 Rubin Ultra 的 576 颗 GPU 裸片。而这还只是硬件改进。

软件方面，Nvidia 发布了 Nvidia Dynamo——一个开放的 AI 引擎栈，专注于让推理的部署与扩展更容易。它有潜力颠覆 vLLM 与 SGLang——提供多个 vLLM 不具备的特性，而且性能更高。与硬件层的创新相结合，Dynamo 将把吞吐-交互性曲线再一次向右大幅移动——尤其改善高交互性用例的吞吐。

![](https://substack-post-media.s3.amazonaws.com/public/images/017e9808-a454-459c-bcbe-07be396b07f0_2309x1332.png)
*来源：Nvidia*

Dynamo 为当前的推理栈带来了几项关键新特性：

- **智能路由器（Smart Router）**
- **GPU 规划器（GPU Planner）**
- **面向推理的改进版 NCCL 集合通信**
- **NIXL——NVIDIA 推理传输引擎**
- **NVMe KV 缓存卸载管理器**

## 智能路由器

智能路由器在多 GPU 推理部署中，智能地把每个 token 路由到预填充（prefill）与解码（decode）GPU。对预填充而言，这意味着确保流入的 token 均匀分配到服务预填充的各 GPU，以避免预填充阶段任何给定专家成为瓶颈。

类似地——在解码阶段——要确保序列长度与请求在各解码 GPU 之间分布均衡。GPU 规划器还可以复制那些流量更重的专家，帮助保持负载均衡。

该路由器还能在各模型服务副本（replica）之间做负载均衡——这是 vLLM 及许多其他推理引擎不支持的能力。

![](https://substack-post-media.s3.amazonaws.com/public/images/c03590d3-5ca8-458b-b33a-fd3ce3101b47_1149x686.png)
*来源：Nvidia*

## GPU 规划器

GPU 规划器是预填充与解码节点的自动扩缩容器（autoscaler），随一天当中自然波动的需求变化拉起额外节点。它可以在 MoE 模型的众多专家之间，在预填充与解码节点两侧实现一定程度的负载均衡。GPU 规划器会拉起额外的 GPU，为高负载专家提供更多算力。它还可以按需在预填充节点与解码节点之间动态重新分配节点，进一步提升资源利用率。

此外，它还支持改变用于解码与预填充的 GPU 比例——这对 Deep Research 这类场景尤其有用：这类应用需要审阅海量上下文，却只生成相对少量的内容，因此对预填充的需求高于解码。

![](https://substack-post-media.s3.amazonaws.com/public/images/f9f0fec7-e131-4ff1-9938-0a7d427429c8_1170x633.png)
*来源：Nvidia*

## **面向推理的改进版 NCCL 集合通信**

这个低延迟通信库是 Nvidia 集合通信库（NCCL）中的一组新算法，可以在更小的消息尺寸下把延迟降低 4 倍——从而整体上显著提升推理吞吐。

[Sylvain 今年 GTC 的演讲](https://register.nvidia.com/flow/nvidia/gtcs25/ap/page/catalog/session/1727457129604001QT6N)对这些新增内容有更详尽的阐述——介绍了实现这一提升的单次（one-shot）与两次（two-shot）all-reduce 算法。

由于 AMD 的 RCCL 库是 NVIDIA NCCL 的原样复制 fork，Sylvain 的 NCCL 重构将继续扩大 CUDA 护城河，并使 AMD 的 RCCL 要损失数千个工程小时来把 Nvidia 这次大重构同步进 RCCL。当 AMD 花数千工程小时追赶 Nvidia 的改动时，Nvidia 却会用这些时间继续推进集合通信软件栈与算法的前沿。

![](https://substack-post-media.s3.amazonaws.com/public/images/12365f8e-7215-40cc-a6f3-380296b095d5_1024x608.png)
*来源：Nvidia*

## NIXL - NVIDIA 推理传输引擎

要在预填充节点与解码节点之间传输，需要低延迟、高带宽的通信传输库。NIXL 将采用 InfiniBand GPU 异步初始化（IBGDA）。目前的 NCCL 中，控制流要经过 CPU 代理线程，而数据流直接到 NIC，无需经过 CPU 缓冲。而有了 IBGDA，控制流与数据流都不必经过 CPU，直接从 GPU 到 NIC。

NIXL 还将把 CXL、本地 NVMe、远端 NVMe、CPU 内存、远端 GPU 内存与 GPU 之间收发数据迁移的复杂性抽象掉。

![](https://substack-post-media.s3.amazonaws.com/public/images/9b7b0130-da82-4d6c-b321-a69cdcc0e1da_1151x654.png)
*来源：Nvidia*

## **NVMe KV 缓存卸载管理器**

KV 缓存卸载管理器通过把先前用户会话的 KV 缓存保存到 NVMe 存储而非直接丢弃，让预填充的总体执行更高效。

![](https://substack-post-media.s3.amazonaws.com/public/images/c596bc00-30ba-492a-a72f-4bcb3f303527_1024x633.png)
*来源：Nvidia*

当用户与 LLM 进行持续的多轮对话时，LLM 需要把对话早前的提问与回答也纳入考量、同样作为输入 token。在朴素实现中，推理系统会丢弃原本用于生成那些早前问答的 KV 缓存，意味着这些 KV 缓存必须重新计算，重复同一批计算。

而有了 NVMe KV 缓存卸载，当用户离开时，KV 缓存可以卸载到 NVMe 存储系统，直到用户回到对话。当用户在对话中提出下一个问题时，KV 缓存可以快速从 NVMe 存储系统取回，免去重新计算 KV 缓存的需要。

这释放了预填充节点的容量去承接更多流入流量，或者反过来可以缩减所需的预填充部署规模。用户也将获得好得多的体验——首 token 时间更快，因为取回 KV 缓存所需的时间远少于重新计算。

![](https://substack-post-media.s3.amazonaws.com/public/images/fb906f51-e5ce-496b-bcf1-5021bd5ca4b7_1014x683.png)
*来源：Nvidia*

在 [DeepSeek 开源周 Day 6 的 GitHub 笔记](https://github.com/deepseek-ai/open-infra-index/blob/main/202502OpenSourceWeek/day_6_one_more_thing_deepseekV3R1_inference_system_overview.md)中，研究人员披露了磁盘上 KV 缓存 56.3% 的命中率，意味着其预填充部署获得了可观的效率提升。我们了解到，在用户进行多轮对话的这类部署上，典型的 KV 缓存命中率可达 50-60%。部署这套 NVMe 存储方案是有成本的，因此存在一个交叉点：当对话足够短时，直接重算比重新加载更容易也更便宜；但除此之外，节省是巨大的。

任何持续关注 [DeepSeek 开源周](https://github.com/deepseek-ai/open-infra-index/tree/main?tab=readme-ov-file)的人，对上述所有技术都会非常熟悉。在 Nvidia 为 Dynamo 补齐更多文档之前，上面的链接可以说是快速深入了解这些技术的最佳去处。

所有这些特性的成果，是全线都非常亮眼的推理加速。Nvidia 甚至讨论了在现有 H100 节点上部署 Dynamo 带来的改进。本质上——Dynamo 把 DeepSeek 的创新民主化了，让社区里的每个人都能用上开源模型技术的最佳成果。这让所有人——而不只是拥有深厚推理部署工程班底的顶级 AI 实验室——都能部署高效率的推理系统。

最后——由于 Dynamo 全面处理分离式（disaggregated）推理与专家并行，它在单副本与高交互性部署上尤其有帮助。当然——拥有大量节点是 Dynamo 充分发挥能力、交付有意义提升的前提。

![](https://substack-post-media.s3.amazonaws.com/public/images/7e5bb716-01fe-431b-b07a-7371d0e52836_1165x790.png)
*来源：Nvidia*

## **AI 总拥有成本——成本下降**

在结束关于 Blackwell 的讨论后不久，Jensen 用这些创新如何让他成为「首席营收毁灭官」把观点钉死。他进一步强调，Blackwell 相比 Hopper 最高有 68 倍的性能增益，带来 87% 的成本下降。Rubin 预计带来更高的性能增益——是 Hopper 的 900 倍，成本降低 99.97%。

显然，Nvidia 正以毫不松懈的节奏推进改进——正如 Jensen 所说：「当 Blackwell 开始规模出货时，Hopper 白送都送不出去。」

![](https://substack-post-media.s3.amazonaws.com/public/images/72c74dfc-0aed-4e1a-9150-0c5602f147c1_2132x1427.png)
*来源：Nvidia*

同样的信息我们已经宣讲了一段时间——强调在产品周期早期而非晚期部署算力的重要性。在去年 10 月发布的[《AI 新兴 GPU 云（Neocloud）手册与剖析》](https://semianalysis.com/2024/10/03/ai-neocloud-playbook-and-anatomy/)中，我们解释了正是这一动态驱动了 H100 租赁价格从 2024 年年中开始加速下跌。相当长一段时间以来，我们一直在敦促生态优先部署 B200 与 GB200 NVL72 等下一代系统，而不是采购 H100 或 H200。

订阅了我们 [AI 云总拥有成本（TCO）模型](https://semianalysis.com/ai-cloud-tco-model/)的客户已经熟悉我们对代际生产率跃升的预期，以及这将如何驱动这些芯片在 AI 新兴 GPU 云的租赁定价，并最终决定芯片所有者能够赚到的净现值。

事实上，我们的 H100 租赁价格预测框架正是围绕 Jensen 所阐释的那个要点构建的。我们结合对未来装机量、集群总拥有成本以及未来芯片能力的估计，构建出预测价格曲线。到目前为止，这个框架很有指导意义。我们于 2024 年 4 月首次向客户发布 H100 租赁价格预测模型——该模型对 2024 年初至今 H100 租赁价格的预测准确率达到 98%。

![](https://substack-post-media.s3.amazonaws.com/public/images/3faa18c2-f8e2-48f2-8c79-69dcf399cfb2_1724x1128.png)
*来源：AI TCO Model*

## **CPO 的切入点**

![](https://substack-post-media.s3.amazonaws.com/public/images/3e0e97a0-6cc1-4e6e-8756-64c32d8bb0a1_1231x701.png)
*来源：Nvidia*

在主题演讲中，Nvidia 宣布了其首个共封装光学（CPO）方案，将部署于其横向扩展交换机中。有了 CPO，收发器如今被外置激光源（ELS）取代，与直接紧邻芯片硅片放置的光引擎（OE）共同完成数据通信。光纤电缆不再插到收发器端口上，而是插到交换机上把信号直接引导至光引擎的端口。

![](https://substack-post-media.s3.amazonaws.com/public/images/cfefa490-05cc-4e87-8d33-a47f9816f675_1267x659.png)
*来源：Nvidia*

CPO 的首要优势是功耗显著降低，原因有几个方面。在交换机本身，节省相当可观：不再需要数字信号处理器（DSP），而且可以使用功耗更低的激光光源。这种节省通过线性可插拔光模块（LPO）收发器也能获得，但 CPO 还允许大得多的交换机端口数（radix），让网络得以扁平化掉一层——集群可以借助 CPO 使用两层网络，替代使用 DSP 收发器的三层网络。这意味着砍掉整整一整层交换机及配套，同时享受相应的成本与功耗节省——其量级在功耗维度上几乎与收发器本身的节省同样显著。

我们的分析显示，对一个 400k* GB200 NVL72 部署，从基于 DSP 收发器的三层网络转向基于 CPO 的两层网络，可带来最高 12% 的集群总功耗节省——收发器功耗从占计算资源的 10% 降到仅占计算资源的 1%。

![](https://substack-post-media.s3.amazonaws.com/public/images/d28da705-0950-4c9c-9e89-c809514fa1c8_888x571.png)
*来源：SemiAnalysis*

Nvidia 今天发布了多款基于 CPO 的交换机，其中包括 Quantum X-800 3400 的 CPO 版本——该产品本身[一年前在 GTC 2024 首秀](https://semianalysis.com/2024/03/25/nvidias-optical-boogeyman-nvl72-infiniband/)。它拥有 144 个 800G 端口，总吞吐 115T，将包含 144 个 MPO 端口和 18 个 ELS。这台交换机将于 2025 年下半年推出。配有 512 个 800G 端口的 Spectrum-X 交换机同样值得关注，它可以在高速下实现非常大的端口数——支撑非常快、非常扁平的网络拓扑。这台以太网 CPO 交换机将于 2026 年下半年推出。

![](https://substack-post-media.s3.amazonaws.com/public/images/8de9ed6b-33a7-418c-bc99-8ee7e39a023d_948x592.png)
*来源：Nvidia*

尽管今天的发布已经堪称突破，我们仍然认为 Nvidia 在 CPO 领域只是在热身。我们认为，长期来看 CPO 最大的贡献将是部署在纵向扩展网络之中——它有潜力大幅提升 GPU 纵向扩展网络的端口数与聚合带宽，实现更快、更扁平的纵向扩展网络，并打开远超 576 GPU 的纵向扩展 world size 的大门。我们将在近期的一篇文章中更深入地解析 Nvidia 的 CPO 方案。

## **Nvidia 仍是王者，且正盯上你的计算成本**
