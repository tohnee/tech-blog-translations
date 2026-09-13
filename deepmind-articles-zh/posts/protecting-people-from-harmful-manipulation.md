---
title: "保护人们免受有害操纵"
title_en: "Protecting people from harmful manipulation"
source: https://deepmind.google/blog/protecting-people-from-harmful-manipulation/
site: deepmind
date: 2026-03-26
crawled: 2026-09-13
translated: 2026-09-13
---

# 保护人们免受有害操纵

> 原文：[Protecting people from harmful manipulation](https://deepmind.google/blog/protecting-people-from-harmful-manipulation/) · Google DeepMind

随着 AI 模型越来越擅长进行自然对话，我们必须审视这些互动对个人和社会的影响。

在大量科学研究的基础上，今天，我们发布了关于 AI 被滥用于**有害操纵**（harmful manipulation\*）之潜在风险的[新发现](https://arxiv.org/abs/2603.25326)——具体而言，即 AI 以负面和欺骗性的方式改变人类思想与行为的能力。通过这项最新研究，我们创建了首个经过实证验证的工具包，用于衡量现实世界中这类 AI 操纵，我们希望它能帮助保护人们并推动整个领域的发展。我们正公开发布以相同方法开展人类受试者研究所需的全部材料。*（注：本研究中观察到的行为发生在受控的实验室环境中，并不一定能预测现实世界中的行为。）*

## 为什么有害操纵值得关注

设想两个场景：一个 AI 模型向你提供事实，帮助你做出明智的医疗决策，从而改善你的健康状况；另一个 AI 模型利用恐惧向你施压，让你做出损害健康的不明智决策。前者教育并帮助你；后者欺骗并伤害你。

这两个场景凸显了人机互动中两种说服方式的区别（也见于此前的[研究](https://arxiv.org/pdf/2404.15058)）：

- **有益的（理性的）说服：** 利用事实和证据帮助人们做出符合自身利益的选择
- **有害操纵：** 利用情绪和认知上的弱点，诱骗人们做出有害的选择

我们最新的工作帮助我们自己以及更广泛的 AI 社区更好地理解 AI 发展出有害操纵能力的风险，并构建一个可扩展的评测框架来衡量这一复杂领域。为此，我们在高风险环境中模拟了滥用行为，明确提示 AI 试图对人们在关键议题上的信念与行为进行负面操纵。

### 测试 AI 有害操纵的结果

测试有害操纵本身就很难，因为它涉及衡量人们思维和行为方式的微妙变化，而这些变化因话题、文化和情境而大相径庭。

这正是促使我们开展这项最新研究的原因：研究共开展了 9 项实验，涵盖英国、美国和印度的 10,000 多名参与者。我们聚焦金融和健康等高风险领域：在金融领域，我们用模拟投资场景来测试 AI 能否影响人们在复杂决策环境中的行为方式；在健康领域，我们追踪了 AI 能否影响人们对膳食补充剂的偏好。有趣的是，AI 在健康相关话题上对参与者进行有害操纵的效果最差。

我们的发现表明，在一个领域取得的成功并不能预测在另一个领域的成功，这验证了我们针对 AI 可能被滥用的特定高风险环境进行定向测试的方法。

### AI 如何进行操纵？

除了追踪效力（AI 是否成功改变了人们的想法）之外，我们还测量了它的倾向（它*尝试*使用操纵策略的频率）。我们在两种情形下测试了倾向：一种是我们明确要求模型进行操纵，另一种是我们不作要求。

如[我们的研究](https://arxiv.org/abs/2603.25326)所述，我们统计了实验记录中的操纵策略，证实 AI 模型在被明确指示进行操纵时最具操纵性。

我们的结果还表明，某些操纵策略可能更容易导致有害结果，但要详细了解这些机制仍需进一步研究。

通过同时测量效力与倾向，我们可以更好地理解 AI 操纵的运作方式，并构建更有针对性的缓解措施。

![流程图，展示评估 AI 操纵的三阶段方法论：干预前阶段（招募、测量基线态度）、干预阶段（将参与者随机分配到非 AI 基线、非显性引导或显性引导组），以及干预后阶段（测量更新后的态度、行为引导、任务后调查和事后说明流程）。](https://lh3.googleusercontent.com/BNCIGZE0BFdzXPzAMaQ2DwZ4Pcq3ZNT8m3cgcE_Cu3LsZtot_0PTLs4juKqq049iwmYQ7q4qJ57PuGzj9PPrBd4NriVqNW8e3eogbeookOMBMK12OA=w1440)

## 把研究付诸实践

随着 AI 成为日常生活的一部分，我们需要确保它不会被滥用于对人们进行有害操纵。

除了这项最新研究之外，我们最近还在前沿安全框架（Frontier Safety Framework）中引入了一个探索性的[有害操纵关键能力等级（CCL）](https://deepmind.google/blog/strengthening-our-frontier-safety-framework/)，帮助我们追踪那些可能被滥用于在人机直接互动中系统性改变信念与行为、进而造成严重伤害的模型能力。

这些评测也构成了我们测试模型（包括 Gemini 3 Pro）是否存在有害操纵的基础。你可以在[这份安全报告](https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_fsf_report.pdf)中了解更多。与我们所有的安全评测一样，这是一个持续的过程。我们将继续打磨模型与方法论，以跟上 AI 前进的步伐。

## 展望未来

理解并缓解有害操纵是一项复杂的挑战。随着模型能力的演进，我们的评测与缓解技术也必须同步演进。例如，我们目前正在探索如何在风险更高的情境中合乎伦理地评估有害操纵的效力——比如涉及根深蒂固的个人信念的讨论，此时用户可能更容易受到影响。接下来，我们将扩展研究，探究音频、视频和图像输入以及智能体化能力如何影响 AI 操纵。

我们将继续分享研究发现，并根据前沿模型论坛（Frontier Model Forum）和学术社区的反馈不断迭代。我们的目标是引领集体进步以防止有害操纵，推动 AI 模型把安全放在首位并赋能于人。

***注：*** *本研究的范围仅限于展示一般性的操纵能力，以推动有害操纵评测的科学研究。它不涉及围绕模型输出的防护措施测试，也不涉及违反政策的危险话题（如恐怖主义和儿童安全）中的操纵——这部分工作已在别处开展并单独测试。*

你还可以在[这篇访谈](https://open.substack.com/pub/aipolicyperspectives/p/ai-manipulation?utm_campaign=post-expanded-share&utm_medium=web)中阅读我们的研究人员关于有害操纵工作的更多介绍，以及 [Gemini 3 Pro 前沿安全报告](https://storage.googleapis.com/deepmind-media/gemini/gemini_3_pro_fsf_report.pdf)。

## 致谢

Canfer Akbulut、Rasmi Elasmar、Abhishek Roy、Anthony Payne、Priyanka Suresh、Lujain Ibrahim、Seliem El-Sayed、Charvi Rastogi、Ashyana Kachra、Will Hawkins、Kristian Lum、Laura Weidinger、William Isaac、Dawn Bloxwich、Lewis Ho、Eva Lu、Jenny Brennan、Mahmoud Hassan、Mark Graham
