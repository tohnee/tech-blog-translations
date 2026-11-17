---
title: "我们的合作伙伴如何让 Opus 在网络安全中发挥作用"
title_en: "How our partners are putting Opus to work for cybersecurity"
date: 2026-05-21
source: https://claude.com/resources/articles/how-our-partners-are-putting-opus-to-work-for-cybersecurity
crawled: 2026-11-17
translated: 2026-11-17
---

# 我们的合作伙伴如何让 Opus 在网络安全中发挥作用

> 原文：[How our partners are putting Opus to work for cybersecurity](https://claude.com/resources/articles/how-our-partners-are-putting-opus-to-work-for-cybersecurity) · Claude 博客

了解 Wiz、Palo Alto Networks 和 Accenture 等公司如何借助 Claude Opus 更快地发现并修复漏洞，并大规模部署 AI 防御。

AI 正在改变安全漏洞被发现和利用的速度，而最明确的应对方式，是让安全团队把高能力模型用于自身的防御。

当我们[公测推出 Claude Security](https://claude.com/resources/articles/claude-security-public-beta) 时，也公布了一批基于 Claude Opus 构建的技术与服务合作伙伴，因为每个团队的采用路径都不同：有的可能直接使用 Claude，有的通过已在运行的平台使用，还有的通过熟悉其环境的服务伙伴使用。

其中若干产品现已上线，早期结果展示了前沿模型防御在实践中是什么样子。

## 早期成果

合作伙伴报告称，无论内部还是客户环境中，由 Opus 驱动的防御能力都有显著提升：

* 每周对超过 15 万个生产资产进行持续渗透测试，每周发现数千个经确证的高危和严重漏洞，且零误报（Wiz，客户生产环境）。
* 相当于一年份的渗透测试工作量，在三周内完成（Palo Alto Networks，内部测试）。
* 在 1,600 个应用和 500,000 多个 API 上，安全测试覆盖率从约 10% 提升到 80% 以上，扫描周转时间从 3 到 5 天缩短到一小时以内（Accenture，自有基础设施）。

这些工作分为三个领域：大规模进攻性测试、缩小漏洞发现与修复之间的差距，以及把受治理的 AI 部署到生产环境。

## 生产规模下的持续进攻性测试

进攻性测试是指像对手那样攻击自己的系统，从而先一步找到可被利用的路径。

Wiz [Red Agent](https://www.wiz.io/blog/red-agent-claude-opus) 是一个 AI 驱动的攻击者，借助 Opus 在生产 Web 应用和 API 上像人类渗透测试员一样推理。它分析应用逻辑、串联步骤，并实时适应服务器响应，从而暴露传统扫描器遗漏的逻辑驱动型缺陷。它每周在超过 15 万个生产资产上持续运行，发现数千个高危和严重级别的漏洞，每一个都用可利用性证明和来自 Wiz Security Graph 的业务上下文进行了确证。「安全团队不再受限于数据不足，而是受限于对数据采取行动的能力，」Wiz 的 AI 与威胁研究副总裁 Alon Schindel 说。「通过把前沿模型嵌入 Wiz 智能体，我们让组织能够以 AI 的速度进行防御。」

[Unit 42 Frontier AI Defense](https://www.paloaltonetworks.com/unit42/ai-advantage) 是 Palo Alto Networks 的专家主导服务，使用 Opus 寻找隐藏漏洞、梳理它们如何串联成关键攻击路径，并制定抵御 AI 赋能攻击的加固路线图。该服务把暴露面分析与一份经过基准检验的机器速度防御蓝图以及实操转型工作结合起来。「当攻击者把前沿模型武器化来自动化网络攻击时，防御必须更快，」Palo Alto Networks Unit 42 高级副总裁 Sam Rubin 说。

CrowdStrike 的 [Frontier AI Readiness and Resilience Service](https://www.crowdstrike.com/en-us/services/ai-security-services/frontier-ai-readiness-and-resilience/) 把同类能力带到财富 500 强中超过 60% 的企业所信任的平台上：将 Opus 与 CrowdStrike 的 AI 红队服务和专有智能体框架结合，持续搜寻客户应用中的潜伏零日漏洞、验证发现，并在新代码进入生产环境前加速修复。

> 「像 Anthropic Claude Opus 这样的前沿模型，正在赋予防御方一年前还不存在的能力优势，把漏洞管理一路左移。」——Mark Manglicmot，CrowdStrike 全球咨询服务副总裁

## 缩小发现与修复之间的差距

漏洞暴露风险很大一部分存在于「发现漏洞」与「修复漏洞」之间的空隙里，因为分诊、优先级排序、补丁测试和跨团队交接都需要时间。

Accenture 的 [Cyber.AI](https://newsroom.accenture.com/news/2026/accenture-and-anthropic-team-to-help-organizations-secure-scale-ai-driven-cybersecurity-operations) 是一个智能体平台，把资产、身份、威胁和控制连接进单一的运营模型，由 Opus 在其上进行推理，把检测、优先级排序和修复作为一个持续循环来运行。Accenture 先在内部大规模验证：在其自有全球 IT 基础设施中，把 1,600 个应用和 500,000 多个 API 的安全测试覆盖率从约 10% 提升到 80% 以上，把扫描周转时间从 3 到 5 天缩短到一小时以内——这些结果构成了 Cyber.AI 如今向客户交付能力的基础。

> 「企业领导者正航行在历史上变化最快、最复杂的网络威胁格局中。我们与 Anthropic 合作，交付客户保持领先所需的工具。」——Harpreet Sidhu，Accenture 网络安全全球负责人

TrendAI™ [Vision One](https://www.trendmicro.com/en_us/business/products/one-platform.html) 使用 Opus 辅助的漏洞研究，帮助 185 个国家的企业识别暴露面并通过虚拟补丁缓释风险。经过确证的发现还会流入 TrendAI Zero Day Initiative 进行协调披露，在供应商补丁可用之前最长 96 天就开始保护处于风险中的系统。「随着 AI 加速漏洞发现，防御方真正的挑战变成了大规模修复，」TrendAI 首席平台与业务官、TrendAI 负责人 Rachel Jin 说。「我们与 Anthropic 合作，帮助客户在攻击者利用这段空窗之前，通过缓释和虚拟补丁降低风险。」

Deloitte 的[持续威胁暴露管理（CTEM）](https://www.deloitte.com/global/en/services/consulting-risk/services/deloitte-cyber-attack-surface-management.html)构建在 Deloitte Ascend™ 之上，把发现、验证、优先级排序和修复作为一个工作流运行，包括在没有补丁时设计对策。Opus 的代码推理和自动化稳定性测试，让团队有信心在数小时而非数天或数周内完成修复。「构建在 Ascend 之上的 CTEM 存在的目的，是减少漏洞修复中的决策延迟，」Deloitte 合伙人、美国网络业务负责人 Adnan Amjad 说，「这段时差决定了攻击者与防御者谁能赢得这个窗口。」

## 让 AI 受治理地进入生产环境

智能体 AI 用例的新世界给许多团队带来了新的挑战。在没有清晰框架的情况下，为部署建立控制措施、审计证据和自主性边界，常常让安全领域的 AI 采用陷入「试点炼狱」。

PwC 的 [Claude Native Cybersecurity 产品](https://www.pwc.com/us/en/technology/alliances/anthropic.html)同时解决 CISO 提出的两个问题：让 AI 安全进入生产环境，以及实现网络职能本身的现代化。Secure AI Adoption 让企业从沙箱走向生产只需数周而非数个季度，并附带部署、治理和审计证据，帮助 CISO 和 CRO 有信心地为团队引入创新。Scaled Frontier Defense 把 Opus 驱动的智能体推理整合进现有的漏洞管理、检测、安全工程和 GRC 工作流，在既定防护栏和可审计性之内实现自主执行。

> 「这是网络安全的决定性时刻：AI 驱动的转型已成为保持韧性与竞争力的必要条件。」——Morgan Adamski，PwC 美国网络、数据与技术负责人

## 不断壮大的生态

BCG、Infosys 和 SentinelOne 也正在基于 Opus 构建防御性网络产品，随着它们陆续推出，我们会分享更多细节。

上述每一个产品都建立在同一套 Opus 底层能力之上：对代码进行推理、理解哪些暴露会转化为现实世界的风险，以及维持长时间的智能体工作流。我们很高兴与这些伙伴合作，通过最适合各团队的接入点，把前沿防御带给更多安全团队。

*进一步了解 [Claude 在安全场景中的应用](https://claude.com/solutions/security)。*
