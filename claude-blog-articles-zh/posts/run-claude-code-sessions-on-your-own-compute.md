---
title: "Claude Code 的自托管环境"
title_en: "Self-hosted environments for Claude Code"
source: https://claude.com/blog/run-claude-code-sessions-on-your-own-compute/
crawled: 2026-09-14
translated: 2026-09-14
---

# Claude Code 的自托管环境

> 原文：[Self-hosted environments for Claude Code](https://claude.com/blog/run-claude-code-sessions-on-your-own-compute/) · Claude 博客

自托管环境（self-hosted environments）现已进入公测（public beta），让你可以在自己的基础设施上运行 Claude Code 会话。你可以从网页端、移动端、桌面端或例行任务（routine）发起会话，它会在你的网络内部运行，与你的内部服务、工具链和安全防护措施同处一地，而不是运行在 Anthropic 托管的基础设施上。

对于大多数企业，我们强烈建议使用我们的托管服务，以获得运营上的简便——无需运行或维护任何基础设施。自托管环境适合那些因网络、工具或合规要求而需要把智能体执行保留在自己控制的基础设施上的团队。如果你选择这条路线，请规划好工程人力，负责初始设置和持续维护。

### **为何选择自托管**

在预览计划（preview program）中，我们看到一些组织基于以下几个关键原因采用自托管环境：

- **网络访问**：会话在你的网络内部运行，可以访问内部服务、数据库和镜像仓库，而无需把它们暴露到公共互联网上
- **可定制性**：在你的环境中预装编译器、SDK 和内部 CLI，让每个会话一启动就具备构建能力
- **合规性**：源代码和构建产物保留在你控制的基础设施上

“自托管环境让我们能够把 Claude Code 集成到现有开发工作流中，同时保持我们的安全与运营管控。这种配置意味着 Claude 可以生成 PR、协助修复 CI 问题，并响应开发者工作流事件，算力还可以按需扩展。Claude 理解我们的代码库，非常契合我们工程团队的构建方式。”

### **数据留在你的基础设施上**

仓库的检出副本、构建产物、密钥，以及会话创建或修改的任何文件，都保留在你自行配置的基础设施上。

而对话本身——包括提示、回复和工具结果（其中可能包含 Claude 读取的代码）——会发送给 Anthropic 进行推理，会话记录也会被存储，以便可以从任意入口继续该会话。

### **工作原理**

使用自托管环境时，你需要部署一组[运行器（runner）](https://code.claude.com/docs/en/self-hosted-environments#key-concepts)。这些长期运行的进程会领取会话，并为每个[会话](https://code.claude.com/docs/en/self-hosted-environments#session-lifecycle)启动一个 Claude Code 进程。运行器有两种模式。

1. **固定模式（Fixed）**：你保持一定数量的运行器常驻运行，会话被分配到它们之上。
2. **按需模式（On-demand）**：编排器（orchestrator）监视排队的会话，会话到达时启动运行器，工作结束时将其停止，使容量随需求变化。

一个运行器可以同时服务多个会话，但每个会话都在自己的检出副本中运行，因此不同开发者和账户之间的工作彼此隔离。来自所有受支持入口的会话都会路由到同一个环境，因此你只需配置一次，团队无论从哪里发起会话都能使用。

**注意**：自托管环境与[远程控制（Remote Control）](https://code.claude.com/docs/en/remote-control)不同，后者让开发者可以用手机或浏览器继续在自己机器上运行的会话。使用远程控制的会话在所属机器停止运行时即告结束，并与运行 `claude` 命令的用户绑定；而自托管环境则在由你的平台团队运营的共享基础设施上运行会话，任何用户都可以使用。

### **开始使用**

自托管环境现已进入公测，面向 Claude Team 和 Enterprise 计划的组织开放。该功能默认关闭，使用 ZDR（零数据保留，zero data retention）的组织无法使用。

请规划由平台团队、开发者体验团队或开发者效能团队负责初始设置与持续运营，包括构建和维护运行器镜像、更新运行器，以及在你使用按需模式时运行编排器。

更多信息请参阅[文档](https://code.claude.com/docs/en/self-hosted-environments)。欢迎通过 [GitHub](https://github.com/anthropics/claude-code/issues) 或你的 Anthropic 客户团队分享反馈。

FAQ（常见问题）
