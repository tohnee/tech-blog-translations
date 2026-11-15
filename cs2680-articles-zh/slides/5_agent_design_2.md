---
title: "第 5 讲：智能体设计 II——多智能体系统"
title_en: "Agent Design II: Multi-Agent Systems"
source: https://cs2680.seas.harvard.edu/slides/5_agent_design_2.pdf
pages: 46
crawled: 2026-11-16
translated: 2026-11-16
---

# 第 5 讲：智能体设计 II——多智能体系统

> PDF 讲义文本抽取：[5_agent_design_2.pdf](https://cs2680.seas.harvard.edu/slides/5_agent_design_2.pdf) · Harvard CS2680

## 第 1 页

**现代 AI 系统：智能体与系统优化**

Juncheng Yang

智能体设计 II：多智能体系统

## 第 2 页

**事务**

- Claude Code Premium seat
- 作业 1
  - Canvas
  - repo url
  - mini product
- 作业 2 在等你，约两周后截止
- 办公时间：下周四 3:30–5pm，SEC 4.308
- Pre-proposal

## 第 3 页

**今日安排**

- 多智能体设计
- 架构
- 协调：任务分解
- 通信
- 智能体记忆

## 第 4 页

（空白页）

## 第 5 页

**从一个智能体到多个**

- 架构
- 协调
- 通信

多智能体并不新鲜，它已有数十年的研究历史，我们不会深入展开。

## 第 6 页

**何时以及为什么要把工作拆给多个智能体？**

- **专门化**
  - 不同的模型、prompt 和工具
- **隔离**
  - 给不同智能体不同权限
- **并行**
  - 独立子任务并发执行
- **上下文管理**
  - 不要给每个智能体完整轨迹

举手

## 第 7 页

**每个架构背后的三个问题 / 三张图**

- **控制图：谁来协调？**
  - 一个 supervisor、一个层级，还是根本没有人；运行时是否变化（handoff）
- **通信图：它们如何通信？**
  - 直接消息、广播，还是共享工作区
- **任务图：工作如何分解？**
  - 由 planner 预先拆分、通过竞价，还是从局部规则中涌现

## 第 8 页

**多智能体架构**

1. Supervisor–worker
2. Hierarchical
3. Pipeline / DAG
4. Blackboard
5. Committee
6. Market
7. Swarm
8. Dynamic topology

## 第 9 页

**1. Supervisor–worker**

- 一个智能体负责计划、委派和集成；工作者只看到自己的子任务

主管（Supervisor）→ 研究员 / 编码者 / 审查者

子任务独立且可并行时最佳。

弱点：supervisor 成为瓶颈：它要重读每个结果，上下文增长最快。

Task：supervisor 预先拆分 · Control：一个 supervisor · Comms：星形，经 supervisor

## 第 10 页

**2. 层级式智能体**

- Supervisor–worker 的递归应用：supervisor 管理子 supervisor
- 适合本身就能层级分解的任务——存储、查询引擎、测试
- 挑战：分解发生在哪里，以及多少上下文跨越每个边界？

功能经理 → 后端负责人 / 前端负责人 → API / 数据库 / UI / E2E 测试

示例：功能构建

Task：每层再次拆分 · Control：嵌套 supervisor · Comms：树形，仅父子

## 第 11 页

**3. 流水线 / DAG**

- 固定阶段，每个边界都有类型化契约
- 调试成本最低的拓扑——错误会定位到某个阶段
- 弱点：没有回退路径；第四阶段无法向第一阶段索取更好的来源。

OCR → 字段提取 → 与 PO 匹配 → 审批 → 入账

一条重试边胜过再多一个智能体

示例：发票处理

Task：阶段在设计时固定 · Control：顺序就是控制 · Comms：阶段到阶段

## 第 12 页

**4. 黑板与共享记忆**

- 智能体通过共享状态而不是直接消息来协调
- 工作区可以是数据库、向量存储、文件系统、Git 仓库或任务图

Task：从共享状态涌现 · Control：无中心控制 · Comms：间接，经工作区

智能体可以加入或离开而无需重新接线；共享状态持久且可检查。

挑战：一致性、并发控制、来源、版本管理、垃圾回收。

Git repository：任务列表、commit、历史

功能智能体 / 重构智能体 / 测试智能体

示例：智能体共享一个 Git 仓库

## 第 13 页

**5. 委员会 / 辩论**

- 智能体提出并讨论，然后由 judge 或投票解决分歧

Judge → Grader A / Grader B

示例：论文评分

Task：一个任务，并行重复 · Control：judge 决定 · Comms：同伴之间，然后到 judge

在判断密集型任务上提高准确率

失败模式——没有独立性的共识：相同模型和上下文，相同盲点。

## 第 14 页

**6. 市场与拍卖**

- 智能体根据能力、成本和延迟对公布的任务竞价
- 异构智能体在模型、工具、机器、成本和专长上各不相同

“谁能跑这个训练任务？”

- A100 node：$0.20 · ETA 3s
- T4 node：$0.05 · ETA 10s
- H100 node：$0.40 · ETA 1s

任务交给 A100 node

示例：GPU 任务路由器——5 秒内最便宜的出价获胜

Task：公布，由出价认领 · Control：拍卖师清算 · Comms：广播，出价返回

工作落到最便宜的有能力智能体上，无需中央计划者。

弱点：出价是自报的，智能体可以夸大能力来获胜。

## 第 15 页

**7. 蜂群（Swarm）**

- 没有永久协调者，智能体直接协商并交换发现
- 需要发现、寻址、同步、终止、信任等协议

拣货机器人 1 / 拣货机器人 2 / 拣货机器人 3 / 拣货机器人 4

示例：仓库机器人协商谁拣哪些订单

没有协调者成为瓶颈或故障点；同伴进出时工作继续。

弱点：通信复杂度 O(n²)；冲突解决困难。产品中很少使用。

Task：本地协商 · Control：无永久协调者 · Comms：全对全，O(n²)

## 第 16 页

**8. 动态拓扑**

- 任务运行期间增加、移除或重新连接智能体

示例：支持机器人只在工单升级时加入计费 agent 和日志 agent。

常规工单 → 支持机器人 → 工单升级 → 升级后：支持机器人 + 计费智能体 + 日志智能体

Task：工作变难时重新拆分 · Control：随智能体加入而转移 · Comms：运行时动态

容量随难度扩展；简单工单保持廉价。

弱点：每次运行形状不同，故障难以复现。

## 第 17 页

**真实系统是混合体**

主管 → 规划智能体 → 动态任务 DAG → 编码者 / 研究者 / 测试者 → 共享 Git → 审查者

结合：

- 层级结构
- 共享记忆
- 必要时重新规划的流水线

## 第 18 页

**八种架构**

| 类别 | 架构 | 核心思想 | 最适合 | 弱点 |
| --- | --- | --- | --- | --- |
| 集中式 | Supervisor–worker | 一个计划者，多个工作者 | 可分离子任务 | 计划者瓶颈 |
| 集中式 | Hierarchical | 监督者的监督者 | 递归拆分 | 错误放大 |
| 集中式 | Pipeline / DAG | 每个阶段喂给下一个 | 清晰有序阶段 | 错误传播 |
| 集中式 | Market / auction | 智能体对任务竞价 | 动态分配 | 糟糕出价 |
| 去中心化 | Blackboard | 共享工作区 | 一个共享工件 | 状态过期 |
| 去中心化 | Committee / debate | 回答，然后协调 | 判断型任务 | 群体思维 |
| 去中心化 | Swarm | 直接对话，无控制者 | 本地协商 | O(n²) 消息 |
| 混合 | Dynamic topology | 随工作推进重新连线 | 未知结构 | 难以调试 |

## 第 19 页

**任务分解**

复杂任务 → 子任务 1 / 子任务 2 / 子任务 3 → 合并结果

## 第 20 页

**任务分解**

- **Data**：每个智能体处理文档或记录的一个子集
- **Expertise**：安全、性能、正确性、法律分析
- **Stage**：计划、实现、测试和审查
- **Hypothesis**：智能体调查竞争性解释
- **Tool**：Web、数据库、代码执行或内部文档
- **Authority**：智能体在不同管理域中行动

示例：一个 200 文件的 PR 先按 data（文件）拆分，再按 expertise（安全、性能）拆分。

## 第 21 页

**创建子任务时需要考虑的事项**

- 目标
- 输入与相关上下文
- 边界与排除项
- 可用工具与权限
- 期望输出 schema
- 完成测试
- 预算与截止时间
- 依赖

**差的子任务**

“Research storage systems”

**更好的子任务**

“找出 2026 年发表的存储相关论文；返回标题、日期、系统贡献、评估规模和一手来源 URL；排除数据库查询优化”

## 第 22 页

**粒度权衡**

- 任务太大：并行度低；工作保持串行
- 任务太小：调度和通信开销占主导

Tmulti ≈ Tplanning + Tcritical path + Tcommunication + Tmerge

只有当节省的串行工作超过计划、通信和集成成本时，并行才有帮助。

示例：20 个单行查找批成 4 个子任务，使开销低于收益。

## 第 23 页

**静态 vs 动态分解**

- **Static**：执行前已知；可预测、易评估。示例：总结五份上传的 PDF。
- **Dynamic**：智能体根据发现创建新任务。示例：死链派生一个查找任务。
- **Recursive**：工作者本身也可以委派。示例：审查智能体为每个子领域启动一个子智能体。
- **Opportunistic**：空闲智能体认领新出现的任务。示例：空闲智能体拿起下一个未标注文档。

分解需要派生上限、预算、深度限制和终止条件。否则委派会递归爆炸。

## 第 24 页

**常见分解失败**

**01 Overlap**

Agent A / Agent B：两个智能体总结同一篇论文

**02 Gap**

2020–23 / 2024 / 2025–26：“2020–2023”加“2025–2026”跳过了 2024

**03 Hidden dependency**

Sizing → Pricing：Pricing 需要 Sizing，但只有运行时才发现

**04 Unmergeable outputs**

Unstructured / JSON：一个智能体返回自由文本，另一个返回 JSON；合并失败

## 第 25 页

**常见分解失败（续）**

**05 Lost global context**

§1 ✓　§2 ✓　§3 ✓　整份报告 ✗

每一节都没问题；整份报告自相矛盾

**06 Straggler**

20s / 25s / 4 min

六个智能体 20 秒完成，一个花了 4 分钟

## 第 26 页

**智能体通信**

用户 → 研究智能体 → Web 智能体 / 编码智能体 / 数据智能体 → 最终答案

## 第 27 页

**多智能体通信的四个维度**

- **Topology**
  - 谁能和谁说话？
  - supervisor–worker、对等
  - 由架构决定（前面讨论过）
- **Medium**
  - 信息如何交换？
  - 消息、共享内存、文件、数据库
- **Format and Semantics**
  - 消息如何结构化、如何表达信息？
  - delegate、report、ask、handoff、cancel
- **Channel**
  - 信息如何传递？
  - p2p、广播、pub–sub、共享状态、请求—响应

## 第 28 页

**通信介质**

- **消息传递**
  - 智能体通过队列或总线发送显式消息
  - 例：coder 把结果投递到 orchestrator 的收件箱
- **共享内存**
  - 一个进程内状态对象，每个智能体都读写
  - 例：工作完成时更新的共享任务列表
- **文件与工件（包括 DB）**
  - 工作产物通过文件存储交接
  - 例：researcher 写 `notes.md`；writer 打开它

## 第 29 页

**通信通道**

- **直接点对点消息**
  - Planner 把任务规范交给 coder 智能体
- **广播**
  - Orchestrator 告诉每个智能体构建失败了
- **发布—订阅**
  - 智能体订阅“new ticket”主题并响应
- **共享黑板**
  - 智能体读写同一个共享发现草稿
- **请求—响应**
  - 智能体查询检索智能体并等待文档
- **工件传递**
  - 一个智能体写 `report.md`；下一个读它

## 第 30 页

**消息格式**

- **自然语言**
  - 灵活，但含糊
- **结构化消息**
  - 易校验，表达力较弱

实用设计两者兼用：

```json
{
"task_id": "T17",
"type": "result",
"status": "complete",
"claim": "The regression began after commit X",
"confidence": 0.82,
"evidence": ["log:2391", "commit:X"],
"artifact": "analysis/T17.json",
"requires_response": false
}
```

## 第 31 页

**消息应携带语义**

内容用自然语言，协调用结构化协议。

**把控制与内容分开**

全塞进一个字符串：

```json
{"message": "some text"}
```

结构化：

```json
{"id": "msg-381",
"task_id": "t-17",
"from": "planner",
"to": "researcher",
"type": "DELEGATE",
"payload": { ... } }
```

运行时知道的操作：

DELEGATE　QUERY　REPORT　HANDOFF　UPDATE　CANCEL　ACK　ERROR　COMPLETE

运行时可以路由、重试和停止，而无需问 LLM 这条消息是什么意思。

## 第 32 页

**通信：设计空间**

| 维度 | 选项 | 经验法则 |
| --- | --- | --- |
| Topology | supervisor–worker、peer-to-peer、mesh | 镜像任务的依赖关系 |
| Medium | messages、shared memory、files | 每条链路一种介质 |
| Channel | p2p、broadcast、pub–sub、request–reply | 只有所有人都需要知道时才广播 |
| Format | natural language + control fields | 按字段路由，不按散文路由 |

每个选择都在延迟、上下文或可靠性之间取舍。

## 第 33 页

**通信是一个困难的分布式系统问题**

Agent A → “purchase 8 GPU instances” → Agent B

网络超时——没有回复

B 执行了动作吗？

- 重试，还是放弃？
- at-most-once 还是 at-least-once？
- 这里真有 exactly-once 吗？
- 在 `task_id` 上放幂等键
- 补偿 / 回滚路径
- 而且重复购买谁来付钱？

## 第 34 页

**分布式系统很难**

- **部分失败**：你无法区分慢智能体和死智能体
- **并发与非确定性**：许多机器同时修改状态
- **复制状态之间的一致性**：一致性、可用性、分区、延迟之间的权衡
- **没有全局时钟**：不同机器上的时钟不一致
- **不可靠网络**：丢包、延迟、重排、重复……
- **调试与可观测性**：大量请求、带时钟漂移的分布式日志

多智能体系统继承了常见的分布式系统问题。

## 第 35 页

**系统运行多个智能体时的更多挑战**

- **Scheduling**：谁下一个运行，运行多久
- **State management**：检查点、记忆、来源、版本管理
- **Resource allocation**：模型、CPU 和其他共享资源

没有预先确定的请求流：系统无法知道谁需要运行、运行多久、每个智能体将消耗多少资源。

## 第 36 页

**考虑黑盒 LLM 时更难！**

**Context**

- 信息丢失：摘要丢掉了工作者知道的内容
- 上下文污染：重要的东西被掩埋
- 过时信息：X=5 之后 B 仍按 X=3 行动
- 信念冲突：A 说安全，B 说脆弱

**协调与通信 / 可观测性与故障诊断**

- 为什么失败？
- 失去归属：每个智能体都以为另一个拥有它
- 通信循环：A 问 B，B 问 C，C 问 A

## 第 37 页

**A2A：agent ↔ agent**

Agent A → 发现能力 → Agent B

发送消息、创建任务 → 进度更新 → 返回工件

示例：“分析公司 X 是否应把推理栈迁移到 GPU Y。”

- Research Agent：通过 Agent Cards 找到同伴
- Finance Agent：估算 GPU 成本
- Search Agent：查找基准数据
- Coding Agent：运行这些基准

## 第 38 页

**A2A agent card**

每个 A2A server 发布一张机器可读的卡：发现加能力描述。

```json
{
"name": "Travel Agent",
"description": "Plans business travel",
"skills": [{ "id": "book-flight" }],
"supportedInterfaces": [ ... ],
"capabilities": { "streaming": true },
"securitySchemes": { ... }
}
```

```
GET /.well-known/agent-card.json
```

调用者可以了解：

- **Identity**——这个智能体是谁
- **Skills**——它声称能做什么
- **Endpoints**——在哪里、如何调用
- **Capabilities**——流式、推送
- **Auth**——需要满足哪种安全方案

## 第 39 页

**A2A 的三个抽象**

一条 message 启动一个 task；task 以 artifacts 返回结果。

- **Message**
  - 客户端与智能体之间的一轮
  - 示例：“Book a flight to Boston”
- **Task**
  - 带 ID 和生命周期的有状态工作单元
  - 示例：task-42: working → completed
- **Artifact**
  - 任务产生的输出
  - 示例：行程 PDF 和订票数据

starts / returns

后续消息加入同一个任务：“Which date?” → “Oct 3”

## 第 40 页

**A2A 任务生命周期**

A2A 是有状态任务协议：工作可以暂停等待输入或认证，然后恢复。

Submitted（已提交）→ Working（工作中）→ Input required（需要输入）/ Auth required（需要认证）→ Completed（已完成）/ Failed（失败）/ Rejected（被拒绝）/ Canceled（已取消）

示例：“Book a flight” → Input required：“Which date?” → “Oct 3” → Working again

## 第 41 页

**跟踪长时运行任务**

任务可以运行数秒或数小时；调用者选择跟踪方式。

- **Polling**
  - 客户端反复检查直到完成
  - 用于：短任务
- **Streaming**
  - 流式实时更新
  - 用于：交互式输出
- **Push notification**
  - 完成时触发 webhook
  - 用于：数小时长的任务

A2A 标准化的是通信，不是编排：委派、拆分和停止仍由框架负责。

## 第 42 页

**MCP：agent ↔ capability**

MCP 是智能体的服务边界：一次工具调用，一个结果。

文件系统 / 数据库 / GitHub / 浏览器 → Agent → MCP

MCP 标准化什么：

- **tools**——可调用、有类型的 capabilities
- **resources**——host 可以附加的可读数据
- **prompts**——可复用交互模板
- 一个 client 与多个 server 对话
- 由 host 而非模型决定暴露什么

## 第 43 页

**MCP vs. A2A**

一个 A2A 远程智能体本身可以调用二十个 MCP server。

| | MCP | A2A |
| --- | --- | --- |
| 主要抽象 | capability / tool | agent / task |
| 关系 | agent → service | agent → agent |
| 发现 | tools、resources、prompts | agent capabilities |
| 工作单元 | 一次工具调用 | 长时运行任务 |
| 内部状态 | 能力接口 | 理想情况下不透明 |
| 类比 | 设备 / API 接口 | 服务间 RPC |

## 第 44 页

**设计原则**

1. **多智能体真的必要吗？**
   - 单智能体足够；多智能体常常只增加开销和复杂性
2. **决定拓扑**
   - 反映任务依赖，最小化通信
3. **识别信息丢失点**
   - 把聚合节点视为细节丢失之处
4. **识别失败隔离边界**
   - 确保系统不会停滞

密集网状结构很少是最佳默认。更多通信会增加上下文压力，却不增加有用信息。

## 第 45 页

**下一节课**

- 智能体设计 III
- 智能体记忆
- 智能体可靠性
- 智能体评估

## 第 46 页

（空白页）
