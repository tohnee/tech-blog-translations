---
title: "韩国万亿美元主权 AI 投资：Nvidia 赢，Hynix 输"
title_en: "Korea's Trillion-Dollar Sovereign AI Investment: Nvidia Wins, Hynix Loses"
subtitle: "韩国上演一场「鱿鱼游戏」全国 AI 锦标赛，最优秀的非中国开源模型惨遭淘汰，为什么 Nvidia 需要开源，以及对 Hynix 和三星的影响"
date: 2026-09-01
source: https://newsletter.semianalysis.com/p/koreas-trillion-dollar-sovereign
crawled: 2026-09-15
authors: ["Max Kan", "Ray Wang", "Myron Xie", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 韩国万亿美元主权 AI 投资：Nvidia 赢，Hynix 输

> 原文：[Korea's Trillion-Dollar Sovereign AI Investment: Nvidia Wins, Hynix Loses](https://newsletter.semianalysis.com/p/koreas-trillion-dollar-sovereign) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**韩国上演一场「鱿鱼游戏」全国 AI 锦标赛，最优秀的非中国开源模型惨遭淘汰，为什么 Nvidia 需要开源，以及对 Hynix 和三星的影响**

世界各地的企业和政府每天都在越来越依赖美国的前沿模型。初创公司 CEO 已经无法想象没有 AI 怎么经营公司，用不了多久，世界上其他所有组织也会如此。

与此同时，一个事实已经再清楚不过：前沿模型的访问权限捏在 Anthropic、OpenAI 和美国政府手里。Fable 5 曾被美国政府（USG）临时封禁，GPT 5.6 和 Astra 也同样被推迟过。这两款模型都带有网络、生物等安全护栏——出发点虽好，却常常让好用户无法完成无害的任务。考虑到近期的[安全事件](https://openai.com/index/hugging-face-model-evaluation-security-incident/)以及公众对日益强大的 AI 的普遍担忧，前沿模型的使用今后极有可能只会越来越受限。事实上，我们认为**OpenAI/Anthropic 最终完全停止以 API 形式提供其最强模型**是可能出现的结果。

开源似乎是对付这些依赖焦虑的显易答案，但它远不是银弹。首先，各种「开源」许可证正变得越来越苛刻。仅举一例：任何年收入超过 $20M 的「模型即服务」企业，都必须与 Moonshot 单独谈判协议才能服务 Kimi K3。其次，某家实验室今天开源了模型，并不能保证它将来会继续开源。设想 2028 年，因为没有任何相关模型开源、而一切又必须出于安全考虑留在本地部署，你只能用 2027 年水平的智能去支撑某个极高价值的应用场景。这有点像你的 Fable 请求被降级成 Opus——只是糟糕 100 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/f29f41fc-660c-4609-a423-a38f3ccf2f11_884x862.png)
*开源模型 token 量过去一个月显著增长。来源：OpenRouter*

彻底解决这些担忧的唯一办法，是预训练一个运行在自己 GPU 上的模型。到目前为止，这基本上还是企业层面的问题：潜在收益是否配得上所需的巨额投入？**然而很快，同一道算术题将摆在每个主要国家面前。**

今天，我们将深入解析韩国的主权 AI 布局。韩国不仅是 AI 供应链中两家最重要公司的所在地，还有着技术自主的悠久传统（任何被迫用过 Naver 地图的外国人都懂），并且目前是主权 AI 领域当之无愧的领跑者。

随后我们将讨论对投资者的两大影响：为什么 Nvidia 是主权 AI 最大的支持者，以及为什么韩国的雄心与三星和 Hynix 股东的利益未必一致。

## 韩国版「鱿鱼游戏」——全国 AI 锦标赛：尝试打造国产前沿模型

2025 年 6 月，韩国政府宣布了「독자 AI 파운데이션 모델」（独立 AI 基础模型）项目。顾名思义，目标是开发一个韩国组织无需依赖外国 AI 实验室就能自行训练、修改和运营的模型。

这个项目最有意思的地方在于其结构。政府没有预先选定唯一的国家级冠军，而是举办了一场锦标赛。所有参赛者都能获得 AI 三大支柱——算力、数据和研究人员——的补贴，并每 6 个月接受一次评估。每个阶段，输家被淘汰，其资源被重新分配给赢家。

竞赛以 [15 个联合体](https://eiec.kdi.re.kr/policy/materialView.do?num=269498)开局。十个通过了初审，2025 年 8 月选出五强：Naver Cloud、LG AI Research、SK Telecom、NC AI 和 Upstage。大多数读者可能完全没听说过这些公司的 AI 业务，但其中一些出乎意料地有实力。例如 SKT、LG 和 Naver 在 ChatGPT 问世之前就都预训练过 LLM。

各队获得的补贴不尽相同。第一轮中，政府从 SKT 和 Naver 租借了约 3,000 颗 H100 等效算力，分发给另外 3 支参赛队。政府还在数据上花了约 $45M（美元）。其中大部分付给了韩国公司，购买图书、新闻文章、视频广播等内容——这些内容连同部分韩国政府档案在所有参赛队之间共享。此外，政府还给了每家公司约 $2M 让其自行采购数据。最后是研究人员：政府向每家公司提供约 $1.4M 用于尝试招募海外人才，但只有 Upstage 接受了这一提议。

随着锦标赛推进，存活下来的队伍将获得更多资源，但[约 $350M](https://www.news1.kr/it-science/general-it/5868735) 的政府总预算与美国实验室相比仍只是零头。不过，正如我们后文将解释的，这只是韩国计划中 AI 投资的一小部分。此外，他们目前的结果表明，从零训练一个不错的模型，可能比大多数人想象的更便宜。

原计划是从 5 队减到 4 队、3 队，最终 2 队，每轮约 6 个月。两支获胜队伍将于 2026 年底选出，政府在 2027 年全年为其提供额外资源以放大模型规模。

然而，第一轮结尾却上演了一场意料之外的戏剧性事件！

5 支队伍的评分构成为：基准测试占 40%、专家评审占 35%、用户测试占 25%。NC 垫底，这意味着其余 4 队本应全部晋级，但政府决定把 Naver 也取消资格。原因是他们使用了阿里巴巴 Qwen 模型家族的视觉与音频编码器。

替 Naver 说句公道话：这些编码器是独立的神经网络，其输出再馈入主 LLM；而且韩国政府起初并未说清参赛者可以使用开源中的哪些东西。直到提交之后，政府才裁定外国架构是允许的，但即便是辅助组件，也必须在初始化权重之后再训练和开发。

Naver 坚称他们已经开发了自己的编码器，随时可以替换掉 Qwen 的部分，但政府不出所料地强硬，拒绝恢复其资格。

少了 1 支队伍后，韩国政府决定举办一场补充赛选出新的第 4 名参赛者，最终选中了 Motif Technologies——一家新兴实验室（neolab），于 2025 年 2 月从韩国 AI 基础设施软件公司 Moreh 分拆出来。

4 家公司都在 7 月开源了各自最新的模型，最近一轮的结果于 8 月 18 日公布。但在剧透结果之前，先来看看这些模型。

### 那么，他们的模型到底有多好？

下面是 4 个模型的概览：

![](https://substack-post-media.s3.amazonaws.com/public/images/e4e691bf-4cfa-41e1-8111-ac8af06b0257_2034x900.png)
*来源：SemiAnalysis*

再看它们在基准测试上的对比：

![](https://substack-post-media.s3.amazonaws.com/public/images/c052c93e-d099-4681-941c-676ce171c02c_1480x1178.png)
*来源：SemiAnalysis Tokenomics 模型*

可以看到，两家初创公司（Motif 和 Upstage）显著跑赢了背靠真正财阀的团队。它们的模型参数量还不到对方一半，这一点更令人印象深刻。

在 Artificial Analysis 的智能指数（Intelligence Index）上，Motif 3 领先 Upstage 10 分，是迄今最好的韩国模型。更值得注意的是，它还明显领先于 Inkling 和 Nemotron 3 Ultra——当今最好的两个美国开源模型。

![](https://substack-post-media.s3.amazonaws.com/public/images/18f0619b-8a76-4656-bb09-b069674d5064_2032x1133.png)
*来源：Artificial Analysis、SemiAnalysis*

Motif 是一家[不到 30 人](https://www.linkedin.com/feed/update/urn:li:activity:7485122160470978561/)的初创公司，去年 6 月发布了他们的第一个预训练模型，总参数量仅 [2.6B](https://huggingface.co/Motif-Technologies/Motif-2.6B)。他们只融资了 $17M，可用的算力也只有区区 768 颗 B200（< 2MW）。

相比之下，Thinking Machines 是当下最炙手可热的新兴实验室，种子轮就以 $12B 投后估值融了 $2B，还与 Nvidia 签下了 1GW+ 的算力协议并伴随额外融资。至于 Nvidia 本身，它手中的资源就更不用提了。

![](https://substack-post-media.s3.amazonaws.com/public/images/eacee1dc-1958-4654-993c-0aad4468e95b_1926x721.png)
*来源：SemiAnalysis*

换句话说，**一家你八成没听说过的韩国小初创，用紧巴巴的预算从零训练出了全世界最好的非中国开源模型**。

这里不是要贬低 Thinking Machines 或 Nvidia。训练开源模型都不是他们的核心业务。我们想强调的是：从零训练一个接近 SOTA 的开源模型，所需资源很可能比多数人以为的少。专注没有替代品——训练 Motif 3 的总算力成本（含实验）按今天的价格算[只有约 $15M（美元）](https://www.linkedin.com/feed/update/urn:li:activity:7485122160470978561/)。对每个主要国家来说，这显然都在预算之内。

### 韩国政府值得商榷的判断

我们[此前](https://newsletter.semianalysis.com/p/are-open-models-catching-up)已[多次](https://newsletter.semianalysis.com/p/the-coding-assistant-breakdown-more)深入撰文讨论基准测试的种种问题，但它们的方向性通常还是对的。**在 Artificial Analysis 智能指数这类指标上拉开 10 分以上的差距，几乎总是对应着模型能力的台阶式跃升**（例如 GPT 4o 到 o1，或 Opus 4.8 到 Fable 5）。

有鉴于此，当我们看到**最新一轮被淘汰的偏偏是 Motif**时，非常震惊。或许你可以说这个模型「刷分」（benchmaxxed）、不配第一，但垫底实在令人费解。

提醒一下，参赛者的评分有三项：基准测试 40%、专家评审 35%、用户测试 25%。Motif 虽然在基准测试上得分最高，但在另外两项上都排名垫底。

![](https://substack-post-media.s3.amazonaws.com/public/images/c19edd74-5f21-4858-a836-7b904b3fec87_2321x969.png)
*来源：SemiAnalysis*

后两项的具体评估方法不透明得让人抓狂。用户测试方面，我们完全不知道用户实际拿模型做了什么任务、依据什么标准打分。而且所有测试都不是盲测，用户很可能对名气更大的公司带有偏见。

专家评审部分更可疑。简单说，10 位外部专家就「发展战略」「未来规划」「生态影响」之类的东西给四个模型打分。这些词究竟指什么，你我恐怕只能靠猜；但有一点很清楚：某些类别天然偏向 LG 和 SKT 这样的大公司。我们还听说，专家评审担心 Motif 的技术会经由外国投资者流出海外。这相当令人费解，因为比赛的要求之一就是所有技术组件必须开源。

我们认为，Motif 被淘汰后将不再获得任何政府支持，实在令人惋惜。主权 AI 计划的全部意义就在于集结本国 AI 人才打造高质量模型。Motif 证明了自己恰恰有这个能力，政府应当运用自身影响力和资源帮他们补上「未来规划」和「生态影响」这类短板——而不是因此惩罚他们。

现在，**Motif 可能为了获得继续研究所需的资金和算力而被迫迁出韩国**。对于国家 AI 锦标赛上杀出的黑马而言，这大概是所有结局中最讽刺的一种。希望其他国家在推进自己的主权 AI 计划时能做得更好。

## 一万亿美元的数据中心

话虽如此，韩国最终的 AI 冠军将获得极为充裕的资源。7 月，他们[宣布](https://www.datacenterdynamics.com/en/news/south-korea-announces-919bn-investment-into-three-mega-projects-plans-to-build-184gw-worth-of-data-centers-by-2035/)了一笔高达 $919B 的巨额投资，到 2029 年建成 8.4GW、2035 年建成 18.4GW。第一阶段，SK 集团、GS 集团和 Naver 将分别建设 5GW、2.4GW 和 1GW。第二阶段的其余 10GW 由 SK 集团另行负责。

我们已经确认了第一阶段的 3 个在建站点，合计 4.4GW。包括确切位置、MW 爬坡节奏和电源在内的完整细节，请参阅我们的[数据中心模型](https://semianalysis.com/datacenter-industry-model/)。

![](https://substack-post-media.s3.amazonaws.com/public/images/fb2ebd34-0ee3-486d-b00b-51b4d875c150_1120x840.png)
*Naver 位于韩国世宗的 1GW 站点。来源：SemiAnalysis 数据中心模型*

尽管这些时间表很激进，但我们认为可以实现。监管环境有利，李在明总统更是明确把 AI 基础设施定位为类似韩国 1990 年代宽带建设的「留名青史」工程。整个 2000 和 2010 年代，韩国的互联网独树一帜地又便宜又快，正是这一点孕育了本国的搜索、电商和电竞产业。

需要说明的是，这些产能并非全部用于支撑韩国的主权 AI 计划，其中很大一部分很可能卖给 Anthropic 或 OpenAI。但重要的是，韩国由此获得了在必要时大幅扩张主权 AI 的选择权，而且这种本土算力爬坡，未来很可能被美中之外的更多国家效仿。

## 为什么 Nvidia 需要开源和主权 AI

Jensen（黄仁勋）最近在 Twitter 上[首次发声](https://x.com/JensenHuang/status/2080643682408321103?s=20)，发表了一篇关于开源 AI 重要性的宣言。随后除 Anthropic 外，几乎所有重要 AI 公司都联署了这份宣言。摘录如下：

> 「我们的 AI 领导地位将不由某一个前沿模型来评判，而取决于美国能否建立一个渗入每个行业的强大、开放的生态系统。这对在全国各地创造创新与繁荣的机会至关重要。它要求扩大 AI 的可及性、鼓励竞争、培育强健的应用层，并让美国人对自己所依赖的技术拥有更大的掌控权。开放权重模型——任何人都可以下载、检视、修改并在自己的基础设施上运行的 AI 模型——是这一基础的重要组成部分，因为它们让先进的 AI 更可及、更可适配、也更普及。」

围绕开源 AI 的许多论述总爱高谈智能民主化与技术权力去中心化。然而掀开引擎盖看，往往不过是各人为自家持仓代言。

没有谁比 Nvidia 更需要开源 AI。正如我们此前向 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)订阅者解释的，以 API 价格出售前沿 token 是增量算力中 ROI 最高的用例。因此，Anthropic 加 OpenAI 未来将拿下净新增 GW 中越来越大的份额，而 Nvidia 目前正走向一个只有 2 个真客户的世界。把超大规模云厂商算上，这个数字也许能到 7，但对全球市值第一的公司来说，这显然无法接受。更何况这 7 个客户中除了 SpaceX 之外，全都在积极自研 XPU，蚕食 Nvidia 的利润率。

科技界最著名的竞争策略之一是「[把你的互补品商品化](https://www.joelonsoftware.com/2002/06/12/strategy-letter-v/)」。核心思想是：当某样东西变得更便宜、更充足时，与它配套的一切东西的需求都会上升。这解释了公司为什么常常「免费」「赠送」东西。经典案例包括：1) Google 免费提供 Chrome 并开源 Android，扩大了网民入口，让搜索广告更值钱；2) 微软保留向 IBM 的竞争对手授权 MS-DOS 的权利，助推 PC 成为商品化的硬件平台。

对 Nvidia 而言，AI 模型与应用是其 GPU 的互补品。**其业务的长期健康，取决于一个不只有 Anthropic 和 OpenAI 的、充满活力且多元的 AI 生态系统。**

他们最近与全球最大的一批资本配置者宣布的 [$500B 谅解备忘录（MOU）](https://nvidianews.nvidia.com/news/nvidia-partners-with-apollo-blackrock-blackstone-brookfield-goldman-sachs-and-kkr-to-establish-ai-compute-infrastructure-financing-platforms-to-mobilize-over-500-billion-of-third-party-capital)，只是 Nvidia 为实现这一愿景所能施展的巧妙金融工程的一例。通过把「Nvidia AI 工厂算力」变成一种「可投资资产类别」，世界各地的 SSI 和 Thinking Machines 们就有办法撬动养老金、保险公司和私人信贷机构的资本，去购买海量算力。

![](https://substack-post-media.s3.amazonaws.com/public/images/227673ba-d611-4c22-8ff0-db2f95333de3_2048x1210.png)
*来源：SemiAnalysis*

主权 AI 是 Nvidia 分散客户群的另一个巨大机会。SK 集团已[承诺](https://nvidianews.nvidia.com/news/sk-group-and-nvidia-expand-strategic-partnership-across-ai-factories-and-next-generation-memory)在其 5GW 建设中采用 2 GW 的 Rubin，Naver 也[签署](https://nvidianews.nvidia.com/news/naver-nvidia-and-brookfield-to-expand-koreas-national-ai-factory-infrastructure-buildout)了另外 200MW。**我们预计 Jensen 还会继续宣布与其他国家的类似交易。**

## 数据中心豪赌与内存

从主权 AI 的视角看，韩国对政府和企业自建数据中心与 GPU 集群的投资完全说得通。主权模型归根结底需要主权基础设施：在本国掌控之下决定模型在哪里训练、如何部署、谁能访问底层算力。

韩国的挑战在于，它仍然缺少一家上规模的国产先进制程加速器供应商。Rebellions 和 FuriosaAI 有一些进展，但客观上在部署规模、软件成熟度和商业化可用性上仍落后于 Nvidia 和 AMD。而 Google TPU、AWS Trainium 这类超大规模云厂商自研的替代品，同样不在韩国自己手里。

数据中心建设归根结底取决于两样东西：资本和算力。在我们看来，资本是较容易的问题。韩国政府过去几年一直把 AI 投资列为优先事项，Naver、SK Telecom、三星（Samsung）、SK Hynix 等本土头部科技公司也在向数据中心、AI 基础设施和模型开发投入大量资源。而算力则是另一回事。韩国可以为土地、电力、散热和楼宇出资，但它无法像世界上大多数国家一样，仅靠砸钱就造出一个有全球竞争力的加速器生态系统，也无法保证获得最新平台的供应。

如果韩国的目标只是建立本土 AI 生态，那么与 Nvidia 保持常规的供应商关系也许就足够了。但如果它想成为全球领先的主权 AI 玩家，就需要更深的东西：更高的路线图透明度、紧密的技术整合、对新一代算力平台的可靠获取，以及对培育周边本土生态的支持。

这正是 Nvidia 与三星和 SK Hynix 扩展关系在此刻的意义所在。据报道，三星计划建造一座[使用](https://investor.nvidia.com/news/press-release-details/2025/NVIDIA-and-Samsung-Build-AI-Factory-to-Transform-Global-Intelligent-Manufacturing/default.aspx)超过 50,000 颗 GPU 的 Nvidia AI 工厂，而 SK Telecom 宣布的 2GW DSX AI 工厂预计将部署由 SK Hynix HBM4 驱动的 Vera Rubin 系统。尽管公开公告并未披露优惠 GPU 配给或保底数量，但更深层的战略协同应能增强韩国规划和部署先进算力的能力——这可比单纯盖起容纳这些算力的数据中心难得多。

在此背景下，我们认为 Nvidia 的盘算不止于多拿下一个大型主权算力客户。正如我们此前向[内存模型](https://semianalysis.com/memory-model/)订阅者[解释](https://semianalysis.com/institutional/samsung-better-hbm-pricing-than-sk-hynix-in-2027-nvidias-2027-hbm-pricing-outlook-server-oem-memory-crunch-sk-hynix-samsung-earnings-reconciliation/)过的，我们认为韩国的基础设施建设潮也为 Nvidia 提供了深化与 SK Hynix 关系的机会——后者是其最重要的内存供应商之一，也是 SK 集团体系内的关键成员。我们相信 Nvidia 很可能已经锁定了 SOCAMM 的长期协议，以及优惠的 HBM 定价和 2027 年的大额采购承诺，尽管最终谈判结果可能与我们目前的估计有出入。

### 跨越 AI 基础设施栈、超越内存的扩张，是有代价的
