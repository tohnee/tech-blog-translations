---
title: "SGLang 的流水线并行：扩展至百万 token 上下文及更长"
title_en: "Pipeline Parallelism in SGLang: Scaling to Million-Token Contexts and Beyond"
author: "Shangming Cai"
date: "January 15, 2026"
previewImg: /images/blog/chunked_pipeline/preview_cpp.jpg
source: https://lmsys.org/blog/2026-01-15-chunked-pipeline/
translated: 2026-09-12
---

# SGLang 的流水线并行：扩展至百万 token 上下文及更长

> 原文：[Pipeline Parallelism in SGLang: Scaling to Million-Token Contexts and Beyond](https://lmsys.org/blog/2026-01-15-chunked-pipeline/) · LMSYS Blog · Shangming Cai

## **TL;DR**

我们很高兴推出 SGLang 经过高度优化的流水线并行（PP）实现，专为应对超长上下文推理的挑战而设计。通过融合**分块流水线并行（Chunked Pipeline Parallelism）**、**异步 P2P 通信**，以及一个简单而有效的**动态分块（Dynamic Chunking）机制**，这一 PP 设计在实现业界领先性能的同时，还能与其他并行策略、PD 分离（预填充-解码分离）以及 HiCache 无缝兼容。在多节点部署中，当分块预填充大小设为 12K 时，采用该实现扩展到 PP4 TP8，在 H20 集群上为 DeepSeek-V3.1 带来了相对 TP8 **3.31 倍的预填充吞吐量**，并以 **30.5% 的领先幅度**显著超越 TP32 方案（2.54×）。这凸显了 PP 在大规模跨节点扩展上相对纯 TP 的固有架构优势。此外，该实现还能将 TTFT 最多降低 **67.9%**，同时保持 **82.8% 的强扩展效率**，为超长上下文场景下扩展万亿参数模型提供了一条高效的开源路径。

<img src="/images/blog/chunked_pipeline/ds_throughput.png"
     alt="Prefill Throughput (Batch Size = 1) of DeepSeek-V3.1 on H20 (Higher is better)"
     style="display: block; margin: 20px auto 0; width: 75%; max-width: 100%; height: auto;">

<p style="color: black; text-align: center; font-size: 0.9em;">DeepSeek-V3.1 在 H20 上的预填充吞吐量（Batch Size = 1，越高越好）<br> 注：DCK 12288（σ=0.65）表示启用动态分块（Dynamic Chunking），初始分块预填充大小设为 12K，平滑因子设为 0.65。</p>

<div style="border-left: 4px solid #3b82f6; padding: 10px 12px; margin: 12px 0; background: #eff6ff; border-radius: 8px;">
  <strong>👉 查看 <a href="https://github.com/sgl-project/sglang/issues/11857">PP 路线图</a>。</strong>
</div>

## **引言**

随着大语言模型（LLM）向万亿参数架构和"无限"上下文窗口演进，底层推理服务基础设施也必须转向更细粒度的跨节点并行化策略。虽然 KV 缓存（KV cache）技术有效缓解了冗余计算问题，却无法规避超长序列（初始输入 token 长度（ITL）极大）固有的高昂首 token 延迟（TTFT）。张量并行（TP）虽仍是节点内扩展的常规手段，但在多节点部署中频繁遭遇通信瓶颈。另一方面，传统流水线并行（PP）虽然通过减少通信量化解了这一瓶颈，但在处理此类超长提示词时，难以避免资源利用不足和流水线气泡（bubble）开销的问题。

借鉴开源创新与学术研究的成果，SGLang 推出了一套高度优化的流水线并行实现，以异步通信和动态分块预填充为核心特性，有效将流水线气泡降至最低。通过整合这些技术，SGLang 重新探索并定义了超长提示词的处理方式——切实"扩展掉"了长序列预填充令人望而却步的延迟，将其转变为高吞吐、计算可扩展的流式工作流。

实证基准测试表明，SGLang 的 PP 实现达到了业界领先水平。在大规模部署中，它在各种模型架构上扩展至 PP4 时仍能保持**超过 80% 的扩展效率**；在 H20 上以 PP8 部署 Qwen3-235B-A22B-FP8 处理超长提示词时，TTFT 最多可降低 **81%**。

## **背景：为什么选择流水线并行？**

为验证流水线并行（PP）对长上下文预填充的必要性，必须将其与现有范式进行对比评估，即张量并行（TP）和上下文并行（CP）。尽管 TP 和 CP 各有优势，但从通信量、气泡占比和实现复杂度的理论与实证拆解来看，PP 在多节点扩展中占据着一个独一无二的优化位置。以下分析概述了每种方法固有的具体权衡。

### **1\. 通信量与可扩展性分析**

分布式推理扩展的首要瓶颈是设备间通信。随着模型深度和序列长度的增加，设备间传输的数据量会成为限制因素，在扩展到大规模、多节点部署时尤其如此。

假设 $B$ 表示批大小（Batch Size，超长上下文推理中通常为 1），$S$ 表示总序列长度（Sequence Length），$H$ 表示隐藏状态维度（Hidden State），$L$ 表示总层数（Layer Number），$M$ 表示微批（Micro-batch）数量，激活精度为 FP8（1 字节）。基于此，我们分析了不同并行策略的通信量。

* **TP：** TP 将单个权重张量切分到单层内的多个设备上。正因如此，TP 在注意力模块（Attention Block）和 MLP 模块之后都需要同步，从而产生高昂的通信开销。因此，通信量随层数线性增长。这种频繁的 **All-Reduce** 同步使 TP 受限于带宽，难以在大型集群上扩展。
$$
\text{Commu Volume}({TP}) = 2 \cdot (TP_{Size} - 1) \cdot \left( B \cdot S \cdot \frac{H}{TP_{Size}} \right)  \cdot 2 \cdot L \cdot \text{bytes} \approx 4 \cdot B \cdot S \cdot H \cdot L \cdot \text{bytes}
$$
（注：在基于环（ring）的实现中，每次 All-Reduce 涉及 $2 \times$ 数据量。每层包含 $2 \times$ 次 All-Reduce 操作，一次在注意力模块之后，一次在 MLP 模块之后。）
* **CP：** 类似地，CP 需要大量同步通信来聚合跨设备的键值（KV）状态。CP 通常在每一层执行 **All-Gather**，在带宽受限的环境中会带来显著的延迟代价。
$$
\text{Commu Volume}({CP}) = (CP_{Size} - 1) \cdot \left( B \cdot \frac{S}{CP_{Size}} \cdot 2 \cdot H_{KV} \right)  \cdot L \cdot \text{bytes} \approx 2 \cdot B \cdot S \cdot H_{KV} \cdot L \cdot \text{bytes}
$$
（注：此处假设 CP 采用基于 Ring-Attention 的方案。对于使用 GQA 的模型，$H_{KV}$ 小于 $H$，这会降低 CP 的通信量。）
* **PP：** 相比之下，PP 的通信足迹显著更小。数据**仅在流水线阶段（stage）的边界处**传输，使用的是**点对点（P2P）**原语而非集合通信操作。由于一个阶段通常包含多层，通信频率由阶段数（$P$）决定，而非总层数（$L$）。关键在于，对于固定的模型，当增加每个阶段的层数时，边界处的通信量保持不变。
$$
\text{Commu Volume}({PP}) = M \cdot \left( \frac{B}{M} \cdot S \cdot H \right) \cdot (P-1) \cdot \text{bytes} = B \cdot S \cdot H \cdot (P-1) \cdot \text{bytes}
$$
（注：在 $P \ll L$ 的多节点部署中，PP 的总通信量相比 TP 可实现接近一个数量级的降低。）

### **2\. 气泡占比的权衡**

PP 在优化通信的同时，也引入了流水线气泡——即设备等待数据依赖而产生的空闲期。这在通信效率与设备利用率之间形成了一种权衡。

* **TP 与 CP：** 两种方法理论上都能实现零气泡占比，因为所有设备都在同一张量或序列的不同部分上同时计算。在通信不阻塞计算的前提下，这可以最大化计算强度。
* **PP：** PP 不可避免地存在气泡占比，其大小由 PP 度（$P$）与微批数量（$M$）共同决定：
$$
\text{Bubble Ratio} = \frac{P - 1}{P - 1 + M}
$$

然而，对于负载可观（$M \gg P$）的长上下文预填充场景，该占比会显著下降，使得相比通信方面的收益，效率损失可以忽略不计。在[**性能表现**](#performance-impact)一节中，我们将评估本 PP 实现的**强扩展效率**（Strong Scaling Efficiency，即在问题规模保持不变的情况下增加处理器数量）。

值得注意的是，虽然 PP 在跨节点扩展（此时通信带宽往往成为首要瓶颈）中具有独特优势，但一般不建议采用纯高并行度的 PP 配置。这是因为对于固定的负载 $M$，流水线气泡占比会随 PP 度 $P$ 成比例增加。更好的策略是利用 TP 或 CP 等无气泡的并行方法进行节点内扩展。由于节点内通信通常使用 NVLink 等高带宽互连，这些集合通信相比跨节点传输远不容易成为性能瓶颈，从而让系统在不引入额外流水线开销的情况下最大化计算利用率。

### **3\. 实现复杂度与架构通用性**

对于现代推理系统而言，尤其是开源项目，新功能的实现复杂度与架构通用性是至关重要的考量因素。

* **TP：** TP 易于实现且支持广泛。然而，大规模 TP 配置本质上不可行，因为量化块（quantization block）所需的粒度有时无法与 MoE FFN 权重施加的切分约束对齐。因此，即便不考虑通信量与开销，由于 TP 与量化（一项至关重要、不可或缺的优化技术）存在这种不兼容，更大的 TP 度在多节点扩展场景中也常常被排除。
* **CP：** CP 实现复杂，需要对注意力机制进行特定的、往往具有侵入性的修改（例如 Ring Attention）。这些改动必须针对每一种注意力变体和具体模型量身定制，通用性较差。
* **PP：** PP 的复杂度居中。它只需对模型进行切分，而与层的内部机制无关。这使得 PP 成为适用于所有模型架构的通用方案，无需针对特定注意力变体进行内核级别的重写。某种程度上说，消除 PP 气泡比实现 PP 本身更难。

| 指标 | 张量并行（TP） | 上下文并行（CP） | 流水线并行（PP） |
| :---: | :---: | :---: | :---: |
| **切分维度** | 隐藏状态（$H$） | 序列（$S$） | 层（$L$） |
| **通信模式** | AllReduce（每层） | AllGather（每层） | P2P（Send/Recv） |
| **通信量** | 高 | 中 | **低** |
| **气泡占比** | **0** | **0** | $\frac{P - 1}{P - 1 + M}$ |
| **实现复杂度** | **低** | 高<br>（依赖具体注意力变体） | 中 |
| **架构通用性** | **高** | 低 | **高** |

总而言之，通用性与扩展效率之间的平衡，使 PP 不仅仅是一种备选方案，更是长上下文预填充扩展到 TP 和 CP 遭遇带宽天花板的大规模多节点集群时的**必要组件**。与此同时，CP 有潜力与 TP 形成互补，实现节点内的无气泡扩展与加速。**PP × CP** 已在开发之中（见[未来路线图](#future-roadmap)），将包含在本博客的第二部分中。

## **挑战："气泡"与"内存墙"**

在传统的流水线并行设置中，模型层被切分到多张 GPU 上（Stage 1 到 Stage N）。服务标准请求（例如 < 4K token）时通常运转良好。然而，当处理超过 **128K 乃至 100 万 token** 的提示词时，两个关键问题便会浮现：

1. **流水线气泡：** 将提示词作为一个整体批次处理，会让下游 GPU 陷入长时间空闲，形成巨大的"流水线气泡"，严重降低吞吐量。
2. **内存墙：** 单次处理 100 万 token 的提示词，需要为整个序列存储并传输中间隐藏状态，带来巨大的开销和峰值内存占用。

## **SGLang 的流水线并行架构**

SGLang 的流水线实现超越了标准的"顺序"方案。我们引入了若干进阶特性，以最小化"气泡"（即 GPU 空闲时间）并最大化硬件利用率。

### **1\. 分块流水线并行（CPP）**

在单次前向传播中处理 100 万 token 的提示词，会因后续阶段等待第一阶段完成而产生大量气泡。受 Mooncake[\[1\]](https://dl.acm.org/doi/pdf/10.1145/3773772)、BladeLLM[\[2\]](https://arxiv.org/pdf/2501.15383?) 和 TeraPipe[\[3\]](http://proceedings.mlr.press/v139/li21y/li21y.pdf) 等架构的启发，SGLang 支持分块流水线并行（Chunked Pipeline Parallelism）。SGLang 不再将完整提示词一次性送入流水线，而是将其切分为更小的"块"（chunk，如 4K 或 6K token）。这些块像微批一样流经各个流水线阶段。通过把长提示词拆成更小的块，系统得以让预填充阶段"流水线化"。第一阶段一完成 Chunk 1 隐藏状态的计算并发起 PP 通信，就立即转入处理 Chunk 2，与此同时 Stage 2 也开始处理 Chunk 1。这样，流水线启动延迟不再与总序列长度成正比，而只与第一个块的大小成正比。

从工程角度看，这一方法是应对超长上下文挑战的关键第一步。值得一提的是，SGLang 早在六个多月前就率先支持了这一特性（[#5724](https://github.com/sgl-project/sglang/pull/5724)、[#8846](https://github.com/sgl-project/sglang/pull/8846)），足见其对优化真实场景长上下文推理的长期投入。

### **2\. 更好的重叠：微批与异步 P2P 通信**

尽管相比张量并行，流水线并行与分块预填充的结合能显著减少通信量，但它常常受制于流水线气泡——GPU 在等待 CPU 元数据处理或网络传输时被阻塞。为消除这一性能隐患，SGLang 实现了带非阻塞异步点对点（P2P）通信的微批事件循环（Micro-batching Event Loop），使 GPU 计算与 CPU 元数据处理及 PP 通信相互重叠。这样，当一个微批正在 GPU 上计算时，下一个微批已在准备并被高效地调度就位，从而让流水线尽可能保持饱和。代码见[此处](https://github.com/sgl-project/sglang/blob/main/python/sglang/srt/managers/scheduler_pp_mixin.py)。

该实现的关键机制包括：

* **事件循环中解耦的同步/异步逻辑：** 调度器在 `_pp_send_pyobj_to_next_stage` 中使用 `async_send`，它不等待传输完成，而是返回一个 `P2PWork` 句柄。实际的同步（`P2PWork.work.wait()`）被推迟到调用 `_pp_commit_comm_work` 时才执行，从而让 CPU 可以在数据传输途中执行其他工作——比如调度下一批请求或处理元数据。
* **多流执行：** 除作为同步流的主 `default_stream` 之外，SGLang 还使用专用的 `forward_stream` 和 `copy_stream`，分别执行前向传播的 GPU 计算和设备到主机（D2H）内存传输，以实现更好的重叠。当 `_pp_launch_batch` 在 GPU 上为当前阶段执行当前微批时，CPU 通过 `_pp_process_batch_result` 处理上一个微批的结果。

### **3\. 进阶选项：动态分块（Dynamic Chunking）**

借助分块流水线并行和异步 P2P 通信，SGLang 在 PP 度提升至 4 时已能实现超过 80% 的强扩展效率。然而，固定大小的分块预填充仍可能在流水线中造成气泡，且 PP 度越高，这种低效越明显。造成这一现象的主要原因是，模型在处理相同大小的块时执行延迟并不均匀，这主要源于自注意力的增量特性。**随着前缀序列长度的增长，每个块的处理时间呈非线性上升。这些时间错配会在流水线中级联传播，在更高 PP rank 上叠加放大效率损失。**

<img src="/images/blog/chunked_pipeline/pp_bubbles_before.jpg"
     alt="Fig. 1: Pipeline diagram with fixed chunked prefill size"
     style="display: block; margin: 20px auto 0; width: 65%; max-width: 100%; height: auto;">

<p style="color: black; text-align: center; font-size: 0.9em;">图 1：固定分块预填充大小下的流水线示意图</p>

我们使用较大的 PP 度测试了不同模型，发现它们都符合这一结论。以下是一个典型案例的剖析（profile）结果。

<img src="/images/blog/chunked_pipeline/profile_before.png"
     alt="Fig. 2: Profile result of the PP rank 7 with fixed chunked prefill size"
     style="display: block; margin: 20px auto 0; width: 85%; max-width: 100%; height: auto;">

<p style="color: black; text-align: center; font-size: 0.9em;">图 2：固定分块预填充大小下 PP rank 7 的剖析结果</p>


因此，如果 SGLang 仍**在 CPP 中使用固定的分块预填充大小，流水线气泡占比将高于理论预期（即 $\frac{P - 1}{P - 1 + M}$）**。

为解决这一问题，SGLang 引入了动态分块机制来预测下一个块的最优大小，使其满足以下条件：
$$
\text{Runtime}(L + \Delta L) - \text{Runtime}(L) = \text{Runtime}(\text{Initial Chunk Size})
$$

其中 $L$ 表示前缀序列长度（Prefix Sequence Length），$\Delta L$ 表示下一个块的大小（Next Chunk Size）。通过剖析一系列不同 ITL 的请求，我们将累计运行时长建模为序列长度的二次函数。利用该模型，我们可以对任意给定的前缀长度 $L$ 求解出最优的下一个块大小 $\Delta L$。由于注意力机制的计算/通信复杂度随 $L$ 增长，下一个块的大小会随 $L$ 的增大而逐步减小，以保持各流水线阶段之间块执行时间的对齐。

基于这一方法，调度器可以在运行时预测并动态减小块的大小，从而将阶段错位造成的气泡降至最低。需要注意的是，调度器并不直接使用原始预测值。为了便于高效的 KV 缓存内存管理并保证与硬件执行效率的亲和性，该值会向下对齐到 max(`--page-size`, 64) 的最近整数倍。

<img src="/images/blog/chunked_pipeline/pp_bubbles_after.jpg"
     alt="Fig. 3: Pipeline diagram with perfect dynamic chunking"
     style="display: block; margin: 20px auto 0; width: 65%; max-width: 100%; height: auto;">

<p style="color: black; text-align: center; font-size: 0.9em;">图 3：理想动态分块下的流水线示意图</p>

然而，由于硬件、模型和目标负载各不相同，静态配置很少能在所有场景下都达到最优。因此，切换到动态分块模式后，需要一定程度的超参数调优才能达到峰值性能。此外，我们还发现，由于不同形状下算子（kernel）性能存在差异，二次函数难以完美拟合。为此，我们引入了环境变量（`SGLANG_DYNAMIC_CHUNKING_SMOOTH_FACTOR`）来对动态分块算法的缩减进行平滑，默认值为 0.75，它决定了预填充阶段块大小可以变化的幅度。该值越大，块大小的缩减越激进，可能提升性能，但也会增加块的总数（末尾的块可能变得非常小，反而可能导致性能下降）。

**动态分块预填充调优指南**

* **第 1 步 \- 迭代找出目标 PP 度下的最优固定分块预填充大小**：对于目标 ITL，不同的 PP 度可能有不同的最优分块预填充大小。因此，用户应根据可用于扩展的资源迭代求出基线。
* **第 2 步 \- 为动态分块选择初始块大小**：将初始大小设为最优固定分块预填充大小的 2 倍或 3 倍。这可以减少块的总数，避免"尾部块"造成硬件利用不足。为了在极大的输入 token 长度（ITL）下保持效率，动态预测器会自动保证后续块至少为该初始大小的 1/4。此外，针对此类情况，也建议使用更大的初始块大小（例如最优固定分块预填充大小的 4 倍）。
* **第 3 步 \- 平滑因子调整**：该因子控制块大小对二次函数性能拟合模型所给出预测的遵循程度。
  * 1.0：严格遵循模型。
  * **0.6 – 0.85（推荐）**：在动态伸缩与硬件稳定性之间取得最佳平衡的典型区间。通过实验我们发现，0.6 到 0.85 之间的取值通常能为动态分块带来最佳性能，如图 4 和图 5 所示。
  * 0：禁用动态调整，回退到传统的固定大小分块。

<img src="/images/blog/chunked_pipeline/sigma_ds.png"
     alt="Fig. 4: Example of tuning the smooth factor for DeepSeek-V3.1 (Lower is better)"
     style="display: block; margin: 20px auto 0; width: 85%; max-width: 100%; height: auto;">

<p style="color: black; text-align: center; font-size: 0.9em;">图 4：DeepSeek-V3.1 平滑因子调优示例（越低越好）</p>


<img src="/images/blog/chunked_pipeline/sigma_qwen.png"
     alt="Fig. 5: Example of tuning the smooth factor for Qwen3-235B-A22B-FP8 (Lower is better)"
     style="display: block; margin: 20px auto 0; width: 85%; max-width: 100%; height: auto;">

<p style="color: black; text-align: center; font-size: 0.9em;">图 5：Qwen3-235B-A22B-FP8 平滑因子调优示例（越低越好）</p>

* **另一个小优化技巧：** 当层无法在各 rank 间整除时，将更大的分区放在更高的 PP rank 上。当较大的 PP rank 在等待上一阶段的结果时，这可以提高 GPU 利用率，从而减少高 PP rank 上的气泡。以 DeepSeek-V3.1 为例，`SGLANG_PP_LAYER_PARTITION=15,15,15,16` 通常比 `16,15,15,15` 表现更好。

为验证这些组合策略的有效性，我们对使用动态分块的 DeepSeek-V3.1 执行过程进行了剖析。从以下 PP rank 3 的剖析结果可以看到，与静态分块方案相比，流水线气泡被显著压缩，执行更加饱和。

<img src="/images/blog/chunked_pipeline/profile_after.png"
     alt="Fig. 6: Profile result of the PP rank 3 with dynamic chunking (DeepSeek-V3.1)"
     style="display: block; margin: 20px auto 0; width: 85%; max-width: 100%; height: auto;">

<p style="color: black; text-align: center; font-size: 0.9em;">图 6：动态分块下 PP rank 3 的剖析结果（DeepSeek-V3.1）</p>

### **4\. 生产就绪：兼容 PD 分离与 HiCache**

SGLang 的一项独特优势，是在流水线设置中原生支持**预填充-解码分离（PD 分离，PD Disaggregation）**。在分离式集群中，预填充节点可以使用高并行度的 PP 来处理极长上下文的提示词，而解码节点则可以采用不同的并行策略（如高并行度 TP）来最大化 token 生成速度。

* **逐块 KV 缓存传输：** SGLang 不必等所有块都处理完毕——启用 PD 分离后，借助 mooncake 等传输引擎后端，一个块的 KV 缓存可以立即从预填充节点传输到解码节点。该特性大幅降低了 KV 缓存的传输开销。
* **灵活的混合策略：** SGLang 允许用户在 PD 分离下混用多种并行策略。你可以在一组预填充节点上以 PP8 TP8 运行繁重的预填充任务，并采用其他组合（如 PP1 TP8、PP8 TP1、PP1 DP16 EP16）进行高吞吐解码，针对推理生命周期的不同阶段进行优化。这使得用户能够以高度可定制的方式满足生产环境中预期的首 token 延迟（TTFT）和 TPOT 目标。
* **内存效率：** 通过将模型权重分布到各设备上，PP 降低了单 GPU 的内存占用，从而可以容纳更大的 KV 缓存并支持更高并发。因此，在某些场景下可用于扩展最大上下文长度。

在处理超过 128K token 的上下文时，SGLang 还支持将分块流水线并行与 **HiCache** 结合使用。HiCache 是一个分布式分层 KV 缓存系统，可进一步降低超长初始 ITL 下多轮问答与智能体（agentic）应用的 TTFT：

* **语义前缀匹配：** SGLang 的 HiCache 采用基于基数树（radix tree）的层级结构，在块级别匹配前缀。当长上下文请求到达时，SGLang 可以执行分层缓存查找。如果前缀 token（在之前的块中已处理）已缓存于 HiCache 的"存储（Storage）"层（如主机内存或本地磁盘），PP 流水线就可以完全跳过这些块，大幅降低 TTFT。

## **性能表现**

本节对 DeepSeek-V3.1 和 Qwen3-235B-A22B-FP8 模型的 PP 性能特征进行了严格的定量评估。分析重点关注 PP 度、动态分块（Dynamic Chunking，DCK）与硬件可扩展性之间的相互作用。

我们的实验测试平台是一个由 6 个 H20 节点（8 × 96GB VRAM GPU）组成的小型集群。由于测试资源有限，未对 DeepSeek-V3.1 开展 PP 度为 8 的实验。此外，对于 DeepSeek-V3.1 的 PP size \= 1 配置，我们使用了一台独立的 H20 节点（8 × 141GB VRAM GPU）来获取输入 token 长度为 128K 时的基线性能（96GB VRAM 版本会出现 OOM）。为了更好地验证流水线饱和时的吞吐量表现，我们在吞吐量测试中测量了连续 16 个请求的平均值。

注：我们用记号 **DCK** 表示启用动态分块时的分块预填充大小设置，**σ** 表示动态分块的平滑因子。为了开展极长上下文实验，我们将上述模型的上下文长度覆盖为 100 万，仅用于性能分析。此外，我们曾尝试对 DeepSeek-V3.1 进行 TP32、对 Qwen3-235B-A22B-FP8 进行 TP8 的实验，但遗憾的是，大 TP 配置本质上不受支持，因为权重量化块无法被 FFN（MoE）层的权重整除（[参考 Issue](https://github.com/sgl-project/sglang/issues/3345)）。为了在多节点扩展场景中充分对比 TP 与 PP 的差异，我们修改了 DeepSeek-V3.1 的模型实现文件（在 `load_weights` 中跳过部分权重加载）和 config.json（[变通方案 Issue](https://github.com/sgl-project/sglang/issues/3491#issuecomment-2650779851)），让 TP32 得以运行——仅用于性能验证目的。

### **输入 token 吞吐量与强扩展效率**

吞吐量随 PP 度变化的分析表明，两个模型家族都具备很强的水平扩展能力，但扩展效率的高低因配置而异。

* **PP 与 TP 的对比**：实验数据揭示了一个关键现象：将张量并行（TP）扩展到 16 时出现了性能下滑，而混合并行方案（PP2 TP8）表现更优。尽管占用的 GPU 总数完全相同，PP2 TP8 在吞吐量和延迟指标上都始终优于 PP1 TP16。此外，在所有分块大小配置下，PP4 TP8 在吞吐量和延迟指标上也始终优于 PP1 TP32。值得注意的是，在固定分块大小 12288 下，该配置在 PP4 TP8 的所有分块策略配置中性能最低；但即便是 PP4 TP8 的这一最差表现，仍以 **18.4%** 的显著幅度领先于 PP1 TP32（固定分块大小同样为 12288）——而这已经是所测纯 TP 配置中的最佳性能。采用动态分块后，这一领先幅度进一步扩大到 **30.5%**。这些结果凸显了 PP 方案的固有优势。
* **DCK 出色的可扩展性**：**Qwen DCK 18K** 配置展现出最高的可扩展性，PP8（32 GPU）相比 PP1（4 GPU）取得了 **6.14 倍**的加速。这一表现说明，块大小的动态调整优化了计算强度与节点间通信延迟之间的平衡。
* **架构对比**：在 PP4 阈值以内，DeepSeek 模型展现出与 Qwen 相近的扩展轨迹。值得注意的是，**DeepSeek DCK 12K（3.31×）**略优于静态 4K 变体（3.20×），验证了动态分块策略在提升吞吐量方面的跨架构稳健性。

<img src="/images/blog/chunked_pipeline/ds_throughput.png"
     alt="Fig. 7: Throughput Analysis of DeepSeek-V3.1 (Higher is better)"
     style="display: block; margin: 20px auto 0; width: 85%; max-width: 100%; height: auto;">

<p style="color: black; text-align: center; font-size: 0.9em;">图 7：DeepSeek-V3.1 吞吐量分析（越高越好）</p>


<img src="/images/blog/chunked_pipeline/qwen_throughput.png"
     alt="Fig. 8: Throughput Analysis of Qwen3-235B-A22B-FP8 (Higher is better)"
     style="display: block; margin: 20px auto 0; width: 85%; max-width: 100%; height: auto;">

<p style="color: black; text-align: center; font-size: 0.9em;">图 8：Qwen3-235B-A22B-FP8 吞吐量分析（越高越好）</p>

强扩展效率曲线刻画了系统扩展过程中硬件利用率的衰减情况（在强扩展效率分析中，ITL 保持 128K 不变而 $P$ 增大，因此按照公式，气泡占比下界必然更高）。所有配置的效率都随 PP 度（GPU 数量）的增加呈单调衰减。不过，**Qwen DCK 18K** 在 PP8 规模下仍保持了 **76.9%** 的优异效率，而静态 6K 配置则降至 **69.6%**。这印证了更大且经动态管理的块对流水线气泡造成的性能衰减更具韧性。受资源限制，DeepSeek-V3.1 的评估最高到 PP size \= 4，效率保持在 **82.8%**。按当前斜率外推，DeepSeek 很可能呈现与 Qwen 相似的效率轨迹，且预计 DCK 将优于固定分块策略。

<img src="/images/blog/chunked_pipeline/scale_efficiency.png"
     alt="Fig. 9: Strong Scaling Efficiency vs. PP Size Analysis (Higher is better)"
     style="display: block; margin: 20px auto 0; width: 85%; max-width: 100%; height: auto;">

<p style="color: black; text-align: center; font-size: 0.9em;">图 9：强扩展效率随 PP 度变化分析（越高越好）</p>

### **降低 TTFT 并扩展至百万 token 输入长度**

从图 10 和图 11 可以观察到，无论采用固定分块设置还是动态分块，将 PP 度从 PP1 提升到 PP4 都能带来 TTFT 的大幅下降，但动态分块在不同 PP 设置下表现更佳。对于 Qwen3-235B-A22B-FP8，基线 TTFT **\~55.5s**（PP1 TP4）在 PP8 TP4 配置下降至 **\~10.5s**，延迟改善约 **81.1%**。对于 DeepSeek-V3.1，基线 TTFT **\~48.5s**（PP1 TP8）在 PP4 TP8 配置下降至 **\~15.5s**，延迟改善约 **67.9%**。这些结果表明，分块流水线并行在降低 TTFT 方面非常有效。

<img src="/images/blog/chunked_pipeline/ds_ttft.png"
     alt="Fig. 10: TTFT Analysis of DeepSeek-V3.1 (Lower is better)"
     style="display: block; margin: 20px auto 0; width: 85%; max-width: 100%; height: auto;">

<p style="color: black; text-align: center; font-size: 0.9em;">图 10：DeepSeek-V3.1 TTFT 分析（越低越好）</p>


<img src="/images/blog/chunked_pipeline/qwen_ttft.png"
     alt="Fig. 11: TTFT Analysis of Qwen3-235B-A22B-FP8 (Lower is better)"
     style="display: block; margin: 20px auto 0; width: 85%; max-width: 100%; height: auto;">

<p style="color: black; text-align: center; font-size: 0.9em;">图 11：Qwen3-235B-A22B-FP8 TTFT 分析（越低越好）</p>

为了展示 SGLang 这一优化后的分块流水线并行的可扩展性，我们在不同输入 token 长度下对使用 PP8（32 张 NVIDIA H20 GPU）的 Qwen3-235B-A22B-FP8 进行了 TTFT 基准测试。如下表所示，系统能够高效扩展以处理海量上下文。即便在 **100 万 token** 的极端边界上，SGLang 在 NVIDIA H20 上仍保持高度稳定和可接受的延迟，展现了其应对最严苛长上下文应用的能力。

<br>
<center>表 1：Qwen3-235B-A22B-FP8 在 H20 上以 PP8 TP4 运行时的 TTFT 随输入 token 长度的变化</center>
<div align="center">

| 输入 token 长度 | 128K | 256K | 512K | 1M |
| :---: | :---: | :---: | :---: | :---: |
| TTFT (s) | 10.54 | 32.68 | 114.33 | 420.91 |

</div>
<br>

使用算力和带宽高于 H20 的硬件，或在更多节点上扩展到更大的 PP 度（例如 DeepSeek-V3.1 模型使用 PP8 TP16），可进一步降低百万 token 上下文的 TTFT。我们诚邀社区在各种硬件配置上试用这一新特性，分享性能测试结果并报告遇到的 bug。我们期待听到你的声音——欢迎在 [PP 路线图](https://github.com/sgl-project/sglang/issues/11857)的 issue 中提出任何问题。你的反馈对帮助我们打磨这些长上下文优化至关重要！另外，敬请期待即将推出的 CP × PP 实现——对 DeepSeek-V3.2 的初步支持已在 main 分支上提供。

## **快速上手**

要使用这些特性，只需配置 `--pp-size` 和 `--chunked-prefill-size`。若要进一步采用动态分块方案，请使用 `--enable-dynamic-chunking` 并设置环境变量 `SGLANG_DYNAMIC_CHUNKING_SMOOTH_FACTOR`。

注：要求 SGLang 版本 `>= v0.5.7`

示例：
```bash
# Example: Serving DeepSeek-V3.1 with 128K Input Token Length (32 GPUs total)
# Using 8-way Tensor Parallelism and 4-way Pipeline Parallelism

# prefill node 0 (fixed chunked prefill size)
python3 -m sglang.launch_server \
  --model-path deepseek-ai/DeepSeek-V3.1 --trust-remote-code \
  --nnodes 4 --node-rank 0 --tp 8 --pp-size 4 \
  --port 30000 --dist-init-addr <MASTER_NODE_IP> \
  --mem-fraction-static 0.8 --attention-backend fa3 \
  --host 0.0.0.0 --watchdog-timeout 3600 \
  --max-running-requests 128 --chunked-prefill-size 4096

# prefill node 0 (with dynamic chunking)
export SGLANG_DYNAMIC_CHUNKING_SMOOTH_FACTOR=0.65
python3 -m sglang.launch_server \
  --model-path deepseek-ai/DeepSeek-V3.1 --trust-remote-code \
  --nnodes 4 --node-rank 0 --tp 8 --pp-size 4 \
  --port 30000 --dist-init-addr <MASTER_NODE_IP> \
  --mem-fraction-static 0.8 --attention-backend fa3 \
  --host 0.0.0.0 --watchdog-timeout 3600 \
  --max-running-requests 128 --chunked-prefill-size 12288 --enable-dynamic-chunking


# Example: Serving Qwen3-235B-A22B-FP8 with 128K Input Token Length (32 GPUs total)
# Using 4-way Tensor Parallelism and 8-way Pipeline Parallelism

# prefill node 0 (fixed chunked prefill size)
python3 -m sglang.launch_server \
  --model-path Qwen/Qwen3-235B-A22B-FP8 --trust-remote-code \
  --nnodes 4 --node-rank 0 --tp 4 --pp-size 8 \
  --port 30000 --dist-init-addr <MASTER_NODE_IP> \
  --mem-fraction-static 0.8 --attention-backend fa3 \
  --host 0.0.0.0 --watchdog-timeout 3600 \
  --max-running-requests 128 --chunked-prefill-size 6144

# prefill node 0 (with dynamic chunking)
export SGLANG_DYNAMIC_CHUNKING_SMOOTH_FACTOR=0.8
python3 -m sglang.launch_server \
  --model-path Qwen/Qwen3-235B-A22B-FP8 --trust-remote-code \
  --nnodes 4 --node-rank 0 --tp 4 --pp-size 8 \
  --port 30000 --dist-init-addr <MASTER_NODE_IP> \
  --mem-fraction-static 0.8 --attention-backend fa3 \
  --host 0.0.0.0 --watchdog-timeout 3600 \
  --max-running-requests 128 --chunked-prefill-size 18432 --enable-dynamic-chunking
```

## **未来路线图：**

我们正在持续打磨 PP 技术栈。我们 2026 上半年的 PP 路线图包括以下重要任务：

* 兼容上下文并行（CP），进一步降低 TTFT
* 解码侧的流水线并行
  * 性能优化与最佳实践调优
* 面向动态分块的更优拟合与分块策略

<div style="border-left: 4px solid #3b82f6; padding: 10px 12px; margin: 12px 0; background: #eff6ff; border-radius: 8px;">
  <strong>👉 查看 <a href="https://github.com/sgl-project/sglang/issues/11857">PP 路线图</a>。</strong>
</div>

## **结语**

SGLang 的流水线并行实现不仅仅是模型切分，更是面向长上下文时代对推理生命周期的全面重构。通过将分块预填充与异步通信、动态分块相结合，SGLang 为长上下文场景下服务并加速万亿参数模型提供了最高效的开源路径。

## **致谢**

- 感谢 SGLang 团队和社区在实现过程中给予的支持与帮助，尤其要感谢 **Shangming Cai**、**Xuchun Shang**、**Yanbo Yang**、**Leon Gao**、**Ying Sheng**、Zhiqiang Xie、Lianmin Zheng 以及许多其他贡献者。
- 感谢 **Jianhao Fu**（来自 AntGroup SCT Network Team）、**Kevin Li**（来自 TikTok）、Siyu Liu（来自 Alibaba Cloud Computing）、Xiaolei Zhang（来自 ByteDance）、Teng Ma（来自 Alibaba Cloud Computing）、Chao Wang（来自 Meituan）以及 Xiaowei Wang（来自 NVIDIA）在代码改进和测试方面作出的突出贡献。
- 我们从 [SGLang](https://github.com/sgl-project/sglang)、Mooncake[\[1\]](https://dl.acm.org/doi/pdf/10.1145/3773772) 和 TeraPipe[\[3\]](http://proceedings.mlr.press/v139/li21y/li21y.pdf) 的系统设计中获益良多，它们共同帮助改进了这套流水线并行实现。

## **参考文献**

[1] Qin, Ruoyu, et al. "Mooncake: A kvcache-centric disaggregated architecture for llm serving." ACM Transactions on Storage (2024).\
[2] Yang, An, et al. "Qwen2. 5-1m technical report." arXiv preprint arXiv:2501.15383 (2025).\
[3] Li, Zhuohan, et al. "Terapipe: Token-level pipeline parallelism for training large-scale language models." International Conference on Machine Learning. PMLR, 2021.
