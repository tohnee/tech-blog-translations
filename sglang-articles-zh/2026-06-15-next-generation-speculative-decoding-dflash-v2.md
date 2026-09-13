---
title: "下一代投机解码：DFlash 与 Spec V2"
title_en: "The next generation of speculative decoding: DFlash and Spec V2"
author: "Z Lab, Modal, and SGLang Teams"
date: "June 15, 2026"
source: https://lmsys.org/blog/2026-06-15-next-generation-speculative-decoding-dflash-v2/
translated: 2026-09-12
previewImg: /images/blog/dflash-v2/dflash-arch-diagram.webp
type: blog
---

# 下一代投机解码：DFlash 与 Spec V2

> 原文：[The next generation of speculative decoding: DFlash and Spec V2](https://lmsys.org/blog/2026-06-15-next-generation-speculative-decoding-dflash-v2/) · LMSYS Blog · Z Lab, Modal, and SGLang Teams

将 Modal 与 Z Lab 的 DFlash 投机解码模型，与 SGLang 新近设为默认的 Spec V2 引擎结合使用，你可以获得当前最先进的大模型推理服务延迟。我们联合发布的新 DFlash 模型（面向 Qwen 3.5 397B-A17B）在我们测试的所有设置下，吞吐量均同时高于基线模型与原生 MTP 投机解码。在 HumanEval 编程数据集、并发数为 1 的场景下，其吞吐量达到基线的 4.3 倍以上、MTP 的 1.5 倍。

<div style="text-align: center;">
  <img src="/images/blog/dflash-v2/dflash-headline-perf.webp" style="width: 60%;"></img>
  <small>负载：Qwen 3.5 397B-A17B（BF16），HumanEval。设置：贪心解码，开启 thinking，最大新 token 数 4096。硬件：Modal 上的 8 张 B200。接受长度为跨请求的平均值。草稿 token/块数量按吞吐量最大化选取（MTP：7 步；DFlash：块大小 16）。</small>
</div>

为庆祝这次合作，我们在三个 Hugging Face 组织下同步发布了这个模型：

- [`z-lab/Qwen3.5-397B-A17B-DFlash`](https://huggingface.co/z-lab/Qwen3.5-397B-A17B-DFlash)
- [`modal-labs/Qwen3.5-397B-A17B-DFlash`](https://huggingface.co/modal-labs/Qwen3.5-397B-A17B-DFlash)
- [`lmsys/Qwen3.5-397B-A17B-DFlash`](https://huggingface.co/lmsys/Qwen3.5-397B-A17B-DFlash)

你可以用下面的命令亲自试用这个模型：

```shell
export SGLANG_ENABLE_OVERLAP_PLAN_STREAM=1

python -m sglang.launch_server \
  --model-path Qwen/Qwen3.5-397B-A17B \
  --trust-remote-code \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path modal-labs/Qwen3.5-397B-A17B-DFlash \
  --speculative-dflash-block-size 8 \
  --speculative-draft-attention-backend fa4 \
  --attention-backend trtllm_mha \
  --linear-attn-prefill-backend triton \
  --linear-attn-decode-backend flashinfer \
  --mamba-scheduler-strategy extra_buffer \
  --tp-size 8 \
  --max-running-requests 32 \
  --cuda-graph-max-bs-decode 32 \
  --cuda-graph-backend-prefill tc_piecewise \
  --enable-flashinfer-allreduce-fusion \
  --mem-fraction-static 0.8 \
  --host 0.0.0.0 \
```

下文将介绍 DFlash 为投机解码设计的新颖的 diffusion + KV 注入策略、这一策略为何能带来大幅加速，以及 [Z Lab](https://z-lab.ai)、SGLang 与 [Modal](https://modal.com) 的团队如何携手让这些加速惠及所有人。

## DFlash：并行草稿生成与 KV 注入

基于 Transformer 的大语言模型（LLM）非常强大，但其自回归解码过程使推理变得缓慢：token 必须逐个生成，[算术强度](https://modal.com/gpu-glossary/perf/arithmetic-intensity)很低，难以充分利用现代硬件。

[投机解码](https://arxiv.org/abs/2211.17192)化解了这一瓶颈：用一个更小、更快的草稿模型一次性提出多个 token，再由目标 LLM 并行验证，且不影响模型质量。

然而，许多投机解码方法——例如 [EAGLE 系列](https://arxiv.org/abs/2503.01840)，以及 [Gemma 4](https://blog.google/innovation-and-ai/technology/developers-tools/multi-token-prediction-gemma-4/) 与 [DeepSeek-V4](https://www.lmsys.org/blog/2026-04-25-deepseek-v4/) 等近期模型原生的多 token 预测（MTP）模块——仍然依赖串行的自回归，只不过是从目标模型转移到了草稿模型上。草稿模型逐个生成草稿 token，同样不适合现代硬件，也限制了可达到的加速比。

这正是 Z Lab 开发 [DFlash](https://arxiv.org/abs/2602.06036) 的原因：它使用轻量级的块扩散（block diffusion）草稿模型并行生成一整块草稿 token——这正是 GPU 和 TPU 喜欢的计算方式。小米新发布的 MiMo v2.5-Pro-UltraSpeed 就借助 DFlash 实现了[超过 1k 的输出 tps](https://mimo.xiaomi.com/blog/mimo-tilert-1000tps)。

用块扩散做投机草稿生成并非易事。直接训练一个小型块扩散模型作为草稿模型，接受长度会偏低；而用 [SpecDiff-2](https://arxiv.org/abs/2511.00606) 这类现成的大型扩散 LLM 作为草稿模型，又会带来很大的内存占用和高昂的草稿生成成本。

DFlash 的核心洞察很简单：目标 LLM 最了解上下文。受 [Medusa](https://arxiv.org/abs/2401.10774)、[EAGLE](https://arxiv.org/html/2503.01840v1) 和 MTP（[Gloeckle et al., 2024](https://arxiv.org/abs/2404.19737)；[Samragh et al., 2025](https://arxiv.org/abs/2507.11851)）等已有方法的启发，我们从目标模型中提取上下文 token 的隐藏表示。与以往工作不同的是，我们将它们直接注入草稿模型的 KV 缓存。这种做法随草稿深度增加的扩展性更好。KV 注入还让草稿模型无需从头对完整上下文建模，可以专注于预测下一个 token 块——而且用的是与目标模型后面几层相同的张量！

![](/images/blog/dflash-v2/dflash-arch-diagram.webp)

借助这一设计，DFlash 既利用了目标 LLM 产生的丰富且高度相关的上下文特征，又让草稿模型保持极小、极高效。因此，DFlash 能在草稿生成延迟很低的情况下获得很高的接受长度。

### DFlash 为什么这么快？

投机解码的加速主要取决于两个因素：每轮有多少草稿 token 被接受，以及草稿模型带来多少额外开销。DFlash 同时改进了这两点：扩散式草稿生成降低了草稿成本，KV 注入提高了接受率。

具体来说，我们在同一数据集上为 Qwen 3-4B 训练了一个 5 层 EAGLE-3 草稿模型和若干 5 层 DFlash 变体草稿模型，比较它们的端到端接受长度与速度。基线版 DFlash 的接受长度与 5 层 EAGLE-3 草稿模型相近，但凭借超快的并行草稿生成，它带来了高得多的端到端加速。结果以 `acc_len / speedup` 形式报告。

| 任务      | EAGLE-3（5 层）   | DFlash         |
| :-------- | :----------------- | :------------- |
| GSM8K     | 4.2 / 2.1x         | **4.2 / 3.3x** |
| HumanEval | 4.3 / 2.2x         | **4.0 / 3.2x** |
| MT-Bench  | 3.1 / 1.4x         | **3.0 / 2.2x** |

**DFlash 草稿生成更快**

EAGLE-3 这类自回归草稿模型逐个生成草稿 token，随着草稿长度增长，草稿生成成本大致线性上升。为了保持低延迟，这类方法通常只能依赖很浅的草稿模型，草稿质量因此受限。

DFlash 用块扩散草稿模型绕开了这一瓶颈：单次前向传播即可并行生成一整块 token，草稿生成对硬件友好得多。一个生成 4、8 甚至 16 个 token 的 5 层 DFlash 草稿模型，其草稿生成延迟远低于生成 4 个 token 的单层 EAGLE-3 草稿模型。

<img src="/images/blog/dflash-v2/dflash-vs-eagle-draft-latency.webp" style="display:block; margin-left: auto; margin-right: auto; width: 60%"></img>

通过消融 DFlash 的其他架构特性，我们可以观察到这项技术的独立影响。即便接受长度更低，得益于更快的草稿生成，DFlash 的端到端加速仍高于 EAGLE-3。

| 任务      | EAGLE-3（5 层）   | DFlash（仅扩散）        |
| :-------- | :----------------- | :---------------------- |
| GSM8K     | 4.2 / 2.1x         | **3.5 / 2.9x**          |
| HumanEval | 4.3 / 2.2x         | **3.5 / 2.9x**          |
| MT-Bench  | 3.1 / 1.4x         | **2.6 / 2.0x**          |

**KV 注入提升接受长度**

草稿生成得快，也要草稿 token 被接受才真正有用。EAGLE-3 只在草稿模型的输入处使用目标模型的特征，这一信号在更深的草稿模型中会逐渐衰减。

DFlash 则将目标模型特征注入每一层草稿层的 KV 缓存。这使草稿模型在整个生成过程中始终与目标模型的上下文强关联，让更深的草稿模型也能产出更高质量的草稿。

同样，通过消融扩散式草稿生成，我们也能观察到 KV 注入的独立影响。在自回归模式下运行的 DFlash，凭借更高的接受长度，在我们的端到端基准测试中仍然取得了更高的加速。

| 任务      | EAGLE-3（5 层）   | DFlash（仅注入）        |
| :-------- | :----------------- | :---------------------- |
| GSM8K     | 4.2 / 2.1x         | **4.8 / 2.4x**          |
| HumanEval | 4.3 / 2.2x         | **4.6 / 2.3x**          |
| MT-Bench  | 3.1 / 1.4x         | **3.4 / 1.5x**          |

## 在 SGLang 中实现 DFlash

上一节的基准数据来自 Z Lab 研发过程中 DFlash 的初始实现。基于这些亮眼的结果，Modal 与 SGLang 团队同 Z Lab 展开合作，在 SGLang 推理引擎中优化其端到端性能。

把 DFlash 这样的性能优化技术从研究推向生产，需要两个基本环节：在高性能引擎中实现该技术，然后对从主机调度器到 GPU 执行的端到端系统性能进行优化。

沿着这两条线，DFlash 在 SGLang 中的集成可以分为两部分。第一，DFlash 被加入原始的（[现已弃用](https://github.com/sgl-project/sglang/pull/25464)）V1 投机解码引擎。除了实现新的草稿模型架构之外，这还需要打通草稿与目标模型之间的 KV 缓存以支持注入。第二，DFlash 被加入新的 V2 投机解码引擎，后者通过[减少与主机的同步](https://modal.com/blog/host-overhead-inference-efficiency)带来了更好的性能。

在 [DFlash 的初始实现](https://github.com/sgl-project/sglang/pull/22077)中，我们为现有的投机解码引擎加入了对这一新模型架构的支持，包括新增一个 `DFlashWorker` 来控制草稿模型的执行，以及由它驱动的 `DFlashDraftModel`。

先回顾一下背景：SGLang 用一个调度器进程（主要运行在主机上）驱动模型 worker 进程（主要运行在加速器上）的执行。SGLang 投机解码机制中有一个反直觉之处：与调度器通信（通过 `.forward_batch_generation` 等方法）的是草稿模型 worker。它包住目标模型的 worker 来执行验证轮次，并在草稿就绪时调用它。如果你去读代码或看 trace，请记住这一点！

这并非 DFlash 的新东西。DFlash 主要的新颖之处在于 KV 注入——它把草稿模型和目标模型的状态绑定在了一起。在 EAGLE 这类方法中，草稿 KV 缓存完全为草稿模型私有，基于草稿自身潜在表示（latent）的 KV 投影计算得到；而在 DFlash 中，则是由草稿模型对目标模型的潜在表示做 KV 投影。

我们不想把这些潜在表示存下来挤占宝贵的 KV 缓存空间，也希望所有前缀相同的请求能共享基数树缓存（radix cache）。因此，我们在草稿前向计算的其余部分之前就完成草稿 KV 投影——即_立即物化_（immediate materialization）。这一步必须快，所以我们加入了按层批量执行的线性投影，以及一个用于 norm+RoPE 后处理的融合 Triton 算子。

## 用 Spec V2 与重叠调度消除 DFlash 的主机开销

这套实现可用且已经很快，但我们知道还能更快。当时我们正在同步开发 V2 投机解码引擎，于是下一步就是[将 DFlash 与 V2 引擎结合](https://github.com/sgl-project/sglang/pull/23000)——这也正是如今 SGLang 中提供的方案。

V2 引擎整体的核心目标，是减少主机-设备同步点——无论 GPU 多快、算子多好，这类同步点都会[严重拖累推理性能](https://modal.com/blog/host-overhead-inference-efficiency)。解决方案就是_重叠调度器_（overlap scheduler）。

具体来说，有两个关键的可以重叠的机会：

1. GPU 完成第 N-1 个批次之后，主机端的 `pop_and_process` 清理工作（例如停止 token 检测、请求元数据更新）可以与 GPU 处理第 N 个批次的工作重叠；
2. 为第 N 个批次做主机端 KV 分配（在 `prepare_for_decode` 中）可以与 GPU 处理第 N-1 个批次的工作重叠。

在 V2 引擎加上这些优化之后，在单张 B200 上以并发 32 运行 Qwen 3-8B 时，性能提升了超过 33%，从约 11.4 ktok/s 提升到约 15.3 ktok/s（[详情见此](https://github.com/sgl-project/sglang/pull/23000)）。

## 多个模型的高性能 DFlash 草稿模型现已可供使用

今天，我们发布一个面向 Qwen 3.5 397B-A17B 的新 DFlash 草稿模型。在我们测试的所有设置下，它的吞吐量都高于该模型原生的 MTP 投机解码——任务覆盖从 GSM8K 到 HumanEval 再到 MT-Bench，请求并发从 1 到 32。

<div style="text-align: center;">
  <img src="/images/blog/dflash-v2/dflash-perf-big-sweep.webp" style="width: 80%;"></img>
  <small>如需了解基准测试细节并自行复现这些数字，请参见 <a href="https://huggingface.co/modal-labs/Qwen3.5-397B-A17B-DFlash/tree/main/benchmark">Hugging Face 仓库</a>。</small>
</div>


你可以在 Z Lab 的 [Hugging Face DFlash 合集](https://huggingface.co/collections/z-lab/dflash)中找到更多高质量草稿模型。更多模型即将推出，敬请期待！

## 现在就在 SGLang 中试用 DFlash

你不必只读读这篇博客然后干着急。你可以[阅读代码](https://github.com/sgl-project/sglang/pull/23000)，可以用本文开头给出的命令部署一个 DFlash 加速的 SGLang 服务器，也可以直接在 [Modal](https://modal.com/docs/examples/sglang_low_latency) 上启动一个。

你也可以针对自己的数据或目标模型训练 DFlash 投机模型。同样的块扩散 + KV 注入方法适用于大多数目标 LLM。感兴趣的话，欢迎联系 [Z Lab](https://z-lab.ai) 或 [Modal](https://modal.com)！

更宏观地说：正因为开放权重模型的建设者、系统研究人员和开源社区的共同努力，你才能以最优的智能水平、速度和成本运行推理。无论是 [Z Lab](https://z-lab.ai/) 对 DFlash 这类技术的研究工作，还是 [Modal](https://modal.com/) 这类开源贡献者带来的特性与性能增强，全球最优秀的大模型推理成果都在源源不断地进入 SGLang 开源引擎，供你在其上构建、与之共建。

## 致谢

感谢所有为 Spec V2 和 DFlash 落地 SGLang 做出贡献的人。

Z Lab：Jian Chen、Yesheng Liang、Zhijian Liu。

Modal：David Wang、Charles Frye。

SGLang：Qiaolin Yu、Liangsheng Yin、Khoa Pham。
