---
title: "vLLM 中的原生强化学习 API"
title_en: "Native RL APIs in vLLM"
source: https://vllm.ai/blog/2026-05-28-native-rl-apis
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM 中的原生强化学习 API

> 原文：[Native RL APIs in vLLM](https://vllm.ai/blog/2026-05-28-native-rl-apis) · vLLM 博客

作者：Aaron Hao、Sumanth Hegde、Kyle Sayers、Kourosh Hakhamaneshi 以及 vLLM 团队

[#强化学习](https://vllm.ai/blog/tags/reinforcement-learning)[#异步RL](https://vllm.ai/blog/tags/async-rl)

随着后训练工作负载不断扩展，我们看到 vLLM 被广泛采用为首选推理引擎。然而，两个问题反复出现：

1. 训练与推理之间的权重同步以临时（ad-hoc）方式实现，并在各框架间重复造轮子。
2. 异步 RL 设置在规模化时变得脆弱，尤其是在 P/D 和 DPEP 部署中。

在本文中，我们介绍 vLLM 中的两项改进：

1. 原生权重同步 API，为 RL 框架提供标准接口。
2. 对异步 RL 的改进支持，包括新的暂停模式以及对 DPEP 场景死锁的修复。

## vLLM 中的原生权重同步 API

### 背景

在线 RL 环境中，vLLM 模型权重必须定期同步，以确保生成的 rollout 来自最新或较新的模型权重版本，从而提供更有用的反馈。

![Figure 1: RL system overview.](https://vllm.ai/blog-assets/figures/2026-05-28-native-rl-apis/rl_system_overview.png)

图 1：RL 系统概览。

传统上，这一权重加载由各 RL 框架分别处理，通常通过为 vLLM worker 扩展自定义的接收和加载权重逻辑来实现。虽然可行，但会带来几个问题：

- **额外复杂度**：框架作者必须实现并维护自定义 worker 扩展，如果对流行的传输策略提供原生支持会更好。
- **重复劳动**：大多数 RL 框架最终都有非常相似的实现（如打包张量传输、RPC 端点）。
- **版本锁定**：框架通常以临时方式处理接收权重的预处理/后处理，以便 vLLM worker 能够加载，这可能导致实现被版本锁死。

### vLLM 中的新 API

我们在 vLLM 中引入原生权重同步 API 来将其标准化。权重传输 API 由四个阶段和一个可插拔后端组成：

1. **初始化**（`init_weight_transfer_engine`）：建立训练器与推理 worker 之间的通信通道。在训练循环开始前调用一次。
2. **开始权重更新**（`start_weight_update`）：开始一次权重更新。在每个训练步（或一批步）之后调用。让 vLLM worker 准备好接收权重。
3. **更新权重**（`update_weights`）：把全部或部分权重从训练器更新到推理引擎。可多次调用以进行分块权重传输。
4. **完成权重更新**（`finish_weight_update`）：结束当前权重更新。执行任何必要的后处理（如量化）。

相应的 API 在 API 服务器和引擎层级均有实现。

目前我们支持以下后端：

1. **NCCL**：使用 NCCL 广播操作在位于不同 GPU 上的训练与推理 worker 之间传输权重。
2. **IPC**：使用 CUDA IPC，通过共享内存句柄进行同设备权重传输。

两个后端都支持优化的打包（packed）实现，以最小化序列化开销。

核心传输逻辑通过可插拔的 `WeightTransferEngine` 抽象实现，把权重传输与 worker 实现分离，让用户可以轻松引入自己的实现。核心思想是：**初始化**和**更新权重**阶段通常由 RL 框架开发者定制，包含*传输*逻辑；而 start 和 finish 是控制消息，在 vLLM 中执行与传输方式无关的预处理/后处理。

> **注意：** HTTP 权重传输端点要求设置 `VLLM_SERVER_DEV_MODE=1`。

### 示例

例如，在 vLLM 上通过 NCCL 并结合 FP8 量化进行权重传输时，各操作如下所示：

![Figure 2: Weight transfer via NCCL with FP8 quantization on vLLM.](https://vllm.ai/blog-assets/figures/2026-05-28-native-rl-apis/weight_transfer_nccl.svg)

图 2：在 vLLM 上通过 NCCL 结合 FP8 量化进行权重传输。

新 API 的用法如下：

**1. 为权重传输配置引擎**

```
from vllm import LLM
from vllm.config import WeightTransferConfig

llm = LLM(
    model="my-model",
    weight_transfer_config=WeightTransferConfig(backend="nccl"),
)
```

**2. 初始化通信状态**：初始化训练器与推理引擎之间的通信状态。训练器的 rank 0 进程与所有推理 worker 加入共享的 NCCL 进程组。

```
from vllm.distributed.weight_transfer.base import WeightTransferInitRequest

# Initialization for inference
llm.init_weight_transfer_engine(
    WeightTransferInitRequest(      # <--- initialization parameters
        init_info=dict(
            master_address=master_address,
            master_port=master_port,
            rank_offset=1,          # <--- offset accounts for trainer rank 0
            world_size=world_size,  # <--- trainer + all inference workers
        )
    )
)

# Initialization for training
from vllm.distributed.weight_transfer.nccl_engine import (
    NCCLWeightTransferEngine,
)

group = NCCLWeightTransferEngine.trainer_init(
    dict(
        master_address=master_address,
        master_port=master_port,
        world_size=world_size,
    )
)
```

**3. 从训练器发送权重**：在训练器上启动权重传输。`WeightTransferEngine` 实现了 `trainer_send_weights` 方法，接受可迭代的参数列表，并为全部或部分参数发起传输。用户也可以实现自己的发送功能。这里我们还可以利用打包张量广播，把多个小张量批量合并进更大的缓冲区，以获得更高吞吐的传输。

```
from vllm.distributed.weight_transfer.nccl_engine import (
    NCCLTrainerSendWeightsArgs,
    NCCLWeightTransferEngine,
)

trainer_args = NCCLTrainerSendWeightsArgs(
    group=group,
    packed=True,  # use packed broadcasting for efficiency
)

# send weights from an `AutoModelForCausalLM` instance
NCCLWeightTransferEngine.trainer_send_weights(
    iterator=model.named_parameters(),
    trainer_args=trainer_args,
)
```

**4. 在推理引擎中接收权重**

```
from vllm.distributed.weight_transfer.base import WeightTransferUpdateRequest

# executed asynchronously while trainer sends weights
llm.start_weight_update()
llm.update_weights(
    WeightTransferUpdateRequest(
        update_info=dict(
            names=names,
            dtype_names=dtype_names,
            shapes=shapes,
            packed=True,
        )
    )
)
llm.finish_weight_update()
```

### 自定义权重传输

权重传输 API 的主要目标之一，是让 RL 框架能够用 vLLM 实现自定义权重传输策略。有了新 API，用户可以实现并注册自定义的 `WeightTransferEngine`：

```
from dataclasses import dataclass
from typing import Iterator, Callable, Any
from torch import Tensor
from vllm.distributed.weight_transfer.base import (
    WeightTransferEngine,
    WeightTransferInitInfo,
    WeightTransferUpdateInfo,
)


# define custom dataclasses for initialization and update weights metadata
@dataclass
class MyInitInfo(WeightTransferInitInfo):
    """Custom initialization info."""
    ...


@dataclass
class MyUpdateInfo(WeightTransferUpdateInfo):
    """Custom update info."""
    ...


# custom weight transfer engine
class MyWeightTransferEngine(WeightTransferEngine):
    init_info_cls = MyInitInfo
    update_info_cls = MyUpdateInfo

    def init_transfer_engine(self, init_info: MyInitInfo):
        ...

    def receive_weights(
        self,
        update_info: MyUpdateInfo,
        load_weights: Callable[[list[tuple[str, Tensor]]], None],
    ):
        ...

    @classmethod
    def trainer_send_weights(
        cls,
        iterator: Iterator[tuple[str, Tensor]],
        trainer_args: dict[str, Any] | Any,
    ):
        ...

# finally, register the weight transfer engine
from vllm.distributed.weight_transfer import WeightTransferEngineFactory
WeightTransferEngineFactory.register_engine("my_weight_transfer", MyWeightTransferEngine)
```

注意，`trainer_send_weights` 方法是可选的。它封装了训练器上使用的发送逻辑，用户不必以这种方式组织自己的发送逻辑。

上面这个简单的 API 可以支持许多高级用例。作为原型，我们在[这里](https://github.com/hao-aaron/vllm/blob/89c951b3296578c60cbb82e05ca3d1734364ba8c/examples/rl/sharded_reloading/README.md)演示了如何实现 [Etha](https://github.com/cmriat/Etha) 风格的分片权重传输。

## 面向异步 RL 的改进暂停/恢复支持

在异步 RL 中，权重更新发生在推理请求仍在途之时。通常，异步 RL 中的权重同步涉及三个操作：暂停生成、传输更新后的权重，然后恢复生成。用户可以选择如何处理在途请求（例如中止所有运行中的请求，或从已生成的 token 处恢复生成），以及保留还是丢弃 KV 缓存。

![Figure 3: Asynchronous RL system diagram, inspired by AReaL. Training and generation overlap, with training utilizing 4 samples for each step. After a training step finishes, all the engines are paused, weights are updated, the KV cache is discarded, and then the engines are resumed. KV cache is recomputed on resumption and generation progresses as before.](https://vllm.ai/blog-assets/figures/2026-05-28-native-rl-apis/async_rl.svg)

图 3：异步 RL 系统示意图，灵感来自 AReaL。训练与生成相互重叠，训练每步使用 4 个样本。一个训练步完成后，所有引擎被暂停、权重被更新、KV 缓存被丢弃，随后引擎恢复运行。恢复时重新计算 KV 缓存，生成照常推进。

### 暂停/恢复的 keep 模式

为了在推理引擎运行期间安全地更新权重，vLLM 提供了 `pause_generation` 和 `resume_generation` 方法。相同的功能在 HTTP 服务器上以 `POST /pause` 和 `POST /resume` API 的形式提供。此前，`AsyncLLMEngine.pause_generation` 支持两种模式：

- 中止所有请求
- 等待请求完成

我们加入第三个选项：**keep 模式**。下表比较了各种模式：

| 模式 | 说明 | 对客户端的影响 | 能否用于异步 RL？ |
| --- | --- | --- | --- |
| `abort` | 中止所有进行中的请求 | 客户端必须处理重试 | 可以 |
| `wait` | 等待所有进行中的请求 | 客户端无需重试 | 不能，权重更新前生成必须完成 |
| `keep` | 暂停进行中的请求 | 客户端无需重试 | 可以 |

keep 模式的用法如下：

```
# pause - preserve ongoing requests
await engine.pause_generation(mode="keep")
# update weights here
# resume
await engine.resume_generation()
```

在 keep 模式下：

- 进行中的请求被暂停但不会被丢弃。
- 调度器停止运行，但状态得以保留。

### 修复 DPEP 场景中的死锁

大规模异步 RL 需要在 DPEP 部署中对在途权重更新进行细致协调。在 vLLM 中，`DPCoordinator` 确保生成在各个 vLLM rank 间被仔细协调，以防止死锁。更具体地说，只要任意 DP rank 中仍有活跃请求被调度，每个 DP rank 都会执行一次前向传播。

![Figure 4: DP-coordinated generation across vLLM ranks.](https://vllm.ai/blog-assets/figures/2026-05-28-native-rl-apis/dp_generate.svg)

图 4：跨 vLLM rank 的 DP 协调生成。

此前，在 vLLM 的 DP 部署中进行异步 RL 常常导致死锁，主要原因是一些引擎已收到暂停信号，而另一些引擎仍在活跃地处理请求并等待所有引擎加入。出现这种情况的一个原因是暂停状态在 `AsyncLLM` 对象中跟踪，而 DP 协调消息在 `EngineCore` 进程与 `DPCoordinator` 之间交换。举例来说，在 DP world size 为 2 时，可能出现如下死锁场景：

1. API 服务器 DP Rank 0 收到一个生成请求并转发给 `EngineCore`。API 服务器向 `DPCoordinator` 发出 `FIRST_REQ` 消息以开始新的一波（wave）。该请求被转发给 DP Rank 0 的 `EngineCore`，后者开始一个新的调度器步骤。
2. 控制器向两个引擎发出 `/pause` 请求。暂停状态被设置在 `AsyncLLM` 对象中，新请求不再转发给 `EngineCore`。所有 DP rank 上的 API 服务器随后立即返回。
3. 训练器发出权重更新请求。与此同时，DP Rank 0 的 `EngineCore` 已进入前向传播，正在等待其他 DP rank 加入。（为简单起见，这里忽略 `start_weight_update` 和 `finish_weight_update` 请求。）
4. 权重更新请求到达 DP Rank 1 的 `EngineCore`，该副本进入 NCCL 广播集合通信，等待其他 rank。权重更新请求在 DP Rank 0 的 `EngineCore` 上排队。
5. `DPCoordinator` 向 DP Rank 1 的 `EngineCore` 发送 `START_DP_WAVE` 消息，但该消息被排队。
6. 不同 rank 处于不同的集合通信中，形成死锁。

同一场景如下图所示：

![Figure 5: A deadlock scenario possible in DPEP deployments in vLLM.](https://vllm.ai/blog-assets/figures/2026-05-28-native-rl-apis/vllm_deadlock.svg)

图 5：vLLM DPEP 部署中可能出现的一种死锁场景。

我们通过两项改动来解决这一问题：

**1. 把暂停逻辑移入 `EngineCore`。** 暂停状态不再在 `AsyncLLM` 入口层跟踪，而是直接在调度器中处理。这减少了暂停与生成请求之间的竞态条件。

**2. 两阶段暂停/恢复。**

- **阶段 1（本地暂停）**：每个引擎暂停调度，但继续按步骤运行，响应任何进入的 `START_DP_WAVE` 请求，因此仍可参与所需的前向传播。
- **阶段 2（全局暂停）**：目前，所有 rank 每 32 步执行一次全局 all-reduce，检查任意 DP rank 中是否有待处理请求。在同一个 all-reduce 阶段，我们也检查所有引擎是否处于"本地暂停"状态。如果所有 rank 一致同意，它们就一起停止。

这确保了：

- 不会有 rank 陷入等待。
- 即使引擎收到暂停请求，`START_DP_WAVE` 仍会被遵守。
- 所有 worker 一致地完成状态转换。

于是，与之前相同的场景得到了优雅处理：

1. API 服务器 DP Rank 0 收到一个生成请求并转发给 `EngineCore`。API 服务器向 `DPCoordinator` 发出 `FIRST_REQ` 消息以开始新的一波。该请求被转发给 DP Rank 0 的 `EngineCore`，后者开始一个新的调度器步骤。
2. 控制器向两个引擎发出 `/pause` 请求。暂停请求被转发给两个 rank 的 `EngineCore`。暂停请求在 DP Rank 0 的 `EngineCore` 中排队，直到该步骤完成。注意此时 API 服务器尚未返回。
3. DP Rank 0 的 `EngineCore` 开始执行前向传播，worker 在 all-to-all 集合通信上等待。
4. DP Rank 1 的 `EngineCore` 收到暂停请求，进入"本地暂停"状态。
5. `DPCoordinator` 向 DP Rank 1 的 `EngineCore` 发送 `START_DP_WAVE` 消息。
6. DP Rank 1 的 `EngineCore` 开始执行前向传播。由于两个 DP rank 都已加入，前向传播完成。
7. DP Rank 0 的 `EngineCore` 处理暂停请求，进入"本地暂停"状态。
8. DP Rank 0 与 DP Rank 1 的 `EngineCore` 参与周期性 all-reduce，发现两个引擎都处于"本地暂停"状态，于是进入"全局暂停"状态。
9. API 服务器在 `/pause` 调用上返回。
10. 训练器发出权重更新请求。API 服务器把权重更新请求转发给 `EngineCore` 进程。（为简单起见，这里忽略 `start_weight_update` 和 `finish_weight_update` 请求。）
11. 所有 vLLM worker 进入 NCCL 广播集合通信。训练器启动 NCCL 广播。
12. 权重更新顺利完成。

![Figure 6: Deadlock-free pause/resume in DPEP deployments with the two-phase protocol.](https://vllm.ai/blog-assets/figures/2026-05-28-native-rl-apis/vllm_no_deadlock.svg)

图 6：采用两阶段协议后 DPEP 部署中无死锁的暂停/恢复。

## 验证

### 演示新的 RL API

我们在 [SkyRL](https://github.com/NovaSky-AI/SkyRL) 中演示新 RL API 的用法。

在 SkyRL 中，训练器通过 HTTP 与推理引擎交互。对于权重同步，SkyRL 使用原生权重同步 API，以及面向异步 RL 的原生 `/pause` 和 `/resume` API。与原生 RL API 的集成详见[文档](https://docs.skyrl.ai/docs/getting-started/inference_architecture)，我们演示了在原始 DAPO 配方上对 Qwen3-1.7B 的异步训练（[示例](https://github.com/NovaSky-AI/SkyRL/blob/dec7137d9c57db59458a677de09add0b24413f26/examples/train/algorithms/dapo/run_dapo_qwen3_1.7b_aime_fully_async_onestep.sh)）。

![Figure 7: Asynchronous training of Qwen3-1.7B on the DAPO recipe in SkyRL using the native RL APIs.](https://vllm.ai/blog-assets/figures/2026-05-28-native-rl-apis/skyrl_validation.svg)

图 7：在 SkyRL 中使用原生 RL API 在 DAPO 配方上对 Qwen3-1.7B 进行异步训练。

### 规模化验证：Wide-EP 环境下的完全异步 RL

Prime-RL 团队针对 `zai-org/GLM-5.1-FP8` 的部署验证了 RL API：推理以 P/D 分离方式运行在 16 个 8xH200 节点上——2 个 4P+4D 副本，预填充与解码均为 DPEP32。所有实例还配置了 CPU KV 缓存卸载，容量为每节点 1TB。跨引擎路由由 `vllm-router` 启用，它提供缓存感知的粘性路由。训练器在另外 16 个 8xH200 节点上运行等价的 BF16 模型（`zai-org/GLM-5.1`），在自定义数学环境中使用 [IcePop](https://arxiv.org/abs/2510.18855) 作为所选算法。该部署在训练中已稳定运行超过 100 步，评估性能持续增长，RL 曲线上升，KL 偏差稳定，权重更新正常推进。

![Figure 8: Prime-RL validation of fully async RL with zai-org/GLM-5.1-FP8 across 16 8xH200 nodes.](https://vllm.ai/blog-assets/figures/2026-05-28-native-rl-apis/prime_rl.svg)

图 8：Prime-RL 在 16 个 8xH200 节点上对 zai-org/GLM-5.1-FP8 进行的完全异步 RL 验证。

## 结论

我们观察到 vLLM RL 社区对基于新 RL API 进行构建的兴趣日益增长。vLLM RL 社区的一些进行中的工作包括集成新的 [K8s 原生权重传输引擎](https://github.com/vllm-project/vllm/pull/40828)，以及以通用方式支持[分片感知、RDMA 原生的权重传输](https://github.com/vllm-project/vllm/issues/40822)。新开发的进展在 [vLLM RL 路线图](https://github.com/vllm-project/vllm/issues/41733)中跟踪。

更多关于 vLLM 中 RL 工具的内容请阅读文档：

- [权重传输](https://docs.vllm.ai/en/latest/training/weight_transfer/)
- [异步 RL](https://docs.vllm.ai/en/latest/training/async_rl/)

在这里试用 vLLM 上的新 API：<https://github.com/vllm-project/vllm/tree/main/examples/rl>。

## 致谢

感谢以下使这一切成为可能的团队与个人：

- **Prime-RL** 团队（特别是 [Matej Sirovatka](https://github.com/S1ro1)）以及 [**Junjie Zhang**](https://github.com/junjzhang)，帮助我们通过大规模运行验证和调试 RL API。
- **NemoRL** 团队，提供了优化的打包张量实现。
- [Robert Shaw](https://github.com/robertgshaw2-redhat)，组织了 RL 相关工作。
- [Kyle Sayers](https://github.com/kylesayrs)，通过逐层重载让量化权重重载成为可能。
