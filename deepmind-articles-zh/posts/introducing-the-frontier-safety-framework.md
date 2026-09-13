---
title: "前沿安全框架介绍"
title_en: "Introducing the Frontier Safety Framework"
source: https://deepmind.google/blog/introducing-the-frontier-safety-framework/
site: deepmind
date: 2024-05-17
crawled: 2026-09-13
translated: 2026-09-13
---

# 前沿安全框架介绍

> 原文：[Introducing the Frontier Safety Framework](https://deepmind.google/blog/introducing-the-frontier-safety-framework/) · Google DeepMind

我们分析与缓解先进 AI 模型未来风险的方法

Google DeepMind 一直在推动 AI 的边界，开发出的模型改变了我们对可能性的认知。我们相信，即将到来的 AI 技术将为社会提供宝贵的工具，帮助应对气候变化、药物发现和经济生产力等关键全球挑战。与此同时，我们认识到，随着我们持续推进 AI 能力的前沿，这些突破最终可能带来超越当今模型的新风险。

今天，我们正式介绍[前沿安全框架](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/introducing-the-frontier-safety-framework/fsf-technical-report.pdf)（Frontier Safety Framework）——一套用于主动识别未来可能造成严重危害的 AI 能力、并建立相应检测与缓解机制的协议。该框架聚焦于模型层面强大能力所带来的严重风险，例如异常的智能体能力或复杂的网络攻击能力。它的设计旨在与我们的对齐研究（训练模型按照人类价值观和社会目标行事）以及 Google 现有的 AI 责任与安全[实践体系](https://ai.google/responsibility/principles/)相互补充。

该框架目前处于探索阶段，我们预计随着实施经验的积累、对 AI 风险与评测理解的加深，以及与产业界、学术界和政府的合作，它将显著演进。尽管这些风险超出了当今模型的能力范围，但我们希望框架的实施与完善能帮助我们为应对它们做好准备。我们的目标是在 2025 年初之前将这一初步框架全面落地。

## 框架概览

今天公布的第一版框架建立在我们对前沿模型关键能力进行[评估](https://arxiv.org/abs/2403.13793)的[研究](https://deepmind.google/discover/blog/an-early-warning-system-for-novel-ai-risks/)基础上，并遵循了「负责任能力扩展」（[Responsible Capability Scaling](https://www.gov.uk/government/publications/emerging-processes-for-frontier-ai-safety/emerging-processes-for-frontier-ai-safety)）这一正在成形的方法。该框架包含三个关键组成部分：

1. **识别模型可能具备的、有严重危害潜力的能力。** 为此，我们研究模型在高风险领域可能造成严重危害的路径，然后确定模型在其中发挥作用所需的最小能力水平。我们将其称为「关键能力等级」（Critical Capability Levels，CCL），它们指导我们的评测与缓解方法。
2. **定期评测我们的前沿模型，以检测它们何时达到这些关键能力等级。** 为此，我们将开发一套称为「预警评测」（early warning evaluations）的模型评测套件，当某个模型接近某个 CCL 时发出警报，并以足够高的频率运行它们，以便在该阈值被触及之前获得预警。
3. **当模型通过预警评测后，应用缓解计划。** 这应当综合考虑收益与风险的整体平衡，以及预期的部署场景。这些缓解措施将主要聚焦于安全（防止模型权重外泄）和部署（防止关键能力被滥用）。

![一条水平进度条，展示 Google DeepMind 前沿安全框架：显示 AI 能力前沿向某个关键能力等级（即模型能力在未缓解的情况下蕴含严重危害风险）推进的进度，并用虚线标示在到达该阈值之前的预警评测。](https://lh3.googleusercontent.com/tUe2gHHnUi013q2evLJdwDNY_TqWQxZAjqkTFJi5t5yDbxmBzkeOKa_ITW_PibTaGvVbU-81bdrilp1gyKJKEPlR8gnfBHTfNbuiuGRmbZ39ELoA0w=w1440)

这张图展示了框架各组成部分之间的关系。

## 风险领域与缓解级别

我们最初的一组关键能力等级基于对四个领域的调研：自主性、生物安全、网络安全，以及机器学习研发（R&D）。我们的初步研究表明，未来基础模型的能力最有可能在这些领域构成严重风险。

在自主性、网络安全和生物安全方面，我们的首要目标是评估威胁行为者利用具备先进能力的模型实施后果严重的有害活动的程度。对于机器学习研发，重点在于具备这类能力的模型是否会促成其他关键能力模型的扩散，或导致 AI 能力的快速且不可控的升级。随着我们对这些及其他风险领域开展更深入的研究，我们预计这些 CCL 将不断演进，并会新增更高层级或其他风险领域的若干 CCL。

为了能针对每个 CCL 调整缓解措施的强度，我们还拟定了一套安全与部署缓解措施。更高级别的安全缓解措施能更好地防范模型权重外泄，更高级别的部署缓解措施则能对关键能力实施更严格的管理。然而，这些措施也可能拖慢创新速度、削弱能力的广泛可及性。在缓解风险与促进可及性和创新之间取得最佳平衡，对 AI 的负责任发展至关重要。通过权衡整体收益与风险，并考虑模型开发与部署的具体情境，我们力求确保负责任的 AI 进步，在释放变革性潜力的同时防范意外后果。

## 投入这门科学

框架背后的研究尚处于起步阶段，但进展迅速。我们在前沿安全团队（Frontier Safety Team）上投入了大量资源，该团队协调了框架背后的跨职能工作。他们的职责是推进前沿风险评估的科学，并基于不断深化的认知来完善我们的框架。

该团队开发了一套评测套件，用于评估关键能力带来的风险，尤其强调自主的大语言模型智能体，并在我们最先进的模型上进行了实测。他们[最近的论文](https://arxiv.org/abs/2403.13793)描述了这些评测，还探讨了可能构成未来「[预警系统](https://deepmind.google/discover/blog/an-early-warning-system-for-novel-ai-risks/)」的机制。论文介绍了评估一个模型距离完成其当前无法完成的任务还有多远的技术方法，还包含了一支专家预测团队对未来能力的预测。

## 坚守我们的 AI 原则

我们将定期审视并演进该框架。特别是，随着我们对框架进行试点，并加深对风险领域、CCL 和部署场景的理解，我们将继续开展针对具体 CCL 校准具体缓解措施的工作。

我们工作的核心是 Google 的 [AI 原则](https://ai.google/responsibility/principles/)，它要求我们在追求广泛收益的同时缓解风险。随着我们系统的改进和能力的提升，像前沿安全框架这样的举措将确保我们的实践继续兑现这些承诺。

我们期待与产业界、学术界和政府的各方合作，共同开发和完善该框架。我们希望分享我们的方法，能促进与其他各方合作，就评估未来几代 AI 模型安全性的标准和最佳实践达成一致。

[阅读技术报告](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/introducing-the-frontier-safety-framework/fsf-technical-report.pdf)
