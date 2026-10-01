---
title: "携手 NVIDIA，让企业更好地管控自己的 AI 智能体"
title_en: "Giving companies more control over their AI agents, with NVIDIA"
date: 2026-09-28
source: https://claude.com/blog/giving-companies-more-control-over-their-ai-agents-with-nvidia/
crawled: 2026-10-01
translated: 2026-10-01
---

# 携手 NVIDIA，让企业更好地管控自己的 AI 智能体

> 原文：[Giving companies more control over their AI agents, with NVIDIA](https://claude.com/blog/giving-companies-more-control-over-their-ai-agents-with-nvidia/) · Claude 博客

NVIDIA 今日发布了 [Open Agent Safety Platform](https://nvidianews.nvidia.com/news/open-agent-safety-platform)，这是一个用于强化 AI 安全的开放软件平台与参考系统设计。Anthropic 已与 NVIDIA 展开合作，为智能体技术栈引入额外的安全与管控层。

Claude Managed Agents 是一套用于大规模构建和部署生产级智能体的可组合 API，它把智能体所需的凭证保存在凭证金库（vault）中，智能体本身永远接触不到这些凭证。开源的 NVIDIA OpenShell 软件则用于管控智能体在工作过程中能执行什么、能访问什么。同时使用 Managed Agents 与 OpenShell 的客户可以限制智能体能做的事情、审查智能体做了什么，并确认这些限制确实到位。

企业正从「用 AI 回答问题」走向部署智能体——这些智能体处理跨业务部门的复杂工作、使用专有数据，并代表用户采取行动。随着模型不断进步，智能体的用途越来越广，获得的访问权限也越来越多。智能体的权限越大，企业就越需要对其行为进行管控和检查。

## **分层防护**

防护始于模型内部的安全护栏。Managed Agents 和 NVIDIA Open Shell 在模型之外施加限制，作用于智能体的所作所为。每一层都设计为独立执行各自的限制，因此防护并不依赖任何单一一层。这些防护层是模块化的，企业可以按自身环境选择采用哪些。

## **Claude Managed Agents 负责执行工作并保管凭证**

在 Managed Agents 中，智能体循环（agent loop）与沙箱——即实际执行工作的隔离环境——运行在不同的服务器上。凭证，也就是密码和访问密钥，保存在单独的凭证金库中，因此智能体永远接触不到它们。

Managed Agents 还提供审计追踪（audit trail），记录每个智能体做过什么，并支持与企业现有的访问控制体系集成。企业可以自带沙箱环境，并自行选择沙箱在哪里运行、以何种方式运行。

## **NVIDIA OpenShell 决定智能体能访问什么**

[OpenShell](https://www.nvidia.com/en-us/ai/openshell/) 是 NVIDIA 推出的开源安全运行时软件。它治理并监控所有 AI 智能体的行为，并对每一个动作执行策略。除非有规则明确允许，OpenShell 一律拦截。它会检查智能体尝试使用的每一个工具，并对智能体访问的文件、网络连接和数据应用规则。这些规则在智能体之外执行，而且 OpenShell 会记录它允许或拦截的每一个决定。

团队可以从极窄的权限起步，审查日志，再借助 Claude 逐步收紧规则，直至只保留任务所需的最小访问权限。随后，OpenShell 的策略证明器（policy prover）会用数学证明来确认：在团队写下的规则之下，智能体到底能访问哪些资源。

## **Claude Managed Agents 包含什么**

- 生产级智能体：安全沙箱、身份验证与工具执行都已为你打理妥当。
- 长时运行的会话：可自主连续工作数小时，进度和产出即使遭遇断连也会保留。
- 多智能体编排：智能体可以启动并指挥其他智能体，将复杂工作并行化。
- 可信治理：让智能体在内建的受限权限、身份管理与执行追踪保障下访问真实系统。

## **团队如何使用 Managed Agents**

- [Notion](https://claude.com/customers/notion-qa) 让团队在自己的工作区内把工作交给 Claude。工程师用它交付代码，其他员工用它制作网站和演示文稿。数十个任务可以并行运行，团队同时基于这些结果协同推进。
- [Rakuten](https://claude.com/customers/rakuten-qa) 在工程、产品、销售、市场和财务等部门运行专职智能体，每一个都在一周内部署完成。
- [Asana](https://claude.com/customers/asana-qa) 打造了 AI Teammates——在 Asana 项目中与人并肩工作、承接任务并起草交付物的智能体。借助 Managed Agents，该团队以远超从前的速度上线了高级功能。

## **正式可用**

Managed Agents 现已正式可用。它可以在由你掌控的沙箱中运行——既可以在你自己的基础设施上运行，也可以通过托管服务提供商运行。NVIDIA OpenShell 采用 Apache 2.0 许可证开源，可在 [GitHub](https://github.com/NVIDIA/OpenShell) 和 NVIDIA 的[开发者资源页面](https://docs.nvidia.com/openshell/latest/about/overview)获取。

FAQ（常见问题）
