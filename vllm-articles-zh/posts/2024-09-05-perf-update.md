---
title: "vLLM v0.6.0：吞吐量提升 2.7x，延迟降低 5x"
title_en: "vLLM v0.6.0: 2.7x Throughput Improvement and 5x Latency Reduction"
source: https://vllm.ai/blog/2024-09-05-perf-update
crawled: 2026-09-12
translated: 2026-09-12
---

# vLLM v0.6.0：吞吐量提升 2.7x，延迟降低 5x

> 原文：[vLLM v0.6.0: 2.7x Throughput Improvement and 5x Latency Reduction](https://vllm.ai/blog/2024-09-05-perf-update) · vLLM 博客

vLLM 团队

[#性能](https://vllm.ai/blog/tags/performance)

**TL;DR：** vLLM 在 Llama 8B 模型上实现了 2.7x 的吞吐量提升和 5x 的 TPOT（每输出 token 耗时）加速，在 Llama 70B 模型上实现了 1.8x 的吞吐量提升和 2x 的 TPOT 降低。

![](https://vllm.ai/blog-assets/figures/perf-v060/llama8B_comparison.png)   ![](https://vllm.ai/blog-assets/figures/perf-v060/llama70B_comparison.png)
vLLM v0.5.3 与 v0.6.0 的性能对比：Llama 8B 在 1xH100、Llama 70B 在 4xH100 上，使用 ShareGPT 数据集（500 个提示）。TPOT 在 32 QPS 下测得。

一个月前，我们发布了[性能路线图](https://blog.vllm.ai/2024/07/25/lfai-perf.html)，承诺将性能作为首要任务。今天，我们发布了 vLLM v0.6.0，相比 v0.5.3 带来 1.8-2.7x 的吞吐量提升，在保持丰富特性和出色易用性的同时达到了最先进水平（SOTA）的性能。

我们将首先诊断 vLLM 此前的性能瓶颈，然后介绍我们在过去一个月中实现并落地的解决方案，最后展示最新版 vLLM v0.6.0 与其他推理引擎的基准测试结果。

### 性能诊断

LLM 推理需要 CPU 与 GPU 的紧密协作。虽然主要计算发生在 GPU 上，但 CPU 在请求的服务与调度中也扮演着重要角色。如果 CPU 的调度速度跟不上，GPU 就会闲置等待 CPU，最终导致 GPU 利用率低下，拖累推理性能。

一年前 vLLM 首次发布时，我们主要针对内存有限的 GPU 上的较大模型进行优化（例如 NVIDIA A100-40G 上的 Llama 13B）。随着内存更大、速度更快的 GPU（如 NVIDIA H100）日益普及，以及模型针对推理的优化日益成熟（例如 GQA 和量化等技术），推理引擎中其他 CPU 部分所花费的时间成为显著瓶颈。具体而言，我们的性能分析结果显示，对于在 1 块 H100 GPU 上运行的 Llama 3 8B：

- HTTP API 服务器占总执行时间的 33%。
- 总执行时间的 29% 花费在调度上，包括从上一步收集 LLM 结果、为下一步调度待运行的请求，以及将这些请求准备为 LLM 的输入。
- 最后，只有 38% 的时间花费在 LLM 的实际 GPU 执行上。

通过上述基准测试，我们在 vLLM 中发现了两个主要问题：

- **CPU 开销高。** vLLM 的 CPU 组件耗时惊人地长。为了让 vLLM 的代码易于理解和贡献，我们将 vLLM 的大部分保持为 Python，并使用了许多 Python 原生数据结构（如 Python 列表和字典）。这成为了显著的开销，导致调度和数据准备耗时偏高。
- **各组件之间缺乏异步性。** 在 vLLM 中，许多组件（如调度器和输出处理器）以同步方式执行，会阻塞 GPU 执行。这主要是由于：1）我们最初的假设是模型执行会比 CPU 部分慢得多；2）便于实现许多复杂的调度情形（例如束搜索的调度）。然而，这一问题导致 GPU 等待 CPU，降低了其利用率。

总结来说，vLLM 的性能瓶颈主要源于*阻塞 GPU 执行的 CPU 开销*。在 vLLM v0.6.0 中，我们引入了一系列优化来将这些开销降到最低。

### 性能增强

为了让 GPU 保持忙碌，我们做了以下几项增强：

#### 将 API 服务器与推理引擎分离为不同进程（[PR #6883](https://github.com/vllm-project/vllm/pull/6883)）

![](https://vllm.ai/blog-assets/figures/perf-v060/illustration-api-server.png)服务进程架构改造前后示意图。我们将 HTTP 服务组件从 vLLM 引擎中分离出来，并用 ZMQ socket 将二者连接。这种架构确保两个 CPU 密集型组件相互隔离。

通过细致的性能分析，我们发现管理网络请求以及为 OpenAI 协议格式化响应会消耗相当多的 CPU 周期，尤其是在高负载并开启 token 流式传输的情况下。例如，Llama3 8B 在轻负载下每 13 ms 生成 1 个 token，这意味着前端需要每秒回传 76 个对象，而在数百个并发请求下这一需求还会进一步增加。这对旧版 vLLM 构成了挑战，因为 API 服务器和推理引擎运行在同一个进程中。结果是，推理引擎和 API 服务器的协程不得不竞争 Python GIL，造成 CPU 争用。

我们的解决方案是将负责请求校验、分词和 JSON 格式化的 API 服务器，与负责请求调度和模型推理的引擎分离开来。我们使用开销很低的 ZMQ 连接这两个 Python 进程。通过消除 GIL 约束，两个组件都可以在无 CPU 争用的情况下更高效地运行，从而提升性能。

即使在拆分为两个进程之后，我们发现引擎内部的请求处理方式以及与 HTTP 请求的交互方式仍有很大改进空间。我们正在积极进一步提升 API 服务器的性能（[PR #8157](https://github.com/vllm-project/vllm/pull/8157)），力争在不久的将来使其效率接近离线批量推理。

#### 提前批量调度多个步骤（[PR #7000](https://github.com/vllm-project/vllm/pull/7000)）

![](https://vllm.ai/blog-assets/figures/perf-v060/illustration-multi-step.png)
vLLM 多步调度方法示意图。通过一次批量执行多个调度步骤，我们让 GPU 比以前更忙碌，从而降低延迟并提升吞吐量。

我们发现 vLLM 调度器和输入准备带来的 CPU 开销导致 GPU 利用率不足，吞吐量不理想。为解决这一问题，我们引入了*多步调度*（multi-step scheduling），它一次执行调度和输入准备，然后让模型连续运行 `n` 步。通过确保 GPU 在这 `n` 步之间无需等待 CPU 而持续处理，该方法将 CPU 开销摊薄到多个步骤上，显著减少 GPU 空闲时间，提升整体性能。

这将 4xH100 上运行 Llama 70B 模型的吞吐量提升了 28%。

#### 异步输出处理（[PR #7049](https://github.com/vllm-project/vllm/pull/7049)、[#7921](https://github.com/vllm-project/vllm/pull/7921)、[#8050](https://github.com/vllm-project/vllm/pull/8050)）

![](https://vllm.ai/blog-assets/figures/perf-v060/illustration-async-output-processing.png)
vLLM 异步输出处理示意图。通过将输出数据结构处理的 CPU 工作与 GPU 计算重叠，我们减少了 GPU 空闲时间并提升了吞吐量。

延续最大化 GPU 利用率的努力，我们还彻底改造了 vLLM 中模型输出的处理方式。

此前，vLLM 在每生成一个 token 后，会将模型输出从 GPU 搬到 CPU，检查停止条件以判断请求是否完成，然后再执行下一步。这一输出处理往往很慢，涉及对生成的 token ID 进行反分词（de-tokenize）和字符串匹配，且开销随批大小增长而增加。

为解决这一低效问题，我们引入了*异步输出处理*（asynchronous output processing），将输出处理与模型执行重叠起来。vLLM 现在不立即处理输出，而是将其延迟——在执行第 `n+1` 步的同时处理第 `n` 步的输出。该方法假设第 `n` 步没有请求已满足停止条件，因此每个请求会产生多执行一步的轻微开销。然而，GPU 利用率的大幅提升远超这一成本，带来了整体性能的改善。

这将 4xH100 上运行 Llama 70B 模型的每输出 token 耗时降低了 8.7%。

#### 其他优化

为进一步降低 CPU 开销，我们仔细审查了整个代码库并进行了以下优化：

- 随着请求的到来和完成，Python 会不断分配和释放新对象。为减轻这一开销，我们创建了对象缓存（[PR #7162](https://github.com/vllm-project/vllm/pull/7162)）来保存这些对象，将端到端吞吐量显著提升 24%。
- 从 CPU 向 GPU 发送数据时，我们尽可能使用非阻塞操作（[PR #7172](https://github.com/vllm-project/vllm/pull/7172)）。这样 CPU 可以在 GPU 拷贝数据的同时发起多次拷贝操作。
- vLLM 支持多样的注意力后端和采样算法。对于使用简单采样请求的常见工作负载（[PR #7117](https://github.com/vllm-project/vllm/pull/7117)），我们引入了一条跳过复杂步骤的快速代码路径。

在过去一个月里，vLLM 社区为此类优化付出了大量努力。我们将继续优化代码库以提升效率。

### 性能基准测试

凭借上述努力，我们很高兴地分享：与上个月的 vLLM 相比，性能已大幅提升。根据我们的性能基准测试，它已达到最先进水平。

**服务引擎。** 我们将 vLLM v0.6.0 与 TensorRT-LLM r24.07、SGLang v0.3.0 和 lmdeploy v0.6.0a0 进行基准对比。其他引擎使用其默认设置。对于 vLLM，我们通过设置 `--num-scheduler-steps 10` 开启了多步调度。我们正在积极努力使其成为默认开启。

**数据集。** 我们使用以下三个数据集对不同服务引擎进行基准测试：

- **ShareGPT**：从 ShareGPT 数据集中以固定随机种子随机抽取的 500 个提示。
  - 平均输入 token：202，平均输出 token：179
- **Prefill-heavy（预填充密集）数据集**：从 sonnet 数据集合成的 500 个提示，平均约 462 个输入 token 和 16 个输出 token。
- **Decode-heavy（解码密集）数据集**：从 sonnet 数据集合成的 500 个提示，平均约 462 个输入 token 和 256 个输出 token。

**模型。** 我们在两个模型上进行基准测试：Llama 3 8B 和 70B。我们没有使用最新的 Llama 3.1 模型，因为搭配 TensorRT LLM backend v0.11 的 TensorRT-LLM r24.07 尚不支持它（[issue 链接](https://github.com/NVIDIA/TensorRT-LLM/issues/2105)）。

**硬件。** 我们使用 A100 和 H100 进行基准测试，它们是用于推理的两款主流高端 GPU。

**指标。** 我们评估以下指标：

- Time-to-first-token（TTFT，首 token 延迟，单位 ms）。图中展示了均值和均值的标准误。
- Time-per-output-token（TPOT，每输出 token 耗时，单位 ms）。图中展示了均值和均值的标准误。
- 吞吐量（单位：请求/秒）。
  - 吞吐量在 QPS inf 条件下测得（即所有请求同时到达）。

#### 基准测试结果

在 ShareGPT 和 Decode-heavy 数据集上，vLLM 在服务 Llama-3 模型时于 **H100 上取得了最高吞吐量**。

![](https://vllm.ai/blog-assets/figures/perf-v060/overall_throughput.png)
在不同工作负载下，与其它框架相比，vLLM 在 H100 上的 Llama 8B 和 70B 上实现了高吞吐量。

关于其余性能基准测试，以及采集到的首 token 延迟（TTFT）和每输出 token 耗时（TPOT）的详细指标，请参阅[附录](#appendix)以获取更多数据和分析。你可以按照[这个 GitHub issue](https://github.com/vllm-project/vllm/issues/8176) 来复现我们的基准测试。

**当前优化的局限。** 虽然我们当前的优化带来了显著的吞吐量提升，但也存在性能上的取舍，尤其是多步调度带来的：

- *逐 token 延迟出现波动：* 在我们当前的多步调度实现中，我们会按批一次性返回多个步骤的输出 token。从终端用户的角度看，他们会成批收到回复的 token。我们正在通过将中间 token 流式回传给引擎来解决这一问题。
- *低请求速率下 TTFT 更高：* 新请求只能在当前多步执行结束后才开始执行。因此，更高的 `--num-scheduler-steps` 会在低请求速率下导致更高的 TTFT。我们的实验关注的是高 QPS 下的排队延迟，因此该效应在附录的结果中并不显著。

### 结论与未来工作

在这篇文章中，我们讨论了 vLLM 中带来 1.8-2.7x 吞吐量提升、并追平其他推理引擎的性能增强。我们将继续稳步提升性能，同时不断扩展模型覆盖、硬件支持和多样化特性。对于本文讨论的特性，我们将继续打磨，使其达到生产级可用。

同样重要的是，我们还将专注于改进 vLLM 的核心以降低复杂度，从而降低贡献门槛，解锁更多性能增强。

### 参与进来

如果你还没有，我们强烈建议你更新 vLLM 版本（安装说明见[这里](https://docs.vllm.ai/en/latest/getting_started/installation.html)）并亲自试一试！我们始终乐于了解你的使用场景，以及如何让 vLLM 为你做得更好。你可以通过 [vllm-questions@lists.berkeley.edu](mailto:vllm-questions@lists.berkeley.edu) 联系 vLLM 团队。vLLM 也是一个社区项目，如果你有兴趣参与和贡献，欢迎查看我们的[路线图](https://roadmap.vllm.ai/)并认领[适合新手的 issue](https://github.com/vllm-project/vllm/issues?q=is:open+is:issue+label:%22good+first+issue%22)。欢迎[在 X 上关注我们](https://x.com/vllm_project)以获取更多更新。

如果你身在湾区，可以在以下活动中与 vLLM 团队见面：[vLLM 与 NVIDIA 合办的第六届 Meetup（09/09）](https://lu.ma/87q3nvnh)、[PyTorch Conference（09/19）](https://pytorch2024.sched.com/event/1fHmx/vllm-easy-fast-and-cheap-llm-serving-for-everyone-woosuk-kwon-uc-berkeley-xiaoxuan-liu-ucb)、[CUDA MODE IRL Meetup（09/21）](https://events.accel.com/cudamode)，以及[首届 Ray Summit 的 vLLM 专题（10/01-02）](https://raysummit.anyscale.com/flow/anyscale/raysummit2024/landing/page/sessioncatalog?search.sessiontracks=1719251906298001uzJ2)。

无论你身在何处，都别忘了报名参加线上的[双周 vLLM Office Hours](https://neuralmagic.com/community-office-hours/)！每两周都会有新话题讨论，下一期将深入剖析性能增强。

### 致谢

本博文由伯克利的 vLLM 团队起草。性能提升来自 vLLM 社区的集体努力：来自 Neural Magic 的 [Robert Shaw](https://github.com/robertgshaw2-neuralmagic) 以及来自 IBM 的 [Nick Hill](https://github.com/njhill)、[Joe Runde](https://github.com/joerunde) 主导了 API 服务器重构；来自 UCSD 的 [Will Lin](https://github.com/SolitaryThinker) 以及来自 Anyscale 的 [Antoni Baum](https://github.com/Yard1)、[Cody Yu](https://github.com/comaniac) 主导了多步调度工作；来自 Databricks 的 [Megha Agarwal](https://github.com/megha95) 和来自 Neural Magic 的 [Alexander Matveev](https://github.com/alexm-neuralmagic) 主导了异步输出处理；还有 vLLM 社区的众多贡献者贡献了各项优化。所有这些努力让我们齐心协力，取得了巨大的性能提升。

## 附录

我们在本节中收录详细的实验结果。

#### Llama 3 8B 在 1xA100 上

在 Llama 3 8B 上，vLLM 在 ShareGPT 和 decode-heavy 数据集上取得了与 TensorRT-LLM 和 SGLang 相当的 TTFT 和 TPOT。LMDeploy 的 TPOT 低于其他引擎，但 TTFT 总体偏高。吞吐量方面，TensorRT-LLM 在所有引擎中吞吐量最高，vLLM 在 ShareGPT 和 decode-heavy 数据集上吞吐量排名第二。

![](https://vllm.ai/blog-assets/figures/perf-v060/A100_8B.png)

#### Llama 3 70B 在 4xA100 上

在 Llama 3 70B 上，vLLM、SGLang 和 TensorRT-LLM 的 TTFT 和 TPOT 相近（LMDeploy 的 TPOT 更低但 TTFT 更高）。吞吐量方面，vLLM 在 ShareGPT 数据集上取得最高吞吐量，在其他数据集上与其他引擎的吞吐量相当。

![](https://vllm.ai/blog-assets/figures/perf-v060/A100_70B.png)

#### Llama 3 8B 在 1xH100 上

vLLM 在 ShareGPT 和 Decode-heavy 数据集上取得了最先进的吞吐量，但在 Prefill-heavy 数据集上吞吐量较低。

![](https://vllm.ai/blog-assets/figures/perf-v060/H100_8B.png)

##### Llama 3 70B 在 4xH100 上

vLLM 在 ShareGPT 和 Decode-heavy 数据集上拥有最高吞吐量（尽管仅略高于 TensorRT-LLM），但 vLLM 在 Prefill-heavy 数据集上的吞吐量较低。

![](https://vllm.ai/blog-assets/figures/perf-v060/H100_70B.png)
