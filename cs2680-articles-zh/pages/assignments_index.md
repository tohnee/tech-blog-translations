---
title: "五份作业：使用、构建并优化同一个智能体系统"
title_en: "Use, build, and optimize a single agent system across five assignments"
source: https://cs2680.seas.harvard.edu/assignments/index.html
crawled: 2026-11-16
translated: 2026-11-16
---

# 五份作业：使用、构建并优化同一个智能体系统

> 原文：[Use, build, and optimize a single agent system across five assignments](https://cs2680.seas.harvard.edu/assignments/index.html) · Harvard CS2680

CS2680 现代 AI 系统：智能体与系统优化（CS2680 Modern AI Systems: Agents and System Optimizations）

作业

# 五份作业：使用、构建并优化同一个智能体系统

这五份作业并不是五个互不相关的练习。它们是同一个系统，你逐步将其拆解并接管。你将首先使用一个现有的编程智能体构建一个智能体应用，然后用自己的循环替换智能体运行时，并构建后续作业评分所依据的评估集，接着围绕一个黑盒模型 API 优化所有环节，再将该 API 替换为你自己提供服务的模型，最后优化整个智能体技术栈。

作业 1、2、5 各占 10%，作业 3 和作业 4 各占 20%。五份作业合计占课程成绩的 70%。没有考试。其余的主要构建任务是[期末项目](../project.html)（20%），问题由你自己选择。

作业 1、2、4 包含一份书面报告，与代码一起提交到代码仓库。作业 3 和作业 5 各包含一篇[公开发布的博客文章](https://blog.cs2680.com/publish/)。**五份作业均为个人作业。** 预计工作量：作业 1 为 4–6 小时，作业 2 为 10–12 小时，作业 3 为 10–15 小时，作业 4 为 10–14 小时，作业 5 为 12–18 小时。

五份作业都通过一个**私有 GitHub 仓库**提交代码。只需创建一次，并将每份作业的代码、书面报告文件、基准测试输出和会话归档分别放在 `assignmentN/` 下，其中 `N` 是作业编号（`assignment1/` 到 `assignment5/`）。保持仓库为私有，并将授课教师和四位助教添加为协作者，以便他们访问：[`1a1a11a`](https://github.com/1a1a11a)、[`LauYeeYu`](https://github.com/LauYeeYu)、[`SeverinaZheng`](https://github.com/SeverinaZheng)、[`G6KlayWang`](https://github.com/G6KlayWang) 和 [`AdvaithRavishankar`](https://github.com/AdvaithRavishankar)。

  

[作业 1 · 9 月 2 日（周三）发布 · 9 月 20 日（周日）截止 · 10%

Mads-Lens1：观察智能体工作

从智能体用户做起。用 Claude Code 为 Claude Code 本身构建一个 Web UI：一个驱动真实智能体会话的浏览器前端——提交提示词，实时观看轨迹流（每一次工具调用及其输入和结果），在智能体派生子智能体时看到它分叉成树，看到运行何时失败，继续会话，并查看每次运行的成本。在你自己的机器上提供服务（公开部署到 CloudLab 或 AWS 是可选的），并写下你的收获。这份作业刻意做得很小，也是后续课程中唯一不作为衡量基准的作业。](assignment1.html)
[作业 2 · 9 月 21 日（周一）发布 · 10 月 4 日（周日）截止 · 10%

Mads-Loop：构建智能体循环

基于课程提供的起始代码，围绕一个模型 API 亲手构建智能体循环：带机器可读 schema 的工具调用、上下文管理、重试、终止，以及在输出格式错误和工具损坏时的优雅失败。在课程提供的基准测试上评估，找出智能体能否帮助你自己的任务，并理解智能体的极限在哪里。隐藏测试考察的是运行时，而不是模型。](assignment2.html)
[作业 3 · 10 月 5 日（周一）发布 · 10 月 20 日（周二）截止 · 20%

Mads-Opt：让每一个 token 都物有所值

模型仍是黑盒 API，因此要优化它周围的一切。减少不必要的 token 和调用，在足够好的地方选用更便宜的模型，让工具执行重叠进行，压缩或重构上下文，并重新设计控制流。在保持任务成功率不变的前提下，降低成本和延迟。](assignment3.html)
[作业 4 · 10 月 21 日（周三）发布 · 11 月 10 日（周二）截止 · 20%

Mads-Serve：拥有服务引擎

去掉前沿 API。在一块 RTX PRO 4500（32 GB）上自行提供模型服务，让你的作业 3 智能体针对它运行，并找出是什么限制了这次运行。然后在模型固定的前提下，通过修改服务引擎或智能体来让它更快。排行榜按解决的任务数和端到端时间对提交进行排名。](assignment4.html)
[作业 5 · 11 月 11 日（周三）发布 · 11 月 24 日（周二）截止 · 10%

Mads-Stack：优化完整技术栈

建立在作业 4 之上。让你自己的智能体变强：修复阻碍它的因素，并从其他智能体设计中汲取好的想法。你也可以在一块 RTX PRO 4500（32 GB）上更换模型和服务引擎。排行榜运行 Terminal-Bench 2.0，达到其基线的提交可获得全部排行榜分数。你在作业 4 的 26 个任务上的排名可获得加分。你还需发表一篇博客文章，讲述你从作业 2–5 中学到的东西。](assignment5.html)

1 “Mads”是 Modern Agent Design and Systems（现代智能体设计与系统）的缩写，也代表了本课程的主线，同时向 [MaDSys](https://madsys.seas.harvard.edu/) 致敬——这是哈佛大学测量与系统设计（Measurement and Design of Systems）研究组，本课程由该研究组讲授并提供支持。

---

# 相关内容

* [计算环境配置](../computing/index.html)。Claude Code、模型 API、HPC（GPU 节点）和 AWS。
* [迟交天数](../policy.html#late-days)。本学期共 4 天，可用于所有作业。
* [AI 使用政策](../policy.html#ai-policy)。鼓励使用 AI，但必须披露。
