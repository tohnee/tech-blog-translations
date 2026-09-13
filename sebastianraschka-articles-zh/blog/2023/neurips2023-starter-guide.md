---
title: "LLM Efficiency Challenge 2023 参赛指南"
title_en: "LLM Efficiency Challenge 2023 Guide"
source: https://sebastianraschka.com/blog/2023/neurips2023-starter-guide.html
crawled: 2026-09-06
translated: 2026-09-06
---

# LLM Efficiency Challenge 2023 参赛指南

> 原文：[LLM Efficiency Challenge 2023 Guide](https://sebastianraschka.com/blog/2023/neurips2023-starter-guide.html)

大语言模型（LLM）为开发更高效的训练方法提供了最有趣的机会之一。几周前，NeurIPS 2023 LLM Efficiency Challenge 开赛，聚焦高效的 LLM 微调，本指南是一份简短的实操讲解，说明如何参加这项比赛。本文涵盖你需要知道的一切，从搭建编程环境到完成首次提交。

## 1 - 什么是 NeurIPS Efficiency Challenge？

[NeurIPS 2023 Efficiency Challenge](https://llm-efficiency-challenge.github.io) 是一项专注于**用 1 块 GPU 训练 1 个 LLM 共 24 小时**的比赛——拥有最佳 LLM 的团队将获得在 NeurIPS 2023 上展示成果的机会。

像 GPT-4 这样的大语言模型能力惊人。然而，它们的开发和运行成本高昂，而且对定制大语言模型的需求也很大：

- 用于撰写草稿的个人助手（许多研究者和公司不能把敏感材料提交给 ChatGPT）；
- 面向法律、医疗或金融数据与文档的问答系统；
- 在特定领域或公司产品方面具备领域知识的客服聊天机器人。

撇开应用不谈，对于像我这样的研究者来说，这项比赛是一个非常好的机会，可以开发和尝试更高效训练 LLM 的新方法。

但在进入实操章节之前，先简要回顾一些要点和限制以获得整体认识。不过，参赛者应该查阅[官方指南](https://llm-efficiency-challenge.github.io/rules)了解所有最新细节。

![banner](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/banner.webp)

*比赛官方网站位于 <https://llm-efficiency-challenge.github.io>*

## 2 - 比赛概览

本节简要介绍 *NeurIPS 2023 Efficiency Challenge*。（我强烈建议同时查阅[官方指南](https://llm-efficiency-challenge.github.io/rules)了解所有最新细节。）

**GPU**

由于只允许使用 1 块 GPU，这项比赛是一个很好的试验场，可以专注试验高效微调技术，而不必太操心基础设施。只允许使用以下两种 Nvidia GPU：

- A100（40 GB 内存）；
- 以及 RTX 4090（24 GB 内存）。

（由于这两种 GPU 不能直接比较，比赛设有两个不同的赛道和排行榜。）

**模型**

三种 transformer LLM 架构类型都允许使用：编码器、编码器-解码器和解码器。（编码器和解码器有什么区别？我在[这里](https://magazine.sebastianraschka.com/p/understanding-encoder-and-decoder)讨论过。）

不过，我推测仅解码器（decoder-only）架构可能是最有前景的方向：

> “我们在 Wang et al. (2022a) 中探讨了这个问题，评估了编码器-解码器和仅解码器架构与因果（causal）、前缀（prefix）和掩码（masked）语言建模等[预训练](https://sebastianraschka.com/glossary/#pretraining "Pretraining")目标的交互。我们的结果表明，预训练刚结束时，因果式仅解码器模型表现最佳——这印证了最先进 LLM 的架构选择。”——引自 [BLOOM: A 176B-Parameter Open-Access Multilingual Language Model](https://arxiv.org/abs/2211.05100)

下图总结了获批准的 LLM 列表。注意，比赛聚焦于尚未（进行过）微调的基础（foundation）LLM，因为微调正是这项比赛的重点。

![Allowed LLMS](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/allowed-llms.webp)

*比赛中允许使用的模型（截至撰写时）*

**数据与任务**

选择数据集时要注意：模型不需要处理超过 2048 个 token 的上下文。评估基于斯坦福 [HELM](https://crfm.stanford.edu/helm/latest/) [基准测试](https://sebastianraschka.com/glossary/#benchmark "Benchmark")套件的一个子集，将在英文文本上进行。（我们会在本文末尾运行 HELM 基准测试。）

参赛者需提交训练和评估代码，其中应包含在"开源"数据集上用 A100 或 RTX 4090 训练[基础模型](https://sebastianraschka.com/glossary/#base-model "Base Model")最长 24 小时的所有必要步骤。截至撰写时，允许使用以下数据集：

- [Databricks-Dolly-15](https://huggingface.co/datasets/databricks/databricks-dolly-15k)（1.5 万条指令-回复对）
- [OpenAssistant Conversations Dataset (oasst1)](https://huggingface.co/datasets/OpenAssistant/oasst1)
- [Alpaca Libre](https://github.com/mobarski/alpaca-libre)

![Neurips2023 starter guide dataset](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/dataset.webp)

*来自 [Alpaca-Libre](https://github.com/mobarski/alpaca-libre) 数据集的两个示例。*

**更新：主办方刚刚禁止在比赛中使用 Alpaca-Libre，因为它违反了比赛政策——该政策规定比赛中不得使用任何 LLM 生成的数据。**

**由于本文是一篇提交教程，我尽量聚焦于从零到提交的主要流程。不过我可能会在未来的独立文章中更详细地重访某些主题，比如数据集。**

## 3 - 官方入门套件

NeurIPS 效率挑战赛的组织者选择了 [Lit-GPT](https://github.com/Lightning-AI/lit-gpt) 仓库作为官方入门套件——这是一个开源 GitHub 仓库，实现了加载流行 LLM 的方法和工具（见下表）。这对我很方便，因为我过去对该仓库有过一些贡献，包括实现 LLaMA-Adapter v2、全量微调、移植[低秩适应](https://sebastianraschka.com/glossary/#lora "LoRA (Low-Rank Adaptation)")（LoRA）、协作实现 QLoRA 等等。

同样值得一提的是，Lit-GPT 实现了与本次比赛最相关的 LLM，如下表所示：

| Lit-GPT 中的模型 | 参考文献 |
| --- | --- |
| Meta AI Llama 2 | [Touvron et al. 2023](https://arxiv.org/abs/2307.09288) |
| Stability AI FreeWilly2 | [Stability AI 2023](https://stability.ai/blog/stable-beluga-large-instruction-fine-tuned-models) |
| TII UAE Falcon | [TII 2023](https://falconllm.tii.ae) |
| OpenLM Research OpenLLaMA | [Geng & Liu 2023](https://github.com/openlm-research/open_llama) |
| LMSYS Vicuna | [Li et al. 2023](https://lmsys.org/blog/2023-06-29-longchat) |
| Together RedPajama-INCITE | [Together 2023](https://together.ai/blog/redpajama-models-v1) |
| EleutherAI Pythia | [Biderman et al. 2023](https://arxiv.org/abs/2304.01373) |
| StabilityAI StableLM | [Stability AI 2023](https://github.com/Stability-AI/StableLM) |

截至撰写时，我建议聚焦 Llama 2，或许还有 Falcon，因为根据公开排行榜，这两个模型系列目前最有前景。（为了让本指南聚焦于提交流程，更详细的模型讨论留待未来的文章。）

**在接下来的章节中，我将带你一步步搭建计算环境、配置 Lit-GPT 仓库，以便开展实验和提交！**

*注意，并不要求使用组织者建议的这个 Lit-GPT 入门套件。另外请注意，组织者与该仓库或其开发者并无关联，而是独立选择了它——这很可能是因为它相对易于定制、便于"魔改"，在尝试新研究想法时会很趁手。*

## 4 - 搭建项目环境

就个人而言，我喜欢为手头的每个研究项目创建专用的虚拟环境，这有助于我管理特定的版本号等。为此，我（至今）仍然偏爱使用 [conda 包管理器](https://docs.conda.io/en/latest/)。本节中，我会带你走一遍我惯用的搭建流程。（如果你已经习惯使用 `conda`、`venv` 或任何其他虚拟环境方案，可以跳过本节。）

在你计划运行实验的机器上，下载 [miniconda](https://docs.conda.io/en/latest/miniconda.html) 或 [miniforge](https://github.com/conda-forge/miniforge)。如果你用的是 Linux 电脑，那大概就是下面截图中的第一行、最顶上那一个。

![Neurips2023 starter guide miniforge](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/miniforge.webp)

*Miniforge 安装选项*

然后执行相应的 shell 脚本并按照提示操作，即可安装 conda 包管理器：

```python
sh Miniforge3-Linux-x86_64.sh
```

接下来，创建一个新的 conda 环境：

```python
conda create -n neurips2023-1 python=3.10 --yes
```

安装完成后，激活环境：

```python
conda activate neurips2023-1
```

![Neurips2023 starter guide conda activate](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/conda-activate.webp)

在远程机器上工作时，我还喜欢使用 [tmux](https://github.com/tmux/tmux/wiki)，这样万一断线重连也能恢复终端会话：

```python
tmux new -s neurips-1
cd ~/Developer/neurips23
conda activate neurips2023-1
```

这样，每次断线后，我都可以重新登录机器，并通过以下命令恢复会话：

```python
tmux attach -t neurips-1
```

## 5 - 安装依赖

为 NeurIPS 比赛搭好虚拟环境之后，现在可以克隆 Lit-GPT 仓库并安装相应依赖了。首先，克隆 [Lit-GPT](https://github.com/Lightning-AI/lit-gpt) GitHub 仓库：

```python
git clone https://github.com/Lightning-AI/lit-gpt.git
```

该仓库包含一个 [requirements.txt](https://github.com/Lightning-AI/lit-gpt/blob/main/requirements.txt) 文件，列出了使用仓库代码所需的来自 [PyPI](https://pypi.org/) 的 Python 包。但注意，Lit-GPT 用到了最新的 PyTorch 特性，因此我们必须安装 PyTorch nightly 版本（遗憾的是，它无法通过 requirements.txt 文件安装）。

我们可以在 [pytorch.org 安装菜单](https://pytorch.org/)中选择并运行相应的命令来安装最新的 PyTorch 版本，如下面截图所示。

![The PyTorch installation menu](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/pytorch-nightly.webp)

*PyTorch 安装菜单*

接下来，我们可以用 `pip` 通过以下命令安装其余依赖：

```python
cd lit-gpt
pip install -r requirements.txt
```

## 6 - 下载模型检查点

截至撰写时，我建议把 Meta 新发布的 [Llama 2](https://arxiv.org/abs/2307.09288) 作为最有前景的基础模型。为简单起见，聚焦 70 亿参数版本可能比较合理——使用参数高效微调技术时，它应该能装进 24 GB 的 RTX 4090 或 40 GB 的 A100 GPU。（如果想下载其他模型，请参阅 [Lit-GPT 教程](https://github.com/Lightning-AI/lit-gpt/tree/main/tutorials)。）

我们可以使用 Lit-GPT 仓库提供的 scripts/download.py 脚本下载 7B 的 Llama 2 基础模型。下载的文件大约需要 13 GB 磁盘空间。

不过，首先你需要完成以下步骤：

1. 在 <https://huggingface.co/meta-llama/Llama-2-7b> 创建 Hugging Face（HF）账号。
2. 在 <https://huggingface.co/meta-llama/Llama-2-7b> 申请 Llama-2 访问权限。
3. [获取你的 HF token](https://huggingface.co/settings/tokens)，你可以在 <https://huggingface.co/settings/tokens> 生成它。

![Neurips2023 starter guide hf](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/hf.webp)

接下来，要下载 Llama 7B 模型，我们需要通过 `--token` 参数提供 HF token，如下所示：

```python
cd ~/Developer/neurips23/lit-gpt
pip install huggingface_hub
python scripts/download.py --repo_id meta-llama/Llama-2-7b-hf --token your_hf_token
```

（这里的 `your_hf_token` 是你可以在 HF 网站的用户账户中复制的 token。）

如果你看到如下消息

> Your request to access model meta-llama/Llama-2-7b-hf is awaiting a review from the repo authors.

那么可能就需要等待（目前是 1-2 天）审核批准。

好消息是，在此期间我们可以使用 7B 的 OpenLLaMA 模型，它不需要身份验证：

```python
python scripts/download.py --repo_id openlm-research/open_llama_7b
```

![Neurips2023 starter guide openllama](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/openllama.webp)

（你也可以通过 `--repo_id openlm-research/open_llama_3b` 使用更小的 30 亿参数版本进行实验。）

默认情况下，检查点文件会保存在 Lit-GPT 仓库内的本地目录 `checkpoints/` 中。

接下来，我们把下载的文件转换成 Lit-GPT 中所有模型共用的权重格式：

```python
python scripts/convert_hf_checkpoint.py --checkpoint_dir checkpoints/openlm-research/open_llama_7b
```

在准备数据集和微调模型之前，先用相应的 `generate` 脚本确认它能正常工作：

```python
python generate/base.py --checkpoint_dir checkpoints/openlm-research/open_llama_7b --prompt "Tell me an interesting fun fact:"
```

注意，基础模型是作为文本补全模型训练的，这与经过指令微调、可用于对话的模型不同。我们这里使用基础模型，因为微调正是比赛的一部分。不过可以看到，尽管该模型只训练过预测下一个词，它也能给出有趣的回答：

![Tip: Using Symlinks](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/prompt-response.webp)

**技巧：使用符号链接**

你可能迟早会想创建多个项目文件夹。我建议使用[符号链接（symbolic link）](https://en.wikipedia.org/wiki/Symbolic_link)，以避免重新下载或复制原始模型检查点或数据集。例如，如果模型检查点放在共享目录 `/shared/data/checkpoints` 中，你可以在 `lit-gpt` 仓库内按如下方式创建符号链接：

```python
cd ~/Developer/neurips23/experiment1/lit-gpt
ln -s /shared/data/checkpoints checkpoints
```

（你可以用同样的 `ln -s` 命令为你的数据集创建符号链接。）

## 7 - 下载并准备数据集

我强烈建议查看[官方规则](https://llm-efficiency-challenge.github.io/challenge)，了解允许使用的模型和数据集的最新信息。如前所述，截至撰写时，允许使用以下数据集：

- [Databricks-Dolly-15](https://huggingface.co/datasets/databricks/databricks-dolly-15k)
- [OpenAssistant Conversations Dataset (oasst1)](https://huggingface.co/datasets/OpenAssistant/oasst1)
- [Alpaca Libre](https://github.com/mobarski/alpaca-libre)

**更新：主办方刚刚禁止在比赛中使用 Alpaca-Libre，因为它违反了政策——政策规定比赛中不得使用任何 LLM 生成的数据。**

为简单起见，本次比赛我们将使用 Alpaca Libre——本文开头的*数据与任务*一节中简要介绍过它。可以按如下方式下载，它会把原始 .json 文件转换为 PyTorch 张量格式，以加速后续的数据加载：

```python
python scripts/prepare_alpaca_libre.py --checkpoint_dir checkpoints/openlm-research/open_llama_7b/
```

（这应该很快；处理后的 Alpaca-Libre 数据集保存在 `./data/alpaca_libre/` 下，大约占用 120 Mb。）

**注意：** 如果你的仓库中还没有 prepare_alpaca_libre.py 文件，那很可能是因为我刚把它提交给 Lit-GPT，还没有合并。这种情况下，你可以从[这个 PR](https://github.com/Lightning-AI/lit-gpt/pull/358) 下载，或者改用 scripts/prepare_alpaca.py 来处理常规 Alpaca 数据集。

**注意：** 如果你以后打算换用别的模型，就需要用不同的 –checkpoint_dir 标志重新准备数据集，因为不同模型可能使用不同的分词器。

## 8 - 建立微调基线

完成上一节介绍的数据集准备步骤之后，我们现在可以进入更有意思的部分——微调模型。这正是发挥创造力的地方：组合或构思新的研究想法，以提升基础模型的建模性能。

我计划在后续文章中写一些值得尝试的有趣研究方向。为了让本指南聚焦主要步骤，这里我们专注于建立一个性能基线。为此，我们选用 OpenLLaMA 7B 模型，使用低秩适应（LoRA）在 Alpaca-Libre 数据集上进行微调：

```python
python finetune/lora.py \
--data_dir data/alpaca_libre/ \
--checkpoint_dir checkpoints/openlm-research/open_llama_7b/ \
--precision bf16-true
```

（可以通过 `python finetune/lora.py --help` 查看更多选项。）

使用默认设置，即微批大小（microbatch size）为 4、[上下文长度](https://sebastianraschka.com/glossary/#context-length "Context Length")为 2048、以及如上所示的 bf16-true 精度（后文会解释），在 A100 上耗时约 7 小时 28 分：

```python
{'eval_interval': 100, 'save_interval': 100, 'eval_iters': 100, 'log_interval': 1, 'devices': 1, 'learning_rate': 0.0003, 'batch_size': 128, 'micro_batch_size': 4, ...}
Global seed set to 1337

Loading model 'checkpoints/openlm-research/open_llama_7b/lit_model.pth' with {'org': 'openlm-research', 'name': 'open_llama_7b', 'block_size': 2048, 'vocab_size': 32000, ...}

Number of trainable parameters: 4,194,304
Number of non trainable parameters: 6,738,415,616

Validating ...

...

Estimated TFLOPs: 357.80
Measured TFLOPs: 324.99
...
iter 30 step 0: loss 1.9667, iter time: 92.21ms
iter 31 step 1: loss 1.9221, iter time: 196.06ms (optimizer.step)
iter 32 step 1: loss 1.0282, iter time: 199.56ms
iter 33 step 1: loss 1.3246, iter time: 136.38ms
iter 34 step 1: loss 2.0406, iter time: 94.96ms
iter 35 step 1: loss 2.2522, iter time: 84.61ms
iter 36 step 1: loss 1.4814, iter time: 113.93ms
iter 37 step 1: loss 1.7872, iter time: 92.81ms
...

...
iter 49990 step 1562: loss 0.5110, iter time: 84.79ms
iter 49991 step 1562: loss 0.5513, iter time: 147.55ms
iter 49992 step 1562: loss 0.4352, iter time: 134.89ms
iter 49993 step 1562: loss 0.3533, iter time: 101.12ms
iter 49994 step 1562: loss 0.4636, iter time: 166.13ms
iter 49995 step 1562: loss 0.5932, iter time: 96.34ms
iter 49996 step 1562: loss 0.4907, iter time: 131.20ms
iter 49997 step 1562: loss 0.4948, iter time: 135.04ms
iter 49998 step 1562: loss 0.5330, iter time: 84.70ms
iter 49999 step 1562: loss 0.4570, iter time: 100.29ms
Training time: 26239.77s
Saving LoRA weights to 'out/lora/alpaca/lit_model_lora_finetuned.pth'
```

就个人习惯而言，我还喜欢在所有脚本中加入下面这一行，这样训练结束后就能看到最大内存占用：

```python
print(f"Memory used: {torch.cuda.max_memory_allocated() / 1e9:.02f} GB", file=sys.stderr)
```

![Neurips2023 starter guide memory alloc](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/memory-alloc.webp)

对于上面的模型，它会打印出：

```python
Memory used: 28.81 GB
```

考虑到比赛允许使用 40 GB 内存的 A100 GPU，这告诉我们还可以增加可训练参数的数量、微批大小或其他设置，把内存占用再提高约 11 GB，以充分利用这块 GPU。

顺便一提，通过[这个 Pull Request](https://github.com/Lightning-AI/lit-gpt/pull/275)，应该也支持用 `--quantize "bnb.nf4"` 进行类 QLoRA 的微调。这会把内存占用降到 17.04 GB，让你可以在 RTX 4090 上运行。如果你使用 RTX 4090，后面几节还会有更多降低内存需求的技巧。

## 9 - 使用模型

为了用提示词快速检验模型，我们可以像下面这样使用 `generate/lora.py` 脚本：

```python
python generate/lora.py --prompt "how do you make pizza?" \
--checkpoint_dir '/home/sebastian/Developer/neurips23/lit-gpt/checkpoints/openlm-research/open_llama_7b'
```

![Neurips2023 starter guide pizza](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/pizza.webp)

这里我们主要想确认模型能生成连贯的文本输出。看起来不错。本文后面还会回到模型评估的话题。

## 10 - 调整微调设置

在前面的章节中，我们用默认设置微调并使用了基础模型。当然，如果真想在比赛中*一较高下*，就需要做一些改动。我计划在未来的文章中讨论研究方向，但现在先简要介绍几个设置，帮助你充分利用现有代码。

前面的*建立微调基线*一节提到过微批大小为 4、上下文长度为 2048 等默认设置。这些可以直接在脚本顶部修改：

![default-script](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/default-script.webp)

我们来讨论其中一些设置的含义。

**`*_interval` 设置**

`*_interval` 设置用于指定模型评估和保存的频率。这在开发模型时很有用。不过，在提交之前，最好把这个数字调大一些，以省下几秒或几分钟。

**`devices`**

`devices` 指定使用多少个设备。如果这个数字大于 2，它会使用全分片数据并行（fully-sharded data parallelism），即 a）运行数据并行，并且 b）把大层切分到多块 GPU 上。如果你有兴趣，我在[深度学习课程的第 9.2 和 9.3 单元](https://lightning.ai/courses/deep-learning-fundamentals/9.0-overview-techniques-for-speeding-up-model-training/unit-9.2-multi-gpu-training-strategies/)中对多 GPU 训练有更多讲解。

![Neurips2023 starter guide tensor parallelism](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/tensor-parallelism.webp)

不过，由于比赛限制只能用 1 块 GPU，这里我们不必操心这个设置，保持 `devices=1` 即可。

**`override_max_seq_length`**

设置 `override_max_seq_length=None` 意味着使用模型的默认上下文长度。对 OpenLLaMA 来说是 `2048`，恰好也是比赛允许的最大长度。所以在这种情况下，如果你打算尝试不同的模型（想要提交有竞争力的结果，你多半应该这么做），最好设置为 `override_max_seq_length=2048`。

**`learning_rate`**

`learning_rate` 是一个需要我们反复琢磨的超参数。通常，我们通过监控损失并在验证集上评估模型来确定它。学习率调优的详细讨论超出了本文的范围，但你可以看看我深度学习课程的[第 6.2 单元——学习率与学习率调度器](https://lightning.ai/courses/deep-learning-fundamentals/unit-6-overview-essential-deep-learning-tips-tricks/unit-6.2-learning-rates-and-learning-rate-schedulers/)。

**`batch_size` 与 `micro_batch_size`**

由于模型使用了梯度累积，这里有两个批大小设置：`batch_size` 和 `micro_batch_size`。`micro_batch_size` 是模型每次前向传播实际接收的批大小；`batch_size` 决定反向传播时模型更新所用的实际批大小。

换句话说，如果 `batch_size` 设为 128、`micro_batch_size` 设为 4，模型会执行 32 次前向传播（128 / 4 = 32）来为每次反向传播累积损失。不过，模型性能和梯度更新与常规训练完全相同。我们可以把梯度累积看作一种节省内存的技巧。如果想进一步了解梯度累积，可以看我的博文《[Finetuning LLMs on a Single GPU Using Gradient Accumulation](https://sebastianraschka.com/blog/2023/llm-grad-accumulation.html)》。

![gradient-accum](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/gradient-accum.webp)

*梯度累积示意图，来自 [Finetuning LLMs on a Single GPU Using Gradient Accumulation](https://sebastianraschka.com/blog/2023/llm-grad-accumulation.html)*

如果把 `micro_batch_size` 从 4 改为 2，可以显著节省计算内存而不牺牲建模性能，但也会增加运行时间。这是参赛过程中必须牢记的权衡。

**`lora_*` 参数**

`lora_*` 系列参数设置 LoRA 的可训练参数。例如，把 `lora_key` 从 `False` 改为 `True`，就会在 value 和 query 权重之外，为 LLM 的 *key* 权重也启用 LoRA。实践中，这可以让性能更接近全量微调。

下面是我根据上述讨论选择的几个设置，总内存占用为 23.66 GB，代码因此既能在 RTX4090 上运行，也能在 A100 上运行：

![Neurips2023 starter guide lora changes](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/lora-changes.webp)

截图中 `max_iter` 设为 100 是为了快速实验，这意味着脚本大约 2 分钟就能跑完。不过，对于"真正的"训练，迭代次数应至少与数据集中的记录数相当（Alpaca 或 Alpaca-Libre 是 5 万条）。

**关于全量微调的说明**

7B 的 OpenLLaMA 模型有 6,738,415,616 个参数。然而在 LoRA 脚本中只有一小部分参数是可训练的（默认 4,194,304 个），这实现了参数高效微调。为什么不微调整个模型？因为它会消耗大量内存。我没能把全量微调塞进单块 A100。

事实上，我需要 6 块 GPU 和张量分片才能跑起来。下面是我《[Finetuning Falcon LLMs More Efficiently With LoRA and Adapters](https://sebastianraschka.com/blog/2023/falcon-finetuning.html)》一文中的一组基准测试：

![Neurips2023 starter guide falcon](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/falcon.webp)

## 11 - 避免内存溢出错误

正如前面暗示的，这项比赛的主要挑战之一是避免内存溢出（out-of-memory）错误，因为我们的 GPU 内存有限。上文简要讨论了梯度累积、量化、选择更小的基础模型以及 LoRA 等技巧。

还有许多额外的技巧，包括自动混合精度训练、低精度浮点数、高效的模型初始化、选择更精简的优化器以及参数卸载（offloading）。逐一讨论这些技术超出了本文的范围，但第一个好消息是，其中大部分已经在 Lit-GPT 代码中实现了。

第二个好消息是，我有一篇独立文章更详细地讨论了所有这些方法：《[Optimizing Memory Usage for Training LLMs and Vision Transformers in PyTorch](https://sebastianraschka.com/blog/2023/pytorch-memory-optimization.html)》。

![来自 [Optimizing Memory Usage for Training LLMs and Vision Transformers in PyTorch](https://sebastianraschka.com/blog/2023/pytorch-memory-optimization.html) 的内存优化技巧](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/memory-tricks.webp)

*内存优化技巧，来自 [Optimizing Memory Usage for Training LLMs and Vision Transformers in PyTorch](https://sebastianraschka.com/blog/2023/pytorch-memory-optimization.html)*

《[Optimizing Memory Usage for Training LLMs and Vision Transformers in PyTorch](https://sebastianraschka.com/blog/2023/pytorch-memory-optimization.html)》一文还介绍了 Lightning 的 [Fabric](https://lightning.ai/docs/fabric/stable/)——一个用于便捷加速 PyTorch 模型训练的开源库，Lit-GPT 内部就用它来减少样板代码。

## 12 - 研究方向

最初，我计划写一个详尽的章节，介绍本次比赛中值得探索的研究想法和方向。不过，鉴于本文已经（几乎过分地）长，这些内容留待以后的文章。与此同时，你或许可以在我的 Research Highlights 系列中找到一些灵感：[2023 年 6-7 月](https://magazine.sebastianraschka.com/p/ai-research-highlights-in-3-sentences-738)、[2023 年 5-6 月](https://magazine.sebastianraschka.com/p/ai-research-highlights-in-3-sentences-2a1)和 [2023 年 4-5 月](https://magazine.sebastianraschka.com/p/ai-research-highlights-in-3-sentences)。

## 13 - 在本地评估模型

写到这里，大多数读者大概已经读完这篇长篇入门指南，迫不及待想自己动手了。不过还有一件值得讨论的事：评估建模性能！我保证这部分会简短（并且我计划以后写一篇更详细的评估文章）。

比赛提交将在[斯坦福 HELM 基准测试](https://crfm.stanford.edu/helm/latest/)的一个子集上评估，该套件包含 42 个场景和 59 个指标。

其中包括 [HellaSwag](https://crfm.stanford.edu/helm/latest/?group=hellaswag) 和 [TruthfulQA](https://crfm.stanford.edu/helm/latest/?group=truthful_qa) 等场景，它们也出现在其他基准测试中，例如 EleutherAI 的 [Language Model Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness)。

为了避免过拟合，或许可以先用 Evaluation Harness 中的几个任务来开发模型（把它们当作验证集），然后再把它们应用到 HELM 基准上。由于比赛评估将基于 HELM 的一个子集，我们可以把 HELM 更多地当作测试集。

Lit-GPT 目前直接支持 Language Model Evaluation Harness（并且 [HELM 支持也在开发中](https://github.com/Lightning-AI/lit-gpt/pull/370)）。我们来简要看看如何在 Lit-GPT 中使用 Evaluation Harness。

首先，我们需要克隆并安装官方的 Evaluation Harness 仓库：

```python
git clone https://github.com/EleutherAI/lm-evaluation-harness
cd lm-evaluation-harness
pip install -e .
cd ..
```

（注意，`pip install -e .` 会进行本地安装并运行 `python setup.py develop`，这样对 `lm-evaluation-harness` 包的修改就不需要重新安装。）

然后，要评估 OpenLLaMA 模型，我们可以在 `lit-gpt` 仓库中按如下方式对检查点文件运行 harness：

```python
python eval/lm_eval_harness.py \
  --checkpoint_dir "checkpoints/openlm-research/open_llama_7b/" \
  --precision "bf16-true" \
  --eval_tasks "[truthfulqa_mc]" \
  --batch_size 4 \
  --save_filepath "results-openllama-7b.json"
```

这应该只需要 5 分钟就能跑完。

（对于 LoRA 微调过的模型，Lit-GPT 仓库中有一个对应的 `lm_eval_harness_lora.py` 脚本。）

如果想包含多个任务，比如 HellaSwag 和 TruthfulQA，可以把 `[truthfulqa_mc]` 替换为 `[truthfulqa_mc,hellaswag]`。**完整任务列表见[这里的任务表](https://github.com/EleutherAI/lm-evaluation-harness/blob/master/docs/task_table.md)。**

![Small excerpt of the tasks supported in the Evaluation Harness](https://sebastianraschka.com/images/blog/2023/neurips2023-starter-guide/tasks.webp)

*Evaluation Harness 所支持任务的一小部分摘录*

这会得到如下 JSON 输出：

```python
{"results": 
    {"truthfulqa_mc": 
        {"mc1": 0.23133414932680538, 
         "mc1_stderr": 0.014761945174862673, 
         "mc2": 0.352784342017196, 
         "mc2_stderr": 0.01356224149206526}}, 
         "versions": {"truthfulqa_mc": 1}, 
         "config": {"model": "open_llama_7b", "num_fewshot": 0, 
        					   "batch_size": 4, "device": "cuda:0", 
        					   "no_cache": true, "limit": null, 
        					   "bootstrap_iters": 2, "description_dict": null
}}
```

所得的 `mc1` 和 `mc2` 分数衡量模型生成真实陈述的频率比例（范围为 0 到 1）。mc1 与 mc2 分数的区别在 [TruthfulQA](https://github.com/sylinrl/TruthfulQA) 仓库中解释如下：

- “**MC1（Single-true，单真）**：给定一个问题和 4-5 个答案选项，选出唯一正确的答案。模型的选择是它在问题之后赋予最高补全对数概率的那个答案选项，且独立于其他答案选项。分数是所有问题上的简单准确率。”
- “**MC2（Multi-true，多真）**：给定一个问题和多个真/假参考答案，分数是分配给真答案集合的归一化总概率。”

TruthfulQA 会用于最终模型评估吗？很可能不会。我在这里只是把它作为简单的参考。注意，Llama 2 Chat 模型（由于已经微调过，不允许参加本次比赛）可以作为好成绩的参考。

作为对比，我们可以在 Llama 2 7b [对话模型](https://sebastianraschka.com/glossary/#instruct-model "Instruct Model")上运行同样的评估代码，如下所示：

```python
python eval/lm_eval_harness.py \
   --checkpoint_dir "checkpoints/meta-llama/Llama-2-7b-chat-hf/" \
   --precision "bf16-true" \
   --eval_tasks "[truthfulqa_mc]" \
   --batch_size 4 \
   --save_filepath "results-llama2-7b.json"
```

结果得到 mc1 和 mc2 分数分别为 `0.306` 和 `0.454`。这听起来不算好：0.3 意味着只有 30% 的回答是真实的。不过作为对比，根据 [TruthfulQA](https://github.com/sylinrl/TruthfulQA) 仓库的数据，大 25 倍的 175B GPT-3 模型也只达到了 21%。

## 14 - 提交作品

比赛目前只允许提交 3 次。因此，我强烈建议先在本地开发好模型，再进行首次提交（比赛截止日期目前列为 2023 年 10 月 15 日）。

如前所述，你可以使用 Evaluation Harness 进行模型评估。此外，HELM 评估很快也会加入 Lit-GPT，这对于在提交前评估你的最终候选模型会很有用。

至于提交本身，你需要提交一个 Docker 镜像。所幸，组织者在[这里](https://github.com/llm-efficiency-challenge/neurips_llm_efficiency_challenge)维护了一个 GitHub 仓库，包含确切的步骤，还有一份玩具提交（toy-submission）设置指南，供你在提交前于本地测试模型。（考虑到代码示例将来可能过时，我建议先查阅[官方比赛仓库](https://github.com/llm-efficiency-challenge/neurips_llm_efficiency_challenge)。）

注意，组织者还维护了一个 [Discord 频道](https://discord.gg/XJwQ5ddMK7)，用于解答关于比赛的其他问题。

## 结语

我对研究界开发（更）高效的 LLM 微调方法感到非常兴奋。也希望你觉得这项比赛和我一样有用、令人兴奋。请把这个比赛传播出去——参与的人越多，我们就能越大地推进高效 LLM 研究领域。

如果你有任何问题，以下是一些最好的联系方式：

- 如果你遇到 Lit-GPT 的问题，并认为它是 bug，请[考虑在 GitHub 上提交 Issue](https://github.com/Lightning-AI/lit-gpt/issues)。
- 如果你发现本文代码有任何问题，也可以提交 issue 并用我的 [GitHub 账号 @rasbt](https://github.com/rasbt) 艾特我，或[通过社交媒体联系我](https://x.com/rasbt)——我非常乐意修复！
- 关于挑战赛的 Lit-GPT 相关问题，我在 Lightning AI 的同事们也[在这里](https://discord.com/channels/1077906959069626439/1134560480795570186)维护了一个 Discord 频道。
- 此外，非常欢迎包含改进和新技术实现的 [Lit-GPT pull request](https://github.com/Lightning-AI/lit-gpt/pulls)！

祝编程和实验愉快！
