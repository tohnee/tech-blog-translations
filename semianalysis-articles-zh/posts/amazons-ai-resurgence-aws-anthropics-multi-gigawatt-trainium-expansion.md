---
title: "亚马逊的 AI 复兴：AWS 与 Anthropic 的多吉瓦级 Trainium 扩张"
title_en: "Amazon’s AI Resurgence: AWS & Anthropic's Multi-Gigawatt Trainium Expansion"
subtitle: "Anthropic 的多吉瓦级集群、Trainium 产能爬坡、单位内存带宽 TCO 最优、系统级路线图、Bedrock 与内部模型"
date: 2025-09-03
source: https://newsletter.semianalysis.com/p/amazons-ai-resurgence-aws-anthropics-multi-gigawatt-trainium-expansion
crawled: 2026-09-15
authors: ["Jeremie Eliahou Ontiveros", "Dylan Patel", "AJ", "Myron Xie"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 亚马逊的 AI 复兴：AWS 与 Anthropic 的多吉瓦级 Trainium 扩张

> 原文：[Amazon’s AI Resurgence: AWS & Anthropic's Multi-Gigawatt Trainium Expansion](https://newsletter.semianalysis.com/p/amazons-ai-resurgence-aws-anthropics-multi-gigawatt-trainium-expansion) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**Anthropic 的多吉瓦级集群、Trainium 产能爬坡、单位内存带宽 TCO 最优、系统级路线图、Bedrock 与内部模型**

两年半前，我们曾预警 AWS 一场迫近的[「云危机」](https://semianalysis.com/2023/03/20/amazons-cloud-crisis-how-aws-will/)。如今，证据已越积越多。AWS 是亚马逊帝国的掌上明珠，贡献了集团约 60% 的利润，并主导着利润丰厚的云计算市场。但它一直难以把这一优势延续到新的 GPU/XPU 云时代。

在季度新增云营收上，Microsoft Azure 如今领跑市场，而 Google Cloud 与 AWS 之间的差距也已显著收窄——尤其是随着 [Google 在 TPU 上的一系列大动作，我们已就此连续发帖讨论一个多月](https://semianalysis.com/accelerator-model/)。市场已经注意到了这一点。年初至今，亚马逊是四大科技与 AI 巨头中明显的掉队者，投资者因其在 AI 上失去势头而给这家公司的折价也最狠。

![](https://substack-post-media.s3.amazonaws.com/public/images/6227dc41-f0ed-4125-87c2-b52961d1b42c_1024x606.png)
*来源：SemiAnalysis Core Research、公司公告*

今天，SemiAnalysis 再度给出一个与市场共识相左的判断。当市场还在过度渲染「云危机」叙事时，我们提出的却是 AWS 的 AI 复兴。一个月前，我们已向 [Core Research 订阅用户](https://semianalysis.com/core-research/)完整阐述了这一论点，预测其增速即将加速，到 2025 年底突破 20% 的同比增长。

![](https://substack-post-media.s3.amazonaws.com/public/images/414c071a-3f68-4268-8f7c-94ba79182635_1024x509.png)
*来源：SemiAnalysis Core Research*

亚马逊的救星有名有姓：Anthropic。这家初创公司是 2025 年 GenAI 市场上公认的领跑者，年初至今营收增长至五倍，年化已达 $5B。

![](https://substack-post-media.s3.amazonaws.com/public/images/01c05a64-a990-4506-9f1d-d0690410b13a_1024x547.png)
*来源：The Information、路透社、彭博社、SemiAnalysis Core Research*

要维持这一轨迹，Anthropic 正在 [Scaling Laws](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/) 上豪掷重注。尽管 Dario 的这家公司在曝光度上不及 OpenAI、xAI 和 [Meta Superintelligence](https://semianalysis.com/2025/07/11/meta-superintelligence-leadership-compute-talent-and-data/)，它在投资上却毫不手软。AWS 正为其锚定客户建设**远超 1GW、已进入收尾阶段的数据中心产能**。AWS 当前的数据中心建设速度超过其整个历史上的任何时期。而且**后续还有远不止这些**。

![](https://substack-post-media.s3.amazonaws.com/public/images/348cc316-30b7-41e3-a083-911df1ae1a33_1024x576.png)
*来源：SemiAnalysis Datacenter Industry Model*

要理解并预测各 AI 实验室按云厂商拆分的 GPU/XPU 算力电力容量，我们依赖自研的 [Datacenter Industry Model](https://www.semianalysis.com/p/datacenter-model)，其底层是实时卫星影像。该模型受到所有超大规模云厂商、AI 实验室和全球最大投资者群体的信赖，*可为 OpenAI、Anthropic、xAI、Meta Superintelligence、Google DeepMind 等提供**逐栋楼宇的季度数据中心预测**。[联系我们获取更多信息](Sales@SemiAnalysis.com)。*

## Trainium 对决 GPU

亚马逊的 AI 数据中心在规模和速度上令人印象深刻，但单栋建筑的设计并不出奇。这套[为风冷高度优化](https://semianalysis.com/2025/02/13/datacenter-anatomy-part-2-cooling-systems/#google-datacenters-%e2%80%93-energy-for-water-tradeoff)的蓝图，与 5 年前传统的 AWS 云数据中心如出一辙。

这些设施的独特之处在于内部：它们将容纳**全球最大的非 NVIDIA AI 芯片集群，最大园区的 Trainium2 数量接近 100 万颗**。要全面了解 Trainium2 系统，请阅读[我们 2024 年 12 月的技术深度解析](https://semianalysis.com/2024/12/03/amazons-ai-self-sufficiency-trainium2-architecture-networking/)。

Trainium2 在很多方面落后于 NVIDIA 的系统，但它对[多吉瓦级的 AWS/Anthropic 交易](https://www.semianalysis.com/p/datacenter-model)至关重要。其在单位 TCO 内存带宽上的优势，与 Anthropic [激进的强化学习路线图](https://semianalysis.com/2025/06/08/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data/)完美契合。Dario Amodei 的这家公司深度参与了设计过程，而它对 Trainium 路线图的影响只会从这里开始与日俱增。

说白了：Trainium2 正在向一个**Anthropic 定制芯片项目**收敛。这将使 Anthropic 与 Google DeepMind 并列，成为近期内仅有的能享受**紧密软硬件协同设计**红利的 AI 实验室。

![](https://substack-post-media.s3.amazonaws.com/public/images/377f07d4-2e4e-4833-afc7-dd75f876c777_1024x357.png)
*来源：AI Cloud TCO Model*

本报告将深入剖析亚马逊 AI 复兴的方方面面：Anthropic 合作伙伴关系、数据中心以及 Trainium。在报告末尾，我们会对 Anthropic、AWS Bedrock 与内部模型给出更长期的展望，并解释为什么并非一切都一片光明。

首先，回过头来看为什么 AWS 迄今表现不及竞争对手们的 AI 云。

## AWS 的 GenAI 表现不佳

要理解亚马逊在 GenAI 时代表现不佳的原因，我们可以拆解 GPU/XPU 云市场的成功要素。最简化地看，GPU/XPU 产能有两大主要客户群体：

- 批发裸金属用户：OpenAI、Anthropic、字节跳动（ByteDance）等大规模客户，以及其他超大规模厂商。
- 托管 SLURM/Kubernetes 用户：初创公司、研究机构和企业试点项目等较小客户。

### 云危机与 ClusterMAX 评级中的落后表现

在第二类市场中，我们的 [ClusterMax AI 云评级](https://semianalysis.com/2025/03/26/the-gpu-cloud-clustermax-rating-system-how-to-rent-gpus/)是比较各家相对优劣的最佳工具。白金级和金牌级 AI 云获得了比其他厂商更多的增长动能，并拥有高于行业平均的定价能力。因此，CoreWeave、Oracle、Nebius、Crusoe 和 Azure 等厂商在多租户 GPU 集群市场（这类集群对高性能和先进软件层有较高要求）跑赢了大盘。

![](https://substack-post-media.s3.amazonaws.com/public/images/dbf0fa08-c2d5-42ef-a937-665ed42e6ce3_1024x615.png)
*来源：SemiAnalysis ClusterMAX GPU 云评级*

[正如我们两年前所预言](https://semianalysis.com/2023/03/20/amazons-cloud-crisis-how-aws-will/)，亚马逊表现不佳的关键在于使用了自研网络架构 EFA。AWS 在前端网络上 ENA 的成功，尚未复制到后端的 EFA 上。EFA 在性能上仍落后于其他网络方案：NVIDIA 的 InfiniBand 与 Spectrum-X，以及 Cisco、Arista、Juniper 的 RoCEv2 方案。原始性能并非唯一指标，EFA 的用户体验同样不如 InfiniBand 和 RoCEv2。话虽如此，随着 Amazon 最新的 EFAv4 推出，其在真实报文尺寸下的性能正在改善——尽管仍落后于竞争对手。

亚马逊的自研网络还[因 NVIDIA 系统的定制化需求而拖累了上市时间](https://x.com/SemiAnalysis_/status/1959758467402784855)。其他方面，如先进的有源/无源自动化每周例行健康检查策略，也不如金牌与白金级云那样扎实。

我们即将推出的 ClusterMAXv2 评级将基于自研测试，对各大云厂商给出最新评价。敬请期待！

### 寻找锚定客户

对 AWS 的 XPU 业务增长而言，更重要的是**锁定锚定客户的能力——它们是 GenAI 第一波需求中的做市者**。规模、上市速度、深度合作关系和价格，是赢得这些大客户的关键，其重要性甚至超过先进的软件层。

没有哪家公司比 Microsoft 更能说明这一点。Azure 在 AI 上跑赢同业，完全由其与 OpenAI 的合作关系驱动。截至 2025 年 Q2（2025 年 6 月），OpenAI 超过 $10B 的云支出全部记在 Azure 账上。

![](https://substack-post-media.s3.amazonaws.com/public/images/7cf42542-67fc-456a-bc11-41ca08f65139_1024x508.png)
*来源：SemiAnalysis Datacenter Industry Model*

Amazon 早已理解锚定客户的必要性，并于 2023 年 9 月[向 Anthropic 投资了 $1.25B（可增至 $4B）](https://semianalysis.com/2023/10/02/amazon-anthropic-poison-pill-or-empire/)。2024 年 3 月，合作进一步扩大，[Anthropic 承诺使用 Trainium 和 Inferentia 芯片](https://www.aboutamazon.com/news/company-news/amazon-anthropic-ai-investment)。2024 年 11 月，[Amazon 再向 Anthropic 追加投资 $4B](https://www.aboutamazon.com/news/aws/amazon-invests-additional-4-billion-anthropic-ai)，[后者则指定 AWS 为其主力 LLM 训练合作伙伴](https://www.aboutamazon.com/news/aws/amazon-invests-additional-4-billion-anthropic-ai)。

### Anthropic 一枝独秀，AWS 却表现平平？

Amazon 这一把押对了。Anthropic 是 2025 年 GenAI 市场公认的领跑者，年化营收从 $1B 暴涨至 $5B。在这样的背景下，AWS 的平淡表现令投资者沮丧可以理解，但他们误解了 Anthropic 在训练与推理上的支出构成。

![](https://substack-post-media.s3.amazonaws.com/public/images/b77d4f69-7460-45f7-9709-b281de0a926c_1024x547.png)
*来源：SemiAnalysis Tokenomics*

有**两个明确的原因**可以解释为什么 Amazon 尚未真正从其与 Anthropic 的关系中获益：

1. 截至 2025 年 Q2，Anthropic 的云支出规模不足 OpenAI 的一半。
2. Anthropic 的支出中有很大一部分流向了 Google Cloud——后者是 Anthropic 最早的主要投资者之一（2022 年底的 $300M 轮融资），并且在扩大后的 AWS 交易之前，一直是 Anthropic 在 2023 和 2024 年的首选云合作伙伴。

![](https://substack-post-media.s3.amazonaws.com/public/images/315d7305-7da2-407b-a362-97b5a08962d3_1024x507.png)
*来源：SemiAnalysis Datacenter Industry Model*

## Anthropic 与 AWS 的多吉瓦级 AI 训练基础设施

具体而言，我们认为 Anthropic 暴涨的推理需求大部分由 Google Cloud 承接。拥有全球最好的推理系统（TPU）是一项关键竞争优势。

AWS 的大规模基础设施建设，旨在为这一关键客户分走一块蛋糕，同时聚焦于**训练**。虽然 Anthropic 的头条曝光不及 OpenAI、xAI 和 Meta 等同行，但它已全力投入 AGI 竞赛，并不打算在训练开支上缩手缩脚。Anthropic 管理层真心信奉[面向 RL 的扩展](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/)。

他们的信念最早今年就会落地。下图展示了三个进入收尾建设阶段的 AWS 园区，拥有超过 1.3GW 的 IT 容量，**专门用于满足 Anthropic 的训练需求**。建设速度令人惊叹。

![](https://substack-post-media.s3.amazonaws.com/public/images/eed0550a-e73f-4693-991e-fc95b5f6fc7a_1024x576.png)
*来源：SemiAnalysis Datacenter Industry Model*

虽然这些数据中心从空中俯瞰已然成型，但我们认为它们尚未产生有意义的营收。Trainium 在组装环节遇到了一些良率问题——对一个全新系统而言这相当正常。我们认为到 2025 年底，这三个大型 AWS 园区将为 AWS 的营收做出实质性贡献，并把增速拉升至 20% 的同比门槛之上。

![](https://substack-post-media.s3.amazonaws.com/public/images/2757411e-3e3d-465b-aa82-b637633ee401_1024x509.png)
*来源：SemiAnalysis Core Research——Core Research 是我们的机构研究服务，受到全球多数最大对冲基金与投资者的信赖。联系我们，获取业内关于 AI 硬件、软件与基础设施最细颗粒度的洞察。*

Anthropic 不会止步于此。其估值 $183B 的约 $13B 融资轮，将为其提供与 AWS、Google 及其他方签署更多交易的弹药。AWS 也没有原地等待——他们已开始为接下来的 GW 级数据中心破土动工，以承接这波增长。

![](https://substack-post-media.s3.amazonaws.com/public/images/58e99612-92fc-46a8-a6c1-1b97237f9b05_1024x553.png)
*来源：SemiAnalysis Datacenter Industry Model*

如前所述，这些数据中心将主要装满 AWS 的自研芯片 [Trainium](https://semianalysis.com/2024/12/03/amazons-ai-self-sufficiency-trainium2-architecture-networking/)。考虑到如此庞大的规模，Anthropic 这一赌注有多大胆**怎么强调都不为过**。他们不仅承诺投入数百亿美元，而且押的是一款基本未经市场验证的芯片！

下面我们通过深入拆解 Trainium 的 TCO 与路线图，来理解这笔豪赌的逻辑。

## Trainium2 TCO 分析——Anthropic 的豪赌何以可能奏效

当前 Trainium2 的供应链信号极其强劲。我们业内领先的 [AI Accelerator Model](https://semianalysis.com/accelerator-industry-model/) 同时追踪封装出货与系统/机柜出货，两项自年初以来均大幅飙升。该模型*为构成 Trainium2 与 Trainium3 产品族的 10 多个 SKU 提供季度出货量预测，并点名有望从特定 SKU 中超额受益的供应商。[联系我们获取更多信息](Sales@SemiAnalysis.com)。*

![](https://substack-post-media.s3.amazonaws.com/public/images/d5e4a6cb-ee16-49ea-ad64-5288333af03c_1024x552.png)
*来源：SemiAnalysis Accelerator and HBM Model*

注意这是芯片产量，机柜产量存在滞后，但我们同样在追踪。

当然，与 NVIDIA 和 Google 的 TPU 竞争绝非易事。当 Google 正在推出其第七代 TPU Ironwood 时，Trainium2 只是 Amazon 的第三代 AI 加速器。

### 芯片规格：Trainium2 全面落后，但是……

简单看一下芯片规格，就会发现 Trainium 相对 NVIDIA 明显落后：

- NVIDIA 的 GB200 在 FP16 算力上有 **3.85 倍优势**，为 2500 TFLOP/s/颗，而 Trainium2 为 667 TFLOP/s/颗。注意规格书数字相对实际可达 FLOPs 存在虚高。
- 在**内存带宽**方面，差距缩小到 2.75 倍：8000GB/s/GPU 对 2900GB/s/Trn2。

![](https://substack-post-media.s3.amazonaws.com/public/images/ebe72b52-b6a4-4b23-8c3b-a85a6399d12d_1024x553.png)
*来源：Amazon、SemiAnalysis*

评估纵向扩展网络带宽是另一个关键项。我们已多次解释[纵向扩展网络对推理模型推理的重要性](https://semianalysis.com/2024/12/25/nvidias-christmas-present-gb300-b300-reasoning-inference-amazon-memory-supply-chain/#built-for-reasoning-model-inference)。我们的[强化学习深度解析](https://semianalysis.com/2025/06/08/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data/)强调了 RL 与推理工作负载的相似性，这使得内存带宽成为扩展后训练（post-training）的关键要素。

- NVIDIA 的 GB200 NVL72 在整个 World Size 范围内拥有 576TB/s 的聚合内存带宽。
- 相对 Trainium2（Teton2-PD-Ultra-3L SKU）的 186 TB/s，这是 **3.1 倍的优势**——需要注意的是，该数值因 SKU 而异。

虽然 Trainium 看起来明显落后，但一旦把总拥有成本（TCO）纳入考量，局面就完全不同了。

### Trainium 在单位 TCO 内存带宽上的优势

在下表中，我们将 TCO 纳入对比。虽然 NVIDIA 在单位有效训练 PFLOP 的 TCO 上有明显领先，但 Trainium2 在每百万 token 的 TCO 和每 TB/s 内存带宽的 TCO 上极具竞争力。

![](https://substack-post-media.s3.amazonaws.com/public/images/3fa83400-60da-4742-8b8b-131e439ac2b7_1024x357.png)
*来源：AI Cloud TCO Model*

而且我们不认为 NVIDIA 即将推出的 VR200 NVL144 相对 AWS 的 Trainium3 能改变这一格局。需要说明的是，TCO 还有很多其他变量。AWS 还有其他更适合某些用例的系统级架构部署。再往后，[NVIDIA 的 Kyber 机柜将拥有全球最先进的纵向扩展网络架构](https://semianalysis.com/2025/03/19/nvidia-gtc-2025-built-for-reasoning-vera-rubin-kyber-cpo-dynamo-inference-jensen-math-feynman/#kyber-rack-architecture)。

要完整理解 50 多个 NVIDIA SKU 的 TCO，以及与所有 AMD、Trainium 和 TPU SKU 的详细 TCO 对比，请[查看我们的 AI Cloud TCO Model](https://semianalysis.com/ai-cloud-tco-model/)。最大的超大规模云厂商、新兴 GPU 云（neocloud）及其财务投资方都依赖我们的模型来把握投资决策时点。

### Anthropic 押注软硬件协同设计

Trainium2 单位 TCO 内存带宽的优势，是理解 Anthropic 这一选择的关键。虽然 NVIDIA 的芯片和系统在大多数方面更优，但 Trainium2 与 Anthropic 的路线图完美契合。他们是在[扩展强化学习等后训练技术](https://semianalysis.com/2025/06/08/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data/)上最激进的 AI 实验室。他们的路线图受内存带宽的制约大于受 FLOPs 的制约。我们近期的 HBM 报告深入解释了哪些 AI 工作负载倾向于内存受限。

Anthropic 的上量（ramp）不仅使其成为 Trainium2 唯一的大型外部最终用户，其规模还将显著超过 Amazon 的内部需求（如 Bedrock、Alexa 等）。他们如今深度参与 Trainium 的所有设计决策，实质上等于把 Amazon 的 Annapurna Labs 当作自己的定制芯片合作伙伴！**这使 Anthropic 成为除 Google DeepMind 之外，唯一能享受紧密软硬件协同设计红利的 AI 实验室**。

### Trainium 路线图：加倍押注系统级创新

Amazon 正在为其锚定客户推出一套新的系统级架构。目前 AWS 已部署的两个系统是 Teton PD 和 Teton PD Ultra。明年，新的 Teton PDS 和 Teton Max 将大批量出货。[我们的 AI Accelerator Model 按季度提供精确出货量与逐 SKU 拆解](https://semianalysis.com/accelerator-industry-model/)。

![](https://substack-post-media.s3.amazonaws.com/public/images/4bfcf56c-0eb5-4cdc-9c3c-593978efdf66_1024x517.png)
*来源：SemiAnalysis Accelerator Industry Model、AWS*

关键差异**在于引入了名为 NeuronLinkv3 的全对全（all-to-all）纵向扩展网络**。Trainium 的架构由此向 NVIDIA 的 NVL72 NVLink 收敛。

**四个 NeuronLinkv3 交换托盘**将置于机柜中部，上下各均匀分布 8 个计算托盘（合计 16 个）。[正如我们两个月前在 Core Research 上强调的，某些供应链厂商将获得超额受益](https://semianalysis.com/core-research/)——Core Research 是我们的机构研究服务，受全球最大对冲基金信赖。自我们发文以来，那家厂商的股价已上涨 73%。我们将 PDS 的引入视为 Trainium 追赶 NVIDIA 进程中的过渡一步。我们还认为，Anthropic 深度参与了这套新系统级架构的推出。

![](https://substack-post-media.s3.amazonaws.com/public/images/af62f51b-0cdc-4e58-80e0-ea8828c9d9ba_1024x292.png)
*来源：SemiAnalysis Accelerator Industry Model、AWS*

Anthropic 在设计决策中介入的加深，对未来出货量是好兆头。但他们也没有放弃 TPU 和 NVIDIA GPU。我们的 [Accelerator Model](https://semianalysis.com/accelerator-industry-model/) 按精确 SKU 预测 Amazon 与 Google Cloud 的芯片采购，我们的 [Datacenter model](https://www.semianalysis.com/p/datacenter-model) 则用于理解哪些数据中心与云合作伙伴支撑 Anthropic 的上量。[Anthropic 2026 年的 TPU 上量规模巨大，其交易还有诸多独特之处——对此我们已连续发帖讨论一个多月。](https://semianalysis.com/core-research/google-selling-tpu-systems-externally-further-tpu-revisions/)

现在让我们把视角拉长，评估 AWS 的未来可能是什么样子。付费墙之后，我们讨论以下内容：

- Amazon 关键客户 Anthropic 的前景。
- Anthropic 之外 Amazon 的 GenAI 业务：Bedrock 与内部 LLM 投入。
- Trainium 在 2026 与 2027 年的上量、潜在新外部客户，以及它可能如何影响 Amazon 未来数年的财务面貌。
