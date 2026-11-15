---
title: "作业 1 — 体验编程智能体（10%）"
title_en: "Assignment 1 — Experience a coding agent(10%)"
source: https://cs2680.seas.harvard.edu/assignments/assignment1.html
crawled: 2026-11-16
translated: 2026-11-16
---

# 作业 1 — 体验编程智能体（10%）

> 原文：[Assignment 1 — Experience a coding agent(10%)](https://cs2680.seas.harvard.edu/assignments/assignment1.html) · Harvard CS2680

CS2680 现代 AI 系统：智能体与系统优化（CS2680 Modern AI Systems: Agents and System Optimizations）

作业 1 — 体验编程智能体

# 作业 1 — 体验编程智能体（10%）

**发布** 9 月 2 日（周三） · **截止** 9 月 20 日（周日）晚 11:59 · 个人作业 ·
[全部五份作业](index.html)

构建一个驱动 [Claude Code](../computing/claude-code.html) 的网页：你输入请求，智能体在你选择的目录上工作，页面在它工作的同时向你展示它在做什么。

这份作业刻意做得很小，也是后续课程中唯一不作为衡量基准的作业。在你自己的机器上提供服务就足够了。这是一项创造性任务。第 2 部分规定了页面必须做什么；页面长什么样、如何工作由你设计，而那些有意思的决策（进行中的运行应当是什么样子、一次工具调用的结果要展示多少、一次失败应当如何呈现）恰恰是规格留给你决定的部分。

五份作业都通过一个与助教共享的私有 GitHub 仓库提交代码；这份作业放在其中的 `assignment1/` 目录。参见[交付物](#deliverables)。

**也用 Claude Code 来构建前端。** 这是获得一个可用页面的最快方式，而且观察智能体构建它的过程，会教你页面应当展示什么。

## 学习目标

* 使用 Claude Code 构建可运行的软件。
* 以编程方式（headless 模式及其事件流）驱动智能体，而不只是交互式使用。
* 实时观察轨迹：智能体读取了什么、运行了什么，以及这些操作花费了多少。

## 第 1 部分 — 从终端驱动 Claude Code

**Headless 模式。** 使用 `-p` 调用时，Claude Code 以非交互方式运行；配合 `--output-format stream-json`，它会在运行过程中每行打印一个 JSON 事件（在 print 模式下，该输出格式还需要 `--verbose`）。事件流首先是一个 init 事件，然后是 assistant 消息、工具调用及其结果，最后是一个携带 `total_cost_usd`、`duration_ms`、`num_turns` 和 `session_id` 的最终 result 事件。下面是一次最小运行，事件已裁剪到其关键字段：

```
$ claude -p "Say hello in one short sentence." --output-format stream-json --verbose
{"type":"system","subtype":"init","session_id":"fe891e8a-…","cwd":"…","model":"…","tools":[…],…}
{"type":"assistant","message":{"role":"assistant","content":[{"type":"text","text":"Hello! How can I help you today?"}],…},…}
{"type":"result","subtype":"success","num_turns":1,"duration_ms":4333,"total_cost_usd":0.137852,"session_id":"fe891e8a-…",…}
```

让智能体真正干活的提示词（例如“读取 main.py 并添加一个 `--help` 标志”）会穿插更多内容为 `tool_use` 块的 assistant 事件，以及携带匹配 `tool_result` 的 user 事件；这些正是你的页面要渲染的内容。把 result 事件中的 session id 传回去（`claude -p --resume <session-id> "<follow-up>" …`）即可继续对话。参见 [headless 模式文档](https://code.claude.com/docs/en/headless)。

在编写任何 Web 代码之前，先在一个临时目录上从终端运行它，并阅读它打印的事件，因为你在第 2 部分构建的前端正是这个事件流的渲染器。然后保存一次完整运行到文件（`claude -p "<prompt>" --output-format stream-json --verbose > events.jsonl`）；它将成为你在第 2 部分的测试输入。

**开启自动接受，以免运行被权限提示中断。** 默认情况下，Claude Code 在编辑文件或运行命令前会询问。在交互式会话中，按 Shift+Tab 切换到自动接受模式。在 headless 运行中没有人可以询问，因此需要批准的请求会被拒绝：用 `--dangerously-skip-permissions` 启动运行以自动批准一切（针对临时目录这是正确的选择），或用 `--allowedTools`（例如 `--allowedTools "Edit" "Bash(pytest:*)"`）只自动批准指定的工具，并在第 2 部分的服务器启动智能体时传入同样的标志。

**使用哈佛登录认证，不要使用 Agent SDK 或 API key。** headless 模式读取与交互式 Claude Code 相同的已存储凭据，因此你已有的[哈佛登录](../computing/claude-code.html)就是全部配置。Agent SDK 在这里不是合适的工具，原因有二。第一，Anthropic 的[使用政策](https://code.claude.com/docs/en/legal-and-compliance)要求 SDK 使用 Claude Console 的 API key，而课程不提供这些 key。第二，导出的 `ANTHROPIC_API_KEY` 优先级高于你的哈佛登录，因此设置它会在不知不觉中记到你自己的账户上。

## 第 2 部分 — 前端

现在给你刚刚运行的内容加上一个网页：你的服务器将第 1 部分的命令作为子进程启动，将其事件转发到浏览器，并保留 session id，以便后续提示词可以恢复会话。页面需要七项功能。每项功能都以“页面必须做什么”的形式陈述；如何实现由你决定。每项功能下方的草图展示了它所需的行为，而不是你必须照搬的设计。

1. **提交提示词。** 一个文本框将你的请求发送给 Claude Code，后者在你选择的工作目录上运行，页面可以在第一次运行结束后启动另一次运行。

   工作目录

   ~/scratch/demo-repo

   find the bug that makes test\_parse fail and fix it

   运行
2. **实时展示轨迹。** 轨迹就是智能体做过的事，逐个事件呈现：assistant 的文本，以及每一次工具调用的名称和输入（读取 `parser.py`、运行 `pytest`、编辑文件）。每个事件到达时就渲染，而不是等运行结束后再渲染。assistant 的文本通常是 Markdown，因此要按格式渲染，而不是显示原始标记。

   进行中
   The test expects a trailing newline. I will read the parser first.

   Read
   tests/test\_parse.py
   ✓

   Bash
   pytest -x
   ✓

   Edit
   src/parser.py

   等待中
3. **展示工具结果。** 每个工具调用的结果随调用一起出现，较长的结果要刻意裁剪（测试日志可能有数千行，而一个被日志淹没的页面就没人会读）。展示多少、如何折叠其余部分，是你应当做出的设计决策。

   Bash
   pytest -x
   ✓

   FAILED tests/test\_parse.py::test\_parse
   ValueError: unexpected token ')'
   ▸ 87 more lines, folded
4. **展示状态，既按工具调用也按运行。** 状态存在于两个层次，页面要像 Claude Code 终端那样把两者都展示出来。(1) 按工具调用：从 `tool_use` 块到达的那一刻起，直到匹配的 `tool_result` 附加为止（两者共享该调用的 id），调用都处于等待状态；报告错误的结果要能明显看出是错误。(2) 按运行：智能体自主工作，直到最终 result 事件结束本轮，因此要显示运行是进行中、已完成还是失败；失败的运行（错误的目录、智能体错误）要产生可见的错误，而不是让页面永远等待。

   运行期间 · 按工具调用

   Bash
   pytest -x
   ✓

   Edit
   src/parser.py

   等待中

   本轮结束 · 按运行
   All 12 tests pass.
   ✓ 已完成

   一次失败的运行

   你
   start a run in /bad/path
   ✕ 失败

   Error: /bad/path is not a directory (exit 1)
5. **继续对话。** 后续提示词恢复同一个会话，因此智能体保留上一轮的上下文。

   你
   add a --json flag to the CLI
   ▸ 23 events, folded
   Added the --json flag and updated the tests.
   ✓ 已完成
   $0.58 · 42 s · 12 turns · session\_id fe891e8a-…

   你
   now update the README for it

   进行中
   resumed session fe891e8a-…
6. **展示运行的各项数字。** 运行结束时，显示其美元成本、实际耗时和轮次数。Claude Code 会在最终 result 事件中报告这三项，因此这是一个展示功能，而不是测量练习。

   Added the --json flag and updated the tests.
   ✓ 已完成
   $0.58 · 42 s · 12 turns · session\_id fe891e8a-…
7. **将轨迹展示为树。** 你在功能 2 中渲染的事件序列并不总是扁平的：Claude Code 可以把工作委派给子智能体，子智能体发出的每个事件都携带一个 `parent_tool_use_id`，指向派生它的那次工具调用（来自主智能体的事件在该字段上为 `null`）。将每个子智能体的事件嵌套到对应的工具调用之下，并支持折叠，以免一次长时间的子智能体运行淹没主智能体的事件；没有子智能体的运行仍按功能 2 的扁平列表渲染。此外，在对话旁边展示整个轨迹的大纲，只列调用名称，像目录一样，让读者可以纵览整个运行并跳转到某次调用。只要窗口足够宽，大纲就显示在对话旁边，而不是作为固定在页面顶部的条带；在窄窗口上可以折叠收起。除这两种视图外，欢迎你设计更好的轨迹可视化。子智能体只在运行时才会出现，因此请用一个要求使用子智能体的提示词来演示（例如“使用一个子智能体勘察这个目录”）。

   Bash
   pytest -x
   ✓

   任务

   Task
   survey this directory

   Read
   src/parser.py
   ✓

   Grep
   "TODO"
   ✓
   A small parser package with one failing test.

   Task
   summarize the README
   · 4 events collapsed

   Edit
   src/parser.py
   ✓

   大纲

   Bash

   Task

   Task

   Read

   Grep

   Edit

**把七项功能合起来，就是一个页面。** 下方草图展示了一种可能的整体效果：第一次运行已完成并显示各项数字，第二次运行从同一会话恢复且仍在进行中，一个工具结果已展开并被折叠，一个子智能体嵌套在其 Task 调用之下。它展示的是行为，而不是你必须照搬的设计。

大纲

Read

Read

Grep

Edit

Bash

Read

Edit

Bash

Edit

Bash

Bash

你

Read

Task

Task

Read

Glob

Grep

Read

Edit
工作目录

~/scratch/demo-repo

你
add a --json flag to the CLI
▸ 23 events, folded
Added the --json flag and updated the tests.
✓ 已完成
$0.58 · 42 s · 12 turns · session\_id fe891e8a-…

你
use subagents to survey the repo, then update the README

进行中
resumed session fe891e8a-…
I will run two surveys, then edit the README.

Read
README.md
✓

# demo-cli
A small CLI for parsing logs.
▸ 34 more lines, folded

任务

Task
survey the code

Read
src/cli.py
✓

Grep
"--json"
✓
cli.py implements --json.

Task
survey the docs
· 5 events collapsed

Edit
README.md

等待中

输入后续消息…

运行

**尝试超出必需功能去改进。** 智能体通常只做刚好满足你提示词期望的最小工作，因此你前端的第一个可用版本很可能并不好用。这七项功能只是基本要求，但你可以更有创造力：让页面更直观、让你要找的东西更容易找到、让进行中的运行更容易跟进。自己使用这个页面，注意它在哪些地方让你恼火，然后修掉它。这份作业的许多乐趣在于看着你的前端随着每一次改动越来越友好，书面报告的第一节就要求你说明自己所做的改进。

**给智能体一些可做的工作。** 你的页面驱动 Claude Code 在一个工作目录上工作，而在空目录上演示看不到任何值得看的东西，因此请为智能体准备一个小型真实代码库（最简单的是与前端自己的仓库分开）。任何有几个文件和一套测试的项目都可以：一个旧的课程项目、一个你在使用的小型开源工具，或你正在构建的前端本身的一个副本。演示效果好的任务是具体且多步骤的（“找出让 `test_parse` 失败的 bug 并修复它”、“添加一个 `--json` 标志并更新 README”），因为它们让智能体读取、运行和编辑，而这正是功能 2 和功能 3 所展示的内容。

**通过重放录制的流来高效测试。** 针对保存的 `events.jsonl` 开发渲染逻辑，给服务器加一个重放模式，从文件读取而不是启动智能体。实时运行需要一分钟甚至更久，并消耗真实用量，而重放录制的流瞬间完成且免费，这就是十秒编辑-测试循环与一分钟循环的差别。最后再用实时运行测试，因为有两件事只有实时运行才能验证：事件必须在*到达时*渲染，而不是在运行结束后；会话恢复需要真实的 session id。对于树视图，请再保存一份来自派生子智能体运行的 `events.jsonl`，这样树视图的渲染也能在重放中开发。

任何语言、任何 Web 技术栈都可以。但是，不要使用智能体框架，也不要重新实现智能体循环（那是作业 2）。

**在哪里运行。** 你自己的机器就足够了，评分不要求公开 URL。如果你希望页面能从其他设备访问，[CloudLab](../computing/cloudlab.html) 或 AWS 机器也可以；这种情况下要在前面加一个随机访问令牌（例如 `openssl rand -hex 16`，不要放进仓库），并拒绝所有不带该令牌的请求，因为这里的公开页面相当于一个远程控制入口，可以在那台机器上读取文件并运行命令。无论哪种方式，都要让智能体指向一个临时目录而不是你的主目录：你的页面、截图和演示会展示它读取的一切。如果你在自己的笔记本电脑上配置遇到困难，欢迎联系助教寻求帮助。

## 第 3 部分 — 书面报告

Markdown 或 PDF，以 `assignment1/writeup.md` 或 `assignment1/writeup.pdf` 提交到仓库。不限页数，但不要凑篇幅：一份能清楚说明每一点的简短报告就足够了。**请自己撰写文字。** 书面报告记录你观察和学到了什么，因此完全由 AI 生成的报告会背离这一目的，并会被扣分。报告包含三个部分：

1. **你构建了什么。** 用一段话和一张截图说明前端的功能，并列出你在七项必需功能之外所做的改进；可以用项目符号列表，如果列表太长也可以融入段落。
2. **你学到了什么。** 需要三项观察，每项都对应会话中的某个具体时刻。(1) 智能体如何工作：它在哪些地方花的时间比你预期多、它读取了哪些你不会读的内容，或它处理任务的方式与你有什么不同。(2) 一个陷阱：出了什么问题或让你意外，你如何察觉，以及你会提醒同学注意什么。(3) 一条经验：下次使用智能体时你会有什么不同做法，你会如何更好地提示、界定范围或监督它，以及会话中的什么让你学到了这一点。除这三项之外，欢迎补充更多：洞见，或你沿途掌握的新工具、技能和插件。
3. **你会改变的一件事。** 如果你能改变 Claude Code 工作方式的一件事（不是你的前端），那会是什么，你看到了什么让你想要这个改变？

## 如果你想做更多

以下内容都不是必需或计分的，但每一项都是你刚构建的工具的真实功能，而喜欢这份作业的学生往往整个学期都在使用自己的前端：一个取消运行中智能体的停止按钮、权限提示的批准/拒绝按钮、智能体所改文件的差异视图，以及多个会话在并行标签页中运行。

## 交付物

一个仓库服务整门课程：五份作业都通过同一个**私有 GitHub 仓库**提交代码、书面报告和会话文件，仅与授课教师和助教共享，不与他人共享。只有演示视频上传到 Canvas。仓库创建一次，将这份作业放在 `assignment1/` 目录，后续作业依次放在 `assignment2/`、`assignment3/` 等目录。邀请授课教师和四位助教，GitHub 用户名分别为 [`1a1a11a`](https://github.com/1a1a11a)、[`LauYeeYu`](https://github.com/LauYeeYu)、[`SeverinaZheng`](https://github.com/SeverinaZheng)、[`G6KlayWang`](https://github.com/G6KlayWang) 和 [`AdvaithRavishankar`](https://github.com/AdvaithRavishankar)。

1. 你的**代码**，位于共享仓库的 `assignment1/` 中，并附一个说明如何启动服务器的 README。
2. **书面报告**，位于仓库中的 `assignment1/writeup.md` 或 `assignment1/writeup.pdf`。
3. 一段**演示视频**（2–3 分钟），上传到 Canvas，展示前端处理一个真实的多轮任务，并且智能体的工具调用在工作时可见地流式输出。视频必须展示全部七项功能，包括一次失败的运行和一次派生子智能体的运行。此外，你可以报名在 9 月 21 日的分享会上现场展示前端（报名链接将在 Canvas 上发布）。现场展示是可选的，依据[展示反馈标准](../discussion.html#presentation-feedback)最多可获得 4 个加分百分点。
4. 你的 **Claude Code 会话文件**，按[每份作业需提交的内容](../computing/claude-code.html#export)所述归档，并提交到仓库的 `assignment1/`。检查你的 `.gitignore` 没有排除该归档。与每份作业一样，它们不单独计分；它们是书面报告各项主张背后的记录。

## 评分

| 权重 | 组成部分 |
| --- | --- |
| **70%** | 七项必需功能，每项 10%，根据你的演示视频评为可用 / 部分可用 / 缺失，仓库作为佐证 |
| **20%** | 书面报告：第 2 节占主要部分，具体且锚定会话的观察才能得分，泛泛的赞美不能 |
| **10%** | 视觉设计：布局与可读性 |

## 功能

根据你的演示视频评判：下列行为各占 10%，部分实现得部分分，从未演示得零分。

| 功能 | 满分标准 |
| --- | --- |
| **提交提示词** | 从页面提交会在你选择的工作目录上启动一次运行，第一次运行结束后可以从同一页面启动第二次运行。 |
| **实时展示轨迹** | assistant 文本和每一次工具调用（名称与输入）在*运行进行期间*按顺序出现，assistant 文本中的 Markdown 按格式渲染，而不是原始标记。 |
| **展示工具结果** | 每次工具调用的结果随调用一起可见，长输出被刻意裁剪或折叠，使页面保持可读。 |
| **展示状态，既按工具调用也按运行** | 工具调用在其结果到达前明显处于等待状态，结果报告错误时明显显示为错误；运行的进行中、已完成和失败状态可区分；演示中展示一次失败的运行（例如错误的工作目录）产生可见错误。 |
| **继续对话** | 后续提示词恢复同一会话，演示中展示延续的上下文（例如一个只有结合上一轮才说得通的后续问题被正确回答）。 |
| **展示运行的各项数字** | 每次完成的运行都显示来自 result 事件的美元成本、实际耗时和轮次数。 |
| **将轨迹展示为树** | 派生子智能体的运行显示哪些事件属于哪个子智能体（嵌套在派生调用之下，或采用你自己设计的等效可视化）；宽窗口下，仅含调用名称的大纲位于对话旁边；长时间的子智能体运行可以折叠；没有子智能体的运行仍能正确渲染。 |

[作业 2 — 构建智能体 harness →](assignment2.html)
