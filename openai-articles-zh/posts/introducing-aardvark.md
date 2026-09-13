---
title: "介绍 Aardvark：OpenAI 的智能体安全研究员"
title_en: "Introducing Aardvark: OpenAI’s agentic security researcher"
source: https://openai.com/index/introducing-aardvark/
crawled: 2026-09-13
category: research
translated: 2026-09-13
---

# 介绍 Aardvark：OpenAI 的智能体安全研究员

> 原文：[Introducing Aardvark: OpenAI’s agentic security researcher](https://openai.com/index/introducing-aardvark/) · OpenAI 博客

**2026 年 3 月 6 日更新：** *Aardvark 现已成为 Codex Security，并以研究预览版（research preview）形式开放。*

*Aardvark 现已直接内置于 Codex，以 Codex Security 的形式通过 Codex 网页版逐步向 ChatGPT Enterprise、Business 与 Edu 客户推出，未来一个月内免费使用。详情请参阅我们的博客*[此处](https://openai.com/index/codex-security-now-in-research-preview/)*。*

今天，我们正式发布由 GPT‑5 驱动的智能体安全研究员 Aardvark。

软件安全是技术领域最关键、也最具挑战性的前沿之一。每年，企业和开源代码库中都会发现数以万计的新漏洞。防御方肩负着艰巨的任务：必须抢在攻击者之前发现并修补漏洞。在 OpenAI，我们正努力让天平向防御方倾斜。

Aardvark 代表了 AI 与安全研究领域的一项突破：一个能够帮助开发者和安全团队大规模发现并修复安全漏洞的自主智能体。Aardvark 现已开启私密测试（private beta），以便在实际环境中验证并打磨其能力。

## Aardvark 的工作原理

Aardvark 持续分析源代码仓库，以识别漏洞、评估可利用性、按严重程度排定优先级，并提出有针对性的补丁。

Aardvark 的工作方式是监控代码库的提交与变更，识别漏洞及其可能被利用的方式，并提出修复方案。Aardvark 不依赖模糊测试（fuzzing）或软件成分分析这类传统程序分析技术，而是利用基于 LLM 的推理与工具使用来理解代码行为、识别漏洞。Aardvark 寻找 bug 的方式与人类安全研究员类似：阅读代码、分析代码、编写并运行测试、使用工具，等等。

Aardvark 依靠一个多阶段流水线来识别、解释并修复漏洞：

- **分析**：首先分析整个仓库，生成一个威胁模型（threat model），反映其对项目安全目标与设计的理解。
- **提交扫描**：在新代码提交时，对照整个仓库与威胁模型检查提交级变更，扫描漏洞。仓库首次接入时，Aardvark 会扫描其历史记录，以发现既有问题。Aardvark 会逐步解释其发现的漏洞，并对代码进行标注，供人工审查。
- **验证**：一旦 Aardvark 发现疑似漏洞，它会在隔离的沙箱环境中尝试触发该漏洞，以确认其可利用性。Aardvark 会描述所采取的步骤，以确保返回给用户的洞察准确、高质量且误报率低。
- **修补**：Aardvark 与 OpenAI Codex 集成，帮助修复其发现的漏洞。它会为每个发现附上一个由 Codex 生成、并经 Aardvark 扫描的补丁，供人工审查，实现高效的一键修补。

Aardvark 与工程师并肩工作，与 GitHub、Codex 及现有工作流集成，在不拖慢开发的情况下提供清晰、可操作的洞察。虽然 Aardvark 为安全而生，但在测试中我们发现，它还能发现逻辑缺陷、不完整的修复、隐私问题等 bug。

## 当下已见实效

Aardvark 已投入服务数月，持续运行于 OpenAI 内部代码库以及外部 alpha 合作伙伴的代码库。在 OpenAI 内部，它已经发现了多个有价值的漏洞，并为 OpenAI 的防御态势做出了贡献。合作伙伴尤为称赞其分析的深度——Aardvark 能发现仅在复杂条件下才会出现的问题。

在“黄金”（golden）仓库的基准测试中，Aardvark 识别出了 92% 的已知及人工植入漏洞，展现出高召回率与真实场景中的实效。

## 面向开源项目的 Aardvark

Aardvark 也已被应用于开源项目，由它发现并经我们负责任披露（responsible disclosure）的漏洞数量众多，其中 10 个已获得 CVE（Common Vulnerabilities and Exposures，公共漏洞与暴露）编号。

作为数十年开放研究与负责任披露的受益者，我们致力于回馈——贡献工具与发现，让数字生态对每个人都更安全。我们计划为部分精选的非商业开源仓库提供免费（pro-bono）扫描，为开源软件生态与供应链的安全贡献力量。

我们最近[更新](https://openai.com/index/scaling-coordinated-vulnerability-disclosure/)了[对外协同披露政策](https://openai.com/policies/outbound-coordinated-disclosure-policy/)（outbound coordinated disclosure policy）。新政策采取对开发者友好的立场，注重协作与可扩展的影响，而非可能给开发者带来压力的僵硬披露时间表。我们预计，Aardvark 这类工具将发现越来越多的 bug，因此希望以可持续的方式开展协作，实现长期的安全韧性。

## 为什么这件事很重要

软件如今是每个行业的支柱，这意味着软件漏洞对企业、基础设施乃至整个社会都是系统性风险。仅 2024 年一年，就有超过 4 万个 CVE 被上报。我们的测试显示，大约 1.2% 的提交会引入 bug——改动虽小，后果却可能极为严重。

Aardvark 代表了一种全新的“防御者优先”模式：一个随代码演进持续提供防护、与团队并肩作战的智能体安全研究员。通过尽早捕获漏洞、验证真实可利用性并提供清晰的修复方案，Aardvark 能够在不拖慢创新的前提下增强安全。我们坚信应当扩大安全专业能力的可及性。我们将从私密测试起步，并在学习积累的过程中逐步扩大开放范围。

## 私密测试现已开放

我们正邀请部分精选合作伙伴加入 Aardvark 私密测试。参与者将获得抢先体验，并与我们的团队直接合作，打磨检测准确度、验证工作流与报告体验。

我们希望在各种环境中验证其表现。如果你的组织或开源项目有兴趣加入，可以[在此申请](https://www.openai.com/form/aardvark-beta-signup)。
