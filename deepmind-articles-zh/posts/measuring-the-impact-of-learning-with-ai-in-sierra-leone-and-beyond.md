---
title: "衡量在塞拉利昂及其他地区用 AI 学习的影响"
title_en: "Measuring the impact of learning with AI in Sierra Leone and beyond"
source: https://deepmind.google/blog/measuring-the-impact-of-learning-with-ai-in-sierra-leone-and-beyond/
site: deepmind
date: 2026-06-09
crawled: 2026-09-13
translated: 2026-09-13
---

# 衡量在塞拉利昂及其他地区用 AI 学习的影响

> 原文：[Measuring the impact of learning with AI in Sierra Leone and beyond](https://deepmind.google/blog/measuring-the-impact-of-learning-with-ai-in-sierra-leone-and-beyond/) · Google DeepMind

今天，我们分享一项随机对照试验（RCT）的[结果与技术报告](https://storage.googleapis.com/deepmind-media/LearnLM/learnLM_sierraleone_may26.pdf)，该试验与 [Fab AI](https://www.fab-ai.org/) 合作开展，并得到塞拉利昂教育部的支持¹。在八周时间里，我们评估了 Gemini 中的 [Guided Learning](https://blog.google/products-and-platforms/products/education/guided-learning/) 如何影响塞拉利昂 Port Loko 地区 12 所学校 1,763 名初中生的数学学习进展。

> 我们期望创新并改善服务交付，但我们也必须严格研究创新的结果……因此，我感到高兴的是，我们现在拥有强有力的证据，表明精心设计的 AI 可以帮助改善学习成果，支持我们众多辛勤工作的教师。

Conrad Sackey

塞拉利昂基础与中级教育部长

这项预先注册试验的结果表明，AI 可以成为强大的教学伙伴——不是取代教师，而是扩展他们的触达范围。这项研究是我们[持续努力](https://blog.google/products-and-platforms/products/education/measuring-the-impact-of-ai-on-teaching-and-learning/)的一部分，即为 AI 对教与学的影响建立全球证据基础。

## 超越答案引擎：保护批判性思维

一个常见的担忧是，生成式 AI 可能成为学生的捷径，让他们绕过深度学习所必需的、具有挑战性却不可或缺的认知努力。[Guided Learning](https://blog.google/products-and-platforms/products/education/guided-learning/) 正是为解决这一担忧而设计：它建立在我们 [LearnLM](http://goo.gle/learnlm) 工作多年的研究和实践之上，以教学法为根基，并经过专门调优，优先帮助构建理解而非直接提供答案。

来自塞拉利昂的数据表明这一方法是有效的。对我们试验期间交换的超过 11.3 万次交互的分析显示，91.4% 的对话中，学生使用该工具来构建概念理解，而不是简单地寻求答案。Gemini 的回应是，在其 76% 的消息中提出脚手架式（scaffolding）问题，仅在 2% 的情况下提供直接解答。这种「苏格拉底式」交互确保认知上的重活仍由学生自己承担。

## 以教师为主导的干预

这次试验的成功建立在 AI 与教育者的伙伴关系之上，教师始终牢牢居于体验的中心。教育者设计课程、设定目标，并主持推动学习的课堂讨论。

在焦点小组访谈中，教师们报告说 Gemini 也促进了他们自身的专业成长。通过使用该工具备课，他们发现了讲解分数等熟悉主题的新方法。许多人描述了一种从「讲授者」到「促进者」的转变——在教室中走动，支持一对对学生走过各自的学习旅程。

为了帮助其他人实施类似项目，我们正在发布一份[教师培训指南](https://goo.gle/LearnLM-SierraLeone-Teacher-Training)，其中包含与 Fab AI 合作创建的材料，以及本研究使用的具体操作规程。

## 衡量影响

定量结果十分显著。与对照组相比，使用 Guided Learning 的学生数学成绩提升了 +0.258 个标准差。从实际角度来说，这相当于在八周试验期内取得了约 1.2 至 1.7 年的典型学习进展。

在那些教师将 Gemini 融入约一半课时、在试验期间达到 12 小时使用目标的课堂中，学生的提升更高——约相当于 1.8 至 2.5 年的学习进展。参与度也异常高：69% 的学生达到或超过了使用目标，远超自愿使用教育技术通常仅有的 5%（即著名的[「5% 问题」](https://www.educationnext.org/5-percent-problem-online-mathematics-programs-may-benefit-most-kids-who-need-it-least/)）。这意味着学生不仅投入了学习，而且更喜欢来上课了。

除了数字之外，我们还看到了行为上的深刻转变。学生们报告说更享受数学了，并在常规教学之外主动投入学习。至关重要的是，随着时间推移，他们的对话和提问变得更加以学习为导向，从寻求直接解答转向技能构建。具体来说，到最后一周，技能构建类查询上升到 90%——高于第一周的 68%——而求答案类问题从 25% 下降到 10%，证明学生不只是想要答案，而是想理解自己是如何得出答案的。

为了进一步理解 Guided Learning 对学生学习的影响，我们正在全球范围内开展一系列额外的预先注册 RCT。本着推进开放科学、及时传播洞察的精神，我们还将发布一份与 Fab AI 合作的、关于我们 RCT 方法的[实操手册](https://goo.gle/LearnLM-SierraLeone-Playbook)，帮助其他人以贴合自身需求与情境的方式开展更快、可扩展的研究——以获得与技术进步同步的、稳健的本地化证据。随着后续 RCT 的完成，我们将继续发布结果与经验，构建更全面的跨国证据基础，希望能为整个学习生态中负责任的 AI 开发提供参考。此外，我们对[全球 AI for Learning 联盟（GAILA）](https://www.globalaiforlearningalliance.org/)的支持将通过集体行动加速这些承诺及其他工作。

## 前方的路

尽管这些结果令人鼓舞，它们也凸显了「成就差距」的挑战。虽然大多数学生都从中受益，但那些入学时数学基础更强的学生受益最大。这凸显了一个重要需求：提供能为最需要帮助的学生带来最大收益的工具。

展望未来，我们计划将这些试验扩展到其他国家，并更深入地探究元认知（metacognition）和关系智能（relational intelligence）等领域，以获得更全面的视角，探索学习中的细微复杂性。通过将教师主导课堂的关系基础与 AI 个性化、脚手架式的能力相结合，我们可以帮助确保技术成为通向人人可及的、有意义的学习机会的桥梁。

---

1 我们还获得了 Google.org 和盖茨基金会对本次试验的支持。[EducAid](https://www.educaid.org.uk/)、[Laterite](https://www.laterite.com/) 和 [Oxford MeasurEd](https://www.oxfordmeasured.co.uk/) 也与我们展开了合作。
