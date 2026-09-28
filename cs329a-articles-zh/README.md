# Stanford CS329A《Self-Improving AI Agents》课程材料中文索引

> 课程站：[cs329a.stanford.edu](https://cs329a.stanford.edu)（讲师 Aakanksha Chowdhery，2025 秋季）。
> 归档 `cs329a-articles/`：课程页面 2（`pages/`）+ 指定阅读 34 篇（`papers/`，其中 AlphaCode 2 / AlphaEvolve 为 DeepMind PDF 报告，另有 2 份原始 PDF 一并归档）。
> 译文 `cs329a-articles-zh/`：文件名与英文一一对应；翻译规范 `TRANSLATION_GUIDE_CS329A.md`。

## 课程日程（24 节，2025-09-22 至 12-12）与指定阅读

**第 1 讲 · Mon Sep 22 · Course Overview**

**第 2 讲 · Fri Sep 26 · Test-time Compute Scaling**
- [Large Language Monkeys: Scaling Inference Compute with Repeated Sampling (Brown et al. 2024)](https://arxiv.org/abs/2407.21787)
- [Archon: An Architecture Search Framework for Inference-Time Techniques (Saad-Falcon et al. 2024)](https://www.arxiv.org/abs/2409.15254)
- [Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters (Snell et al. 2024)](https://arxiv.org/abs/2408.03314)
- [How Do Large Language Monkeys Get Their Power (Laws)?](https://arxiv.org/abs/2502.17578)

**第 3 讲 · Mon Sep 29 · Robust Verification**
- [Shrinking the Generation-Verification Gap with Weak Verifiers](https://arxiv.org/abs/2506.18203)
- [Training Verifiers to Solve Math Word Problems (Cobbe et al. 2021)](https://arxiv.org/abs/2110.14168)
- [Let's Verify step by step (Lightman et al. 2023)](https://arxiv.org/abs/2305.20050)
- [Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations (Wang et al. 2023)](https://arxiv.org/abs/2312.08935)

**第 4 讲 · Fri Oct 3 · Learning from feedback with tools/code**  
*截止：Homework 1 out (due Oct 13)*
- [ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al. 2022)](https://arxiv.org/abs/2210.03629)
- [RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning](https://arxiv.org/abs/2410.02089)
- [Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073)

**第 5 讲 · Mon Oct 6 · Multi-step Reasoning/Planning**
- [SWiRL: Synthetic Data Generation & Multi-Step RL for Reasoning & Tool Use](https://arxiv.org/abs/2504.04736)
- [Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models (Zhou et al. 2023)](https://arxiv.org/abs/2310.04406)
- [SPRINT: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models](https://arxiv.org/abs/2506.05745)
- [ADaPT: As-Needed Decomposition and Planning with Language Models (Prasad et al. 2024)](https://arxiv.org/abs/2311.05772)
- [Wider or Deeper? Scaling LLM Inference-Time Compute with Adaptive Branching Tree Search](https://arxiv.org/abs/2503.04412)

**第 6 讲 · Fri Oct 10 · Train Time Scaling/Scaling RL**  
*截止：Project Proposal due*
- [STaR: Bootstrapping Reasoning With Reasoning (Zelikman et al. 2022)](https://arxiv.org/pdf/2203.14465)
- [DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models](https://arxiv.org/abs/2402.03300)
- [DAPO: An Open-Source LLM Reinforcement Learning System at Scale](https://arxiv.org/abs/2503.14476)

**第 7 讲 · Mon Oct 13 · Open-Ended Evolution of Self-Improving Agents**  
*截止：Homework 2 out on Oct 14 (due Oct 22)*
- [Automated design of agentic systems](https://arxiv.org/pdf/2505.22954)
- [The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery (Lu et al. 2024)](https://arxiv.org/abs/2408.06292)
- [AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/AlphaEvolve.pdf) → [译文](papers/alphaevolve.md)

**第 8 讲 · Fri Oct 17 · Self improvement with Search & Deep Research Agents**
- [Competition-Level Code Generation with AlphaCode](https://arxiv.org/pdf/2203.07814)
- [AlphaCode 2 Technical Report](https://storage.googleapis.com/deepmind-media/AlphaCode2/AlphaCode2_Tech_Report.pdf)
- [Search-o1: Agentic Search-Enhanced Large Reasoning Models](https://arxiv.org/pdf/2501.05366)

**第 9 讲 · Mon Oct 20 · Guest Lecture Melvin Johnson (Google DeepMind)**

**第 10 讲 · Fri Oct 24 · Mid term presentations**  
*截止：Homework 3 out (due Nov 7)*

**第 11 讲 · Mon Oct 27 · Mid term presentations**

**第 12 讲 · Fri Oct 31 · Mid term presentations**

**第 13 讲 · Mon Nov 3 · Agentic Frameworks for Software Engineering**
- [CodeMonkeys: Scaling Test-Time Compute for Software Engineering](https://arxiv.org/abs/2501.14723)
- [KernelBench: Can LLMs Write Efficient GPU Kernels?](https://arxiv.org/pdf/2502.10517)
- [Improving Parallel Program Performance with LLM Optimizers via Agent-System Interfaces](https://arxiv.org/abs/2410.15625)

**第 14 讲 · Fri Nov 7 · Augmenting Agents with Memory Guest Lecturer: Junchen Jiang (LMCache, UChicago)**
- [Cartridges: Lightweight and general-purpose long context representations via self-study](https://arxiv.org/abs/2506.06266)
- [MemGPT: Towards LLMs as Operating Systems (Packer et al, 2023)](https://arxiv.org/abs/2310.08560)
- [CacheBlend: Fast Large Language Model Serving for RAG with Cached Knowledge Fusion](http://arxiv.org/abs/2405.16444)

**第 15 讲 · Mon Nov 10 · Guest Lecture Denny Zhou, Google DeepMind**

**第 16 讲 · Fri Nov 14 · Guest Lecture Thang Luong, Google DeepMind**

**第 17 讲 · Mon Nov 17 · Agentic Evaluations & Long-Horizon Tasks**
- [Measuring AI Ability to Complete Long Tasks](https://arxiv.org/abs/2503.14499)
- [GDPVal: Evaluating AI Model Performance on Real-World Economically Valuable Tasks](https://arxiv.org/abs/2510.04374)
- [DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis](https://arxiv.org/abs/2508.20033)

**第 18 讲 · Fri Nov 21 · Guest Lecture Misha Laskin (Reflection AI)**

**第  讲 · Mon Nov 24 · Holiday**

**第  讲 · Fri Nov 28 · Holiday**

**第 19 讲 · Mon Dec 1 · Guest Lecture Danny Driess (Physical Intelligence)**

**第 20 讲 · Fri Dec 5 · Future Research Areas**

**第  讲 · Wed Dec 10 · Final Project Due**  
*截止：Final project due (EoD)*

**第  讲 · Fri Dec 12 · Final Project Poster Presentation**

## 课程页面
- [index](pages/index.md) · [EN](../../cs329a-articles/pages/index.md)
- [pastprojects](pages/pastprojects.md) · [EN](../../cs329a-articles/pages/pastprojects.md)

## 论文全列表（34 篇，按文件名）

- ADaPT: As-Needed Decomposition and Planning with Language Models（arXiv:2311.05772） → [译文](papers/adapt.md) · [EN](../../cs329a-articles/papers/adapt.md)
- The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery（arXiv:2408.06292） → [译文](papers/ai-scientist.md) · [EN](../../cs329a-articles/papers/ai-scientist.md)
- Competition-Level Code Generation with AlphaCode（arXiv:2203.07814） → [译文](papers/alphacode.md) · [EN](../../cs329a-articles/papers/alphacode.md)
- AlphaCode 2 Technical Report → [译文](papers/alphacode-2.md) · [EN](../../cs329a-articles/papers/alphacode-2.md)
- AlphaEvolve: A Gemini-Powered Coding Agent for Designing Advanced Algorithms → [译文](papers/alphaevolve.md) · [EN](../../cs329a-articles/papers/alphaevolve.md)
- Archon: An Architecture Search Framework for Inference-Time Techniques（arXiv:2409.15254） → [译文](papers/archon.md) · [EN](../../cs329a-articles/papers/archon.md)
- CacheBlend: Fast Large Language Model Serving for RAG with Cached Knowledge Fusion（arXiv:2405.16444） → [译文](papers/cacheblend.md) · [EN](../../cs329a-articles/papers/cacheblend.md)
- Cartridges: Lightweight and general-purpose long context representations via self-study（arXiv:2506.06266） → [译文](papers/cartridges.md) · [EN](../../cs329a-articles/papers/cartridges.md)
- CodeMonkeys: Scaling Test-Time Compute for Software Engineering（arXiv:2501.14723） → [译文](papers/codemonkeys.md) · [EN](../../cs329a-articles/papers/codemonkeys.md)
- Constitutional AI: Harmlessness from AI Feedback（arXiv:2212.08073） → [译文](papers/constitutional-ai.md) · [EN](../../cs329a-articles/papers/constitutional-ai.md)
- DAPO: An Open-Source LLM Reinforcement Learning System at Scale（arXiv:2503.14476） → [译文](papers/dapo.md) · [EN](../../cs329a-articles/papers/dapo.md)
- Darwin Godel Machine: Open-Ended Evolution of Self-Improving Agents（arXiv:2505.22954） → [译文](papers/darwin-godel-machine.md) · [EN](../../cs329a-articles/papers/darwin-godel-machine.md)
- DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis（arXiv:2508.20033） → [译文](papers/deepscholar-bench.md) · [EN](../../cs329a-articles/papers/deepscholar-bench.md)
- DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models（arXiv:2402.03300） → [译文](papers/deepseekmath.md) · [EN](../../cs329a-articles/papers/deepseekmath.md)
- GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks（arXiv:2510.04374） → [译文](papers/gdpval.md) · [EN](../../cs329a-articles/papers/gdpval.md)
- KernelBench: Can LLMs Write Efficient GPU Kernels?（arXiv:2502.10517） → [译文](papers/kernelbench.md) · [EN](../../cs329a-articles/papers/kernelbench.md)
- Large Language Monkeys: Scaling Inference Compute with Repeated Sampling（arXiv:2407.21787） → [译文](papers/large-language-monkeys.md) · [EN](../../cs329a-articles/papers/large-language-monkeys.md)
- Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models（arXiv:2310.04406） → [译文](papers/lats.md) · [EN](../../cs329a-articles/papers/lats.md)
- Let's Verify Step by Step（arXiv:2305.20050） → [译文](papers/lets-verify-step-by-step.md) · [EN](../../cs329a-articles/papers/lets-verify-step-by-step.md)
- How Do Large Language Monkeys Get Their Power (Laws)?（arXiv:2502.17578） → [译文](papers/llm-monkeys-power-laws.md) · [EN](../../cs329a-articles/papers/llm-monkeys-power-laws.md)
- Improving Parallel Program Performance with LLM Optimizers via Agent-System Interfaces（arXiv:2410.15625） → [译文](papers/llm-optimizers-agent-system-interfaces.md) · [EN](../../cs329a-articles/papers/llm-optimizers-agent-system-interfaces.md)
- Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations（arXiv:2312.08935） → [译文](papers/math-shepherd.md) · [EN](../../cs329a-articles/papers/math-shepherd.md)
- Measuring AI Ability to Complete Long Software Tasks（arXiv:2503.14499） → [译文](papers/measuring-long-tasks.md) · [EN](../../cs329a-articles/papers/measuring-long-tasks.md)
- MemGPT: Towards LLMs as Operating Systems（arXiv:2310.08560） → [译文](papers/memgpt.md) · [EN](../../cs329a-articles/papers/memgpt.md)
- ReAct: Synergizing Reasoning and Acting in Language Models（arXiv:2210.03629） → [译文](papers/react.md) · [EN](../../cs329a-articles/papers/react.md)
- RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning（arXiv:2410.02089） → [译文](papers/rlef.md) · [EN](../../cs329a-articles/papers/rlef.md)
- Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters（arXiv:2408.03314） → [译文](papers/scaling-test-time-compute-optimally.md) · [EN](../../cs329a-articles/papers/scaling-test-time-compute-optimally.md)
- Search-o1: Agentic Search-Enhanced Large Reasoning Models（arXiv:2501.05366） → [译文](papers/search-o1.md) · [EN](../../cs329a-articles/papers/search-o1.md)
- SPRINT: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models（arXiv:2506.05745） → [译文](papers/sprint.md) · [EN](../../cs329a-articles/papers/sprint.md)
- STaR: Bootstrapping Reasoning With Reasoning（arXiv:2203.14465） → [译文](papers/star.md) · [EN](../../cs329a-articles/papers/star.md)
- Synthetic Data Generation & Multi-Step RL for Reasoning & Tool Use（arXiv:2504.04736） → [译文](papers/swirl.md) · [EN](../../cs329a-articles/papers/swirl.md)
- Training Verifiers to Solve Math Word Problems（arXiv:2110.14168） → [译文](papers/training-verifiers-gsm8k.md) · [EN](../../cs329a-articles/papers/training-verifiers-gsm8k.md)
- Shrinking the Generation-Verification Gap with Weak Verifiers（arXiv:2506.18203） → [译文](papers/weak-verifiers-gen-verification-gap.md) · [EN](../../cs329a-articles/papers/weak-verifiers-gen-verification-gap.md)
- Wider or Deeper? Scaling LLM Inference-Time Compute with Adaptive Branching Tree Search（arXiv:2503.04412） → [译文](papers/wider-or-deeper.md) · [EN](../../cs329a-articles/papers/wider-or-deeper.md)
