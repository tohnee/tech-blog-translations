---
title: "CS329A index"
source: https://cs329a.stanford.edu
crawled: 2026-09-23
---

Stanford CS329A | Self-Improving AI Agents

## Course Overview

**Autumn 2025**

This course covers the latest techniques and applications of AI agents
that can continuously improve themselves through interaction with themselves and the environment.
The course will start with self-improvement techniques for LLMs, such as constitutional AI,
using verifiers, scaling test-time compute, combining search with LLMs, and train time scaling with RL.
We will then discuss the latest research in augmenting LLMs with tool use, code, and memory,
and orchestrating AI capabilities with multimodal interaction.
We will next discuss multi-step reasoning and planning problems for agentic workflows,
and the challenges in building robust evaluation frameworks.

Our goal is that the students learn from the latest research papers,
discuss the suggested readings in each class, work on an original research project in this area,
and learn from invited academic and industry speakers about applications in building coding agents,
research assistants in STEM, and autonomous systems in robotics.

## Course Staff

### Instructors

[![](images/aakanksha.jpeg)

Aakanksha Chowdhery](https://www.achowdhery.com/)

Instructor

[![](images/azalia.jpeg)

Azalia Mirhoseini](http://azaliamirhoseini.com/)

Instructor

### Course Assistants

[![Chelsea Zou](images/chelsea.jpeg)

Chelsea Zou

CA](https://bosonphoton.github.io/)

[![Shree Reddy](images/shree.jpeg)

Shree Reddy

CA](https://www.linkedin.com/in/shree-reddy-7221421b2/)

[![Kaien Yang](images/kaien.jpeg)

Kaien Yang

CA](https://www.linkedin.com/in/kaienyang/)

[![Adrian Gamarra Lafuente](images/adrian.jpeg)

Adrian Gamarra Lafuente

CA](https://www.linkedin.com/in/adrian-gamarra/)

## Logistics

- **Lectures** are held on Monday/Friday 4:30 PM - 5:50 PM PT in Autumn 2025 in Skilling Auditorium. In-person lectures will start with the first
  lecture.

## Schedule

| # | Date | Description | Paper Readings* | Deadlines |
| --- | --- | --- | --- | --- |
| 1 | Mon Sep 22 | Course Overview |  |  |
| 2 | Fri Sep 26 | Test-time Compute Scaling | - [Large Language Monkeys: Scaling Inference Compute with Repeated Sampling (Brown et al. 2024)](https://arxiv.org/abs/2407.21787) - [Archon: An Architecture Search Framework for Inference-Time Techniques (Saad-Falcon et al. 2024)](https://www.arxiv.org/abs/2409.15254) - [Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters (Snell et al. 2024)](https://arxiv.org/abs/2408.03314) - [How Do Large Language Monkeys Get Their Power (Laws)?](https://arxiv.org/abs/2502.17578) |  |
| 3 | Mon Sep 29 | Robust Verification | - [Shrinking the Generation-Verification Gap with Weak Verifiers](https://arxiv.org/abs/2506.18203) - [Training Verifiers to Solve Math Word Problems (Cobbe et al. 2021)](https://arxiv.org/abs/2110.14168) - [Let's Verify step by step (Lightman et al. 2023)](https://arxiv.org/abs/2305.20050) - [Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations (Wang et al. 2023)](https://arxiv.org/abs/2312.08935) |  |
| 4 | Fri Oct 3 | Learning from feedback with tools/code | - [ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al. 2022)](https://arxiv.org/abs/2210.03629) - [RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning](https://arxiv.org/abs/2410.02089) - [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) | Homework 1 out (due Oct 13) |
| 5 | Mon Oct 6 | Multi-step Reasoning/Planning | - [SWiRL: Synthetic Data Generation & Multi-Step RL for Reasoning & Tool Use](https://arxiv.org/abs/2504.04736) - [Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models (Zhou et al. 2023)](https://arxiv.org/abs/2310.04406) - [SPRINT: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models](https://arxiv.org/abs/2506.05745) - [ADaPT: As-Needed Decomposition and Planning with Language Models (Prasad et al. 2024)](https://arxiv.org/abs/2311.05772) - [Wider or Deeper? Scaling LLM Inference-Time Compute with Adaptive Branching Tree Search](https://arxiv.org/abs/2503.04412) |  |
| 6 | Fri Oct 10 | Train Time Scaling/Scaling RL | - [STaR: Bootstrapping Reasoning With Reasoning (Zelikman et al. 2022)](https://arxiv.org/pdf/2203.14465) - [DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models](https://arxiv.org/abs/2402.03300) - [DAPO: An Open-Source LLM Reinforcement Learning System at Scale](https://arxiv.org/abs/2503.14476) | Project Proposal due |
| 7 | Mon Oct 13 | Open-Ended Evolution of Self-Improving Agents | - [Automated design of agentic systems](https://arxiv.org/pdf/2505.22954) - [The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery (Lu et al. 2024)](https://arxiv.org/abs/2408.06292) - [AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/AlphaEvolve.pdf) | Homework 2 out on Oct 14 (due Oct 22) |
| 8 | Fri Oct 17 | Self improvement with Search & Deep Research Agents | - [Competition-Level Code Generation with AlphaCode](https://arxiv.org/pdf/2203.07814) - [AlphaCode 2 Technical Report](https://storage.googleapis.com/deepmind-media/AlphaCode2/AlphaCode2_Tech_Report.pdf) - [Search-o1: Agentic Search-Enhanced Large Reasoning Models](https://arxiv.org/pdf/2501.05366) |  |
| 9 | Mon Oct 20 | Guest Lecture Melvin Johnson (Google DeepMind) | Evolution of Post-training from Chatbots to Agents |  |
| 10 | Fri Oct 24 | Mid term presentations |  | Homework 3 out (due Nov 7) |
| 11 | Mon Oct 27 | Mid term presentations |  |  |
| 12 | Fri Oct 31 | Mid term presentations |  |  |
| 13 | Mon Nov 3 | Agentic Frameworks for Software Engineering | - [CodeMonkeys: Scaling Test-Time Compute for Software Engineering](https://arxiv.org/abs/2501.14723) - [KernelBench: Can LLMs Write Efficient GPU Kernels?](https://arxiv.org/pdf/2502.10517) - [Improving Parallel Program Performance with LLM Optimizers via Agent-System Interfaces](https://arxiv.org/abs/2410.15625) |  |
| 14 | Fri Nov 7 | Augmenting Agents with Memory  Guest Lecturer: Junchen Jiang (LMCache, UChicago) | - [Cartridges: Lightweight and general-purpose long context representations via self-study](https://arxiv.org/abs/2506.06266) - [MemGPT: Towards LLMs as Operating Systems (Packer et al, 2023)](https://arxiv.org/abs/2310.08560) - [CacheBlend: Fast Large Language Model Serving for RAG with Cached Knowledge Fusion](http://arxiv.org/abs/2405.16444) |  |
| 15 | Mon Nov 10 | Guest Lecture Denny Zhou, Google DeepMind | LLM Reasoning |  |
| 16 | Fri Nov 14 | Guest Lecture Thang Luong, Google DeepMind | Towards AI Superhuman Reasoning: AlphaProof, AlphaGeometry & Gemini IMO Gold Medal |  |
| 17 | Mon Nov 17 | Agentic Evaluations & Long-Horizon Tasks | - [Measuring AI Ability to Complete Long Tasks](https://arxiv.org/abs/2503.14499) - [GDPVal: Evaluating AI Model Performance on Real-World Economically Valuable Tasks](https://arxiv.org/abs/2510.04374) - [DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis](https://arxiv.org/abs/2508.20033) |  |
| 18 | Fri Nov 21 | Guest Lecture Misha Laskin (Reflection AI) | Building Agentic Systems for Autonomy: Lessons & Open questions |  |
|  | Mon Nov 24 | Holiday |  |  |
|  | Fri Nov 28 | Holiday |  |  |
| 19 | Mon Dec 1 | Guest Lecture Danny Driess (Physical Intelligence) | Multimodal AI Agents in Robotics |  |
| 20 | Fri Dec 5 | Future Research Areas |  |  |
|  | Wed Dec 10 | Final Project Due |  | Final project due (EoD) |
|  | Fri Dec 12 | Final Project Poster Presentation |  |  |

*Paper readings may be updated closer to the class date.

## Grading

- **Homework 1 (15%)**
  - Due Oct 13
- **Homework 2 (15%)**
  - Due Oct 23
- **Homework 3 (20%)**
  - Due Nov 7
- **Project Proposal (2.5%)**
  - Due Oct 10
- **Midterm presentation + Report (10%)**
  - 5-10 minute presentation on Oct 24, Oct 27, and Oct 31
- **Final project (35%)**
  - Due Dec 10
- **Poster (2.5%)**
  - Dec 12

## Homework Assignments

There will be three homework assignments. Homework 1 will be released on Oct 3. Homework 2 will be released on Oct 13. Homework 3 will be released on Oct 23. The homeworks will help develop intuition for the basics of self-improvement, multi-step reasoning, and tool use techniques.

## Research Projects

As a graduate seminar, research is a big part of the class. Students will work in teams of 2 to 4 to complete original
research. These projects should be broadly around research areas discussed in class and benchmarks related to agent workflows. Students will receive API credits to support their
development work.

## Course Policies

### Late Policy

- All students have 4 free late days for the quarter.
- You may use up to 2 late days per assignment with no penalty.
- Late days can be used for assignments, project proposal, and project milestone.
- Late days cannot be used for the final project report.
- There will be a 25% penalty for each additional late day.
- No exceptions to this policy.

### Audit Policy

Audits are not allowed for this course.

### Communication with Course Staff

- Please read the course documentation carefully before asking general questions.
- Questions should be asked during office hours or on EdStem.
