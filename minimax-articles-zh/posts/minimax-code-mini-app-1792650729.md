---
title: "MiniMax Code Mini App 正式发布"
date: 2026-10-22
source: https://minimax.io/blog/minimax-code-mini-app-1792650729
crawled: 2026-10-26
title_en: "Introducing MiniMax Code Mini App"
translated: 2026-10-26
---

# MiniMax Code Mini App 正式发布

> 原文：[Introducing MiniMax Code Mini App](https://minimax.io/blog/minimax-code-mini-app-1792650729) · MiniMax

2026-10-22

MiniMax CodeMini AppAgent

Mini App 是一款长时运行、前后端俱全的应用。它以插件形式安装，既能调用 Agent、也能被 Agent 调用，让 Agent 的工作成果始终留在一个保持在线的页面上。

![封面：一只手将一张卡片放入 Mini App 集群中，这些 Mini App 包括股票仪表盘、3D 模型、地图和聊天窗口，并通过一条线与 Agent 相连](https://file.cdn.minimax.io/public/minimax-code-mini-app-overseas-cover-1-1792651248999.jpg?x-oss-process=image/format,webp)

今天，我们在 MiniMax Code 桌面端正式推出 [Mini App](https://agent.minimax.io/docs/miniapp/overview)。Mini App 是一款长时运行、具备前端与后端的应用。它以插件形式安装，可以与 Agent 相互调用。我们的目标是让 Agent 的工作成果始终停留在一个保持在线的页面上，而不是散落在一条条对话里。

如今已经有大量工作交给了 Agent 处理——从重构代码到梳理消息。但每一项任务都只能在各自的对话里推进：想重新捡起一项任务，你得在一堆对话里翻找上下文，回忆它当初是干什么用的。让 Agent 生成一个 HTML 仪表盘固然能把信息集中到一个页面上，但这个页面只展示生成那一刻的数据。想让它保持更新、继续推进任务，或者保存结果，你就得回到聊天框，把一切重新解释一遍。人与 AI 之间的协作从来不是一次交接就完事的：有时需要人来修改，有时需要 AI 接手推进。

插件（plugin）让你改变 Agent，Mini App 则让你在 Agent 之上构建应用。端口、Agent、数据目录这类系统级事项都由宿主（host）MiniMax Code 负责，由它划定彼此的边界。工具长什么样，由你决定——直接告诉 Agent 就行。

## Mini Apps

Mini App 是一种兼容 [MiniMax 插件协议](https://agent.minimax.io/docs/code/agents/plugin-submission)的扩展，在插件的基础上增加了 `miniapp.json` 清单文件、一个前端和一个 Node.js 服务器。架构很直接：Node.js 服务器负责取数、保存结果，并通过托管 MCP（hosted MCP）把应用的能力暴露给 Agent。页面出现在会话侧边栏中，也可以弹出成独立窗口。进程、端口、鉴权、凭证，以及支持回滚的发布流程，全部由宿主处理。

![Mini App 架构：以插件形式安装的 Mini App，各自拥有自己的页面、Node 服务器和数据，位于宿主 MiniMax Code 之上；宿主提供端口、Agent 和数据目录。双方通过托管 MCP 和 Agent API 相互调用，你只需告诉 Agent 你想要什么样的工具](https://file.cdn.minimax.io/public/minimax-code-mini-app-overseas-architecture-2-1792651248999.jpg?x-oss-process=image/format,webp)

本次发布包含三部分：

* Mini App 运行时：一个 Node 后端，带有持久化数据目录、托管 MCP、Agent API、Host Connectors，以及可以直接在页面上完成的工具审批
* `/miniapp-creator`：从对话里的一句话需求，直接生成一个可用的页面
* 插件市场中的官方 Mini App，以及开源社区仓库 MiniMax-Code-MiniApps

通过 `/miniapp-creator`，Agent 会先对每个数据源执行一次只读查询，确认自己能拿到真实数据；然后编写页面和后端，发布应用并打开它，再用内置浏览器截图检查结果。

首批官方 Mini App 中，就有几个是这样由我们工程团队之外的同事做出来的：

* 一个股票仪表盘 Mini App，把散落在知识星球（Zsxq）、Jinmen Finance 和腾讯文档中的股票信息汇入同一个仪表盘。
* CadQuery Viewer 让你在 3D 模型上标记位置，并把这些标记发回对话，交给 Agent 去修改。
* Self-drive Route Planner 把地图路线、地点搜索与图像生成整合进同一个旅行规划工作台。
* MiniMax Bot 本身就是一个 Mini App。主 Bot 会组建团队，把长时任务交给后台的 Agent 会话去执行，再审查并向你汇报结果。这些会话中的 Agent 反过来也可以调用 Bot 的工具来发消息、保存和检索记忆。Bot 的绝大多数更新只需要改插件，无需等待 MiniMax Code 发版。它的源代码现在已放入开源社区仓库。

开源社区的开发者也已经开始构建自己的 Mini App：有按日期和模型统计 token 用量的仪表盘，有以泳道图形式浏览 Git 历史的 Git Commit Tree，还有回放对话模型轨迹的 Session Trajectory。也有一些偏向日常生活与创意工作，比如用来记录心情、每天抽一张灵感卡的 Xinyu Island，以及由 Agent 创建并编辑交互式图解的 Anatomy Gallery。

> “从早期的工作流，到 RAG 和 Agentic Search，再加上在 MiniMax 工作带来的启发，我发现专业工作需要的不只是一个炫酷的 Agent，而是一个让 Agent 与人紧密协作的原生环境。作为金融分析师，我过去大部分时间都花在四处收集零散信息上。现在 Mini App 把这些信息汇入了我的工作区，我可以专注于思考与判断，把整理、分析和消化信息的活儿全部交给 Mini App。”
>
> — MiniMax 产品经理

关于安全：账户凭证由宿主持有，插件和页面都无法接触它们。连接器（Connector）和 Agent 权限必须先在清单文件中声明，才能使用。每个 Mini App 的服务器端口只对它自己的页面和 Agent 开放。当页面想把内容传给 Agent 时，内容会先进入你的输入框，由你审阅、修改后再发送。**Mini App 的代码会以你的身份在你的机器上运行，所以请只安装来自可信来源的应用包。**

## 立即上手

Mini App 现已支持 MiniMax Code 桌面端（macOS / Windows）的本地会话。

你可以从插件市场安装现成的 Mini App，也可以在对话里描述需求，让 Agent 现场帮你造一个。用上一段时间后，再让 Agent 按你的工作方式去调整它。

开始构建：

* 下载 MiniMax Code：<https://agent.minimax.io/download>（中国大陆：<https://agent.minimax.cn/download>）
* 按照快速上手指南，用 `/miniapp-creator` 构建你的第一个 Mini App：<https://agent.minimax.io/docs/miniapp/authors/quickstart>

## 开放的社区

MiniMax Bot 和社区 Mini App 的源代码都在开源仓库 [MiniMax-Code-MiniApps](https://github.com/MiniMax-AI/MiniMax-Code-MiniApps) 中。如果你做出了一个自己觉得好用的 Mini App，欢迎通过 pull request 与大家分享。

如果你需要 Mini App 目前还不具备的运行时能力，欢迎在社区仓库置顶的[能力愿望清单](https://github.com/MiniMax-AI/MiniMax-Code-MiniApps/issues/9)下留言。
