---
title: "为什么 Streams 不使用 AI？"
title_en: "Why doesn't Streams use AI?"
source: https://deepmind.google/blog/why-doesnt-streams-use-ai/
site: deepmind
date: 2017-11-29
crawled: 2026-09-13
translated: 2026-09-13
---

# 为什么 Streams 不使用 AI？

> 原文：[Why doesn't Streams use AI?](https://deepmind.google/blog/why-doesnt-streams-use-ai/) · Google DeepMind

关于 Streams——我们的安全移动医疗应用——人们最常问我的一个问题就是：「DeepMind 为什么要做一个不用人工智能的东西？」

对一家人工智能（AI）公司来说，这是个合情合理的问题。当我们最初考虑进军医疗领域时，我们天然的着眼点就是 AI，以及它能如何帮助英国国家医疗服务体系（NHS）及其患者。我们认为，AI 在革新我们对疾病的认识——它们如何发生发展、如何被诊断——方面潜力巨大，而这反过来又可以帮助科学家发现新的疗法、照护路径和治愈方法。

在 DeepMind Health 的早期，我们与伦敦皇家自由医院（Royal Free Hospital）的临床医生会面，他们想知道 AI 能否改善有急性肾损伤（acute kidney injury，AKI）风险的患者的照护。AKI 众所周知难以发现，若不加治疗可能导致重病甚至死亡。

目前，AKI 的检测方式是把一个公式（称为 [AKI 算法](https://www.england.nhs.uk/akiprogramme/aki-algorithm/)）应用于 NHS 患者的血液检测。这个算法不错，但众所周知它并不完美。例如，它容易对患有慢性（而非急性）肾病的患者产生假阳性。它也不敏感于患者是入院两小时还是两周、患者是 8 岁还是 92 岁——而这些都会造成差异。

我们与皇家自由医院的合作伙伴一道，看到了技术可以提供帮助的许多方式，并对 AI 与非 AI 方法都抱有兴趣。

作为其中的一部分，我们于 2015 年向 NHS 健康研究管理局（Health Research Authority，HRA）提交了[一份初步伦理申请](https://www.hra.nhs.uk/planning-and-improving-research/application-summaries/research-summaries/using-machine-learning-to-improve-prediction-of-aki-deterioration/)，申请在皇家自由医院开展一项使用去个性化患者数据的潜在研究项目。该项目旨在结合经典统计学与 AI，开发出能够更准确地预测和识别 AKI 的更好算法。

但是，我们与皇家自由医院的临床医生相处的时间越久，就越清楚地看到：他们最紧迫的问题，并不能单靠用 AI 开发更好的算法来解决。他们明确告诉我们，他们的核心挑战在于如何实际落地一个算法，切实改变照护的提供方式。

我们曾多次谈及 NHS 当前的技术状况，以至于人们很容易忘记情况究竟有多糟糕。临床医生至今仍然普遍使用传呼机相互联系，而我在帝国理工学院（Imperial College London）开展的一项[研究](http://www.surgjournal.com/article/S0039-6060(14)00047-6/abstract)发现，这造成了沟通障碍，拖慢了对高危患者的治疗。想一想：如果发条消息不能靠短信，而要用座机呼叫某人，然后等对方回电才能传达信息，你一天的时间会少多少。想象一下每天被呼叫多达 25 次的情形。再想象一下，如果办公室里所有人不得不共用数量有限的电脑、你必须排队等待使用，你一天的时间又会少多少。

这就是医生和护士每天面对的现实，而与此同时，他们还要照护重症患者。

我们团队早期与皇家自由医院临床医生的这些会面，改变了我们对改善 AKI 等疾病照护最需要什么的看法。我们放弃了在皇家自由医院开展 AI 研究的想法，转而全力打造一个工具——Streams——以解决更紧迫的问题：以协调一致的方式快速响应特定的患者警报。

有了 Streams，医生和护士不必登录共用电脑，用手机就能看到做出照护与治疗决策所需的患者信息。它把化验结果和生命体征观测数据送到他们手心，并在患者病情恶化时以「突发新闻」式的警告发出提醒。它还让不同临床医生之间的沟通变得简单，使每个人随时掌握最新的信息。

![流程图，对比检测 AKI 的传统延迟式临床工作流（使用传呼机、电话和台式电脑登录）与使用 Streams 移动应用通知专科医生的加速直达工作流。](https://lh3.googleusercontent.com/v4ji9R48Allniw9hmgfpnviwhIyOq6XhFZS8DDIfHiSq82wyUT6PSGKDAUEq7MtYjpJ_FlVjFOpZtG3hQPamPsOnppMk8tVrcxiLCnxIGwVhQqY0xg=w1440)

通过更快、更简单地把现有的患者数据送到合适的护士或医生手中，Streams 让他们有更多时间专注于患者——而这一切尚未依赖 AI。

事实证明，构建 Streams 是一项巨大的工程；考虑到 2015 年我们团队规模有限，我们决定不再同步推进与皇家自由医院的 AI 研究。除了额外的工作量之外，它还要求我们把团队一分为二，以确保皇家自由医院的个人身份可识别数据（用于 Streams）与去标识化数据（用于研究）完全分开保管。所以我们没有继续推进 AI 研究，也没有签署为此所需的与皇家自由医院的附加协议。时至今日，我们从未与皇家自由医院开展过任何研究或 AI 开发。

这并不意味着我们已停止思考 AI 未来如何帮助临床医生。我们与其他合作伙伴推进了多个 AI 研究项目，并且一贯明确表示：我们希望未来在皇家自由医院使用的 Streams 能用上 AI。

但俗话说，千里之行始于足下。我们把 Streams 视为通往那个 AI 赋能未来的关键第一步。如果连一个能把临床信息送达护士和医生的应用都没有，AI 警报将毫无意义。你不能从纸笔记录的数据中生成 AI 建议，也无法通过传呼机或传真机发送详细的临床警报。

时机成熟时，我们希望与皇家自由医院开展研究，但只会在获得适当批准的前提下进行。目前，我们与他们的合作聚焦于 Streams 能为临床医生和患者解决的更迫切的问题。

你可以在[这里](https://health.google/)进一步了解 Streams 及其工作方式。
