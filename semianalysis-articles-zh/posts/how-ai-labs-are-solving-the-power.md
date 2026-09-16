---
title: "AI 实验室如何破解电力危机：现场燃气发电深度解析"
title_en: "How AI Labs Are Solving the Power Crisis: The Onsite Gas Deep Dive"
subtitle: "自备发电（BYOG）、告别电网、燃气轮机 vs. 往复式发动机 vs. 燃料电池、为什么不多建 CCGT？、现场发电 TCO"
date: 2025-12-30
source: https://newsletter.semianalysis.com/p/how-ai-labs-are-solving-the-power
crawled: 2026-09-15
authors: ["Ajey Pandey", "Jeremie Eliahou Ontiveros", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AI 实验室如何破解电力危机：现场燃气发电深度解析

> 原文：[How AI Labs Are Solving the Power Crisis: The Onsite Gas Deep Dive](https://newsletter.semianalysis.com/p/how-ai-labs-are-solving-the-power) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**自备发电（Bring Your Own Generation）、告别电网、燃气轮机 vs. 往复式发动机 vs. 燃料电池、为什么不多建 CCGT？、现场发电 TCO**

# 电网已经老朽不堪

近两年前，我们率先预测了一场正在逼近的电力紧缺。在报告 **[AI 数据中心能源困境——AI 数据中心空间争夺战](https://newsletter.semianalysis.com/p/ai-datacenter-energy-dilemma-race)** 中，我们预测美国 AI 电力需求将从 2023 年的约 3GW 增长到 2026 年的 28GW 以上——这一压力将压垮美国的供应链。我们的预测被证明非常准确。

下面的图表说明了这一切：仅得克萨斯州一地，**每月**都有**数十吉瓦的数据中心负荷申请**涌入。而过去 12 个月里，获批的容量仅勉强超过 1 吉瓦。电网容量已经卖光了。

![](https://substack-post-media.s3.amazonaws.com/public/images/e566cdd5-3ecc-4023-8fd5-a4c8f47f777d_2930x1507.png)
*来源：ERCOT 2024 大型可调节负荷工作组（LFLTF）*

然而，AI 基础设施等不起电网动辄数年的输电升级。一个 AI 云每吉瓦每年可以创造 100-120 亿美元的收入。让一座 400 MW 的数据中心哪怕提前六个月上线，就价值数十亿美元。经济上的需要让电网过载这类问题相形见绌。行业已经在寻找新的解决方案。

十八个月前，埃隆·马斯克（Elon Musk）用四个月建成一个 10 万 GPU 集群，震惊了整个数据中心行业。多项创新成就了这一惊人壮举，但能源策略最为亮眼。xAI 完全绕开电网，使用车载燃气轮机和发动机在现场发电。如下图所示，xAI 已在其数据中心附近部署了超过 500MW 的燃气轮机。在一个 [AI 实验室竞相抢建首个吉瓦级数据中心](https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter)的世界里，**速度就是护城河**。

![](https://substack-post-media.s3.amazonaws.com/public/images/b467823e-102f-47aa-97ec-e1d399f8f77b_1024x555.jpeg)
*来源：SemiAnalysis 数据中心行业模型*

超大规模云厂商和 AI 实验室正一个接一个地效仿，暂时抛开电网去建设自己的现场发电厂。正如我们几个月前在[数据中心模型](https://www.semianalysis.com/p/datacenter-model)中讨论的，2025 年 10 月，OpenAI 与 Oracle 下达了有史以来最大的现场燃气发电订单——一座位于得克萨斯州的 2.3GW 电厂。现场燃气发电市场正在进入年增长率三位数的时代。

受益者远不止那些老牌玩家。是的，GE Vernova 和西门子能源（Siemens Energy）的股价已经飙升。但我们正在见证一波前所未有的新进入者，例如：

- **斗山 Enerbility（Doosan Enerbility）**，这家韩国工业巨头把 H 级燃气轮机的推出时机拿捏得恰到好处。它已经[拿下了一份 1.9GW 订单，服务于马斯克的 xAI——几周前我们已向数据中心行业模型订阅用户独家拆解了这笔交易](https://semianalysis.com/institutional/xais-1-9gw-gas-turbine-order-with-doosan-colossus-2-progress/)。
- **瓦锡兰（Wärtsilä）**，历史上是一家船用发动机制造商，意识到为邮轮提供动力的同款发动机也可以为大型 AI 集群供电。它已经签署了 800MW 的美国数据中心合同。
- **Boom Supersonic**——没错，就是那家超音速客机公司——宣布与 Crusoe 签订 **1.2 GW 燃气轮机合同**，把数据中心发电的利润当作其 Mach 2 客机的又一轮融资。

为了解各供应商的增长与市场份额，我们在[数据中心模型](https://semianalysis.com/datacenter-industry-model/)中建立了一套逐站点跟踪现场燃气发电部署的数据库。结果令我们吃惊：**仅在美国，已有 12 家不同供应商各自锁定超过 400 MW 的数据中心现场燃气发电订单。**

![](https://substack-post-media.s3.amazonaws.com/public/images/3aea9513-1713-449a-827e-18713518ede2_3731x2214.png)
*来源：SemiAnalysis 数据中心行业模型*

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

然而，现场发电也带来一整套自身的挑战。如下文详述，电力成本往往比电网供电贵（贵得多）。许可审批可能是一个漫长而复杂的过程。而且它已经造成了一些数据中心延期——最引人注目的是 Oracle/Stargate 的一座吉瓦级设施，我们的[数据中心行业模型](https://semianalysis.com/datacenter-industry-model/)通过分析整个许可流程，比彭博社的头条新闻提前三周预测到了这一结果。

同样，像 xAI 这样的聪明公司已经找到了对策。马斯克的 AI 实验室甚至开创了一种新的选址流程——在两个州的边界上建设，以最大化尽早拿到许可的概率！田纳西州没能按时交付，密西西比州则欣然让马斯克建起了一座吉瓦级电厂。

![](https://substack-post-media.s3.amazonaws.com/public/images/a08393e1-6f99-44dc-a37f-b7769ba26623_852x1362.png)
*来源：SemiAnalysis 数据中心行业模型*

本报告是对「自备发电」（Bring Your Own Generation, BYOG）的深度解析。我们先讲电网为何跟不上，然后对数据中心可用的每一种发电技术做技术拆解——GE Vernova 的航改燃机、西门子的工业燃机、Jenbacher 的高速发动机、瓦锡兰的中速发动机、Bloom Energy 的燃料电池等等。

接着我们考察部署形态与运营挑战：完全孤岛运行的数据中心、燃气 + 电池混合、能源即服务（Energy-as-a-Service）模式，以及决定哪种方案胜出的经济学。付费墙之后，我们分享对厂商定位以及现场发电未来的看法。

## AI 时代，电网已死？

在深入解决方案之前，我们需要理解电网为什么会失灵。公平地说，美国的电力系统迄今为止是 AI 基础设施的首要支撑。除马斯克之外，当今所有主要的 GPU 与 XPU 集群都靠电网电力运行。我们在此前多篇 SemiAnalysis 深度解析中覆盖过其中许多：

- [微软 AI 战略解构](https://newsletter.semianalysis.com/p/microsofts-ai-strategy-deconstructed)展示了 OpenAI 在威斯康星、佐治亚和亚利桑那的大规模并网设施。
- 我们的[多数据中心训练报告](https://www.semianalysis.com/p/multi-datacenter-training-openais)，深挖了谷歌在俄亥俄以及艾奥瓦/内布拉斯加的大规模电网供电集群，以及 OpenAI 与 Oracle、Crusoe 和 Lancium 在得州 Abilene 的吉瓦级集群。
- 我们的 [Meta 超级智能文章](https://newsletter.semianalysis.com/p/meta-superintelligence-leadership-compute-talent-and-data)铺陈了他们宏大的 AI 计划，其中包含一些现场燃气发电，但仍主要由 AEP 在俄亥俄的系统和 Entergy 在路易斯安那的系统供电。
- 我们的[亚马逊 AI 复兴](https://newsletter.semianalysis.com/p/amazons-ai-resurgence-aws-anthropics-multi-gigawatt-trainium-expansion)论点，讨论了 AWS 为 Anthropic 建设的大规模 Trainium 集群，同样接入 AEP 和 Entergy 的基础设施。

这些洞见出现在我们的[数据中心行业模型](https://semianalysis.com/datacenter-industry-model/)中，比官方宣布早了数月乃至数年。我们的模型还在跟踪数十个在建、将于 2026 年及以后交付的大规模集群——包括它们的确切启动日期、满载容量、终端用户和能源策略。

但我们已经到了拐点。2024-25 年上线的大型数据中心是在 2022-23 年、淘金潮之前锁定电力的。自那以后，争夺从未停歇。我们估计已有**约 1 太瓦（terawatt）的负荷申请**提交给了美国的公用事业公司和电网运营商。

![](https://substack-post-media.s3.amazonaws.com/public/images/e8b85901-01b1-4e0f-9ce0-ff4cc0b718bd_2521x1600.png)
*来源：SemiAnalysis 数据中心行业模型*

结果是字面意义上的「大堵车」（gridlock）。正如我们在 **[吉瓦级 AI 训练负荷波动与电网停电风险](https://newsletter.semianalysis.com/p/ai-training-load-fluctuations-at-gigawatt-scale-risk-of-power-grid-blackout)** 中解释的，电网的慢是设计使然：

1. **实时平衡**：电力供需必须每一秒都近乎完美地匹配。一旦失配，数百万用户就有停电风险——2025 年 4 月的伊比利亚半岛大停电便是一例。
2. **系统研究**：每一个大型新负荷（数据中心）或新电源（电厂）都会触发深度工程研究，以确保它不会破坏电网稳定。而且在一些地方，电网拓扑变化太快，负荷研究还没做完就已过时。

![](https://substack-post-media.s3.amazonaws.com/public/images/85df89ad-eea6-4a86-8354-803d96c25129_624x355.png)
*来源：2025 ITP 项目组合*

当数百个开发商同时提交并网申请时，系统就会卡死。这变成了一场囚徒困境：

- 如果所有人协调行动，电网本可以更快处理更多申请。

  - FERC 第 2023 号令（FERC Order 2023）已推动电网运营商为此采用**集群研究（cluster studies）**，但这些改革直到 2025 年才固化下来。
- 实际上，「淘金潮」式的行为意味着开发商同时向不同公用事业公司提交大量投机性申请

  - 例如截至 2024 年中，AEP 俄亥俄收到的负荷申请达 **35 GW**——其中 68% 甚至连土地控制权都没有
- 投机性申请堵住了所有人的队列，反过来又刺激其他地方出现更多投机申请
- 恶性循环不断加速

![](https://substack-post-media.s3.amazonaws.com/public/images/df329af2-9a83-430c-a068-680d2eaaa3e9_1204x652.png)
*来源：PJM 负荷分析小组委员会*

供给侧同样受限。对大多数发电类型而言，从并网申请到商业运行的时间线如今拉长到了**五年**。

![](https://substack-post-media.s3.amazonaws.com/public/images/dc289e35-2585-43af-a588-90b1a61674bd_1248x540.png)
*来源：Lawrence Berkeley National Lab*

AI 基础设施开发商等不起五年。很多情况下，他们连六个月都等不起，因为*多等六个月就意味着数十亿美元的机会损失。*

### **BYOG 登场——自备发电（Bring Your Own Generation）**

BYOG 的核心价值主张很简单：**不用等电网，先干起来。**数据中心可以靠本地发电无限期运行，等电网供电最终到位后，再把这批设备转为备用电源。

这正是 xAI 的策略。他们用移动式燃气轮机建成了 Colossus，用几个月而非几年让设施上线。现在所有人都在照搬这套打法。

让我们看看怎么做。

# 如何自备发电

## 旧世界 vs 新世界

BYOG 需要彻底重新思考电厂的建设方式。传统上，我们通过大型集中式吉瓦级基荷发电机供电——辅以较小的调峰电厂来应对全网负荷尖峰。联合循环模式下的重型燃气轮机是现代最常见的配置，其无可匹敌的燃料效率（>60%）构成了现代文明的支柱。但它的主要问题是部署速度：

- 大型燃气轮机通常有多年交期，而当前交期正处于历史最高点。
- 到货之后，一座大型联合循环电厂的建设与调试还需要 **~2 年——在 AI 时代这就是永恒。**

![](https://substack-post-media.s3.amazonaws.com/public/images/b33e8f47-7c0c-4644-ae01-0fd20dd53e71_1300x930.png)
*一台联合循环燃气轮机（CCGT）。来源：Knoxville News Sentinel*

AI 数据中心的「BYOG」电厂改写了剧本，而 xAI 为全行业带路。为了更快部署，马斯克的 AI 实验室采用了卡特彼勒（CAT）子公司 Solar Turbines 的小型模块化 16MW 燃气轮机。这些轮机小到可以用标准长途卡车运输，几周内即可完成部署。马斯克甚至没有买下它们——而是向 Solaris Energy Infrastructure 租赁，以绕过设备交期。他还借助 VoltaGrid 的车载移动燃气发动机机队进一步提速！

![](https://substack-post-media.s3.amazonaws.com/public/images/7270f9f8-addf-403b-b3dc-77a98cd5665b_1430x908.png)
*Solar SMT130（额定 16 MW）。卡车用作比例参照。来源：CAT（Solar Turbines）*
![](https://substack-post-media.s3.amazonaws.com/public/images/c9ed803a-d129-4fe1-920b-6a13a9e5a274_1600x900.png)
*来源：Tom's Hardware*

其他超大规模厂商迅速跟进。Meta 与 Williams 在俄亥俄的部署很有代表性——其电厂由五种不同类型的轮机与发动机构成，设计模式显然是「能按时拿到什么就部署什么！」

![](https://substack-post-media.s3.amazonaws.com/public/images/c0c11789-f392-49d6-8874-060fa89a919d_624x428.png)
*Socrates South 卫星影像（2025 年 11 月 11 日）*

现在让我们深入探讨数据中心运营方可用的各类设备。

## 设备全景概览

在数据中心开发商可用的燃气发电机中，有三大类别：

1. 燃气轮机（GT）——低温、爬坡慢的**工业燃气轮机（IGT）**；高温、爬坡快的**航改燃气轮机（Aero）**；以及非常大的**重型燃气轮机**。
2. 往复式内燃机（RICE）——包括较小的 3-7 MW **高速发动机**和较大的 10-20 MW **中速发动机**。有时简称「recips」。
3. 固体氧化物燃料电池（SOFC）——目前的主要可选项来自 Bloom Energy。

还有其他现场发电选项，例如与现有核电厂共址、在现场建小型模块化反应堆（SMR）、地热等等，但本报告不予讨论。这些方案大多无法在未来约 3 年内带来净新增发电能力。

![](https://substack-post-media.s3.amazonaws.com/public/images/1dc2e3bb-1ade-48e5-9f6f-0d74e22d79b3_705x238.png)

要理解哪些方案最适合哪些用例，需要深挖核心权衡。我们认为以下几点最相关：

- **成本：**通常以 $/kW 列示。这些成本估算差异极大，且在每个发电机类别中都在持续上涨。注意维护费用同样相关：某些系统使用寿命更短，即年维护成本更高。
- **交期（发货与安装）：**通常以月或年计。随着需求增长超过供给，各类发电机的交期都在拉长。

  - 注意，发电机可得性之外的其他因素也会影响通电时间。最突出的是现场发电的空气许可，即便在得州这类审批较快的州也可能要一年以上。
  - 此外，安装时间在不同系统之间差异巨大。有些从设备到场到发电只需几周，例如小型车载轮机或发动机，以及燃料电池。大型 CCGT 的组装则可能超过 24 个月。
- **冗余与可用率**：发电机的预期可用性，以全年正常运行时间百分比或「几个 9」表示。美国电网过去十年的平均可用率为 99.93%（3 个 9），部分地区更高。对于现场电厂，可以通过增加热备与冷备、或额外的备用电源来管理冗余。单台轮机越大，管理备件与备用电源就越困难。
- **爬坡速率：**以冷启动到最大出力之间的分钟数衡量。低于 10 分钟的爬坡速率使发电机有资格担任电网的备用电源或应急备电。爬坡慢则意味着该机组主要用于基荷供电。
- **土地占用：**以 MW/英亩衡量。在空间受限地区这更重要。小型发电系统的用水量微不足道，即使成规模也一样。但特大型轮机的冷却确实需要大量用水。
- **热耗率与燃料效率：**以每 kWh 天然气 BTU 数衡量。热耗率越高效率越低——投入更多燃料，产出同样的电，留下更多废弃物。铭牌热耗率假设「峰值」运行工况，通常为最大出力。低于 50% 出力时效率大幅下降。

  - 这些现场燃气系统中有许多可以配置为**热电联产（CHP）**系统。对数据中心而言，这需要把燃气发电机的废热用于**吸收式制冷**系统，从而减少数据中心制冷的用电。

现实中我们观察到：谁的订单簿有空位、谁能给出靠谱的时间表，谁就往往能赢下合同，其他大部分规格反而不重要！

话虽如此，现在让我们深入剖析不同类型的燃气电厂。

#### 航改燃机与 IGT——对数据中心极具吸引力

燃气轮机按布雷顿循环（Brayton Cycle）运行：压缩空气，在其中燃烧燃料，再让高温燃气通过涡轮。轮机以**进气温度**区分高低。温度越低，安装成本越低、维护成本越低、峰值效率越低、爬坡也越慢。

![](https://substack-post-media.s3.amazonaws.com/public/images/fbdea229-e3c1-46f2-bc1a-d4790ea57eee_1129x594.png)

航改燃气轮机说白了就是固定在地上的喷气发动机。GE Vernova 的 aero 源自 GE 的喷气发动机；三菱电力（Mitsubishi Power）的源自普惠（Pratt & Whitney）；西门子能源的源自罗尔斯·罗伊斯（Rolls-Royce）。由于喷气发动机本来就是为在紧凑、适航的包体内输出巨大功率而设计的，它们相对容易改造为固定式发电：延长涡轮轴，在末端装上发电机线圈，加上进气与排气消音器，再从储罐或管道供给燃料即可。这也是 Boom Supersonic 能如此迅速转型航改燃机的原因之一：他们的工程与制造大部分可以直接沿用。

![](https://substack-post-media.s3.amazonaws.com/public/images/7443f969-4531-4e17-b8e3-f8229eed9f78_624x495.png)
*三菱重工 FT8 MOBILEPAC（额定 30 MW）。来源：Mitsubishi Heavy Industries*

下面我们展示 Martin Drake 电厂的画面，配有 6 台 GE Vernova LM2500XPRESS 机组。这就是电力公司部署航改燃机的方式——作为应对电网突发供电短缺的「调峰电厂」。

![](https://substack-post-media.s3.amazonaws.com/public/images/37829f1d-54b2-4235-a7e2-0e31424b03bd_796x676.png)

航改燃机的核心制造商与重型燃机类似：GE Vernova、三菱电力和西门子能源主导市场，同时销售 aero 和温度较低的**工业燃气轮机（IGT）**。此外，卡特彼勒也以 Solar 品牌生产 IGT，Everllence（原 MAN Energy Systems）亦然。

两种 GE Vernova 设计主导着航改燃机市场：

- **LM2500**——约 34 MW，为快速部署优化，尤其是 LM2500XPRESS 形态。
- **LM6000**——约 57 MW，现有快速部署的 LM6000VELOX 配置。

Aero 的燃料效率尚可，但在空间和重量方面极其高效。它们能塞进很小的占地，某些配置下可以用两辆平板拖车运输。简单循环 aero 通常以 30-60 MW 的包体交付，冷启动到满出力只需 5-10 分钟。但在低于满稳定负荷时效率会受损。Aero 也可以配置为小型联合循环电厂：

- 1x1（一台燃气轮机带动一台汽轮机），或
- 2x1（两台燃气轮机带动一台汽轮机）。

这些联合循环配置以爬坡速度为代价换来更高效率和更大出力，启动时间延长至 30-60 分钟。

按当前价格，aero 的全包资本开支为 **$1,700-2,000/kW**，且根据近期订单，交期为 **18-36 个月**且不断上升。较小的轮机交期可短至 12 个月，较大的 aero（约 50 MW）可达 36 个月。这些系统安装很快（通常 2-4 周），但工厂订单已排得满满当当。一种变通办法是车载轮机，有货时可租赁并快速部署。xAI 用的正是这一策略，与 Solaris Energy Infrastructure 合作，缩短了 Colossus 1 和 2 的通电时间。

#### 工业燃气轮机（IGT）

工业燃气轮机与 aero 的工作循环相同，共享紧凑占地、模块化、交期相对较快等优点。但它们是从零开始为固定式用途设计的，而非改装自航空发动机。它们通常在更低的进气温度下运行，采用更简单的设计，以效率和爬坡速度为代价换取更低的运维成本。

![](https://substack-post-media.s3.amazonaws.com/public/images/573a0140-75ab-47ca-96c2-51534f6adc44_624x396.png)
*SMT130 IGT 剖视图。来源：Solar Turbines*

简单循环 IGT 的功率大致在 5-50 MW 之间，冷启动到满出力约 20 分钟。这使得它们单凭自己太慢，无法在没有电池或柴油机组辅助的情况下充当调峰电厂或应急备电。与 aero 一样，IGT 可以升级为联合循环配置，在提升效率的同时进一步拖慢爬坡速率。

最常见的专用工业燃气轮机是**西门子能源 SGT-800** 和 **Solar Titan 系列**。不过，像 **GE Vernova 6B** 这样较小的重型燃机有时也会承担类似用途。

![](https://substack-post-media.s3.amazonaws.com/public/images/7270f9f8-addf-403b-b3dc-77a98cd5665b_1430x908.png)
*Solar SMT130（额定 60 MW）。卡车用作比例参照。来源：CAT（Solar Turbines）*

按当前价格，IGT 的全包资本开支为 **$1,500-1,800/kW**，交期约 **12-36 个月**，与 aero 类似。不过，采购二手或翻新 IGT 可以把交期缩短到 12 个月以内，Fermi America 就是这样采购电力的。

总体而言，我们认为航改燃机和 IGT 是现场发电非常有吸引力的方案，因为：

- 它们的尺寸「刚刚好」：小到便于做冗余，又大到不必在现场摆太多机组、把维护搞复杂。
- 它们爬坡快：虽然能源效率不如其他方案，但更容易转用作备用电源。
- 它们部署快：普通卡车和施工队就能运输安装，不需要重型燃机那种疯狂的重型吊装基础设施。

我们会在报告后文讨论部署考量时再谈这些概念。Aero 和 IGT 的主要问题正日益变成交期。

燃气轮机中供应最紧张的部件是叶片和核心机（core），它们必须承受高温和高速。这些叶片使用含铼、钴、钽、钨、钇等稀土金属的单晶镍基合金。值得注意的是，钇在中国政府[出口管制](https://www.china-briefing.com/news/chinas-rare-earth-export-controls-impacts-on-businesses/)的稀土之列。而核心机所需的高温陶瓷同样供应短缺。

### 往复式发动机（RICE）

往复式发动机的工作原理与汽车发动机类似，只是规模大得多——一台 11MW 发动机可长达 45 英尺（14 米）以上。它们采用四冲程燃烧循环，并按转速划分：

- **高速发动机**——约 1,500 rpm；占地和出力更小。
- **中速发动机**——约 750 rpm；机械应力较低，维护成本通常更低。

RICE 冷启动到满出力约 10 分钟，实际与 aero 相当。这使 RICE 可以担任调峰电厂或备用发电机，从而省去柴油备电。纸面上，RICE 的 O&M 高于轮机，因为运动部件更多。实际上，它们对燃料杂质、灰尘和高环境温度的耐受性好于许多轮机，在炎热气候下的性能衰减（de-rating）也更小。

![](https://substack-post-media.s3.amazonaws.com/public/images/a722cd1c-5759-413a-952c-f31727d7fba9_946x570.png)

中速发动机的制造相当集中，主要制造商为瓦锡兰（Wärtsilä）、Bergen Engines 和 Everllence（原 MAN Energy）。

![](https://substack-post-media.s3.amazonaws.com/public/images/e36502d2-404f-4d3c-b963-b9f2410c1733_624x269.png)
*Bergen B36:45V20AG（额定 11.3 MW）。人用作比例参照。来源：Bergen Engines*

高速发动机的制造不如轮机集中。除了 Jenbacher、CAT、康明斯（Cummins）和罗罗子公司 MTU 这些显要玩家之外，还有大量制造商，因为高速燃气发动机在功能上等同于许多数据中心目前用于备用电源的柴油发动机设计。影响最深远的往复式发动机是 **Jenbacher J624**——一台 4.5MW 涡轮增压燃气发动机，可以集装箱化以便于物流。该系统是 VoltaGrid 能源集成服务的首选发电机。

![](https://substack-post-media.s3.amazonaws.com/public/images/7173c083-7b7f-4487-a7b0-8ce07e685f6e_1430x953.png)
*来源：VoltaGrid*

RICE 系统的单机发电量通常低于同级别轮机。中速发动机在 7 MW 到 20 MW 之间，较高出力靠涡轮增压实现。高速发动机更小，单机出力在 3 MW 到 5 MW 之间。但在 50%-80% 的部分负荷区间运行时，RICE 发电机比轮机更高效。

往复式发动机的工作温度远低于燃气轮机，接近 600°-700°C。这大大降低了对高性能合金的需求。只有活塞、燃烧室和涡轮增压器中的高温部件仍然需要稀有镍钴合金，其余都可用普通铸铁、钢和铝制造。总体而言，RICE 对关键矿物的依赖更低，尤其是在材料供应紧张时放宽排放控制的情况下。

按当前价格，往复式发动机的全包资本开支为 **$1,700-2,000/kW**，交期 **15-24 个月**。与轮机相比，这些系统在生产环节的延误较少；制造周期接近 12-18 个月。但中速 RICE 比轮机重得多，安装和调试可能需要长达约 10 个月。

高速发动机的部署可以快得多。例如，在 Colossus 1 的初期部署中，xAI 动用了 34 套 VoltaGrid 车载系统，搭载 Jenbacher 高速发动机。高速发动机尤其受**能源采购服务商**（下文详述）青睐，其供应广泛、单机小、通电更快。下面我们展示 VoltaGrid 在圣安东尼奥的一个 50MW 部署，包含 20 台 Jenbacher J620（单机额定 3.36kW）。

![](https://substack-post-media.s3.amazonaws.com/public/images/c54c17fc-0c9c-48e8-81bd-93ae63be79fb_1157x552.png)
*来源：VoltaGrid*

代价是规模：要用 5 MW 发动机建一个 2 GW 的现场燃气系统，你需要 **500 台机组！**这带来重大的运营影响。如果每台发动机每 2,000 小时需要一次小保养，维护人员每年就要做 2,000 多次保养，几乎每周 40 次。这些成本比轮机大修（可能需要更换整个核心机）更可预测，但会积少成多，对拥有大量小机组的机队尤其如此。空间和备件库存同样随之增长，不过小型发电机可以垂直堆叠以缓解用地——这是中速发动机做不到的技巧。

### 燃料电池与 Bloom Energy 的崛起

一个相当小众的方案正在切走越来越大的蛋糕：燃料电池。Bloom Energy 的 SOFC 燃料电池常与氢能联系在一起，但它也能使用天然气，并被定位为基荷电源。我们最早在 2024 年的[数据中心模型](https://semianalysis.com/datacenter-industry-model/)中点名 Bloom Energy 将是大赢家。自那以后，订单一飞冲天。

![](https://substack-post-media.s3.amazonaws.com/public/images/dd4de2e8-06ba-451d-8831-d1ff2f9b65f7_624x354.png)
*来源：Power Engineering*

Bloom 的「Energy Server」由多个约 1kW 的电堆组成，组装成约 65kW 的模块，再封装成一台 325kW 发电机。迄今为止，投运的最大 SOFC 电厂在数十 MW 级，主要位于美国和韩国。

![](https://substack-post-media.s3.amazonaws.com/public/images/6537eded-6e51-4f4e-846e-e4053ea6d3d1_1248x678.png)
*来源：Bloom Energy*

它们的发电方式与传统发电机截然不同：**没有燃烧过程**。氧气被电化学还原为氧离子，穿过陶瓷电解质；在燃料电池的另一端，这些离子与从甲烷天然气中剥离出来的氢原子结合。这一结合释放出水、CO2 和电力。

![](https://substack-post-media.s3.amazonaws.com/public/images/7c6fea39-20de-4b4f-ae57-fe8584103bed_726x547.png)

这一根本性差异赋予 Bloom 燃料电池一项关键优势：除 CO2 之外，它们不产生实质性的空气污染。在 EPA 层面的许可审批显著比燃烧发电机顺畅、容易。这也是我们经常在人口密集区（例如办公楼附近）看到它们的原因。

Bloom 的杀手锏是部署速度。它几乎只需要预制基座和简单的模块安装。把电气工程算进去，安装与调试也能在几周内完成，与航改燃机和高速 RICE 相当。

在速度即护城河的 AI 时代，仅此一项优势就足以让 Bloom 占据一席之地。

Bloom 的主要挑战是成本。燃料电池的效率相当好，等效热耗率为 6,000-7,000 BTU/kWh，与 CCGT 相当。但燃料电池系统的成本显著高于轮机或 RICE 系统，资本开支在 **$3,000-$4,000/kW** 之间。Bloom 不宣传爬坡速率，暗示这些机组太慢，无法充当调峰或应急备电。

维护成本历史上也显著高于其他方案。单个燃料电池电堆的寿命约 **5-6 年**，之后必须更换和翻新。这种逐电堆的更换约占服务成本的 65%，尽管具体数字被严格保密。Bloom 除了透露电堆核心使用陶瓷外，对其材料信息披露甚少，但声称其燃料电池不依赖中国或其他争议地区的关键矿物。

![](https://substack-post-media.s3.amazonaws.com/public/images/79098fb0-5f05-49f3-91af-1e4cec6c5a31_1505x788.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/09c9b4cc-eeba-44ca-a84a-15876c9eff84_1570x837.png)
*来源：Bloom Energy*

我们在付费墙后提供 Bloom 燃料电池的 TCO 估算。

# 重型燃气轮机：BYOG 的未来？

在 ChatGPT 出现之前，只有公用事业公司和独立发电商（IPP）有理由购买 250 MW 以上的燃气轮机，因为超过这一门槛的轮机对大多数工业应用来说实在太大了。如上所述，部署速度是一个问题，但我们越来越多地看到开发商先用较小的航改燃机/RICE 提供「桥接电力」，待大型 CCGT 投运后再把它们转为备用/冗余。

大型轮机按燃烧（轮机进气）温度和技术栈分档：

**E 级与 F 级**——较老、温度较低、效率较低的设计。一些 F 级机组仍在销售，通常销往发展中市场，因为它们以更低的资本开支提供不错的效率。「工业」轮机与小型 E/F 级机架之间的界限是模糊的，以下知名型号正跨越这条边界：

- GE Vernova 6B
- GE Vernova 7E
- Siemens Energy SGT6-2000E

**H 级及同级**——现代高温设计。其点火温度与现代 aero 和喷气发动机相当，但单机功率约为 10 倍。最突出的例子有：

- **GE Vernova HA** 系列（例如 HA.02）
- Siemens Energy **H/HL**
- 三菱重工 **J** 系列（例如 H510J）
- 更近一些，韩国公司**斗山 Enerbility（Doosan Enerbility）**已开始生产一款新的 H 级轮机 **DGT6**。在一个已有十年以上历史的市场里很少见到新进入者，但斗山在汽轮机制造上经验深厚，并有建造三菱设计的 F 级轮机的实绩。

如下图所示，这些系统既大且重，安装和调试过程可能需要相当长时间。

![](https://substack-post-media.s3.amazonaws.com/public/images/ea7ede7b-a314-4d9c-b59f-d7593149bf3e_740x814.png)
*位于伊利诺伊州 Grundy County 的 Three Rivers CCGT 一景。卫星影像。*

### 联合循环燃气轮机（CCGT）

联合循环燃气轮机（CCGT）利用了这样一个事实：简单循环的排气仍然很热，热到足以把水烧成蒸汽。让排气通过余热锅炉（HRSG）产生蒸汽，驱动一台独立的汽轮机和发电机，其结果是同样的燃料产出第二轮电力。把一台轮机的垃圾变成另一台轮机的宝藏，CCGT 可以比简单循环轮机高效 50-80%。

![](https://substack-post-media.s3.amazonaws.com/public/images/27759ab0-bc15-4f96-8334-804f10759535_1216x700.png)

面向大负荷最受推崇的 CCGT 是重型 CCGT，出力可达吉瓦级。不过，即使是小型航改或工业燃机也可以搭配集成汽轮机销售，在燃料输入几乎不变的情况下大幅提升出力。常见配置有：

- **1x1**——一台燃气轮机带动一台汽轮机
- **2x1**——两台燃气轮机带动一台汽轮机

理论上，更多燃气轮机可以共同带动一台汽轮机，但收益递减。CCGT 系统的主要缺点是爬坡速率：汽轮机的加入使冷启动到满出力的时间放缓到 30 分钟以上。

另一个主要缺点是交期：其安装与调试比简单循环部署更长。

# 从设备到落地：部署、挑战与经济性

了解设备全景是必要条件，但并不充分。现场燃气的真正复杂性不在于在 LM2500 和 Jenbacher J624 之间做选择——而在于如何配置、部署和运营这些系统，以满足数据中心的可用性要求。

电网是系统工程学的奇迹：成千上万台发电机、数百条输电线和精密的市场机制共同交付 99.93% 的平均可用率。脱离电网，你就得自己扛起这份复杂性——用一座电厂达到电网级的可靠性。冗余与可用率正是**现场燃气发电成本在多数情况下结构性远贵于电网供电**的关键原因。

下一节考察领先部署如何解决这一挑战，以及它对设备选型意味着什么。

## Crusoe 与 xAI：桥接电力部署

迄今最流行的现场燃气策略之一是「桥接电力」（bridge power）。数据中心园区与电网积极洽谈接入，但先用现场电力开始运营。

桥接电力清除了电力这一运营瓶颈，让数据中心提前几个月开始训练模型或产生收入。这种提速意义重大！**AI 云每 MW 每年可净得 $10-12M 收入，这意味着让 200 MW 的数据中心哪怕提前六个月通电上线，就能净得 10-12 亿美元收入。**

桥接电力带来两大好处：

1. 可用性要求可以与工作负载相匹配。例如在得州 Abilene 和田纳西州 Memphis，xAI 与 Crusoe/OpenAI 都在部署大型训练集群。鉴于大型 GPU 集群本身就不可靠，训练任务并不需要特别高的可用性。因此可以避免为冗余而「过度建设」电厂。一旦并网落实，园区的用途可以更灵活，也能用于推理。
2. 通过取消柴油发电机备电获得有利的经济性。在 Memphis 和 Abilene，取消备电降低了数据中心单位 MW 的资本开支。一旦并网落实，这些轮机可以转任备电——因此快爬坡系统更受青睐，例如航改燃机。

为确保合理的可用率，xAI 给轮机配上了 MegaPack。这同时也能平抑负荷波动——我们将在下面讨论这个问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/b4ab9185-d960-4f39-964b-1ac2ab6c757c_1248x938.png)
*xAI Memphis 上空卫星影像*

### 永久离网：冗余挑战与能源即服务

许多发电机厂商建议数据中心业主根本不必费心与大电网并网；他们主张数据中心客户永久离网。像 VoltaGrid 这样的公司提供全套「能源即服务」（Energy-as-a-Service）包，管理电力服务的方方面面：

- **电能量**——MW 容量与 MWh 电量
- **电能质量**——电压与频率容差
- **可靠性**——目标可用率的「几个 9」
- **通电时间**——从签约到运行只需数月

它们通常与支付电力服务费的客户签订长期 PPA——EaaS 厂商实质上扮演着公用事业公司的角色。它们采购设备、设计部署方案、有时组装 BoM，并维护和运营电厂。

部署离网发电的一个关键挑战是管理冗余。例如，得州 Shackelford County 的 1.4GW Vantage 数据中心园区将部署 2.3GW 的 VoltaGrid 系统。这类系统单机小，便于做冗余——但如果用大型重型轮机做现场发电，冗余方案可能就是干脆建两座电厂，甚至更多。

发电机厂商会建议至少 N+1 配置，甚至 N+1+1 配置。N+1 配置在一台发电机意外停机时仍维持全额发电能力，而 N+1+1 配置在做到这一点的同时*还*保留另一台待机，以保障检修轮换。这相当于开车既带备胎*又*带补胎工具。注意 N+1 或 N+1+1 未必指字面上的发电机台数，因为数据中心负荷通常远大于单台现场燃气发电机。例如，考虑一座总（IT + 非 IT）电力需求为 200 MW 的数据中心：

### 示例 1：11-MW RICE

- **发电机组**：26 × 11 MW RICE 机组
- **总容量**：286 MW

正常运行时：

- 23 台发动机以约 80% 负荷运行，产出 200+ MW。
- 一台发电机故障：22 台发动机小幅提至约 82% 负荷。
- 剩余 3 台发动机留作检修或冷备用。

让发动机低于满负荷运行可降低 O&M，多余的机组为检修排程提供缓冲。

Nexus Datacenter 正在采用类似方法：他们最近为一支由 30 台 Everllence 18V51/60G 燃气发动机组成的车队申请了空气许可，每台 20.4 MW，总发电 613 MW。该场地还将包含 152 MW 柴油备用发电，很可能满足全厂 N+1 冗余要求。

### 示例 2：30-MW 航改燃机

- **发电机组**：9 × 30 MW aero
- **总容量**：270 MW

正常运行时：

- 7 台轮机以约 95% 负荷运行，以获最佳效率。
- 一台轮机故障：第 8 台轮机启动，维持出力。
- 第 9 台轮机留作检修备用。

由于轮机大修比发动机维护更具破坏性，一些厂商提供**热更换（hot-swap）**方案：把需要大修的轮机整机换成替换核心机。

在炎热气候下（例如美国西南部），降容可能需要 **10-11 台 aero** 才能维持 N+1+1 冗余。

Crusoe 在 Abilene 为 Oracle 和 OpenAI 建设的场地采用了这一设置的变体：部署了十台轮机——五台 GE Vernova LM2500XPRESS 航改燃机和五台 Titan 350，铭牌发电能力为 360MW。

![](https://substack-post-media.s3.amazonaws.com/public/images/650ec585-1693-45aa-9a14-557f2260d942_1418x648.png)
*来源：Citrini Research*

### 示例 3：Meta + Williams Socrates South

Meta 与 Williams 正在建设两座 200 MW 的表后（behind-the-meter）燃气电厂，为 Meta 的 New Albany 枢纽供电，我们已在本文中覆盖：[Meta 在俄亥俄的新一代超高速「帐篷」数据中心 – SemiAnalysis](https://semianalysis.com/core-research/metas-new-ultra-fast-tent-datacenters-in-ohio/)

![](https://substack-post-media.s3.amazonaws.com/public/images/c0c11789-f392-49d6-8874-060fa89a919d_624x428.png)
*Socrates South 卫星影像（2025 年 11 月 11 日）*

**Socrates South** 项目是一支混合车队：

- 3 × Solar Titan 250 IGT（23 MW）
- 9 × Solar Titan 130 IGT（16.5 MW）
- 3 × Siemens SGT-400 IGT（14.3 MW）
- 15 × Caterpillar 3520 快速启动发动机（3.1 MW）

围墙内的铭牌容量为 **306 MW**：轮机约 **260 MW**，发动机约 **46 MW**。正常条件下，一部分 IGT 稳定运行输出 200 MW。如果一两台 IGT 跳机，RICE 车队可以快速爬坡补上缺口。其余 IGT 留作检修切换。这支撑起一个 N+1+1 的表后设计。

不过，与前两个例子相比，这是一个「拼凑」式的实现：轮机型号互不匹配，所用的发动机也更小——1,800 rpm 的高速燃气发动机。这表明 Williams 把通电时间置于标准化检修计划之上。

### 匹配电网可用率：超额建设、电网作备、电池

要匹配电网提供的「三个 9」可用率，现场电厂必须为冗余而「超额建设」。这通常是现场发电的电力成本相对电网更高的关键原因。

冗余给运营方带来了一个新难题：系统规模与「超额建设」比例之间存在权衡。虽然 H 级和 F 级轮机的能源效率高于 aero，但更高的冗余需求意味着，如果设计不当，基于重型轮机的孤岛系统的电力成本可能反而高于 aero。必须考虑简单「超额建设」之外的其他方案，例如用较小的轮机做「备电」、电池、甚至电网连接。

![](https://substack-post-media.s3.amazonaws.com/public/images/4fdac23d-4633-4d53-9af9-00056a9fe69c_2848x1504.jpeg)

要理解超额建设比例，可以用一个实际例子。在得州 Shackelford County，VoltaGrid 正在用 2.3GW 的 Jenbacher 系统为 1.4GW（IT 容量）数据中心供电（64% 超额）。可以这样拆解：

- 峰值 PUE 超额：与得州并网站点的典型情况一样，存在 1.4x - 1.5x 的过量配置，主要与制冷相关。
- 另有 10-17% 与冗余相关的超额建设。

对 H/F 级系统而言，简单的超额建设往往不是最经济的路径。一些运营方在考虑纯粹作备用的电网连接——但这带来并网时间表的挑战，也让选址复杂化（需要高压线路接入）。也可以建一座巨型电池电厂——正如我们在 xAI 的 Colossus 2 部署中展示的——但考虑到典型的 2-4 小时储能时长，这既昂贵又不实用。最后，还可以混用不同大小的轮机与发动机，H 级以联合循环模式担任基荷，IGT/aero/RICE 做备用——但这通常比电网连接或 2-4 小时 BESS 更贵。

### 管理负荷浪涌

AI 算力负荷（尤其是训练）变化极大，包括亚秒级、兆瓦量级的功率浪涌与骤降。电力系统的**惯性（inertia）**越大，它在维持电频的同时管理短期功率波动的能力就越强。如果频率偏离 50 Hz 或 60 Hz 基准太远，功率波动可能导致跳闸或设备故障。所有火电机组都有一定惯性，因为它们靠旋转的重物发电。但开发商可以通过辅助系统增加惯性：

- **同步调相机（Synchronous condensers）**——本质上是作为电动机空转、不带机械负载的发电机。一旦与电网同步，只消耗少量损耗。在负荷突变时，它们吸收或输出**无功功率**，稳定电压并提供短时惯性。其能量容量小，只能撑几秒而非几分钟。

![](https://substack-post-media.s3.amazonaws.com/public/images/b3fbaa17-60c6-448d-ba22-818942df9adb_624x624.png)
*来源：Baldor.com*

- **飞轮（Flywheels）**——提供真正的旋转动能缓冲。电动发电机组与一个大飞轮耦合，接在发电与负荷之间。飞轮可以在 **5-30 秒**内注入或吸收**有功功率**（不只是无功），平滑暂态、发电机跳机和电压骤降。例如，Bergen 就通过一家关联厂商把飞轮与其发动机打包出售。

![](https://substack-post-media.s3.amazonaws.com/public/images/9c30a014-762b-4dfa-9e3c-8fe8c86bca2a_1430x1430.png)
*来源：Piller Power*

- **电池储能系统（BESS）**——电池可以随负荷变化同步爬坡，通过高速控制提供「合成惯性」，[如我们早前一篇文章所述](https://newsletter.semianalysis.com/p/ai-training-load-fluctuations-at-gigawatt-scale-risk-of-power-grid-blackout)。它们擅长调频，但由于逆变器限流，在无功功率和故障电流方面的贡献不如同步电机。

VoltaGrid 将 RICE 车队与同步调相机组合使用。Bergen Engines 卖过同一母公司旗下厂商的飞轮配发动机。发动机制造商瓦锡兰拥有电池储能业务线，可以与数据中心项目捆绑。Bloom 声称其燃料电池系统不需要任何管理负荷波动的设备。具体采用哪种系统，一部分取决于当地约束，更多取决于厂商偏好。xAI 偏好用特斯拉的 Megapack 做备电和处理负荷波动。

![](https://substack-post-media.s3.amazonaws.com/public/images/881af022-a429-4287-bd7e-bdf87ed4337a_1248x1118.png)
*Megapacks + MACROHARD*

## 我们到底建不建得够燃气电厂来给 AI 供电？

当前燃气发电系统的交期前所未有。历史上，燃气轮机制造商平均只接受出厂前 20 个月的订单，但如今三大制造商 GE Vernova、西门子能源和三菱电力已接单排到 2028 和 2029 年，之后还有不可退款的预订槽位。每家公开上市的燃气系统制造商都报告数据中心需求上升，但大多数以谨慎回应，而非全速扩建。

- **GE Vernova** 承诺将产量提高到 **24 GW/年**，但那只是回到其 2007-2016 年的水平。他们正在为机械制造增聘人手，但不打算扩大工厂占地。
- **西门子能源**也计划*在不*扩大工厂占地的前提下投资扩产。他们转而优先涨价、倚重服务收入、优先投资回收期短的项目。他们计划到 2028-30 年把年产能从约 20GW 提升到 >30GW。
- **三菱重工**在近期财报电话会上指引燃气轮机与联合循环产量增加 **30%**，与[彭博社报道](https://www.bloomberg.com/news/articles/2025-08-31/mitsubishi-heavy-to-double-gas-turbine-capacity-as-demand-soars)的 2027 年产能翻倍计划相左。
- **卡特彼勒**计划在 2024 到 2030 年间把发动机产量翻倍、轮机产量提升至 2.5 倍，但其 Solar 品牌轮机产量在 2020-2024 年间平均约 600 MW/年，2022 年的峰值产量为 1.2 GW。
- **瓦锡兰**只承诺渐进式扩张，宁愿对数据中心需求「观望」，并保住与船用客户的关系。

在主要燃气发电制造商中，只有 Bloom Energy、卡特彼勒和新进入者 Boom Supersonic 宣布了雄心勃勃的扩张计划。Bloom Energy 声称到 2026 年底可达到 2 GW/年的产能，Boom Supersonic 计划到 2028 年底达到 2 GW/年。乍一看，尽管需求暴涨，很少有制造商完全「All-in AGI」。这种犹豫一部分反映了真实的制造极限；更多则反映了 30 年燃气发电繁荣-萧条周期留下的创伤后应激（PTSD）。值得注意的是，最严重的瓶颈在重型轮机，Aero、IGT 和 RICE 系统的约束较小。

## 燃气轮机的两轮繁荣-萧条周期

自 90 年代中期以来，燃气轮机行业经历了*两轮*冲击整个行业的繁荣-萧条周期。第一轮繁荣发生在 1997 到 2002 年间，由美国部分地区的电力放松管制驱动，吸引了新公司以**独立发电商（IPP）**身份入场，外加（颇具讽刺意味的是）互联网泡沫带来的电力需求高增长预期——Huber 与 Mills 的论文《The Internet Begins with Coal》（互联网始于煤）让这一观点广为流传。Calpine、Duke、Williams、NRG 等大玩家对轮机下整批订单，把 GE Vernova（当时的 GE Power）和西门子能源（当时西门子股份公司的电力部门）推上月球级的订单量。GE 在 2001 年交付了超过 **60 GW** 燃气轮机；西门子在 2002 年达到 **20+ GW** 的峰值。

![](https://substack-post-media.s3.amazonaws.com/public/images/69e6ba37-ea1c-45f7-8344-1e09ccfe8643_1451x728.png)
*来源：Energy Information Administration*

崩盘来得很快。互联网泡沫破裂，安然（Enron）丑闻冲击电力交易业务，订单枯竭，GE 和西门子陷入此后数年的制造寒冬。燃气轮机行业的第二轮「繁荣」与其说是繁荣，不如说是订单的企稳。2006 到 2016 年间，GE 年均轮机交付约 **20 GW/年**，西门子约 **15 GW/年**。随后，2017 到 2022 年间市场一落千丈，GE 和西门子的产量都跌破 10 GW/年。

这两家大公司既对 Y2K 燃机繁荣存有制度记忆，也对近年历史性低销量记忆犹新。值得注意的是，三菱重工基本躲过了这些繁荣-萧条周期。直到非常近期，MHI 卖出的硬件都只是 GE Vernova 和西门子能源的一小部分。它之所以成为「三巨头」之一，是因为更大的公司收缩到了它的销量水平，*加上* Alstom Energy、Westinghouse 等玩家已经关停或被收购。这或许部分解释了 MHI 的扩张意愿，尽管其传闻中的产能翻倍计划未在财报电话会上得到证实。

## 供应链瓶颈

然而，即便有未来高需求的保证，燃气轮机核心机生产与物流的内部瓶颈也可能阻碍增产。

燃气轮机叶片与导向叶片堪称人类文明技术能力的最高标杆之一，需要极致的冶金与加工质量才能正确制造。

![](https://substack-post-media.s3.amazonaws.com/public/images/74b05e80-124e-4fcb-9a09-424938593d89_624x413.jpeg)
*加工单片涡轮叶片。来源：Reliable Turbine Services, LLC*

涡轮叶片与导向叶片是现代工业制造的最苛刻部件之一，制造它们需要非凡的冶金与加工精度。因此，西方的生产集中在四家公司：

- **Precision Castparts Corporation（PCC）**
- **Howmet Aerospace**
- **Consolidated Precision Products（CPP）**
- **Doncasters**

这些公司不仅供应工业与发电燃气轮机，也供应民用与军用喷气发动机。除 CPP 外，它们都拥有垂直整合的金属供应，但规模只有客户的一小部分，因此对市场冲击脆弱得多。第二轮燃机萧条恰逢新冠疫情导致的航空订单下滑，这些公司近期因此受创严重。需求增长不仅要求这些公司增聘专业人手，还要求它们应对钇、铼、单晶镍、钴等材料的供应链。更重要的是，它们很可能不愿做这些投资，因为如果跟着 AI 泡沫坠崖，它们将是损失最惨重的一方。

此外，重型燃气轮机的生产还受物流制约。仅核心机就是 300-500 吨的系统，需要专用驳船、铁路车厢和拖车运输。即便拿到许可，重型燃机还需要 24-30 个月建造、安装和测试才能投运。售后市场 OEM 可以围绕翻新核心机建新电厂，但搬运和集成这些核心机仍是重大挑战。这些约束对 aero 和 IGT 较轻——它们小到可以用标准集装箱或常规拖车运输。

![](https://substack-post-media.s3.amazonaws.com/public/images/563ad592-27dd-4381-9f6e-7c30aa41be91_1619x1079.jpeg)
*Siemens SGT5-800H H 级轮机装在自行式模块运输车（SPMT）上。来源：Siemens China*

## 新玩家来救场：从客机到轮船？

一如既往，每逢供给受限，许多聪明的公司都在探索解法。ProEnergy 是最早带来创新的公司之一。其 PE6000 项目改装波音 747 的 CF6-80C2 发动机核心机，交付规格与封装和 GE Vernova LM6000 几乎一致、可直接投运的航改燃机。

![](https://substack-post-media.s3.amazonaws.com/public/images/722e94e6-b9c2-48c7-b7d3-9f1bd09e9bc3_1237x643.png)
*ProEnergy PE6000。来源：Datacenter Dynamics*

更近一些，Boom Supersonic 宣布开发基于其超音速喷气发动机设计的 **Superpower** 航改燃机。其提出的形态看起来与 GE Vernova LM2500 惊人地相似，工作原理也相同：一台可以装进一个集装箱的小型喷气发动机（进气、控制与排气等辅助设备再装 1-2 个集装箱）。该发动机的测试仍在进行中，但初步宣传规格显示 Superpower 单机出力可达 42 MW——即便在高环境气温下也是如此。

![](https://substack-post-media.s3.amazonaws.com/public/images/15b3afb5-850a-498c-a925-9609aa84637d_4096x2304.jpeg)
*来源：@bscholl，Twitter*

首批 1.2 GW 产能已被 Crusoe 预订，目标是 2027 年产 200 MW、2028 年 1 GW、2029 年 2 GW。初始订单价格暗示硬件成本为 $1,000/kW，但该数字不含电厂配套设备（balance of plant）、运输或调试，不应与全包成本直接对比。Boom Supersonic 已对叶片与导向叶片生产实现垂直整合，但冶金仍依赖外部供应商，这可能仍是供应链瓶颈。

我们尚未看到其他公司加入改装行列。但中速发动机主要由长期制造船用发动机的公司生产——例如瓦锡兰。事实上，它们大体就是同款发动机，可以在同一工厂制造。什么时候我们会看到旧船用发动机被改装去给数据中心供电？

现在让我们把注意力转向比较不同方案与制造商。我们还将分析现场发电的经济性与 TCO，并与美国的电网进行对比。

# 现场燃气发电 TCO 分析与领先厂商
