---
title: "试点全球首个双盲 AI 评测"
title_en: "Piloting the world's first double-blind AI evaluations"
source: https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/
site: deepmind
date: 2026-08-27
crawled: 2026-09-13
translated: 2026-09-13
---

# 试点全球首个双盲 AI 评测

> 原文：[Piloting the world's first double-blind AI evaluations](https://deepmind.google/blog/piloting-the-worlds-first-double-blind-ai-evaluations/) · Google DeepMind

利用密码学安全环境，为专有模型基准测试建立信任

想象一下，一名学生即将参加一场高风险考试。如果他不小心提前看到了考试题目，那么取得满分就会受到这一知识的影响，使其成为毫无意义的成绩。要真正衡量他知道什么，他必须在参加考试之前完全看不到考题。这正是行业在评估先进 AI 模型时面临的挑战。如果模型已经见过测试题目——这一问题被称为基准污染（benchmark contamination）——那么结果只能在一定程度上被信任。

今天，我们推出**全球首个针对专有前沿级别 AI 模型的双盲评测**，它将外部评测限制在一个密码学「盒子」中，使评测内容无法在测试前被模型用于优化性能。我们正与新加坡 AI 安全研究所（Singapore AI Safety Institute）、OpenMined、AVERI 以及 [MLCommons](https://mlcommons.org/2026/08/double-blind-reliability-evaluation/) 合作，在一个[隐私保护环境](https://cloud.google.com/blog/products/identity-security/verifiable-trust-in-the-ai-era-whats-new-in-confidential-computing)中，针对机密基准测试一个 Gemini Flash Lite 模型，从而提升评测的完整性。

在 Google，我们在模型开发和部署的整个过程中使用广泛的评测来评估我们的 AI 系统，但我们并不只依赖内部测试。为了识别潜在的盲点，我们与多元化的外部合作伙伴合作，包括专业研究实验室、公民社会组织以及各国的 AI 安全与保障研究所（AI Safety and Security Institutes, AISI），利用他们独特的专长对我们的模型进行压力测试。

随着 AI 模型能力越来越强，确保模型事先没有见过测试题目或提示词至关重要，否则结果可能产生偏差。政策制定者、研究人员和企业需要相信 AI 基准测试能够准确反映模型的真实能力与安全性，但如果模型能够提前「偷看」评测题目，就可能人为抬高分数并削弱这种信任。

尽管零日志协议（zero-logging protocols）和严格的合同保障措施长期以来一直将外部测试提示词保密，但引入技术和密码学保障措施标志着安全模型评估向前迈出了重要一步。

## 双盲评测的工作原理

![一张架构图，展示「AI 拥有方」与「评测方」之间使用安全「GPU Enclave」的七步安全评测工作流。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/QIliP0rsPdITCeVJ/Double_blind_evals_diagram.svg)![一张架构图，展示「AI 拥有方」与「评测方」之间使用安全「GPU Enclave」的七步安全评测工作流。](https://storage.googleapis.com/gdm-deepmind-com-prod-public/media/original_images/QIliP0rsPdITCeVJ/Double_blind_evals_diagram_dark.svg)

一直以来，高风险的外部评测都需要一种权衡。要么评测方交出他们的测试提示词（冒着模型提供方提前看到测试题目的风险），要么模型提供方交出他们的模型权重（冒着知识产权泄露的风险）。

双盲评测消除了这种妥协。通过使用 Google Cloud [Confidential Computing](https://cloud.google.com/security/products/confidential-computing) 产品组合中的 Confidential Space，我们可以用密码学方法验证外部评测数据和专有模型分别对其各自拥有方保持私密。评测方无法看到 Gemini 模型权重，Google 也无法看到评测方的测试提示词。

## 在模型评测中建立信任的新方法

这种密码学证据有助于防止基准污染并保护敏感数据。随着模型能力的增强，这对于高度敏感的评测尤为重要，例如用于网络安全或由政府机构使用的评测。双盲评测使独立组织能够在不损害数据主权或安全性的前提下，严格测试先进模型。

我们希望这次试点能为模型监督开辟新的前沿，帮助更广泛的行业构建更安全、更可靠、被广泛信任的 AI 系统。要了解更多关于我们的方法和发现，请阅读我们的[技术报告](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/piloting-the-worlds-first-double-blind-ai-evaluations/double-blind-evaluations-technical-report.pdf)。
