---
title: "作业 3 — Harness 竞赛（20%）"
title_en: "Assignment 3 — Harness competition(20%)"
source: https://cs2680.seas.harvard.edu/assignments/assignment3.html
crawled: 2026-11-16
translated: 2026-11-16
---

# 作业 3 — Harness 竞赛（20%）

> 原文：[Assignment 3 — Harness competition(20%)](https://cs2680.seas.harvard.edu/assignments/assignment3.html) · Harvard CS2680

CS2680 现代 AI 系统：智能体与系统优化（CS2680 Modern AI Systems: Agents and System Optimizations）

作业 3 — Harness 竞赛

# 作业 3 — Harness 竞赛（20%）

**发布** 10 月 5 日（周一） · **截止** 10 月 20 日（周二）晚 11:59 · [幻灯片](../slides/8_assignment3.pdf) · [全部五份作业](index.html)

**⚠️ 排行榜不接受迟交天数，并将于 10 月 20 日（周二）晚 11:59 关闭。**

如果你在排行榜关闭时仍未提交，排行榜部分得 0 分。迟交天数仅适用于仓库和视频。

## 第 0 部分. 框架

### 两类容器

主智能体运行在**智能体容器**中，该容器由课程的 `dispatcher/agent.Dockerfile` 构建，并挂载你的 `src/`。主智能体循环从一开始就在这个容器中启动，记忆、子智能体以及其他功能也应存在于此。`starter_code` 文件夹以只读方式挂载到 `/madsOpt`，你的智能体只能写入其中两个位置：`.tasks/`（其工作目录）和 `madsOpt_logs/`（日志写入处）。它需要写入的其他任何内容（临时文件、缓存）都放在容器内的其他地方，例如 `/tmp`。

每个任务运行在**自己的任务容器**中，由该任务自己的镜像构建：仓库检出到任务的起始提交，并带有任务所需的工具链和测试依赖。这个容器承载你的智能体读取和修改的代码。某些 Go 任务需要修复中必须添加的模块。它们的任务容器带有预热好的模块缓存，并设置了 `GOPROXY=off`，因此 `go get <module>@<version>` 和 `go mod tidy` 可以离线工作。要查看可用内容，运行 `ls $(go env GOMODCACHE)/cache/download/<module>/@v/`。`evaluation_scripts/prepare_images.sh` 构建这些镜像，使任务可以离线解决。

你的智能体通过设施调度器（facility dispatcher）来启动任务、生成补丁并评估它。两个容器都无法访问互联网：智能体容器唯一的出口是通往课程 API 的出口代理，由 `CS2680_BASE_URL` 指向；任务容器则没有出口。

下图展示了各个组件运行在哪里，以及它们如何相互通信。

课程 API api.cs2680.com

宿主机

模型调用（HTTPS，经由出口代理）

智能体容器

智能体（你的 src/）
循环、提示词、工具、子智能体、记忆

调度器客户端（dispatcher/）
next\_task、extract\_patch、evaluate、done

任务容器 k
最多同时打开 5 个

sandbox\_server.py
:8000 上的 /health /exec /read /write

位于 /app 的仓库
处于任务的起始提交

HTTP POST
Sandbox(url, workdir)

设施 run\_all.py
响应调度器请求、
启动容器、保存判定结果

请求与
评估结果

启动和移除任务容器

评分容器
任务镜像的全新副本、
你的补丁，以及隐藏测试

evaluate(k)：你的补丁

失败测试数 / 总数

### 你的智能体如何访问任务

当你的智能体请求一个任务时，调度器启动任务容器，等待其就绪，并将一个包含任务规格和访问容器所需细节的 dict 交给你的智能体：

```
problem_statement, requirements, interface   # the issue and its specification
task                                         # the task index k
sandbox_url                                  # http://<container>:8000
workdir                                      # the repository path inside it, e.g. /app
```

一个极小的 HTTP 服务器（`src/sandbox_server.py`）运行在任务容器内，提供四条路由：`/health`、`/exec`（在仓库中运行 shell 命令并返回 stdout、stderr 和退出码）、`/read`（读取文件）、`/write`（写入文件）。你的智能体通过普通 HTTP POST 与它通信。`src/sandbox.py` 将它们包装为 `Sandbox(url, workdir)`，提供 `exec`、`read_text` 和 `write_text`；你的智能体对仓库的所有操作都通过这些调用完成。你可以为所需的任何功能添加路由（新工具、子智能体等）。不要用本地 `open()` 或 `subprocess` 触碰仓库：它们作用于智能体容器，而那里没有仓库。

### 接受评分，并决定下一步做什么

当你的智能体认为任务已解决时，它生成一个补丁并请设施为其评分：

```
dispatcher.extract_patch(k)        # `git diff` of the task container -> the task's patch folder
                                   # (or dispatcher.submit_patch(k, text) to write your own)
ev = dispatcher.evaluate(k)        # -> {"tests_failed": F, "tests_total": T, "attempt": a}
```

设施将补丁复制到任务镜像的全新副本上（带有同样预热好的 Go 模块缓存，且无网络），应用该任务的隐藏测试并运行，然后把测试总数和失败数发送给智能体。你的智能体随后在以下两者之间选择：

```
dispatcher.continue_task(k)   # keep working: the task container and your edits stay exactly as
                              # they are, the submitted patch is deleted, and you may call
                              # evaluate(k) again when you have a new one
dispatcher.done(k, reason, iterations)
                              # the task is final. Its last evaluation is its result; a patch you
                              # submitted but never evaluated is graded now; no patch counts as a
                              # failure. The task container and the patch folder are removed.
```

### 调度器执行的规则

* **最多同时存在 5 个任务。** 当已有 5 个打开时，`next_task()` 抛出 `DispatcherError`；没有剩余任务时返回 `None`。
* **每个任务一次只允许一次尝试。** 当 k 的评分仍在运行时，`continue_task(k)`、`evaluate(k)` 和 `done(k)` 会被拒绝。
* **评分有时间限制：35 分钟。** 挂起的测试套件按全部测试失败计算。
* **整个运行有时间限制：4 小时。** 计时从你的智能体打开第一个任务时开始。4 小时后运行停止：智能体下一次调用调度器时抛出 `DispatcherShutdown`，所有仍打开的任务按那一刻调用了 `done(k)` 来处理完成（最后一次评估计入；已提交但未评估的补丁会被评分；没有补丁算失败），从未打开过的任务算失败。已经开始的评分仍会完成。

### 入口点

```
class Agent:
    def __init__(self, dispatcher): ...
    def run(self): ...
```

运行器构造 `Agent(dispatcher)` 并调用 `run()`。此后由你决定流程：保持多少个任务打开、是否并行处理、何时评估、是否在一个失败的任务上再花一次尝试还是继续下一个，以及从一个任务带到下一个任务的内容。`src/agentic_loop.py` 中的起始 `Agent` 仅演示这些调用。它一次拿一个任务，且不做任何修复尝试，因此在你编写自己的实现之前，每个任务都会失败。

通过 `dispatcher.logger(k)` 记录模型调用和工具调用。排行榜从该 trace 中读取你的轮次数。

## 第 1 部分. 起始代码

### 先初始化你的仓库

将[作业 3 起始归档](assignment3.tar.gz)下载到你的共享私有课程仓库根目录，并在那里解压。它会创建 `assignment3/`，起始代码在 `assignment3/starter_code/` 中，包括 `init.sh` 和 `package_claude_sessions.py`。如果你已经从课程作业仓库复制了起始代码，请跳过这一步：将归档解压到你的 `assignment3/` 上会替换你已修改的文件。

```
# From your shared course repository:
tar -xzf assignment3.tar.gz
rm assignment3.tar.gz
```

**在开始使用 Claude Code 工作之前，运行 `init.sh`：**

```
# From your shared course repository:
bash assignment3/starter_code/init.sh
```

这会将 `package_claude_sessions.py` 复制到仓库根目录，并在那里创建 `CLAUDE.local.md`，其中包含适用于该仓库所有工作的流程。Claude Code 会将你的修改连同仓库的会话日志一起提交到仓库根目录的 `claude-sessions.tar.gz` 中。

### 其中有什么

初始化后，两个辅助文件都位于仓库根目录：

```
course-repository/
├── CLAUDE.local.md               repository workflow instructions for Claude Code
├── package_claude_sessions.py    session packager copied by init.sh
└── assignment3/
    └── starter_code/            starter files listed below
```

共享流程从仓库根目录运行 `python3 package_claude_sessions.py --path . --output claude-sessions.tar.gz`，以包含每份作业以及仓库其他工作的会话。对于作业 3 的提交，请在仓库根目录运行 `python3 package_claude_sessions.py`，生成 `assignment3/a3-sessions.tar.gz`。其余说明使用相对于 `assignment3/starter_code/` 的路径。

你可以修改 `src/` 下的任何内容并在其中添加功能。其余部分（`dispatcher/`、`madsOpt.py` 和 `evaluation_scripts/`）与排行榜使用的完全相同。唯一例外是 `dispatcher/student_name.json`，你在其中填写姓名（第 2 步）；在排行榜上则使用评分者自己的 session id。

```
assignment3/starter_code/
├── init.sh                      run first: copies the session packager and creates CLAUDE.local.md at the repository root
├── package_claude_sessions.py    packager source, copied to the repository root by init.sh
├── src/                          YOURS: everything here may change (the leaderboard takes only src/)
│   ├── agentic_loop.py           class Agent (your entry point): a starter showing every dispatcher, sandbox, model and trace call
│   ├── config.py                 your harness settings (the course API settings are environment variables, see Step 2)
│   ├── sandbox.py                Sandbox(url, workdir): exec / read_text / write_text over HTTP
│   └── sandbox_server.py         the HTTP server inside every task container (run_all.py needs its GET /health)
├── dispatcher/                   course infrastructure
│   ├── dispatcher.py             Dispatcher, the client your Agent calls: next_task, extract_patch / submit_patch, evaluate, continue_task, done, logger
│   ├── egress_proxy.py           the reverse proxy to the course API: the agent container's only way out
│   ├── session.py                the run's session id, sent with every course API request
│   ├── student_name.json         your first and last name, filled in once (see Step 2)
│   └── agent.Dockerfile          the agent container image (python + openai, built offline)
├── madsOpt.py                    course infrastructure: builds the client and calls Agent(...).run()
└── evaluation_scripts/
    ├── prepare_images.sh         one-time setup (needs internet)
    ├── run_all.py                runs your agent on all tasks and grades them
    ├── evaluate_one.sh           grades one patch on a pristine task container
    ├── make_predictions.py       collects the final patches into predictions.json
    ├── trace_logger.py           the JSONL trace your agent writes through dispatcher.logger(k)
    ├── agent_task_input.json     the tasks
    └── task_test.json            the tests each task is graded with
```

### 运行它

**第 0 步. 前置条件。** Linux x86\_64；Docker；`git`；带 `pip` 的 `python3`（3.10+）；约 15 GB 空闲磁盘用于镜像。如果你在本地机器上遇到困难，可以使用 [CloudLab](../computing/cloudlab.html) 机器或 [AWS](../computing/aws.html) 机器。

```
# only if Docker is not installed:
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
newgrp docker            # or log out and back in
docker run hello-world   # check that it works

# only if python3 has no pip ("No module named pip"):
sudo apt update
sudo apt install python3-pip
```

**第 1 步. 配置镜像。**

```
# From your shared course repository:
cd assignment3/starter_code
bash evaluation_scripts/prepare_images.sh
```

该脚本获取任务数据（SWE-bench Pro，固定提交）、为任务容器安装便携式 Python、下载 openai wheel、拉取每个任务的镜像、构建智能体镜像，并为每个需要额外包的 Go 任务构建预热镜像。成功构建以 `== all images present` 结束。

**第 2 步. 设置环境变量并测试。**

```
export CS2680_API_KEY=...
export CS2680_MODEL_EXPERT=expert        # Expert: most capable model; per 1M tokens: $2.00 input, $0.10 cached input, $10.00 output
export CS2680_MODEL_STANDARD=standard    # Standard: per 1M tokens: $0.08 input, $0.004 cached input, $0.28 output
export CS2680_MODEL_STARTER=starter      # Starter: cheapest model; per 1M tokens: $0.01 input, $0.0005 cached input, $0.04 output
python3 evaluation_scripts/run_all.py --limit 0
```

`run_all.py` 将每个 `CS2680_*` 变量传入智能体容器，并将 `CS2680_BASE_URL` 设置为出口代理——智能体访问课程 API 的唯一途径。你的智能体用 `os.environ` 读取它们；绝不要硬编码 API URL。它在一次运行中可以使用三个模型中的任意一个，也可以任意多地使用它们。

该命令启动智能体容器和代理，检查网络规则（课程 API 可访问，其他一切被阻断），启动并对每个任务容器做健康检查，然后停止，不运行你的智能体。请查找 `EGRESS OK`，以及每个任务的 `preflight k: ... ok`。

第一次在终端运行 `run_all.py` 时，它会询问你的名和姓（拉丁字母），并保存到 `dispatcher/student_name.json`。此后一次运行的每个课程 API 请求都会携带 session id `<First>_<Last>_<UTC start time>`，例如 `Jane_Doe_20261006T172408Z`，由出口代理添加；运行会打印它，并保存在 `run_logs/session_id` 中。如果你在没有终端的情况下运行（例如使用 `nohup`），请先填写该文件，否则运行会在启动任何内容之前退出。

**第 3 步. 运行它。**

```
python3 evaluation_scripts/run_all.py
```

进度写入 `run_logs/sequence.log`。运行结束后，`starter_code` 中包含 `run_all_results.md`（例如 `3/5 passed`）、`pro_eval/`（评分器对每个任务的输出）、`model_patch_<k>.diff` 和 `madsOpt_logs/<k>/run.jsonl`（你的智能体 trace）。起始智能体只是一个骨架，不做任何修复，因此预期它得到 `0/5 passed`。在下一次运行之前，将上一次运行的输出归档到另一个文件夹。

## 第 2 部分. 排行榜提交

排行榜使用与起始代码相同的 `dispatcher/`、`madsOpt.py` 和 `evaluation_scripts/`，在评估任务集上为你的 `src/` 评分。它只从你上传的内容中取 `src/`。排行榜地址：<https://leaderboard.cs2680.com/>

**第 1 步. 登录并修改密码。** 在排行榜页面上，使用与你的 Canvas 账号关联的哈佛邮箱登录。初始密码为 Cs2680-<你的 8 位学号>；这与你的 API 账号的初始登录凭据相同。登录后，点击你的姓名，从下拉菜单中选择 `Change Password`。

**第 2 步. 排行榜。** 登录后，`Leaderboard` 页面显示前 10 名学生（每人以最佳提交代表），下方显示你自己的最佳提交及其名次。评分一结束排行榜就会更新。

**第 3 步. 提交。** 在 Submit 页面，上传 `src/` 文件夹的 zip，并选择本次运行最多可评分的任务数。运行会取评估集的前 *k* 个任务，如果留空则取全部。

**第 4 步. 提交如何衡量。** 每次提交按三个指标评估：

* 解决的任务数，
* 每个已解决任务的成本（运行期间课程 API 账号被收取的费用除以解决的任务数），
* 每个已解决任务的时间（端到端实际时间，从打开第一个任务到完成最后一个任务，除以解决的任务数）。

**第 5 步. 过往提交、取消与每日预算。** Past submissions 页面列出你正在进行和过往的提交。你最多可以有一个提交在排队或评分，该提交带有 **Cancel** 按钮。每名学生每天有 **30 美元**用于排行榜评分，每次提交上限为 **10 美元**。如果评分达到任一上限就会停止，届时已完成的部分将作为该提交的结果记录。

* 取消仍在**排队**中的提交会将其从队列中移除，不产生费用。
* 取消**正在评分**的提交会停止运行。到目前为止的费用从你当天的 30 美元中扣除，该提交以取消时刻的三个指标记录。

**第 6 步. 排名：天际线。** 每名学生按最佳提交排名。

* 解决**至少 7 个任务**的最佳提交按三个指标划分天际线层级。如果一份提交在所有三个指标上都不差于另一份，且至少在一个指标上更好，则前者支配后者。第 1 名是所有未被任何其他提交支配的提交；第 2 名对剩余提交应用相同规则，依此类推。
* 解决任务少于 7 个的最佳提交排在这些提交之下，仅按解决任务数排序。
* 相同名次为并列，下一名次计入其前面的所有人：1、1、1、4、……
* 新提交只有在排名严格优于你当前最佳时才会成为你的最佳提交。并列时保留当前最佳。

### 关于排行榜提交的更多信息

* **排行榜有 26 个任务**，编号 1 到 26（如果你在 Submit 页面设置了任务数，则只有前 *k* 个）。
* **一次运行在 4 小时处截断**，从你的智能体打开第一个任务时开始计时（见第 0 部分的规则）。
* **崩溃或超时的运行仍然计入**，以其届时完成的任务计。Past submissions 页面还显示每次提交的逐任务结果，编号 1 到 26：每个任务的时间和轮次数，以及每个未解决任务的简短原因：
  + *not opened*：你的智能体从未请求该任务，或运行时间先耗尽；
  + *not finished*：任务打开期间运行崩溃或超时；
  + *no patch*：任务以空补丁结束；
  + *tests did not run*：评分未产生测试结果；
  + *import error*：测试无法收集（例如导入或语法错误）；
  + *broke existing tests*：补丁之前通过的测试现在失败；
  + *new tests failed*：修复本应使其通过的测试仍然失败（一个任务可能同时显示最后两项）。
* **美元成本在评分期间受到检查。** 评分器每 2 分钟汇总一次运行到目前为止的花费。如果达到你当天剩余预算，评分停止并保存为 `Reached the budget`，以届时已完成的部分计。

## 第 3 部分. 提交与评分

### 提交

提交包含三部分：**代码**（排行榜上的 `src/`）、一份**书面报告**和一段**视频**。

#### 代码

将 `assignment3/starter_code/src/` 打包为 zip，并在排行榜的 Submit 页面上传 `src.zip`（第 2 部分第 3 步）：

```
# Run from assignment3/starter_code/:
zip -r src.zip src
```

另外，按[每份作业需提交的内容](../computing/claude-code.html#export)所述归档你的 Claude Code 会话文件，并将其提交到仓库的 `assignment3/`。检查你的 `.gitignore` 没有排除该归档。与每份作业一样，会话文件本身不计分。它们是书面报告中各项主张背后的记录。

#### 书面报告

一份回答以下问题的 PDF 文档：

1. **你的 harness 的主要组件是什么？** 例如子智能体、从一个任务带到下一个任务的记忆，或哪个模型层级负责什么。
2. **你做了哪些优化和权衡？** 例如继续处理失败任务还是放弃的策略，或你同时保持多少个任务打开。
3. **你遇到了哪些陷阱，什么起了帮助？** 描述这些陷阱，以及你认为什么帮助提升了准确率（解决的任务数）、每个已解决任务的成本或每个已解决任务的时间。

书面报告必须完全是你自己的工作，不得包含 AI 生成的文字。将其提交到仓库的 `assignment3/writeup.pdf`。仓库中的 `assignment3/` 应包含：

```
assignment3/
├── starter_code/         your agent code and local run outputs
├── a3-sessions.tar.gz    your Claude Code session files
└── writeup.pdf           the write-up
```

#### 视频

在视频中，露脸并用你自己的声音讲解同样的经验教训。打开你的代码并移动光标浏览，同时导航你的 harness：展示书面报告中每个组件所在的位置，以及陷阱和有帮助的技术。在 Canvas 上提交视频。

### 评分

| 部分 | 分数 | 评分内容 |
| --- | --- | --- |
| 排行榜 | **80** | 你最佳提交在排行榜上的名次（第 2 部分第 6 步），按下述方式计分。 |
| 书面报告 | **10** | 你从作业中学到的经验教训，在一页内清晰解释。 |
| 视频 | **10** | 对同样经验教训的清晰 3 分钟展示，当某条经验涉及你的 harness 时展示相应代码。 |

**排行榜得分。** 设 *r* 为你最佳提交的名次：

```
score = max(81 − r, 50)    if any of your submissions achieves the baseline
score = 81 − r             otherwise
```

**基线**在 4 小时内、10 美元限额内解决 16 个任务。如果你的任何提交达到基线，你就会获得相应分数，即使该提交不是你的最佳提交。例如，第 1 名得 80 分；第 12 名无论是否超过基线都得 69 分；第 40 名如果超过基线得 50 分，否则得 41 分。

#### 加分

如果你发现安全漏洞并报告，可获得最多 3 个加分点，计入最终课程成绩（不仅限于本次作业）。滥用漏洞会导致本次提交作废。

[← 作业 2 — 构建智能体 harness](assignment2.html)
[作业 4 — Mads-Serve：拥有模型 →](assignment4.html)
