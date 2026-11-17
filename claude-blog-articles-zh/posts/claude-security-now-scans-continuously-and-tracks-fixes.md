---
title: "Claude Security 现可持续扫描并跟踪修复进度"
title_en: "Claude Security now scans continuously and tracks fixes"
date: 2026-10-21
source: https://claude.com/resources/articles/claude-security-now-scans-continuously-and-tracks-fixes
crawled: 2026-11-17
translated: 2026-11-17
---

# Claude Security 现可持续扫描并跟踪修复进度

> 原文：[Claude Security now scans continuously and tracks fixes](https://claude.com/resources/articles/claude-security-now-scans-continuously-and-tracks-fixes) · Claude 博客

Claude Security 现在能随着代码变化跟上你的代码仓库，跟踪发现的问题直到它们被修复，从团队补充的上下文中学习，并通过 API 和 MCP 连接你现有的工具。现面向 Claude Enterprise 客户开放公测。

自 [Claude Security](https://claude.com/product/claude-security) [于今年 4 月进入公测](https://claude.com/resources/articles/claude-security-public-beta)以来，已有数千家组织用它发现了超过一百万个漏洞。

Claude Security 不再等有人手动发起扫描，而是随着代码变化持续跟进你的代码仓库，跟踪哪些发现已被修复，并利用团队告知的环境信息来判断什么才重要。Claude Security 由我们完整的模型家族驱动，包括 Claude Mythos，且无需 Cyber Verification Program 访问权限。

最新版 Claude Security 今日起面向 Claude Enterprise 客户开放公测。组织每月可获得 25,000 美元的免费使用额度，连续两个月。该优惠适用于截至 2026 年 12 月 31 日的使用量。完整条款见[帮助中心](https://support.claude.com/en/articles/14661296-use-claude-security)。

## **持续监控，跟上代码变化**

一次扫描只捕捉一个瞬间，而代码每天都在变。客户团队告诉我们，他们希望覆盖范围能始终保持最新，而不用谁去安排扫描。

创建一个项目，通过 Claude GitHub 应用（包括 GitHub Enterprise Server）连接代码仓库，或使用来自 GitLab 及其他 Git 提供方的访问令牌连接，并为每个仓库选择分支和范围。Claude 会先跑一次深度基线扫描，之后根据变更的风险与复杂度定期扫描变更，让你手上的发现列表始终贴近代码的当前状态。

一个项目可以包含多个仓库，因此 Claude 能捕捉存在于服务之间的问题，比如后端信任了本应由客户端校验的输入。

![Claude Security 界面](https://assets.claude.com/fe39204ec42e8d48c853bf16bb08bdb19bf99a22.png)

## **修复上线后，发现即被标记为已修复**

大多数修复发生在发现问题的那款工具之外。Claude Security 会把未关闭的发现与发生变更的代码做比对，修复一旦落地就把它标记为已修复——无论你的团队是在 Claude Code 里修的，还是在别的流程里修的。如果 Claude Security 之后再次发现该问题，这条发现会自动重新打开。

![Claude Security 界面](https://assets.claude.com/579a7fb43c95d281cf38ba2dafca75eea40a7058.png)

## **团队的知识塑造扫描结果**

每个环境都有扫描器仅凭代码看不到的控制措施。客户团队希望能有一种方式把这些控制措施告诉 Claude Security，并让它能跨相互依赖的服务进行审视。现在，每个项目都有一个知识库，你可以在这里描述代码如何部署、适用哪些安全策略，以及团队里任何一位新来的安全工程师都需要了解的信息。

![Claude Security 界面](https://assets.claude.com/440f4c1037a629695ec66eb0a17c218782b51d35.png)

Claude Security 还会根据你的代码生成一份威胁模型，供团队审阅和编辑。后续扫描会使用这些威胁模型来判断哪些东西值得标记。补充的上下文还能帮助 Claude Security 跳过你的环境已经处理掉的风险。

## **每条发现都附带严重程度与利用路径**

每条发现都会附带一个严重程度评级（依据你项目的威胁模型判定），以及关于攻击者如何抵达易受攻击代码的说明，让团队优先修复那些确实可达的问题。部分发现还会包含攻击路径示意图。

![Claude Security 界面](https://assets.claude.com/58c85ec0105dd3b16b367ae71e70c14db55e6d4f.png)

## **发现直达你的工具，并为大规模推广提供管控**

新的 API 让你可以把 Claude Security 集成进现有工作流。你可以列出并读取项目与发现，将发现标记为已解决或重新打开，创建并管理项目及其代码仓库。用户可以在 Claude Security 设置中创建个人访问令牌，该令牌只能看到和修改该用户本人可访问的内容。Webhook 还可以在新发现产生时通知你的系统。

Claude Security 也以 MCP 连接器的形式在 [Claude.ai](http://claude.ai) 和 Claude Code 中提供。工程师可以调出一条发现、就此询问 Claude、开始修复，并在同一次会话中把它标记为已解决。

新增的基于角色的访问控制让管理员可以决定谁可以查看项目、分诊（triage）发现、创建项目。组织可以把 Claude Security 开放给更多拥有代码的团队，而不必让所有人都有创建项目的权限。

## **快速开始**

最新版 [Claude Security](http://claude.ai/security) 自今日起面向 Claude Enterprise 客户开放公测。管理员可以在管理控制台中启用它，并设置团队中谁可以访问。

使用[快速开始指南](https://academy.claude.com/tutorials/getting-started-with-claude-security)设置你的第一个项目，更多细节请访问[帮助中心](https://support.claude.com/en/articles/14661296-use-claude-security)。

*组织每月可获得 25,000 美元的免费使用额度，连续两个月。该优惠适用于截至 2026 年 12 月 31 日的使用量。完整条款见[帮助中心](https://support.claude.com/en/articles/14661296-use-claude-security)。*

> "Claude Security 发现了许多同时期进行的传统渗透测试漏掉的实质性问题，其中若干个若被在野利用，会造成重大影响。"

Jon Donovan，软件工程师，IonQ

> "Claude Security 扫描过一次我们的代码以建立基线。现在它会随着代码变化持续跟进，我们团队直接在 Claude 里修复问题，不必再切换到另一个工具。"

Jake Meredith，产品安全，Gusto

> "API 和 MCP 的加入改变了游戏规则，也将是 IonQ 产品安全团队进一步把 Claude Security 投入实际运营的路径。"

Joe Coniglio，安全工程师，IonQ

> "Claude Security 发现了若干我们其他工具都没抓到的逻辑缺陷。当我们把自己的风险策略写进威胁模型、聚焦外部用户实际能触及的范围之后，发现结果就与我们的优先级排序方式一致了，而不只是看一个严重性分数。"

Nathan Hunstad，安全总监，Vanta
