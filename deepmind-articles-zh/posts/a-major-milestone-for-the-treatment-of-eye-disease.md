---
title: "眼病治疗的一项重大里程碑"
title_en: "A major milestone for the treatment of eye disease"
source: https://deepmind.google/blog/a-major-milestone-for-the-treatment-of-eye-disease/
site: deepmind
date: 2018-08-13
crawled: 2026-09-13
translated: 2026-09-13
---

# 眼病治疗的一项重大里程碑

> 原文：[A major milestone for the treatment of eye disease](https://deepmind.google/blog/a-major-milestone-for-the-treatment-of-eye-disease/) · Google DeepMind

我们高兴地宣布与 [Moorfields 眼科医院](https://deepmind.com/blog/announcements/announcing-deepmind-health-research-partnership-moorfields-eye-hospital)联合研究合作第一阶段的成果，它有可能变革威胁视力的眼病的管理方式。

这项成果在线发表于 [Nature Medicine](https://www.nature.com/articles/s41591-018-0107-6)（开放获取全文见博客末尾），表明我们的 AI 系统能够以前所未有的准确度快速解读日常临床实践中的眼部扫描影像。对于 50 多种威胁视力的眼病，它推荐患者治疗转诊方式的准确度可与世界顶级专家医生相媲美。

这些还只是早期结果，但它们表明我们的系统能够应对日常临床实践中遇到的各种各样的患者。从长远来看，我们希望这能帮助医生快速优先安排需要紧急治疗的患者——最终有望挽救视力。

## 更精简的流程

目前，眼科护理专业人员使用光学相干断层扫描（OCT）来帮助诊断眼部疾病。这些 3D 图像提供了眼球后部的精细地图，但难以读取，需要专家分析才能解读。

分析这些扫描所需的时间，加上医疗专业人员必须处理的海量扫描数量（仅 Moorfields 一家每天就超过 1,000 份），可能导致从扫描到治疗之间出现漫长的延误——即便患者需要紧急救治也是如此。如果患者突发问题，例如眼内出血，这些延误甚至可能让患者付出失去视力的代价。

我们开发的系统正是为了应对这一挑战。它不仅能在几秒钟内自动检测眼病的特征，还能通过推荐患者是否应转诊治疗，来优先安排最需要紧急救治的患者。这一即时分诊过程应能大幅缩短从扫描到治疗之间流逝的时间，帮助糖尿病眼病和年龄相关性黄斑变性的患者避免视力损失。

## 适应性强的技术

我们不希望这只是一个学术上有意思的结果——我们希望它被用于真实的治疗。因此，我们的论文还直面了 AI 在临床实践中的关键障碍之一：「黑箱」问题。对于大多数 AI 系统，很难确切理解它们为什么做出某个推荐。这对需要理解系统推理而不仅仅是输出的临床医生和患者来说是一个巨大的问题——不仅要知其然，还要知其所以然。

我们的系统以一种新颖的方式处理这一问题：将两个不同的神经网络与二者之间一个易于解释的表示相结合。第一个神经网络被称为分割网络，它分析 OCT 扫描，提供不同类型眼部组织的地图以及它所看到的疾病特征，例如出血、病灶、异常积液或其他眼病症状。这张地图让眼科护理专业人员得以洞察系统的「思考」。第二个网络被称为分类网络，它分析这张地图，向临床医生呈现诊断和转诊建议。关键在于，该网络以百分比的形式表达这一建议，使临床医生能够评估系统对其分析的置信度。

![展示当前眼病检测流程的信息图。流程从 OCT 扫描开始，由受过训练的技术人员进行分析，这需要时间，因而可能延误对需要紧急救治的患者的治疗。而 AI 可以在几秒钟内分析 OCT 图像并识别眼病特征，并将推荐结果传递给临床医生。](https://lh3.googleusercontent.com/t78mlRIzLYO2Gqv6Wvn0g1Q6loXy9-cOpcsuWGb7p1S9B8z-C8VpxfRds-NM6QjUjjCboyUfPBv5BHTnEjU9VKAKUJyL5pzzxmFJAlzBb5ZetieT5eo=w1440)

AI 如何帮助临床医生检测眼病

这一功能至关重要，因为眼科护理专业人员在决定患者接受的护理与治疗类型方面始终扮演着关键角色。让他们能够审视这项技术的建议，是让该系统在实践中可用的关键。

除此之外，我们的技术可以轻松应用于不同类型的眼部扫描仪，而不仅限于它在 Moorfields 接受训练时所用的特定设备类型。这看似无关紧要，但意味着这项技术可以相对容易地在全世界推广，大幅增加可能受益的患者数量。这也确保了即使在 OCT 扫描仪随时间升级或更换的情况下，系统仍可在医院和其他临床环境中继续使用。

## 下一阶段

虽然我们对这一进展感到无比自豪，但这项[初步研究](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/a-major-milestone-for-the-treatment-of-eye-disease/De%20Fauw%20et.%20al%20Nature%20Medicine%202018.pdf) [PDF] 还需要转化为产品，然后经过严格的临床试验和监管批准，才能投入实际使用。但我们有信心，假以时日，这套系统将变革眼病的诊断、治疗和管理。

我们在 Moorfields 的合作伙伴希望我们的研究能帮助他们改善护理、减轻临床医生的部分负担并降低成本——三者同时实现。因此，我们也在下一步工作上下了很大功夫。

如果这项技术通过临床试验被验证可普遍使用，Moorfields 的临床医生将能在其位于英国的 30 家医院和社区诊所中免费使用它，初期为期五年。这些诊所每年服务 30 万名患者，每天收到超过 1,000 份 OCT 扫描转诊——每一份都可能受益于诊断准确度和速度的提升。

我们同样自豪的是，我们在这个项目中投入的工作将帮助加速许多其他 NHS 研究工作。Moorfields 保存的原始数据集适用于临床使用，但不适用于机器学习研究。因此，我们在清理、整理和标注该数据集上投入巨大，打造了世界上最好的面向 AI 的眼科研究数据库之一。

这个改进后的数据库由 Moorfields 作为非商业性公共资产持有，目前已被医院研究人员用于九项针对各类疾病的独立研究——未来还会有更多。Moorfields 还可以将 DeepMind 训练好的 AI 模型用于其未来的非商业研究工作。

对于自 2016 年与 Moorfields 签署协议以来一直参与这项工作的我们所有人来说，这是一个极其令人振奋的里程碑，也再次证明了临床医生与技术专家携手合作所能实现的可能。随着进展，我们将持续向大家更新。

**附注**

在 Nature Medicine 上[阅读开放获取的论文全文](https://www.nature.com/articles/s41591-018-0107-6.epdf?author_access_token=PAbvHEuv_YYmrPVbG5HqKdRgN0jAjWel9jnR3ZoTv0P43NEH20hFuvBoJk6cvICihn8kmL6tmejFlnuPlbT_0KmJgK6N07SPh_ZLy0Nxb0-LAGIDBaH1fjJTkD9ahUEQpRlEudtlG9E1v3ca9xNQcQ%3D%3D)

[在此下载作者版本](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/a-major-milestone-for-the-treatment-of-eye-disease/De%20Fauw%20et.%20al%20Nature%20Medicine%202018.pdf) [PDF]
