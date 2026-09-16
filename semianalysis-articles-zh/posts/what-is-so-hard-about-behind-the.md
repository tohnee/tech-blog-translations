---
title: "数据中心的表后电力到底难在哪？第一部分"
title_en: "What is So Hard About Behind-The-Meter Power For Datacenters? Part 1"
subtitle: "愚蠢的科学实验 vs. 印钞机"
date: 2026-09-10
source: https://newsletter.semianalysis.com/p/what-is-so-hard-about-behind-the
crawled: 2026-09-15
authors: ["Ellie Holbrook", "Robert Boswall", "Jeremie Eliahou Ontiveros", "Nicolas Bontigui", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 数据中心的表后电力到底难在哪？第一部分

> 原文：[What is So Hard About Behind-The-Meter Power For Datacenters? Part 1](https://newsletter.semianalysis.com/p/what-is-so-hard-about-behind-the) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**愚蠢的科学实验 vs. 印钞机**

![](https://substack-post-media.s3.amazonaws.com/public/images/0fe650d6-cdda-4d26-a83d-1e793cf406c0_1672x941.png)

去年，我们最先指出，[现场燃气发电已成为 AI 实验室与超大规模云厂商解决电力约束的主要手段](https://newsletter.semianalysis.com/p/how-ai-labs-are-solving-the-power)。我们的乐观判断远非市场共识：表后（behind-the-meter，BTM）主电源方案曾被冠以各种名号，比如「[科学实验](https://www.axios.com/2026/07/27/off-grid-ai-data-centers-reckoning)」「[黑暗吉瓦（Dark Gigawatts）](https://www.axios.com/2026/07/27/off-grid-ai-data-centers-reckoning)」，甚至是「[人类有史以来尝试过的最愚蠢的事情](https://www.volts.wtf/p/doing-data-centers-the-not-dumb-way)」！

但自那以后，这条供应链出现了大规模加速。我们的[能源模型](https://semianalysis.com/energy-model/)目前追踪到供应链中 **仅面向表后 AI 算力** 的 75GW 具约束力的确定订单——其中仅 2026 年第二季度就下单约 20GW。最初只是 Elon Musk 的一项实验，如今已成为每一家 AI 实验室和超大规模云厂商的主流选择。需要说明的是，这一数据并不包含许多其他分析师计入统计的数百 GW 投机性、毫无依据的公告——我们只专注于专门服务 BTM AI 算力的 OEM 所收到的具约束力订单，并按项目级别逐一追踪。

![](https://substack-post-media.s3.amazonaws.com/public/images/d187f762-eebb-4ebf-a9e3-18ff8491c84d_2430x1296.png)
*资料来源：SemiAnalysis Energy Model；sales@semianalysis.com*

从确定的设备订单到交付落地的项目，道路依然漫长且充满挑战，执行风险相当可观，这正是本报告的焦点。但这个行业比你想象的更有经验：到今年年底，美国将有约 3GW 在运数据中心 IT 容量由表后电源供电，而且这一数字将连续多年保持三位数增长。我们的能源模型与数据中心模型已计入所有潜在延期因素，正如我们在《[别再说 2026 年美国数据中心产能有一半被取消了](https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter)》一文中深入阐述的那样。

![Image preview](https://substack-post-media.s3.amazonaws.com/public/images/2906ff1c-b475-4668-a38f-de6d96871268_2700x1440.png)
*资料来源：SemiAnalysis Energy Model；sales@semianalysis.com*

领先 AI 实验室和超大规模云厂商所开发的多个最具战略意义的项目正依赖表后电源，支撑着未来数千亿美元的营收。采用范围之广前所未有。举几个例子：

- 2026 年年初至今，Microsoft 已签署超过 5GW 的表后铭牌容量，其中 2.7GW 来自与 Joulent 和 Chevron 的合作，另有远超 2GW 通过与 Crusoe 等公司的交钥匙数据中心租约获得。这 5GW 涵盖了类型广泛的各种电力设备；[完整拆分](https://semianalysis.com/energy-model/)供我们的能源模型订阅客户查阅。
- Google 历来对现场燃气最不情愿，但正在 Armstrong County 的旗舰园区部署 930MW 离网航改式燃气轮机。此外，这家搜索巨头还将在怀俄明州部署 900MW 的 Bloom Energy 燃料电池——正如[我们 2026 年 2 月所言](https://semianalysis.com/institutional/2026-datacenter-outlook-6-gw-leased-this-quarter-google-cloud-and-aws-acceleration-in-q4-anthropic-and-google-driving-the-market-2/)，这对 Bloom Energy 是重大利好。这些燃料电池将与 >1GW 的 Mitsubishi J 级燃气轮机配套。
- Anthropic 和 Meta 均与 Enchanted Rock 签署了 300–500MW 的协议。Enchanted Rock 是一家 0.5MW 发电机组供应商，其产品围绕一台 21.9 升 V12 燃气发动机构建。另外，Anthropic 由 Google 兜底的得克萨斯州旗舰园区也将部署超过 1.5GW 的离网电源；Anthropic 各数据中心设施的完整拆分供我们的[数据中心模型](https://semianalysis.com/datacenter-industry-model/)订阅客户查阅。
- OpenAI 即将在其位于得克萨斯州 Shackelford County 的 1.4GW（IT 容量）离网旗舰园区开始运营，使用超过 **五百台 4.25MW 的 Jenbacher J624 发动机**。我们在下文展示了该园区的一部分。加上其位于新墨西哥州的 1.3GW IT 园区，这代表着 OpenAI 依赖表后电源与 Oracle 签署的超过 $150B（1500 亿美元）的合同支出。

![](https://substack-post-media.s3.amazonaws.com/public/images/c70af619-d9fb-4481-9772-08bf560a81fa_5585x3465.png)
*资料来源：SemiAnalysis Datacenter Model；SemiAnalysis Energy Model；Sales@semianalysis.com*

为什么会这样？为什么那么多能源专家错得如此离谱？关键在于理解 AI 经济学。我们已在多篇文章和我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)中详细讨论过。简单回顾一下：兆瓦对终端用户的价值正在飞速飙升。一座支撑 1GW IT 孤岛运行数据中心的电厂通常耗资约 $5B（50 亿美元）。在当前环境下，**推理 API 营收可达每 GW 每年 $100B（1000 亿美元），毛利率超过 90%**。为了更快的部署速度，多花一倍的钱或接受效率低 30%，根本无需犹豫。换个说法，**Anthropic 及其同行只需 20 天的推理营收就能赚回一座电厂的价值**。正如我们六个月前所讨论的，[AI 基础设施栈中的大部分价值正在向前沿模型开发者转移](https://newsletter.semianalysis.com/p/ai-value-capture-the-shift-to-model)。

电网根本跟不上需求。新建电源动辄需要五年以上，而在需求侧，数据中心并网也要数年。更多信息请阅读我们关于美国电网约束的文章（[US Grid Constraints](https://newsletter.semianalysis.com/p/us-grid-constraints-towards-40gw)）。

![](https://substack-post-media.s3.amazonaws.com/public/images/e283a93c-faff-44b5-be6c-5ce8934ebeae_1009x538.png)
*资料来源：SemiAnalysis Tokenomics Model；SemiAnalysis Inference Simulator；sales@semianalysis.com*

这样的市场环境，对于表后电源突破上述约束是压倒性的利好。但这些数据中心现场电源方案正日益偏离其并网同类。正如一年前所预测，赢家并不只有 GEV 和 Siemens Energy 这样的在位者。最大的受益者是数十家往复式发动机供应商，形态各异，单机 0.5MW 到 20MW 的方案正在大规模落地。一年前，我们统计到 12 家获得数百 MW 级数据中心离网订单的制造商；[如今这一数字已达 22 家](https://semianalysis.com/institutional/pistons-at-the-gate-bullish-recips-on-expanding-prime-power-deployments-4x-capacity-bring-up-and-competitive-cost-lead-time-trade-off/)，且还将继续增长。我们的[能源模型](https://semianalysis.com/energy-model/)按季度追踪 30 多家 OEM 的制造产能、订单、交付与可获量。

![](https://substack-post-media.s3.amazonaws.com/public/images/cda4ece6-66ad-4da3-9f3d-53b3561414f3_2430x1296.png)
*资料来源：SemiAnalysis Energy Model；sales@semianalysis.com*

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

这一切的光明面是创新，但另一面是行业迫近的执行挑战。其中许多事情从未在这种规模或速度下做过。裂痕已开始显现。许可审批延误已迫使 Oracle Project Jupiter 和 Nebius 新泽西等高曝光项目紧急转向污染更低的替代方案（Bloom 燃料电池）。管道延误也冲击了 Oracle 1.3GW IT 的 Project Jupiter（我们的能源模型早在 2026 年 5 月就[预警了这一点](https://semianalysis.com/institutional/oracles-new-mexico-stargate-gas-pipeline-delayed-no-bloom-without-gas)，远早于媒体头条）。市场上关于可靠性问题的传闻日益频繁。劳动力短缺来势汹汹。设计与可用率的考量充满挑战，拖慢了一些项目的最终投资决策（FID）。与失败项目绑定的确定订单，则催生出了一个刚刚起步的燃气轮机二级市场。

在今天的报告中，我们深入「数据中心微电网」的世界。我们审视 BTM 建设浪潮面临的挑战与质疑，并看看这一切究竟是如何落地的。

1. 「表后」到底是什么。详述数据中心与电网之间可能的各种关系，主电源与备用电源之辨；包括什么时候算是名不副实的微电网。表后究竟该如何定义？
2. 项目如何成败。我们梳理 BTM 项目的六个关键阶段与挑战：合同与融资可行性、许可审批、燃料供应、设备采购、劳动力，以及无电网连接运行的物理学。我们从融资之墙讲起——开发商越来越多地陷入「先有鸡还是先有蛋」的困境，以及新一代「BTM 公用事业」的崛起。
3. 路在何方。「并网，还是不并网」；当电网电力最终到来时，这些电厂将何去何从——向电网送电、继续当主电源、转为备用，还是迁往他处。与此同时，为应对当下而拼命扩张的订单簿和制造产能又将走向何方。我们还将给出对得克萨斯州 BTM 走向的看法。

过去几个月，我们为[能源模型](https://semianalysis.com/energy-model/)客户发布了大量研究，梳理设备格局（燃气轮机、往复式发动机、燃料电池）中的赢家与输家、AGX 等承包商、中压 UPS 系统等电厂配套（BoP）设备，以及新的低电压穿越（LVRT）法规可能对某些大型工业企业造成的负面影响。在本报告付费墙之后，我们为 Substack 订阅者精选了其中一部分内容。

> 会议预告：9 月，SemiAnalysis 能源模型团队成员将出席以下会议：曼谷 Gastech（14–17 日）；达拉斯 Data Center World Power（21–23 日）；拉斯维加斯 Yotta 与奥斯汀 Gulf Coast Power Association（均为 28–30 日）。欢迎发邮件至 energy@semianalysis.com，一起聊聊电力！

*我们感谢 Celsius Industries 的 Michele Tarawneh 对本报告的宝贵输入！*

# 「BTM」到底是什么？

电表是计量电力的装置，安装在项目线路与电网线路的交汇点上。该点电网一侧的一切——变电站、高压塔、电厂——都属于「表前」（front of the meter）；项目一侧的一切——开关设备、电池和现场发电机——都属于「表后」（behind the meter）。

此外还有一些特定术语，但实际使用中常被混用：「behind-the-meter」（表后）、「off-grid」（离网）、「islanded」（孤岛运行）、「co-located」（共址）和「micro-grid」（微电网）。这很令人头疼，也常引发定义之争，但可以用连接方式来理清它们：

![](https://substack-post-media.s3.amazonaws.com/public/images/c21de2a8-c4b3-4705-9bbf-9eab3b7b35d6_2600x1680.png)
*资料来源：SemiAnalysis*

1. **电网供电（Grid-supplied）：** 电网为数据中心供电；现场发电仅作备用。电厂向公共网络供电，再由公共网络向数据中心供电。
2. **电网并联（Grid-parallel）：** 本地发电和电网受电都可向数据中心供电。是否可上网送电，视权利与连接条件而定。

   1. 数据中心、其本地电源与其获准的电网受电容量之间的相对规模可以差别很大。ERCOT 的「受提取限制私用网络」（Withdrawal-Limited Private Use Network，WLPUN）框架明确支持利用现场发电来削减大型负荷所需的输电容量。
   2. 考虑三种示例配置，均服务于同一座 **1,000 MW 数据中心**：

      1. **电网主导：** 250 MW 本地发电 + 1,000 MW 受电上限。本地发电抵扣部分电网用电；在数据中心满载、本地发电满发 250 MW 时，还需受电 750 MW。
      2. **电厂主导、满额受电连接：** 1,200 MW 本地发电 + 1,000 MW 受电上限。电厂可覆盖正常需求，而受电上限也足以承接整个数据中心负荷。
      3. **电厂主导、受限受电连接：** 1,200 MW 本地发电 + 250 MW 受电上限。满载时至少 750 MW 必须来自本地资源。若本地发电全部失去，将需要替代电源，或至少削减 750 MW 负荷。
3. **仅上网（Export-only）：** 本地发电为数据中心供电；电网连接只允许送电上网，不允许受电带载。
4. **离网（Off-grid）：** 本地发电为数据中心供电，没有运行中的电网连接。

#### **净计量**

在本文语境中，净计量（net metering）指在面向电网的计量或结算边界上，将数据中心的用电与其关联发电相互抵扣。ERCOT 将其表述为减少用户自电网的计量用电量；它并不一定是那种按账单周期把上网电量抵扣用电量的居民屋顶光伏零售安排。

Freestone 就是一例：ERCOT 报告称，PUCT 于 2026 年 5 月批准了 Freestone County 一座 1,099 MW 燃气电厂与一座 760 MW 数据中心之间的净计量安排。

#### **为什么「仅上网」不等于「离网」**

数据中心并不需要一条单独的电网馈线来保持电气连接。如果其供电回路接入电厂的并网交流系统，它就是经由电厂与电网相连；即便净送电上网，场站仍参与该互联系统的频率动态和共享惯性响应。视电网运营水平而定，这种安排可能对数据中心有利，带来更好的电气可靠性与电能质量。

#### **既有机组带来的监管区分**

监管机构还会区分新建电源与此前向电网供电的电厂。《得克萨斯州公用事业法典》第 §39.169 条「大型负荷客户与既有发电资源共址」适用于涉及 **截至 2025 年 9 月 1 日** 已注册为独立发电资源的在运设施的某些净计量安排；该条款要求通知 ERCOT 并接受 PUCT 审查，设有豁免情形与视同批准条款。

将既有机组的出力改供新负荷，可能减少对更大范围电网的可用供应。ERCOT 表示，截至 2026 年 5 月批准的两项净结算安排均要求：数据中心削减用电或切换至备用电源，而电厂须在接到 ERCOT 指令后 30 分钟内将全部出力返回电网。

### **运行状态与部署形态：孤岛运行、过渡电源、电网作后备**

「孤岛运行」（islanded）是一种运行状态：并网型数据中心断开断路器，靠自己的发电运行。与之相关但又有区别，美国能源部（DOE）将「微电网」定义为「位于清晰界定的电气边界之内、作为单一可控实体相对于电网运行的相互连接的负荷与分布式能源的组合」，其电网部署办公室（Grid Deployment Office）补充称，微电网「可以以并网或孤岛模式运行，包括完全离网的应用」。本文中，「可孤岛微电网」指能够解列的并网型场站；「离网微电网」指完全没有电网连接的场站。许多 BTM 项目对这个词用得很随意，或许是因为它能避免说出「燃气」二字。

实践中，这一切可能随时间大幅改变。许多 BTM 项目规划了电网连接，把 BTM 当作「过渡桥」——一旦公用事业交付连接，发电机便可转入备用角色。我们在《[现场燃气深度解析](https://newsletter.semianalysis.com/p/how-ai-labs-are-solving-the-power)》中深入描述过，这是最流行的路径，因为电力系统在成本和可靠性上都受益于显著的规模经济。xAI 位于孟菲斯（Memphis）的 Colossus 1 走的就是这条路。

另一些项目则把规划中的电网连接当作「后备」，即作为一种有助于提升预期可用率的新增能源资源。我们看到有项目在完全孤岛模式下按 2 个或 3 个「9」的预期可用率规划，并网后再增加一个「9」。未来几年将有多少 BTM 电厂转为并网，我们会在付费墙后给出更多思考。

# **为什么 BTM 建设如此之难？**

一份燃气轮机订单加一条邻近的管道，并不等于一个项目。从新闻稿到首次送电之间，横亘着六道关键关卡：合同与融资可行性、许可、燃料、设备、劳动力和电气物理。我们按许可级别的追踪显示，已预订产能几乎在每一道关卡上都遭遇困难。

![Six-part BTM framework](https://substack-post-media.s3.amazonaws.com/public/images/d48333e1-a65d-49f9-bf61-36a89d5108c4_2700x1580.png)
*资料来源：SemiAnalysis Energy Model；sales@semianalysis.com*

## **第 0 关：合同与融资可行性**

下文将讨论 GW 级孤岛数据中心上线面临的所有物理挑战。但在那之前，还有一个也许更大的挑战：资金。传统上，并网的成本很低，并网申请和信用证的金额都很有限。这足以开发出可信的场站，即便是 GW 级也行，并由此引发了美国乃至全球对电力的疯狂追逐。用有限资本——最多几百万美元——快速获利轻而易举。我们在《[Onsite Gas Deep Dive](https://www.bing.com/search?pglt=2083&q=onsite+gas+deep+dive&cvid=bb1ec263808b4c889798e699f40117f7&gs_lcrp=EgRlZGdlKgYIABBFGDkyBggAEEUYOdIBCDI4OTZqMGo3qAIAsAIA&FORM=ANNTA1&PC=DCTS)》和《[US Grid Constraints](https://newsletter.semianalysis.com/p/us-grid-constraints-towards-40gw)》等文章中对此有详尽讨论。

孤岛数据中心则根本不同，因为没有现成基础设施可供接入。按每 GW IT 容量约 $5B（50 亿美元）的电厂造价，加上日益高昂的设备定金，前期资本开支卡住了许多项目。

这就引出了经典的 BTM「先有鸡还是先有蛋」难题：贷款方希望看到有可靠承购方的长期供电协议（ESA），以及清晰的 SLA 和其他合同条款；承购方希望看到可信的时间表和项目系统设计；开发商则需要早期资金支付设备定金，才能拿出那份可信的时间表与设计。而在[燃气发电设备需求空前旺盛](https://semianalysis.com/energy-model/)的当下，没有这笔资金就意味着时间表一拖再拖。

![Image preview](https://substack-post-media.s3.amazonaws.com/public/images/4a4e041d-ed40-4570-bb6c-26330d327508_2700x1440.png)
*资料来源：SemiAnalysis*

早期成功者有三种形态：

1. 全垂直整合，Musk 打法：正如我们在《[Colossus 2](https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter)》一文中详述的，xAI 为自用而建电厂，视其为最快的算力建设方式。其资金大概率来自股权融资。
2. 全范围数据中心开发商：某些开发商把建造与能源都纳入核心能力，向超大规模云厂商出售时一并对 BTM 电厂负责。在成本收益率（Yield on Cost）模型中，他们通常把现场电源计入成本包络——之后往往突破 $20M/MW 大关。完整场站级细节见我们的[数据中心产业模型](https://semianalysis.com/datacenter-industry-model/)。
3. 数据中心 + 电力搭档：数据中心开发商与电力开发商联合向超大规模云厂商销售场站。但超大规模云厂商要签两份独立合同：一份数据中心、一份电力。Oracle Stargate 的某些场站即基于此类安排。联合销售意味着承购方得到全栈方案；但主要缺点是要应付更多交易方，而且由于两份合同彼此独立，无论电力还是数据中心哪一边延期，都可能承担搁浅费用的风险。

在 BTM 电力领域，所有这些复杂性催生了一类新型服务商：能源即服务（EaaS）供应商。它们是新一代「BTM 公用事业」。VoltaGrid 等公司以长期合同交付电力而不只是设备，附带容量与可用率保证。EaaS 无所不包：从租赁发电机组，到在永久电厂和真正的管道完成许可、建设和调试之前，用槽车把压缩天然气运到现场充当「虚拟管道」。

VoltaGrid 已被证明是这股潮流的赢家之一，从 Vantage Datacenters 等一线开发商手中拿下数 GW 订单。Williams、Solaris 等也在崛起，斩获大单。另外，一些制造商正越来越多地亲自下场，如 Bloom Energy 和 Enchanted Rock。我们在[能源模型](https://semianalysis.com/energy-model/)中追踪数百个项目的全部供应链、EPC、BESS/同步调相机（SynCon）等环节。

![](https://substack-post-media.s3.amazonaws.com/public/images/222c7c88-0f06-4783-b274-21a0ce6e05e7_963x524.png)
*资料来源：VoltaGrid*

这道资本之墙是否意味着 BTM 相对电网存在结构性劣势？***过去是，现在不再是了***。美国电网约束正在实时显现，体现在两个方面：

1. 随着美国电网的确定富余容量耗尽，服务一座新的 GW 级数据中心必须搭配 GW 级电源。如今资本需求普遍达到每 GW 数十亿美元量级。廉价的 GW 级并网已不复存在。
2. 多数公用事业公司的拖沓与不可靠人尽皆知，而且在延期交付或可用率出问题时，电网 ESA 通常不像 BTM 合同那样具约束力、罚则也没那么多。这说得通，两者本来就是性质迥异的合同。因此，对于执行速度与可信度至关重要的 GW 级项目，BTM 的竞争力与日俱增。

因此，我们[认为](https://newsletter.semianalysis.com/p/us-grid-constraints-towards-40gw)融资环境正日益利好 BTM。此外，数据中心开发商在能源领域越来越老练，正在组建自己的世界级团队，并越来越多地向承购方提供包括 BTM 电厂在内的全交钥匙范围。

## **阶段 1：许可**

### **州说了算**

说完资金，现在来攻克物理挑战，先从许可说起。我们在《[现场燃气深度解析](https://newsletter.semianalysis.com/p/how-ai-labs-are-solving-the-power)》中就警告过：即便在审批最快的州，为现场发电取得空气许可也可能要一年以上，而且许可当时就已经在拖累一些项目。本节我们将概述各州许可强度的差异，以及一些开发商绕开许可障碍的创造性解法。

因此，第一个决策是在哪里递交申请。找到友好地区至关重要；如果拿不准，可以把场址选在州界上对冲风险。Colossus 2 坐落于田纳西州孟菲斯的 Tulane Road，距密西西比州界仅数百米之北。它的电厂则在州界另一侧，位于 Southaven 一处前 Duke Energy 场地——由 xAI 一家关联公司于 2025 年 7 月购入。这样一来，空气许可便从曾为 Colossus 1 燃气轮机发证的 Shelby County 挪到了密西西比州。密西西比州允许这些燃气轮机以「临时」机组身份在无空气许可的情况下运行至多 12 个月，并于 2026 年 3 月由其许可委员会一致批准了一座 41 台燃气轮机、1.2 GW 的电厂，将其转为永久。

更广泛的启示是：开发商如今挑选司法辖区几乎像挑选设备一样仔细。同一座电厂，在一个州可能只需标准化登记，在另一个州要逐案审批空气许可，在第三个州则要分别取得空气、选址和发电三套批准。

![](https://substack-post-media.s3.amazonaws.com/public/images/0451ed1a-b17c-4cc8-a69b-e8e0bc420a49_2430x1296.png)
*资料来源：SemiAnalysis Energy Model；Sales@semianalysis.com*

州与州之间的这种不对称，加之廉价天然气，解释了为什么得克萨斯州承载的 BTM 机组将超过其他任何州。州决定流程如何展开，但联邦规则设定了大部分参数。美国环境保护署（EPA）制定核心空气质量标准、排放定义与大型源框架；州和地方当局通常负责执行这些规则、发放许可，并增设自己的审批通道。

### **空气许可门槛如何运作**

潜在排放量（Potential to Emit，PTE）指电厂全年满负荷运行时的排放吨数，按污染物分别计。美国每一份空气许可都要检验 PTE。对燃气发电而言，两种关键污染物是氮氧化物（NOx）和一氧化碳（CO）。联邦层面有两条线：任何污染物 PTE 超过每年 250 吨的电厂须走完整的大型源审查——建模、公众程序，时间表可能因此增加数年；PTE 超过 100 吨的电厂还需要 Title V 运营许可，这是联邦监管的第二层。各州在联邦线以下另设自己的门槛。

#### **层级：**

1. 作为非道路发动机豁免：在现场停留不超过 12 个月的移动式发动机

   1. 位于固定源许可体系之外。仅适用于往复式发动机：任何每小时 1000 万 Btu 及以上的燃气轮机都落入联邦排放标准，这一点已被 EPA [2026 年 1 月的燃气轮机规则](https://www.federalregister.gov/documents/2026/01/15/2026-00677/new-source-performance-standards-review-for-stationary-combustion-turbines-and-stationary-gas)确认。密西西比州依据州规则豁免了 xAI 拖车装载的 Southaven 燃气轮机；该决定正在联邦法院受到挑战；见 [40 CFR 1068.30](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-U/part-1068/subpart-A/section-1068.30)。
2. 小型新源审查（Minor NSR）：PTE 低于所有大型源门槛

   1. 由州或县颁发的建设许可，豁免界限与所需建模量由其规定。至少 30 天公众意见期。接受可执行的运行小时数或燃料上限以压在线下的电厂属于「合成小型源」（synthetic minor）；日后更改该上限将触发完整的大型源审查，视同新建电厂；见 [40 CFR 51.160 至 51.161](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-51/subpart-I/section-51.160)；[40 CFR 52.21(r)(4)](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-52/subpart-A/section-52.21)。
3. 显著劣化预防（PSD），即大型源审查：任一污染物 PTE 达每年 250 吨。28 个列名行业为 100 吨；EPA 将「蒸汽电厂」解读为涵盖联合循环电厂，而简单循环电厂被视为未列名，因此适用 250 吨上限。

   1. 通常由州颁发。只要因一种污染物被列为大型源，电厂就必须对所有超过显著率（NOx 40 吨、CO 100 吨）的污染物采用最佳可行控制技术（BACT），对空气质量影响进行建模，通常需提交一年监测数据，并接受至少 30 天公众意见。《清洁空气法》要求在申请材料完备后一年内作出决定（[第 165(c) 条](https://www.law.cornell.edu/uscode/text/42/7475)）；实际耗时并无全国性数据；见 [40 CFR 52.21](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-52/subpart-A/section-52.21)。
4. 未达标区 NSR（Nonattainment NSR）：该区域未达某污染物的联邦空气标准。它在该污染物上取代 PSD；其余污染物仍适用 PSD。

   1. 门槛降至每年 100 吨，并随臭氧未达标区被评定为严重（serious）、重度（severe）或极端（extreme）而进一步降至 NOx 和 VOC 50、25 或 10 吨（[《清洁空气法》第 182 条](https://www.law.cornell.edu/uscode/text/42/7511a)）。电厂必须达到最低可达排放率（LAER），并以每吨 1.1 至 1.5 吨的比率向同一区域的其他排放源购买抵减量。地点决定门槛：达拉斯和休斯敦为 25 吨，芝加哥、盐湖城和拉斯维加斯为 50 吨，北弗吉尼亚和凤凰城为 100 吨（[EPA Green Book](https://www.epa.gov/green-book)）；见 [40 CFR 51.165](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-51/subpart-I/section-51.165)。
5. Title V 运营许可：PTE 达每年 100 吨及以上，叠加在适用的建设许可之上。

   1. 须在投运后 12 个月内申请。把所有要求汇集成一份为期五年的可执行文件。EPA 有 45 天异议期，公众有 60 天请愿期。它增加监测、报告与费用，本身不设定新的排放限值；见 [40 CFR 70.2](https://www.ecfr.gov/current/title-40/chapter-I/subchapter-C/part-70/section-70.2)。

#### 三点注意事项。

1. 简单循环电厂适用 250 吨线，依据的是监管机构一以贯之的实践——包括密西西比州自己的 xAI 许可——而非 EPA 的成文裁定。
2. 联邦线以下各州各异。得克萨斯州要求所有新建设施采用控制技术。弗吉尼亚州对超过 40 吨 NOx 的项目都要发证。加利福尼亚州各区的控制措施触发点低至每天 10 磅。
3. 无论许可层级如何，联邦排放标准均适用。[2026 年 1 月的规则](https://www.federalregister.gov/documents/2026/01/15/2026-00677/new-source-performance-standards-review-for-stationary-combustion-turbines-and-stationary-gas)对基荷运行的新建大型燃气轮机设定了 5 ppm NOx 下限。这意味着从第一天起就要上选择性催化还原（SCR）。

![](https://substack-post-media.s3.amazonaws.com/public/images/2af5a1de-c574-4813-bf59-7a04ce49f029_2430x1296.png)
*资料来源：SemiAnalysis Energy Model；Sales@semianalysis.com*

园区规模之下，很低的排放速率也会累积成巨大的年度总量。以示例性的受控 NOx 排放率 0.10g/kWh 计，250MW × 8,760 小时每年约产生 241 美制短吨；同一算法在约 259MW 处达到 250 吨。实际答案取决于设备的受控排放水平、适用门槛，以及监管机构把哪些机组合并计为同一排放源。

于是开发商只能在电厂规模与运行方案两头做文章。在项目与规则允许的情况下，分期授权可以让首批机组先上线，同时更大规模扩建的审批继续推进。但小时数与排放限值必须经得起既定运行计划的检验，且可执行。监管机构需要一份关于整个园区如何运行的、可信的方案。

#### Project Jupiter：宏大设计

英国电视名宿、建筑评论家 Kevin McCloud（节目《Grand Designs》主持人）若看到 Oracle 的 Project Jupiter，恐怕要挑起眉毛了——它展示了许可如何迫使整个设施以惊人的速度推倒重来。

最初的申请于 2025 年 11 月 17 日递交，包含东、西两个独立微电网，规模都恰好压在联邦 250 吨大型源线之下。西侧申请提出 34 台 GE TM2500 与 20 台 Mitsubishi FT8（54 台燃气轮机，约 1,677 MW），东侧微电网规模更高。其策略是以「合成小型源」方式运行：安装排放能力远超大型源门槛的设备，再接受把获准排放压在线下的运行限制。东侧微电网申报的 NOx 潜在排放量为每年 521 吨，申请上限 248.90 吨，比门槛低 1.1 吨。

![](https://substack-post-media.s3.amazonaws.com/public/images/b9b8db8a-c77a-4851-83fe-5b1ba41f0540_2430x1296.png)
*资料来源：SemiAnalysis Energy Model；Sales@semianalysis.com*

新墨西哥州环境部认定，贴着门槛设定的限值实际无法执行。申请人把两个上限都降至 245 吨以求解决，环境部随后裁定两份申请材料完备并公布拟发证意向——但涌入了约 7,155 条公众意见，部长同意举行听证会，申请人遂于 2026 年 4 月 27 日、即宣布燃料电池改设计当天，撤回了两份申请。

随后项目放弃了燃气轮机设计，于 4 月围绕 Bloom Energy 固体氧化物燃料电池重新申请。修改后的方案目标是 NOx 每年约 37 吨，比原燃气轮机配置低约 92%。

技术路线切换并未让许可问题消失。2026 年 8 月 23 日，新墨西哥州最高法院中止了行政空气许可程序，直至另行下令。该中止令只是暂停程序，并未裁断申请本身的是非；9 月 1 日，大法官们一致驳回了开发商哪怕是暂时解除中止令的请求。监管机构的决定截止日期是 2026 年 11 月 23 日。

### **燃料电池的逃生通道**

燃料电池提供了一条逃离许可中最棘手环节的通道，但逃不掉许可程序本身。

该技术通过电化学反应而非火焰燃烧发电，NOx 及其他常规污染物通常远低于同等规模的燃气轮机或往复式发动机群。视场址与配置而定，燃料电池可以让项目低于 PSD 大型源门槛，转而走标准化或小型源通道。它们仍需许可、仍产生 CO₂ 和少量其他污染物，但其优势在于更轻的监管负担，而非零排放。

AEP Ohio 在俄亥俄州 AWS Hilliard 场站的 72.9MW Bloom 安装项目，展示了燃料电池许可中的波折：项目虽保持在会触发大型源通道的门槛之下，但仍需俄亥俄州 EPA 空气许可和单独的州选址批准，且空气许可于 2025 年 11 月被 Hilliard 市提起上诉。

Nebius 在其首个美国 BTM 部署中同样做了技术取舍，以一份十年期购电协议用 328MW Bloom 燃料电池取代了原计划的燃烧类发电，公司称部署更快、许可负担更轻是这次切换的优势。

燃料电池可以帮项目快速穿过许可矩阵，但也会让投机项目更容易「装点门面」。我们在得州发现一份申请：一座拟建的 560MW Bloom 燃料电池电厂缴纳了 $900 标准许可费，从 2025 年 12 月 19 日收到申请到 2026 年 1 月 14 日获得批准，TCEQ 认定该设施在 PSD 和 Title V 下均非大型源。

标准许可只确认拟议的设备配置符合一份预先写好的排放包络。它并**不**证明该数据中心已有确定的租户、融资、已购设备、确定的燃气供应或开工令。这正是我们不把「已获许可」当作新 BTM 项目放行信号的原因。

![Permit-credibility ladder](https://substack-post-media.s3.amazonaws.com/public/images/1f58862d-c19a-4396-8667-2414cf44cfa7_2700x1540.png)
*资料来源：SemiAnalysis Energy Model*

请注意，另一个常被忽视的许可约束是水。对散热器冷却的往复式发动机而言，工艺水需求可以很低：散热器把发动机热量直接排入空气。但某些简单循环燃气轮机为控制 NOx 需要喷水或喷汽，形成持续的用水需求，而干式低排放（DLE）燃烧则免去这种喷射。轮机整套配置与技术标签同样重要。例如 Pratt 的 FT8 MOBILEPAC 就采用喷水。

联合循环又添一重抉择。湿式循环冷却会通过蒸发和排污损失水——排污是为了防止溶解物质累积而排放的水。干式冷却则把热量排给空气。

## **阶段 2：天然气**

许可固然是选址的核心约束，燃料又添一重。美国天然气泛滥：高油价让人们始终有动力「拼命钻探」（drill baby drill），采油伴生的天然气需要找到去处；同时阿巴拉契亚（Appalachia）和 Haynesville 又提供了充足的干气（不伴生于采油）供应。

然而，难点在于运输。建设管道可以同时是 BTM 数据中心建设流程中最难和最易的环节——和许可一样，高度取决于地理。此外，一条管道通常不够。固定（firm）合同绑定最大日供气量、指定的接收与交付点，以及（如约定）最低交付压力；而可中断服务在管道趋紧时会被削减。因此地图上的一条线说明不了什么，关键是每天有多少确定气量能物理抵达电厂计量表。燃料的物理系统还必须扛得住故障。视场址而定，这可能意味着独立气源、冗余内部管网、LNG 储备或双燃料能力，以及在入口压力需要时加装冗余增压压缩。气源品质同样重要：甲烷值、热值和沃贝指数（Wobbe index）一旦漂出发动机的燃料包络，就可能迫使控制参数调整或降额运行。

几个大型项目的例子：

- 在得克萨斯州建管道，只需要对得州铁路委员会（Texas Railroad Commission）一家交代，这意味着该州的数据中心开发商越来越多地自己动手建管道。联邦涉水许可与地役权仍然适用，而纯私有支线没有强制征地权（condemnation），一个「钉子户」就能迫使改线。Crusoe 自行为通往 Abilene Duroc 电厂的 16 英寸管线提出申请；Trailblazer Infrastructure——Sweetwater 的开发商，与 Tallgrass 的 Trailblazer 系统无关——在其税收增量融资计划中为一条 31 英里延长线编列了 $120M（1.2 亿美元）预算。再加上 ERCOT 的接入规则和全美最便宜的天然气，你就得到了为什么这么多建设规划落在得州的又一层解释。
- 在路易斯安那州，Energy Transfer 旗下 ETC Tiger Pipeline 正在建设 Franklin Farms 支线——13.2 英里 36 英寸管道、日输量十亿立方英尺，外加一条较短分支——为 Entergy Louisiana 的新联合循环电厂供气，再由这些电厂经电网为 Meta 的 Hyperion 园区供电。托运方是 Entergy 而非 Meta，所以这是公用事业服务路线，而非表后路线。即便不设增压，从 2026 年 7 月联邦申报到 2028 年 2 月投用也要 19 个月。
- 新墨西哥州。我们又回到 Oracle 的 Project Jupiter。该园区将由 Transwestern 建设的 Green Chile 管道供气。这条管道按合同应于今年 8 月 15 日投用，但日期已过，连路由都未获批，更别说开工铺管。8 月 14 日，Transwestern 申报了新的投用日期——2027 年 2 月 1 日，联邦机构此次推进得出奇地快。若要赶上明年 2 月的投产日期，这种速度必须保持下去，未来两个月内就需要 FERC 下达命令。有记录以来没有一张同类证书以这种速度发放，我们追踪的 33 个可比项目中，也没有一个在公众意见期结束前获批。我们估计 2027 年 4 月或 5 月首通气，2028 年年中爬坡至满负荷 2.45 GW，但在此之前还有几道坎要过。

燃料合同与管道申报也能帮助去芜存菁。一条邻近管道说明不了什么，但一份确定运输合同、一份已签署的供气协议，或一份已向监管机构递交的管道申请，有助于判断哪些场站正在真正走向通气。

一些有意思的观察：

- Energy Transfer 向 Nexus Hubbard 园区供气 150 MMcf/d，足够支撑实际已订购往复式发动机中的约 750 MW。但该园区待批的空气许可覆盖 5,230MW 机组，意味着所需气量约为已签约供气量的七倍——要么还有更多气合同在路上，要么许可是先于气源锁定的一种对冲。
- Liberty Energy 与 PowerBridge 的合资项目覆盖西得州一个规划 2 GW 的园区，一期超过 300 MW 发电容量目标 2027 年第四季度。Liberty 于 2026 年 7 月 22 日告诉投资者，该场站将以表后模式起步（很可能在 ERCOT 的 Batch Zero 之列），并可能在 2028 年接受一个规模未定的电网连接。届时园区大部分将位于一个私用网络之后——即 ERCOT 那种在单一连接点把场站发电与其负荷相抵的结构，我们在《[US Grid Constraints](https://newsletter.semianalysis.com/p/us-grid-constraints-towards-40gw)》中有详解。

## **阶段 3：设备**

今年以来，燃气轮机、往复式发动机及其他发电设备市场显著增长：新制造商不断入局，现有 OEM 也在扩充产能，以跟上现场发电需求的增长。

我们在《[现场燃气深度解析](https://newsletter.semianalysis.com/p/how-ai-labs-are-solving-the-power)》中梳理过新技术类型与在位制造商，数据中心运营商可选的各类设备可在该文中查阅。

自 2025 年 12 月 30 日那篇文章以来，三大类别没有变化：

1. 燃气轮机（GT）：

   1. 工业燃气轮机（IGT）：数十兆瓦级、更小更重的机型；
   2. 航改式燃气轮机（aero）：喷气发动机改装用于发电，30 至 115 MW 区间，5 至 8 分钟内可完成爬载；以及
   3. 重型框架式燃气轮机：约 400 MW，与汽轮机组成联合循环后燃料效率更高。
2. 往复式内燃机（RICE），或称「recips」：

   1. 高速发动机（1,500 至 1,800 rpm）：单机约 0.5 至 4.5 MW，如 INNIO 的 Jenbacher Type 6 和 Caterpillar 的 G3520；以及
   2. 中速发动机（500 至 1,000 rpm）：约 5 至 20 MW，如 Wärtsilä 的 34SG、31SG 与 50SG，INNIO 的 J920，以及 Everllence 的 51/60G。
3. 燃料电池：Bloom Energy 的固体氧化物机型拿走了几乎所有订单（追踪口径下燃料电池订单中 Bloom 为 3.8 GW，FuelCell Energy 仅 0.03 GW）。

虽然燃气轮机拿下了早期大部分订单，但很快就销售一空，最早的档期已排到 2030 年之后。原因在于 BTM 开发商要与公用事业公司争抢轮机档期。相比之下，往复式发动机在公用事业那里远没那么抢手，其供应商越来越像 AI 算力的「纯玩家」。正因如此，我们按季度追踪的 BTM AI 算力确定订单出现了向 recips 的剧烈倾斜。

![](https://substack-post-media.s3.amazonaws.com/public/images/cda4ece6-66ad-4da3-9f3d-53b3561414f3_2430x1296.png)
*资料来源：SemiAnalysis Energy Model；sales@semianalysis.com*

而且我们预计这一趋势将持续。EROCK、FTAI Power、Dynamis，连同 INNIO、Wärtsilä、Caterpillar、Cummins 以及 Bloom Energy，正以比 GEV 等在位者更激进的力度扩产，并把更多供应导向数据中心市场。Caterpillar 正把大型往复式发动机产量提升至 2024 年水平的近 3 倍；INNIO 预计总产能从 2025 年的每年 3.5 GW 大致增至 2030 年的每年约 10 GW。

我们还看到轮机二级市场的出现。不过可不便宜！主流 OEM 的普遍缺货，催生了一个用溢价换时间的二级市场。一个被释放的交付档期相对工厂新订单存在实质性溢价——最清晰的公开标杆是一笔档位转让按固定价上浮 16% 成交，计入全部成本后溢价达 46%——溢价买到的是未来一两年（或更早）而非未来五年的档期交付，以及更快的送电。

![](https://substack-post-media.s3.amazonaws.com/public/images/1cdf21bb-752b-410d-9086-a6132a285da3_2430x1296.png)
*资料来源：SemiAnalysis Energy Model；sales@semianalysis.com*

这个二级市场的关键，在于供应链中投机性订单的存在。一些人承诺购买轮机或签署最低采购协议、支付定金，却并没有实际的数据中心场址可供部署。我们看到这种行为主要影响燃气轮机市场，尤其是 GEV 和 Siemens 两大在位者。这些设备如今依然紧俏、需求旺盛，鉴于上文讨论的二级市场价格，一些「投机者」已经赚得盆满钵满。

![Image preview](https://substack-post-media.s3.amazonaws.com/public/images/534453fc-ef33-4217-a16f-9db5d10049b3_2700x1440.png)
*资料来源：SemiAnalysis Energy Model；sales@semianalysis.com*

### 没有配套系统（BoP），就没有 BTM 电厂

谈到 BTM 瓶颈时，发电设备通常是对话的中心，但我们认为焦点正日益转向电厂配套系统（BoP）。如果园区要苦等变压器、中压开关柜或容纳电气设备的 e-house，发电设备再好也无用。集电系统与控制系统还必须把整群机组的出力汇成一座可运转的电厂。而这类电气设备——通常中压、有时高压（视电厂规模与系统设计而定）——由于标准化程度高、且常被数据中心用作自身电气系统的一部分，正处于极高需求之中（[参见我们就此主题的深度解析](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical)）。

![](https://substack-post-media.s3.amazonaws.com/public/images/7aac63d0-204b-4562-8b7b-8d56d9a49cc0_2116x3064.png)
*资料来源：SemiAnalysis Datacenter Model；SemiAnalysis Energy Model；Sales@semianalysis.com*

### **阶段 4：建设、调试与劳动力**

资金、许可、天然气和设备一旦解决，另一重挑战便浮出水面。建设电厂并按合同规定的 SLA 标准运营，需要高素质的劳动力、承包商与 EPC。需要说明的是，把这一切称作「科学实验」的人完全忽视了：已有 3GW 数据中心 IT 容量正由表后电厂供电运行。我们的数据中心模型与能源模型追踪每一个项目及其精确时间表和供应链。

![Image preview](https://substack-post-media.s3.amazonaws.com/public/images/2906ff1c-b475-4668-a38f-de6d96871268_2700x1440.png)
*资料来源：SemiAnalysis Energy Model；sales@semianalysis.com*

但随着规模急剧扩大，问题终将出现，尤其是在数据中心建设潮导致劳动力稀缺加剧的背景下。

我们在《[乐高数据中心的狂野西部](https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters)》（The Wild Wild West of LEGO Datacenters）中的劳动力市场建模——基于[工业模型](https://semianalysis.com/industrials-model/)所含劳动力模型——测得 2027 年缺口为 288,000 名工人。电工是最大的工种，约占现场工时的 30%，且随着液冷增加机械工作量，到 2030 年将趋向 40%。

把机械和电气工作搬进工厂，可使现场劳动力减少约 63%、现场持证电工工时减少约 85%——这正是预制 eHouse、橇装电厂和整体模块化方案在供应商名单中普及的原因：它们既是劳动力套利，也是抢跑工期、超前进度的机会。

但现场仍需要大量劳动力。就电厂而言，美国已建了几十年，劳动力供给池健康，成本也低于数据中心建设。大型联合循环燃气电厂的峰值用工商约为每兆瓦半个建筑工人：

- 加州 Palomar，546MW，峰值 283 名技工；
- 俄亥俄州 Guernsey，1,875MW，十五年后峰值接近 1,000 名；

因此，在吉瓦级园区，电厂建设的峰值人数可能只占园区峰值用工的五分之一到四分之一。

然而，***这批劳动力并不通用。*** 联合循环（CCGT）电厂是机械承压工程：锅炉制造工安装余热锅炉（HRSG）承压部件，管道焊工的焊缝必须通过射线检测，机械安装工（millwright）要把轮机对中到千分位。**全美只有 10,200 名锅炉制造工，该职业每年流失约 800 人，且劳工统计局预计其规模还将萎缩。**

话虽如此，BTM 建设将采用多种方案，每种发电类型依赖不同工种，在劳动力问题上各有优劣。

- 往复式发动机不需要锅炉制造工，但依赖电工和机械安装工，因此电厂会与自己的数据中心抢同一批人。
- 燃料电池不需要任何稀缺工种：没有承压部件，在劳动力受限的建设中这是强有力的论据。但在多吉瓦规模下，数百组燃料电池阵列加上所需的超级电容、BESS 等，构成了一种从未大规模实践过的配置形态。

这正是「省劳力」电源方案对终端客户吸引力与日俱增的原因。随着[美国电网在 2028 年耗尽电力与富余容量](https://newsletter.semianalysis.com/p/us-grid-constraints-towards-40gw)，这些方案将成为解决数据中心电力约束的主要途径。

当然，调试不是终点。一个永久孤岛需要日常运行值守、远程监测、本地响应、计划性维护、备件与突发工况的服务保障。节奏以运行小时数计。Caterpillar 给出的参考是 20,000 小时顶部大修、80,000 小时大修；Jenbacher 机组可能在 60,000 或 80,000 小时需要大修。按每年 8,000 运行小时计，Caterpillar 顶部大修约 2.5 年一次，大修约 7.5–10 年一次。确切答案因发动机与负载循环而异。

为对冲这两大问题，一些 OEM 日益走向垂直化。Bloom Energy 是主要例子，因为其方案当然不像轮机和发动机那样广泛建立。Bloom 为其部署承担大部分安装与运维（O&M）工作，并自聘、自训人员来完成。其他厂商也在跟进，这两个问题正日益成为设备订单的决定性因素。EROCK 也依赖这一模式，其采用的较小排量卡车衍生发动机，使安装和运维都远比传统轮机电厂简单。PROENERGY 也披露拥有庞大的自有员工队伍，必要时可充当 EPC 与运维方。

### **阶段 5：孤岛运行的物理学**

最后一关最不显眼，也最不容犯错。在 xAI 的 Colossus 1，让燃气轮机追踪 GPU 负载被证明比预期更难：每秒数次 10 至 20MW 的功率抖动，而这类振荡会激发扭振模式，吞噬轮机-发电机轴的寿命。这一问题促使 xAI 部署了第一期的 150MW Tesla Megapack。我们已就[吉瓦级 AI 训练负载波动及其电网停电风险](https://newsletter.semianalysis.com/p/ai-training-load-fluctuations-at-gigawatt-scale-risk-of-power-grid-blackout)撰文详述。由此引发了一场新的争夺战：BESS 对阵飞轮/同步调相机（SynCon），竞争与 BTM 场站发电设备搭档的位置。

![Image preview](https://substack-post-media.s3.amazonaws.com/public/images/da0e5956-feb0-476e-ba96-bb953f701e58_2700x1440.png)
*资料来源：SemiAnalysis Energy Model；sales@semianalysis.com*

让现代燃气轮机能够通过许可的燃烧室技术，只有在约半数额定负荷以上（加装负荷下探升级后约 35% 以上）才能保持排放性能。AI 训练负载摆动剧烈而迅速，可能把轮机压到这条底线以下——此时控制系统会追加引燃燃料或回退到扩散燃烧模式，NOx、CO 和未燃碳氢化合物全面跳升。许可是按潜在排放量撰写的，因此这条底线会被写进申请。

并网电厂从系统「借」用两项服务：一是惯量——抵抗频率变化的旋转质量；二是故障电流——让断路器识别短路并跳闸的涌流。孤岛电厂必须两者自给。发动机和轮机可向故障点输出五到十倍额定电流；电池、光伏和燃料电池则被电力电子钳制在约 1.2–2 倍，薄到常规过流保护失去裕度。一座纯逆变器搭建的孤岛，可能无法切除自身的短路故障。

燃料电池用超级电容回答同一问题：超级电容向阶跃负载瞬间放电，并随电堆爬载再充电。我们对 Bloom 配比的渠道调研显示，按功率计接近 3:2——照此推算，Project Jupiter 的 2.45GW 意味着约 1.6GW 超级电容，远超现有 58MW 的先例。

### **不用天然气能做到吗？**

很多人在尝试。历经六重难关之后，你很可能会想：可再生能源或许能绕开许可、燃料和供应链瓶颈。已有先行者，尤其是 Crusoe 携手 Redwood。Google 等也在超大规模部署可再生能源与 BESS，但这些场站仍保持并网。

可再生能源过空气许可容易得多：没有燃烧源需要许可，燃料零成本，也没有管道需要铺设。但难点在电气物理。离网环境下，一切都经逆变器连接。逆变器型电源向短路点只能输出额定电流的很小倍数——仅为发动机或轮机的一小部分——常规过流保护可靠跳闸的裕度不足。因此，一个清洁的可再生孤岛必须购置构网型逆变器加同步调相机。

我们 2025 年 12 月的现场燃气一文测得美国电网平均可用率约 99.93%，即大约三个 9，并证明现场电源必须超额配置才能与之匹配。

Crusoe 与 Redwood Materials 在内华达州 Sparks 运营中的数据中心微电网，自 2025 年 6 月起依靠 12 MW 光伏和 63 MWh 梯次利用电动汽车电池运行，电网作后备。在 2026 年 3 月 24 日的公告中，Crusoe 报告连续七个月运行可用率 99.2%，并宣布扩建至 20 MW。把光伏加电池的设计放大到吉瓦级园区，需要可观的发电容量、储能与土地；具体数量取决于负载曲线、气候、可靠性目标以及电网后备的可用性。电池在燃气项目里自有其位置：渡越（ride-through）、负载平滑与备用能量。Liberty Energy 首席财务官在 2026 年 7 月 23 日表示，其数据中心客户的电池功率容量平均为燃气容量的 50%。

买方对中断的容忍度正在提高。Microsoft 表示，其 Fairwater Atlanta 场址正是因为公用事业电力有韧性而入选，并且「能够以三个 9 的成本实现 4x9 的可用性」——即以 99.9% 可用率的成本拿到 99.99% 的可用率——这使其可以为 GPU 集群省去现场发电、不间断电源（UPS）系统和双路供电配电（Scott Guthrie，Microsoft，2025 年 11 月 12 日）。在我们的工业模型中，基于逐设备自下而上的物料清单（BoM），我们追踪 30 余种不同数据中心设计的预期可用率。我们追踪 Anthropic、OpenAI、Meta 及其他所有超大规模云厂商的设计，看到了向更低冗余演进的清晰趋势。

目前，没有任何一条路线能同时闯过全部六关：燃气卡在许可和承压工种（锅炉制造工与管道焊工）上，燃料电池卡在稳定性投入与未经验证的规模上，光伏加电池则卡在孤岛本身。

## **接下来路在何方？**

**下面我们讨论长期展望与赢家输家。我们将给出对 BTM 电厂的展望：它们是否注定全部转为并网，以及太阳能与电池在其中如何定位。**

**我们还将讨论 OEM 市场与 BoP 市场的赢家与输家。一些重大的行业变化对某些大型工业企业不利，但其业务组合内部也存在对冲因素。**
