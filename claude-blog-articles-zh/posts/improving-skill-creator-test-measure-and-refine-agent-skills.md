---
title: "改进 skill-creator：测试、衡量并打磨 Agent Skills"
title_en: "Improving skill-creator: Test, measure, and refine Agent Skills"
source: https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills/
crawled: 2026-09-14
translated: 2026-09-14
---

# 改进 skill-creator：测试、衡量并打磨 Agent Skills

> 原文：[Improving skill-creator: Test, measure, and refine Agent Skills](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills/) · Claude 博客

skill-creator 现在可以帮你编写 eval（评估）、运行基准测试，并在模型演进的过程中确保你的 skills 持续可用。这些更新现已在 Claude.ai 和 Cowork 中上线，也以 [Claude Code 插件](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator)的形式提供，并可在[我们的仓库](https://github.com/anthropics/skills/tree/main/skills/skill-creator)中获取。

自去年 10 月[发布 Agent Skills](https://claude.com/blog/skills) 以来，我们注意到大多数 skill 作者都是领域专家，而非工程师。他们熟悉自己的工作流，却没有工具来判断：一个 skill 在新模型上是否仍然有效、是否会在该触发的时候触发、以及一次编辑之后它是否真的变好了。

今天，我们宣布 skill-creator 的一系列增强，帮助作者更有信心地构建。我们把软件开发中的部分严谨实践（测试、基准测试、迭代改进）带到 skill 编写中，而且不要求任何人写代码。

## **两类 skill**

Skills 大致分为两类：

**能力增强（capability uplift）**类 skill 帮助 Claude 完成基础模型做不到、或无法稳定做到的事情。我们的[文档创建 skills](https://github.com/anthropics/skills/tree/main/skills) 就是很好的例子。它们把一些技巧和模式固化下来，产生的输出比单靠提示更好。

**编码偏好（encoded preference）**类 skill 记录的是这样一些工作流：Claude 本来就能完成其中每一步，但 skill 会按照你团队的流程把这些步骤编排起来。例如：一个按照既定标准走完 NDA 审查的 skill，或者一个利用来自多个 MCP 的数据起草每周更新的 skill。

这一区分很重要，因为这两类 skill 需要测试的原因可能不同：

- 能力增强类 skill 可能随着模型进步而变得不再那么必要。eval 能告诉你什么时候出现了这种情况。
- 编码偏好类 skill 更持久，但其价值取决于它对你的实际工作流的还原程度。eval 正是验证这种还原度。

无论哪种情况，测试都能把一个*看起来*有效的 skill，变成一个你*确知*有效的 skill。

## **用 eval 测试并改进 skills**

skill-creator 现在可以帮你编写 eval——即检查 Claude 在给定提示下是否做出你所期待行为的测试。如果你写过软件测试，这会非常眼熟：定义若干测试提示（必要时加上文件），描述「好」是什么样子，然后 skill-creator 会告诉你这个 skill 是否经得起检验。

以我们的 PDF skill 为例，它此前在处理不可填写表单时表现不佳。Claude 必须在没有已定义字段可供参照的情况下，把文本放置到精确坐标上。eval 定位出了这个失败，我们随后发布了修复，把文本定位锚定到提取出的文本坐标上。

eval 的用处很多，其中两个重要用途是：捕捉质量退化（regression），以及了解模型的进步。

第一，**捕捉质量退化。**随着模型及其周边基础设施的演进，上个月运行良好的 skill 今天也许表现不同。在新模型上运行 eval，能在变化影响到你团队工作之前给出早期信号。

第二，**知道通用模型能力何时已超越你的 skill。**这主要适用于能力增强类 skill。如果基础模型在*不加载* skill 的情况下也能通过你的 eval，那就是一个信号：skill 中的技巧可能已被吸收进模型的默认行为。skill 并没有坏，只是不再必要了。

我们还添加了**基准测试模式（benchmark mode）**，用你的 eval 运行一次标准化评估。你可以在模型更新之后，或者在迭代 skill 本身的过程中运行它。它会跟踪 eval 通过率、耗时和 token 用量。

你的 eval 和结果完全归你所有。可以在本地存储，接入仪表盘，或接入 CI 系统。

## **借助多智能体支持实现更快、更一致的评估**

顺序运行 eval 可能很慢，而且累积的上下文可能在各次测试运行之间相互渗透。skill-creator 现在通过**多智能体支持（multi-agent support）**启动相互独立的智能体并行运行 eval——每个都在干净的上下文中运行，拥有各自的 token 与耗时指标。结果更快，且没有交叉污染。

我们还添加了用于 A/B 对比的**比较智能体（comparator agents）**：可以是两个 skill 版本之间的对比，也可以是有 skill 与无 skill 的对比。它们在不知道哪个是哪个的情况下评判输出，因此你能看出某项改动是否真的有效。

## **让 skill 在正确的时机触发**

eval 衡量的是输出质量，但前提是你的 skill 要在该触发的时候触发。随着 skill 数量的增长，描述的精确性变得至关重要：太宽泛会产生误触发，太狭窄则永远不会触发。skill-creator 现在可以帮你调优描述以获得更可靠的触发——它会对照示例提示分析你当前的描述，并给出既能减少误报（false positive）又能减少漏报（false negative）的修改建议。

我们在文档创建 skills 上运行了这一功能，6 个公开 skill 中有 5 个的触发效果得到改善。

## **展望未来**

随着模型的进步，「skill」与「规格说明」（specification）之间的界线可能会变得模糊。今天，一个 SKILL.md 文件本质上是一份实现计划，用详细的指令告诉 Claude *如何*做某件事。假以时日，只需一段自然语言描述这个 skill *应该做什么*，剩下的交给模型去解决，也许就足够了。

我们今天发布的 eval 框架正是朝这个方向迈出的一步。eval 已经描述了「做什么」。最终，这段描述本身可能就是 skill。

## 开始使用

所有 skill-creator 更新现已在 Claude.ai 和 Cowork 上可用。让 Claude 使用 skill-creator，即可开始。

Claude Code 用户可以安装[插件](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator)，或从我们的[仓库](https://github.com/anthropics/skills/tree/main/skills/skill-creator)下载。

FAQ（常见问题）
