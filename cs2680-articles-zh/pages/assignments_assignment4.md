---
title: "作业 4 — Mads-Serve：拥有模型（20%）"
title_en: "Assignment 4 — Mads-Serve: own the model(20%)"
source: https://cs2680.seas.harvard.edu/assignments/assignment4.html
crawled: 2026-11-16
translated: 2026-11-16
---

# 作业 4 — Mads-Serve：拥有模型（20%）

> 原文：[Assignment 4 — Mads-Serve: own the model(20%)](https://cs2680.seas.harvard.edu/assignments/assignment4.html) · Harvard CS2680

CS2680 现代 AI 系统：智能体与系统优化（CS2680 Modern AI Systems: Agents and System Optimizations）

作业 4 — Mads-Serve：拥有模型

# 作业 4 — Mads-Serve：拥有模型（20%）

**发布** 10 月 21 日（周三） · **截止** 11 月 10 日（周二）晚 11:59 · 个人作业 · [幻灯片](../slides/assignment4.pdf) · [全部五份作业](index.html)

在作业 3 中，你的智能体通过课程 API 调用模型。在本作业中，你在**一块 RTX PRO 4500（32 GB）**上自行提供模型服务，让你的作业 3 智能体指向它，然后通过修改服务引擎或智能体来让它更快。

**⚠️ 一次只能使用一块 RTX PRO 4500。**

课程的 GPU 资源有限，由全班共享，因此请为同学留出足够的资源。你一次最多只能在一块 GPU 上运行。如果被发现使用多于一块 GPU，你会收到警告，此后每次违规将扣除本作业成绩的 10%。排行榜评分在单独的 GPU 上运行，不计入此限制。

**⚠️ 排行榜不接受迟交天数，并于 11 月 10 日（周二）美东时间晚 11:59 停止接收提交。**

上传在晚 11:59 之前开始的 zip 会被接受并评分，即使上传在晚 11:59 之后完成。请保持 Submit 页面打开，直到它显示 zip 已提交。届时提交的作业仍会被评分并计入，即使评分稍后完成。如果届时没有排行榜提交，你在 60 个排行榜分数中得 0 分。迟交天数仅适用于书面报告和视频。

## 先初始化你的仓库

在用于作业 3 的机器上，将[作业 4 起始归档](assignment4.tar.gz)下载到你的共享私有课程仓库根目录，并在那里解压。它会创建 `assignment4/`，起始代码在 `assignment4/starter_code/` 中。

```
# From your shared course repository:
tar -xzf assignment4.tar.gz
rm assignment4.tar.gz
```

**在开始使用 Claude Code 工作之前，运行 `init.sh`：**

```
# From your shared course repository:
bash assignment4/starter_code/init.sh
```

这会将 `package_agent_sessions.py` 复制到仓库根目录，并在那里写入 `CLAUDE.local.md` 以替换作业 3 的版本，使 Claude Code 将你的修改连同仓库的会话日志（Claude Code、Cursor 和 Codex）一起提交到仓库根目录的 `agent-sessions.tar.gz` 中。提交时你需要再运行一次打包器（[第 4 部分](#part-4-submission-and-grading)）。

## 第 1 部分. 运行基本 SGLang 配置

如果你此前没有使用过课程集群，请先在 HPC 页面完成[首次配置](../computing/cluster.html#first-time)。下面有些步骤在登录节点上运行一次，已作标注。其余步骤在你 GPU 节点上的 screen 会话中运行。

### 在 GPU 节点上启动作业

从登录节点（`ssh cs2680`）在一个 RTX PRO 4500 节点上启动作业，其中包含一个 `screen` 会话，并附加到该会话：

```
sbatch -p gpu-g7-reserved --gres=gpu:rtxpro4500:1 -c 8 --mem=28G -t 4:00:00 -J work -o /dev/null --wrap 'screen -dmS work; while screen -ls work | grep -q "\.work"; do sleep 30; done'
squeue -u $USER --name=work                 # wait for state R, and note the JOBID
srun --jobid=<JOBID> --overlap --pty screen -r work
```

刚关机的节点大约需要 4 分钟启动（状态 `CF`）。如果你的连接断开，screen 会话会继续运行。按 `Ctrl-a d` 分离，再次运行 `srun` 那行即可重新附加。作业在 4 小时后结束，或者当你在登录节点运行 `scancel <JOBID>` 时结束。完成后请结束它，因为你一次只能持有一块 GPU。HPC 页面在[在 GPU 节点上提供模型服务](../computing/cluster.html#serving)中解释了这些命令。

### 配置环境变量

在登录节点上一次性为你的服务器创建密码。你的智能体在每次请求中都会发送它，没有它的人无法使用你的 GPU：

```
mkdir -p ~/a4/engine && (umask 077 && openssl rand -hex 16 > ~/a4/serve.key)
```

然后在你为本作业使用的每个新 shell 中设置这两个变量，无论是在登录节点还是每个 GPU 作业中（新的 screen 窗口也是新的 shell）。下面的命令会用到它们：

```
export A4=/shared/courseSharedFolders/176914outer/176914/a4   # the course environment
export SERVE_KEY=$(cat ~/a4/serve.key)                       # your server's password
```

### 配置 SGLang

`$A4` 中的课程环境包含 SGLang 的依赖、用于运行时编译内核的 CUDA 工具链，以及课程模型（Qwen3.6-35B-A3B NVFP4）的权重。基本 SGLang 配置使用 FlashInfer 的原生 FP4 内核运行该 checkpoint 的 FP4 专家层，这些内核在课程环境中已预构建。SGLang 本身是你自己的克隆，因此你可以修改它。在登录节点上一次性执行：

```
git clone --depth 1 --branch v0.5.20 https://github.com/sgl-project/sglang.git ~/a4/sglang
git -C ~/a4/sglang switch -c a4                  # a branch for your commits
cp $A4/basic-sglang-flags.txt ~/a4/engine/flags.txt
git config --global user.name "Your Name"        # once, if you have not set these on the cluster
git config --global user.email "your Harvard email"
```

然后，在 GPU 节点上的每个作业中：

```
bash $A4/bin/setup.sh
```

`setup.sh` 在节点的本地磁盘上构建环境，并以 `setup finished` 结束。在刚启动的节点上约需 **5 分钟**，在已运行过它的节点上约需 30 秒。

环境详情

环境为 Python 3.12，带有 PyTorch 2.13、FlashInfer 0.6.18 和 sgl-kernel 0.4.7，以及 CUDA 13.4 工具链。`setup.sh` 在节点上安装 Python 包，并通过 SGLang 使用的每个编译器编译一个测试内核。它不复制权重：服务器从 `$A4/hf` 读取它们。环境位于节点自身磁盘上的 `/local_scratch/$USER/a4`，只有你能读取。在 10 月 29 日集群变更之前启动的节点没有 `/local_scratch`，因此在那种节点上环境位于 `/var/tmp/$USER-a4`。如果 `serve.sh` 提示课程环境未配置好，请再次运行 `setup.sh`。这发生在你在 10 月 29 日课程的脚本迁移环境之前运行过 `setup.sh` 的作业中。每个节点有自己的磁盘，因此在另一个节点上的作业需要再次运行 `setup.sh`。如果其他学生的文件占满了节点磁盘，`setup.sh` 会使用 `$A4/venvs` 中共享的包副本，而不是安装它们，并打印一条提示。一切工作方式相同，但每次启动服务器会多花约 2–5 分钟，因为包通过网络加载。克隆时可能打印 `warning: refs/tags/v0.5.20 ... is not a commit!`，这无害。

### 启动服务器

```
bash $A4/bin/serve.sh > ~/a4/server.log 2>&1 & tail -f ~/a4/server.log   # Ctrl-c stops watching; the server keeps running
```

等待日志打印出这一行。在节点上的首次启动约需 **6 分钟**，在同一节点上重启约需 1.5 分钟。

```
[2026-10-15 19:17:00] The server is fired up and ready to roll!
```

然后按 `Ctrl-c` 停止查看，并检查服务器。`smoke.py` 会检查你的智能体依赖的七项内容，以 `7/7 passed` 结束：

```
python3 $A4/bin/smoke.py http://127.0.0.1:30000 $SERVE_KEY
```

要尝试修改，请编辑 `flags.txt` 或你的克隆，在启动它的 shell 中用 `kill %1` 停止服务器，然后再次运行 `serve.sh` 那一行。排行榜不运行 `serve.sh`，而是运行你的 `engine/launch.sh`（[第 4 部分](#part-4-submission-and-grading)），起始模板中的该脚本使用相同的 `flags.txt` 启动 SGLang。

**在退出作业之前**，停止服务器并运行 `bash $A4/bin/cleanup.sh`。它会从节点上删除你的环境副本。没有其他东西会删除它。它会一直保留到节点关闭，即使你的作业达到时间限制或用 `scancel` 结束。你的副本约占 20 GB。在有 `/local_scratch` 的节点上，它位于一个约 400 GB 的磁盘中。在没有该目录的节点上，它位于 `/var/tmp`，该目录为节点上的每个作业提供 66 GB，因此三个学生的副本就会把它占满。`cleanup.sh` 还会删除旧版 `setup.sh` 在节点 `/var/tmp` 中创建的副本。

服务器配置

`serve.sh` 从 `~/a4/sglang` 启动 SGLang，使用 `~/a4/engine/flags.txt` 中的标志，随后是课程设置的标志：`--model-path nvidia/Qwen3.6-35B-A3B-NVFP4 --served-model-name qwen3.6-35b-a3b-fp4 --host 0.0.0.0 --port 30000 --api-key $SERVE_KEY`。在首次启动的 8 分钟中，约 3 分钟用于加载权重，约 3 分钟用于 FlashInfer 为该卡调优内核。

你可以修改 `flags.txt` 中基本 SGLang 配置的任何标志。你的标志不能设置模型路径、服务模型名、地址、key 或 GPU 数量，因为 `serve.sh` 和排行榜会设置它们，也不能使用 `--config`，因为它也可能设置这些。该配置中有三个标志需要小心：

* `--moe-runner-backend` 是使用 SGLang 服务 Qwen3.6-35B-A3B NVFP4 所必需的。没有它，启动会以 `NotImplementedError` 失败。
* `--mamba-ssm-dtype bfloat16` 以低于 checkpoint 指定的精度存储线性注意力层的状态。它属于模型数值行为的一部分，因此修改它可能改变模型能解决多少任务。
* `--reasoning-parser` 和 `--tool-call-parser` 填充你的智能体读取的 `reasoning_content` 和 `tool_calls` 字段，`--enable-metrics` 和 `--enable-cache-report` 让服务器报告更多关于其工作的信息。

运行你自己的脚本

集群没有安装 SGLang 的包或 CUDA 工具链，因此课程将它们作为环境提供。课程环境是一个 Nix 环境，`setup.sh` 将其解包到节点的本地磁盘上，程序只有通过 `nix-portable` 启动时才能看到它，`serve.sh` 为服务器执行了这一步。节点上的普通 shell 则看不到，因此那里的 `python` 找不到 `torch` 或 `sglang`。要运行你自己的脚本（例如 `python -m sglang.bench_serving`），请先在该环境中打开一个 shell：

```
source $A4/bin/np.sh && a4sh bash --norc
export PYTHONPATH=~/a4/sglang/python HF_HOME=$A4/hf HF_HUB_OFFLINE=1 OPENAI_API_KEY=$SERVE_KEY
```

诸如 `sglang.bench_serving` 的客户端会发送 `OPENAI_API_KEY` 中的 key；没有它就会得到 `401`，并报告服务器未就绪。`HF_HUB_OFFLINE=1` 使脚本从 `$A4/hf` 中课程的副本加载模型文件，同时也会阻止从 Hugging Face Hub 下载，因此在必须下载数据集的 shell 中请不要设置它。

常见问题

| 日志显示 | 解决方法 |
| --- | --- |
| `NotImplementedError ... Use --moe-runner-backend flashinfer_cutlass instead` | 添加 `--moe-runner-backend flashinfer_cutlass`，基本标志中已如此。 |
| `setup.sh` 打印 `this node uses the course's shared copy` | 其他学生的文件占满了该节点磁盘，因此 `setup.sh` 使用了共享的包副本。一切正常，但每次启动服务器会多花约 2–5 分钟。要加快启动，请换到另一个节点（下一行）。 |
| `setup.sh` 打印 `only NG free on <node>, and setup needs MG` | 节点磁盘已满。如果这些文件是你早先作业留下的，请运行 `bash $A4/bin/cleanup.sh`，然后再次运行 `setup.sh`。否则，结束作业（在登录节点运行 `scancel <JOBID>`），并用 `--exclude=<node>` 重新提交 `sbatch` 那行（多个节点用 `--exclude=<node1>,<node2>`）。`setup.sh` 在第一行打印节点名。 |
| `np.sh: run this inside a Slurm job on a GPU node` | 你位于登录节点。请先在 `gpu-g7-reserved` 上启动作业。 |
| 自己的脚本中出现 `No module named 'sglang'`（或 `'torch'`） | 该 shell 没有环境。按上面的方式用 `source $A4/bin/np.sh && a4sh bash --norc` 打开一个。 |
| 启动或 CUDA graph 捕获期间出现 `CUDA out of memory` | 你的标志使用了超过该卡容量的 GPU 内存。撤销使用该内存的修改。 |

### 连接你的智能体

你的智能体及其任务容器需要 Docker，而集群没有 Docker，因此它们运行在你用于作业 3 的机器上。该机器必须位于哈佛网络或哈佛大学 VPN 上才能访问集群。`assignment4/starter_code/` 中的起始代码（[先解压并初始化](#initialize-your-repository)）是作业 3 的框架，带有 25 个新任务，并以你的服务器替代课程 API，其调度器不再限制同时存在的任务数量。将你的作业 3 `src/` 复制覆盖它的 `src/`。出口代理运行在容器中，无法访问你机器的 `localhost`，因此在 Docker 网桥地址（通常是 `172.17.0.1`）上打开到 GPU 节点的 [SSH 隧道](../computing/cluster.html#tunnel)，并将 harness 指向它（从 CloudLab 或 AWS 机器上，按 HPC 页面[从 CloudLab 或 AWS 访问集群](../computing/cluster.html#cloudlab-aws)所述打开隧道）：

```
cd assignment4/starter_code                           # from your course repository; the rest runs here
ssh -f -N -o ExitOnForwardFailure=yes -L 172.17.0.1:30000:<node>:30000 cs2680
export A3_API_UPSTREAM=http://172.17.0.1:30000
export CS2680_API_KEY=$(ssh cs2680 cat a4/serve.key)   # the same key as your server
export CS2680_MODEL_EXPERT=qwen3.6-35b-a3b-fp4 CS2680_MODEL_STANDARD=qwen3.6-35b-a3b-fp4 CS2680_MODEL_STARTER=qwen3.6-35b-a3b-fp4
bash evaluation_scripts/prepare_images.sh             # once: about 40 GB to download
python3 evaluation_scripts/run_all.py --limit 0       # preflight: look for EGRESS OK
```

本作业不提供课程 API 及其三个模型（starter、standard 和 expert）。所有模型调用都指向你服务的模型，因此上面三个模型变量都指向它。预检会确认你的服务器接受你的 key 并提供该模型的服务。起始代码的 `README.md` 列出了你的机器所需的磁盘、CPU 和内存，以及预检失败意味着什么。

## 第 2 部分. 测量你的起始运行

在基本 SGLang 配置下，让作业 3 的智能体运行这 25 个任务，从一开始就保持全部 25 个任务打开。服务器日志和智能体日志会随运行写入，但服务器的 `/metrics` 端点只在你读取的那一刻显示其计数器和度量值，因此在运行期间要定期读取（例如每 10 秒用 `curl`），并保留每一次读数。

记录排行榜评分的两个数字：解决的任务数，以及从运行开始（服务器已就绪）到最后一个任务完成的端到端时间。你的智能体同时处理所有任务，因此这就是完成整个任务集的时间。

然后找出时间花在哪里。根据服务器日志、`/metrics` 读数和智能体日志，测量解释起始运行端到端时间所需的一切，并绘制整个运行期间的变化。

同时针对同一个服务器运行 SGLang 的服务基准测试 `python -m sglang.bench_serving`。选择其设置，尽可能准确地描述你的智能体工作负载，将其报告与你在起始运行中测得的结果进行比较，并保留两者。

## 第 3 部分. 让服务更高效

**让服务器更快地服务你的智能体**，从而让智能体用更少时间解决任务集。分三步进行：

1. **找原因。** 使用第 2 部分的测量找出是什么限制了速度。
2. **列出修复方案。** 指出可消除原因的对引擎或智能体的修改，并预测每项修改的作用。
3. **尝试。** 实现最有希望的方案，并测量每项带来的帮助。

一次只改一处，在与你起始运行相同的任务上测量，并保留你报告的每次运行的日志。

**边做边记录每项修改。** 每次尝试修改时，即使没有帮助，也要将其加入书面报告中的[优化表格或列表](#write-up)。

### 允许的修改

* **引擎。** SGLang 或 vLLM——课程环境提供的两个框架——可对其源代码做任何修改，并可使用任何设置。要使用 vLLM 0.31.0，请遵循排行榜引擎约定页面上的 [Using vLLM](https://leaderboard.cs2680.com/a4/engines.html#vllm)，该说明会克隆 vLLM、在节点上用 `bash $A4/bin/setup.sh --vllm` 安装，并将 `$A4/basic-vllm-flags.txt` 放到你的 `flags.txt` 位置；当 `~/a4/engine/engine.json` 指定 `vllm` 时，`serve.sh` 会启动 vLLM。提前编译的内核（SGLang 的 `sgl-kernel`、vLLM 的 C++ 和 CUDA 扩展）无法在课程节点上重新构建，因此补丁只能修改 SGLang 的 `python/sglang/` 下文件（不含 `python/sglang/kernels/aot/`），或 vLLM 的 `vllm/` 下文件；运行时编译的内核可以修改。你也可以自行承担风险使用其他服务框架。将其构建到你自己的环境文件夹中，并将引擎命名为 `other`，如引擎约定页面 [Your own engine](https://leaderboard.cs2680.com/a4/engines.html#own-engine) 所述。课程不解决其他框架的问题。该页面列出了所有引擎的约定。
* **智能体。** 它如何使用服务器。

**不得修改模型。** 保持 `engine.json` 中的模型与起始代码一致，不要在引擎加载权重时转换它们（例如使用 `--quantization` 或 `--dtype`）。允许引擎设置，例如 KV 缓存的数据类型；投机解码可以使用模型自己的多 token 预测头，但不能使用单独的草稿模型。

你的服务器在一张 GPU 上运行。你不得修改任务集、调度器或评估脚本，也不得将模型调用发送到你的服务器之外的任何地方。

### 作弊

作业 3 的规则适用：不得使用 gold patch 或隐藏测试，不得为特定任务或仓库编写任何内容，不得利用离线运行评估任务所学到的内容。这些规则同样适用于引擎：引擎不得识别任务或提示词，不得预置从任务预计算出的响应或任何其他状态，不得在两次评分运行之间保留状态。通过在任务上测量来调优通用设置（例如服务器标志）是允许的。违规会使提交作废。如果你不确定某项修改是否允许，请在提交前发邮件询问我们。

## 第 4 部分. 提交与评分

提交包含三部分，与作业 3 相同。

* **代码。** 你的智能体放在 `src/`，服务器放在 `engine/`。起始代码的 `engine/` 是基本 SGLang 配置：
  + `engine.json`：框架（`sglang`、`vllm`，或带 `"env"` 中自建环境文件夹的 `other`）和模型（不要修改）；
  + `flags.txt`：`$A4/basic-sglang-flags.txt` 的副本；
  + `launch.sh`：启动服务器的脚本，其唯一有效行是 `exec a4-serve --flags-file "$A4_ENGINE_DIR/flags.txt"`；
  + `sglang.patch`，仅当修改了 SGLang 时需要：你克隆相对于 v0.5.20 的修改，无论是否提交，由 `git -C ~/a4/sglang add -A python/sglang && git -C ~/a4/sglang diff --no-renames v0.5.20 -- python/sglang > ~/a4/engine/sglang.patch` 写出（对于 vLLM 为 `vllm.patch`，如引擎约定页面所示）。将 `engine/` 与 `src/` 一起打包为 `submission.zip`，并在排行榜的 Submit 页面上传。另外在仓库根目录运行 `python3 package_agent_sessions.py`，它会将你的 Claude Code、Cursor 和 Codex 会话写入 `assignment4/a4-sessions.tar.gz`。
* **书面报告。** `writeup.md`，用你自己的话写，不得包含 AI 生成的文字。按以下顺序涵盖四件事：
  1. 是什么限制了你的起始运行，以及你如何发现；
  2. 将 SGLang 的服务基准测试与你的智能体运行比较时，你发现了什么；
  3. 你的优化表格或列表，每项尝试的修改对应一条，包括没有帮助的条目，每条包含：
     + *修改*：你改了什么；
     + *观察*：导致该修改的测量及其数字；
     + *推理*：你为什么预期该修改会有帮助，以及你预测它会带来什么效果；
     + *结果*：你测得的结果，与其前一次运行比较，并给出日志中的数字；
  4. 你学到的经验教训。
* **视频。** 用 **3 分钟**讲解同样内容，露脸并用你自己的声音，对任何依赖日志或 `/metrics` 的主张展示相应材料。上传到 Canvas。

```
assignment4/
├── starter_code/
│   ├── src/              your agent
│   └── engine/           engine.json, flags.txt, launch.sh, and your patch if you made one
├── a4-sessions.tar.gz    your agent session files
└── writeup.md            the write-up
```

排行榜用 bash 运行 `launch.sh`，以替代 `serve.sh` 或你自己的批处理脚本，因此其中的 `#SBATCH` 行不起作用。它在课程沙箱内运行，沙箱没有网络。沙箱隐藏 `/shared`、`/scratch` 以及每个主目录。只有 `/shared` 上课程的权重和 Python 包仍可见，且为只读。因此，调用 `$A4/bin/serve.sh` 或读取 `~/a4` 的 `launch.sh` 在那里会失败。沙箱将课程的 `a4-serve` 放入 `PATH`，并向 `launch.sh` 提供其注释中列出的变量。你的服务器必须监听 `127.0.0.1:$A4_PORT`，对每个请求要求 `$A4_KEY_FILE` 中的 key（只有 `/health` 和 `/metrics` 可以不带 key 应答），提供一个名为 `$A4_SERVED_MODEL_NAME` 的模型，并在评分作业开始后 45 分钟内应答。

**提交之前**，按排行榜运行它的方式测试你的 `engine/`。将其放到集群上的 `~/a4/engine`（起始代码的 `README.md` 说明了做法），停止你自己的服务器，并在 `setup.sh` 之后于 GPU 节点上的作业中运行以下命令（vLLM 用 `setup.sh --vllm`，`other` 用 `setup.sh --weights-only`）：

```
bash $A4/bin/check-submission.sh --launch
```

它会按排行榜规则检查 `engine/`，在课程沙箱中像评分一样从它启动你的服务器，并打印 `PASS` 或 `FAIL` 以及服务器日志末尾。使用起始模板时约需 5 分钟。在排行榜上启动失败的服务器仍会占用你当天 3 次评分中的一次。

### 排行榜

排行榜在全新的 RTX PRO 4500 节点上从 `engine/` 启动你的服务器，等待其就绪，然后从 `src/` 在评估集上运行你的智能体，使用与起始代码相同的 `dispatcher/`、`madsServe.py` 和评估脚本，并以评估集的 26 个任务替代起始代码的 25 个任务。排行榜地址：<https://leaderboard.cs2680.com/>，使用作业 3 的账号登录。其 `Leaderboard` 页面按最佳提交显示前 10 名学生，并显示你自己的最佳提交及其名次。

下图跟踪一次提交，从上传到运行结束。你的服务器在无网络的课程沙箱中运行，智能体的模型调用只到达你的服务器，端到端时间从服务器就绪到最后一个任务完成。

submission.zip
src/ 你的智能体
engine/ 你的服务器

Submit 页面

队列
每名学生一个，
每天 3 次评分

有 GPU 空闲

RTX PRO 4500 节点
每次评分使用全新节点

课程沙箱，无网络

engine/launch.sh
启动你的服务器

你的服务器
启动上限：45 分钟

src/
智能体容器

你的智能体（src/）

dispatcher/、madsServe.py
与起始代码相同

模型调用
仅发往你的服务器

一个智能体打开全部 26 个任务

任务容器 k
k = 1 到 26
任务的仓库，
打开数量不限

评分容器
测试时间限制：35 分钟
任务镜像的全新副本、
你的补丁，以及隐藏测试
等待，然后服务器启动

不计入
端到端时间，最多 4 小时
计时开始：服务器就绪
计时结束：最后一个任务完成

**限制。**

* **等待 GPU：无限制。** 评分会等到有 RTX PRO 4500 节点空闲。等待时间不计入任何限制，也不计入你的得分。
* **服务器启动：45 分钟**，从评分作业开始到你的服务器应答，包括任何安装。届时未就绪的服务器会导致评分失败，Past submissions 页面会显示其日志末尾。这段时间不计入你的得分。
* **运行：4 小时**，从你的服务器就绪时开始计时，端到端时间也从此时开始。4 小时后运行停止：所有仍打开的任务按智能体调用了 `done` 完成，从未打开的任务算失败，截断之后的时间不计入。
* **同时存在的任务：无限制。** 你的智能体可以在开始时打开所有任务。
* **补丁评分：35 分钟。** 挂起的测试套件按全部测试失败计算。
* **提交：一次一个排队或评分中，每天 3 次评分**（第 3 步）。因课程方问题导致的评分失败不计入。

**第 1 步. 提交。** 在 Submit 页面上传 `submission.zip`。每次评分运行评估集的全部 26 个任务。

**第 2 步. 指标。** 每次提交按两个指标评估：

* 解决的任务数，
* 端到端时间，从你的服务器就绪到最后一个任务完成，最多 4 小时。

**第 3 步. 过往提交与取消。** Past submissions 页面列出你正在进行和过往的提交。你最多可以有一个提交在排队或评分中，每天最多 **3 次评分**（美东时间午夜至午夜）。排队中或评分中的提交带有 **Cancel** 按钮。评分在其作业获得 GPU 后计入你的 3 次。取消仍在**排队**或**等待 GPU** 的提交会将其从队列中移除，不计入你的 3 次。取消**正在评分**的提交会停止运行，并计入你的 3 次之一，且该提交不计入排行榜：它没有名次，也未达到基线。

**第 4 步. 天际线排名。** 排名使用所有学生的每一次有效提交，而不仅是每名学生的最佳提交。有效提交是指已用其两个指标评分、学生未取消、且课程团队未标记为违规或作废的提交。

* 解决**至少 7 个任务**的提交按两个指标分轮排名。如果一份提交在两个指标上都不差于另一份，且至少在一个指标上更好，则前者支配后者。每一轮中，前沿是所有剩余提交中未被其他剩余提交支配的那些。有提交位于前沿的每名学生在那一轮获得名次，然后在下轮之前移除该学生的所有提交。
* 你的**最佳提交**是你所在轮次前沿中的某一份提交。如果你有多份位于前沿，最佳的是解决任务最多的那份，其次端到端时间最短的，再次最早的。
* 没有解决 7 个任务的有效提交的学生排在所有这些学生之下，按其有效提交中解决任务最多的一份排序。
* 相同名次为并列，下一名次计入其前面的所有人：1、1、1、4、…… 排行榜显示前 10 名，或在超过 10 人并列第 1 时显示所有并列者。
* 每次评分后都会重新计算轮次，因此其他学生的新提交可能把你移到更靠后的轮次。

**关于排行榜的更多说明。**

* **排行榜有 26 个任务**，编号 1 到 26。它们不是起始代码的 25 个任务。
* **服务器的日志。** 当你的服务器启动失败或未在 45 分钟内就绪时，Past submissions 页面会显示其日志末尾：最多最后 50 行和 5,000 个字符，并排除看起来像凭据或已记录请求的行。日志用于调试服务器：利用它读取排行榜的任务违反了“不得为特定任务编写任何内容”的规则。当服务器在运行期间停止，或停止应答达 90 秒（重新启动它的 `launch.sh` 也算，因为重启会重新加载权重），评分以 *Engine stopped during the run* 结束，并按已完成的任务计入。该页面随后不显示日志，因为到那时你的服务器已经看到了排行榜的任务。
* **崩溃或超时的运行仍然计入**，以其届时完成的任务计。Past submissions 页面还显示每次提交的逐任务结果（编号 1 到 26），包括每个任务的时间和轮次数，以及每个未解决任务的以下原因之一：
  + *not opened*：你的智能体从未请求该任务，或运行时间先耗尽；
  + *not finished*：任务打开期间运行崩溃或超时；
  + *no patch*：任务以空补丁结束；
  + *tests did not run*：评分未产生测试结果；
  + *import error*：测试无法收集（例如导入或语法错误）；
  + *broke existing tests*：补丁之前通过的测试现在失败；
  + *new tests failed*：修复本应使其通过的测试仍然失败（一个任务可能同时显示最后两项）。

### 评分

| 部分 | 分数 | 标准 |
| --- | --- | --- |
| 排行榜 | **60** | 你最佳提交在排行榜上的名次，按下述方式计分。 |
| 书面报告 | **30** | 第 4 部分中[书面报告](#write-up)的四个部分。 |
| 视频 | **10** | 对同样内容的清晰 3 分钟展示，并在屏幕上给出证据。 |

**排行榜得分。** 设 *r* 为你最佳提交的名次：

```
score = max(61 − r, 40)    if any of your valid submissions achieves the baseline
score = max(61 − r, 0)     otherwise
```

**基线**是在一次提交中解决至少 7 个任务且端到端时间不超过 100 分钟。如果你的任何有效提交达到该基线，你的得分至少为 40，即使该提交不是你的最佳提交。排行榜在其 26 个任务上衡量两项指标，这些任务比起始代码的 25 个任务更难，因此你在起始代码任务上的时间不能说明你是否达到基线。

例如，第 1 名得 60 分；第 12 名无论是否达到基线都得 49 分；第 30 名如果达到基线得 40 分，否则得 31 分。

[← 作业 3 — Harness 竞赛](assignment3.html)
[作业 5 — Mads-Stack →](assignment5.html)
