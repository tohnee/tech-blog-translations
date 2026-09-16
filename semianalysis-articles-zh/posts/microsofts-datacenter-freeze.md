---
title: "微软数据中心冻结：1.5GW 自建放缓与租约取消的误读"
title_en: "Microsoft's Datacenter Freeze - 1.5GW Self-Build Slowdown & Lease Cancellation Misconceptions"
subtitle: "OpenAI 转向、Oracle 与 Stargate 加速、超大规模云厂商资本开支影响、Vertiv 所受影响被误读、Copilot 采用疲软"
date: 2025-04-28
source: https://newsletter.semianalysis.com/p/microsofts-datacenter-freeze
crawled: 2026-09-15
authors: ["Dylan Patel", "Jeremie Eliahou Ontiveros", "Maya Barkin"]
tags: ["Hyperscalar", "Datacenter", "AI Infrastructure"]
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 微软数据中心冻结：1.5GW 自建放缓与租约取消的误读

> 原文：[Microsoft's Datacenter Freeze - 1.5GW Self-Build Slowdown & Lease Cancellation Misconceptions](https://newsletter.semianalysis.com/p/microsofts-datacenter-freeze) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**OpenAI 转向、Oracle 与 Stargate 加速、超大规模云厂商资本开支影响、Vertiv 所受影响被误读、Copilot 采用疲软**

过去几个月，出现了不少围绕微软缩减数据中心租赁活动（包括几起数据中心租约取消）的报道，引发市场担忧。我们早在 12 月 17 日就向我们的[数据中心模型](https://semianalysis.com/datacenter-industry-model/)订阅客户提示了微软退出多份数据中心租赁合同（比华尔街的头条新闻早了两个月）。这件事并不像表面看起来那么简单，微软的行动背后还有大量细节。

市场一直在聚焦「取消 2GW 租约」，但这**只涉及不具约束力的意向书（LOI），并非正式合同**。这种说法没有提到，微软手里还有**约 5GW 已签订约束性合同的预租容量，将在 2025 年至 2028 年间陆续投入运营**。**实际上，过去两个季度微软放弃的不具约束力的合同远超 2GW**。2024 年年中，微软几乎与每一家供应商都在洽谈容量，此后则完全冻结了新的租赁活动。

下面的图表是一个绝佳例证。2023 年和 2024 年上半年，微软几乎凭一己之力撑起了租赁市场。它不仅在激进签约，还通过全面锁定不具约束力的 LOI，事实上「冻结」了整个市场。**我们估计，从 2023 年第一季度到 2024 年第二季度，微软占到了全部新增租赁交钥匙（turnkey）容量的 60% 以上**。2024 年 6 月，微软的预租容量超过了其他四大超大规模云厂商的**总和**。

![柱状图：微软、Meta、Google、Amazon、Oracle 等公司多个季度的数据中心预租容量（兆瓦）估算。](https://semianalysis.com/datacenter-industry-model/)
*来源：SemiAnalysis 数据中心模型*

与此同时，**微软大幅加码自建：在美国本土和全球范围内收购了数万英亩土地，加快现有站点建设，并为未来站点锁定了数吉瓦（GW）的电力**。综合来看，这些动作表明[微软正在为史上最雄心勃勃的基础设施建设做准备](https://semianalysis.com/2023/11/15/microsoft-infrastructure-ai-and-cpu/)。

虽然租赁放缓本身不容小觑，但这些变化对短期和中期并不构成实质性影响，只会作用于 2027 年及以后。更重要的，是微软自建数据中心计划调整所带来的放缓。**我们的研究表明，微软正在冻结 1.5GW 的近期自建数据中心项目——这些项目原本计划于 2025 年和 2026 年上线**。

微软正在全球范围内冻结多个（但并非全部）自建项目，对 2025 年和 2026 年容量的影响立竿见影——[我们此前已向数据中心模型订阅客户做过提示](https://semianalysis.com/datacenter-industry-model/)。多个数百兆瓦级的微软园区进展乏善可陈，尽管我们的研究表明这些项目已锁定能源并取得所有必要审批。**这是微软有意为之，目的是放缓自建容量的扩张。**

下面的照片展示了微软多个美国数据中心项目的停滞状况——类似的例子还有很多。场地基础工程略有推进，但微软已冻结主体建筑（楼体外壳）的施工，并推迟或取消了[冷却](https://semianalysis.com/2025/02/13/datacenter-anatomy-part-2-cooling-systems/)和[电气](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/)设备订单。进度明显慢于该公司 2023 年和 2024 年开发自建园区的速度。下文我们将解读微软这一战略转变的来龙去脉。

市场误解了微软的容量增长，其对 Vertiv 等设备供应商的影响与分析师的说法大相径庭。这种业余级别的混淆，导致一位华尔街分析师在 Vertiv 2025 年第一季度（Q1 25）财报发布前预测其订单将明显走弱。

他们没有理解的一点是：微软约 5GW 预租容量中的很大一部分尚未进入 Vertiv 的订单簿。而这只是众多重大误读之一——我们会在本报告末尾解释对 Vertiv 的真实影响。

是什么导致了微软的战略转变？对 Vertiv 这类数据中心设备供应商，以及更广泛的 GPU 和 AI 基础设施市场，又会有什么后果？尽管存在 1.5GW 的自建暂停和全部新租赁活动的冻结，实际影响并不像看上去那么悲观。我们将在下文一一拆解。

## 微软的租赁与自建狂热
