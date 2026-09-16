---
title: "TPU 推理外部化全速前进——InferenceX"
title_en: "TPU Inference Externalization Full Steam Ahead - InferenceX"
subtitle: "InferenceX，每美元性能最高提升 50%，TPU 软件栈快速外部化，客户群持续扩大，Ironwood，TPUv8i，CUDA 护城河被削弱"
date: 2026-09-07
source: https://newsletter.semianalysis.com/p/tpu-inferencex-full-steam
crawled: 2026-09-15
authors: ["Alec Ibarra", "Cam Quilici", "Bryan Shan", "Wenyao Gao", "Daniel Nishball", "Zane Fong", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# TPU 推理外部化全速前进——InferenceX

> 原文：[TPU Inference Externalization Full Steam Ahead - InferenceX](https://newsletter.semianalysis.com/p/tpu-inferencex-full-steam) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**InferenceX，每美元性能最高提升 50%，TPU 软件栈快速外部化，客户群持续扩大，Ironwood，TPUv8i，CUDA 护城河被削弱**

十多年来，整个行业眼看着 Google 用自研芯片建立起一个帝国。搜索、广告、YouTube 以及每一代 Gemini 都运行在 TPU 上。很少有加速器像它这样接受过如此多的架构审视，也很少有芯片引发过如此多关于「走出设计它的公司之后，其性能与经济性会是什么样」的争论。Anthropic 是 TPU 最大的用户，到 2029 年将超过 DeepMind 自身的用量。

![数据中心墙面的鱼眼视图：成排的服务器机柜、复杂的线缆与头顶的桥架。](https://substack-post-media.s3.amazonaws.com/public/images/679784de-e6df-4cb4-8bf6-3347cb9ed002_1200x588.png)
*来源：Google*

Google 内部的成功从来不是问题。问题在于：行业里的其他人到底能真正拿到这份优势中的多少。你能不能拿一个开源权重模型，用一个熟悉的推理引擎来提供服务，并在对你业务最关键的经济性指标上击败 NVIDIA？

今天，我们在 [InferenceX](https://inferencex.semianalysis.com/) 官方预览版上发布 TPUv7 Ironwood 的首批第三方推理结果。在与 B200/B300 的同口径对比中，Ironwood 的每美元性能最高领先 50%。它的优势覆盖 Pareto 曲线的大部分区间，我们从两侧审视其经济性：Google 内部的总拥有成本，以及真实客户支付的外部 TCO。

Ironwood（TPUv7）是 Google 第一代真正去争夺外部推理负载的产品：这些芯片既可以直接买断，也可以通过 Google 自家云租用。[2025 年 11 月我们就已指出](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the)，Anthropic 非常青睐 TPU，承诺采购超过 100 万颗（其中约 40 万颗以上为直接采购，60 万颗以上通过 GCP 租用），主要用于训练，但也用于推理。[我们的加速器模型收录了 Anthropic TPU 出货量与 Google 整体 TPU 逐季度出货量的最新数字，以及对 TPUv8i、v8t 和多款 v9 / v10 的预估等更多内容。](https://semianalysis.com/accelerator-hbm-model/)

新的 TorchTPU 软件栈——TPU 的外部软件栈——的发展速度令我们兴奋。在文章后面，我们会讨论 TPU 软件外部化仍需完成的工作，包括优化投机解码（speculative decoding）、分离式预填充（disaggregated prefill）、KV 缓存卸载、多轮智能体负载等。即便如此，我们 SemiAnalysis **强烈认为 TPU 外部化正朝着正确方向全速前进。**此外，与仍在学习建立「测试先行」软件文化的 AMD 不同，Google 拥有数十年软件工程经验和极其成熟的质量驱动文化，因此我们预计外部 TPU 软件会快速走向成熟。

本文将覆盖为开源权重模型所做的 TPU 内核与推理服务栈的全部优化，包括 DP attention 优化、MoE 路由与内核优化、以及减少 GDN 内核中的 padding。我们还将深入解析 TPU 系统，并讨论杰出的 TPU 性能工程师们为了让这套软件栈广泛可用正在推进的下一步工作。

Google 花了十多年时间展示它能用 TPU 建造什么。现在轮到我们衡量行业里的其他人能用 TPU 做到什么了。

特别感谢 Google 团队（Chris Chan、Jahangir Hasan、Kyuyeun Kim、Wangyuan Zhang、Anne Stern、Puneith Kaul、Ruizi Dong、Sangam Jindal、Qi Zhou、Madhan Jaganathan、Gang Ji、Jun Wan、Devanshu Jain、Jiaxin Cao、Srinath Mandalapu、Haowen Ning）、Inferact 团队和 RedHat 团队（Michael Goin）打造了这个出色的 TPU 基础与性能！同时也要感谢同样在开发 TorchTPU SGLang 的 RadixArk 团队。

# InferenceX 官方预览：TPUv7 Ironwood 对阵 Blackwell 与 Blackwell Ultra

在与 Nvidia GPU 的同口径对比中，即将推出的原生 TorchTPU vLLM 软件栈已经交出了强劲成绩。Google 以 FP8 精度的 Qwen3.5 397B 作为初始 bring-up 模型。后文将深入解析：对于外部 TPU 上的 vLLM/SGLang 服务，为什么新的 TorchTPU 路线相比此前的 TorchAX 路径是一次显著进步。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

这一基础就位后，Google 计划将支持扩展到其他开源权重模型，包括 Kimi K3 和 GLM5.3。一旦少数几个模型被充分优化，我们认为在 day 0 附近为一大批流行开源模型添加优化支持就会容易得多。今天，vLLM 和 SGLang 的 day 0 支持集中在 Nvidia，对 AMD 的 day 0 覆盖只能算差强人意。我们预计 TorchTPU 在不久的将来会足够稳定，vLLM 和 SGLang 的维护者可能会把 TPU 加入 day 0 支持名单。该软件栈预计将于 10 月前后结束内测并开源。

在聚合服务（aggregated serving）、FP8、单 token 预测的同口径对比中，TPU 的每美元性能比以 FP8 运行聚合服务的 B200 和 B300 最高领先 50%。当在 NVIDIA GPU 上以 FP4 服务模型时，相对 FP8 存在质量损失。TPUv7 没有原生 FP4 计算，因此在 FP4 上 NVIDIA GPU 仍然保持领先。这一点将随着原生支持 FP4 的 TPUv8i 而改变，因此我们强烈认为 TPUv8i Boardfly 将足以与 Rubin NVL72 竞争。

我们认为，一旦 Google 启用分离式服务（disaggregated serving）与投机解码——并且在对比双方都开启 MTP 与分离式服务的前提下——TPU 的每美元性能优势能够保持。文章后面会讨论 Google 在 TorchTPU 基础就位后计划添加的优化。为了控制 bring-up 范围，Google 最初只针对 8k1k 进行了基准测试。但我们相信 TorchTPU 软件栈在智能体负载上同样会有惊人表现，今年晚些时候我们也会发布这部分结果。文章后段还会谈到 TPU 外部推理的下一步工作与路线图。

## TPU 是每美元性能之王

在每用户 100 tokens/s 的交互性下，Ironwood 的成本约为每百万总 token $0.181，而 B200 为 $0.222，B300 为 $0.276。这比 B200 低约 19%、比 B300 低 34%，同时提供相同的单用户生成速度。

在这组对比中，我们使用外部 TPU TCO 对比超大规模云厂商实验室采购 TPU 的 B200/B300 TCO。[去年，SemiAnalysis 加速器模型率先披露：Google 正在直接出售 TPU，而不仅仅是通过 Google Cloud 对外出租。](https://semianalysis.com/accelerator-hbm-model/)TPU 更低的小时成本抵消了它在交互性区间大部分范围内的吞吐劣势。[SemiAnalysis TCO 模型提供了 TPU BoM 估算与 TCO 估算的完整拆解。](https://semianalysis.com/ai-cloud-tco-model/)

![](https://substack-post-media.s3.amazonaws.com/public/images/8047a697-0d6f-41fe-8c16-71998778ecb4_2048x1228.png)
*来源：SemiAnalysis InferenceX 预览版*
![](https://substack-post-media.s3.amazonaws.com/public/images/d306f42c-a30b-45c7-82c9-dbaff7e654b3_2048x1228.png)
*来源：InferenceX 预览版*

在原始性能曲线的大部分区间，TPU 并没有超越 Nvidia GPU。但这一对比没有计入 TPU 更低的 TCO。**TPU 的买家主要关心的是自己能赚多少收入，也就是每美元性能和每瓦特性能。**

尽管如此，在每用户 20 tok/s 的交互性下，Ironwood 在原始吞吐上也处于领先，达到每颗芯片 9,364 总 tokens/s，而 B200 为 8,903，B300 为 8,925。在这组测试中，这比两款 GPU 都高约 5%。叠加更低的建模小时成本，Ironwood 每美元产出的 token 比 B200 多 50.4%，比 B300 多 96.0%。

![](https://substack-post-media.s3.amazonaws.com/public/images/69317046-6bae-4d80-9b8b-f9777076792d_2048x1228.png)
*来源：SemiAnalysis InferenceX 预览版*

如果按 Google 内部负载的 TPU TCO（$1.03/芯片·小时）计算，在并发 256 下每美元性能优势扩大到比 B200 高 76.7%、比 B300 高 130.2%。不过，这些高并发结果伴随着延迟上的取舍。例如在并发 256 下，TPU 的平均 TTFT 为 5.41 秒，而 B200 为 3.75 秒，B300 为 2.40 秒。前文讨论的 50% 至 96% 优势特指这一数据点，并非适用于每一个延迟目标。

![](https://substack-post-media.s3.amazonaws.com/public/images/ac73c91e-efa3-4f2a-a9ea-2f5eb15e4a27_2048x1222.png)
*来源：SemiAnalysis InferenceX 预览版*

从端到端延迟看，Ironwood 在最高吞吐点之后依然保持竞争力。在 20 秒中位响应时间下，Pareto 曲线上 TPU 约为每百万总 token $0.098，而 B200 为 $0.106，B300 为 $0.132。因此 TPU 的成本约比 B200 低 8%、比 B300 低 25%。

![](https://substack-post-media.s3.amazonaws.com/public/images/01cfa04c-b0fe-456d-ba3c-367c434f373c_2048x1223.png)
*来源：SemiAnalysis InferenceX 预览版*
![](https://substack-post-media.s3.amazonaws.com/public/images/b160a968-2cdc-4ce8-8a74-cd5eb63e1141_2048x1223.png)
*来源：SemiAnalysis InferenceX 预览版*

尽管有上述全部优势，在同口径曲线的一小段区间上 B200 仍然可以胜出，包括 30 秒中位响应时间附近。不过在更长的响应时间下，TPU 会重新夺回每百万 token 的成本优势，同时在图中重叠区间内对 B300 保持成本优势。

## 苹果对香蕉：GB300 NVL72 分离式 vs TPUv7 聚合式

Google 内部在生产环境运行分离式服务已有多年，那条路径经过深度优化，但外部 TPU 服务栈还没有一条完全优化的分离式路径。所以今天，在分离式对分离式的比较中，GB200/300 NVL72 在每美元性能上更有竞争力。但我们预计这一差距会在几个月内收窄，随着 Google、Inferact、RadixArk 和 SemiAnalysis 陆续落地优化，TPUv7 将能够与 GB200/300 NVL72 抗衡，我们也会在后续文章中发布 TPUv7 分离式 vs GB200/300 NVL72 分离式的对比。TPUv7 pod 可以通过低延迟 ICI 互联扩展到 1k+ 颗以上芯片，因此可以实现 NVIDIA NVL72 无法完成的大模型分离式与超宽 EP（ultra wide EP）优化。

即便是在 TPUv7 聚合式服务 vs GB300 NVL72 分离式这种「苹果对香蕉」的对比中，按内部 TCO 计算，TPUv7 在高延迟以及低至中等偏左延迟区间仍有相当的竞争力。但在中等偏右的 e2e 延迟区间，GB300 NVL72 分离式对 TPUv7 聚合式服务握有一项优势。

![](https://substack-post-media.s3.amazonaws.com/public/images/1883d94c-1996-47de-942b-c8eef7cf3eb1_1576x808.png)
*来源：SemiAnalysis*

从 GB300 NVL72 分离式 vs TPUv7 聚合式来看，两者在低和高 e2e 延迟两端都具竞争力，但在中间区间，GB300 对 TPUv7 聚合式有约 30% 的每美元性能优势。我们强烈相信，一旦 TPUv7 上的分离式服务完成优化，它将能在整条 Pareto 曲线上与 GB300 NVL72 全面竞争。

![](https://substack-post-media.s3.amazonaws.com/public/images/d2210f76-7a91-405e-a3ba-a1692b080618_1550x842.png)
*来源：SemiAnalysis*

# 使用全新原生、一等公民 TorchTPU 后端的推理服务 vs 此前的 TorchAX 软件栈

## 此前的 TorchAX vLLM 后端

Google 此前使用 TorchAX 后端，把 vLLM 和 SGLang 中基于 PyTorch 的实现翻译成 JAX。TorchAX 的初衷是让开发者通过 JAX 运行 PyTorch 模型定义。然而这条路的问题促使 Google 与 PyTorch、vLLM、SGLang 社区合作开发一条新路线：TorchTPU。它让开发者把 TPU 当作原生 PyTorch 设备使用，而 StableHLO、XLA 和面向 TPU 优化的 Pallas 内核在幕后负责底层执行。在接下来的章节中，我们将展示这个新 TorchTPU 后端与 NVIDIA Blackwell 及 Blackwell Ultra GPU 相比的性能。

vLLM 的 TPU 支持经历了三个阶段：

- 第一个 TPU 原型使用 [PyTorch/XLA](https://docs.pytorch.org/xla/master/learn/xla-overview.html)。其惰性执行模型把多个操作收集成计算图交给 XLA 编译，而不是立即执行每个 PyTorch 操作。
- 当前的公开后端 [tpu-inference](https://vllm.ai/blog/2025-10-16-vllm-tpu) 在有 TPU 优化版 JAX 实现时优先使用；否则由 TorchAX 把原始 PyTorch 模型翻译成 JAX 可执行的操作。目标是复用成熟的 TPU 原语与并行支持，而无需重写每一个 PyTorch 模型。
- 即将到来的第三个设计 TorchTPU 让 vLLM 把 TPU 当作原生 PyTorch 设备。今后它将成为 SGLang 和 vLLM 在 TPU 上的首选后端。

下图放大展示第二阶段，说明 vLLM 的 tpu-inference 后端如何将直接使用 JAX 的模型与经由 TorchAX 运行的 PyTorch 模型结合起来。

![](https://substack-post-media.s3.amazonaws.com/public/images/678ca15d-f0c0-4c36-a63f-b1108939cbb1_2048x1620.png)
*来源：SemiAnalysis/vLLM*

当初选择 JAX 是务实的。在上一次[公告](https://vllm.ai/blog/2025-10-16-vllm-tpu)中，Google 描述了底层优化、paged attention 以及让 vLLM 的 worker 模型适配 TPU 执行的困难。他们认为 JAX 能提供更成熟的 TPU 原语与并行支持。TorchAX 让团队无需重写每个 PyTorch 模型就能用上这些能力，同时面向 TPU 的 JAX 实现可以共享同样的内核与编译器工作。

使用 TorchAX 时，开发者仍然用 PyTorch 编写模型，但由 JAX 在 TPU 上执行。TorchAX 充当两个框架之间的翻译层。正如 [TorchAX 文档](https://google.github.io/torchax/user_guide/how-it-works/)所解释的，torchax.tensor.Tensor 的行为与普通 PyTorch 张量一样，但底层由 jax.Array 支撑。当模型调用一个张量操作（在 PyTorch 中称为 ATen 操作）时，TorchAX 通过 __torch_dispatch__ 钩子拦截它，并翻译成一个或多个 JAX 操作。因此即便计算由 JAX 完成，模型仍可保持用 PyTorch 编写。

vLLM 还必须管理生成过程中不断变化的状态，尤其是 KV 缓存——它保存早期 token 的注意力信息以便复用。其[模型包装器](https://github.com/vllm-project/tpu-inference/blob/a32e183a676cf428cb1cea953f58fdd616accb3e/tpu_inference/models/vllm/vllm_model_wrapper.py#L171-L348)把模型权重和 KV 缓存以显式状态的形式呈现给 JAX。这一过程称为函数化（functionalization），把原本发生在 Python 对象内部的状态变化转换成编译器可以追踪的输入与输出。随后 jax.jit 可以把每个推理步骤捕获为计算图，送入 JAX 编译流水线以供反复执行。

在此之上，各组件分工明确。Pallas 为性能关键操作提供经优化的 TPU 内核。StableHLO 以编译器可处理的标准化格式表示程序，XLA 再把它转换成 TPU 的可执行代码。在 vLLM 的标准 PyTorch 路径中，torch.compile 负责协调图捕获与编译。在 TorchAX 路径中，JAX/XLA 流水线已经完成了这些任务，因此 vLLM 绕过了通常的 torch.compile 路线。这些翻译层引发的诸多问题，正是 TorchTPU vLLM 软件栈要解决的。

### 此前的 SGLang JAX 后端

![](https://substack-post-media.s3.amazonaws.com/public/images/63ea9afd-01ea-4df3-b632-3524e2507d04_2048x1742.png)
*来源：SemiAnalysis/SGLang*

SGLang 当前的公开 TPU 软件栈使用 [SGLang-JAX](https://github.com/sgl-project/sglang-jax)。SGLang-JAX 与 vLLM 的 TorchAX 后端做出了类似的取舍，但采用了不同的方式：它是一个独立的 JAX 原生推理引擎，而不是经由 TorchAX 翻译的 PyTorch SGLang 运行时。它把 SGLang 式的调度与前缀缓存与 JAX 模型及 TPU 专用内核结合在一起。Google 和 RadixArk 已宣布推出 SGL-torchtpu，作为额外的 PyTorch 原生后端来扩展可用的服务路径。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

## 转向全新原生、一等公民的 TorchTPU 后端

[TorchTPU](https://developers.googleblog.com/torchtpu-running-pytorch-natively-on-tpus-at-google-scale/) 把框架边界移到了 PyTorch 自身。它利用 PyTorch 的 [PrivateUse1 后端扩展点](https://docs.pytorch.org/tutorials/advanced/privateuseone.html)，在 device=”tpu” 上暴露一个普通的 torch.Tensor，而不是一个由 JAX 数组支撑的包装器。PyTorch 调度器把 ATen 操作路由到 TPU 后端。开发者可以以 eager 模式运行代码用于 bring-up 和调试，也可以调用 torch.compile 进行图捕获。在编译路径中，TorchDynamo 和 AOTAutograd 生成 FX 图，TorchTPU 将其降级为 StableHLO，XLA 再生成 TPU 可执行代码。Google 的[会议幻灯片](https://hosted-files.sched.co/pytorchconferenceeu2026/cb/TorchTPU%20-%20PyTorch%20Paris%20%2726%20-%20Google%20Slides.pdf)明确说明了编译器选择：这条路使用 XLA，而不是 Inductor 和 Triton。

![](https://substack-post-media.s3.amazonaws.com/public/images/c09d8e99-682d-43dd-9292-3cf29295f79e_1074x1148.png)
*来源：SemiAnalysis/PyTorch/Google*

因此「原生」有其明确的边界：它覆盖 PyTorch 张量、调度、eager 执行、编译入口和分布式 API。XLA 仍是编译器，内核层继续使用 TPU 专用实现。TorchTPU 可以调用 Pallas 和基于 JAX 的自定义内核。[Helion 的 TPU 后端](https://pytorch.org/blog/helion-on-tpu-towards-hardware-heterogeneous-kernel-authoring/)同样会生成 Pallas。面向用户的框架变成了 PyTorch 原生，而编译器与性能关键内核仍然面向 TPU。

开发者可以使用 .to(”tpu”)，同时保留熟悉的分布式接口和推理引擎代码。Google 文档说明支持 DDP、FSDP2、DTensor、每设备一个进程，以及 MPMD 与 SPMD 两种执行方式。这些接口与 PyTorch 推理引擎已采用的进程与分布式模型相吻合。

对 vLLM 和 SGLang 而言，机会在于复用更多上游模型代码、调度器、连续批处理（continuous batching）、API 和特性逻辑，而不是在 PyTorch 到 JAX 的边界上重建一遍。这应能降低模型与引擎特性的 bring-up 成本，即便最终 TPU 实现仍需要专用内核。

原生 PyTorch 支持并不能免除 TPU 专用优化的需要。Pallas 与 TorchAX 的用途不同：TorchAX 让 PyTorch 模型代码经由 JAX 执行，而 Pallas 用于直接为 TPU 硬件实现性能关键操作。移除 TorchAX 并不意味着移除其下层的 Pallas 内核。由于 TorchTPU 允许原生 PyTorch 代码调用 Pallas 和 JAX 内核，为早期软件栈开发的内核可以迁移到新栈中。

与 GPU 上的 PyTorch vLLM 类似，高性能推理仍然需要自定义内核。张量形状与布局仍需调优，才能高效使用 TPU 的矩阵乘法单元。我们相信现有 Pallas 内核大多可以顺畅迁移到新的原生 TorchTPU 服务栈，但这并不意味着每个内核都能原封不动地迁移。诸如包装器、张量布局、运行时集成等许多环节仍可能需要小幅适配与验证。

## 与 Google TPU 团队的强生态系统协作

vLLM 和 SGLang 是两大主流开源生产级推理服务栈。Inferact、RadixArk 和 Red Hat 正在大力投入与 Google 的协作，让 TorchTPU 后端在这两个栈中都成为一等公民体验。这种社区支持对 TPU 推理外部化极其重要。

![](https://substack-post-media.s3.amazonaws.com/public/images/9d86a8b7-cc12-4730-9b6a-a77258ad60c5_1860x720.png)
*来源：Inferact*

截至九月初，TorchTPU 仍处于内测阶段，将在 10 月中旬 PyTorch Conference 期间开源。我们很高兴看到它推动 TPU 在 PyTorch、vLLM 和 SGLang 中走向一等公民体验。TorchTPU vLLM 与 TorchTPU SGLang 开源后，我们会将 InferenceX/AgentX 的 TPU 基准测试从我们的 fork 迁移到公开仓库。

![](https://substack-post-media.s3.amazonaws.com/public/images/8304bd1c-ed83-4091-a71b-00ec572542a4_1200x675.png)
*来源：RadixArk*

# TPU 推理优化深度解析

为原生 TorchTPU 服务栈首个 bring-up 模型优化 TPU 推理的冲刺，投入了数百个工程小时和大量 PR。如后文所述，TPU 架构与 GPU 架构不同，因此需要一套自己的优化才能高效运行模型。下文描述的优化改善了（在某些情况下是首次实现了）Qwen3.5-397B 及其他模型在 Ironwood 上的性能。其中大部分 Pallas 内核优化可以迁移到新的原生 TorchTPU 软件栈。

## DP Attention 优化

有一个问题并非 TPU 独有：如何把模型架构中的并行度有效映射到硬件。例如 Qwen3.5 的 GQA 注意力层有 32 个查询头，却只有 2 个共享 KV 头。在 TP8（八个逻辑设备）下，查询计算可以均摊到 8 个设备上，每设备 4 个查询头。但 KV 头无法在这些设备间均分。每个 KV 头被 16 个查询头共享，意味着四个设备需要相同的 KV 数据来计算各自的局部注意力。当 TP 数超过 KV 头数时，标准做法是在各 TP rank 间复制 KV 头。vLLM 已支持这一点，TPU 后端只需一个[兼容性修复](https://github.com/vllm-project/tpu-inference/pull/2661)来激活这一既有行为，避免不必要的 All-to-All 通信。

面向更高并发的服务，TPU 后端还新增了对[八路注意力数据并行（DP8）](https://github.com/vllm-project/tpu-inference/pull/2187)与八路专家并行（EP8）相组合的支持，简称「DP attention」或 DEP8。此时不再把每个请求的注意力拆分到全部八个设备，而是每个设备处理不同的请求子集，并在本地保留这些请求的两个 KV 头。注意力权重仍是复制的，但 KV 缓存保存的是不同的请求历史，而不是同一历史的重复副本。与此同时，512 个路由专家仍然分布在各设备上，避免了体积大得多的专家权重池被复制。要实现这一点，需要在推理引擎中[协调请求分配、循环状态槽位和块表（block table）](https://github.com/vllm-project/tpu-inference/pull/2577)。

![](https://substack-post-media.s3.amazonaws.com/public/images/e1f13662-fc12-400e-889e-9958d0ad45f7_2048x770.png)
*来源：SemiAnalysis*

## 通信优化

在 DP attention 与 EP 下，TPU 的 GroupedGEMM 实现会在专家运行前 all-gather 收集 token 激活值和路由元数据，再用 reduce-scatter 对加权输出求和，把每个 token 的结果送回其注意力 rank。后端最初分开收集被选中的专家 ID 与路由权重。Google [把两者合并为一次 all-gather](https://github.com/vllm-project/tpu-inference/pull/2174)，去掉了一个额外的集合通信——对这么小的数组，其延迟可能主导传输时间。该 PR 报告在 DeepSeek-V3 测量中每层节省约 [80 微秒](https://github.com/vllm-project/tpu-inference/pull/2174)。80 µs 听起来不多，但 DeepSeek-V3/R1 有 58 层需要这个 AllGather。这些层累计起来，单次前向传播可节省约 4.64 ms（80 µs × 58），从而降低 TPOT、提升交互性。

![](https://substack-post-media.s3.amazonaws.com/public/images/59c3d46f-7b88-4e65-8715-f160b83c3d6e_2048x771.png)
*来源：SemiAnalysis*

Google 还[在 SparseCore 上实现了 ReduceScatter 集合通信](https://github.com/vllm-project/tpu-inference/pull/2888)（它更适合数据搬运这类不规则操作），并利用 Ironwood 更快的裸片间链路先在每颗芯片内部合并贡献，再跨芯片交换部分和。这种每芯片两设备的布局以及芯片间 ICI 网络将在下一节展开。双缓冲让内核传输一个数据块的同时累加另一个，使本地归约与裸片间传输同较慢的芯片间流量重叠。把集合通信放到 SparseCore 上运行还能把 TensorCore 的执行腾给其他操作。

![](https://substack-post-media.s3.amazonaws.com/public/images/4c82923a-c144-4447-8b73-f622ba7df27e_2048x1357.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/e9c2975f-0974-414f-8af6-300bc8613121_2048x1202.png)
*来源：Google 与 SemiAnalysis*

在上图中，各通信阶段相互重叠，缩短了端到端执行时间。以标注为 t_1 的时刻为例：此时芯片内 DMA ScatterReduce（P1）已完成 MB（microbatch）1 的处理。ICI dim 0 上的 ScatterReduce（P2.0）现在可以对 MB0 进行，并与后续 MB 的 P1 *同时*执行。相对于基线，该优化[在并发 64 到 512 区间使 8k1k 吞吐提升 4.1% 至 14.2%](https://github.com/vllm-project/tpu-inference/pull/2888)（其中并发 256 下为 8.5%），并在并发 512 下使 1k8k 吞吐提升 26.1%。

感谢阅读 SemiAnalysis！本文为公开文章，欢迎随意分享。

[分享](https://newsletter.semianalysis.com/p/tpu-inferencex-full-steam?utm_source=substack&utm_medium=email&utm_content=share&action=share)

把这个集合通信从 TensorCore 挪到 SparseCore 也意味着集合通信运行时，TensorCore 上可以流水线排入更多工作。但并非每个集合通信都值得迁移。某些情况下，把集合通信卸载到 SparseCore 反而会*恶化*性能。例如对 Qwen3.5，现在[由一个阈值决定 all-reduce 与 all-gather 何时卸载到 SparseCore](https://github.com/vllm-project/tpu-inference/pull/2777)，**当小集合通信能装进 VMEM、而 SparseCore 卸载开销会使其变慢时，就让其留在 TensorCore 上**。默认阈值由 VMEM 容量推导而来。该 PR 报告 8k1k 吞吐在并发 64 下提升 2.7%，并发 128 下提升 5.7%。

## 优化 MoE 路由与专家内核

混合专家（MoE）层为每个专家产生不规则的 token 组，这些参差不齐的组必须被重排成 TPU 矩阵单元能够高效消化的形式。下面的一些改动是路由与 grouped-matmul 后端的通用改进，任何 MoE 模型都能受益；另一些则直接在 Qwen3.5 上测得。

[第二版 grouped matmul](https://github.com/vllm-project/tpu-inference/pull/1688) 重构了专家输入送入 MXU 的方式。它去除了冗余的 tile 计算，按有效行数而非填充后的最大值来规划传输规模，对专家权重做三重缓冲，使下一组的权重在当前组计算时已在传输途中，并把组元数据生成融合进内核。

专家输入的不规则重排随后[被移到 SparseCore 上](https://github.com/vllm-project/tpu-inference/pull/2137)。SparseCore 负责数据搬运，把每个专家的 token 收集成连续组，TensorCore 则专心执行专家矩阵乘法。[随后的又一次重写](https://github.com/vllm-project/tpu-inference/pull/2836)改进了内存读取流水线，并把合并（combine）工作拆分到 token 和隐藏维度上。该 PR 报告，相比原始 SparseCore 内核，8k1k 服务吞吐提升 12%，TTFT 与 TPOT 同步下降。

![](https://substack-post-media.s3.amazonaws.com/public/images/c47d1e6a-dad4-48bc-8239-9194bea17544_2048x838.png)
*来源：SemiAnalysis*

另一项优化[把 ragged gather-reduce 路径中的 top-k 权重 gather 移到了 SparseCore 上](https://github.com/vllm-project/tpu-inference/pull/2634)。这里的 gather 指在单设备上从内存读取被选中的条目，而不是跨设备的 all-gather。此前 TensorCore 在预处理阶段收集路由权重和源索引，限制了 TensorCore/SparseCore 的重叠。把这些 gather 移入 SparseCore 内核后，在 batch 2k、16 路专家并行的 DeepSeek-V3 微基准中，TensorCore 开销从 29 µs 降到 14 µs，整体操作延迟从 146 µs 降到 137 µs。

对小 batch 而言，通用 ragged 路径的开销超过了它所整理的工作本身。因此一个[专用的小 batch 置换方案](https://github.com/vllm-project/tpu-inference/pull/2674)构建 one-hot 矩阵，用普通矩阵乘法把 token 置换到对应专家、再把结果置换回来。在 8k1k 负载上，这使吞吐在并发 64 下提升 7.3%，并发 128 下提升 5.1%。

一项进行中的（WIP）改动[把专家 ID 与 token 索引打包成单个排序键](https://github.com/vllm-project/tpu-inference/pull/3488)，让 XLA 执行更简单的排序，同时保留所需的顺序。排序延迟从 106.6 µs 降至 21.7 µs。该 PR 报告 8k1k 服务性能提升 0.6% 至 8.5%，而且同一改动还使 FP8 all-gather 成为可能。

## 优化 Gated DeltaNet Pallas 内核

Gated DeltaNet（GDN）是一种循环计算。也就是说，每一步中运行状态先衰减，再用一个秩一项（rank-one term）更新，最后投影产生输出。关于 GDN 等线性注意力机制的深入解析，请参阅以下文章：

下面的改动展示了它的矩阵运算、向量更新与状态传输如何在 MXU、VPU、VMEM 和 HBM 之间调度。[最初的 Qwen3.5 支持](https://github.com/vllm-project/tpu-inference/pull/2004)加入了 causal Conv1D 与 GDN 的纯 JAX 实现，将其接入 TPU 算子分发，并启用了循环状态缓存。后续 PR 又对这些实现做了优化。

![](https://substack-post-media.s3.amazonaws.com/public/images/6ff82904-c377-4bbd-97a7-ad6eb54932ec_1875x925.png)
*来源：GitHub*

另一个「低垂果实」式的优化，是通过[重排输出投影计算中的代数式](https://github.com/vllm-project/tpu-inference/pull/2498)使 MXU 与 VPU 的工作重叠。此前 VPU 先对衰减后的状态施加秩一更新，然后 MXU 再将更新后的状态与查询相乘产生输出。这一依赖迫使 MXU 等待。

把衰减后的状态记为 S、修正向量记为 Δ、键和查询记为 k 和 q，输出可以展开为：

![](https://substack-post-media.s3.amazonaws.com/public/images/1c3573d3-b885-4a29-abc4-998df6ab3399_2048x263.png)
*来源：SemiAnalysis*

现在 MXU 可以直接从衰减状态计算 Sq，同时 VPU 为下一个 token 构造更新后的状态。本次更新对输出的贡献则单独用 kᵀq（每头一个标量点积）计算，再做一次小规模的缩放向量加法。这把状态更新从 MXU 的依赖路径中移除了。报告的 8k1k 吞吐提升为并发 64 下 2.79%、并发 512 下 4.48%。

下一个改动[减少了向量寄存器溢出（spill）](https://github.com/vllm-project/tpu-inference/pull/2741)：在解码循环内对 Q 和 K 切片，让同时存活的数据更少。decode-64 内核因此提速约 20%，但端到端收益较小——并发 512 下 8k1k 提升 0.8%、1k8k 提升 3.8%，因为该内核只是解码步骤的一部分。

[异步状态传输](https://github.com/vllm-project/tpu-inference/pull/2650)利用双缓冲让 DMA 与计算重叠。第二组缓冲占用的额外 VMEM 起初使数据并行注意力出现回退。通过复用现有 scratch 缓冲、缩短临时变量的生命周期，容量被找回，回退也随之消除。报告的 8k1k 吞吐提升为并发 512 下 11.3%。

[GDN v3](https://github.com/vllm-project/tpu-inference/pull/3016) 把 Conv1D 与 GDN 融合为单个内核以减少 HBM 往返，改进了 prefill 布局，并将混合 prefill/decode 执行统一到一条路径。报告的内核级加速为：decode 1.41×、prefill 1.60×、混合 batch 2.14×。这些测量只针对内核本身，并不代表端到端服务收益。

![](https://substack-post-media.s3.amazonaws.com/public/images/c6dad690-9354-48a2-846f-1f7107907e3d_2048x672.png)
*来源：SemiAnalysis*

仅仅改善内核内部各操作之间的重叠，就能带来显著的性能提升！

## 管理混合状态与 Paged Attention

Qwen3.5 是一个混合模型，有两种状态：GQA 层累积随每个 token 增长的 KV 历史，而 GDN 层为每个请求保存固定大小的循环状态。状态分配、存储精度、注意力页大小和物理数据布局共同决定了实际可用的 HBM 有多少、注意力运行得有多高效。

[批量 ragged paged attention](https://github.com/vllm-project/tpu-inference/pull/1961) 将序列打包在一起，预计算页元数据，并采用三重缓冲来改善流水线、减少 padding。这一改动为共享注意力后端奠定了基础。该 PR 的工作负载示例使用 Qwen3-32B，因此其测量结果应与 Qwen3.5-397B 的结果分开看待。

循环状态现在[采用紧凑分配](https://github.com/vllm-project/tpu-inference/pull/2416)，每个活跃请求约对应一个槽位，而不是每个层组都占用 `num_blocks` 个槽位。在报告的配置中，这收回了约 76 GiB 的 HBM，注意力块池扩大 71%，并发 64 下 1k8k 输出吞吐提升 18%。

[以 BF16 存储循环状态](https://github.com/vllm-project/tpu-inference/pull/2482)使其 HBM 占用减半，同时在 VMEM 内部保持 FP32 运算。这在保住 FP32 算术的同时节省了内存容量与传输带宽。报告的 1k8k 吞吐提升为并发 512 下 15%。

移除[旧的混合页大小对齐约束](https://github.com/vllm-project/tpu-inference/pull/2627)后，批量注意力可以使用合适的 2 的幂次页大小，包括 256 token。并发 512 下 1k8k 吞吐提升约 7%。这适用于非前缀缓存路径，与后文引入的对齐检查点模式是两回事。

![](https://substack-post-media.s3.amazonaws.com/public/images/ab7479c2-7b29-4ede-9796-9e8126a92b40_2048x756.png)
*来源：SemiAnalysis*

通过[根据 KV 头数选择 reshape 路径](https://github.com/vllm-project/tpu-inference/pull/2653)，避免了不必要的 KV 布局拷贝，而不是强加一个只有其他形状才需要的布局约束。并发 512 下 Qwen3.5 8k1k 吞吐提升约 4.1%。

## 减少 Padding 与低并发开销

当只有四个或八个请求在途时，为数百并发调优的配置就是在浪费算力：编译出的形状桶过大、元数据按配置的最大值规划、padding token 触发无效的专家计算。InferenceX 的工作点恰好处于这些低并发区间，由此催生了以下改动。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

请求元数据现在[按活跃请求数分桶](https://github.com/vllm-project/tpu-inference/pull/2513)，而不是始终按配置的最大值。在 8k1k 并发 64 测试中，GDN 调度开销从 283 µs 降至 97 µs，吞吐从每芯片 2,328 升至 2,516 tokens/s。

![](https://substack-post-media.s3.amazonaws.com/public/images/35b683ee-7e31-401a-8a8a-31c53e253aa2_2048x819.png)
*来源：SemiAnalysis*

[面向 InferenceX 的 Qwen3.5 专项调优](https://github.com/vllm-project/tpu-inference/pull/3080)缩小了 rotary 表、按 DP rank 规划序列上限，并为并发 4 增加了专用注意力桶。并发 4 下的综合收益为 8k1k 提升 13.3%、1k1k 提升 15.5%。

[又一轮低并发调优](https://github.com/vllm-project/tpu-inference/pull/3116)切换到 TP8 注意力加专家并行，减小最小 token 桶，并把 padding token 路由到 0 号专家，使其不再触发额外的专家权重加载。1k1k 的综合收益为并发 4 下 22.9%、并发 8 下 18.1%。8k1k 上，并发 4 吞吐提升 9.2%，但并发 8 下降 5.3%。

## 为混合模型启用前缀缓存

上述收益是在随机输入基准上测得的，请求之间没有任何共享。前缀缓存对智能体和多轮负载至关重要，因为它们会复用长的系统提示和对话历史。对混合模型来说，缓存的前缀必须同时保留其 KV 块和前缀末尾的 GDN 循环状态。而只要请求继续，该循环状态通常就会被覆写，这让前缀缓存比「常规」注意力模型更难。

[支持 DP 的混合前缀缓存](https://github.com/vllm-project/tpu-inference/pull/3422)通过为 GDN 提供分开的槽位解决了这个问题：一个用于读取检查点，一个用于写入活跃状态。请求继续时不再覆写与其缓存前缀关联的检查点。状态地址由块表推导——这正是定位 KV 块所用的同一结构。检查点按对齐的缓存粒度保存，因此保存的状态总是与 KV 块边界对齐。该模式需要完整的检查点池，而非前述紧凑的按请求分配，用一部分 HBM 换取跨请求复用。当前缀真正被共享时，收益就会显现。

![](https://substack-post-media.s3.amazonaws.com/public/images/c0cd68d1-b16d-442d-87e4-ca98067ae979_2048x856.png)
*来源：SemiAnalysis*

## Paged Attention 中的 Lane 布局与流水线深度

两个硬件事实决定了 KV 缓存在 TPU 上的布局方式。下一节会更详细地讨论 TPU 硬件。第一，向量单元处理的 tile 其最后一维为 128 个 lane 宽，因此任何末维小于它的数组都会被填充。第二，Pallas 内核通过双缓冲来隐藏 HBM 延迟：在计算当前块的同时预取下一块。两个块都必须装进 VMEM，因此计算块的大小决定了预取能有多深。这两条约束此前都在损耗容量与吞吐。

在批量注意力内核中，KV 缓存沿头维度打包键和值，FP8 下打包因子是四。一个每设备只有单个 KV 头的模型只有两样东西可打包，因此每个 tile 有一半浪费在 padding 上。[sequence-on-lane 布局](https://github.com/vllm-project/tpu-inference/pull/3170)解决了这个问题：把页的 token 放在 128-lane 轴上，把头维度放到子 lane 轴上。可用的 KV 页翻倍（在报告的配置中从 5,141 增至 10,283），头维度只需是 32 的倍数而非 128，这让头维度为 64 的模型也能使用该内核。该布局在低并发下使单 token 延迟增加约 3%，但在 8k1k 并发 128 下，额外容量使吞吐提升 16.5%、中位 TTFT 缩短 95%，因为请求不再等待 KV 空间。

![](https://substack-post-media.s3.amazonaws.com/public/images/725b7e9e-8c46-4d02-880e-5a7de8886e87_2048x915.png)
*来源：SemiAnalysis*

RPA v3 的块大小启发式也有类似的盲区。在 v7x 解码期间，它把 KV 计算块设成与 KV 预取块相同，约 16k token，VMEM 几乎没有留给预取缓冲的空间。[将两种块大小分离](https://github.com/vllm-project/tpu-inference/pull/3102)后，KV 预取块保持 16k token，计算块降到 4k。这给流水线留出了跑到 MXU 前面的空间，解码吞吐从每秒 64.9k 提升到 96.3k token——在 Qwen3-0.6B 上四次运行均复现了这一 49% 的收益。吞吐在块大小扫描中呈干净的反 U 形曲线。调优参数表无法表达这一改进，因为它每个形状只存一个块大小，这就是该改动最初以环境变量覆盖形式落地的原因。后续跟进已把表格扩展为分别保存预取与计算两种大小。

![](https://substack-post-media.s3.amazonaws.com/public/images/72c0863c-a506-404a-8522-70bcadb3a89a_2048x756.png)
*来源：SemiAnalysis*

# TPU 系统级协同设计与网络解析

正如我们在 [TPU 之王那篇文章](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the)中所说，Google 在推理上的单 token 成本优势是协同设计（co-design）的结果。Google 不追求单芯片峰值性能，而是把计算裸片、芯片间互联和编译器放在一起设计，从而把计算与通信当作一个整体系统来优化。这种联合优化有助于解释 Ironwood 的每美元性能。接下来几节将审视芯片与网络如何协同工作。[Anthropic 是 TPU 的忠实拥趸，并在训练中大量使用。](https://semianalysis.com/accelerator-hbm-model/)

## Ironwood 芯片

TPUv7 Ironwood 打破了定义 TPU v4 与 TPU v5p 的「MegaCore」惯例——那种设计把两个物理核心融合成共享一个内存空间的单一逻辑加速器。Ironwood 则拥有两个独立的计算裸片，各自运行自己的独立逻辑设备。两片之间用高带宽裸片间链路连接，而非统一内存互联。JAX 及其他框架现在把它们暴露为每芯片两个不同的设备。每颗 Ironwood 芯片搭载 2 个 TensorCore 和 4 个第三代 SparseCore。SparseCore 加速嵌入查找等稀疏操作——这些操作若交给稠密矩阵引擎只会使其拥塞。

![](https://substack-post-media.s3.amazonaws.com/public/images/2690029e-8ec9-4b9e-b517-ec6d2950e8a2_1999x1130.png)
*来源：Google*

内存方面，每颗芯片的 HBM 容量约为 Trillium 的 6 倍，这一跃升直接决定了 KV 缓存的余量和 batch 大小。值得注意的是，Ironwood 是第一代拥有原生 FP8 硬件支持的 TPU，而此前各代都只能用软件模拟 FP8。

![](https://substack-post-media.s3.amazonaws.com/public/images/6e6e4785-cd71-4160-90b8-40bf02e1483e_1456x542.png)
*来源：SemiAnalysis*

关于 Ironwood 的更多内容，请阅读我们的 TPUv7 文章

## MXU 与形状为何重要

矩阵乘法单元（MXU）——真正执行乘法的引擎——是一个脉动阵列（systolic array）：由乘累加单元组成的二维网格。权重被载入阵列并保持不动；激活值从边缘流入，部分和逐格在网格中脉动传递、边传边累加。完成的结果从另一侧流出，中间过程完全不经过内存。从初代到 v5，每代 TPU 都使用 128x128 的 MXU，每周期可完成 16,384 次乘累加（MAC）。从 TPU v6e 起并延续到 Ironwood，阵列翻倍至 256x256，即每周期 65,536 次 MAC，每周期 FLOPs 达到上一代设计的 4 倍。

请阅读 [scaling book](https://jax-ml.github.io/scaling-book/tpus/)（又称「ML 系统圣经」），了解关于 TPU 与规模化扩展的一流权威信息。

问题在于：更大的脉动阵列只有在被「喂饱」时才是免费的。矩阵的两个维度都需要填充到至少 MXU 的边长——旧一代是 128，v6e 和 v7 是 256——XLA 编译器会尽职地把任何更小的轴填充到 tile 尺寸。每个填充单元在那个周期仍占着一个 MAC 单元，乘的是一个对结果毫无贡献的零。Llama 3 8B 以 128 的注意力头维度为例说明了这一点。在 Ironwood 的 256x256 MXU 上，该头维度恰好是阵列原生宽度的一半，使两个注意力矩阵乘法的 MXU 利用率上限为 50%（不是 75%，因为只有头维度是 128）。

这一影响的深远程度超出单个模型的注意力层。过去可以随意选择的架构超参数（如头维度、张量并行切分后剩余的 KV 头数、MoE 专家宽度）如今越来越需要考虑 TPU 的 tile 几何，因为形状失配是对实际交付吞吐的直接课税，软件栈其余部分再优秀也无济于事。内核作者同样需要显式考虑这一点。[ragged paged attention](https://arxiv.org/abs/2604.15464v1) 等生产级注意力内核会在 XLA 默认分块产生低效布局时，使用显式打包维度来减少 padding。

### TPU 很挑食

GPU 的矩阵核心消费的是小 tile，因此各种头维度、专家宽度和切分后的 KV 头数都能接近峰值性能。在 H100 或 B200 上，用 64 而不是 128 的维度几乎不付出代价，还能换来更便宜的注意力层。GPU 架构让研究者可以优先考虑评测性能而不损失推理性能。但对 TPU 来说，这个超参数变成了一种取舍。

如前所述，这些选择在 256 宽的脉动阵列上并非免费。按照把 Llama 3 8B 注意力矩阵乘限制在 50% 的同一套算术，64 的头维度在一行内核代码都没写之前就把上限压到 25%。gpt-oss 的头维度就是 64。DeepSeek 的 MLA 把查询/键维度拆成 128 加 64、共 192，对任何 2 的幂次阵列都显得笨拙，对宽阵列更是糟糕。

![](https://substack-post-media.s3.amazonaws.com/public/images/7e493590-cb03-43cf-851a-816a576d2083_1876x976.png)

由此带来的后果是：bring-up 成本差异巨大，且与模型的流行程度几乎不相关。形状规整的模型只需要调度、服务和调优工作，以周计。与 tile 几何打架的模型则需要新内核才能勉强打平，更不用说在每美元性能上取胜。内核工程师是有限的，因此把外部化的顺序优先安排在硬件不会一开始就落后一圈的模型上，是理性的做法——任何处在这个位置的加速器厂商，我们预计都会如此行事。

## 环面拓扑（Torus）

大规模推理与训练横跨数千颗芯片，它们需要持续互相通信。TPU 通过名为 ICI（Inter-Chip Interconnect）的定制网络进行 P2P 连接。ICI 完全绕过主机 CPU，让芯片直接交换激活值与梯度，而不必经 PCIe 和通用 NIC 中转。ICI 背后的拓扑逐代演进：TPU v2 和 v3 使用 2D 环面，每颗芯片连接 4 个邻居；从 TPU v4 和 v5p 起，Google 改用 3D 环面，每颗芯片沿 +/-X、+/-Y、+/-Z 三个轴连接 6 个邻居。Ironwood（TPUv7）沿用这一 3D 环面。基本构件是由 64 颗芯片构成的 4x4x4 立方体，其规模恰好对应一个物理服务器机柜。

![](https://substack-post-media.s3.amazonaws.com/public/images/f07dc2e7-090b-472a-a2bf-82c6fbb1cb67_1456x1956.png)
*来源：SemiAnalysis*

环面与普通网格的区别在于其回绕链路。把一条线的两端接起来形成环，最坏情况跳数就从 N 降到 N/2。这与让 Pac-Man 的迷宫显得比实际更小是同一个技巧。Google 更进一步采用「twisted torus（扭转环面）」，一种类似莫比乌斯带的回绕方式，把平均跳数压得更低。要扩展到单个 4x4x4 立方体之外，Google 用光路交换机（OCS）把多个立方体缝合起来，在更大的可重构拓扑中保留回绕特性，一路扩展到 Ironwood 完整的 9,216 芯片超级 pod 及其 42.5 FP8 exaflops 的聚合算力。OCS 在运维上的回报是：Google 可以在数秒内用反射镜物理改路，绕开失效链路或坏死芯片，而不必派技术员在运行中的数据中心里重新熔接铜缆。

![](https://substack-post-media.s3.amazonaws.com/public/images/fc7f1e6f-b854-4da5-b6c1-8f1bbdb49cb8_1456x1505.png)
*来源：SemiAnalysis*

这一横向扩展设计在当年是革命性的。在 NVL72 机柜出现之前，塞不进单个 8-GPU 节点的模型只能使用流水线并行，因为节点间的 InfiniBand 太慢。而在 TPU pod 上，ICI 环面向整个 pod（v5p 上多达 8,960 颗芯片）提供 NVLink 级别的带宽。有了这样的带宽，DSV3 规模的模型可以用张量并行、专家并行和数据并行（FSDP 式权重切分）分片到整个 pod 上，而无需按流水线阶段切分层。

尽管 TPU 环面比单跳 NVLink 交换设计的跳数更多，但我们即将发布的 CollectiveX/NetworkingX 结果显示，在很多情况下，TPU 环面对小型 EP 消息的延迟低于单跳 NVSwitch。

## 展望：TPUv8i 的 Boardfly 网络

Google 新发布的第八代 TPU 产品线有两颗专用芯片：面向训练的 TPU 8t 和面向推理的 TPU 8i。这是 Google 首次把训练和推理拆分为两个独立的架构设计，而不是发布一个兼顾两者的架构。TPU 8t 在纵向扩展上延续了 3D 环面血统，而 TPU 8i 用名为「Boardfly」的新拓扑取代了环面。这个名字致敬了超算领域长期使用的 Dragonfly 式高端口数（high-radix）网络设计。Boardfly 采用更扁平、分层的高 radix 交换机互联，而非最近邻 mesh。[Boardfly 拓扑会影响每颗芯片的网络接入资本开支。](https://semianalysis.com/ai-networking-model/)

回报是：与同等规模的 3D 环面相比，网络直径缩短超过 50%——在 1,024 至 1,152 芯片的可比规模上，从约 16 跳降到约 7 跳。跳数更少意味着集合通信的尾延迟显著降低；一旦你要跨 MoE 层路由 token，或运行每多一跳都会叠加成用户可感延迟的多轮智能体负载，这一点至关重要。TPU 8i 还以硬件支撑这一切：ICI 带宽达 19.2 Tb/s，是上一代的两倍；片上 SRAM 达 384 MB，是上一代的 3 倍，其容量专为把推理与智能体模型的 KV 缓存放到片上而设计，免去与 HBM 的往返。

![](https://substack-post-media.s3.amazonaws.com/public/images/83cff324-fa52-4b79-b901-80da6f9345a9_2000x1268.png)
*来源：Google*

不过，这些硬件余量本身不会自动兑现。要把更低直径的网络和更大的片上缓存转化为单 token 成本收益，软件栈仍需跟上。下一节将介绍实现路径的路线图，包括投机解码、prefill-decode 分离，以及在生产中充分发挥 TPUv8 所需的更广泛模型支持。

# 夯实 TPU 基础的下一步

这些预览结果为同一硬件上的持续优化确立了起点。我们预计随着 TPU 外部化推进，性能还会继续提升，但整个软件栈仍有大量工作要做。

## 启用并优化投机解码（MTP）

Google 团队需要聚焦的第一个领域是优化投机解码。一个廉价的小型起草模型（drafter）向前猜出若干 token，主模型用一次前向传播全部验证，不匹配的猜测直接丢弃。留下来的内容与模型自己生成完全一致。投机解码是无损的，质量零损失。

它奏效的原因在于：解码受带宽约束而非算力约束。要为单个用户产出一个 token，你要把整个模型的权重从 HBM 里流出来。这次权重读取是主导成本，而无论验证一个 token 还是五个，成本几乎不变。矩阵单元大多闲着，活全由内存系统干。投机解码正是拿这些闲置算力，把一次极其昂贵的权重读取摊销到多个 token 上——这就是 MTP、DSpark 这类一次起草多个 token 的方法既便宜又有效的原因。

![](https://substack-post-media.s3.amazonaws.com/public/images/9126a39f-54f9-4df1-bd09-4d0d64deaf17_2048x559.png)
*来源：vLLM*

## Prefill-Decode 分离与 KV 缓存卸载

Prefill-decode（PD）分离是 TPU 团队正在外部化的另一项优化。它把 prefill 和 decode 拆到不同的 TPU 池上，让每个池可以独立调优、独立扩缩以匹配负载。

![](https://substack-post-media.s3.amazonaws.com/public/images/282af9ce-a0c4-4c7b-8053-00026f16f945_1112x548.png)
*来源：DistServe*

Google 内部为 Gemini 服务运行 PD 分离已有很长时间，但外部化的工作几个月前才开始。相关工作包括 llm-d 中的 TPU 支持以及 TPU-Sync（前称 TPU-raiden）的开源——这是 Google 的分离式 KV 缓存传输库。TPU-Sync 原生支持 JAX 和原生 TorchTPU 栈，并可通过提取原生 PJRTBuffer 硬件描述符执行零拷贝传输。有了分离式 PD，我们相信 TPUv7 能够成为 GB200/GB300 的强劲对手，甚至在每美元性能上击败它们。

[TPU-Sync 还支持原生 TPU KV 缓存 DRAM 卸载](https://github.com/google/tpu-sync)——在大模型和中大 batch 场景下，HBM 已装不下所有用户的 KV 缓存，这一能力必不可少。很高兴看到 Google 也把它的 DRAM 卸载优化开放给了公众。

![](https://substack-post-media.s3.amazonaws.com/public/images/62a1acf1-77d0-4c16-85da-9a046d56f2f8_1974x1342.png)
*来源：GitHub*

Google 正在把原生 TPU 卸载栈外部化，并[支持业界标准的 Mooncake Store 卸载库](https://github.com/kvcache-ai/Mooncake/issues/2662)及 Mooncake Store 的 DRAM P2P 池化能力。我们相信 Mooncake Store 支持将基于 tpu-sync 中的原语实现。

![](https://substack-post-media.s3.amazonaws.com/public/images/ec6b5d7e-af79-484b-bcf7-ebc50d36c3e3_2048x1204.png)
*来源：GitHub*

有了 P2P 池化，每台 TPU 主机上的 KV 缓存存储被聚合为单一逻辑内存池，任何一台服务器上的 TPU 都能访问其他服务器的 KV 缓存。这把多个节点各自的内存贡献统一成了一个共享逻辑池。

![](https://substack-post-media.s3.amazonaws.com/public/images/f51b3df9-ffa4-408f-b617-1eb3dde40740_2039x975.png)
*来源：Mooncake*

此外，Mooncake Store 在支持 WEKA/Vast 等传统分布式文件系统后端的同时，[还能把多台服务器的 NVMe 存储汇聚成单一逻辑池](https://kvcache.ai/blog/scaling-kv-cache-beyond-memory/)。

## AgentX TPU

KV 缓存卸载对长上下文、多轮智能体负载尤其重要，优化的 KV 缓存存储可以实现很高的 KV 缓存命中率。

从高层次看，智能体负载有四个特征：

1. 多轮：一个会话包含数十甚至数百次用户与助手的交互，而聊天机器人场景只有寥寥几次。这类负载把长上下文、高 prefill 复用，与子智能体突发和大量工具调用结合在一起。
2. 长上下文：系统提示、工具定义和大量轮次使上下文迅速累积。
3. 高前缀复用：由于对话线性推进——第 n-1 轮的输出（通常）被拼接到第 n 轮——大部分上下文可以从 KV 缓存直接服务而无需重算（这取决于可用于存放 KV 张体的存储量）。随着 n 增大，缓存输入相对非缓存输入的比例通常趋于 1。
4. 子智能体突发：一个会话会启动多个携带全新上下文、生命周期很短的子智能体，造成 KV 缓存的突发式模式。

[我们听说许多 Google TPU 客户已经在询问 AgentX 性能结果，我们很高兴宣布：我们也正在把 TPU 带上 AgentX！](https://newsletter.semianalysis.com/p/agentx-inferencexv3-does-cuda-moat)

![](https://substack-post-media.s3.amazonaws.com/public/images/9ca94316-e44c-4bec-9d0a-041ad73df31e_2048x909.png)
*来源：DeepSeek、SemiAnalysis*

Ironwood 没有原生 FP4，因此眼下公平的同口径对比对象是 FP8 Blackwell：FP8 对 FP8 没有质量损失，而 FP4 对 FP8 会在 FP4 一侧引入质量差异。Google 的 TPUv8i 确实有原生 FP4 加速，所以当我们在 InferenceX/AgentX 上完成 TPUv8i 的 bring-up 后，将进行 FP4 对 FP4 的比较。

我们强烈认为，在原生 TorchTPU 这个稳定基础之上构建原生 vLLM 与 SGLang 支持，是 TPU 外部化的正确方向。TorchTPU 意在取代之前的 TorchAX 栈，后者很快将被弃用。Google 接下来将让 Kimi K3 和 GLM5.3 在单轮和/或 AgentX 这类智能体负载上跑起来，同时还有 Google 自家的开源权重模型如 Gemma4。一旦少数几个模型在 TorchTPU 栈上运行起来，新增模型将变得容易得多，TPU 支持也将更贴近 day 0 落地。

罗马不是在 day 0 建成的，所以我们不应指望 TPU 外部化一蹴而就。但我们强烈相信，这一切正以极快的速度发生。

# TPU 高性价比的总拥有成本

我们对 TPUv7 的完整 BOM 与 TCO 估算收录于 [SemiAnalysis AI TCO 模型](https://semianalysis.com/ai-cloud-tco-model/)。结构概览如下。
