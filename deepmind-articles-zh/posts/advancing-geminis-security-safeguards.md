---
title: "推进 Gemini 的安全防护措施"
title_en: "Advancing Gemini's security safeguards"
source: https://deepmind.google/blog/advancing-geminis-security-safeguards/
site: deepmind
date: 2025-05-20
crawled: 2026-09-13
translated: 2026-09-13
---

# 推进 Gemini 的安全防护措施

> 原文：[Advancing Gemini's security safeguards](https://deepmind.google/blog/advancing-geminis-security-safeguards/) · Google DeepMind

我们正在发布一份新的白皮书，阐述我们如何把 Gemini 2.5 打造成迄今最安全的模型家族。

想象一下，让你的 AI 智能体总结你最近的邮件——一个看似简单的任务。Gemini 和其他大语言模型（LLM）在执行这类任务上持续进步，它们需要访问我们的文档、日历或外部网站等信息。但如果其中一封邮件里藏着恶意的隐藏指令，企图诱骗 AI 泄露私密数据或滥用其权限，那该怎么办？

间接提示词注入（indirect prompt injection）是一个现实存在的网络安全挑战：AI 模型有时难以区分真实的用户指令和嵌入在所检索数据中的操纵性命令。我们的新白皮书[《Lessons from Defending Gemini Against Indirect Prompt Injections》](https://storage.googleapis.com/deepmind-media/Security%20and%20Privacy/Gemini_Security_Paper.pdf)阐述了我们的战略蓝图，用以应对间接提示词注入——它们使由先进大语言模型支持的智能体化 AI 工具成为此类攻击的目标。

我们不仅要构建能力强大的 AI 智能体，更要构建安全的 AI 智能体——为此我们持续研究 Gemini 可能如何响应间接提示词注入，并增强其抵御能力。

![](https://deepmind.google/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)![](https://deepmind.google/static/images/fallback/video_poster_fallback_dark.4d55bc99efa6.jpg)

![你的浏览器不支持 video 标签。](/static/images/fallback/video_poster_fallback_light.57b61d57842a.jpg)

## 评估基线防御策略

间接提示词注入攻击错综复杂，需要持续保持警惕并采用[多层防御](https://arxiv.org/abs/2503.18813)。Google DeepMind 的安全与隐私研究团队专注于保护我们的 AI 模型免受蓄意的恶意攻击。靠人工寻找这些漏洞既缓慢又低效，尤其是在模型快速演进的背景下。这正是我们构建一套自动化系统来不断探测 Gemini 防御的原因之一。

## 用自动化红队测试让 Gemini 更安全

我们安全策略的核心是自动化红队测试（ART）：我们内部的 Gemini 团队以现实的方式不断攻击 Gemini，以揭示模型中潜在的安全弱点。使用这一技术——连同我们白皮书中详述的其他努力——显著提高了 Gemini 在工具使用期间抵御间接提示词注入攻击的防护率，使 Gemini 2.5 成为迄今最安全的模型家族。

我们测试了研究界提出的若干防御策略，以及我们自己的一些构想：

![一张表格，展示针对间接提示词注入的基线防御策略，分为「Prompt Modifications (In-context)（提示词修改（上下文内））」和「Checking the Data Input/Output (Classifiers)（检查数据输入/输出（分类器））」两类。详细策略包括 In-Context Learning（上下文学习）、Spotlighting（聚光）、Paraphrasing（改写）、Classifiers（分类器）、Self-reflection（自我反思）和 Perplexity Filters（困惑度过滤器）。](https://lh3.googleusercontent.com/8U1p0Z0fok_zyUGLarrIZY59jqZvYXAipW5NIPQ3p3I_RCKhyeBTt-ZGC_5935AyowZ2O4HBGfBYrQb8oIs-CW-8cD3MzfNbHudI-6xX7BLmZ5RGAw=w1440)

## 为自适应攻击定制评估

基线缓解措施在面对基本的非自适应攻击时展现出前景，显著降低了攻击成功率。然而，恶意行为者越来越多地使用自适应攻击——专门设计为随 ART 一同演化和调整，以绕开被测试的防御。

像 Spotlighting 或 Self-reflection 这样成功的基线防御，在面对学会了如何应对并绕过静态防御方法的自适应攻击时，效果大幅下降。

这一发现揭示了一个关键点：只针对静态攻击测试过的防御会带来虚假的安全感。要实现稳健的安全，关键在于评估那些会随潜在防御而演化的自适应攻击。

## 通过模型加固构建内在韧性

虽然外部防御和系统级护栏很重要，但增强 AI 模型识别并无视嵌入在数据中的恶意指令的内在能力同样关键。我们把这一过程称为「模型加固（model hardening）」。

我们在一个由真实场景构成的大型数据集上对 Gemini 进行了微调，其中 ART 针对敏感信息生成有效的间接提示词注入。这让 Gemini 学会忽略恶意嵌入指令、遵循用户的原始请求，从而只给出它应当提供的正确、安全的响应。这使模型能够从内在上理解如何处理随时间演化、作为自适应攻击一部分的受损信息。

这种模型加固显著增强了 Gemini 识别并无视注入指令的能力，降低了其攻击成功率。而且重要的是，模型在正常任务上的表现没有受到明显影响。

需要指出的是，即便有了模型加固，也没有任何模型能完全免疫。执着的攻击者仍可能发现新的漏洞。因此，我们的目标是让攻击对对手而言困难得多、代价高昂得多、复杂得多。

## 以整体方式看待模型安全

保护 AI 模型免受间接提示词注入等攻击需要「纵深防御」（defense-in-depth）——使用多层保护，包括模型加固、输入/输出检查（如分类器）以及系统级护栏。对抗间接提示词注入是我们落实[智能体安全原则与指南](https://research.google/pubs/an-introduction-to-googles-approach-for-secure-ai-agents/)、以负责任方式开发智能体的关键途径。

保护先进 AI 系统免受间接提示词注入这类具体的、不断演化的威胁，是一项持续的工作。它要求我们坚持持续且自适应的评估，改进现有防御并探索新防御，同时在模型自身中构建内在韧性。通过层层设防并不断学习，我们可以让 Gemini 这样的 AI 助手继续保持极大的实用性与可信度。

要进一步了解我们为 Gemini 构建的防御，以及我们关于使用更具挑战性的自适应攻击来评估模型稳健性的建议，请参阅 GDM 白皮书[《Lessons from Defending Gemini Against Indirect Prompt Injections》](https://storage.googleapis.com/deepmind-media/Security%20and%20Privacy/Gemini_Security_Paper.pdf)。
