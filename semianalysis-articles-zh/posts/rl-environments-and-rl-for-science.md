---
title: "RL 环境与 RL 用于科学：数据铸造厂与多智能体架构"
title_en: "RL Environments and RL for Science: Data Foundries and Multi-Agent Architectures"
subtitle: "劳动者自动化、RL 即服务、Anthropic 的下一个重注、GDPval 与实用性评估、计算机使用智能体、生物学中的 LLM、中期训练、实验室采购模式、平台政治与准入"
date: 2026-01-06
source: https://newsletter.semianalysis.com/p/rl-environments-and-rl-for-science
crawled: 2026-09-15
authors: ["AJ", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# RL 环境与 RL 用于科学：数据铸造厂与多智能体架构

> 原文：[RL Environments and RL for Science: Data Foundries and Multi-Agent Architectures](https://newsletter.semianalysis.com/p/rl-environments-and-rl-for-science) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**劳动者自动化、RL 即服务、Anthropic 的下一个重注、GDPval 与实用性评估、计算机使用智能体、生物学中的 LLM、中期训练、实验室采购模式、平台政治与准入**

*我们正在招聘 AI 分析师与 Tokenomics 分析师职位。[点此申请](https://app.dover.com/SemiAnalysis/careers/ddbb65b5-1f71-4c20-835f-7c6860ed5d7f)，或直接与我们联系。*

去年 6 月，我们曾指出，扩展强化学习（RL）是解锁更强 AI 能力的关键路径。如下文将展示的，过去几个月印证了我们的论点：主要的能力提升正来自 RL 算力的爬坡。预训练仍在持续优化，但各家实验室的注意力已激光般聚焦于扩展 RL 的算力。

最好的例证来自 OpenAI。该公司近期所有旗舰模型——o1、o3 以及 GPT-5 系列——都使用同一个基座模型 GPT-4o。长达 18 个月里，OpenAI 模型性能的提升完全由后训练和扩大 RL 算力驱动。如今 OpenAI 已解决其预训练问题，随着这一扩展维度被解锁，进步还会更快。

![](https://substack-post-media.s3.amazonaws.com/public/images/7e50fdb7-cb85-4d29-b665-bf4743c5d3f6_1142x634.png)

这并不是说预训练已死：Anthropic、xAI，尤其是 Google，都从扩大预训练中收获了显著增益。但 OpenAI 去年的进展、以及凭借一个较旧的基座模型保持领先的事实，是后训练有效性的存在性证明。

扩展 RL 并不容易，它需要源源不断的任务供模型求解与学习。预训练有整个互联网可供训练，而 RL 的同等语料库尚未完全建立。大多数 RL 数据和任务必须从零构建，相当耗费人力。

让模型「做作业」始于数学题——因为数学题易于判分。此后方法不断演进，拓展到医疗与金融建模等新兴领域。为此，模型被置于日益专业化的「环境」之中，由环境要求模型完成这些任务。

任务与数据的聚合可以靠人工完成，也可以通过筛选高信噪比的用户数据实现。后者正是 Windsurf 和 Cursor 这类公司即便没有实验室级资源、也能后训练出有竞争力模型的原因。

这些后训练工作提升了模型在编码等领域的能力（capability），也提升了模型的*实用性（utility）*：模型在 Excel、PowerPoint 等日常工具中更加可用。

为衡量模型在实用性与能力上的进步幅度，OpenAI 推出了一个名为 GDPval 的评估。该评估覆盖 44 种职业的 1,000+ 项任务，取自占经济总量 >5% 的行业。其中许多任务是数字化的，但人类需要数小时才能完成。这些任务与专家合作创建，专家平均拥有 14 年从业经验。

模型在给定提示词和一组辅助文件的前提下求解这些问题。任务包括：为一个虚构人物报税、以度假村客户顾问的身份制作幻灯片、用给定的一组素材视频剪辑商业广告。判分方式是专家在模型的答案与人类专家的答案之间做选择。若胜率持平，则意味着模型的表现与人类专家相当。目前最强的模型 GPT-5.2 得分约 71%，即其成果有 71% 的时间打平或优于人类产出。

![](https://substack-post-media.s3.amazonaws.com/public/images/370d577f-508c-40df-b6d4-857bf1225db8_1022x575.png)
*GDPval 示例任务集。来源：OpenAI*

尽管 GDPval 存在一些问题（例如偏重异常具体的数字化工作），但它是评估范式从测量抽象智能转向现实世界实用性的最佳范例。这与以往大多数模型评估形成鲜明对比——后者聚焦于数学知识或以选择题形式判分的博士级科学问题。

底层趋势是模型能够自主运行的时间越来越长。随着短程与长程能力的提升，AI 公司认为模型可以帮助发明它们自己的下一代。OpenAI 的目标是到 2028 年 3 月拥有自主的 AI 研究员。Anthropic 预计到 2027 年，Claude 这样的系统将能自主发现原本需要数年才能取得的突破。

![](https://substack-post-media.s3.amazonaws.com/public/images/4d7a943d-bd4c-4a9a-8be7-c63038e40a79_1568x883.png)
*来源：Anthropic*

但这段旅程需要海量的数据与任务整理。例如，计算机使用环境需要大量枯燥的软件工程工作，包括复刻互联网上的现有网站。实验室自己做会很慢，因此这类工作大部分被外包了出去。

# 外包与 Scale AI 的幽灵

历史上，Scale AI 是各实验室最大的数据承包商之一，如今已被 Meta 大体收编。Scale 曾从各家实验室获得可观的支出，2024 年营收超过 $1.4B。

![](https://substack-post-media.s3.amazonaws.com/public/images/12f97061-879f-43b5-8d42-acc3af9930f3_1652x977.png)
*来源：Sacra、SemiAnalysis*

然而在收购之后，多家 AI 实验室基本停止了与 Scale 的合作。这是为了避免 Meta 接触到它们最看重的数据。Scale 团队的部分成员加入了 Meta 的超级智能团队（Superintelligence group），多担任领导职务，或进入安全与评估团队。该组织如今继续产出评估并保留部分数据合同，但已不再像从前那样为各实验室提供服务。

尽管潮水早已转向 Surge 等其他数据供应商，Scale 仍留下了一个亟待填补的巨大空缺。是谁在填补这个空缺？

# 淘金热里卖铲子。RL 扩张热潮里……

淘金热里，卖铲子。RL 扩张热潮里，卖 RL 环境。已有 35 家以上的公司冒了出来，目标正是在各个领域做这件事。

一类公司专注于克隆网站。例如，环境公司雇佣海外开发者复刻 DoorDash 或 Uber Eats 等网站的 UI，再把仿制品卖给实验室。实验室随后训练智能体在这些网站中导航，使其在生产环境中能够可靠、稳定地执行所需功能。

这种「UI 健身房」（UI gym）每个网站通常售价约 $20,000，OpenAI 已为 ChatGPT Agent 的训练与开发购买了数百个网站。这些环境属于一次性购置，可供未来的模型反复使用。以往运行产生的轨迹（trajectory）与日志会被保留，并回灌到训练的各个阶段，例如中期训练（mid-training）。

![](https://substack-post-media.s3.amazonaws.com/public/images/04032584-5b2e-4b30-afa9-ba2fcc0f9ab9_2140x780.png)
*来源：Karina Nguyen 的一次公开演讲、SemiAnalysis*

另一些公司则拓展到比单一网站更复杂的环境，例如 Slack、Salesforce、AWS 终端、Microsoft OneDrive、Gmail、Discord 和 Atlassian。目标是让智能体在这些软件平台中自主运作，学习并更深入地理解如何在其中导航与操作。

这些平台一旦建成，就可以组合起来呈现更高保真度的任务与工作负载。把 Slack、通往浏览器的 API 端点和代码编辑器组合起来，就能为模型构造出愈发真实的软件任务。这也让交互从单轮变为多轮——例如在模型执行到一半时，通过 Slack 发消息要求变更某个功能。

构建这类环境的公司包括 [Habitat](https://www.habitat.inc/)、[DeepTune](https://deeptune.com/)、[Fleet](https://www.fleetai.com/)、[Vmax](https://vmax.ai/)、[Turing](https://www.turing.com/)、[Mechanize](https://www.mechanize.work/)、[Preference Model](https://www.preferencemodel.com/)、Bespoke Labs、Veris.ai 等众多玩家。即便在这些公司之间，质量与侧重点也差异悬殊。有的专注 UI 健身房，如 Turing；有的如 Mechanize 则专注软件工程任务。这些公司几乎都处于种子阶段、员工不足 20 人，最多只服务 1 到 3 家客户。

上述公司大多将环境闭源，以独家合同的形式供给实验室。不过也有一些例外，如 Prime Intellect 将自己的环境开源，并在培育 [Environments Hub](https://www.primeintellect.ai/blog/environments)，目标是打造 RL 环境的一站式商店。

还有一些公司在为环境开发工具链。例如 [HUD](https://www.hud.so/) 的工具可以把任意软件（如游戏、浏览器、Google Sheets）封装进 Docker 化容器，使其成为可扩展的 RL 环境。每个容器分两层：环境后端（被封装的实际软件），以及位于其上、暴露工具定义供智能体调用的 MCP 服务器。当智能体发起 `click(x,y)` 或 `type(text)` 这类工具调用时，MCP 服务器将其翻译为底层软件上的动作，并返回结果观测（observation）。这套体系通常会被扩展成大量并行实例。每个任务包含提示词、初始设定条件和成功判据，成功后返回奖励信号。每次工具调用与观测都通过遥测（telemetry）捕获，既便于调试，也会被收集起来回灌到后续阶段的训练中。

![](https://substack-post-media.s3.amazonaws.com/public/images/a0e265cb-a9a1-4cc2-8baa-3b1a353d98a1_1480x1620.png)

需求最旺的环境是编码环境。理解它们如何构建、组织与装配，能为我们提供一个独特视角，看清支撑当下这轮进步的基础设施与工程投入。

# 所以你想做一个编码环境？

编码环境的需求之高，以至于我们认为一些已经倒闭的初创公司被收购，看中的就是又一个可用于制作环境的私有 GitHub 仓库的价值。要理解这些仓库为何如此值钱，就得理解编码环境究竟是如何构建的。这个过程比看上去要复杂得多。

SWE-rebench 是一个从 GitHub 聚合数千项 Python 任务的基准测试，展示了这类环境的构建方式。它采用的流程也是自动化的，我们预计各实验室正在做同样的事。

流水线的起点是下载 GitHub Archive，其中包含 3 万个仓库和 45 万个采用宽松许可证的 PR。随后数据集按若干条件过滤：PR 必须已解决、已合并进主分支、对问题有充分描述、影响不止一个文件等。PR 必须引入或修改测试文件，因为那是判分的依据。例如，若模型的补丁让先前失败的测试通过（且不破坏其他测试），该任务即判定为已解决。

为实现环境配置自动化，由 LLM 为每项任务生成安装指令。模型阅读仓库中的相关文件（README、setup.py、requirements.txt、Docker 文件），然后合成一份结构化的 JSON「配方」，指定 Python 版本、依赖安装命令和测试执行命令。

![](https://substack-post-media.s3.amazonaws.com/public/images/997762d1-a8cc-47ab-b1b5-494566767783_1460x779.png)
*来源：Badertdinov、Golubev 等*

随后每项候选任务都要经过基于执行的验证。环境在容器中实例化，并运行该 PR 测试补丁中的测试。只有满足以下条件，任务才算有效：在应用解题补丁之前至少有一个测试失败；应用补丁后，所有初始失败的测试全部通过；此前通过的测试继续通过。经过层层过滤，最初 45 万个 PR 最终留下 21,336 项任务。

但大多数 PR 无法满足这些严格标准，这正是产出率低的原因。SWE-smith 展示了这一点：先让 LLM 在仓库最新 commit 上完成安装，然后用四种方法合成 bug：提示模型向正常工作的函数中注入细微错误；施加确定性的 AST 变换，如翻转 if/else 块或删除循环；用 LLM 依据当前代码库对真实 PR 做语义上的逆向；把已验证的单函数 bug 组合成更难的多文件任务。每个候选都要通过「是否至少破坏一个既有测试」来验证。

重要的是，这些方法并不互斥。PR 挖掘从真实开发历史中捕捉贴近现实的 bug 模式，而合成生成则提供覆盖整个代码库的数量与广度。能够访问私有仓库的实验室可以在同一套环境上同时运行两条流水线：先挖掘 PR，再用合成 bug 加以扩充。这种组合打法很可能相当接近前沿实验室构建代码 RL 环境的真实做法。

规模化之后，这些流水线可产出数以万计的任务。DeepSeek 最终使用了 24,667 项从 GitHub 提取的编码任务来训练 V3.2。我们从 Kimi 等其他实验室了解到，其开发的基础设施可同时支撑 10,000+ 个实例的实例化。总体而言，任务越难，训练时所需的 rollout 就越多。原因在于难题更难解出，而 rollout 越多，模型的「射门机会」就越多。但代价是单次 rollout 变慢——吞吐量是以速度换来的。

![](https://substack-post-media.s3.amazonaws.com/public/images/e8df58ac-7c11-491d-9233-53f934d71a74_1536x1011.png)
*来源：SemiAnalysis*

# 数据铸造厂与专家承包商

环境工具链之所以普遍有用，是因为环境正被铺设到众多不同领域：让模型辅助设计流程的芯片设计环境、让模型处理税务的会计环境、面向医疗流程的 EHR 软件，都只是几个例子。

环境本身由软件工程师搭建，但工作流程往往由参与环境创建过程的领域承包商来设计、描述和判分：金融专业人士帮忙定义金融任务，医生负责医学，律师负责法律，如此等等。

实验室会通过人力数据承包公司（稍后详述）介入，请他们对具体任务的创建出谋划策。合同期通常至少一个季度，可为兼职或全职。承包商设计任务、撰写预期解法、设定奖励信号，某些情况下还要为模型的解答判分。这些奖励信号可以采取评分量规（rubric，其编写也可能有承包商参与）或严格验证器的形式。受雇协助搭建 GDPval 这类评估的，正是这一类专家。

![](https://substack-post-media.s3.amazonaws.com/public/images/44e8dce0-9fc7-4835-bd97-ac730132e885_1880x802.png)
*OpenAI 的数据处理流水线。OpenAI 为承包商设有一个私有内部平台 Feather，数据经由该平台处理。图片来源：OpenAI*

各实验室借助 Mercor、Handshake、Surge 和 Aboda.ai 等公司在众多专业领域雇佣这类专家。Surge 是其中更成熟、规模更大的玩家，我们估计其营收已接近 $1B ARR。

这些公司大多起家于 AI 面试或职位匹配业务，但最终发现，做实验室与专家承包商之间的连接者更有价值。

编码需求量最大，但摄影、音乐、设计等非专业领域的支出也在升温。如前所述，实验室不仅想增加某一领域后训练的任务数量，也想拓展广度与多样性。

这些供应商的营收主要来自 Anthropic、OpenAI、Google 等西方实验室。不过我们认为 Surge 也在国际市场积极活动，向 Moonshot（月之暗面）和 Z.ai（智谱）等中国实验室供货。事实上，我们认为获取这些 RL 环境，是 Kimi K2 Thinking 与 GLM-4.6 能力跃升的重要原因。当这些公司宣传其在 PowerPoint 幻灯片或 Excel 表格制作上的能力提升时，那正是额外 RL 训练的直接成果。

中国的风投机构正积极扶持本土数据铸造厂竞争者，以便以低于西方同行的价格全面服务本地生态。大多数中国实验室在 RL 扩展上仍处于早期：Qwen 目前投入后训练的算力约占其预训练算力的 5%。本土数据铸造厂业务一旦成功，将极大加速这一转变——当然，前提是算力允许。

![](https://substack-post-media.s3.amazonaws.com/public/images/70e2bbd2-5bd8-4410-aace-24fef73f4e63_1606x1003.png)
*来源：Aboda.ai、SemiAnalysis*

在上图的案例中，承包商提供带讲解的完整解答。承包商也可以为模型输出判分，并就错误给出反馈。这类数据可以用任何语言采集，必要时再由另一个模型翻译。

Mercor 等公司也是大量评分量规的生产者，这些量规可用于各种不同领域。目前大多数量规由人工撰写，不过也有一些公司（如 The LLM Data Company）在尝试让模型来编写量规。实现方式之一，是将高性能模型接入高度可靠的 MCP 以提取信息，再据此生成结构化量规。

![](https://substack-post-media.s3.amazonaws.com/public/images/0265b727-8cc7-4774-98f9-023dea365b99_1493x1744.png)
*LLM 生成的评分量规。来源：The LLM Data Company*

尽管当前 AI 实验室仍以消费人工生成的数据为主，我们认为这一路子有可观的上行空间。长期来看，随着模型变强，可靠性与质量都会改善。如前所述，所有实验室都在追逐 AI 自动化的 AI 研究。

鉴于选项如此多样，理解数据采购决策对于研判实验室战略至关重要。这一范式[不同于预训练时代人人都能拿到同样的数据](https://newsletter.semianalysis.com/p/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data)。

# 各实验室的采购模式

### Anthropic

在 RL 环境市场上，Anthropic 一直是个激进买家。它常常是几十家新公司的首个客户，向它们提供独家合同，某些情况下还传授环境构建的诀窍。我们认为它正与十几家 RL 环境公司开展承包合作。该公司多半希望建立一个足够广的供应商生态，让产品同质化，从而压低某些类型环境的价格。

一个活跃的供应商生态还能吸引投资人，进一步补贴成本。代价则是同时管理众多供应商的摩擦成本，因此我们相信 Anthropic 正要求供应商在多数领域遵守特定的[沙箱框架](https://github.com/laude-institute/sandboxes)，并自建了一个供应商对接平台。

虽说该公司确实以代码为核心，但我们如今看到它开始在别的领域发力。例如，计算机使用已在优先级清单上高居多时。包括生物学在内的其他领域也在爬坡，后文将有所展示。编码仍是其努力的重心，但已不是唯一感兴趣的领域。

### OpenAI

我们认为 OpenAI 的供应商池比 Anthropic 小，但其数据净支出超过 Anthropic 和多数其他实验室。为降低对 Surge、Mercor、Handshake 等第三方的依赖，OpenAI 正在自建人力数据团队。xAI 从一开始就采取了类似做法，公司创立起就发布 AI 导师（AI tutor）岗位，如今正加大招聘力度。

它之所以支出超过其他实验室，是因为有众多并行领域都在扩张。ChatGPT Agent 大量使用 UI 健身房。斩获 IMO 金牌的模型（GPT-5.1 Codex Max 的一个版本）得益于海量数学与代码数据。面向消费者的版本则融合了所有这些项目的数据，外加围绕行为（behaviour）的定向后训练。

![](https://substack-post-media.s3.amazonaws.com/public/images/ec316bd5-13f2-4f91-971e-62102e1570ab_1446x840.png)
*IMO 获奖模型的示例答案。来源：OpenAI*

各项目的数据被聚合后回灌到中期训练（后文详述），带来了全方位的性能提升。

OpenAI 采购的海量数据在其后训练工作中扮演了关键角色——如前所述，正是后训练推动了几代模型关键能力的前进。随着其人力数据团队壮大，OpenAI 将不必再向众多数据供应商支付利润加成，同样的成本可以聚拢更多数据量。

### Google DeepMind

Google DeepMind 的采购相当分散。具体到环境采购，一直由不同团队与项目的研究员各自推动。他们感兴趣的环境集中在编码和计算机使用，尤其是与 ML 相关的环境和任务。

Google 在 Gemini 2.5 Pro 上的后训练算力投入很少，发布时可能不足预训练算力的 5%。虽然 Gemini 3 已有所加码，我们仍认为相对其他实验室偏小。不过，Google 在这一范式中的位置无可替代：底层平台（Sheets、Slides、Docs、Drive、Maps）本就归它所有，无需另起炉灶。更重要的是，其庞大的产品经理队伍对数亿用户与这些产品的真实交互有着深刻洞察，这为什么样的模型表现才算优秀提供了直接信号。接下来，Google 何时利用这些用户行为在上述应用上后训练 Gemini，多半只是时间与政治问题。对 Google 而言，这比单纯的技术障碍更难逾越。

Google 也在加强防御，下调了 Gmail 等产品被爬取的速率限额。这让其他公司更难抓取其应用数据用于复刻（例如制作供训练用的仿制应用）。

不过从长远看，这些模型究竟能有多大用处？通往 AGI 的路径，难道只是层层堆叠的环境吗？

# 基于 LLM 的自动化并非必然

围绕 AI 导致岗位自动化（尤其是白领工作）的猜测已有很多。OpenAI 的 GDPval 论文提供了一个与此假说相悖的有趣数据点。OpenAI 发现，人类专家借助模型反而更快，完成任务的成本比不用时更低。随着能力提升，人类被增强（augment），而非被取代（automate）。

![](https://substack-post-media.s3.amazonaws.com/public/images/d48cf181-b0d4-4e01-af41-d3768ea66d19_1130x1100.png)
*来源：OpenAI。SemiAnalysis 数据点反映的是成为 SemiAnalysis 客户后获得的效率与成本改善。*

近期内，专家工作迎来的未必是自动化，而是任务增强。软件工程这类任务大概率如此。

再举一例：在 AI 热潮之前，许多人预言放射科会被自动化，依据是视觉模型的能力提升。[尽管技术持续进步，这一预言并未成真](https://www.worksinprogress.news/p/why-ai-isnt-replacing-radiologists)。

事实证明，放射科远不止读片那么简单。

![](https://substack-post-media.s3.amazonaws.com/public/images/50035824-6960-41dd-a500-980d0bc38d14_1140x925.png)
*来源：Works In Progress*

「模型主要起增强作用」这一判断，在咨询、软件工程等专业领域或许成立。但我们认为，对于[短周期、重复性的任务](https://x.com/karpathy/status/1971220449515516391)——例如呼叫中心之类的工作——恐怕并非如此。

无论能力如何，普及总存在一些障碍，包括但不限于网络平台与公司的防御姿态。对智能体而言尤其如此。

# 抱歉，你的智能体无权访问

智能体还可能被大网站封禁，ChatGPT Agent 与 Amazon 之间就正上演这一幕。

![](https://substack-post-media.s3.amazonaws.com/public/images/29d60d24-7f6b-4aba-87bb-eb38e3bdd036_1016x380.png)
*来源：SemiAnalysis*

对 Amazon 而言，此举合乎逻辑：智能体在其平台上购物，会让用户绕开平台上的所有广告。Amazon 可以把生态圈限定给自家的 Nova 和 Rufus 模型，也可以把访问权当作谈判筹码。

后者恰恰正在发生。OpenAI 正与 Amazon 谈判以获取购物平台的访问权，尽管这可能取决于有关[使用 Amazon 云与芯片](https://semianalysis.com/accelerator-hbm-model/)的细节。我们预计 Google、Meta、Microsoft 和 X 都会尽可能限制各自生态的访问权，尽管这可能受制于反垄断顾虑。

Amazon 与 OpenAI 这类交易的核心，是把免费用户变现。此前已有先例：[OpenAI 发布了与 Shopify 和 Etsy 集成的「Instant Checkout」](https://x.com/OpenAI/status/1972708279043367238)。我们在 8 月就指出这是智能体的一条潜在路径。

在企业侧，许多公司正在搭建自己的智能体。它们常常与其他初创公司签约，由后者针对特定任务或工作负载为其提供「RL 即服务」。

# RL 即服务

RL 在教会模型使用工具方面极为有效。借助开源工具链，一些初创公司如今向大企业提供定制化 RL 服务。这个赛道既有 RunRL、Osmosis 这类较小的 YC 初创公司，也有由资深研究者创立的 Applied Compute 和 Adaptive ML。

这类服务常用 Qwen 模型，因为它们易于后训练且运行所需资源少。Qwen 型号众多，包括小型稠密模型，所需技能与配置门槛更低。

完成定制后训练后，这些模型运行在租用的硬件上。目前，Baseten 承载着许多这类小型定制模型。典型目标包括 Salesforce、AWS Terminal，以及创建或关闭 Jira 工单。还可以让模型可靠地使用 MCP，例如从 SEC 文件中提取数据。

与这些「RL 即服务」初创公司同场的还有各大实验室：OpenAI 近期推出了「强化微调」（Reinforcement Fine Tuning，RFT）服务。OpenAI RFT 的目标是让任何拥有足够数据的客户对 OpenAI 模型做 RL，使之适配客户自己的任务与领域。

实际运行中，该服务未达预期。我们认为它不够稳定，对多数客户而言也太贵。因此，这类服务需求大多流向了年轻的初创公司。这些 YC 系新秀利润率不高，甚至常常亏钱，但它们的服务价格只有 OpenAI 平台的约五分之一，正在抢占市场份额。

长期来看，局面会改变。OpenAI 瞄准的是能豪掷数百万美元的大企业；总体而言，实验室们终将拿走大部分营收。对 OpenAI 来说，这将通过「Strategic Deployment（战略部署）」团队完成，其目标是直接与客户共建定制模型。OpenAI 早早押注这类服务作为企业级用例，2025 年该公司**企业**业务的增速已超过消费端。

![](https://substack-post-media.s3.amazonaws.com/public/images/c103b69d-c1f2-4a3e-8780-abd93fb63602_1040x995.png)
*来源：OpenAI*

Anthropic 也在入场。我们认为 Anthropic 有一套自己的类 RFT 服务，比 OpenAI 的更稳定、样本效率更高。Anthropic 可能会通过 API 开放该服务，同时也在积极招聘「前线部署工程师（Forward Deployed Engineers）」——与 OpenAI 如出一辙，估计职能与 OpenAI 的战略部署团队相同。

Anthropic 正大量引进 Trainium，这对 RL 在经济上颇具吸引力，部分原因在于其较低的 $/HBM。HBM 通常占芯片物料清单（BOM）的大头，而 Amazon 直接采购 HBM，压低了成本。RL 工作负载以推理为主，属于内存瓶颈型。这意味着，只要把吞吐量优化到位，拥有 Trainium 这种低总拥有成本（TCO）芯片的客户就能从该服务中赚取可观的利润率。

如前所述，训练定制模型蕴含可观的上行空间。我们尤其兴奋的领域之一是科学发现——定制模型在其中可以取得大量进展。

还有不少公司也提供 RL 即服务，如 ThinkingMachines 的 Tinker，以及 Applied Compute 和 Adaptive ML。在这个市场上，这三家目前的成就都超过 OpenAI 与 Anthropic。

# RL 用于科学

LLM 开启了一片新边疆：模型可以检索、规划并提出实验。配上合适的工具，智能体还能亲手执行这些实验。RL 则能把这些实验的反馈转化为模型可用以自我改进的信息，在条件合适时形成自我改进的闭环。

已有多家公司在利用这一点，Periodic Labs 便是其中之一，它的目标是打造一个由实验室产出数据训练而成的 AI 科学家。

目标是建立一个奖励根植于物理实验的闭环 RL 系统。模型使用工具——包括其他更小的专用模型——来检验假设、验证想法。随后，这些想法在保真度越来越高的模拟器中接受测试，其结果再指导物理实验。

这样，子智能体（subagent）各司其职，通用 LLM 则负责统筹编排。编排范围还可延伸到物理工具，例如材料的表征。

![Fig. 1](https://substack-post-media.s3.amazonaws.com/public/images/67ec8066-bec8-4d85-afb9-0c08b0b62bf2_936x670.png)
*现有闭环系统示例。来源：Wang 等，2025*

这种先通过保真度递增的方法验证想法、在进入实验室前给实验去风险的流程，大致对应着一名研究生的典型工作流。

![](https://substack-post-media.s3.amazonaws.com/public/images/38ce44d5-ee80-4656-9a39-4b1a91873de6_1460x666.png)
*Periodic 的闭环系统。来源：Rohan Pandey。*

可以用开源模型作为起点，再通过中期训练扩展能力。中期训练本质上是预训练的延续（下一个 token 预测），可用于延长模型的知识截止日期、加深特定领域的知识，以及为高算力 RL 做铺垫。例如，OpenAI 模型的知识截止日期之所以更新，正是模型之上持续进行中期训练的结果。

在高度专门的科学领域，中期训练会让后训练之后的模型质量更高。Meta 在其近期代码专用模型中发现，中期训练的收益即便在其他阶段（如 SFT）施加之后依然保留。Meta 为近期一个模型的中期训练用了 1T token，而我们估计 OpenAI 的用量在 5-10 倍以上。

![](https://substack-post-media.s3.amazonaws.com/public/images/949e444d-605d-44bc-ab24-8b39d9b00554_1460x471.png)
*来源：Meta*

其中一个被加入中期训练阶段的数据例子，是以往运行产生的环境轨迹——即旧版本模型做 RL 时生成的、被收集起来的 rollout。

![](https://substack-post-media.s3.amazonaws.com/public/images/7ea859aa-bfe3-44a3-b203-8a6785c66335_1077x913.png)
*来源：Meta*

为给 RL 和中期训练供给数据，Periodic 正在建一座大型物理实验室，用以开展实验并产出经实验验证的奖励信号。这与业界其他努力一致：DeepMind 也将于 2026 年启用一间自动化材料科学研究实验室。

亲自做实验能完整掌握输入变量与结果，这是纯靠已发表论文训练所无法保证的——文献之间即便指标可比也常常互相矛盾。另一个需要大量实验室工作的领域是生物学。这也是各家实验室路线分化明显的一个领域。

# RL 遭遇湿实验室

生物学有两大核心瓶颈：「如何更快地识别出有前景的候选药物」，以及「找到候选之后如何更快地推进药物开发」。OpenAI 和 Anthropic 都建立了制药合作，但切入的是这条管线的不同环节。

OpenAI 瞄准早期发现，构建能亲自执行研究的系统。最近，OpenAI 展示了 GPT-5 在闭环中运行：提出方案修改、接收实验结果、自主迭代，全程无人类介入。作为这项工作的一部分，OpenAI 还不得不搭建基础机器人系统来执行实验。其根本目的，是提高找到有用候选的速率。

Anthropic 则瞄准药物开发与审批流程。Claude for Life Sciences 是一个自带预制连接器的平台，直连 Benchling、10x Genomics、PubMed 及科学家常用的其他服务，目标之一是加快药物试验的迭代速度。整套方案被打包成即插即用的企业级解决方案，大体上可以理解为生命科学领域一款（真正能用的）Copilot。核心思路是加快文档撰写与审批的速度。

我们认为两家公司最终有可能收敛到同时进攻两个环节，但当前的分工颇能说明问题：OpenAI 追逐登月式的 AI 项目，Anthropic 则延续其更平淡但务实的企业插件与解决方案路线。长期潜力将取决于各自的迭代速度，以及承接管线中越来越多任务的能力。

这背后隐含着训练模型所需的海量生物学数据。虽然 Mercor 这类公司乐于赚实验室的钱，但它们没有相应的 ML 或物理基础设施来供应大量生物学数据。在我们看来，这正是 Medra 这类公司的用武之地——它们的目标就是向实验室大量供给生物学数据。

Medra 计划建立一间聚焦生物学的机器人自动化科学实验室。该公司不打算做基础模型，也不做药物设计；它要做的是搭建实验基础设施，产出基础模型公司训练所需的经验证数据。与 Periodic 一样，Medra 计划自建拥有数百台机器人的实验室。我们相信，在上述闭环的驱动下，机器人化将带来更一致的结果与更快的迭代，但随着装置不断优化、系统愈发稳健，学习曲线也会十分陡峭。实验室自动化是一个存在了几十年的老问题，改善更可能来自收窄范围，而非突然的突破。

这进一步说明后训练与预训练有多么不同：如果 OpenAI 与 Google DeepMind 选择优化的实验组合不同，最终的模型与应用就会分道扬镳。在这些极度专门领域的深耕，与「模型同质化、彼此相似」的论调背道而驰。

RL 环境正在*溢出*到物理世界。这些环境不再只是软件世界里可以随意拉起的 Docker 容器，而是需要由人类或机器人执行的实验，材料、电力、设备和实验室空间都有真实成本。这带来一些有趣的推论，比如每美元投入的边际数据量远低于软件领域：一项生物学实验的成本可达数百到数千美元、耗时数小时，而一个编码任务可以被尝试 64 次、判分成本微不足道。这使得更高效的算法与特定的架构决策变得愈发必要，才能让物理世界的 RL 切实可行。

# 为什么生物学 RL 挑战重重

科学实验所需时长千差万别。在生物学中，大量实验需要数天才能完成。更长的周期意味着更长的 rollout，也意味着奖励将是稀疏的。稀疏奖励能给模型学习提供的信号更少。

![A screenshot of a computer
AI-generated content may be incorrect.](https://substack-post-media.s3.amazonaws.com/public/images/31e4836d-b56b-4d50-b74a-c3119c191f47_937x296.png)
*来源：Nvidia、TogetherAI、SemiAnalysis*

一种应对办法是奖励模型的中间步骤，而不只是最终结果。这奖励的是模型的过程与思考，而非仅仅最后一个动作。虽然「正确」的步骤长什么样很难精确判定，但可以借助评分量规来近似。事实上，这正是 OpenAI 在其近期评估 Frontier Science（测量模型执行科研任务的能力）中，为开放式研究任务判分的方式。在实验实践中，任务可以拆分为各自计奖的子任务，从而缩短判分的时间跨度。

![](https://substack-post-media.s3.amazonaws.com/public/images/bebca705-7e8a-491b-bd76-887242074973_1067x1008.png)
*来源：OpenAI*

长 rollout 对 GPU 稼动率也是灾难，因此许多实验室采用了权重在线更新（in-flight weight updates）等方法：交换权重后，拖尾的 rollout 带着过期的 KV 缓存继续跑。这样训练得以继续，而无需等待拖尾 rollout 完成。其效果是，同样的实际耗时下迭代次数可以提升 2 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/0eb2e6c0-c770-46c2-9a0a-ad28f85be884_1345x1120.png)
*来源：Piché 等，2025*

另一个瓶颈在可用数据本身。科学文献中常常出现连基本问题都互相矛盾的结果，这让构建可靠的训练集变得困难。生物学稍好一些，因为现有开源数据更为常见。AlphaFold 使用蛋白质数据库（Protein Data Bank）的数据训练，其中包含 170,000 个样本；FutureHouse 的 Ether0 使用了 Open Reaction Database；EvE 等其他努力也将持续为模型供应商提供宝贵的平台。

不过制药公司也握有大片闭源数据集。我们预计会看到更多前沿实验室与药企的合作：前者拥有药企难以吸引到的 ML 人才，后者则握有实验室欠缺的生物学数据与临床知识。

![A diagram of a machine
AI-generated content may be incorrect.](https://substack-post-media.s3.amazonaws.com/public/images/2aed2777-73b3-4f31-b8ab-6683aa0b73fc_937x527.png)
*来源：Novo Nordisk*

尽管存在障碍（包括上文列举的一些），但可摘的低垂果实如此之多，我们预计聚焦高算力科学 RL 的努力会在相当短的时间内产生极高的价值。

推动这轮巨大进步的许多能力都依赖于扩展 RL。这条路虽然还远未到头，但另一个维度也已初现曙光。它用当前模型即可实现，只是成本要高得多。下面我们深入一个正在我们眼前展开的新边疆。

# 多智能体架构：GPT-5.2 Pro、Gemini Deep Think、Grok Heavy、Claude
