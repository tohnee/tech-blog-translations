---
title: "Forge: Scalable Agent RL Framework and Algorithm"
date: 2026-02-14
source: https://www.minimax.io/blog/forge-scalable-agent-rl-en-1779896141
crawled: 2026-09-22
---

# Forge: Scalable Agent RL Framework and Algorithm

2026-02-14

AIRLForge

![Forge RL framework hero](https://filecdn.minimax.chat/public/forge-hero-1779895280980.jpeg)

Forge RL framework hero

Scaling reinforcement learning for real-world agents runs into a three-way conflict: **system throughput**, **training stability**, and **agent flexibility** all pull in different directions, and that tension has long blocked industrial-grade RL.

This post describes how our internal RL framework **Forge** breaks that triangle by combining a flexible system architecture, an algorithm tuned for long-horizon agents, asynchronous scheduling that respects the training distribution, and aggressive training/inference optimisations. Standardised interaction protocols let Forge train arbitrary agent scaffolds at scale, which is what enabled the breakthrough capabilities of the MiniMax M2.5 model.

During the build of MiniMax M2.5, Forge worked with more than one hundred thousand distinct real-world agent scaffolds and environments. With context lengths reaching 200k and a daily throughput on the order of millions of samples, the system stayed convergent on reward and lifted the underlying model on capability. Combined with our CISPO algorithm and composite reward design, M2.5 advances what efficient, reliable real-world productivity looks like — and pushes our mission of *Intelligence with Everyone*.

## 1. Problem Formulation

Before going into architecture, we frame the objective. The Agent RL system is designed to maximise an **Effective Agent Training Yield** **J**:

max⁡θJ(θ)=Throughput(A)×Sample Efficiency(A)s.t.∀A∈Ωagent(Arbitrary Agent)E[Update Variance]<δ(Stability)E[∥J(T)−J∗∥]<ϵ(Convergence)\begin{aligned} \max_{\theta} J(\theta) = & \text{Throughput}(\mathcal{A}) \times \text{Sample Efficiency}(\mathcal{A}) \\ \text{s.t.} \quad & \forall \mathcal{A} \in \Omega_{\text{agent}} \quad (\text{Arbitrary Agent}) \\ & \mathbb{E}[\text{Update Variance}] < \delta \quad (\text{Stability}) \\ & \mathbb{E}[\|J^{(T)} - J^*\|] < \epsilon \quad (\text{Convergence}) \end{aligned}θmax​J(θ)=s.t.​Throughput(A)×Sample Efficiency(A)∀A∈Ωagent​(Arbitrary Agent)E[Update Variance]<δ(Stability)E[∥J(T)−J∗∥]<ϵ(Convergence)​

Here **System Throughput** is raw tokens processed per second, bounded by four components — rollout, training, data processing, I/O. **Sample Efficiency** is the average improvement per sample, driven by data distribution, data quality, algorithm efficiency, and off-policy-ness. The constraints in the formulation are proxy signals for stability and convergence. Three structural problems stand in the way of maximising J; we cover them next.

### 1.1 Agent Extensibility and Framework Flexibility

Today's RL paradigms put a glass ceiling on agent complexity for two structural reasons:

**Restricted Agent Autonomy.** Standard frameworks treat the agent as a white-box function and share state between the agent and the trainer. That rigidity makes it hard to model complex cognitive architectures — for example dynamic context management or multi-agent collaboration — and prevents the trained capability from generalising onto arbitrary black-box agents that do not honour those assumptions.

**Token Consistency Barrier.** Existing token-in/token-out (TITO) architectures couple the agent tightly to the underlying token logic. Keeping the inference-side abstraction (the high-level loop) and the training-side representation (token-level data) in lock-step is computationally expensive once any non-trivial context management is in play.

### 1.2 System Efficiency and Compute Redundancy

Agent rollout times have extreme variance — from seconds for a simple API call to hours for long reasoning chains. That creates a scheduling deadlock:

**Asynchronous Controller.** There is a sharp trade-off between hardware efficiency and training stability. Strict FIFO/synchronous scheduling exposes the straggler effect: one slow task causes head-of-line blocking and idles the cluster. Greedy / first-finished-first-out modes recover throughput but at the cost of severe distributional shift — early in training the data is dominated by short easy tasks, and later by clustered hard ones. The non-stationarity destabilises optimisation and makes gradients oscillate.

**Prefix Redundancy.** In agent scenarios, the interaction between the tokenizer and built-in context management means a substantial fraction of requests share identical prefixes. Recomputing those prefixes wastes compute during training and creates its own engineering problems.

### 1.3 Algorithmic Challenges: Credit Assignment and Optimization Stability

**Sparse Rewards, High Gradient Variance.** Agent tasks are long-horizon with delayed feedback: a single outcome depends on a chain of thousands of actions. Attributing credit to specific tokens or tool calls within a 200k context window is statistically fragile. The resulting low signal-to-noise ratio in return estimation produces high gradient variance that destabilises training at scale.

**Latency-Agnostic Optimisation.** Classical RL objectives optimise correctness — step-wise or outcome rewards — and ignore wall-clock cost. Real agentic settings often admit multiple valid trajectories with very different latency profiles because of tool execution and serial processing. Without an incentive for parallelism or efficient tool use, you get agents that are correct but slow in practice.

## 2. System Architecture and Agent RL Paradigm

To soften the efficiency-vs-off-policyness trade-off and cut redundancy, we make the following architectural moves.

### 2.1 RL System Design

Rather than tie the system to a specific implementation, we use a generalised middleware design that decouples the agent's reasoning logic from the underlying training infrastructure. The system has three modules:

![Forge RL three-module system architecture](https://filecdn.minimax.chat/public/forge-rl-system-1779895280981.png)

Forge RL three-module system architecture

**Agent Side.** This layer abstracts the General Agent — both white-box and black-box scaffolds — together with its environment. It drives recursive environmental interaction and lets the agent behave as a pure trajectory producer. By isolating environment feedback from system overhead, the agent can focus on its own core logic (context management, reasoning chains) and stay agnostic to the training/inference plumbing.

**Middleware Abstraction Layer.** The bridge between Agent Side and Training/Inference Side, comprising the Gateway server and the Data Pool.

- **Gateway Server:** a standardised communication endpoint that handles completion requests between the agent and the LLM. Using common protocols, it hides the actual underlying model from the agent's behavioural logic.
- **Data Pool:** a distributed store that asynchronously collects rollout trajectories and reports from the agent. It buffers between generation and training, enabling flexible data processing and batching strategies for efficiency and algorithmic experimentation.

**Training and Inference Side.** Carries the heavy compute — the LLM (Rollout) Engine and the Train Engine.

- **Rollout Engine:** optimised for high-throughput token generation, serving requests forwarded by the middleware.
- **Train Engine:** consumes processed token sequences from the Data Pool and updates the policy, staying in sync with the Rollout Engine so the agent explores under the latest policy distribution.

Offline evaluation showed large performance gaps that were attributable to the scaffold rather than the model. Thanks to the modular framework, we can train across a wide variety of scaffolds without touching the agent internals, which lets the model generalise across scaffolds — that is, across environments. Engines and agents are fully decoupled, so plugging in new agents is mechanical. In total we have integrated hundreds of scaffold types and thousands of tool invocation formats.

### 2.2 White-Box Agent RL for Context Management (CM)

With white-box agents, full scaffold design and augmentation let us directly observe and optimise the model under specific agent architectures. Building MiniMax M2.5 surfaced several problems that hurt earlier models on long-horizon tasks needing active context management (such as DeepSearch):

**Context Rot.** As the number of turns grows, accumulated intermediate reasoning and redundant observations create attention dilution. The model loses focus on the critical bits even when it is strictly inside the absolute context window.

**Inference-Training Mismatch.** Context management does extend the effective interaction horizon at inference and helps long-context performance, but applying it only at inference produces a severe shift from the RL training distribution. The model is forced to absorb unexpected context transitions on the fly, which drags overall performance down.

To kill that distribution shift and keep the reasoning faithful, we fold CM into the RL interaction loop itself, treating context management as a functional action that drives state transitions:

**CM-Driven State Transitions.** CM becomes an explicit agent action; context transitions sit naturally inside environment dynamics. The transition from S_t to S_{t+1} implicitly carries the context-switching logic, so context adaptation is folded straight into the training objective.

**Adaptive Reasoning Patterns.** Optimising π under this framework lets the model internalise the distribution shift, and robust reasoning patterns emerge that prioritise state-critical tokens.

**Context-Aware Management Strategy.** The model learns to anticipate context-management operations and shifts during RL generation. By keeping task-critical information and pruning noise, performance lifts noticeably when the model runs inside a context-management agent framework.

### 2.3 Black-box Agent RL: Robustness Across Heterogeneous Scaffolds

In real deployments a large share of our user base runs proprietary or complex agent architectures that behave as black boxes. Model performance often varies sharply with the underlying scaffold, because standard training paradigms do not generalise across cognitive architectures. To address that, we validated the framework with a dedicated black-box agent experiment, ensuring consistent optimisation no matter how opaque the agent is.

**Non-Intrusive Integration.** Forge is fully agnostic to the agent's internals. Agents simply route their requests to the RL service Gateway, and the framework handles data collection and training behind the scenes. So during real RL training Forge supports arbitrary context manipulations — memory compression, history rewriting — alongside any complex internal Agent Loop (Deep Think, multi-agent architectures).

**Multi-Scaffold Generalisation.** Decoupling the training loop from the agent's internal state gives MiniMax M2.5 broad compatibility with a wide range of black-box agents. The range covers code-centric agents that lean heavily on Sandbox and MCP environments — including training our OpenCode Agent entirely as a black box — through to agents using aggressive context-reduction strategies such as Truncate BC. Empirically the gains are consistent and stable, even on completely opaque systems.

![Black-box agent training results](https://filecdn.minimax.chat/public/forge-blackbox-1779895280982.png)

Black-box agent training results

## 3. Engineering Optimization

### 3.1 Hybrid Scheduling Strategy: Windowed FIFO

To bridge throughput and distributional consistency, we use **Windowed FIFO** — a sliding constraint on the training scheduler that sits between strict synchronous ordering and greedy asynchronous execution.

The core rule governs how the training scheduler pulls samples from the global generation queue. Even when a large batch of size N is in flight, the scheduler can only see a window of size W (for example W = 0.3N).

**Restricted Visibility.** Let the queue be Q = [T_0, T_1, …, T_{N-1}] with head index i. The scheduler is limited to fetching completed trajectories from the slice [T_i, T_{i+W-1}].

**Local Greedy Disorder (inside the window).** Within [T_i, T_{i+W-1}] the scheduler can grab any completed trajectory immediately. This breaks the head-of-line blocking effect: fast tasks inside the window do not have to wait for the absolute first task to finish.

**Global Strict Blocking (window boundary).** Even if a task at index j > i+W (outside the window) is done — which is common for the easy short tasks in a large generation batch — the scheduler is forbidden from picking it up.

**Sliding Constraint.** The window only slides forward (i → i+1) as the head of the queue is consumed. This forces the scheduler to wait for stragglers — the complex, long-horizon tasks — within the current window, preventing the training distribution from drifting toward the fast and easy samples further down the queue.

![Windowed FIFO scheduler](https://filecdn.minimax.chat/public/forge-windowed-fifo-1779895280983.png)

Windowed FIFO scheduler

### 3.2 Accelerating Agent Trajectory Training with Prefix Tree Merging

Agent training datasets are usually long multi-turn dialogues that overlap heavily.

### Redundancy in the Naive Approach

**Prefix Overlap.** In a straightforward multi-turn dialogue, messages are appended one after another. With a consistent tokenizer, multiple completions that share the same history could in principle be merged.

**Complex Context Management.** Agents often deploy sophisticated context strategies — discarding irrelevant intermediate results, self-summarising — so distinct completions frequently share extensive common prefixes.

**Limitation of the Naive Approach.** Traditional training treats every sample as independent and recomputes those shared prefixes again and again. In long-context training the wasted TFLOPS are enormous and throughput suffers.

![Prefix tree merging illustration](https://filecdn.minimax.chat/public/forge-prefix-tree-1779895280984.png)

Prefix tree merging illustration

### Prefix Tree Merging

To eliminate the redundancy, we move from linear sample processing to a tree-structured approach.

**Prefix Tree Merge.** For the complex context management common in agent scenarios (illustrated by the long common context above), multiple completions can be merged into a single prefix tree at the sample level — even if their later responses diverge slightly or come from different sampling branches — as long as they share an underlying prefix.

Using attention primitives such as Magi Attention we keep logical execution identical to a standard forward pass. After the forward pass, the prefix tree is unrolled from metadata so the loss is computed normally, leaving downstream logic untouched.

By skipping redundant prefix prefilling, the scheme produces a **40x training speedup** and significantly reduces memory pressure, allowing longer sequences or larger batch sizes, while keeping strict mathematical equivalence to standard methods on loss and metrics.

### 3.3 Extreme Inference Acceleration

Three architectural moves on the generation pipeline:

**MTP-based Speculative Decoding.** Instead of a static draft model, we use Multi-Token Prediction heads continuously fine-tuned with Top-K KL loss. That keeps the draft aligned with the evolving RL policy, sustaining high acceptance rates and meaningful speedups under distribution drift.

**Heterogeneous PD Disaggregation.** Prefill and Decode are decoupled to remove PD interference in mixed MoE scheduling and allow independent parallelism strategies per instance, jointly maximising global throughput and tail latency for long-horizon tasks.

**Global L3 KV Cache Pool.** To avoid redundant prefilling across multi-turn agent RL and to push prefix cache hit rates with group-level rollout, we use a DFS-backed Global L3 Cache. A cost-aware scheduler routes requests by weighing queuing delay against cache migration cost, maximising cache locality without overloading individual instances.

## 4. Scalable Agent RL Algorithm

### 4.1 RL Algorithm

We use **CISPO** as the core algorithm, adapted to the characteristics of long-horizon agents.

**Unified Mixed-Domain Training.** Multi-stage RL often produces negative transfer or interference between domains, so we go the other way and mix tasks across Reasoning, General QA, and Agent domains in one training run. That joint setup eliminates the sequential-stage degradation and improves generalisation across diverse tasks.

JCISPO(θ)=E(q,a)∼D,{oi}i=1G∼πθold(⋅∣q)[1∑i=1G∣oi∣∑i=1G∑t=1∣oi∣sg(r^i,t(θ))A^i,tlog⁡πθ(oi,t∣q,oi,<t)]\mathcal{J}_{\text{CISPO}}(\theta) = \mathbb{E}_{(q,a)\sim\mathcal{D}, \{o_i\}_{i=1}^G \sim \pi_{\theta_{\text{old}}}(\cdot|q)} \left[ \frac{1}{\sum_{i=1}^G |o_i|} \sum_{i=1}^G \sum_{t=1}^{|o_i|} \mathbf{sg}(\hat{r}_{i,t}(\theta)) \hat{A}_{i,t} \log \pi_\theta(o_{i,t} \mid q, o_{i,<t}) \right]JCISPO​(θ)=E(q,a)∼D,{oi​}i=1G​∼πθold​​(⋅∣q)​​∑i=1G​∣oi​∣1​i=1∑G​t=1∑∣oi​∣​sg(r^i,t​(θ))A^i,t​logπθ​(oi,t​∣q,oi,<t​)​

where:

r^i,t(θ)=clip(ri,t(θ),0,1+ϵhighIS)A^i,t=∑p=tT(rpspeed+rpperf)−Bi\begin{aligned} \hat{r}_{i,t}(\theta) &= \text{clip}\left( r_{i,t}(\theta), 0, 1 + \epsilon_{high}^{IS} \right) \\ \widehat{A}_{i,t} &= \sum_{p=t}^T (r_p^{\text{speed}} + r_p^{\text{perf}}) - B_i \end{aligned}r^i,t​(θ)Ai,t​​=clip(ri,t​(θ),0,1+ϵhighIS​)=p=t∑T​(rpspeed​+rpperf​)−Bi​​

### 4.2 Dense and Efficiency-Aware Reward

To tackle credit assignment in ultra-long contexts (up to 200k) while keeping training stable, we use a composite reward framework:

**Process Reward.** For dense feedback we target intermediate behaviours — for example penalising language mixing or specific tool-invocation errors — rather than relying only on the final outcome.

**Task Completion Time Reward.** In agentic settings, multiple trajectories can complete the task, and total duration depends not just on token generation but also on tool execution and sub-agent invocation latency. Because completion time is core to user experience, we incorporate relative completion time as a reward signal, which incentivises the agent to use parallelism and accelerate execution.

**Reward-to-go for Variance Reduction.** Sparse rewards drive high gradient variance on long-horizon tasks. We use the Reward-to-go formulation to normalise returns, which lowers gradient variance, sharpens credit assignment, and stabilises optimisation.

## 5. Conclusions

With Forge we resolved the impossible triangle of scaling RL for agents: a breakthrough in RL system throughput together with robust generalisation across arbitrary agent scaffolds. Plugging that flexible architecture into our stable CISPO algorithm enabled the massive-scale training behind MiniMax M2.5. This holistic approach removes previous constraints, delivers efficient real-world agent capabilities, and pushes our mission of *Intelligence with Everyone* further.

Original post: [Forge: Scalable Agent RL Framework and Algorithm on Hugging Face](https://huggingface.co/blog/MiniMax-AI/forge-scalable-agent-rl-framework-and-algorithm)
