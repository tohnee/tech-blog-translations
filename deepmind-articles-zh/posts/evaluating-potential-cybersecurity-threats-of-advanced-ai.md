---
title: "评估先进 AI 的潜在网络安全威胁"
title_en: "Evaluating potential cybersecurity threats of advanced AI"
source: https://deepmind.google/blog/evaluating-potential-cybersecurity-threats-of-advanced-ai/
site: deepmind
date: 2025-04-02
crawled: 2026-09-13
translated: 2026-09-13
---

# 评估先进 AI 的潜在网络安全威胁

> 原文：[Evaluating potential cybersecurity threats of advanced AI](https://deepmind.google/blog/evaluating-potential-cybersecurity-threats-of-advanced-ai/) · Google DeepMind

人工智能（AI）长期以来一直是网络安全的基石。从恶意软件检测到网络流量分析，预测性机器学习模型和其他狭义 AI 应用已在网络安全领域使用了几十年。随着我们越来越接近通用人工智能（AGI），AI 自动化防御、修复漏洞的潜力将变得更加强大。

但要收获这些收益，我们也必须理解并缓解日益先进的 AI 被[滥用](https://cloud.google.com/blog/topics/threat-intelligence/adversarial-misuse-generative-ai)以发动或增强网络攻击的风险。我们新的[评估 AI 新兴网络攻击能力](https://arxiv.org/abs/2503.11917)的框架，正是为此而设计。它是迄今同类评估中最全面的一次：它覆盖网络攻击链的每一个阶段，涉及广泛的威胁类型，并以真实世界数据为基础。

我们的框架使网络安全专家能够在恶意行为者利用 AI 发动复杂网络攻击之前，识别哪些防御是必要的，以及如何为它们排定优先级。

## 构建一个全面的基准测试

我们更新后的[前沿安全框架](https://deepmind.google/discover/blog/updating-the-frontier-safety-framework/)承认，先进的 AI 模型可能使网络攻击自动化并加速其进程，有可能降低攻击者的成本。这反过来又提高了攻击以更大规模开展的风险。

为了走在 AI 驱动网络攻击这一新兴威胁的前面，我们改编了久经考验的网络安全评估框架，例如 [MITRE ATT&CK](https://attack.mitre.org/)。这些框架使我们能够跨越端到端的网络攻击链评估威胁——从侦察到在目标上采取行动——并覆盖一系列可能的攻击场景。然而，这些既定框架在设计时并未考虑攻击者利用 AI 入侵系统的情况。我们的方法通过主动识别 AI 可能在哪里使攻击更快、更便宜或更容易——例如实现完全自动化的网络攻击——来填补这一空白。

我们分析了发生在 20 个国家的超过 12,000 次在网络攻击中使用 AI 的真实尝试，数据来自 [Google 威胁情报小组](https://cloud.google.com/blog/topics/threat-intelligence/adversarial-misuse-generative-ai)。这帮助我们识别出这些攻击展开过程中的常见模式。在此基础上，我们整理了七类典型的攻击类别——包括钓鱼、恶意软件和拒绝服务攻击——并识别出网络攻击链上的关键瓶颈阶段，在这些阶段 AI 可能显著改变攻击的传统成本。把评估聚焦在这些瓶颈上，防御者可以更有效地为安全资源排定优先级。

![一张描绘网络攻击链各阶段的示意图，用图标和符号表示每个阶段](https://lh3.googleusercontent.com/ms4heyXxh-WiYVfB5O7GH-d6RBqd_uCnSc6wfAt73snLHESG-i7RarLdiRFY80AAWNGdzI3PO6gombXFDxwXIRI99iTJ38wIqzWScUU3M0fhGu2A=w1440)

网络攻击链的各个阶段

最后，我们创建了一个网络攻击能力基准测试，用于全面评估前沿 AI 模型在网络安全方面的强项与弱项。我们的基准测试由 50 个挑战组成，覆盖整个攻击链，包括情报收集、漏洞利用和恶意软件开发等领域。我们的目标是让防御者能够制定有针对性的缓解措施，并把模拟 AI 驱动的攻击作为红队测试演练的一部分。

## 早期评估的洞见

我们使用这一基准测试开展的初步评估表明，孤立地看，现有的 AI 模型不太可能为威胁行为者带来突破性能力。然而，随着前沿 AI 变得更加先进，可能的网络攻击类型将会演化，这要求防御策略持续改进。

我们还发现，现有的 AI 网络安全评估往往忽视网络攻击的重要方面——例如"隐匿"（攻击者隐藏自己的存在）和"持久化"（攻击者维持对被入侵系统的长期访问）。而这些领域恰恰是 AI 驱动的方法可以特别有效之处。我们的框架通过讨论 AI 可能如何降低攻击在成功之路上的门槛，照亮了这个问题。

## 赋能网络安全社区

随着 AI 系统不断扩展规模，它们自动化并增强网络安全的能力，有潜力改变防御者预测和响应威胁的方式。

我们的网络安全评估框架旨在支持这一转变：它清晰地呈现 AI 也可能被滥用的方式，以及现有网络防护可能不足之处。通过突出这些新兴风险，这一框架与基准测试将帮助网络安全团队加固防御，领先于快速演化的威胁。

[阅读完整论文](https://arxiv.org/abs/2503.11917)
