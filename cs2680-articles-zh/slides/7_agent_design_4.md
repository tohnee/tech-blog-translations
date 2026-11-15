---
title: "第 7 讲：智能体设计 IV——评估"
title_en: "Agent Design IV: Evaluation"
source: https://cs2680.seas.harvard.edu/slides/7_agent_design_4.pdf
pages: 37
crawled: 2026-11-16
translated: 2026-11-16
---

# 第 7 讲：智能体设计 IV——评估

> PDF 讲义文本抽取：[7_agent_design_4.pdf](https://cs2680.seas.harvard.edu/slides/7_agent_design_4.pdf) · Harvard CS2680

## 第 1 页

**现代 AI 系统：智能体与系统优化**

Juncheng Yang

智能体设计 IV：评估

## 第 2 页

**事务**

- 办公时间：本周四 3:30pm，SEC 4.308
- 期末项目海报展示：12 月 7 日 9am–1pm
  - 如果时间不合适，请在本周末前联系我们
- 作业 2 本周日截止（尽早开始！）

## 第 3 页

**事务：Claude Code 会话日志**

- 打包所有相关内容（完整会话日志缺失部分会从作业 2 扣分）
  - `~/.claude/projects/`（macOS 和 Linux）、`C:\Users\<YourUsername>\.claude\projects\`（Windows）
- 可以上传更多
- 不会因为使用 AI 被扣分，但作业的某些部分应该是你自己的工作
  - 17 名学生用 Claude 帮助写报告
  - 6 名用于润色文字 ☺
  - 少数创建要点后让 Claude 写 ☺
  - 7 名写了草稿再编辑（不鼓励），少数从别处粘贴（ChatGPT？）
  - 4 名的输出几乎与 Claude 完全一致，2 名的报告中留下了 Claude Code 的 TODO
- 一份简短报告：对你自己的反思
- 不要操纵会话日志！这将被视为违反学术诚信
  - 三名学生试图删除历史
- AI 生成的文字很容易被检测（即使没有历史）
- 完美隐藏所有历史比你的作业还难。

## 第 4 页

**今日安排**

- 智能体评估
- 成本高效的智能体

## 第 5 页

**你如何评估智能体的能力？**

- 历史与趋势
- 指标
- 有代表性的基准
- 挑战

## 第 6 页

**评估智能体的不同方式**

**组件级评估**

- Planning：任务分解
- Tool use：发现、选择、参数化
- Memory：提取、合并、检索
- Error recovery

**端到端评估**

- Success rate：任务完成了吗？
- Cost：每任务花费
- Latency：完成任务的时间

## 第 7 页

**一段历史**

- **2018 年之前**：语言建模、狭窄任务——Penn Treebank、WikiText、LAMBADA、SQuAD
- **2018–2019**：迁移学习、通用 NLU——GLUE、SuperGLUE、ARC、HellaSwag、WinoGrande
- **2020–2022**：基础模型能力——MMLU、BIG-bench、GSM8K、MATH、HumanEval、TruthfulQA、HELM
- **2023–2024**：智能体与工具使用、上下文、多模态——MT-Bench、Chatbot Arena、AlpacaEval、IFEval、LongBench、MMMU、GPQA、AgentBench、WebArena、GAIA、SWE-bench、OSWorld、τ-bench
- **2024–2025**：难度、鲁棒性、新鲜度——MMLU-Pro、LiveBench、LiveCodeBench、MMMU-Pro、FrontierMath、Humanity's Last Exam
- **2025–2026**：更大范围、更少具体指令、更真实用例、更新问题——GDPval、BrowseComp、Terminal-Bench、ARC-AGI-3……

https://cs2680.com/notes/agent-evaluation

## 第 8 页

**评估目标**

| 评估目标 | 代表性基准 | 成功的含义 |
| --- | --- | --- |
| 预测文本 | PTB、WikiText | 给观察到的文本分配高概率 |
| 产生正确答案 | MMLU、GSM8K、GPQA、HLE | 匹配已知答案 |
| 产生更受偏好的回答 | Arena、AlpacaEval、MT-Bench | 获得有利的人类或模型判断 |
| 产生可运行的代码 | HumanEval、LiveCodeBench、SWE-bench | 通过可执行测试 |
| 完成交互式任务 | WebArena、OSWorld、τ-bench、Terminal-Bench | 达到所需的环境状态 |

## 第 9 页

**评估目标**

| 评估目标 | 代表性基准 | 成功的含义 |
| --- | --- | --- |
| 预测文本 | PTB、WikiText | 给观察到的文本分配高概率 |
| 产生正确答案 | MMLU、GSM8K、GPQA、HLE | 匹配已知答案 |
| 产生更受偏好的回答 | Arena、AlpacaEval、MT-Bench | 获得有利的人类或模型判断 |
| 产生可运行的代码 | HumanEval、LiveCodeBench、SWE-bench | 通过可执行测试 |
| 完成交互式任务 | WebArena、OSWorld、τ-bench、Terminal-Bench | 达到所需的环境状态 |

## 第 10 页

**指标**

- 早期基准
  - Perplexity：留出文本上平均负对数似然的指数（越低越好）
  - Accuracy 或 F1
  - Preference 或胜率
- Capability
  - Pass@k：k 个解中至少一个通过
  - Pass^k：k 个解全部通过（由 τ-bench 提出）
- Cost
  - 主要是 LLM 成本
  - 被忽视：工具调用等（例如 LLM 缓存未命中）
- Latency / duration
  - 不只是 LLM

## 第 11 页

**基准评估循环**

```python
for task in benchmark:
    environment = reset_to_task_initial_state(task)
    while not terminated and within_budget:
        observation = environment.observe()
        action = agent(task_instruction, observation, history, tools)
        environment.execute(action)
    
    score = task_evaluator(
  agent_final_answer,
  final_environment_state,
  trajectory
    )
```

## 第 12 页

**GAIA：通用 AI 助手**

- 466 个人类编写的问题
- 网页浏览、电子表格、PDF、图像、音频、计算
- 短答案：数字、字符串或列表
  - 例如 17.4 或 4,381
- 没有固定工具 API
  - 每个智能体自带搜索、浏览器、Python、shell
- 测试整个智能体系统，而不只是 LLM

难度等级：

- Level 1：≤ 5 步，零或一个工具
- Level 2：5–10 步，多个工具
- Level 3：任意长，许多工具

Source: Mialon et al., GAIA, arXiv 2023

## 第 13 页

**GAIA：助手能否研究并返回正确答案？**

示例任务：一个附件电子表格包含一份电影列表。找出满足两个条件的电影，查其导演，并报告导演的出生地。

智能体做了什么：

搜索 → 打开网页 → 下载 PDF → 提取表格 → 运行 Python → 答案 4,381

（discarded by the evaluator 为未计分；scored 为计分）

评分：只对最终答案评分：

```
score = (1/N) Σi 1[ normalize(ŷ) = normalize(y) ]
```

测量：推理、检索、工具选择与综合，评分干净

不测量：动作——发邮件、订机票、修改数据库、提交表单、更新 issue

## 第 14 页

**BFCL：模型的工具接口可靠吗？**

Prompt

```
User
Book the cheapest flight from 
Boston to Chicago next Monday.
```

可用工具：

```
search_flights(...)
book_flight(flight_id,
  passenger_id)
get_weather(...)
```

➔ 模型会做哪些调用？

- 正确：先 search，选最便宜的，然后 book
  - `search_flights(origin="BOS", destination="CHI", date=...)`
  - `book_flight(flight_id=..., passenger_id=...)`
- 编造 ID
  - 应该向用户询问 `passenger_id`
- 无关调用
  - `get_weather(...)` 订票不需要

评分：AST 或执行检查；多轮检查每轮的状态 + 回复

V4 增加：Web 搜索、记忆；读分类分数，而不是综合分

Source: Patil et al., Berkeley Function Calling Leaderboard, ICML 2025

## 第 15 页

**WebArena：智能体能完成 Web 工作流吗？**

示例任务：在 GitLab 中创建 issue“Update onboarding documentation”，指派给 Alex，并添加 documentation 标签。

智能体做什么（灰色：观察（可访问性树）；青色：动作（点击、输入、停止））：

可访问性树 → 点击 [Projects] → 可访问性树 → 点击 [project] → 输入 issue 标题 → 点击 [Create issue]，停止…

任务如何评分：

重置快照 → 轨迹 τ → 最终状态 sT → 功能检查 → 成功 1/0

- 812 个任务
- 自托管：shopping、admin、Reddit、GitLab、maps、Wikipedia
- 文本观察：可访问性树；按元素 ID 点击或输入
- Issue 任务检查：issue 存在，assignee 和 label 正确
- 其他任务检查：最终 URL、页面内容、后端状态、文本答案
- WebArena-Verified：结构化输出；移除 LLM-as-a-judge，对 HTTP trace 做确定性检查

Source: Zhou et al., WebArena, ICLR 2024; WebArena-Verified, ServiceNow, 2025

## 第 16 页

**OSWorld：智能体能操作真实计算机吗？**

示例任务：添加计算列、排序、另存为 `result.xlsx`

智能体做什么（灰色：观察（像素）；青色：动作（鼠标、键盘））：

截图 → 点击 LibreOffice → 截图 → 点击单元格 → 输入公式 → 保存文件…

任务如何评分：

初始化逻辑 → 轨迹 τ → 最终状态 sT → 评估器 f → 奖励 R

（not scored / inspected）

- 369 个任务：浏览器、办公、文件、系统应用
- 跨应用工作流跨越多个应用
- 像素观察：截图
- 电子表格：单元格、公式、文件位置
- 其他检查：设置、文件、应用配置

OSWorld 2.0（2026）：108 个长工作流（常常 1 小时以上），数百步，约 27 个检查点用于部分得分

Source: Xie et al., OSWorld, NeurIPS 2024; os-world.github.io

## 第 17 页

**SWE-bench：智能体能修复真实仓库 issue 吗？**

智能体做什么：

grep 仓库 → 检查实现 → 检查测试 → 运行测试 → 修改文件 → 运行测试 → 调试 → 生成补丁

补丁如何评分：

智能体补丁 → 应用到仓库 → 运行测试 → 是否解决

变体：

- Verified：人工检查
- Lite：300 任务子集
- Multilingual：9 种语言
- Multimodal：图像 issue
- Pro：更难、多文件

Sources: Jimenez et al., 2024; OpenAI, 2024; Deng et al., 2025; swebench.com

示例任务：用一个空索引调用库函数会错误地抛出异常。让它返回空结果，同时保留现有行为。

## 第 18 页

**τ-bench：智能体能和用户交互、遵守政策并改变后端状态吗？**

两个交互角色，一份政策：

- Simulated user：一个 LLM 扮演客户
- Agent：受航空公司政策约束
- Tools + airline DB：API 调用改变真实状态

Airline policy：

- basic economy 不能修改

示例任务：

“我需要把明天的航班改到晚间航班。”

流程：

询问身份 → 查询预订 → 搜索航班 → 解释票价差额 → 获得确认 → change_booking(…) → 预订已更新

灰色：与用户对话；青色：调用工具

评估最终 DB 状态

Source: Yao et al., τ-bench, arXiv 2024

## 第 19 页

**τ-bench 评估最终状态和一致性**

Scoring：原始奖励为

```
r = raction × routput
```

- raction = 1 仅当最终数据库匹配标注的目标状态。
- routput = 1 仅当面向用户的回复包含必需信息。

只读调用可以变化，但非预期的写入会导致失败。

该基准还引入了 pass^k：

- pass^k：同一场景的 k 次独立运行全部成功的概率
- pass@k：只需要一次成功运行
- 4/4 成功；1 次就够

pass^k 有意比 pass@k 更严格。

Source: Yao et al., τ-bench, arXiv 2024

τ³-bench 实现现在包括修正任务、更多领域、知识检索和语音评估。

## 第 20 页

**Terminal-Bench：智能体能通过 shell 完成真实任务吗？**

任务领域：端到端工作，不只是仓库 bug 修复

编程　系统管理 + 服务器配置　数据处理

模型训练　安全　科学工作流

任务如何打包和评分：

任务指令 → Docker 容器 → 智能体 shell 轨迹 → 最终系统状态 → 测试套件：通过或失败

`instruction.md` / `Dockerfile` / `tests/test.sh`（不计分 / 由测试检查）

- TB 2.0 有 89 个任务 → TB 4.0 有 66 个
- 隐藏的人类解法；v4.0 剪掉饱和任务，8 小时超时

代表性任务：在实时 KV 服务上部署新协议：连接不丢失，延迟保持

## 第 21 页

**Terminal-Bench：介于 SWE-bench 和 OSWorld 之间**

| | SWE-bench | Terminal-Bench | OSWorld |
| --- | --- | --- | --- |
| 智能体如何行动 | 在一个仓库中编辑文件 | 容器中的 shell 命令 | 鼠标点击和按键 |
| 智能体观察什么 | 代码和测试输出 | 终端输出 | 截图 |
| 任务范围 | 修复一个 GitHub issue | 配置、调试、修复、构建 | 操作任意桌面应用 |
| 评分方式 | 仓库的测试 | 最终系统状态上的测试 | 最终状态检查 |

没有 GUI grounding：测试长时程推理和系统交互，而不需要预测鼠标坐标。

Source: Merrill et al., Terminal-Bench 2.0, arXiv 2026

## 第 22 页

**TheAgentCompany：模拟一家公司**

公司环境：

- GitLab：代码
- Plane：工单
- ownCloud：文档
- RocketChat：团队聊天

Coworkers：LLM 模拟

一项工作，端到端：

读工单（Plane）→ 询问同事（RocketChat）→ 检查仓库（GitLab）→ 编写代码（workspace）→ 运行测试（terminal）→ 更新 issue（Plane）→ 报告结果（RocketChat）

- 175 个任务：软件、PM、数据科学、HR、财务
- 部分得分：检查点为工作的每一步打分

```
Spartial = 0.5 · earned/total + 0.5 · Sfull
```

Score by progress：

- 4/8，未完成：0.25
- 7/8，未完成：0.44
- 8/8，完成：1.00

Source: Xu et al., TheAgentCompany, arXiv 2024; the-agent-company.com

## 第 23 页

**智能体基准**

| 基准 | 智能体操作的环境 | 典型动作 | 评分内容 |
| --- | --- | --- | --- |
| GAIA | Web / 文件 / 代码工具 | 搜索、检查文件、计算 | 简短最终答案 |
| WebArena | 自托管网站 | 点击、输入、导航 | 网站或后端状态 |
| OSWorld | 完整桌面 VM | 鼠标、键盘、应用交互 | 文件、应用状态、系统状态 |
| SWE-bench | 软件仓库 | 检查、编辑、运行测试 | 补丁通过测试 |
| BFCL | 函数 / API 接口 | 结构化函数调用 | 调用、参数和结果状态 |
| τ-bench | 客服 API 与对话 | 与用户交谈、调用 API | 数据库状态和回复 |
| Terminal-Bench | 隔离终端容器 | 任意 shell 命令 | 任务特定验证器测试 |
| TheAgentCompany | 模拟软件公司 | 使用 Web 应用、代码、文件，与同事交谈 | 工作流检查点和最终系统状态 |

## 第 24 页

**智能体评估充满挑战且仍在演进**

- 挑战
- 演进

## 第 25 页

**数据泄漏：四个层面，不只是训练**

- **Training leakage**：任务或其人类修复在训练数据中
- **Eval-time leakage**：智能体上网搜索并复制未来的修复
- **Environment leakage**：沙箱暴露未来 commit 或隐藏测试
- **Benchmark overfitting**：prompt 和脚手架在公开测试集上调优

现实工具 ⟺ 更大的泄漏面

而智能体评估所需的现实工具，其基准可能可被搜索到。

## 第 26 页

**泄漏可能发生在整个智能体栈**

现代“智能体”性能大致是如下函数：

P = f(LLM, prompt, scaffold, tools, retriever, memory, environment)

| 组件 | 可能的泄漏 |
| --- | --- |
| Base model | 预训练中的基准样例 |
| Fine-tuning | 基准解法被用作智能体训练轨迹 |
| Prompt | 从测试任务派生的 few-shot 示例 |
| Retrieval | 基准答案被索引进 RAG 语料 |
| Memory | 之前基准尝试被存储 |
| Web search | 已发布的任务解法被检索 |
| Environment | 未来 Git commit / 隐藏工件被暴露 |
| Scaffold | 针对基准手工调优的启发式 |
| Agent development | 研究者反复检查测试失败并调优系统 |

其中任何一项都可能包含基准信息。因此，说“模型没有在测试集上训练”远不足以支撑智能体评估。

## 第 27 页

**智能体评估的挑战：单一用户轮次**

- 大多数基准给智能体一条完全指定的指令
- prompt 输入，最终状态输出——循环中没有用户
- 真实工作是含糊的、会被修订和打断
- 缺少约束、任务中途纠正、目标变化
- 单轮评分奖励自信的猜测
- 问一个澄清问题会消耗步数且不得分

## 第 28 页

**智能体评估的挑战：单一用户轮次**

这就是你在作业 1 中使用 Claude Code 的方式。

（本页为图示）

## 第 29 页

**智能体评估的挑战：单一用户轮次**

（本页为图示）

## 第 30 页

**智能体评估的挑战：单一用户轮次**

- 大多数基准给智能体一条完全指定的指令
- prompt 输入，最终状态输出——循环中没有用户
- 真实工作是含糊的、会被修订和打断
- 缺少约束、任务中途纠正、目标变化
- 单轮评分奖励自信的猜测
- 问一个澄清问题会消耗步数且不得分

- **Clarification**：目标不明确时它会问吗？
- **Recovery**：任务中途纠正后它会重新规划吗？
- **Memory**：它会跨轮次携带约束吗？

## 第 31 页

**智能体评估的挑战：还有更多**

- **Success rate 不够**：一次 200 步、$40 的运行，对比一次 12 步、$0.30 的运行？——成本与延迟
- **非确定性**：同一智能体、同一任务、不同结果：单次运行分数是噪声，不是信号
- **安全与副作用**：在通往通过的过程中，删除文件、发送邮件或花钱不受惩罚
- **指标**：只看结果的评分会放过幸运或不安全的运行；轨迹匹配又会否定合法的运行

参与：MaDSys 组正在构建一个使用真实流量的智能体评估研究平台——如果你有兴趣并且每周能投入 20+ 小时，请联系我。

## 第 32 页

**前沿追赶得有多快**

- **GLUE · 2018**：14 个月达到人类水平（87.1）；91.1
- **MMLU · 2020**：39 个月达到专家水平（89.8）；92.3
- **GPQA Diamond · 2023**：10 个月达到 PhD 专家水平（69.7）；96.0
- **SWE-bench Verified · 2024**：22 个月从 33% → 95%；95.0
- **ARC-AGI-2 · 2025**：11 个月达到普通人平均水平（60）；95.0
- **ARC-AGI-3 · 2026**：6 个月从 0.5% → 62.7%\*；62.7

## 第 33 页

**基准很快饱和**

时间线：2016 → 2017 → 2018 → 2019 → 2020 → 2021 → 2022 → 2023 → 2024 → 2025 → 2026 年 9 月

基准：

SQuAD 1.1、GLUE、SuperGLUE、ARC-AGI-1、MMLU、MATH、HumanEval、Chatbot Arena、MT-Bench、WebArena、SWE-bench → Verified、GPQA Diamond、MMMU、OSWorld、FrontierMath、Humanity's Last Exam、ARC-AGI-2、Terminal-Bench、GDPval、SWE-bench Pro、Remote Labor Index、ARC-AGI-3、OSWorld 2.0

分类：狭窄任务 / NLU 套件 / 知识与推理 / 助手 / 智能体 / 仍未饱和 / 已饱和

Saturated = 前沿达到人类基线，或顶级模型之间不再有区分度。

## 第 34 页

**智能体评估仍在演进**

| 维度 | 早期评估 | 当前前沿 |
| --- | --- | --- |
| 评估目标 | 基础模型 | 模型 + prompt + 工具 + 智能体框架 |
| 交互 | 静态、单轮 | 有状态、长时程 |
| 评分器 | 精确匹配或似然 | 测试、环境状态、人类或 judge 模型 |
| 数据集 | 固定且公开 | 新鲜、隐藏、动态或污染感知 |
| 主要指标 | 平均准确率 | 除任务成功外的系统效率、可靠性、质量、成本和延迟 |
| 主要关注 | 跨样本泛化 | 在现实约束和安全要求下的稳健完成 |

## 第 35 页

**真实世界智能体还要考虑更多维度**

能力　成本　速度　智能体可用性

作业 3：你将按全部三个指标评估

- 能力 Capability（越高越好）
- 成本 Cost（越低越好）

更优：如果 A 在任何指标上都不差，且至少在一个指标上更好，则 A 支配 B。

第 1 名 / 第 2 名 / 第 3 名：第 1 名是 Pareto 前沿；速度未画出。

## 第 36 页

**下一节课**

- 成本高效的智能体
- 案例研究
- 不同类型的智能体
- 智能体框架

## 第 37 页

（空白页）
