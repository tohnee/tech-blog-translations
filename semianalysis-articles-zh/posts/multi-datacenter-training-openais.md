---
title: "多数据中心训练：OpenAI 击败 Google 基础设施的雄心计划"
title_en: "Multi-Datacenter Training: OpenAI's Ambitious Plan To Beat Google's Infrastructure"
subtitle: "吉瓦级集群、电信网络、长途光纤、分层与异步 SGD、分布式基础设施的赢家"
date: 2024-09-04
source: https://newsletter.semianalysis.com/p/multi-datacenter-training-openais
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball", "Jeremie Eliahou Ontiveros"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 多数据中心训练：OpenAI 击败 Google 基础设施的雄心计划

> 原文：[Multi-Datacenter Training: OpenAI's Ambitious Plan To Beat Google's Infrastructure](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**吉瓦级集群、电信网络、长途光纤、分层与异步 SGD、分布式基础设施的赢家**

由于持续为 scaling laws 输送燃料所带来的不断进步，AI 基础设施的建设胃口永无止境。今年，前沿 AI 模型的训练集群[已扩展到 10 万块 GPU](https://www.semianalysis.com/p/100000-h100-clusters-power-network)，2025 年 30 万块以上 GPU 的集群也在规划之中。鉴于施工周期、许可审批、法规以及[电力供应](https://www.semianalysis.com/p/ai-datacenter-energy-dilemma-race)等诸多物理约束，在单一数据中心站点上对大模型进行同步训练的传统方法正接近临界点。

Google、OpenAI 和 Anthropic 已经在执行将大模型训练从单一站点扩展到多个数据中心园区的计划。[Google 拥有当今世界最先进的计算系统](https://www.semianalysis.com/p/google-ai-infrastructure-supremacy)，并率先大规模应用了许多如今才刚刚被其他公司采用的关键技术，例如其机柜级液冷架构和多数据中心训练。

Gemini 1 Ultra 就是在多个数据中心上训练的。尽管可用的 FLOPS 更多，Google 现有的模型仍落后于 OpenAI 和 Anthropic，因为他们在合成数据、强化学习（RL）和模型架构方面仍在追赶，但即将发布的 Gemini 2 将改变这一局面。此外，到 2025 年，Google 将具备跨多个园区进行吉瓦级训练的能力，但令人意外的是，Google 的长期计划远不如 OpenAI 和 Microsoft 激进。

![](https://substack-post-media.s3.amazonaws.com/public/images/0dbb178d-6bbd-4b40-843d-eea46d1c2491_1390x788.png)
*来源：Google*

大多数公司才刚刚通过 [Nvidia 的 GB200 架构](https://www.semianalysis.com/p/gb200-hardware-architecture-and-component)接触高密度液冷 AI 芯片，该架构计划明年爬坡至数百万颗。而 Google 已经部署了数百万颗液冷 TPU，占用的液冷 AI 芯片产能超过 1 吉瓦（GW）。Google 基础设施与其竞争对手之间的巨大差距肉眼可见。

![](https://substack-post-media.s3.amazonaws.com/public/images/44d62018-5fba-4ed2-9bda-e78aaacdb1cd_2042x1528.png)
*来源：SemiAnalysis 数据中心模型*

上图所示的 AI 训练园区电力容量已接近 300MW，明年将爬坡至 500MW。除了规模庞大之外，这些设施的能效也非常高。在下图中我们可以看到大型冷却塔和集中式设施水系统，水管连接三栋建筑，可带走接近 200MW 的热量。这套系统让 Google 在一年中的大部分时间无需开启冷水机组，根据最新的环境报告，2023 年实现了 1.1 的 PUE（电源使用效率）。

![](https://substack-post-media.s3.amazonaws.com/public/images/c3d0e1e0-4cdf-4877-b9c9-b48913d5844c_2136x1442.png)
*来源：Google*

虽然上图仅展示了设施水系统，但水还会通过冷板式直冷（Direct-to-Chip）系统输送至机柜，由液-液（Liquid-to-Liquid）热交换器将热量从机柜传递到中央设施水系统。这套能效极高的系统与 Nvidia GB200 的 L2L 部署方式类似——我们的 [GB200 深度解析](https://www.semianalysis.com/p/gb200-hardware-architecture-and-component)中有详细描述。

另一方面，下图所示的 Microsoft 当今最大的训练集群不支持液冷，尽管建筑总建筑面积（GFA）大致相当，每栋建筑的 IT 容量却低了约 35%。公开数据显示其 PUE 为 1.223，但 PUE 的计算方式对风冷系统有利，因为服务器内部的风扇功耗没有被正确计入——风冷 H100 服务器的这部分占服务器功耗的 15% 以上，而液冷（DLC）服务器则不到 5%。因此，每向芯片输送 1 瓦功率，Microsoft 需要额外约 45% 以上的电力用于服务器风扇、设施制冷及其他非 IT 负载，而 Google 每瓦 IT 功率的额外负载接近约 15%。再叠加 TPU 更高的能效，局面就更加难看了。

![](https://substack-post-media.s3.amazonaws.com/public/images/6126c5fb-b453-4f12-b87f-869eb0b35953_1570x1406.png)
*来源：SemiAnalysis 数据中心模型*

此外，为了在（亚利桑那州的）沙漠中获得尚可的能效，Microsoft 需要消耗大量的水——其用水效率（WUE，升/千瓦时）高达 2.24，远高于 0.49 的集团平均值，也远高于略高于 1 的 Google 平均值。这种高用水量已引发媒体的负面关注，他们已被要求在该园区即将建设的数据中心中改用风冷冷水机组，这将降低每栋建筑的用水量，但会进一步推高 PUE，拉大与 Google 的能效差距。在未来的报告中，我们将更详细地探讨数据中心的运作方式以及超大规模云厂商的典型设计。

因此，基于现有的数据中心参考设计，Google 的基础设施效率要高得多，扩建 MW 的速度也快得多，因为其每栋建筑的容量高出 50% 以上，且每单位 IT 负载需要签约的市电电力更少。

# **Google 的 AI 训练基础设施**

Google 在基础设施建设上始终有独到之处。虽然其单个数据中心的设计如今已比 Microsoft、Amazon 和 Meta 更先进，但这仍未完全体现其基础设施优势的全貌。Google 建设大规模园区已有十余年历史。下图所示的 Google 艾奥瓦州康瑟尔布拉夫斯（Council Bluffs）站点就是一个很好的例证：[尽管已建成多年，其西侧部分仍拥有接近 300MW 的 IT 容量](https://www.semianalysis.com/p/datacenter-model)。虽然相当一部分容量分配给了传统工作负载，但我们认为[位于底部的建筑部署了大量 TPU](https://www.semianalysis.com/p/accelerator-model)。采用最新数据中心设计的东侧扩建将进一步增加 AI 训练容量。

![](https://substack-post-media.s3.amazonaws.com/public/images/176e42e8-ba17-4faa-9097-5be88dc4fb69_2764x1276.png)
*来源：SemiAnalysis 数据中心模型*

Google 最大的 AI 数据中心彼此之间也相距很近。Google 拥有 2 个主要的多数据中心区域，分别位于俄亥俄州和艾奥瓦州/内布拉斯加州。如今，康瑟尔布拉夫斯周边区域正在积极扩建，规模将超过现有容量的两倍。除上述园区外，Google 在该区域还拥有另外三个站点，它们都已在建设中，并且都在升级高带宽光纤网络。

![](https://substack-post-media.s3.amazonaws.com/public/images/a135b0e2-6fcc-43d8-bbe3-5a68f4bf509b_2009x1503.png)
*来源：SemiAnalysis 数据中心模型*

有三个站点彼此相距约 15 英里（康瑟尔布拉夫斯、奥马哈和帕皮利恩），另有约 50 英里外内布拉斯加州林肯市的一个站点。下图所示的帕皮利恩（Papillion）园区为 Google 在奥马哈和康瑟尔布拉夫斯周边的业务新增了超过 250MW 的容量，加上前述园区，2023 年合计容量超过 500MW，其中很大一部分分配给了 TPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/2a49570b-55a5-4a28-91e8-0594b828e3c3_2800x1186.png)
*来源：SemiAnalysis 数据中心模型*

另外两个站点目前规模尚不及前者，但正在快速爬坡：到 2026 年，四个园区合计将形成 GW 级的 AI 训练集群。约 50 英里外的林肯数据中心将成为 Google 最大的单一站点。

Google 庞大的 TPU 版图还不止于此。另一个即将建成的 GW 级集群位于俄亥俄州哥伦布市周边——该区域正在上演类似的主题：三个园区同步开发，到 2025 年底合计达到 1 吉瓦！

![](https://substack-post-media.s3.amazonaws.com/public/images/8be09263-1051-4aa5-b6ee-79a6cc96b8f1_1888x1446.png)
*来源：SemiAnalysis 数据中心模型*

下图所示的新奥尔巴尼（New Albany）集群将成为 Google 最大的集群之一，并且已经在承载 TPU v4、v5、v6。

![](https://substack-post-media.s3.amazonaws.com/public/images/45b08c99-ac21-409e-ab5e-f3f7662a5439_2042x1528.png)
*来源：SemiAnalysis 数据中心模型*

Google 俄亥俄区域与艾奥瓦/内布拉斯加区域还可以进一步互联，为训练单一模型提供数吉瓦的电力。我们在[数据中心模型](https://www.semianalysis.com/p/datacenter-model)中提供了 5,000 多个数据中心的精确季度历史及预测电力数据，涵盖 AI 实验室、超大规模云厂商、新兴 GPU 云（neocloud）和企业的集群建设状态。关于多数据中心训练的软件栈和方法，本报告后文会详细展开。

# **Microsoft 与 OpenAI 的反击？**

Microsoft 和 OpenAI 非常清楚自己在近期基础设施方面的劣势，并已启动一项雄心勃勃到极点的基建计划，以求在建设规模上压过 Google。他们试图在 Google 自己最擅长的游戏——水冷多数据中心训练集群——中击败 Google。

Microsoft 和 OpenAI 正在建设接近吉瓦级的超高密度液冷数据中心园区，同时与 [Oracle、Crusoe、CoreWeave、QTS、Compass 等公司](https://www.semianalysis.com/p/datacenter-model)合作，以获得超过 Google 的 AI 训练与推理总容量。

其中一些园区建成后，将比 Google 今天任何一个单一园区都大。事实上，Microsoft 在威斯康星州的园区将超过 Google 俄亥俄州所有站点的总和，但它的建设[需要一些时间](https://www.semianalysis.com/p/datacenter-model)。

更加雄心勃勃的是 OpenAI 与 Microsoft 将多个超大规模园区互联起来、在全国范围内运行巨型分布式训练的计划。Microsoft 和 OpenAI 将率先建成多 GW 级计算系统。他们正与供应链伙伴一起，深入参与[有史以来最宏大的基础设施建设](https://www.semianalysis.com/p/microsoft-infrastructure-ai-and-cpu)。

本报告将在接近结尾处详细介绍 Microsoft 和 OpenAI 的基础设施建设。在此之前，将首先介绍多园区同步与异步训练方法、掉队者（straggler）、容错、静默数据损坏（SDC）以及多数据中心训练面临的各种挑战。

随后我们将解释数据中心互联（DCI）以及数据中心之间的城域和长途连接如何通过光纤电信网络实现，包括技术和设备两个层面。

最后，我们将探讨电信供应链，讨论 AI 基础设施建设下一阶段的关键受益者，包括我们认为哪些公司对此的杠杆敞口最大。

# **多数据中心分布式训练**

在深入 Microsoft 和 OpenAI 的基础设施建设之前，先讲一点分布式训练的基础知识。大语言模型（LLM）主要采用同步方式训练。训练数据通常被切分为若干更小的 mini-batch，每个 mini-batch 由运行在不同 GPU 组上的独立数据副本（data replica）处理。处理完一个 mini-batch 后，每个副本计算出梯度，随后所有副本必须在每个 mini-batch 处理结束时进行同步。

这种同步涉及聚合来自所有副本的梯度，通常通过 all-reduce 之类的集合通信操作完成。梯度聚合后取平均，用于一致地更新模型参数。这确保所有数据副本维持完全相同的参数，使模型能够稳定收敛。这一过程的「齐步走」特性——所有设备彼此等待完成后再进入下一步——保证了没有任何设备在模型状态上领先或落后太多。

![](https://substack-post-media.s3.amazonaws.com/public/images/ac0f23d2-9fac-4951-81ee-b47816639562_1709x835.png)
*来源：Preferred Networks*

虽然同步梯度下降能带来稳定收敛，但也引入了严峻挑战，尤其是当单个训练作业的规模扩展到 10 万颗以上芯片时，通信开销会显著增加。同步的特性还意味着对延迟有严格要求，并且必须有一条大管道连接所有芯片，因为数据交换是以巨大突发的方式进行的。

当你尝试将多个区域的 GPU 用于同一个训练工作负载时，它们之间的延迟会增加。即使以光在光纤中 208,188 km/s 的速度传播，从美国东海岸到西海岸的往返时间（RTT）也有 43.2 毫秒（ms）。此外，各类电信设备还会引入额外延迟。这是一个相当可观的延迟量，对标准同步训练来说很难克服。

根据阿姆达尔定律（Amdahl's Law），当存在大量同步活动时，为一个工作负载增加更多芯片所带来的加速收益会递减。随着芯片数量的增加，如果程序运行时间中需要同步的部分（即对应于计算中保持串行、无法并行化的比例）保持不变，你就会达到一个理论极限：即使 GPU 数量翻倍，总吞吐量的提升也不到 1%。

![](https://substack-post-media.s3.amazonaws.com/public/images/1b25028f-8072-4190-aac9-012cb2edb1b6_823x620.png)
*来源：Wikipedia*

除了阿姆达尔定律所描述的向单一工作负载扩展更多 GPU 的理论极限外，同步梯度下降还存在掉队者（straggler）等实际挑战。只要有一颗芯片慢了 10%，就会导致整个训练运行慢 10%。例如，在下图中，从第 7,500 步到第 19,000 步，字节跳动（ByteDance）发现其 MFU 缓慢下降，因为工作负载中的芯片一颗接一颗地变得略微偏慢，整个工作负载逐渐被掉队者拖累。

![](https://substack-post-media.s3.amazonaws.com/public/images/899e7918-9dcc-48af-a775-74cc1eef58d4_1291x584.png)
*来源：ByteDance*

在识别并移除掉队者后，他们从检查点（checkpoint）重启了训练工作负载，使 MFU 恢复到正常水平。可以看到，MFU 从 40% 降到了 30%，降幅达 25%。当你拥有 100 万块 GPU 时，MFU 下降 25% 相当于任何时刻都有 25 万块 GPU 在空转，仅 IT 资本开支一项的等价成本就超过 100 亿美元。

# **容错训练**

容错训练是所有分布式系统不可或缺的组成部分。当数以百万计的计算、内存和存储元件同时工作时，[总会出现故障，甚至在各种「完全相同」的系统之间也存在性能差异——这就是所谓的「硅抽奖」（silicon lottery）](https://arxiv.org/pdf/2009.06489)。系统设计本来就是要应对这些情况的。但与直觉相反，在全球最大的计算问题——机器学习训练——中，采用的却是完全相反的思路。

所有芯片都必须完美工作，因为在 10 万块 GPU 中哪怕只坏一块，这块 GPU 就会导致全部 10 万块 GPU 从检查点重启，带来极其惊人的 GPU 空闲时间。而在容错训练下，单块 GPU 故障时只有少数几块其他 GPU 受影响，绝大多数 GPU 继续正常运行，无需从模型权重检查点重启。LLAMA 3.1 等开源模型就曾因此烧掉大量的成本和时间。

Nvidia 的 InfiniBand 网络同样存在这种可能有缺陷的原则：每个数据包都必须严格按同样的顺序送达。任何乱序或故障都会导致数据重传。正如[10 万 GPU 集群报告](https://www.semianalysis.com/i/145735023/reliability-and-recovery)中所提到的，仅网络故障的度量单位就是分钟级而非小时级。

实现容错训练的主要开源库叫 TorchX（前身为 TorchElastic），但它存在明显缺点：既没有覆盖各种故障场景的长尾，也不支持 3D 并行。这导致几乎每一家大型 AI 实验室都在自研容错训练系统。

不出所料，容错基础设施的领导者 Google 通过 [Borg](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/) 和 [Pathways](https://arxiv.org/pdf/2203.12533) 拥有最佳的容错训练实现。这些库覆盖的极端案例最多，并且是紧密垂直整合的一部分：Google 既设计自己的训练芯片，也制造自己的服务器、编写自己的基础设施代码，同时还进行模型训练。这类似于造车：垂直整合程度越高，就越能快速定位制造问题的根因并加以解决。Google 几年前的 Pathways 系统正是其实力的证明，我们将在本报告后文中详述。

总体而言，在将 10 万块以上 GPU 的集群扩展用于单一工作负载时，容错是最需要解决的方面之一。Nvidia 在 AI 系统可靠性方面远远落后于 Google，这也正是 NVIDIA 招聘职位描述中反复提到容错的原因……

![](https://substack-post-media.s3.amazonaws.com/public/images/3076ef35-e7ac-4bb6-9b93-7252fc8b5d0a_634x158.png)
*来源：Nvidia Workday*

在 CPU 的世界里，容错基础设施基本上已是解决的问题。例如，Google 的自研数据库 [Spanner](https://research.google/pubs/spanner-googles-globally-distributed-database-2/) 运行着包括 YouTube、Gmail 和 Stadia（RIP）在内的 Google 几乎所有生产服务，能够在全球范围内分布式扩展，并对存储服务器和 NVMe 磁盘故障保持容错。Google 数据中心里每小时都有数百块 NVMe 磁盘损坏，但无论对最终客户还是内部而言，Spanner 的性能和可用性始终保持不变。

大规模集群上传统 CPU 工作负载容错的另一个例子是 [MapReduce](https://storage.googleapis.com/gweb-research2023-media/pubtools/4449.pdf)。MapReduce 是一种建模方式：用户对数据样本进行处理即「map」（映射），并将多个数据样本归并为一个聚合值即「reduce」（归约）。例如，统计一篇文章中有多少个字母「W」就是 map-reduce 的绝佳理论工作负载：对每个单词做 map，map 阶段输出每个数据样本中字母「W」的数量，而「reduce」阶段则聚合所有样本中「W」的数量。MapReduce 可以通过检测哪些 CPU worker 节点损坏，并在其他 CPU worker 节点上重新执行失败的 map 和 reduce 任务来实现容错。

![](https://substack-post-media.s3.amazonaws.com/public/images/1d1607ed-d123-4dd3-9dc0-a15083e9479e_1062x793.png)
*来源：Google*

CPU 领域相当一部分容错研究和系统出自 Jeff Dean、Sanjay Ghemawat 以及 Google 的众多其他世界级分布式系统专家之手。随着机器学习训练规模越来越大、对容错 ML 训练系统的要求越来越高，这种构建健壮可靠系统的专业能力将成为 Google 的竞争优势之一。

一般来说，GPU 故障遵循浴缸曲线：大部分故障发生在集群寿命的初期（即早期失效）和末期。这正是全集群老化测试（burn-in）极其重要的原因。遗憾的是，由于一心想在集群寿命周期内榨取最多收益，相当一部分 AI 新兴 GPU 云（neocloud）并没有对集群进行妥善的老化测试，导致终端用户体验极差。

相比之下，在超大规模云厂商和大型 AI 实验室，大多数集群会在高温和快速波动的温度下进行相当长时间的老化测试，以确保所有早期失效都已过去、进入随机失效阶段。充足的老化时间必须与 GPU 和光收发器度过早期问题之后的可用寿命消耗相平衡。

耗损失效阶段是指元件在寿命末期因疲劳而失效，通常源于 7×24 小时使用期间中高温与高温之间的快速波动。光收发器尤其因剧烈的热循环而磨损严重。

![](https://substack-post-media.s3.amazonaws.com/public/images/9d10f901-4a37-470f-8a22-dc21250aaaf7_1193x805.png)
*来源：SemiAnalysis*

在 CPU 领域，当承载虚拟机（VM）的物理主机出现错误率上升的迹象时，在物理主机之间迁移虚拟机是很常见的做法。超大规模云厂商甚至掌握了在终端用户毫无察觉的情况下在物理主机之间热迁移虚拟机的方法。其通常做法是在后台复制内存页，然后当用户应用出现一瞬间的变慢时，将 VM 快速切换到第二台正常运行的物理主机上。

![](https://substack-post-media.s3.amazonaws.com/public/images/d6ce8a24-0589-4130-9b20-e55b971df60b_1456x738.png)
*来源：SemiAnalysis*

有一个名为 CRIU（Checkpoint/Restore In Userspace，用户态检查点/恢复）的主流 Linux 软件包，被 Docker、Podman 和 LXD 等主流容器引擎使用。CRIU 可以在物理主机之间迁移容器和应用程序，甚至能冻结整个进程状态并将其检查点到存储磁盘上。很长一段时间里，CRIU 只能在 CPU 和 AMD GPU 上使用，因为 Nvidia 一直拒绝实现该功能，直到今年才改变。

随着 2024 年初起 Nvidia GPU 开始支持 GPU CRIU 检查点，现在可以以顺畅得多的方式把 CPU 进程状态、内存内容和 GPU 进程从一台物理主机迁移到另一台。

![](https://substack-post-media.s3.amazonaws.com/public/images/8e4adb25-6051-4dc0-9623-652bc7024f34_1421x714.png)
*来源：SemiAnalysis*

在 [Microsoft 的 Singularity 集群管理器论文](https://arxiv.org/pdf/2202.07848)中，作者描述了利用 CRIU 对 GPU 虚拟机进行透明迁移的方法。Singularity 还从零开始设计，以支持全局式的 GPU 工作负载调度和管理。该系统已被用于 Phi-3 训练（1024 块 H100）以及许多其他模型。这是 Microsoft 在追赶 Google 垂直整合的 Borg 集群管理器。

![](https://substack-post-media.s3.amazonaws.com/public/images/a3b3f5f6-f8eb-4e7f-80da-aec36eacfc0d_859x874.png)
*来源：Microsoft*

遗憾的是，正因为容错训练如此重要，相关方法的对外发表实际上已经停止。当 OpenAI 等公司向硬件行业讲述这些问题时，他们的表述都非常含糊、高度概括，以免泄露任何分布式系统的诀窍。需要明确的是，这些技术比模型架构更重要，因为两者都可以被视为计算效率的一部分。

![](https://substack-post-media.s3.amazonaws.com/public/images/43fc2632-ba22-43e4-8043-65281f93ee3c_957x506.png)
*来源：OpenAI*

另一个常见问题是静默数据损坏（Silent Data Corruption，SDC），它会导致计算机在处理结果中无意间产生无声的错误，而不向用户或管理员发出任何警报。这是一个极难解决的问题，因为「静默」字面意义上就意味着错误难以察觉。这些静默错误在很多情况下可能无关紧要，但也可能使输出畸变为 NaN（「Not A Number」，非数）或使输出梯度变得极大。如下方 Google 的 Jeff Dean 给出的梯度范数图所示，有些 SDC 在绘成图表后表现为梯度范数尖峰，很容易肉眼识别，但也有其他 SDC 无法用这种方法检测出来。

也存在并非由硬件 SDC 引起的梯度范数尖峰，它们实际上源于一大批异常数据，或学习率、初始化方案等超参数未得到妥善调校。所有运营 GPU 集群的公司都会经常遇到 SDC，但由于资源有限，通常恰恰是中小型 neocloud 无法快速识别和修复这些问题。

对于 Nvidia GPU，有一款名为 DCGMI Diagnostics 的工具可以帮助诊断 SDC 等 GPU 错误。它能捕获相当一部分常见 SDC，但遗憾的是会漏掉很多导致数值错误和性能问题的极端案例。

我们在对来自多家 neocloud 的 H100 进行自测时遇到过这样的情况：DCGMI 诊断级别 4 通过，但 NVSwitch 的算术逻辑单元（ALU）工作不正常，导致在使用 NVLS NCCL 算法时出现性能问题和错误的 all-reduce 结果。我们将在即将发布的 NCCL/RCCL 集合通信文章中深入探讨我们的测试发现。

相比之下，Google 的 Pathways 在识别和解决 SDC 方面表现出色。由于 Google 基础设施与训练栈的垂直整合，他们可以在启动大规模训练工作负载之前，轻松地把 SDC 检查作为收尾（epilogue）和开场（prologue）环节执行。

![](https://substack-post-media.s3.amazonaws.com/public/images/2a5ac612-e358-44da-88c0-0b8c2dd817ab_1243x695.png)
*来源：Google*

异步训练曾经是一种广泛使用的训练技术。2012 年，Google Brain 著名的「100 倍工程师」Jeff Dean 发表了一篇名为 [DistBelief](https://research.google/pubs/large-scale-distributed-deep-networks/) 的论文，描述了在数千个 CPU 核心组成的集群上训练深度学习模型的异步（"Async"）与同步（"Sync"）梯度下降技术。该系统引入了全局「参数服务器」，并被广泛应用于生产环境，训练 Google 的自动补全、搜索和广告模型。

![](https://substack-post-media.s3.amazonaws.com/public/images/3ff776a0-30f1-494d-baff-c2c27aad6449_850x321.png)
*来源：ResearchGate*

这种参数服务器风格的训练在当时对模型的效果非常好。然而，由于较新的模型架构带来收敛性挑战，各家都简化了训练，回归到完全同步梯度下降。当前和以往的前沿级模型，如 GPT-4、Claude、Gemini 和 Grok，全都采用同步梯度下降。但为了继续扩大单次训练所用的 GPU 数量，我们认为目前正出现向异步梯度下降的回归。

# **训练策略**

在阿姆达尔定律下，规避增加芯片收益递减的一种方法是减少程序之间所需的全局同步次数，让工作负载中更大的占比（半）独立地运行。可以想象，这与多园区、多区域和跨大洲训练非常契合，因为不同 GPU 之间存在延迟和带宽的层级结构。

在园区内的各栋建筑之间（距离很近，不到 1km），延迟非常低、带宽非常高，因此可以更频繁地同步。相比之下，在同一区域内（100km 以内），带宽可能很充裕，但延迟更高，你会希望降低同步频率。此外，各园区拥有不同数量的 GPU 也是可以接受的，因为它们之间做负载均衡相当容易。例如，若园区 A 有 10 万块 GPU 而园区 B 只有 7.5 万块，那么园区 B 的 batch size 大约会是园区 A 的 75%，做同步时则对不同园区取加权平均。

![](https://substack-post-media.s3.amazonaws.com/public/images/16c78adf-aafe-40a7-82c4-e1ca45d6c9ad_990x660.png)
*来源：SemiAnalysis*

这一原则同样适用于延迟更高的多区域之间和跨大洲场景，因此同步频率还应更低。实质上——同步是分层的。

打个比方，这就像你会更常见到距离较近的朋友，其次才是同一条海岸线上其他城市的朋友，而你见到同一海岸线上朋友的频率又高于其他大洲城市里的朋友。

![](https://substack-post-media.s3.amazonaws.com/public/images/0cc0e8ac-0a4f-464c-ab0b-520c832f81b3_1800x620.png)
*来源：PyTorch*

此外，分层同步梯度下降（SGD）的另一个好处是有助于缓解掉队者问题，因为大多数掉队者通常只在少数几步中出现，随后便恢复正常性能；同步次数越少，掉队者在性能异常期间破坏同步过程的机会就越少。由于并非每次迭代都进行全局同步，掉队者的影响也就不那么突出。分层 SGD 是近期多数据中心训练中非常普遍的创新。

![](https://substack-post-media.s3.amazonaws.com/public/images/da26e025-38ae-45d7-a82c-d8743171be56_1600x1204.png)
*来源：PyTorch*

另一种有前景的方法是重新启用 Jeff Dean 2012 年 [DistBelief](https://research.google/pubs/large-scale-distributed-deep-networks/) 论文中讨论的异步参数服务器。模型的每个副本处理自己的一批 token，每隔若干步，每个副本与参数服务器交换数据并更新全局权重。这就像 git 版本控制：每个程序员先在自己的任务上工作几天，然后合并到 master（现在叫 main）分支。这种方法的朴素实现很可能带来收敛问题，但 OpenAI 将能借助各种优化器创新，解决本地模型副本向参数服务器交换数据时的更新问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/f2f22bdf-0d4a-4a93-8ba4-c7972d7a4078_437x307.png)
*来源：Research Gate*

MetaAI 的 Branch-Train-Merge 论文描述了类似思路：从现有 LLM（master 分支）分叉，在数据集子集上训练，再合并回 master 分支。我们认为这一方法的经验将被融入 OpenAI 等公司最终采用的多园区训练技术中。Branch-Train-Merge 及类似方法的主要挑战在于，对 GPT3 175B 或 GPT4 1.8T 这类规模的现代大模型来说，合并并非已解决的问题。为了维持收敛，还需要投入更多工程资源来管理合并和更新 master 分支。

![](https://substack-post-media.s3.amazonaws.com/public/images/76a7711c-4fd9-434f-a737-9ddad90ed18c_1276x615.png)
*来源：Meta*

要将其扩展为分层方法，还需要建立多层级参数服务器，数据不仅在模型副本与最近的参数服务器之间交换，也在参数服务器彼此之间交换。在最底层，各个模型副本与最近的参数服务器通信，较频繁地执行更新，以确保本地组内更快的收敛与同步。

这些本地参数服务器将组成更高的层级，每一层先聚合和提炼来自下层的更新，再向上传播。由于涉及的 GPU 数量庞大，参数服务器可能需要以 FP32 保存主权重。这类似于 Nvidia 推荐的 FP8 训练方式：以 FP32 保存主权重，以免在大量 GPU 累加时溢出；而在做矩阵乘法之前，训练服务器会降精度（downcast）到 FP8 以提高效率。我们认为这一配方依然成立：参数服务器中的主权重为 FP32，但[实际计算将以 FP8 甚至更低的格式（如 MX6）进行](https://www.semianalysis.com/p/neural-network-quantization-and-number)。

![](https://substack-post-media.s3.amazonaws.com/public/images/cc151aa7-6468-4df9-808d-2bcec7812427_1218x789.png)
*来源：SemiAnalysis*

为了实现多园区训练，Google 目前使用一个名为 MegaScaler 的强大切分器，能够借助 Pathways 的同步训练，将任务切分到园区内的多个 pod 和区域内的多个园区上。MegaScaler 让 Google 在扩大参与单一训练工作负载的芯片数量时，在稳定性和可靠性上获得了显著优势。

随着行业回归异步训练，这可能反而成为 Google 的软肋。MegaScaler 建立在同步式训练原则之上，即每个数据副本与所有其他数据副本通信交换数据。要为 MegaScaler 增加异步训练能力可能相当困难，或许需要进行大规模重构，甚至另起炉灶启动全新项目。虽然 Pathways 在设计之初就考虑了异步数据流，但在实践中，Pathways 目前所有生产用例都是完全同步的 SGD 式训练。话虽如此，Google 显然有能力重做这套软件栈。

![](https://substack-post-media.s3.amazonaws.com/public/images/69fa7969-529b-4c5a-b7d9-d45281986830_1977x668.png)
*来源：Google，Jeff Dean*

跨区域连接数据中心时存在两大主要限制：带宽和延迟。我们总体上认为，从长期看，限制因素将是玻璃（光纤）中光速带来的延迟，而非带宽。这是因为园区之间、区域之间敷设光缆的成本主要是许可和开挖的费用，而非光缆本身。因此，比如在凤凰城和达拉斯之间敷设 1,000 对光纤的成本只比 200 对略高。话虽如此，行业是在监管框架和时间尺度内运作的，光纤对不可能即刻铺就，因此降低带宽占用的策略仍然非常关键。

![](https://substack-post-media.s3.amazonaws.com/public/images/1a7d28d0-4912-48e8-b282-302a521062d5_908x600.png)
*来源：SemiAnalysis*

我们认为，在这个多园区、多区域训练集群上训练的模型将达到 100T（参数）以上的量级。对于区域内的各可用区（AZ），我们认为区域内各园区站点之间增长到约 5Pbit/s 是对它们近期可达规模的合理假设，而区域之间 1Pbit/s 是合理的带宽量。如果跨数据中心带宽真有那么高，在园区站点之间交换权重并不会成为训练的主要瓶颈，因为以线速传输只需 0.64 秒。交换 400TB 权重（4 字节 = 1 个参数）只需 0.64 秒，考虑到每若干个计算步骤所要花费的时间，这已经非常好了。

![](https://substack-post-media.s3.amazonaws.com/public/images/169a7cab-72e3-4b0c-ac3a-7a0a3df0821b_1738x315.png)
*来源：SemiAnalysis*

虽然 Nvidia 提供一款名为 MetroX 的 InfiniBand fabric 网络交换产品，支持 40km 以内的连接，但没有任何 AI 实验室在使用它，只有几个跨 10km 内多园区的非 AI HPC 集群在用。此外，其每台机箱只有 2×100Gbps，而 40km 以内城域以太网方案的生态已相当成熟。因此，即便是大量使用 InfiniBand 的 Microsoft，在数据中心之间也使用以太网。

# **从吉比特到太比特：调制与复用**

如今，数据中心内部网络（即数通，Datacom）的主要目标通常是通过光纤链路为每个终端设备（即每块 GPU）提供高达 400Gbps 的速率，而在 Nvidia 向 Connect-X8 网络接口卡（NIC）切换的推动下，AI 应用向 800Gbps 的过渡将于明年全面展开。

相比之下，电信网络会把一个设施内多台设备和服务器的通信需求聚合到数量更少但速率高得多的光纤上。数通收发器跑 800Gbps 时通常每对光纤只能用到最高 100Gbps（DR8），需要多对独立光纤；而电信应用在海底电缆以及许多陆地和城域部署中，已经在单单一对单模光纤上承载超过 20-40Tbps。

更大的带宽通过以下组合实现：

1. 更高阶的调制方案，在给定波长上每个符号传递更多比特。
2. 密集波分复用（DWDM），将多个光波长合并到单根光纤上。

在调制方面，数交通常使用基于 VCSEL 和 EML 的收发器，支持 PAM4 调制。这是一种强度调制方案（即强度调制直接探测——IMDD 光模块），通过四个不同的电平来传信，每个符号编码 2 比特数据。

![](https://substack-post-media.s3.amazonaws.com/public/images/50721bf9-b069-4527-9a0a-5134ee41da97_755x343.png)
*来源：ResearchGate*

提高速率的途径要么是提高符号发送速率（以 Gigabaud 或 Gbd 计量），要么是增加每符号的比特数。例如，一个 400G SR8 收发器可以以 26.6 Gbd 的速率发送符号，并采用 PAM4 实现每符号 2 比特，即每对光纤总共 50Gbps。把 8 对光纤合并到一个连接器中，整体即可达到 400Gbps。要达到整体 800Gbps，可以将符号速率提高到 53.1 Gbd，同时在 8 个通道上继续使用 PAM4。然而，符号速率翻倍往往比采用更高阶的调制方案更难。

16-正交幅度调制（16-QAM）就是这样一种方案，广泛应用于 ZR/ZR+ 光模块和电信领域。它不仅对信号波的四种不同幅度进行编码，还使用两路彼此相位相差 90 度的独立载波，每路载波各有四种不同幅度，总共可表示 16 种不同的符号，每符号传递 4 比特。再通过双极化（dual polarization）进一步扩展：利用另一组载波，一组处于水平极化状态、另一组处于垂直极化状态，可表示 256 种符号，实现每符号 8 比特。大多数 400ZR/ZR+ 和 800ZR/ZR+ 收发器最高只支持 DP-16QAM，而专用电信系统（外形尺寸更大）在优质光纤上可以支持到 DP-64QAM，达到每符号 12 比特。

![](https://substack-post-media.s3.amazonaws.com/public/images/4fdda494-c976-4401-b1a0-dfabede8a649_565x420.png)
*16-QAM 中 16 种可能的波形。来源：EverythingRF*

要实现利用不同相位的调制方案，就需要相干光模块（coherent optics，勿与 Coherent 公司混淆）。当光源发出的光波彼此同相时，光才被认为是相干的——这对实现基于相位的调制方案很重要，因为不一致（非相干）的光源会导致不一致的干涉，使相位调制信号无法恢复。

相干光模块需要使用能够处理高阶调制方案的相干数字信号处理器（DSP），以及可调谐激光器和调制器；不过在 400ZR 的场合，常常采用硅光子学来实现更低的成本。值得注意的是，可调谐激光器同样非常昂贵，因此业界也在尝试在 coherent-lite 方案中使用更便宜的 O 波段激光器。

ZR/ZR+ 光模块是一类日益流行的收发器，采用相干光学，专为数据中心互联设计，每对光纤可提供大得多的带宽，传输距离也远得多，可达 120km 至 500km。它们通常采用 OSFP 或 QSFP-DD 封装——与数通应用常用封装相同——意味着可以直接插在数通所用的同款网络交换机上。

![](https://substack-post-media.s3.amazonaws.com/public/images/753be8e4-f2c6-417d-bd9f-3764bffe058d_1873x613.png)
*来源：SemiAnalysis*

传统电信系统也可以用于数据中心互联，但相比 ZR/ZR+ 可插拔模块——后者可以直接插在两端的网络端口上、省去若干电信设备——这需要一条复杂得多的电信设备链，占用数据中心更多的物理空间。

![](https://substack-post-media.s3.amazonaws.com/public/images/2c0f4945-907e-43f1-9712-e365960daedc_975x552.png)
*来源：Cisco*

相比使用 PAM4 的强度调制直接探测（IMDD）收发器，更高阶的调制方案能在每对光纤上实现更大的带宽，DP-16QAM 的情况下是 8 倍。不过长距离传输仍受光纤限制，因此还可以用密集波分复用（DWDM）在每对光纤上实现更大带宽。DWDM 的原理是把多个光波长合并到一对光纤上。在下面的例子中，C 波段（1530nm 至 1565nm）的 76 个波长与 L 波段（1565nm 至 1625nm）的 76 个波长被复用到同一根光纤上。

![](https://substack-post-media.s3.amazonaws.com/public/images/b272f427-18db-42fc-b5b7-5c45491c407a_1284x602.png)
*来源：Ciena*

如果该系统能部署每波长 800Gbps，单对光纤的容量可达 121.6Tbps。海底电缆通常会最大化使用的波长数，而有些部署可能只使用不到 16 个波长，不过 96 个波长的部署也并非闻所未闻，目前典型部署的目标是每对光纤 20-60Tbps。

许多部署最初只点亮 C 波段上的少数几个波长，随客户需求增长逐步点亮更多 C 波段乃至最终 L 波段的波长，使现有光纤的速率得以随时间大幅升级。

# **超大规模云厂商的电信网络部署**

美国大多数城域区域仍有大量可供点亮利用的光纤，而 AI 数据中心互联所需的巨大带宽正是榨取这些容量潜力的完美方式。在海底电缆中，联盟往往只部署 8-12 对光纤，因为线缆本体和敷设成本随光纤对数增加而上升。在陆地光缆中，成本大头是开挖沟槽的人工和设备（在某些城区还有通行权费用），而非光纤本身，因此企业在城域开挖陆地路由时往往一次敷设数百对乃至上千对光纤。

跨海洋训练将比跨陆地训练困难得多。

一个典型的光纤商业案例可能会假设相当数量的光纤对闲置以备未来需求。而且不只是城域——通常任何主要公路、输电线路、铁路或其他基础设施旁边都会有光缆伴随——任何建设基础设施的一方都会倾向于顺手敷设光纤作为副业，因为既然开挖队本来就要到场，这带来的增量成本微乎其微。

就超大规模云厂商的电信网络而言，它们更倾向于自建网络，而不是与电信运营商合作：直接与设备厂商和建设公司对接，满足长途、城域和数据中心互联的需求。

![](https://substack-post-media.s3.amazonaws.com/public/images/cb41ed52-4033-4f7e-8da8-0b704fabc539_2662x1488.png)
*来源：Microsoft*

数据中心互联是指在点对点网络中连接两个相距约 50km 以内的数据中心，通常通过敷设数千对光纤来建设。超大规模云厂商可以在两个远端数据中心内的网络交换机上插入 ZR 收发器，要么把收发器调谐到不同的光波长，再用无源复用器（即 DWDM 链路）把最多 64 个收发器合并到单对光纤上——若使用 400ZR，每对光纤最高可达 25.5Tbps——要么干脆让每个 ZR 收发器独占一对光纤。

![](https://substack-post-media.s3.amazonaws.com/public/images/fccf502f-d4c1-4d0a-bad5-2322c0cea783_2862x772.png)
*来源：Arista*

更复杂、同样实现 DWDM 的电信系统可以将更多 ZR 光信号复用到更少的光纤对上，并支持不止点对点的网络，但这需要在数据中心里腾出几机柜的空间放置路由器、ROADM 以及 DWDM 所需的复用器/解复用器等电信设备。

由于成本大头在于为光纤开挖沟槽，大多数超大规模云厂商觉得多铺远超需求的光纤对更省事，既节省数据大厅内的空间，又避免了更复杂的电信部署。通常只有在光纤物理容量获取受限的地点部署时，它们才会为了短距离而部署复杂的电信系统——美国以外可能存在这种情况，超大规模云厂商在光纤稀缺的城域可能被迫只能用区区 2-4 对光纤。

![](https://substack-post-media.s3.amazonaws.com/public/images/f81d8853-1c3b-4d4d-8938-d00b275d7bf5_2246x1422.png)
*来源：Anritsu*

但对于长途网络，超大规模云厂商就需要动用一整套与数通产品截然不同的电信产品。一个典型的长途网络至少需要几个基本系统：转发器（Transponder）、DWDM 复用器/解复用器、路由器、光放大器、增益均衡器和再生站点，以及在多数（但并非全部）情况下需要的 ROADM（可重构光分插复用器）和 WSS（波长选择开关）。

![](https://substack-post-media.s3.amazonaws.com/public/images/3843d27b-ad3f-4552-bd1c-c0bce3b8b2b6_2444x1390.png)
*来源：TelecomHall*

转发器在电信领域实现与收发器类似的功能，但价格昂贵得多，工作功率也更高。它的一侧向真正的电信网络收发信号（线路侧），另一侧则提供多种可能的端口组合，连接本地局站内的客户端设备（客户端）。例如，一台转发器线路侧可提供 800Gbps，客户端提供 4 个 200Gbps 的光口或电口，而客户可选的端口容量与光/电组合不胜枚举。客户端可以连接数据中心内部的路由器或交换机，线路侧则连接复用器，用 DWDM 把多台转发器的信号合并，并可能经由 ROADM 为比简单点对点更复杂的网络拓扑提供光交换。

![](https://substack-post-media.s3.amazonaws.com/public/images/250327c0-0f20-474c-97a2-4c9ea008b247_1258x1070.png)
*一台典型的转发器。来源：Ciena*

DWDM 依靠复用器和解复用器（mux/demux）工作：从每台转发器收取波长略有不同的光信号，合并到一对光纤上。每台转发器都是可调谐的，可以精确设定特定波长以便复用到同一对光纤上。使用 ROADM 时，转发器通常连接「无色」（colorless）mux/demux，再接到波长选择开关（WSS），使 ROADM 能够动态地把转发器调谐到特定波长，以优化各种网络目标。

光放大器用于对抗光信号在光纤上长距离传输的衰减。放大器沿光纤路由每隔 60-100km 设置一处，可以直接放大光信号而无需将其转换为电信号。每三个放大器之后需要一台增益均衡器，确保以不同速度传播的不同波长光信号得到均衡，避免出错。在数千公里的超长途部署中，还需要再生（regeneration）：把光信号转入电域，对信号进行整形和重定时，再用另一组转发器重新发送。

如果网络连接的不止两个点，并且有多个站点需要上、下流量，就需要 ROADM（可重构光分插复用器）。这种设备可以在网络的给定位置以光学方式上/下特定波长的光，而无需把任何信号下电做处理或路由。某个位置要发送或接收的波长可以从主光纤网络中加上或落下，而不承载该位置流量的其他波长则可以畅通无阻地穿过 ROADM。ROADM 还带有控制平面，可以主动发现和监测网络状态，了解光纤网络上哪些信道空闲、各信道的信噪比、已被保留的波长，并且如上所述可以控制转发器，把线路侧调谐到合适波长。

![](https://substack-post-media.s3.amazonaws.com/public/images/0ba5d73f-1325-4830-9ca1-107025dfbbdf_1562x820.png)
*来源：Ciena*

这些不同的组件通常组合在一个模块化机箱里，大致长这样：

![](https://substack-post-media.s3.amazonaws.com/public/images/5e27f1c8-18d6-499d-8777-b1a7bb56b992_1281x800.jpeg)
*来源：Optical Connection News*

Ciena、Nokia、Infinera 和 Cisco 是全球电信系统与设备的几家主要供应商，而 Lumentum、Coherent、Fabrinet 和 Marvell 则向这些大供应商提供各类子系统与有源器件。迄今为止，器件厂商的强势主要体现在数据中心互联的 ZR/ZR+ 光模块上，但随着超大规模云厂商和其他运营方不得不认真对待跨非相邻数据中心的训练，它们可能会大幅增加对单价高得多的电信设备与系统的支出。

来自非云客户的电信设备需求似乎也已触底，可能很快进入周期的复苏阶段——这将提振各家电信供应商的境况。

接下来，让我们讨论 OpenAI 和 Microsoft 雄心勃勃的多数据中心训练计划，以及这场大规模建设中电信领域的赢家。

# **OpenAI 与 Microsoft 计划如何击败 Google**
