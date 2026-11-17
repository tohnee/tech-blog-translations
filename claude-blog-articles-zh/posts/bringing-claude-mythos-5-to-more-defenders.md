---
title: "让更多防御者用上 Claude Mythos 5 的网络安全能力"
title_en: "Bringing the cybersecurity capabilities of Claude Mythos 5 to more defenders"
date: 2026-08-21
source: https://claude.com/resources/articles/bringing-claude-mythos-5-to-more-defenders
crawled: 2026-11-17
translated: 2026-11-17
---

# 让更多防御者用上 Claude Mythos 5 的网络安全能力

> 原文：[Bringing the cybersecurity capabilities of Claude Mythos 5 to more defenders](https://claude.com/resources/articles/bringing-claude-mythos-5-to-more-defenders) · Claude 博客

*我们分享一项进展：我们正努力帮助更多团队把前沿能力用于网络防御。[Claude Mythos 5](https://www.anthropic.com/news/claude-fable-5-mythos-5) 现已在 [Claude Security](https://claude.com/product/claude-security) 中上线，并将很快接入合作伙伴的网络防御工具。我们同时启动一支 3500 万美元的基金，帮助加固开源软件的安全，并公布了扩展 [Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet)（网络验证计划）的方案。*

今年四月，我们推出 [Project Glasswing](https://www.anthropic.com/glasswing)，把我们能力最强的前沿模型 Claude Mythos Preview（及其后继版本 Claude Mythos 5）交到一小批组织手中——它们负责守护世界上最关键的一些软件。这为防御方争取到一个窗口期，让他们能在能力相近的模型全面开放或落入恶意行为者手中之前，发现并修复漏洞。

我们的目标始终是：在安全允许的范围内，让尽可能多的防御者获得 Mythos 级别的防御能力。为此，我们一直在研发[安全分类器](https://www.anthropic.com/research/next-generation-constitutional-classifiers)与防护措施，使我们能够扩大 Mythos 级模型的开放范围，同时不让其攻击性网络能力落入不当之手。[Claude Fable 5](https://www.anthropic.com/news/claude-fable-5-mythos-5) 是第一步：它让模型得以广泛可用，同时阻断了两用性质的网络安全工作。

今天，我们迈出下一步。风险最高的情形，是用户可以直接访问模型——恶意行为者可能试图把模型引向有害用途。但如果用户只能获得特定输出，例如某个漏洞的补丁或一条安全告警，风险就会低得多。我们此次宣布的调整，让用户能更多地获取防御性成果，同时对模型的直接访问保留适当的护栏：

* **把 Claude Mythos 5 集成进防御者依赖的工具。** 我们正与网络安全技术及服务合作伙伴合作，把 Claude Mythos 5 集成进防御者已经在用来保护软件的产品与服务。
* **Claude Security 扫描现在可以运行在 Claude Mythos 5 上。** Claude Enterprise 套餐的客户现在可以在 Claude Security 中运行我们能力最强的模型，用它扫描代码库中的安全漏洞并给出补丁建议。
* **3500 万美元额度投向开源安全。** 新设立的 Defender Advantage Fund（0xDAF）将提供 3500 万美元额度，支持为开源项目修补漏洞、把开源软件扫描与打补丁流程的部分环节自动化、以及试验新安全方法的组织。
* **扩展 Cyber Verification Program。** 该计划目前已为通过审核的防御者降低 Opus 与 Sonnet 模型上的防护限制。未来几周，我们将扩展该计划，把 Opus 和 Sonnet 上更广泛的两用能力纳入其中，Mythos 级别的访问随后跟进。

我们的目标依然不变：随着 AI 模型能力日益增强，帮助各类组织适应网络安全在节奏与要求上的变化。我们将继续开发防护措施、访问计划与社区支持，让我们能力最强的模型能够安全地提供给广泛的个人与组织。

## 把 Mythos 集成进现有网络防御工具

守护医院、公用事业、金融系统和软件供应链的团队，早已依赖一整套产品与服务来完成安全运营、事件响应、威胁情报与检测工程。要让这些防御者最快用上前沿能力，就是把他们已经在跑的工具与 Mythos 级模型集成。

我们的许多合作伙伴已经[在 Claude Opus 上构建了网络安全产品](https://claude.com/resources/articles/how-our-partners-are-putting-opus-to-work-for-cybersecurity)，帮助安全团队更快地分诊告警、识别威胁、修复漏洞。我们现在正与这些伙伴以及更多伙伴合作，把 Claude Mythos 5 构建进他们的产品与服务，让他们能够向客户交付 Mythos 级别的防御成果。

最终用户使用这些产品时，并不是直接与 Mythos 交互。他们是通过一个为特定任务专门构建的界面来使用：Mythos 在后台运行，用户只会收到该产品本应提供的特定产物。举例来说，一个修复漏洞的工具，其输出可能是一份建议补丁列表。这份输出由 Mythos 生成，但用户没有办法去提示模型——比如说——为一个漏洞编写利用程序。我们与合作伙伴也都部署了滥用防范措施，以确认模型始终处于预期范围之内。

这项工作尚在早期，我们预计它会随时间扩展。如果你在构建安全产品或服务，并希望把 Claude Mythos 5 带给你的客户，可以[在此登记意向](https://claude.com/form/mythos-cyber-partner)。

## 面向 Enterprise 客户提供由 Claude Mythos 5 驱动的 Claude Security

从今天起，[Claude Security](https://claude.com/product/claude-security) 扫描开始在 Claude Mythos 5 上运行。Claude Security 会扫描代码库中的漏洞，并给出供人工复核的补丁建议；它目前面向 Claude Enterprise 客户公测，使用 Mythos 5 的扫描按你现有套餐的标准 token 用量计费，无需单独购买附加项。

Enterprise 管理员可以在[管理控制台](http://claude.ai/admin-settings/claude-code)中启用 Claude Security。用户可以从 [claude.ai/security](http://claude.ai/security) 选择一个仓库，用 Claude Mythos 5 进行扫描。Claude 随后扫描代码库中的漏洞，并为每一项发现返回 [CWE](https://cwe.mitre.org/)（Common Weakness Enumeration，通用缺陷枚举）类别、置信度与严重程度评级，以及修复建议。

用户接着可以打开 Claude Code on the web 来实施修复。交互式打补丁使用的是贵组织在 Claude Code 中可访问的模型。Mythos 扫描本身不会把 Mythos 的访问权限延伸到其他入口。每个补丁都必须经人工审核批准后才能实施。

Claude Security 使用 Mythos 5 扫描你拥有的代码，返回的是详细的发现结果而非未经处理的原始输出，同时不暴露模型本身。这意味着防御者可以调用 Claude Mythos 5 的能力，而模型不会因此向可能滥用它的人开放。

关于 Claude Security 的更多信息，请参阅我们的[上手指南](https://claude.com/resources/tutorials/getting-started-with-claude-security)。

## 启动 Defender Advantage Fund，加固开源软件安全

世界上一些使用最广的程序，建立在开源软件之上。然而这些项目往往由志愿者或非营利基金会维护，他们可能缺乏资源或人手，来全面防御自己的项目免受攻击。通过 Project Glasswing，我们向开源安全组织直接捐赠了 400 万美元，为计划内的开源安全基金会提供了额度，帮助扫描并修补广泛使用的项目，并支持 [Akrites](https://akrites.org/) 和 [Gold Eagle](https://www.whitehouse.gov/releases/2026/07/white-house-launches-gold-eagle-initiative-for-unprecedented-cybersecurity-vulnerability-coordination/) 这类协同漏洞修复行动。

新设立的 Defender Advantage Fund（0xDAF）在这一基础上更进一步，提供 3500 万美元的 Claude 额度，用于支持那些帮助开源维护者加固软件安全的组织。资助将聚焦三个方向：修补广泛使用项目中现存的漏洞；以其他项目可复制的方式实现扫描与打补丁的自动化；帮助项目探索更有雄心的安全方案，使其能够抵御整类攻击。

我们将从少量金额较大的试点资助开始，摸清哪些做法有效、哪些最易规模化。未来几周，我们会公布首批获资助方的详情。

## 扩展 Cyber Verification Program

迄今为止，我们的 Cyber Verification Program 已为组织提供在使用 Claude Opus 和 Sonnet 模型时访问两用能力的通道。加入该计划的组织会获得降低后的防护限制，从而尽量减少对已获认可、在其有权保护的系统上从事正当网络安全工作的团队造成的打断。

未来几周，我们将演进该计划，扩大对 Claude Mythos 的受防护访问。具体而言，漏洞分诊与验证等防御性能力的访问将扩展到 Mythos 级模型，网络防御者在 Claude Opus 与 Sonnet 级模型上遇到的拦截也会减少。此外，我们将继续与美国政府的伙伴合作，通过 Project Glasswing 扩大 Claude Mythos 的访问范围，重点面向符合严格安全控制要求的关键基础设施防护方。

我们将在未来几周分享有关 Cyber Verification Program 扩展的更多细节。与此同时，我们鼓励所有从事正当网络安全工作的安全团队申请该计划，以在 Claude Opus 和 Sonnet 模型上获得降低的防护限制。如果你已报名并获批，无需任何操作；我们会主动联系你告知更新。

## 下一步

这些举措延续了我们一贯的努力：让前沿模型的防御能力惠及更多个人与组织，并支持开源社区加固项目以抵御攻击。我们将继续与政府伙伴、各类组织、开源维护者以及更广泛的行业合作，共同建设当今能力强大的 AI 模型所要求的、有韧性的网络基础设施。

* 申请 [Cyber Verification Program](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet)。
* [登记意向](https://claude.com/form/mythos-cyber-partner)，用 Mythos 构建网络安全产品与服务。
* Claude Security 面向 Enterprise 客户公测。管理员可在[管理控制台](http://claude.ai/admin-settings/claude-code)中启用 Claude Security。完整操作演示见我们的[上手指南](https://claude.com/resources/tutorials/getting-started-with-claude-security)。
