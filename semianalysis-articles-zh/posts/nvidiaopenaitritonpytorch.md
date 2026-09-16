---
title: "Nvidia 在机器学习领域的 CUDA 垄断正在被打破——OpenAI Triton 与 PyTorch 2.0"
title_en: "How Nvidia’s CUDA Monopoly In Machine Learning Is Breaking - OpenAI Triton And PyTorch 2.0"
date: 2023-01-16
source: https://newsletter.semianalysis.com/p/nvidiaopenaitritonpytorch
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Nvidia 在机器学习领域的 CUDA 垄断正在被打破——OpenAI Triton 与 PyTorch 2.0

> 原文：[How Nvidia’s CUDA Monopoly In Machine Learning Is Breaking - OpenAI Triton And PyTorch 2.0](https://newsletter.semianalysis.com/p/nvidiaopenaitritonpytorch) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

过去十年间，机器学习软件开发的格局发生了重大变化。许多框架来了又去，但大多数都严重依赖 Nvidia 的 CUDA，并在 Nvidia GPU 上表现最佳。然而，随着 PyTorch 2.0 和 OpenAI 的 Triton 的到来，Nvidia 在这一领域的主导地位——主要源于其软件护城河——正在被打破。

本报告将涉及以下话题：为什么 Google 的 TensorFlow 输给了 PyTorch；为什么 Google 未能将其在 AI 领域的早期领先公开转化为商业成果；机器学习模型训练时间的主要构成；内存容量/带宽/成本之墙；模型优化；为什么其他 AI 硬件公司至今未能撼动 Nvidia 的主导地位；为什么硬件将开始变得更加重要；Nvidia 在 CUDA 上的竞争优势如何被抹平；以及 Nvidia 的某个竞争者在一家大型云厂商的训练芯片上取得的一场大胜。

以千英尺高空视角概括：机器学习模型的默认软件栈将不再是的 Nvidia 的闭源 CUDA。主动权本来握在 Nvidia 手里，但他们却任由 OpenAI 和 Meta 掌控了软件栈。由于 Nvidia 自家专有工具的失败，那个生态系统构建起了自己的工具，而如今 Nvidia 的护城河将被永久性削弱。

# **TensorFlow 对决 PyTorch**

若干年前，框架生态还相当碎片化，但 TensorFlow 是领跑者。Google 看起来即将掌控机器学习行业。他们握有先发优势——最常用的框架 TensorFlow，并且设计/部署了唯一获得成功的 AI 专用加速器 TPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/8e2121a6-9982-4d67-8347-293dcd047047_1334x873.png)
*https://thegradient.pub/state-of-ml-frameworks-2019-pytorch-dominates-research-tensorflow-dominates-industry/*

然而，最终获胜的是 PyTorch。Google 未能将先发优势转化为对新生机器学习行业的主导。如今，Google 在机器学习社区中多少处于孤立地位，因为它不使用 PyTorch 和 GPU，而是偏爱自己的软件栈和硬件。秉承 Google 的一贯作风，他们甚至还有第二个框架 Jax，与 TensorFlow 直接竞争。

关于 Google 在搜索和自然语言处理领域的主导地位将因大语言模型而衰退的讨论不绝于耳，尤其是来自 OpenAI 以及那些利用 OpenAI API 或正在构建类似基础模型的各种初创公司的模型。虽然我们认为这种悲观论调被夸大了，但那个故事留待日后再谈。尽管面临这些挑战，Google 仍站在[最先进机器学习模型](https://arxiv.org/abs/2212.13138)的最前沿。他们发明了 transformer，并在许多领域（PaLM、LaMBDA、Chinchilla、MUM、TPU）保持业界最优。

回到 PyTorch 为何获胜的问题。虽然其中不乏从 Google 手中夺取控制权的成分，但主要还是由于 PyTorch 相比 TensorFlow 在灵活性和易用性上的提升。如果从第一性原理层面剖析，PyTorch 与 TensorFlow 的区别在于使用「**Eager 模式（动态执行）**」而非「**图模式（Graph Mode）**」。

Eager 模式可以被视为一种标准的脚本化执行方式。深度学习框架在每次操作被调用时立即逐行执行，就像任何其他 Python 代码一样。这让调试和理解代码变得更容易，因为你可以看到中间操作的结果，并观察模型的行为方式。

相比之下，图模式分为两个阶段。第一阶段是定义一个表示待执行运算的计算图。计算图是一系列相互连接的节点，节点表示运算或变量，节点之间的边表示它们之间的数据流。第二阶段是对优化后的计算图进行延迟执行。

这种两阶段方法让理解和调试代码变得更难，因为在图执行结束之前，你看不到究竟发生了什么。这类似于「解释型」与「编译型」语言的差别，比如 Python 与 C++。Python 更容易调试，很大程度上正因为它是解释执行的。

尽管 TensorFlow 如今默认提供 Eager 模式，但研究界和大多数大型科技公司已围绕 PyTorch 收拢。一个例证是：几乎每一个登上新闻的生成式 AI 模型都基于 PyTorch。Google 的生成式 AI 模型基于 Jax，而非 TensorFlow。

当然，还有一长尾的图像网络（image net）在使用 TensorFlow 和 Keras 等其他框架，但新模型开发的算力预算全都流向了 PyTorch 模型。关于 PyTorch 为何获胜的更深入解释，见[此处](https://thegradient.pub/state-of-ml-frameworks-2019-pytorch-dominates-research-tensorflow-dominates-industry/)。总体而言，如果你在 NeurIPS（最主要的 AI 会议）会场里走一圈，所有生成式 AI 工作中，凡非 Google 出品，用的都是 PyTorch。

# **机器学习训练的组成**

如果将机器学习模型训练拆解到最简形式，模型的训练时间包含两大时间构成：

1. 计算（FLOPS）：在每一层内运行稠密矩阵乘法
2. 内存（带宽）：等待数据或层权重到达计算资源。常见的带宽受限运算包括各种[归一化](https://pytorch.org/docs/stable/generated/torch.nn.LayerNorm.html)、[逐元素运算](https://pytorch.org/docs/stable/torch.html)、[SoftMax](https://pytorch.org/docs/stable/generated/torch.nn.Softmax.html) 和 [ReLU](https://pytorch.org/docs/stable/generated/torch.nn.ReLU.html)。

在过去，机器学习训练时间的主导因素是计算时间，即等待矩阵乘法完成。随着 Nvidia GPU 的持续发展，这很快不再是首要问题。

Nvidia 的 FLOPS 借助摩尔定律提升了多个数量级，但更主要依靠的是架构变革，例如张量核心和更低精度的浮点格式。相比之下，[内存并未走上同样的路径](https://www.semianalysis.com/p/cxl-enables-microsoft-azure-to-cut)。

![](https://substack-post-media.s3.amazonaws.com/public/images/3a422e2d-f2d2-404e-aad4-dec31f47ce77_1187x862.png)

如果我们回到 2018 年——彼时 BERT 模型是最先进的，Nvidia V100 是最先进的 GPU——我们会发现矩阵乘法已不再是提升模型性能的主要因素。自那以后，最先进模型的参数量增长了 3 到 4 个数量级，而最快的 GPU 的 FLOPS 增长了一个数量级。

![](https://substack-post-media.s3.amazonaws.com/public/images/5c718323-fd9c-4c6d-8ea3-815dea887386_1513x487.png)
*https://arxiv.org/pdf/2007.00072.pdf*

即便在 2018 年，纯计算受限的负载占据了 99.8% 的 FLOPS，却只占 61% 的运行时间。归一化和逐元素运算的 FLOPS 分别比矩阵乘法低 250 倍和 700 倍，却消耗了模型近 40% 的运行时间。

# **内存墙**

随着模型规模持续飙升，大语言模型仅模型权重一项就要占用数百 GB（乃至 TB 级）内存。Baidu 和 Meta 部署的生产级推荐网络，因其庞大的嵌入表而需要数十 TB 的内存。大模型训练/推理中相当大一部分时间并非花在计算矩阵乘法上，而是花在等待数据到达计算资源上。显而易见的问题是：为什么架构师不把更多内存放到更靠近计算单元的地方？答案是 $$$。

![](https://substack-post-media.s3.amazonaws.com/public/images/a62c2392-d588-4fdf-8872-e51ba3335250_704x513.jpeg)

内存遵循一个从「近而快」到「慢而便宜」的层级结构。最近的共享内存池位于同一颗芯片上，通常由 SRAM 构成。一些机器学习 ASIC 尝试利用巨大的 SRAM 池来容纳模型权重，但这种做法存在问题。[即便是 Cerebras 约 $2,500,000 的晶圆级芯片](https://www.semianalysis.com/p/gpt-model-training-competition-heats)，片上也只有 40GB 的 SRAM。这一点内存容量不足以容纳一个 100B+ 参数模型的权重。

Nvidia 的架构一直只在裸片上使用少得多的内存。当前一代 A100 有 40MB，下一代 H100 有 50MB。在台积电（TSMC）的 5nm 制程节点上，1GB 的 SRAM 需要约 200mm^2 的硅片面积。一旦加上相关的控制逻辑/互联结构，就需要超过 400mm^2 的硅片面积，约为一颗 Nvidia 数据中心 GPU 总逻辑面积的 50%。考虑到 A100 GPU 售价 $10k+，而 H100 更接近 $20k+，从经济角度看这是不可行的。即使忽略 Nvidia 在数据中心 GPU 上约 75% 的毛利率（约 4 倍加价），对于全良品产品而言，每 GB SRAM 内存的成本仍将高达数百美元。

此外，片上 SRAM 内存的成本不会通过传统的摩尔定律工艺微缩降低多少。同样 1GB 的内存，在下一代台积电 3nm 工艺上实际成本反而更高。虽然 3D SRAM 会在某种程度上缓解 SRAM 成本问题，但那只是对曲线的暂时扳折。

[![](https://substackcdn.com/image/fetch/$s_!HwSb!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fbucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com%2Fpublic%2Fimages%2F0150776c-9bf2-4bea-a9c2-41b24b7a0f15_1280x1280.png)SemiAnalysisTSMC’s 3nm Conundrum, Does It Even Make Sense? – N3 & N3E Process Technology & Cost DetailedA couple of weeks ago, we were able to attend IEDM, where TSMC presented many details about their N3B and N3E, 3nm class process nodes. Furthermore, TSMC announced it would up its capital expenditure in Phoenix, Arizona, with a total of $40 Billion invested in Fab 21 phases 1 and 2. This fab would produce chips in the N5 and N3 families, respectively. This report will cover the process node transition, the excessive costs of TSMC’s most advanced technology, and how it will significantly accelerate changes in the industry towards…Read more4 years ago · 32 likes · 3 comments · Dylan Patel and Afzal Ahmad](https://www.semianalysis.com/p/tsmcs-3nm-conundrum-does-it-even?utm_source=substack&utm_campaign=post_embed&utm_medium=web)

内存层级中再往下一级，是紧耦合的片外内存 DRAM。DRAM 的延迟比 SRAM 高一个数量级（约 >100 纳秒 vs 约 10 纳秒），但也便宜得多（每 GB 几美元 vs 每GB 数百美元）。

DRAM 在过去数十年间沿着摩尔定律的路径前行。当 Gordon Moore 创造这一术语时，Intel 的主营业务正是 DRAM。他关于晶体管密度和成本的经济预测，对 DRAM 而言大致成立至约 2009 年。但自约 2012 年以来，DRAM 的成本几乎没有改善。

![](https://substack-post-media.s3.amazonaws.com/public/images/3f3c7f05-649b-4f02-91be-61c84a30888f_1697x883.png)

对内存的需求只增不减。DRAM 如今[已占服务器总成本的 50%](https://www.semianalysis.com/p/cxl-enables-microsoft-azure-to-cut)。这就是内存墙，而且它已经在产品中显现。对比 Nvidia 2016 年的 P100 GPU 和刚刚开始出货的 2022 年 H100 GPU：内存容量增长 5 倍（16GB -> 80GB），而 FP16 性能增长 46 倍（21.2 TFLOPS -> 989.5 TFLOPS）。

虽然容量是一大瓶颈，但它与另一大瓶颈——带宽——紧密相连。更高的内存带宽通常通过并行获得。尽管如今标准 DRAM 每 GB 只要几美元，但要获得机器学习所需的巨大带宽，Nvidia 使用的是 HBM 内存——一种由 [3D 堆叠 DRAM 层构成、需要更昂贵封装的器件](https://www.semianalysis.com/p/advanced-packaging-part-1-pad-limited)。算上封装和良率成本，HBM 的价格在每 GB $10 到 $20 区间。

内存带宽与容量的成本约束在 Nvidia 的 A100 GPU 上不断显现。若不经过重度优化，A100 的 FLOPS 利用率往往很低。FLOPS 利用率衡量的是：训练一个模型实际所需计算的总 FLOPS，与 GPU 在该模型训练时间内理论上可计算的 FLOPS 之比。

即使有顶尖研究人员的重度优化，60% 的 FLOPS 利用率对大语言模型训练而言已算非常高的利用率。其余时间都是开销：等待来自另一项计算/内存的数据的空闲时间，或是为了缓解内存瓶颈而即时重算结果。

从当前一代 A100 到下一代 H100，FLOPS 增长超过 6 倍，但内存带宽仅增长 1.65 倍。这引发了对 H100 利用率低下的诸多担忧。A100 需要[许多技巧](https://www.mosaicml.com/composer)来绕过内存墙，而 H100 将需要实施更多。

H100 为 Hopper 带来了[分布式共享内存和 L2 多播](https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/)。其理念是不同的 SM（可理解为核心）可以直接写入另一个 SM 的 SRAM（共享内存/L1 缓存）。这[有效增大了缓存规模并降低了 DRAM 读写所需的带宽](https://www.nvidia.com/en-us/on-demand/session/gtcfall22-a41095/)。未来架构将依赖向内存发送更少的操作，以将内存墙的影响降到最低。应当指出，更大的模型往往能达到更高的利用率，因为 FLOPS 需求呈更指数级的增长，而内存带宽和容量需求则趋于更线性地增长。

# **算子融合——权宜之计**

> 正如训练 ML 模型一样，弄清你所处的运行区间（regime）能让你聚焦于真正重要的优化。例如，如果你的时间全部花在内存搬运上（即处于内存带宽受限区间），那么提升 GPU 的 FLOPS 无济于事。反过来，如果你的时间全部花在大型矩阵乘法上（即计算受限区间），那么把模型逻辑重写成 C++ 来降低开销也帮不上忙。
>
> <https://horace.io/brrr_intro.html>

再回到 PyTorch 获胜的原因：是 Eager 模式带来的灵活性与易用性提升，但转向 Eager 模式并非全是阳光和彩虹。在 Eager 模式下执行时，每个操作都从内存读出、计算、再写回内存，然后才处理下一个操作。如果不做重度优化，这会显著推高内存带宽需求。

因此，Eager 模式下执行模型的主要优化方法之一叫做算子融合（operator fusion）。操作不再把每个中间结果写入内存，而是被融合起来，让多个函数在一次 pass 中完成计算，以尽量减少内存读写。算子融合改善了算子分发、内存带宽和内存容量成本。

![](https://substack-post-media.s3.amazonaws.com/public/images/40995db9-3a8d-4917-8943-c313807d92b9_3420x1952.png)
*https://horace.io/brrr_intro.html*

这种优化通常需要编写自定义 CUDA kernel，但这比使用简单的 Python 脚本难得多。作为一种内建的折中，PyTorch 随时间推移在框架内原生实现了越来越多的算子。其中许多算子只是把多个常用操作融合为一个更复杂的单一函数。

算子的增加既让在 PyTorch 中创建模型变得更容易，也让 Eager 模式的性能因内存读写减少而变得更快。副作用是 PyTorch 在几年内膨胀到超过 2,000 个算子。

![](https://substack-post-media.s3.amazonaws.com/public/images/437175e3-1af1-451e-941e-5715858cff16_690x862.png)

我们想说软件开发者很懒，但说实话，几乎所有人都懒。一旦习惯了 PyTorch 中某个新算子，他们就会一直用它。开发者甚至可能并未察觉性能提升，而只是因为用它意味着少写代码。

此外，并非所有操作都能融合。决定哪些操作融合、哪些操作在芯片和集群层面分配给特定计算资源，往往要耗费大量时间。哪些操作在哪里融合的策略虽然大体相似，但会因架构不同而差异显著。

# **Nvidia 是王者**

算子的增长与默认地位帮助了 Nvidia，因为每个算子都很快针对其架构做了优化，却没有针对任何其他硬件优化。如果一家 AI 硬件初创公司想完整支持 PyTorch，就意味着要以高性能原生支持那份不断增长的 2,000 算子清单。

由于需要各种技巧来榨取最大性能，在 GPU 上以高 FLOPS 利用率训练巨型模型所需的人才门槛越来越高。Eager 模式执行加算子融合意味着，所开发出的软件、技术和模型都被推着去适配当前一代 GPU 的算力与内存之比。

所有开发机器学习芯片的公司都受制于同一堵内存墙。ASIC 受制于必须支持最常用的框架。ASIC 受制于默认的开发方法论——使用 Nvidia 与外部库混合、针对 GPU 优化的 PyTorch 代码。在这种背景下，一种舍弃 GPU 各类非计算包袱、换取更多 FLOPS 和更严格编程模型的架构，几乎没有立足之地。

**易用性为王。**

打破这一恶性循环的唯一方法，是让在 Nvidia GPU 上运行模型的软件能以尽可能小的代价无缝迁移到其他硬件。随着模型架构趋于稳定，PyTorch 2.0、OpenAI Triton [以及 MosaicML 等 MLOps 公司](https://www.mosaicml.com/composer)的抽象层成为默认，芯片方案的架构与经济性将开始取代 Nvidia 优越软件所赋予的易用性，成为采购决策的最大驱动因素。

# **PyTorch 2.0**

就在几个月前，[PyTorch 基金会成立并从 Meta 羽翼下独立](https://ai.facebook.com/blog/pytorch-foundation/)。伴随这一向开放开发与治理模式的转变，2.0 已发布供早期测试，并将于 3 月全面可用。PyTorch 2.0 带来诸多变化，但最根本的区别在于它新增了一个支持图执行模式的编译方案。这一转变将让充分利用各类硬件资源变得容易得多。

PyTorch 2.0 在 Nvidia A100 上带来[86% 的训练性能提升](https://www.youtube.com/watch?v=ppWKVg-VxmQ)，在 CPU 上[推理性能提升 26%](https://www.youtube.com/watch?v=ppWKVg-VxmQ)！这大幅降低了训练模型所需的计算时间与成本。这些收益可以延伸到 [AMD](https://www.semianalysis.com/p/amd-to-infinity-and-beyond)、[Intel](https://www.semianalysis.com/p/intel-is-throwing-the-kitchen-sink)、[Tenstorrent](https://www.semianalysis.com/p/tenstorrent-blackhole-grendel-and)、Luminous Computing、[Tesla](https://www.semianalysis.com/p/tesla-dojo-unique-packaging-and-chip)、Google、[Amazon](https://www.semianalysis.com/p/amazon-graviton-3-uses-chiplets-and)、Microsoft、[Marvell](https://www.semianalysis.com/p/marvelldeepdive2022)、[Meta](https://www.semianalysis.com/p/meta-discusses-ai-hardware-and-co)、[Graphcore](https://www.semianalysis.com/p/graphcore-announces-worlds-first?s=w)、[Cerebras](https://www.semianalysis.com/p/gpt-model-training-competition-heats)、SambaNova 等的其他 GPU 和加速器。

对于目前未经优化的硬件，PyTorch 2.0 带来的性能提升会更大。Meta 等公司重金贡献 PyTorch，源于他们想在自己的、由 GPU 组成的数十亿美元训练集群上，以更少精力更容易地实现更高的 FLOPS 利用率。他们也有动力让自己的软件栈更易移植到其他硬件，从而给机器学习领域引入竞争。

PyTorch 2.0 还为[分布式训练带来进步](https://www.youtube.com/watch?v=bGo-2xNvNAc)，为数据并行、[分片](https://pytorch.org/blog/introducing-pytorch-fully-sharded-data-parallel-api/)、[流水线并行](https://github.com/pytorch/tau)和张量并行提供更好的 API 支持。此外，它在整个栈中原生支持动态形状（dynamic shapes），这在许多场景中[让支持 LLM 的可变序列长度变得容易得多](https://www.youtube.com/watch?v=rn-kJQ-7JmQ)。这是首个从训练到推理全链路支持动态形状的大型编译器。

![](https://substack-post-media.s3.amazonaws.com/public/images/05aab965-a207-4d01-b680-6c0fb7bdcc8a_936x656.png)

# **PrimTorch**

为 PyTorch 编写一个完整支持全部 2,000+ 算子的高性能后端，对除 Nvidia GPU 以外的每一种机器学习 ASIC 而言都很困难。PrimTorch 把算子数量降到约 250 个原语算子，同时保持 PyTorch 终端用户的易用性不变。PrimTorch 让实现各种非 Nvidia 的 PyTorch 后端变得更简单、更可及。定制硬件和系统厂商可以更轻松地搭建起自己的软件栈。

# **TorchDynamo**

转向图模式需要一个稳健的图定义。Meta 和 PyTorch 尝试实现这一点已有约 5 年，但他们想出的每个方案都有重大缺陷。他们最终用 TorchDynamo 破解了这道难题。TorchDynamo 能摄取任何 PyTorch 用户脚本——包括那些调用第三方库的脚本——并生成 [FX 图](https://arxiv.org/pdf/2112.08429.pdf)。

Dynamo 把所有复杂操作降低（lower）为 PrimTorch 中的约 250 个原语操作。图一旦形成，未使用的操作会被丢弃，图会决定哪些中间操作需要存储或写入内存、哪些有被融合的可能。这大幅降低了模型内部的开销，同时对用户完全无缝。

TorchDynamo 已适用于[测试的 7,000 个 PyTorch 模型中超过 99%](https://dev-discuss.pytorch.org/t/torchdynamo-update-8-torchdynamo-passed-correctness-check-on-7k-github-models/663)——包括来自 OpenAI、HuggingFace、Meta、Nvidia、Stability.AI 等的模型——**且无需对原始代码做任何修改**。受测的 7,000 个模型是从 GitHub 上使用 PyTorch 的最热门项目中不加甄别地挑选的。

![](https://substack-post-media.s3.amazonaws.com/public/images/1d458fdc-ae3c-406c-9ca2-16f011b7081a_1058x736.png)

Google 的 TensorFlow/Jax 和其他图模式执行管线通常要求用户确保自己的模型符合编译器架构，图才能被捕获。Dynamo 通过启用部分图捕获、守卫图捕获（guarded graph capture）和即时重捕获（just-in-time recapture）改变了这一点。

- 部分图捕获允许模型包含不支持的/非 Python 结构。当无法为模型的某一部分生成图时，会插入一个图断点（graph break），不支持的结构将在各部分图之间以 Eager 模式执行。
- 守卫图捕获检查被捕获的图是否可有效执行。守卫（guard）是指任何需要重新编译的变更。这一点很重要，因为同一段代码运行多次不应触发多次重编译。
- 即时重捕获允许在已捕获的图无法有效执行时重新捕获该图。

![](https://substack-post-media.s3.amazonaws.com/public/images/fc42cb6d-5aaa-471b-b65f-fae82146fbd2_1920x966.png)

PyTorch 的目标是打造一个统一前端，以流畅的 UX 借助 Dynamo 生成图。这一方案的用户体验保持不变，但性能可以显著提升。捕获图意味着执行可以在大规模计算资源上更高效地并行化。

Dynamo 和 [AOT Autograd](https://pytorch.org/functorch/stable/notebooks/aot_autograd_optimizations.html) 随后将优化过的 FX 图传递给 PyTorch 原生编译层 TorchInductor。硬件公司也可以拿这张图输入自己的后端编译器。

# **TorchInductor**

TorchInductor 是一个 Python 原生深度学习编译器，为多种加速器和后端生成快速代码。Inductor 接收含有约 250 个算子的 FX 图，并将其降低到约 50 个算子。随后 Inductor 进入调度阶段，在此完成算子融合并确定内存规划。

接着 Inductor 进入「Wrapper Codegen（包装代码生成）」阶段，生成在 CPU、GPU 或其他 AI 加速器上运行的代码。包装代码生成器取代了编译器栈中的解释器部分，可以调用 kernel 并分配内存。后端代码生成部分针对 GPU 利用 OpenAI Triton，输出 PTX 代码。针对 CPU，则由一个 Intel 编译器生成 C++（也能在非 Intel CPU 上运行）。

未来将支持更多硬件，但关键在于 Inductor 大幅减少了编译器团队为其 AI 硬件加速器打造编译器所需的工作量。此外，代码在性能上更为优化，内存带宽和容量需求显著降低。

> 我们不想构建一个只支持 GPU 的编译器。我们想要的是能扩展支持各种硬件后端的东西，而同时具备 C++ 和 [OpenAI] Triton 正是这种通用性的保证。
>
> [Jason Ansel – Meta AI](https://www.youtube.com/watch?v=ppWKVg-VxmQ)

# **OpenAI Triton**

OpenAI 的 Triton 对 Nvidia 机器学习闭源软件护城河构成了一个极具颠覆性的切入角度。Triton 直接接收 Python，或经由 [PyTorch Inductor 栈](https://github.com/pytorch/pytorch/blob/master/torch/_inductor/codegen/triton.py)输入。后者将是最常见的用例。Triton 随后将输入转换为 LLVM 中间表示（IR）再生成代码。就 Nvidia GPU 而言，它直接生成 PTX 代码，跳过 Nvidia 的闭源 CUDA 库（如 cuBLAS），转而使用 cutlass 等开源库。

CUDA 通常由专攻加速计算的人使用，但在机器学习研究者和数据科学家中知名度较低。高效使用 CUDA 并非易事，需要对硬件架构有深刻理解，这会拖慢开发过程。因此，机器学习专家可能需要依赖 CUDA 专家来修改、优化和并行化他们的代码。

Triton 弥合了这一鸿沟，让高级语言也能达到与低级语言相当的性能。Triton kernel 本身对典型 ML 研究者而言相当易读，这对易用性意义重大。Triton 自动处理内存合并（memory coalescing）、共享内存管理和 SM 内调度。Triton 对逐元素矩阵乘法帮助不大——这些运算已经做得非常高效。Triton 对高成本逐元素运算以及[降低更复杂操作的开销](https://github.com/HazyResearch/flash-attention/blob/main/flash_attn/flash_attn_triton.py)极其有用，例如 [Flash Attention](https://github.com/HazyResearch/flash-attention)——它把矩阵乘法作为更大的融合操作的一部分。

[分享](https://newsletter.semianalysis.com/p/nvidiaopenaitritonpytorch?utm_source=substack&utm_medium=email&utm_content=share&action=share)

OpenAI Triton 目前只官方支持 Nvidia GPU，但这一情况在不久的将来就会改变。未来将支持多家其他硬件厂商，这个开源项目正获得惊人的发展势头。其他硬件加速器直接对接 Triton 中 LLVM IR 的能力，大幅缩短了为一块新硬件构建 AI 编译器栈的时间。

Nvidia 庞大的软件组织缺乏远见，未能将其在机器学习软硬件上的巨大优势转化为机器学习默认编译器的地位。他们对易用性的忽视，让 OpenAI 和 Meta 的局外人得以创建一个可移植到其他硬件的软件栈。为什么他们不是那个为 ML 研究者打造 Triton 式「简化版」CUDA 的人？像 [Flash Attention](https://github.com/HazyResearch/flash-attention) 这样的东西，为什么出自博士生之手而非 Nvidia？

本报告余下部分将指出在 Microsoft 取得重大胜利的那款具体硬件加速器，以及多家公司正被快速集成到 PyTorch 2.0/OpenAI Triton 软件栈的硬件。此外，还将呈现相反的观点，为 Nvidia 在 AI 训练市场的护城河/实力辩护。

[获取团体订阅 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
