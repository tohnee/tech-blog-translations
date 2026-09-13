---
title: "推出 Gemini 3.5 Flash Cyber"
title_en: "Introducing Gemini 3.5 Flash Cyber"
source: https://deepmind.google/blog/introducing-gemini-3-5-flash-cyber/
site: deepmind
date: 2026-07-21
crawled: 2026-09-13
translated: 2026-09-13
---

# 推出 Gemini 3.5 Flash Cyber

> 原文：[Introducing Gemini 3.5 Flash Cyber](https://deepmind.google/blog/introducing-gemini-3-5-flash-cyber/) · Google DeepMind

Google 多年来持续投资网络安全，率先开展自动化漏洞发现以保护全球的代码库。像 [CodeMender](https://deepmind.google/blog/introducing-codemender-an-ai-agent-for-code-security/) 这样的工具——我们的代码安全智能体——可以自动发现并修复关键软件漏洞。但随着 AI 智能体发现漏洞的速度快于防御者修复的速度，应对这一全球性威胁需要一种能力强大、价格可负担且可扩展的方法。

今天，我们通过推出 Gemini 3.5 Flash Cyber 来扩展长期以来的努力，帮助防御者做好更充分的准备。这是建立在 3.5 Flash 之上的轻量级网络安全模型，经过微调以快速高效地发现、验证和修补漏洞，在这些任务上比 Gemini 的主线 Flash 模型更有效。

Flash 的性能与效率使其成为我们网络安全模型工作的理想基础。通过构建在 Flash 之上，3.5 Flash Cyber 提供了相对于大型、昂贵网络安全模型而言成本更低且能力强大的替代方案。

鉴于这项技术的双重用途性质，我们对 3.5 Flash Cyber 的部署方式采取了审慎的态度。作为有限访问试点计划的一部分，3.5 Flash Cyber 即将通过 CodeMender 专门提供给政府和可信合作伙伴，并随时间逐步扩大。这将让一线防御者在关键漏洞被利用之前抢先发现并修复它们，同时缓解更广泛的滥用风险。

另外，我们还将 CodeMender 的基础能力通过正式发布的 Gemini 模型直接带给客户，载体是 [Gemini Enterprise Agent Platform](https://cloud.google.com/blog/products/identity-security/find-and-fix-software-vulnerabilities-with-codemender)。

## 搜索空间问题：轻量级模型在代码安全中的优势

发现深层缺陷需要探索巨大的执行搜索空间。依赖对大型语言模型的单次昂贵调用可能造成瓶颈。3.5 Flash Cyber 特别适合发现那些需要智能体扫描大型代码库并分析大量代码路径的漏洞。

CodeMender 会多次调用 3.5 Flash Cyber，因此智能体可以分析多得多的代码路径来发现和验证漏洞。随后，子智能体汇总生成一份单一的高质量报告。

凭借其速度和经济性，3.5 Flash Cyber 可以轻松集成到高频扫描、对时间敏感的发布流程或大规模的提交（commit）扫描流水线中。

## 3.5 Flash Cyber 基准测试结果：大型网络安全模型的高效替代方案

我们在多种基准测试上对 3.5 Flash Cyber 进行了测试。特别地，我们在 CyberGym 基准上测试了 3.5 Flash Cyber，该基准以数百个真实世界的软件漏洞评估 AI 智能体。通过利用 3.5 Flash Cyber 的低成本，将 CodeMender 配置为针对一份最终报告最多调用 3.5 Flash Cyber 五次，整体智能体在 CyberGym\* 上取得了与明显更大的模型相当的性能。

### CyberGym 上的成功率（pass@1）

*\*竞争对手结果来自厂商自行报告的分数*

我们还在 CyberGym 之外、不设安全防护栏（guardrails）的情况下对该模型的能力进行了压力测试。[Google 的 Big Sleep](https://cloud.google.com/blog/products/identity-security/cloud-ciso-perspectives-our-big-sleep-agent-makes-big-leap) 团队独立构建了一项评测，专注于在一些世界上最复杂的代码库（如 Chrome 和 Safari）中发现关键且难以发现的漏洞。在这里，3.5 Flash Cyber 显著超过了主线 3.5 Flash 和 3.6 Flash。

### Big Sleep 评测上的成功率（pass@1）

3.5 Flash Cyber 还在 Google Chrome 的生产提交扫描流水线上进行了评估。这些漏洞未对外公开，这确保了该基准对 Gemini 和竞争对手模型都保持无污染。

结果显示，与 3.5 Flash 相比，3.5 Flash Cyber 带来了显著提升。注：Opus 4.6 之后更新的竞争对手模型版本由于内置安全防护栏而拒绝执行这些任务，因此未在图中展示。

### Chrome 生产提交扫描流水线上的成功率（pass@1）

此外，与主线 3.5 Flash 和 Claude Opus 4.6 相比，3.5 Flash Cyber 持续发现更多独特漏洞。在高度复杂的 V8 JavaScript 引擎上以固定调用次数进行测试时，3.5 Flash Cyber 发现了 55 个独特的已确认问题，而主线 3.5 Flash 发现了 47 个，Opus 4.6 发现了 36 个——其中包括另外两个被测模型都未捕捉到的 10 个问题。

基础的网络安全模型可能陷入循环，反复发现同一个问题而遗漏关键漏洞。强大的模型撒下更广的网，发现更多独特问题。

随着我们扩大调用次数，我们发现 3.5 Flash Cyber 会持续发现新的代码路径和漏洞。

## 现实应用与 Google 的防御规模化

基准测试只是故事的一部分。CodeMender 中的 3.5 Flash Cyber 已经在 Google 的内部代码库中发现并修复漏洞，包括 Chrome、Android、Cloud、Ads 和 YouTube。

轻量级模型所带来的发现速度，已经产生了可衡量的影响。

例如，Google 的 Cloud 漏洞研究团队使用 3.5 Flash Cyber 以创纪录的时间主动加固了我们的系统。仅用 2 小时，该模型就在公开 API 中发现了远程代码执行漏洞，并在一个敏感的生产服务中发现了内存损坏漏洞。它随后生成了一个 100% 可靠的远程代码执行利用（exploit），绕过了地址空间布局随机化（ASLR）和 Write XOR Execute（W^X）等标准缓解技术。

来自 Wiz 和 Cloud CISO Security Engineering 测试人员的早期反馈证实，3.5 Flash Cyber 相比主线 3.5 Flash 模型有显著的能力提升。

## 大规模赋能防御者

Google 在软件安全领域的领导地位给了我们独特的优势。例如，由 Google 运营、覆盖超过 70 万个开源漏洞的漏洞数据库 [OSV.dev](https://osv.dev/)，以及超过 10 年的 [OSS-Fuzz](https://github.com/google/oss-fuzz) 结果，帮助我们识别质量最高的漏洞。

这使我们能够超越合成网络安全样本，教会我们的模型真实的安全专业人员如何工作。我们的模型学会使用行业标准工具、通读 Chromium 等大规模项目中数百万行代码，并独立完成需要数小时持续深入分析的复杂安全任务。

通过用 3.5 Flash Cyber 驱动 CodeMender，我们正在提供一种能力强大、可扩展且价格可负担的架构，帮助更多防御者保护软件安全。
