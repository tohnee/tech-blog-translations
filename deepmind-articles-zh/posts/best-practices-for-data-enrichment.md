---
title: "数据富集的最佳实践"
title_en: "Best practices for data enrichment"
source: https://deepmind.google/blog/best-practices-for-data-enrichment/
site: deepmind
date: 2022-11-16
crawled: 2026-09-13
translated: 2026-09-13
---

# 数据富集的最佳实践

> 原文：[Best practices for data enrichment](https://deepmind.google/blog/best-practices-for-data-enrichment/) · Google DeepMind

与 AI 伙伴关系组织（Partnership on AI）共同构建负责任的数据收集方式

在 DeepMind，我们的目标是确保我们所做的一切都达到最高的安全与伦理标准，符合我们的[运行原则](https://deepmind.google/blog/how-our-principles-helped-define-alphafolds-release/)（Operating Principles）。这一切最重要的起点之一，便是我们如何收集数据。过去 12 个月里，我们与 [Partnership on AI](https://partnershiponai.org/)（PAI）合作，认真思考这些挑战，并共同制定了一套用于负责任人类数据收集的标准化最佳实践与流程。

## 人类数据收集

三年多前，我们成立了人类行为研究伦理委员会（Human Behavioural Research Ethics Committee，HuBREC）。这是一个参照学术机构审查委员会（IRB）——例如医院和大学中常见的那种——模式设立的管理机构，旨在保护参与我们研究的人类受试者的尊严、权利与福祉。该委员会监督以人为研究对象的实验性行为研究，例如研究人类在决策过程中如何与人工智能（AI）系统交互。

在涉及行为研究的项目之外，AI 社区还日益投入到"数据富集"（data enrichment）相关的工作中——即由人来执行、用于训练和验证机器学习模型的任务，例如数据标注和模型评估。行为研究通常依赖作为研究对象的自愿参与者，而数据富集则涉及有偿完成任务以改进 AI 模型的人。

这类任务通常在众包平台上进行，往往引发与工人报酬、福祉和公平性相关的伦理考量，而相关平台可能缺乏必要的指引或治理体系来保证达到足够的标准。随着各研究实验室加速开发日益精密的模型，对数据富集实践的依赖可能会不断增长，对更强指引的需求也随之而来。

![一幅抽象的线条插画：中央是一个紫色菱形中的天平图标，通过电路般的线条与多个符号相连，这些符号代表合乎伦理的数据收集，包括盾牌、对勾、图表、用户档案和安全指示。](https://lh3.googleusercontent.com/A_3-bk3DSqECVjlksGBzFpt5n763bQlLYTHmvnx-gypkGhGgYXYSF2eHESJPSc8NZ6h-AjMCfCZ0KK3Iy2k2Xj9hdAK-sBduQCMzj98fQtLbJGwGDnU=w1440)

作为运行原则的一部分，我们承诺维护并推动 AI 安全与伦理领域（包括公平性与隐私）的最佳实践，以避免产生伤害风险的非预期后果。

## 最佳实践

继 PAI 关于数据富集服务负责任采购的[最新白皮书](https://partnershiponai.org/responsible-sourcing-considerations/)之后，我们合作制定了数据富集的实践与流程。其中包括为 AI 从业者创建的五个步骤，用以改善参与数据富集任务人员的工作条件（更多细节请访问 [PAI 的数据富集采购指南](https://partnershiponai.org/wp-content/uploads/2022/11/data-enrichment-guidelines.pdf)）：

1. 选择合适的报酬模式，确保所有工人的报酬高于当地生活工资。
2. 在启动数据富集项目之前，先行设计并运行一次试点。
3. 为目标任务寻找合适的工人。
4. 为工人提供经验证的说明和/或培训材料。
5. 与工人建立清晰、定期的沟通机制。

我们共同创建了必要的政策与资源，期间向内部法务、数据、安全、伦理和研究团队征求了多轮反馈，随后在少数几个数据收集项目上进行试点，之后再推广到整个组织。

这些文件更清晰地说明了在 DeepMind 设置数据富集任务的最佳方式，提升了我们研究人员对研究设计与执行的信心。这不仅提高了我们审批与启动流程的效率，更重要的是，改善了参与数据富集任务人员的体验。

PAI 最近的案例研究《在一家 AI 开发商落地负责任的数据富集实践：DeepMind 之例》（[Implementing Responsible Data Enrichment Practices at an AI Developer: The Example of DeepMind](https://partnershiponai.org/wp-content/uploads/2022/11/case-study_deepmind.pdf)）进一步解释了负责任的数据富集实践，以及我们如何将其融入现有流程。PAI 还为希望开发类似流程的 AI 从业者和组织提供了[有用的资源与支持材料](https://partnershiponai.org/responsible-sourcing-library/)。

## 展望未来

尽管这些最佳实践为我们的工作提供了支撑，我们不应仅依赖它们来确保我们的项目达到研究参与者和工人福祉与安全的最高标准。DeepMind 的每个项目都不相同，因此我们设有一个专门的人类数据审查流程，让我们能够与研究团队持续沟通，逐案识别并化解风险。

这项工作旨在为其他有意改进数据富集采购实践的组织提供参考，我们希望这能促成跨行业的对话，进一步发展这些准则与资源，惠及各团队与合作伙伴。通过这次合作，我们还希望引发更广泛的讨论：AI 社区如何继续发展负责任数据收集的规范，并共同建设更好的行业标准。

进一步了解我们的[运行原则](https://deepmind.google/blog/how-our-principles-helped-define-alphafolds-release/)。
