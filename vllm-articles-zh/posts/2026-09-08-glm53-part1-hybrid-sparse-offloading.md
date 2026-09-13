---
title: "GLM 5.3 优化（第一部分）：vLLM 中的 Hybrid HiSparse 卸载"
title_en: "GLM 5.3 Optimizations, Part 1: Hybrid HiSparse Offloading in vLLM"
source: https://vllm.ai/blog/2026-09-08-glm53-part1-hybrid-sparse-offloading
crawled: 2026-09-12
translated: 2026-09-13
---

# GLM 5.3 优化（第一部分）：vLLM 中的 Hybrid HiSparse 卸载

> 原文：[GLM 5.3 Optimizations, Part 1: Hybrid HiSparse Offloading in vLLM](https://vllm.ai/blog/2026-09-08-glm53-part1-hybrid-sparse-offloading) · vLLM 博客

作者：vLLM 团队

[#glm](https://vllm.ai/blog/tags/glm)[#KV 缓存](https://vllm.ai/blog/tags/kv-cache)[#性能](https://vllm.ai/blog/tags/performance)

**TL;DR：** vLLM 的使命是让推理更快、服务成本更低。在这个两部分系列中，我们介绍为达成该目标而给 GLM 5.3 引入的新优化：第一部分演示 Hybrid HiSparse 如何助力单台 8× H200 节点上的聚合部署——对这个规模的模型而言，该节点的内存相当紧张。Hybrid HiSparse 让 GLM 5.3 能够以完整的 100 万上下文长度运行——这在之前的该硬件上是不可能的——并在各上下文长度上实现大幅更高的并发。

## 在需要时利用稀疏性

智能体工作负载的特点是大量并发请求，每个请求都带有不断增长的长上下文。由于 GPU 块池是固定的，KV 缓存终将耗尽空间，使并发请求无法再分配新块。

到目前为止，解决这一问题主要有两种选择，各有取舍：

- **抢占（Preemption）**选中一个请求，丢弃其 KV 缓存，之后再重新预填充。该请求在每次被驱逐时都要重新支付完整的 TTFT。
- **卸载（Offloading）**把块移到主机内存，但稠密注意力要求每个 token 都驻留在 GPU 上，因此并发请求数仍受 GPU 显存限制。

对 sparse-MLA KV 缓存而言，indexer 选出 top-K token，注意力只关注这些 token。[HiSparse](https://arxiv.org/abs/2608.07009) 正是利用这一行为，把除这些被选中 token 之外的全部 KV 缓存卸载到 CPU，从而给出每个请求所需 GPU 显存的有效上界。indexer KV 仍驻留 GPU 并随上下文长度增长，但整体要小得多，而 GLM 5.3 的 [IndexShare](https://arxiv.org/abs/2603.12201) 意味着每四个 sparse-MLA 层才有一个 indexer 层。

我们推出 Hybrid HiSparse，它还会在容量充足时继续把 KV 缓存留在 GPU 上，只有当 KV 缓存承压时才应用上述 HiSparse 卸载机制。热缓冲页按 token 索引，因此一页可以容纳取自许多不同 CPU 块的 token，从而在大范围上下文上实现缩减。这样，Hybrid HiSparse 只在系统承受 KV 缓存压力（即更高并发）时才支付 CPU-GPU 内存传输的代价。

![同一个池、两个不断增长的请求：抢占 vs 卸载](https://vllm.ai/blog-assets/figures/2026-09-08-glm53-part1-hybrid-sparse-offloading/hisparse-two-requests.svg)

同一个池、两个不断增长的请求：抢占 vs 卸载

*抢占：B 的槽位被释放，其 KV 不复存在。传统卸载：B 的 KV 保留在主机上，无需重新预填充，但在全部内容重新装进 GPU 之前 B 仍无法运行，于是只有 A 独自解码。混合稀疏卸载：每个请求就地释放自己最冷的页，同样的槽位被重新出租为新的尾部和热页，两者都继续解码。*

只有 Hybrid HiSparse 让两个请求都继续解码。热页与 KV 页从同一个块池租借，更重要的是，它们位于同一个 KV 缓存张量中，因此在 sparse MLA 内核眼里它们就是普通页。混合稀疏独有的特点是：部分 token 可以存在于热缓冲中，同时另一些 token 仍可存在于 GPU 常驻页中，从而减少 CPU 重载的量。

## 工作原理

![一个共享 GPU 块池上的三种 KV 驻留状态](https://vllm.ai/blog-assets/figures/2026-09-08-glm53-part1-hybrid-sparse-offloading/hisparse-residency.svg)

一个共享 GPU 块池上的三种 KV 驻留状态

*每个面板中圈出的是同样的六个 top-K token；变化的只是它们的驻留状态。实线箭头：未命中，把一行复制进热页。虚线箭头：热命中，无需复制即可复用。*

驻留按页跟踪，因此随着压力的起落，一个请求在三种状态之间迁移：

- **完全驻留**：全部 sparse-MLA KV 保持驻留 GPU，同时已完成的 prefix 页被主动物化到主机内存。
- **混合驻留**：请求的尾部留在 GPU 上，更早的页只存在于 CPU 内存，indexer 想要从那些页取的行放在热缓冲里。块表中真实块与空占位符并列，尾部永不被驱逐。一个融合内核完成 top-K 解析：常驻 token 就地读取，热 token 读取并刷新其 LRU 条目，未命中则把锁页主机内存中的一行复制进一个 LRU 槽位。解码路径上没有任何东西等待 CPU 决策，因此仍可被 CUDA Graph 捕获。
- **零驻留**：复用一个只存在于 CPU 内存中的 prefix 的新请求，以占位符和一页热页起步。行随 indexer 的选择而到达，因此我们只为模型实际关注的内容付费，而不是整个历史。

三种状态都能成立，是因为热缓冲并不是一份单独的分配。热缓冲页就是一个普通的 KV 缓存块，通过 vLLM 的 Hybrid Memory Allocator 从与常驻页相同的池中租借，请求首次需要时取走，不再需要时归还。无论行位于常驻页还是热缓冲，解析器交给 HMA 的都是 HMA 行 ID，HMA 用一次跨步即可完成聚合。一个请求释放的块可以成为另一个请求的热缓冲容量。

HiSparse 在压力到来之前就做好准备。当一个可缓存的 prefix 页完成时，HiSparse 在继续从 GPU 提供它的同时，把一次到 CPU 内存的复制排入队列。如果 GPU 缓存稍后被填满，该页无需再复制一次即可释放其 GPU 槽位。即使压力先到达更新的页，复制一经排队其 GPU 槽位即可复用，而 CPU 副本在传输完成后即可用于 prefix 复用。

`hisparse-glm` 分支让这条路径保持轻量：在前向传播之后，一次启动中把所有 sparse-MLA 层一起复制。复制排在模型的 GPU stream 上，同步因此简单而安全。

## 与 vLLM 其余部分协同

Hybrid HiSparse 是共享 HMA 池上的一个驻留策略，也是与 vLLM 其他 KV 机制并列的一个连接器，因此栈的其余部分照常工作。其他缓存组仍使用正常的前缀缓存、传输与卸载；indexer KV 尤其不受 HiSparse 影响：标准的 OffloadingConnector 可以用普通的块粒度存储独立卸载它。当 prefix 装不进常驻空间时，来自 P/D 分离的导入可以落在主机侧；投机解码则通过逐步可重放的解析器计划工作，并共享请求的热状态。

热缓冲默认为每个请求 2 倍 top-K 行，在保持缓冲尺寸较小的同时确保高命中率。由于 MLA KV 在各 TP rank 之间完全相同，锁页主机池按 DP 副本分配，并在其本地 TP rank 之间共享。TP rank 0 写入共享副本，每个 rank 都能读取，并用一个 CUDA 事件保持 stream 顺序。

## 数字

我们使用 OpenHands 多轮智能体工作负载（[来源](https://www.lmsys.org/blog/2026-07-13-glm52-optimization)）在 8× H200 上对 GLM 5.3 进行了基准测试：13 轮对话，第一轮 74,160 个 token，后续每轮 753 个 token，固定 220 个 token 输出。两个 TP8 部署都使用 MTP3、FP8 KV 缓存、142K 准入上限、`max_num_batched_tokens=32768`、`max_num_seqs=256` 与 `gpu_memory_utilization=0.92`。卸载基线使用 512 GiB 卸载池；Hybrid HiSparse 把同样的主机预算拆分为 384 GiB 的 HiSparse 池和 128 GiB 的卸载。

![GLM 5.3 交互性-吞吐量帕累托曲线，以及 Hybrid HiSparse 与 KV 卸载的实测并发运行请求数](https://vllm.ai/blog-assets/figures/2026-09-08-glm53-part1-hybrid-sparse-offloading/openhands-pareto-occupancy.svg)

GLM 5.3 交互性-吞吐量帕累托曲线，以及 Hybrid HiSparse 与 KV 卸载的实测并发运行请求数

*上：交互性-吞吐量扫描。交互性为 1000 除以平均 TPOT；逻辑总 token 吞吐量计入前缀缓存的提示词 token，并除以八块 GPU。下：每个基准测试点期间采集的非零 `vllm:num_requests_running` 样本的均值。Hybrid HiSparse：`e8ef1e07bd`。卸载基线：`80cb71c9ff`。*

我们计划让 Hybrid HiSparse 在 vLLM v0.30 中广泛可用。在此之前，这些结果所用的确切启动命令与基准客户端设置见下文[复现附录](#appendix-reproducing-our-results)。

## 只在需要的地方卸载

Hybrid HiSparse 只在需要的地方卸载。KV 从 GPU 起步，只要还有空间就留在那里；池子吃紧时，再逐页放弃驻留。热缓冲与常驻页共享池和张量，因此承压中的请求能以部分驻留继续解码，而不必等待槽位释放，也不必再次支付重新预填充的代价。

## 估算你的配置能获得的收益

下面的计算器使用同样的可用 HBM，估算普通 GPU 常驻 KV 与混合稀疏卸载的容量。调整工作负载、GPU、并行、热缓冲与主机池来逼近一次部署。调整这些数值可以感受并发可能的提升幅度。

计算器显示了为使 CPU 内存不成为 GPU 侧 indexer 与热缓冲所能支撑并发数瓶颈所需的最小 HiSparse 主机池。原生 indexer 卸载被建模为一个独立的全量 CPU 池：它扩展前缀缓存，但活跃的 indexer 历史仍消耗 HBM，因此仍属于运行请求上限的一部分。图中在假设 HiSparse 主机容量不构成限制的前提下，比较各序列长度上 HiSparse 与普通 GPU 常驻的总并发。热缓冲给每个请求增加固定的 GPU 开销，因此在短上下文时普通驻留能容纳更多请求；在更长上下文时，限制 sparse-MLA 驻留让 HiSparse 能支撑更多并发请求。增大热缓冲会用一部分容量换取更大的热缓存覆盖。

> **注意：** 这些是规划估算，不是有保障的服务上限：运行时工作区、请求长度偏斜与调度行为都可能降低实践中达到的并发。

> **注意：** MTP 可能进一步限制并发，因为其热缓冲必须一次性容纳所有验证 token。在本文发布时，这意味着把每个热缓冲的大小定为 `(num_speculative_tokens + 2) × top-K`。随着我们努力缩小缓冲，这一点可能变化。由于我们计划放宽该约束，下面的计算器目前未将其纳入考虑。

[交互式图表](https://vllm.ai/blog-assets/interactive\_pages/hisparse\_concurrency\_calculator.html)

[全屏打开并发计算器](https://vllm.ai/blog-assets/interactive_pages/hisparse_concurrency_calculator.html)

## 第二部分

这是用 vLLM 服务 GLM 5.3 系列的第一篇。Hybrid HiSparse 在 P/D 部署的解码侧最为关键，那里上下文最长、KV 压力最大。第二部分我们将在大规模部署上把各部分组合起来，结合新的与既有优化：Prefill Context Parallelism（PCP）、[Decode Context Parallelism（DCP）](https://vllm.ai/blog/2026-08-07-decode-context-parallelism)、[自适应验证](https://vllm.ai/blog/2026-08-14-dspark-adaptive-verification)与 Hybrid HiSparse。

## 致谢

vLLM 的 Hybrid HiSparse 实现由 Matthew Bonanni（Red Hat）、Lucas Wilkinson（Red Hat）与 Fares Obeid（Prime Intellect）开发。设计成型过程中与 Chao Lei（蚂蚁集团）和 Nicolò Lucchesi（Mistral）密切合作。Simon Veitner（Red Hat）为性能评估与本博客的撰写做出贡献。我们感谢 [HiSparse](https://arxiv.org/abs/2608.07009) 的作者们开发了本工作所采用的稀疏卸载概念。

## 附录：复现我们的结果

上述结果使用 [vLLM `e8ef1e07bd`](https://github.com/neuralmagic/vllm/commit/e8ef1e07bd2f174bebfe34c3a3e35e952931efb1)。我们计划让 Hybrid HiSparse 在 vLLM v0.30 中广泛可用；在那之前，请构建上述固定 checkout。使用以下命令在一台 8× H200 节点上启动 Hybrid HiSparse 配置：

```
vllm serve zai-org/GLM-5.3 \
  --served-model-name glm-agentx \
  --trust-remote-code \
  --host 0.0.0.0 \
  --port 8000 \
  --tensor-parallel-size 8 \
  --kv-cache-dtype fp8 \
  --gpu-memory-utilization 0.92 \
  --max-model-len 142000 \
  --max-num-batched-tokens 32768 \
  --max-num-seqs 256 \
  --enable-prefix-caching \
  --attention-config '{"hisparse_config":{"host_pool_gib":384}}' \
  --kv-transfer-config '{"kv_connector":"OffloadingConnector","kv_role":"kv_both","kv_connector_extra_config":{"spec_name":"TieringOffloadingSpec","cpu_bytes_to_use":137438953472}}' \
  --speculative-config '{"method":"mtp","num_speculative_tokens":3}' \
  --enable-auto-tool-choice \
  --tool-call-parser glm47 \
  --reasoning-parser glm45
```

`host_pool_gib` 按 DP 副本计，并取整到完整的主机块。128 GiB 卸载池存放 HiSparse 不管理的缓存组，包括 indexer KV。要复现不带 MTP 的 HiSparse，省略 `--speculative-config`。要得到图中所示的无 HiSparse MTP3 基线，保留 `--speculative-config`，省略 `--attention-config`，并把 `cpu_bytes_to_use` 改为 `549755813888`（512 GiB）。无 MTP 基线则同时省略 HiSparse 与 `--speculative-config`。HiSparse 目前仅在 NVIDIA GPU 上实现。

### 复现填充后的 OpenHands 扫描

基准客户端所需的一切都随本博客一起提供，因此这套做法是自足的：[`build_openhands_padded_dataset.py`](https://vllm.ai/assets/repro/2026-09-08-glm53-part1-hybrid-sparse-offloading/build_openhands_padded_dataset.py)、[`install_evalscope_deps.sh`](https://vllm.ai/assets/repro/2026-09-08-glm53-part1-hybrid-sparse-offloading/install_evalscope_deps.sh)与[`evalscope-all-nodeps.txt`](https://vllm.ai/assets/repro/2026-09-08-glm53-part1-hybrid-sparse-offloading/evalscope-all-nodeps.txt)。把三者下载到同一目录。EvalScope 固定在 `acd09b44384d53174768bb1063f675420f76fae9`。以下命令构建确定性的 128 段对话数据集，然后在每个点上用全新的对话运行 c1/c8/c16/c24/c32：

```
python3.12 -m venv client-venv
source client-venv/bin/activate
bash install_evalscope_deps.sh
pip install 'modelscope[datasets]==1.34.0' 'lxml==6.0.2'
pip install 'evalscope[perf] @ git+https://github.com/modelscope/evalscope.git@acd09b44384d53174768bb1063f675420f76fae9'

python build_openhands_padded_dataset.py \
  --model zai-org/GLM-5.3 \
  --pad-source openscience \
  --first-turn-length 74160 \
  --subsequent-turn-length 753 \
  --num-turns 13 \
  --number 128 \
  --output-path openhand-zai-org-GLM-5.3.json

evalscope perf \
  --model glm-agentx \
  --url http://127.0.0.1:8000/v1/chat/completions \
  --api openai \
  --dataset swe_smith \
  --dataset-path openhand-zai-org-GLM-5.3.json \
  --dataset-offset 52 \
  --max-tokens 220 \
  --multi-turn \
  --number 4 16 32 48 64 \
  --parallel 1 8 16 24 32 \
  --extra-args '{"ignore_eos":true}' \
  --name tp8-hisparse384-native128 \
  --outputs-dir results \
  --no-timestamp
```

对于图中数据，交互性为 `1000 / mean_TPOT_ms`；每 GPU 逻辑总 token 吞吐量为 EvalScope 的总 token 吞吐量除以八。每个测量点期间我们每 30 秒抓取一次 `/metrics`。请求占用为非零 `vllm:num_requests_running` 样本的均值，MTP 接受长度为 `1 + Δ(vllm:spec_decode_num_accepted_tokens_total) / Δ(vllm:spec_decode_num_drafts_total)`。
