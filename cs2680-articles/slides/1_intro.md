---
title: "1_intro"
source: https://cs2680.seas.harvard.edu/slides/1_intro.pdf
pages: 50
crawled: 2026-11-16
---

# 1_intro

> PDF 讲义文本抽取：[1_intro.pdf](https://cs2680.seas.harvard.edu/slides/1_intro.pdf) · Harvard CS2680

Modern AI Systems: Agents 
and System Optimizations
Juncheng Yang
Overview 
https://cs2680.com

2Harvard Madsys    ·   course.agentic-system.org
Plan for today
• Course overview
• Policy and logistics
• AI systems and agentic systems

3Harvard Madsys    ·   course.agentic-system.org
About me
Juncheng Y ang
• Assistant Professor at SEAS
• Graduated from CMU in 2024
• Previously, AWS, Snowflake, 
Cloudflare, Twitter

5Harvard Madsys    ·   course.agentic-system.org
Harvard MaDSys (Measurement and Design of Computer Systems) Group
Efficiency
less resources
higher utilization
Storage Systems
Reliability
less downtime
more robust
faster
more scalable
Performance
less carbon emission
Sustainability
Agent Serving Systems
Caching
Sustainable storage
Context management
LLM serving optimizations
People find solutions, we find problems; 
we measure, design, and operate real systems

6Harvard Madsys    ·   course.agentic-system.org
Me and TFs
Juncheng Y ang Yiyu Liu Yunjia Zheng
Office hour: by appointment
cs2680-staff@g.harvard.edu
Office hour: by appointment Office hour: by appointment
Course staff email

Harvard Madsys    ·   course.agentic-system.org 7
I will try to remember everyone’s name
Please say your name first before asking or 
answering questions

8Harvard Madsys    ·   course.agentic-system.org
Each table selects a leader to introduce everyone at the table
Next, Your Turn
5 minIntroduce yourself to others at your table
• name and where you are from
• program, year and background
• research interest
• why you take this class and what you hope to learn

Harvard Madsys    ·   course.agentic-system.org 9
The course
What you will learn, the assignments, 
and the project

10Harvard Madsys    ·   course.agentic-system.org
What is this course about
Agentic AI Systems A graduate-level computer 
systems course
• Expected background: one 
graduate-level systems course 
(OS, networking, databases, 
architecture)
• Experience with real systems
• Agent design
• LLM / agent serving systems

11Harvard Madsys    ·   course.agentic-system.org
What you will learn in this course
Foundations
First few classes
Systems for LLMs & agents
Majority of the classes
• GPU programming and kernels
• Batching, scheduling, memory 
management
• Load balancing and routing
• KV-cache and prefix-cache
• Agent serving systems and other 
optimizations
• Introduction to LLMs and agents
• How to use Claude Code
• How to design a coding agent
• How to optimize your coding agent

12Harvard Madsys    ·   course.agentic-system.org
Five assignments (1–3)
1 2 3
Build a web UI for 
Claude Code
Build a simple coding 
agent
Optimize your coding 
agent
• Solve a set of simple 
problems
• Create new problems for 
the assignment 3 
leaderboard
• Open-ended: context, 
memory, test-time 
scaling, routing, sub-
agents, tool call
• Metrics: accuracy, cost, 
latency
• Experience the magic 
of coding agents
• Understand the 
lifecycle of coding 
agent

13Harvard Madsys    ·   course.agentic-system.org
Five assignments (4–5)
4 5Serve your agent Optimize the full stack
• The hardest assignment — harder tasks 
• Open-ended: quantization, routing, fine-
tuning, engine–agent co-design
Scored on the leaderboard
Assignments 3 & 5: leaderboard ranking + 
baseline improvement
Do NOT take this class if you care about 
GPA
Expect 10+ hours every week
• From a commercial API to a small model
• Co-tune your agent and the serving 
engine for performance

14Harvard Madsys    ·   course.agentic-system.org
Project 
1
Build a tool
Find a gap and build a tool you will 
actually use
2
Research
A research project — talk to the TFs 
first
• Open-ended, individual project + AI
• Poster and demo session during reading period
• Grading: code + report +  poster / demo peer review

Harvard Madsys    ·   course.agentic-system.org 15
A lot of learning happens
after class
Learn the skills to 
learn — we provide 
pointers
Hands-on class: learn 
by doing the 
assignments
Class time is limited

Harvard Madsys    ·   course.agentic-system.org 16
Grading, policy and logistics
The parts worth reading carefully

17Harvard Madsys    ·   course.agentic-system.org
Grading 
4 Late days throughout semester 20% penalty per day for late submission
Participation  4%
Bonus  10%
course feedback + problems that AI 
cannot solve
Assignment 3 and 5 sharing sessions are 
based on leaderboard ranking
Five assignments  70%
1, 2, 4: 10% each · 3, 5: 20% each
Project  16%
Presentation  10%
paper + assignment 1
Alert: 20% A grading policy enforced  ·  an A or even A- is hard to earn

18Harvard Madsys    ·   course.agentic-system.org
Enrollment 
40
planned and budgeted 
capacity
80
enrolled today
68+10+6
prospective, cross-
registration and waiting list
Auditing
Allowed only if Harvard policy permits 
and a seat is available
Cap has increased to 80
However, computing resources might 
not increase proportionally
It is likely that you may not be able to 
get a GPU on the assignment due date

19Harvard Madsys    ·   course.agentic-system.org
Policy: using AI in this course
Read the assignment submission page on the course website
Disclosure required
What worked and did not work
Upload your session log
Required with each assignment
Using AI is encouraged
However, you should reason about AI-generated code, and you are 
responsible for all code you submit

20Harvard Madsys    ·   course.agentic-system.org
Policy: attendance and laptops
No video recording
See the website for the full policy
Attendance required
In-person attendance is expected
Laptops allowed
If you plan to keep yours open, please 
sit at the back
Guest lecturers
Meeting sign-up opens a week before
Class is not recorded

21Harvard Madsys    ·   course.agentic-system.org
Other logistics: computing
Read the computing page on the website
Claude Code API access
 GitHub
Private repo, shared with 
staff
Class HPC
• Everyone with Canvas access is already 
on the system
• SLURM-based; RTX 6000 PRO Blackwell
• Course work only
AWS
• Sign up and fill in the Google Form 
before Friday
• Terminate or turn off your instance 
when not in use
api.cs2680.com

Harvard Madsys    ·   course.agentic-system.org 22
Schedule may change during the semester
The first time offering this course: expect a bumpy ride ahead!
Grading may change as well (paper reading)
Week 1 Week 14

Harvard Madsys    ·   course.agentic-system.org 23
A few questions first
To help me understand everyone’s 
background

Harvard Madsys    ·   course.agentic-system.org 24
How many computer systems courses have you 
taken?
Operating systems Distributed systems Databases
Computer networking Computer architecture … anything else

Harvard Madsys    ·   course.agentic-system.org 25
How many of these topics are you familiar with?
Transformer 
architecture TP / PP / DP / EP
iteration-level 
scheduling / 
pagedAttention
Linear attention GPU 
programming Linux kernel

Harvard Madsys    ·   course.agentic-system.org 26
How have you used AI?
1
Chat
2
Coding agent
MCP , Skills / Plugins, subagent, 
parallel agent
3
Customized agent

27Harvard Madsys    ·   course.agentic-system.org
Agentic Coding Levels
0 No AI  —  hand-written code
1 Assist  —  AI autocompletion
2 Supervised  —  AI writes functions, you review
3 Scoped  —  hand off a task, review the code
4 Goal-driven  —  AI writes all, tests verify
5 Parallel agents  —  sub-agents split the work

Harvard Madsys    ·   course.agentic-system.org 28
Part I — AI Systems
How they differ from traditional 
computer systems

29Harvard Madsys    ·   course.agentic-system.org
What is an AI System? 
Many moving parts: scheduling & orchestration, state management, communication, 
caching, fault-tolerance, security , observability…
* AI systems a broad term, this course narrowly focuses on LLM systems.
AI / ML
“What model should we use?” / ”How 
should I design the model”
• Pick a model and write a Python script 
to solve the task
• Optimizes for accuracy and capability
AI Systems
“How do we train and serve it at scale?”
• Maximum GPU utilization 
(performance)
• Minimal resource waste (efficiency)
• Minimal downtime (reliability)
• Lower carbon footprint (sustainability)

30Harvard Madsys    ·   course.agentic-system.org
Why should you care about AI systems? 
This is where capability becomes product
… and it is harder than the AI itself 
Critical digital infrastructure
Understand model design Design better products More job opportunities

31Harvard Madsys    ·   course.agentic-system.org
How AI systems differ: compute
Heterogeneous computation
• CPU: tokenization, kernel launch, data movement, tool calls — GPU: matmul
• Mixed GPU generations and xPUs
Distinct phases of computation
• Prefill is compute-bound; decode is memory-bandwidth-bound
• The same deployment hits different bottlenecks: compute, bandwidth, capacity
Unpredictable execution time
• Output-length dependent, which complicates scheduling

32Harvard Madsys    ·   course.agentic-system.org
How AI systems differ: non-deterministic compute
Distributivity also fails: a * (b + c) != a * b + a * c, but not used widely
Transitivity: a == b, b == c does not imply a == c
Why it happens
• Floating-point addition isn’t 
associative — rounding at 
every operation
• Butterfly effect: a 7th-decimal 
shift in a matmul flips the next 
token
Where it comes from
• Runtime: warp/block scheduling, memory 
ordering, async streams, batch size
• Software: fused multiply-add vs two ops, 
autotuning, subnormals
• Hardware: CUDA vs tensor core, Hopper FP8 
vs Blackwell micro-scaling tiles
Approximate computing is acceptable

33Harvard Madsys    ·   course.agentic-system.org
How AI systems differ: memory, storage and 
communication
Huge state
• Model weights: GBs to TBs
• KV-cache: 10s–100s KB per token
• Prefix cache: KV reuse across 
requests
• Data movement is the bottleneck
Multi-GPU communication
• Pipeline / tensor / expert / context 
parallelism
• Collectives: NCCL, UCCL
• Topology: NVLink, 
Ethernet/InfiniBand
• CPU and kernel bypass: RDMA

34Harvard Madsys    ·   course.agentic-system.org
How AI systems differ: fast-moving models and 
workloads
Rapidly-evolving 
model architecture
• MHA, GQA, MLA, NSA, 
linear attention…
Rapidly-evolving workloads
• Multi-turn chat: interactive, latency-sensitive
• Problem solving: reasoning with long output
• RAG: retrieve doc before answering, long context
• Agents: long context, prefix-cache critical, routing 
and load balancing
Adapt model to hardware 
  design hardware for model architecture

35Harvard Madsys    ·   course.agentic-system.org
How AI systems differ: reliability, power and energy
Reliability
• 9% AFR, 50,000hr MTBF
• One GPU fails every 3 hours in a 
16K-GPU cluster
Power and energy
• CPU 100–300W; GPU 700–1000W, 
4–8 GPUs per server
• Server power 800W → 6,000W, an 
8x increase
• How to avoid power fluctuation

Harvard Madsys    ·   course.agentic-system.org 36
Part II — Agentic AI Systems
What an agent is, and why it is a 
systems problem

37Harvard Madsys    ·   course.agentic-system.org
What is an AI agent? 
Memory
LLM
Reasoning & Planning
Agent
Action
Observation
Environment
An AI agent is an autonomous software system that 
uses an AI model to reason about a goal, use external 
tools, and execute multi-step actions until a task is 
finished
1. plan — break the task 
into sub-steps
2. act — call external 
tools (APIs, databases)
3. observe — interpret the 
results of those tools
4. adapt — revise the plan 
on new information
5. deliver — return the 
final result

38Harvard Madsys    ·   course.agentic-system.org
Why do we need an AI agent? 
LLMs are strange computers: superhuman and incompetent at the same time
Superhuman at
• Recalling vast factual knowledge
• Language
• Pattern matching
• Generating code
• Operating across many domains
Surprisingly weak at
• Persistent memory
• Reliably understanding context
• Avoiding hallucinations
• Knowing what they don’t know
• Security and adversarial input
https://www. youtube.com/watch?v=LCEmiRjPEtQ&t=874

39Harvard Madsys    ·   course.agentic-system.org
Agents as a new kind of computer
LLM
Context window
Tools
Agent Harness
Agent
An LLM is more than a smarter CPU
a new kind of programmable computer — with a completely different programming model and 
failure model
→
→
→
→
→
CPU
RAM / working memory
Peripherals
OS
Application

40Harvard Madsys    ·   course.agentic-system.org
Why are agents a systems problem?
Many turns: the critical path spans GPU, CPU, storage, network and external services.
Traditional LLM serving
request inference response
Agent serving
infer tool infer tool retrieval infer …
Dependencies between steps Highly variable step latency Blocking / waiting on tools
Rapidly growing state Concurrency & speculation Failures anywhere in 
trajectory

41Harvard Madsys    ·   course.agentic-system.org
The agentic systems stack
Application / User
Agent / Harness   planning · context · memory · tools · subagents
Model
Serving System
batching · scheduling · routing · caching
Runtime / Kernels
CUDA · Triton · collectives
Hardware   GPU · CPU · memory · network · storage
External Environment Agent
Serving
Hardware
co-design
Tools
web · files · APIs · humans
Systems
scheduling · caching

42Harvard Madsys    ·   course.agentic-system.org
What are we optimizing?
Throughput is the wrong objective for an agent.
maximize   task success
subject to latency cost resources reliability security
Useful, but insufficient What we actually optimize
TTFT / TPOT
Tool-call latency
GPU utilization
More tokens/sec can still mean a slower, 
costlier agent.
Task success / accuracy
End-to-end latency
Tokens / task
$ / successful task
Energy / successful task

43Harvard Madsys    ·   course.agentic-system.org
Agentic systems introduce new systems problems
Every property of an agentic workload names a systems problem this course will study.
Long trajectories
→ state & context management
Repeated prefixes
→ prefix caching
Tool dependencies
→ dependency-aware scheduling
Variable tool latency
→ asynchronous execution
Multiple agents
→ orchestration & communication
Huge context
→ memory hierarchy & retrieval
Branching reasoning
→ speculative execution
Different models
→ routing
External side effects
→ security & isolation
Long-running tasks
→ checkpointing & fault tolerance

44Harvard Madsys    ·   course.agentic-system.org
Observability is a first-class problem
For agents, the distributed trace becomes a nested trajectory.
Session
Turn
Agent step
Model request
Tool call
Tool result
Agent step
Subagent
…
You cannot optimize 
what you cannot 
observe.
 

45Harvard Madsys    ·   course.agentic-system.org
Questions you will think about in this course
1   Why does batching improve throughput but 
hurt agent latency?
2   When should an agent use a larger model?
3   Where should KV / prefix state live?
4   How should requests from the same agent 
be scheduled?
5   Can tool calls overlap with inference?
6   When should we spawn a subagent?
7   How do we route across heterogeneous 
GPUs and models?
8   How do we recover a 30-minute agent when 
something fails?
9   How do we optimize $ / successful task, not 
tokens / sec?
By the end of CS2680, you should answer 
these quantitatively.

46Harvard Madsys    ·   course.agentic-system.org
What we will not cover in this course
• Training (inference dominates compute demand)
• data pipeline
• checkpoint
• pre-training, fine-tuning, post-training, RL rollout 
• cluster management
• Model architecture design
• Other topics related to inference
• Communication 
• Power and energy
• New hardware design

47Harvard Madsys    ·   course.agentic-system.org
Next class
• LLM basics

48Harvard Madsys    ·   course.agentic-system.org

Harvard Madsys    ·   course.agentic-system.org 49
Optional reading

50Harvard Madsys    ·   course.agentic-system.org
AI agents vs. AI assistants vs. bots
AI agent AI assistant Bot
Purpose Autonomously and 
proactively performs tasks Assists users with tasks Automates simple tasks or 
conversations
Capabilities
Complex, multi-step 
actions; learns and adapts; 
decides independently
Responds to prompts; can 
recommend actions, but 
the user decides
Follows pre-defined rules; 
limited learning; basic 
interactions
Interaction Proactive; goal-oriented Reactive; responds to user 
requests
Reactive; responds to 
triggers or commands
https://cloud.google.com/discover/what-are-ai-agents

51Harvard Madsys    ·   course.agentic-system.org
Key differences: autonomy, complexity, 
learning
Autonomy
Agents operate and decide independently to reach a goal. 
Assistants need user input and direction. Bots follow pre-
programmed rules.
Complexity Agents handle complex tasks and multi-step workflows. 
Assistants and bots suit simpler tasks and interactions.
Learning Agents use machine learning to adapt over time. Assistants may 
learn somewhat. Bots learn little or not at all.
