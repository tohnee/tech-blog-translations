---
title: "MiMoCode：模型与智能体协同进化"
title_en: "XiaomiMiMo/MiMo-Code"
source: https://github.com/XiaomiMiMo/MiMo-Code/blob/main/README.md
crawled: 2026-09-22
translated: 2026-09-22
---

# MiMoCode：模型与智能体协同进化

> 原文：[XiaomiMiMo/MiMo-Code](https://github.com/XiaomiMiMo/MiMo-Code/blob/main/README.md) · 小米 MiMo

<h1 align="center">MiMoCode</h1>

<p align="center">
  <img src="assets/readme/mimocode-banner.png" alt="MiMoCode" width="700">
</p>

<p align="center"><strong>MiMo Code：模型与智能体协同进化</strong></p>

<p align="center">
  <a href="README.zh.md">中文</a> | English
</p>

<p align="center">
  <a href="https://mimo.xiaomi.com/coder">官网</a> | <a href="https://mimo.xiaomi.com/en/blog/mimo-code-long-horizon">博客</a>
</p>

---

MiMoCode 是一款终端原生（terminal-native）AI 编程助手。它可以读写代码、运行命令、管理 Git，并借助持久化记忆系统在多个会话之间保持对项目的深入理解，同时持续自我改进。

<p align="center"><strong>MiMo Desktop Beta 邀请</strong>：<a href="https://mimo-ai.xiaomimimo.com/desktop/invite/">申请国际版 Beta 资格</a></p>

## 小米 MiMo Desktop Beta

<p align="center"><img src="assets/readme/mimo-desktop-en.jpg" alt="Xiaomi MiMo Desktop 英文界面：开始一个新任务" width="900"></p>

小米 MiMo Desktop 为真实工作场景而生：一个对话即可处理办公、设计、编程和多模态创作，多个对话之间可以分工协作。桌面应用以 **MiMo Code 作为核心引擎**，将其终端原生的智能能力带入桌面工作流。

- **智能编排**：评估任务类型与成本，动态选择模型、框架和工具；复杂任务可以在多个智能体之间并行执行。
- **持续迭代**：拖入多种格式的文件，创建 PPT、网页、3D 资产和应用，在会话内预览并操作结果，精确编辑选定区域，并回滚版本。
- **可控的长任务成本**：在标准模型与旗舰模型之间路由，只编辑必要的区域，支持最高 99% 的同会话缓存命中率与 95% 的跨会话缓存命中率。
- **浏览器控制**：打开网页、检索信息、填写表单，并在生成网页后检查关键交互。
- **电脑控制（仅国际版）**：读取屏幕并跨应用操作鼠标与键盘；录制与回放（Record & Replay）让你可以用自然语言复用录制好的工作流。

通过 Beta 审批后，用户可以获得新版 **MiMo-X-Pro-Preview** 与 **MiMo-X-Flash-Preview** 模型的限时、限量试用。

MiMoCode 支持接入任意主流 LLM 供应商 API。

---

## 快速开始

```bash
# One-line install (macOS / Linux)
curl -fsSL https://mimo.xiaomi.com/install | bash

# One-line install (Windows PowerShell)
powershell -ep Bypass -c "irm https://mimo.xiaomi.com/install.ps1 | iex"

# Or install via npm (all platforms)
npm install -g @mimo-ai/cli

# Run
mimo
```

首次启动会自动引导你完成配置。支持的选项：
- **小米 MiMo 平台** — OAuth 登录
- **Codex（ChatGPT Pro/Plus）** — OpenAI OAuth 登录
- **从 Claude Code 导入** — 一步迁移已有的认证信息
- **供应商列表** — 通过 API Key 接入目录中的供应商，或在支持处使用 OAuth（例如 xAI/Grok）
- **自定义供应商** — 在 TUI 中添加任意 OpenAI 兼容 API

<details>
<summary><strong>WSL：剪贴板问题</strong></summary>

如果你在 WSL 上复制时遇到乱码，请安装 `xsel`：
```bash
sudo apt install xsel
```
</details>

<details>
<summary><strong>macOS：默认终端中的渲染问题</strong></summary>

MiMoCode 不支持 macOS 内置的终端（Terminal.app）。如果界面错位、闪烁或出现其他渲染问题，请改用 [iTerm2](https://iterm2.com/) 或 VS Code 集成终端：

```bash
brew install --cask iterm2
```
</details>

<details>
<summary><strong>TUI 卡顿与视觉动画问题</strong></summary>

如果直接通过 SSH 运行时 TUI 卡顿，请在本地渲染，只在远程主机上运行 MiMoCode 服务端。在远程项目目录下启动服务端：

```bash
# Remote host
mimo serve --port 4096

# Local host: create the SSH port forward
ssh -N -L 4096:127.0.0.1:4096 user@remote-host

# Local host: connect from another terminal
mimo attach http://127.0.0.1:4096
```

如果是装饰性动画导致卡顿，可以运行 `/vivid`，或在 `ctrl+p` 命令面板中配置 **Vivid visuals**，按需在 Vivid 与 Minimal 视觉效果之间切换。

</details>

<details>
<summary><strong>Windows：Shell 中 CJK（中日韩）输出乱码</strong></summary>

在 Windows 上，若系统区域设置不是 UTF-8（例如 zh-CN，其活动代码页为 936/GBK），包含 CJK 字符的命令输出可能出现乱码（mojibake）。MiMoCode 会对其启动的 PowerShell/cmd 子进程强制 UTF-8 输出。如果在此机制尚未覆盖的场景中仍然出现乱码，可以开启 Windows 的系统级 UTF-8 支持：

**设置 → 时间和语言 → 语言和区域 → 管理语言设置 → 更改系统区域设置 → 勾选“Beta: 使用 Unicode UTF-8 提供全球语言支持” → 重启。**

这会把所有程序的活动代码页（ACP）切换为 UTF-8（65001），子进程因此不再继承旧代码页。注意这是系统级的 Beta 开关，可能导致部分较老的非 Unicode 程序显示异常，请将其视为一种权宜方案。
</details>

---

## MiMo 生态系统

除 MiMoCode 之外，小米 MiMo 模型也可以在 Cursor、Cline、Zed 等其他智能体和编程工具中使用。

**[awesome-mimo-agent](https://github.com/XiaomiMiMo/awesome-mimo-agent)** 汇集了在这些工具中使用 MiMo 的配置指南——如果你想在其他地方试用 MiMo，值得一读。欢迎贡献：提交 PR 来添加你自己的配置。

---

## 核心特性

### 多智能体（Multiple Agents）

| 智能体 | 描述 |
|--------|------|
| **build** | 默认。拥有完整工具权限，用于开发 |
| **plan** | 只读分析模式，用于代码探索与方案设计 |
| **compose** | 编排模式，用于规格驱动开发与技能驱动工作流 |

按 `Tab` 可在主智能体之间切换。子智能体由系统按需创建。首条消息之后模式即锁定：Build 与 Plan 仍可互相切换，但 Compose 一旦进入便被隔离——从会话开始就固定技能/工具集，可以显著提升工具调用的可靠性。

对于前沿模型（Fable/Sol 级别），运行 compose 类工作的推荐方式是在 **build** 智能体上使用 **`/compose-next`** 技能——参见 [Compose 模式](#compose-模式)。

### 持久化记忆

基于 SQLite FTS5 全文检索的跨会话记忆：

- **项目记忆**（`MEMORY.md`）— 持久化的项目知识、规则与架构决策
- **会话检查点**（`checkpoint.md`）— 由 checkpoint-writer 子智能体自动维护的结构化状态快照
- **草稿笔记**（`notes.md`）— 智能体的临时笔记区
- **任务进度**（`tasks/<id>/progress.md`）— 每个任务的日志

会话恢复时记忆会自动注入，智能体无需重新学习项目上下文。

### 智能上下文管理

- **自动检查点** — 基于模型上下文窗口决定何时保存会话状态
- **上下文重建** — 当上下文接近上限时，从最新检查点、项目记忆、任务进度和保留的近期消息重建上下文，使智能体可以继续当前任务
- **预算化注入** — 使用 token 预算控制进入上下文的检查点、记忆与笔记内容量，并按重要性排序
- **可调节的压缩点** — `/context-limit`（或 `compaction.max_context`）可以让某个模型早于其自身窗口进行压缩（compaction），按模型分别设置

<details>
<summary><strong>早于模型窗口进行压缩（<code>/context-limit</code>）</strong></summary>

压缩通常在略低于模型上下文窗口的位置触发。运行 `/context-limit` 可以为当前模型选择一个更小的工作预算——`200K` / `300K` / `500K` / `1M` 或自定义值——按模型存储为 `compaction.max_context`：

```jsonc
{
  "compaction": {
    "max_context": {
      "openai/gpt-5.6": "272K", // token count, "300K", "1M", or "50%" of the window
      "anthropic/*": "300K" // wildcards allowed, longest pattern wins
    }
  }
}
```

该值始终会被钳制到供应商实际接受的范围，因此只能降低压缩点，不能提高。`0` 可恢复为模型自身窗口。

你可能需要它的原因：

- **成本档位。** 对于输入超过 272K 的请求，OpenAI 对 GPT-5.6 的整个请求按 2 倍输入价、1.5 倍输出价计费。
- **宣传的窗口并不总是你实际能用的窗口。** 同一个模型的可用窗口可能因接入方式而异——ChatGPT/Codex 订阅、直连 API Key，或 OpenRouter 之类的转售渠道——因此目录里标注的 1M 并不代表你的链路真的提供 1M。
- **质量与延迟。** 非常长的上下文更慢，而且超过某个点之后并不会更好。

`mimo models <provider>` 会按模型打印 MiMoCode 解析到的窗口以及触发压缩的 token 数。提示词页脚使用同一数字作为分母（`33.0K/260K↓ (13%)`——`↓` 表示预算已生效），`/status` 会给出明细。

</details>

### 任务跟踪

树状任务系统（`T1`、`T1.1`、`T1.2`……）与检查点系统自动集成，因此会话恢复时任务进度得以保留。

### 子智能体系统

主智能体可以按需创建子智能体。子智能体共享当前会话上下文，可以并行工作，并具备生命周期跟踪、取消与后台执行能力。

### 目标 / 停止条件

`/goal` 命令为会话设置停止条件。当智能体试图停止时，一个独立的裁判模型会评估对话，判断条件是否真正满足——防止自主工作过程中过早地“乐观停止”。

### Compose 模式

Compose 是 MiMoCode 面向规格驱动开发的结构化工作流，编排从规格（spec）到交付代码的完整生命周期。

推荐的使用方式是在 **build** 智能体上使用 **`/compose-next`** 技能：一份自包含的完整契约，覆盖 grill → workspace → spec → implement → verify → review → finalize → finish，特性文档位于工作区根目录下的 `docs/compose/spec/<feature>.md`。它面向前沿模型（Fable/Sol 级别）设计，这类模型能将大部分工作流内化，从一份紧凑契约出发工作效果最好。

传统路径是专用的 **compose 智能体**（用 `Tab` 切换），它编排十四个内置技能，覆盖规划、执行、代码评审、TDD、调试、验证与合并——这套循序渐进的流程对较弱的模型仍然有用。

### 工作流（Workflows）

工作流是确定性的 JavaScript 脚本，在沙箱化运行时中编排多个智能体。与智能体对话不同，工作流编码固定的阶段序列，带有重试上限和自动并行化——即发即忘（fire-and-forget）式执行，无需用户交互。

MiMoCode 自带四个内置工作流：

| 工作流 | 阶段 | 描述 |
|----------|--------|-------------|
| `compose` | Brainstorm → Design → Implement → Verify → Review → Report → Merge | 完整开发流水线。将独立任务自动并行化到隔离的 git worktree 中，按任务执行 TDD，并在阶段之间传递结构化输出。最适合可清晰分解为独立子任务、定义良好的任务。 |
| `deep-research` | Brief → Plan → Research → Reflect → Write → Review | 多源深度研究报告生成器。规划相互独立的研究角度，并行运行子智能体收集带引用的发现，反思缺口，撰写一份连贯的 Markdown 报告，然后对引用做冷评审。收敛型：可通过文件检查点恢复。 |
| `fact-check` | Plan → Search → Extract → Group → Crosscheck → Report | 对抗式事实核查。并行运行网络搜索，提取可核查的事实，对重复项分组，然后用 3 人陪审团式的对抗投票交叉验证每一条。最适合精确论断（“X 是否为真？”）。 |
| `research-experiment` | Baseline → Loop → Audit → Report | 面向可机械验证指标的自主优化循环。建立基线，按假设 → 实现 → 评估 → 保留/回退的循环迭代，审计是否存在刷指标（metric gaming）行为，并产出可复现的结果日志。需要一条固定预算的评估命令和一个明确的可编辑文件范围。 |

compose 工作流与交互式路径互补：当需求清晰、任务可以干净拆分时使用**工作流**（确定性、并行、非交互）；当你需要在流程中途转向或在步骤之间注入判断时，使用 **build** 智能体加 `/compose-next`（或传统的 compose 智能体）（会话式、交互式）。

**自定义工作流：** 在 `.mimocode/workflows/` 或 `.claude/workflows/` 中放置 `.js` 文件即可定义你自己的工作流，或使用相同名称覆盖内置工作流（例如 `.mimocode/workflows/compose.js`）。

### 内置技能（Builtin Skills）

技能是可复用的指令集，教会智能体如何处理特定任务（例如生成 PDF、撰写学术论文、检索 arXiv）。对于新任务，MiMoCode 会按精确名称、本地化别名和 BM25 相关性搜索可用的非 Compose 技能。高置信度匹配会自动加载；不确定的匹配会排序后交由智能体评估。在 TUI 中输入 `/` 可浏览自动补全列表，或用 `/<skill-name>` 直接调用技能——在一条消息中提及两个及以上技能会自动加载它们，并注入多技能编排计划。

MiMoCode 捆绑了以下内置技能：

| 技能 | 描述 |
|-------|-------------|
| `arxiv` | 检索、阅读、引用和分析 arXiv 论文 |
| `claude-code` | 将编程、测试、评审和 Git 任务委托给 Claude Code CLI |
| `codex` | 在无头自动化、CI、容器和远程环境中运行和排障 Codex CLI |
| `compose-next` | 推荐的规格→交付（spec→ship）特性交付工作流；仅在用户明确请求时调用 |
| `data-analytics` | 通过可复用工作流分析产品与业务数据：数据质量、KPI、仪表盘、报告、Notebook 与市场规模测算 |
| `deep-research` | 用并行子智能体和内置网络工具产出带引用的多源研究报告 |
| `docx-official` | 生成、读取和转换 Word（.docx）文件 |
| `html-to-video-pipeline` | 通过无头浏览器 + ffmpeg 将 HTML 渲染为 MP4 |
| `learn-everything` | 将文档、URL 或主题转化为带练习、反馈和进度跟踪的自适应课程 |
| `loop` | 按固定节奏调度周期性提示 |
| `mimocode-docs` | MiMoCode 特性、命令、供应商与配置的自文档化参考 |
| `modern-python-toolchain` | 用 uv、Ruff 和 Pyright 搭建现代 Python 项目 |
| `pdf-official` | 生成、读取、填写和转换 PDF 文件 |
| `pptx-official` | 编写和操作 PowerPoint（.pptx）演示文稿 |
| `product-design` | 通过聚焦的工作流探索、审计、实现和 QA 产品与 UX 设计 |
| `research-paper-writing` | 撰写和润色学术论文（ML/CV/NLP 风格） |
| `sales` | 支持销售调研、会议准备、客户分级、交易策略、预测和 CRM 工作流 |
| `skill-creator` | 创建和改进智能体技能的交互式向导 |
| `super-research` | 运行长时程、可审计的研究、实验、基准测试、诊断、复现和引用核查 |
| `xlsx-official` | 构建、清洗和转换电子表格（.xlsx/.csv） |

`claude-code` 与 `codex` 仅在分别安装了 `claude` 和 `codex` 可执行文件时才会出现。其他技能可能仍需要其指令中描述的任务专用工具。

**覆盖内置技能：** 在项目级（`.mimocode/skills/<name>/SKILL.md`）或个人级（例如 `~/.config/mimocode/skills/<name>/SKILL.md`）MiMoCode 技能目录下创建同名 `name` 的技能即可。项目中的开放标准 `.agents/skills/` 与 `~/.agents/skills/` 也是兼容的发现根目录。扫描顺序中较晚发现的用户技能会覆盖同名内置技能。

<details>
<summary><strong>通过环境变量配置技能</strong></summary>

| 变量 | 效果 |
|----------|--------|
| `MIMOCODE_DISABLE_BUILTIN_SKILLS=true` | 禁用全部内置技能 |
| `MIMOCODE_DISABLE_OFFICIAL_SKILLS=true` | 仅禁用办公/媒体技能：`docx-official`、`pdf-official`、`pptx-official`、`xlsx-official`、`html-to-video-pipeline` |
| `MIMOCODE_DISABLE_SLASH_SKILLS=true` | 在 TUI `/` 自动补全中隐藏技能，但不禁用它们 |

**外部技能根目录**（默认范围为 `.mimocode` + 开放标准 `.agents`）：

| 环境变量 | 默认值 | 效果 |
| --- | --- | --- |
| `MIMOCODE_DISABLE_AGENTS_SKILLS=true` | 未设置 = 开启 | 关闭 `~/.agents/skills` 与项目 `.agents/skills` |
| `MIMOCODE_ENABLE_CLAUDE_CODE_SKILLS=true` | 未设置 = 关闭 | 启用 `.claude/skills` |
| `MIMOCODE_ENABLE_CODEX_SKILLS=true` | 未设置 = 关闭 | 启用 `.codex/skills`（仅用户技能；Codex 的 `skills/.system` 永不加载） |
| `MIMOCODE_ENABLE_OPENCODE_SKILLS=true` | 未设置 = 关闭 | 启用 `.opencode/skills` |

外部扫描永远不会匹配 `skills/` 之下带点号（dotted）的路径段。

`MIMOCODE_DISABLE_BUILTIN_SKILLS` 与 `MIMOCODE_DISABLE_OFFICIAL_SKILLS` 会将相应技能从智能体的可用技能列表中彻底移除——它们不会出现在上下文中，也无法被调用。`MIMOCODE_DISABLE_SLASH_SKILLS` 只影响 TUI 自动补全；技能对智能体仍然可用。

</details>

### 语音输入

由 TenVAD 和 MiMo ASR 驱动的实时流式语音输入。用 `/voice` 激活后即可说话——音频按停顿分段，并增量转写进输入框。面向已登录 MiMo 的用户。需要 `sox`（macOS 上 `brew install sox`，其他平台类似）。

<details>
<summary><strong>WSLg 音频配置</strong></summary>

```bash
sudo apt install -y sox pulseaudio libasound2-plugins
export PULSE_SERVER=unix:/mnt/wslg/PulseServer
```
</details>

<details>
<summary><strong>SSH 远程音频（Mac → 远程主机）</strong></summary>

```bash
# Mac (local)
brew install pulseaudio
pulseaudio --load="module-native-protocol-tcp auth-ip-acl=127.0.0.1" --exit-idle-time=-1 --daemonize
# Add to ~/.ssh/config: RemoteForward 4713 127.0.0.1:4713

# Remote host
apt install -y pulseaudio pulseaudio-utils sox
export PULSE_SERVER=tcp:127.0.0.1:4713
# Verify: pactl info
```
</details>

<details>
<summary><strong>非 MiMo 语音供应商（OpenRouter、内部 API 等）</strong></summary>

语音输入可以通过 `voice` 配置字段路由到其他 OpenAI 兼容供应商。ASR 模型（`mimo-v2.5-asr`）仅在 MiMo 平台提供；语音控制模型（`mimo-v2.5`）在 OpenRouter 及兼容中转平台上可用。

**OpenRouter（仅语音控制）：**

使用 `/connect` 登录 OpenRouter，然后在配置中添加：
```jsonc
{
  "voice": {
    "control_model": "openrouter/xiaomi/mimo-v2.5"
  }
}
```

**内部 / 自建中转（ASR 与语音控制均可）：**
```jsonc
{
  "provider": {
    "internal": {
      "options": {
        "baseURL": "https://your-api-gateway.example.com/v1",
        "apiKey": "sk-..."
      },
      "models": {
        "xiaomi/mimo-v2.5-asr": { "name": "MiMo-V2.5-ASR" },
        "xiaomi/mimo-v2.5": { "name": "MiMo-V2.5" }
      }
    }
  },
  "voice": {
    "asr_model": "internal/xiaomi/mimo-v2.5-asr",
    "control_model": "internal/xiaomi/mimo-v2.5"
  }
}
```

自定义供应商必须在其 `models` 字段中注册至少一个模型才会被识别。`voice.*_model` 中的模型名会直接发送给 API——无需与注册的模型键完全一致。

> **注意：** 注册在自定义供应商下的模型会出现在模型选择列表中。不要把仅支持 ASR 的模型（例如 `mimo-v2.5-asr`）用作主力编程模型。

</details>

### Dream 与 Distill

- **`/dream`** — 扫描近期会话轨迹，将持久性知识提取进项目记忆，并删除过时条目
- **`/distill`** — 在近期工作中发现重复的手工工作流，将高置信度候选打包为可复用的技能、子智能体或命令

---

## 配置

MiMoCode 使用 JSON/JSONC 配置文件，并发布了 JSON Schema 用于自动补全和校验。

### 文件位置

| 文件 | 项目级 | 全局 |
|------|--------------|--------|
| 主配置 | `.mimocode/mimocode.jsonc`（也支持 `.json`） | `~/.config/mimocode/mimocode.jsonc`（也支持 `.json`） |
| TUI 配置 | `.mimocode/tui.json` | `~/.config/mimocode/tui.json` |
| 认证凭据 | — | `~/.local/share/mimocode/auth.json` |

> 在 Windows 上，XDG 路径位于 `%LOCALAPPDATA%\mimocode\` 之下。你可以用 `MIMOCODE_HOME` 覆盖所有路径。

### JSON Schema

MiMoCode 首次加载配置时会自动注入 `$schema` 字段，因此你的编辑器开箱即可获得补全和校验：

| 配置 | Schema URL |
|--------|-----------|
| `mimocode.jsonc` / `mimocode.json` | `https://mimo.xiaomi.com/mimocode/config.json` |
| `tui.json` | `https://mimo.xiaomi.com/mimocode/tui.json` |

<details>
<summary><strong>VS Code / Cursor：信任 Schema 域名</strong></summary>

将以下内容加入 `settings.json`，使编辑器可以下载 Schema 以获得自动补全：

```json
{
  "json.schemaDownload.trustedDomains": {
    "https://mimo.xiaomi.com/": true
  }
}
```

</details>

<details>
<summary><strong>数据目录</strong></summary>

除配置文件外，MiMoCode 将运行时数据存储在 XDG 路径（或 `$MIMOCODE_HOME`）下：

| 目录 | 默认路径（Linux） | 内容 |
|-----------|----------------|----------|
| data | `~/.local/share/mimocode/` | SQLite 数据库、认证凭据（`auth.json`）、记忆、日志 |
| state | `~/.local/state/mimocode/` | TUI 偏好（`kv.json`）、最近使用的模型（`model.json`） |
| cache | `~/.cache/mimocode/` | 语言服务器、缓存的模型目录、技能 |

要删除已存储的凭据，请删除数据目录中的 `auth.json`。在 macOS 上，XDG 数据默认位于 `~/Library/Application Support/mimocode/`。

</details>

### 自定义 OpenAI 兼容端点

如果你的供应商不在内置模型目录中，可以直接用其 base URL、API Key 和模型 ID 配置：

```jsonc
{
  "$schema": "https://mimo.xiaomi.com/mimocode/config.json",
  "model": "custom/MODEL_NAME",
  "provider": {
    "custom": {
      "name": "Custom",
      "npm": "@ai-sdk/openai-compatible",
      "only_configured_models": true,
      "models": {
        "MODEL_NAME": {
          "name": "MODEL_NAME"
        }
      },
      "options": {
        "baseURL": "BASE_URL",
        "apiKey": "API_KEY"
      }
    }
  }
}
```

- 使用精确的键名 `baseURL` 和 `apiKey`。
- 原样保留供应商给出的 base URL 和模型 ID。MiMoCode 不要求供应商已知，除非端点本身要求，你不应添加或删除 `/v1`。
- `models` 下的键是上游模型 ID。支持包含 `/` 的模型 ID，因为 `model` 中只有第一个 `/` 用于分隔供应商 ID 与模型 ID。
- 如有需要，可将 `custom` 替换为另一个未使用的小写供应商 ID，并在顶层 `model` 值中使用相同 ID。
- `@ai-sdk/openai-compatible` 适用于 OpenAI 兼容 API。使用不同线协议（wire protocol）的服务需要其供应商专属的适配器。

将用户级设置放在 `~/.config/mimocode/mimocode.jsonc`（或同目录下的 `mimocode.json`），或仅项目级设置放在 `.mimocode/mimocode.jsonc`（或 `.json`），并与已有配置合并。由于 `apiKey` 以明文存储，请确保该文件仅你的用户可读，且绝不提交到版本库。运行 `mimo models` 或使用 TUI 模型选择器来验证配置的模型。

要声明自定义模型支持哪些输入模态（图像、音频、视频、PDF），可在 TUI 中运行 `/modalities`——这是一个多选对话框，会将设置持久化到配置，无需手工编辑。

### 关键选项

- 供应商与模型选择
- 智能体权限与自定义智能体
- 检查点与记忆行为
- MCP 服务器连接
- 快捷键与主题

Max Mode（带裁判选择的并行 best-of-N 推理）可通过配置中的 `experimental.maxMode` 启用。

<details>
<summary><strong>允许系统临时目录（<code>/tmp</code>）</strong></summary>

默认情况下，读写项目工作目录之外的文件会触发 `external_directory` 权限提示——包括系统临时目录。这是有意为之：MiMoCode 不会悄悄放宽权限，因此项目之外模型能触碰什么始终由你掌控。

临时目录经常被触发，因为大多数模型会把它当作草稿空间（例如快速脚本、一次性数据文件）。如果你信任自己的环境并且不想每次都被提示，可以在配置中选择允许：

```json title=".mimocode/mimocode.json"
{
  "$schema": "https://mimo.xiaomi.com/mimocode/config.json",
  "permission": {
    "external_directory": {
      "/tmp/**": "allow"
    }
  }
}
```

**此设置存在已知风险——使用需自担风险。** 临时目录是全局可写的，并与机器上所有其他进程和用户共享。自动允许意味着模型可以不经确认在那里读写，这会扩大你暴露于可预测临时路径/符号链接攻击的风险面（例如其他进程预先把 `/tmp/foo` 创建为指向敏感文件的符号链接）。因此，它只推荐在单用户、受控环境或容器内使用。请尽量收窄允许列表。

</details>

<details>
<summary><strong>跳过权限提示（<code>--dangerously-skip-permissions</code>）</strong></summary>

对于可信的一次性环境（容器、沙箱、CI），你可以自动批准智能体的一切操作，而不必逐项确认：

```bash
# TUI — prompts once for an explicit confirmation on startup
mimo --dangerously-skip-permissions

# Headless
mimo run --dangerously-skip-permissions "your prompt"

# Or via environment variable (any surface)
MIMOCODE_DANGEROUSLY_SKIP_PERMISSIONS=1 mimo
```

这会在你的配置之下注入一个**允许一切的基线**，因此没有规则的工具会自动批准——但你写下的任何显式规则仍然优先（最后匹配的规则胜出，而你的规则位于注入的 `*` 之后）。`deny` 仍然会拦截；注意残留的 `ask` 规则也仍然会提示，而顶层的 `"*": "ask"` 会让该标志形同虚设。在 TUI 中它会显示红色警告，并要求你先接受风险才生效（没有 TTY 时会跳过提示，因此在 CI 中会无需确认直接激活）。

**这很危险。** 权限被绕过后，一个恶意提示、文件或插件可以运行任意 shell 命令，并在毫无确认的情况下读取、修改或外传你的数据。只在你完全信任该工作区的地方使用。

更轻量的选择是 `/skip-permissions` 命令，在 TUI 内运行时切换自动允许：`deny` 规则仍然拦截，强制询问的操作（例如破坏性 bash）会在 60 秒后自动拒绝，并向模型反馈可据以行动的信息，而不是挂起等待。

</details>

---

## 开发

```bash
bun ci                   # Install dependencies (= bun install --frozen-lockfile)
bun run dev              # Run in development mode
bun turbo typecheck      # Type check
```

---

## 与 OpenCode 的关系

MiMoCode 构建为 [OpenCode](https://github.com/anomalyco/opencode) 的一个分支（fork）。它保留了 OpenCode 的全部核心能力（多供应商、TUI、LSP、MCP、插件），并新增了持久化记忆、智能上下文管理、子智能体编排、目标驱动的自主循环、compose 工作流，以及通过 dream/distill 实现的自我改进。

---

## 社区

扫描二维码加入社区群聊：

<p align="center">
  <img src="assets/readme/community-qrcode-1.jpg" alt="社区群聊二维码 1" width="240">
  &nbsp;&nbsp;
  <img src="assets/readme/community-qrcode-2.jpg" alt="社区群聊二维码 2" width="240">
</p>

---

## 许可证

源代码基于 [MIT License](./LICENSE) 授权。

对 MiMoCode 的使用还受 [使用限制](./USE_RESTRICTIONS.md) 约束。
对小米 MiMo 托管服务的使用受 [MiMo 服务条款](https://platform.xiaomimimo.com/docs/terms/user-agreement) 约束。
对 MiMo 名称、Logo 和商标的使用受 MiMo 商标政策约束。
