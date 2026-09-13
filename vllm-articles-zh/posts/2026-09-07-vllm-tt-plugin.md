---
title: "在 Tenstorrent 硬件上服务 LLM：深入 vLLM TT 插件"
title_en: "Serving LLMs on Tenstorrent Hardware: Inside the vLLM TT Plugin"
source: https://vllm.ai/blog/2026-09-07-vllm-tt-plugin
crawled: 2026-09-12
translated: 2026-09-13
---

# 在 Tenstorrent 硬件上服务 LLM：深入 vLLM TT 插件

> 原文：[Serving LLMs on Tenstorrent Hardware: Inside the vLLM TT Plugin](https://vllm.ai/blog/2026-09-07-vllm-tt-plugin) · vLLM 博客

作者：Tenstorrent 团队

[#硬件](https://vllm.ai/blog/tags/hardware)[#生态](https://vllm.ai/blog/tags/ecosystem)

今天我们发布 [**vLLM TT Plugin**](https://github.com/tenstorrent/vllm-tt-plugin)，它通过标准的树外（out-of-tree）平台插件机制，把 [Tenstorrent](https://tenstorrent.com/) 加速器带入 vLLM。

将其与 vLLM 一同安装，只要 [TT-Metal](https://github.com/tenstorrent/tt-metal) 的 `ttnn` 可以导入，Tenstorrent 硬件就会被自动发现并注册为 vLLM 平台。服务接口没有任何变化：同样的 OpenAI 兼容 API、同样的请求格式、同样的客户端代码。

这个项目更有意思的地方并不在于后端本身的存在，而在于：Tenstorrent 设备长得并不太像 GPU，而 vLLM 的插件接口被证明足够通用，使我们能够把这些差异——相位受限的调度器、不同的数据并行拓扑、部分驻留在设备上的采样路径——完全表达在 vLLM 核心之外。

## 支持的模型

插件以 `TT` 前缀的约定注册 Tenstorrent 后端的架构，因此检查点由它声明的架构匹配，而不是按名称：

| 模型家族 | 架构 |
| --- | --- |
| Llama 3.1 / 3.2 / 3.3 | `TTLlamaForCausalLM` |
| Llama 3.2 Vision | `TTMllamaForConditionalGeneration` |
| Qwen 2.5 / Qwen 3 | `TTQwen2ForCausalLM`、`TTQwen3ForCausalLM` |
| Qwen 3.5 / Qwen 3.6 | `TTQwen3_5ForConditionalGeneration` |
| Qwen 2.5-VL / Qwen 3-VL | `TTQwen2_5_VLForConditionalGeneration`、`TTQwen3VLForConditionalGeneration` |
| Mistral / Mistral 3 | `TTMistralForCausalLM`、`TTMistral3ForConditionalGeneration` |
| Gemma 3 | `TTGemma3ForConditionalGeneration` |
| Gemma 4 | `TTGemma4ForCausalLM`、`TTGemma4ForConditionalGeneration`、`TTGemma4UnifiedForConditionalGeneration` |
| DeepSeek V3 | `TTDeepseekV3ForCausalLM` |
| GPT-OSS 20B / 120B | `TTGptOssForCausalLM` |

这些名称背后的类随 [TT-Metal](https://github.com/tenstorrent/tt-metal) 与运行时本身一同发布：每一个都是一个面向 vLLM 的生成器，包裹着手工编写的 TTNN 模型实现。插件本身不携带模型代码——它只注册名称，tt-metal 提供这些名称所解析到的实现。

由于匹配基于架构，一个条目可以覆盖多个版本——例如 `TTQwen3_5ForConditionalGeneration` 就是服务 `Qwen/Qwen3.6-27B` 的架构。

多模态覆盖值得一提，因为新后端往往长时间只支持文本：Llama 3.2 Vision、Qwen-VL、Qwen 3.6、Mistral 3 与 Gemma 3 如今都能通过该插件提供服务。

模型不必内置于插件中。把 `EXTRA_MODELS_DIR` 指向一个包含若干 bundle 文件夹的目录——每个文件夹持有 `vllm_metadata.json` 和一个 adapter 类——即可在启动时按 `TT<HFArch>` 约定注册架构。分发工具无需修改源码就能交付一个开箱即用的模型，而 `TT_VLLM_BUILTIN_MODELS=0` 则把注册表收窄为仅包含外部提供的那些。

以上就是你现在能服务的模型。本文其余部分讲它如何工作：网状（mesh）架构给一个按 GPU 形状设计的服务栈强加了哪些设计选择，以及我们在做这些选择时学到了什么。

## 为什么 Tenstorrent 后端看起来不一样

Tenstorrent 系统是**一个由片上网络（fabric）连接起来的核与芯片组成的网格（mesh）**。诸如 n150 或 n300 的单卡本身就已经是一个小网格；[QuietBox](https://tenstorrent.com/hardware/tt-quietbox) 是更大的网格；而 [Galaxy](https://tenstorrent.com/hardware/galaxy) 则是 32 颗 Wormhole 芯片，按运行时直接配置的拓扑连线（`FABRIC_1D`、`FABRIC_2D`、`FABRIC_1D_RING`）。程序按网格形状编译并被追踪（trace），fabric 在芯片之间搬移数据是编译后程序的一部分，而不是由主机发起的集合通信调用。

通过该插件服务的模型都是针对 TT mesh **手写的 [TTNN](https://github.com/tenstorrent/tt-metal) 实现**，覆盖从双芯片 n300 到 32 芯片 Galaxy。在这一系统内，它们运行与 GPU 上相同的并行化套路——跨芯片的张量并行、跨子网格的数据并行——只不过用 TTNN 表达并编译进网格程序，而不是配置成运行时的 rank。正是这种手工调优带来了更好的 tokens/$；这里不引用具体数字，最新数据见 [tenstorrent.com](https://tenstorrent.com/) 与 [GitHub](https://github.com/tenstorrent/tt-metal)。

![对比 GPU 上由主机发起的集合通信与编译后的 Tenstorrent 网格程序的示意图](https://vllm.ai/blog-assets/figures/2026-09-07-vllm-tt-plugin/mesh-vs-collectives.svg)

对比 GPU 上由主机发起的集合通信与编译后的 Tenstorrent 网格程序的示意图

图 1：跨芯片并行存在于何处。在按 GPU 形状设计的栈中，主机在每一层发起集合通信，并行性是以张量并行和流水线并行 rank 表达的运行时选择。在 Tenstorrent 上，整个网格被编译并追踪为一个程序，fabric 在其中于芯片间搬移数据，因此主机每步只需提交和读取一次。

这种编译模型——整个网格一份被追踪的程序——几乎决定了下游的一切：

- **没有可配置的张量并行或流水线并行 rank。** Galaxy 上的 70B 模型不是「TP=32 个进程」，而是一个为 32 芯片网格编译的程序。`MESH_DEVICE=TG` 取代了 `--tensor-parallel-size`，插件干脆直接拒绝 `-tp`/`-pp`，而不是假装支持它们。最契合（模型，网格）组合的并行方式直接实现在模型代码里。
- **工作单元是完整的一步追踪执行。** 设备执行的主导方式是针对固定批形状回放捕获的 trace，这使得同构、形状稳定的批次远比异构批次便宜。
- **采样可以在设备上进行。** 由于网格程序可以把采样一直带到最后，返回的 token 往往已经选定，主机根本看不到 logits。

其中每一点都与按 GPU 形状设计的推理栈中某处的假设相冲突。接下来的小节就是我们如何化解它们。

## 插件接入，而非分叉

vLLM 的硬件插件机制于 [2025 年 5 月推出](https://vllm.ai/blog/2025-05-12-hardware-plugin)，`vllm-ascend` 与 `vllm-spyre` 是最早的使用者；源自 Spyre 工作的可插拔调度器（pluggable scheduler）成果更是让我们这套方案得以成立的关键。我们深度依赖它。

插件注册了两个入口点：

| 入口点组 | 名称 | 目标 |
| --- | --- | --- |
| `vllm.platform_plugins` | `tt` | `vllm_tt_plugin.entrypoints:platform_plugin` |
| `vllm.general_plugins` | `tt_model_registry` | `vllm_tt_plugin.entrypoints:register` |

`platform_plugin()` **只在 `ttnn` 可导入时**返回 `TTPlatform`，因此把该包装进普通 CUDA 环境不会意外选中 Tenstorrent 平台。

从这里开始，一切都经由一次交接完成。`TTPlatform.check_and_update_config()` 校验配置、注册模型架构，并通过 vLLM 现有的扩展点替换为 Tenstorrent 自有的运行时类：

| vLLM 配置字段 | TT 实现 |
| --- | --- |
| `parallel_config.worker_cls` | `vllm_tt_plugin.worker.TTWorker` |
| `scheduler_config.scheduler_cls` | `vllm_tt_plugin.scheduler.TTScheduler` 或 `vllm_tt_plugin.lane_scheduler.TTLaneCoordinator` |

设备特有的选项挂在 vLLM 通用的 additional-config 命名空间上，而不是新增 CLI 标志：

```
--additional-config.tt.sample_on_device_mode all
--additional-config.tt.fabric_config FABRIC_1D_RING
```

**vLLM 核心中不存在任何 Tenstorrent 特有的内容。** 这一点决定了一个后端能否持续可用：支持节奏跟随 vLLM 的发布节奏，而不是我们自己的，谁也不会被困在一个落后上游三个月的分叉上。我们目前针对固定的 vLLM 版本做验证，并随插件 API 面逐渐稳定而扩大这个窗口。

## 基于相位的调度：纯预填充或纯解码步骤

上游 vLLM 的 V1 调度器基于 token 预算，这是有意为之。每个请求有已计算 token 数与目标 token 数；每一步在预算范围内分配更多 token 工作。预填充和解码并不是分开的模式，这正是分块预填充与混合进度批处理能够自然产生的原因。

Tenstorrent 路径的约束更强。每个调度步骤只会有三种结果之一：

- **纯预填充（prefill-only）**
- **纯解码（decode-only）**
- **空（empty）**

不存在预填充+解码混合的批次。在这一约束内仍支持分块预填充：超过每步 token 预算的提示词会被拆分到多个预填充步骤，纯解码步骤交错插在这些块之间，因此在长预填充进行时，进行中的请求仍能持续推进。默认仍优先接纳预填充工作，这样随后的解码步骤能以更大、更高效的批次运行；如果没有预填充可接纳但有解码请求在运行，该步骤就是纯解码，进度得以继续，KV 压力也能得到缓解。

![对比上游 token 预算步骤与 Tenstorrent 相位同构步骤的时间线](https://vllm.ai/blog-assets/figures/2026-09-07-vllm-tt-plugin/scheduling-phases.svg)

对比上游 token 预算步骤与 Tenstorrent 相位同构步骤的时间线

图 2：同一条长提示词在两种调度模型下的表现。上游把它摊到四个分块步骤上，并把其他请求的解码工作混进这些步骤。在 Tenstorrent 上，一步要么全是预填充、要么全是解码：提示词以纯预填充块运行，中间交错纯解码步骤，因此每一步都保持稳定、可追踪的形状，同时进行中的请求持续前进。

这是最可能让人皱眉的设计选择，因此值得精确说明它付出了什么、又没有付出什么。

**它换来了什么。** 追踪执行奖赏批形状的稳定性：一个纯预填充或纯解码的步骤可以回放恰好为该形状捕获的 trace，而混合两者的步骤则需要一个从未捕获过的形状。相位分离本身并不是 Tenstorrent 的怪癖：最大规模的 GPU 部署也在刻意做同样的选择——把预填充和解码放在完全独立的实例上，即[分离式服务](https://docs.vllm.ai/en/stable/features/disagg_prefill/)。Tenstorrent 调度器把同样的切分应用在单个引擎内的步骤粒度，而不是整个集群的实例粒度。

**它没有牺牲什么。** 广义上的连续批处理依然成立。请求进入 `waiting`，在结构化输出语法编译期间可能停泊在 `skipped_waiting`，可以在其他请求仍活跃时被接纳，可以被抢占再恢复，并且独立完成。限制只存在于设备单步*之内*，而不横跨请求生命周期。

**它确实付出了什么。** 交错粒度是完整的一步。上游把一个预填充块和进行中的解码混进同一步；Tenstorrent 调度器则是交替进行，因此一个解码请求仍要在自己的步骤之间等过每一个预填充块，而且每次模式切换都会清空下文描述的异步解码重叠流水线。两者都是调度策略层面的代价，而非根本性限制：无论硬件还是 vLLM，都不妨碍未来版本捕获混合形状的步骤。

## Galaxy 上的单进程 lane 数据并行

这是在 vLLM 其他地方都没有对应物的部分，也是我们最希望获得反馈的部分。

一些 Tenstorrent 模型——通过 `TT_LLAMA_TEXT_VER=llama3_70b_galaxy` 的 Llama 3.3 70B、通过 `TT_QWEN3_TEXT_VER=qwen3_32b_galaxy` 的 Qwen3-32B，以及 GPT-OSS——由*单次执行*（single-execute）生成器服务：一个程序横跨整个 Galaxy 网格，每步执行一次。没有任何子网格可以分给第二个引擎进程。标准的按 rank 分设备的多进程数据并行，在这里根本没有东西可划分。

**但是：** 这些模型是单*权重*、单*执行*的，却保有**四个相互独立的数据并行 KV 缓存**，各自位于自己的 DP 子网格上。于是，进程层面无物可分，而又有四样东西需要独立调度。

我们最初的实现是像 vLLM 通常那样给每个 DP rank 单独一个进程。然而，鉴于这些 rank 必须协商预填充还是解码的步骤类型，而实际上只有一次网格提交/读取，我们需要对 vLLM 核心做相当多的修改——远超硬件插件机制的范围。按 rank 的调度器确实并行运行了，但每一步额外的进程间 scatter/gather 的代价超过了那份并行度赚回来的收益。

更好的答案是把并行放进*单个*引擎进程内部：

`TTLaneCoordinator` 为每条 **lane** 持有一个独立的 `TTScheduler`。每条 lane 有自己的 `waiting` 和 `running` 队列、自己的准入决策、自己的 KV 缓存管理器，以及自己的 lane 本地块 ID 空间。新请求被分配到负载最轻的 lane，并始终绑定在该 lane 上。

由于设备同时执行所有 lane，协调器必须每步选定一个共享模式：

- 如果任何 lane 能接纳预填充，**所有** lane 都执行预填充步骤，并受与单调度器情形相同的解码交错节奏约束
- 否则，所有 lane 执行解码步骤
- 对所选模式没有工作的 lane，为合并后的批次贡献一个空切片

随后，协调器合并各 lane 的 `SchedulerOutput` 对象，worker 构造一份合并的设备输入，runner 再把结果按 lane 拆分回去——全部发生在同一个进程内，**没有任何进程级集合通信**——这正是拖垮多进程方案的那笔 scatter/gather 开销。

![对比被放弃的多进程 DP 设计与最终交付的单进程 lane-DP 设计的示意图](https://vllm.ai/blog-assets/figures/2026-09-07-vllm-tt-plugin/lane-dp.svg)

对比被放弃的多进程 DP 设计与最终交付的单进程 lane-DP 设计的示意图

图 3：同样的四个数据并行 KV 缓存，两种调度方式。上方是我们放弃的设计：四个引擎进程每一步都通过进程间 scatter/gather 协商共享的预填充或解码模式，尽管实际上只有一次网格提交和读取。下方是我们交付的设计：单个引擎进程，一个选定共享模式的协调器，四个持有 lane 本地块 ID 的独立调度器，一份合并的设备输入，以及按 lane 拆分回的结果。

有一个细节我们花了一段时间才弄对。如果一个被迫执行的预填充步骤接纳了零个 token（通常因为 KV 压力），而某些 lane 仍有解码工作在跑，这一步就会以解码模式重试。没有这个重试，KV 压力会把协调器拖进无进展循环：因为某个 lane *想*接纳而选中预填充，却因没有空闲块而什么也接纳不了，而本可以释放那些块的解码永远不会运行。

这一切面向用户的表面刻意保持平淡：

```
MESH_DEVICE=TG \
TT_LLAMA_TEXT_VER=llama3_70b_galaxy \
VLLM_RPC_TIMEOUT=900000 \
python examples/server_example_tt.py \
  --model "meta-llama/Llama-3.3-70B-Instruct" \
  --data_parallel_size 4 \
  --max_num_seqs 8 \
  --async-scheduling \
  --additional-config.tt.dispatch_core_axis col \
  --additional-config.tt.sample_on_device_mode all \
  --additional-config.tt.fabric_config FABRIC_1D_RING \
  --additional-config.tt.worker_l1_size 1344544 \
  --additional-config.tt.trace_region_size 220000000
```

`--data_parallel_size 4 --max_num_seqs 8` 变成四条进程内 lane，每条八个请求：32 并发，其中 `--max_num_seqs` 表示每条 lane 的容量。用户写下他们已经熟悉的同样标志，后端把它们映射到模型实际需要的拓扑——单次执行的 Galaxy 模型用进程内 lane，其余情况用每 rank 一个子网格的常规多进程 DP（在启动时发现并通过 `TT_VISIBLE_DEVICES` 分配）。启动日志会说明它选择了哪一种。

## 设备端采样，以及一个无人需要配置的回退

设置 `sample_on_device_mode` 后，网格程序会把采样一路带到 token 选择，返回 token 而不是 logits。

很多请求用不了这条路径——logprobs、惩罚项、允许 token 掩码、坏词过滤、自定义 logits 处理器。插件既不拒绝它们，也不要求用户选择模式，而是**按批次自行决定**：只要批次需要设备路径无法表达的东西，就回退到 vLLM 自带的 `LogitProcessor` 与采样器路径，可以时再切回设备路径。需要主机侧采样的请求以一次回读为代价获得正确结果；其余请求继续走快路径。`always_compat_sampling` 可强制走主机路径，用于调试或 A/B 对比。

## 解码重叠是异步回读，而不是异步执行模型

插件支持解码/主机重叠，以每个模型的 `supports_async_decode` 声明为开关——如果模型没有声明，平台会禁用异步调度，而不是让用户打开某个未经校验的东西。

究其底层，这里的「异步」含义比通常更窄，坦率的说法是：它是**异步主机回读**，而不是设备侧的执行线程：

1. 以 `read_from_device=False`（非阻塞）提交解码工作。
2. 用 `read_decode_output(..., async_read=True)` 启动主机回读，并把返回的事件与提交记录一起保存（同样非阻塞）。
3. 稍后在收尾阶段通过 `ttnn.event_synchronize(...)` 等待这些事件。
4. 只有在那之后，才把设备输出转换为主机张量与采样结果。

![展示通过异步主机回读实现解码重叠的时间线](https://vllm.ai/blog-assets/figures/2026-09-07-vllm-tt-plugin/async-decode.svg)

展示通过异步主机回读实现解码重叠的时间线

图 4：重叠从何而来。没有它时，主机回读并采样上一步期间，设备只能等待。有了异步解码，回读保持在进行中，主机在设备仍然忙碌时调度下一步并收尾上一步——唯一的阻塞等待是收尾时的 `ttnn.event_synchronize()`。

引擎维护一个深度为 2 的进行中队列，并在阻塞之前填满它，因此主机可以在第 *N* 步的回读仍在进行时调度第 *N+1* 步。只有当批次*稳定*时——形状稳定、设备端采样、没有结构化输出簿记、没有恢复的预填充——重叠才得以保持。任何一条被打破时，都会先排空未决工作再继续。

所以：预填充在实践中仍是同步的，解码重叠是稳态生成的快路径，而不是通用的异步流水线。插件仓库中的 [`docs/SCHEDULING.md`](https://github.com/tenstorrent/vllm-tt-plugin/blob/main/docs/SCHEDULING.md) 有完整论述，包括当执行器的输出线程与引擎线程竞争同一结果时保持正确性的收尾簿记。

## 当前限制

`TTPlatform` 在配置阶段就拒绝或调整不受支持的组合，因此用户会在任何东西到达设备之前得到明确的错误，而不是运行中途失败：

- **张量并行和流水线并行是支持的，但方式不同。** 并行来自网格形状（`MESH_DEVICE`）与模型实现，而不是 vLLM 的 TP/PP rank。
- **投机解码尚不支持。**
- **LoRA 尚不支持。**
- **提示词 logprobs 尚不支持**，会在请求校验时被拒绝。
- **前缀缓存**只对声明支持它的模型启用。
- **异步解码重叠**只对声明具备该能力的模型启用。
- **标准多进程 DP 不支持 MoE 模型。** 需要内部数据并行的单次执行模型（如 GPT-OSS）改为并入 lane-DP。
- **多主机服务尚不支持。** Tenstorrent 硬件可以扩展到远超单机，但当前的 TT 多主机模型实现无法直接映射到 vLLM 的多主机范式。

这些是当前 Tenstorrent 运行时与模型实现的属性，而不是硬件、软件栈或 vLLM 插件 API 的根本限制。其中每一项未来都可能支持，较大的几项已列入下文路线图。

## 上手试用

先安装 [TT-Metal](https://github.com/tenstorrent/tt-metal/blob/main/INSTALLING.md) 并激活该环境，然后克隆插件并在仓库根目录运行其安装脚本：

```
git clone https://github.com/tenstorrent/vllm-tt-plugin.git
cd vllm-tt-plugin
source docs/install-vllm-tt.sh
```

脚本以 `VLLM_TARGET_DEVICE=empty` 构建 vLLM——`tt` 平台由插件在运行时提供——并安装插件。然后启动服务并查询：

```
MESH_DEVICE=T3K VLLM_RPC_TIMEOUT=100000 python examples/server_example_tt.py
```

```
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "meta-llama/Llama-3.1-70B-Instruct", "prompt": "San Francisco is a", "max_tokens": 32}'
```

现有 OpenAI 客户端代码无需改动。

> **注意：** 当前安装流程会在 tt-metal 环境中针对 **0.26.0** 从源码构建 vLLM。各模型的命令、网格形状与所需环境变量见[插件 README](https://github.com/tenstorrent/vllm-tt-plugin)与相应的 tt-metal 模型演示。

## 接下来

- **更广的异步解码覆盖**——更多模型家族声明 `supports_async_decode`，更少的强制排空条件（尤其是设备端采样模式）。
- **更多模型的前缀缓存**，以及 lane-DP 对请求专属 RoPE 的支持，让视觉模型也能使用。
- **投机解码**，待网格侧的草稿/验证方案敲定之后。
- **多主机服务**——扩展到单机装不下的模型。

## 致谢

这项工作依托 Ascend 团队贡献的 vLLM 平台插件机制和 Spyre 团队贡献的可插拔调度器设计——没有后者，我们这样的相位调度器就意味着分叉。感谢 vLLM 维护者把 V1 扩展点保持得足够通用，让网格架构也能从中穿过。

我们感谢为这项工作做出贡献的众多才华横溢的人：Viktor Puš、Tomasz Cheda、Sanjar Adylov 与 Salar Hosseini。

我们特别希望就两件事获得反馈：把 `--data_parallel_size` 折叠成进程内 lane 是否是对单次执行模型合适的用户界面，以及接下来应优先支持哪些模型家族。欢迎在 [vllm-tt-plugin](https://github.com/tenstorrent/vllm-tt-plugin) 提 issue 和 pull request，也可以在 vLLM Slack 上找到我们。
