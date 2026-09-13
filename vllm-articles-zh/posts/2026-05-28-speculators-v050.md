---
title: "Speculators v0.5.0：DFlash 支持与在线训练"
title_en: "Speculators v0.5.0: DFlash Support and Online Training"
source: https://vllm.ai/blog/2026-05-28-speculators-v050
crawled: 2026-09-12
translated: 2026-09-13
---

# Speculators v0.5.0：DFlash 支持与在线训练

> 原文：[Speculators v0.5.0: DFlash Support and Online Training](https://vllm.ai/blog/2026-05-28-speculators-v050) · vLLM 博客

作者：Fynn Schmitt-Ulms、Helen Zhao、Rahul Tuli 与 Dipika Sikka（Red Hat AI 模型优化团队）

[#投机解码](https://vllm.ai/blog/tags/speculative-decoding)[#生态](https://vllm.ai/blog/tags/ecosystem)

[v0.5.0 版本](https://github.com/vllm-project/speculators/releases/tag/v0.5.0)为投机解码模型训练带来了显著的架构改进：引入 DFlash 算法支持、完全统一的在线训练能力，以及向 vLLM 原生隐藏状态提取系统的完整迁移。本次发布在训练灵活性与投机解码工作流的生产就绪性上都是一个重大进步。

主要特性包括：

- DFlash 算法支持——利用块扩散（block diffusion）进行单次前向草稿 token 生成
- Gemma 4 DFlash 结果
- 基于 vLLM 原生的在线与离线训练，统一隐藏状态提取
- 更新了文档与示例，阐明关键工作流

## DFlash 算法支持

v0.5.0 引入了对 DFlash 投机解码算法的训练支持，这是一种与自回归 Eagle 3 模型截然不同的草稿 token 生成方式。Eagle 3 通过多次前向传播自回归地生成草稿 token，而 DFlash 采用块扩散在单次前向传播中生成所有草稿 token。

DFlash 的单次前向特性可以大幅降低投机解码的开销，对于较长的草稿序列尤其如此。起草器为每个前缀生成一个长度为 B 的 token 块。这一块结构完全通过注意力掩码实现。与 Eagle3 的另一个关键区别是，DFlash 使用非因果注意力模式，块内的查询可以关注同一块内的所有其他 token。

在训练期间，多个预测块会并行训练。一个直接的做法是在序列中每个可能的位置之后都开始一个预测块。但对于长序列，这会使注意力掩码增长得极其庞大，导致训练在内存和计算成本上都不可行。为避免这一点，我们并不在所有位置都开始块，而是从真正对训练损失有贡献的位置中随机挑选一小组"锚点"位置。预测块只挂在这些锚点上。这样，无论序列多长，预测块的数量都保持固定，使训练能扩展到长得多的上下文，同时注意力掩码依然可控。

## 训练 DFlash 投机模型

训练 DFlash 模型遵循与 Eagle 3 类似的在线工作流。完整教程见[这里](https://docs.vllm.ai/projects/speculators/en/latest/user_guide/tutorials/train_dflash_online/)。

与 Eagle 3 的关键区别在于训练命令中的投机模型专属参数，如下所示：

```
torchrun --standalone --nproc_per_node 2 scripts/train.py \
    --verifier-name-or-path "Qwen/Qwen3-8B" \
    --vllm-endpoint "http://localhost:8000/v1" \
    --speculator-type dflash \
    --draft-vocab-size 8192 \
    --block-size 8 \
    --max-anchors 3072 \
    --num-layers 5 \
    --target-layer-ids "2 18 33" \
    --epochs 5 --lr 1e-4
```

DFlash 专属参数包括：

```
--block-size # Number of tokens generated per diffusion block
--max-anchors # Maximum anchor points for speculation during training
--speculator-type # Must specify dflash
```

## Gemma 4 DFlash 投机模型

借助 DFlash 算法支持，我们训练了一个 [Gemma 4 31B DFlash 投机模型](https://huggingface.co/RedHatAI/gemma-4-31B-it-speculator.dflash)，并在多种任务类型上评估了接受率。结果表明其在推理和代码生成任务上表现尤为出色：

![Figure 1: Gemma 4 DFlash acceptance rates across diverse task types.](https://vllm.ai/blog-assets/figures/2026-05-28-speculators-v050/gemma4-dflash-acceptance-rates.png)

图 1：Gemma 4 DFlash 在多种任务类型上的接受率。

Gemma 4 DFlash 的逐 token 延迟优于 Eagle 3 和单独的 FP8 量化验证器。将 DFlash 与 FP8 量化验证器结合可获得更大收益，如下所示：

![Figure 2: Gemma 4 DFlash inter-token latency comparison.](https://vllm.ai/blog-assets/figures/2026-05-28-speculators-v050/gemma4-dflash-latency.png)

图 2：Gemma 4 DFlash 逐 token 延迟对比。

## 在 vLLM 中服务 DFlash 模型

自 PR [#38300](https://github.com/vllm-project/vllm/pull/38300) 起（包含在 `vllm>=0.20.0` 中），DFlash 模型可与 vLLM 的投机解码基础设施无缝集成。

与 Eagle 3 模型类似，DFlash 模型的 config.json 中包含 `speculators_config`，其中记录目标模型、投机 token、投机算法名称等细节。有了这一配置，模型只需一条基本的 `vllm serve` 命令即可服务，如下所示。

```
vllm serve -tp 2 RedHatAI/gemma-4-31B-it-speculator.dflash
```

## 统一的在线与离线训练支持

v0.5.0 通过 [vLLM 的隐藏状态提取系统](https://vllm.ai/blog/extract-hidden-states)（在 vLLM v0.18.0 中引入）为在线和离线两种训练模式增加了原生支持。此前版本的 Speculators 使用 vLLM 的底层工具提取隐藏状态，要求把 vLLM 作为直接 Python 依赖。这种方式把训练流水线与 vLLM 的内部 API 紧密耦合，而这些 API 常在 vLLM 版本更新时变动，需要手动与上游变化同步。此次集成移除了以往自定义的数据生成流水线，并消除了 vLLM 作为直接 Python 依赖的需求。

两种训练模式现在使用同一条基于 vLLM 的提取路径：

- 在线训练：在训练过程中即时提取隐藏状态
- 离线训练：预生成隐藏状态并缓存到磁盘，然后训练

通过利用 vLLM 的原生隐藏状态提取，Speculators 继承了 vLLM 的全部推理优化，包括高效的内存管理、批处理策略和硬件加速支持。训练现在通过 vLLM 服务器的标准 REST API 与运行中的 vLLM 服务通信，把训练基础设施与 vLLM 的内部实现细节解耦。这一架构转变带来更好的版本稳定性，让团队可以独立于 Speculators 训练框架更新 vLLM。

在线训练的过程如下：

1. vLLM 服务器以基础模型（以及一些特殊配置）初始化
2. 训练提示词被发送给 vLLM 进行推理
3. 隐藏状态被提取并临时写入磁盘（或内存盘）
4. 训练进程加载提取出的隐藏状态并删除文件
5. 投机模型在提取的状态上训练

[本教程](https://docs.vllm.ai/projects/speculators/en/latest/user_guide/tutorials/train_eagle3_online/)提供关于在线训练工作流的更多信息。

离线数据生成也已更新，使用与在线相同的隐藏状态提取系统和数据格式。我们开发了新脚本，用请求填满运行中的 vLLM 服务器并把结果写入磁盘。这两种方式耦合得非常紧密，你甚至可以组合使用。例如，你可以先离线生成部分隐藏状态，然后运行训练并加载已有的隐藏状态，同时生成缺失的部分。你也可以运行一个生成文件后不清理文件的在线训练任务，从而在第一个 epoch 生成一次，后续 epoch 直接加载这些文件。

[本教程](https://docs.vllm.ai/projects/speculators/en/latest/user_guide/tutorials/train_eagle3_offline/)更详细地介绍离线训练工作流。

## 新增全面文档

另一个值得一提的亮点是更新后的[文档站点](https://docs.vllm.ai/projects/speculators/en/latest/)。我们为 Speculators 支持的投机解码算法添加了简明介绍，并提供了训练投机模型的详细教程。面向开发者，我们还新增了关于如何向 Speculators 库添加新投机解码算法的指南，以及完整的 API 参考。
