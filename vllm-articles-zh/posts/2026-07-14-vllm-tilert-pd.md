---
title: "vLLM x TileRT：面向延迟关键型服务的专用解码"
title_en: "vLLM x TileRT: Specialized Decode for Latency-Critical Serving"
source: https://vllm.ai/blog/2026-07-14-vllm-tilert-pd
crawled: 2026-09-12
translated: 2026-09-13
---

# vLLM x TileRT：面向延迟关键型服务的专用解码

> 原文：[vLLM x TileRT: Specialized Decode for Latency-Critical Serving](https://vllm.ai/blog/2026-07-14-vllm-tilert-pd) · vLLM 博客

作者：TileRT 团队

[#分离部署](https://vllm.ai/blog/tags/disaggregation)[#性能](https://vllm.ai/blog/tags/performance)[#生态](https://vllm.ai/blog/tags/ecosystem)

分离式服务将受计算限制的预填充阶段与受内存带宽限制的解码阶段分离开来，已成为大规模服务大语言模型日益标准化的模式，而 vLLM 通过一流的连接器接口对此提供支持。

这一架构转变带来一个容易被忽视的好处：一旦预填充与解码分离，**解码侧就变成了可插拔的**。不同的服务场景适合不同的引擎设计。预填充池、调度器、缓存层和服务 API 都原封不动地留在原地，而解码池则成为一个可以审慎选择的对象。

今天，我们正是要引入这样一种选择：**vLLM 预填充搭配 TileRT 解码**，通过 vLLM V1 的公开连接器接口集成，并随 TileRT 0.1.5 一同发布。对于延迟关键型工作负载，这一组合带来 **TileRT 原生的单用户解码速度**，而部署的其他一切仍保持原生 vLLM。

## 为什么需要第二种解码选择？

vLLM 的原生解码过去是、现在仍然是正确的默认选择：它是为覆盖海量模型与硬件的高吞吐量批量服务而构建的。但如今有一类不断增长的工作负载——例如智能体循环、交互式编程助手、实时语音——其中真正重要的指标不是总吞吐量，而是 token 到达每个用户手中的速度。这些工作负载受延迟约束，需要一个从零开始、专为这种场景设计的解码引擎。原生解码与 TileRT 针对的是同一条吞吐量-延迟边界上的不同点，这正是二者能够协同组合的原因。

TileRT 正是这样一个引擎：一个全新的推理运行时，其唯一的构建目标就是把单用户解码速度推向硬件的极限。我们曾在别处撰文阐述为什么我们相信[速度正在成为独立的扩展维度](https://www.tilert.ai/blog/speed-as-the-next-scaling-law.html)。

不过，本文要讲的并不是引擎本身，而是一个更现实的问题：能否在采用一个专用解码引擎的同时，**不放弃你所依赖的生态**——例如 OpenAI 兼容 API、调度、前缀缓存、工具调用，以及 vLLM 的运维成熟度？

这次集成的设计目标就是把这种取舍降到最小：

- **预填充仍是 vLLM。** 调度、分块预填充、前缀缓存——原封不动。
- **服务接口仍是 vLLM。** 相同的 API、相同的请求格式、相同的工具链。
- **只有解码改变，而且只对你发往那里的流量生效。** 与 TileRT 配对的栈与现有 vLLM 部署并行运行；每个工作负载自行选择端点。

## 架构：设计层面的共存

核心设计原则是**对 vLLM 零改动**：不 fork、不打补丁、不包装内部 worker。整个集成完全存在于 vLLM V1 的公开扩展面之后：一个 `KVConnectorBase_V1` 实现，组合在 `MultiConnector` 之下，并通过标准的 `kv_connector_module_path` 机制加载。这不仅仅是工程美感的问题：添加一个 TileRT 解码池不会破坏你已在运行的 vLLM 部署的稳定性，升级 vLLM 也不意味着要重新移植一个 fork。

![设计层面的共存：延迟关键型流量由 TileRT PD 路由器打标，并由 TileRT 连接器认领；常规流量则走原生分离部署路径——两者都由一个组合在 MultiConnector 之下的原生 vLLM 预填充池提供服务。](https://vllm.ai/blog-assets/figures/2026-07-14-vllm-tilert-pd/pd_arch.png)

设计层面的共存：延迟关键型流量由 TileRT PD 路由器打标，并由 TileRT 连接器认领；常规流量则走原生分离部署路径——两者都由一个组合在 MultiConnector 之下的原生 vLLM 预填充池提供服务。

**路由。** 一个轻量级路由器位于 TileRT 池前端。对每个请求，它设置 `max_tokens=1`（由 vLLM 执行预填充并产出第一个 token），并在标准的透传字段中附加目标解码节点：`kv_transfer_params = {"tilert_host": ..., "tilert_ctrl_port": ...}`。发往原生池的流量照常通过原有的分离部署代理，不做任何修改。

**认领过滤。** TileRT 连接器只认领带有标记的请求，对其他一切请求严格保持无操作（no-op），因此两个解码池可以共享同一个预填充实例（甚至是同一个前向批次）：为部分流量采用 TileRT 不会对其余流量产生任何影响。

**纯粹的生产者。** 该连接器仅充当 `kv_producer`，从不触及调度或采样；它只在预填充完成后提取并传输状态。在其他所有方面，预填充实例就是一台原生 vLLM 服务器。

## 交接是如何工作的

要让跨引擎分离部署切实可用，必须满足三件事：传输必须快，不能拖慢预填充节点，而且解码引擎必须精确地从预填充中断的地方接续。

**数据平面。** 预填充完成后，请求的注意力状态（压缩后的 KV、稀疏注意力索引缓存以及少量元数据）以 RDMA 单边写入的方式传输到解码节点，直接写入预先注册的 GPU 缓冲区，传输引擎可用 Mooncake 或 NIXL。没有中间序列化，也不经过主机内存中转。交接协议本身与底层传输引擎无关，后者的职责只是搬运字节。

**与预填充完全重叠。** 状态提取发生在前向计算窗口之内：请求的状态在其缓存块被回收之前复制到一个中转缓冲区，实际的网络传输由后台发送器完成。发往 TileRT 的请求永远不会阻塞下一次预填充迭代，包括与同一批次中发往原生池的请求一起时也是如此。

**注入运行中的引擎。** 状态到达后会被转换为 TileRT 的原生布局，并直接注入正在运行的引擎；解码立即开始，从第一步起就启用了多 token 投机解码。

## 性能评估

![在 8× NVIDIA B200 上使用 TileRT v0.1.5 测得的 GLM-5.1-FP8 token 生成速度。输出长度 1K，输入长度 1K–192K。柱状图比较了不使用 MTP 的 TileRT、使用 MTP（平均接受长度 3.2）的 TileRT，以及最佳 MTP 接受长度 4.0 下的峰值。](https://vllm.ai/blog-assets/figures/2026-07-14-vllm-tilert-pd/glm5_tilert_mtp.png)

在 8× NVIDIA B200 上使用 TileRT v0.1.5 测得的 GLM-5.1-FP8 token 生成速度。输出长度 1K，输入长度 1K–192K。柱状图比较了不使用 MTP 的 TileRT、使用 MTP（平均接受长度 3.2）的 TileRT，以及最佳 MTP 接受长度 4.0 下的峰值。

## 如何选择你的解码池

当单用户 token 速度是约束瓶颈（例如交互式智能体、实时助手、有延迟 SLO 要求的推理），且模型属于 TileRT 支持的范围时，路由到 **TileRT 解码**。

若追求最大总吞吐量、高并发批处理，以及通用解码所覆盖的长尾模型与功能，则继续使用**原生 vLLM 解码**。

两种栈暴露相同的 OpenAI 兼容接口，因此在二者之间迁移工作负载只需改动路由，无需改动客户端。

**当前限制。** 在本版本中，一个 TileRT 解码节点每次只服务一个进行中的请求，由路由器提供门控分发和背压。本版本的模型覆盖为 GLM-5/5.1 和 DeepSeek-V3.2，更多支持即将到来。

## 快速上手

TileRT 0.1.5 已发布在 [PyPI](https://pypi.org/project/tilert/)（`pip install tilert`；提供 Python 3.12、CUDA 13 的 wheel 包）和 [TileRT 仓库](https://github.com/tile-ai/TileRT)。请同时在预填充节点和解码节点上安装；预填充侧需要用它来加载连接器插件。

```
# 0. One-time: convert the HF checkpoint to TileRT's weight format
python -m tilert.models.preprocess.weight_converter \
    --model_type glm-5 \
    --model_dir /path/to/GLM-5.1 \
    --save_dir /path/to/tilert-glm5.1-weights

# 1. TileRT decode node
python -m tilert.pd_vllm.decode_server \
    --engine tilert --model glm5 \
    --model-weights-dir /path/to/tilert-glm5.1-weights \
    --with-mtp --max-seq-len 202752 \
    --kv-cache-dtype fp8 \
    --ctrl-port 5556 --http-port 5557

# 2. vLLM prefill (stock vLLM; the connector loads as a plugin).
#    The MTP speculative config is required: prefill populates the
#    draft-layer KV that decode-side speculation resumes from.
vllm serve /path/to/GLM-5.1 \
    --served-model-name glm5.1 \
    --port 8000 \
    --tensor-parallel-size 8 \
    --enforce-eager \
    --trust-remote-code \
    --return-tokens-as-token-ids \
    --gpu-memory-utilization 0.8 \
    --kv-cache-dtype fp8_ds_mla \
    --speculative-config '{"method": "mtp", "num_speculative_tokens": 1}' \
    --kv-transfer-config '{
        "kv_connector": "TileRTConnector",
        "kv_connector_module_path": "tilert.pd_vllm.prefill_connector",
        "kv_role": "kv_producer",
        "kv_connector_extra_config":{
            "tilert_host":"[TILERT_DECODE_SERVER_IP]",
            "tilert_ctrl_port":5556,
            "tilert_model":"glm5",
            "tilert_max_seq_len":202752
        }
    }'

# 3. Router: OpenAI-compatible ingress for the TileRT pool
python -m tilert.pd_vllm.pd_router \
    --vllm-url http://prefill-node:8000 \
    --decode decode-node:5556:5557 \
    --model-path /path/to/GLM-5.1 \
    --port 23333
```

要让 TileRT 池与原生 vLLM 解码池共享同一个预填充实例，需要把两个连接器都组合在 `MultiConnector` 之下。我们验证过的配置端到端使用 NIXL（原生池用 vLLM 标准的 `NixlConnector`，TileRT 池用 NIXL 模式的 TileRT 连接器），因此共享的预填充只使用一个传输库；只需修改预填充侧的 `--kv-transfer-config`。

## 展望未来

我们认为，分离部署正在悄然改变推理栈的含义：它不再是一个单一引擎，而更像共享服务层背后多个专用引擎的组合。vLLM 的连接器接口正是让这种组合在今天成为可能的关键，本次集成就是一个具体例子。这也是 TileRT 这样的引擎敢于如此深度专精的原因：只要服务层是共享的、接口是开放的，在一个维度上做深就不再意味着重造其他一切。

我们非常期待社区的反馈：关于集成接口、关于哪些工作负载能从中受益，以及接下来应该支持哪些模型。

## 致谢

我们感谢 vLLM 社区设计了 V1 连接器接口，让零改动的集成成为可能；感谢 Mooncake 和 NIXL 项目提供 RDMA 传输引擎。同时感谢 [Inferact Inc.](https://inferact.ai/) 在改进 vLLM-TileRT 集成方面的合作。
