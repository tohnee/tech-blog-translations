---
title: "吉瓦级 AI 训练负载波动：电网大停电风险几何？"
title_en: "AI Training Load Fluctuations at Gigawatt-scale - Risk of Power Grid Blackout?"
subtitle: "108GW 大负载并网队列、Tesla Megapack、超级电容、吉瓦级电池、PyTorch「防止电厂被炸」开关"
date: 2025-06-25
source: https://newsletter.semianalysis.com/p/ai-training-load-fluctuations-at-gigawatt-scale-risk-of-power-grid-blackout
crawled: 2026-09-15
authors: ["Jeremie Eliahou Ontiveros", "Dylan Patel", "Ajey Pandey"]
tags: ["Datacenter"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 吉瓦级 AI 训练负载波动：电网大停电风险几何？

> 原文：[AI Training Load Fluctuations at Gigawatt-scale - Risk of Power Grid Blackout?](https://newsletter.semianalysis.com/p/ai-training-load-fluctuations-at-gigawatt-scale-risk-of-power-grid-blackout) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**108GW 大负载并网队列、Tesla Megapack、超级电容、吉瓦级电池、PyTorch「防止电厂被炸」开关**

最大的几家 AI 实验室正竞相建设数吉瓦级的数据中心，让我们这套拥有百年历史的电网承受到前所未有的压力。规模巨大只是其一，更关键的是，**AI 训练负载的负载特性（load profile）极其独特**：在几分之一秒内，负载会在满载与近乎空载之间意外地大起大落。我们的电网从来就不是为这种模式设计的。到了吉瓦级规模，最坏情形就是**数百万美国人大停电**。

这个问题让头部 AI 实验室也措手不及。[Meta 的 LLaMa 3 论文](https://arxiv.org/pdf/2407.21783)就提到了功率波动带来的挑战，而那「仅仅」是一个 24,000 卡 H100 集群（IT 容量 30MW）。

> 训练期间，数以万计的 GPU 可能同时增加或减少功耗，例如所有 GPU 都在等待检查点（checkpointing）或集合通信完成，或者整个训练任务启动或关闭的时候。一旦发生这种情况，整个数据中心的功耗可能出现数十兆瓦量级的瞬时波动，将电网的承受能力拉到极限。随着我们为未来更大规模的 Llama 模型扩展训练，这仍是我们持续面临的挑战。

迫于无奈，工程师们造出了 **“pytorch_no_powerplant_blowup=1”** 这个命令，用生成假负载的方式来抹平功率抽取曲线。但到了吉瓦级规模，这类假负载每年浪费的电费累计可达数千万美元！硬件厂商们随即排着队拿出正经的解决方案。

在孟菲斯，xAI 的「Colossus」选择了 Tesla 的 Megapack 系统。马斯克这家以造车起家的公司目前领跑电池储能系统（BESS）市场，并且正在积极接触公用事业公司和数据中心运营商，想把自己的方案变成行业标准。Tesla 真的会吃下这个市场吗？抑或是在 BESS 之外，还有靠得住的替代方案来应对 AI 训练负载波动？

- ![](https://substack-post-media.s3.amazonaws.com/public/images/1067945f-e020-47de-8eaa-63537c439aa0_1024x415.png)
- ![](https://substack-post-media.s3.amazonaws.com/public/images/0e874a32-c372-44b4-a05a-b8e03bfc7464_1024x511.png)

*来源：Tesla*

为了理解市场层面的影响，我们从第一性原理出发，解释电能质量为何重要，以及电网设计的一些基本考量。随后我们剖析 AI 训练与推理的负载特性，并将其与传统负载对比，摆清楚一个吉瓦级 AI 训练数据中心可能如何触发大停电。接着我们逐一检视解决方案——从超级电容到 UPS 再到电池储能系统（BESS）——并找出最可能的赢家。[我们的逐项目数据中心预测](https://www.semianalysis.com/p/datacenter-model)让我们得以提前看清接下来的走势，我们认为有几家公司注定会获得不成比例的收益。

*SemiAnalysis 将从下周开始在 [Instagram Reels](http://instagram.com/semianalysis) 和 [TikTok](https://www.tiktok.com/@semianalysis) 发布独家内容。欢迎关注我们的社交媒体，获取 AI 与 GPU 产业的最新洞见。*

## **电能质量，简述**

**电能质量**（power quality）这个词从未进入大众词汇，这本身就是公用事业工程师专业能力最好的证明。大多数读者只是随手按下开关，就笃定灯光不会闪烁、电器不会烧毁、断路器不会跳闸。但这份底气，建立在**以几分之一秒为尺度让发电与电力负载实时平衡**的基础之上。

电网的几乎每个环节——火电厂、核电站、变压器、高压线路——都运行在**交流电（AC）**之上。在交流电力系统中，**电压**和**电流**以一个受到严格管控、随地区而定的频率振荡：北美为 60 Hz（每秒 60 个周期），欧洲和亚洲为 50 Hz。居民负载通常只用一条振荡线路，但数据中心这类工业负载通常接入**三相**电：每路电源线实际上是三根导线，三个振荡周期彼此错开运行。

![](https://substack-post-media.s3.amazonaws.com/public/images/543d34a1-2c27-4db2-8152-a22ea233dd28_1618x1232.png)
*来源：维基百科「三相电」词条*

然而，电压和频率是电能十分脆弱的属性。一旦电力供需不能紧密匹配，电压和频率都会偏离设定值。供给超过需求时，电压和频率会升破基线；供给*低于*需求时，电压和频率则跌破基线。仅仅 10% 的摆动就足以烧毁电动机、触发断路器跳闸、令电子设备宕机，而电网运营商的职责就是守住**电能质量**的门槛。

2021 年冬天的得州寒潮印证了这一点。极寒天气令采暖需求飙升，多座大型燃气电厂被迫停机。供给掉队，系统频率随之跌破 59.4 Hz。在 ERCOT（得州电网）的规则下，频率低于 59.4 Hz 持续九分钟就会触发保护性跳闸，令全州陷入**持续多日、造成持久损害的大停电**。

为了保住电网不垮，ERCOT 对家庭和企业拉闸限电，把需求一路砍到与残缺的供给相匹配为止。

![](https://substack-post-media.s3.amazonaws.com/public/images/c65ca665-11bd-40c8-9f07-9eb76980864f_2314x1198.png)
*来源：Practical Engineering*

这凸显了电网稳定如何依赖供需之间的稳定平衡，以及失衡带来的风险。幸运的是，居民用电需求相当可预测，而电炉钢制造、芯片厂和云数据中心这类大负载抽取的通常也是平稳的负载。GenAI 的崛起彻底改写了这套剧本。

## **AI 负载特性深度剖析**

AI 计算系统通常是同步运行的。一次大型 GPU 训练可能动辄数十万块 GPU 协同、同步地工作。基础概念我们在[这里](https://semianalysis.com/2024/09/04/multi-datacenter-training-openais/#multi-datacenter-distributed-training)讲过。这种模式与传统计算负载特性格格不入：

- 云计算是把大量虚拟机卖给大量用户的生意——每个用户的使用场景千差万别。一些大客户可能租下数千台 VM，但即便如此，它们的负载特性总体仍是异构的。别忘了，一个 100MW 的数据中心可以容纳数百万个 CPU 核心（以及 VM）。
- 传统推理负载，比如 Meta 的 DLRM（AdRec、信息流排序等），通常由多个小模型组成，每个模型的算力需求都不大。最终结果是一种非同步的模式。

下面这张 Google Cloud 发布的图表显示，云数据中心与 AI 数据中心的负载波动相差约 15 倍——从 1.5 MW 到 15MW。

![](https://substack-post-media.s3.amazonaws.com/public/images/b2a584d4-b5c9-4618-a273-1247a6dc9568_2326x798.png)
*来源：Google 在 OCP EMEA Summit 2025 上的分享，SemiAnalysis*

### **大规模训练集群**

在大型 AI 训练数据中心的语境下最容易理解这一点：那里多达数十万块 GPU 联网组成一台超级计算机。更多细节可阅读[我们关于 100k H100 集群网络架构的深度解析](https://semianalysis.com/2024/06/17/100000-h100-clusters-power-network/)。造成 AI 训练负载剧烈波动的原因有很多，例如：

- 批内尖峰与凹陷（毫秒级）：处理一个 batch 的过程中，矩阵计算阶段功率飙升，数据搬运和同步等较轻的操作阶段功率回落。
- 检查点写入/恢复（毫秒级）：写检查点期间负载可能骤降至接近零，通常持续几毫秒。
- 同步（最长数秒）：随着集群规模扩大到数十万卡，AllReduce 操作常受网络问题困扰，有时会导致 GPU 计算空转长达数秒。
- 一次训练收尾：超大规模训练结束后，如果没有下一个负载立刻让 GPU 满功率运转，就会带来巨大的负载落差。

以上并未穷尽所有原因，而且要说清楚：其中不少可以通过软件修改以及负载与集群管理的优化来部分缓解。但问题依然存在，AI 训练负载在这方面确实非常独特。我们需要的是**基于硬件的解决方案**。

下面的论文展示了一次训练运行的实测结果。

![](https://substack-post-media.s3.amazonaws.com/public/images/aa92e862-f85e-46ed-9115-5c52867f3d0a_1664x1264.png)
*来源：《AI Load Dynamics–A Power Electronics Perspective》*

### **推理负载**

来自 Google、Meta、TikTok 等公司的大规模推理部署（DLRM）的实证经验表明，推理侧的问题远没有训练侧突出。但 GenAI 又一次带来了全新的动态：

- 预填充（prefill）与解码（decode）：每个 LLM 查询都有两个截然不同的阶段。前者的计算量（FLOPS）通常远高于后者，这意味着 GPU 在 prefill 阶段满功率运行，而 decode 阶段往往不到 50%。现代的 prefill 与 decode 分离（disaggregated）技术可以缓解这一问题。
- 节点间通信停顿：高批处理（batching）对于有利润地服务数百万用户至关重要，而在 SOTA 推理模型的语境下往往需要大量节点。此时推理负载就开始更像训练了。

关于第二点，最好的例子是 DeepSeek 极为独特的推理部署——用很小的 GPU 资源高效服务数百万用户——[我们在 Core Research 中向订阅客户做过深度讲解](https://semianalysis.com/core-research/)。

![](https://substack-post-media.s3.amazonaws.com/public/images/7b37f17d-f79f-4437-9340-966e44b7baa7_1716x1300.png)
*来源：《AI Load Dynamics–A Power Electronics Perspective》*

推理和训练都存在负载波动问题，但训练负载要棘手得多，因为它涉及高达吉瓦级的系统同步运行。不过，考虑到 [Scaling Laws](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/) 与 [强化学习](https://semianalysis.com/2025/06/08/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data/) 的演进趋势，我们认为推理负载也将越来越多地依赖大规模横向扩展集群——这同样会带来问题，只是程度不同。

## **电网冲击——AI 数据中心正在涌入电网**

要理解问题的量级和潜在风险，我们先退后一步，看看当今最大 AI 数据中心的规模。下面展示的是 OpenAI 的一个主力训练集群。**这栋楼就是当今世界最大的单体建筑**（[与威斯康星的一座「姊妹」站点并列](https://semianalysis.com/datacenter-industry-model/)），IT 容量约 300MW、额定容量约 400MW，遥遥领先第二名。对于我们数据中心解剖系列报告（[制冷系统](https://semianalysis.com/2025/02/13/datacenter-anatomy-part-2-cooling-systems/)与[电气系统](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/)）的读者来说，规模一目了然——光是 210 台风冷冷水机组和现场那座巨型变电站就足以说明问题。

自 2025 年 1 月起，第二栋一模一样的建筑已开工建设，将在 2026 年年中把整个园区推向吉瓦级。

![](https://substack-post-media.s3.amazonaws.com/public/images/10bda619-24b8-4810-ae1b-ff1959e1f5ff_2271x1374.png)
*来源：SemiAnalysis 数据中心模型*

这引起了 ERCOT（得州电力可靠性委员会）的注意——该机构负责监管得州电网。下面这张图一目了然：**超过 108GW 的「大负载」正在申请接入 ERCOT**，其中大多数是数据中心。作为参照，美国全国的峰值负载也才 745GW！

需要说明的是，全世界的数据中心负载排队清单里都充满重复申请，ERCOT 也不例外。108GW 这个数字并不现实（[它的数据中心负载预测同样不现实](https://semianalysis.com/datacenter-industry-model/)）。SemiAnalysis 未来的报告会更深入地探讨这个话题，相关数据已在我们数据中心模型中提供。

![](https://substack-post-media.s3.amazonaws.com/public/images/79a09674-cb14-40eb-a4c9-67c7ec9b93f2_2048x1218.png)
*来源：ERCOT*

NERC（北美电力可靠性公司）——覆盖整个北美的监管机构——同样表示关切，并正在质询各主要输电公用事业公司在开展并网研究时如何对数据中心负载建模。我们深挖了这些研究报告、监管备案文件、ERCOT 会议材料等，以便更准确地把握问题的量级。下面逐一拆解。

### **问题一：管理快速功率波动**

负载开停导致电力需求随时间变化并不是新鲜事，几十年来一直靠供给侧在秒级尺度上同步调节来管理。但在几分之一秒内管理数百兆瓦的功率变化，对运营商来说是一场前所未有的挑战。而这恰恰就是吉瓦级 AI 数据中心带来的威胁。

供给侧调节通常是指启停发电机，或指挥发电机向上或向下**爬升**出力。发电机的**爬升速率**以**每分钟兆瓦**（MW/min）计，例如一台爬升速率为 10 MW/min 的发电机可以在 10 分钟内增减 100MW 出力。化石燃料发电机组的爬升速率在 5-50 MW/分钟之间，而核电站的爬升速率太慢，无法对任何电网状况作出响应。

传统上，亚秒级的电压与频率平衡依靠系统**惯量**来打理。由于传统发电机本质上是一块巨大的旋转磁体，这些旋转质量固有的动量可以吸收电力供需之间的小幅失衡，代价是多余的热量和更低的运行效率。

![](https://substack-post-media.s3.amazonaws.com/public/images/d6aee200-8ace-42b6-8e90-d7a0a8920fab_2094x1194.png)
*来源：《Balancing the Grid：POSOCO 电力系统惯量评估报告》*

发电结构的变化正使这一点日益受到挑战。越来越多的电力来自**间歇性可再生**能源，尤其是风电和光伏。这些系统并不产生与电网其余部分同步的交流电，而是发出**直流电（DC）**，再通过**逆变器**转换为交流电。

由于这些逆变器并非围绕大型旋转质量构建，它们不具备*被动*补偿供需失衡所需的惯量，而供需失衡正是电压和频率漂移的根源。同时，由于这些间歇性可再生能源的发电依赖天气条件，除非搭配电池，否则它们无法像化石燃料发电机那样按 MW/min 的爬升速率被调度。如今也有更新颖的电能质量管理工具，包括专用电能质量设备，如电容器组、同步调相机、静止无功补偿器（SVC）以及静止同步补偿器（STATCOM）。

### **问题二：连锁大停电风险**

尽管 ERCOT 对电能质量问题着墨颇多，但他们的会议记录显示，还有一个更大的担忧：连锁大停电。

#### **低电压穿越（LVRT），简述**

ERCOT 特别考虑了一种与数据中心相关的故障响应：**低电压穿越（LVRT）**。低电压穿越应对的并非完全断电，而是一种**瞬时**闪变——输入电压可能骤降，例如跌破基线 30%，持续 30 毫秒到 5 秒不等。这种断电形态对应的是远处一台**重合器**清除**故障**时的标准动作。某种意义上，重合器就是能自动「重新合闸」的断路器。重合器一旦检测到问题，就会跳闸，等待一段预设时间，然后重新合闸。

![](https://substack-post-media.s3.amazonaws.com/public/images/aa076d8f-27e0-4ed8-89cf-62eedc4cd786_700x486.png)
*来源：Tavrida Electric*

通常，重合器会把「跳闸—等待—重合—再跳闸」的循环执行两三次，之后才永久跳闸。这种重复对清除野生动物引发的问题尤其重要。电力故障最常见的肇因就是鸟类、松鼠和树木。这些动物往往以错误的方式触碰电力线路，造成短路。重合器复位时的电击真的可以把障碍物从电线上「电」下来，从而无需线路抢修队开车到场处理就能清除故障。当然，经历这一系列事件之后，动物们是真的出问题了。

如果故障发生在直接给数据中心供电的线路上，数据中心只会短暂经历一次断电。然而，电网是一个深度互联的系统，别的线路上的故障会以电压骤降的形式在电网中激起冲击波。在一次 LVRT 事件中，数据中心会因那处远方故障而看到电压跌落，待远处重合器跳闸后电压又会恢复。如果重合器一次重合就成功，数据中心不会再看到任何电压凹陷。但如果重合器循环几次才清除故障或最终放弃，数据中心就可能接连经历几次电压骤降。LVRT 的难点在于保持在线、「扛过」这波低压闪变，同时不与电网解列。

![](https://substack-post-media.s3.amazonaws.com/public/images/7898a395-a55c-4c6a-aacc-fea1fa6fef00_1817x987.png)
*来源：《Low-Voltage Ride-Through Operation of Grid-Connected Microgrid Using Consensus-Based Distributed Control》*

数据中心通常用**不间断电源（UPS）**和备用发电来应对 LVRT。[我们的数据中心解剖——电气系统报告](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/#generators-medium-voltage-transformers-and-power-distribution)详细讲解了数据中心内的电力流向和相关设备。一旦电网电压凹陷，UPS 可以近乎瞬时地作出反应，把数据中心从电网供电切换到电池储能供电（通常可维持五分钟运行）。这种切换足够平滑，不会迫使电子设备关机。若电网电压恢复，UPS 可以让数据中心重新并网。然而，如果 UPS 连续检测到多次电压骤降——比如重合器反复循环清除故障的那种情形——UPS 就可能与电网永久解列，并把数据中心切换到备用发电（通常是柴油发电机）。

对数据中心自身而言，切换到备用电源没什么问题——柴油备用燃料虽然贵，但「电网 → UPS → 备用发电机」的两次切换*并不会中断运营*。然而，这种切换操作会给整个电网带来严重问题：它会在一瞬间把数百兆瓦乃至吉瓦级的电力需求从电网上摘掉。这反过来造成电力供需的突然失衡，引发电压和频率波动，进而可能导致*其他*发电机或大负载跳闸离网，酿成**连锁电网失效**。

请注意，这并不是新问题。2024 年 7 月，一条故障输电线路导致弗吉尼亚州 1.5GW 的数据中心意外离网并启动备用电源。Dominion Energy 最终成功化解，没有酿成大停电，但为此采取了非常极端的措施。然而，[考虑到美国即将迎来的负载增长](https://www.semianalysis.com/p/ai-datacenter-energy-dilemma-race)，再加上前述的 AI 训练负载特性，弗吉尼亚事件可能会变得司空见惯。

![](https://substack-post-media.s3.amazonaws.com/public/images/ccec8c77-f8d2-4921-ac16-27f592a2fc24_1935x794.png)
*来源：北美电力可靠性公司（NERC）*

### **噩梦场景之一：数据中心离网风险**

2025 年 5 月的一次会议上，ERCOT 的两份报告描述了一个潜在的噩梦场景。

第一份来自 Yunzhi Cheng 的报告建立了一个模型，研究一次低电压穿越失败会在什么条件下击垮数据中心。模型将两种气象场景与两种故障响应场景交叉组合。

气象场景有两种：

- 夏季高峰（Summer Peak，SP）：得州全境电力负载最大化的时刻；热浪来袭第三天的傍晚。
- 高可再生占比最小负载（High Renewable Minimum Load，HRML）：得州全境呈**「鸭子曲线」**的电力负载；晴朗的春季或秋季正午，电力负载最低与表后太阳能出力最大的交汇点。

![](https://substack-post-media.s3.amazonaws.com/public/images/78fe2dff-f579-4381-9ba8-3a09be8ccd66_1200x1200.png)
*来源：Visual Capitalist*

故障响应场景有两种：

1. 数据中心在电压跌破基线 75% 时立即跳闸
2. 数据中心可承受 70% 电压、持续 20 毫秒的 LVRT，但电压再低或时间再长都不行。

Cheng 模拟了西得州一座变电站内一条 345kV 输电线路（约为供应得州奥斯汀所需电力的 1/6）上的故障。将两组场景组合，他基于四套可能的假设组合对故障结果进行了建模：

- 夏季高峰时发生故障，电压跌破基线 75% 即跳闸
- 夏季高峰时发生故障，可承受 70% 电压、20 毫秒的 LVRT
- 高可再生最小负载时发生故障，电压跌破基线 75% 即跳闸
- 高可再生最小负载时发生故障，可承受 70% 电压、20 毫秒的 LVRT

Cheng 发现，在全部四套假设下，ERCOT 电网系统都会有至少 1.5 GW 的数据中心负载几乎立即离网。如果故障发生在「鸭子曲线」日、且数据中心不具备 LVRT 能力，电网可能眼睁睁看着 2.5 GW 负载——即目前西得州的全部数据中心——几乎在同一时刻离网。请注意，西得州数据中心的负载很快就会飙过 10GW。

**基准情形下的数据中心离网风险**

![](https://substack-post-media.s3.amazonaws.com/public/images/b1db6fab-e1ed-4760-bd1c-1ba4c7919624_1970x486.png)
*来源：ERCOT*

在*西得州每一座数据中心*的并网点安装同步调相机（本质上是一个巨大的电磁飞轮）会有帮助，因为系统惯量被直接加到了每处负载身边。但即便采取这种对策，仍有 1.3-1.9 GW 的负载面临离网风险。

**数据中心离网风险 + 同步调相机**

![](https://substack-post-media.s3.amazonaws.com/public/images/98be74a3-04f9-450b-b64b-e7ae1bc28a8f_1698x420.png)
*来源：ERCOT*

更何况，同步调相机是非常昂贵的系统。这类系统的资本开支[约合每 MVA 无功容量 3 万至 6 万美元](https://market.us/report/synchronous-condenser-market/)。按 Cheng 模型采用的安装规格，一个 1 GW 数据中心需要花 1,000 万至 2,000 万美元来安装。

![](https://substack-post-media.s3.amazonaws.com/public/images/5af56019-8430-49e7-a3d7-3522aa7edc1b_1733x974.png)
*来源：维基百科「同步调相机」词条*

### **噩梦场景之二：连锁失效风险**

第二份来自 Luis Hinojosa 的报告则推演了这么多数据中心因一次瞬时故障而集体离网的连锁后果。他发现，如果一次有超过约 2.6 GW 的电力负载同时离网，整个 ERCOT 系统的电网频率将升破 ERCOT 动态工作组设定的 60.4 Hz「危险区」。

![](https://substack-post-media.s3.amazonaws.com/public/images/09cbc12b-9834-4cb3-9113-988bcf3f72cc_2208x962.png)
*来源：ERCOT*
![](https://substack-post-media.s3.amazonaws.com/public/images/260c07c1-22fb-4649-9c40-3f9ad74613e4_1136x586.png)
*来源：ERCOT*

即便是规模较小的 2 GW 离网，也会造成超出 ERCOT 安全容忍度的**频率变化率（ROCOF）**不稳定。

![](https://substack-post-media.s3.amazonaws.com/public/images/b8a89b25-c466-4ca9-8329-4ddc439b1c08_2310x1008.png)
*来源：ERCOT*
![](https://substack-post-media.s3.amazonaws.com/public/images/f30a0cd2-86f7-456a-820f-e641166fb550_1090x586.png)
*来源：ERCOT*

这一规模的离网还会危及电压质量：如果超过 2.5 GW 负载同时离网，得州电网的大片区域将出现破坏性的电压问题。

![](https://substack-post-media.s3.amazonaws.com/public/images/f232e9b4-f9c2-46ee-a578-eafcc96e9432_2062x604.png)
*来源：ERCOT*

Hinojosa 将研究结论汇总为两条负载损失的运行限值：如果整个 ERCOT 系统在短时间内损失 2.6 GW 负载，或西得州负载区损失 2.0 GW，得州电网就会处于危险的不稳定状态，面临连锁大停电的风险。

### **噩梦场景之三：这在伊比利亚半岛已经上演过**

Cheng 和 Hinojosa 的分析所勾勒的电网稳定性问题，揭示了一条与[2025 年 4 月 28 日伊比利亚半岛大停电](https://www.entsoe.eu/news/2025/05/09/entso-e-expert-panel-initiates-the-investigation-into-the-causes-of-iberian-blackout/)惊人相似的电网失稳路径。在那次事件中，2.2 GW 发电能力跳闸离网，据报道是因为[当地电网运营商的调度决策失误](https://www.reuters.com/business/energy/investigation-into-spains-april-28-blackout-shows-no-evidence-cyberattack-2025-06-17/)。这引发了连锁的电压与频率波动，导致西班牙和葡萄牙全境断路器纷纷跳闸。由于伊比利亚电网与欧洲大陆其余部分相对隔离，外部联络线无法稳住电网，最终在 27 秒内全盘崩溃。

同样的场景完全可能在得州上演：如果 2-2.5 GW 的数据中心负载在短时间内相继跳闸离网，类似的电压与频率波动就可能引发席卷全得州的连锁失效。而且，得州互联电网与其他电网之间*只有四条*联络线，这些外部连接对稳定电网的作用微乎其微。一旦这些失效开始在得州境内回响式扩散，再想挽救已经太迟。而这一切的导火索，可能只是西得州某座变电站附近，一只松鼠在错误的时间踩上了错误的电线。

## **如何避免噩梦场景——解决方案**

请注意，**恶化系统级电能质量的责任主要由数据中心一方承担**——如果数据中心造成谐波问题，账单就得由它来付。这自然促使全行业积极寻找解决方案。

下文我们先讨论电池储能系统（BESS）；面向订阅用户的部分，我们将讨论其他基于硬件的解决方案及其相关供应商，以及它们如何与 Nvidia 全新的 800V 直流供电架构相契合。

## **电池储能系统（BESS）的前景**

Tesla 相信，解决数据中心电能质量问题的最佳方案是数百兆瓦乃至吉瓦级的大规模电池。在 2025 年 5 月的 ERCOT 会议上，Tesla 展示了一份幻灯片，内容与它 2025 年 4 月在北美电力可靠性委员会（NERC）主办的更大规模大负载研讨会上的演示几乎一致（[演示材料见此](https://www.nerc.com/comm/RSTC/LLTF/LLTF_April_Meeting_&_Technical_Workshop_Presentations_.pdf)）。该幻灯片聚焦其 Megapack 2 XL 电池，如下所示。

![](https://substack-post-media.s3.amazonaws.com/public/images/98e2ea13-8dd9-4f10-a880-961aa88c659d_1971x1071.png)
*来源：Tesla*

这份材料展示了**电池储能系统（BESS）**在数据中心的应用前景，与制造商无关。BESS 在数据中心的杀手级特性在于：这些系统可以在数秒内以数百兆瓦的功率充电或放电，使电池既能以恰当的反应速度、又能以足够的功率输出应对数据中心负载波动。

### **用于电能质量与电网稳定的 BESS**

一套接入逆变器的兆瓦级电池可以通过快速充放电来管理电能质量问题，这被称为**快速频率响应**。

![](https://substack-post-media.s3.amazonaws.com/public/images/e5f2b4d1-f231-43be-91b2-6d6bc575e2b6_1789x1043.png)
*来源：Tesla*

Tesla 将 BESS 描述为管理需求波动的更可行选项，优于柴油发电机或电容器组等替代方案。数据中心电容器的原理，以及我们是否认同 Tesla 的说法，将在付费墙后展开。Tesla 的方案假定 Megapack 2 XL 会与发电机、UPS 等既有措施*配套*安装。其中一张幻灯片指出，将 BESS 与发电机串联安装可以让该发电机运行更平滑（进而延长寿命）。

![](https://substack-post-media.s3.amazonaws.com/public/images/39357d2d-8137-4b34-842e-861adf1ad913_1936x791.png)
*来源：Tesla*

Tesla 提到电容器组也是一种选择，但也正确指出电容器组无法在秒级尺度上完成负载平滑。相比之下，BESS 可以在兆瓦/毫秒、兆瓦/秒*以及*兆瓦/分钟三个尺度上管理负载波动，其灵活性远超电容器组、柴油发电机或电网级资源所能企及。

如上所述，BESS 还能改善对低电压穿越（LVRT）的响应。值得注意的是，Tesla 描述 Megapack 的功能时是将其与现有 UPS *搭配*使用，而不是把 BESS 方案描述成 UPS 的*替代品*。具体来说，Tesla 将其 BESS 描述为对 UPS 基线行为的补偿手段：当电压连续多次骤降时 UPS 会离网，一旦 UPS 切换到离网运行，BESS 就会从电网上抽取功率充电，让电网在其手动复位期间仍看到「模拟」的负载。

### **用于需求响应的 BESS**

Tesla 还提出了对数据中心的一项附加收益：**需求响应**。这种做法名目繁多——电网边缘响应、柔性负载管理、负载削减、负载调节——但时至今日，由于缺乏激励，普及率一直不高（得州的比特币矿工除外）。需求响应的概念很简单：如果你参与这类项目，电网可以强制你关停负载，但会为此给你补偿。

在当今电力紧缺的环境下，激励的天平开始倾斜。需求响应能让输电系统释放更多容量，并缩短通电时间（time-to-power）。根据[杜克大学的一项研究](https://nicholasinstitute.duke.edu/sites/default/files/publications/rethinking-load-growth.pdf)，如果新增负载每年能实现 20-90 小时的需求响应，仅 ERCOT 系统就可在不进行额外系统升级的情况下多接纳 6.5-14.7 GW 的新增负载（不限于数据中心）。

这源于电网的基本设计原则。许多潜在站址在当地可发电或可输入的电量上存在限制。但这类约束每年只在 20-90 小时内、即全年的 0.25-1% 时间内真正起作用。电网一年中负载最大的那些**高峰时段**，正是电网大量物理基础设施的具体设计规格所在。值得注意的是，由于这些高峰主要由空调和表后太阳能驱动，它们相当可预测：盛夏热浪深处的傍晚时分，表后太阳能发电随日落消退之际。

![](https://substack-post-media.s3.amazonaws.com/public/images/230c9f12-7ee5-443b-afe9-e84b0bc1ccd1_1877x1086.png)
*来源：《Rethinking Load Growth——评估美国电力系统整合大型柔性负载的潜力》*

xAI 参与田纳西州孟菲斯一个需求响应项目，是它能以快于常规时间线的速度接入电网电力的关键。虽然现场的燃气轮机让集群得以在四个月内建成投运，但 xAI 还建设了一座变电站，并已从电网抽取 150MW——从提出负载申请到落地不到一年，速度惊人。

![](https://substack-post-media.s3.amazonaws.com/public/images/4765bea4-a026-40a6-afae-08c69ea240ac_2000x812.png)
*来源：Tesla*

不过，需求响应的落地在客户侧和公用事业公司侧都有挑战。在客户侧，没有人*喜欢*执行需求响应——很多情况下这意味着关灯、关空调、削减「非必要」工艺负载。备用电源由此成为刚需，而 Tesla 认为 BESS 正好胜任：数据中心不必削减负载，而是让 BESS 放电，从而降低电表处的电力需求。

![](https://substack-post-media.s3.amazonaws.com/public/images/aea28e42-34c7-4270-8b25-36d8b0f28780_1924x838.png)
*来源：Tesla*

值得注意的是，这要求在**高峰事件**（peak event）启动前把电池充满，事件启动后再放电。给电池充电本身就是挑战：公用事业公司通常只提前 24 小时识别出高峰事件的可能性，并提前 3 小时才确定高峰事件大概率的 3-6 小时窗口。即便公用事业公司通知客户高峰事件时真的足够及时（有理由对此表示怀疑），除非 BESS 一直保持满电，否则留给反应的时间*非常有限*。若缺少跨多个大负载的精细**荷电状态（SOC）**管理，一个先进的需求响应项目可能眼看着高峰负载挪到下午 1 点或 2 点——因为各路大负载为了备战*预计*下午 5 点出现的高峰事件，纷纷提前给自家电池充电。此外，用于需求响应的每一分 SOC，都是*没有*留给 LVRT 事件或更大规模停电备用的 SOC。每一套 BESS 都必须被编程为在需求响应与备用电源这两大任务之间权衡取舍——优先其一，必然等比例牺牲其二。

然而，即便装上 BESS，也解决不了需求响应在公用事业公司侧的挑战。首要的一点是：公用事业公司做需求响应普遍非常糟糕。公用事业公司的 IT 基础设施往往落后 10-20 年，需求响应管理软件（DRMS）也仍是一个不成熟的市场。各家公用事业公司在需求响应的技术构件上普遍力不从心，例如：

- 采集和管理高质量高峰预测所需的数据
- 编写并运行好的高峰预测工具
- 就高峰事件通知客户
- 将需求响应措施接入工商业建筑中拼凑而成的楼宇管理系统（BMS）
- 精确计量客户的需求响应量
- 将需求响应转化为账单抵扣

除了执行层面，公用事业公司也难以给出让需求响应值得做的激励支付。作为纯电量市场（energy-only market），ERCOT 对发电容量并无严格定价——那样才会给峰值需求标上硬价格。该机构已批准一项名为**[绩效信用机制（PCM）](https://www.spglobal.com/commodity-insights/en/research-analytics/texas-electric-regulators-turn-to-a-novel-solution-to-solve)**的市场改革，大概率在 2026 或 2027 年落地。然而，即便 PCM 成本能反映出像 MISO 和 PJM 那样高得有争议的峰值成本——每 kW-月 8-15 美元（每 MW-日 270-500 美元）（含容量与输电）——对 20 MW 的需求削减而言，算上公用事业公司的人工、DRMS SaaS 费用和给客户的账单抵扣，每月也就在 16 万-30 万美元量级。折到数据中心的电费账单上，大概也就是一笔五位数的抵扣。对于为*落地*需求响应所投入的全部精力和资本而言，这往好里说是零头，往坏里说是侮辱。

### **BESS 的成本**

Tesla 的幻灯片对 Megapack 系统的净成本含糊其辞，因为实际成本很可能不菲。根据 [Lazard 2024 年 6 月的 LCOE 报告](https://www.lazard.com/media/xemfey0k/lazards-lcoeplus-june-2024-_vf.pdf)，一套 100 MW 的 BESS：两小时电池（即 Tesla 幻灯片所述规格）需要 **3,800 万至 8,000 万美元**，四小时电池（要实现可用的需求响应或备用电源则属必需）需要 **7,600 万至 1.57 亿美元**。按这样的安装价格，一套适配吉瓦级数据中心的 BESS 成本将**接近 10 亿美元**，而且 Tesla 并不会在这个价位上把 BESS 当作 UPS 或柴油发电机的*替代品*。它干脆就是一笔额外成本——体现在建设工期、资本开支（CAPEX）、土地占用、供应链脆弱性，以及无穷的麻烦上。

那么，BESS 就是管理数据中心负载波动的最佳方案吗？今天我们聚焦表后（behind-the-meter）BESS；SemiAnalysis 未来的报告会在[显著高于过去 20 年的负载增长](https://www.semianalysis.com/p/datacenter-model)背景下，探讨 BESS 与可再生能源在电网中更广泛的角色。

下面，我们将探讨基于硬件的替代方案，比较它们的优劣，并讨论相关供应商。

## 基于硬件的 AI 训练负载波动解决方案
