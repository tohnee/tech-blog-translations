---
title: "vLLM-Omni 中的 TTS 推理工程实践"
title_en: "Engineering TTS Inference in vLLM-Omni"
source: https://vllm.ai/blog/2026-06-23-vllm-omni-tts
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM-Omni 中的 TTS 推理工程实践

> 原文：[Engineering TTS Inference in vLLM-Omni](https://vllm.ai/blog/2026-06-23-vllm-omni-tts) · vLLM 博客

作者：vLLM-Omni TTS 团队

[#性能](https://vllm.ai/blog/tags/performance)[#多模态](https://vllm.ai/blog/tags/multimodal)[#推理](https://vllm.ai/blog/tags/inference)

vLLM-Omni 最初以全模态模型支持起步，此后扩展到多个文本转语音（TTS）系统，包括 Qwen3-TTS、VoxCPM2、Fish Speech S2 Pro 与 Higgs Audio V3。本文介绍我们在适配和优化这些模型时遇到的具体工程问题、采用的解决方案，以及背后的工程权衡。

---

## TTS 推理与传统 LLM 推理的差异

TTS 与纯文本 LLM 推理都使用自回归模型，但二者的服务瓶颈不同。

**TTS 是一条流水线，通常包含多个模型阶段。** 典型的 TTS 系统至少有两个阶段：一个 Talker 自回归地预测编解码（codec）token，一个 Code2Wav 模块从这些编解码 token 重建波形音频。这两个阶段的计算特征差异极大：Talker 是受延迟约束的单 token 解码负载，而 Code2Wav 是受吞吐量约束的并行解码器。如果调度器对两个阶段一视同仁，Talker 的延迟会阻塞 Code2Wav 的输入，而 Code2Wav 的并行能力也得不到充分利用，延迟和吞吐量都会受损。

**流式输出有严格的延迟预算。** 在语音合成中，用户期望在几百毫秒内听到第一包音频。连接器（connector）层必须支持分块流式传输，而块大小直接影响 TTFP，即 Time To First Audio Packet（首音频包延迟）。块太小，Code2Wav 没有足够上下文来保持音频在块边界处的连续性；块太大，首包延迟又变得不可接受。

**吞吐量依然重要。** 在在线服务中，单张 GPU 能承受多少并发、每秒墙钟时间能生成多少秒音频，直接决定部署成本。TTS 的吞吐量优化比 LLM 更复杂，因为 Talker 和 Code2Wav 的瓶颈不同，二者之间的连接器还会带来自身的传输开销。提升吞吐量意味着在平衡两个阶段的同时消除各自内部的瓶颈。

![vLLM-Omni TTS 服务流水线](https://vllm.ai/blog-assets/figures/vllm-omni-tts/tts-serving-pipeline.png)

vLLM-Omni TTS 服务流水线

本文余下部分首先概述我们使用的优化技术，然后以 Qwen3-TTS 为主例走完整条优化路径。接着我们用 VoxCPM2、Higgs Audio V3 和 Fish Speech S2 Pro 说明为什么不同的 TTS 架构需要不同的服务策略。

---

## 优化概览

不同的 TTS 模型有不同的瓶颈。vLLM-Omni 不对所有模型套用同一套固定的优化配方，而是根据每个模型的流水线结构、解码状态、批形状（batch shape）和数值约束来选择优化手段。

| 技术 | 适用对象 | 为何重要 |
| --- | --- | --- |
| 阶段分离与连接器分块 | Qwen3-TTS、Higgs Audio V3 | 让 Talker 延迟与 Code2Wav 吞吐量可以独立调优。 |
| 批量化解码预处理 | Qwen3-TTS | 减少 Talker 解码热路径中每个请求重复的 Python 工作。 |
| 整前向 `torch.compile` | VoxCPM2 | 让 Dynamo 看到更完整的 MiniCPM4 前向循环，减少 Python 与编译代码之间的边界。 |
| CFM/LocDiT 解码尾部批处理 | VoxCPM2 | 把大量微小的逐请求扩散调用合并为更大的 GPU 批。 |
| 常驻 GPU 的解码状态 | Higgs Audio V3 | 将多码本状态更新移出 Python 循环，减少同步。 |
| 模型专属的 q\_len=1 注意力 | Fish Speech S2 Pro | 为纯解码注意力做特化，而不是为通用分页/变长路径付出代价。 |

关键在于，并非每项优化都适用于所有 TTS 架构。工程上的挑战在于为正确的模型形态选择正确的抓手。

---

## Qwen3-TTS：一条完整的优化路径

Qwen3-TTS 是 Qwen 团队推出的语音生成模型家族。它采用离散多码本语言模型架构与 12 Hz tokenizer 进行声学压缩和高保真重建[1](#user-content-fn-11)。它的三个变体——用于音色克隆的 Base、用于预定义说话人并支持指令式情感与风格控制的 CustomVoice，以及根据音色、情感和韵律的自然语言描述设计新声音的 VoiceDesign——共享同一套两阶段架构：Talker 自回归地预测编解码 token，Code2Wav 并行解码这些 token。Qwen3-TTS 的 Code2Wav 是一个轻量的非 DiT 解码器，不需要扩散模型那样的迭代去噪循环。

在本文讨论的四个模型中，Qwen3-TTS 的流水线形态最为标准：Talker → 连接器 → Code2Wav。这使它成为走完整条 TTS 推理优化流程的合适示例。

### 1. 流式：把连接器分块与 Code2Wav 解码窗口解耦

第一个优化目标是流式输出。在 Qwen3-TTS 的早期实现中，连接器流式分块与 Code2Wav 解码分块绑定在同一个分块参数上，主要是 `codec_chunk_frames`。

连接器把编解码 token 从 Talker 传给 Code2Wav。在流式模式下，如果连接器发送非常小的块，Code2Wav 看到的解码块也很小，这会损害跨块音频连续性。如果为了音质增大块大小，首包延迟又会增加。

我们通过引入相互独立的参数来解耦这两个职责：

- `codec_chunk_frames`：连接器流式分块大小，控制 Talker 到 Code2Wav 的传输节奏。
- `decode_chunk_frames` 与 `decode_left_context_frames`：Code2Wav 内部解码窗口与左侧上下文，与连接器分块保持独立。
- `initial_codec_chunk_frames`：更小的首个编解码块，让 Code2Wav 可以更早启动，后续块再回到常规大小。

有了这一设计，连接器可以用较小的块大小来降低首包延迟，而 Code2Wav 保持 300 帧的解码窗口外加 25 帧左侧上下文以维持跨块音质。两个旋钮可以独立调节[2](#user-content-fn-6)。

![Qwen3-TTS 连接器分块解耦](https://vllm.ai/blog-assets/figures/vllm-omni-tts/qwen3-tts-connector-chunking.png)

Qwen3-TTS 连接器分块解耦

### 2. 吞吐量：Stage 0 解码预处理

解决流式延迟后，下一个瓶颈是吞吐量。第一道障碍是 Talker 解码循环。Qwen3-TTS 的每个 Talker 解码步都需要请求级预处理：说话人嵌入（speaker embedding）准备、`trailing_text` 维护和输入嵌入构造。c=1 时这些开销很小；c=64 时每个解码步要循环 64 个请求，Python 侧循环加张量切片就成为可见的瓶颈。

为了定位这些开销，我们在 H20 × 2 上以 c=64 的音色克隆场景对 Talker 解码做了性能剖析。在更全面的热路径优化之前的一次热运行（warm run）中，模型外的 Python 与 runner 侧工作——包括 `preprocess_decode_batch`、`make_omni_output`、`process_additional_info`、`build_mm_cpu` 以及记账式同步——每个解码步处于毫秒量级。每步几毫秒单独看不大，但一句话可能需要约 200 个解码步；在 c=64 时，这一开销会在整个序列中不断重复，成为端到端延迟的重要部分。

GPU 利用率也印证了这一点。以 `nvidia-smi` 在 c=64 下采样，Stage 0 和 Stage 1 的基线平均 GPU 利用率分别约为 14% 和 6%。GPU 常常在等 Python 调度、小张量分配和内核启动开销，而不是在等计算。这正是瓶颈不在 GPU 原始 FLOPs、而在服务路径开销的原因。

第一个具体目标是说话人嵌入准备。在 Qwen3-TTS 音色克隆模式下，每个请求用参考音频提取说话人嵌入，并在解码过程中执行 mel/STFT 计算。原始路径为每个请求在 CPU 上计算 mel 频谱再拷贝到 GPU。高并发下，这变成了大量小的 CPU 到 GPU 传输和内核启动。我们把 mel 基与窗缓冲缓存在 GPU 上，并把 mel/STFT 计算批量放到 GPU 上执行，消除了重复的 CPU 工作和 H2D 传输。

下一个目标是 `trailing_text`。解码期间，Talker 维护一个 `trailing_text` 滑动窗口，缓存已生成 token 的嵌入。每个解码步追加当前 token 的嵌入并移除最旧的 token。原始实现使用张量切片与拼接，频繁分配新张量。优化后的路径改为跟踪一个偏移量，只在偏移越过阈值或到达缓冲区末尾时才压缩（`_TRAILING_TEXT_COMPACT_MIN_FRAMES = 64`）；中间的解码步直接按偏移索引，不再分配新张量。

批量化的 `preprocess_decode_batch` 路径消除了逐请求解码开销的一大来源[3](#user-content-fn-7)。下文的最终吞吐数字来自叠加后的完整优化路径，包括 Stage 0 批处理、连接器改动、异步 D2H、runner 热路径清理以及 CUDA Graph 调优[4](#user-content-fn-1)[2](#user-content-fn-6)[3](#user-content-fn-7)。在最终叠加运行中，Qwen3-TTS 在 H20 × 2 上的音频吞吐量从 26.55 audio-s/s 提升到 42.88 audio-s/s（+61.5%），P99 E2EL 从 17.7s 降到 9.0s。

![Qwen3-TTS Stage 0 发射合并](https://vllm.ai/blog-assets/figures/vllm-omni-tts/qwen3-tts-stage0-dispatch-consolidation.png)

Qwen3-TTS Stage 0 发射合并

上面的 trace 窗口展示的是对 Stage 0 预处理做批处理后的服务路径效果：解码热路径中的 CPU 发射调用更少、小的 GPU 内核切片更少，而不是在主张更高的 GPU 利用率。

### 3. 热路径清理

预处理批量化之后，剩余的性能剖析显示还有许多小的 Python 开销。每项都很小，但在高频的 c=64 解码循环中会累积。

`req_id_to_index` 此前使用 `req_ids.index()`，把查找变成每个解码步内的 O(N²) 列表扫描。换成字典后查找变为 O(1)。非流式请求不需要在 orchestrator 中走逐输出的流式路径，因此我们提前跳过该路径。编解码禁止掩码（codec-disallowed mask）被预计算为缓冲区，使 `compute_logits` 可以直接使用 `masked_fill`，而不必每次重建掩码[4](#user-content-fn-1)。

Qwen3-TTS 在多处使用 CUDA Graph。Talker 的 code predictor 根据部署配置有自己的图路径。这里我们聚焦 Code2Wav 解码器的 CUDA Graph。解码器输入形状为 `(batch, num_quantizers, codec_frames)`。在分块解码中，`codec_frames` 只有少数几种取值：流式块加左侧上下文、非流式的 `decode_chunk_frames + decode_left_context_frames`（300 + 25 = 325），以及尾块。这些取值可以在预热（warmup）时枚举。`CUDAGraphDecoderWrapper` 按 `(batch_size, frames)` 捕获图，推理时用 `bisect_left` 选择最近的填充桶（padded bucket）。如果没有匹配的图，则回退到 eager 执行。

在使用 `qwen3_tts.yaml` 的多轮 c=16 重复测试中，Code2Wav CUDA Graph 命中率从 88% 起步，五轮连续测试后稳定在 81% 左右。主要的单样本形状，如 `(1, 98) -> 169`、`(1, 73) -> 73`、`(1, 123) -> 169` 和 `(1, 325) -> 325`，都命中了已捕获的桶。回退主要来自批大小 > 1 的形状，如 `(2, 98, 169)` 和 `(8, 73, 73)`。整个运行过程中 `stream_capture_fallbacks=0`，即没有回退是由流捕获失败引起的。

### 4. 数值精度：code predictor 的 fp32 对齐

Talker 的 code predictor 有一条对精度敏感的路径。它处理的序列非常短，通常只有 2–8 个 token，且反复执行预填充。vLLM 的 bfloat16 融合内核与参考实现可能有细微差异。在这条短序列、高频的路径上，这些微小差异会累积，几十步之后就可能影响音频质量。

修复方法是把 code predictor 的层拆开，让选定的运算保持 fp32：RMSNorm 方差、RoPE cos/sin、注意力和 QKV 投影都使用 PyTorch 原生实现，与参考路径做到位级对齐。

### 5. 验证

叠加这些优化后，Qwen3-TTS 在 H20 × 2、c=64 的音色克隆场景下音频吞吐量提升 61.5%，P99 端到端延迟几乎减半。完整数字见性能数据部分。

我们还用 H20 × 2、音色克隆和流式输出做了一轮热并发扫描：

| c | 平均 TTFP | 平均 E2E | P50 TTFP | P50 E2E |
| --- | --- | --- | --- | --- |
| 1 | 70.61ms | 564ms | 70.61ms | 564ms |
| 8 | 268.75ms | 1.55s | 287.15ms | 1.70s |
| 16 | 451.32ms | 2.62s | 516.15ms | 2.75s |
| 32 | 637.43ms | 5.05s | 634.22ms | 5.10s |
| 64 | 1127.93ms | 8.73s | 1051.05ms | 8.78s |

从 c=1 到 c=64，E2E 从 0.56s 增长到 8.73s，并非按 64× 线性增长。热态高并发服务会摊薄固定成本，但在 c=64 时，Talker 与调度路径仍是排队的主要来源。这正是热路径清理和 CUDA Graph 依然重要的原因。

---

## VoxCPM2：单阶段混合 TTS

VoxCPM2 是 OpenBMB 推出的无 tokenizer TTS 模型。它采用扩散-自回归混合设计，运行在 AudioVAE V2 的隐空间（latent space）中[5](#user-content-fn-12)。它的 Talker 是一个四段级联：

```
MiniCPM4 (28 layers, PagedAttention) → FSQ → MiniCPM4 ResidualLM (8 layers) → LocDiT (CFM solver) → AudioVAE
```

LocDiT 执行 CFM（Conditional Flow Matching，条件流匹配）扩散去噪，AudioVAE 重建 48 kHz 波形音频。在 vLLM-Omni 中，VoxCPM2 没有被拆成多个运行时阶段，而是作为单阶段 AR TTS 流水线运行：MiniCPM4、FSQ、ResidualLM、LocDiT 和 AudioVAE 全部在同一个模型实例内执行，模型直接输出音频。这避免了阶段之间的隐变量传输，也让解码尾部 CFM/LocDiT 与 VAE 路径的跨请求批处理更容易实现。

![VoxCPM2 单阶段混合流水线](https://vllm.ai/blog-assets/figures/vllm-omni-tts/voxcpm2-single-stage-pipeline.png)

VoxCPM2 单阶段混合流水线

与采用 Talker 到 Code2Wav 两阶段流水线的 Qwen3-TTS 不同，VoxCPM2 的优化聚焦两个问题：如何让 28 层的 MiniCPM4 更快，以及如何避免 CFM/LocDiT 在高并发下让 GPU 利用不足。

### 探索 torch.compile

28 层的 MiniCPM4 是 VoxCPM2 Talker 中最重的部分，因此第一个优化目标是 `torch.compile`。最终效果最好的路径并不是我们最初预期的那条。

第一次尝试分别编译每层的 `mlp` 和 `o_proj`：28 层 × 2 个模块 = 56 个编译区域，使用 `fullgraph=True`[6](#user-content-fn-3)。问题在于 Dynamo 无法跨编译区域边界优化。每个边界都会增加一次 Python → 编译代码 → Python 的切换，56 个区域意味着每个解码步要经历大量切换。

随后我们把整个 `Model.forward` 用 `torch.compile`（`fullgraph=False`）包裹[7](#user-content-fn-4)。这让 Dynamo 能看到完整的 28 层循环。PagedAttention 仍会造成图断裂（graph break），但 Dynamo 只需记住少量子图。每步发射从许多小区域减少到少数几个较大区域。RTF 从约 0.21 降到约 0.13，这是对 VoxCPM2 单项收益最大的优化。

为了量化这一点，我们对三种配置做了剖析：eager、逐层编译和整图/统一图。逐层编译减少了部分内核数量和内核时间，但发射次数没有下降。整图/统一图才是关键一步：`cudaLaunchKernel` 次数下降约 71%，内核事件约 30%，内核时间约 27%。单请求 E2E 在逐层编译下下降约 2.6%，整图下约 6.5%。

![VoxCPM2 编译发射时间线与计数器](https://vllm.ai/blog-assets/figures/vllm-omni-tts/voxcpm2-compile-dispatch-combined.png)

VoxCPM2 编译发射时间线与计数器

这张时间线以 profiler 视图为主，内嵌的全 trace 计数器说明了为什么逐层编译不够：发射次数一直持平，直到整前向编译路径减少了 Python 与编译代码之间的边界。

我们还尝试过 `mode="reduce-overhead"`，它会启用自动 CUDA Graph 捕获。但这与 PagedAttention 有状态的 KV 缓存冲突：图捕获期间 `slot_mapping` 被固定下来，重放（replay）时可能把注意力结果写入错误的 KV 缓存位置，导致错误的停止 logits 和提前截断。

`fullgraph=True` 无法容忍 PagedAttention 和自定义精度边界造成的图断裂；`fullgraph=False` 在保留整前向视图的同时，允许这些边界回退到 eager 执行。

### CFM/LocDiT 解码尾部批处理

单请求延迟改善后，高并发瓶颈转移到 CFM/LocDiT。每个请求在 CFM 去噪期间运行一个 LocDiT 注意力/GEMM 负载，但单请求的批非常小，在 CFG 下通常只有 B=2。这远远填不满 GPU。高并发下，各请求独立运行 LocDiT 会让 GPU 利用不足。

解决方案是跨请求批量处理 CFM/LocDiT 解码尾部。我们从多个请求收集 `lm_h`、残差输出和前缀特征条件，然后一次性以批方式运行 `dit_proj`、CFM/LocDiT、`feat_encoder` 和 `stop_head`，再把结果散回各请求状态。结合每三个隐块做一次 VAE 解码、批量 VAE 解码、合并的音频 D2H 拷贝，以及 LocDiT 融合 QKV / 融合 gate-up MLP，H20 × 1 在 c=64 下的吞吐量从 4.19 req/s 提升到 10.83 req/s（+158.8%），音频吞吐量从 12.16 audio-s/s 提升到 33.07 audio-s/s（+172.0%）[8](#user-content-fn-5)。

CFM 的 Euler 积分循环内还有一个同步问题。对 0 维 GPU 张量调用 `.item()` 会强制 GPU 到 CPU 的同步。原路径在每个扩散步做 4 次。以 10 个时间步、约 60 个解码步计算，一个请求可能触发约 2,400 次同步。用 GPU 侧的 `.copy_()` 广播替代 `.item()` 后，该循环不再需要 CPU 参与。

VAE 解码也有一个结构性问题。最初的实现采用"累积再解码"模式：每五步把此前生成的所有隐补丁拼接起来，把整个前缀重新解码一遍，总工作量是 O(N²)。改为滑动窗口解码——每次调用 12 帧 pad 上下文加 4 个新帧——工作量降到 O(N)。长文本 RTF 不再随文本长度增长，各长度都保持在 RTF 0.132–0.138 左右[7](#user-content-fn-4)。

---

## Higgs Audio V3：动态批与多码本状态

Boson AI 的 Higgs Audio V3 支持 100 多种语言和零样本音色克隆。在架构上，它有几个重要特征：36 层、隐藏维度 2560 的 Qwen3 主干，GQA，使用大 `[N × V, D]` 矩阵加偏移查找的融合多码本嵌入，以及带 BOC/EOC 特殊 token 的 MusicGen 式延迟模式 `[0, 1, 2, ..., 7]`。

它整体的 Talker → Code2Wav 形态与 Qwen3-TTS 相似，但由于多码本预测和延迟模式，Talker 内部有所不同。

与 Qwen3-TTS 相比，Higgs v3 的瓶颈不同：Qwen3-TTS 受限于 Python 热路径和流式分块边界；Higgs v3 受限于复杂的多码本解码状态管理和 CUDA Graph 兼容性。

### 把解码状态搬到 GPU

Higgs v3 的主要吞吐量收益来自把逐请求的 Python 字典状态机搬进常驻 GPU 的批量张量[9](#user-content-fn-10)。这些状态包括 `_decode_last_codes`、`_decode_has_codes`、延迟计数、EOC 倒计时、生成完成标志以及相关解码元数据。收益来自减少 Python 逐请求循环、减少 D2H 同步，并把采样/状态更新逻辑挪到批量化的 GPU 热路径上。在本文报告的基准中，35.26 audio-s/s 的结果是在单张 H20、c=16、eager + 本地 MLP CUDA Graph 配置下测得的，而不是 PIECEWISE 全解码图路径。

困难之处在于 vLLM 调度器可能在解码期间重排、缩减、完成或移除请求。行级状态不能想当然地等同于请求级状态。音频 AR 状态比文本状态更复杂，因为延迟码本、EOC 渐落（ramp-down）和终止帧都有语义含义。任何一个状态滞后一步，结果就是一个音频质量问题，而不是一次干净的崩溃。GPU 状态、CPU 覆盖状态和调度器 token 必须有单一事实来源，否则停止语义会不一致。

### 让 CUDA Graph 适配动态批形状

为 Higgs v3 Talker 解码路径做 CUDA Graph 捕获时暴露了另一个问题。Talker 有一个音频反馈机制：前一个音频 token 的嵌入会替换下一个续写 token 的嵌入。实现中使用布尔掩码来选择当前处于解码状态的请求，所得张量形状取决于运行时有多少请求处于解码状态。

CUDA Graph 捕获要求流操作固定、输入输出形状固定。输出形状依赖运行时数据的布尔掩码选择违反了这一要求。

变通方法是让 CUDA Graph 路径使用统一的单 token 解码批。每个 span 长度都是 1，因此 `decode_mask` 全为 True，选择操作变成空操作并返回原张量。图看到的是稳定的全批形状，而不是依赖数据的压缩形状。

### 本地 MLP CUDA Graph 对比 PIECEWISE

本地 MLP CUDA Graph 仍是 Higgs v3 最重要的图优化。它覆盖 `post_attention_layernorm + mlp` 的主要 GPU 开销。vLLM PIECEWISE CUDA Graph 看起来更完整，因为它能覆盖更大的解码步。但实践中，Higgs v3 的多码本延迟模式使 token 布局在每个解码步之间变化，嵌入查找和注意力前的索引操作都依赖数据。PIECEWISE 在这些区域要么图断裂回 eager，要么需要额外的元数据同步。

在端到端测试中，PIECEWISE 要求禁用本地 MLP 图，这一权衡得不偿失。eager 加本地 MLP 图比 PIECEWISE 图更快。

### 一个被否决的暂存重叠设计

有一个被否决的设计仍值得记录：一步音频暂存重叠。想法是把音频暂存的 D2H 拷贝与下一个解码步重叠，以减少 GPU 空闲时间。试运行通过了，但负载测试显示 vLLM 调度器可能在解码期间重排、缩减或完成请求，指向某一行的游标可能失去与请求的映射。这种游标滞后设计在动态批处理下是结构性不安全的，它不是边界条件 bug。未来的重叠设计应以 request-id 为键，并包含 finish/remove 的排空钩子。

---

## Fish Speech S2 Pro：当通用注意力成为瓶颈

Fish Audio 的 Fish Speech S2 Pro 采用 Dual-AR 架构，在超过 1000 万小时的音频上训练，支持 80 多种语言[10](#user-content-fn-13)。在 vLLM-Omni 中，Fish Speech S2 Pro 以 slow\_ar + Fast AR + DAC 解码器的方式运行：slow\_ar 沿时间轴预测语义码本，Fast AR 在每个解码步预测残差码本，DAC 解码器从 10 个码本重建波形音频。

与以 Python 预处理为主要瓶颈的 Qwen3-TTS 不同，Fish Speech 的瓶颈在 GPU 侧。高并发下，q\_len=1 注意力占主导。通用的分页/变长注意力带有针对预填充、分块预填充、解码及其他模型形状的形状检查和分支。对 Fish 的纯解码形状而言，这些灵活性就是开销。

### 模型专属注意力内核

剖析显示，高并发下 Fish slow\_ar 的大部分时间花在 q\_len=1 的 SlowAR 注意力以及 DAC 与运行时之间的数据交接上。通用注意力必须支持很多形状，而 Fish 的解码范围窄得多：q\_len=1、fp16/bf16、head\_dim=128、块大小 16，以及 Fish 的 GQA 布局。

我们为 SlowAR 解码注意力实现了一个 Fish 专属的 Triton 内核[11](#user-content-fn-9)。它不处理预填充或其他模型。如果请求不满足形状约束，执行会回退到原始注意力路径。

该内核有两条路径。不超过 1024 token 的短序列用一次遍历的标准 online softmax。网格为 `(batch_size, num_kv_heads)`，每个 program 处理一个批行和一个 KV 头的全部 Q 头。块大小硬编码为 16，与 vLLM 的 KV 缓存块大小一致，因此块表查找就是直接的 `tl.load`，无需额外的 gather 逻辑。长序列走 split-partial-combine 路径：把序列切成段，独立计算部分 m/l/acc，再用 online softmax 递推合并。这让参考音频长上下文请求也能留在快路径上。

分发逻辑有一个细微之处。内核需要序列长度来选择短路径或长路径，但精确的序列长度在 GPU 上，读回 CPU 会引发同步。因此 runner 用已计算 token 数加已调度 token 数在 CPU 侧算出 `seq_lens_cpu_upper_bound`。该上界总是不小于真实序列长度：短路径不会读漏，长路径的切分也不会覆盖不足。CUDA Graph 捕获期间，上界被设为 `max_model_len`，因此所有图路径仍被覆盖。

![Fish Speech Stage 0 在 q\_len=1 快路径前后的运行时形状](https://vllm.ai/blog-assets/figures/vllm-omni-tts/fish-speech-stage0-runtime-shape.png)

Fish Speech Stage 0 在 q\_len=1 快路径前后的运行时形状

这张 trace 是 q\_len=1 注意力特化前后 Fish 路径的本地运行时形状视图，用于补充内核设计讨论，而不是取代基准数字。

快路径只作用于 Fish SlowAR 注意力层。模型加载时，我们遍历 `model.layers`，把每个注意力层的 `impl.forward` 换成一个包装器：约束匹配时分发到 Fish 快路径。预填充请求、非 Fish 模型和不支持的解码形状仍使用原始注意力实现。

### Fast AR 缓冲复用与编译

Fish Speech 的 Fast AR 是一个四层轻量 transformer，在每个 slow\_ar 步之后预测残差码本。它维护一个按调用持有的 KV 缓存：每个残差码本步只解码一个新 token，并把 K/V 写入预分配的 `_k_cache` 和 `_v_cache` 张量。

每个 Fast AR 解码步要投影 slow\_ar 隐藏状态、嵌入当前语义 token、逐层运行注意力和 MLP，并从 logits 采样。虽然序列很短——至多 10 个 token——但重复分配和重复预填充在 c=64 时变得可见。

我们一次性分配 `_embed_buf`、`_pos_ids`、`_k_cache` 和 `_v_cache` 并复用。`_embed_buf` 形状为 `(batch_size, num_codebooks + 1, hidden_dim)`，覆盖一次 Fast AR 解码的全部时间步。`_k_cache` 和 `_v_cache` 按层、批、KV 头、序列位置和头维度预分配，`forward_one` 可以原地读写。

我们还用 `torch.compile` 编译 Fast AR。与 VoxCPM2 的 MiniCPM4 不同，Fast AR 只有四层，编译开销很小。使用 `fullgraph=False` 是因为注意力用 `F.scaled_dot_product_attention` 而非分页注意力，SDPA 内部可能发生图断裂；Dynamo 只需记住少数子图。`dynamic=True` 让编译结果能应对批大小变化。

### DAC 与运行时侧优化

DAC 与运行时侧的改动包括几项较小的优化。编解码负载传输从 Python `list[int]` 改为张量负载：直接序列化 2D 码张量，而不是展开成 Python 整数，降低高并发下的分配与 GC 压力。fp16 DAC 支持把内存和计算减半。按帧数设限的 DAC 批处理限制一次 DAC 前向处理的帧数，防止一个长请求阻塞其他请求。异步分块处理让连接器传输与 DAC 计算重叠：slow\_ar 和 Fast AR 每个解码步产出一个 10 码本编解码帧，连接器把帧攒到 `codec_chunk_frames`，DAC 解码器处理当前块的同时连接器在累积下一块。

---

## 性能数据

以下数字来自 vLLM-Omni cookbook 基准测试。指标：

- **RTF**：生成时间除以音频时长。低于 1 表示快于实时。
- **TTFP**：Time To First Audio Packet（首音频包延迟）。
- **Tput**：音频吞吐量，即每秒墙钟时间生成的音频秒数。
- **E2EL**：端到端延迟。

### Qwen3-TTS (c=64, p=512, H20 × 2, 音色克隆)

| 指标 | 优化前 | 优化后 | 变化 |
| --- | --- | --- | --- |
| 音频吞吐量 | 26.55 audio-s/s | 42.88 audio-s/s | +61.5% |
| 中位数 E2EL | 9654ms | 5699ms | −41.0% |
| P99 E2EL | 17686ms | 8956ms | −49.4% |
| P99 TTFP | 7558ms | 5563ms | −26.4% |

### VoxCPM2 (c=64, H20 × 1, CFM 批处理前/后)

| 指标 | 优化前 | 优化后 | 变化 |
| --- | --- | --- | --- |
| 请求吞吐量 | 4.19 req/s | 10.83 req/s | +158.8% |
| 音频吞吐量 | 12.16 audio-s/s | 33.07 audio-s/s | +172.0% |

### Fish Speech S2 Pro (H20, 单 GPU, c=64, Triton KV 缓存 + 张量负载)

| 指标 | 数值 |
| --- | --- |
| 音频吞吐量 | 23.72 audio-s/s |
| 请求吞吐量 | 5.95 req/s |
| 平均 TTFP | 899.67 ms |
| 平均 E2EL | 10.47 s |

### Higgs Audio V3 (H20, 单 GPU, c=16, eager + 本地 MLP 图)

| 指标 | 数值 |
| --- | --- |
| 请求吞吐量 | 5.18 req/s |
| 音频吞吐量 | 35.26 audio-s/s |
| 墙钟时间 | 96.5s |
| 相对基线加速比 | 2.70× |

---

## 致谢

我们感谢 Minghui Jiang、Yueqian Lin、Canlin Guo、Shunyang Li、Taichang Zhou、Yuekai Zhang、Juan Pablo Zuluaga、Nick Cao、Ruirui Yang、Wenjing Chen、Haiyan Wu、Han Gao、Hongsheng Liu 和 Roger Wang 的贡献与反馈。

---

## 参考文献

---

如果你对 TTS 推理优化感兴趣，欢迎加入 [vLLM Slack](https://slack.vllm.ai) 的 `#sig-omni` 频道，或在 [vLLM-Omni GitHub](https://github.com/vllm-project/vllm-omni) 提 issue。

## 脚注

1. Qwen3-TTS — [QwenLM/Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS) [↩](#user-content-fnref-11)
2. Qwen3-TTS streaming connector decoupling — [PR #3485](https://github.com/vllm-project/vllm-omni/pull/3485) [↩](#user-content-fnref-6) [↩2](#user-content-fnref-6-2)
3. Qwen3-TTS high-concurrency Stage 0 batching — [PR #3662](https://github.com/vllm-project/vllm-omni/pull/3662) [↩](#user-content-fnref-7) [↩2](#user-content-fnref-7-2)
4. Qwen3-TTS hot-path micro-optimizations — [PR #3689](https://github.com/vllm-project/vllm-omni/pull/3689) [↩](#user-content-fnref-1) [↩2](#user-content-fnref-1-2)
5. VoxCPM2 — [OpenBMB/VoxCPM](https://github.com/OpenBMB/VoxCPM) [↩](#user-content-fnref-12)
6. VoxCPM2 per-layer compile + PagedAttention — [PR #2690](https://github.com/vllm-project/vllm-omni/pull/2690) [↩](#user-content-fnref-3)
7. VoxCPM2 whole-model compile + streaming VAE + CFM sync fix — [PR #2758](https://github.com/vllm-project/vllm-omni/pull/2758) [↩](#user-content-fnref-4) [↩2](#user-content-fnref-4-2)
8. VoxCPM2 CFM/LocDiT batching + decode-tail optimizations — [PR #3882](https://github.com/vllm-project/vllm-omni/pull/3882) [↩](#user-content-fnref-5)
9. Higgs Audio V3 GPU-resident state machine + CUDA Graph — [PR #4204](https://github.com/vllm-project/vllm-omni/pull/4204) [↩](#user-content-fnref-10)
10. Fish Speech S2 Pro — [fishaudio/fish-speech](https://github.com/fishaudio/fish-speech) [↩](#user-content-fnref-13)
11. Fish Speech S2 Pro KV cache fast path + DAC optimizations — [PR #3773](https://github.com/vllm-project/vllm-omni/pull/3773) [↩](#user-content-fnref-9)
