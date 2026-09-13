---
title: "深入了解 Speculators v0.3.0 为 vLLM 带来的投机解码训练支持"
title_en: "Diving into speculative decoding training support for vLLM with Speculators v0.3.0"
source: https://vllm.ai/blog/2025-12-13-speculators-v030
crawled: 2026-09-12
translated: 2026-09-13
---

# 深入了解 Speculators v0.3.0 为 vLLM 带来的投机解码训练支持

> 原文：[Diving into speculative decoding training support for vLLM with Speculators v0.3.0](https://vllm.ai/blog/2025-12-13-speculators-v030) · vLLM 博客

作者：Fynn Schmitt-Ulms、Helen Zhao、Rahul Tuli 和 Dipika Sikka（Red Hat AI 模型优化团队）

[#投机解码](https://vllm.ai/blog/tags/speculative-decoding)[#生态](https://vllm.ai/blog/tags/ecosystem)

## 核心要点

- 投机解码是一种用于提升推理性能的优化手段；然而，为每个 LLM 训练一个专属的草稿模型既困难又耗时，而面向 vLLM 生成模型的、可用于生产的训练工具又十分稀缺
- [Speculators v0.3.0](https://github.com/vllm-project/speculators/releases/tag/v0.3.0) 为 Eagle3 草稿模型提供端到端训练支持，这些模型可与 vLLM 无缝配合运行
- 训练支持包括使用 vLLM 进行离线数据生成，以及针对单层与多层草稿模型的训练能力，同时适用于 MoE 与非 MoE 验证器

## 规模化推理

在过去十年间，LLM 的规模与能力迅速扩张，对推理性能的要求也随之水涨船高。由于 LLM 按顺序生成 token——每生成一个 token 都需要对数十亿参数做一次完整的前向传播——生成成本会快速攀升。随着模型规模不断增大，这种顺序计算成为显著瓶颈，使得如今的 LLM 能力惊人却常常速度缓慢。

投机解码是缓解这一挑战的一项颇有前景的优化：它允许较小的草稿模型提出候选 token，再由更大的模型快速验证，从而加速生成。

本文将把投机解码作为一种优化技术加以探讨，介绍 [Speculators](https://github.com/vllm-project/speculators) 库，并深入剖析它及其近期发布的 [v0.3.0 版本](https://github.com/vllm-project/speculators/releases/tag/v0.3.0)。Speculators 为研究人员、工程师和机器学习从业者提供了端到端生成投机解码模型的工具，并可与 vLLM 无缝集成。

## 什么是投机解码？

投机解码允许 LLM 在一次前向传播中生成多个 token。它的工作方式是将一个小型「草稿」模型与完整尺寸的「验证器」模型（即你想要服务的原始 LLM）结合使用。草稿模型运行成本低、速度快（通常只是一个 transformer 块），承担主要工作并自回归地预测若干 token。验证器模型则并行处理这些 token：对每个 token，验证器判断自己是否认同草稿的预测。如果验证器否决了某个 token，序列的其余部分将被丢弃；否则这些 token 就会纳入验证器模型的响应。

这种做法的优势在于：

1. 最终响应与单独使用验证器模型时来自同一分布，这确保了使用投机解码不会造成模型性能的退化。
2. 验证器模型能够并行生成多个 token。
3. 由于草稿模型很小，其运行开销通常微乎其微

综合起来，这可以将模型延迟降低 1.5-3x，从而显著加快生成速度。

## 在 vLLM 中使用投机解码模型

有了 vLLM 和 Speculators，运行投机解码模型就像用 vllm serve 部署其他模型一样简单。具体而言，投机解码在低吞吐场景下表现最佳——此时 GPU 尚未饱和，能够利用验证器模型的并行 token 生成能力。此外，草稿模型必须与验证器模型紧密对齐，这正是我们要为每个验证器专门训练草稿模型的原因。然而，为特定 LLM 训练草稿模型可能既困难又耗时。幸运的是，Speculators 库简化了这一训练过程，让用户能够产出与 vLLM 无缝集成的草稿模型。

## 创建新的草稿模型

当前投机解码算法的最先进水平（SOTA）是 Eagle3（[(Zhang et al., 2025)](https://arxiv.org/abs/2503.01840)）。

Eagle3 草稿模型以验证器模型三个层的隐藏状态作为输入，捕捉验证器的潜在特征。这些隐藏状态与 token id 一起送入较小的草稿模型，由其自回归地生成草稿 token。

这意味着训练 Eagle3 草稿模型需要一份包含以下组成部分的样本序列数据集：

1. 验证器模型的隐藏状态（来自三个中间层）
2. token id
3. 损失掩码（用于只在模型响应上训练，忽略用户提示）
4. 验证器模型的输出概率（草稿模型的训练目标）

### 数据生成

直接从 vLLM 中提取这些值并非易事。幸运的是，Speculators v0.3.0 通过一个隐藏状态生成器支持离线训练数据生成，它可以从标准 LLM 文本数据集中产出隐藏状态张量。这些隐藏状态张量随后被保存到磁盘，供后续训练过程使用。

数据生成主要有三个环节：预处理、隐藏状态生成和保存。

![data_generation_overview](https://vllm.ai/blog-assets/figures/2025-12-13-speculators-v030/data_generation.png)

数据生成概览

预处理接收一个原始数据集，

1. 重新格式化并规范化对话轮次
2. 应用模型的聊天模板
3. 对对话进行分词
4. 基于助手响应片段计算损失掩码
5. 将其连同 token ID 一起保存到磁盘
6. 收集 token 频率统计信息并保存到磁盘以备后用

损失掩码确保训练只关注机器生成的 token。对于通常只在最后一条响应中插入思考 token 的推理模型，Speculators 提供了一个额外的开关，可以随机丢弃对话轮次，确保模型在各种对话长度上得到训练。

隐藏状态生成器通过一个自定义 worker 扩展利用了 vLLM 的插件系统。它对模型的前向传播打补丁，以便在预填充阶段拦截并捕获中间隐藏状态。该生成器使用 vLLM 的多进程执行器进行高效的批量推理，并支持对更大模型使用张量并行。下图展示了这一过程。

![hidden_state_generator](https://vllm.ai/blog-assets/figures/2025-12-13-speculators-v030/hidden_state_generator.png)

隐藏状态生成器

在保存阶段，每个处理后的样本都会作为单独的 .pt 文件保存到磁盘，其中包含：

- `input_ids`：分词后的输入序列
- `hidden_states`：按捕获层逐一记录的张量列表
- `loss_mask`：指示可训练 token 的二值掩码

生成器使用 ThreadPoolExecutor 实现异步 I/O，在隐藏状态生成继续进行的同时并行执行磁盘写入，从而最大化吞吐量。

除数据文件外，还有两个额外文件会保存到磁盘：

- `data_config.json`，包含关于数据生成的元数据
- `token_freq.pt`，包含关于 token 频率的信息

存储在 token\_freq.pt 中的频率数据用于构建额外的目标到草稿（t2d）与草稿到目标（d2t）文件。这些文件充当验证器完整词表与草稿模型较小词表之间的映射。这种缩减后的「草稿」词表只保留出现频率最高的 token，从而提升草稿模型的效率。

以下脚本可用于启用离线数据生成：

- [`data_generation_offline.py`](https://github.com/vllm-project/speculators/blob/main/scripts/data_generation_offline.py)：预处理数据、保存 token 频率分布并生成隐藏状态
- [`build_vocab_mapping.py`](https://github.com/vllm-project/speculators/blob/main/scripts/build_vocab_mapping.py)：构建 t2d 与 d2t 张量

### 训练

Speculators v0.3.0 支持训练 Eagle3 草稿模型。训练以前述步骤生成的样本和词表映射文件以及模型配置信息作为输入，并初始化一个新的 Eagle3DraftModel 实例。随后，该模型使用 Eagle3 作者提出的一种名为「训练时测试」（train-time-testing）的技术进行训练。训练时测试在训练期间模拟多步草稿采样过程，确保模型学会预测的不只是第一个 token，还包括后续 token。

![flex_attention](https://vllm.ai/blog-assets/figures/2025-12-13-speculators-v030/flex_attention.png)

FlexAttention

图示来自 Eagle3（[(Zhang et al., 2025)](https://arxiv.org/abs/2503.01840)）论文。

上图展示了训练时测试的过程以及每一步的注意力掩码。对每个前缀，草稿模型生成下一个 token（蓝色）。接着，针对每个前缀加第一步生成结果，模型再生成第二个 token（黄色），依此类推。

训练时测试之所以难以实现，是因为其注意力掩码非常稀疏，而常见的注意力实现很难以高效利用计算与内存的方式处理它。这正是 Speculators 采用 FlexAttention（[(He et al., 2024)](https://arxiv.org/abs/2412.05496)）进行注意力计算的原因。FlexAttention 将注意力掩码切分为块，只在非空区域计算注意力。结合 `torch.compile`，它在加速计算的同时大幅降低了反向传播所需的激活值显存。

对任何训练实现来说，另一个重要特性是批处理。LLM 训练样本的批处理会因序列长度通常各不相同而变得更加复杂。解决这个问题有两种方法：第一种是通过截断与填充的组合使序列等长。这对长度均匀的数据集效果良好，但在需要大量填充的数据集上会浪费算力。Speculators v0.3.0 采用的是第二种方法：沿「序列」维度拼接序列，然后配置注意力掩码将它们视为各自独立的序列。这种做法与 FlexAttention 实现配合良好，性能也更好，尤其是再结合一种智能批采样算法——它能高效地将样本打包进接近最大序列长度的批次。

这些组件共同使 Speculators 的 Eagle3 模型训练既快速又节省内存，而且全部可以通过单个 [train.py](https://github.com/vllm-project/speculators/blob/main/scripts/train.py) 脚本完成。

## 在 vLLM 中运行 Speculators 模型

训练完成后，该库会生成一个完整的模型工件，其中扩展的 config.json 文件包含 `speculators_config`。之后只需一条简单的 vllm serve 命令，即可在 vLLM 中无缝运行这些模型：

```
vllm serve RedHatAI/Llama-3.1-8B-Instruct-speculator.eagle3
```

运行该命令时，vLLM 会读取存储在 `speculators_config` 中的投机解码设置（例如验证器模型的名称）。这些信息用于将草稿模型和验证器模型加载到同一个服务器中并配置投机解码。`speculators_config` 提供了一种标准化的配置格式，使模型成为自包含的整体、知道自己应该如何运行，同时让投机解码模型的部署变得与运行任何其他 LLM 一样简单。关于 `speculators_config` 的更多细节，请[参见下文示例](#speculators_config)。

简化的一条命令部署非常适合入门，而当你需要更多控制时，vLLM 也提供了完整形式的语法。它在以下场景很有用：

- 使用与配置中不同的验证器模型
- 调整投机解码参数，例如投机 token 的数量

完整形式的命令会部署基础（验证器）模型，并通过 `--speculative-config` 标志指定 speculator。
这种灵活性对实验和优化至关重要。例如，你可能想换用量化版本的验证器来进一步提升性能：

```
vllm serve RedHatAI/Qwen3-8B-FP8-dynamic \
  --tensor-parallel-size 1 \
  --gpu-memory-utilization 0.9 \
  --speculative-config '{"model": "RedHatAI/Qwen3-8B-speculator.eagle3", "num_speculative_tokens": 5, "method": "eagle3"}'
```

在这个例子中，我们使用 FP8 量化的 Qwen3-8B 作为验证器（而非 `speculators_config` 中引用的默认 BF16 版本），并将投机 token 数量从默认的 3 增加到 5，以争取更高的吞吐量。

## vLLM 集成：可用于生产的投机解码

Speculators 与 vLLM 的紧密集成，使投机解码从一项研究技术转变为可用于生产的特性。vLLM 对 Eagle3 的支持让各种模型架构与配置都能无缝部署：

**vLLM 服务与 Speculators 训练**：

- Llama（3.1、3.2、3.3）：8B 至 70B 参数
- Qwen3：8B、14B、32B 参数
- Qwen3 MoE：235B-A22B 参数（混合专家）
- GPT-OSS：20B、120B 参数

**仅 vLLM 服务**：

- 多模态：Llama 4 视觉语言模型

## 接下来做什么？

Speculators 接下来将专注于以下功能：

- 在线数据生成（在训练的同时生成隐藏状态，无需中间落盘缓存）
- 对视觉语言模型的数据生成支持
- 重新生成验证器响应（用验证器生成的响应替换数据集中的「助手」响应，获得对齐更好的训练数据）

## 参与进来！

想进一步了解投机解码？欢迎查看 [Speculators 仓库](https://github.com/vllm-project/speculators)，并通过认领 [Good First Issues](https://github.com/vllm-project/speculators/issues) 帮助这个仓库成长！

更多资源、文档和 Slack 频道请见：

- **Speculators 文档**：<https://docs.vllm.ai/projects/speculators/en/latest/>
- **vLLM Slack 频道**：`#speculators`、`#feat-spec-decode`
- **数据生成与训练脚本**：<https://github.com/vllm-project/speculators/blob/main/scripts/README.md>
- **端到端示例**：<https://github.com/vllm-project/Speculators/tree/main/examples/data_generation_and_training>
- 已训练完成的 Speculators 模型列表请查看 [Red Hat AI Hub](https://huggingface.co/collections/RedHatAI/speculator-models)

## 附录

### Eagle3 算法

![Eagle3 Algorithm](https://vllm.ai/blog-assets/figures/2025-12-13-speculators-v030/EAGLE3.png)

Eagle3 算法

### `speculators_config`：

```
{
  "architectures": ["Eagle3Speculator"],
  "auto_map": {"": "eagle3.Eagle3SpeculatorConfig"},
  "Speculators_model_type": "eagle3",
  "Speculators_version": "0.3.0",

  "draft_vocab_size": 10000,
  "transformer_layer_config": {
    "num_hidden_layers": 1,
    "hidden_size": 4096,
    ...
  },

  "Speculators_config": {
    "algorithm": "eagle3",
    "proposal_methods": [{
      "proposal_type": "greedy",
      "speculative_tokens": 3,
      ...
    }],
    "verifier": {
      "name_or_path": "meta-llama/Llama-3.1-8B-Instruct",
      "architectures": ["LlamaForCausalLM"]
    }
  }
}
```

这份配置将 speculator 定义为一个完整的模型，包含：

- 模型身份：
  - `architectures`：speculator 的模型类（如 Eagle3Speculator）
  - `auto_map`：面向 Hugging Face 兼容性的自定义模型加载
  - `Speculators_model_type`：具体的 speculator 实现
- 草稿模型架构：
  - `transformer_layer_config`：草稿模型 transformer 层的完整规格
  - `draft_vocab_size`：为高效草稿生成而缩减的词表大小（通常为 10k-32k 个 token）
  - 模型专属的配置选项
- 投机解码配置：
  - `algorithm`：投机解码算法（EAGLE3）
  - `proposal_methods`：带参数的 token 生成策略
    - `speculative_tokens`：每步生成的草稿 token 数量
    - `verifier_accept_k`：验证时考虑多少个 top-k 预测
    - `accept_tolerance`：接受草稿 token 的概率阈值
  - `verifier`：使用哪个验证器模型进行校验
    - `name_or_path`：HuggingFace 模型 ID 或本地路径
    - `architectures`：用于兼容性检查的验证器架构
