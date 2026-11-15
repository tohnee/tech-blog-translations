---
title: "作业 2 — 构建智能体 harness（10%）"
title_en: "Assignment 2 — Build an agent harness(10%)"
source: https://cs2680.seas.harvard.edu/assignments/assignment2.html
crawled: 2026-11-16
translated: 2026-11-16
---

# 作业 2 — 构建智能体 harness（10%）

> 原文：[Assignment 2 — Build an agent harness(10%)](https://cs2680.seas.harvard.edu/assignments/assignment2.html) · Harvard CS2680

CS2680 现代 AI 系统：智能体与系统优化（CS2680 Modern AI Systems: Agents and System Optimizations）

作业 2 — 构建智能体 harness

# 作业 2 — 构建智能体 harness（10%）

**发布** 9 月 21 日（周一） · **截止** 10 月 4 日（周日）晚 11:59 ·
[全部五份作业](index.html)

你将构建 `madsLoop`，一个最小化的编程智能体 harness（智能体运行框架），并用 SWE-bench Pro 测试它。智能体就是循环中的模型。它提出工具调用，你的 harness 执行这些调用并把结果反馈回去。本任务的目标是构建模型 API 之外你所需要的一切。

**⚠️ 第 0 部分和第 1 部分只勾勒了智能体的基础。不要盲信它。**

它们描述的是一种**设计选择**，而不是标准答案。
遵循它们的整体结构，但要批判性地评估其底层逻辑。把其中的接口、工具、工作流和提示词当作起点，用真实任务检验它们，并按需修改。
书面报告会问你做了什么不同以及为什么。完全照做的智能体可能会失败。唯一的要求是：1）使用 qwen3.6-35b-a3b 作为模型；2）我们能够调用 run\_task.sh 生成可评估的补丁（用 run\_all.sh 评估）以及智能体日志；3）所有日志符合要求的 schema。

**⚠️ 并非所有给定的任务都可解。**

我们将提供 10 个任务。有些即使使用完美的 harness 也可能无法完成。不过，如果一个任务可以通过修改第 0 部分和第 1 部分来解决，就认为它是可解的。

## 模型 API

我们使用 `api.cs2680.com` 上的课程代理，一个与 OpenAI 兼容的端点，来服务这些请求。

在你运行命令的 shell 中导出你的 key：

```
export CS2680_API_KEY="hyi-..."     # your key
```

```
import os
from openai import OpenAI

# Read the key from the environment. Never hardcode it and never commit it.
# Your agent runs inside the task container, so you have to pass it 
# (e.g. `docker run -e CS2680_API_KEY=...`, see 2.3).
CS2680_API_KEY = os.environ["CS2680_API_KEY"]

client = OpenAI(
    base_url="https://api.cs2680.com/v1",
    api_key=CS2680_API_KEY,
)
resp = client.chat.completions.create(
    model="qwen3.6-35b-a3b",
    messages=[{"role": "user", "content": "hello"}],
    tools=[...],         
)
```

在本作业中，qwen3.6-35b-a3b 将作为骨干模型，并应用于所有评估。

## 环境配置

你设计的智能体将运行在 **Docker 容器**中：每个任务以一个预构建镜像的形式提供，其中包含代码仓库及其依赖；你的智能体在该容器内运行，官方评估也在另一个容器中运行。确保已安装 Docker 并能不使用 `sudo` 运行；提供的十个任务镜像每个约 1.6–1.8 GB。

* **x86-64 Linux 主机是最省事的路径。** 镜像为 `linux/amd64` 构建，可原生运行。
* **Apple Silicon（M1–M4）：** 镜像将在模拟环境下运行。在你运行脚本的 shell 中设置 `PLATFORM_FLAG="--platform linux/amd64"`。`run_task.sh` 会将它传给 `docker pull` 和 `docker run`。预期运行更慢。
* **Windows：** 使用 WSL 2 并开启 Docker Desktop 的 WSL 集成，所有操作都在 Linux 侧运行。
* **偏好 Linux 机器？** 你可以使用课程集群，参见[集群使用说明](../computing/cluster.html)。

如果在配置环境时遇到困难，请联系助教。

## 第 0 部分 — 接口与日志

将[作业 2 起始归档](assignment2.tar.gz)下载到与作业 1 相同的私有 GitHub 仓库根目录。解压生成 `assignment2/`，将所有作业 2 文件放在该目录中，并在该目录下运行下面的命令。

```
# From your shared course repository:
tar -xzf assignment2.tar.gz
cd assignment2
```

### 0.1 接口

```
python madsLoop.py -p "<problem statement>" [--log] <workdir>
```

* `-p` — issue 文本：`evaluation_scripts/agent_task_input.json` 中该任务条目的 `problem_statement` 字段。这是你的智能体收到的任务描述。
* `<workdir>` — 代码库检出路径。
  你的智能体只能在这个目录内读取、搜索、编辑和运行命令。我们将以 /app 为例。
* `--log` — trace 日志，默认关闭。设置后，你的智能体将运行 trace 写入当前工作目录下的 `madsLoop_logs/` 目录（如果不存在则创建），schema 见 0.3。我们评估你的智能体时会传入 `--log`。
* 智能体结束时，修复以未暂存变更的形式存在于 `<workdir>` 中，后续补丁将通过 `git diff` 生成。

### 0.2 开发者日志（`developer_logs/`）

你的提交包含一个 `assignment2/developer_logs/` 目录，记录**你如何使用编程智能体构建 `madsLoop`**。日志应为 `.jsonl` 格式。如果你通过终端或 IDE 使用编程智能体，通常可以在以下位置找到会话日志：

| 工具 | 如何导出 |
| --- | --- |
| Claude Code（终端，或 VS Code / JetBrains 扩展） | 会话中执行 `/export`，或 `~/.claude/projects/<project>/*.jsonl` 下的会话记录 |
| OpenAI Codex（CLI 或 IDE 扩展） | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` 下的会话日志 |
| Cursor | `~/.cursor/projects/<project>/agent-transcripts/*.jsonl` |
| Gemini CLI | `~/.gemini/tmp/<project_hash>/chats/session-*.jsonl` |

### 0.3 智能体日志（`madsLoop_logs/`）

使用 `--log` 运行时，你的智能体应将 trace 以 JSONL 写入 `./madsLoop_logs/`（每次运行一个文件，例如 `madsLoop_logs/run1.jsonl`）：每行一个 JSON 对象，每个事件一行，按顺序记录，可据此重建整个运行过程。每行携带 `timestamp`（ISO-8601）和 `event`；其余字段取决于事件类型：

| `event` | 必需字段 |
| --- | --- |
| `run_start` | `model_id`、`workdir` |
| `api_request` | `iteration`、`prompt_tokens`、`completion_tokens`、`total_tokens`（直接取自 `response.usage`） |
| `api_retry` | `iteration`、`error`、`backoff_s` |
| `tool_call` | `iteration`、`tool_name`、`arguments` |
| `tool_result` | `iteration`、`tool_name`、`result`（按喂给模型时的原样截断）、`is_error` |
| `run_end` | `reason`（`done` / `no_tool_calls` / `error` / 自设限制）、`num_iterations` |

示例行：

```
{"timestamp": "2026-09-12T14:03:07+00:00", "event": "run_start", "model_id": "qwen3.6-35b-a3b", "workdir": "/app"}
{"timestamp": "2026-09-12T14:03:11+00:00", "event": "api_request", "iteration": 1, "prompt_tokens": 1834, "completion_tokens": 96, "total_tokens": 1930}
{"timestamp": "2026-09-12T14:03:11+00:00", "event": "tool_call", "iteration": 1, "tool_name": "bash", "arguments": {"command": "grep -rn 'version_check' qutebrowser/utils/"}}
{"timestamp": "2026-09-12T14:03:12+00:00", "event": "tool_result", "iteration": 1, "tool_name": "bash", "result": "qutebrowser/utils/qtutils.py:91: ...", "is_error": false}
{"timestamp": "2026-09-12T14:12:40+00:00", "event": "run_end", "reason": "done", "num_iterations": 14}
```

请严格遵循这些字段。开发期间，你可以按需使用 stderr 进行打印式调试。但是，使用 --log 时，输出必须遵循此 schema。

## 第 1 部分 — harness 必须包含的内容

### 1.1 工具定义

这是你告诉模型有哪些工具可用的一份清单：每个工具都有名称、自然语言描述，以及参数的 JSON Schema。

一组可用的最小工具集如下，你也可以设计不同的工具集：

| 工具 | 用途 |
| --- | --- |
| `bash(command)` | 在 `<workdir>` 中运行 shell 命令（搜索、运行测试、检查） |
| `read_file(path)` | 返回文件内容（带行号有助于模型编辑） |
| `edit_file(path, old_string, new_string)` | 替换文件中的精确字符串 |
| `done(summary)` | 智能体声明自己已完成 |

### 1.2 智能体循环

让它成为智能体而非聊天机器人的 while 循环：

```
messages = [system prompt, user message containing the problem statement]
loop:
    response = model(messages, tools)
    if response contains tool calls:
        execute each requested tool
        append the assistant message AND one tool-result message per call
        continue
    else:
        break   # model produced a final answer
```

修好你引入的失败很重要，而与你的改动无关的既有失败可以忽略。如果不确定，可以与未修改的代码进行比较。

### 1.3 对话状态管理

模型是无状态的：每次请求都必须重新发送完整历史。你的 harness 拥有这份历史：

* 维护 `messages` 数组：system prompt、初始 user 消息，然后是交替出现的 assistant 轮次（包括其工具调用）和工具结果消息。模型发起的每一次工具调用都必须与且仅与一条引用其调用 ID 的结果消息配对——未配对的调用会导致 API 错误。
* 编写一个 system prompt，告诉模型它的角色、接口（“你正在修复位于 ... 的仓库中的一个 issue；做最小改动；不要修改测试”）、复现协议（“在编辑之前，根据需求在 `/tmp` 下编写复现检查，并用 `repro_check` 注册每一个；
* 上下文增长：工具输出会不断累积。至少要在追加之前截断大输出。

这就是整个最小 harness：工具定义（模型可以请求什么）、循环 + 工具执行器（你的代码执行它所请求的操作）、对话状态（把各轮串起来的记忆）。

## 第 2 部分 — 在容器中运行

**⚠️ 第 2 部分可以信任。:>**

run\_task.sh 可以修改。确保 run\_task.sh 能配合你在第 0 和第 1 部分所做的修改工作。

`agent_task_input.json` 中的每个任务条目都指定了一个预构建 Docker 镜像（`docker_image`），其中包含目标代码仓库。仓库在 `/app` 中检出到指定的 `base_commit`，所有必需的依赖均已预装。要运行你的智能体，首先启动对应的容器，然后在运行中的容器内以 `/app` 作为工作仓库执行智能体。

### 2.1 拉取镜像（每个任务一次）

其他任务的镜像名称在其 `evaluation_scripts/agent_task_input.json` 条目的 `docker_image` 字段中。在 x86-64 主机上，镜像原生运行：

```
# the first task's image (jefzda/sweap-images:qutebrowser.qutebrowser-…)
IMG=$(python -c "import json; print(list(json.load(open('evaluation_scripts/agent_task_input.json')).values())[0]['docker_image'])")
docker pull "$IMG"
```

### 2.2 配置容器环境：`docker_env.sh`

任务镜像没有安装 `openai` 包。使用 `assignment2/docker_env.sh` 安装你的智能体所需的一切。它会在智能体运行之前于容器内执行。最小版本：

```
#!/bin/bash
# docker_env.sh — container setup, runs before madsLoop.py
pip install -q openai
```

如果你的智能体还需要其他东西（例如固定某个 `openai` 版本），请在 docker\_env.sh 中添加，以修改容器环境。确保你的智能体能在 Python 3.10+ 上运行，并可使用 `openai` 和标准库。

### 2.3 在容器内运行你的智能体：run\_task.sh

```
# the first task: its instance_id, and its problem statement (the -p payload) as a file
IID=$(python -c "import json; print(list(json.load(open('evaluation_scripts/agent_task_input.json')))[0])")
python -c "import json; print(list(json.load(open('evaluation_scripts/agent_task_input.json')).values())[0]['problem_statement'])" > problem.txt

docker run --rm \
  --entrypoint bash \
  -v "$PWD:/madsLoop" \
  -e CS2680_API_KEY="$CS2680_API_KEY" \
  "$IMG" \
  -c 'bash /madsLoop/docker_env.sh && \
      cd /tmp && \
      python /madsLoop/madsLoop.py -p "$(cat /madsLoop/problem.txt)" --log /app && \
      cp -r madsLoop_logs /madsLoop/ && \
      git -C /app diff' \
  > "model_patch_$IID.diff"
```

上面的脚本为每个任务确定 ID 和问题陈述，将对应的代码库挂载到容器中，把 `CS2680_API_KEY` 传进去，并配置环境。然后运行 madsLoop。智能体完成对仓库的修改后，脚本导出 madsLoop 日志并生成 diff 补丁。可以随意修改 run\_task.sh，只要确保 run\_all.sh 能调用它即可。

### 2.4 评估你的补丁

使用**官方 SWE-bench Pro 评估脚本**（[scaleapi/SWE-bench\_Pro-os](https://github.com/scaleapi/SWE-bench_Pro-os)）进行真实评估，这与我们评分使用的是同一个工具。它将你的 diff 应用到全新的检出上，恢复留出的测试文件，并运行实际测试。按 `make_patches.py` 的做法将补丁打包成 `patches.json`：

```
python - <<'EOF'
import json, pathlib
tasks = json.load(open("evaluation_scripts/agent_task_input.json"))
predictions = [{"instance_id": iid,
                "model_patch": pathlib.Path(f"model_patch_{iid}.diff").read_text(),
                "prefix": "madsLoop"}
               for iid in tasks]
json.dump(predictions, open("patches.json", "w"), indent=2)
EOF
```

然后运行评估：

```
bash evaluation_scripts/evaluate.sh
```

它会写出 `pro_eval/eval_results.json`，将每个 `instance_id` 映射为 true/false（是否解决），并在 `pro_eval/<instance_id>/` 下提供每个实例的测试日志——这是判断任务是否真正解决的基准事实，可用于迭代你的智能体。补丁的评分方式是将其应用到全新检出、恢复留出的测试文件并运行隐藏测试——你的智能体对现有测试文件所做的任何修改都会被覆盖，因此修改测试帮不了你。

### 2.5 提供的评估脚本（`evaluation_scripts/`）

起始归档包含 `assignment2/evaluation_scripts/` 作为评估入口。它包含：

| 文件 | 作用 |
| --- | --- |
| `agent_task_input.json` | 本地测试任务，以 `instance_id` 为键——你的智能体**唯一**可以使用的任务数据 |
| `task_test.json` | 每个任务的评估数据（测试设置、计分测试），以 `instance_id` 为键——仅供 `evaluate.sh` 使用；你的智能体绝不能读取它 |
| `run_task.sh <idx>` | 拉取任务镜像并在其容器中运行你的智能体（2.1–2.3）；写出 `model_patch_<instance_id>.diff` 并复制回 `madsLoop_logs/` |
| `make_patches.py` | 将你的 `model_patch_*.diff` 文件打包成 `patches.json` |
| `evaluate.sh` | 对 `patches.json` 运行官方 SWE-bench Pro 评估（2.4），将 `agent_task_input.json` 与 `task_test.json` 合并以确定测试设置 |

从 `assignment2/` 运行这些命令，并将 `MADSLOOP_REPO` 设置为其绝对路径。任务 JSON 始终从 `evaluation_scripts/` 内部读取，所有输出（补丁、`patches.json`、`madsLoop_logs/`、`pro_eval/`）都落在 `assignment2/` 下：

```
# Run from assignment2/:
export MADSLOOP_REPO="$PWD"
bash evaluation_scripts/run_task.sh 0     # one task, or run_all.sh for all four
python3 evaluation_scripts/make_patches.py
bash evaluation_scripts/evaluate.sh       # -> pro_eval/eval_results.json
```

**在 `evaluation_scripts/` 中你可以改什么。** 你可以自由编辑 `run_task.sh`、`agent_task_input.json` 和 `task_test.json`，以便在本地做测试——指向你自己的任务、添加调试信息、调整容器配置。我们保留的是 `run_all.sh`、`evaluate.sh` 和 `make_patches.py`：我们运行自己未修改的副本。

### 2.6 构建你自己的任务（`mytest/`）

除了我们给你的任务之外，你还要**自己构建四个任务**。不要从 SWE-bench Pro 或任何其他智能体基准中取题。目的是检验你的 harness 在没有人针对它调优过的任务上是否依然可靠。四个任务分别来自以下来源之一：

* **一个开源仓库**——一个真实 issue，以及关闭它的提交或拉取请求；或
* **你自己过去的一个项目**——你实际修复过的 bug，或你实际添加过的功能。

构建一个任务意味着产出三样东西。

**1. 一段描述。** 这是你的智能体收到的全部信息。它取代我们给你的任务中的 `problem_statement`、`requirements` 和 `interface`，应当是 `problem_statement` 字段中的单段文字。说明哪里有问题或缺失、它如何表现出来，以及什么算完成。将 `requirements` 和 `interface` 保留为键，值设为 `""`，使条目与 `agent_task_input.json` 具有相同形状，你的智能体就能不加修改地读取它。

**2. 证明已修复的测试。** 记录到 `mytest/task_test.json`，以 `instance_id` 为键，字段与 `evaluation_scripts/task_test.json` 相同：`before_repo_set_cmd`、`selected_test_files_to_run`、`fail_to_pass`、`pass_to_pass`。`fail_to_pass` 至少是一个在 `base_commit` 上失败、在任务完成后通过的测试。`pass_to_pass` 是在两种状态下都通过的测试，这样破坏仓库的补丁就无法被计为修复。

**3. 一个容器。** `mytest/tasks/<instance_id>/Dockerfile` 构建一个镜像，仓库检出到 `base_commit`，所有依赖均已安装，使测试无需网络访问即可运行。为其打标签，并将标签放入任务的 `docker_image` 字段——这正是 `run_task.sh` 运行的字段。你不必推送到任何地方：当拉取失败时，`run_task.sh` 会回退到你本地 Docker 守护进程中同名的镜像。

除 Dockerfile 外，还要包含 `mytest/tasks/<instance_id>/gold.diff`：真正的修复，即上游提交或你当时写的内容。它的存在是为了让测试可信，也就是说应用它必须让每一个 `fail_to_pass` 测试变绿。

将四个任务分成两个文件：

* `mytest/solved_after_change.json`——**两个**任务，你的智能体最初**无法**解决，在你修改智能体中的某些内容后**可以**解决。修改必须在提交的代码中。书面报告和视频对此进行说明。
* `mytest/unsolved.json`——**两个**在你提交时智能体仍然无法解决的任务。它们的 `gold.diff` 仍必须让测试通过。

**运行它们。** 工作流与 2.1–2.4 相同，只替换一处：`evaluate.sh` 中的官方评估只认识 SWE-bench Pro 实例，因此无法为你的镜像评分。请编写 `mytest/verify.sh` 来完成这项工作。

```
IID=...                                                # one of your four instance_ids
IMG=...                                                # that task's docker_image tag

docker build -t "$IMG" "mytest/tasks/$IID/"            # 1. build the image
TASKS_JSON=mytest/solved_after_change.json \
  bash evaluation_scripts/run_task.sh 0                # 2. agent -> model_patch_$IID.diff
bash mytest/verify.sh "$IID" "model_patch_$IID.diff"   # 3. apply, run tests, report
```

`verify.sh` 接收一个 `instance_id` 和一个 diff，从该任务的 `docker_image` 启动全新容器，用 `before_repo_set_cmd` 重置检出，应用 diff，运行 `selected_test_files_to_run`，并且只有在**每一个** `fail_to_pass` 测试都通过且**没有** `pass_to_pass` 测试回归时才打印 `RESOLVED`，规则与官方评估相同。不带 diff 运行它可得到 `base_commit` 基线。

将四个任务的输出保存到 `mytest/results/` 下：`<instance_id>.before.log`（在 `base_commit`，显示 `fail_to_pass` 失败）和 `<instance_id>.after.log`（对于 `solved_after_change.json` 中的两个任务，使用你智能体的补丁；对于 `unsolved.json` 中的两个任务，使用 `gold.diff`）。

**`mytest/` 下最少需要提交的内容：**

| 路径 | 数量 | 内容 |
| --- | --- | --- |
| `solved_after_change.json` | 2 个条目 | 智能体侧任务字段，形状与 `agent_task_input.json` 相同 |
| `unsolved.json` | 2 个条目 | 同上 |
| `task_test.json` | 4 个条目 | `before_repo_set_cmd`、`selected_test_files_to_run`、`fail_to_pass`、`pass_to_pass` |
| `tasks/<instance_id>/Dockerfile` | 4 | 构建该任务 `docker_image` 中所命名的镜像 |
| `tasks/<instance_id>/gold.diff` | 4 | 真正的修复；使 `fail_to_pass` 变绿 |
| `verify.sh` | 1 | 在容器中应用 diff 并报告 `RESOLVED` / `unresolved` |
| `results/<instance_id>.{before,after}.log` | 8 | 你记录的运行结果 |

## 交付物

提交包含三部分：**代码**（一个 GitHub 仓库）、一份**书面报告**和一段**视频**。我们使用与作业 1 相同的**私有 GitHub 仓库**，代码和书面报告放在 `assignment2/` 下。视频应上传到 Canvas。

### 代码

我们的评分方式是克隆你的共享仓库，并从 `assignment2/` 运行 `bash evaluation_scripts/run_all.sh`。请按以下布局将该作业目录中的智能体入口、容器配置、评估脚本、书面报告和日志放在其中。

共享仓库内要求的布局：

```
assignment2/
├── madsLoop.py                             # the agent entry point
├── docker_env.sh                           # container setup (see 2.2)
├── writeup.pdf                             # the one-page write-up
├── src/                                    # the modules madsLoop.py imports, the harness design
│   ├── agentic_loop.py                     #   (any structure you like — this is one example)
│   ├── tools.py
│   └── prompts.py
├── developer_logs/                         # how you built madsLoop (see 0.2)
│   └── claude_code_session.jsonl           #   logs in jsonl
├── evaluation_scripts/                     # provided by us (see 2.5)
│   ├── agent_task_input.json               #   
│   ├── task_test.json                      #  
│   ├── run_task.sh                         #  
│   ├── run_all.sh                          #   entry point for our grading evaluation, do not change it
│   ├── make_patches.py                     #   
│   └── evaluate.sh                         #   
├── mytest/                                 #  four tasks you build yourself (see 2.6)
│   ├── solved_after_change.json            #   2 tasks: unsolved at first, solved after a change to your agent
│   ├── unsolved.json                       #   2 tasks: still unsolved at the end
│   ├── task_test.json                      #  
│   ├── tasks/<instance_id>/Dockerfile      #   one per task: builds the image named in docker_image
│   ├── tasks/<instance_id>/gold.diff       #   one per task: the real fix, never shown to your agent
│   ├── verify.sh                           #   applies a patch in the container and runs the tests
│   └── results/                            #   <instance_id>.before.log and .after.log per task
└── README.md                               # optional: design notes, tool-set rationale
```

我们的评估方式是运行 `run_all.sh`，它会对每个任务调用 `run_task.sh`。你的 `run_task.sh` 应当使用 `--log` 调用你的智能体，并为每个任务生成补丁；随后 `run_all.sh` 将这些补丁打包并评估。

### 书面报告

一份一页（硬性上限）的 PDF，位于 `assignment2/writeup.pdf`，包含三个部分：

1. **你认为（而不是智能体认为）`agent_task_input.json` 中哪些任务不可解，以及为什么。** 列出 `instance_id`，并给出你运行中的证据：智能体尝试了什么、卡在哪里，以及任务本身的什么原因（而不是你的智能体）使它不可解。你可以按任何你认为合适的方式修改第 0 和第 1 部分的说明。由这些说明导致的失败不应被视为不可解。相反，请找出任务本身使其无法解决的问题。
2. **你与讲义相比做了什么不同的地方。** 使用项目符号，每条对应一处差异：你的 harness 在哪里偏离了第 0–1 部分描述的设计，以及为什么。
3. **你如何让 `solved_after_change.json` 中的两个任务通过。** 对这两个任务分别说明：最初哪里失败、你在智能体中改了什么，以及该修改如何把失败变为通过。

文档必须完全是你自己的工作。不得包含 AI 生成的文字。

### 视频

录制一段 **3 分钟**的视频。首先讲解你的代码：入口、工具、智能体循环，以及对话状态如何保存。然后展示你修改了代码的哪一部分，使 `solved_after_change.json` 中的两个任务从无法解决变为可解决，以及为什么该修改带来了差别。视频应上传到 Canvas。

## 评分

| 部分 | 权重 | 评分内容 |
| --- | --- | --- |
| 隐藏任务 | **40%** | 我们使用 `run_task.sh` 在提供的任务以及若干额外的隐藏 SWE-bench Pro 任务（格式与 `agent_task_input.json` 相同）上运行你的智能体，并用官方评估为每个补丁评分。得分是可解任务中被解决的比例。对不可解任务得到 PASS 会失分。所有隐藏任务都是可解的。请自行判断哪些任务可解，然后解决它们。 |
| 书面报告 | **40%** | 20%——给定任务中哪些不可解及其原因。10%——你与讲义相比做了什么不同。10%——`mytest/` 任务：你自己构建的四个任务，均不来自 SWE-bench Pro，每个都有单段 `problem_statement`、能构建的 `Dockerfile`，以及能被 `gold.diff` 变绿的 `fail_to_pass` / `pass_to_pass` 测试；四个任务都能在 `run_task.sh` 下运行并在你的 `verify.sh` 下评分；`solved_after_change.json` 中的两个任务在你描述的修改之前失败、之后通过；对修改的解释与代码一致。 |
| 视频 | **20%** | 3 分钟视频：对代码的清晰讲解，以及正确说明哪项修改使 `solved_after_change.json` 中的两个任务从无法解决变为可解决。 |

## 现在开始吧！

祝你和你的智能体玩得开心！下载起始文件 [`assignment2.tar.gz`](assignment2.tar.gz)，并按[第 0 部分](#part-0)所述解压。

[← 作业 1 — 体验编程智能体](assignment1.html)
[作业 3 — Harness 竞赛 →](assignment3.html)
