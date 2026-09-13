---
title: "从 vLLM 中提取隐藏状态"
title_en: "Extracting hidden states from vLLM"
source: https://vllm.ai/blog/2026-03-30-extract-hidden-states
crawled: 2026-09-12
translated: 2026-09-13
---

# 从 vLLM 中提取隐藏状态

> 原文：[Extracting hidden states from vLLM](https://vllm.ai/blog/2026-03-30-extract-hidden-states) · vLLM 博客

作者：Fynn Schmitt-Ulms

[#投机解码](https://vllm.ai/blog/tags/speculative-decoding)

PR [#33736](https://github.com/vllm-project/vllm/pull/33736)（包含在 `vllm>=v0.18.0` 中）为 vLLM 引入了新的隐藏状态提取系统。这篇博文探讨这一功能的动机、设计、用法与未来方向，以及它在 vLLM 的 [Speculators](https://github.com/vllm-project/speculators/)（一个用于创建和训练投机解码模型的库）中的使用。

## 动机

隐藏状态是模型对 token 序列的内部中间表示。它们能揭示模型的内部状态，并在投机解码中被大量使用。

### 投机解码回顾

投机解码通常把一个"验证器"模型——也就是你想要服务的大 LLM——与一个小的"草稿"模型组合起来。草稿模型生成草稿 token，再由验证器模型并行验证。这可以显著加速解码（依方法不同，最高 2-5x），尤其是在模型性能受内存带宽限制的低批大小场景下。

研究人员发现，把验证器模型的内部隐藏状态提供给草稿模型，可以改善起草的对齐与整体质量。因此出现了 [Eagle-3](https://arxiv.org/abs/2503.01840)、[P-Eagle](https://arxiv.org/abs/2602.01469)、[DFlash](https://arxiv.org/abs/2602.06036) 等方法，它们需要来自验证器多个层的隐藏状态作为输入。

由于草稿模型以隐藏状态为输入，训练它们需要访问包含大量隐藏状态与验证器输出的数据集。大多数投机解码库（如 Speculators）用以下两种方式之一来解决：

1. 用 `transformers` 生成隐藏状态。这可行，但有两个重大缺点：(A) vLLM 的所有性能优化（如大模型/分布式支持等）都会丢失。(B) 它引入了一整类由 transformers 与 vLLM 隐藏状态之间的细微不一致导致的潜在 bug。
2. 大幅修改与补丁 vLLM。这通常需要手动搭建 vLLM 核心组件并直接调用内部 API。随着 vLLM 内部实现随时间更新，这会造成沉重的维护负担。这也意味着许多 vLLM 功能（如前缀缓存、自动批处理、异步服务器等）必须被禁用。此前版本的 Speculators（`<0.5.0`）就是这样处理隐藏状态生成的。

两种方式各有缺点，而随着投机解码日益流行，需要更好、更高性能的解决方案。

## 设计考量

在把隐藏状态提取直接集成进 vLLM 时，我们考虑了许多需求。

首先，系统应以高性能的方式返回隐藏状态。模型的隐藏状态可能非常大。对于 `hidden_size` 为 4096 的 `Qwen3-8B model`，提取的隐藏状态形状为 `[seq_len, num_layers_to_extract, 4096]`。对一个 8k token 的序列、4 层、FP16 而言，这相当于 268 MB 的数据。因此，把隐藏状态序列化后直接放进请求的响应体返回并不现实。

而隐藏状态占用如此多的空间，哪怕只是临时存放在显存中也非小事。必须预分配内存，并同时为所有并发请求做好管理，包括处理分块预填充、请求抢占等，以避免 OOM 错误。

由于这一功能只在用户需要从 vLLM 获取隐藏状态时才起作用——而大多数部署场景并非如此——关键是它不能给 vLLM 的"热路径"引入任何新开销（运行时或认知上的）。在实践中，这意味着限制改动范围，并尽可能复用现有功能。

最后，最终用户使用、存储或传输隐藏状态的方式多种多样。例如，在"离线"投机器（speculator）训练中，隐藏状态会针对整个数据集提前生成并缓存到磁盘，然后才开始训练。而"在线"训练则在训练过程中即时生成隐藏状态，需要把它们高效地传输到各个训练进程，最好不需要先写盘。为支持这些不同场景，隐藏状态提取系统必须灵活/可扩展。

## 设计洞见

基于上述需求，以下几个设计洞见促成了隐藏状态提取系统的实现。这些洞见总结如下。

1. vLLM 支持用 Eagle-3（及类似）投机解码模型运行推理，这些模型以验证器模型的隐藏状态作为输入。因此，把隐藏状态从验证器模型传送到草稿模型的管道已经存在。
2. vLLM 有一个可扩展的 [KV Connector API](https://docs.vllm.ai/en/stable/api/vllm/distributed/kv_transfer/kv_connector/v1/)，用于高效地从 vLLM 的 KV 缓存中提取数据，Prefill/Decode 分离等功能都用到了它。该 API 的现有实现支持通过 Nixl 传输 KV 缓存数据、写入磁盘、存入共享内存等。该 API 还被设计为支持 KV 缓存状态的异步传输，并确保 KV 缓存块在传输完成前不会被释放。
3. 隐藏状态到其 token 序列输入的映射方式与 KV 缓存数据相同。换句话说，每个 token 都有一个隐藏状态值，且该值只有在其前面的前缀序列上下文中才有效。
4. vLLM 支持为投机草稿模型单独配置 KV 缓存配置/大小。

把这些想法结合起来（图 1），我们可以这样提取隐藏状态：

1. 创建一个虚拟草稿模型，利用现有的 Eagle-3 模型管道从 vLLM 接收验证器隐藏状态。
2. 这个虚拟模型有一个带自己 KV 缓存的虚拟注意力层。它不执行注意力计算，而是直接把隐藏状态输入插入自己的 KV 缓存。
3. 然后由一个自定义 KV Connector 把虚拟草稿模型的 KV 缓存数据（其中现在存放着我们的隐藏状态）保存到磁盘，或以其他方式传输。

这满足所有设计要求：利用现有的 Eagle-3 路径把隐藏状态输送到草稿模型，同时提供了一种高性能的隐藏状态提取方法，并通过 KV Connector API 灵活应对不同的下游用途。由于草稿模型把隐藏状态存放在虚拟注意力层中，vLLM 知道要为它们分配显存。vLLM 还使用与 KV 缓存相同的分页内存系统来管理隐藏状态，这使前缀缓存、分块预填充、高效批处理等成为可能。

![图 1：隐藏状态提取系统设计图。](https://vllm.ai/blog-assets/figures/2026-03-30-extract-hidden-states/design_diagram.png)

图 1：隐藏状态提取系统设计图。

## 用法与限制

[examples/offline\_inference/extract\_hidden\_states.py](https://github.com/vllm-project/vllm/blob/main/examples/offline_inference/extract_hidden_states.py) 展示了如何用 Python API 提取隐藏状态。该系统也可配合 vLLM 服务器使用，可以用下面的命令启动。

```
vllm serve Qwen/Qwen3-8B --speculative_config '{
	"method": "extract_hidden_states",
	"num_speculative_tokens": 1,
	"draft_model_config": {
		"hf_config": {
			"eagle_aux_hidden_state_layer_ids": [3, 18, 33, 36]
		}
	}
}' --kv_transfer_config '{
	"kv_connector": "ExampleHiddenStatesConnector",
	"kv_role": "kv_producer",
	"kv_connector_extra_config": {
		"shared_storage_path": "/tmp/hidden_states"
	}
}'

```

这条命令设置了系统的两个主要组件。`--speculative_config` 指示 vLLM 使用伪造的"extract\_hidden\_states"投机方法，它会搭建虚拟草稿模型，同时支持指定从哪些层提取隐藏状态。第二个组件是 `--kv_transfer_config`，它设置自定义 KV Connector，专门用于从草稿模型的各层提取隐藏状态。截至撰写时，只有"ExampleHiddenStatesConnector"（一个写磁盘的简单实现）存在，但性能更好的连接器很快会加入。请注意，这两个组件必须一起使用，系统才能按预期工作。

vLLM 运行后，发往服务器的任何请求都会返回一个"kv\_transfer\_params"字典，其中包含"hidden\_states\_path"。该路径指向一个已保存的 safetensors 文件，内含隐藏状态与 token id。保存目录可以通过上面配置中的"shared\_storage\_path"字段指定。

```
# `/tmp/hidden_states/{req_id}.safetensors`
{
	"token_ids": [prompt_seq_len],
	"hidden_states": [prompt_seq_len, num_hidden_layers, hidden_size]
}

```

注意事项：

- 它可以与 `--tensor-parallel-size` 和 `--data-parallel-size` 参数配合，用于单节点多 GPU 部署。
- 只会保存提示 token 及其隐藏状态。因此我们建议调用 `v1/completions` 端点时带上 `max_tokens=1` 采样参数。

## 进行中的工作

- **集成进 vLLM 的 [speculators](https://github.com/vllm-project/speculators) 项目**：speculators 库专为高效训练投机解码算法而设计。最近合并的 [speculators PR #353](https://github.com/vllm-project/speculators/pull/353) 已更新 speculators，使其使用新的 vLLM 原生隐藏状态提取系统，并启用了草稿模型的在线训练。该功能将包含在 `speculators v0.5.0` 中。
- **性能改进**：隐藏状态专用 KV Connector（"ExampleHiddenStatesConnector"）的初始实现尚未优化，包含阻塞式的隐藏状态写入。目前正积极推动在该连接器中启用异步写入。
- **设备到设备连接器**：ExampleHiddenStatesConnector 把隐藏状态直接写到磁盘，再由训练进程使用。这种方式简单，也是不错的测试实现，但难以扩展到更大的训练负载。未来的工作包括开发更先进的隐藏状态连接器，把隐藏状态直接从一个设备传输到另一个设备，包括多节点环境。
