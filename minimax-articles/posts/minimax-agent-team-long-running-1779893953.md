---
title: "MiniMax Agent Team: Built for Long-Running Tasks and Continuous Evolution"
date: 2026-05-27
source: https://www.minimax.io/blog/minimax-agent-team-long-running-1779893953
crawled: 2026-09-22
---

# MiniMax Agent Team: Built for Long-Running Tasks and Continuous Evolution

2026-05-27

AIAgentProduct Update

Today we are introducing the overall upgrade of MiniMax Agent. We have given the upgraded Agent a new name: Mavis — MiniMax as a Jarvis, your AI butler.

This release brings the following updates:

- **Launching Agent Teams.** On MiniMax Agent desktop you can now run multiple Agents in parallel, create Agents in different roles, and have them form a team that collaborates on complex tasks — ideal for long, complex work a single Agent cannot finish alone.
- **Merging TokenPlan and Agent Plan.** One subscription unifies CLI, API, and Agent across M2.7, music, video, and voice. Credits are shared between Agent and API for more flexible usage. If you previously subscribed to both plans, you will get an extra month of membership.

![MiniMax Agent Team Banner](https://filecdn.minimax.chat/public/agent-team-hero-1779893281286.jpeg)

MiniMax Agent Team Banner

This time we want to share the thinking behind Agent Teams: how did we design the Agent team? What problem does it solve? What cost did we pay? When should users adopt Agent Team, and when is it unnecessary?

Let's first revisit **how today's single-Agent setup actually executes**.

> “Help me put together a long-form article about Agent Team. The information must be based on the latest data in 2026, and deliver both Markdown and HTML versions.”

In the past, we would hand this sentence to a powerful AI assistant. It would reply immediately, pushing a long block of text back into the chat. The experience felt smooth, but as delivery quality requirements rise, problems surface: who gathers the sources? Who verifies the facts? Who lays out the document? And once today's job is done, will the system even remember the pitfalls next time?

## 1. Why we need an Agent Team

Even though you can iterate Skills to make a single Agent deliver well, when a single Agent produces the final result it is inevitably both the judge and the contestant. That contradiction is the starting point of Agent Team.

Agent Team turns a complex task that was crushed onto one Agent into a process with a front office and a back office, with acceptance, and with memory. The user still sends only one message, but the Agent Team system decides whether to split the task, which roles can run in parallel, which results must be verified, and which experience should be retained.

Continuing the scenario above.

> “Help me put together a long-form article about Agent Team. The information must be based on the latest data in 2026, and deliver both Markdown and HTML versions.”

A single Agent might finish this smoothly, like a coworker sitting next to the user. When the user asks “polish this paragraph”, it can edit immediately; when the user says “format is off here”, it confirms right away. But a few problems show up: 1) if the user does not command it, the Agent stops and the user has to keep telling it to “confirm” or “keep going”.

- **A single Agent stops at moments the user does not expect.**

Users often see an Agent with 7 things to do that pauses after 3 edits and starts reporting: “I have finished edits 1, 2, 3 — would you like me to continue with the other 5?”

This happens because models commonly have context anxiety, and training for very long tasks itself takes huge money, time, and algorithmic effort. The model's judgment of when a task can stop is fuzzy.

![](https://filecdn.minimax.chat/public/agent-team-why-stop-l-1779893281287.jpeg)

![](https://filecdn.minimax.chat/public/agent-team-why-stop-r-1779893281288.jpeg)

- **A single Agent gets dumber over time — degradation is obvious on long tasks.**

Users often feel that as the Agent runs it shifts from “a smart assistant” to “managing someone who is busy but easily distracted”. The user keeps asking: do you still remember that earlier requirement? Why did you turn the research task into a product marketing pitch?

As long as one step drifts, **everything downstream will keep generating along the drift**.

Worse, a single Agent rarely forms natural “checks and balances”. It might honestly self-check, but it is still inspecting the very scene it just constructed itself.

![](https://filecdn.minimax.chat/public/agent-team-why-dumber-l-1779893281289.jpeg)

![](https://filecdn.minimax.chat/public/agent-team-why-dumber-r-1779893281290.jpeg)

- **A single Agent also cannot respond quickly to long-cycle tasks.**

Especially in IM scenarios (driving Agents through messaging apps), user patience is very short. After sending a message in IM, users expect a response within seconds. Even if the task is complex, users still want a first reply along the lines of: “got it, here is what I will do, I will come back when it is done.” They do not want to stare at a chat box for ten minutes, half an hour, or longer just to confirm the task has started.

**“Why isn't my Agent replying to me” is the largest single source of user feedback we receive.**

Agent Team offers a different experience. The main Agent first responds quickly to the user: I have received the task, the goal is confirmed, and I will split and execute in the background. The task is broken into multiple section bundles or multiple versions, and executed in parallel.

Users no longer need to wait for every sub-step to finish. They receive reports at key checkpoints: task started, blocked, decision needed, completed.

They can also chat with the main Agent anytime: “I just had another idea, can you also research it on the side”, and the main Agent can respond: “sure, I will spin up another Agent group now and report when there is progress. By the way, of the in-flight tasks 2/5 are done, 2 of the remaining 3 are in the verification stage, and the last one I will keep watching.”

Just like a thoughtful friend who replies to your WeChat messages in seconds.

![](https://filecdn.minimax.chat/public/agent-team-im-cmp-l-1779893281291.jpeg)

![](https://filecdn.minimax.chat/public/agent-team-im-cmp-r-1779893281292.jpeg)

- Stepping outside any one task, we naturally have to accept **the diversity of user needs and the division of roles across domains.**

On the same day, a single user might ask the Agent to write code, gather information, build slides, summarize a meeting, read a PDF, work on spreadsheets, handle expense reports, plan a project, and generate a weekly report. Each kind of task has different input structure, tool permissions, quality criteria, risk level, and delivery format.

A single Agent can temporarily play different roles via Skills, but role-playing is not the same as role specialization. Real specialization, from the context perspective alone, has at least four dimensions: different tools, different context, different memory, different skills. From the result side, output protocol and acceptance criteria are also different. Suppose we have already built the Agent Team system above — Agents with different responsibilities can repeatedly meet tasks in their own domain, turn pitfalls into memory and valuable actions into Skills, like a group of colleagues who work long-term with the user and keep getting better at their respective jobs.

![](https://filecdn.minimax.chat/public/agent-team-role-l-1779893281293.jpeg)

![](https://filecdn.minimax.chat/public/agent-team-role-r-1779893281294.jpeg)

## 2. Multi-Agent collaboration in the industry today

| Product / Engine | How Multiple Agents Collaborate | Strengths | Limitations |
| --- | --- | --- | --- |
| OpenAI Agents SDK | One agent can hand off a task to another, or temporarily call another agent for specialized results and then continue itself. The framework persists the conversation, checks I/O compliance, and records execution. | Clear collaboration model, suitable for splitting tasks across specialized agents;  Built-in safety checks and process recording, easy to productize;  Suitable for customer service, business processes, and tool-calling scenarios. | Multiple agents usually relay in sequence — limited native parallelism;  Agents run inside the same framework, so isolation is weak;  Better for in-product collaboration than large-scale independent task execution. |
| LangGraph | Places multiple agents inside an explicit workflow, with each agent owning one step. A supervisor agent can decide who handles the next step, or complex tasks can be split into multi-layer teams. The system saves intermediate state for pause, resume, and human intervention. | Controllable flow, suitable for complex business logic;  Expresses branches, loops, and multi-layer tasks;  Supports progress save & resume, suitable for long-running workflows;  Outputs are traceable and debuggable, helpful for cost control; | Higher build and debug cost;  Agents mostly collaborate within the same system — weak standalone execution;  Complex workflows demand strong engineering design. |
| OpenCode | OpenCode itself is primarily a single-agent product and does not focus on multi-agent collaboration. Its core value is unifying commands, skills, permissions, and sessions on the same execution path, so it can serve as the low-level execution layer inside an external multi-agent system. | Unified command system, fine-grained permission control — solid as a reliable coding agent;  Human and agent operations share the same rules; well suited as an execution engine inside a larger system. | No complete multi-agent team mechanism internally;  Does not handle inter-agent division, communication, verification, or scheduling;  Team collaboration must be supplemented by an external system. |
| OMC / oh-my-claudecode — Team Pipeline | Multiple agents relay across stages: plan, requirements, execute, verify. On verification failure, the pipeline enters a repair stage, then re-executes or re-verifies until completion or terminal failure. | Complete process covering plan, requirements, execution, verification, and repair;  Continues fixing after verification failure — never stops at half-done;  Good fit for complex coding tasks. | Heavyweight flow — high overhead for simple tasks;  Depends on terminal environment and multiple background windows;  Fixed stages — high cost to adjust the plan mid-flight. |
| Claude Code — Teams | A Lead Agent creates the team and assigns tasks to multiple Teammates. Each Teammate has an isolated context, model, and permission set, and can execute tasks independently. The Lead dispatches tasks, monitors status, sends messages, and closes members; Teammates report status when finished. | Deeply integrated with Claude Code, coherent UX;  Context isolation between members, suitable for parallel division of labor;  Full task management, messaging, idle notifications, and close confirmation — relatively complete team collaboration. | Scheduling relies on the Lead Agent’s own judgment — stability depends on the model;  Complex dependencies are not explicit enough;  Some run modes depend on terminal windows — limited long-running cross-session capability. |
| OMC Ralph Loop / Ralph Mode | Ralph keeps the task moving forward. It typically pairs parallel execution with verification: multiple execution units push the task, then results are checked repeatedly; problems get patched until pass or limit. | Emphasizes quality of completion, suitable for tasks needing repeated polishing;  Bridges execution and verification, reducing the "half-done and stopped" pattern;  Suitable for complex development and repair work. | Higher runtime and cost;  If the check criteria are unclear, repeated fixes may produce limited gains;  Iteration cap, cost cap, and stop conditions must be set. |
| OMC Autopilot + Ralph | Autopilot splits a task into a full chain: analyze requirements and technical approach, draft an implementation plan, execute, then let Ralph keep completing and repairing, ending with build, check, test, and multi-angle verification. | Covers the full process from requirement understanding to final verification;  Suitable for fully automated complex-task execution;  Ralph keeps fixing problems after execution, improving delivery quality. | Long system flow — fits complex tasks, not lightweight tweaks;  Each stage depends on the previous one — misunderstanding upstream poisons downstream;  Clear acceptance criteria are required, otherwise late-stage verification quality drops. |

## 3. MiniMax Agent Team: giving every Agent more freedom on top of a constrained multi-Agent loop

MiniMax's Agent Team is a multi-Agent system led by a main Agent that splits complex tasks into parallel sub-tasks dispatched to a batch of Agents, with adversarial quality gates baked in — an Agent loop driven by deterministic code logic. Inspired by Ralph-Loop and Harness, we recognized that model context is precious; by splitting tasks and classifying responsibilities, each step gets context isolation, raising the overall quality of Agent output.

![](https://filecdn.minimax.chat/public/agent-team-team-overview-l-1779893281295.jpeg)

![](https://filecdn.minimax.chat/public/agent-team-team-overview-r-1779893281296.jpeg)

- **The basic collaboration flow of Leader, Worker, and Verifier**

To turn multi-Agent from concept into a usable product, you need a basic collaboration flow. We have simplified it to three role types: Leader, Worker, and Verifier.

Leader translates the user goal into a task structure.

Worker executes specific sub-tasks. Different Workers can have different tools, context, and output requirements. Some Workers do research, others edit code. Worker value lies in specialization: the clearer the role, the more easily Worker outputs can be reused, compared, and inspected.

Verifier turns “it's done” into “it can be delivered”. It can check sources, coverage checklists, and risk boundaries, and can also suggest changes to the Worker's result. This reflects Agent Team's design logic: Worker Agent and Verifier Agent are in an adversarial relationship. Both aim to finish, but one finishing triggers the other to start — much like R&D and QA inside a company, delivering high-quality results through multiple rounds of adversarial iteration, without requiring the CEO (the human user) to micro-manage.

![](https://filecdn.minimax.chat/public/agent-team-lwv-l-1779893281297.jpeg)

![](https://filecdn.minimax.chat/public/agent-team-lwv-r-1779893281298.jpeg)

- Compared with Task tools that can only create a task and receive a single round of results, **Agent Team is a team you can interact with at any time.**

Traditional Task tools usually live at the model tool-call layer: the main Agent calls a task / dispatch / spawn-style tool, passes a prompt, and waits for the sub-Agent to return a piece of text or summary. This mechanism fits short-lived, low-risk, locally exploratory tasks — for instance, asking another model to quickly search files, summarize materials, sanity-check an idea, or generate candidate answers. Even though there are SubAgents running in the background today, communication between Agents is essentially one shot of input/output — no multi-round dialogue, no real-time reporting of issues and conflicts.

To keep the Team running stably, we picked **a reliable state machine** to manage each Agent's run lifecycle. One lifecycle is one Session, and the state machine is the Team Engine. The Team Engine manages every task through producing, verifying, and done. When verifying fails, the Team Engine wakes up the producing node again to keep editing. The Leader gets the Team Engine's latest status throughout, can proactively confirm task details, and can even send supplementary prompts to the producing or verifying Agent that is currently running. The collaboration relationship is no longer constrained to one function call, but becomes proactive push + on-demand query in a multi-round interaction.

Every Agent Team run carries long-term value. The experience from this run can be deposited into memory and **Skills**, so each specific Agent becomes more proactive about how to collaborate with the user and finish tasks efficiently, and so all Agents understand the user better.

![](https://filecdn.minimax.chat/public/agent-team-engine-l-1779893281299.jpeg)

![](https://filecdn.minimax.chat/public/agent-team-engine-r-1779893281300.jpeg)

- **Inter-Agent communication design: Agents and humans have equal rights**

When designing how Agents should collaborate, the most direct line of thought is to look at how humans and Agents collaborate today. Users can prompt, spawn, abort, and kill an Agent through the front-end UI, which means an Agent itself should also be able to perform those actions on another Agent. We abstract the user's operations on an Agent as an interface, and the actual operator of those operations can be the user, another Agent, or the Agent Team engine.

![](https://filecdn.minimax.chat/public/agent-team-comm-l-1779893281301.jpeg)

![](https://filecdn.minimax.chat/public/agent-team-comm-r-1779893281302.jpeg)

Of course, this design must keep its boundaries: “equal rights” does not mean Agents get unlimited permissions, and it does not mean humans step out of the accountability chain. Quite the opposite — only when Agents and humans share the same auditable collaboration surface do permissions, responsibilities, and risks become easier to see.

### 3.1. Core scenario 1: IM integration, async execution with fast response

IM interaction constraints are peculiar. When the user sends a message, they expect feedback within seconds, but many tasks naturally need minutes or even hours to execute: researching, drafting meeting minutes, building slides, running tests. If the system makes the user wait for the final result, the experience becomes “the Agent went missing in the chat box”.

A single Agent here easily falls into a dilemma: either deliver a shallow answer for a fast reply, or finish the full task at the cost of long silence. Worse, IM conversation keeps going — the user may add new requirements, switch topics, or ask another question mid-flight. If long tasks and the current conversation are bound to the same context, the system cannot keep response speed up and cannot keep background tasks free of pollution from new messages.

This echoes the design principles for long-running tasks, status updates, and human-in-the-loop in Google's A2A protocol. Anthropic's Managed Agents blog argues that “session is not the same as a model context window”, and that long tasks need a recoverable session log as the external context object.

Industry consensus is forming: the underlying logic of IM async execution is that when a task spans multiple message rounds, multiple tools, and multiple Agents, you cannot rely on any one model's current context staying intact. The system must persist task state, event logs, file artifacts, and decision records as recoverable objects. Agent collaboration is a stateful long-term task.

![IM 异步执行场景](https://filecdn.minimax.chat/public/agent-team-core-im-1779893281303.jpeg)

IM 异步执行场景

### 3.2. Core scenario 2: Coding Harness

The Agent Team project draws heavily on the Harness mindset. Harness pushes a step further from “Agent writes code”: an Agent must follow the full development lifecycle — code lives on branches, execution in sandboxes, edits as diffs, tests that can rerun, reviews that leave records, failures that can be replayed, and when needed, tasks that can be split across roles. Stop conditions for the Agent are bound to deterministic, observable external systems.

- **Division of developer / tester / reviewer roles in coding tasks**

An engineered Coding Harness contains at least four role types.

Leader is the control plane. It first judges whether the task is worth starting a Team for: **fixing typos or replacing constants may be cheaper for a single Agent or a script; cross-file understanding and parallel comparison of approaches is what Team is for**. It also decides the granularity: should we read the code first, explore approaches in parallel, write reproduction tests first, how many retries on failure, and when to escalate to a human.

Developer owns the implementation, with a clear work brief: **requirements, relevant files, project constraints, and forbidden actions**. Its output is not only natural-language explanation, but also reasons for the change, potential risks, and verification suggestions.

Tester turns “it looks runnable” into “there is external evidence”. It locates existing test entry points, compresses failure logs, and adds a minimal reproduction when needed. The key is tool-grounded: verification results come from commands, tests, or executable checks.

Reviewer is not the same as Tester. Tests answer “did it pass the known checks?”; Review cares about “should it be changed this way?” It examines abstraction boundaries, compatibility, error handling, dependencies introduced, permission expansion, and whether logs leak sensitive info. Reviewer can also **run in parallel with specializations**: a general reviewer for maintainability, a security reviewer for input / credential / network boundaries, a domain reviewer for business semantics.

- **How automated testing, code review, and human acceptance plug in**

Layer one is automated testing and static checks. Harness treats test, lint, build, and format check as first-class citizens. After the Developer changes the code, the Tester runs verification; on failure, the Leader decides whether to have the Developer fix it, ask the Tester for more logs, or escalate an environment problem.

Layer two is code review. A Reviewer Agent can do an automatic first pass to catch unused variables, missed exception branches, public-API breakage, dangerous shell calls, secrets in logs, out-of-scope file edits, and so on.

### 3.3. Core scenario 3: parallel information retrieval and research

A single Agent runs into slow research, polluted or dangerously injected context, evidence lost inside the context, and biased research directions. The value of Agent Team is to split research into parallel information channels, then merge results into structured conclusions via verifier and synthesizer. The focus is on designing a trustworthy research pipeline that is both fast and capable of escaping a single Agent's line of thinking, gathering and confirming information from different angles and from both sides.

- **How an independent verifier reduces citation errors and factual hallucinations**

Verifier first checks source verifiability. Formal sources should use stable URLs: official pages, conference pages, author blogs. Search caches and aggregator pages can serve only as leads, not as evidence for a formal conclusion. Verifier also checks whether the source status is stale and whether counter-evidence denies the truth of the claim.

![并行信息检索和研究](https://filecdn.minimax.chat/public/agent-team-core-research-1779893281304.jpeg)

并行信息检索和研究

### 3.4. Core scenario 4: pipeline-style office document writing

When a single Agent writes a document, the easiest illusion is: as long as the model can write, it can deliver. When the user says “help me create a report / Excel / PDF”, a single Agent often generates a big block of text first, then tries to format, check, and fix in one pass. Short documents can survive on one context window; once the task grows into a long report, formal contract, or financial spreadsheet, the problems surface fast: content planning, sourcing, structural consistency, chart objects, headers/footers, and export quality all crammed into one context and one execution loop.

- **Agent Team takes the result from “producible” to “deliverable”**

Multi-Agent collaboration splits document delivery into multiple verifiable stages. Planner first defines the document goal and structure; Writer produces the body; Formatter handles layout and file objects; Evaluator independently checks content, formatting, and file integrity. This split turns “document generation” from a one-shot text generation into something closer to a CI/CD build pipeline: each step produces an intermediate artifact, each step has checks, and each step can be retried locally on failure.

![流水线式办公文档写作](https://filecdn.minimax.chat/public/agent-team-core-docwriting-1779893281305.jpeg)

流水线式办公文档写作

## 4. Hard problems and reflections during development

- **The context cost that Team collaboration brings**

A group of collaborating Agents exposes a new class of cost: handoff cost, sharing cost, and aggregation cost. None of these costs are “solved by a slightly larger model context window”.

Handoff cost: the same piece of information has to be reorganized between Agents. After the research Agent collects dozens of pages, it hands them off to the writing Agent. The writing Agent needs a document that has already been preliminarily researched. The writing Agent also has to hand off a writing result to the format-check Agent. Today we deal with this by making handoff artifacts: 1) readable handoff files, 2) a shared notepad file across Agents. Workers communicate slowly and non-disruptively through file paths plus summaries, avoiding stuffing everything into context at once.

Sharing cost: the price of “giving every Agent visibility into all information”. Every extra shared section costs every Worker tokens on every round. When an Agent hits a problem mid-execution, it should write memory in the right way so the lesson can be broadcast to all running and to-be-launched Agents' contexts. We use three approaches to maintain such shared information: 1) intra-Agent memory — this Agent's experience on this run; subsequent runs of the same Agent get the hint, and running Agents are also notified immediately; 2) inter-Agent communication CLI — Agents can directly talk to other running nodes for interrupt-style communication; 3) the whiteboard mentioned above — compared with 1 and 2 (which are proactive notifications), the whiteboard supports persisting larger volumes, and other Agents can pull on demand more gracefully when needed.

Aggregation cost: the work needed to merge multiple Workers' outputs into one deliverable. It is easy to collect 10 versions of materials in parallel, but hard to merge them into one article whose facts are consistent, whose citations line up, and whose style is unified. At this step the Leader's job is “merge 10 into 1”, not “call in a few more people for more material”. Acknowledging that this is expensive is the first step in designing a Team.

- **The trade-off between time / token consumption and result ROI**

Multi-Agent in prior research has rarely been equated with high ROI. The paper Cost of Consensus claims that under specific models and homogeneous debate setups, consumption can reach 2.1–3.4x the tokens of isolated self-correction, with accuracy that does not improve and sometimes gets worse. The conclusion is clear: “more” without structure and without stop conditions only spreads uncertainty in parallel — a simple AI chatroom can hardly guarantee the quality of the final output.

ROI also includes user waiting. Even though we made long tasks async and let users chat with the Leader Agent any time — reducing the user's need for instant exchange — overall delivery time still grows. Compared to a single Agent finishing it all in one pass, Agent Team unavoidably executes 1-2-3-4 in order. We thought a lot about how to control reasonable splitting granularity and balance “big tasks deliver poorly” vs “over-split tasks deliver too slowly”. We believe that as model intelligence rises, running the Team in the background and reporting actively when done trades a task structure for the psychological cost of “staring at the Agent slowly generate in the same conversation”. The value of multi-Agent shows up here together with its cost: users are willing to wait longer for verifiable, recoverable, auditable results — as long as the process is transparent.

And we believe that once users see the high-quality results delivered by Agent Team, **their trust in Agents will rise, so they free up their own bandwidth for deeper, broader thinking — to be a thoughtful person with humanity, and hand the execution-of-thought and delivery-of-result tasks to Agent Team**.

- **The cost of Verifier, retries, and Leader decision**

Verifier is the key for a Team to move from demo to delivery.

The first cost is verification itself. A coding task has to run tests; a research task has to cross-check sources and confirm citation boundaries; the more rigorous the verification, the higher the cost; verification that just goes through the motions leaves only a false sense of “it seems to pass”.

The second cost is the retry strategy. If a Worker keeps spinning in “edit a bit — get rejected by the verifier — edit a bit”, the whole plan only gets more expensive.

The third cost is that Leader decisions cannot be fuzzy. In front of high-risk actions — merging code, overwriting production data — the final judgment must be signed off by a human. GitHub Copilot cloud agent's official docs keep the entire flow inside GitHub: plans, commits, logs, and PRs are all reviewable by the team; the changelog also notes that safety and quality analysis runs before a PR is finalized.

The direction it points to is clear: Agent delivery includes not only the result, but also a replayable, accountable trace.

- **A multi-Agent system is a runtime, not prompt orchestration**

Stepping away from model and context, back to how we built the system: multi-Agent is often simplified into “write a few prompts / skills and let the model role-play”. In our actual code, this simplification is only the initial demo; the real complexity is hidden in details, all so the user enjoys the smooth experience of “just chat”. Team Engine needs to manage many complex objects and state transitions so the Agent Team runs are sufficiently automated and observable. The rendering layer must absorb operations on the same concept from multiple actors — user, Agent, Team Engine, etc.: for instance “create a task” can come from many sources. Another source of rendering complexity is message origin. Besides user-Agent dialogue, there is dialogue between Agents, messages from scheduled jobs, periodic monitoring from Team Engine, and user messages from IM. The heavy software engineering behind the scenes is all to let the user browse a carefully arranged set of information sources from a clean UI.

Industry materials point the same way. OpenAI Agents SDK's official docs emphasize sandbox, workspace, handoff, and tracing; AWS AgentCore's official release lists Runtime, Memory, Identity, Gateway, Browser as enterprise modules. They jointly signal one thing: the center of gravity of Agent products is moving from “writing prompts” to “maintaining the control plane”.

Acknowledging that Agent Team is a runtime changes product judgment. New features cannot be patched only by prompts — they need events and observability in the runtime; permissions, runtime constraints, and memory-write constraints cannot rely only on Agent self-discipline — they need appropriate soft/hard gates and interceptors. Maintaining multi-Agent as a runtime is much heavier than maintaining it as a prompt template, but only that way can it serve real work reliably.

## 5. Lessons

### 5.1 Multi-Agent exists to complete complex tasks more reliably

The core of multi-Agent is structure. Multi-Agent without structure is just more expensive concurrency; multi-Agent with structure is a delegable, parallel, verifiable execution system.

So when judging whether a **multi-Agent product is valuable**, don't look at how many Agents it can launch at the same time. Look at whether it can answer a few questions: why split, how to verify, when to stop, how to recover from failure, how to manage memory. The clearer the answers, the more multi-Agent looks like a production system; the muddier the answers, the more it looks like a demo group-chat.

### 5.2 Team value depends on complexity, but ROI cannot be judged on the short term alone

Team is only one option. The longer the task, the deeper the chain, the higher the risk, the more reusable the experience — the more Team's gain is likely to beat its cost; the shorter, lower-risk, and more deterministic the task, the more a single Agent or classic automation wins. We should not encourage users to “spin up a Team for everything”, but help them judge when collaboration is worthwhile and when simplicity should be kept.

Whether you pick Team or a single Agent for execution, you still need memory, Skills, and similar mechanisms so Agents keep improving over the long term. Even if Team uses more tokens and more time, the Agent should walk away with more experience and more memory. From a long-term view, the growth of an Agent that understands the user better and is more seasoned should be part of the ROI calculation. Because once we believe an Agent owns enough memory and Skills, Team should be the most hands-free execution mode for the Agent.

### 5.3 The future Agent will look more like a long-term digital team

Following the design mentioned in “Inter-Agent communication design: Agents and humans have equal rights”, future Agent products will open fully reciprocal control interfaces and data flow to both humans and Agents. Humans will lean more on a management panel to configure Agent roles, capabilities and boundaries, and to assign tasks, deferring to human judgment at key checkpoints. And that panel itself can be controlled by an Agent. The overall runtime may look closer to the low-efficiency AI chatroom mentioned earlier. Whether AI can fully take over management and scheduling so the management panel / Team Engine becomes lighter and lighter — that still depends on stronger models showing up.

Multi-Agent exists to move AI from “one-shot tool” to “long-term partner” — and from boosting individual efficiency to freeing humans from the specific work of execution.

## 6. Open source and how to use it

Our latest MiniMax Agent will be open-sourced soon. Given the size of the work and the pace of internal iteration, the open source release is expected to land together with the MiniMax M3 model.

Before open source, our desktop app is already officially released, and you are welcome to download and try it:

https://agent.minimaxi.com/download

. Today, a single MiniMax subscription gives you access to both Agent and TokenPlan.
