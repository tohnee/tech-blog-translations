---
title: "用 vLLM 加速 RLHF：来自 OpenRLHF 的最佳实践"
title_en: "Accelerating RLHF with vLLM, Best Practice from OpenRLHF"
source: https://vllm.ai/blog/2025-04-23-openrlhf-vllm
crawled: 2026-09-12
translated: 2026-09-13
---

# 用 vLLM 加速 RLHF：来自 OpenRLHF 的最佳实践

> 原文：[Accelerating RLHF with vLLM, Best Practice from OpenRLHF](https://vllm.ai/blog/2025-04-23-openrlhf-vllm) · vLLM 博客

作者：OpenRLHF 团队

[#大规模服务](https://vllm.ai/blog/tags/large-scale-serving)

随着对具备推理能力的大语言模型（LLM）训练需求的增长，基于人类反馈的强化学习（RLHF）已成为一项基石性技术。然而，传统 RLHF 流水线——尤其是使用近端策略优化（PPO）的流水线——常常受制于巨大的计算开销。这一挑战在擅长复杂推理任务的模型（如 OpenAI-o1 和 DeepSeek-R1）上尤为突出：生成长思维链（CoT）输出可能占到总训练时间的 90%。这些模型必须生成跨越数千 token 的详细分步推理，使推理显著比训练阶段本身更加耗时。作为开创性的推理框架，vLLM 为生成 RLHF 样本和更新模型权重提供了用户友好的接口。

## OpenRLHF 的设计

为了在 RLHF 框架的性能与易用性之间取得平衡，[OpenRLHF](https://github.com/OpenRLHF/OpenRLHF) 被设计为一个高性能且对用户友好的解决方案，集成了 Ray、vLLM、零冗余优化器（ZeRO-3）和自动张量并行（AutoTP）等关键技术：

**[Ray](https://github.com/ray-project/ray)** 是 OpenRLHF 分布式架构的骨干。凭借强大的调度与编排功能，Ray 高效管理复杂的数据流与计算，包括将基于规则的奖励模型分布到多个节点。

**配合 Ray Executor 与 AutoTP 的 vLLM** 在加速推理中扮演核心角色。凭借内置的 Ray Executor 支持以及与 HuggingFace Transformers 的集成，它通过 AutoTP 实现高效的权重更新，从而带来高吞吐量且节省显存的 LLM 生成。

**配合 [HuggingFace Transformers](https://github.com/huggingface/transformers) 的 ZeRO-3** 是来自 [DeepSpeed](https://github.com/deepspeedai/DeepSpeed) 的内存优化方法，使 OpenRLHF 无需 Megatron 这类重量级框架即可训练大模型。与 HuggingFace 的无缝集成让预训练模型的加载与微调变得简单。

Ray、vLLM、ZeRO-3 和 HuggingFace Transformers 共同构成了一套前沿而精简的 RLHF 训练加速方案。该架构还影响了 [veRL](https://github.com/volcengine/verl) 等其他框架，后者采用了类似的范式来实现可扩展且高效的 RLHF 训练。OpenRLHF 也是首个基于 Ray、vLLM 和 ZeRO-3 开发的开源 RLHF 框架，已被 Google、字节跳动、阿里巴巴、美团、Berkeley Starling 团队等使用。

![Ray and vLLM in OpenRLHF](https://vllm.ai/blog-assets/figures/openrlhf-vllm/ray.png)

OpenRLHF 中的 Ray 与 vLLM

如上图所示，OpenRLHF 使用 [Ray 的 Placement Group API](https://docs.ray.io/en/latest/ray-core/scheduling/placement-group.html) 来灵活调度 RLHF 流水线的各个组件，包括 vLLM 引擎、Actor、Critic、Reference 和 Reward 模型。虽然这些组件是分开表示的，但它们可以被放置在共享的 Ray placement group 中，以最大化资源效率。例如，在混合引擎配置中，所有模块可以在同一个 GPU 组内运行；或者可以将特定组件——例如 Actor 和 Critic——组合在一起。所有模块由一个中央 Ray Actor 编排，它管理整个训练生命周期。Actor 与 vLLM 引擎之间的权重同步通过高性能通信方式处理，例如 NVIDIA 集合通信库（NCCL）或混合引擎设置中的 CUDA 进程间通信（IPC）内存传输。

## 使用 vLLM Ray Executor 实现 RLHF 加速

OpenRLHF 和 vLLM 提供了一套干净、高效的 API，用于简化 RLHF 流水线内部的交互。通过实现自定义的 `WorkerExtension` 类，用户可以处理训练组件与推理组件之间的权重同步。环境变量 `VLLM_RAY_PER_WORKER_GPUS` 和 `VLLM_RAY_BUNDLE_INDICES` 支持对每个 worker 的 GPU 资源进行细粒度分配，从而实现多个组件共享 GPU 组的混合引擎配置：

```
# rlhf_utils.py
class ColocateWorkerExtension:
    """
    Extension class for vLLM workers to handle weight synchronization.
    This class ensures compatibility with both vLLM V0 and V1.
    """
    def report_device_id(self) -> str:
        """Report the unique device ID for this worker"""
        from vllm.platforms import current_platform
        self.device_uuid = current_platform.get_device_uuid(self.device.index)
        return self.device_uuid

    def update_weights_from_ipc_handles(self, ipc_handles):
        """Update model weights using IPC handles"""
        handles = ipc_handles[self.device_uuid]
        device_id = self.device.index
        weights = []
        for name, handle in handles.items():
            func, args = handle
            list_args = list(args)
            list_args[6] = device_id  # Update device ID for current process
            tensor = func(*list_args)
            weights.append((name, tensor))
        self.model_runner.model.load_weights(weights=weights)
        torch.cuda.synchronize()

# main.py
class MyLLM(LLM):
    """
    Custom LLM class to handle GPU resource allocation and bundle indices.
    This ensures proper GPU utilization and placement group management.
    """
    def __init__(self, *args, bundle_indices: list, **kwargs):
        # Prevent Ray from manipulating CUDA_VISIBLE_DEVICES at the top level
        os.environ.pop("CUDA_VISIBLE_DEVICES", None)
        # Configure GPU utilization per worker
        os.environ["VLLM_RAY_PER_WORKER_GPUS"] = "0.4"
        os.environ["VLLM_RAY_BUNDLE_INDICES"] = ",".join(map(str, bundle_indices))
        super().__init__(*args, **kwargs)


# Create Ray's placement group for GPU allocation
pg = placement_group([{"GPU": 1, "CPU": 0}] * 4)
ray.get(pg.ready())

# Create inference engines
inference_engines = []
for bundle_indices in [[0, 1], [2, 3]]:
    llm = ray.remote(
        num_gpus=0,
        scheduling_strategy=PlacementGroupSchedulingStrategy(
            placement_group=pg
        )
    )(MyLLM).remote(
        model="facebook/opt-125m",
        tensor_parallel_size=2,
        distributed_executor_backend="ray",
        gpu_memory_utilization=0.4,
        worker_extension_cls="rlhf_utils.ColocateWorkerExtension",
        bundle_indices=bundle_indices
    )
    inference_engines.append(llm)
```

[完整的 RLHF 示例](https://docs.vllm.ai/en/latest/getting_started/examples/rlhf_colocate.html)演示了如何以指定的 GPU 数量初始化 Ray、创建 placement group 来管理资源，以及定义训练 actor 和推理引擎。训练 actor 负责模型初始化和权重更新，而推理引擎通过 vLLM 提供模型服务。权重同步通过 CUDA IPC 或 NCCL 执行，确保整个 RLHF 流水线的一致性与效率。

## 致谢

我们衷心感谢 vLLM 的贡献者，包括 [Kaichao You](https://github.com/youkaichao)、[Cody Yu](https://github.com/comaniac)、[Rui Qiao](https://github.com/ruisearch42) 以及许多其他人——没有他们的工作，OpenRLHF 与 vLLM 的集成将无从谈起。vLLM 团队的 [Kaichao You](https://github.com/youkaichao) 领导了 RLHF 集成工作。

OpenRLHF 项目是首个基于 Ray 和 vLLM 的开源 RLHF 框架。我们要感谢 [Jian Hu](https://github.com/hijkzzz)、[Songlin Jiang](https://github.com/HollowMan6)、[Zilin Zhu](https://github.com/zhuzilin)、[Xibin Wu](https://github.com/wuxibin89) 以及许多其他人对 OpenRLHF 项目的 Ray、vLLM Wrapper 和混合引擎组件做出的重要贡献。[Jian Hu](https://github.com/hijkzzz) 领导开发工作。
