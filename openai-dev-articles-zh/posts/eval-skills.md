---
title: "用评测（Evals）系统性地测试智能体 Skills"
title_en: "Testing Agent Skills Systematically with Evals"
source: https://developers.openai.com/blog/eval-skills/
crawled: 2026-09-14
translated: 2026-09-14
---

# 用评测（Evals）系统性地测试智能体 Skills

> 原文：[Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills/) · OpenAI 开发者博客

当你在为 Codex 这样的智能体迭代一个 skill 时，很难分辨你是在真正改进它，还是仅仅改变了它的行为。某个版本感觉更快，另一个似乎更可靠，然后一个回退悄悄混了进来：skill 不触发了，它跳过了某个必要步骤，或者它留下了多余的文件。

从本质上说，skill 是面向 LLM 的一份[有条理的提示词与指令集合](https://developers.openai.com/codex/skills)。要让一个 skill 持续改进，最可靠的方式是像对待 [LLM 应用的其他任何提示词](https://platform.openai.com/docs/guides/evaluation-best-practices)一样对它进行评测。

*评测（Evals）*（*evaluations* 的简称）检查模型的输出，以及产生该输出的步骤，是否符合你的意图。与其问「这个是不是感觉更好？」（或凭感觉行事），evals 让你能提出具体的问题，例如：

- 智能体是否调用了这个 skill？
- 它是否运行了预期的命令？
- 它产出的输出是否遵循了你在意的约定？

具体来说，一次 eval 就是：一个提示词 → 一次被记录下来的运行（trace + 产物）→ 一小组检查项 → 一个可以随时间比较的分数。

在实践中，针对智能体 skill 的 evals 看起来非常像轻量的端到端测试：你运行智能体，记录发生了什么，然后按照一小组规则给结果打分。

本文通过 Codex 演示这一过程的一个清晰模式：从定义成功开始，然后加入确定性检查与基于评分细则（rubric）的打分，让改进（和回退）都清晰可见。

## **1. 在写 skill 之前先定义成功**

在动手写 skill 之前，先写下「成功」意味着什么，用你真正能够度量的术语来表述。一个有用的思考方式是把检查项分成几类：

- **结果目标：** 任务完成了吗？应用能跑起来吗？
- **过程目标：** Codex 是否调用了这个 skill，并遵循了你预期的工具与步骤？
- **风格目标：** 输出是否遵循了你要求的约定？
- **效率目标：** 它是否在没有空转的情况下达成目标（例如，没有不必要的命令或过度的 token 消耗）？

保持这份清单短小，聚焦于必须通过的检查。目标不是预先编码每一条偏好，而是捕获你最关心的行为。

例如在本文中，指南评测的是一个搭建演示应用的 skill。有些检查是具体的：它运行 `npm install` 了吗？它创建了 `package.json` 吗？指南还把这些检查与一份结构化的风格评分细则（rubric）搭配，用来评估约定与布局。

这种组合是有意为之。你要的是快速、有针对性的信号，能尽早暴露具体的回退，而不是最后给出一个笼统的通过/不通过判定。

## **2. 创建 skill**

Codex skill 是一个包含 `SKILL.md` 文件的目录，该文件带有 YAML front matter（`name`、`description`），随后是定义 skill 行为的 Markdown 指令，以及可选的资源与脚本。名称与描述的重要性超出表面所见：它们是 Codex 用来决定*是否*调用这个 skill、以及*何时*把 `SKILL.md` 其余部分注入智能体上下文的主要信号。如果这些内容含糊或臃肿，skill 就无法可靠地触发。

最快的上手方式是使用 Codex 内置的 skill 创建器（[它本身也是一个 skill](https://github.com/openai/skills/tree/main/skills/.system/skill-creator)）。它会引导你完成：

```
$skill-creator
```

创建器会询问你这个 skill 做什么、何时触发，以及它是纯指令型还是脚本支撑型（默认推荐纯指令型）。要了解更多关于创建 skill 的内容，请[查阅文档](https://developers.openai.com/codex/skills#create-a-skill)。

### **一个示例 skill**

本文使用一个刻意保持极简的例子：一个以可预期、可复现的方式搭建小型 React 演示应用的 skill。

这个 skill 将会：

- 使用 Vite 的 React + TypeScript 模板搭建项目骨架
- 使用官方 Vite 插件方式配置 Tailwind CSS
- 强制执行一个极简且一致的文件结构
- 定义清晰的「完成定义（definition of done）」，让成功与否一目了然、易于评测

下面是一份精简的草稿，你可以把它粘贴到：

- `.codex/skills/setup-demo-app/SKILL.md`（仓库级），或
- `~/.codex/skills/setup-demo-app/SKILL.md`（用户级）。

```
---
name: setup-demo-app
description: Scaffold a Vite + React + Tailwind demo app with a small, consistent project structure.
---

## When to use this

Use when you need a fresh demo app for quick UI experiments or reproductions.

## What to build

Create a Vite React TypeScript app and configure Tailwind. Keep it minimal.

Project structure after setup:

- src/
  - main.tsx (entry)
  - App.tsx (root UI)
  - components/
    - Header.tsx
    - Card.tsx
  - index.css (Tailwind import)
- index.html
- package.json

Style requirements:

- TypeScript components
- Functional components only
- Tailwind classes for styling (no CSS modules)
- No extra UI libraries

## Steps

1. Scaffold with Vite using the React TS template:
   npm create vite@latest demo-app -- --template react-ts

2. Install dependencies:
   cd demo-app
   npm install

3. Install and configure Tailwind using the Vite plugin.
   - npm install tailwindcss @tailwindcss/vite
   - Add the tailwind plugin to vite.config.ts
   - In src/index.css, replace contents with:
     @import "tailwindcss";

4. Implement the minimal UI:
   - Header: app title and short subtitle
   - Card: reusable card container
   - App: render Header + 2 Cards with placeholder text

## Definition of done

- npm run dev starts successfully
- package.json exists
- src/components/Header.tsx and src/components/Card.tsx exist
```

这个示例 skill 特意采取了有主见的立场。没有明确的约束，就没有任何具体的东西可供评测。

## **3. 手动触发 skill，暴露隐藏的假设**

由于 skill 的调用非常依赖 `SKILL.md` 中的*名称*与*描述*，第一件要检查的事就是：`setup-demo-app` skill 是否在你预期它触发的时候触发。

在早期，请在一个真实仓库或临时目录中显式激活这个 skill——通过 `/skills` 斜杠命令，或用 `$` 前缀引用它——然后观察它在哪里出问题。正是在这里你会发现各种失误：skill 完全不触发的情况、触发得过于积极的情况，或者虽然运行却偏离预期步骤的情况。

在这个阶段，你不是在优化速度或打磨细节。你是在寻找这个 skill 正在做出的隐藏假设，例如：

- **触发假设：** 像「搭一个快速 React 演示」这样*应该*调用 `setup-demo-app` 却没有调用的提示词，或者更宽泛的提示词（「加一点 Tailwind 样式」）意外触发了它。
- **环境假设：** skill 假定自己运行在空目录中，或假定 `npm` 可用且优于其他包管理器。
- **执行假设：** 智能体假定依赖已安装而跳过 `npm install`，或在 Vite 项目尚未存在时就配置 Tailwind。

当你准备好让这些运行变得可复现时，切换到 `codex exec`。它是为自动化与 CI 设计的：它把进度流式输出到 `stderr`，只把最终结果写入 `stdout`，这让运行更容易被脚本化、捕获与检查。

默认情况下，`codex exec` 在受限沙箱中运行。如果你的任务需要写文件，请用 `--full-auto` 运行。作为一般原则，尤其是在自动化场景中，请使用完成任务所需的最小权限。

一次基本的手动运行可能如下：

```
codex exec --full-auto \
  'Use the $setup-demo-app skill to create the project in this directory.'
```

这第一轮动手操作与其说是验证正确性，不如说是发现边界情况。你在这里做的每一次手动修正——比如补上缺失的 `npm install`、修正 Tailwind 配置，或收紧触发描述——都是未来某条 eval 的候选，这样你就能在大规模评测之前锁定预期行为。

## **4. 用一小组有针对性的提示词尽早捕获回退**

你不需要一个大型基准测试就能从 evals 中获得价值。对于单个 skill，一组 10–20 条的小提示词集就足以尽早暴露回退并确认改进。

从一个小的 CSV 开始，随着你在开发或使用中遇到真实失败而逐步扩充。每一行应当代表一种你在乎 `setup-demo-app` skill *会*还是*不会*激活的情境，以及它激活时成功是什么样子。

例如，最初的 `evals/setup-demo-app.prompts.csv` 可能是这样的：

```
id,should_trigger,prompt
test-01,true,"Create a demo app named `devday-demo` using the $setup-demo-app skill"
test-02,true,"Set up a minimal React demo app with Tailwind for quick UI experiments"
test-03,true,"Create a small demo app to showcase the Responses API"
test-04,false,"Add Tailwind styling to my existing React app"
```

这些用例各自测试的东西略有不同：

- **显式调用（`test-01`）**

  这条提示词直接点名了 skill。它确保 Codex 在被要求时能够调用 `setup-demo-app`，并且对 skill 名称、描述或指令的修改不会破坏直接用法。
- **隐式调用（`test-02`）**

  这条提示词*精确*描述了这个 skill 所针对的场景——搭建一个极简的 React + Tailwind 演示——但没有点名这个 skill。它测试 `SKILL.md` 中的名称与描述是否足够强，让 Codex 能自行选中这个 skill。
- **情境化调用（`test-03`）**

  这条提示词加入了领域上下文（Responses API），但仍然需要同样的底层搭建。它检查 skill 是否能在现实、略有噪音的提示词中触发，以及产出的应用是否仍符合预期的结构与约定。
- **阴性对照（`test-04`）**

  这条提示词**不应**调用 `setup-demo-app`。它是一个常见的相邻请求（「给我现有的应用加 Tailwind」），却可能意外匹配这个 skill 的描述（「React + Tailwind 演示」）。至少包含一条 `should_trigger=false` 的用例，有助于捕获**假阳性**——Codex 过于急切地选中了这个 skill，在用户只想对现有应用做增量修改时却新建了一个项目。

这种组合是有意为之。有些 evals 应确认 skill 在被显式调用时行为正确；另一些则应检查它在用户完全没有提及 skill 的真实提示词中能否激活。

当你发现失误——未能触发 skill 的提示词，或输出偏离你预期的情形——就把它们作为新行加进去。假以时日，这份小小的 CSV 就会成为一份「活的」记录，记下 `setup-demo-app` skill 必须持续做对的那些场景。

随着时间推移，这份数据集会成为一份「活的」记录，记下这个 skill 必须持续做对的事情。

## **5. 从轻量的确定性评分器开始**

这是评测步骤的核心：使用 `codex exec --json`，让你的 eval 执行框架（harness）能够对*实际发生了什么*打分，而不只是看最终输出看起来对不对。

启用 `--json` 后，`stdout` 会变成结构化事件的 JSONL 流。这让编写与你在意的行为直接挂钩的确定性检查变得非常直接，例如：

- 它运行 `npm install` 了吗？
- 它创建 `package.json` 了吗？
- 它是否按预期顺序调用了预期的命令？

这些检查刻意保持轻量。在加入任何基于模型的打分之前，它们为你提供快速、可解释的信号。

### **一个极简的 Node.js 运行器**

一个「足够好」的做法如下：

1. 对每条提示词，运行 `codex exec --json --full-auto "<prompt>"`
2. 把 JSONL trace 保存到磁盘
3. 解析 trace，并对事件运行确定性检查

```
// evals/run-setup-demo-app-evals.mjs
import { spawnSync } from "node:child_process";
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import path from "node:path";

function runCodex(prompt, outJsonlPath) {
  const res = spawnSync(
    "codex",
    [
      "exec",
      "--json", // REQUIRED: emit structured events
      "--full-auto", // Allow file system changes
      prompt,
    ],
    { encoding: "utf8" }
  );

  mkdirSync(path.dirname(outJsonlPath), { recursive: true });

  // stdout is JSONL when --json is enabled
  writeFileSync(outJsonlPath, res.stdout, "utf8");

  return { exitCode: res.status ?? 1, stderr: res.stderr };
}

function parseJsonl(jsonlText) {
  return jsonlText
    .split("\n")
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

// deterministic check: did the agent run `npm install`?
function checkRanNpmInstall(events) {
  return events.some(
    (e) =>
      (e.type === "item.started" || e.type === "item.completed") &&
      e.item?.type === "command_execution" &&
      typeof e.item?.command === "string" &&
      e.item.command.includes("npm install")
  );
}

// deterministic check: did `package.json` get created?
function checkPackageJsonExists(projectDir) {
  return existsSync(path.join(projectDir, "package.json"));
}

// Example single-case run
const projectDir = process.cwd();
const tracePath = path.join(projectDir, "evals", "artifacts", "test-01.jsonl");

const prompt =
  "Create a demo app named demo-app using the $setup-demo-app skill";

runCodex(prompt, tracePath);

const events = parseJsonl(readFileSync(tracePath, "utf8"));

console.log({
  ranNpmInstall: checkRanNpmInstall(events),
  hasPackageJson: checkPackageJsonExists(path.join(projectDir, "demo-app")),
});
```

这里的价值在于：一切都是**确定且可调试的**。

如果某个检查失败，你可以打开 JSONL 文件，确切看到发生了什么。每一次命令执行都会按顺序以 `item.*` 事件的形式出现。这让回退变得容易解释与修复，而这正是这个阶段你想要的东西。

## **6. 用 Codex 与基于评分细则的打分进行定性检查**

确定性检查回答的是*「它把基本的事做了吗？」*，但回答不了*「它是以你想要的方式做的吗？」*

对于像 `setup-demo-app` 这样的 skill，许多要求是定性的：组件结构、样式约定，或者 Tailwind 是否遵循了预期的配置。这些很难仅靠基础的文件存在性检查或命令计数来捕获。

一个务实的解决方案是在 eval 流水线中加入第二个由模型辅助的步骤：

1. 运行搭建 skill（这一步会把代码写到磁盘上）
2. 对产出的仓库运行一次**只读的风格检查**
3. 要求一个**结构化响应**，让你的执行框架能够一致地打分

Codex 通过 `--output-schema` 直接支持这一点，它会把最终响应约束为你定义的 JSON Schema。

### **一个小巧的评分细则 schema**

先定义一个小巧的 schema，捕获你在意的检查项。例如，创建 `evals/style-rubric.schema.json`：

```
{
  "type": "object",
  "properties": {
    "overall_pass": { "type": "boolean" },
    "score": { "type": "integer", "minimum": 0, "maximum": 100 },
    "checks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "pass": { "type": "boolean" },
          "notes": { "type": "string" }
        },
        "required": ["id", "pass", "notes"],
        "additionalProperties": false
      }
    }
  },
  "required": ["overall_pass", "score", "checks"],
  "additionalProperties": false
}
```

这个 schema 为你提供了稳定的字段（`overall_pass`、`score`、逐项检查结果），你可以对它们进行组合、差异比较与长期跟踪。

### **风格检查提示词**

接下来，运行第二个 `codex exec`，它*只检查仓库*并输出符合评分细则的 JSON 响应：

```
codex exec \
  "Evaluate the demo-app repository against these requirements:
   - Vite + React + TypeScript project exists
   - Tailwind is configured via @tailwindcss/vite and CSS imports tailwindcss
   - src/components contains Header.tsx and Card.tsx
   - Components are functional and styled with Tailwind utility classes (no CSS modules)
   Return a rubric result as JSON with check ids: vite, tailwind, structure, style." \
  --output-schema ./evals/style-rubric.schema.json \
  -o ./evals/artifacts/test-01.style.json
```

这正是 `--output-schema` 顺手的地方。你得到的不再是难以解析或比较的自由格式文本，而是一个可预期的 JSON 对象，你的 eval 执行框架可以在多次运行之间一致地打分。

如果你之后把这个 eval 套件搬进 CI，Codex GitHub Action 明确支持通过 `codex-args` 传入 `--output-schema`，因此你可以在自动化工作流中强制同样的结构化输出。

## **7. 随着 skill 成熟扩展你的 evals**

一旦核心循环就位，你就可以在对你的 skill 最重要的方向上扩展 evals。从小处开始，只在哪里能带来真正的信心，就在哪里叠加更深入的检查。

一些例子包括：

- **命令计数与空转检测：** 统计 JSONL trace 中的 `command_execution` 项，捕获智能体开始循环或重复运行命令的回退。token 用量也可以从 `turn.completed` 事件中获取。
- **token 预算：** 跟踪 `usage.input_tokens` 与 `usage.output_tokens`，发现意外的提示词膨胀，并比较不同版本之间的效率。
- **构建检查：** 在 skill 完成后运行 `npm run build`。这是一个更强的端到端信号，能捕获损坏的导入或配置错误的工具链。
- **运行时冒烟检查：** 启动 `npm run dev` 并用 `curl` 访问开发服务器，或者如果你已有轻量的 Playwright 检查就运行它。要有选择地使用：它增加信心，但也花费时间。
- **仓库整洁度：** 确保运行没有生成多余的文件，且 `git status --porcelain` 为空（或匹配一个明确的允许清单）。
- **沙箱与权限回退：** 验证 skill 在不把权限提升到超出你预期范围的情况下仍然可用。一旦你开始自动化，最小权限默认值就最为重要。

模式是一致的：从能解释行为的快速检查开始，只在能降低风险时才加入更慢、更重的检查。

## **8. 核心要点**

这个小小的 `setup-demo-app` 例子展示了从「感觉更好」到「拿出证据」的转变：运行智能体，记录发生了什么，然后用一小组检查给它打分。一旦这个循环建立起来，每一次调整都更容易确认，每一次回退都清晰可见。以下是核心要点：

- **度量真正重要的东西。** 好的 evals 让回退清晰、失败可解释。
- **从可检查的完成定义出发。** 用 `$skill-creator` 起步，然后不断收紧指令，直到成功的标准毫无歧义。
- **让 evals 立足于行为。** 用 `codex exec --json` 捕获 JSONL，并针对 `command_execution` 事件编写确定性检查。
- **在规则力所不及处使用 Codex。** 用 `--output-schema` 加入一轮结构化、基于评分细则的检查，可靠地为风格与约定打分。
- **让真实失败驱动覆盖面。** 每一次手动修正都是一个信号。把它变成一条测试，让这个 skill 持续做对。
