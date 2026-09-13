---
title: "我们如何构建 OWL：ChatGPT 浏览器 Atlas 背后的新架构"
title_en: "How we built OWL, the new architecture behind our ChatGPT‑based browser, Atlas"
source: https://openai.com/index/building-chatgpt-atlas/
crawled: 2026-09-13
category: engineering
translated: 2026-09-13
---

# 我们如何构建 OWL：ChatGPT 浏览器 Atlas 背后的新架构

> 原文：[How we built OWL, the new architecture behind our ChatGPT‑based browser, Atlas](https://openai.com/index/building-chatgpt-atlas/) · OpenAI 博客

作者：*Ken Rockot（技术组成员）与 Ben Goodger（ChatGPT Atlas 工程负责人）*

上周，我们[发布了 ChatGPT Atlas](https://openai.com/index/introducing-chatgpt-atlas/)，一种在 ChatGPT 陪伴下浏览网络的新方式。除了是一个功能完整的网页浏览器，Atlas 还让我们得以一窥未来：一个你可以带着 ChatGPT 走遍互联网的世界——提问、提建议、为你完成任务。在本文中，我们将拆解这个产品最复杂的工程侧面之一：我们如何把 ChatGPT 变成一个越用越好用的浏览器。

让 ChatGPT 成为网络世界里真正的副驾驶，意味着重新构想浏览器的整个架构：把 Atlas 与 Chromium 运行时分离。这就要求我们开发一种全新的 Chromium 集成方式，让我们能够实现产品目标：即时启动、即使打开更多标签页也保持响应，以及为智能体用例打下坚实基础。

## 奠定基础

Chromium 是一个自然而然的基础构件。它提供了一个最先进的网页引擎，具有稳健的安全模型、公认的性能表现和无与伦比的网页兼容性。此外，它由一个持续改进它的全球社区开发。它是现代桌面网页浏览器的常见选择。

## 重新思考浏览器体验

我们出色的设计团队为用户体验设定了宏大的目标，包括为 Agent 模式等功能提供丰富的动画和视觉效果。这要求我们的工程团队在 UI 上采用最现代的原生框架（SwiftUI、AppKit 和 Metal），而不是简单地为开源 Chromium 的 UX 换一层皮。结果是，Atlas 的 UI 是对整个应用 UX 的全面重建。

我们还有其他产品目标，比如快速启动，以及在不牺牲性能的前提下支持数百个标签页。用开箱即用的 Chromium 实现这些目标很有挑战性，因为它对许多细节都有自己的固定主张——从启动序列、线程模型到标签页模型。我们考虑过在这里做大改，但我们希望保持对 Chromium 的补丁集足够克制，以便快速集成新版本。为了让开发速度得到最大提升，我们需要想出一种不同的方式来集成并驱动 Chromium 运行时。

对我们技术投入的一块试金石是：它不仅要能实现更快的新功能实验、迭代和交付，还要能让我们保持 OpenAI 工程文化的一个核心部分：入职第一天就发布（shipping on day one）。每位新工程师都要在入职第一天的下午做出并合并一个小改动。我们需要确保这一点仍然可行，尽管检出并构建 Chromium 可能要花上几个小时。

## 我们的方案：OWL

我们对这些挑战的回答，是构建一个我们称之为 **OWL：OpenAI's Web Layer** 的新架构层。OWL 是我们对 Chromium 的集成方式，其要点是把 Chromium 的浏览器进程运行在主 Atlas 应用进程*之外*。

可以这样理解：Chromium 通过把标签页移入独立进程而革命性地改变了浏览器。我们把这一思路再推进一步，把 Chromium 本身移出主应用进程，放进一个隔离的服务层。这一转变解锁了一连串好处：

- **一个更简单、更现代的应用：**Atlas 几乎完全用 SwiftUI 和 AppKit 构建。一种语言、一套技术栈、一个干净的代码库。
- **更快的启动：**Chromium 在后台异步启动。Atlas 无需等待——像素几乎立即出现在屏幕上。
- **与卡顿和崩溃隔离：**Chromium 是一个强大而复杂的网页引擎。它的主线程卡住时，Atlas 不会；它崩溃时，Atlas 依然屹立。
- **更少的合并烦恼：**因为我们不再基于那么多 Chromium 开源 UI 构建，我们相对上游 Chromium 的 diff 小得多，也更容易维护。
- **更快的迭代：**大多数工程师从不需要在本地构建 Chromium。OWL 以预构建二进制的形式在内部发布，因此 Atlas 的构建只需几分钟而非几小时。

由于我们团队的大多数工程师不会经常从源码构建 Chromium，开发可以快得多——甚至新成员也能在入职第一个下午合并简单的改动。

## OWL 的工作原理

从宏观上看，Atlas 浏览器是 **OWL 客户端（OWL Client）**，而 Chromium 浏览器进程是 **OWL 宿主（OWL Host）**。它们通过 IPC 通信，具体使用 [Mojo](https://chromium.googlesource.com/chromium/src/+/main/mojo/README.md)——Chromium 自家的消息传递系统。我们为 Mojo 编写了定制的 Swift（甚至 TypeScript）绑定，因此我们的 Swift 应用可以直接调用宿主侧的接口。

OWL 客户端库暴露一个简单的公开 Swift API，它抽象了宿主服务层所暴露的几个关键概念：

- **Session：**全局配置与控制宿主
- **Profile：**为特定用户配置文件管理浏览器状态
- **WebView：**控制并嵌入单个网页内容（例如渲染、输入、导航、缩放等）
- **WebContentRenderer：**把输入事件转发进 Chromium 的渲染管线，并从渲染器接收反馈
- **LayerHost/Client：**在 UI 与 Chromium 之间交换合成信息

此外还有大量的服务端点，用于管理书签、下载、扩展和自动填充等高层功能。

### 渲染：让像素跨越进程边界

在客户端应用中共享一个互斥呈现空间的各个 WebView，会在一个共享的合成容器中换入换出。例如，一个浏览器窗口通常只有一个共享容器可见，在标签条中选择一个标签页就会把该标签的 WebView 换入容器。在 Chromium 侧，这个容器对应一个 `gfx::AcceleratedWidget`，它最终由一个 `CALayer` 支撑。我们把这个层的上下文 ID 暴露给客户端，客户端中一个 `NSView` 使用私有的 `CALayerHost` API 将其嵌入。

像 `<select>` 下拉菜单或取色器这类特殊情况——Chromium 会用独立的弹出 widget 来渲染它们——也采用同样的方式。它们没有 `content::WebContents`，但*确实*拥有带自己 `gfx::AcceleratedWidget` 的 `content::RenderWidgetHostView`，因此同样适用这种委托渲染模型。

OWL 在内部保持视图几何信息与 Chromium 侧同步，因此 GPU 合成器可以得到相应更新，总能生成尺寸与设备缩放都正确的层内容。

我们还复用这一技术，把 Chromium 自身原生 Views UI 的元素有选择地投影到 Atlas 中（这对快速搭建权限提示等功能也很有用，无需在 SwiftUI 中从零构建替代品）。这一技术大量借鉴了 Chromium 在 macOS 上针对可安装网页应用的现有基础设施。

### 输入事件：解析与转发

Chromium UI 会先把平台事件（如 macOS 的 NSEvent）翻译成 Blink 的 WebInputEvent 模型，再转发给渲染器。但由于 OWL 在一个隐藏进程中运行 Chromium，我们在 Swift 客户端库内自行完成这一翻译，并把已经翻译好的事件向下转发给 Chromium。

从那里开始，它们遵循与真实输入事件在网页内容中通常相同的生命周期。这包括：每当页面表明自己没有处理某个事件时，事件会被*退回*给客户端。发生这种情况时，我们会重新合成一个 NSEvent，让应用的其余部分有机会处理该输入。

### Agent 模式：特殊情况

Atlas 的智能体浏览功能给我们的渲染、输入事件转发和数据存储方案带来了一些独特的挑战。

我们的 computer use 模型期望以单张屏幕图像作为输入。但某些 UI 元素——例如 `<select>` 下拉菜单——会在标签页边界之外的独立窗口中渲染。在 Agent 模式下，我们把那些弹出窗口按正确坐标合成回主页面图像，让模型在一帧中看到完整上下文。

在输入方面，我们采用同样的原则：由智能体生成的事件直接路由到渲染器，绝不经过特权的浏览器层。这样即使在自动化控制下也能保持沙箱边界。例如，我们不希望这类事件合成出让浏览器做出与当前显示的网页内容无关之事的键盘快捷键。

智能体浏览还可以在一个临时的「未登录」上下文中运行。我们没有共享用户现有的无痕（Incognito）配置文件——那可能泄露状态——而是使用 Chromium 的 `StoragePartition` 基础设施来启动隔离的内存存储。每个智能体会话都从全新状态开始，会话结束时，所有 cookie 和站点数据都会被丢弃。你可以同时运行多个「未登录」智能体会话，每个会话位于自己的浏览器标签页中，且彼此完全隔离。

## 一种使用网络的新方式

如果没有全球 Chromium 社区以及他们为现代网络打造基础的杰出工作，这一切都无从谈起。OWL 以一种新的方式建立在这一基础之上：把引擎与应用解耦，把世界级的网页平台与现代原生框架融合，并解锁一个更快、更灵活的架构。

通过重新思考浏览器如何「容纳」Chromium，我们正在为新一类的体验创造空间：更顺畅的启动、更丰富的 UI、与操作系统其余部分更紧密的集成，以及一个以想法的速度前进的开发循环。如果这听起来正是你想挑战的方向，欢迎查看我们在 Atlas 上的职位空缺：[Software Engineer, Atlas](https://openai.com/careers/software-engineer-atlas-san-francisco/)、[Software Engineer, iOS](https://openai.com/careers/software-engineer-ios-san-francisco/) 以及[更多职位](https://openai.com/careers/search/?c=e1e973fe-6f0a-475f-9361-a9b6c095d869%2Cf002fe09-4cec-46b0-8add-8bf9ff438a62%2Cab2b9da4-24a4-47df-8bed-1ed5a39c7036)。

**前往 [chatgpt.com/atlas](http://chatgpt.com/atlas?openaicom-did=e181c8f2-dce1-467d-a4b2-31120824d909&openaicom_referred=true) 试用 Atlas。**
