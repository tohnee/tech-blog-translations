---
title: "第 4 讲：智能体设计 I——上下文管理与工具设计"
title_en: "Agent Design I: Context Management and Tool Design"
source: https://cs2680.seas.harvard.edu/slides/4_agent_design_1.pdf
pages: 56
crawled: 2026-11-16
translated: 2026-11-16
---

# 第 4 讲：智能体设计 I——上下文管理与工具设计

> PDF 讲义文本抽取：[4_agent_design_1.pdf](https://cs2680.seas.harvard.edu/slides/4_agent_design_1.pdf) · Harvard CS2680

## 第 1 页

**现代 AI 系统：智能体与系统优化**

Juncheng Yang

智能体设计 I：上下文管理与工具设计

## 第 2 页

**事务**

- 作业 1 本周日截止
- 分享你的 repo
- 填写 Google 表单
- 作业 1 分享报名本周四开始

## 第 3 页

**今日安排**

- 智能体循环（ReACT）
- 工具设计
- 上下文管理
  - prompt 工程
  - 上下文工程

## 第 4 页

**ReAct 循环**

在一个循环中推理与行动。

- **Thought（思考）**
  - 我知道什么、缺什么、下一步做什么？
- **Action（行动）**
  - 发出一个环境可以运行的结构化调用。
- **Observation（观察）**
  - 环境用事实回答。

- 只推理：没有任何东西检查推理；小错误会累积成自信的幻觉。
- 只行动：没有计划支撑的工具调用；模型会重复自己。
- ReAct：Thought 引导下一个 Action；Observation 纠正下一个 Thought。

重复，直到观察回答了问题——或停止规则结束运行。

https://arxiv.org/pdf/2210.03629

## 第 5 页

**智能体循环（实现）**

```python
messages = [
    {"role": "system", "content":
        "Solve the task using the tools."},
    {"role": "user", "content": user_request},
]
for step in range(MAX_STEPS):
    response = call_model(messages, tools)
    messages.append(response.message)
    if response.final_answer:
        return response.final_answer
    for call in response.tool_calls:
        args = validate(call.arguments)
        result = execute_tool(call.name, args)
        messages.append({
            "role": "tool",
            "tool_call_id": call.id,
            "content": serialize(result),
        })
raise RuntimeError(
    "Agent exceeded its step limit")
```

用户请求 → 模型 → 下一个动作？→ 执行工具 → 返回工具结果 → 返回答案；final answer / tool call

## 第 6 页

**智能体循环（框架职责）**

- 组装上下文
  - 作为智能体框架设计者，你将要做的事
- 校验请求、检查权限并运行它
- 可选地处理结果并管理上下文
- 编写工具定义

用户请求 → 模型 → 下一个动作？→ 执行工具 → 返回工具结果 → 返回答案；final answer / tool call

## 第 7 页

**编程智能体的组成**

三个组件，一个上下文窗口——要把它们放在一起设计。

**01 模型 + 智能体循环**

LLM 提出动作，看到结果，重复直到完成。

→ 智能体 = 模型 + 循环

**02 工具与护栏**

搜索、读取、编辑、运行测试与 shell——位于权限、沙箱和审批之后。

→ 工具设定能力；护栏保证安全

**03 状态：上下文与记忆**

窗口现在有什么，加上智能体在步骤之间携带什么。

→ 组装它；保留跨轮次存活的内容

## 第 8 页

**我们应该为智能体提供哪些工具？**

- 搜索 / 读取
- 编辑 / 写入
- 执行
- 其他

举手 = 得分

## 第 9 页

**智能体应如何找到相关代码？**

举手 = 得分

## 第 10 页

**工具：搜索与读取——glob 与 grep**

- 智能体在 ls、glob 和 grep 上循环——无需构建或维护同步
- 始终反映实时仓库
- 成本：消耗轮次和上下文；词法匹配会漏掉同义改写

示例——“fix the login timeout”

1. grep
   - `grep -rn "timeout" src/`
   - 12 个文件 37 处命中
2. glob
   - `glob src/**/auth/*.ts`
   - 缩小到 `auth/retry.ts`
3. 读取 + 打补丁
   - `read auth/retry.ts`
   - `RETRY_MS = 500` → 已打补丁

## 第 11 页

**工具：搜索与读取——语义搜索**

- 语义：对代码块做 embedding，按含义检索
- 结构：文件树加排序符号（Aider 的 repo map）
- 查询时很快；成本在于建索引和重新同步

示例——“where do we rate-limit?” 第一次查询就返回 `throttle.ts`

**Embedding search**

查询 → 最近的块

同样的含义、不同的词——向量会靠得很近

**Structural search——repo map**

```
aider/coders/base_coder.py:
  class Coder:
    def apply_updates(self)
aider/commands.py: class Commands
```

文件、类和签名的排序大纲

## 第 12 页

**工具：搜索与读取——外部信号**

- 源代码之外的证据：栈追踪、失败测试、git 历史
- 调试时精度最高的信号
- 只有存在此类信号时才有用

示例——checkout 崩溃报告

1. 读取信号
   - `stack trace: cart.ts:88`
   - 命名了 3 个帧
2. 打开那些帧
   - `read tax.ts:20-60`
   - `applyTax` 中的舍入
3. 打补丁 + 重跑
   - `pytest tests/tax.py`
   - 通过，全程未使用搜索

## 第 13 页

**工具：搜索与读取——语言服务器（LSP）**

- 查询编译器索引：定义、引用、符号、类型
- 解析 import、重载和重命名，而 grep 只能猜测
- 成本：每种语言一个实时 server；冷启动慢

示例——把 `charge()` 重命名为 `capture()`

1. 查找引用
   - `textDocument/references`
   - 42 个调用点，7 个文件
2. 重命名符号
   - `textDocument/rename`
   - 包含别名 import
3. 验证
   - type check
   - 无未解析符号

## 第 14 页

**搜索与读取：对比**

| 方法 | 通过什么找到代码 | 最适合 | 主要成本 |
| --- | --- | --- | --- |
| glob / grep | 字面名称与路径 | 名称已知或可猜 | 每次搜索消耗轮次与上下文 |
| 语义索引 | 嵌入块的含义 | 措辞与代码不匹配 | 建立并重新同步索引 |
| 外部信号 | 追踪、失败测试、git 历史 | 已有报告指向代码 | 只对部分任务存在 |
| 语言服务器 | 编译器符号图 | 编辑必须跟随引用 | 每种语言一个实时 server |

实践中——从 grep 开始；名称用尽时再求助索引或 LSP。

## 第 15 页

**搜索与读取：对比**

| 方法 | 通过什么找到代码 | 最适合 | 主要成本 |
| --- | --- | --- | --- |
| glob / grep | 字面名称与路径 | 名称已知或可猜 | 每次搜索消耗轮次与上下文 |
| 语义索引 | 嵌入块的含义 | 措辞与代码不匹配 | 建立并重新同步索引 |
| 外部信号 | 追踪、失败测试、git 历史 | 已有报告指向代码 | 只对部分任务存在 |
| 语言服务器 | 编译器符号图 | 编辑必须跟随引用 | 每种语言一个实时 server |

实践中——从 grep 开始；名称用尽时再求助索引或 LSP。

## 第 16 页

**智能体应如何编辑代码？**

举手 = 得分

## 第 17 页

**工具：编辑——整文件重写**

- 模型重新生成整个文件；工具覆盖它
- 没有可能写错的补丁语法——每次编辑都能干净应用
- 成本：输出随文件大小增长；未改动的代码可能漂移

示例——给 API client 添加重试

1. 读取文件
   - `read client.ts`
   - 120 行进入上下文
2. 重新生成
   - `write client.ts`
   - 整个文件，改动 4 行
3. 结果
   - `diff` vs previous
   - 第一次就应用成功

## 第 18 页

**工具：编辑——统一 diff / patch**

- 模型发出补丁；单独的工具应用它
- 紧凑、可审查、人类和 CI 已在使用的格式
- 成本：行号或上下文漂移时 hunk 会失败

示例——在两个文件中提高重试上限

1. 读取锚点
   - `read client.ts, api.ts`
   - 手中有行号
2. 发出补丁
   - `@@ -41,3 +41,3 @@`
   - 6 行，两个 hunk
3. 应用
   - `git apply patch.diff`
   - 两个 hunk 都应用成功

## 第 19 页

**工具：编辑——搜索替换**

- 模型发出精确锚点字符串及其替换内容
- 输出与改动量成正比，而非文件大小
- 成本：锚点有歧义、过时或空白不匹配时失败

示例——提高重试次数

1. 定位锚点
   - `grep -n "retries = 3"`
   - 唯一匹配
2. 替换块
   - `retries = 3` → `5`
   - 一次调用，无需重写
3. 验证
   - 读回该块
   - 文件其余部分未动

## 第 20 页

**工具：编辑——结构化 / AST 编辑**

- 模型命名对某个符号的操作：重命名、添加参数
- 不受格式影响；不会产生非法语法
- 成本：每种语言需要工具；可表达的编辑集合有限

抽象语法树（AST）　https://www.youtube.com/watch?v=lCrC-qojPpU

https://pierce.dev/notes/how-language-servers-work

示例——给 `fetchUser()` 添加 timeout 参数

1. 命名操作
   - `add_param(fetchUser)`
   - timeout，默认 5s
2. 工具应用它
   - 重写签名和所有 18 个调用者
3. 验证
   - parse + type check
   - 构造上即合法

## 第 21 页

**智能体如何应用编辑**

- Token 成本
- 鲁棒性——编辑是否落到它该落的地方？
- 整文件重写：长文件会漂移
- 统一 diff：过时行会失效
- 搜索 / 替换块：需要精确、唯一匹配
- 结构化 / AST 编辑：语言覆盖有限

举手 = 得分

## 第 22 页

**工具执行：本质上是一个 shell**

最强大也最危险的工具。

- 组合——一次调用可以串联、过滤、循环和重试
- 触达——文件系统、网络、包管理器、已安装二进制
- 持久性——文件和进程比单次调用活得更久
- 影响范围——shell 能做什么，智能体就能做什么

## 第 23 页

**工具执行：你必须考虑的事项**

- 失败信号——智能体真正能据此行动的 error
- 输出——足够但不要太多
- 持续时间——长时运行与后台进程
- 预算——何时停止重试并交回
- 隔离——代码在哪里运行，能触达什么

## 第 24 页

**另外五个常用工具**

A. 记忆与笔记——把发现写入文件；计划可存活于 compaction
B. 子智能体与委派——探索返回候选清单，而不是 40 次文件读取
C. Web 搜索与抓取——先读已安装的源码，再上网
D. 浏览器与视觉反馈——对渲染结果截图并反馈回去
E. 询问用户——一个廉价问题胜过一次自信的错误补丁

## 第 25 页

**工具设计最佳实践**

- **少而正交的工具**：重叠的工具会让模型犹豫不决。
- **专用而非通用**：`search_orders(customer_id)` 胜过裸的 `run_sql` 工具。
- **Token 廉价的输出**：截断、分页、摘要（工具设计就是上下文设计）。
- **能教学的错误**：返回修复提示，而不只是“invalid argument”。
- **默认幂等**：尽可能安全重试。

## 第 26 页

**我们能只提供 shell 工具吗？**

在做作业时自己找答案！

- 无专用编辑器：10.3%
- 仅 shell：11.0%
- 整文件视图：12.7%
- 完整交互历史：15.0%
- 专门构建的 SWE-agent……：18.0%

在 GPT-4 上不成立

## 第 27 页

**上下文管理**

Prompt 工程

上下文工程

## 第 28 页

**从 prompt 到智能体系统**

- **2023–2024　Prompt Engineering**
  - “我们应该如何指示模型？”
  - 措辞、示例、输出格式
- **2025–2026　Context Engineering**
  - “模型应该看到什么？”
  - 检索、记忆、历史、压缩
- **2026　Harness Engineering**
  - “智能体应该如何运作？”
  - 循环、工具、沙箱、重试、停止
- **Now -> Next　Goal Engineering**
  - “什么算成功？”
  - 目标、标准、约束、权衡

人们喜欢造词。我使用它们，是为了让你遇到时知道它们是什么意思，但这不代表我同意或喜欢它们。

## 第 29 页

**Prompt 工程**

- Zero-shot
- Few-shot
- Role & persona
- Chain-of-thought
- Tree-of-thoughts
- Self-consistency
- Prompt chaining
- Meta prompting

## 第 30 页

**Zero-Shot Prompting：只有指令**

示例：

```
你是一名支持工单分诊助手。
把工单分类为：
billing | bug | feature | other
只回复 JSON：{"label": ...}
如果不清楚，使用 "other"。
工单：“导出 PDF 时崩溃。”
→ {"label": "bug"}
```

只有指令

**何时使用**

- 任务常见且众所周知
- 格式可以用文字说明

**何时换方法**

- 规则是隐性的 → few-shot

## 第 31 页

**Few-Shot Prompting：指令 + 示例**

示例：

```
分类工单。只回复 JSON。
“这个月被扣了两次费。”
→ {"label": "billing"}
“能加个深色模式吗？”
→ {"label": "feature"}
“asdfgh”
→ {"label": "other"}
“导出 PDF 时崩溃。”
→  ?
```

指令加上少量示范示例。

**何时使用**

- 输出形态不寻常
- 规则更容易展示而非说明

**何时换方法**

- 任务需要步骤 → chain-of-thought

## 第 32 页

**Role & Persona Prompting：赋予角色**

用角色引导行为。

**何时使用**

- 语气或判断很重要
- 受众很特定

**何时换方法**

- 需要步骤 → chain-of-thought

示例：

```
你是一位资深 SRE，正在为高管读者审查一份 postmortem。
标出证据缺口；绝不推测。
直接：最多五条。
→ “时间线遗漏了 04:12 告警确认——这是证据缺口，不是原因。”
```

## 第 33 页

**Chain-of-Thought：让步骤显式**

示例：

```
用编号步骤推演，然后以：ANSWER: <value> 结尾
Q: 前 4 周每周 3 个功能，之后 2 周每周 5 个。总数？
1. 3 × 4 = 12
2. 5 × 2 = 10
3. 12 + 10 = 22
ANSWER: 22
```

先推理步骤，最后给答案。

**何时使用**

- 任务确实有步骤
- 错误来自跳过了工作

**何时换方法**

- 存在多条路径 → tree-of-thought

## 第 34 页

**Tree-of-Thought：分支、打分、剪枝**

分支、打分、剪枝各条路径。

**何时使用**

- 多条路线都合理
- 你能廉价地给它们打分

**何时换方法**

- 只有一个正确答案 → self-consistency

示例：

```
提出 3 种降低 checkout 延迟的方法。按影响和投入各打 1–5 分，然后扩展最好的。
A 缓存预热      impact 3 effort 2
B 去掉第三方    impact 5 effort 4
C 懒加载资源    impact 4 effort 1
扩展 C，然后 B。剪掉 A。
```

## 第 35 页

**Self-Consistency：采样，然后投票**

多次采样，多数投票。

**何时使用**

- 存在一个正确答案
- 错误判断代价高昂

**何时换方法**

- 阶段可分离 → chaining

示例：

```
同一 prompt，5 个样本，T = 0.7
“这张发票是重复的吗？”
yes | yes | no | yes | yes
→ 多数：yes  (4/5 = 0.8)
阈值 0.8 → 回答。
如果是 3/5，转人工。
```

## 第 36 页

**Prompt Chaining：一次调用一个任务**

示例：

```
Stage 1  提取
  in: 邮件文本
  out: {vendor, amount, date}
Stage 2  校验 + 丰富
  out: {..., vendor_id}
Stage 3  起草回复
  out: {subject, body}
```

失败 schema → 只重试该阶段

一次调用一个任务，校验交接。

**何时使用**

- 工作可拆成阶段
- 你能校验每个输出

**何时换方法**

- 要调 prompt 本身 → meta prompting

## 第 37 页

**Meta Prompting：让模型写 prompt**

示例：

```
这是我的 prompt、10 个测试用例，以及它失败的 3 个。
重写 prompt，修好这 3 个，同时不破坏另外 7 个。
只返回新 prompt。
→ v2 增加了一条显式拒绝规则
   8/10 → 10/10 在评估集上
```

模型重写自己的 prompt。

**何时使用**

- 你有评估集可打分
- 你要调的就是 prompt

**何时换方法**

- 收益停滞 → 重新审视你的选择

## 第 38 页

**选择正确的技术**

**从简单开始**

- Zero-shot——任何常见任务的基线
- Few-shot——输出形态不寻常或规则隐性
- Role & persona——语气或判断重要

**加入推理**

- Chain-of-thought——任务需要多步推理
- Tree-of-thought——多条路径值得打分
- Self-consistency——多问几次，取多数票

**工程化系统**

- Prompt chaining——阶段可分离，交接可校验
- Meta prompting——prompt 本身就是工件

## 第 39 页

**有些技术已经过期**

- 在做作业时自己发现！

举手 = 得分

## 第 40 页

**设计 prompt：四条最佳实践**

EXAMPLE PROMPT

```
### Instruction ###
把下面文本翻译成西班牙语：
Text: "hello!"
```

MODEL OUTPUT

```
¡Hola!
```

Instruction、分隔符、数据——按这个顺序。

1. 从简单开始，再迭代
   - 只在需要时添加上下文
2. 划分区块
   - 上下文、指令、工具、输出规范
3. 具体且简洁
   - 聪明的措辞什么也换不来
4. 把大任务拆成子任务
   - 不要前置全部复杂度

Prompt 建议是模型特定的——每次换模型都要重新调。

## 第 41 页

**上下文工程**

上下文工程是“把恰好正确的信息填入上下文窗口，以供下一步使用”的精细艺术与科学。

——Andrej Karpathy

Karpathy, X (2025)——x.com/karpathy/status/1937902205765607626

## 第 42 页

**上下文是有限资源**

- **成本**
  - 每一步都重新发送整个窗口。
  - → 每一轮都再次付费
- **延迟**
  - 更大的 prompt 预填充和解码更慢。
  - → 每一轮循环都更慢
- **注意力**
  - 随着窗口填满，召回会衰减；中间部分会被漏掉。
  - → 更多上下文不等于更好的答案

举手 = 得分

## 第 43 页

**长度和位置都会损害准确率**

准确率随输入增长而衰减，也取决于答案位于窗口中的什么位置。

- 简单查找：73%（输入增长后下降）
- 有干扰项：46% → 40%
- 答案位置（20 份文档中）：
  - 第 1 位：76%
  - 第 5 位：61%
  - 第 10 位：55%
  - 第 15 位：59%
  - 第 20 位：71%

Context Rot (Chroma)；Liu et al., “Lost in the Middle,” TACL 12 (2024)

## 第 44 页

**上下文窗口的解剖**

- 系统 prompt（约 2K）
  - 角色、规则、输出契约——静态，始终驻留
- 工具定义（约 6K）
  - 每个 schema 都消耗 token，无论是否使用
- 检索上下文（约 25K）
  - 按需拉入的文件、搜索命中、文档
- 项目环境（约 8K）
  - 刻意读回的草稿和笔记
- 消息历史（约 80K 且持续增长）
  - 轮次加上原始工具输出——增长最快
- 为模型自身回复预留的 tokens

上下文变得太大时该怎么办？

举手 = 得分

（单次智能体轮次的示意性 token 预算）

## 第 45 页

**管理上下文窗口**

Admission　Offloading　Transformation　Compaction

预防性且无损　→　有损且不可逆

## 第 46 页

**准入：把守进入上下文窗口的内容**

- 定向检索
  - 窄查询；取字段，不取整篇文档
- 工具输出整形
  - 丢掉 DOM，保留提取结果
- 截断
  - 只在整形无效时限制大小
- 隔离
  - 把原始负载交给子智能体

Before：原始 DOM 直接传入——48,000 tokens

After：只有价格和标题——900 tokens

小了 98%，答案相同

举手 = 得分

## 第 47 页

**卸载：不到需要时不加载**

保持可检索，而非常驻。

- 渐进式工具定义
  - 只在需要时加载 schema
- 工具搜索
  - 保留索引；按需获取
- 工具输出卸载
  - 返回句柄，按需加载
- 外部化任务列表
  - 把计划放在磁盘上
- 持久记忆
  - 把笔记写出；保留一个小索引

Before：60 个 schema 常驻——42,000 tokens

After：索引 + 3 个 schema——3,100 tokens

小了 93%，60 个全部可达

举手 = 得分

## 第 48 页

**变换：有选择地丢弃历史**

- 去重
  - 只保留每个对象的最新状态
- 观察掩蔽
  - 剥离超过 N 步的工具结果
- 滑动窗口
  - 只保留最近轮次和头部

Before：每个结果都保留——96,000 tokens

After：只保留最新状态——24,000 tokens

小了 75%，没有做任何摘要

举手 = 得分

## 第 49 页

**压缩：LLM 作为最后手段**

- 滚动摘要
  - 边进行边总结旧工具结果
- 完整摘要
  - 达到上限时重写整个历史
- 自动记忆
  - 把关键事实持久化到窗口之外

**警告**

- 为输出预留余量
- 保留系统前缀
- 之后重新注入关键事实

At the limit：历史填满窗口 → LLM compaction → 压缩后：余量恢复

## 第 50 页

**上下文失败的五种方式**

- **Poisoning（污染）**：幻觉进入窗口，之后被当作事实引用
- **Distraction（分心）**：历史增长到智能体模仿自己过去的行为
- **Confusion（混淆）**：无关工具和文档把答案带偏
- **Clash（冲突）**：新信息与旧信息矛盾；两者都未解决
- **Drift（漂移）**：真实目标被掩埋，被附近的子目标替换

Breunig, “How Contexts Fail and How to Fix Them” (2025)

说出失败的名字，修复方法就显而易见了。

## 第 51 页

**智能体 = 模型 × 框架**

模型能力设定上限；框架决定实现出的性能。

## 第 52 页

**改变框架可将准确率提高 2 倍**

| 基准 | 基础框架 | 改进框架 |
| --- | --- | --- |
| SWE-bench Verified | 43 / 169 | 72 / 169 |
| SWE-bench Pro | 31 / 316 | 72 / 316 |

**变化**

- 旧工具输出被压缩
- 最近观察保持可见
- 检测重复和停滞
- 卡住时进行干预

一些表面上的“模型失败”，实际上是上下文和控制循环的失败。

Lewis, S., “Same Model, Different Harness: Different Coding-Agent Results” (arXiv:2608.26218, 2026)

## 第 53 页

**智能体 = 模型 × 框架**

在作业中亲自实验。

智能体循环、prompt、工具、上下文管理、失败处理都很重要！

## 第 54 页

**下一节课**

- 智能体设计 II
- 智能体（持久）记忆
- 成本高效的智能体
- 安全与保障
- 多智能体设计

## 第 55 页

**延伸阅读**

## 第 56 页

**超越 ReAct 循环**

- **ReAct**：每一步都循环
  - Thought → Act → Observe
- **Reflexion**：失败后循环
  - Attempt → Evaluate → Critique → Retry
- **Plan-and-execute**：偏离时循环
  - Plan → Execute steps → Re-plan
- **Tree search**：没有循环——一次宽扫描
  - State → Branch A · B · C → Keep best
  - 并行探索分支——只有一个存活

图例：模型调用 / 应用 / 工具动作 / 被选中的结果
