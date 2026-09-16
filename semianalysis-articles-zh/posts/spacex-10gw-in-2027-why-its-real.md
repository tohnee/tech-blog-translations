---
title: "SpaceX 2027 年 10GW——为什么是真的、将为 SpaceX 带来 $300B ARR，以及为什么微软会成为最大承购方"
title_en: "SpaceX 10GW in 2027 – Why It’s Real, Will Drive $300B ARR for SpaceX, and Why Microsoft Will Be the Largest Offtaker"
subtitle: "每吉瓦每年 $100B 的推理收入、SpaceX 的星际速度、微软 2026 年的 10GW 觉醒、Azure 可实现三位数增长"
date: 2026-08-07
source: https://newsletter.semianalysis.com/p/spacex-10gw-in-2027-why-its-real
crawled: 2026-09-15
authors: ["Jeremie Eliahou Ontiveros", "Reyk Knuhtsen", "Jordan Nanos", "Max Kan", "Dylan Patel", "Muhammad Zuhair"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# SpaceX 2027 年 10GW——为什么是真的、将为 SpaceX 带来 $300B ARR，以及为什么微软会成为最大承购方

> 原文：[SpaceX 10GW in 2027 – Why It’s Real, Will Drive $300B ARR for SpaceX, and Why Microsoft Will Be the Largest Offtaker](https://newsletter.semianalysis.com/p/spacex-10gw-in-2027-why-its-real) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**每吉瓦每年 $100B 的推理收入、SpaceX 的星际速度、微软 2026 年的 10GW 觉醒、Azure 可实现三位数增长**

Elon Musk 在 SpaceX 首次财报电话会上宣布明年的吉瓦级野心，再次震惊了世界。他「保守」地设定仅 2027 年一年就新建并交付 6-8GW 的增量，而且这个数字有可能远超 +10GW。按每 GW $50B 计算，这意味着 2027 年 $300-500B 的资本开支（capex），与我们预期的 AWS 和 Google 相当——对一家盈利能力显著逊于对手超大规模云厂商的公司来说，这是一个令人难以置信的数字。

然而，我们相信这个数字是真的。我们看到 SpaceX 有望在 2027 年底前建成约 10GW。我们评估了所有适合 SpaceX 的场址，并已将清单提供给我们的[数据中心模型](https://semianalysis.com/datacenter-industry-model/)订阅客户。我们的[能源模型](https://semianalysis.com/energy-model/)订阅客户还握有按季度更新的燃气发电设备精确供应清单，覆盖 30 多家燃气轮机、发动机、燃料电池供应商。其中很多数据，我们在市场醒悟之前就已经提供。下文将讨论 Elon 如何绕过典型的数据中心建设约束。

正如我们在 Meta Compute 深度解析中所解释的，「大规模 + 近期可用」的算力组合极其稀缺，其定价溢价巨大——高达 $50B/GW/年。不过，AI 实验室承受得起，并且能借此过上好日子。

我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)和[推理模拟器](https://semianalysis.com/consulting/)证明：在现实的性能水平（如每 GPU tokens/sec）下，**OpenAI 和 Anthropic 在 GB300 集群上销售 API 推理时，每 GW 每年可以产生超过 $100B 的收入**。这远超按当前新兴 GPU 云（neocloud）价格租用 GB300 集群一年的成本。

对前沿模型公司而言，提供推理 token 服务利润丰厚得令人难以置信。

![](https://substack-post-media.s3.amazonaws.com/public/images/a4e1a2ba-c403-46a0-a0e6-a1724ad8cb17_2430x1296.png)
*来源：SemiAnalysis Tokenomics Model、SemiAnalysis Inference Simulator*

我们采用保守的租金定价 $3/GPU-小时，假设成本约为 $12B/GW/年，并使用我们的[推理模拟器](http://semianalysis.com/consulting)、配合前沿级模型架构和我们的智能体编程基准 [AgentX（InferenceX 的一部分）](https://inferencemax.ai/)——该基准通过收集真实生产编程轨迹构建——来估算 token 产量。我们按真实工作负载比例，把 token 产量与输入、缓存读、缓存写和输出 token 的价格混合，得出最终估算：超过 $100B/GW/年。

作为背景介绍：我们的[推理模拟器](https://semianalysis.com/consulting)建立在对现代 AI 加速器工作原理的根本性理解之上，从零构建。我们为前沿模型的推理过程建立了 roofline 与真实性能模型，每个算子都有计时，并输出真实 trace。它是对真实工作负载在真实芯片上执行的端到端仿真。我们已在种类广泛的加速器与工作负载上验证了模拟器的保真度，并持续改进它基于设计规格精确预测未来加速器性能的能力。

![](https://substack-post-media.s3.amazonaws.com/public/images/5e508607-fc09-402e-b1b1-2a3d4a4ca88e_1200x598.jpeg)
*覆盖芯片上端到端仿真工作负载执行的细粒度数据会产出真实的 profiler trace，可用 Perfetto 等标准工具分析。来源：SemiAnalysis Inference Simulator*
![](https://substack-post-media.s3.amazonaws.com/public/images/da1d160f-cc47-49a9-8cf9-002d41972d22_1151x675.jpeg)
*针对常见推理工作负载与硬件平台，沿帕累托前沿生成高层级预测。来源：SemiAnalysis Inference Simulator*

如需了解更多关于我们如何将推理模拟器用于定制研究与分析的信息，请联系 [sales@semianalysis.com](mailto:sales@semianalysis.com)。

除了 OpenAI 和 Anthropic，世界上其实还有第三家有能力按 GW「印出」这种经济性的公司：**微软**。凭借**对 OpenAI 模型的完整访问权**，他们可以产生完全相同的每 MW 收入和利润率，却不用支付任何训练成本。**Satya 在与 OpenAI 的谈判中拿捏得恰到好处：2026 年 4 月重签的协议把原来的 20% 收入分成从等式中去掉了。** 简单说，微软有巨大的动力尽可能多、尽可能快地采购 MW。虽然其数据中心产能目前大部分以约 $14M/MW/年的价格供给了 OpenAI，但他们有机会改善这一结构。潜在影响是：Microsoft Azure 的营收增速从约 42% 加速到明年超过 100%。这是一个一代人一遇的机会，而 SpaceX 的位置好得不可思议。

![](https://substack-post-media.s3.amazonaws.com/public/images/2c326c26-195e-461f-b2cc-18e88b7fe29d_2700x1440.png)
*来源：SemiAnalysis Tokenomics Model*

微软以 $50B/GW/年的价格与 SpaceX 签下 3GW 听起来很疯狂，但我们认为这是可能的，原因有二：

- 1/ 微软已经在为一场史诗级的数据中心爬坡做准备。如下文所述，他们年初至今已签署 10GW 合同，总合同价值超过 $300B（不含 GPU 成本）。我们预计还会签署更多。需要注意的是：这些合同贡献的是 2027 年底和 2028 年的产能。近期仍有一个缺口要填补。
- 2/ 90 天可取消条款，与 SpaceX 同 Anthropic 和 Google 的交易类似，资产负债表风险为零。考虑到收入机会，这对 Amy Hood 来说签字毫无压力。

对 SpaceX 而言，下一个自然的问题就是融资。没有头部超大规模云厂商的资产负债表，Elon 怎么付得起这么多资本开支？我们预计是以下两项的组合：

- 1/ NVIDIA 的支持，以厂商融资（vendor financing）形式降低前期现金成本。这很可能就是 Elon 在财报电话会上宣布只站队 NVIDIA 的原因！正如我们的加速器模型反复说明的，xAI/SpaceX 曾积极评估 TPU 和 AMD 等替代方案——所以多半是财务账让他们放弃了这些选项、专注 NVIDIA。
- 2/ 由行业最高定价驱动、凭借最快交付时间实现的经营现金流融资：SpaceX 将继续以 3-5 个月交期销售大规模算力——一个无可匹敌的供给——并相应定出 $30-50M/MW/年的价格。这让资本开支不到一年即可回本。我们在 [Meta Compute](https://newsletter.semianalysis.com/p/meta-compute-everyone-wants-to-be) 一文中深入探讨过这一点。

这一切意味着 SpaceX 有望在 2027 年底走上 $300B ARR 的道路。这还只假设其 2027 年增量算力的 50% 被变现，其余留给 Grok 和 Cursor 团队做训练（未建模任何推理收入）。

![](https://substack-post-media.s3.amazonaws.com/public/images/731a10f2-4e94-4d9c-abe7-b3bf1f93ccb0_2700x1440.png)
*来源：SemiAnalysis Tokenomics Model*

下面进入正题。先从微软讲起——这家巨头终于壮观地醒过来了：去年的暂停已经逆转，年初至今已签署 10GW 具约束力合同。我们将简要讨论达到 $100M/MW/年推理收入的经济账。随后转向 SpaceX，分析他们的数据中心爬坡，以及 2027 年底前实现 10GW+ 的可行性。

# 微软的 10GW 觉醒：抢下 $100M/MW/年的机会

2024 年 12 月，我们在[数据中心模型](https://semianalysis.com/datacenter-industry-model/)中比任何人都更早指出微软租赁活动的急剧暂停。今天，巨人醒了。[我们的模型逐季追踪租赁活动、neocloud 签约、自建开工，以及大规模具约束力的 PPA 与 ESA。](https://semianalysis.com/datacenter-industry-model/)下面我们展示输出结果。微软在上述所有层面合计已签约超过 10GW，相当于约 $300B 的新增具约束力承诺。

![SemiAnalysis 图表展示微软 2025 与 2026 年能源合同与建设活动的预计增长。
AI 生成内容可能不准确。](https://substack-post-media.s3.amazonaws.com/public/images/2151a0ea-4cb2-4d92-bca2-629635199d33_1248x666.png)
*来源：SemiAnalysis Datacenter Model*

这次觉醒的一个关键原因，是他们不顾一切地需要算力来抓住 $100M/MW/年 的收入机会。微软于 2025 年 10 月与 OpenAI 签署了 $250B 协议，在我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)中估算总量约为 7GW——这是理解「美元对瓦特」计算细节的全球最佳工具。这笔庞大的基础设施即服务（IaaS）交易使微软在其他用例上高度受制于算力。他们一直无法把自己对 OpenAI 模型的访问权用于 API 业务 Foundry，或用于 Copilot 等应用。

然而，恰恰是这些服务的利润率和每 MW 收入遥遥领先。我们在 [AI 价值捕获](https://newsletter.semianalysis.com/p/ai-value-capture-the-shift-to-model)一文中深入解释过。

过去一个月，老练的投资者终于形成共识：按 API 价格提供前沿 token 实际上是一门极高毛利的生意。早在[一月](https://semianalysis.com/institutional/inference-gross-margin-framework-model-providers-dynamically-control-economics-via-interactivity-or-user-happiness/)，我们就最先向 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)订阅客户指出了这一点，解释了推理毛利率为何在 60% 以上。随后在六月，我们又跟进一篇[深度解析](https://semianalysis.com/institutional/anthropic-likely-has-85-api-gross-margins/)，展示 Opus 4.8 的毛利率尤其高达 85%+。此后这成了所有人分析 Anthropic 时的默认引用数字。

为了得出这些毛利估算，我们不得不仔细综合泄露的财务数据、[InferenceX](https://inferencex.semianalysis.com) 数据、对业内所有最新加速器的微基准测试、开源实验室的论文、博客与推文等等。[DeepSeek 投资人电话会泄露](https://news.pedaily.cn/202607/566749.shtml)（其中提到他们的 GPU 回本期为 10 个月）等新数据点证实我们的估算量级正确，但我们也率先承认：缺乏颗粒度令人极不满意。**与其要一个全公司层面的推理毛利率数字，你真正想知道的是整条吞吐–延迟帕累托前沿上每一种（模型, 加速器）组合的毛利率。** 比如：在 Trainium3 上服务 Opus 5 Fast 与在 TPUv7 上服务 Fable 5，毛利率各是多少？

我们用[推理模拟器](https://semianalysis.com/consulting)回答这个问题，该产品仅面向 SemiAnalysis 咨询客户。

我们的 [AI 云 TCO](https://semianalysis.com/ai-cloud-tco-model/) 模型已经回答了等式的成本一侧，但收入一侧在历史上一直不可知。为解决这一问题，我们编写了一个仿真框架，在虚拟硬件上仿真真实的模型执行，背后是覆盖多种加速器与算子类型、经过调校的细粒度性能模型。我们在每一种可能的服务配置下将每个模型运行于仿真的 XPU 上，并混合真实世界与理想化的服务条件。这使我们能够在对模型架构做出充分知情的假设的前提下，精确估计任意软件、硬件与工作负载组合的性能。

得益于这个模拟器，**我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)现在包含了在所有相关芯片上运行 OpenAI/Anthropic 旗舰模型的每 MW 收入高层级数字。** 工作负载形态显然是巨大的变量，我们仿真了运行总价值超过 $1M 的智能体轨迹（采集自我们自己的使用），同时满足从第一方端点实测得到的真实交互性与 TTFT 水平。作为预告，以下是我们在 GB200 与 GB300 上服务 Fable 5 的数字：

![](https://substack-post-media.s3.amazonaws.com/public/images/408b0a52-7932-4bdd-ae9c-5fa7a159845b_1247x620.png)
*来源：SemiAnalysis Tokenomics Model*

**这就是微软每 MW $100M 的机会。** 鉴于近期 Codex 需求激增、OpenAI ARR 随之加速，我们相信微软通过服务 OAI 模型能够以类似的费率将算力变现。

要抓住这个一生一次的机会，微软和 AI 实验室需要数据中心，而且要快、要大。SpaceX 已经两次证明他们能比别人建得更快，但其算力产能到 2026 年底「只有」2GW。他们真的能在 2027 年短短一年内建成 10GW+ 吗？

## SpaceX：以星际速度建设数据中心

在我们的 [Meta Compute](https://newsletter.semianalysis.com/p/meta-compute-everyone-wants-to-be) 一文中，我们深入解释了为什么 Elon 再一次证明自己是商业天才。他明白 AI 实验室的利润率已大幅飙升，因此为他的 GPU 集群引入了「价值定价法」，而不是更常见的「成本加成」。

要让这台机器持续运转，Elon 需要比任何人都更快地建设数据中心。我们相信他做得到。这份信心从何而来？我们已多次撰文讨论过 [Elon 的速度](https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter)：122 天建成 Colossus 1 的 300MW、六个月建成 Colossus 2 的 200MW、为绕开许可审批把自备电厂建在边境 1 公里外，等等。

此后还有更多速度展示。Southaven 电厂已从 2026 年 2 月的 27 台燃气轮机（约 495MW）扩张到 2026 年 7 月的 69 台（1.7GW）。

还有「[MiniHard](https://x.com/elonmusk/status/2082613281328660734)」的亮相——2026 年 3 月启动垂直施工后，很可能仅用约 5 个月就达到 450-500MW！这并不意味着 Elon 建得比别人更好，他只是采用了另一套打法。

开关设备和大功率变压器排单到两年后？那就从中国买功率模块，跳过大型电力变压器（LPT），把中压电从发电侧直接送到供应充足得多的低压变压器。Elon 的公司拥有世界上最有天赋的电气工程师——没有人比他们更懂如何权衡速度与效率。全球大多数数据中心运营商都在为效率和质量优化——这是拿下 15-20 年照付不议（take-or-pay）超大规模云厂商数据中心合同的唯一途径。SpaceX 将专注于完全不同的取舍：速度高于一切。在算力紧缺、AI token 利润率极高的时代，一个三个月即可交付、带 90 天取消条款的 500MW 集群，是世界上最稀缺、最有价值的资产之一。所有常规「质量」指标都无关紧要。证据？Google——世界上垂直整合程度最高的基础设施公司——最后不知怎么就跟 SpaceX 签了约。

燃气轮机排单 5 年以上？GEV 是这样，但其他选择很多——我们的能源模型追踪了 30 多家已拿到服务数据中心大额订单的燃气发电设备制造商。只要你挖得够深、愿意与 新供应商合作，可用产能相当充裕。轮机二级市场成交量正在激增——例如，最初计划送往 Oracle 新墨西哥州场址的轮机全部流入了市场。二级市场价格很高，但 Elon 付得起。

劳动力才是终极约束？那就尽可能并行施工、压缩调试流程、尽可能预组装。据报道，Colossus 2 施工期日劳动力峰值约 3,000 名建筑工人，低于其他在建吉瓦级数据中心的水平（原文此处数字表述残缺）。Elon 历来擅长以低于行业标准的人员配置完成伟业——看看 Tesla 和 SpaceX 的历史就知道。

这样算来，到 2027 年建成多座这样的机房楼体（shell）时间绰绰有余。而且这还是他第一个真正的绿地项目，下一座大概能做得更快。当然，另一条路是改造（retrofit）。正如我们去年 xAI 深度解析所讲，Colossus 1 和 2 正是靠改造以惊人的速度建成的。

一年建成 10+GW 则是另一回事。SpaceX 需要在全国范围内物色合适的土地——许可宽松、可获燃气。不过我们相信，可选方案远多于支撑一轮实质性爬坡所需。这自然将在很大程度上依赖现场燃气发电——请参阅我们的能源深度解析，了解其运作方式和必要性。

付费墙之后，我们将讨论我们猜测 Elon 可能拿下的部分场址。

# 这怎么可能？
