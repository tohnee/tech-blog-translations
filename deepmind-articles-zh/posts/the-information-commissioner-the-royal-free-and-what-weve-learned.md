---
title: "信息专员、皇家自由医院，以及我们的所学"
title_en: "The Information Commissioner, the Royal Free, and what we've learned"
source: https://deepmind.google/blog/the-information-commissioner-the-royal-free-and-what-weve-learned/
site: deepmind
date: 2017-07-03
crawled: 2026-09-13
translated: 2026-09-13
---

# 信息专员、皇家自由医院，以及我们的所学

> 原文：[The Information Commissioner, the Royal Free, and what we've learned](https://deepmind.google/blog/the-information-commissioner-the-royal-free-and-what-weve-learned/) · Google DeepMind

今天，英国各家医院将[有数十人本可避免地死于](http://qualitysafety.bmj.com/content/early/2012/07/06/bmjqs-2012-001159)脓毒症和急性肾损伤（AKI）等疾病，只因他们的预警信号没有被及时发现和处理。为帮助解决这一问题，我们与伦敦皇家自由 NHS 基金会信托的临床医生共同开发了 [Streams](https://deepmind.com/about/health) 应用，利用移动技术自动审查化验结果，从急性肾损伤开始筛查严重问题。一旦发现问题，Streams 就会向相应的临床医生发送安全的智能手机警报，并附上此前的病史信息，使其能够立即做出诊断。

让我们感到自豪的是，Streams 在皇家自由医院部署后的几周内，[护士们表示它每天能为她们节省多达两个小时](https://www.royalfree.nhs.uk/news-media/news/new-app-helping-to-improve-patient-care/)，我们也已经听到一些例子：得益于即时警报，[罹患重症的患者](https://www.standard.co.uk/news/health/new-mother-receives-pioneering-kidney-treatment-after-app-detects-lifethreatening-illness-a3476936.html)得到了更快的诊治。由于 Streams 的设计使其为未来更先进的技术（包括 AI 驱动的临床警报）做好了准备，我们希望它终将为患者和临床医生带来更多益处。

信息专员办公室（ICO）[现已结束](https://ico.org.uk/about-the-ico/news-and-events/news-and-blogs/2017/07/royal-free-google-deepmind-trial-failed-to-comply-with-data-protection-law/)一项为期一年的调查。该调查聚焦于皇家自由医院在 2015 年底及 2016 年对 Streams 进行的临床测试，其目的是保证这项服务能够在医院安全部署。ICO 认为这一将患者数据用于测试的做法缺乏充分的法律依据（国家数据守护者（National Data Guardian）[也表达了同样看法](https://www.theguardian.com/technology/2017/may/16/google-deepmind-16m-patient-record-deal-inappropriate-data-guardian-royal-free)），并对患者对相关情况知情的程度提出了关切。ICO 承认，其中许多问题已经由皇家自由医院解决，并要求该信托签署一份正式承诺书，以确保今后的合规。

ICO 的承诺书也确认，皇家自由医院始终保有对所有患者数据的控制权，DeepMind 一贯只扮演「数据处理者」（data processor）的角色，并依照该信托的指令行事。数据的安全或保密性方面未发现任何问题。

我们欢迎 ICO 对此案深思熟虑的裁决，希望它能保障 Streams 在今后对患者数据安全、合法的处理。

虽然今天的结论针对的是皇家自由医院，我们也需要反思自己的行为。当这项工作于 2015 年启动时，我们一心追求快速见效，低估了 NHS 及患者数据相关规则的复杂性，也低估了人们对一家知名科技企业涉足医疗的潜在担忧。我们几乎只专注于构建护士和医生想要的工具，把自己的工作视为面向临床医生的技术，而不是一件需要向患者、公众和整个 NHS 负责、并由他们塑造的事情。我们在这方面做错了，我们需要做得更好。

自那以后，我们在透明度、监督和公众参与方面努力做出了一些重大改进。例如：

- 我们在 2015 年与皇家自由医院签署的最初法律协议，本可以在具体项目内容以及我们承诺遵守的患者信息处理规则方面写得详细得多。我们与皇家自由医院在 2016 年用一份全面得多的合同（可在[此页面](https://deepmind.com/about/health)查阅）取代了它，我们也与使用 Streams 的其他 NHS 信托签署了同样严格的协议。
- 我们犯了一个错误：没有在 2015 年工作刚启动时就公开它。此后，我们主动公布并公开了我们与 NHS 后续合作的合同。
- 在最初与护士和医生合作、开发满足临床需求的产品时，我们做得不够，没有让患者和公众充分了解我们的工作，也没有邀请他们质疑和塑造我们的优先事项。此后，我们与患者专家合作，制定了[患者与公众参与策略](https://deepmind.com/about/health)，并于 2016 年 9 月举办了我们的首场大型公开活动，未来还会有更多。
- 为了显著加强对我们工作的监督，早在任何监管或媒体批评出现之前，我们就邀请了[九位备受尊敬的独立评审员](https://deepmind.com/about/health)来审视 DeepMind Health。这一小组即将发布他们第一年的评审结果，我们期待着他们提出改进建议。

我们希望这些举措有助于整体提升 NHS 信息技术的水准，未来我们还想在[可验证数据审计（Verifiable Data Audit）](https://deepmind.com/blog/article/trust-confidence-verifiable-data-audit)等项目上走得更远。

归根结底，如果我们想构建技术来支持 NHS 这样重要的社会机构，就必须确保我们服务于社会的优先事项，而不是跑在它们前面。在寻找令人兴奋的新方法来改善医疗，与超越患者预期之间，只有一线之隔。我们知道，在医疗工作起步时我们在这一点上没有做好，我们会继续倾听和学习，以求改进。我们也完全认同[国家数据守护者](https://www.gov.uk/government/news/national-data-guardian-emphasises-need-for-a-public-conversation)和 [Understanding Patient Data](https://understandingpatientdata.org.uk/) 等备受尊敬的声音：它们呼吁就利用数据改善医疗保健展开更多的公共讨论，我们将尽己所能支持这一进程。

我们是一支在 NHS 环境中长大、并在其中工作过的团队，因一个珍贵的机遇走到一起——把我们的专业能力用于帮助患者、护士、医生，以及我们深爱的医疗服务。这是一个绝佳的机会，让我们证明自己一直以来的信念：只要我们把伦理、问责和公众参与做对，新技术系统就能产生难以置信的积极社会影响。这是我们所能想象的最重要挑战。
