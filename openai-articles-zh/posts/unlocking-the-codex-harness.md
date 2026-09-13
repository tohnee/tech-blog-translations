---
title: "解锁 Codex 执行框架：我们如何构建 App Server"
title_en: "Unlocking the Codex harness: how we built the App Server"
source: https://openai.com/index/unlocking-the-codex-harness/
crawled: 2026-09-13
category: engineering
translated: 2026-09-13
---

# 解锁 Codex 执行框架：我们如何构建 App Server

> 原文：[Unlocking the Codex harness: how we built the App Server](https://openai.com/index/unlocking-the-codex-harness/) · OpenAI 博客

OpenAI 的编程智能体 Codex 存在于许多不同的界面形态中：[网页应用](https://chatgpt.com/codex)、[CLI](https://github.com/openai/codex)、[IDE 扩展](https://developers.openai.com/codex/ide/)，以及[全新的 Codex macOS 应用](https://openai.com/index/introducing-the-codex-app/)。在底层，它们都由同一个 Codex 执行框架（harness）驱动——即支撑所有 Codex 体验的智能体循环与逻辑。它们之间的关键纽带是什么？是 [Codex App Server](https://developers.openai.com/codex/app-server)——一个对客户端友好、双向的 JSON-RPC1 API。

在本文中，我们将介绍 Codex App Server，并分享到目前为止我们在「把 Codex 的能力引入你的产品、帮助用户增强工作流」方面的最佳实践心得。我们会讲解 App Server 的架构与协议，以及它如何与不同的 Codex 界面形态集成；还会给出充分利用 Codex 的技巧——无论你想把 Codex 变成代码评审者、SRE 智能体，还是编程助手。

## App Server 的起源

在深入架构之前，先了解 App Server 的来历会很有帮助。最初，App Server 只是一种在不同产品间复用 Codex 执行框架的实用手段，后来逐渐演化为我们的标准协议。

Codex CLI 最初是一个 TUI（终端用户界面），也就是说通过终端来访问 Codex。当我们构建 VS Code 扩展（一种对 IDE 更友好的、与 Codex 智能体交互的方式）时，我们需要一种方式来使用同一个执行框架，以便从 IDE UI 驱动同一个智能体循环，而无需重新实现它。这意味着要支持请求/响应之外更丰富的交互模式，例如探索工作区、在智能体推理时流式输出进度，以及生成 diff。我们首先尝试把 [Codex 暴露为 MCP 服务器](https://github.com/openai/codex/pull/2264)，但事实证明，以对 VS Code 有意义的方式维护 MCP 语义非常困难。于是我们引入了一个镜像 TUI 循环的 JSON-RPC 协议，这成了 [App Server 非官方的第一版](https://github.com/openai/codex/pull/4471)。当时我们没有预料到其他客户端会依赖 App Server，所以它并没有被设计成一个稳定的 API。

在接下来的几个月里，随着 Codex 的采用不断增长，内部团队和外部合作伙伴都希望能在自己的产品中嵌入同一个执行框架，以加速其用户的软件开发工作流。例如，JetBrains 和 Xcode 希望获得 IDE 级别的智能体体验，而 Codex 桌面应用需要并行编排多个 Codex 智能体。这些需求促使我们设计一个平台级界面，让我们的产品和合作伙伴集成都能长期安全地依赖。它必须易于集成且向后兼容，也就是说我们可以在不破坏现有客户端的情况下演进协议。

接下来，我们将介绍我们如何设计架构与协议，让不同的客户端都能使用同一个执行框架。

## Codex 执行框架的内部结构

首先，让我们仔细看看 Codex 执行框架内部有什么，以及 Codex App Server 如何把它暴露给客户端。在我们上一篇 Codex [博客](https://openai.com/index/unrolling-the-codex-agent-loop/)中，我们拆解了协调用户、模型与工具之间交互的核心智能体循环。这是 Codex 执行框架的核心逻辑，但完整的智能体体验还不止于此：

**1. 线程（thread）的生命周期与持久化**。线程是用户与智能体之间的一次 Codex 对话。Codex 会创建、恢复、分叉和归档线程，并持久化事件历史，使客户端能够重新连接并渲染出一致的时间线。

**2. 配置与认证**。Codex 加载配置、管理默认值，并运行「使用 ChatGPT 登录」（Sign in with ChatGPT）等认证流程，包括凭证状态。

**3. 工具执行与扩展**。Codex 在沙箱中执行 shell/文件工具，并接入 MCP 服务器和技能（skills）等集成，使它们能在一致的政策模型下参与智能体循环。

这里提到的所有智能体逻辑（包括核心智能体循环）都位于 Codex CLI 代码库中名为「[Codex core](https://github.com/openai/codex/tree/main/codex-rs/core)」的部分。Codex core 既是一个承载所有智能体代码的库，也是一个运行时，可以启动它来运行智能体循环并管理单个 Codex 线程（对话）的持久化。

要发挥作用，Codex 执行框架必须能被客户端访问。这正是 App Server 的用武之地。

App Server 既指客户端与服务器之间的 JSON-RPC 协议，也指一个承载 Codex core 线程的常驻进程。从上图可以看到，一个 App Server 进程有四个主要组件：stdio 读取器、Codex 消息处理器、线程管理器（thread manager）以及核心线程。线程管理器为每个线程启动一个核心会话（core session），然后 Codex 消息处理器直接与每个核心会话通信，提交客户端请求并接收更新。

一个客户端请求可以产生许多事件更新，正是这些细粒度的事件让我们能够在 App Server 之上构建丰富的 UI。此外，stdio 读取器和 Codex 消息处理器充当客户端与 Codex core 线程之间的转换层。它们把客户端的 JSON-RPC 请求翻译成 Codex core 操作，监听 Codex core 的内部事件流，然后将这些底层事件转换成一小撮稳定、可直接用于 UI 的 JSON-RPC 通知。

客户端与 App Server 之间的 JSON-RPC 协议是完全双向的。一个典型的线程包含一个客户端请求和许多服务器通知。此外，当智能体需要输入（例如一次审批）时，服务器也可以主动发起请求，并暂停当前轮次（turn），直到客户端响应。

## 对话原语

接下来，我们将拆解对话原语（primitives）——App Server 协议的构建基块。为智能体循环设计 API 颇有难度，因为用户/智能体之间的交互并不是简单的请求/响应。一个用户请求可能展开为一系列结构化的动作，客户端需要忠实地呈现它们：用户的输入、智能体的增量进展、过程中产生的工件（例如 diff）。为了让这种交互流易于集成并在不同 UI 之间保持稳健，我们最终确定了三个边界清晰、生命周期明确的核心原语：

**1. 条目（item）：**条目是 Codex 中输入/输出的原子单元。条目是有类型的（例如用户消息、智能体消息、工具执行、审批请求、diff），并且每个条目都有明确的生命周期：

- `item/started`：条目开始时
- 可选的 `item/*/delta` 事件：内容流式传入时（适用于支持流式的条目类型）
- `item/completed`：条目以其最终负载落定时

这一生命周期让客户端可以在 `started` 时立即开始渲染，在 `delta` 上流式呈现增量更新，并在 `completed` 时完成落定。

**2. 轮次（turn）：**轮次是由用户输入发起的一个智能体工作单元。当客户端提交一个输入（例如「运行测试并总结失败项」）时它开始，当智能体完成对该输入的所有输出时它结束。一个轮次包含一串条目，代表这一过程中产生的中间步骤与输出。

**3. 线程（thread）：**线程是用户与智能体之间正在进行的 Codex 会话的持久容器。它包含多个轮次。线程可以被创建、恢复、分叉和归档。线程历史会被持久化，因此客户端可以重新连接并渲染一致的时间线。

现在，我们来看一个客户端与智能体之间简化后的对话，其中对话由上述原语表示：

在对话开始时，客户端与服务器需要建立 `initialize` 握手。客户端必须在任何其他方法之前发送一次 `initialize` 请求，服务器以响应作为确认。这给了服务器宣告自身能力的机会，也让双方在真正开始工作前就协议版本、功能开关与默认值达成一致。以下是 OpenAI VS Code 扩展的一个示例负载：

#### JSON

```
1{2  "method": "initialize",3  "id": 0,4  "params": {5    "clientInfo": {6      "name": "codex_vscode",7      "title": "Codex VS Code Extension",8      "version": "0.1.0"9    }10  }11}
```

服务器返回的内容如下：

#### JSON

```
1{2  "id": 0,3  "result": {4    "userAgent": "codex_vscode/0.94.0-alpha.7 (Mac OS 26.2.0; arm64) vscode/2.4.22 (codex_vscode; 0.1.0)"5  }6}
```

当客户端发起新请求时，它会先创建一个线程，再创建一个轮次。服务器会回传表示进度的通知（`thread/started` 和 `turn/started`），也会把它登记的输入作为条目回传，比如这里的用户消息。

工具调用也会作为条目回传给客户端。此外，在运行某个操作之前，服务器可以通过发送服务器请求来请求客户端审批。审批会暂停轮次，直到客户端回复「允许」（allow）或「拒绝」（deny）。下面就是 VS Code 扩展中审批流程的样子：

最后，服务器发送一条智能体消息，然后以 `turn/completed` 结束该轮次。智能体消息的 delta 事件会把消息的片段陆续流式传回，直到消息以 `item/completed` 落定。

图中的消息为便于阅读做了简化。如果你想看完整轮次的 JSON，可以从 Codex CLI 代码库运行这个测试客户端：

#### Bash

```
1codex debug app-server send-message-v2 "run tests and summarize failures"
```

## 与客户端集成

现在，让我们看看不同的客户端形态如何通过 App Server 嵌入 Codex。我们将介绍三种模式：本地应用与 IDE、Codex Web 运行时，以及 TUI。

这三种模式的传输方式都是基于 stdio 的 JSON-RPC（JSONL）。JSON-RPC 让你用自己选择的语言构建客户端绑定变得非常直接。Codex 的各个形态和合作伙伴集成已经用 Go、Python、TypeScript、Swift、Kotlin 等语言实现了 App Server 客户端。对于 TypeScript，你可以通过运行以下命令直接从 Rust 协议生成定义：

#### Bash

```
1codex app-server generate-ts
```

对于其他语言，你可以生成一个 JSON Schema 包，然后喂给你偏好的代码生成器，运行：

#### Bash

```
1codex app-server generate-json-schema
```

#### 本地应用与 IDE

本地客户端通常会打包或获取一个平台专属的 App Server 二进制文件，将其作为长驻子进程启动，并保持一个双向 stdio 通道用于 JSON-RPC。以我们的 VS Code 扩展和桌面应用为例，发布产物中包含平台专属的 Codex 二进制文件，并且固定在一个经过测试的版本上，因此客户端运行的始终是我们验证过的确切二进制。

并非每个集成方都能频繁发布客户端更新。像 Xcode 这样的一些合作伙伴选择让客户端保持稳定、并在需要时允许其指向更新的 App Server 二进制文件，从而解耦发布周期。这样，他们无需等待客户端发版就能采用服务器端的改进（例如 Codex core 中更好的自动压缩，或新支持的配置键），并推出 bug 修复。App Server 的 JSON-RPC 接口被设计为向后兼容，因此旧客户端可以安全地与更新的服务器对话。

#### Codex Web

Codex Web 使用 Codex 执行框架，但把它运行在容器环境中。一个 worker 会配置一个带有已检出工作区的容器，在容器内启动 App Server 二进制文件，并维持一个长驻的基于 stdio2 的 JSON-RPC 通道。网页应用（运行在用户浏览器标签页中）通过 HTTP 和 SSE 与 Codex 后端通信，由后者流式推送 worker 产生的任务事件。这让浏览器侧的 UI 保持轻量，同时让我们在桌面端与 Web 端拥有一致的运行时。

由于 Web 会话是短暂的（标签页会关闭、网络会中断），网页应用不能作为长时间运行任务的事实来源。把状态与进度保存在服务器上意味着即使标签页消失，工作也会继续。流式协议与已保存的线程会话让新会话可以轻松重连、从断点继续并追上进度，而无需在客户端重建状态。

#### TUI/Codex CLI

历史上，TUI 是一个「原生」客户端，它与智能体循环运行在同一个进程中，直接与 Rust core 类型对话，而不是走 app-server 协议。这让早期迭代非常快，但也让 TUI 成为一个特例形态。

既然 App Server 已经存在，我们计划[重构 TUI](https://github.com/openai/codex/pull/10192) 来使用它，使其表现得和其他客户端一样：启动一个 App Server 子进程，通过 stdio 通信 JSON-RPC，并渲染同样的流式事件与审批。这解锁了这样的工作流：TUI 可以连接到运行在远程机器上的 Codex 服务器，让智能体贴近算力，即使笔记本休眠或断网工作也能继续，同时仍然在本地提供实时更新与控制。

## 选择合适的协议

Codex App Server 将是我们今后持续维护的一等集成方式，但也有一些功能更受限的其他方式。默认情况下，我们建议客户端使用 Codex App Server 来集成 Codex，但了解不同的集成方式及其利弊仍然很有价值。以下是驱动 Codex 最常见的几种方式，以及各自适用的场景。

### JSON-RPC 协议

#### 将 Codex 作为 MCP 服务器

运行 [`codex mcp-server`](https://developers.openai.com/codex/guides/agents-sdk/)，然后从任何支持 stdio 服务器的 MCP 客户端连接（例如 [OpenAI Agents SDK](https://openai.github.io/openai-agents-js/)）。如果你已经有一套基于 MCP 的工作流，并希望把 Codex 作为一个可调用的工具来调用，这是很好的选择。缺点是你只能得到 MCP 暴露的内容，因此依赖更丰富会话语义的 Codex 特有交互（例如 diff 更新）可能无法干净地映射到 MCP 端点上。

#### 跨提供商的智能体执行框架协议

一些生态系统提供了可移植的接口，能够面向多个模型提供商和运行时。如果你想要一个能协调多个智能体的统一抽象，这可能是不错的选择。代价是这些协议往往收敛于能力的公共子集，这会让更丰富的交互更难表达，尤其是当提供商特有的工具与会话语义很重要时。这个领域变化很快，我们预计随着我们找出表示真实世界智能体工作流的最佳原语，会有更多通用标准出现（[skills](https://agentskills.io/home) 就是一个很好的例子）。

#### Codex App Server

当你希望把完整的 Codex 执行框架以稳定、对 UI 友好的事件流形式暴露出来时，请选择 App Server。你既能获得智能体循环的全部功能，也能获得「使用 ChatGPT 登录」、模型发现和配置管理等辅助功能。主要的代价是集成工作量，因为你需要用你的语言构建客户端侧的 JSON-RPC 绑定。不过在实践中，只要你把 JSON schema 和文档喂给 Codex，它就能帮你完成大部分繁重工作。与我们合作的许多团队都借助 Codex 快速做出了可用的集成。

### 嵌入 Codex 的其他方式

#### [Codex Exec](https://developers.openai.com/codex/cli/reference/#codex-exec)

一种轻量、可脚本化的 CLI 模式，适合一次性任务和 CI 运行。它非常适合自动化与流水线场景：你希望单条命令以非交互方式运行到底、为日志流式输出结构化内容，并以明确的成功或失败信号退出。

#### [Codex SDK](https://developers.openai.com/codex/sdk/)

一个 TypeScript 库，用于在你的应用中以编程方式控制本地 Codex 智能体。当你想要一个原生的库接口来支撑服务端工具与工作流、又不想单独构建 JSON-RPC 客户端时，它是最佳选择。由于它的发布早于 App Server，目前支持的语言更少、覆盖面也更小。如果有开发者感兴趣，我们可能会增加包装 App Server 协议的更多 SDK，让团队无需编写 JSON-RPC 绑定就能覆盖执行框架的更多接口。

## 展望未来

在本文中，我们分享了如何着手设计一个与智能体交互的新标准，以及如何把 Codex 执行框架变成一个稳定、对客户端友好的协议。我们介绍了 App Server 如何暴露 Codex core、让客户端驱动完整的智能体循环，并支撑包括 TUI、本地 IDE 集成与 Web 运行时在内的广泛形态。

如果这激发了把 Codex 集成进你自己工作流的灵感，值得一试 App Server。所有源代码都在 Codex CLI 开源[代码库](https://github.com/openai/codex/blob/main/codex-rs/app-server/README.md)中。欢迎分享你的反馈和功能请求。我们期待听到你的声音，并继续让智能体对每个人都更加触手可及。
