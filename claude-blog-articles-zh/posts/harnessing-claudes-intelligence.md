---
title: "智能体执行框架设计：驾驭 Claude 智能的三种模式"
title_en: "Agent Harness Design: 3 Patterns for Harnessing Claude's Intelligence"
date: 2026-04-02
source: https://claude.com/resources/articles/harnessing-claudes-intelligence
crawled: 2026-11-17
translated: 2026-11-17
---

# 智能体执行框架设计：驾驭 Claude 智能的三种模式

> 原文：[Agent Harness Design: 3 Patterns for Harnessing Claude's Intelligence](https://claude.com/resources/articles/harnessing-claudes-intelligence) · Claude 博客

*构建在智能、延迟与成本之间取得平衡的应用。*

Anthropic 联合创始人 Chris Olah [说过](https://www.darioamodei.com/post/the-urgency-of-interpretability)，像 Claude 这样的生成式 AI 系统更多是"长"出来的，而不是"造"出来的。研究者设定条件来引导生长，但最终涌现出的具体结构或能力并不总是可预测的。

这给基于 Claude 构建应用带来了挑战：[智能体执行框架把假设固化在代码里](https://www.anthropic.com/engineering/harness-design-long-running-apps)，假设 Claude 自己做不到什么；但随着 Claude 能力提升，这些假设会逐渐过时。

智能体执行框架（agent harness）是模型外围的软件脚手架：循环、工具、[上下文管理](https://claude.com/resources/articles/context-management)和防护栏，把原始的智能转化为可工作的智能体。智能体执行框架设计，就是决定脚手架里该放什么，以及在模型进步时该拿掉什么的实践。

本文分享三种模式，供团队在构建应用时采用，以便跟上 Claude 不断演进的能力，同时平衡延迟与成本：利用它已经掌握的东西，追问你可以停止做什么，以及谨慎地用执行框架划定边界。

### **1. 依靠模型，而非执行框架：利用 Claude 已经掌握的东西**

我们建议使用 Claude 熟悉的工具来构建应用。

2024 年底，Claude 3.5 Sonnet 在 SWE-bench Verified 上达到 49%——[当时的最优水平](https://www.anthropic.com/engineering/swe-bench-sonnet)——而它只用了 [bash 工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool)和一个用于查看、创建和编辑文件的[文本编辑器工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool)。Claude Code 正是建立在同样这些工具之上。[Bash](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool) 并不是为构建智能体而设计的，但它是 Claude *知道*怎么用、并且随着时间越用越好的工具。

![](https://assets.claude.com/9ff0af45fd385dc84e3043c0646dd4b98ceba256.png)

Claude 各版本模型在 SWE-bench Verified 基准上的得分，凸显了它的演进。

我们看到 Claude 把这些通用工具组合成解决不同问题的模式。例如，[Agent Skills](https://agentskills.io/home)、[程序化工具调用](https://platform.claude.com/docs/en/agents-and-tools/tool-use/programmatic-tool-calling)和[记忆工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)，全部构建自 bash 和文本编辑器工具。

![](https://assets.claude.com/4f2f17a50558ff747a3cc161f845023ab21a9f21.png)

程序化工具调用、技能和记忆，都是对 bash 与文本编辑器工具的组合。

### **2. 精简执行框架：追问你可以停止做什么**

[执行框架把假设固化下来](https://www.anthropic.com/engineering/harness-design-long-running-apps)，假设 Claude 自己做不到什么。随着 Claude 能力提升，这些假设应当被检验。

**让 Claude 编排自己的行动**

一个常见的假设是：每个工具结果都应该流回 Claude 的[上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows)，用于指导下一步行动。用 token 处理工具结果可能缓慢、昂贵，而且如果结果只是要传给下一个工具，或者 Claude 只关心输出中的一小片，那这种处理就是不必要的。

![](https://assets.claude.com/846ce7bdd3af066b26f3eb238cce8df7302b9ccb.png)

Claude 调用工具，工具在某个环境中执行。

设想为了推断某一列而读取一张大表：整张表都落进上下文，Claude 为每一行不需要的数据支付 token 成本。可以在工具设计层面用[硬编码的过滤器](https://platform.claude.com/docs/en/about-claude/models/migration-guide#additional-recommended-changes)来解决。但这没有触及一个事实：执行框架正在做一个*编排决策*，而 Claude 更处于做这个决策的位置。

给 Claude 一个[代码执行](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)工具（例如 [bash 工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool)或[特定语言的 REPL](https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool)）可以解决这个问题：它让 Claude 编写代码来表达工具调用以及调用之间的逻辑。不再由执行框架决定每个工具调用结果都要作为 token 处理，而是由 Claude 决定哪些结果直接透传、过滤或管道给下一次调用，全程不触碰上下文窗口。只有代码执行的输出会进入 Claude 的上下文窗口。

![](https://assets.claude.com/bd8453083ea472d1e2af60252a9ec47d7d429249.png)

Claude 可以编写代码来表达工具调用及调用之间的逻辑。

编排决策从执行框架转移到了模型。既然代码是 Claude 编排行动的一种通用方式，那么一个强大的编程模型也是一个强大的*通用*智能体。Claude 在这种模式下于[非编码评估](https://claude.com/resources/articles/improved-web-search-with-dynamic-filtering)中表现强劲：在 BrowseComp 这个测试智能体网页浏览能力的[基准](https://arxiv.org/abs/2504.12516)上，让 Opus 4.6 具备自行过滤工具输出的能力，把准确率从 45.3% 提升到 61.6%。

**让 Claude 管理自己的上下文**

任务特定的上下文引导 Claude 如何使用 bash 和文本编辑器工具这类通用工具。一个常见的假设是：[系统提示](https://platform.claude.com/docs/en/release-notes/system-prompts)应当手工撰写任务特定的指令。问题在于，用指令预加载提示无法扩展到许多任务：每多加一个 token 都在消耗 [Claude 的注意力预算](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)，而用很少使用的指令预填上下文是一种浪费。

赋予 Claude 访问[技能](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)的能力可以解决这个问题：每个技能的 YAML frontmatter 是一段预加载进上下文窗口的简短描述，提供技能内容概览。如果任务需要，Claude 可以调用读取文件的工具，逐步展开完整技能。

![](https://assets.claude.com/606dbffc4fe38a3a1a05c4d88650c2a2e160766d.png)

Claude 可以使用技能来逐步披露与任务相关的上下文。

技能赋予 Claude 自由组装自己上下文窗口的能力，而[上下文编辑](https://platform.claude.com/docs/en/build-with-claude/context-editing)则是其反面：提供一种选择性移除已过时或不相关上下文的方式，例如旧的工具结果或思考块。

借助[子智能体](https://code.claude.com/docs/en/sub-agents)，Claude 越来越擅长判断何时分叉到一个全新的上下文窗口，以隔离特定任务的工作。[在 Opus 4.6 上](https://www-cdn.anthropic.com/0dd865075ad3132672ee0ab40b05a53f14cf5288.pdf)，派生（spawn）子智能体的能力使 BrowseComp 上的结果比最佳的单智能体运行提升了 2.8%。

**让 Claude 持久化自己的上下文**

长时运行的智能体会超出单个[上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows)的容量。一个常见的假设是：记忆系统应当依赖模型外围的检索基础设施。我们的很多工作都聚焦于给 Claude 一些简单的方式，让它*自己选择*要持久化哪些内容。

例如，[压缩（compaction）](https://platform.claude.com/docs/en/build-with-claude/compaction)让 Claude 总结过去的上下文，以在长周期任务中保持连贯性。经过若干版本迭代，Claude 越来越善于选择该记住什么。以智能体式搜索任务 [BrowseComp](https://www-cdn.anthropic.com/14e4fb01875d2a69f646fa5e574dea2b1c0ff7b5.pdf) 为例，无论我们给多少压缩预算，Sonnet 4.5 都停留在 43%。而在同样的设置下，Opus 4.5 提升到 68%，Opus 4.6 达到 84%。

[记忆文件夹](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool)是另一种方式，让 Claude 把上下文写入文件，之后按需读取。我们看到 Claude 在智能体式搜索中使用了它。在 BrowseComp-Plus 上，给 Sonnet 4.5 一个记忆文件夹[把准确率从 60.4% 提升到 67.2%](https://www-cdn.anthropic.com/bf10f64990cfda0ba858290be7b8cc6317685f47.pdf)。

![](https://assets.claude.com/2ac581337b2050f448e2a22b9a8e4a1451e0d72c.png)

Claude 可以把上下文持久化到记忆文件夹。

[长周期游戏](https://www.youtube.com/watch?v=CXhYDOvgpuU)（例如 Pokémon）是 Claude 使用记忆文件夹能力提升的一个例子。Sonnet 3.5 把记忆当作流水账，记下非玩家角色（NPC）说了什么，而不是什么才重要。走了 14,000 步之后，它留下了 31 个文件——其中包括两条关于毛毛虫宝可梦的近重复记录——而它还在第二座城镇：

```
caterpie_weedle_info:
- Caterpie and Weedle are both caterpillar Pokémon.
- Caterpie is a caterpillar Pokémon that does not have poison.
- Weedle is a caterpillar Pokémon that does have poison.
- This information is crucial for future encounters and battles.
- If our Pokémon get poisoned, we should seek healing at a Pokémon
  Center as soon as possible.
```

后来的模型会写战术笔记。Opus 4.6 在相同的步数下只有 10 个文件，按目录组织，拿到了三枚道馆徽章，还有一个从自身失败中提炼的学习文件：

```
/gameplay/learnings.md:
- Bellsprout Sleep+Wrap combo: KO FAST with BITE before Sleep
  Powder lands. Don't let it set up!
- Gen 1 Bag Limit: 20 items max. Toss unneeded TMs before dungeons.
- Spin tile mazes: Different entry y-positions lead to DIFFERENT
  destinations. Try ALL entries and chain through multiple pockets.
- B1F y=16 wall CONFIRMED SOLID at ALL x=9-28 (step 14557)
```

### **3. 在执行框架设计中谨慎划定边界**

智能体执行框架在 Claude 周围提供结构，以落实用户体验、成本或安全方面的要求。

**设计上下文以最大化缓存命中**

[Messages API](https://platform.claude.com/docs/en/build-with-claude/working-with-messages) 是无状态的。Claude 看不到之前轮次的对话历史。这意味着执行框架在每一轮都需要把新的上下文连同所有过去的动作、工具描述和指令一起打包给 Claude。

提示可以基于设定的[断点](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)进行缓存。换句话说，Claude API 会把截至某个断点的上下文写入缓存，并检查该上下文是否匹配任何先前的缓存条目。

由于缓存 token 的[成本是基础输入 token 的 10%](https://platform.claude.com/docs/en/about-claude/pricing)，以下是执行框架中帮助最大化缓存命中的几条原则：

| 原则 | 说明 |
| --- | --- |
| 静态在前，动态在后 | 排序请求，让稳定的内容（系统提示、工具）排在最前。 |
| 用消息承载更新 | 在 messages 中追加 `<system-reminder>`，而不是直接修改提示。 |
| 不要更换模型 | 避免在会话中途切换模型。缓存与模型绑定，切换会让缓存失效。如果需要更便宜的模型，请使用子智能体。 |
| 谨慎管理工具 | 工具位于被缓存的前缀中，增删任何一个都会使其失效。需要动态发现时，使用 **tool search**，它以追加方式生效，不破坏缓存。 |
| 更新断点 | 对于多轮应用（如智能体），把断点移到最新消息，以保持缓存最新。可使用**自动缓存（auto-caching）**实现。 |

**为 UX、可观测性或安全边界使用声明式工具**

Claude 未必知道一个应用的安全边界或 UX 界面。Claude 发出工具调用，由执行框架处理。bash 工具赋予 Claude 广泛的程序化行动能力，但它只给执行框架一个命令字符串——所有动作都是同样的形状。把动作提升为专用工具，就给了执行框架一个带类型参数的动作特定钩子，可以拦截、把关、渲染或审计。

需要安全边界的动作自然是专用工具的候选对象。可逆性通常是个好标准；对外部 API 调用这类难以逆转的动作，可以用用户确认来把关。像 `edit` 这样的写入工具可以包含陈旧性检查，以免 Claude 覆盖掉自上次读取以来已被改动的文件。

![](https://assets.claude.com/ed3130dafac3f6d95a73485c34751ac8461625ca.png)

专用工具可用于基于安全、UX 或可观测性考量的动作。

当某个动作需要呈现给用户时，工具同样有用。例如，可以把工具调用渲染为模态框，向用户清晰地展示一个问题、提供多个选项，或者阻塞智能体循环直到用户给出反馈。

最后，工具对可观测性也有帮助。当动作是一个带类型的工具时，执行框架获得的是结构化参数，可以记录日志、追踪和重放。

把动作提升为工具的决策应当持续重新评估。例如，Claude Code 的[自动模式](https://www.anthropic.com/engineering/claude-code-auto-mode)（auto-mode，本文发表时处于研究模式）为 bash 工具提供了一道安全边界：它让第二个 Claude 读取命令字符串并判断是否安全。这种模式可以*减少*对专用工具的需求，且只应用于用户信任整体方向的任务。对于某些高风险动作，专用工具仍然有其价值。

### 智能体执行框架设计的未来

Claude 智能的前沿始终在变化。关于"Claude 做不到什么"的假设，需要在其能力的每一次阶跃变化后重新检验。

我们看到这种模式反复出现。在我们[为长周期任务构建的一个智能体](https://www.anthropic.com/engineering/harness-design-long-running-apps)中，Sonnet 4.5 会在感知到上下文上限临近时过早收尾。为解决这种"上下文焦虑"，我们加入了重置机制来清空上下文窗口。到了 Opus 4.5，这个行为消失了。我们为补偿而构建的上下文重置，成了执行框架里的累赘。

清除这些累赘很重要，[因为它可能成为](http://www.incompleteideas.net/IncIdeas/BitterLesson.html) Claude 性能的瓶颈。随着时间推移，我们应用中的结构或边界应当基于这个问题来修剪：*我可以停止做什么？*

*要使用本文讨论的所有工具和模式，请查看我们的 [claude-api skill](https://github.com/anthropics/skills/tree/main/skills/claude-api)。*

### 致谢

本文由 Claude Platform 团队技术人员 Lance Martin 撰写。特别感谢 Thariq Shihipar、Barry Zhang、Mike Lambert、David Hershey 和 Daliang Li 就文中主题进行的有益讨论。感谢 Lydia Hallie、Lexi Ross、Katelyn Lesse、Andy Schumeister、Rebecca Hiscott、Jake Eaton、Pedram Navid 和 Molly Vorwerck 的编辑审阅与反馈。
