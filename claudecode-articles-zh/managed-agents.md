---
title: "Managed Agents 的规模化之道：把大脑与双手解耦"
title_en: "Scaling Managed Agents: Decoupling the brain from the hands"
source: https://www.anthropic.com/engineering/managed-agents
published: 2026-04-08
crawled: 2026-09-11
translated: 2026-09-11
---

# Managed Agents 的规模化之道：把大脑与双手解耦

> 原文：[Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents) · Anthropic Engineering Blog

*按照我们的[文档](https://platform.claude.com/docs/en/managed-agents/overview)即可开始使用 Claude Managed Agents。*

工程博客的一个反复出现的主题是如何[构建高效智能体](https://www.anthropic.com/engineering/building-effective-agents)，以及如何为[长时运行的工作](https://www.anthropic.com/engineering/harness-design-long-running-apps)[设计执行框架](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)。这项工作的一条共同线索是：框架编码了「Claude 自己做不到什么」的假设。然而这些假设需要被频繁质疑，因为随着模型进步它们会[过时](http://www.incompleteideas.net/IncIdeas/BitterLesson.html)。

仅举一例：在先前的工作中[我们发现](https://www.anthropic.com/engineering/harness-design-long-running-apps)，Claude Sonnet 4.5 会在察觉上下文上限临近时过早收尾——这种行为有时被称为「上下文焦虑」。我们的对策是在框架里加入上下文重置。但当我们把同一框架用在 Claude Opus 4.5 上时，发现这个行为消失了。重置成了死重。

我们预计框架会继续演化。所以我们构建了 Managed Agents：Claude 平台上的一个托管服务，代表你运行长周期智能体，通过一小组力求超越任何特定实现——包括我们今天运行的这些——的接口。

构建 Managed Agents 意味着解决计算领域一个古老的问题：如何为「[尚无人想到的程序](http://www.catb.org/esr/writings/taoup/html/ch03s01.html)」设计系统。几十年前，操作系统通过把硬件虚拟化成抽象——*进程*、*文件*——解决了这个问题，这些抽象足够通用，可以服务于当时还不存在的程序。抽象比硬件活得更久。`read()` 命令不关心它访问的是 1970 年代的磁盘组还是现代 SSD。其上的抽象保持稳定，其下的实现自由更迭。

Managed Agents 遵循同一模式。我们把智能体的组件虚拟化：会话（session，记录一切已发生之事的只追加日志）、执行框架（harness，调用 Claude 并把 Claude 的工具调用路由到相关基础设施的循环）、沙箱（sandbox，Claude 运行代码和编辑文件的执行环境）。这让每一部分的实现都可以在不惊动其他部分的情况下更换。我们对这些接口的形态持强观点，但对它们背后运行什么不作规定。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F903b624ada206b10753a24c6a1367e74a869165d-1080x1080.png&w=3840&q=75)

## 别养宠物

我们最初把所有智能体组件放进单个容器：会话、智能体框架和沙箱共享一个环境。这种做法有好处：文件编辑是直接的 syscall，也没有服务边界需要设计。

但把一切耦合进一个容器，我们撞上了一个古老的基础设施问题：我们领养了一只[*宠物*](https://cloudscaling.com/blog/cloud-computing/the-history-of-pets-vs-cattle/)。在「宠物 vs 牲畜」的类比里，宠物是有名字、需要手工照料、你承受不起失去的个体；牲畜则是可互换的。在我们这里，那台服务器成了宠物：容器一挂，会话就没了。容器失联时，我们得把它护理回来。

护理容器意味着调试无响应的卡死会话。我们唯一的窗口是 WebSocket 事件流，但它无法告诉我们故障*发生在哪里*——harness 里的 bug、事件流中的丢包、容器掉线，表现全一样。要弄清哪里出了问题，工程师得在容器里开个 shell，但那个容器往往同时装着用户数据，这条路等于让我们失去了调试能力。

第二个问题是框架假定 Claude 处理的一切都和它同住一个容器。当客户要求我们把 Claude 连到他们自己的虚拟私有云时，他们要么与我们的网络做对等连接，要么在我们的环境里跑 harness。框架里一个固化的假设，在我们想把它连到不同基础设施时成了绊脚石。

## 把大脑与双手解耦

我们得出的方案是：把「大脑」（Claude 及其框架）与「双手」（执行动作的沙箱和工具）以及「会话」（会话事件日志）解耦。每一部分都成为对其他部分少做假设的接口，每一部分都可以独立失败或被替换。

**框架搬出容器。** 把大脑与双手解耦，意味着框架不再住在容器里。它调用容器的方式与调用任何其他工具一样：`execute(name, input) → string`。容器成了牲畜。容器挂了，框架把故障作为工具调用错误捕获并传回给 Claude。如果 Claude 决定重试，可以按标准配方重新初始化一个新容器：`provision({resources})`。我们再也不用护理挂掉的容器了。

**从框架故障中恢复。** 框架自己也成了牲畜。因为会话日志在框架之外，框架里没有任何东西需要在崩溃后幸存。一个框架实例挂了，可以用 `wake(sessionId)` 重启新的，用 `getSession(id)` 取回事件日志，从最后一个事件继续。在智能体循环期间，框架用 `emitEvent(id, event)` 写入会话，以保持事件的持久记录。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F73e900af5b9d6ed8c64db0a8e74d4465963556b7-1640x1596.png&w=3840&q=75)

**安全边界。** 在耦合设计中，Claude 生成的任何不可信代码都与凭证运行在同一个容器里——所以一次提示注入只需说服 Claude 读一下它自己的环境。攻击者一旦拿到那些 token，就可以派生全新的、不受限的会话并把工作委派出去。缩小作用域是显而易见的缓解手段，但这又编码了「Claude 拿着有限 token 做不成什么」的假设——而 Claude 正变得越来越聪明。结构性修复是确保 token 永远无法从 Claude 生成代码所在的沙箱中触及。

我们用两种模式保证这一点。认证可以随资源打包，也可以保存在沙箱外的金库中。对 Git，我们在沙箱初始化时用每个仓库的访问 token 克隆仓库并接入本地 git remote。git `push` 和 `pull` 在沙箱内直接工作，智能体从头到尾不经手 token 本身。对自定义工具，我们支持 MCP 并把 OAuth token 存入安全金库。Claude 通过专用代理调用 MCP 工具；该代理接收与会话关联的 token，再从金库取回对应凭证、向外部服务发起调用。harness 从头到尾不知晓任何凭证。

## 会话不是 Claude 的上下文窗口

长周期任务常常超出 Claude 上下文窗口的长度，而应对这一问题的标准手段全都涉及「保留什么」的不可逆决定。我们在关于上下文工程的[先前工作](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)中探讨过这些技术。例如，压缩让 Claude 保存上下文窗口的摘要，记忆工具让 Claude 把上下文写入文件、实现跨会话学习。这些还可以搭配上下文修剪——选择性地移除旧工具结果或思考块之类的 token。

但不可逆地选择保留或丢弃上下文可能导致失败。很难知道未来的轮次会需要哪些 token。如果消息被压缩步骤改写，harness 会把被压缩的消息从 Claude 的上下文窗口中移除，除非它们被另行存储，否则无法恢复。先前的工作[探索过](https://arxiv.org/pdf/2512.24601)把上下文存储为生活在上下文窗口*之外*的对象来解决这一问题的办法。例如，上下文可以是一个 REPL 中的对象，LLM 通过写代码来过滤或切片、以编程方式访问它。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fcf0719d7832b1f577b7393c84a7c53eecc725ca4-760x200.png&w=1920&q=75)

在 Managed Agents 中，会话提供同样的好处：充当一个生活在 Claude 上下文窗口之外的上下文对象。但上下文不是存储在沙箱或 REPL 里，而是持久地存放在会话日志中。接口 `getEvents()` 让大脑可以通过选择事件流的位置切片来查询上下文。这个接口使用灵活：大脑可以从上次停止阅读的地方接着读，可以回退到某个时刻之前的几个事件看铺垫，也可以在某个动作之前重读上下文。

取回的事件还可以在传入 Claude 上下文窗口之前，在 harness 中做变换。这些变换完全由 harness 决定，包括为了高提示缓存命中率所做的上下文组织，以及各种上下文工程。我们把「会话中的可恢复上下文存储」与「harness 中的任意上下文管理」分成两个关注点，因为我们无法预测未来的模型会需要什么样的具体上下文工程。接口把上下文管理推给 harness，只保证会话是持久的、可查询的。

## 许多大脑，许多双手

**许多大脑。** 把大脑与双手解耦解决了我们最早的客户抱怨之一。当团队想让 Claude 操作他们自己 VPC 里的资源时，唯一的路径是与我们的网络做对等连接，因为装着框架的容器假定所有资源都近在咫尺。框架不再住在容器里之后，这个假设就消失了。同样的改动还带来了性能回报。当我们最初把大脑放进容器时，意味着许多大脑需要许多容器：每个大脑在容器配置好之前无法开始推理；每个会话都要预先支付完整的容器启动成本。每个会话——哪怕永远不会碰沙箱——都得克隆仓库、启动进程、从我们的服务器取回待处理事件。

这些死时间体现在首 token 时间（TTFT）上，它度量一个会话从接下工作到产出第一个响应 token 之间的等待。TTFT 是用户*体感*最尖锐的延迟。

大脑与双手解耦意味着容器只在需要时由大脑通过工具调用 `execute(name, input) → string` 来配置。不需要立即用容器的会话就不必等。编排层一从会话日志拉出待处理事件，推理即可开始。用这个架构，我们的 p50 TTFT 降了约 60%，p95 降了超过 90%。扩展到许多大脑，只是启动许多无状态的 harness、并按需把它们连到双手。

**许多双手。** 我们还想要把每个大脑连到许多双手的能力。实践中，这意味着 Claude 必须对许多执行环境做推理、决定把工作派到哪里——这比在单一 shell 里操作是更难的认知任务。我们最初把大脑放在单个容器里，就是因为更早的模型做不到这件事。随着智能扩展，单容器反而成了限制：容器一挂，大脑伸进去的每一双手的状态全部丢失。

大脑与双手解耦后，每双手都成为一个工具 `execute(name, input) → string`：一个名字和输入进去，一个字符串返回。这个接口支持任何自定义工具、任何 MCP 服务器，以及我们自己的工具。harness 不知道沙箱是一个容器、一部手机，还是一个宝可梦模拟器。而且因为没有任何一双手与任何一个大脑耦合，大脑之间可以互相传递双手。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F4f67b1c10566552aec514a716ea43544ab330e0b-668x243.png&w=1920&q=75)

## 结语

我们面对的挑战是古老的：如何为「尚无人想到的程序」设计系统。操作系统靠把硬件虚拟化为足够通用的抽象、以服务当时不存在的程序，存活了几十年。在 Managed Agents 上，我们的目标是设计一个能容纳未来 harness、沙箱以及 Claude 周围其他组件的系统。

Managed Agents 是同一精神下的元框架（meta-harness）：它不对 Claude 未来需要的*特定* harness 持观点，而是一个带通用接口、可容纳许多不同 harness 的系统。例如，Claude Code 是一个出色的 harness，我们在各类任务中广泛使用。我们也展示过任务专用的智能体框架在窄域中表现出色。Managed Agents 可以容纳其中任何一种，随时间匹配 Claude 的智能。

元框架设计意味着对 Claude 周围的接口持强观点：我们预期 Claude 需要操纵状态（会话）与执行计算（沙箱）的能力。我们也预期 Claude 需要扩展到许多大脑与许多双手的能力。我们把这些接口设计得可以在长时间跨度上可靠、安全地运行。但我们不对 Claude 需要的大脑或双手的数量与位置做任何假设。

## 致谢

作者：Lance Martin、Gabe Cemaj 和 Michael Cohen。感谢 Nodir Turakulov 和 Jeremy Fox 就这些话题的有益讨论。特别感谢 Agents API 团队和 Jake Eaton 的贡献。
