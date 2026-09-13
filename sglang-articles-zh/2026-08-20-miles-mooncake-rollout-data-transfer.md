---
title: "Mooncake 赋能 Miles：从碎片化 rollout 数据到高效批量 I/O"
title_en: "Mooncake for Miles: From Fragmented Rollout Data to Efficient Bulk I/O"
author: "Mooncake community"
date: "August 20, 2026"
previewImg: /images/blog/miles-mooncake-rollout-data-transfer/featured.png
source: https://lmsys.org/blog/2026-08-20-miles-mooncake-rollout-data-transfer/
translated: 2026-09-12
---

# Mooncake 赋能 Miles：从碎片化 rollout 数据到高效批量 I/O

> 原文：[Mooncake for Miles: From Fragmented Rollout Data to Efficient Bulk I/O](https://lmsys.org/blog/2026-08-20-miles-mooncake-rollout-data-transfer/) · LMSYS Blog · Mooncake community

## 分离式 RL 系统中的 rollout 数据

大语言模型的强化学习结合了两类截然不同的负载：**rollout 生成**与**模型训练**。

在 rollout 阶段，推理 worker 在一批提示词上运行当前策略并生成回复。在此过程中，它们还会产生学习算法所需的信息，包括生成的 token、掩码、对数概率、奖励、序列长度、样本标识符以及其他元数据。这些输出共同构成了下一步训练所要消费的 **rollout 数据**。

在小规模场景下，生成与训练可以共享同一执行环境。但在更大规模下，现代 RL 系统越来越多地采用**分离式架构（disaggregated architecture）**：rollout 生成与训练作为相互独立的 worker 组部署，往往分布在不同进程、GPU 甚至不同机器上。

这两个阶段在资源与执行特性上有着根本差异：rollout 是以推理为主的负载，其吞吐量取决于解码效率、批处理与请求调度；而训练依赖大规模、高度同步的张量计算。将二者分离，可以让每一侧独立地进行扩缩容与调度，而不必把两种负载硬塞进同一种执行模式。

这种分离还使**流水线级并发**成为可能：Miles 可以在训练 rollout *N* 的同时，让 rollout worker 已经开始生成 rollout *N+1*。因此，异步 RL 系统可以让 rollout 与训练 worker 以各自的节奏推进，而不必让某个阶段在每次操作之后都等待另一个阶段。

其收益是更高的资源利用率，以及在规划推理与训练算力时更大的灵活性。但分离式架构也引入了一道新的系统边界：**rollout worker 产生的数据必须先移动到另一组 worker，训练才能消费它**。

这道交接环节恰好位于生成与下一次策略更新之间。传输一旦变慢，训练器就得干等数据，rollout worker 上的内存也会被占用超过必要的时间。因此，对 Miles 这样的分布式 RL 系统而言，如何高效地将这份**结构化 rollout 数据从推理侧搬运到训练侧**，成为端到端 RL 流水线中的重要一环。

## RL rollout 数据传输为何具有挑战性

RL rollout 数据与分布式训练中常见的那类大而规整的张量有很大不同。

一个 rollout 批次通常是**异构的结构化对象**，而不是单个连续张量。根据框架和算法的不同，它可能包含生成的 token、损失掩码、对数概率、奖励、序列长度、样本标识符、路由信息、元数据以及其他辅助字段。这些值可能以张量、NumPy 数组、Python 标量列表、每样本长度不一的数组、字节串或任意 Python 对象的形式表示。

有几个特性使得这类数据很难被高效搬运。

**挑战 1：异构的数据类型与复杂的语义**

不同的 rollout 字段在表示与语义上有本质差异。稠密张量与数值数组可以作为类型化缓冲区高效传输；而变长（ragged）序列需要行边界信息，标量列表需要保留原始取值，元数据或 Python 对象则可能需要更通用的编码。与此同时，训练器必须精确重建 RL 框架所期望的结构，包括 dtype、shape、行序、空值状态与元数据。通用序列化器在功能上可以处理这些对象，但往往以额外的转换、拷贝和重建为代价。因此，高效的 rollout 传输需要同时理解每个字段的物理表示与逻辑结构。

**挑战 2：高度碎片化的内存布局**

rollout 数据可能包含数量极其庞大的小内存分配。在采集到的 Miles 负载中，tokens、loss_masks、rollout_log_probs 等主要字段都以 list[np.ndarray] 形式表示，每个样本各分配一个 NumPy 数组。随着批次规模增大，逐个传输这些碎片会带来反复的内存注册与 Store 操作，而把完整 Python 对象整体序列化则需要遍历、拷贝并重建一个庞大的对象图。挑战在于：如何在不丢失原始结构的前提下，把碎片化的逻辑数据转化为高效的批量传输。

这两个挑战叠加起来，意味着 rollout 数据的搬运远不只是带宽问题：系统必须在保留结构的同时，高效地移动碎片化的异构数据。

一条有效的数据通路需要同时满足以下几项要求：

* **效率：** 避免过度的序列化、拷贝、对象重建以及逐分配的传输开销。
* **正确性：** 在整个往返过程中保留字段类型、形状、行边界、空值状态、元数据以及 Python 层面的取值。
* **可扩展性：** 在样本数、对象碎片数与总负载规模增长时依然保持良好性能。
* **灵活性：** 支持异构字段，而不强迫 RL 框架展平或重写其原生的 rollout 表示。
* **可预期的交接延迟：** 足够快地交付批次，使训练器不会因等待 rollout 数据而停顿。

## 用 Mooncake 驱动 Miles 的 rollout 数据传输

**Miles** 是一个面向大规模模型后训练的高性能强化学习框架。它将 **SGLang 用于高吞吐 rollout 生成**、**Megatron-LM 用于可扩展训练**，并为偏好直接训练 Hugging Face 模型实现的负载提供 PyTorch FSDP2 后端。Miles 支持完全异步的 RL——rollout 与训练 worker 解耦、可独立推进——同时具备训练回路内快速权重更新、agentic rollout、低精度训练，以及面向大规模生产级 RL 负载的容错等特性。

这种分离式、异步化的设计，使得 rollout 到训练的数据通路成为 RL 流水线中的关键环节。rollout 批次是结构化且异构的，往往包含碎片化的逐样本数据与框架特有的元数据；随着负载规模增长，高效的传输与重建变得愈发重要。

**Mooncake** 为分布式 AI 负载提供高性能数据面。针对 RL rollout 数据，它在该数据面上扩展出了结构化对象传输能力，使异构且碎片化的 rollout 对象能够在保留原始结构与语义的前提下被搬运。

Mooncake 现已集成到 Miles 中，作为 rollout 数据传输后端。在从 Miles 采集的 rollout 数据上，这一集成带来了显著低于现有 Ray 路径的传输延迟：远程 GET 大约快 **10–14×**，PUT 则提升约 **1.2–1.6×**。

其结果是在不改变 RL 编程模型的前提下，实现更快的 rollout 到训练交接，为 Miles 的大规模结构化 rollout 负载提供了一条更高效的数据通路。

## rollout 数据如何在 RL 流水线中流转

Miles 同时支持同步与异步训练循环。无论哪种模式，只要 rollout worker 与训练器部署在相互独立的进程或不同机器上，每个完成的 rollout 批次都必须跨越这一边界，才能被下一步训练消费。

一个有用的设计原则是将**控制面**与**数据面**分离。框架调度器决定 rollout 批次应该去往何处，但不应自己搬运大块负载；它只传递一个轻量的传输引用，其中不包含张量负载与 Store 分块布局，同时在需要时仍可附带 JSON 安全的元数据。实际的 rollout 负载则走另一条路径：

* 框架调度器传递传输引用；
* Mooncake 负责存储与传输负载；
* 训练 worker 在执行训练步骤前重建原始对象；
* 所有读取方完成后，框架移除短生命周期的 Store 对象。

这种分离让调度决策保持轻量，同时让大块 rollout 负载经由专用的数据通路传输。

### Miles 实际传输的内容

从 **Miles** 采集到的 rollout 数据让这条数据通路变得具体。对于给定的框架配置，字段契约是稳定的，但各字段并不共享同一种便利的内存表示。它们大致可归为三类：

| 字段组 | Miles 中的表示 | 传输关注点 |
| --- | --- | --- |
| Token、掩码与对数概率行 | 每样本数值行 | 大量彼此独立的行对象；长度可能因样本而异。 |
| ID、长度、奖励与标志位 | Python 标量列表 | 字节数很小，但训练必需。 |
| 可选与对象元数据 | Python 值、张量字典或嵌套对象 | 保留结构、空值以及特性启用状态的语义。 |

在我们的采集中，第一类字段占据了绝大部分字节。其余字段更小，但既不能丢弃也不能归一化掉：它们承载着样本标识、长度、奖励、特性状态以及簿记信息。其确切大小取决于具体负载；基准测试一节给出了一个实测示例。

### Miles 采用完整字典交接（Completed-Dict Handoff）

在 **Miles** 中，当前的交接从完整的 rollout 字典就绪之后开始：生产者调用 `put(data, type="dict")`，调度器携带返回的引用，训练器则调用 `get` 来重建原始字典。

<center>
<img src="/images/blog/miles-mooncake-rollout-data-transfer/rollout-data-plane.svg"
     alt="Synchronous rollout transfer for Miles"
     style="width:60%; max-width:1100px"/>
</center>

*图 1：Miles 对完整的 rollout 字典使用同步的 `put` 和 `get`。引用经调度器传递，而 Mooncake 通过 Store 数据面搬运负载。*

单次传输调用是同步的：生产者要等 `put` 完成后才返回引用，训练器也要等 `get` 结束后才消费该对象。

这并不妨碍 RL 流水线本身是异步的：Miles 可以在训练 rollout *N* 的同时生成 rollout *N+1*。换言之，并发位于传输操作之上——每一次单独的交接都是同步的，但不同的 rollout 与训练阶段可以在流水线层面重叠进行。

## Mooncake 如何保留并传输 Miles 的 rollout 数据

Mooncake 在不同层次上应对这两个挑战。它先让结构保持可见足够长的时间，以便为每个字段选择高效的表示：张量与数组保持类型化，变长行携带紧凑的边界元数据，Python 值则保留 GET 重建它们所需的全部信息。随后，它将碎片化的内存转化为批量 I/O：一份拷贝计划把符合条件的小行直接打包进可复用的、已注册的 BufferPool chunk，而大型连续张量与数组可以走原生 Store 路径。这样就避免了两个极端——要么把整个字典序列化成一大块不透明的数据，要么为每一次小内存分配都发起一次 Store 操作。

生成的负载成员作为一个 bundle（捆绑包）发布。其清单（manifest）记录了这些成员存放的位置以及彼此如何拼装，并且只有在负载就绪后才对外可见。GET 按这份描述反向执行，取回并重建原始的 Miles 字典。Miles 仍使用那个很小的公共接口——`put(data, type="dict")` 与 `get(ref, type="dict")`；schema、字段布局、传输计划与重建逻辑都留在 Mooncake 内部。

<center>
<img src="/images/blog/miles-mooncake-rollout-data-transfer/structured-transfer-architecture.svg"
     alt="Mooncake structured-object transfer architecture"
     style="width:70%; max-width:1100px"/>
</center>

*图 2：Schema 与叶子展开揭示每个字段的类型与结构。针对字段的编码生成带类型的负载成员与重建元数据；Bundle Store 最后发布它们的清单。符合条件的碎片化传输使用基于 BufferPool 的暂存，GET 则按相同的结构反向执行。*

### 为每个字段选择合适的布局

Mooncake 首先把字典展开成可高效编码的叶子节点：数组与张量保持类型化，变长行携带紧凑的边界元数据，受支持的 Python 值保留重建所需的全部信息。对于含义模糊或对性能敏感的字段，由框架提供的 schema 固定其存储表示；未提供 schema 时，Mooncake 会从观测到的取值中推断出一个。

同样的选择逻辑也适用于多模态数据。处理后的像素与相关模型输入可以继续走张量路径；PIL 图像、编码后的 PNG/JPEG 字节以及变长的媒体列表则使用面向媒体的布局，保留它们的边界与重建元数据，而不强迫所有表示都挤过同一个序列化器。

### 将碎片化内存转化为批量 I/O

逐行单独发送会产生成千上万次注册与 Store 请求；先把整个字段拼接起来虽然能避免这些请求，却会引入一份全尺寸的临时副本。Mooncake 的做法是构建一份拷贝计划，按需填充可复用的、已注册的 BufferPool chunk。其原生路径把符合条件的数值行直接拷贝进这些 chunk，避免了 Python 层面的逐行循环和临时拼接。大型连续数组与张量在 Store 支持时仍走直接或原生路径。

### 发布完整 bundle 并直接重建

Mooncake 只有在全部负载与元数据就绪后才发布 bundle 清单，因此读取方永远不会看到写了一半的 Miles 字典。执行 GET 时，清单标明需要取回哪些成员，结构化元数据则描述如何重建每个字段。符合条件的读取可以直接以基于 BufferPool 的目的地为目标，无需经过中间的 `bytes` 对象；带类型的变长行还可以直接以视图方式访问结果缓冲区。

训练器在使用完毕后释放本地基于 BufferPool 的结果。所有读取方结束后，Miles 移除短生命周期的 Store 对象，Mooncake 则回收其负载 chunk 与清单。

<center>
<img src="/images/blog/miles-mooncake-rollout-data-transfer/challenge-response.svg"
     alt="Rollout data challenges and Mooncake optimizations"
     style="width:50%; max-width:1100px"/>
</center>

*图 3：Miles rollout 数据的两大挑战与 Mooncake 的结构化编码及批量传输优化一一对应。*

## 性能结果

对于固定的框架配置，更换模型本身并不会改变字段契约。传输规模取决于样本数量、提示词与响应的长度，以及诸如教师模型对数概率、路由信息或多模态输入等可选字段。

### 基准负载

Miles 使用 Qwen3-0.6B 在数学类提示词上生成了源数据（`rollout_id=0`，8 个源样本）。本次采集中的每条响应都是 256 个 token。为构造基准负载，三个较大的数值字段被规范化为带类型的 ndarray 行，同时保留其取值、行长度、dtype 以及逐样本的碎片化形态。对这些样本取平均后，逻辑负载的构成如下：

| 单个采集样本的组成部分 | 计算方式 | 逻辑字节数 |
| --- | ---: | ---: |
| `tokens` | 提示词加响应的平均 token 数 x 4 B（`int32`） | ~1,338 B |
| `loss_masks` | 256 项 x 4 B（`int32`） | 1,024 B |
| `rollout_log_probs` | 256 项 x 4 B（`float32`） | 1,024 B |
| 标量与对象字段 | ID、长度、奖励、标志位与版本元数据 | ~36 B |
| **总计** | | **~3,422 B** |

前三个字段合计约 3,386 字节，占这种样本布局的 98.9%。更大的基准负载通过重复这 8 个采集样本构造而成，在增加逻辑样本数的同时，保持字段类型与碎片化的分配模式不变。上述计算描述的是本次采集，并不代表 Miles 固定的样本大小。

<center>
<img src="/images/blog/miles-mooncake-rollout-data-transfer/rollout-object-anatomy.svg"
     alt="Miles rollout object anatomy"
     style="width:50%; max-width:1100px"/>
</center>

_图 4：Qwen3-0.6B 基准采集中单个样本的实测构成。_

### 传输结果

该基准测试度量的是 Miles 所使用的完整扁平字典交接，并将 Miles 的 Ray 后端与 Mooncake 结构化对象传输进行对比。

PUT 是生产者装载负载之后的一次计时的后端调用；GET 取一次预热后三次远程消费者试验的平均值。引用序列化与调度器交接不计入计时区域。这些数字只覆盖负载传输与重建，不代表端到端训练吞吐量。

在所测试的负载规模范围内，Mooncake 让 Miles 的 GET 比 Ray 后端快约 10–14 倍；PUT 提升约 1.2–1.6 倍。

<center>
<img src="/images/blog/miles-mooncake-rollout-data-transfer/miles-get-latency.svg"
     alt="Miles GET latency benchmark"
     style="width:40%; max-width:1100px"/>
</center>

_图 5：对于这种碎片化的 Miles rollout 布局，Mooncake 的 GET 快约 10–14 倍。纵轴为对数坐标。_

PUT 的提升相对较小。其计时路径包含 Python 对象遍历、变长行打包、元数据与清单构建，以及负载传输。GET 在这一负载上的改善幅度更大，而且训练器必须在开始训练步骤之前完成 GET。

## 下一步计划

Miles 集成奠定了基础数据通路。下一步的优先事项是与 Miles 社区一起，在更广泛的真实 RL 负载上对其进行验证。

- **验证更多模型与负载。** 我们将把验证扩展到多模态与 VLA 负载、智能体强化学习（agentic RL）、世界模型训练，以及面向视频生成或扩散模型的强化学习。由于这些负载以不同方式组合了媒体、轨迹、动作、奖励与中间状态，每类负载都会用真实的 rollout 数据和端到端训练来验证其正确性、兼容性与传输性能。
- **将 rollout 数据与 KV 缓存负载隔离。** Mooncake 需要为短生命周期的 rollout 数据与 KV 缓存数据建立独立的计量、配额与逐出策略，以免 rollout 流量的突发把对延迟敏感的缓存条目逐出。

## 致谢

这项工作跨越了多个代码仓库，评审与验证同样如此。我们感谢 Xinpeng Zhao（[@zxpdemonio](https://github.com/zxpdemonio)）、Teng Ma（[@stmatengss](https://github.com/stmatengss)）、Xingyuan Wu（[@yokinoshitayoki](https://github.com/yokinoshitayoki)）、[@fzyzcjy](https://github.com/fzyzcjy)、[@guapisolo](https://github.com/guapisolo)、Xuchun Shang（[@XucSh](https://github.com/XucSh)）、Bo Gao（[@Bo-Vincent](https://github.com/Bo-Vincent)）、He Zhou（[@ehuohz](https://github.com/ehuohz)）和 Yufeng He（[@he-yufeng](https://github.com/he-yufeng)），他们在 Mooncake 实现与评审、Miles 集成与验证，以及设计反馈、评审与测试等方面做出了贡献。

## 相关链接

- Mooncake 项目：[https://github.com/kvcache-ai/Mooncake](https://github.com/kvcache-ai/Mooncake)
- Mooncake 文档：[https://kvcache-ai.github.io/Mooncake/](https://kvcache-ai.github.io/Mooncake/)
- Miles Mooncake rollout 传输用户指南：[radixark/miles#2535](https://github.com/radixark/miles/pull/2535)
