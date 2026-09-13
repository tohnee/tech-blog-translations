---
title: "以 AI co-clinician 开启医疗健康新模式"
title_en: "Enabling a new model for healthcare with AI co-clinician"
source: https://deepmind.google/blog/ai-co-clinician/
site: deepmind
date: 2026-04-30
crawled: 2026-09-13
translated: 2026-09-13
---

# 以 AI co-clinician 开启医疗健康新模式

> 原文：[Enabling a new model for healthcare with AI co-clinician](https://deepmind.google/blog/ai-co-clinician/) · Google DeepMind

全球各地的医疗体系都在追求更好的疗效、更低的成本，以及患者和临床医生双双改善的体验。然而，进展受到全球临床专家短缺的制约——世界卫生组织预测，到 2030 年全球将短缺超过 [1000 万名](https://www.who.int/health-topics/health-workforce#tab=tab_1)医疗工作者。

虽然 AI 常被视为弥合这一差距的关键，但它尚未能充分满足临床医生和患者的需求。正因如此，今天我们宣布启动 AI co-clinician 研究计划，探索 AI 如何更好地放大医生的专业能力，为患者提供更高质量的医疗照护。

在 Google DeepMind，我们在医疗 AI 领域的旅程从用 [MedPaLM](https://www.nature.com/articles/s41586-023-06291-2) 攻克考试式的医学知识测试，到用 [AMIE](https://www.nature.com/articles/s41586-025-08866-7) 在基于文本的模拟医疗问诊中比肩医生的表现——包括在[真实世界可行性](https://arxiv.org/abs/2603.08448)试验场景中。我们还有着悠久的研究历史，探索临床医生与 AI 系统如何[协同](https://www.nature.com/articles/s41591-023-02437-x)[工作](https://www.nature.com/articles/s41586-025-08869-4)。

我们假设，医疗服务的下一步演进将呈现"三方照护"（triadic care）形态：AI 智能体在医生的执业权威之下，帮助患者走过就医旅程。医学从来都是一项团队运动，而 AI 智能体可以为场上带来更多队友：扩展临床医生的覆盖范围，同时确保他们保留判断力和控制权。

这就是我们 AI co-clinician 研究计划的基石：这一 AI 被设计为照护团队中的协作成员，在专业临床监督下与患者互动。我们在面向临床医生和面向患者两种场景中设计并评估了 AI co-clinician。兼顾这两个视角，是 AI 提升医疗服务的质量、成本、可得性与体验的关键。

![推进医疗 AI 研究，使其在协助临床医生照护患者时更值得信赖、更有帮助。](https://lh3.googleusercontent.com/vLxAt9kpWmN9_JK-NtqdapCtx4oLQxABsU8azN1YPzBYczAq0by_CC8Wxo_-Q4uAIDGaIYlOE7b-2Ccn7eWpUnT4klHP-k9f5VwayPOL7VE8bwO1=w1440)![推进医疗 AI 研究，使其在协助临床医生照护患者时更值得信赖、更有帮助。](https://lh3.googleusercontent.com/0rnwFgayHueBbnKMt6k8PHALBRnUFEhLI4e7cYFAFngDzy6TimQJQSSbLtatyN2tvrlkD6DpA_SEjV9shhWy9cDoZ47wjjtbhjaeJs-rF51LT1CpmQ=w1440)

推进医疗 AI 研究，使其在协助临床医生照护患者时更值得信赖、更有帮助。

## 用 AI co-clinician 增强临床医生的能力

对医生而言，一个工具只有在值得信赖、有事实锚定时才有用。因此，我们研究了 AI co-clinician 通过呈现高质量证据来支持临床医生的能力如何。

我们与学术医师合作，改编了"[NOHARM](https://arxiv.org/abs/2512.01241)"框架来测试我们的 AI 是否存在"犯的错误"（错误信息）和"漏的错误"（未能呈现关键信息）。

在面对面盲评中，医生们一致更偏好 AI co-clinician 的回答，胜过领先的证据合成工具。在对 98 个真实的基础医疗问题的客观分析中，我们的系统在 97 个案例中零严重错误，表现优于两种被医生广泛使用的 AI 系统。

![该研究对 98 个真实的基础医疗问题进行了盲比较，这些问题从多样化来源收集而来，随后由一组主治医师进行打磨。这一多步骤迭代过程包括全面的背景研究，以及针对每个问题开发答案评估指标，以便对临床准确性和是否符合最佳实践指南进行严格的专业评估。借助这一由专家主导的打磨阶段，该方法能够精确刻画针对具体场景、达成共识的遗漏错误与多余错误，确保评估反映真实世界临床决策的复杂性。](https://lh3.googleusercontent.com/9LvJBboLhrYPfvFvBNsFFKjHrLstUwPZnijw5DTKxeq4V7ywOuphVgQ-SsUnVrkYZUd2lfilYmq3ar0j5kRwK5RnHdM4WW3hQM2QPNS9xeXAHH04EA=w1440)![该研究对 98 个真实的基础医疗问题进行了盲比较，这些问题从多样化来源收集而来，随后由一组主治医师进行打磨。这一多步骤迭代过程包括全面的背景研究，以及针对每个问题开发答案评估指标，以便对临床准确性和是否符合最佳实践指南进行严格的专业评估。借助这一由专家主导的打磨阶段，该方法能够精确刻画针对具体场景、达成共识的遗漏错误与多余错误，确保评估反映真实世界临床决策的复杂性。](https://lh3.googleusercontent.com/eV_oh4BspI5sTemDMURYAexvb4RR_pWhDarbE_mNxiu44u6JAcFuysKWc0-PzRhtZIvmCbSzyPDjuD08M6UNQ1YAEu-vbds8rBRcE47scxA2Z4cZPQw=w1440)

该研究对 98 个真实的基础医疗问题进行了盲比较，这些问题从多样化来源收集而来，随后由一组主治医师进行打磨。这一多步骤迭代过程包括全面的背景研究，以及针对每个问题开发答案评估指标，以便对临床准确性和是否符合最佳实践指南进行严格的专业评估。借助这一由专家主导的打磨阶段，该方法能够精确刻画针对具体场景、达成共识的遗漏错误与多余错误，确保评估反映真实世界临床决策的复杂性。

除了可靠的临床证据合成之外，AI 系统在回答药物与治疗干预相关问题时，还应达到医生所要求的精确度。这对 AI 是一项困难的任务，却仍未被充分探索。为弥补这一缺口，我们在 [OpenFDA 版 RxQA](https://arxiv.org/abs/2503.06074) 问题上评估了 AI co-clinician——这是一个旨在考察复杂药物知识与推理的富有挑战性的基准测试。我们在应对这些测试方面看到了显著进展，超越了其他前沿 AI 系统，尤其是当问题以真实照护中的开放式提问方式提出时。这些发现凸显了先进 AI 的潜力：当临床医生应对日益数据密集的医疗规划与管理要求时，它能提供有益的协助。

![RxQA 最初以多选题（MCQ）测试的形式提出，即使是基础医疗医生得分也仅属中等。虽然我们的结果显示各 AI 系统在公开可得的（OpenFDA）RxQA 集上的 MCQ 表现有显著提升，但临床医生在真实世界中的需求以开放式问题的形式呈现，而不是要从预设选项中挑出正确答案。在"针对药物的开放式问答"这一更贴近现实的临床任务上，AI co-clinician 优于现有前沿模型。综合来看，这些结果表明 AI 可以在临床推理的这些方面比肩人类医师的熟练程度，同时仍有进一步提升的空间。](https://lh3.googleusercontent.com/jSXmRbnKcAyrA6-8PkN4Mc7M0MRGIoy7f26f5Xh6VW1lIBcxDfJfGborwpp3J6K3wa_TOvdrd-_MxzX0GwxfdBQ_fgDj4s5l2Yby8CnBYnA61zN9-Gw=w1440)![RxQA 最初以多选题（MCQ）测试的形式提出，即使是基础医疗医生得分也仅属中等。虽然我们的结果显示各 AI 系统在公开可得的（OpenFDA）RxQA 集上的 MCQ 表现有显著提升，但临床医生在真实世界中的需求以开放式问题的形式呈现，而不是要从预设选项中挑出正确答案。在"针对药物的开放式问答"这一更贴近现实的临床任务上，AI co-clinician 优于现有前沿模型。综合来看，这些结果表明 AI 可以在临床推理的这些方面比肩人类医师的熟练程度，同时仍有进一步提升的空间。](https://lh3.googleusercontent.com/SAhM0LNrq7XsML50gD-PGYCKzk_3n7Fhh9kGZohJkPqotKzECEl8KzVmQ5uSTRGFpJai_ZvBC3wE7pZ1sqzZzxEknYxYtqpC6ap35m0XJ54meD4X=w1440)

RxQA 最初以多选题（MCQ）测试的形式提出，即使是基础医疗医生得分也仅属中等。虽然我们的结果显示各 AI 系统在公开可得的（OpenFDA）RxQA 集上的 MCQ 表现有显著提升，但临床医生在真实世界中的需求以开放式问题的形式呈现，而不是要从预设选项中挑出正确答案。在"针对药物的开放式问答"这一更贴近现实的临床任务上，AI co-clinician 优于现有前沿模型。综合来看，这些结果表明 AI 可以在临床推理的这些方面比肩人类医师的熟练程度，同时仍有进一步提升的空间。

## 研究 AI co-clinician 在远程医疗场景中的实时多模态能力

除了辅助临床医生的场景之外，我们还在研究 AI co-clinician 在面向患者的研究场景中的表现。专业的临床评估历来包括细微的视觉和听觉线索，例如观察患者的步态、呼吸模式的细微差别，或皮肤变化的外观。虽然此前的研究（包括我们与 [Beth Israel Deaconess 医疗中心](https://research.google/blog/exploring-the-feasibility-of-conversational-diagnostic-ai-in-a-real-world-clinical-study/)的合作）证明了 AI 文本对话在就诊前的价值，但把交互限制在文本从根本上限制了 AI 的临床价值。医学不只是文本；它需要眼睛、耳朵和声音。

这就是为什么我们正在探索实时多模态 AI 作为照护团队辅助环节的潜力。基于 [Gemini](https://deepmind.google/models/gemini/pro/) 和 [Project Astra](https://deepmind.google/models/project-astra/) 的能力，我们测试了 AI co-clinician 使用实时音频和视频与患者互动的能力，模拟了未来有能力支持更好的诊断与管理的 AI 在专家监督下进行远程医疗通话的场景。关于我们方法与结果的更多细节，请参阅我们的技术报告："[Towards Conversational Medical AI with Eyes, Ears and a Voice](https://www.gstatic.com/vesper/ai_coclinician_technical_report.pdf)"。

我们与哈佛和斯坦福的学术医师合作，设计了一项随机模拟研究，包含 20 个合成的临床场景和 10 名扮演"标准化病人"的医生。该智能体展示了超越纯文本系统的全新能力，例如实时指导患者完成复杂的体格检查。例如，它成功纠正了一名患者的吸入器使用方法，并指导肩部手法检查以识别肩袖损伤。

虽然关于 AI 能否匹敌或超越人类临床表现的讨论很多，但这些高保真模拟更严格地检验了这一前提。我们评估了问诊技能的 140 多个方面，发现专家医生的整体表现优于该 AI 系统，尤其是在识别"危险信号"和指导关键体格检查方面。这一发现表明，这些系统目前最适合作为执业者的辅助工具，而非临床判断的替代品。与此同时，我们的工作也凸显了 AI 能力的重大进步：在 140 个评估领域中，AI co-clinician 有 68 个领域的表现达到或超过基础医疗医生（PCP）的水平。这些结果凸显了广阔的前景，并标示出进一步研究最能切实推进医疗 AI 的具体方向。

![一项随机、界面盲法、交叉设计的模拟研究结果，涉及由真实基础医疗医生、AI co-clinician 或 GPT-realtime 执行的 120 次假设性远程医疗问诊。评估中由一组内科住院医师扮演标准化病人，演绎 20 个标准化的门诊场景。这些场景涵盖一系列临床状况，经过专门设计，要求进行主动的听觉与视觉推理。针对场景定制的标准从七个维度评估问诊质量，每一项均采用锚定的 0–2 评分，以区分遗漏、部分完成和完全恰当的表现。误差线对应 95% 置信区间。](https://lh3.googleusercontent.com/16STUlrYSIGJX5sseNvEJeGSoIhkZflOFInB930bunecCACV3Kedta4Y8dsZxI73oDT5DM1wTRyDF8R_s__6e5GGPn4T9wpXuV2vW7DKeNJWGZeU=w1440)![一项随机、界面盲法、交叉设计的模拟研究结果，涉及由真实基础医疗医生、AI co-clinician 或 GPT-realtime 执行的 120 次假设性远程医疗问诊。评估中由一组内科住院医师扮演标准化病人，演绎 20 个标准化的门诊场景。这些场景涵盖一系列临床状况，经过专门设计，要求进行主动的听觉与视觉推理。针对场景定制的标准从七个维度评估问诊质量，每一项均采用锚定的 0–2 评分，以区分遗漏、部分完成和完全恰当的表现。误差线对应 95% 置信区间。](https://lh3.googleusercontent.com/JuYBusE84dqtTx57RtDsi7_U2ASDi4Dg3i5HurLZRfsbZNTPbyxPJoF5-rA5P7CY7sLJSk-nAQNSTBZnUSNhX8838J_G71pTaLUJ0xphNuar-BxF=w1440)

一项随机、界面盲法、交叉设计的模拟研究结果，涉及由真实基础医疗医生、AI co-clinician 或 GPT-realtime 执行的 120 次假设性远程医疗问诊。评估中由一组内科住院医师扮演标准化病人，演绎 20 个标准化的门诊场景。这些场景涵盖一系列临床状况，经过专门设计，要求进行主动的听觉与视觉推理。针对场景定制的标准从七个维度评估问诊质量，每一项均采用锚定的 0–2 评分，以区分遗漏、部分完成和完全恰当的表现。误差线对应 95% 置信区间。

下面你可以看到研究团队在这个远程医疗场景中扮演假设性患者与 AI co-clinician 互动的视频，展示了该系统的潜在能力与局限。

第 1 页，共 3 页

![](https://lh3.googleusercontent.com/SEW3vIThALZb_WupI7O5Z7ULu1f5EadPoJd31VNYk29wtqWcOnUltIah_1G-0rmmCeCWMEnzaRumHp5k-k3N4FXNK_INsAIJZ1GNdCnqmaRK4v0DaA=w1440-h810-n-nu)

这些视频仅用于研究目的，不涉及真实患者。我们分享它们是为了展示这项技术当下的能力与局限。我们最初的研究合作不涉及视频所示的能力，这些能力不用于疾病的诊断、治愈、缓解、治疗或预防，也不用于提供医疗建议。

![](https://lh3.googleusercontent.com/kY9cF88fsAhEQ8GFr0b-alW9T34EFTMYns1mAPyAhUMDQqpR4Wz5mtwukcrpw-_Fe6virZx5uY_5r089ZICcV5PL4KMn-F8v1iX9FLbncG8WW7IE=w1440-h810-n-nu)

这些视频仅用于研究目的，不涉及真实患者。我们分享它们是为了展示这项技术当下的能力与局限。我们最初的研究合作不涉及视频所示的能力，这些能力不用于疾病的诊断、治愈、缓解、治疗或预防，也不用于提供医疗建议。

![](https://lh3.googleusercontent.com/Hh0h8YQG74o9YxtJQjyv3A9SDrFl4qyPu2zT6KBR9WyRU52RXedKRBkyBTIaDKwVIPyqVrUajOJ2PldYe_E0ZISJnmGp_XDnCIG_yDoug-4f3PNbXnA=w1440-h810-n-nu)

这些视频仅用于研究目的，不涉及真实患者。我们分享它们是为了展示这项技术当下的能力与局限。我们最初的研究合作不涉及视频所示的能力，这些能力不用于疾病的诊断、治愈、缓解、治疗或预防，也不用于提供医疗建议。

## 用防护措施打造临床级 AI 的信任

将 AI 迁移并部署到临床环境，需要毫不妥协的架构与运营防护措施。在我们面向患者的远程医疗对话模拟研究中，AI co-clinician 采用双智能体架构：一个"规划者"（Planner）模块持续监控对话，验证"说话者"（Talker）智能体始终处于安全的临床边界之内。

同样，为满足医生的需求，AI co-clinician 优先使用临床级证据，对检索内容进行验证与引文核查。上文报告的评估由医生设计，用以反映他们现实世界中多样化的证据需求，通过假设场景构造问题，以严格评估 AI 的能力。

## 开展研究合作，对 AI co-clinician 进行严格的真实世界评估

为了进一步开发和评估 AI co-clinician，我们目前正与学术和研究合作伙伴一起推进分阶段的方法，覆盖全球多样化的医疗环境，包括美国、印度、澳大利亚、新西兰、新加坡和阿联酋。

随着我们逐步推进这些评估阶段，我们将在更多地区深化研究，包括使命契合的医疗组织和学术医学中心。我们的目标是确保医疗 AI 按照适用标准负责任地开发和部署，支持全球范围内的更好健康。

*注意：在现阶段，我们的研究合作不用于疾病的诊断、治愈、缓解、治疗或预防，也不用于提供医疗建议。*

## 致谢

我们感谢哈佛医学院和斯坦福医学部的研究合作伙伴，以及与我们团队一起开展进一步可信测试者评估的众多医学中心和照护组织。本项目与 Google DeepMind、Google Research、Google Cloud 和 Google for Health 的许多团队合作完成，我们感谢队友们富有洞见的讨论与贡献。

特别要指出的是，如果没有以下核心研究与工程工作，AI co-clinician 不可能实现：Aniruddh Raghu, Arthur Chen, Charlie Taylor, CJ Park, David Stutz, Devora Berlowitz, Doug Fritz, Dylan Slack, Eliseo Papa, Jack Chen, JD Velasquez, Jing Rong Lim, Katya Tregubova, Kelvin Guu, Meet Shah, Richard Green, Ryutaro Tanno, Sukhdeep Singh, Victoria Johnston, Adam Rodman。

我们感谢众多合作者的宝贵贡献，包括 Ali Eslami, Aliya Rysbeck, Andy Song, Anil Palepu, Anna Cupani, Bakul Patel, Bibo Xu, Brett Hatfield, David Wu, Ed Chi, Emma Cooney, Erica Oppenheimer, Erwan Rolland, Euan A. Ashley, Francesca Pietra, Rebeca Santamaria-Fernadez, Gordon Turner, Gregory Wayne, Hannah Gladman, Irene Teinemaa, Jack O'Sullivan, Jacob Koshy, Jan Freyberg, Jason Gusdorf, Joelle Wilson, Katherine Tong, Juraj Gottweis, Michael Howell, Mili Sanwalka, Pavel Dubov, Pete Clardy, Peter Brodeur, Rachelle Sico, SiWai Man, Sumanth Dahathri, Taylan Cemgil, Tim Strother, Uchechi Okereke, Valentin Lievin, Vishnu Ravi, Yana Lunts, Yun Liu, Simon Staffell, Rachel Teo, Adriana Fernandez Lara, Armin Senoner, Danielle Breen, Paula Tesch, Leen Verburgh, Dimple Vijaykumar, Juanita Bawagan, Muinat Abdul, Mariana Montes 和 Rob Ashley。功能视频由 Christopher Godfree、Matt Mager、Emma Moxhay 和 Simon Waldron 制作。

感谢 James Manyika 和 Demis Hassabis（德米斯·哈萨比斯）在整个研究过程中富有洞见的指导与支持。
