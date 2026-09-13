---
title: "更新前沿安全框架"
title_en: "Updating the Frontier Safety Framework"
source: https://deepmind.google/blog/updating-the-frontier-safety-framework/
site: deepmind
date: 2025-02-04
crawled: 2026-09-13
translated: 2026-09-13
---

# 更新前沿安全框架

> 原文：[Updating the Frontier Safety Framework](https://deepmind.google/blog/updating-the-frontier-safety-framework/) · Google DeepMind

前沿安全框架（FSF）的下一轮迭代，在通往 AGI 的道路上制定了更强的安全协议

AI 是一个强大的工具，正在帮助解锁新的突破，并在我们这个时代一些最大的挑战上取得重大进展——从气候变化到药物发现。但随着它的发展不断推进，先进能力可能带来新的风险。

正因如此，我们于去年[推出了](https://deepmind.google/discover/blog/introducing-the-frontier-safety-framework/)前沿安全框架的第一版——一套帮助我们领先于强大前沿 AI 模型可能带来的严重风险的协议。此后，我们与产业界、学术界和政府的专家合作，加深了对风险的理解、对风险的实证评测，以及我们可以应用的缓解措施。我们还在针对 Gemini 2.0 等前沿模型的安全与治理流程中落实了该框架。作为这项工作的成果，今天我们发布更新版的[前沿安全框架](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/updating-the-frontier-safety-framework/Frontier%20Safety%20Framework%202.0.pdf)。

框架的主要更新包括：

- 针对我们的关键能力等级（CCL）给出安全等级（Security Level）建议，帮助识别哪些环节最需要全力遏制模型权重外泄风险
- 实施一套更一致的部署缓解措施应用流程
- 阐述一套业界领先的处理欺骗性对齐风险的方法

## 关于强化安全的建议

安全缓解措施有助于防止未经授权的行为者外泄模型权重。这一点尤其重要，因为获得模型权重意味着可以移除大多数防护措施。鉴于展望日益强大的 AI 时所牵涉的利害关系，在这方面出错可能对安全造成严重影响。我们的初始框架认识到需要一种分层的安全方法，允许实施强度不一的缓解措施，以与风险相匹配。这种相称的方法也确保我们在缓解风险与促进访问和创新之间取得恰当的平衡。

从那时起，我们借鉴[更广泛的研究](https://www.rand.org/pubs/research_reports/RRA2849-1.html)来演进这些安全缓解等级，并为我们的每个 CCL 推荐一个等级。\* 这些建议反映了我们的评估：前沿 AI 领域在模型达到某个 CCL 时应当适用的最低适当安全等级。这一映射过程帮助我们把最需要最强缓解措施、以遏制最大风险的环节分离出来。在实践中，由于我们整体安全姿态的强大，我们安全实践的某些方面可能超出此处推荐的基线等级。

框架的第二版为机器学习研发（R&D）领域内的 CCL 推荐了格外高的安全等级。我们认为，对于未来的情景——当模型能够显著加速和/或自动化 AI 开发本身时——前沿 AI 开发者拥有强大的安全能力将十分重要。这是因为，这类能力若不受控制地扩散，将极大挑战社会审慎管理并适应 AI 发展快速步伐的能力。

确保前沿 AI 系统的持续安全，是一项全球共同的挑战，也是所有领先开发者的共同责任。重要的是，把这件事做对是一个集体行动问题：如果安全缓解措施未在整个领域广泛采用，任何单个行为者的安全缓解措施的社会价值都将大打折扣。构建我们认为可能需要的这类安全能力需要时间——因此，所有前沿 AI 开发者齐心协力迈向更高的安全措施、加速推进共同的行业标准至关重要。

## 部署缓解措施流程

我们还在框架中阐述了部署缓解措施，重点是防止我们所部署的系统中的关键能力被滥用。我们更新了部署缓解方法，对在滥用风险领域达到某个 CCL 的模型应用更严格的安全缓解流程。

更新后的方法包括以下步骤：首先，我们通过在一组防护措施上迭代来准备一套缓解措施。在此过程中，我们还将制定一份安全论证（safety case），即一个可评估的论证，表明与模型 CCL 相关的严重风险已被降低到可接受的水平。随后由适当的公司治理机构审查该安全论证，只有获得批准才会正式发布（GA）部署。最后，我们在部署之后继续审查并更新防护措施与安全论证。我们做出这一改变，是因为我们认为所有关键能力都值得经过这样彻底的缓解流程。

## 应对欺骗性对齐风险的方法

框架的第一版主要聚焦滥用风险（即威胁行为者利用已部署或已外泄模型的关键能力造成危害的风险）。在此基础上，我们采取了一套业界领先的方法，主动应对欺骗性对齐的风险，即自主系统蓄意破坏人类控制的风险。

针对这一问题的一种初步方法，聚焦于检测模型何时可能发展出某种基线的工具性推理能力，使其能在缺乏防护措施的情况下破坏人类控制。为缓解这一点，我们探索自动化监控，以检测对工具性推理能力的非法使用。

我们不指望自动化监控在长期内持续足够——如果模型达到更强的工具性推理水平——因此我们正在积极开展、并强烈鼓励进一步的针对这些场景的缓解方法研究。虽然我们还不知道这类能力出现的可能性有多大，但我们认为整个领域为这种可能性做好准备十分重要。

## 结语

我们将以我们的 [AI 原则](https://ai.google/responsibility/principles/)为指导，持续审视并发展这一框架，这些原则进一步阐明了我们对负责任开发的承诺。

作为努力的一部分，我们将继续与社会各界的合作伙伴协作。例如，如果我们评估某个模型已达到对公共整体安全构成未经缓解的实质性风险的 CCL，我们会在有助于推动安全 AI 发展的情况下，向相应的政府主管部门共享信息。此外，最新版框架概述了若干可供进一步研究的潜在领域——我们期待在这些领域与研究社区、其他公司和政府展开合作。

我们相信，开放、迭代和协作的方式，将有助于为评估未来 AI 模型的安全性建立共同标准和最佳实践，同时保障 AI 为人类带来的益处。[首尔前沿 AI 安全承诺](https://www.gov.uk/government/publications/frontier-ai-safety-commitments-ai-seoul-summit-2024/frontier-ai-safety-commitments-ai-seoul-summit-2024)标志着这一集体行动迈出的重要一步——我们希望我们更新后的前沿安全框架为这一进程做出进一步贡献。展望 AGI，把这件事做对将意味着解答影响极其深远的问题——例如恰当的能力阈值与缓解措施——这些都需要包括政府在内的更广泛社会的投入。

[阅读技术报告](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/updating-the-frontier-safety-framework/Frontier%20Safety%20Framework%202.0.pdf)

前沿安全框架的最新更新由 Lewis Ho, Celine Smith, Claudia van der Salm, Joslyn Barnhart 和 Rohin Shah 开发，领导者为 Allan Dafoe, Anca Dragan, Andy Song, Demis Hassabis（德米斯·哈萨比斯）, Four Flynn, Jennifer Beroshi, Helen King, Nicklas Lundblad 和 Tom Lue。我们感谢 Aalok Mehta, Adam Stubblefield, Alex Kaskasoli, Alice Friend, Amy Merrick, Anna Wang, Ben Bariach, Charley Snyder, David Bledin, David Lindner, Dawn Bloxwich, Don Wallace, Eva Lu, Heidi Howard, Iason Gabriel, James Manyika, Joana Iljazi, Kent Walker, Lila Ibrahim, Mary Phuong, Mikel Rodriguez, Peng Ning, Roland S. Zimmermann, Samuel Albanie, Sarah Cogan, Sasha Brown, Seb Farquhar, Sebastien Krier, Shane Legg, Victoria Krakovna, Vijay Bolina, Xerxes Dotiwalla, Ziyue Wang 的重大贡献。

**脚注**

\*关键能力定义——为识别模型可能拥有的、具有造成严重危害潜力的能力，我们研究模型在高风险领域可能造成严重危害的路径，然后确定模型为在这一危害中扮演角色所必须具备的最低能力水平。我们称之为"关键能力等级"（CCL），它们指导我们的评估与缓解方法。
