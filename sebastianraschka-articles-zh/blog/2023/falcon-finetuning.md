---
title: "使用 LoRA 对 Falcon LLM 进行微调"
title_en: "Falcon LLM Finetuning with LoRA"
source: https://sebastianraschka.com/blog/2023/falcon-finetuning.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 使用 LoRA 对 Falcon LLM 进行微调

> 原文：[Falcon LLM Finetuning with LoRA](https://sebastianraschka.com/blog/2023/falcon-finetuning.html)

微调让我们能够以高性价比的方式适配预训练 LLM。但我们应该使用哪种方法？本文针对当前表现最好的开源 LLM——Falcon，比较了几种不同的[参数高效微调](https://sebastianraschka.com/glossary/#lora "LoRA (Low-Rank Adaptation)")方法。

借助本文介绍的参数高效微调方法，可以把"在 6 块 GPU 上花一天时间微调 LLM"变成"在单块 GPU 上花 1 小时"。

## [预训练](https://sebastianraschka.com/glossary/#pretraining "Pretraining")与微调 LLM

在深入 LLM 微调细节之前，我们先简要回顾一下通常是如何训练 LLM 的。

LLM 的训练分为两个阶段。第一阶段是代价高昂的预训练步骤，模型在包含数万亿词的大型无标注数据集上训练。由此得到的模型通常被称为*基础*（foundation）模型，因为它们具备通用能力，可以被适配到各种下游任务。一个经典的[预训练模型](https://sebastianraschka.com/glossary/#base-model "Base Model")例子就是 GPT-3。

第二阶段是对这样的基础模型进行微调。这通常涉及训练预训练模型学会遵循指令，或执行另一个特定的目标任务（例如情感分类）。ChatGPT（最初是 GPT-3 基础模型的一个微调版本）就是经过微调以遵循指令的模型的典型例子。借助本文介绍的参数高效微调方法，可以把"在 6 块 GPU 上花一天时间微调 LLM"变成"在单块 GPU 上花 1 小时"。

![Falcon finetuning finetuning process](https://sebastianraschka.com/images/blog/2023/falcon-finetuning/finetuning-process.webp)

图题：微调一个预训练 LLM 使其遵循指令

微调还能让模型更好地适配其原始训练数据中覆盖不足的特定领域或文本类型。例如，如果我们希望模型理解和生成医学文本，就可以在医学文献上对它进行微调。

除了构建自定义聊天机器人，微调还可以把这些模型定制到特定的业务需求，在目标应用中提供更出色的性能。此外，当数据无法上传或无法与云端 API 共享时，微调还能带来数据隐私方面的优势。

**本文旨在说明如何在几小时内、在单块 GPU 上高效且低成本地微调一个顶尖的 LLM。**

## 微调 vs. ChatGPT

在 ChatGPT 的时代，我们究竟为什么还要关心微调模型？

OpenAI 的 ChatGPT 和 Google 的 Bard 这类闭源模型的问题在于，它们无法被方便地定制，这让它们在许多用例中吸引力下降。不过幸运的是，近几个月我们见证了大量开源 LLM 的涌现。（虽然 ChatGPT 和 Bard 具有强大的[上下文学习](https://sebastianraschka.com/glossary/#few-shot-prompting "Few-Shot Prompting")能力，但微调后的模型在特定任务上优于通用模型；最近强调这一点的研究例子包括 [Goat](https://arxiv.org/abs/2305.14201) 和 [Gorilla](https://arxiv.org/abs/2305.15334)。）

## 开源 LLM 与 Falcon 架构

微调开源 LLM 有诸多好处，例如更强的定制能力和更好的任务表现。此外，开源 LLM 也是研究人员开发新技术的绝佳试验台。另外，它还允许对环境的控制并保证可复现性——这对科学研究至关重要，而受 API 限制的模型无法满足这些条件。那么，如果今天要采用一个开源模型，应该选哪个？

截至撰写本文时，由 [Technology Innovation Institute](https://www.tii.ae/) 开发的 Falcon 模型是当前表现最好的开源 LLM。在本文中，我们将学习如何高效地微调它，例如在你的自定义数据集上。

![Falcon finetuning openllm](https://sebastianraschka.com/images/blog/2023/falcon-finetuning/openllm.webp)

图题：[OpenLLM 排行榜](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)节选

Falcon LLM 有不同的规模：截至撰写本文时，有 70 亿参数版本（Falcon 7B）和 400 亿参数版本（Falcon 40B）。此外，每种规模都有基础版（Falcon 7B 和 Falcon 40B）和[指令微调版](https://sebastianraschka.com/glossary/#instruct-model "Instruct Model")（Falcon 7B-instruct 和 Falcon 40B-instruct）。指令微调版已经针对通用任务做过微调（类似于 ChatGPT），但如果需要，仍可以在领域特定数据上进一步微调。（附言：[一个 180B 版本也在开发中](https://twitter.com/TIIuae/status/1664353061840601088?s=20)。）

请注意，Falcon 模型是完全开源的，采用了宽松的 [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) 许可证，允许不受限制的商业使用——例如 PyTorch Lightning、TensorFlow 和 OpenOffice 用的就是同一个许可证。

**Falcon 与 GPT 或 LLaMA 等其他 LLM 有何不同？**

除了上面强调的在 OpenLLM 排行榜上的更好表现之外，Falcon、LLaMA 和 GPT 之间还存在一些小的架构差异。LLaMA（[Touvron et al. 2023](https://arxiv.org/abs/2302.13971)）引入了以下架构改进，这些改进很可能是 LLaMA 性能优于 GPT-3（[Brown at al. 2020](https://arxiv.org/abs/2005.14165)）的原因：

- 与 GPT-3 类似，LLaMA 把层归一化放在[自注意力](https://sebastianraschka.com/glossary/#mha "Multi-Head Attention (MHA)")块之前；不过，研究人员没有像 GPT-3 那样使用 LayerNorm（[Ba et al. 2016](https://arxiv.org/abs/1607.06450)），而是选择了较新的 [RMSNorm](https://sebastianraschka.com/glossary/#rmsnorm "Root Mean Square Layer Normalization (RMSNorm)")（[Zhang and Sennrich 2019](https://arxiv.org/abs/1910.07467)）变体。
- LLaMA 借鉴了 PaLM（[Chowdhery et al. 2022](https://arxiv.org/abs/2204.02311)）使用 [SwiGLU](https://sebastianraschka.com/glossary/#swiglu "SwiGLU")（[Shazeer 2020](https://arxiv.org/abs/2002.05202)）激活函数的想法，而不是像 GPT-3 那样使用 ReLU。
- 最后，LLaMA 用[旋转位置嵌入（RoPE）](https://sebastianraschka.com/glossary/#rope "Rotary Positional Embeddings (RoPE)")（[Su et al. 2022](https://arxiv.org/abs/2104.09864)）取代了 GPT-3 使用的绝对位置嵌入，这一点与 GPTNeo（[Black et al. 2022](https://arxiv.org/abs/2204.06745)）类似。

那么，[根据目前已知的信息](https://huggingface.co/tiiuae/falcon-40b)，Falcon 采用了与 LLaMA（和 GPTNeo）相同的 RoPE 嵌入，除此之外与 GPT-3 共享相同的架构，唯一区别是使用了多查询注意力（multiquery attention，[Shazeer 2019](https://arxiv.org/abs/1911.02150)）。

多查询注意力是指为了效率，在不同的注意力头之间共享同一组键（key）和值（value）张量的概念，下方的多头注意力块图示说明了这一点。

![Falcon finetuning multiquery](https://sebastianraschka.com/images/blog/2023/falcon-finetuning/multiquery.webp)

图题：多查询注意力

此外，根据[训练数据信息](https://huggingface.co/tiiuae/falcon-40b#training-data)，Falcon 40B 是在 1000B（1 万亿）个 token 上训练的，其中 82% 的 token 来自 [RefinedWeb](https://huggingface.co/datasets/tiiuae/falcon-refinedweb) 语料库，其余 token 则来自书籍、论文、对话（Reddit、StackOverflow 和 HackerNews）以及代码。

虽然 Falcon 的官方论文尚未发布，但一篇相关论文[*The RefinedWeb Dataset for Falcon LLM: Outperforming Curated Corpora with Web Data, and Web Data Only*](https://arxiv.org/abs/2306.01116) 提供了证据，表明精选的网络数据可能正是其成功的关键。

总结一下，Falcon 的架构与 GPT-3 和 LLaMA 非常相似。Falcon 良好性能的关键差异因素很可能归功于它的训练数据集。

## 参数高效微调方法

本文余下部分将主要聚焦于 Falcon 7B，它让我们可以在单块 GPU 上微调该模型。Falcon 7B 目前被认为是同规模级别中最好的开源 LLM。（不过，本文余下介绍的同一套代码也可用于更大的 40B 版本。）

![Falcon finetuning openllm 2](https://sebastianraschka.com/images/blog/2023/falcon-finetuning/openllm-2.webp)

图题：知名的开源 LLM。[OpenLLM 排行榜](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)节选。

参数高效微调范式有很多，出色的综述[*Scaling Down to Scale Up: A Guide to Parameter-Efficient Fine-Tuning*](https://arxiv.org/abs/2303.15647) 中对此有详细介绍。

所有这些方法都达成了同一个目标：与传统微调（更新原始模型参数）相比，它们让我们能以更参数高效的方式训练模型。最大的问题是：哪些方法在实践中最值得采用？

让我们先看性能[基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")，再深入探讨这些不同方法的工作原理。

## 性能对比

为了在这个性能基准中使用一个通用数据集，我们选择流行的 [Alpaca 数据集](https://github.com/gururise/AlpacaDataCleaned)做指令微调，它包含 52k 条指令微调样本。其结构如下：

- Instruction: "Give three tips for staying healthy."
- Output: 1.Eat a balanced diet and make sure to include plenty of fruits and vegetables. 2. Exercise regularly to keep your body active and strong. 3. Get enough sleep and maintain a consistent sleep schedule."

我们考虑的三种方法是：

- Low-Rank Adaptation（LoRA）（[Hu et al. 2021](https://arxiv.org/abs/2106.09685)）；
- LLaMA Adapter（[Zhang et al. 2023](https://arxiv.org/abs/2303.16199)）；
- LLaMA-Adapter v2（[Gao et al. 2023](https://arxiv.org/abs/2304.15010)）。

没错，我们可以使用 LLaMA-Adapter 方法进行微调——尽管名字如此，这些适配器方法并不专属于 LLaMA 架构，我们稍后会讨论这一点。

**准备模型和数据集**

在这个基准测试中，我们将使用 [Lit-Parrot](https://github.com/Lightning-AI/lit-parrot) 开源库，它为训练和使用各种 LLM 提供了高效的实现。

![Falcon finetuning lit parrot](https://sebastianraschka.com/images/blog/2023/falcon-finetuning/lit-parrot.webp)

图题：Lit-Parrot 仓库（https://github.com/Lightning-AI/lit-parrot）

第一步是下载模型：

```python
python scripts/download.py --repo_id tiiuae/falcon-7b
```

（这需要大约 20 GB 的存储空间。）

第二步，把权重转换为标准化形式：

```python
python scripts/convert_hf_checkpoint.py --checkpoint_dir checkpoints/tiiuae/falcon-7b
```

第三步，我们需要下载数据集。在本例中，我们将使用包含 52k 指令对的 Alpaca 数据集 [link]：

```python
python scripts/prepare_alpaca.py --checkpoint_dir checkpoints/tiiuae/falcon-7b/
```

（稍后会更多介绍如何使用自定义数据集。）

**运行代码**

现在，我们运行 Falcon 7B 模型的微调脚本。下面我们将比较 4 种不同的方法。目前先聚焦微调结果，这些方法的工作原理会在本文后面讨论。

Adapter：

```python
python finetune/adapter.py --checkpoint_dir checkpoints/tiiuae/falcon-7b/
```

Adapter v2：

```python
python finetune/adapter_v2.py --checkpoint_dir checkpoints/tiiuae/falcon-7b/
```

LoRA：

```python
python finetune/lora.py --checkpoint_dir checkpoints/tiiuae/falcon-7b/
```

完整微调（更新所有层）：

```python
python finetune/lora.py --checkpoint_dir checkpoints/tiiuae/falcon-7b/
```

我们先来看看微调 LLM 所需的时间：

![Falcon finetuning training time](https://sebastianraschka.com/images/blog/2023/falcon-finetuning/training-time.webp)

正如上面的图表所示，使用参数高效微调方法比微调所有层（"full"）快约 9 倍。此外，由于显存限制，微调所有层需要 6 块 GPU，而 **Adapter 方法和 LoRA 可以在单块 GPU 上运行**。

说到 GPU 显存需求，峰值显存需求如下图所示：

![Falcon finetuning memory requirements](https://sebastianraschka.com/images/blog/2023/falcon-finetuning/memory-requirements.webp)

微调 Falcon 7B 的所有层需要在 6 块 GPU 的每一块上占用约 40 GB 显存（此处通过 DeepSpeed 进行张量分片）。也就是说总共 240 GB。相比之下，参数高效微调方法只需要约 16 GB 内存，这让用户甚至可以在单块消费级 GPU 上微调这些模型。

顺便一提，请注意显存需求与每种方法需要更新的参数数量直接相关：

- 完整微调：7,217,189,760
- Adapter：1,365,330
- Adapter v2：3,839,186
- LoRA：3,506,176

是的，你没看错：完整微调（更新所有层）需要更新的参数是 Adapter v2 或 LoRA 方法的 2000 倍，而如 [Hu et al. 2021](https://arxiv.org/abs/2106.09685) 所报告的那样，后者的建模性能与完整微调相当（有时甚至更好）。

至于推理速度，我们有以下性能数据：

- LoRA：21.33 tokens/秒；内存占用：14.59 GB（可以将 LoRA 权重与原始权重合并，把性能提升到 >28 tokens/秒）
- Adapter：26.22 tokens/秒；内存占用：14.59 GB
- Adapter v2：24.73 tokens/秒；内存占用：14.59 GB

**超参数**

如果你想复现上述结果，以下是我使用的超参数设置概览：

- `bfloat16` 精度（我在文章 [Accelerating Large Language Models with Mixed-Precision Techniques](https://lightning.ai/pages/community/tutorial/accelerating-large-language-models-with-mixed-precision-techniques/) 中写过更多关于 bfloat16 的内容）。
- 此外，脚本被配置为使用梯度累积、以 128 的有效 batch size 训练模型 52k 次迭代（即 Alpaca 数据集的大小）（关于梯度累积的更多细节见我的文章 [Finetuning LLMs on a Single GPU Using Gradient Accumulation](https://lightning.ai/pages/blog/gradient-accumulation/)）。
- 对于 LoRA，我使用秩（rank）8，以大致匹配 Adapter v2 新增的参数数量。
- `adapter.py`、`adapter_v2.py` 和 `lora.py` 各自在单块 A100 GPU 上训练。`full.py` 脚本需要 6 块 A100 GPU，并通过 DeepSpeed 进行张量分片。

另外，我把修改过设置的脚本上传到了 GitHub 的[这里](https://github.com/rasbt/LLM-finetuning-scripts/tree/main/lit-benchmarks/falcon-7b)，供参考。

## 质量对比

虽然针对真实任务的详细性能基准超出了本篇博客文章的范围，但这些方法的定性模型表现大致相同。它与 [LoRA](https://arxiv.org/abs/2106.09685) 和 [LLaMA-Adapter](https://arxiv.org/abs/2303.16199) 论文中讨论的完整微调性能相匹配。

如果你想使用并评估这些模型，可以使用 lit-parrot 提供的以下 `generate` 脚本，例如：

```python
python generate/lora.py --checkpoint_dir checkpoints/tiiuae/falcon-7b --lora_path out/lora/alpaca/lit_model_lora_finetuned.pth
```

## LLaMA-Adapter

简而言之，LLaMA-Adapter 方法（在本博客文章中我们称之为 *Adapter*）向现有的 LLM 添加少量可训练的张量（参数）。这里的想法是只训练新参数，而原始参数保持冻结。这可以在反向传播期间节省大量计算和内存。

再稍微详细一点，LLaMA-Adapter 在嵌入输入之前添加（prepend）可调的提示张量（前缀）。在 LLaMA-Adapter 方法中，这些前缀是在一个嵌入表中学习和维护的，而不是外部提供的。模型中的每个 transformer 块都有自己独特的已学习前缀，从而在不同模型层之间实现更有针对性的适配。

此外，LLaMA-Adapter 引入了零初始化注意力机制并结合门控。这种所谓 *zero-init* 注意力与门控背后的动机是：适配器和前缀调优可能会通过引入随机初始化的张量（前缀提示或适配器层）而破坏预训练 LLM 的语言知识，导致微调不稳定以及初始训练阶段的高损失值。

LLaMA-Adapter 方法的主要概念如下图所示，常规 transformer 块中被修改的部分以紫色高亮。

![Falcon finetuning llama adapter](https://sebastianraschka.com/images/blog/2023/falcon-finetuning/llama-adapter.webp)

一个关键想法是只添加少量可训练参数。这里另一个需要注意的要点是，该方法并非 LLaMA LLM 独有——这就是为什么我们可以用它来微调 Falcon 模型。

如果你对 LLaMA-Adapter 方法的更多细节感兴趣，请查看我的文章 [Understanding Parameter-Efficient Finetuning of Large Language Models: From Prefix Tuning to LLaMA-Adapters](https://lightning.ai/pages/community/article/understanding-llama-adapters/)。

## LLaMA-Adapter v2

在文本和指令上微调 LLM 时，较新的 LLaMA-Adapter v2（[Gao et al 2023](https://arxiv.org/abs/2304.15010)）相比 LLaMA-Adapter V1（[Zhang et al. 2023](https://arxiv.org/abs/2303.16199)）增加了可调参数的数量。第一个差异是它为全连接（线性）层添加了偏置单元。由于它只是把现有的线性层从 `input * weight` 改为 `input * weight + bias`，因此对微调和推理性能的影响很小。

第二个差异是它使前面提到的 RMSNorm 层变为可训练。虽然由于更新了额外的参数，这对训练性能有一些小影响，但它不会影响推理速度，因为它没有给网络添加任何新参数。

## Low-Rank Adaptation（LoRA）

Low-Rank Adaptation（[Hu et al 2021](https://arxiv.org/abs/2106.09685)）与上面的 Adapter 方法类似，也是向模型添加少量可训练参数，同时原始模型参数保持冻结。不过，其底层概念与 LLaMA-Adapter 方法有根本性的不同。

简而言之，LoRA 将一个权重矩阵分解为两个更小的权重矩阵，如下图所示：

![Falcon finetuning lora weights](https://sebastianraschka.com/images/blog/2023/falcon-finetuning/lora-weights.webp)

关于 LoRA 的更多细节，请参阅我更长、更技术性的文章 [Parameter-Efficient LLM Finetuning With Low-Rank Adaptation (LoRA)](https://lightning.ai/pages/community/tutorial/lora-llm/)。

## 在你的自定义数据集上微调 LLM

在本文中，我们在 Alpaca（52k 条指令）数据集上运行了几个性能基准。在实践中，你可能好奇如何把这些方法应用到你自己的数据集上。毕竟，开源 LLM 的优势就在于我们可以针对自己的目标数据和任务对它们进行微调和定制。

从本质上讲，在你自己的数据集上使用这些 LLM 和技术，所需要的就是确保数据以标准化的形式组织，这在 Aniket Maurya 的博客文章 [How To Finetune GPT Like Large Language Models on a Custom Dataset](https://lightning.ai/pages/blog/how-to-finetune-gpt-like-large-language-models-on-a-custom-dataset/) 中有更详细的描述。

## 结论

在本文中，我们看到了如何使用 LLaMA-Adapter 方法或 LoRA，在单块 GPU 上微调像 Falcon 这样的最先进的开源 LLM。

传统的全层微调需要 9 个小时，并且至少需要 6 块各带 40 GB 显存的 A100 GPU；而本文重点介绍的参数高效微调方法可以在单块 GPU 上以 9 倍的速度微调同一个模型，显存需求减少 15 倍。

如果你有兴趣在自己的项目中采用这些方法，请查看开源的 [Lit-Parrot](https://github.com/Lightning-AI/lit-parrot/) 仓库来上手。

**致谢**

我要感谢 Carlos Mocholí，他在修复我的 LoRA 脚本方面帮了大忙。同时也要向 Adrian Wälchli 和 Luca Antiga 致谢，感谢他们将 Falcon 集成到 Lit-Parrot 仓库中。
