---
title: "Anthropic 订阅的价值是 OpenAI 的 5 倍以上"
title_en: "Anthropic Subscriptions Offer 5x+ More Value Than OpenAI"
subtitle: "实测 Anthropic、OpenAI、Meta、SpaceXAI、MiniMax、Moonshot、Z.ai、Cursor 与 Cognition 全部 AI 订阅计划的用量上限"
date: 2026-10-05
source: https://newsletter.semianalysis.com/p/anthropic-subscriptions-offer-5x
crawled: 2026-09-15
authors: ["Andrew Megalaa", "Max Kan", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-10-08
---

# Anthropic 订阅的价值是 OpenAI 的 5 倍以上

> 原文：[Anthropic Subscriptions Offer 5x+ More Value Than OpenAI](https://newsletter.semianalysis.com/p/anthropic-subscriptions-offer-5x) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**实测 Anthropic、OpenAI、Meta、SpaceXAI、MiniMax、Moonshot、Z.ai、Cursor 与 Cognition 全部 AI 订阅计划的用量上限**

订阅计划仍是消费者与小企业为 AI 付费的主要方式。这些计划的补贴力度极大——正如我们此前在 [6 月](https://semianalysis.com/institutional/a-200-claude-plan-can-consume-8000-worth-of-tokens/)解释过的——但作为强力的客户获取与营销工具，在经济上依然说得通。例如，[OpenAI](https://x.com/thsottiaux/status/2102463847714247142)[慷慨](https://x.com/thsottiaux/status/2103637477760311522)[重置](https://x.com/thsottiaux/status/2105173168281506088)用量上限所赢得的口碑，是 Codex 采用率近期激增的部分原因，也迫使 Anthropic 为避免在舆论场上被吊打而[一再](https://x.com/ClaudeDevs/status/2078511173759324328)[收回](https://x.com/ClaudeDevs/status/2089798442306711646)[成命](https://x.com/ClaudeDevs/status/2093742321473065266)，取消了原本计划中的订阅削弱（nerf）。

此外，正因为订阅计划补贴力度如此之大，尽管它们只占总营收的一小部分，却可能对利润率和每 MW 营收（revenue per MW）产生重大影响。以 Anthropic 的以下粗略数字为例。

![](https://substack-post-media.s3.amazonaws.com/public/images/2ac5c578-4092-4afe-bdaf-cbf61f7f83b5_2048x1194.png)
*来源：SemiAnalysis Tokenomics Model*

**订阅虽仅占总营收的 10%，却可能占用超过 40% 的推理算力，并将混合每 MW 营收拉低约 $36M。** 订阅对 OpenAI 而言更为重要，因为其占总营收的比重更大。具体数字参见我们的 [Tokenomics Model](https://semianalysis.com/tokenomics-model/)。

换言之，**如果你想准确建模 AI 实验室的财务状况，就必须理解它们的订阅用量上限。**

那么，用量上限究竟如何运作？理解订阅的正确方式是：你每月支付的款项为你换得一定数量的「积分」（credits）。每个（模型，token 类型）组合消耗的积分数量各不相同。**由于积分成本比率可能与 API 价格比率大相径庭，同一计划的「价值」会随你运行的模型和工作负载而变化。** 换句话说，**孤立地说某个计划价值 $X 并无意义——你必须把（计划，模型，工作负载）这个完整三元组放在一起考量**。

下图展示了同一个 $200/月的 Claude 计划，其 API 等价价值如何随模型与工作负载而变化。

![](https://substack-post-media.s3.amazonaws.com/public/images/e61e3841-450f-4662-a21f-dc0f844d05ab_2000x1126.png)
*来源：SemiAnalysis Tokenomics Model*

单靠一张静态快照同样不够。各家实验室会随促销和新模型发布公开调整用量上限，也可以随时通过调整积分成本悄悄改变上限。理想做法是每天复核每个（计划，模型，token 类型）组合的成本，以便实时暴露任何变化。

这正是 SemiAnalysis 全新 [Subscriptions Dashboard](https://tokenomics.semianalysis.com/subscriptions) 所做的事，该面板仅向 [Tokenomics Model](https://semianalysis.com/tokenomics-model/) 订阅者开放。除 OpenAI 与 Anthropic 的全部订阅计划外，我们还跟踪 Meta、SpaceXAI、Cursor、Cognition、Z.ai、MiniMax 与 Moonshot。

![](https://substack-post-media.s3.amazonaws.com/public/images/6e451f84-a586-40da-90c8-5e2fcd196222_2048x1077.png)
*我们面板的截图，仅展示了可用数据的一小部分。来源：SemiAnalysis Tokenomics Model*

新的厂商、计划和模型一经发布就会加入。本文余下部分将概述各家当前的用量上限。除非另有说明，下文所有 token 数量与美元金额均假设为智能体（agentic）用法。

# 方法论

token 的定价通常按每百万 token（MTok）计，分为以下几类：

- 输入（Input）：进入 LLM 上下文窗口的、未经缓存的新鲜 token
- 缓存写入（Cache write）：为多轮对话而缓存的输入 token。通常比普通输入 token 略贵。
- 缓存读取（Cache read）：对话中此前轮次已缓存的 token。与未缓存 token 相比通常极为便宜。
- 输出（Output）：模型生成的 token。最昂贵的 token 类型。

此外，部分模型对超过某一上下文窗口长度的 token 收费更高。这类模型通常会在触及昂贵区间之前进行压缩（compact），因此我们的测量也保持在阈值以下。

![](https://substack-post-media.s3.amazonaws.com/public/images/fab43609-4792-498e-934f-a4455bd2b509_941x454.png)
*来源：OpenAI*

订阅计划并不公开这种细粒度定价。它们提供的只是一个 0 到 100% 的简单用量仪表，横跨 5 小时与 7 天两个窗口，有时还为某个模型（如 Fable）单设一个仪表。订阅档位之间的差异，只体现为相对该厂商其他计划的用量倍数。例如 OpenAI 曾在其 $20 Plus 计划中宣传「Expanded Codex usage」（Codex 用量扩展），在 $100 Pro 计划中宣传「比 Plus 多 5 倍用量」，在 $200 Pro 计划中宣传「20 倍用量」——直到他们把 $200 计划的用量砍掉[一半](https://x.com/thsottiaux/status/2104951965184925941?s=20)，并从其[定价](https://chatgpt.com/pricing/)页面上删除了所有相对用量的表述。

![](https://substackcdn.com/image/fetch/$s_!eIgD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd495b7d3-d488-4ffb-9f85-f52ea0d449fc_460x178.png)
*Claude Code 用量仪表截图。来源：Claude Code CLI*

## 实验设置

我们通过逐次只隔离一种 token 类型的实验，并观察模型厂商仪表的移动幅度，来计算每个（计划，模型，token 类型）三元组的订阅费率。一次实验即是用一个特定 prompt 反复调用若干次，使某一种 token 类型最大化、其余类型最小化。

![](https://substack-post-media.s3.amazonaws.com/public/images/0f26243f-cdd4-41a3-b89c-6b78dac4317b_2048x1034.png)
*来源：SemiAnalysis Tokenomics Model*

输入、缓存写入与缓存读取共用同一个 prompt 模板。我们取《战争与和平》（*War and Peace*）的一部分作为语料，因为部分模型在收到大段乱码时会拒绝响应。输入 token 实验在每次调用时使用随机标签，确保任何内容都不会被缓存。缓存写入实验以相同方式运行，但 prompt 被标记为可缓存，因此每个新标签都会强制写入一条新的缓存条目。缓存读取实验使用固定标签，因此首次调用写入缓存，其后每次重复调用都读取缓存。

输出 token 实验则用一篇技术文章来强制长输出，因为模型会拒绝「把 SemiAnalysis 重复 100,000 遍」这类机械式 prompt。

## 结果计算

每次调用我们记录两件事：厂商对每种类型计费的 token 数量，以及用量仪表的读数。把这些变成价格需要三步。

### 1. 测量每种 token 类型的费率

厂商的用量仪表通常以固定步长移动：可能是一整个百分点、一个积分、一分钱等。单个请求往往根本推不动仪表，因此单次请求的成本无法直接测量。

我们改为按「步」测量。请求运行期间，我们持续累计已用 token 总数；仪表每跳动一次，就存下当时的累计值。两次仪表跳动之间消耗的 token 构成一步，即仪表移动一个单位的成本。

我们丢弃两个不完整的步。实验开始时，仪表已走在通往下一次跳动的半路上，因此第一次跳动之前消耗的 token 不足一整步，会让费率显得偏高；最后一次跳动之后的 token 永远凑不满一步，所以也一并丢弃。

计算费率时，我们把完整各步中仪表移动的总量加起来，除以这些步消耗的 token 数。厂商对输入、输出与缓存 token 的计费各不相同，因此我们对每一类分别计算费率。

![](https://substack-post-media.s3.amazonaws.com/public/images/07a6b9ad-a758-4e40-9894-595aaf3d0e08_2048x1143.png)
*来源：SemiAnalysis Tokenomics Model*

注意事项：

- 由于我们每个请求只能读一次仪表，单步的误差可能达到一个请求之多。这些误差不会随连续步数增加而累积，因此我们跟踪的是一个区间而非单一数值，且计入的步数越多区间越窄。我们持续累加步数，直到区间收窄到 ±5% 以内，然后报告全部步数上的费率。
- 没有任何请求只包含单一类型的 token。例如某些计划要求每个请求都附带一组固定指令。我们用已测得的其他类型价格把这部分额外开销扣除。
- 在部分计划上，缓存读取几乎免费，甚至可能完全推不动仪表。若累计 500M（5 亿）缓存读取 token 后仪表仍纹丝不动，我们即认定缓存读取免费。

### 2. 把费率换算成每个窗口及每月的 token 数量

每次调用后，我们读取计划展示的每一个仪表：可能是 5 小时上限、每周上限，对 Fable 这类模型还有其专属的每周上限。于是每种 token 类型在每个仪表上都有一个「价格」——即一百万 token 会消耗该上限的百分之几。由这个价格即可反推上限能装下多少 token：例如一百万 token 消耗上限的 5%，则整个上限相当于 2,000 万 token。

![](https://substack-post-media.s3.amazonaws.com/public/images/51471699-71b4-4d96-96ef-5bcc29bed2b0_2048x901.png)
*来源：SemiAnalysis Tokenomics Model*

5 小时上限在一周内会重置多次，因此每月的量实际上由每周上限封顶。

### 3. 定价

最后，我们把每种类型的一百万 token 所消耗的上限百分比换算成美元金额，得出 API 等价价值。例如，若你消耗了 $200 计划每月上限的 1%，即相当于 $2。

随后，我们假设一种工作负载形态，在该比例下计算每个计划总共能提供多少 token。智能体工作负载采用我们 9 月自身的用量比例，见 [Tokenomics Model](https://semianalysis.com/tokenomics-model/) 的报告。

最后，乘以 API 价格下的每百万 token 混合单价，得到 API 等价价值。

![](https://substack-post-media.s3.amazonaws.com/public/images/a979d2fd-77fa-456d-b1c8-efb9f82d174a_2048x1002.png)
*来源：SemiAnalysis Tokenomics Model*

## 撞见某厂商的 A/B 测试

在打磨方法论的过程中，我们遇到一桩非常令人困惑的事：某厂商的同一个订阅，我们测试的 3 个账号中恰有 1 个的上限比另外 2 个低约 20%。这个不走运的账号注册时间又明显更久，我们一度担心该厂商存在某种诡异设定——根据账号年龄调整订阅上限。

好在与该厂商沟通之后，我们确认事实并非如此：这个不走运的账号只是他们正在运行的、规模「极小」的用量上限 A/B 测试的一部分。他们还特意强调，自己「并非一刀切地下调上限」，而是在测试「如何更好地平衡用户触及上限时的体验」。

这一结论有两点耐人寻味：

1. 它证明厂商随时可以悄悄更改订阅上限
2. 我们的方法足够灵敏，能探测到这类细微变化！

# OpenAI 对比 Anthropic

AI 订阅圈最大的问题，是 Anthropic 的上限与 OpenAI 相比孰优孰劣。注意 OpenAI 刚刚在上周对其订阅做出重大调整：把 $200 计划的 API 等价价值[砍半](https://x.com/thsottiaux/status/2104823812042940713?s=20)，并引入新的 $500 档位。以下数字描述的是 OAI 与 ANT 的**当前状态**；随后我们将深入剖析 OpenAI 的近期调整。

![](https://substack-post-media.s3.amazonaws.com/public/images/181ea48e-2e63-4f41-a742-c7af3d7eeb15_2048x1157.png)
*来源：SemiAnalysis Tokenomics Model*

在 GPT-6 Astra 对比 Fable 5.1 上，双方上限总体相当接近——但请记住，Fable 只能用到你上限的 50%。换句话说，你的 $200 ANT 计划在消耗 $2,485 的 Fable 5.1 之后仍有 50% 余量，而同档 OAI 计划在消耗 $2,897 的 Astra 之后就已彻底耗尽。

当我们把 Opus 5.5 与 GPT 6.1 Sol 放在一起比较时，这多出来的 50% 开始变得极为关键。

![](https://substack-post-media.s3.amazonaws.com/public/images/44bfcff4-5589-4822-a348-bc4e83cf478b_2048x1161.png)
*来源：SemiAnalysis Tokenomics Model*

在这一中间档模型上——两家公司都把它宣传为大多数用户的日常主力——Anthropic 是压倒性的更优交易，API 等价价值全面约为 5 倍。你可以说这对 OAI 不公平，因为 6.1 Sol 的单 token 价格远低于 Opus 5.5；但即便改比 token 数量，差距依然巨大。

![](https://substack-post-media.s3.amazonaws.com/public/images/e6b9e23d-8049-4235-8c21-9a5a2b0cd1f0_2048x1153.png)
*来源：SemiAnalysis Tokenomics Model*

总体而言，我们认为 API 等价价值是刻画订阅计划「价值」的最佳单一指标，但某些时候原始 token 数量可能更合适。例如，当某模型在 API 价格下本身就是一笔特别糟糕（或特别划算）的交易时，API 等价价值当然会产生误导。

token 效率同样是一个极其相关的因素，可惜行业在此缺乏可靠数据。很多人喜欢引用 Artificial Analysis 的这张[图表](https://artificialanalysis.ai/#price-and-cost)，但我们认为 AA Intelligence Index 中的基准任务完全不能代表人们用 LLM 做的真实工作。

## OpenAI 新的 $500 计划与大幅上限削减

我们的跟踪证实了 [Tibo](https://x.com/thsottiaux/status/2104823812042940713?s=20) 宣布的 OpenAI $200 计划价值削减 50%。削减前购买的 $200 计划可保留旧的高上限直至 10 月 29 日，新购计划则立即按低上限计。

![](https://substack-post-media.s3.amazonaws.com/public/images/2c53c9a0-1c69-4ee8-8e47-f86ae0655c0f_2048x1082.png)
*来源：SemiAnalysis Tokenomics Model*

如你所见，OpenAI 恰好把每个模型档位的 token 数量都砍半。这导致 Sol 档模型的 API 等价价值下降超过 50%，因为 OAI 同时还下调了 6.1 Sol 的缓存输入 token 定价。

新的 $500 计划相对旧 $200 计划仅多提供 21% 的 Astra。有意思的是，由于前述 6.1 Sol 降价，Sol 档模型的 API 等价价值反而下降了。

![](https://substack-post-media.s3.amazonaws.com/public/images/97d35c43-9687-4fd9-b825-6c3987d0cd14_2048x1113.png)
*来源：SemiAnalysis Tokenomics Model*

当然，300 TPS 的 Ultrafast 才是 $500 计划真正的头牌功能，我们目前正在测试其上限。结果一出来就会发布给 [Tokenomics Model](https://semianalysis.com/tokenomics-model/) 订阅者。我们也在积极测试在 Devin 等第三方应用中使用 ChatGPT 订阅时的上限。

$200/月的计划过去也比 OpenAI 其他订阅享受显著更高的补贴。若把每个（计划，模型）组合按 API 等价价值和每美元 token 数归一化，可以看到 Pro 100 在 Astra 上的单位美元价值约为 Plus 的 2 倍，而 Pro 200 在全部模型上又比 Pro 100 再高出约 2 倍。

![](https://substack-post-media.s3.amazonaws.com/public/images/67342d61-8eb1-426b-8553-c8abf4ebaba7_2048x1143.png)
*来源：SemiAnalysis Tokenomics Model*

经上周削减后，Pro 100、200、500 对每个模型提供的每美元 token 数已完全一致。Plus 在 Sol 上也相差不大，但在 Astra 上相对吃亏。

反观 Anthropic，其全部订阅档位早就提供相同的单位美元价值，且目前全面碾压 OpenAI。

![](https://substack-post-media.s3.amazonaws.com/public/images/45036f6e-d317-435c-9d28-286c80d944d4_2048x1176.png)
*来源：SemiAnalysis Tokenomics Model*

独立开发者曾因 OpenAI 相对 Anthropic 慷慨的订阅上限而对其称道，但如今这一说法已完全不成立。任何 Claude 订阅上的 Opus 5.5，其价值都远超 OpenAI 的任何产品。

为 OpenAI 辩护的唯一理由是，其 Pro 计划均无 5 小时上限，这让你更容易消耗掉每月总上限中更高的百分比。但我们不认为这足以抵消 Claude 计划上 Opus 5.5 约 4 倍的 API 等价价值优势。

## 实验室会随 API 定价调整而调整订阅上限吗？

近期我们观察到 Anthropic 与 OpenAI 模型的多轮显著降价。

- [Fable 5.1](https://x.com/claudeai/status/2094848588190830982) 相对 Fable 5 将缓存读取降价 75%
- [Opus 5.5](https://x.com/ClaudeDevs/status/2103548467729887677) 相对 Opus 5 将输入与输出 token 定价下调 20%，缓存读取下调 60%。
- [GPT 6.1](https://x.com/OpenAIDevs/status/2104993053002043870) Sol 相对 GPT 6 Sol 将缓存读取下调 50%。而在此之前，[GPT 6 Sol](https://x.com/OpenAIDevs/status/2102461432684282061) 已相对 5.6 Sol 便宜了 60–67%。

一个重要问题是：实验室是否会在这些降价之后同步调整 token 上限，从而让你的订阅 API 等价价值保持恒定。

前文已经展示过，OpenAI 在发布 6.1 Sol 时并未调整 $200/月计划上的 Sol token 上限，导致 API 等价价值下降约 30%。

Anthropic 在发布 5.1 时也完全没有上调 Fable 的 token 上限，但在 5.5 降价时确实上调了 Opus 的 token 上限。

![](https://substack-post-media.s3.amazonaws.com/public/images/60858e51-902d-421f-808d-34bc93b4b37a_2048x1113.png)
*来源：SemiAnalysis Tokenomics Model*

不过，Max 计划约 20%、Pro 计划约 50% 的 token 上调，仍不足以完全抵消 API 降价的影响。

## 提升订阅利润率的两种不同路径

正如本文开头所解释的，订阅的毛利率远低于 API，并显著拉低 OpenAI 与 Anthropic 的每 MW 营收。两家公司都清楚这一点，却选择了两种不同的策略来削减对订阅用户的补贴。

对同一计划，Anthropic 会随模型更高端而压低其 API 等价价值。从 Sonnet 5.5 到 Opus 5.5 的降幅不大，但到 Fable 5.1 就非常可观了。

![](https://substack-post-media.s3.amazonaws.com/public/images/8fc90004-5853-4cd5-87ff-465898c5ee6b_2048x1033.png)
*来源：SemiAnalysis Tokenomics Model*

在以更高官方定价发布更强模型的同时压低其 API 等价价值，是停止补贴订阅的更含蓄做法。假设 100% 利用率和 92% 的 API 毛利率，把用量跑满 Opus 5.5 与 Fable 5.1 分别对应 -369% 和 1% 的毛利率。若采用更现实的 20% 平均利用率，毛利率则分别升至 6% 和 80%。

换言之，**如果人人只用 Fable，Anthropic 的订阅计划恐怕早已拥有软件般的利润率**。随着 Anthropic 摸索出如何把模型做小，Opus 档模型的服务成本会随时间持续下降；而在 Fable 之上的新模型档位，订阅上限还会更低（假设它们根本被纳入订阅的话）。

而 OpenAI 选择了核弹级选项：一刀切、立即把所有档位砍到 Fable 水平的上限。

![](https://substack-post-media.s3.amazonaws.com/public/images/e674e5f4-cf61-425a-8db7-90395d9ade21_2048x1036.png)
*来源：SemiAnalysis Tokenomics Model*

这种做法本应招致公众反弹，但 OpenAI 不知怎的几乎完全避开了。原因可能是 DevDay 的满屏好评淹没了前一天负面新闻，加上对存量计划额外保留一个月的祖父条款（grandfathering）。

# 中国的订阅计划仍是好交易

尽管算力紧张，中国的实验室仍然提供有补贴的订阅计划，只是补贴力度因模型而异、差距悬殊。

![](https://substack-post-media.s3.amazonaws.com/public/images/c5c0445c-0292-4c32-9980-17c4d4fa175b_2048x1116.png)
*来源：SemiAnalysis Tokenomics Model*

按单位美元归一化后，它们与 OpenAI、Anthropic 的对比如下。

![](https://substack-post-media.s3.amazonaws.com/public/images/dffbac4f-e3c2-4ffb-909d-5662634c3d19_4332x2502.png)
*来源：SemiAnalysis Tokenomics Model*

在中国实验室这里，越买高档订阅，单位美元价值越高。平均而言，其单位美元 API 等价价值略低于 OpenAI 的约 12 倍。

# 第三方计划逊于第一方

我们要考察的最后一组对比，是 OpenAI 与 Anthropic 模型在自家第一方计划与 Cursor、Cognition（Devin）等第三方套壳之间的比较。
