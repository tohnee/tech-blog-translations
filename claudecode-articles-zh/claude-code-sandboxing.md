---
title: "超越权限提示：让 Claude Code 更安全、更自主"
title_en: "Beyond permission prompts: making Claude Code more secure and autonomous"
source: https://www.anthropic.com/engineering/claude-code-sandboxing
published: 2025-10-20
crawled: 2026-09-11
translated: 2026-09-11
---

# 超越权限提示：让 Claude Code 更安全、更自主

> 原文：[Beyond permission prompts: making Claude Code more secure and autonomous](https://www.anthropic.com/engineering/claude-code-sandboxing) · Anthropic Engineering Blog

在 [Claude Code](https://www.claude.com/product/claude-code) 中，Claude 与你并肩写代码、跑测试、调试，浏览你的代码库、编辑多个文件、运行命令验证自己的工作。给 Claude 这么大的代码库和文件访问权会带来风险，在提示注入的情况下尤其如此。

为帮助应对这一点，我们在 Claude Code 中推出了两个构建于沙箱机制之上的新特性，二者都旨在为开发者提供更安全的工作环境，同时让 Claude 更自主地运行、更少弹出权限提示。在内部使用中，我们发现沙箱机制安全地减少了 84% 的权限提示。通过划定 Claude 可以自由工作的明确边界，它们同时提升了安全性与自主性。

### **保障 Claude Code 用户的安全**

Claude Code 运行在基于权限的模型上：默认只读，即在做出修改或运行任何命令之前先征求许可。也有一些例外：我们自动放行 echo、cat 这类安全命令，但大多数操作仍需明确批准。

不停地点「批准」会拖慢开发周期，还会导致「批准疲劳」——用户可能不再细看自己批准的到底是什么，反而让开发变得更不安全。

为此，我们为 Claude Code 推出了沙箱机制。

## **沙箱机制：更安全、更自主的路线**

沙箱机制预先划定边界，Claude 在边界内可以更自由地工作，而不必为每个动作请求许可。启用沙箱后，权限提示大幅减少，安全性同时提升。

我们的沙箱方案构建在操作系统级特性之上，提供两重边界：

1. **文件系统隔离**：确保 Claude 只能访问或修改特定目录。这对防止被提示注入的 Claude 修改敏感系统文件尤其重要。
2. **网络隔离**：确保 Claude 只能连接获得批准的服务器。这防止被提示注入的 Claude 外泄敏感信息或下载恶意软件。

值得注意的是，有效的沙箱必须*同时*具备文件系统隔离与网络隔离。没有网络隔离，一个被攻陷的智能体可以外泄 SSH 密钥这类敏感文件；没有文件系统隔离，一个被攻陷的智能体可以轻松逃出沙箱获得网络访问。正是两种技术并用，我们才能为 Claude Code 用户提供更安全也更快捷的智能体体验。

### Claude Code 的两个新沙箱特性

#### **沙箱化 bash 工具：无需权限提示的安全 bash 执行**

我们推出[一个新的沙箱运行时](https://docs.claude.com/en/docs/claude-code/sandboxing)（beta 研究预览版），让你精确定义智能体可以访问哪些目录和网络主机，而无需启动和管理容器的开销。它可以用来沙箱化任意进程、智能体和 MCP 服务器。它同时以[开源研究预览](https://github.com/anthropic-experimental/sandbox-runtime)的形式提供。

在 Claude Code 中，我们用这个运行时来沙箱化 bash 工具，让 Claude 在你设定的边界内运行命令。在安全沙箱内，Claude 可以更自主地运行、无需权限提示即可安全执行命令。如果 Claude 试图访问沙箱*之外*的东西，你会立即收到通知，可以选择是否允许。

我们把它构建在 [Linux bubblewrap](https://github.com/containers/bubblewrap) 和 macOS seatbelt 等操作系统级原语之上，在 OS 层面强制执行这些限制。它们覆盖的不只是 Claude Code 的直接交互，还包括命令派生的任何脚本、程序或子进程。如上所述，这个沙箱同时强制执行：

1. **文件系统隔离**：允许对当前工作目录的读写访问，但阻止修改目录之外的任何文件。
2. **网络隔离**：只允许通过连接到沙箱外代理服务器的 unix 域套接字访问互联网。这个代理服务器对进程可连接的域名实施限制，并处理对新域名的用户确认。如果你想要更高的安全性，我们还支持自定义这个代理，对出站流量施加任意规则。

两个组件都可配置：你可以轻松选择允许或禁止特定文件路径或域名。

![This image illustrations how sandboxing in Claude Code works.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F0d1c612947c798aef48e6ab4beb7e8544da9d41a-4096x2305.png&w=3840&q=75)

Claude Code 的沙箱架构用文件系统和网络控制隔离代码执行：自动放行安全操作、拦截恶意操作，只在必要时请求许可。

沙箱机制确保即便提示注入得逞，也被完全隔离，无法波及用户的整体安全。这样，被攻陷的 Claude Code 偷不走你的 SSH 密钥，也无法向攻击者的服务器回传信息。

要上手这个特性，在 Claude Code 中运行 /sandbox，并查看关于我们安全模型的[更多技术细节](https://docs.claude.com/en/docs/claude-code/sandboxing)。

为了让其他团队更容易构建更安全的智能体，我们已[开源](https://github.com/anthropic-experimental/sandbox-runtime)了这个特性。我们相信其他开发者也应考虑为自己的智能体采用这项技术，以增强其智能体的安全态势。

#### **网页版 Claude Code：在云端安全运行 Claude Code**

今天我们同时发布[网页版 Claude Code](https://docs.claude.com/en/docs/claude-code/claude-code-on-the-web)，让用户在云端的隔离沙箱中运行 Claude Code。网页版 Claude Code 在隔离沙箱中执行每个会话，以安全稳妥的方式完整访问其所在的服务器。这个沙箱的设计确保敏感凭证（如 git 凭证或签名密钥）永远不与 Claude Code 同处沙箱之内。这样，即便沙箱中运行的代码被攻陷，用户也不会受到进一步伤害。

网页版 Claude Code 使用一个自定义代理服务，透明地处理所有 git 交互。在沙箱内部，git 客户端用一个特制的、范围受限的凭证向该服务认证。代理验证这个凭证以及 git 交互的内容（例如确保它只推送到配置的分支），然后附上正确的认证 token，再把请求发给 GitHub。

![This illustration depicts how Claude Code on the web uses a custom proxy to handle all git interactions.](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fe8f66bcf73d9d23cae67e67776b2d31373c13050-4096x2305.png&w=3840&q=75)

Claude Code 的 Git 集成把命令经由一个安全代理路由：验证认证 token、分支名和目标仓库——在放行安全的版本控制工作流的同时，阻止未授权的推送。

## 上手指南

新的沙箱化 bash 工具和网页版 Claude Code，为用 Claude 开展工程工作的开发者同时带来了安全与生产力的实质性提升。

上手这些工具：

1. 在 Claude 中运行 `/sandbox`，查看关于如何配置沙箱的[我们的文档](https://docs.claude.com/en/docs/claude-code/sandboxing)。
2. 前往 [claude.com/code](http://claude.ai/redirect/website.v1.8d765132-6cfe-4e99-b345-873621da564c/code) 试用网页版 Claude Code。

或者，如果你在构建自己的智能体，请查看我们[开源的沙箱代码](https://github.com/anthropic-experimental/sandbox-runtime)，考虑把它集成进你的工作。期待看到你构建的东西。

想进一步了解网页版 Claude Code，请阅读我们的[发布博客](https://www.anthropic.com/news/claude-code-on-the-web)。

## 致谢

本文由 David Dworken 和 Oliver Weller-Davies 撰写，Meaghan Choi、Catherine Wu、Molly Vorwerck、Alex Isken、Kier Bradwell 和 Kevin Garcia 参与贡献。
