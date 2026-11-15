---
title: "Assignment 4 — Mads-Serve: own the model(20%)"
source: https://cs2680.seas.harvard.edu/assignments/assignment4.html
crawled: 2026-11-16
---

# Assignment 4 — Mads-Serve: own the model(20%)

> 原文：[Assignment 4 — Mads-Serve: own the model(20%)](https://cs2680.seas.harvard.edu/assignments/assignment4.html) · Harvard CS2680

CS2680 Modern AI Systems: Agents and System Optimizations

Assignment 4 — Mads-Serve: own the model

# Assignment 4 — Mads-Serve: own the model (20%)

**Out** Wed Oct 21 · **due** Tue Nov 10, 11:59pm · individual · [slides](../slides/assignment4.pdf) · [all five assignments](index.html)

In Assignment 3 your agent called models through the course API. In this assignment you serve the model yourself on one **RTX PRO 4500 (32 GB)**, point your Assignment 3 agent at it, and then make it faster by changing the serving engine or the agent.

**⚠️ ONE RTX PRO 4500 AT A TIME.**

The course has limited GPU resources, shared by the whole class, so please leave enough for your classmates. You should run on at most one GPU at a time. You will get a warning if you are found using more than one GPU, and each further violation will cost 10% of your score on this assignment. Leaderboard gradings run on separate GPUs and do not count.

**⚠️ THE LEADERBOARD DOES NOT ACCEPT LATE DAYS AND STOPS TAKING SUBMISSIONS ON TUESDAY, NOVEMBER 10, AT 11:59 P.M. ET.**

A zip whose upload starts by 11:59 p.m. is accepted and graded, even if the upload finishes after 11:59 p.m. Keep the Submit page open until it says the zip was submitted. Submissions made by then are still graded and count, even if their grading finishes later. With no leaderboard submission by then, you get 0 of the 60 leaderboard points. Late days apply only to the write-up and the video.

## Initialize your repository first

Download the [Assignment 4 starter archive](assignment4.tar.gz) into the root of your shared private course repository, on the machine you used for Assignment 3, and extract it there. It creates `assignment4/`, with the starter code in `assignment4/starter_code/`.

```
# From your shared course repository:
tar -xzf assignment4.tar.gz
rm assignment4.tar.gz
```

**Before you start work with Claude Code, run `init.sh`:**

```
# From your shared course repository:
bash assignment4/starter_code/init.sh
```

This copies `package_agent_sessions.py` to the repository root and writes `CLAUDE.local.md` there in place of Assignment 3's, so that Claude Code commits your changes together with the repository's session logs (Claude Code, Cursor and Codex) in `agent-sessions.tar.gz` at the repository root. For the submission you run the packager once more ([Part 4](#part-4-submission-and-grading)).

## Part 1. Run the basic SGLang setup

If you have not used the course cluster before, do the [first-time setup](../computing/cluster.html#first-time) on the HPC page first. Some steps below run once on the login node, as marked. Run the rest in the screen session on your GPU node.

### Start a job on a GPU node

From the login node (`ssh cs2680`), start a job on an RTX PRO 4500 node that holds a `screen` session, and attach to it:

```
sbatch -p gpu-g7-reserved --gres=gpu:rtxpro4500:1 -c 8 --mem=28G -t 4:00:00 -J work -o /dev/null --wrap 'screen -dmS work; while screen -ls work | grep -q "\.work"; do sleep 30; done'
squeue -u $USER --name=work                 # wait for state R, and note the JOBID
srun --jobid=<JOBID> --overlap --pty screen -r work
```

A node that was powered down takes about 4 minutes to boot (state `CF`). The screen session keeps running if your connection drops. Press `Ctrl-a d` to detach, and run the `srun` line again to reattach. The job ends after 4 hours, or when you run `scancel <JOBID>` on the login node. End it when you are done, since you may hold only one GPU at a time. The HPC page explains these commands in [Serving a model on a GPU node](../computing/cluster.html#serving).

### Set up the environment variables

Once, on the login node, create a password for your server. Your agent sends it with every request, and nobody without it can use your GPU:

```
mkdir -p ~/a4/engine && (umask 077 && openssl rand -hex 16 > ~/a4/serve.key)
```

Then set these two variables in every new shell you use for this assignment, on the login node and in every GPU job (a new screen window is a new shell too). The commands below use them:

```
export A4=/shared/courseSharedFolders/176914outer/176914/a4   # the course environment
export SERVE_KEY=$(cat ~/a4/serve.key)                       # your server's password
```

### Set up SGLang

The course environment in `$A4` holds SGLang's dependencies, a CUDA toolchain for kernels compiled at run time, and the weights of the course's model (Qwen3.6-35B-A3B NVFP4). The basic SGLang setup runs that checkpoint's FP4 experts with FlashInfer's native FP4 kernels, which the course environment ships prebuilt. SGLang itself is your own clone, so you can modify it. Once, on the login node:

```
git clone --depth 1 --branch v0.5.20 https://github.com/sgl-project/sglang.git ~/a4/sglang
git -C ~/a4/sglang switch -c a4                  # a branch for your commits
cp $A4/basic-sglang-flags.txt ~/a4/engine/flags.txt
git config --global user.name "Your Name"        # once, if you have not set these on the cluster
git config --global user.email "your Harvard email"
```

Then, in every job on a GPU node:

```
bash $A4/bin/setup.sh
```

`setup.sh` builds the environment on the node's local disk and ends with `setup finished`. It takes about **5 minutes** on a node that has just booted and about 30 seconds on a node where you already ran it.

Environment details

The environment is Python 3.12 with PyTorch 2.13, FlashInfer 0.6.18 and sgl-kernel 0.4.7, and a CUDA 13.4 toolchain. `setup.sh` installs the Python packages on the node and compiles a test kernel through each compiler SGLang uses. It does not copy the weights: the server reads them from `$A4/hf`. The environment goes in `/local_scratch/$USER/a4`, on the node's own disk, and only you can read it. A node started before the cluster change on October 29 has no `/local_scratch`, so there it goes in `/var/tmp/$USER-a4`. If `serve.sh` says that the course environment is not set up, run `setup.sh` again. This happens in a job where you ran `setup.sh` before the course's scripts moved the environment on October 29. Each node has its own disk, so a job on another node runs `setup.sh` again. If other students' files have filled the node's disk, `setup.sh` uses a shared copy of the packages in `$A4/venvs` instead of installing them, and prints a note. Everything works the same, but each server start takes about 2-5 minutes longer because the packages load over the network. The clone may print `warning: refs/tags/v0.5.20 ... is not a commit!`, which is harmless.

### Start the server

```
bash $A4/bin/serve.sh > ~/a4/server.log 2>&1 & tail -f ~/a4/server.log   # Ctrl-c stops watching; the server keeps running
```

Wait until the log prints this line. The first start on a node takes about **6 minutes**, and a restart on the same node about 1.5 minutes.

```
[2026-10-15 19:17:00] The server is fired up and ready to roll!
```

Then press `Ctrl-c` to stop watching, and check the server. `smoke.py` checks seven things your agent relies on and ends with `7/7 passed`:

```
python3 $A4/bin/smoke.py http://127.0.0.1:30000 $SERVE_KEY
```

To try a change, edit `flags.txt` or your clone, stop the server with `kill %1` in the shell that started it, and run the `serve.sh` line again. The leaderboard does not run `serve.sh` but your `engine/launch.sh` ([Part 4](#part-4-submission-and-grading)), which in the starter's template starts SGLang with the same `flags.txt`.

**Before you exit the job**, stop the server and run `bash $A4/bin/cleanup.sh`. It deletes your copy of the environment from the node. Nothing else deletes it. It stays until the node shuts down, even after your job hits its time limit or you end it with `scancel`. Your copy takes about 20 GB. On a node that has `/local_scratch`, it is there, on a disk of about 400 GB. On a node without it, it is in `/var/tmp`, which has 66 GB for every job on the node, so three students' copies fill it. `cleanup.sh` also deletes a copy that an older `setup.sh` made in `/var/tmp` on the node.

Server configuration

`serve.sh` starts SGLang from `~/a4/sglang` with the flags in `~/a4/engine/flags.txt`, followed by the flags the course sets: `--model-path nvidia/Qwen3.6-35B-A3B-NVFP4 --served-model-name qwen3.6-35b-a3b-fp4 --host 0.0.0.0 --port 30000 --api-key $SERVE_KEY`. Of the first start's 8 minutes, about 3 load the weights and about 3 are FlashInfer tuning its kernels for this card.

You may change any of the basic SGLang setup's flags in `flags.txt`. Your flags may not set the model path, the served model name, the address, the key or the number of GPUs, since `serve.sh` and the leaderboard set them, and may not use `--config`, which could set them too. Three of the setup's flags need care:

* `--moe-runner-backend` is required to serve Qwen3.6-35B-A3B NVFP4 with SGLang. Without it, startup fails with `NotImplementedError`.
* `--mamba-ssm-dtype bfloat16` stores the linear-attention layers' state at lower precision than the checkpoint specifies. It is part of the model's numerics, so changing it can change how many tasks the model solves.
* `--reasoning-parser` and `--tool-call-parser` fill the `reasoning_content` and `tool_calls` fields your agent reads, and `--enable-metrics` and `--enable-cache-report` make the server report more about its work.

Running your own scripts

The cluster has none of SGLang's packages or the CUDA toolchain installed, so the course provides them as an environment. The course environment is a Nix environment that `setup.sh` unpacks on the node's local disk, and a program sees it only when it is started through `nix-portable`, which `serve.sh` does for the server. A plain shell on the node does not, so `python` there finds no `torch` or `sglang`. To run a script of your own (e.g., `python -m sglang.bench_serving`), first open a shell inside the environment:

```
source $A4/bin/np.sh && a4sh bash --norc
export PYTHONPATH=~/a4/sglang/python HF_HOME=$A4/hf HF_HUB_OFFLINE=1 OPENAI_API_KEY=$SERVE_KEY
```

Clients such as `sglang.bench_serving` send the key in `OPENAI_API_KEY`; without it, they get `401` and report that the server is not ready. `HF_HUB_OFFLINE=1` makes scripts load the model's files from the course's copy in `$A4/hf`, and it also stops downloads from the Hugging Face Hub, so leave it out in a shell that must download a dataset.

Common problems

| The log says | Fix |
| --- | --- |
| `NotImplementedError ... Use --moe-runner-backend flashinfer_cutlass instead` | Add `--moe-runner-backend flashinfer_cutlass`, as the basic flags do. |
| `setup.sh` prints `this node uses the course's shared copy` | Other students' files fill this node's disk, so `setup.sh` used the shared copy of the packages. Everything works, but each server start takes about 2-5 minutes longer. For faster starts, move to another node (next row). |
| `setup.sh` prints `only NG free on <node>, and setup needs MG` | The node's disk is full. If the files are yours from an earlier job, run `bash $A4/bin/cleanup.sh`, then `setup.sh` again. Otherwise, end the job (`scancel <JOBID>` on the login node) and submit the `sbatch` line again with `--exclude=<node>` (for several nodes, `--exclude=<node1>,<node2>`). `setup.sh` prints the node's name on its first line. |
| `np.sh: run this inside a Slurm job on a GPU node` | You are on the login node. Start a job on `gpu-g7-reserved` first. |
| `No module named 'sglang'` (or `'torch'`) in your own script | That shell does not have the environment. Open one with `source $A4/bin/np.sh && a4sh bash --norc`, as above. |
| `CUDA out of memory` during startup or CUDA graph capture | Your flags use more GPU memory than the card has. Undo the change that used the memory. |

### Connect your agent

Your agent and its task containers need Docker, which the cluster does not have, so they run on the machine you used for Assignment 3. That machine must be on the Harvard network or the Harvard University VPN to reach the cluster. The starter code in `assignment4/starter_code/` ([extracted and initialized first](#initialize-your-repository)) is the Assignment 3 framework with 25 new tasks and with your server in place of the course API, and its dispatcher no longer limits how many tasks are live. Copy your Assignment 3 `src/` over its `src/`. The egress proxy runs in a container, which cannot reach your machine's `localhost`, so open the [SSH tunnel](../computing/cluster.html#tunnel) to the GPU node on the Docker bridge address (usually `172.17.0.1`) and point the harness at it (from a CloudLab or AWS machine, open the tunnel as the HPC page describes in [reaching the cluster from CloudLab or AWS](../computing/cluster.html#cloudlab-aws)):

```
cd assignment4/starter_code                           # from your course repository; the rest runs here
ssh -f -N -o ExitOnForwardFailure=yes -L 172.17.0.1:30000:<node>:30000 cs2680
export A3_API_UPSTREAM=http://172.17.0.1:30000
export CS2680_API_KEY=$(ssh cs2680 cat a4/serve.key)   # the same key as your server
export CS2680_MODEL_EXPERT=qwen3.6-35b-a3b-fp4 CS2680_MODEL_STANDARD=qwen3.6-35b-a3b-fp4 CS2680_MODEL_STARTER=qwen3.6-35b-a3b-fp4
bash evaluation_scripts/prepare_images.sh             # once: about 40 GB to download
python3 evaluation_scripts/run_all.py --limit 0       # preflight: look for EGRESS OK
```

The course API and its three models (starter, standard and expert) are not available in this assignment. Every model call goes to the model you serve, so all three model variables above name it. The preflight checks that your server accepts your key and serves that model. The starter's `README.md` lists the disk, CPU and memory your machine needs, and what a failed preflight means.

## Part 2. Measure your starting run

Run your Assignment 3 agent on the 25 tasks with the basic SGLang setup, keeping all 25 open from the start. The server's log and your agent's logs are written as the run goes, but the server's `/metrics` endpoint shows its counters and gauges only at the moment you read it, so while the run lasts, read it at regular intervals (for example, every 10 seconds with `curl`) and keep every reading.

Record the two numbers the leaderboard scores: tasks solved, and the end-to-end time from the start of the run (with your server already up) to the last task done. Your agent works on all the tasks at the same time, so this is the time to finish the whole set.

Then find out where the time goes. From the server's log, your `/metrics` readings and your agent's logs, measure whatever you need to explain your starting run's end-to-end time, and plot it over the whole run.

Also run SGLang's serving benchmark, `python -m sglang.bench_serving`, against the same server. Choose its settings to describe your agent's workload as well as you can, compare what it reports with what you measured in your starting run, and keep both.

## Part 3. Make serving efficient

**Make the server serve your agent faster**, so that the agent solves the task set in less time. Work in three steps:

1. **Find the cause.** Use your Part 2 measurements to find what limits the speed.
2. **List fixes.** Name the changes to the engine or the agent that could remove the cause, and predict what each would do.
3. **Try them.** Implement the most promising ones and measure how much each helps.

Change one thing at a time, measure it on the same tasks as your starting run, and keep the logs of every run you report.

**Record each change as you go.** Each time you try a change, add it to the [table or list of optimizations](#write-up) in your write-up, even if it did not help.

### Allowed changes

* **The engine.** SGLang or vLLM, the two frameworks the course environment provides, with any change to their source code and any settings. To use vLLM 0.31.0, follow [Using vLLM](https://leaderboard.cs2680.com/a4/engines.html#vllm) on the leaderboard's engine conventions page, which clones vLLM, installs it on the node with `bash $A4/bin/setup.sh --vllm`, and puts `$A4/basic-vllm-flags.txt` in place of your `flags.txt`; `serve.sh` then starts vLLM when `~/a4/engine/engine.json` names `vllm`. Kernels compiled ahead of time (SGLang's `sgl-kernel`, vLLM's C++ and CUDA extensions) cannot be rebuilt on the course nodes, so a patch may change only files under `python/sglang/` for SGLang (not `python/sglang/kernels/aot/`) or under `vllm/` for vLLM; kernels compiled at run time may change. You may also use another serving framework at your own risk. Build it into an environment folder of your own and name the engine `other`, as [Your own engine](https://leaderboard.cs2680.com/a4/engines.html#own-engine) on the engine conventions page describes. The course does not fix problems with other frameworks. That page lists the conventions for every engine.
* **The agent.** How it uses the server.

**You may not change the model.** Keep the model in `engine.json` as the starter has it, and do not convert its weights when the engine loads them (e.g., with `--quantization` or `--dtype`). Engine settings such as the KV cache's data type are allowed, and speculative decoding may use the model's own multi-token-prediction head but not a separate draft model.

Your server runs on one GPU. You may not change the task set, the dispatcher or the evaluation scripts, or send model calls anywhere but your server.

### Cheating

The rules of Assignment 3 apply: no gold patches or hidden tests, nothing written for particular tasks or repositories, and nothing learned from running the evaluation tasks offline. They apply to the engine too: it may not recognize a task or a prompt, ship responses or any other state precomputed from the tasks, or keep state from one graded run to the next. Tuning a general setting, such as a server flag, by measuring it on the tasks is allowed. A violation invalidates the submission. If you are not sure whether a change is allowed, email us before you submit it.

## Part 4. Submission and grading

The submission has three parts, as in Assignment 3.

* **Code.** Your agent goes in `src/`, and your server goes in `engine/`. The starter's `engine/` is the basic SGLang setup:
  + `engine.json`: the framework (`sglang`, `vllm`, or `other` with your environment folder in `"env"`) and the model (do not change it);
  + `flags.txt`: a copy of `$A4/basic-sglang-flags.txt`;
  + `launch.sh`: the script that starts your server, whose one working line is `exec a4-serve --flags-file "$A4_ENGINE_DIR/flags.txt"`;
  + `sglang.patch`, only if you changed SGLang: your clone's changes against v0.5.20, committed or not, which `git -C ~/a4/sglang add -A python/sglang && git -C ~/a4/sglang diff --no-renames v0.5.20 -- python/sglang > ~/a4/engine/sglang.patch` writes (for vLLM, `vllm.patch`, as the engine conventions page shows).Zip `engine/` with `src/` into `submission.zip` and upload it on the leaderboard's Submit page. Also run `python3 package_agent_sessions.py` from the repository root, which writes your Claude Code, Cursor and Codex sessions to `assignment4/a4-sessions.tar.gz`.
* **Write-up.** `writeup.md`, in your own words with no AI-generated text. Cover these four things, in this order:
  1. what limited your starting run, and how you found it;
  2. what you found when you compared SGLang's serving benchmark with your agent's runs;
  3. a table or a list of your optimizations, with one entry for each change you tried, including the ones that did not help, and for each entry:
     + *Change*: what you changed;
     + *Observation*: the measurement that led you to the change, with its number;
     + *Reasoning*: why you expected the change to help, and what you predicted it would do;
     + *Result*: what you measured, compared with the run before it, with numbers from your logs;
  4. the lessons you learned.
* **Video.** The same material in **3 minutes**, with your face visible and in your own voice, showing the log or `/metrics` for any claim that depends on it. Upload it to Canvas.

```
assignment4/
├── starter_code/
│   ├── src/              your agent
│   └── engine/           engine.json, flags.txt, launch.sh, and your patch if you made one
├── a4-sessions.tar.gz    your agent session files
└── writeup.md            the write-up
```

The leaderboard runs `launch.sh` with bash in place of `serve.sh` or your own batch script, so `#SBATCH` lines in it have no effect. It runs inside the course's sandbox, which has no network. The sandbox hides `/shared`, `/scratch` and every home folder. Only the course's weights and Python packages on `/shared` stay visible, and they are read-only. So a `launch.sh` that calls `$A4/bin/serve.sh` or reads `~/a4` fails there. The sandbox puts the course's `a4-serve` on `PATH` and gives `launch.sh` the variables its comments list. Your server must listen on `127.0.0.1:$A4_PORT`, require the key in `$A4_KEY_FILE` on every request (only `/health` and `/metrics` may answer without it), serve one model named `$A4_SERVED_MODEL_NAME`, and answer within 45 minutes of the start of the grading job.

**Before you submit**, test your `engine/` as the leaderboard runs it. Put it in `~/a4/engine` on the cluster (the starter's `README.md` shows how), stop your own server, and run this in a job on a GPU node after `setup.sh` (`setup.sh --vllm` for vLLM, `setup.sh --weights-only` for `other`):

```
bash $A4/bin/check-submission.sh --launch
```

It checks `engine/` against the leaderboard's rules, starts your server from it in the course's sandbox as a grading does, and prints `PASS` or `FAIL` with the end of the server's log. With the starter's template it takes about 5 minutes. A server that fails to start on the leaderboard still counts as one of your 3 gradings that day.

### Leaderboard

The leaderboard starts your server from `engine/` on a fresh RTX PRO 4500 node, waits until it is ready, and then runs your agent from `src/` on the evaluation set, with the same `dispatcher/`, `madsServe.py` and evaluation scripts as the starter code and the evaluation set's 26 tasks in place of the starter's 25. The leaderboard is at <https://leaderboard.cs2680.com/>, and you log in with your Assignment 3 account. Its `Leaderboard` page shows the top 10 students by their best submission, and your own best submission with its rank.

The figure below follows one submission from your upload to the end of its run. Your server runs in the course's sandbox with no network, your agent's model calls reach only your server, and the end-to-end time runs from the moment your server is ready to the last task done.

submission.zip
src/ your agent
engine/ your server

Submit page

Queue
one per student,
3 gradings a day

a GPU is free

RTX PRO 4500 node
fresh for each grading

course sandbox, no network

engine/launch.sh
starts your server

Your server
startup limit: 45 min

src/
Agent container

Your agent (src/)

dispatcher/, madsServe.py
as in the starter code

model calls
only to your server

one agent opens all 26 tasks

Task container k
k = 1 to 26
the task's repository,
no limit on how many are open

Grading container
test time limit: 35 min
a fresh copy of the task image,
your patch, and the hidden tests
waiting, then server startup

not counted
end-to-end time, at most 4 h
clock starts: server ready
clock stops: last task done

**Limits.**

* **Waiting for a GPU: no limit.** A grading waits until an RTX PRO 4500 node is free for it. The wait counts toward no limit and not toward your score.
* **Server startup: 45 minutes**, from the start of the grading job to the moment your server answers, including any installation. A server that is not ready by then fails the grading, and the Past submissions page shows the end of its log. This time does not count toward your score.
* **Run: 4 hours**, counted from the moment your server is ready, when the end-to-end time also starts. After 4 hours the run stops: every task still open is finished as if your agent had called `done`, tasks never opened count as failures, and the time after the cut does not count.
* **Tasks live at once: no limit.** Your agent may open every task at the start.
* **Grading of a patch: 35 minutes.** A test suite that hangs counts as all of its tests failing.
* **Submissions: one queued or being graded at a time, and 3 gradings a day** (Step 3). A grading that fails because of a problem on the course's side does not count.

**Step 1. Submit.** On the Submit page, upload `submission.zip`. Every grading runs all 26 tasks of the evaluation set.

**Step 2. Metrics.** Every submission is evaluated on two metrics:

* the number of tasks solved,
* the end-to-end time, from the moment your server is ready to the last task done, at most 4 hours.

**Step 3. Past submissions and cancelling.** The Past submissions page lists your ongoing and past submissions. You can have at most one submission queued or being graded at a time, and at most **3 gradings a day** (midnight to midnight, Eastern time). The submission queued or being graded has a **Cancel** button. A grading counts toward your 3 once its job has a GPU. Cancelling a submission that is still **queued** or **waiting for a GPU** removes it from the queue, and it does not count toward your 3. Cancelling a submission that is **being graded** stops the run and counts as one of your 3, and the submission does not count on the leaderboard: it gets no rank and does not achieve the baseline.

**Step 4. Skyline ranking.** The ranking uses every valid submission from all students, not only each student's best. A valid submission is one graded with its two metrics that its student did not cancel and that the course staff did not mark as a violation or invalidate.

* Submissions that solved **at least 7 tasks** are ranked in rounds over the two metrics. One submission dominates another if it is at least as good on both metrics and better on at least one. In each round, the front is every remaining submission that no other remaining submission dominates. Every student with a submission on the front is ranked in that round, and then all of that student's submissions are removed before the next round.
* Your **best submission** is one of your submissions on the front of your round. If several of yours are on it, your best is the one that solved the most tasks, then the one with the shortest end-to-end time, then the earliest.
* Students with no valid submission that solved 7 tasks rank below all of them, by the most tasks one of their valid submissions solved.
* Equal ranks are ties, and the next rank counts everyone ahead of it: 1, 1, 1, 4, ... The leaderboard shows the top 10, or everyone at rank 1 when more than 10 share it.
* The rounds are computed again after every grading, so another student's new submission can move you to a later round.

**More about the leaderboard.**

* **The leaderboard has 26 tasks**, numbered 1 to 26. They are not the 25 tasks of the starter code.
* **Your server's log.** When your server fails to start or is not ready within 45 minutes, the Past submissions page shows the end of its log: at most its last 50 lines and 5,000 characters, without the lines that look like a credential or a logged request. The log is for debugging your server: using it to read the leaderboard's tasks breaks the rule against anything written for particular tasks. When your server stops during the run, or stops answering for 90 seconds (a `launch.sh` that restarts it counts, since a restart reloads the weights), the grading ends as *Engine stopped during the run* and counts with the tasks it had finished. The page then shows no log, since by then your server has seen the leaderboard's tasks.
* **Crashed or timed-out runs still count**, with the tasks they had finished by then. The Past submissions page also shows each submission's per-task results (numbered 1 to 26), with each task's time and number of turns and, for each unsolved task, one of these reasons:
  + *not opened*: your agent never asked for the task, or the run's time ran out first;
  + *not finished*: the run crashed or timed out while the task was open;
  + *no patch*: the task ended with an empty patch;
  + *tests did not run*: the grading produced no test results;
  + *import error*: the tests could not be collected (e.g., an import or syntax error);
  + *broke existing tests*: a test that passed before your patch now fails;
  + *new tests failed*: a test your fix should make pass still fails (a task can show both of the last two).

### Grading

| Part | Points | Criteria |
| --- | --- | --- |
| Leaderboard | **60** | The rank of your best submission on the leaderboard, scored as below. |
| Write-up | **30** | The four parts of the [write-up](#write-up) in Part 4. |
| Video | **10** | A clear 3-minute presentation of the same material, with the evidence on screen. |

**Leaderboard score.** If *r* is the rank of your best submission:

```
score = max(61 − r, 40)    if any of your valid submissions achieves the baseline
score = max(61 − r, 0)     otherwise
```

The **baseline** is at least 7 tasks solved with an end-to-end time of at most 100 minutes, both in one submission. If any of your valid submissions achieves it, your score is at least 40, even if that submission is not your best. The leaderboard measures both on its 26 tasks, which are harder than the starter's 25, so your times on the starter's tasks do not show whether you achieve it.

For example, rank 1 scores 60, rank 12 scores 49 whether or not you achieve the baseline, and rank 30 scores 40 if you achieve the baseline and 31 if you do not.

[← Assignment 3 — Harness competition](assignment3.html)
[Assignment 5 — Mads-Stack →](assignment5.html)
