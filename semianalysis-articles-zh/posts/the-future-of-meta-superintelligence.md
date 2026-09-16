---
title: "Meta Superintelligence 的未来：一年进展更新"
title_en: "The Future of Meta Superintelligence: A 1 Year Progress Update"
subtitle: "一家顶级 RL 环境初创公司凭空诞生、我们见过的最激进算力爬坡、2000 公里以上的 scale-across，以及给 Google DeepMind 的几点建议"
date: 2026-07-09
source: https://newsletter.semianalysis.com/p/the-future-of-meta-superintelligence
crawled: 2026-09-15
authors: ["Max Kan", "Julien Martin-Prin", "Jeremie Eliahou Ontiveros", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Meta Superintelligence 的未来：一年进展更新

> 原文：[The Future of Meta Superintelligence: A 1 Year Progress Update](https://newsletter.semianalysis.com/p/the-future-of-meta-superintelligence) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**一家顶级 RL 环境初创公司凭空诞生、我们见过的最激进算力爬坡、2000 公里以上的 scale-across，以及给 Google DeepMind 的几点建议**

自灾难性的 Llama 4 发布促使扎克伯格（Zuck）重建其整个 AI 组织以来，已经过去一年多。亮点包括：震惊业界的 143 亿美元 Scale AI「投资」，只为挖走 Alexandr Wang 及其安全、评估与对齐实验室（SEAL）团队的最优秀人才；向顶级 AI 研究员/工程师开出的数亿美元（有时超过 10 亿美元）薪酬包；以及借助全新「Tent」数据中心设计实现的加速算力爬坡。更多细节，请参阅我们关于 MSL 的[首发文章](https://newsletter.semianalysis.com/p/meta-superintelligence-leadership-compute-talent-and-data)。

自那以后，前沿 AI 越来越像 OpenAI 与 Anthropic 之间的双雄争霸。Google 曾凭借 Gemini 3 Pro 和 Nano Banana 短暂站上聚光灯下，但此后光环急剧褪色。尽管完成了对 Windsurf 的收购，他们离一款有说服力的智能体编程产品仍相去甚远，而 3.5 Flash 是一个刷榜的道具（benchmaxxed prop），在真实场景中的表现远逊于 GPT 5.5 和 Opus 4.8（更别提 Fable 和 5.6 了）。3.5 Pro 在编程上甚至没到 Opus 的水平。Microsoft 已经把他们凭借 GitHub Copilot 取得的先发优势挥霍殆尽，也未能有效利用其对 OpenAI IP 的访问权。SpaceXAI 每年向 Anthropic/Google 出售价值 260 亿美元的 GPU，而中国实验室则实在太缺算力，无法真正触及前沿。

与此同时，MSL 于今年 4 月随 Muse Spark 的发布完成公开首秀。你可以说这个模型对 Meta 而言是一种相对退步。Llama 3 70B 和 3.1 405B 发布时都是 SOTA 开源模型，而 Muse Spark 尽管同样闭源，在大多数基准上却落后于同期发布的开源模型 DeepSeek v4 Pro 和 Kimi K2.6。

![](https://substack-post-media.s3.amazonaws.com/public/images/ba2b8877-a6d2-42cc-81c1-b01a6f3f2110_1456x749.webp)
*来源：SemiAnalysis Tokenomics 模型*

然而，孤立地评判 Muse Spark 是只见树木、不见森林。对 MSL 而言，重要的是斜率，而不是截距。从零开始重建整个团队显然会伴随一些短期挫折，而 Meta 看起来终于还清了这笔债。因此，有趣的问题不在于 MSL 今天在哪里，而在于预测他们未来 6 个月会走到哪里。

最简单地讲，构建真正的前沿模型需要三样东西：**数据**、**人才**和**算力**。我们认为 **Meta** 是唯一有望在三者上都做到世界级的超大规模厂商/新型实验室（neolab），因此**拥有追赶 Anthropic/OpenAI 的最佳机会**。我们将在下文详细解释原因，但作为预告，这里先给出我们全新 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)的 AI 算力预测。

![](https://substack-post-media.s3.amazonaws.com/public/images/7fe52455-f883-4458-9b83-eeb4e7268982_1456x693.webp)
*来源：SemiAnalysis Tokenomics 模型*

最后，在付费墙之后，我们将讨论这一切对 Google——那家今天大多数人仍认为凑齐了「AI 三巨头」的公司——意味着什么。

### **数据是新的石油（这次是真的）**

我们从数据讲起，因为它是 Meta 最新的优势，也可能是三者中最被低估的一个。

2024 年，Ilya 说出了那句名言：「数据是 AI 的化石燃料。」这个类比正确地强调了数据对训练 AI 模型的重要性，但错误地假设好数据的数量是有限的。现实中，只要需求足够强劲，市场力量总会找到办法。

这一次，看不见的手创造出了一条全新的人类数据/RL 环境供应链。三家在位者——Mercor、Surge 和 Handshake——的 ARR 都已超过 10 亿美元，而许多成立仅一年左右的新入场者（如 Fleet、Mechanize 和 Afterquery）的 ARR 已在 1 亿美元上下。

![](https://substack-post-media.s3.amazonaws.com/public/images/23576eef-6ae2-4498-a8c3-c0e97c669446_1456x1024.webp)
*来源：公开披露信息，SemiAnalysis*

强化学习（RL）是当今提升 AI 能力最重要的扩展定律。大致思路是：不再只是预测下一个 token，而是教会模型如何完成整项任务（例如修复代码库中的一个 bug）。除了*任务*本身，RL 还要求你为模型提供完成任务所在的*环境*、模型与环境交互可用的*工具*，以及检查模型答案正确与否的*验证器*。更多背景请参阅我们[此前](https://newsletter.semianalysis.com/p/rl-systems-mind-the-gap-matching)[关于](https://newsletter.semianalysis.com/p/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data)[RL 的几篇文章](https://newsletter.semianalysis.com/p/rl-environments-and-rl-for-science)。

值得强调的是，许多 AI 业内人士相信，仅凭更多的 RL 环境/任务就足以自动化几乎所有白领工作。以下引自我室友 Sholto Douglas——Anthropic 一位知名研究员——去年做客 [Dwarkesh 播客](https://www.dwarkesh.com/p/sholto-trenton-2)时的话：

> 即使算法进展停滞不前，我们始终没找到让进步延续下去的办法——我不认为是这样，进展并没有停滞，看起来进展得很好——**只要拥有足够多的、正确类型的数据，当前这套算法就足以自动化白领工作。**与所有这些工作薪资加总的可服务市场（TAM）相比，这件事划算得不成比例。

一般而言，所有这些数据公司都靠从相关行业雇用专家承包商来创建新的 RL 任务（这也是它被称为「人类数据」的原因）。不过，如今每家数据公司还在拼命寻找另一样东西：白领工作的真实录屏。

#### **屏幕录制对制作 RL 任务极其有价值**

想当然地，你可能会认为屏幕录制主要对监督微调（SFT）这类较旧的训练范式有用，那些范式教 AI 模仿人类。毕竟，RL 的全部要义就是让 AI 自己摸索步骤，并且只根据结果来分配奖励。

然而在现实中，只要愿意多做一点额外的工作，屏幕录制对制作 RL 任务仍然可以极其有用。

第一个好处是真实性。RL 数据只有在 1) 代表真实的有经济价值的工作，且 2) 难度对 AI 恰到好处时，才算好数据。太容易，AI 无从学习；太难，它永远拿不到任何奖励。

校准任务难度的唯一办法，就是让 AI 把同一个问题多尝试解决若干次，然后据此迭代。如今要做出一个对前沿模型来说足够难的 RL 任务其实相当难，所以你的专家承包商通常把时间花在把任务变得更难上。例如，Mechanize 只[期望](https://www.mechanize.work/what-working-here-is-like/)他们付 40 万美元以上年薪聘来的软件工程师每周做出 1 个好任务。

在这些约束下，如果你让一位普通 PE 分析师从零开始构思一个新的金融建模任务（因为你只想通过 RL 让自己的模型在 Excel 上更强），最终得到的往往是一个为难度而牺牲真实性的造作任务。这就是 OpenAI 的 [GDPval](https://openai.com/index/gdpval/) 和 Mercor 的 [Apex](https://www.mercor.com/apex/) 套件这类基准的主要问题（一个好的基准与一个好的 RL 环境大体等价）。读一读那些任务就会发现，大多数都被不自然地过度规格化，听起来不像是人类真的会交给 AI 去做的事。

举个例子，有一个 GDPval 任务要求 AI 制定一份行程。在现实世界中，这个任务的难点在于从邮件、短信、各类网站等分散来源抓取所有上下文来搭建日程，但 GDPval 把这些统统略过，直接给 AI 超详细的分步指令。人类绝不会给 AI 写这种 1000 多词的提示词——到了那个程度，自己动手做行程反而更容易！

![](https://substack-post-media.s3.amazonaws.com/public/images/71d7b5fa-18cc-4ca4-be5e-6b1baffdf0ef_736x632.webp)
*来源：OpenAI，SemiAnalysis*

另一方面，如果你以某人做日常工作的屏幕录制为基础来构建任务，那么根据定义，它必然代表真实的知识工作。

与此相关，工作流的最佳实践和正确性的定义会随时间大幅变化，所以确保你的数据*持续*真实的唯一办法，就是拥有源源不断的真实录制。例如，今天一个好的编程 RL 任务会涉及编排子智能体（subagent），而这在仅仅 7 个月前根本不存在。

屏幕录制对制作验证器也极其有用。如今，大多数验证器都是*评分量表（rubric）*。由于白领工作通常是主观的——不像数学和编程，你可以直接检查最终数字是否正确、或者跑一套集成测试——你的验证器最终会是一套编码在评分量表中的规则/偏好，由人类或 LLM 用它来给 AI 的输出打分。随着任务本身变得更长、更复杂，与之对应的评分量表也会如此。

如果你收集到足够多（通常是数千条）的人在大致相同任务、略微不同情境下操作的痕迹（trace），你最终会捕捉到该任务的整个动作空间。这就足以让 LLM 或多或少地一次性写出评分量表。当然，你仍然需要人来做最终审核，而且关键是要为所有不同标准分配权重，但这显然比让专家从零开始创建评分量表高效得多（通常质量也更高）。

![](https://substack-post-media.s3.amazonaws.com/public/images/d47f50a2-0f50-4182-91e5-0428f8fa0617_774x877.webp)
*OpenAI HealthBench 的评分量表示例。来源：OpenAI，SemiAnalysis*

录制对确定性验证器同样大有用处。知道任务完成后应用的底层状态，往往是创建知识工作确定性验证器的第一步，因为验证器的全部意义就在于检查 AI 是否成功达到了期望的终态。一段足够详细的录制可以免费提供这些信息。

#### **Meta 刚刚创建了一家顶级 RL 环境初创公司**

有了这些背景，我们就能更好地理解最近的新闻：Meta 开始追踪员工的屏幕、键盘和鼠标动作。这简直可以算是当今世界上最有价值的数据之一！当然，由 Scale AI 出身的那位掌门来牵头这场转型，也颇具诗意。

当所有数据公司都在拼命试图与投行、律所和广告公司合作录制其工作流时，Meta 是世界上少数几家内部就拥有分别投身于这些行业的足够庞大人力的公司之一。

尽管承受着公关冲击和最初的员工反弹，Meta 依然足够敏捷和激进地做了这件事，这已经相当令人印象深刻。是的，他们后来[有所](https://www.theinformation.com/articles/meta-rolls-back-parts-employee-tracking-tool-staff-backlash)回撤，加强了隐私保护，并允许员工暂停追踪器 30 分钟，但我们认为这些是非常轻微的让步。

此外，他们在 5 月底把数据工作提升到了*另一个层级*：在最近一轮裁员/重组中宣布成立新的「应用 AI 工程组织」。**约 3000 名工程师**——包括 70% 的新毕业生和数量可观的资深工程师——今后将**全职制作 RL 任务/环境**。

我们认为，这是 MSL 一个极其被低估的优势。在从 RL 环境初创公司购买编程数据方面，Anthropic 迄今是最激进的实验室，这也是他们的模型如今如此擅长编程的一个重要原因。

Mercor 最近[披露](https://x.com/EverettRandle/status/2074527860510085498)，2026 年第二季度其平台记录了 2,517,000 个专家小时，相当于约 4800 人每周工作 40 小时。Meta 已经处在同一量级，而且其平均质量可能更高。此外，如果这个实验最终被证明像我们认为的那样有价值，他们还有另外约 7 万人可以调用。

也值得在此澄清一个迷思：这 3000 名 Meta 工程师并不会去做无脑的、低水平的数据标注。第三世界国家受教育不足的承包商画边框或给文本做 NSFW 分类的时代早已过去。到了这个阶段，模型已经足够聪明，制作一条好的训练数据本身就是一场真正的智力挑战。深入理解失败模式、确保你的环境对奖励黑客（reward hacking）稳健、在不降低质量的前提下扩展任务创建，全都不是简单的工程问题。

除了向数据公司采购之外，Anthropic 的工程师自己也已制作编程任务一年多。前沿实验室愿意为一个像样的编程任务支付 5000 美元以上。Mercor 的平均时薪最近[突破](https://x.com/BrendanFoody/status/2057195063126405430?s=20)了 100 美元/小时，而软件工程师（SWE）的时薪显著高于平均水平。这些数据公司里最顶尖的专家承包商年收入超过 7 位数。

制作 RL 数据不仅明显比某些大厂工作更有经济价值，说不定还更有智力上的刺激。

### **Instagram 广告可以养活大量算力**

与 OpenAI 和 Anthropic 相比，Meta 拥有一份与超大规模厂商身份相称的资产负债表；与 Google 相比，Meta 没有一个急于把尽可能多算力租出去的云业务。再加上扎克伯格愿意接受[自由现金流为负](https://semianalysis.com/institutional/hyperscaler-fcf-will-be-negative-in-cy27/)，Meta 应该能点亮比世界上任何其他公司都多的内部 AI 算力。

这正是我们看到正在发生的事情。我们全新的 Tokenomics 模型预测，到今年年底，Meta 的 AI 算力将超过 OpenAI 和 Anthropic 两家中的任何一家。

![](https://substack-post-media.s3.amazonaws.com/public/images/5bf2a781-ae54-4957-9a03-9974d35d6bf6_1456x693.webp)
*来源：SemiAnalysis Tokenomics 模型*

值得注意的是，这些算力中有相当一部分将用于推荐系统（RecSys）和生成式广告。不过，即使我们保持保守、只把 Meta 特定的高调数据中心站点划归 MSL，他们 2026 到 2027 年的训练算力仍与 OpenAI 和 Anthropic 相当。关于 Meta 算力战略更详细的拆解，请参阅我们近期的[通讯](https://newsletter.semianalysis.com/p/meta-compute-everyone-wants-to-be)，具体数字见我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)。

#### **一场由 5 大巨塔引领的前所未有的算力爬坡**

关于 Colossus 和 Elon 快速点亮海量算力的能力，外界已有[大量](https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter)报道，但 Meta 今天正在做的事情可以说更加惊人——这一点我们的[数据中心行业模型](https://semianalysis.com/datacenter-industry-model/)订阅者一年多前就知道了。

Meta 正在同时建设 5 个 1GW+ 级的「巨塔」（titan）集群：俄亥俄的 Prometheus、路易斯安那的 Hyperion，以及位于 El Paso、爱荷华和印第安纳的 3 个未命名园区。

人类历史上从未见过一整座完整 1GW 园区同时在建——最接近的纪录是 AWS 为 Project Rainier 在印第安纳建设的 800MW——而 Meta 现在同时有两个！Hyperion 和爱荷华。

在 Hyperion，Meta 正在建造世界上最大的单体建筑，每栋 400MW。今天在建总量达 1.5GW：3 栋 400MW 的巨兽，外加另外 3 栋标准的 100MW 建筑。

![](https://substack-post-media.s3.amazonaws.com/public/images/0f63fb95-9240-4645-a199-6be5406d9856_1456x803.webp)
*来源：SemiAnalysis 数据中心模型*

在爱荷华，Meta 与一家领先的数据中心运营商签署了 1GW 租约（[正如我们 2025 年 6 月在我们的数据中心模型中提示的](https://semianalysis.com/datacenter-industry-model/)）。从下面的卫星图可以看到，他们在仅仅 1 年内就从一片空地变成了整个 GW 全面开建。

![](https://substack-post-media.s3.amazonaws.com/public/images/8ae8bdd3-8484-4594-b9e1-7295847145b2_1456x800.webp)
*2025 年 5 月（左）对比 2026 年 5 月（右）。来源：SemiAnalysis 数据中心模型*

在 Prometheus——如今已部分投运——Meta 目前在建的还不到完整的 1GW，但他们正在全面拥抱我们在上一篇 MSL 文章中点出的那种务实帐篷（tent）数据中心设计。Prometheus 集群还在不断扩张——从最初的约 1GW 到两年内的如今超过 3GW。要理解 Meta 如何做到这一点，请查看我们的[数据中心模型](https://semianalysis.com/datacenter-industry-model/)。我们对全部五座巨塔有建筑级别的跟踪，并且是第一家以精确月度时间线指出任何扩建的机构。其中一些设施使用表后（behind-the-meter）电力，我们跟踪确切的系统类型并提示许可风险。

![](https://substack-post-media.s3.amazonaws.com/public/images/93ba1a72-70bb-4cf1-a3d6-1358a498fd99_1456x715.webp)
*来源：SemiAnalysis 数据中心模型*

#### **连接巨塔：Meta 的 scale-across 方案**

由于 Meta 主要自建并自营数据中心，他们在定制基础设施以契合实际需求方面拥有更大的灵活性。Prometheus 就是一个好例子。Prometheus 不是单一数据中心或园区，而是分布在 6 个园区的 27 座数据中心组成的星座。其中 5 座彼此相距 6 公里以内，第 6 座距离其余各座 75 到 80 公里。

![](https://substack-post-media.s3.amazonaws.com/public/images/3f7b2f35-8c41-43a5-a903-607f493e52f8_2048x983.png)
*来源：SemiAnalysis AI 网络模型，Meta*

这一设计选择背后的原因在于：扩展到数百兆瓦目前极具挑战性，尤其是在散热和电力管理方面。训练下一代前沿 AI 模型需要大量算力——远超 100MW——正因如此，把工作负载分散到多座数据中心才是突破当前限制的前进路径。

不过，伴随这一设计选择而来的是一项新挑战：网络。更大集群的全部意义，在于能够在合理的时间框架内训练更大的模型。如果加速器之间无法高效通信，吉瓦级园区就毫无意义。这就是 scale-across 登场的地方。

为此，Meta 推出了一个名为 AI-Backbone（简称 AIBB）的方案。这是其 [10X Backbone](https://engineering.fb.com/2025/10/16/data-center-engineering/10x-backbone-how-meta-is-scaling-backbone-connectivity-for-ai/) 的演进版本，专为 AI 和超大规模集群需求而设计。该网络架构由多条 L3 Superspine（或称后端聚合，Backend Aggregation，简称 BAG）组成，互联多达 5 个 DSF（解耦调度网络，Disaggregated Scheduled Fabric）或 7 个 NSF（非调度网络，Non-Scheduled Fabric）横向扩展域（这些域也可以混搭）。L3 Superspine 再汇聚到单一的 L4 跨 BAG 枢纽，该枢纽计划为整个 Prometheus 集群提供约 22 Pbit/秒的双向带宽。

![](https://substack-post-media.s3.amazonaws.com/public/images/7dba2e3c-9f84-4083-a574-80f82a68e91d_2048x692.png)
*来源：SemiAnalysis AI 网络模型*

DSF 和 NSF 域位于单一数据中心机房之内，而 L3 和 L4 则分布在所有数据中心。L3 层位于单一园区内，而 L4 主要用于把各园区互联起来。L3 与 L4 之间的连接是 LR 光模块与采用 ZR 光模块的密集波分复用（DWDM）系统的组合，具体取决于通往另一园区的光纤长度。

![](https://substack-post-media.s3.amazonaws.com/public/images/c8f98e89-d671-4183-88a6-66b273d1b90a_2048x785.png)
*来源：SemiAnalyis AI 网络模型*

虽然这看起来是完美方案，但这种网络架构以及数据中心之间的距离天然引入延迟。在 DSF 或 NSF 域内部，延迟通常在 1 到 10 微秒之间，但到达 100 公里外站点的延迟不可能低于 500 微秒——仅光纤中光的传播就决定了这一点——这迫使 Meta 对训练工作流采用异步策略。预训练可以在单一域内同步进行，而 RL 则可以相当容易地在全球范围分布式展开。

总体而言，Prometheus 为当前的限制提供了一种解法，而其他巨塔在 scale-across 上会走得更远——把相距达 2,000 公里以上的园区连接起来。

### **集结 MSL 超级战队**

去年，Meta 因开出能让 Patrick Mahomes 都眼红的 AI 研究员薪酬包而名声大噪。在斥资 140 亿美元收购 Alexandr Wang、再花 10 亿美元以上买断 Nat Friedman 和 Daniel Gross 的风投基金之后，据[报道](https://www.theinformation.com/newsletters/ai-agenda/zuckerbergs-new-ai-team-good)，到 2025 年 6 月底 Meta 已挖走至少 14 名研究员。这些人大多来自 OpenAI，但也有少数来自 Anthropic 和 Google。一些响亮的名字包括 Shengjia Zhao、Trapit Bansal、Joel Pobar 和 Jack Rae。

自那以后，MSL 延续了其疯狂招人的势头。值得注意的研究/工程岗位新聘包括：

- Andrew Tulloch（前 Thinking Machines 联合创始人）
- Joshua Gross、Mark Jen、Yinghai Lu（Thinking Machines 创始团队）
- Jason Wei、Hyung Won Chung 和 Zhiqing Sun（前 OpenAI）

MSL 招的不只是技术岗成员。今年 1 月，他们请来了 [Dina Powell McCormick](https://about.fb.com/news/2026/01/dina-powell-mccormick-joins-meta-as-president-and-vice-chairman/)——一位人脉深厚的金融人士、特朗普和小布什（W Bush）的前顾问——出任总裁兼副主席，帮助建设其算力舰队。同样地，他们 4 月还从 OpenAI 的算力团队挖走了三剑客（Pete Hoeschele、Anuj Saharan、Shamez Hemani），不过其中 1 人已经因为 Meta 基础设施组织内部的文化问题而离职。

就像一支体育战队突然开始挥金如土签约超级巨星一样，这支新集结的 Meta 超级战队能否真正夺冠，只有时间能给出答案。不过，扎克伯格已经亮明意图，正在汇集一切可用资源，向前沿发起真正的冲击。截至今天，其他任何超大规模厂商都说不出同样的话。这对 Meta 的业务是福是祸取决于你的先验判断，但我们认为，他们拥有追赶 Anthropic/OpenAI 的最佳机会。

### **但话说回来，成功远非板上钉钉**

我们总体上看好 MSL 的未来，但值得强调的是，他们基本上还停留在第一步。**我们赞赏他们为真正冲击 RSI（递归自我改进）而调动资源与胆识，但现在他们必须做真正的工作了。**追赶 Anthropic 说来容易做来难，而且归根结底，Meta 仍是一家内部意见与优先级相互竞争众多的大科技公司。

正如我们在近期一篇关于 [Meta 算力](https://newsletter.semianalysis.com/p/meta-compute-everyone-wants-to-be)的文章中所解释的，Meta 有很多方式可以在短期内临时性地将算力变现，同时为自己保留选择权——一旦其研究组织达到正确的里程碑，就全力押注 MSL。**然而，如果他们做出任何表明决心真正动摇的事情——比如签署没有回拨（clawback）条款的长期算力出售协议、解散新成立的 RL 任务创建组织，或者放任顶级研究员流失——那么我们的看好程度将会实质性下降。**你甚至可以说，其中任何一条都无异于给 MSL 判了死刑。

**我们在正式发布之前简要测试了 Muse Spark 1.1，认为在通用智能体场景下，它大致与 Opus 4.6 或 GLM 5.2 相当。**Meta 选择把该模型定价在略低于 GLM 5.2 的水平，感觉是有意为之。我们的一些工程师注意到，它有个坏习惯：对警告置之不理而不是去修复，而且不能正确使用编辑工具。

我们内部的 token 用量都不会迁移到 Muse Spark 1.1，但在现阶段这仍在预期之内。即便在乐观情形下，我们也不预计他们能在今年年底之前与 Anthropic 或 OpenAI 持平。

### **这对 Google 意味着什么**
