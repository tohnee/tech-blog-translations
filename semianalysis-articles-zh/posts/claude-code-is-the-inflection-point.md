---
title: "Claude Code 就是拐点"
title_en: "Claude Code is the Inflection Point"
subtitle: "它是什么、我们如何使用它、行业冲击、微软的困境、Anthropic 为何正在取胜"
date: 2026-02-05
source: https://newsletter.semianalysis.com/p/claude-code-is-the-inflection-point
crawled: 2026-09-15
authors: ["Doug O'Laughlin", "Jeremie Eliahou Ontiveros", "Jordan Nanos", "Dylan Patel", "Daniel Nishball"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Claude Code 就是拐点

> 原文：[Claude Code is the Inflection Point](https://newsletter.semianalysis.com/p/claude-code-is-the-inflection-point) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**它是什么、我们如何使用它、行业冲击、微软的困境、Anthropic 为何正在取胜**

当前 GitHub 公开 commit 中有 4% 正由 Claude Code 编写。按当前轨迹发展，我们认为到 2026 年底，Claude Code 将占每日全部 commit 的 20% 以上。就在你眨眼之间，AI 已经吞噬了整个软件开发。

我们的姊妹刊物 Fabricated Knowledge 曾把软件比作[互联网崛起时代的线性电视](https://www.fabricatedknowledge.com/p/ai-is-creating-peak-software-media)，并认为 [Claude Code 的崛起将成为软件之上的一层新智能，如同 DRAM 之于 NAND 的关系](https://www.fabricatedknowledge.com/p/the-death-of-software-20-a-better)。今天，SemiAnalysis 将深入解析 Claude Code 带来的冲击、它究竟是什么，以及 Claude 为什么如此出色。

![](https://substack-post-media.s3.amazonaws.com/public/images/6ec41954-9498-4c2f-b23a-81e2bae29f82_2761x1579.png)
*来源：Tokenomics 团队、GitHub，由 Claude Code 生成*

我们认为 Claude Code 是 AI「智能体」的拐点，让人得以一窥 AI 未来的运作方式。它将在 2026 年为 Anthropic 带来卓越的营收增长，使这家实验室在增速上大幅超越 OpenAI。

我们构建了一个详细的 Anthropic 经济模型，精确量化了其营收和资本开支对云合作伙伴 AWS、Google Cloud、Azure 的影响，以及 Trainium2/3、TPU 和 GPU 等相关供应链的连带影响。这正是 [Tokenomics 模型的核心用途](https://semianalysis.com/tokenomics-model/)。

未来三年，Anthropic 新增的电力规模有望与 OpenAI 相当。关于 Anthropic 与 OpenAI 的逐栋建筑追踪，请参阅我们的[数据中心行业模型](https://semianalysis.com/datacenter-industry-model/)。值得注意的是，Sam 的 AI 实验室正遭遇多处数据中心延期，我们早在头条新闻出炉前数月就指出了这一点，最著名的是在 Coreweave 2025 年第三季度财报前瞻中，我们明确预警其资本开支指引将大幅不及预期。

![](https://substack-post-media.s3.amazonaws.com/public/images/c04de5e0-5ec5-4c11-a6d3-c3dab116d665_927x585.png)
*来源：SemiAnalysis 数据中心模型*

由于更多算力意味着更多营收，我们可以预测 ARR 增长，并直接比较 Anthropic 与 OpenAI。

![](https://substack-post-media.s3.amazonaws.com/public/images/7572d353-1443-483a-a286-4cb33d1413f9_927x585.png)
*来源：SemiAnalysis Tokenomics 模型*

值得注意的是，我们的预测显示 Anthropic 的季度 ARR 增量已经反超 OpenAI。**Anthropic 每月新增的营收已超过 OpenAI。**我们认为 Anthropic 的增长将受制于算力。

让我们更深入地挖掘 Anthropic 的皇冠明珠：Claude Code。

## **Claude Code 与智能体的未来**

智能体将成为有机智能（人类）与人工智能（AI）交互的主要方式。但 Claude Code 同时也演示了反方向：展示智能体如何与人类交互。

我们认为，AI 的未来将在于对 token 的编排，而不仅仅是按基础成本出售 token。以史为鉴，我们把 OpenAI ChatGPT API 视为 token 的「请求—响应」，类似于 Web 1.0 时代用 TCP/IP 把用户连接到托管在互联网上的静态网站。TCP/IP 固然是奠基性技术，但在 Web 2.0 和动态网页的时代，这一通信协议沦为通往互联网这一终点的手段。今天，互联网用 TCP/IP 数据包组织远比静态网站庞大的信息集合。协议固然重要，但真正创造出数万亿美元价值的，是构建在协议之上的应用。

这正是 SemiAnalysis 认为 AI 又一次站上关键时刻的原因——一个即使不超越、也足以匹敌 2023 年初 ChatGPT 时刻的关键时刻。

![](https://substack-post-media.s3.amazonaws.com/public/images/c1640e14-9bd1-4646-8592-097fcfcd5c4d_3180x1779.png)
*来源：SemiAnalysis Tokenomics 模型，由 Claude Code 生成*

每一个时刻都拓展了 AI 的能力边界。GPT-3 证明了规模有效。Stable Diffusion 展示了 AI 能生成图像。ChatGPT 证明了对智能的需求。DeepSeek 证明了这件事可以在更小的规模上做到，而 o1 则表明可以通过扩大规模让模型达到更好的性能。Studio Ghibli 的病毒式刷屏只是普及节点，而 Claude Code 是智能体层面的一项新突破——把模型输出组织成更高级的成果。

## **Claude Code 是什么？**

Claude Code 是一个终端原生的 AI 智能体，并不像 Cursor 那样聚焦于 IDE 或聊天侧边栏。Claude Code 是一个 CLI（命令行界面）工具：它读取你的代码库，规划多步骤任务，然后执行这些任务。把 Claude Code 仅仅视为聚焦「代码」的工具可能并不准确——它更像是 Claude 计算机。拥有对计算机的完全访问权限后，Claude 可以理解环境、制定计划、迭代式地完成计划，全程接受用户的指挥。

Claude Code 能做的不只是写代码，它是 AI 智能体的最佳范例。你可以用自然语言与计算机交互，描述目标和结果，而非实现细节。给 Claude（这个 CLI）一个输入——比如一份电子表格、一个代码库或一个网页链接——然后让它完成某个目标。它会制定计划、核实细节，然后执行。

这是对未来的一瞥，但它今天已经在软件领域成为现实。你最喜欢的工程师们都在氛围编程（vibe coding）：

- **Andrej Karpathy**（[一年前创造了 vibe coding 一词的人](https://x.com/karpathy/status/1886192184808149383?s=20)）正在[公开讨论这一相变](https://x.com/karpathy/status/2015883857489522876?s=20)，并特别说道："我已经注意到，我手写代码的能力正在慢慢萎缩。生成（写代码）与甄别（读代码）是大脑中两种不同的能力。"

- **Vercel CTO Malte Ubl** 声称，他的「新主要工作」是「告诉 AI 它哪里做错了」

- **NodeJS 创造者 Ryan Dahl** 说："人类编写代码的时代已经结束"

- **Ruby on Rails 创造者 David Heinemeier Hansson** 正在体验某种预期中的怀旧：一边手写代码，一边追忆手写代码的时光

- **Claude Code 创造者 Boris Cherny** 说："我们几乎 100% 的代码都由 Claude Code + Opus 4.5 编写"

- 就连 **Linus Torvalds** 也在 vibe coding：<https://github.com/torvalds/AudioNoise>

但不止是程序员。在 SemiAnalysis，我们的分析师与技术团队各有不同的角色和职责。数据中心模型团队每周需要审阅数百份文档。AI 供应链团队需要检查包含数千行条目的物料清单（BOM）。内存模型团队需要在现货价格暴涨时近乎实时地构建预测。我们的技术团队需要为 [InferenceMAX](https://inferencemax.semianalysis.com/) 维护一个实时仪表板，包括每晚在 9 种不同系统类型/集群上运行最新的软件配方。从监管申报到许可证、从规格书到文档、从配置到代码，我们与计算机交互的方式已经改变。

举个例子，我们的行业模型分析师现在用 Claude Code 生成大量有用的图表和分析，来解析和传达大型数据集中的重要趋势：

下面是一个输入：

![](https://substack-post-media.s3.amazonaws.com/public/images/456e53bb-cf1f-4e16-94cf-7ad23cb32e08_900x936.png)
*来源：SemiAnalysis、Claude Code*

然后是输出：

![](https://substack-post-media.s3.amazonaws.com/public/images/29cab5bf-fe5d-46e0-b93b-9caaf5a7d1ea_1043x585.png)
*来源：SemiAnalysis、Claude Code*

程序员将不再亲自写代码，而是要求（智能体）代为完成任务。而 Claude Code 的魔力在于——*它就是能用*。许多知名程序员终于向 vibe coding 的新浪潮低头，并意识到编程实际上已接近一个「被解决的问题」，由智能体来支撑比由人类来做更好。

竞争的焦点正在转移。对「哪个模型最棒」的线性基准测试的执念将显得老派，好比拿拨号上网的速度与 DSL 相比。速度和性能固然重要，模型也是驱动智能体的引擎，但性能将以「生成一个网站的净数据包产出」来衡量，而不是数据包本身的质量。明天的「网站级功能」将通过工具、记忆、子智能体和验证回路的编排来创造成果，而非仅仅给出响应。所有信息工作终于都能被模型覆盖。

Opus 4.5 是让这一切成为可能的引擎，而线性基准测试中重要的东西，对长时程智能体任务而言可能根本无关紧要。后文再详述。

## **超越编程：滩头阵地，而非终点**

编程曾是最有价值的工作，在 2020 年代的软件工程时代程序员炙手可热。如今，就智能体化信息处理带来的颠覆而言，编程只是一块滩头阵地，而规模达 15 万亿美元的信息工作经济体正面临风险。全球有超过 10 亿信息工作者，据国际劳工组织（ILO），约占 36 亿全球劳动力的 1/3。

信息工作类别中的每一个工作流往往都相似，共享着 Claude Code 已在软件上证明可行的那套流程：READ（摄取非结构化信息）、THINK（运用领域知识）、WRITE（产出结构化输出）、VERIFY（对照标准核查）。这覆盖了大多数信息工作者（包括研究工作！）的绝大部分日常。如果智能体能吃掉软件，还有哪个劳动力池是它们碰不得的？

我们的看法是：碰不得的寥寥无几。而随着 Claude Code（以及 Cowork）的崛起，智能体的总可服务市场（TAM）远大于 LLM 本身。客户支持和软件开发这样的细分市场将开始进军更庞大的金融服务、法律、咨询及其他行业。这正是 [SemiAnalysis Tokenomics 模型](https://semianalysis.com/tokenomics-model/)的核心关注点。

![](https://substack-post-media.s3.amazonaws.com/public/images/322aa44f-6be7-4182-9a2a-d8845c6a81c5_1430x818.png)
*来源：McKinsey、Mordor Intelligence、Grand View Research、Precedence Research。由 Claude Code 生成。*

鉴于编程这个「杀手级用例」，以及 Claude Code / Cowork 明确的可泛化性，这足以支撑一套完全不同的测算逻辑。将大多数「请求—响应」和信息检索自动化很可能是可行的，这打开了绝对金额的天花板。[Tokenomics 模型的目标](https://semianalysis.com/tokenomics-model/)就是随着智能体 AI 扩展到商业的方方面面，持续追踪新的杀手级用例和 TAM。

### **普及的约束：任务时程**

真正让这张大饼中更大部分可被颠覆的，是更长的任务时程。一个智能体在搞砸任务之前能连续工作多久？METR 数据显示，自主任务时程每 4-7 个月翻一番（2024-2025 年加速到约 4 个月）。

![](https://substack-post-media.s3.amazonaws.com/public/images/a27e004c-72b7-4058-a24e-f1c6c6c9266f_1430x880.png)
*来源：METR、SemiAnalysis Tokenomics 团队*

每一次翻倍都解锁整块蛋糕的更多部分。在 30 分钟水平，你可以自动补全代码片段；在 4.8 小时水平，你可以重构一个模块。到了以天计的任务，你可以把一整项审计自动化。而 Anthropic 显然也看到了这一点。

2026 年 1 月 12 日，Anthropic 发布了 Cowork——「通用计算版 Claude Code」。四名工程师用 10 天打造了它。大部分代码由 Claude Code 自己编写。相同的架构：Claude Agent SDK、MCP、子智能体。它能从收据创建电子表格、按内容整理文件、从散乱的笔记起草报告。它就是 Claude Code 减去终端、加上桌面。

![](https://substack-post-media.s3.amazonaws.com/public/images/f50e715d-28e1-4397-9514-ece12ddd3632_1049x664.png)
![](https://substack-post-media.s3.amazonaws.com/public/images/4d386d33-e530-49fd-9619-a8d72cbbc10d_1049x655.png)

这是对未来的一瞥。一个理解你日常工作情境、能按需构建并生成信息处理的框架（harness）。你不再需要从数据库下载的报告里自己制作图表，智能体会替你生成一份格式比你自己用 Excel 做得还好的报告。每当你需要收集信息——比如销售配额——你的智能体会从 UI 或 API 中提取信息并代你生成报告。信息工作本身将像 Claude Code 自动化软件工程一样被自动化。

![](https://substack-post-media.s3.amazonaws.com/public/images/6321004f-cff8-45ec-abcd-dddbc20b1d6f_936x474.png)
*来源：SemiAnalysis——由 Claude Code 根据我们的共封装光学（CPO）文章生成。*

尽管它今天还不完美，但它显然已经能比大多数人类更快地处理、综合和格式化数据。在某些情况下，这还伴随着更高的保真度和更低的成本。幻觉固然会有，但大多数现有系统本身就充斥着人类导致的错误。如果信息能以可用的保真度处理完毕并传递给下一步，这本身就会大幅增加工作的供给。我们真真切切地处在一个时点：任何人都可以向这类智能体工作流输入一句话，跑一个多变量回归——这在 2000 年代需要一生的训练才能做到。

[Stack Overflow 2025 开发者调查](https://survey.stackoverflow.co/2025)显示 84% 的程序员在使用 AI，而这已是普及的最前沿。只有 31% 在使用编程智能体，这意味着对更广义的信息工作浪潮而言，这条渗透曲线还处于早期。正如编程智能体渗透「一眨眼」般到来，更广义的信息工作也将很快看到 AI 的普及。

## **智能的价格正在崩塌**

软件工程过去是、将来也永远是信息工作的黄金标准。但随着质量终于跨过关键阈值，程序员与其工具的关系已经翻转。程序员实际上只是在驾驭一个黑盒工具来达成结果，而这之所以成为可能，不仅因为质量，还因为 token 所承载智能的价格出现了惊人幅度的下跌。一个配备 Claude Code 的开发者如今能完成过去一个团队一个月的工作。

Claude Pro 或 ChatGPT 的价格为每月 20 美元，而 Max 订阅分别为每月 200 美元。美国知识工作者的全成本中位数约为每天 350-500 美元。一个每天只需约 6-7 美元、就能处理其一部分工作流的智能体，带来的是 10-30 倍的 ROI，这还没算智能水平本身的提升。

**企业界已经开始行动**

智能成本的大规模通缩将重新定价每一家信息公司可重复工作的利润率。[埃森哲（Accenture）刚刚签署协议，为 30,000 名专业人员提供 Claude 培训](https://newsroom.accenture.com/news/2025/accenture-and-anthropic-launch-multi-year-partnership-to-drive-enterprise-ai-innovation-and-value-across-industries)——这是迄今为止最大规模的 Claude Code 部署。埃森哲将聚焦金融服务、生命科学、医疗保健和公共部门。这些都是信息自动化的巨大未开发市场。[OpenAI 刚刚发布了 Frontier](https://openai.com/index/introducing-openai-frontier/)，聚焦企业级普及。

企业软件显然是智能成本大降的第一个牺牲品。SaaS 本身就是把工作流的信息处理固化成代码。SaaS 的三重护城河——数据切换成本（数据被锁死）、工作流锁定（学习 UI）、集成复杂性（Slack 如何与 Jira 协作）——都已在边际上被部分侵蚀。SaaS 75% 的毛利率看起来像一个巨大的机会：智能体以更低的迁移成本在系统之间搬运数据，智能体本身不依赖面向人类的工作流，而 MCP 集成让集成变得容易得多。SaaS 的每个环节都在变便宜，其利润率已成为 AI 的第一个猎物。

一个简单的例子：智能体现在可以直接代你查询 Postgres 数据库、生成图表并发邮件给利益相关方。这原本差不多就是 CRM 那类 SaaS 工作流的成本，而且不需要就 UI 变更培训人员或更新软件。它「就是能用」。BI/分析（智能体查询数据库）、数据录入、ITSM（L1/L2 工单分诊）和后台对账已经在自动化进程之中！这些已经在敲响软件界最神圣护城河的大门。

在我们看来，任何由人类点击按钮、收集信息、再把信息重新格式化成另一种媒介（邮件、图表、Excel、演示文稿）的工作都面临巨大风险。LLM 恰恰最擅长这类数据互换：毫不费力地把文本变成音频、英语变成中文、文字变成图像。而我们认为，这对全世界最大的公司之一——微软（Microsoft）——构成巨大威胁。

## **竞争格局（微软的难题）**

成本崩塌正在摧毁按席位收费的软件模式。而随着 Claude Code 在 SemiAnalysis 内部的大规模采用，我们看到的最大份额转移莫过于微软按席位的 Office 365。「人类可点击的按钮」的定义就是微软，推而广之就是所有按席位收费的软件。需要警惕的模式是：一套适用于多行业工作流、为人类设计的软件。

如果智能体会代你查询销售线索数据，公司为什么还需要标准化的 Salesforce？Salesforce 本质上是一个表单和工作流的包装，而表单和工作流很可能由 AI 搭建成数据库、再按需查询。每一分 UX 或偏好都面临风险。Tableau 作为一个概念已经过时；Figma（面向人类的线框图）面临风险。人类与计算机交互的核心方式即将改变，而微软正坐在旧范式的中心。

## **夹在两门生意之间**

我们最近（错误地）预测微软营收将加速，主要基于其庞大的对外租赁 GPU 机队和向外部代工产能的转移。但我们认为，在最近的财报电话会上，他们决定战略性收手。原话如下：

> 过去一段时间你在我们和我们的产品上看到的加速，很大程度上来自我们正把 GPU 和产能分配给过去几年招揽的众多有才华的 AI 人才。这样做的结果是，剩下的部分才用来服务需求持续增长的 Azure 产能。有一种理解方式——因为我有时会被问到这个问题——如果我把第一、第二季度刚上线的这些 GPU 全部分配给 Azure，那个 KPI 本来会超过 40。

重要的上下文是这一段：

> 我们真正做的是长期决策。**我们做的第一件事，是满足销售端使用量的增长，以及 M365 Copilot、GitHub Copilot（原文作 GitHub pilot）等第一方应用加速普及的需要**。然后我们确保对**研发和产品创新的长期属性**进行投资。

微软内部有两头巨兽：为公开市场投资者服务的 Azure 增长，以及为保住 Office 365 产品套件而投资 Copilot。要果断赢下其中一头，很可能必须输掉另一头。而眼下，微软是全球最大的 AI 云之一，服务着 OpenAI 和 Anthropic 这样的公司。但他们是在把 GPU 租给蛮族——而这些蛮族将摧毁他们在生产力软件领域的城堡。

Claude for Excel 实际上就是 Copilot for Excel 本该成为的样子，**但它是由外部公司在他们自己的第一方产品上发布的**。今天大多数现金仍来自 Office，但大部分终值来自 Azure 营收增长。要加速 Azure，就等于放城门外的蛮族更快地拆掉城墙。微软当年与这些新贵做成了生意，但随着 OpenAI 和 Anthropic 成长为更大的平台，这条护城河是否还能把他们挡在外面，已经很不确定。

讽刺的是，微软的 AI 支出*必须*增加，否则 O365 产品套件的终值将会暴跌。他们确实握有分发渠道，但那主要建立在一个定位与 AI 新贵相比日益被侵蚀的产品之上。与此同时，微软在 AI 领域的核心伙伴 OpenAI 自身也正遭受 Claude Code 带来的企业级颠覆。OpenAI 必须迅速回应 Claude Code 在智能体普及上的崛起，否则他们自己看起来会像一家基础设施公司（卖 token）而非解决方案（智能体）公司。颠覆的风险正在急剧攀升，而发生这一切的，是有史以来最赚钱的公司之一。

GitHub Copilot 和 Office Copilot 领先了一年时间，作为产品却几乎没有取得任何进展。与此同时，Satya 实际上亲自下场出任[微软 AI 的产品经理](https://www.businessinsider.com/microsoft-ceo-satya-nadella-ai-revolution-2025-12?utm_source=reddit&utm_medium=social&utm_campaign=insider-artificial-sub-post)，远离他作为 CEO 的日常职责。相当清楚的是：这一个产品的赌注，可能就是整个公司。

## **Anthropic 的融资与狂飙：Anthropic 为什么在赢？**
