---
title: "ClusterMAX 3.0：业界标准的 GPU 云评级体系回归"
title_en: "ClusterMAX 3.0: The Industry Standard GPU Cloud Rating System Returns"
subtitle: "事无巨细：可靠性、性能、支持、定价——当然还有安全——这是我们迄今对全球 GPU 云厂商最彻底的一次分析"
date: 2026-09-23
source: https://newsletter.semianalysis.com/p/clustermax-30-the-industry-standard
crawled: 2026-09-15
authors: ["Jordan Nanos", "Sam Harshe", "Samuel Kruse", "Pratt Bhatt", "Billy Cao", "Jack Carson", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-23
---

# ClusterMAX 3.0：业界标准的 GPU 云评级体系回归

> 原文：[ClusterMAX 3.0: The Industry Standard GPU Cloud Rating System Returns](https://newsletter.semianalysis.com/p/clustermax-30-the-industry-standard) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**事无巨细：可靠性、性能、支持、定价——当然还有安全——这是我们迄今对全球 GPU 云厂商最彻底的一次分析**

距离 ClusterMAX 上一次大版本发布已过去 8 个月，垂涎三尺的投资者们几乎已经找不出还能塞支票的口袋，GPU 供给也已归零。与此同时，我们一直在埋头把各家集群往死里折腾。

几周前，我们用几段限制级（R 级）轶事为这份报告预热——它们来自我们探测各家新兴 GPU 云（neocloud）安全实践的亲身经历——还引得一家你多半听说过的 neocloud 客户发布了公开安全提醒（PSA）。

今天，我们终于完整呈现这次测试的广度与深度——ClusterMAX 3.0 比以往任何一版都更彻底，覆盖计算、网络、存储、编排、UI、监控、支持，以及你能想到要在一朵 GPU 云上检查的几乎一切。我们会讲清楚谁在大单频出、谁的工程师在埋头苦干，以及谁家的集群你在谈判时应该要求附赠一瓶阿司匹林。

事不宜迟，ClusterMAX 3.0 的领奖台如下：

![](https://substack-post-media.s3.amazonaws.com/public/images/b2130ed4-61b4-49a8-98e5-03408801831c_1432x880.png)
*来源：SemiAnalysis ClusterMAX 3.0，2026 年 9 月*
![](https://substack-post-media.s3.amazonaws.com/public/images/d9bb4097-5b9c-4863-a7d1-533dce1fde2a_1258x711.png)
*来源：SemiAnalysis Neocloud 看板，面向我们的 AI Cloud TCO 模型订阅客户开放*

# 结果（执行摘要）

[YouTube](https://youtube.com/@semianalysis?si=4_Vv7QxIgISst4Rn) 总结视频与播客讨论即将上线！

- ClusterMAX 3.0 首发即带来对 neocloud 行业的全面测评，覆盖 77 家厂商。
- 我们将市场观察范围扩大到 323 家厂商，高于 [ClusterMAX 2.0](https://newsletter.semianalysis.com/p/clustermax-20-the-industry-standard) 时的 209 家、[ClusterMAX 1.0](https://newsletter.semianalysis.com/p/the-gpu-cloud-clustermax-rating-system-how-to-rent-gpus) 时的 169 家，以及最早那篇 [AI Neocloud Playbook and Anatomy](https://newsletter.semianalysis.com/p/ai-neocloud-playbook-and-anatomy) 文章中的 124 家。
- 作为本研究的一部分，我们累计访谈的 neocloud 终端用户已远超 200 家。
- 我们更新了[横跨 10 大类别的逐条评分标准](https://www.clustermax.ai/criteria)，并更新了对[Slurm、Kubernetes、独立服务器、监控面板与健康检查的预期](https://www.clustermax.ai/expectations)的直接描述。这些内容全部上线在我们的网站上。我们鼓励厂商在开发产品时参考这些清单。我们仍把这些清单视为大量终端用户访谈经验的结晶，它们代表了终端用户期望其云厂商具备的功能特性。
- Nebius 与 CoreWeave 同列白金级。CoreWeave 仍在为全行业树立技术标杆，而 Nebius 如今已确立了能够持续对他人收取溢价的厂商地位。Nebius 一系列漂亮的商业决策，使其能够以卖方价格服务整整一类新兴 AI 实验室（neolab）。
- Google Cloud 与 Oracle 同列黄金级。Azure 降至白银级，Fluidstack 转为「无法测试」，Crusoe 跌至青铜级。Lambda、Firmus 与 TensorWave 留在白银级，GMI 则从青铜级升至白银级。
- 许多公司从白银级（或黄金级）跌至青铜级或更低。我们本轮提高了门槛，全球仅有 19 家 neocloud 获得奖牌评级（Medallion）。
- 我们在青铜级与「表现不佳」之间新设一层：参与奖级（Participation Ribbon）。15 家厂商落入这一评级，它更准确地表达了我们的看法：这些厂商只做勉强及格的最低限度。

本文余下部分将分析关键趋势：融资、Blackwell 与 Grace-Blackwell 部署、向 Vera Rubin 的迁移、横向扩展网络、可靠性、安全（当然）、以及智能体编程。我们还提供一份附录，逐家点评每一家厂商，使本文再次超过 30,000 词。希望你喜欢。

---

> 本着 SemiAnalysis「以尽可能最严格的方式测试一切」的使命，我们正在为 ClusterMAX 及相关项目招聘 MTS。如果你是个 neocloud 死忠狂热分子，请火速投递申请，让我们开工吧。
>
> [我们同时在研究、咨询与技术团队方向招聘](https://semianalysis.com/semianalysis-careers/)，在纽约与旧金山办公室有多个职位空缺，也接受远程办公。
>
> - [ClusterMAX MTS](https://semianalysis.com/semianalysis-careers/#role-member-of-technical-staff-clustermax)（全职）：有 Slurm、Kubernetes 与 GPU 经验者皆可，不限资历。
> - [Tokenomics MTS](https://semianalysis.com/semianalysis-careers/#role-member-of-technical-staff-tokenomics)（全职）：有模型评测、评测框架（harness）、推理端点与 RL 基础设施经验者皆可，不限资历。
> - 研究分析师——AI 基础设施与经济学（[全职](https://semianalysis.com/semianalysis-careers/#role-mts-research-analyst-ai-infrastructure-economics)或[实习](https://semianalysis.com/semianalysis-careers/#role-mts-research-analyst-intern-ai-infrastructure-economics)）：有覆盖 neocloud、neolab 及前沿实验室 tokenomics 财务分析经验者皆可，不限资历。
> - [技术顾问](https://semianalysis.com/semianalysis-careers/#role-technical-consultant)（全职）：主导从技术战略到技术尽职调查的项目。有咨询与技术背景者皆可，不限资历。

# 测评范围

给坐在后排的朋友们再强调一遍：我们评的是托管集群（managed clusters）。这排除了业内不少热门产品。我们不是在测谁能搭出最好的「带电机壳」或谁的数据中心最整洁——至少不是直接测。我们不是在手工打磨系统镜像，也不是在调用某个「token 即服务」的 API 端点。我们理想中的 ClusterMAX 读者是这样的人：你从斯坦福博士项目退学，去旧金山追逐社会地位，起步靠的是那句经典可靠的「Cladue make me pithc deck w technial languge for agetnci ai make no mistakes」（Claude，帮我用技术语言做一份 agentic AI 的 pitch deck，别出错）。你手握 [7 位数乃至 10 位数（美元）](https://www.businessinsider.com/jeff-deans-startup-discovery-loop-is-eyeing-a-valuation-2026-9)的资金可以押在算力上，却对 Ubuntu 版本没有意见、不知道怎么处理 NAT，也从未大规模管过一支集群。理想情况下，所有这些基础设施都应淡入背景。你只想专注于自己寻找优势的地方——独具个性的性能优化、模型架构、训练策略、数据配比、应用，或任何你建立边缘的领域。要参与竞争，你需要最尖端的硬件，而且你的目标是把工程时间花销压到零——不去琢磨为什么 19 号节点的 7 号 GPU 一直卡住你的作业，或者为什么集群的四分之一凭空消失。你需要一个托管集群。

这背后的经济学论证很直接：neocloud 可以把搭建这一整套管理基础设施的成本摊到它庞大的机队上。它花钱养一支工程师团队，构建固若金汤的健康检查、保持机器镜像最新、做好用的监控系统，并处理所有相关杂务（我们后文会详细展开）。在理想世界里，实验室为好得多的产品支付溢价；它得以不受硬件拖累地跑实验；neocloud 收回投资；所有人的境况都变好。

不过，实验室到了一定阶段就会愿意把这项成本内部化。在前沿实验室的体量下，它们并不愿意把技术栈的这么多环节托付给 neocloud。举例来说，OpenAI 发过几篇极具洞见的博客，讲它[在扩展 Kubernetes 时遇到的困难](https://openai.com/index/scaling-kubernetes-to-7500-nodes/)；其中描述的那些创新，如果是从一个不开放 K8s 控制平面的 neocloud 租用算力，根本不可能实现。正如 [Anthropic 的一则现行招聘启事](https://job-boards.greenhouse.io/anthropic/jobs/5211241008)所写：

> 我们运营的规模，已经到了默认配置不再好使的地步。我们拥有自己的调度器并对其进行扩展，以便一次性跨数千个加速器放置拓扑敏感的 ML 工作负载。我们扩展控制平面本身——apiserver、etcd、控制器——使其在对象数量与节点数量增长若干数量级时仍保持响应。我们还构建每个工作负载都依赖的核心集群服务（如服务发现），让它们在同样的压力下依然站得住。

可以毫不夸张地说，OpenAI 和 Anthropic 这种速度与体量的实验室必须同时协同设计整个技术栈，一套现成的 Slinky 实现——哪怕是很好的实现——也远远不够。

前沿实验室在管理基础设施上的显性用心，恰恰说明了 ClusterMAX 的意义。截至我们上次核查，OpenAI 与 Anthropic 公开职位描述中含「Kubernetes」一词的薪资区间总和为 **$27,769,274-$42,687,654**，这还不算它们已有的庞大团队拿的薪水。如果你没在指望一场万亿美元级的流动性事件，又需要足够好的基础设施来给自己一个翻身的机会，你就需要一家 neocloud 替你扛下重活。

至少在纸面上，较小的 neocloud 客户是以大卫之姿对抗歌利亚。OpenAI 与 Anthropic 在各自的~~逻辑斯蒂~~指数增长曲线上保持着惊人增速，而我们的[数据中心行业模型](https://semianalysis.com/datacenter-industry-model/)目前预计，到 2027 年底它们将占全部实验室算力的 56.3%。

![](https://substack-post-media.s3.amazonaws.com/public/images/d167da3e-8fe2-4d65-b6f2-c3c226d7ebad_2100x758.png)
*OpenAI 算力容量。来源：SemiAnalysis Tokenomics 模型。*

正如我们后文更详细描述的，融资还带来一种马太效应：盈利的前沿实验室比小实验室更容易锁定产能，后者被迫接受高额预付款、更差的价格，也更难提前数年做规划。

这是否意味着托管集群已死？cLUsTerMaX 凉了？事实上，尽管 Anthropic 与 OpenAI 逐年吃掉更大的份额，托管集群作为一门生意仍在指数增长。我们帮过无数实验室找算力，还有无数实验室正在寻货、愿意付钱、等待新产能上线。Anthropic 与 OpenAI 是最大的客户，但还有一条长尾——单笔「仅仅」数亿美元的交易所汇聚起来的总价值是巨大的。

托管集群相对前沿实验室裸金属扩大份额的一个可能情景，与开源模型的进展有关。服务开源模型的利润已经比许多人意识到的更丰厚；我们最近建模分析了「[卖开源 token 每年每 MW 可以赚超过 1 亿美元](https://semianalysis.com/institutional/you-can-make-over-100m-per-mw-per-year-selling-open-source-tokens/)」，即便按今天的租金也留足了利润空间。可以想象开源模型提高市场份额——无论是因为边际采用者对成本更敏感，还是算法进步缩小了与闭源的差距。无论动力机制如何，这都会提升托管集群的相对地位。供给侧几乎任何一道裂缝，都会让实验室稍微不那么愿意自担基础设施、稍微更愿意依赖 neocloud。

这些集群之上的各层正在快速成熟，但它们不在 ClusterMAX 的测评范围内。有几个细分方向值得考虑：推理端点（inference endpoint），分公开与私有，按 token 计费；后训练服务，为特定用例定制开源模型；还有沙箱服务，为智能体（尤其在 RL rollout 期间）提供基础设施，简化并优化容器与 CPU 管理。这些都宽泛地归入「GPU 服务」，边界常常模糊。例如，一家云可能先用闲余容量起一个推理端点，或既对外提供沙箱基础设施、又在对内支撑自家销售的 RLaaS。我们近期会发布更多相关内容，但它超出了本报告的范围。

# 测试方法论

在 ClusterMAX 3.0 中，我们向每家厂商申请了如下资源：

- 32 张 GPU（4 台 8 卡 HGX 节点，或 8 台 4 卡 NVL72 节点）
- 高带宽网络（我们提出 800G RoCE 或 XDR InfiniBand，但许多厂商尚未就绪）
- 10TB+ 高性能文件存储（支持 NFS/POSIX 挂载，以及通过 CSI 驱动提供 RWX StorageClass）
- 10TB+ 兼容 S3 协议的对象存储
- 一个监控面板（通常基于 Grafana）
- 5 天测 Slurm，5 天测 K8s（可并行——在一个 SonK（Slurm on Kubernetes）集群上——或顺序进行，如果厂商想收回节点重新部署）
- NVIDIA 侧要求 Blackwell 而非 Hopper（B200、B300、GB200、GB300 均可接受），AMD 侧接受 MI355X。H100 如今已经 4 岁多了！

我们分 3 个阶段测试集群，具体如下。当然，我们始终会联系这些厂商的客户、听取其反馈，作为对实测的补充。

## 阶段 1：审计（Audit）

首先，审计覆盖一批「是/否」问题。集群设置是否正确？软件是否已安装？是否为最新版本？各项实用工具是否符合预期？跑一遍约需 15 分钟。它可在 [GitHub](https://github.com/SemiAnalysisAI/ClusterMAX) 获取，或通过 **{uv} pip install clustermax** 安装。

审计在我们给集群上负载之前检查配置。它覆盖硬件清单、软件与固件版本、GPU 访问、容器、调度器配置、网络、存储、健康监控与安全。我们会检查哪些组件适用于被测环境，并对全部检查项给出通过、警告、失败与跳过的标记。这一部分我们免费公开并将长期维护。其余部分暂不外发。

## 阶段 2：性能（Performance）

性能阶段对集群各组件及集群整体的性能特征设置通过/失败阈值。通过微基准与真实世界基准完成。

具体而言，我们测试：

- GPU 计算
- 网络
- 存储
- 生命周期
- 训练
- 推理

下文将更详细地解释，但请注意我们的测试内容会随时间演进。

### GPU 计算

我们先检查 GPU 的真实 GEMM 性能。GEMM 是现代 AI 工作负载中最关键的运算——这一点我们已经讲过很多次——而分组 GEMM（Grouped GEMM）对现代 MoE 模型尤为重要。

我们在 cuBLASLt（或 hipBLASLt）与 DeepGEMM 上测试分组 GEMM，覆盖多种精度：BF16、FP16、TF32、FP32、FP8 E4M3、MXFP8 与 NVFP4，视集群中芯片支持情况而定。我们使用一组统一的形状，在 Kimi K2.5、K3 与 DeepSeek V3、V4 Pro 模型的不同 gate_up 与 down 投影、不同 batch size 下测试。

随后我们测试 GEMM、GEMV 带宽，以及 MAMF（Maximum Achievable Matmul FLOPS，来自 [Stas Bekman](https://github.com/stas00/ml-engineering/tree/master/compute/accelerator/benchmarks)）——它在每张 GPU 上按精度各扫一段时间，使用 cuBLASLt（或 rocBLAS）。我们报告所有 GEMM 测试的 FLOPs。

![](https://substack-post-media.s3.amazonaws.com/public/images/7a2db658-0ea7-4ef5-acfb-5b8db57913e5_829x781.png)
*来源：SemiAnalysis ClusterMAX 结果看板*
![](https://substack-post-media.s3.amazonaws.com/public/images/4d603db1-709e-4fad-a1e4-d1bc4f5ea8f0_829x778.png)
*来源：SemiAnalysis ClusterMAX 结果看板*

我们还通过 GEMV 测试与 **nvbandwidth** 测试内存。GEMV 用一个瘦向量做矩阵-向量乘法，以 GB/s 为单位报告，作为低批次解码流式行为的代理指标。NVIDIA 的 `nvbandwidth` 工具内置于 DCGM 健康检查，测量 h2d（CPU 到 GPU）、d2d（GPU 到 GPU）与 d2h（GPU 到 CPU）带宽。最后，我们还有自定义 PyTorch 脚本，通过实际的张量拷贝测量同样的路径，记录 pinned h2d、d2h 与本地 HBM 拷贝的带宽。

最后，我们为老派玩家（boomers）测一下 HPL-MxP。HPL-MxP 用低精度分解求解大型稠密线性方程组，意味着计算、内存与通信被同时打满。该测试在单个工作负载中覆盖计算、HBM、横向扩展网络上的 MPI 广播、NVLink 与数值正确性。我们按芯片类型在多种数字格式下报告 FLOPs。

尽管 GEMM 是现代 AI 工作负载的核心，这些微基准却极少能拉开厂商差距——想把这类功能搞砸都难。重要的是在后文描述的长时间烤机中检验原始 GEMM 性能：如果散热不当，芯片可能降频以避免过热。在一次 GEMM 突发测试里，你不太可能发现什么值得注意的东西。我们在每家厂商都跑这些测试，因为它们很快，而且一旦失败集群立刻不可用，但我们更担心的是其他测试。

### 生命周期

为了理解集群在整个生命周期中的易用性，我们设计了一套刻意的测试。先以多种方式（下载/上传主要走 Cloudflare）检查互联网速度。然后测试通过 **pip** 与 **uv** 安装 PyTorch、vLLM 等常用包所需的时间，以及从 Docker Hub、ghcr.io 和 [nvcr.io](http://nvcr.io) 下载容器、从 Hugging Face 与 ModelScope 拉取模型所需的时间。

随后我们在每个可用存储层（home、共享文件系统、本地 NVMe scratch 以及任何额外挂载点——即 `/home`、`/data`、`/scratch` 等）上以全新包缓存重做 **pip** 与 **uv** 的 **install** 测试，再从每个位置运行 `import torch` 看耗时。在大多数厂商那里这只要 1-2 秒，但在一些存在 LOSF（海量小文件）性能问题的文件系统上，居然能拖到 10-20 秒。

最后，我们拿先前下载的模型，运行 **vllm serve** 命令，测试到能访问 /v1/models 为止的时间。同样，某些厂商能在 10-40 秒内从共享存储把一个小模型加载进 GPU 内存，而有些厂商要超过 2 分钟。

![](https://substack-post-media.s3.amazonaws.com/public/images/5cc822c9-bfcc-4b35-85bb-031a385dc56d_783x474.png)
*来源：SemiAnalysis ClusterMAX 结果看板*

### 网络

我们对节点间与节点内传输跑一套宽泛的通信性能基准。包括 MPI 集合通信、通过 MPI 启动的 NCCL 或 RCCL 测试，在 8 B 到 16 GB 的消息大小上测量 all-to-all、all-reduce、all-gather 及其他集合操作的带宽与时延。同样的工作负载也通过 PyTorch 的 **torch.distributed** 运行。此外，我们使用 RDMA perftest（具体为 **ib_write_bw** 与 **ib_read_bw**），逐条网络轨道（rail）测量点对点带宽，连同主机内存兜底路径（经 PCIe），以定位任何问题。

我们以 2 的倍数逐步扩大 world size 直到用满整个集群，并跟踪性能的扩展情况。我们还做禁用 NVLink 的测试（尤其在 GB200 或 GB300 NVL72 集群上），以隔离横向扩展网络的性能。这里做账必须小心，因为 world size、算法以及作业相对横向扩展边界的摆放都会实质性地影响结果。

![](https://substack-post-media.s3.amazonaws.com/public/images/49e7f132-bc0e-43f9-9ad2-e569bff872e9_1654x186.png)
*来源：快速检查集群网络栈开箱支持哪些特性*
![](https://substack-post-media.s3.amazonaws.com/public/images/d1712792-316c-44f0-a33c-3e3014dde8c5_739x829.png)
*来源：SemiAnalysis ClusterMAX 结果看板*
![](https://substack-post-media.s3.amazonaws.com/public/images/c38eaf49-3d21-47bb-aaac-5ccf43c614b8_733x915.png)
*来源：SemiAnalysis ClusterMAX 结果看板*

### 存储

我们运行 fio、ior、Elbencho、一个用 Torch 与 Torch DCP 编写的自定义检查点保存/加载基准，以及一个由 [Skild AI](https://www.skild.ai/) 分享给我们的自定义 datagen 基准。datagen 大概是最有意思的，它逼近其机器人数据管线中的真实工作负载：生成视频（MP4）与 parquet 传感器数据集的聚合写入吞吐。

不过发现问题最多的，还是老老实实的 fio。我们扫描带缓冲/直接 I/O 的顺序/随机读写，使用 1MiB 顺序块与 4 KiB 缓冲 / 64 KiB 直接随机块，客户端数从 c1 一路加到 c32；如果节点数超过 4，就加到集群能承受的最多客户端。只要存储配置有任何差错，fio 扫描几乎总有某个设置会暴露出糟糕的性能。我们跟踪吞吐、IOPS 与时延，当然，如果测试在客户端过多时失败，我们还会顺带发现元数据的不一致。

![](https://substack-post-media.s3.amazonaws.com/public/images/e9e56d45-b74d-4d51-8f3c-5b5ba1b33a35_734x749.png)
*来源：SemiAnalysis ClusterMAX 结果看板*

当然，这在很大程度上取决于分给我们的卷有多大、SLO 如何定义。这些结果要打个折扣看——上面这张图其实只能说明 Azure 给了我们一个 PB 级挂载。这个「折扣」也说明为什么掌握大量集群的数据很重要。比如缓冲测试的时延更高（你可能也料到了），而且若测试跑得不够久，结果会非常嘈杂。但到底高多少、多嘈杂？要知道「够好」与「需要向厂商拉警报」的区别，与一个庞大的同侪集做对比至关重要。

对象存储方面，我们对着一个 S3 桶再跑一遍这套测试。我们还运行自定义基准，测量大对象顺序读/写吞吐、小对象 PUT 与 GET 速率、以及读时延（p50、p90、p99）。在这类测试中我们保持一切条件一致。当然，一如既往，若发现某个集群在某类工作负载上吃力，我们就会驻留更久，跑更多测试以更精确地隔离问题。

### 训练

进入真实世界，网络或存储上的问题开始在实际测试中显形。我们通过 torchtitan 跑两个作业：在 C4 数据集上以 FSDP 预训练 llama 3.1 8B，以及通过 torchtitan 带专家并行训练 GPT-OSS MoE。前者受 FLOPs 限制，后者受集合通信限制（除非你在 NVL72 上）。因此，后者能让网络的问题一目了然。

![](https://substack-post-media.s3.amazonaws.com/public/images/6fa1e9ed-5b12-4623-ac2a-0ee2a63462a5_740x714.png)
*来源：ClusterMAX 结果看板*
![](https://substack-post-media.s3.amazonaws.com/public/images/321be736-0b73-4b6a-b7ba-ba6fe06c960c_734x772.png)
*来源：ClusterMAX 结果看板*

### 推理

我们在单节点与多节点场景下、用不同模型运行 InferenceX [AgentX 基准](https://inferencex.semianalysis.com/agentx)，找出受算力限制、受内存限制与受通信限制的状态，并开启 profiling 追踪，以 InferenceX 结果作为对比的基准性能。与训练测试一样，这凸显了微基准所覆盖的各类集群组件的重要性。如果一个集群连 NCCL 测试都扛不住，它肯定也产不出多少 token，而我们的 InferenceX 测试会展示有效吞吐（goodput）是如何流失的。

## 阶段 3：可靠性（Reliability）

基准测试中看到扎实的性能，并不意味着厂商能撑起扎实的[有效吞吐](https://newsletter.semianalysis.com/p/how-much-do-gpu-clusters-really-cost)，更不意味着他们会带来舒心的支持体验。因此，我们以多种方式测试可靠性、监控与自动修复（autoremediation）。

### 烤机（Burn-in）

我们先对 GPU 与网络做 8 小时烤机：在张量核心上同时跑大型 GEMM 与 all-to-all 通信，监控脚本跟踪温度、功率、时钟频率、FLOPs、网络连通性、时延、带宽，当然还持续追踪内核环形缓冲区里的任何错误。你会震惊于这个简单测试能诱发出多少硬件问题。**必须同时压测 GPU 与网络，这一点怎么强调都不为过。**烤机要求这两类组件同时经历热胀冷缩，才能逼近真实工作负载下的真实压力行为。许多厂商仍在使用 GPU 与网络分开烤的脚本。

### 网络 fabric

接下来，我们循环运行大消息的 all-to-all、all-gather 与 reduce-scatter，测试横向扩展与纵向扩展网络 fabric 的持续性能。我们报告平均、最小与最大带宽，外加集合通信错误。在前端网络上，我们还测试四个节点之间每个有向对的管理网丢包、RTT 与 TCP 带宽。这项附加测试抓到烤机漏掉的错误的次数不多，但我们喜欢这份数据，而且它曾揭示某些以太网在高负载下的巨大性能差异。

### 存储

继续，我们用 fio（如前所述）在每个客户端数量上测试文件系统耐力：先跑 7.5 分钟顺序混合读写，再跑 7.5 分钟随机混合读写。我们逐步增加客户端数，报告带宽随时间的变化、IOPS、尾时延与性能衰减。有意思的是，我们看到过一些厂商在高负载下相比初始基准带宽衰减接近 40%。

对象存储可用时，我们还会跑 15 分钟 PUT、GET、LIST 与 DELETE 混合负载，测量吞吐衰减、p99 GET 首字节时间漂移、限流与错误。我们在这些测试中见过约 10% 的差异。

### 编排

在 Kubernetes 上，我们通过反复创建/删除 GPU pod 并向 API 查询 GPU 分配情况来测试「扰动（churn）」。我们同时报告调度时延与启动时延，并在 **kubectl delete po** 卡住时记为失败。我们还逐批增加纯 CPU 沙箱 pod，测量多少个到达 Ready、耗时多久、以及其余的为何停留在 Pending。

最后，我们反复启动一个挂载卷、写入并 fsync 一个文件、然后被删除的 pod，以此测试 PVC 生命周期。我们在每轮之间等待拆除完成，并用一轮预热把首次镜像拉取从计时中剔除。

### 破坏性测试

终于到了最好玩的部分：故意搞破坏。

首先，我们重启集群中的所有节点。你希望这不是破坏性测试，但它就是。在 Kubernetes 上，我们先 cordon 并 drain 节点、发出重启命令、要求 boot ID 发生变化，然后等待它回到集群。计时在我们能于该节点上的全新 pod 中运行 **nvidia-smi** 时停止。在 Slurm 上，我们直接拿到分配或 SSH 后运行 **sudo reboot**。Slurm-on-Kubernetes 稍有不同，因此我们尽量从 Kubernetes 层操作以正确测试它。我们的脚本全程计时。

注入故障时，我们先用 DCGM 注入方法。如果不好使，我们就往内核日志里写一条合成的 NVIDIA XID 或 SXID 消息，观察厂商现有的健康检查与调度器如何响应。我们不动它们的健康代理与 drain 自动化，检测错误并采取行动就看它们自己的工具链。大多数健康检查从内核环形缓冲区读取，但有些不是，因此我们会与厂商沟通，确保我们的触发机制有效、且我们有权限拉取。作为最后的可靠手段，我们重置 GPU 的上游 PCIe 桥，产生一条货真价实的 XID 79。

在所有这些场景中，我们计时：检测故障耗时多久、节点在 `DRAIN` 状态停留多久、回到集群后运行一条基本命令耗时多久。在 AMD 系统上，我们注入一条 UMC RAS 错误并以相同方式跟踪。

这是我们最关键的测试。凡是听到大量客户抱怨可靠性的厂商，普遍没有把健康检查、监控面板与自动修复建立起来。可靠性是全球许多最大客户眼中第一重要的标准，我们在《[GPU 集群的真实成本](https://newsletter.semianalysis.com/p/how-much-do-gpu-clusters-really-cost)》一文中详细讨论过。

![](https://substack-post-media.s3.amazonaws.com/public/images/fa331e4d-ca20-4efb-a547-4c4b45f38fd8_923x756.png)
*来源：ClusterMAX 结果看板*

值得指出的是，动手实测只是总评级的一部分。有许多东西我们无法亲手测到，需要用其他研究方法细致了解，即：大规模下的性能、长期可靠性、支持体验、定价、GPU 可得性与交付时间线。

## 即将推出：智能体工作负载与 RL

我们还有两套测试套件，将在后续工作中详细介绍。

## CPU 计算

CPU 是现代智能体工作负载的关键性能因素，我们此前讨论过。我们开发了一套全面的基准，在一个即将推出的项目 SandboX 中，通过常见 Linux 工具使用与更多微基准，把 CPU 性能在这些智能体工作负载上逼到极限。

SandboX 运行一系列有代表性的代码执行类 CPU 密集工作负载，包括环形洗牌的生产者-消费者队列、Redpanda（测量本地 Kafka 兼容消息代理及其吞吐）以及一个动态负载压测。

我们还对 Kubernetes 集群做沙箱生命周期基准，以了解在 GPU 集群剩余 CPU/内存资源上混部 RL 沙箱的可行性。我们报告冷启动时延、调度吞吐、每节点密度、容量与基线。

### 强化学习（RL）

一次 RL 运行有很多活动部件：展开轨迹的生成器、在沙箱中执行动作的环境、以及接收 rollout、更新策略并把更新后的权重推回推理引擎的训练器。扩展 RL 意味着在训练器、推理引擎、环境沙箱执行、rollout 传输、权重同步等的利用率最大化之间做平衡，任何一环成为瓶颈都可能卡住整个 RL 栈。

我们还看到后训练即服务（Post-Training-as-a-Service，RLaaS）的兴起：客户自带环境（或由前置部署的工程师搭建），托管训练厂商搭建基础设施来后训练开放权重模型。卖点是既定制化又保护客户 IP——这话如今俨然成了 Satya 的口号。

在即将推出的 PostTrainingX 基准中，我们扫描训练器与推理的 GPU 配比、batch size、rollout 并发与策略陈旧度（policy-staleness）限制，研究它们对性能与训练稳定性的影响。

我们通过每张推理 GPU 的每秒输入/输出 token 数、rollout 时延、KV 缓存占用与前置缓存命中率来跟踪生成器性能；通过权重同步时延、传输带宽与网络遥测来跟踪通信效率；通过训练吞吐、优化器步长时间、MFU、训练/rollout KL、观测到的策略陈旧度、裁剪比例、梯度范数与被拒绝的 rollout 来跟踪训练器性能与稳定性。

对于环境，我们测量搭建时间、工具执行时间、超时与基础设施故障。GPU 利用率、内存占用与功耗提供系统级上下文，而归档的轨迹、日志与精确的环境定义让结果可复现。

![](https://substack-post-media.s3.amazonaws.com/public/images/58068806-a29a-439d-b8a2-a8e071d42102_908x772.png)

PostTrainingX 的目标是对每家厂商做基准测试，包括 Applied Compute、Azure Foundry、Fireworks、Thinky、Baseten、Trajectory、Engram、AI21 平台等托管训练平台，以及 Miles、slime、prime-rl、verl 等开源框架。最终结果应能给客户数据，来决定是在开源框架上自建后训练栈，还是交给托管 RL 厂商。

我们已经开始在开源框架（包括 Miles、prime-rl 与 verl）上运行，下一步将扩展到托管厂商。敬请期待……

# 行业趋势

## 融资

过去几个月 neocloud 圈最热的话题是融资。人人都想「跟着钱走」，这正是我们的 AI Compute, Capital, and Markets 模型所做的事——该模型在[最近一篇拆解 NVIDIA「兜底宇宙」的文章](https://newsletter.semianalysis.com/p/nvidias-backstop-universe-heads-i)中发布。下面我们再讨论几个热点。

### 债务与获取债务融资

如今，neocloud 们意识到，一份信用良好的客户合同能帮助它们以低于自身评级的利率获得债务。这意味着没有确定性客户（或称「投资级承购方（IG offtaker）」）的厂商，可能需要更昂贵的债务或类股权资本来购买 GPU、起步或扩张。与此同时，出借方也需要证据证明厂商能按时交付集群并履行客户合同中的 SLA。能否举债，既取决于可用于偿债的现金与合同总价值（TCV），也同样取决于租约终止权。这促使多家保险公司带着参数化保险产品进入市场，保护 neocloud 及其出借方免受合同终止的冲击——典型设计是在终止事件发生时提供一个月的过渡期以寻找新承购方。我们非常喜欢这个结构，认为这是出借方为这类交易去风险的扎实手段。

### 交易对手风险与 Nvidia 的「资产负债表即服务」

在一个大型 neocloud 项目中，GPU 出借方与数据中心出借方在同一项目内面对的交易对手可能不同。例如在 Anthropic TPU neocloud 结构中，Broadcom 支持设备融资，而 Google 支持数据中心租金。由于供应链中多笔贷款可能依赖同一家 AI 实验室，即便每笔贷款名义上的借款人是不同的 neocloud 或数据中心，也存在系统性、相关联的风险。正如我们刚讨论的，建设延期可能触发合同取消并损害现金流。

于是有了 Nvidia 的兜底。由于 Nvidia 通过收入下限（revenue floor）、业主担保以及计划转让给第三方的租约来支撑 GPU 需求，它们能够帮助 neocloud 与 AI 实验室在没有超大规模云厂商参与的情况下获得投资级融资。Nvidia 在首次销售时赚取 GPU 毛利，如今还能在其「AICP 下限」之上分得一部分收入。因此，其金融支持直接拉动其硬件需求。资产负债表就是护城河（The Balance Sheet Is The Moat）。

### 折旧时间表

自去年 11 月我们[撰文炮轰 Burry 博士](https://newsletter.semianalysis.com/i/178649945/depreciation-schedules-and-the-future-of-gpus-in-azure)以来，这个话题热度略有下降。也许是因为大家都在签 6 年期合同，也许是因为那些 4 岁高龄却死不降价的 H100！谁知道呢。

无论如何，我们在建模折旧时把设备采购日期与投用日期分开处理。6 年折旧假设需要厂商特定的依据支撑，而在 NVIDIA 的 AICP 计划中，6 年收入下限并不能真正确立 GPU 的使用寿命。我们的折旧敏感性测试会显著改变建模利润率，但出借方优先看 IRR，所以我们不在此公布。当然，财务分析并不能确立未来买家为 GPU 支付的真实价格——那取决于供需动态与终极问题：残值。由于出借方无法把贷款偿还计划与我们用于设备折旧的会计假设剥离开，我们仍困在一个没有人愿意为 4、5、6 年机龄的 GB300 评估残值的世界里。

## Blackwell 与 Grace Blackwell

现在回到本文余下部分的技术内容。好戏来了。

正如我们在 [ClusterMAX 2.0 中详细讨论的](https://newsletter.semianalysis.com/i/178057384/gb200-nvl72-reliability-and-slas)，运营 8 卡 H100 HGX 服务器与 GB300 NVL72 机柜级系统之间的差异是巨大的。3-4 年前靠安装 H100 练手的厂商，如今要应对以下这些：

1. 基于 ARM 的 Grace CPU（而非 x86 的 Intel 或 AMD）
2. sm100/sm103 的 Blackwell GPU（需要 CUDA 13.0+）
3. 强制直接液冷（DLC）
4. 高压供电（每机柜 130kW+，通过三相 408 或 480V 供电）
5. 横向扩展网络：800G CX-8 NIC 配 51.2T 或 102.4T（800GbE RoCE Spectrum-X）或 115.2T 交换机（800Gb XDR InfiniBand）
6. 纵向扩展网络：机柜级 NVLink 交换机与背板，72 卡互联
7. 前端（或前端/存储融合）网络的 BF-3 或 BF-4 DPU
8. 带 shuffle 板/shuffle 线缆的多平面（multiplanar）网络

所有这些变化都会影响部署软件、监控系统、技术员培训、设施级电气/制冷/机械系统、OEM 支持合同与关系等等。

一家厂商在 Hopper 世代成功，并不意味着它在 Blackwell 世代也会成功。

在我们的评级中，对任何把 Grace Blackwell 交付给我们的厂商都给予加分，而且坦率地说，在部署、监控与可靠性/热备方面的困难上给了它们多得多的宽容。

这意味着，如果客户租用的是仅靠 RoCE 或 InfiniBand 连接的标准 HGX 节点，我们期望看到有热备节点可用的自动修复：端到端 1 小时内完成更换、约 2 分钟内完成检测。但对 NVL72 系统而言，在另一个纵向扩展 fabric 上热插拔一个托盘是没有意义的。

因此在我们的测试中，只要健康检查（仍要求 2 分钟或更短时间内）发现了不健康的节点、并阻止工作负载再被调度上去，它就尽了本分。如上所述，我们为许多实验室和云提供 GB300 NVL72 SLA 建议，最常见的模式可以叫「NVL64+」：即 SLA 施加到每个节点，但当一台机柜的 18 个节点中同一时刻有 3 个或更多故障时，整柜视为宕机。原因很简单，就是 2 的幂：大量作业能被 64 整除、跑在 64 张 GPU 上，而填满 72 张 GPU 的最大配置是 world_size=8 * num_jobs=9。

## 迁移到 Vera Rubin

有意思的是，从 Grace Blackwell 迁到 Vera Rubin所需的变化，远少于从 Hopper 到 Blackwell。厂商管理的仍是 Arm CPU、液冷机柜级架构、72 卡 NVLink 纵向扩展网络、多平面横向扩展网络以及一些 Bluefield DPU。而当年 GB200 面世时，这一切都是全新的！

主要变化在于横向扩展网络从 800G CX-8 NIC 升级到 1.6T CX-9 NIC，以及机柜功率从约 130kW 提高到约 200kW，包括 [800V DC 方案](https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part)。

早期需求比 Blackwell 世代切换时更强劲——部分原因是[把 GB 软件移植到 VR，比当年从 Hopper 到 GB 容易](https://newsletter.semianalysis.com/p/vera-rubin-nvl72-vs-gb200-nvl72-inference)——而且**我们从许多厂商那里听到，他们有望比原计划更早交付 VR**。点亮（bring up）过程出奇地顺利，物理设计似乎也成熟得多。

## 横向扩展网络

横向扩展网络是厂商仍能自己做主的最后一个大型设计决策。Nvidia 与 OEM/ODM 锁定了 NVL72 机柜的大部分。在机柜之外，厂商自行选择拓扑、布线，以及 Kubernetes 或 Slurm 如何把 fabric 交给作业。我们在每一层都发现了问题。

先从物理层说起：800G CX-8 NIC 是多平面的——每张 NIC 的带宽被拆分到若干独立的交换 fabric 上，称为平面（plane）。每 GPU 总带宽保持 800G。平面越多，每台交换机的有效端口越多，每张 NIC 的上联路径也越多，这就需要 shuffle。每条 NIC 通道都必须落到正确的平面上，因此 shuffle 盒把光纤映射放进配线模块，而 shuffle 线缆则把映射做在线缆组件里。两者都可行，但在可靠性（需要多频繁地维护设备）与可维护性（修理或更换设备有多容易）上各有取舍。

Oracle 是这种物理设计的先驱，拿到 GB300 节点时就能看出来。我们拿到的每个 4 GPU 托盘有 16 个物理 200G 端口，即每 GPU 4 个平面。Linux 暴露出 4 个可用的 800G RDMA VF（rdma_vf_rail0 到 rdma_vf_rail3），每 GPU 一个，各在自己的 VRF 里。聚合 PF 失败且没有可用 GID，于是我们只能依赖他们的 SPCX NCCL 插件——每连接 16 个队列对，并跨平面自适应路由。

为什么要这么折腾？答案是规模。Oracle 在此物理设计之上构建了 Acceleron。他们的 MRC 拓扑论文展示了每张 NIC 如何拆成 8x100G，把一台 51.2T 交换机变成 512 个端口，仅用 2 层、最多 3 跳交换，即可支持 131,072 张 GPU 满带宽。OpenAI 于 2026 年 5 月通过 OCP 发布了 MRC，Oracle 则在 Stargate Abilene 上运行它。软件层允许 MRC 把一条连接喷洒到多条路径与平面上、乱序摆放数据、用选择性 ACK 恢复丢包，并用 SRv6 源路由绕开故障或拥塞链路。这个逻辑层在任何规模下都可能变得复杂。作业出问题的地方就在这里。

要分配 RDMA 设备并正确使用它，Kubernetes 必须把正确的设备与接口交给每个 pod。换句话说，NVIDIA NetworkOperator 的配置与使用方式有很多种。配错了，对谁都是灾难。

我们的脚本识别 NetworkOperator 的以下部署模式（资源名取自我们检查过的集群的实例）：

- rdma_shared_device：rdma/rdma_shared_device_* 配资源背书的 NAD，或退化为宿主机网络
- sriov_host_device：nvidia.com/hostdev 或 nvidia.com/rdma_host_dev 配 HostDeviceNetwork NAD，用于直接设备访问与 GPUDirect RDMA
- sriov_legacy：通过 NAD 绑定的 nvidia.com/<resource> 获得 VF 并配 SriovNetwork NAD，必要时再加 RDMA CNI
- sriov_ib：如 nvidia.com/mlnxics 的 InfiniBand VF 配 SriovIBNetwork NAD。分区 fabric 还需要正确的 PKey 与 UFM 配置
- ovs_offload：nvidia.com/switchdev 配 OVSNetwork NAD，用于硬件卸载的 Open vSwitch
- rdma_ib / rdma_roce：rdma/ib、rdma/roce 或 nvidia.com/rdma_*，每条轨道一个 NAD，或退化为宿主机网络
- 厂商特定：AWS EFA（vpc.amazonaws.com/efa 与 libfabric）、DOKS（rdma/fabricN 配 roce-net-fabricN@fabricN）、GKE DRANET（DRA claim 模板与 pod resourceClaims）

设备配置及其上的 NCCL 插件会改变作业性能。在 Google 的 GB300 上，内置 NCCL 库选中了一个不可路由的链路本地 GID，我们一测就挂起。设置 NCCL_IB_GID_INDEX=3 解决了问题，而 Google 的 gIB 插件在 16 节点、16 GiB all-to-all 上达到 99.5 GB/s，对其他厂商是 95.3 GB/s——即跑满性能。

话虽如此，多节点 NVLink 又是另一个问题。NVIDIA DRA 驱动中的 ComputeDomain CRD 让每个作业拥有自己的 IMEX 守护进程与通道声明，独立于 RDMA。Google、GMI 与 Firmus 的 Kubernetes 用了 ComputeDomain，但 RDMA 路径各不相同：Google 用 DRANET，GMI 用宿主机网络的共享设备，Firmus 用每轨道 VF。与此同时，Oracle、Azure Slurm、GMI Slurm、Firmus Slurm 与 Nebius Soperator 从宿主机侧提供 IMEX、无租户声明。Azure AKS 在有 GPU DRA ResourceSlices 的情况下运行多节点 NVLink，却没有租户可见的 ComputeDomain，通道来源与租户隔离边界也无文档说明。

每个 ComputeDomain 必须留在一个 NVLink 域内，因为跨域需要 RDMA。换言之，这是在「纵向扩展 NVLink + 横向扩展 RDMA」层级化网络上的拓扑感知组网。当我们不感知 ComputeDomain、错误地启动作业时，只要摆放跨了机柜，它们就在 clique 建立阶段直接挂起。至于 EFA 不支持 DeepEP 与 MoonEP 的牢骚，我们留到附录的 AWS 厂商点评里再发。

## 可靠性、健康检查、自动修复与 SLA

大约在启动《[GPU 集群的真实成本？](https://newsletter.semianalysis.com/p/how-much-do-gpu-clusters-really-cost)》研究的同时，我们开始向每一个受测集群注入故障。厂商之间的差异巨大。处理一次故障需要两件事：

1. 发现它发生了
2. 妥善修好它

发现故障，我们推荐监控面板。一个好的面板能显示故障组件、受影响的作业、当前调度器状态，以及每项检查上次运行的时间。一个放旧了的绿色结果不是健康的证据。当然，监控面板依赖遥测，所以你必须把 DCGM 配置正确（且安全）。

修复故障，我们期望自动修复：重启并以热备节点替换。自动修复覆盖不了一切。有些故障需要人工介入、RMA 及其他厂商必须直接与客户沟通的工作。我们在此前[关于该主题的文章](https://newsletter.semianalysis.com/p/how-much-do-gpu-clusters-really-cost)中以有效吞吐为单位精确量化了成本。

NVIDIA 最近开源了 NVSentinel——一套面向 Kubernetes 的故障检测与修复系统。它读取 DCGM、syslog 与云维护事件，随后可以 cordon 并 drain 节点、重置 GPU 或重启。默认安装仅监控。软件是容易的部分，重要的是从每个 XID 到厂商动作的映射。受控的（contained）XID 94 需要应用重启；不受控的 XID 95 需要 GPU 恢复。显然，对每个 XID 都无脑重启每个节点，你会杀死健康的工作；而严重 XID 之后仍让 GPU 可被调度，你又冒工作负载崩溃的风险。

这也是许多客户只要裸金属的原因——他们只想让厂商关掉工单。关工单比听起来难。一张工单可能来自 100 多种 XID 中的任何一种，每种含义与解法都不同。SOP 覆盖从换硬盘或电源、清洁线缆、重插内存/GPU/NIC，一直到 RMA 单个部件或整台服务器托盘。

自动修复有很多不同选择，正确的选择取决于系统。而且对 GB 与 HGX 来说，修复是两个不同的问题。在 HGX 上，你换入一台 8 GPU 的热备节点。在 NVL72 上，你无法往 NVLink 域里热插 8 张更多 GPU。一个故障托盘带走 4 张 GPU，选项只有降级运行整柜或整柜更换。好消息是 GB300 往往比 GB200 更少故障。无论哪种，从错误到数据中心动作的流转才是关键。

有些厂商告诉我们，他们会先等一等再行动，给客户留时间把东西从节点上拿走。那是自我安慰（cope）。我们模拟的是硬故障：节点已经死了，没什么可拿的。（一个普遍真理：如果厂商说他们「为了给客户选择权」而选择不做某事，那基本就是 cope，厂商自己承认只是时间问题。）

这正是自持自营数据中心与租用 colo 的分野。自营厂商控制着驻场技术员、备件与 SOP。Colo 里的厂商则依赖业主的 remote hands 及其日程。两者都会体现在产能恢复速度上，而这正是 SLA 必须度量的东西。

在 SLA 方面，我们为 3 个层级的厂商制定了一套标准化 SLA。

这些文件提供以下内容：

- 两种场景（HGX 8 卡系统，如 H100 或 B300；以及 MGX 4 卡系统，如 GB200 或 VR NVL72）下「节点」「机柜」「集群」「站点」的技术定义
- 所有系统「宕机时间（downtime）」的技术定义
- 三个层级的配套 SLA（「青铜」「白银」「黄金」，含对应阈值与宕机时间的信用赔付）
- 双向承诺的宕机时间度量与信用赔付机制
- 建议排除在宕机时间度量之外的项目，如软件升级、安全补丁与物理维护
- 建议的月度厂商 SLA 表现复盘节奏
- 买方在低于建议阈值时享有的合同终止权
- 验收测试定义，描述跨 GPU 计算、网络、存储与软件应执行的测试类型，以验证集群可用并可验收，并建议联系 SemiAnalysis 进行 ClusterMAX 技术评估
- 买方在错过约定验收日期时享有的合同终止权
- 「不可抗力（force majeure）」条款定义
- ……等等

我们鼓励算力买家（Neolab）、云厂商（Neocloud）、债务/融资伙伴与保险公司以这些条款作为合同基础，并在验收测试与月度 SLA 表现复盘中纳入 SemiAnalysis 技术评估。我们使用 **cmax** 工具与一套全面的专有流程执行该技术评估。

更多信息请联系 [clustermax@semianalysis.com](mailto:clustermax@semianalysis.com)。

## 安全

自我们发布《[多数 Neocloud 的安全很糟糕](https://newsletter.semianalysis.com/p/most-neoclouds-suck-at-security)》以来，各方的反应令我们备受鼓舞。朋友们在自家集群上运行[我们的 CLI](https://github.com/SemiAnalysisAI/clustermax)，找出该换掉的陈年旧包；总体上，业界以更严肃的态度对待这一问题的动力也在增强。

尽管如此，我们认为它仍值得更多审视。当「AI 是否会毁灭人类」的论战甚嚣尘上之时，却几乎没有人分析它究竟可以通过哪些具体手段脱离控制、造成伤害。[OpenAI](https://openai.com/index/hugging-face-incident-and-the-road-ahead/) 与 [Anthropic](https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals) 正砸着天文数字的钱做功能获得性（gain-of-function）研究，它们的一部分基础设施已被曝光相当可疑；然而基本无人评论的是：GPU 集群——承载这些模型的物理宿主——往往压根没有你期望的那种免疫系统。

无论你对 AI 能力持何种信念，良好安全实践的必要性都成立。即便这些集群不会因 AI 工具而变得更脆弱，事实仍然是：我们正把数十亿美元花在并未达到应有安全水平的基础设施上。不难想象许多不愉快的场景，其全部所需不过是一个会 Vim、深谙操作系统的人。去读读 Hugging Face 的事件报告，数一数那些让火势蔓延的平凡网络安全错误吧。

同样值得强调的是，这在某种程度上是结构性风险。当整个行业正艰难应对严厉监管与不加分辨的社会反弹之时，一家 LLM 工厂被攻破是它最不该送上头条的事。这出于网络安全理由——每个被攻陷的节点都增加了攻击者可探索的邻居数量——也出于寻常的社会政治理由：无论好坏，唱衰者都会把整个 neocloud 行业一竿子打翻。

做个好邻居，别被黑。

![](https://substack-post-media.s3.amazonaws.com/public/images/dcd6b188-48c7-4998-a18f-20a0bd3fc723_1339x1339.png)

## 智能体编程

智能体编程已经在给托管 GPU 集群带来利润率压力，因为使用 AI 工具的客户更愿意选择裸金属或轻托管集群。我们在测试中随时随地都能看到这方面的证据。如果我们需要添加 Linux 用户而集群上没有现成脚本，Codex **/goal make useradd script and add my whole team**（目标：写个 useradd 脚本，把我全组加进去）就省去了跑腿。尤其在文档糟糕的集群上，智能体帮我们把所有可能的配置硬啃了一遍，让我们得以脱困。相应的 Slack 对话常常是这样的：

> 「哥们，这个 XYZ 到底该怎么用？」

> 「没事了，Codex 告诉我是 ABC。」

> 「对对，就是这个。我们把它写进文档。」

智能体在成功标准清晰、上下文良好的环境里帮我们最多；否则，它们对待 GPU 系统的方式相当天真。它们具备相关知识，但相对于看似合理实则错误的方案，这些知识并没有被赋予足够高的权重。例如 Claude 有个习惯：不用作业数组而用循环，把 Slurm 控制器按在地上摩擦。我们的一个智能体嫌 NVLink fabric 配置太麻烦，干脆改走 InfiniBand 启动作业并宣布胜利；另一个犯了类似错误，把存储测试跑在了 NVMe 而不是 NFS 上；还有一个在把 GPU 作业调到 CPU 节点上之后，反过来怪厂商性能差。我们通常让智能体通宵运行，指令要么是 `/goal fix this part of the cluster so tests can run`（目标：修好集群这部分让测试能跑），要么是 `/goal try to break this part of the cluster with a realistic workload`（目标：用真实工作负载试着搞坏集群这部分）。总体上，这让我们成倍放大了产出，但有时验证结果所花的时间比我们自己干还长。如果你对怎么搭集群心里有数，智能体会让你更强大，你甚至可以考虑接受一个比原本更差的厂商。如果你不知道自己在干什么，你的 AGI 顾问会兴高采烈地教你朝自己脚上开枪。在这门半透明的生意里，智能体放大而不是抹平技能差距。

一个有洞察力的例子是 CoreWeave 的集群点亮（bring-up）流程——它本来就已位列业内最严谨之列。现在，除了严苛的经典流程之外，他们还让 LLM 在整个机队上做统计分析，寻找能更早标记故障、改进流程的模式。CoreWeave 还有一个 NodeBot，在其自动化告警之上提供轻量推理，总结情况并建议后续步骤，为环节中的人类简化诊断。例如，团队描述过这样一个事件：一条[导热界面材料泵出（pump-out）告警](https://www.youtube.com/shorts/WP3LKBHL8vQ)本应把节点移出集群接受调查，但同时出现的一条 [PMU halt 告警](https://forums.developer.nvidia.com/t/xid-62-xid-154-gsp-pmu-halt-crash-on-rtx-pro-6000-blackwell-during-llm-inference/364958)却抢着要让节点重启而非分诊。NodeBot 在此冲突之下识别出了正确动作。CoreWeave 有大规模运行 GPU 的经验，掌握无数训练数据中不存在的经验法则，并有专家持续闭环以改进对这些模型的使用；即便 [OpenAI 用 AI 生成的 kernel 造出了炸裂的芯片](https://newsletter.semianalysis.com/p/openai-jalapeno-better-than-nvidia)，我们也不认为 CoreWeave 会在短期内被拿着 vibe coding 数据中心自动化的新贵 neocloud 威胁到。

尽管——老实说——业内人人都在至少部分工作流中使用 AI，我们看到唯一称得上 AI-first 的产品是 AWS 提供的一个不错的 MCP 服务器。除此之外，所有文档名义上都是写给人看的。厂商迎合智能体能做的最好的事，就是提供穷尽式文档——理想情况下比任何人类可能通读的都更详尽——并在集群上留下「黄金配方」作为爬山的起点。除了尚未 AI-first 的传统流程，还有许多系统纯粹因为不为智能体设计而更差。例如，让 AI 管理你的作业或许有利于集群利用率，但它并不尊重那些为辅助研究而设的老式系统。CoreWeave 与 Nebius 有大量 Slurm 层优化——带 RBAC 与按用户/组强制优先级的真实作业记账系统、精心管理的分区、作业数组、日志与指标——在一切都由智能体运行时全部浪费。CoreWeave 还告诉我们，他们见过头节点内存耗尽，因为远程遥控的 Claude 把集群「糊弄编排」（sloporchestrates）一通。看厂商改进其 AI 智能体亲和性，将是一件有趣的事。

# 展望未来

正如本文贯穿描述的，我们历来测的是集群。但市场显然已朝两个相反方向移动。

首先，最大的实验室正以数百 MW 计的规模采购裸金属，且拥有自管训练集群、编排软件、监控与可靠性的在室人才。本质上，它们的 neocloud 供应商（当它们使用而非自建时）就是一群关工单的数据中心技术员。这是一门复杂的生意，不容小觑：NVIDIA GPU 有 [172 种有据可查的独有故障方式](https://docs.nvidia.com/deploy/xid-errors/analyzing-xid-catalog.html)（XID）。其中许多故障模式还会相互叠加，构成一片令人叹为观止的故障场景面积，需要简单排障逻辑、人类经验、以及日益增多的 AI 智能体研究相结合，才能从故障中恢复。

与此同时，许多初创公司正筹集数千万乃至数亿美元，并把几乎全部资金花在算力上。但由于这类研究大量由 RL 驱动——在真实生产轨迹上对长时程智能体做持续学习——对离线、吞吐优化的推理与在线、时延敏感的推理的需求都非常旺盛。同时，越来越多客户在寻找为其工作流购买原味开源 token 的最简途径。

这引出我们即将发布的下一篇文章：推理端点的解剖（Anatomy of an Inference Endpoint），并逐步把推理端点测试纳入未来版本的 ClusterMAX。我们认为，所有 neocloud 此后都需要一门端点生意。

我们还将评估推理之外的 RL 基础设施：沙箱、托管训练、评测等。我们持续看到大量新厂商每天进入（以及退出）市场。身处 AI 行业是个激动人心的时代，而 neocloud 正居于风暴中心。

如果你读到了这里、还渴望了解我们对每家厂商的逐一点评，你应该考虑来 SemiAnalysis 工作！

> 我们正在研究、咨询与技术团队方向积极招聘，纽约与旧金山办公室有多个职位空缺，也接受远程办公。
>
> **ClusterMAX 工程师：**有 Slurm、Kubernetes 与 GPU 经验者皆可，不限资历（[全职](https://semianalysis.com/semianalysis-careers/#role-member-of-technical-staff-clustermax)）
>
> **Tokenomics 工程师：**有模型评测、评测框架、推理端点与 RL 基础设施经验者皆可，不限资历（[全职](https://semianalysis.com/semianalysis-careers/#role-member-of-technical-staff-clustermax)）
>
> **研究分析师——AI 基础设施与经济学：**有覆盖 neocloud、neolab 及前沿实验室 tokenomics 财务分析经验者皆可，不限资历（[全职](https://semianalysis.com/semianalysis-careers/#role-mts-research-analyst-ai-infrastructure-economics)或[实习](https://semianalysis.com/semianalysis-careers/#role-mts-research-analyst-intern-ai-infrastructure-economics)）
>
> **技术顾问：**主导从技术战略到技术尽职调查的项目。有咨询与技术背景者皆可，不限资历（[全职](https://semianalysis.com/semianalysis-careers/#role-technical-consultant)）

感谢阅读，期待在未来的 ClusterMAX 版本中再见。

# 附录：厂商点评

## 白金级

### CoreWeave

CoreWeave 仍是业内最锐利、最扎实、最主动的 neocloud。

我们的 CoreWeave 集群在所有关键类别都是典范。健康检查如预期工作，可靠性出色，几乎所有测试开箱即达预期值。与 Nebius 一起，CoreWeave 是全行业的标尺——不只在「表现优异」的抽象意义上，也在字面意义上：我们会把它们的集群与低评级集群做对比，用以精确描述别家的不足。当其他 neocloud 还要人催着更换发霉的 GPU 驱动时，CoreWeave 不仅把基本功打理妥当，还搭起了一套可观的自研栈来压榨边际性能与可靠性提升。

[ClusterMAX 2.0 报告](https://newsletter.semianalysis.com/p/clustermax-20-the-industry-standard)详述了 CoreWeave 的设计决策，包括裸金属开通、Slurm 分叉、DPU 的使用与健康检查。自那以后，CoreWeave 的极客们新加的一个聪明功能叫「[GPU 掉队者检测](https://docs.coreweave.com/products/sunk/discover_sunk/straggler-detection)」，集成在他们业内最佳的面板里。CoreWeave 不必让客户翻日志或对整个机队做二分法来隔离坏 rank，而是对 NCCL 遥测应用自研算法，并基于发现推荐修复策略。CoreWeave 团队告诉我们，他们几乎每天都在与客户的电话会上使用这个功能。有各种各样的软故障不写 XID、也不留任何明显痕迹，却随着作业等待掉队者而白白烧掉 GPU 时。

比发现坏 GPU 更好的，是压根别调度它们；CoreWeave 还有一套体系，确保每个节点在被托付客户工作负载之前先过一道高门槛。在 CKS 中节点空闲时，CoreWeave 每小时跑 20-30 分钟烤机，验证纵向与横向扩展 fabric 是否健康、GEMM 数据是否达标、D2H 与 H2D 带宽是否够高等等。这些测试会被客户工作负载抢占；对运维者不可见，却帮忙确保抓到故障的不是生产工作负载。CoreWeave 当然不是唯一有主动健康检查的厂商，但其体系异常稳健。

这种严谨延伸到 CoreWeave 的[点亮流程](https://docs.coreweave.com/platform/fleet-management/node-lifecycle)。CoreWeave 每周开通约 10,000 张 GPU，他们相信自己掌握着比上帝还多的、关于「什么能证明一台 Blackwell 机柜健康」的数据。在 CoreWeave 看来，Nvidia 的诊断工具擅长抓很多故障，而其独一无二的数据深度让他们得以部署一套自定义的补充测试套件，包括针对 NVLink 的测试。这一流程的核心是 Fleet LifeCycle Controller（FLCC），它「[自动化节点开通、测试与监控](https://www.sec.gov/Archives/edgar/data/1769628/000119312525044231/d899798ds1.htm)」，掌管从上电到交付的全程。重要的是，正如其他大规模运营机队者可以佐证的，存在一大堆 Nvidia 文档覆盖不佳的冷门故障模式。CoreWeave 对这些故障做统计以更好地预测未来故障，并把响应模式固化进 FLCC。这也是大规模运营经验成为我们评级关键标准之一的原因。新手与 CoreWeave 这样拥有严格 runbook、自动化与烤机的厂商之间，差距是天壤之别。如上文「智能体编程」一节所述，CoreWeave 在这套体系之上使用 LLM，提炼人类工程师注意不到的洞察。CoreWeave 还在交付前与制造商协作。参与程度随 OEM/ODM 与生产阶段而异，但总体目标是在供应链中逆向推进、尽早抓问题：能在点亮时发现的，绝不要留到生产；能在 L11 诊断发现的，绝不要留到出厂之后。

他们在 Blackwell NVL72 点亮与验证上的经验，加上与 Nvidia 和 Dell 的紧密关系，使 CoreWeave 成为首家宣布 [VR200 NVL72 系统通过 L11 诊断](https://x.com/SemiAnalysis_/status/2060912340590084479)的厂商。CoreWeave 把 VR 描述为「我们带上自家 IP 的一代」。随着计算的物理需求持续攀升，CoreWeave 认为「大楼的运营方式如今是计算机运营方式的一部分——它们不再是两件独立的东西」。因此，CoreWeave 在[近期的一篇博客](https://www.coreweave.com/blog/a-deep-dive-on-coreweave-innovations-for-nvidia-vera-rubin-nvl72)中推出了自研的 Racky、Valvey 与 RLCC。特别有意思的是 Valvey——一个可编程的每机柜液冷阀组。它让 CoreWeave 能对每个机柜的冷却回路做细粒度控制，并且在泄漏或其他紧急情况下具备触发停机的能力。尽管 CoreWeave 开始以超大规模厂商的心态自建硬件，它却把自己的路线框定为「反超大规模」：传统基础设施强调冗余、以防故障为目标，而 CoreWeave 为优雅失败与快速恢复而构建，限制故障域，对不可避免的故障做出更敏捷的响应。

然而，在当前这场万亿美元级建设中，CoreWeave 一边响应客户需求的暴涨，一边应对不断上升的资本成本。当然也有不少好消息可讲：它与 Meta、Microsoft、OpenAI 及 NVIDIA 这些最大客户的关系看似稳固，最近还与 [Anthropic 签下多年协议](https://investors.coreweave.com/news/news-details/2026/CoreWeave-Announces-Multi-Year-Agreement-With-Anthropic/default.aspx)。今夏它宣布了与 [HRT](https://investors.coreweave.com/news/news-details/2026/Hudson-River-Trading-to-Build-Next-Gen-Research-Platform-Powered-by-NVIDIA-Vera-Rubin-NVL72-on-CoreWeave-Cloud/default.aspx) 和 [Jane Street](https://www.coreweave.com/news/jane-street-signs-6-billion-ai-cloud-agreement-with-coreweave) 的重磅交易。它还在[积极扩张 APAC 产能](https://www.coreweave.com/news/coreweave-expands-cloud-ai-platform-to-indonesia-marking-first-move-into-asia-pacific-region)，表示「[期待国际市场成为增长的主要动力](https://www.fool.com/earnings/call-transcripts/2026/08/18/coreweave-crwv-q2-2026-earnings-call-transcript/)」。但它身负 $35B 债务，随着资本成本上升，项目落地变慢。因此 CoreWeave 越来越聚焦于长期裸金属合同——有投资级对手方时易于融资——而非利润率更高、市场却不太愿意资助的托管集群。此外，我们上次的报告提到过一串亮眼的近期收购，但此后其 [Core Scientific 合并告吹](https://investors.corescientific.com/news-events/press-releases/detail/124/core-scientific-announces-termination-of-merger-agreement-with-coreweave)，再无其他公告。

至于反馈（有些略显吹毛求疵）：

1. 我们希望其托管 SUNK 认证 RBAC 能按集群粒度实施
2. 我们希望启用本地 GPUDirect Storage 能在 UX 控制台里做成一键按钮
3. 新用户 onboarding 以及 UX 控制台中 SSH 公钥输入框的位置，让许多尝试过的用户极其困惑

CoreWeave 已开始从裸金属多元化，第一步是提供[自助服务 SUNK 集群](https://investors.coreweave.com/news/news-details/2026/CoreWeave-SUNK-Expands-Capabilities-to-Bring-AI-Workloads-Online-Faster--Anywhere/default.aspx)，使其在有余力时可以选择卖向按需市场。同样值得注意的是，并非所有「裸金属」合同都一样。在 CoreWeave 的所有裸金属合同中，它们仍管理横向扩展与前端网络、做烤机、负责修理/更换、监控及其他常规 day-two 运维。相比之下，有些厂商自称 neocloud，却被锁在自己的数据机房之外。我们将在即将发布的文章中比较各家厂商的裸金属产品，届时深挖这些细节。

CoreWeave 还上线了托管推理平台，最近[披露 $100M ARR](https://s205.q4cdn.com/133937190/files/doc_financials/2026/q2/CRWV-US-CORRECTED-TRANSCRIPT-CoreWeave-Q2-2026-Earnings-Call-11August2026.pdf)。我们正在为即将发表的 serverless 推理端点文章积极测试它，不过失望地发现不支持按 token 计费的公开端点。目前只能说，CoreWeave 的推理端点还有一些工作要做。

### Nebius

在 ClusterMAX 2.0 中，Nebius 被评为全球第二好的 neocloud，却仍留在黄金级。这一次，Nebius 无可争议地成为行业领导者，各类产品都很强，且能收取可观溢价。Nebius 升入白金级。

Nebius 与 Nvidia 的关系依旧紧密，包括 [3 月的 $2B 投资](https://nebius.com/newsroom/nvidia-and-nebius-partner-to-scale-full-stack-ai-cloud)，Nvidia 已于 7 月披露[持有其 9.3% 股份](https://finance.yahoo.com/technology/ai/articles/nvidia-reports-9-3-beneficial-134838540.html)。Nebius 是 2025 年 12 月首家部署 HGX B300 的厂商，并[位列最早进行 VR NVL72 点亮的 neocloud 之一](https://blogs.nvidia.com/blog/vera-rubin/)，[预计今年底明年初开始部署](https://www.fool.com/earnings/call-transcripts/2026/08/19/nebius-nbis-q2-2026-earnings-call-transcript/)。

Nebius 在美国与欧洲多地的建设持续推进，[最近把 2027 年底已签约电力目标上调至 5 GW](https://www.sec.gov/Archives/edgar/data/1513845/000110465926094568/tm2622968d1_ex99-2.htm)。承购方方面，Nebius 与超大规模厂商 [Meta](https://nebius.com/newsroom/nebius-signs-new-ai-infrastructure-agreement-with-meta) 和 [Microsoft](https://nebius.com/newsroom/nebius-announces-multi-billion-dollar-agreement-with-microsoft-for-ai-infrastructure) 签了大单，与 [Reflection AI](https://techcrunch.com/2026/07/14/reflection-inks-1b-compute-deal-with-nebius/) 和 [Palantir](https://nebius.com/newsroom/palantir-and-nebius-partner-to-deliver-a-complete-sovereign-ai-stack-to-palantir-customers) 签了较小的单，是少数几家既握有数百 MW 超大规模协议、又仍定期竞标小得多的初创合同的 neocloud。它们是所有 neocloud 中在短期集群市场上最活跃的，服务着许多满意的客户。Nebius 用俄式口音吓跑潜在客户的日子已一去不返。这一点也反映在其产能采购上：与许多同行不同，Nebius 通过遍布的数据中心与软件伙伴网络，机会主义地抢下了 5-20 MW 区间的站点。

至于集群本身——好集群通常很无聊。在 Nebius 上，烤机零错误运行；Slurm 具备拓扑感知；我们需要的包都在集群上而且普遍较新；WAN 良好；编排层没有暗坑。Nebius 与其他所有厂商之间的一个技术差异点是：Nebius 构建并开源了其偏好的 SonK 发行版 [Soperator](https://github.com/nebius/soperator)。（CoreWeave 当然也在内部自建 SUNK，但不开源。）本轮我们测的一个 Gcore 集群用了 Soperator，之前几轮的 Voltage Park 与 FPT 集群也是。Nebius [写道「Soperator 真正的魔力在于我们使用 'jail' Persistent Volume 的方式」](https://nebius.com/blog/posts/soperator-in-open-source-explained)：Nebius 在 `jail` 提供一个 VirtioFS 卷，然后绑定挂载到 `/`，因此你不必操心把缓存指向正确的目录，`salloc` 节点时也不必多想把文件带在身上。在我们对其他厂商的点评中你会看到 SonK 上管理存储系统的一堆棘手问题：Slurm 与 Kubernetes 对持久化的哲学不同，当你实际上隔着好几层、站在一个临时 Kubernetes pod 之上时，要营造裸金属的幻觉并不总是容易。Nebius 的做法让运维者毫无压力。

具体而言，Nebius 在每个 worker 上提供了多个存储层：`/jail` VirtioFS、`/home` NFS、`/mnt/data/` VirtioFS、`/mnt/local-nvme` ext4 与 `/mnt/memory` tmpfs，外加[一流 S3](https://docs.nebius.com/object-storage/)。对 I/O 密集作业推荐 `/mnt/data`，而共享代码与其他低并发访问数据用 `/home` 即可。我们最初测 `/mnt/data` 时，看到 4 KiB 顺序分配写非常慢，而 128+ 个 rank 并发建目录时偶尔因元数据可见性不一致返回 `EEXIST`，杀死了我们的作业。针对我们反馈的病态工作负载，Nebius 重新调优了该文件系统，之后它被证明又稳又快。我们反复折腾并确认错误已解决；按客户端计它跑赢中位数，我们还能进一步确认它可扩展到跨两个机柜承载高要求工作负载。

Nebius 在健康检查上下了大功夫，在我们的测试中表现良好。在我们 GB300 机柜上的合成错误注入后，Nebius 自动将节点恢复服役；流程尚未针对速度优化，从头到尾花了 8 小时 40 分，但检测是即时的，流程最终走得通。此外，我们测的其他 GB300 机柜并不会自动重启并恢复故障节点，因此这一流程能自动驾驶本身就给 Nebius 加分。（正如「Blackwell 与 Grace Blackwell」一节所述，GB300 节点普遍根本不做自动修复，因为 NVL72 机柜里没法真正热插拔节点，排障一般也比 HGX 服务器复杂得多。）Nebius 还为我们提供了一组出色的面板，照亮了集群健康等诸多方面。

![](https://substack-post-media.s3.amazonaws.com/public/images/31c3e010-0c8b-4dba-8b86-4a388335ff60_2048x1208.png)

这一切的结果是，Nebius 眼看着自己的每 MW 收入相对 CoreWeave 攀升（市值也随之上涨）。由于按当前价格它们还有多得多的产能可卖，我们预计这一趋势会持续。有趣的是，我们目睹 Nebius 在近期谈判中变得非常激进，包括一次把一批产能直接拿出来拍卖。总体而言，索要高价、加上 1 年期承诺预付比例最高可达 100% 的大额预付款，看起来是一门很不错的生意——尤其当这些预付款在当前 TCV 下就能覆盖服务器全部 capex 时。项目 IRR 无限高，谁不想要？

在其最大的裸金属站点，Nebius 继续面临建设与许可延期，包括 Béthune 和 Vineland 两地，我们已[为我们业内领先的数据中心模型客户做了详尽覆盖](https://semianalysis.com/institutional/nebius-post-earnings-likely-over-optimistic-arr-target-still/)。但随着各类芯片陆续上线，Nebius 的履历使其处于继续增长的强势位置。

总体而言，Nebius 一再令我们印象深刻。虽然我们确实认为它在许多技术层面以及与 NVIDIA 和前沿实验室的关系上仍落后于 CoreWeave，但扎实的商业决策已确立其作为服务 neolab 的默认 neocloud 的地位。

## 黄金级

### Google Cloud

在 Google Brain 与 DeepMind 从前沿奇怪后撤之际，GCP 的签约势头鲜有对手。值得一提的伙伴包括 [Palo Alto Networks 的 $10B 大单](https://finance.yahoo.com/news/google-cloud-lands-deal-palo-130205661.html)与 Thinking Machines Lab 的[「数十亿美元交易」](https://techcrunch.com/2026/04/22/exclusive-google-deepens-thinking-machines-lab-ties-with-new-multi-billion-dollar-deal/)，还有与其利润丰厚的 AI 安全组织 Anthropic 关系的扩展。通过收购[网络安全初创 Wiz（$32B）](https://techcrunch.com/2026/03/11/google-completes-32b-acquisition-of-wiz/)与能源初创 [Intersect（$4.75B 现金）](https://abc.xyz/investor/news/news-details/2025/Alphabet-Announces-Agreement-to-Acquire-Intersect-to-Advance-U-S--Energy-Innovation-2025-DVIuVDM9wW/default.aspx)，Google 一直在积极扩张技术能力。它还通过[放量 TPU 销售](https://semianalysis.com/accelerator-hbm-model/)（而非只在 GCP 内出租）让自己暴露于新的收入流——这一进展我们非常渴望跟踪。其自有 TPU 即服务也仍在增长，这要归功于与 [Blackstone 的 $5B 交易](https://www.blackstone.com/news/press/blackstone-announces-joint-venture-with-google-to-create-new-tpu-cloud/)，目标产能 500 MW。Google 手握数 GW 的 pipeline，我们期待继续跟踪其与其他超大规模厂商及实验室在电力与许可获取上的竞争。

凭借横跨技术栈如此多层的独特位置，Google 的工程师总量或许超过世界上任何公司，但它在[支持创新方面的履历明显不完美](https://killedbygoogle.com/)。在 ClusterMAX 1.0 中我们指出其平台的问题一大堆，却预言 GCP 会迅速达到黄金或白金级。直到 ClusterMAX 3.0 这一预言才成真，但 Google 终于、而且稳稳地名列最佳托管集群厂商之中。

GCP 的 GPU 体验不如我们的白金厂商 CoreWeave 与 Nebius 精致。与更年轻、更专注的 neocloud 的流畅 UI 相比，其控制台像车管所（DMV）。访问需要一个偶尔闹脾气的 Google Cloud CLI，逼得我们有时改用 Google 控制台的浏览器连接，而它同样不可靠。我们的 GB200 GKE 集群上有一处小配置错误：默认 StorageClass 拒绝挂到 `a4x-highgpu-4g` 节点，逼得我们改用非默认 class 才拿到块存储。吹毛求疵之外，GKE 配置得很好，我们用得开心。Google 的托管 Slurm 已正式 GA 且相当扎实，默认值与健康检查都配置得当。我们为 ClusterMAX 2.0 在其托管 Slurm 上做的许多测试如今仍然有效，因为 GCP 产品管理层的官僚们终于允许真实客户使用该产品了，而不是给它贴上「Beta」「Pre Release」「尚未 GA」之类的标签。（顺便说一句，我们后面要讲的许多 neocloud 倒应该考虑更常用用这些标签——合适的度在两者之间。）

![](https://substack-post-media.s3.amazonaws.com/public/images/ba8d6bb3-86ab-4dd2-be3e-d310b9718ccb_666x108.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/aba7483b-faa9-4e5a-b52f-6e581ffdd2ca_2048x1241.png)

我们的 GCP 集群与其他受测集群之间最大的差异点在网络。第一次 NCCL 测试挂起，因为自动 GID 选择选错了地址；固定 `NCCL_IB_GID_INDEX=3` 后完成了运行。即便如此，NCCL 测试结果仍不能令人满意：你希望看到性能随消息大小单调上升的大致逻辑斯蒂曲线，但我们看到的是如下锯齿状：

![](https://substack-post-media.s3.amazonaws.com/public/images/693ad4f9-4ec8-443e-a72c-2ac4f40d6d15_1928x1478.png)

这倒有可能是 NCCL 自身的问题而非 GCP 配置的问题。NCCL 的启发式[并不总能为消息大小与拓扑选出正确的协议和算法](https://developer.nvidia.com/blog/understanding-nccl-tuning-to-accelerate-gpu-to-gpu-communication/)，一些手工调优总在预期之内。然而，我们此时已积累数 GB 的网络数据，知道应该有更好的表现。问题最终只是我们没有启用 gIB 插件——这是 Google 为在其 RoCE 网络上提升性能而随附的一组 NCCL 插件。自 26.07 起，gIB 已内置进 NGC PyTorch 镜像，因此 Google 的客户默认获得这套定制栈。装上 gIB 后，我们得到了更好的曲线，16 节点 all-to-all 峰值吞吐提高 4.4%。（注意，这两组测试都关闭了多节点 NVLink fabric，以隔离横向扩展网络（此处为 RoCE）的性能。）

![](https://substack-post-media.s3.amazonaws.com/public/images/1bd9c330-467a-42b9-9da6-175f6a9af4a7_1329x1042.png)

虽不完美，但看起来好多了，而且头部数字扎实。至此，fabric 健康、配置够好已无疑问，想继续榨汁的工程师有了一个坚实的起点。

这是 Nvidia 与 Google 为 Google 的 ConnectX-7/8 NCCL 插件做自动激活的漂亮工作。以前用户得折腾正确的库加载路径与环境变量，才能在 GCP 的 Nvidia GPU 机器上正确设置并优化 ConnectX NIC 的性能。我们几个季度前给了反馈，如今它已完全自动化！

![](https://substack-post-media.s3.amazonaws.com/public/images/dc7905b0-29a3-4d2b-bc64-bc5547bdb441_1682x1144.png)
*来源：Nvidia*

GKE 的健康检查工作正常。与其他有 NVL72 系统经验的厂商一样，Google 的健康检查做了介入，但把病节点带回机队留给运维者决定。具体来说，注入 XID 后，健康检查标了 `GPUUnhealthy=True` 与 `cloud.google.com/health-check-status=warning`，但节点保持可调度。这种配置用起来省心，是 GCP 客户偏好的默认行为，也可以按用户喜好配置为对不同严重级别的错误做出响应。

要继续进步，GCP 可以参考 Nebius 与 CoreWeave 近期做出的种种体验改进。它应交付一个更好导航的控制台、简化 IAM 与 RBAC，并让集群访问无痛——无论是通过标准 SSH 或 `kubectl`，还是把现有 CLI 做到万无一失。尤其如今 gIB 已进入默认 Nvidia 镜像，我们希望 GCP 的运维者从 GCP 横向扩展网络中压榨性能不再费劲。他们也可以继续深耕中端市场的 neolab、改善贴身支持体验，并改善与 Nvidia 的关系。GCP 一再把生意输给更小、更弱的 neocloud，要么因为缺 GPU 产能，要么因为拒绝以某个价位服务市场。

我们期待在可用时测试 GCP 的 VR NVL72 系统，并看到 GCP 在可用性与性能上的持续改进。

### Oracle

正如 ClusterMAX 2.0 提到的，Oracle 在超大规模厂商中位置独特：其增长必须来自大合同。与 AWS、Google、Azure 不同，Oracle 没有任何出售前沿 token 的协议；与 Meta、Google 不同，它没有可倚仗的非前沿实验室。它持续砍下涉及 OpenAI、Meta 与 Nvidia 的巨额交易，并报告「[6 月至 8 月交付 850MW 新增数据中心容量](https://s23.q4cdn.com/440135859/files/content_files/1q27-pressrelease-September_FINAL.pdf#page=1)」——一个令人咋舌的数字。我们预计其 2027 年的相对增长为超大规模厂商中最大，尽管基数最小。

我们测了 Oracle 的两个集群，依次介绍。第一个是 Slurm 上的 GB300 NVL72 集群，建在[多平面网络](https://blogs.oracle.com/cloud-infrastructure/first-principles-acceleron-multiplanar-networking)上。这是原味 Slurm，但由于客户需求，Oracle 已把 Slurm-on-OKE 列上路线图。分配开始后，我们试图从控制台找路进去，但和所有超大规模控制台一样，那里是个令人生畏的地方。

![](https://substack-post-media.s3.amazonaws.com/public/images/efe741a9-f74f-4a0b-9c5f-070fbb4e2cf7_2048x1090.png)

重要的是，Oracle 的控制台不支持 RBAC——控制台上没有任何东西与 SSH 用户关联——因此我们所有 SSH 密钥只能在机器上管理。有一次，我们的实习生想往 `authorized_keys` 追加内容时忘了 `-a` 参数，把我们之前的密钥全删了。显然是经典的人为失误，但这正说明我们为什么偏好控制台上有一条加固路径。当一条错误命令就可能把我们锁在集群外时，我们宁愿不信我们的实习生——尤其那位，无意冒犯——在命令行敲咒语。所幸 Oracle 的工程师立刻发现了错误并替我们修好。

我们希望他们修好这一点并加上企业级 RBAC。

不出所料，Oracle 的集群从第一天起表现就很好。他们提供了 InfiniBand 与 NCCL 测试脚本，这很有帮助，因为原版脚本无法正确用满全部 4 条轨道。烤机无瑕疵，Oracle 托管的 Lustre 吞吐强劲。Oracle 的健康检查如预期工作：对我们的合成错误 drain 了节点，但是否终止并更换 GB300 节点留给用户决定。Oracle 托管的 Prometheus 与 Grafana 不错，虽然不完美——例如未与终端用户的作业记账体验集成。但积极的一面是，健康指标现已集成进控制台的 Cluster Manager，一眼看清关键状态更容易了。

![](https://substack-post-media.s3.amazonaws.com/public/images/e34a3ddb-3a0f-4480-be9b-63a10a3775fa_2048x1192.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/e6b17127-debb-47f4-8c8d-510e5e724040_873x473.png)

接下来我们在 OKE 上测了 MI355X。这是除 TensorWave 之外唯一让我们试驾 AMD GPU 的厂商。旅程颇为颠簸。

正如我们上次抱怨的，起初需要 SSH 进一个 operator 节点来操控 Kubernetes。这一次，团队很快解决了我们的 Oracle CLI 问题，我们得以迅速把凭据下载到本地。不过该集群上更大的问题在 NIC。峰值性能接近线速，硬件上我们检测不出问题。问题出在 ionic 驱动上。我们在全部八张 NIC 上做逐轨道 `ib_write`/`ib_read` 扫描，每条轨道都到 391 Gb/s，然后测完那一刻节点就卡死了：pod 被删除时，perftest 进程始终完不成 `rdma_cm` 拆除，强制的 `kill` 让 NIC 的 destroy-CQ 命令超时，`ionic_0` 与 `ionic_4` 上的 RDMA 管理队列死掉。更糟的是，两个端口仍显示 400 Gb/s `ACTIVE`，节点保持 `Ready`。被动检查不查 RDMA 控制路径，而主动检查已经 8 天没跑过。我们在 RCCL 反复失败后 grep `dmesg` 才发现问题。Oracle 在一个周末迅速诊断并重启：他们自己的 `ibwrite` 健康检查几天前在该集群上就以同样方式失败过。在一通我们解释了病态工作负载的电话之后，他们与 AMD 沟通并向集群推送了不同的驱动与固件，问题解决。

另有一次，一块 GPU 间歇性从 PCIe 总线上消失，既没被健康检查抓到，也没在面板上恰当呈现。Oracle 迅速更换了节点，并对我们关于面板的反馈做了回应。

![](https://substack-post-media.s3.amazonaws.com/public/images/3a8838cf-5ef3-4634-8a08-87f34daba095_2048x492.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/33c3e134-2403-4583-a918-0074c8acc52e_2048x1174.png)

这段经历喜忧参半，但 Oracle 的响应速度很好。这些驱动已知不稳定，健康检查却没有任何告警，这一点尤其不可取。不过，Oracle 与 AMD 的密切关系显然是资产：他们能直接对话相关团队、诊断问题、迅速打上补丁。在 Oracle 这种体量的组织里，这种支持并不常有。有意思的是，Oracle 还是白银级及以上唯一一家已装库中没有可适用 CVE 的厂商，也是青铜级及以上仅有的两家之一。对我们而言这更多是预期而非加分项，但它清晰地证明了其集群部署与升级的自动化确实在起作用。

如果我们是 neolab，这次测试经历会让我们对与 Oracle 合作抱有信心。然而，鉴于 Oracle 日益押注于为 OpenAI 等前沿实验室做 Stargate 之类的裸金属部署，这一点已无关紧要。那门生意的成功更多取决于[天然气管道建设的政府批准](https://newsletter.semianalysis.com/i/201118118/3-well-capitalized-projects-facing-permitting-and-local-opposition-issues)，而不是 RCCL 测试。

尽管如此，Oracle 自上次测试以来有进步，整体体验非常好。我们期待未来继续盯住他们。

## 白银级

### Lambda

Lambda 最近一次上新闻，是因为与 Hut8 和 Nvidia 一起参与了 [Anthropic 的 $35B 交易](https://www.reuters.com/technology/anthropic-signs-35-billion-cloud-deal-with-nvidia-backed-lambda-source-says-2026-08-31/)，在 Nueces County 落地 350 MW。在那之前，有传闻称其[正筹备 2027 年 IPO](https://finance.yahoo.com/technology/ai/articles/ai-cloud-provider-lambda-in-talks-for-3-billion-pre-ipo-round-234205946.html)，而且它分别为建设筹了 [$1B](https://lambda.ai/blog/lambda-closes-1-billion-senior-secured-credit-facility)、[$926M](https://lambda.ai/blog/lambda-closes-926-million-senior-secured-term-loan-b-facility) 与 [$1B](https://www.bloomberg.com/news/articles/2026-08-28/nvidia-backed-lambda-inks-1-billion-private-debt-for-chip-deal) 债务。在这一切增长之中，自 ClusterMAX 2.0 判其白银级后，我们有意在这一轮评估 Lambda 的集群。

Onboarding 以一份漂亮的 deck 和 PDF 开始，解释集群上会有什么，访问权限也很快搞定。

![](https://substack-post-media.s3.amazonaws.com/public/images/d5aecaed-0d08-4c63-8b24-f1058479b4dd_1011x449.png)

我们在 ClusterMAX 2.0 中[批评过 Lambda 的可靠性](https://newsletter.semianalysis.com/i/178057384/lambda)；这一轮测试，可靠性正是 Lambda 的重点之一。其被动健康检查覆盖相关状况，并最终自动修复了我们在测试中模拟的三处错误。两个合成 XID 在 15 分钟内被自动修复，并配有监控节点健康的面板。我们通过重置 PCIe 次级总线触发真 XID 79 的测试让节点进入 `NotReady`，没有 `GpuXid`、没有 cordon、Kubernetes 层也无监控可见性，但节点最终在 2 小时后重新加入机队。我们在 Kubernetes 层的节点重启测试也无事完成。

![](https://substack-post-media.s3.amazonaws.com/public/images/770c1ebb-c945-4e86-8ff8-cd1c0af7f664_2048x1174.png)

编排层显著改进，但仍有一把问题。Slurm 配置未设 CPUs per task，因此 Slurm 默认分配只给一个逻辑核，除非启动时显式要求更多。Slurm 上未启用无密码 **sudo**，因为我们用的是托管 Slurm 而非非托管。Lambda 是我们遇到的唯一一家做这种区分的厂商，但显然其部分客户想要自家集群的 root 权限，另一些则不（?）。我们喜欢在自己集群上拥有 root。

缺少的还有不经分配就 SSH 到计算节点。如果别人在跑作业而你无法附加到其分配、或作业卡住，调试就很头疼。这也是我们喜欢自家集群「yolo 模式」的又一个理由。

更重要的是，Slurm 上软件过期，包括默认位置 **/usr/bin/nvcc** 处的 CUDA Toolkit 12.0（老到与 B300 SM100 架构不兼容），以及不可接受的老驱动。好的一面是，Slurm 确实配置了拓扑设置，他们给我们的 NCCL 配方也工作良好。测试中我们没有遇到真实错误，所有测试（包括烤机与存储）都显示了良好性能。

我们当年对 Lambda 1-Click 集群的执念，在如今产能预订排期数月的世界里显得古雅。确实，正如开篇所述，Lambda 的利润底线日益由脱离托管集群的裸金属建设驱动。尽管如此，Lambda 的编排持续进步、客户满意，使其位居 ClusterMAX 3.0 的上游。

## Microsoft

由于微软的**官僚体系**，用 Azure 集群可能非常艰难。其工程师已尽力，但这不是一个为灵活满足客户而设的组织。在品味问题上，微软的客户不排第一。

测试期间，我们不许拥有自己的 Azure 账户，只能用某位 Azure 工程师的用户跑集群，这让我们无法逛控制台、体验真实的 onboarding。我们的 GPU 被安排在弗吉尼亚，但由于某道晦涩的内部敕令，控制面不许放在那里，而是跑在得州圣安东尼奥。访问需要搭 VPN，来回折腾了一阵（准确说：整整 3 周）才通。堡垒机上禁用粘贴，跑测试时我们只能手动敲入 GitHub 与 HuggingFace token——真的是一个字符一个字符地敲。不过我们一次就敲对了，没事 [😮‍💨](https://emojipedia.org/face-exhaling)。

一切终于跑起来后，我们发现一把过期的包，糟糕的默认 NCCL 配置让第一次运行泡汤。AKS 上 `managed-csi-premium-v2` `StorageClass` 挂不上，在 Azure Files Premium 上超过 4 个客户端跑 `fio` 就报 `EAGAIN`。Slurm 集群没有挂载并行文件系统，导致我们一个从 NFS 加载 DeepSeek-V4 的测试超时。

![](https://substack-post-media.s3.amazonaws.com/public/images/635db7a9-5287-4c8b-b77e-827a2ccea9f9_515x394.png)
*来源：一次典型的 Azure 体验*

跑烤机时，我们 Slurm 机柜上 10 个节点出了真故障，杀死了作业。微软抓到了错误，追查到一台不健康的主机，并开出 Guest Health Report 送修。一条 `scontrol` resume 命令把它们带了回来，此后我们的 Kubernetes 与 Slurm 机柜都无错完成了烤机。

我们注入合成 XID 测试 Azure 健康检查后，CycleCloud 立即 drain 了节点，但没有恢复或更换。因为我们占的是整柜 GB300，如上文「Blackwell 与 Grace Blackwell」一节所述，这是令人满意的。

由于账户问题，我们默认看不到自己的 Kubernetes 面板。Azure 工程团队转而为我们搭了一套自定义面板，细节极其丰富——对官僚紧身衣的一场漂亮突围。我们要为此给我们的朋友 Xu Xue 点个赞，因为我们相当确定他远超职责要求为我们构建了这一切、却不会承认。他精选的面板已在[这里](https://github.com/xuexu6666/aks/tree/main/gb300/vanillaarm64/clustermax#curated-dashboard-folder--azure-kubernetes-service-monitoring-gb300)开源，对任何从零搭建 Grafana 面板监控 Nvidia GPU 集群的人来说都是绝佳资源。

![](https://substack-post-media.s3.amazonaws.com/public/images/c233643e-91ca-46e4-bd17-5335a920b937_2048x1088.png)

[Satya 曾说](https://www.dwarkesh.com/p/satya-nadella-2)「我们要把 Azure 建成长尾工作负载的绝佳平台」，还说微软「不是做五份裸金属服务合同、服务五个客户的那种生意」。然而极难见到有 VC 支持的实验室用 Azure 做训练与推理。「五个裸金属客户」都说多了。其实是两家：OpenAI 和 MAI。很快会变三家，Anthropic 正在多元化。

Azure 最有趣的资产，是它能服务 OpenAI 的模型并保留 100% 收入。它们仍能完全访问 OpenAI 的全部 IP。而 Azure 还能另外夸耀与 OpenAI 的大型裸金属交易，以及与 Anthropic 日益丰厚的合作关系。这是一个极其强势的位置。若不是[那次暂停](https://newsletter.semianalysis.com/i/178649945/microsoft-and-openai-in-2023-25-from-all-in-on-ai-to-the-big-pause)的话。

由于 Azure 主要在另一个位面上竞争——海量部署与数千亿 capex——其管理集群的能力只会让它更灵活。与 Google、Oracle 一样，Azure 的现金流来自不需要帮忙设置 `ComputeDomain` 的承购方。但以测试质量看，这三家仍可以与想要更高接触体验的实验室切一些更小、利润更高的合同。

不过这短期内似乎不太可能发生。支持与控制台让人头疼，即便 Azure 是唯一一家你有可能在横向扩展网络上拿到 Nvidia 参考架构的超大规模厂商。我们也想借此验证一下：这些超大规模厂商的脚步是否依然轻快。

### Firmus

Firmus 是 Nvidia 最喜欢的新星之一，也是我们在亚太的最爱。8 月它[宣布 $2B 融资轮](https://firmus.co/newsroom/firmus-announces-fully-subscribed-usdusd2-billion-strategic-equity-investment-to-accelerate-nvidia-ai-factory-expansion-across-australia-and-asia-pacific)，投后 $10.5B，用于扩张澳大利亚、马来西亚与印尼；而仅 4 个月前它刚完成投后 $5.5B 的 [$505M 轮](https://firmus.co/newsroom/firmus-raises-usdusd505-million-in-strategic-equity-investment-led-by-coatue)。Firmus 还在 3 月为墨尔本与塔斯马尼亚的 Project Southgate 建设[签下 $10B 债务额度](https://firmus.co/newsroom/firmus-signs-multi-year-agreement-with-global-hyperscale-customer-at-project-southgate)。就在上周，它[披露总签约产能 900 MW，并宣布 OpenAI 成为其马来西亚扩张的锚定租户](https://firmus.co/newsroom/firmus-surpasses-900-mw-contracted-capacity-adds-openai-as-anchor-customer-and-expands-into-malaysia)。总而言之，Firmus 已披露 18,400 张 GB300 GPU 在部署中、今年晚些时候在塔斯马尼亚再加 36,800 张，pipeline 里还有数 GW 与数万张 VR。

测试 Firmus 的一个开发集群，我们起飞颠簸、降落却相当平稳。要拿到芯片，得用 Microsoft Entra 账户过 Microsoft SSO，再下载并配置一个 pre-release 版的 vCluster CLI。我们是新技术的舔狗，但涉及集群访问，我们宁愿直接 SSH。与 Firmus 团队几轮往返后，我们上去了。

![](https://substack-post-media.s3.amazonaws.com/public/images/22591118-db8b-43f6-b570-fe9cadbdff30_2048x1098.png)

……上了集群，但还没真正跑起来。Kubernetes 与 Slinky 的默认设置都有很多可挑剔之处。Slurm 登录节点没有 `sudo`、没有 `vim` 或 `nano`，HPC-X 装了但不在 `PATH`，也没有 NVCC。更重要的是，我们没有如预期那样在两个机柜上分别拿到 4 个 Slurm 节点与 4 个 Kubernetes 节点，而是每柜各 2 个。这本身未必是问题，但 Kubernetes 侧配了 `[nvidia.com/gpu.clique](http://nvidia.com/gpu.clique)` 却没有任何东西消费它，而 Slurm 用的是 `topology/flat`。于是每个编排器可见的节点都横跨多个机柜，又没有任何机制避免多节点作业无谓地跨越机柜边界。我们只能自己推断节点命名规则，确保测试摆放得当。

除此之外，测试期间 Kubernetes 控制面的 `etcd` 可见性闪烁了几次，杀死了我们的作业并导致 Slurm 与 Kubernetes 两层重启。最终归因于一次交换机固件升级问题，此后 10 天未再复发。我们还因一次重启中的 wedged 失去了一张 NIC，Firmus 的健康检查没抓到，因为它们在我们测的开发集群上未激活。Firmus 是我们唯一一个把 GPU HBM 暴露为 NUMA 节点的 GB300 集群——一个有趣的配置，但我们判为失败，因为主机侧溢出时它会让你意外淹没设备 HBM。WAN 时好时坏、常常很差，到 NGC 只维持 0.25 Gb/s。最后一个问题：其中一个机柜的 NVLink fabric 性能显著劣化，原因是 Firmus 在开发集群上实验的一项功率设置；修复后我们的数字回到了健康区间。

于是到测试结束时，我们有了令人满意但家当不足的 Slinky 与 Kubernetes 层，知道了怎么访问它们，测试套件能跑出强劲性能。我们理解托管集群目前不是 Firmus 的重点，但我们相信其技术团队有大量唾手可得的果子可摘。在 Firmus 把庞大产能搬上线的同时，我们期待看到他们持续让 GPU 软件栈的用户日子更好过。

### TensorWave

TensorWave 是一家纯 AMD neocloud，我们通过 K8s 与 Slinky 测了其 MI355X 产品。上次报告我们强调了 TensorWave onboarding 之艰难——光是上集群就要来回拉锯，之后还有一堆减速带。这次的改善显著：onboarding 顺畅，直接发给我们的 `kubeconfig` 完美可用，控制台能轻松添加带 SSH 访问的团队成员，TensorWave 支持团队在整个测试期间都很上心。

![](https://substack-post-media.s3.amazonaws.com/public/images/0cf70335-6a7f-4096-af05-91345833c99d_1762x1020.png)

作为纯 AMD 云，TensorWave 在应对 AMD 软件栈的战斗中逆风前行——该软件栈[尽管近期进步显著](https://newsletter.semianalysis.com/p/can-amd-break-the-cuda-moat-amd-advancing)，[仍远落后于 Nvidia](https://inferencex.semianalysis.com/)。我们在 TensorWave 集群的 RCCL 微基准上看到了这一点：即便用 TensorWave 的二进制与配方，all-gather 与 all-to-all 在 32 KiB 处挂起。其他集合操作在不同消息大小上扩展不均、吞吐不佳。[编者按：RCCL？不如叫 Rick L！]总体而言，可以说 AMD 网络栈缺乏 Nvidia 工具链那样的社区支持。硬件侧当然也一样。比微基准更重要的是，我们在实践中看到，GB300 NVL72 系统在实验室中的需求冠绝全行业：其性能优势如此之大，即便算上更高的价格，它们往往也提供最佳的每美元性能。AMD 的机柜级回应 [MI455X Helios](https://tensorwave.com/blog/tensorwave-powers-frontier-ai-growth-for-cloud-customers-with-amd-helios-rackscale-solution) 仍在[爬坡量产](https://newsletter.semianalysis.com/p/can-amd-break-the-cuda-moat-amd-advancing)，当然也尚未由 TensorWave 提供。因此，TensorWave 在榜单上的位置不仅取决于其内部改进，也取决于 AMD 持续缩小与 Nvidia 差距的工作。

就其宣传的内容而言，我们的 TensorWave 集群全面良好。南北向带宽强劲，存储性能出色，烤机无恙完成。当我们折腾 Kubernetes 层时，其可靠性良好，Slinky 层易于使用。

健康检查立即识别了我们模拟的错误，把节点带入 `drng`。

![](https://substack-post-media.s3.amazonaws.com/public/images/c7ef5150-eafb-4b86-8107-1747f6834a4a_1246x228.png)

面板奇怪地把节点标为「Allocated」，而不是单独归类。不过没过多久，就给了我们一个肥美多汁的大按钮，点一下就能批准用新节点替换我们的「病」节点。

![](https://substack-post-media.s3.amazonaws.com/public/images/1c865a25-bf2c-4979-829d-174de670437a_2048x1177.png)

更换在约 43 分钟内完成。我们更希望默认就自动修复——我们甚至不想去点那个肥美多汁的大按钮——但除此之外，TensorWave 的监控与自动修复堪称典范。

![](https://substack-post-media.s3.amazonaws.com/public/images/4a311905-19d3-45bd-9d3c-3aa8b2e1fb03_1246x718.png)

总体而言，TensorWave 是领先的 AMD 专属 neocloud，在 AMD GPU 上提供可与 Oracle、微软等超大规模厂商相媲美（有时更好）的体验。而且他们没有停步。TensorWave 已与 Fermi [达成协议](https://tensorwave.com/blog/fermi-announces-binding-lease-agreement-with-tensorwave)，在得州锅柄地带落 222 MW、并有最高扩至 650 MW 的权利，取决于 Fermi 落实项目融资。6 月 [$350M B 轮](https://tensorwave.com/blog/tensorwave-raises-350-million-series-b-at-1-55b-valuation-to-expand-global-amd-powered-ai-infrastructure)投后 $1.55B 是一股东风，目前正与超大规模厂商洽谈大单。随着 [OpenAI](https://openai.com/index/openai-amd-strategic-partnership/) 与 [Anthropic](https://ir.amd.com/news-events/press-releases/detail/1292/amd-and-anthropic-announce-strategic-partnership-to-deploy-up-to-2-gigawatts-of-amd-instinct-mi450-series-gpus) 都宣布与 AMD 就 MI450 世代达成战略合作，我们预计 TensorWave 将受益，纯 AMD neocloud 有望冲进黄金级。我们期待在可用时测试 TensorWave 的 MI455X Helios。

### GMI

GMI 是一家总部在 Mountain View、根在台湾的 neocloud。去年 11 月[宣布 $500M Nvidia 交易](https://www.gmicloud.ai/en/blog/gmi-cloud-brings-taiwans-first-ai-factory)、今年 3 月[再加 $12B](https://www.gmicloud.ai/en/blog/gmi-cloud-announces-1gw-sovereign-ai-infrastructure-in-japan-accelerated-by-nvidia-vera-rubin-nvl72-tm)，pipeline 里有数百架 GB300 机柜、后续还有 VR 计划，硬件上他们一直踩在前沿。最近，他们还通过与较小的 neocloud 签约、把算力转售给既有客户群来扩张机队——这种模式现金流诱人，因为不需要前期资本支出。在 [ClusterMAX 2.0](https://newsletter.semianalysis.com/p/clustermax-20-the-industry-standard) 判其「青铜级最佳 neocloud」之后，我们有意测试其托管集群的进展。

Onboarding 有点颠簸：从控制台下载的 Kubeconfig 是空的，我们上传的 SSH 密钥也从未同步到集群。与团队几轮往返后，我们进去了。问题原来是控制台对我们这轮测试是只读的，所以我们无法验证其功能。上一轮我们根本没有自助控制台可用，所以这算进步。

与上次一样，计算达标、烤机干净、InfiniBand fabric 扎实。相对 ClusterMAX 2.0 的一个显著进步在 GMI 的存储：GMI 提供了高性能的 RWX NFS 默认 StorageClass，Slurm 层的 `/home` 上也可用。我们试 GMI 的 S3 时遇到困难，结果发现是他们文档里的一个 typo。等~~卡拉马佐夫~~Karasev 兄弟跳上电话会议修好之后，我们验证对象存储性能同样良好。集群配置上最大的阻碍是：GMI 期望通过 ComputeDomain CRD 在 Kubernetes 集群上配置 IMEX 域。这完全可行——许多其他高评级厂商也这么做——但 GMI 的 Kueue 不容忍该 claim，于是我们的作业干坐在 `Suspended`。绕行的办法是把作业提交到一个没有名为 `default` 的 `LocalQueue` 的命名空间。我们建议 GMI 在文档中写明 MNNVL 作业需要跳过队列，或者——更好——把 Kueue 配置成容忍 DRA resource claim。

GMI 的面板（上次测试时还不存在）很有用，包括来自 DCGM 的硬件信息以及 NVLink 与 InfiniBand 监控。

![](https://substack-post-media.s3.amazonaws.com/public/images/a43db568-8572-4364-bf82-2a54b367c68a_2031x1230.png)

由于缺乏备用产能，我们没能完整体验 GMI 的健康检查，但能测的部分表现良好：节点在 Kubernetes 层被迅速 cordon，随后重启并自动 uncordon。注入合成错误后，Slurm 层也很快把一个节点带入 `DRAIN`。GMI 在 Slack 里设了告警，因此我们能看到他们的系统检测到错误、以及与支持讨论后续步骤的线程，这很方便。

我们的 GMI 体验在每个关键方面都很扎实，期待在其产能快速爬坡的同时继续测试。

## 青铜级

### Amazon Web Services（AWS）

上一份报告把 AWS 体验总结为「头痛」。这一次，我们不得不拿出*Amazon Basic Care 布洛芬片：退烧、缓解身体酸痛、头痛、关节炎疼痛等，棕色瓶装 200 粒*，才把测试熬完。

AWS 的难，在你上集群之前就开始了——甚至在你想开通集群之前：它始于你凝视 AWS 那座托管产品动物园之时。为了理清这一切，我们不得不画了一张维恩图：

![](https://substack-post-media.s3.amazonaws.com/public/images/870e9761-ea42-466a-a72a-1b1763e21d5f_1700x1650.png)
*来源：实习生（我忘了他叫啥）*

（*读者慎入（Caveat lector）*：对 AWS GPU 产品细节不感兴趣者可跳过本段。）[SageMaker](https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-mlconcepts.html) 是 AWS 的全托管平台，面向最低维护场景。如果你不想碰任何基础设施，它提供[serverless 模型定制](https://docs.aws.amazon.com/sagemaker/latest/dg/customize-model.html)与[数据科学环境](https://aws.amazon.com/sagemaker/unified-studio/)，把底层计算抽象掉。再上一层是 [SageMaker HyperPod](https://aws.amazon.com/sagemaker/ai/hyperpod/) 产品线，同时支持 [Slurm](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-slurm.html) 与 [EKS](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-eks.html)。HyperPod 产品线为想保留 `ssh` 或 `kubectl` 访问的用户开箱提供诸多便利，如[健康检查](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-resiliency-slurm-deep-health-checks.html)、[自动修复](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-resiliency-slurm-auto-resume.html)、[面板](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-cluster-observability-slurm.html)，以及[无检查点训练（checkpointless training）](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-eks-checkpointless.html)等工作负载级特性。如果你想要基础设施被抽象、但 ML 栈自己管，可以走出 SageMaker 大伞，选择 [EKS Auto Mode](https://docs.aws.amazon.com/eks/latest/userguide/automode.html)，它负责节点开通、自动扩缩、OS 打补丁与节点维修。EKS Auto Mode 是包在「托管 EC2 实例」之上的一层，但它们并非真正意义上的 EC2 实例：不出现在 EC2 控制台里，也不提供普通 EC2 实例那种可定制性。在 EKS Auto Mode 中，用户无法访问控制面，而且必须允许 AWS 出于[安全原因每 21 天回收一次 worker](https://docs.aws.amazon.com/eks/latest/userguide/automode.html#:~:text=21%20days%20%28which%20you%20can%20reduce%29)。最后，要更大的可定制性，还有 [EKS + Karpenter](https://docs.aws.amazon.com/eks/latest/best-practices/karpenter.html)，用户可以用开源工具 [Karpenter](https://karpenter.sh/) 自管自动扩缩。

尽管亚马逊以「[客户痴迷](https://www.amazon.jobs/content/en/our-workplace/leadership-principles)」著称，这份小说篇幅的 GPU 菜单显然是「[你交付的是你的组织架构图](https://en.wikipedia.org/wiki/Conway%27s_law)」这句格言的绝佳例证，而非真实需求分层的反映。而且一旦你下了单，官僚之苦丝毫未减。这是对组织的批评，不针对任何具体团队——AWS 有点[三世纪危机罗马帝国](https://en.wikipedia.org/wiki/Crisis_of_the_Third_Century)的味道。要在下一轮 ClusterMAX 测试中提升排名，我们建议 AWS 换一个帝国和/或时代作为参照。

不过，这些产品有一个统一特征：第一次开通必定失败。于是我们又画了一张澄清用的维恩图：

![](https://substack-post-media.s3.amazonaws.com/public/images/96cb228c-6606-4934-9672-72ef4487dd7f_1700x1560.png)
*来源：同上。*

这终于把我们带到 AWS 的运维者体验。我们在控制台开通的一个 SageMaker 集群因 IAM 权限不足而失败。有些 EKS 集群用 Terraform 简化开通，但这条路未经战火检验：要求你处在正确的（在途）仓库的正确分支的正确 commit 的正确子目录里，还要准确知道该拧哪些旋钮才能不发非法请求。一个集群起来时没有 Lustre，而且无论与 AWS 工程师往返多久都不让挂载。为测试计，我们在新区域开了一个新集群来收集文件系统性能数据；但如果我们是真实世界的实验室，这至少短期内是瘫痪性的。与我们合作的 AWS 团队始终乐于帮忙，但显然他们既没有放手解决问题的自由，也缺乏对系统全貌的洞察，尤其是与我们对标的那些扁平、敏捷的 neocloud 相比。本不该需要六位工程师开好几个电话会才能开通一个 Slurm 集群。

货送到之后，没有什么拦路虎阻止我们开箱拿到合理性能。驱动、固件与大多数实用工具都是最新的。不过这对 AWS 这种有信誉的厂商只是最低要求，别处的毛刺也不少。

我们受测 AWS 集群与其 B200 同侪的一个基本差异点是：AWS 使用其专有横向扩展 fabric——Elastic Fabric Adapter（EFA）。测试中，EFA 峰值吞吐强劲。在 B200 上经 EFA 跑四节点 32 GPU all-to-all [NCCL](https://en.wikipedia.org/wiki/Settler_colonialism) 测试，我们在 16 GiB 消息大小下测得 59.44 GB/s busbw，考虑到跨节点边界的流量比例，约合横向扩展线速的 92%。在其他流量模式与启动机制的网络测试中，只要消息足够大，吞吐位列最佳 B200 集群之列。然而，EFA 的时延始终逊于调校良好的 InfiniBand 同侪。例如消息大小降到 64 KiB 时，同样的四节点 32 GPU all-to-all NCCL 测试在 EFA 上花 85.26µs，而在 InfiniBand 同侪上不到 50µs；在时延主导的小消息测试中，EFA 与 InfiniBand 这 30-40% 的差距始终存在。这看似吹毛求疵，但横向扩展时延对现代[专家并行](https://inferencex.semianalysis.com/glossary/expert-parallelism)工作负载是关键指标——这类负载频繁跨节点边界发送小 token 向量。比如这个 64 KiB NCCL 测试就与 Kimi K3、DeepSeek V4 这类模型的专家路由步骤相似。我们的发现与 [Perplexity 一篇关于优化 EFA 的精彩技术博客](https://research.perplexity.ai/articles/enabling-trillion-parameter-models-on-aws-efa)相互印证，其报告了类似结果：EFA 峰值吞吐令人满意，但在「MoE dispatch 与 combine 期间交换的消息大小」上要多付约 20µs 的时延惩罚。（注意 Perplexity 那篇文章对比的是 ConnectX-7 NIC，我们测的是 ConnectX-8，但两代标称吞吐相同。）当 Perplexity 那些神级工程师在写极其详尽的长文、讲解如何在你的定制网络栈上「启用」基础功能时，这可不是好信号。

![](https://substack-post-media.s3.amazonaws.com/public/images/8af3c70d-f9ae-43c4-afb5-98722cd154cb_2048x1253.png)
*EFA 上的 all-reduce 测试。注意消息大小要翻很多倍，完成时间才有明显变化；这是因为在小消息下，决定性能的是时延而非线速。*

在上游 vLLM 与 SGLang 中，EFA 上的专家并行推理仍需额外设置。AWS 报告过成功的 vLLM 部署，但用户必须安装 EFA 用户态库，并用 EFA 支持构建相关通信组件——视工作负载可能包括 DeepEP、NIXL 或 Mooncake Store。[AWS 的 DeepEP fork](https://github.com/amazon-contributing/DeepEP) 通过 NCCL GIN 支持 EFA；[DeepEP V2](https://github.com/deepseek-ai/DeepEP) 使用 NCCL GIN，其基于 NVSHMEM 的 V1 路径现已标记为 legacy。上游集成与默认容器打包仍需努力。NCCL EP 是开发中的另一条路；所附 vLLM 集成仍是[草稿 PR](https://github.com/vllm-project/vllm/pull/56241)。总体而言，EFA 不是前沿通信库的优先事项，用户要等数周乃至数月才能得到有限的支持。

AWS 是唯一一家在这方面如此特立独行的云。我们测的其他所有厂商都用 InfiniBand 或 RoCE。当然，AWS 那些 GW 级交易的客户有资源把 EFA 调好，但我们仍认为，最大厂商的横向扩展栈独一份地难缠，是一件憾事。

换个角度看，存储是另一个常常不配合的基础集群服务。我们在 `ap-south-1a` 开的 B200 集群对每个存储请求都报含糊的 `Insufficient capacity` 错误，而那些 `Failed` 文件系统删了 5 小时 46 分 55 秒。

![](https://substack-post-media.s3.amazonaws.com/public/images/bf42d75a-3a29-49ae-b581-025db99bce52_1244x252.png)

要测 Lustre 性能需要换区域再开一个集群，意味着又一场旷日持久的 bring-up——又一个盯着终端、试图分辨 Terraform 是否在推进的夜晚。

![](https://substack-post-media.s3.amazonaws.com/public/images/d91b500f-d3b9-4fd0-a3a0-77a6d644b532_2048x1218.png)
*来源：开通炼狱。*

在 AWS 上用 Terraform 申领存储就像养娃：你只能看着，祈祷它破坏完之后会开始创造。而存储创建出来之后，访问也未必顺畅。Kubernetes 层上，一个集群默认不提供 StorageClass，唯一自带的 StorageClass 又因驱动不对让我们的 PVC 永远 `Pending`。我们只能自己定义带正确 provisioner 的 StorageClass。

通电联网之后，存储性能喜忧参半。所提供的 [FSx 在普通缓冲 I/O 上挣扎明显](https://github.com/SemiAnalysisAI/ClusterMAX-internal/blob/d039ae43c09bc20e32cfea67469f80069e90d2a8/runs/aws-eks-karpenter-b200/20260729-094037/tests/fio/fio.values.json#L34)：fio 测试中 p99 顺序读时延高达 9.2 秒，而同一指标在关闭缓冲时为 312 毫秒。缓冲设置下时延更高可以预期，但这是病态级差距。

AWS 健康检查的表现同样喜忧参半。我们的 EKS Auto Mode 集群抓到了注入的 XID，置 `AcceleratedHardwareReady=False`，并在注入仅 24 分钟后给了我们一个健康的新节点。与此同时，我们的 SageMaker HyperPod Slurm 集群立即检测到 XID、把节点带入 `DRAIN`、完成了大部分重部署流程，却在最后被自己的脚绊倒：它要求先过一次深度健康检查才能重新入队，而该深度健康检查是作为 Slurm 作业提交的，要等到节点被加回机队后才能被调度。于是运维者必须手动推一条 `scontrol ... State=RESUME`，机队才恢复健康。在我们反馈后，AWS 迅速修复了这个循环依赖，在单台 H100 节点上的复测无需介入即成功。变好了。

我们 EKS Karpenter 集群的健康检查更是自败。`dcgm-server` DaemonSet 不容忍 `[nvidia.com/gpu:NoSchedule](http://nvidia.com/gpu:NoSchedule)` 污点，所以没有附到 worker 节点上，导致监控代理报 `error connecting to nv-hostengine` 并以 `Reason=DCGMError` 翻转 `AcceleratedHardwareReady=False`。Karpenter 随即把 `NodeClaim` 标记为待终止，替换节点因同样原因被标为不健康，系统原地转圈，直到我们手动改 DaemonSet 让它容忍 GPU 污点。健康检查还发生了另一次过敏反应：它注意到 IMEX 守护进程没有被调度。IMEX 负责跨节点配置 NVLink fabric，但我们的是普通 B200 节点经 EFA 通信，IMEX 无事可做：这个守护进程落不了地本应无害。结果监控日志发出了精神分裂式的消息

**ignoring IMEX health code on non-NVLink multi-node system, code=122**

**sending condition to exporter,**

**Reason=NvidiaFabricError,**

**Severity=Fatal**

如果我们没有手动把 **NodeRepair=false** 钉住、拦住过度热情的垃圾回收来阻塞我们的工作，这又会回收掉一个健康节点。最后，临近测试收尾，Karpenter 在 **EndDate** 前 39 分钟拆掉了我们的 B200 集群，强制驱逐了一个进行中的 4 节点 MPIJob。我们在这里说得这么细，是因为这些 bug 对世界最大的云来说低级得几乎难以置信。AWS 生命周期中唯一无痛的部分，或许是 Karpenter 的扩容与缩容——几分钟内无错完成。然而 GPU 产能必须大块、提前锁定，因此 Karpenter 的敏捷自动扩缩是个毫无意义的功能。

尽管产品问题多多，我们接触的 AWS 专家与工程师聪明而响应迅速。他们急于展示改进、征求文档反馈、回头修正测试中的错误，甚至做了一个漂亮、前瞻的 [MCP 服务器](https://awslabs.github.io/mcp/servers/sagemaker-ai-mcp-server)，其技能被我们薅进了自己的代码库。AWS 的问题出在组织结构。以 AWS 的资源，居然有这么多基本问题从网眼里漏下去，令人惊叹。

2 月，AWS [宣布与 OpenAI 的交易扩大 $100B](https://press.aboutamazon.com/2026/2/openai-and-amazon-announce-strategic-partnership)；2Q26 其[净销售额同比增长 37%](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000024/amzn-20260630xex991.htm)；[Trainium 业务 ARR 达 $25B、同比三位数增长](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000024/amzn-20260630xex991.htm)；[其对 Anthropic 的投资正以每年数百亿美元的速度增值](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000024/amzn-20260630xex991.htm)；Bedrock 继续[在夯基础般的收入上赚夯基础般的利润率](https://newsletter.semianalysis.com/p/anthropic-growth-and-bedrock-mix)。

托管集群不是 AWS 的优先级。

### Gcore

Gcore 是一家「卢森堡-ish」的 neocloud，在一个名叫「欧洲」的暧昧地区建设，依靠其他厂商提供产能。它们近来没有浮夸的公告，不过正在为 Hopper 机队添置 Blackwell。ClusterMAX 2.0 中我们测了其经 Soperator 提供的 Kubernetes 与 SonK，给了白银。这次我们只又试了 SonK。

我们对 Gcore 能力的了解受限于其产能不足：多数厂商至少给 4 个 B300 节点至少一周，而 Gcore 紧到只能匀出 3 台 H200。不过这个集群上让我们忙活的东西也不少。

![](https://substack-post-media.s3.amazonaws.com/public/images/45cb65a8-b84d-4b13-99cb-24afea4c0cce_2024x286.png)

我们在 Soperator 层的测试需要与 Gcore 团队几轮往返来修毛边，但团队始终热心。当我们的首轮扫描大多因一个阻止非 root 用户运行工作负载的错误配置而失败时，团队迅速回应，确认 `kernel.apparmor_restrict_unprivileged_userns=0` 能解锁。当每个 Slurm worker 报 `RealMemory=2048 MiB`（显然错误地继承了 CPU 配置）时，Gcore 团队再次快速修复了又一个糟糕默认值。这曾让我们连 `nvidia-smi` 都跑不了，我们很高兴看到它迅速被修复。

![](https://substack-post-media.s3.amazonaws.com/public/images/4ede5496-e7a8-469c-96f7-97530bc48a7e_2048x126.png)

Soperator 层默认禁用节点间 SSH，让调试略添难度，但团队指给我们一个 `soperator-createuser` 便利脚本让日子好过些。测试期间团队还排查了其面板的一个错误。

![](https://substack-post-media.s3.amazonaws.com/public/images/0fe89460-79f5-4eeb-bd38-db18f40971f6_2048x1214.png)

Kubernetes 层没有默认 StorageClass，用户必须显式选择 NFS。Slurm 层的存储配置得当，用的是 Soperator 易用的默认方案——NFS 挂在 `/`——营造出单一共享卷接到所有节点的幻觉。该存储在各工作负载下表现良好。N/S 网络不错，E/W 网络最终达标，但 RDMA 设备名非标准、又没有 `topology.conf`，配置要多走几步。

我们注入的 XID 被迅速抓到并显示在 Grafana 里；有意思的是，节点在 Slurm 层进入 `Down`，而 Kubernetes 层毫无变化——尽管注入就是经由 K8s 做的。因为 Gcore 没有备用产能，我们无法测自动修复。

![](https://substack-post-media.s3.amazonaws.com/public/images/49a763f9-8c8b-44cd-8b93-ce1bda77006b_2048x1149.png)

Gcore 的细心与其经打磨后能做对基本功的 Soperator 产品令我们印象深刻。我们期待测试 Gcore 的 B300/GB300 管理（包括对 XDR ConnectX-8 NIC 的处理），并看其 Soperator 与 Kubernetes 产品的改进。

### GMO

GMO 的托管 Slurm 集群在两个 B300 节点上交出了强劲的网络与存储性能。主要缺口是受限制的 profiling、有限的企业管控与缺乏自动修复。

Slurm 交付时 head 节点、分区与 topology.conf 均已配置。驱动与 CUDA/NCCL/HPC-X 模块在节点间保持最新且一致，Pyxis 可用。Onboarding 直接了当，虽然纯日文控制台需要我们手动 ctrl+c、ctrl+v 翻译才能看懂。

![](https://substack-post-media.s3.amazonaws.com/public/images/df12c9e5-7529-4849-897c-d4198170d523_1226x667.png)
*来源：想象你是只上过两节日语课就退课的 SemiAnalysis 实习生，正试图找到 Grafana 面板*

Grafana 访问花了我们五天排障：先漏看了 macOS login-keychain 说明，又把证书密码填进了要系统密码的地方。GMO 调查并多次跟进。最后一个错误在我们，但更清晰的证书说明本可省时——或者，别用不必要的自定义证书来访问网站。日本式安全表演再度上演。

![](https://substack-post-media.s3.amazonaws.com/public/images/91ea0e60-f11b-4708-ae48-23cf601addd6_1111x913.png)
*来源：试图访问我们的 Grafana 面板*

每节点 16 条 400 Gb/s 轨道交出了强劲的 NCCL 结果，不过两节点比我们惯常的四节点下限提供的扩展证据要少。MPI 启动需要显式 NCCL_IB_HCA 设置，GMO 称已在 nccl.conf 里提供，但起初对我们不奏效。烤机无网络错误、无重试、无 ECC 错误，温度与功率正常。

共享 home/data/work 目录开箱即用。FIO 顺序读写、随机读与 torch.save 都扎实，构建在调校良好的 DDN Lustre 之上。但我们那些刻意的测试（共享存储上的 `import torch` 与 vLLM Serve）表现很差；GMO 表示可以排查，但我们把它归因于经典 Lustre 元数据性能调优问题，继续往前走。与许多其他 Lustre 实现一样，GMO 的存储产品缺少快照、自动备份与容灾选项。

集群还没有 `sudo`、worker 上没有 Docker，并且要求用 **snodes**——他们自建的一个展示集群元数据的便利脚本——因为他们阻止用户在自己的集群上运行任何 **scontrol** 命令。安全表演again。

最后，到 worker 节点的 SSH 也被屏蔽。而在 Slurm 作业内，`RmProfilingAdminOnly=1` 阻止了 Nsight Compute 的 GPU 计数器，perf 也不能满足我们的 profiling 需求。我们认为，选择 yolo 模式的托管集群应当允许用户对自己的工作负载做 profiling。我们想要，但 GMO 提供不了。

最后，Grafana 暴露了有用的 DCGM 指标，但缺少我们喜欢的 XID 检测、估算 TFLOPS、SM Active 与 SM Occupied 视图，难以胜任性能与可靠性监控。Slurm 作业汇总视图也比较简陋。我们合成注入的 XID 79 日志没有引发任何可观察的告警或节点 drain。GMO 说他们在 Slurm prolog 里跑 dcgmi health，确认 XID 79 不在白名单，并同意未来排查。我们以「GMO 缺少任何自动修复体系、至少我们无法验证」结束了测试。

![](https://substack-post-media.s3.amazonaws.com/public/images/0fd9aa99-91e9-423f-8096-cf04312f20c9_1312x888.png)
*来源：我们在 GMO 上的 Grafana 面板！*

总体而言，GMO 缺少 Kubernetes 与企业特性（RBAC、SSO、客户可访问的审计日志），使其归属于有效服务日本市场的利基本地玩家。我们与其团队的支持体验是有帮助的，但遵循标准日本办公时间。展望未来，我们预计 GMO 会继续是日本的领导者，但缺乏将业务扩张到本地地理之外的雄心。

### Verda

总部在赫尔辛基的 Verda（前 DataCrunch）今年 6 月[披露 $100M ARR 与 $200M 总融资](https://verda.com/blog/100m-revenue-run-rate)。他们与 Nvidia 保持密切关系，并继续激进地寻求融资。技术方面，自我们 11 月测试以来他们落地了一批功能，我们对他们的工程团队与路线图持乐观态度。

上一轮，Verda 的 Slurm 还在官方 beta，也不提供 Kubernetes。这一次，他们提供托管 Kubernetes，并把 Slurm 产品迁到 Slurm-on-Kubernetes 以简化部署。我们在 Slurm 与 K8s 两层都测了；毛边不少，但代表显著进步与持续开发的坚实起点。我们还发现安全扎实。

![](https://substack-post-media.s3.amazonaws.com/public/images/1eba537c-4823-4331-9aca-a3f6d9937dd0_2048x1180.png)

购买与 onboarding 顺畅，集群 30 分钟无障碍开通。Grafana 面板开箱即用，我们 SSH 上集群也无事。

![](https://substack-post-media.s3.amazonaws.com/public/images/a56ff15e-9317-41f5-ac49-5bc36feb1a2c_1318x1213.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/45655420-db56-4293-a8d0-80a50c59c73a_2048x1177.png)

不过上集群之后路上有些坎。我们的 Slurm 测试从一个有意思的坑开始：SSH 进去时我们以为在 Slinky 层，实际上落在了外层 VM 上，它包了一层命令、通过 `kubectl exec` 进入 `LoginSet` 来跑 `salloc`、`sinfo` 等。行为很反常——比如所有 Slurm 命令把我们升到 `root`，我们的 Python 环境也消失了——花了一个晚上调试，我们才拼明白：我们的 Slurm 访问是幻觉，要用另一条 SSH 命令才能正确进入 Slinky 层。

![](https://substack-post-media.s3.amazonaws.com/public/images/22583e07-2129-4410-bcfc-c0dcf855b317_1500x139.png)

Verda 的工程师响应迅速，很快开了一通支持电话，合情合理地解释了这些便利功能背后的考量，并指给我们受支持的路径。虽然这个功能害我们头疼，但工程师愿意费心让集群更好用，是件看多的事。

Slinky 层可用但不完美。Verda 跑了一个超过 Slurm 10 秒 `MessageTimeout` 的 NCCL-test prolog，导致每次分配都出现一条吓人但无害的 `Prolog hung` 告警。更重要的是，Verda 不支持 Pyxis 或 Enroot，我们只能靠一个巨大的 `.sif` 文件搭环境。绕行方案就绪后，我们无恙完成了 8 小时烤机，微基准数字令人满意。

![](https://substack-post-media.s3.amazonaws.com/public/images/e9d03267-f400-43ca-88a6-32280b0f55e7_1716x227.png)

与此同时，Kubernetes 层只能经堡垒机操控，控制台无法下载 `kubeconfig`。把 Verda 产品对齐到用户标准工作流，这是个相对简单的修复。

性能扫描中暴露的最大短板是共享文件系统。总吞吐数字优秀，但跨节点文件锁似乎根本没被强制执行：`flock()` 与 `fcntl()` 跨节点 100/100 次独占锁违约，而同节点对照组拒绝了每一次尝试。这强烈指向 `virtiofs` 未能公布锁行为的问题。我们还看到多客户端从 Hugging Face 下载时数据损坏，以及 32 客户端 Elbencho 的 `ENOENT` 失败。这也是唾手可得的果子，而且在跑 Slinky 时共享文件系统可靠与否根本重要。

最后，Verda 的健康检查程序尚未配置完全。它们是字面意义的「健康检查」——评估节点是否健康——但没有任何东西消费其输出：它们 exit `1`——「对，这台死了」——然后继续。因此，不想让坏节点悄悄杀掉工作流的用户必须自带可靠性套件。Verda 当然也没有提供自动修复。

Verda 沟通始终及时清晰，其工程师似乎既有自由也有动力改进产品。9 月 10 日，在我们的测试完成后，他们[向 Instant Clusters 推送了一批改动](https://verda.com/blog/instant-clusters-h1-2026#gpu-cluster-health-checks)，看起来是有分量的。我们期待看到他们继续打磨 Slinky 与 Kubernetes 产品的边角、调优存储系统、并实现稳健的健康检查与自动修复。

### Moonlite

[Moonlite](https://www.moonlite.ai/) 是一家总部在芝加哥的 neocloud，ClusterMAX 3.0 的新入选者。创始团队出自 Crusoe，目前运营一支 Hopper 机队，最近交付了首批 B300 与 GB300，未来几个月将持续爬坡。据 LinkedIn，Moonlite 是本轮与我们合作的公司里人最少的，且以工程为中心。

我们测了 Moonlite 的 Kubernetes 与 Slinky。交接顺畅，onboarding 文档定义了经过验证的配方，Kubeconfig 给了我们所需的一切。默认情况下 Slinky 上所有人共享同一个 root 用户；我们提出要非 root 用户后，Moonlite 在半小时内做了个 `moonlite-adduser` 便利脚本，并当天烘进了登录 pod 镜像。这既显示 Moonlite 对反馈的响应，也显示其稚嫩。我们喜欢这种响应，但更希望有一套久经战火的系统——最好通过控制台——来处理这类基本功。

硬件方面，我们测的一切开箱良好。NCCL 测试达到 ConnectX-7 规格，NFS 良好，计算基准扎实，烤机无恙。不过要再说一遍：我们测的是 H100——业界如今已驾轻就熟，因此比其他厂商的 GB300 NVL72 更容易做对。尽管如此，我们对 Hopper 性能满意。

系统里一个我们无法测试的组件是 NVMe——存在但访问不到。没有任何东西暴露它：没有 local-path `StorageClass`，`hostPath` 不可用，而 Slurm worker 是只有 VAST `/home` 的 Slinky pod。Kubernetes 层完全没有默认 `StorageClass`，未限定的 PVC 挂在 `Pending`。

我们通过 PCIe 次级总线重置测试了 Moonlite 的健康与监控系统，Moonlite 在 11 分钟内告警了我们。经我们许可，他们 cordon 节点、跑诊断，总计 57 分钟后将其交还机队——其中包括他们等待我们指示如何处理的几分钟。实际场景中，他们会与真实客户预先定义策略，让团队按具体错误照 runbook 执行。Moonlite 的典型 SLA 是 15 分钟内响应，其团队通过 Slack 与 PagerDuty 收告警。我们从其客户那里听到的正是：到目前为止他们确实做到了。

在我们看来，任何能在一小时内把机队恢复满编的自动修复流程都算合格。但人工流程虽可接受，规模化后我们希望看到自动化。我们还希望在出错时集群有更好的可见性：从重置到 Moonlite 人工介入之间，用户唯一可见的变化是节点在 Kubernetes 层保持 `Ready`，但广播的 GPU 数从 8 变成了 7。

Slinky 层的 worker 上没有任何容器运行时，但其余都完成了任务，登录 pod 上有我们要求的大部分东西。Moonlite 的 Grafana 尚可，但缺少调度层细节，也不显示最关键的信息：错误状态。

Moonlite 尝试做的事，都做得不错。我们期待在其产品成熟、手上磨出 GB300 老茧之后再次测试他们。

### Together

在 ClusterMAX 2.0 中，我们这样写 Together：

> Together 是一家强厂商，Slurm 与 Kubernetes 集群产品都很扎实，但因可靠性问题未能进入黄金级。

这一轮，Together 的问题——大体但不完全与可靠性有关——使其降至青铜级。

计算测试中我们有两个节点故障：一个回来了，另一个没打招呼就被送去 RMA，我们只能干瞪眼纳闷它去哪了。测试后期，Together 的 Slurm `HealthCheckProgram` 试图在已被调度的节点上、于 45 秒超时内跑 `dcgmi diag -r 1`；诊断没落地，超时被误读为失败，节点在运行中被 drain。Together 拿到我们的反馈后迅速修复。另有一次，我们的一个节点因存储 NIC 处于 `operstate=down` 而无法访问 VAST，Together 解释是其新轻量 VM 栈中 NIC 初始化的竞态所致。没有任何机制抓这个错，只能人工介入重新部署健康节点，把测试机队补回 4 台。我们喜欢「缩短集群开通时间」的说法，但显然不喜欢看到它影响可靠性。

![](https://substack-post-media.s3.amazonaws.com/public/images/6d454aea-e52e-44f2-8250-0c8b0ad86720_2048x874.png)

Together 的健康检查在某些场景确实正确工作，较 [ClusterMAX 2.0](https://newsletter.semianalysis.com/p/clustermax-20-the-industry-standard) 有进步。当我们在 Slurm 集群触发 PCIe 次级总线重置时，节点在 67 秒内被 drain，自动节点更换在 35 分 7 秒内无人工介入完成。一次合成错误也在 Kubernetes 层 cordon 了节点，并因为我们关着 `Auto Repair` 而正确地未触发自动修复。

Together 的 Kubernetes 与 Slinky 层都能用，不过有一些麻烦。有意思的是，Together 建议避免使用 Slinky 集群的 Kubernetes 层：要把 Slinky 节点转成 K8s，我们被指示先拆掉再以原味 Kubernetes 重开。因此其 Slinky 产品应按纯 Slurm 评估。把痛点尽量简述：OCI 镜像解压因 `/tmp` 默认设置而失败，我们只能把解压重定向到 `/scratch`；此时 Slurm 竟然照常 exit `0`；NFS 拒绝任何含 `:` 的文件名；租户无权读 `dmesg`，导致无法检查 XID 事件；非登录的 worker shell 的 `PATH` 里既无 `nvcc` 也无 `mpirun`，普通批处理脚本与交互环境行为不同、缺工具。没有一条致命，但加上其他更小的错误，我们花了几个开发日才能畅通无阻地跑自己的东西。奇怪的是，Together 的公网对多数服务吞吐强劲，但连 Canonical 的 Ubuntu 归档源反复建立失败、连接后卡死、或传输低于 20 kB/s，又把我们晾在集群搭建的半路。

一次公网 IP 检查确认，这台不稳定的 B300 集群属于 `AS53735 IREN`。这座 N+0 的 Prince George 数据中心，与 Crusoe 那被诅咒的雷克雅未克站点并列，是业内以不可靠著称的两座数据中心之一。我们强烈怀疑这两座至少有一座没有以「[土地承认仪式](https://x.com/SemiAnalysis_/status/2093805994493034883)」（Land Acknowledgement）开过光。我们知道多家极其不满的 Together 客户，苦于链路抖动、电力问题、集群访问被切断、未经用户批准的随机升级出错且不回滚、以及最终被甩锅给单一 ISP 的整周末宕机（对，这个站点只有一家 ISP——加拿大北部没有冗余）。也许他们别的站点更好，但 IREN Prince George 的 TogetherAI 站点完全是糟糕的。

甩锅游戏玩了一阵之后，很清楚：可靠性问题不能全怪底层供应商。客户支持工程师的无压失误（unforced errors）已造成客户与厂商之间的信任缺失。

当然，托管集群不是 Together 的饭碗，也不是其主要收入来源。7 月其[宣布 $800M C 轮](https://www.together.ai/blog/announcing-our-series-c)时，公告对其托管集群业务至多一笔带过，反而强调「Together AI 是一家研究驱动的公司」。其[沙特 250MW](https://finance.yahoo.com/technology/ai/articles/together-ai-humain-form-strategic-120000648.html)的承购方尚未披露，但我们知道 Together 更想按 token 而非按 GPU 小时收费。尽管如此，我们希望 Together 能真正「Together」起来，解决集群可靠性问题，让它的 Slurm 与 Kubernetes 产品成为值得骄傲的东西。

### Crusoe

ClusterMAX 2.0 的 Crusoe 一节以谨慎收尾：

> Crusoe 面临降级到 ClusterMAX 白银的风险，因为其许多顶尖个人贡献者工程师离职，其云部门的文化开始变得像大厂。整个组织、尤其是工程部门中层管理者太多。这导致发布缓慢得难以置信（比如其 AutoClusters 功能），令我们对 Crusoe 公有云产品的未来感到担忧。Chase 如果不想失去他的全部 10x 工程师、并随之失去 neocloud 生意，就需要迅速调整航向。

自那段话发表以来八个多月，Crusoe 也赢了不少。估值从约 [$10B](https://www.globenewswire.com/news-release/2025/10/24/3172932/0/en/Crusoe-the-AI-Factory-Company-Raising-1-375-Billion-at-a-Valuation-Above-10-Billion-to-Power-the-Future-of-AI-Infrastructure.html) 涨到 [$30.9B](https://www.crusoe.ai/resources/newsroom/crusoe-announces-series-f-funding)，在得州宣布了 [900MW](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-900-mw-ai-factory-campus-in-abilene-texas-to-support-microsoft-ai-infrastructure) 与 [1.0GW](https://www.crusoe.ai/resources/newsroom/crusoe-and-lancium-announce-1-gigawatt-ai-data-center-campus-in-childress-texas) 园区、[以及更多别处](https://semianalysis.com/datacenter-industry-model/)，仍是[乐高数据中心蛮荒西部](https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters)里的创新者。他们拥有所有数据中心建设者中最实在的 pipeline。

收购 Atero 的一批神级以色列工程师之后，其推理端点业务也极受推崇。他们还与 Jane Street 等公司做成了漂亮的交易。

手头够忙、生意够旺：他们有些集群惊艳，有些却糟糕透顶。

然而本轮 ClusterMAX 测试发现，Crusoe 的 neocloud 业务转向不够快。问题回到根本：可靠性与卫生。

我们在[预期](https://www.clustermax.ai/expectations)与点评中强调健康检查，但真实硬件故障在测试中很少见，因为我们的 ClusterMAX 分配又小又短。Crusoe 打破了这一趋势。5 月我们拿到的测试 AutoClusters 的 H100 集群上，我们看到了一场令人叹为观止的 [XID](https://docs.nvidia.com/deploy/xid-errors/analyzing-xid-catalog.html) 弹幕——五天里一个集群上的真实错误，比其余全部测试加起来还多。

![](https://substack-post-media.s3.amazonaws.com/public/images/a329b23f-21d8-4161-8d1d-f6773c4f7648_710x708.png)

这个贯穿测试的模式再度出现：某些方面出奇地差，另一些方面却服务成熟——这场 XID 风暴伴随着便利的邮件：样式精美，礼貌地通知我们这些错误。

![](https://substack-post-media.s3.amazonaws.com/public/images/5fb352f0-7454-46a2-a664-06b4b3475be4_1906x717.png)

除了贡献本轮大多数硬件故障之外，Crusoe 还独享一项殊荣：我们测过的最老 Linux 内核与最老 GPU 驱动。Crusoe 此后改正了这些短板，但测试当时有若干软件版本远低于我们的最低预期：上述 NVIDIA 驱动未通过我们的 `**cmax audit security`，Docker、ConnectX 固件与 `runc` 也是。这些问题指向松弛的安全姿态与糟糕的工程卫生。

![](https://substack-post-media.s3.amazonaws.com/public/images/43394dd5-0859-4fda-995d-ebce78b6608d_2048x770.png)

这些软件版本的批评也不是纸上谈兵。我们 B300 集群跑的 Linux 内核 `5.15.0-185-generic`，早于一个名为「[writeback: Avoid lockups when switching inodes](https://github.com/torvalds/linux/commit/9426414f0d42f824892ecd4dccfebf8987084a41)」的补丁系列。我们内核遇到的特定问题，由修复了上游内核的 commit `[e1b849c](https://github.com/torvalds/linux/commit/e1b849cfa6b61f1c866a908c9e8dd9b5aaab820b)` 的描述讲得很清楚：
```
There can be multiple inode switch works that are trying to switch inodes to / from the same wb. This can happen in particular if some cgroup exits which owns many (thousands) of inodes and we need to switch them all. In this case several inode_switch_wbs_work_fn() instances will be just spinning on the same wb->list_lock while only one of them makes forward progress. This wastes CPU cycles and quickly leads to softlockup reports and unusable system.

```

什么时候会有一个拥有数千个 `inode` 的 `cgroup` 退出？一个答案：Slurm 作业被拆除时。我们的情形是，随着一个普通工作负载收尾，NUMA 节点上的每个 CPU 都卡在争抢同一个 `list_lock`，处理器变得不可用。恰好位于冻结 NUMA 节点上的本地 NFS 客户端拿不到 CPU 时间，其存活探针超时并上报节点不健康。Kubelet 试图用 `SIGTERM` 与 `StopContainer` 控制损失，但内核慢条斯理地洗衣服——重新分配脏 `inode`——过了两个多小时才满足终止请求。最终结果又是一封来自 Crusoe 的 `NotReady` 邮件——而这一封的独特之处在于，它源于一个老旧的 CPU 内核。

![](https://substack-post-media.s3.amazonaws.com/public/images/02cee8f4-3296-49c3-978f-5731e80353c2_600x1166.png)

到我们测试结束时，这个内核不只是又老又慢：它被 [CVE-2026-64378](https://ubuntu.com/security/CVE-2026-64378)（利用有缺陷的 writeback 行为，7 月 25 日发布，严重性 7.8）正式标记为安全漏洞；[针对该内核的另一条 7.8](https://ubuntu.com/security/CVE-2026-64531) 也于 7 月 27 日贴出。于是，Linux 内核加入了我们收藏的 Crusoe 暴露于 CVE 的软件清单。Crusoe 已告知我们将升级到 6 大版本内核——一个必要的补丁。

![](https://substack-post-media.s3.amazonaws.com/public/images/c39e3841-11dc-4862-a7a8-6352c494c1d0_2048x1470.png)
*来源：Crusoe 2026 年 8 月 13 日的一则招聘启事*

我们在 Crusoe 的 Kubernetes 层做 XID 注入时，错误被迅速检测到并触发了 `Node Replacement` 工作流，但由于一个漏过 Crusoe CI 的 Slurm 命名惯例不一致，节点无法进入 `drain`。健康监控系统空转，反复抓到错误、反复尝试标记节点不健康却失败。Crusoe 工程团队诊断速度惊人，数小时内就上线了替换。然而，替换节点存储 NIC 有故障，立刻进入 `drain`。手动重置节点 VM 后问题依旧。Crusoe 工程团队告知我们，后一事件中 AutoClusters 未能修复是「已知缺口」，他们将在「几周内上线自动修复动作」。对一次基础的可靠性失败而言，这响应迟缓得令人意外。

![](https://substack-post-media.s3.amazonaws.com/public/images/858e75c1-c96e-4877-8263-21d9a60bda07_2030x810.png)

最后简短一提：该集群的 WAN 是我们测过最慢之列，依场景在 0.47 Gbps 到 0.78 Gbps 之间。冰岛出海的光缆确实细。

所有这些问题加起来，就是一台以不稳定著称的集群——前沿实验室的朋友们对此盖章确认，他们既抱怨故障数量，也抱怨 Crusoe 工程师对及时修复明显缺乏兴趣。要说清楚：我们一度把 Crusoe 视为全球第二的 neocloud、因而全球第二的租 GPU 去处，并据此给过推荐。唉，巨人陨落啊。

不过，虽然 Crusoe 的机器镜像早就该刷新、其工程师的 Claude Tags 或 Codex 审批也下不来，他们内部 Slack 里倒是装了这样的自动化：

![](https://substack-post-media.s3.amazonaws.com/public/images/fd0ebfbf-f058-4e7f-b3c8-3b99064127c2_2031x141.png)

2025 年 11 月的 CVE 算不算「历史包袱」？

说正经的，这是优先级问题，是官僚失控问题。我们不知道该怎么看待上面那样的资深 Linux 内核工程师招聘启事。说真的，我们只是请大家把东西保持更新。不需要雇 Linus 也能明白这为什么有道理。所以，看到 Crusoe 秀肌肉、花重金请好人固然酷，但把 Crusoe 带到今天这步田地的，从来不是缺人、缺钱或缺技术。我们的抱怨集中在最基本的问题上，而不是那些无疑占用更多工程时间、我们用起来也开心的 [Slinky 配置](https://www.crusoe.ai/resources/blog/slurm-on-crusoe-managed-kubernetes-how-we-built-managed-gpu-training-infrastructure)、[控制台](https://www.crusoe.ai/cloud)或 [CLI](https://docs.crusoecloud.com/installing-the-cli/)。

我们乐于与 Crusoe 的工程团队合作，相信他们有充足的人才改善排名。坦白说，最近几个月事情似乎正在回到正轨：工程师们状态在线、推代码、为即将到来的发布兴奋。Atero 收购物超所值，把 Crusoe 火箭般送上许多买家在推理端点质量上的首选清单。我们乐见其成。

然而，在托管集群这门生意里，[TCO 归结为有效吞吐，有效吞吐归结为可靠性](https://newsletter.semianalysis.com/p/how-much-do-gpu-clusters-really-cost)，而 Crusoe 的集群异常不可靠。

本轮 Crusoe 位居青铜级底部。

### Prime Intellect

Prime Intellect 今年 7 月[完成 $130M A 轮](https://www.primeintellect.ai/blog/series-a)，[估值 $1B](https://techcrunch.com/2026/07/08/prime-intellect-raises-130m-series-a-to-help-enterprises-build-their-own-ai-agents/)，披露「横跨算力、RL 与后训练、沙箱、推理、环境与评测的年化收入 run rate 达 $100M」。

我们测了 Slurm 与 Kubernetes B300 集群，两层编排总体都算享受，尽管各自都缺一些我们希望有的包。庞大的 Slurm 控制面又快又灵，机器莫名其妙配了 2TB 内存。跑 **salloc** 的 swap 空间管够。

快速统一了 NCCL bootstrap 接口之后，我们的网络测试在 ConnectX-8 NIC 上跑到 13 个节点、吞吐出色。存储无虞，Weka **/data** 卷在 4 节点表现优异并持续稳定扩展。PrimeIntellect 的托管 Grafana 是我们遇到的较好之一。不过我们上的是一个还在烤机中的集群，于是看到了源源不断的错误——测试监控与健康检查的简易办法！

![](https://substack-post-media.s3.amazonaws.com/public/images/474ff935-9589-410b-a578-22f98d257375_2048x1154.png)

先是 Kubernetes 集群一个节点被标 **NotReady**，显然是驻场技术员在折腾相邻服务器，5 分钟内回归。随后，一次 PyTorch 网络测试中，另一个 Kubernetes 节点停止上报 kubelet 状态，分布式作业无法完成；节点重启后回来，作业完成。第二天，2 个 Slurm 节点宕机，一个 NVLink 问题，另一个重启后卡住。两者经介入后迅速回归，但后者很快又犯老毛病，一次突然重启导致一个存储测试失败。一次 MPI 测试在最后阶段中止，相应的 Slurm 作业停留在 **COMPLETING**——所有 worker 短暂失联——那正发生在我们把集群交还之前的当口。

这些可靠性问题都可以归因于：我们是在一个小窗口里上的集群，而他们还在为付费客户烤机。行吧。但 Prime 手头没有可留作热备的富余算力，这指向更大的问题：产能约束日益收紧。Prime 是别人算力的转售商，依赖底层厂商为客户保证高质量体验。这带来的挑战，是高质量训练/RL 框架、面板与一支神级工程师团队的疯狂 Slack 在线也未必总能盖住的。

话虽如此，Prime 的健康检查全程表现惊艳，快速介入并限制了每次错误的损害。我们认为系统默认响应合理，甚至喜欢其 Slack 告警——团队对告警的跟进也很及时。鉴于 Prime 的产能来自多家厂商，其软件层的质量对实验室放心使用至关重要。在我们测过的 marketplace 里，Prime 似乎是最好的。

![](https://substack-post-media.s3.amazonaws.com/public/images/4736b265-c5f7-4f4a-b287-4dfddef97232_2048x842.png)

这留给 Prime Intellect 一份直白的作业——也是我们无法直接洞察的：提升可靠性、建立基础负载产能，以真正 neocloud 的身份在榜单上攀升。我们对团队的技术能力毫无疑问；他们在这个集群上把很多难事做对了，而且是这个榜单上唯一把真实模型训练经验注入其软件与支持方法的厂商。不管好坏，他们在别处的工作远比这里评估的主业托管算力更令人印象深刻。

这期间我们预览了其托管训练产品，印象极深。RL 基础设施明显比简单的托管 Slurm 或 Kubernetes 集群更复杂——它建立在同样的地基之上，但多了三个必须保持同步的组件：

1. 训练
2. 推理
3. 沙箱/环境

不久之后，我们将通过一个暂定名为 PostTrainingX 的项目评估托管训练基础设施厂商与 RLaaS 公司。如果要先放出一版排名，Prime 有望竞争白金！敬请期待。

### DigitalOcean

这是我们第一次完整体验 DigitalOcean 开发者流程的一轮测试。DigitalOcean [自我营销](https://www.sec.gov/Archives/edgar/data/1582961/000158296126000045/a2026-q1dopressrelease.htm)为「第一个为推理与智能体时代端到端打造的云」，把自己与「聚焦裸金属的 neo-cloud 与缺乏云平台的推理套壳」区分开。说白了：DigitalOcean 卖的东西里包括托管集群。

DigitalOcean 的托管集群由 Kubernetes 编排，扎实但略欠成熟。其 onboarding 文档让我们自己装 Multus、再建网络附着、装 MPI Operator、创建 MPIJob manifest。没有理由不预先替客户配好。配好之后，集群表现良好，计算与 XDR 网络全部达标基准，烤机无恙完成。集群开箱也没有 RWX StorageClass，又添一步基础设置——更好的 K8s 厂商会替你办好。存储配好后其性能很有意思：多个客户端数下顺序写约比顺序读快 6 倍，与多数集群相反。我们预计 DigitalOcean 的顺序读性能经重新调优可显著改善。

测健康检查时，我们的第一次 XID 注入无人察觉：监控系统什么都没检测到，节点保持可调度。我们提醒 DigitalOcean 团队后，他们迅速响应、找到系统里的 bug，并让我们当周晚些时候重测。第二次顺利，注入 50 分钟后我们拿到了新节点。

一家 neocloud 若是「为推理端到端打造」，那意味着它不提供 Slurm。DigitalOcean 团队贴心地给了我们一套搭 Slinky 的 runbook，基本功做对了，但要算 production-ready 还需要大量工作。没有 SSH 访问，也没有如前所述的默认 RWX 卷，意味着没地方放 `/shared`。任何打算在 DigitalOcean 上跑 Slurm 的人，都应预期自己动手搭编排。

DigitalOcean [将于 2027 年全年新增 60 MW 产能](https://www.sec.gov/Archives/edgar/data/1582961/000158296126000045/a2026-q1dopressrelease.htm)，除托管 K8s 外，还有一系列有趣的 GPU 服务，如 [Droplets](https://www.sec.gov/Archives/edgar/data/1582961/000158296126000045/a2026-q1dopressrelease.htm)与[裸金属 Hopper 与 MI300X](https://www.digitalocean.com/products/bare-metal-gpus)，但它们在 ClusterMAX 测评范围之外。而据我们目前所见，没有 GB 或 VR 的计划。我们期待下次测试时该团队继续改进其托管 Kubernetes 服务。

### Hyperstack

Hyperstack 隶属 NexGen Cloud，是一家总部在英国的 neocloud，[在美国、加拿大与挪威提供 Kubernetes 集群](https://docs.hyperstack.cloud/llms.txt)。它最近[以 $354M 估值融资 $45M](https://www.nexgencloud.com/news/nexgen-cloud-secures-45-million-in-series-a-funding-to-expand-sovereign-ai-infrastructure-in-europe)，计划为「全周期开发」推出许多 AI 新品。在[宣布 $34M 债务额度建设 B200 机队](https://www.nexgencloud.com/news/usd.ai-provides-34m-facility-to-finance-nexgen-clouds-gpu-deployment-in-sweden)的同时，它还披露计划今年晚些时候部署 4,500 张 B300、2027 年再上线 56 MW。

我们测的托管 Kubernetes 集群相较 ClusterMAX 2.0 标志着显著进步，为其持续增长打下坚实基础。计算与网络测试达标，烤机保持良好数字、无硬错误。我们的 Kubernetes 节点重启恢复迅速，挂载与卸载 PersistentVolume 毫无麻烦。N/S 网络良好，存储够用，尽管我们未能在时间线内用上 Hyperstack 通常提供的 Weka 与 VAST。

我们的合成 XID 在一秒内即被检测到，带 `NvidiaFatalXid=True` 标记。测试过程有些别扭，因为 Hyperstack 没有额外产能，我们只能从机队里拆一个节点出来模拟备件。支持团队在注入 12 分钟后通知我们已检测到错误，备件在总计 52 分钟后重新入队。有意思的是，此时「病」节点仍未被 cordon——那要等到 1 小时 30 分才在 Kubernetes 层登记。这一切都由 Hyperstack 的 SRE 团队在我们合成错误触发 Grafana 告警后人工驱动。

![](https://substack-post-media.s3.amazonaws.com/public/images/a7211d5c-b5ef-44b1-a9f5-e99495125b2a_961x486.png)

总体而言，这次测试是成功的，我们感谢 Hyperstack 让它顺利推进的投入。不过正如团队自己所知，所需的人工支持量让我们担心其可复制性。Hyperstack 提供 24/7 支持，目标单节点故障 60 分钟内介入，但最好不必指望另一支工程队按对按钮，你的集群才能恢复满血。

测试期间唯一的直接错误是两个 pod——`cilium-envoy` 与 `csi-hyperstack-node`——因 `Too many open files` 崩溃循环。小烦扰，不影响我们的工作流。

我们期待随着 Hyperstack 壮大团队、积累更大集群的管理经验、持续自动化与加固基础设施，继续与他们合作。

## 参与奖级（Participation Ribbon）

### Vultr

Vultr 自称「[全球最大的私有云基础设施公司](https://www.businesswire.com/news/home/20260708517182/en/Vultr-and-SUSE-Launch-Validated-Full-Stack-NVIDIA-Enterprise-AI-Platform-to-Accelerate-Production-Deployments)」——它不是；又称「[全球最大的私有超大规模厂商](https://www.hpe.com/us/en/newsroom/press-release/2026/06/vultr-selects-hpe-and-nvidia-for-next-generation-ai-infrastructure-for-cloud-scale-data-centers.html)」——就算前一条成立，这条也轮不到它。不过它仍是 neocloud 圈一个有分量的玩家，拥有现代化的 GB300 与 MI355X，包括俄亥俄一个宣称 [50 MW 的 AMD 站点](https://www.businesswire.com/news/home/20251202285088/en/Vultr-and-AMD-Expand-Collaboration-to-Drive-Global-AI-Innovation-and-Scale)。在 [ClusterMAX 2.0](https://newsletter.semianalysis.com/p/clustermax-20-the-industry-standard) 中，Vultr 的集群带着一堆基础错误交付。不幸的是，快一年后模式依旧。

Vultr 为我们测试构建的镜像中有大量带可适用 CVE 的库，包括 CUDA、DCGM、Docker、runc 与 ConnectX 固件。我们的 Slinky 登录 pod 没挂 `/shared`、缺 Pyxis plugstack 配置，我们只能从一个 worker pod 编排，直到 Vultr 支持团队在测试中途重新部署登录 pod，把两个问题都修了。K8s 层可见的存储还有一个基础问题：默认存储配置与我们的裸金属集群不兼容。默认 StorageClass `vultr-block-storage` 毫无怨言地完成 provision 与绑定，然后 pod 永远卡在 `ContainerCreating`。不过挂在 worker 节点上的 Lustre 层非常出色，32 客户端聚合读达 91.7 GB/s。Grafana 配了但只对了一部分，NVLink 读数为 0，因为 `DCGM_FI_PROF_NVLINK_*` 字段没配。

众所周知，Vultr 的横向扩展网络一直有可靠性问题，已让合作伙伴不敢开工或扩大现有合作。我们建议 Vultr 继续提升集群的结实程度，并打造所有相关工具与编排合理配置且保持最新的黄金镜像。

### Vessl

Vessl 是一家韩国新锐 neocloud，自视为「多云编排器」而非掮客：长期买入裸金属，在上面提供带 SLA 的管理层。他们[宣称在运 5,000 张 GPU](https://vessl.ai/ko/blog/vessl-b200-ai-factory)，目标是 2027 年底达到 100 MW。[一则 Vessl 旧的商务拓展招聘启事](https://kgsa.net/?page_id=29&mod=document&uid=8667)写着要「速度。我们必须快跑、快学、不断迭代」，并要求「[每周至少 60 小时](https://www.linkedin.com/posts/the-concept-of-80000-hours-career-consulting-share-7471245601628696577-HlPU/)」。

我们爱这份雄心；不过我们抽样的 Kubernetes 与 Slinky 口味 Vessl 集群之稚嫩，也给了他们大量功课。我们的 onboarding 以一条「要钉住三个设置才能让 RDMA fabric 可用」的通知开始。有提示总比没有强，但我们更希望拿到一个开箱即性能良好的集群。

![](https://substack-post-media.s3.amazonaws.com/public/images/6f043a94-7c2c-4c37-9d56-b627138a60b8_1744x238.png)

第三条针对一个特别累赘的配置：默认情况下，由于 Vessl 的 Kubernetes `LimitRange`，每个容器使用超过 2GB 主机内存就硬失败。防御性默认在某些场景或许合理，但这是个糟糕设置。节点很少被要求同时跑多个作业，容器理应可支配全部主机 DRAM——几百 GB——因为超过 2GB 就 OOM 掉它们实在窒息。我们建议 Vessl 放宽该限制，使之与主机物理容量对齐，并让失败更优雅。

管理方面，Slinky 层上 Vessl 没有提供任何用户管理方式，只能靠机器上的传统 Linux 工具。我们从控制台加的 SSH 密钥没出现在集群上，经 Vessl CLI 加的也没有；后来才知道这些工具与 Vessl 的 Blackwell 集群互不相干。因此我们只能用 Slack 上私信给我们的私钥与 `kubeconfig`。

![](https://substack-post-media.s3.amazonaws.com/public/images/4e712d05-e3d0-4d5f-9c27-5a9b89b4b156_2048x298.png)

集群提供了一个合理（尽管奇怪）的 `add-user` 便利脚本来建新 Linux 用户。

![](https://substack-post-media.s3.amazonaws.com/public/images/c421b89f-eb94-43ca-a479-45e4885de096_1308x822.png)

然而它没提供 `pip`、`git` 甚至 `sudo` 这类基本包。

![](https://substack-post-media.s3.amazonaws.com/public/images/02307a5c-746c-40ed-ac40-d402528367c2_1292x72.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/42e8d396-2de6-4d06-b1e0-df2d635a9340_946x69.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/4dcc0786-1a69-42d6-93fd-73ba6e53865b_783x70.png)

于是这个集群需要一番功夫才到起跑线。但我们实习生的 Linux 系统管理员修行还没结束。Vessl 的 Slurm 登录节点跑在一个临时 OverlayFS 根上，运行时对 `/etc/passwd` 与 `/usr/bin` 的改动只存在于容器可写层，Kubernetes 回收 pod 后便不保。这导致我们的用户在测试中途消失。

另一处 Slinky 错误配置让 Slurm 层在部分测试期间瘫痪。我们的工作负载写进一个没有清理的 overlay，在根卷累积了 863 GiB，导致 Kubernetes 标记节点 `DiskPressure` 并重启。这不仅带倒了本地 worker，也带倒了 Slurm 控制器守护进程，使整个 Slurm 层间歇不可访问。我们推断 `slurmctld` 被调度到了也跑着 `slurmd` 的节点上。把 `slurmd-pyxis` pod 与 `slurmctld` 混部通常是坏实践，这段轶事就是绝佳例证：数据平面不该被控制平面的行政事务拖累，控制平面也不该落在数据平面的爆炸半径里。Vessl 让 Enroot 改写到更大的卷迅速止血，但据我们所知，根因——worker 与控制器混部——仍未解决。显然，Vessl 没有大规模生产运行 Slinky 的经验。

![](https://substack-post-media.s3.amazonaws.com/public/images/265cf619-792d-401e-a5d4-a2de20f10a35_2048x798.png)

另一个错误让 Kubernetes 访问时好时坏。我们 `kubeconfig` 中 `server` 字段的 URL 并不总是解析到同一 IP：Vessl 错误地把私有 `10.x` IP 与公网 IP 一起发布到了记录集。有时我们的 `kubectl` 解析到正确的（公网）IP、可以访问；有时解析到错误的、请求挂起直到重试成功。我们建议 Vessl 把 `10.x` IP 从公共记录集移除。

我们在 Vessl 集群 Kubernetes 层设置的 `NetworkPolicy` 被接受但不执行——所有租户 pod 之间的 HTTP 请求无视定义的规则一概放行。Vessl 没有配置健康检查程序，应把这件事与上述所有平凡的「生活质量」特性列为优先。

![](https://substack-post-media.s3.amazonaws.com/public/images/f24cf8a2-afbd-43a3-9537-ffa22f1dea42_1425x78.png)

Vessl 提供的硬件本身在测试全程表现良好，包括 InfiniBand 上的 NCCL 测试。鉴于其宣传中即将上线如此庞大的机队，Vessl 有充分动力加固其产品——为用户提供更好的服务，也让自己配得上更好的价格。下次测试时我们有兴趣观察 Vessl 的进展。

### Runpod

Runpod 是总部在新泽西 Moorestown 的 neocloud，机队包括 RTX PRO 6000、H100、H200、B200 与 B300。今年 6 月，他们[以 $1B 估值融资 $100M](https://www.prnewswire.com/news-releases/runpod-raises-100m-led-by-summit-partners-to-accelerate-the-ai-developer-cloud-302808689.html)，并在 Twitter 宣布[收入从 2 月到 6 月翻倍至 $240M ARR](https://x.com/LukePiette/status/2069822990615728333)。

我们能测的集群在西雅图，新到连存储都还没配。我们的「Instant Cluster」确实 instant，不到 2 分钟就转起来了。

![](https://substack-post-media.s3.amazonaws.com/public/images/b3b62b74-729a-4b4e-92fd-8672fbbfa140_2048x1113.png)

Runpod 的用户模型不寻常。理想世界里，我们通过带 RBAC 的网页控制台管理权限：按邮箱加团队成员、升降权限、建组、丢入 SSH 密钥自动同步到集群。而 Runpod 则是利用其敏捷开通，建议按需铸造 Instant Cluster：工程师以单租户方式操作集群，用完归还池子。预算、监控等策略因此在集群层之上处理，而非通过 Linux 用户管理或 Slurm 记账这类传统工具。Runpod 的设计选择可行，但值得一提：我们最终没有按建议的方式使用集群，而是退回到更熟悉的模式——把 Linux 账号绑到我们的 SSH 密钥上。

我们第一次烤机就失败了：一个节点的两张 NIC 的 port 1 链路掉线，疑似 leaf 交换机问题。没有健康检查抓到错误，但有一个 Grafana 面板——如果你知道去哪看——会高亮这个错。拿到我们的反馈后，Runpod 团队迅速改进面板，让 InfiniBand 状态更容易看到。

![](https://substack-post-media.s3.amazonaws.com/public/images/3c2a0073-ebec-4897-bca3-ad5501b3fe33_2048x1054.png)

第二次烤机尝试中，网络表现良好，测试无错完成。

集群新到没有共享文件系统可测。软件方面，我们的初始审计发现许多待改进之处：CUDA Toolkit、GPU 驱动与 NIC 固件因安全原因已 deprecated，CUDA Toolkit 还是额外负担，因为 [12.8 不支持 SM103](https://docs.nvidia.com/cuda/archive/12.9.0/pdf/CUDA_Toolkit_Release_Notes.pdf)——B300 的 SM 架构。这导致我们一些基准第一次运行就失败。集群还缺大量预期工具：没有容器运行时，许多基础 HPC 包缺席。Slurm 还偶尔把等待中的作业标为 `InvalidAccount`，即便 `AccountingStorageEnforce=none` 且 `AllowAccounts=ALL`，作业也跑不了。绕行办法是不停 spam `scontrol update JobId=<jobid> Account=me` 直到 Slurm 接受。

我们还见到一次镜像解压填满 50 GB 根 overlay——它与 `/var/spool/slurmd` 共享——导致 `slurmd` 无法写、节点被 drain。我们的租户没有 `scontrol update` 凭据，测试只能缺编继续。另外，Linux 拒绝 `unshare -Ur`，我们只能改用 `udocker`。我们标准的 XID 注入路径被挡，因为没有写 `/dev/kmsg` 的权限；我们没有发起节点重启的机制；默认未启用无密码 `sudo`。这里的主题很清楚：在 Runpod 环境里，用户缺少完成工作所需的许多权限。

我们发现 Runpod 团队异常乐于接受反馈、急于解释决策。我们喜欢[其大多数招聘岗位都是正经工程岗](https://www.runpod.io/careers)，希望他们继续在易访问性与开发者控制之间取得更好的平衡。

### Bitdeer

Bitdeer 自 ClusterMAX 2.1 起新入测评。又一家转型 AI 的矿企，[据其最新公告](https://ir.bitdeer.com/news-releases/news-release-details/bitdeer-reports-unaudited-financial-results-second-quarter-2026)已坐拥 1.75GW 总电力容量，令人印象深刻。不过这大多喂给了加密货币矿机：[我们的 SemiAnalysis 数据中心行业模型估计其在线 AI 电力只有几 MW](https://atlas.semianalysis.com/?dashboard=datacenter_model)。尽管如此，Bitdeer 正猛打方向盘转向利润率更高的 GPU 生意，未来几年 pipeline 里已有数百 MW——Knoxville、Wenatchee、Fox Creek、Rockdale 及挪威与马来西亚的站点（或改造中或新建中）。既想纵向也想横向增长，Bitdeer 不满足于单纯的 colo 生意，从 token 即服务到托管智能体、当然还有托管集群，新芽产品一应俱全。

![](https://substack-post-media.s3.amazonaws.com/public/images/1f265b3a-94a5-4931-b066-fdcccf9de49a_1496x902.png)
*来源：bitdeer.ai*

Bitdeer 给了我们其公开控制台的额度后，我们花了大量时间琢磨他们到底指望我们测什么。健康检查没搭，监控面板不好使，PyTorch、Docker 等许多基础库没装，网络设置为空，IMEX 未配置，控制台不支持 RBAC 之类普通便利。Bitdeer 的监控安装器下载了一个错误 CPU 架构的二进制。SSH 最终能用，但奇怪地要求 RSA 密钥而非 ed25519。Kubernetes 查询反复断连。简言之，这个集群的管理严格名义化。能说的最多是：它有 GPU 驱动、NCCL、CUDA、一个 OS 与内核，而且都足够新。

等我们有时间把东西配起来，性能尚可。烤机中 GPU 达到预期数字，NVLink 承载了预期流量。

![](https://substack-post-media.s3.amazonaws.com/public/images/7f84fb39-e5a1-4e8e-b260-1f8d47fe13d6_1280x857.png)

然而该集群的 WAN 性能差到出奇，多次测试平均约 0.1 GB/s。性能差的原因我们不得而知；毋庸说，这会妨碍真实世界使用。

最要命的是，获得支持极其痛苦。整个技术团队都在亚洲（我们的情形是马来西亚/新加坡），意味着排障时 8-12 小时的响应周期。把它放进本档之外的任何档位都不可能。

我们期待未来几轮测试中看到 Bitdeer 随托管云产品成熟、落地健康检查与托管 Kubernetes 等特性而进步。Bitdeer 把时间与注意力投向哪里将很有意思，因为管理层已毫不含糊地宣布其 neocloud 业务不是主要焦点：「[执行托管租赁（colocation lease）协议才是头等大事。](https://www.sec.gov/Archives/edgar/data/1899123/000121390026054748/ea028888001ex99-1.htm)」

### Shadeform

Shadeform 继续以小团队专注掮客与单个 GPU VM 的小规模市场转售。我们喜欢其界面、也喜欢与 Shadeform 团队合作，但若没有更大雄心，他们将留在我们的最低档。

### Radiant

Radiant 由 Brookfield 收购英国 neocloud Ori 而成——我们在 ClusterMAX 2.1 讨论过 Ori。不幸的是，我们一直没能测到一个能工作、安全达标的集群。尽管规划了近一年、营销不遗余力、公告里亿与吉瓦齐飞，Radiant 至今尚未部署一块 Blackwell GPU。

### FPT

FPT 在我们的测试中出现过若干安全问题，已在 ClusterMAX 2.1 中描述。我们尚未复测，也不知晓其有任何 Blackwell 产能。

### Core42

Core42 是这一档的黑马。他们有扎实的团队、GPU 配额、政治靠山，以及 Mubadala 这台无限提款机。我们期待看到他们拼好拼图、随进军美国市场而在榜单上火箭蹿升。

### Latitude

Latitude 正取得进展维持其规模不大的云业务，最近被 Megaport 收购并借此上市。我们有机会测了几台 RTX Pro 6000 Blackwell 服务器，但只要 Latitude 还缺最新最强的 GPU，我们预计他们只能困在这一档。

### IBM Cloud

自 ClusterMAX 2.0 那场灾难体验以来，我们还没有机会重试 IBM Cloud。

### BuzzHPC

Buzz 正在加拿大掀起波澜，搭上 Carney 对决 Trump 关联的主权 AI 浪潮，与 Bell 等伙伴在萨斯喀彻温落地 1.2GW 与 $50B，外加该国其他地方的 300MW+，可谓阵容豪华。BuzzHPC 经母公司 HIVE Digital Technologies Ltd. 成为 ClusterMAX 榜上众多上市公司之一。不幸的是，我们从 Buzz 测过的所有 GPU 都处在质量存疑的集群里，依赖同样存疑的软件供应商伙伴选择。自 ClusterMAX 2.0 以来我们未能复测，但希望近期有所改变。

### Neysa

印度 neocloud Neysa 今年 2 月[宣布 $1.2B 融资](https://neysa.ai/press-release/blackstone-leads-funding-of-over-1-billion-dollar-to-neysa/)，含 $600M 股权与 $600M 债务，由 Blackstone 领投，投后 $1.4B。他们宣称「[9,216 张风冷 NVIDIA B300 于 2026 年 12 月至 2027 年 3 月间分阶段到位](https://neysa.ai/blog/hpc-architecture/)」，pipeline 里还有等量的 AMD MI350X。增长惊人，显然是印度这方面领导者。

不幸的是，本轮测试揭示了一个错误百出的集群。集群开通时预装的许多软件包过期数月甚至数年，若干严重 CVE 可适用。例如 CUDA Toolkit 12.0[发布于 2022 年 12 月](https://developer.nvidia.com/cuda-toolkit-archive)，比 Neysa 公司本身还老，居然被装在我们集群的 **/usr/bin/nvcc**。

我们乐于与 Neysa 团队合作，鼓励其在产能暴增、海外大客户到来之际继续改善安全姿态、夯实基本功。尽管 Neysa 现有客户大多困在 Hopper 世代（有几张 B300 可用），印度次大陆尚无 GB（因而也没有直接液冷）进入生产。

### Vast.ai

一家在客户对话中不断被提起、按需随机 GPU 的转售商/marketplace，拥有业内较好的伙伴拓展团队之一，在世界各地寻找闲置产能。不幸的是，UI 实在糟糕，太难用。

### Hyperbolic

上一轮以来我们没机会复测 Hyperbolic，但他们总算把基础安全合规认证搞完了！Hyperbolic 进入榜单。

### STN

STN 一直很让人困惑。他们是最早部署 B300 的云之一，也是极少数提供「私有云」选项的厂商——客户自行采购集群、把芯片留在自己资产负债表上，STN 负责集群运营。多家客户告诉我们他们喜欢这种安排，胜过那些漫天要价的 neocloud。

我们一直乐于与 STN 团队合作，但不幸的是，最近三次接洽，我们都遇到了某种性能、可靠性或配置问题，要求修复，得到修复承诺，没等到修复，然后时间耗尽。

遗憾的是，在能看到一次客户视角的完整端到端测试体验之前，我们只能把 STN 留在这一档。

## 不推荐——表现不佳

基于实测，这些厂商只要修复一个或多个关键问题即可迅速升至青铜级，例如：只提供老 GPU、缺基础安全认证（SOC 2、ISO 27001）、关键服务器特性配置错误（留着 PCIe ACS 不关，或未启用 GPUDirect RDMA）、或在集群创建与硬件宕机期间照收 GPU 小时费。

### SharonAI

Sharon AI 是澳大利亚 neocloud，[宣称 pipeline 有 132MW、其中 116MW 已签出](https://sharonai.com/press-releases/sharon-ai-announces-us1-32-billion-five-year-cloud-computing-service-agreement/)，而我们估计其当前规模约 4 MW。他们没有 SOC 2 或 ISO 27001。我们测了 2 台裸金属 H200 节点验证基本功能。期待其产品成熟后继续测试 Sharon AI。

### IREN

IREN 继续在我们的 neocloud 客户对话中出现，而且通常不是好话。他们在加拿大 BC 北部 Prince George 与 Mackenzie 的 HGX B200 和 B300 价格低到尘埃，而那些故事我们也听过了：多日停电、网络升级、存储故障、空气质量管控导致链路抖动、满屏 XID。用户口中业内最差站点第一名。而我们也是其用户——我们从多家转售其产能的厂商那里测过 IREN GPU。我们听到的很多过得不开心的用户，租的不是 IREN 转售商，而是 IREN 本尊。

话虽如此，Childress 与 Sweetwater 的新项目看起来好得多（读作：电力、制冷与 ISP 不再是 N+0！）。我们在数据中心模型中对这些站点有大量覆盖，只需说：尽管其云服务技术短板一堆，我们预计 [NVIDIA 的 $2.1B 投资](https://nvidianews.nvidia.com/news/nvidia-and-iren-announce-strategic-partnership-to-accelerate-deployment-of-up-to-5-gigawatts-of-ai-infrastructure)会帮他们这次少偷点工减料。

我们建议 IREN 别再在公开营销与投资者材料里假装提供托管集群和推理端点，专注其裸金属产品——市场上对其服务的需求大把。

### Hydra Host

Hydra Host 于 2026 年 6 月[融资 $100M A 轮](https://hydrahost.com/post/tokens-are-the-new-oil-hydra-host-series-a/)，NVIDIA 是投资方之一。他们专注撮合交易，托管集群经验我们只有早前测试可依。考虑升级之前，我们需要测一个真正的托管集群。

### FarmGPU

我们对 FarmGPU 的测试进展有限。Slurm 层未正确广播 GPU 资源，Kubernetes 层也没有为横向扩展网络暴露任何 RDMA 设备。

尽管如此，我们非常欣赏 FarmGPU 的开放开发文化，包括扎实的 Grafana 监控体验与详细的部署笔记。其技术团队值得信赖、合作扎实，尽管光是正确部署几个小集群就已让他们绷到极限。

### WhiteFiber

WhiteFiber 于 2025 年 8 月[首次 IPO 交割时募得毛额 $159.4M](https://www.whitefiber.com/news?id=19)。我们先前的测试发现网络性能良好，但 Slurm/Kubernetes 集成不可用、作业监控薄弱。较新的客户反馈显示有改善，不过临时的 Slurm 登录文件系统仍是隐患。我们需要验证这些运维问题确已修复。

### PaleBlueDot

PaleBlueDot 于 2026 年 1 月完成 B Capital 领投的 [$150M B 轮](https://www.prnewswire.com/news-releases/palebluedot-ai-raises-150m-series-b-to-scale-global-ai-compute-infrastructure-302672782.html)。我们此前发现其 marketplace 对单个 VM 而言好用，但缺乏完整的托管集群体验。不幸的是，他们已关闭按需控制台，转向在专属数据中心服务几家大客户。

### Akamai

Akamai/Linode 过去一年变化不大，聚焦单节点 GPU，无托管 Slurm 或 Kubernetes。我们会继续观察这头沉睡的巨人何时醒来。

### Hetzner

Hetzner 的低成本托管模式仍提供一些便宜的 PCIe GPU，具体是 RTX 4000 与 6000 Pro Blackwell Edition。我们等着看他们是否迈出更大一步，凭其全部数据中心运营经验真正服务 AI 市场。

### Mithril

Mithril（前 Foundry）2024 年就[宣布 $80M 融资](https://mithril.ai/blog/introducing-foundry)，志在「为 AI 恢复公有云的承诺」。如今它是一个包裹 3 个 Nebius 可用区的 marketplace，提供 H100 或 H200，不过只有 H200 有带横向扩展网络的选项。

![](https://substack-post-media.s3.amazonaws.com/public/images/15b5188b-419c-4668-beb5-cec14d49a018_911x313.png)
*来源：Mithril 官网*

曾有一些让我们相当兴奋的 TPU 支持公告，但那项合作似乎已被悄悄抹掉。

### OVHCloud

OVHcloud 在全球拥有可观基础设施，运营着大量数据中心，其中一些与本榜单头部 neocloud 共用。但我们的疑虑未变：在各家为了拿到最新最强算力而疯狂奔走的 AI 时代，通用 IaaS 不是增长引擎。又一头沉睡的巨人。

### Massed Compute

Massed Compute 上一次宣布的融资，是 2025 年 8 月来自 Digital Alpha 的[最高 $300M 股权加收入分成融资](https://www.hpcwire.com/off-the-wire/massed-compute-gains-300m-backing-for-nvidia-powered-ai-cloud-expansion/)。他们以此推动了一家裸金属公司的合理增长，但仅此在 ClusterMAX 评级体系里不够看，尤其他们的[垃圾炮聊天机器人](https://massedcompute.com/faq-answers/?question=What%20are%20the%20key%20features%20of%20NVIDIA%20H100%20GPUs%20that%20enable%20improved%20performance%20in%20machine%20learning%20workloads%3F#:~:text=These%20answers%20are%20generated%20by%20an%20AI%20system%20and%20may%20be%20incomplete%20or%20inaccurate.)还在被网络爬虫索引。

## 不推荐——无法测试

我们的「不推荐——无法测试」档一如既往，但为澄清起见，本节包括四类公司：

1. 我们曾测过、现在声称零闲置产能和/或拒绝参与测试的厂商，包括 Fluidstack、Cirrascale、Lightning AI（最近与 Voltage Park 合并）、Scaleway、CUDO Compute、Denvr Dataworks 与 Atlas Cloud。
2. 尚未上线、尚未测试、总体让我们感兴趣的厂商——尽管我们相信其中一些未具名者在公开营销材料里宣称自己做托管集群、实际只做裸金属，从而误导投资者（即撒谎）。这包括 SpaceXAI、Mistral、Poolside Infrastructure Company、Nscale、Highrise、Corvex、Andromeda、Volta、Firebird、Tatra、Sesterce、Yotta、Boostrun、GlobalAI、Argentum 与 Qumulus。
3. 体量大且重要、但因地理或监管原因无法妥善测试的厂商，包括 Alibaba Cloud、MegaSpeed、BytePlus、RunSun、SK Telecom、Naver Cloud 与 Indosat/Zankore/Lintasarta。
4. 太小而无足轻重者。它们仍在我们市场观察范围内，但不参与评级。

### Fluidstack

就我们所知，Fluidstack（目前）已退出托管集群市场，因为其重心已从托管 Nvidia 集群转向 10 万+ 芯片规模的裸金属 TPU 部署。我们期待未来无论他们届时提供什么芯片，都能再次合作测试。

### Cirrascale

不幸的是，在收到一封要求修改我们上一篇文章中与 Cirrascale 合作经历描述的律师函后，我们一直未能建立富有成效的合作关系。

### Lightning（与 Voltage Park 合并）

Lightning 与 Voltage Park 合并后，合并公司不幸用光了 GPU，我们没能测到整合后的产品。尽管该公司持续宣传自己是全球部署 GPU 数第三大的 neocloud。他们进不了前十。

### Scaleway

最近我们听说，Scaleway 降低了多个客户合作的优先级，并似乎毫无充分理由地主动与 NVIDIA 分手、转向 AMD。我们认为这很可惜。

### CUDO

本周期 CUDO 未提供有代表性的托管 Slurm 或 Kubernetes 环境，因其聚焦其他业务优先级（即管理一堆裸金属数据中心的建设）。环境可用时我们期待重新评估 CUDO。

### Denvr Dataworks

尽管领导层更迭、社区里偶有活跃，我们在测试 Denvr 上毫无进展，也未看到业务有任何有意义的增长，能把他们从创始人挖的坑里捞出来。

### Atlas Cloud

最近我们一直拿不到 Atlas 的 GPU，尽管其加密货币母公司大肆公告裸金属数据中心，其托管推理产品也时不时出现在端点厂商名单上。

### SpaceXAI

我们爱 Colossus，迫不及待想测 SpaceXAI 的 neocloud 产品！

### Mistral

Mistral 刚完成 [€3B D 轮](https://techcrunch.com/2026/09/08/mistral-raises-e3b-as-sovereign-ai-becomes-big-business/)，而 TeamPCP 的黑客声称要把其整个代码库放到暗网出售，其真伪尚待确认。无论如何，我们非常兴奋能测他们的 neocloud 产品。团队告诉我们平台 8 月仍在起来、在 onboarding 首批客户，所以我们非常期待未来与之测试。在我们看来显而易见：有为自己模型建训练集群经验的公司（见上文），若选择转型，会成为成功的 neocloud。

### Poolside Infrastructure Company

在 Nvidia 以 $6B 的「license-acqui-hire」（许可+收购+招聘）把这个神级团队收编、埋进 Nemotron 官僚体系之后，Poolside 的香火由 Poolside Infrastructure Company 延续——它正在西得州开发其 Project Horizon 园区。我们尚未测过他们的任何东西，但其经验与雄心使其随时可能入局——只要那支精简骨架团队决定在 neocloud 业务上放手一搏。

### Nscale

Nscale 3 月[宣布 $2B C 轮](https://www.nscale.com/press-releases/nscale-series-c)，5 月宣布收购 AnyScale，几天前刚递交 S1 准备在 NYSE 上市。令我们难以置信的是，他们生意做得这么大，却继续在公开营销材料里宣称提供托管集群与推理端点——这显然不是事实。不过显然，他们会继续成功。他们握有大量土地与电力、一些建设与数据中心运营经验，而人们真的很想要价格漂亮的裸金属。

### Highrise

Highrise 是 Hut 8 的 AI Cloud 业务，新闻不断。我们希望很快能测到他们的托管集群。

### Corvex

Corvex 继续对 ClusterMAX 躲着走，尽管 8 月宣布了 $33M 定增以扩建数据中心产能。他们[选择的合并对象是 Movano——Evie 智能戒指的制造商](https://www.corvex.ai/blog/press-release-corvex-to-go-public-in-all-stock-merger-withmovano-creating-a-pure-play-platform-for-secure-ai-infrastructure-and-high-performanceinference)。产品路线图变化不可谓不大。私下里，他们声称在美国政府（USG）有一些安全客户。我们期待测试。

### Andromeda

Andromeda 从其他厂商拿产能、在上面叠一层托管集群服务。我们多次商谈测试，也乐于与其技术团队合作，但其商务面有点见不得光。转售商有一种扭曲的激励：对客户隐瞒底层厂商是谁，生怕客户绕过自己直接签约。不幸的是，这会导致糟糕的传话游戏，最坏时演变成大量互相甩锅。具体而言，我们对非规避（non-circumvention）条款有意见，希望 Andromeda 能建立一种持久的商业模式，让他们可以坦然亮出自己扎实的技术团队及其价值。

具体而言，我们知道 Andromeda 有三种不同选项：

1. 租算力——典型 1:1 neocloud 关系，Andromeda 聚合底层厂商产能并转售，但依赖它们提供支持
2. 管算力——有些客户手里的供应商名单增至 3、4 家，想要「一个可掐的喉咙」，Andromeda 就成为那个喉咙
3. 自带集群——也叫私有云，客户想拥有自己的硬件（并掌控自己的供应链），但仍需要帮手管理一切，实质是 SRE 外包

我们看到名单上第 3 选项的强劲增长。我们也期待尽快测到 Andromeda 的 Blackwell 产能——不管它身在何处。

### Volta

Volta 带着 [$300M 风投资金与另外 $5B 客户融资池](https://www.bloomberg.com/news/articles/2026-08-04/nvidia-dell-back-ai-cloud-startup-volta-at-2-4-billion-value)登场。其首个大型已宣布合同使用 Bitdeer 的挪威站点。我们尚未测试其云软件或客户运营。

### Firebird

Firebird 正在亚美尼亚建设 GPU 基础设施，Ameriabank 宣布了 $60M 建设融资，并在哈萨克斯坦有扩张计划。最近，他们成为一篇关于 Nvidia 芯片获取与亚美尼亚-阿塞拜疆和平进程报道的主角；[联合创始人 Razmig Hovaghimian 回应称，该项目在这些外交进展之前数年就已扎根](https://zartonkmedia.com/2026/09/06/following-wsj-report-firebird-co-founder-offers-context-armenia-ai-project-has-roots-going-back-years-built-to-make-armenia-a-global-technology-powerhouse/)。GPU 外交。为亚美尼亚人民交付的压力来了！我们仍需看到其托管云实际运转。

### Tatra

Tatra 正在斯洛伐克建设 B300 与 GB300 产能，利用该国的核电与水电基础。我们收到了对其父子团队技术功底的极佳反馈——勤劳，令人敬佩的一家人。不过眼下，我们还需要他们把首批产能完整部署，才能送上考场。

### Sesterce

8 月我们经 Sesterce 开了一台按需 H100。控制台显示的 Ubuntu 选项过时，开通慢条斯理，最终我们拿到了一台能用的机器。然后我们发现底下垫着的是 Shadeform。掮客套掮客。我们挺想知道，在客户跑上工作负载之前，究竟有多少家公司要赚一道差价！话虽如此，Sesterce 正与大承购方推进一些大型裸金属 Blackwell 集群。那些我们想测。

### Groq

Groq 立志挑战 Nvidia，但在一场「license-acqui-hire」带走 Jonathan Ross 与大部分工程团队之后，剩下的公司转型了……转去出租 Nvidia GPU！想再拿 $350M 圆梦，当 neocloud 就对了（[8 月已宣布](https://groq.com/newsroom/groq-becomes-an-nvidia-cloud-partner)）。我们期待有朝一日测到端点以外的产品。Jensen 拿到了芯片团队和一个新客户。不亏。

### Yotta

Yotta 在一场主要参观登录界面的 onboarding 演示后，交给我们一个四节点 H100 Kubernetes 集群。要提工单，我们先被从 Shakti Cloud 引到 One Yotta，再绕回 Shakti 域。不幸的是，这一堆门户无助于让集群保持在线——我们开始测试不到一天就撞上真实故障（XID 94）。这里的测试仍在进行，性能扎实（虽然远超我们的截稿期），但综合客户反馈与自身体验，信号已经相当明确。我们要看到 Blackwell GPU 与更好的可靠性，他们才能跟上业内其他人。

### Darya

Darya 正把 GPU 云基础设施带进塔吉克斯坦——就在阿富汗边境上——这无疑扩大了我们需要测试的地图范围。[其 H200 集群于 2025 年 6 月上线，随后与 Yotta 签约在 Darvoz 开发水电供能的 AI 数据中心](https://yotta.com/press-releases/darya-ai-and-yotta-data-services-sign-strategic-collaboration-agreement-to-develop-tajikistans-first-green-ai-data-center/)。有意思的东西，不过在领教过 Yotta 的门户迷宫之后，我们特别好奇其运营模式中有多少部分能一路搬去塔吉克斯坦。我们尚未获得 Darya 集群的访问权，不过很乐意去现场看看。

![](https://substack-post-media.s3.amazonaws.com/public/images/28a998bd-2550-4185-aa2c-808cf6d383ae_1448x892.png)
*来源：Darya 数据中心的谷歌地图*

### Boostrun

Boostrun 有些扎实的裸金属，但用钞能力跳过了部分 Kubernetes 工程：[vCluster 称该公司在 45 天内上线托管 Kubernetes，未新招一名平台工程师。他们选择了租户隔离的控制面、专属私有节点，以及用 Netris 做网络开通](https://www.vcluster.com/case-studies/boost-run)。明智。我们宁愿看到小厂用成熟软件，也不想看他们花一年重新发明 Kubernetes。在客户讨论中，我们仍会考虑再叠加一家运营商以获得全托管训练体验。我们间接测过一个 Boostrun 集群——经另一家转售其产能的厂商——但仍在等待与其支持团队直接接洽的机会。在把他们搬上榜单之前，我们想看到真实合作中 Boostrun 自己扛下多少 day-two 运维。

### Global AI

Global AI 把主权云的卖点贯彻得相当字面：[专属、单租户、物理隔离（air-gapped）的集群按数据机房出售（据他们所说）。客户决定 Global AI 何时可以访问其系统](https://www.globalai.com/)——对裸金属而言是扎实的产品。然而，当宣传中提供托管集群选项时，我们需要看到更多。哪怕只评裸金属，我们也想看到开通与安全补丁如何处理、监控栈多全面、可靠性与健康检查如何运作，以及驻场团队关工单又快又准的能力到底如何。我们尚未见到这一层细节。

### Argentum

Argentum 官网写着[「200,000+ GPU 现货可用」](https://argentum-ai.com/)。在读到本文这一节之前，你听说过 Argentum 吗？

### QumulusAI

QumulusAI 找到了一种不一样的 GPU 债源：[经 USD.AI 的 $500M 无追索权额度](https://www.qumulusai.com/articles/qumulusai-secures-500m-non-recourse-financing-facility-through-usdai-to-accelerate-ai-infrastructure-growth)，以「GPU 仓单代币」（GPU Warehouse Receipt Tokens）作为稳定币借款的抵押品，可为获批部署提供最高 70% 的融资。「GPU 仓单代币」真的是这个名字。公告描述的是一笔额度，所以我们不把 $500M 算作已装机硬件。在客户交流中，Qumulus 作为产能供应方被提及，托管训练之上可能还需再叠一家运营商。我们仍需检查其自有软件与支持，但初期客户反馈出人意料地扎实。

### Alibaba Cloud

阿里巴巴可展示的软件比寻常 neocloud 初创多得多。一个例子是[其 ACK Slurm operator：一个 SlurmCopilot 组件在 Slurm 与 Kubernetes 之间协调资源分配，避免闲置资源搁浅在某一个调度器里](https://www.alibabacloud.com/help/en/ack/cloud-native-ai-suite/use-cases/implement-slurm-hpc-and-kubernetes-load-hybrid-scheduling-on-ack-cluster)。这正是我们喜欢戳一戳的编排管道，而显然这家公司还没准备好被戳。我们有账号、被列入几个模型端点的白名单、也直接对接过销售团队，但至今未能拿到任何现代 GPU 或这套 ACK 软件的测试权限。

### Megaspeed

他们的马来西亚与印尼站点有大量硬件可查，但我们还没有登录权限。

### BytePlus

BytePlus 的 [GPU 服务宣传多轨道网络上的交换机亲和摆放、对其 vePFS 并行文件系统的直接 RDMA 访问](https://www.byteplus.com/en/product/gpu)，以及与我们最爱模型的集成：Seedance 2.5。我们尚未完成对其集群的评估，但显然有值得关注的东西。滴答，滴答。

### Humain

Humain 给自己派了不少活。在沙特 GPU 建设之外，[Tareq Amin 宣布了约 6 GW 的数据中心雄心，以及 Humain One——一个面向任何计算机的实时语音界面](https://www.reuters.com/world/middle-east/saudi-ai-firm-humain-unveils-6-gigawatt-data-centre-plan-new-ai-operating-system-2025-10-27/)。我们愿意从一次登录和一个能用的集群开始，但至今未收到团队回复，只能好奇他们把什么秘密藏在 Groq 系统旁边。

### SK Telecom

SK Telecom 为韩国主权基座模型计划运营着超过 1,000 张 B200。正如我们[近期文章所覆盖的](https://newsletter.semianalysis.com/p/koreas-trillion-dollar-sovereign)，政府还从 SK Telecom 与 Naver 合计租用了约 3,000 张 H100 等效算力用于竞赛第一轮。SK Telecom 已宣布规模大得多的 2 GW NVIDIA DSX AI 工厂，预计在 SK 集团规划的 5 GW 一期建设内部署搭载 SK hynix HBM4 的 Vera Rubin 系统。我们经 Vessl 测过 SK Telecom 的 GPU，表现扎实，但没有与 SK 直接合作过。要把他们视为认真的玩家，我们需要看到他们在国际市场上有更多动作，但技术底子显然在那儿。

### Naver

Naver 与 SK Telecom 一样高度可信。它已运营超大规模级数据中心，其 7 月与 NVIDIA 和 Brookfield 的计划要求把 GAK Sejong AI 工厂从初始 55 MW 扩展到 2028 年的 200 MW。我们感兴趣的是，这些运营经验有多少能触达外部客户，而非只服务 Naver 内部研究团队。我们尚未测过那种体验。

### Indosat（Zankore）

Zankore 已宣布首期约 200 MW 的 GB300 NVL72 产能将于 2027 年上半年交付。即便其 Blackwell 部署略有延期，他们仍在通往长期 1 GW 雄心的正轨上，主要服务（传闻中的）来自中国大陆的承购方。而且他们[已拿到 $3.1B 贷款](https://www.reuters.com/business/media-telecom/ooredoo-backed-zankore-secures-31-billion-financing-nvidia-ai-cloud-platform-2026-09-09/)去干这件事！

# ClusterMAX 的下一步

