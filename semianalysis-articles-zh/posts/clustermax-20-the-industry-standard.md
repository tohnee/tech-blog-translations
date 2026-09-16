---
title: "ClusterMAX™ 2.0：行业标准的 GPU 云评级系统"
title_en: "ClusterMAX™ 2.0: The Industry Standard GPU Cloud Rating System"
subtitle: "按体量计 95% 覆盖率，84 家供应商获评级，209 家供应商被追踪，140+ 家客户接受调研，46,000 字供您享用"
date: 2025-11-06
source: https://newsletter.semianalysis.com/p/clustermax-20-the-industry-standard
crawled: 2026-09-15
authors: ["Jordan Nanos", "Daniel Nishball", "Michelle Shen", "Cheang Kang Wen", "Wei Zhou", "Jeremie Eliahou Ontiveros", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# ClusterMAX™ 2.0：行业标准的 GPU 云评级系统

> 原文：[ClusterMAX™ 2.0: The Industry Standard GPU Cloud Rating System](https://newsletter.semianalysis.com/p/clustermax-20-the-industry-standard) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**按体量计 95% 覆盖率，84 家供应商获评级，209 家供应商被追踪，140+ 家客户接受调研，46,000 字供您享用**

# 引言

GPU 云（自去年 10 月起也被称为「Neocloud」，即新兴 GPU 云）正处于 AI 热潮的中心。Neocloud 承载着 AI 领域一些最重要的交易，是终端用户租用 GPU 来训练模型、处理数据和构建推理端点的关键枢纽。

我们此前的研究已经树立了理解 Neocloud 的行业标准：

自 ClusterMAX 1.0 于 6 个月前发布以来，行业已发生重大变化。H200、B200、MI325X 和 MI355X GPU 已大规模到位。GB200 NVL72 已向超大规模客户批量交付，GB300 NVL72 系统正在陆续上线。TPU 和 Trainium 也已入场竞技。与此同时，许多买家正把 ClusterMAX 评级体系当作可信赖的独立第三方，以及一份理解这个市场的全面技术指南。

是时候出更新版了！

# 执行摘要

YouTube 视频摘要请见[这里](https://www.youtube.com/watch?v=cZp9eJCWXW0)！

- ClusterMAX 2.0 首发即带来对 84 家供应商的全面评测，较 ClusterMAX 1.0 的 26 家大幅增加。我们将市场观察范围扩展至共计 209 家供应商，高于上一篇文章的 169 家，也高于最早《AI Neocloud Playbook and Anatomy》中的 124 家。作为本次研究的一部分，我们访谈了超过 140 位 Neocloud 终端用户。
- 我们发布了测试中考虑的全部评测标准的逐项清单，涵盖 10 个主要类别（安全、生命周期、编排、存储、网络、可靠性、监控、定价、合作伙伴关系、可用性）。
- 我们发布了五份关于我们期望的说明，覆盖 SLURM、Kubernetes、独立单机、监控和健康检查。我们鼓励供应商在开发自身服务时参考这些清单。我们将这些清单视为对终端用户访谈内容的汇总，并在（供应商）开发服务的过程中持续追求品质。
- CoreWeave 保住头名位置，仍是白金（Platinum）级别中唯一的成员。CoreWeave 为其他厂商树立了标杆，也是我们在终端用户访谈中唯一一家能持续获得溢价定价的云。
- Nebius、Oracle 和 Azure 是黄金（Gold）级别中的顶尖供应商。Crusoe 和新入榜的 Fluidstack 也进入了黄金级别。
- Google 升至白银（Silver）级别榜首，与 AWS、together.ai 和 Lambda 并列。全球范围内还有更多云首次上榜即获得青铜（Bronze）或白银级别，共计 37 家云获得奖牌评级。
- 我们分析了以下关键趋势：Slurm-on-Kubernetes、虚拟机还是裸金属、用 Kubernetes 做训练、向 Blackwell 的过渡、GB200 NVL72 的可靠性与 SLA、加密货币矿工长留牌桌、定制存储方案、集群级网络、容器逃逸、安全预披露计划（embargo program）、渗透测试与审计
- 对于同时部署了 AMD 和 NVIDIA GPU 的供应商，其 AMD 云服务的质量远逊于其 NVIDIA 云服务。与 NVIDIA 相比，AMD 服务往往缺少关键功能，例如细粒度监控、带自动修复的健康检查，以及可正常使用的 SLURM 支持。
- 作为本文的配套，我们发布了 <https://www.clustermax.ai/>——一站式查看我们当前的评测标准、期望与结果，并将持续更新

在进入结果之前，我们先指出一点：自 3 月底发布 v1.0 以来，我们评级最高的几家 Neocloud 合计已确认近 $400Bn 的剩余履约义务（Remaining Performance Obligations，RPO）。这进一步印证了我们的评级体系在整个生态系统中都能很好地传导——从技术用户，到希望签约算力的关键决策者。

![](https://substack-post-media.s3.amazonaws.com/public/images/e19b49d3-ef75-4137-b024-caddfdcb412d_720x264.png)
*来源：SemiAnalysis Tokenomics 模型*

# 评级结果

ClusterMAX 2.0 首发带来更新后的排行榜：

![](https://substack-post-media.s3.amazonaws.com/public/images/c3e88b22-b4dd-46bf-b1d3-96e354e47e28_1738x873.png)
*ClusterMAX 2.0 排名，2025 年 11 月*

我们还发布了按类型划分的更新版市场追踪：

![](https://substack-post-media.s3.amazonaws.com/public/images/4a4defe4-d5db-4916-869d-cf635d58c218_2044x1390.png)
*ClusterMAX 2.0 市场全景，2025 年 11 月*

许多人在这项研究中做出了贡献。我们感谢各大领先 AI 实验室、硬件 OEM、投资人、初创公司、行业意见领袖等所有 ClusterMAX 的支持者。ClusterMAX 的影响力是巨大的。社区知名人士支持我们工作的完整评价名单，请见 <https://www.clustermax.ai/quotes>

发布 ClusterMAX 第一版时，我们收到了两条明确的反馈：

1. 只看结果表格的人想知道，某家云究竟为什么会获得某个评级。
2. 读完第一篇文章（估计 76 分钟读完、超过 20,000 字）的人，则想要关于我们体验的更多细节信息。

   1. 作为参照，《动物庄园》（Animal Farm）约 29,800 字，而讲述扎克伯格联合创立 Facebook 的电影《社交网络》（Social Network）的台词约 34,000 字
   2. 本篇 ClusterMAX 2.0 文章超过 46,000 字

在本文中，我们试图在有用的摘要信息与能准确描述我们体验的详细技术信息之间取得平衡。更多信息可随时致信 [clustermax@semianalysis.com](mailto:clustermax@semianalysis.com) 索取。

# 我们在招人 —— ClusterMAX

如果你喜欢这篇文章，并且对 Neocloud 有独特的技术视角，我们非常愿意与你合作。欢迎考虑加入我们，一起打造 ClusterMAX 2.1、ClusterMAX 3.0 及后续版本：

**主要职责**

- 主导下一代基准测试与 TCO 分析的开发，发布于未来版本的 **[ClusterMAX™](https://semianalysis.com/2025/03/26/the-gpu-cloud-clustermax-rating-system-how-to-rent-gpus/)** 及相关项目。
- 与来自 203+ 家 Neocloud、超大规模云厂商、算力市场平台和主权 AI 项目的高管与工程师协作
- 建立并维护与 NVIDIA、AMD、Intel 等 AI 芯片制造商、初创公司和 OEM 的合作关系
- 在与领先 AI 实验室、投资人、初创公司和社区成员既有关系的基础上，了解他们与云供应商合作的经验，并贡献专业见解
- 撰写详细的技术研究报告，分析基准测试结果、可靠性与易用性
- 通过参加 NeurIPS、MLSys、NVIDIA GTC、OCP、SC、HotChips 等重要会议紧跟新兴趋势与技术。鼓励出差，但非必需

**任职要求**

- 具有 PyTorch 或 JAX 等 ML 框架的使用经验
- 具有运行 Kubernetes 或 SLURM 的 GPU/TPU 集群使用经验
- 具有 Weka、VAST、Lustre、GPFS 等文件系统的使用经验
- 具有 InfiniBand、RoCEv2 等互连网络的使用经验
- 具有 ML 系统基准测试经验（GEMM、nccl-tests、vllm、sglang、mlperf、STAC、HPL、FIO、torchtitan、megatron 等）
- 有超大规模云厂商、Neocloud、服务器 OEM、芯片制造商或大规模使用这些技术的用户方工作经验者优先
- 积极主动，能够胜任全球化分布式团队协作

[查看职位描述](https://app.dover.com/apply/SemiAnalysis/c19093ad-b5f8-42b0-9b97-d960464f298c)

# 评级级别

依据 10 项关键标准（安全、生命周期、编排、存储、网络、可靠性、监控、定价、合作伙伴关系与可用性）完成评估后，我们会为某家 Neocloud 给出五种评级之一（白金 Platinum、黄金 Gold、白银 Silver、青铜 Bronze，或表现不佳 Underperforming）。

需要理解的是，这是一套相对评级体系。也就是说，每家 Neocloud 在这十项标准上的服务质量，都是相对于同行来评估的。把逐项标准全部勾选达标只是个开始；更关键的是，黄金和白金级别的 Neocloud 之所以能脱颖而出，靠的是推出别人没有、且客户认可的新功能与新特性。

**ClusterMAX™ 白金（Platinum）** 代表业内最优秀的 GPU 云供应商。该级别的供应商在所有评估标准上始终表现卓越。白金级供应商积极主动、勇于创新，并与用户社区保持活跃的反馈闭环，持续抬高行业标杆。在实践中，白金级供应商能够获得高于竞争对手的溢价定价，因为客户认识到其服务的 TCO 更优——即便直接对比时，其每 GPU 小时的裸价格（$ per GPU-hr）高于竞争对手。

**ClusterMAX™ 黄金（Gold）** 指在所有评估类别中表现强劲、但仍有改进空间的服务商。黄金级供应商在用户体验上可能存在小的缺口或不一致，但总体上对反馈响应及时、有持续改进的承诺。黄金级供应商是很好的选择，通常能赢得订单——尤其是当他们的每 GPU 小时价格最优、且集群能在客户期望的时间线上交付时。

**ClusterMAX™ 白银（Silver）** 是一项合格可用的 GPU 云服务，但与黄金或白金级供应商相比可能存在明显差距。由于这些差距，一些用户不会考虑白银级供应商的服务——无论其每 GPU 小时价格多么有吸引力、可用性多么好。总体而言，白银级 GPU 云仍有改进和成长空间，我们鼓励它们采纳行业最佳实践以追赶同行。

**ClusterMAX™ 青铜（Bronze）** 涵盖满足我们最低标准的所有 GPU 云供应商，也是我们在任何情况下都还愿意直接向他人推荐的最后一级。常见问题可能包括：支持服务不稳定、网络性能欠佳、SLA 不明确、与 Kubernetes 或 SLURM 等主流工具的集成有限、或定价缺乏竞争力。该级别的供应商需要在可靠性和客户体验上做出相当大的改进。该级别中的一些供应商已经在努力追赶，我们期待尽快再次对他们进行测试。

**不予推荐（Not Recommended）** 是我们的最后一个类别，名字本身就说明了一切。该级别的供应商在一项或多项标准上未达到我们的基本要求。需要注意的是，这是一个很宽泛的类别，因此在正文中我们会具体描述每家云究竟缺了什么。不予推荐名单又进一步细分为两类：

- **表现不佳（Underperforming）**——根据我们的实测，我们认为该级别的供应商只要修复一个或多个关键问题，就能迅速升至青铜甚至白银级别。关键失分的例子包括但不限于：没有现代 GPU 可供使用（例如只有 A100、MI250X 或 RTX 3090，因为我们期望至少要有 H100 可用）、未完成基础的安全认证（如 SOC 2 Type I/II 或 ISO 27001）、关键服务器功能配置失误（即没有禁用 ACS，或没有启用 GPUDirect RDMA），或存在侵害客户利益的商业行为，例如在集群还在搭建过程中、或服务器因硬件故障停机期间仍向用户收取 GPU 小时费用。
- **暂不可用（Unavailable）**——该级别的供应商拥有令我们感兴趣、令我们兴奋的服务，但由于尚未对公众开放或无法供我们测试，我们无从验证。例子包括：尚未正式上线服务的供应商（尽管其宣传材料会让你以为早已上线）、已完全售罄且没有新增产能计划的供应商、仅服务涉密政府客户的供应商，以及其他原因。我们对该级别中的许多供应商都感到兴奋，但在测试上坚持「信任但要验证」的原则，在完成实测之前将他们保留在此类别。

# 评级标准

为了更详细地说明我们如何在 10 项关键标准上比较各 Neocloud，下面列出 ClusterMAX 2.0 所用测试标准的逐项清单。值得注意的是，这份清单已于 8 月 6 日发送给所有与我们有工作关系的 GPU 云供应商。我们相信，随后许多云把集群交付推迟了数周，并匆忙创建或修改服务以满足我们的期望。举例来说，有的云供应商此前从未安装过 SLURM，却在向我们交付集群前一周才第一次尝试安装；有的第一次尝试在 Kubernetes 上启用支持 RDMA 的网络；还有更多供应商在我们发函告知后，才刚刚着手修补其服务中刚得知的关键安全漏洞。

我们欣赏这些努力，也认为抬高标杆对生态是好事，但我们对在集群交付过程中出现显著延误的云做了扣分处理。同时，借助这项工作中对 140+ 位云用户的访谈，我们尽力分辨「现状」与「未来状态」——换句话说，在我们测试的服务中，哪些是已公开、正式可用（GA）且被客户实际使用的，哪些还只是规划中、尚未上线。

我们开展这项研究，是为了帮用户简化一项评估：SLURM 集群、Kubernetes 集群或独立单机是否配置妥当、能否满足预期。我们听许多用户讲过「退还」集群的经历，甚至有人在与提供单机访问的某些算力市场打交道时玩起了「俄罗斯轮盘赌」。在这些场景中，GPU 驱动、GPU 服务器硬件、后端互连网络、共享存储挂载、互联网连接等方面的可靠性问题，都会让用户对供应商失去信任并流失。虽然我们无法在大时间尺度上测量可靠性，但会在约 5 天的测试中尽力评估。

有兴趣的读者可访问 ClusterMAX 网站 <https://www.clustermax.ai/criteria>，查看完整、动态且定期更新的逐项标准清单。我们欢迎 Neocloud 用户主动联系，提出希望纳入这份清单的标准。特别要感谢 GPU MODE 的 Mark Saroufim，他就 Nvidia Nsight Compute 提出了宝贵建议——让用户无需计算节点上的 sudo 权限即可对 GPU 内核做性能剖析。更多细节见：<https://clustermax.ai/monitoring#performance-monitoring>

8 月 6 日发出时，我们的逐项标准清单如下：

1. **安全（Security）**

- 是否已由第三方审计机构出具相关认证，证明公司流程符合基本标准？（SOC2 Type 1、ISO 27001 等）
- 是否针对全球客户具备更具体的合规资质（即能否面向全球销售服务）？
- 后端网络对多租户用户是否做了安全隔离（InfiniBand Pkeys、VLAN）
- 驱动与固件是否为最新版本？未来漏洞的通知与修补流程是怎样的？

2. **生命周期（Lifecycle）**

- 服务的接入与退出是否便捷？是否存在隐藏费用？
- 创建集群有多容易？
- 随时间推移扩容集群是否容易？
- 集群是否好用？（如下载速度、上传速度）
- 支持体验有多好？

3. **编排（Orchestration）**

- 集群是否以合理的默认配置完成部署？（OS 版本、sudo、ssh、git/vim/nano/python/docker 等基础软件包预装）
- 添加/移除用户、组和权限是否方便？
- 能否对集群的计算与存储资源实施 RBAC
- 是否集成外部 IAM 供应商实现 SSO
- SLURM 方面：modules、pyxis/enroot、hpcx/mpi、nvcc、nccl、topology.conf 已设置、dcgmi health -c、LBNL node healthcheck 或同等物、prolog/epilog、GPUDirect RDMA 全部正确配置
- Kubernetes 方面：kubeconfig 易于下载和使用、cni 已配置、支持任意 helm chart、GPUOperator 与 NetworkOperator 能方便地申请资源、默认提供 ReadWriteMany StorageClass、metallb 或外部 LoadBalancer、node-problem-detector（或同等物），全部正确配置
- 在 slurm 和 kubernetes 上均要求：nccl-tests 或 rccl-tests 跑满预期带宽，多节点 torchtitan 训练任务达到预期 MFU（k8s 训练通过 pytorchjob、jobset、volcano batch 或其他同等 CRD）
- 仅限 kubernetes：使用 llm-d 的多节点预填充-解码分离（P-D disagg）服务达到预期吞吐

4. **存储（Storage）**

- 提供 POSIX 兼容文件系统（如 Weka、VAST、DDN）
- 提供 S3 兼容对象存储（即 AWS S3、Azure Blob、GCS、R2、CAIOS、Scality 便于使用）
- slurm 上提供 /home 与 /data（或同等路径）挂载，k8s 上提供默认 RWM StorageClass
- 提供本地盘或分布式本地文件系统，用于 /lvol（或同等路径）缓存
- 存储可扩展且性能良好

5. **网络（Networking）**

- 提供 InfiniBand 或 RoCEv2
- 提供 MPI 实现（即默认 mpirun 即可使用 hpc-x）
- /etc/nccl.conf 中的默认 NCCL 配置合理
- nccl-tests 或 rccl-tests 或 stas all_reduce_benchmark.py 跑满带宽
- 多节点 torchtitan 训练任务达到预期 MFU
- 支持 SHARP，以提升大规模场景下的 nccl 性能
- 提供 NCCL 监控插件
- 提供 NCCL 慢节点（straggler）检测

6. **可靠性（Reliability）**

- 提供硬件正常运行时间 SLA 且合理（如计算节点 99.9%、机柜 99%）
- 提供 7x24 支持，15 分钟响应 SLA
- 互连网络无链路抖动（link flapping）
- 文件系统不会随机卸载
- WAN 连接长期稳定，上传/下载速度合理
- 完整的被动健康检查（Passive Health Checks）套件

  - https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/feature-overview.html#background-health-checks
  - 检测并排空（drain）：GPU 掉卡（fall off the bus）、PCIe 错误、IB 或 RoCEv2 事件/链路抖动、温度超限、GPU 或 CPU 内存 ECC 错误、XID 或 SXID、NCCL/RCCL 停滞
- 完整的主动健康检查（Active Health Checks）套件

  - 轻量测试套件在 prolog/epilog 中运行，或以每小时/每天的频率在低优先级分区的空闲节点上运行
  - 激进测试套件每周在空闲节点上运行
  - DCGM level 1、2、3 加 EUD、DtoH 与 HtoD 带宽、本地 NCCL 测试、本地 IB 测试、成对 GPU 与 CPU 的 ib_write_bw、ib_write_latency、GPUBurn 或 GPU Fryer、NVIDIA TinyMeg2、UberGEMM、多节点 megatron 或 torchtitan 任务结果与参考值一致

7. **监控（Monitoring）**

- 预装 Grafana 或同等仪表盘，可查看集群信息的高层与底层视图
- 便于配置自定义告警
- 集成 SLURM 的任务统计、资源使用与汇总（sacct）
- 集成 Kubernetes（kube-state-metrics、node-exporter、dcgm-exporter、cAdvisor）
- DCGM 信息可用

  - 通过 DCGM_FI_PROF_SM_ACTIVE 监控 SM Active
  - 通过 DCGM_FI_PROF_SM_OCCUPANCY 监控 SM Occupancy
  - 通过 DCGM_FI_PROF_PIPE_TENSOR_ACTIVE 估算 TFLOPs
  - 通过 DCGM_FI_DEV_PCIE_REPLAY_COUNTER 监控 PCIe AER 比率
  - 通过 DCGM_FI_DEV_ECC_SBE_VOL_TOTAL 获取 GPU 与 CPU 内存错误
  - 节点级健康状态：功耗、风扇转速、温度（CPU、内存、NIC、光模块等）
  - PCIe、NVLink 或 XGMI、InfiniBand/RoCEv2 吞吐
  - dmesg 日志（如 promtail）

8. **定价（Pricing）**

- 一般而言，在质量不变的前提下，每 GPU 小时价格越低对终端用户越好
- 消费模式（1 个月、3 个月、6 个月、1 年、2 年、3 年）
- 存储、计算节点、网络等分开计费或打包计费
- 既有合同的扩容与延期

9. **合作伙伴关系（Partnerships）**

- AMD 或 NVIDIA 投资
- NVIDIA NCP 认证
- NVIDIA exemplar cloud 性能认证
- AMD Cloud Alliance 成员身份
- 对安全更新信息的掌握（如关注 Wiz）
- SchedMD 合作伙伴关系（SLURM 的开发者）
- 参与行业活动、生态支持

10. **可用性（Availability）**

- GPU 总量与大规模集群运营经验
- 按需可用性、利用率、容量块（capacity blocks）
- 最新 GPU 型号可用（H100、H200、B200、MI300X、MI325X、MI355X）
- 未来 GPU 路线图（B300、GB200 NVL72、GB300 NVL72、VR、MI400 等）

自 2025 年 9 月 15 日测试窗口关闭以来，这份清单已经出现了许多显著改进。为了接纳评级体系的新成员，未来几周我们将接受任何希望冲上榜单、获得 ClusterMAX 奖牌身份的供应商。为此，我们将渐进式发布小版本（如 ClusterMAX 2.1），而无需重新测试所有供应商。

当行业出现重大变化时——例如 GB200、GB300、VR200 和 MI450X 等机柜级系统获得广泛市场采用——我们将进行大版本升级，即 ClusterMAX 3.0。我们预计大约每 6 个月一次。

## 示例测试

许多行业分析师和金融投机者认为 GPU 算力已经大宗商品化，只需按每 GPU 小时价格即可轻松比较。我们认为，价格只是买家在敲定一个集群、甚至一台虚拟机时考量的众多标准之一。

这些简单测试通常不到一分钟即可完成。我们把它们当作探针，用来揭示网络配置、存储性能、对等互联（peering）和虚拟化开销方面的潜在问题。一家在这些基础设置任务上失败的供应商，几乎必然无法胜任数周级的多节点训练任务。以下是一些能直接对比各 GPU 云的有用信息：

**安装 PyTorch 的耗时**（分别用 uv 和 pip）。这是 WAN 连接质量与小文件本地磁盘 I/O 的探针。使用现代的 uv 安装器时，我们观察到巨大分化。一流供应商（如 CoreWeave、GCP）约 3.2 秒完成安装；中位数约 8.5 秒，而一家青铜级供应商竟耗时 41.2 秒。用 pip 则普遍更慢，中位数约 28 秒，凸显了不采用现代工具链的代价。

**从 NGC 下载 pytorch 容器的耗时**。拉取 22.1GB 的标准 nvcr.io/nvidia/pytorch:24.05-py3 容器，是检验供应商对等互联与本地缓存策略的关键测试。维护本地 NGC 镜像的白金级供应商（如 CoreWeave）10 秒内即完成拉取；黄金级供应商（如 Nebius、Oracle）为 45-60 秒，尚可接受；白银级供应商常需 90-120 秒，而许多青铜级供应商超过 4 分钟，暴露出基础设施基本配置的缺失。

**运行「import torch」的耗时**。这衡量开发者的「冷启动」时间，包括驱动初始化与库加载。只要不是近乎瞬时完成，就是配置不当或虚拟化开销的信号。中位数为尚可忍受的约 1.8 秒，但我们发现多家供应商（尤其是 VM 配置复杂的那些）存在令人抓狂的 8-10 秒延迟。

**下载 15B Microsoft/phi-4 模型的耗时**。这是对从 Hugging Face CDN 持续下载的 WAN 吞吐的实测。中位耗时约 35 秒（约 3.4 Gbps）。顶级供应商稳定跑出 6 Gbps 以上的速度，约 20 秒完成；其他供应商则明显落后，加剧了研究人员在模型之间切换的摩擦。

**将 15B Microsoft/phi-4 模型加载进 GPU 显存的耗时**。这是对本地数据通路的纯测试：从磁盘（本地 NVMe 或共享文件系统）经 PCIe 到 GPU 显存。中位耗时约 12 秒。耗时更长与本地存储层级不佳直接相关，这个瓶颈在每次加载 checkpoint 时都会被感受到。

**机器地理位置与 IP 归属是否与供应商名称相符**。对机器公网 IP 做一次简单的 whois 查询。这项测试对揪出聚合商和转售商至关重要。在对小型供应商的多次测试中，IP 归属分别解析到了 Oracle、CoreWeave 或 AWS。这与部分供应商的宣传相悖，也让人对其定价与支持质量产生疑问。

**通用网络 speedtest**。speedtest-cli 虽是合成测试，但便于发现 WAN 饱和或流量整形。我们观察到下载中位数约 4.5 Gbps、上传约 2.8 Gbps。更有意思的是，一些供应商（如 STN）能跑出漂亮的对称 10 Gbps speedtest 成绩，但在真实文件下载（如 NGC、Hugging Face）上表现糟糕，说明其部署了流量管理来专门应付这类合成测试。

**互连带宽测试（「nccl-tests」或「rccl-tests」）**。使用开源仓库（以 mpi 构建，或使用 Stas Bekman 在 Machine Learning Open Book 中维护的 torch 启动脚本），我们在合成的 allreduce、allgather 和 alltoall 负载上测试互连网络，并与预期的 algbw 和 busbw 结果对比。这是验证网络配置正确、计算节点已启用 GPUDirect RDMA 的简单方法。在 SLURM 上，我们通过 salloc/mpirun、salloc/srun 或 sbatch/enroot/pyxis 运行该测试；在 Kubernetes 上，通过 MPIOperator 或 JobSet 运行。

**GEMM 基准**。使用自定义脚本，我们验证单块 GPU 的通用矩阵乘法是否达到预期性能（实际 TFLOPs）。这是验证 GPU 是否正常工作的简单方法。该测试直接在 python 脚本中运行。

**单节点 RL 任务**。使用 prime intellect 的 verifiers 库，我们运行 GRPO 训练脚本，训练一个 Qwen 模型去解谜题游戏 wordle，并与给定 GPU 上每个 rollout 的预期训练时长对比。这是验证 GPU 是否正常工作的简单方法。该测试直接在 python 脚本中运行。

**多节点预训练任务**。使用 torchtitan 库，我们运行多模态预训练脚本，在 C4 数据集上训练 Llama 模型，并与每步预期训练时长和 MFU 对比。这是验证 GPU 与互连网络是否达到预期表现的重要方法。在 SLURM 上通过 sbatch 运行，在 Kubernetes 上通过 PyTorchJob 或 JobSet 运行。

**多节点推理基准**。使用 llm-d，我们部署一个预填充-解码分离（prefill-decode disaggregated）的推理端点来服务 Qwen 模型。我们验证 vllm 性能套件上的推理吞吐符合预期，并验证当端点后面部署更多模型副本时性能随之提升。该测试仅在 Kubernetes 上运行。

直接对比供应商时，部分结果颇值得一看：

![](https://substack-post-media.s3.amazonaws.com/public/images/3bb72a24-f855-4287-91b2-521293452af4_4953x2313.png)
*来源：ClusterMAX 独立虚拟机测试*
![](https://substack-post-media.s3.amazonaws.com/public/images/ac891514-403e-473e-91d6-b3f81d9b9aa5_4953x2313.png)
*来源：ClusterMAX 独立虚拟机测试*
![](https://substack-post-media.s3.amazonaws.com/public/images/478e9e22-7b9d-4259-bc7c-0e50cb208fce_2678x1212.png)
*来源：ClusterMAX 独立虚拟机与 slurm 集群测试*

# 值得关注的趋势

有许多显著趋势正在改变 Neocloud 行业今天的运作方式，以及客户对供应商的期望。以下是对其中几个趋势的描述：

- Slurm-on-Kubernetes
- 虚拟机还是裸金属？
- 用 Kubernetes 做训练
- 向 Blackwell 过渡
- GB200 NVL72 的可靠性与 SLA
- 加密货币矿工长留牌桌
- 定制存储方案
- InfiniBand 安全
- 容器逃逸、安全预披露计划、渗透测试与审计

## Slurm-on-Kubernetes

目前有三种在 Kubernetes 上运行 Slurm 的方式：

- CoreWeave 的 SUNK
- Nebius 的 Soperator
- SchedMD 的 Slinky

这三种 Slurm-on-Kubernetes 方案之间存在重大差异。下文我们描述这些项目之间的关键区别，以及 Neocloud 生态中不同供应商和用户目前的使用方式。

CoreWeave 的 SUNK 最先上市，属于专有软件，并且至今仍是在同一底层集群上同时运行 slurm 与 Kubernetes 任务的唯一可行方案。例如：一个 slurm 训练任务的批处理队列，与一个 Kubernetes 上自动扩缩容的推理端点，共同竞争底层 GPU 资源。

其次是 Nebius 的 Soperator，它已[开源](https://github.com/nebius/soperator)，在偏好 slurm 的 Nebius 用户中得到了广泛采用。与 SUNK 不同，我们没有发现任何用户会通过 kubeconfig/kubectl 访问底层 Kubernetes 集群来调度 Kubernetes 上的工作负载。相反，Nebius 依靠自动扩缩容和节点生命周期来在 slurm 批处理队列与 kubernetes 推理集群之间调配 GPU（举个例子）。不过，底层集群的访问是开放的，一些客户确实会利用这一访问权限做集群生命周期管理、可观测性/日志、通过 kubectl 调试，有些人甚至会定制 Soperator 本身——配置用户与访问管理、VPN、自定义 prolog/epilog 脚本、CSI 驱动等。

目前，我们知道 Nebius 之外还有两家云供应商（即 Voltage Park 和 GCORE）依赖 Soperator 提供其 Slurm-on-Kubernetes（SonK）服务。

最后是 SchedMD 的 Slinky——slurm 的原创者、slurm 路线图的守门人、PR 的拒绝者、以及唯一的官方支持提供者：<https://github.com/slinkyproject>

目前，Slinky 拆分成了多个独立项目，最重要的是 [slurm-operator](https://github.com/SlinkyProject/slurm-operator)——一组自定义控制器与 CRD，能够把核心 slurm 服务跑在 Kubernetes 集群上，而不是直接跑在裸金属或虚拟机上。这些 slurm 服务包括：

- slurmctld——slurm 控制器，管理哪些任务在集群中的哪些 slurm 工作节点上运行，以及这些工作节点的健康状态。在 kubernetes 上，这是
  slurmd——slurm 工作节点本身
- slurmrestd——为 slurmctld 提供 API 端点
- slurmdbd——用于存储任务统计（即谁运行了什么）的数据库

![](https://substack-post-media.s3.amazonaws.com/public/images/ca3efb4c-f405-475a-b0df-315e4e7b2e62_600x600.png)
*来源：《飞出个未来》（Futurama）*

为此，slinky 引入了一个新进程 slurm-operator，用于管理集群上的 slurm 资源。Slinky 还引入了一个独立的登录 pod，以 CRD「LoginSet」的形式管理，运行用户对 slurm 集群执行命令所需的 sshd、sackd 和 sssd 进程——这些命令包括 srun、sbatch、salloc、scontrol、squeue、sinfo、sacct 和 sacctmgr。

![](https://substack-post-media.s3.amazonaws.com/public/images/69c852fc-10cf-4b46-a5ae-bff7ccf8ecb8_791x631.png)
*来源：https://github.com/SlinkyProject/slurm-operator*

开箱即用的 Slinky 默认状态是不可用的。不幸的是，这成了那些出于各种原因想在 kubernetes 上跑 slurm、却又缺乏 slurm 经验（除了 sinfo 命令之外什么都没测过）的云供应商的巨大陷阱（footgun）。默认的 Slinky LoginSet pod 缺少 vim、nano、git、python、sudo 权限等。结果是：有五家不同的云供应商给我们开通了 slurm 集群登录权限，我们运行 sinfo，然后……就什么也做不了了。没有 git 怎么下载代码库？没有 vim/nano 怎么编辑文件？没有 python 怎么运行脚本？没有运行 apt 的权限怎么安装软件？

在这些环境中，节点之间的 SSH 访问通常也不存在。讲清楚 Slinky，基本上就是讲解 SUNK 和 Soperator 的最佳起点。那我们就开讲吧。

Soperator 最初于 2024 年 10 月随 [第三季度财报](https://nebius.com/newsroom/nebius-group-n-v-announces-third-quarter-2024-financial-results) 公布，并配有[介绍博客](https://nebius.com/blog/posts/introducing-soperator)和[说明文章](https://nebius.com/blog/posts/soperator-in-open-source-explained)，但托管版 Soperator 直到 [2025 年 6 月](https://nebius.com/blog/posts/introducing-managed-soperator)才发布。

从架构上讲，Soperator 与 Slinky 类似，都是跑在 Kubernetes 之上，而非与之并列。在 Nebius 的实现中，用户被分配的是运行在一个内部 kubernetes 集群上的、基于 qemu 的虚拟机，Soperator 在其中管理 Slurm 环境。实际上，在 Nebius 这里是「Kubernetes 上的虚拟机上的 Kubernetes 上的 Slurm」（Slurm-on-Kubernetes-on-VMs-on-Kubernetes）。不过最后一层并非必需，任何虚拟机或裸金属 kubernetes 集群都可以。只要存储配置正确，Soperator 在其他 kubernetes 集群上也运行良好。

从技术上讲，Soperator 是一个 Kubernetes Operator，自动完成相关 slurm 服务的部署与生命周期管理。整个集群通过 SlurmCluster 自定义资源定义（CRD）以声明式方式定义：

1. 为 Slurm 控制平面（slurmctld、slurmdbd）开通（provision）KubeVirt VirtualMachine 资源。
2. 生成必要的配置文件（如 slurm.conf）并分发到各虚拟机。
3. 以 SlurmNodeSet 资源管理计算分区，后者进而创建并管理 slurmd 工作节点所在的虚拟机池。
4. 对性能至关重要的是，它编排将 NVIDIA GPU 和 InfiniBand/RoCEv2 NIC 等硬件直通（passthrough）给虚拟机，使任务可获得裸金属级性能。
5. 它还负责弹性伸缩：用户只需修改 CRD 中的 replicas 字段即可扩缩分区，Soperator 会通过创建或删除底层虚拟机来完成调谐（reconcile）。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/e1d95061-ebe5-4c69-8a90-6e265e2242db_936x736.png)
*来源：项目仓库中的 Soperator 架构图：https://github.com/nebius/soperator*

然而，与 SUNK 或 slurm-bridge 不同，Soperator 并不提供混合调度器来让相互竞争的 slurm 与 kubernetes 任务共置并仲裁。

最后，要详细讲清 SUNK，关键在于关注 CoreWeave 在元数据管理以及与 CKS 集成上的差异。SUNK 内置了一个 slurm syncer pod，在 slurm 服务与 Kubernetes 调度器之间同步元数据。这一点在 slurm epilog 运行时体现得很明显：它发现节点健康故障，向 slurm 控制器抛出错误，将节点置为「drain」（排空）状态。集成并不止于 slurm 层，它还通过自定义调度器与 kubernetes 集成。一个 slurm 任务实际上会为特定 pod 创建带有自定义调度器逻辑的 kubernetes 资源：先设置一个哑调度（dummy schedule），让 slurm 完成真正的调度，然后把该 pod 接到 slurm 控制器上。这意味着用户可以在集群上同时运行 kubernetes 和 slurm 任务，但一切都由 slurm 实际调度。结果是 slurm 控制器对集群上运行的所有工作负载都了如指掌。

![视频通话截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/14c6b951-6c41-4b46-be45-7cb7f028dcd3_418x287.png)
*来源：CoreWeave。参考文档见此*

此外，Slinky 和 Soperator 的 LoginSet 默认行为也有许多不尽如人意之处。在 SUNK 中，登录 pod 控制器流程包含与 LDAP/IAM 系统的对接以管理用户，并自动将用户负载均衡到一个按需启动的交互式临时 ssh pod 上，该 pod 挂载标准共享文件系统作为用户的 /home 目录。访问该 pod 可以通过 ssh，也可以通过 tailscale operator，这意味着集群不需要为每个登录 pod 分配公网 IP。而在 Slinky 中，负载均衡是基于 IP 的三层（layer 3）轮询，如果用户安装了某些软件后与集群断连，就可能遇到不一致的问题。

总体来看，许多供应商显然希望兼得两者：用 kubernetes 做硬件生命周期管理与可靠性保障，同时保留 slurm 为批处理调度提供的易用性和熟悉感。我们预计 Slurm-on-Kubernetes 将持续成为供应商的一个有吸引力的选择。

## 虚拟机还是裸金属？

这场经典争论正在演进。CoreWeave 和 Oracle 等供应商力挺裸金属以获得最大性能。但这种做法需要把网络、存储和安全功能卸载到 DPU（如 Nvidia BlueField）上，复刻 AWS 借 Nitro 系统推广开来的超大规模云模式。

与此同时，Nebius（kubevirt）和 Crusoe（cloud-hypervisor）等供应商则采用轻量级虚拟机。其主张是这能带来显著的运营收益，例如快速开通（秒级 vs 分钟/小时级）、有状态快照、共享存储和更干净的安全隔离。就 Nebius 而言，他们已经达到了裸金属级性能——我们的测试、行业基准以及与其用户的直接交流都证实了这一点。而 Crusoe 的这一性能水平仍在持续打磨中。

总的来说，如今的选择与其说关乎性能，不如说关乎供应商的架构哲学。值得注意的是，即使在业内顶级供应商之间，裸金属、虚拟机（cloud-hypervisor）与 Kubernetes 上的虚拟机（kubevirt）孰为基础设施生命周期的最佳方案，也尚无定论。

## 用 Kubernetes 做训练

即便没有 Slinky、Soperator 或 SUNK，在 Kubernetes 上跑训练任务依然有别的办法。

具体而言，Kubeflow（MPIOperator、PyTorchJob、TrainingOperator）、Jobset、Kueue、Volcano、Trainy、dstack 和 SkyPilot 等工具/CRD 都提供了在 kubernetes 集群上调度训练任务、处理批处理队列的方法。

了解每个工具的用途和出处会很有帮助：

- **Kueue** – CRD – 管理任务队列与用户配额。与 kubernetes 默认调度器配合工作。帮助团队共享底层集群资源（即谁分到哪些 GPU）。
- **Volcano** – 自定义调度器 – 提供 gang 调度、任务依赖等 kubernetes 默认调度器所缺失的高级特性。可与 Kueue 配合使用。
- **PyTorchJob** – Operator/CRD – pytorch 任务的生命周期管理。来自 KubeFlow 社区。
- **MPIOperator** – Operator/CRD – 管理 MPI 任务的生命周期。来自 KubeFlow 社区。
- **KubeFlow Training** – 平台 – 多个不同训练 operator 的集合，不止 MPI 和 PyTorch。
- **Jobset** – CRD – 面向 gang 调度任务的通用资源定义，是对 Kubernetes batch API 的改进。由 Google 贡献给 kubernetes 社区，采用率快速增长。可与 Volcano 和 Kueue 配合使用。
- **Trainy** – 平台 – 简化向 kubernetes 提交任务的流程，减轻用户与 yaml 打交道的负担。付费产品。
- **dstack** - 平台 - 简化向 kubernetes 提交任务的流程，减轻用户与 yaml 打交道的负担。开源，另提供企业版选项（支持、SSO）。
- **SkyPilot** – 平台 – 简化向 kubernetes 提交任务的流程，减轻用户与 yaml 打交道的负担。开源，采用率快速增长。

我们预计市场将向少数几种方案收敛：偏好开源（OSS）的用 Jobset + Kueue，需要带 gang 调度的大规模批处理队列的用 Volcano，多云场景下的用 SkyPilot。

## 向 Blackwell 过渡

过去一年我们目睹了 H100 价格的陡降，以及许多组织在转向 Blackwell 上的犹豫。我们相信性能提升迟早会到来，尤其是对使用 FP8 和 FP4（MXFP4 或 NVFP4 数据类型）的用户，尤其是推理场景。测试期间，我们从不同供应商处收到了 H100、H200 和 B200 混合配置的节点。

就排名而言，目前我们主要考量 Hopper 的性能——在与终端用户的交流中，H100 和 H200 仍是我们听到的最热门集群（以采购数量计，而非总规模）。

## GB200 NVL72 的可靠性与 SLA

在 Hopper 时代，故障域是节点。而在 GB200 NVL72 这类 Blackwell 机柜级系统中，整个机柜——包括计算、NVLink 交换机、线缆盒/背板以及多张网络（横向扩展 scale-out、纵向扩展 scale-up）——构成故障域。这一根本性转变使可靠性与服务等级协议（SLA）成为客户与供应商价格谈判中的关键一环。

正如我们在 8 月的 GB200 NVL72 文章中所述，单个组件故障就可能需要排空（drain）整个 72-GPU 机柜。需要说明的是，这不是字面意义上把机柜冷却回路里的液体排掉，而是指 slurm 概念中节点状态 = "drain"，或 kubernetes 节点健康状态 = "drain" 且节点被「cordoned」（隔离）。作为应对，顶级供应商正在超越节点级正常运行时间，推出机柜级 SLA。我们看到 CoreWeave 和 Oracle 等头部供应商开始提供 99% 的机柜级正常运行时间保证，并附带相应的违约赔偿——即便是在替客户管理热备（hot spare）的情况下。

我们认为，要在 GB200 NVL72 机柜级系统上达到这一正常运行时间水平，唯有大规模投入：主动式自动化健康检查（主动与被动兼备）、能在故障打断任务之前检测并修复的精细化监控、面向大规模部署热备的自动化开通流程，以及从技术员到 SRE 再到终端用户的全员垂直整合投入。

这一点在 GCP 和 AWS 身上尤为突出——他们选择了 NVL36x2 而非完整的 NVL72，不过目前所有大规模部署 GB200 NVL72 的供应商那里，我们也听到了背板/线缆盒的问题。Nvidia 的说法是，问题根源是一个固件 bug，会导致 NVLink 连接随时间推移失步（lose sync），而非硬件故障。于是，在最早于 2024 年 11 月就开始出货 ES/PS 系统、并于今年春天开始批量出货之后，Nvidia 终于在本月发布那个大名鼎鼎的固件版本 1.3，让系统得以稳定使用。说清楚点：这比 NVL36x2 系统出货晚了 6-7 个月。这也影响到 Meta 的许多机柜——他们选择了 Ariel NVL36x2（72 CPU + 72 GPU），正如我们在《GB200 Hardware Architecture - Component Supply Chain and BOM》一文中所述。

如下图所示，NVL36x2 机柜的间歇性 NVLink 可靠性问题出在跨机柜 ACC 线缆上——这些线缆把两个 NVL36 机柜连接起来，组成一个逻辑上的 NVL72。由于长度更长，这些 ACC 线缆和飞越（flyover）线缆都存在恼人的信号完整性问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/3ddfa740-1a05-45c5-a222-2cf1e2901c67_2336x1480.png)
*Meta 用 168 根粗壮的 ACC 线缆将两个 NVL36 机柜连成一个 NVL72（来自 Meta 在 HotChips 2025 上的 Catalina 演讲）*
![](https://substack-post-media.s3.amazonaws.com/public/images/b96672f5-dcf5-43c5-b647-e279c9c842d5_3386x1814.png)
*AWS 宣传其 P6e-GB200 = NVL36*2 = NVL72 服务器（来自 AWS 的 YouTube）*

本次固件更新将修复的问题之一，正是那个导致 NVLink 连接随时间失步的固件 bug。我们认为这些系统中的硬件问题仍在持续，包括完全失效、瞬态中断，以及从固件到驱动再到软件库的软件栈不稳定——必须升级到最新版本才能获得可接受的终端用户体验。许多 NVL36x2 和 NVL72 的终端用户与超大规模运营方，仍在抱怨背板、跨机柜 ACC 线缆以及附加 flyover 线缆的可靠性。

供应商们描述的运营 GB200 NVL72 机柜级系统最艰难之处，并不在于故障总量、部件质量观感，甚至不是软件栈的稳定性，而是爆炸半径（blast radius）与恢复时间。下面我们描述在背板/线缆盒故障时从头重新开通一台 GB200 NVL72 机柜的流程，前提是修复的前置条件已满足（即机柜已在集群层面 drain/cordon，机上没有任务、或只有可抢占任务在跑）：

1. 机械验证。假设 NVLink 背板/线缆盒（实际上是机柜的「脊柱」）已被更换，或者这是一台首次开机的新机柜，需确保所有计算/交换托盘插入背板的盲插连接器严格对准。
2. 电力验证。给机柜内的 PDU 上电，但让计算托盘保持待机状态（POST），先把注意力放在 NVLink fabric 上。
3. 带外管理连通性。全部 18 个计算托盘和 9 个 NVLink 交换托盘上所有 BMC 的 MAC 地址须被集群管理器（如 NVIDIA Base Command Manager、Canonical MaaS）识别并可访问。为这些 BMC 分配 IP。
4. 应用固件基线。若带 Grace CPU 的计算托盘、NVLink 交换机、CX-7 或 CX-8 后端 NIC 与 BlueField-3 前端 NIC 之间存在版本不匹配，就会出问题。必须将带有正确固件包的黄金镜像同时应用到机柜的所有组件上。注意，NVLink 交换机固件与后续 OS 层驱动版本之间存在严格的兼容性要求，必须遵守。
5. 启动 NVLink 交换托盘。在计算托盘加载 OS 之前，必须先把 NVLink 交换托盘启动到最小 OS/固件栈，然后运行机柜级诊断。换言之，全部 72 块 Blackwell GPU 都要能跨越新背板/线缆盒/「脊柱」互相看见。如果重新插拔或更换部件无法解决问题，排障流程就从头再来（别想跳步收过路费，直接带着新背板回到机械验证）。
6. 校准 NVLink fabric。Fabric 训练（training）是指强制 NVLink 接口的 SerDes 相对铜背板做训练，调整其电气信号参数以建立稳定连接。这一步验证所有链路都运行在全速。如果有链路训练失败或以低速协商，你猜怎么办：重新插拔、逐个换件，确定到底是哪个部件出了故障（计算托盘、NVSwitch 托盘、铜背板、连接器/转接板）。搞不好，就换新背板从头再来。
7. 部署操作系统。通常目标 OS 会同时部署到所有节点，并附上与新固件基线匹配的 GPU 驱动、MOFED/DOCA 驱动、CUDA Toolkit、DCGM 和 Fabric Manager 的组合。
8. 启动 Fabric Manager。所有计算托盘都必须运行起来，才能验证这 72 块 GPU 在 OS 层面仍能通过 NVLink 互相看见。
9. 与横向扩展网络集成。横向扩展 fabric（区别于纵向扩展的 NVLink fabric）是 InfiniBand 或 RoCE。对于 InfiniBand，UFM 必须发现新的 GUID、分配 LID 并重新计算 fabric 路由路径。对于 RoCE（Spectrum-X），用 LLDP 识别新节点的拓扑位置，集群管理器（BCM）自动分配 IP。节点用 BGP 向 fabric 通告自己的路由，更新所有交换机的转发表。前端/南北向（N-S）上联网络也应用类似流程。
10. 考机（Burn-in）验证。对机柜内所有节点运行供应商的标准主动健康检查套件，执行 dcgmi diag -r 3、nccl-tests、多节点 ubergemm 以及一个抽样多节点训练任务等测试，确保 CPU、GPU、纵向扩展与横向扩展接口同时经历热胀冷缩。

我们详述这一流程，是为了解释为什么供应商认为，为一块新背板或一台全新 NVL72 机柜做开通，可能需要 9 小时到数天不等。如果读者中有人试过在自己的游戏 PC 或工作站上装 Nvidia 驱动，不妨想象同时给 18 台 PC 和 9 台工作站装驱动——而且你还要给它们全部重装新 OS，与此同时你家孩子在车库里随手乱掰断路器，微波炉上的时钟还必须和炉灶上的完全同步。

无论如何，这里一个关键问题是准确诊断故障。经验丰富的 NVL72 运营者当然不想在不必要的时候花时间去更换昂贵部件，尤其当这段时间可能构成一整天的机柜停机、计入其对客户的正常运行时间 SLA 时。业界已经出现了各种技巧来定位并识别具体发生的故障。大致归纳如下：

- 如果只有单条链路故障：是托盘连接器上的某个特定引脚，或背板上的某条走线
- 如果一块 GPU 上的所有链路都故障：是该 GPU 的 SerDes，或它到托盘连接器的局部布线
- 如果一个托盘（4 块 GPU）上的所有链路都故障：是该托盘或该槽位的电路板故障
- 如果出现大范围、随机的故障：是背板

对于机柜的首次故障，还应考虑对托盘做 A/B 对调，以精确定位故障是跟着托盘走还是留在槽位上。要在生产环境中做到这一点，我们强调供应商侧高质量监控仪表盘、主动/被动健康检查与自动修复的重要性，并在整个 ClusterMAX 研究中大力推广。

Nvidia 如何在工具层面支持客户也尚不明朗。我们听到不同供应商描述不同的故障场景，而这些似乎目前都在用「打地鼠」的方式解决。换句话说，Nvidia 是在临时拼凑用于调试和修复故障的工具与方法。这就留给供应商在运营流程和软件系统上做差异化的空间。看来，供应商把一款新调试工具接入其自动化栈的速度，可能就是决定性差距。

这一切最终落脚为供应商对客户的 SLA 承诺。此外，我们还看到应用于这些机柜级系统的 SLA 五花八门，涉及各种正常运行时间保证和违约赔偿。我们见过的方案差异之大令人瞩目：

1. 供应商同时承诺节点级 SLA 和机柜级 SLA。也就是说，单个节点必须有 99% 的正常运行时间，而机柜（定义为 18 个节点中的 16 个，或 72 块 GPU 中的 64 块）的 SLA 较低，为 95%。客户可使用机柜中的所有节点。
2. 供应商只承诺节点级 SLA。也就是说，单个节点有 99% 的正常运行时间保证，但客户只能使用机柜 18 个节点中的 16 个。余下节点由供应商另作他用（包括作为客户的热备、跑其他客户的工作负载、或跑内部工作负载）
3. 供应商只承诺机柜级 SLA。也就是说，18 个节点全部都必须保持 95% 的在线时间，客户可使用所有节点。

赔偿额度或抵扣的运作方式也各不相同。一旦违约，有的供应商坚持只提供未来账单的抵扣额度，供客户日后消费使用；另一些供应商则实时对账，直接把停机时间从当月账单中扣除。

目前，我们对各种 SLA 方案没有强烈偏好，也不打算给供应商或客户提建议。不过，在经历了 Hopper 一代的部署之后，我们希望这一轮互相起诉的人能少一些。敌意更少 = 对所有人都更好。

记住喽各位，CoreWeave 可是在 8 月就宣称 GB300「[可用于生产环境（production ready）](https://www.coreweave.com/blog/coreweaves-nvidia-gb300-nvl72-production-ready-instances-for-enterprise-ai-featuring-nvidia-blackwell-ultra-gpus-deliver-more-than-6x-performance-gain-on-deepseek-r1)」的！

## 加密货币矿工长留牌桌

加密货币矿工的「AI 转型」是真实存在的，其主要驱动力是他们相比纯 AI Neocloud 的先发优势。矿工们长期以来做的就是寻找廉价、大规模电力资源的生意。随着生成式 AI 腾飞并[改变传统数据中心的需求](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical)，许多比特币矿企意识到自己坐拥金矿。我们得出了[同样的结论](https://www.fabricatedknowledge.com/p/crypto-datacenters-nav)，并在 2025 年交易雪崩、股价飙升之前[给出了对行业的看多观点](https://youtu.be/-H4GakGDBy8?si=8W3pA8HLPIWq3TKL)。

虽然行业主角们[大多已成功建成 AI 数据中心并出租给各 Neocloud，但一些公司意识到，通过垂直整合可以提高每 MW 的实际价值](https://www.semianalysis.com/p/datacenter-model)。如今，按算力排名的许多头部比特币矿企都已拥有专门的 AI Cloud 业务。这份名单包括但不限于以下美国上市公司：Terawulf、Cipher Mining、IREN/Iris Energy、Hut 8/Highrise、VCV Digital/Atlas Cloud、BitDeer、Applied Digital，以及 Core Scientific（已被 CoreWeave 收购）。完整的 GPU 买方名单（含估算的季度 GPU 数量）[请参考我们业界领先的 AI Accelerator & HBM 模型](https://semianalysis.com/accelerator-industry-model/)。

表面上看，加密矿工尚未在 ClusterMAX 的白金或黄金级别形成竞争力。但了解 Neocloud 历史的人会注意到：Crusoe 正是从比特币挖矿起家的；Fluidstack 则已与 Terawulf 和 Cipher Mining 合作（背后有 Google 支持），为领先 AI 实验室交付黄金级集群。我们认为，这种聚焦基础设施底座的加密商业模式，对这些公司而言有两条可能的路径：

1. **供电外壳 / 托管（Colocation）：** 把他们吉瓦级、高密度的数据中心空间出租给其他 Neocloud 或前沿 AI 实验室——后者更愿意自行部署硬件——而且如有需要，可以实际把对方挡在自己的设施之外。
2. **批发式裸金属：** 自行采购 GPU 并以裸金属集群形式对外提供，利用其低能源成本在价格上激进竞争，让团队有事可做，并利用其融资渠道先于需求批量采购 GPU，从而获得定价套利机会。

没有哪家公司比 IREN 更能诠释「比特币转 AI」的转型。它在得克萨斯州 Childress 运营着全球最大的矿场之一，见下图。

![](https://substack-post-media.s3.amazonaws.com/public/images/45ab672e-37bc-4063-b0ab-761257b4240a_1428x953.png)
*来源：SemiAnalysis AI 数据中心模型*

IREN 已成功转型为批发式裸金属云，拿下与 Microsoft 的 200MW 交易，将在同一座得州 Childress 园区部署 GB300 GPU。IREN 已经公布了将整座比特币矿场改造成巨型 GPU 集群的愿景。

尽管他们在销售 GPU 云容量方面非常成功，但其经济回报并不像市场参与者通常描绘的那样。[我们的 AI Cloud TCO 模型](https://semianalysis.com/ai-cloud-tco-model/)（受全球最大 GPU 买方与金融领袖信赖）估算 IREN/Microsoft 交易的精确经济账，用户可用它与其他大型交易（如 Nscale、CoreWeave、Nebius、Oracle 等）比较。我们的 [AI Tokenomics 模型](https://semianalysis.com/tokenomics-model/)在此工作基础上进一步扩展，追踪算力供给的流动，以及各类需求如何流向最终使用这些算力的各个「token 工厂」。OpenAI 和 Anthropic 等 AI 实验室作为大部分算力容量的最终用户，在其中格外显眼！

![](https://substack-post-media.s3.amazonaws.com/public/images/438e3499-d154-485e-acf5-4baa9e5ec765_936x494.png)
*来源：IREN 新闻稿*

## 定制存储方案

海量数据集的崛起制造了存储瓶颈。高性能 POSIX 文件系统（Weka、VAST、DDN）虽然仍属主流，但一个新趋势正在出现：S3 兼容对象存储（如 CoreWeave 的 CAIOS 或 Nebius 的 Enhanced Throughput 对象存储），有时会搭配超大规模的分布式本地 NVMe 缓存。CoreWeave 的 LOTA（Local Object Transfer Accelerator）是最佳范例，可将数据透明地缓存在计算节点的本地盘上。

在我们的分析中，最初为以文本和代码为主的 LLM 训练而建设的算力，把存储当作次要问题，存储占集群 TCO 的比例不足 5%。然而，随着图像与视频生成、气象预测、药物发现、实时语音、机器人和世界模型等数据密集型负载的兴起，我们已经看到一些具体集群设计中存储占到集群 TCO 的 20% 以上（例如不到 2000 块 GPU 就配了超过 100 PB 存储）。

我们预计将有更多供应商需要应对「惊群」（thundering herd）问题——即那些在 100PB+ 规模下提供巨大聚合带宽的共享文件系统所面临的难题。

## InfiniBand 安全

谈到多租户云的安全，最关键的因素之一就是后端互连网络。它是 GPU 节点之间所有「东西向」流量的数据平面，对大型云而言，通常涉及共享的三层（three-tier）网络架构。实际上，供应商需要能够为每个租户（很多情况下还要为每个租户内部的子租户）创建延伸到私有后端互连的隔离「VPC」。

虽然多租户网络安全早已通过二层 VLAN 或三层 VXLAN、配合数据中心交换机与网络管理软件（如 Arista CloudVision/EOS、Cisco NDFC/NX-OS、Juniper Apstra/Junos）建立起来，但在 InfiniBand 上做这件事还比较新。Nvidia 最近发布了一篇[相关博客](https://developer.nvidia.com/blog/infiniband-multilayered-security-protects-data-centers-and-ai-workloads/)，强调为客户交付安全的多租户 InfiniBand 网络，远不止配置 PKeys 那么简单。

具体来说，分区键（Partition Keys，PKeys）是 InfiniBand 标准的网络分段机制，功能上等同于以太网世界的 VLAN。PKey 是分配给 InfiniBand 端口（HCA 和交换机两侧都有）的 16 位值。一个数据包要想被送达，其头部的 PKey 必须与接收端口分区表中的有效条目匹配，从而在 fabric 层面强制隔离。在许多不同的供应商那里，我们拿到过号称「隔离」的 4 节点或 2 节点集群，却能看到远多于我们自己那 16 或 32 个端点的设备——原因是 PKeys 配置错误，或压根没有任何配置。

然而，仅靠 PKeys 不足以构成健壮多租户环境的安全边界。PKeys 由中央子网管理器（Subnet Manager，SM）管理。一个被攻陷的租户节点有可能发送恶意子网管理数据包（SMP）来刺探 fabric 拓扑，在安全薄弱的 fabric 中甚至可以尝试重配 PKeys、破坏租户隔离。

真正的硬件级强制隔离，Nvidia 在这篇博客中有详细描述：<https://docs.nvidia.com/networking/display/nvidiamlnxgwusermanualfornvidiaskywayappliancev822302lts/configuring+partition+keys+(pkeys)>，我们建议所有部署 InfiniBand 的供应商仔细研读。

该博客描述了 InfiniBand 安全的多层方案。其成果是一次性设置，包括：

- **M_Key：** 管理密钥，防止不守法主机篡改设备配置。密钥不匹配时，请求将被丢弃。
- **P_Key：** 分区密钥，类似 VLAN。这类密钥定义了哪些设备可以互相「看见」或通信，在整个 fabric 上实现严格的流量隔离。
- **SA_Key：** 用于子网管理器（Subnet Administrator）中的敏感操作（例如增删记录）
- **VS_Key：** 用于 ibdiagnet 等厂商工具
- **C_Key 与 N2N_Key：** 保护通信管理器流量与节点间消息
- **AM_Key（仅在启用 SHARP 时）：** 专用于 SHARP 聚合，确保数据只被授权交换机归约

只依赖基础 PKey 配置而不加这些额外层的供应商，其安全姿态明显更弱。我们认为，InfiniBand 相关的额外复杂性——主要归咎于 Nvidia 文档匮乏——已导致行业内全职员工和可雇外包承包商中严重缺乏相应的高水平技能人才。

## 容器逃逸、安全预披露计划、渗透测试与审计

Neocloud 领域的安全，已从一道勾选题迅速升级为关键差异化因素。安全公司 Wiz 最近发现的 [NVIDIAScape（CVE-2025-23266）](https://www.wiz.io/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape)给业内许多人敲响了警钟。该漏洞允许在容器内运行的用户「逃逸」出容器，并提权到底层宿主节点的完整 root 权限——在任何客户工作负载相互毗邻、仅靠同一底层宿主上的容器做隔离的多租户环境中，这都是巨大的安全漏洞。最值得注意的是，该漏洞用一段简单的三行脚本即可利用，很容易在软件供应链中被植入 docker 镜像。

作为测试期间的概念验证（POC），我们把这一漏洞利用程序内置到基于 vLLM 和 nvidia pytorch 基础镜像构建的自定义容器中。运行起来极其简单：拉取容器、运行即可。显然，任何运行过期容器工具链版本、又允许执行来自公共仓库的任意容器的供应商，都在把客户置于风险之中：持久化后门、数据外泄、勒索软件、挖矿劫持等等。测试期间，我们演示了该漏洞利用在十几家供应商上有效——他们的 nvidia-container-toolkit 未更新（版本需为 1.17.8 或更高，详见：<https://nvidia.custhelp.com/app/answers/detail/a_id/5659>）。

最重要的是，这不仅是 Nvidia 一家的问题。AMD 生态历来缺乏健壮、安全的容器运行时，导致许多部署默认就是不安全的。ROCm container-toolkit 最近的开发正是对此的直接回应。然而，这些事件凸显了厂商安全预披露计划（embargo program）、客户沟通与修复的极端重要性。

顶级供应商被纳入 Nvidia 的 embargo 计划，会提前收到 NVIDIAscape 之类漏洞的通知。这让他们能在漏洞及其利用方法公开之前开发并部署补丁，保护客户。在我们的反馈和多家供应商的直接推动下，AMD 现在也建立了正式的安全预披露计划，让其 Neocloud 合作伙伴得以有效准备。我们现在测试 AMD 集群和独立 AI 虚拟机时，会把所提供的 rocm container toolkit 版本纳入考量（见：<https://github.com/ROCm/container-toolkit>）。

这就引出渗透测试与审计这些更大的话题。我们无法审计所追踪的每一家供应商的内部安全实践。因此我们的标准要求至少要有 SOC 2 Type I 或 ISO 27001 等第三方认证。对于托管专有模型和敏感企业数据的供应商来说，这是证明存在正式安全流程的绝对底线。不过，我们鼓励所有 Neocloud 采用超大规模云厂商的心态：零信任、纵深防御策略，配合持续审计和主动安全姿态。仅靠被动打补丁或基础渗透测试，无法有效服务全球领先的前沿 AI 实验室。

# AMD 和 NVIDIA 可以为 GPU 云与 ML 社区做得更好

由于 InfiniBand 相关的培训与文档持续缺失，许多 Neocloud 对 InfiniBand 并不熟悉。**自 8 个月前 ClusterMAX v1 向 Nvidia 提出同样建议以来，Neocloud 实际落实的情况并没有多大改善**（[见当时对 AMD 和 Nvidia 的建议](https://newsletter.semianalysis.com/i/174558503/recommendations-to-amd-and-nvidia)）。最近有一些[公开文档更新](https://docs.nvidia.com/networking/display/nvidiainfinibandsecurityoverviewandguidelines/practical+guidelines)，但[还不够，且未覆盖用于验证的命令](https://docs.nvidia.com/networking/display/nvidiainfinibandsecurityoverviewandguidelines/security+in+infiniband)。我们感谢那些正在努力改善局面的 Nvidia 员工。我们建议他们迅速继续提供更多优质、公开可访问的文档，并对其 NCP 大力开展培训，讲清安全加固 InfiniBand 网络所需的各种密钥（SMKeys、MKeys、PKeys、VSKeys、CCKeys、AMKeys 等）。我们建议 Nvidia 帮助其 GPU 云正确加固 InfiniBand 网络，并对所有使用 InfiniBand 的 GPU 云完成一次审计。

此外，[8 个月前我们同样建议 Nvidia 修复 SHARP 对 GPU 供应商的易用性问题，并建议 Nvidia 默认启用它](https://newsletter.semianalysis.com/p/the-gpu-cloud-clustermax-rating-system-how-to-rent-gpus?open=false#%C2%A7recommendations-to-amd-and-nvidia)。**Nvidia 在 SHARP 易用性上没有带来任何实质性改善**，InfiniBand SHARP 使用率极低的状况依旧。

在 ClusterMAX v1 中，我们[建议 AMD 在 slurm 中把容器支持作为一等公民，此后他们已启用初步支持，但 bug 不少](https://newsletter.semianalysis.com/p/the-gpu-cloud-clustermax-rating-system-how-to-rent-gpus?open=false#%C2%A7recommendations-to-amd-and-nvidia)。我们建议 AMD 对其 slurm 容器支持做进一步 QA，做到无 bug，别让终端用户每周都踩到新 bug。

对于同时提供 AMD 和 Nvidia 的供应商，其 AMD 云服务的质量远逊于其 Nvidia 云服务，缺少健康检查或可用的 slurm 支持等关键功能，比如 Crusoe 和 Oracle 等。OCI 的 AMD slurm 服务比 Nvidia 版差得多。Crusoe 和其他混合云也是如此。

## 关于 NVIDIA 云乱象的几点结语：从雄心到坟墓。别相信你撒谎的眼睛！

当 NVIDIA 以传闻中 $300-$900M 的价格收购 Lepton（一家 20 人的初创公司）时，Neocloud 们吓坏了。Lepton 曾是 ClusterMAX 黄金级供应商，拥有跨多云基础设施运行的独门能力、漂亮的履历（贾扬清是 PyTorch 的联合创造者之一）和对技术细节深挖的功力。我们是 Lepton 最大的粉丝！

到如今这个地步，Nvidia 似乎铁了心要毁掉 Lepton 的价值：让团队专注于做用户根本不在乎的功能、把产品界面换成深色主题和 Nvidia 品牌皮肤，还搞坏了各种东西（比如创建存储卷、notebook 和批任务的界面，以及在底层节点上触发健康检查的功能），而不是增加任何新东西。换句话说，Nvidia 版 Lepton 让我们想起当年的 cuDNN 下载门户，并加入了 Nvidia 软件收购「打包入库、等它死去」的长名单。罗列如下：

- 2024 年 5 月，Nvidia 以 $700M 收购 run:ai（编排与调度）
- 2024 年 5 月，Nvidia 以 $300M 收购 deci（推理优化）
- 2024 年 7 月，Nvidia 以 $100M 收购 shoreline.io（硬件自动修复）
- 2024 年 7 月，Nvidia 以传闻中的 $100M 收购 brev.dev（云开发机）
- 2025 年 4 月，NVIDIA 以传闻中的 $900M 收购 Lepton（集群、编排、监控与健康检查）

如果传闻属实，合计 $2.1B！还有一些重大发布：

- 2023 年 3 月 GTC 上，Nvidia 发布 DGX Cloud。
- 2023 年 8 月 Google Cloud Next 上，Nvidia 宣布 DGX Cloud 将登陆 Google Cloud。
- 2023 年 11 月 AWS re:Invent 上，Nvidia 与 AWS 宣布 DGX Cloud 将登陆 AWS，具体采用 GH200 Grace Hopper 超级芯片。
- 2023 年 11 月 Microsoft Ignite 上，Nvidia 宣布在 Microsoft Azure 上推出 AI foundry 服务，且 Nvidia DGX Cloud 已上线 Azure Marketplace。
- 2024 年 3 月 GTC 上，Nvidia 宣布 DGX Cloud 正式全面可用（GA）
- 2025 年 1 月 CES 上，Nvidia 宣布 Uber 正在使用 Nvidia 的 DGX Cloud 为其 robotaxi 车队构建模型。
- 2025 年 5 月台北 COMPUTEX 上，Nvidia 宣布以新名称「DGX Cloud Lepton」扩展 DGX Cloud 平台。公告将 Lepton 描述为一个算力市场，通过全球云合作伙伴将开发者与数以万计的 GPU 连接起来。
- 6 月的 GTC Paris 上，Nvidia 宣布 DGX Cloud Lepton 扩展至欧洲。

总体来看，这些公告和 Nvidia 承诺开源整个 run:ai 一样空洞。我们至今没有在 GitHub 上看到那个量级的发布。Lepton 也是如此（gpud 除外）。我们屏息以待。

在我们发表了一些关于 Lepton 收购现状的评论之后，Nvidia 直接向我们表示：被当成 Neocloud 让他们深感被冒犯。显然，这些收购都不是用来牟利或创收的。相反，前 DGX Cloud 正被「拖到谷仓后面处理掉」，而新的 DGX Cloud Lepton 得到力推。这对 Neocloud 是好事——看来花了 $2B 之后，Jensen 终于意识到他不想与自己最大的客户竞争。所以 DGX Cloud，可别那么干！

当我们尝试获取 DGX Cloud 的测试权限时，需要在不同周分别与 Nvidia 团队成员进行一次介绍通话和一次战略通话。没有这些沟通，我们手里只剩下 DGX Cloud 网站。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/9311c62a-6a50-4a1d-8afb-91bf3210f7f9_935x732.png)

网站把用户引向以下入口：

- **立即试用 Nvidia DGX Cloud** —— NGC 上的 NIMs 页面，那是一个模型端点 API
- **使用 Nvidia DGX Cloud 无服务器推理** —— 由 Nvidia Cloud Functions 驱动的无服务器推理 30 天预览注册页，看起来也是一个模型端点 API
- **探索 Nvidia DGX Cloud Create** —— 一个「与我们交谈」的注册页
- **用 Nvidia DGX Cloud Lepton 全球部署** —— 申请 DGX Lepton 访问权限的注册页。但如果你是 GPU 云供应商（也许想把你的算力接入这个市场？），可以发邮件到 NVIDIA Cloud Partner 邮箱：[dgxc_lepton_ncp_ea@nvidia.com](mailto:dgxc_lepton_ncp_ea@nvidia.com)
- **申请配备 NVIDIA GB200 的 Nvidia DGX Cloud** —— 一条绕回 DGX Cloud 首页的循环链接
- **在 DGX Cloud 上获取 Nvidia Omniverse** —— 指向 Azure Marketplace 上 DGX Cloud 页面的链接，需要注册，而且很可能把你的信息发给 Nvidia 销售部门的某个人

所以，DGX Cloud 的大部分似乎并不是一个 Neocloud，而是一堆议程不明的、与 Nvidia 销售团队的未来会议。

例外是门户里的最后一个链接，它把你带到 Azure。在那里，你可以连过两道 MFA，获得一个购买机会：DGX Cloud A100 80GB 1 节点 – 1 个月订阅，「超值低价」$23,360.00（可选自动续费）。

注意，这折合 $4.05 每 A100 小时——这是我们迄今在任何地方见过的最差价格，没有之一。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/432ed07a-f1ae-474f-a5bc-9a331af3fee9_936x692.png)
*来源：Azure、Nvidia*
![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/62fba08b-44f7-4d76-92ec-f7d9e8e2a2b7_936x692.png)
*来源：Azure、Nvidia*

话虽如此，Nvidia 还收购了 Brev——一个对 DataCrunch（现名 Verda）等 Neocloud 很有用的前端，它实际上似乎来自 Shadeform 的编排层。不过这个控制台简洁好用，且对公众开放：<https://brev.nvidia.com/environment/new/public>

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/fe01e294-1006-4cb9-9b23-000b6c4878f5_936x471.png)
*来源：Nvidia*

我们非常期待未来测试 Lepton、DGX Cloud 和 Brev。Nvidia 招募了一批极其勤奋、才华横溢的工程师，还有大量有用的 IP，其社区本可从中受益。我们希望未来能看到更多。

最终，我们也获得了测试 Lepton 的机会。

![](https://substack-post-media.s3.amazonaws.com/public/images/f8827598-08e7-4629-96cb-c7b56f04f5a7_3184x1714.png)
*来源：Nvidia、DGX Cloud Lepton*

在我们的测试期间（由于各种会议导致的拖延，测试在我们对所有 Neocloud 收工一个多月后才进行），我们未能成功创建 dev pod、批任务，也未能在节点上运行健康检查。尽管 DGX Cloud Lepton 被描述为「通过全球云合作伙伴将开发者与数以万计 GPU 连接起来的算力市场」，我们却被迫把自己的 GPU 机器接入控制台。这些机器始终在 DGX Cloud Lepton 之外管理和付费。平台上似乎没有任何预先注册的可用云，只有「BYOC」（Bring Your Own Cloud，自带云）功能。

总体而言，我们把 Nvidia 当作 Neocloud 或「类 Neocloud」供应商来体验的经历非常怪异。我们敦促 Nvidia 开源 lepton、run:ai、deci、shoreline 和 brev 的全部软件，让其 200+ 家 Neocloud 供应商社区受益。我们尤其希望 Lepton 能走上 TRT-LLM、NCCL 等的道路，而不是 RIVA、Maxine、Isaac 和 Drive 的道路。

# 评价

以下评价来自每日与 GPU 云基础设施打交道的行业专家、研究者与实践者。这些视角有助于阐明塑造 ClusterMAX™ 评级体系的真实挑战与考量。

## 行业领袖

> 「ClusterMAX 已成为我们做出数据驱动决策的宝贵工具，帮助我们决定在哪里、如何部署算力。作为在性能、可靠性与支持等维度对 GPU 云进行基准测试的领先体系，它为我们的团队在通过 Stargate 等项目扩展 OpenAI 基础设施的过程中提供了关键洞察——帮助确保 AI 的福祉惠及每一个人。」

—— Peter Hoeschele，OpenAI Stargate 总经理

> 「Meta 的超级智能事业同时依赖内部自建集群与云供应商，来打造用于前沿模型训练与推理的最大规模 AI 机群。ClusterMAX 提供了一套全面、可供全行业信赖的 GPU 云供应商评级体系。」

—— Santosh Janardhan，Meta 全球基础设施负责人

> 「AI 正在改变每个行业，其背后的基础设施必须可靠、可扩展且透明。SemiAnalysis 的行业标准评级体系 ClusterMAX，照亮了真正重要的东西——真实世界的性能、卓越的运营和客户支持——帮助各组织在复杂的 GPU 云版图中导航。对于任何向 GPU 云租用算力的人来说，它都是宝贵的资源。」

—— Michael Dell，戴尔科技（Dell Technologies）董事长兼 CEO

> 「在快速演变的 AI 格局中，选对 GPU 云供应商对最大化效率、最小化风险至关重要。Supermicro 赞赏 SemiAnalysis 的 ClusterMAX 评级体系，它从安全性、可靠性和性能上评估供应商，为企业和初创公司 alike 带来无与伦比的 GPU 基础设施价值。」

—— Charles Liang，Supermicro 总裁兼 CEO

> 「ClusterMAX 已成为 GPU 云的首选基准。通过聚焦用户真正关心的东西——托管 Kubernetes、SLURM 集成、运营可靠性和企业级支持，SemiAnalysis 帮助 GPU 消费者穿透 GPU 云的营销噪音，选出运行其工作负载的最佳平台。」

—— Hunter Almgren，慧与（Hewlett Packard Enterprise）杰出技术专家

> 「Snowflake 的使命是让每家企业都能以其所需的性能和规模，用数据和 AI 充分释放潜力。随着我们扩大 GPU 使用以加速 AI 工作负载，像 ClusterMAX 这样客观透明的基准评测无比珍贵。这套体系提供了从性能、可靠性和成本上评估 GPU 云供应商所需的清晰度，帮助我们做出正确的基础设施决策，以大规模支撑我们的客户。」

—— Dwarak Rajagopal，Snowflake AI 工程与研究副总裁

## 金融领袖与风险投资人

> 「ClusterMAX 是评估 GPU 云供应商的行业标准——它带来了亟需的透明度，让所有大大小小的 GPU 终端用户都能清晰了解最新的 GPU 云版图。」

—— Gavin Baker，Atreides Management 管理合伙人兼 CIO

> 「SemiAnalysis 凭借拼搏与努力，迅速成长为行业内值得信赖的信息源。ClusterMAX 就是最好的例证——它提供了一套全行业可以信赖的全面评级体系来评估 GPU 云供应商。」

—— Brad Gerstner，风险投资基金 Altimeter Capital 创始人、董事长兼 CEO

> 「ClusterMAX 在客户关心的关键维度——性能、可靠性、编排与安全——上对供应商进行严格基准测试，让我们能够准确把握 AI 算力的走向。」

—— Ricard Boada，Brookfield Asset Management 全球 AI 基础设施高级副总裁

> 「对 AI 初创公司、尤其是早期公司来说，GPU 往往是最大的一笔支出项。选对云供应商真的可能决定生死。SemiAnalysis 的 ClusterMAX 通过对成本、性能和可靠性做基准测试穿透噪音——这让团队在挑选 GPU 云时拥有做出最聪明决策所需的数据。」

—— Sonith Sunku，Z Fellows 风险投资人

## AI 公司与初创企业

> 「在 Periodic Labs，我们正在打造一位『AI 科学家』来加速科学发现。要做新颖的研究，我们依赖在大规模下既稳定又高性能的 GPU 云。SemiAnalysis 的 ClusterMAX 树立了 GPU 云行业标准，在我们评估云供应商时帮助极大。他们对可靠性、性能、网络和托管 Kubernetes 编排的评估，与我们的工作负载需求高度契合。」

—— William Fedus，Periodic Labs CEO，前 OpenAI 研究副总裁

> 「在 Cursor，我们用帮助工程师更快、更聪明地构建的工具，推进 AI 原生软件开发的前沿。为支撑研究，我们依赖可靠、高性能且易于扩展的 GPU 云。我们很高兴 SemiAnalysis 推出 ClusterMAX 这一行业标准的 GPU 云排名体系。它在可靠性、快速换节点与性能方面的评估，反映了对我们工作负载真正重要的东西。」

—— Federico Cassano，Cursor 研究科学家

> 「Jua 是一家前沿 AI 实验室，正在构建地球的基础世界模型——模拟天气、飓风、野火等。我们在托管 Slurm 上训练，在托管 Kubernetes 上做推理，ClusterMAX 与我们的 GPU 需求高度契合。」

—— Marvin Gabler，Jua CEO

> 「AdaptiveML 是面向企业推理、预训练和强化学习的统一平台。我们使用 FluidStack，并在全部三大超大规模云厂商的 GPU 上部署。我们的技术栈运行在 Kubernetes 上。ClusterMAX 的 9 大类标准与我们的需求高度契合。」

—— Daniel Hesslow，AdaptiveML 联合创始人兼研究科学家

> 「Extropic 正在开拓热力学计算——构建根植于信息物理学的 AI 系统。在内部，我们使用 SLURM 集群管理实验。我们很高兴看到 SemiAnalysis 行业标准的 ClusterMAX 体系将各供应商 SLURM 服务的评估纳入标准。」

—— Guillaume Verdon，Extropic 创始人，前 Alphabet 量子机器学习负责人

> 「在 Mako，我们正在把开发者从 GPU 性能工程的瓶颈中解放出来。我们的 AI 编程智能体为 NVIDIA、AMD 和定制加速器自动生成、优化并部署 GPU 内核。ClusterMAX 这套行业标准的 GPU 云评级体系，其多维度评估与我们的硬件无关方法论相契合，让我们能够为未来的 AI 系统交付无缝、可扩展的推理与 RL 后训练。」

—— Waleed Atallah，Mako CEO

> 「作为一家新兴 AI 实验室，Nous Research 开发了 Hermes 4 等广受欢迎的模型。对我们而言，ClusterMAX 是在我们最关心的关键维度——价格、性能与网络稳定性——上评估 GPU 云的行业标准。」

—— Emozilla，Nous Research CEO

> 「ClusterMAX 对我们很有用，虽然 Dylan Patel 这个人挺烦的。」

—— Matthew Leavitt，DatologyAI

> 「在 Cartesia，我们正在开发下一代交互式多模态智能，这需要高效、低时延且有韧性的基础设施。像 ClusterMAX 这样的体系提供了清晰度与技术细节，帮助各组织更好地理解如何扩展其算力基础设施。」

—— Arjun Desai，Cartesia 联合创始人

## 基础设施与平台服务商

> 「在 Modal，我们是面向 AI 与 ML 工程师的无服务器平台。高性能、可靠的 GPU 基础设施是客户的关键诉求。我们很高兴 SemiAnalysis 创建了其行业标准的 GPU 云排名体系 ClusterMAX。它指导了我们内部 GPU 可靠性系统 gpu-health 的开发，也为我们的 GPU 云供应商评估提供洞见。」

—— Jonathon Belotti，Modal 工程团队

> 「Baseten 是一个高性能推理平台，运营于模型性能的前沿，服务市场中多家领先 AI 公司和早期采用的企业。我们的推理栈提供极速冷启动、自动扩缩容和企业级可靠性。作为一家在 10+ 家云上运营的服务商，我们很高兴 SemiAnalysis 创建了其行业标准的 GPU 云排名体系 ClusterMAX。该体系在 9 项关键标准上进行评估，正是我们在 AI 模型性能前沿运营时最看重的。」

—— Ed Shrager，Baseten 特别项目负责人

> 「GPU 云正在通过普及企业级算力来推动 AI 革命。与传统云不同，GPU 云需要专门的软硬件优化，而这关乎 AI 性能的成败。SemiAnalysis 的 ClusterMAX GPU 云排名体系对完整技术栈提供了整体评估，并结合世界级分析，为 WEKA 提供了为 GPU 云合作伙伴及其客户设计强大 AI 基础设施方案所需的关键洞察。」

—— Val Bercovici，WEKA 首席 AI 官

> 「ClusterMAX 已成为 GPU 云排名的行业标准，其结果与我们在 fal 的真实体验完全吻合。」

—— Batuhan Taskaya，Fal.ai 工程负责人

## ML 社区领袖与内容创作者

> 「SemiAnalysis 为 GPU 云行业创建了深度研究与排名，覆盖了像我这样的终端用户所关心的领域，例如开箱即用的 slurm/kubernetes、NCCL 性能和高可靠性。」

—— Stas Bekman，开发者，《Machine Learning Engineering Open Book》作者（GitHub 10k+ star）

> 「SemiAnalysis 团队做出的这份 GPU 云排名，我觉得是所有其他人都希望自己能做出来的。它足够彻底、全面而且中立。方法论与真实世界应用对齐，而且相当全面。」

—— Jon，Asianometry，80 万+ 订阅的科技 YouTuber

# 展望未来

展望未来，针对 ClusterMAX 3.0 及期中评级，我们将直接公布对 slurm、Kubernetes、独立单机、监控和健康检查的期望。

请访问以下页面查看：

- slurm 相关：<http://clustermax.ai/slurm>
- kubernetes 相关：<http://clustermax.ai/k8s>
- 独立单机相关：<http://clustermax.ai/standalone>
- 监控相关：<http://clustermax.ai/monitoring>
- 健康检查相关：<http://clustermax.ai/health-checks>

请注意，这些页面会随时间更新。

# 结语

感谢您抽时间阅读 ClusterMAX 2.0！今后，您可以在 <http://clustermax.ai/> 查看最新排名与期中动态，或通过 [clustermax@semianalysis.com](mailto:clustermax@semianalysis.com) 与我们联系。

![](https://substack-post-media.s3.amazonaws.com/public/images/aa561ef5-7fa1-4a79-b70e-d93951471e95_2760x1810.png)
*clustermax.ai 网站首页。来源：SemiAnalysis*

# 各家云逐家评测

## 白金（Platinum）

### CoreWeave

自我们上一篇文章以来，CoreWeave 发布了一些重要公告。他们在纳斯达克完成 $1.5B 的 IPO，股票代码 $CRWV，股价 6 个月内上涨超过 200%。

他们宣布与 OpenAI 达成三项扩展合作：3 月 $11.9B、5 月 $4B、9 月 $6.5B，总承诺金额达到 $22.4B。这些交易面向训练。CoreWeave 还在 9 月拿下 Meta 这个新客户，签署了一份为期 6 年、至 2031 年、价值 $14.2B 的协议。

他们还在 7 月宣布以 $9B 全股票收购 Core Scientific，相当于新增 1.3GW 的数据中心足迹。他们还向英国投入 £1.5B，并向宾夕法尼亚州 Lancaster 投入 $6B。

注：想逐项追踪 CoreWeave 产能上线的读者，可参阅我们的数据中心行业模型：<https://semianalysis.com/datacenter-industry-model/>

他们在 5 月收购了 Weights & Biases，9 月收购了 OpenPipe。我们将在下文讨论 W&B 的整合。

他们还推出了 CoreWeave Ventures，一只投资 AI 公司的基金：<https://investors.coreweave.com/news/news-details/2025/CoreWeave-Launches-Ventures-Group-to-Invest-in-Future-of-AI/default.aspx> 。我们认为这是对一系列战略性投资举措的直接回应，例如 AWS Activate（最高 $300k 抵扣额度）、Microsoft for Startups（最高 $150k 抵扣额度）、Google for Startups Cloud Program（最高 $350k 抵扣额度），以及 NVIDIA Inception + NVentures 计划。

CoreWeave 宣布了全球最早一批 GB200 NVL72 和 GB300 NVL72 部署，以及一些 RTX 6000 Pro Blackwell 实例，为未来用 Rubin CPX 做多样化布局打下了基础。

从我们的测试来看，CoreWeave 的集群满足全部标准，并为其他 Neocloud 树立了标杆。正因如此，我们了解到多个案例中，CoreWeave 的托管 slurm 或 Kubernetes 集群能够比 Nebius、Fluidstack、Crusoe、Lambda、Together.ai 等直接竞争对手要价更高（按每 GPU 小时计约高出 10-15%）。事实上，CoreWeave 的定价更接近四大超大规模云厂商的水平。我们认为 CoreWeave 未来面临的主要挑战，是相对竞争对手持续创新和差异化，以维持这种定价权。我们相信在 GB200 和 GB300 NVL72 这一代上，他们会继续成功。

本节我们将谈谈 CoreWeave 的新动向，以及他们如何持续为业内其他人树立标杆。

- Slurm-on-Kubernetes
- 裸金属开通
- DPU 的使用
- 安全
- 监控与健康检查
- W&B 集成
- 存储
- TCO
- 服务
- 客户

#### Slurm-on-Kubernetes

目前 CoreWeave 已整合为三种产品：

1. CoreWeave 托管 SUNK（Slurm on Kubernetes）
2. CoreWeave 托管 Kubernetes
3. 不带任何托管调度器的 CoreWeave 裸金属

自 2023 年 10 月 SUNK 首次发布以来，新集群的采用一直强劲，这导致其裸金属 slurm 服务被弃用。所有偏好 slurm 的新客户都被引导至 SUNK。本文前文我们讨论了整个行业的 slurm-on-Kubernetes 趋势，其中 SUNK 是相对 Soperator 和 Slinky 最成熟的选择。CoreWeave 从零开发了 SUNK，掌控其路线图，并与底层 Kubernetes 运行时 CKS 深度集成，还整合了他们的监控仪表盘（以 Grafana 为主，品牌名为 CoreWeave Observe™）、健康检查系统和开通系统（品牌名为 CoreWeave Mission Control）。

此外，CoreWeave 没有止步于开源 slurm，而是为这个流行的任务调度器开发了自己的定制分支。具体来说，在开源 Slinky 中，slurm 控制器的 REST API 存在内存泄漏问题——例如，当有用户试图排队 100,000 个任务时就会出问题。

具体而言，slurm 在大规模下的运作方式依赖优先级概念。换句话说，一个最高优先级的大型预训练任务不可能被自动缩容，而且应该始终有空闲节点可供在中断发生时补充进该任务。而在这个任务运行期间，用户可以把较小的研究/实验 slurm 任务标记为可抢占（preemptible），放到中等或低优先级分区上运行。从功能上说，这意味着 slurm 调度器把信息移交给 kubernetes，后者为 kubernetes 任务打标签，将其关联到对应分区。实际上，前沿实验室积压着大量低优先级扫参（sweep）任务，随时可以吃掉多余的节点：尝试最新的学习率、数据配比等，看看能否改进研究效果。

因此，CoreWeave 用 go 语言重写了 slurm REST API 的逻辑，现在为 SUNK 使用了一个基于 RPC 的登录 pod 控制器，在大规模下性能更好。

有意思的是，我们知道 CoreWeave 与一些终端用户做过直接授权交易，这些用户想在 CoreWeave 之外的托管 Kubernetes 集群上运行 SUNK。虽然我们不认为 SUNK 授权是 CoreWeave 的重要营收来源，但这体现了使用 SUNK 的客户体验质量，也是其工程投入的证明。

#### 裸金属开通

CoreWeave 与其他云供应商的一个重要差异，是控制平面和工作节点服务都用裸金属机器。由于基本上所有 CoreWeave 客户都整台使用标准 HGX 的 8 卡机器（或 NVL72 机柜中的 4 卡机器），无需把一台机器虚拟化成多个 1 卡、2 卡或 4 卡 GPU 实例。

不过，Nebius 和 Crusoe 等同样不拆分 GPU 机器的供应商，则分别继续使用 kubevirt 和 cloud-hypervisor，以实现虚拟机的其他好处：共享块存储（扩容、快速开通、PXE 启动、备份、克隆、恢复等）和网络隔离。

由于虚拟机的启停比裸金属机器更容易/更快（即底层 OS 无需在租户之间更换），CoreWeave 面临一个必须解决的挑战：如何在大集群中快速更换和修复故障机器。为此，CoreWeave 开发了 Fleet Lifecycle Controller 和 Node Lifecycle Controller，供其 FleetOps 和 CloudOps 团队通过 CoreWeave Mission Control 服务来开通机器。

这套定制技术栈实际上在 kubernetes 上使用了一个名为 NodeSet 的 CRD，在裸金属节点上线之前就把它们定义为 kubernetes 资源。此外，CoreWeave 开发了自定义 operator（类似 DaemonSet 与 ReplicaSet 的混合体），用于空闲检查和调试等功能。这种定制还延伸到「受保护的滚动更新」（Protected Rolling Updates），它感知 slurm 状态，会等节点排空（drain）后再推出更新的 pod。实际上，硬件故障后修复完毕的节点会进入一个队列，等待被加入多租户后端网络 fabric 上的逻辑集群。

#### DPU 的使用

由于采用裸金属开通，CoreWeave 必须应对与 AWS 的 Nitro 或 Azure 的 Boost 相同的挑战。换句话说，如何在前端和后端网络都实现安全的多租户隔离。值得指出的是，即便客户以批发裸金属方式租下了整座数据中心，这类租户隔离挑战依然存在。租户仍会雇佣和解雇实习生、顾问、合作伙伴公司、学术合作者，也普遍有在同一底层硬件上的不同用户组之间实施隔离的需求。

因此，CoreWeave 在每个节点上都使用 Nvidia BlueField DPU，卸载传统上由宿主 CPU 上 hypervisor 承担的功能（VPC、加密、网络隔离、NAT 网关等）。采用分布式 NAT 网关和分布式存储网关架构，消除了一种常见的中央性能瓶颈。AI 负载具有「突发性」，因为单个研究任务或自动扩缩容的推理端点可能随机地同时开始拉取巨大的模型权重文件。把网关服务从集中式改为 DPU 上的分布式，保证了到 WAN 或存储的线速性能。

在 Kubernetes 上，这实际上是通过 CRD 和自定义控制器实现的，使裸金属节点可以在租户之间迁移，同时保持网络隔离与策略。强制执行的边界变成了 DPU，而不是 hypervisor。实际上，CoreWeave 团队通过 `kubectl get dpuconfigurations.nimbus.infra.coreweave.com` 来编程这一层的 API。

在后端网络上，InfiniBand 网络隔离通过按租户更改 PKeys（分区键）实现，这是类似以太网 VLAN 的硬件强制机制。CoreWeave 是少数提供 SHARP 的供应商之一，SHARP 可以显著提升某些集合通信的性能。不过，对于安全要求最高的客户，CoreWeave 不允许多租户 InfiniBand 开启 SHARP。

![各种线缆的拼贴
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/64268219-bec7-4ebe-91be-5e7fbc0a293c_935x534.png)
*来源：CoreWeave*

#### 安全

谈到安全，CoreWeave 是唯一具有超大规模云厂商心态的 Neocloud。这意味着零信任策略、租户之间的严格隔离和持续审计。

例如，一些其他 Neocloud 会提供对服务器 BMC 的直接访问，而 CoreWeave 以极其谨慎的态度对待 BMC——[它是一块巨大的攻击面](https://developer.nvidia.com/blog/analyzing-baseboard-management-controllers-to-secure-data-center-infrastructure/)。宿主机到 BMC 的访问已被禁用：从宿主 OS 到 BMC 的 KCS（Keyboard Controller Style）和 NIC（RNDIS Ethernet over USB）接口均已禁用。实际上，BMC 管理网络被隔离为只能与控制平面通信（N/S 侧），并强制执行二层隔离以阻止 BMC 之间的横向移动（E/W 侧）。

对于超大客户，BMC 访问通过利用专用 BMC 网络的动态跳板机（jumpbox）设置进行。DPU 上的 ACL 由 Fleet Lifecycle Controller 经 NIMBUS 更新，确保他们只能访问其特定租户内的 BMC IP。

另一个关键决策是避免多个客户运行在同一台机器上的情形。实际上，客户可以随意攻击自己的机器——正如容器逃逸场景所示——但如果一个节点下线维修或在租户之间迁移，它会先被 PXE 引导到干净状态，然后另一个租户才能在其上运行。这由 Fleet Lifecycle Controller（FLCC）和 Node Lifecycle Controller（NLCC）处理。

在容器逃逸方面，预计未来还会有针对 pytorch、transformers、vllm、sglang 等项目上游 nightly 分支的漏洞利用，CoreWeave 正在把所有客户镜像切换为以 ChainGuard 镜像为基础。自 Broadcom 收购 VMware 并随后上调 Bitnami 价格以来，我们看到这一领域的一个普遍趋势。值得注意的是，CoreWeave 的容器镜像已成为许多其他 Neocloud 的事实标准——从登录 pod 到 nccl-test 示例，许多其他供应商的镜像都是 FROM coreweave 镜像构建的，或者干脆直接提供从 CoreWeave 的 gcr 仓库拉取镜像的脚本：<https://github.com/coreweave/nccl-tests/pkgs/container/nccl-tests>

更多安全细节：

- 纵深防御与风险建模：安全建立在一个全面的威胁模型之上，该模型驱动纵深防御策略，贯穿默认安全的应用开发生命周期以及深入的运行时与基础设施加固。
- 应用与代码安全：应用安全成熟度框架强制要求所有代码变更经过机密扫描、SAST、SCA 和 DAST，并有严格的修复 SLA。风险通过 pre-commit 钩子、policy-as-code、CI/CD 强制执行、Chainguard 基础镜像和黄金服务模板（golden service templates）在投产前被拦截。
- 生产基础设施与访问：Teleport 以客户审批、RBAC、基于 TPM 的节点加入和会话记录（包括按键/系统调用）来治理特权访问，并积极淘汰传统 SSH。
- 机器群完整性与证明：基于 SPDM 的固件证明、Secure Boot 和 Measured Boot 从上电起验证整机群的完整性，确保只有经过加密验证的固件才能运行，并能在工作负载调度前进行远程证明。
- 数据与工作负载加密/身份：SecVault PKI 基础设施为数据（对象存储、数据库、API）提供加密支持，而 mTLS 的采用将把端点身份绑定到可信固件。跨集群 JWT 认证和 SPIFFE 集成保障工作负载之间的通信安全。
- 持续监控与安全姿态：Eclypsium 和 Wiz 提供持续的安全姿态管理，包括固件漏洞扫描和云工作负载姿态，而遥测管道确保策略合规与偏差检测。
- 企业身份与数据：安全策略强制所有用户使用抗钓鱼 MFA 和设备信任，Kolide 负责执行设备姿态检查。Policy-as-code 的 Okta 规则治理访问，Cyera、Proofpoint 和 Netskope 等系统管理数据治理与 DLP 管控。

我们得到的反馈是，CoreWeave 的安全限制对许多高级用户来说过于严苛。例如，默认情况下 systemd 不可用，许多 CPU 和 GPU 性能剖析工具也因严格的安全考虑而无法使用。这导致终端用户做出一些奇怪的设计选择，比如在 tmux shell 里跑后台进程，而不是使用 systemd。

#### 监控与健康检查

CoreWeave 的监控与健康检查系统是一项关键差异化优势，也是与质疑 CoreWeave 溢价定价的大型客户讨论 TCO 时首要量化的条目。换句话说，在 10k+ GPU 规模上运行的用户深知中断对训练任务的影响。

CoreWeave 意识到，标准的 Nvidia（DCGM）exporter 并不会暴露所有关键指标，例如对诊断导热硅脂失效这类隐蔽硬件问题至关重要的某些热传感器。CoreWeave 用更底层的 NVML 库开发了专有 exporter。这为稳健的节点级健康验证提供了必要的粒度。

此外，他们还为互连 fabric 构建了 exporter。为识别计算托盘与交换机之间信号完整性劣化这类瞬态物理层问题，CoreWeave 开发了一个精密的关联引擎。我们注意到，其他供应商在烤机（burn-in）和主动定时健康检查期间并不运行持续的多节点任务，而是分别运行单节点任务、集合通信和 GPU 压力测试（[GPU burn](https://github.com/wilicc/gpu-burn)、[GPU fryer](https://github.com/huggingface/gpu-fryer) 或 [多节点 ubergemm](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-multinode-diagnostics.html#supported-tests-for-multi-node-diagnostics)）。关键在于，故障往往是由 GPU 与互连的**同时**热胀冷缩引起的。这对 NVL72 机柜级架构尤其重要。

通过追踪整个 fabric 上同时出现的 XID 或 SXID 错误等事件，CoreWeave 能够自动定位许多故障类型的根因。例如，如果连接到同一交换机端口的多个计算托盘都报错，交换机就会被标记；而如果某个错误在托盘被移动后仍跟随该托盘，则是托盘或其线缆被标记。这类简单直觉随经验积累，CoreWeave 已在 GB200 和 GB300 NVL72 机柜级系统上积累数月——这套系统让许多其他供应商运营起来极为吃力。<https://semianalysis.com/2025/08/20/h100-vs-gb200-nvl72-training-benchmarks/#gb200-nvl72-unreliability>

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/5ddb3f17-6379-4995-8c9e-d3bea778e4f9_936x636.png)
*来源：CoreWeave 在我们的集群上模拟的一些错误*

Meta 的 Llama 3 论文最清晰地描述了训练活动中可靠性问题可能出现在哪里。在训练 Llama 3 405B 的 54 天里，使用 8 个各含 3,072 块 H100 的 pod，任意时刻 24k 块 GPU 中有 16k 块在用，共发生 466 次任务中断（其中 47 次是计划内升级），导致 419 次 GPU 服务器故障，以及三次重度人工干预。

这隐含着 2,111 H100-天的 MTBF，我们可以假设「重度人工干预」指的是从上一个检查点重启任务。

这个例子突出表明，硬件稳定性和互连性能的哪怕微小改进，也能从大型模型数月的训练排期中省下数天甚至数周时间。在我们交流的研究人员中，硬件故障也是第一大挫败来源。

![带文字的表格
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/0d9eb732-36a5-4a60-8cbe-9b929f2a182b_936x549.png)
*来源：The Llama 3 Herd of Models https://arxiv.org/abs/2407.21783*

论文的这一节还因另外两点而「臭名昭著」：一是提到「基于一天内不同时段的 1-2% 周期性吞吐波动」（即 GPU 在中午更热、性能更差）；二是评论说「数以万计的 GPU 可能同时增加或降低功耗（……）会导致整个数据中心功耗以数十兆瓦为单位瞬时波动，挑战电网的极限」——这后来导致一位 Meta 工程师在某次提交中意外把 PYTORCH_NO_POWERPLANT_BLOWUP=1 环境变量带进了上游代码。

![文字特写
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/03b0c4ca-8a5f-41c4-9d6d-76dab48edf85_930x308.png)
*来源：The Llama 3 Herd of Models https://arxiv.org/abs/2407.21783*

总之，在与其他 Neocloud 合作解决可靠性难题时，我们仍将 CoreWeave 的监控仪表盘、被动健康检查方式和一整套主动健康检查视为标准。更多细节见：<http://clustermax.ai/expectations/health-checks>

#### W&B 集成

在被收购之前，Weights & Biases（W&B）已成为任务调度面向用户指标领域的行业领导者，但定价相当高，而且公司的创新似乎一直在亏钱。显然，CoreWeave 注意到了自家客户与 W&B 企业客户之间的高度重叠。具体来说，其中一些客户曾因在其 W&B 部署背后搭建了极其庞大的日志基础设施而闻名，实际上是在滥用这套系统。

W&B 整合显而易见的第一步，是把基础设施级指标（如 OOME 或 AER）集成到 W&B 仪表盘中，让用户可以看到。通常，单个研究人员无权访问集群级 grafana 仪表盘，但仍有大量他们可以利用的有用信息，特别是来自底层 Nvidia DCGM 的信息。

#### 存储

CoreWeave 的存储产品随时间逐渐成熟，包括原生对象存储产品「CAIOS」（CoreWeave AI Object Storage）和本地缓存「LOTA」（Local Object Transfer Accelerator）。

LOTA 是一个透明的分布式缓存，直接驻留在每个 GPU 节点的本地 NVMe 上。公开基准测试显示，它在 Blackwell 上可达到每 GPU 超过 7GB/s 的持续吞吐。

实际上，有了 LOTA，用户无需 cp 或 rsync 任何东西。只需把 S3 兼容应用指向 cwlota.com 端点，而不是主 CAIOS 端点 cwobject.com。LOTA 随后会以分布式方式在整个集群内管理数据向本地 NVMe 的缓存。

按牌价计算，例如一个 1,204 GPU 的集群，按每 GPU 小时 $3 租用 1 年，总成本为 $26.9M。

而在存储方面，1PB 活动数据按每月 $0.11/GB 计，成本为 $1.3M，占总 BOM 的 4.6%。

总体而言，我们很少见到存储成本超过集群总成本的 5%。

随着时间推移，我们预计 AWS、Azure、GCP 和 Oracle 等超大规模云厂商将跟随当前趋势，降低其对象存储产品的每月每 GB 价格（很多情况下是受 CloudFlare R2 竞争驱动），降低或取消惩罚性的出口流量费，并降低或取消数据访问等存储操作相关费用。

#### 支持

以我们的经验，以及与 CoreWeave 服务用户的直接交流来看，我们的印象是：团队成员被充分授权、乐于帮助客户，并以在这家公司工作为荣。值得注意的是，所有数据中心技术员都是 CoreWeave 员工，接受公司标准化培训，并持有公司股权。CoreWeave 是少数从未用别人的 GPU 来扩充产能的 Neocloud 之一，在其所有设施中保持了垂直整合。

此外，CoreWeave 的「直连专家」支持模式意味着所有客户都能获得快速响应，无需额外费用。但别处可不一定如此！最近，CoreWeave 还特意在 Slack 上给我们发了一条 ClearFeed 通知，说他们的年度公司外出活动（offsite）可能导致支持响应出现一些延迟。

![消息截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/d98fcd18-383d-40fe-b664-de6d617bab40_578x280.png)
*来源：CoreWeave*

上次，我们建议 CoreWeave 做一个 UI 控制台流程来部署其托管 slurm 方案，最好点击不超过四次。CoreWeave 基本上做到了，不过界面上 30 多个数据中心看起来大多置灰不可选。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/84800a5c-6b9a-4832-865f-9bcfb71e8f05_936x508.png)
*来源：CoreWeave*

#### 总拥有成本（TCO）

总之，CoreWeave 在 Slurm-on-Kubernetes、裸金属开通、DPU 使用、安全、监控与健康检查、W&B 集成、存储和支持方面的执行成果，使其能够宣称相对竞争对手更低的 TCO，并按每 GPU 小时获得溢价定价。

在他们扩张规模之际，我们给 CoreWeave 的反馈是：继续完善按需、自助式集群体验，继续开发支持大规模推理的自动扩缩容功能，并保持在 NVL72 机柜级部署上的可靠性领先。从客户角度看，CoreWeave 的一个不足仍然是不提供按需实例或自动扩缩容，且很少接受短期租赁。这一点不同于 Nebius 和 Crusoe，也限制了与高利润「spot 实例」市场相关的潜在上行空间。
## 黄金（Gold）

### Nebius

自 ClusterMAX 1.0 以来，在我们与客户的交流中，Nebius 始终是 CoreWeave 最直接的竞争对手。Nebius 的客户包括 Shopify、Recraft、Mirage、Genesis Therapeutics，最近还与 Microsoft 就其新泽西州 Vineland 数据中心签下一份为期 5 年、价值 $17.4B（可扩展至 $19.4B）的协议。我们[预计 Nebius 向 Microsoft 的交付还会继续提前](https://semianalysis.com/core-research/openais-250b-azure-commitment-msft-needs-neoclouds-capacity/)，健康的交易管道也预示着会有更多增量产能随时间陆续上线。

Nebius 在财务上的差异化来自其低资本成本：资产负债表上有数十亿美元现金、无债务，并且是我们追踪的两家纯 GPU 上市 Neocloud 之一（另一家是 CoreWeave）。在技术上，Nebius 的差异化在于虚拟化的 GPU 基础设施方案（建立在 Yandex 的经验之上），以及借助内部 AI 团队「吃自家狗粮」（dogfood）带来的 AI 原生方法——这已经催生了 AI 领域的多家分拆初创公司。

虽然我们知道他们在争取托管（colocation）协议和建立信用评级方面历经波折，但其工程实力有目共睹。Nebius 平台优先考虑灵活性、按需访问和稳健的 Kubernetes 原生体验。这与 CoreWeave 的裸金属长期预留模式形成对照，使 Nebius 成为自动扩缩容和 spot 实例（尤其用于实验和推理）的有力选择。Nebius 在各类算力市场上持续以低价供应商形象出现，而且是少数把真实价格直接放在官网首页的供应商。

![网站截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/2786b950-f482-424a-85f6-0a53e8b6166c_935x516.png)
*来源：Nebius*

似乎这还不够，Nebius 还在进军推理端点市场！

本节将讨论我们对 Nebius 平台的实操体验：

- Slurm-on-Kubernetes
- 虚拟化与存储
- 监控与健康检查
- 按需实例

#### Slurm-on-Kubernetes

自 ClusterMAX 1.0 以来，Nebius 已正式推出其[托管 Soperator 服务](https://nebius.com/blog/posts/introducing-managed-soperator)，提供完全自助式的 Slurm-on-Kubernetes 体验。

我们进行了实测，不出所料，我们拿到的 Slurm 集群开箱即用、完全就绪。包括预装的驱动、Docker、节点间免密 SSH，以及开箱即达预期的集合通信（nccl-tests）和 pytorch 训练任务（torchtitan 预训练）性能。

这些要求也许看似基础，却不能想当然。本文后面会描述，其他供应商要把 Slurm-on-Kubernetes（通过 Soperator 或 Slinky）以合理的默认配置装好有多难。值得注意的是，由于 Nebius 使用的是自家开源项目 [Soperator](https://github.com/nebius/soperator)，他们完全掌控路线图，并实现了垂直整合——从 sbatch 脚本的客户支持问题，一直到 kubernetes 编排、硬件和数据中心排障层。

控制平面也颇为美观：

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/f4cd7168-85d2-428f-bf86-1fb76e9503f0_937x660.png)
*来源：SemiAnalysis 的 Nebius 集群*

#### 虚拟化与存储

与 CoreWeave 的裸金属优先策略不同，Nebius 把平台建在层层相互管理的 Kubernetes 集群之上，一路向下都用 KubeVirt。这意味着客户工作负载——即便是完整的 8-GPU 节点——也运行在客户可以访问的一个 kubernetes 集群内的虚拟机里，而该集群本身又由一个只有 Nebius 能访问的 kubernetes 集群管理。这种设计与 GCP 编排算力的方式类似。该架构让 Nebius 得以利用虚拟机的优势，例如快速开通和高级存储特性。例如，他们用 virtio-fs 挂载一个巨大的共享根文件系统——在我们的集群上开箱即显示为 197TB、挂载在「/」——但显然并不需要在服务器里物理安装 197TB 的硬盘。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/11d49df2-690f-4d8a-b9e4-de7ed73d1cbc_518x148.png)
*来源：SemiAnalysis 的 Nebius 集群*

Nebius 的存储方案构建在 YDB <https://ydb.tech/docs/en/contributor/distributed-storage> 之上，后者实际上支撑着他们的块存储、共享文件系统和存储产品。这种存储方式缩短了新机器的启动时间（即拉取容器镜像或模型文件），在一些按需自动扩缩容负载的例子中，从 10 分钟以上降至约 2-3 分钟。

一种常见认知是裸金属性能优于虚拟机。当我们提出这一点时，Nebius 团队坚持认为用户只需对平台跑基准测试即可。他们的立场是：由于 InfiniBand fabric 和 Nvidia GPU 本身没有虚拟化层，性能应与裸金属完全一致。我们的初步测试似乎印证了这一说法，第三方结果也是如此。例如，在上一轮 MLPerf Inference v5.1 基准测试中，Nebius 在 Nvidia GB200 NVL72、HGX B200 和 HGX H200 系统上运行 Llama 模型推理取得了顶级性能。

<https://nebius.com/blog/posts/bare-metal-class-performance-mlperf-inference>

客户关于虚拟机的另一个反馈点，是能否轻松启用底层硬件计数器做性能监控。启用硬件计数器的方法因虚拟化平台而异。

在 VMware vSphere 中，可以通过编辑虚拟机设置启用虚拟化 CPU 性能计数器。这一功能称为 vPMC，允许客户操作系统访问宿主机的性能监控单元（PMU）。而在搭载 Hyper-V 的 Windows Server 和 Windows 10/11 上，可以用 Set-VMProcessor 等 PowerShell cmdlet 为处于停止状态的虚拟机启用特定的性能监控硬件特性（如 pmu、pebs、lbr）。

而在 KubeVirt（Nebius 所用）经 KVM/QEMU 的场景下，虚拟机会从底层宿主机继承暴露硬件计数器的能力。该过程通常需要在底层 kubernetes 集群上配置虚拟机的 CRD，以启用 Intel 的虚拟 PMU。CPU 周期数、缓存未命中、分支预测错误等硬件级性能数据都可以由此获得。通常可以在 Kubernetes 集群上激活一个功耗指标或 PMU 插件（如 Telegraf 插件）来启用这一能力。例如，一些用户会用 Kubernetes CPU manager 等特性把 vCPU 绑定到宿主机 pCPU 上，为 CPU 密集型负载获得可预期的延迟，以完成高级性能调优。

值得注意的是，对于坚持要求裸金属且做长期租赁的超大客户，Nebius 确实可以提供裸金属集群。

#### 监控与健康检查

起初，我们对监控的访问只是通过 SSH 端口转发打开的一个简易 Grafana 仪表盘。这些指标和健康检查比较基础，但团队随后发布了一系列更新，显著提高了水准。

有意思的是，由于这一切都在被集成进 SOperator，而 Soperator 又是开源的，我们得以在 Soperator 的 GitHub 项目上看着路线图逐步落地：<https://github.com/orgs/nebius/projects/1>

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/82ef1e50-f573-4155-a180-32b5871ddb9b_935x494.png)
*来源：Nebius Soperator 的 GitHub 项目*

没有哪家 Neocloud 在开发上像 Nebius 这样开放透明。

差不多在通知我们仪表盘和健康检查改进的同一时间，Nebius 还发布了一篇博客，详细描述了他们在可靠性上的做法：现场工厂测试、节点部署测试、虚拟平台测试、预开通集群测试、被动与主动健康检查。我们相信这套烤机测试、健康检查与监控仪表盘组合将提升集群的可靠性与易用性，尤其是当 Nebius 为 Microsoft 等客户大规模转向 GB300 NVL72 机柜级系统之时。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/6108afa3-2d8a-4fb8-9c11-1de2059a312a_936x309.png)
*来源：Nebius*
![计算机程序示意图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/e2e1c842-6ae7-4974-9958-4da08be8d043_936x226.png)
*来源：Nebius https://nebius.com/blog/posts/how-we-build-reliable-clusters*

博客中，Nebius 描述了一个假设示例：一个 1,024 GPU 集群在 336 小时（14 天）内发生 13 次故障，得出 GPU 级 MTBF 为 26,446 GPU 小时，即 1,101 GPU 天。

一个恰当的对比来自 Meta Llama 3 论文的数据：一个 16,000 GPU 集群在 1,296 小时（55 天）内发生 419 次故障，得出 GPU 级 MTBF 为 50,677 GPU 小时，即 2,111 GPU 天。

再进一步对比，我们听说在黄金和白银级供应商处运行类似规模集群（1k 到 2k GPU）的客户，曾在相当长的时间里每天经历多达 5 次以上故障。这相当于 GPU 级 MTBF 低于 10,000 GPU 小时，即不足 400 GPU 天。

在我们的研究中，Meta 公布的数字非常高，体现了 Meta 运营数据中心和 Hopper 代 GPU 的水准。而 Nebius 的假设数字则对应相当不错的客户体验。

博客后文，Nebius 声称曾有一个 3,000 GPU 集群不间断运行了 169,800 GPU 小时，即 56.6 小时的稳定运行。这折算成 GPU 级 MTBF 高达 169,800 GPU 小时即 7,000 天，离谱至极。我们对供应商这样挑选可靠性数据的做法普遍感到无奈。

我们鼓励客户自行追踪这类可靠性数据，尤其是当 DataDog、New Relic、Splunk 或自定义 Prometheus Alertmanager 已配置并接入 Slack 频道、用于 XID 相关错误通知时。如果你在追踪这些数据，并愿意贡献给匿名化汇总研究，请联系：[clustermax@semianalysis.com](mailto:clustermax@semianalysis.com)

![计算机错误信息截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/14f8d842-3d8f-423a-b777-552113266e08_854x468.png)
*来源：Nebius https://nebius.com/blog/posts/how-we-build-reliable-clusters*

显然，在 1k+ GPU 规模的托管 slurm 集群方面，Nebius 正在积累实战经验（battle scars）。

#### 按需实例

Nebius 的一项关键差异化优势，是对按需和自动扩缩容负载的稳健支持。这是其软件定义架构的直接结果。他们提供可抢占（pre-emptible）实例，主要面向推理客户，功能上类似超大规模云厂商的 spot 实例。这让用户能以更低成本获取算力，同时理解负载可能被中断。

我们见过公开的实际案例，例如 Shopify 在 Nebius 平台上使用 SkyPilot 和 dstack sky 的工作，凸显了他们在支持动态、研究型负载上的强项。这种灵活性对无法签订长期合约的用户是显著优势，似乎也是 Nebius 客户入站线索的主要来源。

#### TCO

Nebius 在 GPU 云市场中提供了一个有说服力且技术上与众不同的选择。他们基于 KubeVirt 和 Soperator 的 Kubernetes 原生虚拟化技术栈的深度投入，使其能够提供高性能训练领域罕见的灵活性和按需访问。虽然他们在获取数据中心方面可能面临阻力，但其软件栈成熟且高性能。

我们给 Nebius 的反馈是：在向客户推出这些更新的同时，继续改进监控与健康检查的可见性，并为所有层级用户简化通知流程。他们通过基于虚拟机的架构交付等同裸金属的性能，是一项重要的工程成就。对于以研究、自动扩缩容推理为核心需求、且负载能受益于类 spot 可抢占市场的用户来说，Nebius 是挑战竞争对手长期预留模式的绝佳选择。

值得注意的是，一些客户始终揪着 Nebius 的俄罗斯出身不放——尽管其全部员工都在俄罗斯境外工作——而不是基于技术优劣做采购决策。我们不确定 Nebius 能如何应对持这种心态的客户。

### Oracle

Oracle 刚刚交出了市场见过的最不可思议的季度财报。我们的[预测已领先于市场一致预期](https://semianalysis.com/core-research/orcl-preview-rpo-can-increase-120b-in-f1q26-and-above-200b-for-fy26-well-above-street-expectations/)，但即便如此也没能完全料到这一结果。具体来说，Oracle 在第一财季与三家不同客户签署了四份价值数十亿美元的合同，其中包括与 OpenAI 的 $300Bn+ 大单。The Information 近期的报道提出了这些数十亿合同下 AI 服务器利润率的担忧，但我们认为爬坡期利润率偏低是合理的，并[预计利润率将显著扩张](https://semianalysis.com/core-research/core-weekly-insights-orcl-veco-colocation-chain/)。

![电脑屏幕截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/44192941-3be5-40f8-b4ba-348096089482_936x671.png)
*来源：Oracle*

Oracle 的处境十分独特：它是唯一一家没有自建 AGI 研究计划、也没有大规模风险投资的超大规模云厂商（在全球 45 个活跃区域拥有 100 多个可用域 AD）（尽管 Larry 在和 Elon 互通几条短信后确实向 xAI 投了 $2B），这使它拿下了与 OpenAI、Meta、ByteDance 和 Nvidia 的合同。据公开信息，他们目前握有美国 Stargate 超过 60% 的份额。我们也在 [Accelerator & HBM 模型](https://semianalysis.com/accelerator-hbm-model/)中对此做详细追踪。

Oracle 还早早转向批发式裸金属，利用其资产负债表优势，同时在托管 slurm 和托管 kubernetes 市场保持了可观的存在感。在很多情况下，我们发现其他云供应商提供的服务器，其 IP 地址、位置等信息明白无误地表明我们其实运行在 Oracle 的数据中心里。

Oracle 的默认部署通常通过控制台完成，后台用 Terraform 自动化。对一些用户来说，一个明显的摩擦点是几乎强制使用 Oracle Linux（默认版本 8.10），它基于 Fedora。这一操作系统选择颇有争议，因为许多 AI 负载——尤其是开源社区的负载——最先是在基于 Debian 的操作系统上测试的，特别是 Ubuntu，因其兼容性广、易用性好。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/7c28227d-728e-413f-bf31-a4b5ec9e5736_935x336.png)
*来源：SemiAnalysis 的 Oracle Linux 头痛经历*

我们把默认使用 Oracle Linux 归因于与 Canonical 的历史恩怨。这令人意外，因为经过认证的 Ubuntu 镜像早在 2017 年就已在 Oracle Bare Metal Cloud Services 上提供，并且一直更新到如今的 24.04 版。

要通过 OCI 控制台部署 slurm 或 kubernetes 集群，用户不幸必须使用 OCI 控制台。视觉上，该控制台遵循 [Redwood 设计系统](https://redwood.oracle.com/)，并使用他们的 [JavaScript Extension Toolkit (JET)](https://www.oracle.com/webfolder/technetwork/jet/index.html)，两者都毫无愉悦可言。即便在 AI 时代，Oracle 对 Java 的终身承诺依然坚定不移。部署集群后，想访问 Grafana 仪表盘的用户需要在迷宫般的 UI 选项中穿行。感兴趣的话，秘籍是：左侧汉堡菜单 > Developer Services > Stacks > Stack details > Application Information >（往下滚动）> Grafana admin password。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/6ee8adbd-3c4e-4dee-a980-dad1e7f8f67f_935x502.png)
*来源：SemiAnalysis 的 OCI 控制台*

在 slurm 和 Kubernetes 的测试中，一切顺利。我们很快在 nccl-tests 上达到预期的集合通信带宽，在 torchtitan 上达到预期 MFU。有意思的是，首次登录 slurm 集群时，我们发现有一个节点处于 drain 状态。它很快被更换，但这也凸显了与 CoreWeave 相比，在健康检查和裸金属节点开通方式上的差异。

Oracle 正积极改进平台可靠性与用户体验。Node Auto-Repair 与 Node Problem Detector 集成预计在第四季度推出，目标是通过官方 OCI 二进制程序为客户提供「doctor HPC」般的用户体验。团队还在开发一种名为 Sustained Workflow Check 的主动健康检查机制，即运行 PyTorch 和 CUDA matmul 线性回归 2-5 分钟，以确保持续性能。该检查目前按需运行，多数情况下由 Oracle 工程师直接与客户协作，把检查安排在低优先级分区。默认行为正在开发中，以便将其集成进 slurm 和 OKE。

托管 Kubernetes 方面，Oracle 提供 OKE（Oracle Container Engine for Kubernetes），默认所有资源都是公开的。用户可以选择关闭这一默认值并使用 Nvidia GPU Operator，不过默认配置使用的是一个自定义 operator。OKE 提供 GPU 和 GPU+RDMA 节点池作为开通选项，还通过一个复选框提供集成存储选项。设置 RDMA 的官方指南是公开的，nccl-test 的清单显示 allreduce 和 allgather 操作具有不错的开箱性能。

OKE 设置中最令人懊恼的一点是缺少直接的 kubeconfig 文件。用户只能 SSH 进集群执行管理操作。对于一个公网可达、带负载均衡的服务来说，这很反直觉，而且集群管理员或用户要从外部正常访问集群，可能还需要一台堡垒机代理。对用户而言，kubernetes 相对 slurm 的一大关键优势就是可以在本地开发代码、快速切换不同集群上下文，无需 ssh。

网络方面，OKE 在 Kubernetes 中使用 RDMA 网络的默认做法是向 pod spec 注入两个字段：hostNetwork: true 和 dnsPolicy: ClusterFirstWithHostNet。在 OKE 上，Oracle 并不部署完整的 GPU Operator，而只部署 device plugin，计划之后再补上完整 operator。节点上安装了 Nvidia toolkit 并自动更新，确保软件栈保持最新。在 kubernetes 上用 vllm 基准测试经 llm-d 的预填充/解码（PD）分离推理，结果强劲，而且通过公网 IP 与所提供的 LoadBalancer 服务的设置和集成都很简单。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/885c73c5-d50d-4a69-9e9b-e1909928916a_936x690.png)
*来源：Oracle HPC on OKE 仓库 https://github.com/oracle-quickstart/oci-hpc-oke/blob/main/docs/running-pytorch-jobs-on-oke-using-hostnetwork-with-rdma.md*

初始测试阶段缺少集成的健康检查。虽然后来加上了 slurm 指标，但控制平面最初缺乏必要的 CLI 功能，导致不得不做一些回滚，以防客户无意中终止任务。新引入的「mgmt」CLI 旨在解决这些运营复杂性问题，我们对此表示赞同。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/e8c94afe-05bc-48a1-a06f-130e5147e0de_936x306.png)
*来源：Oracle*

存储方面，Oracle 提供了一个稳健的市场，Weka 和 DDN 是主要合作伙伴。Weka 既可以通过他们的在线按需市场获取（即可用装满 NVMe 的裸金属实例按需搭建），也可以通过直接签约获得。Oracle 客户反馈，在 Oracle 上与 Weka 的联合支持体验比 VAST 或 DDN 都更好。网络方面，Oracle 和其他超大规模云厂商一样自卖自夸，试图让大客户相信 InfiniBand 并非唯一的高性能网络方案、他们的 RoCE 用起来很好。他们在这方面似乎正在取得进展。

总体而言，Oracle 在改进其托管集群产品上进展显著，监控仪表盘和节点生命周期管理都有提升，但在主动性方面仍有改进空间。客户仍有可能比 Oracle 的自动化系统更早发现坏节点，并且不得不手动上报以更换节点。

Oracle 仍是四大超大规模云厂商中性价比最高的，部署新基础设施最快，同时提供最佳支持。我们预计 Oracle 未来将继续扩大其批发式裸金属和托管集群两项业务，并鼓励 Oracle 保持对所有客户提供卓越客户支持的承诺。

### Azure

Azure 维持其黄金级供应商的评级，因为它在 2026 年底之前仍将承载 OpenAI 的绝大部分产能。

遗憾的是，如果你不是 OpenAI 的员工，Azure 在托管集群或按需虚拟机方面算不上重要玩家。全球所有区域的 Hopper 和 Blackwell 产能都吃紧，CycleCloud slurm 开通流程亟需更新，至少也该简化。随着 OpenAI 与 Microsoft 锁定长期合作关系、Microsoft 获得约 27% 股份及至 2032 年的模型/IP 权利，这一点已被[再次确认](https://openai.com/index/next-chapter-of-microsoft-openai-partnership/)。

当我们考察可靠性并对比 slurm（CycleCloud）与 kubernetes（AKS）时，OpenAI 这类锚定租户享有的批发裸金属体验与市场上其他客户的托管体验之间的差距就一目了然。

AKS 的可靠性包含完全托管的节点自动修复（Node Auto-Repair）功能。该系统基于 kubelet 状态条件自动检测不健康节点，并尝试通过重启或重装镜像进行修复。这一理念延伸到监控：Azure Monitor for Containers 开箱即用地提供对集群每一层的集成可见性。

形成鲜明对照的是，CycleCloud 依赖传统 HPC 模式，即 slurm 的 HealthCheckProgram。但 CycleCloud 没有提供像 LBNL 的 Node Health Check <https://github.com/mej/nhc> 这样开箱即用的默认方案，也没有任何针对 Azure 基础设施定制的方案。健康检查的全部运营负担都压在用户身上，他们必须编写、测试和维护自定义脚本来监控 GPU 和 InfiniBand fabric。不仅如此，集成监控仅限于 UI 里一个高层级的节点状态视图，迫使用户为任何有意义的任务级或硬件级洞察（如 DCGM 仪表盘）自行搭建方案。

举例来说，部署 CycleCloud 集群时，当前文档分裂为旧指南和以 GitHub 为中心的新方式。用户需要分别配置登录节点和调度器节点，还要自行开通并管理 MySQL 数据库来处理 slurm 记账（sacct）。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/38e571f6-0d68-463a-a971-5649830a1019_937x467.png)
*来源：Azure*

不过，超大规模云厂商平台的全面性也有其优点。网络很直接，提供经 NAT 网关或堡垒主机的访问选项。它还通过支持自定义镜像、集成 Azure Spot Virtual Machines 以实现高性价比突发负载，带来灵活性。Azure 在 HPC 领域的历史积淀，对从学术 HPC 背景转向 GPU 集群的用户来说会很亲切。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/dd8528d9-f71b-4de4-babd-ad473510f54e_937x467.png)
*来源：Azure*

网络方面，Azure 在超大规模云厂商中继续保持性能领先，是唯一采用 InfiniBand 部署并大规模实施 SHARP 的厂商。安全性同样坚如磐石，Microsoft 一向以稳健的安全与合规实践著称，这使其成为联邦政府机构和国防承包商信赖的合作伙伴。

话虽如此，Microsoft 与其关键客户 OpenAI 的关系动态正在转变。自 Satya 表示自己「那 $80B 没问题」以来，Stargate 已经膨胀为一个 $600B 的庞然大物，其中大部分被 Oracle 收入囊中。Google、xAI 和 Meta 纷纷效仿，Zuck 承诺在未来 5-7 年投入同样总额的 $600B。

现实是，考虑到前沿实验室的算力需求和既有承诺，我们预测 Azure 的市场份额将会流失。这将把 Azure 留给市场上其余客户，而这些客户普遍要求强大的 slurm 或 kubernetes 托管集群体验和顺畅的支持体验。

要服务好这类客户，我们认为 Azure 必须重塑其 CycleCloud 产品，简化当前的集群部署与监控体验。否则，鉴于其对从 A 轮初创到 AI 独角兽的糟糕用户体验，Azure 有被降至白银级的风险。与 CoreWeave、Nebius、Oracle 等 Neocloud 的全托管、Kubernetes 原生、垂直整合产品相比，再加上我们在 AWS 和 GCP 身上看到的激进产能建设和调价，Azure 面临着激烈竞争。

### Fluidstack

Fluidstack 是本轮唯一新晋黄金级的云，也无疑拥有最独特的商业模式。Fluidstack 几乎所有客户部署都涉及第三方数据中心供应商。Fluidstack 实际上就是那个「雇佣兵」：各组织找它来把青铜级的数据中心基础设施变成黄金级的客户体验。Google 也已下场[锁定托管算力需求](https://semianalysis.com/core-research/core-weekly-insights-6/)，由 Fluidstack 担任 Terawulf 和 Cipher 站点的运营方，这些算力可能用于其 TPU。我们在[这里](https://semianalysis.com/core-research/google-clouds-growth-will-surge-in-2026/)探讨了 GCP 为何愿意为这些交易「兜底」、以及 GCP 为何需要 Fluidstack。

从 Meta、Poolside、Blackforest Labs，以及一个在 TeraWulf 布法罗（Buffalo）数据中心运行、获得 Google 巨额财务兜底的未具名客户身上，这一点表露无遗。

我们对 Fluidstack 的实操体验，就是其价值主张的现场演示：一个高度协作、深度技术性的合作伙伴关系，能根据专家反馈快速改进平台。虽然初始集群有些毛糙，但 Fluidstack 团队解决问题速度之快、之精准，无人能及。

我们最初的 slurm 集群自带集成进 srun 的 pyxis 和 MPI 支持，最初的二节点 nccl-tests 在大消息尺寸下性能也在正常范围。但我们立刻撞上一个严重的易用性问题：prolog.d 脚本塞满了健康检查，导致在单个节点上调度一次交互式运行要花一分多钟。每次任务启动时，该脚本都会完整跑一遍 NVLink 和 InfiniBand 的单节点 NCCL 测试，外加主机到设备的带宽检查。

当我们指出这一点时，团队立即承认问题，并承诺按路线图把这些主动健康检查改为在后台空闲节点上运行——这也是其他顶级供应商的标准做法。

由此开启了一轮快节奏的反馈循环，定义了我们整个测试期：

性能调优：我们发现基础镜像里缺少 Nvidia HPC-X 工具包，而这对中等消息尺寸下的最佳 nccl 性能是必需的。虽然 NGC 容器里有，但并非所有用户都用 pyxis/enroot。24 小时内，Fluidstack 团队就把 HPC-X 部署到了我们集群的基础镜像，并将其加入面向所有客户的标准部署流水线。

监控仪表盘：Grafana 仪表盘本身不错，但我们发现缺少 NVLink Rx/Tx 利用率的图表，而且张量核心管道的 DCGM 指标有误（采集的是 SIMT 单元，而不是像 DCGM_FI_PROF_PIPE_TENSOR_HMMA_ACTIVE 这样张量核心专用的管道）。团队第二天就实现了正确的 DCGM 指标。

安全姿态：这是最关键的发现。我们发现集群运行着受 NVIDIAScape（CVE-2025-23266）影响的 nvidia-container-toolkit 版本。我们上报后几分钟内，团队就在我们的集群上修补了该漏洞。虽然即时修复令人印象深刻，但我们的反馈聚焦于更大的运营需求：自动化依赖扫描和主动式安全流程，例如加入 Nvidia 的安全预披露（embargo）计划。这促成了关于其软件供应链安全战略的一次良性讨论。

被动健康检查：我们发现 DCGM 的后台健康检查没有启用。通过注入 PCIe replay 错误（dcgmi test --inject --gpuid 0 -f 202），我们确认节点不会自动进入 drain。我们建议主动轮询 dcgmi health -c，并配置 NVIDIA Health Check（NHC）基于特定阈值排空节点（例如每分钟 >8 次 PCIe replay，或每秒 >100 个 NVLink CRC 错误）。团队立即将此列入近期路线图。

切换到 Kubernetes 无缝顺畅，kubeconfig 可直接从 UI 获取。集群提供了扎实的基础，包含标准组件：Cilium 作 CNI、支持 ReadWriteMany 的 CSI、node-problem-detector、kube-prometheus-stack、draino、一个用于关闭 ACS 的自定义控制器，以及 Nvidia Network Operator + GPU Operator，全部经 ArgoCD 管理。这种高接触模式通常涉及共享的基础设施即代码仓库，确保客户获得所需的精确工具——比如在我们的案例中添加 cert-manager。

然而这次测试再次暴露了 slurm 评测中最关键的主题：软件供应链安全。我们发现 Nvidia GPU Operator chart 落后了一个次版本，使集群暴露于同一个 NVIDIAScape 漏洞利用之下。这凸显了他们主动安全姿态上的显著缺口，尤其是没有加入能提前收到漏洞通知的厂商预披露计划。接到通知后，团队协调了一个维护窗口，不到一小时就修补了漏洞，并受此推动着手把安全流程正规化——包括更频繁的主动更新、订阅漏洞数据库，以及着手加入 Nvidia 的披露计划。

总体而言，我们对 Fluidstack 的体验非常出色。平台开箱并不完美，但集群交付后几小时内，slurm 和 kubernetes 都达到了完全可用的状态，工程团队展现了精英级的响应速度和专业能力。在超大规模云厂商的工单系统里可能要几周甚至几个月才能解决的问题，这里几小时就修好了。如果说测试期间有谁真正践行了「前向部署工程」（Forward Deployed Engineering）的精神，那就是 Fluidstack。

### Crusoe

自 3 月以来，Crusoe 一直在努力扩张数据中心足迹，同时设法让 Neocloud 业务活下来。

Crusoe 已宣布：

- 与 Oracle 合作开发 Abilene——OpenAI 的旗舰 Stargate 项目，规模超过 1.2 GW，合资资金达 $15B。
- 向 GE Vernova 订购 29 套 LM2500XPRESS 航改燃气轮机机组，足以支撑超过 1GW 电力。
- 部署 AMD MI355X GPU——尽管 Nvidia 是其 $600M D 轮融资的关键投资方。
- 在怀俄明州建一座 1.8GW 数据中心，设计可扩展至 10GW：<https://www.crusoe.ai/resources/newsroom/crusoe-and-tallgrass-announce-ai-data-center-in-wyoming>。
- 与 atNorth 合作扩建冰岛设施，并为该项目安排了 $175M 信贷额度。
- 与 Polar 在挪威合作一座较小的 12MW 设施，并计划扩建至 52MW。
- 从 Brookfield 获得 $750M 信贷额度。
- 从 Upper90 获得 $225M 信贷额度。
- 「Prometheus」，一座位于得州西部二叠纪盆地（Permian Basin）的 150MW 设施。

有意思的是，Prometheus 首次公开展示了 Crusoe 的数字火炬气回收（Digital Flare Mitigation）技术。在二叠纪盆地这类地点采油时，天然气火炬燃烧属于废物排放。而借助 DFM，Crusoe 可以在现场部署移动数据中心单元，把这些本被烧掉的天然气转而供给现场数据中心的发电机。这些 DFM 单元以「Crusoe Spark」之名发布，如今已包含托管 B200 所需的全部基础设施。

![Crusoe 介绍 Crusoe Spark：面向可扩展边缘计算的模块化 AI 数据中心](https://substack-post-media.s3.amazonaws.com/public/images/ac83abd3-c9ec-43a5-85de-186d8fabb3ae_936x526.jpeg)
*来源：Crusoe Spark 发布（来自 Crusoe 的 YouTube 频道）*

在所有这些公告之后，Crusoe 声称拥有 3.4GW 的数据中心足迹，其中一部分已经开始在其资产负债表上体现为营收。

![网站截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/214c7c4a-8cc4-4368-a9d3-6c464fa3174a_937x397.png)
*来源：Crusoe.ai*

是的，动静不少。

至于 Crusoe 上的真实客户体验：大约六个月前我们开始测试 slurm 时，他们刚推出名为「Auto Clusters」的全托管 slurm 方案。在这段时间里，该服务已经走完了它的生命周期，重心现在转向 Slurm-on-Kubernetes 体验。遗憾的是，新的 Slurm-on-Kubernetes 体验尚处早期，开箱不可用。

启动集群很简单，通过 Crusoe CLI 即可，避免了复杂的 terraform 脚本，也简化了 webUI 的部分复杂度。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/e6a435e9-0276-472d-b8d4-90d95a97ba9b_641x639.png)
*来源：Crusoe*

然而，既然采用了简单的 CLI 方式，我们就期待合理的默认配置。Crusoe 声称其 Slurm-on-Kubernetes 方案为自研，同时借鉴了 Slinky。遗憾的是，登录 pod 缺少 vim、nano、git、python 和 sudo 权限。我们给了些建议，让他们少借鉴一些开源 Slinky、把集群做到开箱即用。该 SonK 方案也不支持分区、RBAC 和 SSO 集成，对一个超过约 10 名研究员规模的实验室来说基本没法用。

此外，为了测试在不开 slurm 的情况下开通 kubernetes 集群，我们要额外配置很多东西。Crusoe CMK 集群不包含默认的 ReadWriteMany StorageClass，导致任何带持久卷声明（PVC）的负载都无法部署。我们不得不在控制台上摸索许多额外配置步骤，才弄清如何配置这个存储类。

测试期间，我们还在 slurm、kubernetes 和独立单机上遇到若干性能与可靠性问题。我们反复在单个 Docker 容器内看到 NVML 驱动不匹配错误，暗示镜像或驱动管理可能不稳定。我们估计这是由于 Crusoe 使用 [cloud-hypervisor](https://github.com/cloud-hypervisor/cloud-hypervisor.)，并坚持用虚拟机构建其全部基础设施——包括 GB200 NVL72。

网络方面，虽然集成了用于 InfiniBand 分区的 PKeys，但通过控制台使用它们并不直观。我们还遇到过共享文件系统随机卸载的麻烦，以及需要手动部署系统盘、手动配置 RAID 设置（随之而来的各种坑）。

与 Crusoe 用户聊大规模可靠性时，反馈时好时坏。有些人体验不错，但所有在 2025 年 3 月之前于 Crusoe 冰岛设施测试过集群的人，似乎都有一段共同经历：大量链路抖动（link flap）和随机文件系统卸载。Crusoe 最后不得不使用「clicker」清洁器清理 20,000 个布满灰尘和其他碎屑的光纤端面。有人说那些碎屑是火山灰。

我们发现，2023 年 11 月，atNorth 的冰岛数据中心 ICE02 开始发布状态公告，称雷克雅内斯半岛（Reykjanes）Þorbjörn 山附近的地震活动与火山隆起有所增加。该数据中心距这座火山约 35km。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/0a52486d-933a-4cfc-9dde-54adfdb05413_937x694.png)
*来源：EDIS Global*
![电脑屏幕截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/37303b2d-250d-418d-b83a-d73f4edecf14_937x719.png)
*来源：https://status.edis.global/notices/y2d8vjath5kvmq8t-iceland-potential-volcanic-eruption*
![城市地图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/b0808ec5-423a-4805-a804-cfced30fe539_936x829.png)
*来源：Google Maps。顺手查一下一位 atNorth 数据中心技术员午休时间跑去一座活火山要多长时间*

据我们了解，这座如今被 Crusoe 称为家的数据中心，持续经历显著的地震活动和空气质量问题，于是又催生了更多来自冰岛的这类 YouTube 热门视频。

![一人手持蓝绿两色电线
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/b520d037-0aae-485d-960d-50bcf89ac500_937x652.png)
*来源：trueCable 的 YouTube 频道*

总体而言，Crusoe 显然在执行一项雄心勃勃的战略，锁定了大量电力产能和数据中心地产。他们已经从加密货币挖矿转型为 AI 云一次，如今似乎正在经历第二次转型：从云供应商转向数据中心基础设施供应商。

然而，Crusoe 面临被降至 ClusterMAX 白银级的风险：其多位顶尖的独立贡献者（IC）工程师离职，云部门的文化开始变得像大公司。整个组织里中层管理者太多，工程部门尤甚。这导致发布节奏极其缓慢（例如他们的 AutoClusters 功能），让我们对 Crusoe 公有云产品的未来感到担忧。Chase 如果不想失去他所有的 10x 工程师、并最终随之失去 Neocloud 业务，就需要迅速调整航向。
## 白银（Silver）

### Together

Together 是一家实力强劲的供应商，slurm 和 kubernetes 集群产品都很稳健，但可靠性问题使其未能进入黄金级。在比较报价时，我们听用户说，他们普遍期望 Together 的每 GPU 小时价格更低，以补偿可靠性上的折价。在运营 64 GPU 及以上集群的用户中，Together 是我们听到可靠性抱怨最多的少数供应商之一。我们估计这是因为他们使用了五花八门的数据中心合作伙伴，给性能和稳定性带来了「掷骰子」式的随机性。遗憾的是，与其他白银、黄金、白金级供应商不同，Together 也不向大多数客户提供 1 周 POC，这让买家在做出数百万美元承诺之前，很难知道自己在这套集群上会有怎样的体验。

以上就是 TogetherAI 从黄金级供应商跌至白银级供应商的全部原因。

Together 的多数据中心战略似乎是形势所迫。由于其无服务器推理端点业务稳步增长，他们有庞大的算力需求。为本文做调研时，我们与多家 Neocloud 交流过，他们都声称 Together 是自己最大的客户之一。在无服务器推理端点业务上竞争确有两大好处：一是形成销售漏斗，可以向推理客户交叉销售 GPU 集群；二是让 Together 得以在空闲集群算力上跑推理负载，消化其成本。这也让 Together 有机会享受其内核团队的劳动成果。TKC 是一项出色的特性，Tri Dao 的 FlashAttention 的影响怎么强调都不为过。在本文调研期间，我们直接从 Dan Fu 那里听到了 TKC 的路线图。我们怀疑 Dan 是业内唯一头衔为「VP, Kernels」的人，而且理由充分。TKC 始终令人印象深刻，它帮助客户和 Together 自己的无服务器推理端点业务实现了更高的性能与效率。Together 通过运行公有和私有无服务器端点来抵消空闲算力成本的模式，如今已被 Nebius 等效仿。何不让空闲算力多赚点钱呢？

测试期间，我们拿到了一个经典 Together slurm 集群、一个 TKE kubernetes 集群，以及一个即将发布、处于预览阶段的 Instant Cluster。slurm 的上手流程很顺畅：在控制台创建账户、上传 ssh 密钥，Together 工程团队会发给你一份上手文档。一条 ssh 命令，集群开箱即用。遗憾的是，测试中我们注意到，在 VSCode 或 Cursor 的远程 SSH 会话里，集群对终端命令响应极慢。标准终端应用则正常，而且我们从多个地点都能复现这种缓慢，因此我们相信问题出在其数据中心供应商身上。

Kubernetes 的上手体验就没那么精致了。他们没有提供可下载的 kubeconfig 文件，而是要我们通过 ssh 登录访问集群。如前所述，这对 kubernetes 管理员和用户来说并不常见，他们一般更愿意在本地开发代码、按需切换上下文。此外，我们发现 Helm 等标准工具没有安装，用户默认也没有 sudo 权限，需要更多手工配置。Together 用 rancher k3s 提供这些集群，考虑到其无服务器端点有多大比例跑在 kubernetes 上，这有点奇怪。Together 有多个客户（包括 Hedra、Cartesia 和 Krea）在这些托管 K8s 集群上用数千块 GPU 成功运行生产推理。但目前，Together 在这些集群中不具备水平节点自动扩缩容能力。你承诺多少容量，就得到多少。集群业务与端点业务之间的这种动态博弈很值得玩味：用户既可以把它看作 Together 自己与自己竞争，也可以看作给终端用户提供了选择。

![计算机程序截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/3d4c4089-b55b-43bc-a687-9619706269bb_936x819.png)
*来源：Together。试图使用我们的 TKS 集群，翻车*

「Instant Clusters」是 Together 最新的产品，设计为可通过 API、CLI 和 Terraform provider 全面管理。该产品允许用户动态开通集群、按需增删节点，适合应对突发容量和自动扩缩容。Instant Clusters 的架构采用与 Nebius 类似的多层方案提供强租户隔离。第一层，基础 Kubernetes 集群用 KubeVirt 为客户创建专用虚拟机（VM）。第二层，这些 VM 组成该客户专用的隔离 Kubernetes 集群。第三层，再用 Slinky 的 slurm-operator 把 slurm 装进客户的专用 K8s 集群。总体而言，这一架构让 Together 能够在现代虚拟化技术栈之上提供灵活、按需的 Slurm 环境。值得注意的是，在我们的测试中，Together 是唯一一家把 Slinky 正确配置到开箱即用的供应商——sudo 权限、vim/nano、git、python 等基础包一应俱全。他们显然已经向部分用户推出了该产品，我们期待它全面 GA。

在这些集群上，Together 提供主要驻美的待命 SRE 团队的 7×24 小时支持。网络方面，他们与客户直接协作，在数据中心层面配置防火墙规则，并按需提供 IP 地址，包括 1:1 NAT 和可通过 MetalLB 等服务分配的公网 IP。

Together 与黄金级供应商之间最后、也是最重要的一块差距，是监控与可靠性上的主动和自动化方法。这是 Together 的弱项，而且鉴于他们签约使用的数据中心和 GPU 基础设施伙伴过于分散，这个问题很难绕开。

在审查监控仪表盘时，我们发现他们的 Grafana 监控仪表盘有一个 bug，把 InfiniBand 带宽错误地报告为物理上不可能的 1.14 Tbit/s。值得肯定的是，我们指出后，他们的团队迅速找到了查询中的计算错误并部署了修复。

对于被动健康检查，我们期望检查在后台持续运行，以便发现在线节点的故障。这也是他们当前实现与全自动化系统之间差距最明显的地方。Together 已实现对许多关键问题的检测，包括 GPU 掉卡（falling off the bus）、PCIe 错误、InfiniBand 链路抖动、GPU 高温以及 ECC 内存错误率过高。基础的 Kubernetes 节点健康检查也已就位。然而，最关键的缺口是自动修复。虽然他们能检测到上述大多数问题，但自动排空故障节点的逻辑（除 slurm 下 GPU 掉卡之外）仍在路线图上。路线图上的其他关键功能还包括：检测不可纠正的 Nvidia XID 错误、识别卡死的 NCCL 任务，以及实现基于 AI/ML 的预测性故障分析。

在主动健康检查方面，Together 目前实现了一套完整的单节点验证测试，包括 Nvidia 的 DCGM 诊断（level 3）、PCIe 带宽测试、用于验证本地互连的单节点 NCCL 与 InfiniBand all-reduce 测试，以及 GPUBurn 等 GPU 压力测试。然而，关键的多节点和应用级测试仍在路线图上，包括验证 InfiniBand fabric 在负载下表现的成对 ib_write 测试、用 Nvidia 的 TinyMeg2 做硬件正确性验证，以及用 Megatron 等模型做全栈性能测试、确保 TFLOPs 和损失收敛与参考值一致。我们此前已指出，这些测试在烤机和集群运营期间至关重要：它们会长时间同时压测 GPU 和互连，使整个集群像正常运行时那样发生热胀冷缩。我们鼓励 Together 优先实现这些主动健康检查，因为我们相信这有助于提升可靠性，尤其是与不受其直接控制的数据中心伙伴合作时。

总之，Together 的托管集群业务继续运行在扎实的基础上。他们的集群和无服务器推理端点产品都拥有庞大且不断增长的客户群。其主动式单节点健康检查相当出色。然而体系尚未完整。我们认为，「被动检测到节点故障、而非主动自动修复」之间的差距，是用户当下遭遇可靠性问题的关键原因。

### Lambda

Lambda 是另一个本有黄金级实力的候选者，不幸的是它在一个错误的类别上拿了第一：客户抱怨。Lambda 2012 年起步时做的是人脸识别软件，随后转型转售 SuperMicro GPU 工作站、服务器，最终做本地部署（on-premises）集群。如今，他们似乎已 100% 聚焦于「Superintelligence Cloud」，并努力甩掉历史上的本地服务器和工作站业务。他们与 Microsoft 的[最新公告](https://lambda.ai/blog/lambda-announces-multibillion-dollar-agreement-with-microsoft-to-deploy-ai-infrastructure-powered-by-tens-of-thousands-of-nvidia-gpus)表明，他们将跨数万块 Nvidia GPU 提供价值数十亿美元的产能。

与用户交流时反复出现的一个主题是：Lambda 似乎不幸地试图为所有人做所有事。虽然公司在搭建专用 HPC 集群方面经验深厚，但这尚未转化为精致、易用的云控制台或集群监控体验。他们的产品线让人无所适从：新版 mslurm、旧版 mslurm、新版 mk8s、旧版 mk8s、私有云、1-Click Cluster 和按需实例。

值得注意的是，1-Click Cluster 并非真的只需一次点击，因为你还得等待审批。它更像是一个「一次点击-如果审批通过-并且付了钱-然后你才能拥有」集群。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/f30c7652-e758-40dd-b0a1-c15ef0d3e2fa_936x242.png)
*来源：Lambda Labs*

对于想立刻拿到按需机器的用户，Lambda 通常被认为是顶级的按需供应商，拥有最大的可租 GPU 机队。然而，以我们最近的经验，Lambda 的按需业务正饱受成功之苦。我们通常迎来的都是显示容量售罄的置灰界面：

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/b2e1e4cd-aa7d-4ed1-b78b-f12886012569_935x486.png)
*来源：Lambda Labs：试图从 Lambda 拿到一台按需 GPU 实例*

另外，有一阵子 Lambda 似乎要进军无服务器推理 API 端点业务，这将使其与一些最大的客户正面竞争。但现在不是了：

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/f9c6481a-22dc-4998-9964-47344c99dc46_936x598.png)
*来源：Lambda Labs*

总体而言，我们喜欢这种聚焦。Lambda 已经转向，非常专注于其 1-Click-Cluster（1CC）业务，主打「猎杀大单」（big game hunting）。

测试期间，我们评估了他们新版（自管）和旧版（基于 rancher）的 Kubernetes 产品，以及最新推出的 slurm 产品。这两者都不由 UI 或 CLI 驱动，而是需要一位 Lambda 工程师为你搭建集群。

Lambda 的 Kubernetes 产品感觉像一个早期阶段的产品，技术债明显，用户体验不佳。虽然当前产品已不使用 Rancher，但公开文档仍提到它，造成最初的困惑。推理负载的用户体验尤其欠缺。集群不带默认的公网 IP 方案（如 MetalLB 或外部 LoadBalancer）。搭建面向公网的推理服务既复杂又缺乏文档，需要大量手工配置。这反映出一个以训练负载为目标开发的平台，而非推理。虽然文档里有简单的单 GPU vLLM 部署示例，却没有多 GPU、多节点或自动扩缩容推理负载的示例。

监控方面，Lambda 混用了多种开源工具，包括用于 GPU 设备管理的 LeptonAI gpud 和用于健康检查的 node-problem-detector，但它们与新旧 mk8s 产品的监控仪表盘集成得并不顺畅。仪表盘容易访问，但若不安装一个未写入文档的 agent 就无法接入指标——而且细看之下，该 agent 还在开发中。

slurm 方面，Lambda 的产品是较新的补充，上手过程问题频发。初始设置繁琐：ssh 密钥未在集群上正确配置；默认主目录默认不跨节点共享，需要手动搬运数据。新建用户账户也很头疼，需要诸如取消环境变量（XDG_DATA_HOME）之类的变通手段才能正常工作。

值得肯定的是，一旦迈过这些初始障碍，集群性能相当强劲。我们在 nccl-tests 上观察到符合预期的 allreduce、allgather 和 alltoall 带宽，并在示例 torchtitan 训练负载上达到了满 MFU。Lambda 还提供了一些有用（尽管难找）的工具。例如，一条欢迎信息（在 Cursor 或 VSCode 等部分 SSH 客户端中不可见）中包含自定义说明，介绍如何用 grafana-access 命令快速查看性能指标。

Lambda 在 slurm 集群上的可靠性方案包括一个可按需运行的自定义 dcgm-status 脚本：

该脚本还被安排以固定节奏在低优先级的「可抢占」分区中运行：

![程序截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/886e4633-5588-4da7-aed5-ed1427531a17_935x725.png)
*来源：我们的 Lambda 测试集群*
![黑屏程序截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/a61413b0-5ee2-456e-b2a2-b13e50e1d551_935x224.png)
*来源：我们的 Lambda 测试集群*

Lambda 在开发全面主动与被动健康检查上的投入令我们印象深刻，我们相信他们正在妥善解决可靠性难题，积累大规模运营 NVL72 机柜级系统所需的实战经验。

话虽如此，我们遇到的一些访问问题指向 Lambda 更广泛的运营挑战。在我们短暂的测试窗口内，他们的云控制台（虽然不是我们的集群）经历了宕机。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/7df56f4d-e298-4e9d-a53d-cba66c254179_937x557.png)
*来源：Lambda Labs*
![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/74617ea2-6c23-4630-bf0f-e7a9b810ae31_937x496.png)
*来源：Lambda Labs*

内部似乎存在一定程度的混乱。当被问及真正的「云控制台」体验时，Lambda 承认团队背景主要是传统 HPC 集群部署，而非构建可扩展、自助式的云基础设施。我们鼓励 Lambda 在精简产品组合、聚焦 mslurm 和 mk8s 产品的同时，未来真正把重心放在云体验上。

好的一面是，Lambda 正根据我们的反馈积极改进平台。他们设有合规团队，针对各站点落实 SOC 2 Type II 要求；并且正在实施 SHARP 和 InfiniBand 安全密钥以实现多租户隔离——这遵循了 Nvidia 近期的建议（很可能也与 Nvidia 以一份 $1.5B 合同成为客户有关）。其存储产品目前以 VAST 为主，未来的 S3 兼容产品正在开发中。

总体而言，Lambda 是一家硬件功底深厚、产能庞大、未来规划宏大的强势供应商。但其公有云产品尚显稚嫩，与其团队打交道的过程也显得混乱。我们鼓励 Lambda 继续努力，把其 HPC 硬件实力转化为稳定、易用、可靠的云服务。

### Google Cloud（GCP）

你会以为 Google 会定下标准。从 jax 到 transformer，从搜索到地图，从 Waymo 到 YouTube。我们用 Gmail 加 Gcal 预订一个 Gmeet 来完成工作。我们还得从 gcr 拉 CoreWeave 的容器，到他们的 kubernetes 集群上运行。关于 TPU 的传闻满天飞。

自本文第一版以来，Google 已解决了一些拖后腿的问题，特别是决定为其 H200（a3-mega）和 B200（a3-ultra）实例以及 GB200 NVL72 实例（a4）采用标准 CX-7 NIC。

我们的测试从为 slurm 和 Kubernetes（GKE）各开通一个集群开始。托管 slurm「Cluster Director」产品仍处于预览阶段，不过在 Google 这里，「预览」也意味着关键客户已经用了好几个月，而且运行良好。其架构遵循标准的托管服务模式：slurmctld 由 GCP 负责，用户则可访问登录节点和工作节点。我们很欣赏默认配置，包括预先放进 GCS 桶、可立即使用的 nccl-test 网络性能测试脚本和 FIO 存储性能测试脚本。存储方面，GCP 推荐用 Filestore 做主目录，提供快照、备份等企业特性，而托管 Lustre 则定位于大规模、高性能的 scratch 空间。开通我们的 Lustre 文件系统很直接，但并不即时，大约花了 40 分钟。

有意思的是，该集群还展现了自愈能力：当我们为了清理环境、从 slurm 转向 GKE 测试而故意删除一个工作节点时，Cluster Director 服务几分钟内就自动重建了它，以维持目标容量。我们只能从 cluster director 界面删除整个集群，删除才真正生效。演示很精彩。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/0ab2ffbc-3459-42f7-bbec-94bd13b1b201_935x524.png)
*来源：Google Cloud。在 GKE 上删除 SLURM 集群。这个 UI 让人心情愉悦*

然而，基于 GKE 的方案才是 GCP 真正大放异彩之处，感觉领先除 CoreWeave 之外的所有 Neocloud 竞争对手数年。使用「Cluster Toolkit」，初始设置很顺畅。最令人印象深刻的是，集群交付时就预装了 Kueue 和 JobSet。这种对现代、Kubernetes 原生批处理负载调度的即时开箱支持，是一项重要差异化优势。当竞争对手还在自建 operator 或依赖 Slurm-on-Kubernetes 项目时，GCP 已提供成熟、完全集成的方案。

开箱性能不错。用标准 JobSet YAML 跑 nccl-tests，我们无需任何调优就立刻达到了 allgather、allreduce 和 alltoall 操作的预期带宽。不过值得指出，我们的体验并不能代表其他人在大规模下遇到的情况。

目前，对于使用 Nvidia CX-7 NIC 的 GCP gIB 机型（如 a3-ultra H200、a4 B200 和 a4x GB200），要获得良好性能，用户必须使用 `gIB` 插件。这意味着用户需要在 sbatch 脚本或 jobset 清单中加入额外的容器挂载和命令，例如 `--container-mounts="/usr/local/gib"`、`export NCCL_NET=gIB`、`source /usr/local/gib/scripts/set_nccl_env.sh` 等。这样的用户体验很差，导致即便是高级用户，与其他供应商直接对比时也会看到糟糕的性能。实际上，你需要一位 GCP 工程师才能在大规模下获得预期性能，而且这个横向扩展网络上 alltoall 集合通信是否能如预期工作，对我们来说仍是个悬而未决的问题。

我们对 Google 改善这一体验的建议是：让 Nvidia 把 gIB 插件二进制文件直接内置进所有 NGC 容器镜像，并在容器初始化时加入逻辑，在兼容的 GCP 机器上自动选择 gIB 插件。这样用户就无需手动把它挂载进容器。通过厂商和设备 ID，或检查 `/sys/bus/pci/devices/*`，是可以检测是否运行在带 gIB 的 GCP 机器上的。Google 和 Nvidia 已表示开始研究此事，并已有改进计划。

在更高级的网络能力上，GCP 为大规模训练提供了一项关键功能：NCCL 掉队者（straggler）检测，由其 CoMMA（Collective Monitoring and Management Agent）驱动。在数百或数千块 GPU 的分布式任务中，单个表现不佳的节点即「掉队者」就可能拖慢整个集合通信。诊断掉队者的位置是重大挑战。CoMMA 尝试用一个精密的、基于 eBPF 的代理以无侵入方式追踪 NCCL 操作来解决这个问题。通过监控 `AllReduce、AllGather 和 AlltoAll` 等集合通信的进度，它声称能识别出具体哪些 rank 落后。检测到掉队者时，CoMMA 会向 Cloud Logging 发出详细的 JSON 载荷，不仅指出慢的 rank，也指出正常推进的 rank。客户对 CoMMA 的反馈褒贬不一。

存储性能稳健，容量灵活。GCP 的工具自动准备了一个 FIO 基准测试任务，我们运行它来测试 scratch 写入、训练数据读取和检查点写入等 I/O 模式，主目录和 lustre 挂载都交出了扎实的结果。Google 还有一个包含 Weka 等方案的市场，以备客户有部署偏好。当然，GCS 也可按需使用，许多企业本来就把数据长期保存在那里。

当然，没有哪种云体验是没有复杂性的。我们遇到的主要障碍是一个经典的云 IAM 大坑。尝试运行 torchtitan 训练任务时，我们的 pod 被拒绝访问 GCS 桶中的数据集。这需要诊断节点池的 service account，并运行一系列 gcloud 和 gsutil 命令来授予必要权限。虽然这对经验丰富的 GCP 用户是常规操作，但这是与超大规模云厂商打交道必须承受的取舍。

GCP 对生产级 AI 负载的重视，从 [GKE Inference Gateway](https://cloud.google.com/kubernetes-engine/docs/concepts/about-gke-inference-gateway) 正式 GA 可见一斑。我们对 GKE Inference Gateway 的评估聚焦两个特性：预填充-解码（PD）分离和前缀感知路由（prefix-aware routing）。我们发现，官方宣传可带来潜在 60% 吞吐提升的 PD 分离，并未集成到标准 GKE Quickstart 配置或文档中。它目前以「高级优化」的形式存在，处于「持续开发中」。

相比之下，GKE 的前缀感知路由实现成熟且文档完善。常见方案需要一个用户自管的代理，把请求路由到 vLLM 或 SGLang 等推理引擎以复用 KV 缓存；GKE 则把这一路由逻辑直接集成进其托管 L7 负载均衡器。这一设计从服务栈中移除了一个用户自管组件，降低了运维复杂度。GKE 提供了稳健的推理网络层，但其稳定、集成的特性（如托管路由）与文档尚不完善的能力（如基于 llm-d 的 PD 分离）之间界线分明。

监控方面，Google 把 DCGM 指标直接集成进主集群仪表盘。与单独的 grafana 实例相比，这是很好的体验：authN 和 authZ 自动接入部署集群的同一个直观控制台。这还支持一些定制。我们建议通过 DCGM_FI_PROF_PIPE_TENSOR_ACTIVE * peak_fp8_flops 增加一个 TFLOP 估算器。例如对 H200 而言，该值为 1979 TFLOPS。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/f1c1f0c4-32da-479b-8692-765a865157b9_935x479.png)
*来源：Google Cloud*

健康检查方面，Google 的 slurm 产品缺少后台健康检查程序。目前他们依赖一个运行若干 dcgm 测试的 prolog 健康检查，但尚未将其集成为 slurm 中的 NodeHealthCheck 程序，以便在批处理任务运行期间做监控。相比之下，GKE 允许用户配置 AutoRepair，还提供「修复与更换」功能的 API，用户可以请求更换。这是一套强大的响应式方案，但需要客户的集群管理员手工配置，达不到黄金和白金级 Neocloud 在健康检查上展现的主动性水平。我们鼓励 Google 向一些竞争对手看齐，用这样的视角看待故障：如果客户先发现了问题，那就说明哪里出了岔子。

我们与 Google 工程团队的合作体验非常出色，但代价高昂。获得高级支持通常需要一份数百万美元的算力合同，外加 3% 的溢价（针对最低 $1M 的消费），这构筑了高准入门槛，与 Neocloud 直接对比时差异一目了然。

展望未来，我们对 Google 数据中心里的 NVL72 机柜级架构有所顾虑。出于供电、散热、网络和可靠性方面的考虑，Google 和 AWS 都选择了 NVL36x2，而非真正的 NVL72 机柜。其结果本应与 NVL72 相当——拥有与标准 NVL72 机柜相同的 72 GPU 纵向扩展域——但由于跨机柜 NVLink ACC 线缆，它是一种不同的拓扑。

![网络示意图
自动生成的描述](https://substack-post-media.s3.amazonaws.com/public/images/3eccc5d0-4ca5-458e-85f9-42dcef9b2797_936x1187.png)
*来源：SemiAnalysis GB200 硬件架构*
![电脑截图
自动生成的描述](https://substack-post-media.s3.amazonaws.com/public/images/73f31e58-83f7-4bae-aa39-7ee1bd8cbccb_936x572.png)
*来源：SemiAnalysis GB200 硬件架构*

但在实际中，GCP 或 AWS NVL36x2 的用户要多等数周甚至数月才能拿到稳定固件，把机柜调稳到能跑基本集合通信的程度。

![Google 分享面向 AI 云平台的液冷 NVIDIA Blackwell GB200 NVL 机柜照片](https://substack-post-media.s3.amazonaws.com/public/images/b25cb704-5eb8-4a14-9a71-6ff33e17426b_668x1001.jpeg)
*来源：一台 NVL36x2 工程样机，来自 Google 的 Twitter*

总之，Google 有志于树立标杆并获取溢价定价，但 gIB 工作流、缺乏 GA 的托管 slurm 服务、NVL72 机柜级稳定性方面的报道问题，以及不明确的 SLA + SLO 等瑕疵，使当前定价难以令人信服，尤其是对用户中仍然大受欢迎的老款 H100 实例而言。不过，随着行业跨过 H100，Google 的路线图显然强劲。一旦他们大规模推出 B200 和 GB200 实例、并把若干路线图项目推进到 GA，他们将有充分的实力支撑这份溢价。Google 正走在通往黄金级或更高级别的快车道上。

### Amazon Web Services（AWS）

我们在这家全球最大的云上的体验充满头痛。AWS 提供 SageMaker Hyperpod Slurm 和 SageMaker Hyperpod EKS（kubernetes）。我们从 slurm 开始。有意思的是，AWS 与 OpenAI 签署了一份为期 7 年、价值 $38B 的多年协议，让 OpenAI 在搭载 NVIDIA GB200/GB300 的 AWS EC2 UltraServers 上运行核心 AI 负载，但公告中对 EFA 或 HyperPod/Slurm 只字未提。

我们最初按主文档路径、通过 SageMaker 控制台创建 slurm 集群。这条路被证明是条死胡同。成功开通可用集群的唯一方法，是抛开标准文档，改用 AWS 官方 workshop（http://catalog.workshops.aws/sagemaker-hyperpod）里的一个 CloudFormation 栈。该方法会先预置全部所需的基础设施栈——包括 VPC、IAM 角色、S3 桶和 FSx for Lustre 文件系统——再尝试创建集群本身。实际上，默认控制台流程并不能正确配置必要的依赖。

话虽如此，要让 CloudFormation 脚本正确工作，还需在多份文档间穿梭——修正 IAM 策略（AmazonSageMakerClusterInstanceRolePolicy）、申请各种配额、上传并运行生命周期脚本。值得注意的是，这些脚本埋在一个毫不相干的 GitHub 仓库的五层目录深处：<https://github.com/aws-samples/awsome-distributed-training/blob/main/1.architectures/5.sagemaker-hyperpod/LifecycleScripts/base-config/lifecycle_script.py>，而且极其脆弱。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/9cc47afa-5361-46ec-9d5b-3b30bd0aa740_937x421.png)
*来源：AWS*
![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/63f48c6d-8d31-4976-8fd1-698756843dc8_937x362.png)
*来源：在 AWS 控制台上为我们自己申请并审批配额*

这些脚本必须从 git 仓库手动下载、上传到 S3 桶，然后在配置集群的第四步添加进去。在创建 VPC、IAM 角色、S3 桶和 Lustre FSx 时，一旦漏掉某一步或需要把脚本上传到不同路径，整个开通流程就得重来。

第一次尝试，我们没有定义足够的控制器节点来支撑 4 节点的 ml.p5en.48xlarge（H200）集群。第二次尝试，4 个节点中有 1 个因竞态条件未能正确挂载 Lustre FSx，整个集群回滚。第三次尝试，控制器节点所需的实例规格在该区域/可用区已售罄，只能回滚重试。终于，在第四次尝试中，通过指定控制器虚拟机规格（用 c5.xlarge 而非 m5.4xlarge）、并严格一次只加一个节点，我们才成功开通集群。单个集群的开通过程可能耗时约两小时，因为每个节点的部署可能需要 30 分钟以上（前提是有容量）。

前后加总，我们连续 14 个小时扑在这套集群的开通上，其间接到五位 AWS 工程师跨越不同时区的间歇性来电。值得注意的是，那个必须逐节点添加的 Lustre FSx 竞态条件，AWS 工程师知道已超过一年，却始终未修。调研期间我们与三家不同的 AWS 客户交谈，他们证实搭建 hyperpod slurm 集群时遇到过一模一样的问题。

此外，按标准文档路径上手单个 GPU 实例，实际上根本得不到一台能用的 GPU 实例。按控制台指南操作，开通出来的 GPU 实例没有安装任何 Nvidia 驱动，默认根卷只有 8GB，连手动安装所需驱动都不够。我们认为，这正是 lightning.ai、Qubrid 等在 AWS 数据中心里转售 GPU 算力的各类市场平台能维持生意的主要原因：AWS 的 UI 实在太难用了。

在 HyperPod 集群上，AWS（和其他超大规模云厂商一样）取消了公网 IP，改用一个专有的 SSH 包装脚本 easy_ssh.sh <https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-run-jobs-slurm-access-nodes.html>。遗憾的是，这个 easy_ssh.sh 一点都不 easy：Access Token 默认每 24 小时轮换一次，必须从 AWS 控制台重新获取，访问走的是 AWS SSM 方式。这既浪费时间又令人恼火，更别提用 add_users.sh 管理用户、或把集群接入 IAM 供应商的流程了。

独一无二的是，AWS 是唯一一家让客户经理为一块他们直接提供给我们测试的容量区块（capacity block）不断纠缠我们一位团队成员催款的云。虽然问题最终得到解决，但这段经历说明 AWS 这个组织是个庞然大物，客户必须用力推，才能让左手和右手说上话。

除我们的直接测试外，多家部署数百块 GPU 的 AWS 用户的独立反馈还突显了其他问题：需要 /16 CIDR 以避免 IPv4 耗尽（因为每个 GPU 实例要消耗 81 个 IP），以及 EKS 缺乏 IPv6 支持。常见的大坑还包括 HyperPod 不会自动使用既有预留——这是集群可能被迫重建的又一个原因——以及另一种（但同样令人恼火）逐节点添加的必要性，这次是为了避免 EFA 错误。

健康检查方面，与其他超大规模云厂商相比，AWS 的方法确实相对全面。然而，深度健康检查可能长得离谱（60-120 分钟），为了更快扩容最好将其禁用。遗憾的是，除了标准的手工开源工具外，面向 slurm 或 Kubernetes 集群健康、性能和任务统计的监控仪表盘基本不存在。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/441d976b-d94a-4dc9-9a26-b22bb93ebf2d_936x645.png)
*来源：AWS 深度健康检查 https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-hyperpod-eks-resiliency-deep-health-checks.html*

最后是网络。自上一篇文章以来变化不大。AWS 对在所有 H200、B200、B300、GB200 NVL72、GB300 NVL72 乃至未来 VR300 机柜级架构上坚持用 EFA 依然坚定不移。那些从 InfiniBand 和高端 RoCEv2 部署中获得过更优性能的客户，普遍不喜欢 EFA 的性能和调试体验。但 AWS 对 EFA 的执着毫不动摇，甚至设计了这样的未来架构：在计算托盘与一整柜塞满定制 K2V6 EFA NIC 的独立「JBOK」（Just a Bunch of NICs）机柜之间走 PCIe 连接。

在 GB200 上，他们的 p6e 平台采用 NVL36x2，并遭遇了与 GCP 相同的 NVLink 可靠性麻烦——跨机柜 NVLink ACC 线缆引发重大问题。

![Amazon Web Services 为下一代 Nvidia GPU 开发散热技术 - DCD](https://substack-post-media.s3.amazonaws.com/public/images/cd6e31a4-8405-45e5-8dd5-1688fcb33c7b_936x491.jpeg)
*来源：AWS*

AWS 把这种解耦设计包装成面向可靠性的战略选择，声称它实现了 N+1 NIC 冗余，并通过把娇贵的光模块移到更凉爽的专用托盘来提升其平均无故障时间（MTBF）。然而工程现实表明，这一举措与其说是选择，不如说是被逼无奈：在密集的 1U 计算 sled 里塞进多块高功耗 K2V6 NIC，热与空间的约束使然。该架构引入了来自 PCIe 有源电缆（AEC）重定时器的不容忽视的延迟，在我们看来像是一种复杂的变通。

不过，这种 JBOK 设计也促成了一次早该完成的转向——轨道优化（rail-optimized）网络拓扑，这对重 All-to-All 集合通信的 MoE 模型性能至关重要。但这种对元器件级可靠性的执念，导致了系统级上令人震惊的低效运营模式。一整柜 GB200（或逻辑机柜，因为 AWS 和 Google 一样选择了 NVL36x2）被当作一个名为「Ultraserver」的单一故障域。这意味着单个计算 sled 故障，就必须先排空机柜内全部 18 个节点的负载，才能尝试维修。这与客户从其他 GB200 NVL72 机柜级供应商那里获得并期待的免工具热插拔可维护性形成鲜明反差。最坏情况下，该策略对 TCO 的影响极为残酷：为维持容量 SLA 需要整柜整柜的「备件」机柜，而这份成本不可避免地通过糟糕的 SLA 赔付或更高价格转嫁给客户。

对 EFA 用户来说，调试也异常艰难。首先，在使用 InfiniBand 或 RoCEv2（融合以太网）的传统 HPC 环境中，工程师有一套标准工具箱：ib_write_bw、ib_ping、ibv_devinfo 和 ibdiagnet，可直接测试物理层。而在 EFA 上，你的访问权限到宿主机的 EFA 驱动为止。其次，由于 NCCL 不直接与 EFA 通信，要应对多层抽象。通信路径是一长串软件垫片：

*NCCL → aws-ofi-nccl 插件 → Libfabric API → EFA Libfabric Provider → RDMA Core Library 中的自定义 ibverbs provider → EFA 内核驱动 → AWS 硬件*

当一个 NCCL 集合通信（如 AllReduce）挂起或性能不佳时，错误信息往往很泛，比如超时或 provider 错误。定位问题源头是一场噩梦：是 NCCL 本身的 bug？是 aws-ofi-nccl 插件的不兼容或 bug？是 Libfabric 配置错误或撞上边角案例？是 EFA provider 遇到了 SRD 协议问题（如拥塞、重传）？还是 NIC、交换机或线缆的物理硬件问题？没有针对每一层的深度内省工具，调试就变成了管理一堆 AWS 支持工单的过程。

第三种是「灰色故障」（gray failure）的情形：任务性能因莫名的原因劣化。是我们集群上其他任务造成的拥塞？是次优的路由策略？是同一全局 fabric 上的吵闹邻居租户？多租户在网络中从来都难处理，GPU 集群的后端互连也不例外。

最后，集群设置的那些易用性问题同样会影响网络体验。安全组、IAM 权限和集群置放群组（Cluster Placement Group）都必须正确处理，才能确保用户获得应有的性能。许多小事加在一起，就成了管理员的大麻烦。

总体而言，我们尽力反映客户的真实体验，而客户一再告诉我们：EFA 在大规模下表现不佳。但 AWS 不在乎，他们不会向 Nvidia 低头去采用 CX-7 或 CX-8 NIC。他们已经在这块 EFA NIC 上砸了太多时间和精力，非把它弄成不可，非要省下那 0.8% 的 TCO 不可。

总体而言，Amazon SageMaker HyperPod 的难用程度令人惊讶，尤其是考虑到 AWS 是云计算行业的领导者、并以「客户至上」自我标榜。AWS 官方文档难以跟随或干脆是错的，底层平台在大规模下的易用性和性能也存在问题。对于正在考虑 HyperPod 的团队，我们建议为集群维护预留大量工程投入预算，包括构建能绕开 AWS 独有限制的自定义自动化所需的时间。

### Scaleway

Scaleway 继续巩固其利基定位：一家高端的主权欧洲云供应商，专注于大规模 AI 训练，尤其面向初创公司和非营利组织。

该公司面向高端 AI 的主打产品完全围绕用于训练的 slurm 展开。推理和 Kubernetes 总体上不是其未来战略的重心。最近的一项重大改进是部署了一个「copilot」Grafana 实例，包含关键的 DCGM 和 slurm exporter。这直接回应了我们在本文第一版中对其产品缺乏监控的批评。此外，Scaleway 通过 slurm prolog 和 epilog 脚本实施健康检查来增强可靠性，并对监控数据做主动管理以确保集群稳定。

![计算机程序截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/f8b85c85-be81-4b4f-b116-deca7acebb4d_935x598.png)
*来源：Scaleway*

网络方面，Scaleway 继续主要提供配备 Nvidia Spectrum-X 网络的 H100 节点。他们通常会为客户提供预留集群数天或数周的机会，将其性能与传统 InfiniBand 对比，并见到了良好结果。有意思的是，测试期间 Scaleway 与某客户合作开发了一个优于 nccl-tests 的合成基准，显示相对 InfiniBand 有 20% 的性能提升。然而，在一个关键的真实负载案例中，这一性能优势并未兑现。

展望未来，Scaleway 的 Blackwell 计划仍处规划阶段，且只瞄准 HGX B200/B300 基板，而非全整合的 GB200 NVL 系统。公司也在探索 AMD GPU，但在欧洲尚未看到显著的客户拉动力。

总体而言，Scaleway 的商业模式已开始体现出主权、符合 GDPR 基础设施的「欧洲溢价」。其资源分配方式便是明证：大规模任务要求客户整集群签约，而非允许按需使用单台 8 卡 GPU 机器。这一模式瞄准资金充足、态度严肃的 AI 项目，包括围绕 Scaleway Startup Program 构建的生态。该计划提供抵扣额度和支持，旨在服务下一代欧洲科技公司。

我们预计 Scaleway 将继续在稳固的利基市场中经营，优先为欧洲市场提供专用高性能集群，并附带相应溢价。

### Cirrascale

Cirrascale 在市场上占据着一个独特、且多少令人困惑的位置，因此落在我们的白银级。该公司的云服务按订单构建（build-to-order）运营，这种模式更像高接触的托管（colocation）或系统集成服务，而非传统云产品。他们的服务包括租转购（rent-to-own）方案，以及帮客户采购服务器（例如从 Supermicro）的服务——服务器归客户所有，Cirrascale 收费提供托管、上架配置和 RMA 协调。这与大多数其他供应商的做法有本质区别，或可类比 Lambda 的 Private Cloud 业务、Fluidstack 的部分协议，以及 STN 的托管服务。

我们与 Cirrascale 团队的打交道经历颇有挑战。Cirrascale 团队认为我们的标准——尤其是围绕 Kubernetes 等软件编排的部分——与他们的客户无关。他们的理念是不承担平台层的任何责任，即只提供裸金属访问，期望客户自带并自管软件栈。然而，在与 Cirrascale 客户的交流中，我们听说他们其实并不喜欢这种方式。把一个简单的 DCGM 后台健康检查集成进 Slurm 环境、并接入数据中心运营系统，就能更快地诊断问题，在训练运行中获得更多有效产出（goodput），还可能为 Cirrascale 省 RMA 的时间与金钱。

虽然 Cirrascale 已部署数千块 GPU，并在新 B200 和 AMD MI355X 系统上拥有大量客户积压订单，但其市场地位也经历了显著变动。值得注意的是，曾在 Cirrascale 托管其全部自有服务器的 OpenAI，已将整套基础设施迁往 Microsoft Azure。这家旗舰级 AI 实验室从客户自有/受管托管模式转向超大规模云厂商，是行业方向的一个有力风向标。

总之，Cirrascale 服务一个特定利基：希望拥有硬件资产、但把数据中心运营的复杂性外包出去的组织。然而，他们对软件栈的放手态度，使我们很难把他们推荐给期待可靠、省心集群的团队。这一模式给客户压上了沉重的运营负担，也坐实了 Cirrascale 的白银级位置。

### GCORE

GCORE 是一家总部位于卢森堡的供应商，成立于 2014 年，最初专注于游戏、CDN 和通用云。但现在，是 AI。GCORE 在全欧洲提供 GPU，数据中心位于卢森堡、葡萄牙、德国、荷兰、英国和美国（弗吉尼亚州和加利福尼亚州）。他们还有进军北欧的计划，部分通过自建，也通过与 Northern Data Group（又名 Taiga Cloud）的既有合作。这一合作走向如何尚不明朗，因为 Northern Data 显然刚因 2023 年加密货币挖矿业务相关的税务欺诈指控被突击搜查了办公室。

GCORE 平台功能丰富，在易用性与底层硬件性能之间取得了不错的平衡。遗憾的是，我们只测到了 Kubernetes。事后我们才得知，他们基于 SOperator 的 Slurm-on-Kubernetes 方案[埋在 API 文档里](https://gcore.com/docs/api-reference/cloud/managed-kubernetes/create-k8s-cluster#body-add-ons-slurm)。我们期待未来测试它。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/b200cc78-4890-4c38-90ad-cb7e86ac6a8d_937x510.png)
*来源：GCORE 控制台（另注：我们希望 AWS 控制台长这样）*

上手流程从一连串人工关卡开始，我们很快意识到面对的是一个仿照超大规模云厂商打造的企业级控制台。创建账户后，我们需要申请提升配额才能开集群。有意思的是，在超大规模云厂商那里我们自己就能批准这些配额提升，而在 GCORE，是一位无名无脸的支持团队成员替我们做决定。结果，为了给我们的 2 节点 kubernetes 集群配上 2TiB VAST 存储，我们前后尝试了三次（跨越两个工作日）才获得配额批准。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/6c9e9284-6f8d-4ddd-b2fa-9f67e6a4e21d_937x495.png)
*来源：GCORE*

硬着头皮继续，我们按要求走完流程：创建三个虚拟网络、一个 VPC、开通 Kubernetes 集群——结果集群在「provisioning」状态卡了两个多小时，最终失败。值得注意的是，GCORE 对网络很较真：路由器、可配置网络、浮动 IP、防火墙、保留 IP 一应俱全。只是对非云原生用户来说，这些会让初始设置变得混乱。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/eae21b51-4c1b-4fe1-a0ea-7aae893b1734_937x505.png)
*来源：在 GCORE 上为我们的 Kubernetes 集群配置路由器*

第二次尝试更成功，至少表面如此。集群正确启动，包括用我们费尽周折争取来的 VAST 配额建好的默认 ReadWriteMany StorageClass。遗憾的是，集群交付时没有预装 Nvidia GPU Operator 或 Network Operator。这是许多有 kubernetes 经验、但在转向 AI 市场时漏掉一些基础的通用云的关键问题。有些观点（比如预装 GPU 和 Network Operator）是值得在客户集群上强制执行的。

在确认 nccl-tests、torchtitan 预训练任务以及经 llm-d 部署的预填充/解码分离推理端点性能符合预期后，我们转向监控。遗憾的是，这部分似乎完全留给用户自理。黄金和白金级供应商会负责 CNI、CSI、主动/被动健康检查（例如通过 node-problem-detector 或自定义控制器与 CRD）、kube-prometheus-stack（即 Grafana 仪表盘）以及 Slurm-on-Kubernetes，而 GCORE 把这些统统丢给用户。

总体而言，GCORE 平台实力强劲，是我们测试过的最佳纯自助 kubernetes 产品之一。控制台具备人们期待的所有企业级特性，这也解释了他们为何能凭借 PCI DSS 合规和全球数据中心足迹打入大企业。我们鼓励 GCORE 开发高级集群监控仪表盘，在 kubernetes 层实施主动/被动健康检查，并考虑随时间打磨出一流的 Slurm-on-Kubernetes 体验。

### Firmus / Sustainable Metal Cloud（SMC）

Firmus 是一家澳大利亚公司，最近获得 Nvidia 的战略投资，估值 $1.9B：<https://www.afr.com/technology/nvidia-backs-australian-ai-factory-firmus-with-1-9b-valuation-20250915-p5mv0v>。他们当前的雄心是打造「南半球的 Stargate」，特别聚焦 GB300 NVL72 和 VR 等下一代机柜级系统。虽然我们认为 Firmus 在浸没式冷却上的大部分经验走错了方向、如今已被浪费，我们也相信这个团队是业内少数几家具备工程功力、能有效监控和维护这些 DLC（直接液冷）系统物理层的团队之一。我们审查了他们针对浸没式部署的遥测与故障预测系统，其对细节的关注、以及对物理栈的深刻理解令人瞩目——深入到定制光模块和光缆中的信号质量与光功率电平。然而，这种最低物理层的功力，却可能被一个与客户需求脱节的高层 UX 拖后腿。

我们的测试从一开始就遇到一道难题：集群访问被强制 VPN 挡在门后。对于习惯了带公网 IP 或精简 SSH 包装的标准云工作流的团队来说，这是重大的运营瓶颈。虽然一些安全敏感客户（如国防、情报和科研领域的国际联邦机构）可能接受甚至偏好二层、三层、五层或七层的隔离，普通大众可不这么干活。Firmus 没有准备任何替代访问方式，这在我们看来很说明问题。

连上之后，我们的 slurm 环境也存在一些配置问题。标准的 topology.conf 未做拓扑感知调度设置，一条简单的「srun -N1 –gpus-per-node=8 –pty bash」命令因超长 prolog 耗时一分多钟才执行完。Firmus 团队似乎把我们此前关于健康检查的反馈推向了极端，把 prolog 塞满了不必要的 dcgm level 3 检查——其实 level 1、2，或配置好 HealthCheckProgram 的一个 epilog 就足够了。值得肯定的是，集群预置了 nccl-test 脚本，跑出了预期带宽。

如前所述，Firmus 的监控技术栈独树一帜，超越标准 DCGM 指标，将数据喂给 ML 模型以在组件故障发生前进行预测。「链路抖动」被正式定义为一小时内五次事件，触发自动诊断。他们的内部验证套件详尽彻底，在备用节点上运行回归测试，包括 P2P 带宽测试、GDR 拷贝、小规模 llama 训练和 NCCL 测试，以主动识别临近故障的 GPU、NVLink 或 InfiniBand 互连。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/11a1344a-e46a-49c1-aeca-da6c023cb9f7_894x392.png)
*来源：Firmus 浸没罐定制监控仪表盘*
![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/f610ff4e-5907-4f66-aaa4-104c67fe15a0_937x454.png)
*来源：Firmus 定制 Grafana 仪表盘，展示一次训练运行期间的相关 GPU 利用率指标*

这种物理层监控投入，是 Firmus 计划支撑其激进的「99.94% SLA」的方式——通过保障最大有效产出来与竞争对手拉开差距，这与我们从 CoreWeave、Nebius 等顶级供应商那里听到的说法一致。他们的商业模式与其他大型 Nvidia 云类似，为即将到来的机柜级部署给出了诱人的预期定价，其中很大一部分得益于其向塔斯马尼亚大规模扩张带来的低电力成本。我们鼓励 Firmus 继续专注于从物理层到编排层（即配置妥当的 slurm 和 kubernetes 集群）的卓越运营，不要被当红厂商兜售的花哨 PaaS 和 SaaS 应用分心。

### GMO Cloud

GMO Cloud 隶属于庞大的日本企业集团 GMO Internet Group，呈现出一套高度自成一体的做法，瞄准其本土市场。该产品建立在安全之上，其严格程度在我们看来已经改变了用户体验，但性能依然扎实。

由于 kubernetes 不可用，我们聚焦 slurm，很快发现 sinfo 和 scontrol 对终端用户完全禁用。这一决定大概是以安全为名做出的，却给我们依赖 scontrol show hostnames $SLURM_JOB_NODELIST 等基础便利功能的预置脚本带来了麻烦。它还迫使我们修改一些标准调试流程，因为用户无法查看集群状态或拓扑。所幸 GMO 提供了便利命令「snodes」和一个自定义脚本「get_master_addr.sh」，让我们以预期性能跑起了任务。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/47e14b4a-62b3-45c7-aee1-abea36895992_790x481.png)
*来源：SemiAnalysis 使用 GMO 便利脚本*

除了这些便利脚本，还出现了其他一些易用性问题。GMO 没有配置 topology.conf，理由是：他们手动把客户集群分配给不跨 Spectrum-X leaf 交换机的服务器，并按已知主机名组织一切，因此 slurm 层的拓扑感知是多余的。我们认为这暴露出其缺乏运营大型客户集群、以及在大规模多租户环境中处理硬件故障的经验。

因聚焦安全而强推非标准工作流的主题，延续到了他们的容器化策略。该环境不支持 Pyxis 和 Enroot，实际上堵死了已在基于 Docker 的容器上标准化的团队。用户必须围绕 Singularity 重建整套工作流——这是一项不小的工程，也为新用户竖起了又一道门槛。

遗憾的是，这种对安全的专注在最基本的层面也会掉链子，形成一个奇怪的悖论。一方面，没有任何已知漏洞利用的简单命令行工具被锁死；另一方面，我们发现了过时的软件包——登录节点和计算节点上的 nvidia-container-toolkit 分别是 1.16.2 和 1.17.4 版。虽然 GMO 承认这些已被其内部漏洞扫描器标记、并已列入更新计划，但崭新的集群上跑着受 9.0 严重级（Critical）CVE 影响的旧软件，与面向用户的种种限制形成鲜明反差。总体而言，GMO 的做法在我们看来像是一场安全表演（security theater）。

好的一面是，基础环境为 HPC 任务配置得相当到位。节点预装并配置好了 HPC-X、NCCL 和 nvcc，从源码构建 nccl-tests 并跑满预期带宽易如反掌。我们也在 torchtitan 任务上达到了预期 MFU。此外，标准的 dcgmi health -c 程序被正确配置为 Slurm HealthCheckProgram，满足了我们对后台健康检查的期望。

最后，该平台缺少关键的可观测性与可靠性特性。没有监控仪表盘——不过 GMO 表示未来版本已规划基于 Grafana 的方案。目前，用户只能依赖基础的 Slurm 邮件通知了解任务状态，我们也未能识别出任何主动健康检查体系，故障检测的负担大部分落在用户身上。

总体而言，GMO 在日本国内建立了明显优势，尤其考虑到该地区对 Slurm 等传统 HPC 技术的依赖。支持力度强劲，我们预计 Turing：<https://group.gmo/news/article/9501/> 和 AI Robot Association（AIRoA）<https://internet.gmo/en/news/article/45/> 等样板客户信任该产品，因为 GMO Cloud 是国内领导者。我们建议 GMO 把重心放在易用性而非安全表演上，通过定制 Grafana 仪表盘改进用户的监控选项，改进被动与主动健康检查，并考虑未来开发 kubernetes 产品。

### Vultr

先说个开场：Vultr 创下了本轮 ClusterMAX 的纪录——启动会议一口气来了 12 个人。Vultr 去年以 $3.5B 估值完成融资，投资方包括 AMD Ventures，今年夏天又拿到了 $329M 债务融资。如今，Vultr 在其 32 个全球区域中的一部分提供 AMD MI355X GPU（由 AMD 兜底）和不断扩充的 NVIDIA GPU 机队（包括 HGX B200）。

![网站截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/134631bf-ecf8-4abf-9216-b4445ce7626e_936x598.png)

我们开始测试时，Vultr 的 SLURM 服务看起来还很新，像个控制台里的二等公民。登录之后也确实如此。集群缺 pyxis、hpcx、topology.conf，默认登录用户是「root」（且没有默认工作目录）。最重要的是，没有共享主目录文件系统。我们建议了一些基本修正，很快改用「ubuntu」用户、默认工作目录切到共享的 /mnt/vfs，一切顺利起步。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/b36e8c64-9698-483e-9d32-c10253107baf_477x244.png)
![计算机程序截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/5661a17e-509b-4500-bc40-1a8c7ea32f01_694x314.png)

最终，我们让 nccl-tests 跑到了预期带宽，一些基础 torchtitan 训练也达到了预期 MFU。

接手我们的 kubernetes 集群时，不幸发现拿到的 NVIDIA GPU Operator 和 Network Operator 版本已超过一年未更新，意味着它们受三个独立「critical」级 CVE 影响，例如 Wiz 发现的 NVIDIAScape：<https://www.wiz.io/blog/nvidia-ai-vulnerability-cve-2025-23266-nvidiascape>。我们建议升级，团队回复说他们「正在写 jira」。

测试期间，我们遇到一些间歇性链路抖动，最终自行消失了。遗憾的是，由于缺少监控仪表盘、集群互连上也没有任何主动或被动健康检查，此事既没有主动通知，也没有任何修复处置。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/5750b6c8-290f-4cfe-98de-4292ed80da61_935x800.png)

在 kubernetes 集群上让 nccl-tests 跑满带宽之后，我们与支持团队协作排查集群上的一个训练任务。团队成员之一 Enis 对 KubeFlow 相当熟悉，装好它并配置了一个示例 torchtitan 训练任务在其网络上顺利运行。我们对此印象深刻！

![电脑屏幕截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/cbd41255-92a5-4296-b599-aac95d1f3c9d_937x272.png)
*来源：一幅美景*

转向推理后，VKE 表现强劲。Vultr Cloud Controller Manager 作为 Vultr 托管控制平面的一部分运行（在集群内不可见），负责自动开通 LoadBalancer 公网 IP 等资源。默认安装的 helm chart 合理，配置新 chart 也很容易，这要归功于预先配置好的默认 ReadWriteMany StorageClass。

根据我们的反馈，Vultr 已加入 NVIDIA 预披露（embargo）计划，以确保未来安全漏洞能提前获知。Vultr 对 AMD 产品安全办公室（Product Security Office）的主动接触，似乎也促使 AMD 自行建立了类似的安全预披露计划。

我们欣赏 Vultr 对改进的承诺以及其工程师的直接参与。我们建议他们着手开发监控仪表盘、主动与被动健康检查，并继续积累大规模 GPU 集群的运营经验。

### Voltage Park

Voltage Park 是一个绝地翻身的故事。如果这次评测是在 2023 或 2024 年，情节会大不相同。我们评的是现在的 Voltage Park，而现在的 Voltage Park 是一家实力已然不算弱的供应商，专注于 H100 GPU。截至我们测试时，其按需容量似乎经常售罄。公司正快速迭代功能，包括最近推出的 SLURM 服务和 Kubernetes 的 OIDC 集成。Voltage Park 提供业内最低的价格之一。

我们最初使用 slurm 的经历包括大量开通难题，多次尝试才把测试集群跑起来。开通之后，我们会被负载均衡到不同的登录节点，并遭遇如今已成经典的 SonK 问题：没法运行代码。没有 git、vim、nano，也没有 sudo 权限。不过，Voltage Park 是唯一一家似乎自知存在这些 SonK 问题的供应商，他们建议用 kubectl exec 命令进入登录 pod，而不是原先经公网 IP 的 ssh。这种容器优先的方式帮我们绕过了最初的 root 权限问题，但安装软件仍需时间，而且一旦连接被重置，所有已安装的软件都会消失——换句话说，登录 pod 是无状态的。Voltage Park 工程团队承诺为登录 pod 构建一个新容器镜像，内置运行 slurm 任务和编辑代码所需的软件，并在不到 24 小时内交付了承诺。这种对客户支持的投入令我们印象深刻。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/d2fc1fb9-c6d2-42d6-8bb7-f0de9e07b378_937x442.png)
*来源：在 Voltage Park 直接从控制台启动一个 SonK 集群*

在预期的容器环境中，配置就扎实多了。我们发现了为网络感知调度正确配置的 topology.conf、到位的 SLURM prolog 和 epilog 脚本，以及装有 pyxis 和 enroot 的现代容器工具链。互连性能强劲，集合通信跑出预期带宽。下载速度也不错，共享文件系统相当快。

运营层面，我们遇到两个主要担忧。首先，Voltage Park 的仪表盘有一个区别于「Terminate（终止）」的「Shutdown（关机）」功能。「Shutdown」会停掉实例，但会继续按预留容量计费——这一细微差别在 UI 里交代得并不清楚，我们预计这是一颗迟早要炸的雷。值得注意的是，没有任何其他供应商提供这种「Shutdown」与「Terminate」并存的选项，而且即便与 Voltage Park 团队讨论过「Shutdown」按钮的用途之后，我们仍然非常困惑它的预期用例是什么。我们建议

其次，他们处理按需集群硬件故障的流程是手动的，需要运维人员介入才能把节点从用户集群中轮换出去。这与顶级供应商提供的自动化、有韧性的系统相去甚远。安全补丁不及时也是明证：集群预装的 nvidia container toolkit 版本（1.17.4）已过时 9 个月，如本文前文所述，受 CVE-2025-23266（NVIDIAScape）和 CVE-2025-23267 影响，两者的 CVSS 评分分别为 9.0 和 8.5（满分 10）（均为「Critical」级）。

总之，我们认为 Voltage Park 如今已拥有坚实的技术基础，足以向前走并从声誉问题中恢复。技术团队的执行力令我们鼓舞，期待未来看到更多改进。

### Tensorwave

Tensorwave 是一家最近从 AMD Ventures 融得 $100M A 轮的供应商。因此，他们专注于 AMD 硬件，包括其亚利桑那州图森（Tucson）数据中心里的 8,192 块 MI325X GPU。我们热爱所有 GPU，也钟爱 AMD，因此与 Tensorwave 合作已久——他们慷慨地向我们提供 GPU，用于远超 ClusterMAX 范围的基准测试。我们感谢这份支持。

我们对 Tensorwave SonK 平台的测试表明，它总体上不够稳定。上手流程令人困惑，依赖 Rancher 的 RKE2 开源 kubernetes 发行版（旧称 RKE Government）、Longhorn 做存储，以及一个为正确支持 AMD GPU 而修改过的 Slinky 版本来实现 SonK。登录集群时，我们起初不得不提升到 sudo 才能运行基本的 kubectl 命令、让一个「slurm-login」便利脚本跑起来。为了拿到可用的 kubeconfig，我们与 Tensorwave 团队来回折腾了不少（值得注意的是，现在从控制台下载已经很容易）。我们还遇到权限与用户组的问题——它们似乎未在跳板机与 Slurm 登录节点之间正确同步。这个问题在我们测试期之后也已修复，但很明显，他们在让 RBAC 限权的集群与外部 IAM 供应商对接方面经验有限。此外，Slurm 登录节点缺少我们期待的（如今已成经典的）工具：vim、nano、git 以及运行 apt install 的 sudo 权限。不过在 Tensorwave 这里，团队只用了几小时就修改好基础容器镜像、装上了这些工具。这样的响应速度令我们印象深刻。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/8feae912-04d3-41c6-bae6-0f0236850397_936x561.png)
*来源：我们的 Tensorwave 控制台*

除访问之外，平台上没有拓扑感知调度，健康检查未与 Slurm 集成以自动排空未通过检查的节点，监控仪表盘也缺少 AMD [RDC 软件包](https://github.com/ROCm/rocm-systems/tree/develop/projects/rdc)特有的 GPU 与系统健康关键信息。基于 DCGM 构建的 NVIDIA 供应商起步更简单，而 Tensorwave 因为只做 AMD，很多东西不得不从零搭建。然而最重要的还是可靠性。测试期间，我们经历了多次可靠性问题，其中包括持续数小时甚至数天的宕机。在两个月里，我们经历了 7 次独立的中断：GPU 节点的硬件与固件问题、一次 Kubernetes 重新部署、SonK/slurm-login 连接问题、Weka 存储维护、交换机与路由器维护，甚至还有一次停电。值得注意的是，这些问题没有一个直接与 AMD GPU 相关——问题出在集群的其余部分和 GPU 周边的设施上。

值得肯定的是，Tensorwave 团队始终对我们的反馈响应迅速，并能快速处理我们提出的问题。我们也看到可靠性随时间推移总体在改善。总体而言，需要我们来指导正确的 Slurm 配置、监控和健康检查，这一事实本身就说明他们在运营 8,192 块 MI325X GPU 或更大规模的多租户集群上普遍缺乏经验。我们期待随着他们建设更多 AMD GPU 产能，与 Tensorwave 开展更多合作。

## 青铜（Bronze）

### GMI

GMI 是我们青铜级中排名最靠前的 Neocloud，只是还差一口气。这家公司展现出潜力，近期进展包括通过安全合规认证，以及为 H100 和 H200 节点实现机密计算能力。然而在我们的测试中，其 slurm 集群实在难以使用。

我们没能获得任何自助服务控制台或监控仪表盘的访问权限，从最初提出申请、到多次跟进之后，历时一个多月才最终登录成功。

在集群上，slurmctld 直接运行在一个计算节点上，环境里缺少 docker、modules 工具等基本软件。更严重的是，尽管环境中部署了支持 POSIX/NFS 与 S3 的 VAST，集群开通时却没有配置跨节点的共享 home 目录。经过协商在集群上配置好共享文件系统后，我们发现其性能糟糕透顶：基本的文件保存操作、乃至终端里的回车，都要花好几秒才能完成或响应。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/42dd5b79-c08f-4724-b66a-96d52b6935bd_726x545.png)

我们的一台 GMI 节点，配有 1.9TB 共享存储和 27.9TB 本地存储，与 NVIDIA 的 DGX 规范完美契合

好的一面是，底层硬件针对高性能工作负载的配置看起来是正确的。对 nvidia_peermem 的检查确认 GPUDirect RDMA 已启用，团队也确认其互连网络基于 InfiniBand 构建，并使用 PKeys 做网络隔离。

我们同样没有发现任何主动或被动健康检查的迹象，也没有任何监控仪表盘可供了解集群状态或任务性能。

未来，当我们能确认其 Slurm 服务运转良好、监控仪表盘开发完成、主动与被动健康检查到位、并推出完善的 Kubernetes 服务时，GMI 无疑将是升入白银级别的有力候选者。

### STN

STN 是我们名单上第二家「如果测试表现更好、本应进入白银级别」的供应商。做个类比，STN 与 Cirrascale 类似，也就是说，STN 为按单个客户定制构建（built-to-order）的集群提供专属托管服务。这里没有「公有」云体验，坦率地说，这里面也没多少东西称得上「云」。但想要高接触度（high-touch）服务体验的客户在这里可以得到满足。在我们的测试中，STN 平台被严重的配置错误和可靠性问题拖累，最终落入青铜级别。

上手流程完全靠人工，需要通过电话核对 PDF 文件并开通账户。我们获得了一个 4 节点 B200 集群，硬件令人印象深刻，包括四张网络 fabric（互连与存储各用 RoCEv2）和 25TB 的 VAST。然而，这些高端硬件却被基础配置失误拖了后腿。例如，我们发现每个节点上有七块本地 NVMe 盘未挂载。Slurm 环境也缺少影响性能的关键组件：没有 topology.conf，GPUDirect RDMA 被禁用（nvidia_peermem 未加载），MPI 也没有安装。

不幸的是，STN 最大的弱点是可靠性。测试期间，我们看到两个不同节点进入「down」状态，其中一个「down」了超过两天。由于 STN 的修复流程完全靠人工，客户必须自己发现故障并上报。值得注意的是，节点上虽然启用了 dcgm health -c，但它并没有作为 HealthCheckProgram 接入 Slurm。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/b05aabfe-462f-4d90-a316-c7fb3a17450d_936x230.png)
![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/7d4badd1-4890-4f36-885c-ba0fd43a9958_936x191.png)
*在不同时间点查看我们处于「down」状态的节点*

我们建议 STN 未来把精力放在真正的集群可靠性上，而不是向 Grafana 上报虚假的「正常运行时间 SLA」指标。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/60568609-cfe9-4750-81cc-fc0647b7fd5d_937x457.png)
*来源：截图声称我们已评估过自家 SLA，正在逼近 100%*

最后，让任务跑起来也是一场斗争。STN 工程师花了数周时间修改集群，装上 hpcx、nccl 和 nvcc，启用 GPUDirectRDMA 并关闭 ACS，我们才得以在四个节点上运行基础的 nccl-test 和 torchtitan 训练任务。我们还遇到了疑似 WAN 上的网络流量整形，它拖慢了我们的下载速度，却让 speedtest-cli 的成绩好看得很。

尽管如此，在我们与客户的交流中，STN 已证明他们有能力为客户做深度定制工作。展望未来，我们建议 STN 将其大部分 Slurm 开通流程和健康检查自动化，并开发完善的监控仪表盘以提升可靠性。在那之前，我们认为 STN 仍是一个高风险选择、一家青铜级供应商。

### Prime Intellect

Prime Intellect 是我们最喜欢的「并非 Neocloud、却又恰好也是一家 Neocloud」的初创公司。Prime 最出名的是其去中心化训练（INTELLECT）和合成数据集生成（SYNTHETIC）。他们还推出了一个环境中心（environments hub），迅速成为关注开源 RL 环境的研究人员的首选去处。我们由衷喜爱 Prime 的开源贡献：Verifiers（一个创建 RL 环境的库）、PCCL（一个通过 TCP/IP 运行集合通信的库，即在 WAN 上）以及 PRIME-RL（一个大规模异步 RL 框架）。

测试时，对方为我们提供了一个 4 节点 SLURM 集群，该功能当时仍处于 beta 阶段。我们就一些配置问题给出了初步反馈：没有共享 home 目录、没有免密 ssh、没有预装 MPI、lmod、容器工具链、pyxis 或 enroot。最初尝试启动批处理任务时因 InvalidAccount 错误而失败，通过 torchrun 运行的分布式 PyTorch 任务卡死在主机名解析上，提示存在网络问题。我们还发现缺少健康检查或 dcgmi 集成，也没有可用的监控仪表盘。

![电脑多屏截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/7540cdec-e850-4878-8291-af81ab0fd471_937x490.png)
*在 Prime 上启动一个 slurm 集群*

发现这些问题后，Prime 团队立刻全力行动，彻底重构了配置。不到一天时间，他们就加上了免密 ssh、带 nct 的 docker、enroot、pyxis、NVIDIA HPC SDK（nvcc、mpirun、hpcx）、python3 别名、预装的 uv，以及一个由控制节点托管的 /home 目录 NFS 挂载。

Prime Intellect 的响应速度是此次合作中我们最大的收获之一。从在 Slack 里发出反馈到拿到一个能用的集群，只花了几个小时。未来，我们期待进一步验证其 slurm 服务在拓扑感知调度、自动化健康检查、监控仪表盘以及大规模 I/O 性能上的表现。我们了解到已有一些大客户先行一步，在 Prime 的公开控制台和市场之外、以 1k GPU 规模运行集群。我们对即将推出的 kubernetes 服务也非常期待。总体而言，如果 Prime 团队保持这种狂飙式的新功能交付节奏，我们预计他们将在 ClusterMAX 排名中迅速上升。

### Neysa

Neysa 是一家在印度市场运营的新兴供应商。他们最近与 NTT Data 和特伦甘纳邦政府签署了谅解备忘录（MoU），将在海得拉巴建设一座 400MW、25k GPU 的设施，目前运营着一支 H100、H200 以及即将上线的 AMD MI300X GPU 机队。然而，我们的测试显示，与国际竞争对手相比，其当前平台在安全性和可用性上存在差距。

上手流程让我们对安全性产生担忧。访问通过基于用户名和密码的 SSH 管理，辅以人工 IP 地址过滤和碎片化的用户账户体系。我们无法为团队其他成员创建新用户来进行测试，这意味着他们很难支持对接外部 IAM 供应商的 RBAC。

SLURM 环境本身也存在基础配置错误。最初任务无法运行，因为未配置默认分区（partition），每次提交都必须手动指定。此外也没有配置 topology.conf。如果 Neysa 未来要运行 25k GPU 的集群，拓扑感知调度将至关重要。同样，监控和健康检查实际上形同虚设。测试期间所提供的 Grafana 仪表盘无法工作，而且似乎缺少一些让健康检查或性能监控正常运转所需的 exporter。积极的一面是，容器化工作负载的软件栈是现代的：我们发现了最新的 NVIDIA container toolkit，pyxis 和 enroot 也都已安装。

测试时，Neysa 尚无可供我们测试的 Kubernetes 服务。我们期待未来对其进行测试。我们预计 Neysa 将受益于对印度 DPDP 等法规的合规，但认为他们目前不太可能拓展到本土市场之外。我们鼓励 Neysa 改进其默认体验：更好的安全态势、用户管理、主动式支持体验、默认的监控系统以及健康检查。

![手机截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/304d92fb-1a08-449f-9af4-1fcf61e70ce6_937x442.png)

### Hyperstack/NexGen

Hyperstack 拥有一个轻快易用的 web 门户，我们可以在挪威、加拿大和美国三个区域快速便捷地开通和释放 GPU 虚拟机。他们还接入了 PaleBlueDot.AI 等外部市场，我们在那里得以再次测试。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/b116b492-30b7-47e1-b2f3-4a11e289ca61_937x500.png)

然而，在我们的直接测试中也发现：要么他们的旗舰 Kubernetes 服务存在问题，要么我们赶上了一个容量糟糕的日子。等待三个小时后，我们得到一个含糊的「reconcile failed」错误。系统没有给出任何日志或细节。幸运的是，这次尝试期间我们的账户没有被收取 GPU 时间费用（不像名单上其他某些供应商——后文详述）。

![网页截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/8c9eb707-93bd-4748-8e36-05ea73a8308c_937x498.png)

第二次尝试换了不同 GPU，进展更多了一些。在「Creating（创建中）」阶段卡了 4 个小时后，看起来确实创建了一些机器，也给集群分配了公网 IP。

![](https://substack-post-media.s3.amazonaws.com/public/images/444f9277-628c-48c2-a56d-c4d24e83f31a_937x497.png)
![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/19b91477-1c1a-4bd6-9284-4c34decac75a_937x486.png)
*我们的 kubernetes 集群，在等待点什么发生*

我们鼓励 Hyperstack 修复其 kubernetes 部署工作流中的这一核心问题，让客户能够可靠地在集群中使用其 H100 和 H200 GPU。

### Atlas Cloud

Atlas Cloud 给人的印象有些混乱。其网站把用户引向模型游乐场（model playground）和 Serverless 端点环境，但核心业务却是一家典型的裸金属批发商。Atlas 隶属于一家名为 VCV Digital 的控股公司，姊妹公司 Tiger DC 目前正在南卡罗来纳州建设一座新数据中心。VCV Digital 旗下还拥有加密货币公司 One Blockchain。

公司承认 Atlas 的业务重心正处于转型之中——先是美国转向亚洲，如今又转回来。在我们的测试中，我们无法开通/释放用于测试的 GPU Pod。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/a8960789-7b48-4ce8-af9d-29dbb4da61f2_936x494.png)

尽管如此，我们预计 Atlas 未来将继续在裸金属批发市场运营。我们鼓励 Atlas 参考我们的评级标准，据此规划核心的安全、用户管理、网络和存储服务的开发。最终，我们还鼓励他们考虑发展高级监控、健康检查、编排软件与支持服务，以便在其 TigerDC 站点及其他地方扩展裸金属批发业务。

### BuzzHPC

BuzzHPC 是 HIVE Digital Technologies（前身为 HIVE Blockchain）的 AI 部门，后者是一家聚焦气候凉爽、绿电充裕地区（加拿大、冰岛、瑞典）的加密矿企。HIVE 于 2022 年收购了 GPU Atlantic（又名 gpu.one）位于加拿大新不伦瑞克省的一座 50MW 设施，就此转型进入 AI 云市场。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/aebb0014-9b67-4425-a79e-4b4f91668cd3_936x511.png)
*来源：我们的消息源*

在我们的测试中，拿到的 Slurm 集群几乎一次性集齐了本轮测试中我们见过的所有毛病，简直令人「叹为观止」。清单如下：

- 一开始没有控制面（control plane）机器
- 一开始没有 NFS 挂载，随后用户的默认工作目录也不在共享文件系统上
- 一开始节点之间没有免密 ssh
- worker 节点上未安装 docker 和 nvidia container toolkit
- 未安装 modules，也没有 hpcx、nccl、nvcc
- 没有 pyxis 或 enroot
- 未安装或未启用 dcgmi 后台健康检查
- 未配置 prolog 或 epilog，没有主动健康检查
- 没有监控仪表盘

为了绕过这一切，我们用 PyTorch 自带的 libnccl 跑了一个 2 节点 nccl 测试。遗憾的是，带宽不及预期（大约低了 10 倍）。这很奇怪，因为 ibstat 显示节点里有 8 张 400Gb 的 CX-7。

于是我们很快确认：GPUDirect RDMA 没有安装，ACS 也没有关闭。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/855a2823-51fe-492e-aad4-1d47a4f19b6f_936x478.png)
*BuzzHPC 控制台*

值得肯定的是，BuzzHPC 团队响应积极，与我们连续协作数天解决了我们发现的部分问题。他们还承诺将我们的反馈纳入今后默认的 slurm 服务中。

然而，即便经过这些修复，集群仍未达到我们对可用性、监控和健康检查的预期标准。BuzzHPC 的平台似乎仍处在密集开发阶段。我们期待未来看到 BuzzHPC 的更多进展。

### Shadeform

Shadeform 以 GPU 算力市场的形式运营，而非直接供应商，自己不持有任何 GPU。与其他市场不同，Shadeform 团队精简、融资仅 $200 万，严格专注于自家软件和撮合交易。其平台对可用 GPU 实例提供透明视图，并明确标识每台机器背后的底层供应商，例如 Verda（前身 Datacrunch）、Lambda、Voltage Park、Hydra Host、Digital Ocean 和 Nebius。这种透明度还延伸到展示 SOC2 Type II、HIPAA 等合规认证信息。

![电脑程序截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/865d2258-5385-470a-a5a4-632ee5bde9b9_936x501.png)
*来源：在 Shadeform 控制台上悬停 Nebius 图标，查看其一摞合规认证*

事实上，截至我们测试时，Shadeform 提供来自 23 家不同供应商的 GPU 访问，是我们在任何市场上见过的最多的一家。

有意思的是，Shadeform 的主营业务已经转型，如今以经纪人（broker）身份进入批发裸金属市场。这意味着其相当一部分收入来自为客户谈判并搭建大规模集群部署，尤其是在亚太地区（台湾、日本、印度）。Shadeform 网站因此成为一个有价值的发现工具，也常常是各家 Neocloud 的 GPU 首次公开露面的地方。Shadeform 似乎还是 NVIDIA Brev 服务目前唯一的合作伙伴——我们将在本文后文介绍 Brev。

尽管如此，由于没有可供我们测试的完善 Slurm 或 Kubernetes 服务、没有监控仪表盘，也无法对底层供应商的机器做主动/被动健康检查，我们认为 Shadeform 很难超越青铜级别。我们期待未来测试其集群产品，并想办法评估其经纪服务。

### Runpod

Runpod 运营着一支超过 20,000 块 GPU 的庞大机队，用户遍布全球。然而，把每个用户都塞进一个「pod」（容器）里的这一根本架构选择，严重限制了其服务大规模训练、推理以及任何企业级工作负载的能力。

在我们的测试中，这种以容器为中心的设计让人无法使用标准 HPC 与 MLOps 工具，例如用带 Pyxis 或 Enroot 的 Slurm 运行容器化 MPI 任务、对底层裸金属基础设施执行主动健康检查，或使用 Kubernetes。

在我们测试 Runpod 的 Slurm 服务（仍在 Beta 阶段）时，最初用的是直接来自另一家供应商 FarmGPU 的集群，我们就发现的一系列问题给出了反馈。Runpod 技术团队反应积极，接收了反馈，并承诺在下一个开发周期积极吸收。几周后，Runpod 另一批团队成员坚持让我们换一家裸金属供应商、直接从他们的控制台重新测试。我们欣赏这种投入，但第一轮测试中发现的所有核心问题依然存在。

默认用户是 root，无法添加其他用户、强制 RBAC 或使用外部 IAM 供应商。默认 home 目录（~）不在共享文件系统上，迫使用户切换到单独的 /workspace 目录。更关键的是，环境缺少必备工具。我们发现没有预装 MPI，最初用 srun 运行基于 MPI 的任务也失败了，因为必须修改 hostfile、指定外部容器主机名和路由——这些信息不会在 DNS 或标准 IP 中更新。具体来说，我们必须 export NCCL_SOCKET_IFNAME=”ens1”（因为它没有预先写入 /etc/nccl.conf）、export HF_HOME=/workspace/.cache/huggingface（因为默认工作目录是 /root 而不是 /workspace）、执行 head_node_ip=$(srun --nodes=1 --ntasks=1 -w “$head_node” ip addr show ens1 | grep “inet “ | awk ‘{print $2}’ | cut -d’/’ -f1)，并在 mpirun 命令里加上 --hostfile hostfile，而标准集群上的做法要简单得多。即便在第二轮测试前已经掌握了这些自定义做法，其文档目前仍然很不完善，显然还是个 beta 功能。

在监控和健康检查方面，我们预计 Runpod 仍将难以保证大规模训练所需的可靠性与性能。我们听到多位 Runpod 客户反映：由于 Runpod 不会明确告知你会落在哪家底层硬件供应商上（除了让你选「区域」，以及在「secure 云」或「community 云」之间二选一），他们实际上感觉像在转轮盘赌，试图「抽到一个好 pod」。换句话说，因为控制台里看不到性价比信息，用户只能凭自己对质量的感觉反复开通/释放 pod，浪费大量时间。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/3e4b9378-bfa4-4d7f-9b7f-75536fd451c9_935x594.png)
*来源：在 runpod 控制台上查看一些欧洲区域*

总体而言，我们预计 Runpod 将继续服务于看重其简化、容器优先方式的利基市场，但若不对其架构做出根本性改变，它很难在我们的标准上取得进展。

### Verda/DataCrunch

Verda（前身 DataCrunch）总部位于芬兰，在芬兰和冰岛均设有数据中心。登录后，Verda 提供一个干净漂亮的控制台，开通资源相当顺畅。其「Instant Clusters」功能好用，几分钟内就建起了一个 slurm 集群。其 Slurm 实现的完整度也令我们印象深刻，与本名单上许多青铜级甚至白银级供应商形成鲜明对比。从这次体验看，尽管该服务仍标注为「Beta」，他们似乎已经和客户一起实战检验过了。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/d3bd5227-745d-4b79-a84e-9a4f1629b40d_936x514.png)
*来源：清爽直观的集群创建设置*

具体来说，我们拿到的 B200 集群具备我们期待的一切：pyxis、enroot、hpcx、nccl、nvcc、topology.conf，以及接入 Slurm HealthCheckProgram 的 dcgmi health -c。

监控方面，Grafana 仪表盘附带一条有趣的 SSH 命令用于获取密码，配置也相对完善。与任务性能相关的缺失项都比较次要，我们给出了如何在标准 DCGM 指标之外做些改进、并以对用户有意义的方式展示的反馈。该平台也仍然没有任何办法在存储层或 slurm 层添加带 RBAC 强制的用户。

总体而言，有了可用的 B200 实例和完整的 slurm 安装，我们的初步印象是 Verda 较上一轮测试已有显著进步。然而，这一坚实的软件基础仍被商业与运营层面的重大问题拖累。

我们从多位 Verda 客户那里听说了可靠性问题，既有硬件层面的，也有 WAN 连接方面的。具体来说，有 Verda 客户告诉我们，整个站点可能毫无解释地陷入瘫痪。这类事情难免发生，但更严重的问题在于响应。遗憾的是，我们看到 Verda 在实例宕机或整站无法访问时，仍向客户收取 GPU 时间费用。在我们看来，这是一种冒犯性的商业行为。我们对所有云供应商的基本期望是：以书面形式承诺其 SLA，一旦违约，以服务积分或从客户月度账单中扣减的方式承担责任。不遵守书面 SLA，就会抵消我们在测试中从 Verda 身上看到的诸多技术优势和有吸引力的定价。

> 注：本文发布以来，我们已与 Verda 详细讨论了这一问题。Verda 承诺以至少 2 倍于宕机实例运行费用的服务积分，补偿所有遭遇停机的客户。通过聊天联系技术支持的客户会收到一条自动消息，说明所有停机都将获得补偿。工作日发生的停机，Verda 通常在 24 小时内退款；周末发生的停机则在次周一处理。对按月计费的客户，任何停机或缺陷都通过从当月发票中扣除相应金额的方式予以补偿。
>
> 坦率地说，我们认为这是一个非常好的回应。
>
> 总体而言，SemiAnalysis 建议客户在向供应商追讨停机赔偿时，务必保留好服务器日志、截图及其他信息，随时可用。到目前为止，我们只见过黄金级或白金级供应商会在客户没有主动要求的情况下发放补偿积分。

总体而言，我们建议 Verda 解决其可靠性难题，完成目前处于 beta 阶段的 slurm 服务，改进监控仪表盘，并继续开发其 kubernetes 服务。我们期待未来看到 Verda 的更多表现。

### Digital Ocean

Digital Ocean 是传统云供应商进军 GPU 领域的又一个案例。然而，其 H200 标准定价为每小时 $3.44，又没有 slurm 和 kubernetes，我们认为对于那些尚未被锁定在其生态系统里的客户，它将很难赢得生意。

![](https://substack-post-media.s3.amazonaws.com/public/images/87f4c53a-e6c3-4a3f-a990-607ebc7d5338_937x652.png)
*尝试创建一个「GPU Droplet」*

虽然很遗憾我们未能在 Digital Ocean 控制台上直接创建 GPU 实例，但我们通过 PaleBlueDot（一个市场平台，本文后文会讨论）访问到了一台机器。这台单机性能尚可，但由于无法创建集群，也没有共享存储或高性能网络、监控或健康检查，我们很难推荐把 Digital Ocean 的 GPU 用于最低限度开发者机器之外的任何用途。

### IBM Cloud

IBM Cloud 是我们最后一家进军 GPU 领域的通用云。IBM 落入了传统企业傲慢的窠臼——对市场早有定论的事情固执己见。

IBM 不让你用 Slurm，而是推销 LSF；不让你用 Weka 或 VAST，而是推销 Spectrum Scale（他们的 GPFS）；不让你用 kubernetes，而是推销 OpenShift。这一切据说都是为了您好，尊敬的客户，因为 IBM 比您更懂。[可事实并非如此，他们也并不更懂——就连 IBM 自己的 AI 研究部门用的也是 SLURM 而非 LSF](https://github.com/foundation-model-stack/fms-fsdp/blob/main/scripts/train.slurm)。

不幸的是，当我们试图与 IBM 安排测试时，他们竟然停用了我们的账户，还阻止我们注册新账号。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/6fa58846-1f43-4d61-8698-dfefd7c5f257_937x528.png)
*IBM 阻止我们测试他们的服务 L*
![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/e2919c64-8af9-4c2f-bce6-2bd5f893e130_893x282.png)
*更加莫名其妙的错误*

即便试图绕过这一验证流程，IBM 的账户验证团队（与我们最初对接的分析师关系和产品管理团队不是同一批人）也会拨打账户注册时填写的手机号，喋喋不休地盘问我们在平台上做什么。「研究」两个字不足以打发，我们必须详细解释要用新账户究竟做什么。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/19449cdd-1fbe-4fc1-b650-d0b5d7e63147_936x495.png)
*得知 GPU 是 CPU 所不具备的「额外脑力」*
![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/eb48203b-36be-4c02-81ab-ca910353a052_936x495.png)

虽然有不少可用优惠券参与的促销，但在默认区域法兰克福，每小时 $12.25 的 H100 价格实在难以自圆其说……

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/9c004f5f-29f3-4be3-ad88-a0a631ce92d4_936x495.png)

尽管如此，我们确实只用了 45 秒就开通了一台新机器，分配浮动 IP 并访问它花的时间稍长一点。基础镜像里没有预装 NVIDIA 驱动、docker 和 nvidia container toolkit，让我们在开始测试前又多费了一番周折。但总归是能用的。

当我们用 docker 做一个简单的下载速度测试、进行到大约一半时，IBM 再次发现了我们的账户并将其关闭。在将来能够测试其服务之前，我们维持 IBM 作为青铜级供应商的评级。

### Hot Aisle

Hot Aisle 是一家只做 AMD 的新兴 GPU 云，以有竞争力的价格按需提供 1 卡 VM 或 8 卡裸金属节点的 MI300X GPU。最近，他们完成了 SOC 2 Type I 审计并取得 HIPAA 合规。有意思的是，他们还推出了 2 卡和 4 卡 VM，AMD 的 xGMI 互连以直通方式透出、可供使用。这对开发者机器而言是一项独特而有竞争力的产品。我们认识开源生态里的几位用户，就因为其灵活性和有代表性的真实性能而在 Hot Aisle 上做测试。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/39aaf715-ee9d-4fbc-a80b-048d800abeca_936x866.png)
*4 块 GPU 之间可用的 AMD xGMI 互连*

目前，Hot Aisle 没有共享存储、监控仪表盘、健康检查、现代安全实践、RBAC、垂直整合的支持服务，也不具备规模化运行能力（即一次运行超过 2 台或 4 台机器）。他们在网站上声称有 slurm 或 kubernetes，但当我们寻求帮助时，实际并未搭建好。我们第一次尝试测试时，Hot Aisle 无服务可用，没有任何裸金属服务器或虚拟机供我们使用，不过后来还是抢到了一些。

![电脑程序界面截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/1e32b293-7f4c-4e30-9ee1-26040902054b_935x318.png)
*生意兴隆——只剩 3 块 GPU 可用！*
![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/a2ab1165-f4a9-4bb7-b16d-12bad12369b7_936x459.png)

在市场转向 MI325X 和 MI355X 之际，很难理解 Hot Aisle 除了提供廉价 MI300X 之外还能如何进取。当其他供应商自 9 月起就已完整搭建好 MI355X 并向付费客户开放时，Hot Aisle 的 MI355X 可能要到今年年底、甚至明年初才会面世。专注单台开发者机器而非集群，是利基；专注 AMD GPU 而非 NVIDIA GPU，是利基；专注 MI300X 而非 MI325X 或 MI355X，又是利基。于是，利基的利基的利基市场。

### Vast.ai

Vast.ai（不要与存储供应商 Vast Data 混淆）以 GPU 市场的形式运营，而非直接供应商。该平台声称自身已直接通过 SOC2 合规，还有其他一些值得关注的安全信息：<https://vast.ai/compliance>。他们还表示许多底层数据中心供应商通过了 ISO27001 认证，这对一家聚合商而言是显著进步，但对底层供应商究竟是谁，其透明度仍低于我们的期望——因为通常只描述所在位置。Vast 确实提供了让用户按 ID 追踪数据中心、以及切换「secure cloud」开关的方式，但除国家之外并不公开底层供应商的真实身份。集群可按需申请，我们未能试用。用户可以通过 stripe（信用卡）、coinbase 或 crypto.com 为 GPU 付费。

我们的测试体验印证了该平台的架构取向：它几乎完全为容器化工作负载而设计，极力把用户推向 Jupyter notebook 环境。要获得基本的 SSH 访问需要手工配置多个步骤，连上之后也很清楚：我们运行在容器里，而不是 VM 或裸金属主机。这种纯容器模式直接排除了 Slurm 或原生 Kubernetes 等标准多节点编排，尽管可以按需申请集群。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/79f87294-7c31-4830-b15f-0d81d3f85441_936x585.png)

可靠性与性能难以预测，这是聚合商模式的通病。我们的第一个测试实例开通在捷克，底层供应商不明（不过 IP 查询显示可能是 E-Infra 或 Zoner Cloud）。虽然这个实例能用，但市场模式意味着用户每次部署都要在诸多质量维度上掷骰子。在无法测试托管 Slurm/Kubernetes、多节点集群，也无法审视监控与健康检查的情况下，Vast.ai 仍是一个主要面向个人开发者和爱好者的平台。

### CUDO Compute

CUDO Compute 成立于 2017 年，与名单上许多同行一样，其起点是加密挖矿，只是规模不大。CUDO 如今运营着一个全球数据中心伙伴网络，最近还宣布与 CanopyCloud.io 建立合作，以在全球范围扩展其数据中心网络。

我们的上手体验从其 web 控制台开始，它提供高度可配置、以项目为单位的方式，来组织跨全球数据中心的资源。目前，互联互通节点只在达拉斯提供，8 卡裸金属服务器则可在巴黎、斯德哥尔摩或挪威克里斯蒂安桑获得。总体而言，10 座全球数据中心中有 6 座提供 GPU VM，其余 4 座只提供 CPU VM。我们决定通过 CUDO 位于南非森丘里昂（Centurion）的数据中心，开通了我们有史以来第一台非洲 GPU VM。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/9e504a74-35b5-4bc5-a6a9-bc0b30051572_936x510.png)
*在 CUDO Compute 上开通一台 VM*

开通虚拟机很顺畅，整个开通流程不到 4 分钟，控制台还提供便捷的 ssh 密钥管理。很实用的一点是，我们可以在所使用的数据中心位置配置一块共享磁盘，这意味着本地数据可以在 VM 开通/释放的循环之间重复利用。不过，我们部署的这块 200GB 磁盘不是文件系统卷，默认不会挂载、对 OS 镜像不可见。我们更希望有一个可挂载到多台机器的共享文件系统卷——这需要服务端具备类似的底层功能来支持。同样令人遗憾的是，我们是以共享 root 用户登录 VM 的，而不是把经 RBAC 强制的认证凭据从控制台传递到底层 VM。

此外，基础 Ubuntu 镜像开箱即用并不适合 AI：所提供的驱动版本和 nvidia container toolkit 版本严重过时（意味着不安全）。OS 镜像还缺少 pip/pip3，python3 也没有别名到 python，搭建一个基础开发虚拟环境需要额外步骤。至关重要的是，CUDO Compute 与底层数据中心确实维持着 ISO 27001 合规，这是许多同类供应商都缺失的一项关键安全认证。

总体而言，CUDO Compute 拥有令人看好的基础：控制台灵活易用，覆盖全球。但由于缺少托管 slurm 或 kubernetes 服务、共享文件存储、监控仪表盘、健康检查以及任何形式的主动式企业支持选项，该平台尚不具备大规模训练和推理的条件。我们建议 CUDO 专注打磨基础机器镜像以提升易用性，考虑部署共享文件存储，并继续在编排层积累 slurm 与 kubernetes 集群的经验。

### Lightning.ai

Lightning.ai（又称 Lightning Cloud）是一家为 Neocloud 和超大规模云厂商的 GPU 机器做经纪的平台，并在其上叠加了实用的 MLOps 功能。Lightning Cloud 的创业故事始于 PyTorch Lightning 的开发——一个开源框架，用来组织和简化 PyTorch 的样板代码，如训练循环、日志、checkpoint 和分布式训练。lightning 的 git 代码库似乎是 Lightning Cloud 销售漏斗入口的第一大来源。

快进到今天，随着 LLM 崛起，市场出现了分化。NVIDIA NeMo 等老一代框架在底层使用 Lightning，而我们测试所用的新一代框架如 torchtitan、verifiers 和 Megatron-LM 则不用。开源的 `pytorch-lightning` 和 `lightning` 软件包仍在快速增长：

![](https://substack-post-media.s3.amazonaws.com/public/images/6c9e41f3-542b-4c43-9248-19ccd74462dd_1101x633.png)
*来源：Lightning.ai，数据来自 pypi*

功能上，Lightning Cloud 产品提供了一种跨多云追踪「谁在用什么」的简便方式。我们有机会测试了 Lightning Studio，它支持在浏览器里（VSCode、Jupyter notebook）或通过远程 SSH（VSCode、Cursor、Windsurf 等）访问 GPU。用户还可以向按需获得单机或集群提交批处理任务和「mmt」（多机训练）任务。我们对集群的测试即将展开。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/8800c025-6159-4a42-a150-476d1fcf6641_937x494.png)
*来源：我们的 lightning.ai 主页*

值得注意的是，这些多 GPU studio、批处理任务和 mmt 训练任务仅限 Pro、Teams 或 Enterprise Custom 付费档位的用户使用。Lightning 是我们见过的唯一一家按席位（per-seat）收费的 Neocloud，再在幕后把它换算成其替客户管理的集群上的 GPU 小时。

![](https://substack-post-media.s3.amazonaws.com/public/images/ecaa1389-1d7e-4182-8bcc-0736c661011b_1224x694.png)
*来源：lightning.ai/pricing*

有意思的是，平台提供便捷的方式为现有「studio」（即 notebook 或远程 shell）挂载/卸载 GPU，并在闲置时自动休眠。这意味着用户只为所用付费。Lightning 还会预估从特定供应商（如 AWS、Google、Lambda、Voltage Park 或 Nebius）开通 GPU 的等待时间，其中最糟的是 AWS 的 8x H200 机器，预估等待 3 小时。遗憾的是，尽管网站另有说法，NScale 并无 GPU 可供使用。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/3d6ff237-f89c-463e-9deb-8eba5bad656a_937x494.png)
*在 Lightning.ai 中使用 VSCode notebook*

测试中另一个引人注目的细节是：notebook 拥有完整的 CLI 访问权限（包括 docker），这意味着 notebook 直接运行在底层 VM 之上。这给了用户在环境里的完全灵活性。

总体而言，我们对这种把集群访问从用户那里抽象掉的远程开发环境的实用性持怀疑态度，尤其在市场高端。GPU 算力最大的买家们，用一个简单的 manifest.yaml 在 kubernetes 上起一个 notebook，或在 slurm 集群里通过 `srun -N1 —gpus-per-node=8 —pty bash` 访问单机，都不成问题。

如果行业越过 lightning 框架继续前行，而 GPU 市场业务继续只聚焦于在昂贵的超大规模云之上赚取差价、没有第三方算力，我们很难为 Lightning Cloud 看到出路。至于 ClusterMAX 评级体系，我们期待未来测试 Lightning Cloud 的 mmt 训练和 kubernetes。我们鼓励 Lightning 考虑构建 slurm 服务，增加与任务日志和性能剖析联动的底层集群健康监控仪表盘，增加与集群主动/被动健康检查的集成，以及高性能存储与网络的定制选项。

### Qubrid

Qubrid 以青铜级别进入我们的评级。该供应商通过一个干净的 web 控制台提供单 GPU 实例（VM）和裸金属服务器租赁，硬件从 H100 到最新的 B200。

我们对其单 VM 服务的实测喜忧参半。好的一面是，开通单机的用户体验很顺畅，SSH 和 Jupyter 访问都易于配置，我们的 B200 实例约 8 分钟即开通可用。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/43dcf57e-250a-4d1d-b9b5-bcfb77fc714b_936x499.png)
*来源：Qubrid 控制台*

然而，Qubrid 在机器还卡在开通中时就向用户计费，这一事实破坏了这种基础可用性。我们只能猜测，原因在于 Qubrid 正如我们登录时一项基础 IP 测试所证实的，跑在弗吉尼亚州阿什本（us-east）的 AWS 硬件上，尽管他们并未向客户说明这一点。读者可以在上图中看到，我们的 B200 实例默认安装的是 CUDA 12.4 工具链。虽然驱动较新（12.6），但这个旧工具链显然无法用于 Blackwell 硬件（即 SM100）——后者要求 CUDA 12.8 及以上。

最后，Qubrid 的商业模式更像传统服务器托管商，而非灵活的 Neocloud。其定价要求严格的最短承诺（例如 H100 至少 1 周、H200 至少 1 个月、B200 至少 3 个月），并且公然宣传按年租服务器——尽管硬件并不属于他们。我们鼓励 Qubrid 修正其计费做法，解决可用性问题，并更坦率地说明卖给客户的究竟是谁的硬件。

### Latitude.sh

Latitude.sh 定位为一家简单直接的供应商，提供裸金属或虚拟的 L40S 和 H100 机器，主要位于得克萨斯州达拉斯。登录后，控制台干净整洁、组织有序。我们欣赏其按项目组织资源、并为「dev」或「pre-prod」等环境打标签的能力。开通选项清晰，几秒钟就能起一台机器。

一个有趣且较为独特的功能是「Cloud Gateway」服务，它借助 Megaport 建立与主要公有云的私有连接。对于追求混合云或多云策略的客户，这可能颇具吸引力。

不幸的是，测试期间我们遇到了几个问题：一台 L40S VM 报出 NVML 驱动/库不匹配错误，一台 H100 VM 的驱动开通干脆没正常工作。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/cc9497ec-7fe4-417e-9380-92957a039809_935x205.png)

这类不稳定本是使用虚拟机的固有风险之一。不过，重新开通几台新 VM 后，L40S 和 H100 实例的表现符合预期，GPU 开箱即被 nvidia-smi 识别。

话虽如此，唯一可用的基础 OS 镜像是「Ubuntu 24 ML-in-a-Box」，可它内置的 pytorch 版本过时，python3 缺少 python3-venv 包，python 没有别名，docker 和 nvidia-container-toolkit 也没有预装。

除单实例层面的问题外，Latitude 没有 Slurm 或 Kubernetes 服务，没有集成监控仪表盘，没有共享存储选项，也没有健康检查。

对个人开发者或小团队来说，Latitude.sh 或许价格诱人。但对于寻求生产级集群的组织而言，该平台力有不逮。

### Denvr Dataworks

在之前几轮测试中，Denvr Dataworks 是一家实力不俗、前景可期的云供应商，只是对浸没式冷却有份「半职业级」的痴迷。先不谈浸没式冷却在技术层面是否可行，同样明确的是，围绕数据中心冷却淡水用量的说法也被大大夸大了。[这份报告](https://eta-publications.lbl.gov/sites/default/files/2024-12/lbnl-2024-united-states-data-center-energy-usage-report.pdf?utm_source=substack&utm_medium=email)和[这篇文章](https://andymasley.substack.com/p/the-ai-water-issue-is-fake)对此有详细描述：根据统计口径不同，美国数据中心去年的淡水用量不到全国淡水量的 0.15%。

- 若只计冷却用水，每日 5,000 万加仑
- 若计入发电用水但不含水坝水库蒸发，每日 2 亿-2.75 亿加仑
- 若计入水电水库的蒸发，每日 6.28 亿加仑

与高尔夫球场灌溉每日约 20 亿加仑的用水量相比，液冷每日 5,000 万加仑只占约 2.4%。

遗憾的是，Denvr 原班人马似乎大多已离职，直接使用其网站也无法开通 GPU。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/67f8f0d9-1ee2-4927-930b-eaa7ae6dbfe3_937x496.png)
*没有 VPC 就开不了 VM*
![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/a1866d60-824a-494d-96e0-16a973b5210b_937x496.png)
*不找系统管理员就建不了 VPC*

不过，Denvr 的硬件并未完全消失。看起来 Denvr 已转型为纯批发，通过聚合商和市场对外输出产能。在我们测试 Dstack Sky 平台期间，我们的任务经 vast.ai 落在了得克萨斯州休斯敦的一台 Denvr Dataworks 机器上。在穿过层层「套娃」般的 ssh 隧道、进入那个由 dstack 编排、vast.ai 部署、运行在 Denvr 服务器上的容器之后，我们成功在这套硬件上跑起了一个多 GPU（2x H100）RL 训练任务。能用的时候，还真能用。

未来，我们期待重新审视 Denvr 平台，并测试其 slurm 或 kubernetes 服务。

## 不予推荐（Not Recommended）

**不予推荐（Not Recommended）** 是我们的最后一个类别，名字本身就说明了一切。该级别的供应商在一项或多项标准上未达到我们的基本要求。需要注意的是，这是一个很宽泛的类别，因此在正文中我们会具体描述每家云究竟缺了什么。

- **表现不佳（Underperforming）**——根据我们的实测，我们认为该级别的供应商只要修复一个或多个关键问题，就能迅速升至青铜甚至白银级别。关键失分的例子包括但不限于：没有现代 GPU 可供使用（例如只有 A100、MI250X 或 RTX 3090，因为我们期望至少要有 H100 可用）、未完成基础的安全认证（如 SOC 2 Type 1 或 ISO 27001）、关键服务器功能配置失误（即没有禁用 ACS，或没有启用 GPUDirect RDMA），或存在侵害客户利益的商业行为，例如在集群还在搭建过程中、或服务器因硬件故障停机期间仍向用户收取 GPU 小时费用。
- **暂不可用（Unavailable）**——该级别的供应商拥有令我们感兴趣、令我们兴奋的服务，但由于尚未对公众开放或无法供我们测试，我们无从验证。例子包括：尚未正式上线服务的供应商（尽管其宣传材料会让你以为早已上线）、已完全售罄且没有新增产能计划的供应商、仅服务涉密政府客户的供应商，以及其他原因。我们对该级别中的许多供应商都感到兴奋，但在测试上坚持「信任但要验证」的原则，在完成实测之前将他们保留在此类别。

## 表现不佳（Underperforming）

#### Sharon AI

Sharon AI 是一家总部位于澳大利亚、正大举进军美国市场的公司。其雄心包括合资企业 Texas Critical Data Centers，目标建设一座 250MW 数据中心，并有扩至 1GW 的路径。他们宣传拥有一支最新硬件机队，包括 NVIDIA H200、H100 和 AMD MI300X GPU，全部以 InfiniBand 部署。

然而，注册账户并登录其「Client Area（客户区）」后，我们实际上找不到开通实例的入口。我们能以还算合理的按小时按需价格配置出一台 GPU 机器。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/c1cda8ef-20f4-40e9-8557-0bda7926e278_935x649.png)

尽管控制台相当长一段时间里都显示这台 VM 处于「ready（就绪）」状态，我们还是花了 6 分 21 秒才开通并访问到这台虚拟机、开始跑一些测试。机器上还出现了 NVML 驱动/库版本不匹配错误：

![电脑程序截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/51ed670b-1e98-469e-8c97-f7092db7822e_630x234.png)

可一分钟后……它自己消失了

![电脑程序截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/4a49619b-88e2-42bf-bea3-c2209a0de78d_772x589.png)
![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/740e5192-17cf-47f6-ae65-65d042b03f9f_481x367.png)

我们认为后台有一些开通脚本在运行——尽管我们的 ssh 访问早已在控制台启用。值得注意的是，我们在设置过程中确实选了一个与「docker、portainer、nvidia container toolkit」相关的镜像，而那些东西确实开始随机跑了起来。

可是，错误又回来了。而这一次，它再也没走。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/4cba2ef5-fb64-4bde-a376-f117f310917e_935x354.png)

又等了 22 分钟后，我们认赔关闭了实例。有意思的是，开通实例可以按需进行，但要关闭实例却需提交人工「Cancellation Request（注销请求）」。平台也没有积分体系，所以在月度账单出来之前，你不会知道自己花了多少钱。希望我们的注销请求已被受理！

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/0cbdb807-bd18-4428-85db-8ac542b0a5c7_936x646.png)

最关键的是，Sharon AI 把自己定位为企业级供应商，却连这一类别的基本门槛（table stakes）都没达到。我们找不到任何公开文件或证据表明其持有 SOC 2 或 ISO27001 安全认证。对一家经手潜在敏感训练数据和专有模型的公司来说，这是一票否决项。

### IREN/Iris Energy

IREN 是最激进的加密矿企之一，正试图把自有设施改造为 Neocloud。与 TeraWulf、Core Scientific 和 Cipher Mining 等竞争对手不同——这些公司都通过经营带电壳体（powered shell）数据中心基础设施业务（即托管，colocation）从既有投资中实现了可观价值——IREN 却执意走艰难路线，在团队毫无相关经验的情况下独自建造 Neocloud，目前已为当前及未来客户锁定近 100K 块 GPU。

我们曾在 2025 年 3 月测试过 IREN，发现其服务严重不足，硬件上存在多处基础配置错误，例如 ACS 未禁用、GPUDirect RDMA 未启用。2025 年 3 月，我们对 AllReduce 集合通信的双节点 NCCL 测试显示，IREN 机器在 128MiB 消息大小下仅约 129.27GB/s，而 NVIDIA 参考值和我们对顶级 Neocloud 的测试都远在 >= 300GB/s busBW 之上。IREN 工程师后来向我们证实，根因是其团队未禁用系统 PCIe 交换机上的 ACS 设置，导致 GPU 无法与 NIC 直接通信、只能绕道 CPU 的 root complex。这本该是个简单的修复，而且检查与整改用软件很容易自动化，但我们一直无法核实 IREN 是否做出了任何改变。本轮测试期间，IREN 已连续三个多月声称没有可供测试的容量。

最近 IREN 收获了一些成功，与 Microsoft 签署了价值 $97 亿的承购协议，标的为其位于得克萨斯州柴尔德里斯（Childress）750MW 站点的一部分。业内众所周知，与 ClusterMAX 白银、黄金或白金级别的供应商相比，IREN 的价格低于市场水平。我们认为原因有二：

- 低于平均水平的成本结构：自持数据中心，且选址聚焦电价低廉地区（比特币挖矿行业的典型做法）
- 服务质量低于市场平均水平

若要深入分析 IREN 已公告 AI 云合同的经济性，[我们的 AI 云 TCO 模型](https://semianalysis.com/ai-cloud-tco-model/)是最佳工具。它受到众多 GPU 大买家及其金融赞助方的信赖。

### Hydra Host

Hydra Host 是另一家在没有任何安全合规认证的情况下运营的市场/经纪平台，也因此丢掉了一些《财富》500 强客户的机会。其 Brokkr 平台最近经过重新设计，可以便捷地访问来自众多数据中心的 GPU，不过如果你想确切知道租的是哪家供应商的 GPU，很多信息是缺失的。我们测试期间，Brokkr 平台上列出的许多 GPU 都处于「at capacity（满载）」状态，甚至包括 A100：

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/64637967-950e-410a-9333-d7481a20bd73_937x496.png)

总计，在我们测试时，Hydra 的 A4000、3090、5090、A10、A6000、GH200、A100 和 B200 均「满载」。可按需使用的有：8x 4090、8/7/5/4x L40S、16x V100、越南的 8x H100，以及印度、华盛顿州或日本的 8x H200。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/8ec1a57b-e3bb-4291-a8d9-a98d1164799c_937x490.png)

遗憾的是，要真正用上这些服务器，Hydra 强制用户预付一周的账单，并承诺「未使用部分退款」，而不是提供真正的按需体验。

我们期待在 Hydra 完成其在办的 SOC2 Type II 合规认证后，于 ClusterMAX 2.1 期间测试其白手套（white glove）集群产品。

### FarmGPU

我们仅通过 Runpod 测试了 FarmGPU，因为他们目前没有直接访问其云服务的途径。相关经历我们已在那一节详述：与团队多轮沟通之后，我们最终在一个经过修改的 Runpod 编排 slurm 集群上，于其网络上看到了符合预期的 NCCL 测试性能。我们未能测试 kubernetes，也无法核实任何监控和健康检查是否到位。

总体而言，我们欣赏 FarmGPU 持续改进的承诺、对存储盘性能的深厚知识，以及他们对 OCP Neocloud 工作组的贡献——其中描述了在 Celestica 白盒交换机上搭配 Kubernetes 使用 SONiC NOS 的经验。

目前 FarmGPU 尚未完成基础安全认证。我们期待未来再次测试其服务。

### Whitefiber

Whitefiber 是 Bit Digital 的全资子公司——后者也是一家最近从加密挖矿转向 Ethereum 质押与 AI 的公司。Whitefiber 于 2025 年 8 月在纳斯达克上市，融资约 $1.5 亿。两家公司合计（$WYFI 与 $BTBT）市值已接近 $10 亿。Bit Digital 最近宣布了一座可从 24MW 扩展至 99MW 的北卡罗来纳州数据中心，是对其蒙特利尔既有布局的大幅扩充，意在承载更多 AI 客户。该公司过去曾提及 288MW 的 LOI（意向书），并已公开宣布 4,096 块 H100、1,040 块 H200 和 464 块 B200 的合同。想深入了解这类公司及其扩张计划，请参阅我们的[数据中心模型](https://semianalysis.com/datacenter-industry-model/)。

在我们的测试中，Whitefiber 的网络性能处于参考值范围之内，某些消息大小下甚至略好。

在其他方面，我们遗憾地感到失望，其质量与网络性能不可同日而语。我们获得了一个 Slinky 集群，可同时访问 slurm 层和 kubernetes 层。不幸的是，两层都不能用。起初 slurm 无法从远程机器访问，经过大量协商才得以解决；而在 kubernetes 层，由于 slurm-bridge 未配置、所有 GPU 资源被 slinky 占用，任何任务都无法调度。最终我们靠一台跳板机进入了 slurm 集群，然后遭遇了典型的 slinky 自坑（footgun）：没有 git、vim、nano、python，也没有安装软件的 sudo 权限。

集群仪表盘冗长详尽，却缺少关于任务的重要指标。我们找不到任何主动或被动健康检查。对方还给了我们 clockwork 和 trainy 的仪表盘访问权限，但两者既没有解释也没有文档，因此在测试中派不上用场。

Whitefiber 显然在 AI 云业务上投入不菲：聘请了一支庞大的顾问团队，集成自研互连以替代 NVIDIA，并把推销上门的软件买了个遍。遗憾的是，仅因缺少第三方审计机构出具的基础安全认证（如 SOC 2 Type I/II 或 ISO27001），他们连青铜级都进不了。我们相信，到 ClusterMAX 2.1 或 ClusterMAX 3 时，只要 Whitefiber 拿下基础的 SOC2 Type I 合规并修好其 SLURM/Kubernetes 编排，至少能进入青铜级。

### DeepInfra

DeepInfra 是 GPU 云赛道的新入局者，起步于推理服务，如今对外出租市场上最便宜的一批 B200。我们认为，推理这种相对波动大的业务增长快于算力侧可预测的节奏，DeepInfra 正是在寻找客户来消化其闲置产能。换言之，与在既有云业务上扩张推理端点业务的 Nebius 或 GMI 相比，他们走的是相反的路线。

遗憾的是，DeepInfra 目前在 Neocloud 市场上唯一的产品——8xB200 实例——在我们每次尝试测试时都无容量可用，而且没有安全合规认证。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/de6ea251-b133-43de-8321-5da1e4a34773_936x495.png)

凭借有吸引力的定价和一支有才华的工程团队，我们希望未来在 Neocloud 市场上看到 DeepInfra 的更多动作。

### Dstack Sky

dstack 这家公司有一个非常有趣的编排器和调度器，可以取代 slurm 或 kubernetes。我们喜欢超越 slurm 和 kubernetes 的思路，也不断听到 dstack 用户对其体验的好评。但另一面，dstack sky 市场服务就没这个水准了。Dstack sky 是一家云经纪平台，与其 GPU 编排产品的思路类似，聚焦以 CLI 驱动的方式开通 GPU 资源。该服务允许用户创建三类资源：开发环境（可通过 IDE 访问的 GPU 实例）、任务（task，批处理作业）或服务（service，已部署的模型或 web 应用）。

底层一切都由 docker 容器驱动。正如我们此前评审其他市场和经纪平台时所说，这给构建开发环境带来了初始限制，用户必须遵从才能使用该产品。不过令人欣慰的是，dstack 并不要求用户从其基础镜像构建，而是允许用户自带任意镜像、由 dstack 在其上叠加编排。我们特别喜欢那个自动修改用户本地 .ssh/config 文件的便利脚本，可以快速访问新建的系统。

然而，这层抽象伴随着严重的透明度缺失。底层 GPU 供应商（即「Backend」）如何被选中并不清楚，当你从 CLI 获得「Offers（报价）」时，也没有查看供应商完整列表或按价格筛选的途径。申请 H100 时，我们无从分辨 PCIe 与 SXM 型号。测试期间我们碰巧拿到了 2 块 SXM GPU，但这似乎纯属运气。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/50859f48-9e02-459e-9496-8f13c395ff70_936x422.png)
*通过 dstack 获取供应商的 2x H100 报价*

连上之后，我们发现自己是 root 登录，意味着集群侧没有 RBAC 或共享存储选项。我们连接的机器只提供一个 100GB 的小 root 分区，连接速度极慢，CLI 里敲个回车都要卡上几秒。这可能是因为我们的实例由泰国的一家供应商（"Internet Thailand Company Ltd."）开通。不过存储性能不错，导入 torch 只用了 6 秒。

这段体验凸显了 Dstack 模式里的多层间接性：我们向 Dstack 购买积分；Dstack 再向 Vast.ai 这样的供应商支付实例费用；Vast.ai 又向终端供应商付费来运行容器（泰国的这家供应商底下可能还套着一家数据中心运营商）。究竟有多少层、最终由谁负责硬件维护和安全，都不得而知——对任何严肃工作负载而言，这都是重大隐患。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/9ea80b64-1339-4fcb-b58a-419ac9a8b8f8_937x293.png)
*在 1x H100 上、使用 `verifiers` 代码库跑一个 RL 评测任务*

尽管如此，我们仍能用 dstack 在 5 分钟内于 VSCode 中连上一台带 2x H100 的远程机器，再用不到 5 分钟装好所需软件，并跑通一个示例模型评测的 RL rollout。全程不到 30 分钟，用既有积分按分钟计费。这种按需开发体验相当不错，促使我们重新思考用 CLI 起机器这件事。能用的时候，还真能用。

我们期待未来再次测试 dstack，该公司计划不久后完成 SOC 2 Type 1 等基础安全合规认证。

### PaleBlueDot

PaleBlueDot 是表现不佳级别中众多缺少基础安全认证的市场之一。在测试聚合于 PaleBlueDot 市场上的五种不同云中的一部分时，我们体验良好：开通并连接虚拟机都很简单，且只按分钟计费。我们鼓励 PaleBlueDot 考虑接入更多供应商，以提升 GPU 可用性，并通过 slurm 或 kubernetes 编排加共享存储提供真正的集群体验。

### Hyperbolic

Hyperbolic 把自己定位为低成本 GPU 聚合商，然而其「高端」H100 和 H200 产品在网站上明确标注为「beta」。用户可以用加密货币、银行转账或信用卡为 GPU 付费。

我们的实测以异常迅速的开通时间开场：一台新 H100 实例从开通到可访问不到 25 秒，是我们全部调研中最快的一次。不幸的是，节点上的软件状态立刻让这一成绩打了水漂。实例预装的是过时的 PyTorch 版本（2.5.1），Docker 等必备工具也没有预装。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/310f7227-f93e-46e8-92bf-01b423cab3cc_935x536.png)
*来源：Hyperbolic 上一台全新的 H100 节点*

平台可靠性成为最致命的失分项。我们的测试被持续不断的连接中断、实例莫名其妙落入「Unknown status（未知状态）」所困扰，最终开通系统彻底瘫痪，我们无法创建或访问任何实例。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/3d43c154-df2f-4982-a966-87971c0ef20d_937x503.png)
*来源：未知状态……*
![电脑屏幕截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/a3f881b9-e577-4392-b50d-8a042303b87b_937x503.png)
*来源：hyperbolic UI 里的错误*

总体而言，Hyperbolic 生意前景可期，但缺少基础安全认证，而且在我们测试过的所有市场中，其按需 VM 的用户体验属于最差之列。问题究竟出在 Hyperbolic 一侧还是底层数据中心供应商一侧尚不清楚，但我们认为这正好说明：GPU 经纪平台/市场/聚合商的潜在用户必须直面可靠性方面的挑战。

### Aethir

Aethir 通过构建去中心化 GPU 算力基础设施（DePIN）充当底层基础设施伙伴。它聚合全球分布的闲置 GPU 产能，出租用于 AI 和云游戏。其模式建立在自家加密货币代币（ATH）之上，投资者用其「质押（stake）」GPU 并提供流动性，实际上是在对现货实例价格的波动性进行交易。

遗憾的是，Aethir 并非真正的自助式体验，潜在买家需要填写表单才能在其平台上购买 GPU 时间。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/4014c43e-7359-40bd-b8f4-4ae83ef6841b_937x897.png)

这个去中心化网络概念虽对云游戏尤为有用，但在 AI 领域尚未起飞。Aethir 没有任何安全合规认证，用户无从评估这家收款并管理 GPU 访问的公司是否建立了访问控制。

### Akash Network

Akash 是一个去中心化市场，号称在「Mainnet（主网）」上有 64 家活跃供应商。登录后，看起来有许多不同的消费级 GPU 可用。我们决定试一试，申请 1x H200。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/3ff3a7ae-f4f5-472e-a6ea-f3030109a225_937x497.png)
*申请一个 1x H200 部署*

遗憾的是，我们无法访问平台上的任何 H100 或 H200。有意思的是，平台提供了申请 AMD MI100 GPU 的选项，但当我们尝试申请它们或不同的 NVIDIA 消费级 GPU（3080、4090）时，得到的只有一个充满歉意的加载画面：

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/0a504cd5-04d6-4f51-b58f-3dfc27eb350a_937x497.png)
*等待竞价中……L*

等了几个小时也没等到一个 4090 的竞价之后，我们放弃了。总体而言，我们在 Akash 上的经历让我们认为，它基本上没准备好承载任何工作负载。

### Salad Cloud

Salad Cloud 是另一个去中心化市场，其「Community Cloud」产品主要聚焦以降价提供消费级游戏 GPU。而在其「Secure Cloud」产品中，没有 SXM H100、H200 或 B200 等高端 GPU 的选项。自 ClusterMAX 1.0 以来，我们确实欣赏 Salad Cloud 已通过 SOC 2 Type 1 认证，并且不向客户收取冷启动（cold-boot）时间费用。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/733157c5-77e5-456f-aa9d-de55b0d04bc6_937x554.png)
*来源：Salad Cloud 网站上的安全免责声明*

### Clore

Clore 是一个去中心化 GPU 市场，与 Aethir 和 Akash 类似。它把个人硬件「主机」（爱好者或小规模加密矿工）与寻求按需算力的用户连接起来。由于平台围绕其加密代币构建，用户被鼓励使用加密货币付款并质押 GPU。

测试期间，我们在注册账户时就遇到了基本问题。对于这样一个缺乏用户对 GPU 集群所期待的基础安全、可靠性、编排、存储和网络功能的平台，我们对其能否立得住存有总体疑虑。

### Mithril/ML Foundry

Mithril（前身 ML Foundry，再前身 Foundry）以 GPU 聚合商的身份运营，或者用他们自己的话说，是一家「AI omnicloud」。其核心理念是：GPU 市场的主要问题是价格发现与市场低效。他们的解法是通过聚合与抽象创造一个「流动性市场」，让成本动态调整以反映供给增加。我们完全不认同这个前提，也不认同这个解法。

「GPU 市场缺乏价格发现」这一前提本身就是错的，反映出对市场的根本误解。以我们的经验，超过 90% 的 GPU 云租赁量是企业间的长期合同交易，标准条款是 25% 首付、按月付款直至期满。换言之，典型的 B2B 交易。

原因——本报告已详细阐述——在于并非所有 GPU 都部署得同等好。GPU 算力不是大宗商品。Mithril 以及其他试图把 GPU 市场当成原油或木材那样激进金融化的公司，只围绕每 GPU 小时价格这一个变量做文章。这确实是一项重要标准，但它只是我们评估供应商质量的 129 项标准之一，而且往往难以反映集群的实际 TCO。

在一个对底层供应商层层聚合、抽象、如同「掷骰子」的市场之上再叠加抽象，Mithril 把全部运营负担都压给了终端用户。作为供应商，Mithril 无法掌控客户的支持体验、编排软件偏好、网络与存储性能、监控体验，以及最关键的——集群的可靠性与安全态势。

话虽如此，即便 GPU 算力真是一个流动性充足、已大宗商品化的市场，我们预期的赢家也应当开放接入众多 GPU 供应商、提供可用性的实时数据流、未来供给预测、来自终端用户的实际质量代理信息……但不幸的是，我们等来的是这个：

![黑白屏幕截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/7c4b349d-c2a9-4275-b356-5d8946095494_937x554.png)
*来源：已等待 3 个月，还在继续等。*

### GPU.net

GPU.net 又是一个市场，而且按数字算是最大的之一。其首页自豪地展示着接入 42 家供应商、共计 121k 块 GPU 可用。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/80cc70a2-0d6f-45e7-9ff9-5596ea565901_936x490.png)

按需价格合理，H100 为每小时 $2.15。遗憾的是，所有 H100 和 H200 SXM 似乎都不可用，尝试购买时显示「Booking Error（预订错误）」。最终，我们开通了一台 1x H100 80GB PCIe 和一台 2x L40S 机器，各花了约 2 分钟。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/c64c3f51-785d-44d6-8edd-e8a31c02cef0_936x509.png)

分别登录我们位于北美的 H100 机器和位于澳大利亚的 2x L40S 机器：一台有 GPU 驱动，一台没有。有意思的是，没有驱动的那台装了 docker，有驱动的那台反而没装。

我们发现，那台 H100 PCIe 机器（控制台上标注为「North America」）创建于 Hyperstack/NexGen Cloud 的蒙特利尔数据中心，而 2x L40S 机器（控制台上标注为「Australia」）则创建于 Sharon AI 位于澳大利亚墨尔本的数据中心。

总体而言，GPU.net 是又一个以加密为核心的去中心化市场，或许能为用户提供接入多家云供应商的选择权。但他们在可靠性、一致的用户体验，以及安全合规与认证等我们对 Neocloud 的诸多基本期待上都力不从心。

### Massed Compute

在上一版 ClusterMAX 中，我们评论过 Massed Compute 这家运营尚可的裸金属算力供应商，如何不幸地用包含错误信息的 AI 生成 SEO 垃圾文章淹没互联网。这对社区有害，而且修复很简单：在他们聊天机器人网页 HTML 的 **<head>** 区段加上 **<meta name=”robots” content=”noindex, nofollow”>** 即可。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/280aedc2-eb37-45aa-9dd2-a310d2aa0e83_935x520.png)
*来源：Massed Compute 的聊天机器人幻觉出一款新 H100——「dual GPU」*

### Exabits

Exabits 以裸金属供应商的身份运营，主要通过市场而非直连云对外输出产能。该供应商与一个加密货币项目相关联，后者似乎通过质押为 GPU 提供资金。

我们尝试通过 PaleBlueDot.ai 市场开通 Exabits 实例——它与 Digital Ocean、Massed 和 Nebius 等其他供应商并列在列。遗憾的是，在我们测试窗口内，该平台上没有可供开通的 Exabits 容量。

由于没有可访问的自助平台、市场上也没有可用实例，我们无法就任何核心标准评估 Exabits，包括编排（Slurm/Kubernetes）、多节点网络、安全或监控。

### Sesterce

Sesterce 是一家总部位于马赛的法国云，目前声称拥有 1GW 算力、管理 100k 块 GPU、获得 €7.5 亿投资。他们以加密挖矿起家，但最近宣布了一项横跨多座数据中心的欧洲主权 €520 亿投资计划。该计划的首个站点位于 Valence Romans Agglo，将部署 40k 块 GPU，总计 €18 亿。随后他们计划在大东部大区（Grand Est）增设两个站点，到 2028 年合计 600MW 产能、500,000 块 GPU，并在 2030 年进一步扩展到 1.2GW、超过 100 万块 GPU。好大的规划。

回到当下，Sesterce 似乎在其遍布赫尔辛基、堪萨斯城、得梅因、盐湖城、杜勒斯、纽约、卡尔加里、多伦多、孟买、大阪、澳大利亚、法兰克福、阿姆斯特丹、华沙、冰岛、挪威和瑞典的「区域」里，拥有较为可观的 NVIDIA GPU 可用性。从这种规模来看，单个 VM 显然部署在由其他供应商运营的数据中心里。定价也印证了「中间商在赚差价」的情形。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/603065b6-44e6-4116-98f2-9ebb5ad04a27_936x493.png)

用户可以在计划启动 GPU 机器的区域轻松创建卷（volume），日后还能在其他机器上复用这些卷。不错的功能。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/d0347acb-bac2-4785-a262-1a813cff2a27_936x493.png)

用户还可以配置特定的 docker 镜像，预加载到机器缓存中。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/5f27eba5-e5c4-4b92-abcb-176f3d89804a_936x493.png)

我们的 1x B200 VM 开通于赫尔辛基数据中心，登录后我们发现这台机器属于 DataCrunch（现已更名 Verda，另一家 ClusterMAX 青铜级供应商）。

集群可以申请（但不能按需开通）：B200 在赫尔辛基一次最多 16 个节点，H100 或 H200 在马赛一次 1-4 个节点。

遗憾的是，这些集群只是带共享存储选项的裸金属机器。Sesterce 不提供 Slurm 或 Kubernetes 编排、集群监控仪表盘或健康检查。经外部 IAM 供应商认证的 RBAC 似乎也不可用。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/8955655e-f408-40fd-839f-e9f0d5759772_755x532.png)
*登录一台 Sesterce 机器，docker 镜像已预加载在缓存中*

这台机器还预装了 nvidia 驱动和 docker，nvidia container toolkit 已配置且为最新版本。从赫尔辛基这个位置的下载速度相当扎实，安装 pytorch、下载 NGC pytorch 容器、从 Hugging Face 下载模型的速度都位居我们测试前列。

总体而言，我们在 Sesterce 的体验是扎实的。我们预计，对某些用户来说，为可用性和一台配置妥当的个人开发机支付 Sesterce 的溢价，足以抵消在其他云上经历的头疼问题。鉴于其公有云服务打下的坚实基础，我们鼓励 Sesterce 切入按需 slurm 与 kubernetes 集群赛道。

最重要的是，我们敦促 Sesterce 明示其平台上究竟是哪家供应商在实际运行机器，并公开披露简单安全审计与合规（如 SOC2 Type I 或 ISO 27001）的第三方认证，以便进入 ClusterMAX 评级。

### E2E Networks

E2E Networks 是一家上市的印度云基础设施供应商。在大规模融资和作为政府 IndiaAI 计划核心伙伴的推动下，公司正经历雄心勃勃的扩张。它在德里、孟买和金奈运营数据中心，但其 AI 平台「TIR」只在德里运行。这是我们本文的最后一篇评测，也是我们整体体验最差的一家。

测试流程始于一道咄咄逼人的 KYC（Know Your Customer，了解你的客户）程序，完成之前连登录都不行。我们按照其文档尝试开通一个训练集群，很快撞上问题。平台确实提供了一批有趣的预配置软件镜像（包括 NVIDIA NeMo），也提供为 slurm 集群创建共享文件系统的选项。然而，我们遭遇的是彻头彻尾的资源不可用。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/415627f0-54bd-4749-8860-1c6130e88e0a_935x496.png)
*创建一个 SLURM 集群*
![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/b316922d-1332-4665-a379-996ba5e49532_619x233.png)
*无法创建共享文件系统*

最严重的问题就发生在这个排队等待 slurm 集群部署的过程中。我们眼睁睁看着积分余额被耗尽，然后转为负数。而自始至终，我们都无法对集群点击删除、无法把账户从队列里移除。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/9d778784-6cb0-429d-8c0f-3b5412b7252b_936x496.png)
*为一个卡在「creating（创建中）」阶段的集群欠下 $7,061.05*

最终，E2E 支持团队的解决方式是把我们的账户彻底停用。我们认为，这种在集群尚在创建、完全不可用期间仍向客户计费的商业决定，是我们全部 ClusterMAX 测试中见过的最冒犯性的商业行为。

### OVHcloud

作为欧洲最大的云供应商之一，OVHcloud 拥有庞大的版图和丰富经验，本应占据有利位置去收割 EEA（欧洲经济区）的主权 AI 市场。然而，OVH 至今仍被一套缺乏现代 GPU 的传统 IaaS/VPS 模式所定义，而且，怎么说呢，[还有那次斯特拉斯堡数据中心失火](https://corporate.ovhcloud.com/en/newsroom/news/informations-site-strasbourg/)。拜托，那至今仍是任何人想到 OVH 时的第一反应……

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/4a33147d-1e8c-48a4-974f-2c618f740271_937x709.png)
*来源：OVH 可提供的最现代 GPU 是 H100 PCIe（价格还高达 £2.41）*

### Dihuni

Dihuni 是一家位于弗吉尼亚州的供应商，拥有一份扎实的客户名单。Dihuni 还与东京的大型电子公司 NEC 保持长期合作。为运营其 GPU 云，Dihuni 与 Qubrid（本文前文已介绍）建立了关键合作。我们认为这是一个显著趋势：像 Qubrid 这样的 Neocloud 开始把软件卖给 Dihuni 这类已有数据中心、想要「一键起步」的供应商。

### Akamai/Linode

Akamai 这家 CDN 巨头于 2022 年 3 月以 $9 亿收购 Linode，想以数据中心、网络和自由现金流为基础构建一朵云。当年晚些时候，ChatGPT 登场，舞台已经搭好。不幸的是，Akamai 进军 GPU 云市场的表现堪称「错失良机」的案例研究。Akamai 完全无视所有高端 GPU，只聚焦 RTX 6000 Blackwell。

不出所料，该平台没有托管 Slurm 集群，其 Kubernetes 引擎也未针对 GPU 服务器优化。

Akamai 的战略似乎聚焦于单节点、小规模推理或开发者 VM——一个人满为患的低利润市场。对一家坐拥其资源的公司来说，这种缺乏雄心让我们相当失望。

### HETZNER

Hetzner 是一家总部位于德国的受欢迎的低成本供应商，在纽伦堡、法尔肯施泰因、图苏拉运营自有设施，并在阿什本、希尔斯伯勒和新加坡设有托管机房。目前可用的 GPU 只有 RTX 4000 和 RTX 6000，可能是受其数据中心某些环境条件所限。在 Hetzner 为用户提供可组建集群的高端数据中心 GPU 之前，按我们的标准它将留在表现不佳类别。

## 暂不可用（Unavailable）

### NScale

NScale 是一家获 NVIDIA 支持的合作伙伴，在 Stargate 挪威项目中占据重要地位——我们在数据中心模型中已有详尽覆盖：<https://semianalysis.com/datacenter-industry-model/>。他们已宣布与 Microsoft 签署多份数十亿美元合同，第一份在 9 月，随后 10 月又有后续公告。这些部署面向 NVIDIA 的 GB300 机柜级方案。

遗憾的是，无论是直接、还是通过 Lightning.ai 等公开宣传的合作方，我们都未能获得 NScale 平台上任何 GPU 的访问权限。我们对这些困难深表遗憾，期待未来测试 NScale 的服务。

### Core42/G42

Core42 是 G42 的 Neocloud 部门。G42 还运营着 MGX（一只投资基金）和 Khazna（一家数据中心开发公司）。三者均总部位于阿联酋。

我们在数据中心模型及公开文章中对这些公司已有详尽覆盖，例如：<https://newsletter.semianalysis.com/p/ai-arrives-in-the-middle-east-us-strikes-a-deal-with-uae-and-ksa>。最新进展显示，一笔区区 10T 美元的「针锋相对」交易换来了出口许可获批、NVIDIA 恢复向阿联酋发运 GPU。

目前我们还无法访问并测试 Core42 提供的集群。我们对这些困难深表遗憾，期待未来测试 Core42 的服务。

### HUMAIN Compute

HUMAIN Compute 是沙特阿拉伯公共投资基金（PIF）的 Neocloud 部门。沙特 PIF 还参与了国家「2030 愿景」计划下的其他重大技术与基础设施项目。尽管已有关于其建设大规模 AI 基础设施意向的重大公告，但一个可供测试和评测的公开自助平台尚未就绪。

### Corvex

Corvex（前身 Klustr）目前运营 H200 和 B200，并计划很快扩展到 GB200 NVL72 系统。遗憾的是，在我们测试期间，Corvex 已全部售罄。

我们欣赏的是，为了服务其客户——尤其是美国涉密联邦政府机构——Corvex 严格维持 SOC 2 Type II、ISO 27001/27017/27018、PCI-DSS 和 FedRAMP 认证合规，并配备 InfiniBand 与 RoCEv2 隔离、SR-IOV 安全控制，以及自动客户通知和 CVE 补丁管理。该平台宣传具备自动化 Slurm 与 Kubernetes 开通、开箱即用的拓扑配置，以及接入 DCGM 和任务遥测的集成 Grafana 监控。

我们期待未来测试 Corvex。

### Highrise

这是加密矿企 Hut 8 的 AI 品牌。尽管已宣布超过 10GW 电力容量的宏大计划，我们始终未能获得 Highrise 上任何可供评测的 GPU。我们期待未来测试其产品。

### BluSky

BluSky 是一家小规模初创公司，通过与美国最大加密矿企之一 RIOT 的关系获得了海量电力。我们期待未来测试其产品。

### Andromeda

Andromeda 的创建初衷是充当 Nat Friedman 和 Daniel Gross（NFDG）投资组合内公司的风投支持集群，专门服务其 [AI Grant](https://aigrant.com/)（或 [AI Grant](https://aigrant.org/)）的受助者。该公司还运营着热门网站 [gpulist.ai](http://gpulist.ai)。其如今的模式是代表这些初创公司，从我们名单上的一系列 Neocloud 采购产能。实际上，他们是一家初创公司可以倚靠的「按需共享 SRE（fractional SRE）」或「按需共享采购团队」。有用户向我们描述，Andromeda 可以拿过这些集群并部署自己的编排层，主要通过 Slurm on Kubernetes，租户之间仅有轻量 namespace 隔离。看来 NFDG 组合公司之间彼此信任。

随着 Nat 和 Daniel 先是加入 SSI、如今又入职 Meta，Andromeda 的前途未卜。我们对战略风投以算力（叠加现金）支持初创公司的概念感到兴奋——这让它们有能力与超大规模云厂商、CoreWeave 和 NVIDIA NVentures 等战略方的初创扶持计划竞争。我们期待未来看到 Andromeda 的更多表现。

### Mistral

Mistral 起家时是全球领先的 AI 公司之一，钟情于开源模型、磁力链接和 le chat（是应用，不是猫）。如今算力已到手，他们又转型（或说扩展）出构建 Neocloud 的能力，纳入其公开业务，尤其聚焦欧洲的主权 AI 项目。今年夏天，Mistral 甚至请到马克龙总统与 Jensen 同台为其服务站台。正如 Jensen 在那场活动上所说：「一个国家可以外包很多东西，但把你全部的智能都外包出去毫无道理。」随着这些工作全面推进，我们期待未来测试 Mistral 的公开服务。

### Firebird

Firebird 是今年夏天在 GTC 巴黎登场的又一家供应商，获得亚美尼亚政府 $5 亿支持，计划采购 GB300 NVL72 机柜级系统，聚焦主权 AI。他们得到了亚美尼亚电信（Telecom Armenia）和爱尔兰 Imagine Broadband 的支持。虽然公开服务尚未上线，我们期待未来对其进行测试。

### TELUS

TELUS 是加拿大大型电信运营商，已在数据中心部署 GPU，但其自主的主权 AI 布局仍处于「即将上线」状态。该平台目前无法测试，不过我们预计会在即将到来的 ClusterMAX 2.1 中纳入它。令我们鼓舞的是，TELUS 将从第一天起就同时向用户提供 slurm 和 kubernetes 集群。

### Telenor

Telenor 是挪威大型电信运营商，已宣布与 NVIDIA 合作建设挪威首座「AI 工厂」。尽管早在 2025 年 2 月就发布了初始公告，该平台至今尚未上线、无法测试。挪威坐拥全球最大的主权财富基金之一、气候凉爽、绿电廉价。我们期待 Telenor 未来带给市场的东西。

### Alibaba Cloud

阿里巴巴云（Alibaba Cloud）虽是亚洲的超大规模云厂商，但其高性能现代 GPU（H100/B200）在大多数公开区域并不容易获得测试，重心主要在中国国内市场。

阿里云的托管 Kubernetes 服务名为容器服务 Kubernetes（Container Service for Kubernetes，ACK）。ACK 提供全托管方案：由阿里云负责对集群运行至关重要的控制平面（master 节点），用户只需创建并管理 worker 节点。这简化了 Kubernetes 集群的部署与运维。ACK 支持多种节点类型，包括带 GPU 等异构算力的节点，适合广泛的工作负载，尤其是 AI 与机器学习。

阿里云还在其弹性高性能计算（E-HPC）服务中提供托管 Slurm 方案。E-HPC 是一个简化高性能计算集群部署与管理的平台，其中还包括 Slurm on Kubernetes 方案，通过专用 operator 在 ACK 内部署和管理 Slurm 集群。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/99935c55-61fa-4d7b-8554-4134875c70c4_937x500.png)
*来源：中国的可用区里 GPU 选择不多*

在我们的[数据中心模型](https://semianalysis.com/datacenter-industry-model/)中，我们已覆盖阿里巴巴在泰国、墨西哥、韩国、马来西亚和菲律宾的全球扩张。巴西也有一座新数据中心在建：字节跳动（ByteDance）拟在那里追加 $100 亿，华为云计划在当地建设第 4 座数据中心，腾讯也计划进军南美。值得注意的是，滴滴、速卖通（AliExpress）、Shein 和许多中国车企也在向巴西扩张。阿里云正抢在起跑阶段进场，帮助巴西从零构建其 AI 产业。

未来我们非常有兴趣测试阿里云的体验。其软件控制台显然相当精良，并经全球最大的一批 AI 公司验证过规模。我们将持续紧密追踪这家 Neocloud 在地缘政治上的姿态。

### ARC Compute

ARC Compute 有着向加拿大客户部署 H100、H200、B200 和 B300 各代 HGX GPU 服务器的履历。不幸的是，ARC 也吃了不少官司：从起诉两名被抓到窃取源代码、招揽客户的离职员工，到涉嫌在服务器销售中违反美国出口管制。其网站上宣传 InfiniBand 互连的 H100 集群低至每小时 $1.45，对任何能接触到并测试的人来说都颇具吸引力。遗憾的是，我们未能获得访问权限开展测试。

### MegaSpeed

《纽约时报》最近对 Megaspeed 做了一些报道，但不知何故没有点出阿里巴巴是其主要客户。Megaspeed 总部位于新加坡，我们在[数据中心模型](https://semianalysis.com/datacenter-industry-model/)中已追踪其在马来西亚的大规模建设有一段时间了。

我们未能访问任何 Megaspeed 云服务来进行测试。

### Bitdeer

Bitdeer 是一家总部位于新加坡的公司，从比特大陆（Bitmain）分拆而来——后者是中国最大的加密矿企，也销售挖矿专用 ASIC。Bitdeer 运行着大量这类 ASIC，如今也做起了 Neocloud。其平台包括遍布全球的站点：新加坡、马来西亚、印度尼西亚、冰岛、荷兰、加拿大和美国。

![电脑截图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/96bde92c-288b-48aa-af4e-fecc450e4184_936x485.png)

我们登录测试时，马来西亚、美国、冰岛和荷兰名义上有 H100 可用，新加坡还有 B200 和 H100。Bitdeer 网站声称已取得 SOC2 Type I 和 ISO/IEC 27001:2022 合规，这本应让他们轻松上榜。然而 Bitdeer 设有咄咄逼人的 KYC 流程，使我们在测试期间无法租用 GPU。因此，我们无法就其按需 GPU 云平台验证任何东西。

有意思的是，Bitdeer 按 VM 对带宽收取不同费用，速率从 1Mb/s 到 1024 Mb/s，可按固定或按量流量计费。在重度使用场景下，这会让他们平台上 1x B200 VM 的成本从每小时 $4.69 翻倍至 $8.27。

抛开实测不谈，Bitdeer 还有一些宏大计划。其位于俄亥俄州马西隆（Massillon）的站点最近接受了第三方可行性评估，评估其是否适合建设 Tier 3 HPC/AI 数据中心，结果报告「大体积极（……），得益于土地、电力、光纤和水资源的可得性」。我们注意到，这份报告对既有建筑只字未提，这很有意思。看起来 Bitdeer 和其他加密矿企一样，计划推倒既有建筑，把这块带电土地用于崭新的 AI 云建筑，最终以带电壳体（powered shell）或托管（colo）形式出售，在成本之上赚取 10-15% 的利润率。

![仓库鸟瞰图
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/8ca6c597-11b7-46f8-a52e-2454732b20ac_936x706.png)
*来源：SemiAnalysis 数据中心模型*

### Runsun

Runsun 是一家总部位于新加坡的供应商，GPU 部署在日本和美国，并计划很快扩展到韩国、澳大利亚和欧洲。Runsun 声称以裸金属服务形式部署了超过 10,000 块 GPU。目前我们未能获得任何可供测试的资源，但期待未来测试 Runsun 的云服务。

### FPT CLOUD

东南亚一家大型区域供应商，在越南和日本拥有可观产能，并在整个地区建有伙伴关系。我们未能在本文发稿前获得集群访问权限，但预计很快会在 ClusterMAX 2.1 中纳入他们。敬请期待。

### Backend

Backend 是一家韩国 Neocloud，拥有众多似乎能简化集群上手的软件产品。我们欣赏 Backend 的灵活性——它显然支持客户在其本地（on-prem）、其云上或开发者工作站上运行软件栈。目前来看，Backend 缺少可观的算力容量，其公有云服务仍处于 beta 阶段、需邀请才能测试。我们期待未来测试 Backend。

### Naver

Naver 实际上就是「韩国的 Google」，这要归功于其在搜索、博客、论坛、电商、支付等领域的成功。Naver 最近刚刚公开了其推出 Neocloud 的计划，这在很大程度上要感谢 Jensen 的首尔之行以及与 HBM 制造商 SK Hynix 和三星的会面。这个新云项目将总计部署约 260,000 块 GPU：其中 60,000 块给 Naver 用于公有云服务，另外 200,000 块在三星、SK、现代（Hyundai）和 Naver 内部工作负载之间分配。

值得注意的是，Naver 已在运营一朵云，拥有一个成果丰硕的大型研究组织，并已具备基础设施来哺育韩国的初创和学术生态。我们期待未来测试 Naver 的 GPU 云产品。

### Indosat

印度尼西亚大型电信运营商，已与 NVIDIA 签署 MOU，将成为印尼首个经认证的 NVIDIA 云合作伙伴。该平台尚未上线，无法测试。

### SAKURA

日本重要的主权 AI 云，与 KDDI 和 HPE 就大型 Blackwell 集群签有重大 MOU。其公开的自助 AI 云平台尚未开放测试。

### Yotta

Yotta 的 Shakti Cloud（不要与同名的数据中心行业会议「Yotta」混淆）是印度主权 AI 浪潮的先行者，用 Jensen 的话说，是他「最喜欢的亚洲云」。Yotta 已宣布 Shakti 中部署了超过 16,000 块 H100 GPU，Blackwell 正在部署中、后续还有更多。这让 Yotta 保持着印度 GPU 数量最多的地位——到 2025 年底总计 32,768 块。

我们对至今测试 Yotta 云服务所遭遇的困难深表遗憾，期待在即将到来的 ClusterMAX 2.1 中纳入其测试。

### Neev Cloud

Neev Cloud 是另一家印度 Neocloud，遗憾的是他们不愿让我们测试其服务——尽管其计划在 $15 亿投资支持下，到 2026 年在中印度印多尔（Indore）部署 40,000 块 GPU。首笔订单于 2024 年年中向 HPE 下达，共 8,000 块 GPU，并计划扩展至金奈、孟买、海得拉巴和诺伊达。

其网站声称有 1,000 到 16,000 块 GPU 经 InfiniBand 互联，H200、B200 和 B300 均可「预预留（pre-reservation）」。首页上一张 Neev Cloud CEO 与莫迪握手的醒目合影，让我们推断 Neev 将主要服务印度主权客户。不过，kubernetes 和 slurm 集群似乎无法供测试。印度是一个拥有活跃科技生态的大国，但究竟有多少 Neocloud 能走下去，尚不明朗。

### Evroc

Evroc 又是一家建设 Neocloud 的欧洲公司，聚焦可持续性与主权。Evroc 总部位于斯德哥尔摩，计划在阿兰达斯塔德（Arlandastad）和戛纳建设数据中心，并在巴黎、斯德哥尔摩和法兰克福拥有伙伴。其规划涉及多达 10,000 块 GPU 的 GB300 NVL72。目前我们未能测试 Evroc 的任何云服务，但期待未来测试这朵「世界最清洁的云」。

### greenai.cloud

GreenAI Cloud 是又一家总部位于瑞典、聚焦可持续性与主权的云供应商。GreenAI 特别宣称「CO2 负排放计算」，主要服务国防、情报、健康与科学领域对安全高度敏感的政府机构。其已落实 Schrems II 合规，并拥有 Level 4 级安全设施。A100、H100、H200 和 B200 GPU 均可用，但没有 GB200 NVL72。有意思的是，与 Cerebras 昙花一现的合作似乎已不了了之，greenai 团队强调绝不会再与该公司做生意。我们尚未有机会测试 greenai 的任何云服务，但希望未来能有机会。

# 免责声明

*本文展示的各徽标及相关商标仅出于编辑与信息目的，符合适用法律下合理使用（fair use）的原则。本文不明示或暗示任何相关公司存在所有权、隶属关系、赞助或背书关系。各徽标及相关商标的全部权利、权属与利益仍归各公司专有。*

*ClusterMAX™ 呈现的内容、方法论与数据为 SemiAnalysis 的知识产权。任何全部或部分使用本作品用于金融产品的创建、构造、发行或估值——包括但不限于衍生工具、投资基金、指数、交易所交易产品或结构性票据——均须事先获得作者书面同意。*

*未经授权用于商业或金融目的，包括基于这些评级创建衍生或投资工具，均被严格禁止。授权垂询与合作提案可发送至 clustermax@semianalysis.com*
