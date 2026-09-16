---
title: "Gemini 完蛋了，但 GCP 正火力全开"
title_en: "Gemini is Cooked but GCP is Cooking"
subtitle: "GCP 营收同比增长 >100%，DeepMind 的长期失败是 Google Cloud 的短期收益"
date: 2026-08-07
source: https://newsletter.semianalysis.com/p/gemini-is-cooked-but-gcp-is-cooking
crawled: 2026-09-15
authors: ["Max Kan", "Joey Brookhart", "Doug O'Laughlin", "Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Gemini 完蛋了，但 GCP 正火力全开

> 原文：[Gemini is Cooked but GCP is Cooking](https://newsletter.semianalysis.com/p/gemini-is-cooked-but-gcp-is-cooking) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**GCP 营收同比增长 >100%，DeepMind 的长期失败是 Google Cloud 的短期收益**

8 月 5 日星期三，Google [宣布](https://blog.google/company-news/inside-google/message-ceo/next-chapter-ai-momentum/)对 DeepMind 领导层进行彻底改组。简要回顾：

- DeepMind 联合创始人、前 CEO Demis Hassabis 不再参与日常运营。
- 前 Google 首席科学家、Gemini 联合负责人 Jeff Dean 离职，创办一家名为 Discovery Loop 的新实验室（neolab）。Jeff 是 Google 工程界无可争议的 GOAT（史上最佳），联合创立了 Google Brain，并开启了 TPU 项目。
- 与 Jeff 同行的还有 Sanjay Ghemawat、Quoc Le 和 Oriol Vinyals。Sanjay 和 Quoc 都是 Google Fellow——这一头衔只授予公司最顶尖的十多位技术贡献者。[1](#footnote-1) Oriol 是 Gemini 联合负责人之一。
- 前 DeepMind CTO、硕果仅存的另一位 Gemini 联合负责人 Koray Kavukcuoglu 接替 Demis 执掌 DeepMind/Gemini。

显然，这些不是一群对 Gemini 4 Pro 感到兴奋的人会有的动作。

从一切实际意义上讲，我们认为 **DeepMind 已不再是前沿实验室**。几个月前我们就因强化学习团队大量出走和算力配置糟糕，向 [Tokenomics](https://semianalysis.com/tokenomics-model/) 客户表达过这一判断。Google 还会继续跌跌撞撞地发布模型，但他们重新达到 SOTA 的概率已降为零。

此外，今天这个消息的**最大受益者**既不是 Anthropic 也不是 OpenAI——而是 **Google Cloud**。过去 Gemini 和 GCP 曾拼命争抢算力配额，现在胜负已定：Thomas Kurian 赢了。**因此我们预计 GCP 营收增长将显著加速**。

## Gemini 3 Pro 就是巅峰

2025 年底，Anthropic、OpenAI 和 Google 是毋庸置疑的 AI 三巨头。直到上周仍有人持这种看法，但对用心观察的人来说，Gemini 在 2026 年的陨落早已清晰可见。以下摘自我们 **7 月 9 日**向 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)订阅客户发布的[机构报告](https://semianalysis.com/institutional/googles-fall-from-grace-why-gemini-3-pro-was-the-top-plus-some-thoughts-on-openai-msl-and-spacexai/)：

> - 2025 年 11 月，Gemini 3 Pro 可以说是世界上最好的模型，迫使 Sam Altman 在 OpenAI 发布「红色警报（code red）」。
> - 自那以后，DeepMind 与 OpenAI/Anthropic 之间的差距急剧拉大。Gemini 3.5 Flash 彻底失败，**业内风声显示即将发布的 Gemini 3.5 Pro 大约只有 Opus 4.5 的水平**。这真真不如 GLM 5.2，更遑论 Fable 5 和 GPT 5.6。
> - 我们相信 Gemini 的处境只会更糟，因为 Google 缺乏构建 RSI 所需的宗教般信仰。我们认为 MSL 和 SpaceXAI 很可能在今年年底前在模型质量上双双超越他们。
> - 与 Noam Shazeer 和 John Jumper 一样，Gemini 大多数最优秀的 RL 人才最近都离开了公司。
> - OpenAI 已经解决了预训练问题，一个代号「Doug」的大得多的模型正在紧锣密鼓地开发中。

倒数第二条值得强调。Jeff、Sanjay、Quoc 和 Oriol 只是 DeepMind 一长串高调离职中最新的一批。尽管当前 LLM 范式背后的大部分基础性突破都是 Google 发现的，如今的 Google 却根本留不住顶级 AI 人才。

值得注意的是，Jeff 及其同伴创建新实验室 Discovery Loop 所沿用的打法，是 Ineffable Intelligence 的 David Silver 去年 11 月开创的。为了追求自己的使命，顶级 AI 研究者如今选择离开 Google，从外部投资者和 Google Ventures 那里融资数十亿美元，然后把这些钱花在 GCP 里的 Nvidia GPU 上。

自我们的[机构报告](https://semianalysis.com/tokenomics-model/)以来，Google 已悄悄取消了 Gemini 3.5 Pro，转而靠炒作 Gemini 4 来[自我安慰](https://x.com/OfficialLoganK/status/2079594867161022817?s=20)。作为过渡模型，他们发布了 Gemini 3.6 Flash，但总体上不如 Muse Spark 1.2、Grok 4.5 和中国一线开源模型。视统计口径而定，Gemini 目前排在第 8 或第 9 位，我们看不出 Gemini 4 能扭转他们的颓势。

![](https://substack-post-media.s3.amazonaws.com/public/images/4c11127d-75d3-4b40-8ffa-8edbaab508b3_1976x1108.png)
*来源：Artificial Analysis*

与此同时，Gemini 第一方 API 的 token 增速明显放缓已是人尽皆知。[1Q26](https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q1-2026/) 他们增长 60%，从每分钟 10B token 升至 16B；[2Q26](https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q2-2026/) 仅增长 38%，至 22B。这导致 Gemini 1P API 收入增速相应下滑。

![](https://substack-post-media.s3.amazonaws.com/public/images/eaf8ff61-9043-4226-b3e3-f296d8dd1b88_1955x918.png)
*来源：SemiAnalysis Tokenomics Model*

不过，**Gemini Enterprise Agent Platform（前身为 Vertex）整体表现明显更强**，这要归功于 Claude 等第三方模型。如需 Amazon Bedrock、Microsoft Foundry 和 Google Vertex 按模型提供商拆分的完整收入数据，以及对 OpenAI 和 Anthropic 的所有影响分析，请参阅我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)。

### **信仰无可替代**

我们认为 Gemini 的核心问题始终是根本性的信仰缺失。算力是 AI 进步的命脉，所有「AGI 信仰入脑」的实验室都在不顾一切地尽可能多抢算力。

当然，预付多个 GW 的费用也非常吓人、非常昂贵，尤其是当你没有一门快速增长的高毛利 API 生意时。不过，正如我们在[此前](https://newsletter.semianalysis.com/p/the-future-of-meta-superintelligence)[通讯](https://newsletter.semianalysis.com/p/meta-compute-everyone-wants-to-be)中所解释的，有创造性的办法可以克服这一限制，以非常诱人的费率把富余产能变现，**同时保留把一切收回给自己的研究团队的选择权**。明确地说，这正是我们在 Meta 和 SpaceX 身上看到的。

Google 则不然：他们认定，把海量算力以长期合同卖给 Gemini 最凶猛的竞争对手、且不指望这些算力还能回到 DeepMind 手里，是完全值得的。

3Q26 到 4Q27 的 TPU 总出货量中，超过 20% 将直接卖给 Anthropic。[2](#footnote-2) 这还不包括 GCP 目前已出租给 Anthropic 的数十万颗 TPU，以及未来 6 个季度已承诺出租给 Anthropic 和 Meta 的更多数十万颗。

![](https://substack-post-media.s3.amazonaws.com/public/images/f2873391-8508-4334-bd3e-5964ff75a1cd_2075x1013.png)
*来源：SemiAnalysis Accelerator Model*

关于到 2030 年每季度生产的 TPU、GPU、Trainium 等的数量及其终端客户的完整细节，请参阅我们的[加速器模型](https://semianalysis.com/accelerator-hbm-model/)。

只要你听过 Google Cloud CEO Thomas Kurian 的任何一次访谈，就知道他不是 AGI 信徒。比如在一期[播客](https://www.youtube.com/watch?v=bNdiBwXbLNw)中，他主张 TPU 成为支撑 Citadel、美国能源部和通用高性能计算等客户的「通用目的基础设施」是件好事。当被问到为什么在 Anthropic 与 Gemini 竞争的情况下还向其出售算力时，他说这是 Google 作为一家「平台公司」的自然结果。

而正是这个人，很可能刚刚赢下了一场重大的内部政治斗争，将获得对 Google 算力配额更大的控制权。

### **试着为 DeepMind 的前沿雄心做最强辩护**

到目前为止我们对 DeepMind 显然相当看空。如果非要为「他们未来仍能训练出真正的 SOTA 模型」给出最强论证（steelman），大概会是这样：

- 现有班子显然行不通。在原领导团队下，他们追上 Anthropic/OpenAI 的希望极其渺茫。
- 如今大扫除已完成，新人可以从一张白纸开始。说不定他们还会收购式招揽（acqui-hire）一家像 SSI 或 Thinking Machines 这样的新实验室。
- 有了这支新团队，他们追上前沿的概率实际上反而上升了。

也许存在某种平行世界能让这一切发生，但我们认为概率基本为零。Google 的问题不在 Jeff Dean，也不在 Noam Shazeer，而在于其极度官僚、慢得令人痛苦、战略上畏首畏尾的文化。[别忘了](https://x.com/thsottiaux/status/2083596911060324570)，DeepMind 比 ChatGPT 早一年就有了 AI 聊天机器人，却因担心颠覆自家核心业务而未获准发布。

![](https://substack-post-media.s3.amazonaws.com/public/images/03c20d1a-8bcf-4861-a8dc-0a96d2963392_1041x745.png)
*来源：Tibo（来自 X）*

有趣的是，Tibo 本人正是 Google 人才流失的又一个绝佳例子。这位 9 年资历的 Google/DeepMind 老兵于 2024 年 7 月离职加入 OpenAI，联合领导了最初的编程智能体团队，如今执掌 Codex。反观 Google，2025 年 7 月「收购」Windsurf 来打造自己的智能体编程平台，到目前为止算不上顺风顺水。

也别忘了，DeepMind 本身就是最早的那场 AI 收购式招揽！有了 12 年的后见之明，我们已经知道那一切如何收场。再往名单里添一家新实验室，多半只会重蹈覆辙。

## GCP 的金融化

我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)估算，Gemini ARR 在 2Q26 为 $12B。相比之下，到 2027 年底，GCP 的第三方 AI ARR（IaaS/TaaS）将超过 $73B，外加 $120B 的 TPU 销售额。**以 30% 多（high 30s）EBIT 利润率实现的 $200B 对外销售，对比今天只有 $12B 的第一方业务，重心在哪一目了然。** Google 管理层态度明确：让 GCP 走金融化路线的短期收益，值得为此放弃任何前沿领域的长期竞争力。

![](https://substack-post-media.s3.amazonaws.com/public/images/d1799850-cdf8-4545-9eb8-a1641666892f_2187x1094.png)
*来源：SemiAnalysis Tokenomics Model*

尽管 Gemini 不济，GCP 仍在继续加速。上季度 GCP 增长 82%。但这并非全部来自我们传统意义上的「云」业务。GCP 有了一个新收入来源：把整套 TPU 系统卖给为 Anthropic 等客户运营数据中心的外部 SPV（特殊目的实体）。**这些 TPU 销售按总额法入账，约 $35B/GW**。2Q26 我们估算 TPU 销售约 $1.2B，即核心 GCP 增速在 70% 出头。鉴于 TPU 系统在手订单超过 $150B，**这些 TPU 系统销售将把 GCP 2027 年增速推到 100% 出头（mid 100s），而卖方一致预期只有 64%**。

![](https://substack-post-media.s3.amazonaws.com/public/images/1cc76e1d-e524-4ba4-9744-c1d64400edd6_1987x980.png)
*来源：SemiAnalysis Tokenomics Model*

虽然这些系统销售的 EBIT 利润率略低于核心云业务 30% 出头（low 30%）的水平，我们仍预计 GCP 整体未来能实现 30% 中到高（mid to high 30s）的 EBIT 利润率。投资者将如何对当前 TPU 在手订单及未来任何大额销售进行资本化，仍是一个开放问题。不过，鉴于各实验室旺盛的算力需求，我们预计很快会有更多多 GW 级交易公布并充实这一在手订单。总而言之，**我们估计未来几个季度可能有超过 $250B 的额外 TPU 订单（Bookings）计入 GCP 的 RPO（剩余履约义务）**。在那之前，GCP 增长如此抢眼的加速叠加良好的利润率，**将在 2027 年为 Google EPS 贡献约 $3**。

关于 Amazon、Microsoft 和 Oracle 云业务更细致的拆解，以及财报季更新的 Google 预测，请参阅我们的 [Tokenomics 模型](https://semianalysis.com/tokenomics-model/)。

## 许愿须谨慎
