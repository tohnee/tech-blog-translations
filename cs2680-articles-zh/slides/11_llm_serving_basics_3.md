---
title: "第 11 讲：LLM 服务基础（三）——调度、分页与并行"
title_en: "LLM Serving Basics III: scheduling, paging and parallelism"
source: https://cs2680.seas.harvard.edu/slides/11_llm_serving_basics_3.pdf
pages: 59
crawled: 2026-11-16
translated: 2026-11-16
---

# 第 11 讲：LLM 服务基础（三）——调度、分页与并行

> PDF 讲义文本抽取：[11_llm_serving_basics_3.pdf](https://cs2680.seas.harvard.edu/slides/11_llm_serving_basics_3.pdf) · Harvard CS2680

## 第 1 页

**现代 AI 系统：智能体与系统优化**

Juncheng Yang

LLM 服务基础（三）：调度、分页与并行

## 第 2 页

**今日安排**

- LLM 服务性能评估
- 调度与资源管理
- 并行

## 第 3 页

**事务**

- 作业 4 下周二午夜截止
  - 阅读并调优引擎参数
  - 投机解码
  - 智能体与引擎协同设计
  - 在书面报告和视频中体现测量／观察 + 推理
  - 你看到了什么、做了什么、什么变了以及为什么、权衡是什么
  - 测量时使用不止一个计数器和指标
- 项目提案上周三截止

## 第 4 页

**LLM 服务不同于以往的计算，例如 Web 服务、批处理作业**

Web 请求约 5–50 ms 就跑完

LLM 请求：预填充 → 解码：每个 token 一次批前向

为什么要花好几节课讲 LLM 服务？

巨大算力：LLM 需要 GPU 和其他加速器

每个 token 都要付费：每个用户请求都要重跑模型

GPU 很贵：服务效率决定成本与速度

## 第 5 页

**LLM 服务的不同之处：单个请求内部**

两个阶段、两个瓶颈

Web 请求：一次短小、无状态的调用

LLM 请求：预填充：计算受限｜解码：内存受限

多 GPU、多服务器：计算与通信

一个请求的前向：GPU 1｜GPU 2｜GPU 3｜GPU 4

柔软、增长的状态：路由器

GPU 1：持有它的 KV 缓存

GPU 2：必须重建它

Token = 重建状态的检查点

## 第 6 页

**LLM 服务的不同之处：跨多个请求**

输出长度未知：提示已知，输出在停止 token 之前未知

Token 作为工作单位：准入、调度、路由、自动扩缩容

速率限制、价格、SLO 都以 token 计数

10⁴–10⁶× 的成本跨度

不断移动的瓶颈：批大小（小 → 大）、上下文长度（短 → 长）、阶段混合（预填充 → 解码）

智能体与推理让每个差距都更大

第 1 轮：新增

第 2 轮：复用 + 新增

第 3 轮：复用前缀 + 新增

约 90% 前缀复用

KV 缓存变成了存储问题

## 第 7 页

**LLM 推理指标与评估**

## 第 8 页

**LLM 服务的两个阶段：预填充与解码**

| | 预填充 | 解码 |
| --- | --- | --- |
| 粒度 | 一次处理全部 S 个提示 token | 每步 1 个 token |
| 主导算子 | 矩阵–矩阵 GEMM | GEMV / 瘦 GEMM |
| 瓶颈 | 计算（FLOPs） | 内存带宽 |
| 延迟驱动因素 | TTFT | TPOT × 输出长度 |

服务效果：一个请求混合了计算受限阶段和内存受限阶段

评估

## 第 9 页

**一个请求时间线上的服务指标**

TTFT｜TBT｜解码 → 每次前向一个 token

排队｜预填充｜t1 t2 t3 t4 t5 t6

时间 →

TPOT = 5 个 TBT 间隔（t2…t6）的平均值

TBT 是单个间隔，按 token 测量，所以它的 P99 能捕捉卡顿。

TPOT 对所有间隔取平均：(E2E − TTFT) ÷ (n − 1)。少数几次长卡顿几乎不会改变它。

E2E = TTFT + TPOT × (n − 1)：从到达到最后一个 token（t6）

吞吐：所有请求合计的每 GPU tokens/s，由大批次最大化。

有效吞吐（goodput）：只统计满足其 TTFT 和 TPOT SLO 的请求的吞吐。

评估

## 第 10 页

**GPU 吞吐 vs 用户吞吐**

GPU 吞吐：服务器每秒发出的全部 token

用户吞吐：1 ÷ TPOT——单个读者感受到的速度

批 1 → 64：GPU 吞吐 20×，但每用户慢 3×

0 / 2K / 4K / 6K

0 25 50 75 100

交互性（每用户 TPS）

6K TPS/GPU

100 TPS/用户

每 GPU TPS

评估

## 第 11 页

**陷阱 1：短促、瞬态的测量**

例子：一次性发送 500 个请求

- 早到的请求要支付 kernel 编译、惰性加载、GPU 时钟爬升和冷前缀缓存的代价；
- 晚到的请求则在不断缩小的批中运行。

整段平均把两者混在一起。

你应该做什么：报告稳态性能。

单次运行的吞吐，K tokens/s

示意；横轴为秒

5.0K / 0K / 2K / 4K / 6K

0 15 30 45 60

预热｜排空

在这里测量

评估

## 第 12 页

**陷阱 2：报告误导性或晦涩的指标**

请求在提示长度、输出长度和延迟敏感度上各不相同，一个平均值可能掩盖用户实际看到的情况。

例子：两个响应各 100 token，都在 5 s 内流式返回

平滑：50 ms

卡顿：卡住 4.5 s，没有新 token，然后 50 ms

平均 TPOT：相同的 50 ms TPOT，但一个用户盯着冻结的流看了 4.5 s。

评估

最大 TBT：50 ms / 4,500 ms

0 s　5 s

你应该做什么：(1) 展示完整分布；(2) 报告 TTFT、TPOT 和吞吐。

## 第 13 页

**陷阱 3：不真实的工作负载**

Token 内容

基准｜真实

草稿 token 很少被接受

kq 7z ##vl 3x｜Summarize this email

长度分布

基准｜真实

一个 320K 的提示会卡住整个批

320K

请求到达

基准｜真实

突发把 P99 TTFT 大幅推高

前缀缓存命中

基准｜真实

共享提示可跳过预填充

评估

你应该做什么：重放真实 trace，使用真实长度和到达时间。

## 第 14 页

**陷阱 4：不公平的比较**

修正：在同一硬件上调优每个基线，然后逐个关闭每种技术来测量其影响。

评估

资源或调优不对等

我们：8 GPU｜基线：4 GPU

两倍的 GPU 可以解释 2× 的胜利

未调优的基线

默认基线 1.0×｜调优基线 1.6×｜我们（调优）1.8×

相对调优基线的真实增益：1.8 ÷ 1.6 ≈ 1.1×

没有隔离算法

实现 70%｜算法 30%

只有 30% 来自算法

## 第 15 页

**批处理、调度、分页与缓存**

批处理

请求调度

内存管理

前缀缓存

## 第 16 页

**连续批处理与迭代级调度**

静态批处理

客户端组成一个批

服务器把整个批跑完

Client｜Server

空闲｜空闲

时间 →

动态批处理

每个请求一到就发送

服务器等待并组成一个批

Client｜Server

等待｜等待｜等待｜空闲｜空闲

时间 →

连续批处理

每个请求一到就发送

按每个 token 生成迭代把序列批在一起

Client｜Server

新｜新

时间 →

批处理

## 第 17 页

**当请求的输入长度和 KV 历史不同时，普通批处理会失效**

| 请求 | 阶段 | 本步 token 数 | KV 缓存长度 |
| --- | --- | --- | --- |
| A | 预填充 | 128 | 0 |
| B | 解码 | 1 | 500 |
| C | 解码 | 1 | 1,000 |

把每个输入都填充到 128 token

A：128 有用

B：127 被填充

C：127 被填充

Yu et al., OSDI 2022 (Orca)

批处理

## 第 18 页

**注意力无法共享一个 GEMM：每个请求读取自己的 KV 缓存，且长度不同**

批处理

线性层：可批处理

Tokens（A、B、C）共享 W → Output（A、B、C）

× W =

每个 token 乘同一个 W，所以一个 GEMM 就能服务所有请求

注意力：按请求

Query × 自己的 KV 缓存、token

A × 300

B × 40

C × 120

没有共享操作数，长度参差不齐，所以每个请求各跑各的注意力

Orca 的观察：并非每个 Transformer 操作都需要相同的批处理策略。

Yu et al., OSDI 2022 (Orca)

## 第 19 页

**选择性批处理：批处理所有线性层，只按请求拆分注意力**

展平 → 批处理 → 按请求 → 批处理 → 批处理

输入 token：来自所有请求，拼成一个以 token 为主序的矩阵

QKV 投影：所有 token 一个 GEMM

Attention A：自己的 KV 缓存

Attention B：自己的 KV 缓存

Attention C：自己的 KV 缓存

Merge + 输出投影：一个 GEMM

MLP、LayerNorm、残差：对所有 token 批处理

为什么有效：线性层对每个 token 一视同仁，所以一个 GEMM 服务所有请求；只有注意力需要每个请求自己的 KV 缓存。

Yu et al., OSDI 2022 (Orca)

批处理

## 第 20 页

**请求调度**

FCFS/SJF · 分块预填充 · 分离式部署

## 第 21 页

**请求调度：先来先服务（FCFS）**

vLLM 和 SGLang 默认使用 FCFS

- 随着 KV 缓存空间释放，按到达顺序接纳等待中的请求
- 简单且无饥饿，但队首的一个长请求会拖慢后面所有请求

但如何混合新到请求的预填充和正在进行的解码？

立即预填充

批更大，但阻塞所有解码请求

等解码完成

TPOT 受影响更小，但新请求排队很久

调度

D D 预填充 D D

解码在这里被卡住

D D D D D 预填充

新请求等待

## 第 22 页

**预填充优先的调度器保护 TTFT；解码优先的调度器保护 TPOT**

预填充优先（SGLang）

D D 预填充 D D　时间 →

+ TTFT：新提示立即开始

+ 吞吐：批每一步都能补满

− TPOT：每次有新请求到达都会卡住所有解码

解码优先（FasterTransformer）

D D D D D 预填充　时间 →

+ TPOT：稳定的 token 流

− TTFT：新提示要等一次排空

− 吞吐：随着请求结束，批会缩小

打破权衡的两种方式

分块预填充：把小的提示块混入解码批

分离式部署：在独立的 GPU 上运行预填充与解码

框架来自 Agrawal et al., Sarathi-Serve, OSDI 2024

调度

## 第 23 页

**分块预填充试图取得平衡**

方块宽度 = 步时间。D = 4 个运行中请求的纯解码步。

不分块：D → 预填充 2,048 token + 4 个解码 · 92 ms → D D

运行中的请求要等 92 ms 才能拿到下一个 token

512 token 分块：D → Chunk 1 + 4 decodes → Chunk 2 + 4 decodes → Chunk 3 + 4 decodes → Chunk 4 + 4 decodes → D D

每一步：512 个提示 token + 4 个解码，所以约每 23 ms 出一个 token

每步 token 预算限制了迭代延迟

这依赖混合批 kernel 与纯预填充或纯解码 kernel 一样高效。

SGLang：预填充优先（用 `--prefill-decode-interval N` 保护解码）

vLLM：解码优先（配合分块预填充）

Agrawal et al., Sarathi-Serve, OSDI 2024; SGLang and vLLM scheduler docs

调度

分块预填充的缺点是什么？

## 第 24 页

**分块预填充需要更多内存读取**

2,048 token 的提示，块大小 512

Iter 1：chunk 1

Iter 2：cached KV + chunk 2

Iter 3：cached KV + cached KV + chunk 3

Iter 4：cached KV + cached KV + cached KV + chunk 4

现在计算｜从缓存读取｜尚未

总预填充 FLOPs 相同，只是分散到 4 个更短的步。

代价：KV 被重复读取

第 k 块读取 (k − 1) × 512 个 token

Agrawal et al., Sarathi (2023) and Sarathi-Serve (OSDI 2024); vLLM: `enable_chunked_prefill`

块大小在解码延迟与预填充效率之间做权衡

调度

## 第 25 页

**PD 分离把预填充和解码分开**

一个请求的路径

提示到达 → 预填充池：运行提示，输出 token 1 → 每请求的 KV 缓存 → 解码池：加载 KV，然后大批解码 → token 2 … n

预填充池：计算受限；按 TTFT 定容并并行

KV 传输：提示 KV 逐层经 NVLink 或 RDMA 发送

解码池：内存受限；大批次，按 TPOT 定容

DistServe (Zhong et al., OSDI 2024); Splitwise (Patel et al., ISCA 2024); Mooncake (Qin et al., FAST 2025)

调度

## 第 26 页

**每个池都有自己的并行方式和批大小，针对自己的 SLO 调优**

分别配置每个池

| | 预填充池 | 解码池 |
| --- | --- | --- |
| 目标 | TTFT SLO | TPOT SLO |
| 批 | 一个或少数几个提示 | 数百条序列 |
| 并行 | 更多 TP，更低延迟 | 更多副本 |
| 最适合的 GPU | 高 FLOPS | 高 HBM 带宽 |

代价：每个请求一次 KV 传输、需要调 P∶D 比例、两个或更多实例。

Zhong et al., DistServe, OSDI 2024; Patel et al., Splitwise, ISCA 2024

调度

## 第 27 页

**PD 分离需要在节点之间搬运 KV 缓存**

KV 大小：Llama-3.1-70B（GQA），FP16

2（K、V）× 80 层 × 8 个 KV 头 × 128 维 × 2 字节 = 每 token 320 KB

× 65,536 token = 20 GB

其预填充 ≈ 11.5 s：2 × 70B × 65,536 ÷ (4 × 200 TFLOPS)

搬运 20 GB 的时间

| 链路 | 带宽 | 时间 |
| --- | --- | --- |
| NVLink，H100 | 450 GB/s | 44 ms |
| NVLink，A100 | 300 GB/s | 67 ms |
| InfiniBand 400 Gb/s | 50 GB/s | 400 ms |
| PCIe 4.0 x16 | 32 GB/s | 625 ms |
| 以太网 100 Gb/s | 12.5 GB/s | 1.6 s |

即使 400 ms 也不到预填充时间的 4%。

逐层流式传输能隐藏大部分：第 i 层的 KV 在发运时，第 i+1 层正在计算。

调度

## 第 28 页

**从 FCFS 到 SJF：短请求不应排在长请求后面**

队头阻塞：一个满批，按到达顺序服务

GPU：批已满

R0 · 长回答，1,000 个输出 token

R1 20 tok｜R2 20 tok｜R3 20 tok｜R4 20 tok

R1–R4 要等 R0 的全部 token；队首在左侧；到达顺序 R0 → R4

FCFS：按到达顺序服务。vLLM 和 SGLang 的默认；一个长任务会延迟它后面的每个请求。

SJF：最短作业优先。最小化平均等待时间，但需要预先知道每个作业的大小。

对 LLM 而言，作业大小取决于输出长度，而在解码结束前是未知的。

调度

## 第 29 页

**最短作业优先需要输出长度，所以学会对它们排序**

三个请求同时到达；GPU 每秒输出一个 token

FCFS：R0 · 10 token → R1 · 2 → R2，平均 6.7 s/token

SJF：R2 → R1 · 2 → R0 · 10 token，平均 1.3 s/token

0 s　13 s

难点：输出长度在解码结束前未知，因此必须预测

等待中的提示 → OPT-125M 排序器给每个提示打分 → 队列按预测排名排序 → vLLM 的批每一步取最前面的

排序而不是回归：用排序损失训练；只关心相对顺序

饥饿保护：等待过久的请求会被提升

Fu et al., Efficient LLM Scheduling by Learning to Rank, NeurIPS 2024

ADVANCED —— 可略读，或自行深入阅读

调度

## 第 30 页

**FastServe：带跳入多级队列的 token 级抢占**

按提示长度跳入队列

新作业进入其时间片足以覆盖预填充时间的最高队列

Wu et al., FastServe, NSDI 2026 (arXiv 2305.05920)

Q1　q

Q2　2q

Q3　4q

Q4　8q · 最低优先级

长提示：prefill > 2q → Q3

短提示：prefill ≤ q → Q1

降级：用完自己时间片的作业下降一个队列

提升：等待过久的作业会被提升回去，以防饥饿

为什么有效：长作业下沉、短作业先完成，因此在不知道作业大小的情况下近似 SRPT（最短剩余处理时间优先）

ADVANCED —— 可略读，或自行深入阅读

调度

条长 = 每一轮的时间片 →

↓ 时间片用完：降级　·　Q1 = 最高优先级

## 第 31 页

**检验你的理解：请求调度**

Q1. 每当长提示到达时，P99 TBT 就会飙升。哪些技术可以解决？

答：分块预填充限制每步的提示 token 数；PD 分离把预填充移出解码步。

Q2. 什么时候 PD 分离不值得部署？

答：短提示或小规模集群：KV 传输、P∶D 调优和额外实例的成本超过卡顿的代价。

Q3. SJF 需要作业大小。对于智能体工作负载，还有其他方法可以避开这一点吗？

答：用未缓存的预填充 token 数作为作业大小。

调度

## 第 32 页

**内存管理**

PagedAttention

## 第 33 页

**输出长度未知，迫使 KV 预留以三种方式浪费内存**

Llama-3.1-70B 在两块 H200 上，282 GB 内存

权重 141 GB · 50%｜KV 缓存 ~130 GB · 45%｜激活 Act.

每 token 320 KB · 在 128K token 上限下每请求 40 GB · 约 3 个这样的请求就填满 KV 预算

The cat sat on｜Hi all

请求 A：为其 128K token 上限预留｜请求 B

使用中｜已预留｜内部碎片｜外部碎片｜使用中｜预留｜内部｜外部

1. 已预留（Reserved）

为尚未生成的 token 保留的槽位。以后会用到，但在那之前一直空闲。

2. 内部碎片（Internal fragmentation）

超过真实结尾的槽位。回复在达到最大长度前就命中了 EOS。

在 Orca 式连续分配器中，只有 20–38% 的 KV 内存保存了真实 token。

来源：Kwon et al., SOSP 2023, Fig. 2–3; Meta Llama 3.1 70B config, 2024; NVIDIA H200 datasheet

PagedAttention

## 第 34 页

**连续缓存无法共享，所以 n 个样本要存 n 份相同的提示**

并行采样，n = 3，连续大块

Sample 1：Prompt KV，copy 1，Output 1

Sample 2：Prompt KV，copy 2，Output 2

Sample 3：Prompt KV，copy 3，Output 3

并行采样：对同一提示的 n 个回复会把提示复制 n 次

Beam search：各 beam 共享提示以及每步都会移动的前缀；一次分叉会复制整个大块

共享系统提示：每个用户请求都重复相同的指令

PagedAttention

## 第 35 页

**PagedAttention 像操作系统分页那样管理 KV 缓存**

请求 A：逻辑块｜块表｜GPU 中的物理 KV 块

每个 token 一个槽位（OS：字节）

| 逻辑块 | 物理块 # | 已填充 |
| --- | --- | --- |
| 0 The cat sat on | 4 | 4 |
| 1 the mat and then | 1 | 4 |
| 2 it slept | 3 | 2 |

row = 逻辑块

0 Hi all

1 the mat and then

2

3 it slept

4 The cat sat on

5

按需分页：只有最后一个块填满才分配新块

共享页、写时复制：共享的提示块带引用计数

交换到磁盘：把块换到 CPU 内存

一级间接寻址消除了对连续内存的需求。

来源：Kwon et al., PagedAttention and vLLM, SOSP 2023, Fig. 6。块可容纳 16 个 token；图中显示 4 个。

PagedAttention

## 第 36 页

**前缀缓存**

## 第 37 页

**前缀缓存：复用服务器已经计算过的前缀 KV**

前缀缓存

三个聊天请求共享一个系统提示

Req 1：系统提示 → 预填充 → Q1

Req 2：系统提示 → 缓存命中 → Q2

Req 3：系统提示 → 缓存命中 → Q3

预填充工作量，1,000 token 提示 + 50 token 问题

无缓存：3 × 1,050 = 3,150 token

前缀缓存：1,050 + 50 + 50 = 1,150 token

共享前缀从哪来

系统提示：每个请求重复相同指令

多轮聊天：每一轮都重发历史

智能体：每一步都重发工具和此前的轨迹

只做精确匹配：一个 token 的 KV 依赖它之前的每一个 token。

## 第 38 页

**块哈希：用整个前缀的哈希查找缓存 KV 块**

来源：vLLM documentation, Automatic Prefix Caching design, 2024

前缀缓存

一个提示，每块 4 个 token（vLLM 使用 16）

You are a helpful → h0 = H(∅, B0) → 命中：块 7

assistant who → h1 = H(h0, B1) → 命中：块 2

answers in French → h2 = H(h1, B2) → 未命中：计算

每个哈希都折入其父哈希，所以 h2 考虑了全部 12 个 token，而不只是最后 4 个。

查找：对新提示的每个完整块做哈希；遇到第一个未命中就停止

共享：一次命中会增加该块的引用计数；不复制任何东西

驱逐：无人引用的块留在缓存中，直到需要内存时按 LRU 顺序淘汰

粒度：最后一块未填满时从不共享

在 PagedAttention 之上加一张哈希表，就把共享块变成了缓存。

## 第 39 页

**SGLang RadixAttention：把每个请求的 KV 存进基数树并共享前缀**

来源：Zheng et al., SGLang, NeurIPS 2024, Sec. 3 and Fig. 3

前缀缓存

一棵树保存所有已缓存请求的 KV

root

System prompt

Few-shot set

Chat A, turn 1

Chat B, turn 1

Query 1

Query 2

Query 3

Turn 2

LRU 已驱逐

到达：在树中匹配最长前缀；只预填充其余部分

完成：把新 token 作为分支持入；KV 留在 GPU 上

驱逐：没有运行中请求使用时，丢弃最近最少使用的叶子

分支共享父节点的 KV，所以公共前缀只存一次。

## 第 40 页

**检验你的理解：前缀缓存**

Q1. 两个提示只在 1,000 个 token 中的第 3 个 token 处不同。它们能共享多少 KV？

答：最多两个 token；用 16 token 块哈希则一个都不能共享：每个 token 的 KV 都依赖它前面的所有 token。

Q2. 为什么最大化前缀缓存命中会与公平调度冲突？

答：优先服务缓存最热的客户端可能饿死其他客户端。

Q3. 一个缓存前缀在块中间结束。哪种索引仍能复用它：块哈希还是基数树？

答：基数树，它按 token 粒度匹配；块哈希只复用完整块。

前缀缓存

## 第 41 页

**并行：一个模型，多块 GPU**

数据并行（DP）

张量并行（TP）

流水线并行（PP）

专家并行（EP）

序列并行（SP）

## 第 42 页

**为什么一块 GPU 不够**

- 仅权重就超过单块 GPU；KV 缓存还要抢同一份 HBM
- 单块 GPU 的带宽限制了解码速度
- 并行换来容量与速度

一个 bf16 的 70B 模型

权重 140 GB，一块 GPU 只有 141 GB

把它切到 4 块 GPU 上

GPU 0｜GPU 1｜GPU 2｜GPU 3

每块 35 GB 权重，还有空间放 KV

粗略估算

t_token ≥ 2N ÷ BW_HBM

H200 上的 70B bf16：140 GB ÷ 4.8 TB/s ≈ 29 ms

并行

## 第 43 页

**集合通信：send/recv、broadcast、all-gather**

颜色 = 产生数据的 GPU；数字 = 分片；M = A、W 或 0–3 的大小

之前 → 之后

G0 G1 G2 G3 → G0 G1 G2 G3

Send / recv：一块 GPU 把缓冲区发给一个对等方

使用者：PP 阶段跳转、SP 环

A → A A A

Broadcast：一块 GPU 把它的缓冲区复制给所有 GPU

使用者：把批输入送到 TP rank

W → W W W W

All-gather：每个 GPU 贡献一个分片；所有 GPU 都得到完整数据

使用者：TP 输出、SP 的 K/V

0 1 2 3 → 每个 GPU 都得到 0 1 2 3

每 GPU 成本：M｜M｜0.75 M

并行

## 第 44 页

**集合通信：reduce-scatter、all-reduce、all-to-all**

颜色 = 源 GPU；数字 = 分片

灰色 Σ = 跨 GPU 求和；M = 全部 4 个分片

之前 → 之后

G0 G1 G2 G3 → G0 G1 G2 G3

Reduce-scatter：跨 GPU 求和；每个 GPU 保留一个分片

使用者：带序列并行的 TP

每块 GPU 原本都有 0 1 2 3 → G0 得到 Σ0，G1 得到 Σ1，G2 得到 Σ2，G3 得到 Σ3

All-reduce：跨 GPU 求和；每块 GPU 保留全部

= reduce-scatter + all-gather

使用者：行并行层之后的 TP

0 1 2 3（各 GPU）→ 每块 GPU 都有 Σ0 Σ1 Σ2 Σ3

All-to-all：GPU i 把分片 j 发给 GPU j

使用者：EP 的 token dispatch 与 combine

每块 GPU 原本都有 0 1 2 3 → 之后：G0 收到 0 0 0 0，G1 收到 1 1 1 1，G2 收到 2 2 2 2，G3 收到 3 3 3 3

每 GPU 成本：0.75 M｜1.5 M｜0.75 M

并行

## 第 45 页

**数据并行：更多副本**

- 每块 GPU 持有整个模型
- 请求分散到各副本
- 扩展吞吐
- 每个副本有自己的调度器和 KV 缓存

传入请求 → 路由器拆分流量 → replica 0（完整模型 + 自己的 KV）｜replica 1（完整模型 + 自己的 KV）

2× 吞吐，最大模型大小不变

粗略估算

吞吐 ≈ G × Θ₁

G 个副本；每 GPU 内存仍为 2N + KV

通信：0，副本之间从不通信

矩阵视角

X₀ × W = Y₀（GPU 0）｜X₁ × W = Y₁（GPU 1）

X₂ × W = Y₂（GPU 2）｜X₃ × W = Y₃（GPU 3）

每块 GPU 有相同的 W；批按行拆分

并行

## 第 46 页

**张量并行：在层内拆分**

- 每层的矩阵跨 GPU 切片
- 每块 GPU 计算每一层的一部分
- 每个块用一次 all-reduce 合并切片
- 需要 NVLink 级带宽，所以留在一个节点内

一个 transformer 层，四块 GPU

shard 0｜shard 1｜shard 2｜shard 3

每个块之后 all-reduce

对全部 L 层重复

GPU 越多，通信越多

粗略估算

每 GPU 权重 = 2N ÷ G

70B，G = 4 块 GPU → 每块 35 GB

每 GPU 通信：每层 2 × 1.5 × 2bh 字节

并行

## 第 47 页

**列并行线性层：按列切分 W，每块 GPU 拥有完整的输出列**

每块 GPU 持有 W 的纵向切片和 X 的完整副本，因此无需通信就能算出自己的输出列。

X：b × h，所有 GPU 上都有

× W₀ W₁ W₂ W₃：每个 h × f/G

= Y₀ Y₁ Y₂ Y₃：每个 b × f/G

GPU 0: Y₀ = X · W₀

GPU 1: Y₁ = X · W₁

GPU 2: Y₂ = X · W₂

GPU 3: Y₃ = X · W₃

b 个 token，h 个隐藏单元，f 为输出宽度

通信

层内没有通信。只有当下一步需要完整 Y 时才加一次 all-gather。

Shoeybi et al., Megatron-LM, arXiv 1909.08053, 2019

并行

## 第 48 页

**行并行线性层：按行切分 W，每块 GPU 持有一个部分和，需要 all-reduce**

每块 GPU 持有 W 的横向切片和 X 中对应的列。它的乘积是全尺寸的，但只是答案的一部分。

X₀ X₁ X₂ X₃：每个 b × h/G

×

W₀

W₁

W₂

W₃：每个 h/G × h

= Z₀ + Z₁ + Z₂ + Z₃：部分和，每个 b × h

all-reduce

Z

Z = Σ Zᵢ

b 个 token，h 为隐藏大小；GPU i 计算 Zᵢ = Xᵢ · Wᵢ

通信

对 b × h 输出做一次 all-reduce（bf16 下 2bh 字节）；每块 GPU 发送 2(G − 1)/G × 2bh，在 G = 4 时为 3bh

Shoeybi et al., Megatron-LM, arXiv 1909.08053, 2019

并行

## 第 49 页

**Megatron TP 块：先列并行再行并行，每个块一次 all-reduce**

列并行层的输出分片恰好就是行并行层需要的输入，所以 GPU 只在最后通信一次。

MLP

X → Up + gate（列并行）→ 激活（本地，无通信）→ Down proj（行并行）→ All-reduce（对部分和求和）

Attention

X → Q、K、V 投影（列并行，每 GPU 1/G 个头）→ Attention（本地，按头）→ 输出投影（行并行）→ All-reduce（对部分和求和）

Shoeybi et al., Megatron-LM, arXiv 1909.08053, 2019

并行

## 第 50 页

**流水线并行：切分各层**

- 各层被切成连续阶段
- 每块 GPU 拥有一个连续的层块
- 微批让每个阶段保持忙碌
- 能容忍较慢的链路，因此可以跨节点

80 层切成 4 个阶段

L1–20｜L21–40｜L41–60｜L61–80

粗略估算

气泡 = (G − 1) ÷ (m + G − 1)

G = GPU（阶段）数，m = 微批数

G = 4：m = 4 → 43%，m = 16 → 16%

通信：每个阶段跳转发送一次 2bh 字节

前向：4 个微批，4 个阶段

G0: 1 2 3 4

G1: 1 2 3 4

G2: 1 2 3 4

G3: 1 2 3 4

时间步 1–7 →

灰色 = 气泡：28 个槽位中 12 个空闲 = 3/7 ≈ 43%

并行

## 第 51 页

**专家并行：切分专家**

- 一个 MoE 层有很多专家；每个 token 只用其中几个
- 专家分散在多块 GPU 上
- 用 all-to-all 把 token 送到其专家
- 路由不均会让部分 GPU 空闲

8 个专家分布在 4 块 GPU 上

GPU 0：E0 E1

GPU 1：E2 E3

GPU 2：E4 E5

GPU 3：E6 E7

粗略估算

每 GPU 负载 ≈ k × b ÷ G

top-2、1,024 token、4 GPU → 每块 512

每 GPU 通信：每层 2 × 0.75 × 2kbh 字节

token t → E3 和 E7（k = 2）

1. Dispatch：把 t 发给它的 k 个专家
2. Compute：每个专家本地运行
3. Combine：把结果送回并求和

所有 GPU 同时做这件事：all-to-all

并行

## 第 52 页

**上下文并行：切分 token**

- 长提示会溢出一块 GPU
- 每块 GPU 持有一个 token 块
- Ring attention 传递 K/V 块
- 帮助预填充，不帮助解码

一个 128K token 的提示分到 4 块 GPU

GPU 0：0–32K

GPU 1：32–64K

GPU 2：64–96K

GPU 3：96–128K

把 K/V 块传给下一块 GPU

每个 query 仍然看到每个 key

传输与注意力计算重叠

粗略估算

每 GPU token 数 = s ÷ G

128K token 提示，G = 4 → 每块 32K token

通信：每层 G − 1 次 K/V 块传递

并行

## 第 53 页

**TP 和 EP 每 token 搬运的字节比 PP 多 240×**

| 策略 | 集合通信 | 频率 | 字节 / token / GPU |
| --- | --- | --- | --- |
| 数据并行 | 无 | 从不 | 0 |
| 张量（G = 4） | all-reduce | 每层 2 次 | 3.9 MB |
| 流水线（G = 4） | send / recv | 每阶段跳转 1 次 | 16 KB |
| 专家（G = 4，top-2） | all-to-all | 每个 MoE 层 2 次 | ≈ 3.9 MB |

70B 形状的模型：h = 8,192，80 层，bf16，解码一个 token。

环形 all-reduce 搬运 2(G − 1)/G 的数据；每层都有 MoE，4 个专家中 3 个在远端。

并行

## 第 54 页

**TP 和 EP 需要 NVLink**

每 GPU 链路带宽，GB/s 每方向

H100 SXM：NVLink 4（双向 900 GB/s）、PCIe Gen5 x16、InfiniBand NDR 400 Gb/s

一次传输的成本

t = 字节 ÷ 带宽 + 跳数 × 延迟

张量流量，3.9 MB/token/GPU

NVLink ≈ 9 µs；InfiniBand ≈ 78 µs，另加开销

经验法则

TP 在节点内；PP 跨节点

50 GB/s　InfiniBand NDR

64 GB/s　PCIe Gen5 x16

450 GB/s　NVLink 4

并行

## 第 55 页

**检验你的理解：并行**

Q1. 一个 70B bf16 模型放在 4 块 H200（每块 140 GB）的单节点上。先做哪种切分，为什么？

答：NVLink 上 TP = 4，或者 DP2 + TP2，取决于上下文大小。

Q2. 增加第二个节点。应该用什么并行？

答：跨节点 PP：每 token 一次 2h 字节的跳转；而 TP 每层都要 all-reduce，流量约多 240×。

Q3. 为什么长上下文下 DP 注意力 + EP 可能优于 TP，而短上下文下反而不如？

答：长上下文：当 KV 头数 < rank 数时 TP 会复制 KV，而 DP 支持更大的批。短上下文：all-to-all 开销占主导。

并行

## 第 56 页

**并行：要点**

数据并行扩展吞吐：G 个副本服务 G× 的请求，但每个副本都必须持有整个模型

张量并行降低每 token 延迟：每块 GPU 读取 1/G 的权重，代价是每层 all-reduce；留在一个 NVLink 节点内

流水线与序列并行增加容量：流水线跨节点、流量轻但带来气泡；序列并行切分超长提示

专家并行服务 MoE 模型：专家分散在 GPU 上；代价是 all-to-all 流量和专家负载不均

并行

## 第 57 页

**下一讲：投机解码**

今日概要

测量：TTFT 和 TBT 分位数、有效吞吐

批处理：连续批处理、选择性批处理

调度：请求调度、分块预填充、分离式部署

内存管理：分页、共享 KV 缓存

并行：DP、TP、PP、EP、SP

## 第 58 页

**延伸阅读**

## 第 59 页

**延伸阅读：每一节背后的论文**

评估

Agrawal et al., On Evaluating Performance of LLM Inference Systems, arXiv 2025

批处理与调度

Yu et al., Orca, OSDI 2022

Agrawal et al., Sarathi-Serve, OSDI 2024

Sheng et al., Fairness in Serving LLMs, OSDI 2024

PD 分离

Zhong et al., DistServe, OSDI 2024

KV 缓存内存

Kwon et al., PagedAttention and vLLM, SOSP 2023

Zheng et al., SGLang, NeurIPS 2024

并行

Shoeybi et al., Megatron-LM, arXiv 2019

Korthikanti et al., Reducing Activation Recomputation, MLSys 2023

Thakur, Rabenseifner and Gropp, Collective Operations in MPICH, IJHPCA 2005
