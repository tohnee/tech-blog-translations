---
title: "Dell 是如何打败 Supermicro 的"
title_en: "How Dell Is Beating Supermicro"
subtitle: "企业市场、主权 AI、CoreWeave、Tesla、x.AI、AI 新兴 GPU 云的经济学与订单"
date: 2024-05-30
source: https://newsletter.semianalysis.com/p/how-dell-is-beating-supermicro
crawled: 2026-09-15
authors: ["Dylan Patel", "Daniel Nishball", "Caleb Goh"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# Dell 是如何打败 Supermicro 的

> 原文：[How Dell Is Beating Supermicro](https://newsletter.semianalysis.com/p/how-dell-is-beating-supermicro) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**企业市场、主权 AI、CoreWeave、Tesla、x.AI、AI 新兴 GPU 云的经济学与订单**

在 Nvidia 的 GTC 2024 上，Jensen 亲自走到 Dell 的展台，一遍又一遍地高喊「Dell」。Jensen 甚至在主题演讲中把台下的 Michael Dell 点名请上台。Nvidia 显然对 Dell 作为 AI 服务器公司的前景兴奋不已，但这是为什么？

Dell 进入 AI 服务器市场极晚。在上一代 A100 时期，他们只提供了面向规模小得多的 HPC 市场的低量、低端 4xA100 服务器（Redstone）。而且在 HPC 领域，Dell 在[公开披露的系统](https://www.top500.org/statistics/list/)中只占 7% 的市场份额，而其主要竞争对手 Lenovo 和 HPE 分别占 32.6% 和 22.4%。Dell 甚至没有推出 8xA100 HGX 服务器（Delta）——那可是所有做 AI 的公司都在用的机型。这包括 OpenAI 这样的公司，他们正是[用 8xA100 Delta 训练并推理 GPT-3.5 和 GPT-4](https://www.semianalysis.com/p/gpt-4-architecture-infrastructure)。

![](https://substack-post-media.s3.amazonaws.com/public/images/c7e8ccaf-d891-4b77-b044-3ed0ff28b187_1775x881.png)
*来源：Nvidia，SemiAnalysis*

Dell 在 8xH100 HGX 服务器的设计和出货上同样迟到。这一切导致 Dell 一度是 Nvidia 优先级最低的合作伙伴；但如今，沉睡的巨人 Dell 终于醒了，而且可以说已成为 Nvidia 优先级最高的 OEM。

Nvidia 服务器市场大体可以分为 OEM（Dell、Supermicro、HPE、Lenovo 等）和 ODM（Quanta、FII、Inventec、Wistron、Wiywynn、ZT Systems 等）。超大规模云厂商倾向于从 ODM 采购，ODM 组装服务器的毛利率约 ~2% 到 ~3%。超大规模厂商这样做是因为相对于其他公司，它们所需的服务的档次要低得多。

另一方面，市场上还有一批重要买家——[企业客户](https://www.semianalysis.com/p/accelerator-model)、[主权 AI 玩家](https://www.semianalysis.com/p/accelerator-model)，以及[超过 15 家 AI 新兴 GPU 云（Neocloud）](https://www.semianalysis.com/p/gpu-cloud-economics-explained-the)——它们需要 OEM。基本上，整个去年和今年大部分时间里，Supermicro 都是这些买家当中许多家的唯一货源。

**这一切已经改变。**

在非超大规模客户这一群体中，Dell 正在[许多其他新兴 GPU 云、企业和主权 AI 项目中抢占份额](https://www.semianalysis.com/p/accelerator-model)。Dell 尤其拿下了 CoreWeave、Tesla 和 x.ai 的订单，而这三家[是走 OEM 供应链而非 ODM 直采的最大的三家 GPU 买家](https://www.semianalysis.com/p/accelerator-model)。

人云亦云的流行说法是：Dell 不过是靠 Nvidia 的产能配给吃到了偏饭……毕竟，谁控制了~~香料，谁就控制了宇宙~~ Nvidia GPU 配给，谁就能把它们卖出去，不是吗？这种思路是不对的。如果你想要 GPU 服务器，你现在就可以从 Dell 或 Supermicro 下单，第三季度就能到货。交期正在压缩。产能配给和 GPU 供应链的紧张并不是 Dell 份额提升的原因。

首选 OEM 合作伙伴易主的真正原因要有趣得多。我们将在下文解释 Dell 是如何打败 Supermicro 的、GPU 新兴云的经济学，以及这些新兴云继续增长和投资的能力。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
