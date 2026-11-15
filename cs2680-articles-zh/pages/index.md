---
title: "课程公告"
title_en: "Announcement"
source: https://cs2680.seas.harvard.edu/
crawled: 2026-11-16
translated: 2026-11-16
---

# 课程公告

> 原文：[Announcement](https://cs2680.seas.harvard.edu/) · Harvard CS2680

CS2680 现代 AI 系统：智能体与系统优化（CS2680 Modern AI Systems: Agents and System Optimizations）

2026 年秋季

# 课程公告

* 2026 年 10 月 28 日：[Claude Code 使用反馈](http://how-i-used-claude.cs2680.com/)网站上线。
* 2026 年 10 月 8 日：[作业排行榜](https://leaderboard.cs2680.com)上线。
* 2026 年 9 月 4 日：我们已将课程容量扩大到 80 名学生。
* 2026 年 8 月 28 日：旁听政策：只要学校政策允许且教室尚有余位，任何人都可以自由旁听。但我们没有为旁听学生准备计算资源。
* 2026 年 8 月 17 日：欢迎选修 CS2680 现代 AI 系统：智能体与系统优化！课程于每周一和周三在 SEC LL2.229 上课。

---

# 课程概览

本课程沿着一个智能体系统（agentic system）自上而下走一遍：从智能体循环（agent loop）一直到其下的服务栈。你首先使用一个现代编程智能体（Claude Code），随后利用课程提供的 API 访问权限设计自己的智能体，对它进行测量并加以优化。接下来，你亲自部署一个开放权重模型，并对模型之下的各层负责：批处理与调度、KV 缓存与前缀复用、路由、量化以及投机解码。

上课时间与地点

**周一和周三**
上午 11:15 – 下午 12:30
SEC LL2.229

先修要求

**CS61**，以及至少一门研究生层次的计算机系统课程。
假定你熟悉 Python 和 PyTorch。参见[我们假定的背景](policy.html#background)。

考核方式

五份[作业](assignments/index.html)和一个[期末项目](project.html)。
全学期课堂参与。
没有考试。

**课程形式。** 本课程分为两部分。

* **第一部分 — LLM 与智能体导论。** 你将学习如何使用编程智能体（Claude Code），以及如何设计智能体。你还会探索各种智能体架构、用例与优化方法。
* **第二部分 — 面向 LLM 与智能体的系统。** 我们将讨论 LLM 服务（批处理、调度、路由、缓存、量化与投机解码）以及智能体系统。

五份作业沿着这一技术栈分五步向下推进。第一步，Mads-Lens[1](#mads-name-footnote) 让你观察智能体如何工作（作业 1）。第二步，你在 Mads-Loop 中亲手构建这个循环（作业 2）。第三步，你在 Mads-Opt 中让每一个 token 都物有所值（作业 3）。第四步，你在 Mads-Serve 中拥有自己的服务引擎，并在课程提供的 GPU 上运行模型（作业 4）。第五步，你在 Mads-Stack 中优化整个技术栈（作业 5）。

1 “Mads”是 Modern Agent Design and Systems（现代智能体设计与系统）的缩写，也代表了本课程的主线，同时向 [MaDSys](https://madsys.seas.harvard.edu/) 致敬——这是哈佛大学测量与系统设计（Measurement and Design of Systems）研究组，本课程由该研究组讲授并提供支持。

**本课程的预期。** 本课程不会教给你完成作业所需的全部知识。它侧重的是学习方法，并为你指明值得探索的方向。请预期在课后投入大量时间自学与实验。如果你想拿到 A，就要按这个标准来规划。

**评分。**

* 作业 1 Mads-Lens：观察智能体工作 10%
* 作业 2 Mads-Loop：构建智能体循环 10%
* 作业 3 Mads-Opt：让每一个 token 都物有所值 20%
* 作业 4 Mads-Serve：拥有服务引擎 20%
* 作业 5 Mads-Stack：优化完整技术栈 10%
* [期末项目](project.html) 20%
* 课堂参与 10%
* 加分：可选展示每次最高 4%；课程反馈最高 6%；当前 AI 无法解决的问题每个 2%；作业 5 排名最高 5%；合计最高 10%

细节见[政策页面](policy.html)。

**课程网站。** <https://cs2680.com>

---

# 课程团队

![Juncheng Yang](staff/juncheng-yang.jpg)

[Juncheng Yang](https://juncheng.seas.harvard.edu)

授课教师

![Yiyu Liu](staff/yiyu-liu.jpg)

[Yiyu Liu](https://lau.yeeyu.org/)

助教（TF）

![Advaith Ravishankar](staff/AdvaithRavishankar.jpg)

Advaith Ravishankar

助教（TF）

![Charles Wang](staff/charles.jpg)

Charles Wang

助教（TF）

![Yunjia Zheng](staff/yunjia-zheng.jpg)

[Yunjia Zheng](https://scholar.google.com/citations?user=6o4Er-UAAAAJ)

助教（TF）

**联系方式：** [cs2680-staff@g.harvard.edu](mailto:cs2680-staff@g.harvard.edu) 所有与课程相关的问题请使用该邮箱。我们只回复哈佛学生的邮件。由于收到的邮件数量很大，我们不回复外部咨询。

**答疑时间：**

* 授课教师：仅限预约
* 助教：参见 Ed + 预约

---

# 课程安排

*暂定，可能调整。*

讲者为**学生**的行由学生主导：要么是论文讨论（见[论文讨论页面](discussion.html)），要么是作业分享会。论文展示为可选，每次最多可获得 4 个加分百分点。

| 周 | 日期 | 讲者 | 主题 | 阅读材料 | 备注 |
| --- | --- | --- | --- | --- | --- |
| **第一部分 — LLM 与智能体导论** | | | | | |
| 1 | 2026-09-02 | Juncheng Yang | 课程概览与课程安排 [[幻灯片]](slides/1_intro.pdf) |  | **[作业 1](assignments/assignment1.html) 发布**（Mads-Lens：观察智能体工作）；注册 AWS |
| 2 | 2026-09-07 | *停课 — 劳动节* | | | |
| 2 | 2026-09-09 | Juncheng Yang | 智能体使用 I：Claude Code 如何工作 [[幻灯片]](slides/2_agent_use_1.pdf) | [How I use LLMs](https://www.youtube.com/watch?v=EWvNQjAaOHw)；[Best practices for Claude Code](https://code.claude.com/docs/en/best-practices)；[Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/)；[更多阅读 →](readings/sep-09.html) |  |
| 3 | 2026-09-14 | Juncheng Yang | 智能体使用 II：借助多智能体成为 100 倍工程师 [[幻灯片]](slides/3_agent_use_2.pdf) | [Claude Code agent teams](https://code.claude.com/docs/en/agent-teams)；[Software is changing (again)](https://www.youtube.com/watch?v=LCEmiRjPEtQ)；[Research acceleration: The view inside OpenAI](https://openai.com/index/research-acceleration-view-inside-openai/)；[更多阅读 →](readings/sep-14.html) |  |
| 3 | 2026-09-16 | Juncheng Yang | 智能体设计 I：上下文管理与工具设计 [[幻灯片]](slides/4_agent_design_1.pdf) | [ReAct](https://arxiv.org/abs/2210.03629)；[A practical guide to building agents](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents)；[LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent)；[更多阅读 →](readings/sep-16.html) | **[作业 1](assignments/assignment1.html) 截止**：9 月 20 日（周日）晚 11:59 |
| 4 | 2026-09-21 | 学生 | 学生分享 I：从作业 1 中学到的 |  | **[作业 2](assignments/index.html#assignment-2) 发布**（Mads-Loop：构建智能体循环） |
| 4 | 2026-09-23 | Juncheng Yang | 智能体设计 II：多智能体架构、协调与通信 [[幻灯片]](slides/5_agent_design_2.pdf) | [multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)；[scaling agent systems](https://arxiv.org/pdf/2512.08296)；[don’t build multi-agents](https://cognition.com/blog/dont-build-multi-agents)；[更多阅读 →](readings/sep-23.html) |  |
| 5 | 2026-09-28 | Juncheng Yang | 智能体设计 III：智能体记忆与可靠性 [[幻灯片]](slides/6_agent_design_3.pdf) | [where agents fail](https://arxiv.org/abs/2509.25370)；[MemGPT](https://arxiv.org/abs/2310.08560)；[更多阅读 →](readings/sep-28.html) |  |
| 5 | 2026-09-30 | Juncheng Yang | 智能体设计 IV：智能体评估 [[幻灯片]](slides/7_agent_design_4.pdf) | [Agent evaluation and benchmarks](notes/agent-evaluation.html) | **[作业 2](assignments/index.html#assignment-2) 截止**：10 月 4 日（周日）晚 11:59 |
| 6 | 2026-10-05 | Harsh Nilesh Pathak (Snowflake) | 特邀讲座：在企业环境中开发与评估智能体 |  | **[作业 3](assignments/index.html#assignment-3) 发布**（Mads-Opt：让每一个 token 都物有所值） |
| 6 | 2026-10-07 | Juncheng Yang | 高级智能体设计 I：成本与性能 [[幻灯片]](slides/8_agent_design_5.pdf) | [Cost-effective agents](notes/cost-effective-agents.html) | 预提案截止（可选，仅在希望讨论你的想法时提交） |
| 7 | 2026-10-12 | *停课 — 原住民日* | | | |
| 7 | 2026-10-14 | 学生 | 高级智能体设计 II：智能体安全、自进化 harness | [OWASP agentic top 10](https://genai.owasp.org/download/52117/?tmstv=1765059207)；[更多阅读 →](readings/oct-14.html) |  |
| **第二部分 — 面向 LLM 与智能体的系统** | | | | | |
| 8 | 2026-10-19 | Juncheng Yang | 高效 LLM 服务基础 I：LLM 简介 [[幻灯片]](slides/9_llm_serving_basics_1.pdf) | [Transformer](https://arxiv.org/abs/1706.03762)；[Llama 3](https://arxiv.org/abs/2407.21783)；[Mixtral](https://arxiv.org/abs/2401.04088)；[更多阅读 →](readings/oct-19.html) | **[作业 3](assignments/index.html#assignment-3) 截止**：10 月 20 日（周二）晚 11:59 |
| 8 | 2026-10-21 | Juncheng Yang | 高效 LLM 服务基础 II：GPU 简介 [[幻灯片]](slides/10_llm_serving_basics_2a.pdf) | [CUDA programming guide](https://docs.nvidia.com/cuda/cuda-c-programming-guide/)；[更多阅读 →](readings/oct-21.html) | **[作业 4](assignments/index.html#assignment-4) 发布**（Mads-Serve：拥有服务引擎） |
| 9 | 2026-10-26 | 学生 | 学生分享 II：Harness 优化 [[幻灯片]](slides/assignment3_sharing_protected.pdf) |  |  |
| 9 | 2026-10-28 | Yunjia Zheng 和 Juncheng Yang | 作业 3 反馈 [[幻灯片]](slides/assignment3_feedback_protected.pdf) |  | **[项目提案截止](project.html#proposal)** |
| 10 | 2026-11-02 | Juncheng Yang | 作业反馈与智能体陷阱、GPU 编程（续）[[作业](slides/feedback_assignment.pdf)、[GPU](slides/10_llm_serving_basics_2b.pdf)] |  |  |
| 10 | 2026-11-04 | Juncheng Yang | 高效 LLM 服务基础 III：批处理、分页与并行 [[幻灯片]](slides/11_llm_serving_basics_3.pdf) | [Orca](https://www.usenix.org/conference/osdi22/presentation/yu)；[vLLM](https://arxiv.org/abs/2309.06180)；[更多阅读 →](readings/nov-04.html) |  |
| 11 | 2026-11-09 | Xianzheng Dou 和 Haythem Memmi (Meta) | 特邀讲座：为什么基础设施决定 AI 的节奏 |  | **[作业 4](assignments/index.html#assignment-4) 截止**：11 月 10 日（周二）晚 11:59 |
| 11 | 2026-11-11 | Juncheng Yang | 高效 LLM 服务：投机解码 [[幻灯片]](slides/12_llm_serving_spec_decoding.pdf) | [speculative decoding](https://arxiv.org/abs/2211.17192)；[EAGLE](https://arxiv.org/abs/2401.15077)；[Medusa](https://arxiv.org/abs/2401.10774)；[DSpark](https://arxiv.org/abs/2607.05147)；[更多阅读 →](readings/nov-11.html) | **[作业 5](assignments/index.html#assignment-5) 发布**（Mads-Stack：优化完整技术栈） |
| 12 | 2026-11-16 | 学生 | 高效 LLM 服务：KV 缓存优化与模型架构 |  |  |
| 12 | 2026-11-18 | 学生 | 学生分享 III：展示你的服务引擎（作业 4） |  |  |
| 13 | 2026-11-23 | Juncheng Yang | 高效 LLM 服务：剪枝与量化 |  | **[作业 5](assignments/index.html#assignment-5) 截止**：11 月 24 日（周二）晚 11:59 |
| 13 | 2026-11-25 | *停课 — 感恩节假期* | | | |
| 14 | 2026-11-30 | Juncheng Yang | 高效智能体系统：调度与前缀缓存 |  |  |
| 14 | 2026-12-02 | Juncheng Yang | 高效智能体系统：路由与负载均衡 |  |  |
| 14 | 2026-12-07 | 学生 | 期末项目海报与演示 | 以海报和现场演示的形式展示你的期末项目。**地点：SEC 1.402，上午 9:00 至下午 1:00** | **期末项目截止**：12 月 8 日（周二）晚 11:59 |

---

# 参考页面

* [智能体评估与基准测试](notes/agent-evaluation.html)。评估设计、指标、可靠性、成本与基准选择。
* [高性价比智能体](notes/cost-effective-agents.html)。在完整任务中分配模型、推理、上下文、协作与服务资源的技术。

---

# 计算资源

课程使用的每种环境的配置说明都在[计算环境配置](computing/index.html)页面。作业与[期末项目](project.html)所需的计算资源来自：

* [Claude Code](computing/claude-code.html)。作业 1 必需。
* [模型 API 访问](computing/api.html)。作业 2 和作业 3 必需。
* [课程 HPC](computing/cluster.html)。作业 4 和作业 5 必需。
* [AWS](computing/aws.html)。第一周内注册；使用该账号是可选的。

---

**教材。** 无需教材。背景阅读：

* 计算机系统：
  [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/)
* 机器学习系统：
  [Machine Learning Systems](https://mlsysbook.ai)
* 大语言模型：
  [Foundations of Large Language Models](https://arxiv.org/abs/2501.09223)
* 深度学习：
  [The Little Book of Deep Learning](https://fleuret.org/francois/lbdl.html)

# 致谢

我们感谢以下机构的支持。

[![Harvard Faculty of Arts and Sciences](sponsors/harvard-fas.svg)](https://www.fas.harvard.edu/)

[![Harvard John A. Paulson School of Engineering and Applied Sciences](sponsors/harvard-seas.svg)](https://seas.harvard.edu/)

[![Harvard University MaDSys: Measurement and Design of Systems](sponsors/madsys.png)](https://madsys.seas.harvard.edu/)

软件系统、数据与硬件支持。

[![NVIDIA](sponsors/nvidia.svg)](https://www.nvidia.com/)

[![Amazon Web Services](sponsors/aws.png)](https://aws.amazon.com/)

[![CloudLab](sponsors/cloudlab.png)](https://www.cloudlab.us/)

[![Chameleon Cloud](sponsors/chameleon.png)](https://www.chameleoncloud.org/)

---

[![Web Analytics Made Easy - Statcounter](https://c.statcounter.com/13351434/0/7a833262/1/)](https://statcounter.com/ "Web Analytics Made Easy - Statcounter")
