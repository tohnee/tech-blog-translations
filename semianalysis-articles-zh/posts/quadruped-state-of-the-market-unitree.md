---
title: "四足机器人市场全景——宇树、Boston Dynamics、ANYbotics、DEEP Robotics 与正在崛起的应用生态"
title_en: "Quadruped State of The Market - Unitree, Boston Dynamics, ANYbotics, DEEP Robotics, and The Rising Application Ecosystem"
subtitle: "四足机器人无可匹敌的可扩展性、宇树惊人的产能、第三方供应商带来新格局、全新应用与机遇、宇树难以置信的物料清单（BoM）、四足机器人 TAM"
date: 2025-10-20
source: https://newsletter.semianalysis.com/p/quadruped-state-of-the-market-unitree
crawled: 2026-09-15
authors: ["Reyk Knuhtsen", "Dylan Patel", "Niko Ciminelli", "Joe Ryu", "Jeremie Eliahou Ontiveros", "Robert Ghilduta"]
tags: ["Robotics"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 四足机器人市场全景——宇树、Boston Dynamics、ANYbotics、DEEP Robotics 与正在崛起的应用生态

> 原文：[Quadruped State of The Market - Unitree, Boston Dynamics, ANYbotics, DEEP Robotics, and The Rising Application Ecosystem](https://newsletter.semianalysis.com/p/quadruped-state-of-the-market-unitree) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**四足机器人无可匹敌的可扩展性、宇树惊人的产能、第三方供应商带来新格局、全新应用与机遇、宇树难以置信的物料清单（BoM）、四足机器人 TAM**

四足机器人是当今最先进的通用型机器人。虽然它们不像人形机器人那样频繁占据头条，但随着其 [L2 级自主](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/)（Level 2 Autonomy）能力上线，一大批机器人领域此前不存在的新市场机会正在打开。理解四足机器人市场及其生态，是窥见自主机器人未来的重要一环。

当前，四足机器人硬件供应商主要两家：西方先驱 Boston Dynamics（波士顿动力）与中国硬件冠军宇树科技（Unitree）。ANYbotics/DEEP Robotics 是值得一提的重要玩家，我们会简要介绍。更广泛的新兴初创生态正在托举所有供应商——它们利用新的 AI 模型架构增强硬件，并用软件支持多种应用。我们将讨论这些市场动态，给出未来展望，以及正在被解锁的新机遇。

我们还将深入分析宇树 Go2 与 B2 的详细物料清单（BOM），包括齿轮箱、电机、驱动器、轴承、连杆、电池、LiDAR、足部传感器、光学相机、SoC、摄像头等。这里的重点是：它们的利润率高得惊人，远超多数人的想象。宇树并没有亏本卖货，他们已经攻克了低成本大批量制造。

我们还会为以下行业提供总可服务市场（TAM）分析框架：石油与天然气、半导体晶圆厂和数据中心，以及暴露于四足机器人需求的零部件供应商。鉴于传闻中的[宇树即将 IPO](https://www.reuters.com/business/autos-transportation/chinese-robotics-firm-unitree-eyeing-7-billion-ipo-valuation-sources-say-2025-09-08/) 及其大部分营收来自四足机器人，这一切都极具时效性。

我们的核心要点：

- 宇树相对西方同行拥有显著的成本优势。
- 凭借中国制造业的压倒性优势，宇树拥有宽得多的产品线和快得多的产品发布节奏。
- 作为硬件供应商，Boston Dynamics（以及程度较轻的 ANYbotics/DEEP Robotics）已在西方市场实现部署，受益于部分垂直整合。
- 宇树目前更聚焦中国工业部署，其**安全问题**仅在部分市场构成障碍。
- 不过，宇树在西方研究实验室/机构中已获得实质性 traction，其低成本硬件与完善的开发套件，加上强大的研究者开源社区，形成了合力。
- 第三方应用层生态持续成长并促进四足机器人落地，提升**所有**四足机器人的能力。

## 为什么四足机器人统治导航任务

虽然无人机、轮式机器人、履带式机器人等更多 [L2 级自主](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/)系统同样可以自主运行，但四条腿的四足机器人是行进世界中灵活性、适应性最强的设计之一。这为一大批可被自动化的新角色打开了大门。

四足机器人凭借动态行走穿越这些杂乱狭窄的区域，随时调整姿态、弯曲“膝盖”。这种灵活性在化工厂、建筑工地等脏乱、障碍密布的环境中至关重要。

![](https://substack-post-media.s3.amazonaws.com/public/images/d2560e11-fb6d-4e22-b455-d66aa7ef16bd_1372x684.jpeg)
*来源：Unitree*

此外，其形态允许系统集成商加装多种不同的传感器和部件——从 LiDAR、声学传感器到图像采集设备等等。以需要同时兼顾热量、声音和成像的油气设施为例，这一点至关重要。凭借四足的承载力和可观的大容量电池，所有这些传感器都可以在其上长时间支撑更持久的巡检。

轮式机器人、履带式机器人和无人机当然都可以针对特定用例做专门化，但作为通用平台，四足机器人开箱即用的功能最为丰富。这将带来更广泛的应用、摊薄成本，使其成为导航任务中可扩展性最强的形态因子。那么，为什么其他形态做不到这么通用？

### 无人机——小巧但娇贵的导航

无人机的速度远高于四足机器人，成本也低得多。然而，法规可能限制它们。多数情况下，无人机无法真正自主运行，需要操作员持续监视，在建筑工地等户外场所尤其如此。

此外，安全接近待检区域仍是无人机的[一大难题](https://www.mdpi.com/1424-8220/21/6/2194)。靠近墙壁、天花板或地面会产生紊乱气流，可能导致无人机坠毁。这被称为“桨叶下洗流”（prop wash），它会让无人机在大约 ~1.5 倍螺旋桨直径的距离上被墙壁“吸引”，毁掉巡检作业。

可以用更多传感器来缓解，但无人机本就只有 ~30-45 分钟的短暂续航。相比之下，四足机器人续航可达数小时，且耐碰撞。

![](https://substack-post-media.s3.amazonaws.com/public/images/4aa8d1c2-823c-42a2-a083-25e41d43fc22_1920x1440.jpeg)
*来源：Coptrz*

### 轮式与履带式机器人——皮实，但有取舍

再看替代方案：轮式机器人速度更快（[~2m/s](https://clearpathrobotics.com/husky-a300-unmanned-ground-vehicle-robot/)，四足为 0.75-1 m/s）、更坚固；履带式机器人[更皮实、抓地力更好](https://www.academia.edu/123097297/_Wheels_vs_tracks_A_fundamental_evaluation_from_the_traction_perspective)，但比四足机器人慢（~0.4 m/s）。轮式/履带式机器人可以专门针对速度或载荷优化，但代价又是一个通用性、可扩展性更差的平台。

而四足机器人解决了许多制约轮式/履带式机器人的瓶颈难题。

**缺乏动态步态**：难以在狭窄、受限空间中行进。例如 [Argus](https://robot.martecsrl.it/download/argus.pdf) 需要 2.5 米转弯半径，这在化工厂这类局促环境中被进一步放大。多数四足机器人身长仅 ~1 米左右，行进灵活性因而高得多。

![](https://substack-post-media.s3.amazonaws.com/public/images/d47b4466-5677-47c3-8a2f-25e136911ceb_2452x1266.png)
*来源：ANYBotics，一台 ANYmal 正在穿越狭窄走廊*

**穿越杂物**：轮式/履带式机器人可能碾压地面物体，损坏物体或自身，还可能被卡住。履带式机器人的越障高度可能只有 4-6cm，轮式机器人最高可到 12cm。但增大轮径同样有代价：更大的轮子牺牲稳定性、增大车体尺寸，带来回转半径难题——但为了越过坡顶的“纵向通过角”（breakover angle），有时又不得不如此。

![](https://substack-post-media.s3.amazonaws.com/public/images/188f0e35-c3ec-4f55-820c-84bdba2862d3_1920x1920.jpeg)
*来源：SuperDroidRobots*

**不同高度的表面**：显而易见，却在许多应用中至关重要。建筑工地遍布可能阻碍行进的障碍物、路缘或楼梯。坡道和电梯能帮上忙，但会推高机器人部署成本。

履带式机器人有时**确实可以**攀爬 [20cm](https://microwatt.com/wp-content/uploads/2021/08/exr-1-operating-guide.pdf) 以上的台阶，坡度甚至可达 [45 度](https://www.taurob.com/inspector/)，使上楼梯成为可能，但有翻倒风险。此外，跨越过宽的缝隙（即大于轮径）可能使机器人被卡住，而四足机器人可跨越约 [~30cm](https://www.anybotics.com/anymal-technical-specifications.pdf) 的缝隙。

![](https://substack-post-media.s3.amazonaws.com/public/images/5ad68578-981c-45cf-8b2d-95a2eb97d2b9_1024x683.jpeg)

## 四足机器人崛起的关键使能因素

过去的四足硬件过于笨重、低效且昂贵，难以证明使用价值，如今它们已能力出众：

- [锂电池（li-ion）的突破与成本下降](https://www.econopolis.be/en/blog/posts/2024/may/is-double-digit-day-nearing-for-li-ion-batteries/)改变了格局：2010 年约 ~12kg 的电池，如今凭借功率密度提升只剩 [~6kg](https://rmi.org/the-rise-of-batteries-in-six-charts-and-not-too-many-numbers/)。
- 硬件厂商从笨重、易漏、昂贵（数千美元）的液压执行器转向了更便宜的电动执行器。
- 传感器为 [L2 级](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/#level-2-autonomous-mobility)机器人提供了“视觉”，且性能稳步提升、价格持续下降。LiDAR 价格下降了[几个数量级](https://futurism.com/price-eyes-autonomous-vehicles-drops-75k-just-250)，摄像头[像素数翻了几倍](https://www.phonearena.com/news/in-2024-54-mp-the-average-resolution-for-primary-smartphone-cameras_id163407)，飞行时间（即深度）传感器的[测距翻倍](https://www.kitguru.net/peripherals/camera-peripherals/christopher-nohall/intel-announces-its-latest-realsense-depth-camera-d455/)。
- 算力呈指数级提升：从 Nvidia [2015 年](https://developer.nvidia.com/blog/nvidia-jetson-tx1-supercomputer-on-module-drives-next-wave-of-autonomous-machines/)1TFLOP 的 Jetson TX1，到今天 2070 TFLOPS（[FP4](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-thor/)）的 Jetson Thor。

硬件的发展如今需要软件来实现应用层功能，所幸许多要素已经就位：

- 核心自主：自行规划、导航和控制自身的能力，例如在现实世界中行动的通用 AI 模型
- 任务专用软件：使四足机器人能执行特定任务，如读取仪表、检测气体泄漏或分析热成像图。
- 系统集成：将多个传感器接入机器人以进行巡检与处理，并将机器人接入基础设施以收集数据

这绝非小事：**每一个**环境、传感器或应用往往都**需要一套同时适配**任务与机器人的**定制解决方案**。通常由第三方公司入场，在硬件之上补齐这剩下的解决方案。

如今软硬件俱备，市场即将起飞。

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

## 市场格局铺陈

当前四足机器人硬件市场由两家主导：Boston Dynamics 与宇树，DEEP Robotics 和 ANYbotics 落后。Boston Dynamics 与 ANYbotics 在一定程度上垂直整合，自行掌控和设计软件/自主能力，以实现精简部署。

宇树和 DEEP Robotics 则采取硬件优先路线，同时布局多款人形和四足机器人。它们与研究社区及第三方生态紧密协作，其他人常常基于其硬件构建自主系统。

**Boston Dynamics** 是人形机器人、四足机器人和鲁棒运动控制的先驱之一。其四足机器人 **Spot** 已在多种环境中承担巡检。据多方报道，Boston Dynamics 产品线（含仓储机械臂 "Stretch"）年收入在 $100M-$200M 之间。

![](https://substack-post-media.s3.amazonaws.com/public/images/6eac9662-528e-4467-892b-f36ab5ca6ec9_2560x1707.jpeg)
*来源：Boston Dynamics*

**DEEP Robotics** 的防护等级（IP67）、续航和载荷与工业级宇树产品相当，价格却高出 30% 以上，公司专注工业应用。目前其上升势头很快，已在 40 多个国家实现约 [600 例部署](https://www.morningstar.com/news/accesswire/1053303msn/deep-robotics-showcases-core-technologies-real-world-applications-of-embodied-intelligence-robots-at-waic-2025)。

![](https://substack-post-media.s3.amazonaws.com/public/images/7ce2ef67-a1ae-4462-b685-a117e3ee7396_1200x472.jpeg)
*来源：DEEP Robotics*

**ANYbotics** 于 2016 年从苏黎世联邦理工学院（ETH Zurich）剥离——后者是全球顶尖、以前沿运动控制研究著称的机器人实验室之一。该公司如今专注于危险和肮脏环境中的巡检任务，年收入[不足 $27M](https://www.zoominfo.com/c/anybotics/401723840)。

![](https://substack-post-media.s3.amazonaws.com/public/images/50e7e909-21d1-442a-bbaf-a4279255d981_2732x2049.jpeg)
*来源：Siemens*

中国的**宇树**统治着四足机器人市场，据估计 2023 年按销量计占全球 [70%](https://news.qq.com/rain/a/20241005A03SNM00) 份额。其强力定价与硬件征服了科研圈，目前正扩张进入工业巡检市场。公司年营收已突破 [10 亿元人民币](https://eu.36kr.com/en/p/3353252936479360)（约 $140M）。

![](https://substack-post-media.s3.amazonaws.com/public/images/39b7ea28-5b48-42ad-91fb-214c6325f93b_1200x1200.jpeg)
*来源：Unitree Spain，Unitree B1*

宇树产品线丰富，其核心制造与组装工艺可以复用于全系列产品的制造，成本之低令人惊叹。

- Go2 四足机器人是其低端产品，价格约为高端机型的 ~1/10，已被[用于数据采集](https://igrownews.com/unitree-robotics-latest-news/)等应用。
- B1 是工业级防水四足机器人，宇树将其宣传为最坚固、最多能的四足机器人之一，拥有 20kg 行走载荷的惊人能力。（[点击这里看它背着 250kg 上下楼梯！](https://www.aboutamazon.com/news/operations/amazon-million-robots-ai-foundation-model)）
- B2（不防水）在 B1 基础上打造，续航更长、关节更强，行走载荷达 40kg。B2 还可选装轮子。
- A2（Stellar Hunter，“星际猎手”）是其最新四足机器人，已知规格不多，但续航、载荷和敏捷性都令人印象深刻。同样可选装轮子。

![](https://substack-post-media.s3.amazonaws.com/public/images/a12d527e-7ba5-4524-a5b3-b659f70e7220_1128x191.jpeg)
*来源：Unitree*

## 硬件市场现状——宇树的定价优势

四足机器人市场尚处早期，但**仅 2023 年一年，宇树的出货量就已约为下一名竞争对手总出货量的 ~10 倍。**如今数字已高得多，但这是最近的公开表态。

![](https://substack-post-media.s3.amazonaws.com/public/images/ce78bdac-667f-430f-bad6-d9b6faa913d5_1255x852.png)
*来源：SemiAnalysis 估算、GGII 报告*

该估算包含宇树低端机型 Go2——**旺季时其 [Go2 日产能约 200 台](https://semianalysis.com/core-research/)。**

西方四足机器人通常采用机器人即服务（RaaS）模式，月费约 $10K。但缺乏中国供应链优势的它们，成本仍显著高于宇树。

![](https://substack-post-media.s3.amazonaws.com/public/images/ac7f1425-7ab0-42fd-b711-8928136810fb_1314x599.png)
*来源：SemiAnalysis 估算*

宇树的低成本打法令人印象深刻；西方产品虽然在应用层功能上略胜宇树一筹——比如稳定的 API 或自主能力——但这些功能往往并不完整。

## 自主能力——并非全貌

在 [L2 级自主](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/#level-2-autonomous-mobility)一文中，我们讨论了这些四足机器人的自主能力正在上线，但这些四足硬件公司并未完全兑现这一潜力。这种自主能力需要：

- 规划——判断周围环境，确定遵循的方案
- 导航——在环境中恰当地机动
- 定位——就位以安全、准确地执行巡检

西方四足机器人的自研自主系统***确实能够***绕开人员、障碍物和危险规划路径，并在厂区内可靠移动。但**定位**并不总是精准，往往需要 AprilTags（类似二维码、用于为机器人重新定向的标记）或面向特定任务的定向模型。**规划**则可能失灵——在新情况下（如移动中的人员）机器人会停滞或做出糟糕选择（有些干脆原地停住）。**导航**在杂乱环境中仍然脆弱。在训练过的场景里，西方产品可能表现良好，但面对陌生场景就可能吃力。

至于宇树，其自研自主能力外界了解较少。但从我们的调研看，目前很可能没有超出预编程动作和遥操作的范畴。虽然西方四足机器人相对宇树开发了部分自主/软件栈，但这未必能为他们赢得更多部署。

## 四足机器人市场正在如何演变？

市场仍处早期，已出现两种泾渭分明的商业策略。

- **垂直化**：西方公司走的是这条路，自 ~2018 年起将大部分软件、系统集成和自主能力内部化，以支撑更早的应用落地——但同样不完整。
- **生态化**：宇树选择聚焦硬件规模化，同时借助更广泛的研究社区和第三方生态来完成软件与部署。

我们不指望四足机器人厂商做出包打天下的一体化产品。相反，机器人将作为硬件平台，其上叠加不断进步的外部解决方案。这很可能催生一个由专业玩家构成的碎片化市场，包括原生四足机器人厂商（OEM）、模型供应商、系统集成商和软件供应商。很多时候，这些应用层公司会掌控部署的大头。

### 模型供应商——出售自主能力

[L2 级自主](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/#level-2-autonomous-mobility)的到来，为提供出色自主技术栈的**模型供应商**创造了切入点。西方正涌现两家瞩目的模型供应商：

- [FieldAI](https://www.fieldai.com/)——为四足机器人及其他 L2 级系统提供“风险感知”基础模型，如今仅靠**即插即用**（drop-in）就能在多种环境中安全导航。FieldAI 的功能化部署已覆盖建筑工地、工业与能源厂区、安防巡逻等领域。
- [Skild AI](https://www.skild.ai/)——提供专有“大脑”，在多种机器人形态上统辖运动与操作自主。Skild AI 的四足机器人已在建筑与安防巡逻场景落地。

FieldAI 与 Skild AI 利用最先进的 AI 模型补齐四足自主能力缺口，动态适应、独立可靠地完成任务。Boston Dynamics 和 ANYbotics 也在探索 AI 模型，但目前落后于这些专业厂商；而宇树似乎更能助力 AI 研究（详见软件部分）。

![](https://substack-post-media.s3.amazonaws.com/public/images/ab672b8d-c7d1-45b5-8ec5-a3b8b3996e4e_500x507.jpeg)
*来源：FieldAI*

尽管创立不久，两家公司都前景可期，并最近获得巨额投资：Skild 估值达 [$4.5B](https://finance.yahoo.com/news/nvidia-samsung-back-4-5b-203049332.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAIHcrNjsMROHxh3QCTp5cdaIvG9LZiwuBY_-SA6bMyKj5JbUB4xNknmc-5LVf8_7_CkBEjx-Yuy7PwyVdpws-AvqeOGIoRS74_F4LlLM2SBvnDFi62gaYXXQF67GLAIOEmI2Em6imkK8rvm-myUYsYgMtAhUWMsb_8TSuH27g1Sw)，FieldAI 两轮融资后累计超过 [$400M](https://www.fieldai.com/news/fieldai-announces-over-400m-in-funds-raised-to-advance-embodied-ai-at-scale)。

### 系统集成——新传感器与基础设施

正如我们在 [L1 级自主](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/#level-1-intelligent-pick-and-place)中看到的，集成的好坏决定机器人的可行性。对 [L2 级自主](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/#level-2-autonomous-mobility)的四足机器人而言，其通用性缓解了以往的可靠性负担，但集成仍未高效。

系统集成商通过按客户期望的工作流配置四足机器人，帮助企业落地自动化。这包括传感器、工具，以及与既有基础设施的安装和调试。系统集成商随后针对具体应用改造四足平台，为客户/四足 OEM 减负。不过，Boston Dynamics 和 ANYbotics 配备了成熟的 API/SDK 以精简系统集成，而宇树的据称逊色不少。从事这类工作的公司有：

- [Chironix](https://chironix.com/news/chironix-robot-psychologists/) 用其 PilotOS 软件为四足机器人集成所需传感器并接入既有基础设施
- [IntuitiveRobots](https://www.intuitive-robots.com/our-payload-integrations-with-spot-robot/) 为 Spot 集成声学传感器等载荷，并将数据转译为可视图像
- [SUPCON](https://en.people.cn/n3/2025/0219/c90000-20278525.html) 这家中国系统集成商成功将四足机器人集成进沙特阿拉伯的油气厂区基础设施

![](https://substack-post-media.s3.amazonaws.com/public/images/6b262d6c-fe40-4938-b382-28d33e3c5fde_1280x800.jpeg)
*来源：IntuitiveRobots*

系统集成领域尚未“整合”，[SLB](https://www.slb.com/news-and-insights/newsroom/updates/2025/slb-partners-with-anybotics-to-advance-autonomous-robotic-operations-in-the-oil-,-a-,amp;-gas-sector) 等大玩家才刚开始集成四足机器人。客户和四足供应商往往依据部署需求、地域和公司来选择集成商。很多时候，模型供应商及其他应用层公司也可能把持这一环节。

### 应用层——API 锦上添花，并非命脉

这些公司补上运营的最后一层：或夯实任务自主，或编排（多台）四足机器人，或提供面向客户的仪表盘。它们让四足机器人部署在长期运营中尽可能高效。这类玩家如：

- [Lattice](https://www.anduril.com/article/anduril-unveils-lattice-for-mission-autonomy)（Anduril 旗下）提供强健的编排与规划层，尤其面向机器人机队
- [Formant](https://formant.io/resources/supported-devices/) 提供优化的机队管理与遥测，在许多案例中与 Spot、ANYmal 及**宇树**机器人搭配部署。

![](https://substack-post-media.s3.amazonaws.com/public/images/59010264-7a93-419f-9bce-5e8efe7fc883_768x432.webp)
*来源：Formant*

ANYbotics 和 Boston Dynamics 凭借预建的 API 和数据采集平台拥有先发优势。不过，随着宇树日益流行，与我们交流过的公司正在学会即便面对其逊色的集成平台也照常开展工作。

### 生态普惠众生，亦重塑格局

得益于[自动化需求](https://semianalysis.com/2025/03/11/america-is-missing-the-new-labor-economy-robotics-part-1/)，四足机器人**生态**正百花齐放，优雅的部署方案不断上线。这股势头可能惠及宇树这类以硬件为核心的玩家，进一步拉平应用层的竞技场。一旦四足硬件商品化，第三方供应商可能成为西方四足格局中最具影响力的力量。

四足机器人厂商的经济增长可来自两方面：硬件成本下降，或能力/吞吐提升。对西方四足厂商而言，可能需要强化供应链，或为**自家**四足机器人培育更强的生态。对宇树来说，当前降价+借力生态的策略或许已经足够。

### 没有超大规模客户，碎片化在所难免

机器人领域正开始出现“超大规模客户”，比如拥有[百万台机器人](https://www.aboutamazon.com/news/operations/amazon-million-robots-ai-foundation-model)的亚马逊。超大规模客户进场后，市场往往会向少数玩家集中。今天的四足机器人市场缺少这样的客户，因此格局碎片化。一旦这样的客户出现，其形态更可能像 AWS——作为服务对外出售——而非特斯拉内部自用的 Optimus。在那之前，宇树硬件优先的策略将持续受益于生态玩家，后者正不断切走下面这类部署的份额。

### 潜在市场机遇

驱动四足机器人市场的因素很多，但西方经济体对四足机器人的需求高于劳动力或资本更廉价的国家。西方客户的兴趣与采用可能主导市场格局与企业演进。让我们看看未来五年西方市场的新机遇！

**数据中心**：在超大规模云厂商的数据中心，停机一天损失可达约 [$1M](https://semianalysis.com/datacenter-industry-model/)。四足机器人可巡检电气场区，依据声学和热学水平判断变电站设备是否正常。对冷却基础设施而言，要确保没有泄漏、盘管温度不均或风扇异常振动，以免危及训练/推理。四足机器人大部分时间将在室外工作，恶劣天气下需要更高 IP 防护等级，或更长续航才能巡完庞大场区。

![](https://substack-post-media.s3.amazonaws.com/public/images/010b0159-50b9-4a35-8791-f4f42a3249ca_1529x1776.webp)
*来源：FieldAI*

**末端配送**：在大学校园、智慧城市、高尔夫球场等封闭区域，这是另一个前景可观的应用。这类环境中，时薪 $18 的人类配送员每单成本可高达 $9，而机器人每单只需约 [$2.50](https://www.campusidnews.com/ohio-state-and-avride-robots-get-food-to-students-faster-and-cheaper)。在如此小的区域内用汽车成本高昂，人类配送员效率低下。四足机器人——尤其是加装轮子的——完美契合这一角色，能把一项低效服务变成赚钱生意。

![](https://substack-post-media.s3.amazonaws.com/public/images/f92d4fd5-2753-43aa-a87c-08bb5168eaf3_1200x675.webp)
*来源：InterestingEngineering*

**安防巡逻**：无武装保安可能需要 24/7 巡逻一处设施，按薪资和培训水平不同，年成本在 $250K-$450K 之间。除了让人类远离危险，考虑到四足机器人 RaaS 月费仅 $10K，还能为公司省下大笔开支。在更大周界场景下，可采用轮式方案加快巡逻。

![](https://substack-post-media.s3.amazonaws.com/public/images/3e451e80-b0a0-456c-ab28-286509ae45bd_1794x973.png)
*来源：FieldAI*

## 这些四足机器人都在哪里工作？

### Boston Dynamics 的主攻方向：晶圆厂

这类设施标准严苛；机器人要入场，必须通过低颗粒物合规认证，流程可长达数月。但一旦获批，价值显而易见：一根失效管道的更换成本可达 $30,000，而由 Spot 机器人早发现、早维修，成本最低只要 $3,000。

![](https://substack-post-media.s3.amazonaws.com/public/images/3957a1b1-4f08-4b33-87d9-6636a2a92005_2560x1706.jpeg)
*来源：Intel*

进一步进入厂务下层（subfab）或洁净室则更难。有些晶圆厂可能要求四足机器人一旦进入就永不离开，这意味着完全自主和绝对可靠。此外，严苛的颗粒物限值可能要求密封关节、特种材料，甚至“连体服”式外罩。

### ANYbotics 的主攻方向：肮脏与危险环境

ANYbotics 瞄准另一个利基：需要 IP67 防护的环境。该等级使机器人防尘且可[浸水](https://www.youtube.com/watch?v=eIuM-PWV8r0)，对于腐蚀性钾矿或海水会损毁普通机器的海上钻井平台至关重要。它目前是唯一拥有 IP67 级四足机器人的西方公司，尽管 Boston Dynamics 也计划对 Spot 做“加固”。

ANYbotics 似乎是唯一在开发防爆机型 ANYmal X 的四足厂商，计划 2026 上半年（1H26）推出。ATEX（防爆）认证将允许其进入存在爆炸性气体的 Zone 1 区域，打开更大一片油气市场。

![](https://substack-post-media.s3.amazonaws.com/public/images/66929568-938e-4489-a003-d1f0e8963de9_1232x742.png)
*来源：ANYBotics*

给足式机器人做防爆远比封装设备或固定式设备复杂。它需要更改电池化学体系、充氮以及消除火花的防护措施。该流程最长可耗时两年，并会冻结硬件设计——拖慢平台创新，却打开一个重要市场并降低安全风险。

我们听到系统集成商将 ANYbotics 视为腐蚀性、危险以及即将覆盖的易爆环境中的首选。付费墙后，我们将测算四足机器人的潜在 TAM。

### DEEP Robotics：从电力基础设施到物流

与 DEEP Robotics 的交流表明，其[表现出色](https://technode.com/2025/01/07/deep-robotics-delivers-x30-quadruped-robot-spock-for-singapore-power-inspections/)的[工业巡检](https://www.digitaljournal.com/pr/news/accesswire/deep-robotics-leads-industrial-robot-1182802635.html)业务——无论国内还是[海外](https://technode.com/2025/01/07/deep-robotics-delivers-x30-quadruped-robot-spock-for-singapore-power-inspections/)——均成绩亮眼，并且可能进军末端配送。凭借皮实的轮式机器人和广泛的海外网络，只要宇树更便宜的轮式四足机器人不进场，扩张看似可行。虽然宇树也有一些工业应用，但其重心似乎在另一个市场。

![](https://substack-post-media.s3.amazonaws.com/public/images/1bc62664-4a9e-4dce-a154-3516e43d4dba_800x600.jpeg)
*来源：DEEP Robotics*

### 宇树：从中国工业用例到科研市场

尽管其高端四足机器人比西方机型便宜最多 50%，并拥有完全防水的 IP68 等级，它们在西方工业市场仍不常见。它们有时部署于中国国家电网、化工厂和钢铁厂，往往作为[遥操作机器而非完全自主机器](https://prosmt.ai/wp-content/uploads/2025/07/B2inspection_compressed.pdf)运行。

![](https://substack-post-media.s3.amazonaws.com/public/images/2c825424-7fd9-4665-abf6-813f239e8ada_1170x406.png)
*来源：Unitree，正在巡检广东某石化厂*

宇树在**轮式四足机器人**上还有独特优势，在需要速度的应用（如巡逻大型周界）中可能击败其他西方四足机器人。

![](https://substack-post-media.s3.amazonaws.com/public/images/be5e0e5c-7566-4792-9eba-42c26984f1bb_2402x1203.png)
*来源：YouTube*

随着生态持续部署宇树机器人，它在另一个圈子里依旧**占统治地位**。

## 科研——宇树的主场

宇树在服务科研圈方面出类拔萃。Spot 和 ANYmal 对多数实验室来说太贵，尤其是测试控制策略时有损坏硬件的风险。研究者转而选择低价的 Go2，在宇树的软件开发套件（SDK）上开展大规模研发。这又反哺宇树——顶尖高校的项目帮助其平台构建强健的软件模型。随着宇树持续碾压自己的成本曲线，这种圈占将不断扩大。

![](https://substack-post-media.s3.amazonaws.com/public/images/70d33920-b62d-4915-8f83-8d1463aa69a7_1105x621.png)
*来源：NaVILA，一台正在学习导航的宇树 Go2*

### “RL 专用机器人”？新时代的软件架构

有人把宇树称为为[强化学习](https://semianalysis.com/2025/06/08/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data/)（RL）设计的“特殊机器人”。这话虽然有点令人困惑，却点出了“对 RL 友好的接口”有多么不为人知。让我们来聊聊那些让机器人特别适合策略学习的软件架构！

软件层把感知以最小延迟转化为运动。一些开发者使用 ROS 等开源框架，大厂则自建技术栈。两者角色相同：抽象硬件、管理传感器-执行器通信，并提供运动学与传感器融合库。

部署 RL 策略带来新的要求。这一过程被称为 [sim2real](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/)（仿真到现实），它必须以缩小仿真与现实差距的方式呈现数据——这是一个复杂的架构挑战。

- **控制回路**：在这一范式中，策略以“状态向量”为输入——包含当前电机位置、近期传感器数据和过往动作的复杂快照——并输出“动作向量”，其中包含电机位置与力矩的新指令。平台必须维持精确的实时时序，确保状态观测与动作执行保持同步，因为哪怕微小的失配都可能让训练好的策略失效。

![](https://substack-post-media.s3.amazonaws.com/public/images/009c197d-9f71-4023-bd2a-ceabadcf9430_720x278.webp)
*来源：Binay Dhakal*

机器人软件平台统筹整个过程：持续读取传感器数据、构建 RL 策略所需的状态表示、再执行所得动作。这要求坚实的通信与算力基础。

- 通信总线：四足机器人设计者通常组合使用多种总线。执行器、IMU（用于空间定位/运动）和位置编码器等实时部件常运行在控制器局域网（CAN）或 RS-485 等可靠总线上；相比之下，支撑感知的高带宽传感器——如摄像头、LiDAR 和麦克风——通常走 USB 之类的总线。

- 算力架构：底层算力架构的主控板通常依赖通用 ARM 处理器，因其能效出色且嵌入式 Linux 支持成熟。这些芯片往往足以执行运动策略和基础推理。但对于需要大型[视觉-语言-动作（VLA）模型](https://semianalysis.com/2025/07/30/robotics-levels-of-autonomy/)的高级应用，系统集成商正日益转向 NVIDIA 的嵌入式计算平台，尤其是 Jetson 系列和新近发布的 Thor——它们为在边缘运行大型神经网络提供必要的张量加速。

![](https://substack-post-media.s3.amazonaws.com/public/images/1f68a07e-0564-4171-8536-0f898e822929_1800x1200.webp)
*来源：Mehatronika，Nvidia Jetson Thor*

软件架构并非家家平等。多数四足机器人只提供基础的行走与攀爬控制器，而宇树开放直接电机控制，支持完整的控制开发。Boston Dynamics 的 Spot 也提供这种权限，但要按年循环付费。

这种直接电机控制对科研至关重要，因为在预设控制器之下学习会受到约束。《Rapid Motor Adaptation》（[2020](https://ashish-kmr.github.io/rma-legged-robots/)）是第一篇基于宇树机器人的重要论文，展示了实时适应困难地形——唯有通过这种开放性才可能实现。此后，研究者构建了[首批端到端运动系统](https://vision-locomotion.github.io/)之一——从视觉直达电机控制——成果不断精进。这类前沿研究主要在宇树平台上完成。

![](https://substack-post-media.s3.amazonaws.com/public/images/3a6747fe-2a70-41da-89a8-13e4bfa70764_2344x1105.png)
*来源：RMA*

[立即订阅](https://newsletter.semianalysis.com/subscribe?)

## 安全问题？

后门被发现（由 [Andreas Makris](https://www.linkedin.com/in/makrisandreas/) 发现）之后，安全可能成为头条风险，但现实情况好坏参半。宇树缺乏清晰的本地化（on-premises）数据方案，这可能限制其进入受 [NERC](https://www.nerc.com/pa/comp/guidance/EROEndorsedImplementationGuidance/CIP-013-1%20R1%20R2%20%20Supply%20Chain%20Management%20(NATF).pdf) 监管的美国公用事业。我们最近听说一些石油天然气公司已告知集成商不会部署宇树机器人。此外，对数据敏感的领域（如半导体晶圆厂）也排斥宇树。

与此同时，许多买家的顾虑没那么重。宇树四足机器人已广泛应用于建筑、关键基础设施甚至安防/巡逻工作。即便在[美国](https://www.insidegovernmentcontracts.com/2025/02/fy2025-ndaa-congressional-efforts-to-bolster-u-s-resilience-against-chinese-tech-and-influence/)/[欧盟](https://digital-strategy.ec.europa.eu/en/policies/nis2-directive)发出警告之后，部署仍在继续。安全因素很可能决定宇树能进入哪些细分市场，但眼下许多买家似乎举棋不定。

铺陈完四足机器人市场，我们现在来检视：是什么让宇树四足机器人比**其他任何选择**都便宜得多。

## 执行器设计是关键

执行器驱动四足机器人运动，占物料清单的最大份额，通常为 50–70%。各家公司的设计路线却各不相同。执行器分为旋转式（产生旋转运动）和直线式（产生直线运动，常与腿部机构搭配）。设计细节将在后续文章深入探讨，这里我们比较宇树在三个维度上如何做执行器：坚固性、成本和效率。

![](https://substack-post-media.s3.amazonaws.com/public/images/93c71fee-1c8b-4652-a897-b7d56b93a1e7_1985x309.png)
*来源：SemiAnalysis 估算*

## 宇树的执行器：MIT Cheetah 3 与准直驱

宇树选择了准直驱（QDD）风格执行器，与 [MIT Cheetah 3（2018）](https://dspace.mit.edu/bitstream/handle/1721.1/126619/iros.pdf?sequence=2)类似。其效率出色、成本极低，但坚固性稍逊。

![](https://substack-post-media.s3.amazonaws.com/public/images/0500b065-75a3-45de-b382-780bb3a678f3_2608x1397.jpeg)
*来源：Thomas Godden，QDD 执行器设计*

QDD 堪称足式运动的最佳设计之一，其减速比低（5:1–25:1），而常见高减速比齿轮箱可高达 200:1。高减速比能从小电机输出出色而精确的力矩，但代价是：

- **“透明度”差**：众多轮齿让四足脚爪传回的受力变得混杂难辨。
- **高摩擦**：这使关节在受到冲击时难以平滑地反向运动，增加了损坏风险。

QDD 的低减速比降低了摩擦，并带来可反向驱动性（backdrivability）——即向对抗力让步的能力。在崎岖地形上，腿可以像人类膝盖一样自然弯曲，而不是僵硬撞击、令机器人失稳。可反向驱动性对安全的现实世界通行至关重要。

宇树的 QDD 减速比通常低于 10:1，进一步降低摩擦与成本。由于执行器占机器人物料清单一半以上，这些更便宜、更柔顺的执行器让宇树同时获得适应性和重大成本优势。

![](https://substack-post-media.s3.amazonaws.com/public/images/ee05eeb8-6d34-48b6-9e85-388895fa428a_4096x3072.jpeg)
*来源：Takayuki Todo*

然而，低减速比带来了坚固性短板。QDD 常用的行星齿轮比其他方案磨损更快，需要频繁维修。此外还会引入“齿隙”（backlash）——齿轮反转时产生微小误差，影响精确运动。可以通过把脚爪踩压到地面来重新获取定位加以补偿，但随着齿轮磨损，齿隙只会越来越大。

![](https://substack-post-media.s3.amazonaws.com/public/images/85f05c63-b77d-48ee-a6ea-54438cf89f11_420x175.webp)
*来源：OrientalMotor*

由于减速比低，QDD 依赖高扭矩密度电机，这让更大的机器人明显更重。例如宇树工业级 B2 的电机重量是 Go2 的 3 倍以上。低减速比放大尺寸还会降低精度和坚固性，使更大的 B1/B2 机型容易出现“摇晃”。

![](https://substack-post-media.s3.amazonaws.com/public/images/57f7faa4-a2c0-4ec4-8950-25168fe659c4_2537x1329.png)
*来源：YC's Vlogs，宇树 B1 的腿部*

## 传感器：中国的成本优势

为了在世界中导航，四足机器人依赖一套标准传感器组合：四周摄像头提供全向视野，中央 LiDAR 提供 360° 覆盖，通常还有飞行时间（ToF）传感器负责深度感知。这些可占四足机器人成本的 20%。各家设计不一——例如宇树省去了侧面摄像头、更依赖 LiDAR——但为了安全，全覆盖是**必需**的。

![](https://substack-post-media.s3.amazonaws.com/public/images/495f20dc-2863-404e-b29f-7e6fde81c770_1463x1035.png)
*来源：Boston Dynamics*

在这方面，宇树又获得一项成本优势。公司从 Robosense、LIVOX 等中国厂商采购只要几百美元的低价 LiDAR，或者[廉价自产](https://www.unitree.com/LiDAR)。相比之下，西方 LiDAR 价格更接近 $2,000。据报道，Boston Dynamics 要求完全不含中国部件的物料清单，因而与此类节省无缘。

## 续航——中国硬件实力

续航是关键约束，从 90 分钟到 5 小时不等。宇树 A2 "Stellar Hunter" 可运行超过 5 小时，或带 25kg 载荷运行 3 小时以上。但这些数字不含机载传感与推理。典型西方四足部署会加挂 1-3 块 Nvidia Jetson Orin（每块约 ~50 W）以及声学、热成像和摄影测量传感器。即便算上这些附加负载，宇树的续航仍约为西方对手的 ~**2 倍**。

![](https://substack-post-media.s3.amazonaws.com/public/images/b4f988a7-0035-490e-b5d4-f012cd3f8d5a_768x432.jpeg)
*来源：Boston Dynamics*

## 接下来会怎样？

宇树握有重大成本优势，其消费级和工业级四足机器人的价格都只有西方产品的零头。付费墙后的完整 Go2 物料清单显示，即便定价低廉其利润率依然很高，B2 则更加惊人。这一优势已赢得科研圈的大部分，那里的开源工作或将反哺强化宇树的软件。随着生态扩张，包括宇树在内的所有四足机器人都可能走向更广的应用与部署。

西方四足机器人变强的一条路径是[强化本土供应链](https://semianalysis.com/2025/03/11/america-is-missing-the-new-labor-economy-robotics-part-1/)，在成本上正面竞争，并有望触达更大部分的科研群体。在那之前，宇树很可能继续统治成本竞争力。
