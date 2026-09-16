---
title: "2023 数据中心展望——AMD 与 Intel 的营收、ASP 和出货量——Genoa 爬坡细节"
title_en: "2023 Datacenter Outlook – AMD and Intel Revenue, ASP, and Units – Genoa Ramp Details"
subtitle: "AMD 营收份额能到 35%？"
date: 2022-10-17
source: https://newsletter.semianalysis.com/p/2023-datacenter-outlook-amd-and-intel
crawled: 2026-09-15
authors: ["Dylan Patel"]
tags: []
audience: only_paid
paywalled: true
translated: 2026-09-15
---

# 2023 数据中心展望——AMD 与 Intel 的营收、ASP 和出货量——Genoa 爬坡细节

> 原文：[2023 Datacenter Outlook – AMD and Intel Revenue, ASP, and Units – Genoa Ramp Details](https://newsletter.semianalysis.com/p/2023-datacenter-outlook-amd-and-intel) · SemiAnalysis

> ⚠️ 付费订阅文章：以下为公开可见的预览部分翻译，正文在付费墙处截断，并非全文。

**AMD 营收份额能到 35%？**

编者按：市场状况此后显著走弱，2023 年服务器出货量看来将大幅下滑。我们认为 AMD 仍将夺取份额，但此前预测的出货量偏高。

AMD 已为其下一代基于 Zen 4 的 96 核 Genoa 服务器平台举办了预沟通会。虽然我们未能正式签署 NDA 出席，但业界围绕这条新产品线的讨论已经持续数月，包括本周我们正在参加的 OCP 峰会。其性能表现绝对惊人：在许多通用应用中，每路（socket）性能超过现有平台的 2 倍。

本报告将量化 2023 年现有服务器 CPU 产品线（如 Rome/Milan 和 Ice Lake SP）以及下一代 Genoa、Bergamo、Sienna 和 Sapphire Rapids 的出货量、平均售价（ASP）和营收。我们预计 2023 年服务器出货量将比 2022 年低 5.4%，比 2021 年低 5.1%。详细数据将在下文更深入地展开，但先给一个总括：到 2023 年 Q4，基于 DDR5 / PCIe 5.0 的 x86 服务器平台在总出货量中的爬坡渗透率仅约 18.2%。以出货量论，这是一个缓慢的爬坡。更重要的指标是内容量（content）：我们预计 2023 年 Q4 进入数据中心 CPU 的 bit 中约 34% 为 DDR5。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/d4eaaef7-0630-474f-a530-95185bdea130_1198x395.png)

自 2019 年底 Rome CPU 发布以来，AMD 在服务器市场的份额快速攀升。更重要的是，凭借更优的 TCO，其平均售价从低于 Intel 变为大幅高于 Intel。两年之内，AMD 的市场份额翻了一倍以上。往前看，我们预计 AMD 在 x86 服务器出货量中的份额将从 2022 年 Q2 的 13.9% 升至 2023 年 Q4 的 21.2%。由于平均售价（ASP）高企，AMD 的营收份额将远超这一数字。量化 AMD 未来 ASP 的提升，将比出货量增长更为重要。

感谢阅读 SemiAnalysis，如果你喜欢我们的内容，欢迎分享！

[分享](https://newsletter.semianalysis.com/p/2023-datacenter-outlook-amd-and-intel?utm_source=substack&utm_medium=email&utm_content=share&action=share)

卖方和买方的一致预期似乎认为 Genoa 和 Bergamo 只能将 ASP 提升 20% 到 30%，但很显然，他们没有和任何 ODM 或超大规模云厂商交流过。Genoa/Bergamo 相对 Milan/Rome 的代际目录价（list price）大幅上涨（目录价并不代表批量成交价）。反对 ASP 大幅上涨的论据通常是：我们正处于衰退中，AMD 不会有定价权。而现实是，Genoa 和 Bergamo 将催生至少自 Broadwell 和 Skylake 以来最广泛的数据中心基础设施换新周期。

一般来说，企业和甚至云厂商至今仍让许多 2015 年部署的 Intel Skylake SP 服务器继续服役。原因在于 Intel 和 DRAM 行业在改善单位性能总拥有成本（TCO）方面长期停滞，没有实质性的进步。Amazon、Microsoft 以及行业里的大多数公司都按 3 年对服务器计提折旧。2019 年，Amazon 开始调整云服务器的使用寿命，因为 Intel 2019 年的服务器基本上就是 Skylake SP 的回锅版。快进到今天，Amazon 和 Microsoft 已将服务器使用寿命一路调整到 6 年！

Genoa 标志着 TCO 的重大转折，让替换老旧服务器变得划算。与 2 路 Skylake/Cascade Lake SP 服务器相比，2 路（socket）Genoa 在通用性能上达到 4 倍，且 TCO 显著更优。基于 Genoa 的服务器初始资本开支要高得多，原因是 CPU、DDR5 和 PCIe 5.0 的成本更高。尽管资本开支有如此大的跳升，相比继续让已完成折旧的服务器服役，基于 Genoa 和 Bergamo 的服务器将收回数倍于投入的回报。

这些前期资本开支只占数据中心实际运营成本的极小一部分。超大规模云厂商的基础设施团队拥有复杂的 TCO 模型，涵盖各种非 CPU 成本，例如[占服务器资本开支 50% 的 DRAM](https://semianalysis.substack.com/p/cxl-enables-microsoft-azure-to-cut)、稼动率、功耗、散热成本、数据中心占地、机柜内服务器密度、网络、供电、资源冗余、平台工程成本以及授权软件。

超大规模云厂商的这些团队，其唯一职责就是维护这一模型，并为各种工作负载权衡不同的硬件选项。一个极度简化的 TCO 口诀——一位 Amazon 员工告诉我们他有时在路上会用——是：一台在役服务器的成本是其电力成本的 10 倍。

![](https://bucketeer-e05bbc84-baa3-437e-9518-adb32be77984.s3.amazonaws.com/public/images/71c1ae94-0a33-404e-8e4a-a8aff426222f_1690x497.png)

在这个高度简化的模型下，用 1 台 2 路 Genoa 服务器替换 4 台现有 2 路 Skylake/Cascade Lake 服务器（2 颗 CPU 对 8 颗 CPU），是一笔净现值为正的交易。资本开支的回本期约为 18 个月；而升级到 Rome/Milan 服务器的回本期仍要约 4 年。若再考虑安全性、CXL 和 AVX512 等新特性，改善幅度还会更加显著。

视具体用例而定，这些 TCO 和回本数字可能高得多也可能低得多，原因成百上千；但这里只是给出一个演示性的心智模型，用来反驳「Genoa/Bergamo 的 ASP 只比上一代高 20% 到 30%」的说法。另一个论据是：Genoa 用的先进制程硅片面积接近两倍，封装也更复杂，所以 AMD 理应收取更高的价格。

接下来是我们对基于 Zen 4 的服务器平台的季度增量爬坡预测，以及 Intel 和 AMD 在 2022 年 Q4 和 2023 年各季度的出货量、ASP 和营收。爬坡起步较慢，但到 2023 年 Q1 将加速至每季度 10 万颗的增量。随着 AMD 逐步收缩现有平台，并把更多后端基板供应从 Rome/Milan 转配给 Genoa/Bergamo/Siena，2023 年下半年将进一步提速。

[团体订阅享 8 折优惠](https://newsletter.semianalysis.com/subscribe?group=true&coupon=fe141654)
