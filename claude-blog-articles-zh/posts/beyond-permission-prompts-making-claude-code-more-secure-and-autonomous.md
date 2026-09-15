---
title: "超越权限提示：让 Claude Code 更安全、更自主"
title_en: "Beyond permission prompts: making Claude Code more secure and autonomous"
source: https://claude.com/blog/beyond-permission-prompts-making-claude-code-more-secure-and-autonomous/
crawled: 2026-09-14
translated: 2026-09-14
---

# 超越权限提示：让 Claude Code 更安全、更自主

> 原文：[Beyond permission prompts: making Claude Code more secure and autonomous](https://claude.com/blog/beyond-permission-prompts-making-claude-code-more-secure-and-autonomous/) · Claude 博客

为了解决这一问题，我们在 Claude Code 中推出了两个构建在沙箱机制之上的新特性，二者都旨在为开发者提供一个更安全的工作环境，同时让 Claude 能够更自主地运行、产生更少的权限提示。这些特性是**原生沙箱机制**（native sandboxing）的范例：通过划定 Claude 可以在其中自由工作的明确边界，它们同时提升了安全性与自主性。

## 我们目前保障用户安全的方式

Claude Code 运行在基于权限的模型上：默认情况下它是只读的，这意味着在进行修改或运行任何命令之前，它都会先请求权限。这也有一些例外：我们使用静态分析来自动放行 echo 或 cat 这类安全命令，但大多数操作仍需明确批准。

但不断点击「批准」会拖慢开发速度，并可能导致「批准疲劳」（approval fatigue）——用户可能不再仔细关注自己批准的到底是什么。为了让 Claude Code 既更安全又更高效，我们想找到一种更好的方法。

## 沙箱机制：一种更安全、更自主的方式

沙箱机制预先划定边界，让 Claude 可以在其中更自由地工作，而不必为每个动作请求权限。

随着对 Claude Code 的这次更新，我们正在转向这一方式。我们的沙箱方案构建在操作系统级特性之上，用以实现两个新特性，每个特性都基于以下两组核心边界：

1. **文件系统隔离**，确保 Claude 只能访问或修改特定目录。这对防止被提示注入（prompt injection）的 Claude 修改敏感系统文件尤为重要。
2. **网络隔离**，确保 Claude 只能连接到经过批准的服务器。这可以防止被提示注入的 Claude 泄露敏感信息或下载恶意软件。

值得注意的是，有效的沙箱机制需要文件系统隔离与网络隔离*二者兼备*。没有网络隔离，一个被攻破的智能体可能窃取 SSH 密钥等敏感文件；没有文件系统隔离，一个被攻破的智能体则可以轻松逃出沙箱并获得网络访问权限。正是通过同时使用这两种技术，我们才能为 Claude Code 用户提供更安全的智能体体验。

### Claude Code 中的两个新沙箱特性

#### 沙箱化 bash 工具：无需权限提示的安全 bash 执行

今天，我们推出一个新的沙箱运行时（sandbox runtime），目前处于研究预览阶段，它让你能够精确界定你的智能体可以访问哪些目录和网络主机，而无需承担启动和管理容器的开销。它可以用来对任意进程、智能体和 MCP 服务器进行沙箱化。现已作为开源研究预览在此发布：[GitHub 链接？]

在 Claude Code 中，我们使用这个运行时对 bash 工具进行沙箱化，让 Claude 能够在你设定的边界内运行命令。这些命令默认更安全，需要的用户权限提示更少，因此 Claude 可以更自主地运行。如果 Claude 试图访问沙箱*之外*的东西，你会立即收到通知，并可以选择是否允许。

我们将其构建在操作系统级原语之上，例如 [Linux bubblewrap](https://github.com/containers/bubblewrap) 与 MacOS seatbelt，从而在操作系统层面强制执行这些限制。它们覆盖的不仅是 Claude Code 的直接交互，还包括该命令派生的任何脚本、程序或子进程。

如上所述，这个沙箱同时强制执行：

1. **文件系统隔离**，允许对当前工作目录的读写访问，但阻止修改目录之外的任何文件。
2. **网络隔离**，只允许通过连接到运行在沙箱之外的代理服务器的 unix 域套接字进行互联网访问。这个代理服务器对进程可以连接的域名实施限制，并处理对新域名的用户确认。如果你想进一步提升安全性，我们甚至支持自定义这个代理，对出站流量实施任意规则。

两个组件都可配置：你可以轻松选择允许或禁止特定的文件路径或域名。

沙箱机制确保即便提示注入得手，其影响也被完全隔离，无法波及用户的整体安全。这样一来，被攻破的 Claude Code 无法窃取你的 SSH 密钥，也无法向攻击者的服务器回传信息。

要开始使用这一特性，请运行：`claude --sandbox`，并在此阅读关于我们安全模型的更多技术细节。

为了让其他团队更容易构建更安全的智能体，我们已开源 [XXX]。我们相信，其他 AI 公司也应考虑为自己的智能体采用这项技术，以增强其智能体的安全态势。

#### Claude Code on the web：在云端安全地运行 Claude Code

今天，我们同时发布 [Claude Code on the web](https://docs.claude.com/en/docs/claude-code/claude-code-on-the-web)，让用户能够在云端的隔离沙箱中运行 Claude Code。Claude Code on the web 在隔离沙箱中执行每个 Claude Code 会话，让其在安全可靠的前提下对所在服务器拥有完整访问权限。我们设计的这套沙箱确保敏感凭证（如 git 凭证或签名密钥）永远不会进入沙箱环境。这样，即使沙箱中运行的代码被攻破，用户也能免受进一步的损害。

Claude Code on the web 使用一个自定义代理服务来透明地处理所有 git 交互。在沙箱内部，git 客户端使用一个定制的作用域凭证（scoped credential）向该服务进行身份验证。代理会验证这个凭证以及 git 交互的内容（例如确保只推送到配置的分支），然后在把请求发送给 GitHub 之前附上正确的认证令牌。

## 开始使用

我们全新的沙箱化 bash 工具与 Claude Code on the web，为在工程工作中使用 Claude 的开发者带来了安全性与生产力的双重显著提升。

要开始使用这些工具：

1. 运行 `claude --sandbox`，并查阅关于如何配置这个沙箱的[我们的文档](https://docs.claude.com/en/docs/claude-code/sandboxing)。
2. 前往 [claude.com/code](http://claude.ai/code) 试用 Claude Code on the web。

或者，如果你正在构建自己的智能体，请查看我们开源的沙箱代码，并考虑把它集成到你的工作中。我们期待看到你构建出的一切。

FAQ（常见问题）

要开始使用 Claude Code，你需要设置一个 API 密钥并按照提供的文档操作。文档会指导你完成高效发起请求与处理响应的全过程。

从聊天机器人到自动化内容生成，Claude 的多功能性使它成为企业和开发者的宝贵工具。

用户反馈在 Claude 的改进中扮演着关键角色。通过分析用户交互，开发者可以找出需要改进的地方并实施必要的变更。
