---
title: "用 AI 让医生提前 48 小时发现危及生命的疾病"
title_en: "Using AI to give doctors a 48-hour head start on life-threatening illness"
source: https://deepmind.google/blog/using-ai-to-give-doctors-a-48-hour-head-start-on-life-threatening-illness/
site: deepmind
date: 2019-07-31
crawled: 2026-09-13
translated: 2026-09-13
---

# 用 AI 让医生提前 48 小时发现危及生命的疾病

> 原文：[Using AI to give doctors a 48-hour head start on life-threatening illness](https://deepmind.google/blog/using-ai-to-give-doctors-a-48-hour-head-start-on-life-threatening-illness/) · Google DeepMind

[我们最新发表于《自然》（Nature）的研究](https://nature.com/articles/s41586-019-1390-1)表明，人工智能现在可以在可避免的患者伤害的主要成因发生之前最多两天做出预测。与美国退伍军人事务部（VA）的专家合作，我们开发了一项技术，未来有望让医生在治疗急性肾损伤（AKI）方面获得 48 小时的先机——在英国，每年有超过 [10 万人](https://www.england.nhs.uk/akiprogramme/)受这一疾病影响。与这些发现一同发布的，还有一项对我们面向临床医生的移动助手 Streams 的同行评审服务评估，它表明数字工具的使用可以改善患者护理并降低医疗成本。两者共同构成了医学领域一项变革性进展的基础，帮助医疗模式从被动应对转向主动预防。

每年有数百万人死于本可以通过更早检测加以预防的疾病。急性肾损伤（AKI）就是其中之一——一种患者肾脏突然停止正常工作的病症。该病困扰着[英国](https://improvement.nhs.uk/documents/251/Patient_Safety_Alert_Stage_2_-_AKI_resources.pdf)和[美国](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3362180/)多达五分之一的住院患者，向来难以察觉，而且病情恶化可能迅速发生。[专家](https://www.ncepod.org.uk/2009aki.html)认为，如果医生能足够早地进行干预，多达 30% 的病例是可以预防的。

> 这类数字技术无疑将为及时的临床干预和治疗开辟新的可能，从而减少对患者的伤害。

Jeremy Hughes 教授

英国肾脏研究组织（Kidney Research UK）主席

过去几年，我们 DeepMind 的团队一直致力于为可避免的患者伤害这一复杂问题寻找答案，构建能够更早发现严重病症的数字工具，帮助医生和护士为有需要的患者提供更快、更好的护理。这是我们团队迄今最大的医疗健康研究突破，它证明我们不仅能更有效地发现病情恶化，还能真正在其发生之前做出预测。

DeepMind 团队与 VA 合作，将 AI 技术应用于从一百多个 VA 站点网络收集的、经过全面去标识化的电子健康记录数据集。[研究](https://www.nature.com/articles/s41586-019-1390-1)显示，该 AI 能够比目前的诊断提前最多 48 小时准确预测患者的 AKI。重要的是，对于那些病情恶化到需要接受透析的患者，模型正确预测了其中十分之九。这有望在未来为更早的预防性治疗提供一个窗口期，避免肾透析等更具侵入性的治疗手段。模型在设计上还考虑了未来的通用性：它有可能推广到败血症等疾病恶化及其他重大病因上——败血症是一种危及生命的感染。

为了解决「黑箱」问题——AI 落地临床实践的主要障碍之一——模型还会提供对其预测肾功能恶化最重要的临床信息，并给出若干相关血液检测的预测结果。这些信息或可帮助临床医生理解 AI 告警背后的推理逻辑，并预判患者未来可能出现的恶化。

然而，如果没有合适的工具向专科医生发出警报，这些预测就无法帮助真正的患者。临床医生目前仍经常使用传呼机、纸质记录和传真机相互沟通，但要让关键信息在正确的时间送达正确的专科医生手中，我们迫切需要更好的技术。因此，我们同样高兴地宣布，对我们移动医疗助手 Streams 的同行评审评估结果也于今日发表。这项工作由伦敦大学学院（University College London）的研究人员完成。

![流程图，对比了检测并上报 AKI 的缓慢人工「实施前路径」与使用 Streams 移动应用的快速自动化「数字化赋能诊疗路径」。](https://lh3.googleusercontent.com/Ru0HRA9qh_fBIxIO0MoXkcbeN3yYk_c2qzK4tmNPgsmveMh0hjKNzf4gBRpoGK8DmkjZXmFzNqAeDPlGMS6ZoYWq8cU4vyP2bZWJx22zaWq3p_Nw2A=w1440)

示意图：高危患者在传统路径与数字化赋能诊疗路径中分别如何被标记

Streams 是面向临床医生的移动医疗助手，自 2017 年初起在伦敦皇家自由 NHS 基金会信托（Royal Free London NHS Foundation Trust）投入使用。该应用使用现有的国家级 AKI 算法标记患者病情恶化，支持在病床边查看医疗信息，并使临床团队之间能够即时沟通。在皇家自由医院推广后不久，临床医生就[表示](https://www.royalfree.nhs.uk/news-media/news/new-app-helping-to-improve-patient-care/) Streams 每天为他们节省多达两小时。我们也听说了像 [Afia Ahmad](http://www.standard.co.uk/news/health/new-mother-receives-pioneering-kidney-treatment-after-app-detects-lifethreatening-illness-a3476936.html) 这样的患者的故事——正是得益于该应用，她的治疗得以及时升级。但我们希望通过严谨的临床评估来量化这些收益。今天的结果表明，该应用节省了临床医生的时间，改善了护理，并减少了该院 AKI 病例被漏诊的数量。

通过使用 Streams，[专科医生在 15 分钟或更短时间内即可完成对紧急病例的审查](https://www.nature.com/articles/s41746-019-0100-6)（而这一流程原本可能需要数小时），AKI 漏诊病例也更少（3.3%，而非 12.4%）。该应用还[将 AKI 患者的平均住院费用降低了 17%](https://www.jmir.org/2019/7/e13147/)——考虑到 AKI 每年给英国国家医疗服务体系（NHS）造成的损失[超过 10 亿英镑](https://academic.oup.com/ndt/article/29/7/1362/1844079)，这展现了未来为医院节约成本的巨大潜力。

> 这将是一场游戏规则改变者，将推进我们对急性肾损伤的诊疗与认识。

Donal O'Donoghue

曼彻斯特大学肾脏医学教授、英国肾脏护理组织（Kidney Care UK）受托人主席

[定性研究](https://www.jmir.org/2019/7/e13143/)的反馈是积极的，医疗专业人士强调了该应用如何加快了对有需要患者的发现、节省了他们执行行政事务的时间，并改善了团队沟通。一位受访者表示，该应用「让诊疗流程更加顺畅，加快了患者获得肾脏专科审查的速度」。肾病学团队的另一位临床医生则说：「无论你在医院的哪个角落，都能查到任何人的血液检测结果，这是无与伦比的……它每天至少能省下——我不知道该怎么量化——但每天至少能省下几个小时。」

在正确的时间把关于正确患者的正确信息送达正确的医生，是全球医疗体系面临的巨大难题。关键在于，皇家自由医院的这些早期发现表明，要想进一步改善患者的治疗结局，临床医生需要能够在现行 NHS 算法检测到 AKI 之前进行干预——这正是我们对 AKI 的研究如此富有前景的原因。这些结果构成了我们长期预防性医疗愿景的基石，帮助医生以主动而非被动的方式进行干预。

Streams 目前并未使用人工智能，但团队现在打算寻找方法，将预测型 AI 模型安全地集成到 Streams 中，以便为临床医生提供关于患者病情恶化的智能洞见。

对 DeepMind Health 团队而言，这是一个重大里程碑，该团队将把这项工作作为 Google Health 的一部分继续推进，由 David Feinberg 博士领导。正如我们于 2018 年 11 月[宣布](https://deepmind.com/blog/announcements/scaling-streams-google)的那样，Streams 团队以及从事医疗健康转化研究的同事们将加入 Google，以便在全球范围内产生积极影响。DeepMind Health 团队与 Google 的经验、基础设施与专业知识相结合，将帮助我们继续开发能够支持更多临床医生的移动工具，解决关键的患者安全问题，并且——我们希望——在全球范围内挽救数千人的生命。
