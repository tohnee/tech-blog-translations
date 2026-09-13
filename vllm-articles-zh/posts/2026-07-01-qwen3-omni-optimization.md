---
title: "在 vLLM-Omni 中服务多阶段 Qwen3-Omni 的经验与教训"
title_en: "Experience and Lessons Learned from Serving Multi-Stage Qwen3-Omni in vLLM-Omni"
source: https://vllm.ai/blog/2026-07-01-qwen3-omni-optimization
crawled: 2026-09-12
translated: 2026-09-13
---

# 在 vLLM-Omni 中服务多阶段 Qwen3-Omni 的经验与教训

> 原文：[Experience and Lessons Learned from Serving Multi-Stage Qwen3-Omni in vLLM-Omni](https://vllm.ai/blog/2026-07-01-qwen3-omni-optimization) · vLLM 博客

作者：vLLM-Omni 团队与蚂蚁集团 SCT 团队

[#性能](https://vllm.ai/blog/tags/performance)[#多模态](https://vllm.ai/blog/tags/multimodal)[#vllm-omni](https://vllm.ai/blog/tags/vllm-omni)

Qwen3-Omni 将多模态理解与语音生成结合在一起。本文介绍 [vLLM-Omni](https://github.com/vllm-project/vllm-omni) 如何把它作为分阶段流水线来服务，并针对在线负载优化每个阶段。

## TL;DR

vLLM-Omni 的 Qwen3-Omni 服务栈包括：

- **三阶段流水线：** Thinker 负责多模态推理，Talker 负责语音编解码生成，Code2Wav 负责波形重建。
- **OpenAI 兼容服务：** `/v1/chat/completions` 是 Qwen3-Omni 文本与音频生成的主要端点。
- **批处理、CUDA Graph、异步分块、异步输出、副本与热路径清理：** 在 Thinker、Talker 和 Code2Wav 上进行阶段级批处理与逐阶段图捕获，提升高并发吞吐量；异步分块交接与异步输出让流水线和解码 worker 不会因全量负载屏障和同步负载构造而停顿；Talker/Code2Wav 副本扩展语音生成阶段；热路径清理削减随语句长度增长的每步模型内部开销。
- **性能验证：** 受控基准扫描与 DFX 性能运行显示，随着每层优化逐一开启，音频 TTFP（首音频包延迟）更低、音频 RTF（实时因子）更低、吞吐量更高。

## 快速上手

用 `--omni` 服务该模型时，默认的 Qwen3-Omni 部署配置会自动解析：

```
vllm serve Qwen/Qwen3-Omni-30B-A3B-Instruct \
  --omni \
  --port 8091
```

如需显式配置，传入分阶段部署配置：

```
vllm serve Qwen/Qwen3-Omni-30B-A3B-Instruct \
  --omni \
  --port 8091 \
  --deploy-config vllm_omni/deploy/qwen3_omni_moe.yaml
```

内置配置包含 `platforms:` 段。vLLM-Omni 会检测运行时后端（CUDA、NPU、ROCm 或 XPU）并自动合并对应的差异配置——无需额外的 CLI 参数。同一条启动命令可跨硬件使用。

请求应使用 `/v1/chat/completions`。在请求体中设置 `modalities` 来声明输出类型——例如只用文本用 `["text"]`，文本加语音用 `["text", "audio"]`。

部署选项、异步分块设置和多副本布局，请参阅 [Qwen3-Omni 在线服务指南](https://github.com/vllm-project/vllm-omni/blob/main/examples/online_serving/qwen3_omni/README.md)。

## Qwen3-Omni 服务模型

纯文本 LLM 服务是一个循环：预填充、解码、去 tokenize。Qwen3-Omni 在多模态推理之后增加了两个语音阶段，各自有不同的计算特征：

```
Thinker   -> multimodal understanding + text generation
Talker    -> hidden states and embeddings to RVQ codec codes
Code2Wav  -> codec codes to waveform audio
```

![图 1：vLLM-Omni 中的 Qwen3-Omni 服务是一条分阶段数据流：Thinker 产生文本和隐藏状态，Talker 产生编解码码字，Code2Wav 重建音频。](https://vllm.ai/blog-assets/figures/2026-07-01-qwen3-omni-optimization/qwen3-omni-serving-flow.svg)

图 1：vLLM-Omni 中的 Qwen3-Omni 服务是一条分阶段数据流：Thinker 产生文本和隐藏状态，Talker 产生编解码码字，Code2Wav 重建音频。

## 优化概览

Qwen3-Omni 流水线的不同部分会遇到不同的瓶颈。vLLM-Omni 不套用同一套固定配方，每项优化都针对特定的阶段或交接。下面的逐项走读按我们验证它们的顺序依次展开，并依次回答三个问题：**为什么**存在这个问题、**为什么有效**（该机制如何消除问题），以及**你能得到什么**（实测收益）。

| 技术 | 目标阶段 / 路径 | 解决的问题 | 主要收益 |
| --- | --- | --- | --- |
| 阶段拆分 | Thinker → Talker → Code2Wav | 计算特征差异极大的三个阶段共享一个循环，单一的批处理/图/设备策略会让最慢的子路径卡住其余部分——限制吞吐量并阻碍按阶段调优和扩缩 | 每阶段独立的运行时策略 |
| AR + Code2Wav 批处理 | Talker MTP 路径、Code2Wav 异步分块 | 高并发下单请求的微任务让 SM 在发射间隙空闲，限制 GPU 占用率与 req/s | 更高的占用率与 req/s |
| CUDA Graph | Thinker / Talker / Code2Wav 解码路径 | 每个解码步重复的 CPU 侧内核发射推高 TPOT，让音频 RTF 高于实时 | 更低的 TPOT 与音频 RTF；扫描中约 4× 的吞吐跃升 |
| 异步分块 | Thinker→Talker、Talker→Code2Wav | 全量负载的阶段屏障迫使 Code2Wav 等待完整的 Talker 负载，延迟首音频并推高音频 TTFP | 流水线化交接；最大的音频 TTFP 降幅 |
| 异步 omni 输出 | Thinker 连接器负载 | 同步负载构造在分块之间阻塞 Thinker 解码 worker，把 GPU 时间浪费在分配上并拉低吞吐量 | 恢复吞吐量且音频 TTFP 不回退 |
| 阶段副本 | Talker、Code2Wav | Thinker 仍有余量时 Talker 和 Code2Wav 已饱和排队，成为负载下的尾部瓶颈 | 只对瓶颈阶段横向扩展 |
| 热路径清理 | Talker code predictor、连接器负载 | 每步的 Python、分配和同步开销在长语句上累积，推高 E2EL 与音频 TTFP | 更低的每步延迟；可与上述所有层叠加 |

我们在 Seed-TTS `en` 上用受控基准扫描验证了每一层（`Qwen3-Omni-30B-A3B-Instruct`，并发 `1`/`16`/`32`/`64` 下分别 `10`/`160`/`320`/`640` 条 prompt，`5` 次预热，三张可见 GPU 映射为 `0/1/2`）。每个配置都用隔离的部署配置重启服务器，并在前一行的基础上叠加一项优化。从 **Batch** 到 **Async output**，每张 GPU 固定一个阶段（Thinker / Talker / Code2Wav 分别在 GPU 0 / 1 / 2，各单副本）；**Stage replicas** 行让 Thinker 保持在 GPU 0，在 GPU 1 和 2 上运行 2× Talker + 2× Code2Wav。下表汇总并发 64 的结果；[验证结果](#validation-results)给出了全部四个并发级别的图表。

| 步骤 | 新增配置 | Talker / Code2Wav 副本 | Req/s | 平均音频 TTFP | 平均音频 RTF |
| --- | --- | --- | --- | --- | --- |
| 基线 | Batch | 1 / 1 | 2.2 | 5884 ms | 1.15 |
| + CUDA Graph | 在 Thinker、Talker、Code2Wav 上做图捕获 | 1 / 1 | 8.6 (+299%) | 2790 ms (−53%) | 0.59 (−49%) |
| + 异步分块 | 异步分块的阶段交接 | 1 / 1 | 9.3 (+8%) | 655 ms (−77%) | 0.63 |
| + 异步输出 | 异步 omni 输出路径 | 1 / 1 | 11.3 (+22%) | 631 ms (−4%) | 0.47 (−25%) |
| + 阶段副本 | 2× Talker + 2× Code2Wav | 2 / 2 | 11.7 (+4%) | 632 ms | 0.47 |

![图 2：Qwen3-Omni 的性能来自对分阶段数据流、阶段运行时和解码热路径的一体化优化。](https://vllm.ai/blog-assets/figures/2026-07-01-qwen3-omni-optimization/qwen3-omni-optimization-stack.svg)

图 2：Qwen3-Omni 的性能来自对分阶段数据流、阶段运行时和解码热路径的一体化优化。

## 逐阶段展开的优化栈

每项优化都建立在前一项之上，因此每一步报告的数字都假定其上方的每一层已经启用。

### 1. 阶段拆分与批处理：基线

**为什么。** Qwen3-Omni 不是一个同质的解码循环：Thinker 做多模态 AR 文本生成，Talker 跑一条 codec 预测器的 AR 路径，Code2Wav 跑并行的声码器（vocoder）解码。把这三个差异极大的负载折叠进同一条服务路径，等于强迫它们共用同一套批处理策略、图策略和设备布局——并让最慢的子路径卡住其余部分。把阶段分开消除了这种耦合，但也暴露出第二个问题：语音路径的大部分 GPU 时间仍然花在单请求的微任务上。每个 Talker 解码步是一次短短的 code predictor 前向，每个 Code2Wav 分块是一次小的声码器前向，因此在并发 64 时逐请求地运行它们，SM 会在发射间隙闲置，固定的每步成本永远摊不薄。

**为什么有效。** 这依次解决了两个问题。第一，阶段拆分打破耦合：阶段边界成为一等的服务对象，连接器定义了跨过每个边界的是什么（隐藏状态、嵌入、编解码码字、分块元数据），调度器可以在各自的关键路径上对每个阶段做调度、批处理和图捕获——于是没有任何单一策略被强加给三者，最慢的子路径也不再卡住其余部分。第二，逐阶段批处理填上 SM 空闲的缺口：把并发请求收拢进一次 Talker MTP 调用和一次 Code2Wav 前向，填满了被单请求微任务闲置的 SM，并把固定的每步成本摊到整个批次上。

**你能得到什么。** 显式阶段让 vLLM-Omni 可以把每个组件当作独立运行时对待——各自独立的 `max_num_seqs`、采样参数、连接器、graph/eager 策略和可选副本——这是下面每项优化的前提。这个批处理化、阶段拆分的配置就是 **Batch** 基线，后面每一行都建立在它之上。

### 2. CUDA Graph：逐阶段解码图捕获

**为什么。** 批处理提升了占用率，但每个解码步仍在为重复的 CPU 侧内核发射付费。Qwen3-Omni 有三个解码密集的阶段；仅 Talker 一句话就可能执行数百个短步，而此前每步都要从 Python 重新发射同一套稳定的算子序列。并发 64 时，这种发射税主导了 TPOT，即使在批处理之后音频 RTF 仍高于实时。

**为什么有效。** CUDA Graph 消除了主导 TPOT 的每步内核发射：它一次性捕获固定的算子序列，然后用最少的 CPU 工作重放。每个阶段的捕获点不同，但原理一致：解码形状按稳定的 `(batch, seq, frames)` 档位分桶，运行时在预热时录下图并在热路径上复用。

![图 3：每个阶段在不同位置捕获图。Thinker 和 Talker 在 vLLM 的外层图下解码；Talker 的内层 code predictor 用 torch.compile 编译而不是再包一层图；Code2Wav 使用内层 CUDAGraphDecoderWrapper。](https://vllm.ai/blog-assets/figures/2026-07-01-qwen3-omni-optimization/qwen3-omni-cuda-graph-stages.svg)

图 3：每个阶段在不同位置捕获图。Thinker 和 Talker 在 vLLM 的外层图下解码；Talker 的内层 code predictor 用 torch.compile 编译而不是再包一层图；Code2Wav 使用内层 CUDAGraphDecoderWrapper。

#### Stage 0 — Thinker：vLLM 外层解码图

Thinker 是自回归多模态阶段（`LLM_AR`）。当 `enforce_eager` 为 false 时，它在解码路径上使用 vLLM 标准的 CUDA Graph 捕获——与纯文本 LLM 服务相同的机制。这消除了长 Thinker 生成过程中重复的 CPU 侧内核发射。

#### Stage 1 — Talker：外层解码图 + 编译的 code predictor

当 `enforce_eager: false` 时，Talker 阶段同样走 vLLM 的外层 CUDA Graph 路径。每个 Talker 解码步还会额外调用 **code predictor**——一个输出 RVQ 编解码码字的短重预填充 transformer。这条内层路径单独优化：

- **`torch.compile`** 融合 5 层 predictor 前向（`dynamic=False`、`epilogue_fusion=False`），让 RMSNorm/RoPE 在数值上与参考路径对齐，同时仍能减少每步内核数量。
- 在 CUDA 上，code predictor 默认**不**启用第二层手动 CUDA Graph（`use_cuda_graphs=False`），因为那会与 vLLM 的 Talker `CUDAGraphWrapper` 冲突。外层 Talker 图与编译的内层前向互补：一个捕获 AR 阶段循环，另一个融合 codec 预测的微前向。

可选的前缀图桶（连接器配置中的 `code_predictor_prefix_graphs`）在显式启用时可以捕获更多稳定的 predictor 形状。

#### Stage 2 — Code2Wav：内层声码器图

Code2Wav 是生成阶段（`LLM_GENERATION`），不是 AR 循环。它的图路径是**内层** `CUDAGraphDecoderWrapper`，而非 vLLM 的外层包装器：

```
# Enabled during weight load when stage enforce_eager is false
self.code2wav.enable_cudagraph(
    codec_chunk_frames=chunk_frames,
    codec_left_context_frames=left_frames,
)
```

**来自连接器配置的形状分桶。** 预热之前，包装器从阶段连接器配置读取 `codec_chunk_frames` 与 `codec_left_context_frames`。捕获会枚举异步分块和全量负载解码在运行时会命中的 `(batch, num_quantizers, frames)` 桶——包括来自 `initial_codec_chunk_frames` 的更小首块。

**声码器预热。** `precompute_snake_caches()` 在图捕获之前运行，使 SnakeBeta 激活不必在捕获的解码循环内反复付出初始化成本。

**分块分发。** 在异步分块模式下，`chunked_decode_streaming` 把稳定分块委托给 `_cudagraph_wrapper.chunked_decode_with_cudagraph`；形状与已捕获桶匹配时，全量负载路径使用包装器的批量解码入口。

**你能得到什么。** 在基准扫描中为全部三个阶段开启 CUDA Graph，req/s 从 **2.2** 提升到 **8.6**（+299%），平均音频 TTFP 从 **5884 ms** 降到 **2790 ms**，平均音频 RTF 从 **1.15** 降到 **0.59**。大部分收益来自同时消除 Thinker 文本生成、Talker codec 解码和 Code2Wav 声码器前向的发射开销。

### 3. 异步分块：流水线化的阶段间交接

**为什么。** CUDA Graph 让每个阶段更快，但流水线仍是**屏障同步**的：Thinker 结束之前 Talker 不能启动，Talker 攒齐完整负载之前 Code2Wav 不能出音频。因此首音频延迟跟随完整的 Thinker 生成加完整的 Talker 预填充——哪怕产出第一段可听的分块只需要几个 codec 帧。

**为什么有效。** 异步分块用**流水线化的部分交接**取代全量负载屏障。Thinker 增量地发出嵌入行；Talker 累积 codec 帧并按 `initial_codec_chunk_frames` / `codec_chunk_frames` 边界切片；异步调度器让分块传输与阶段计算重叠，于是前一个阶段还在解码时下一个阶段就可以开始工作——首音频在几个 codec 帧之后就能就绪，而不是等完整的 Thinker 生成加 Talker 预填充。

![图 4：没有异步分块时，每个阶段都要等前一阶段的完整负载，首音频跟随完整 Thinker 生成加 Talker 预填充。异步分块让部分交接重叠，Code2Wav 只需几个 codec 帧就可以开始出音频。](https://vllm.ai/blog-assets/figures/2026-07-01-qwen3-omni-optimization/qwen3-omni-async-chunk-timeline.svg)

图 4：没有异步分块时，每个阶段都要等前一阶段的完整负载，首音频跟随完整 Thinker 生成加 Talker 预填充。异步分块让部分交接重叠，Code2Wav 只需几个 codec 帧就可以开始出音频。

**你能得到什么。** 异步分块是扫描中音频 TTFP 最大的收益：平均音频 TTFP 从 **2790 ms**（CUDA Graph）降到 **655 ms**。

### 4. 异步输出：非阻塞的负载构造

**为什么。** 异步分块把 Thinker→Talker→Code2Wav 流水线化，但**同步负载构造**仍可能阻塞解码 worker。如果 Thinker 必须在每个分块边界完整组装连接器负载——拷贝嵌入和隐藏状态——下一个解码步才能开始，那么即使阶段交接已增量化，GPU 时间仍会流失在 Python 调度上。

**为什么有效。** `async_omni_output` 把负载构造与阶段交接解耦：Thinker 把解码状态交给一条非阻塞输出路径后立即返回处理下一个 token，连接器则异步组装并发出分块。

![图 5：异步输出前后的解码步间隔。同步负载构造时，GPU 在 Talker 步之间空闲约 2.8 ms；把负载组装移出解码路径后，步骤首尾相接，步间间隔缩小到约 41 µs。](https://vllm.ai/blog-assets/figures/2026-07-01-qwen3-omni-optimization/qwen3-omni-async-output-step-gap.svg)

图 5：异步输出前后的解码步间隔。同步负载构造时，GPU 在 Talker 步之间空闲约 2.8 ms；把负载组装移出解码路径后，步骤首尾相接，步间间隔缩小到约 41 µs。

**你能得到什么。** 在并发 64 的异步分块之上，异步输出让平均音频 TTFP 保持在 **631 ms** 附近，同时把平均音频 RTF 从 **0.63** 降到 **0.47**。

### 5. 阶段副本：扩展 Talker 与 Code2Wav

**为什么。** 负载下三个阶段不会同等饱和。对每个请求，Thinker 只生成一次文本，但 Talker 和 Code2Wav 随后要运行数百个短解码步和声码器前向，把文本渲染成音频——语音侧的持续小步工作多得多。因此随着并发攀升，Talker 和 Code2Wav 先饱和：并发 64 时任何一者的单副本都会成为尾部瓶颈，而 Thinker 仍有余量。扩展整条流水线可以解决问题，却会因复制大型多模态 Thinker 而浪费内存。

**为什么有效。** 副本只给饱和的阶段增加容量，而不是整条流水线。GPU 0 上的单个 Thinker 供分布在 GPU 1 和 2 上的 2× Talker 与 2× Code2Wav 副本使用：额外副本吸收语音侧的积压，重量级的多模态阶段保持单份。基准部署配置用以下方式启用：

```
{
  "stage_overrides": {
    "1": {"num_replicas": 2, "devices": "1,2"},
    "2": {"num_replicas": 2, "devices": "1,2"}
  }
}
```

![图 6：异步分块与阶段副本针对的是流水线的语音生成一侧，Talker 和 Code2Wav 在并发负载下可能在那里成为瓶颈。](https://vllm.ai/blog-assets/figures/2026-07-01-qwen3-omni-optimization/qwen3-omni-async-replica.svg)

图 6：异步分块与阶段副本针对的是流水线的语音生成一侧，Talker 和 Code2Wav 在并发负载下可能在那里成为瓶颈。

**你能得到什么。** 在异步输出之上加副本，并发 64 时达到 **11.7** req/s——扫描中的最高吞吐——同时平均音频 TTFP 保持在 **632 ms** 附近、平均音频 RTF 保持在 **0.47** 附近。副本相对单个 Talker/Code2Wav 的优势随并发攀升而扩大，因为语音阶段最先饱和。

### 6. 热路径清理：Talker 解码与连接器负载

**为什么。** 批处理、图、异步分块和副本消除的是结构性、框架级的瓶颈——这些优化适用于大多数多模态服务流水线。剩下的是模型内部的：剖析 Talker 解码循环仍能看到一长串小开销，它们每步重复出现，因此随语句长度增长——冗余的连接器流量、构造负载时每步的 `torch.cat` 和 CPU 序列化、codec 预测器里的 Python 分发，以及对下一步马上要在 GPU 上使用的解码状态做设备到主机的读取。

**为什么有效。** 下面的每一项修复都消除其中一种重复开销——或削减每次部署的固定开销——且不改变音频输出：

**仅解码的连接器交接。** Chunk 0 仍传输完整的 Thinker 预填充；此后的每个解码步只发送新的 `embed.decode` 行，不再重传完整的预填充嵌入与隐藏状态张量。连接器流量保持**每步 O(1)**，而不是随 prompt 长度增长；每次交接还避免了冗余的 CPU 序列化和跨阶段拷贝——否则它们会在长语句的每个 Talker 步上重复。

**单 GPU 执行器默认值。** 去掉 `distributed_executor_backend` 隐式的 `"mp"` 默认值后，单 GPU 部署可以使用 `uni` 执行器，避免多进程启动、IPC 和 worker 同步开销——这些在每步延迟最要紧的低并发路径上尤其重要。

**连接器负载构造。** 此前累积 Thinker 与 Talker 负载要在每个分块边界反复付出 `torch.cat`。改为按 token 传递解码嵌入并裁掉冗余组装，消除了这些分配和拷贝工作。同一组改动还会在请求的最终阶段就在本地时跳过构造下游 pooler/多模态 CPU 负载，避免在不喂给其他阶段的路径上做隐藏状态 D2H。

**Talker code predictor 重写。** 旧路径通过 Hugging Face `generate()` 驱动非常短的 codec 预测器序列，在每个 Talker 步上附加 Python 分发、动态分配和 KV 缓存开销。重写使用 SDPA 的重预填充、原生 GQA、内联 top-k 采样、缓存的模块引用，以及内层 transformer 上的 `torch.compile`。在 CUDA 上，这条编译路径位于 vLLM 的 Talker CUDA Graph 之下，而不是加一层冲突的第二图（见 §2）。

**常驻 GPU 的解码状态与阶段本地快路径。** `hidden_states.last`、`hidden_states.trailing_text`、`embed.tts_pad_projected`、`codes.audio` 等中间张量保存在 `model_intermediate_buffer` 中，下一步在设备上直接复用，而不必做会把每个 Talker 步串行化的设备到主机往返。Talker 和 Code2Wav 还跳过多模态 `get_mrope_input_positions`——它们只需要廉价的线性位置——`_store_value` 在张量已在 CPU 上时避免冗余的 `.to("cpu")` 工作。

**数值精度护栏。** 这些重写不能回退音频质量，因此 RMSNorm 方差和 RoPE 保持 fp32（`epilogue_fusion=False`），按调用分配的嵌入缓冲避免跨请求混叠——上述加速是在这一约束之上运行的，而不是对抗它。

**你能得到什么。** 热路径清理消除随语句长度增长的开销。在一个长上下文单请求测试中，E2EL 从 21.28 s 降到 7.37 s，音频 TTFP 从 3197 ms 降到 1796 ms，音频 RTF 从 0.71 降到 0.28。这些改动与上面的层叠加，并体现在 DFX 性能套件基线中，而不是扫描表中单独的一行。

## 验证结果

下面的图表画出[优化概览](#optimization-overview)汇总的同一轮基准扫描——Batch、CUDA Graph、异步分块、异步输出与阶段副本——覆盖全部四个并发级别（`1`/`16`/`32`/`64`），每个都从 **Batch** 基线起步。

![图 7：c=1（橙色）、c=16（紫色）、c=32（绿色）和 c=64（红色）下的请求吞吐量（req/s）。阶段副本在 c=64 达到 11.7 req/s、c=32 达到 6.8 req/s，高于 2.2 req/s（c=64 的 Batch）。](https://vllm.ai/blog-assets/figures/2026-07-01-qwen3-omni-optimization/qwen3-omni-bench-reqps.svg)

图 7：c=1（橙色）、c=16（紫色）、c=32（绿色）和 c=64（红色）下的请求吞吐量（req/s）。阶段副本在 c=64 达到 11.7 req/s、c=32 达到 6.8 req/s，高于 2.2 req/s（c=64 的 Batch）。

![图 8：c=1、16、32 和 64 下的平均音频 RTF。Batch 在负载下达到或超过实时（c=64 时 RTF 高至 1.15）；异步输出与副本让 c=32/c=64 的 RTF 保持在约 0.47 或以下。](https://vllm.ai/blog-assets/figures/2026-07-01-qwen3-omni-optimization/qwen3-omni-bench-rtf.svg)

图 8：c=1、16、32 和 64 下的平均音频 RTF。Batch 在负载下达到或超过实时（c=64 时 RTF 高至 1.15）；异步输出与副本让 c=32/c=64 的 RTF 保持在约 0.47 或以下。

![图 9：c=1、16、32 和 64 下的平均音频 TTFP（毫秒，对数刻度）。异步分块把 c=64 的 TTFP 从约 5884 ms（Batch）降到约 655 ms。](https://vllm.ai/blog-assets/figures/2026-07-01-qwen3-omni-optimization/qwen3-omni-bench-ttfp.svg)

图 9：c=1、16、32 和 64 下的平均音频 TTFP（毫秒，对数刻度）。异步分块把 c=64 的 TTFP 从约 5884 ms（Batch）降到约 655 ms。

### 综合解读三组扫描

三组扫描讲的是同一个故事：每一层针对不同的瓶颈，合在一起则相互放大。

- **吞吐量（图 7）。** 请求吞吐量从 Batch 基线的 **2.2 req/s** 攀升到并发 64 的 **11.7 req/s**（约 5.4×），在并发 32 从 **1.1** 提升到 **6.8 req/s**。单项最大跃升是 CUDA Graph（约 4×）；异步输出在高并发下提供最后的大推动，阶段副本把吞吐量推向峰值，且余量随并发上升而扩大。
- **实时因子（图 8）。** 平均音频 RTF 从 Batch 下高于实时的 **1.15** 降到并发 64 的 **0.47**——解码从负载下落后于播放，变成从容领先于播放。
- **首包延迟（图 9）。** 并发 64 时平均音频 TTFP 从 **约 5884 ms** 降到 **约 632 ms**，其中异步分块贡献最大的单次削减（降到 **约 655 ms**），后续各层则保住了这一收益。

结论是：没有任何单一层独自扛起全部收益——CUDA Graph 与异步分块主导延迟削减，异步输出与阶段副本在并发 32 和 64 下补上吞吐余量。把它们叠起来，就把一条负载下勉强跟得上的流水线，变成了实时余量充裕的流水线。

## 致谢

我们感谢 [vLLM-Omni](https://github.com/vllm-project/vllm-omni) 中的 Qwen3-Omni 贡献者，包括 Haiyan Wu、Taichang Zhou、Canlin Guo、Ruirui Yang、Ziming Huang、Wengang Zheng、Lianhao Xu、Han Gao、Junhong Liu、Samit Huang、Hao Chen、Alex Brooks、Chenguang Zheng、Peiqi Yin、Wenjing Chen、Nick Cao、Shunyang Li、Yong Yang、Divyansh Singhvi、Yueqian Lin、Dayu Qiu、Roger Wang 和 Hongsheng Liu，感谢他们的贡献与反馈。

---

## 参考文献

**源码与配置**

- vLLM-Omni 中的 Qwen3-Omni 流水线拓扑：[`pipeline.py`](https://github.com/vllm-project/vllm-omni/blob/main/vllm_omni/model_executor/models/qwen3_omni/pipeline.py)
- vLLM-Omni 中的 Qwen3-Omni 模型包装器：[`qwen3_omni.py`](https://github.com/vllm-project/vllm-omni/blob/main/vllm_omni/model_executor/models/qwen3_omni/qwen3_omni.py)
- Qwen3-Omni 阶段输入处理器：[`stage_input_processors/qwen3_omni.py`](https://github.com/vllm-project/vllm-omni/blob/main/vllm_omni/model_executor/stage_input_processors/qwen3_omni.py)
- Qwen3-Omni 部署配置：[`qwen3_omni_moe.yaml`](https://github.com/vllm-project/vllm-omni/blob/main/vllm_omni/deploy/qwen3_omni_moe.yaml)
- Qwen3-Omni 异步分块性能配置：[`test_qwen3_omni_async_chunk.json`](https://github.com/vllm-project/vllm-omni/blob/main/tests/dfx/perf/tests/test_qwen3_omni_async_chunk.json)
- Qwen3-Omni 多副本性能配置：[`test_qwen3_omni_multi_replicas.json`](https://github.com/vllm-project/vllm-omni/blob/main/tests/dfx/perf/tests/test_qwen3_omni_multi_replicas.json)
- Qwen3-Omni 模型仓库：[Qwen/Qwen3-Omni-30B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct)

**优化 PR**

- CUDA Graph（§2）：Thinker [vllm-omni#523](https://github.com/vllm-project/vllm-omni/pull/523)、Talker [vllm-omni#669](https://github.com/vllm-project/vllm-omni/pull/669)、Code2Wav [vllm-omni#2376](https://github.com/vllm-project/vllm-omni/pull/2376)
- 异步分块（§3）：跨阶段分块计算/通信 [vllm-omni#727](https://github.com/vllm-project/vllm-omni/pull/727)、重叠分块 IO 与计算的异步调度 [vllm-omni#951](https://github.com/vllm-project/vllm-omni/pull/951)、包间延迟优化 [vllm-omni#1656](https://github.com/vllm-project/vllm-omni/pull/1656)
- 异步输出（§4）：异步 omni 输出物化 [vllm-omni#4476](https://github.com/vllm-project/vllm-omni/pull/4476)
- 阶段副本（§5）：支持多阶段部署 [vllm-omni#2396](https://github.com/vllm-project/vllm-omni/pull/2396)、omni 阶段运行时与分布式副本控制平面 [vllm-omni#3855](https://github.com/vllm-project/vllm-omni/pull/3855)
- 热路径清理（§6）：[vllm-omni#3007](https://github.com/vllm-project/vllm-omni/pull/3007)、[vllm-omni#3164](https://github.com/vllm-project/vllm-omni/pull/3164)、[vllm-omni#3878](https://github.com/vllm-project/vllm-omni/pull/3878)

如果你对 Qwen3-Omni 服务或全模态推理感兴趣，欢迎加入 [vLLM Slack](https://slack.vllm.ai) 的 `#sig-omni` 频道，或在 [vLLM-Omni GitHub](https://github.com/vllm-project/vllm-omni) 提 issue。
