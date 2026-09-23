---
title: "用 SapFix 与 Sapienz 自动发现并修复软件缺陷"
title_en: "Finding and fixing software bugs automatically with SapFix and Sapienz"
date: 2018-09-13
source: https://ai.facebook.com/blog/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz
crawled: 2026-09-22
translated: 2026-09-22
---

# 用 SapFix 与 Sapienz 自动发现并修复软件缺陷

> 原文：[Finding and fixing software bugs automatically with SapFix and Sapienz](https://ai.facebook.com/blog/finding-and-fixing-software-bugs-automatically-with-sapfix-and-sapienz) · Meta AI（Wayback 存档）

2018 年 9 月 13 日

调试代码是件苦差事。但 Facebook 工程师创建的新型 AI 混合工具 SapFix，可以显著减少工程师花在调试上的时间，同时加快新软件的推出进程。SapFix 能自动为特定缺陷生成修复，然后提交给工程师审批并部署到生产环境。SapFix 已被用于加速向数百万台使用 Facebook Android 应用的设备推送健壮、稳定的代码更新——这是此类 AI 驱动的测试与调试工具首次在生产环境中如此大规模使用。我们打算与工程界分享 SapFix，因为它是调试自动化演进的下一步，有望为众多公司和研究组织提升新代码的生产力与稳定性。

SapFix 被设计为可以独立运行的工具，既可以与 Facebook 在 F8 上发布、且已部署到生产的智能自动化软件测试工具 Sapienz 搭配，也可以脱离它运行。在当前的概念验证阶段，SapFix 专注于修复 Sapienz 在缺陷进入生产之前发现的问题。流程从 Sapienz 与 Facebook 的 Infer 静态分析工具开始，帮助定位需要打补丁的代码位置。一旦 Sapienz 与 Infer 锁定了与崩溃相关的特定代码片段，就可以把信息传给 SapFix，后者自动从几种策略中选择来生成补丁。

## SapFix 如何进行调试

（配图展示 SapFix 如何为软件缺陷生成补丁。）针对高发缺陷，SapFix 创建完全或部分回退引入缺陷的代码提交的补丁。对更复杂的崩溃，系统从其模板化修复集合中汲取生成补丁。这些模板基于以往修复池，从人类工程师创建的模板中自动采集而来。当此前使用的人工设计模板不适用时，SapFix 会尝试基于变异的修复：对导致崩溃语句的抽象语法树（AST）做小的代码修改，不断调整补丁直到找到可能的解决方案。

## 自主验证与人工审批

一旦落到某个具体补丁上，SapFix 的工作还远未结束。该工具为每个缺陷生成多个候选修复，然后通过检查三个问题评估其质量：是否有编译错误、崩溃是否仍然存在、该修复是否引入新的崩溃？为解决后两个问题，SapFix 会在打过补丁的构建上运行开发者已编写的测试以及 Sapienz 创建的测试。而且与之前的补丁生成步骤一样，这一验证过程自主进行，并与更大的代码库隔离。

SapFix 正在复刻人类目前所做的调试工作，但它并非为独自向生产代码部署修复而设计。当补丁通过完整测试后，SapFix 把它们发送给人类审阅者审批。这与人类生成的报告被其他开发者检查和批准的方式非常相似，只是系统会自动跟踪审阅者的反馈、落地被接受的补丁并清理其余补丁。某些情况下，SapFix 会从多个选项中挑出最佳修复，并把推荐呈现给工程师。（配图展示 SapFix 如何就其生成的修复寻求工程师反馈：若被拒绝则放弃补丁，若被接受则落地。）因此，无论其底层技术多么强大、自主运行节省了多少时间与精力，SapFix 都无法自行实施其提议的修复。工程师始终在回路之中，该工具依赖他们的专业知识来确认提议的修复是否应当部署。

由于 SapFix 仍在开发中，它还没有达到 Sapienz 的使用规模——后者如今每月产出数百份精确指出出错行号的缺陷报告，审查与 Facebook、Instagram、Workplace 及 Messenger 的 Android 应用相关的代码。Sapienz 的报告中约四分之三促成了开发者的修复。但自从 8 月开始测试 SapFix 以来，该工具已成功生成被人类审阅者接受并推送到生产的补丁。

## 为全自动调试铺路

据我们所知，这标志着机器生成的修复——经自动端到端测试与修复——首次被部署到 Facebook 这种规模的代码库中。这是 AI 混合工具的重要里程碑，并进一步证明基于搜索的软件工程能减少软件开发的摩擦。随着我们开发 SapFix 以处理不同类型的缺陷与软件，该工具有望改变代码生成的速度与质量。这不仅适用于大规模运营的公司，也几乎适用于所有编写代码的人。无论搭配还是分开使用，SapFix 与 Sapienz 都让开发者把更少时间花在调试上、更多时间用于创造下一个新事物。

但通过这项工作，我们也希望鼓励对代码自动修复与改进的持续研究。科学文献对这一领域热情高涨：既有对各类技术的实证研究，也有供科学界攻克的诱人的开放问题与挑战集，还有对自动改进代码近期结果的综述。作为首个在此规模部署的此类工具，SapFix 将为这一令人兴奋但充满挑战的研究议程注入新的动力与活力。Sapienz 与如今的 SapFix 都计划在完成额外工程工作后开源，我们收到的反馈将帮助我们以及更广泛的 AI 社区，改进「自动发现并修复代码缺陷」这一集体任务。

虽然我们目前聚焦 SapFix 如何在崩溃发生前自动拦截，其更长期的应用可能包括让软件更快、更灵敏。这些系统提供了显著的基础收益，其影响有望与将要使用它们的开发者一样多样而广泛。

我们感谢以下工程师并致谢他们对 SapFix 的贡献：Alex Marginean、Johannes Bader、Satish Chandra、Alexander Mols 和 Andrew Scott。

**作者：**

- Yue Jia，Facebook 软件工程师
- Ke Mao，Facebook 软件工程师
- Mark Harman，Facebook 工程经理
