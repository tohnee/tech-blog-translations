---
title: "SGLang 中的 DSpark：置信度驱动的可变长度验证投机解码"
title_en: "DSpark in SGLang: Speculative Decoding with Confidence-Driven, Variable-Length Verification"
author: "SGLang Team"
date: "July 6, 2026"
source: https://lmsys.org/blog/2026-07-06-dspark-sglang/
translated: 2026-09-12
previewImg: /images/blog/dspark-sglang/perf-compare.png
type: blog
---

# SGLang 中的 DSpark：置信度驱动的可变长度验证投机解码

> 原文：[DSpark in SGLang: Speculative Decoding with Confidence-Driven, Variable-Length Verification](https://lmsys.org/blog/2026-07-06-dspark-sglang/) · LMSYS Blog · SGLang Team

投机解码用额外的计算换取更少的解码步数，但随着负载增长，这笔交换越来越不划算：在 batch size 为 `B`、每步投出 `K` 个投机 token 时，目标模型每步要验证 `B * K` 个 token，超过某个临界点后，验证的代价就会超过它省下的开销。DSpark 从两头同时下手——一是**半自回归块**起草器（一次 draft 前向产出整个块，因此接受率保持在高位），二是由草稿模型自身置信度驱动的**每请求可变验证长度**，不再去验证负载大概率不会接受的 token。算法及其收益来自 DSpark 论文。

SGLang 现已支持在稠密与稀疏模型（如 Qwen3 和 DeepSeek-V4）上运行 DSpark。本文介绍这一集成工作（[sgl-project/sglang#30261](https://github.com/sgl-project/sglang/pull/30261)）。我们在一个开源推理服务引擎上复现了论文收益的**形状**——单用户加速，以及验证预算随负载上升而收缩——并描述了把这一调度变成真实时钟时间的**工程实现**：在参差（ragged）、按请求可变的验证之上捕获完整 CUDA 图（这样裁剪后的 batch 重放的是一张真正更小的图，而不是填充过的图）；一条具备重叠感知的投机路径，把调度器藏在前向计算之后；一个代价表（cost table）profiler，让调度器能在线确定每个请求的验证预算；以及针对"裁剪会掩盖的接受率天花板"的可观测性。我们的硬件、引擎和流量都与论文不同，因此我们复现的是机制与曲线，而不是逐位一致的数字；下文每一处"更快"都是相对我们自己的对照组测得的——两组配置除投机配置外完全相同。

## 相对 MTP 与非投机基线的加速

<p align="center"><img src="/images/blog/dspark-sglang/perf-compare.png" width="640" alt="H200 dp4 上的聚合吞吐量对比单用户解码速度，每个实验组一条曲线：非投机下限、MTP 与 DSpark。越靠右上越好；每个标记点是一个 batch size 下三轮平均的结果。"></p>


*图 1. 聚合吞吐量（y 轴）对比单用户解码速度（x 轴）；每条曲线表示并发从 batch 1 扫到 256，每个实验组一条曲线。越靠右上越好。*

在图 1 的示例中，DSpark 在整个并发扫描范围内都给出了最优的吞吐量/延迟折中，明显领先于 MTP 和非投机下限。三个实验组均在 H200 上以 4 个 rank 的 DP 注意力运行 DeepSeek-V4-Flash，除投机配置外完全相同——分别是非投机下限、MTP（EAGLE 风格基线，取 1-1-2 与 3-1-4 两种配置在每个 batch size 下的最优值）以及 DSpark。

## 在 SGLang 中引入 DSpark

采自论文的 DSpark 算法由三个草稿侧组件构成：

- **块起草器（block drafter）** — 包含一条稠密路线（如 Qwen3）和一条稀疏路线（如 DeepSeek-V4）；一次前向即可输出一个 `gamma` token 的块，并由一个轻量的序列头（Markov 或 RNN）让每一步以上一个 token 为条件，因此整个块是半自回归的。
- **置信度头（confidence head）** — 为每个被起草的 token 打分，估计其在验证中存活的机会；对整块取乘积即得该块的存活概率。
- **序列温度缩放（Sequential Temperature Scaling，STS）** — 对这些分数做校准，使存活概率能反映调度器据此做预算的真实接受率。

围绕这三个组件，SGLang 补充了推理服务支撑面：

- **置信度调度器** — 把每个块的存活概率换算成每步、每请求的验证预算。
- **每请求参差验证（per-request ragged verify）** — 同一 batch 内每个请求可以有可变的验证长度（`static` / `compact` / `cap-accept`）。
- **完整 CUDA 图** — 在参差、可变长度的验证之上捕获。
- **可观测性** — 裁剪之下的接受率天花板及其他指标。
- **加性 SPS 代价表** — 离线剖析得到的步时模型，由调度器在线读取。
- **数据并行注意力** — 与其他并行维度协同支持。
- **零开销调度** — 集成进 SGLang 的重叠调度器，几乎没有 DSpark 专属的特判逻辑。
- **性能优化** — 融合的 Triton 算子，以及分片的块起草器矩阵乘法。

### 验证模式

这三种验证模式是本文其余部分展开所围绕的主轴。`static` 每步验证完整的草稿块（基线）。`compact` 只验证调度器为每个请求选定的窗口——这是生产路径。`cap-accept` 验证完整块，但只提交到该窗口为止：输出与 `compact` 相同，同时暴露出完整验证本可接受多少 token——这就是我们测量裁剪之下天花板的方法。

### 完整 CUDA 图下的参差验证

按请求的窗口塞不进固定形状的 CUDA 图：一个 batch 里一个请求验证 2 个 token、另一个验证 6 个，就不存在单一的 query 长度；而把所有人都填充到完整块宽度，等于把裁剪又填了回去。因此我们让 batch 保持参差，并把图键定为 token **总数**——把可变长度的请求前向打包（front-pack）进一个紧凑缓冲区，再向上取整到最近的已捕获档位（tier）。当预算被裁剪时，打包后的总数落进更小的档位，DSpark 便重放一张真正更便宜的图（更少的 attention 与 MLP 行，而不是掩码后的全宽前向）；在 DP 注意力下，各 rank 共享同一档位（取所有 rank 所需的最大值）并一起降档。

打包后的缓冲区是一个 `cu_seqlens` 风格的 varlen 输入，因此 compact 验证可以直接复用后端已有的注意力算子——在 DeepSeek-V4 上就是模型自带的 sparse-MLA 路径（`flash_mla`），无需新算子；每个受支持的后端只需在图重放时从打包布局重建自己的 varlen 元数据。

<p align="center"><img src="/images/blog/dspark-sglang/ragged-verify.svg" width="840" alt="固定形状的解码图把每个请求都填充到完整块宽度（N x W = 18 格，其中 8 格是填充）；参差的 compact 图把调度的 token 前向打包进一个缓冲区，只对总数向上取整到最近的已捕获档位（12 格，其中 2 格是填充）。两者都要把填充算进前向，因此参差路径计算的填充格数少得多。"></p>

*图 2. 把每请求验证长度可变的 batch 装进已捕获的 CUDA 图。固定形状的图把每个请求都填充到完整块宽度（N x W）；参差路径则把调度的 token 前向打包，只对总数向上取整到最近的已捕获档位，在相同的被接受 token 数下计算的填充格数少得多。*

### 可观测性

裁剪会"审查"掉天花板：compact 模式只验证块的前几个位置——即调度器的窗口——因此完整块验证在这一步本可接受多少 token 永远不会被观测到；而没有这个数字，你就无法区分一次好的裁剪和一次有损的裁剪。cap-accept 运行可以把它恢复出来：它验证完整块，但只提交到窗口为止，因此提交的内容与 compact 完全一致，同时暴露出天花板。我们还提供了每请求置信度与校准指标（如 ECE），供事后分析使用。

### 估计裁剪下的天花板

块接受估计器（block-accept estimator）专为生产运行等不希望额外跑一轮伴生实验的场景设计，能在 compact 运行内部直接恢复出被审查天花板的估计值。它利用后续步骤中目标 token 及其 logprob，并在"被裁剪与未被裁剪轨迹中锚定 token（anchor token）性质相似"的假设下，为反事实的尾部计算估计区间。

## 动态调度与固定调度的初步对比

置信度调度器只是一个最初的、朴素的版本，我们也以这种定位来看待它——它是"机制端到端可行"的证明，而不是精调后的结果。
我们在两个接受率不同的示例负载上，对比 `compact`（每步 SPS-argmax 预算）与 `no-trim`——即走同一参差路径的 `static` 全块调度。

<p align="center">
<img src="/images/blog/dspark-sglang/dyn-schedule-gsm8k.png" width="49%">
<img src="/images/blog/dspark-sglang/dyn-schedule-arena.png" width="49%">
</p>

*图 3. compact（动态裁剪）对比 no-trim（完整块），batch 从 1 到 256、DP4，在两个接受率不同的示例上。越靠右上越好。*

动态预算的优势主要体现在高 batch 下。batch size 为 1 时，目标验证并不会随 token 增多而明显变慢，裁剪省不了多少，两组打平。随着并发上升、吞吐量开始趋平，裁剪缩短了每步耗时，`compact` 开始领先。在接受率更低的示例上，差距更大、也出现得更早——接受率越低，可裁剪的尾部越多，这与代价模型的预测完全一致。

每个面板内部都是干净的 `compact` 对 `no-trim` 的 A/B 对比（面板内设置完全相同），但两个示例之间并非严格的单变量对照：除接受率外，它们在设置上也略有差异（prompt 格式与每组轮数），因此我们解读的是跨示例的趋势，而不是跨面板的绝对数字。

这些预算的质量也取决于背后的代价表。我们目前的 SPS（及校准）拟合只是初步近似，可能尚未充分刻画步时如何随上下文长度变化——因此调度器最终落在的具体工作点仍有改进空间，我们在此展示的是机制本身，而不是一个调优过的数字。

## 混合流量下的每请求差异化

同质化的扫描掩盖了置信度调度真正的意义。同一个 batch 中的两个请求，如果一个远比另一个更容易预测，就不该拿到相同的验证窗口。混合流量正是这一点发挥作用的地方。

![按数据集划分的验证预算（左）：cap-accept 下 gsm8k、arena-hard 与 poetry 每个验证步的天花板/窗口/实际交付 token 数；以及三种负载的每步验证长度分布（右）。](/images/blog/dspark-sglang/mixed-dataset.png)

*图 4. 按负载划分的预算（左）与每步验证长度分布（右）。*

举个例子，我们按接受难度混合三种负载：gsm8k（高）、arena-hard（中）、poetry（低）。窗口随难度收窄——分别为 5.24、3.78、2.91 个 token——而相对天花板（即不裁剪时块本可接受的数量）的利用率保持在高位（0.88–0.97）。调度器是在为每个请求单独定尺寸，而不是套用一个 batch 平均值。右图逐步展示了这一点：约 55% 的 gsm8k 步骤填满了 6 的完整窗口，而约 80% 的 poetry 步骤只用了 3 个或更少。

## 性能优化与零开销调度（ZOS）

两类工程工作把调度变成真实时钟时间：削减每一步的成本，以及把调度器藏在前向计算之后。二者合力在 DeepSeek-V4-Pro、TP=8、B300 上于 batch size 1 达到**接受长度约 5 时 383.7 tok/s**。

我们把成簇的细碎操作重写为融合的 Triton 算子，例如 compact scatter、SWA 页索引、验证长度 top-k 调度，以及参差窗口打包。块起草器的采样路径被折叠进融合算子，其矩阵乘法做了分片。在一个示例 profile 中，目标验证之外的开销减少了 1.7 ms（对照 7.3 ms 的验证本身）。

DSpark 几乎不需要任何特判就能直接接入 SGLang 的零开销（重叠）调度器，并加上论文中的"回看两步"置信度中继（two-step-back confidence relay）。这里面几乎没有 DSpark 专属的管道工作。SGLang 的 spec-v2 运行时已经在独立的流上把下一步的调度与当前前向计算重叠起来，而 DSpark 以一等公民 worker 的身份接入：前向输出以异步 future 返回，跨迭代次序依赖运行时的设备侧屏障（device-side barrier），设备端页表则意味着每步无需主机同步。置信度中继复用同一通道，只是回看两步读取。解码循环因此可以无气泡运行——比关闭调度器时紧凑约 1.5 倍。

![batch size 1 的解码：重叠调度器关闭（上）时，run_batch 迭代之间以及起草生成与目标验证阶段之间出现气泡；开启（下）时全部背靠背运行。](/images/blog/dspark-sglang/zos.png)

*图 5. batch size 1 的解码，重叠调度器关闭（上）对比开启（下）。开启后，`run_batch` 迭代之间、以及单步内部块起草生成与目标验证阶段之间都不再有气泡。*

## 剖析代价表

![加性 SPS 代价表拟合——原始步时与拟合值（a）、吞吐量（b）——以及 SPS 预测与实测解码步时（c），DeepSeek-V4 on H200。](/images/blog/dspark-sglang/sps-table.png)

*图 6. 加性代价模型——原始值与拟合值（a）、吞吐量（b）——以及预测与实测步时（c）。*

我们把调度器对步时 `T(bs, K)` 的估计表示为一个加性模型（`K` 为该 batch 的额外验证 token 数）：
`T(bs, K) = bias + alpha(bs) + theta(M), M = bs + K`，
其中 `alpha(bs)` 是请求规模下限（draft 前向加一部分注意力开销），不受裁剪影响；`theta(M)` 是目标模型的验证 token 开销，也是裁剪唯一能省下的项。调度器的 argmax 在"期望接受的 token 数"与"真实边际成本"之间权衡，因此只有 `theta` 较大的地方才有裁剪空间。图 6(c) 在在线服务器上验证了该模型的预测。

## 下一步计划

DSpark 现已进入 SGLang；我们在 [sgl-project/sglang#30344](https://github.com/sgl-project/sglang/issues/30344) 中跟踪路线图。接下来：

- **代价模型与调度** — 更强、越来越在线化/自适应的代价模型，以及对动态调度器的进一步改进。
- **模型覆盖** — 支持更多稠密与稀疏模型。
- **并行** — 覆盖更多并行模式与服务拓扑。
- **可观测性** — 将块接受估计器、跨检查点的置信度校准等指标产品化。
- **健壮性** — 加固完整 CUDA 图路径，扩大压力/回归测试范围。

感谢 DSpark 的作者以及 DeepSeek 提供的算法与模型。

## 附录：复现步骤

以下所有命令均在预构建镜像内运行（`docker pull lmsysorg/sglang:dev-dspark`），或从源码构建：[sgl-project/sglang#30261](https://github.com/sgl-project/sglang/pull/30261)，锁定在 commit [`692c5f7d`](https://github.com/sgl-project/sglang/commit/692c5f7d532f129424b57961c262bbd253b411dc)。

**图 1、3、6 —— frontier 服务器（DeepSeek-V4-Flash，H200，DP4）。** 启动 DSpark 实验组：

```bash
SGLANG_ENABLE_METRICS_DEVICE_TIMER=1 \
python3 -m sglang.launch_server \
  --model-path deepseek-ai/DeepSeek-V4-Flash-DSpark \
  --speculative-algorithm DSPARK \
  --tp 4 --dp-size 4 --enable-dp-attention --enable-dp-lm-head \
  --moe-a2a-backend none --moe-runner-backend flashinfer_mxfp4 --disable-flashinfer-autotune \
  --swa-full-tokens-ratio 0.1 --chunked-prefill-size 1024 \
  --mem-fraction-static 0.8 --cuda-graph-max-bs 192 --max-running-requests 1024 \
  --disable-radix-cache --trust-remote-code --host 0.0.0.0 --port 30000
```

其中 `--disable-radix-cache` 是为了避免基准测试脚本命中缓存。其余实验组只改动投机配置：**non-spec** 去掉 `--speculative-*` 并加载 `--model-path deepseek-ai/DeepSeek-V4-Flash`；**MTP** 使用同一目标模型，配合 `--speculative-algorithm EAGLE --speculative-num-steps {1,3} --speculative-eagle-topk 1
--speculative-num-draft-tokens {2,4}`（取两种配置在每个 batch size 下的最优值）；DSpark compact 或 static 设置 `SGLANG_RAGGED_VERIFY_MODE=compact|static`；
使用 SPS 表执行 compact 模式时加上 `--speculative-dspark-sps-table-path sps_table.json`；
图 3 的 **no-trim** 实验组是 `SGLANG_RAGGED_VERIFY_MODE=compact` 且不带 SPS 表（参差路径运行在完整窗口上）。用固定 prompt 跨 batch size 扫描来驱动任一实验组：

```bash
python3 -m sglang.benchmark.one_batch_server \
  --model None --base-url http://127.0.0.1:30000 \
  --batch-size 1 8 16 32 64 96 128 160 192 256 --output-len 1024 --temperature 0.7 \
  --fixed-prompt-file frontier_prompt.txt --fixed-prompt-apply-chat-template --show-report
```

固定 prompt 在[这里](https://gist.github.com/sglang-bot/71cc966dce295e78cbd0baddc402d151)
（`frontier_prompt.txt`），由 16 道 GSM8K 问题拼接而成，以便生成的是真实内容。
鉴于投机解码在不同数据集上的接受长度不同，用户可以在自己的数据上测试。

图 6 的代价表来自一次剖析运行：以
`SGLANG_DSPARK_ENABLE_SPS_RECORD=1 SGLANG_SIMULATE_ACC_LEN=1.0` 启动 `compact`，再用 `python3 -m sglang.benchmark.dspark_sps_profiler all` 拟合加性
模型（在 input-len 512 下扫描 batch × 验证比例网格）。

**图 4 —— 混合流量。** 服务器与图 1 相同，`--mem-fraction-static 0.7`、块大小为 6；通过
`SGLANG_RAGGED_VERIFY_MODE` 运行全部三种模式（`static` / `compact` / `cap-accept`），驱动一组 gsm8k + arena-hard + poetry 混合请求，
以非流式 makespan 吞吐量计量。

**图 5 —— 零开销（DeepSeek-V4-Pro，B300，TP8）。**

```bash
SGLANG_RAGGED_VERIFY_MODE=compact SGLANG_DSV4_FP4_EXPERTS=1 SGLANG_TORCH_PROFILER_DIR=./trace \
python3 -m sglang.launch_server \
  --model-path deepseek-ai/DeepSeek-V4-Pro-DSpark --speculative-algorithm DSPARK \
  --tp 8 --moe-runner-backend flashinfer_mxfp4 --disable-flashinfer-autotune \
  --mem-fraction-static 0.82 --chunked-prefill-size 4096 --cuda-graph-max-bs 4 \
  --trust-remote-code --host 127.0.0.1 --port 30000
# overlap off: append --disable-overlap-schedule
```

捕获一个 batch-1 的解码 trace，然后只看 GPU 轨道：

```bash
python3 -m sglang.benchmark.one_batch_server \
  --model None --base-url http://127.0.0.1:30000 \
  --batch-size 1 --input-len 256 --output-len 256 \
  --profile --profile-activities GPU --profile-steps 20
```
