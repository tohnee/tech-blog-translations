---
title: "Assignment 5 — Mads-Stack: optimize the full stack(10%)"
source: https://cs2680.seas.harvard.edu/assignments/assignment5.html
crawled: 2026-11-16
---

# Assignment 5 — Mads-Stack: optimize the full stack(10%)

> 原文：[Assignment 5 — Mads-Stack: optimize the full stack(10%)](https://cs2680.seas.harvard.edu/assignments/assignment5.html) · Harvard CS2680

CS2680 Modern AI Systems: Agents and System Optimizations

Assignment 5 — Mads-Stack: optimize the full stack

# Assignment 5 — Mads-Stack: optimize the full stack (10%)

**Out** Wed Nov 11 · **due** Tue Nov 24, 11:59pm · individual · [slides](../slides/assignment5.pdf) · [all five assignments](index.html)

Assignment 5 builds on [Assignment 4](assignment4.html). Its goal is a strong agent of your own. Start from your Assignment 4 agent, fix what held it back, and take good ideas from other agent designs. You may also change the model and the serving engine, but you do not have to. You still serve on one **RTX PRO 4500 (32 GB)**.

* **Leaderboard (50 points)** for your agent's result on [Terminal-Bench 2.0](#terminal-bench). See [Grading](#grading).
* **Blog post (40 points) and video (10 points)** on what you learned from Assignments 2-5. See [Blog post](#blog-post). There is no write-up.
* **Bonus (up to 5 percentage points of your course score)** for your rank on Terminal-Bench 2.0 and on the 26 tasks of Assignment 4's leaderboard. See [Bonus](#bonus).

The same agent runs Terminal-Bench and Assignment 4's tasks, so first [generalize](#changes) your Assignment 4 agent.

**⚠️ ONE RTX PRO 4500 AT A TIME.**

As in Assignment 4, use at most one GPU at a time. The first violation gets a warning, and each further one costs 10% of your score on this assignment.

**⚠️ THE LEADERBOARD DOES NOT ACCEPT LATE DAYS AND STOPS TAKING SUBMISSIONS ON TUESDAY, NOVEMBER 24, AT 11:59 P.M. ET.**

Without a submission by then, you get 0 of the 50 leaderboard points and no bonus. Late days apply only to the blog post and the video.

**⚠️ WRITE YOUR BLOG POST YOURSELF.**

If we find that your blog post was written by AI, we will deduct points.

## Part 1. Set up and adapt your agent

### Set up

Download the [Assignment 5 starter archive](assignment5.tar.gz) into the root of your course repository, extract it, and run `bash assignment5/starter_code/init.sh` before you start work with Claude Code, as in [Assignment 4](assignment4.html#initialize-your-repository). Copy your Assignment 4 `src/` and `engine/` into `assignment5/starter_code/`. The starter's `run_all.py` runs your agent on [Terminal-Bench 2.0](#terminal-bench) or on the 25 tasks of Assignment 4's starter.

On the cluster, Assignment 5 has its own course environment, which is Assignment 4's environment with two changes: the model is served as `cs2680-model`, and `engine.json` may name a [model folder](#model-folder) of your own. Set it in every new shell, and use `$A5` wherever Assignment 4's page uses `$A4`:

```
export A5=/shared/courseSharedFolders/176914outer/176914/a5   # the course environment
```

The `A4_*` variables that `launch.sh` gets, such as `$A4_PORT`, keep their names, and so does the folder `~/a4`. When you connect your agent as in [Assignment 4](assignment4.html#connect-your-agent), set all three `CS2680_MODEL_*` variables to `cs2680-model`, as the starter's `README.md` shows.

### Terminal-Bench 2.0

[Terminal-Bench 2.0](https://arxiv.org/abs/2601.11868) is a public benchmark of 89 tasks, from software engineering to system administration, security, data science and model training. Each task gives your agent an instruction and a container with internet access, and sets its own time limit, CPUs and memory. When your agent finishes a task, the task's hidden tests run in the same container and check its final state. The images take about 49 GB compressed and run only on x86\_64. Public results for version 2.0 are on its [leaderboard on Harbor Hub](https://hub.harborframework.com/datasets/terminal-bench/terminal-bench-2/latest?tab=leaderboard).

### The dispatcher

The dispatcher gives Terminal-Bench tasks and Assignment 4's tasks in the same form, so your agent needs no code for a particular benchmark. Three things change from Assignment 4:

* `next_task()` returns `task` (the index *k*), `instruction` (the whole task as text), `sandbox_url`, `workdir` and `time_limit_s`. `time_limit_s` is the most seconds the task may stay open: the smaller of its own limit and what is left of the run's limit (for Assignment 4's tasks, what is left of the 4 hours). It is `None` only when no limit applies, as for an Assignment 4 task in a local run with `A3_RUN_LIMIT_S=0`.
* `done(k)` ends task *k*, and the course grades the task's final state. A task still open when `time_limit_s` runs out is graded at that moment.
* `evaluate`, `extract_patch`, `submit_patch` and `continue_task` are removed.

### Generalize your Assignment 4 agent

To generalize your Assignment 4 agent, make seven changes:

1. **Read the task from `instruction`.** Remove prompts and code that assume a repository to fix or a patch to produce. The working directory may not be a git repository, and tools and prompts written for code repositories help less on most Terminal-Bench tasks.
2. **Check your own work.** Without `evaluate(k)`, which in Assignment 4 ran a task's hidden tests on your agent's patch before the task ended, your agent must write and run its own checks before `done(k)`.
3. **Leave the final state in place.** Files must be where the instruction asks for them. A service the task asks for must still run after `done(k)`, so start it detached, with its output redirected to a file.
4. **Handle long and interactive commands.** One sandbox command runs for at most 900 seconds, so run longer jobs in the background and poll them. A command cannot take keyboard input. Drive an interactive program, such as an editor or a REPL, through tmux, which you can install in the container, or use its non-interactive mode.
5. **Read and write anywhere.** Assignment 4's `src/sandbox_server.py` refuses paths outside the repository and `/work`, but tasks may write anywhere, such as `/etc`. Use the starter's copy, or remove the limit from yours.
6. **Budget each task's time.** Plan a task's turns and commands within its `time_limit_s`.
7. **Take the model name from the environment.** Read it from the `CS2680_MODEL_*` variables, which the leaderboard sets to `cs2680-model`. Do not hard-code Assignment 4's model name. Your server no longer lists it, and some engines, such as vLLM, reject a request for it.

## Part 2. Improve the full stack

### Keep improving your agent and serving engine

Work as in [Parts 2](assignment4.html#part-2-measure) and [3](assignment4.html#part-3-improve) of Assignment 4: measure, find what limits your run, and fix it. In the agent, study the tasks it fails and try ideas from other agent designs. In the serving engine, continue your Assignment 4 work within its [allowed changes](assignment4.html#what-you-may-change). A faster server also gives your agent more turns within each task's time limit. Results vary between runs, so run a change more than once before you conclude that it helped. Record each mistake your agent makes and each technique you try, including the ones that did not help.

You may also change the model: serve another checkpoint, quantize, prune or distill the model, train or fine-tune one, or add a draft model for speculative decoding. Assignment 4's rules that fix the model do not apply. Your server still serves the name `cs2680-model` and must be ready within 45 minutes, including loading the weights. You may train a model in any way, except on the tasks and your agent's runs of them (see the [rules](#rules) below), and on the course cluster within the one-GPU limit. A smaller model can solve fewer tasks, so measure tasks solved after every model change.

To serve another model, put it in a folder of your own on the cluster, under `/shared/courseSharedFolders/176914outer/176914/a4-models/<your cluster username>/`, and set `engine.json`'s `"model"` to the folder's path. The folder holds everything your server loads, a draft model included, in at most 48 GiB. Each grading copies it to the GPU node when the grading starts, and the copy counts toward the 45 minutes. The leaderboard's [Engine conventions](https://leaderboard.cs2680.com/a5/engines.html#model-folder) page lists the folder's rules, and `$A5/bin/check-submission.sh --launch` tests a folder as a grading uses it.

### Rules

Your harness should work across general tasks rather than being tailored to specific tasks or repositories in the benchmarks. The following practices are considered violations. Any submission containing them will be invalidated and excluded from the leaderboard, and your ranking will revert to those of your best valid submission:

1. **Using the gold patch:** Do not submit, match against, or use any part of the gold patch (for Terminal-Bench, the reference solution) or the hidden tests. The agent should not be aware that a gold patch exists.
2. **Hard-coding task- or repository-specific information:** Do not encode specific failure modes, solutions, or repository knowledge into the harness. For example, an instruction such as "For Ansible tasks, be careful with files in folder X" is not allowed.
3. **Providing lessons learned outside the current evaluation:** Do not include knowledge about particular tasks obtained from offline experimentation. This restriction also applies to instructions that may appear general but encode a benchmark-specific lesson. For example, "If the requirements mention the initializer, modify `__init__`" is not allowed.
4. **Copying code between tasks:** Each task is solved from its own starting code. Do not copy code from one task's repository, files or git history into another task, directly or through the model. Your agent may carry notes to other tasks, such as how the tests run or which approach failed, but not the project's code.
5. **Training on the tasks:** Do not train or fine-tune a model on the tasks of Terminal-Bench 2.0 or Assignment 4 or on your agent's runs of them, before or during a grading, or serve a model you know was trained on them.
6. **Recognizing tasks in the server:** Rules 2 and 3 also apply to your server and model folder, which may not recognize a task or a prompt, or ship responses or cache contents precomputed from the tasks.
7. **Using the internet:** In a Terminal-Bench container, your agent may use the internet, for example to install packages, but not to look up Terminal-Bench, a task or its solution.

The harness may instead guide the agent to inspect relevant source code, examine nearby or similar structures, and derive an appropriate solution during the evaluation. Any task-specific insight should be discovered by the agent as it works and can be verified through the trajectory.

You may run Terminal-Bench 2.0 and the 25 tasks of Assignment 4's starter yourself, but not the 26 leaderboard tasks, to measure changes, tune general settings such as server flags, and fix general mistakes like those in [Part 1](#changes).

We keep and review the trajectories, source code, and patches generated during each submission evaluation. If we find a violation, we'll let you know by email. If you're unsure whether your harness design follows these guidelines, feel free to email us before submitting.

## Part 3. Submission and grading

You submit three things:

* **Code.** As in [Part 4 of Assignment 4](assignment4.html#part-4-submission-and-grading), under `assignment5/starter_code/`: your agent in `src/` and your server in `engine/`, zipped into `submission.zip` for the leaderboard, and your agent sessions packaged with `python3 package_agent_sessions.py`.
* **Blog post.** A post on the [course blog](https://blog.cs2680.com/), as described in [Blog post](#blog-post) below.
* **Video.** A clear presentation of the same material in **3 minutes**, with the evidence on screen, uploaded to Canvas.

### Leaderboard

The leaderboard is at <https://leaderboard.cs2680.com/a5>, and you log in with the same account as in Assignment 4. As in Assignment 4, it starts your server on a fresh RTX PRO 4500 node and runs your agent. Every grading of your `submission.zip` has two runs: Terminal-Bench 2.0 first, then the 26 tasks, which start only after the Terminal-Bench run has ended. Your server starts once and serves both runs. Each run is measured on tasks solved and end-to-end time:

* **Terminal-Bench 2.0:** every task, each under its own limits (see [Terminal-Bench 2.0](#terminal-bench)), with 6 hours for the whole run and no limit on how many tasks are open at once. This run decides your 50 leaderboard points and part of your [bonus](#bonus).
* **The 26 tasks of Assignment 4's leaderboard**, as in Assignment 4: no network, 4 hours for the whole run, and all tasks may be open at once. This run decides the rest of your [bonus](#bonus).

Each run's limit and end-to-end time count from the run's start. In both runs, the tasks come in a new random order in every grading, and a task never opened counts as not solved. The course uses the two results to study how much the agent harness changes a benchmark score and how to control the variance between runs. You get **2 gradings a day**, and Assignment 4's other leaderboard rules apply, with two additions for the two runs:

* **Cancel** works as in Assignment 4 until the Terminal-Bench run has ended. After that, it stops only the run on the 26 tasks: your Terminal-Bench result counts, and the grading has no result on the 26 tasks.
* **Problems on the course's side** are handled as in Assignment 4. A task hit by one is not rerun: it is graded on the state it reached, so it may count as not solved. A grading that fails because of one goes back to the queue to be graded again. Up to three gradings a day that end as *Engine check failed* or stop for a problem on the course's side do not count toward your 2 gradings a day; any more do. If the grading fails after your Terminal-Bench result is recorded, that result is kept, only the run on the 26 tasks is graded again, and the grading counts toward your 2 gradings a day.

### Blog post

**Write a post on the [course blog](https://blog.cs2680.com/) about what you learned from Assignments 2-5.** You do not need to organize it by assignment.

Before you start, think back over all four assignments and write about as many of your lessons as you can think of. For each lesson, describe what you did, what happened and what you learned, with your own measurements and examples. Mistakes are lessons too, so include them along with what worked.

Write the post yourself, in your own words. **Don't generate it with AI.** Publish it with the blog's [publishing guide](https://blog.cs2680.com/publish/). The post is public, so make sure there is no private data.

### Grading

We expect everyone who puts in enough effort to get full or nearly full marks.

**Baseline.** A submission meets the baseline if its Terminal-Bench 2.0 run reaches either of these two targets:

| Target | Tasks solved | End-to-end time |
| --- | --- | --- |
| Fast | at least 20 | at most 2 hours |
| Accurate | at least 30 | at most 6 hours (the whole run) |

Both numbers describe one whole run: the tasks it solved and its end-to-end time. As in Assignment 4, the end-to-end time runs from the run's start, when your server is ready, to the moment the last task ends, whether by `done(k)`, at a time limit, or when your agent stops. For example, a run that solves 22 tasks and whose last task ends 2 hours and 10 minutes after the start misses the fast target, even if it had solved 20 tasks within the first 2 hours.

**Leaderboard score.** If *s* is the most tasks one of your valid submissions solved on Terminal-Bench 2.0:

```
score = 50               if any of your valid submissions meets the baseline
score = min(2 × s, 40)   otherwise
```

For example, if none of your submissions meets the baseline and your best one solved 15 tasks, you get 30 points. A submission that solved 20 or more tasks but missed both targets gets 40. Your score depends only on your own submissions, not on other students' results.

**Terminal-Bench ranking.** The leaderboard ranks every valid submission from all students as in Step 4 of [Assignment 4's leaderboard](assignment4.html#leaderboard), with 20 tasks in place of 7: submissions that solved at least 20 tasks are ranked in rounds over tasks solved and end-to-end time, and students with no valid submission that solved 20 tasks rank below all of them, by the most tasks one of their valid submissions solved. Your rank does not change your score, and the [bonus](#bonus) uses its own rankings.

### Bonus

The bonus adds up to 5 percentage points to your final course score: up to 3 from the run on the 26 tasks and up to 2 from the Terminal-Bench run. Only submissions that meet the [baseline](#baseline) are qualified for bonus, so the techniques behind a bonus must also work on Terminal-Bench. **The baseline and the bonus must come from the same submission: a submission that does not meet the baseline itself earns no bonus, even if another of your submissions meets it.** Each of the two runs has its own ranking of qualified submissions, in rounds as in the Terminal-Bench ranking above, and the two rankings may use different submissions of yours. The ranking on the 26 tasks counts only submissions that solved at least 7 of them, as in Assignment 4. You get points for the round in which you are ranked:

| Your round | The 26 tasks | Terminal-Bench 2.0 |
| --- | --- | --- |
| 1 | 3 | 2 |
| 2 | 2 | 1 |
| 3 | 1 | 0 |
| 4 or later | 0 | 0 |

For example, if you are ranked in round 1 on the 26 tasks and in round 2 on Terminal-Bench, your bonus is 3 + 1 = 4 percentage points. The bonus counts toward the course's 10% cap on [bonus credit](../policy.html#bonus) and does not change your score on this assignment.

[← Assignment 4 — Mads-Serve](assignment4.html)
