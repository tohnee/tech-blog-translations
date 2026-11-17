---
title: "推理 hooks：为 Claude Enterprise 提供内联数据防泄漏"
title_en: "Inference hooks: inline data loss prevention for Claude Enterprise"
date: 2026-08-05
source: https://claude.com/resources/articles/claude-enterprise-inference-hooks
crawled: 2026-11-17
translated: 2026-11-17
---

# 推理 hooks：为 Claude Enterprise 提供内联数据防泄漏

> 原文：[Inference hooks: inline data loss prevention for Claude Enterprise](https://claude.com/resources/articles/claude-enterprise-inference-hooks) · Claude 博客

![](https://assets.claude.com/ea1030817dc2ba53b41c8049ca9a707dfc09fcce.gif)

推理 hooks（inference hooks）让你的合规团队在每个提示词和工具调用响应到达 Claude 之前进行检查并执行策略——覆盖聊天、Claude Code、Claude Cowork 等 Claude Enterprise 各界面。由你的 DLP 服务器做出阻止或放行的裁决，Claude 实时执行该决定，在未经批准的内容到达 Claude 之前将其拦下。

安全团队要求：员工可能在其中传递敏感数据的每一条通道，都必须经过由他们团队掌控的检查点。在此之前，原生的内联强制执行仅限于 Claude Code 的客户端 hooks。推理 hooks 弥补了这一缺口，用一个统一的执行层覆盖所有 Claude Enterprise 界面，无需为每个产品单独集成，也不必为每个产品部署一个智能体。

## 推理 hooks 的工作方式

![](https://assets.claude.com/d4d917c41136cdd796632537b4ed39618b0bc62b.png)

当组织开启推理 hooks 后，每个推理请求都会经由一条经签名的 WebSocket 连接路由到一台安全服务器。在模型开始生成之前，Claude 会把提示词及其周边上下文发送到你的服务器。你的服务器返回裁决——放行或拒绝——Claude 只有在拿到裁决后才会继续。同样的检查也适用于工具调用：当 Claude 调用工具时——包括通过 MCP、skills 和插件接入的工具——工具响应会在回传给模型之前接受检查。

已有团队在运用这项实时检查。「推理 hooks 增加了一个检查点，可以在模型看到任何内容之前，实时检查流向 Claude 的数据，」Bandwidth 信息安全副总裁 Andrew Grimmett 表示。「这让我们能够更放心地加快 AI 推进，同时不放弃控制权。」

## 推理 hooks 的用法

把现有的 DLP 项目扩展到 Claude。推理 hooks 使用开放的、基于 webhook 的协议，并公开了 schema。这让部署变得简单——只需指向你其他工具已经在向其上报的同一台服务器，包括 Netskope、Palo Alto Networks、Proofpoint、Zscaler，或你自建的 AI 安全服务器。

用一套配置覆盖聊天、Claude Code、Cowork 以及更多 Claude Enterprise 产品。在组织层面开启一次推理 hooks，它就会作用于 Claude Enterprise 各界面，包括通过 MCP 连接器、skills 和插件发起的工具调用。

通过影子模式（始终放行）、基于角色的排除以及按比例灰度发布来简化上线。按组织的风险偏好调整故障策略容忍度、超时和其他设置。

## 开始使用

推理 hooks 现以 beta 形式向 Claude Enterprise 客户提供。请阅读[文档](https://platform.claude.com/docs/en/manage-claude/inference-hooks)，配置你组织的 DLP 服务器，并开始在 Claude Enterprise 各界面执行策略。

对安全厂商而言，推理 hooks 构建在带有文档化 schema 的 webhook 协议之上，因此你可以构建集成，而 Claude Enterprise 客户则可以把自己的组织指向你的平台。
