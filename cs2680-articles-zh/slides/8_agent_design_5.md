---
title: "第 8 讲：智能体设计 V——成本高效的智能体"
title_en: "Agent Design V: Cost-effective Agents"
source: https://cs2680.seas.harvard.edu/slides/8_agent_design_5.pdf
pages: 54
crawled: 2026-11-16
translated: 2026-11-16
---

# 第 8 讲：智能体设计 V——成本高效的智能体

> PDF 讲义文本抽取：[8_agent_design_5.pdf](https://cs2680.seas.harvard.edu/slides/8_agent_design_5.pdf) · Harvard CS2680

## 第 1 页

**现代 AI 系统：智能体与系统优化**

Juncheng Yang

智能体设计 V：成本高效的智能体

## 第 2 页

**事务**

- 作业 3 今天开始
  - 比之前的作业难得多
  - 排行榜：每天提交次数有限，没有迟交日
  - 占总成绩 20%：像期中考试一样对待
  - 尽早开始
  - 下周办公时间（时间待定）
- 作业更新
  - 作业 4 现在值 20 分，作业 5 值 10 分
  - 原因：作业 5 太难，且与课程项目和其他课程的项目重叠

## 第 3 页

**事务**

- 日程更新
  - 一些讲座提前，以适应作业变化
  - 两场加分论文展示讲座：今天开放报名
- Claude Code 会话日志
  - 更新所有相关会话的日志
  - 不要修改会话日志：这违反学术诚信

## 第 4 页

**今日安排**

- 成本高效的智能体
- 智能体架构
- 编程智能体案例研究

## 第 5 页

**设计成本高效的智能体**

本讲聚焦 LLM 成本，忽略其他计算成本。

## 第 6 页

**回顾一个会话的结构**

会话 → 第 1 轮 → 第 2 轮 → 第 3 轮 → …

一个 turn：

用户消息 → 模型调用 → 工具调用 → 模型调用 → 回复用户

一个用户轮次 = 多个 LLM 和工具步骤（steps）

## 第 7 页

**成本从哪里来？**

```
Cost = Users × Sessions / User
     × Turns / Session
     × Steps / Turn
     × Tokens / Step
     × Price / Token
```

- ↑ GROW：采用率和参与度
- ↓ SHRINK：智能体轨迹
- ↓ SHRINK：单价

## 第 8 页

**你的 Claude Code 使用情况：每会话轮次**

- 大多数会话只有一个 prompt
- 好：你们大多数人为每个任务开新会话
- 少数人跑马拉松会话

Single-prompt sessions：

- Assignment 1：68%
- Assignment 2：75%

Marathons：100+ turns

## 第 9 页

**减少每个任务的（用户）轮次**

第 k 轮会重读第 1…k−1 轮，因此总成本随轮次数的平方增长。

用户为什么会回来：没有计划、过早停止，或从未检查。

- **前置规划**
  - 行动前先确认目标和计划一次
- **结构化任务分解**
  - 拆成子任务，每个都有完成检查
- **交接前自验证**
  - 返回前运行测试并检查输出

目标：自主完成任务，无需用户中途检查。

每任务轮次 / 每轮步数 / 每步 tokens / 每 token 价格

## 第 10 页

**你的 Claude Code 使用情况：每轮步数**

- 大多数轮次步数很少
- 主要是因为 effort 设为 medium 或 high
- 有些轮次跑了近 1,000 步

每轮步数中位数：

- Assignment 1：3
- Assignment 2：4

## 第 11 页

**减少每轮步数**

- **一次调用一个动作**
  - 4 次模型调用：Model → Tool → Model → Tool → Model → Tool → Model
- **先计划，再批处理**
  - 2 次模型调用：Model → 3 tools in parallel → Model
- **批量独立调用**
  - 一步读五个文件，而不是五步
- **复用计划和 skill**
  - 重放之前有效的做法，而不是重新推导
- **前置加载上下文**
  - 开始时读所需文件，而不是每步读一个

每次模型调用都重读完整上下文，所以调用越少成本越低。

每任务轮次 / 每轮步数 / 每步 tokens / 每 token 价格

## 第 12 页

**复用计划、skill 和经验：相关论文**

- **Skill 库**
  - Voyager（2023）：存储可执行 skill
  - SkillRL（2026）：联合改进 skill 库和智能体策略
- **来自经验的洞见**
  - ExpeL（2023）：提取可复用洞见
  - ReasoningBank（2025）：保留成功和失败运行的策略
- **Playbook 与计划模板**
  - Test-Time Plan Caching（2025）：复用并适配计划模板
- **持久对话记忆**
  - Mem0（2025）：存储并更新事实
  - LightMem（2025）：离线合并
  - SimpleMem（2026）：压缩记忆

ADVANCED——略读，或自行深入阅读

复用在任务重复时才有回报；记忆维护和过时条目可能抹掉节省。

每任务轮次 / 每轮步数 / 每步 tokens / 每 token 价格

## 第 13 页

**你的 Claude Code 使用情况：每步 tokens**

- 主智能体
  - 中位数 200K–300K
  - p90：600K–700K
- 子智能体
  - 中位数约 80K
  - p90：约 200K

Main-agent median：

- Assignment 1：208K
- Assignment 2：301K

## 第 14 页

**你的 Claude Code 使用情况：随步数增长的 tokens**

- 上下文累积并快速增大

Context at step ~500：

- Assignment 1：670K
- Assignment 2：650K

## 第 15 页

**你的 Claude Code 使用情况：大多数 token 是缓存读取**

- 输出比新 prefill（缓存写入）小 5 倍
- 新 prefill 比缓存读取小 100 倍
- 典型价格比，缓存读取 : 输入 : 输出 = 1 : 10 : 50

Cache-read token share：Assignment 1 为 97.6%

## 第 16 页

**减少每步输入 tokens：保持上下文精简**

- **丢掉过时内容**
  - 截断过时结果
  - 掩蔽已使用的工具输出
- **压缩历史**
  - 把旧轮次总结成状态
- **缩小进入内容**
  - 压缩观察
  - 保留错误，而不是完整日志
- **卸载到文件**
  - 保存大输出；传路径
- **只加载所需**
  - 选择性检索：只取相关工具和记忆
  - 隔离探索：子智能体返回摘要

留在上下文中的 token 在之后每一步都要再次付费。

每任务轮次 / 每轮步数 / 每步 tokens / 每 token 价格

## 第 17 页

**减少每步输入 tokens：相关论文**

- **压缩智能体历史**
  - ACON（2025）：峰值上下文减少 26–54%
  - Active Context Compression（2026）：智能体自我压缩，token 减少 23%
  - TRACE（2026）：摘要导致返工
- **上下文作为外部记忆**
  - MemGPT（2023）：上下文作为快速记忆
  - Scroll（2026）：无损外部日志；由代码选择模型看到什么
- **Prompt 压缩**
  - LLMLingua（2023）：最多减少 20 倍 token
  - LongLLMLingua、LLMLingua-2（2024）
  - Prompt Compression in the Wild（2026）：只在长 prompt 上有回报
- **把工具数据留在上下文外**
  - Code execution with MCP（2025）：在代码中过滤结果，150K → 2K tokens
  - Tool Search（2025）：工具 token 减少 85%
  - Programmatic Tool Calling：减少 37%

ADVANCED——略读，或自行深入阅读

每任务轮次 / 每轮步数 / 每步 tokens / 每 token 价格

## 第 18 页

**减少每步输出 tokens：少要一点**

- **Prompt 级约束**
  - 说明长度、格式和要跳过什么
  - 用不超过 100 词回答。（Answer in ≤100 words.）
  - 只返回 JSON。（Return only JSON.）
  - 一句话。前三项。（One sentence. Top 3 items.）
  - 不要复述问题。（Don't restate the problem.）
  - 不要解释推理过程。（Don't explain your reasoning.）
  - 简洁 system prompt：“Be concise; omit background unless requested.”（保持简洁；除非被要求，否则省略背景。）
- **输出 token 上限**
  - 在 API 调用中设硬限制
  - `max_tokens=300`
  - `max_output_tokens=300`
  - 简单，但截断可能把答案切在句子中间
  - 与简洁输出 prompt 配合
  - 注意：推理可能用光上限

每任务轮次 / 每轮步数 / 每步 tokens / 每 token 价格

## 第 19 页

**减少每步输出 tokens：schema 与 effort**

- **结构化输出**
  - 要求只包含所需字段的 schema
  ```json
  {"action": "search",
   "argument": "KV cache"}
  ```
  - 限制 enum 和可选字段，使模型无法添加额外内容
  - 适合工具型智能体：工具调用周围的散文纯属成本
- **自适应推理 effort**
  - 让思考预算与步骤匹配
  - `lookup: effort="low"`
  - `debug:  effort="high"`
  - 查找和格式化用低 effort；规划和调试用高 effort
  - 按调用或按步骤设置，作为 reasoning effort 或 thinking-token 预算

每任务轮次 / 每轮步数 / 每步 tokens / 每 token 价格

## 第 20 页

**减少每步输出 tokens：相关论文**

- **Prompt 与预算**
  - Concise CoT（2024）：要求简洁
  - CCoT（2024）：在 CoT 中设字数限制
  - Chain of Draft（2025）：简洁草稿
  - TALE（2024）：推理 token 预算
- **自适应推理 effort**
  - Ares（2026）：每步选择 effort
  - When to Plan（2025）：只在有用时规划
  - s1、L1（2025）：强制思考预算
  - Reason Efficiently, ShorterBetter
- **结构化输出与解码**
  - Let Me Speak Freely?（2024）：严格格式可能损害推理
  - XGrammar、SGLang（2024）
  - JSONSchemaBench（2025）
- **只输出变化**
  - AdaEdit（2026）：diff 或整文件
  - CodeStruct（2026）：AST 级编辑
  - Tool-making agents（2026）：可复用工具减少输出 token 58%

ADVANCED——略读，或自行深入阅读

每任务轮次 / 每轮步数 / 每步 tokens / 每 token 价格

## 第 21 页

**降低每 token 价格：缓存与批处理**

每 token 价格相对于基础输入（Claude API）：

- 0.05×：批处理 + 缓存输入
- 0.1×：缓存输入
- 0.5×：批处理输入
- 1×：基础输入 token
- 5×：输出 token

- **保持稳定前缀**
  - system prompt、工具、早期历史
- **把能等的批处理**
  - 评估、回填、批量任务

每任务轮次 / 每轮步数 / 每步 tokens / 每 token 价格

## 第 22 页

**降低每 token 价格：模型路由**

- **预先选择**
  - 在生成前为每轮选一个模型
  - 方式：在偏好数据上训练的路由器；也可以选择智能体角色
- **失败后升级**
  - 先试便宜模型；检查失败时向上迁移
  - 检查：学习到的评分器、自验证或执行反馈
- **每步重新路由**
  - 随着智能体轨迹增长重新选模型
  - 方式：根据历史和预算路由；orchestrator 把模型当工具调用

难点：一个廉价的规划错误可能浪费后续许多动作。

每任务轮次 / 每轮步数 / 每步 tokens / 每 token 价格

## 第 23 页

**降低每 token 价格：后续讲座中的系统技术**

- **模型优化**
  - MoE / 稀疏
  - 量化
  - 剪枝
  - 蒸馏
  - 面向工作负载的微调
- **服务引擎优化**
  - 投机解码
  - KV 缓存优化
  - 更好的请求调度
- **硬件**
  - 更快的 kernel
  - 更好的 kernel 调度
  - 专用加速器

每任务轮次 / 每轮步数 / 每步 tokens / 每 token 价格

## 第 24 页

**降低每 token 价格：相关论文**

- **前缀缓存**
  - vLLM（2023）：PagedAttention
  - SGLang（2024）：RadixAttention 前缀缓存
  - Prompt Cache（2024）：模块化复用
- **预先选择**
  - RouteLLM（2024）：学习型路由器
  - MasRouter（2025）：也选择智能体角色
- **失败后升级**
  - FrugalGPT（2023）：学习型级联
  - AutoMix（2023）：自验证
  - EcoAssistant（2023）：执行反馈
- **每步重新路由**
  - ToolOrchestra（2025）：小 orchestrator
  - BAAR、MTRouter（2026）：预算感知

ADVANCED——略读，或自行深入阅读

每任务轮次 / 每轮步数 / 每步 tokens / 每 token 价格

## 第 25 页

**每项节省都有反向成本**

- **压缩 vs 重建**
  - 被丢弃的文件会重新读取，摘要会重写缓存
- **路由 vs 更长的失败**
  - 便宜模型的一个坏计划可能增加许多步骤或一次失败尝试
- **子智能体 vs 重复上下文**
  - 每个子智能体都重读共享文件和指令
- **投机 vs 浪费的工作**
  - 错误猜测烧 token，并争用相同工具

净节省 = 毛节省 − 反向成本；在同一批任务上测量两者。

## 第 26 页

**为每个任务设预算上限，进展停滞时停止**

| 每任务限制 | 示例 |
| --- | --- |
| 金额 | $10 |
| 模型调用 | 80 次调用 |
| 工具时间 | 15 分钟 |
| 每步重试 | 2 次重试 |

根据 tracing 过的运行设置限制，例如成功任务 p95 的 2 倍。

**停止条件**

- 验证器通过
- N 步内没有新的通过测试
- 同一错误重复
- 触到限制：带摘要交接

一个带摘要停止的任务，比一个失控的任务成本更低。

示例限制仅作说明。

## 第 27 页

**你真的需要 LLM 吗？**

- 每次都走相同步骤？写脚本
  - 让 LLM 写一次代码，然后只运行它
- 输入格式固定？用规则解析
  - 正则、parser 和模板每次调用零成本
- 只需狭窄的标签或分数？训练一个小分类器
  - GBM 或 Jev!
- 固定工作流、很少推理？把工作流脚本化
  - 只在需要推理的步骤调用 LLM

只有当某一步需要推理时才求助 LLM。

## 第 28 页

**让你的智能体更快**

更快的智能体通常（但不总是）也更便宜。

- 加速 LLM 服务
- 改进编排
- 加速工具调用
- 并行化工作
- 投机动作

## 第 29 页

**完成时间是关键路径，而不是所有步骤之和**

Serial：time ≈ 所有步骤之和

排队 → 初始化 → Prefill → 推理 → 工具 → 编排

Parallel：time ≈ 关键路径

计划 → Worker A / Worker B → 合并

红色：决定完成时间的关键路径

- 更便宜可能更慢：小模型可能需要更多步
- 并行成本更高：等待更少，总 token 更多

## 第 30 页

**加速 LLM 服务**

上一节的每项成本技术也会降低延迟。

更少轮次 / 更少步骤 / 更少 tokens / 更便宜的服务 / 缓存、更小的模型

## 第 31 页

**改进编排**

- **异步执行**
  - 例如工具调用运行时开始下一步
- **持久会话**
  - 例如跨步骤保持一个 shell 或浏览器打开
- **流式与流水线**
  - 例如在 LLM 响应完成前开始工具调用
- **服务同置**
  - 例如在与模型相同的主机上运行工具

## 第 32 页

**加速工具调用**

构建、测试和页面加载可能比模型调用本身更久。

- **缓存工具结果**
  - 重复读取和搜索命中缓存
- **更快的硬件**
  - 在服务器而不是笔记本上跑重计算
- **更好的工具**
  - 同一工作用更快、更便宜的工具；选择性调用工具
- **快速失败**
  - 让挂起的调用超时

调模型之前，先测量每步的工具时间。

## 第 33 页

**并行化工作**

串行：读取文件 A → 读取文件 B → 读取文件 C

并行：读取文件 A / 文件 B / 文件 C 同时

同样的工作，三分之一的等待。

- **并行工具调用**
  - 一步发出独立调用
- **并行子智能体**
  - 拆分独立子任务；合并摘要

只有独立工作才并行；共享状态需要合并步骤。

## 第 34 页

**投机动作**

1. **预测**
   - 一个便宜模型猜下一个动作
2. **提前运行**
   - 主模型思考时执行猜测
3. **比较**
   - 把猜测与主模型的选择对比

- 猜中：结果已就绪；跳过等待
- 猜错：丢弃；成本是一次浪费的调用

当猜测经常正确且动作可撤销时才有回报。

**开放问题**

如何在有限的 GPU、CPU 和 API 预算下调度投机调用，使节省的关键路径时间超过浪费的工作。

## 第 35 页

**投机什么**

| 对象 | 内容 | 工作 |
| --- | --- | --- |
| 工具意图（Tool intent） | 下一个是哪个工具 | SPORK [8] |
| 工具调用（Tool call） | 工具及其参数 | PASTE [5]、Speculative Tool Calls [2] |
| 下一个动作（Next action） | 任意动作或 API 响应 | Speculative Actions [1] |
| 分支（Branches） | 同时探索多条可能路径 | B-PASTE [6] |
| 轨迹（Trajectory） | 一条已经执行的多步链 | Speculative Macro Commit [10] |

视野从一次调用增长到整条轨迹。

ADVANCED——略读，或自行深入阅读

Sources: [1] Speculative Actions (ICLR 2026) · [2] Speculative Tool Calls (arXiv 2025) · [5] PASTE (arXiv 2026) · [6] B-PASTE (arXiv 2026) · [8] SPORK (arXiv 2026) · [10] Speculative Macro Commit (arXiv 2026)

## 第 36 页

**预测来自哪里**

- **基于模型（Model-based）**
  - 一个小 draft 模型预测大模型下一步会做什么
  - Speculative Actions [1]、Speculative Tool Calls [2]
- **自投机（Self-speculative）**
  - 同一模型的早期分支预测它自己稍后的工具调用
  - SPORK [8]
- **基于历史（History-based）**
  - 过去的轨迹预测下一个工具，其参数绑定到最后一个结果
  - PASTE [5]、Speculate with Memory [9]
- **无损（Lossless）**
  - 保留工作前总是验证
- **有损（Lossy）**
  - SPAgent [3] 跳过一些检查

ADVANCED——略读，或自行深入阅读

Sources: [1] Speculative Actions (ICLR 2026) · [2] Speculative Tool Calls (arXiv 2025) · [3] SPAgent (arXiv 2025) · [5] PASTE (arXiv 2026) · [8] SPORK (arXiv 2026) · [9] Speculate with Memory (arXiv 2026)

## 第 37 页

**两个例子**

**PASTE [5]**：从过去轨迹预测下一个工具

```
search(q)
  → visit(results[0].url)
  → extract(page)
```

一旦 `search(q)` 开始，轨迹模式表明下一步是 visit。URL 从搜索结果填入，因此 visit 在模型仍在生成时就开始运行。

**SPORK [8]**：模型预测自己的工具调用

```
think: 2,000 tokens …
  early probe → search(q)
tool_call search(q): ready
```

工具意图在推理早期往往已经清楚。一个分叉 probe 启动预测的调用，主模型发出调用时结果已经在那里。

Sources: [5] PASTE (arXiv 2026) · [8] SPORK (arXiv 2026)

## 第 38 页

**在循环中优化：运行、测量、修改、再来**

1. **运行并 profile**
   - 记录每次调用、token、工具和等待
2. **测量**
   - 理解成本和延迟的来源
3. **只改一件事**
   - 压缩、路由、缓存或并行
4. **重新评估**
   - 同样的任务：成功率、花费、p95 延迟

重复。

记住这一点，用于作业 4！

## 第 39 页

**智能体架构**

Monolithic · Modular · Microkernel

## 第 40 页

**三种框架架构**

1. **Monolithic harness（单体框架）**
   - 一切都在一个运行时中
   - Agent 包含 memory、tools、context、planning、execution
2. **Modular harness（模块化框架）**
   - 接口，一个控制器
   - 智能体 → MemoryProvider / ToolProvider / ContextProvider / SandboxProvider（记忆、工具、上下文、沙箱接口）
3. **Agent microkernel（智能体微内核）**
   - 核心只保留协调
   - 智能体运行时（状态 · 调度 · 安全）→ 标准化协议 → 记忆 / 工具 / 执行调度

转变：责任从智能体中移出，从代码到接口再到服务。

## 第 41 页

**单体框架：一个运行时实现记忆、工具、上下文、规划和执行**

```python
class CodingAgent:
    def __init__(self):
        self.memory   = Memory()
        self.tools    = Tools()
        self.context  = ContextManager()
        self.planner  = Planner()
        self.executor = Executor()
    def run(self, task):
        while not self.finished:
            a = self.planner.plan(task)
            r = self.executor.execute(a)
            self.context.update(r)
```

**优点**

- 实现和调试简单
- 通信开销最小
- 内部状态易于共享
- 执行开销低

**缺点**

- 难以替换某个组件
- 组件紧密耦合
- 难以跨智能体共享基础设施
- 隔离难以强制

关键特征：智能体在一个运行时中拥有一切。

## 第 42 页

**模块化框架：智能体仍控制循环，但通过接口访问每个组件**

```python
agent = CodingAgent(
  memory_provider=RedisMemory(),
  tool_provider=MCPTools(),
  context_provider=SlidingWindowContext(),
  sandbox_provider=DockerSandbox())
# Docker → Firecracker: swap one provider
```

单体：智能体 → 内置记忆

模块化：智能体 → MemoryProvider → RedisMemory

**优点**

- 组件替换容易
- 更好的测试和扩展性
- 职责分离清晰
- 第三方实现可插入

**缺点**

- 控制器仍拥有生命周期
- 协调逻辑变复杂
- 故障域仍可能共享
- 联合调优需要修改控制器

关键特征：一个控制器通过接口委派。

## 第 43 页

**智能体微内核：小运行时协调，外部服务提供能力**

智能体运行时（状态 · 协调 · 调度 · 安全）

→ 标准化协议

→ 记忆服务（数据库）/ 工具服务（工具 API）/ 执行服务（沙箱）

服务可以运行在独立容器或机器中。

**优点**

- 服务独立扩展
- 更好的故障隔离
- 如果强制实施，隔离更强
- 共享、集中管理的基础设施

**缺点**

- 更高的通信开销
- 更多故障模式
- 端到端调试更难
- 需要标准协议和生命周期

关键特征：运行时协调；外部服务提供能力。

## 第 44 页

**运行一段 Python：只有微内核把沙箱管理交给自己的服务**

1. **Monolithic**
   - 智能体 → 本地执行 Python
2. **Modular**
   - 智能体 → `SandboxProvider.run(code)` → 执行 Python
3. **Microkernel**
   - 智能体运行时 → 发送执行请求 → 执行服务 → 分配沙箱 → 执行 Python，返回结果

微内核：执行服务拥有分配、隔离和沙箱生命周期。

- 跳数最少；隔离难以强制
- 换 provider，而不是换智能体

## 第 45 页

**微内核以简单性和低开销换取隔离、共享和规模**

| 维度 | Monolithic | Modular | Microkernel |
| --- | --- | --- | --- |
| 设计原则 | 一切集成 | 接口抽象 | 最小核心 + 服务 |
| 中央控制器 | 是 | 是 | 是，但弱化 |
| 组件替换 | 困难 | 容易 | 容易，如果协议匹配 |
| 执行隔离 | 可选 | 可选 | 架构强调 |
| 组件部署 | 通常一起 | 一起或分离 | 常常独立 |
| 独立扩展 | 有限 | 可能 | 强 |
| 通信成本 | 低 | 低–中 | 可能更高 |
| 典型用例 | 独立智能体 | 智能体框架 | 多智能体基础设施 |

适配：单体适合独立智能体，微内核适合多智能体基础设施。

## 第 46 页

**八个框架**

- **CC　Claude Code**
  - Anthropic · TypeScript（闭源）
  - Claude 周围的策略层和类型化 hooks
- **CX　Codex CLI**
  - OpenAI · Rust
  - 沙箱优先，询问其次
- **DSH　DeepSeek Harness**
  - DeepSeek AI · TypeScript
  - 一切皆 plugin，甚至循环
- **OC　OpenCode**
  - Anomaly (SST) · TypeScript、Bun
  - 一个会话服务器，客户端很薄
- **PI　Pi**
  - Mario Zechner / Earendil · TypeScript
  - 一个用 TypeScript 扩展的小核心
- **OMP　oh-my-pi**
  - Can Bölük / Stencil Labs · TypeScript + Rust
  - Pi 分支，原生工具和 IDE 接入
- **CLAW　OpenClaw**
  - OpenClaw Foundation · TypeScript
  - 面向聊天渠道的助手网关
- **HM　Hermes Agent**
  - Nous Research · Python
  - 一个会自己写 skill 的智能体

## 第 47 页

**Codex CLI 独有**

- **批准前先沙箱**
  - 命令在无网络访问的沙箱中运行。智能体只有要离开沙箱时才请求批准。
- **遵守文法的补丁**
  - Lark 文法设定补丁封装。智能体分四遍匹配 hunk。

## 第 48 页

**DeepSeek Harness 独有**

- **循环也是 plugin**
  - 循环、适配器、工具、日志和审批都是 plugin。YAML 层可以替换每个 plugin。
- **请求来自日志**
  - 每个请求是会话日志的冻结视图。框架只向该日志添加条目。
- **Compare-and-swap 编辑**
  - 如果文件在模型上次读取后发生变化，编辑失败。

## 第 49 页

**OpenCode 独有**

- **框架是一个服务器**
  - TUI、SDK 和 Web 应用使用同一个 OpenAPI HTTP 服务器。
- **带大小限制的模糊编辑**
  - 九个替换器从精确匹配到锚点匹配。框架拒绝过大的模糊匹配。
- **每步一个快照**
  - 影子 git 仓库让 `/undo` 恢复文件，而不只是聊天。

## 第 50 页

**Pi 独有**

- **最小核心**
  - 核心有四个工具，没有 MCP、子智能体或审批。扩展提供所有其他功能。
- **带价格检查的缓存预热**
  - 只有预期节省 ≥ $0.05 时，Pi 才发送 keep-alive 请求。
- **供其他项目使用的库**
  - pi-ai 在 10 种 wire API 上支持 42 个提供商。另外三个项目使用 Pi 代码。

## 第 51 页

**oh-my-pi 独有**

- **Hashline 编辑**
  - 每次编辑给出 4 位十六进制文件标签和行号。模型不再重新输入旧文本。
- **进程内 IDE**
  - 一个 shell 为所有调用保持打开。原生工具提供搜索、AST、LSP 和调试器。
- **特殊上下文方法**
  - snapcompact 把旧历史变成图像。当正则匹配时，TTSR 停止并重试。

## 第 52 页

**OpenClaw 独有**

- **带队列通道的聊天网关**
  - 27 个聊天渠道把消息发到每个会话一个通道。队列模式控制运行期间到达的消息。
- **压缩前先记忆**
  - 首先，一个静默轮次写入带日期的笔记。召回同时使用全文搜索和向量搜索。
- **Fences、taint 和 sentinels**
  - Fences 隔离不受信任的文本。网络读取会污染该轮。智能体监控秘密 sentinel。

## 第 53 页

**Hermes Agent 独有**

- **会学习的分支**
  - 后台分支检查每个被轻推的轮次，然后编辑记忆和 skills。
- **最早压缩**
  - 压缩在窗口的 50% 开始。这是八个框架中最早的。
- **执行前保存**
  - 在任何副作用发生前，智能体把工具调用行写入会话数据库。

## 第 54 页

**下一节课**

- 智能体安全与保障
- 自进化框架
