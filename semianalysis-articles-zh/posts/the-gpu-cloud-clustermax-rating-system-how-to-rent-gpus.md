---
title: "GPU 云 ClusterMAX™ 评级系统 | 如何租用 GPU"
title_en: "The GPU Cloud ClusterMAX™ Rating System | How to Rent GPUs"
subtitle: "按租赁 GPU 价值计 90%+ 覆盖率，GPU 云评估指南，GPU 价格更新，GPU 泡沫破裂，CoreWeave IPO，超大规模云厂商，AI 新兴 GPU 云经济学，新兴 GPU 云 IRR"
date: 2025-03-26
source: https://newsletter.semianalysis.com/p/the-gpu-cloud-clustermax-rating-system-how-to-rent-gpus
crawled: 2026-09-15
authors: ["Dylan Patel", "Kimbo Chen", "Daniel Nishball", "Ivan Chiam", "Reyk Knuhtsen"]
tags: ["Hyperscaler", "Neoclouds", "Benchmarks"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# GPU 云 ClusterMAX™ 评级系统 | 如何租用 GPU

> 原文：[The GPU Cloud ClusterMAX™ Rating System | How to Rent GPUs](https://newsletter.semianalysis.com/p/the-gpu-cloud-clustermax-rating-system-how-to-rent-gpus) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**按租赁 GPU 价值计 90%+ 覆盖率，GPU 云评估指南，GPU 价格更新，GPU 泡沫破裂，CoreWeave IPO，超大规模云厂商，AI 新兴 GPU 云经济学，新兴 GPU 云 IRR**

*ClusterMAX™ 评级系统及本文内容由 SemiAnalysis 独立完成。SemiAnalysis 客户向我们支付的任何报酬，过去、现在或将来均与本文所表达的具体分级、评级或评论没有直接或间接的关联。*

## 引言

GPU 租赁市场的狂热已经降温。我们在 [2023 年 12 月的 GPU 云经济学报告](https://semianalysis.com/2023/12/04/gpu-cloud-economics-explained-the/)中预言了这一点，并在 [2024 年 10 月发布的《AI Neocloud 解剖与指南》报告](https://semianalysis.com/2024/10/03/ai-neocloud-playbook-and-anatomy/#part-2-the-ai-neocloud-economy)中重申了这一观点。技术进步意味着算力成本会随时间下降，我们如今认为 GPU 租赁已进入买方市场，尤其是 Hopper 级和 MI300 级 GPU。目前有 100 多家 AI 新兴 GPU 云（Neocloud）和超大规模云厂商可以提供广泛的供应。

部分原因在于新入局者增多，租赁选择更加丰富。而在今天之前，市场上一直没有任何「租 GPU 指南」，也没有对 GPU 云的独立评估。

过去 12 个月里，我们投入时间打造了 GPU 云 ClusterMAX™ 评级系统（GPU Cloud ClusterMAX™ Rating System），简称 ClusterMAX™。我们对尽可能多的 GPU 云进行了独立测试和/或收集了客户反馈。我们相信，凭借这第一个 GPU 云评级，我们将覆盖**按 GPU 数量计 90% 的 GPU 租赁市场**。我们希望在下一轮评级中纳入更多供应商，以便评估它们的品质。

![](https://substack-post-media.s3.amazonaws.com/public/images/aa4160e7-37d5-4e61-bd2c-088c6fd32f35_778x868.png)
*来源：SemiAnalysis*

这并不是 GPU 供应商的完整名单。我们掌握的参与者名单要广泛得多，完整的市场版图见下图。这份名单似乎每天都在扩大，但其中许多新兴 GPU 云（neocloud）尚未准备好迎接客户。这正是 ClusterMAX™ 的意义所在——它是一个帮你化繁为简的简单工具。把预算花在获得 ClusterMAX™ 评级的供应商上，大概是值得的。

![](https://substack-post-media.s3.amazonaws.com/public/images/8d241640-86e6-4a2b-acab-16410696343b_1024x562.png)
*来源：SemiAnalysis*

我们的评级分类为白金（Platinum）、黄金（Gold）、白银（Silver）、青铜（Bronze）和表现不佳（UnderPerform）。我们将在本报告后文详细解释每个评级。

此外，我们还将讨论 H100 租赁市场及其走向、超大规模云厂商与新兴 GPU 云的价格对比、集群级 TCO、集群回报与情景分析、围绕需求的各种争论，并把这一框架/分析应用于 CoreWeave 及其 IPO。

![](https://substack-post-media.s3.amazonaws.com/public/images/c5e7a2bb-74d5-4f52-9035-42a3ac7fa09d_1024x211.png)
*来源：SemiAnalysis*

## 执行摘要

1. SemiAnalysis 开发了全球首个 GPU 云评级系统——我们将其命名为 ClusterMAX™。我们从一个普通理性客户的视角来评估 GPU。
2. SemiAnalysis 已独立测试了数十种 GPU，按 GPU 数量计，ClusterMAX™ 目前覆盖整个 GPU 市场的约 90%。
3. 当前 GPU 云行业的整体水准非常低。ClusterMAX™ 旨在提供一套准则，帮助提升整个 GPU 云行业的水位。ClusterMAX™ 准则评估的是大多数 GPU 租用者关心的特性。
4. ClusterMAX™ 共有五个不同级别：白金（Platinum）、黄金（Gold）、白银（Silver）、青铜（Bronze）和表现不佳（UnderPerform）。
5. 我们将每 3-6 个月定期开展 ClusterMAX™ 评级与评估工作，让各家 GPU 的改进得以及时反映，客户也能获得 GPU 的最新信息。
6. ClusterMAX™ 白金代表正在抬升行业水位的 GPU 云，而达到这一层级的 GPU 云只有一家——CoreWeave。
7. CoreWeave 是目前唯一一家有可靠运营 10k+ H100 大规模集群经验的非超大规模云厂商。
8. ClusterMAX™ 青铜类别中的一些供应商已经在奋起直追，例如 Google Cloud。我们相信，到下一次重新评估时，Google Cloud 正走在直通 ClusterMAX™ 黄金或 ClusterMAX™ 白金的火箭轨道上。
9. 企业主要从超大规模云厂商和 CoreWeave 租用 GPU。企业很少从新兴 GPU 云租用。
10. 超大规模云厂商的 GPU 租赁价格高于 Neocloud 巨头和新兴 GPU 云，因为超大规模云厂商主要服务企业市场。
11. 在超大规模云厂商中，Oracle 的 GPU 租赁价格处于最低之列。
12. 在技术实力过硬的 GPU 云中，Nebius 提供中短期租赁的最低绝对价格和最优条款。Crusoe 在强大技术实力之外，也提供合理的定价与合同条款。
13. 正如我们在 [2023 年 12 月发表的 GPU 云经济学文章](https://semianalysis.com/2023/12/04/gpu-cloud-economics-explained-the/)中首次讨论的，技术进步意味着算力成本会随时间下降，我们如今认为 GPU 租赁已是买方市场。上百家 GPU 云都在争夺基本相同的客户。
14. DeepSeek 的发布曾让 H200 租赁价格获得短暂的企稳甚至上涨，但中长期看，价格仍在下行。
15. 「首席营收毁灭官」黄仁勋上周说：*「等 Blackwell 开始大量出货，Hopper 你送人都没人要。」* 从 GPU 运营方的视角看，这应是对 GPU 租赁供应商的一声警钟——务必签订能保护自己免受算力价格快速下跌影响的合同，即尽可能签长期合同。而从客户的视角看，他们可能更偏好灵活的承诺，选择更短期的合同。
16. 我们将在文末进一步讨论 GPU 租赁定价与 GPU 的 IRR，以及不同合同期限下的近期 GPU 租赁市场价格。如果你主要关心 GPU 的财务面，或者如何思考 GPU 租赁业务的单位经济模型，请直接下拉到文末。

## GPU 云 ClusterMAX™ 评级系统

ClusterMAX™ 评级的目标是评估并基准测试 100 多家 GPU 供应商。这能让更广泛的 ML 社区了解每家 GPU 供应商的能力、特性、优势与劣势，帮助租用方了解哪些 GPU 云最能满足其需求。我们的第二个目标是提供一套准则，帮助提升整个 GPU 云行业的水位。目前，这个水位低得超乎你的想象。

![](https://substack-post-media.s3.amazonaws.com/public/images/1e5d7753-8cfc-4b4e-94cb-aa313c6feb6e_1024x560.png)
*来源：South Park*

ClusterMAX™ 有望抬升行业水位。过去一年里，我们一头扎进深水区，做了大量的基准测试与性能剖析，见识了 GPU 供应商的最佳与最差实践。我们的测试规模从单节点一路扩展到 1024 GPU 集群，今天我们向社区分享我们的发现。

我们评估 GPU 租用者关心的特性，包括：

- 安全
- 生命周期与技术实力
- Slurm 与 Kubernetes
- 存储
- NCCL/RCCL 网络性能
- 可靠性与服务等级协议（SLA）
- 自动化的主动与被动健康检查及监控
- 消费模式、性价比与可用性
- 技术合作伙伴关系

在今天的报告中，我们将深入讲解我们如何评估 GPU，相关准则见后文。

我们将每 3-6 个月重新评估并更新 GPU 云 ClusterMAX™ 层级榜单，以纳入 GPU 租赁市场的新信息。我们希望给 GPU 供应商反馈和改进的机会，我们也始终欢迎并珍视与 GPU 供应商的对话。

我们将 ClusterMAX™ 评级体系分为五个层级：

- ClusterMAX™ 白金（Platinum）
- ClusterMAX™ 黄金（Gold）
- ClusterMAX™ 白银（Silver）
- ClusterMAX™ 青铜（Bronze）
- 表现不佳（UnderPerform）

每个层级都有支撑其评级的特质。下面从最好到最差逐一讨论。

**ClusterMAX™ 白金（Platinum）** 层级代表业内*最优秀*的 GPU 云供应商。该类供应商在各项评估标准上始终表现卓越，包括安全、性价比、技术实力、有明确 SLA 背书的可靠性、无缝的托管 Slurm/Kubernetes 服务，以及一流的 NCCL/RCCL 网络性能。白金级供应商积极主动、勇于创新，并与社区保持活跃的反馈闭环，持续抬升行业水位。这正是他们成为翘楚的原因。

**ClusterMAX™ 黄金（Gold）** 层级供应商在大多数关键评估类别中表现出*强劲*的实力，同时存在一些改进空间。他们提供扎实的安全、可靠的基础设施、有竞争力的定价以及称职的技术支持。尽管黄金级 GPU 云在主动健康检查等特性上可能存在缺口或不一致，但总体上对反馈响应及时、有持续改进的承诺。他们是 GPU 租用者最大化吞吐量的绝佳选择。

被评为 **ClusterMAX™ 白银（Silver）** 的供应商提供*合格可用*的 GPU 云服务，在性能、安全与价值之间取得尚可的平衡，但与黄金或白金级服务相比通常存在明显差距。这些供应商满足可靠性、安全、支持方面的基本标准，网络性能尚可，但缺乏高级编排能力，或定价结构令人困惑。白银级 GPU 云仍有改进空间，通常能从采纳行业最佳实践中显著受益。

**ClusterMAX™ 青铜（Bronze）** 层级包括满足*最低*标准、但在我们的评估领域中持续表现出短板的 GPU 云供应商。常见问题可能包括：支持服务不稳定、网络性能欠佳、SLA 不明确、与 Kubernetes 或 Slurm 等主流工具集成有限、或定价缺乏竞争力。该层级的供应商需要在可靠性和客户体验上做出相当大的改进。该类别中的一些供应商已经在努力追赶——例如 Google Cloud——我们很期待看到他们 3-6 个月后的下一次 ClusterMAX™ 成绩。

被归入 **表现不佳（UnderPerform）** 类别的 GPU 供应商在多项重要评估指标上未能满足行业与安全的基本要求。该层级的供应商通常存在严重问题，如不安全的实践、可靠性或在线率低下、营销信息不清晰或误导、技术知识或客户支持有限，以及编排能力不足。最常见的情形是，表现不佳层级的供应商没有 SOC2 合规，或者存在安全风险——你的工作负载与互联网之间的流量可能被网络设备记录下来。落入 **表现不佳** 类别的 GPU 供应商，往往正是那些在互联网上群发 AI 生成广告的公司。

## 黄仁勋，「首席营收毁灭官」

「首席营收毁灭官」黄仁勋上周说：「等 Blackwell 开始大量出货，Hopper 你送人都没人要。」

早在 2024 年 4 月，我们在 [AI 云总拥有成本模型](https://semianalysis.com/ai-cloud-tco-model/)中的定价模型就预示了这一结局。2024 年全年，随着 H100 产能爬坡，GPU 价格持续下行；到 2024 年底，随着买家把重心转向 Blackwell 战略，跌势仍在延续。一年之后回看，我们的预测几乎分毫不差，H100 SXM 的误差范围仅在 2-3%。

![](https://substack-post-media.s3.amazonaws.com/public/images/d57f668f-d504-4b6d-a513-9145e2746ba1_1024x670.png)
*来源：SemiAnalysis*

该预测模型有三个主要输入：

1. **全球 AI 加速器装机量**：我们利用我们的[加速器行业模型](https://semianalysis.com/accelerator-industry-model/)确定迄今每一款 GPU SKU 的装机量，并基于供应链分析对未来 GPU 出货量做出预估。

2. **AI 集群的总拥有成本**：我们计算一个 AI 集群的总拥有成本，既包括 AI 服务器、网络、存储、安装与服务等资本成本，也包括托管机房租赁、电力成本、远程运维与支持工程师、互联网连接等运营成本。

3. **AI 加速器的算力吞吐**：估算与实测的有效训练 FLOPS 和推理吞吐（单位为 tokens/秒/GPU）。对某些系统，我们的 AI 工程团队进行了训练与推理的性能剖析和基准测试；对其他系统，我们基于芯片规格和架构估算了产出。

我们将算力总成本与算力吞吐结合，计算出以训练每有效 PFLOP 的 $/hr 和推理每百万 token 的 $/M tokens 计的算力成本。

算力的市场成本随后由各加速器按其装机量加权平均得出。有了这个算力市场成本，再乘以某一加速器的算力能力，即可算出该加速器的「按市价计」（mark to market）租赁成本。

下表给出了这一预测机制的一个简单示例。从中可以看到，以 $/M tokens 计，GB200 NVL72 的推理单位成本比 H100 低 75%；以每有效 PFLOP 的 $/hr 计，其训练成本低 56%。这意味着，如果 GB200 NVL72 设定了算力市场价格，那么 H100 每小时的价格必须比 GB200 NVL72 低 65%，买家才会在两者之间无差异。要与每 GPU 小时 $2.20 的 GB200 NVL72 竞争，H100 的租金必须定在每 GPU 小时 $0.98。

![](https://substack-post-media.s3.amazonaws.com/public/images/609df1e8-dde3-471f-a54f-7b1618faf9b1_1734x1204.png)
*来源：SemiAnalysis*

算力成本低得多的系统日益普及，这一动态推动整体算力成本（以 $/M tokens 和每有效 PFLOP 的 $ 计）走低，进而拖累旧款显卡的租赁价格同步下行。

在付费墙后（文末），我们对 GB200 未来定价、H100 与 GB200 新兴 GPU 云的 IRR 估算以及不同合同期限的市场价格做了深度解析。我们还将讨论如何把上述框架应用于分析 CoreWeave 的单位经济模型与潜在投资回报。以上基本就是给 AI TCO 模型做的中插广告。现在，回到 ClusterMAX™ 评级。

## GPU 云 ClusterMAX™ 评级系统准则

我们的 GPU 云 ClusterMAX™ 评级是基于大多数 GPU 租用者对 GPU 的期望设计的。在进入准则之前，先讨论 GPU 用户的需求。我们的准则优先考虑 GPU 用户的需求及其偏好的使用体验。

大多数 GPU 租用者希望 GPU 节点开箱即带托管的 Slurm/Kubernetes，从而可以专注于编写代码、训练和部署他们的 PyTorch/JAX 模型。GPU 租用者希望在基本无需操心底层基础设施管理与维护的情况下，进行从小到大规模的实验。大多数 GPU 租用者明白 GPU 有时会出故障，而当故障发生时，他们希望对根因以及供应商如何解决问题拥有完全的可见性。

为打造 ClusterMAX™ 评级，我们与许多 GPU 租用者交流，了解他们对 GPU 的需求与期望。基于这些交流，我们在评估中考察以下属性：

- 安全
- 生命周期与技术实力
- 可靠性/SLA
- Slurm 与 Kubernetes 服务
- NCCL/RCCL 网络性能
- 存储
- 主动/被动健康检查与监控
- 定价与消费模式
- 技术合作伙伴关系

## 安全

我们从安全讲起，因为对许多 GPU 租用者来说，这是一票否决的关键因素。他们把专有模型权重存放在 GPU 上——这些权重训练成本从数万到数千万美元不等，是大多数 GenAI 公司的核心知识产权。此外，训练和/或推理这些 ML 模型可能涉及专有信息、个人身份信息或其他用户数据。租用 GPU 的这些公司的客户，不希望因为使用了一家不安全的 GPU 云而导致数据泄露。在欧盟国家，赌注更高，因为依据 GDPR 法律，泄露用户数据会招致巨额罚款。

我们还注意到，全行业存在一条长长的尾巴：大量新兴 GPU 云连最基本的 SOC2 或 ISO 27001 安全认证都没有。我们甚至看到「AMD Alliance Instinct Cloud Partners」名单上的一些云也不具备 SOC2 或 ISO27001 这类基本安全。我们已与 AMD 沟通，他们确认正在调查此事，并承诺帮助提升这一议题上的行业标准。

企业大多从超大规模云厂商租用 GPU，因为 GPU 用户信任超大规模云厂商会正确落实安全措施。我们开始看到一些企业考虑从新兴 GPU 云租用，且大多数都倾向 CoreWeave。这些企业执行更严格的尽职调查，从非超大规模云厂商租用时风险厌恶程度更高。

许多企业甚至没有用于验证云安全性的检查清单，因为他们默认会获得与向超大规模云厂商租 CPU 同等的安全。进入企业市场的新兴 GPU 云（如 CoreWeave）必须向潜在企业客户证明自己是安全的。以 CoreWeave 为例，它已经跨过了这道坎，客户中包括 Jane Street 等金融公司。Jane Street 这类高频交易公司有着最严苛的安全要求，因为它们处理的是专有数据与算法——那是它们赚钱的秘方。

确保租户网络隔离对防止未授权的数据访问至关重要。在以太网上，这通过在网络交换机上设置 VLAN 实现：租户 A 的节点只能与租户 A 的节点通信，租户 A 的节点不能与租户 B 的节点通信，反之亦然。在以太网上，租户隔离也可以用 DPU（如 Bluefield-3）来实现，由 DPU 而非网络交换机来管理隔离。我们看到只有最先进的 GPU 云运营商用 DPU 实现租户隔离——例子包括 CoreWeave、OCI、AWS、GCP 和 Azure。

其他 GPU 云缺乏充分利用 DPU 功能集的技术能力，只能退而求其次，在网络交换机上实现租户隔离。在 InfiniBand 上，租户隔离通过[分区键（Partition Keys）](https://docs.nvidia.com/networking/display/winof2v310lts/infiniband+network)（PKeys）完成。我们建议 GPU 租用者在云主服务协议（MSA）中明确要求：以太网和 InfiniBand 网络均通过 VLAN 或 IB PKeys 实现租户网络隔离，以确保通过适当的租户隔离获得进一步保护。

除 PKeys 外，InfiniBand 上还有其他一些密钥，GPU 运营商必须设置它们以确保安全，防止 InfiniBand 网络被轻易劫持：

必须设置[子网管理器密钥（Subnet Manager Key，SM Key）](https://docs.oracle.com/cd/E76424_01/html/E36266/z4001ba12074893.html)，以防止未授权的子网管理器/UFM 部署。还必须设置[管理密钥（Management Key，MKey）](https://docs.nvidia.com/networking/display/ibdiagnetusermanualv290/infiniband+security#src-80580471_safe-id-SW5maW5pQmFuZFNlY3VyaXR5LU1hbmFnZW1lbnRLZXkoTUtFWSk)，保护 fabric 免遭未授权的配置更改。为防止 fabric 的拥塞控制功能被劫持，必须设置[拥塞控制密钥（CongestionControl Key，CC Key）](https://docs.nvidia.com/networking/display/ibdiagnetusermanualv290/infiniband+security#src-80580471_safe-id-SW5maW5pQmFuZFNlY3VyaXR5LUNvbmdlc3Rpb25Db250cm9sS2V5KENDS2V5KQ)，在非阻塞 IB fabric 上同样需要设置。对启用了 SHARP 网内归约的 InfiniBand fabric，必须启用[聚合管理密钥（Aggregation Management Key，AM Key）](https://docs.nvidia.com/networking/display/ibdiagnetusermanualv290/infiniband+security#src-80580471_safe-id-SW5maW5pQmFuZFNlY3VyaXR5LUFnZ3JlZ2F0aW9uTWFuYWdlbWVudEtleShBTUtleSk)，防止 InfiniBand 的 SHARP 聚合管理器被劫持。可以看到，为确保安全必须设置的 InfiniBand 安全密钥数量众多；然而，Nvidia 缺乏公开文档，行业整体对这些关键密钥也普遍缺乏认识和教育。

我们建议 Nvidia 提供公开可访问的 InfiniBand 安全文档与培训，帮助 GPU 云正确完成配置。我们已把许多 GPU 云直接引向 Nvidia 获取最佳实践。

作为 GPU 租用者，我们建议你在云主服务协议（MSA）中明确要求设置 PKeys、AM Keys、SM Keys、M Keys、CC Keys、VS Keys，以进一步确认你租用的 GPU 已启用这些安全防护。

CoreWeave 过去提供多租户 GPU 集群服务的方式是：用单个 Kubernetes 集群承载多个租户，再在同一 Kubernetes 集群内以 Kubernetes 命名空间隔离各租户，为每个租户提供一个 [vCluster](https://www.vcluster.com/docs/vcluster/introduction/what-are-virtual-clusters)。这项如今常被称为「CoreWeave Classic」的服务并不安全，CoreWeave 早在几年前就已弃用这种以 Kubernetes 命名空间隔离租户的集群实现方式。

CoreWeave 已改为每个 Kubernetes 集群只承载一个租户，因为这才是真正安全的实现。在这种实现下，一个物理集群将包含多个 Kubernetes 集群，每个租户拥有自己的 Kubernetes 集群，而不再只是拥有一个 Kubernetes 命名空间。

租户之间仅用 Kubernetes 命名空间隔离之所以不安全，是因为存在大量容器逃逸漏洞，主要集中在 GPU 驱动或容器工具链中。这些容器逃逸漏洞会让攻击者逃出容器，在同一主机的其他用户之间横向移动，甚至可能在 Kubernetes 集群内提权到其他租户的主机。

目前，每月都有新发现的已知容器逃逸漏洞，而未知的容器逃逸漏洞可能多达数十个。2024 年 9 月，Wiz 发现了一个影响超过 35% 环境的严重 GPU 容器与 Kubernetes 漏洞。因此，仅做 Kubernetes 命名空间隔离是不安全的。隔离边界应该落在 VLAN 上，并且每个租户应拥有自己的 Kubernetes 集群。

- <https://www.wiz.io/blog/nvidia-ai-vulnerability-deep-dive-cve-2024-0132>
- <https://www.wiz.io/blog/wiz-research-critical-nvidia-ai-vulnerability>
- [https://nvidia.custhelp.com/app/answers/detail/a_id/5614](https://nvidia.custhelp.com/app/answers/detail/a_id/5614https:/nvd.nist.gov/vuln/detail/CVE-2025-23359)
- <https://nvd.nist.gov/vuln/detail/CVE-2025-23359>
- <https://nvidia.custhelp.com/app/answers/detail/a_id/5599>
- <https://nvidia.custhelp.com/app/answers/detail/a_id/5585/~/security-bulletin%3A-nvidia-container-toolkit---november-2024>

许多 GPU 服务采用多租户集群，但每个租户位于不同的特定物理服务器组合上，任意两个租户不共享相同的物理服务器。而对某些 GPU 云服务，特别是按需服务，单台物理主机上可能承载多个租户。如果单台物理主机上有多个租户，就必须做 VM 级隔离——鉴于上述 Nvidia/AMD 几乎每月爆出的容器安全问题，同一主机上多租户之间仅靠容器隔离是远远不够的。再强调一次：如果只使用容器隔离，黑客可以利用这些已知容器逃逸漏洞逃逸到物理主机权限，进而可能窥探其他租户的容器并查看模型权重，甚至可能访问其他服务器并获取其他服务器上租户的模型。我们强烈反对在一台物理主机上仅靠基于容器的隔离承载多个租户。

## 生命周期与技术实力

挑选 GPU 云供应商时，评估其技术实力至关重要，因为这直接影响你团队的整体体验。技术实力的影响在入驻之前就能感受到，尤其体现在营销信息的清晰度、销售流程、透明的定价、合理的主服务协议（MSA）草案、入驻前支持以及数据迁移能力等方面。

此外，评估**销售阶段**——沟通是否透明、技术问题是否得到及时解答、承诺是否界定清晰——同样能反映供应商整体的客户导向。我们看到经验丰富的 GPU 云通常会安排一位技术工程师与客户对接咨询，帮助实现顺畅的销售与入驻体验。

在销售过程中可以问的一个直白问题是：他们是否认识 Sylvain。所有优化过 NCCL 设置与 InfiniBand 交换机配置、并且擅长调试 NCCL 与网络 fabric 的顶级 GPU 云，都与大名鼎鼎的 Sylvain 打过交道。

MSA 中一项必备内容是确切的交付日期。在 GPU 云行业，延期交付现象非常普遍。作为客户，你应当确保对 MSA 中的确切交付日期满意，并确保在出现任何延迟时有退出条款。

在**准备阶段**，领先的 GPU 云通常允许用户提前把数据迁入集群，确保入驻后工作负载可以立即开跑，从而大幅缩短「价值实现时间」。GCP、Azure、OCI、AWS 等所有超大规模云厂商都允许这样做。此外，CoreWeave、Nebius 等大多数新兴 GPU 云也允许客户提前上传超大数据集，以免浪费 GPU 时间。GPU 云应当收集足够的相关信息、提出关键问题，确保不会出现意想不到的磕绊或路障。

**入驻流程**本身至关重要；集群应当按时交付，集群供给应有高度自动化，确保不出现人为错误或失误。交付的集群应当经过考机（burn-in），考机流程与验收测试应公开在其网站上或 YouTube 会议演讲录像中。实例重启应当不出问题：重启之后所有系统都应正常工作，无需手动设置任何东西，例如重新挂载网络文件系统。在入驻阶段应用 ClusterMAX™ 评级系统时，我们评估「价值实现时间」，即「成功启动有用工作的时间」。例如，如果开箱即用就有托管 Slurm 或 Kubernetes，终端用户就不必花几天时间自己摸索安装，从而缩短价值实现时间。

**主力工作阶段**的持续支持至关重要，因为 GPU 的故障率确实高于传统 CPU 服务器。H100/H200 会出现软故障或硬故障，因此拥有优秀的支持服务极为关键。**由于温度更高且三星 HBM 成熟度较低，MI300x 的故障率是 H100/H200 的两倍以上。** 对于维护事件与宕机，我们观察到顶级 GPU 云会沟通正在发生什么、正在执行哪些排查步骤，以及修复的预计时间。对于 1-2 个 GPU 节点的故障，我们观察到顶级 GPU 云会在 90 秒内快速拉起新节点提供给租户，确保客户不必等待排障。顶级 GPU 云还会就宕机向客户做出公平补偿。训练中哪怕只损失一台 GPU 服务器，也意味着集群的相当大一部分不可用，因为大多数训练代码库要求固定数量的 GPU，缺一块 GPU 都无法运行。

最后，在**退出阶段**，我们评估是否存在供应商锁定。超大规模云厂商以高昂的出口流量费著称，以此阻止客户转向其他云。大多数 Neocloud 巨头和新兴 GPU 云在把数据迁往其他 GPU 云时不收取出口流量费。

## Slurm 与 Kubernetes

90% 的客户在推理负载上偏好 Kubernetes，约 50% 的客户在训练中使用 Slurm。排名靠前的 GPU 供应商正日益通过提供经过完整测试、开箱即用的托管 Kubernetes 与 Slurm 环境来拉开差距，同时也提供不带预配置调度器的裸 GPU 节点。客户普遍偏好这些托管调度方案，因为自行搭建 Slurm 和 Kubernetes 会消耗宝贵的 GPU 资源，且搭建可能耗时数天，直接推高成本、延误产出。

![](https://substack-post-media.s3.amazonaws.com/public/images/a7b85212-7b86-46e8-92a3-8e6ed858ae34_1024x765.png)
*来源：Futurama*

我们预计 Slurm 在遥远的未来仍将流行。一个常见误解是：调度器的选择与是否使用虚拟化相互独立无关。你可以用裸金属 Slurm，也可以用带 VM 的 Slurm。Slurm 和裸金属并不互斥。Kubernetes 同理：可以有裸金属 Kubernetes（CoreWeave 即是如此），也可以有带虚拟机的 Kubernetes（例如 GKE 或 EKS）。

![](https://substack-post-media.s3.amazonaws.com/public/images/34dc8687-e088-4457-86c4-7cc3b246da1e_522x238.png)
*来源：SemiAnalysis*

当供应商提供托管的 Kubernetes 和 Slurm 平台时，客户就能最大化 GPU 利用率，显著缩短投入使用的时间。值得注意的是，即便是 **Meta** 和 **Jane Street** 这类技术实力雄厚的机构，也因为其高效与可靠而选择使用 CoreWeave 的托管 Slurm 和 Kubernetes 服务。CoreWeave 的托管 Slurm 与 Kubernetes 对提升有效产出（goodput）和价值实现时间大有助益。一个显著的例外是 OpenAI——出于对通用人工智能（AGI）的高度安全与运营戒备，它选择不使用托管调度器。

![](https://substack-post-media.s3.amazonaws.com/public/images/e122a7c8-31ca-481b-9e31-0576c680ca6e_1024x523.png)
*来源：SemiAnalysis*

我们还发现许多供应商的[开箱即用 Slurm 方案没有配置 topology.conf](https://slurm.schedmd.com/topology.html)。不配置 topology.conf 会导致负载变慢、NCCL 性能下降。一些供应商的 Slurm 方案配置不当，缺少 [pyxis 插件](https://github.com/NVIDIA/pyxis)——该插件支持在 Slurm 中以容器方式构建可复现环境，被 CoreWeave、GCP、AWS、OCI 及其他主要供应商的客户广泛使用。另有一些供应商未正确配置 NVIDIA HPC-X 模块或 Slurm MPI 集成。

## 存储

高效且高性能的存储方案对机器学习负载至关重要，训练与推理皆然。我们看到大多数客户需要托管的高性能并行文件系统（如 Weka、Lustre、Vast Data、DDN），和/或需要托管的 S3 兼容对象存储。

训练期间，必须快速、可靠地访问海量数据以无瓶颈地喂饱 GPU，这意味着模型 checkpoint 的加载与保存需要高性能存储，GPU 才能最大化 MFU，从而显著缩短训练时间。

托管对象存储同样关键，可实现灵活、经济、可扩展的数据存储，让团队高效地存储、版本化并检索训练数据集、checkpoint 和模型产物。

对 ML 推理负载，面向性能的存储可确保模型在生产场景中从存储快速加载。慢速或低效的存储会造成明显延迟，损害终端用户体验，或降低 AI 应用的实时响应能力。因此，评估 GPU 云供应商是否提供可靠的托管并行文件系统与对象存储方案、并确保这些方案在各种负载下都经过优化与验证、表现优异，至关重要。

![](https://substack-post-media.s3.amazonaws.com/public/images/4a75169d-d2ad-48ce-acca-53c1bd1cb2f5_1024x643.png)
*来源：Nvidia*

在使用 GPU 时，用户对存储的两大主要不满是：文件卷随机卸载，以及遇到「大量小文件」（Lots of Small File，LOSF）问题。随机卸载问题的解决方案是使用一个名为「autofs」的程序，它会让你的共享文件系统自动保持挂载。

其次，LOSF 问题很容易避免——只有当你决定自建存储方案（比如 NFS 服务器）而不是向 Weka、Vast 这类存储软件厂商付费时，它才会成为问题。终端用户会非常快地察觉集群上的 LOSF 问题：如果集群存在 LOSF 问题，仅仅是把 PyTorch 导入 Python 这一步都会彻底卡死。

下图来自我们在 Crusoe 集群上的测试，展示了一个经过优化、没有 LOSF 问题的集群存储方案应有的表现。可以看到，即便 GPU 数量扩展上去，将 PyTorch 导入 Python 进程所需的时间依然相当平稳。

![](https://substack-post-media.s3.amazonaws.com/public/images/e62a9ae7-da31-449c-a81a-106344a4727c_1024x677.png)
*来源：SemiAnalysis*

这与运行在未优化共享存储上的集群是天壤之别：在后者上，多节点 Python 训练中导入 PyTorch 所需的时间会爆炸式增长，往往导致集群完全不可用。请注意高性能存储与另一个存在 LOSF 问题的集群之间的行为差异。

![](https://substack-post-media.s3.amazonaws.com/public/images/533539f2-bedd-44a2-8ad0-001ad8a2ad1b_1024x678.png)
*来源：SemiAnalysis*

## NCCL/RCCL 网络性能

选择 GPU 云服务时，对 NCCL/RCCL 网络性能进行全面验证，对最大化训练与推理性能至关重要。供应商应提供经过验证、开箱即用的 NCCL/RCCL-tests 脚本，使客户能够独立确认网络性能，尤其是在 16MiB 至 512MiB 这一现实关键的消息大小区间内。

一个在 all-reduce 上慢一半的网络，会使 O(70B) 训练的 MFU 下降 10%，使 O(8x7B) 混合专家模型的 MFU 下降 15-20%。一个常见误解是推理不需要高速网络。实际上，推理供应商会采用消耗大量网络带宽的技术，如[分离式服务（disaggregated serving）](https://arxiv.org/abs/2401.09670)，以实现高性价比的高性能推理。分离式服务多年来已是行业标准，上周 NVIDIA 开源了分布式推理框架 [Dynamo](https://github.com/ai-dynamo)，进一步普及了分离式服务与众多其他推理优化技术。

![](https://substack-post-media.s3.amazonaws.com/public/images/47be025a-3693-4527-a3bb-249e73e22848_1024x538.png)
*来源：Nvidia*

必须认识到，并非所有纸面 400G 的网络性能都一样——实际网络性能高度依赖于：网络是否无阻塞且做了 rail 优化（rail optimized）、用的是 InfiniBand 还是以太网、用了哪些 NIC 和交换机，以及最后 GPU 运营商是否用 nccl/rccl-tests 正确配置并验证了他们的网络 fabric。

我们观察到采用 ConnectX-7 NIC 的网络 fabric 表现最佳。我们看到，像 OCI 那样用高端交换机精心调优的网络，完全可以与 Spectrum-X 以太网一较高下。InfiniBand 仍然倾向于表现最好，尤其是在启用 SHARP 网内归约时。我们已对 128 GPU 到 1024 GPU 规模的网络做了 NCCL/RCCL 基准测试，并将在未来一两个月内发布的 NCCL/RCCL 网络深度解析文章中公布全部性能数据。我们在即将发布的文章中测试并分析了以下网络：

- 8x400GbE Spectrum-X RoCEv2 以太网 H100
- 8x400G InfiniBand NDR H100
- 8x400G InfiniBand NDR + SHARP H100
- 8x400GbE Oracle Cloud RoCEv2 以太网 H100
- 8x200GbE Google Cloud Fastrak 以太网 a3-mega H100
- 8x400GbE Google Cloud RoCEv2 以太网 a3-ultra H200
- 16x200GbE AWS EFAv3 以太网 p5en H200
- 8x400GbE RoCEv2 以太网 MI300X

即便网络本身无阻塞，我们也发现采用更大 1 跳 rail 优化 pod 的网络能取得更高的 NCCL 性能，因为需要在 rail pod 之间穿行的流量更少，拥塞也随之减轻。在 GCP 的 8x400GbE a3-ultra 上，其 1 跳 rail pod 仅由 4 个节点组成；而在 OCI 以太网和 InfiniBand 参考架构中，1 跳 rail pod 的规模是 32 台服务器。这也是 OCI 的 4x400GbE 服务 NCCL 性能优于 GCP 最新 8x400GbE a3-ultra 服务的原因之一。

![](https://substack-post-media.s3.amazonaws.com/public/images/b35cd7bc-15ad-4807-8a96-39efee590437_1024x549.png)
*来源：SemiAnalysis*

GPU 云实施拓扑感知的租户分配意味着更好的性能——通过把租户节点装箱（binpacking）到所需的最少数量的 rail pod 中，租户节点之间通信的跳数可以降到最低。即便是对无阻塞网络，拓扑感知的租户分配也是必需的。

在租户环境内部，开箱即用的拓扑感知调度配置（如 Kubernetes topology 或 Slurm 的 topology.conf）至关重要，即便在经过优化且无阻塞的网络设置中亦然。我们看到此类配置对某些消息大小可带来 20-30% 的性能提升，且与集群规模无关。我们观察到，这对只使用集群一部分的工作负载以及对占用整个集群的工作负载都有显著影响。我们曾在一个 1024 GPU 无阻塞 InfiniBand 参考架构部署上看到，某些消息大小下 nccl-tests 慢了 20-30%。我们将在 NCCL/RCCL 深度解析文章中展开这一话题。

对基于以太网的部署，了解供应商用的是搭载高质量、久经考验的 NOS（如 Arista EOS）并已针对最优性能妥善调优的高品质 Arista 交换机，还是更廉价的替代品，会显著影响 NCCL 性能。请注意，顶尖交换机公司出色的 Tomahawk5 交换机与中游交换机公司平庸的 Tomahawk5 交换机之间存在可观的性能差距。当 GPU 云没有把白牌（WhiteBox）Tomahawk5 交换机调优好、配置糟糕时尤其如此。把它们调得很好是可能的，只是许多云没做到，因为这做起来很难。

另一个考虑因素是 InfiniBand fabric 上是否启用了 SHARP 网内归约。全世界只有三家 GPU 供应商正确配置了 SHARP——即 CoreWeave、Azure 和 Firmus/Sustainable Metal Cloud。InfiniBand SHARP 通过在 InfiniBand 交换机内部而非 GPU 的 SM 中完成归约来提升网络性能。即便 GPU 供应商启用了 SHARP，终端用户也很难正确调优，并确保其训练与推理代码库使用正确版本的 PyTorch、Nvidia 驱动和正确的 NCCL 库版本，从而真正获得性能提升。

由于这种难度，整个 GPU 云行业全球只有五家客户在生产环境的训练与推理负载中使用 SHARP，而这五家中有一家就是 Nvidia 自己。因此，我们建议 Nvidia 让 SHARP 对 GPU 供应商更易于设置，并默认启用 SHARP，从而改善部署与管理 SHARP 的整体用户体验。

![](https://substack-post-media.s3.amazonaws.com/public/images/ebce5a24-b8d2-4a02-9a25-2a1daf2f02a8_1024x799.png)
*来源：SemiAnalysis*

最后，我们看到排名前 10% 的 GPU 云正在开发 [NCCL profiler 插件](https://github.com/NVIDIA/nccl/tree/master/ext-profiler)，以获得深度性能可观测性，让客户更深入地洞察 NCCL 性能，用于调试与优化。选择把 NCCL 监控插件部署到生产环境的 GPU 云，将帮助其客户实现更快的性能和更高的有效产出，带来更好的整体客户体验和更高的单位支出性能。

![](https://substack-post-media.s3.amazonaws.com/public/images/ca4f394a-acb6-446d-8f85-3cc1dc30a22d_1024x541.png)
*来源：SemiAnalysis*

## 可靠性与服务等级协议（SLA）

可靠性与清晰的服务等级协议（SLA）是你对 GPU 供应商在线时间预期的基础性约定。精确界定供应商如何定义 SLA 事件至关重要——无论是节点故障、链路抖动（link flapping）等网络中断，还是 NCCL 超时这类软硬件层面的问题。举例来说，如果一家 GPU 云的 SLA 定义含糊，哪怕集群中有一块 NIC 每分钟抖动一微秒、导致集群根本无法使用，它也可能声称自己满足了 99% 的 SLA 要求。

NIC 哪怕只抖动一微秒，也会导致 NCCL 停滞，整个训练负载随之挂起。在这种情况下，重启负载可能需要几分钟到 30 分钟不等。顶级 GPU 云的 NCCL 超时率和 NIC 抖动率通常很低，因为他们已经完成了网络与光模块的考机，并采取了给光纤除尘等关键措施——光纤积灰正是有效产出劣化的首要原因之一。

顶级 GPU 供应商通常会列明在何种条件下发放服务积分，包括积分返还机制、这些流程的透明度以及事件解决的周转时间。同样重要的是，供应商是否备有随时可用的「热备件」（hot spares），从而在硬件故障时立即切换，大幅缩短停机时间。

我们看到顶级 GPU 云设有专门的部署团队负责集群考机与部署。这些团队会在单服务器级和全集群级进行集成与测试，期间网络测试会在 OEM 的集成工厂完成。我们建议全集群高温考机至少持续 3-4 周，以便暴露节点各组件中的所有早期失效（infant mortality）故障。

集成团队常会把 LINPACK 包装成他们的考机与验收流程。但我们并不认为这是个好测试：LINPACK 既不大量使用网络，也不重度使用 GPU 的 HBM 显存，只使用并测试 GPU 的 FP64 核心。相比之下，ML 训练对网络、HBM 和 BF16/FP16/FP8 张量核心的消耗都非常重。因此，我们认为应当采用对关键组件进行真正「烤机」的考机与验收测试。

![](https://substack-post-media.s3.amazonaws.com/public/images/c93f730e-bef6-4e0d-a2d8-3a683ae78930_1024x691.png)
*来源：SemiAnalysis*

测试与考机流程旨在部署前识别潜在硬件或网络问题，是必不可少的实践。公开分享考机报告、公开记录测试流程的供应商，展现出更高的问责度与对自身基础设施稳定性的信心。要成为 ClusterMAX™ 白金 GPU 云，这种程度的透明度是必要条件。CoreWeave 通过其 KubeCon 演讲和众多公开博客文章展示了其深入细致的验收与考机流程。

对于 1-2 个 GPU 节点的故障，我们看到顶级 GPU 云通常能在 90 秒内快速拉起新节点交给租户，客户无需等待排障。顶级 GPU 云也会就不可用做出公平补偿。哪怕只是单台 GPU 服务器不可用，也意味着集群的一大部分不可用，因为大多数训练代码库要求固定数量的 GPU，缺一块都不行。

## 自动化的主动与被动健康检查及监控

顶级 GPU 供应商为客户提供可靠的、开箱即用的被动健康检查选项，旨在及时发现 GPU 异常，例如严重的 XID 错误。这些被动检查监控 GPU 的降级回退事件——主要是 GPU 劣化并退回到较慢 PCI 总线通信模式的情形。供应商确保对 GPU 健康状况的持续掌握，检测那些可能演变为性能下降或故障的状态。这些被动健康检查通过确认存储挂载保持稳定可用来验证节点完整性，保障数据可用性与系统可靠性。

在被动监控之外，领先的 GPU 供应商为其方案配备了自动化的每周计划、可抢占的**主动健康检查**，主动地每周验证软硬件性能。这些主动诊断通常包括 NCCL-tests，用于评估 GPU 间通信的完整性与性能，确保集群能高效执行集合通信操作并达到预期参考值。供应商还集成了 NVIDIA 数据中心 GPU 管理器（DCGM）诊断套件（sudo dcgmi diag -r 4），深度评估 GPU 硬件健康，在问题恶化前发现它们。

为进一步强化检测能力，顶级 GPU 供应商引入了精密的每周自动计划的**静默数据损坏（Silent Data Corruption，SDC）检测检查**（如 TinyMeg2），能够及早发现张量核心或 SIMT 单元中的细微损坏问题。他们还配以快速的 ML 训练 Megatron 收敛测试——通常为两分钟的基准测试——快速揭示计算正确性偏差，从而将停机时间降到最低并保障数据准确性。

最后，高端 GPU 供应商提供丰富的**开箱即用 Grafana 监控能力**，让运营者深度洞察集群运行状态。这类监控通常包括 TFLOP/s 估算的实时追踪，可对 GPU 性能做出准确、实时的评估。供应商对关键互连链路提供全面监控，及时发现链路抖动或间歇性连接问题。此外，与 Grafana 等可视化平台的集成带来了直观的监控仪表盘，功能包括实时 Slurm 作业队列集成、性能趋势可视化，以及清晰标示上一次主动健康检查何时执行的指示器，让管理员获得可付诸行动的洞察，保持 GPU 性能与可靠性的最优状态。

## 消费模式、性价比与可用性

定价、消费模式与即时可用性是选择 GPU 供应商时最重要的因素之一。客户希望以最低的价格、最优的条款获得最全面的功能组合。

GPU 算力价格以美元/GPU/小时表示——以配 8x400G InfiniBand 的 H100 SXM 典型按需价格 2.99 美元/小时/GPU 计算，租用一台 8 GPU 服务器每小时花费 23.92 美元，每天 574.08 美元。

对大多数新兴 GPU 云而言，这个价格是全包的，含板载 CPU、网络、电费、本地 NVMe 存储，以及配置妥当的 Slurm 和驱动。客户通常另行租用专用网络存储，用于训练、checkpoint 或管理训练与推理数据，以及对象存储。存储一般单独计费，高性能网络存储约 6-9 美分/GB/月，对象存储约 2-3 美分/GB/月。互联网连接及数据流入流出通常不收费。

订阅 GPU 算力有以下几种选择：

- **按需（On-demand）**：GPU 算力买方按 GPU 实例/服务器的实际使用时长付费，算力价格可调整。这提供了最大的灵活性，最常用于开发、突发推理或个人爱好性质的工作。不过，在三种主要选项中它的价格通常最高。目前最优的按需价格是每 GPU 每小时 2.99 美元。
- **Spot**：又称抢占式，与按需类似，按实例/服务器的实际使用时长计费，但使用可随时被中断，以便为其他负载或用户让路。这最适合不需要实时处理的作业，不过作业的平滑恢复仍是一项发展中的能力。Spot 实例最适合推理负载或可以提前一分钟通知就中断的批处理作业。没有人用 spot 实例做训练，因为多节点实例被随机踢掉是极具破坏性的。Spot 定价让新兴 GPU 云得以灵活地快速释放产能，留给更重要的客户或利润更高的负载。Spot 定价可以低于按需价格——我们见过 2.00 美元乃至 1.00 到 2.00 美元区间的报价。
- **合同/预留（Contract/Reserved）**：算力价格在给定时间内锁定，使用不可被中断。常见合同期限包括一个月、6 个月、一年、18 个月、2 年、3 年。由于 H100/H200 在上百家 GPU 云中广泛可得，大多数客户已不再签 1-3 年期的合约。

可抢占或按需的集群选项提供更多灵活性，特别适合间歇性或弹性负载。一个值得注意的策略正在部分新兴 GPU 云供应商中兴起：以折扣价出售闲置算力，但附带特定条款，允许供应商在出现更高 paying 的客户时短期内（通常七天）收回资源。

Google Cloud Platform（GCP）和 Amazon Web Services（AWS）等供应商通过 flex 模式或容量块（capacity blocks）提供预定容量，让客户在设定的时间段内可预期地访问资源。

从 **GPU 供应商的视角**看，锁定长期合同通常更有利，主要原因是——正如 NVIDIA「首席营收毁灭官」黄仁勋所强调的——GPU 的单位美元性能每年提升极快，尽早锁定让 GPU 云得以通过长期合同提前锁定利润率。

从**客户的视角**看，锁定短期合同通常更有利，理由正是黄仁勋先生在其 GTC 主题演讲中提到的那一点——他每发布一代新 GPU，每年交付的 GPU 单位美元性能就呈指数级提升。

大多数客户正与竞争对手进行一场 AI 军备竞赛，这意味着可用性仍是关键的差异化因素。客户经常需要立即供给资源，不仅希望集群今天就有，简直希望昨天就有。Nebius 和 Crusoe 在这方面都很出色：供应充足，且具备在极短的时间内（通常不到两天）完成从初次接触到签约再到供给大规模 GPU 集群（例如 128 块 GPU）的能力。

Nebius 目前以最优的绝对价格脱颖而出，同时保持扎实的技术能力。他们的打法包括激进的成本优化策略，例如在 GPU 服务器上采用原始设计制造商（ODM）硬件，大幅降低总拥有成本。例如，绕开 Dell、Supermicro 这类通常给服务器加上高达 10-15% 毛利的传统 OEM 供应商，Nebius 通过自主设计的 ODM 机箱把毛利从典型的 10-15% 压缩到约 2%，实现成本削减。

这一策略不仅降低了初始硬件支出，还降低了[持续的电力消耗](https://www.youtube.com/watch?v=jPLbKjYAado)，让 Nebius 得以把可观的节省让利给客户。所有超大规模云厂商也都采用这种 ODM 策略，但 Nebius 是唯一一家部署 ODM 自制机箱的非超大规模云厂商。

对那些看重超大规模云能力与严苛安全措施的客户，Oracle 在定价上具备独特优势。其定价模型反映了企业级安全及与其他云服务的全面整合，与需要深度生态整合或合规导向负载的组织非常契合。因此，虽然 Oracle 未必是绝对最便宜的选择，但它为企业客户带来了卓越的性价比。

## 技术合作伙伴关系

Nvidia 有一个名为「Nvidia Cloud Partner（NCP）」的计划：能满足特定要求的 GPU 云可获得 NCP 地位，Nvidia 会帮助它们获取销售机会，并确保它们与技术人员保持沟通渠道，助力其 GPU 云服务进步。我们发现，拥有 NCP 地位的 GPU 云往往比没有的表现更好。

黄仁勋投资了以下 GPU 云：

- Together AI
- CoreWeave
- Nebius
- Crusoe
- Lambda labs

根据我们的测试，这五家 GPU 云总体上用户体验和性能都不错。五家中有四家的服务达到 ClusterMAX™ 白金或 ClusterMAX™ 黄金标准。

相比之下，我们发现 AMD 投资的 GPU 云往往用户体验不佳，AMD 投资的云中没有任何一家跻身 ClusterMAX™ 白金、ClusterMAX™ 黄金或 ClusterMAX™ 白银。

一些「AMD Alliance Instinct Cloud Partners」甚至不具备 SOC2 这类基本安全。因此，我们认为登上「AMD Alliance Instinct Cloud Partners」名单并不能很好地预示其在 ClusterMAX™ 中会获得高层级。

我们已与 AMD 沟通，他们确认正在调查此事，并承诺帮助提升这一议题上的行业标准。

向 [SchedMD](https://www.schedmd.com/)（Slurm 的开发方）付费购买支持的 GPU 云，可以通过对 GPU 资源稳健高效的管理显著提升客户体验与服务品质。借助 SchedMD 的专业能力，GPU 云供应商能够为用户提供无缝且经过优化的体验，确保计算任务被高效、有效地处理。

## 给 AMD 和 Nvidia 的建议

我们建议 AMD 确保其所有「Alliance Instinct Cloud Partners」取得 SOC2 认证，并确保任何新的「Cloud Partner」在加入之前就具备 SOC2 安全。我们建议 Nvidia 和 AMD 树立全行业的标准，帮助即便是非合作伙伴的云也取得 SOC2 安全认证。取得 SOC2 安全认证对 GPU 云不应该是可选项，而应是必备项。这就像航空公司的 FAA 认证：也许有人愿意搭乘没有 FAA 认证的航班，但大多数人不会。由于大多数模型权重和代码库是价值数万到数百万美元的专有知识产权（IP）而非开源，大多数客户需要 SOC2 这类基本安全。

此外，我们建议 AMD 提供 [pyxis 容器 Slurm 支持](https://github.com/NVIDIA/pyxis)，让在 Slurm 上运行容器有良好的用户体验。目前，在 Slurm 上运行容器颇具挑战，甚至 AMD 自己的内部脚本也因缺少 Pyxis 能力而一团糟。相比之下，在一家配置正确的 Nvidia GPU 云上，用 Pyxis 在 Slurm 上运行容器是毫不费力的体验。

对 NVIDIA，我们建议其提供公开可访问的文档与培训，讲解安全加固一张 InfiniBand 网络所需的各类密钥（SMKeys、MKeys、PKeys、VSKeys、CCKeys、AMKeys 等）。我们建议 Nvidia 帮助其 GPU 云正确加固 InfiniBand 网络，并对所有使用 InfiniBand 的 GPU 云完成一次审计。

此外，我们建议 Nvidia 改善 SHARP 对 GPU 供应商的易用性，并建议其默认启用 SHARP，而不是让 GPU 供应商设置起来困难重重、让终端用户难以在训练与推理负载上看到 SHARP 的真实收益。

我们建议 Nvidia 在每次发布新版 NCCL 之前，对 GCP 网络、AWS 网络和 Oracle 网络执行回归测试，防止其超大规模云合作伙伴的 NCCL 性能出现退化。例如：在 Oracle 上，自 NCCL 2.21.5 起，某些云尝试部署其后直至 2.26 的任何 NCCL 版本时都出现了性能退化。

## ClusterMAX™ 白金级 GPU 供应商

**ClusterMAX™ 白金（Platinum）** 层级代表业内可获得的最高的 GPU 云服务标准。该类供应商在所有关键评估标准上始终表现卓越，包括采取可靠的安全措施、对所提供价值而言有竞争力的定价、深厚的技术实力、有明确 SLA 背书的杰出可靠性、无缝的托管 Slurm/Kubernetes 服务，以及卓越的 NCCL/RCCL 网络性能。白金级供应商积极主动、勇于创新，并与社区保持活跃的反馈闭环，持续抬升行业水位、树立卓越标杆。目前，只有一家 GPU 云正在抬升行业水位、够格 ClusterMAX™ 白金，那就是 CoreWeave**。**

## CoreWeave

CoreWeave 显然在提供最佳 GPU 云体验方面处于领先地位，有效产出极高，并受托为 OpenAI 和 MetaAI 等 AGI 实验室、Jane Street 等高频交易公司、甚至 NVIDIA 的内部集群管理大规模 GPU 基础设施。CoreWeave 是可靠运行大规模 GPU 集群的专家。

CoreWeave 提供 4 种服务：

- CoreWeave 裸金属（不含任何托管调度器）
- CoreWeave 托管 SUNK（Slurm in Kubernetes）
- CoreWeave 托管 Slurm
- CoreWeave 托管 Kubernetes

其裸金属服务不含任何 CoreWeave 托管的软件或调度器，实际上只有两类客户：OpenAI/Azure 和 Nvidia EOS。OpenAI/Azure 选择裸金属，是出于对通用人工智能（AGI）的安全与运营戒备，同时也是为了可靠性与性能而更紧密地掌控集群。至于 Nvidia 租用并用于内部开发的 CoreWeave 11,000 H100 EOS 集群，同样是裸金属——因为 Nvidia 在开发自家 Slurm 和 Kubernetes 运算符与插件期间，自己管理 Slurm 和 Kubernetes 对它很有用。

虽然其余客户都有权不使用 CoreWeave 的托管服务，但所有客户最终都选择了托管服务，因为 CoreWeave 的托管体验实在太出色。

![](https://substack-post-media.s3.amazonaws.com/public/images/6d253a51-251b-4801-b8eb-68ce142c00b0_1024x563.png)
*来源：CoreWeave*

首先，我们要讲 CoreWeave 的自动化节点生命周期控制器：它确保在集群上线期间，每个节点都接受完整的考机测试，以及带 NCCL-tests 和 ib_write_bw 的全集群 InfiniBand 网络高温考机。这轮上线考机不仅筛查硬故障，还会与参考值比对，识别不达性能预期或出现静默数据损坏（SDC）问题的节点。未通过这项全面测试的节点将被自动排空（drain）以供排查，在问题彻底解决之前不会进入客户集群。

![](https://substack-post-media.s3.amazonaws.com/public/images/97d55d02-f36c-406c-a8f7-d3f36e7557eb_1024x454.png)
*来源：CoreWeave*

部署到客户环境后，他们会每隔几秒持续执行被动健康检查，确保 GPU 正常工作。由此带来高有效产出，并自动排空和修复不健康的节点。被动健康检查监控的项目包括：

- GPU 从总线脱落（falling off the bus）
- PCIe 错误
- 以太网与 InfiniBand事件，如链路抖动（Link Flaps）
- 温度状况，如 GPU 温度
- GPU 与 CPU 内存统计，如 ECC 错误率
- Nvidia XID 与 Nvidia SXID 错误码
- 等等

除被动健康检查外，他们还会每周自动排期，在空闲 GPU 上运行主动健康检查，执行一整套主动测试以验证节点健康。这些测试包括：

- NVIDIA DCGM diag level 3 及扩展测试（EUD）
  DtoH 与 HtoD 带宽测试，验证 CPU 到 GPU 的 PCIe 性能
- 本地 NCCL all-reduce 测试，验证 NVLink/NVSwitch/NVLS 性能
- 本地 InfiniBand all-reduce 测试，验证 InfiniBand 性能与链路（通过强制禁用 NVLink/p2p/SHM）
- 成对 GPU ib_write_bw 与 ib_write_latency 双向测试，对照参考值验证网络符合规格
- 成对 CPU ib_write_bw 与 ib_write_latency 双向测试，对照参考值验证网络符合规格
- GPUBurn，验证 GPU 在负载下不会故障
- Nvidia TinyMeg2，验证硬件正确性、确保 GPU 没有 SDC
- Megatron 测试，检验 TFLOP/s/GPU 性能是否与参考值吻合、损失收敛是否与参考损失曲线吻合

通过在集群上线期间以及客户集群的整个生命周期内持续自动排期执行这些测试，他们能够主动摘除不健康节点、防止客户向不健康节点提交作业，从而确保客户获得高有效产出。客户可以在仪表盘中看到每个节点上一次主动健康检查（称为「verification」）的时间。

![](https://substack-post-media.s3.amazonaws.com/public/images/e35561ef-6e1d-4b2b-a2d9-c8cf09775755_1024x392.png)
*来源：SemiAnalysis*

在主仪表盘上，他们还展示各类事件，比如「GPUFallingoffthebus」和「LinkFlaps」这类经典常见错误。在无需改动任何应用/终端用户代码的基础设施层，他们用 "DCGM_FI_PROF_PIPE_TENSOR_ACTIVE * 1979" 追踪当前 fp8 TFLOP/s 的粗略估计（乘 989 即得 bf16 TFLOP/s 估计），并有一套系统来关联哪些告警导致了集群级或作业级 TFLOP/s 的下降。例如，你可以清楚看到作业级 TFLOP/s 的下降是由 PCIeFault 和 IBLink 抖动故障造成的。虽然 DCGM_FI_PROF_PIPE_TENSOR_ACTIVE 并非最精确的 MFU 估计，但它让客户和 CoreWeave 能看清哪些事件与 MFU 下降相关。除 CoreWeave 基础设施层的 MFU 估计外，客户还可以在应用层自行计算 MFU 和 TFLOP/s/GPU，获得更精确的绝对 TFLOP/s/GPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/f832c57d-6ea6-499b-9f82-b8a25860d440_1024x559.png)
*来源：CoreWeave*

CoreWeave 有出色的开箱即用仪表盘，可追踪 InfiniBand 和 NVLink 带宽以及温度等一系列其他统计指标，并全部向终端用户开放以协助调试。正如一些人了解的，冷通道温度在昼夜之间会变化，这些温度变化可能带来 2-3% 的性能差异；CoreWeave 让终端用户对自己所用每个节点的温度传感器拥有完全的可见性。

![](https://substack-post-media.s3.amazonaws.com/public/images/978d5ce0-8662-451f-b642-62e90b664e45_1024x265.png)
*来源：CoreWeave、SemiAnalysis*

所有这些主动与被动指标都会被采集以检测异常值，类似于画一条「最佳拟合曲线」，找出偏离中位数一定范围的节点与数据点。

此外，CoreWeave 通过节点控制器总览改善了客户对可靠性和每个节点状态的可见性：展示每个节点从健康状态，到被分诊排查、被调试，再到被 RMA 退回 OEM 的全过程状态。

![](https://substack-post-media.s3.amazonaws.com/public/images/c3a0699f-7081-4401-8a43-a00bebf0cdf7_1024x635.png)
*来源：CoreWeave*

我们认为 CoreWeave 了不起的地方在于，它提供了一套自动化托管方案，把 ML 工程师或科学家本来就不该操心的事务全部抽象掉。

监控、被动健康检查、自动排期的主动健康检查，加上开箱即用的托管调度器——这一切都回归到 ML 工程师/科学家的本愿：专注于非基础设施事务，拥有一批健康的、经过验证的节点——它们被被动健康检查持续扫描、并被主动健康检查每周自动扫描。但 ML 工程师/科学家也明白，有时东西会坏，坏节点未必会被健康检查逮住；在那些情况下，他们希望对正在发生的一切拥有完全的可见性。

其开箱即用的 Slurm 方案自带 [pyxis 插件](https://github.com/NVIDIA/pyxis)，让可复现容器成为 Slurm 内的一等公民，并自带[自动生成的 Slurm 拓扑](https://slurm.schedmd.com/topology.conf.html)以确保优化的 NCCL 集合通信。CoreWeave 还[开源了其 nccl-tests 脚本](https://github.com/coreweave/nccl-tests/tree/master)以保证可复现性。除 Azure 外，CoreWeave 是仅有的几家提供启用 InfiniBand SHARP 网内归约方案的供应商之一。它还与 Nvidia 及部分客户合作启用 SHARP，优化客户的负载与 NCCL 性能。

这些都是 Meta、Jane Street 这样的公司选择使用 CoreWeave 托管 Slurm/Kubernetes 的原因。

CoreWeave 还提供 Slurm in Kubernetes（SUNK）方案，即在 Kubernetes 内部运行 Slurm。客户可以用它动态地以 Slurm 调度训练、以 Kubernetes 服务承接推理。这个方案除了一个缺点之外几乎没有其他缺点。

唯一的缺点是，修改 GPU vboost 设置要求 Slurm 容器以特权模式运行，不过这只需在 yaml 里很简单地开启即可。有人可能认为 SUNK 意味着供应商锁定，但事实并非如此。如果客户想离开 CoreWeave，可以把批处理脚本和 Kubernetes yaml 文件带到其他供应商——Kubernetes yaml 和批处理脚本是开放标准，在任何正确配置的 Slurm 方案上都能工作。客户之所以持续续约，是因为 CoreWeave 的技术实力、其出色的节点生命周期控制器和健康检查。

在我们对 CoreWeave H100 集群的独立测试中，我们注意到其工程师与解决方案架构师团队是 GPU 基础设施和 NCCL 领域的权威专家。他们的入驻体验顺畅，并提供了一份列明所有 IP 地址和常见 FAQ 的入驻文档。当我们深入追问某些 PCIe AER 健康检查、以及 SMKeys 与 MKeys 的区别等具体 InfiniBand 安全密钥问题时，CoreWeave 无疑是技术上的行家。

自助部署和 CoreWeave 的部署中缺失的一点是：一大堆复杂的拓扑、yaml 文件和 Kubernetes 操作——这些通常不在希望用 Slurm 训练的 ML 科学家的词汇表里。好在 CoreWeave 会为任何希望由 CoreWeave 代为部署的客户指派一名工程师。我们建议 CoreWeave 开发一个 UI 控制台流程来部署其托管 Slurm 方案，最好不超过四次点击。

CoreWeave 集群经常提交[极具竞争力的 MLPerf 训练成绩](https://www.coreweave.com/blog/mlperf-coreweave-nvidia-record-breaking-cloud-native-ai-supercomputer)。此外，[NVIDIA 提交](https://developer.nvidia.com/blog/nvidia-sets-new-generative-ai-performance-and-scale-records-in-mlperf-training-v4-0/)的所有 MLPerf Training 成绩都是在 CoreWeave 11,000 H100 EOS 集群上取得的——NVIDIA 从 CoreWeave 租用该集群。CoreWeave 运营着众多集群，其中许多超过 10,000 块 GPU。凭借与 NVIDIA 的紧密合作，他们能拿到下一代 GPU 产能配给的早期批次；正如我们在 Neocloud 解剖一文中所述，每个 GPU 周期中最先部署的玩家能够从优质客户手中锁定长期的低风险合同。

CoreWeave 是唯一一家能够持续可靠地运营 10,000+ GPU 集群的新兴 GPU 云。除 CoreWeave 之外，仅有的几家能可靠运营这种规模的是四家超大规模云厂商：Azure、OCI、AWS 和 GCP。

从客户角度看，CoreWeave 的一个不足是很少接受短期租赁，其业务大多是面向长期租户的巨型集群。这一点不同于 Nebius 和 Crusoe——它们为 GPU 短期租赁提供有竞争力的条款。

## ClusterMAX™ 黄金级 GPU 供应商

**ClusterMAX™ 黄金（Gold）** 层级供应商在大多数关键评估类别中表现出强劲实力，同时存在一些改进空间。他们提供扎实的安全实践、可靠的基础设施、有竞争力的定价模式和称职的技术支持。尽管黄金级 GPU 云在高级主动健康检查等特定功能上可能偶有缺口或不一致，但他们总体上对反馈响应及时、对持续改进有清晰承诺，是 GPU 租用者最大化有效产出的出色选择。要从黄金升至白金，他们必须有像 CoreWeave 那样抬升行业水位的实绩。

## Crusoe

过去七个月我们一直在使用 Crusoe Cloud，其服务始终令我们印象深刻。他们的控制台 UI 直观易用、对用户友好，大大简化了资源管理与部署。他们在仪表盘中提供的直观体验为 GPU 云市场树立了高标准，尤其是在易用性与可及性方面。

在处理 Crusoe 服务器上的 GPU 总线错误时，我们的体验非常正面。当我们发现 GPU 总线错误时，Crusoe 发来一封邮件协助解决。邮件中，Crusoe 解释说它已自动检测到 GPU 从总线脱落（GPU-fell-off-the-bus）错误，预留了一个热备节点，并请我们在控制台重启节点以完成迁移。Crusoe 自动识别问题、主动修复，并引导用户完成迁移。这种稳健的故障管理提升了用户体验。

![](https://substack-post-media.s3.amazonaws.com/public/images/f46ded0d-c43e-4738-a02e-4bbc619251ac_1024x444.png)
*来源：Crusoe、SemiAnalysis*

起初，Crusoe 缺少完全托管的 Slurm 方案，客户需要通过 Terraform 脚本手动搭建 Slurm 集群。不过，他们以卓越的白手套服务体验弥补了这一复杂性：Crusoe 的工程师亲自为大多数客户完成 Slurm 搭建，确保部署顺畅、摩擦最小。上周的 GTC 上，Crusoe 宣布了名为「[Auto Clusters](https://static.rainfocus.com/nvidia/gtcs25/sess/1736564473769001z9Hl/FinalPresPDF/S74475_1743005927914001c0TT.pdf)」的完全托管 Slurm 服务，补上了这一缺口。这项新服务有望进一步简化客户工作流，消除以往手动部署的复杂性。他们的新「Auto Clusters」产品还将自带[自动生成的 Slurm 拓扑](https://slurm.schedmd.com/topology.conf.html)以确保优化的 NCCL 集合通信，并在检测到不健康节点时自动更换节点。

![](https://substack-post-media.s3.amazonaws.com/public/images/9382f8df-9bc1-435c-bec3-50732f67e479_1024x578.png)
*来源：Crusoe*

Crusoe 已经提供了稳健的、完全托管的 Kubernetes 服务，用户部署和扩展容器化负载非常方便。在监控与可靠性方面，Crusoe 目前实现了基础的被动健康检查；不过与 CoreWeave 等行业领导者相比，这些检查的细致与全面程度仍有差距。他们尚未实现自动化的每周排期主动健康检查（如 dcgm diag、nccl-tests、Nvidia TinyMeg2 等）。但他们表示这项关键功能正在积极开发中，将很快集成到其托管 Slurm 与托管 Kubernetes 服务中，并力争把健康检查推进到 CoreWeave 的水准。

虽然他们不做每周排期的主动健康检查，但在集群上线期间，他们会在集群初始启动时做考机和主动健康检查，进行一定程度的测试与验证。我们建议他们研究 CoreWeave 的集群考机做法，把集群考机推进到与 CoreWeave 同等水平。CoreWeave 已经树立了全集群考机的最高行业标杆。

![](https://substack-post-media.s3.amazonaws.com/public/images/75a5c30f-516f-4c24-881c-fe2a2184f624_1024x538.png)
*来源：Crusoe*

在定价与合同条款方面，Crusoe 提供有竞争力的短中期合同，对初创公司和部分企业很有吸引力。他们的价格与条款不如 Nebius 有竞争力，但对追求简洁 UI 与用户体验、行动迅速的初创公司而言，Crusoe 是有竞争力的。

同样，Crusoe 目前不提供用于 GPU 监控的托管 Grafana 仪表盘，这也是他们已明确的改进领域之一。他们已清晰沟通了在即将推出的托管 Slurm 与 Kubernetes 方案中引入高级托管 Grafana 监控仪表盘的计划，以进一步增强可观测性与易用性。总体而言，Crusoe 对用户反馈响应显著，展现出快速演进产品以满足客户需求、并在 GPU 云市场中有效竞争的坚定承诺。

## Nebius

Nebius 以提供 GPU 云市场的最低定价而著称，这得益于其财务状况。其资产负债表上有数十亿美元且没有存量债务，资金充沛、腾挪空间巨大。这种财务实力直接转化为更大的风险承受力和对业务发展更强的投入。例子包括把 H100 合同桥接到 B200 部署这类创新服务，以及在圣克拉拉无处不在、旨在抢占心智的广告牌。其结果是为客户带来无与伦比的成本节省——Nebius 提供市场领先的条款和极具竞争力的价格。

Nebius 维持低价的关键策略之一，是坚持使用自主设计的原始设计制造商（ODM）机箱。通过内部设计硬件并直接与 ODM 合作，Nebius 绕开了通常加价约 10-15% 毛利的 Dell、Supermicro 等传统 OEM 供应商。Nebius 的 ODM 策略把毛利大幅压缩到约 2%，显著降低了初始硬件投入和电力消耗等持续运营开支。这种成本效率使 Nebius 在非超大规模云厂商中独树一帜——此类优化通常只见于超大规模云厂商内部。

由于其前俄罗斯云服务商的血统，它拥有一支由技术过硬的前俄罗斯工程师组成的极具天赋的团队。不过，Nebius 在用户体验方面仍落后于竞争对手。尽管其按需 NVIDIA H100 的价格约为每小时 1.50 美元（至少每月前一千小时如此）——只有 Lambda Labs 等竞争对手收费的一半——Nebius 的客户增长依然吃力。许多用户仍然首选 Lambda Labs，主要因为 Nebius 的 UI 和 UX 依然过于复杂、不直观，给技术倾向较弱的客户造成了摩擦。Nebius 已承诺修复其 UI/UX 问题。

最后，Nebius 目前提供完全托管的 Kubernetes 方案，但尚未提供全自动的托管 Slurm 集群，这是其产品组合中的一大缺口。他们正在积极开发其「Soperator」Slurm 方案，其中包含基础的被动与主动健康检查。然而，这些检查仍达不到 CoreWeave 等供应商树立的行业领先标准。要匹敌竞争对手的可靠性与可观测性，Nebius 需要在全面的每周排期主动健康检查上加大投入，并实现先进的开箱即用 Grafana 仪表盘。强化这些运营层面，将把可靠性提升到 CoreWeave 的水平并实现自动化节点生命周期，进一步增强其本已颇具吸引力的价值主张。

![](https://substack-post-media.s3.amazonaws.com/public/images/2c0b987e-85fb-4577-a4bb-df2e18481856_1024x793.png)
*来源：Nebius*

## Oracle Cloud Infrastructure

从我们的测试看，OCI 的 GPU 体验强劲，并一直被公认为四大超大规模云厂商中性价比最高的。其 GPU 服务可通过 OCI 市场一键 UI 部署，即同时涵盖 Slurm 与监控的「[OCI HPC stack](https://docs.oracle.com/en/solutions/deploy-nvidia-ai-on-oci-gvt-region/configure-hpc-cluster-stack-oracle-cloud-marketplace.html#GUID-DD03DBFF-0258-4669-9753-72930294287C)」。然而，尽管这套配置令人印象深刻，OCI 的 Slurm 方案并非完全托管——目前是以一两位 OCI 解决方案架构师支持的共同托管形式运作。要保持竞争力——尤其是面对 AWS 和 CoreWeave 全面的托管 Slurm 方案（后者拥有出色的节点生命周期控制器和自动化主动健康检查）——我们强烈建议 OCI 投入打造完全托管的「Oracle Managed Slurm（OMS）」服务，这将惠及各类 Oracle 客户（除 OpenAI 外，因其 AGI 安全政策）。

![](https://substack-post-media.s3.amazonaws.com/public/images/f42966cd-4297-441f-b36a-6daee007249c_1024x919.png)
*来源：Oracle*

在监控、可靠性与被动健康检查方面，OCI 通过其 Slurm HPC stack 市场方案提供了不错的服务，配齐 DCGM、Grafana 监控和被动健康检查。尽管如此，OCI 目前缺少 CoreWeave 方案中的高级主动健康检查与自动化节点生命周期管理，例如每周自动排期的主动健康检查（NCCL-tests、ib_write_bw、dcgm diag）以及自动标记不健康节点。Oracle 已确认该功能已在路线图上，计划于 Q2 完成。OCI HPC stack 的 Slurm 方案还缺失的一点，是与高速并行文件系统（如 OCI 的托管 Lustre 服务）的集成。

OCI 还开箱即用提供自动生成的 `topology.conf` 配置，实现拓扑感知调度以提升网络性能——这是许多新兴 GPU 云供应商仍然忽视的重要特性。

与 GCP 不同，OCI 运营 RoCE 网络已有相当长时间，甚至早于 GenAI GPU 时代。他们拥有阵容深厚的高性能网络专家，如 [Jag](https://blogs.oracle.com/cloud-infrastructure/post/first-principles-zettascale-oci-superclusters) 及其团队。Jag 和他的团队能够从第一性原理出发推演网络问题——例如全行业链路抖动源于 DSP 重校准——同时借鉴数十年的经验。从我们的测试看，OCI 的 RoCEv2 网络与 Spectrum-X 以太网相比非常有竞争力（前提是你在正确的 nccl 版本上并使用了定制的 OCI tuner 插件）。尽管 OCI 的网络栈使用 Nvidia CX-7 NIC，我们仍注意到在 OCI 集群上，nccl 2.21.5 之后的多个版本存在若干小的 nccl tuner 回归，即便通信 SM 数量相同。我们将在即将发布的 nccl/rccl 网络深度解析文章中，展示我们在 OCI 上以真实消息大小运行的多达 512 GPU 的全面基准测试结果。

我们建议 OCI 与 Nvidia NCCL 团队合作，确保在 Nvidia NCCL 团队发布新版 nccl 之前先在 OCI 集群上完成适当的回归测试，使开箱即用的 NCCL tuner 在 OCI 上拥有优化的性能。

归根结底，OCI 的支持与服务团队凭借技术实力和以客户为中心的理念脱颖而出。在我们的整个互动过程中，OCI 团队始终展现出深厚的技术功底和对客户成功的真诚投入。除 GPU 之外，OCI 是一家超大规模云厂商，意味着它还提供数据库、对象存储、基于 CPU 的 VM 等服务，可用于数据处理或网页抓取等任务。

这套完整的基础设施让客户无需从其他超大规模云向专业化 GPU 新兴 GPU 云迁移或串流数据，带来显著的运营效率与更低的复杂度。选择超大规模云厂商的另一个显著优势，是其长期客户合作模式。长期租用算力往往捆绑联合上市（go-to-market，GTM）的合作机会。这些 GTM 合作有望借助 OCI 庞大的客户群扩大客户的市场触达，为客户带来收益。不过，这些 GTM 合作的实际效果因具体情况而异颇大。

在安全方面，OCI 表现卓越，提供一流的企业级标准，包括稳健的租户网络隔离、RoCEv2 fabric 上的 VLAN 隔离，以及 InfiniBand fabric 的 PKEY 隔离。相比之下，许多专注 GPU 的云供应商连 SOC2 或 ISO27001 合规等基本认证、或必要的网络隔离协议都不具备，这使 OCI 成为对安全有严苛要求的企业的优先选择。

## Azure

Azure 提供稳健的 GPU 云基础设施，并以卓越的网络性能著称。根据我们在多达 128 块 H100 集群上的内部测试，Azure 展现了令人印象深刻的能力，尤其值得注意的是其利用 InfiniBand SHARP 实现高效的网内归约。这一先进的网络配置使 Azure 成为高性能、大规模 AI 负载的顶级选择，特别适合密集的多节点训练场景。在我们即将发布的 NCCL/RCCL 深度解析文章中，我们将展示 Azure InfiniBand 网络上开启与不开启 SHARP 的真实 NCCL 基准测试。

安全是 Azure 的另一突出强项。它在稳健的安全与合规实践方面享有卓越声誉，这使其成为政府机构、国防承包商以及 OpenAI 等顶尖 AGI 研究实验室的可靠伙伴。Azure 在大规模下的可靠性有目共睹：它成功管理着庞大的 GPU 集群，包括支持 OpenAI 那些广为人知的、涉及超过 100,000 块 NVIDIA H100 GPU 集群的部署，凸显了 Azure 安全管理高要求、高敏感负载的能力。值得注意的是，OpenAI 对 Azure 巨型集群的可靠性抱怨不少，但 OpenAI 的可靠性标准本就极高，因为它的集群实在太庞大。

在工作负载管理方面，Azure 提供 CycleCloud——一个用户友好的、基于 Web 的 UI，用于部署和管理 Slurm 集群。CycleCloud 包含基础健康检查，可增强可靠性与运营感知。我们期待对 CycleCloud 做完整分析。不过，与 CoreWeave 全自动主动与被动健康检查系统等更先进的方案相比，Azure 的方案仍有改进空间。我们特别建议 Azure 考虑采纳与 CoreWeave 全面做法类似的实践，例如定期自动化检查（包括 NCCL 测试、ib_write_bw 和 DCGM 诊断），以及自动排空与更换节点，以提升整体可靠性。

此外，Azure 提供托管 Lustre 并行文件系统，为大规模 HPC 和 AI 负载量身打造高性能存储。这套集成且经过优化的存储方案确保数据密集型负载能够高效、可靠地扩展。为进一步完善其服务，Azure 若能采纳像 CoreWeave 这类行业领先 GPU 云所部署的更广泛的被动与主动监控方案，将从中受益，为其用户带来更高的可靠性与更完善性能监控。

Azure 的超大规模云厂商地位确保了生态的一体化——无需从别处串流数据，数据可以直接存放在 Azure 原生的 Data Lake 与数据仓库选项中。此外，从 Azure（或其他超大规模云厂商）长期租用算力往往附带「合作伙伴」权益，由这家超大规模云厂商帮助你把产品卖给其他 Azure 客户。

## Together AI

从我们的测试看，Together AI 在 GPU 云供应商市场中格外突出。单论其集群服务，通常只能算 ClusterMax™ 白银级；真正把它抬升到 ClusterMax™ 黄金的是其卓越的支持与技术实力。Together AI 的团队由 Flash Attention 发明者 Tri Dao 领衔，其 Together Kernel Collection（TKC）显著提升了客户性能。我们估计其 GPU 云客户中约有 30-40% 在使用 TKC。我们认为，不克隆一个 Tri Dao，别处无法复制 Together 创造的价值。通过测试，我们验证了 TKC 对训练与推理的真实性能提升，Tri Dao 的内核确实是实打实的性能增益。

![](https://substack-post-media.s3.amazonaws.com/public/images/7b67fe87-6a49-4474-9bc2-28c8a7a51367_1024x548.png)
*来源：Together AI*

即便不使用 TKC 的客户，也大大受益于 Tri Dao 团队在训练负载调试、优化与排障方面的咨询专长。这种组合创造了真正全方位、有支持的服务体验，远不止出租 Kubernetes 或 Slurm 托管集群。其有竞争力的定价进一步增强了吸引力。

此外，Together AI 提供直观、用户友好的托管 Slurm 与 Kubernetes 方案，可直接通过其仪表盘访问，[只需几次点击即可完成部署](https://www.youtube.com/watch?v=J8vTTRi2GN4)。作为 NVIDIA 投资组合公司，Together AI 还能提前获得 Blackwell GPU 等新 NVIDIA 硬件，并与 NVIDIA 紧密合作开发面向下一代 GPU 的优化内核。

![](https://substack-post-media.s3.amazonaws.com/public/images/35adb7f3-ccfa-48a7-82a7-7a9edfb5fa1a_1024x621.png)
*来源：Together AI*

不过仍有改进空间。Together AI 目前缺少用于 Slurm 环境容器管理的 Pyxis 插件，也不提供稳健的被动健康检查或每周排期的主动健康检查，可靠性方面存在隐忧。其默认 Grafana 仪表盘与竞争对手相比也较为基础。

我们建议 Together AI 实施类似 CoreWeave 的全面健康检查体系，以及更丰富、更细致的 Grafana 仪表盘。此外，由于 Together AI 目前依赖 Applied Digital 或 Crusoe 等其他 GPU 云提供的基础设施，支持问题的解决可能因「传话游戏」而延迟。好在这一点将大幅改善：Together AI 计划年内部署自己的硬件基础设施，摆脱目前对外部供应商的依赖，让问题解决更顺畅。

## LeptonAI

LeptonAI 是由 PyTorch 联合创造者创立的 GPU 云。LeptonAI 不拥有任何 GPU，而是提供用于管理 GPU 和健康检查的 ML 平台软件层。他们会声称自己就是你的超级计算团队。你可以通过他们租 GPU——由他们从其他供应商租来 GPU，LeptonAI 加上他们的软件和每 GPU 小时几美分；你也可以从定价出色的 Nebius 租 GPU，然后按每 GPU 小时几美分购买 LeptonAI 和支持，获得整套 LeptonAI 平台。LeptonAI 把大型科技公司（Google、Meta 等）的 ML 平台经验带给更广阔的世界，让普通用户也能用上。LeptonAI 的工程师显然深谙其道，对客户想要什么有很强的产品感觉。

训练方面，他们提供一种类 Slurm 的作业提交方式。在我们的测试中，只花了几分钟就改好了 sbatch 脚本使其在 LeptonAI 平台上运行。切换到 LeptonAI ML 平台做训练相当直观。LeptonAI 应当推出完整的 sbatch 超集 API，而不只是「类似 Slurm sbatch」。

在 LeptonAI 平台中，你可以在控制台仪表盘查看节点生命周期，看到每个节点上的作业与状态。他们的节点生命周期可视化出类拔萃，唯一拥有更好节点生命周期仪表盘的公司是 CoreWeave。

![](https://substack-post-media.s3.amazonaws.com/public/images/97c319f9-40fe-47af-8689-7232ecb5781b_1024x423.png)
*来源：LeptonAI*

被动健康检查方面，LeptonAI 运行 gpud——这是他们[开源的](https://github.com/leptonai/gpud/tree/main/pkg) GPU 被动健康检查方案，覆盖了大多数被动健康检查项。这套被动 GPU 检查仍在完善中，但已是一个强有力的方案。

![](https://substack-post-media.s3.amazonaws.com/public/images/d7668954-924d-43e9-b688-d0152eb96290_1024x469.png)
*来源：LeptonAI*

LeptonAI 也有手动主动健康检查，如 DCGM diag 和 nccl-tests，但需通过 UI 仪表盘手动运行，并非像 CoreWeave 那样每周自动排期执行，而且 LeptonAI 不提供 NCCL 测试应有的参考值。我们建议他们提供一个让客户选择加入自动排期主动健康检查的选项。LeptonAI 也没有 Megatron 损失收敛主动健康检查，也没有 Nvidia TinyMeg2 SDC 检测主动健康检查。

![](https://substack-post-media.s3.amazonaws.com/public/images/0424d2f9-3938-4d6b-ac45-ed00dcff35c0_1024x503.png)
*来源：LeptonAI*

LeptonAI 还有一些 beta 功能，比如零影响的 NCCL profiler：客户只需勾选一个复选框，就能充分利用其自研的 NCCL profiler 来可视化集合通信瓶颈，帮助客户优化网络瓶颈。

![](https://substack-post-media.s3.amazonaws.com/public/images/42c1cc45-b3db-4491-b8d7-2dbd6348f5ea_1024x488.png)
*来源：LeptonAI*

## ClusterMAX™ 白银级 GPU 供应商

被评为 **ClusterMAX™ 白银（Silver）** 的供应商提供合格可用的 GPU 云服务，在性能、安全与价值之间取得尚可的平衡；不过，与黄金或白金级服务相比，它们通常存在更明显的差距。这些供应商满足可靠性、安全与支持方面的基本行业标准，但可能缺乏高级编排集成、网络性能中等，或总拥有成本（TCO）偏高，导致客户承担更高的价格。**ClusterMAX™ 白银** 供应商对客户和 SemiAnalysis 的反馈持开放态度，正在积极寻求改进，力争未来与 ClusterMAX™ 白金竞争。

## AWS

我们对 AWS 听到的头号抱怨是：它的网络比 InfiniBand 和 Spectrum-X 以太网差。事实确实如此，AWS 也一直在改进，于 2024 年 12 月发布了新的 p5en EFAv3 16x200GbE H200 实例。

在 nccl-tests 上，其 EFAv3 实例比当年的 EFAv2 实例要接近 InfiniBand/Spectrum-X 性能得多。

AWS 的 P5 EFAv2 实例是 32x100GbE，逊于 InfiniBand/Spectrum-X/RoCEv2，但根据我们的 nccl-tests 测试，优于 2024 年 4 月发布的 GCP a3-mega 实例（8x200GbE）。我们的 NCCL 测试还显示：其 H100 p5 EFAv2 的网络优于 GCP a3-mega；其新的 H200 p5en EFAv3（16x200GbE）的网络也优于 GCP a3-mega。而 GCP 2025 年 1 月公开发布的新 h200 a3-ultra 服务（8x400GbE RoCEv2 以太网）的网络性能优于 AWS 新的 p5en EFAv3 服务。我们将在即将发布的 nccl/rccl 网络深度解析文章中，展示我们在真实消息大小上运行的结果与基准。

AWS 不只是一朵纯 GPU 云，还具备云的其他全部服务，如 Bigtable、数据库、对象存储和并行文件系统，可满足数据处理和网页抓取之需。作为一朵完整的云，它意味着你不需要把数据从完成数据处理的「主超大规模云」复制（或串流）到新的云集群——你的所有数据本来就在那里。从超大规模云长期租用算力往往附带「合作伙伴关系」和联合上市的额外好处，AWS 会帮你向企业和其他 AWS 客户销售。GTM 合作是否有效，真的要看具体情况。

AWS 还提供名为 FSX 的托管 Lustre 并行文件系统，用作集群范围的 POSIX 网络存储。对象存储方面，他们还有大名鼎鼎的 S3 托管对象存储服务。

![](https://substack-post-media.s3.amazonaws.com/public/images/ed00a7e4-500d-4b37-9bbd-03937cac2bb3_890x608.png)
*来源：AWS*

AWS 提供名为 Hyperpod 的托管 Slurm 与 Kubernetes 服务，大幅简化了集群搭建。他们提供 UI 仪表盘和易于遵循的设置指引来完成托管服务的部署。

![](https://substack-post-media.s3.amazonaws.com/public/images/4a94fb46-1715-416f-acee-c2e22e62e00a_1024x349.png)
*来源：AWS*

Hyperpod 包含基础的被动与基础主动健康检查，还集成了简洁的 Grafana 仪表盘用于监控系统健康。遗憾的是，开箱即用状态下，它缺少自动化的主动健康检查，例如每周运行 nccl-tests、Nvidia 的 tinymeg2 SDC 检测器和 Megatron 收敛测试。

![](https://substack-post-media.s3.amazonaws.com/public/images/ff021e49-f772-4b17-93d1-24f047243270_1024x355.png)
*来源：AWS*
![](https://substack-post-media.s3.amazonaws.com/public/images/fcbc729c-6d46-4f23-83b4-66f485514815_1024x543.png)
*来源：AWS*

为进一步提升服务，AWS 应继续投资网络改进，并考虑将高级被动与主动的每周自动排期健康检查策略作为开箱默认或以简单复选框的形式让终端客户选择加入，就像 CoreWeave 所做的那样。

## Lambda Labs

Lambda Labs 被公认为按需 GPU 实例的首选供应商，主要得益于其出色的用户界面和直观的控制台体验，尤其是无缝的 JupyterLab 集成。尽管存在其他供应商——例如 Nebius 以一半的价格提供 H100 SXM GPU——Lambda 的按需 GPU 实例依然受欢迎，因为其他家的 UX 或安全欠佳。Lambda Labs 的 H100 SXM 定价 2.99 美元/小时/GPU，凭借其庞大的按需业务量，它通常为按需市场设定价格基准。当 Lambda Labs 下调或上调其按需价格时，其余厂商通常跟随。

用户还希望在其按需服务中获得标准 Lambda stack 基础镜像之外更多的基础镜像选择。大量用户和 SemiAnalysis 自己的测试都表明，其按需实例的启动时间过长，通常在 30 分钟左右。作为对比，Crusoe 的 H100 SXM 实例启动时间不到 90 秒。这应该是 Lambda Labs 追求的标杆。此外，Lambda 默认按需实例错误地将 CUDA 工具链和 CLI 工具路径设为 /usr/bin/nvcc，而非行业标准的 /usr/local/cuda/bin/nvcc，导致与许多开源仓库的兼容性问题。我们已与 Lambda Labs 团队沟通，他们承诺缩短其按需实例的启动时间。

![](https://substack-post-media.s3.amazonaws.com/public/images/cd5fe694-04ab-49f4-858c-9e7f1a4f48c2_1024x462.png)
*来源：Lambda Labs、SemiAnalysis*

Lambda Labs 还提供托管 Kubernetes 服务，大大简化了用户的容器编排。其托管 Kubernetes 服务配有开箱即用的控制台 UI 和 Grafana 监控仪表盘，可查看节点与 GPU 指标。此外，他们为终端客户提供开箱即用的 nccl-tests 脚本，供客户验证网络性能。他们还提供基于 Vast Data 的高速并行文件系统作为网络存储。

![](https://substack-post-media.s3.amazonaws.com/public/images/2160bccd-72de-4dc3-a9ad-264891ed960c_1024x549.png)
*来源：Lambda Labs*
![](https://substack-post-media.s3.amazonaws.com/public/images/d812b0eb-3a4d-4ced-8de2-a9c0f518aec7_1024x560.png)
*来源：Lambda Labs*

然而，他们当前的 Slurm 方案是非托管的，且从我们的测试来看并不好。他们缺少 Pyxis Slurm 插件和许多其他 Slurm 功能。好在 Lambda 正在积极开发托管 Slurm 方案，有望显著改善用户体验。

不过，Lambda 仍缺少若干必备功能，例如自动化的被动与主动健康检查；其指标仪表盘目前也遗漏了竞品方案（如 CoreWeave）中的关键 GPU 指标。我们建议 Lambda Labs 研究 CoreWeave 的被动与主动健康检查，并实现可与 CoreWeave 出色的开箱即用 Grafana 仪表盘相媲美的指标仪表盘。

## Firmus/Sustainable Metal Cloud

SMC 是澳裔新加坡可持续 AI 工厂建设者 Firmus Technologies 旗下的 AI 云与 GPU 服务品牌。他们提供 Slurm 与 Kubernetes 调度方案（包括面向容器负载的 Pyxis），并采用 WEKA 的高性能存储平台支撑大规模 AI 应用。从我们的测试看，这是一个相当不错的方案。

在 MLPerf Training v4.0 基准测试中，SMC 训练 GPT-3 175B 模型展现了出色性能。此外，SMC 已提交经过验证的 MLPerf 功耗结果，证实 H100 浸没式液冷的功耗低于可比的风冷 GPU 方案。他们声称，这种电力节省转化为更低的 TCO，并声称凭借更低的 TCO，能够为客户提供更低的价格。

![](https://substack-post-media.s3.amazonaws.com/public/images/c29c80ab-d5e8-4a5d-8396-9fa83631a238_1600x1066.jpeg)
*来源：SMC*

他们是除 CoreWeave 和 Azure 之外少数几家启用 InfiniBand SHARP 网内归约的云之一，并通过 nccl-tests 向我们展示了其更优的网络性能。但他们的客户中没有技术专家，因此客户并未使用 SHARP——因为 SHARP 也需要在客户应用层做调优。他们也分享了未启用 SHARP 的 nccl-tests 结果，同样具有竞争力。

一个值得注意的担忧是：由于在浸没环境中使用了风冷散热器，SMC 的 GPU 在负载下比正确部署的可比风冷方案温度高约 10 度，导致 1-2% 的性能损失。尽管如此，SMC 声称其定价足以补偿这一轻微的性能损失，提供更优的 TCO 性能比。他们正在探索采用浸没专用散热器来解决这一问题。

目前，SMC 缺少 Slurm 和 Kubernetes 的自助部署选项，依赖 SMC 自家工程师协助搭建。建议他们开发用户界面或命令行界面以简化部署。此外，实施类似 CoreWeave 的自动化被动健康检查和每周自动排期主动健康检查，将提升系统可靠性。缺少用于监控 GPU 温度与活动的基本 Grafana 仪表盘是另一个待改进领域，采纳 CoreWeave 的开箱即用监控方案可能有所裨益。

SMC 已展现出对客户和 SemiAnalysis 反馈的接纳态度，正在积极考虑这些建议，以完善其服务并在 AI 云服务市场保持竞争力。

## Scaleway

从我们的测试看，Scaleway 提供稳健的 Slurm 与 Kubernetes 方案，并配有由 VAST Data 驱动的高性能托管文件系统。这一集成确保 AI 与 HPC 负载获得可扩展、高效的数据管理。测试期间，我们注意到 Scaleway 支持 NVIDIA 的 Pyxis 插件，可实现 Slurm 内的无缝容器集成。他们的技术团队对这些技术有深刻的理解。

作为符合 GDPR 的供应商和 NVIDIA NCP 合作伙伴，Scaleway 强调数据隐私，并利用前沿 GPU 技术。然而，他们对「镀金」DGX Hopper 机箱的使用导致更高的总拥有成本（TCO），而增加的成本往往转嫁给客户。我们建议 Scaleway 探索 OEM 替代方案（如 Dell 或 Supermicro 的 HGX SKU），或考虑 ODM 机箱选项，以更低的成本交付同样的性能。请注意，并不建议为了成为 NVIDIA NCP 合作伙伴而购买「镀金」机箱。

![](https://substack-post-media.s3.amazonaws.com/public/images/6bce5065-47a0-48f9-9b41-c47d71263b56_640x354.png)
*来源：Scaleway*

目前，Scaleway 缺少 Slurm 与 Kubernetes 的自助部署选项。尽管其工程师会协助部署，但提供 UI 或 CLI 自助工具将改善用户体验。此外，缺少自动化被动健康检查和每周自动排期主动健康检查令人遗憾。我们建议 Scaleway 研究 CoreWeave 的健康检查做法并考虑采纳类似实践。

此外，Scaleway 未提供用于监控 GPU 指标（如温度和 SM 活动）的基本 Grafana 仪表盘。实现这些仪表盘将为系统性能提供宝贵洞察。令人欣慰的是，Scaleway 一直乐于接受客户和 SemiAnalysis 的反馈，正积极着手弥补这些缺口、完善其服务。

## ClusterMAX™ 青铜级 GPU 供应商

**ClusterMAX™ 青铜（Bronze）** 层级包括满足最低必要标准、但在关键评估领域持续存在显著短板的 GPU 云供应商。常见问题可能包括：技术实力或支持不稳定、网络性能欠佳、SLA 不明确、与 Kubernetes 或 Slurm 等主流工具集成有限，或定价缺乏竞争力。该类别供应商通常需要在可靠性和客户体验上做出相当大的改进。GPU 供应商落入这一层级的另一个原因是：过去几年其方案一直表现平平。

该类别中的一些供应商已经在努力追赶。Google Cloud 就是一个例子——我们相信，到 3-6 个月后的下一次 ClusterMAX™ 评估时，GCP 和其他一些供应商已走在直通 ClusterMAX™ 白金/黄金的快车道上。

## Google Cloud

长期以来，GCP 提供的 GPU 服务都不尽如人意，网络更差、开箱功能更少。自 2024 年 4 月起，它一直处于「追赶」模式。许多客户抱怨过其 GPU 服务，但 Google Cloud Platform（GCP）正在听取反馈、快速改进，努力追赶竞争对手。

回顾历史背景：其第一个 H100 服务名为「a3-high」，[2023 年 8 月发布](https://cloud.google.com/blog/products/compute/announcing-cloud-tpu-v5e-and-a3-gpus-in-ga)，每节点提供 800Gbit/s 的「Fastrak TCP」网络带宽。而当时 Oracle、Microsoft、所有 Neocloud 巨头和大多数新兴 GPU 云提供的纸面网络速度都是 3200Gbit/s。这意味着 GCP 的网络带宽只有竞争对手的 25%。大多数使用 a3-high 的 GCP 客户都不太满意。我们将把 GCP 这段 GPU 历程称为「完全不行阶段」。

Google 听取了客户的这些反馈，[2024 年 4 月](https://cloud.google.com/blog/products/compute/whats-new-with-google-clouds-ai-hypercomputer-architecture)发布了经过改进的第二个 H100 服务「a3-mega」，把每节点网络带宽从 800Gbit/s 的「Fastrak TCP」翻倍到 1600Gbit/s。尽管这是重大改进，但仍比 Oracle、Microsoft、CoreWeave 和 AWS 等竞争对手慢 50%。

根据我们的 NCCL 测试，在真实消息大小上，他们的速度只有竞争对手的一半。网络 NCCL 性能慢一倍传导到端到端训练性能上，就是 O（Llama 70B）规模训练的 MFU 差 10%，O（8x7B）混合专家稀疏模型的 MFU 差 15-20%。而且很长一段时间里，这项服务不支持 LL128 nccl 协议，训练和 nccl 网络性能更糟，终端用户还需要设置复杂的环境变量才能让其 NCCL net/tuner 插件工作。此外，他们的 Slurm recipe 漏洞百出、难以搭建。我们将这称为「追赶阶段」——GCP 显然在努力改进，但尚未追平竞争对手。

GCP 继续收集客户反馈，[2025 年 1 月](https://cloud.google.com/blog/products/compute/a3-ultra-with-nvidia-h200-gpus-are-ga-on-ai-hypercomputer)，他们推出了 a3-ultra 实例，终于提供每节点 3200Gbit/s、配 ConnectX-7 NIC 的 RDMA 以太网，切实提高了每节点的网络带宽。这次更新让 GCP 更接近 Oracle、Microsoft 和 CoreWeave 等竞争对手的能力。

但实际上，他们现实的 NCCL 集合通信网络仍略有差距，我们将在下文详述。凭借新的 a3-ultra SKU，他们从 TCP 转向了基于以太网的 RDMA。大多数人都知道，RDMA 常被选作集群网络协议以取代 TCP，因为其时延更低、AI 集合通信性能更高。我们很高兴 GCP 终于转向更为主流的 GPU 组网方式，但这来得太迟——比竞争对手推出 3200Gbit/s RDMA 网络服务晚了 18 个月。我们将这称为「**即将赶上是**」（almost caught up）阶段。请注意，目前其大多数客户和 GPU 机群仍是 A3-Mega，这意味着大多数客户仍在经历糟糕的网络，使用 A3-Mega 时性能要差 10-20%。

到 2025 年年中，GCP 将正式发布其最新的 A4 B200 和 A4X GB200 实例，在纸面上与 AWS、Azure、OCI 以及其他将提供每 GPU 400Gbit/s 的新兴 GPU 云具有竞争力。GCP 还将继续改进并推出新的软件功能，树立行业标准。我们将这称为「**设立标杆**」（setting the bar）阶段。

由于 A3-High 和 A3-Mega 拖沓的体验与性能，他们失去了大量客户对其产品的信心，重拾信心需要时间。我们相信，到 2025 年年中，GCP 将完成「追赶」，并很快在全行业抬升标杆、赢回客户信心。我们相信 Google 的 GPU 服务有望迈向 ClusterMAX™ 黄金或 ClusterMAX™ 白金级 GPU 云。

2025 年 1 月，我们主动联系 Google，向他们展示了我们的 NCCL 性能测试以及 GCP 客户向我们反馈的全部投诉与意见清单。GCP 团队对反馈相当虚心，正迅速着手解决。

他们承认的第一条反馈，是占其 GPU 机群主体的 A3-High 与 A3-Mega 网络性能不佳。他们正通过 a3-ultra 的推出解决这一问题——a3-ultra 配备行业标准的每节点 3200Gbit/s RDMA 带宽。至于其即将推出的 A4 B200 和 A4X GB200 服务，纸面速度将与业界其他 B200 和 GB200 服务具有竞争力。

A3-mega 实例此前还缺少 LL128 协议，这意味着其真实消息大小下的现实 NCCL 性能受损。2025 年 1 月，他们向所有客户发布了在 a3-mega 上启用 LL128 协议的修复。A3-ultra 则开箱即带 LL128 NCCL 协议，因此在其较新 SKU 上看到这些改进令人欣慰。A3-ultra 的性能仍略逊于 OCI 以太网和 Azure InfiniBand，但在端到端训练性能上，GCP 只比可比的 InfiniBand 参考方案低 1-2% 的 MFU。注意，GCP a3-ultra 的每个 rail 组规模仍只有 4 个节点，而在 OCI、Azure 和大多数新兴 GPU 云上是 32 个节点。这意味着集合通信需要更多跳数，带来更多拥塞和更慢的性能。我们将在 NCCL 深度解析文章中详细解释。至于 a3-mega，他们目前仍缺少 NVLSTree NCCL 算法。NVLSTree NCCL 算法利用 NVSwitch 中的 NVLS 功能做多节点加速，可获得更快的网络集合通信性能。他们正在实现该算法。而 a3-ultra 开箱即支持 NVLSTree、NVLS、RING、TREE 和 PAT 算法，很高兴看到 GCP 在其最新 SKU 上交付功能完备的产品。在我们即将发布的 NCCL/RCCL 深度解析文章中，我们将展示跨 GCP 实例的性能基准及其与其他方案的对比。

从与 GCP 客户的交流来看，所有客户都抱怨过配置所需的「激活能」：要正确设置 NCCL 环境变量、正确链接并调试 GCP 网络/tuner 插件使其正常工作，门槛太高。客户在调试 NCCL 环境变量上浪费昂贵的 GPU 时间，而在 Azure 和 OCI 上，NCCL 开箱即用。GCP 承认了这一反馈，正在研究如何让体验更顺畅。客户抱怨的第二件事，是 GCP 不会自动使用 [slurm topology.conf](https://slurm.schedmd.com/topology.html) 做 Slurm 拓扑感知调度，而是让用户在自己的 sbatch 脚本里手工完成拓扑排序。GCP 已正视这一反馈，并于今年实现修复。

![](https://substack-post-media.s3.amazonaws.com/public/images/2caad321-412c-4726-80cb-5f27fd72eb0d_1024x537.png)
*来源：GCP*

GCP 客户的第三条反馈，是他们目前没有完全托管的 Slurm 服务。GCP 承认了这一反馈，并正在积极调研。GCP 目前有 Cluster Toolkit，许多客户用它搭建集群，但它目前没有基于 GUI 的搭建选项，也不托管，更没有开箱即用的每周自动排期主动健康检查选项。尽管 Cluster Toolkit 相比 6 个月前的非托管 Slurm recipe 已是巨大进步，但仍缺少「托管」等诸多功能。

GCP 客户的第四条反馈（GCP 已承认）是：他们正在改善客户技术支持，为客户的整个生命周期及其工单（从创建到解决）指派一位负责工程师。目前，GCP 只会派一堆人上电话会，而客户想要的只是一位懂行的工程师从头到尾「负责」问题——从分诊、热修复到长期解决。「几十位产品经理和工程师」涌向客户电话会的问题并非 GCP 的 GPU 服务独有，而是 Google 全公司层面需要解决的问题。

请注意，Google 的大多数内部团队是在 TPU 上做 GenAI 训练与推理的；因此，GCP 的 GPU 体验与 Google 内部的 ML 基础设施体验并不相同。内部少数使用云 GPU 的 Google 团队之一是 DeepMind 旗下的 Isomorphic Labs。虽然 GCP 客户与 GCP 解决方案架构师团队之间有紧密的反馈闭环（他们自己也在用），但其「吃自家狗粮」（dogfooding）的程度远不及 AWS 这类以万物 dogfooding 闻名的公司。

与 OCI 或 CoreWeave 不同，GCP 的监控并非开箱即设置好；虽然可以用 [OpsAgent](https://cloud.google.com/ai-hypercomputer/docs/monitor) 相对简单地搭起监控仪表盘，但它远不及 CoreWeave 的监控 Grafana 仪表盘与指标那么先进。每一位客户都想监控 GPU；因此我们建议这应当开箱即设置。健康检查方面，GCP 确实在 VM 上运行被动健康检查，但没有开箱方案在空闲节点上运行每周排期的主动健康检查——不像 CoreWeave 和 Nebius。GCP 确实有 [cluster-health-scanner](https://github.com/GoogleCloudPlatform/cluster-health-scanner)，但它既非每周自动排期，也非开箱即用方案。我们建议 GCP 花些时间和金钱，亲自试用 CoreWeave SUNK 的服务，看看他们是如何做健康检查与监控的。

GCP 不只是一朵 GPU 云，还具备云的其他全部服务，如 Bigtable、数据库、对象存储和并行文件系统，可满足数据处理和网页抓取之需。作为一朵完整的云，它意味着你不需要把数据从完成数据处理的「主超大规模云」复制（或串流）到新兴 GPU 云集群——你的所有数据本来就在那里。

安全方面，[GCP 的安全](https://cloud.google.com/security/compliance/offerings#/countries=United_States)是一流水准，包括妥善实施的租户[网络隔离与传输中加密](https://cloud.google.com/docs/security/encryption-in-transit)。任何有严格安全要求的企业大概都应该选择超大规模云厂商。

## 其他青铜级供应商

另一些供应商落入 ClusterMAX™ 青铜层级，是因为没有非 beta 的开箱即用 Slurm 和/或 Kubernetes 服务，或者其 Slurm 和/或 Kubernetes 服务漏洞百出、配置不当。我们已向他们反馈，大多数供应商对反馈持开放态度，目前正在构建和推出开箱即用的 Slurm 和/或 Kubernetes 服务。该青铜层级中的一些供应商经营 GPU 云服务已有年头，但直到上个月才取得 SOC2 合规。尽管我们欣慰于他们取得 SOC2 合规，但目前还不能把他们排得更高，因为他们才刚刚拿到 SOC2。

值得一提的是，对其中一些供应商——例如 DataCrunch 的按需单节点服务——相当适合开发工作。我们评估了 DataCrunch 的按需单节点服务，体验相当不错。但遗憾的是，其生产集群不适合推理或训练。

![](https://substack-post-media.s3.amazonaws.com/public/images/51d2b8e4-4d15-4bc7-bcdf-9d5e57e0c9a6_1024x596.png)
*来源：Datacrunch*

TensorWave 也有 beta 版的托管 Slurm 与托管 Kubernetes 服务，正在开发被动与主动健康检查。我们相信，到下一次评估时，TensorWave 的服务有潜力达到 ClusterMAX™ 白银。

## ClusterMAX™ 表现不佳级 GPU 供应商

被归入 **表现不佳（UnderPerform）** 类别的 GPU 供应商，在多项重要评估指标上未能满足行业与安全的关键基本要求。该层级的供应商通常存在严重问题，包括安全实践不足、可靠性或在线率低下、营销信息不清晰或误导、技术知识或客户支持有限，以及编排能力欠缺。

大多数供应商落入该类别的原因是连 SOC2 或 ISO 27001 等基本安全认证都没有。其中一些供应商还因其底层 GPU 供应商同样不满足 SOC 2 合规而落入此类。

安全是许多 GPU 租用者一票否决的关键因素，因为他们把专有模型权重存放在 GPU 云上——这些权重的训练成本从数万到数千万美元不等，是大多数 GenAI 公司的核心知识产权。此外，训练和/或推理这些 ML 模型可能涉及专有信息、个人身份信息或其他相关用户数据。租用 GPU 的这些公司的客户，不希望因使用不安全的 GPU 云而导致数据泄露。在欧盟国家，赌注更高，因为依据 GDPR 法律，泄露用户数据会招致巨额罚款。这就像航空公司之于 FAA 认证——也许有人想搭乘没有 FAA 认证的航班，但大多数人不会。

该类别中的一些 GPU 供应商甚至告诉我们，他们因缺少 SOC2 而丢了潜在订单，目前正在取得 SOC2 合规的过程中。我们欢迎该类别的供应商取得 SOC2 合规。

该类别中的一些 GPU 供应商甚至在其公开网站上承认，可能存在安全与隐私隐患，GPU 服务器与互联网之间的流量可能被第三方网络设备大量记录。

![](https://substack-post-media.s3.amazonaws.com/public/images/bf758eb1-6ba6-4769-a6a9-dda697456b2a_1024x235.png)
*来源：SaladCloud*

一些 GPU 供应商（如 Massed Compute）落入 **表现不佳** 类别的原因，是对社区毫无益处：用一堆内容错误的 AI 生成 SEO 垃圾文章淹没互联网。这对 ML 社区有害，因为它给本已嘈杂的互联网添加了大量噪音，还会主动把人引入歧途。

例如，在 Google 上搜索「H100 vs A100 L2 Cache」，Massed Compute 那篇信息错误的 AI 生成垃圾文章排在第一。他们在主动传播误导性信息，这对一家 GPU 供应商来说是可怕的起点。

![](https://substack-post-media.s3.amazonaws.com/public/images/f48da40c-3e17-447b-b5a4-aa6611bbd382_1024x537.png)
*来源：Google Search*

点进链接，文章开头就说 H100 的 L2 缓存是 256MB——完全错误。我们建议 Massed Compute 停止用 AI 生成的垃圾内容轰炸互联网。

![](https://substack-post-media.s3.amazonaws.com/public/images/95d5a59e-af8a-4c6d-b48f-79d1e422b7e9_703x1024.jpeg)
*来源：Massed Compute*

该类别中的一些供应商还缺少正确的网络驱动与 GPU 驱动，导致 NCCL 性能更差。此外，该类别中的一些供应商存在潜在的已知安全问题，例如未能用 VLAN 和 pKeys 实现适当的租户隔离。

以上就是我们首个 ClusterMAX™ 评级系统更新的全部内容。请持续关注后续文章及更多 ClusterMAX™ 更新。

## 2024 年 AI 新兴 GPU 云 GPU 租赁价格趋势

尽管许多观察 GPU 价格走势的人把 AI 新兴 GPU 云的 H100 租赁价格描述为「崩盘」——我们一点也不意外——并将其视为 H100 供应改善带来的算力成本合理且合乎逻辑的下降。同样重要的是 B200 与 GB200 可得性的不断提高：我们已经看到定期租赁合同在陆续签订，这开始压低市场算力成本，进而压低 H100 的租赁价格。

在下一节中，我们将回顾 2024 年的 GPU 租赁价格趋势、2025 年的展望，以及如何分析 AI 新兴 GPU 云的总拥有成本与回报。我们还将讨论即将到来的 CoreWeave IPO，以及我们如何运用 SemiAnalysis AI 总拥有成本框架来分析 CoreWeave 的投资回报与单位经济模型。
