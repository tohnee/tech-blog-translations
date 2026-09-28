---
title: "MemGPT：迈向作为操作系统的大语言模型"
title_en: "MemGPT: Towards LLMs as Operating Systems"
arxiv: 2310.08560
source: https://arxiv.org/abs/2310.08560
crawled: 2026-09-23
translated: 2026-09-23
---

# MemGPT：迈向作为操作系统的大语言模型

> 原文：[MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560) · Stanford CS329A 指定阅读

Charles Packer（加州大学伯克利分校；通讯作者：[cpacker@berkeley.edu](mailto:cpacker@berkeley.edu)）
Sarah Wooders（加州大学伯克利分校）
Kevin Lin（加州大学伯克利分校）
Vivian Fang（加州大学伯克利分校）
Shishir G. Patil（加州大学伯克利分校）
Ion Stoica（加州大学伯克利分校）
Joseph E. Gonzalez（加州大学伯克利分校）

###### 摘要

大型语言模型（LLM）已经彻底改变了 AI，但受限于有限的上下文窗口，这阻碍了它们在 extended conversation（长程对话）和文档分析等任务中的效用。为了能够使用超出有限上下文窗口的上下文，我们提出虚拟上下文管理（virtual context management），这一技术的灵感来自传统操作系统中的分层存储体系——后者通过在物理内存与磁盘之间的分页（paging），提供了更大虚拟内存的假象。
利用这一技术，我们推出了 MemGPT（MemoryGPT），一个智能管理不同存储层级的系统，从而在 LLM 有限的上下文窗口内有效提供扩展上下文。
我们在两个现代 LLM 的有限上下文窗口严重拖累其表现的领域评估了这一受操作系统启发的设计：文档分析——MemGPT 能够分析远超底层 LLM 上下文窗口的大型文档；以及多会话聊天——MemGPT 可以创建通过与用户的长期互动来记忆、反思并动态演化的对话智能体。
我们在 <https://research.memgpt.ai> 发布了实验所用的 MemGPT 代码和数据。

###### 关键词：

Machine Learning, ICML

## 1 引言

近年来，大型语言模型（LLM）及其底层 transformer 架构（Vaswani et al., 2017；Devlin et al., 2018；Brown et al., 2020；Ouyang et al., 2022）已成为对话式 AI 的基石，并催生了大量消费级与企业级应用。尽管有这些进展，LLM 所使用的有限固定长度上下文窗口显著阻碍了它们在长对话或长文档推理中的适用性。
例如，使用最广泛的开源 LLM 只能支持几十条来回消息，或在超出最大输入长度之前（Touvron et al., 2023）对一篇短文档进行推理。

直接延长 transformer 的上下文长度会因 transformer 架构的自注意力机制而导致计算时间和内存成本的二次方增长，这使得设计新的长上下文架构成为一个紧迫的研究挑战（Dai et al., 2019；Kitaev et al., 2020；Beltagy et al., 2020）。
虽然开发更长的模型是一个活跃的研究方向（Dong et al., 2023），
但即使我们能够克服上下文扩展的计算挑战，近期研究表明长上下文模型难以有效利用额外的上下文（Liu et al., 2023a）。
因此，鉴于训练最先进 LLM 所需的巨大资源以及上下文扩展的收益递减，亟需支持长上下文的替代技术。

本文研究如何在继续使用固定上下文模型的同时提供无限上下文的假象。
我们的方法借鉴了虚拟内存分页的思想——该思想最初是为了让应用程序能够处理远超可用内存的数据集，通过在主存与磁盘之间分页移动数据而发展起来。
我们利用 LLM 智能体函数调用能力的最新进展（Schick et al., 2023；Liu et al., 2023b）设计了 MemGPT，一个受操作系统启发的虚拟上下文管理 LLM 系统。
借助函数调用，LLM 智能体可以读写外部数据源、修改自身的上下文，并选择何时向用户返回响应。

这些能力使 LLM 能够在上下文窗口（类似操作系统中的「主存」）与外部存储之间有效地将信息「换入换出」（page in and out），类似于传统操作系统中的分层存储。
此外，函数调用还可用于管理上下文管理、响应生成与用户交互之间的控制流。这使智能体可以选择为单个任务迭代地修改其上下文中的内容，从而更有效地利用其有限上下文。

在 MemGPT 中，我们将上下文窗口视为一种受限的内存资源，并为 LLM 设计了一个类似于传统操作系统中存储层级（memory tier）的存储层次结构（Patterson et al., 1988）。
传统操作系统中的应用程序与虚拟内存交互，后者通过操作系统将溢出数据分页到磁盘、并在应用程序访问时（经由缺页）将数据取回内存，从而提供了比物理（即主）内存实际可用资源更多的假象。
为了提供类似的更长上下文长度的假象（类似虚拟内存），我们允许 LLM 通过一个「LLM 操作系统」——我们称之为 MemGPT——来管理其自身上下文（类似物理内存）中放置的内容。MemGPT 使 LLM 能够检索其上下文中所缺失的相关历史数据，也能将相关性较低的数据从上下文中驱逐到外部存储系统。
图 3 展示了 MemGPT 的各组件。

![Refer to caption](2310.08560v2/memgpt_diagrams_wide_memory_creation.png)

图 1：
MemGPT（左侧）在收到关于上下文空间有限的系统警报后，将数据写入持久记忆。

存储层次、操作系统函数与基于事件的控制流的组合使用，使 MemGPT 能够用具有有限上下文窗口的 LLM 处理无界上下文。
为展示这一新的受操作系统启发的 LLM 系统的效用，我们在两个现有 LLM 表现因有限上下文而严重受限的领域评估 MemGPT：文档分析——标准文本文件的长度可能迅速超过现代 LLM 的输入容量；以及对话智能体——受有限对话窗口约束的 LLM 在 extended conversation 中缺乏上下文感知、人设一致性和长期记忆。
在这两个场景中，MemGPT 都能克服有限上下文的限制，胜过现有的基于 LLM 的方法。

![Refer to caption](2310.08560v2/memgpt_diagrams_wide_memory_search.png)

图 2：
MemGPT（左侧）可以搜索上下文之外的数据，把相关信息带入当前上下文窗口。

图 3：
在 MemGPT 中，固定上下文的 LLM 处理器配备了一个分层存储系统以及让它管理自身存储的函数。
LLM 的提示 token（输入），即*主上下文*（main context），由系统指令、工作上下文和一个 FIFO 队列组成。
LLM 的补全 token（输出）由函数执行器解释为函数调用。
MemGPT 使用函数在主上下文与*外部上下文*（归档存储和召回存储数据库）之间移动数据。
LLM 可以通过在其输出中生成一个特殊的关键字参数（request_heartbeat=true）来请求立即进行后续 LLM 推理，从而将函数调用串联起来；函数链式调用正是 MemGPT 能够执行多步检索以回答用户查询的原因。

## 2 MemGPT（MemoryGPT）

MemGPT 受操作系统启发的多级存储架构区分两种主要存储类型：主上下文（类似主存/物理内存/RAM）和外部上下文（类似磁盘内存/磁盘存储）。
主上下文由 LLM 的*提示 token* 构成——主上下文中的任何内容都被视为*在上下文中*（in-context），可被 LLM 处理器在推理期间访问。
外部上下文指保存在 LLM 固定上下文窗口之外的任何信息。
这些*上下文之外*（out-of-context）的数据必须始终被显式移入主上下文，才能在推理期间传递给 LLM 处理器。
MemGPT 提供函数调用，让 LLM 处理器无需任何用户干预即可管理自身的存储。

### 2.1 主上下文（提示 token）

MemGPT 中的提示 token 分为三个连续区段：系统指令、工作上下文和 FIFO 队列。系统指令是只读（静态）的，包含关于 MemGPT 控制流的信息、不同存储级别的预期用途，以及如何使用 MemGPT 函数的指令（例如如何检索上下文之外的数据）。工作上下文是一个固定大小的非结构化文本读写块，只能通过 MemGPT 函数调用写入。在对话场景中，工作上下文用于存储关于用户及智能体所扮演人设的关键事实、偏好和其他重要信息，使智能体能够与用户流畅交谈。
FIFO 队列保存滚动的消息历史，包括智能体与用户之间的消息，以及系统消息（例如存储警告）和函数调用的输入与输出。FIFO 队列的第一个位置存储一条系统消息，包含已被逐出队列消息的递归摘要。

### 2.2 队列管理器

队列管理器管理召回存储和 FIFO 队列中的消息。当系统收到一条新消息时，队列管理器将到来的消息追加到 FIFO 队列，拼接提示 token 并触发 LLM 推理以生成 LLM 输出（补全 token）。队列管理器将到来的消息和生成的 LLM 输出都写入召回存储（MemGPT 消息数据库）。当召回存储中的消息通过 MemGPT 函数调用被检索时，队列管理器将它们追加到队列末尾，重新插入 LLM 的上下文窗口。

队列管理器还负责通过队列驱逐策略控制上下文溢出。当提示 token 超过底层 LLM 上下文窗口的「警告 token 数」（例如上下文窗口的 70%）时，队列管理器向队列中插入一条系统消息，警告 LLM 即将发生队列驱逐（「存储压力」警告），以允许 LLM 使用 MemGPT 函数将 FIFO 队列中包含的重要信息保存到工作上下文或归档存储（一个存储任意长度文本对象的读写数据库）。当提示 token 超过「刷新 token 数」（例如上下文窗口的 100%）时，队列管理器刷新队列以释放上下文窗口中的空间：队列管理器驱逐一定数量的消息（例如上下文窗口的 50%），并使用现有的递归摘要和被驱逐的消息生成新的递归摘要。队列一旦刷新，被驱逐的消息就不再处于上下文中、也不再对 LLM 直接可见，但它们被无限期保存在召回存储中，可通过 MemGPT 函数调用读取。

### 2.3 函数执行器（处理补全 token）

MemGPT 通过由 LLM 处理器生成的函数调用来编排主上下文与外部上下文之间的数据移动。
存储编辑与检索完全自主：MemGPT 基于当前上下文自主更新并搜索自身的存储。
例如，
它可以
决定何时在上下文之间移动内容（例如当对话历史变得太长时，如图 1 所示），并修改其主上下文，以更好地反映其对当前目标与职责的不断演进的理解（如图 3 所示）。
我们通过在系统指令中提供明确的指引来实现自主编辑与检索，这些指引指导 LLM 如何与 MemGPT 存储系统交互。这些指令包含两个主要部分：(1) 对存储层次结构及其各自用途的详细描述；(2) 系统可用来访问或修改其存储的函数模式（schema）（附带其自然语言描述）。

在每个推理周期中，LLM 处理器以主上下文（拼接为单个字符串）为输入，生成一个输出字符串。
该输出字符串由 MemGPT 解析以确保正确性，如果解析器验证了函数参数，函数即被执行。
结果（包括发生的任何运行时错误，例如在主上下文已达最大容量时仍试图向其添加内容）随后由 MemGPT 反馈给处理器。这一反馈回路使系统能够从其行动中学习并相应调整行为。
对上下文限制的感知是让自主编辑机制有效运作的关键方面；为此，MemGPT 会以关于 token 限制的警告提示处理器，以指导其存储管理决策。
此外，我们的存储检索机制被设计为感知这些 token 约束，并实现了分页，以防止检索调用溢出上下文窗口。

表 1：
常用模型与 LLM API 的上下文长度比较（数据收集于 2024 年 1 月）。
*消息数为近似值，假设前置提示为 1k token、平均每条消息约 50 token（约 250 字符）。「开放」指模型为开源或开放权重（与之相对的是仅通过 API 提供）。

|  |  |  |  |
| --- | --- | --- | --- |
|  |  | 上下文窗口 | |
| 模型 / API 名称 | 开放？ | Token 数 | *消息数 |
| Llama (1) | ✓ | 2k | 20 |
| Llama 2 | ✓ | 4k | 60 |
| GPT-3.5 Turbo（发布时） | ✗ | 4k | 60 |
| Mistral 7B | ✓ | 8k | 140 |
| GPT-4（发布时） | ✗ | 8k | 140 |
| GPT-3.5 Turbo | ✗ | 16k | 300 |
| GPT-4 | ✗ | 32k | ~600 |
| Claude 2 | ✗ | 100k | ~2000 |
| GPT-4 Turbo | ✗ | 128k | ~2600 |
| Yi-34B-200k | ✓ | 200k | ~4000 |

### 2.4 控制流与函数链式调用

在 MemGPT 中，*事件*（event）触发 LLM 推理：事件是 MemGPT 的广义化输入，可以是用户消息（聊天应用中）、系统消息（例如主上下文容量警告）、用户交互（例如某用户刚刚登录的提醒，或他们完成文档上传的提醒），以及按固定日程运行的定时事件（允许 MemGPT 在没有用户干预的情况下「未被提示」地运行）。
MemGPT 用解析器处理事件，将其转换为可追加到主上下文的纯文本消息，并最终作为输入送入 LLM 处理器。

许多实际任务需要按顺序调用多个函数，例如，在单次查询的结果中浏览多页，或把来自不同查询、不同文档的数据整理到主上下文中。
函数链式调用允许 MemGPT 在把控制权交还给用户之前顺序执行多个函数调用。
在 MemGPT 中，函数可以带一个特殊标志被调用，请求在所请求的函数执行完毕后立即将控制权交还给处理器。
如果该标志存在，MemGPT 会将函数输出加入主上下文并（继续执行而不是暂停处理器执行）。
如果该标志不存在（一次 *yield*），MemGPT 将不会运行 LLM 处理器，直到下一个外部事件触发（例如用户消息或计划中断）。

![Refer to caption](2310.08560v2/memgpt_diagrams_wide_memory_correction.png)

图 4：
一段示例对话片段，其中 MemGPT（左侧）更新已存储的信息。此处信息存储在工作上下文存储中（位于提示 token 内）。

## 3 实验

我们在两个长上下文领域评估 MemGPT：对话智能体和文档分析。对于对话智能体，我们扩展了现有的 Multi-Session Chat 数据集（Xu et al., 2021），并引入两个新的对话任务来评估智能体在长对话中保留知识的能力。对于文档分析，我们在 Liu et al. (2023a) 的现有任务上对 MemGPT 进行基准测试，包括长文档上的问答和键值检索。我们还提出一个新的嵌套键值检索任务，需要跨多个数据源整理信息，测试智能体从多个数据源整理信息（多跳检索）的能力。我们公开发布了增强的 MSC 数据集、嵌套 KV 检索数据集，以及 2000 万篇维基百科文章的嵌入数据集，以便利未来研究。我们的基准测试代码可在 <https://research.memgpt.ai> 获取。

实现细节。当讨论 OpenAI 模型时，除非另有说明，「GPT-4 Turbo」指特定的 gpt-4-1106-preview 模型端点（上下文窗口 128,000），「GPT-4」指 gpt-4-0613（上下文窗口 8,192），「GPT-3.5 Turbo」指 gpt-3.5-turbo-1106（上下文窗口 16,385）。实验中，我们用所有基线模型（GPT-4、GPT-4 Turbo 和 GPT-3.5）运行 MemGPT，以展示底层模型表现如何影响 MemGPT 的表现。

### 3.1 面向对话智能体的 MemGPT

虚拟伴侣和个性化助理等对话智能体旨在与用户进行自然的长期互动，可能跨越数周、数月甚至数年。这给固定长度上下文的模型带来了挑战，因为它们只能引用对话中有限的历史。一个「无限上下文」智能体应当无缝处理连续交流，没有边界或重置。与用户交谈时，这样的智能体必须满足两个关键标准：
(1) 一致性——智能体应保持对话连贯。新提到的事实、偏好和事件应与用户和智能体双方的先前陈述保持一致。
(2) 吸引力——智能体应利用关于用户的长期知识来个性化回复。引用先前的对话使对话更自然、更吸引人。

因此，我们在这两个标准上评估我们提出的系统 MemGPT：
(1) MemGPT 是否利用其存储提升了对话一致性？它能记住过去互动中的相关事实、偏好和事件以保持连贯吗？
(2) MemGPT 是否借助存储产生了更具吸引力的对话？它会自发地融入远期的用户信息来个性化消息吗？
通过在一致性和吸引力上评估，我们可以判定相对于固定上下文基线，MemGPT 处理长期对话交互挑战的能力如何。它满足这些标准的能力将证明无界上下文是否为对话智能体带来实质收益。

表 2：
深度记忆检索（DMR）表现。
在此任务中，智能体被问及一个关于先前对话（会话 1–5）中讨论过的话题的具体问题。
智能体的回答对照金标准答案评分。
MemGPT 显著优于固定上下文基线。

| 模型 | 准确率 ↑ | ROUGE-L (R) ↑ |
| --- | --- | --- |
| GPT-3.5 Turbo | 38.7% | 0.394 |
| ++ MemGPT | 66.9% | 0.629 |
| GPT-4 | 32.1% | 0.296 |
| ++ MemGPT | 92.5% | 0.814 |
| GPT-4 Turbo | 35.3% | 0.359 |
| ++ MemGPT | 93.4% | 0.827 |

数据集。
我们在 Xu et al. (2021) 提出的 Multi-Session Chat（MSC）数据集上评估 MemGPT 和我们的固定上下文基线。该数据集包含由人类标注者生成的多会话聊天记录，每位标注者被要求在所有会话期间扮演一个一致的人设。MSC 中的每段多会话聊天总共有五个会话，每个会话大约包含十余条消息。
作为一致性实验的一部分，我们创建了一个新会话（会话 6），其中包含同样两个人设之间的一组问答。

#### 3.1.1 深度记忆检索任务（一致性）。

我们基于 MSC 数据集引入一个新的「深度记忆检索」（DMR）任务，旨在测试对话智能体的一致性。在 DMR 中，用户向对话智能体提出一个明确回指先前对话的问题，且预期答案范围非常窄。我们用一个单独的 LLM 生成 DMR 问答（QA）对，该 LLM 被指示写一个从一位用户发给另一位用户的问题，该问题只有利用过去会话中获得的知识才能正确回答（更多细节见附录）。

我们使用 ROUGE-L 分数（Lin, 2004）和一个「LLM 评审」来评估生成回答相对「金标准回答」的质量，后者被指示评判生成回答是否与金标准回答一致（已证明 GPT-4 与人类评估者有高度一致性（Zheng et al., 2023））。
实践中，我们注意到（MemGPT 和基线的）生成回答通常比金标准回答更冗长。
我们使用 ROUGE-L 召回（R）指标，以考虑生成的智能体回复相对较短金标准答案标签的冗长性。

表 3：
对话开场白表现。
智能体的对话开场白通过与金标准人设标签（SIM-1/3）以及人类创作的开场白（SIM-H）的相似度分数评估。
配合多种底层模型，MemGPT 都能超越人类创作的对话开场白的表现。

| 方法 | ↑ SIM-1 | SIM-3 | SIM-H |
| --- | --- | --- | --- |
| 人类 | 0.800 | 0.800 | 1.000 |
| GPT-3.5 Turbo | 0.830 | 0.812 | 0.817 |
| GPT-4 | 0.868 | 0.843 | 0.773 |
| GPT-4 Turbo | 0.857 | 0.828 | 0.767 |

MemGPT 利用存储保持连贯：
表 2 展示了 MemGPT 与固定存储基线的表现。
我们比较使用不同底层 LLM 的 MemGPT，并以不使用 MemGPT 的基座 LLM 作为基线进行比较。
基线可以看到过去五段对话的有损摘要，以模拟一个扩展的递归摘要流程，而 MemGPT 则可以访问完整对话历史，但必须通过分页搜索查询来检索记忆（以将其带入主上下文）。
在此任务中，我们看到 MemGPT 明显提升了底层基座 LLM 的表现：从 MemGPT 换到对应的 LLM 基线时，准确率和 ROUGE 分数都明显下降。

#### 3.1.2 对话开场白任务（吸引力）。

在「对话开场白」任务中，我们评估智能体利用先前对话中积累的知识，为用户打造有吸引力的消息的能力。
为了用 MSC 数据集评估对话开场白的「吸引力」，我们将生成的开场白与金标准人设进行比较：一个有吸引力的开场白应利用人设中包含的一（或多）个数据点，而 MSC 中的人设实际上总结了此前所有会话积累的知识。
我们还与人类生成的金标准开场白（即下一个会话中的第一条回复）进行比较。
我们在表 3 中报告 MemGPT 开场白的 CSIM 分数。
我们测试了使用不同基座 LLM 的若干 MemGPT 变体。

图 5：
文档问答任务表现。
MemGPT 的表现不受上下文长度增加的影响。截断（truncation）等方法可以延长 GPT-4 等固定长度模型的有效上下文长度，但随着所需压缩量的增大，这类压缩方法会导致性能退化。在此任务上，用 GPT-4 和 GPT-4 Turbo 运行 MemGPT 的结果相当。

MemGPT 利用存储提升吸引力：
如表 3 所示，MemGPT 能够打造出与手写人类开场白表现相近、且偶尔更胜一筹的有吸引力开场白。
我们观察到，MemGPT 倾向于打造比人类基线更冗长、覆盖人设信息更多方面的开场白。
此外，我们可以看到，在工作上下文中存储信息是生成有吸引力开场白的关键。

### 3.2 面向文档分析的 MemGPT

文档分析同样因当今 transformer 模型有限的上下文窗口而面临挑战。如表 1 所示，开源和闭源模型都受限于上下文长度（OpenAI 的模型至多 128k token）。然而许多文档轻松超过这些长度；例如，年报（SEC Form 10-K）等法律或金融文档可以轻松突破百万 token 大关。此外，许多真实的文档分析任务需要跨多份此类长文档建立联系。预见这些场景，很难把盲目扩大上下文设想为固定上下文问题的解决方案。近期研究（Liu et al., 2023a）也对单纯扩大上下文的效用提出质疑，因为他们发现大上下文模型中的注意力分布不均（模型更容易回忆起其上下文窗口开头或结尾的信息，而非中间的 token）。为了实现跨文档推理，需要像 MemGPT 这样更灵活的存储架构。

图 6：
MemGPT（左侧）解决文档问答任务的一个示例。一个维基百科文档数据库被上传到归档存储。MemGPT 通过函数调用查询归档存储，将分页的搜索结果拉入主上下文。

#### 3.2.1 多文档问答。

为评估 MemGPT 分析文档的能力，我们在 Liu et al. (2023a) 的检索器-阅读器（retriever-reader）文档问答任务上将 MemGPT 与固定上下文基线进行基准比较。
在此任务中，从 NaturalQuestions-Open 数据集中选择一个问题，检索器为该问题选择相关的维基百科文档。阅读器模型（即 LLM）随后以这些文档为输入，并被要求使用所提供的文档回答问题。
与 Liu et al. (2023a) 类似，
我们随着检索文档数量 $K$ 的增加评估阅读器的准确率。

在我们的评估设置中，固定上下文基线和 MemGPT 使用相同的检索器，该检索器基于 OpenAI 的 text-embedding-ada-002 嵌入、用相似度搜索（余弦距离）选出 top-$K$ 文档。我们使用 MemGPT 的默认存储设置：归档存储用 PostgreSQL，并通过 pgvector 扩展启用向量搜索。我们预先计算嵌入并载入数据库，数据库使用 HNSW 索引以实现亚秒级的近似查询时间。
在 MemGPT 中，整个嵌入文档集被载入归档存储，检索器经由归档存储搜索功能（基于余弦相似度执行向量搜索）自然涌现。
在固定上下文基线中，top-$K$ 文档由检索器独立于 LLM 推理获取，与 Liu et al. (2023a) 的原始检索器-阅读器设置类似。

我们沿用 NaturalQuestions-Open 先前工作（Izacard & Grave, 2020；Izacard et al., 2021）的做法，使用 2018 年末的维基百科转储，并抽样 50 个问题用于评估。抽样的问题和嵌入的维基百科段落均已公开发布。我们用 LLM 评审评估 MemGPT 和基线的表现，以确保答案确实来自检索到的文档，并避免非精确字符串匹配被判为错误。

文档问答任务的结果见图 5。固定上下文基线的表现大致以检索器的表现为上限，因为它们使用的是呈现在其上下文窗口中的信息（例如，如果嵌入搜索检索器未能用所给问题浮现金标准文章，固定上下文基线就永远不会看到金标准文章）。
相比之下，MemGPT 能够通过查询归档存储有效地对检索器进行多次调用，从而扩展到更大的有效上下文长度。
MemGPT 主动从其归档存储检索文档（并可以迭代地翻页浏览结果），因此 MemGPT 可用的文档总数不再受限于 LLM 处理器上下文窗口所能容纳的文档数量。

图 7：
嵌套 KV 检索任务表现。
MemGPT 是唯一能在 2 层嵌套之外持续完成嵌套 KV 任务的方法。
虽然 GPT-4 Turbo 作为基线表现更好，但搭载 GPT-4 Turbo 的 MemGPT 表现不如搭载 GPT-4 的 MemGPT。

由于基于嵌入的相似度搜索的局限，文档问答任务对所有方法都颇具挑战。
我们观察到，所选问题的金标准文档（由 NaturalQuestions-Open 标注）经常出现在前十几条检索结果之外，甚至更远。
检索器的表现直接传导到固定上下文基线的结果：GPT-4 在检索文档较少时准确率相对较低，并随着更多文档加入上下文窗口而持续改善，因为它正确地把自己限定为基于检索文档中的信息来回答问题。
虽然理论上 MemGPT 不受次优检索器表现的限制（即使基于嵌入的排序有噪声，只要完整检索器排序中包含金标准文档，通过分页进行足够多次检索器调用仍能找到它），我们观察到 MemGPT 经常在穷尽检索器数据库之前就停止翻页浏览检索结果。

图 8：
MemGPT（左侧）解决嵌套 KV 任务的一个示例（UUID 为便于阅读已缩短）。在这个特定示例中，键值对有两层嵌套：831..ea5 → 5b8..4c3 → f37...617。
当对最终值（f37...617）的查询只返回一个结果、表明它不再是键时，MemGPT 智能体返回最终答案。

为了在默认上下文长度之外评估固定上下文基线与 MemGPT，我们截断检索器返回的文档片段，以便把相同数量的文档装入可用上下文。
如图 5 所示，不出所料，文档截断降低了准确率，因为随着文档收缩，（金标准文档中的）相关片段被遗漏的概率增大。
MemGPT 使用 GPT-3.5 时性能明显退化，原因是其函数调用能力有限，而使用 GPT-4 时表现最佳。

#### 3.2.2 嵌套键值检索（KV）。

我们基于先前工作（Liu et al., 2023a）提出的合成键值（Key-Value）检索引入一个新任务。该任务的目标是展示 MemGPT 如何从多个数据源整理信息。在原始 KV 任务中，作者生成了一个键值对的合成数据集，其中每个键和值都是一个 128 位 UUID（通用唯一标识符）。智能体随后被给定一个键，并被要求返回与该键关联的值。我们创建了 KV 任务的一个版本——*嵌套 KV 检索*，其中值本身也可能是键，从而要求智能体执行多跳查找。
在我们的设置中，我们将 UUID 对的总数固定为 140，大约对应 8k token（我们 GPT-4 基线的上下文长度）。我们将嵌套层级总数从 0（初始键值对的值不是键）变化到 4（即需要总共 4 次 KV 查找才能找到最终值），并抽样 30 种不同的排序配置，包括初始键位置和嵌套键位置。

虽然 GPT-3.5 和 GPT-4 在原始 KV 任务上表现良好，但两者在嵌套 KV 任务中都很挣扎。GPT-3.5 无法完成任务的嵌套变体，性能立即跌落，在 1 层嵌套时准确率即降为 0（我们观察到其主要失败模式是直接返回原始值）。GPT-4 和 GPT-4 Turbo 好于 GPT-3.5，但也出现类似的跌落，在 3 层嵌套时准确率降为 0。另一方面，搭载 GPT-4 的 MemGPT 不受嵌套层数影响，能够通过函数查询反复访问存储在主上下文中的键值对执行嵌套查找。搭载 GPT-4 Turbo 和 GPT-3.5 的 MemGPT 也优于相应的基线模型，但由于未能执行足够的查找，其表现在 2 层嵌套时也开始下滑。
MemGPT 在嵌套 KV 任务上的表现证明了其组合多个查询以执行多跳查找的能力。

## 4 相关工作

长上下文 LLM。
若干工作路线提升了 LLM 的上下文长度。例如，通过稀疏化注意力实现更高效的 transformer 架构（Child et al., 2019；Beltagy et al., 2020）、低秩近似（Wang et al., 2020）以及神经记忆（Lee et al., 2019）。另一条工作路线旨在将上下文窗口扩展到超过其最初训练的长度，如 Press et al. (2021)；Chen et al. (2023)。MemGPT 建立在这些上下文长度的改进之上，因为它们增大了 MemGPT 中主存的容量。我们的主要贡献是一个分层多级存储，它使用长上下文 LLM 作为主存的实现。

检索增强模型。
MemGPT 外部存储的设计建立在大量先前工作之上，这些工作用来自外部检索器的相关输入增强 LLM（Ram et al., 2023；Borgeaud et al., 2022；Karpukhin et al., 2020；Lewis et al., 2020；Guu et al., 2020；Lin et al., 2023）。特别是，Jiang et al. (2023) 提出 FLARE，一种允许 LLM 在生成过程中主动决定何时检索、检索什么的方法。Trivedi et al. (2022) 将检索与思维链推理交织以改进多步问答。

作为智能体的 LLM。
近期工作探索了为 LLM 增加额外能力，使其在交互环境中充当智能体。
Park et al. (2023) 提出为 LLM 添加存储并将 LLM 用作规划器，并在一个多智能体沙盒环境（灵感来自《模拟人生》视频游戏）中观察到涌现的社会行为，智能体可以在其中执行基本活动，如做家务/爱好、去上班以及与其他智能体交谈。
Nakano et al. (2021) 训练模型在回答问题前搜索网页，并在其网页浏览环境中使用与 MemGPT 类似的分页概念来控制底层上下文大小。
Yao et al. (2022) 表明，交织思维链推理（Wei et al., 2022）可以进一步提升交互式 LLM 智能体的规划能力；类似地，在 MemGPT 中，LLM 可以在执行函数时「边想边说」。Liu et al. (2023b) 引入了一套 LLM-as-an-agent 基准，在交互环境（包括电子游戏、思维谜题和网络购物）中评估 LLM。
相比之下，我们的工作专注于解决为智能体配备用户输入的长期记忆这一问题。

## 5 结论

本文介绍了 MemGPT，一个受操作系统启发的、用于管理大语言模型有限上下文窗口的新颖 LLM 系统。通过设计类似传统操作系统的存储层次与控制流，MemGPT 为 LLM 提供了更大上下文资源的假象。这一受操作系统启发的方法在两个现有 LLM 表现受有限上下文长度限制的领域得到了评估：文档分析和对话智能体。在文档分析中，MemGPT 通过在存储中有效地换入换出相关上下文，能够处理远超当前 LLM 上下文限制的长文本。在对话智能体中，MemGPT 使智能体能够在 extended dialogue 中保持长期记忆、一致性和可演化性。总体而言，MemGPT 表明，分层存储管理和中断等操作系统技术即使在固定上下文长度的约束下也能释放 LLM 的潜力。这项工作开辟了众多未来探索的方向，包括将 MemGPT 应用于其他具有海量或无界上下文的领域、集成数据库或缓存等不同的存储层级技术，以及进一步改进控制流和存储管理策略。通过将操作系统架构的概念引入 AI 系统，MemGPT 代表了在 LLM 固有极限内最大化其能力的一个有前景的新方向。

## 参考文献

- Beltagy et al. (2020)

  Iz Beltagy, Matthew E Peters, and Arman Cohan.
  Longformer: The long-document transformer.
  *arXiv preprint arXiv:2004.05150*, 2020.
- Borgeaud et al. (2022)

  Sebastian Borgeaud, Arthur Mensch, Jordan Hoffmann, Trevor Cai, Eliza Rutherford, Katie Millican, George Bm Van Den Driessche, Jean-Baptiste Lespiau, Bogdan Damoc, Aidan Clark, et al.
  Improving language models by retrieving from trillions of tokens.
  In *International conference on machine learning*, pp. 2206–2240. PMLR, 2022.
- Brown et al. (2020)

  Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al.
  Language models are few-shot learners.
  *Advances in neural information processing systems*, 33:1877–1901, 2020.
- Chen et al. (2023)

  Shouyuan Chen, Sherman Wong, Liangjian Chen, and Yuandong Tian.
  Extending context window of large language models via positional interpolation.
  *arXiv preprint arXiv:2306.15595*, 2023.
- Child et al. (2019)

  Rewon Child, Scott Gray, Alec Radford, and Ilya Sutskever.
  Generating long sequences with sparse transformers.
  *arXiv preprint arXiv:1904.10509*, 2019.
- Dai et al. (2019)

  Zihang Dai, Zhilin Yang, Yiming Yang, Jaime Carbonell, Quoc V Le, and Ruslan Salakhutdinov.
  Transformer-xl: Attentive language models beyond a fixed-length context.
  *arXiv preprint arXiv:1901.02860*, 2019.
- Devlin et al. (2018)

  Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova.
  Bert: Pre-training of deep bidirectional transformers for language understanding.
  *arXiv preprint arXiv:1810.04805*, 2018.
- Dong et al. (2023)

  Zican Dong, Tianyi Tang, Lunyi Li, and Wayne Xin Zhao.
  A survey on long text modeling with transformers.
  *arXiv preprint arXiv:2302.14502*, 2023.
- Guu et al. (2020)

  Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, and Mingwei Chang.
  Retrieval augmented language model pre-training.
  In *International conference on machine learning*, pp. 3929–3938. PMLR, 2020.
- Izacard & Grave (2020)

  Gautier Izacard and Edouard Grave.
  Leveraging passage retrieval with generative models for open domain question answering.
  *arXiv preprint arXiv:2007.01282*, 2020.
- Izacard et al. (2021)

  Gautier Izacard, Mathilde Caron, Lucas Hosseini, Sebastian Riedel, Piotr Bojanowski, Armand Joulin, and Edouard Grave.
  Unsupervised dense information retrieval with contrastive learning.
  *arXiv preprint arXiv:2112.09118*, 2021.
- Jiang et al. (2023)

  Zhengbao Jiang, Frank F Xu, Luyu Gao, Zhiqing Sun, Qian Liu, Jane Dwivedi-Yu, Yiming Yang, Jamie Callan, and Graham Neubig.
  Active retrieval augmented generation.
  *arXiv preprint arXiv:2305.06983*, 2023.
- Karpukhin et al. (2020)

  Vladimir Karpukhin, Barlas Oğuz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih.
  Dense passage retrieval for open-domain question answering.
  *arXiv preprint arXiv:2004.04906*, 2020.
- Kitaev et al. (2020)

  Nikita Kitaev, Łukasz Kaiser, and Anselm Levskaya.
  Reformer: The efficient transformer.
  *arXiv preprint arXiv:2001.04451*, 2020.
- Lee et al. (2019)

  Juho Lee, Yoonho Lee, Jungtaek Kim, Adam Kosiorek, Seungjin Choi, and Yee Whye Teh.
  Set transformer: A framework for attention-based permutation-invariant neural networks.
  In *International conference on machine learning*, pp. 3744–3753. PMLR, 2019.
- Lewis et al. (2020)

  Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al.
  Retrieval-augmented generation for knowledge-intensive nlp tasks.
  *Advances in Neural Information Processing Systems*, 33:9459–9474, 2020.
- Lin (2004)

  Chin-Yew Lin.
  Rouge: A package for automatic evaluation of summaries.
  In *Text summarization branches out*, pp. 74–81, 2004.
- Lin et al. (2023)

  Xi Victoria Lin, Xilun Chen, Mingda Chen, Weijia Shi, Maria Lomeli, Rich James, Pedro Rodriguez, Jacob Kahn, Gergely Szilvasy, Mike Lewis, Luke Zettlemoyer, and Scott Yih.
  Ra-dit: Retrieval-augmented dual instruction tuning, 2023.
- Liu et al. (2023a)

  Nelson F Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang.
  Lost in the middle: How language models use long contexts.
  *arXiv preprint arXiv:2307.03172*, 2023a.
- Liu et al. (2023b)

  Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan Yang, et al.
  AgentBench: Evaluating llms as agents.
  *arXiv preprint arXiv:2308.03688*, 2023b.
- Nakano et al. (2021)

  Reiichiro Nakano, Jacob Hilton, Suchir Balaji, Jeff Wu, Long Ouyang, Christina Kim, Christopher Hesse, Shantanu Jain, Vineet Kosaraju, William Saunders, et al.
  WebGPT: Browser-assisted question-answering with human feedback.
  *arXiv preprint arXiv:2112.09332*, 2021.
- Ouyang et al. (2022)

  Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al.
  Training language models to follow instructions with human feedback.
  *Advances in Neural Information Processing Systems*, 35:27730–27744, 2022.
- Park et al. (2023)

  Joon Sung Park, Joseph C O’Brien, Carrie J Cai, Meredith Ringel Morris, Percy Liang, and Michael S Bernstein.
  Generative agents: Interactive simulacra of human behavior.
  *arXiv preprint arXiv:2304.03442*, 2023.
- Patterson et al. (1988)

  David A Patterson, Garth Gibson, and Randy H Katz.
  A case for redundant arrays of inexpensive disks (raid).
  In *Proceedings of the 1988 ACM SIGMOD international conference on Management of data*, pp. 109–116, 1988.
- Press et al. (2021)

  Ofir Press, Noah A Smith, and Mike Lewis.
  Train short, test long: Attention with linear biases enables input length extrapolation.
  *arXiv preprint arXiv:2108.12409*, 2021.
- Ram et al. (2023)

  Ori Ram, Yoav Levine, Itay Dalmedigos, Dor Muhlgay, Amnon Shashua, Kevin Leyton-Brown, and Yoav Shoham.
  In-context retrieval-augmented language models.
  *arXiv preprint arXiv:2302.00083*, 2023.
- Schick et al. (2023)

  Timo Schick, Jane Dwivedi-Yu, Roberto Dessì, Roberta Raileanu, Maria Lomeli, Luke Zettlemoyer, Nicola Cancedda, and Thomas Scialom.
  Toolformer: Language models can teach themselves to use tools.
  *arXiv preprint arXiv:2302.04761*, 2023.
- Touvron et al. (2023)

  Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al.
  Llama 2: Open foundation and fine-tuned chat models.
  *arXiv preprint arXiv:2307.09288*, 2023.
- Trivedi et al. (2022)

  H. Trivedi, Niranjan Balasubramanian, Tushar Khot, and Ashish Sabharwal.
  Interleaving retrieval with chain-of-thought reasoning for knowledge-intensive multi-step questions.
  *ArXiv*, abs/2212.10509, 2022.
  URL <https://api.semanticscholar.org/CorpusID:254877499>.
- Vaswani et al. (2017)

  Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin.
  Attention is all you need.
  *Advances in neural information processing systems*, 30, 2017.
- Wang et al. (2020)

  Sinong Wang, Belinda Z Li, Madian Khabsa, Han Fang, and Hao Ma.
  Linformer: Self-attention with linear complexity.
  *arXiv preprint arXiv:2006.04768*, 2020.
- Wei et al. (2022)

  Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al.
  Chain-of-thought prompting elicits reasoning in large language models.
  *Advances in Neural Information Processing Systems*, 35:24824–24837, 2022.
- Xu et al. (2021)

  Jing Xu, Arthur Szlam, and Jason Weston.
  Beyond goldfish memory: Long-term open-domain conversation.
  *arXiv preprint arXiv:2107.07567*, 2021.
- Yao et al. (2022)

  Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao.
  React: Synergizing reasoning and acting in language models.
  *arXiv preprint arXiv:2210.03629*, 2022.
- Zheng et al. (2023)

  Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric Xing, et al.
  Judging llm-as-a-judge with mt-bench and chatbot arena.
  *arXiv preprint arXiv:2306.05685*, 2023.

## 6 附录

### 6.1 提示词与指令

MemGPT 提示词为求简洁经过了编辑。完整的实现细节（包括精确的提示词）请访问 <https://research.memgpt.ai>。以下提示词/指令展品按规范整块保留英文原文。

#### 6.1.1 MemGPT 指令（DMR）

用于 MemGPT 人设的示例指令（聊天/对话相关任务）。

The following is information about myself. My task is to completely immerse myself in this role (I should never say that I am an AI, and should reply as if I am playing this role). If the user asks me a question, I should reply with a best guess using the information in core memory and conversation_search.

基线通过系统提示（前置提示）收到以下指令：

Your task is to answer a question from the user about your prior conversations.

The following is a summary of all your prior conversations:

CONVERSATION_SUMMARY

Answer from the perspective of the persona provided (do not say that you are an AI assistant).

If you do not have enough information to answer the question, reply ’NO ANSWER’. Either reply with the answer, or reply ’NO ANSWER’, do not say anything else.

#### 6.1.2 LLM 评审（DMR / 开场白）

为了检验 DMR 任务答案的正确性，我们使用了 LLM 评审。LLM 评审会收到基线方法和 MemGPT 各自生成的答案，并被要求用以下提示做出评判：

Your task is to label an answer to a question as ’CORRECT’ or ’WRONG’.

You will be given the following data: (1) a question (posed by one user to another user), (2) a ’gold’ (ground truth) answer, (3) a generated answer which you will score as CORRECT/WRONG.

The point of the question is to ask about something one user should know about the other user based on their prior conversations.

The gold answer will usually be a concise and short answer that includes the referenced topic, for example:

Question: Do you remember what I got the last time I went to Hawaii?

Gold answer: A shell necklace

The generated answer might be much longer, but you should be generous with your grading - as long as it touches on the same topic as the gold answer, it should be counted as CORRECT.

For example, the following answers would be considered CORRECT:

Generated answer (CORRECT): Oh yeah, that was so fun! I got so much stuff there, including that shell necklace.

Generated answer (CORRECT): I got a ton of stuff... that surfboard, the mug, the necklace, those coasters too..

Generated answer (CORRECT): That cute necklace

The following answers would be considered WRONG:

Generated answer (WRONG): Oh yeah, that was so fun! I got so much stuff there, including that mug.

Generated answer (WRONG): I got a ton of stuff... that surfboard, the mug, those coasters too..

Generated answer (WRONG): I’m sorry, I don’t remember what you’re talking about.

Now it’s time for the real question:

Question: QUESTION

Gold answer: GOLD_ANSWER

Generated answer: GENERATED_ANSWER

First, provide a short (one sentence) explanation of your reasoning, then finish with CORRECT or WRONG. Do NOT include both CORRECT and WRONG in your response, or it will break the evaluation script.

#### 6.1.3 自指示 DMR 数据集生成

DMR 问答对使用以下提示和原始 MSC 数据集生成：

Your task is to write a ”memory challenge” question for a simulated dialogue between two users.

You get as input:

- personas for each user (gives you their basic facts)

- a record of an old chat the two users had with each other

Your task is to write a question from user A to user B that test’s user B’s memory.

The question should be crafted in a way that user B must have actually participated in the prior conversation to answer properly, not just have read the persona summary.

Do NOT under any circumstances create a question that can be answered using the persona information (that’s considered cheating).

Instead, write a question that can only be answered by looking at the old chat log (and is not contained in the persona information).

For example, given the following chat log and persona summaries:

old chat between user A and user B

A: Are you into surfing? I’m super into surfing myself

B: Actually I’m looking to learn. Maybe you could give me a basic lesson some time!

A: Yeah for sure! We could go to Pacifica, the waves there are pretty light and easy

B: That sounds awesome

A: There’s even a cool Taco Bell right by the beach, could grab a bite after
B: What about this Sunday around noon?

A: Yeah let’s do it!

user A persona:

I like surfing

I grew up in Santa Cruz

user B persona:

I work in tech

I live in downtown San Francisco

Here’s an example of a good question that sounds natural, and an answer that cannot be directly inferred from user A’s persona:

User B’s question for user A

B: Remember that one time we went surfing? What was that one place we went to for lunch called?

A: Taco Bell!

This is an example of a bad question, where the question comes across as unnatural, and the answer can be inferred directly from user A’s persona:

User B’s question for user A

B: Do you like surfing?

A: Yes, I like surfing

Never, ever, ever create questions that can be answered from the persona information.

#### 6.1.4 文档分析指令

用于文档分析任务前置提示的示例指令。

You are MemGPT DOC-QA bot. Your job is to answer questions about documents that are stored in your archival memory. The answer to the users question will ALWAYS be in your archival memory, so remember to keep searching if you can’t find the answer. Answer the questions as if though the year is 2018.

问题通过以下提示提供给 MemGPT：

Search your archival memory to answer the provided question. Provide both the answer and the archival memory result from which you determined your answer. Format your response with the format ’ANSWER: [YOUR ANSWER], DOCUMENT: [ARCHIVAL MEMORY TEXT]. Your task is to answer the question:

对基线，提供以下提示及检索到的文档列表：

Answer the question provided according to the list of documents below (some of which might be irrelevant. In your response, provide both the answer and the document text from which you determined the answer. Format your response with the format ’ANSWER: <YOUR ANSWER>, DOCUMENT: [DOCUMENT TEXT]’. If none of the documents provided have the answer to the question, reply with ’INSUFFICIENT INFORMATION’. Do NOT provide an answer if you cannot find it in the provided documents. Your response will only be considered correct if you provide both the answer and relevant document text, or say ’INSUFFICIENT INFORMATION’. Answer the question as if though the current year is 2018.

#### 6.1.5 LLM 评审（文档分析）

为了检验文档分析任务答案的正确性，同时确保答案确实来自所提供的文本（而非来自模型权重），我们使用了 LLM 评审。LLM 评审会收到基线方法和 MemGPT 各自生成的答案，并被要求用以下提示做出评判：

Your task is to evaluate whether an LLM correct answered a question. The LLM response should be the format "ANSWER: [answer], DOCUMENT: [document_text]" or say "INSUFFICIENT INFORMATION". The true answer is provided in the format "TRUE ANSWER:[list of possible answers]". The questions is provided in the format "QUESTION: [question]". If the LLM response contains both the correct answer and corresponding document text, the response is correct. Even if the LLM’s answer and the true answer are slightly different in wording, the response is still correct. For example, if the answer is more specific than the true answer or uses a different phrasing that is still correct, the response is correct. If the LLM response if "INSUFFICIENT INFORMATION", or the "DOCUMENT" field is missing, the response is incorrect. Respond with a single token: "CORRECT" or "INCORRECT".

#### 6.1.6 K/V 任务指令

MemGPT 智能体使用以下人设定义，旨在鼓励 MemGPT 迭代搜索：

You are MemGPT DOC-QA bot. Your job is to answer questions about documents that are stored in your archival memory. The answer to the users question will ALWAYS be in your archival memory, so remember to keep searching if you can’t find the answer. DO NOT STOP SEARCHING UNTIL YOU VERIFY THAT THE VALUE IS NOT A KEY. Do not stop making nested lookups until this condition is met.

基线收到以下提示：

Below is a JSON object containing key-value pairings, all keys and values are 128-bit UUIDs, and your task is to return the value associated with the specified key. If a value itself is also a key, return the value of that key (do a nested lookup). For example, if the value of ’x’ is ’y’, but ’y’ is also a key, return the value of key ’y’.
