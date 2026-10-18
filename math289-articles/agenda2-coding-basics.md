---
title: "Week 2: Coding Basics — Session Agenda"
source: https://web.stanford.edu/class/math289/agenda2.pdf
crawled: 2026-10-18
---

MATH 289 Fall 2026 Week 2 / Coding Basics
Week 2: Coding Basics
Session agenda
Sessions:September 28 and 30, 10:30–11:50 a.m.
Leads:Shurui Liu and Fred Rajasekaran
Before class
•Install the ChatGPT desktop app and Visual Studio Code (VS Code).
•Create a GitHub account and make sure you can sign in.
•Windows users: follow the WSL setup guide.
• Before Day 2, check that you can access FarmShare with your SUNet ID and Stanford two-step authentication. See
Getting Connected.
Day 1: From a coding agent to a GitHub repository
Monday , September 28·80 minutes
Goal:Build a small program with a coding agent, understand how it works, and track and share it with Git and GitHub.
Time Activity
0–5 minWarm-up and setup.Finish the preparation above and resolve initial setup issues.
5–10 min What is a coding agent?Discuss how an agent can read, edit, and run code, and where human review fits in.
10–20 minSet up a coding agent.Install a desktop agent, select a model, and explore the interface. Experienced
participants may use their preferred tools.
20–30 minFirst project.Create a project folder. Ask Codex to implement a prime sieve and a prime-counting function,
then explain the code. Check a few small examples and generate a plot to reuse on Day 2.
30–35 minDiscussion.Where did things go wrong? How did you check the output? What did the agent’s explanation
clarify?
35–55 minLive terminal and Git demonstration.Shurui works through the workflow on a volunteer’s laptop, starting
with a fresh project folder. Practice navigation, repository creation, commits, and pushing to GitHub.
55–80 min Command-line agents and LaTeX.Install the Codex or Claude Code CLI and discuss why a CLI is useful on
a remote server. Demonstrate the Overleaf–Git workflow with an accessible project, then ask the agent to suggest
corrections to typos or mathematical mistakes. Review its suggestions.
T erminal and Git topics
•Navigate withcdand inspect files withls -alh; introduce package managers such asaptand Homebrew.
•Practicegit init,git add,git rm,git commit,git status, andgit log.
• Explain git fetch , git merge , git pull , andgit push . A pull fetches remote changes and integrates them according
to the repository’s configuration.
•Review changes and commit deliberately. Explain why force-pushing can overwrite shared history.
Day 1 checkpoint:Create a local repository and a private GitHub repository; push the sieve code; write a short
README.mdyourself, then commit and push it.
1

MATH 289 Fall 2026 Week 2 / Coding Basics
Day 2: Running code on Stanford FarmShare
W ednesday , September 30·80 minutes
Goal:Connect to a remote machine, move code and results between machines, and understand when to use a scheduled
compute job.
Time Activity
0–5 minWarm-up and discussion.What computing resources are available, and when is a laptop enough?
5–15 minConnect with SSH.Log in to FarmShare, identify the remote machine and current directory, and distinguish
the remote shell from the local one.
15–30 minTransfer files with SCP.Copy a practice file from the laptop to FarmShare, verify the transfer, and remove
only that practice copy.
30–45 minClone the project with Git.Set up GitHub authentication and clone the private repository on FarmShare.
Keep credentials out of the repository.
45–55 min Run the sieve.Run a small, quick example and inspect the output. Discuss file permissions, privacy, and CPU
and memory use on a shared system.
55–65 minBring results back.Copy the generated plots from FarmShare to the laptop and open them locally.
65–70 min Introduction to Slurm.Explain login nodes versus compute nodes and demonstrate submitting a small batch
job. Usetoporhtopto inspect resource use.
70–80 min Troubleshooting and optional tools.Address setup issues. If time permits, introducetmux, Python 3,uv, or a
CLI agent on FarmShare, including memory use, device authentication, and logging out.
Where to run code:Keep login-node work brief and within the shared resource limits. Use a Slurm job for long-running
or CPU- or memory-intensive computations. See the FarmShare overview and Running Jobs.
Day 2 checkpoint:Clone and run your project on FarmShare, retrieve a plot, and explain how you would submit a
larger computation through Slurm.
Exercises
1. Propose a project.Think of a software project you would actually want to use. Post a short description in the
course Slack, including its purpose and a first achievable milestone.
2. Explore a codebase with an agent.Choose a repository, read its README.md, clone it, and ask the agent to
explain its structure and intended workflow. Summarize the main components, required dependencies, and one part
of the code you now understand. Examples include mathematical reasoning agents such asrethlas or danus, or
coding-agent projects such asdeepseek-harness or opencode. For a larger challenge, explore Mathlib (with a Lean
toolchain) orverl(with its reinforcement-learning dependencies).
2