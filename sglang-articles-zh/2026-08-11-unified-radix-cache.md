---
title: "统一基数树缓存：用一棵树支撑混合模型的前缀缓存"
title_en: "Unified Radix Cache: One Tree for Hybrid Model Prefix Caching"
author: "Zhangheng Huang, Ke Bao, Yi Zhang, Jialin Ouyang, Sicheng Pan"
date: "August 11, 2026"
previewImg: /images/blog/unified-radix-cache/image1.svg
type: blog
source: https://lmsys.org/blog/2026-08-11-unified-radix-cache/
translated: 2026-09-12
---

# 统一基数树缓存：用一棵树支撑混合模型的前缀缓存

> 原文：[Unified Radix Cache: One Tree for Hybrid Model Prefix Caching](https://lmsys.org/blog/2026-08-11-unified-radix-cache/) · LMSYS Blog · Zhangheng Huang, Ke Bao, Yi Zhang, Jialin Ouyang, Sicheng Pan

## 引言

当多个请求共享相同的 token 前缀时，前缀缓存（prefix caching）可以复用它们的 KV。在全注意力（full attention）下，共享前缀的 KV 一经计算完成，随着更多 token 的追加依然保持有效。后续带有相同前缀的请求可以直接复用这些 KV 条目，而不必在预填充（prefill）阶段重新计算。SGLang 使用一棵以 token 序列为键的基数树（radix tree）来跟踪这一映射关系。在预填充之前，这棵树会找出最长的可复用前缀，并将其 KV 的位置返回给调度器。

混合模型打破了这一单一的复用规则。一个请求可能同时组合全注意力 KV、滑窗注意力（SWA）KV 和循环状态（recurrent state），三者的复用语义各不相同：全注意力 KV 在整个匹配前缀范围内始终可复用；滑窗注意力 KV 只覆盖末尾的窗口；循环状态则只在某个精确的前缀检查点处有效。它们共享同一个 token 前缀，但**并不共享同一个可复用边界**。强行对所有部分施加同一个边界，要么丢弃本可有效的复用，要么允许无效的复用。

这些复用规则在不同模型家族中以不同的组合形式出现。如果为每种组合都编写一个专门的缓存类，就会产生一个组合爆炸式的类矩阵（class matrix），尤其是在叠加了 [HiCache](https://www.lmsys.org/blog/2025-09-10-sglang-hicache) 这类正交能力之后。早期的实现正是遵循了这一模式，在各个缓存变体之间重复实现了匹配、插入、加锁和逐出逻辑。

[统一基数树缓存（Unified Radix Cache）](https://github.com/sgl-project/sglang/pull/21206)通过将**共享前缀标识**与**组件特有的复用有效性**分离开来，解决了这种组合式设计难题。一棵以 token 为键的基数树拓扑为每个前缀提供统一的规范坐标，而全注意力 KV、滑窗注意力 KV 和 Mamba 检查点则以组件（component）的形式挂载其上。HiCache 原生地融入同一套组件生命周期，将组件标识延伸到 GPU L1、主机 L2 以及外部 L3 层级。辅助内存池可以以 sidecar 的形式跟随组件存在，而无需定义新的复用边界。新的模型家族可以组合这些现有能力，而不必再引入另一棵缓存树。

<figure class="figure-box">
<img src="/images/blog/unified-radix-cache/image1.svg" alt="统一基数树缓存的共享 token 拓扑、组件复用语义、HiCache 层级与 sidecar">
<figcaption>图 1：一棵基数树拓扑提供统一规范的前缀标识。FULL、SWA 和 MAMBA 组件分别执行路径、末尾窗口和检查点的复用语义，HiCache 则控制它们的数据驻留在 GPU L1、主机 L2 还是外部 L3 层级。sidecar 跟随声明的源内存池，不会改变树的行为。</figcaption>
</figure>

## 核心要点

- **一棵树取代缓存类矩阵。** 全注意力 KV、滑窗注意力 KV 和 Mamba 检查点共享同一棵基数树拓扑，而由各组件分别强制执行各自的复用语义。
- **钩子（hooks）让树核心保持通用。** 匹配、分裂、插入、加锁和逐出均由组件控制，因此新的混合组合不需要新的树实现。
- **HiCache 原生融入组件生命周期。** 组件与 sidecar 在 GPU L1、主机 L2 和外部 L3 层级之间迁移时保持相同的前缀标识。在多轮基准测试中，L3 让 DeepSeek-V4-Flash 后期轮次的命中率维持在 98% 左右，Inkling-Small 则达到 96.8%。
- **会话活跃度引导逐出。** 会话感知逐出会优先照顾活跃会话的缓存条目，但不会把它们钉在内存中。在 SWE-bench 测试中，会话感知的统一基数树缓存配置相比采用 LRU 的普通 HiRadixCache，TTFT（首 token 延迟）降低了 2.9% 至 16.6%。
- **实验性 Rust 树核心降低长前缀开销。** 在滑窗基准测试中，该原型在第 176 至 200 轮的 TTFT 最多比 Python 树低 42%。

## 一棵树，可组合的组件

混合模型将共享同一 token 前缀、却遵循不同复用规则的可缓存值组合在一起。统一基数树缓存把共享前缀映射到同一棵基数树拓扑，并把每种复用规则映射为一个 `TreeComponent`。`UnifiedTreeCore` 负责执行通用的匹配、分裂、插入、加锁和逐出机制；`UnifiedRadixCache` 负责协调内存池操作，而每个组件只需定义自身有差异的那部分语义。

FULL 组件始终存在。对于混合滑窗注意力模型，SGLang 会添加 SWA 组件；对于含混合循环层（recurrent layer）的模型，则添加 MAMBA 组件。例如，[DeepSeek-V4](https://www.lmsys.org/blog/2026-04-25-deepseek-v4/) 组合了 FULL 和 SWA，[Kimi-K3](https://www.lmsys.org/blog/2026-07-27-kimi-k3-day0-support) 为其 KDA 循环状态组合了 FULL 和 MAMBA，[Inkling](https://www.lmsys.org/blog/2026-07-15-inkling-day0-support) 则在同一棵树上组合了全部三种组件。新的模型家族可以直接复用现有的组件组合；如果它引入了当前组件集合无法表达的复用规则，SGLang 可以添加一个新的 `TreeComponent`，而不必再实现另一棵树。

FULL 提供路径复用：它为匹配前缀中的每个 token 保留 KV，并保护相应的祖先路径。SWA 提供窗口复用：它要求一段连续的末尾窗口，而较早的 SWA 槽位可能是空墓碑（tombstone），其对应的基数树节点仍保留在共享拓扑中。MAMBA 提供检查点复用：它要求在可复用前沿处保留一个循环状态检查点，并在修改之前将共享状态复制到请求私有的槽位中。这些组件对同一个候选边界施加不同的规则。

### 寻找安全的复用边界

在前缀匹配过程中，`UnifiedTreeCore` 沿着规范的 FULL 路径前进，并将每个访问到的节点视为候选边界。仅有 FULL 匹配成功并不够：每个处于激活状态的组件都会创建一个校验器（validator），只有当所有校验器都接受候选节点时，可复用边界才能前进。某个组件的拒绝并不会终止遍历，因为它可能接受更靠后的节点。在图 2 中，n1 和 n2 通过了所有校验器，而 n3 和 n4 至少未通过一个组件检查。遍历到达 n4，但最终保留 n2 作为最深的安全结果。

<figure class="figure-box">
<img src="/images/blog/unified-radix-cache/image2.svg" alt="match_prefix 如何选出被所有组件接受的边界">
<figcaption>图 2：组件投票将遍历深度与可复用前缀深度分离开来。遍历到达 n4，而 n2 仍是 FULL、SWA 和 MAMBA 共同接受的最深边界。</figcaption>
</figure>

遍历完成后，核心会构建一个 `MatchResult`。随后由各组件的收尾（finalizer）函数准备所选值以供复用，包括当共享的 MAMBA 检查点要变为某个请求私有时所需的复制操作。

### 贯穿树生命周期的组件钩子

同一套组件契约覆盖了树生命周期的其余部分：

| 生命周期 | 组件决定的内容 |
|-----------|----------------------------|
| 匹配 | `create_match_validator` 判断候选节点是否可复用；`finalize_match_result_in_tree_core` 与 `finalize_match_result_in_cache` 负责准备最终选定的结果。 |
| 分裂 | `redistribute_on_node_split` 决定基数树节点被拆分时组件数据如何迁移。 |
| 插入 | `update_component_on_insert_overlap` 与 `commit_insert_component_data` 决定组件拥有哪些内存池索引，以及新数据挂载到何处。 |
| 加锁 | `acquire_component_lock` 与 `release_component_lock` 保护一条路径、一个末尾窗口或单个检查点。 |
| 逐出 | `evict_device_start`、`evict_device_next_node` 和 `evict_device_end` 选择设备侧候选；`evict_component` 移除组件数据，`drive_host_eviction` 回收主机资源。 |

这一契约让树核心保持通用，同时允许各组件保留各自不同的正确性规则。移除某个组件的数据并不总会移除对应的基数树节点：剩余的拓扑仍可为其他组件提供锚定，被清空的组件槽位可以作为墓碑保留，直到该组件被重新写回或该节点不再需要。由于组件语义始终依附于同一个前缀标识，HiCache 可以将组件数据延伸到各个内存层级，而无需引入另一棵树。

## 跨内存层级的原生 HiCache

组件决定什么可以被复用，HiCache 决定可复用的数据驻留在哪里。统一基数树缓存在 GPU L1、主机 L2 和外部 L3 层级之间携带相同的组件标识，因此在层级之间移动数据不会改变其前缀标识或复用规则。组件负责描述所需的传输，`HybridCacheController` 负责执行实际的物理 I/O。

### 组件、锚点与 Sidecar

并非每个物理内存池都需要自己的组件。锚点（anchor）决定复用语义，或提供供其他内存池遵循的页索引。sidecar 存储独立的数据负载，但复用其声明的源内存池的索引；它随源内存池一起迁移，既不参与可复用边界的投票，也不会向基数树拓扑添加新的槽位。

[DeepSeek-V4](https://www.lmsys.org/blog/2026-04-25-deepseek-v4/) 具体展示了这一区分。FULL 覆盖逻辑前缀，而 SWA 只覆盖其末尾窗口，因此二者都是组件；它们还使用相互独立的设备索引空间。在图 3 的归一化六页示例中，分配器在运行时将 FULL 的尾部槽位 `F4, F5` 映射到 SWA 槽位 `S0, S1`。C4 与 C128 压缩 KV 内存池、indexer 缓冲区和压缩器状态则不定义新的复用边界，它们以 sidecar 形式注册：其中三个内存池跟随 FULL，两个跟随 SWA。

<figure class="figure-box">
<img src="/images/blog/unified-radix-cache/image3.svg" alt="DeepSeek-V4 的组件及其派生的 HiCache sidecar">
<figcaption>图 3：组件可以在相互独立的索引空间之间做转换，而每个 sidecar 则精确复用其声明源内存池的索引。这两种关系都在 HiCache 各层级间保持同一个共享前缀标识。</figcaption>
</figure>

### HiCache 多轮基准测试结果

多轮负载在每一轮都会扩展可复用的对话前缀。如果在 GPU 容量耗尽之后，较低层级仍能保留该前缀，那么缓存命中率就应保持较高水平，TTFT 的增长也应更加缓慢。

我们在两个混合模型上比较三种缓存配置：仅 GPU L1、GPU L1 加主机 L2，以及 GPU L1 加主机 L2 再加 500 GiB Mooncake Store 分布式内存层级作为 L3。DeepSeek-V4-Flash 使用 FULL 和 SWA，运行在四张 H200 GPU 上（TP4），48 个客户端，60 轮，每轮输入 4,096 个 token、输出 16 个 token。Inkling-Small 使用 FULL、SWA 和 MAMBA，运行在八张 H200 GPU 上（TP8），64 个客户端，30 轮，每轮输入 1,216 个 token、输出 64 个 token。

下面的命令大纲中包含模型路径和 Mooncake 客户端配置的占位符。它们记录了此处使用的运行时与负载相关 flag，但并不是一个完整可复现的环境。

<details>
<summary>DeepSeek-V4 与 Inkling 的配置大纲</summary>

每种缓存配置独立运行，并在启动下一种配置之前先停止当前的服务器。

#### DeepSeek-V4

```bash
export MODEL=/path/to/DeepSeek-V4-Flash-FP8
export SGLANG_ENABLE_UNIFIED_RADIX_TREE=1
COMMON="--trust-remote-code --model-path $MODEL --tp 4 --mem-fraction-static 0.9 \
  --context-length 262144 --page-size 64 --max-running-requests 16 \
  --host 0.0.0.0 --enable-cache-report --enable-metrics \
  --enable-metrics-for-all-schedulers"
HICACHE="--enable-hierarchical-cache --hicache-ratio 2 --hicache-size 0 \
  --hicache-mem-layout page_first --hicache-io-backend kernel \
  --hicache-write-policy write_through \
  --hicache-storage-prefetch-policy wait_complete"

# L1-only
sglang serve $COMMON --port 30001

# L2 HiCache
sglang serve $COMMON $HICACHE --port 30000

# Start the 500 GiB external Mooncake Store tier first, then add:
sglang serve $COMMON $HICACHE --port 30000 \
  --hicache-storage-backend mooncake \
  --hicache-storage-backend-extra-config "$MOONCAKE_CLIENT_JSON"

# Benchmark: use port 30001 for L1, or port 30000 for L2/L3.
PORT=30000
python3 benchmark/hicache/bench_multiturn.py \
  --host 127.0.0.1 --port "$PORT" --model-path "$MODEL" \
  --num-clients 48 --num-rounds 60 --request-length 4096 --output-length 16 \
  --max-parallel 16 --request-rate 64 --disable-auto-run \
  --disable-random-sample --enable-round-barrier --ready-queue-policy fifo \
  --seed 20260626
```

#### Inkling

```bash
export MODEL=/path/to/inkling
export SGLANG_ENABLE_UNIFIED_RADIX_TREE=1
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

COMMON="--trust-remote-code --model-path $MODEL --tp 8 \
  --mem-fraction-static 0.85 --context-length 262144 --page-size 64 \
  --max-total-tokens 750080 --max-running-requests 16 --host 0.0.0.0 \
  --enable-cache-report --enable-metrics --enable-metrics-for-all-schedulers \
  --mamba-radix-cache-strategy extra_buffer --swa-full-tokens-ratio 0.1 \
  --mamba-full-memory-ratio 0.1 --disable-prefill-cuda-graph"
HICACHE="--enable-hierarchical-cache --hicache-ratio 2 --hicache-size 0 \
  --hicache-mem-layout page_first --hicache-io-backend kernel \
  --hicache-write-policy write_through \
  --hicache-storage-prefetch-policy wait_complete"

# L1-only
sglang serve $COMMON --port 30001

# L2 HiCache
sglang serve $COMMON $HICACHE --port 30000

# Start the 500 GiB external Mooncake Store tier first, then add:
sglang serve $COMMON $HICACHE --port 30000 \
  --hicache-storage-backend mooncake \
  --hicache-storage-backend-extra-config "$MOONCAKE_CLIENT_JSON"

# Benchmark: use port 30001 for L1, or port 30000 for L2/L3.
PORT=30000
python3 benchmark/hicache/bench_multiturn.py \
  --host 127.0.0.1 --port "$PORT" --model-path "$MODEL" \
  --num-clients 64 --num-rounds 30 --request-length 1216 --output-length 64 \
  --max-parallel 16 --request-rate 64 --disable-auto-run \
  --disable-random-sample --enable-round-barrier --ready-queue-policy fifo \
  --seed 20260626 --log-file "inkling-${PORT}.jsonl" --tag inkling
```

</details>

<figure class="figure-box">
<img src="/images/blog/unified-radix-cache/image4.png" alt="DeepSeek-V4 与 Inkling 的 HiCache 多轮基准测试">
<figcaption>图 4：随着对话历史增长，L1 与 L1+L2 逐渐触及容量上限，此后缓存命中率下降、TTFT 上升。外部 L3 层级能在更多轮次中保留可复用前缀，并带来最高的有效输入 token 吞吐量。两行使用不同的模型、GPU 数量、请求形态和坐标尺度，因此只能在每一行内部比较不同层级。</figcaption>
</figure>

图 4 按轮次报告平均 TTFT 与提示词 token 缓存命中率。每一轮的命中率等于各请求被缓存的前缀 token 数之和除以其完整提示词长度之和。在两种负载中，L1 最先丢失可复用前缀，L2 推迟了容量上限的到来，而 L3 在预热之后保持高位，最终收在 96% 以上。

在 DeepSeek-V4-Flash 上，L3 将命中率维持在 98% 附近，平均 TTFT 保持在 9 秒以下，有效输入 token 吞吐量达到 145.5K tokens/s，而 L1 为 9.4K，L1+L2 为 14.3K。在 Inkling-Small 上，L3 最终命中率为 96.8%、TTFT 为 1.23 秒，有效输入 token 吞吐量达到 67.1K tokens/s，而 L1 为 15.5K，L1+L2 为 21.1K。

有效输入 token 吞吐量的定义沿用 [`bench_multiturn.py`](https://github.com/sgl-project/sglang/blob/2969ab3d4147e2ec76ec0c9b2b40bd32454f45f5/benchmark/hicache/bench_multiturn.py)：完整提示词长度之和除以实际运行时间（wall-clock）。由于命中缓存的前缀 token 也被计入其中，它衡量的是前缀复用下的服务推进速度，而不是纯粹的预填充计算吞吐量。在这些测试中，L3 的收益主要来自在较小层级达到容量上限之后仍能让可复用前缀保持可用。

## 共享树上的会话感知逐出

[会话感知逐出](https://github.com/sgl-project/sglang/pull/29173)直接实现在 `UnifiedRadixCache` 中。该机制提供了一种普通 LRU 所不具备的复用信号。LRU 只记录哪些缓存条目最近被访问过，却不知道哪些前缀属于活跃会话、可能在其后续轮次中再次被复用。在内存压力之下，它可能在保留无关条目的同时逐出某个活跃会话的 GPU KV。

应用为每个请求附加一个稳定的 `session_id`。当请求成功完成后，统一基数树缓存会为该会话注册其可复用区域：FULL 跟踪其前缀路径，SWA 跟踪其末尾窗口，MAMBA 跟踪其可复用前沿。所有会话仍然共享同一棵基数树拓扑，每一轮也仍然携带完整的提示词。

这些引用改变的是逐出顺序，而不是把内存钉住。FULL 按照是否被引用、会话引用计数以及配置的基础逐出优先级来排序候选条目。SWA 和 MAMBA 先扫描各自可复用区域内未被引用的条目，当需要更多空间时才回退到被引用的条目。当前策略覆盖 GPU L1 和主机 L2，不覆盖外部 L3 层级。

当应用调用 `/close_session` 时，统一基数树缓存会移除该会话的引用，但不会立即删除其缓存条目。会话代数（session generation）与有界的已关闭会话墓碑机制，可以防止在会话关闭或重开之后才结束的过期请求恢复已被释放的引用。

<figure class="figure-box">
<img src="/images/blog/unified-radix-cache/image6.svg" alt="FULL、SWA 与 MAMBA 组件上的会话感知逐出">
<figcaption>图 5：三个活跃会话共享同一棵基数树拓扑。FULL 跟踪被引用的前缀路径，SWA 跟踪末尾窗口，MAMBA 跟踪可复用前沿。GPU 与主机的逐出优先考虑未被引用的条目，被引用的条目仍可作为后备被逐出。关闭会话会移除其保留信号，但不会立即删除可复用的缓存条目。</figcaption>
</figure>

### SWE-bench 负载上的会话感知 HiCache

我们在 SWE-bench 智能体轨迹上评估了 DeepSeek-V4-Pro 和 Qwen3.5-397B-A17B，均使用 TP8 并开启 HiCache。基线使用带 LRU 的普通 HiRadixCache；对比组开启统一基数树缓存与 `--enable-session-radix-cache`。由于该对比同时改变了缓存实现与逐出策略，观察到的差异不应被解读为对会话感知能力的孤立消融实验。[基准测试记录](https://github.com/sgl-project/sglang/pull/29173#issuecomment-5090977488)提供了服务器 flag 与沙箱配置。

图 6 上半部分将设备缓存与主机缓存的命中率堆叠展示。在批大小 128 时，DeepSeek-V4-Pro 的设备命中率从约 42% 提升到 51%；在批大小 32 时，Qwen3.5-397B-A17B 从约 5% 提升到 34%；在批大小 64 时，Qwen 的设备加主机总命中率从约 58% 提升到 67%。

下半部分报告对应的 TTFT。相对于普通 HiRadixCache 基线，会话感知的统一基数树缓存配置在批大小 128 和 256 下，为 DeepSeek-V4-Pro 分别带来 11.0% 和 2.9% 的 TTFT 降幅；Qwen3.5-397B-A17B 在批大小 32 和 64 下分别观察到 13.5% 和 16.6% 的 TTFT 降幅。

<figure class="figure-box">
<img src="/images/blog/unified-radix-cache/image7.png" alt="DeepSeek-V4-Pro 与 Qwen3.5-397B-A17B 在 SWE-bench 上的缓存命中率与 TTFT">
<figcaption>图 6：上方面板堆叠展示缓存驻留情况：柔和的橙色和蓝色底部分别表示基线配置与统一（Unified）配置的设备缓存命中，灰色顶部表示主机缓存命中。下方面板报告实测 TTFT，每组柱子上方的标签显示相对基线的降幅。两个模型使用各自独立的 TTFT 坐标尺度。</figcaption>
</figure>

## 迈向 Rust 树核心

随着共享前缀不断增长，树的遍历、锁的簿记、LRU 更新和逐出扫描会给调度器的关键路径增加额外工作。`UnifiedRadixCache` 将这棵树的状态机与缓存编排分离开来，这使树核心成为原生实现的天然目标。

[实验性 Rust 统一基数树缓存](https://github.com/sgl-project/sglang/pull/29074)是一个可选开启、仅支持 L1 的原型。Rust 负责管理基数树拓扑、逐组件的锁记账、侵入式 LRU 链表以及逐出遍历；Python 仍然是请求到 token 映射和物理 KV 分配的唯一所有者。在修改树之后，Rust 会返回延迟执行的动作，由 Python 应用到内存池上。该原型支持 FULL、SWA 和 MAMBA，但不支持 HiCache。

我们在一个 200 轮的合成对话上比较该原型与 Python 版 `UnifiedRadixCache`。每一轮追加 100 个输入 token 并生成 100 个输出 token。两种后端使用相同的模型和服务器 flag，在相同的 GPU 上依次运行，各执行六次试验。负载涵盖：TP2 下的 Qwen3-32B 全注意力、TP2 下的 gpt-oss-20b SWA，以及 TP4 下的 Qwen3-Next-80B-A3B 混合 SSM。[复现脚本](https://github.com/lm-sys/lm-sys.github.io/tree/main/scripts/rust_radix_cache/multi_turn)需要 release 构建的 Rust 扩展。

<figure class="figure-box">
<img src="/images/blog/unified-radix-cache/image5.png" alt="实验性 Rust 与 Python 树核心在 FULL、SWA 与混合 SSM 模型上的 TTFT">
<figcaption>图 7：实验性仅 L1 的 Rust 原型与 Python 树的对比。上排显示总 TTFT 与以 CUDA event 计时的 GPU 预填充时长；下排显示二者之差，这并不是对 CPU 时间的直接测量。三个模型使用各自独立的 y 轴尺度。</figcaption>
</figure>

Rust 原型在 SWA 负载上取得了最大降幅：全部 200 轮的 TTFT 降低 38%，第 176 至 200 轮降低 42%。全注意力负载的 TTFT 总体降低 10%，最后 25 轮降低 18%。混合 SSM 负载的 TTFT 总体降低 5%，最后 25 轮降低 7%。

图 7 下排是将以 CUDA event 计时的 GPU 预填充时长从总 TTFT 中扣除后的结果。这一差值（residual）包含了树的簿记、调度、同步、采样、反解码（detokenization）、传输以及其他未插桩统计的开销。它并不是一个直接的 CPU 计时器，因此 Rust 与 Python 的完整差距不能只归因于基数树操作。混合 SSM 的结果恰好说明了这一边界：其差值大幅下降，但由于 GPU 前向计算占比更大，总 TTFT 上可见的变化受限。

上述测量结果仅适用于前述实验性原型。后续的 Rust `UnifiedTreeCoreInterface` RFC [#32710](https://github.com/sgl-project/sglang/pull/32710) 定义了目标所有权边界：编排与内存池管理仍保留在 Python 中，藏在可替换的树核心之后。该 RFC 目前仅支持 FULL，也未公布性能结果。

## 后续工作

统一基数树缓存确立了共享前缀标识，但系统中仍有三个部分需要围绕它进一步收敛：

- **完成可替换的 Rust 树核心。** 路线图 [#20415](https://github.com/sgl-project/sglang/issues/20415) 跟踪这一迁移。剩余工作是将 Rust 核心扩展到 SWA、MAMBA 和 HiCache，同时将内存池分配与编排继续保留在 Python 中。
- **将 GPU L1 直接连接到外部 L3 层级。** 直接 L3 模式将使主机 L2 成为可选的中转层（staging tier），并把分布式内存暴露为一个更大的共享缓存。这需要协同的准入、预取、传输与逐出，而不仅仅是又一个存储连接器。
- **在整个推理服务栈中协同智能体 KV 缓存。** 智能体负载已经在单个引擎内部从前缀缓存中获益。路线图 [#21846](https://github.com/sgl-project/sglang/issues/21846) 将同一缓存标识延伸到路由器、预填充与解码 worker 以及 HiCache，使这些层能够为会话、子智能体和工具调用协同执行预取、降级与保留。

## 结论

混合模型没有一个放之四海而皆准的可复用边界，但也不必为注意力与循环状态的每一种组合都单独建一棵基数树。统一基数树缓存只保留一棵规范统一的 token 拓扑，由 FULL、SWA 和 MAMBA 组件各自执行自己的复用、加锁与逐出语义。

这一共享标识的价值超出了前缀匹配本身：HiCache 让它在各内存层级间得以保留，会话引用把它转化为保留信号，而实验性 Rust 核心则展示了树簿记如何在不必把内存池所有权移出 Python 的前提下演进。更长期的方向是让可复用的缓存状态对整个推理服务系统可见，而不仅仅局限于本地分配器。

## 致谢

我们感谢阿里云 TairKVCache 团队共同主导了统一基数树缓存与 HiCache 在各混合模型上的集成，并验证了大规模生产环境部署。我们感谢 Thinking Machines Lab 团队在高负载下验证统一基数树缓存，并修复了跨组件组合的正确性问题。我们还感谢 Clank.world 团队在高并发生产部署中验证 Gemma 4 SWA HiCache。

我们还要感谢 Mingjun Zhang 在会话感知逐出方面的工作及其验证；感谢蚂蚁集团 SCT 推理团队的 Tingwei Huang 协助完成 Hybrid HiCache 与 Mooncake 的集成。我们感谢 Lianmin Zheng、Ishan Dhanani、Zhiqiang Xie、Chao Shi、Yanbo Yang、Shangming Cai、Hongjia Zhang 以及 SGLang 社区在架构评审、系统集成、基准测试和反馈方面的贡献。同时感谢相关路线图 [#20415](https://github.com/sgl-project/sglang/issues/20415) 和 [#21846](https://github.com/sgl-project/sglang/issues/21846) 的所有贡献者。

<style>
.figure-box {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #fafafa;
  padding: 12px 16px 10px;
  margin: 1.5em 0;
}
.figure-box img {
  margin: 0 auto;
  box-shadow: none;
}
.figure-box figcaption {
  font-size: 0.85em;
  line-height: 1.5;
  color: #6b7280;
  margin-top: 8px;
}
.figure-box figcaption code {
  font-size: 0.85em !important;
  background: transparent;
  color: inherit;
  padding: 0;
}
.article details {
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #fafafa;
  padding: 8px 16px;
  margin: 1em 0;
}
.article details summary {
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95em;
  color: #374151;
}
.article details[open] summary {
  margin-bottom: 8px;
}
.article blockquote {
  border-left: 3px solid #d1d5db;
  padding-top: 0.5em;
  padding-bottom: 0.5em;
}
.article table {
  border-collapse: collapse;
  border: 1px solid #d1d5db;
  font-size: 0.95rem;
}
.article table th,
.article table td {
  text-align: left;
  border: 1px solid #e5e7eb;
  padding: 0.6em 0.9em;
  vertical-align: top;
}
.article table th {
  background: #f3f4f6;
  font-weight: 600;
}
.article table tbody tr:nth-child(even) {
  background: #fafafa;
}
.article table td:first-child {
  width: 42%;
}
.article table code {
  font-size: 0.8rem !important;
  background: #eef1f5;
  padding: 0.1em 0.4em;
  border-radius: 4px;
  white-space: nowrap;
}
</style>
