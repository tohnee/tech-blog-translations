---
title: "为安全团队提供更强的 Claude Enterprise 可见性与控制力"
title_en: "More visibility and control over Claude Enterprise for security teams"
date: 2026-11-05
source: https://claude.com/resources/articles/claude-enterprise-security-updates
crawled: 2026-11-17
translated: 2026-11-17
---

# 为安全团队提供更强的 Claude Enterprise 可见性与控制力

> 原文：[More visibility and control over Claude Enterprise for security teams](https://claude.com/resources/articles/claude-enterprise-security-updates) · Claude 博客

[Claude Enterprise](https://claude.com/solutions/enterprise) 新增了安全与管理功能，包括安全中心（security center）、正式可用的[推理钩子（inference hooks）](https://claude.com/resources/articles/claude-enterprise-inference-hooks)、集中管理（centralized management），以及更多访问控制能力。

要查看 Claude 的配置情况，安全中心会展示贵组织的 Claude 设置与 Anthropic 推荐配置之间的对比。要落实你们的策略，推理钩子会把提示词和工具调用发送到你们的数据安全工具进行检查。要管理访问权限，集中管理为公司提供一个统一的管理员控制台来管理全公司设置；新的访问控制让你可以通过 Admin API 将会员登出、自行管理 IP 允许列表，并可在受管计算机的 Claude Desktop 中屏蔽个人及其他外部 Claude 账户，以帮助防止影子 IT。

我们最近还宣布了端点检测与响应（EDR）集成，可在用户计算机上的统一 Claude（[unified Claude](https://claude.com/resources/articles/unified-claude-enterprise)）和 Cowork 虚拟机中运行贵组织的传感器。

安全团队需要看清 Claude 是如何配置的、它在公司设备上做了什么，以及人们工作过程中数据是如何被处理的。这些功能正好赋予他们这种可见性与控制力。

## 安全中心：在一处审阅你的 Claude 安全设置

![Claude 组织设置中的安全态势仪表盘，16 项控制中有 13 项已通过。](https://assets.claude.com/893acaa9f8b564cda630ed280d69e5c7d2bca5f7.png)

安全团队可以在一个页面上审阅 Claude 针对对话、Cowork 和 Claude Code 的安全设置，而不必逐项检查。安全中心是组织设置中的新页面，会把现有设置与 Anthropic 的推荐配置进行对比，让团队看清需要改什么、在哪里改。

对于每一项控制，安全中心都会显示当前值、推荐值（如果有），以及可以修改该项设置的链接。它还会标明哪些设置是新增的或近期变更的。安全中心在每次页面加载时检查配置，因此自动检查的控制项反映的是当前设置。已开通 Compliance API 的组织可以通过该 API 读取同样的结果。

证明（attestations）为管理员提供了一个用于安全评审的共享工作区。他们可以一次性共同走完整个流程：记录每项控制的当前状态、接受风险，并在同一个地方标记问题。

你可以把安全中心页面下载为报告，分享给审计人员和相关利益方。报告会标出哪些控制项是由页面自动检查的，哪些是由所有者（Owner）确认的。安全中心是基于 Anthropic 建议的指导性内容，不是认证，也不保证符合任何法律或标准。

## 推理钩子

推理钩子将 Claude 与贵组织已经在用的数据安全工具连接起来，使数据防泄漏（DLP）和安全策略能够在人们工作过程中作用于提示词和工具调用。

钩子分两类，现均已正式可用：

* 提示词钩子（prompt hooks）将受支持的 Claude 产品中的提示词发送到你们的安全工具进行检查。
* 工具调用前钩子（pre-tool-call hooks）在受支持的 Claude 产品中，于工具调用执行之前对其进行检查。

钩子与安全厂商配合工作。你的团队可以沿用已经写好的策略，并将其应用到 Claude 上。

## 集中管理：一个控制台管理全组织的身份与访问

集中管理为你的父组织（parent organization）——代表公司在 Claude Enterprise 和 Claude Platform 各组织之上的统属层级——提供位于 admin.claude.com 的专属管理员控制台。管理员可在此对父组织下的各组织统一管理全公司设置，而不必逐个进入各组织设置。这些设置包括单点登录、目录同步（SCIM）、域名验证、群组和 Compliance API 密钥。

控制台在一处展示父组织下的所有组织，并新增两种角色。父组织所有者（parent organization owner）可以管理父组织层级的一切事务，包括谁担任所有者和管理员角色。父组织管理员（parent organization admin）除这些角色分配之外，可以管理其他所有事务。

公司还可以连接多个身份提供商，每个提供商都有各自的单点登录和 SCIM 配置。被收购的公司可以保留现有提供商，你的团队也可以一次迁移一个域名到新的提供商。

每个组织仍保留自己的成员、角色、设置和组织级安全控制（如 IP 允许列表、租户限制和会话时长）。父组织角色默认不会授予组织内部的访问权限，但在父组织层级创建的 Compliance API 密钥可以跨组织读取数据。

## 访问控制：会员登出与影子 IT 防范

安全团队现在只需一次 Admin API 调用，就能将会员登出 Claude，而无需将其移出组织。该调用会终止该会员在所有浏览器和设备上的登录会话，Claude Code 等应用需要重新登录。它不会终止 API 密钥、已在运行的云会话或定时例程，之后该会员也可以重新登录。

Enterprise 管理员现在可以自行设置和管理 IP 允许列表，无需经过 Anthropic。IP 允许列表将大多数 Claude 产品的访问限制在贵组织批准的 IP 地址范围内。

管理员现在可以设置最常用的 Claude Desktop 设置，无需通过设备管理下发。为帮助防止影子 IT，管理员还可以在受管计算机的 Claude Desktop 中屏蔽个人及其他外部 Claude 账户。所有者还可以限制人们可以在 Claude 中使用哪些工作区文件夹。

## Cowork 与统一 Claude 中的端点检测与响应（EDR）

当 Cowork 和统一 Claude 在本地工作时，它们会在用户计算机上隔离的虚拟机中运行 shell 命令和代码，以获得额外保护。这种隔离有助于保护设备，而安全团队希望对这个虚拟机拥有与端点其他位置同等的可见性。

管理员现在可以在 Cowork 虚拟机内运行本组织的 EDR 传感器。传感器会把虚拟机中的活动上报到安全团队已经在监控的同一个控制台。此功能覆盖用户计算机上的虚拟机，不覆盖云端的 Cowork 会话。

管理员通过 macOS 和 Windows 上的设备管理来设置该集成。每次虚拟机启动时，Claude 会先验证来自 EDR 厂商的传感器包签名，然后再安装。传感器以检测模式运行：向安全团队上报活动，但不阻断。该集成适用于受支持的 EDR 厂商，名单列于[帮助中心](https://support.claude.com/en/articles/17828685-run-your-endpoint-detection-and-response-edr-sensor-in-claude-cowork-on-claude-desktop)。

## 开始使用

这些功能面向 Claude Enterprise 提供，测试期间的部分例外情况列于[帮助中心](https://support.claude.com/en)。

[安全中心](https://support.claude.com/en/articles/18246629-review-your-organization-s-security-posture-with-the-security-center)处于测试（beta）阶段。[推理钩子](https://support.claude.com/en/articles/16059458-inference-hooks-overview)（包括提示词钩子和工具调用前钩子）已正式可用。管理员可以在组织设置中管理推理钩子和安全中心。

[集中管理](https://support.claude.com/en/articles/18232924)也处于测试阶段。开始设置时，父组织下任一组织的管理员访问 admin.claude.com 并提名父组织管理员。其他组织的管理员进行审阅和批准，最后一次批准即完成设置。设置无法撤销，因此请在开始前确定好父组织管理员人选。

通过 Admin API [将会员登出](https://support.claude.com/en/articles/13133750-manage-members-on-team-and-enterprise-plans#h_3cba7d14e5)和[自助式 IP 允许列表](https://support.claude.com/en/articles/13200993-restrict-access-to-claude-with-ip-allowlisting)均处于测试阶段。所有者可以在组织设置中管理 [Claude Desktop 设置](https://support.claude.com/en/articles/12622667-enterprise-configuration-for-claude-desktop#h_21135034c8)，同样处于测试阶段。

Cowork 中的[端点检测与响应](https://support.claude.com/en/articles/17828685-run-your-endpoint-detection-and-response-edr-sensor-in-claude-cowork-on-claude-desktop)在 macOS 和 Windows 上处于测试阶段，适用于 Claude Team 和 Enterprise；同时也适用于 Amazon Bedrock、Google Cloud Vertex AI 和 Microsoft Foundry 上的 Claude 桌面应用，通过 MDM 为受支持的厂商部署。
