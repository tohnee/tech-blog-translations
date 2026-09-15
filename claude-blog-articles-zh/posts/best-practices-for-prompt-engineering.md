---
title: "2026 年提示工程最佳实践"
title_en: "Prompt engineering best practices for 2026"
source: https://claude.com/blog/best-practices-for-prompt-engineering/
crawled: 2026-09-14
translated: 2026-09-14
---

# 2026 年提示工程最佳实践

> 原文：[Prompt engineering best practices for 2026](https://claude.com/blog/best-practices-for-prompt-engineering/) · Claude 博客

## 提示工程是什么？

[提示工程](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)是一种通过组织指令来让 AI 模型给出更好输出的技艺。它关乎你如何表述查询、指定风格、提供上下文，以及引导模型的行为来实现你的目标。

模糊的指令与精心打造的提示之间的差距，可能就决定了泛泛而谈的输出与恰如你所愿的结果之间的距离。一个结构糟糕的提示可能需要多轮来回澄清意图，而一个经过精心设计的提示则能一次到位。

提示工程也是[上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)的基础构件，后者已成为与 LLM 打交道时日益重要的一环。一个结构糟糕的提示可能需要多轮来回澄清意图，而一个经过精心设计的提示则能一次到位。不过，对 Claude 5 代模型而言，提示正在与[面向 Claude 5 代模型的上下文工程](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models)融合——更少的脚手架，更多的精心策展。

为了帮助你入门，我们整理了团队的一些最佳实践，其中包括能够立即改善效果的实用方法。我们会从今天就能用上的简单习惯讲起，再逐步进阶到适用于复杂项目的高级方法。

## 如何运用提示工程

在最基础的层面上，提示工程无非就是修改你传给 LLM 的查询。它往往只是在真正提出请求之前往查询里补充信息——但知道*哪些*信息才是*该*分享的信息，正是打造一个出色且有效提示的诀窍所在。

### 核心技巧

这些提示工程技巧构成了高效 AI 交互的基础。坚持使用它们，你就能立刻看到回复质量的提升。

#### 明确而清晰

现代 AI 模型对清晰、明确的指令响应得异常好。不要指望模型自己领会你想要什么——直接说出来。用简单的语言准确说明你想要什么，不要有歧义。

**关键原则**：清楚地告诉模型你想看到什么。如果你想要全面的输出，就直说。如果你想要特定的功能，就列出来。像 Claude 这样的现代模型尤其受益于明确的指引。

**示例：创建一个数据分析仪表盘**

**模糊**：「创建一个数据分析仪表盘」

**明确**：「创建一个数据分析仪表盘。尽可能包含所有相关功能与交互，超越基础水平，做出一个功能完备的实现。」

第二个版本明确要求了全面的功能，并向模型传达了你希望它超越最低限度的信号。

**最佳实践**：

- 以直接的动作动词开头：「撰写」「分析」「生成」「创建」
- 跳过客套话，直奔请求
- 说明你希望输出包含什么，而不只是要处理什么
- 对质量与深度的期望要具体

#### 提供上下文与动机

解释*为什么*某件事重要，能帮助 AI 模型更好地理解你的目标，并给出更有针对性的回复。对于能够推理你深层目标的新一代模型，这一点尤其有效。

**示例：格式偏好**

**效果较差**：「绝对不要使用项目符号列表」

**效果较好**：「我偏好以自然段落而非项目符号列表的形式呈现回复，因为我觉得连贯的行文更易读、更像对话。项目符号列表对我的随意学习风格来说显得太正式、太像清单了。」

第二个版本帮助模型理解规则背后的理由，使它能在相关的格式选择上做出更好的决策。

**何时提供上下文**：

- 说明输出的用途或受众
- 澄清某些约束为何存在
- 描述输出将如何被使用
- 表明你想解决的是什么问题

#### 保持具体

提示工程中的「具体」，指的是用明确的准则和要求来组织你的指令。你对自己想要的东西说得越具体，结果就越好。

**示例：膳食规划**

**模糊**：「为一套地中海饮食制定膳食计划」

**具体**：「为糖尿病前期管理设计一份地中海饮食膳食计划。每日 1,800 卡路里，侧重低升糖食物。列出早餐、午餐、晚餐和一次加餐，并附完整的营养成分明细。」

**怎样的提示才算足够具体？**

包括：

- 清晰的约束（字数、格式、时间线）
- 相关的上下文（受众是谁、目标是什么）
- 期望的输出结构（表格、列表、段落）
- 任何要求或限制（饮食需求、预算上限、技术约束）

#### 使用示例

示例并非总是必需，但在解释概念或演示特定格式时特别出彩。示例也被称为单样本（one-shot）或少样本（few-shot）提示，它用「展示」代替「描述」，能厘清那些仅靠文字描述很难讲清楚的细微要求。

**给现代模型的重要提示**：Claude 4.x 及类似的高级模型对示例中的细节非常敏感。请确保你的示例与你希望鼓励的行为保持一致，并尽量减少任何你想避免的模式。

**示例：文章摘要**

**不用示例**：「总结这篇文章」

```
Here's an example of the summary style I want:

Article: [link to article about AI regulation]
Summary: EU passes comprehensive AI Act targeting high-risk systems. Key provisions include transparency requirements and human oversight mandates. Takes effect 2026.

Now summarize this article in the same style: [link to your new article]
```

**何时使用示例**：

- 期望的格式展示起来比描述更容易
- 你需要特定的语气或风格
- 任务涉及微妙的模式或惯例
- 简单指令未能产生一致的结果

**专业提示**：先从一个示例开始（单样本）。只有当输出仍不符合你的需求时，再增加更多示例（少样本）。

#### 允许 Claude 表达不确定性

明确允许 AI 表达不确定，而不是硬着头皮猜。这能减少幻觉，提高可靠性。

**示例**：「分析这份财务数据并识别趋势。如果数据不足以得出结论，请直说，不要臆测。」

这一简单的补充让模型得以承认自身的局限，从而使回复更值得信赖。

**[在 Claude 中立即尝试这些方法。](https://claude.ai/)**

## 高级提示工程技巧

这些核心习惯已经能带你走得很远，但你仍可能遇到需要更复杂方法的情形。当你构建智能体解决方案、处理复杂的数据结构，或需要拆解多阶段问题时，高级提示工程技巧最能大显身手。

### 预填充 AI 的回复

预填充（prefilling）让你替 AI 起个头，从而引导格式、语气或结构。这一技巧在强制输出格式或跳过客套话时尤其强大。

**何时使用预填充**：

- 你需要 AI 输出 JSON、XML 或其他结构化格式
- 你想跳过对话式的开场白，直奔内容
- 你需要维持特定的嗓音或角色
- 你想控制 AI 回复的开头方式

**示例：强制 JSON 输出**

不使用预填充时，Claude 可能会说：「Here's the JSON you requested: {...}」

使用预填充（API 调用）时：

```
messages=[
    {"role": "user", "content": "Extract the name and price from this product description into JSON."},
    {"role": "assistant", "content": "{"}
]
```

AI 会从左花括号开始续写，只输出合法的 JSON。

**注**：在聊天界面中，你可以通过非常明确的表述来近似实现这一效果：「只输出合法的 JSON，不要任何开场白。以左花括号开始你的回复。」

### 思维链提示

思维链（chain of thought，CoT）提示要求模型在回答之前先进行逐步推理。这一技巧对那些受益于结构化思考的复杂分析任务很有帮助。

**现代做法**：Claude 提供了[扩展思考](https://www.anthropic.com/news/visible-extended-thinking)功能，可以自动完成结构化推理。在可用的情况下，扩展思考通常比手写思维链提示更可取。不过，理解手写 CoT 仍然有价值——当扩展思考不可用，或你需要可审查的透明推理时，它就派上用场。

**何时使用思维链**：

- 扩展思考不可用（例如免费的 [Claude.ai](http://claude.ai) 计划）
- 你需要可审查的透明推理
- 任务需要多个分析步骤
- 你想确保 AI 考虑到特定因素

思维链有三种常见实现方式：

**基础思维链**

只需在指令中加上「Think step-by-step」（逐步思考）。

```
Draft personalized emails to donors asking for contributions to this year's Care for Kids program.

Program information:
<program>
{{PROGRAM_DETAILS}}
</program>

Donor information:
<donor>
{{DONOR_DETAILS}}
</donor>

Think step-by-step before you write the email.
```

**引导式思维链**

组织你的提示，为其提供明确的推理阶段。

```
Think before you write the email. First, think through what messaging might appeal to this donor given their donation history. Then, consider which aspects of the Care for Kids program would resonate with them. Finally, write the personalized donor email using your analysis.
```

**结构化思维链**

用标签把推理过程与最终答案分开。

```
Think before you write the email in <thinking> tags. First, analyze what messaging would appeal to this donor. Then, identify relevant program aspects. Finally, write the personalized donor email in <email> tags, using your analysis.
```

**注**：即便扩展思考可用，对复杂任务而言，显式的 CoT 提示仍然有益。两种方法互补，并不互斥。

### 控制输出格式

对现代 AI 模型，有几种控制回复格式的有效方式：

**1. 告诉 AI 要做什么，而不是不要做什么**

与其说：「不要在回复中使用 markdown」不如试试：「你的回复应当由流畅连贯的散文段落构成」

**2. 让提示风格与期望的输出相匹配**

你在提示中使用的格式风格可能影响 AI 的回复风格。如果你想要最少的 markdown，就减少提示中的 markdown。

**3. 明确说出格式偏好**

要对格式做细致控制：

```
When writing reports or analyses, write in clear, flowing prose using complete paragraphs. Use standard paragraph breaks for organization. Reserve markdown primarily for inline code, code blocks, and simple headings.

DO NOT use ordered lists or unordered lists unless you're presenting truly discrete items where a list format is the best option, or the user explicitly requests a list.

Instead of listing items with bullets, incorporate them naturally into sentences. Your goal is readable, flowing text that guides the reader naturally through ideas.
```

### 链式提示

与前述技巧不同，链式提示（prompt chaining）无法在单个提示中实现。它把复杂任务拆解为若干按顺序执行的小步骤，每一步使用单独的提示。每个提示负责一个阶段，其输出再喂给下一条指令。

这种方式以延迟换取更高的准确率，因为它让每个单独的任务都变得更简单。通常这一技巧会通过工作流或以编程方式实现，但你也可以在收到回复后手动提供后续提示。

**示例：研究摘要**

1. **第一个提示**：「总结这篇医学论文，涵盖研究方法、发现与临床意义。」

1. **第二个提示**：「从准确性、清晰度与完整性三方面审查上面的摘要，给出分级的反馈。」

1. **第三个提示**：「根据以下反馈改进摘要：[第 2 步的反馈]」

每个阶段都通过聚焦的指令完成一层打磨。

**何时使用链式提示**：

- 你有一个需要拆解为多个步骤的复杂请求
- 你需要迭代式的打磨
- 你在做多阶段分析
- 中间环节的验证能带来价值
- 单个提示产生的结果不稳定

**权衡**：链式提示会增加延迟（多次 API 调用），但对复杂任务而言，它往往能显著提升准确性与可靠性。

## 你可能听说过的技巧

一些在早期 AI 模型上颇为流行的提示工程技巧，对如今像 Claude 这样的模型来说已不那么必要。不过，你仍可能在旧文档中遇到它们，或在特定情形中发现它们有用。

### 用 XML 标签组织结构

XML 标签曾是一种被推荐的为提示增加结构与清晰度的方式，尤其是在纳入大量数据时。虽然现代模型在没有 XML 标签的情况下也能更好地理解结构，但它在特定情形下仍然有用。

**示例**：

```
<athlete_information>
- Height: 6'2"
- Weight: 180 lbs
- Goal: Build muscle
- Dietary restrictions: Vegetarian
</athlete_information>

Generate a meal plan based on the athlete information above.
```

**XML 标签可能仍有帮助的情形**：

- 你在处理混合了多种内容类型的极复杂提示
- 你需要对内容边界有百分之百的把握
- 你在使用较旧的模型版本

**现代替代方案**：对大多数用例来说，清晰的标题、空白行与明确的表述（「使用下方运动员信息……」）同样有效，而且开销更小。

### 角色提示

角色提示（role prompting）指在表述查询时定义专家人格与视角。虽然这可能有效，但现代模型已经足够成熟，过重的角色提示往往没有必要。

**示例**：「你是一位财务顾问。分析这个投资组合……」

**重要告诫**：不要过度约束角色。「你是一位乐于助人的助手」通常好过「你是一位只讲技术行话、从不犯错误的世界知名专家」。过于具体的角色会限制 AI 的发挥空间。

**角色提示可能有帮助的情形**：

- 你需要在大量输出中保持一致的语气
- 你在构建一个需要特定人格的应用
- 你想为复杂话题引入领域专家的视角框架

**现代替代方案**：通常，直接说清楚你想要的视角会更有效：「分析这个投资组合，重点关注风险承受能力与长期增长潜力」，而不是先指派一个角色。

[在 Claude 中尝试](https://preview.claude.ai/new)。

## 综合运用

你已经单独见识了各项技巧，但它们真正的威力在于战略性地组合。提示工程的艺术不在于把所有技巧都用上——而在于为你的具体需求挑选正确的组合。

**组合多种技巧的示例**：

```
xtract key financial metrics from this quarterly report and present them in JSON format.

I need this data for automated processing, so it's critical that your response contains ONLY valid JSON with no preamble or explanation.

Use this structure:
{
  "revenue": "value with units",
  "profit_margin": "percentage",
  "growth_rate": "percentage"
}

If any metric is not clearly stated in the report, use null rather than guessing.

Begin your response with an opening brace: {
```

这个提示组合了：

- 明确的指令（准确说明要提取什么）
- 上下文（为什么格式重要）
- 示例结构（展示格式）
- 允许表达不确定性（不确定就用 null）
- 格式控制（以左花括号开头）

## 如何选择合适的技巧

并非每个提示都需要所有技巧。以下是一个决策框架：

**从这里开始：**

1. 你的请求是否清晰明确？如果不是，先打磨清晰度
2. 任务简单吗？只使用核心技巧（具体、清晰、提供上下文）
3. 任务需要特定格式吗？使用示例或预填充
4. 任务复杂吗？考虑拆解（链式）
5. 需要推理吗？使用扩展思考（如可用）或思维链

**技巧选择指南**：

| 如果你需要…… | 使用…… |
|---|---|
| 特定的输出格式 | 示例、预填充或明确的格式指令 |
| 逐步推理 | 扩展思考（Claude 4.x）或思维链 |
| 复杂的多阶段任务 | 链式提示 |
| 透明的推理 | 带结构化输出的思维链 |
| 防止幻觉 | 允许模型说「我不知道」 |

## 常见提示问题排查

即便初衷良好的提示也可能产生意外结果。以下是常见问题及其解决办法：

- **问题：回复太过泛泛** → 解决办法：增加具体性、示例，或明确要求全面的输出。让 AI「超越基础水平」。
- **问题：回复跑题或没抓住重点** → 解决办法：更明确地说明你的真实目标，并提供你为何这样问的上下文。
- **问题：回复格式不一致** → 解决办法：添加示例（少样本）或使用预填充来控制回复的开头。
- **问题：任务太复杂，结果不可靠** → 解决办法：拆分成多个提示（链式）。每个提示只做好一件事。
- **问题：AI 添加了不必要的开场白** → 解决办法：使用预填充，或明确要求：「跳过开场白，直接给答案。」
- **问题：AI 编造信息** → 解决办法：明确允许它在不确定时说「我不知道」。
- **问题：你想要的是实现，AI 却只给建议** → 解决办法：明确表达动作：「修改这个函数」，而不是「你能提点修改建议吗？」

**专业提示**：从简单开始，只在需要时增加复杂度。每加一项都测试一下，看它是否真的改善了结果。

## 要避免的常见错误

从这些常见的坑里吸取教训，节省时间并改进你的提示：

- **不要过度设计**：更长、更复杂的提示并不一定更好。
- **不要忽视基础**：如果核心提示含糊不清，高级技巧也帮不了你。
- **不要指望 AI 会读心**：对你想要的东西要具体。含糊其辞会给 AI 留下误解的空间。
- **不要一次用上所有技巧**：选择能解决你具体挑战的技巧。
- **不要忘记迭代**：第一个提示很少能一次完美。测试并打磨。
- **不要依赖过时的技巧**：对现代模型而言，XML 标签和重度角色提示已不那么必要。从明确、清晰的指令开始。

## 提示工程的其他考量

### 处理长内容

实施高级提示工程的挑战之一在于，它会通过额外的 token 消耗带来上下文开销。示例、多轮提示、详细的指令——它们都会消耗 token，而上下文管理本身就是一门技能。

请记住，在合理且值得的地方才使用提示工程技巧。关于如何有效管理上下文的全面指引，请参阅我们关于[上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)的博客文章。

**上下文感知能力的改进**：包括 Claude 4.x 在内的现代 AI 模型，其上下文感知能力已显著增强，有助于缓解历史上「迷失在中间」（lost-in-the-middle）的问题——过去模型难以对长上下文的各个部分给予同等的关注。

**为什么任务拆分依然有用**：即便有这些改进，把大任务拆成更小、更独立的块仍然是一项有价值的技巧——不是因为上下文长度的限制，而是因为它能帮助模型在非常具体的需求与范围之内专注于做到最好。边界清晰、目标聚焦的任务，始终比试图在单个提示中完成多个目标能产出更高质量的结果。

**策略**：处理长上下文时，把最关键的信息放在开头或结尾，让信息的结构保持清晰。处理复杂任务时，考虑把它们拆成聚焦的子任务是否能提升每个部分的质量与可靠性。

### 提示工程示例：好的提示长什么样

提示工程是一门手艺，你需要多试几次才能掌握。想知道自己做得对不对，唯一的办法就是测试并观察。第一步是自己动手试一试。你马上就能看出用了与没用本文所讲技巧的查询之间的差别。

要真正磨练提示工程技能，你需要客观衡量提示的有效性。好消息是，这正是我们在 [anthropic.skilljar.com](https://anthropic.skilljar.com/claude-with-the-anthropic-api) 上的提示工程课程所讲的内容。

**快速评估技巧**：

- 输出是否符合你的具体要求？
- 你是一次成功，还是需要多轮迭代？
- 多次尝试之间的格式是否一致？
- 你是否避开了上文列出的常见错误？

## 最后的建议

提示工程归根结底是关于沟通：用一种能让 AI 最清楚地理解你意图的语言来表达。从本指南前半部分的核心技巧开始，坚持使用，直到它们成为你的第二本能。只有当高级技巧能解决具体问题时，再把它们叠加进来。

记住：最好的提示不是最长或最复杂的那个，而是以最少的必要结构可靠达成目标的那个。随着练习，你会培养出对「什么情形用什么技巧」的直觉。

对于希望在每个会话而非每个提示中都生效的指令，请把它们移入 [CLAUDE.md 文件、skills 或其他引导方法](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)。不过，向上下文工程的转变并不意味着提示工程的重要性下降。

事实上，提示工程是上下文工程中的基础构件。每一个精心打造的提示都会成为塑造 AI 行为的更大上下文的一部分，与对话历史、附件文件和系统指令协同工作，创造更好的结果。

[立即在 Claude 中开始编写提示。](https://preview.claude.ai/new)

## 更多资源

- [提示工程文档](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
- [交互式提示工程教程](https://github.com/anthropics/prompt-eng-interactive-tutorial)
- [提示工程课程](https://anthropic.skilljar.com/claude-with-the-anthropic-api)
- [上下文工程指南](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

FAQ（常见问题）
