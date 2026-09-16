---
title: "微软 AI 战略解构——从能源到 token"
title_en: "Microsoft's AI Strategy Deconstructed - From Energy to Tokens"
subtitle: "「大暂停」、AI Token 工厂经济栈、OpenAI、新兴 GPU 云租赁、GitHub Copilot、MAI 与 Maia"
date: 2025-11-12
source: https://newsletter.semianalysis.com/p/microsofts-ai-strategy-deconstructed
crawled: 2026-09-15
authors: ["Jeremie Eliahou Ontiveros", "Dylan Patel", "Myron Xie", "Wei Zhou", "Jordan Nanos", "Clara Ee", "Daniel Nishball", "AJ"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 微软 AI 战略解构——从能源到 token

> 原文：[Microsoft's AI Strategy Deconstructed - From Energy to Tokens](https://newsletter.semianalysis.com/p/microsofts-ai-strategy-deconstructed) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**「大暂停」、AI Token 工厂经济栈、OpenAI、新兴 GPU 云租赁、GitHub Copilot、MAI 与 Maia**

2023 年和 2024 年，微软还站在 AI 之巅，但一年前它急剧转向：大幅暂停了数据中心建设，并放缓了对 OpenAI 的投入承诺。一年前我们就向[数据中心模型订阅客户](https://www.semianalysis.com/p/datacenter-model)指出了这一点，[后来又就此撰写了一篇 newsletter 文章](https://newsletter.semianalysis.com/p/microsofts-datacenter-freeze)。

2025 年的主旋律，则是 OpenAI 去微软化：Oracle、CoreWeave、Nscale、SB Energy、亚马逊（Amazon）和 Google 都与 OpenAI 直接签署了大型算力合同。

这看起来处境相当糟糕。今天的文章将剖析微软的失误，同时我们还发布了[与萨提亚·纳德拉（Satya Nadella）以及我们的老朋友 Dwarkesh Patel 的公开访谈——我们在访谈中就微软的 AI 战略与执行向他发起了挑战](https://www.youtube.com/watch?v=8-boBsWcr5A)。

如今，微软对 AI 的投资已全面回归，这家 AI 巨头对加速计算（Accelerated Computing）的需求从未如此旺盛。这位雷德蒙德巨人已经意识到自己走错了路，并大幅调整了航向。随着[新宣布的 OpenAI 合作协议](https://blogs.microsoft.com/blog/2025/10/28/the-next-chapter-of-the-microsoft-openai-partnership/)落地，我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)预测，Azure 的增长将在未来几个季度***加速***。

![](https://substack-post-media.s3.amazonaws.com/public/images/4464a250-8f21-4301-8e53-6c513ca11832_3303x1653.png)
*来源：SemiAnalysis Tokenomics 模型*

微软在 [AI Token 经济栈](https://semianalysis.com/tokenomics-model/)的每一个环节都有布局，目前正见证加速增长，我们预计这一趋势将在未来几个季度乃至数年内延续。

![](https://substack-post-media.s3.amazonaws.com/public/images/4a042c69-b68a-4a53-84ad-3288494b8e97_3303x1653.png)
*来源：SemiAnalysis Tokenomics 模型*

这家公司正在积极寻找近期产能，凡是可以到手的资源都会果断出手。自建、租赁、新兴 GPU 云（Neocloud）、偏远地区选址——为了加速近期产能增长，所有选项都摆上了桌面（确切数字见我们的[数据中心模型](https://semianalysis.com/datacenter-industry-model/)订阅内容）。

![](https://substack-post-media.s3.amazonaws.com/public/images/37552a43-3de2-4366-a858-f6295e47ce8b_2861x1523.png)
*来源：SemiAnalysis Tokenomics 模型*

在硬件层面，微软甚至可以使用 **OpenAI 的自研芯片 IP**——当前在研的最令人兴奋的自研芯片 ASIC。鉴于 OpenAI ASIC 的发展轨迹远好于微软的 Maia，微软最终很可能会用这款芯片来服务 OpenAI 模型。这种态势与微软在 OpenAI 模型上的处境如出一辙：虽然能用上 OpenAI 的模型，但微软仍在通过 Microsoft AI 训练自己的基础模型。我们认为，微软正试图成为一家真正垂直整合的 AI 巨头，剔除第三方毛利率栈中的大部分环节，以比同行更低的成本交付更多的智能。

在这篇报告中，我们将深入剖析微软 AI 业务的方方面面。我们首先回顾微软与 OpenAI 合作关系的历史，涵盖 2023-24 年微软数据中心投资的历史性激增，以及其 OpenAI 训练集群指数级膨胀的规模——从数十 MW 到吉瓦级。随后我们分析「大暂停」以及它高调重返数据中心市场的过程。这背后很大一部分动因，是 OpenAI 股权结构的大幅简化，以及微软对一件事的聚焦：为「把模型能力通过无状态 API 转化为产品用例（和收入）」提供所需的基础设施。

![](https://substack-post-media.s3.amazonaws.com/public/images/e7ca381d-c56a-4e65-86d6-7633a9d264fa_1103x690.png)
*来源：SemiAnalysis Tokenomics 模型、公司披露信息*
![](https://substack-post-media.s3.amazonaws.com/public/images/169f1412-d509-4016-bf33-162854ea6c9c_916x608.png)
*来源：SemiAnalysis Tokenomics 模型、公司披露信息*

然后，我们逐一分析微软在 AI Token 经济栈中的定位：

- 应用
- 大模型（LLM）
- PaaS
- IaaS
- 芯片
- 系统架构

![](https://substack-post-media.s3.amazonaws.com/public/images/b5e04730-6db0-4ac5-b1c1-88fe9fe2a9a2_1587x1145.png)
*来源：SemiAnalysis*

在每一节中，我们都会深入探讨微软的产品组合、竞争定位与前景。对微软来说并非全是好消息：这家软件巨头的主导性生产力套件和 AI 算力平台正面临一大批新进入者和挑战者。

# 2023-25 年的微软与 OpenAI：从 All-In AI 到「大暂停」

## 2023-24 年：自建、租赁，以及为 OpenAI 建造全球最大的数据中心

2022 年 11 月 ChatGPT 的发布改变了世界。微软是第一个对「ChatGPT 时刻」作出反应的超大规模云厂商，而且反应极为壮观。虽然微软早在 2019 年就向 OpenAI 投资了 $1B，但在 2023 年 1 月将这笔投资扩大了 10 倍。与此同时，微软启动了史上最激进的数据中心建设——主要受其核心 AI 合作伙伴驱动。

下图展示了数据中心预租赁（pre-leasing）活动——这是产能增长与资本开支（CapEx）最佳领先指标之一。从 2023 年一季度到 2024 年二季度，微软的预租赁规模令其他超大规模云厂商*加总*也相形见绌。仅 2023 年三季度，微软一家的租赁量就几乎相当于*2022 年全年整个北美市场的租赁总量*。

![](https://substack-post-media.s3.amazonaws.com/public/images/c0ec63c0-7eca-4789-b2d4-66c763b9d1ce_3318x1773.png)
*来源：SemiAnalysis 数据中心模型*

而数据中心租赁只是图景的一部分。我们的[逐栋楼宇数据中心行业模型](https://semianalysis.com/datacenter-industry-model/)显示，2024 和 2025 年间微软自建产能新增的 MW 数实现了前所未有的增长。此外，微软还[向 CoreWeave 和 Oracle 签约了数十亿美元](https://semianalysis.com/tokenomics-model/)的额外产能。

### 微软与 OpenAI 的训练集群——从一栋楼的一部分到全球最大的设施

这一轮建设最具标志性的符号，或许当属「Fairwater」项目。2023-24 年，微软规划并同步建设了**全球最大的两座数据中心**。让我们短暂回溯一下，感受微软 2023-24 年建设的规模。下方展示的是其首个大型训练集群，位于艾奥瓦州，GPT-3.5 就是在这里训练的。我们估计该集群部署了约 25k 颗 A100 芯片。虽然下图的园区面积已相当可观，但我们认为 OpenAI 当时只使用了其中一栋 Ballard 大楼的两间数据大厅，即约 19MW。

![](https://substack-post-media.s3.amazonaws.com/public/images/67a81e93-c25b-4be9-a3ef-9ef06dd54d64_1632x946.png)
*来源：SemiAnalysis 数据中心模型*

第二个大型集群建在亚利桑那州。它随时间推移逐栋扩展：第一栋 H100 大楼于 2023 年建成，2024 年在另一栋设施中部署了 H200，2025 年又有两座数据中心部署 GB200。总计我们估计四栋楼共约 130k 块 GPU。

![](https://substack-post-media.s3.amazonaws.com/public/images/2f261c59-cf3c-4cf5-87fa-0d5f07244cba_1118x1040.png)
*来源：SemiAnalysis 数据中心模型*

微软为 OpenAI 建造的下一代集群名为 Fairwater，规模大得多。每座「Fairwater」由两栋建筑组成——一栋 48MW 的标准 CPU 与存储设施，以及一栋超密度的 GPU 大楼。后者为两层结构、总面积约 800k 平方英尺，功率高达约 300MW，相当于 20 万+ 美国家庭的用电量，对应每栋楼超过 150k 颗 GB200 GPU。下方是威斯康星州的设施——完全专用于 OpenAI。

![](https://substack-post-media.s3.amazonaws.com/public/images/8adae9d5-740e-4c32-beb8-8c57d7d06054_1525x1009.png)
*来源：SemiAnalysis 数据中心模型*

在佐治亚州，QTS 为微软建造了一座「姊妹」设施，同样服务于 OpenAI。虽然冷却系统不同，但这栋 GPU 大楼同样约 300MW。下图展示了该设施的规模——世界上没有任何其他建筑配备如此数量的风冷冷水机组！现场变电站的规模同样令人印象深刻。

![](https://substack-post-media.s3.amazonaws.com/public/images/30e49ed4-79f5-4240-abfa-c95a03e23858_1221x982.png)
*来源：SemiAnalysis 数据中心模型*

不仅单体建筑是全球最大，它们所在的园区还更加庞大。在亚特兰大，第二座 Fairwater 已全面开工。

![](https://substack-post-media.s3.amazonaws.com/public/images/451c01ca-805f-47b2-9cc1-5e7a95573d9f_915x970.png)
*来源：SemiAnalysis 数据中心模型*

在威斯康星州，第二座 Fairwater 即将开工，而且事情还没完——微软正在为一个更大的第三期做准备。我们相信微软设计了两栋**单体超过 600MW 的建筑**，每栋设施的 CPU/存储规模和柴油发电机数量都是标准约 300MW Fairwater 的 2 倍。下方展示了这些 600MW 建筑的总平面图。如果按时建成，它们将是世界上最大的单体数据中心。

![](https://substack-post-media.s3.amazonaws.com/public/images/46dea919-6d1c-4dcb-8ae1-4441ba81670b_3274x2436.png)
*来源：SemiAnalysis 数据中心模型、当地披露信息*

全部建成后，这里将成为全球最大的园区之一，IT 容量超过 2GW。

![](https://substack-post-media.s3.amazonaws.com/public/images/7eb9a716-f995-48e9-b9a6-3e523793d53c_1524x916.png)
*来源：SemiAnalysis 数据中心模型*

锦上添花的是，微软计划将所有这些主要 AI 区域通过超高速 AI 广域网（WAN）连接起来，带宽超过 300Tb/s，并可扩展至 10Pb/s 以上。一年多前，我们就在《**[多数据中心训练：OpenAI 击败谷歌基础设施的雄心计划](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais)**》一文中指出了这一点。

下方展示了一个假设的 5GW 分布式集群的网络设计示意图。我们将在报告后文基于我们的 [AI 网络模型](https://semianalysis.com/ai-networking-model/)，全面讨论 Fairwater 网络架构的方方面面。

![](https://substack-post-media.s3.amazonaws.com/public/images/c7977f4c-6b41-4573-bb9b-601b0912d8a4_964x927.png)
*来源：SemiAnalysis AI 网络模型*

## 数吉瓦级的「暂停」

在全速冲刺之后，微软突然以一种极为高调的方式踩下了刹车。从数据中心预租赁总余额来看，高峰期微软一家占了租赁合同的 60% 以上！但 2024 年二季度（自然季度）之后，其新增租赁活动冻结，而其他超大规模云厂商则大幅加码。如今微软在超大规模云厂商预租赁总产能中的占比已低于 25%。

![](https://substack-post-media.s3.amazonaws.com/public/images/538e35f6-5fbd-4883-8ece-cd0f3cb237de_3142x1770.png)
*来源：SemiAnalysis 数据中心模型*

当时，微软还退出了数吉瓦规模的不具约束力意向书（LOI），涉及多个地点，例如：

- 美国主要市场，如凤凰城和芝加哥。
- 欧洲主要市场，包括英国和北欧等。
- 在世界其他地区，微软的暂停波及澳大利亚、日本、印度以及拉美。

这些场址最终落入 Oracle、Meta、CoreWeave、Google、亚马逊等主要竞争对手手中。由于态度迟疑、对 AI 信心不足，微软永久性地让出了 AI 基础设施的很大一块份额。

此外，微软也大幅放缓了自建计划。下方图片列出了约 950MW 被「冻结」的 IT 容量。这还不包括弗吉尼亚、佐治亚、亚利桑那以及国际上的多座其他数据中心。

![](https://substack-post-media.s3.amazonaws.com/public/images/0c2b9d55-17df-4a7a-b661-4df7f3eb3ad8_2668x1308.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/c18c8d1f-5ae1-4c0b-97a5-4ae5e4eeae6c_2700x1360.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/4184049a-c133-41e5-962f-f7cd621b6c83_2422x1516.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/01663975-e798-477c-b3c4-583c7476dcb2_2618x1510.png)

在同一时间段内，其他玩家的主要数据中心已经从破土动工走到了承载业务负载。总计微软暂停了超过 3.5GW 本可在 2028 年前建成的产能。[细节详见数据中心模型。](https://semianalysis.com/datacenter-industry-model/)

# 微软 AI 业务组合拆解：IaaS、PaaS、模型、应用

要理解「大暂停」的成因与后果，让我们深入微软 AI 业务组合的各个部分。我们分析各层利润率的首选框架，是我们的「AI Token 工厂经济栈」：

- 从芯片到 token，范围广泛的供应商都暴露于 AI 基础设施建设浪潮。
- 当前，最大的单一利润率栈当然在芯片层，由 NVIDIA 75% 的毛利率（GPM）驱动
- 对于以下四层的终局利润率形态，业界仍存在激烈争论：
- 应用层（如 ChatGPT、Microsoft Copilot、Claude Code……）
- 模型层（如 Claude 4.5 Sonnet、GPT5-Pro、DeepSeek R1……）
- IaaS 层（如 CoreWeave 向 Meta 出租裸金属 GPU 集群、Oracle 向 OpenAI 出租 GPU、Nebius 在多租户集群中向初创公司提供 SLURM 和 K8s……）
- PaaS 层（如 AWS 通过 Bedrock 向财富 500 强企业出售 token、Nebius 将部分 GPU 集群连同 SLURM 和 K8s 出售给初创公司……）

按当前的定价，我们看到头部模型厂商在其直接 API 业务上获得 60%+ 的利润率。

![](https://substack-post-media.s3.amazonaws.com/public/images/66dd92da-11f9-44f5-b860-3bc4ee49dea7_1587x1145.png)
*来源：SemiAnalysis*

## Azure 的 AI 裸金属服务——放弃 $150B 的 OpenAI 毛利润、执行不力与 ROIC 之忧

在建造大规模裸金属 GPU/XPU 集群这门生意中，成功的玩家都掌握了大规模基础设施建设这门艺术。它是多种要素的混合：执行速度、对市场与终端用户需求的理解、选址，以及融资等等。

我们对 Oracle 的[深度解析](https://newsletter.semianalysis.com/p/how-oracle-is-winning-the-ai-compute-market)指出了其为赢下市场而做出的重大战略转变。在科技巨头之外，CoreWeave 是一个绝佳案例：一家起家时毫无规模的玩家，靠在上述标准上的完美执行赢得了市场。现在来看看微软的执行。

### 令人失望的执行，失去 Stargate 合同

要评估微软在裸金属上的成败，深入 Fairwater 项目很有帮助。2024 年初，围绕微软为 OpenAI 打造的 $100B「Stargate（星际之门）」项目传言四起。我们相信微软原计划将该集群部署在威斯康星数据中心园区。如前所述，按路线图该园区容量将超过 2GW。

当然，首份 $100B 的 Stargate 合同最终花落 Oracle 与得克萨斯州阿比林。在我们看来，**微软缓慢的执行**是关键原因。破土动工两年多后，一期仍未投运。相比之下，Oracle 于 2024 年 5 月在得州阿比林破土动工，9 月便开始运营。

![](https://substack-post-media.s3.amazonaws.com/public/images/02a70d27-882d-48f1-b1cb-d510135d17ee_2668x1308.png)

我们还认为微软对 1.5GW 扩容的规划很糟糕。从输电角度看，全部产能最快也要到 2027 年年中才能交付，**比 Oracle 阿比林集群突破 1GW 大关晚了一年**。微软跟不上 OpenAI 尽可能快速扩张的要求——暴露出其对市场的误解。这家 AI 实验室别无选择，只能另寻伙伴来满足其对近期算力的无尽渴求。

![](https://substack-post-media.s3.amazonaws.com/public/images/e0da1bdb-22ed-4380-ac8b-ca3aa651b060_2256x714.png)
*来源：SemiAnalysis 数据中心模型*

### 放弃 $150B 的 OpenAI 毛利润

如我们现在所知，Oracle 已成为 OpenAI 的主要 GPU 合作伙伴。过去十二个月里，双方签署了超过 $420B 的合同金额，[折合约 $150B 的毛利润——AI TCO 模型对每一家新兴 GPU 云的算力合同及其成本/利润率拆解都有详细建模。](https://semianalysis.com/ai-cloud-tco-model/)

按典型的 5 年合同期计算，每年 $30B 的毛利润本可让微软的年毛利润（FY25 财年为 $194B）提升 18% 以上。公平地说，失去 OpenAI 合同**并不只是执行问题**，在某种程度上也是一次有意识的决策。在微软看来，把 OpenAI 的合同全部拿下会损害 Azure 业务的质量，因为：

- 几年之内 OpenAI 将占到 Azure 收入的近 50%。
- 其利润率和资本回报水平远不如 Azure 历史上的云业务。

与微软整体业务相比，Oracle 的 AI ROIC 确实更低，为 20%，而微软（MSFT）整体目前为 35-40%。但我们也看到，一旦剔除将于 2030-2032 年间到期的 OpenAI 收入分成，微软自身 AI 业务的 ROIC 并不比 ORCL 高多少。

![](https://substack-post-media.s3.amazonaws.com/public/images/24c116bb-9c1e-4e8f-b351-41d075aa60a2_3303x1653.png)
*来源：SemiAnalysis Tokenomics 模型*

然而，微软似乎忘了自己不久前的历史教训：正是从以裸金属负载为主的 AI 收入结构，转向更多 API 和 token 工厂式的商业模式，其 ROIC 才得以持续改善。而如今，他们可能刚刚亲手放任一位竞争对手，为自己进军 AI 工厂业务完成了融资！

关于 OpenAI、Oracle 与微软经济模型的完整建模，请参阅我们业内首创的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)。Tokenomics 建立在我们的数据中心与加速器追踪之上，跟踪每一份主要算力合同，并拆解所有相关财务指标：增长、利润、ROIC、融资等等。

### 低估需求、RPO 份额流失、急需新兴 GPU 云产能

微软「大暂停」的一个关键教训是，它大大低估了来自 Meta 等其他玩家的 XPU 云需求规模。如今我们正在见证这一误判的影响。其他玩家预订的 RPO 已显著超过微软。

![](https://substack-post-media.s3.amazonaws.com/public/images/ac16e0c8-3841-4efe-89f5-7a1c899fa813_1231x559.png)
*来源：SemiAnalysis Tokenomics 模型*

微软如今已坚定重返市场，但扩大近期产能的选项已所剩无几。它被迫选择最糟糕的方案：从新兴 GPU 云租入 GPU，再转售给第三方——或以裸金属形式，或通过 Foundry 以 token 形式。Foundry 我们将在下文讨论。当然，「租入裸金属再转售裸金属」这门生意，将给 Azure 带来[显著低于以往](https://semianalysis.com/tokenomics-model/)的利润率。

![](https://substack-post-media.s3.amazonaws.com/public/images/dfa4edcc-15ab-45e5-9db6-02c1e13ef0ec_2861x1523.png)
*来源：SemiAnalysis Tokenomics 模型*

微软当年不屑于自建数据中心，等到意识到自己搞砸了，就只能把利润率拱手付给新兴 GPU 云。

## PaaS 层——并非所有 GPU 都得到同等的部署

### 金牌评级的云……面临降级风险

在今年 3 月发布的 [ClusterMAX 1.0](https://newsletter.semianalysis.com/i/174558503/azure) 中，我们讨论了 Azure 如何在网络性能与安全性、最新 GPU 的可用性上处于领先，并已拿下 OpenAI 算力建设中的最大份额。这使它稳居我们排名的金牌（Gold）梯队，仅次于 CoreWeave，与 Nebius、Oracle、Crusoe 等比邻。然而，到 11 月初 [ClusterMAX 2.0](https://newsletter.semianalysis.com/i/178057384/azure) 发布时，情况已经很清楚：面向 AI 负载的 CycleCloud 与 AKS 新功能的开发步伐已经停滞。

在我们与 140 多家算力买家的交流中——从 OpenAI、Meta、Snowflake、Cursor 等已成规模的 AI 公司，到 Periodic Labs、AdaptiveML、Jua、Nous Research、DatologyAI、Cartesia 等初创公司——有一点很清楚：**Azure 在托管集群或按需 VM 市场上并不是重要玩家**。Azure 面向大规模集群的 GPU 产能似乎直接流向了 OpenAI，剩下的零头则被财富 500 强传统企业里的个人开发者一抢而空。这些热衷于做内部 RAG 聊天机器人的公司，通常都签有企业协议，将全部 IaaS 独家采购自 Azure。

通过实际动手测试，Azure 卖不动面向 AI 的托管 SLURM 或 Kubernetes 集群的原因很清楚：**我们在 CycleCloud SLURM 集群上发现其在易用性、监控、可靠性和健康检查方面存在重大短板**。Azure 一次性整租整栋数据大厅给 OpenAI 的那种「批发式」裸金属体验，与 CoreWeave、Nebius 或 Fluidstack 等服务商提供给终端用户的体验截然不同。

业内典型的 GPU 算力买家寻找的仍然是 H100、H200、B200 或 B300 HGX 服务器，规模在 64 到 8,000 块 GPU 之间。寻找 GB200、GB300 或任何 AMD 产品的买家要少见得多。然而，微软为其最大客户（也就是 OpenAI）在 AMD GPU 以及 GB200/GB300 NVL72 机柜级系统上投入了大量的时间和精力。这一点既体现在工程师薪酬的 OPEX 上，也体现在 GPU 采购与新设施的 CAPEX 上。

另一个观察视角是开源社区。[Hugging Face](https://huggingface.co/) 是所有公司发布和下载开源模型的事实标准平台，来自微软 IP 的每日模型下载量比亚马逊少 5 倍，比 Google 少 3 倍。

微软把 OpenAI 的业务赶走了，但它也并没有因此拿下企业客户或长尾市场。在这一指标上，它显著落后于其他超大规模云厂商。

这一切的结果很清楚：正在积极寻找产能的 AI 公司都在别处下单。这些合同小到价值约 $1M 的 1 年期 64 块 GPU 合同，大到超过 $500M 的 3 年期 8,000 块 GPU 合同。我们看到有初创公司 3 月买了 256 块 H100，11 月就在寻找 9,000 块 GB300 NVL72。而现在，Azure 正错失这一切上行空间。

要服务好这批客户，我们认为 Azure 必须重塑其面向 AI 的 CycleCloud 与 AKS 产品，简化当前的集群部署与监控体验。他们需要构建健康检查、默认部署到集群中，并主动从硬件故障中恢复。他们还需要建设满编的 GTM 和支持团队，把这些集群交付到终端用户手中。我们在 ClusterMAX 2.0 中已提到，由于对从 A 轮初创到 AI 独角兽的糟糕使用体验，Azure 面临被降至银牌（Silver）的风险。

![ClusterMAX 2.0 排名](https://substack-post-media.s3.amazonaws.com/public/images/37dc82bd-d773-44b6-bc4a-d1f3ccf6d399_1738x873.jpeg)
*来源：SemiAnalysis ClusterMAX 2.0 评级，2025 年 11 月，http://clustermax.ai/*

### 「可互换机队」与主权 AI——一场关于推理负载走向的押注

话虽如此，Azure 显然具备成功的根基。它在全球拥有 70 个区域、超过 400 座数据中心。它运营着有史以来最大的 SaaS 业务，拥有向全球最大型组织销售的经验：从面向美国情报机构的「Azure Government Secret」，到面向中国消费者的 Windows PC。

Azure 战略的关键，是通过广泛的地理布局让 AI 更贴近企业客户。这是对 AI 负载未来形态的一次**方向性押注**：

- 当今最大的推理用例——ChatGPT 和编程智能体——对延迟并不敏感，而且随着[任务时间跨度](https://newsletter.semianalysis.com/p/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data?open=false#%C2%A7agentic-tasks-are-increasing-in-time-horizons)的不断拉长，这种不敏感只会进一步加剧。它们大多也不与敏感的企业数据交互。因此，**延迟和数据本地性并不重要**——游戏规则就是尽可能快地扩充产能，向全世界卖出更多 token。
- 未来，企业用例很可能成为增长的重要来源。它们必须满足高安全性、数据本地性法规，以及大型企业典型的环境与约束条件。它们还将与非 AI 负载协同处理，例如特定 Azure 区域内的 Cosmos DB 存储。缺点是，由于电力约束已波及全球大多数大都市圈，数据中心选址过程更加复杂。与那些在电力富余的「偏远之地」建设的同行相比，它们的爬坡速度会慢一些。

建设并利用全球布局，是微软打造「可互换（fungible）」机队这一主旋律的关键。他们已经取得了一些成功。例如字节跳动 Seed 在美国亚利桑那州而非中国或马来西亚训练其视频模型。我们相信 ByteDance Seed 在美国本土向所有主要超大规模云厂商都有租用。虽然这次训练跑在竞争对手的设施上，但这也说明某种程度的可互换性并非必需。

这一基础设施战略与 OpenAI 等头部 AI 实验室截然不同。鉴于最耗算力的负载需要数分钟才能响应（如 Deep Research、推理模型），增加几毫秒的网络延迟对它们无关紧要。

随着 AI 任务时间跨度的拉长，与用户地理位置的远近越来越无关紧要。

数据中心可以见缝插针地落地，服务全球流量。后训练（post-training）负载的算力需求也在快速增长，这类负载同样对延迟不敏感，也不需要大量集中式算力，进一步强化了这一趋势。

### 折旧年限与 Azure 中 GPU 的未来

若把这个「可互换机队」打开细看，会发现一个重要问题——一个近来被大量讨论的问题，那就是：折旧。

以做空闻名的 Michael Burry 最近声称，所有超大规模云厂商（Meta、Google、Oracle、微软、亚马逊）都在通过延长 IT 资产的使用年限来人为推高利润。这一操作把「使用年限」从 2020 年的 3-5 年延长到了如今的 5-6 年。

![](https://substack-post-media.s3.amazonaws.com/public/images/d7a299bc-dfad-41df-973c-f5cc27b3ace5_1476x700.png)
*来源：Michael J. Burry 发于 X（the everything app）*

Burry 博士的论断建立在一个假设之上：NVIDIA 的产品周期如今只有 2-3 年，远低于资产的使用年限。我们认为这是该论证的致命缺陷。新的会计处理虽然在短期对公司有利，但同样建立在数据中心真实运营经验的基础之上。

早在 2020 年微软、Meta 和 Google 把使用年限从 3 年延长到 4 年时，我们还处在公元前 2 年（BC，ChatGPT 之前）。而到了如今公元 3 年（AD，ChatGPT 诞生之后），使用年限的延长已被证明对渴求 CAPEX 的超大规模云厂商有利。那么，2020 年起 IT 设备发生了什么变化并一直延续到 2025 年？答案是：可靠性，以及激励。

Dell、SuperMicro、HPE、联想（Lenovo）、Cisco 等服务器 OEM 厂商长期以来销售的标准服务器保修期为 3 到 5 年。5 年保修当然更贵，但 6 年、7 年的延保选项也比比皆是。价格固然上涨，但厂商要做的不过是备足备件，以便对损耗节点上门维修。与此同时，Cisco、Arista、Aruba、Juniper 等网络设备厂商已在交换机上尝试终身保修。存储厂商也是如此——只要每年支付支持合同，他们就会不断为你更换损耗的硬盘。可以把它想象成汽车：市场高端用户可能每 2 年就租赁换新他们的奔驰，而另一些人则只花油钱和保险费，开着车龄 20 年的老爷车。

看看全球最大的 HPC 集群和超级计算机，这一点便得到印证。这些领先系统运行着市面上最大、最强、最热（有时也最高效）的处理器。超算中心是最早采用液冷的，他们的经验是围绕系统建造数据中心，而不是把系统塞进数据中心。

橡树岭国家实验室的 IBM Summit 曾长期位居 Top500 榜全球最快超级计算机。它于 2018 年 6 月投产，在连续运行 6.5 年后于 2024 年 11 月退役。Summit 采用的 IBM Power9 处理器发布于 2016 年，采购更早在 2014 年就已完成。

「富岳」（Fugaku）2020 年安装于日本理化学研究所（RIKEN），至今仍在运行，位列 Top500 第 7。Sierra 2018 年安装于劳伦斯利弗莫尔国家实验室（LLNL），至今仍在运行，位列第 20。神威·太湖之光（Sunway TaihuLight）2016 年安装于中国无锡的国家超级计算中心，至今仍在运行，位列第 21。El Capitan、Frontier、Aurora 等 Exascale（百亿亿次）系统（分列榜单第 1、2、3 位）于 2021-2025 年间陆续投运，预计将运行至 2027-2032 年。

最后，配备 14,400 块 H100 的 **[Eagle——微软 NDv5](https://www.top500.org/system/180236/)** 于 2023 年安装，现位列第 5。我们预计该系统利用率很高，并将继续运行多年。

再看当下的云服务商，我们在 AWS 上仍能买到配备 8 块 V100 GPU 的 p3.16xlarge 实例。在 Shadeform、Prime Intellect、Runpod 等市场上，也能找到来自 DataCrunch、Paperspace、Lambda Labs 等底层供应商的类似实例。

V100 于 2017 年 5 月发布，2017 年秋季批量出货，NVIDIA 的最后一批产品出货发生在 2022 年 1 月。换句话说，从这款新 GPU 发布算起，NVIDIA 的备件供应持续了 5 年以上。超大规模云厂商和 OEM 有充裕的时间备好备件，让这些实例一直运行到今天——距离 V100 GPU 开始出货已整整 8 年。

![](https://substack-post-media.s3.amazonaws.com/public/images/608fbb5d-0424-4d11-b26c-4e380bff0cfb_1894x986.png)
*在我们的 AWS 控制台上找到一些在售的 V100*

当然，如今按每 MW 收入计算，V100 已算不上一门好生意。以至于我们了解到，有超大规模云厂商正在从老数据中心里拆除 V100、A100 甚至较老的 H100 GPU，为最新最强的产品腾出空间。关键在于，它们这么做并不是因为这些 GPU 磨损老化、寿终正寝，而是由于电力和机房空间的约束，拆除收益较低的资产，换上收益更高的资产。

优化 GPU 云经济学的关键，在于***最大化其经济寿命***。我们的 AI 云 TCO 模型提供了有用的框架。分析一个 H100 集群的 TCO 可以看到，剔除资本成本后，剩余的运营成本为 $0.30-0.40/GPU/小时。问题是：5 年之后，一块 GPU 还能否创造出高于这一水平的收入。

![](https://substack-post-media.s3.amazonaws.com/public/images/fa5397ff-25a2-4c35-a0a2-83fa8568eeda_1125x776.png)
*来源：SemiAnalysis AI 云 TCO 模型*

这一运营成本必须与每块 GPU 榨取的收入相匹配。自然，GPU 的定价权会迅速衰减，因为 NVIDIA 会不断发布在每美元吞吐量和每瓦特吞吐量上都有实质提升的新芯片。我们的 [AI 云 TCO 模型](https://semianalysis.com/ai-cloud-tco-model/)（全球大多数最大的 GPU 买家及其财务支持方都在使用）为所有 NVIDIA、AMD、TPUv7 和 v8、Trainium2 和 3 的 SKU 提供长期租赁价格预测，此外还有详细的集群物料清单（BOM）分析。

![](https://substack-post-media.s3.amazonaws.com/public/images/d57826ad-1a7d-4bae-bcbd-752b536b4b85_1775x1194.png)
*来源：SemiAnalysis AI 云 TCO 模型*

我们历史预测的命中率已被证明相当精准！但从 Azure 这类公司的视角看，目标是在整体市场之上保持更高的定价权。这一点尚无定论，但可能以多种方式实现：

- 通过利用企业客户关系、PaaS 层和垂直整合（应用、模型、token 等），Azure 或许能从 6 年机龄的 GPU 中榨取足够的价值，避免提前退役。
- 另一条路径同样与企业业务相关：在加速计算之外向上销售更高利润率的服务（例如数据库等非 AI 服务）。即使 6 年机龄的 GPU 单独看并不盈利，如果它们恰好是促成更高利润率服务销售的原因，继续运营它们或许就是合理的。

在我们看来，这正是 Azure「可互换机队」战略可能成立、并使其 ROIC 在结构上高于其他玩家的原因。主要的未知数仍是企业采用的规模，以及 Azure 能否向上销售更高价值的服务。

![](https://substack-post-media.s3.amazonaws.com/public/images/d57f668f-d504-4b6d-a513-9145e2746ba1_1024x670.png)
*来源：SemiAnalysis AI 云 TCO 模型*

未来会怎样？Vera Rubin 会兑现性能承诺、促使超大规模云厂商如 Burry 博士所言，把仅服役 2-3 年、完好且仍在创造收入的 GPU 拆掉吗？还是会看到我们 H100 定价数据的下限在未来继续坚挺？这些问题尚待解答，但我们的 TCO 模型给出了我们的最佳估计。依托我们对 GPU 云的专有测试（ClusterMAX）以及通过 [InferenceMAX](https://inferencemax.semianalysis.com/) 进行的每日基准测试，我们力求提供市场上最好的洞察。我们免费开源的 InferenceMAX 平台展示了系统级创新（如 NVIDIA 的 GB200 BVL72）如何在特定用例和配置下，相比更传统的基于 HGX 的 GPU 带来数量级的改进。

![](https://substack-post-media.s3.amazonaws.com/public/images/6bd7ae27-aa0f-4435-b79b-109a5f40c1d1_2160x1088.png)
*来源：SemiAnalysis InferenceMAX——inferencemax.ai*

### Azure Foundry：企业 Token 工厂

Azure Foundry 是微软的「Token 即服务（Token-as-a-Service）」业务，提供多种模型：既有 M365 Copilot、GitHub Copilot 等自家服务在内部使用（第一方 token，1P），也有外部客户希望通过推理端点使用模型（第三方 token，3P）。Azure Foundry 的打法与 OpenAI API 类似，同时争夺个人和企业用例。凭借对 OpenAI 模型权重的 IP 权利，Azure 还可以独立做出定价决策。

目前，大部分 GPT API token 直接经由 OpenAI 处理，但我们预计 Foundry 将成为微软未来的重要增长动力，并夺回部分份额。对微软至关重要的一点是：无论经由 OpenAI API 还是 Azure Foundry 提供服务，到 2032 年为止，**所有 API 推理算力的 100% 份额都归 Azure**。

![](https://substack-post-media.s3.amazonaws.com/public/images/6b4ae112-15c1-4bfa-bdfe-0e899cbbd7a0_1918x1030.png)
*来源：SemiAnalysis Tokenomics 模型*

不过，我们认为面向企业销售 token 的生意仍处于起步阶段。Alphabet 的桑达尔·皮查伊（Sundar Pichai）在 2025 年三季度财报电话会上给出了一条有意思的披露，印证了我们的立场：

> 过去 12 个月里，近 150 家 Google Cloud 客户各自使用我们的模型处理了约 1 万亿 token，应用场景十分广泛。

这条披露意味着，向这 150 家企业销售 Gemini token 的收入还不到 GCP 业务的 0.5%。

把 token 换算成收入，比看上去要复杂得多。我们经常看到分析师犯下大错，比如输入/输出比例失当、漏算缓存 token，或算错价格。我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)全面刻画了 token 生产的经济模型，以及如何把 token 和瓦特换算成收入、利润与 RPO。

# 应用层：GitHub Copilot 的护城河陷入围攻

在代码辅助的应用层，微软凭借 GitHub Copilot 享有绝对统治力。微软拥有第一个行内代码补全模型（即如今俗称的「tab」模型），并且凭借独家的 IP 访问权，早早把 GPT-4 集成进了 Copilot。

从远处看，微软的堡垒似乎坚不可摧。它拥有 VS Code 和 GitHub 这两个行业标准工具，独家掌握用于产品开发的 OpenAI 模型 IP，还坐拥一个庞大的企业客户基本盘可供销售。

然而，他们低估了一批通过 fork VS Code 来打造更紧密、更完善的模型与代码库集成的初创公司的崛起，这些挑战者的合计规模因此得以超越 Copilot。一个关键的促成因素，是这些初创公司采用了 Anthropic 的模型。

![](https://substack-post-media.s3.amazonaws.com/public/images/118c4f46-97ed-4343-9e24-f90eae892038_1638x849.png)
*来源：SemiAnalysis Tokenomics 模型、公司披露/公告*

2025 年初，微软不情愿地将 Anthropic 模型加入 GitHub Copilot，为此付出了不小的利润率代价。GitHub Copilot 从几乎 100% 提供第一方 token，变成不得不从 Anthropic 采购相当一部分 token——后者坐享 50-60% 的毛利率。

各实验室也亲自下场做产品。用户被绑定在一套模型上，但这些模型正是基于生产环境中实际使用的 Harness 和环境训练的。这带来了高度优化的体验——Codex 和 Claude Code 的收入爬坡表明，这种体验非常受欢迎。

此后，微软进一步加码其「模型超市」生态赌注，最近推出了 Agent HQ，可接入来自 Google、xAI 等多家实验室的智能体。

![](https://substack-post-media.s3.amazonaws.com/public/images/304dbcb6-301c-44d2-acd0-98144bbc460d_1792x945.png)
*来源：GitHub*

鉴于其对 OpenAI 模型权重的访问权限只延长到 2032 年，微软需要为其当前利润率最高的 OpenAI 模型产品准备一套备用方案。

# 微软的自研模型：MAI

微软已发布 3 个 MAI 模型，覆盖文本、图像和语音。文本模型 MAI-1 目前在 LMArena 上排名 38 位左右，但尚未通过聊天或 API 公开提供。该模型是在 15,000 块 H100 上训练的大型 MoE 模型，下一款模型将是规模大得多的多模态 LLM。

另外两个分别是图像模型和语音模型。图像模型目前仍位列 LMArena 前十，两者都已在 Copilot 中提供。

对微软来说，后两个模型代表的是一类可以低成本、质量尚可地提供服务的用例。它们远谈不上挑战最先进（SOTA）模型，但我们相信，微软正在悄悄筹备更大规模的内部训练投入，未来几年将攀升至接近 **$16Bn 的年化算力**支出。

![](https://substack-post-media.s3.amazonaws.com/public/images/0fecefcb-28de-49e8-846c-e38e86853baf_3312x1629.png)
*来源：SemiAnalysis Tokenomics 模型*

# Office 365 Copilot

Microsoft Copilot 是一个总括性品牌，其涵盖远不止 GitHub Copilot。还有面向销售、财务、客服、安全等的各种 Copilot。这一品牌家族本身的月活用户已超过 1 亿，将成为推动整体 AI 普及的重要引擎。

打造 Office 365 Copilot 的最新努力落在 Office 智能体（Office Agent）上，下文我们将深入其中的 Excel 智能体。这些智能体的总体目标，是以自主、可用、对用户有价值的方式在微软生态中执行操作。

# 微软的优势：OpenAI IP 与 Office 用户数据

能够访问 OpenAI 的模型、权重和代码库，使微软可以从 OpenAI 模型的原始思维链（Chain of Thought）中进行蒸馏。[蒸馏比小模型后训练更有效](https://newsletter.semianalysis.com/i/174558642/distillation-is-better-than-rl-for-small-models)，这意味着微软无需付出可观的算力成本即可获得强大的能力。

对 OpenAI IP 的访问权还让微软能够用自己的数据微调 OpenAI 模型，这些数据可能比外部公司（在 Office 套件之上构建 Harness 或环境的那些）能拿到的更细粒度、更底层：

> 我们必定会在所有产品中最大限度地使用 OpenAI 模型。

Excel 智能体是 **OpenAI 某款推理模型**经过后训练的版本。据微软宣称，其效果优于前沿实验室的产品。

![](https://substack-post-media.s3.amazonaws.com/public/images/ab337e9d-9e44-4114-b633-95b2f5dd2eb6_1588x916.png)
*来源：Microsoft*

在深入剖析了 Azure 的 AI 业务之后，我们现在把注意力转向 Azure AI 硬件栈的两个关键部分：

- 微软真正的芯片战略：如何在 NVIDIA、Maia、OpenAI、AMD 等之间取得平衡
- Azure 的网络架构，及其对众多供应商的影响

# Mama Ma-ia!：自研 ASIC 的挣扎

在自研芯片开发上，微软在超大规模云厂商中垫底，甚至没有努力追赶。

微软于 2023 年底展示了其 Maia 100 加速器，是四大超大规模云厂商中最后一个拿出 AI 加速器 ASIC 的。

正如对第一代芯片的预期，Maia 100 既没有大批量生产，也没有部署生产负载。这款芯片在生成式 AI 热潮之前就完成了架构设计，导致其缺乏适合推理的内存带宽。ASIC 项目需要迭代多代，才能把有意义的算力从商用（merchant）系统上迁移过来。
