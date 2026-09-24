---
title: "MedGemma 正在帮助全球医疗健康服务提供者提供更优质的照护"
title_en: "MedGemma is helping global healthcare providers deliver better care"
source: https://blog.google/innovation-and-ai/technology/health/medgemma-global-healthcare/
site: google-blog
date: 2026-09-23
crawled: 2026-09-24
translated: 2026-09-24
---

# MedGemma 正在帮助全球医疗健康服务提供者提供更优质的照护

> 原文：[MedGemma is helping global healthcare providers deliver better care](https://blog.google/innovation-and-ai/technology/health/medgemma-global-healthcare/) · Google

能否获得优质的医疗健康服务，往往取决于你住在哪里，以及附近是否有专科医生可用。在世界各地繁忙的城市医院和偏远的乡村诊所，医疗健康工作者都面临同样的挑战：要在专科支持有限的情况下接诊大量患者。

为了帮助应对这些挑战，我们开发了 MedGemma——一系列针对医学文本与图像理解优化的开放权重 AI 模型。MedGemma 构建在我们的 Gemma 模型之上，为开发者、研究人员和公共卫生组织提供了一个灵活适配的基础，可用于构建支持分诊、诊断筛查等场景的专用工具。自发布以来，MedGemma 的下载量已超过 1,000 万次，支撑了全球数千项研究适配。由于模型是开放的，它们可以适配本地语言、针对当地的健康优先事项进行调整，同时各组织仍可完全掌控自己的数据和基础设施。

如今，全球健康组织正在三种关键场景中让 MedGemma 发挥作用：一线照护、大流量医院以及全国性公共卫生项目。

## 触达偏远地区的患者

由于 MedGemma 是一系列开放权重模型，开发者可以在没有有效网络连接的情况下运行移动应用。

在乌干达农村地区，Crane AI 正在使用 MedGemma 构建临床决策支持应用 EaseHealth。一个经适配的 MedGemma 模型在设备端、无需网络连接即可处理临床推理，帮助社区健康工作者评估症状、查阅指南并做出有依据的分诊决策。

在其他偏远诊所，MedGemma 正在支持疾病的早期发现。

赞比亚的宫颈癌发病率位居世界前列。为应对这一问题，Dawa Health 打造了可离线使用的 [DawaMom 应用](https://developers.devsite.corp.google.com/health-ai-developer-foundations/showcase/dawamom)。DawaMom 将 MedGemma 与 [MedSigLIP](https://developers.google.com/health-ai-developer-foundations/medsiglip)
[1](#footnote-1)
——一个面向医学文本与图像的轻量级编码器——结合使用，已为超过 3,500 名女性完成筛查，并计划推广至全国及邻近地区。

在印度，[Visilant](https://developers.google.com/health-ai-developer-foundations/showcase/visilant) 使用基于智能手机的成像系统，已为 5 万多名患者完成白内障和其他眼部疾病的筛查。通过把 MedGemma 引入筛查工作流，Visilant 希望提升对可治疗眼病的检出率，抢在其造成永久性视力丧失之前。

## 在大型医院体系中支持更快速的分诊

MedGemma 也已投入大流量医疗中心使用。在 [AIIMS Delhi](https://blog.google/intl/en-in/company-news/from-seed-to-scale-partnering-with-indias-startups-to-build-the-ai-future/)（德里全印医学科学研究所），临床医生正在试点 IndusDerma——一款专门为满足印度人群独特的医疗健康需求和肤色特点而设计的 AI 辅助皮肤科筛查工具。通过在初级诊疗层面支持早期分诊、结构化临床摘要和临床决策，IndusDerma 让非皮肤科医生也能胜任筛查，并在大流量公共卫生体系中缩短患者获得诊疗的时间。

AIIMS 开发的另一款应用 Aarogyam 则聚焦门诊分诊。AIIMS 的临床医生希望借助 Aarogyam 将转诊至专科前的等待时间缩短 40%，从而提升患者满意度，并让专科医生接诊更多患者。在这些试点顺利完成并通过临床验证之后，AIIMS Delhi 的目标是在其医院网络中推广这些应用——该网络每天最多接待 1.5 万人次的门诊。

## 为国家级健康项目保护患者数据

MedGemma 可以部署在本地或任意云服务器上，让各组织将患者数据留在本地并完全处于自己的掌控之下，这对公共部门的健康举措至关重要。全球多个国家的卫生部正在使用这些模型来满足本国的特定需求。例如，印度尼西亚卫生部正在开发一个结合 MedGemma 与 MedSigLIP 的结核病检测模型，并使用本地胸部 X 光数据进行训练。该工具旨在支持卫生部每年筛查 5,000 万公民、进而消灭结核病的目标。

## 构建开放、负责任的医疗健康解决方案

MedGemma 旨在支持广泛的临床任务。它可以理解医学文档、回答问题，并解读复杂的医学影像，包括 X 光和 CT。通过发布这些模型，我们希望为全球开发者提供支持，帮助他们构建安全、保护隐私、因地制宜的工具，以应对真实世界的健康需求。MedGemma 的模型、代码仓库和文档已向全球开发者和研究人员开放。

请访问 [Health AI Developer Foundations 网站](https://goo.gle/hai-def) 获取资源，进一步了解 MedGemma 及其他模型。你也可以在 [Health AI Developer Foundations 论坛](https://discuss.ai.google.dev/c/hai-def/62) 提问或分享反馈。
