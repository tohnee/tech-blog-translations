---
title: "构建医疗超级智能"
title_en: "Building Medical Superintelligence"
source: https://microsoft.ai/news/building-medical-superintelligence/
site: microsoft
date: 2026-10-22
crawled: 2026-10-26
translated: 2026-10-26
---

# 构建医疗超级智能

> 原文：[Building Medical Superintelligence](https://microsoft.ai/news/building-medical-superintelligence/) · Microsoft AI

如果 AI 能够帮助临床医生一步步完成复杂的医学诊断，以更低的成本、更少的医学检查，达到更高的准确率，会怎样？

这一未来正在到来。在美国急诊科的常见就诊病例上，我们的 AI 诊断系统 MAI-DxO 基于 MIMIC-IV-ED 病例进行评估时，准确率达到医生的 1.7 倍。

而在发表于《新英格兰医学杂志》（*The New England Journal of Medicine*）的医学最难病例上，MAI-DxO 的准确率是借助教科书和互联网进行诊断的医生的两倍以上；当医生不使用这些资源时，则接近四倍。同时，它还能以一半甚至三分之一的成本做到这一点——用更少的检查和操作得到正确诊断。

我们的研究成果今日发表于 *[Science](https://www.science.org/doi/10.1126/science.aeh7930)*。

想进一步了解我们对医疗超级智能的愿景，可阅读本周同期发表于 [*BMJ Digital Health and AI*](https://bmjdigitalhealth.bmj.com/content/2/1/e000395) 的文章。

<!-- 内嵌交互式报告 iframe（base64 编码的独立 HTML，第 1 份），已从归档剥离 -->


## **重新思考 AI 的构建与测试方式**

AI 有潜力变革健康与医疗保健领域，而且进展正在迅速加快。当下的挑战在于：如何构建并严格评估 AI 系统，使其临床推理能力的进步转化为切实的影响。

今天的论文[在早期工作的基础上](https://microsoft.ai/news/the-path-to-medical-superintelligence/)，为这一转变引入了两个基石：序贯诊断基准（Sequential Diagnosis Benchmark，SDBench），用于测试逐步展开的诊断推理；以及微软 AI 诊断编排器（Microsoft AI Diagnostic Orchestrator，MAI-DxO），即我们在该基准上表现最优的 AI 系统。

美国医师执照考试（USMLE）等医学执照考试的设计目的是评估医生的知识水平，而非临床诊断的现实过程。在这类考试中，所有信息一次性给出，考生只需从中选出一个答案；而在实践中，临床医生必须逐步拼凑出完整的病情图景：决定问什么、开哪些检查，以及每一项新发现会如何改变最可能的诊断。这类考试已成为评估医疗 AI 表现的常用基准。

这正是我们开发 SDBench 的原因。它在两组互补的病例集上评估性能：304 个取自《新英格兰医学杂志》（NEJM）病例报告的复杂病例，以及一组来自 MIMIC-IV-ED 的更典型的急诊科就诊病例。每个病例都构成一个交互式病例，AI 模型和/或医生从有限的信息出发，自行选择下一步要获取什么。该基准衡量诊断准确率、请求的证据和估计的检查成本——既评估答案，也评估所走的路径。

我们构建了 MAI-DxO，并在 SDBench 内对其进行测试。它并不依赖单一模型即刻给出答案，而是像一个虚拟医生会诊小组那样运作：每位“医生”提出诊断假设、挑选有用的问题或检查，并对正在形成的观点提出质疑。MAI-DxO 在多轮辩论中协调这一交流，随着证据到来不断更新评估，并权衡每项检查的可能价值与其成本。

**我们的发现：**

- 在复杂的 NEJM 病例上，MAI-DxO 取得了 83% 的诊断准确率。医生在不使用外部参考资料时为 22%，使用时为 36%，即 MAI-DxO 的准确率分别约为 3.7 倍和 2.3 倍。
- 在来自 MIMIC-IV-ED 的更典型的急诊科病例上，MAI-DxO 取得 80% 的准确率，医生为 47%——是医生的 1.7 倍以上。
- 当针对成本进行更深度优化时，MAI-DxO 的性能依然强劲，同时会选择更具成本效益的检查方案。在 NEJM 病例上，一种配置以不到对比系统一半的成本达到了 81% 的准确率。
- 在两个数据集上，没有任何其他人类或 AI 方法能同时做到比 MAI-DxO 更准确且成本更低。
- 当我们使用包括 GPT-5.5 在内的新模型、且不改变编排方法重复这一评估时，这些优势得以保持——甚至有所提升，这表明该方法并不局限于某一代模型。

我们正在开源部分 NEJM 病例的 SDBench——包括基准本身、Gatekeeper、Judge 以及成本估算代码——以便研究人员复现这一评估、测试其他模型，并对研究发现进行挑战或扩展。

[探索 SDBench](https://microsoft.github.io/sdbench)

<!-- 内嵌交互式报告 iframe（base64 编码的独立 HTML，第 2 份），已从归档剥离 -->


<!-- 内嵌交互式报告 iframe（base64 编码的独立 HTML，第 3 份），已从归档剥离 -->


## **从更好的诊断到更好的诊疗**

诊断只是诊疗旅程的一部分。更好的诊疗还要求紧跟医学知识的进展、选择正确的治疗方案、理解病情随时间的变化，并支持体现个人价值观与医疗可及性的选择。机遇在于把这些能力整合为一种今天尚未广泛普及的医疗标准。在发表于 [*BMJ Digital Health and AI*](https://bmjdigitalhealth.bmj.com/content/2/1/e000395) 的《医疗超级智能的基石》（*The Building Blocks of Medical Superintelligence*）一文中，我们探讨了 AI 要支撑这一更宏大的愿景需要什么——并最终超越当今最强临床团队与医疗体系的能力。

序贯诊断提供了一个早期范例：AI 医生相互协作、质疑假设，并随着证据的出现不断完善各自的临床推理。我们的雄心是构建能够连接诊疗旅程中的知识、情境与决策的 AI——而不是仅仅在某一临床任务上表现出色。通过与[梅奥诊所（Mayo Clinic）](https://news.microsoft.com/source/2026/06/02/mayo-clinic-and-microsoft-collaborate-to-develop-a-frontier-ai-model-for-healthcare/)的合作，我们旨在将前沿 AI、临床专业知识与纵向多模态数据结合起来，构建能够应对真实世界诊疗复杂性与多样性的系统。

## **在真实世界中测试**

基准测试固然重要，但真正的检验在于真实临床环境中的表现。通过与波士顿**贝斯以色列女执事医疗中心（Beth Israel Deaconess Medical Center）**建立新的合作，我们将在不同的医院场景中评估临床推理能力。在一项前瞻性研究中，患者将直接与系统交互，其表现将与医生的独立评估进行对照。与临床团队并肩工作，将揭示这项技术在哪些方面奏效、在哪些方面不足，以及如何融入繁忙的工作流程。

## **微软的医疗健康事业**

医疗 AI 的快速进展正在为患者和临床医生打开新的可能。为了将这一进展转化为实际影响，我们正在把微软内部各地的医疗健康团队——包括微软研究院（Microsoft Research）的科学家以及 Dragon Copilot、PowerScribe 等产品背后的团队——汇聚为 Microsoft AI 之内的一项整体性事业。通过协同工作，我们将加速交付值得信赖的 AI 系统，推动更好的临床结局与就医体验。

## 与我们共创未来

我们是一个精干、行动迅速的实验室，汇聚了世界上最顶尖的一些人才。在 MAI，我们拥有一张令人兴奋的算力路线图，正在快速而广泛地扩张。我们还肩负着一个我们真心信仰的宏大使命。我们同样有幸与出色的产品团队合作，让我们的模型有机会触达数十亿用户、创造巨大的积极影响。如果你才华横溢、志向远大又不失谦逊，你会在这里如鱼得水——快来加入我们，一起打造下一代模型吧！

[查看全部职位](/careers/#join-the-team)

## 更多故事

![一幅色彩斑斓的绘画风格插图：一个人手持手机注视屏幕，周围漂浮着心形和聊天图标，暗示他们正在使用社交媒体或收发消息。背景充满鲜活的形状。](https://microsoft.ai/wp-content/uploads/2026/03/0_0-1-2-1.jpg)

[### 健康检查：人们如何将 Copilot 用于健康](https://microsoft.ai/news/health-check-how-people-use-copilot-for-health/)

健康

![一幅朦胧而鲜活的风景图：五彩缤纷的野花田，背景是起伏的绿色山丘，上方是柔和的蓝天。](https://microsoft.ai/wp-content/uploads/2026/06/Group-2147234768.png)
