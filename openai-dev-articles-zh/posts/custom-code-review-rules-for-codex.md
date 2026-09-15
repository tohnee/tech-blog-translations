---
title: "为 Codex 定制 Code Review 规则"
title_en: "Custom Code Review rules for Codex"
source: https://developers.openai.com/blog/custom-code-review-rules-for-codex/
crawled: 2026-09-14
translated: 2026-09-14
---

# 为 Codex 定制 Code Review 规则

> 原文：[Custom Code Review rules for Codex](https://developers.openai.com/blog/custom-code-review-rules-for-codex/) · OpenAI 开发者博客

用 Codex 做代码审查时，有些意见总是反复出现。可能是关于保留旧的 API 契约、避免把客户数据写进日志，或者避免一个会破坏其他服务的重命名。这些检查很重要，但当上下文只存在于少数几位审查者的脑中时，它们很容易被遗漏。

Codex Code Review 现在可以使用 `AGENTS.md` 中的自定义仓库规则来捕获这些问题，并指引作者查看每条发现背后的指引。如果你已经在用 `AGENTS.md` 指导编码任务，同一个文件也可以用来指导审查。当贡献者或编程智能体在仓库中一个不熟悉的部分工作、还不了解其历史时，这尤其有用。在本文中，我们将展示仓库规则的适用位置以及如何写好它们，包括我们在测试过程中学到的经验。

## 交付更多代码

编程智能体可以承接更大的变更、在更长的时间跨度上工作，帮助团队把更多想法变成代码。在 OpenAI，每周 PR 量自第四季度以来增长了一倍以上，我们在许多客户那里也看到了类似的趋势。更多代码是好事：它帮助团队发布新功能、解决更多问题。但这也意味着更多的拉取请求在等待知道该看什么的人，代码审查很快就会成为瓶颈。

当多个变更同时到达时，审查会变得更难。一个 diff 可以看起来完全合理，却仍然破坏一个旧客户端，或越过作者所不知道的边界。必须有人记住那些上下文，并在作者还来得及据此行动的时候分享出来。

## 审查瓶颈

当更多拉取请求落地时，审查者用来弄清每个变更意图、并在留下反馈之前收集相关上下文的时间更少了。一旦作者转向别的事情，哪怕是一个小小的修订也可能拖得更久。快速反馈能帮助团队充分利用更快的开发速度，而不必让人成为瓶颈。

有些问题也很难只从 diff 中看出来。重命名一个响应字段看起来可能只是例行清理，但它可能破坏仍然依赖现有契约的客户端。有经验的审查者也许记得那个字段为什么必须保留；而新的贡献者，或第一次在该服务中工作的智能体，很可能不记得。

## 规则即接口

那么，如何把团队通常需要时间积累的上下文交给一个编程智能体？新的仓库规则（repository rules）接口让你可以把简洁、有范围限定的审查指引放进 `AGENTS.md`。Codex Code Review 可以应用与某个变更相关的规则，并在发现（finding）中引用它们。与其在每一个拉取请求里重复同样的解释，不如把它保存在它所适用的代码旁边。

随着编程模型变得越来越可引导，一条简短、范围明确的指令可以帮助把一次冗长的审查聚焦到你的团队真正关心的事情上。[Codex 仓库本身就把 Code Review 规则保存在 `AGENTS.md` 中](https://github.com/openai/codex/blob/5c18cc0acc3734f0e78e422a7fd94ea4a2be652e/AGENTS.md#L85-L110)，涵盖模型可见上下文与破坏性变更等关注点。

下面是一个真实的例子：

Codex app-server 会发出一个名为 `rawResponseItem/completed` 的内部通知。它被标记为实验性（experimental），但 Codex Cloud 已经在消费它。该仓库的[破坏性变更审查规则](https://github.com/openai/codex/blob/5c18cc0acc3734f0e78e422a7fd94ea4a2be652e/AGENTS.md#L102-L110)明确把 `rawResponseItem/*` 列为审查者应当保留的集成面——即使它仍处于实验阶段。

[现有的线上传输名称定义在 app-server 协议中](https://github.com/openai/codex/blob/5c18cc0acc3734f0e78e422a7fd94ea4a2be652e/codex-rs/app-server-protocol/src/protocol/common.rs#L1665-L1670)。设想一次清理改动了其中一行：

```
-RawResponseItemCompleted => "rawResponseItem/completed"
+RawResponseItemCompleted => "rawResponseItem/done"
```

这个改动可以编译通过，但监听现有通知的客户端将不再收到它。相关的仓库规则节选非常简洁：

```
## Code Review Rules

### Breaking changes

Search for breaking changes in external integration surfaces:

- raw response item events (`rawResponseItem/*`), even while experimental
```

对于这个示意性的 diff，一条 Code Review 发现可能会这样写：

> **保留现有的 `rawResponseItem/completed` 通知。** Codex Cloud 的消费方监听的是这个线上名称，因此即使该事件仍是实验性的，重命名也会破坏它们。请保留现有名称，或按照 `AGENTS.md` 中的说明添加一个向后兼容的事件。

Codex 团队[添加这条规则正是为了保护 Codex Cloud 的消费方](https://github.com/openai/codex/pull/29086)。把仓库级规则放在根目录，把服务专属规则放在相关目录中。在审查期间，Codex 可以应用覆盖了被改文件的指引，并把相关规则指给作者；一个不相关的变更不需要 app-server 的上下文。

规则与团队已经依赖的其他工具并存。测试与 linter 适合那些可以确定性表达的检查；仓库规则则帮助捕获更难编码的判断。兼容性要求与数据边界是很好的起点。作者在做出变更之前，不需要了解每一次过去的事故或每一条本地惯例；相关的指引已经摆在那里。

## 写出经得起考验的规则

我们用一个包含已知规则违规与安全反例的 eval 套件测试了 Code Review 利用仓库指引的效果。在主套件中，规则引导的变体找回了 98% 的所需自定义发现，而基线对照组为 58.3%。

发现规则违规只是工作的一部分。我们还想知道，当多条规则争夺注意力、或一个拉取请求已经内容繁多时会发生什么。我们既测试了影响重大的违规，也测试了应该保持原样的变更，然后围绕四个问题组织结果：

| 我们评估的维度 | 问题 |
|---|---|
| 覆盖率（Coverage） | 当 diff 内容繁多、多条规则争夺注意力时，Codex 能否浮现出目标违规？ |
| 克制（Restraint） | 干净的变更与合理的例外是否能避免不必要的发现？ |
| 保持力（Retention） | 在仓库规则之外，Code Review 是否仍能捕获普通的 bug？ |
| 可操作性（Actionability） | 每条发现是否指明相关的指引、位置与优先级？ |

我们还尝试了人们熟悉的指引写法，从简短的条目列表到由特定团队负责的章节。

在内部仓库中使用规则时，我们也发现了同样的模式。Codex 能够找到并引用默认审查可能会遗漏的本地指引，但宽泛的指令很容易制造噪音。小而范围明确、带有明确安全路径的规则集，帮助 Codex 聚焦在最最有用的内容上，而不会把某条规则套用到每一个邻近的变更上。

**从影响重大、又不显而易见的不变式（invariant）开始。**把审查者反复解释的检查编码下来，例如兼容性要求或数据边界。如果删掉某条规则并不会改变审查结果，那就不要写它。

**把规则限定在它们所管辖的代码范围内。**把仓库级指引放在根目录，把服务专属指引放在嵌套的 `AGENTS.md` 中。狭窄的范围可以避免无关指令争夺注意力，并让归属清晰。

**写明不变式与安全路径。**`rawResponseItem/*` 规则指出了兼容性风险。「保留现有名称或添加一个向后兼容的事件」则给作者提供了一个明确的替代方案。

**让规则持久且保持最新。**描述结果，而不是可能变化的函数名。审查对规则的更新，并收窄或移除反复产生噪音的指引。

把格式化与其他机械性检查留在 CI。仓库规则留给那些不写下来审查者就不得不反复追问的问题。

## 开始使用

如果你的仓库已经启用了 Codex Code Review，在适用的 `AGENTS.md` 文件中添加两三条规则，然后开一个有代表性的拉取请求。如果你刚接触 Code Review，[Code Review 快速开始](https://developers.openai.com/codex/third-party/github)介绍了如何为 GitHub 仓库开启它。你也可以直接用 `@codex review` 请求审查。

从审查者不断重复的解释开始，或从那种一旦遗漏后果严重的仓库专属错误开始。尝试一个应当触发规则的变更、一个安全反例，以及一个不相关的变更。确认第一个产生了有用的发现、其余两个没有制造噪音，然后根据你看到的结果打磨指引。

Codex Code Review 仍然是一位额外的审查者；测试、分支保护与必需的批准继续提供硬性的强制约束。

如果你发现自己花在审查变更上的时间比写变更还多，那就从你们团队不断重复的一个检查开始。把它加进 `AGENTS.md`，在下一次拉取请求上试试 Codex Code Review。
