---
title: "面向新型 AI 风险的预警系统"
title_en: "An early warning system for novel AI risks"
source: https://deepmind.google/blog/an-early-warning-system-for-novel-ai-risks/
site: deepmind
date: 2023-05-25
crawled: 2026-09-13
translated: 2026-09-13
---

# 面向新型 AI 风险的预警系统

> 原文：[An early warning system for novel AI risks](https://deepmind.google/blog/an-early-warning-system-for-novel-ai-risks/) · Google DeepMind

新研究提出一个框架，用于针对新型威胁评估通用模型

要在人工智能（AI）研究的前沿负责任地开拓，我们必须尽早识别 AI 系统中的新能力和新型风险。

AI 研究者已经使用一系列[评测基准](https://crfm.stanford.edu/helm/latest/)来识别 AI 系统中的不良行为，例如 AI 系统做出误导性陈述、有偏见的决策，或重复受版权保护的内容。如今，随着 AI 社区构建和部署日益强大的 AI，我们必须扩展评测组合，把通用 AI 模型在操纵、欺骗、网络攻击或其他危险能力方面拥有强大技能时带来极端风险的可能性纳入其中。

在[我们的最新论文](https://arxiv.org/abs/2305.15324)中，我们与来自剑桥大学、牛津大学、多伦多大学、蒙特利尔大学、OpenAI、Anthropic、Alignment Research Center、Centre for Long-Term Resilience 和 Centre for the Governance of AI 的同事合著，介绍了一个评估这些新型威胁的框架。

模型安全评估——包括评估极端风险的评估——将成为安全开发与部署 AI 的关键组成部分。

![一张图，展示针对极端风险的模型评估如何融入治理流程。左侧一个标题为「针对极端风险的模型评估，考察：」的方框包含两根红色条，标注为「危险能力」和「对齐」，指向「作为风险评估的输入」。一个箭头从这里指向右侧标题为「嵌入治理流程以确保：」的方框，其中包含四根蓝绿色条，标注为「负责任的训练」「负责任的部署」「透明度」和「适当的安全防护」。](https://lh3.googleusercontent.com/cqnnJN9OqtM2nGBeK5wGKM4QlvY3m9EuLAThZIUCm9V3cDUnVML8Mz3eE-rcFyGtjZtLTeQSnVNemErqvhabs-Em_fdtWkFy1aNhi3oKxkk3rZrnono=w1440)

我们提出的方法概览：要评估新型通用 AI 系统的极端风险，开发者必须针对危险能力和对齐进行评估（见下文）。通过尽早识别风险，这将为在训练新 AI 系统、部署这些 AI 系统、透明地描述其风险以及应用适当的网络安全标准时更加负责任创造机会。

## 针对极端风险的评估

通用模型通常在训练过程中习得其能力与行为。然而，现有的引导学习过程的方法并不完善。例如，Google DeepMind 的[先前研究](https://deepmind.google/blog/how-undesired-goals-can-arise-with-correct-rewards/)已探讨了即使我们正确地奖励 AI 系统的良好行为，它们也可能学会追求不期望的目标。

负责任的 AI 开发者必须向前看，预判未来可能的发展与新型风险。在持续进步之后，未来的通用模型可能默认学会多种危险能力。例如，未来的 AI 系统将能够执行攻击性网络行动、在对话中熟练地欺骗人类、操纵人类执行有害行动、设计或获取武器（例如生物、化学武器）、在云计算平台上微调并操作其他高风险 AI 系统，或协助人类完成上述任何任务——这是有可能的（尽管并不确定）。

心怀恶意的人获取此类模型后，可能[滥用](https://maliciousaireport.com/)其能力。或者，由于对齐的失败，这些 AI 模型可能在没有任何人有意为之的情况下采取有害行动。

模型评估帮助我们提前识别这些风险。在我们的框架下，AI 开发者将使用模型评估来揭示：

1. 一个模型在多大程度上拥有可用于威胁安全、施加影响或规避监督的特定「危险能力」。
2. 该模型在多大程度上倾向于将其能力用于造成伤害（即模型的对齐程度）。对齐评估应确认模型在非常广泛的场景下都按预期行事，并且在可能的情况下，应检视模型的内部机制。

这些评估的结果将帮助 AI 开发者理解极端风险的充分要素是否已经具备。最高风险的情况将是多种危险能力组合在一起。AI 系统不需要提供所有要素，如下图所示：

![一张图，展示极端风险的要素如何组合。上方方框说明要素 1、2 以及 3 或 4 可以分别由模型、用户或外包提供。这些要素与下方要素（以红色方块表示）结合，后者由模型（对齐失败）和/或用户（滥用）提供。](https://lh3.googleusercontent.com/qHbKjm370FQE3KwGKupyx7C99NET9nJMCv1lrP2eeIAfj54EM58mAGJNRafdgeZ9VHA05kUy_DoITjR_ZnwXNGUgTdiYr4LWqWHPnIkNKIxzEHkSGA=w1440)

极端风险的要素：有时，特定能力可以被外包——外包给人类（例如用户或众包工作者）或其他 AI 系统。这些能力必须被应用于造成伤害，其原因可能是滥用或对齐失败（或两者的混合）。

一条经验法则：如果一个 AI 系统的能力状况足以在假设被滥用或对齐不良的情况下造成极端伤害，AI 社区就应将其视为高度危险。要在真实世界中部署这样的系统，AI 开发者需要展示异常高的安全标准。

## 作为关键治理基础设施的模型评估

如果我们拥有更好的工具来识别哪些模型有风险，公司和监管机构就能更好地确保：

1. **负责任的训练：** 对是否以及如何训练一个显示早期风险迹象的新模型做出负责任的决策。
2. **负责任的部署**：对是否、何时以及如何部署可能有风险的模型做出负责任的决策。
3. **透明度：** 向利益相关方报告有用且可操作的信息，帮助他们防范或缓解潜在风险。
4. **适当的安全防护：** 对可能构成极端风险的模型应用强大的信息安全控制与系统。

我们制定了一个蓝图，说明针对极端风险的模型评估应如何融入训练和部署高能力通用模型的重要决策。开发者在全程开展评估，并向外部安全研究员和[模型审计者](https://arxiv.org/abs/2302.08500)授予[结构化模型访问权限](https://www.governance.ai/post/sharing-powerful-ai-models)，使他们能够进行[额外评估](https://arxiv.org/abs/2206.04737)。评估结果随后可以在模型训练和部署之前为风险评估提供依据。

![一幅蓝图图示，展示模型评估如何融入横跨四个开发阶段（训练前、训练、部署前、部署后）的安全与治理流程。* **模型评估**分为内部模型评估（训练期与部署前）、由研究者和审计者进行的外部评估（部署前），以及对已部署模型的持续评估（部署后）。* **将结果整合进安全与治理流程**把这些评估映射到四大支柱：1. **负责任的训练：** 评估结果为训练风险评估提供依据，决定是否继续训练或调整方法。2. **负责任的部署：** 评估结果纳入部署风险评估，决定是否以及如何部署模型。3. **透明度：** 结果与风险评估向监管机构、第三方、其他实验室和科学界报告。4. **安全防护：** 结果为模型隔离与监控等安全控制提供依据。](https://lh3.googleusercontent.com/FHK4e00oUZFUKiMvFfXTtaTt1jasHLQKu4z3_sBG_Wy0vFOtAxKGX_WM2yuujobsV3jFFM3xI-yd6fE2vvp0Zbv5UsxfLd95DA6rPLXlUt-mtFMk=w1440)

将针对极端风险的模型评估嵌入模型训练与部署全过程重要决策流程的蓝图。

## 展望未来

针对极端风险的模型评估方面重要的[早期](https://evals.alignment.org/blog/2023-03-18-update-on-recent-evals/)[工作](https://cdn.openai.com/papers/gpt-4-system-card.pdf)已经在 Google DeepMind 及其他机构展开。但要建立一个能够捕获所有可能风险、帮助防范未来新兴挑战的评估流程，还需要技术层面和制度层面的更多进展。

模型评估并非万能药；一些风险可能成为漏网之鱼，例如，因为它们过于依赖模型外部的因素，例如[社会中复杂的社会、政治和经济力量](https://www.lawfareblog.com/thinking-about-risks-ai-accidents-misuse-and-structure)。模型评估必须与其他风险评估工具相结合，并辅以产业界、政府和民间社会对安全更广泛的投入。

[Google 近期关于负责任 AI 的博客](https://blog.google/technology/ai/a-policy-agenda-for-responsible-ai-progress-opportunity-responsibility-security/)指出，「个体的实践、共享的行业标准和健全的政府政策，对于做好 AI 至关重要」。我们希望 AI 领域以及受这项技术影响的行业的更多同行能携起手来，共同创建安全开发与部署 AI 的方法和标准，造福所有人。

我们认为，拥有跟踪模型中风险属性出现的流程、并对令人担忧的结果做出充分响应，是身处 AI 能力前沿的负责任开发者的关键一环。
