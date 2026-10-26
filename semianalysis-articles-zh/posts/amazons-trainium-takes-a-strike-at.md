---
title: "亚马逊 Trainium 向训练之王发起冲击"
title_en: "Amazon’s Trainium Takes a Strike at the Training King"
subtitle: "Trainium 最适合推理？但如今训练同样出色、原生 Trainium PyTorch、高质量 CI、TorchTitan、GPU 做不到的分析器"
date: 2026-10-23
source: https://newsletter.semianalysis.com/p/amazons-trainium-takes-a-strike-at
crawled: 2026-10-26
authors: ["Kimbo Chen", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-10-26
---

# 亚马逊 Trainium 向训练之王发起冲击

> 原文：[Amazon’s Trainium Takes a Strike at the Training King](https://newsletter.semianalysis.com/p/amazons-trainium-takes-a-strike-at) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Trainium 最适合推理？但如今训练同样出色、原生 Trainium PyTorch、高质量 CI、TorchTitan、GPU 做不到的分析器**

Trainium 已经在推理领域证明了自己。Anthropic 正在 Trainium2 和 Trainium3 上运行生产推理与 RL rollout。从历史上看，Trainium 一直很适合推理，却不是研究训练的最佳选择：推理场景下，模型架构的变化速度比训练慢得多；而在训练中，研究人员要对模型架构做大量不同的实验与消融（ablation），需要一个覆盖广泛 API 面的软件栈。过去，这正是 Trainium 的短板所在。

AWS Neuron 团队正在大力弥补这一短板，其中最大的转变，是走向一等公民级的原生 PyTorch 训练体验。在训练循环里到处撒 `xm.step()`、与定制的 XLA 风格执行模型搏斗的日子已经一去不复返。如今 Trainium 以 PyTorch 用户期望的方式运行 PyTorch：eager 模式、torch.compile 以及标准 API。

过去几周，SemiAnalysis 工程团队一直在试用 Trainium3 机柜，体验非常好——我们欣赏它整体的前进方向。需要说明的是，它还不算完美，我们自己就踩到过几个 bug。它离 CUDA 生态的成熟度还差得很远，但方向是对的。在智能体编程（agentic coding）的助力下，他们的团队进展迅速。

此外，与其他加速器公司不同——在那里我们不得不拼尽全力，才能为他们自己的工程师争取到一支还算稳定的 CI 机器队伍——Trainium 则将多达 80,000 个物理核心投入自动化质量控制。

本文将带大家回顾我们在 Trainium3 的 TorchTitan 与 TorchNeuron 软件栈上的使用体验，以及 Trainium 的 Neuron Explorer 性能分析器的使用感受——它比 Nvidia 和 AMD 的分析器都要好得多。我们制作了一批演示，展示 Trainium 的分析器何以「GPU 做不到」。

![](https://substack-post-media.s3.amazonaws.com/public/images/680cf6ed-4bdd-4d53-9c2c-569ac56bb93c_1452x790.png)
*在 Trainium 性能分析器中可视化 AWS 副总裁 Nafea Bshara，展示 Trainium 的细粒度分析器。来源：SemiAnalysis*

**在即将发布的下一篇文章中，我们将深入探讨如何在 Trainium3 上编写光速级 NKI 内核并进行微基准测试。**想深入了解 Trainium 硬件，请参阅我们此前那篇对它做完整硬件拆解的文章。

![](https://substack-post-media.s3.amazonaws.com/public/images/66643b53-8390-4e90-a3a2-e4d46fe6bf6f_1426x1367.png)
*来源：SemiAnalysis*

# 我们正在招聘

SemiAnalysis 正在招聘多个技术团队成员（Member of Technical Staff）职位。如果你觉得这类分析有意思，欢迎投递：

[点击此处投递](https://app.dover.com/apply/SemiAnalysis/2a9c8da5-6d59-4ac8-8302-3877345dbce1?rs=55634680)

我们在寻找：

- **高动机、高水准的技术团队成员，加入我们不断壮大的工程团队。**
- **技术团队成员将在推理基准测试与系统建模的开发中扮演关键角色**
- **你也将参与撰写和准备我们的 newsletter 文章并推动其发表，还有机会以直接作者身份获得署名认可。**
- **我们招聘各经验层级的独立贡献者（IC）。薪酬具有竞争力**
- **作为面试流程的一部分，你需要完成一个付费编程挑战，其设计贴近 SemiAnalysis 的日常工作**
- **薪酬具有竞争力，视经验、技能、所在地与业务需求而定**

**任职要求**

- **主动积极、自我驱动，能在全球化团队中独立工作。**
- **通过工作经历、个人项目或个人 Substack 博客，展现出 PyTorch 或 JAX 等 ML 框架的实战经验**
- **扎实掌握以下至少一项：transformer 架构、LLM 并行策略，和/或 CUDA 并行编程**
- **研究能力强，能够从多源信息中综合提炼洞见。**
- **要求英语流利，会中文者优先**

# 迈向一等公民的 PyTorch 体验

亚马逊对其软件战略做出了一次重大路线修正，我们相信这将显著拓宽 Trainium3 的采用面。TorchNeuron 代表的是一种原生 PyTorch 体验，而不是像以往那样通过 PyTorch/XLA 项目把 Trainium 用胶带捆到 PyTorch 上。新的后端面向所有前沿实验室内核工程师之外的广大用户。AWS 甚至挖来了 Google 原生 Torch-on-TPU 工作的负责人，请他为 Trainium 开发原生 Torch。此人从该项目在 Google 启动之初就是 TPU 软件负责人，涵盖 XLA、xprof、Cloud TPU 等。

旧方案让所有从 CUDA 转过来的用户都觉得 Trainium 处处陌生。PyTorch/XLA 依赖惰性张量图捕获，没有一等公民的 eager 模式；也不支持 PyTorch 的原生分布式 API（torch.distributed.*）和原生并行 API（DTensor、SimpleFSDP、DDP），用户只能依赖 torch_xla.experimental.spmd_fsdp、torch_xla.distributed.spmd 这类树外的 XLA SPMD API。对习惯了 CUDA 上原生 PyTorch 的研究人员来说，切换到 Trainium 意味着要重新学习怎么写训练循环。

![](https://substack-post-media.s3.amazonaws.com/public/images/eb846e38-260b-4211-9146-390bebf520bc_1446x1012.png)
*来源：AWS*

要在 GPU 研究代码库里到处插入 XLA 标记来完成移植，这种痛苦足以让任何一个用过 PyTorch/XLA 的人望而却步。

![](https://substack-post-media.s3.amazonaws.com/public/images/73ccd20a-b8b7-435f-8802-4960c36062d9_1126x668.png)
*来源：AWS*

从高层看，唯一需要的改动就是把 `.to("cuda")` 换成 `.to("neuron")`，理论上绝大多数 PyTorch ATen 算子都能开箱即用、表现尚可。

![](https://substack-post-media.s3.amazonaws.com/public/images/85a8b8ec-1992-4b58-bb84-dc655d291eaf_526x329.png)
*来源：AWS*

理论上，借助 PyTorch 的 torch.accelerator 硬件无关 API，像 bf16 autocast 这样的代码甚至无需改动——不过 PyTorch 中仍有一些 API，以及一些研究代码库，尚未迁移到 torch.accelerator 命名空间，仍在直接调用 torch.cuda.* 命名空间。

由于机器人、生物科技、世界模型与自动驾驶领域的学术界和研究人员大多使用 BF16，Trainium Torch 在 Day 0 不会支持 TorchAO MXFP8——要等他们先把 BF16 训练体验打磨到位。我们对这个先后顺序并无异议，因为做 MXFP8 训练的大多是大型 Tier 1 实验室，他们有足够的内核工程师为大型训练任务编写自定义内核。

# Trainium Torch 生态

PyTorch 之所以流行，不仅因为 PyTorch 本体，也因为它的整个库生态，包括 Hugging Face Transformers、PEFT、diffusers、TRL、Accelerate、TorchTitan 等。让我们惊讶的是，Trainium Torch 已经支持了生态中大量这类库——其中就包括间接封装层多得离谱的 Hugging Face Accelerate。Trainium 还支持 TorchTitan，它是最流行、代码最干净的开源训练代码库之一，许多 Tier 2 实验室都 fork 它作为内部训练代码库的地基。Trainium 全新的 PyTorch 体验对它也提供了完整支持。

我们已经看到 Google 如何成功与 Inferact/RadixArk 合作，把 TPU 带进 vLLM/SGLang 生态，还拿下 Meta 成为其生产环境 TPU 客户。而且，随着 TPU 进入 vLLM/SGLang 生态，[TPU 已经自动获得 Muse Spark Open 的 Day 0 支持](https://www.lmsys.org/blog/2026-10-15-meta-muse-spark-open#multi-platform-support)，并拿到了热门后续模型的 TPU Day 0 支持承诺。

诚然，智能体编程的兴起让引擎代码本身的重要性下降了，但 vLLM/SGLang 带来的是生态。无论哪个开源模型发布，全球 ML 社区在 Day 0 都会把 vLLM/SGLang 当作推理的默认之选。没有任何一个 vibe coding 出来的引擎有这种覆盖面。

[我们已经开始看到 Trainium 快速向 vLLM/SGLang 社区投入资源：提供硬件访问，以及基于原生 PyTorch（TorchNeuron）构建的 Trainium 版 SGLang 早期访问，思路与 TorchTPU 如出一辙。](https://x.com/sgl_project/status/2113299489394205121)

![](https://substack-post-media.s3.amazonaws.com/public/images/23423dd8-6352-4943-af4d-c303ca5ad2af_1492x1384.png)
*来源：SemiAnalysis*

# TorchTitan 使用体验

TorchTitan 是最流行的开源预训练框架之一，我们测试了 Neuron 对它的支持，以此衡量研究人员用 Trainium 训练一个不算平凡的模型时的用户体验。具体而言，我们在 16 颗 Trainium2 芯片（共 64 个 LNC=2 逻辑核心）上训练了 Qwen3-32B，也在拥有 64 颗物理芯片的机柜级 Trainium3 UltraServer 上做了同样的尝试。

总体而言，我们对用户体验是满意的，虽然有一些粗糙之处，不过亚马逊团队已经把它们列入了修复路线图。

为完整起见，我们会在下文给出 Trainium2 的 MFU，但真正要关注的是：对 ML 研究消融实验而言，最重要的不是一条优化到光速的软件栈，而是足够好的性能和对各类模型架构改动的广泛支持，让研究人员不必与软件栈搏斗就能迭代。

使用 Neuron 官方的 TorchTitan 镜像，我们顺利启动了训练，没有遇到任何问题。实测 **eager 模式下平均训练吞吐为每秒 11,099 个 token，MFU 为 23.89%**；编译模式下则为 **每秒 14,156 个 token、MFU 30.47%，吞吐较 eager 模式提升 1.28 倍**。我们还试着在建模代码里稍微改动模型架构，同样运行良好。

Neuron 还为更现代的模型架构提供了训练配方，我们测试了它的 gpt-oss 20B 训练配方。Neuron 通过与 [GraphTrainer](https://github.com/pytorch/torchtitan/blob/main/torchtitan/experiments/graph_trainer/README.md)——TorchTitan 的实验性训练器模块——集成来支持 gpt-oss 训练：具体包括添加 Trainium 兼容的 SimpleFSDP 配置、一个用于 PyTorch 计算图捕获的编译后端，以及面向注意力与 MoE 运算的自定义 NKI 内核。就用户体验而言，这套配方开箱即用，一切顺利。

尚未用上游 API 实现的一点是 TokenSwitch。在 MoE 时代，无论推理还是训练，MoE combine 与 MoE dispatch 都是最重要的通信算子之一，占通信量的 60-70%，而 TokenSwitch 正是 PyTorch 为它们提供的一等 API。Trainium 暂不支持它，而是依赖一个名为 NeuronEPTokenDispatcher 的自定义 TorchTitan 类。把它迁移到 TokenSwitch API 上看起来是个简单的修复，AWS 团队也已承诺与 Meta PyTorch 团队合作修改 TokenSwitch ABC（抽象基类），让它同样能支持 Trainium。

略微令人失望的地方在于 Neuron 编译器编译耗时很长，导致第一步之前要等很久。具体来说，eager 模式下第一步耗时 184.6 秒（编译模式为 255.7 秒），是（不含第一步的）平均步时长的 30-55 倍。gpt-oss 那次训练的编译时间更是离谱地高达 27 分 17 秒，用户体验相当糟糕——对尝试新模型架构的研究人员尤其如此。原因在于，Trainium 编译器栈历史上主要面向推理：推理场景编译时间无关紧要，因为编译是离线完成的、每个镜像缓存一次，不影响生产推理；训练则不然。就当时的推理而言这是正确的取舍，但对迭代模型架构的研究人员来说，这就是一个实实在在的摩擦点。

Neuron 团队已经在直接着手解决这个问题。即将发布的 TorchNeuron 版本将引入一个带大量预编译 NKI 内核的新编译器后端，并为快速编译重新架构了编译栈，目标是把 eager 与编译两种模式下的首步耗时（time-to-first-step）最多降低两个数量级，且性能几乎无回退。如果真能兑现，编译时间就再也不是个话题了。

# 训练 MatMul 性能

对实验性训练来说，最重要的事情之一是：当 ML 研究人员尝试各种花样时，能在一大片形状（shape）范围内都拿到像样的性能。我们用 PyTorch 的 nn.functional.linear API 对单个 Trainium3 逻辑核心（LNC=2）做了基准测试，考察其矩阵乘法性能，并与 GB300、B200 做了参照对比。我们遍历了主要开放权重模型中投影运算的矩阵形状，并把 M 维度设为 1、128 和 2048，分别代表不同的 batch size 场景。

![](https://substack-post-media.s3.amazonaws.com/public/images/5b02cad9-f642-4bae-be70-4b2141f6a983_1980x1260.png)
*来源：SemiAnalysis*

在我们的基准测试中，从矩阵乘法计算量达到 1 GFLOP 的中段开始，Trainium3 的 MFU 就明显高于 GB300。直到 100 GFLOP 之后，GB300 和 B200 才开始反超 Trainium3，而到 1 TFLOP 之后，Trainium3 又重新领先。

# FlexAttention API

FlexAttention 是一个高层 API，让你能用 PyTorch 实现各种注意力变体，同时自动生成反向传播并保持合理的性能。FlexAttention 支持得好不好，直接体现了一块硬件对研究人员的灵活性和易用性。我们在 Trainium3 上运行了 [FlexAttention 基准测试套件](https://github.com/meta-pytorch/attention-gym/blob/main/benchmarks/flex_perf.py)，检验它的 FlexAttention 支持情况。

![](https://substack-post-media.s3.amazonaws.com/public/images/d03ecc2c-c3cf-4424-a366-5a9d2bd037a6_1600x680.png)
*来源：SemiAnalysis*

总体来看，Trainium3 通过了 96 个测试用例中的 89 个，通过率 93%。全部 7 个失败用例都出现在大 batch size（4）和大序列长度（8192）下，且**全部是因为编译超出时间预算，而非数值错误**。这些问题会在后续版本的 TorchNeuron 中修复。

此外，我们还尝试在 Trainium3 上实现了几个 FlexAttention 基准套件之外的自定义注意力变体，数值结果与 Nvidia GPU 完全一致。

![](https://substack-post-media.s3.amazonaws.com/public/images/a8cb4895-1a44-461d-838a-f13de37d3a8e_1600x680.png)
*来源：SemiAnalysis*

# 自动化质量保障

在全球 ML 社区，SemiAnalysis 素有「CI Karen」（较真监工）之名：我们对所有硬件厂商一视同仁地设定高标准，并不遗余力地推动 AI 芯片公司的高管层真正为工程师提供足够的资源和 CI 机器队伍，以维持自动化质量控制的高标准。

![](https://substack-post-media.s3.amazonaws.com/public/images/2ece87e1-1fd3-4bae-bd17-9fe9e28190e1_1040x598.png)
*来源：SemiAnalysis*

最近的一项成果，是在与 AMD 高管层缠斗了 9 个多月之后，为他们自己的工程师争取到足够多的稳定节点，使门控（gating）测试组的对齐率达到 93%。

![](https://substack-post-media.s3.amazonaws.com/public/images/78c1bfee-bc21-46e5-bb7f-1abfe8ac31fe_2048x1065.png)
*来源：vLLM Dashboard*

推理是个窄问题。一个只服务少数几个生产模型的实验室，需要的是前向传播、基本固定的架构，以及一小撮热点内核。

训练则是个普适性问题。数千个算子中的每一个都需要反向传播，研究代码库有时还会不小心以更高精度运行某些算子，这些也必须被支持。为确保 Trainium 能覆盖广泛的模型架构、并把 eager 模式与编译模式都做好，AWS 收集了一份庞大的清单——Hugging Face 上热度最高的 10 万多个模型，覆盖各种不同的归一化、MLP、MoE 布局与注意力类型。他们不仅测试程序不崩溃，还测试性能、哪些算子仍在走 CPU fallback 而没有原生支持、图中断（graph break）出现在哪里；最重要的是，他们用 CPU 与 Nvidia 基线检验数值正确性，并测试张量级对齐和损失曲线发散情况。10 分钟内做完一场考试很容易，但考了 0 分的话，做得再快也毫无意义。训练软件栈同理：拿到像样的 MFU% 很容易，难的是在不引入数值问题的前提下拿到像样的 MFU%。

![](https://substack-post-media.s3.amazonaws.com/public/images/db0a6c55-273d-4f78-9819-694f30224206_717x649.png)
*来源：AWS*

虽然通过率尚未达到 100%，但重要的是轨迹。AWS 正在快速爬升，靠 agent 集群系统性地修复剩余的失败项。我们认为 AWS 内部汇总表——也就是高管层看到的那张——透明呈现缺口而不是把它们藏起来，这本身就是一种优势。

这话是我们凭经验说的。当 SemiAnalysis 和上游维护者试图推动其他硬件厂商改进质量控制文化时，我们发现高管层看到真实的对齐通过率时是真的震惊。有一家厂商尤其严重：中层的层层过滤，等 CI 数据传到高管层时已经显示 99.99%，而当时实际的门控对齐通过率低于 5%。

# Neuron Explorer——优于 Nvidia 与 AMD 的性能分析器

Trainium 的性能分析器目前遥遥领先于业界，是 SOTA 水准。这里分享我们的初步印象，完整的使用体验将留到未来的 Trainium 内核文章中再讲。

Trainium 的性能分析器深受 Anthropic 全体性能工程师喜爱。Anthropic 的性能负责人（曾任职于 Jane and Finch Street）公开表示，Trainium 上的性能分析远好于 Nvidia GPU（显然也远好于 AMD GPU）。

![](https://substack-post-media.s3.amazonaws.com/public/images/ea535417-4c21-49ed-b9f9-c3c80eb222af_2048x822.png)
*来源：Tristan Hume（Twitter）*

我们同意 Tristan Hume 的看法。以我们的经验，跨过最初那道坎——性能分析配置稍微有点令人困惑（但并非无解）——之后，整个分析体验非常出色。要设置的环境变量很多，要保存的文件类型不一，采集和查看 profile trace 的命令也五花八门。这还只是内核性能分析的配置，PyTorch 性能分析的配置与之相似但又有细微差别，更让人犯迷糊。在 Codex 的帮助下（[因为 Claude 拒绝写 Trainium 内核](https://x.com/jakehalloran1/status/2102480535369208157)），我们最终可用的配置流程如下：

- 启动一个常驻的 Neuron Explorer 服务器
- 用 neuron-explorer capture 命令对内核做性能分析
- 以 Web 请求的方式，把采集到的 trace 作为 artifact 上传到 Neuron Explorer 服务器

我们已向 AWS 反馈：希望文档能更清楚地说明工作流——解释哪些环境变量因何而设、每种文件类型各有什么用途。

配置完成之后，分析器的用户体验非常好。Neuron Explorer 是与硬件协同设计的。我们尤其喜欢它的时间线视图：不同硬件单元分行显示，气泡（bubble）一眼可见。相比之下，GPU 程序员要做 SM 内部的性能分析，只能自己动手搭——官方 Nsight 工具并不支持。

![](https://substack-post-media.s3.amazonaws.com/public/images/2b780b6a-3587-41be-ac01-c268c4624261_1001x609.png)
*来源：SemiAnalysis*

我们也喜欢这个查看器对依赖关系的可视化。选中某个块后，它依赖的块和依赖它的块会以不同颜色高亮，这有助于我们推理工作之间的重叠情况，例如计算是否与内存加载充分重叠。下图显示，选中的白色块：

- 流依赖（flow-dependent）于红色块
- 顺序依赖（order-dependent）于橙色块
- 是蓝色块的流依赖
- 是紫色块的输出依赖

![](https://substackcdn.com/image/fetch/$s_!lX4e!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9c749837-cde0-4015-8def-23186b72fc97_647x166.png)
*Neuron Explorer 依赖关系可视化。来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/d333f32c-4e37-489c-8281-b741310499d3_2048x924.png)
*Neuron Explorer 代码编辑器映射。来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/c19ace2d-f4ea-4fa5-8dcb-14dc63db54cf_1172x486.png)
*Neuron Explorer：悬停在事件上时显示的事件信息。来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/178ccf7f-c5f1-4763-8cea-921827276215_656x538.png)
*Neuron Explorer 内存 bank 利用率可视化。来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/a75e0579-f42c-49ba-96f5-336140a1fa4e_604x292.png)
*Neuron Explorer 微秒级内存吞吐可视化。来源：SemiAnalysis*

## Trainium 性能分析器演示——像素画

Neuron Explorer 还有很多功能：代码编辑器映射、MFU 估算、内存占用，甚至由于分析器精度极高还能拿来做像素画。下面的图片全部来自在真实 Trainium 硬件上运行产生的分析 trace，不是伪造的 profile 报告。我们主要受 Daniel Liu（Anthropic 性能工程师）那篇 Bad Apple 帖子启发，自研了一个用于生成图像的智能体编程 [SKILL.md](http://skill.md)。逐帧自动生成视频的版本还没来得及做，但未来会做出来，并把这个 [SKILL.md](http://skill.md) 开源给大家使用。这些像素画主要是这样生成的：利用每个物理核心上的 16 个 DMA 引擎，通过激活 DMA 引擎来给区域「上色」，阴影区域的宽度则由我们让每个 DMA 引擎搬运多少数据决定。

![](https://substack-post-media.s3.amazonaws.com/public/images/c62b77ad-11c6-4250-96d4-7e269fb46dff_2048x886.png)
*Neuron Explorer 上的 Bad Apple。来源：Daniel Liu*
![](https://substack-post-media.s3.amazonaws.com/public/images/c99913b4-6db5-45df-b4e8-4e1db122f915_2048x929.png)
*SemiAnalysis 标志可视化。来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/7d1da3ef-a722-4275-9249-897009a7470a_1258x802.png)
*Jeff Bezos 可视化（还没开始 looksmaxxing）。来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/5811851d-661c-400e-85cf-ce78ca4f93aa_2064x1118.png)
*Dylan Patel 可视化（还没开始 looksmaxxing）。来源：SemiAnalysis*

既然 AWS 是 Nvidia 的合作伙伴，Jensen 应该让他的工程师去和 AWS Trainium 团队约个会，请教做精确细粒度性能分析所需的硬件特性，好让 Nvidia 学会如何把这种能力加进 Feynman 或 Feynman-Next GPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/45749adc-f952-40a7-a175-f4a5cd3e21d0_2048x1193.png)
*Jensen 在 Trainium3 上的可视化。来源：SemiAnalysis*

Nvidia 的内核内性能分析器 Nsight Compute 采用的是另一种设计：它提供聚合指标和性能属性的详细信息，而不是基于事件的查看器。我们能找到的最接近的东西是 Tri Dao 的 QuACK 内核内性能分析器，它使用了 [Nvidia 的内核内事件追踪（In-Kernel Event Tracing）API](https://docs.nvidia.com/cutlass/latest/media/docs/pythonDSL/guides/iket_profiling.html)。QuACK 需要专门设计才能让 Perfetto 做出相应的可视化，而 AWS 把这类体验在 Neuron Explorer 中做成了一等公民的、集成完善的功能，令人欣喜。

![](https://substack-post-media.s3.amazonaws.com/public/images/922100d3-ea70-4104-99e9-f2e6e069e6e1_2048x795.png)
*QuACK 的内核内性能分析器：QuACK GEMM 内核的可视化。来源：QuACK*
![](https://substack-post-media.s3.amazonaws.com/public/images/f3cbed7a-998a-454c-a7ad-485c0e8bb312_2048x1280.png)
*Nsight Compute 视图：FlashAttention 4 工作负载分析。来源：Nvidia Nsight*
