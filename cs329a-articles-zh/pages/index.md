---
title: "Stanford CS329A：自我改进的 AI 智能体（课程主页）"
title_en: "CS329A index"
source: https://cs329a.stanford.edu
crawled: 2026-09-23
translated: 2026-09-23
---

# Stanford CS329A：自我改进的 AI 智能体（Self-Improving AI Agents）

> 原文：[CS329A Course Website](https://cs329a.stanford.edu) · Stanford

## 课程概述

**2025 年秋季学期**

本课程涵盖能够通过与自身及环境交互而持续自我改进的 AI 智能体的最新技术与应用。课程将从 LLM 的自我改进技术入手，例如 Constitutional AI、使用验证器、扩展测试时计算（test-time compute）、将搜索与 LLM 相结合，以及通过强化学习（RL）进行训练时扩展。随后我们将讨论用工具调用、代码与记忆增强 LLM 的最新研究，以及通过多模态交互编排 AI 能力。接着，课程将讨论智能体工作流中的多步推理与规划问题，以及构建稳健的评估框架所面临的挑战。

我们的目标是：让学生研读最新的研究论文，在每堂课上讨论推荐阅读材料，围绕这一方向完成一项原创研究项目，并从受邀的学术界与工业界演讲者那里了解相关应用——包括构建编程智能体（coding agents）、STEM 领域的研究助理，以及机器人领域的自主系统。

## 课程团队

### 主讲教师

[![](images/aakanksha.jpeg)

Aakanksha Chowdhery](https://www.achowdhery.com/)

主讲教师

[![](images/azalia.jpeg)

Azalia Mirhoseini](http://azaliamirhoseini.com/)

主讲教师

### 课程助教

[![Chelsea Zou](images/chelsea.jpeg)

Chelsea Zou

课程助教（CA）](https://bosonphoton.github.io/)

[![Shree Reddy](images/shree.jpeg)

Shree Reddy

课程助教（CA）](https://www.linkedin.com/in/shree-reddy-7221421b2/)

[![Kaien Yang](images/kaien.jpeg)

Kaien Yang

课程助教（CA）](https://www.linkedin.com/in/kaienyang/)

[![Adrian Gamarra Lafuente](images/adrian.jpeg)

Adrian Gamarra Lafuente

课程助教（CA）](https://www.linkedin.com/in/adrian-gamarra/)

## 课程安排

- **授课时间**：2025 年秋季学期，每周一/周五下午 4:30–5:50（太平洋时间），地点为 Skilling Auditorium。课程自第一讲起即为线下授课。

## 日程表

| 课次 | 日期 | 主题 | 论文阅读* | 截止 |
| --- | --- | --- | --- | --- |
| 1 | 9 月 22 日（周一） | 课程概述 |  |  |
| 2 | 9 月 26 日（周五） | 测试时计算扩展 | [Large Language Monkeys: Scaling Inference Compute with Repeated Sampling (Brown et al. 2024)](https://arxiv.org/abs/2407.21787)<br>[Archon: An Architecture Search Framework for Inference-Time Techniques (Saad-Falcon et al. 2024)](https://www.arxiv.org/abs/2409.15254)<br>[Scaling LLM Test-Time Compute Optimally can be More Effective than Scaling Model Parameters (Snell et al. 2024)](https://arxiv.org/abs/2408.03314)<br>[How Do Large Language Monkeys Get Their Power (Laws)?](https://arxiv.org/abs/2502.17578) |  |
| 3 | 9 月 29 日（周一） | 稳健验证 | [Shrinking the Generation-Verification Gap with Weak Verifiers](https://arxiv.org/abs/2506.18203)<br>[Training Verifiers to Solve Math Word Problems (Cobbe et al. 2021)](https://arxiv.org/abs/2110.14168)<br>[Let's Verify step by step (Lightman et al. 2023)](https://arxiv.org/abs/2305.20050)<br>[Math-Shepherd: Verify and Reinforce LLMs Step-by-step without Human Annotations (Wang et al. 2023)](https://arxiv.org/abs/2312.08935) |  |
| 4 | 10 月 3 日（周五） | 通过工具/代码从反馈中学习 | [ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al. 2022)](https://arxiv.org/abs/2210.03629)<br>[RLEF: Grounding Code LLMs in Execution Feedback with Reinforcement Learning](https://arxiv.org/abs/2410.02089)<br>[Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) | 作业 1 发布（10 月 13 日截止） |
| 5 | 10 月 6 日（周一） | 多步推理/规划 | [SWiRL: Synthetic Data Generation & Multi-Step RL for Reasoning & Tool Use](https://arxiv.org/abs/2504.04736)<br>[Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models (Zhou et al. 2023)](https://arxiv.org/abs/2310.04406)<br>[SPRINT: Enabling Interleaved Planning and Parallelized Execution in Reasoning Models](https://arxiv.org/abs/2506.05745)<br>[ADaPT: As-Needed Decomposition and Planning with Language Models (Prasad et al. 2024)](https://arxiv.org/abs/2311.05772)<br>[Wider or Deeper? Scaling LLM Inference-Time Compute with Adaptive Branching Tree Search](https://arxiv.org/abs/2503.04412) |  |
| 6 | 10 月 10 日（周五） | 训练时扩展/扩展强化学习 | [STaR: Bootstrapping Reasoning With Reasoning (Zelikman et al. 2022)](https://arxiv.org/pdf/2203.14465)<br>[DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models](https://arxiv.org/abs/2402.03300)<br>[DAPO: An Open-Source LLM Reinforcement Learning System at Scale](https://arxiv.org/abs/2503.14476) | 项目提案截止 |
| 7 | 10 月 13 日（周一） | 自我改进智能体的开放式进化 | [Automated design of agentic systems](https://arxiv.org/pdf/2505.22954)<br>[The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery (Lu et al. 2024)](https://arxiv.org/abs/2408.06292)<br>[AlphaEvolve: A Gemini-powered coding agent for designing advanced algorithms](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/AlphaEvolve.pdf) | 作业 2 于 10 月 14 日发布（10 月 22 日截止） |
| 8 | 10 月 17 日（周五） | 借助搜索与深度研究智能体的自我改进 | [Competition-Level Code Generation with AlphaCode](https://arxiv.org/pdf/2203.07814)<br>[AlphaCode 2 Technical Report](https://storage.googleapis.com/deepmind-media/AlphaCode2/AlphaCode2_Tech_Report.pdf)<br>[Search-o1: Agentic Search-Enhanced Large Reasoning Models](https://arxiv.org/pdf/2501.05366) |  |
| 9 | 10 月 20 日（周一） | 客座演讲：Melvin Johnson（Google DeepMind） | 后训练的演进：从聊天机器人到智能体 |  |
| 10 | 10 月 24 日（周五） | 期中展示 |  | 作业 3 发布（11 月 7 日截止） |
| 11 | 10 月 27 日（周一） | 期中展示 |  |  |
| 12 | 10 月 31 日（周五） | 期中展示 |  |  |
| 13 | 11 月 3 日（周一） | 面向软件工程的智能体框架 | [CodeMonkeys: Scaling Test-Time Compute for Software Engineering](https://arxiv.org/abs/2501.14723)<br>[KernelBench: Can LLMs Write Efficient GPU Kernels?](https://arxiv.org/pdf/2502.10517)<br>[Improving Parallel Program Performance with LLM Optimizers via Agent-System Interfaces](https://arxiv.org/abs/2410.15625) |  |
| 14 | 11 月 7 日（周五） | 用记忆增强智能体（客座讲师：Junchen Jiang，LMCache，芝加哥大学） | [Cartridges: Lightweight and general-purpose long context representations via self-study](https://arxiv.org/abs/2506.06266)<br>[MemGPT: Towards LLMs as Operating Systems (Packer et al, 2023)](https://arxiv.org/abs/2310.08560)<br>[CacheBlend: Fast Large Language Model Serving for RAG with Cached Knowledge Fusion](http://arxiv.org/abs/2405.16444) |  |
| 15 | 11 月 10 日（周一） | 客座演讲：Denny Zhou（Google DeepMind） | LLM 推理 |  |
| 16 | 11 月 14 日（周五） | 客座演讲：Thang Luong（Google DeepMind） | 迈向 AI 超人类推理：AlphaProof、AlphaGeometry 与 Gemini IMO 金牌 |  |
| 17 | 11 月 17 日（周一） | 智能体评估与长时程任务 | [Measuring AI Ability to Complete Long Tasks](https://arxiv.org/abs/2503.14499)<br>[GDPVal: Evaluating AI Model Performance on Real-World Economically Valuable Tasks](https://arxiv.org/abs/2510.04374)<br>[DeepScholar-Bench: A Live Benchmark and Automated Evaluation for Generative Research Synthesis](https://arxiv.org/abs/2508.20033) |  |
| 18 | 11 月 21 日（周五） | 客座演讲：Misha Laskin（Reflection AI） | 构建面向自主性的智能体系统：经验与开放问题 |  |
|  | 11 月 24 日（周一） | 假期 |  |  |
|  | 11 月 28 日（周五） | 假期 |  |  |
| 19 | 12 月 1 日（周一） | 客座演讲：Danny Driess（Physical Intelligence） | 机器人领域的多模态 AI 智能体 |  |
| 20 | 12 月 5 日（周五） | 未来研究方向 |  |  |
|  | 12 月 10 日（周三） | 期末项目截止 |  | 期末项目截止（当日结束前） |
|  | 12 月 12 日（周五） | 期末项目海报展示 |  |  |

*论文阅读列表可能随临近上课日期而更新。

## 评分

- **作业 1（15%）**
  - 10 月 13 日截止
- **作业 2（15%）**
  - 10 月 23 日截止
- **作业 3（20%）**
  - 11 月 7 日截止
- **项目提案（2.5%）**
  - 10 月 10 日截止
- **期中展示 + 报告（10%）**
  - 在 10 月 24 日、10 月 27 日和 10 月 31 日进行 5–10 分钟的展示
- **期末项目（35%）**
  - 12 月 10 日截止
- **海报（2.5%）**
  - 12 月 12 日

## 作业

本课程共有三次作业。作业 1 将于 10 月 3 日发布，作业 2 将于 10 月 13 日发布，作业 3 将于 10 月 23 日发布。这些作业将帮助你对自我改进、多步推理与工具调用等基础技术建立直觉。

## 研究项目

作为一门研究生研讨课，研究是本课程的重要组成部分。学生将以 2–4 人为一组完成原创研究。这些项目应大致围绕课堂上讨论的研究方向，以及与智能体工作流相关的基准测试展开。学生将获得 API 额度以支持其开发工作。

## 课程政策

### 迟交政策

- 所有学生本学期共有 4 天免费迟交额度（late days）。
- 每次作业最多可使用 2 天迟交额度而不受处罚。
- 迟交额度可用于作业、项目提案和项目里程碑。
- 迟交额度不可用于期末项目报告。
- 超出额度后，每迟交一天将扣减 25%。
- 本政策无任何例外。

### 旁听政策

本课程不允许旁听。

### 与课程团队的沟通

- 在提出一般性问题之前，请先仔细阅读课程文档。
- 问题应在答疑时间（office hours）提出，或发布在 EdStem 上。
