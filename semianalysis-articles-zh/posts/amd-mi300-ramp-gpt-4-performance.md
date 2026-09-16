---
title: "AMD MI300 爬坡、GPT-4 性能、ASP 与出货量"
title_en: "AMD MI300 Ramp, GPT-4 Performance, ASP & Volumes"
subtitle: "来自 Microsoft、Meta、Oracle、Google、Supermicro/Quanta 直销、Amazon 的订单量"
date: 2023-11-01
source: https://newsletter.semianalysis.com/p/amd-mi300-ramp-gpt-4-performance
crawled: 2026-09-15
authors: ["Dylan Patel", "Myron Xie"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# AMD MI300 爬坡、GPT-4 性能、ASP 与出货量

> 原文：[AMD MI300 Ramp, GPT-4 Performance, ASP & Volumes](https://newsletter.semianalysis.com/p/amd-mi300-ramp-gpt-4-performance) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**来自 Microsoft、Meta、Oracle、Google、Supermicro/Quanta 直销、Amazon 的订单量**

AMD 即将推出的 MI300 有望成为 LLM 推理领域唯一能对 NVIDIA 和 Google 硬件构成实质威胁的竞争者。Groq、SambaNova、Intel、Amazon、Microsoft Athena 等目前都还构不成竞争。为此，AMD 一直在大力投资其自有的 ROCm 软件、PyTorch 生态以及 OpenAI 的 Triton。

在上文中（今年 1 月），我们讨论了软件层面的问题及其解决进展，以及 MI300 的主要客户、优势与用例（LLM 推理）。这一判断已开始兑现：[Databricks](https://www.databricks.com/blog/training-llms-scale-amd-mi250-gpus)、[AI21](https://blog.allenai.org/announcing-ai2-olmo-an-open-language-model-made-by-scientists-for-scientists-ab761e4e9b76)、[Lamini](https://www.lamini.ai/blog/lamini-amd-paving-the-road-to-gpu-rich-enterprise-llms)、[Moreh 和韩国电信（KT）](https://moreh.io/blog/training-221b-parameter-korean-llm-on-1200-amd-mi250-gpu-cluster-230814)等公司已在使用 AMD GPU 做推理/训练。

我们在 6 月详细解析过 MI300 的架构，重申了上述观点，并更深入地探讨了成本、网络和各种配置。今天我们还想谈一谈 MI300 的 GPT-4 性能。

Microsoft、Meta、Oracle、Google、Supermicro/Quanta 直销、Amazon 等公司已对 MI300 下了数量不等的订单。我们将在下文详述出货量、毛利率和平均价格，但先来看看 AMD 官方的说法。

> 基于我们在 AI 路线图执行上的快速进展以及云客户的采购承诺，我们目前预计第四季度数据中心 GPU 营收约为 4 亿美元，并随着全年出货的爬坡，2024 年将超过 20 亿美元。这一增长将使 MI300 成为 AMD 历史上最快达成 10 亿美元销售额的产品。我期待在 12 月的 AI 活动上分享更多进展细节。
>
> Lisa Su，AMD CEO

注意，她在这里其实对 MI300 有所保留，只说了超过 20 亿美元。我们将在下文分享我们的数字。值得一提的是，由于 AMD MI300 供应链环节繁多，数据透明度极高——从台积电开始投片算起，AMD 大约需要 7 个月才能真正出货一块 MI300X 8 GPU 基板。

撇开 AMD 当前在 LLM 训练和推理市场不足 0.1% 的份额不谈，AMD 在数据中心市场的份额正持续稳步增长。随着明年年中 Turin 和 Turin-Dense 的发布，这一势头将持续到明年。

要推算 AMD 明年来自 MI300 的营收，有两个切入角度：一是 AMD 能锁定多少供应，二是主要客户会下多少订单。

在供应端，我们的 AI 加速器模型会按存储厂商拆分 HBM 出货量、CoWoS 产能、封装良率等，覆盖每一款采用 CoWoS 生产的加速器，包括 NVIDIA、AMD、Google/Broadcom、Meta/Broadcom、Intel/AlChip、Amazon/AlChip、Amazon/Marvell、Microsoft/GUC 等的产品。

我们定期为客户更新这一模型，它给出了 AMD 每季度可出货的总颗数。注意，台积电 N5/N6 晶圆生产、SoIC 重组晶圆生产、CoWoS 晶圆生产、GPU 封装出货、测试和 8-GPU 基板生产都存在时间滞后。为了实现我们下文将讨论的出货量，订单其实在很久之前就已下达，尤其考虑到 HBM 和 CoWoS 的供应紧张。

另一面是客户。Microsoft、Meta、Oracle、Google、Supermicro/Quanta 直销和 Amazon 是订单的主要来源，但供应链其他环节也有一些订单，包括面向 HPC 类应用的 MI300A。把两面合在一起，我们得出的图景是：AMD 在第三季度之前处于供应受限状态，第四季度则转为供过于求。我们的需求端建模已计入 NVIDIA B100 提前上市的影响。

现在来看数字，包括出货量、毛利率和 ASP。我们还将简要讨论 MI350X 和 MI400。

[获取团体订阅 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
