---
title: "面向长时运行应用开发的执行框架设计"
title_en: "Harness design for long-running application development"
source: https://www.anthropic.com/engineering/harness-design-long-running-apps
published: 2026-03-24
crawled: 2026-09-11
translated: 2026-09-11
---

# 面向长时运行应用开发的执行框架设计

> 原文：[Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) · Anthropic Engineering Blog

*作者 Prithvi Rajasekaran，我们 [Labs](https://www.anthropic.com/news/introducing-anthropic-labs) 团队成员。*

过去几个月，我一直在攻克两个相互关联的问题：让 Claude 产出高质量的前端设计，以及让它在无人干预下构建完整应用。这项工作源于我们更早的[前端设计技能](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md)和[长时运行编码智能体框架](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)项目——在那里，我和同事们通过提示工程与框架设计把 Claude 的表现提升到远超基线，但两者最终都撞上了天花板。

为了突破，我寻找能在两个截然不同的领域都成立的新型 AI 工程方法——一个由主观品味定义，另一个由可验证的正确性与可用性定义。从[生成对抗网络](https://en.wikipedia.org/wiki/Generative_adversarial_network)（GAN）汲取灵感，我设计了一个带**生成器**（generator）与**评估器**（evaluator）智能体的多智能体结构。要构建一个能可靠打分——而且打得有品味——的评估器，首先要开发一组标准，把「这个设计好吗？」这类主观判断转化为具体的、可打分的术语。

随后我把这些技术应用到长时运行自主编码上，沿用了早期框架工作的两条经验：把构建分解为可处理的小块，以及用结构化产物在会话间交接上下文。最终成果是一个三智能体架构——规划者（planner）、生成器与评估器——在长达数小时的自主编码会话中产出内容丰富的全栈应用。

## 为什么朴素的实现不够

我们此前已经证明，框架设计对长时运行智能体编码的有效性有显著影响。在更早的[实验](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)中，我们用一个初始化智能体把产品规格分解成任务清单，再由一个编码智能体一次实现一个功能，然后交接产物以在会话间携带上下文。更广的开发者社区也收敛到类似的洞见，例如「[Ralph Wiggum](https://ghuntley.com/ralph/)」方法用钩子或脚本让智能体保持连续的迭代循环。

但仍有一些问题挥之不去。对更复杂的任务，智能体仍倾向于随时间推移跑偏。在拆解这个问题时，我们观察到智能体执行这类任务时有两种常见失败模式。

其一是模型在长任务中随上下文窗口填满而失去连贯性（见我们关于[上下文工程](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)的文章）。一些模型还表现出「上下文焦虑」——当它们自认为接近上下文上限时，开始过早收尾。上下文重置——完全清空上下文窗口、启动全新智能体，配合携带前一智能体状态与后续步骤的结构化交接——同时解决这两个问题。

这不同于压缩（compaction）：压缩是把对话的较早部分就地摘要，让同一个智能体带着缩短的历史继续跑。压缩保留了连续性，却没给智能体一张白纸，上下文焦虑因此仍可能存在。重置提供了白纸，代价是交接产物必须携带足够的状态，让下一个智能体干净地接手。在早期测试中，我们发现 Claude Sonnet 4.5 的上下文焦虑严重到仅靠压缩不足以支撑长任务的强劲表现，因此上下文重置成为框架设计的必要部分。这解决了核心问题，却给每次框架运行增加了编排复杂度、token 开销和延迟。

第二个问题我们此前没有讨论过：自我评估。当被要求评估自己产出的工作时，智能体倾向于自信地赞美这份工作——即便在人看来质量显然平平。这个问题在主观任务（如设计）上尤其突出，因为没有与可验证软件测试等价的二值检查。一个布局是精致还是平庸是判断题，而智能体在给自己打分时可靠地偏向好评。

然而，即便在结果可验证的任务上，智能体有时也表现出糟糕的判断，妨碍它们完成任务。把「干活的智能体」与「评判的智能体」分离，被证明是解决这个问题的有力杠杆。这种分离本身并不能立刻消除宽容倾向——评估器仍是一个倾向对 LLM 生成物慷慨的 LLM。但把一个独立评估器调教得挑剔，远比让生成器批判自己的作品可行得多；而一旦外部反馈存在，生成器就有了可以对照迭代的具体目标。

## 前端设计：让主观质量可打分

我从前端设计开始实验，自我评估问题在这里最显眼。缺乏干预时，Claude 通常趋向安全、可预测的布局——技术上能用，视觉上乏味。

两个洞见塑造了我为前端设计构建的框架。第一，美学无法完全归约为分数——个体品味永远有差异——但可以通过编码设计原则与偏好的打分标准来改进。「这个设计美吗？」很难一致地回答，但「这是否遵循我们的好设计原则？」给了 Claude 具体的打分依据。第二，把前端生成与前端评判分离，可以形成一个反馈循环，推动生成器产出更强的作品。

带着这些想法，我写了四条打分标准，放进生成器与评估器智能体的提示：

- **设计质量：** 这个设计是否浑然一体，而非零件拼凑？这方面的强作品意味着色彩、字体、布局、图像等细节融合出独特的情绪与身份。
- **原创性：** 有没有定制决策的证据，还是模板布局、库默认值和 AI 生成套路？人类设计师应当能识别出刻意的创意选择。未修改的现成组件——或紫渐变叠白卡片这类 AI 生成的标志性痕迹——在此不合格。
- **工艺（Craft）：** 技术执行：字体层级、间距一致性、色彩和谐、对比度。这是能力检查而非创造力检查。大多数合理的实现默认都能过关；不及格意味着基本功坏了。
- **功能性：** 独立于美学的可用性。用户能否理解界面的功能、找到主要操作、不经猜测完成任务？

我把设计质量与原创性的权重放在工艺与功能性之上。Claude 默认在工艺与功能性上得分就不低，所需的技术能力模型天然具备。但在设计与原创性上，Claude 的产出常常至多算是乏味。这些标准明确惩罚高度通用的「AI slop」套路，而加重设计与原创性的权重则推动模型承担更多美学冒险。

我用带详细分数拆解的少样本示例校准了评估器。这确保评估器的判断与我的偏好一致，并减少了跨迭代的分数漂移。

我把这个循环构建在 [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) 上，编排因此保持简单。生成器智能体先根据用户提示创建 HTML/CSS/JS 前端。我给评估器配了 Playwright MCP，让它可以直接与运行中的页面交互，然后给每条标准打分、写出详细批评。实践中，评估器会自己导航页面、截图并仔细研究实现，然后给出评估。这些反馈回流给生成器，成为下一轮迭代的输入。每次生成我跑 5 到 15 轮迭代，每轮通常在回应评估器批评的过程中把生成器推向更有辨识度的方向。因为评估器是主动导航页面而非给静态截图打分，每个周期都消耗真实的挂钟时间。完整运行最长达到四个小时。我还指示生成器在每次评估后做一个策略决策：若分数走势良好就细化当前方向，若路子不对就转向完全不同的美学。

多次运行中，评估器的评估随迭代改进，随后趋于平稳，但仍有上升空间。有些生成是增量打磨；另一些在迭代之间急转美学方向。

标准的措辞以我未完全预料的方式引导了生成器。加入「最好的设计是博物馆级」这类短语，把设计推向某种特定的视觉趋同，说明与标准相关联的提示直接塑造了输出的性格。

虽然分数总体随迭代改善，模式并不总是干净的线性。后期的实现整体更好，但我经常遇到更偏爱中间某轮而非最后一轮的情况。实现复杂度也随轮次增加，生成器会为回应评估器的反馈而伸手够更雄心勃勃的方案。即使在第一轮迭代，产出也明显好于完全无提示的基线，说明标准及其配套语言本身就在任何评估器反馈发挥作用之前，把模型引离了通用默认值。

一个显著的例子：我提示模型为一个荷兰美术馆做网站。到第九轮迭代，它产出了一个虚构美术馆干净、深色主题的落地页。页面视觉精致，但大体符合我的预期。然后，在第十个循环，它彻底推翻了原有方案，把网站重新想象成一种空间体验：一个以 CSS 透视渲染的棋盘格地板 3D 房间，画作以自由位置挂在墙上，展厅之间靠门洞导航而非滚动或点击。这是我在单次生成中从未见过的创造性跃迁。

[观看视频](https://cdn.sanity.io/files/4zrzovbb/website/9877febd34432f7f582aecd0023b951223605c6a.mp4)

## 扩展到全栈编码

带着这些发现，我把这个 GAN 式模式应用到全栈开发。生成器-评估器循环自然地映射到软件开发生命周期——代码评审与 QA 扮演着与设计评估器相同的结构角色。

### 架构

在我们更早的[长时运行框架](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)中，我们用一个初始化智能体、一个一次做一个功能的编码智能体以及会话间的上下文重置，解决了连贯的多会话编码问题。上下文重置是关键解锁：那个框架用的是 Sonnet 4.5，它表现出前文提到的「上下文焦虑」。打造一个跨上下文重置仍运转良好的框架，是让模型保持在任务上的关键。Opus 4.5 基本上自行消除了这种行为，所以我在这个框架里完全去掉了上下文重置。智能体作为单个连续会话跑完整个构建，上下文增长由 [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) 的自动压缩沿途处理。

在这项工作中，我在原框架的地基上构建了一个三智能体系统，每个智能体针对我在先前运行中观察到的具体缺口。系统包含以下智能体角色：

**规划者（Planner）：** 我们以前的长时运行框架要求用户预先提供详细规格。我想把这一步自动化，于是创建了一个规划者智能体：接一句 1-4 句话的简单提示，扩展成完整的产品规格。我提示它对范围要有雄心，并聚焦于产品语境和高层技术设计，而非细粒度的技术实现。这样强调是出于一个顾虑：如果规划者试图预先规定细粒度技术细节又搞错了，规格中的错误会级联传导到下游实现。约束「要交付什么」、让智能体在工作中自己找路径，似乎更聪明。我还要求规划者寻找把 AI 功能编织进产品规格的机会。（示例见文末附录。）

**生成器（Generator）：** 早先框架的一次一个功能的方式对范围管理很有效。我在这里套用类似模型，指示生成器以冲刺（sprint）方式工作，从规格中一次领取一个功能。每个冲刺以 React、Vite、FastAPI 和 SQLite（后来是 PostgreSQL）的技术栈实现应用，生成器被要求在每个冲刺结束时先自我评估，再交接给 QA。它也有 git 做版本控制。

**评估器（Evaluator）：** 早期框架产出的应用常常看起来惊艳，但真正上手用时仍有实打实的 bug。为了抓住这些，评估器用 Playwright MCP 像用户一样点击运行中的应用，测试 UI 功能、API 端点和数据库状态。然后它对照自己发现的 bug 和一套仿照前端实验设计的标准给每个冲刺打分——这里的标准调整为覆盖产品深度、功能性、视觉设计和代码质量。每条标准都有硬性阈值，任何一条跌破阈值，该冲刺即失败，生成器会收到关于哪里出了问题的详细反馈。

每个冲刺之前，生成器与评估器协商一份冲刺合同：在写任何代码之前，就这部分工作「完成」的定义达成一致。这一设计存在的原因是产品规格有意保持高层，而我们需要一个步骤来弥合用户故事与可测试实现之间的鸿沟。生成器提出要构建什么、以及如何验证成功，评估器审查该提案，确保生成器在造对东西。两者迭代直到达成一致。

通信经由文件进行：一个智能体写文件，另一个读文件并在其中或以新文件回应，前一个再读。生成器然后按照商定的合同构建，再把工作交接给 QA。这既让工作忠于规格，又避免了过早过度规定实现细节。

### 运行框架

这个框架的第一版使用 Claude Opus 4.5，把用户提示同时跑在完整框架和单智能体系统上以作对比。我用 Opus 4.5 是因为在我开始这些实验时它是我们最好的编码模型。

我写了以下提示来生成一个复古游戏制作器：

> *Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode.*

下表显示了框架类型、运行时长和总成本。

| **框架** | **时长** | **成本** |
| --- | --- | --- |
| 单智能体 | 20 分钟 | $9 |
| 完整框架 | 6 小时 | $200 |

完整框架贵了 20 多倍，但输出质量的差异立竿见影。

我期待的是一个这样的界面：构建关卡及其组成部件（精灵、实体、瓦片布局），然后按下播放来真正玩这个关卡。我先打开单智能体运行的产出，初始应用看起来符合这些预期。

然而随着点击深入，问题开始浮现。布局浪费空间，固定高度的面板让视口大半空白。工作流僵硬：想填充关卡时它提示我先创建精灵和实体，但 UI 里没有任何东西引导我按这个顺序操作。更要命的是，游戏本身是坏的。我的实体出现在屏幕上，但对输入毫无响应。翻代码发现实体定义与游戏运行时之间的接线断了，而且表面上完全看不出断在哪里。

打开界面 / 精灵编辑器 / 游戏运行

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F23c98f1d7ae720bfb39190d50e0706c03b177ad8-1999x1320.png&w=3840&q=75)

打开单智能体框架创建的应用时的初始界面。

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F24472c85629a6c82a092f25def4a659042be1f7c-1999x1010.png&w=3840&q=75)

在单智能体框架做的精灵编辑器中创建精灵

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F79217dbfce3f31172eb7fd4deee5449023c9b2ac-1999x757.png&w=3840&q=75)

尝试游玩我创建的关卡，未能成功

评估完单智能体运行后，我转向框架运行的产出。这次运行同样始于那句一句话提示，但规划者步骤把它扩展成横跨十个冲刺的 16 项功能规格。它远远超出了单智能体运行尝试的范围：除核心编辑器和游玩模式外，规格还要求精灵动画系统、行为模板、音效与音乐、AI 辅助的精灵生成器与关卡设计器，以及带分享链接的游戏导出。我让规划者可以读我们的[前端设计技能](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md)，它读了并用其为应用创建了一套视觉设计语言，作为规格的一部分。对每个冲刺，生成器与评估器协商一份合同，定义该冲刺的具体实现细节以及用于验证完成的可测试行为。

这个应用立刻显示出比单智能体运行更多的打磨与顺滑。画布占满整个视口，面板尺寸合理，界面有一致的视觉身份，与规格中的设计方向一致。单智能体运行中的某些笨拙之处仍然存在——工作流仍没说清要先建精灵和实体再填充关卡，我是自己摸索出来的。这更像基础模型产品直觉的缺口，而不是框架本要解决的问题，不过它确实暗示了框架内可以做针对性迭代来进一步提升输出质量的地方。

逐个用过编辑器后，新运行相对单智能体的优势更加明显。精灵编辑器更丰富、功能更全：工具面板更干净、取色器更好、缩放控件更可用。

因为我让规划者把 AI 功能编织进规格，这个应用还内置了 Claude 集成，可以通过提示生成游戏的各个部分。这大大加快了工作流。

打开界面 / 精灵编辑器 / AI 游戏设计 / AI 游戏设计 / 游戏运行

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fa8bef95425966495629095a5cb38bde4a8b13558-1999x997.png&w=3840&q=75)

初始界面：在完整框架构建的应用中创建新游戏

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fc05aa3ef8daaf0ef3d0dba66d6480ab753e9cbaa-1999x1007.png&w=3840&q=75)

精灵编辑器感觉更干净、更好用

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F287b35f4683ecb77ac6a8d66bf2b3ed5956d1db9-1999x1008.png&w=3840&q=75)

用内置 AI 功能生成关卡

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F8596eab2b4a06124df41ad6b2f7ff4ff9d9f105f-1999x1000.png&w=3840&q=75)

用内置 AI 功能生成关卡

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Ff2953550e51957a0a49a3792a0df3bcfed0fde48-1994x1654.png&w=3840&q=75)

玩我生成的游戏

最大的差异在游玩模式。我真的能移动实体、玩这个游戏了。物理还有毛边——我的角色跳上一个平台却最终与它重叠，直觉上不对——但核心功能能用了，而单智能体运行没能做到。四处操作后，我也撞上了一些 AI 关卡构建的局限：有一堵大墙我跳不过去，于是卡住了。这说明框架还有一些常识性改进和边界情况可以处理，把应用打磨得更好。

通读日志可以清楚地看到，评估器让实现与规格保持一致。每个冲刺，它逐条执行冲刺合同的测试标准，通过 Playwright 演练运行中的应用，对任何偏离预期行为的地方提出 bug。合同相当细——仅 Sprint 3 就有 27 条覆盖关卡编辑器的标准——而评估器的发现具体到无需额外调查就能行动。下表列出评估器识别出的几个问题示例：

| **合同标准** | **评估器发现** |
| --- | --- |
| Rectangle fill tool allows click-drag to fill a rectangular area with selected tile | **FAIL** — Tool only places tiles at drag start/end points instead of filling the region. `fillRectangle` function exists but isn't triggered properly on mouseUp. |
| User can select and delete placed entity spawn points | **FAIL** — Delete key handler at `LevelEditor.tsx:892` requires both `selection` and `selectedEntityId` to be set, but clicking an entity only sets `selectedEntityId`. Condition should be `selection || (selectedEntityId && activeLayer === 'entity')`. |
| User can reorder animation frames via API | **FAIL** — `PUT /frames/reorder` route defined after `/{frame_id}` routes. FastAPI matches 'reorder' as a frame_id integer and returns 422: "unable to parse string as an integer." |

让评估器达到这个水平花了功夫。开箱即用的 Claude 是个不合格的 QA 智能体。早期运行中，我看着它识别出正当问题，然后说服自己这些不是大事、照样批准工作。它还倾向于浅层测试，不去探测边界情况，于是更微妙的 bug 常常漏网。调优循环是：读评估器的日志，找到它的判断与我的分歧之处，更新 QA 提示来解决那些问题。经过几轮这样的开发循环，评估器的打分方式才让我觉得合理。即便如此，框架输出仍显示了模型 QA 能力的极限：小的布局问题、某些交互不够直观、以及评估器未充分演练的深层嵌套功能中未发现的 bug。显然还有更多验证空间可以通过进一步调优捕捉。但相比单智能体运行中应用的核心功能根本跑不起来，这个提升是显而易见的。

### 迭代框架

第一轮框架结果令人鼓舞，但它也笨重、缓慢、昂贵。顺理成章的下一步是在不损害性能的前提下简化框架。这一半靠常识，一半源于一个更普遍的原则：框架中的每个组件都编码了一个「模型自己做不到某事」的假设，而这些假设值得压测——既因为它们可能是错的，也因为随着模型进步它们会迅速过时。我们的博客文章[《构建高效智能体》](https://www.anthropic.com/research/building-effective-agents)把底层思想表述为「寻找尽可能简单的方案，只在需要时增加复杂度」，对任何维护智能体框架的人来说，这都是反复出现的模式。

在第一次简化尝试中，我把框架大幅裁剪并试了几个有创意的新想法，但无法复现原版的性能。而且越来越难分辨框架设计里哪些部件真正承重、以何种方式承重。基于那次经验，我转向更有条理的方法：一次只移除一个组件，审视它对最终结果的影响。

在我进行这些迭代循环期间，我们发布了 Opus 4.6，这进一步激励了降低框架复杂度。有充分理由预期 4.6 需要比 4.5 更少的脚手架。正如我们的[发布博客](https://www.anthropic.com/news/claude-opus-4-6)所说：「[Opus 4.6] 规划更周密、能更长时间维持智能体任务、能在更大的代码库中更可靠地运作，并具备更好的代码评审与调试技能来捕捉自身错误。」它在长上下文检索上也大幅改进。这些正是框架当初要补足的能力。

### 移除冲刺结构

我从完全移除冲刺结构开始。冲刺结构曾帮助把工作分解成块，让模型连贯地工作。鉴于 Opus 4.6 的改进，有充分理由相信模型可以原生胜任这项工作，而无需这类分解。

我保留了规划者和评估者，因为两者都持续带来明显的价值。没有规划者，生成器会缩水：拿到原始提示后，它不先规格化就开始构建，最终做出的应用不如规划者版本功能丰富。

冲刺结构移除后，我把评估器改为运行末尾的单一 pass，而不是按冲刺打分。模型强了很多，这改变了评估器在某些运行中的承重程度——其有用性取决于任务相对于模型可靠自治能力所处的位置。在 4.5 上，那条边界很近：我们的构建正处于生成器单干时的能力边缘，评估器在整个构建过程中都能抓到有意义的问题。在 4.6 上，模型的原始能力提升，边界外移。过去需要评估器把关才能连贯实现的任务，现在常常落在生成器自己就能做好的范围内；对这些任务，评估器成了不必要的开销。但对仍在生成器能力边缘的那部分构建，评估器继续带来实打实的提升。

实际启示是：用不用评估器不是一个固定的非黑即白决策。当任务超出当前模型可靠单干的范围时，它值得这个成本。

伴随结构简化，我还添加了提示来改进框架为每个应用构建 AI 功能的方式——特别是让生成器构建一个真正的智能体，能通过工具驱动应用自身的功能。这花了真功夫，因为相关知识足够新，Claude 的训练数据覆盖很薄。但调优足够多轮之后，生成器能正确构建智能体了。

### 更新版框架的结果

为检验更新后的框架，我用以下提示生成了一个数字音频工作站（DAW）——一个用于作曲、录音和混音的音乐制作程序：

> *Build a fully featured DAW in the browser using the Web Audio API.*

运行仍然耗时且昂贵：约 4 小时、124 美元 token 成本。

大部分时间花在构建者身上，它连贯运行了两个多小时，不再需要 Opus 4.5 所需的冲刺分解。

| **智能体与阶段** | **时长** | **成本** |
| --- | --- | --- |
| 规划者 | 4.7 分钟 | $0.46 |
| 构建（第 1 轮） | 2 小时 7 分 | $71.08 |
| QA（第 1 轮） | 8.8 分钟 | $3.24 |
| 构建（第 2 轮） | 1 小时 2 分 | $36.89 |
| QA（第 2 轮） | 6.8 分钟 | $3.09 |
| 构建（第 3 轮） | 10.9 分钟 | $5.88 |
| QA（第 3 轮） | 9.6 分钟 | $4.06 |
| **V2 框架总计** | **3 小时 50 分** | **$124.70** |

与之前的框架一样，规划者把一行提示扩展成完整规格。从日志可以看到，生成器模型在规划应用与智能体设计、接线智能体、并在交接 QA 前测试等方面做得很好。

话虽如此，QA 智能体仍然抓到了真实的缺口。在第一轮反馈中，它指出：

> This is a strong app with excellent design fidelity, solid AI agent, and good backend. The main failure point is Feature Completeness — while the app looks impressive and the AI integration works well, several core DAW features are display-only without interactive depth: clips can't be dragged/moved on the timeline, there are no instrument UI panels (synth knobs, drum pads), and no visual effect editors (EQ curves, compressor meters). These aren't edge cases — they're the core interactions that make a DAW usable, and the spec explicitly calls for them.

第二轮反馈中，它再次抓到几个功能缺口：

> Remaining gaps:  
> - Audio recording is still stub-only (button toggles but no mic capture)  
> - Clip resize by edge drag and clip split not implemented  
> - Effect visualizations are numeric sliders, not graphical (no EQ curve)

放任自流时，生成器仍可能漏细节或把功能做成空壳，而 QA 在抓住这些「最后一英里」问题、交回生成器修复上仍具价值。

根据提示，我期待一个这样的程序：能创作旋律、和声与鼓点，把它们编排成歌，过程中还有一个内置智能体帮忙。下面的视频展示了结果。

[观看视频](https://cdn.sanity.io/files/4zrzovbb/website/555910f9adb3938734940224e7a6f4c7cbbbd8f2.mp4)

这个应用离专业音乐制作程序还很远，智能体的作曲功力显然还需要大量打磨。另外，Claude 实际上听不见，这让 QA 反馈循环在音乐品味方面效果打折。

但最终的应用具备了功能完整的音乐制作程序的全部核心部件：在浏览器中运行的编排视图、混音器和走带控制。更进一步，我完全通过提示拼出了一段短歌：智能体设定速度与调性、铺下旋律、建起鼓轨、调整混音器电平、并加了混响。作曲的核心原语都在，智能体能自主驱动它们，用工具从端到端创作出一个简单的作品。可以说它还不够 pitch-perfect——但正在路上。

## 接下来是什么

随着模型持续改进，大致可以预期它们能工作更长时间、应对更复杂的任务。某些情况下，这意味着围绕模型的脚手架随时间推移变得不那么重要，开发者可以等下一代模型、看某些问题自行消失。另一方面，模型越好，开发能达成超出模型基线能力的复杂任务的框架，空间反而越大。

带着这些想法，这项工作有几条值得带走的经验。用你正在构建所针对的模型做实验、读它在真实问题上的轨迹、并调优其表现以达成你要的结果，永远是好实践。处理更复杂的任务时，有时可以通过分解任务、为问题的每个方面配置专门智能体来换取提升空间。而当新模型落地时，重新审视框架通常也是好实践：剥掉不再承重的部分，加入能实现以前不可能的更强能力的新部件。

从这项工作中，我的信念是：有趣的框架组合空间不会随模型进步而缩小，而是会移动。AI 工程师的有趣工作，就是不断找到下一个新颖组合。

## 致谢

特别感谢 Mike Krieger、Michael Agaby、Justin Young、Jeremy Hadfield、David Hershey、Julius Tarng、Xiaoyi Zhang、Barry Zhang、Orowa Sidker、Michael Tingley、Ibrahim Madha、Martina Long 和 Canyon Robbins 对这项工作的贡献。

也感谢 Jake Eaton、Alyssa Leonard 和 Stef Sequeira 帮助打磨本文。

## 附录

规划者智能体生成的计划示例。

```
RetroForge - 2D Retro Game Maker

Overview
RetroForge is a web-based creative studio for designing and building 2D retro-style video games. It combines the nostalgic charm of classic 8-bit and 16-bit game aesthetics with modern, intuitive editing tools—enabling anyone from hobbyist creators to indie developers to bring their game ideas to life without writing traditional code.

The platform provides four integrated creative modules: a tile-based Level Editor for designing game worlds, a pixel-art Sprite Editor for crafting visual assets, a visual Entity Behavior system for defining game logic, and an instant Playable Test Mode for real-time gameplay testing. By weaving AI assistance throughout (powered by Claude), RetroForge accelerates the creative process—helping users generate sprites, design levels, and configure behaviors through natural language interaction.

RetroForge targets creators who love retro gaming aesthetics but want modern conveniences. Whether recreating the platformers, RPGs, or action games of their childhood, or inventing entirely new experiences within retro constraints, users can prototype rapidly, iterate visually, and share their creations with others.

Features
1. Project Dashboard & Management
The Project Dashboard is the home base for all creative work in RetroForge. Users need a clear, organized way to manage their game projects—creating new ones, returning to works-in-progress, and understanding what each project contains at a glance.

User Stories: As a user, I want to:

- Create a new game project with a name and description, so that I can begin designing my game
- See all my existing projects displayed as visual cards showing the project name, last modified date, and a thumbnail preview, so that I can quickly find and continue my work
- Open any project to enter the full game editor workspace, so that I can work on my game
- Delete projects I no longer need, with a confirmation dialog to prevent accidents, so that I can keep my workspace organized
- Duplicate an existing project as a starting point for a new game, so that I can reuse my previous work

Project Data Model: Each project contains:

Project metadata (name, description, created/modified timestamps)
Canvas settings (resolution: e.g., 256x224, 320x240, or 160x144)
Tile size configuration (8x8, 16x16, or 32x32 pixels)
Color palette selection 
All associated sprites, tilesets, levels, and entity definitions

...
```
