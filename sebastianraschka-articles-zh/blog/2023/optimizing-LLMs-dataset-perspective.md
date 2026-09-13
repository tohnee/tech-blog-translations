---
title: "从数据集视角看大语言模型"
title_en: "LLMs From a Dataset Perspective"
source: https://sebastianraschka.com/blog/2023/optimizing-LLMs-dataset-perspective.html
crawled: 2026-09-06
translated: 2026-09-06
---

# 从数据集视角看大语言模型

> 原文：[LLMs From a Dataset Perspective](https://sebastianraschka.com/blog/2023/optimizing-LLMs-dataset-perspective.html)

本文聚焦于如何通过精心整理的数据集对大语言模型进行微调，从而提升其建模性能。具体来说，本文重点介绍的是针对指令微调对数据集进行修改、利用或操作的策略，而不是改动模型架构或训练算法（后者将是未来文章的主题）。本文还会讲解如何准备你自己的数据集来微调开源大语言模型。

值得注意的是，[NeurIPS LLM Efficiency Challenge](https://llm-efficiency-challenge.github.io) 目前正在进行中，目标是在单块 GPU 上于 24 小时内训练一个大语言模型，这对关心大语言模型效率的从业者和研究者来说非常有趣。本文讨论的技术与这项比赛直接相关，我们还会深入探讨这些以数据集为中心的策略如何可能应用到比赛场景中。此外，本文还将给出一些值得尝试的新实验建议。

[**本文是一篇转载文章，最早发表于 Lightning AI 博客**](https://lightning.ai/pages/community/tutorial/optimizing-llms-from-a-dataset-perspective/)。

## 监督式指令微调

什么是指令微调？我们为什么要关心它？

指令微调是一种提升 ChatGPT 和 [Llama-2-chat](https://www.google.com/url?q=https://arxiv.org/abs/2307.09288&sa=D&source=editors&ust=1694778155820217&usg=AOvVaw3DfjwSmu9UDiKXYfwwNURe) 这类语言模型性能的方法：让模型针对一系列"输入示例配对期望输出"的数据生成输出。它使模型在特定应用或任务中的行为更加可控、更符合预期，还能提升 AI 系统在真实场景中的可靠性、针对性与安全性。

![Optimizing LLMs dataset perspective image1](https://sebastianraschka.com/images/blog/2023/optimizing-llms-dataset-perspective/image1.webp)
*来自 [InstructGPT 论文](https://www.google.com/url?q=https://arxiv.org/abs/2203.02155&sa=D&source=editors&ust=1694778155821067&usg=AOvVaw0b9IRsqGEu2lM_iI5nMzZM)的标注图*

指令微调使用由"指令—响应"配对组成的数据集来提升大语言模型遵循指令的能力。这样的指令微调数据集通常由三个部分构成：

1. 指令文本
2. 输入文本（可选）
3. 输出文本

下面的示例列出了两个训练样本，一个不含可选的输入文本，一个含有：

![Optimizing LLMs dataset perspective image3](https://sebastianraschka.com/images/blog/2023/optimizing-llms-dataset-perspective/image3.webp)

随后，大语言模型通过下一 token 预测在这些指令数据集上进行微调（与[预训练](https://sebastianraschka.com/glossary/#pretraining "Pretraining")类似）。与预训练的区别在于：模型会先看到完整的指令和输入文本作为上下文，然后才被要求以自回归方式执行下一 token 预测、生成输出文本，如下图所示。

![Optimizing LLMs dataset perspective image2](https://sebastianraschka.com/images/blog/2023/optimizing-llms-dataset-perspective/image2.webp)

上述以迭代、逐 token 的方式微调大语言模型生成期望输出的过程，也被称为[监督微调](https://sebastianraschka.com/glossary/#instruction-finetuning "Instruction Finetuning (SFT)")。

在实践中，监督微调之后还有一个可选的微调阶段：它使用额外的偏好数据和排名标签，这些数据来自对大语言模型生成的响应进行比较的人类标注者。这一过程也被称为基于人类反馈的强化学习（[RLHF](https://sebastianraschka.com/glossary/#rlhf "RLHF (Reinforcement Learning from Human Feedback)")），但它超出了本文的范围——本文聚焦于指令数据集本身。（不过，如果你想了解更多，我在[这里](https://magazine.sebastianraschka.com/p/llm-training-rlhf-and-its-alternatives)有一篇关于 RLHF 的可选文章。）

## 微调流水线与数据集来源

微调大语言模型时，指令微调数据集可以通过多种途径获得：

**1. 人工创建：** 专家标注者可以提供明确的指令和反馈，创建用于指令微调的数据集。这对于特定领域任务，或者减少特定的偏见和不良行为尤其有用。

**2. 大语言模型生成：** 我们可以用现有的大语言模型生成海量的候选输入—输出配对（前提是服务条款允许）。随后可以由人工对质量进行精修或评分，再用于微调新的大语言模型。这种方法通常比上述人工创建的方式更高效，因为一个现成的大语言模型（如通过 API 接口调用的 GPT-4）可以在短时间内生成大量候选样本。

使用人工创建或大语言模型生成数据的大语言模型微调流水线，在近期出色的一篇综述 *[Instruction Tuning for Large Language Models](https://arxiv.org/abs/2308.10792)* 中有概括：

![Optimizing LLMs dataset perspective image5](https://sebastianraschka.com/images/blog/2023/optimizing-llms-dataset-perspective/image5.webp)
*来自 [Instruction Tuning for Large Language Models](https://arxiv.org/abs/2308.10792) 论文的图*

此外，我们还可以把人工创建与大语言模型生成的指令数据结合起来，兼取两者之长。

接下来的几节将更详细地讨论用于指令微调的大语言模型生成数据集和人工创建数据集，包括近期的研究亮点。

## 大语言模型生成的数据集

数据集标注一直是机器学习领域的瓶颈。作为人工标注者，像"把一张图片归类为猫或狗"这样的简单标注任务，一旦需要大规模进行，就已经相当费时费力。

需要长篇文本标注的任务则更加耗时、更具挑战性。因此，人们在利用现有大语言模型自动生成指令微调数据集方面投入了大量精力。

**Self-Instruct**

最著名、使用最广泛的大语言模型生成数据集方法之一是 [Self-Instruct](https://arxiv.org/abs/2212.10560)。

那么，它是如何工作的？简要来说，它包含四个阶段：

1. 用一组人工编写的指令（本例中为 175 条）作为种子任务池，并从中采样指令；
2. 使用一个预训练大语言模型（如 GPT-3）来确定任务类别；
3. 给定新指令，让预训练大语言模型生成响应；
4. 对响应进行收集、修剪和过滤，然后加入任务池。

![Optimizing LLMs dataset perspective image4](https://sebastianraschka.com/images/blog/2023/optimizing-llms-dataset-perspective/image4.webp)

Self-Instruct 早期的一个知名应用是 [Alpaca 数据集](https://github.com/gururise/AlpacaDataCleaned)，它由 5.2 万个大语言模型生成的指令—响应配对组成。今年早些时候，Alpaca 被用于创建第一个微调版 [Llama v1](https://arxiv.org/abs/2302.13971) 模型。

**反向翻译（Backtranslation）**

另一类有趣的思路是从响应出发反向工作，用大语言模型生成对应的指令。

换句话说，不必从人类写手那里收集指令微调数据集，而是可以用大语言模型来产出指令—响应配对（这也被称为[蒸馏](https://sebastianraschka.com/glossary/#distillation "Distillation")）。

在一篇题为 *[Self-Alignment with Instruction Backtranslation](https://arxiv.org/abs/2308.06259)* 的论文中，研究者通过"指令反向翻译"对大语言模型进行精调，发现该方法超越了在 Alpaca 等蒸馏数据集上训练的模型。

![Optimizing LLMs dataset perspective image7](https://sebastianraschka.com/images/blog/2023/optimizing-llms-dataset-perspective/image7.webp)

**NeurIPS 效率挑战赛规则**

注意，以"1 个大语言模型、1 天、1 块 GPU"为核心的 [NeurIPS LLM Efficiency Challenge](https://llm-efficiency-challenge.github.io) 不允许使用大语言模型生成的数据集。

因此，在下一节*高质量数据集*中，我们将聚焦于可以作为替代的人工生成指令数据集。

如果你有兴趣参加 [NeurIPS LLM Efficiency Challenge](https://llm-efficiency-challenge.github.io)，我在[这里](https://github.com/Lightning-AI/lit-gpt/blob/main/tutorials/neurips_challenge_quickstart.md)写了一篇快速上手教程。

**关于大语言模型生成数据集与模仿模型的提醒**

在深入讨论人工生成的指令微调数据集之前，我想就大语言模型生成数据集简单提醒一句。没错，用大语言模型生成数据集听起来好得不太真实，因此对在大语言模型生成数据集上微调出的大语言模型，我们要格外仔细地评估。

例如，在近期一篇 *[The False Promise of Imitating Proprietary LLMs](https://arxiv.org/abs/2305.15717)* 论文中，研究者观察到，众包标注者对在大语言模型生成数据上训练的大语言模型给出了高分。然而，这些所谓的"模仿模型"主要复制的是它们所训练的上游大语言模型的风格，而不是其事实准确性。

## 高质量数据集：少即是多

上一节我们讨论了大语言模型生成的数据集。现在，让我们换个方向，考察一个高质量的人工生成数据集——它也是 [NeurIPS LLM Efficiency Challenge](https://llm-efficiency-challenge.github.io) 所允许使用的。

**LIMA**

*[The LIMA: Less Is More for Alignment](https://arxiv.org/abs/2305.11206)* 论文表明，在指令微调数据集上，质量胜过数量。

在这项研究中，研究者精心挑选了 1000 个指令配对，用监督微调的方式微调了 650 亿参数的 Llama-v1 模型，即 LIMA。

值得注意的是，其他微调过的 Llama 模型（如 Alpaca）是在一个规模大得多的数据集上训练的——包含 5.2 万个大语言模型生成的指令配对。在部分基准测试中，LIMA 的表现优于采用了基于人类反馈的强化学习（RLHF）方法的模型，包括 ChatGPT 和 GPT-3.5。

![Optimizing LLMs dataset perspective image6](https://sebastianraschka.com/images/blog/2023/optimizing-llms-dataset-perspective/image6.webp)
*来自 [LIMA 论文](https://arxiv.org/abs/2305.11206)的标注图*

下一节将向你展示如何上手开源大语言模型，并在 LIMA 上微调这些模型。

## 在 LIMA 上微调大语言模型

本节讲解如何使用 [Lit-GPT 仓库](https://github.com/Lightning-AI/lit-gpt)在 LIMA 这类指令数据集上微调开源大语言模型。

（注意，[NeurIPS LLM Efficiency Challenge](https://llm-efficiency-challenge.github.io) 的主办方已批准在比赛中使用 LIMA。主办方还选定 Lit-GPT 作为起始工具包，因为它的代码相对易用、易于定制，而这正是探索新研究方向的重要前提。）

截至撰写本文时，Lit-GPT 目前支持的模型如下：

| **模型与用法** | **出处** |
| --- | --- |
| Meta AI [Llama 2](https://github.com/Lightning-AI/lit-gpt/blob/main/tutorials/download_llama_2.md) | [Touvron et al. 2023](https://arxiv.org/abs/2307.09288) |
| Stability AI [FreeWilly2](https://github.com/Lightning-AI/lit-gpt/blob/main/tutorials/download_freewilly_2.md) | [Stability AI 2023](https://stability.ai/blog/stable-beluga-large-instruction-fine-tuned-models) |
| Stability AI StableCode | [Stability AI 2023](https://stability.ai/blog/stablecode-llm-generative-ai-coding) |
| TII UAE [Falcon](https://github.com/Lightning-AI/lit-gpt/blob/main/tutorials/download_falcon.md) | [TII 2023](https://falconllm.tii.ae/) |
| OpenLM Research [OpenLLaMA](https://github.com/Lightning-AI/lit-gpt/blob/main/tutorials/download_openllama.md) | [Geng & Liu 2023](https://github.com/openlm-research/open_llama) |
| LMSYS [Vicuna](https://github.com/Lightning-AI/lit-gpt/blob/main/tutorials/download_vicuna.md) | [Li et al. 2023](https://lmsys.org/blog/2023-03-30-vicuna/) |
| LMSYS [LongChat](https://github.com/Lightning-AI/lit-gpt/blob/main/tutorials/download_longchat.md) | [LongChat Team 2023](https://lmsys.org/blog/2023-06-29-longchat/) |
| Together [RedPajama-INCITE](https://github.com/Lightning-AI/lit-gpt/blob/main/tutorials/download_redpajama_incite.md) | [Together 2023](https://together.ai/blog/redpajama-models-v1) |
| EleutherAI [Pythia](https://github.com/Lightning-AI/lit-gpt/blob/main/tutorials/download_pythia.md) | [Biderman et al. 2023](https://arxiv.org/abs/2304.01373) |
| StabilityAI [StableLM](https://github.com/Lightning-AI/lit-gpt/blob/main/tutorials/download_stablelm.md) | [Stability AI 2023](https://github.com/Stability-AI/StableLM) |
| Platypus | [Lee, Hunter, and Ruiz 2023](https://arxiv.org/abs/2308.07317) |
| NousResearch Nous-Hermes | [Org page](https://huggingface.co/NousResearch) |
| Meta AI [Code Llama](https://github.com/Lightning-AI/lit-gpt/blob/main/tutorials/download_code_llama.md) | [Rozière et al. 2023](https://arxiv.org/abs/2308.12950) |

在这个简短的实操演示中，我们将使用 7B 参数的 [Llama 2 基座模型](https://github.com/Lightning-AI/lit-gpt)，并在 LIMA 上对它进行微调。

假设你已经克隆了 Lit-GPT 仓库，可以通过以下三个步骤上手：

1) 下载并准备模型：

```python
export HF_TOKEN=your_token

python scripts/download.py \
 --repo_id meta-llama/Llama-2-7b-hf
```

```python
python scripts/convert_hf_checkpoint.py \
 --checkpoint_dir meta-llama/Llama-2-7b-hf
```

2) 准备数据集：

```python
python scripts/prepare_lima.py \
 --checkpoint_dir checkpoints/meta-llama/Llama-2-7b-hf
```

3) 使用[低秩适应](https://sebastianraschka.com/glossary/#lora "LoRA (Low-Rank Adaptation)")（LoRA）微调模型：

```python
python finetune/lora.py \
 --checkpoint_dir checkpoints/meta-llama/Llama-2-7b-hf \
 --data_dir data/lima
```

注意，第 2 步准备数据集时必须提供 –checkpoint\_dir 参数，因为数据集准备是依赖于具体模型的。不同的大语言模型可能使用不同的分词器和特殊 token，因此相应地准备数据集非常重要。

为了保持本文聚焦于数据集视角，我略去了对 LoRA 微调流程的详细讲解。不过，如果你有兴趣深入了解，可以看我这篇文章：[Finetuning Falcon LLMs More Efficiently With LoRA and Adapters](https://lightning.ai/pages/community/finetuning-falcon-efficiently/)。

此外，我的 [NeurIPS 2023 LLM Efficiency Challenge 快速上手指南](https://github.com/Lightning-AI/lit-gpt/blob/main/tutorials/neurips_challenge_quickstart.md)一文或许也对你有帮助，其中我一步步演示了环境搭建、微调和模型评估。

---

**提示**

根据[官方比赛规则](https://llm-efficiency-challenge.github.io/question)，评估所用的最大[上下文长度](https://sebastianraschka.com/glossary/#context-length "Context Length")为 2,048 个 token。因此，我建议在准备数据集时把最大长度设为 2,048 个 token：

```python
python scripts/prepare_lima.py \
  --checkpoint_dir checkpoints/meta-llama/Llama-2-7b-hf \
  --max_seq_length 2048
```

另一种做法是编辑 [finetune/lora.py](https://github.com/Lightning-AI/lit-gpt/blob/main/finetune/lora.py%23L37) [文件](https://github.com/Lightning-AI/lit-gpt/blob/main/finetune/lora.py%23L37)，把 `override_max_seq_length = None` 改成 `override_max_seq_length = 2048`，以降低 GPU 显存需求。

另外，我还建议修改 max\_iter 设置，将其改为 `max_iter = 1000`，这样相当于对 LIMA 数据集（包含 1000 个训练样本）完整训练约 1 遍。

![Optimizing LLMs dataset perspective image9](https://sebastianraschka.com/images/blog/2023/optimizing-llms-dataset-perspective/image9.webp)

---

作为参考，在默认设置下用 LoRA 在 5.2 万个指令配对（如 Alpaca）上微调一个 7B 参数模型，在 A100 GPU 上大约需要 1 小时。注意，LIMA 比 Alpaca 小 50 倍，所以微调只需几分钟。

![Optimizing LLMs dataset perspective image8](https://sebastianraschka.com/images/blog/2023/optimizing-llms-dataset-perspective/image8.webp)

图题：通过《Finetuning Falcon LLMs More Efficiently With LoRA and Adapters》（<https://lightning.ai/pages/community/finetuning-falcon-efficiently/>）在 5.2 万个数据点上微调 7B 模型

## Lit-GPT 中可用的模型与数据集

截至撰写本文时，[Lit-GPT](https://github.com/Lightning-AI/lit-gpt) 目前支持多个微调数据集。

![Optimizing LLMs dataset perspective image12](https://sebastianraschka.com/images/blog/2023/optimizing-llms-dataset-perspective/image12.webp)

[Dolly](https://github.com/Lightning-AI/lit-gpt/blob/main/tutorials/prepare_dataset.md) 和 [LIMA](https://github.com/Lightning-AI/lit-gpt/blob/main/tutorials/prepare_dataset.md%23lima) 数据集是人工生成的，因此可以在 [NeurIPS LLM Efficiency Challenge](https://llm-efficiency-challenge.github.io) 中放心使用。

此外，如果你有兴趣使用不同的数据集来为你的项目定制大语言模型，下一节将简要说明具体做法。

## 准备新的自定义数据集

除了上文提到的现有数据集之外，你可能还想添加新的数据集，或者使用自己的数据集来微调定制的开源大语言模型。

为 Lit-GPT 中的大语言模型准备数据集主要有两种方式：

1. 使用 scripts/prepare\_csv.py 脚本从 CSV 文件中读取指令数据集。
2. 创建一个类似 LIMA 所用的自定义 scripts/prepare\_dataset.py 脚本。

准备新数据集最简单的方式，是使用 Lit-GPT 中的 scripts/prepare\_csv.py 脚本从 CSV 文件读取。你只需要一个包含如下所示三个列名的 CSV 文件：

![Optimizing LLMs dataset perspective image10](https://sebastianraschka.com/images/blog/2023/optimizing-llms-dataset-perspective/image10.webp)

假设你把这个数据集导出为 MyDataset.csv，接下来就可以按如下方式准备数据并微调模型：

1) 准备数据集：

```python
python scripts/prepare_csv.py \
  --csv_dir MyDataset.csv \
  --checkpoint_dir checkpoints/meta-llama/Llama-2-7b-hf
```

2) 使用低秩适应（LoRA）微调模型：

```python
python finetune/lora.py \
  --data_dir /data/csv \
  --checkpoint_dir checkpoints/meta-llama/Llama-2-7b-hf
```

还有一些用于确定随机种子或训练/验证划分的额外选项，可以通过以下命令查看：

```python
python scripts/prepare_csv.py --help
```

如果你对第二种方式感兴趣——即创建一个类似 LIMA 的 prepare\_dataset.py 脚本——我在[Lit-GPT 文档的这里](https://github.com/Lightning-AI/lit-gpt/blob/main/tutorials/prepare_dataset.md%23preparing-custom-datasets-for-instruction-finetuning)补充了说明。

## 其他值得考虑的数据集

上一节介绍了如何在 Lit-GPT 中为开源大语言模型准备自定义数据集。如果你没有自己想要实验的数据集，但又想用现成的数据集做实验（例如，NeurIPS LLM Efficiency Challenge 只允许使用公开可得的数据集），下面是一些值得探索的数据集指引。

考虑到 [NeurIPS LLM Efficiency Challenge](https://llm-efficiency-challenge.github.io) 的规则，这份列表聚焦于人工生成的英文数据集，而非大语言模型生成的数据集。

**[Open Assistant](https://huggingface.co/datasets/OpenAssistant/oasst1)**（多语言）是一个由人工创建和标注的类助手对话集合。它包含 35 种语言的 161,443 条消息，并附有 461,292 条质量评价，最终形成了超过 10,000 棵标注完备的对话树。该数据集来自一项全球众包活动，共有超过 13,500 名志愿者参与。

**[Natural Instructions](https://arxiv.org/abs/2104.08773)** 是一个人工编写的英文指令数据集，包含 19.3 万条条目，覆盖 61 个不同的 NLP 任务。

**[P3 (Public Pool of Prompts)](https://arxiv.org/abs/2110.08207)** 是一个指令微调数据集，由 170 个英文 NLP 数据集和 2,052 个英文提示（prompt）构建而成。提示（有时也称任务模板）把传统 NLP 任务（如问答、文本分类）中的一个数据实例映射为一个自然语言的输入—输出配对。

**[Flan 2021](https://arxiv.org/abs/2301.13688)** 是一个英文指令数据集合集，通过把 62 个流行的 NLP 基准测试（包括 SNLI、AG News 等）转换为语言输入—输出配对而构建。

## 值得探索的研究方向

在讲清楚了指令微调的"为什么"和"怎么做"之后，我们可以探索哪些有趣的研究方向来提升开源大语言模型的性能呢？

**合并数据集**

除了上文提到的 P3 和 Flan 2021 数据集之外，我还没有见过通过组合多个来源的数据集来创建更大规模数据集的尝试。例如，尝试 LIMA 与 Dolly 等数据集的组合可能是值得做的。

**数据集顺序**

顺着上面数据集合并的思路，探索以不同顺序访问不同数据点所起的作用（例如，按指令类型排序或打乱）可能也很有意思。除了 [Pythia 论文](https://arxiv.org/abs/2304.01373)中做过的预训练实验之外，我还没有见过在指令微调场景下关于数据集顺序的研究。

**多轮（Multiple-Epoch）训练**

由于对数据集规模的要求很高，大语言模型在预训练时通常训练不到一个 epoch，也就是说它们不会多次重访同一批数据点。计算成本是原因之一，另一个原因是大语言模型容易过拟合。不过，既然我们手头有许多减少过拟合的技术，研究大语言模型场景下的多轮训练会很有意思。

例如，在 LIMA 这样的小数据集上训练大语言模型只需几分钟。那么，对数据集迭代多轮是否有意义呢？

**自动质量过滤**

把数据集过滤作为默认步骤是否有意义？

与前面讨论的 LIMA 研究相关，*[AlpaGasus: Training A Better Alpaca with Fewer Data](https://arxiv.org/abs/2307.08701)* 论文同样强调，更大的数据集并不一定有利于微调大语言模型。在 *AlpaGasus* 研究中，研究者使用 ChatGPT 来识别原始 52,000 条样本的 Alpaca 数据集中的低质量指令—响应配对。他们发现，把它缩减到仅 9,000 个高质量配对后，训练 70 亿和 130 亿参数的 Llama-v1 大语言模型时性能反而有所提升。

![Optimizing LLMs dataset perspective image11](https://sebastianraschka.com/images/blog/2023/optimizing-llms-dataset-perspective/image11.webp)
*来自 [AlpaGasus 论文](https://arxiv.org/abs/2307.08701)的标注图*

不过，正如前文提到的，[NeurIPS LLM Efficiency Challenge](https://llm-efficiency-challenge.github.io) 不允许使用大语言模型生成的数据集。因此，这个基于 Alpaca 的 Alpagasus 数据集对这项比赛没有用处。

AlpaGasus 的一个可行替代方案，是用一个大语言模型来过滤人工生成（而非大语言模型生成）的数据集。不过，我不确定基于大语言模型的数据集过滤是否被允许，因此在比赛中使用这类数据集之前，最好先在主办方的 Discord 频道上确认。

接下来的几节将讲解如何使用 LIMA 这类数据集来训练最新的开源大语言模型。此外，我还会重点介绍一些可以在 [NeurIPS LLM Efficiency Challenge](https://llm-efficiency-challenge.github.io) 中尝试的有趣研究方向。

## 结论

本文介绍了指令微调，并讲解了大语言模型生成数据集和人工生成数据集各自的优势。我们还快速过了一个教程，讲解如何用不同的数据集微调开源大语言模型，以及如何使用自己的数据集创建定制的大语言模型。与专有 API 和服务相比，这样的大语言模型可以帮助你利用公司内部的特定数据集、在特定用例上改进大语言模型，并给你完整的隐私控制权。

如果你有任何问题，欢迎随时联系：

- 如果你对 Lit-GPT 有任何建议、反馈或遇到问题，并且你认为这是一个 bug，请考虑在 [GitHub 上提交 Issue](https://github.com/Lightning-AI/lit-gpt/issues)。
- 此外，非常欢迎提交包含改进和新技术实现的 [Lit-GPT pull requests](https://github.com/Lightning-AI/lit-gpt/pulls)！

如果你正在参加 [NeurIPS LLM Efficiency Challenge](https://llm-efficiency-challenge.github.io)，我希望你和我一样觉得这项比赛有用且令人兴奋。

- 我建议从[我在这里整理的快速上手指南](https://github.com/Lightning-AI/lit-gpt/blob/main/tutorials/neurips_challenge_quickstart.md)开始。
- 关于某个特定数据集是否允许在比赛中使用的问题，我建议通过主办方的 [Discord 频道](https://discord.gg/XJwQ5ddMK7)再次确认。
- 关于与该比赛相关的 Lit-GPT 问题，我在 Lightning AI 的同事们也维护了一个 [Discord 频道](https://discord.gg/MWAEvnC5fU)。

祝学习、编程和实验愉快！
