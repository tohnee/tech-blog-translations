---
title: "用 GPT-5.4 设计令人愉悦的前端"
title_en: "Designing delightful frontends with GPT-5.4"
source: https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4/
crawled: 2026-09-14
translated: 2026-09-14
---

# 用 GPT-5.4 设计令人愉悦的前端

> 原文：[Designing delightful frontends with GPT-5.4](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4/) · OpenAI 开发者博客

GPT-5.4 是比前辈们更出色的 Web 开发者——能够生成更具视觉吸引力、更大胆进取的前端。值得注意的是，我们在训练 GPT-5.4 时重点提升了 UI 能力与图像的运用。只要引导得当，模型就能产出可直接投入生产的前端，融入细腻的笔触、精心打磨的交互与优美的图像。

Web 设计可能产生的结果面非常大。出色的设计在克制与创造之间取得平衡——既借鉴经受住时间考验的模式，又引入新意。GPT-5.4 已经学习了这一广阔的设计方法光谱，理解网站可以被构建出来的许多不同方式。

当提示词不够具体时，模型往往会退回到训练数据中的高频模式。其中一些是经过验证的惯例，但许多只是出现频率过高、我们想要避免的习惯。结果通常说得过去、也能用，但可能滑向千篇一律的结构、薄弱的视觉层级，以及达不到我们脑海中构想的那些设计选择。

本指南介绍一些实用技巧，帮助你引导 GPT-5.4 打造出你设想中的设计。

## 模型改进

虽然 GPT-5.4 在[多个维度](https://openai.com/index/introducing-gpt-5-4/)上都有提升，但就前端工作而言，我们聚焦于三项实际的收益：

- 在整个设计过程中更强的图像理解能力
- 功能上更完整的应用与网站
- 更善于使用工具来检查、测试并验证自己的工作

### 图像理解与工具使用

GPT-5.4 经过了原生使用图像搜索与图像生成工具的训练，可以把视觉推理直接融入其设计过程。为获得最佳效果，请指示模型先生成一块情绪板（mood board）或几个视觉方案，再挑选最终素材。

你可以通过明确描述图像应当捕捉的属性（例如风格、配色、构图或情绪），引导模型找到出色的视觉参考。你还应当在提示词中加入指引，让模型复用此前生成的图像、调用图像生成工具创建新的视觉素材，或在需要时参考特定的外部图像。

```
Default to using any uploaded/pre-generated images. Otherwise use the image generation tool to create visually stunning image artifacts. Do not reference or link to web images unless the user explicitly asks for them.
```

### 功能性改进

模型经过了训练，能够开发更完整、功能上更健全的应用。可以预期模型在长程任务上更加可靠。那些你以前认为不可能实现的游戏与复杂用户体验，现在一两轮对话就能成为现实。

### Computer Use 与验证

GPT-5.4 是我们第一个为计算机操作（computer use）训练的主线模型。它可以原生地在界面中导航，再结合 Playwright 等工具，就能迭代地检查自己的工作、验证行为并完善实现——支撑更长、更自主的开发工作流。

观看我们的[发布视频](https://openai.com/index/introducing-gpt-5-4/?video=1170427106%20)，看看这些能力的实际表现。

Playwright 对前端开发尤其有价值。它让模型能够检查渲染后的页面、在多个视口下测试、遍历应用流程，并发现状态或导航方面的问题。提供 Playwright 工具或 skill 能显著提高 GPT-5.4 产出精致、功能完整界面的可能性。凭借改进的图像理解能力，它还为模型提供了一种以视觉方式验证工作、并在提供了参考 UI 时检查自己是否与之相符的途径。

## 实用技巧快速上手

如果你只打算采纳本文中的少数几条做法，请从这些开始：

1. 先选择低推理档位（reasoning level）。
2. 预先定义你的设计系统与约束（例如字体排印、配色、布局）。
3. 提供视觉参考或情绪板（例如附上一张截图），为模型提供视觉护栏。
4. 预先定义叙事或内容策略，以指导模型的内容创作。

下面是一个上手提示词。

```
## Frontend tasks

When doing frontend design tasks, avoid generic, overbuilt layouts.

**Use these hard rules:**
- One composition: The first viewport must read as one composition, not a dashboard (unless it's a dashboard).
- Brand first: On branded pages, the brand or product name must be a hero-level signal, not just nav text or an eyebrow. No headline should overpower the brand.
- Brand test: If the first viewport could belong to another brand after removing the nav, the branding is too weak.
- Typography: Use expressive, purposeful fonts and avoid default stacks (Inter, Roboto, Arial, system).
- Background: Don't rely on flat, single-color backgrounds; use gradients, images, or subtle patterns to build atmosphere.
- Full-bleed hero only: On landing pages and promotional surfaces, the hero image should be a dominant edge-to-edge visual plane or background by default. Do not use inset hero images, side-panel hero images, rounded media cards, tiled collages, or floating image blocks unless the existing design system clearly requires it.
- Hero budget: The first viewport should usually contain only the brand, one headline, one short supporting sentence, one CTA group, and one dominant image. Do not place stats, schedules, event listings, address blocks, promos, "this week" callouts, metadata rows, or secondary marketing content in the first viewport.
- No hero overlays: Do not place detached labels, floating badges, promo stickers, info chips, or callout boxes on top of hero media.
- Cards: Default: no cards. Never use cards in the hero. Cards are allowed only when they are the container for a user interaction. If removing a border, shadow, background, or radius does not hurt interaction or understanding, it should not be a card.
- One job per section: Each section should have one purpose, one headline, and usually one short supporting sentence.
- Real visual anchor: Imagery should show the product, place, atmosphere, or context. Decorative gradients and abstract backgrounds do not count as the main visual idea.
- Reduce clutter: Avoid pill clusters, stat strips, icon rows, boxed promos, schedule snippets, and multiple competing text blocks.
- Use motion to create presence and hierarchy, not noise. Ship at least 2-3 intentional motions for visually led work.
- Color & Look: Choose a clear visual direction; define CSS variables; avoid purple-on-white defaults. No purple bias or dark mode bias.
- Ensure the page loads properly on both desktop and mobile.
- For React code, prefer modern patterns including useEffectEvent, startTransition, and useDeferredValue when appropriate if used by the team. Do not add useMemo/useCallback by default unless already used; follow the repo's React Compiler guidance.

Exception: If working within an existing website or design system, preserve the established patterns, structure, and visual language.
```

## 打造更好设计的技巧

### 从设计原则开始

定义一些约束，例如：一个 H1 标题、不超过六个区块、至多两种字体、一个强调色，以及首屏之内只有一个主要 CTA。

### 提供视觉参考

参考截图或情绪板能帮助模型推断布局节奏、字体比例、间距系统与图像处理方式。下面是一个 GPT-5.4 自行生成情绪板供用户审阅的例子。

*在 Codex 中用 GPT-5.4 创作的情绪板，灵感来自纽约咖啡文化与 Y2K 美学*

在 Codex 中用 GPT-5.4 创作的情绪板，灵感来自纽约咖啡文化与 Y2K 美学

### 把页面组织成叙事

典型的营销页面结构：

1. Hero——确立身份与承诺
2. 辅助图像——展示背景或环境
3. 产品细节——解释所提供的产品
4. 社会证明——建立可信度
5. 最终 CTA——把兴趣转化为行动

### 要求遵循设计系统

鼓励模型在构建早期就建立清晰的设计系统。定义核心设计令牌（design tokens），例如 `background`、`surface`、`primary text`、`muted text` 与 `accent`，以及 `display`、`headline`、`body`、`caption` 等字体角色。这种结构帮助模型在整个应用中产出一致、可扩展的 UI 模式。

对大多数 Web 项目来说，从 **React 和 Tailwind** 这类熟悉的栈起步效果很好。GPT-5.4 在这些工具上表现尤为出色，让快速迭代并达到精致结果变得更容易。

动效与分层的 UI 元素可能引入复杂性，尤其是当固定或浮动组件与主要内容发生互动时。在处理动画、覆盖层或装饰层时，加入鼓励安全布局行为的指引会有帮助。例如：

```
Keep fixed or floating UI elements from overlapping text, buttons, or other key content across screen sizes. Place them in safe areas, behind primary content where appropriate, and maintain sufficient spacing.
```

### 调低推理档位

对较简单的网站来说，推理越多并不总是越好。实践中，**低与中推理档位往往能带来更好的前端结果**，帮助模型保持快速、专注、不容易过度思考，同时仍留有余地，在更有野心的设计上把推理调高。

### 让设计立足于真实内容

给模型提供真实的文案、产品背景或清晰的项目目标，是改善前端结果最简单的方法之一。这些上下文能帮助它选择合适的站点结构、塑造更清晰的区块级叙事，写出更可信的文案，而不是退回到通用的占位模式。

## 用 Frontend Skill 把这一切整合起来

为了帮助大家在通用前端任务上充分发挥 GPT-5.4 的能力，我们还准备了一个专门的 [`frontend-skill`](https://github.com/openai/skills/tree/main/skills/.curated/frontend-skill)，可以在下方找到。它在结构、品味与交互模式上给模型更强的指引，帮助它开箱即产出更精致、更有意图、更令人愉悦的设计。

```
---
name: frontend-skill
description: Use when the task asks for a visually strong landing page, website, app, prototype, demo, or game UI. This skill enforces restrained composition, image-led hierarchy, cohesive content structure, and tasteful motion while avoiding generic cards, weak branding, and UI clutter.
---

# Frontend skill

Use this skill when the quality of the work depends on art direction, hierarchy, restraint, imagery, and motion rather than component count.

Goal: ship interfaces that feel deliberate, premium, and current. Default toward award-level composition: one big idea, strong imagery, sparse copy, rigorous spacing, and a small number of memorable motions.

## Working Model

Before building, write three things:

- visual thesis: one sentence describing mood, material, and energy
- content plan: hero, support, detail, final CTA
- interaction thesis: 2-3 motion ideas that change the feel of the page

Each section gets one job, one dominant visual idea, and one primary takeaway or action.

## Beautiful Defaults

- Start with composition, not components.
- Prefer a full-bleed hero or full-canvas visual anchor.
- Make the brand or product name the loudest text.
- Keep copy short enough to scan in seconds.
- Use whitespace, alignment, scale, cropping, and contrast before adding chrome.
- Limit the system: two typefaces max, one accent color by default.
- Default to cardless layouts. Use sections, columns, dividers, lists, and media blocks instead.
- Treat the first viewport as a poster, not a document.

## Landing Pages

Default sequence:

1. Hero: brand or product, promise, CTA, and one dominant visual
2. Support: one concrete feature, offer, or proof point
3. Detail: atmosphere, workflow, product depth, or story
4. Final CTA: convert, start, visit, or contact

Hero rules:

- One composition only.
- Full-bleed image or dominant visual plane.
- Canonical full-bleed rule: on branded landing pages, the hero itself must run edge-to-edge with no inherited page gutters, framed container, or shared max-width; constrain only the inner text/action column.
- Brand first, headline second, body third, CTA fourth.
- No hero cards, stat strips, logo clouds, pill soup, or floating dashboards by default.
- Keep headlines to roughly 2-3 lines on desktop and readable in one glance on mobile.
- Keep the text column narrow and anchored to a calm area of the image.
- All text over imagery must maintain strong contrast and clear tap targets.

If the first viewport still works after removing the image, the image is too weak. If the brand disappears after hiding the nav, the hierarchy is too weak.

Viewport budget:

- If the first screen includes a sticky/fixed header, that header counts against the hero. The combined header + hero content must fit within the initial viewport at common desktop and mobile sizes.
- When using `100vh`/`100svh` heroes, subtract persistent UI chrome (`calc(100svh - header-height)`) or overlay the header instead of stacking it in normal flow.

## Apps

Default to Linear-style restraint:

- calm surface hierarchy
- strong typography and spacing
- few colors
- dense but readable information
- minimal chrome
- cards only when the card is the interaction

For app UI, organize around:

- primary workspace
- navigation
- secondary context or inspector
- one clear accent for action or state

Avoid:

- dashboard-card mosaics
- thick borders on every region
- decorative gradients behind routine product UI
- multiple competing accent colors
- ornamental icons that do not improve scanning

If a panel can become plain layout without losing meaning, remove the card treatment.

## Imagery

Imagery must do narrative work.

- Use at least one strong, real-looking image for brands, venues, editorial pages, and lifestyle products.
- Prefer in-situ photography over abstract gradients or fake 3D objects.
- Choose or crop images with a stable tonal area for text.
- Do not use images with embedded signage, logos, or typographic clutter fighting the UI.
- Do not generate images with built-in UI frames, splits, cards, or panels.
- If multiple moments are needed, use multiple images, not one collage.

The first viewport needs a real visual anchor. Decorative texture is not enough.

## Copy

- Write in product language, not design commentary.
- Let the headline carry the meaning.
- Supporting copy should usually be one short sentence.
- Cut repetition between sections.
- do not include prompt language or design commentary into the UI
- Give every section one responsibility: explain, prove, deepen, or convert.

If deleting 30 percent of the copy improves the page, keep deleting.

## Utility Copy For Product UI

When the work is a dashboard, app surface, admin tool, or operational workspace, default to utility copy over marketing copy.

- Prioritize orientation, status, and action over promise, mood, or brand voice.
- Start with the working surface itself: KPIs, charts, filters, tables, status, or task context. Do not introduce a hero section unless the user explicitly asks for one.
- Section headings should say what the area is or what the user can do there.
- Good: "Selected KPIs", "Plan status", "Search metrics", "Top segments", "Last sync".
- Avoid aspirational hero lines, metaphors, campaign-style language, and executive-summary banners on product surfaces unless specifically requested.
- Supporting text should explain scope, behavior, freshness, or decision value in one sentence.
- If a sentence could appear in a homepage hero or ad, rewrite it until it sounds like product UI.
- If a section does not help someone operate, monitor, or decide, remove it.
- Litmus check: if an operator scans only headings, labels, and numbers, can they understand the page immediately?

## Motion

Use motion to create presence and hierarchy, not noise.

Ship at least 2-3 intentional motions for visually led work:

- one entrance sequence in the hero
- one scroll-linked, sticky, or depth effect
- one hover, reveal, or layout transition that sharpens affordance

Prefer Framer Motion when available for:

- section reveals
- shared layout transitions
- scroll-linked opacity, translate, or scale shifts
- sticky storytelling
- carousels that advance narrative, not just fill space
- menus, drawers, and modal presence effects

Motion rules:

- noticeable in a quick recording
- smooth on mobile
- fast and restrained
- consistent across the page
- removed if ornamental only

## Hard Rules

- No cards by default.
- No hero cards by default.
- No boxed or center-column hero when the brief calls for full bleed.
- No more than one dominant idea per section.
- No section should need many tiny UI devices to explain itself.
- No headline should overpower the brand on branded pages.
- No filler copy.
- No split-screen hero unless text sits on a calm, unified side.
- No more than two typefaces without a clear reason.
- No more than one accent color unless the product already has a strong system.

## Reject These Failures

- Generic SaaS card grid as the first impression
- Beautiful image with weak brand presence
- Strong headline with no clear action
- Busy imagery behind text
- Sections that repeat the same mood statement
- Carousel with no narrative purpose
- App UI made of stacked cards instead of layout

## Litmus Checks

- Is the brand or product unmistakable in the first screen?
- Is there one strong visual anchor?
- Can the page be understood by scanning headlines only?
- Does each section have one job?
- Are cards actually necessary?
- Does motion improve hierarchy or atmosphere?
- Would the design still feel premium if all decorative shadows were removed?

```

在 Codex 应用中运行以下命令即可安装 `frontend-skill`：

```
$skill-installer frontend-skill
```

下面是借助 Frontend Design skill 生成的一些示例网站。

### 落地页

### 游戏

### 仪表盘

## 核心要点

当提示词提供了清晰的设计约束、视觉参考、结构化叙事与明确的设计系统时，GPT-5.4 能够生成高质量的前端界面。

我们希望这些技巧能帮助你构建更有辨识度、设计更出色的应用。

如果你想分享一个完全用 GPT-5.4 与 [Codex](http://developers.openai.com/codex) 这样的编程智能体生成的项目，欢迎提交你的应用，在我们的[展示廊](http://developers.openai.com/showcase)中亮相。
