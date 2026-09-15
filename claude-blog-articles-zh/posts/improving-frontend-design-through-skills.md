---
title: "通过 Skills 改进前端设计"
title_en: "Improving frontend design through Skills"
source: https://claude.com/blog/improving-frontend-design-through-skills/
crawled: 2026-09-14
translated: 2026-09-14
---

# 通过 Skills 改进前端设计

> 原文：[Improving frontend design through Skills](https://claude.com/blog/improving-frontend-design-through-skills/) · Claude 博客

你可能已经注意到：如果让 LLM 在没有任何指引的情况下构建一个落地页，它几乎总会千篇一律地使用 Inter 字体、白底紫色渐变，外加极少的动画。

问题出在哪？[分布收敛](https://en.wikipedia.org/wiki/Convergence_of_random_variables)（distributional convergence）。在采样过程中，模型依据训练数据中的统计模式来预测 token。稳妥的设计选择——那些放之四海皆准、谁也不得罪的方案——在网络训练数据中占据主导。没有方向指引时，Claude 就会从这个高概率中心区域采样。

对于构建面向用户产品的开发者而言，这种千篇一律的美学会削弱品牌辨识度，让 AI 生成的界面一眼即被认出——也随之被一眼略过。

### 可引导性难题

好消息是，只要提示得当，Claude 具有很强的可引导性（steerability）。告诉 Claude「避免使用 Inter 和 Roboto」或「用氛围感背景代替纯色」，结果会立刻改善。这种对指引的敏感是一种特性：它意味着 Claude 可以适应不同的设计语境、约束条件和审美偏好。

但这也带来了一个现实挑战：任务越专门，需要提供的上下文就越多。就前端设计而言，有效的指引涵盖排版原则、色彩理论、动画模式和背景处理。你需要在多个维度上指明哪些默认值应当避开、哪些替代方案值得优先采用。

你可以把这些统统塞进系统提示，但这样一来，每一个请求——调试 Python、分析数据、写邮件——都会携带前端设计上下文。问题于是变成：如何恰好在需要时向 Claude 提供领域专属指引，又不给无关任务带来永久性的上下文开销？

## **Skills：动态上下文加载**

这正是 [Skills](https://www.anthropic.com/news/skills)（智能体技能）的设计初衷：按需交付专门化的上下文，而不带来永久性开销。skill 是一份文档（通常是 markdown），包含指令、约束和领域知识，存放在指定目录中，Claude 可以通过简单的文件读取工具访问它。Claude 可以借助这些 skills 在运行时动态加载所需信息，逐步增强自己的上下文，而不是一开始就把所有内容全部加载。

在配备这些 skills 以及读取它们所需的工具之后，Claude 能够根据手头的任务自主识别并加载相关 skill。例如，当被要求构建落地页或创建 React 组件时，Claude 可以加载一个前端设计 skill，并按需（just-in-time）应用其中的指令。这是最核心的思维模型：skills 是按需激活的提示与上下文资源，为特定任务类型提供专门化指引，却不产生永久性的上下文开销。

这让开发者既能收获 Claude 可引导性的好处，又不必把许多互不相干任务的指令一股脑塞进系统提示而压垮上下文窗口。正如我们此前[所解释的](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)，上下文窗口中的 token 过多会导致性能退化，因此让上下文窗口的内容保持精炼聚焦，对于激发模型的最佳表现极为重要。Skills 通过让有效的提示变得可复用、可按语境加载，解决了这个问题。

## **通过提示获得更好的前端输出**

通过创建一个前端设计 skill，我们可以在不付出永久性上下文开销的前提下，让 Claude 生成明显更好的 UI。核心洞见是：像前端工程师那样思考前端设计。你越能把美学上的改进映射为可实现的前端代码，Claude 就执行得越好。

基于这一洞见，我们找到了几个针对性提示效果很好的领域：排版、动画、背景效果和主题。它们都能干净利落地转化为 Claude 可以编写的代码。在提示中落实这些并不需要详尽的技术说明，只需使用有针对性的语言，促使模型对这些设计维度进行更深入的批判性思考，就足以引出更强的输出。这与我们在[上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)博客文章中给出的指引高度一致：在合适的高度上向模型提示，避免两个极端——低空硬编码式的逻辑（比如指定精确的十六进制色值），与高空含糊其辞、默认模型与你共享上下文的指引。

### **排版**

为了看看实际效果，我们先从排版入手，把它当作可以通过提示影响的一个维度。下面的提示专门引导 Claude 使用更有意思的字体：

```
<use_interesting_fonts>
Typography instantly signals quality. Avoid using boring, generic fonts.

Never use: Inter, Roboto, Open Sans, Lato, default system fonts

Here are some examples of good, impactful choices:
- Code aesthetic: JetBrains Mono, Fira Code, Space Grotesk
- Editorial: Playfair Display, Crimson Pro
- Technical: IBM Plex family, Source Sans 3
- Distinctive: Bricolage Grotesque, Newsreader

Pairing principle: High contrast = interesting. Display + monospace, serif + geometric sans, variable font across weights.

Use extremes: 100/200 weight vs 800/900, not 400 vs 600. Size jumps of 3x+, not 1.5x.

Pick one distinctive font, use it decisively. Load from Google Fonts.
</use_interesting_fonts>
```

**使用基础提示生成的输出：**

**使用基础提示加排版段落生成的输出**

‍

有趣的是，强制使用更有意思的字体，似乎也促使模型顺带改进了设计的其他方面。

仅排版一项就带来了显著改进，但字体只是其中一个维度。那么贯穿整个界面的一致美学呢？

### **主题**

另一个可以提示的维度，是借鉴知名主题与美学的风格设计。Claude 对流行主题有着丰富的理解；我们可以利用这一点，传达希望前端呈现的特定美学。下面是一个例子：

```
<always_use_rpg_theme>
Always design with RPG aesthetic:
- Fantasy-inspired color palettes with rich, dramatic tones
- Ornate borders and decorative frame elements
- Parchment textures, leather-bound styling, and weathered materials
- Epic, adventurous atmosphere with dramatic lighting
- Medieval-inspired serif typography with embellished headers
</always_use_rpg_theme>
```

这会生成如下 RPG 主题的 UI：

排版与主题的例子说明针对性提示确实有效。但手动指定每个维度十分繁琐。如果能把这些改进合并成一个可复用的资产呢？

### **一份通用提示**

同样的原则也适用于其他设计维度：针对动效（动画与微交互）进行提示，可以补上静态设计所欠缺的精致感；引导模型选择更有意思的背景，则能营造深度和视觉趣味。这正是全面型 skill 大放异彩之处。

把这一切整合起来，我们开发了一份约 400 token 的提示——足够精简，加载后不会撑爆上下文（即便作为 skill 加载也是如此）——它在排版、色彩、动效和背景各方面都显著改善了前端输出：

```
<frontend_aesthetics>
You tend to converge toward generic, "on distribution" outputs. In frontend design,this creates what users call the "AI slop" aesthetic. Avoid this: make creative,distinctive frontends that surprise and delight. 

Focus on:
- Typography: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics.
- Color & Theme: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.
- Motion: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions.
- Backgrounds: Create atmosphere and depth rather than defaulting to solid colors. Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic.

Avoid generic AI-generated aesthetics:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

Interpret creatively and make unexpected choices that feel genuinely designed for the context. Vary between light and dark themes, different fonts, different aesthetics. You still tend to converge on common choices (Space Grotesk, for example) across generations. Avoid this: it is critical that you think outside the box!
</frontend_aesthetics>
```

在上面的示例中，我们首先向 Claude 给出关于问题本身以及我们想解决什么的一般性上下文。我们发现，向模型提供这类高层上下文是一种有助于校准输出的提示技巧。随后，我们列出前面讨论过的那些设计改进向量，并给出针对性建议，鼓励模型在所有这些维度上进行更有创造性的思考。

我们还在结尾附加了一段指引，防止 Claude 收敛到另一个局部最优（local maximum）。即便明确要求避免某些模式，模型也可能退回到其他常见选择（比如排版上选 Space Grotesk）。最后那句「跳出思维定式」的提醒，就是为了强化创意上的多样性。

### **对前端设计的影响**

启用这个 skill 后，Claude 在多类前端设计上的输出都有改善，包括：

**示例 1：SaaS 落地页**

**图注：**AI 生成的 SaaS 落地页，使用平庸的 Inter 字体、紫色渐变和标准布局。未使用任何 skill。

**图注：**AI 生成的前端，使用与上图渲染相同的提示外加前端 skill，现在具备了独特的排版、协调的配色和分层的背景。

**示例 2：博客布局**

AI 生成的博客布局，使用默认系统字体和平铺的白色背景。未使用任何 skill。

AI 生成的博客布局，使用相同提示外加前端 skill，呈现出杂志感字体、氛围深度与考究的间距。

**示例 3：管理后台**

AI 生成的管理后台，采用标准 UI 组件，视觉层级几近于无。未使用任何 skill。

AI 生成的管理后台，使用相同提示外加前端 skill，具备大胆的排版、协调的深色主题和有目的性的动效。

## **用 Skills 改进 [claude.ai](http://claude.ai) 中的 artifact 质量**

设计品味并不是唯一的局限。Claude 在构建 artifacts 时还面临架构上的约束。[Artifacts](https://support.claude.com/en/articles/9487310-what-are-artifacts-and-how-do-i-use-them) 是 Claude 在聊天旁边创建并展示的交互式、可编辑内容（例如代码或文档）。

除了上面探讨的设计品味问题，Claude 在 [claude.ai](http://claude.ai) 中还有一个默认行为，限制了它生成出色前端 artifact 的能力。目前，被要求创建前端时，Claude 只会构建一个包含 CSS 和 JS 的单个 HTML 文件。这是因为 Claude 知道：前端必须是单个 HTML 文件，才能作为 artifact 正确渲染。

就像人类开发者如果只能在单个文件里写 HTML/CSS/JS，也只能做出非常基础的前端一样，我们假设：如果给 Claude 指令去使用更丰富的工具链，它就能生成更令人惊艳的前端 artifact。

这促使我们创建了一个 [web-artifacts-builder skill](https://github.com/anthropics/skills/blob/main/web-artifacts-builder/SKILL.md)，它利用 Claude [使用计算机](https://www.claude.com/blog/create-files)（computer use）的能力，引导 Claude 使用多文件以及 [React](https://react.dev/)、[Tailwind CSS](https://tailwindcss.com/)、[shadcn/ui](https://ui.shadcn.com/) 等现代 Web 技术来构建 artifact。在底层，这个 skill 暴露了一些脚本：(1) 帮助 Claude 高效搭建一个基础 React 仓库；(2) 在 Claude 完成编辑后，用 [Parcel](https://parceljs.org/) 把所有内容打包成单个文件，以满足单 HTML 文件的要求。这正是 skills 的核心优势之一：让 Claude 能够调用脚本去执行样板化操作，从而在最小化 token 用量的同时提升可靠性与性能。

有了 web-artifacts-builder skill，Claude 就能利用 shadcn/ui 的表单组件和 Tailwind 的响应式网格系统，创建更完整的 artifact。

**示例 1：白板应用**

例如，在没有 web-artifacts-builder skill 的情况下被要求创建一个白板应用时，Claude 输出了一个十分简陋的界面：

而在使用新的 web-artifacts-builder skill 时，Claude 开箱即生成了一款干净得多、功能丰富的应用，支持绘制不同形状和文字：

**示例 2：任务管理应用**

类似地，被要求创建一个任务管理应用时，没有这个 skill 的 Claude 生成了一款功能可用但极其简朴的应用：

有了这个 skill，Claude 生成了一款开箱即功能丰富的应用。例如，Claude 加入了「Create New Task」（新建任务）表单组件，允许用户为任务设置类别（Category）和截止日期（Due Date）：

要在 [Claude.ai](http://claude.ai) 中试用这个新 skill，只需启用它，然后在构建 artifact 时让 Claude「使用 web-artifacts-builder skill」。

## **用 Skills 优化 Claude 的前端设计能力**

这个前端设计 skill 揭示了关于语言模型能力的一个更普遍的原理：模型往往具备超出其默认表现的能力。Claude 拥有很强的设计理解力，但在没有指引时，分布收敛会把这份能力掩盖起来。固然可以把这些指令加进系统提示，但那意味着每个请求都会携带前端设计上下文，即便这些知识与手头任务毫不相干。而使用 Skills，则能把 Claude 从一个需要不断指引的工具，变成一个为每项任务带来领域专长的伙伴。

Skills 还高度可定制——你可以创建完全贴合自身需求的 skill。这让你能够精确定义要固化进 skill 的基本要素，无论是你公司的设计系统、特定的组件模式，还是行业专属的 UI 惯例。把这些决策编码进 Skill，你就把智能体思考过程中的组成部分转化为整个开发团队都能复用的资产。这个 skill 成为可持续沉淀、可扩展的组织知识，确保各项目之间质量一致。

这一模式并不限于前端工作。凡是 Claude 明明具备更广博的理解、输出却流于平庸的领域，都是开发 Skill 的候选对象。方法始终如一：识别收敛性的默认选择，提供具体的替代方案，在合适的高度上组织指引，并通过 Skills 使其可复用。

对前端开发而言，这意味着 Claude 无需针对每个请求做提示工程，也能生成独具特色的界面。要开始上手，可以探索我们的[前端设计 cookbook](https://github.com/anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb)，或试用我们的[ Claude Code 全新前端设计插件](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design)。

**心动了？要创建你自己的前端 skill，请查看我们的 [skill-creator](https://github.com/anthropics/skills/tree/main/skill-creator)。**

**致谢**
本文由 Anthropic 应用 AI 团队的 Prithvi Rajasekaran、Justin Wei 和 Alexander Bricken 撰写，营销合作伙伴 Molly Vorwerck 和 Ryan Whitehead 亦有贡献。

## Agent Skills

今天就开始用 Skills 与 Claude 一起构建更强大的应用。

FAQ（常见问题）
