---
title: "SGLang 服务 GLM5.2 NVFP4 agentic 负载：两周内达到 500 TPS"
title_en: "Serving GLM5.2 NVFP4 Agentic Workload with SGLang: Reaching 500 TPS in 2 Weeks"
author: "SGLang Team"
date: "July 14, 2026"
previewImg: /images/blog/glm52-optimization/glm52-nvfp4-performance-pareto.png
type: blog
source: https://lmsys.org/blog/2026-07-13-glm52-optimization/
translated: 2026-09-12
---

# SGLang 服务 GLM5.2 NVFP4 agentic 负载：两周内达到 500 TPS

> 原文：[Serving GLM5.2 NVFP4 Agentic Workload with SGLang: Reaching 500 TPS in 2 Weeks](https://lmsys.org/blog/2026-07-13-glm52-optimization/) · LMSYS Blog · SGLang Team

## TL;DR

- 8xB300 上超过 500 TPS（bs=1）
- 为 GLM 5.2 MTP 实现无同步投机解码
- Spec V2 内置 IndexShare MTP
- ISL 80k 下 TopK-V2 提速 2.33x
- Indexer 前导（prologue）融合
- GEMM 算子改进

![GLM-5.2 NVFP4 day-0 与 v0.5.15.post1 在 B300 上的交互性对比](/images/blog/glm52-optimization/glm52-nvfp4-day0-vs-v0515-tps.png)

*图 0：Day-0 与 v0.5.15.post1 在 8\*B300 上的性能对比*

## 背景

[GLM-5.2](https://huggingface.co/zai-org/GLM-5.2-FP8) 延续了与此前 GLM 检查点相同的骨干结构：在 DeepSeek-V3 风格的 MoE 之上，叠加带稀疏注意力索引器（sparse-attention indexer）的 DSA。它新增了两项重要架构变更：面向 DSA 的 IndexShare，以及带 IndexShare 与 KVShare 的多 token 预测（MTP）。

SGLang 从 day 0（首发日）起即在（Grace）Blackwell 硬件上支持 GLM-5.2-NVFP4 检查点，稀疏注意力与 MoE 均使用 trtllm-gen 算子（kernel）。为了让这套 day-0 技术栈成为更快、更稳定、更贴近生产环境的推理服务路径，我们引入了以下优化。

## 优化

### 运行时优化

#### 零开销调度与 Spec v2

Spec V2 是 SGLang 用于投机解码的[重叠（overlap）运行时](https://www.lmsys.org/blog/2024-12-04-sglang-v0-4/)。当 GPU 在 forward 流上执行当前一轮模型前向时，会在 plan 流上完成下一步的 KV 分配与元数据准备，从而把 CPU 开销隐藏在前向计算内部。

我们最近已将 Spec V2 默认开启。理论上，重叠调度器应该能让 CPU 在 GPU 仍忙于当前一轮时处理下一轮的簿记工作，使迭代之间几乎不出现空泡（bubble）。但在实践中，还需要几项优化才能完全兑现重叠调度器与 Spec V2 的收益：我们让 DSA 的 draft-extend 路径支持 CUDA 图（CUDA Graph），让 `seq_lens_cpu` 在 DSA 中成为可选项以消除 D2H 同步，移除了剩余的 H2D 同步，并融合了 `_apply_cuda_graph_metadata` 中的小型 eager 元数据算子。随着这些 GPU 空泡被消除，我们获得了 11% 的端到端 TPS 加速。

![Spec V2 优化前的解码 trace](/images/blog/glm52-optimization/spec-v2-before.png)

![Spec V2 优化后的解码 trace](/images/blog/glm52-optimization/spec-v2-after.png)

*图 1：batch size 1 下的解码过程，Spec v2 优化前（上）与优化后（下）对比。开启后，**run_batch** 迭代之间不再有空泡。*

#### SGLang 中的 IndexShare MTP

GLM-5.2 自带一个很强的 MTP 头，接受长度（accept length）经常达到 5 以上，这使其在 agentic coding 这类低延迟负载上获得显著加速。为了正确实现 GLM-5.2 的 MTP 行为，我们对 SGLang 的投机解码运行时做了几处修改。

首先，IndexShare 要求 SGLang 在多个 draft step（草稿步）之间复用 DSA 索引器的 top-k：draft step 0 计算出的 top-k 会被保存并传递给后续步骤，让它们无需重算索引器。在长上下文下，这最多可将 draft step 开销削减约 1.9x，且不影响输出质量。

其次，top-k 需要从正确的位置获取种子，在 SGLang 中这个位置是上一轮 run_batch 迭代的 draft-extend。由于 Spec V2 以异步方式执行各步骤，我们必须把这个种子值穿过重叠调度器的 relay buffer 传递下去，以免它在迭代之间丢失。

### 算子（Kernel）优化

#### TopK-V2

DSA 索引器会把每个 query 转换为对历史 KV 位置的打分，然后挑选出 top 候选用于稀疏注意力。沿用我们在 [DeepSeek-V4 博客](https://www.lmsys.org/blog/2026-04-25-deepseek-v4/)中介绍的「Lightning-TopK」设计，我们把原来的 DSA TopK-V1 算子升级为 TopK-V2，将 TopK 当作一个选择问题而非排序问题来处理。

![TopK-V2 的八 CTA cluster 基数选择设计](/images/blog/glm52-optimization/topk-v2-cluster-radix-select.png)

*图 2：TopK-V2 将一条长分数行切分到八个 CTA 上，每个 CTA 构建一个本地 10-bit 直方图。跨 cluster 的归约定位出包含第 2048 大分数的 bin；高于它的值直接输出，边界候选则经过精确的 FP32 基数选择。被选中的逻辑位置随后被转换为索引器 KV 缓存的物理槽位。*

![TopK-V2 的 10-bit 直方图构建](/images/blog/glm52-optimization/topk-v2-histogram.png)

*图 3：TopK-V2 构建直方图时，每个 FP32 分数先被舍入到 FP16，再变换为一个无符号 key，其顺序与分数的数值顺序一致。key 的高 10 位选出 1,024 个 bin 中的一个，对应计数器被原子递增。这个粗糙直方图只用于定位边界区域；FP32 精化保证了最终 top-k 选择的精度。*

TopK-V2 对短行和中等长度的行使用寄存器驻留（register-resident）或单 CTA 的流式路径。对长行，则由八个 CTA 组成的 cluster 各自构建本地 10-bit 基数直方图，并在 cluster 内归约，以确定阈值所在的 bin。

跨 cluster 的归约定位出包含第 2048 大分数的 bin；高于它的值直接输出，边界候选则经过精确的 FP32 基数选择。被选中的逻辑位置随后被转换为索引器 KV 缓存的物理槽位。算子随后在 FP32 边界处收集候选，并使用精确的基数平局裁决（radix tie-break）恰好返回 `k` 个条目，运行时 `k` 最大支持到 2048。

一个规划算子会根据批内的序列长度分布选择 cluster 的分界阈值，并为常驻 cluster 池构建工作列表，因此这套方案在每次前向时生成一次，并在各 DSA 层之间复用。TopK-V2 还把选择与页表变换融合进单个算子，以降低延迟。

![DSA TopK-V1 与 TopK-V2 算子延迟对比](/images/blog/glm52-optimization/topk-v1-vs-v2-latency.png)

*图 4：TopK-V1 与 TopK-V2 的算子延迟对比，测试场景为 batch size 1、6 个 draft token 的目标模型验证。两个算子均将 Top-K 与页表变换融合在一起。*

基准测试结果显示，在 80K ISL（输入序列长度）下，TopK-V2 将平均算子延迟从 40.7 µs 降至 17.5 µs，提速 2.33×。其优势随上下文长度增长而扩大，在 1M ISL 下达到 10.17×，延迟从 372.1 µs 降至 36.6 µs。这一不断拉大的差距表明，TopK-V2 在长上下文负载下的扩展效率要高得多。

#### Indexer 前导（Prologue）融合
![DSA 索引器前导依赖链：融合前与融合后](/images/blog/glm52-optimization/indexer-prologue-fusion.png)\
*图 5：DSA Indexer 前导算子：融合前与融合后*

DSA 索引器的前导阶段负责准备两路数据：一路是存入索引器 KV 缓存的 key 表示，另一路是用于计算稀疏注意力候选的 query 表示。原始实现把这一过程表达为一连串小型算子和投影。

在「融合前」路径中，key 侧依次执行 `wk`、LayerNorm、RoPE、Hadamard 变换、FP8 量化和缓存写入；query 侧依次执行 `wq_b`、RoPE、Hadamard 变换、FP8 量化和 head-gate 缩放。此外，`weights_proj` 是一个独立的投影，为每个头的门控提供输入。

[PR #27705](https://github.com/sgl-project/sglang/pull/27705) 通过两种方式压缩了这条依赖链：

第一，它把 `wk` 与 `weights_proj` 融合为单个 BF16 投影 `wk_weights_proj`，其输出被切分为 key 激活和原始 head-gate 权重两部分。这从索引器路径中省掉了一个小 GEMM，并让 head-gate 权重可以直接被融合后的 query 算子复用。

第二，它融合了逐元素的尾段计算：

- key 路径：LayerNorm + RoPE + FP8 量化 + 分页索引器 KV 缓存写入。
- query 路径：RoPE + FP8 量化 + head-gate 缩放。

图中展示了这一改动在调度上的重要影响。融合前，缓存写入排在 key 侧计算之后，拉长了关键路径；融合后，key 侧可以作为单个包含缓存写入的算子运行，query 侧则作为另一个融合算子运行。两路可以重叠执行，索引器前导因此从一长串算子启动变成一对更短、更干净的分支。算子总数从 12 个降至 4 个。

融合路径还去掉了 Hadamard 变换。对 Q 和 K 施加同一个正交变换可以在量化前保持二者的内积，因此它真正起作用的地方在于量化后的表示。融合路径改为直接对未经变换的激活做量化。

算子数量的减少直接转化为可测量的解码吞吐量收益，不过在小 batch size 下效果更明显，因为那里启动开销占主导。batch size 为 1 时，解码吞吐量提升约 8%：索引器前导中受访存限制的算子消失了，而算子从 12 个减到 4 个也按比例去掉了更大一块关键路径。batch size 为 128 时，提升幅度更小但依然稳定，约为 5%。

#### GEMM 算子改进
![CuTe DSL BF16 GEMM 相对 cuBLAS 的加速比](/images/blog/glm52-optimization/cutedsl-bf16-gemm-speedup.png)\
*图 6：不同 batch size 下 CuteDSL BF16 GEMM 相对 CuBLAS GEMM 的加速比*

GLM-5.2 中并非每个矩阵乘法都以 NVFP4 运行。为了保护精度，该检查点的量化方案让注意力投影和共享专家 MLP 保持在 BF16，只对路由专家做量化。[PR #30117](https://github.com/sgl-project/sglang/pull/30117) 为这些 BF16 层增加了一个可选的 CuTe DSL BF16 GEMM 后端，来自 FlashInfer 的 [TGV GEMM](https://github.com/flashinfer-ai/flashinfer/pull/3281)。

该算子按专职分工把工作拆分到不同 warp：一些 warp 只负责从内存加载数据，一个 warp 只做矩阵乘法，另外几个 warp 只负责把结果写回。由于这些是同时运行的独立 warp，加载、计算和存储得以重叠进行，而不是依次发生。

加速的真正来源是该算子对加载流水线的激进程度。它不是加载一个 tile 的数据、等它被用完再加载下一个，而是让许多 tile 的数据同时保持在途，为此几乎用满了 GPU 的全部共享内存。在解码运行的小 batch size 下，这些 GEMM 的大部分时间都花在等内存而不是计算上，因此算子能把加载提前得越多，花在等待上的时间就越少。这正是它相对 cuBLAS 这类通用库的主要优势——后者的流水线策略保守得多。

一步调优还会为当前运行的形状挑选最合适的 tile 尺寸，而一个预先测得的启发式规则会在每次调用时决定使用该算子还是回退到 cuBLAS。

在 TP4 下有两个 BF16 层收益明显：融合 QKV 投影（M, 2624, 6144；各 rank 间复制）和注意力输出投影 o_proj（M, 6144, 4096；跨 rank 切分）。在 M=1 到 32 的完整解码范围内扫描：

融合 QKV 投影在每一个 batch size 下都胜出，相对 cuBLAS 平均加速 1.08x，峰值 1.13x。o_proj 同样在每一个 batch size 下胜出，平均 1.05x，峰值 1.08x。batch size 为 1 时，端到端解码加速约为 4%。

## 性能结果

![GLM NVFP4 在 SGLang 上的性能 Pareto 曲线](/images/blog/glm52-optimization/glm52-nvfp4-performance-pareto.png)

*图 7：GLM 5.2 NVFP4 在 SGLang 上的性能 Pareto 曲线。*

图 7 汇总了 GLM NVFP4 模型在 OpenHands 多轮 agentic coding 负载上的性能结果。每个对话以约 80K token 的提示词开始，每轮输出约 220 个 token，共 13 轮。后续轮次复用前缀，整体缓存命中率约 92%。我们进行并发扫描，并把每 GPU token 吞吐量（tok/s/GPU）对交互性（tok/s/user）作图。每张图都固定模型、GPU 家族、精度、负载、推理服务框架和服务模式，只将 SGLang 的不同版本与自身比较。

有三点值得强调。第一，GLM-5.2 是一个比 GLM-5.1 高效得多的架构。在相同的 SGLang 版本上，GLM-5.2 在 4×GB300 和 8×B300 上分别带来约 1.4x 和约 1.3x 的单用户交互性/每 GPU 吞吐量提升。这一收益来自把 IndexShare 应用到 DSA 层，以及改进后的 MTP 头——它复用了 IndexShare 和 KVShare。第二，自 day-0 以来，单用户交互性提升了 18-34%。在 batch size 1 下，我们的优化大幅削减了每 token 开销，让我们在 8xB300 上达到 **500+ TPS**。第三，我们没有在高并发吞吐量上做任何妥协——batch size 8 下的峰值吞吐量也提升了 6–11%。

![四张 GB300 GPU 上的输入序列长度消融](/images/blog/glm52-optimization/isl-ablation.png)

*图 8：改变输入序列长度的消融测试。为提高可复现性，我们模拟了 5 的接受长度。*

图 8 的 ISL 消融结果直接展现了索引器优化的回报。在 day-0 路径上，DSA 索引器必须对一条随上下文增长的分数行进行排序，其开销随序列长度上升，单用户交互性也随输入增长迅速劣化。TopK-V2 显著缓解了这一瓶颈，使交互性一路到 1M token 都基本保持平稳。

## 下一步计划
本文主要聚焦于低并发、高缓存命中率场景的优化。未来，我们将把支持扩展到更高并发的场景：
- 面向更重负载的更优算子：面向预填充（prefill）的 ragged TopK-V2、更快的索引器 MQA logits 算子
- 在 agentic 负载下优化 PD 分离（PD Disaggregation）与专家并行技术
- 通过 [HiCache](https://docs.sglang.io/docs/advanced_features/hicache)、[HiSparse](https://docs.sglang.io/docs/advanced_features/hisparse_guide#hisparse-hierarchical-sparse-attention) 和 [LayerSplit](https://github.com/sgl-project/sglang/pull/29421) 技术改进缓存利用。
- 为 GLM 5.2 支持 [DSpark](https://www.lmsys.org/blog/2026-07-06-dspark-sglang)，帮助提升大并发下投机解码的接受率

## 致谢

我们谨向以下组织与个人致以谢意，感谢他们为 GLM 5.2 NVFP4 模型的支持与优化做出的贡献。

SGLang 社区/RadixArk：Khoa Pham、Baizhou Zhang、Jimmy Shong、Brayden Zhong、Ziyi Xu、Mohammad Miadh Angkad、Xinyuan Tong、Zhendong Hua、Zijie Xia、Jun Liu、Banghua Zhu 以及许多其他贡献者——优化与基准测试

Nvidia：Julien Lin、Zhiyu Cheng、Po-Han Huang、Ryan Stewart、Triston Cao 以及许多其他同事——协助 GLM5.2 NVFP4 的 Day-0 支持

GLM Team：Yuxuan Zhang——在 SGLang 中实现并验证 IndexShare

## 附录

### 复现

如需复现性能结果，请参考[此分支](https://github.com/Jiminator/sglang/tree/glm-nvfp4-blog-repro/benchmark/glm_nvfp4_blog)下的自定义脚本。\
服务端环境使用 SGLang v0.5.15.post1，基准测试客户端使用 [evalscope](https://github.com/modelscope/evalscope)。

负载方面，我们采用 OpenHands 多轮 agentic 回放（replay）：平均输入 ≈ 80k token/请求，每轮输出 220 个 token，每个对话 13 轮，聚合前缀缓存命中率约 92%，并使用真实的 EAGLE 投机接受（未做模拟）。

服务端启动命令如下：

```bash
# TP 4/TP 8
export SGLANG_OPT_USE_TOPK_V2=1
export SGLANG_ENABLE_MOE_DEFERRED_FINALIZE=1
python3 -m sglang.launch_server \
    --model-path nvidia/GLM-5.2-NVFP4 \
    --tensor-parallel-size 4 \    # --tensor-parallel-size 8 for 8*B300
    --quantization modelopt_fp4 \
    --context-length 90000 \
    --max-running-requests 16 \
    --max-prefill-tokens 8192 \
    --chunked-prefill-size 8192 \
    --cuda-graph-max-bs-decode 16 \
    --mem-fraction-static 0.87 \
    --trust-remote-code \
    --kv-cache-dtype fp8_e4m3 \
    --bf16-gemm-backend cutedsl \
    --reasoning-parser glm45 \
    --tool-call-parser glm47 \
    --speculative-algorithm EAGLE \
    --speculative-num-steps 5 \
    --speculative-eagle-topk 1 \
    --speculative-num-draft-tokens 6 \
    --enable-cache-report \
    --host localhost \
    --port "$PORT"

# TEP 4/TEP 8
export SGLANG_OPT_USE_TOPK_V2=1
export SGLANG_ENABLE_MOE_DEFERRED_FINALIZE=1
python3 -m sglang.launch_server \
    --model-path nvidia/GLM-5.2-NVFP4 \
    --tensor-parallel-size 4 \  #  --tensor-parallel-size 8 for 8*B300
    --ep-size 4 \   # --ep-size 8 for 8*B300
    --quantization modelopt_fp4 \
    --context-length 90000 \
    --max-running-requests 16 \
    --max-prefill-tokens 8192 \
    --chunked-prefill-size 8192 \
    --cuda-graph-max-bs-decode 16 \
    --mem-fraction-static 0.87 \
    --trust-remote-code \
    --kv-cache-dtype fp8_e4m3 \
    --bf16-gemm-backend cutedsl \
    --reasoning-parser glm45 \
    --tool-call-parser glm47 \
    --speculative-algorithm EAGLE \
    --speculative-num-steps 5 \
    --speculative-eagle-topk 1 \
    --speculative-num-draft-tokens 6 \
    --enable-cache-report \
    --host localhost \
    --port "$PORT"
```

### PR 列表
IndexShare 实现：[#27114](https://github.com/sgl-project/sglang/pull/27114), [#29654](https://github.com/sgl-project/sglang/pull/29654), [#29787](https://github.com/sgl-project/sglang/pull/29787), [#30839](https://github.com/sgl-project/sglang/pull/30839), [#30992](https://github.com/sgl-project/sglang/pull/30992)\
TopK-V2：[#26788](https://github.com/sgl-project/sglang/pull/26788), [#30274](https://github.com/sgl-project/sglang/pull/30274)\
Draft extend CUDA 图：[#29413](https://github.com/sgl-project/sglang/pull/29413)\
DSA 元数据融合与同步消除：[#29415](https://github.com/sgl-project/sglang/pull/29415), [#29499](https://github.com/sgl-project/sglang/pull/29499)\
Indexer 前导融合：[#27705](https://github.com/sgl-project/sglang/pull/27705)\
GEMM 算子：[#30177](https://github.com/sgl-project/sglang/pull/30117)\
其他优化 PR：[#21531](https://github.com/sgl-project/sglang/pull/21531), [#29595](https://github.com/sgl-project/sglang/pull/29595), [#29667](https://github.com/sgl-project/sglang/pull/29667)
