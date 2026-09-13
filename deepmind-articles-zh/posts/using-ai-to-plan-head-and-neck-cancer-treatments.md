---
title: "用 AI 规划头颈癌治疗方案"
title_en: "Using AI to plan head and neck cancer treatments"
source: https://deepmind.google/blog/using-ai-to-plan-head-and-neck-cancer-treatments/
site: deepmind
date: 2018-09-13
crawled: 2026-09-13
translated: 2026-09-13
---

# 用 AI 规划头颈癌治疗方案

> 原文：[Using AI to plan head and neck cancer treatments](https://deepmind.google/blog/using-ai-to-plan-head-and-neck-cancer-treatments/) · Google DeepMind

我们与[伦敦大学学院医院 NHS 基金会信托放射治疗科](https://deepmind.com/blog/applying-machine-learning-radiotherapy-planning-head-neck-cancer/)合作的[早期结果](https://arxiv.org/abs/1809.04430)表明，我们正在顺利开发一个人工智能（AI）系统，它能够以与专家临床医生相近的标准来分析和分割头颈癌的医学扫描影像。这一分割过程是规划放射治疗时必不可少却耗时的步骤。[研究结果](https://arxiv.org/abs/1809.04430)还显示，我们的系统能够在极短的时间内完成这一过程。

## 加速分割流程

全世界每年有超过 50 万人被诊断出患有头颈癌。放射治疗是治疗的关键环节，但临床工作人员必须进行细致的规划，以免健康组织受到辐射损伤：这一过程需要放射技师、肿瘤学家和/或剂量师手动勾画需要放疗的解剖区域，以及应当避开的区域。

虽然我们的工作仍处于早期阶段，但我们希望它有朝一日能够缩短从诊断到治疗之间的等待时间，这有可能改善癌症患者的治疗效果。我们还希望，精确的自动分割能够加速[自适应放射治疗流程](http://www.christie.nhs.uk/patients-and-visitors/your-treatment-and-care/treatments/radiotherapy/what-we-do/adaptive-radiotherapy/)——即随着肿瘤缩小而调整放射治疗方案——尽管还需要更多工作来研究这在实践中如何运作。

除了改变患者的生活，这项研究还可以为治疗他们的临床医生腾出时间，意味着他们能把更多时间用于患者护理、教育和研究。

## 将研究应用于临床环境

我们已采取措施确保我们的工作具有临床可用性。这包括开发了一种[新的性能指标](https://github.com/deepmind/surface-distance)用于评估模型性能——我们相信它能更好地代表临床流程——以及一个测试集，其中包含对模型此前从未见过的部位的扫描所做的新[高质量分割](https://github.com/deepmind/tcia-ct-scan-dataset)，以展示泛化能力。这两项都已向研究界开源。但要让我们的系统对真实确诊癌症的患者产生影响，我们需要扩展它，并证明它在真实的临床环境中有效。

这就是为什么我们期待与 UCLH 合作进入下一阶段的工作，我们将探索对这些 AI 算法开展人类评估，以检验它们在临床环境中的表现。

在 DeepMind Health，我们认为与社区中的其他人分享我们的工作十分重要。因此，DeepMind Health 高级研究科学家 Olaf Ronneberger 教授将于本周日在世界顶级医学影像会议 [MICCAI](https://www.miccai2018.org/en/) 上展示这些初步发现。

我们始终相信，先进技术能够并且应当帮助改变生活，我们对这个项目的下一步充满期待。随着进展，我们将持续向大家更新。
