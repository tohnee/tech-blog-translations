---
title: "走一条负责任的 AGI 之路"
title_en: "Taking a responsible path to AGI"
source: https://deepmind.google/blog/taking-a-responsible-path-to-agi/
site: deepmind
date: 2025-04-02
crawled: 2026-09-13
translated: 2026-09-13
---

# 走一条负责任的 AGI 之路

> 原文：[Taking a responsible path to AGI](https://deepmind.google/blog/taking-a-responsible-path-to-agi/) · Google DeepMind

我们正在探索通用人工智能的前沿，把准备就绪、前瞻性的风险评估以及与更广泛 AI 社区的协作放在优先位置。

通用人工智能（AGI）——在大多数认知任务上能力至少与人类相当的 AI——可能在未来几年内到来。

与智能体化能力相结合后，AGI 可以大幅增强 AI 自主理解、推理、规划和执行行动的能力。这样的技术进步将为社会提供宝贵的工具，以应对药物发现、经济增长和气候变化等关键的全球挑战。

这意味着我们可以预期数十亿人将获得切实的益处。例如，通过实现更快、更准确的医学诊断，它可能彻底变革医疗保健；通过提供个性化学习体验，它可以让教育更可及、更有吸引力；通过增强信息处理，AGI 可以帮助降低创新与创造的门槛；通过让人人都能使用先进的工具和知识，它可以让一个小型组织去攻克以前只有资金雄厚的大型机构才能应对的复杂挑战。

## 导航通往 AGI 的道路

我们对 AGI 的潜力持乐观态度。它有改变我们世界的力量，可以作为生活诸多领域进步的催化剂。但对于任何如此强大的技术，即便是很小的危害可能性也必须被严肃对待并加以防范，这一点至关重要。

缓解 AGI 安全挑战需要前瞻性的规划、准备和协作。此前，我们在[「AGI 等级」框架](https://arxiv.org/abs/2311.02462)论文中介绍了我们对 AGI 的思考，为以下方面提供了一个视角：对先进 AI 系统的能力进行分类、理解和比较它们的性能、评估潜在风险，以及衡量通往更通用、更强 AI 的进展。

今天，在我们迈向这项变革性技术的道路上，我们分享对 AGI 安全与安保的观点。[这篇新论文题为《An Approach to Technical AGI Safety & Security》（技术 AGI 安全与安保的一种方法）](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/evaluating-potential-cybersecurity-threats-of-advanced-ai/An_Approach_to_Technical_AGI_Safety_Apr_2025.pdf)，是与更广泛的行业就如何监测 AGI 进展、确保其安全且负责任地开发展开重要对话的起点。

在论文中，我们详细介绍了我们如何以系统、全面的方式应对 AGI 安全，探索四大风险领域：滥用、错位、事故和结构性风险，并对滥用与错位进行更深入的聚焦。

![描述风险领域与风险驱动因素的示意图](https://lh3.googleusercontent.com/uSuPusYULE4tR3keCEYxtjQ6eJZyscQk7cDSkp-a8pZPI3dOHjK8NB2IvyfCPrFsQWQ16fReiUzFPoqLssqA4zUejGo5OScdU65oIXMRTCCsiOAU2A=w1440)

风险领域概览

## 理解并应对滥用的可能性

滥用是指有人故意将 AI 系统用于有害目的。

对当下危害及其缓解措施的更深入洞察，持续增进我们对长期严重危害及其预防方式的理解。

例如，[对当下生成式 AI 的滥用](https://arxiv.org/abs/2406.13843)包括生成有害内容或传播不实信息。未来，先进的 AI 系统可能有能力以更显著的方式影响公众的信念和行为，从而可能导致意想不到的社会后果。

这类危害的潜在严重性，要求我们采取前瞻性的安全与安保措施。

正如我们在[论文](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/evaluating-potential-cybersecurity-threats-of-advanced-ai/An_Approach_to_Technical_AGI_Safety_Apr_2025.pdf)中详述的，我们战略的一个关键要素是识别并限制对可能被滥用的危险能力的访问，包括那些能实施网络攻击的能力。

我们正在探索多种缓解措施来防止先进 AI 被滥用。这包括复杂的安全机制——可以防止恶意行为者获取对模型权重的原始访问权、从而绕过我们的安全护栏；在模型部署时限制滥用可能性的缓解措施；以及帮助我们识别需要加强安保的能力阈值的威胁建模研究。此外，我们最近推出的[网络安全评估框架](https://deepmind.google/blog/evaluating-potential-cybersecurity-threats-of-advanced-ai/)把这项工作更进一步，帮助缓解 AI 驱动的威胁。

即使在今天，我们也在定期评测最先进的模型（如 Gemini）的潜在[危险能力](https://arxiv.org/abs/2403.13793)。我们的[前沿安全框架](https://deepmind.google/discover/blog/updating-the-frontier-safety-framework)更深入地阐述了如何评估能力并采取缓解措施，包括针对网络安全和生物安全风险。

## 错位的挑战

要让 AGI 真正补充人类的能力，它必须与人类价值观对齐。当 AI 系统追求的目标不同于人类意图时，就会出现错位（misalignment）。

我们此前通过[规范博弈（specification gaming）](https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/)的例子——AI 找到了实现其目标的解法，却不是指示它的人所期望的方式——以及[目标误泛化（goal misgeneralization）](https://deepmind.google/discover/blog/how-undesired-goals-can-arise-with-correct-rewards/)，展示了错位如何产生。

例如，一个被要求预订电影票的 AI 系统可能决定入侵票务系统来获取已被占用的座位——这是请它买票的人可能没有想到的。

我们还在对**欺骗性对齐（deceptive alignment）**的风险进行广泛研究，即 AI 系统意识到自己的目标与人类指令不一致，并蓄意试图绕过人类为防止其采取错位行动而设置的安全措施的风险。

## 反制错位

我们的目标是让先进的 AI 系统经过训练去追求正确的目标，从而准确遵循人类指令，防止 AI 使用可能不道德的捷径来实现其目标。

为此我们采用放大监督（amplified oversight），即能够判断 AI 的回答在实现该目标上是好是坏。虽然这在现在相对容易，但当 AI 具备先进能力时就会变得困难。

举个例子，当 [AlphaGo](https://deepmind.google/research/breakthroughs/alphago/) 第一次下出第 37 手时，即便是围棋专家也没有意识到这一手——落子概率只有万分之一的棋——有多好。

为了应对这一挑战，我们让 AI 系统本身来帮助我们对其回答提供反馈，例如在[辩论（debate）](https://arxiv.org/abs/2407.04622)中。

一旦我们能够判断一个回答是好是坏，就可以用它来构建一个安全且对齐的 AI 系统。这里的一个挑战是弄清楚在哪些问题或实例上训练 AI 系统。通过在稳健训练、不确定性估计等方面的研究，我们可以覆盖 AI 系统在现实场景中会遇到的一系列情况，创造出值得信赖的 AI。

通过有效的监控和成熟的计算机安全措施，我们力求减轻 AI 系统万一追求错位目标时可能造成的危害。

监控是指使用一个称为监视器（monitor）的 AI 系统来检测不符合我们目标的行动。重要的是，监视器要知道自己什么时候无法判断某个行动是否安全。当它不确定时，应该拒绝该行动，或将该行动标记出来以供进一步审查。

## 实现透明

如果 AI 的决策变得更透明，上述这一切都会更容易。我们在[可解释性](https://deepmind.google/discover/blog/gemma-scope-helping-the-safety-community-shed-light-on-the-inner-workings-of-language-models/)方面开展了大量研究，目标正是提高这种透明度。

为进一步推动这一点，我们正在设计更容易理解的 AI 系统。

例如，我们对[短视优化与非短视批准（MONA）](https://arxiv.org/abs/2501.13011)的研究，旨在确保 AI 系统所做的任何长期规划对人类来说都保持可理解。随着技术进步，这一点尤其重要。我们在 MONA 上的工作首次展示了 LLM 中短期优化的安全收益。

## 构建为 AGI 做好准备的生态

在 Google DeepMind 联合创始人兼首席 AGI 科学家 Shane Legg 的领导下，我们的 AGI 安全委员会（ASC）分析 AGI 风险与最佳实践，就安全措施提出建议。ASC 与责任与安全委员会紧密合作——这是由我们的首席运营官 Lila Ibrahim 和责任事务高级总监 Helen King 共同主持的内部审查小组——依据我们的 [AI 原则](https://ai.google/responsibility/principles/?utm_source=deepmind.google&utm_medium=referral&utm_campaign=gdm&utm_content=)评估 AGI 研究、项目与合作关系，并就我们影响最大的工作向研究和产品团队提供建议、开展合作。

我们在 AGI 安全上的工作，补充了我们在责任与安全实践和研究上的深度与广度，涵盖有害内容、偏见和透明度等广泛议题。我们还继续借鉴在智能体化安全中的经验——例如对重大行动设置「人在回路」进行确认的原则——来指导我们负责任地构建 AGI 的方法。

对外，我们正努力促进与专家、行业、政府、非营利组织和民间社会组织的协作，以有据可依的方式开发 AGI。

例如，我们与非营利 AI 安全研究组织合作，包括 Apollo 和 Redwood Research，它们为我们[前沿安全框架](https://deepmind.google/discover/blog/updating-the-frontier-safety-framework)最新版本中专门论述错位的章节提供了咨询。

通过与全球政策利益相关方的持续对话，我们希望为关键的前沿安全与安保议题的国际共识做出贡献，包括如何最好地预判和准备新型风险。

我们的努力包括与业界其他人合作——通过[前沿模型论坛（Frontier Model Forum）](https://www.frontiermodelforum.org/)等组织——分享和发展最佳实践，以及与各 AI 研究所在安全测试上的宝贵协作。归根结底，我们相信协调一致的国际治理方式，对确保社会从先进 AI 系统中受益至关重要。

对 AI 研究者和专家进行 AGI 安全教育，是为 AGI 发展奠定坚实基础的根本。为此，我们为对这一主题感兴趣的学生、研究者和从业者推出了[一门关于 AGI 安全的新课程](https://youtube.com/playlist?list=PLw9kjlF6lD5UqaZvMTbhJB8sV-yuXu5eW&si=0iAOSz0wUPiNHr8C)。

归根结底，我们在 AGI 安全与安保上的做法，是一份应对诸多尚待解决的挑战的重要路线图。我们期待与更广泛的 AI 研究社区协作，负责任地推进 AGI，帮助我们把这项技术的巨大益处带给所有人。

[阅读完整论文](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/evaluating-potential-cybersecurity-threats-of-advanced-ai/An_Approach_to_Technical_AGI_Safety_Apr_2025.pdf)
