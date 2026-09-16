---
title: "AI 数据中心正在推高美国家庭电费吗？"
title_en: "Are AI Datacenters Increasing Electric Bills for American Households?"
subtitle: "电价误区、PJM 糟糕的市场设计、容量价格 9.3 倍上涨、ERCOT 与 PJM 的电网可靠性与扩张对比"
date: 2026-03-03
source: https://newsletter.semianalysis.com/p/are-ai-datacenters-increasing-electric
crawled: 2026-09-15
authors: ["Aishwarya Mahesh", "Jeremie Eliahou Ontiveros", "Ajey Pandey", "Dylan Patel", "Reyk Knuhtsen"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AI 数据中心正在推高美国家庭电费吗？

> 原文：[Are AI Datacenters Increasing Electric Bills for American Households?](https://newsletter.semianalysis.com/p/are-ai-datacenters-increasing-electric) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**电价误区、PJM 糟糕的市场设计、容量价格 9.3 倍上涨、ERCOT 与 PJM 的电网可靠性与扩张对比**

*SemiAnalysis x Fluidstack 将在 GTC 期间举办一场为期 48 小时的全栈 AI 基础设施黑客马拉松，3 月 15 日开启，主题「从电力到预填充（Power to Prefill），从尘土到解码（Dirt to Decode）」。演讲嘉宾来自 OpenAI、GPU MODE 和 Thinking Machines，并提供算力资助和 GPU 集群访问权限，来与最优秀的人一起构建吧：[点此申请](https://luma.com/SAxFSHack)。*

数据中心负荷增长及其对电价的影响，这一话题仍被广泛误解，就像我们最近[辟谣过的耗水传言](https://newsletter.semianalysis.com/p/from-tokens-to-burgers-a-water-footprint)一样。在 2025 年 6 月住宅电价一夜之间[跳涨约 20%](https://www.pa.gov/governor/newsroom/2025-press-releases/gov-shapiro-s-legal-action-again-averts-historic-price-spike-acr)之后，它成了 2025 年新泽西州选举的焦点议题。有人甚至开始把矛头指向该州为 Microsoft 建设的 300MW Nebius AI 数据中心——鉴于[其 85% 以上的电力为自发](https://newsletter.semianalysis.com/p/how-ai-labs-are-solving-the-power)，这种说法令人啼笑皆非。AI 数据中心真的让家庭多付了 20% 的电费吗？

本报告通过分析美国两个最大的能源市场——它们同时也是最大的 AI 数据中心聚集地——来探讨这个问题：一个是 PJM 互联区域，即覆盖美国东部 13 个州（包括新泽西州）的电网运营机构；另一个是负责得克萨斯州电网的 ERCOT。在「孤星之州」得州，电价过去三年大致保持稳定。反观 PJM 区域的 6,700 万居民，2026 年的电费账单相比「AI 数据中心前」时代将平均上涨约 15%。为何有如此巨大的分化？简而言之，从实证角度看，问题出在政府政策，而不是 AI。

![](https://substack-post-media.s3.amazonaws.com/public/images/f4cbff97-5557-4b44-aaa1-539add752ebc_2400x1125.png)
*来源：SemiAnalysis 能源模型（Energy Model）、PJM、Monitoring Analytics*

我们认为，在 PJM，糟糕的市场设计是罪魁祸首。PJM 家庭电费 15% 的涨幅中，大部分来自一个被广泛误解、多少有些隐晦的机制：BRA 容量拍卖。如下图所示，2025/26 年度拍卖价格较上一年上涨了 9.3 倍。更糟的是：这一上涨是由一场「模拟」驱动的，并不反映实际状况。它在很大程度上取决于中央计划者（PJM）做出的供需预测——正如我们将要解释的，这种预测有着屡次严重失算的历史。

![](https://substack-post-media.s3.amazonaws.com/public/images/9e61dd7a-0a0b-4903-9694-84e6529ae506_3179x1543.png)
*来源：PJM BRA 报告*

许多人把矛头指向 AI 数据中心的激增，这可以理解。PJM 区域正处于 AI 热潮的最前沿：[Google 尤其在俄亥俄州哥伦布市周边训练其 Gemini 模型](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais)，而位于印第安纳州和俄亥俄州的 [Anthropic/Amazon 的「Project Rainier」](https://newsletter.semianalysis.com/p/amazons-ai-resurgence-aws-anthropics-multi-gigawatt-trainium-expansion)和 [Meta 的「Prometheus」](https://newsletter.semianalysis.com/p/meta-superintelligence-leadership-compute-talent-and-data)都位列我们评选的[全球五大 AI 数据中心](https://www.youtube.com/watch?v=a-9egkpaZUw)。PJM 还坐拥全球最大的数据中心枢纽：北弗吉尼亚。

再看看得克萨斯州。该州正经历同等规模的 AI 建设浪潮，OpenAI、Google DeepMind、Anthropic 都在这里建设大型设施。然而得州的电力期货过去一年只变动了几个百分点。没有 9 倍的飙升，没有危机——市场设计截然不同。

![](https://substack-post-media.s3.amazonaws.com/public/images/30a916ae-8f6f-462a-a184-7622bd295775_1808x1110.png)
*来源：Bloomberg*

让我们深入探究。本报告聚焦 ERCOT 和 PJM，因为它们是全美两个最大的能源市场，也是 AI 革命的中心。我们将深入剖析两者各自的市场设计，解释它们如何应对爆发式增长的 AI 数据中心负荷，以及这将如何传导到千家万户。

随后，在付费墙之后，我们将讨论供应链层面的影响。我们认为市场约束正在发生剧变，而许多人尚未察觉。这一转变影响着主要的 AI 受益者，如独立发电商（IPP）（Vistra、Constellation、Talen 等）、设备供应商，以及加密矿企这类数据中心开发商。

希望获得更深入分析的机构用户，请订阅我们的[能源模型](https://semianalysis.com/energy-model/)和[数据中心行业模型](https://semianalysis.com/datacenter-industry-model/)。后者按季度追踪并预测 2017-2032 年间超过 5,000 座独立设施及其电力容量。能源模型则在此基础上构建能源供需分析：追踪并预测美国每一座电厂的运营情况，估算其真实的 ELCC（有效负荷承载能力），分析并网队列动态，并与我们的数据中心需求数据进行匹配。

我们先简要解释「容量（capacity）」究竟是什么、它如何进入你的每月账单，然后再进一步深入市场设计。

*本报告是 SemiAnalysis 与 ADM Investor Services（ADMIS）合作的成果，后者是一家领先的期货经纪与清算公司。*

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

## 容量：为电厂一年 95% 的时间闲置待命买单

总体而言，家庭每月电费账单由以下几部分构成：

- **能量（Energy）**：在解除管制的地区（包括 PJM 的 13 个州和 ERCOT/得州），这部分取决于批发价格，即电力的实时供需。
- **容量（Capacity）**：这项费用在 ERCOT 并不存在，但在 PJM 举足轻重。它取决于**容量**的供需——即每年只在必要的峰值时段开启几个小时的电力。在 PJM，这笔费用每年通过一场大型拍卖确定。
- **输配电（T&D）**：配电网的相关费用。

> 这仍是一个高度管制的领域。输配电服务商通常赚取预先确定的、受监管的股本回报率（ROE）。因此，输配电资产的利用率会影响消费者电价。本报告不会深入这一点——留待未来的深度解析。

- **其他**：税费、零售加价、辅助服务等。由于各地情况不同，本报告不展开。

![](https://substack-post-media.s3.amazonaws.com/public/images/6a888155-3f13-42d0-b47c-2633abbebb27_2848x1504.jpeg)
*来源：SemiAnalysis 估算、EIA*

容量市场的目的，是确保家庭和企业始终有电可用，包括夏季和冬季的峰值日。作为参照：单日之内，仅**纽约市**一地的电力负荷波动幅度就可达 **2 吉瓦（GW）**，而其日峰值约为 **6-8 GW**。热浪来袭时，当所有人同时开动空调，这座城市可以吸纳 **10 GW** 的电力。

在 PJM，为确保需要时有容量可用，我们向电厂所有者付费，让它们的资产在全年 95% 以上的时间里处于待命状态。所付价格由每年举办一次的远期拍卖决定，随后分摊到该区域所有电力用户头上。如下文详述，在 2025/26 交付期，这一价格上涨了 9.3 倍。

而 ERCOT 则是一个「纯能量（energy-only）」市场，没有单独的容量拍卖。实时价格信号决定「稀缺性」，并激励电厂自行解决问题。其中有一些技术细节我们会在报告后文详述，但根本区别在于：ERCOT 没有集中式的年度容量拍卖，而是依靠实时的市场力量。

## PJM：$16B 的模拟

容量市场设计的核心问题在于，它直接受中央计划者 PJM 的供需预测影响。任何预测误差都可能导致数十亿美元的不当支出。在 2025-26 拍卖中，这笔支出总计达 $16B，分摊到 PJM 区域的每一位居民和企业头上。

### 基础剩余拍卖（BRA）如何运作

PJM 通过上述远期容量市场为系统容量付费，该机制称为[基础剩余拍卖（Base Residual Auction，BRA）](https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2025-2026/2025-2026-base-residual-auction-report.pdf)。这是每年举办一次、提前两年进行的拍卖：例如，PJM 的 2027/28 容量需求在 2025 年底完成拍卖。

与以 $/MWh（即给定小时内消耗的电量）交易的批发能源市场不同，BRA 以 $/MW-day（即给定日内预置的峰值电力）为单位交易。PJM 的需求预测决定需要多少兆瓦的发电机、电池和其他资源，才能满足其预测的最大电力负荷（加上备用裕度），然后举行拍卖来发现这些容量的价格。最终，电网上的所有成本都由用户买单，因此当容量拍卖价格飙升时，这一飙升就会传导到家庭电费账单上。

直到不久前，BRA 还算兑现了承诺。2025 年夏季 PJM 酷热难耐，6 月 23 日和 24 日分别创下 PJM 历史第三和第四高峰值日的纪录。灯没有熄灭，因为发电容量足以满足负荷。

但如今，这种可靠性是以异乎寻常的代价换来的。2024 年 6 月至 2025 年 5 月（2024/25 服务期），容量价格为 $29/MW-day。而在当前的 2025/26 服务期，容量价格暴涨 9.3 倍至 $270/MW-day，部分地点的价格甚至接近 $450/MW-day。随后的 2026/27 和 2027/28 拍卖继续以创纪录的价格出清。市场曾普遍认为价格还会更高，但联邦监管机构设定了 $329/MW-day 的价格上限。最近一次拍卖（2025 年 12 月 17 日）已连续第二年触及价格上限。

![](https://substack-post-media.s3.amazonaws.com/public/images/df36a940-6317-428c-9e9e-f171b1d7c3f2_3179x1543.png)
*来源：PJM BRA 报告*

[PJM 把「失控」的电力成本归咎于极端天气和超大规模云厂商数据中心及 AI 的电力需求，这一说法也渗透进了主流新闻。](https://insidelines.pjm.com/maintaining-grid-reliability-through-highest-peaks-in-a-decade/)但这种解释掩盖了 PJM 自身的责任，因为容量价格是提前一年多、基于 PJM 自己设计的模拟模型确定的。

### 幕后的模拟机制

容量价格基于一条人为构造的供需曲线，内部称为[可变资源需求（Variable Resource Requirement，VRR）曲线](https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2026-2027/2026-2027-bra-report.pdf)。VRR 曲线建立在 PJM 的内部预测模型之上，而不是市场对未来的真实判断。数据中心负荷的预测增长改变了这条曲线上的出清价格，在没有任何公开竞价程序的情况下推高了价格。

![](https://substack-post-media.s3.amazonaws.com/public/images/c7cfa0ed-0954-4a3a-9ebf-dd7c2609aaa2_1814x1230.png)

然而，VRR 曲线是由一张假设之网构建而成的，其中许多假设依赖于非公开模型和专有数据。预测负荷哪怕只有温和变化，也可能引发出清价格的大幅波动。容量市场对预测输入的极端敏感性意味着：数据中心负荷数字哪怕只偏差几个吉瓦，都会产生灾难性后果——改变出清点附近的曲线形状，并推高价格。

### 数据中心被指为容量价格飙升的元凶

[PJM 的内部市场监督机构（IMM）](https://www.monitoringanalytics.com/reports/reports/2025/IMM_Analysis_of_the_20252026_RPM_Base_Residual_Auction_Part_G_20250603_Revised.pdf)——联邦能源管理委员会（FERC）要求的独立监督实体——对 2025/26 市场进行了替代情景模拟，让人们得以罕见地窥见 PJM 通常不透明的方法论。根据该市场监督机构的分析，数据中心确实难辞其咎：

- 从预测中**剔除所有数据中心**，PJM 峰值负荷将减少 7,927 MW，总容量支付将**减少 $9.33B**——比实际价格低 64%。
- **只保留已通电的数据中心**，峰值负荷将减少 4,654 MW，总容量支付将**减少 $7.74B**——较实际价格削减 53%。对于采用无限制 VRR 曲线的 **2026/27** 拍卖参数，IMM 估计数据中心合计负荷约为 11,993 MW。

根据 IMM 的分析，仅数据中心负荷的增量增长，就足以解释容量成本相对「无此负荷」假想电网大约翻倍的现象。[IMM 归因出 2025/26 年约 7.9 GW 的数据中心额外需求，2026/27 年约 12 GW。](https://www.monitoringanalytics.com/reports/reports/2025/IMM_Analysis_of_the_20252026_RPM_Base_Residual_Auction_Part_G_20250603_Revised.pdf)其他任何因素都远不及此。

但所有这些模拟都遮蔽了一个更深层次的问题：决定电价的主拍卖**同样基于一场模拟**。VRR 曲线是一条人为构造的供需曲线，基于 PJM 为自己做的预测。如果该预测不准确，这些偏差就会扭曲整个容量市场。

而我们相信这个预测**确实**不准确。我们的方法论[逐座追踪 PJM 区域每一座数据中心的精确建设时间表](https://semianalysis.com/datacenter-industry-model/)，结果显示 PJM 的预测很可能过于乐观。这不是因为需求不足，而是因为数据中心建设延期（正如我们的[工业模型](https://semianalysis.com/industrials-model/)所强调的）、GPU 生产与组装延期（正如我们的[加速器模型](https://semianalysis.com/accelerator-hbm-model/)所解释的）以及其他供应链问题。新硬件平台初期往往问题缠身，达到满容量投运所需的时间也长于往常。

![](https://substack-post-media.s3.amazonaws.com/public/images/f6daac55-f442-4fb9-a3bc-5ecc70c7a318_3180x1716.png)
*来源：SemiAnalysis 数据中心模型、PJM*

下面就是一个绝佳例证。PJM 自己的数据表明，它连提前一年的预测都做不准。2024 年，数据中心负荷预测较 2023 年的预测被下调了 800MW。2025 年，历史重演：数据中心负荷预测较一年前（即 2024 年）的预测又被下调了 1.1GW！

![](https://substack-post-media.s3.amazonaws.com/public/images/482f7f80-0d44-44d8-877b-c9e4be675c83_2222x708.png)
*来源：PJM、Monitoring Analytics*

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

### 远期能源价格讲述了另一个故事

PJM 的能源市场仍更接近一个真正的市场：供需平衡形成每 MWh 电力的动态价格。这些价格在热浪期间飙升、在温和天气回落，并借助分散的市场参与者跟踪天然气价格、输电阻塞和可再生能源出力——一如市场应有的样子。

PJM Western Hub 远期价格——能源交易员对未来看法的最流动基准——在 2028 和 2030 时间窗已上涨 12-20%，2026 时间窗的涨幅略高。这些涨幅不可忽视，但与容量市场 9.3 倍的爆炸完全不可同日而语。PJM 重度依赖模拟的容量机制正在制造一场远期能源市场并不认可的价格冲击。交易员们用真金白银、承担真实风险，并没有把 PJM 模拟 VRR 曲线所产生的那种恐慌计入价格。

![](https://substack-post-media.s3.amazonaws.com/public/images/72c39ddb-b566-436e-8655-7e8517b918ed_1808x1110.png)
*来源：Bloomberg*

### PJM 的供给侧预测同样来自模拟

PJM 的预测和方法论同样影响着预测的供给侧。在 AI 数据中心热潮兴起的一年前，问题就已经开始显现。如下图所示，总报价容量在短短四年间被削减了约 35GW。这些供给去哪了？

![](https://substack-post-media.s3.amazonaws.com/public/images/6ea967ff-1bf5-4d18-8612-fc7098521e9d_3179x1742.png)
*来源：PJM*

如下图所示，燃煤机组退役是最大的驱动因素，但 PJM 还引入了重大的方法论变更，导致近 20GW 的供给凭空消失。其中，PJM 对天然气电厂核算方法的变更，一夜之间就让 14GW 消失了。

![](https://substack-post-media.s3.amazonaws.com/public/images/6f936070-e91d-4ce3-9b91-f9f59e93c834_3979x1919.png)
*来源：PJM*

### 容量价格如何冲击家庭账单

2026/27 基础剩余拍卖（BRA）$329/MW-day 的出清价格，意味着 PJM 每一个负荷都要承受切实的成本上涨。这些成本最终通过零售电价收回，体现为公用事业公司、供应商和大客户更高的容量费用。总体而言，这场拍卖对应约 **$16B 的总容量支付，折合每 MW 约 $120,000**。

要估算其对零售账单的影响，我们需要以下数据点：

· 家庭平均用电量：在 PJM，为每月 880 kWh。

· 「负荷率（load factor）」，即平均用电量与峰值用电量之比。实证数据显示 40% 是常见值。

· 容量价格：按 $329/MW-day，除以每天的小时数，再应用 0.4 的负荷率，得到 $34/MWh（即 3.4 美分/kWh）。

用 3.4 乘以月用电量（880 kWh），得到每月 $29.9 的容量支付。鉴于拍卖已经出清，我们几乎可以断定：家庭每月将比两年前多付 $25-30！

![](https://substack-post-media.s3.amazonaws.com/public/images/f4cbff97-5557-4b44-aaa1-539add752ebc_2400x1125.png)
*来源：SemiAnalysis 能源模型、PJM、Monitoring Analytics*

现在让我们把目光转向得克萨斯州，看看电价如何应对大规模 AI 数据中心的涌入。

## ERCOT：同样的负荷增长，没有价格冲击

得克萨斯州电力可靠性委员会（ERCOT）是一个更容易理解的市场。它运行统一的市场机制，基于实时价格平衡供需。ERCOT 没有两个相互分离的市场，也不做直接影响市场需求的预测。

### 用稀缺性定价取代容量拍卖

ERCOT 不采用一年一度的拍卖驱动的容量市场，而是使用基于运行备用需求曲线（Operating Reserve Demand Curve，ORDC）的实时稀缺性价格加成。当电力供需平衡过于紧张时——比如所有人的空调同时运行——实时能源价格便会飙升，从正常的 $10-50/MWh 一路冲到 $5,000/MWh 的上限，在输电受限区域还有额外的加成。

![](https://substack-post-media.s3.amazonaws.com/public/images/7c2ea8ff-d1ba-4c7b-b934-26a53ba74b88_1799x1114.png)

这种稀缺性价格结构，让每年运行不足 100 小时的容量资源（燃气调峰电厂、电池等）得以回本，因为对一座 50 MW 的电厂或电池系统来说，那寥寥数小时的运行仍可能带来数百万美元的年收入。

换句话说：在 PJM，中央运营机构负责分析系统、确定容量需求，并向电厂所有者保证为提供容量付费。在 ERCOT，没有任何保证，做分析、判断市场容量是否充足的责任落在资产所有者自己身上。实时价格信号就是市场约束的证明。

### ERCOT 的需求预测：惊人——却基本被无视

这一差异尤其有趣，因为 ERCOT 同样发布需求预测，而且预测数字惊人。2025 年 4 月发布的[《2025 年长期负荷预测》](https://www.ercot.com/files/docs/2025/04/29/Long-term-Load-Forecast-RPG.pdf)将数据中心认定为增量峰值增长的最大单一驱动力。部分基于得州输电服务商的宣誓陈述，ERCOT 预计到 2030 年潜在数据中心负荷将达 77.9 GW——是前一年展望中 29.6 GW 的两倍还多，堪称史无前例的单年上修。

![](https://substack-post-media.s3.amazonaws.com/public/images/11a823b3-3e3f-4f95-9b4c-6a9ce585f4a9_1800x961.png)
*来源：ERCOT*

如果按字面意思理解，这一预测意味着在当前负荷曲线之上，再叠加一整个新的 ERCOT 系统量级的结构性需求冲击。而现实中，没有人相信这些数字，市场也基本对它们置之不理。

连 ERCOT 自己也认识到预测并未兑现，于是改弦更张。在 2025 年 5 月的《容量、需求与备用》报告中，它们有意进行了打折处理：普通申请按 49.8% 折算，高管宣誓的申请按 55.4% 折算，所有投运日期一律推后 180 天。ERCOT 的内部电网分析师实际上是在说：在铲子真正动起来之前，它们不会按开发商宣称的 100% 去做规划。

![](https://substack-post-media.s3.amazonaws.com/public/images/1e31a199-bfe3-45c6-9d33-2a6a48cc4fcb_1800x961.png)
*来源：ERCOT*

但关键区别在于：ERCOT 的负荷预测和并网队列约束并不会直接驱动电价。PJM 的预测驱动一条模拟的供需曲线，进而直接决定系统容量的价格边界。ERCOT 则把需求预测用于指导系统规划、输电扩建和资源充裕度研究——而不是作为直接的定价输入。ERCOT 的方法内嵌了一种怀疑精神，在投机性需求影响市场结果之前就把它过滤掉。

### 数据中心负荷更多，稀缺性反而更低

物理系统证实 ERCOT 的方法是行之有效的。电网已经在 2024 年夏季经历了超过 90 GW 的破纪录峰值，并在 2025 年 5 月创下 78.4 GW 的春季纪录。得州超大规模云厂商的需求增长已然巨大，但此后再未发生过局部限电（brownout）。

能源交易员看到的价格同样没有一飞冲天。远期价格——尤其是 2026、2028 和 2030 年合约——过去一年上涨了 11-17%，涨幅可观、与 PJM 大致相仿，但绝无容量价格 9 倍飙升那样的情形。

![](https://substack-post-media.s3.amazonaws.com/public/images/30a916ae-8f6f-462a-a184-7622bd295775_1808x1110.png)
*来源：Bloomberg*

[《2024 年 ORDC 双年度报告》](https://www.ercot.com/files/docs/2024/10/31/2024-biennial-ercot-report-on-the-ordc-20241031.pdf)解释说，可用的在线备用比以往周期更多，使系统得以平稳、从容地增长。太阳能、风能、电池和化石燃料调峰机组都以足够的规模并网，为系统提供了缓冲。可以量化的效果是：触发稀缺性定价的小时数和稀缺性定价总支出较往年双双下降。尽管用电需求增长，ERCOT 区域内的能源如今反而不那么稀缺了。要把系统推入真正的稀缺状态，所需的增量需求吉瓦数已比两年前更多。在公开表态中，ERCOT 对数据中心增长的担忧并不包括资源稀缺方面的忧虑。

![](https://substack-post-media.s3.amazonaws.com/public/images/aeb83ece-fc7c-4534-b358-0b494e4cacef_1740x1100.png)
*来源：ERCOT、SemiAnalysis 标注*

远期批发价格曲线告诉我们，交易员相信 ERCOT 能够消化这一增长。他们押注于供给扩张、备用改善，以及 [SB 6 限电](https://www.bakerbotts.com/thought-leadership/publications/2025/july/texas-senate-bill-6-understanding-the-impacts-to-large-loads-and-co-located-generation)授权能在长期缓解稀缺。这种怀疑态度与 ERCOT 对开发商申报材料自行打折的做法互为镜像。系统运营机构在预测中对数据中心的原始宣称打折；市场则在远期价格中对它们打折。

ERCOT 的行动也快得多：它相对 PJM 的一大关键优势，是只覆盖一个州、不受 FERC 管辖。而 PJM 则必须同时应付 FERC 和 13 个州。

## 冬季风暴 Fern：为可靠性买单 vs. 真正交付可靠性

冬季风暴 Fern（2026 年 1 月 24-27 日）是对 PJM 创纪录的 2025/26 容量价格和 ERCOT 市场纪律的第一次真实压力测试。

### ERCOT：没有危机

ERCOT 的电网挺过了 1 月的严寒。电网运营机构发布的「天气观察（Weather Watch）」始终停留在预防层面。[需求低于预测，未触发任何应急程序，系统保持了充足的备用。](https://www.bakerbotts.com/thought-leadership/publications/2025/july/texas-senate-bill-6-understanding-the-impacts-to-large-loads-and-co-located-generation)除了冬季风暴中常见的杆线和线路停电之外，得州电网没有出现任何问题。

这证明得州从灾难性的冬季风暴 Uri 中吸取了教训。Uri 之后的改革——天然气生产与发电设施的强制性冬季化改造、天然气与电力系统之间协调的改进、运营规程的强化——在真实条件下被证明是有效的。

ERCOT 的实时价格峰值约为 $300/MWh。

### PJM：$270/MW-day 买来一场 21 GW 的失灵

PJM 的电网表现糟糕得多。尽管容量市场已经通过创纪录的出清价格把数据中心负荷风险计入了价格，电网仍因设备冻结和燃料输送故障损失了约 21 GW 的发电容量——占拍卖中出清机组的 15%。

[美国能源部被迫根据《联邦电力法》第 202(c) 条发布紧急命令](https://www.utilitydive.com/news/doe-issues-emergency-orders-for-texas-new-england-and-pjm-markets-Fern-reliability/810464/)，授权电网运营机构绕开环境限制，调用全美数据中心和工业设施约 35 GW 的备用发电容量——这些容量本无资格参与 BRA。

实时电价反映了运营压力。PJM 全系统平均达到 $700/MWh，数据中心密集的弗吉尼亚 Dominion 区域更是飙升至 $1,800/MWh。

这也暴露了 PJM 容量市场的另一个失败之处。在 PJM，电厂无论如何都能拿到钱，哪怕在最需要的时候掉链子。在 ERCOT，电厂只有在备用裕度紧张、真正发电并送入电网时才能获得可观收入——因此它们有充分的动力让设备在寒冷天气下保持运转。

### 风暴揭示了什么

这场风暴暴露了 PJM 容量市场的根本性脱节。高容量价格是由数据中心负荷增长预测驱动的——这个风险确实成真了。但实际的运营故障来自冬季化改造不足和燃料基础设施的薄弱环节，而容量市场并没有激励这些问题得到解决。PJM 9.3 倍的容量价格上涨本应买到可靠性。但它没有。

ERCOT 并未把投机性的数据中心增长计入高企的容量费用，但其强制性的运营改革在考验来临时交付了电网稳定。成本更低，结果更好。

能源部在风暴期间识别出的 35 GW 数据中心备用发电能力，还证明了一件重要的事情：只要整合得当，数据中心可以充当电网资源。虽然 ERCOT 应对这场风暴并未需要启用这些备用资源，但它们的存在本身就是一个可观的可靠性缓冲——而这两个市场都从未将其系统性地计入前瞻规划。这是一类尚未被开发的资产，监管机构和投资者都应予以关注。

## 接下来会怎样

### 政治余波已经到来

PJM 由模拟驱动的定价，已经让容量市场成为政治靶子。2025/26 拍卖价格飙升后，宾夕法尼亚州州长 Josh Shapiro 向 FERC 提出申诉，指控 BRA 规则有失公正。FERC 批准的和解协议设定了更紧的价格上限——一个仅覆盖 2026/27 和 2027/28 交付年的临时封顶。这就是 2027/28 拍卖出清价与上一年几乎相同的原因。

但价格上限并没有修复底层机制。VRR 曲线、需求预测方法论，一切都原封未动。这块「创可贴」还带来了新问题：备用裕度已低于 PJM 自身的可靠性目标。电网仍在运转并保有备用裕度，但裕度正在收窄，而容量市场吸引新发电投资的能力，如今已被未来价格上限的监管不确定性所削弱。

各方曾试图改变 PJM 的结构，但监管和各方考量极其激烈。PJM 试图引入非容量支撑负荷（Non-Capacity-Backed Load，NCBL）规则——本质上是对未自行锁定容量的大型负荷进行削减的机制——遭到利益相关方的一致反对而撤回。[FERC 关于大型负荷和数据中心的拟议规则制定预先通知（ANOPR）](https://www.mayerbrown.com/en/insights/publications/2025/11/ferc-large-load-interconnection-preliminary-rulemaking-key-takeaways-for-data-center-developers-other-large-load-projects-and-investors)表明联邦审查正在加强，但总而言之，FERC 的任何规则制定都需要数年时间，并将面临法律挑战。

### 监管不对称

ERCOT 能动作更快，因为它的监管结构更简单。ERCOT 的服务区域完全位于得州境内，由得州立法机构和公用事业委员会直接监管。SB 6 在一个立法会期内就完成通过、签署并投入实施。而 PJM 的服务区域横跨 13 个州和哥伦比亚特区，其监管授权来自 FERC。要复制 SB 6 那样的限电授权，需要 FERC 批准，甚至可能需要联邦立法——耗时以年计而非以月计。

这种结构性不对称是持久存在、且可用于投资决策的。ERCOT 调整市场规则和运营要求的速度，将持续快于 PJM 改革其容量机制的速度。对于要做 10 年期选址决策的超大规模云厂商而言，这种监管敏捷度与当前的价格差异同等重要。

## 赢家与输家，以及正在转移的市场瓶颈

这就引出下一节：赢家与输家。PJM 预测的一个关键问题，是它们缺乏洞察全局的能力。下面我们将讨论正在转移的约束，及其对以下各方意味着什么：GEV、CAT 和 Bloom Energy 等现场天然气方案的设备商，Vertiv 等设备供应商，Vistra、Talen 等 IPP，以及数据中心开发商和加密矿企。

付费订阅用户可以在免责声明下方继续向下滚动，阅读报告的其余部分。

## 免责声明

## SemiAnalysis 免责声明

> **分析师认证与研究独立性。**
>
> 本报告署名的每位分析师在此证明：本报告中表达的所有观点，均准确反映我们对任何及所有相关证券或发行人的个人观点；且我们的薪酬中没有任何部分曾经、正在或将会与本报告中的具体建议或观点直接或间接相关。
>
> SemiAnalysis LLC（以下简称「公司」）是一家独立的股票研究提供商。公司不是 FINRA 或 SIPC 的成员，也不是注册的经纪交易商或投资顾问。SemiAnalysis 没有任何其他与独立研究提供业务相冲突的受监管或不受监管的业务活动。
>
> **研究与信息的局限性。**
>
> 本报告仅面向 SemiAnalysis LLC 的合格机构或专业客户分发。本报告内容代表其作者的观点、意见和分析。本文所载信息不构成财务、法律、税务或任何其他建议。本文所呈现的所有第三方数据均来自被认为可靠的公开来源；但公司不对该等信息的准确性或完整性作任何明示或默示的保证。在任何情况下，公司均不对该等材料的正确性或更新负责，亦不对因使用这些数据而造成的任何损害或错失的机会承担责任。
>
> 本报告或公司任何分发材料中的内容，均不得被解释为任何出售证券或投资的要约，或征求购买任何证券或投资之要约的行为。收到的任何研究或其他材料均不得被解释为个性化投资建议。投资决策应作为整体投资组合策略的一部分作出，在做出任何投资决策之前，你应咨询专业的财务顾问以及法律和税务顾问。对于基于从 SemiAnalysis LLC 获得的信息或研究而做出的投资决策所引起的任何直接或间接、附带或后果性损失或损害（包括利润、收入或商誉损失），SemiAnalysis LLC 概不负责。
>
> **严禁复制与分发。**
>
> 本报告的任何用户均不得复制、修改、拷贝、分发、出售、转售、传播、转让、许可、让与或发布本报告本身或其中包含的任何信息。尽管有前述规定，有权使用工作模型的客户可以更改或修改其中包含的信息，前提是仅供该客户自用。本报告无意以任何目的提供或分发——若该目的会被任何地方、州、国家或国际法律法规认定为非法或另行禁止，或会使公司在该司法管辖区接受任何形式的注册或监管。
>
> **版权、商标、知识产权。**
>
> SemiAnalysis LLC 及本报告中包含的任何标识或商标均为专有材料。未经 SemiAnalysis LLC 明确书面同意，严禁使用此类名称、标识和商标。除非另有说明，本报告页面或界面及其所载信息和材料的版权均为 SemiAnalysis LLC 拥有的专有材料。未经授权使用本报告中的任何材料，可能违反大量制定法、法规和法律，包括但不限于版权、商标、商业秘密或专利法。

**ADMIS 免责声明**

本文所载的数据、评论和/或观点仅由 ADM Investor Services, Inc.（"ADMIS"）出于信息目的提供，绝不应被解读为 Archer Daniels Midland 公司的数据、评论或观点。本报告包含截至发布之日被认为可靠和准确的信息来源，但未经过独立核实，我们不保证其准确性或完整性。所表达的观点如有变更，恕不另行通知。本报告不应被理解为请求进行任何涉及期货合约和/或相关商品期权买卖的交易。交易期货合约或商品期权的损失风险可能很大，投资者应结合自身财务状况仔细考虑此类投资的固有风险。未经 ADMIS 明确书面同意，严禁复制或转发本报告。再次强调，本文所载的数据、评论和/或观点由 ADMIS 提供，而非 Archer Daniels Midland 公司。版权所有 (c) ADM Investor Services, Inc.

来源与参考文献：

1. Semianalysis 数据中心行业模型

2. <https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2025-2026/2025-2026-base-residual-auction-report.pdf>

3. <https://www.pjm.com/-/media/DotCom/markets-ops/rpm/rpm-auction-info/2026-2027/2026-2027-bra-report.pdf>

4. <https://insidelines.pjm.com/maintaining-grid-reliability-through-highest-peaks-in-a-decade/>

5. <https://www.monitoringanalytics.com/reports/reports/2025/IMM_Analysis_of_the_20252026_RPM_Base_Residual_Auction_Part_G_20250603_Revised.pdf>

6. <https://www.pa.gov/governor/newsroom/2025-press-releases/gov-shapiro-s-legal-action-again-averts-historic-price-spike-acr>

7. <https://www.ercot.com/files/docs/2025/04/29/Long-term-Load-Forecast-RPG.pdf>

8. <https://www.ercot.com/files/docs/2025/05/15/CapacityDemandandReservesReport_May2025.pdf>

9. <https://www.ercot.com/files/docs/2025/06/17/ERCOT-Monthly-Operational-Overview-May-2025.pdf>

10. <https://www.ercot.com/files/docs/2024/10/31/2024-biennial-ercot-report-on-the-ordc-20241031.pdf>

11. <https://www.bakerbotts.com/thought-leadership/publications/2025/july/texas-senate-bill-6-understanding-the-impacts-to-large-loads-and-co-located-generation>

12. <https://www.spglobal.com/commodity-insights/en/news-research/latest-news/electric-power/042325-outlook-2025-texas-summer-power-prices-may-top-2024-levels-on-weather-strong-gas>

13. <https://www.rtoinsider.com/121911-pjm-capacity-auction-clears-max-price-falls-short-reliability-requirement/>

14. <https://elibrary.ferc.gov/eLibrary/docinfo?accession_number=20241230-5225>

15. <https://www.reuters.com/business/energy/power-prices-surge-winter-storm-spikes-demand-us-data-center-alley-2026-01-25/>

16. <https://www.usnews.com/news/top-news/articles/2026-01-25/power-prices-surge-as-winter-storm-spikes-demand-in-us-data-center-alley>

17. <https://www.ercot.com/files/docs/2026/01/28/ERCOT-Post-Event-Report-Winter-Storm-Fern.pdf>

18. <https://www.utilitydive.com/news/doe-issues-emergency-orders-for-texas-new-england-and-pjm-markets-Fern-reliability/810464/>

19. <https://www.publicpower.org/periodical/article/department-energy-asks-grid-operators-be-prepared-make-backup-generation-resources-available-needed>
