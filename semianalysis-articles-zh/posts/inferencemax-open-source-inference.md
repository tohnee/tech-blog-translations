---
title: "InferenceMAX™：开源推理基准测试"
title_en: "InferenceMAX™: Open Source Inference Benchmarking"
subtitle: "NVIDIA GB200 NVL72、AMD MI355X、单 GPU 吞吐 token 数、延迟（每用户 tok/s）、每美元性能、每百万 token 成本、每已部署兆瓦 token 数、DeepSeek R1 670B、GPTOSS 120B、Llama3 70B"
date: 2025-10-09
source: https://newsletter.semianalysis.com/p/inferencemax-open-source-inference
crawled: 2026-09-15
authors: ["Kimbo Chen", "Dylan Patel", "Daniel Nishball", "Cam Quilici", "Cheang Kang Wen"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# InferenceMAX™：开源推理基准测试

> 原文：[InferenceMAX™: Open Source Inference Benchmarking](https://newsletter.semianalysis.com/p/inferencemax-open-source-inference) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**NVIDIA GB200 NVL72、AMD MI355X、单 GPU 吞吐 token 数、延迟（每用户 tok/s）、每美元性能、每百万 token 成本、每已部署兆瓦 token 数、DeepSeek R1 670B、GPTOSS 120B、Llama3 70B**

LLM 推理性能由两大支柱驱动：硬件与软件。硬件创新通过每年发布新的 GPU/XPU 和新系统带来性能的阶梯式跃升，而软件每天都在演进，在这些阶梯式跃升之上持续交付性能增长。

SGLang、vLLM、TensorRT-LLM、CUDA、ROCm 等 AI 软件通过内核级优化、分布式推理策略与调度创新实现性能的持续提升，把性能的帕累托前沿（Pareto frontier）不断向外推——而这些增量版本之间的间隔可能只有短短几天。

软件进步的这种速度带来了一个难题：在固定时间点做的基准测试很快就会过时，无法代表最新软件包所能达到的性能。

InferenceMAX™ 是一个[开源自动化基准测试](https://github.com/InferenceMAX/InferenceMAX)，其设计目标就是以与软件生态系统本身同样快的速度迭代，正是为解决这一难题而生。

![](https://substack-post-media.s3.amazonaws.com/public/images/4be54ad9-692e-4500-948c-38beb5018814_1734x922.png)
*来源：SemiAnalysis InferenceMAX™ GitHub 仓库*

InferenceMAX™ 每晚在数百颗芯片上运行我们的基准测试套件，不断重新测试全球最流行的开源推理框架和模型，以实时追踪真实性能。随着这些软件栈的改进，InferenceMAX™ 以近乎实时的方式捕捉这些进步，为推理性能进展提供了一个鲜活的指标。免费公开的实时仪表盘可在 <https://inferencemax.ai/> 查看。

![](https://substack-post-media.s3.amazonaws.com/public/images/fbf9bb59-ada3-44b0-8cba-c6ee11097b3f_1839x1344.png)
*来源：SemiAnalysis*

AMD 和 NVIDIA 的 GPU 都能在不同类别的工作负载上交付有竞争力的性能，某些类型的工作负载 AMD 表现最佳，另一些则 NVIDIA 更胜一筹。事实上，两个生态都在快速进步！

分析 InferenceMAX™ 的结果时有许多细节和考量，这在很大程度上是因为它被设计为一个中立基准，不会为了吹捧某家特定厂商或方案而挑拣数据。因此，确实存在某些模型和交互性（tok/s/用户）水平下，AMD 当前优于同代 NVIDIA GPU 的情况；也存在另一些交互性水平下 NVIDIA 当前做得更好。InferenceMAX™ 的目标简单而有雄心——提供既尽可能贴近真实世界应用、又反映软件创新持续节奏的基准测试。

在 InferenceMAX™ v1 首发版本中，我们对 GB200 NVL72、B200、MI355X、H200、MI325X、H100 和 MI300X 进行基准测试。未来两个月内，我们将把 InferenceMAX™ 扩展到 Google TPU 和 AWS Trainium 后端，使其成为首个横跨 AMD、NVIDIA 与自研加速器的真正多厂商开放基准。

InferenceMAX™ v1 远非完美，但我们相信它是朝正确方向迈出的良好第一步。未来版本中还有空间去打磨工作负载、扩展模型覆盖面，并更好地反映真实世界负载。

## 致谢

感谢 Lisa Su 和 Anush Elangovan 为这个免费开源项目提供 MI355X 和 CDNA3 GPU。我们要感谢 Anush、Quentin Colombet 以及数十位 AMD 的贡献者，他们响应迅速，帮助我们跨 AMD GPU 调试、优化和验证性能。每当我们遇到 ROCm 的问题（我们注意到，这类问题出现的频率已远低于 2024 年底！），他们都会立刻介入帮助找到临时解决方案让我们继续推进，随后再向 ROCm 合入永久补丁以确保长期稳定性。Quentin 和他的团队正是 [AMD 2.0 式紧迫感](https://semianalysis.com/2025/04/23/amd-2-0-new-sense-of-urgency-mi450x-chance-to-beat-nvidia-nvidias-new-moat/)的体现，[xAI 等许多客户对此非常认可](https://www.youtube.com/live/5dmFa9iXPWI?si=5HHNsDd7bw3lDASk&t=1073)。

我们同样感谢 Jensen Huang 和 Ian Buck 对这一开源努力的支持，他们（通过 OCI）提供了 GB200 NVL72 机柜和 B200 GPU 的使用权限。感谢 Kedar Pandurang Potdar、Sridhar Ramaswamy、Kyle Kranen、ptrblck、NVIDIA 推理团队、NVIDIA Dynamo 团队、NCCL 团队以及 NVIDIA 固件/驱动团队，他们帮助验证和优化 Blackwell 与 Hopper 配置，并以极快的响应速度修复 bug。

我们还要向 SGLang、vLLM 和 TensorRT-LLM 的维护者们致敬，他们打造了世界级的软件栈并将其开源给全世界。此外，感谢 Simon Mo、Kaichao You、Michael Goin 和 Robert Shaw，他们的帮助对于解决几个关键的 Blackwell bug 至关重要。

最后，感谢 Crusoe、CoreWeave、Nebius、TensorWave、Oracle 和 TogetherAI 通过算力资源支持开源创新，使这个项目成为可能；也感谢更广泛的社区持续推动推理基准测试向前。

## 我们正在招聘

我们正在寻找一位工程师加入我们的特别项目团队。这是一个独一无二的机会——在 InferenceMAX™ 这类高曝光度的特别项目上工作，并获得众多行业领袖和 CEO 的支持。如果你热爱性能工程、系统可靠性，并希望在硬件与软件的交汇处工作，这是一个产生全行业影响的难得机会。

**你将参与的工作：**

- 跨多家供应商（AMD、NVIDIA、TPU、Trainium 等）构建并运行大规模基准测试
- 设计可复现的 CI/CD 流水线，将基准测试工作流自动化
- 保障行业合作伙伴所用系统的可靠性与可扩展性

**我们期望你具备：**

- 扎实的 Python 功底
- 站点可靠性工程（SRE）或系统级问题解决背景
- 有 CI/CD 流水线和现代 DevOps 实践经验
- 对 GPU、TPU、Trainium、多云和性能基准测试怀有好奇心

申请链接：<https://app.dover.com/apply/SemiAnalysis/2a9c8da5-6d59-4ac8-8302-3877345dbce1>

# InferenceMAX™ 计划支持者

InferenceMAX™ 计划得到了众多算力大买家和 ML 社区知名人士的支持，其中包括来自 OpenAI、Microsoft、PyTorch 基金会等的代表：

> *"当我们在前所未有的规模上构建系统时，ML 社区拥有开放、透明、能真实反映推理在软硬件之上表现的基准测试至关重要。InferenceMAX™ 的正面交锋基准测试穿透噪音，提供了 token 吞吐、每美元性能和每兆瓦 token 数的鲜活图景。这类开源努力强化了整个生态系统，帮助每一个人——从研究人员到前沿数据中心的运营者——做出更明智的决策。"*
>
> —— Peter Hoeschele，OpenAI Stargate 基础设施与工业计算副总裁

> *"开放协作正在驱动 AI 创新的下一个时代。开源的 InferenceMAX 基准测试为社区提供了透明、每夜更新的结果，赢得信任并加速进步。它展示了我们的 AMD Instinct MI300、MI325X 和 MI355X GPU 在多样工作负载上极具竞争力的 TCO 表现，凸显了我们平台的优势，以及我们让开发者实时了解我们软件进展的承诺。"*
>
> —— Dr. Lisa Su，AMD 董事长兼 CEO

> *"长上下文推理推动推理需求呈指数级增长。NVIDIA Grace Blackwell NVL72 正是为这个会思考的 AI 新时代而生。NVIDIA 正通过持续的硬件与软件创新来满足这一需求，赋能 AI 的下一步发展。InferenceMAX™ 通过高频基准测试，让业界得以透明地观察真实世界工作负载上的 LLM 推理性能。结论很清晰：搭载 TRT-LLM 与 Dynamo 的 Grace Blackwell NVL72 交付了无与伦比的每美元、每兆瓦性能——驱动着全球生产力最高、最具成本效益的 AI 工厂。"*
>
> —— Jensen Huang，NVIDIA 创始人兼 CEO

> *"速度就是护城河。InferenceMAX™ 的每夜基准测试与 AMD 软件栈的改进速度同频。很高兴看到 AMD 的 MI300、MI325 和 MI355 GPU 在多样工作负载和交互性水平上都有如此出色的表现。"*
>
> —— Anush Elangovan，AMD GPU 软件副总裁

> *"InferenceMAX™ 聚焦于 ML 社区真正关心的工作负载。在 NVIDIA，我们欢迎这样的对比，因为它们凸显了我们全栈方法的优势——从 GPU 硬件到 NVLink 网络，再到 NVL72 机柜级方案和 Dynamo 分离式服务，在大规模场景下持续交付业界领先的推理性能与 ROI。"*
>
> —— Ian Buck，NVIDIA 超大规模业务副总裁兼总经理、CUDA 发明人

> *"InferenceMAX™ 的每夜结果凸显了 AMD 软件栈的快速进步。见证一个开放项目的诞生令人兴奋——它在 AMD 软件团队的工作与这些工作如何影响我们 MI300、MI325 和 MI355 GPU 上的具体 ML 用例之间建立了紧密的反馈闭环。我期待 InferenceMAX 的下一步，也期待展示 AMD 平台的能力。AMD GPU 将继续每周都变得更快。"*
>
> —— Quentin Colombet，AMD 高级总监、前 Brium CEO

> *"Azure 的使命是为客户提供性能最强、效率最高、成本最优的 AI 云。SemiAnalysis InferenceMAX™ 通过提供透明、可复现的基准测试，追踪各种 GPU 和软件栈在真实负载下的推理性能，支持了这一使命。关于吞吐、效率和每瓦成本的持续数据，增强了我们将 Azure 推理平台调优到规模化运行的能力，帮助客户在微软云上充满信心地构建。"*
>
> —— Scott Guthrie，微软云与 AI 执行副总裁

> *"在微软，要在规模上为客户交付最佳的推理性能与经济效益，需要深入理解 AI 模型如何与真实世界的硬件和软件交互。像 InferenceMAX™ 这样的开源、可复现基准测试，对于在真实负载下生成关于吞吐、效率和成本的透明洞察至关重要。这些持续信号帮助指导我们的平台战略，使我们能够优化从芯片、系统到软件的整个技术栈，让每一层协同发力，充分释放我们基础设施的潜力。"*
>
> —— Saurabh Dighe，Azure 战略规划与架构企业副总裁

> *"理论峰值与真实推理吞吐之间的差距，往往由系统软件决定：推理引擎、分布式策略和底层内核。InferenceMAX™ 的价值在于它对最新软件进行基准测试，展示了 FP4、MTP、投机解码（speculative decode）和大规模专家并行（wide-EP）等优化在各种硬件上的实际效果。这样开放、可复现的结果能帮助整个社区更快前进。"*
>
> —— Tri Dao，Together AI 首席科学家、Flash Attention 发明人

> *"行业需要更多公开、可复现的推理性能基准。我们 vLLM 团队很高兴与 InferenceMAX™ 合作。更多人人可信、可引用的多样化工作负载与场景，将帮助生态向前发展。公平、透明的测量会推动技术栈每一层的进步——从模型架构到推理引擎再到硬件。"*
>
> —— Simon Mo，vLLM 项目共同负责人

> *"这个基准测试很不错，先生"*
>
> —— Michael Goin，vLLM 维护者

> *"InferenceMAX™ 基准测试是 pogchamp 级别的，请在弹幕里刷 W"*
>
> —— Kaichao You，vLLM 项目共同负责人

> *"InferenceMAX™ 展示了一个开放生态在实践中如何运作。vLLM、SGLang、TensorRT-LLM 等众多领先推理栈都构建在 PyTorch 之上，这类基准测试展示了内核、运行时和框架层面的创新如何转化为包括 NVIDIA 与 AMD GPU 在内多种硬件平台上可衡量的性能。凭借开源与每夜运行，InferenceMAX™ 提供了一种透明、社区驱动的进展追踪方式，并为 PyTorch 用户提供数据驱动的洞察。"*
>
> —— Matt White，PyTorch 基金会执行董事

> *"Oracle Cloud Infrastructure 的构建初衷是为前沿实验室和企业提供灵活性与选择权，提供多种可支撑大规模 AI 的 GPU SKU。InferenceMAX 通过交付开源、可复现、反映最新软硬件之上真实性能、效率与成本的基准测试，强化了这一使命。有了这种透明度，客户可以自信地选择最契合其 AI 战略的平台。"*
>
> —— Jay Jackson，Oracle Cloud Infrastructure 副总裁

> *"InferenceMAX™ 通过开放、透明的基准测试追踪最新 GPU 与软件栈之上的真实推理表现，树立了更高标杆。对客户而言，拥有衡量真实世界每美元 token 数和每瓦 token 数的可复现数据，能把抽象的营销数字变成可执行的洞察。在 CoreWeave，我们支持这一努力，因为它为这个快速变化的领域带来清晰度，帮助整个生态系统充满信心地构建。"*
>
> —— Peter Salanki，CoreWeave CTO

> *"InferenceMAX™ 提供开放、透明的基准测试，揭示当今主流 GPU 与软件栈之上的推理表现，树立了新标准。凭借衡量真实世界每美元 token 数与每瓦 token 数的可复现数据，客户可以超越营销话术、获得可执行的洞察。对于我们 Nebius 这样一家全栈 AI 云提供商而言，这项计划帮助我们自信地构建推理平台，并确保我们与生态保持一致。"*
>
> —— Roman Chernin，Nebius 联合创始人兼首席商务官

> *"在 Crusoe，我们相信成为出色的合作伙伴意味着赋予客户选择权与清晰度。这正是我们自豪支持 InferenceMAX™ 的原因——它为整个 AI 社区提供针对最新硬件的开源、可复现基准测试。通过交付关于吞吐、效率和成本的透明真实世界数据，InferenceMAX™ 穿透炒作，帮助客户自信地为其独特工作负载选择最合适的平台。"*
>
> —— Chase Lochmiller，Crusoe 联合创始人兼 CEO

> *"Supermicro 对 InferenceMAX™ 的发布感到兴奋，这一 SemiAnalysis 基准测试系统衡量真实世界的吞吐、每美元性能和能效。这个开源工具在最新硬件与软件上运行可复现的基准测试，使 AI 实验室和企业能够在规模上选出最佳平台。"*
>
> —— Charles Liang，Supermicro 创始人兼 CEO

> *"在 TensorWave，我们正在基于 AMD GPU 构建下一代云，因为我们相信只有客户拥有强有力的替代选择时，创新才会蓬勃发展。InferenceMAX™ 通过提供开源、可复现的基准测试来追踪最新软硬件之上的吞吐、效率与成本，强化了这一愿景。它穿透虚假的合成数字、突出真实世界的推理性能，帮助客户看到 AMD 平台在规模化 AI 上的全部潜力。"*
>
> —— Darrick Horton，TensorWave CEO

> *"Vultr 致力于提供开放生态，让开发者自由选择如何在 NVIDIA 或 AMD GPU 上构建和扩展 AI。借助 InferenceMAX™，客户获得开放、可复现的基准测试，清晰洞察尖端软硬件之上的吞吐、效率与成本。通过展示真实世界性能，我们助力团队自信地为其 AI 工作负载选择合适的平台。"*
>
> —— Nathan Goulding，Vultr 工程高级副总裁

# 吞吐量（tok/s/gpu）与延迟/交互性（tok/s/用户）之间的根本权衡

大规模服务 LLM 时面临的根本权衡，是吞吐量与交互性（以每用户每秒 token 数为单位计量）之间的取舍。吞吐量是每颗 GPU 处理 token 的速率（tok/s/gpu），而交互性描述的是为每个用户生成 token 的速率（token/秒/用户）。简单来说，你可以快速高效地服务单个用户，通常的做法是同时服务更少的用户，但这样做的代价是整体 GPU 吞吐下降。

这一权衡的存在，是因为 LLM 推理依赖矩阵乘法，而将多个请求合并成批能让矩阵乘法获益——也就是同时服务更多用户。大批量能带来更好的 GPU 利用率和更高的 token 吞吐，但会把可用资源分摊给更多请求，减慢每个用户的 token 处理速度。反过来，小批量把 GPU 资源集中到更少的请求上——即更少的用户，以牺牲整体吞吐为代价交付高交互性。实践中，大多数提供商都在这两个极端之间寻求平衡。这一权衡上的最优点取决于用例：有些应用优先考虑响应速度，另一些优先考虑吞吐。然而，目标交互性水平直接决定推理成本。交互性越高，成本越高。

自持或租用 GPU 系统做推理，通常对应固定的美元/小时成本。因此，随着交互性上升、整体吞吐下降，每小时处理的 token 变少，推高了单位 token 成本（以每百万 token 成本计量）。为保持盈利，提供商的 token 定价必须高于其服务成本。这意味着更高交互性的用例需要更高的单 token 价格来覆盖更高的成本，而高吞吐应用则可以以更低价格服务。

一个简单的类比可以概括整个权衡。一辆城市公交车和一辆法拉利的绝对持有成本可能非常接近，但公交车把成本摊到几十名乘客身上，而法拉利只服务一两个人。法拉利提供卓越的响应性——随到随走、直达路线、高端体验——但每个乘客分摊的成本本质上是更高的。LLM 服务也在类似的约束下运作。

![](https://substack-post-media.s3.amazonaws.com/public/images/539b0f8f-9421-41b4-9e89-a53f2697b0c8_1976x1454.png)
*来源：SemiAnalysis*

# 帕累托前沿曲线

吞吐与延迟之间永远存在权衡。为找出帕累托前沿曲线（Pareto Frontier Curve），我们尝试找出每一个这样的数据点 P：不存在任何其他点在吞吐和延迟两个维度上都优于 P。这意味着数据点 P 是**帕累托最优**的，即没有其他点能在不牺牲另一轴的情况下改善某一轴。把这些帕累托最优点连起来，就得到了帕累托前沿曲线。

![](https://substack-post-media.s3.amazonaws.com/public/images/4686438a-1880-4162-92c9-e64d2ab7718b_2852x993.png)
*来源：SemiAnalysis*

## InferenceMAX v1 基准测试方法论

提供能反映不同 GPU、推理引擎和工作负载在多个交互性水平上全部可能性的基准测试，是 InferenceMAX™ 的核心目标。本节将介绍基准测试方法论是如何围绕这一目标设计的。

每次基准测试运行，我们都会部署一个推理服务器和一个基准测试客户端。推理服务器监听并处理请求。我们根据模型选用 vLLM、SGLang 和 TRT-LLM。基准测试客户端方面，我们使用移除了 vLLM 依赖的 vLLM benchmark serving 脚本。基准测试客户端发送请求、记录运行时间，并保存与推理作业相关的指标。

我们选择用随机序列的请求做基准测试，以规避前缀缓存（prefix caching）——目前把前缀缓存纳入考量过于复杂。前缀缓存因工作负载而异，需要仔细调研请求模式才能选出有代表性的前缀比例。在 InferenceMAX 的后续迭代中，我们将使用 shareGPT 之类的数据集而非随机数据。我们将请求速率设为无限，并设置最大并发请求数，从而捕捉推理服务器在处理特定数量请求时的行为。我们还将请求总数设得足够大，以摊平冷启动带来的不稳定，例如 JIT 编译时间。

输入/输出序列长度方面，我们收敛到三组：代表聊天负载的 1024 输入 token / 1024 输出 token、代表推理（reasoning）负载的 1024 输入 token / 8192 输出 token、代表摘要负载的 8192 输入 token / 1024 输出 token。为模拟真实世界请求中输入序列长度不一的情况，我们将每个请求的输入长度在指定输入序列长度的 80% 到 100% 之间随机变化。

一次基准测试运行的配置项如下：

> · **模型**：LLaMA 70B、DeepSeek R1、gpt-oss 120B
>
> · **精度**：MXFP4 权重、FP8、FP4
>
> · **GPU**：H100、H200、B200、GB200 NVL72、MI300X、MI325X、MI355X
>
> · **开源框架**：[vLLM](https://github.com/vllm-project/vllm)、[SGLang](https://github.com/sgl-project/sglang)、[TRT-LLM](https://github.com/NVIDIA/TensorRT-LLM)
>
> · **并行度**：1、2、4、8 等
>
> · **最大并发**：4、8、16、32、64 等

先说模型。我们选择 LLaMA3 70B 代表稠密（dense）企业级模型部署。

为对稀疏 MoE 模型做基准测试，我们选定了 DeepSeekV3 670B。从算术强度、近似的激活/总参数量以及内存访问模式来看，DeepSeekV3 的模型架构是与 OpenAI 4o/5 等前沿闭源模型架构最匹配的模型。因此，在推测 OpenAI 内部模型架构可能的样子这件事上，DeepSeek 是最好的代理模型。

对于更小的稀疏 MoE 模型，我们选定了 GPT-OSS 120B MoE，因为在算术强度、近似的激活/总参数量和内存访问模式方面，它最接近 GPT-5 mini。

视硬件支持情况，我们在各模型上对 FP8、FP4 和 MX4 权重进行基准测试。我们扫过不同的最大并发用户数（一个与 batch size 类似的概念），以画出完整的吞吐-延迟曲线。我们还扫过不同的模型并行方案，因为更大的模型并行可以减少内存加载时间，从而在一定程度上提升低延迟区的吞吐，以此找到帕累托前沿曲线。

为避免[SGLang 与 vLLM 基准大战](https://x.com/dylan522p/status/1920638653677596836)重演并节省算力时间，我们决定先只从 vLLM 和 SGLang 中为每个模型选定一个作为默认引擎。早在 7 月，我们就告知 AMD 和 NVIDIA：DeepSeek 670B 我们将使用 SGLang，Llama3 70B 和 Llama4 将使用 vLLM。此后我们用 GPT-OSS 120B 替换了 Llama4，因为没有人用 Llama4，而且 GPT-OSS 120B 更接近较小号的「mini」前沿模型。

我们希望服务器配置尽可能反映真实部署，因此我们请 AMD 和 NVIDIA 提交与其官方文档指南在讨论如何在其硬件上部署这些模型时所参考内容相当接近的配置：

> - <https://docs.nvidia.com/llm-inference-quick-start-recipes/index.html>
> - [recipes.vllm.ai](https://docs.vllm.ai/projects/recipes/en/latest/)
> - <https://rocm.docs.amd.com/en/docs-7.0-docker/benchmark-docker/inference-vllm-gpt-oss-120b.html>

我们没有明确说明 InferenceMAX 是否允许预热（warmup），因此 NVIDIA 在其 SGLang DeepSeek 提交中加入了一个预热阶段来处理某些 JIT 编译的内核。在基准测试开发工作接近尾声时，AMD 注意到了 NVIDIA 提交中的上述情况，询问是否允许预热，因为他们没有意识到自己也可以这样做。经过 AMD、NVIDIA 与 SemiAnalysis AI 工程团队之间的讨论，各方同意目前暂不允许预热，而是把 DeepSeek 基准测试的长度最多延长 5 倍以保证公平。出现这种混乱是我们的责任，我们没有从一开始就把预热规则说清楚。我们计划在发布后重新讨论这个话题，因为在真实世界的生产推理中，预热往往发生在 Kubernetes 控制面将 pod 标记为健康之前。

## 讨论：服务 DeepSeek R1 的策略

我们允许各厂商选择性地为 DeepSeek R1 提交分离式服务（disaggregated serving）配置。分离式服务将推理的两个阶段——预填充（prefill）与解码（decode）——分配到不同的 GPU 资源上。通过把两个阶段分开，处于不同阶段的请求不会互相干扰，从而带来更好的 SLA 保障，尤其是在高并发场景下。

我们还在分离式服务之上叠加了大规模专家并行（wide EP）。wide EP 由多项技术支撑，其中最著名的是 DeepEP。DeepEP 提供两种分发模式：normal 和 low latency。normal 模式专注于提升预填充阶段的吞吐，而 low-latency 模式专为降低解码阶段延迟而设计。

对于分离式服务的 DeepSeek R1，我们还收到了启用多 token 预测（MTP）的提交。DeepSeek R1 实现了 MTP：模型被训练为在额外 MTP 模块的帮助下，每次前向传播预测多个 token。据 DeepSeek 介绍，用 MTP 训练可以提升模型的规划能力。此外，在推理中使用 MTP 模块能以极小的模型质量损失提升 token 吞吐。

![](https://substack-post-media.s3.amazonaws.com/public/images/18326fc6-9e43-4998-838b-b2b7087de7f1_2853x1341.png)
*来源：DeepSeek-V3 技术报告，图 3*

NVIDIA 提交了在 GB200 NVL72 上以分离式服务、wide EP 和 MTP 运行 DeepSeek R1 的结果。NVIDIA 还提交了特定配置以描绘帕累托前沿，我们计划未来扩展到扫更大的配置空间。

![](https://substack-post-media.s3.amazonaws.com/public/images/2c25289d-8cf8-4d1a-9be6-69a4e12f9886_2353x1271.png)
*来源：DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving*

在服务 DeepSeek R1 时，SGLang 提供多种并行策略，包括**张量并行（tensor parallel, TP）**、**数据并行（data parallel, DP）**和**专家并行（expert parallel, EP）**。并行策略在 GPU 之间拆分工作，以降低单 GPU 内存占用并提升硬件利用率。

![](https://substack-post-media.s3.amazonaws.com/public/images/076f3327-558d-481f-91be-87edecf55135_2153x1624.png)

通常，我们用张量并行沿注意力头数维度（通常是 128）拆分注意力层的工作。但这与 DeepSeek R1 并不契合，因为它使用 Multi-Latent Attention（MLA）——一种只有单个 KV 头的特殊注意力，会导致 KV 缓存被复制。为解决这个问题，SGLang 在较低交互性场景下使用数据并行注意力（data parallel attention），沿 batch 维度拆分工作，从而免去 KV 缓存复制并降低通信负载。

DeepSeek R1 还有大量专家层，因此我们应用专家并行，为每颗 GPU 分配一组专家层。这降低了内存占用，代价是更高的通信负载。

![](https://substack-post-media.s3.amazonaws.com/public/images/b668c1ec-765e-4bfd-9e17-66c2bfb91c76_1590x1582.png)
*来源：SGLang v0.4: Zero-Overhead Batch Scheduler, Cache-Aware Load Balancer, Faster Structured Outputs*

# InferenceMAX™ 的架构

InferenceMAX™ 使用 GitHub Actions 编排基准测试运行。GitHub Action 把每个基准配置作为一个 [job](https://docs.github.com/en/actions/get-started/understand-github-actions#jobs) 运行，并在 [runner](https://docs.github.com/en/actions/get-started/understand-github-actions#runners) 上执行。我们将 GPU 服务器作为 runner 接入 GitHub Actions，让它们监听请求并执行 job。执行 job 时，runner 会运行为该服务器编写的启动脚本，后者再根据服务器设置调用 Docker 或 SLURM。启动脚本随后执行包含具体基准配置的基准脚本。

我们把「并行策略 + 最大并发」基准扫描的逻辑定义为一个参数化的 [workflow](https://docs.github.com/en/actions/get-started/understand-github-actions#workflows)，并逐步组合该 workflow，以对所有模型执行所有 GPU 类型以及不同输入/输出序列长度的测试。

![](https://substack-post-media.s3.amazonaws.com/public/images/290f8a5a-3e55-45c6-a0e4-7c1dc6065175_2293x1701.png)
*来源：SemiAnalysis*

## 性能结果——吞吐 vs 端到端延迟/交互性（tok/s/用户）

以下是撰写本文时 2025 年 10 月 7 日每夜运行的性能快照。完整的每夜结果请访问我们的仪表盘 <http://inferencemax.ai/>。

解读吞吐 vs 延迟/交互性图表时，请记住大多数实际应用都运行在两个极端之间的某处。只测量单一或有限吞吐/交互性水平的基准结果有时会带来误导。

举例来说，如果在某个交互性水平下 GPU A 的吞吐是 GPU B 的 4 倍——以面向人类的 AI 聊天机器人应用为例取 5 tokens/s/用户——这个交互性水平实际上慢到根本不可用，这意味着这个性能差异在现实世界中几乎没有意义。相反，应当为给定应用选择一个现实的交互性水平。

在本报告后文中，我们还会按这些 GPU 的总拥有成本（TCO）对吞吐做归一化。

每百万 token 的 TCO 才是客户真正关心的北极星指标——性能只是计算该指标的垫脚石。例如，B200 的吞吐可能比 MI355X 高 1.5 倍，但如果它每小时的 TCO 是 2 倍——那么 MI355X 反而是更好的选择，因为即便 MI355X 的单 GPU 绝对吞吐更低，它每单位 TCO 交付的性能更好。

下面我们通过几个基准测试例子来说明如何分析这些结果。

第一组结果：在我们的推理场景（1k 输入 / 8k 输出）下，H100 vLLM 与 MI300X ROCm 7.0 vLLM 在 Llama 3.3 70B FP8 上的对比显示 MI300X 表现强劲，尤其是在低交互性水平（20 到 30 tok/s/用户），这得益于 MI300X 在 TP1 下运行时更好的内存带宽和内存容量优势。

![](https://substack-post-media.s3.amazonaws.com/public/images/471369b0-e290-4560-a348-b3079c8b6e88_2329x1393.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/a46e880d-4076-46ff-84d1-5be99ba50a8a_2634x1582.png)
*来源：SemiAnalysis*

在摘要负载下，H200 与 MI325X 在 vLLM GPT-OSS 120B（MX4 权重）上的对比结果颇具竞争力。交互性低于 110 tok/s/用户时 MI325X 相对 H200 占优，在 110 tok/s/用户以上也仍与 NVIDIA 有一战之力。

![](http://inferencemax.ai/)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/cb664d13-b2f7-42e5-824d-fbf6319c0f7f_2406x1432.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/3350a97b-7c28-4e46-9c80-519555da1eb6_2342x1124.jpeg)
*来源：SemiAnalysis*

在 LLaMA 70B FP4 上，B200 在全部三类工作负载的吞吐性能上都显著优于 MI355X。这说明 AMD 的 FP4 内核还有改进空间。

再看 GPT-OSS 120B 上 B200（vLLM 和 TRT-LLM）与 MI355X vLLM 的对比：按 TCO 归一化后，MI355X 与 B200 vLLM 具有竞争力。下一节我们会看到，在某些交互性区间内 MI355X 的每 TCO 性能优于 NVIDIA。吞吐-延迟图显示的竞争更为胶着——在相同 tok/s/gpu 吞吐下，MI355X 落后 B200 从不超过约 15 秒。我们在现实世界中看到的最实用的交互性区间，对 GPT-OSS 120B 而言约为 150-200 tok/s/用户。

![](https://substack-post-media.s3.amazonaws.com/public/images/d40e2253-8285-466f-8f16-6459c1051fb4_2373x1419.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/918c3a71-6c31-400a-a5c9-fb0930f8a2f7_1879x1121.png)
*来源：SemiAnalysis*

转向 DeepSeek 670B MoE FP8：比较 SGLang 上的 MI325X 与 SGLang 上的 H200 时，我们观察到在给定吞吐水平下，MI355X 在延迟和交互性两方面都明显落后。在相当吞吐下，SGLang 上的 H200 服务推理的延迟始终比 MI325X 低约 40%。此外，比较二者交互性的帕累托前沿也能看到稳定的差距。比较 SGLang 上的 MI355X 与 SGLang 上的 B200，得到的结论与 MI325X vs H200 的比较类似。在 SGLang 镜像方面，AMD 看起来还有大量改进空间。

我们还可以看到，GB200 NVL72 SGLang Dynamo FP8 机柜级推理尚未优化到位，仍有提升空间。

![](https://substack-post-media.s3.amazonaws.com/public/images/2755907c-48bb-47aa-99be-6058c695ac85_1857x1121.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/d68490f3-adfd-4ab7-b6d1-80bae3921ef9_1868x1121.png)
*来源：SemiAnalysis*

再看 FP4 的 DeepSeek 670B MoE：GB200 NVL72 机柜级 TRT-LLM 推理大幅领先单节点 SGLang 推理。我们期待在未来几个月对多节点 8 卡机器上的 wideEP + 分离式预填充进行基准测试。

![](https://substack-post-media.s3.amazonaws.com/public/images/9534de11-42bd-44c9-9398-16bb9deedcfd_1864x1121.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/c98fcaff-2665-406e-8ce0-c63c456532e4_1374x839.png)
*来源：SemiAnalysis*

接下来，我们在 8K 输入 / 1K 输出场景下比较 DeepSeek R1 开启与关闭多 token 预测（MTP）的 GB200——这一输入/输出比例意在反映摘要用例。在吞吐 vs 交互性的对比中，开启 MTP 的收益尤为明显。在 70-140 tok/s/用户区间内，开启 MTP 场景的单 GPU 吞吐显著高于关闭 MTP——在相同交互性（tok/s/用户）下，吞吐最高可达 2-3 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/cb76eccd-5bb3-480e-98b0-e821f11b8d88_1849x1121.png)
*来源：SemiAnalysis*
![](https://substack-post-media.s3.amazonaws.com/public/images/717be24a-af21-4e21-a829-c907bf3aaa88_1883x1121.png)
*来源：SemiAnalysis*

# 性能结果——每百万 token TCO vs 交互性（tok/s/用户）

然而，比较单 GPU token 吞吐只是抵达真正底线——即每 token 总拥有成本（TCO）——所需的若干数据点之一。

ML 推理工程师通常以每百万 token TCO 为单位来衡量。要从单 GPU 吞吐换算到每百万 token TCO，在芯片对芯片比较时必须按美元/小时/GPU 的总拥有成本做归一化。例如，如果 B200 的吞吐比 MI355X 高 1.5 倍，但每小时 TCO 是 2 倍——那么即便绝对性能更低，MI355X 仍是更好的选择。

在我们的 InferenceMAX™ 门户（<http://inferencemax.ai/>），我们针对多类客户群体估算了每百万 token TCO vs 延迟/交互性，例如：

> - 自购并持有芯片的超大规模云厂商和一级前沿实验室（4 年经济使用寿命）
> - 计划自持芯片的新兴 GPU 云（neocloud）巨头和大型托管推理提供商（4 年经济使用寿命）
> - 以 3 年合约、25% 预付款从新兴 GPU 云租用 GPU

对每 token 总拥有成本建模绝非易事，它涉及 SemiAnalysis 多个团队和业务板块。在 AI Token 工厂经济模型（AI Token Factory Economics）栈中，我们展示了推导这一北极星指标所用的全部假设，以及用于确定这些量的 SemiAnalysis 模型。

![](https://substack-post-media.s3.amazonaws.com/public/images/d913a30b-22dc-42bd-93bc-f81500ac9d18_1415x864.png)
*来源：SemiAnalysis AI 加速器模型、SemiAnalysis BoM 与 ODM 模型、SemiAnalysis AI 网络模型、SemiAnalysis AI TCO 模型、SemiAnalysis 数据中心模型。*

其中，[SemiAnalysis AI TCO 模型](https://semianalysis.com/ai-cloud-tco-model/)对多种 AI 服务器方案与网络架构（即 InfiniBand vs SpectrumX vs Arista 以太网 vs 白牌以太网）的组合提供了全面的总拥有成本建模，是 InferenceMAX™ 中单 GPU 总拥有成本以及新兴 GPU 云租赁市场价格的主要来源。

SemiAnalysis GPU 云市场租赁价格报告基于对 70 多家 GPU 云和 100 多家从 GPU 云租卡的最终用户的调研。未来，我们计划在 InferenceMAX.ai 门户上实现不同租约定价时长的仪表盘，比如 1 年或 1 个月。我们还计划支持自定义输入，让你输入自己的 $/GPU/hr 报价，从而确定最匹配你交互性目标与成本的 GPU。

在下文分析中，我们聚焦于自持芯片、并按 4 年经济寿命核算商业案例的超大规模云厂商级运营方的每百万 token 成本。

我们看到，在所有交互性水平下，vLLM 上 MI325X 的每百万 token 成本都优于 vLLM 上 H200 的每百万 token 成本。当引入 NVIDIA（基本）开源的 TRT-LLM 后，H200 当前软件栈战胜了使用当今 vLLM 栈的 MI325X。

![](https://substack-post-media.s3.amazonaws.com/public/images/1217e5ad-909c-419e-b4a5-304a7145275e_1736x1165.png)
*来源：SemiAnalysis*

在推理输入/输出长度场景下运行 Llama3 70B FP4 时，比较 vLLM 上的 B200 与 ROCm 7.0 vLLM 上的 MI355，B200 目前胜出。这也印证了我们的建议：AMD 应更专注于优化 Llama3 的 FP4。

![](https://substack-post-media.s3.amazonaws.com/public/images/5dde0cca-4570-4e17-a685-f8aa0fc9685c_1774x1178.png)
*来源：SemiAnalysis*

在 GPT-OSS 120B FP4 摘要任务上，vLLM 上 MI355X 的每百万 token TCO 低于 vLLM 上的 B200，在交互性低于 225 tok/s/用户时甚至能击败 TRT-LLM 上的 B200。交互性高于 225 tok/s/用户时，TRT-LLM 上的 B200 及其他推理引擎的优化程度更高，每性能 TCO 低于 vLLM 上的 MI355X。

![](https://substack-post-media.s3.amazonaws.com/public/images/1629db8a-7dbb-4d06-b58c-60c58b66a248_1826x1237.png)
*来源：SemiAnalysis*

在 MX4 权重的 GPT-OSS 120B 上，MI300X 在整个交互性区间内都表现出相对 H100 非常强的每 TCO 性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/2f3e8a00-c9fe-4a81-be97-6a3681eb15ee_1668x1121.png)
*来源：SemiAnalysis*

对于使用 MX4 权重的 gpt-oss 120B，在交互性低于 135 tok/s/用户时，TRT-LLM 上 H200 的每 TCO 性能与 MI325X 不相上下。高于该水平后，MI325X vLLM 在每百万 token TCO 上领先 H200 TRT-LLM。

这个结果令人意外之处在于：面向 Hopper 的真开源 vLLM 比「基本」开源的 TRT-LLM Hopper 版更快。在交互性高于 135 tok/s/用户时，连 vLLM 上的 MI325X 都能击败 TRT-LLM 上的 H200。

![](https://substack-post-media.s3.amazonaws.com/public/images/dd8c102c-4041-4e37-be5f-5b308b06adfc_1672x1121.png)
*来源：SemiAnalysis*

再看 FP8 的 DeepSeek 670B MoE：当每百万 token TCO 保持不变时，SGLang 上的 B200 交付的交互性比 SGLang 上的 MI355X 快 1.5 倍。我们注意到，ROCm AITER 中还有大量正在集成到 SGLang 的优化，因此我们预计 SGLang DeepSeek 670B MoE 的每 TCO 性能很快会提升。

当交互性保持在约 35 tok/s/用户时，GB200 NVL72 击败所有其他选项，每百万 token TCO 好 4 倍。我们注意到，Dynamo 团队目前只来得及实现足以在 30 tok/s/用户区域拉低并行成本帕累托前沿的优化。他们还有空间进一步优化，把 FP8 GB200 NVL72 在约 40 及以上交互性水平的成本帕累托前沿继续下压。

![](https://substack-post-media.s3.amazonaws.com/public/images/aa169f01-a0c1-493e-9fcf-15e0c3e9e2dd_1646x1121.png)
*来源：SemiAnalysis*

再看摘要用例下使用 FP4 的 DeepSeek R1：交互性低于 90 tok/s/用户时，使用 Dynamo 分离式预填充的 TRT-LLM 引擎上的 GB200 NVL72 在每百万 token TCO 上决定性地优于所有单节点 8 GPU 服务器。有趣的是，交互性高于 90 tok/s/用户时，TRT-LLM 上的 B200 反而击败 GB200 NVL72。不过就目前而言，对于高交互性用例，单节点 B200 服务器可以取得比 GB200 NVL72 更好的每性能 TCO。

![](https://substack-post-media.s3.amazonaws.com/public/images/a154ae09-41cd-487b-a99c-30f89c793381_1946x1302.png)
*来源：SemiAnalysis*

在下面聚焦推理用例的基准中，SGLang 上的 B200 目前优于 SGLang 上的 MI355X。

![](https://substack-post-media.s3.amazonaws.com/public/images/d8274bbd-4310-44b0-9545-809260cfca44_1669x1121.png)
*来源：SemiAnalysis*

在摘要场景下，使用当今 TRT-LLM Dynamo 软件的 GB200 在交互性低于 80 tok/s/用户时优于 B200 单节点。比较 SGLang 上的 MI355X 与 SGLang 上的 B200，B200 的每百万 token TCO 更好。

![](https://substack-post-media.s3.amazonaws.com/public/images/f5dcfed6-70d1-460f-8963-14784577ca44_1695x1121.png)
*来源：SemiAnalysis*

我们还对使用多 token 预测（MTP）的 FP4 工作负载做了基准测试——MTP 是 DeepSeek 团队在训练期间实现的功能。我们看到，在每百万 token TCO 持平的情况下，MTP 能在该成本水平下交付比无 MTP 高 2-3 倍的交互性（tok/s/用户）。事实上，大多数前沿实验室和一级托管 DeepSeek REST API 端点提供商已经在生产负载中启用了 MTP。

![](https://substack-post-media.s3.amazonaws.com/public/images/90eb3363-3d59-4c46-aff7-521af7ecc45b_1679x1121.png)
*来源：SemiAnalysis*

## 估算的每全包已部署公用电力兆瓦 token 吞吐 vs 交互性（tok/s/用户）

电力是 AI 基础设施的终极约束。每座数据中心都在有限的功耗包络内运行，通常以兆瓦（MW）计量。这直接决定了给定数据中心能产出多少有效计算、最终能产出多少 token。

推理经济学不仅可以从单 GPU 吞吐 vs TCO 的 GPU 性能视角来分析，还可以从每电力吞吐的视角来分析——以每全包已部署公用电力 MW 的 token/s 来衡量。总公用电力涵盖 GPU、CPU、网络设备、其他相关集群 IT 设备以及设施开销的电力需求。设施开销包括配电损耗以及冷水机组、CDU、冷却塔等冷却设备的耗电等项目。每 MW 处理的 token 越多，每单位能源的潜在营收和利润就越高。请注意，对 InferenceMAX™ 而言，我们使用的是全包已部署公用 MW（计入了上述设施开销），而非不计设施开销的全包关键 IT 负荷 MW（Critical IT MW）。这些数值因站点而异，但我们基于自己的 [AI TCO 模型](https://semianalysis.com/ai-cloud-tco-model/)和[数据中心模型](https://semianalysis.com/datacenter-industry-model/)选取了一个行业代表性数值。

请注意，托管（colocation）租金和电费通常不到总拥有成本的 20%。这意味着，如果某颗 GPU 的每 MW token 数比另一颗低 20%，折算到总拥有成本的差异也不到 4%（即 20% × 20% = 4%）。TCO 的大头来自各 GPU 硬件厂商收取的毛利率。有的厂商毛利率高达 75%（即相对销售成本 4 倍加价），有的则低于 50%（即不到销售成本的 2 倍）。

我们使用速率单位——即每 MW 的 token/s，而非每 token 的累计能量（如焦耳/token）。这是因为数据中心容量是以兆瓦（MW）为单位建设的，MW 本身就是速率单位，等于每秒 1 兆焦（MJ）。如果在给定时间段上对速率单位积分，就得到该时段消耗能量的绝对量。

目前，我们把数据中心内各组件的热设计功耗（TDP）加总，来构建给定集群所需 MW 的估算。TDP 并不等于预期平均功率。举个例子：对内存带宽受限的解码负载，系统功耗永远不应达到 TDP，而是停留在一个更低的功率水平——即预期平均功率。未来，我们将通过 ipmitool 实测每个系统（以及网络设备）的实际功耗。到那时我们才会转向每 token 累计能量。

我们基于 InferenceMAX™ 原始结果，结合来自我们的 [AI 数据中心行业模型](https://semianalysis.com/datacenter-industry-model/)的 AI 集群总公用电力数据，估算每已部署电力的吞吐。该模型通过跨厂商、架构和推理栈的功率归一化估算来量化总公用电力。完整估算与持续的每夜基准测试见 [InferenceMAX.ai](https://inferencemax.semianalysis.com/)。

## 每 MW 性能结果

我们看到，对于 gpt-oss 120B（MX4 权重）的推理场景（1K 输入 token / 8K 输出 token），在 90 tok/s/用户交互性水平下，MI300X 每全包已部署 MW 可处理 750,000 token/s（再次说明：这是按公用 MW 计量，而非按关键 IT 负荷 MW），而 MI355X 每全包已部署 MW 可处理 2,550,000 token/s。这代表从 CDNA3 代到 CDNA4 代约 3 倍的能效提升。

![](https://substack-post-media.s3.amazonaws.com/public/images/0aa98f63-d0f8-4666-85fd-47a1bbf78c7a_1645x1121.png)
*来源：SemiAnalysis*

在 NVIDIA 阵营内跨代比较也能看到类似趋势。对比 HGX H100 与 HGX B200 在 FP4 权重 gpt-oss 120B 上的表现：H100 每 MW 可处理 900,000 token/s，而 B200 每 MW 可处理 2.8M token/s——B200 相对 H100 能效好约 3 倍。当看约 180 tok/s/用户的更高交互性水平时，B200 交付了高达 7 倍的能效提升，令人瞠目。

![](https://substack-post-media.s3.amazonaws.com/public/images/3b5b1ecd-8df1-48c8-8e21-5bfa9f21352b_1654x1121.png)
*来源：SemiAnalysis*

再来比较 AMD 与 NVIDIA 同代 GPU 的能效。我们首先看 GPTOSS 120B 的每全包已部署公用 MW token/s。根据下面 InferenceMAX™ 的初步结果快照，以每电力吞吐这一指标衡量，Blackwell 的能效比 CDNA4 架构高 20%。造成这一差距的一个重要因素是：MI355X 仅 GPU 的 TDP 就高得多，为 1.4kW/GPU，而 B200 为 1kW/GPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/594bc030-2862-4521-acf4-d06304a30dce_1687x1121.png)
*来源：SemiAnalysis*

下一组基准，我们看 DeepSeek R1 在 30 tok/s/用户交互性水平下的每电力 token 数。比较单节点 H200 FP8 与 GB200 NVL72 FP4（未启用多 token 预测），GB200 NVL72 的每全包已部署 MW 处理 token/s 提升约 8 倍。注意 H200 和 B200 的结果均为单节点。我们将探索 B200 和 H200 通过在 SpectrumX 以及 InfiniBand 之上实现分离式预填充与大规模专家并行所能解锁的更高每 MW token 吞吐。SGLang 的 [GB200 NVL72 分析](https://lmsys.org/blog/2025-09-25-gb200-part-2/)表明，8 GPU 系统确实可以通过实现大规模专家并行获得强劲的性能提升。不过 SGLang 的博客也表明，即便双方都实现了分离式预填充与 wide EP，GB200 NVL72 依然胜过 Hopper。

![](https://substack-post-media.s3.amazonaws.com/public/images/e17e8c63-bc2a-4ce2-a9c9-0d00a586de3a_1566x1121.png)
*来源：SemiAnalysis*

继续看 DeepSeek，转向 FP8：在 tok/s/gpu vs tok/s/用户上，GB200 同样碾压所有单节点系统。我们注意到这里有一些细节——B200 和 MI355X 都在运行单节点 SGLang，尽管对 DeepSeek 而言，MI355X 上 vLLM 可能交付比 SGLang 更好的结果。我们将探索为 MI355X 增加 DeepSeek on vLLM，和/或为所有 8 GPU 服务器增加 SGLang 多节点 wideEP。此外，如前所述，请注意 Dynamo 团队只来得及实现足以把并行帕累托前沿拉低到约 30 tok/s/用户为止的优化。进一步的优化还能把帕累托前沿继续下压，从而在更高交互性水平上抬升 GB200 NVL72 FP8 的每电力吞吐。

![](https://substack-post-media.s3.amazonaws.com/public/images/129e616b-82d6-413b-ae0c-e28f07b27d84_1661x1121.png)
*来源：SemiAnalysis*

## AMD 的 bug 与 NVIDIA Blackwell 的 bug

有几个 Blackwell bug 的排查过程相当有趣。第一个 bug 是：我们从 2025 年 7 月开始使用的 Blackwell vLLM 镜像，会导致裸机 B200 机器上的实例卡死长达 30 分钟。这个问题尤其难以复现和调试，因为其他人尝试在他们的 Blackwell 集群上使用完全相同的镜像时并没有遇到任何挂起问题。

我们调试这个挂起问题用到的第一个工具是 Python 性能分析器 [py-spy](https://github.com/benfred/py-spy)，用来收集 trace。我们注意到进程卡在了 [ncclCommInitRank](https://github.com/NVIDIA/nccl/blob/8d26308e6aba7f1667b24a861b5dc73f0f2e1f40/src/init.cc#L1974) 上——这很奇怪，因为正如许多 ML 性能工程师所知，这个函数在单节点上应该运行得非常快。另一点值得注意的是，vLLM 对 NCCL 使用了[自家定制的 FFI 绑定](https://github.com/vllm-project/vllm/blob/3d1f67616da88cbf0033bf5027cc0c6e5e9cacf6/vllm/distributed/device_communicators/pynccl_wrapper.py#L144)，原因是[诸多技术考量](https://github.com/vllm-project/vllm/blob/3d1f67616da88cbf0033bf5027cc0c6e5e9cacf6/vllm/distributed/device_communicators/pynccl_wrapper.py#L4-L23)。

![](https://substack-post-media.s3.amazonaws.com/public/images/465df901-046f-4109-84b4-7ccaf092f79e_2810x867.png)
*来源：SemiAnalysis*

通读 vLLM 的 NCCL 绑定后，我们并不认为 FFI 绑定是问题的根因。运行 nvidia-smi，我们看到 GPU_UTIL 不是 100% 而是 0%——说明 GPU 上没有任何内核在运行，因此我们判断这不是设备侧的 NCCL 死锁。

接下来，我们用 Linux [perf](https://perfwiki.github.io/main/) top 性能分析器深入 Python 层之下，试图进一步弄清是哪个共享库可能触发了这个问题。我们注意到该进程（及子进程）的大部分 CPU 周期都花在「libnvidia-ptxjitcompiler.so」上。查阅 libnvidia-ptxjitcompiler 的文档时，我们看到了这样一段描述：*"PTX JIT 编译器库（/usr/lib/libnvidia-ptxjitcompiler.so.575.57.08）是一个将 PTX 编译为 GPU 机器码的 JIT 编译器，由 CUDA 驱动使用。"* 这非常奇怪，我们不明白为什么初始化时要调用 PTX 编译器——明明没有需要即时编译的内核，因为 NCCL 内核通常在构建时就已全部预编译好。

![](https://substack-post-media.s3.amazonaws.com/public/images/a8a1c7d6-51e3-4b5f-85ea-41568792ac21_1937x1121.png)
*来源：SemiAnalysis*

我们太~~懒~~忙了，没空重建整个容器镜像、从头编译带调试符号的 NCCL。于是我们接着用 [strace](https://man7.org/linux/man-pages/man1/strace.1.html) 弄清 ptxjitcompiler 在发起哪些系统调用，以便再往下一层看它在调用哪些函数。我们看到 ptxjitcompiler 在容器内创建文件并向 ~/.nv/ComputeCache/ 写入文件。

![](https://substack-post-media.s3.amazonaws.com/public/images/c9556f28-f5c9-4ffb-935a-d85b790bbe44_2125x1121.png)
*来源：SemiAnalysis*

再剥开一层洋葱皮，我们研究了 ~/.nv/ComputeCache/ 的作用。根据文档，它是把 PTX 虚拟 ISA 转换为 SASS 机器码的缓存。这同样让我们非常困惑，因为 NCCL 通常在构建时除了 PTX 虚拟 ISA 之外还会把机器码一并打包。我们开始阅读 NCCL 构建脚本，[发现我们使用的 CUDA 12 并未启用 SM100（Blackwell）](https://github.com/NVIDIA/nccl/commit/80f6bda4378b99d99e82b4d76a633791cc45fef0#diff-45a9034a0c75cbfbbb34e853a43f6513c1d4c933eccf6adca705abe234fc1113R42-R49)，并发现他们只为尚未发布的 CUDA 13 启用了它。这意味着 SM100 SASS 没有被打包，我们在 JIT 把 compute_90（Hopper）PTX 转换为 SM100 SASS，导致进程耗时极其漫长。其他人运行时没看到这个 bug 的原因是：他用的是内部集群，通过 slurm 的设置手动挂载了自己的主目录。由于 SASS JIT 缓存就存在主目录 ~/.nv/ComputeCache/ 里，SASS 早已被缓存！

原来，vLLM 7 月的容器镜像基于 PyTorch 容器镜像，而后者使用的 NCCL 版本没有预编译 Blackwell SM100。解决办法是使用[修复后的 2.26.2 版本](https://pypi.org/project/nvidia-nccl-cu12/2.26.2.post1/)（已捆绑 Blackwell 支持），这样我们就不用浪费 30 分钟把虚拟 ISA 编译成机器码。这个 bug 已在最新的 vLLM 容器镜像中修复。感谢 simon-mo、youkaichao、mgoin、Robert-shaw、ptrblck 和 Kedar Potdar 帮助实现永久修复并迅速行动、快速解决。

![](https://substack-post-media.s3.amazonaws.com/public/images/e242f6a3-f0a2-4a95-9301-c4bdc6695544_1839x1121.png)
*来源：SemiAnalysis*

我们遇到的另一个 Blackwell 问题是 vLLM/SGLang 的子依赖 Flashinfer 出现文件锁竞态条件。出于某种原因，NVIDIA 决定不把编译好的内核打包进容器镜像，而是在服务器启动时下载。由于我们每个节点最多有 8 个进程（每 GPU 一个进程），如果代码不是进程安全的，下载这些编译内核时就会发生竞态条件。

结果发现，这个竞态条件恰恰是[为了防止竞态条件发生而引入的](https://github.com/flashinfer-ai/flashinfer/pull/1779)！Flashinfer 没有依赖内置 FileLock Python 包的锁清理机制，而是手动清理锁，从而导致了竞态。[这个问题已在 Flashinfer 中修复](https://github.com/flashinfer-ai/flashinfer/pull/1779)，但尚未上游合入 vLLM/SGLang 的 Blackwell 发布容器镜像。特别感谢 Flashinfer 团队和 Kedar Potar 火速介入，帮助调试和打补丁——从与团队取得联系到解决，前后只用了 4 个小时。

还有另一个 Blackwell bug：Flashinfer 把一个构建环境标志名改成了 FLASHINFER_CUDA_ARCH_LIST，但 NVIDIA 的人没有通知 vLLM/SGLang 维护者，也没有提交自己的 PR，因此有几周时间 [vLLM](https://github.com/vllm-project/vllm/pull/25730) 和 [SGLang](https://github.com/sgl-project/sglang/pull/11226) 不支持 flashinfer 的 AOT。

我们还观察到，NVIDIA 容器工具链时不时就会完全报错，并显示如下信息：

> *"docker: Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: error during container init: error running prestart hook #0: exit status 1, stdout: , stderr: Auto-detected mode as 'legacy'*
>
> *nvidia-container-cli: initialization error: driver rpc error: timed out: unknown"*

在命令行尝试使用 nvidia-smi 同样会触发卡死。这表明整个 NVIDIA 驱动实际上已经崩溃。经过与 NVIDIA 固件/驱动团队和 NVIDIA NCCL 团队的细致调试会，我们发现了根因：鉴于我们使用 CUDA graph 且每夜启动超过 500 个 Blackwell 容器，NCCL 2.26 以来存在一个缓慢的资源泄漏 bug。

由于我们要停止和启动大量 Blackwell 容器，这些启停不断累积，最终把驱动搞崩。资源泄漏 bug 的具体成因在于：启用 CUDA graph 时，NCCL 默认会启用 user buffer。如果没有这个资源泄漏 bug，NCCL user buffer 功能本可让 NCCL 直接使用应用层缓冲区实现零拷贝，从而减少应用层缓冲区与 NCCL 内部缓冲区之间的数据搬运。[临时解决办法](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html#nccl-graph-register)是在 bug 修复推出之前先不启用 NCCL user buffer。修复预计在 10 月 20 日前后，预计将随 NCCL 2.28 的小版本更新发布。感谢 Kedar Potar 和众多 NVIDIA 团队成员以惊人的速度和支持力度迅速定位根因并修复 bug。

在 AMD 这边，我们开发 InferenceMAX™ 期间遇到的 bug 更少，而且更容易修复。其中一个 bug 是：AMD 版 cuDNN——AITER——在一个辅助函数中崩溃，原因是它没有考虑到「/opt/rocm/llvm/bin/amdgpu-arch」不仅会返回计算架构（即 gfx942），还可能返回带后缀的 gfx942。AITER 本应通过模式匹配来判断它在哪种架构上工作，但没有考虑存在后缀的情况。[临时修复](https://github.com/InferenceMAX/InferenceMAX/blob/3b8879031799cac260ef00bd8911dabbe5982d49/benchmarks/70b_fp8_mi325x_slurm.sh#L39)很简单，未来几周 AITER 将合入永久修复。感谢 Quentin 帮忙修复这一个！

在对 MI355X 做基准测试时我们还遇到一个 bug：基准运行崩溃并倾泻出 1TB 名为 gpucore.XXX 的文件。调查后发现，根因是服务器配置中的分块预填充（chunked prefill）大小设得过高。将其从 196608 降到 32768 后问题解决（[PR 链接](https://github.com/InferenceMAX/InferenceMAX/pull/80/files)）。

AMD [最近增加了 pyxis 支持](https://instinct.docs.amd.com/projects/container-toolkit/en/release-1.1.x/container-runtime/enroot-pyxis-installation.html)，这为在 SLURM 中使用容器带来了良好体验，尤其是在多节点训练或多节点离线批处理推理作业方面。但我们遇到了一个与其 ROCm 7.0 SGLang 镜像 *"rocm/7.0:rocm7.0_ubuntu_22.04_sgl-dev-v0.5.2-rocm7.0-mi30x-20250915"* 相关的 bug：试图通过 pyxis SLURM 运行该镜像时会发生硬崩溃。根源于该 docker 镜像某些层的权限处理方式，导致层与层之间发生权限冲突。AMD 团队正在研究如何永久修复并防止此类错误再次发生。

7 月时，当我们尝试在 AMD GPU 上为 SGLang 启用 AITER，由于 DeepSeek V3 的编译过程缓慢，整个流程耗时是平常的 10 倍（总计约 30 分钟）（[GitHub issue 在此](https://github.com/sgl-project/sglang/issues/7826)）。这个问题最终在后续版本中解决，目前已修复。

## GitHub Action CI/CD bug

GitHub Actions 的[自托管 runner](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners) 支持为我们在 InferenceMAX™ 中想要运行的基准测试提供了直接的解决方案。集成搭建很快，并允许我们在各种 GPU 集群上运行可复现的工作流，无需自建基础设施。然而，随着 InferenceMAX™ 扩大到包含更多 job，GitHub Actions 的一些局限暴露出来。

每个基准测试变体作为一个独立 job 运行。对每个模型，我们对以下维度的不同组合做基准测试：不同 GPU、输入/输出序列长度、精度、张量并行度和并发度。随着配置增多，每个工作流的 job 数量出现[组合爆炸](https://en.wikipedia.org/wiki/Combinatorial_explosion)。

举例说明：InferenceMAX™ 目前对 3 个模型、最多 7 种 GPU 类型、3 组不同的 ISL/OSL（输入/输出序列长度）组合、2 种精度设置以及各约 4 种并发与张量并行选项进行基准测试。并非每个模型都用到所有可能配置，但按最坏情况估算：3 × 7 × 3 × 2 × 4 × 4 = 2016 个不同的 job。在这个规模下，GitHub Actions 的工作流可视化触到了限制：服务器尝试渲染 DAG 时十秒即超时，报出[错误信息](https://github.com/503.html)。这使调试运行变得极其困难。我们的解决办法是把原来单一的每夜工作流拆成三个，按 ISL/OSL 组合拆分。这样每个工作流的 job 数从约 1500 降到 500，服务器看来能稳定处理。

另一个 bug 与使用 [download-artifacts@v5](https://github.com/actions/download-artifact) action 时的硬限制有关。在每轮完整扫描工作流结束时，会有一个 job 收集并汇总所有 job 的性能结果，这些结果以工作流 artifact 的形式存储。收集过程会调用 download-artifacts@v5 action。它会初始化一个 [artifact client](https://github.com/actions/toolkit/blob/main/packages/artifact/src/internal/client.ts)，后者再调用一个[列出 artifact 的函数](https://github.com/actions/toolkit/blob/main/packages/artifact/src/internal/find/list-artifacts.ts)（需要先列出所有 artifact 再做模式匹配以找到请求的那个），该函数出于「性能原因」强制设置了 1000 的硬上限。据称当客户端尝试列出超过 1000 个 artifact 时应打印警告，但我们从未观察到这一行为。

![](https://substack-post-media.s3.amazonaws.com/public/images/44f22920-4b5c-4e9c-9606-bd0199e77bd0_2351x1121.png)
*来源：GitHub*

感谢 Scott Guthrie 把我们引荐给 GitHub 的相关团队，也感谢这些团队成员帮助我们为这些 bug 实施临时变通方案。我们期待继续使用 GitHub Actions，打造开源世界里规模最大的 GPU CI/CD 集群之一。

## 对 NVIDIA 和 AMD 的建议

尽管大量用户和 GPU 运行在 SGLang 和 vLLM 上，NVIDIA 却把大多数推理工程师分配到了 TensorRT-LLM 上，投入 SGLang 和 vLLM 支持的工程资源相对很少。我们建议 Jensen 把更多推理工程资源投入到支持和贡献 vLLM、SGLang 等热门推理引擎上。这将使 NVIDIA 更好地履行其使命——无论用户选择哪个推理引擎，都能加速其工作负载。

此外，如果 NVIDIA 投入更多时间和资源对其 Blackwell 软件做 QA，减少终端用户在这些新平台上把应用跑起来时遇到的 bug 数量，ML 社区都将从中受益。在开发 InferenceMAX™ 的过程中，我们遇到了许多只在 Blackwell 上出现、在 Hopper 或其他平台上不存在的 bug。

在 AMD 这边，我们建议他们减少为达到合理性能而需要手动启用的 ROCm 专属标志数量。AMD 已认识到这一点，并已着手确保优化配置默认生效。事实上，许多减少所需标志数量的改动已经合入 master。

我们对 NVIDIA 的 Blackwell 平台提出了同样的建议，并建议 NVIDIA 朝着减少达到合理性能所需标志数量的方向努力，转向[默认启用](https://github.com/vllm-project/vllm/pull/25924)[性能优化](https://github.com/vllm-project/vllm/issues/25689)。

## InferenceMAX™ 的下一步

未来几个月，我们将通过集成 Google TPU 和 Amazon Trainium 扩展 InferenceMAX™ 的硬件覆盖，并计划在未来两个月内上线。这将实现 AMD、NVIDIA、Google 和 AWS 加速器之间统一的、可 apples-to-apples 直接对比的比较。这是让 InferenceMAX™ 成为面向全行业的完全跨厂商开放基准测试平台的重要一步。

此外，我们还在启动另一项举措：对 FP4 模型进行包含 MATH-500 和 GPQA-Diamond 在内的每夜评测（evals），让社区能以一致、透明的方式衡量吞吐与质量的权衡。这将有助于凸显低精度推理对各类模型家族与部署场景准确率的影响。另外，我们还将追踪输出 token 吞吐，以生成更深入的洞察。

在 NVIDIA 和 AMD 系统方面，多项令人兴奋的工作正在进行。我们正在 MI300 和 MI355 系列 GPU 以及 B200 GPU 上测试 DeepSeek 的分离式预填充 + 多节点专家并行配置，检验这些先进并行优化在推理负载上的扩展性。与此同时，我们迫不及待想测试 HGX B300 Blackwell Ultra 与 GB300 NVL72 Blackwell Ultra，看看它们相对 GB200 NVL72 能带来多少性能提升。

InferenceMAX™ 并不完美，但我们坚信自己正朝着正确的方向前进——打造一个与 AI 软件进步速度同步的基准测试，并将持续整合 AI 芯片厂商、前沿实验室和加速器大型用户的反馈。

接下来，我们将深入拆解 InferenceMAX v1 当前所用 GPU（如 H100、H200、B200、GB200 NVL72、MI300X、MI325X、MI355X）TCO 的各个组成部分。

## 超大规模云厂商总拥有成本——Hopper、Blackwell、GB200 NVL72、MI300X、MI325X、MI355X
