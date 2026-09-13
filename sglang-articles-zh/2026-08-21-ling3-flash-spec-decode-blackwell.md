---
title: "追逐批量大小 1 的下限：Ling-3.0-flash 在 Blackwell 上的投机解码"
title_en: "Chasing the Batch-1 Floor: Ling-3.0-flash Speculative Decode on Blackwell"
author: "RadixArk SGLang Team, Ant Ling Infra Team"
date: "August 21, 2026"
previewImg: /images/blog/ling3-flash-batch1/00_headline.png
type: blog
source: https://lmsys.org/blog/2026-08-21-ling3-flash-spec-decode-blackwell/
translated: 2026-09-12
---

# 追逐批量大小 1 的下限：Ling-3.0-flash 在 Blackwell 上的投机解码

> 原文：[Chasing the Batch-1 Floor: Ling-3.0-flash Speculative Decode on Blackwell](https://lmsys.org/blog/2026-08-21-ling3-flash-spec-decode-blackwell/) · LMSYS Blog · RadixArk SGLang Team, Ant Ling Infra Team

批量大小为 1（batch-1）的解码正变得越来越重要。例如小米 MiMo 在 6 月[发布了 MiMo-V2.5-Pro UltraSpeed](https://mimo.xiaomi.com/blog/mimo-tilert-1000tps)，宣称在万亿参数 MoE 模型上实现 1,000 tok/s 的解码。

批量 1 让推理栈没有任何藏匿开销的余地。没有批量可以摊销启动开销，没有并发可以填补流水线气泡，算术强度也不足以让精巧的 tile 划分产生收益。关键路径上的每一微秒，都是用户等待的一微秒。

本文讲的就是在 4 块 NVIDIA Blackwell GPU 上，为 Ling-3.0-flash——一个混合线性注意力的 MoE 模型——把这个下限继续压低。文章涵盖两条投机解码路径。在 NEXTN/MTP（多 token 预测）路径上，我们把单请求解码从 288 tok/s 提升到 606 tok/s，平均 TPOT（每 token 生成时间）从 3.33 ms 降到 1.53 ms。第二条路径是 DSpark，一个构建在同一套栈之上、按置信度调度的投机解码器：1000 个请求的测试达到 1120 tok/s，平均 TPOT 0.78 ms，接受长度（accept length）9.95。最后这组对比是受控对比：NEXTN 与 DSpark 在同一台机器上用同一条命令测得，平均 TPOT 降低了 1.9 倍（从 1.53 ms 到 0.78 ms）。本文余下部分要回答的是：那些时间原本去哪儿了，以及把它们夺回来都做了什么。

## 核心要点

- 最终结果：平均 TPOT 下降 54%（3.33 ms → 1.53 ms），单请求吞吐量提升至 2.1 倍（288 → 606 tok/s）。在受控的 1000 请求对比中，DSpark 达到 0.78 ms 平均 TPOT 与 1120 tok/s。
- 优化路线是：主机超前运行（host run-ahead）→ PDL 链接 → 内核优化 → DSpark。移除每步的主机阻塞点，让准备工作得以躲到 GPU 工作背后；随后 PDL 把 MoE、路由器、KDA 与 all-reduce 路径串成链；两处算子融合、一次 KDA 重调优，加上改用 bf16 的路由/lm_head GEMM，缩短了剩余的 GPU 关键路径。
- 数值精度作为带宽旋钮：路由门控与 lm_head 从 fp32 改为 bf16，是结构性修复之后最大的一项单体改动，收益约 +10%。
- 贯穿始终的测量纪律：任何主机侧结论都先做剖析态与未剖析态的校准；冷权重微基准测试；A/B 决策以平均 TPOT 为准，而非单窗口峰值。
- DSpark 提高了每个验证步提交的 token 数：并发 1 下接受长度 9.95、1120 tok/s，平均 TPOT 0.78 ms。对比同一 1000 请求基准上的 NEXTN，平均 TPOT 降低了 1.9 倍。

<p align="center"><img src="/images/blog/ling3-flash-batch1/00_headline.png" alt="Headline results across the four configurations" width="100%"></p>

*图 1. 四种配置的核心结果。*

| 指标（8192 输入 / 1024 输出，并发 1，贪心解码，TP4 bf16） | 基线 | 草稿-扩展图修复后 | NEXTN 调优后 | 使用 DSpark |
|-|-|-|-|-|
| 平均输出吞吐量 | 288 tok/s | 526 tok/s | 606 tok/s | **1120 tok/s** |
| 平均 TPOT | 3.33 ms | 1.76 ms | 1.53 ms | **0.78 ms** |
| TPOT 中位数 | — | — | 1.56 ms | **0.51 ms** |
| 峰值输出吞吐量 | — | — | 1099 tok/s | **1945 tok/s** |
| 接受长度 | 3.14 | 3.13 | 3.25 | **9.95** |

在 GSM8K 上，同一套栈的成绩为：准确率 0.889，无效输出 0.000，延迟 341.5 s，输出吞吐量 511.1 tok/s。

所有运行均在 4 块 Blackwell GPU 上使用 Ling-3.0-flash，TP4、bf16、并发 1、贪心解码，以及同一份固定的 8192 输入 / 1024 输出 random 负载。从左到右，各列分别是：初始 NEXTN 基线、草稿-扩展图修复后的 NEXTN、最终调优的 NEXTN，以及 DSpark。前两列是优化过程中较早的检查点；后两列是受控对比，各自在同一台机器上对同样的 1000 个请求测得。峰值吞吐量只在后两次运行之间比较，因为它是固定 1 秒窗口上的最大值。

这里有两个定义需要交代，它们合起来解释了为什么即便在并发 1 下，输出吞吐量也不是平均 TPOT 的简单倒数：SGLang 的 TPOT 不包含首 token 延迟（TTFT），而输出吞吐量是用总输出 token 数除以基准测试总墙钟时间（参见 [bench_serving 指南](https://github.com/sgl-project/sglang/blob/main/docs/developer_guide/bench_serving.md)）。本文所有核心基准运行都使用合成的 `random` 负载；接受长度尤其取决于提示词与输出分布，因此 9.95 是该负载下的接受长度，而不是模型本身的。

---

## 模型

<p align="center"><img src="/images/blog/ling3-flash-batch1/01_model_architecture.png" alt="Ling-3.0-Flash architecture: 42 layers interleaving 35 KDA linear-attention layers with 7 MLA full-attention layers over a 512-expert MoE" width="100%"></p>

*图 2. Ling-3.0-Flash 架构：42 层中，35 层 KDA 线性注意力与 7 层 MLA 全注意力交错，底层是 512 专家的 MoE。*

Ling-3.0-flash 是一个混合注意力 MoE 模型（`BailingMoeV3`），后文的大部分内容都源自 *hybrid*（混合）这个词。

| 层数 | 共 42 层：35 层 KDA 线性注意力 + 7 层 MLA 全注意力 |
|-|-|
| MoE | 512 个路由专家 + 1 个共享专家，top-8（+1），`moe_intermediate_size` 768 |
| 隐藏维度 | 2560 |
| 词表 | 约 157k，经词表并行的 lm_head 提供服务 |
| 权重 | bf16 下每个 rank 约 63 GB |
| 部署 | 4 块 NVIDIA Blackwell GPU，TP4，bf16，NEXTN 投机解码 |

每六个注意力层里有五个是 KDA。这就是为什么在最终剖析中，8k 上下文下 MLA 注意力每步只花 244 µs；也是为什么这个模型从一开始就是很好的 batch-1 优化对象：注意力便宜、批量极小，关键路径上剩下的就是权重带宽和启动延迟——而这恰好就是本文要讨论的运行区间。

## 一个 batch-1 步的形态

我们以 `steps=5, topk=1, draft_tokens=6` 的 NEXTN 投机解码进行解码。一个解码步是三个 CUDA 图的接力。

<p align="center"><img src="/images/blog/ling3-flash-batch1/02_three_graph_relay.png" alt="Three graphs per decode step" width="100%"></p>

*图 3. 每步三个图。草稿模型提出一条 6 token 的候选链，目标模型一次前向给全部 6 个打分，扩展（extend）图用目标模型的真实隐藏状态重放被接受的前缀，生成下一轮的种子。判定本身（`eagle_sample`）发生在验证图内部；主机要晚一步才知道接受了多少 token。*

草稿是单层 NEXTN 模型，以自回归方式运行：五个步骤却只有四次前向，因为第一个候选来自上一轮的种子，第五个则直接从第四次前向的 top-k 里读出。验证是 42 层完整目标模型对全部 6 个链位置的一次前向。扩展则修补草稿的 KV 缓存——它此前只见过草稿自己的猜测——并把下一轮的种子交回去。

这三个图之间在 CPU 上传递的东西是零。固定形状加填充，让每个依赖接受结果的计数都成为 GPU 上的索引而非主机侧数值；持久缓冲区让生产者图直接写进消费者图的缓冲区；而真正需要在 CPU 上拿到数值的决策（EOS、停止字符串、detokenization）则走一条独立流的 D2H 拷贝，配合一个晚一步才被消费的 `copy_done` 事件。下文的一切都建立在这个性质之上。

## 两种空转时间

项目开始时，GPU 在一个步内只有大约三分之二的时间是忙的。batch-1 下的空闲时间分两种，需要分别诊断，因为对应的修复毫无共同之处：

1. 主机模式空闲。每步三次图重放，图内执行着数百个内核节点，图与图之间的接缝里还有 Python 胶水代码。（是三次重放而非三次前向：草稿图捕获的主体包含全部四次草稿前向，因此自回归草稿循环只花一次重放而不是四次。）如果主机每步循环的耗时超过 GPU 的一步，GPU 就会挨饿。修复办法是隐藏并削减主机工作量。
2. GPU 模式空闲与 GPU 模式开销。主机被隐藏之后，剩下的就是权重带宽（每个 MoE 层每步冷读约 94 MB 被激活的专家权重），加上数百个小内核节点固有的延迟下限。这两者批量 1 都摊销不了。修复办法是 dtype 调整、算子融合，以及启动依赖调度。

<p align="center"><img src="/images/blog/ling3-flash-batch1/03_two_idle_modes.png" alt="Two shapes of idle time at batch 1" width="100%"></p>

*图 4. 两种空闲形态。上：主机循环比 GPU 的工作还长，空洞少而宽，落在图与图之间的接缝处。下：主机被隐藏后，剩下的是数百个 1.5-6 µs 的内核节点——它们的启动下限与自身计算量相当——再加上权重读取本身。*

这两种空闲刻画的是 TPOT 中"步时"的那一侧。另一个杠杆是每步提交多少 token：平均 TPOT ≈ 步时 / 平均接受长度。本文余下部分就沿着这些杠杆展开。主机超前运行与接缝工作消除主机模式空闲；PDL、dtype 调整、融合与重调优缩短 GPU 关键路径；投机参数调优与 DSpark 提高每个目标模型步提交的 token 数。DSpark 后来又回到了第一类问题——一次阻塞式 D2H 读取重新引入了主机阻塞点。

## 先修尺子，再修机器

测量设置的三个特性，决定了下文每一个数字该如何解读。

剖析器会夸大主机侧事件。CUPTI 会给它记录的每个主机事件增加开销。在相同配置下，剖析态测得的步时为 5.2 ms，而从未剖析运行中用 TPOT × 接受长度反推出的真实步时是 4.9 ms。这 0.3 ms 的差距与我们要推理的主机侧效应同一量级，因此剖析态的 trace 可能显示出并不存在的跨 rank 等待。GPU 内核时长来自硬件时间戳，比主机侧计时更可信，但并非无懈可击：追踪仍然会扰动启动时序、并发、缓存状态和 CUDA 图执行，而且 Nsight Systems 文档写明 CUDA 与图节点追踪可能带来显著开销（[用户指南](https://docs.nvidia.com/nsight-systems/UserGuide/index.html)）。因此，这里的每一个主机侧结论都先做了剖析态与未剖析态的校准。

微基准测试对冷权重内核的读数偏乐观。反复调用同一个内核的循环会让它的 2.6 MB 门控权重常驻 L2，而真实模型在同一层的两次相邻调用之间，会用约 94 MB 的专家流量冲刷 L2。热态 7 µs，冷态 11 µs：这足以让它与库版 GEMV 的排名翻转。

峰值吞吐量是单窗口统计量。基准测试的峰值数字是固定 1 秒网格上的最大值，因此带有大约 ±5% 的相位区间：TTFT/TPOT 的偏移会重新切分网格，一项把平均吞吐量提高 2.3% 的改动，打印出来的却可能是从 909 跌到 858。两种读数在固定随机种子下都精确复现，因此可复现性无法把信号与相位区分开。这里的 A/B 决策依据是平均 TPOT × 平均接受长度。这个乘积是步时的推导估计值，而不是直接测量值（两个聚合量的乘积不等于乘积的聚合），但它在多次运行间稳定，且在这些运行中对接受长度漂移不敏感——这正是 A/B 判据所需要的。我们会报告峰值，但从不以峰值为优化目标。

正确性有自己的一道闸门，每项改动在留存前都要过闸：256 token 贪心生成的字节级一致对比；接受长度变化不超过 0.05；以及交错插入温度采样请求后再做一次贪心重跑，以捕捉状态污染。合理改变舍入行为的改动（bf16 门控、单次舍入的 combine）都在提交信息中注明，并以接受长度和任务指标而非位级一致来验证。

## 让主机超前运行

这是整个优化历程余下部分所依赖的结构性改动，属于主机模式空闲的修复。

<p align="center"><img src="/images/blog/ling3-flash-batch1/04_host_run_ahead.png" alt="From lockstep to deep pipelining" width="100%"></p>

*图 5. 从锁步到深度流水线。之前：每一步主机都阻塞在 `resolve_seq_lens_cpu`，等待上一个验证图在 GPU 上跑完，于是超前深度每步都清零，每段主机准备都变成一个 GPU 气泡。之后：队列整整深了一个步，验证 k+1 的启动领先自身执行整整一步，剩下的唯一同步是一个晚一步才被消费的 `copy_done` 事件。*

`cudaGraphLaunch` 一直是异步的，草稿 → 验证 → 扩展在 GPU 上的先后顺序也是免费的：同一条流，FIFO。所以问题从来不是验证要不要等草稿，而是主机是否每一步都被钉在 GPU 进度上。

确实是。在 spec-v2 下，调度器不知道接受长度，因此 `FutureMap.resolve_seq_lens_cpu()` 在构建下一个批次时要把 `new_seq_lens` 从 GPU 拉回来：由一个 publish 事件门控，在私有流上拷贝，然后 `synchronize()`。主机等的不是一次微秒级拷贝，而是上一个验证图执行完毕。代价中位数：每步 485 µs，且超前深度每一步都被清零。

原因是 `needs_cpu_seq_lens` 标志在 spec-v2 涉及的所有后端之间做 OR 叠加。`trtllm_mla` 在全部三种角色里都声明为 `False`；同为线性注意力的姊妹后端 `GDNAttnBackend` 与 `Mamba2AttnBackend` 也都显式声明为 `False`。`KDAAttnBackend` 从未声明过它，于是继承了基类默认值 `True`——尽管它运行的基类元数据代码与那两个姊妹完全相同。

声明 `needs_cpu_seq_lens = False` 让 OR 叠加归零，移除了每步的同步。正确性论证是逐点的：KDA 的元数据从不读取 CPU 镜像，重放的填充量来自 `forward_batch.num_padding`。

主机怎么敢在不知道第 k 步接受结果的情况下就启动第 k+1 步？因为这些数值从不经过 CPU。`FutureMap` 是一个驻留 GPU 的接力站：第 k 步的图把输出 token、`new_seq_lens`、top-k 概率和隐藏状态写入以 `req_pool_idx` 为索引的设备缓冲区，第 k+1 步的图按同一索引读取。主机只处理索引——而索引它本来就知道。

<p align="center"><img src="/images/blog/ling3-flash-batch1/05_run_ahead_slack.png" alt="Where the run-ahead slack lives" width="100%"></p>

*图 6. 余量藏在哪里。面板 A：主机循环（约 4.3 ms）能塞进 GPU 一步（约 4.9 ms）之内，因此被完全隐藏。面板 B：当抖动（一次 gloo 广播或一次 GC 暂停）超出余量时，主机收尾偏晚，GPU 在下一个验证边界处等待，图中第一个集合通信会吸收跨 rank 偏斜。*

超前运行也改变了主机成本的形态。不再是每个 rank 每步都直接支付自己的主机耗时，而是只有耗尽队列余量的那个 rank 才付账。在一次四 rank 的 trace 中，恰好只有一个 rank 处于这种状态：它的调度器段比姊妹长 5-10 倍，草稿图晚启动 40-80 µs，草稿→验证接缝比其他 rank 的中位数高出 165 µs，并周期性出现 400-750 µs 的 GC 特征尖峰。另外三个 rank 在每个汇合点自旋等待它。可以推广的诊断原则：内核的时长不等于它的工作量。一个显示 150-480 µs 的 20 KB embedding all-reduce 并不是慢 all-reduce，而是在吸收偏斜；只有跨 rank 时间对齐才能告诉你哪个 rank 迟到了。

## 收拢接缝

锁步阻塞点消失后，图与图之间的接缝就值得去缩小了。CUDA 图重放之前，步级注意力元数据（kv indices、块表、mamba 状态槽位）必须从活的 `req_to_token` 和 `seq_lens` 重建进图的捕获静态缓冲区。这次重建每步都以 eager 方式运行，构成接缝内容的绝大部分。在 batch 1 下它完全受制于主机：每个 op 花 5-15 µs 派发、1-4 µs 执行。

我们从两个层级下手。第一，融合索引链：`assign_extend_cache_locs_uniform` 把末端偏移的计算搬进内核（均匀的 `draft_token_num` 扩展使跨行前缀和不再必要）；`_fused_state_indices_kernel` 则把一次 gather、一次平移、一次填充哨兵写入和一个 `copy_` 合并成一次启动，并小心保留原有的副作用——包括把填充行的 `req_pool_indices` 清零：函数本身不需要这个清零，但图中其他被捕获的内核依赖它来保证 gather 不越界。

第二，把重建本身捕获进一个以 `(bs, forward_mode)` 为键的小 CUDA 图。它能成立，依托的是重放契约本就保证的一条指针稳定性性质：重放时的 `ForwardBatch` 视图递给后端的只有运行器静态缓冲区和驻留内存池的张量，因此整段准备序列的地址都是固定的。它外围有四重安全机制：两次 eager 预热，确保 Triton JIT 与 autotune 发生在捕获之外；每次重放前恢复各后端 `forward_metadata` 对象的快照（图重放的是设备操作，快照恢复的是 Python 指针）；若捕获失败则永久回退 eager 并给出警告；以及针对填充、TBO、pdmux 与 LoRA 的防护。它以 opt-in 方式随 `SGLANG_ENABLE_METADATA_GLUE_GRAPH` 发布，并在 DFLASH 系投机中被强制禁用，因为那条路径每步都要在主机上重建注意力 plan，捕获重建会把 plan 冻结在捕获时刻。

哪些东西可以捕获，存在一条硬边界。判据是：由纯设备内核组成、只写持久缓冲区的重建可以捕获；任何要走 FlashInfer 风格 `plan()` 的都不行。草稿侧就过不了这一关：多步草稿后端会对主 EAGLE 图已经捕获过的 wrapper 再次 `plan()`，而把这次重新规划录进二级图，会在重放时破坏 wrapper 的内部状态。一个相关的要求是捕获必须幂等。`trtllm_mla` 的 `_init_cuda_graph_metadata` 过去每次调用都会分配新张量并替换自己的 `decode_cuda_graph_metadata[bs]` 条目——二次捕获之后，更早的图会去读已释放的内存。

## PDL：把小内核的延迟下限叠到一起

一个 batch-1 步要在很短的窗口内执行数百个内核节点。在这个尺寸上，启动与前导（prologue）开销几乎与计算本身一样大。程序化依赖启动（Programmatic Dependent Launch，PDL）允许消费者内核在生产者仍在运行时就被调度到 SM 上：消费者先执行所有不依赖生产者输出的部分，只在依赖读取之前，于 `gdc_wait()` 处设置栅栏。

<p align="center"><img src="/images/blog/ling3-flash-batch1/06_pdl_router.png" alt="PDL on the router path" width="100%"></p>

*图 7. 路由路径上的 PDL。没有 PDL 时，每个内核都要等上一个完全退出才启动，门控 matvec 的冷 HBM 权重读取就压在关键路径上。有了 PDL，权重 tile 加载与生产者无关，可以在 `gdc_wait()` 之前发出，2.6 MB 的冷读取就飞进了生产者的尾巴底下；路由器 top-k 也用同样方式预取它的 bias。*

我们接通了三条链：MoE 主链（`moe_align` → up-GEMM → 激活 → down-GEMM → combine → all-reduce）、路由链（norm → 门控 matvec → top-k），以及 KDA 链（`conv1d_update` → 循环 delta 规则 → 门控归一化）。有两个设计要点。

与生产者无关的加载放在 wait 之前。这就是图中全部的技巧，也是对受延迟限制的内核而言，PDL 不止于消除启动开销的原因。

Inductor 内核无法携带 PDL 属性。小 M 的 MoE combine 原本是 `torch.compile` 生成的内核；要加入链，就得把它换成仓库自带的 Triton 归约加 GDC。这带来一个数值副作用：fp32 的 `sum × scale` 只在最后做一次转换，而旧路径舍入了两次。结果略微更精确但非位级相等，提交信息中已声明这一点。

后来，基于在 PTX `griddepcontrol` 中的一个发现，我们升级了语义：`launch_dependents` 只是放行依赖方的启动，而消费者的 `wait` 始终以生产者网格的完全退出作为栅栏。把触发点从生产者末尾移到生产者自己的 wait 之后，可以让消费者的前导与生产者的主体（而不只是尾部）重叠更多；前提条件是：消费者仍必须在提前启动与每次读取生产者输出之间保留自己的 `gdc_wait()`。这是逐个消费者各自的性质，不是一揽子保证，所以我们逐内核核查，转换了其中六个。提前触发能换来什么同样不是确定的：驱动可能提前启动依赖网格，最终兑现多少重叠取决于当时的调度与资源压力（[CUDA 编程指南](https://docs.nvidia.com/cuda/cuda-programming-guide/04-special-topics/programmatic-dependent-launch.html)）。`fused_moe` 以 `M ≤ 512` 检查作为门控：预填充形状下，提前放行一个大的消费者网格会从生产者手中抢走 SM；解码形状下则纯属收益。

PDL 是纯粹的调度语义。累加顺序不变的改动保持位级一致；门控 matvec 以 4/4 全部一致通过了 GDC 开/关位级对比。

## 两次融合与一次重调优

`moe_align`：转到成对轴上。Triton 融合 MoE GEMM 以 `block_size` 大小的 tile 消费 token，tile 内每一行共享同一个专家，而 `moe_align_block_size` 负责构建这一重排。通用路径需要两次内核启动：必须等每个专家的偏移都定稿才能安放任何 token，而这些偏移来自一次全网格扫描，设备级屏障又只存在于内核边界。存在单次启动的变体，但它要把每线程专家计数器暂存在共享内存里，因此最多支持 64 个专家；513 专家的解码一直要付出两次启动的代价。

替换方案工作在成对轴上：一次 [NP, NP] 的成对比较，一步给出每个（token, 槽位）对在所属桶内的稳定序号和该桶的桶员数量；随后由每个桶的 rank-0 代表推导出填充后计数、按桶排序的独占偏移、对外发布的总数，以及逐 block 的专家 id。没有任何开销随专家数量扩展，专家数量上限随之消失。显而易见的替代方案——在填充后的专家轴上（最多 1024 个桶）做直方图与 cumsum——是正确的，但它压在关键路径上的单 SM 工作量约为所替换那两个内核的 3 倍。这正是成对轴在此处成为承重结构的原因。

与参考实现有两处刻意偏离，都以消费者的不变量作为论据：桶内顺序按成对索引保持稳定，而非原子调度顺序（每个对写自己的输出行，消费者与顺序无关）；缓冲区中超出对外发布总数的尾部保持不写（消费者 CTA 在读到它之前就已提前退出）。有一处悬崖：成对张量是 O(NP²) 的。NP=64 时它们完全驻留在寄存器中（约 4 µs，与 CUDA 双内核路径持平）；NP=256 时溢出到本地内存，每次启动约需 230 µs。派发门槛是硬性的 `numel ≤ 64`；更大的批量回退到 CUDA 路径。

SwiGLU 进 up-GEMM epilogue。把 `silu(gate) * up` 折叠进 MoE up-GEMM 的 epilogue，每个 MoE 层省掉一个独立的激活内核，也省掉中间缓冲区整段先写后读的流量。布局技巧是在权重加载时对 `w13` 做逐专家的行交错，让 gate 与 up 落进同一个输出 tile 中相邻的偶/奇列。由于 GEMM 的每个输出列都是独立的点积，交错在位级上是中性的。

位级一致是心思花得最多的地方。被替换的内核是以 `-use_fast_math` 编译的，因此 epilogue 逐条指令复刻它的行为：`__expf` 对应 `mul` + `ex2.approx.ftz`，除法用 `div.approx.ftz`，乘积只在最后舍入一次。微妙之处在于：FlashInfer 以 `float` 实例化激活函子，因此 silu 在乘法之前从不落回 bf16。若在那里先舍入一次，结果就会双重舍入，并在相当大比例的输入上出现偏差。这种偏差在文档里看不见，容差检查也抓不到；必须对整个输入范围做逐元素位比较。

KDA 链验证的 tile 经济学。融合的 conv1d + 门控 delta 规则验证内核早已存在；这几笔提交是对它做了重新调优。在图内计时、轮转冷态测试下，Blackwell 在 T=6 的曲线是单调的：BV=4 为 11.56 µs，8 为 12.53，16 为 12.83，32 为 14.26，64 为 20.7，128 为 38。BV=4 每次调用最多胜出 19%，因为 256 个 CTA 折合 148 个 SM 上的 1.7 个波次，把 q/k 卷积复制 32 份仍比缩短串行链更便宜。对 V 维做 tile 划分从不触碰 K 维的归约顺序，因此在 `num_warps=4` 下每个 BV 都与基线位级一致，重调优没有数值风险。

## bf16 路由门控与 lm_head

结构性改动之后最大的一项单体改动是一次 dtype 调整。在 batch 1 下，路由门控与 lm_head 是纯带宽负载：每个解码步都要冷读每个 MoE 层的门控权重（bf16 下 2.6 MB）和词表并行的 lm_head 投影，而两者都没有计算可以把读取藏在其后。把两者从 fp32 改成 bf16 运行，字节数减半；端到端收益约 +10%，是主机超前运行修复之后任何单项改动的最大增益。与上文其他舍入类改动一样，这一改动也在提交信息中注明，并以接受长度和任务指标而非位级一致来验证。

## 投机解码下的 KDA

一个被拒绝的投机 token 只会让某个 KV 缓存条目无害地过时，但它已经原地污染了一个循环状态。线性注意力与投机并不是免费共存的。

让它可行的方案是：验证期间，循环在关闭状态更新的情况下运行，把每个链位置的后置状态写进中间缓冲区；判定之后，`commit_mamba_states_after_verify` 把属于最后一个被接受位置的状态拷贝进持久槽位。先暂存，再提交。这也是紧凑投机缓存只支持 `topk=1` 的原因：链状时，被接受的前缀是唯一的，状态可以按位置索引；树状时，被接受路径只是众多路径之一，状态就得按树路径索引。

剖析显示 KDA 解码受带宽限制，主要是 K×V 状态上的 HBM 流量，所以除了融合和 tile 重调优之外，那里已经没有多少油水。我们没有把实际达到的带宽与 Blackwell 峰值对比，因此请把它当作形状层面的观察，而不是 roofline 结论。

## batch 1 下投机的经济学

权重带宽占主导有一个反直觉的推论：多验证几个 token 几乎免费。验证 4 个 token 和验证 6 个 token 读的是完全相同的权重。在 batch 1 下加深投机，每加深一步只多花一次廉价的草稿前向（草稿只有单层），外加 KDA 链验证循环里的增量串行成本，换来的是接受长度。

我们没有想当然，而是做了扫描（这次扫描早于融合包落地；如下文所述，最优点后来移动了）：

| steps / draft tokens | 接受长度 | 平均 TPOT | 步时（推导值） | 稳态 tok/s |
|-|-|-|-|-|
| 3 / 4 | 3.11 | 1.51 ms | 4.70 ms | 662 |
| **4 / 5** | **3.37** | **1.45 ms** | **4.89 ms** | **690** |
| 5 / 6 | 3.45 | 1.55 ms | 5.35 ms | 645 |

步时一列是 TPOT × 接受长度，是推导估计值而非直接测量。每加一步约付出步时的 4-9%，而边际接受增益按几何级衰减（d5 → d6 只增加 0.08）。打平条件大致是 `Δaccept > 0.05 × accept`。最优点还会移动：融合包落地、步时下降之后，`(5, 6)` 成为更优配置；等 fp8 权重进一步压低固定基础开销后，还需要再做一轮扫描。

## DSpark：高质量块级草稿

调 NEXTN 的深度是在固定形状算法上拧的一维旋钮。更大的杠杆是换掉算法。优化的下半场就投入到把 DSpark 带到同一个目标模型上，并给它同样的 batch-1 待遇。

### DSpark 做了哪些不同的事

DSpark 算法本身是公开的。这里的工作，是把这份公开配方适配到 Ling-3.0-flash、长上下文在线蒸馏与 batch-1 Blackwell 服务栈上。我们的适配有四点不同。

分布对齐的数据。我们主要在 Ling-3.0-flash 后训练数据上蒸馏，让草稿模型在它服务时将要面对的分布上训练。蒸馏过程中我们还使用了多种采样设置，以提升轨迹多样性以及在投机解码下的鲁棒性。

消融驱动的草稿设计。我们没有直接继承 Ling-3.0-flash 架构，而是对关键草稿选择做了系统性消融，包括是否复用 Ling-3 的注意力结构、使用哪种 RoPE 变体（partial 还是 interleaved）。我们保留了接受长度/延迟权衡最优的设计。

与服务耦合的在线训练系统。面向长上下文与大规模在线训练，我们构建了 SplitServe Trainer——一个单节点 8 GPU 框架，把资源在训练与 SGLang 推理之间对半分配。训练期间，推理侧运行目标模型前向，为草稿生成诸如目标隐藏状态之类的监督信号。这让生成-训练循环保持在本地，削减 IO 开销，提高长上下文负载的训练效率。

<p align="center"><img src="/images/blog/ling3-flash-batch1/07_splitserve_trainer.jpg" alt="SplitServe Trainer layout" width="100%"></p>

*图 8. SplitServe Trainer 布局。*

接受感知的优化。在公开的 DSpark 损失设置之上，我们加入了一个与接受长度相关的损失，让草稿不只为了 token 级和中间目标的对齐而训练，也为了在目标模型验证下获得更长的被接受前缀而训练。

<p align="center"><img src="/images/blog/ling3-flash-batch1/08_acceptance_optimization.jpg" alt="Acceptance-aware optimization" width="100%"></p>

*图 9. 接受感知优化。*

### 47% 的空闲，以及背后的机制

在 Blackwell TP4、batch 1 下的第一份 DSpark trace——覆盖 239 个稳态解码迭代——与 NEXTN 路径已达到的状态相去甚远。步时中位数 10.62 ms，其中 GPU 空闲 4.99 ms（占 47%）。

空闲并不在 CUDA 图内部：3 秒里图内微小间隙合计只有约 80 ms。它全在图与图之间的 eager 段里，表现为每步四五个 100 µs 到 2 ms 的中等间隙。

两个 FlashInfer `plan()` 实现——fa2 的 `BatchPrefillWithPagedKVCacheWrapper` 与 MLA wrapper——被喂入的是设备张量，而它们内部会对 `qo_indptr`、`kv_indptr`、`kv_len_arr` 各自做一次阻塞式 `.to("cpu")`。一次阻塞式 D2H 会等待流上全部在途工作，包括仍在执行的草稿图。于是每一步，CPU 都在草稿启动后立即被钉在 GPU 进度上；约 1 ms 的 `cudaGraphLaunch` CPU 开销再没有 GPU 忙碌窗口可供藏身；调度器尾部又在两者之后串行。

结构上看，这是 `resolve_seq_lens_cpu` 钉扎的又一次重演：主机侧对设备驻留数值的阻塞读取，每步把超前深度清零——而且出现在一个不相干的子系统里。它提示的法则：在 batch 1 下，做任何事之前先排查主机路径上对设备数值的阻塞读取，因为每一处都会把整个主机循环从被隐藏的工作变成一个 GPU 气泡。

### 由主机供数的 plan

那三个数组本来就不必来自设备。DFLASH 家族保证验证与草稿的 `ForwardBatch` 携带 `seq_lens_cpu = prefix + draft_token_num`——这一点在三个独立的调用点都有断言——且它恰好等于设备侧路径算出的 kv 长度。主机早就知道自己卡着等读回的答案是什么。

- fa2 侧。捕获时，在按批量大小区分的目标验证 wrapper 上安装 `fast_prefill_plan`，以 DFLASH 验证输入类型作为门控，从而完全不触及 EAGLE 的目标验证；再加一条断言：不存在自定义掩码（fast plan 不支持自定义掩码；DFLASH 从不携带）。
- MLA 侧。以 `seq_lens_cpu` 在纯主机算术里构建 plan kwargs，零 D2H；通过新增的 `kv_indices_buf` 参数把 `kv_indices` 直接写进 wrapper 的 CUDA 图缓冲区；然后调用 `fast_mla_decode_plan(causal=True)`，跳过三次阻塞 D2H 与四次设备缓冲区刷新。捕获时仍会运行真正的 `plan()`——正是它负责填充缓存模块和 wrapper 的缓冲区。

另外两处修复不需要额外工作。`graph.replay()` 本来就是纯入队操作；除了横在中间的那次 D2H，没有任何东西阻止 CPU 把草稿图 → 验证准备 → 验证图背靠背排进队列。移除它之后，验证元数据准备与两次图启动会在草稿图仍在执行时即已入队，两个图在 GPU 上背靠背运行。

### 结果

在组合任何东西之前，每个环境开关都先单独做了 A/B：

| 开关（逐项单独测量） | 接受长度 | 平均 TPOT | 结论 |
|-|-|-|-|
| 无（重叠调度开，基数树缓存关） | 4.49 | 1.48 ms | 干净基线 |
| `SGLANG_OPT_FUSED_KDA_VERIFY=1` | 4.68 | 1.34 ms | 安全，保留 |

开关级别的轨迹，固定投机配置，全部为 8192 输入 / 1024 输出、并发 1：同步调度 1.67 ms → 关闭基数树缓存的重叠调度 1.48 ms（调度器尾部的空闲窗口从 1118 µs 坍缩到 85 µs）→ 融合 KDA 验证 1.34 ms。

最终部署配置在并发 1 下对 1000 个请求测得：接受长度 9.95，平均 TPOT 0.78 ms，TPOT 中位数 0.51 ms，输出吞吐量 1120 tok/s，峰值 1945 tok/s。9.95 的接受长度是用 block_size 16 的 DSpark 草稿测得的；发布的草稿检查点使用 block_size 8。DSpark 不接受 speculative-num-steps / draft-tokens 这类开关；它们只适用于 NEXTN。

TPOT 中位数乘以平均接受长度得 0.51 × 9.95 ≈ 5.1 ms，与更早那份 trace 测得的步时（KDA 融合之前总计约 5.3 ms）接近。这只能当作一个粗略的一致性检查：它把中位数与均值混在一起，面对这么宽的分布，它并不是步时中位数。要把这个数闭合，就得直接从 trace 测步时，而 DSpark 配置我们还没有做。这份 trace 能支持的是定性结论：主机又一次让开了路，剩下的都在 GPU 上。

## 如今时间花在哪里

<p align="center"><img src="/images/blog/ling3-flash-batch1/09_final_step_breakdown.png" alt="One decode step after the campaign" width="100%"></p>

*图 10. 本轮优化结束后的一步 NEXTN 解码。*

MoE 分组 GEMM 1215 µs；路由 / 激活 / 胶水小内核 1127 µs；all-reduce 951 µs；稠密 GEMM 918 µs；KDA 488 µs；8k 上下文下的 MLA 注意力 244 µs；另有 400 µs 残余空闲。主机被完全隐藏；剩下的是 GPU 工作，而权重带宽在其中占主导。

这份清点对应的是 NEXTN 配置；DSpark 会重新分配这一步（更宽的验证窗口、第二个草稿模型图），但不改变结论。

8k 上下文下的 MLA 注意力只有 244 µs。长上下文在这里不是问题——这正是混合架构带来的结果。MoE 加稠密 GEMM 合计约 2.1 ms，其中几乎全是权重带宽。

因此路线图很短：

1. fp8 权重是剩下的那个大杠杆。在 2.1 ms 的带宽受限工作上把字节数减半，是结构性的 15-20% 收益，远在该指标的噪声带之外。接受长度的对策已有现成方案（bf16 草稿），块量化的 TP 约束也是已知：`moe_intermediate_size = 768`、块大小 128 时，TP4 不可行，需要 `--ep-size 4`。
2. 路由器融合已经到达它合理的终点。把门控 matvec 折进 top-k 内核会把并行度从 129×M 个 CTA 坍缩到 M/BLOCK_M。PDL 链接就是这条路径上正确的停脚点。
3. 主机环境工程。给调度器进程做核心绑定与 GC 调优——这实质上是守护超前运行余量的手段，而不是内核优化。

## 复现

```bash
SGLANG_ENABLE_METADATA_GLUE_GRAPH=1 \
SGLANG_OPT_FUSED_KDA_VERIFY=1 \
SGLANG_ENABLE_FUSED_VERIFY_EXTEND_GRAPH=1 \
python3 -m sglang.launch_server \
  --model-path inclusionAI/Ling-3.0-flash \
  --tp-size 4 --trust-remote-code \
  --speculative-algorithm NEXTN \
  --speculative-num-steps 5 \
  --speculative-eagle-topk 1 \
  --speculative-num-draft-tokens 6 \
  --attention-backend trtllm_mla \
  --flashinfer-allreduce-fusion-backend auto \
  --mem-fraction-static 0.85
```

对于 DSpark 配置，把投机相关开关换成 DSpark 草稿检查点：

```bash
SGLANG_OPT_FUSED_KDA_VERIFY=1 \
python3 -m sglang.launch_server \
  --model-path inclusionAI/Ling-3.0-flash \
  --tp-size 4 --trust-remote-code \
  --speculative-algorithm DSPARK \
  --speculative-draft-model-path inclusionAI/Ling-3.0-flash-dspark \
  --attention-backend trtllm_mla \
  --flashinfer-allreduce-fusion-backend auto \
  --disable-radix-cache
```

两种配置都用同样的方式做基准测试：

```bash
python3 -m sglang.bench_serving --backend sglang \
  --dataset-name random --num-prompts 1000 \
  --random-input-len 8192 --random-output-len 1024 \
  --random-range-ratio 1.0 --max-concurrency 1
```

## 致谢

本工作是 RadixArk SGLang 团队与 Ant Ling Infra 团队的合作成果。感谢 DeepInfra 和 Novita 在 SGLang 上服务 Ling-3.0-flash。

Ant Ling Infra 团队，蚂蚁集团（按姓氏字母排序）：Tiwei Bie, Yuan Luo, Dayu Qiu, Jianfeng Tan, Tongli Wang, Yue Yu, Kaihong Zhang。inclusionAI 团队，蚂蚁集团（按姓氏字母排序）：Xiang Cao, Guoshan Lu, Junbo Zhao。
