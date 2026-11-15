---
title: "第 6 讲：智能体设计 III——记忆与可靠性"
title_en: "Agent Design III: Memory and Reliability"
source: https://cs2680.seas.harvard.edu/slides/6_agent_design_3.pdf
pages: 31
crawled: 2026-11-16
translated: 2026-11-16
---

# 第 6 讲：智能体设计 III——记忆与可靠性

> PDF 讲义文本抽取：[6_agent_design_3.pdf](https://cs2680.seas.harvard.edu/slides/6_agent_design_3.pdf) · Harvard CS2680

## 第 1 页

**现代 AI 系统：智能体与系统优化**

Juncheng Yang

智能体设计 III：记忆与可靠性

## 第 2 页

**事务**

- 办公时间：本周四 3:30pm，SEC 4.308
- 期末项目海报展示：12 月 7 日 9am–1pm
  - 如果时间不合适，请本周联系我们
- AI 生成的参考资料
  - https://cs2680.com/notes/agent-evaluation
  - 阅读材料中的笔记（列表由我筛选）
  - 由我和助教审阅

## 第 3 页

**今日安排**

- 多智能体设计（接上节课）
- 智能体记忆
- 智能体可靠性

## 第 4 页

（空白页）

## 第 5 页

**智能体记忆**

上下文窗口之外的持久状态。

用户 / 智能体框架 / LLM / 记忆存储 / 上下文窗口

- 上下文窗口：临时工作状态
- 记忆存储：跨交互的持久状态

## 第 6 页

**智能体记忆的设计问题**

- 谁拥有记忆？（owner?）
- 值得保留吗？WRITE OR SKIP（写或跳过）——decision
- 它应该变成什么？ENCODE / ORGANIZE（编码 / 组织）——format
- 这个任务需要它吗？RETRIEVE（检索）——task
- 能得出什么更广泛的教训？REFLECT / GENERALIZE（反思 / 泛化）——lesson
- 它仍然有效吗？KEEP / UPDATE / DELETE（保留 / 更新 / 删除）——status
- 它应该放在哪里？STORE（存储）——backend

## 第 7 页

**决策：什么时候某件事应该成为记忆？**

写下每一次交互会提高召回率，也会提高噪声。

- 显式用户请求
- 确定性规则（启发式）
- 小分类器
- 周期性 LLM 审查

高召回 ← 写入每一次交互；高精确 ← 选择性写入

保留？格式？后端？需要？教训？有效？

## 第 8 页

**如何组织记忆？**

- **原始事件 / 片段**：“我们把服务从 vLLM 迁到了 SGLang。”
  - 高保真；庞大且冗余
- **非结构化摘要**：“使用 SGLang 做模型服务。”
  - 紧凑，但可能丢失上下文
- **结构化状态**：`{"serving_engine":"SGLang"…}`
  - 可查询；schema 有约束
- **知识图谱**：Project → USES → SGLang
  - 关联实体及其随时间的变化

保留？格式？后端？需要？教训？有效？

举手

## 第 9 页

**如何存储记忆？**

- **纯文件**：CLAUDE.md、scratchpad
  - 易于检查、diff 和搜索
- **键值或关系数据库**：Redis、SQLite、Postgres JSONB
  - 精确查找、过滤和事务
- **向量存储**：pgvector、Chroma、Pinecone
  - 精确或近似相似度搜索
- **图数据库**：Neo4j、FalkorDB（Graphiti）
  - 关系查询和多跳遍历

保留？格式？后端？需要？教训？有效？

举手

## 第 10 页

**何时应该使用记忆？**

**自动**

每一轮：search → LLM → add

- + 可预测且简单
- – 增加延迟和无关上下文

**运行时控制**

```python
if memory_needed:
    search()
if memorable:
    add()
```

- + 选择性强且高效
- – 需要规则或分类器

**模型控制**

```python
search_memory()
add_memory()
update_memory()
forget_memory()
```

- + 需求驱动；由 LLM 决定何时调用
- – 可能漏掉有用的读取或写入

许多系统使用混合方法；读和写的策略可能不同。

保留？格式？后端？需要？教训？有效？

## 第 11 页

**如何检索记忆？**

语义相关性只是检索信号之一。

基本流水线：Query → Vector search → Top-k memories → Prompt

- **语义匹配**：含义与查询匹配
- **范围**：同一用户、项目、实体或任务
- **重要性**：遗漏或纳入它的代价
- **有效性**：此时此任务为真
- **来源**：出处、置信度和证据

保留？格式？后端？需要？教训？有效？

## 第 12 页

**如何从观察中泛化？**

被问到 vLLM / SGLang / TRT-LLM / LLM 调度

→ reflection

- 假设：对 LLM 推理系统的频繁兴趣
- 置信度：中

**何时应该合并？**

- 在足够多新证据之后，例如每 N 个事件或上下文填满时
- 当事实冲突或重复时
- 尽可能放在后台任务中

保留？格式？后端？需要？教训？有效？

## 第 13 页

**遗忘是一等记忆操作**

**生命周期控制**

- 标记无效
- 永久删除
- TTL 后过期
- 创建层级并从活跃记忆中驱逐

**为什么遗忘**

- 过时信息
- 不正确或冲突的信息
- 隐私与安全
- 存储和检索成本

保留？格式？后端？需要？教训？有效？

## 第 14 页

**记忆需要有效时间与来源**

- 2026 年 4 月：项目用 vLLM 服务模型（superseded，已被取代）
- 2026 年 6 月：项目用 SGLang 服务模型（current，当前）

有效时间：哪个事实何时适用

来源：事实来自哪里

Episode 28：“我们把服务从 vLLM 迁到了 SGLang。”

Project → SERVES_WITH → SGLang

source: Episode 28

保留？格式？后端？需要？教训？有效？

## 第 15 页

**谁拥有记忆？**

**智能体自有**

智能体框架中的文件：CLAUDE.md、agent scratchpad、任务笔记。

智能体框架 / LLM / 读 / 写 / CLAUDE.md、任务笔记

框架把记忆持久化到磁盘。

**专用记忆系统**

智能体调用的服务：Mem0、Graphiti、supermemory。

智能体框架 / LLM / 搜索 · 更新 / memories / 记忆层（库或服务）

记忆是一个 API，跨智能体和会话共享。

## 第 16 页

**专用记忆系统**

**Mem0**

- 以事实为中心
- 输入：消息，按 user、agent 或 run 划分作用域。
- 检索：带过滤的向量搜索；可选图记忆。
- 例：“Uses SGLang for model serving.”

**Graphiti**

- 时间知识图谱
- 输入：产生实体和时间感知事实的 episode。
- 检索：语义、关键词和图搜索的混合。
- 例：uses → SGLang，有效 Apr 2026 → present

**supermemory**

- Profile、memory、document
- 维护用户 profile 以及记忆和文档
- 输入：与来源和时间关联的对话。
- 检索：profile、记忆和文档搜索

## 第 17 页

**智能体记忆设计清单**

- **Observe**：观察并捕获事件
- **Select**：这值得记住吗？
- **Encode / organize**：什么表示能保留所需含义？
- **Store**：它应该放在哪里？文件、数据库？
- **Retrieve**：什么对当前任务有用？
- **Reflect / consolidate**：这次更新或矛盾于旧记忆吗？
- **Forget**：信息何时过时或无关？

每个阶段都是一个策略决策。

## 第 18 页

**失败模式**

- **Retrieval miss**：相关记忆存在但没被找到。
- **Context pollution**：太多无关记忆进入上下文。
- **Memory hallucination**：把推断存成事实：“在哈佛学习”变成“哈佛访问学生”。
- **Staleness**：旧事实覆盖新信息。
- **Isolation failure**：记忆跨越用户边界。
- **Overgeneralization**：一个事件变成持久偏好。
- **Persistent prompt injection**：不受信任的内容之后作为指令返回。
- **Unbounded growth**：大小随生命周期增长，检索成本和质量下降。

举手

## 第 19 页

**如何评估智能体记忆**

- **Writes and update**：精确率、召回率、过时记忆率
- **Retrieval**：精确率、召回率
- **System**：延迟、token 开销、存储增长
- **Governance**：删除合规性和作用域隔离

## 第 20 页

**智能体记忆评估**

- **LoCoMo**：1,540 个问题；10 段长对话
- **LongMemEval**：500 个问题；5 种记忆能力
- **BEAM**：2,000 个问题；最高 10M tokens

记忆组件评估

LoCoMo (ACL 2024) · LongMemEval (ICLR 2025) · BEAM (ICLR 2026) · LoCoMo-Refined

主要测试智能体能否对用户—助手历史进行召回和推理。覆盖召回、时间推理、更新、偏好和拒答。

## 第 21 页

**智能体记忆栈**

**独立记忆层**

- 智能体运行时：Claude Code、Letta、Codex
- Memory management：Mem0、Letta 内置、自定义
- 存储：vector、SQL、graph、object store

**记忆位于框架内部**

- 智能体运行时：Claude Code、Letta、Codex
- 运行时内的记忆管理
- Storage：markdown files

## 第 22 页

**为什么智能体可靠性是个问题？**

错误会累积。

50 步的运行中，只有 1/13 能无错误完成。

- 一次运行只有在每一步都成功时才成功
- 错误传播使真实运行比这更糟

无错误运行的概率（每步 95% 成功）：

| 轨迹步数 | 1 | 5 | 10 | 20 | 50 |
| --- | --- | --- | --- | --- | --- |
| 无错误概率 | 95% | 77% | 60% | 36% | 8% |

假设每一步独立以 0.95 的概率成功。

## 第 23 页

**智能体可靠性**

智能体失败有哪些不同方式？

## 第 24 页

**故障起源于哪里？**

- **User / task spec**：目标是否无歧义？——specification failure
- **Agent harness**：上下文、循环、调度？——harness failure
- **LLM**：推理与规划？——model failure
- **Tool layer**：shell、浏览器、API？——tool failure
- **Environment**：repo、OS、web、服务？——environment failure

## 第 25 页

**任务规范**

| 失败 | 规范说的是 | 智能体做了 | 修复 |
| --- | --- | --- | --- |
| 目标含糊 | “Fix the login bug” | 修错了三个中的一个 | 指明文件、症状和复现步骤 |
| 代理目标 | “Make the tests pass” | 删除了失败的测试 | 禁止修改测试；审查 diff |
| 未说明的约束 | “Speed up search” | 破坏了公共 API | 说明哪些内容不能改变 |
| 没有完成定义 | “Clean up the parser” | 永远停不下来重构 | 给出退出测试和停止规则 |
| 目标冲突 | “Minimal diff, every edge case” | 悄悄丢掉了边界情况 | 显式排序目标 |

## 第 26 页

**智能体框架**

| 失败 | 框架做了什么 | 影响 | 修复 |
| --- | --- | --- | --- |
| 上下文截断错误 | 裁掉了最旧的轮次 | 忘记了“保留 API”规则 | 把关键规则固定在窗口之外 |
| 记忆错误 | 把过时笔记当作事实召回 | 编辑了一个已经移动的文件 | 给记忆标日期；使用前复查 |
| 状态损坏错误 | 保留了半应用的编辑 | 后续步骤建立在损坏文件上 | 检查点；回滚失败步骤 |
| 控制循环错误 | 没有设置步数或成本预算 | 200 步，没有进展 | 限制步数、成本和时间 |
| 阻塞式扇出 | 等待每个子智能体 | 一个慢子智能体拖住整个运行 | 设置超时；使用部分结果 |

## 第 27 页

**模型**

| 失败 | 模型推理 | 智能体做了 |
| --- | --- | --- |
| 幻觉 | “requests.fetch() exists” | 调用了不存在的函数 |
| 违反指令 | “Speed matters more than the API” | 改变了被告知要保留的签名 |
| 错误推理 | “A timeout means the network is down” | 给死锁加了重试 |
| 推理—行动不一致 | “I'll only touch parser.py” | 重写了另外三个文件 |
| 未验证的成功 | “Tests probably pass now” | 宣布完成，什么也没运行 |
| 长时程退化 | “The config still needs fixing” | 撤销了自己第 12 步的修复 |

**修复**

- 对照真实文档检查调用
- 复述约束；检查 diff
- 修复前先检验假设
- 把每个动作与计划比较
- 要求测试输出作为证据
- 重读状态；拆成短任务

## 第 28 页

**工具**

| 失败 | 工具返回 | 智能体做了 |
| --- | --- | --- |
| 截断输出 | 日志的前 100 行 | 漏掉了第 4,000 行的错误 |
| 静默失败 | 退出码 0，空结果 | 假设没有匹配 |
| 含糊 schema | 没有时区的日期 | 任务时间排错了 8 小时 |
| 不稳定调用 | 第一次尝试超时 | 宣布服务宕机 |
| 误导性错误 | 因拼写错误报“Permission denied” | 用 sudo 重试 |

**修复**

- 先返回错误；允许分页
- 把“空”与“失败”分开
- 使用类型化、显式的 schema
- 判断前先退避重试
- 返回精确、可行动的 error

## 第 29 页

**环境**

| 失败 | 环境情况 | 智能体做了 |
| --- | --- | --- |
| 状态过时 | 昨天的缓存构建 | 在旧代码上通过了测试 |
| 版本不匹配 | Python 3.8，而非 3.12 | 交付了会崩溃的代码 |
| 随机失败 | 任务成功依赖环境 | 因闰年失败 |
| 网页布局变化 | 重新设计的 checkout 页面 | 点错了按钮 |
| 速率限制 | 50 次调用后 HTTP 429 | 迁移中途停止 |

**修复**

- 从全新缓存干净构建
- 在 lockfile 中固定版本
- 重跑失败；隔离 flaky
- 行动前重读页面
- 限流并检查点长任务

## 第 30 页

**为失败而设计**

- **Task specification**：把“完成”写成测试
  - 验收测试前置
  - 列出不能改变的内容
- **Agent harness**：给每次运行设界
  - 步数、成本和时间上限
  - 检查点与回滚
- **Model**：要求证据
  - 每个主张都要证明
  - 验证
  - 使用更强的模型
- **Tool**：大声失败
  - 类型化 schema
  - 错误与空结果区分
- **Environment**：固定并隔离
  - 全新、固定版本的沙箱
  - 判断前重试 flaky

我们仍未理解规模化下的智能体，也几乎没有正式的最佳实践。

## 第 31 页

**下一节课**

- 智能体评估
- 成本高效的智能体
- 案例研究
