---
title: "强化我们的前沿安全框架"
title_en: "Strengthening our Frontier Safety Framework"
source: https://deepmind.google/blog/strengthening-our-frontier-safety-framework/
site: deepmind
date: 2025-09-22
crawled: 2026-09-13
translated: 2026-09-13
---

# 强化我们的前沿安全框架

> 原文：[Strengthening our Frontier Safety Framework](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/) · Google DeepMind

我们正在扩展风险领域，并完善风险评估流程。

**2026 年 4 月 17 日更新**

AI 的突破正在改变我们的日常生活，从推进数学、生物学和天文学，到释放个性化教育的潜力。在构建日益强大的 AI 模型的同时，我们致力于负责任地开发技术，并以循证的方法走在新兴风险的前面。

今天，我们发布前沿安全框架（Frontier Safety Framework，FSF）的第三个迭代版本——这是我们迄今最全面的一套识别和缓解先进 AI 模型严重风险的方法。

这次更新建立在我们与业界、学术界和政府专家持续合作的基础之上。我们还吸收了实施前几版框架所获得的经验教训，以及前沿 AI 安全领域不断演进的最佳实践。


### 应对有害操纵的风险

在这次更新中，我们引入了一个针对[有害操纵](https://deepmind.google/blog/protecting-people-from-harmful-manipulation/)的关键能力等级（Critical Capability Level，CCL）\*——具体指具备强大操纵能力的 AI 模型，这类模型可能被滥用，在与模型的交互过程中，系统性地、大幅地改变已识别的高风险情境中的信念与行为，合理地导致严重规模的额外预期伤害。

这一新增内容建立在我们此前识别和评估[生成式 AI 操纵驱动机制](https://arxiv.org/abs/2404.15058)的研究之上，并将其落地。未来，我们将继续投资这一领域，以更好地理解和度量与有害操纵相关的风险。

### 调整应对错位风险的方法

我们还扩展了框架，以应对这样一种潜在的未来场景：错位（misalignment）的 AI 模型可能干扰操作者引导、修改或关闭其运行的能力。

虽然框架的上一版纳入了一种以工具性推理 CCL（即针对 AI 模型开始产生欺骗性思考的特定警示等级）为核心的探索性方法，但在这次更新中，我们进一步为机器学习研究与开发类 CCL 提供了更多协议，聚焦于可能把 AI 研发加速到潜在失稳水平的模型。

除了这些能力带来的滥用风险之外，还存在源自模型在这些能力等级上进行无定向行动的潜力所带来的错位风险，以及此类模型可能被整合进 AI 开发与部署流程所带来的风险。

为应对 CCL 带来的风险，当触及相关 CCL 时，我们会在对外发布前进行安全案例审查。这包括开展详细分析，证明风险已被降低到可管理的水平。对于先进机器学习研究与开发类 CCL，大规模内部部署同样可能构成风险，因此我们现在将这一方法扩展到涵盖此类部署。

### 锐化风险评估流程

我们的框架旨在与风险的严重程度相称地应对风险。我们特别锐化了 CCL 的定义，以识别那些需要最严格的治理与缓解策略的关键威胁。在触及特定 CCL 阈值之前，我们就会持续应用安全与安保缓解措施，这也是我们标准模型开发方法的一部分。

最后，本次更新更详细地介绍了我们的风险评估流程。在我们核心的预警评测基础上，我们描述了如何开展整体性评估，包括系统性的风险识别、对模型能力的全面分析，以及对风险可接受性的明确判定。

### FSF 3.1：引入受追踪能力等级

自 2026 年 4 月 17 日起，我们在[前沿安全框架](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/strengthening-our-frontier-safety-framework/frontier-safety-framework_3-1.pdf)的部分领域中新增受追踪能力等级（Tracked Capability Levels，TCL），引入一种新的能力等级，帮助我们更早发现并评估那些潜在的非极端风险。

我们还就完整的风险管理流程——从最初识别到缓解——提供了更多细节。

## 坚守我们对前沿安全的承诺

前沿安全框架体现了我们的持续承诺：在能力向通用人工智能（AGI）迈进的过程中，以科学、循证的方法追踪并领先于 AI 风险。通过扩展风险领域、强化风险评估流程，我们旨在确保变革性的 AI 造福人类，同时把潜在危害降到最低。

我们的框架将继续基于新的研究、利益相关方的意见和实施中的经验教训而演进。我们始终致力于与业界、学术界和政府协同合作。

通往有益 AGI 的道路不仅需要技术突破，也需要健全的框架来化解沿途的风险。我们希望这次更新的前沿安全框架能为这一集体努力做出切实的贡献。

**了解更多**

[阅读最新的前沿安全框架](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/strengthening-our-frontier-safety-framework/frontier-safety-framework_3-1.pdf)

**脚注**

\*我们的框架围绕称为关键能力等级（CCL）的能力阈值构建。这些是如下能力水平：若缺乏缓解措施，前沿 AI 模型或系统可能在此水平上带来严重伤害的加剧风险。
